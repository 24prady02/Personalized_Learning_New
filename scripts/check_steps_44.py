"""
check_steps_44.py — score each step of the classifier on the 44 labelled
scenarios (reads output/scenario_run_v7/steps_44.json and results.json).

GOLD is the concept(s) each answer is about, judged by hand from the question
part asked (the workbook gives only a level, not a concept).
"""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output" / (sys.argv[1] if len(sys.argv) > 1 else "scenario_run_v7")
for _s in (sys.stdout,):
    _s.reconfigure(encoding="utf-8", errors="replace")

GOLD = {
    "S088": {"compile", "run"}, "S089": {"incremental_development"}, "S090": {"class_declaration"},
    "S091": {"string_literal", "compile_time_error"}, "S093": {"integer_division", "operator_precedence"},
    "S094": {"command_line_args", "array_bounds"},
    "S095": {"primitive_type", "string_type", "primitive_vs_reference"}, "S096": {"data_type"},
    "S097": {"escape_sequences", "char_arithmetic"}, "S098": {"overflow", "int"}, "S101": {"exclusive_or"},
    "S103": {"math_round", "long_type"}, "S104": {"type_conversion", "explicit_cast"}, "S106": {"if_statement"},
    "S108": {"increment_operators"}, "S109": {"dangling_else", "nested_conditionals"},
    "S110": {"accumulator_pattern", "counter_pattern"},
    "S111": {"explicit_cast", "operator_precedence", "math_random"},
    "S112": {"break_statement", "continue_statement"}, "S113": {"infinite_loop"},
    "S114": {"array_default_values", "definite_assignment"}, "S115": {"printing_array_reference"},
    "S116": {"array_traversal"}, "S117": {"variable_swap"}, "S118": {"lookup_table"},
    "S119": {"boolean_flag_array"}, "S120": {"matrix_operations"},
    "S121": {"token_vs_line_input", "standard_input"}, "S122": {"token_vs_line_input"},
    "S123": {"interactive_input"}, "S124": {"filter"}, "S125": {"animation"}, "S126": {"standard_audio"},
    "S127": {"dangling_pages"}, "S128": {"transition_matrix", "matrix_operations"}, "S129": {"teleportation"},
    "S132": {"assignment"}, "S133": {"declaration", "definite_assignment"},
    "S134": {"variable_swap", "assignment"}, "S135": {"de_morgan"}, "S136": {"if_statement", "assignment"},
    "S137": {"println", "assignment"}, "S138": {"accumulator_pattern"},
    "S139": {"coordinate_scaling", "standard_drawing"},
}


def source(item: dict) -> str:
    """Which step produced the evidence item that set a level."""
    st, way = item["statement"], item.get("way", "")
    if st.startswith("confirmed by the run") or item["check"] == "wrong_trace":
        return "code run"
    if st.startswith("answers:") or st == "fix for the given code" or st == "change predicted":
        return "asked-part / wording rule"
    if st.startswith("edge ") or st == "overall purpose":
        return "relation cue rule"
    if st.startswith("L4 way:") or st.startswith("L3 way:"):
        return "NLI (way rule)"
    if st.startswith("refuted "):
        return "NLI (misconception refuted)"
    if st.startswith("diagnoses "):
        return "NLI (error node named)"
    if item["check"] == "E2":
        return "NLI (fact)" if item["score"] >= 0.5 and item["score"] != round(item["score"], 3) or True else ""
    return "similarity (E1)"


def main() -> None:
    steps = json.loads((OUT / "steps_44.json").read_text(encoding="utf-8"))
    res = {s["id"]: s for s in json.loads((OUT / "results.json").read_text(encoding="utf-8"))["scenarios"]}
    rows, tally = [], Counter()
    for r in steps:
        gold = GOLD[r["id"]]
        sem_top1 = {st["top_meaning"][0][0] for st in r["semantic"] if st["top_meaning"]}
        sem_top3 = {c for st in r["semantic"] for c, _, _ in st["top_meaning"]}
        linked = [l["concept"] for l in r["linking"]]
        assessed = [f["concept"] for f in r["final"]]
        tally["sem_top1"] += bool(gold & sem_top1)
        tally["sem_top3"] += bool(gold & sem_top3)
        tally["link_any"] += bool(gold & set(linked))
        tally["link_top"] += bool(linked and linked[0] in gold)
        tally["assessed"] += bool(gold & set(assessed))
        noise = [l["concept"] for l in r["linking"] if l["meaning"] == 0 and l["words"] == 0 and l["code"] == 0]
        tally["noise_links"] += len(noise)
        tally["links"] += len(linked)
        # linked only because semantic matching found it (no cue)
        tally["link_by_meaning_only"] += sum(1 for l in r["linking"] if not l["cues"])
        # the concept and evidence item that set the compared (highest) level
        s = res[r["id"]]
        best = None
        for c in s["concepts"]:
            if c["assessed"] and c["prompt_level"] == s["max_level"]:
                best = c; break
        src, way = "", ""
        if best:
            lv = int(best["prompt_level"][1])
            want = {0: None, 1: "E1", 2: "E2", 3: "E3", 4: "E4"}[lv]
            items = [e for e in best["evidence"] if e["check"] == want and e["status"] == "met"]
            if lv == 0:
                src = "code run" if "inconsistent" in best["prompt_reason"] else "NLI (misconception held)"
            elif items:
                it = max(items, key=lambda e: e["score"])
                src = source(it)
                if src.startswith("NLI (fact)"):
                    src = "NLI (fact)" if it["score"] >= 0.5 and "rule stated" not in it["statement"] else "similarity (fact)"
                    # similarity-only fact matches carry the cosine; NLI ones the entailment
                    n = [x for x in r["nli"] if x["concept"] == best["concept"] and x["clause"] == it["clause"]]
                    if n and n[0]["fact_ent"] < 0.5:
                        src = "similarity (fact)"
                way = it.get("way", "")
        rows.append({"id": r["id"], "expected": r["expected"], "got": s["max_level"], "gold": sorted(gold),
                     "sem_top1": sorted(sem_top1), "sem_top3_hit": bool(gold & sem_top3),
                     "linked": linked, "gold_linked": bool(gold & set(linked)),
                     "gold_top": bool(linked and linked[0] in gold), "gold_assessed": bool(gold & set(assessed)),
                     "level_concept": best["concept"] if best else None, "level_source": src, "level_way": way,
                     "level_ok": s["max_level"] == r["expected"]})
    n = len(steps)
    print({k: v for k, v in tally.items()}, "of", n)
    print("level source:", Counter(r["level_source"] for r in rows))
    print("level source, exact:", Counter(r["level_source"] for r in rows if r["level_ok"]))
    print("level source, wrong:", Counter(r["level_source"] for r in rows if not r["level_ok"]))
    print("gold linked & level ok:", sum(r["gold_linked"] and r["level_ok"] for r in rows),
          "gold not linked & level ok:", sum((not r["gold_linked"]) and r["level_ok"] for r in rows))
    for r in rows:
        print(r["id"], r["expected"], r["got"], "OK " if r["level_ok"] else "BAD", "| sem3", int(r["sem_top3_hit"]),
              "link", int(r["gold_linked"]), "top", int(r["gold_top"]), "| by", r["level_source"], r["level_way"],
              "on", r["level_concept"])
    # NLI decisions that passed their threshold
    p = Counter()
    for r in steps:
        for x in r["nli"]:
            p["pairs"] += 1
            p["fact_pass"] += x["fact_passed"]
            p["mis_pass"] += x["mis_passed"]
            for lv, w in x["ways"].items():
                p[f"{lv}_tested"] += 1
                p[f"{lv}_pass"] += w["passed"]
                p[f"{lv}_ent>=0.7"] += w["ent"] >= 0.7
    print("NLI:", dict(p))
    (OUT / "steps_44_check.json").write_text(json.dumps(rows, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
