"""Run the graph-traversal classifier on the labelled scenarios (no LLM).

Writes ``output/lp_graph/results.json``, ``summary.txt``, ``report.md`` and
``unmatched.json`` (every unmatched answer statement with its scenario id -
use it to grow ``src/lp_graph/lexicon.py``).

Scenarios come from the full repo when it is on the path
(``scripts/run_student_scenarios.load_scenarios`` / ``asked_part`` and
``scripts/check_steps_44.GOLD``); otherwise from a JSON file
(``--scenarios``, default ``data/scenarios_44.json``) holding a list of::

    {"id": "...", "code": "...", "question": "...", "answer": "...",
     "gold_level": "L0".."L4", "gold_concept": "<concept id>"}

    python scripts/run_lp_graph_44.py [--scenarios data/scenarios_44.json] [--nli]
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))

from lp_graph.graph import KG  # noqa: E402
from lp_graph.knowledge import LEVELS  # noqa: E402
from lp_graph.pipeline import assess  # noqa: E402

OUT = ROOT / "output" / "lp_graph"


def load(path: Path) -> list[dict]:
    """Labelled scenarios from the repo modules, else from ``path``."""
    try:  # pragma: no cover - only in the full repo
        from check_steps_44 import GOLD  # type: ignore
        from run_student_scenarios import asked_part, load_scenarios  # type: ignore
    except ImportError:
        with path.open(encoding="utf-8") as fh:
            return sorted(json.load(fh), key=lambda s: str(s["id"]))
    rows = []
    for sc in load_scenarios():
        sid = str(sc["id"])
        gold = GOLD.get(sid) or GOLD.get(sc["id"]) or {}
        rows.append({"id": sid, "code": sc.get("code", ""),
                     "question": asked_part(sc), "answer": sc.get("answer", ""),
                     "gold_level": gold.get("level") or sc.get("gold_level"),
                     "gold_concept": gold.get("concept") or sc.get("gold_concept")})
    return sorted(rows, key=lambda s: s["id"])


def lv(x: str | None) -> int | None:
    return LEVELS.index(x) if x in LEVELS else None


def summarise(rows: list[dict]) -> tuple[str, dict]:
    n = len(rows)
    pairs = [(lv(r["pred_level"]), lv(r["gold_level"])) for r in rows if lv(r["gold_level"]) is not None]
    exact = sum(p == g for p, g in pairs)
    within = sum(p is not None and abs(p - g) <= 1 for p, g in pairs)
    errs = [abs((p if p is not None else 0) - g) for p, g in pairs]
    mae = sum(errs) / len(errs) if errs else 0.0
    per_level = {}
    for L in LEVELS:
        sub = [r for r in rows if r["gold_level"] == L]
        if sub:
            per_level[L] = f"{sum(r['pred_level'] == L for r in sub)}/{len(sub)}"
    in_map = sum(bool(r["gold_concept"]) and r["gold_concept"] in r["map_concepts"] for r in rows)
    main_ok = sum(r["main_concept"] == r["gold_concept"] for r in rows)
    lvl_on_concept = sum(r["level_on_gold_concept"] == r["gold_level"] for r in rows)
    gold_l0 = [r for r in rows if r["gold_level"] == "L0"]
    l0_caught = sum(r["pred_level"] == "L0" for r in gold_l0)
    unmatched = sum(len(r["unmatched"]) for r in rows)
    named = sum(len(r["misconceptions"]) for r in rows)
    unlisted = sum(r["unlisted"] for r in rows)
    stats = {"n": n, "exact": exact, "within_1": within, "mae": round(mae, 3),
             "per_level": per_level, "right_concept_in_map": in_map, "main_concept_right": main_ok,
             "right_level_on_right_concept": lvl_on_concept, "l0_caught": l0_caught,
             "gold_l0": len(gold_l0), "unmatched_statements": unmatched,
             "misconceptions_named": named, "unlisted_errors": unlisted}
    per = " ".join(f"{k} {v}" for k, v in per_level.items())
    line = (f"lp_graph (PPR + ES-Viterbi, no LLM): exact {exact}/{len(pairs)}, "
            f"within-1 {within}/{len(pairs)}, MAE {mae:.2f} | per level {per} | "
            f"right concept in map {in_map}/{n}, main concept right {main_ok}/{n}, "
            f"right level on right concept {lvl_on_concept}/{n} | "
            f"L0 caught {l0_caught}/{len(gold_l0)} | unmatched statements {unmatched} | "
            f"misconceptions named {named} vs unlisted {unlisted}")
    return line, stats


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--scenarios", default=str(ROOT / "data" / "scenarios_44.json"))
    ap.add_argument("--nli", action="store_true", help="enable the optional NLI fallback")
    args = ap.parse_args()

    kg = KG()
    scenarios = load(Path(args.scenarios))
    OUT.mkdir(parents=True, exist_ok=True)
    rows, full, report, unmatched_all = [], [], [f"# lp_graph on {len(scenarios)} scenarios",
                                                 f"graph {kg.version}", ""], []
    for sc in scenarios:
        a = assess(sc["code"], sc["question"], sc["answer"], kg, use_nli=args.nli)
        gold_c = sc.get("gold_concept")
        row = {"id": sc["id"], "gold_level": sc.get("gold_level"), "gold_concept": gold_c,
               "pred_level": a.headline_level, "main_concept": a.main_concept,
               "map_concepts": a.route_student.concepts(),
               "level_on_gold_concept": a.levels[gold_c].level if gold_c in a.levels else "none",
               "misconceptions": [m["id"] for m in a.misconceptions],
               "unlisted": len(a.unlisted), "unmatched": a.unmatched}
        rows.append(row)
        full.append({"id": sc["id"], "gold": {"level": row["gold_level"], "concept": gold_c},
                     "assessment": a.to_dict()})
        unmatched_all += [{"scenario": sc["id"], **u} for u in a.unmatched]
        report += [f"## {sc['id']} (gold {row['gold_level']} {gold_c}; "
                   f"pred {a.headline_level} {a.main_concept})", "", "```", a.to_markdown(), "```", ""]
    line, stats = summarise(rows)
    (OUT / "results.json").write_text(json.dumps(full, indent=1, ensure_ascii=False), encoding="utf-8")
    (OUT / "summary.txt").write_text(line + "\n\n" + json.dumps(stats, indent=1) + "\n", encoding="utf-8")
    (OUT / "report.md").write_text("\n".join(report), encoding="utf-8")
    (OUT / "unmatched.json").write_text(json.dumps(unmatched_all, indent=1, ensure_ascii=False),
                                        encoding="utf-8")
    top = Counter(u["text"].strip().lower() for u in unmatched_all).most_common(10)
    print(line)
    print("10 most frequent unmatched statements:")
    for text, k in top:
        print(f"  {k:>3}  {text}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
