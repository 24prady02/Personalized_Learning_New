"""Results: one figure per scenario (concept nodes and edges, misconception nodes, level nodes) and a listing.

    PYTHONPATH=src python -m lp_graph.subgraph.results [--kg ...] [--gold ...] [--out results]

Writes results/figures/<sid>.png, results/tables/summary.csv and results/results.md.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import networkx as nx  # noqa: E402

from .extract import subgraph_from_code  # noqa: E402
from .report import load_gold  # noqa: E402

CONCEPT, GENERIC, MIS, ERR, LEVEL = "#2b6cb0", "#90b4e0", "#c53030", "#dd6b20", "#718096"


def _layout(g: nx.Graph) -> dict:
    """Spring layout per connected piece, pieces packed left to right so no space is wasted."""
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
    fig.suptitle(f"{title}" + chr(10) + f"{cnt['concepts']} concept nodes ({cnt['generic']} generic kept), {cnt['concept_edges']} concept edges, "
                 f"{cnt['mis_edges']} misconception/error edges to {cnt['misconceptions']} nodes, {cnt['levels']} level nodes, "
                 f"{cnt['components']} connected piece(s)", fontsize=10, y=0.985)
    handles = [plt.Line2D([], [], marker="o", color=CONCEPT, ls="", ms=9, label="concept (found by its code pattern)"),
               plt.Line2D([], [], marker="o", color=GENERIC, ls="", ms=9, label="generic concept kept (edge to a specific one)"),
               plt.Line2D([], [], color="#4a5568", lw=1.5, label="prerequisite (arrow) / parallel (dashed)"),
               plt.Line2D([], [], marker="o", color=MIS, ls="", ms=5, label="misconception node + edge"),
               plt.Line2D([], [], marker="o", color=ERR, ls="", ms=5, label="error node + edge"),
               plt.Line2D([], [], marker="s", color=LEVEL, ls="", ms=6, label="level nodes L0..L4 + has_level edges")]
    ax.legend(handles=handles, loc="upper left", bbox_to_anchor=(0.0, -0.02), fontsize=7, frameon=False, ncol=3)
    # text panel: misconception / error nodes per concept
    panel = fig.add_axes([0.69, 0.10, 0.30, 0.80]); panel.axis("off")
    lines = ["Misconception and error nodes per concept"]
    for c in concepts:
        names = sat[c]
        if not names:
            lines.append(f"{c}: none"); continue
        shown = ", ".join(names[:6]) + (f", ... (+{len(names) - 6})" if len(names) > 6 else "")
        lines.append(f"{c} ({len(names)}): {shown}")
    import textwrap
    wrapped = []
    for ln in lines:
        wrapped += textwrap.wrap(ln, 62, subsequent_indent="    ") or [""]
    size = 7 if len(wrapped) <= 60 else 5.5
    panel.text(0, 1, chr(10).join(wrapped[:110] + (["..."] if len(wrapped) > 110 else [])), va="top", ha="left", fontsize=size, family="monospace", transform=panel.transAxes)
    fig.savefig(out, dpi=150)
    plt.close(fig)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--kg", default="data/raw/chapter1_kg.json")
    ap.add_argument("--gold", default="data/raw/scenarios_20.json")
    ap.add_argument("--out", default="results")
    a = ap.parse_args(argv)
    kg = json.loads(Path(a.kg).read_text(encoding="utf-8"))
    out = Path(a.out)
    (out / "figures").mkdir(parents=True, exist_ok=True)
    (out / "tables").mkdir(parents=True, exist_ok=True)
    rows, md = [], []
    md.append("# Results: code-only subgraph for each scenario\n")
    md.append("Stage 1 reads only the scenario's code. Every concept node below was found by a regex stored on that concept node of the "
              "knowledge graph; the subgraph is then the knowledge graph's edges between those concepts, their misconception and error nodes "
              "and edges, and their level nodes L0..L4 with the has_level edges. Figures: `figures/<sid>.png`.\n")
    for sc in load_gold(Path(a.gold)):
        sid = sc["id"]
        sg = subgraph_from_code(sc["code"], kg, sid)
        draw(sg, out / "figures" / f"{sid}.png", f"{sid}: subgraph from the code alone")
        c = sg["counts"]
        g = sc.get("gold", {})
        gold = sorted(set(g.get("levels", {})) | {x for e in g.get("edges", []) for x in e["id"].split(":", 1)[1].replace("~", "->").split("->")})
        nodes = {x["id"] for x in sg["concepts"]}
        rows.append({"scenario": sid, "concept_nodes": c["concepts"], "generic_kept": c["generic"], "concept_edges": c["concept_edges"],
                     "misconception_edges": c["mis_edges"], "misconception_nodes": c["misconceptions"], "level_nodes": c["levels"],
                     "level_edges": c["level_edges"], "level_mis_links": c["level_mis_links"], "components": c["components"],
                     "gold_concepts": " ".join(gold), "gold_covered": "yes" if set(gold) <= nodes else "no"})
        md.append(f"\n## {sid}\n")
        md.append("```java\n" + sc["code"] + "\n```\n")
        md.append(f"![{sid}](figures/{sid}.png)\n")
        md.append(f"**Concept nodes ({c['concepts']})**: " + ", ".join(
            f"`{x['id']}`" + (" (generic)" if x.get("generic") else "") for x in sg["concepts"]) + "\n")
        if gold:
            md.append(f"**Gold concepts**: {', '.join(f'`{x}`' for x in gold)} — " + ("all in the subgraph" if set(gold) <= nodes else f"missing {sorted(set(gold) - nodes)}") + "\n")
        md.append(f"\n**Concept edges ({c['concept_edges']})**\n\n| edge | logic |\n|---|---|")
        for e in sg["concept_edges"]:
            md.append(f"| `{e['id']}` | {(e['logic'] or '').replace('|', '/')} |")
        md.append(f"\n**Misconception and error nodes ({c['misconceptions']}) via {c['mis_edges']} edges**: " + ", ".join(
            f"`{m['id']}`" for m in sg["misconceptions"]) + "\n")
        md.append(f"**Level nodes**: {c['levels']} (L0..L4 for each concept), **has_level edges**: {c['level_edges']}, "
                  f"**level→misconception links**: {c['level_mis_links']}, **connected pieces**: {c['components']}\n")
        if sg["warnings"]:
            md.append("Notes: " + "; ".join(sg["warnings"]) + "\n")
    with open(out / "tables" / "summary.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)
    summary = ["\n## Summary\n", "| scenario | concept nodes | generic kept | concept edges | misconception edges | misconception nodes | level nodes | links | pieces | gold covered |", "|---|---|---|---|---|---|---|---|---|---|"]
    summary += [f"| {r['scenario']} | {r['concept_nodes']} | {r['generic_kept']} | {r['concept_edges']} | {r['misconception_edges']} | {r['misconception_nodes']} | {r['level_nodes']} | {r['level_mis_links']} | {r['components']} | {r['gold_covered']} |" for r in rows]
    md = md[:2] + summary + md[2:]
    (out / "results.md").write_text("\n".join(md), encoding="utf-8")
    print(f"wrote {len(rows)} figures, {out / 'tables' / 'summary.csv'}, {out / 'results.md'}")


if __name__ == "__main__":
    main()
