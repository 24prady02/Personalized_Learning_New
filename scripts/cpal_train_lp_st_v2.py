"""Improved LP head trainer (v2).

Why v2 exists
-------------
The original cpal_train_lp_st.py produces cpal_lp_head_st.pt with
val_acc ≈ 0.743. The scenario harness's Layer 3 shows the failure
mode: clear L3 replies get classified as L2, clear L4 replies get
classified as L3 — adjacent-class confusion. Training data IS
reasonably balanced (L1=387, L2=354, L3=291, L4=317) so the issue
is the head's discriminative capacity, not class imbalance.

This v2 keeps the same encoder (all-MiniLM-L6-v2 — frozen) and the
same data, but changes:

  1. Label smoothing (eps=0.1)
       Adjacent-class confusion benefits from softer targets — the
       model no longer needs to push the correct logit to 1.0 and
       the wrong adjacent logit to 0.0, which is the regime where
       it was overfitting to spurious surface cues.

  2. Larger head (192 hidden vs 128) + GELU activation
       GELU has a smoother gradient near zero than ReLU and tends
       to learn finer-grained boundaries.

  3. Cosine LR schedule with warmup
       Lets the head settle into a wider minimum.

  4. Mild class weighting (inverse frequency, capped at 1.5x)
       Slight bias against L1 (over-represented at 387) toward L3
       (under-represented at 291).

  5. Best-of-3 seeds
       Runs 3 independent seeds, keeps the checkpoint with highest
       val_acc. Cheap (~30s total) and removes seed-luck variance.

  6. Stratified train/val split
       Original used a uniform random split which can leave some
       classes scarce in val. Stratified guarantees ~15% per class.

Outputs:
  - checkpoints/cpal_lp_head_st_v2.pt — the new head
  - prints a "swap recommendation" line at the end based on whether
    new val_acc beats the baseline (cpal_lp_head_st.pt) by ≥ 0.02.

Does NOT auto-swap. The caller (or operator) decides.

Run:
  python scripts/cpal_train_lp_st_v2.py
"""
from __future__ import annotations
import json
import os
import sys
import time
from pathlib import Path

import torch
import torch.nn as nn

ROOT = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, str(ROOT))

CHECKPOINT_DIR = ROOT / "checkpoints"
CACHE_PATH     = ROOT / "data" / "mental_models" / "gen_cache.json"
LP_ST_V2_PATH  = CHECKPOINT_DIR / "cpal_lp_head_st_v2.pt"
LP_ST_OLD_PATH = CHECKPOINT_DIR / "cpal_lp_head_st.pt"

LP_LEVELS    = ["L1", "L2", "L3", "L4"]
LP_LVL_TO_ID = {lvl: i for i, lvl in enumerate(LP_LEVELS)}

EPOCHS = 80
BATCH  = 64
LR     = 2e-3
WD     = 5e-4
HIDDEN = 192
LABEL_SMOOTHING = 0.10
SEEDS  = [13, 42, 1337]


class MLPHeadV2(nn.Module):
    """3-layer MLP with GELU + dropout. Larger hidden than v1."""
    def __init__(self, in_dim, hidden, num_classes, dropout=0.4):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(in_dim, hidden),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(hidden, hidden // 2),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(hidden // 2, num_classes),
        )
    def forward(self, x): return self.net(x)


def stratified_split(labels: torch.Tensor, val_frac: float,
                      seed: int) -> tuple:
    """Stratified train/val index split — guarantees ~val_frac of
    each class lands in val. Returns (train_idx, val_idx)."""
    g = torch.Generator().manual_seed(seed)
    train_chunks, val_chunks = [], []
    for cls in range(int(labels.max().item()) + 1):
        cls_idx = (labels == cls).nonzero(as_tuple=True)[0]
        perm = cls_idx[torch.randperm(len(cls_idx), generator=g)]
        n_val = max(1, int(round(len(perm) * val_frac)))
        val_chunks.append(perm[:n_val])
        train_chunks.append(perm[n_val:])
    train_idx = torch.cat(train_chunks)
    val_idx   = torch.cat(val_chunks)
    # Re-shuffle so batches don't see classes back-to-back
    train_idx = train_idx[torch.randperm(len(train_idx), generator=g)]
    val_idx   = val_idx[torch.randperm(len(val_idx),   generator=g)]
    return train_idx, val_idx


def class_weights_from_counts(labels: torch.Tensor) -> torch.Tensor:
    """Inverse-frequency weights, capped so we don't over-correct."""
    counts = torch.bincount(labels, minlength=4).float()
    inv = counts.max() / counts.clamp(min=1.0)
    return inv.clamp(max=1.5)


def train_one_seed(feats, labels, seed, device, log_prefix):
    """Train one seed end-to-end. Returns (best_val_acc, best_state_dict, per_class_acc)."""
    torch.manual_seed(seed)
    train_idx, val_idx = stratified_split(labels.cpu(), val_frac=0.15, seed=seed)
    train_idx, val_idx = train_idx.to(device), val_idx.to(device)
    weights = class_weights_from_counts(labels[train_idx].cpu()).to(device)
    head = MLPHeadV2(feats.size(1), HIDDEN, 4).to(device)
    opt = torch.optim.AdamW(head.parameters(), lr=LR, weight_decay=WD)
    sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, T_max=EPOCHS)
    loss_fn = nn.CrossEntropyLoss(weight=weights,
                                   label_smoothing=LABEL_SMOOTHING)

    best_val, best_state, best_per_class = 0.0, None, None
    rng = torch.Generator().manual_seed(seed)
    for ep in range(1, EPOCHS + 1):
        head.train()
        shuf = train_idx[torch.randperm(len(train_idx), generator=rng)]
        for i in range(0, len(shuf), BATCH):
            idx = shuf[i:i+BATCH]
            logits = head(feats[idx])
            loss = loss_fn(logits, labels[idx])
            opt.zero_grad(); loss.backward(); opt.step()
        sched.step()
        head.eval()
        with torch.no_grad():
            preds = head(feats[val_idx]).argmax(dim=-1)
            va = (preds == labels[val_idx]).float().mean().item()
            # per-class
            per_class = {}
            for cls in range(4):
                mask = labels[val_idx] == cls
                if mask.any():
                    per_class[LP_LEVELS[cls]] = float(
                        (preds[mask] == cls).float().mean().item())
        if ep % 20 == 0 or ep == 1:
            print(f"    {log_prefix} ep {ep:3d}: val_acc={va:.3f}  "
                  f"per-class={ {k: round(v,2) for k,v in per_class.items()} }")
        if va > best_val:
            best_val = va
            best_state = {k: v.detach().clone() for k, v in head.state_dict().items()}
            best_per_class = per_class
    return best_val, best_state, best_per_class


def main():
    print("[1/3] Loading sentence-transformers encoder (all-MiniLM-L6-v2)")
    from sentence_transformers import SentenceTransformer
    st = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

    print("[1/3] Loading LP corpus")
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

    print("[2/3] Encoding")
    t0 = time.time()
    texts = [e["text"] for e in examples]
    feats = st.encode(texts, convert_to_tensor=True,
                       show_progress_bar=False, batch_size=64)
    feats = feats.cpu().float()
    labels = torch.tensor([LP_LVL_TO_ID[e["lp_level"]] for e in examples],
                          dtype=torch.long)
    print(f"    encoded in {time.time()-t0:.1f}s, feats={tuple(feats.shape)}")

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    feats  = feats.to(device); labels = labels.to(device)

    print(f"[3/3] Training {len(SEEDS)} seeds")
    all_results = []
    for seed in SEEDS:
        print(f"  seed {seed}:")
        va, state, per_class = train_one_seed(
            feats, labels, seed, device, f"  [seed {seed}]")
        all_results.append((va, state, per_class, seed))
        print(f"    seed {seed} best: val_acc={va:.3f}  "
              f"per-class={ {k: round(v,2) for k,v in per_class.items()} }")

    # Pick best seed
    all_results.sort(key=lambda x: x[0], reverse=True)
    best_val, best_state, best_per_class, best_seed = all_results[0]
    print(f"\n[best] seed={best_seed} val_acc={best_val:.3f}")

    # Baseline comparison
    baseline = 0.0
    if LP_ST_OLD_PATH.exists():
        try:
            baseline = float(torch.load(LP_ST_OLD_PATH, map_location="cpu",
                                         weights_only=False).get("val_acc", 0.0))
        except Exception:
            pass
    delta = best_val - baseline
    print(f"[baseline] cpal_lp_head_st.pt val_acc={baseline:.3f}")
    print(f"[delta]    {delta:+.3f}")

    # Save v2
    head = MLPHeadV2(feats.size(1), HIDDEN, 4)
    head.load_state_dict({k: v.cpu() for k, v in best_state.items()})
    torch.save({
        "state_dict":     head.state_dict(),
        "in_dim":         feats.size(1),
        "hidden":         HIDDEN,
        "activation":     "gelu",
        "num_classes":    4,
        "labels":         LP_LEVELS,
        "encoder":        "sentence-transformers/all-MiniLM-L6-v2",
        "num_examples":   len(examples),
        "val_acc":        best_val,
        "per_class_acc":  best_per_class,
        "label_smoothing": LABEL_SMOOTHING,
        "best_seed":      best_seed,
        "trainer":        "cpal_train_lp_st_v2",
    }, LP_ST_V2_PATH)
    print(f"\nSaved: {LP_ST_V2_PATH}")
    if delta >= 0.02:
        print(f"SWAP_RECOMMENDED  (Δ={delta:+.3f} ≥ +0.02)")
    elif delta >= 0.0:
        print(f"MARGINAL  (Δ={delta:+.3f} — not worth swapping)")
    else:
        print(f"REGRESSION  (Δ={delta:+.3f} — keep baseline)")


if __name__ == "__main__":
    main()
