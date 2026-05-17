"""
Train WM (wrong-model) sub-head on sentence-transformers embeddings
(all-MiniLM-L6-v2) — mirrors cpal_train_lp_st.py but for WM classification.

The HVSAE-latent WM head (cpal_wm_subhead.pt) plateaued at val_acc ~0.04
on the 60-class task because (a) 25/60 wm_ids had no training data in
gen_cache.json and (b) the frozen HVSAE latent under-separated the
similar-belief misconceptions. ST embeddings + a fully-populated corpus
fix both.

Reads:
  data/mental_models/gen_cache.json (filled by cpal_gen_corpus.py)
Saves:
  checkpoints/cpal_wm_subhead_st.pt

LPDiagnostician prefers this file over cpal_wm_subhead.pt when present.
"""
import os, sys, json, time
from pathlib import Path
import torch
import torch.nn as nn

ROOT = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, str(ROOT))

CHECKPOINT_DIR = ROOT / "checkpoints"
CACHE_PATH     = ROOT / "data" / "mental_models" / "gen_cache.json"
CATALOGUE_PATH = ROOT / "data" / "mental_models" / "wrong_models_catalogue.json"
WM_ST_PATH     = CHECKPOINT_DIR / "cpal_wm_subhead_st.pt"


class MLPHead(nn.Module):
    def __init__(self, in_dim, hidden, num_classes, dropout=0.4):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(in_dim, hidden), nn.ReLU(), nn.Dropout(dropout),
            nn.Linear(hidden, hidden // 2), nn.ReLU(), nn.Dropout(dropout),
            nn.Linear(hidden // 2, num_classes),
        )
    def forward(self, x): return self.net(x)


def build_label_space():
    with open(CATALOGUE_PATH, encoding="utf-8") as f:
        cat = json.load(f)
    labels = []
    for cid in sorted(cat["concepts"].keys()):
        for wm in cat["concepts"][cid].get("wrong_models", []):
            labels.append((cid, wm["id"]))
    return labels


def load_corpus(labels):
    with open(CACHE_PATH, encoding="utf-8") as f:
        cache = json.load(f)
    label_to_id = {t: i for i, t in enumerate(labels)}
    examples = []
    missing = []
    for cid, wm_id in labels:
        key = f"wm|{cid}|{wm_id}"
        lines = cache.get(key, [])
        if not lines:
            missing.append(key)
            continue
        for t in lines:
            if isinstance(t, str) and t.strip():
                examples.append({"text": t.strip(),
                                  "concept": cid,
                                  "wm_id": wm_id,
                                  "label_id": label_to_id[(cid, wm_id)]})
    return examples, missing


def main():
    print("[1/3] Loading label space + corpus")
    labels = build_label_space()
    examples, missing = load_corpus(labels)
    print(f"    {len(labels)} WM classes; corpus={len(examples)} examples")
    if missing:
        print(f"    WARN: {len(missing)} WM classes have no training data yet:")
        for m in missing[:10]:
            print(f"      - {m}")
        if len(missing) > 10:
            print(f"      ... +{len(missing)-10} more")
        print("    Run scripts/cpal_gen_corpus.py first to fill them.")

    print("[2/3] Encoding with sentence-transformers/all-MiniLM-L6-v2")
    from sentence_transformers import SentenceTransformer
    st = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    t0 = time.time()
    texts = [e["text"] for e in examples]
    feats = st.encode(texts, convert_to_tensor=True, show_progress_bar=False,
                      batch_size=64).cpu().float()
    y = torch.tensor([e["label_id"] for e in examples], dtype=torch.long)
    print(f"    encoded in {time.time()-t0:.1f}s, feats={tuple(feats.shape)}")

    print("[3/3] Training WM head")
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    feats = feats.to(device); y = y.to(device)
    rng = torch.Generator().manual_seed(42)
    n = feats.size(0)
    perm = torch.randperm(n, generator=rng)
    n_val = max(1, int(n * 0.15))
    val_idx, train_idx = perm[:n_val], perm[n_val:]
    head = MLPHead(feats.size(1), 256, len(labels)).to(device)
    opt = torch.optim.Adam(head.parameters(), lr=1e-3, weight_decay=1e-3)
    loss_fn = nn.CrossEntropyLoss()
    best_val, best_state = 0.0, None
    EPOCHS, BATCH = 80, 128
    print(f"    device={device}  train={len(train_idx)}  val={len(val_idx)}  "
          f"classes={len(labels)}")
    for ep in range(1, EPOCHS + 1):
        head.train()
        shuf = train_idx[torch.randperm(len(train_idx), generator=rng)]
        tot_loss, tot_correct = 0.0, 0
        for i in range(0, len(shuf), BATCH):
            idx = shuf[i:i+BATCH]
            logits = head(feats[idx])
            loss = loss_fn(logits, y[idx])
            opt.zero_grad(); loss.backward(); opt.step()
            tot_loss += loss.item() * len(idx)
            tot_correct += (logits.argmax(dim=-1) == y[idx]).sum().item()
        train_acc = tot_correct / len(shuf)
        head.eval()
        with torch.no_grad():
            va = (head(feats[val_idx]).argmax(dim=-1) == y[val_idx]).float().mean().item()
        if ep % 10 == 0 or ep == 1:
            print(f"    epoch {ep:3d}: loss={tot_loss/len(shuf):.3f} "
                  f"train_acc={train_acc:.3f}  val_acc={va:.3f}")
        if va > best_val:
            best_val = va
            best_state = {k: v.detach().clone() for k, v in head.state_dict().items()}
    chance = 1.0 / len(labels)
    print(f"    best val_acc = {best_val:.3f}  ({best_val/chance:.1f}x chance)")
    if best_state is not None:
        head.load_state_dict(best_state)
    head = head.cpu()

    torch.save({
        "state_dict":   head.state_dict(),
        "in_dim":       feats.size(1),
        "num_classes":  len(labels),
        "labels":       labels,
        "encoder":      "sentence-transformers/all-MiniLM-L6-v2",
        "num_examples": len(examples),
        "val_acc":      best_val,
    }, WM_ST_PATH)
    print(f"Saved: {WM_ST_PATH}")


if __name__ == "__main__":
    main()
