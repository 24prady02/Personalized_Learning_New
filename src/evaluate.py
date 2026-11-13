"""Evaluate Stage 1 on the scenarios and write every output.

For each scenario the code (and only the code) is run through the model and the subgraph is taken out. Then:

* data/processed/<sid>_subgraph.json      the extracted subgraph
* experiments/logs/subgraph_report.txt     one line per scenario + "fully covered: N / 10" (coverage of the gold
                                           concepts; gold is used here for checking only, never in the outputs)
* results/metrics.json                     coverage and size metrics
* results/figures/<sid>.png                node visualization of each subgraph
* results/tables/summary.csv               one row per scenario (counts, concept ids, edges traced, misconception ids)
* results/results.md                       summary table, then per scenario: code, figure, nodes, edges with logic, misconceptions, levels

    python src/evaluate.py                       # everything, on data/raw/scenarios_40.json
    python src/evaluate.py --no-figures          # report and JSON only (no matplotlib / networkx needed)
    python src/evaluate.py --scenarios data/raw/scenarios_not_from_code.json --no-figures --no-json
"""
from __future__ import annotations

import argparse
import csv
import json
import math
from collections import Counter
from pathlib import Path
from typing import Any

from model import subgraph_from_code
from utils import (KG_PATH, LOGS_DIR, NOT_IN_CODE, PROCESSED_DIR, RESULTS_DIR, SCENARIOS_PATH, gold_concepts, load_config,
                   load_kg, load_scenarios)


# ------------------------------------------------------------------ coverage report

def run(kg: dict[str, Any], scenarios: list[dict], out_dir: Path | None = None, hops: int = 0, keep_generic: bool = False) -> dict:
    """Extract every scenario's subgraph; compare the concept nodes with the gold concepts (check only)."""
    generic = {c["id"] for c in kg["concepts"] if (c.get("reader") or {}).get("generic")}
    lines, results, sizes = [], {}, []
    covered = 0
    fire: Counter = Counter()
    for sc in scenarios:
        sid = sc["id"]
        is_ref = bool(sc.get("reference_case"))
        sg = subgraph_from_code(sc["code"], kg, sid, hops, keep_generic)
        got = {c["id"] for c in sg["concepts"]}
        tagged = {c["id"] for c in sg["concepts"] if c["why"] == "code"}
        if not is_ref:
            fire.update(t for t in tagged if t not in generic)
            sizes.append(len(got))
        need = gold_concepts(sc)
        missed = sorted(need - got)
        unexpected = sorted(set(missed) - NOT_IN_CODE.get(sid, set()))
        if not missed and not is_ref:
            covered += 1
        c = sg["counts"]
        tag = "ref" if is_ref else ("ok" if not missed else ("xfail" if not unexpected else "MISS"))
        lines.append(f"{sid:5} tagged {c['tagged']:3}  nodes {c['concepts']:3} ({c['generic']} generic kept)  edges {c['concept_edges']:3}  mis {c['mis_edges']:3}  "
                     f"levels {c['levels']:3}  links {c['level_mis_links']:3}  pieces {c['components']}  {tag:5} missed: {', '.join(missed) or '-'}")
        results[sid] = {"subgraph": sg, "missed": missed, "unexpected_miss": unexpected, "gold_size": len(need)}
        if out_dir:
            out_dir.mkdir(parents=True, exist_ok=True)
            (out_dir / f"{sid}_subgraph.json").write_text(json.dumps(sg, indent=1, ensure_ascii=False), encoding="utf-8")
    n = len(sizes)
    lines.append(f"fully covered: {covered} / {n}   (mean concepts per subgraph: {sum(sizes) / max(1, n):.1f}; S000 is the reference case, not counted)")
    broad = [(cid, k) for cid, k in fire.most_common() if k >= 12]
    lines.append("non-generic concepts firing in >= 12 scenarios: " + (", ".join(f"{c} ({k})" for c, k in broad) or "none"))
    return {"lines": lines, "covered": covered, "n": n, "results": results, "fire": fire}


def metrics(rep: dict) -> dict[str, Any]:
    scored = {sid: r for sid, r in rep["results"].items() if sid != "S000"}
    recall = [1 - len(r["missed"]) / r["gold_size"] for r in scored.values() if r["gold_size"]]
    precision = [r["gold_size"] / r["subgraph"]["counts"]["concepts"] for r in scored.values() if r["subgraph"]["counts"]["concepts"]]
    return {
        "scenarios": rep["n"], "fully_covered": rep["covered"],
        "gold_concept_recall_mean": round(sum(recall) / max(1, len(recall)), 3),
        "gold_share_of_nodes_mean": round(sum(precision) / max(1, len(precision)), 3),
        "mean_concept_nodes": round(sum(r["subgraph"]["counts"]["concepts"] for r in scored.values()) / max(1, len(scored)), 2),
        "mean_concept_edges": round(sum(r["subgraph"]["counts"]["concept_edges"] for r in scored.values()) / max(1, len(scored)), 2),
        "subgraphs_in_one_piece": sum(1 for r in rep["results"].values() if r["subgraph"]["counts"]["components"] == 1),
        "per_scenario": {sid: {"nodes": r["subgraph"]["counts"]["concepts"], "missed": r["missed"], "pieces": r["subgraph"]["counts"]["components"]}
                         for sid, r in rep["results"].items()},
    }


# ------------------------------------------------------------------ figures and listing

CONCEPT, GENERIC, MIS, ERR, LEVEL = "#2b6cb0", "#90b4e0", "#c53030", "#dd6b20", "#718096"


def _layout(g) -> dict:
    """Layout per connected piece, pieces packed left to right."""
    import networkx as nx
    pos: dict = {}
    x_off = 0.0
    for comp in sorted(nx.connected_components(g), key=lambda c: (-len(c), sorted(c)[0])):
        sub = g.subgraph(comp)
        n = len(comp)
        if n == 1:
            local = {next(iter(comp)): (0.0, 0.0)}
        else:
            local = nx.kamada_kawai_layout(sub) if n <= 40 else nx.spring_layout(sub, seed=7, iterations=300)
        span = 1.9 * math.sqrt(n) + 0.8
        xs = [v[0] for v in local.values()]; ys = [v[1] for v in local.values()]
        w = (max(xs) - min(xs)) or 1.0; h = (max(ys) - min(ys)) or 1.0
        for k, (x, y) in local.items():
            pos[k] = (x_off + (x - min(xs)) / w * span, (y - min(ys)) / h * span)
        x_off += span + 2.6
    return pos


def draw(sg: dict, out: Path, title: str) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import networkx as nx
    import textwrap

    concepts = [c["id"] for c in sg["concepts"]]
    generic = {c["id"] for c in sg["concepts"] if c.get("generic")}
    g = nx.Graph()
    g.add_nodes_from(concepts)
    for e in sg["concept_edges"]:
        g.add_edge(e["source"], e["target"])
    pos = _layout(g)
    mis_kind = {m["id"]: m["kind"] for m in sg["misconceptions"]}
    sat = {c: [] for c in concepts}
    for e in sg["mis_edges"]:
        sat[e["source"]].append(e["target"])

    xs = [v[0] for v in pos.values()]; ys = [v[1] for v in pos.values()]
    width = max(xs) - min(xs) + 3.0; height = max(ys) - min(ys) + 3.2
    fig_w = max(11.0, 1.15 * width + 5.5); fig_h = max(7.0, 1.15 * height + 1.5)
    fig = plt.figure(figsize=(fig_w, fig_h))
    ax = fig.add_axes([0.02, 0.10, 0.66, 0.80])
    for e in sg["concept_edges"]:
        (x1, y1), (x2, y2) = pos[e["source"]], pos[e["target"]]
        pre = e["type"] == "prerequisite"
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="-|>" if pre else "-", linestyle="-" if pre else "--", color="#4a5568", lw=1.5, shrinkA=16, shrinkB=16))
    for c in concepts:
        x, y = pos[c]
        for i in range(5):
            lx = x - 0.40 + 0.20 * i
            ax.plot([x, lx], [y - 0.10, y - 0.34], color=LEVEL, lw=0.6, alpha=0.7, zorder=0)
            ax.add_patch(plt.Rectangle((lx - 0.075, y - 0.50), 0.15, 0.15, color=LEVEL, lw=0))
            ax.text(lx, y - 0.425, f"L{i}", ha="center", va="center", fontsize=5.2, color="white")
        k = len(sat[c])
        for j, m in enumerate(sat[c]):
            ang = math.pi * (0.1 + 0.8 * (j + 0.5) / max(k, 1))
            r = 0.55 + 0.22 * (j % 2) + 0.012 * k
            mx, my = x + r * math.cos(ang), y + r * math.sin(ang)
            col = ERR if mis_kind.get(m) == "error" else MIS
            ax.plot([x, mx], [y, my], color=col, lw=0.5, alpha=0.45, zorder=0)
            ax.scatter([mx], [my], s=16, color=col, zorder=3)
        ax.scatter([x], [y], s=420, color=GENERIC if c in generic else CONCEPT, zorder=4, edgecolors="white", linewidths=1.2)
        ax.text(x, y - 0.66, c, ha="center", va="top", fontsize=7.5, color="#1a202c", zorder=5, fontweight="bold")
    ax.set_xlim(min(xs) - 1.5, max(xs) + 1.5); ax.set_ylim(min(ys) - 1.7, max(ys) + 1.5)
    ax.set_aspect("equal"); ax.axis("off")
    cnt = sg["counts"]
    fig.suptitle(f"{title}\n{cnt['concepts']} concept nodes ({cnt['generic']} generic kept), {cnt['concept_edges']} concept edges, "
                 f"{cnt['mis_edges']} misconception/error edges to {cnt['misconceptions']} nodes, {cnt['levels']} level nodes, "
                 f"{cnt['components']} connected piece(s)", fontsize=10, y=0.985)
    handles = [plt.Line2D([], [], marker="o", color=CONCEPT, ls="", ms=9, label="concept (found by its code pattern)"),
               plt.Line2D([], [], marker="o", color=GENERIC, ls="", ms=9, label="generic concept kept (edge to a specific one)"),
               plt.Line2D([], [], color="#4a5568", lw=1.5, label="prerequisite (arrow) / parallel (dashed)"),
               plt.Line2D([], [], marker="o", color=MIS, ls="", ms=5, label="misconception node + edge"),
               plt.Line2D([], [], marker="o", color=ERR, ls="", ms=5, label="error node + edge"),
               plt.Line2D([], [], marker="s", color=LEVEL, ls="", ms=6, label="level nodes L0..L4 + has_level edges")]
    ax.legend(handles=handles, loc="upper left", bbox_to_anchor=(0.0, -0.02), fontsize=7, frameon=False, ncol=3)
    panel = fig.add_axes([0.69, 0.10, 0.30, 0.80]); panel.axis("off")
    lines = ["Misconception and error nodes per concept"]
    for c in concepts:
        names = sat[c]
        if not names:
            lines.append(f"{c}: none"); continue
        shown = ", ".join(names[:6]) + (f", ... (+{len(names) - 6})" if len(names) > 6 else "")
        lines.append(f"{c} ({len(names)}): {shown}")
    wrapped = []
    for ln in lines:
        wrapped += textwrap.wrap(ln, 62, subsequent_indent="    ") or [""]
    size = 7 if len(wrapped) <= 60 else 5.5
    panel.text(0, 1, "\n".join(wrapped[:110] + (["..."] if len(wrapped) > 110 else [])), va="top", ha="left", fontsize=size, family="monospace", transform=panel.transAxes)
    fig.savefig(out, dpi=150)
    plt.close(fig)


def write_results(rep: dict, scenarios: list[dict], out: Path, figures: bool = True) -> None:
    (out / "figures").mkdir(parents=True, exist_ok=True)
    (out / "tables").mkdir(parents=True, exist_ok=True)
    rows, md = [], []
    md.append("# Results: code-only subgraph for each scenario\n")
    md.append("Stage 1 reads only the scenario's code. Every concept node below was found by a regex stored on that concept node of the "
              "knowledge graph; the subgraph is then the knowledge graph's edges between those concepts, their misconception and error nodes "
              "and edges, and their level nodes L0..L4 with the has_level edges. Figures: `figures/<sid>.png`.\n")
    for sc in scenarios:
        sid = sc["id"]
        sg = rep["results"][sid]["subgraph"]
        if figures:
            draw(sg, out / "figures" / f"{sid}.png", f"{sid}: subgraph from the code alone")
        c = sg["counts"]
        edge_ids = [e["id"] for e in sg["concept_edges"]]
        mis_ids = [m["id"] for m in sg["misconceptions"]]
        rows.append({"scenario": sid, "concept_nodes": c["concepts"], "generic_kept": c["generic"], "concept_edges": c["concept_edges"],
                     "misconception_edges": c["mis_edges"], "misconception_nodes": c["misconceptions"], "level_nodes": c["levels"],
                     "level_edges": c["level_edges"], "level_mis_links": c["level_mis_links"], "connected_pieces": c["components"],
                     "concept_node_ids": " ".join(x["id"] for x in sg["concepts"]),
                     "edges_traced": " ".join(edge_ids), "misconception_node_ids": " ".join(mis_ids)})
        md.append(f"\n## {sid}\n")
        md.append("```java\n" + sc["code"] + "\n```\n")
        md.append(f"![{sid}](figures/{sid}.png)\n")
        md.append(f"**Concept nodes ({c['concepts']})**: " + ", ".join(
            f"`{x['id']}`" + (" (generic)" if x.get("generic") else "") for x in sg["concepts"]) + "\n")
        md.append(f"\n**Concept edges traced ({c['concept_edges']})**\n\n| edge | logic |\n|---|---|")
        for e in sg["concept_edges"]:
            md.append(f"| `{e['id']}` | {(e['logic'] or '').replace('|', '/')} |")
        md.append(f"\n**Misconception and error nodes ({c['misconceptions']}) via {c['mis_edges']} edges**: " + ", ".join(f"`{m}`" for m in mis_ids) + "\n")
        md.append(f"**Level nodes**: {c['levels']} (L0..L4 for each concept), **has_level edges**: {c['level_edges']}, "
                  f"**level→misconception links**: {c['level_mis_links']}, **connected pieces**: {c['components']}\n")
        if sg["warnings"]:
            md.append("Notes: " + "; ".join(sg["warnings"]) + "\n")
    with open(out / "tables" / "summary.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)
    summary = ["\n## Summary\n",
               "| scenario | concept nodes | concept edges | misconception edges | misconception nodes | level nodes | pieces | edges traced | misconception nodes |",
               "|---|---|---|---|---|---|---|---|---|"]
    for r in rows:
        summary.append(f"| {r['scenario']} | {r['concept_nodes']} | {r['concept_edges']} | {r['misconception_edges']} | {r['misconception_nodes']} | "
                       f"{r['level_nodes']} | {r['connected_pieces']} | " + (", ".join(f"`{x}`" for x in r["edges_traced"].split()) or "-") + " | "
                       + ", ".join(f"`{x}`" for x in r["misconception_node_ids"].split()) + " |")
    md = md[:2] + summary + md[2:]
    (out / "results.md").write_text("\n".join(md), encoding="utf-8")


# ------------------------------------------------------------------ CLI

def main(argv=None) -> None:
    cfg = load_config()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--kg", default=cfg.get("kg", str(KG_PATH)))
    ap.add_argument("--scenarios", default=cfg.get("scenarios", str(SCENARIOS_PATH)))
    ap.add_argument("--hops", type=int, default=cfg.get("hops", 0), help="0: nodes are exactly the tagged concepts; 1: add one prerequisite hop")
    ap.add_argument("--keep-generic", action="store_true", default=cfg.get("keep_generic", False),
                    help="keep every tagged generic concept (default: keep one only when an edge ties it to a specific tagged concept or its decisive signal fired)")
    ap.add_argument("--processed", default=str(PROCESSED_DIR), help="where the per-scenario subgraph JSON goes")
    ap.add_argument("--results", default=str(RESULTS_DIR))
    ap.add_argument("--log", default=None, help="report log file (default experiments/logs/subgraph_report[_<suffix>].txt)")
    ap.add_argument("--no-json", action="store_true")
    ap.add_argument("--no-figures", action="store_true", help="skip the PNG figures (and the results listing)")
    a = ap.parse_args(argv)

    kg = load_kg(a.kg)
    scenarios = load_scenarios(a.scenarios)
    rep = run(kg, scenarios, None if a.no_json else Path(a.processed), hops=a.hops, keep_generic=a.keep_generic)
    print("\n".join(rep["lines"]))

    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    suffix = "" if Path(a.scenarios).name == SCENARIOS_PATH.name else "_" + Path(a.scenarios).stem.replace("scenarios_", "")
    log = Path(a.log) if a.log else LOGS_DIR / f"subgraph_report{suffix}.txt"
    log.write_text("\n".join(rep["lines"]) + "\n", encoding="utf-8")
    print(f"wrote {log}")

    if not a.no_figures:
        out = Path(a.results)
        write_results(rep, scenarios, out, figures=True)
        (out / "metrics.json").write_text(json.dumps(metrics(rep), indent=1), encoding="utf-8")
        print(f"wrote {out / 'figures'}, {out / 'tables' / 'summary.csv'}, {out / 'results.md'}, {out / 'metrics.json'}")


if __name__ == "__main__":
    main()
