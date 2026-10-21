"""
score_44.py — score a scenario run on the 44 labelled answers, against the
workbook labels and against the labels with the graph's own boundaries applied
(fuse_44.GRAPH_KEY).

Usage: python scripts/score_44.py scenario_run_v9_judge [scenario_run_v7 ...]
"""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from fuse_44 import GRAPH_KEY  # noqa: E402


def main() -> None:
    for run in sys.argv[1:]:
        rows = [s for s in json.loads((ROOT / "output" / run / "results.json").read_text(encoding="utf-8"))["scenarios"]
                if s.get("expected_level")]
        for name, key in (("workbook labels", lambda s: s["expected_level"]),
                          ("graph-boundary labels", lambda s: GRAPH_KEY.get(s["id"], (s["expected_level"],))[0])):
            exp = [key(s) for s in rows]
            got = [s["max_level"] for s in rows]
            exact = sum(g == e for g, e in zip(got, exp))
            within = sum(g is not None and abs(int(g[1]) - int(e[1])) <= 1 for g, e in zip(got, exp))
            per, hit = Counter(exp), Counter(e for g, e in zip(got, exp) if g == e)
            print(f"{run:24s} {name:22s} exact {exact}/{len(rows)}  within-1 {within}  "
                  + "  ".join(f"{k} {hit[k]}/{per[k]}" for k in sorted(per)))
        for s in rows:
            e = GRAPH_KEY.get(s["id"], (s["expected_level"],))[0]
            if s["max_level"] != e:
                srcs = {c["concept"]: f'{c["prompt_level"]}/{c.get("level_source") or "-"}'
                        for c in s["concepts"] if c["assessed"]}
                print(f"   miss {s['id']} expected {e} got {s['max_level']} | {srcs}")


if __name__ == "__main__":
    main()
