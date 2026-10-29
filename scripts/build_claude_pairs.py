"""Turn Claude's offline edge labels into NLI training pairs.

Inputs: data/label_items.jsonl (answers and their candidate edges) and
data/edge_labels/*.jsonl (Claude's labels: E = expressed, C = contradicted;
items not listed = not addressed). Each pair: premise = the student's answer,
hypothesis = the edge-logic text; label 1 entailment (E), 0 contradiction (C),
2 neutral (not addressed, at most twice the E + C pairs of each split).
Split by question (the same hash as before): train / eval. The gold
scenarios are never in the inputs.

    python scripts/build_claude_pairs.py   -> data/claude_pairs.json
"""

from __future__ import annotations

import hashlib
import json
import random
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def split_of(question: str) -> str:
    h = int(hashlib.sha1((question or "").strip().lower().encode()).hexdigest(), 16)
    return "eval" if (h % 1000) / 1000 < 0.3 else "train"


def main() -> int:
    items = {}
    for line in open(ROOT / "data" / "label_items.jsonl", encoding="utf-8"):
        if line.strip():
            r = json.loads(line)
            items[r["id"]] = r
    labels = {}
    for f in sorted((ROOT / "data" / "edge_labels").glob("*.jsonl")):
        for line in open(f, encoding="utf-8"):
            if line.strip():
                rec = json.loads(line)
                labels[rec["id"]] = rec["labels"]          # the last save of an answer wins
    pairs = []
    for aid, lab in labels.items():
        r = items.get(aid)
        if r is None:
            continue
        premise = r["answer"][:800]
        sp = split_of(r["question"])
        for it in r["items"]:
            got = lab.get(it["id"])
            code = got[0] if isinstance(got, list) and got else None
            label = {"E": 1, "C": 0}.get(code, 2)
            if it["kind"] == "way" and label == 0:
                label = 2
            tag = {1: "E", 0: "C", 2: "N"}[label]
            pairs.append({"premise": premise, "hypothesis": it["text"], "label": label,
                          "kind": f"{it['kind']}_{tag}", "answer": aid, "split": sp})
    random.seed(5)
    out = []
    for sp in ("train", "eval"):
        pos = [p for p in pairs if p["split"] == sp and p["label"] != 2]
        neg = [p for p in pairs if p["split"] == sp and p["label"] == 2]
        random.shuffle(neg)
        out += pos + neg[: 2 * len(pos)]
    json.dump(out, open(ROOT / "data" / "claude_pairs.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    print("answers labelled", len(labels), "| pairs", len(pairs), "| kept", len(out))
    print(sorted(Counter((p["split"], p["label"]) for p in out).items()))
    print(sorted(Counter(p["kind"] for p in out if p["label"] != 2).items()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
