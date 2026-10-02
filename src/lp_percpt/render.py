"""
render.py — draw a student's concept map from their student graph.

Self-contained HTML with inline SVG: chapters as columns, prerequisite edges
as arrows (gaps in red), each concept coloured by the level node it has
reached on its L0-L4 ladder. Inferred levels are pale, provisional levels
have a dashed border, frontier concepts are dashed outlines, and concepts at
risk from a held misconception have a red outline.
"""
from __future__ import annotations

import html
from pathlib import Path
from typing import Dict, List, Tuple

from .ladder import LEVELS

COLOURS = {"L0": "#9e9e9e", "L1": "#d9534f", "L2": "#f0ad4e", "L3": "#5bc0de", "L4": "#5cb85c"}
COL_W, ROW_H, NODE_W, NODE_H, TOP = 190, 46, 160, 32, 70


def _layout(kg) -> Dict[str, Tuple[float, float]]:
    pos = {}
    for col, ch in enumerate(kg.chapters):
        members = [cid for cid, c in kg.concepts.items() if c.chapter == ch]
        for row, cid in enumerate(members):
            pos[cid] = (20 + col * COL_W, TOP + row * ROW_H)
    return pos


def render_html(g) -> str:
    kg = g.kg
    pos = _layout(kg)
    width = 40 + len(kg.chapters) * COL_W
    height = TOP + 20 + ROW_H * max(sum(1 for c in kg.concepts.values() if c.chapter == ch) for ch in kg.chapters)
    gaps = {tuple(x) for x in g.gaps}
    nodes = g.nodes
    svg: List[str] = []

    for col, (ch, info) in enumerate(kg.chapters.items()):
        svg.append(f'<text x="{20 + col * COL_W + NODE_W / 2}" y="40" class="ch">'
                   f'{html.escape(info.get("section", ""))} {html.escape(info.get("label", ch))}</text>')

    for dst, c in kg.concepts.items():
        for src in sorted(c.prerequisites):
            (x1, y1), (x2, y2) = pos[src], pos[dst]
            x1 += NODE_W; y1 += NODE_H / 2; y2 += NODE_H / 2
            if x2 < x1:
                x1 = x2 + NODE_W; x2 = x1
            mid = (x1 + x2) / 2 + (25 if x1 == x2 else 0)
            touched = src in nodes and dst in nodes and (nodes[src].observed or nodes[dst].observed)
            cls = "edge gap" if (src, dst) in gaps else ("edge hot" if touched else "edge")
            marker = "arrgap" if (src, dst) in gaps else "arr"
            svg.append(f'<path class="{cls}" d="M{x1},{y1} C{mid},{y1} {mid},{y2} {x2},{y2}" marker-end="url(#{marker})"/>')

    for cid, (x, y) in pos.items():
        c = kg.concepts[cid]
        label = html.escape(c.label)
        n = nodes.get(cid)
        tip = [c.label]
        if n is not None and n.observed:
            lv = LEVELS[n.level]
            fill, cls, tag = COLOURS[lv], "obs" + (" prov" if n.provisional else ""), lv + ("?" if n.provisional else "")
            tip.append(f"{lv} {kg.level_names.get(lv, '')}" + (" (provisional)" if n.provisional else ""))
            tip.append(n.stop_reason)
            if n.held:
                tip.append("held: " + ", ".join(sorted(n.held)))
        elif n is not None and n.inferred_level:
            lv = LEVELS[n.inferred_level]
            fill, cls, tag = COLOURS[lv], "inf", lv + " inf"
            tip.append(f"{lv} inferred from a concept that builds on it")
        elif n is not None and n.frontier:
            fill, cls, tag = None, "front", ""
            tip.append("not yet assessed")
        else:
            fill, cls, tag = None, "idle", ""
        if n is not None and n.at_risk:
            cls += " risk"
            tip.append("at risk: " + ", ".join(n.at_risk))
        style = f' style="fill:{fill}"' if fill else ""
        flags = ""
        if n is not None and n.observed:
            flags = ("!" if n.held else "") + ("=" if n.plateau else "") + ("~" if n.stale else "")
        svg.append(f'<g><title>{html.escape(" | ".join(t for t in tip if t))}</title>'
                   f'<rect x="{x}" y="{y}" width="{NODE_W}" height="{NODE_H}" rx="6" class="{cls}"{style}/>'
                   f'<text x="{x + 8}" y="{y + 21}" class="nl{" dark" if fill else ""}">{label}</text>'
                   f'<text x="{x + NODE_W - 8}" y="{y + 21}" class="lv">{html.escape(tag + flags)}</text></g>')

    rows = []
    for n in sorted((n for n in nodes.values() if n.observed), key=lambda n: -n.last_turn):
        c = kg.concepts[n.concept]
        lv = LEVELS[n.level]
        status = ", ".join(s for s in ("provisional" if n.provisional else "", "plateau" if n.plateau else "",
                                         "stale" if n.stale else "", "pinned" if n.pinned_level is not None else "") if s) or "observed"
        hist = " → ".join(LEVELS[l] for _, l in n.history[-8:])
        rows.append(
            f"<tr><td>{html.escape(c.label)}</td><td>{html.escape(kg.chapters[c.chapter].get('label', c.chapter))}</td>"
            f'<td><span class="pill" style="background:{COLOURS[lv]}">{lv}</span> {html.escape(kg.level_names.get(lv, ""))}</td>'
            f"<td>{html.escape(n.confidence)}</td><td>{html.escape(status)}</td><td>{html.escape(hist)}</td>"
            f"<td>{html.escape(n.stop_reason)}</td><td>{html.escape(', '.join(sorted(n.held)) or '—')}</td></tr>")
    gap_rows = "".join(f"<li>{html.escape(kg.concepts[p].label)} → {html.escape(kg.concepts[c].label)}</li>" for p, c in g.gaps)
    s = g.summary()
    legend = "".join(f'<span><i style="background:{COLOURS[lv]}"></i>{lv} {html.escape(kg.level_names.get(lv, ""))} '
                     f'({s["level_distribution"][lv]})</span>' for lv in LEVELS)

    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Concept Map — {html.escape(g.student_id)}</title>
<style>
:root {{ --bg:#fafafa; --fg:#222; --muted:#777; --idle:#fff; --line:#ccc; --hot:#555; --front:#eef3f8; --bad:#c62828; }}
@media (prefers-color-scheme: dark) {{ :root {{ --bg:#16181c; --fg:#e6e6e6; --muted:#8a8f98; --idle:#1f2329; --line:#3a3f47; --hot:#b8bec8; --front:#243040; --bad:#ef5350; }} }}
body {{ margin:0; padding:16px; background:var(--bg); color:var(--fg); font:14px/1.45 system-ui,-apple-system,Segoe UI,sans-serif; }}
h1 {{ font-size:20px; margin:0 0 4px; }} h2 {{ font-size:16px; margin:20px 0 6px; }}
.sub,.note {{ color:var(--muted); }} .note {{ font-size:12px; }}
.legend {{ display:flex; flex-wrap:wrap; gap:14px; margin:8px 0 12px; }}
.legend i {{ display:inline-block; width:12px; height:12px; border-radius:3px; margin-right:5px; vertical-align:-1px; }}
.wrap {{ overflow-x:auto; border:1px solid var(--line); border-radius:8px; }}
svg {{ display:block; min-width:{width}px; }}
.ch {{ font-weight:600; font-size:13px; text-anchor:middle; fill:var(--fg); }}
.nl {{ font-size:12px; fill:var(--fg); }} .nl.dark,.lv {{ fill:#111; }}
.lv {{ font-weight:700; font-size:11px; text-anchor:end; }}
.idle {{ fill:var(--idle); stroke:var(--line); }}
.front {{ fill:var(--front); stroke:var(--hot); stroke-dasharray:4 3; }}
.obs {{ stroke:#111; stroke-width:1.5; }} .prov {{ stroke-dasharray:5 3; stroke-width:2; }}
.inf {{ fill-opacity:.35; stroke:var(--hot); stroke-dasharray:2 2; }}
.risk {{ stroke:var(--bad) !important; stroke-width:2.5 !important; }}
.edge {{ fill:none; stroke:var(--line); stroke-width:1; }} .edge.hot {{ stroke:var(--hot); stroke-width:1.8; }}
.edge.gap {{ stroke:var(--bad); stroke-width:2.2; }}
table {{ border-collapse:collapse; width:100%; margin-top:8px; font-size:13px; }}
th,td {{ text-align:left; padding:6px 8px; border-bottom:1px solid var(--line); vertical-align:top; }}
.pill {{ color:#111; font-weight:700; padding:1px 6px; border-radius:4px; }}
</style></head><body>
<h1>Concept map: {html.escape(g.student_id)}</h1>
<p class="sub">{s["observed"]} concept(s) assessed · {s["inferred"]} inferred · {s["frontier"]} on the frontier · {s["gaps"]} gap(s) · turn {g.turn}</p>
<div class="legend">{legend}</div>
<p class="note">Solid = observed · dashed border = provisional (jump not yet repeated) · pale = inferred · dashed outline = frontier · red outline = at risk · red arrow = gap · ! held misconception · = plateau · ~ stale</p>
<div class="wrap"><svg viewBox="0 0 {width} {height}" width="{width}" height="{height}">
<defs><marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="var(--hot)"/></marker>
<marker id="arrgap" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="var(--bad)"/></marker></defs>
{''.join(svg)}
</svg></div>
<h2>Assessed concepts</h2>
<table><thead><tr><th>Concept</th><th>Chapter</th><th>Level</th><th>Confidence</th><th>Status</th><th>History</th><th>Why this level</th><th>Held misconceptions</th></tr></thead>
<tbody>{''.join(rows) or '<tr><td colspan="8">Nothing assessed yet.</td></tr>'}</tbody></table>
<h2>Gaps</h2><ul>{gap_rows or '<li>None</li>'}</ul>
</body></html>"""


def write_map(g, path: Path) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_html(g), encoding="utf-8")
    return path
