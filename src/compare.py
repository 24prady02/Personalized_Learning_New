"""Compare Stage 2 diagnoses with the gold labels of data/raw/scenarios_20.json (checking only; gold is never an input).

    python src/compare.py                  # data/processed/<sid>_diagnosis.json  (default settings)
    python src/compare.py --tag bm25       # data/processed/<sid>_diagnosis.bm25.json (a run made with --tag bm25)
    python src/compare.py --tag "" bm25    # both side by side

Per scenario: held misconceptions (gold.held vs the held misconception edges), correct misconceptions (gold.correct vs
edges labelled correct in the evidence), root cause, overall level (in gold accept list), per-concept levels the gold
scores, and the gold edges (confirmed / broken; "context" edges are not scored). Writes results/tables/stage2_vs_gold.csv
and results/stage2_results.md.
"""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from utils import PROCESSED_DIR, RESULTS_DIR, load_scenarios


def score(diag: dict, gold: dict) -> dict:
    ev = diag.get("evidence", diag.get("paths", []))
    held_recs = [h for h in diag.get("held_misconceptions", []) if h.get("kind") == "misconception"]
    held = {h["misconception"] for h in held_recs}
    correct = {c["target"] for c in ev if c["kind"] == "misconception" and c["label"] == "correct"}
    g_held, g_correct = set(gold.get("held", [])), set(gold.get("correct", []))
    # held is right when every gold misconception is held and each extra one rests on the same words as a gold one
    # (the graph words one wrong idea in several ways; the gold names one of them)
    name_of_edge = {f"mis:{h['concept']}->{h['misconception']}": h["misconception"] for h in held_recs}
    extras_ok = all(name_of_edge.get(h.get("shares_evidence_with", ""), None) in g_held
                    for h in held_recs if h["misconception"] not in g_held)
    held_ok = g_held <= held and extras_ok
    root = diag.get("root_cause")
    g_root = gold.get("root_cause")
    # a gold may accept several root causes (two independent faults): any of them counts
    root_accept = gold.get("root_cause_accept") or [g_root]
    root_ok = (root or None) in [r or None for r in root_accept]
    overall_ok = diag.get("overall_level") in (gold.get("overall_level") or {}).get("accept", [])
    lv_hit = lv_tot = 0
    for concept, spec in (gold.get("levels") or {}).items():
        lv_tot += 1
        if (diag.get("levels") or {}).get(concept, {}).get("level") in spec.get("accept", []):
            lv_hit += 1
    labels_by_edge = {}
    for c in ev:                                   # the best label seen for each edge
        labels_by_edge.setdefault(c["edge"], c["label"])
    ed_hit = ed_tot = 0
    for e in gold.get("edges", []):
        if e["status"] not in ("confirmed", "broken"):
            continue
        ed_tot += 1
        ed_hit += labels_by_edge.get(e["id"]) == e["status"]
    return {
        "held_ok": held_ok, "held_pred": sorted(held), "held_gold": sorted(g_held),
        "correct_ok": g_correct <= correct, "correct_pred": sorted(correct), "correct_gold": sorted(g_correct),
        "root_ok": root_ok, "root_pred": root, "root_gold": g_root,
        "overall_ok": overall_ok, "overall_pred": diag.get("overall_level"), "overall_gold": (gold.get("overall_level") or {}).get("level"),
        "levels": f"{lv_hit}/{lv_tot}", "edges": f"{ed_hit}/{ed_tot}",
        "stop": diag.get("stop_reason", diag.get("status")), "prompts": sum((diag.get("llm_calls_by_step") or {}).values()),
        "points": int(held_ok) + int(g_correct <= correct) + int(root_ok) + int(overall_ok) + lv_hit + ed_hit,
        "max_points": 4 + lv_tot + ed_tot,
    }


def main(argv=None) -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--tag", nargs="*", default=[""], help="diagnosis file suffixes to compare ('' = default run)")
    ap.add_argument("--processed", default=str(PROCESSED_DIR))
    a = ap.parse_args(argv)
    scenarios = [s for s in load_scenarios() if not s.get("reference_case")]
    rows, totals = [], {}
    for tag in a.tag:
        suffix = f".{tag}" if tag else ""
        name = tag or "default"
        tot = {"points": 0, "max_points": 0, "held": 0, "correct": 0, "root": 0, "overall": 0, "prompts": 0, "n": 0}
        for s in scenarios:
            f = Path(a.processed) / f"{s['id']}_diagnosis{suffix}.json"
            if not f.exists():
                continue
            r = score(json.loads(f.read_text(encoding="utf-8")), s.get("gold", {}))
            rows.append({"run": name, "scenario": s["id"], **r})
            tot["n"] += 1
            for k in ("points", "max_points", "prompts"):
                tot[k] += r[k]
            for k in ("held", "correct", "root", "overall"):
                tot[k] += int(r[f"{k}_ok"])
        totals[name] = tot

    RESULTS_DIR.joinpath("tables").mkdir(parents=True, exist_ok=True)
    with open(RESULTS_DIR / "tables/stage2_vs_gold.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()) if rows else ["run"])
        w.writeheader()
        for r in rows:
            w.writerow({k: json.dumps(v) if isinstance(v, (list, dict)) else v for k, v in r.items()})

    md = ["# Stage 2 vs gold", "", "Gold is used here only for checking. A tick means the prediction matches the gold "
          "(every gold held misconception held and each extra held one resting on the same words as a gold one; every gold correct misconception found; root cause equal; overall level in the accept list). "
          "levels = gold-scored concepts whose level is in the accept list; edges = gold confirmed/broken edges labelled the same.", ""]
    for name, tot in totals.items():
        md += [f"## {name}  ({tot['n']} scenarios)", "",
               f"held {tot['held']}/{tot['n']}, correct {tot['correct']}/{tot['n']}, root {tot['root']}/{tot['n']}, overall level "
               f"{tot['overall']}/{tot['n']}, points {tot['points']}/{tot['max_points']}, prompts {tot['prompts']}", "",
               "| scenario | held | correct | root | overall | levels | edges | stop | prompts | points |", "|---|---|---|---|---|---|---|---|---|---|"]
        for r in rows:
            if r["run"] != name:
                continue
            t = lambda ok: "yes" if ok else "no"
            md.append(f"| {r['scenario']} | {t(r['held_ok'])} {r['held_pred']} | {t(r['correct_ok'])} {r['correct_pred']} | {t(r['root_ok'])} | "
                      f"{t(r['overall_ok'])} {r['overall_pred']} (gold {r['overall_gold']}) | {r['levels']} | {r['edges']} | {r['stop']} | {r['prompts']} | {r['points']}/{r['max_points']} |")
        md.append("")
    (RESULTS_DIR / "stage2_results.md").write_text("\n".join(md), encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    main()
