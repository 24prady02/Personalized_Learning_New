"""
second_marker_365.py — an independent second marker for all 365 scenarios, to
compare with the classifier (scenario_run_v10_all) where no human label exists.

The marker is a different model (Sonnet; the classifier's judge is Opus). It sees
only the question, the code, the student's answer and the graph's general L0-L4
level definitions (criterion_general and deciding_question of the learning-level
nodes, made concept-neutral). It does not see the classifier's level, the code-run
facts, or the per-concept ways the classifier's judge reads.

Steps:
  1. mark all 365 (claude -p, cached in output/marker_cache, 4 at a time)
  2. score the marker on the 44 human-labelled answers (how far to trust it)
  3. compare marker and classifier on all 365: agreement, Cohen's kappa,
     confusion matrix
  4. review sheet: every disagreement + 20 random agreements, for a person

Usage: python scripts/second_marker_365.py [--run scenario_run_v10_all] [--model sonnet]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import random
import re
import shutil
import subprocess
import sys
import tempfile
import time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from fuse_44 import GRAPH_KEY  # noqa: E402
from run_student_scenarios import asked_part, load_scenarios  # noqa: E402

CACHE = ROOT / "output" / "marker_cache"
LEVELS = ["L0", "L1", "L2", "L3", "L4"]


def level_definitions() -> str:
    kg = json.loads((ROOT / "data" / "chapter1_kg.json").read_text(encoding="utf-8"))
    nodes = {n["level"]: n for n in kg["learning_levels"] if n["concept"] == "program_text"}
    out = []
    for lv in LEVELS:
        n = nodes[lv]
        crit = n["criterion_general"].replace("program text", "the concept")
        dq = n["deciding_question"].replace("program text", "the concept")
        out.append(f"{lv} ({n['name'].split(' / ')[0]}): {crit}\n   Deciding question: {dq}")
    return "\n".join(out)


SYSTEM = """You are an experienced Java teacher marking one student answer on a 5-level learning ladder (L0-L4),
using only the level definitions given. Mark the answer as a whole, for the main thing the question part asks about.
Return JSON only: {"level":"L0|L1|L2|L3|L4|none","concept":"<what the answer is mainly about, a few words>","why":"<one short sentence>"}
Use "none" only when the answer gives nothing that can be levelled (empty, off topic, or only a question)."""


def prompt(defs: str, question: str, code: str, answer: str) -> str:
    return (f"LEVEL DEFINITIONS (from the course knowledge graph):\n{defs}\n\n"
            f"QUESTION (the part the student answers):\n{question}\n\nCODE:\n{(code or '(none)')[:1500]}\n\n"
            f"STUDENT ANSWER:\n{answer}\n\nMark it.")


def call(model: str, text: str) -> dict:
    CACHE.mkdir(parents=True, exist_ok=True)
    f = CACHE / (hashlib.sha256((model + SYSTEM + text).encode("utf-8")).hexdigest()[:24] + ".json")
    if f.exists():
        return json.loads(f.read_text(encoding="utf-8"))
    exe = shutil.which("claude.cmd") or shutil.which("claude") or "claude"
    for wait in (0, 10, 30, 90):
        time.sleep(wait)
        with tempfile.TemporaryDirectory() as tmp:
            sp = Path(tmp) / "system.txt"
            sp.write_text(SYSTEM, encoding="utf-8")
            r = subprocess.run([exe, "-p", "--output-format", "json", "--tools", "", "--no-session-persistence",
                                "--model", model, "--system-prompt-file", str(sp)],
                               input=text, capture_output=True, text=True, encoding="utf-8", cwd=tmp, timeout=600)
        if r.returncode == 0:
            txt = json.loads(r.stdout).get("result", "")
            m = re.search(r"\{.*\}", txt, re.S)
            try:
                out = json.loads(m.group(0)) if m else {"level": "none", "why": "unparsed"}
            except json.JSONDecodeError:
                out = {"level": "none", "why": "unparsed: " + txt[:200]}
            f.write_text(json.dumps(out, ensure_ascii=False), encoding="utf-8")
            return out
    return {"level": "none", "why": "marker unavailable", "unavailable": True}


def kappa(a, b) -> float:
    cats = sorted(set(a) | set(b), key=str)
    n = len(a)
    po = sum(x == y for x, y in zip(a, b)) / n
    ca, cb = Counter(a), Counter(b)
    pe = sum(ca[c] * cb[c] for c in cats) / (n * n)
    return (po - pe) / (1 - pe) if pe < 1 else 1.0


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", default="scenario_run_v10_all")
    ap.add_argument("--model", default="sonnet")
    args = ap.parse_args()
    questions, scenarios = load_scenarios()
    system = {s["id"]: s for s in json.loads((ROOT / "output" / args.run / "results.json").read_text(encoding="utf-8"))["scenarios"]}
    defs = level_definitions()

    jobs = []
    for s in scenarios:
        q = questions.get(s["question"], {})
        asked = asked_part(q.get("question", ""), s["scenario_type"]) or q.get("question", "")
        jobs.append((s, prompt(defs, asked, q.get("code", ""), s["text"])))
    done = [0]

    def work(job):
        s, text = job
        out = call(args.model, text)
        done[0] += 1
        if done[0] % 25 == 0:
            print(f"  marked {done[0]}/{len(jobs)}", flush=True)
        return s["id"], out

    with ThreadPoolExecutor(max_workers=4) as pool:
        marks = dict(pool.map(work, jobs))

    rows = []
    for s, _ in jobs:
        m = marks[s["id"]]
        lv = m.get("level") if m.get("level") in LEVELS else None
        rows.append({"id": s["id"], "type": s["scenario_type"], "question": s["question"], "text": s["text"],
                     "label": s["expected_level"], "graph_label": GRAPH_KEY.get(s["id"], (s["expected_level"],))[0],
                     "system": system[s["id"]]["max_level"], "marker": lv, "marker_concept": m.get("concept", ""),
                     "marker_why": m.get("why", ""), "unavailable": bool(m.get("unavailable"))})
    out = ROOT / "output" / "second_marker"
    out.mkdir(exist_ok=True)
    (out / "marks.json").write_text(json.dumps(rows, indent=1, ensure_ascii=False), encoding="utf-8")

    lines = []
    lab = [r for r in rows if r["label"]]
    for key in ("label", "graph_label"):
        for who in ("marker", "system"):
            ex = sum(r[who] == r[key] for r in lab)
            lines.append(f"on the 44 human-labelled ({key}): {who} exact {ex}/44")
    a = [r["system"] or "none" for r in rows]
    b = [r["marker"] or "none" for r in rows]
    agree = sum(x == y for x, y in zip(a, b))
    within = sum(x != "none" and y != "none" and abs(int(x[1]) - int(y[1])) <= 1 for x, y in zip(a, b))
    lines.append(f"all 365: system and marker agree exactly on {agree}/365 ({agree / 365:.0%}), within one level "
                 f"{within}, Cohen's kappa {kappa(a, b):.2f}")
    unl = [r for r in rows if not r["label"]]
    ag = sum((r["system"] or "none") == (r["marker"] or "none") for r in unl)
    lines.append(f"the 321 unlabelled: agree on {ag}/{len(unl)} ({ag / len(unl):.0%})")
    lines.append(f"marker unavailable: {sum(r['unavailable'] for r in rows)}")
    cats = LEVELS + ["none"]
    conf = Counter(zip(a, b))
    lines.append("confusion (rows = system, columns = marker):")
    lines.append("        " + "".join(f"{c:>7}" for c in cats))
    for x in cats:
        lines.append(f"{x:>7} " + "".join(f"{conf[(x, y)]:>7}" for y in cats))
    print("\n".join(lines))
    (out / "summary.txt").write_text("\n".join(lines), encoding="utf-8")

    # review sheet: every disagreement on the unlabelled answers + 20 random agreements; no levels shown
    import openpyxl
    random.seed(7)
    dis = [r for r in unl if (r["system"] or "none") != (r["marker"] or "none")]
    agr = random.sample([r for r in unl if (r["system"] or "none") == (r["marker"] or "none")], 20)
    sheet = dis + agr
    random.shuffle(sheet)
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Label these"
    ws.append(["Scenario", "Question id", "Question part", "Student answer", "Your level (L0-L4 or none)", "Note"])
    for r in sheet:
        s = next(x for x, _ in jobs if x["id"] == r["id"])
        q = questions.get(s["question"], {})
        ws.append([r["id"], r["question"], asked_part(q.get("question", ""), s["scenario_type"]) or q.get("question", ""),
                   r["text"], "", ""])
    ws2 = wb.create_sheet("Key (hidden from labeller)")
    ws2.append(["Scenario", "In sheet because", "System level", "Marker level", "Marker reason"])
    for r in sheet:
        ws2.append([r["id"], "agreement sample" if r in agr else "disagreement", r["system"], r["marker"], r["marker_why"]])
    ws2.sheet_state = "hidden"
    wb.save(out / "review_sheet.xlsx")
    print(f"review sheet: {len(dis)} disagreements + 20 agreements -> {out / 'review_sheet.xlsx'}")


if __name__ == "__main__":
    main()
