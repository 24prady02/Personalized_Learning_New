"""
run_llm_judge_44.py — the sentence judge replaced by an LLM that reads the
graph's has_level edge logic (no new rules), on the 44 labelled scenarios.

For each answer:
  1. Concepts: the engine's linked concepts (+ the answer graph's best extra).
  2. Code run: the engine runs the code; what it confirmed or contradicted,
     and any misconception whose run gives the student's values, are given to
     the judge as facts.
  3. Judge (local LLM via Ollama, temperature 0): for each concept it gets the
     concept's L0-L4 ways from the graph (exact rules, boundaries, the L0
     everyday / wrong readings) and returns the way the answer shows, with a
     quote and whether the answer's statements are correct.
  4. Level: the judge's level; the code run overrules it (an inconsistent
     trace or a run-held misconception is L0).

Usage:
    python scripts/run_llm_judge_44.py --model qwen2.5:14b --tag qwen14
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
import time
from collections import Counter
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from check_steps_44 import GOLD  # noqa: E402
from run_student_scenarios import asked_part, load_scenarios  # noqa: E402
from src.lp_percpt import models  # noqa: E402
from src.lp_percpt.engine import LPPercptEngine  # noqa: E402

KG_RAW = json.loads((ROOT / "data" / "chapter1_kg.json").read_text(encoding="utf-8"))
EDGES = {(e["source"], e["level"]): e for e in KG_RAW["edges"] if e.get("type") == "has_level"}
LEVEL_NAMES = {"L0": "Prestructural", "L1": "Unistructural", "L2": "Multistructural",
               "L3": "Relational", "L4": "Extended abstract"}

SYSTEM = """You grade one student answer about Java on a 5-level learning ladder (L0-L4), for given concepts.
You are given, for each concept, the WAYS of reaching each level, taken from a knowledge graph. Use only them.
Rules:
- The level is the highest level whose way the answer actually shows, with correct content.
- L0 if the answer's reasoning states or uses a rule that contradicts Java (an everyday reading or a wrong rule listed under L0), even if it uses Java words. A wrong explanation is not L1-L4.
- L1: names the element or states one correct rule, not applied to this code.
- L2: applies the rules correctly to this code (values, trace, output). A bare result with no reasoning is L1.
- L3: correctly relates parts (why, purpose, relation to another concept) as the L3 ways say.
- L4: correctly reasons beyond the given code (a change, a new input, diagnosing an error, new code) as the L4 ways say.
- Respect each level's boundary text.
- FACTS FROM RUNNING THE CODE are certain: a value the run contradicts is wrong.
- If the answer says nothing about a concept, give "none".
Return JSON only: {"concepts":[{"concept":"<id>","level":"L0|L1|L2|L3|L4|none","way":"<way name>","quote":"<words from the answer>","correct":true|false,"why":"<one short sentence>"}]}"""


def ladder_text(cid: str) -> str:
    out = [f"### Concept: {cid}"]
    for lv in ("L0", "L1", "L2", "L3", "L4"):
        e = EDGES.get((cid, lv))
        if not e:
            continue
        out.append(f"{lv} {LEVEL_NAMES[lv]}:")
        bounds = []
        for w in e["ways"][:6 if lv == "L0" else 4]:
            if w["way"] == "inconsistent_trace":
                continue
            rule = re.sub(r"\s+", " ", w.get("exact_rule", ""))
            if lv == "L0":
                rule = rule.split("Right rule:")[0].split("Java rule:")[0].split("In Java,")[0]
            out.append(f"  - {w['way']}: {rule[:230]}")
            b = w.get("boundary", "")
            if b and b not in bounds:
                bounds.append(b)
        for b in bounds[:2]:
            out.append(f"  boundary: {b[:200]}")
    return "\n".join(out)


def run_facts(result) -> list:
    facts = []
    for c in result["concepts"]:
        for it in c["evidence"]:
            st = it["statement"]
            if st.startswith("confirmed by the run"):
                facts.append(f"CORRECT ({it['clause'][:80]!r}): {st}")
            elif it["check"] == "wrong_trace":
                facts.append(f"WRONG ({it['clause'][:80]!r}): {st}")
            elif it["check"] == "held" and "match a run" in st:
                facts.append(f"MISCONCEPTION: {st}")
    return list(dict.fromkeys(facts))


def judge(model: str, prompt: str) -> dict:
    r = requests.post("http://localhost:11434/api/chat", timeout=900, json={
        "model": model, "stream": False, "format": "json",
        "options": {"temperature": 0, "num_ctx": 8192, "seed": 1},
        "messages": [{"role": "system", "content": SYSTEM}, {"role": "user", "content": prompt}]})
    r.raise_for_status()
    txt = r.json()["message"]["content"]
    try:
        return json.loads(txt)
    except Exception:
        m = re.search(r"\{.*\}", txt, re.S)
        return json.loads(m.group(0)) if m else {"concepts": []}


def extra_concept(text: str, kg, have) -> list:
    """The concept whose way rules are closest to the answer (answer-graph candidate)."""
    rules, owner = [], []
    for cid, c in kg.concepts.items():
        for lv in ("L1", "L2", "L3", "L4"):
            for w in c.ways.get(lv, []):
                for r in w.rules:
                    rules.append(r); owner.append(cid)
    sim = models.similarity([text], rules)[0]
    for j in sim.argsort()[::-1]:
        if owner[j] not in have:
            return [owner[j]]
    return []


def prepare(out: Path) -> None:
    """Write one blind prompt per answer (no expected level) and the run metadata."""
    eng = LPPercptEngine(store_dir=out / "students", map_dir=None, review_log=None)
    kg = eng.kg
    questions, scenarios = load_scenarios()
    (out / "prompts").mkdir(parents=True, exist_ok=True)
    (out / "judgements").mkdir(exist_ok=True)
    meta = {}
    for s in [s for s in scenarios if s["expected_level"]]:
        q = questions.get(s["question"], {})
        asked = asked_part(q.get("question", ""), s["scenario_type"])
        shown = f"{q.get('source') or ''}\n{q.get('question', '')}\n{q.get('code', '')}"
        r = eng.process(s["id"], s["text"], code=q.get("code", ""), shown_text=shown, session_id="j", asked=asked)
        linked = [c["concept"] for c in r["concepts"]]
        concepts = linked + extra_concept(s["text"], kg, set(linked))
        facts = run_facts(r)
        prompt = (SYSTEM + "\n\n---\n\n"
                  f"QUESTION (part asked): {asked or q.get('question', '')}\n\nCODE:\n{(q.get('code') or '(none)')[:1500]}\n\n"
                  f"STUDENT ANSWER: {s['text']}\n\nFACTS FROM RUNNING THE CODE:\n"
                  + ("\n".join(facts) if facts else "(no claim of the answer could be checked by running the code)")
                  + "\n\nCONCEPTS AND THEIR WAYS:\n\n" + "\n\n".join(ladder_text(c) for c in concepts)
                  + f"\n\nGrade the answer for each concept: {', '.join(concepts)}.")
        (out / "prompts" / f"{s['id']}.txt").write_text(prompt, encoding="utf-8")
        override = [c["concept"] for c in r["concepts"]
                    if "inconsistent_trace" in (c.get("prompt_reason") or "")
                    or any(it["check"] == "held" and "match a run" in it["statement"] for it in c["evidence"])]
        meta[s["id"]] = {"expected": s["expected_level"], "text": s["text"], "asked": asked, "concepts": concepts,
                         "facts": facts, "run_l0": override, "gold": sorted(GOLD[s["id"]])}
        print(s["id"], concepts, flush=True)
    (out.parent / f"{out.name}_meta.json").write_text(json.dumps(meta, indent=1, ensure_ascii=False), encoding="utf-8")


def score(out: Path, label: str) -> None:
    meta = json.loads((out.parent / f"{out.name}_meta.json").read_text(encoding="utf-8"))
    rows = []
    for sid, m in meta.items():
        f = out / "judgements" / f"{sid}.json"
        j = json.loads(f.read_text(encoding="utf-8")) if f.exists() else {"concepts": []}
        levels = {}
        for item in j.get("concepts", []):
            cid, lv = item.get("concept"), str(item.get("level", "none"))
            if cid in m["concepts"] and lv in ("L0", "L1", "L2", "L3", "L4"):
                levels[cid] = lv
        final = dict(levels)
        for cid in m["run_l0"]:                    # the code run overrules the judge
            final[cid] = "L0"
        rows.append({"id": sid, **m, "judge": j, "levels": levels, "final": final,
                     "best_judge": max(levels.values()) if levels else None,
                     "best": max(final.values()) if final else None})
    (out / "results.json").write_text(json.dumps(rows, indent=1, ensure_ascii=False), encoding="utf-8")
    lines = []
    for key in ("best_judge", "best"):
        b = [r[key] for r in rows]
        exact = sum(x == r["expected"] for x, r in zip(b, rows))
        within = sum(x is not None and abs(int(x[1]) - int(r["expected"][1])) <= 1 for x, r in zip(b, rows))
        mae = sum(abs(int((x or "L1")[1]) - int(r["expected"][1])) for x, r in zip(b, rows)) / len(rows)
        per = Counter(r["expected"] for r in rows)
        hit = Counter(r["expected"] for x, r in zip(b, rows) if x == r["expected"])
        over = sum(x is not None and x > r["expected"] for x, r in zip(b, rows))
        under = sum(x is None or x < r["expected"] for x, r in zip(b, rows))
        lv_of = "final" if key == "best" else "levels"
        gold_lv = sum(any(r[lv_of].get(c) == r["expected"] for c in r["gold"]) for r in rows)
        line = (f"{label} {key}: exact {exact}/{len(rows)}, within-1 {within}, MAE {mae:.2f}, too high {over}, too low {under}, "
                f"per level { {k: f'{hit[k]}/{per[k]}' for k in sorted(per)} }, right level on right concept {gold_lv}/{len(rows)}")
        print(line); lines.append(line)
    for r in rows:
        print(r["id"], r["expected"], "->", r["best"], "OK" if r["best"] == r["expected"] else "XX", r["final"])
    (out / "summary.txt").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="qwen2.5:14b")
    ap.add_argument("--tag", default="qwen14")
    ap.add_argument("--prepare", action="store_true", help="write blind prompts for an outside judge")
    ap.add_argument("--score", action="store_true", help="score judgements/<id>.json written by the judge")
    args = ap.parse_args()
    out = ROOT / "output" / f"llm_judge_{args.tag}"
    if args.prepare:
        if out.exists():
            shutil.rmtree(out)
        prepare(out)
        return
    if args.score:
        score(out, args.tag)
        return
    out = ROOT / "output" / f"llm_judge_{args.tag}"
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    eng = LPPercptEngine(store_dir=out / "students", map_dir=None, review_log=None)
    kg = eng.kg
    questions, scenarios = load_scenarios()
    rows = []
    t0 = time.time()
    for s in [s for s in scenarios if s["expected_level"]]:
        q = questions.get(s["question"], {})
        asked = asked_part(q.get("question", ""), s["scenario_type"])
        shown = f"{q.get('source') or ''}\n{q.get('question', '')}\n{q.get('code', '')}"
        r = eng.process(s["id"], s["text"], code=q.get("code", ""), shown_text=shown, session_id="j", asked=asked)
        linked = [c["concept"] for c in r["concepts"]]
        concepts = linked + extra_concept(s["text"], kg, set(linked))
        facts = run_facts(r)
        prompt = (f"QUESTION (part asked): {asked or q.get('question', '')}\n\nCODE:\n{(q.get('code') or '(none)')[:1500]}\n\n"
                  f"STUDENT ANSWER: {s['text']}\n\nFACTS FROM RUNNING THE CODE:\n"
                  + ("\n".join(facts) if facts else "(no claim of the answer could be checked by running the code)")
                  + "\n\nCONCEPTS AND THEIR WAYS:\n\n" + "\n\n".join(ladder_text(c) for c in concepts)
                  + f"\n\nGrade the answer for each concept: {', '.join(concepts)}.")
        j = judge(args.model, prompt)
        levels, why = {}, {}
        for item in j.get("concepts", []):
            cid, lv = item.get("concept"), str(item.get("level", "none"))
            if cid in concepts and lv in ("L0", "L1", "L2", "L3", "L4"):
                levels[cid], why[cid] = lv, item
        # the code run overrules the judge
        final = dict(levels)
        for c in r["concepts"]:
            if "inconsistent_trace" in (c.get("prompt_reason") or "") or any(
                    it["check"] == "held" and "match a run" in it["statement"] for it in c["evidence"]):
                final[c["concept"]] = "L0"
        row = {"id": s["id"], "expected": s["expected_level"], "text": s["text"], "asked": asked,
               "concepts": concepts, "facts": facts, "judge": j, "levels": levels, "final": final,
               "best_judge": max(levels.values()) if levels else None,
               "best": max(final.values()) if final else None, "gold": sorted(GOLD[s["id"]])}
        rows.append(row)
        print(s["id"], s["expected_level"], "->", row["best"], final, f"{time.time() - t0:.0f}s", flush=True)

    (out / "results.json").write_text(json.dumps(rows, indent=1, ensure_ascii=False), encoding="utf-8")
    for key in ("best_judge", "best"):
        b = [r[key] for r in rows]
        exact = sum(x == r["expected"] for x, r in zip(b, rows))
        within = sum(x is not None and abs(int(x[1]) - int(r["expected"][1])) <= 1 for x, r in zip(b, rows))
        mae = sum(abs(int((x or "L1")[1]) - int(r["expected"][1])) for x, r in zip(b, rows)) / len(rows)
        per = Counter(r["expected"] for r in rows)
        hit = Counter(r["expected"] for x, r in zip(b, rows) if x == r["expected"])
        over = sum(x is not None and x > r["expected"] for x, r in zip(b, rows))
        gold_lv = sum(any(r["final" if key == "best" else "levels"].get(c) == r["expected"] for c in r["gold"]) for r in rows)
        line = (f"{args.model} {key}: exact {exact}/44, within-1 {within}, MAE {mae:.2f}, too high {over}, "
                f"per level { {k: f'{hit[k]}/{per[k]}' for k in sorted(per)} }, right level on right concept {gold_lv}/44")
        print(line)
        with open(out / "summary.txt", "a", encoding="utf-8") as fh:
            fh.write(line + "\n")


if __name__ == "__main__":
    main()
