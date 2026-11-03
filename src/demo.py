"""Demonstration without a notebook: ask for a Java program, a question and a student's answer, run Stage 1 and Stage 2
(exactly src/evaluate.py's extraction and src/traverse.py's walk, the Claude CLI for prune and label), draw every
step, and open one full-screen HTML page in the browser with all of it.

    python src/demo.py                       # asks for the three inputs in the terminal
    python src/demo.py --scenario T007       # a scenario from data/raw/scenarios_20.json
    python src/demo.py --input my.json       # {"code": ..., "question": ..., "answer": ...}
    python src/demo.py --id quiz3_s7         # choose the run id (default: next free MYnn)

Outputs: data/processed/<id>_subgraph.json, <id>_input.json, <id>_diagnosis.json; experiments/logs/traverse_<id>.txt;
results/viewer/<id>_figureNN.png, <id>_steps.md, <id>_demo.html (opened in the browser).
"""
from __future__ import annotations

import argparse
import base64
import json
import re
import sys
import time
import webbrowser
from pathlib import Path

import matplotlib
if __name__ == "__main__":
    matplotlib.use("Agg")                      # headless; imported from the notebook it keeps the inline backend
import matplotlib.pyplot as plt  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))
import model  # noqa: E402
import steps_report  # noqa: E402
import traverse  # noqa: E402
import viz  # noqa: E402
from utils import PROCESSED_DIR, RESULTS_DIR, ROOT, load_config, load_kg, load_scenarios  # noqa: E402


def ask_inputs() -> dict:
    print("Java program (paste the lines; type END on its own line when done):")
    lines = []
    while True:
        line = input()
        if line.strip() == "END":
            break
        lines.append(line)
    question = input("Question asked about the program: ").strip()
    answer = input("Student's answer: ").strip()
    return {"code": "\n".join(lines), "question": question, "answer": " ".join(answer.split())}


def next_id() -> str:
    n = 1
    while (PROCESSED_DIR / f"MY{n:02d}_diagnosis.json").exists():
        n += 1
    return f"MY{n:02d}"


class ProgressLLM(traverse.LLM):
    verbose = True

    def ask(self, prompt, step="other"):
        m = re.search(r"^(?:Concept under consideration|Concept): (\S+)", prompt, re.M)
        e = re.search(r"^Edge: (\S+)", prompt, re.M)
        what = (m.group(1) if m else "") + (f" {e.group(1)}" if e else "")
        t, calls = time.time(), self.calls
        reply = super().ask(prompt, step)
        if self.verbose:
            print(f"  {step:5s} {what:45s} {'cached' if self.calls == calls else f'claude -p {time.time() - t:.0f}s'}", flush=True)
        return reply


def run(sid: str, sc: dict, open_browser: bool = True, verbose: bool = True) -> Path:
    kg = load_kg()
    cfg = load_config()
    tcfg = {**traverse.DEFAULT_TRAVERSAL, **cfg.get("traversal", {})}
    code, question, answer = sc["code"], sc.get("question", ""), sc.get("answer", "")
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    (RESULTS_DIR / "viewer").mkdir(parents=True, exist_ok=True)
    (ROOT / "experiments/logs").mkdir(parents=True, exist_ok=True)

    # Stage 1
    sg = model.subgraph_from_code(code, kg, sid, int(cfg.get("hops", 0)), bool(cfg.get("keep_generic", False)))
    (PROCESSED_DIR / f"{sid}_subgraph.json").write_text(json.dumps(sg, indent=1, ensure_ascii=False), encoding="utf-8")
    (PROCESSED_DIR / f"{sid}_input.json").write_text(json.dumps({"code": code, "question": question, "answer": answer}, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"Stage 1: {sg['counts']['concepts']} concepts, {sg['counts']['concept_edges']} concept edges, {sg['counts']['mis_edges']} misconception edges")

    # Stage 2
    print(f"Stage 2: backend {tcfg['backend']}, model {tcfg['model']}, width {tcfg['width']}, depth {tcfg['depth']}")
    llm = ProgressLLM(tcfg)
    llm.verbose = verbose
    log: list[str] = []
    diag = traverse.traverse(sg, {"id": sid, "code": code, "question": question, "answer": answer}, tcfg, llm, log)
    diag["llm_calls"] = llm.calls
    (PROCESSED_DIR / f"{sid}_diagnosis.json").write_text(json.dumps(diag, indent=1, ensure_ascii=False), encoding="utf-8")
    (ROOT / "experiments/logs" / f"traverse_{sid}.txt").write_text("\n".join(log) + "\n", encoding="utf-8")
    held = [h["misconception"] for h in diag.get("held_misconceptions", [])]
    print(f"{sid}: held={held} root={diag.get('root_cause')} overall={diag.get('overall_level')} stop={diag.get('stop_reason')} prompts={diag.get('llm_calls_by_step')}")

    # figures, in the order the report refers to them
    g = traverse.Graph(sg)
    pos = viz.concept_layout(sg)
    figs: list[Path] = []

    def save(n: int):
        f = RESULTS_DIR / "viewer" / f"{sid}_figure{n:02d}.png"
        plt.savefig(f, dpi=110, bbox_inches="tight"); plt.close("all"); figs.append(f)
    _show = plt.show
    plt.show = lambda *a, **k: None
    viz.draw_graph(sg, pos, "Stage 1: the concept layer of G, with every concept edge"); save(1)
    viz.draw_full_G(sg, pos, "Stage 1: the whole subgraph G (concepts, misconception / error nodes, level nodes L0-L4)"); save(2)
    start = diag.get("start_concepts", [])
    viz.draw_graph(sg, pos, f"Start concepts (blue outline): {', '.join(start)}", reached=start, start=start); save(3)
    steps = viz.parse_log(log)
    reached, cstatus = set(start), {}
    n = 4
    for st in steps:
        sats = []
        for l in st["labels"]:
            kind, src, tgt = viz.edge_parts(l["edge"])
            if kind in ("mis", "err", "lvl"):
                sats.append((src, l["edge"], viz.satellite_text(g, l["edge"]), l["label"]))
            else:
                cstatus[l["edge"]] = l["label"] if l["label"] != "not applied" else cstatus.get(l["edge"])
                reached.update([src, tgt])
        reached.update(st["current"]); reached.update(st["brought"])
        viz.draw_graph(sg, pos, f"Depth {st['depth']}: labelled edges (thick = kept on a path)", reached=reached, start=start,
                       satellites=sats, cedge_status=cstatus, kept=set(st["kept"])); save(n); n += 1
    levels = diag.get("levels", {}); root = diag.get("root_cause") or {}
    sats = [(h["concept"], f"mis:{h['concept']}->{h['misconception']}", h["misconception"], "held") for h in diag.get("held_misconceptions", [])]
    final_status = {ev["edge"]: ev["label"] for ev in diag.get("evidence", []) if ev["edge"].startswith(("pre:", "par:"))}
    viz.draw_graph(sg, pos, f"Diagnosis: root cause {root.get('concept', 'none')} (thick black), concepts coloured by level, overall {diag.get('overall_level')}",
                   reached=set(levels), start=start, concept_labels={c: v.get("level") for c, v in levels.items()},
                   satellites=sats, cedge_status=final_status, kept={s[1] for s in sats}, root=root.get("concept"),
                   level_of={c: v.get("level") for c, v in levels.items()}); save(n)
    plt.show = _show

    # the report (every output) -> HTML with the figures embedded, full width
    md_path = steps_report.main(sid)
    text = md_path.read_text(encoding="utf-8")
    for f in figs:
        b64 = base64.b64encode(f.read_bytes()).decode("ascii")
        text = text.replace(str(f), f"\n\n![{f.name}](data:image/png;base64,{b64})\n\n")
    import markdown
    body = markdown.markdown(text, extensions=["tables", "fenced_code"])
    # the interactive graph
    try:
        from pyvis.network import Network
        net = Network(height="900px", width="100%", directed=True, cdn_resources="in_line", notebook=False)
        net.barnes_hut(gravity=-6000, spring_length=110)
        for c in sg["concepts"]:
            net.add_node(c["id"], label=c["id"], color="#9ecae1" if not c.get("generic") else "#deebf7", shape="ellipse", size=25)
        for m in sg["misconceptions"]:
            net.add_node(m["id"], label=m["id"], color="#f4a3a3" if m.get("kind") != "error" else "#f7c99b", shape="diamond", size=10,
                         title=f"wrong belief: {m.get('wrong_belief', '')}\nright rule: {m.get('correct_rule', '')}")
        for l in sg["levels"]:
            net.add_node(l["id"], label=l["id"], color="#c9b8e8", shape="box", size=8, title=f"{l.get('name', '')}\n{l.get('criterion', '')}")
        for e in sg["concept_edges"]:
            net.add_edge(e["source"], e["target"], label=e["type"], title=e.get("logic", ""), arrows="to" if e["type"] == "prerequisite" else "", dashes=e["type"] == "parallel", color="#444")
        for e in sg["mis_edges"]:
            net.add_edge(e["source"], e["target"], label=e["type"], title=f"wrong: {e.get('logic', '')}\nright: {e.get('twin_logic', '')}", color="#e08080")
        for e in sg["level_edges"]:
            net.add_edge(e["source"], e["target"], label=e["level"], title=e.get("logic", ""), color="#9a86c8")
        gpath = RESULTS_DIR / "viewer" / f"{sid}_G.html"
        gpath.write_text(net.generate_html(), encoding="utf-8")
        interactive = f'<h2>Interactive view of G (zoom, drag, hover an edge to read its rule)</h2><iframe src="{gpath.name}" style="width:100%;height:920px;border:1px solid #ccc"></iframe>'
    except Exception as exc:  # pragma: no cover
        interactive = f"<p>(interactive view skipped: {exc})</p>"
    body = body.replace("<h2>2. Clauses and start concepts", interactive + "\n<h2>2. Clauses and start concepts", 1)
    html = f"""<!doctype html><html><head><meta charset="utf-8"><title>Think on the Graph: {sid}</title>
<style>
body {{ font-family: Segoe UI, Arial, sans-serif; margin: 0; padding: 18px 28px; color: #222; background: #fff; }}
h1 {{ font-size: 26px; }} h2 {{ font-size: 22px; margin-top: 40px; border-bottom: 2px solid #ddd; padding-bottom: 4px; }} h3 {{ font-size: 19px; margin-top: 30px; }} h4 {{ font-size: 16px; margin-top: 22px; }}
img {{ width: 100%; height: auto; display: block; margin: 12px 0 24px; border: 1px solid #e5e5e5; }}
table {{ border-collapse: collapse; width: 100%; font-size: 13px; margin: 8px 0 16px; }} th, td {{ border: 1px solid #ddd; padding: 4px 8px; text-align: left; vertical-align: top; }} th {{ background: #f3f3f3; }}
pre {{ background: #f7f7f7; border: 1px solid #e3e3e3; padding: 10px; overflow-x: auto; font-size: 13px; }} code {{ font-size: 13px; }}
blockquote {{ border-left: 4px solid #ccc; margin: 6px 0; padding: 2px 12px; color: #444; }}
</style></head><body>{body}</body></html>"""
    out = RESULTS_DIR / "viewer" / f"{sid}_demo.html"
    out.write_text(html, encoding="utf-8")
    print("page:", out)
    if open_browser:
        webbrowser.open(out.resolve().as_uri())
    return out


def main(argv=None) -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--scenario", help="id in data/raw/scenarios_20.json")
    ap.add_argument("--input", help="JSON file with code, question, answer")
    ap.add_argument("--id", help="run id (default: next free MYnn)")
    ap.add_argument("--no-browser", action="store_true")
    a = ap.parse_args(argv)
    if a.scenario:
        sc = next(s for s in load_scenarios() if s["id"] == a.scenario)
    elif a.input:
        sc = json.loads(Path(a.input).read_text(encoding="utf-8"))
    else:
        sc = ask_inputs()
    run(a.id or next_id(), sc, open_browser=not a.no_browser)


if __name__ == "__main__":
    main()
