"""Upload one scenario run to GitHub as its own commit.

    upload_run("MY03")           # builds results/viewer/MY03_demo.html and the scenario's own folder notebooks/runs/MY03/
                                 # (README.md = the step report with the figures, shown by GitHub when the folder is opened;
                                 # MY03.ipynb = the same as a notebook; input, diagnosis, subgraph, log, figures, HTML report)
                                 # from the cached prompts, commits the run's files, pushes

Used by the notebook at the end of every run, so each scenario is a separate commit on the branch. Git is called
exactly as from a terminal (the stored login of this computer); nothing is read from it here.
"""
from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from utils import PROCESSED_DIR, ROOT  # noqa: E402

NL = chr(10)


def _git(*args: str) -> str:
    r = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True)
    return (r.stdout + r.stderr).strip()


def _push() -> str:
    """Push the branch; if GitHub has commits this computer lacks (e.g. a file deleted on the GitHub page), put ours on top
    of them (rebase) and push again."""
    out = _git("push", "origin", "HEAD")
    if "rejected" in out or "failed to push" in out:
        branch = _git("rev-parse", "--abbrev-ref", "HEAD")
        out += NL + _git("pull", "--rebase", "origin", branch) + NL + _git("push", "origin", "HEAD")
    return out


def _figure_lines(text: str) -> str:
    """'Figure N: <abs path>.png' lines of a step report -> markdown image links to figureNN.png in the same folder."""
    def link(m: re.Match) -> str:
        return f"**Figure {m.group(1)}{m.group(2) or ''}**" + NL + NL + f"![Figure {m.group(1)}]({m.group(3)})"
    return re.sub(r"^Figure (\d+)( \([^)]*\))?: .+?(figure\d+\.png)\s*$", link, text, flags=re.M)


def _report(sid: str) -> str:
    return _figure_lines((ROOT / "results/viewer" / f"{sid}_steps.md").read_text(encoding="utf-8"))


def run_notebook(sid: str) -> Path:
    """notebooks/runs/<sid>/<sid>.ipynb: the step report as markdown cells, one per section, figures as relative image links
    (figureNN.png beside it), so the file stays small enough for GitHub to show."""
    import nbformat
    parts = re.split(r"(?m)^(?=## )", _report(sid))
    cells = [nbformat.v4.new_markdown_cell(p.rstrip() + NL) for p in parts if p.strip()]
    nb = nbformat.v4.new_notebook(cells=cells, metadata={"kernelspec": {"name": "python3", "display_name": "Python 3", "language": "python"},
                                                         "language_info": {"name": "python"}})
    out = ROOT / "notebooks/runs" / sid / f"{sid}.ipynb"
    out.parent.mkdir(parents=True, exist_ok=True)
    nbformat.validate(nb)
    nbformat.write(nb, out)
    return out


def scenario_folder(sid: str) -> Path:
    """notebooks/runs/<sid>/: everything of one scenario in one folder, with README.md (the step report with its figures),
    which GitHub shows as soon as the folder is opened."""
    folder = ROOT / "notebooks/runs" / sid
    folder.mkdir(parents=True, exist_ok=True)
    pairs = [(PROCESSED_DIR / f"{sid}_input.json", "input.json"), (PROCESSED_DIR / f"{sid}_subgraph.json", "subgraph.json"),
             (PROCESSED_DIR / f"{sid}_diagnosis.json", "diagnosis.json"), (ROOT / "experiments/logs" / f"traverse_{sid}.txt", "traverse_log.txt"),
             (ROOT / "results/viewer" / f"{sid}_demo.html", "report.html"), (ROOT / "results/viewer" / f"{sid}_G.html", f"{sid}_G.html")]
    pairs += [(f, f.name.replace(f"{sid}_", "")) for f in sorted((ROOT / "results/viewer").glob(f"{sid}_figure*.png"))]
    for src, name in pairs:
        if src.exists():
            shutil.copyfile(src, folder / name)
    old = folder / "steps.md"                       # earlier layout; README.md replaces it
    if old.exists():
        old.unlink()
    if (ROOT / "results/viewer" / f"{sid}_steps.md").exists():
        head = (f"Files of this scenario: `input.json` (program, question, answer), `diagnosis.json`, `subgraph.json`, `traverse_log.txt`, "
                f"`report.html` (this report as one full-page file, with the interactive graph `{sid}_G.html`), `{sid}.ipynb` (this report as a notebook)."
                + NL + NL)
        text = _report(sid)
        text = text.replace(NL, NL + NL + head, 1) if text.startswith("# ") else head + text
        (folder / "README.md").write_text(text, encoding="utf-8")
    return folder


def run_files(sid: str) -> list[str]:
    files = [f"notebooks/runs/{sid}", f"data/processed/{sid}_subgraph.json", f"data/processed/{sid}_input.json", f"data/processed/{sid}_diagnosis.json",
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
    scenario_folder(sid)
    held = ", ".join(h["misconception"] for h in diag.get("held_misconceptions", [])) or "none"
    root = (diag.get("root_cause") or {}).get("concept", "none")
    msg = f"Scenario {sid}: held {held}; root cause {root}; overall {diag.get('overall_level')}" + NL + NL + "Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>" + NL
    out = [_git("add", "-A", "--", *run_files(sid), *extra)]
    out.append(_git("commit", "-q", "-m", msg))
    out.append(_push())
    out.append(_git("log", "--oneline", "-1"))
    return NL.join(o for o in out if o)


def upload_notebook() -> str:
    """Commit and push the notebook file as saved on disk (press Ctrl+S in the notebook first)."""
    out = [_git("add", "--", "notebooks/think_on_the_graph.ipynb"),
           _git("commit", "-q", "-m", "Notebook saved with its latest run" + NL + NL + "Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>" + NL),
           _push(), _git("log", "--oneline", "-1")]
    return NL.join(o for o in out if o)


if __name__ == "__main__":
    print(upload_run(sys.argv[1]) if len(sys.argv) > 1 else upload_notebook())
