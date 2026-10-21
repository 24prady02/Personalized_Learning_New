"""
select_60.py — choose 60 of the 169 scenarios that have a level (44 human, 125 Fable)
so that together they cover the graph's edge logic and the diversity of students.

Features of a scenario (all from saved results, no model calls):
  edge logic   every has_level way located in it ("L2 one_step_execution", "L0 everyday_reading", ...),
               by the algorithm or by Fable; every concept linked; every Chapter-1 section
  diversity    its level (L0-L4 / none), its scenario-type family, answer vs own question,
               the question's format, the question itself

Greedy cover: repeatedly take the scenario adding the most still-uncovered features
(ways and levels weigh more), ties to human-labelled ones; levels kept balanced.

Writes output/selected_60/selected_60.json, .xlsx and coverage.txt
Usage: python scripts/select_60.py [--n 60]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import reference_labels_365 as rl  # noqa: E402
from fuse_44 import GRAPH_KEY  # noqa: E402
from reference_labels_365 import BOUNDARIES, lv  # noqa: E402
from reference_panel_365 import SYSTEM, facts_of  # noqa: E402
from run_student_scenarios import asked_part, load_scenarios  # noqa: E402
from src.lp_percpt import judge as judgelib  # noqa: E402
from src.lp_percpt.knowledge import get_knowledge  # noqa: E402

WAYS = ("everyday_reading|misconception|inconsistent_trace|names_the_element|states_the_rule|line_by_line_trace|"
        "output_prediction|one_step_execution|relation_to_neighbour|purpose_of_the_whole|diagnose_an_error|"
        "predict_a_change|transfer_to_a_new_program")
WAY_RE = re.compile(rf"\b(L[0-4])\b[^|;]*?\b({WAYS})\b")
WEIGHT = {"way": 3, "level": 3, "section": 2, "family": 2, "concept": 1, "kind": 2, "format": 1, "question": 0.5, "code": 1}


def fable_output(s, q, r):
    asked = asked_part(q.get("question", ""), s["scenario_type"]) or q.get("question", "")
    cs = list(dict.fromkeys(c["concept"] for c in r["concepts"]))
    text = (judgelib.build_prompt(s["text"], asked, q.get("code", ""), facts_of(r), cs) if cs else
            f"QUESTION (part asked): {asked}\n\nCODE:\n{(q.get('code') or '(none)')[:1500]}\n\nSTUDENT ANSWER: {s['text']}"
            "\n\n(no concept of the graph was linked to this answer)")
    p = text + "\n\n" + BOUNDARIES + "\n\nGrade it."
    f = rl.CACHE / (hashlib.sha256(("fable" + SYSTEM + p).encode("utf-8")).hexdigest()[:24] + ".json")
    if not f.exists():
        return None
    o = json.loads(f.read_text(encoding="utf-8"))
    return None if o.get("unavailable") else o


def family(t: str) -> str:
    m = re.match(r"\s*([A-Z]\d+)\b", t or "")
    if m:
        return m.group(1)[0] + "-series"
    return re.sub(r"\s*\([a-h]\)\s*$", "", (t or "").strip())[:40]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=60)
    ap.add_argument("--fable-only", action="store_true", help="leave out the 44 human-labelled scenarios")
    ap.add_argument("--keep-44", action="store_true", help="start from all 44 labelled scenarios, add the rest")
    ap.add_argument("--from-ids", help="limit the other scenarios to these ids (a JSON list, e.g. output/selected_100_fable/ids.json)")
    args = ap.parse_args()
    kg = get_knowledge()
    questions, scenarios = load_scenarios()
    res = {s["id"]: s for s in json.loads((ROOT / "output" / "scenario_run_v10_all" / "results.json").read_text(encoding="utf-8"))["scenarios"]}

    allowed = set(json.loads(Path(args.from_ids).read_text(encoding="utf-8"))) if args.from_ids else None
    pool = []
    for s in scenarios:
        q = questions.get(s["question"], {})
        r = res[s["id"]]
        o = fable_output(s, q, r)
        human = bool(s["expected_level"])
        if not human and o is None:
            continue                                   # no level: not one of the 169
        if human and args.fable_only:
            continue
        if not human and allowed is not None and s["id"] not in allowed:
            continue
        level = GRAPH_KEY.get(s["id"], (s["expected_level"],))[0] if human else lv(o.get("overall"))
        feats = {("level", level), ("family", family(s["scenario_type"])), ("kind", s["kind"] or ""),
                 ("format", str(q.get("format") or "")), ("question", s["question"]),
                 ("code", hashlib.sha256((q.get("code") or "").strip().encode("utf-8")).hexdigest()[:12])}
        ways = set()
        for c in r["concepts"]:
            if not c["assessed"]:
                continue
            feats.add(("concept", c["concept"]))
            if c["concept"] in kg.concepts:
                feats.add(("section", kg.concepts[c["concept"]].chapter))
            for lvl, w in WAY_RE.findall(c.get("prompt_reason") or ""):
                ways.add(f"{lvl} {w}")
        for c in (o or {}).get("concepts", []):
            if c.get("level") in ("L0", "L1", "L2", "L3", "L4") and c.get("way"):
                for w in re.findall(WAYS, c["way"]):
                    ways.add(f"{c['level']} {w}")
        feats |= {("way", w) for w in ways}
        pool.append({"id": s["id"], "human": human, "level": level, "level_by": "human" if human else "Fable",
                     "algorithm": lv(r["max_level"]), "type": s["scenario_type"], "kind": s["kind"],
                     "question": s["question"], "text": s["text"], "ways": sorted(ways),
                     "concepts": sorted(c for k, c in feats if k == "concept"), "feats": feats})

    print(f"pool: {len(pool)} scenarios with a level ({sum(p['human'] for p in pool)} human, "
          f"{sum(not p['human'] for p in pool)} Fable)")
    universe = set().union(*(p["feats"] for p in pool))
    covered, chosen = set(), []
    if args.keep_44:
        chosen = [p for p in pool if p["human"]]
        for p in chosen:
            covered |= p["feats"]
    per_level_cap = -(-args.n // 5) + 2                # keep the levels balanced
    while len(chosen) < args.n:
        counts = Counter(p["level"] for p in chosen)
        best, best_gain = None, -1.0
        for p in pool:
            if p in chosen:
                continue
            gain = sum(WEIGHT[k] for k, v in p["feats"] - covered)
            if counts[p["level"]] >= per_level_cap:
                gain -= 100
            key = (gain, p["human"], p["level"] != "none")
            if best is None or key > best_key:
                best, best_key, best_gain = p, key, gain
        chosen.append(best)
        covered |= best["feats"]

    out = ROOT / "output" / (f"selected_{args.n}" + ("_fable" if args.fable_only else "") + ("_keep44" if args.keep_44 else ""))
    out.mkdir(parents=True, exist_ok=True)
    rows = [{k: v for k, v in p.items() if k != "feats"} for p in chosen]
    (out / "selected_60.json").write_text(json.dumps(rows, indent=1, ensure_ascii=False), encoding="utf-8")

    lines = []
    for kind in WEIGHT:
        allk = {v for k, v in universe if k == kind}
        got = {v for k, v in covered if k == kind}
        lines.append(f"{kind:9s} covered {len(got)}/{len(allk)}" + (f"   missing: {sorted(map(str, allk - got))[:12]}" if allk - got else ""))
    lines.append("levels: " + str(dict(Counter(p["level"] for p in chosen))))
    lines.append(f"level written by: human {sum(p['human'] for p in chosen)}, Fable {sum(not p['human'] for p in chosen)}")
    all_ways = [f"L{l} {w}" for l, ws in (("0", "everyday_reading misconception inconsistent_trace"),
                                           ("1", "names_the_element states_the_rule"),
                                           ("2", "line_by_line_trace output_prediction one_step_execution"),
                                           ("3", "relation_to_neighbour purpose_of_the_whole diagnose_an_error"),
                                           ("4", "predict_a_change diagnose_an_error transfer_to_a_new_program"))
                for w in ws.split()]
    got_w = {v for k, v in covered if k == "way"}
    lines.append(f"graph ways (13 way names over 5 levels = {len(all_ways)}): covered {sum(w in got_w for w in all_ways)}; "
                 f"not in any of the 169: {[w for w in all_ways if w not in {v for k, v in universe if k == 'way'}]}")
    k = sum(p["algorithm"] == p["level"] for p in chosen)
    lines.append(f"algorithm matches the level on {k}/{len(chosen)} of the chosen (human {sum(p['algorithm'] == p['level'] for p in chosen if p['human'])}/"
                 f"{sum(p['human'] for p in chosen)}, Fable {sum(p['algorithm'] == p['level'] for p in chosen if not p['human'])}/"
                 f"{sum(not p['human'] for p in chosen)})")
    print("\n".join(lines))
    (out / "coverage.txt").write_text("\n".join(lines), encoding="utf-8")

    import openpyxl
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Selected 60"
    ws.append(["Scenario", "Needed level", "Level by", "Algorithm level", "Scenario type", "Question", "Answer",
               "Concepts", "Graph ways located"])
    for p in rows:
        ws.append([p["id"], p["level"], p["level_by"], p["algorithm"], p["type"], p["question"], p["text"][:300],
                   ", ".join(p["concepts"]), ", ".join(p["ways"])])
    wb.save(out / "selected_60.xlsx")
    print("wrote", out)


if __name__ == "__main__":
    main()
