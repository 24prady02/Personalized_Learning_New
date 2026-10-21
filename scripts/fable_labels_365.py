"""
fable_labels_365.py — Fable 5.1 labels the level of every scenario (the reference);
the algorithm (its judge is Opus 5.5, fused with the code run and the graph rules,
locating the has_level edges) is scored against those labels.

Fable sees the question part, the code, the code-run facts, the student's answer,
the per-concept L0-L4 edge logic of the graph and the boundary rules; never the
algorithm's level. Its labels are first checked on the 44 human-labelled answers.

Usage: python scripts/fable_labels_365.py [--run scenario_run_v10_all] [--workers 2]
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import reference_labels_365 as rl  # noqa: E402
from fuse_44 import GRAPH_KEY  # noqa: E402
from reference_labels_365 import BOUNDARIES, call, lv, pmap  # noqa: E402
from reference_panel_365 import SYSTEM, facts_of, wilson  # noqa: E402
from run_student_scenarios import asked_part, load_scenarios  # noqa: E402
from src.lp_percpt import judge as judgelib  # noqa: E402

OUT = ROOT / "output" / "fable_labels"
LEVELS = ["L0", "L1", "L2", "L3", "L4", "none"]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", default="scenario_run_v10_all")
    ap.add_argument("--workers", type=int, default=2)
    args = ap.parse_args()
    rl.WORKERS = args.workers
    questions, scenarios = load_scenarios()
    res = {s["id"]: s for s in json.loads((ROOT / "output" / args.run / "results.json").read_text(encoding="utf-8"))["scenarios"]}
    rows = []
    for s in scenarios:
        q = questions.get(s["question"], {})
        r = res[s["id"]]
        asked = asked_part(q.get("question", ""), s["scenario_type"]) or q.get("question", "")
        concepts = list(dict.fromkeys(c["concept"] for c in r["concepts"]))
        text = (judgelib.build_prompt(s["text"], asked, q.get("code", ""), facts_of(r), concepts)
                if concepts else
                f"QUESTION (part asked): {asked}\n\nCODE:\n{(q.get('code') or '(none)')[:1500]}\n\n"
                f"STUDENT ANSWER: {s['text']}\n\n(no concept of the graph was linked to this answer)")
        rows.append({"id": s["id"], "type": s["scenario_type"], "text": s["text"], "label": s["expected_level"],
                     "graph_label": GRAPH_KEY.get(s["id"], (s["expected_level"],))[0] if s["expected_level"] else None,
                     "algorithm": lv(r["max_level"]),
                     "algorithm_edges": [f'{c["concept"]} -> {c["prompt_level"]}: {(c.get("prompt_reason") or "")[:90]}'
                                         for c in r["concepts"] if c["assessed"]],
                     "prompt": text + "\n\n" + BOUNDARIES + "\n\nGrade it."})

    outs = pmap(lambda r: call("fable", SYSTEM, r["prompt"]), rows, "fable labelled")
    for r, o in zip(rows, outs):
        r["fable"] = lv(o.get("overall"))
        r["fable_concepts"] = {c.get("concept"): c.get("level") for c in o.get("concepts", [])}
        r["fable_why"] = "; ".join(f'{c.get("concept")}: {c.get("why", "")}' for c in o.get("concepts", []))[:400]
        r["unavailable"] = bool(o.get("unavailable"))
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "labels.json").write_text(json.dumps([{k: v for k, v in r.items() if k != "prompt"} for r in rows],
                                                indent=1, ensure_ascii=False), encoding="utf-8")

    lab = [r for r in rows if r["label"]]
    unl = [r for r in rows if not r["label"]]
    lines = []
    for who in ("fable", "algorithm"):
        k = sum(r[who] == r["graph_label"] for r in lab)
        lines.append(f"on the 44 human-labelled (graph-boundary key): {who:9s} {k}/44")
    d44 = [r for r in lab if r["fable"] != r["algorithm"]]
    lines.append(f"on the 44: they disagree on {len(d44)}; algorithm right {sum(r['algorithm'] == r['graph_label'] for r in d44)}, "
                 f"fable right {sum(r['fable'] == r['graph_label'] for r in d44)}")
    k = sum(r["algorithm"] == r["fable"] for r in unl)
    lo, hi = wilson(k, len(unl))
    lines.append(f"THE 321: algorithm matches Fable's label on {k}/{len(unl)} = {k / len(unl):.0%} "
                 f"(95% interval {lo:.0%}-{hi:.0%}); within one level "
                 f"{sum(r['algorithm'] != 'none' and r['fable'] != 'none' and abs(int(r['algorithm'][1]) - int(r['fable'][1])) <= 1 for r in unl)}")
    allk = sum(r["algorithm"] == (r["graph_label"] or r["fable"]) for r in rows)
    lines.append(f"ALL 365 (human label where there is one, else Fable's): {allk}/365 = {allk / 365:.0%}")
    per, hit = Counter(r["fable"] for r in unl), Counter(r["fable"] for r in unl if r["algorithm"] == r["fable"])
    lines.append("321 by Fable's level: " + "  ".join(f"{x} {hit[x]}/{per[x]}" for x in LEVELS))
    conf = Counter((r["algorithm"], r["fable"]) for r in unl)
    lines.append("321 confusion (rows = algorithm, columns = Fable):")
    lines.append("        " + "".join(f"{c:>6}" for c in LEVELS))
    for a in LEVELS:
        lines.append(f"{a:>7} " + "".join(f"{conf[(a, b)]:>6}" for b in LEVELS))
    lines.append(f"Fable calls unavailable: {sum(r['unavailable'] for r in rows)}")
    print("\n".join(lines))
    (OUT / "summary.txt").write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()
