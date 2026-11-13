"""One executed Jupyter notebook per concept of the knowledge graph, stored like the scenario runs.

    python src/concept_notebooks.py                 # all concepts
    python src/concept_notebooks.py char for_loop   # only these

For every concept <c> this writes concept_wise_graph/<c>/ with three files:
    <c>.ipynb   the short notebook that was run for the concept: it draws the picture and writes the other two files
    <c>.png     the graph around the concept
    <c>.md      the explanation: every relation of the concept and its reasoning, written out as text

The visualizer code stays in cell 1 of scenario_explanations/kg_visualizer.ipynb; the concept notebooks load it from there.
Every relation described is an edge of data/raw/chapter1_kg_updated.json.
"""
import json
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import nbformat
from nbclient import NotebookClient

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "concept_wise_graph"
KG = ROOT / "data" / "raw" / "chapter1_kg_updated.json"

LOAD_CODE = r'''# 1. Load the knowledge graph visualizer (cell 1 of scenario_explanations/kg_visualizer.ipynb) and the graph itself.
import json
from pathlib import Path

ROOT = Path.cwd().resolve()
while not (ROOT / 'data' / 'raw').exists() and ROOT.parent != ROOT:
    ROOT = ROOT.parent
_visualizer = json.load(open(ROOT / 'scenario_explanations' / 'kg_visualizer.ipynb', encoding='utf-8'))
exec(''.join(_visualizer['cells'][1]['source']))
print(_loaded)
'''

VIEW_CODE = r'''
# 2. The view of the concept: the picture, and the explanation of every relation.
import re
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

HERE = Path.cwd()                      # concept_wise_graph/<concept>/
VIEW_LAYERS = {'topic', 'concept', 'learning_level', 'misconception', 'error'}
VIEW_ETYPES = {'contains', 'prerequisite', 'parallel', 'has_level', 'misconception', 'error'}
H, _ = filter_graph(VIEW_LAYERS, VIEW_ETYPES, 'All', '', 1, True, CONCEPT)   # only edges of the knowledge graph

# ---- the picture ----
pos = {n: (x, -y) for n, (x, y) in radial_layout(H, CONCEPT).items()}
S = nx.DiGraph()
S.add_nodes_from(H.nodes())
fig, ax = plt.subplots(figsize=(18, 13))
keys = []
for et in sorted({d['etype'] for _, _, d in H.edges(data=True)}):
    st = EDGE_STYLE[et]
    nx.draw_networkx_edges(S, pos, ax=ax, edgelist=[(u, v) for u, v, d in H.edges(data=True) if d['etype'] == et],
                           edge_color=st['color'], width=st['width'] * 0.6, style='dashed' if st['dashes'] else 'solid',
                           arrows=True, arrowstyle='-' if et == 'parallel' else '-|>', arrowsize=9, node_size=260)
    keys.append(Line2D([], [], color=st['color'], lw=2, ls='--' if st['dashes'] else '-', label=et + ' edge'))
MARK = {'box': 's', 'dot': 'o', 'diamond': 'D', 'triangle': '^', 'star': '*'}
for lay, st in LAYER_STYLE.items():
    ns = [n for n, d in H.nodes(data=True) if d['layer'] == lay]
    if ns:
        cols = ([LEVEL_COLOR.get(H.nodes[n]['label'], st['color']) for n in ns] if lay == 'learning_level'
                else ['#111111' if n == CONCEPT else st['color'] for n in ns])
        nx.draw_networkx_nodes(S, pos, ax=ax, nodelist=ns, node_color=cols, node_shape=MARK[st['shape']],
                               node_size=[520 if n == CONCEPT else 260 for n in ns])
        keys.append(Line2D([], [], color=st['color'], marker=MARK[st['shape']], ls='', ms=9, label=lay))
nx.draw_networkx_labels(S, {n: (x, y - 55) for n, (x, y) in pos.items()}, ax=ax, font_size=7,
                        labels={n: _wrap(d['label'], 24) for n, d in H.nodes(data=True)}, verticalalignment='top')
ax.set_title(f"{_CONCEPT[CONCEPT].get('label', CONCEPT)} ({CONCEPT}): {H.number_of_nodes()} nodes, "
             f"{H.number_of_edges()} edges, all from the knowledge graph {str(DATA.get('version'))[:5]}")
ax.legend(handles=keys, loc='upper right', fontsize=8, ncol=2)
ax.margins(0.08)
ax.axis('off')
fig.savefig(HERE / f'{CONCEPT}.png', dpi=110, bbox_inches='tight')
plt.show()

# ---- the explanation (<concept>.md): the two tables of the concept view ----
#   1. Concepts associated with the concept: concept, description, how it is associated
#   2. Every edge in this view and its full label: from, edge, to, full edge label (the exact edge logic)
def md(t):
    """Text from the graph, safe inside a markdown table cell."""
    t = str(t or '').replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    return re.sub(r'([*_`|])', r'\\\1', t).strip().replace('\n', '<br>')

def full_label(u, v, et):
    """The full label of an edge, word for word from the graph, one part per line."""
    if et in ('prerequisite', 'parallel'):
        e = _REL_EDGE.get(frozenset((u, v)), {})
        lines = [md(e.get('logic') or e.get('edge_logic'))]
        if e.get('grounding'):
            lines.append('grounding: ' + md(e['grounding']))
        for x, y in ((u, v), (v, u)):
            if (x, y) in _R_RULE:
                lines.append(f"composition rule (R) of {md(x)} with {md(y)}: {md(_R_RULE[(x, y)])}")
        return lines
    if et in ('misconception', 'error'):
        e = _MIS_EDGE.get((u, v), {})
        return (['**wrong rule:** ' + md(e.get('logic')), '**right rule:** ' + md(e.get('twin_logic'))]
                + (['role: ' + md(e['role'])] if e.get('role') else []))
    if et == 'has_level':
        e = _HAS_LEVEL.get((u, str(v).split('@')[-1]), {})
        lines = [md(e.get('logic'))]
        for i, w in enumerate(e.get('ways', [])):
            link = w.get('linked_misconception') or []
            lines.append(f"**[{i}] {md(w.get('way'))}** ({md(w.get('rule_type'))})"
                         + (' &rarr; ' + md(', '.join(link)) if link else '') + ': ' + md(w.get('exact_rule')))
        return lines
    if et == 'contains':
        return [f"topic {md(u)} contains {md(v)}"]
    return ['']

d0 = _CONCEPT[CONCEPT]
assoc = {o: w for o, w in concept_associations(CONCEPT, 1).items() if o in H}
ORDER = ['prerequisite', 'parallel', 'misconception', 'error', 'has_level', 'contains', 'precedes', 'section_prerequisite']
every = sorted(((u, v, d['etype']) for u, v, d in H.edges(data=True)),
               key=lambda x: (ORDER.index(x[2]) if x[2] in ORDER else 99, x[0], str(x[1])))

out = [f"# {d0.get('label', CONCEPT)} (`{CONCEPT}`)", '',
       md(d0.get('description', '')), '',
       f"Section {md(d0.get('section', ''))} {md(d0.get('section_title', ''))}, "
       f"topic {md(d0.get('topic', ''))} {md(d0.get('topic_title', ''))}. "
       f"From the knowledge graph {str(DATA.get('version'))[:5]} (`data/raw/chapter1_kg_updated.json`).", '',
       f"![The knowledge graph around {CONCEPT}]({CONCEPT}.png)", '',
       f"## Concepts associated with {md(CONCEPT)} ({len(assoc)})", '']
if assoc:
    out += ['| Concept | Description | How it is associated |', '| --- | --- | --- |']
    out += [f"| **{md(o)}** | {md(_CONCEPT[o].get('description', ''))} | {'<br>'.join(md(x) for x in w)} |"
            for o, w in sorted(assoc.items())]
else:
    out.append('No other concept is associated with this one in the graph.')
out += ['', f"## Every edge in this view and its full label ({len(every)})", '',
        '| From | Edge | To | Full edge label |', '| --- | --- | --- | --- |']
out += [f"| **{md(u)}** | {md(et)} | **{md(v)}** | {'<br>'.join(x for x in full_label(u, v, et) if x)} |"
        for u, v, et in every]
out.append('')
(HERE / f'{CONCEPT}.md').write_text('\n'.join(out), encoding='utf-8')
print(f"{CONCEPT}: {H.number_of_nodes()} nodes, {H.number_of_edges()} edges. Written: {CONCEPT}.png, {CONCEPT}.md")
'''


def concepts():
    data = json.loads(KG.read_text(encoding="utf-8"))
    return {c["id"]: c.get("label", c["id"]) for c in data["concepts"]}


def run_concept(c, label):
    """Build the notebook of one concept, run it, save it with its outputs."""
    folder = OUT_DIR / c
    folder.mkdir(parents=True, exist_ok=True)
    for attempt in (1, 2, 3):
        nb = nbformat.v4.new_notebook()
        nb.metadata["kernelspec"] = {"display_name": "Python 3", "language": "python", "name": "python3"}
        nb.cells = [
            nbformat.v4.new_markdown_cell(
                f"# {label} (`{c}`)\n\n"
                f"The knowledge graph around `{c}`. This notebook draws the picture (`{c}.png`) and writes the explanation of "
                f"every relation of the concept: read it in [{c}.md]({c}.md)."),
            nbformat.v4.new_code_cell(LOAD_CODE),
            nbformat.v4.new_code_cell(f"CONCEPT = {c!r}\n" + VIEW_CODE),
        ]
        try:
            NotebookClient(nb, timeout=240, kernel_name="python3", resources={"metadata": {"path": str(folder)}}).execute()
            break
        except Exception as err:                         # a kernel that hangs or dies: say why, then run it again
            print(f"    {c}: attempt {attempt} failed with {type(err).__name__}: {' '.join(str(err).split())[:300]}", flush=True)
            if attempt == 3:
                raise
    # the visualizer's control panel is of no use in a saved notebook: keep only the line that says what was loaded
    nb.cells[1].outputs = [o for o in nb.cells[1].outputs if o.output_type == "stream"]
    nb.metadata.pop("widgets", None)
    nbformat.write(nb, folder / f"{c}.ipynb")
    keep = {f"{c}.ipynb", f"{c}.png", f"{c}.md"}
    for old in folder.iterdir():                       # files of the earlier layout (html page, json, README)
        if old.is_file() and old.name not in keep:
            old.unlink()
    return c


def main(argv):
    every = concepts()
    unknown = [c for c in argv if c not in every]
    if unknown:
        sys.exit(f"not a concept id: {', '.join(unknown)}")
    todo = list(argv) or sorted(every)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    failed = []
    print(f"running {len(todo)} concept notebooks into {OUT_DIR}", flush=True)
    with ProcessPoolExecutor(max_workers=4) as pool:
        jobs = {c: pool.submit(run_concept, c, every[c]) for c in todo}
        for i, (c, job) in enumerate(jobs.items(), 1):
            try:
                job.result()
                print(f"[{i}/{len(todo)}] {c}", flush=True)
            except Exception as err:                     # keep going, report at the end
                failed.append(c)
                print(f"[{i}/{len(todo)}] {c} FAILED: {str(err)[-400:]}", flush=True)
    for old in OUT_DIR.iterdir():                        # shared files of the earlier layout
        if old.is_file():
            old.unlink()
    print(f"done: {len(todo) - len(failed)} run, {len(failed)} failed {failed if failed else ''}", flush=True)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
