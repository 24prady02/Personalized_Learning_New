"""Drawing helpers for the walk figures (shared by the notebook and src/demo.py): concept layout, per-depth
graph pictures, the full-subgraph picture and the interactive pyvis view. Matplotlib + networkx."""
import os, re
from utils import RESULTS_DIR as _RESULTS_DIR
import utils
import math
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D
import networkx as nx
import pandas as pd
try:
    from IPython.display import display, Markdown, HTML
except Exception:  # no IPython: displays are no-ops
    display = lambda *a, **k: None
    Markdown = HTML = lambda x: x

FIG_W, FIG_H = 22, 13          # inches; every walk figure uses this size
LABEL_COLOUR = {"held": "#d62728", "correct": "#2ca02c", "broken": "#d62728", "confirmed": "#2ca02c",
                "shown": "#9467bd", "not applied": "#c7c7c7"}
LEVEL_COLOUR = {"L0": "#f4a3a3", "L1": "#f7c99b", "L2": "#f7e59b", "L3": "#bfe3b4", "L4": "#7fcf8f"}

# ---- reading the traversal log (its line formats are fixed by src/traverse.py)
R_DEPTH = re.compile(r"^--- depth (\d+): current concepts \[(.*)\]")
R_PRUNE = re.compile(r"^  (\S+) \(([^)]+)\): (\d+) candidates -> kept ?(.*)$")
R_LABEL = re.compile(r'^    (\S+) -> (.+?) \(([0-9.]+)\) "(.*)"$')
R_KEPT = re.compile(r"^  kept: (.*)$")
R_COVER = re.compile(r"^  clause coverage: (.*)$")
R_BRING = re.compile(r"^  uncovered clauses bring in: (.*)$")
R_PEND = re.compile(r"^  not yet read: (.*)$")

def parse_log(lines):
    steps, cur, concept = [], None, None
    for line in lines:
        m = R_DEPTH.match(line)
        if m:
            cur = {"depth": int(m.group(1)), "current": re.findall(r"'([^']+)'", m.group(2)), "prunes": [],
                   "labels": [], "kept": [], "coverage": {}, "brought": [], "pending": []}
            steps.append(cur); continue
        if cur is None:
            continue
        m = R_PRUNE.match(line)
        if m:
            concept = m.group(1)
            kept = re.findall(r"(\S+) \(([0-9.]+)\)", m.group(4))
            cur["prunes"].append({"concept": concept, "family": m.group(2), "candidates": int(m.group(3)),
                                  "kept": [(e, float(s)) for e, s in kept]}); continue
        m = R_LABEL.match(line)
        if m:
            cur["labels"].append({"concept": concept, "edge": m.group(1), "label": m.group(2),
                                  "score": float(m.group(3)), "clauses": m.group(4)}); continue
        m = R_KEPT.match(line)
        if m:
            cur["kept"] = re.findall(r"(\S+) \[", m.group(1)); continue
        m = R_COVER.match(line)
        if m:
            for part in m.group(1).split(";"):
                mm = re.match(r"\s*c(\d+) <- (\S+)", part)
                if mm:
                    cur["coverage"][int(mm.group(1))] = mm.group(2)
            continue
        m = R_BRING.match(line)
        if m:
            cur["brought"] = re.findall(r"(\S+) \(", m.group(1)); continue
        m = R_PEND.match(line)
        if m:
            cur["pending"] = [p.strip() for p in m.group(1).split(",")]
    return steps

# ---- edge ids
def edge_parts(eid):
    """(kind, source, target) for mis:/err:/pre:/par:/lvl: ids."""
    kind, body = eid.split(":", 1)
    if kind == "lvl":
        node, _ = body.split("#", 1)
        return kind, node.split("@")[0], node
    if kind == "par":
        a, b = body.split("~", 1)
        return kind, a, b
    a, b = body.split("->", 1)
    return kind, a, b

def short(text, n=34):
    return text if len(text) <= n else text[: n - 1] + "…"

# ---- layout: fixed concept positions for every figure of one run
def concept_layout(sg):
    """Concept positions, the same in every figure of one run. Each connected piece is laid out on its own and scaled so
    that no two concept nodes are closer than MIN_GAP; the pieces are placed side by side."""
    MIN_GAP = 2.6
    G = nx.Graph()
    G.add_nodes_from(c["id"] for c in sg["concepts"])
    G.add_edges_from((e["source"], e["target"]) for e in sg["concept_edges"])
    pos, x0 = {}, 0.0
    for comp in sorted(nx.connected_components(G), key=len, reverse=True):
        H = G.subgraph(comp)
        if len(H) == 1:
            p = {next(iter(H)): (0.0, 0.0)}
        elif len(H) == 2:
            a, b = sorted(H); p = {a: (0.0, 0.0), b: (1.0, 0.0)}
        else:
            p = nx.kamada_kawai_layout(H)
            p = nx.spring_layout(H, pos=p, seed=7, iterations=60, k=1.2 / math.sqrt(len(H)))
        pts = list(p.values())
        dmin = min((math.dist(a, b) for i, a in enumerate(pts) for b in pts[i + 1:]), default=1.0) or 1.0
        f = MIN_GAP / dmin
        xs = [v[0] for v in pts]
        for n, (x, y) in p.items():
            pos[n] = (x0 + (x - min(xs)) * f, y * f)
        x0 += (max(xs) - min(xs)) * f + 6.0
    return pos

def draw_graph(sg, pos, title, reached=(), start=(), concept_labels=None, satellites=None, cedge_status=None,
               kept=(), root=None, level_of=None, ax=None):
    """satellites: list of (concept, edge_id, text, label) drawn around the concept; cedge_status: edge id -> label."""
    concept_labels = concept_labels or {}
    satellites = satellites or []
    cedge_status = cedge_status or {}
    level_of = level_of or {}
    generic = {c["id"] for c in sg["concepts"] if c.get("generic")}
    fig = None
    if ax is None:
        fig, ax = plt.subplots(figsize=(FIG_W, FIG_H))
    # concept edges
    for e in sg["concept_edges"]:
        a, b = pos[e["source"]], pos[e["target"]]
        st = cedge_status.get(e["id"])
        col = LABEL_COLOUR.get(st, "#9a9a9a")
        lw = 3.2 if e["id"] in kept else (2.0 if st else 1.0)
        ls = "--" if e["type"] == "parallel" else "-"
        dx, dy = b[0] - a[0], b[1] - a[1]
        d = math.hypot(dx, dy) or 1.0
        a2 = (a[0] + dx / d * 0.58, a[1] + dy / d * 0.58)
        b2 = (b[0] - dx / d * 0.58, b[1] - dy / d * 0.58)
        if e["type"] == "prerequisite":
            ax.annotate("", xy=b2, xytext=a2, arrowprops=dict(arrowstyle="-|>", color=col, lw=lw, ls=ls,
                        shrinkA=0, shrinkB=0, mutation_scale=16), zorder=2)
        else:
            ax.plot([a2[0], b2[0]], [a2[1], b2[1]], color=col, lw=lw, ls=ls, zorder=2)
        lab = ("prerequisite" if e["type"] == "prerequisite" else "parallel") + (f" · {st}" if st else "")
        ax.text((a[0] + b[0]) / 2, (a[1] + b[1]) / 2, lab, fontsize=6.5, ha="center", va="center", color=col if st else "#555555",
                zorder=3, bbox=dict(boxstyle="round,pad=0.1", fc="white", ec="none", alpha=0.8))
    # satellites (misconception / level-way targets examined at this step)
    by_concept = {}
    for s in satellites:
        by_concept.setdefault(s[0], []).append(s)
    nbr = {}
    for e in sg["concept_edges"]:
        nbr.setdefault(e["source"], []).append(e["target"]); nbr.setdefault(e["target"], []).append(e["source"])
    def free_angles(c, k):
        """k directions around concept c, each as far as possible from its neighbours' directions and each other."""
        cx, cy = pos[c]
        taken = [math.atan2(pos[o][1] - cy, pos[o][0] - cx) for o in nbr.get(c, [])]
        # other concepts that sit close by also block directions
        taken += [math.atan2(p[1] - cy, p[0] - cx) for o, p in pos.items() if o != c and math.hypot(p[0] - cx, p[1] - cy) < 3.0]
        cands = [math.radians(a) for a in range(0, 360, 10)]
        out = []
        for _ in range(k):
            def gap(a):
                ds = [abs((a - t + math.pi) % (2 * math.pi) - math.pi) for t in taken + out]
                return min(ds) if ds else math.pi
            best = max(cands, key=gap)
            out.append(best)
        return out
    for c, items in by_concept.items():
        cx, cy = pos[c]
        angs = free_angles(c, len(items))
        for i, (_, eid, text, label) in enumerate(items):
            ang = angs[i]
            r = 1.6 + 0.35 * (i % 2)
            sx, sy = cx + r * math.cos(ang), cy + r * math.sin(ang)
            col = LABEL_COLOUR.get(label, "#c7c7c7")
            lw = 3.0 if eid in kept else 1.4
            ax.plot([cx, sx], [cy, sy], color=col, lw=lw, zorder=1)
            marker = "s" if eid.startswith("lvl:") else "D"
            ax.scatter([sx], [sy], s=170, marker=marker, color=col, edgecolor="black", linewidth=0.6, zorder=3)
            ax.text(sx, sy - 0.24, short(text), fontsize=7.5, ha="center", va="top", zorder=4,
                    bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.85))
    # concepts
    for c in sg["concepts"]:
        cid = c["id"]
        x, y = pos[cid]
        fc = LEVEL_COLOUR.get(level_of.get(cid), "#d6eaf8" if cid in reached else "#eeeeee")
        ec, lw = ("#1f77b4", 3.0) if cid in start else ("#555555", 1.0)
        if root and cid == root:
            ec, lw = ("black", 4.5)
        ls = "--" if cid in generic else "-"
        circ = mpatches.Circle((x, y), 0.55, fc=fc, ec=ec, lw=lw, ls=ls, zorder=5)
        ax.add_patch(circ)
        lab = cid.replace("_", "\n") if len(cid) > 12 else cid
        extra = concept_labels.get(cid)
        ax.text(x, y, lab, fontsize=7, ha="center", va="center", zorder=6, fontweight="bold" if cid in reached else None)
        if extra:
            ax.text(x, y + 0.68, extra, fontsize=8, ha="center", va="bottom", zorder=6, color="#333333")
    xs = [p[0] for p in pos.values()]; ys = [p[1] for p in pos.values()]
    ax.set_xlim(min(xs) - 2.6, max(xs) + 2.6); ax.set_ylim(min(ys) - 3.2, max(ys) + 2.6)
    ax.set_aspect("equal"); ax.axis("off"); ax.set_title(title, fontsize=13, loc="left")
    handles = [mpatches.Patch(color=LABEL_COLOUR["held"], label="held / broken"),
               mpatches.Patch(color=LABEL_COLOUR["correct"], label="correct / confirmed"),
               mpatches.Patch(color=LABEL_COLOUR["shown"], label="level way shown"),
               mpatches.Patch(color=LABEL_COLOUR["not applied"], label="not applied"),
               Line2D([0], [0], marker="D", color="w", markerfacecolor="#999", label="misconception / error", markersize=8),
               Line2D([0], [0], marker="s", color="w", markerfacecolor="#999", label="level way", markersize=8),
               Line2D([0], [0], color="#9a9a9a", lw=1, label="prerequisite (arrow)"),
               Line2D([0], [0], color="#9a9a9a", lw=1, ls="--", label="parallel"),
               mpatches.Circle((0, 0), 1, fc="white", ec="#1f77b4", lw=2.5, label="start concept")]
    ax.legend(handles=handles, loc="lower left", fontsize=8, ncol=3, frameon=False)
    if fig is not None:
        plt.tight_layout(); plt.show()

def satellite_text(g, eid):
    kind, src, tgt = edge_parts(eid)
    if kind == "lvl":
        e = g.edge_by_id.get(eid, {})
        return f"{e.get('level', tgt.split('@')[-1])} {(e.get('way') or '').replace('_', ' ')}"
    return tgt

# ---- the whole subgraph G: concept nodes and edges, misconception / error nodes and edges, level nodes and edges
def draw_full_G(sg, pos, title):
    """Static picture of all of G: every concept with its misconception / error nodes (diamonds) and its five level
    nodes L0-L4 (squares) around it, every edge labelled with its type."""
    n_sat = max([len([e for e in sg["mis_edges"] if e["source"] == c["id"]]) + 5 for c in sg["concepts"]] + [5])
    R = 1.9 + 0.045 * n_sat
    f = (2 * R + 2.2) / 2.6                     # concepts at least two ring radii (+ room for labels) apart
    bigpos = {k: (x * f, y * f) for k, (x, y) in pos.items()}
    xs0 = [p[0] for p in bigpos.values()]; ys0 = [p[1] for p in bigpos.values()]
    wspan, hspan = max(xs0) - min(xs0) + 2 * R + 5, max(ys0) - min(ys0) + 2 * R + 3
    scale = min(1.0, 70 / max(wspan, 1))
    fig, ax = plt.subplots(figsize=(max(FIG_W, wspan * 0.55 * scale), max(FIG_H * 0.6, hspan * 0.55 * scale)))
    for e in sg["concept_edges"]:
        a, b = bigpos[e["source"]], bigpos[e["target"]]
        dx, dy = b[0] - a[0], b[1] - a[1]; d = math.hypot(dx, dy) or 1.0
        a2 = (a[0] + dx / d * 0.6, a[1] + dy / d * 0.6); b2 = (b[0] - dx / d * 0.6, b[1] - dy / d * 0.6)
        if e["type"] == "prerequisite":
            ax.annotate("", xy=b2, xytext=a2, arrowprops=dict(arrowstyle="-|>", color="#555", lw=1.4, mutation_scale=15), zorder=2)
        else:
            ax.plot([a2[0], b2[0]], [a2[1], b2[1]], color="#555", lw=1.4, ls="--", zorder=2)
        ax.text((a[0] + b[0]) / 2, (a[1] + b[1]) / 2, e["type"], fontsize=7, ha="center", va="center", zorder=3,
                bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none", alpha=0.85))
    for c in sg["concepts"]:
        cid = c["id"]; cx, cy = bigpos[cid]
        sats = [(e["target"], "err" if e["type"] == "error" else "mis") for e in sg["mis_edges"] if e["source"] == cid]
        sats += [(f"L{k}", "lvl") for k in range(5)]
        # directions toward linked concepts stay free, so no node sits on a concept edge or its label
        towards = [math.atan2(bigpos[o][1] - cy, bigpos[o][0] - cx) for e in sg["concept_edges"]
                   for o in ([e["target"]] if e["source"] == cid else [e["source"]] if e["target"] == cid else [])]
        allowed = [math.radians(a) for a in range(0, 360)
                   if all(abs((math.radians(a) - t + math.pi) % (2 * math.pi) - math.pi) > math.radians(28) for t in towards)]
        allowed = allowed or [math.radians(a) for a in range(0, 360)]
        angs = [allowed[int(i * len(allowed) / len(sats))] for i in range(len(sats))]
        for i, (name, kind) in enumerate(sats):
            ang = angs[i]
            sx, sy = cx + R * math.cos(ang), cy + R * math.sin(ang)
            col = {"mis": "#e8a0a0", "err": "#f2c48d", "lvl": "#c9b8e8"}[kind]
            ax.plot([cx, sx], [cy, sy], color=col, lw=0.8, zorder=1)
            ax.scatter([sx], [sy], s=55, marker="s" if kind == "lvl" else "D", color=col, edgecolor="#666", linewidth=0.4, zorder=3)
            ax.text(sx + 0.12 * math.cos(ang), sy + 0.12 * math.sin(ang), short(name, 26), fontsize=5.5,
                    ha="left" if math.cos(ang) >= 0 else "right", va="center", zorder=4)
        ax.add_patch(mpatches.Circle((cx, cy), 0.6, fc="#d6eaf8", ec="#1f4e79", lw=1.5, ls="--" if c.get("generic") else "-", zorder=5))
        ax.text(cx, cy, cid.replace("_", "\n"), fontsize=7, ha="center", va="center", zorder=6, fontweight="bold")
    xs = [p[0] for p in bigpos.values()]; ys = [p[1] for p in bigpos.values()]
    ax.set_xlim(min(xs) - R - 2.5, max(xs) + R + 2.5); ax.set_ylim(min(ys) - R - 1.5, max(ys) + R + 1.5)
    ax.set_aspect("equal"); ax.axis("off"); ax.set_title(title, fontsize=13, loc="left")
    ax.legend(handles=[mpatches.Patch(color="#d6eaf8", label="concept (dashed = generic)"),
                       Line2D([0], [0], marker="D", color="w", markerfacecolor="#e8a0a0", markersize=8, label="misconception"),
                       Line2D([0], [0], marker="D", color="w", markerfacecolor="#f2c48d", markersize=8, label="error"),
                       Line2D([0], [0], marker="s", color="w", markerfacecolor="#c9b8e8", markersize=8, label="level node L0-L4"),
                       Line2D([0], [0], color="#555", lw=1.4, label="prerequisite (arrow)"),
                       Line2D([0], [0], color="#555", lw=1.4, ls="--", label="parallel")],
              loc="lower left", fontsize=8, ncol=3, frameon=False)
    plt.tight_layout(); plt.show()

def show_full_G_interactive(sg, path=None):
    """The same G as an interactive graph (zoom, drag, hover an edge to read its rule)."""
    path = path or str(utils.RESULTS_DIR / "G.html")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    try:
        from pyvis.network import Network
    except Exception:
        print("(pyvis not installed: interactive view skipped)"); return
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
        net.add_edge(e["source"], e["target"], label=e["type"], title=e.get("logic", ""), arrows="to" if e["type"] == "prerequisite" else "",
                     dashes=e["type"] == "parallel", color="#444")
    for e in sg["mis_edges"]:
        net.add_edge(e["source"], e["target"], label=e["type"], title=f"wrong: {e.get('logic', '')}\nright: {e.get('twin_logic', '')}", color="#e08080")
    for e in sg["level_edges"]:
        net.add_edge(e["source"], e["target"], label=e["level"], title=e.get("logic", ""), color="#9a86c8")
    html = net.generate_html()                       # written as UTF-8 ourselves: pyvis would use the Windows code page
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(html)
    display(HTML(html))
