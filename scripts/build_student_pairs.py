"""NLI pairs in student wording, labelled by running the code (no human labels).

For every answer of the non-gold set whose question falls in the training
split (a hash of the question text), and every answer statement with a claim
the code can check:

* the real run confirms the claim and a misconception's misread run
  contradicts it -> the statement agrees with the misconception's correct rule
  (entailment) and contradicts its wrong belief (contradiction);
* the real run contradicts the claim and the misread run confirms it -> the
  statement agrees with the wrong belief and contradicts the correct rule.

Premise = the misconception edge's text (twin_logic / logic), hypothesis = the
student statement. Only misconceptions of the answer's candidate concepts
whose misinterpreter changes the run are used.

    python scripts/build_student_pairs.py   -> data/student_pairs.json (+ data/question_split.json)
"""

from __future__ import annotations

import hashlib
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
os.environ.setdefault("LP_GRAPH_EDGE_NLI", "0")

from lp_graph import claims  # noqa: E402
from lp_graph.graph import KG  # noqa: E402
from lp_graph.pipeline import assess  # noqa: E402

EVAL_SHARE = 0.3


def split_of(question: str) -> str:
    h = int(hashlib.sha1((question or "").strip().lower().encode()).hexdigest(), 16)
    return "eval" if (h % 1000) / 1000 < EVAL_SHARE else "train"


def main() -> int:
    kg = KG()
    gold = set(json.load(open(ROOT / "data" / "scenarios_20_expected.json", encoding="utf-8"))["expected"])
    rows = [r for r in json.load(open(ROOT / "data" / "heldout_365.json", encoding="utf-8"))["rows"]
            if r["id"] not in gold]
    split = {r["id"]: split_of(r["question"]) for r in rows}
    json.dump(split, open(ROOT / "data" / "question_split.json", "w", encoding="utf-8"), indent=0)
    pairs: list[dict] = []
    seen: set[tuple] = set()
    for r in rows:
        try:
            a = assess(r["code"], r["question"], r["answer"], kg)
        except Exception:  # an answer that crashes the pipeline gives no pairs
            continue
        mis_edges = [m for m in a.candidates.mis_edges if m.wrong and m.right]
        for st in a.statements:
            if st.source not in ("answer", "answer_code") or st.hypothetical:
                continue
            if st.source == "answer_code":
                real, mutants = a.trace.answer_run, a.trace.answer_mutants
            else:
                real, mutants = a.trace.run, a.trace.mutants
            if real is None or a.trace.sampled or a.trace.reads_input:
                continue
            for m in mis_edges:
                mut = mutants.get(m.mis)
                if mut is None:
                    continue
                for s in st.slots:
                    if s.implied or s.hypothetical or s.name not in claims.CHECKABLE or s.name == "expr":
                        continue
                    vr, vm = claims.check(s, real), claims.check(s, mut)
                    if vr is True and vm is False:
                        labels = ((m.right, 1), (m.wrong, 0))
                    elif vr is False and vm is True:
                        labels = ((m.wrong, 1), (m.right, 0))
                    else:
                        continue
                    for premise, label in labels:
                        key = (premise, st.text, label)
                        if key in seen:
                            continue
                        seen.add(key)
                        pairs.append({"premise": premise, "hypothesis": st.text, "label": label,
                                      "concept": m.concept, "kind": "student_" + ("right" if label == 1 and premise == m.right
                                                                                   else "wrong" if label == 1 else "contra"),
                                      "answer": r["id"], "split": split[r["id"]]})
    json.dump(pairs, open(ROOT / "data" / "student_pairs.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    from collections import Counter
    print("answers", len(rows), "| split", Counter(split.values()))
    print("student pairs", len(pairs), "| by split/label", sorted(Counter((p["split"], p["label"]) for p in pairs).items()))
    print("answers contributing", len({p["answer"] for p in pairs}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
