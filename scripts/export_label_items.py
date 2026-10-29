"""Export the items Claude labels offline: for each of the 345 non-gold answers,
the candidate edges the graph gives for the concepts found.

Per answer (one JSON line in data/label_items.jsonl):
* question, code, answer and its sentences (s1, s2 ...);
* items, each with an id, a kind and the edge-logic text to judge:
  - "relation": a prerequisite / parallel edge between two concepts the answer
    touches (its logic);
  - "wrong" / "right": a misconception edge of a concept the answer touches
    (the wrong belief and its correct rule), retrieved by TF-IDF;
  - "way": a level way (L1..L4) of the main concept.

The 19 gold scenarios are left out. Nothing is labelled here.

    python scripts/export_label_items.py
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
os.environ.update({"LP_GRAPH_RUN_CODE": "0", "LP_GRAPH_EDGE_NLI": "0", "LP_GRAPH_MEANING": "0",
                   "LP_GRAPH_PCST": "0"})

from lp_graph.edgelogic import reader_for  # noqa: E402
from lp_graph.graph import KG  # noqa: E402
from lp_graph.pipeline import assess  # noqa: E402

MAX_REL, MAX_MIS, MAX_WAYS = 12, 8, 16


def main() -> int:
    kg = KG()
    logic = reader_for(kg)
    gold = set(json.load(open(ROOT / "data" / "scenarios_20_expected.json", encoding="utf-8"))["expected"])
    rows = [r for r in json.load(open(ROOT / "data" / "heldout_365.json", encoding="utf-8"))["rows"]
            if r["id"] not in gold]
    out_path = ROOT / "data" / "label_items.jsonl"
    done = set()
    if out_path.exists():
        done = {json.loads(line)["id"] for line in out_path.read_text(encoding="utf-8").splitlines() if line.strip()}
    n_items = 0
    with open(out_path, "a", encoding="utf-8") as fh:
        for n, r in enumerate(rows):
            if r["id"] in done:
                continue
            try:
                a = assess(r["code"], r["question"], r["answer"], kg)
            except Exception as exc:  # keep going; the answer is listed without items
                a = None
                print(r["id"], "assess failed:", exc, flush=True)
            sents = [s for s in (a.statements if a else []) if s.source in ("answer", "answer_code")]
            touched = set().union(*(set(s.concepts) for s in sents)) if sents else set()
            cset = set(a.candidates.concepts) & touched if a else set()
            items = []
            if a:
                rel = [e for e in a.candidates.relation_edges if e.src in cset and e.dst in cset and e.logic]
                for e in rel[:MAX_REL]:
                    items.append({"id": f"R{len(items)}", "kind": "relation", "edge": e.id, "text": e.logic})
                mis = [m for c in sorted(cset) for m in kg.mis_edges.get(c, []) if m.wrong and m.right]
                mis = sorted(mis, key=lambda m: -logic.score(r["answer"], m.wrong + " " + m.right))
                seen = set()
                for m in mis:
                    if m.mis in seen or len(seen) >= MAX_MIS:
                        continue
                    seen.add(m.mis)
                    items.append({"id": f"W{len(items)}", "kind": "wrong", "edge": m.id, "mis": m.mis, "text": m.wrong})
                    items.append({"id": f"C{len(items)}", "kind": "right", "edge": m.id, "mis": m.mis, "text": m.right})
                main = a.candidates.main_concept
                if main:
                    ways = [(lv, w.text) for lv in ("L1", "L2", "L3", "L4") for w in kg.ways(main, lv) if w.text]
                    for lv, txt in ways[:MAX_WAYS]:
                        items.append({"id": f"V{len(items)}", "kind": "way", "concept": main, "level": lv, "text": txt})
            rec = {"id": r["id"], "reference": r["reference"], "question": r["question"], "code": r["code"],
                   "answer": r["answer"], "main": a.candidates.main_concept if a else None,
                   "sentences": {s.id: s.text for s in sents}, "items": items}
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
            fh.flush()
            n_items += len(items)
            if (n + 1) % 25 == 0:
                print(f"{n + 1}/{len(rows)} answers, {n_items} items", flush=True)
    total = [json.loads(x) for x in out_path.read_text(encoding="utf-8").splitlines() if x.strip()]
    print("answers", len(total), "| items", sum(len(x["items"]) for x in total))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
