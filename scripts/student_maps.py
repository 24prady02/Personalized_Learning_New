"""Trace each student's concept map from the graph's edge logic.

Nodes: the concepts the assessment places at a level (or holds a
misconception on), with that level and misconception. Edges: every relation
edge (prerequisite / parallel) of the graph between two of those nodes, with a
status read from its edge logic:

* mentioned - one answer sentence involves both concepts (the edge is traced);
* stated    - that sentence reads as the edge's logic (edge reading MATCH)
              and links the two with a reason word (because, so, since ...);
* grounded  - stated, and the same sentence makes a claim the run confirms;
* broken    - the assessment breaks it (a held misconception or a claim the
              run contradicts at an endpoint).

Compared with the gold key's edges (only for scoring). Run with execution on
and the original pipeline (ES-Viterbi):

    python scripts/student_maps.py   -> output/student_maps.json + summary
"""

from __future__ import annotations

import json
import os
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))

from evaluate_gold import parse_gold  # noqa: E402
from lp_graph.edgelogic import reader_for  # noqa: E402
from lp_graph.graph import KG  # noqa: E402
from lp_graph.pipeline import assess  # noqa: E402

REASON = {"because", "so", "since", "therefore", "means", "which", "thus", "hence", "as", "when", "then", "if"}
RANK = {"mentioned": 1, "stated": 2, "grounded": 3}


def trace(kg: KG, a) -> dict:
    nodes = {c: {"level": r.level, "misconception": r.misconception}
             for c, r in a.levels.items() if r.level != "none"}
    answer = [s for s in a.statements if s.source in ("answer", "answer_code")]
    stated = {(r["id"], r["statement"]) for r in a.readings
              if r["kind"] == "edge" and r["label"].startswith("MATCH")
              and str(r.get("evidence", "")).startswith(("states the edge logic", "NLI"))}
    stated |= {(st.state.edge, sid) for st in a.route_student.steps if st.state.kind == "E"
               and str(st.reading.evidence).startswith("states the edge logic") for sid in st.statements}
    grounded_sids = {r["statement"] for r in a.readings if r["kind"] == "concept"
                     and r["label"].startswith("MATCH") and r.get("class") in ("run", "relation", "hypothetical", "diagnosis")}
    broken = {b["edge"] for b in a.comparison.broken}
    # an answer sentence is split into clauses (statements); a relation is
    # traced across the clauses of one sentence of one turn
    sentence: dict[tuple[int, int], list] = {}
    for s in answer:
        sentence.setdefault((s.turn, s.sentence), []).append(s)
    units = []
    for group in sentence.values():
        units.append((set().union(*(set(s.concepts) for s in group)), group))
    held = {c: n["misconception"] for c, n in nodes.items() if n["level"] == "L0"}
    code_edges = {e.id for e in a.candidates.relation_edges}
    logic = reader_for(kg)

    def contradicts(c: str, e) -> bool:
        """The held misconception of c is about this edge: its wrong belief or
        its correct rule reads as the edge's logic (graph texts only)."""
        name = held.get(c)
        for m in kg.mis_edges.get(c, []):
            if (name is None or m.mis == name) and m.wrong and e.logic:
                if max(logic.score(m.wrong, e.logic), logic.score(m.right or "", e.logic)) >= logic.match:
                    return True
        return False

    # fix 1: a claim the run confirms about a code line grounds the graph
    # edges between the concepts that line combines
    code = [s for s in a.statements if s.source == "code"]
    line_edges: dict[str, str] = {}
    for s in answer:
        if s.id not in grounded_sids:
            continue
        for cs_ in code:
            shared_vars = set(s.variables) & set(cs_.variables)
            if not shared_vars and len(set(s.concepts) & set(cs_.concepts)) < 2:
                continue
            for x in cs_.concepts:
                for y in cs_.concepts:
                    if x < y:
                        for eid2 in kg.rel_by_concept.get(x, []):
                            e2 = kg.relation_edges[eid2]
                            if e2.other(x) == y:
                                line_edges.setdefault(eid2, f"run confirms: {s.text[:60]} | line: {cs_.text[:40]}")
    edges = {}
    for eid, e in kg.relation_edges.items():
        # fix 3: a held misconception breaks only the edges whose logic it is
        # about, also towards a concept of the code the student does not reach
        if eid in broken or (eid in code_edges and any(c in held and contradicts(c, e) for c in (e.src, e.dst))):
            edges[eid] = {"status": "broken", "kind": e.kind, "logic": e.logic,
                          "evidence": "a held misconception or a run-contradicted claim at an endpoint"}
            continue
        if eid in line_edges:
            for c in (e.src, e.dst):
                nodes.setdefault(c, {"level": "used (not named)", "misconception": None})
            edges[eid] = {"status": "grounded", "kind": e.kind, "logic": e.logic, "evidence": line_edges[eid]}
            continue
        if e.src not in nodes or e.dst not in nodes:
            continue
        status, why = None, ""
        for cs, group in units:
            if not {e.src, e.dst} <= cs:
                continue
            s = max(group, key=lambda x: ((e.id, x.id) in stated, x.id in grounded_sids))
            s_text = " ".join(x.text for x in group)
            s_links = any(x.link_words for x in group)
            s_stated = any((eid, x.id) in stated for x in group)
            s_grounded = any(x.id in grounded_sids for x in group)
            words = {w.strip(".,;:!?()").lower() for w in s_text.split()}
            st = "mentioned"
            if s_stated and (words & REASON or s_links):
                st = "grounded" if s_grounded else "stated"
            if status is None or RANK[st] > RANK[status]:
                status, why = st, s_text[:90]
        if status:
            edges[eid] = {"status": status, "kind": e.kind, "logic": e.logic, "evidence": why}
    return {"nodes": nodes, "edges": edges}


def main() -> int:
    kg = KG()
    gold = parse_gold(ROOT / "data" / "gold_19.md")
    rows = {r["id"]: r for r in json.load(open(ROOT / "data" / "heldout_365.json", encoding="utf-8"))["rows"]}
    maps, tally = {}, Counter()
    for sid in gold:
        r = rows[sid]
        a = assess(r["code"], r["question"], r["answer"], kg)
        m = trace(kg, a)
        maps[sid] = m
        print(f"\n== {sid}  ({a.headline_level})  {r['answer'][:110]!r}")
        for c, n in m["nodes"].items():
            print(f"   [{c}] {n['level']}" + (f"  misconception={n['misconception']}" if n["misconception"] else ""))
        for eid, e in sorted(m["edges"].items(), key=lambda x: -RANK.get(x[1]["status"], 4)):
            print(f"   {e['status']:9} {eid}")
        for eid, want in gold[sid]["edges"].items():
            got = m["edges"].get(eid, {}).get("status", "absent")
            if want == "confirmed":
                tally["gold confirmed"] += 1
                tally["  ...traced (mentioned or better)"] += got in ("mentioned", "stated", "grounded")
                tally["  ...stated or grounded"] += got in ("stated", "grounded")
            elif want == "broken":
                tally["gold broken"] += 1
                tally["  ...broken"] += got == "broken"
            mark = "ok" if (want == "confirmed" and got in RANK) or (want == got) else ("-" if want == "context" else "NO")
            print(f"     gold {want:9} {eid:50} got {got:9} {mark}")
    for c, n in maps.items():
        tally["edges in maps"] += len(n["edges"])
        for e in n["edges"].values():
            tally["  status " + e["status"]] += 1
    (ROOT / "output").mkdir(exist_ok=True)
    name = os.environ.get("LP_MAPS_TAG", "student_maps")
    json.dump(maps, open(ROOT / "output" / f"{name}.json", "w", encoding="utf-8"), indent=1)
    print("\n==== summary")
    for k, v in tally.items():
        print(f"{k:40} {v}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
