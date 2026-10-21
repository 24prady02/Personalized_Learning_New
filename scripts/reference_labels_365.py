"""
reference_labels_365.py — reference levels for all 365 answers from models other
than the classifier's judge (Opus), to score the classifier where no human label exists.

  1. Label    Sonnet 5.5 marks every answer as a teacher would: the question part,
              the code, the output of running that code, the student's answer, the
              graph's L0-L4 level definitions and its boundary rules. It never sees
              the classifier's level, reasons or evidence.
  2. Validate The labeller is scored on the 44 human-labelled answers (graph-boundary key).
  3. Adjudicate  Where classifier and labeller disagree, Fable 5.1 (a third model) sees
              the same material and the two levels as "A" and "B" in random order,
              without knowing which came from the classifier, and picks the right one
              (or its own). It is also scored on the 44.
  4. Score    The classifier against the final reference levels, on the 321 and the 44.

Usage: python scripts/reference_labels_365.py [--run scenario_run_v10_all]
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
from second_marker_365 import level_definitions  # noqa: E402

CACHE = ROOT / "output" / "reference_cache"
OUT = ROOT / "output" / "reference_labels"
LEVELS = ["L0", "L1", "L2", "L3", "L4"]
WORKERS = 4

# the graph's boundary rules (boundary text of the has_level edges), stated generally
BOUNDARIES = """Boundary rules from the knowledge graph (apply them):
- Reading the code with everyday meanings, or using a rule that contradicts Java, is L0, even with Java words.
- Copying the code back word for word with no interpretation is L0.
- A single slip in an otherwise rule-correct trace is L2 with an error, not L0.
- Naming the element, or stating one correct rule or definition without applying it to this code, is L1.
- A bare correct result or output with no justification is L1 (a correct output is not levelled above L1 on its own).
- Applying the rules to this code's values or lines, in order, with justification, is L2.
- Relating the concept to another construct, or stating the purpose of the code, with a reason, is L3.
  A relational answer may be correct or a relational error.
- Locating and fixing the mistake for one given failing case is L3.
- Correct reasoning about code, an input or a change that is NOT in the given code (predicting the effect of a
  change, diagnosing a class of error, writing correct new code) is L4. New code must be correct to be L4.
- A student's question that makes no claim is not levelled: "none"."""

LABEL_SYSTEM = """You are an experienced Java teacher writing the reference level for one student answer on a 5-level
learning ladder (L0-L4). Use the level definitions and boundary rules given. Work out what the code really does
(its run output is given) and whether the student's reasoning is correct before you decide.
Mark the answer as a whole, for the main thing the question part asks.
Return JSON only: {"level":"L0|L1|L2|L3|L4|none","why":"<one or two sentences>"}"""

ADJ_SYSTEM = """You are the second examiner. Two markers gave different levels (A and B) to one student answer on a
5-level learning ladder (L0-L4). Using the level definitions and boundary rules given, decide the correct level.
You may pick A, B, or a different level if both are wrong. Work out what the code really does (its run output is given).
Return JSON only: {"level":"L0|L1|L2|L3|L4|none","pick":"A|B|other","why":"<one or two sentences>"}"""


def material(defs, question, code, run_output, answer) -> str:
    out = run_output if run_output else "(not run: no runnable code, or it needs input)"
    return (f"LEVEL DEFINITIONS:\n{defs}\n\n{BOUNDARIES}\n\nQUESTION (the part the student answers):\n{question}\n\n"
            f"CODE:\n{(code or '(none)')[:1500]}\n\nOUTPUT OF RUNNING THE CODE:\n{str(out)[:600]}\n\n"
            f"STUDENT ANSWER:\n{answer}\n")


def call(model: str, system: str, text: str) -> dict:
    CACHE.mkdir(parents=True, exist_ok=True)
    f = CACHE / (hashlib.sha256((model + system + text).encode("utf-8")).hexdigest()[:24] + ".json")
    if f.exists():
        return json.loads(f.read_text(encoding="utf-8"))
    exe = shutil.which("claude.cmd") or shutil.which("claude") or "claude"
    for wait in (0, 10, 30, 90):
        time.sleep(wait)
        try:
            with tempfile.TemporaryDirectory() as tmp:
                sp = Path(tmp) / "system.txt"
                sp.write_text(system, encoding="utf-8")
                r = subprocess.run([exe, "-p", "--output-format", "json", "--tools", "", "--no-session-persistence",
                                    "--model", model, "--system-prompt-file", str(sp)],
                                   input=text, capture_output=True, text=True, encoding="utf-8", cwd=tmp, timeout=600)
        except (OSError, subprocess.TimeoutExpired):
            continue
        if r.returncode == 0:
            txt = json.loads(r.stdout).get("result", "")
            m = re.search(r"\{.*\}", txt, re.S)
            try:
                out = json.loads(m.group(0)) if m else {"level": "none", "why": "unparsed"}
            except json.JSONDecodeError:
                out = {"level": "none", "why": "unparsed: " + txt[:200]}
            f.write_text(json.dumps(out, ensure_ascii=False), encoding="utf-8")
            return out
    return {"level": "none", "why": "unavailable", "unavailable": True}


def lv(x):
    return x if x in LEVELS else "none"


def kappa(a, b) -> float:
    n = len(a)
    po = sum(x == y for x, y in zip(a, b)) / n
    ca, cb = Counter(a), Counter(b)
    pe = sum(ca[c] * cb[c] for c in set(a) | set(b)) / (n * n)
    return (po - pe) / (1 - pe) if pe < 1 else 1.0


def pmap(fn, items, label):
    done = [0]

    def work(x):
        r = fn(x)
        done[0] += 1
        if done[0] % 25 == 0:
            print(f"  {label} {done[0]}/{len(items)}", flush=True)
        return r
    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        return list(pool.map(work, items))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", default="scenario_run_v10_all")
    ap.add_argument("--labeller", default="sonnet")
    ap.add_argument("--adjudicator", default="fable")
    args = ap.parse_args()
    questions, scenarios = load_scenarios()
    sysres = {s["id"]: s for s in json.loads((ROOT / "output" / args.run / "results.json").read_text(encoding="utf-8"))["scenarios"]}
    defs = level_definitions()
    rows = []
    for s in scenarios:
        q = questions.get(s["question"], {})
        asked = asked_part(q.get("question", ""), s["scenario_type"]) or q.get("question", "")
        rows.append({"id": s["id"], "type": s["scenario_type"], "text": s["text"],
                     "label": s["expected_level"],
                     "graph_label": GRAPH_KEY.get(s["id"], (s["expected_level"],))[0] if s["expected_level"] else None,
                     "system": lv(sysres[s["id"]]["max_level"]),
                     "material": material(defs, asked, q.get("code", ""), sysres[s["id"]].get("run_output"), s["text"])})

    # 1 — label
    marks = pmap(lambda r: call(args.labeller, LABEL_SYSTEM, r["material"] + "\nWrite the reference level."), rows, "labelled")
    for r, m in zip(rows, marks):
        r["labeller"], r["labeller_why"] = lv(m.get("level")), m.get("why", "")

    # 3 — adjudicate the disagreements (A / B in random order, blind to which is the classifier)
    rnd = random.Random(11)
    dis = [r for r in rows if r["labeller"] != r["system"]]
    for r in dis:
        r["a_is_system"] = rnd.random() < 0.5

    def adjudicate(r):
        a, b = (r["system"], r["labeller"]) if r["a_is_system"] else (r["labeller"], r["system"])
        return call(args.adjudicator, ADJ_SYSTEM, r["material"] + f"\nMARKER A: {a}\nMARKER B: {b}\n\nDecide the correct level.")
    adj = pmap(adjudicate, dis, "adjudicated")
    for r, m in zip(dis, adj):
        r["adjudicator"], r["adjudicator_why"] = lv(m.get("level")), m.get("why", "")
    for r in rows:
        r["reference"] = r.get("adjudicator") or r["labeller"]      # agreement stands; else the examiner decides

    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "labels.json").write_text(json.dumps([{k: v for k, v in r.items() if k != "material"} for r in rows],
                                                indent=1, ensure_ascii=False), encoding="utf-8")

    # 2 / 4 — validate on the 44, score on the 321
    lines = []
    lab = [r for r in rows if r["label"]]
    unl = [r for r in rows if not r["label"]]
    for who in ("labeller", "reference", "system"):
        lines.append(f"on the 44 human-labelled (graph-boundary key): {who:9s} exact "
                     f"{sum(r[who] == r['graph_label'] for r in lab)}/44")
    adj44 = [r for r in lab if "adjudicator" in r]
    lines.append(f"on the 44: the examiner settled {len(adj44)} disagreements, right on "
                 f"{sum(r['adjudicator'] == r['graph_label'] for r in adj44)}")
    lines.append(f"all 365: classifier and labeller agree on {sum(r['system'] == r['labeller'] for r in rows)}/365, "
                 f"kappa {kappa([r['system'] for r in rows], [r['labeller'] for r in rows]):.2f}")
    sides = Counter(("classifier" if r["adjudicator"] == r["system"] else "labeller" if r["adjudicator"] == r["labeller"]
                     else "neither") for r in dis)
    lines.append(f"disagreements: {len(dis)}; the examiner sided with {dict(sides)}")
    ex = sum(r["system"] == r["reference"] for r in unl)
    within = sum(r["system"] != "none" and r["reference"] != "none"
                 and abs(int(r["system"][1]) - int(r["reference"][1])) <= 1 for r in unl)
    lines.append(f"THE 321 UNLABELLED: classifier matches the reference level on {ex}/{len(unl)} ({ex / len(unl):.0%}), "
                 f"within one level {within}")
    allx = sum(r["system"] == (r["graph_label"] or r["reference"]) for r in rows)
    lines.append(f"ALL 365 (human label where there is one, else the reference): {allx}/365 ({allx / 365:.0%})")
    per, hit = Counter(r["reference"] for r in unl), Counter(r["reference"] for r in unl if r["system"] == r["reference"])
    lines.append("321 by reference level: " + "  ".join(f"{k} {hit[k]}/{per[k]}" for k in LEVELS + ["none"]))
    lines.append(f"calls unavailable: {sum(1 for m in marks + adj if m.get('unavailable'))}")
    print("\n".join(lines))
    (OUT / "summary.txt").write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()
