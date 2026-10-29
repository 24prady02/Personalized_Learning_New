"""Evaluate the classifier: the 20-scenario regression test and the held-out set.

* **Regression** (``data/scenarios_20_expected.json``): per scenario, the main
  concept, headline level and misconception against the accepted sets.
* **Held-out** (``data/heldout_365.json`` minus the regression ids): exact
  level and within-1 against the reference level, L0 precision / recall,
  false alarms (L0 on an answer the reference puts at L1+), main-concept
  accuracy on the hand-labelled answers, and the needs_review rate.
* **Lint**: fails if a module of ``src/lp_graph`` contains a scenario id or
  a literal question / answer string (no scenario-specific code).

    python scripts/evaluate_lp_graph.py [--only regression|heldout] [--jobs 4] [--tag name]

Writes ``output/eval/<tag>/{regression,heldout}.json`` and ``summary.txt``.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

LEVELS = ["L0", "L1", "L2", "L3", "L4"]
_KG = None


def _assess(row: dict) -> dict:
    global _KG
    from lp_graph.graph import KG
    from lp_graph.pipeline import assess

    if _KG is None:
        _KG = KG()
    try:
        a = assess(row["code"], row["question"], row["answer"], _KG)
        d = a.to_dict()
        return {"id": row["id"], "main": d.get("main_concept"), "level": d.get("headline_level"),
                "misconceptions": [m["id"] for m in d.get("misconceptions", []) if m.get("status") != "corrected"],
                "corrected": [m["id"] for m in d.get("misconceptions", []) if m.get("status") == "corrected"],
                "unlisted": bool(d.get("unlisted_errors")),
                "needs_review": d.get("needs_review"), "unmatched": [u["text"] for u in d.get("unmatched_statements", [])],
                "markdown": a.to_markdown(), "error": None}
    except Exception:  # a crash is a result
        import traceback
        return {"id": row["id"], "main": None, "level": "error", "misconceptions": [], "corrected": [],
                "unlisted": False, "needs_review": None, "unmatched": [], "markdown": "", "error": traceback.format_exc()}


def run_all(rows: list[dict], jobs: int) -> list[dict]:
    if jobs <= 1:
        return [_assess(r) for r in rows]
    with ProcessPoolExecutor(jobs) as ex:
        return list(ex.map(_assess, rows, chunksize=4))


def lint(rows: list[dict]) -> list[str]:
    problems = []
    texts = {r["id"]: [t for t in (r["question"], r["answer"]) if len(t.strip()) >= 25] for r in rows}
    for f in sorted((ROOT / "src" / "lp_graph").glob("*.py")):
        src = f.read_text(encoding="utf-8")
        for m in re.finditer(r"\bS\d{3}\b", src):
            problems.append(f"{f.name}: scenario id {m.group(0)}")
        for sid, ts in texts.items():
            for t in ts:
                if t.strip()[:40] in src:
                    problems.append(f"{f.name}: literal text of {sid}")
    return sorted(set(problems))


def regression(jobs: int) -> tuple[list[dict], str]:
    spec = json.load(open(ROOT / "data" / "scenarios_20_expected.json", encoding="utf-8"))
    held = {r["id"]: r for r in json.load(open(ROOT / "data" / "heldout_365.json", encoding="utf-8"))["rows"]}
    rows = []
    for sid in spec["expected"]:
        src = spec["extra_inputs"].get(sid) or held[sid]
        rows.append({"id": sid, "code": src["code"], "question": src["question"], "answer": src["answer"]})
    res = run_all(rows, jobs)
    lines = [f"{'id':5} {'main ok':8} {'level ok':9} {'mis ok':7} {'got':52} expected"]
    score = {"main": 0, "level": 0, "mis": 0, "all": 0}
    for r in res:
        e = spec["expected"][r["id"]]
        main_ok = not e["main"] or r["main"] in e["main"]
        level_ok = r["level"] in e["level"]
        got_mis = set(r["misconceptions"]) | ({"WRONG_UNLISTED"} if r["unlisted"] and not r["misconceptions"] else set())
        want = set(e["misconception"])
        mis_ok = (not want and not r["misconceptions"]) or bool(want & got_mis)
        if e.get("corrected"):
            mis_ok = mis_ok and bool(set(e["corrected"]) & set(r["corrected"]))
        r.update(main_ok=main_ok, level_ok=level_ok, mis_ok=mis_ok)
        for k, v in (("main", main_ok), ("level", level_ok), ("mis", mis_ok), ("all", main_ok and level_ok and mis_ok)):
            score[k] += v
        got = f"{r['main']} {r['level']} {','.join(r['misconceptions']) or '-'}" + (
            f" (corrected {','.join(r['corrected'])})" if r["corrected"] else "")
        exp = f"{'/'.join(e['main']) or 'any'} {'/'.join(e['level'])} {'/'.join(e['misconception']) or '-'}"
        lines.append(f"{r['id']:5} {'yes' if main_ok else 'NO':8} {'yes' if level_ok else 'NO':9} {'yes' if mis_ok else 'NO':7} {got[:52]:52} {exp}")
    n = len(res)
    lines.append(f"\nregression: main {score['main']}/{n}, level {score['level']}/{n}, misconception {score['mis']}/{n}, all three {score['all']}/{n}")
    return res, "\n".join(lines)


def heldout(jobs: int) -> tuple[list[dict], str]:
    spec = json.load(open(ROOT / "data" / "scenarios_20_expected.json", encoding="utf-8"))
    rows = [r for r in json.load(open(ROOT / "data" / "heldout_365.json", encoding="utf-8"))["rows"]
            if r["id"] not in spec["expected"]]
    res = run_all(rows, jobs)
    by = {r["id"]: r for r in rows}
    exact = within = n = 0
    tp = fp = fn = 0
    review = errors = 0
    main_ok = main_n = 0
    human_exact = human_n = 0
    for r in res:
        ref = by[r["id"]]["reference"]
        got = r["level"]
        if got == "error":
            errors += 1
        if got == "needs_review" or r.get("needs_review"):
            review += 1
        if ref in LEVELS:
            n += 1
            exact += got == ref
            if got in LEVELS:
                within += abs(LEVELS.index(got) - LEVELS.index(ref)) <= 1
            tp += got == "L0" and ref == "L0"
            fp += got == "L0" and ref != "L0"
            fn += got != "L0" and ref == "L0"
        if by[r["id"]]["human"] in LEVELS:
            human_n += 1
            human_exact += got == by[r["id"]]["human"]
        if by[r["id"]]["gold_concepts"]:
            main_n += 1
            main_ok += r["main"] in by[r["id"]]["gold_concepts"]
    p = tp / (tp + fp) if tp + fp else 0.0
    rc = tp / (tp + fn) if tp + fn else 0.0
    text = (f"held-out: {len(res)} answers ({n} with a reference level L0-L4)\n"
            f"  exact level          {exact}/{n} = {exact / max(n, 1):.1%}\n"
            f"  within one level     {within}/{n} = {within / max(n, 1):.1%}\n"
            f"  L0 precision         {tp}/{tp + fp} = {p:.1%}\n"
            f"  L0 recall            {tp}/{tp + fn} = {rc:.1%}\n"
            f"  false alarms (L0 on reference L1+) {fp}\n"
            f"  human-labelled exact {human_exact}/{human_n}\n"
            f"  main concept (gold)  {main_ok}/{main_n}\n"
            f"  needs_review         {review}\n"
            f"  crashes              {errors}")
    return res, text


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", choices=["regression", "heldout"])
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--tag", default="latest")
    a = ap.parse_args()
    out = ROOT / "output" / "eval" / a.tag
    out.mkdir(parents=True, exist_ok=True)
    rows_all = json.load(open(ROOT / "data" / "heldout_365.json", encoding="utf-8"))["rows"]
    parts = []
    bad = lint(rows_all)
    parts.append("lint: " + ("ok" if not bad else "FAIL\n  " + "\n  ".join(bad)))
    if a.only in (None, "regression"):
        res, txt = regression(a.jobs)
        json.dump(res, open(out / "regression.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        parts.append(txt)
    if a.only in (None, "heldout"):
        res, txt = heldout(a.jobs)
        json.dump(res, open(out / "heldout.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        parts.append(txt)
    summary = "\n\n".join(parts)
    (out / "summary.txt").write_text(summary, encoding="utf-8")
    print(summary)
    if bad:
        sys.exit(1)


if __name__ == "__main__":
    main()
