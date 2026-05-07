"""
LP head training ONLY — reads the student-voice LP corpus built by
cpal_gen_corpus.py (via its incremental cache), trains a 4-class head
on frozen HVSAE latent using GPU, saves to checkpoints/cpal_lp_head.pt.

Does NOT touch checkpoints/cpal_wm_subhead.pt — the WM head trained
previously remains in place and runs in parallel via LPDiagnostician.
"""
import os, sys, json, time
from pathlib import Path
import torch
import torch.nn as nn

ROOT = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, str(ROOT))

from src.models.hvsae import HVSAE

CHECKPOINT_DIR = ROOT / "checkpoints"
CACHE_PATH     = ROOT / "data" / "mental_models" / "gen_cache.json"
LP_HEAD_PATH   = CHECKPOINT_DIR / "cpal_lp_head.pt"

LP_LEVELS     = ["L1", "L2", "L3", "L4"]
LP_LVL_TO_ID  = {lvl: i for i, lvl in enumerate(LP_LEVELS)}


class MLPHead(nn.Module):
    def __init__(self, in_dim, hidden, num_classes, dropout=0.3):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(in_dim, hidden), nn.ReLU(), nn.Dropout(dropout),
            nn.Linear(hidden, hidden // 2), nn.ReLU(), nn.Dropout(dropout),
            nn.Linear(hidden // 2, num_classes),
        )
    def forward(self, x): return self.net(x)


def load_lp_corpus_from_cache():
    if not CACHE_PATH.exists():
        raise RuntimeError(f"cache not found at {CACHE_PATH}")
    with open(CACHE_PATH, encoding="utf-8") as f:
        cache = json.load(f)
    examples = []
    n_groups = 0
    for key, lines in cache.items():
        # keys look like "lp|<concept>|<level>" or "wm|<concept>|<wm_id>"
        parts = key.split("|")
        if len(parts) != 3 or parts[0] != "lp":
            continue
        _, concept, level = parts
        if level not in LP_LVL_TO_ID:
            continue
        n_groups += 1
        for t in lines:
            if isinstance(t, str) and t.strip():
                examples.append({
                    "text": t.strip(),
                    "concept": concept,
                    "lp_level": level,
                })
    return examples, n_groups


def main():
    print("[1/4] Loading HVSAE (frozen)")
    ck = torch.load(CHECKPOINT_DIR / "best.pt",
                    map_location="cpu", weights_only=False)
    hv = HVSAE(ck["config"])
    hv.load_state_dict(ck["hvsae_state"])
    hv.eval()
    for p in hv.parameters():
        p.requires_grad = False

    print("[2/4] Loading LP corpus from cache")
    examples, n_groups = load_lp_corpus_from_cache()
    print(f"    {len(examples)} LP examples across {n_groups} "
          f"(concept × level) groups")
    # Per-class counts
    per_class = {}
    for e in examples:
        per_class[e["lp_level"]] = per_class.get(e["lp_level"], 0) + 1
    print(f"    per LP class: {per_class}")

    print("[3/4] Encoding via HVSAE TextEncoder + full forward")
    try:
        from transformers import AutoTokenizer
        tk = AutoTokenizer.from_pretrained("bert-base-uncased")
    except Exception:
        tk = None

    def encode(t):
        t = (t or "").strip() or "empty"
        if tk is not None:
            ids = tk(t, return_tensors="pt", padding=True, truncation=True,
                     max_length=64)["input_ids"].long() % 6000
        else:
            words = t.lower().split()[:64]
            ids = torch.tensor(
                [[abs(hash(w)) % 6000 for w in words]], dtype=torch.long)
        with torch.no_grad():
            out = hv.forward({
                "code_tokens": torch.zeros(1, 10, dtype=torch.long),
                "text_tokens": ids,
                "action_sequence": torch.ones(1, 8, dtype=torch.long),
            }, compute_graph=False)
        return out["latent"].squeeze(0)

    t0 = time.time()
    feats = torch.stack([encode(e["text"]) for e in examples])
    labels = torch.tensor([LP_LVL_TO_ID[e["lp_level"]] for e in examples],
                          dtype=torch.long)
    print(f"    encoded {len(examples)} in {time.time()-t0:.1f}s, "
          f"feats={tuple(feats.shape)}")

    print("[4/4] Training LP head on GPU")
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    feats  = feats.to(device)
    labels = labels.to(device)
    rng = torch.Generator().manual_seed(42)
    n = feats.size(0)
    perm = torch.randperm(n, generator=rng)
    n_val = max(1, int(n * 0.15))
    val_idx, train_idx = perm[:n_val], perm[n_val:]

    head = MLPHead(feats.size(1), 128, 4).to(device)
    opt = torch.optim.Adam(head.parameters(), lr=1e-3, weight_decay=1e-4)
    loss_fn = nn.CrossEntropyLoss()
    best_val = 0.0
    best_state = None
    EPOCHS, BATCH = 80, 128
    print(f"    device={device}  train={len(train_idx)}  val={len(val_idx)}")
    for ep in range(1, EPOCHS + 1):
        head.train()
        shuffled = train_idx[torch.randperm(len(train_idx), generator=rng)]
        total_loss, total_correct = 0.0, 0
        for i in range(0, len(shuffled), BATCH):
            idx = shuffled[i:i + BATCH]
            x, y = feats[idx], labels[idx]
            logits = head(x)
            loss = loss_fn(logits, y)
            opt.zero_grad(); loss.backward(); opt.step()
            total_loss += loss.item() * len(idx)
            total_correct += (logits.argmax(dim=-1) == y).sum().item()
        train_acc = total_correct / len(shuffled)
        head.eval()
        with torch.no_grad():
            vl = head(feats[val_idx])
            val_acc = (vl.argmax(dim=-1) == labels[val_idx]).float().mean().item()
        if ep % 10 == 0 or ep == 1:
            print(f"    epoch {ep:3d}: loss={total_loss/len(shuffled):.3f}  "
                  f"train_acc={train_acc:.3f}  val_acc={val_acc:.3f}")
        if val_acc > best_val:
            best_val = val_acc
            best_state = {k: v.detach().clone() for k, v in head.state_dict().items()}
    print(f"    best val_acc = {best_val:.3f}")
    if best_state is not None:
        head.load_state_dict(best_state)
    head = head.cpu()

    torch.save({
        "state_dict":   head.state_dict(),
        "in_dim":       feats.size(1),
        "num_classes":  4,
        "labels":       LP_LEVELS,
        "num_examples": len(examples),
        "val_acc":      best_val,
    }, LP_HEAD_PATH)
    print(f"\nSaved LP head to {LP_HEAD_PATH}")
    print(f"  per-class: {per_class}")
    print(f"  best val_acc: {best_val:.3f}  ({best_val/0.25:.1f}x chance)")


if __name__ == "__main__":
    main()
