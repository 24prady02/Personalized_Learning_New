"""Fine-tune the NLI cross-encoder on graph pairs + weakly labelled answer pairs,
with progress, checkpoints and a time limit.

Start: cross-encoder/nli-deberta-v3-base (MNLI). Train: data/nli_pairs.json
(graph, train split) + data/answer_pairs.json (train questions, repeated 3x).
Progress goes to output/train_log.txt every 10 steps; the model is saved to
models/nli-answers every 100 steps, at each epoch end, and when the time limit
(--until HH:MM) is reached. At the end it is evaluated on the answer pairs of
the evaluation questions (never trained on), next to the off-the-shelf model.
The 19 gold scenarios are not used.

    python scripts/train_answer_nli.py --until 13:28
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import random
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
BASE = "cross-encoder/nli-deberta-v3-base"
OUT = ROOT / "models" / "nli-answers"
LOG = ROOT / "output" / "train_log.txt"
LABELS = {0: "contradiction", 1: "entailment", 2: "neutral"}


def log(msg: str) -> None:
    line = f"{dt.datetime.now():%H:%M:%S} {msg}"
    print(line, flush=True)
    with open(LOG, "a", encoding="utf-8") as fh:
        fh.write(line + "\n")


def predict(model, tok, rows, device) -> np.ndarray:
    import torch

    model.eval()
    out = []
    with torch.no_grad():
        for i in range(0, len(rows), 32):
            b = rows[i:i + 32]
            enc = tok([r["premise"] for r in b], [r["hypothesis"] for r in b], truncation=True,
                      max_length=128, padding=True, return_tensors="pt").to(device)
            out.append(model(**enc).logits.cpu().numpy())
    model.train()
    return np.concatenate(out) if out else np.zeros((0, 3))


def evaluate(model, tok, rows, device) -> dict:
    if not rows:
        return {}
    pred = np.argmax(predict(model, tok, rows, device), axis=1)
    gold = np.array([r["label"] for r in rows])
    pe, ge = pred == 1, gold == 1
    tp = int(np.sum(pe & ge))
    res = {"accuracy": round(float(np.mean(pred == gold)), 3),
           "entail_precision": round(tp / max(1, int(pe.sum())), 3),
           "entail_recall": round(tp / max(1, int(ge.sum())), 3)}
    for kind in sorted({r["kind"] for r in rows}):
        idx = [i for i, r in enumerate(rows) if r["kind"] == kind]
        res[kind] = round(float(np.mean(pred[idx] == gold[idx])), 3)
    return res


def save(model, tok, note: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    model.config.id2label = LABELS
    model.config.label2id = {v: k for k, v in LABELS.items()}
    model.save_pretrained(str(OUT))
    tok.save_pretrained(str(OUT))
    log(f"checkpoint saved ({note})")


def main() -> int:
    import torch
    from transformers import AutoModelForSequenceClassification, AutoTokenizer

    ap = argparse.ArgumentParser()
    ap.add_argument("--until", default="")
    ap.add_argument("--epochs", type=int, default=3)
    ap.add_argument("--pairs", default="data/answer_pairs.json")
    ap.add_argument("--out", default="models/nli-answers")
    ap.add_argument("--graph", type=int, default=-1, help="graph pairs to mix in (-1 = all)")
    ap.add_argument("--repeat", type=int, default=3, help="times each answer pair is repeated")
    args = ap.parse_args()
    deadline = None
    if args.until:
        h, m = map(int, args.until.split(":"))
        deadline = dt.datetime.now().replace(hour=h, minute=m, second=0, microsecond=0)

    LOG.parent.mkdir(parents=True, exist_ok=True)
    LOG.write_text("", encoding="utf-8")
    global OUT
    OUT = ROOT / args.out
    graph = [r for r in json.load(open(ROOT / "data" / "nli_pairs.json", encoding="utf-8")) if r["split"] == "train"]
    if args.graph >= 0:
        random.seed(3)
        graph = random.sample(graph, min(args.graph, len(graph)))
    ans = json.load(open(ROOT / args.pairs, encoding="utf-8"))
    train = graph + [r for r in ans if r["split"] == "train"] * args.repeat
    ev = [r for r in ans if r["split"] == "eval"]
    device = "cuda" if torch.cuda.is_available() else "cpu"
    tok = AutoTokenizer.from_pretrained(BASE)
    model = AutoModelForSequenceClassification.from_pretrained(BASE).to(device)
    model.train()
    opt = torch.optim.AdamW(model.parameters(), lr=2e-5, weight_decay=0.01)
    steps_per_epoch = (len(train) + 15) // 16
    total = steps_per_epoch * args.epochs
    log(f"train pairs {len(train)} | eval pairs {len(ev)} | {steps_per_epoch} steps per epoch, "
        f"{total} planned | stop at {args.until or 'end'}")
    random.seed(11)
    step, t0, losses, stopped = 0, time.time(), [], False
    for ep in range(1, args.epochs + 1):
        random.shuffle(train)
        for i in range(0, len(train), 16):
            b = train[i:i + 16]
            enc = tok([r["premise"] for r in b], [r["hypothesis"] for r in b], truncation=True,
                      max_length=128, padding=True, return_tensors="pt").to(device)
            labels = torch.tensor([r["label"] for r in b], device=device)
            lr = 2e-5 * min(1.0, (step + 1) / max(1, int(0.1 * total)))
            for g in opt.param_groups:
                g["lr"] = lr
            loss = torch.nn.functional.cross_entropy(model(**enc).logits, labels)
            loss.backward()
            opt.step()
            opt.zero_grad()
            step += 1
            losses.append(float(loss))
            if step % 10 == 0:
                rate = (time.time() - t0) / step
                log(f"epoch {ep} step {step}/{total} ({100 * step / total:.0f}%) "
                    f"loss {np.mean(losses[-10:]):.3f} | {rate:.1f}s/step")
            if step % 100 == 0:
                save(model, tok, f"step {step}")
            if deadline and dt.datetime.now() >= deadline:
                stopped = True
                break
        save(model, tok, f"end of epoch {ep}" if not stopped else f"time limit at step {step}")
        if stopped:
            break
    log(f"training stopped at step {step}/{total} ({100 * step / total:.0f}%)")
    trained = evaluate(model, tok, ev, device)
    log(f"fine-tuned on unseen-question pairs: {trained}")
    base = AutoModelForSequenceClassification.from_pretrained(BASE).to(device)
    log(f"off-the-shelf on the same pairs:   {evaluate(base, tok, ev, device)}")
    json.dump({"steps": step, "planned": total, "eval": trained}, open(OUT / "training.json", "w", encoding="utf-8"),
              indent=1)
    log("DONE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
