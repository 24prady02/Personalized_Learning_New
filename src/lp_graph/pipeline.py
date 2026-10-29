"""Step 7 - ``assess(code, question, answer, kg)``: the whole pipeline, no LLM.

1. split code / question / answer into statements (``statements``); code
   the student wrote is run after the question's code;
2. Personalized PageRank -> candidate concepts, edges, misconceptions;
   the main concept by the ordered rule (``candidates``);
3. the reader compares statements with candidate elements (``reader``);
4. the correct route from the graph (expected concepts and their shortest
   stateable paths); ES-Viterbi over the answer -> the student route
   (``viterbi``);
5. compare the routes (``compare``);
6. level per concept from all readings, root cause, consistency
   (``levels``);
7. ``Assessment.to_dict()`` (JSON) and ``to_markdown()`` (readable trace,
   listing per statement every reading and the one the route used).

When the evidence does not decide (no main concept, or nothing read about
it) the headline is ``needs_review`` with the reason; nothing is invented.
Deterministic: every list is sorted or kept in statement order and every
tie is broken by id.
"""

from __future__ import annotations

from dataclasses import dataclass, field, replace

from . import lexicon
from .candidates import Candidates, select
from .compare import Comparison, compare_routes
from .execution import Trace, Tracer, operator_for, run_program, _same_result
from .graph import KG
from .levels import LevelResult, RootCause, compute_levels, misconception_report, root_causes
from .reader import CONTRADICT, CONTRADICT_RIGHT, MATCH_WRONG, NO, Reader, Segment
from .statements import (Statement, answer_statements, asked_name, code_context, code_statements,
                         question_statements, target_vars)
from .edges import trace_edges
from .slots import Slot
from .viterbi import ESViterbi, Route, connected_subgraph, graph_route


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
    needs_review: str | None = None
    meta: dict = field(default_factory=dict)

    # ----------------------------------------------------------- JSON
    def to_dict(self) -> dict:
        run = self.trace.run
        ar = self.trace.answer_run
        return {
            "graph_version": self.graph_version,
            "input": {"code": self.code, "question": self.question, "answer": self.answer},
            "code_check": self.code_check,
            "code_result": {"compiled": run.compiled, "output": run.output,
                            "error": run.error, "errors": list(run.errors), "error_kind": run.error_kind,
                            "values": dict(run.values), "assumed": dict(self.trace.assumed)},
            "answer_code_result": None if ar is None else {
                "output": ar.output, "error": ar.error, "error_kind": ar.error_kind, "values": dict(ar.values),
                "findings": [f.__dict__ for f in self.trace.answer_findings]},
            "static_findings": [f.__dict__ for f in self.trace.findings],
            "mutant_runs": {k: {"output": v.output, "error": v.error, "error_kind": v.error_kind,
                                "values": dict(v.values),
                                "indistinguishable": k in self.trace.indistinguishable}
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
            "needs_review": self.needs_review,
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
             f"(graph {self.graph_version}; code check: {self.code_check})"]
        if self.trace.assumed:
            L.append("  assumed values (not in the code): " + ", ".join(f"{k} = {v}" for k, v in self.trace.assumed.items()))
        L.append("1 Statements")
        for s in self.statements:
            L.append(f"  {s.source} {s.id:<4} {s.short():<40} -> {_describe(s)}")
        run = self.trace.run
        if self.trace.findings:
            L.append("  static findings: " + "; ".join(f"{f.pattern} ({f.message})" for f in self.trace.findings))
        if self.trace.answer_run is not None:
            L.append(f"  student's code: {_run_text(self.trace.answer_run)}"
                     + ("; " + "; ".join(f"{f.pattern} ({f.message})" for f in self.trace.answer_findings)
                        if self.trace.answer_findings else ""))
        c = self.candidates
        others = [x for x in c.concepts if x != self.main_concept and x not in c.bridges]
        head = f"{self.main_concept} (main)" if self.main_concept else "(no main concept)"
        L.append(f"2 PageRank candidates: {', '.join([head] + others)}"
                 + (f"; bridge {', '.join(c.bridges)}" if c.bridges else ""))
        L.append(f"  main concept: {c.main_reason}")
        L.append("3 Readings (every reading; * = the one the student route used)")
        used = {(sid, st.state.id) for st in self.route_student.steps for sid in st.statements}
        for sid in [s.id for s in self.statements if s.source in ("answer", "answer_code")]:
            rows = [r for r in self.readings if r["statement"] == sid]
            L.append(f"  {sid}" + ("" if rows else "  (nothing matched)"))
            for r in rows:
                mark = "*" if (sid, r["id"]) in used else " "
                blocked = " (blocked)" if r["label"] == CONTRADICT and r["kind"] == "edge" else ""
                cls = f" [{r['class']}]" if r.get("class") else ""
                L.append(f"   {mark} {r['element']:<44} {r['label']}{blocked}{cls}"
                         + (f"  ({r['evidence']})" if r.get("evidence") else ""))
        L.append("4 Routes")
        L.append(f"  correct (from the graph): {_graph_text(self.route_correct)} -> {_run_text(run)}")
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
            L.append(f"  broken link: {_edge_text(b['edge'])} (statement {b['statement']}: \"{b.get('quote', '')}\")")
        if cmp_.lacking_edges:
            L.append(f"  lacking: {', '.join(_edge_text(e) for e in cmp_.lacking_edges)}")
        if cmp_.excessive_edges:
            L.append(f"  excessive: {', '.join(_edge_text(e) for e in cmp_.excessive_edges)}")
        for sk in cmp_.skipped:
            L.append(f"  jump {sk['from']} -> {sk['to']} (statements {', '.join(sk['statements'])}, "
                     f"hop {sk['hop_distance']}"
                     + (f", skipped {', '.join(sk['skipped'])}" if sk["skipped"] else "") + ")")
        for m in self.misconceptions:
            L.append(f"  misconception {m['id']} on {m['concept']}: {m['status']}"
                     + (" (held, then corrected)" if m["status"] == "corrected" else ""))
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
        L.append(f"  headline: {self.main_concept} {self.headline_level}"
                 + (f" ({self.needs_review})" if self.needs_review else ""))
        return "\n".join(L) + "\n"


# ------------------------------------------------------------- assess

def assess(code: str, question: str, answer: str, kg: KG, use_nli: bool = False,
           run_code: bool = True) -> Assessment:
    """Read one answer onto the knowledge graph (see module docstring).
    LP_GRAPH_RUN_CODE=0 switches running the code off: everything is then
    decided by reading code, question and answer only."""
    import os

    if os.environ.get("LP_GRAPH_RUN_CODE", "1") == "0":
        run_code = False
    tracer = Tracer(_with_quoted(code, question), run_code=run_code, question=question,
                    asked_name=asked_name(question))
    trace0 = tracer.trace({})
    ctx = code_context(kg, tracer.program, trace0, tracer.kind)
    code_st = code_statements(kg, ctx, trace0)
    q_st = question_statements(kg, question, ctx)
    tvars = target_vars(q_st, ctx)
    qtypes = frozenset(t for s in q_st for t in s.qtypes)
    a_st = answer_statements(kg, answer, ctx, qtypes, tvars)
    last_turn = max((s.turn for s in a_st), default=0)
    answer_code = [s.text for s in a_st if s.source == "answer_code" and s.turn == last_turn]
    if answer_code and run_code:
        run, findings, _ = tracer.trace_answer(answer_code, {})
        trace0.answer_run, trace0.answer_findings = run, findings
    statements = code_st + q_st + a_st
    by_id = {s.id: s for s in statements}

    extra_mis = _distinguishing_mis(kg, tracer, trace0, answer_code)
    cands = select(kg, statements, trace0, ctx=ctx, extra_mis=extra_mis)
    if os.environ.get("LP_GRAPH_READ_CONCEPTS", "0") == "1":
        _add_read_concepts(kg, cands, answer)
    specs: dict[str, dict | None] = {}
    for m in cands.mis_edges:  # one spec per misconception: the first edge that has a slot
        slot = kg.parts["misconceptions"].get(m.id, {}).get("slot")
        if specs.get(m.mis) is None:
            specs[m.mis] = slot
    trace = tracer.trace(specs)
    if answer_code and run_code:
        trace.answer_run, trace.answer_findings, trace.answer_mutants = tracer.trace_answer(answer_code, specs)
        a_st = _finding_claims(a_st, trace)
        statements = code_st + q_st + a_st
        by_id = {s.id: s for s in statements}
    reader = Reader(kg, trace, cands.main_concept, use_nli, ctx, tracer,
                    focus=frozenset(cands.target) | frozenset(cands.decisive) | {cands.main_concept},
                    question_text=question)

    readings, fault, broken, unlisted = _read_all(kg, reader, cands, a_st)
    anchors = sorted({c for s in code_st + q_st for c in s.concepts})
    expected = _expected(cands)
    order = [c for s in code_st for c in s.concepts if c in expected]
    route_c = graph_route(kg, expected, order)
    co_use = {frozenset((a, b)) for s in code_st for a in s.concepts for b in s.concepts if a < b}
    # an edge a statement states is broken when that same statement holds a
    # misconception of an endpoint or makes a wrong claim an endpoint produced
    readings, broken = _break_by_wrong_endpoint(kg, readings, broken, by_id)
    if os.environ.get("LP_GRAPH_PROVENANCE", "0") == "1":
        readings = readings + _grounded_edges(kg, cands, code_st, a_st, readings, q_st)
    # trace the edges between the concepts found (NLI on edge logic, see edges.py)
    mis0 = misconception_report(readings, by_id, kg)
    e_rows, e_broken, e_extra = trace_edges(kg, cands, a_st, readings, mis0)
    readings = readings + e_rows + e_extra
    broken = broken + [b for b in e_broken if b["edge"] not in {x["edge"] for x in broken}]
    # the student route walks the edges the answer states; a broken edge is
    # blocked for the statements that break it
    blocked = {(b["edge"], b["statement"]) for b in broken}
    level_rows = None
    if os.environ.get("LP_GRAPH_PCST", "0") == "1":
        # PCST instead of ES-Viterbi: the connected piece of edge logic the
        # answer expresses gives the misconceptions, levels and edges (pcst.py)
        from .pcst import solve

        tree = solve(kg, cands, reader, a_st, readings, os.environ.get("LP_GRAPH_SELECT", "pcst"))
        route_s, route_s2 = tree.route, None
        p_mis = misconception_report(tree.rows, by_id, kg)
        p_e_rows, p_broken, p_extra = trace_edges(kg, cands, a_st, tree.rows, p_mis)
        broken = [b for b in broken if b.get("source") != "nli"]
        broken = broken + [b for b in p_broken + tree.broken if b["edge"] not in {x["edge"] for x in broken}]
        level_rows = tree.rows + [r for r in p_e_rows + p_extra if r["kind"] != "edge"] \
            + [r for r in readings if r["kind"] == "concept" and r["label"] == "CONTRADICT"]
        readings = readings + tree.rows
    else:
        route_s, route_s2 = ESViterbi(kg, cands, reader, anchors, fault, co_use, blocked).run(a_st)
        route_rows = _route_wording(route_s, by_id)
        if route_rows:
            readings = readings + route_rows
            mis0 = misconception_report(readings, by_id, kg)
    subgraph = None
    if route_s.mean_cost() > 1:
        matched = sorted({r["concept"] for r in readings if r["kind"] == "concept"
                          and r["label"].startswith("MATCH")})
        subgraph = connected_subgraph(kg, matched)
    keep = set(cands.concepts) | {c for r in e_rows + e_extra for c in r.get("endpoints", [r.get("concept")]) if c}
    if level_rows is None:
        level_rows = readings
    mis = [m for m in misconception_report(level_rows, by_id, kg) if m["concept"] in keep]
    broken_ids = {b["edge"] for b in broken}
    comparison = compare_routes(kg, route_c, route_s, broken, set(expected),
                                [m["id"] for m in mis if m["status"] == "corrected"])
    levels = compute_levels(kg, reader, route_s, by_id, broken_ids, level_rows, sorted(keep),
                            cands.main_concept)
    if os.environ.get("LP_GRAPH_LEVELS", "") == "edgelogic":
        # levels and misconceptions from the edge logic alone: for each concept
        # the has_level / misconception edge the answer most likely expresses
        from .edgeclassify import classify

        cls = classify(kg, cands, a_st, answer)
        sid0 = next((s.id for s in a_st if s.source in ("answer", "answer_code")), "")
        levels = {c: LevelResult(c, v["level"], [sid0],
                                 [{"level": v["level"], "class": "edge", "statements": [sid0],
                                   "evidence": f"{v['edge']} (p {v['p']})"}], v["misconception"])
                  for c, v in cls.items()}
        mis = []
        for c, v in cls.items():
            if v["misconception"]:
                m = next((x for x in kg.mis_edges.get(c, []) if x.mis == v["misconception"]), None)
                mis.append({"id": v["misconception"], "concept": c, "statements": [sid0],
                            "evidence": f"{v['edge']} (p {v['p']})", "role": "primary", "confidence": v["p"],
                            "wrong": m.wrong if m else "", "right": m.right if m else "", "status": "held"})
    answer_direct = {c for s in a_st for c in s.direct}
    roots = root_causes(kg, levels, route_s, answer_direct)
    concept_map = _concept_map(kg, levels, route_s, broken_ids)
    feedback = list(dict.fromkeys(m["right"] for m in mis if m["right"] and m["status"] == "held"))
    unmatched = [{"statement": st.statements[0], "text": by_id[st.statements[0]].text}
                 for st in route_s.steps if st.state.kind == "NOISE"]
    main = cands.main_concept
    review = None
    if main is None:
        headline, review = "needs_review", "no concept of the question or code could be identified"
    elif main in levels and levels[main].level != "none":
        headline = levels[main].level
    elif not a_st:
        headline, review = "none", "no answer"
    else:
        headline, review = "needs_review", f"the answer gives no evidence about {main}"
    run = trace.run
    code_check = ("javac" if run.available else
                  ("static" if run.error_kind else ("unavailable" if tracer.program else
                                                     (tracer.kind.kind if tracer.kind.kind != "empty" else "no code"))))
    return Assessment(code, question, answer, kg.version, code_check, trace, statements, cands,
                      readings, route_c, route_s, route_s2, subgraph, comparison, levels, mis,
                      unlisted, roots, feedback, unmatched, main, headline, review,
                      meta={"concept_map": concept_map})


def _concept_map(kg: KG, levels: dict, route: Route, broken: set[str]) -> dict:
    """The student's concept graph: each concept node with its level, the way
    that showed it, a held misconception and what it needs (the neighbours its
    L3 ways require and its prerequisites, with their levels), joined by the
    relation edges read (stated or broken)."""
    nodes = {}
    for c, r in sorted(levels.items()):
        if r.level == "none":
            continue
        needs = sorted({x for row in kg.parts["ways"].get(c, {}).get("L3", []) for x in row["requires"]}
                       | set(kg.inn.get("prerequisite", {}).get(c, [])))
        nodes[c] = {"level": r.level, "evidence": [w.get("evidence", "") for w in r.ways][:3],
                    "misconception": r.misconception,
                    "needs": {n: (levels[n].level if n in levels else "not shown") for n in needs}}
    edges = [{"edge": e, "status": "broken" if e in broken else "stated"} for e in route.edges()]
    edges += [{"edge": e, "status": "broken"} for e in sorted(broken) if e not in route.edges()]
    return {"nodes": nodes, "edges": edges}


def _grounded_edges(kg: KG, cands, code_st: list[Statement], a_st: list[Statement],
                    readings: list[dict], q_st: list[Statement] = ()) -> list[dict]:
    """Relation edges the answer uses, from provenance (LP_GRAPH_PROVENANCE=1).

    * An answer sentence numbered "N:" / "(N)" explains the program's Nth code
      statement or command; a sentence also explains the code lines whose
      variables it names.
    * The concepts of a sentence (its clauses together) plus those of the code
      it explains: every graph relation edge between two of them is used, and
      so is a two-step prerequisite path a -> m -> b between two of them
      (the reasoning passes through m). Edges are only taken from sentences
      that explain code by number, or whose claims the run confirms.
    * A numbered list that explains two or more units of the same program is
      one explanation of that program, answering the question: the concepts
      of all its units and of the question form one map, so an edge between
      concepts of different units (or a unit and the question) is used too.
    """
    import re

    grounded = {r["statement"] for r in readings if r["kind"] == "concept" and r["label"].startswith("MATCH")
                and r.get("class") in ("run", "hypothetical", "relation", "diagnosis")}
    code = [s for s in code_st if s.source == "code"]
    groups: dict[tuple[int, int], list[Statement]] = {}
    for s in a_st:
        if s.source in ("answer", "answer_code"):
            groups.setdefault((s.turn, s.sentence), []).append(s)
    cset = set(cands.concepts)
    rows, seen = [], set()

    def emit(concepts: set[str], sid: str, why: str) -> None:
        concepts = concepts & (cset | {c for c in concepts if c in kg.rel_by_concept})
        for a in sorted(concepts):
            for eid in kg.rel_by_concept.get(a, []):
                e = kg.relation_edges[eid]
                if e.other(a) in concepts and e.id not in seen:
                    seen.add(e.id)
                    rows.append({"statement": sid, "kind": "edge", "id": e.id, "element": e.id, "label": "MATCH",
                                 "class": "relation", "endpoints": [e.src, e.dst], "source": "grounded",
                                 "evidence": f"grounded edge: {why} uses both ends", "confidence": 1.0})
        # two-step prerequisite paths a -> m -> b between two of the concepts
        for a in sorted(concepts):
            for e1 in (kg.relation_edges[x] for x in kg.rel_by_concept.get(a, [])):
                if e1.kind != "prerequisite" or e1.src != a:
                    continue
                mid = e1.dst
                for e2 in (kg.relation_edges[x] for x in kg.rel_by_concept.get(mid, [])):
                    if e2.kind == "prerequisite" and e2.src == mid and e2.dst in concepts and e2.dst != a:
                        for e3 in (e1, e2):
                            if e3.id not in seen:
                                seen.add(e3.id)
                                rows.append({"statement": sid, "kind": "edge", "id": e3.id, "element": e3.id,
                                             "label": "MATCH", "class": "relation", "endpoints": [e3.src, e3.dst],
                                             "source": "grounded",
                                             "evidence": f"grounded edge: on the path {a} -> {mid} -> {e2.dst}",
                                             "confidence": 1.0})

    units: dict[int, set[str]] = {}
    for group in groups.values():
        concepts = set().union(*(set(s.concepts) for s in group))
        numbered = False
        for s in group:
            m = re.match(r"\s*\(?(\d{1,2})[).:]", s.text)
            if m and 1 <= int(m.group(1)) <= len(code):
                k = int(m.group(1)) - 1
                concepts |= set(code[k].concepts)
                units.setdefault(k, set()).update(concepts)
                numbered = True
            for c_st in code:
                if set(s.variables) & set(c_st.variables):
                    concepts |= set(c_st.concepts)
        if not numbered and not any(s.id in grounded for s in group):
            continue
        emit(concepts, group[0].id, "the sentence explains code that")
    if len(units) >= 2:
        joint = set().union(*units.values()) | {c for q in q_st for c in q.concepts}
        sid = next(s.id for s in a_st if s.source in ("answer", "answer_code"))
        emit(joint, sid, f"the numbered answer explains {len(units)} units of the program; together it")
    return rows


def _add_read_concepts(kg: KG, cands, answer: str) -> None:
    """Concept detection by reading (LP_GRAPH_READ_CONCEPTS=1): a graph
    neighbour of a candidate concept joins the candidates when the reader
    (conceptnli) finds that the answer entails one of the neighbour's own L1
    edge logics (p >= 0.5); its relation edges to the candidates and its
    misconception edges come with it."""
    from . import conceptnli

    if not (answer or "").strip():
        return
    have = set(cands.concepts)
    nbrs = sorted({kg.relation_edges[e].other(c) for c in have for e in kg.rel_by_concept.get(c, [])} - have)
    found = []
    for n in nbrs:
        texts = [w.text for w in kg.ways(n, "L1") if w.text]
        if texts and max(p for p, _ in conceptnli.test(answer[:800], texts)) >= 0.5:
            found.append(n)
    if not found:
        return
    cands.concepts = list(cands.concepts) + found      # a new list: rank / scores stay as PageRank left them
    for n in found:
        cands.scores.setdefault(n, 0.0)
    have |= set(found)
    known = {e.id for e in cands.relation_edges}
    for eid, e in sorted(kg.relation_edges.items()):
        if eid not in known and e.src in have and e.dst in have and (e.src in found or e.dst in found):
            cands.relation_edges.append(e)
    known_m = {m.id for m in cands.mis_edges}
    for n in found:
        cands.mis_edges.extend(m for m in kg.mis_edges.get(n, []) if m.id not in known_m)


def _with_quoted(code: str, question: str) -> str:
    """The code plus any Java statement the question quotes that the code
    does not contain ("What does int k2 = Math.round(2.5); do?")."""
    from .execution import classify_code
    from .statements import _JAVA_IN_TEXT, _looks_java

    if classify_code(code).kind not in ("java", "empty"):
        return code
    flat = "".join(code.split())
    quoted = [m.group(0).strip() for m in _JAVA_IN_TEXT.finditer(question or "")
              if _looks_java(m.group(0)) and "".join(m.group(0).split()) not in flat]
    return "\n".join([code] + quoted) if quoted else code


def _finding_claims(a_st: list[Statement], trace: Trace) -> list[Statement]:
    """Code the student wrote states rules by what it does: a finding such as
    a capitalised name or a loop bound past the end becomes a rule slot of
    that statement (lexicon.FINDING_SLOTS)."""
    extra = [Slot(*lexicon.FINDING_SLOTS[f.pattern], False, None, False, (0, 0), False,
                  (("from", f.pattern),))
             for f in trace.answer_findings if f.pattern in lexicon.FINDING_SLOTS]
    shown = tuple(sorted({lexicon.DECISIVE[f.pattern] for f in trace.answer_findings
                          if f.pattern in lexicon.DECISIVE}))
    out = []
    for s in a_st:
        if s.source == "answer_code" and s.turn == max(x.turn for x in a_st):
            s = replace(s, slots=s.slots + tuple(extra),
                        direct=tuple(sorted(set(s.direct) | set(shown))),
                        concepts=tuple(sorted(set(s.concepts) | set(shown))))
        out.append(s)
    return out


def _route_wording(route: Route, by_id: dict[str, Statement]) -> list[dict]:
    """Readings from wording alone that the ES-Viterbi route chose: a
    misconception state (held) or an L1 way state (named the rule)."""
    rows = []
    for st in route.steps:
        if st.reading.cls != "text-only":
            continue
        sid = st.statements[0]
        if st.state.kind == "M":
            rows.append({"statement": sid, "kind": "misconception", "id": f"route:{st.state.id}",
                         "element": f"{st.state.mis} (on {st.state.c_in}, route)", "label": MATCH_WRONG,
                         "class": "wrong", "concept": st.state.c_in, "role": "primary",
                         "source": "route", "evidence": st.reading.evidence})
        elif st.state.kind == "N":
            # the level of the way the wording states (L1 when not said)
            lv = next((x for x in ("L2", "L3", "L4") if f"states an {x} way" in st.reading.evidence), "L1")
            cls = {"L1": "rule", "L2": "run", "L3": "relation", "L4": "hypothetical"}[lv]
            rows.append({"statement": sid, "kind": "concept", "id": f"N:{st.state.c_in}",
                         "element": f"stay {st.state.c_in}", "label": "MATCH", "class": cls,
                         "concept": st.state.c_in, "source": "route", "evidence": st.reading.evidence})
    return rows


def _break_by_wrong_endpoint(kg: KG, readings: list[dict], broken: list[dict],
                             by_id: dict[str, Statement]) -> tuple[list[dict], list[dict]]:
    # a wrong belief the student holds about an endpoint anywhere in the answer
    held = {r["concept"] for r in readings if r.get("concept") and r["label"] == MATCH_WRONG}
    wrong: dict[str, set[str]] = {}
    for r in readings:
        if r.get("concept") and (r["label"] == MATCH_WRONG or (r["label"] == CONTRADICT and r.get("class") == "run")):
            wrong.setdefault(r["statement"], set()).add(r["concept"])
    for r in readings:
        wrong.setdefault(r["statement"], set()).update(held)
    out, seen = [], {b["edge"] for b in broken}
    for r in readings:
        if r["kind"] == "edge" and r["label"].startswith("MATCH") and set(r.get("endpoints", ())) & wrong.get(r["statement"], set()):
            r = {**r, "label": CONTRADICT, "evidence": r["evidence"] + "; but this statement is wrong about "
                 + ", ".join(sorted(set(r["endpoints"]) & wrong[r["statement"]]))}
            if r["id"] not in seen:
                seen.add(r["id"])
                e = kg.relation_edges[r["id"]]
                broken = broken + [{"edge": e.id, "statement": r["statement"], "parts": [], "stateable": e.stateable,
                                    "quote": by_id[r["statement"]].text if r["statement"] in by_id else "",
                                    "reason": "the statement holds a wrong belief about an endpoint"}]
        out.append(r)
    return out, broken


def _expected(cands: Candidates) -> list[str]:
    """Concepts the correct answer is about: the main concept, the
    question-target and decisive concepts among the candidates."""
    keep = set(cands.concepts)
    out = [cands.main_concept] if cands.main_concept else []
    out += [c for c in cands.decisive if c in keep]
    out += [c for c in cands.target if c in keep and c not in lexicon.GENERIC]
    return list(dict.fromkeys(out))


def _distinguishing_mis(kg: KG, tracer: Tracer, trace: Trace, answer_code: list[str]) -> set[str]:
    """Misconceptions whose misinterpreter changes this code's result (§5.3)."""
    out: set[str] = set()
    if not tracer.run_code and not answer_code:
        return out
    answer_prog = tracer.answer_program(answer_code)[0] if answer_code else None
    answer_real = trace.answer_run
    seen: dict[tuple[str, int], bool] = {}
    for mid, info in sorted(kg.parts["misconceptions"].items()):
        fn = operator_for(info["mis"], info.get("slot"))
        if fn is None:
            continue
        for prog, real in ((tracer.program, trace.run), (answer_prog, answer_real)):
            if not prog or real is None:
                continue
            key = (prog, id(fn))
            if key not in seen:
                mutated = fn(prog)
                seen[key] = bool(mutated and mutated != prog and not _same_result(run_program(mutated), real))
            if seen[key]:
                out.add(info["mis"])
    return out


def _read_all(kg: KG, reader: Reader, cands: Candidates, a_st: list[Statement]):
    """Single-statement readings of every candidate element (for the report,
    levels, broken links, fault attribution and unlisted errors)."""
    readings: list[dict] = []
    fault: dict[str, tuple[str, ...]] = {}
    broken: list[dict] = []
    unlisted: list[dict] = []
    cand = set(cands.concepts)
    for st in a_st:
        seg = Segment((st,))
        wrong = []
        for m in cands.mis_edges:
            r = reader.read_mis(seg, m)
            if r.label == MATCH_WRONG and m.role != "primary" and m.concept not in st.direct:
                continue  # a context-role edge counts only when the student names that concept
            if r.label in (MATCH_WRONG, CONTRADICT_RIGHT):
                readings.append(_row(st, "misconception", f"{m.mis} (on {m.concept}, {m.role})", r,
                                     concept=m.concept, ident=m.id, role=m.role))
            if r.label == MATCH_WRONG:
                wrong.append(m)
        primary = sorted({m.concept for m in wrong if m.role == "primary"}) or \
            sorted({m.concept for m in wrong})
        bad = [(s, src) for s, v, src in reader.checked(seg) if v is False]
        if bad and not wrong:
            blamed = sorted({c for s, src in bad for c in reader.producers(s, src)} & cand) or (
                [reader.main_concept] if reader.main_concept else [])
            primary = blamed
            unlisted.append({"statement": st.id, "text": st.text, "label": "WRONG_UNLISTED",
                             "blamed": blamed,
                             "evidence": "the run contradicts " + ", ".join(
                                 f"{s.name}={s.value!r}" for s, _ in bad)})
        if primary:
            fault[st.id] = tuple(primary)
        for e in cands.relation_edges:
            r = reader.read_edge(seg, e)
            if r.label != NO:
                readings.append(_row(st, "edge", e.id, r, ident=e.id, endpoints=(e.src, e.dst)))
            if r.label == CONTRADICT:
                broken.append({"edge": e.id, "statement": st.id, "parts": list(r.part_ids),
                               "stateable": e.stateable, "quote": st.text})
        for c in cands.concepts:
            r = reader.read_concept(seg, c, fault.get(st.id, ()))
            if r.label != NO:
                readings.append(_row(st, "concept", c, r, concept=c, ident=f"N:{c}"))
    return readings, fault, broken, unlisted


def _row(st: Statement, kind: str, element: str, r, concept: str | None = None,
         ident: str = "", role: str = "", endpoints: tuple[str, ...] = ()) -> dict:
    d = {"statement": st.id, "kind": kind, "element": _element_text(kind, element),
         "id": ident, "label": r.label, "evidence": r.evidence}
    if getattr(r, "cls", ""):
        d["class"] = r.cls
    if r.confidence != 1.0:
        d["confidence"] = r.confidence
    if concept:
        d["concept"] = concept
    if role:
        d["role"] = role
    if endpoints:
        d["endpoints"] = list(endpoints)
    if r.part_ids:
        d["parts"] = list(r.part_ids)
    return d


# ---------------------------------------------------------- rendering

def _statement_dict(s: Statement) -> dict:
    d = {"id": s.id, "source": s.source, "text": s.text, "concepts": list(s.concepts),
         "slots": [sl.as_list() + ([dict(sl.extra)] if sl.extra else []) for sl in s.slots], "order": s.order}
    if s.source in ("answer", "answer_code"):
        d.update({"sentence": s.sentence, "negated": s.negated, "turn": s.turn,
                  "direct": list(s.direct), "context": list(s.context),
                  "link_words": list(s.link_words), "variables": list(s.variables),
                  "hypothetical": s.hypothetical, "corrects": s.corrects,
                  "changes": [dict(c) for c in s.changes]})
    if s.qtype:
        d["question_type"] = s.qtype
    return d


def _describe(s: Statement) -> str:
    if s.source == "question":
        return f"(type: {s.qtype}) " + ", ".join(s.concepts)
    bits = list(s.direct) if s.source in ("answer", "answer_code") else list(s.concepts)
    if s.source == "answer" and s.context:
        bits.append("context: " + ", ".join(s.context))
    if s.source == "answer" and s.variables:
        bits += [v for v in s.variables if v not in bits]
    slots = [f"{'what-if ' if sl.hypothetical else ''}{sl.name}={sl.value!r}"
             for sl in s.slots if not sl.implied]
    out = ", ".join(bits)
    if s.source == "code" and not s.is_result:
        decl = s.meta.get("declares") or []
        if any(not d[2] for d in decl):
            out += " (no initializer)"
        if s.meta.get("reads"):
            out += f" (reads {', '.join(s.meta['reads'])})"
        return out
    if s.turn:
        out = f"[turn {s.turn}{', corrects' if s.corrects else ''}] " + out
    if slots:
        out += "; slot " + ", ".join(slots)
    if s.changes:
        out += "; change " + ", ".join(str(dict(c)) for c in s.changes)
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


def _run_text(run) -> str:
    if run is None:
        return "not run"
    if run.error_kind == "compile":
        return "compile error (" + "; ".join(run.errors or (run.error,)) + ")"
    if run.error_kind == "run":
        return f"run-time error ({run.error})"
    if run.error_kind == "timeout":
        return "does not stop"
    if run.available:
        return f"prints {run.output.strip()!r}" if run.output.strip() else "prints nothing"
    return "not run"


def _graph_text(route: Route) -> str:
    parts = []
    for st in route.steps:
        if st.state.kind == "E":
            parts.append(f"{st.state.c_in} -[{st.state.edge.split(':')[0]}]-> {st.state.c_out}")
        else:
            parts.append(st.state.c_in or "")
    return "; ".join(parts) or "(empty)"


def _student_text(route: Route) -> str:
    parts = []
    for st in route.steps:
        ids = "+".join(st.statements)
        move = f" [{st.move} {st.move_cost}]" if st.move in ("jump",) else ""
        parts.append(f"{ids} -> {st.state.label()}{move}")
    return "; ".join(parts) or "(empty)"


__all__ = ["Assessment", "assess"]
