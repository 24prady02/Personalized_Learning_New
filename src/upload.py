"""Upload one scenario run to GitHub as its own commit.

    upload_run("MY03")           # builds results/viewer/MY03_demo.html and notebooks/runs/MY03.ipynb (the run as its own notebook page,
                                 # shown by GitHub) from the cached prompts, commits the run's files, pushes

Used by the notebook at the end of every run, so each scenario is a separate commit on the branch. Git is called
exactly as from a terminal (the stored login of this computer); nothing is read from it here.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from utils import PROCESSED_DIR, ROOT  # noqa: E402


def _git(*args: str) -> str:
    r = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True)
    return (r.stdout + r.stderr).strip()


def run_notebook(sid: str) -> Path:
    """notebooks/runs/<sid>.ipynb: the run's step report as markdown cells with each figure as an image output, so GitHub
    shows every scenario as its own notebook page. Built from results/viewer/<sid>_steps.md and <sid>_figureNN.png."""
    import base64
    import re
    import nbformat
    text = (ROOT / "results/viewer" / f"{sid}_steps.md").read_text(encoding="utf-8")
    cells, buf = [], []

    def flush():
        if "".join(buf).strip():
            cells.append(nbformat.v4.new_markdown_cell("".join(buf).rstrip() + chr(10)))
        buf.clear()
    for line in text.splitlines(keepends=True):
        m = re.match(r"Figure (\d+)( \(final picture\))?: (.+\.png)\s*$", line)
        if m and Path(m.group(3).strip()).exists():
            flush()
            png = base64.b64encode(Path(m.group(3).strip()).read_bytes()).decode("ascii")
            cell = nbformat.v4.new_code_cell(f"# Figure {m.group(1)}{m.group(2) or ''}", execution_count=int(m.group(1)))
            cell.outputs = [nbformat.v4.new_output("display_data", data={"image/png": png, "text/plain": f"Figure {m.group(1)}"})]
            cell.metadata["scrolled"] = False
            cells.append(cell)
        else:
            buf.append(line)
    flush()
    nb = nbformat.v4.new_notebook(cells=cells, metadata={"kernelspec": {"name": "python3", "display_name": "Python 3", "language": "python"},
                                                         "language_info": {"name": "python"}})
    out = ROOT / "notebooks/runs" / f"{sid}.ipynb"
    out.parent.mkdir(parents=True, exist_ok=True)
    nbformat.validate(nb)
    nbformat.write(nb, out)
    return out


def run_files(sid: str) -> list[str]:
    files = [f"notebooks/runs/{sid}.ipynb", f"data/processed/{sid}_subgraph.json", f"data/processed/{sid}_input.json", f"data/processed/{sid}_diagnosis.json",
             f"experiments/logs/traverse_{sid}.txt", f"results/viewer/{sid}_steps.md", f"results/viewer/{sid}_demo.html",
             f"results/viewer/{sid}_G.html", "experiments/llm_cache"]
    files += [str(p.relative_to(ROOT)).replace("\\", "/") for p in sorted((ROOT / "results/viewer").glob(f"{sid}_figure*.png"))]
    return [f for f in files if (ROOT / f).exists()]


def upload_run(sid: str, build_page: bool = True, extra: tuple[str, ...] = ()) -> str:
    """Commit and push one run. Returns the git output to show."""
    diag = json.loads((PROCESSED_DIR / f"{sid}_diagnosis.json").read_text(encoding="utf-8"))
    if build_page:
        import demo
        sc = json.loads((PROCESSED_DIR / f"{sid}_input.json").read_text(encoding="utf-8"))
        demo.run(sid, sc, open_browser=False, verbose=False)        # every prompt is cached: no new Claude call
    run_notebook(sid)
    held = ", ".join(h["misconception"] for h in diag.get("held_misconceptions", [])) or "none"
    root = (diag.get("root_cause") or {}).get("concept", "none")
    msg = f"Scenario {sid}: held {held}; root cause {root}; overall {diag.get('overall_level')}\n\nCo-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>\n"
    out = [_git("add", "--", *run_files(sid), *extra)]
    out.append(_git("commit", "-q", "-m", msg))
    out.append(_git("push", "origin", "HEAD"))
    out.append(_git("log", "--oneline", "-1"))
    return "\n".join(o for o in out if o)


def upload_notebook() -> str:
    """Commit and push the notebook file as saved on disk (press Ctrl+S in the notebook first)."""
    out = [_git("add", "--", "notebooks/think_on_the_graph.ipynb"),
           _git("commit", "-q", "-m", "Notebook saved with its latest run\n\nCo-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>\n"),
           _git("push", "origin", "HEAD"), _git("log", "--oneline", "-1")]
    return "\n".join(o for o in out if o)


if __name__ == "__main__":
    print(upload_run(sys.argv[1]) if len(sys.argv) > 1 else upload_notebook())
