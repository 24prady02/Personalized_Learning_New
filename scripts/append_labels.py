"""Append labelled answers (JSON lines on stdin) to data/edge_labels/<batch>.jsonl.

    python scripts/append_labels.py batch_3 < labels.jsonl
Each line: {"id": "S123", "labels": {"R0": ["E", "quote"], "W1": ["C", "quote"]}}
(items not listed are "not addressed"). Lines that are not valid JSON are rejected.
"""
import json
import sys
from pathlib import Path

batch = sys.argv[1]
out = Path(__file__).resolve().parents[1] / "data" / "edge_labels" / f"{batch}.jsonl"
ok = bad = 0
with open(out, "a", encoding="utf-8") as fh:
    for line in sys.stdin.read().splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rec = json.loads(line)
            assert isinstance(rec.get("id"), str) and isinstance(rec.get("labels"), dict)
        except Exception:
            bad += 1
            continue
        fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
        ok += 1
print(f"saved {ok} answers to {out.name}" + (f", rejected {bad} bad lines" if bad else ""))
