"""
score_100.py — score runs on the 100 Fable-labelled scenarios (output/selected_100_fable).

Usage: python scripts/score_100.py scenario_run_v10_all scenario_run_100_qwen3
"""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
LV = ["L0", "L1", "L2", "L3", "L4", "none"]


def main() -> None:
    ref = {p["id"]: p["level"] for p in json.loads(
        (ROOT / "output" / "selected_100_fable" / "selected_60.json").read_text(encoding="utf-8"))}
    for run in sys.argv[1:]:
        got = {s["id"]: (s["max_level"] or "none") for s in json.loads(
            (ROOT / "output" / run / "results.json").read_text(encoding="utf-8"))["scenarios"] if s["id"] in ref}
        ids = [i for i in ref if i in got]
        k = sum(got[i] == ref[i] for i in ids)
        w = sum(got[i] != "none" and ref[i] != "none" and abs(int(got[i][1]) - int(ref[i][1])) <= 1 for i in ids)
        per, hit = Counter(ref[i] for i in ids), Counter(ref[i] for i in ids if got[i] == ref[i])
        print(f"{run:26s} exact {k}/{len(ids)}  within-1 {w}  " + "  ".join(f"{x} {hit[x]}/{per[x]}" for x in LV))


if __name__ == "__main__":
    main()
