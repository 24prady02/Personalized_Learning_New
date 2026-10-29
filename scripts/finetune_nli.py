"""Fine-tune the cached NLI cross-encoder on the graph-built pairs.

Trains on the ``train`` split of data/nli_pairs.json (scripts/build_nli_pairs.py),
then fixes the decision thresholds on the ``dev`` split (concepts never seen in
training): the smallest probability at which a label is right at least
TARGET_PRECISION of the time. No student answer and no gold key is used.

    python scripts/finetune_nli.py   -> models/nli-chapter1/ (+ thresholds.json)
"""

from __future__ import annotations

import json
import os
import random
import sys
from pathlib import Path

os.environ.setdefault("HF_HUB_OFFLINE", "1")
os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")
ROOT = Path(__file__).resolve().parents[1]
BASE = "cross-encoder/nli-deberta-v3-base"
OUT = ROOT / "models" / "nli-chapter1"
EPOCHS = 3
BATCH = 16
LR = 2e-5
SEED = 13
TARGET_PRECISION = 0.9
LABELS = {0: "contradiction", 1: "entailment", 2: "neutral"}


def evaluate(model, rows) -> tuple[float, list]:
    import numpy as np

    probs = model.predict([(r["premise"], r["hypothesis"]) for r in rows], apply_softmax=True,
                          batch_size=32, show_progress_bar=False)
    pred = np.argmax(probs, axis=1)
    acc = float(np.mean(pred == np.array([r["label"] for r in rows])))
    return acc, probs


def per_class(rows, probs) -> dict:
    import numpy as np

    out = {}
    pred = np.argmax(probs, axis=1)
    gold = np.array([r["label"] for r in rows])
    for k, name in LABELS.items():
        tp = int(np.sum((pred == k) & (gold == k)))
        out[name] = {"precision": tp / max(1, int(np.sum(pred == k))), "recall": tp / max(1, int(np.sum(gold == k)))}
    return out


def threshold(rows, probs, label: int) -> float:
    """Smallest p such that predictions with P(label) >= p are right >= TARGET_PRECISION."""
    cand = sorted({round(float(p[label]), 3) for p in probs})
    for t in cand:
        sel = [r for r, p in zip(rows, probs) if p[label] >= t]
        if sel and sum(r["label"] == label for r in sel) / len(sel) >= TARGET_PRECISION:
            return t
    return 1.01


def main() -> int:
    import torch
    from sentence_transformers import CrossEncoder, InputExample
    from torch.utils.data import DataLoader

    random.seed(SEED)
    torch.manual_seed(SEED)
    pairs = json.load(open(ROOT / "data" / "nli_pairs.json", encoding="utf-8"))
    train = [r for r in pairs if r["split"] == "train"]
    dev = [r for r in pairs if r["split"] == "dev"]
    # student wording labelled by running the code (build_student_pairs.py), training questions only
    student_file = ROOT / "data" / "student_pairs.json"
    student = json.load(open(student_file, encoding="utf-8")) if student_file.exists() else []
    train += [r for r in student if r["split"] == "train"] * 3   # few, so each is seen three times per epoch
    student_eval = [r for r in student if r["split"] == "eval"]
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = CrossEncoder(BASE, num_labels=3, max_length=256, device=device)
    acc0, probs0 = evaluate(model, dev)
    print(f"dev accuracy before: {acc0:.3f}", json.dumps(per_class(dev, probs0)))
    examples = [InputExample(texts=[r["premise"], r["hypothesis"]], label=r["label"]) for r in train]
    loader = DataLoader(examples, shuffle=True, batch_size=BATCH)
    model.fit(train_dataloader=loader, epochs=EPOCHS, warmup_steps=int(0.1 * len(loader) * EPOCHS),
              optimizer_params={"lr": LR}, show_progress_bar=False, use_amp=device == "cuda")
    acc1, probs1 = evaluate(model, dev)
    print(f"dev accuracy after:  {acc1:.3f}", json.dumps(per_class(dev, probs1)))
    if student_eval:
        acc_s, _ = evaluate(model, student_eval)
        print(f"student pairs of evaluation questions: accuracy {acc_s:.3f} on {len(student_eval)}")
    th = {"entailment": threshold(dev, probs1, 1), "contradiction": threshold(dev, probs1, 0),
          "target_precision": TARGET_PRECISION, "dev_accuracy": acc1, "dev_accuracy_before": acc0,
          "train_pairs": len(train), "dev_pairs": len(dev), "base_model": BASE, "epochs": EPOCHS}
    OUT.mkdir(parents=True, exist_ok=True)
    model.save(str(OUT))
    # keep the base model's tokenizer files (the re-saved copy loads with a regex warning)
    from transformers import AutoTokenizer
    AutoTokenizer.from_pretrained(BASE).save_pretrained(str(OUT))
    json.dump(th, open(OUT / "thresholds.json", "w", encoding="utf-8"), indent=1)
    print("thresholds", th)
    return 0


if __name__ == "__main__":
    sys.exit(main())
