"""
way_match_44.py — step 1 of the plan, run as the classifier on the 44 (no LLM):

  * for each linked concept, the student's clauses (and the whole answer) are
    matched by similarity (MiniLM) with every way of its has_level edges, L0-L4,
    and the ways are ranked, as concepts are ranked;
  * NLI (deberta-v3-small) is only a veto: a way whose rule the answer strongly
    contradicts (>= 0.6) is dropped;
  * the code run is the truth check: an inconsistent trace or a misconception its
    run reproduces is L0; values it confirmed make the answer at least L2.

Concept level = the level of its top-ranked way (A), with the code run applied (B).
Answer level  = L0 if any concept is L0, else the highest concept level (as before).
Scored on the 44 with the graph-boundary levels. No LLM calls.

Usage: python scripts/way_match_44.py
"""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from fuse_44 import GRAPH_KEY  # noqa: E402
from shortlist_check_44 import entries  # noqa: E402
from src.lp_percpt import models  # noqa: E402
from src.lp_percpt.identify import split_clauses  # noqa: E402

VETO = 0.6


def concept_level(text, cid):
    ents = entries(cid)
    if not ents:
        return None, ""
    units = split_clauses(text) + [text]
    sim = models.similarity(units, [r for _, _, r in ents])
    ranked = sorted(((float(sim[:, j].max()), int(sim[:, j].argmax()), j) for j in range(len(ents))), reverse=True)
    top = ranked[:5]
    res = models.nli([(units[u], ents[j][2]) for _, u, j in top]) or [{"contradiction": 0.0}] * len(top)
    for (s, u, j), r in zip(top, res):
        if r["contradiction"] < VETO:
            return ents[j][0], f"{ents[j][0]} {ents[j][1]} ({s:.2f})"
    return None, "all top ways vetoed"


def main() -> None:
    rows = [s for s in json.loads((ROOT / "output" / "scenario_run_v10_all" / "results.json").read_text(encoding="utf-8"))["scenarios"]
            if s.get("expected_level")]
    score = Counter()
    per = Counter()
    hits = {"A": Counter(), "B": Counter()}
    for s in rows:
        target = GRAPH_KEY.get(s["id"], (s["expected_level"],))[0]
        per[target] += 1
        levels = {"A": [], "B": []}
        wrong_by_run = False
        for c in s["concepts"]:
            if "judge_only" in (c.get("gates") or []):
                continue                                   # linked by the algorithm, not added by the judge
            lv, why = concept_level(s["text"], c["concept"])
            if lv is None:
                continue
            levels["A"].append(lv)
            run_l0 = c.get("level_source") == "run" and c["prompt_level"] == "L0"
            confirmed = any(e["statement"].startswith("confirmed by the run") for e in c.get("evidence") or [])
            b = "L0" if run_l0 else (max(lv, "L2") if confirmed and lv != "L0" else lv)
            wrong_by_run |= run_l0
            levels["B"].append(b)
        for v in ("A", "B"):
            ls = levels[v]
            got = None if not ls else ("L0" if "L0" in ls else max(ls))
            ok = got == target
            score[v] += ok
            hits[v][target] += ok
    print("on the 44 (graph-boundary levels):")
    print(f"  LLM judge algorithm (v10, saved)         38/44")
    print(f"  NLI algorithm (v7, saved)                28/44")
    print(f"  step 1 way matching, top way (A)          {score['A']}/44   "
          + "  ".join(f"{k} {hits['A'][k]}/{per[k]}" for k in sorted(per)))
    print(f"  step 1 way matching + code run truth (B)  {score['B']}/44   "
          + "  ".join(f"{k} {hits['B'][k]}/{per[k]}" for k in sorted(per)))


if __name__ == "__main__":
    main()
