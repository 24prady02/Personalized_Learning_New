"""NLI training pairs from the 345 non-gold answers, weakly labelled by their
reference level and the graph (no hand labels, no LLM, no code run; the 19
gold scenarios are never used).

Premise = one student sentence; hypothesis = one claim clause of an edge
logic of a concept the sentence touches (conceptnli.sentences). Labels
(0 contradiction, 1 entailment, 2 neutral = not entailed):

reliable
* reference L1+ (no misconception held): every wrong-belief clause the
  sentence shares an anchor with -> 2;
* reference Lk: the main concept's way clauses above Lk -> 2;
* reference L1 / L2: the main concept's relation-edge logic -> 2;
weak (pseudo-labels from the off-the-shelf NLI model, constrained by the
reference level)
* reference L0: the wrong-belief clause the sentence entails best (>= 0.5)
  -> 1, the clauses of that misconception's correct rule -> 2;
* reference Lk (k >= 1): the main concept's way clause at Lk the sentences
  entail best (>= 0.5) -> 1;
* reference L3: the logic of a relation edge to a neighbour the L3 ways
  require, if entailed (>= 0.5) -> 1.

Split by question (data/question_split.json): ``train`` / ``eval``.

    python scripts/build_answer_pairs.py   -> data/answer_pairs.json
"""

from __future__ import annotations

import json
import os
import random
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
os.environ.update({"LP_GRAPH_RUN_CODE": "0", "LP_GRAPH_EDGE_NLI": "0", "LP_GRAPH_MEANING": "0",
                   "LP_GRAPH_PCST": "0"})

from lp_graph import conceptnli  # noqa: E402
from lp_graph.edgelogic import reader_for  # noqa: E402
from lp_graph.graph import KG  # noqa: E402
from lp_graph.pipeline import assess  # noqa: E402

LEVELS = ("L1", "L2", "L3", "L4")
CAP = 3          # hypotheses of one kind per sentence (by TF-IDF score)


def split_of(question: str) -> str:
    import hashlib

    h = int(hashlib.sha1((question or "").strip().lower().encode()).hexdigest(), 16)
    return "eval" if (h % 1000) / 1000 < 0.3 else "train"


def main() -> int:
    kg = KG()
    logic = reader_for(kg)
    gold = set(json.load(open(ROOT / "data" / "scenarios_20_expected.json", encoding="utf-8"))["expected"])
    rows = [r for r in json.load(open(ROOT / "data" / "heldout_365.json", encoding="utf-8"))["rows"]
            if r["id"] not in gold and r["reference"] in ("L0", "L1", "L2", "L3", "L4")]
    pairs: list[dict] = []
    seen: set[tuple] = set()

    def add(prem: str, hyp: str, label: int, kind: str, r: dict) -> None:
        key = (prem, hyp)
        if key in seen:
            return
        seen.add(key)
        pairs.append({"premise": prem, "hypothesis": hyp, "label": label, "kind": kind,
                      "answer": r["id"], "split": split_of(r["question"])})

    for n, r in enumerate(rows):
        try:
            a = assess(r["code"], r["question"], r["answer"], kg)
        except Exception:
            continue
        ref = r["reference"]
        k = 0 if ref == "L0" else int(ref[1])
        main = a.candidates.main_concept
        sents = [s for s in a.statements if s.source == "answer" and len(s.text.split()) >= 3]
        cset = set(a.candidates.concepts)
        for s in sents:
            vs = tuple(s.variables)
            for c in sorted(set(s.concepts) & cset):
                mis = [m for m in kg.mis_edges.get(c, []) if m.wrong and m.right
                       and logic.score(s.text, m.wrong, vs) > 0]
                mis = sorted(mis, key=lambda m: -logic.score(s.text, m.wrong, vs))[:CAP]
                if k >= 1:
                    for m in mis:
                        for h in conceptnli.sentences(m.wrong):
                            add(s.text, h, 2, "wrong_not_held", r)
                elif mis:
                    clauses = [(m, h) for m in mis for h in conceptnli.sentences(m.wrong)]
                    res = conceptnli.test(s.text, [h for _, h in clauses])
                    best = max(range(len(clauses)), key=lambda i: res[i][0])
                    if res[best][0] >= 0.5:
                        m, h = clauses[best]
                        add(s.text, h, 1, "wrong_held", r)
                        for h2 in conceptnli.sentences(m.right):
                            add(s.text, h2, 2, "right_not_held", r)
            if main not in s.concepts:
                continue
            # levels of the main concept
            for i, lv in enumerate(LEVELS, start=1):
                ways = [w.text for w in kg.ways(main, lv) if w.text]
                clauses = sorted({h for w in ways for h in conceptnli.sentences(w)},
                                 key=lambda h: -logic.score(s.text, h, vs))[:CAP]
                if i > k:
                    for h in clauses:
                        if logic.score(s.text, h, vs) > 0:
                            add(s.text, h, 2, "way_above_level", r)
                elif i == k and clauses:
                    res = conceptnli.test(s.text, clauses)
                    j = max(range(len(clauses)), key=lambda x: res[x][0])
                    if res[j][0] >= 0.5:
                        add(s.text, clauses[j], 1, "way_at_level", r)
            # relation edges of the main concept to a concept the sentence touches
            needs = {x for row in kg.parts["ways"].get(main, {}).get("L3", []) for x in row["requires"]}
            for e in a.candidates.relation_edges:
                if not e.touches(main) or e.other(main) not in s.concepts or not e.logic:
                    continue
                clauses = conceptnli.sentences(e.logic)
                if k in (1, 2):
                    for h in clauses:
                        add(s.text, h, 2, "relation_not_stated", r)
                elif k == 3 and e.other(main) in needs and clauses:
                    res = conceptnli.test(s.text, clauses)
                    j = max(range(len(clauses)), key=lambda x: res[x][0])
                    if res[j][0] >= 0.5:
                        add(s.text, clauses[j], 1, "relation_stated", r)
        if (n + 1) % 25 == 0:
            print(f"{n + 1}/{len(rows)} answers, {len(pairs)} pairs", flush=True)

    # keep the not-entailed pairs at most twice the entailed ones (per split)
    random.seed(7)
    out = []
    for sp in ("train", "eval"):
        pos = [p for p in pairs if p["split"] == sp and p["label"] != 2]
        neg = [p for p in pairs if p["split"] == sp and p["label"] == 2]
        random.shuffle(neg)
        out += pos + neg[: max(2 * len(pos), 200)]
    json.dump(out, open(ROOT / "data" / "answer_pairs.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    print("answers", len(rows), "| pairs kept", len(out))
    print(sorted(Counter((p["split"], p["kind"], p["label"]) for p in out).items()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
