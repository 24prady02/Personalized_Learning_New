"""
reference_panel_365.py — a stronger reference for all 365 answers: two models other
than the classifier's judge (Fable 5.1 and Sonnet 5.5) each mark every answer
independently, from the same graph material the classifier's judge reads (the
per-concept has_level ways and boundaries of L0-L4, the code-run facts and the
general boundary rules), but never the classifier's level.

  reference level = the level both markers give (settled); otherwise unsettled.

Validated on the 44 human-labelled answers (how many get settled, how often a
settled level is right), then the classifier is scored on the settled part of
the 321 and the unsettled part bounds what is left.

Usage: python scripts/reference_panel_365.py [--run scenario_run_v10_all]
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from fuse_44 import GRAPH_KEY  # noqa: E402
from reference_labels_365 import BOUNDARIES, call, lv, pmap  # noqa: E402
from run_student_scenarios import asked_part, load_scenarios  # noqa: E402
from src.lp_percpt import judge as judgelib  # noqa: E402

OUT = ROOT / "output" / "reference_panel"
PANEL = ("fable", "sonnet")     # set by --panel

SYSTEM = judgelib.SYSTEM.replace(
    'Return JSON only: {"concepts"',
    'Then give the OVERALL level of the answer: L0 if its reasoning anywhere uses a rule that contradicts Java; '
    'otherwise the highest level it correctly shows on any concept; "none" if nothing in it can be levelled '
    '(empty, off topic, or only a question).\nReturn JSON only: {"overall":"L0|L1|L2|L3|L4|none","concepts"')


def facts_of(result) -> list:
    """The code run's verdicts on the answer, as the classifier's judge received them."""
    facts = []
    for c in result["concepts"]:
        for it in c.get("evidence") or []:
            st = it["statement"]
            if st.startswith("confirmed by the run"):
                facts.append(f"CORRECT ({it['clause'][:80]!r}): {st}")
            elif it["check"] == "wrong_trace":
                facts.append(f"WRONG ({it['clause'][:80]!r}): {st}")
            elif it["check"] == "held" and "match a run" in st:
                facts.append(f"MISCONCEPTION: {st}")
            elif it["check"] == "own_run":
                facts.append(f"STUDENT'S CODE RUN ON THE QUESTION'S DATA: {st}")
    return list(dict.fromkeys(facts))


def wilson(k: int, n: int, z: float = 1.96):
    if n == 0:
        return (0.0, 1.0)
    p = k / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return ((c - h) / d, (c + h) / d)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", default="scenario_run_v10_all")
    ap.add_argument("--panel", default="fable,opus", help="the two marker models")
    ap.add_argument("--workers", type=int, default=2, help="calls at a time (memory)")
    args = ap.parse_args()
    global PANEL, OUT
    PANEL = tuple(args.panel.split(","))
    OUT = ROOT / "output" / ("reference_panel_" + "_".join(PANEL))
    import reference_labels_365
    reference_labels_365.WORKERS = args.workers
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
        rows.append({"id": s["id"], "label": s["expected_level"],
                     "graph_label": GRAPH_KEY.get(s["id"], (s["expected_level"],))[0] if s["expected_level"] else None,
                     "system": lv(r["max_level"]), "prompt": text + "\n\n" + BOUNDARIES + "\n\nGrade it."})

    for m in PANEL:
        outs = pmap(lambda r: call(m, SYSTEM, r["prompt"]), rows, f"{m} marked")
        for r, o in zip(rows, outs):
            r[m] = lv(o.get("overall"))
            r[m + "_concepts"] = {c.get("concept"): c.get("level") for c in o.get("concepts", [])}
            r[m + "_unavailable"] = bool(o.get("unavailable"))
    for r in rows:
        r["reference"] = r[PANEL[0]] if r[PANEL[0]] == r[PANEL[1]] else None
        r["algorithm_edges"] = [f'{c["concept"]} -> {c["prompt_level"]} ({(c.get("prompt_reason") or "").split(":")[0][:60]})'
                                for c in res[r["id"]]["concepts"] if c["assessed"]]
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "labels.json").write_text(json.dumps([{k: v for k, v in r.items() if k != "prompt"} for r in rows],
                                                indent=1, ensure_ascii=False), encoding="utf-8")

    lines = []
    lab = [r for r in rows if r["label"]]
    unl = [r for r in rows if not r["label"]]
    for m in PANEL:
        lines.append(f"on the 44 (graph-boundary key): {m} alone exact {sum(r[m] == r['graph_label'] for r in lab)}/44")
    lines.append(f"on the 44: classifier exact {sum(r['system'] == r['graph_label'] for r in lab)}/44")
    s44 = [r for r in lab if r["reference"]]
    ok44 = sum(r["reference"] == r["graph_label"] for r in s44)
    lo, hi = wilson(ok44, len(s44))
    lines.append(f"on the 44: panel settles {len(s44)}/44; settled levels right {ok44}/{len(s44)} "
                 f"(95% interval {lo:.0%}-{hi:.0%})")
    sys44 = sum(r["system"] == r["graph_label"] for r in s44)
    lines.append(f"on the 44, settled part: classifier right {sys44}/{len(s44)}; "
                 f"classifier matches the panel {sum(r['system'] == r['reference'] for r in s44)}/{len(s44)}")

    s321 = [r for r in unl if r["reference"]]
    m321 = sum(r["system"] == r["reference"] for r in s321)
    lo, hi = wilson(m321, len(s321))
    lines.append(f"THE 321: panel settles {len(s321)}/{len(unl)}; classifier matches the settled level on "
                 f"{m321}/{len(s321)} = {m321 / max(1, len(s321)):.0%} (95% interval {lo:.0%}-{hi:.0%})")
    u = len(unl) - len(s321)
    lines.append(f"THE 321: unsettled {u}; classifier matches one of the two markers on "
                 f"{sum(r['system'] in (r[PANEL[0]], r[PANEL[1]]) for r in unl if not r['reference'])}/{u}")
    per = Counter(r["reference"] for r in s321)
    hit = Counter(r["reference"] for r in s321 if r["system"] == r["reference"])
    lines.append("321 settled, by level: " + "  ".join(f"{k} {hit[k]}/{per[k]}" for k in ("L0", "L1", "L2", "L3", "L4", "none")))
    for m in PANEL:
        lines.append(f"all 365: algorithm matches {m} on {sum(r['system'] == r[m] for r in rows)}/365")
    lines.append(f"all 365: {PANEL[0]} and {PANEL[1]} agree on {sum(r[PANEL[0]] == r[PANEL[1]] for r in rows)}/365")
    lines.append(f"calls unavailable: {sum(r[m + '_unavailable'] for r in rows for m in PANEL)}")
    print("\n".join(lines))
    (OUT / "summary.txt").write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()
