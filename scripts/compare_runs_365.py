"""
compare_runs_365.py — compare two full scenario runs (all 365): level
distribution, what set each level, how many answers changed and how.

Usage: python scripts/compare_runs_365.py scenario_run_v7 scenario_run_v10_all
"""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ORDER = ["L0", "L1", "L2", "L3", "L4", None]


def load(run):
    return {s["id"]: s for s in json.loads((ROOT / "output" / run / "results.json").read_text(encoding="utf-8"))["scenarios"]}


def main() -> None:
    a_name, b_name = sys.argv[1], sys.argv[2]
    a, b = load(a_name), load(b_name)
    for name, run in ((a_name, a), (b_name, b)):
        for key in ("top_level", "max_level"):
            c = Counter(s[key] for s in run.values())
            print(f"{name:22s} {key:9s} " + "  ".join(f"{k or 'not assessed'} {c[k]}" for k in ORDER))
    src = Counter(c.get("level_source") or "-" for s in b.values() for c in s["concepts"] if c["assessed"])
    print("\nwhat set each assessed concept's level in", b_name, dict(src.most_common()))
    print("answers with a wrong rule (L0 by the run or the judge):", sum(
        any(c.get("wrong_rule") for c in s["concepts"] if c["assessed"]) for s in b.values()))
    print("answers the judge graded:", sum(1 for s in b.values() if any(c.get("judge") for c in s["concepts"])))
    moves = Counter((a[k]["max_level"], b[k]["max_level"]) for k in b if a[k]["max_level"] != b[k]["max_level"])
    print(f"\nmax level changed on {sum(moves.values())} of {len(b)} answers:")
    for (x, y), n in moves.most_common():
        print(f"  {x or 'none'} -> {y or 'none'}: {n}")
    unl = [k for k in b if not b[k].get("expected_level")]
    up = sum(1 for k in unl if (a[k]["max_level"] or "L-") < (b[k]["max_level"] or "L-"))
    down = sum(1 for k in unl if (a[k]["max_level"] or "L-") > (b[k]["max_level"] or "L-"))
    print(f"unlabelled answers: {len(unl)}, level up {up}, level down {down}")


if __name__ == "__main__":
    main()
