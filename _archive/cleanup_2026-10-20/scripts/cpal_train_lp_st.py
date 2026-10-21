"""
Train LP head on sentence-transformers embeddings (all-MiniLM-L6-v2)
rather than HVSAE latent. This encoder was trained on semantic-
similarity objectives, so it should separate reasoning styles
(L1 surface vs L4 transfer) better than HVSAE's content encoder.

Saves to checkpoints/cpal_lp_head_st.pt — orthogonal to the HVSAE head.
LPDiagnostician will prefer this one when present.
"""
import os, sys, json, time
from pathlib import Path
import torch
import torch.nn as nn

ROOT = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, str(ROOT))

CHECKPOINT_DIR = ROOT / "checkpoints"
CACHE_PATH     = ROOT / "data" / "mental_models" / "gen_cache.json"
LP_ST_PATH     = CHECKPOINT_DIR / "cpal_lp_head_st.pt"

LP_LEVELS    = ["L1", "L2", "L3", "L4"]
LP_LVL_TO_ID = {lvl: i for i, lvl in enumerate(LP_LEVELS)}


class MLPHead(nn.Module):
    def __init__(self, in_dim, hidden, num_classes, dropout=0.4):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(in_dim, hidden), nn.ReLU(), nn.Dropout(dropout),
            nn.Linear(hidden, hidden // 2), nn.ReLU(), nn.Dropout(dropout),
            nn.Linear(hidden // 2, num_classes),
        )
    def forward(self, x): return self.net(x)


def main():
    print("[1/3] Loading sentence-transformers encoder")
    from sentence_transformers import SentenceTransformer
    st = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

    print("[1/3] Loading LP corpus from cache")
    with open(CACHE_PATH, encoding="utf-8") as f:
        cache = json.load(f)
    examples = []
    for key, lines in cache.items():
        parts = key.split("|")
        if len(parts) != 3 or parts[0] != "lp": continue
        _, concept, level = parts
        if level not in LP_LVL_TO_ID: continue
        for t in lines:
            if isinstance(t, str) and t.strip():
                examples.append({"text": t.strip(),
                                  "concept": concept,
                                  "lp_level": level})
    per_class = {}
    for e in examples:
        per_class[e["lp_level"]] = per_class.get(e["lp_level"], 0) + 1
    print(f"    {len(examples)} examples, per-class: {per_class}")

    print("[2/3] Encoding with sentence-transformers")
    t0 = time.time()
    texts = [e["text"] for e in examples]
    # SBERT encodes in batches by default — fast
    feats = st.encode(texts, convert_to_tensor=True, show_progress_bar=False,
                      batch_size=64)
    feats = feats.cpu().float()
    labels = torch.tensor([LP_LVL_TO_ID[e["lp_level"]] for e in examples],
                          dtype=torch.long)
    print(f"    encoded in {time.time()-t0:.1f}s, feats={tuple(feats.shape)}")

    print("[3/3] Training LP head")
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    feats  = feats.to(device)
    labels = labels.to(device)
    rng = torch.Generator().manual_seed(42)
    n = feats.size(0)
    perm = torch.randperm(n, generator=rng)
    n_val = max(1, int(n * 0.15))
    val_idx, train_idx = perm[:n_val], perm[n_val:]

    head = MLPHead(feats.size(1), 128, 4).to(device)
    opt = torch.optim.Adam(head.parameters(), lr=1e-3, weight_decay=1e-3)
    loss_fn = nn.CrossEntropyLoss()
    best_val, best_state = 0.0, None
    EPOCHS, BATCH = 60, 128
    print(f"    device={device}  train={len(train_idx)}  val={len(val_idx)}")
    for ep in range(1, EPOCHS + 1):
        head.train()
        shuf = train_idx[torch.randperm(len(train_idx), generator=rng)]
        tot_loss, tot_correct = 0.0, 0
        for i in range(0, len(shuf), BATCH):
            idx = shuf[i:i+BATCH]
            logits = head(feats[idx])
            loss = loss_fn(logits, labels[idx])
            opt.zero_grad(); loss.backward(); opt.step()
            tot_loss += loss.item() * len(idx)
            tot_correct += (logits.argmax(dim=-1) == labels[idx]).sum().item()
        train_acc = tot_correct / len(shuf)
        head.eval()
        with torch.no_grad():
            va = (head(feats[val_idx]).argmax(dim=-1)
                  == labels[val_idx]).float().mean().item()
        if ep % 10 == 0 or ep == 1:
            print(f"    epoch {ep:3d}: loss={tot_loss/len(shuf):.3f} "
                  f"train_acc={train_acc:.3f}  val_acc={va:.3f}")
        if va > best_val:
            best_val = va
            best_state = {k: v.detach().clone() for k, v in head.state_dict().items()}
    print(f"    best val_acc = {best_val:.3f}  ({best_val/0.25:.1f}x chance)")
    if best_state is not None:
        head.load_state_dict(best_state)
    head = head.cpu()

    torch.save({
        "state_dict":   head.state_dict(),
        "in_dim":       feats.size(1),
        "num_classes":  4,
        "labels":       LP_LEVELS,
        "encoder":      "sentence-transformers/all-MiniLM-L6-v2",
        "num_examples": len(examples),
        "val_acc":      best_val,
    }, LP_ST_PATH)
    print(f"Saved: {LP_ST_PATH}")


if __name__ == "__main__":
    main()
