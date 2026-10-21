"""
run_answer_graph_44.py — run the answer-graph classifier (src/lp_percpt/answer_graph.py)
on the 44 labelled scenarios and draw each answer's concept map.

Modes:
    nli   NLI has_level edges (all ways, L0-L4) + code-run edges
    full  nli + question-form edges (a part that asks beyond the code -> L4, why / fix -> L3)

Usage:
    python scripts/run_answer_graph_44.py [--nli cross-encoder/nli-deberta-v3-small] [--tag small]

Writes output/answer_graph_<tag>/results.json, maps.html and prints the level check.
"""
from __future__ import annotations

import argparse
import html
import json
import shutil
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from check_steps_44 import GOLD  # noqa: E402
from run_student_scenarios import asked_part, load_scenarios  # noqa: E402
from src.lp_percpt.answer_graph import Edge, build  # noqa: E402
from src.lp_percpt.engine import LPPercptEngine  # noqa: E402

COLOURS = {"L0": "#9e9e9e", "L1": "#d9534f", "L2": "#f0ad4e", "L3": "#5bc0de", "L4": "#5cb85c", None: "#ffffff"}


def run_and_question_edges(result):
    """Edges the code run decided, and the engine's question-form edges."""
    run, ques = [], []
    for c in result["concepts"]:
        cid = c["concept"]
        if "inconsistent_trace" in (c.get("prompt_reason") or ""):
            run.append(Edge(cid, "L0", "inconsistent_trace", 1.0, "wrong claims >= confirmed claims", "run"))
        for it in c["evidence"]:
            st = it["statement"]
            if st.startswith("confirmed by the run") and it["status"] == "met":
                run.append(Edge(cid, "L2", (it.get("way") or "L2 one_step_execution").split()[-1], 1.0, st, "run"))
            elif it["check"] == "held" and "match a run" in st:
                run.append(Edge(cid, "L0", "misconception", 1.0, st, "run", st.split(":")[0]))
            elif it["check"] in ("E3", "E4") and it["status"] == "met" and (
                    st.startswith("answers:") or st in ("fix for the given code", "change predicted")
                    or st.startswith("diagnoses ")):
                ques.append(Edge(cid, "L" + it["check"][1], (it.get("way") or "").split()[-1], 0.9, st, "question"))
    return run, ques


def draw(sid, row) -> str:
    """One answer's concept map: answer node -> concepts (coloured by level) -> misconceptions."""
    concepts = list(row["levels"])
    mis = sorted({e["misconception"] for e in row["edges"] if e["misconception"]})
    h = max(len(concepts), len(mis), 1) * 70 + 40
    ay = h / 2
    out = [f'<svg width="900" height="{h}" xmlns="http://www.w3.org/2000/svg" font-family="sans-serif" font-size="12">']
    out.append(f'<rect x="10" y="{ay-22}" width="150" height="44" rx="8" fill="#eef" stroke="#557"/>'
               f'<text x="85" y="{ay+4}" text-anchor="middle">answer {sid}</text>')
    pos = {}
    for i, cid in enumerate(concepts):
        y = 40 + i * 70
        pos[cid] = y
        lv = row["levels"][cid]
        best = [e for e in row["edges"] if e["concept"] == cid and e["level"] == lv]
        label = (f'{best[0]["level"]} {best[0]["way"]} ({best[0]["source"]} {best[0]["support"]:.2f})'
                 if best else (row["reasons"][cid].split(";")[0] if lv else "not assessed"))
        out.append(f'<line x1="160" y1="{ay}" x2="390" y2="{y}" stroke="#888" stroke-dasharray="{"" if lv else "4 3"}"/>')
        out.append(f'<text x="200" y="{(ay + y) / 2 - 4}" fill="#333">{html.escape(label[:48])}</text>')
        gold = cid in GOLD.get(sid, set())
        out.append(f'<rect x="390" y="{y-18}" width="230" height="36" rx="6" fill="{COLOURS[lv]}" '
                   f'stroke="{"#000" if gold else "#999"}" stroke-width="{2.5 if gold else 1}"/>'
                   f'<text x="505" y="{y+4}" text-anchor="middle">{html.escape(cid)} · {lv or "—"}</text>')
    for k, m in enumerate(mis):
        y = 40 + k * 70
        out.append(f'<rect x="680" y="{y-18}" width="210" height="36" rx="6" fill="#fde" stroke="#c33"/>'
                   f'<text x="785" y="{y+4}" text-anchor="middle">{html.escape(m[:30])}</text>')
        for e in row["edges"]:
            if e["misconception"] == m and e["concept"] in pos:
                out.append(f'<line x1="620" y1="{pos[e["concept"]]}" x2="680" y2="{y}" stroke="#c33"/>')
    out.append("</svg>")
    return "".join(out)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--nli", default="cross-encoder/nli-deberta-v3-small")
    ap.add_argument("--tag", default="small")
    args = ap.parse_args()
    out = ROOT / "output" / f"answer_graph_{args.tag}"
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    eng = LPPercptEngine(store_dir=out / "students", map_dir=None, review_log=None)
    kg = eng.kg
    questions, scenarios = load_scenarios()
    rows = []
    for s in [s for s in scenarios if s["expected_level"]]:
        q = questions.get(s["question"], {})
        asked = asked_part(q.get("question", ""), s["scenario_type"])
        shown = f"{q.get('source') or ''}\n{q.get('question', '')}\n{q.get('code', '')}"
        r = eng.process(s["id"], s["text"], code=q.get("code", ""), shown_text=shown, session_id="ag", asked=asked)
        run, ques = run_and_question_edges(r)
        row = {"id": s["id"], "type": s["scenario_type"], "expected": s["expected_level"], "text": s["text"],
               "asked": asked, "gold": sorted(GOLD[s["id"]])}
        for mode, qe in (("nli", []), ("full", ques)):
            g = build(s["text"], asked, q.get("code", ""), kg, args.nli, run_edges=run, question_edges=qe)
            row[mode] = {"levels": g.levels, "reasons": g.reasons, "edges": [e.to_dict() for e in g.edges],
                         "best": g.best_level(), "main": g.main_concept(),
                         "main_level": g.levels.get(g.main_concept()) if g.main_concept() else None}
        rows.append(row)
        print(s["id"], s["expected_level"], "| nli", row["nli"]["best"], "| full", row["full"]["best"],
              row["full"]["main"], flush=True)

    (out / "results.json").write_text(json.dumps(rows, indent=1, ensure_ascii=False), encoding="utf-8")
    lines = []
    for mode in ("nli", "full"):
        best = [r[mode]["best"] for r in rows]
        exact = sum(b == r["expected"] for b, r in zip(best, rows))
        within = sum(b is not None and abs(int(b[1]) - int(r["expected"][1])) <= 1 for b, r in zip(best, rows))
        mae = sum(abs(int((b or "L0")[1]) - int(r["expected"][1])) for b, r in zip(best, rows)) / len(rows)
        per = Counter(r["expected"] for r in rows)
        hit = Counter(r["expected"] for b, r in zip(best, rows) if b == r["expected"])
        gold_lv = sum(any(r[mode]["levels"].get(c) == r["expected"] for c in r["gold"]) for r in rows)
        gold_in = sum(bool(set(r[mode]["levels"]) & set(r["gold"])) for r in rows)
        main_ok = sum(r[mode]["main"] in r["gold"] for r in rows)
        line = (f"{mode}: exact {exact}/44, within-1 {within}, MAE {mae:.2f}, per level "
                f"{ {k: f'{hit[k]}/{per[k]}' for k in sorted(per)} }, right concept in map {gold_in}/44, "
                f"main concept right {main_ok}/44, right level on right concept {gold_lv}/44")
        print(line); lines.append(line)
        print("  edge sources:", Counter(e["source"] + ":" + e["level"] for r in rows for e in r[mode]["edges"]))
    (out / "summary.txt").write_text("\n".join(lines), encoding="utf-8")

    cards = []
    for r in rows:
        for mode in ("full",):
            m = r[mode]
            ok = "✓" if m["best"] == r["expected"] else "✗"
            cards.append(f'<section><h3>{r["id"]} · {html.escape(r["type"])} · expected {r["expected"]} · got {m["best"]} {ok}</h3>'
                         f'<p><b>Asked:</b> {html.escape(r["asked"][:200])}<br><b>Answer:</b> {html.escape(r["text"][:300])}</p>'
                         f'{draw(r["id"], m)}<ul>'
                         + "".join(f"<li><b>{html.escape(c)}</b>: {html.escape(m['reasons'][c])}</li>" for c in m["levels"])
                         + "</ul></section>")
    (out / "maps.html").write_text(
        "<!doctype html><meta charset='utf-8'><title>Answer graphs, 44 scenarios</title>"
        "<style>body{font-family:sans-serif;margin:16px;background:#fff;color:#222}section{border-bottom:1px solid #ddd;padding:8px 0}"
        "svg{max-width:100%;height:auto}</style><h1>Answer graphs: 44 labelled scenarios</h1>"
        "<p>Concept colour = level (L0 grey, L1 red, L2 orange, L3 blue, L4 green, white = not assessed); "
        "thick black border = the concept the answer is about (judged). Edge label = the has_level way matched, its source and support.</p>"
        + "\n".join(cards), encoding="utf-8")
    print("wrote", out)


if __name__ == "__main__":
    main()
