"""
Train a small MLP emotion classifier on ProgSnap2 action-feature windows.
Weak labels derived from event patterns:
  - frustrated    = high run_rate AND high error_rate
  - confused      = moderate error_rate, low edit_rate
  - engaged       = high edit_rate AND search activity
  - understanding = submit_flag OR (low error_rate AND high edit_rate)
  - neutral       = everything else
Saves checkpoints/emotion_classifier.pt (7-dim in, 5-class out).
Pairs with BehavioralHMM's _extract_features so orchestrator can call it on
the same windowed feature vectors the HMM sees.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import time
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset

from src.models.behavioral import BehavioralHMM


PROGSNAP2_CSV = Path("data/progsnap2/MainTable.csv")
CKPT = Path("checkpoints/emotion_classifier.pt")
CLASSES = ["neutral", "confused", "frustrated", "engaged", "understanding"]
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"


def weak_label(feat):
    # feat: [run_rate, error_rate, edit_rate, search_rate, pause, help_rate, submit_flag]
    run, err, edit, search, pause, helpr, submit = feat
    if submit >= 0.5 and err < 0.3:
        return 4  # understanding
    if run >= 0.5 and err >= 0.4:
        return 2  # frustrated
    if err >= 0.25 and edit < 0.3:
        return 1  # confused
    if edit >= 0.4 and (search >= 0.2 or helpr >= 0.1):
        return 3  # engaged
    if edit >= 0.4 and err < 0.2:
        return 4  # understanding (silent mastery)
    return 0  # neutral


def build_dataset():
    print(f"[Emotion] loading {PROGSNAP2_CSV}")
    df = pd.read_csv(PROGSNAP2_CSV).sort_values(["SubjectID", "ServerTimestamp"])
    hmm = BehavioralHMM({"behavioral": {"hmm_checkpoint": "checkpoints/behavioral_hmm.json"}})

    X, y = [], []
    for sid, grp in df.groupby("SubjectID"):
        events = grp["EventType"].astype(str).tolist()
        if len(events) < 5:
            continue
        feats = hmm._extract_features(events)
        for f in feats:
            X.append(f)
            y.append(weak_label(f))
    X = np.array(X, dtype=np.float32)
    y = np.array(y, dtype=np.int64)
    print(f"[Emotion] {len(X)} windows, label distribution:")
    for i, c in enumerate(CLASSES):
        pct = (y == i).mean() * 100
        print(f"  {i} {c:<14} {(y == i).sum():>6}  ({pct:.1f}%)")
    return X, y


class EmotionMLP(nn.Module):
    def __init__(self, in_dim=7, n_classes=5, hidden=64):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(in_dim, hidden), nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(hidden, hidden), nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(hidden, n_classes),
        )

    def forward(self, x):
        return self.net(x)


def main():
    X, y = build_dataset()
    # stratified shuffle
    rng = np.random.default_rng(0)
    idx = rng.permutation(len(X))
    split = int(0.85 * len(X))
    tr, te = idx[:split], idx[split:]

    tr_ds = TensorDataset(torch.from_numpy(X[tr]), torch.from_numpy(y[tr]))
    te_ds = TensorDataset(torch.from_numpy(X[te]), torch.from_numpy(y[te]))
    tr_dl = DataLoader(tr_ds, batch_size=256, shuffle=True)
    te_dl = DataLoader(te_ds, batch_size=512, shuffle=False)

    # class-balanced weights
    counts = np.bincount(y[tr], minlength=len(CLASSES)).astype(np.float32)
    weights = torch.tensor(counts.sum() / (counts + 1), dtype=torch.float32).to(DEVICE)
    weights = weights / weights.sum() * len(CLASSES)

    model = EmotionMLP().to(DEVICE)
    opt = optim.Adam(model.parameters(), lr=1e-3)
    loss_fn = nn.CrossEntropyLoss(weight=weights)

    print(f"[Emotion] training on {DEVICE} | {len(tr)} train, {len(te)} val")
    for epoch in range(15):
        t0 = time.time()
        model.train()
        losses = []
        correct = total = 0
        for xb, yb in tr_dl:
            xb, yb = xb.to(DEVICE), yb.to(DEVICE)
            opt.zero_grad()
            logits = model(xb)
            loss = loss_fn(logits, yb)
            loss.backward()
            opt.step()
            losses.append(loss.item())
            correct += (logits.argmax(1) == yb).sum().item()
            total += yb.size(0)
        tr_acc = correct / total
        model.eval()
        correct = total = 0
        with torch.no_grad():
            for xb, yb in te_dl:
                xb, yb = xb.to(DEVICE), yb.to(DEVICE)
                logits = model(xb)
                correct += (logits.argmax(1) == yb).sum().item()
                total += yb.size(0)
        val_acc = correct / total
        print(f"  ep {epoch+1:02d}  loss={np.mean(losses):.4f}  "
              f"tr_acc={tr_acc:.3f}  val_acc={val_acc:.3f}  "
              f"t={time.time()-t0:.1f}s")

    CKPT.parent.mkdir(parents=True, exist_ok=True)
    torch.save({
        "state_dict": model.state_dict(),
        "classes": CLASSES,
        "in_dim": 7,
        "hidden": 64,
    }, CKPT)
    print(f"[Emotion] saved {CKPT}")


if __name__ == "__main__":
    main()
