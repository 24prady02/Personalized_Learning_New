"""
fuse_44.py — the fused classifier on the 44 labelled scenarios: each source
decides what it is reliable for, all of it from the graph's has_level edge logic.

  * L0: the Claude judge (reading the graph's L0 ways) finds a wrong rule, or the
    code run finds an inconsistent trace / a misconception reproduced by its run.
  * Levels set by the code run or by the question-form rules (v7) are kept.
  * Levels set by the weak readers (NLI fact / way / refuted, the "because +
    neighbour" shortcut, a similarity-only fact match) are replaced by the judge.
  * Otherwise the v7 level is kept.

Scored against the workbook labels and against the labels with the graph's own
boundaries applied (GRAPH_KEY): a relation stated with its reason is L3; fixing
one given failing case is L3; a bare correct output is L1.

Usage: python scripts/fuse_44.py
"""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output"
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# workbook label -> label under the graph's boundary text (with the boundary quoted)
GRAPH_KEY = {
    "S104": ("L3", "relation_to_neighbour: a reason relating double and int ('because double is bigger')"),
    "S117": ("L3", "relation_to_neighbour: the reason t is needed ('otherwise a[i] is overwritten')"),
    "S126": ("L3", "L4 diagnose boundary: 'Locating and fixing the mistake for one given failing case is L3'"),
    "S115": ("L1", "L2 boundary: 'A bare correct output is not levelled'"),
    "S128": ("L1", "L2 boundary: 'A bare correct output is not levelled'"),
}
WEAK = ("NLI", "relation cue", "similarity (fact)")


def fuse(j, v, src):
    if "L0" in j["final"].values():
        return "L0", "judge or code run: wrong rule (L0 way)"
    if src.startswith(WEAK):
        return (j["best"] or v), f"judge replaces {src}"
    return v, f"kept ({src})"


def report(rows, key, name):
    exp = [r[key] for r in rows]
    for col in ("v7", "judge", "fused"):
        got = [r[col] for r in rows]
        exact = sum(g == e for g, e in zip(got, exp))
        within = sum(g is not None and abs(int(g[1]) - int(e[1])) <= 1 for g, e in zip(got, exp))
        per = Counter(exp)
        hit = Counter(e for g, e in zip(got, exp) if g == e)
        print(f"{name:22s} {col:6s} exact {exact}/44  within-1 {within}  "
              + "  ".join(f"{k} {hit[k]}/{per[k]}" for k in sorted(per)))


def main() -> None:
    judge = {r["id"]: r for r in json.loads((OUT / "llm_judge_claude" / "results.json").read_text(encoding="utf-8"))}
    v7 = {s["id"]: s for s in json.loads((OUT / "scenario_run_v7" / "results.json").read_text(encoding="utf-8"))["scenarios"]
          if s.get("expected_level")}
    src = {r["id"]: r["level_source"] for r in json.loads((OUT / "scenario_run_v7" / "steps_44_check.json").read_text())}
    rows = []
    for sid, j in judge.items():
        lv, why = fuse(j, v7[sid]["max_level"], src[sid])
        rows.append({"id": sid, "label": j["expected"], "graph_label": GRAPH_KEY.get(sid, (j["expected"],))[0],
                     "v7": v7[sid]["max_level"], "judge": j["best"], "fused": lv, "why": why,
                     "text": j["text"]})
    report(rows, "label", "workbook labels")
    report(rows, "graph_label", "graph-boundary labels")
    print("\nstill wrong under the graph-boundary labels:")
    for r in rows:
        if r["fused"] != r["graph_label"]:
            print(f"  {r['id']} expected {r['graph_label']} got {r['fused']} | v7 {r['v7']} judge {r['judge']} | {r['why']}")
    (OUT / "llm_judge_claude" / "fused_44.json").write_text(
        json.dumps({"graph_key": GRAPH_KEY, "rows": rows}, indent=1, ensure_ascii=False), encoding="utf-8")


if __name__ == "__main__":
    main()
