"""One executed Jupyter notebook per concept of the knowledge graph, stored like the scenario runs.

    python src/concept_notebooks.py                 # all concepts
    python src/concept_notebooks.py char for_loop   # only these

For every concept <c> this writes concept_wise_graph/<c>/ :
    <c>.ipynb   the notebook that was run for the concept (visualizer code, then the concept's view), with its outputs
    <c>.html    the interactive graph page (written by the notebook)
    <c>.json    the nodes and edges of the view (written by the notebook)
    <c>.png     the same graph as a still picture (written by the notebook)
and concept_wise_graph/index.html to move between the pages.

The visualizer code is taken from cell 1 of notebooks/kg_visualizer.ipynb, so there is one copy of it.
Every edge in a view is an edge of data/raw/chapter1_kg_updated.json.
"""
import json
import sys
import html
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import nbformat
from nbclient import NotebookClient

ROOT = Path(__file__).resolve().parents[1]
SOURCE_NB = ROOT / "notebooks" / "kg_visualizer.ipynb"
OUT_DIR = ROOT / "concept_wise_graph"
KG = ROOT / "data" / "raw" / "chapter1_kg_updated.json"

VIEW_CODE = r'''
# The view of one concept: every node the knowledge graph relates to it, and only edges that are in the graph.
import re
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

HERE = Path.cwd()                      # concept_wise_graph/<concept>/
VIEW_LAYERS = {'topic', 'concept', 'learning_level', 'misconception', 'error'}
VIEW_ETYPES = {'contains', 'prerequisite', 'parallel', 'has_level', 'misconception', 'error'}
HOPS = 1
hops_sl.value = HOPS

def _share_library(page):
    """The drawing library is the same in every page: one copy is kept one folder up."""
    def swap(m, name, tag):
        body = m.group(1)
        if len(body) < 100_000 or 'drawGraph' in body:      # the page's own script (its nodes and edges) stays
            return m.group(0)
        lib = HERE.parent / name
        if not lib.exists():
            lib.write_text(body, encoding='utf-8')
        return tag
    page = re.sub(r'<style[^>]*>(.*?)</style>',
                  lambda m: swap(m, 'vis-network.min.css', '<link rel="stylesheet" href="../vis-network.min.css">'),
                  page, flags=re.S)
    return re.sub(r'<script[^>]*>(.*?)</script>',
                  lambda m: swap(m, 'vis-network.min.js', '<script src="../vis-network.min.js"></script>'),
                  page, flags=re.S)

H, _ = filter_graph(VIEW_LAYERS, VIEW_ETYPES, 'All', '', HOPS, True, CONCEPT)
report, writeup = concept_report(CONCEPT), edges_writeup(H, CONCEPT)

# 1. the interactive page
page = _tips(_freeze(render(H, False, True, {CONCEPT}, CONCEPT, CONCEPT).generate_html(), False))
page = _share_library(page.replace('</body>', report + writeup + '</body>', 1))
(HERE / f'{CONCEPT}.html').write_text(page, encoding='utf-8')

# 2. the same view as data
(HERE / f'{CONCEPT}.json').write_text(json.dumps({
    'concept': CONCEPT, 'label': _CONCEPT[CONCEPT].get('label', CONCEPT), 'graph_version': DATA.get('version'),
    'nodes': [{'id': n, 'kind': d['layer'], 'label': d['label']}
              for n, d in sorted(H.nodes(data=True), key=lambda x: (x[1]['layer'], str(x[0])))],
    'edges': [{'from': u, 'to': v, 'type': d['etype'], 'label': d.get('elogic', '')}
              for u, v, d in sorted(H.edges(data=True), key=lambda x: (x[2]['etype'], str(x[0]), str(x[1])))],
}, indent=1, ensure_ascii=False), encoding='utf-8')

# 3. a still picture of the graph (same positions as the interactive page)
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

# 4. the interactive graph, then the concept's report and every edge with its full label
rel = HERE.resolve().relative_to(ROOT).as_posix()
by = {}
for u, v, d in H.edges(data=True):
    by[d['etype']] = by.get(d['etype'], 0) + 1
display(HTML(
    f"<div style='background:#fff;color:#111;padding:10px;font:16px/1.6 arial'><b>{_esc(CONCEPT)}</b>: "
    f"{H.number_of_nodes()} nodes / {H.number_of_edges()} edges ("
    + ', '.join(f'{k} {n}' for k, n in sorted(by.items())) + "). <b>Click an edge to read its exact reasoning</b>; click a node for its rules. Interactive graph: "
    f"<a href='/files/{rel}/{CONCEPT}.html' target='_blank'>{CONCEPT}.html</a> "
    "(shown below when the notebook server is running from the repository folder)</div>"
    f"<iframe src='/files/{rel}/{CONCEPT}.html' style='width:100%;height:1040px;border:1px solid #ddd;background:#fff'></iframe>"))
display(HTML(report + writeup))
'''


def visualizer_code():
    nb = json.loads(SOURCE_NB.read_text(encoding="utf-8"))
    return "".join(nb["cells"][1]["source"])


def concepts():
    data = json.loads(KG.read_text(encoding="utf-8"))
    return {c["id"]: c.get("label", c["id"]) for c in data["concepts"]}


def run_concept(c, label, code):
    """Build the notebook of one concept, run it, save it with its outputs."""
    folder = OUT_DIR / c
    folder.mkdir(parents=True, exist_ok=True)
    nb = nbformat.v4.new_notebook()
    nb.metadata["kernelspec"] = {"display_name": "Python 3", "language": "python", "name": "python3"}
    nb.cells = [
        nbformat.v4.new_markdown_cell(
            f"# {label} (`{c}`)\n\n"
            f"The knowledge graph around the concept `{c}`, from `data/raw/chapter1_kg_updated.json`. "
            "Every edge drawn is an edge of that graph.\n\n"
            "Cell 1 is the knowledge graph visualizer (the same code as `notebooks/kg_visualizer.ipynb`). "
            f"Cell 2 draws the view of `{c}` and writes `{c}.html` (interactive graph), `{c}.json` (nodes and edges) "
            f"and `{c}.png` (still picture) next to this notebook."),
        nbformat.v4.new_code_cell(code),
        nbformat.v4.new_code_cell(f"CONCEPT = {c!r}\n" + VIEW_CODE),
    ]
    NotebookClient(nb, timeout=600, kernel_name="python3", resources={"metadata": {"path": str(folder)}}).execute()
    nbformat.write(nb, folder / f"{c}.ipynb")
    for old in (OUT_DIR / f"{c}.html", OUT_DIR / f"{c}.json"):     # the earlier flat copy of this view
        if old.exists():
            old.unlink()
    return c


def write_index(all_concepts):
    done = [c for c in sorted(all_concepts) if (OUT_DIR / c / f"{c}.html").exists()]
    links = "".join(f'<a href="{c}/{c}.html" target="view">{html.escape(c)}</a>' for c in done)
    (OUT_DIR / "index.html").write_text(
        "<!doctype html><html><head><meta charset='utf-8'><title>Knowledge graph: every concept</title><style>"
        "body{margin:0;display:flex;height:100vh;font:13px arial;color:#111;background:#fff}"
        "#list{width:250px;overflow:auto;border-right:1px solid #ddd;padding:8px;box-sizing:border-box}"
        "#list a{display:block;padding:2px 4px;color:#1a4fa0;text-decoration:none}#list a:hover{background:#eef}"
        "#q{width:100%;box-sizing:border-box;margin-bottom:6px;padding:4px}iframe{flex:1;border:0}</style></head><body>"
        f"<div id='list'><b>{len(done)} concepts</b><input id='q' placeholder='filter'>{links}</div>"
        f"<iframe name='view' src='{done[0]}/{done[0]}.html'></iframe>"
        "<script>document.getElementById('q').oninput=function(){var v=this.value.toLowerCase();"
        "document.querySelectorAll('#list a').forEach(function(a){a.style.display=a.textContent.toLowerCase().indexOf(v)<0?'none':'block'})}</script>"
        "</body></html>", encoding="utf-8")


def main(argv):
    every = concepts()
    todo = [c for c in argv if c in every] or sorted(every)
    unknown = [c for c in argv if c not in every]
    if unknown:
        sys.exit(f"not a concept id: {', '.join(unknown)}")
    code = visualizer_code()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    failed = []
    print(f"running {len(todo)} concept notebooks into {OUT_DIR}", flush=True)
    run_concept(todo[0], every[todo[0]], code)          # the first one alone: it writes the shared drawing library
    print(f"[1/{len(todo)}] {todo[0]}", flush=True)
    with ProcessPoolExecutor(max_workers=4) as pool:
        jobs = {c: pool.submit(run_concept, c, every[c], code) for c in todo[1:]}
        for i, (c, job) in enumerate(jobs.items(), 2):
            try:
                job.result()
                print(f"[{i}/{len(todo)}] {c}", flush=True)
            except Exception as err:                     # keep going, report at the end
                failed.append(c)
                print(f"[{i}/{len(todo)}] {c} FAILED: {str(err)[-400:]}", flush=True)
    write_index(every)
    print(f"done: {len(todo) - len(failed)} run, {len(failed)} failed {failed if failed else ''}", flush=True)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
