"""Step 7 - ``assess(code, question, answer, kg)``: the whole pipeline, no LLM.

1. split code / question / answer into statements (``statements``);
2. Personalized PageRank -> candidate concepts, edges, misconceptions
   (``candidates``);
3. the reader compares statements with candidate elements (``reader``);
4. ES-Viterbi twice: code + question -> correct route, answer -> student
   route (``viterbi``);
5. compare the routes (``compare``);
6. level per concept, root cause, consistency (``levels``);
7. ``Assessment.to_dict()`` (JSON) and ``to_markdown()`` (readable trace).

Deterministic: every list is sorted or kept in statement order and every
tie is broken by id.
"""

from __future__ import annotations

from dataclasses import dataclass, field


from .candidates import Candidates, select
from .compare import Comparison, compare_routes
from .execution import Trace, Tracer
from .graph import KG
from .levels import LevelResult, RootCause, compute_levels, root_causes
from .reader import CONTRADICT, CONTRADICT_RIGHT, MATCH_WRONG, NO, Reader, Segment
from .statements import (Statement, answer_statements, code_context, code_statements,
                         question_statements)
from .viterbi import ESViterbi, Route, connected_subgraph


@dataclass
class Assessment:
    code: str
    question: str
    answer: str
    graph_version: str
    code_check: str
    trace: Trace
    statements: list[Statement]
    candidates: Candidates
    readings: list[dict]
    route_correct: Route
    route_student: Route
    route_student_2nd: Route | None
    subgraph: dict | None
    comparison: Comparison
    levels: dict[str, LevelResult]
    misconceptions: list[dict]
    unlisted: list[dict]
    root_causes: list[RootCause]
    feedback: list[str]
    unmatched: list[dict]
    main_concept: str | None
    headline_level: str
    meta: dict = field(default_factory=dict)

    # ----------------------------------------------------------- JSON
    def to_dict(self) -> dict:
        run = self.trace.run
        return {
            "graph_version": self.graph_version,
            "input": {"code": self.code, "question": self.question, "answer": self.answer},
            "code_check": self.code_check,
            "code_result": {"compiled": run.compiled, "output": run.output,
                            "error": run.error, "error_kind": run.error_kind,
                            "values": dict(run.values)},
            "static_findings": [f.__dict__ for f in self.trace.findings],
            "mutant_runs": {k: {"output": v.output, "error": v.error, "error_kind": v.error_kind}
                            for k, v in sorted(self.trace.mutants.items())},
            "statements": [_statement_dict(s) for s in self.statements],
            "candidates": self.candidates.to_dict(),
            "main_concept": self.main_concept,
            "readings": self.readings,
            "route_correct": self.route_correct.to_dict(),
            "route_student": self.route_student.to_dict(),
            "route_student_2nd": self.route_student_2nd.to_dict() if self.route_student_2nd else None,
            "connected_subgraph": self.subgraph,
            "comparison": self.comparison.to_dict(),
            "levels": {c: r.to_dict() for c, r in sorted(self.levels.items())},
            "headline_level": self.headline_level,
            "misconceptions": self.misconceptions,
            "unlisted_errors": self.unlisted,
            "root_causes": [r.to_dict() for r in self.root_causes],
            "feedback": self.feedback,
            "unmatched_statements": self.unmatched,
        }

    # ------------------------------------------------------- Markdown
    def to_markdown(self) -> str:
        code1 = " ".join(ln.strip() for ln in self.code.splitlines() if ln.strip())
        L = [f"Input: code `{code1}` | question \"{self.question}\" | answer \"{self.answer}\"",
             f"(graph {self.graph_version}; code check: {self.code_check})", "1 Statements"]
        for s in self.statements:
            L.append(f"  {s.source} {s.id:<4} {s.short():<36} -> {_describe(s)}")
        c = self.candidates
        others = [x for x in c.concepts if x != self.main_concept and x not in c.bridges]
        head = f"{self.main_concept} (main)" if self.main_concept else "(no main concept)"
        L.append(f"2 PageRank candidates: {', '.join([head] + others)}"
                 + (f"; bridge {', '.join(c.bridges)}" if c.bridges else ""))
        L.append(f"  main concept: {c.main_reason}")
        L.append("3 Readings")
        for sid in [s.id for s in self.statements if s.source == "answer"]:
            rows = [r for r in self.readings if r["statement"] == sid]
            if rows:
                L.append(f"  {sid}")
            for r in rows:
                blocked = " (blocked)" if r["label"] == CONTRADICT and r["kind"] == "edge" else ""
                L.append(f"    {r['element']:<44} {r['label']}{blocked}"
                         + (f"  ({r['evidence']})" if r.get("evidence") else ""))
        L.append("4 Routes")
        L.append(f"  correct: {_route_text(self.route_correct, self.trace)}")
        L.append(f"  student: {_student_text(self.route_student)}  (cost {self.route_student.cost})")
        if self.route_student_2nd:
            L.append(f"  2nd best: {_student_text(self.route_student_2nd)}  "
                     f"(cost {self.route_student_2nd.cost})")
        if self.subgraph:
            L.append(f"  connected subgraph (list-like answer): {', '.join(self.subgraph['concepts'])}")
        L.append("5 Result")
        for cpt, r in sorted(self.levels.items(), key=lambda kv: (kv[0] != self.main_concept, kv[0])):
            extra = f" (misconception {r.misconception})" if r.misconception else ""
            extra += f" [{r.note}]" if r.note else ""
            L.append(f"  {cpt} {r.level}{extra}")
        cmp_ = self.comparison
        for b in cmp_.broken:
            L.append(f"  broken link: {_edge_text(b['edge'])} (statement {b['statement']})")
        if cmp_.lacking_edges:
            L.append(f"  lacking: {', '.join(_edge_text(e) for e in cmp_.lacking_edges)}")
        if cmp_.excessive_edges:
            L.append(f"  excessive: {', '.join(_edge_text(e) for e in cmp_.excessive_edges)}")
        for sk in cmp_.skipped:
            L.append(f"  jump {sk['from']} -> {sk['to']} (statements {', '.join(sk['statements'])}, "
                     f"hop {sk['hop_distance']}"
                     + (f", skipped {', '.join(sk['skipped'])}" if sk["skipped"] else "") + ")")
        for rc in self.root_causes:
            via = f" (shown: {rc.via}; link {_edge_text(rc.link)})" if rc.link else ""
            L.append(f"  root cause: {rc.concept}{via}, explains {', '.join(rc.explains)}")
            for ct in rc.contrast:
                L.append(f"  likely source: contrast with {ct['neighbour']} ({ct['text']})")
        for u in self.unlisted:
            L.append(f"  wrong but unlisted: {u['statement']} ({u['evidence']})")
        for fb in self.feedback:
            L.append(f"  feedback: {fb}")
        if self.unmatched:
            L.append(f"  unmatched: {', '.join(u['statement'] for u in self.unmatched)}")
        L.append(f"  headline: {self.main_concept} {self.headline_level}")
        return "\n".join(L) + "\n"


# ------------------------------------------------------------- assess

def assess(code: str, question: str, answer: str, kg: KG, use_nli: bool = False,
           run_code: bool = True) -> Assessment:
    """Read one answer onto the knowledge graph (see module docstring)."""
    tracer = Tracer(code, run_code=run_code)
    trace0 = tracer.trace()
    ctx = code_context(kg, tracer.program, trace0)
    code_st = code_statements(kg, ctx, trace0)
    q_st = question_statements(kg, question, ctx)
    a_st = answer_statements(kg, answer, ctx)
    statements = code_st + q_st + a_st
    by_id = {s.id: s for s in statements}

    cands = select(kg, statements, trace0)
    trace = tracer.trace(sorted({m.mis for m in cands.mis_edges}))
    reader = Reader(kg, trace, cands.main_concept, use_nli)

    readings, fault, broken, unlisted = _read_all(kg, reader, cands, a_st)
    anchors = sorted({c for s in code_st + q_st for c in s.concepts})
    route_c, _ = ESViterbi(kg, cands, reader, anchors).run(code_st + q_st)
    route_s, route_s2 = ESViterbi(kg, cands, reader, anchors, fault).run(a_st)
    subgraph = None
    if route_s.mean_cost() > 1:
        matched = sorted({r["concept"] for r in readings if r["kind"] == "concept"
                          and r["label"].startswith("MATCH")})
        subgraph = connected_subgraph(kg, matched)

    comparison = compare_routes(kg, route_c, route_s, broken)
    broken_ids = {b["edge"] for b in broken}
    levels = compute_levels(kg, reader, route_s, by_id, broken_ids)
    answer_concepts = {c for s in a_st for c in s.concepts}
    roots = root_causes(kg, levels, route_s, answer_concepts)
    mis = _misconceptions(kg, route_s)
    feedback = list(dict.fromkeys(m["right"] for m in mis if m["right"]))
    unmatched = [{"statement": st.statements[0], "text": by_id[st.statements[0]].text}
                 for st in route_s.steps if st.state.kind == "NOISE"]
    main = cands.main_concept
    headline = levels[main].level if main in levels else "none"
    run = trace.run
    code_check = ("javac" if run.available else
                  ("static" if run.error_kind else ("unavailable" if code.strip() else "no code")))
    return Assessment(code, question, answer, kg.version, code_check, trace, statements, cands,
                      readings, route_c, route_s, route_s2, subgraph, comparison, levels, mis,
                      unlisted, roots, feedback, unmatched, main, headline)


def _read_all(kg: KG, reader: Reader, cands: Candidates, a_st: list[Statement]):
    """Single-statement readings of every candidate element (for the report,
    broken links, fault attribution and unlisted errors)."""
    readings: list[dict] = []
    fault: dict[str, tuple[str, ...]] = {}
    broken: list[dict] = []
    unlisted: list[dict] = []
    for st in a_st:
        seg = Segment((st,))
        wrong = []
        for m in cands.mis_edges:
            r = reader.read_mis(seg, m)
            if r.label in (MATCH_WRONG, CONTRADICT_RIGHT):
                readings.append(_row(st, "misconception", f"{m.mis} (on {m.concept}, {m.role})", r,
                                     concept=m.concept, ident=m.id))
            if r.label == MATCH_WRONG:
                wrong.append(m)
        primary = sorted({m.concept for m in wrong if m.role == "primary"}) or \
            sorted({m.concept for m in wrong})
        bad = reader.contradicted_claims(seg)
        if bad and not wrong and reader.main_concept:
            primary = [reader.main_concept]
            unlisted.append({"statement": st.id, "text": st.text, "label": "WRONG_UNLISTED",
                             "evidence": "real run contradicts " + ", ".join(
                                 f"{s.name}={s.value}" for s in bad)})
        if primary:
            fault[st.id] = tuple(primary)
        for e in cands.relation_edges:
            r = reader.read_edge(seg, e)
            if r.label != NO:
                readings.append(_row(st, "edge", e.id, r, ident=e.id))
            if r.label == CONTRADICT:
                broken.append({"edge": e.id, "statement": st.id, "parts": list(r.part_ids),
                               "stateable": e.stateable})
        for c in cands.concepts:
            r = reader.read_concept(seg, c, fault.get(st.id, ()))
            if r.label != NO:
                readings.append(_row(st, "concept", c, r, concept=c, ident=f"N:{c}"))
    return readings, fault, broken, unlisted


def _row(st: Statement, kind: str, element: str, r, concept: str | None = None,
         ident: str = "") -> dict:
    d = {"statement": st.id, "kind": kind, "element": _element_text(kind, element),
         "id": ident, "label": r.label, "evidence": r.evidence}
    if concept:
        d["concept"] = concept
    if r.part_ids:
        d["parts"] = list(r.part_ids)
    return d


def _misconceptions(kg: KG, route: Route) -> list[dict]:
    out, seen = [], set()
    for st in route.misconceptions():
        key = (st.state.c_in, st.state.mis)
        if key in seen:
            for m in out:
                if (m["concept"], m["id"]) == key:
                    m["statements"] = sorted(set(m["statements"]) | set(st.statements))
            continue
        seen.add(key)
        edge = next((m for m in kg.mis_edges[st.state.c_in] if m.mis == st.state.mis), None)
        out.append({"id": st.state.mis, "concept": st.state.c_in,
                    "wrong": edge.wrong if edge else "", "right": edge.right if edge else "",
                    "role": edge.role if edge else "", "statements": list(st.statements),
                    "evidence": st.reading.evidence})
    return out


# ---------------------------------------------------------- rendering

def _statement_dict(s: Statement) -> dict:
    d = {"id": s.id, "source": s.source, "text": s.text, "concepts": list(s.concepts),
         "slots": [sl.as_list() for sl in s.slots], "order": s.order}
    if s.source == "answer":
        d.update({"sentence": s.sentence, "negated": s.negated,
                  "link_words": list(s.link_words), "variables": list(s.variables)})
    if s.qtype:
        d["question_type"] = s.qtype
    return d


def _describe(s: Statement) -> str:
    if s.source == "question":
        return f"(type: {s.qtype}) " + ", ".join(s.concepts)
    bits = list(s.concepts)
    if s.source == "answer" and s.variables:
        bits += [v for v in s.variables if v not in bits]
    slots = [f"{sl.name}={sl.value}" for sl in s.slots if not sl.implied]
    out = ", ".join(bits)
    if s.source == "code" and not s.is_result:
        decl = s.meta.get("declares") or []
        if any(not d[2] for d in decl):
            out += " (no initializer)"
        if s.meta.get("reads"):
            out += f" (reads {', '.join(s.meta['reads'])})"
        return out
    if slots:
        out += "; slot " + ", ".join(slots)
    return out


def _element_text(kind: str, element: str) -> str:
    if kind == "edge":
        return "edge " + _edge_text(element)
    if kind == "concept":
        return "stay " + element
    return element


def _edge_text(eid: str | None) -> str:
    if not eid:
        return ""
    body = eid.split(":", 1)[1]
    return body.replace("->", " -> ").replace("~", " ~ ")


def _route_text(route: Route, trace: Trace) -> str:
    path = " -> ".join(route.concept_path()) or "(empty)"
    run = trace.run
    if run.error_kind == "compile":
        return f"{path} -> compile error"
    if run.error_kind == "run":
        return f"{path} -> run-time error"
    if run.available:
        return f"{path} -> prints {run.output.strip()!r}"
    return path


def _student_text(route: Route) -> str:
    parts = []
    for st in route.steps:
        ids = "+".join(st.statements)
        move = f" [{st.move} {st.move_cost}]" if st.move in ("jump",) else ""
        parts.append(f"{ids} -> {st.state.label()}{move}")
    return "; ".join(parts) or "(empty)"


__all__ = ["Assessment", "assess"]
