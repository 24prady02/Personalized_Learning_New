"""Step 3 of the pipeline - the reader: MATCH | CONTRADICT | NO.

``Reader.read_*`` compares a *segment* (1-3 consecutive statements, so a
contrast split over two clauses can be read as one) with one candidate
element. Every reading carries an **evidence class** (``named``, ``rule``,
``run``, ``relation``, ``hypothetical``, ``diagnosis``, ``wrong``); the level
ladder accepts only the class each level needs (levels.py).

* **Concept way (stay)** - ``names_the_element`` matches only when the
  student names the concept (``direct``: alias, symbol or own code), never
  through a variable or pronoun. A rule slot that agrees with a way is
  ``rule`` evidence; a slot that disagrees is a CONTRADICT. A claim about
  this code (output, value, expression, compile / crash) is ``run``
  evidence for a concept only if that concept *produced* the claimed value
  (it is in the code that computes the variable or prints the output).
* **Relation edge** - against the edge-logic parts in ``kg.parts``. An
  endpoint is present if named, or if the segment points at its code and a
  slot agrees with its part. MATCH needs both endpoints and every addressed
  part agreeing *with the slot attached to the part's own concept*.
* **Misconception pair** - a *rule* slot (``lexicon.RULE_SLOTS``) equal to
  the misconception's wrong value is MATCH-WRONG on its own (rules are
  stated, not run). A value / output claim needs the code: the real run
  contradicts it and the misinterpreter run confirms it. The slot's subject
  must be the misconception's concept (or unattached). A pair with no slot
  can match through its generated contrast terms (several wrong-belief
  terms, the concept named, no correct-rule term), at lower confidence.
  CONTRADICT-RIGHT if the segment states the right value.
* **Hypothetical** - a what-if claim is checked against the run of the
  changed program (``Tracer.trace_variant``), never the real run.

Code and question segments are the truth: they MATCH every concept and
edge they show unless a part contradicts the run, and never a misconception.

With ``use_nli`` an optional cross-encoder may label relation-edge parts and
ways that have no slots (MATCH_NLI, lower confidence); it is never used for
misconceptions.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Sequence

from . import claims, lexicon
from .edgelogic import reader_for
from .slots import Slot, normalize, slot_agrees

if TYPE_CHECKING:  # pragma: no cover
    from .execution import Run, Trace, Tracer
    from .graph import KG, MisEdge, RelEdge
    from .statements import CodeContext, Statement

MATCH = "MATCH"
MATCH_NLI = "MATCH_NLI"
CONTRADICT = "CONTRADICT"
NO = "NO"
MATCH_WRONG = "MATCH-WRONG"
CONTRADICT_RIGHT = "CONTRADICT-RIGHT"
WRONG_UNLISTED = "WRONG_UNLISTED"

ENTERS = frozenset({MATCH, MATCH_NLI, MATCH_WRONG})



@dataclass(frozen=True)
class Reading:
    label: str
    part_ids: tuple[str, ...] = ()
    evidence: str = ""
    confidence: float = 1.0
    ways: tuple[tuple[str, int, str], ...] = ()   # (level, index, way) matched
    cls: str = ""                                  # evidence class

    def to_dict(self) -> dict:
        d = {"label": self.label, "evidence": self.evidence}
        if self.cls:
            d["class"] = self.cls
        if self.part_ids:
            d["parts"] = list(self.part_ids)
        if self.ways:
            d["ways"] = [list(w) for w in self.ways]
        if self.confidence != 1.0:
            d["confidence"] = self.confidence
        return d


@dataclass(frozen=True)
class Segment:
    """1-3 consecutive statements read together."""

    statements: tuple["Statement", ...]

    @property
    def ids(self) -> tuple[str, ...]:
        return tuple(s.id for s in self.statements)

    @property
    def source(self) -> str:
        src = self.statements[0].source
        return "answer" if src == "answer_code" else src

    @property
    def concepts(self) -> frozenset[str]:
        return frozenset(c for s in self.statements for c in s.concepts)

    @property
    def direct(self) -> frozenset[str]:
        return frozenset(c for s in self.statements for c in s.direct)

    @property
    def context(self) -> frozenset[str]:
        return frozenset(c for s in self.statements for c in s.context)

    @property
    def slots(self) -> tuple[Slot, ...]:
        return tuple(sl for s in self.statements for sl in s.slots)

    @property
    def text(self) -> str:
        return " / ".join(s.text for s in self.statements)

    @property
    def is_code(self) -> bool:
        return any(s.source == "answer_code" for s in self.statements)


@dataclass
class Reader:
    kg: "KG"
    trace: "Trace | None"
    main_concept: str | None = None
    use_nli: bool = False
    ctx: "CodeContext | None" = None
    tracer: "Tracer | None" = None
    focus: frozenset = frozenset()   # main, question-target and decisive concepts
    question_text: str = ""
    _cache: dict = field(default_factory=dict)
    _nli: object = None

    # ---------------------------------------------------------- helpers
    def _cached(self, seg: Segment, key: str, fn) -> Reading:
        k = (seg.ids, key)
        if k not in self._cache:
            self._cache[k] = fn()
        return self._cache[k]

    @property
    def run(self) -> "Run | None":
        return self.trace.run if self.trace else None

    def meaning(self):
        """The meaning reader (meaning.py) when LP_GRAPH_MEANING=1, else None."""
        import os

        if os.environ.get("LP_GRAPH_MEANING", "0") != "1":
            return None
        from .meaning import meaning_for

        return meaning_for(self.kg, self.logic)

    @property
    def logic(self):
        """The edge-logic reader of this graph (edgelogic.py)."""
        return reader_for(self.kg)

    def variables(self) -> tuple[str, ...]:
        return tuple(self.ctx.var_types) if self.ctx else ()

    def best_edge(self, st: "Statement") -> tuple:
        """The one edge whose logic this answer statement expresses best, among
        all edges of the concepts it is about (and of what the question asks):
        relation edges, both sides of misconception edges, and level ways.
        ("relation", edge id) | ("mis", edge id, "wrong" | "right") |
        ("way", concept, level, index) | () when nothing reaches the threshold.
        Reading every edge kind together means a statement is read as one
        thing - a misconception's wrong side wins only if no relation, way or
        correct side explains the statement better."""
        key = ("BEST", st.id)
        if key in self._cache:
            return self._cache[key]
        best: tuple = ()
        if st.source in ("answer", "answer_code") and not st.hypothetical and len(st.text) >= 3:
            # only the concept nodes already found from the code (and what the
            # question asks about), never every concept a word may name
            found = set(self.focus) | set(self.ctx.code_concepts if self.ctx else ())
            concepts = (set(self.focus) | (set(st.concepts) & found)) & set(self.kg.concepts)
            vs = self.variables()
            score = lambda text: self.logic.score(st.text, text, vs) if text else 0.0  # noqa: E731
            cands: list[tuple[float, tuple]] = []
            for c in sorted(concepts):
                for eid in self.kg.rel_by_concept.get(c, []):
                    cands.append((score(self.kg.relation_edges[eid].logic), ("relation", eid)))
                for m in self.kg.mis_edges.get(c, []):
                    sw, sr = score(m.wrong), score(m.right)
                    cands.append((sw, ("mis", m.id, "wrong")))
                    cands.append((sr, ("mis", m.id, "right")))
                for lv in ("L1", "L2", "L3", "L4"):
                    for w in self.kg.ways(c, lv):
                        cands.append((score(w.text), ("way", c, lv, w.index)))
            cands.sort(key=lambda x: (-x[0], x[1]))
            if cands and cands[0][0] >= self.logic.match:
                best = cands[0][1]
                if best[0] == "mis":  # the two sides share the topic: the distinguishing anchors decide
                    m = next(x for c in self.kg.mis_edges.values() for x in c if x.id == best[1])
                    side, _ = self.logic.side(st.text, m.wrong, m.right, vs)
                    best = ("mis", m.id, {"a": "wrong", "b": "right"}[side]) if side else ()
        self._cache[key] = best
        return best

    def run_for(self, st: "Statement") -> "Run | None":
        """The run a statement's claims are checked against."""
        if not self.trace:
            return None
        if st.source == "answer_code" or (self.trace.answer_run is not None and not self.trace.program):
            return self.trace.answer_run
        return self.trace.run

    def checked(self, seg: Segment) -> list[tuple[Slot, bool, "Statement"]]:
        """(slot, verdict) for every checkable, non-hypothetical claim of an answer segment."""
        if seg.source != "answer":
            return []
        out = []
        for st in seg.statements:
            run = self.run_for(st)
            for s in st.slots:
                if s.name not in claims.CHECKABLE or s.hypothetical:
                    continue
                if not self._checkable(s, st):
                    continue
                v = claims.check_expr(s) if s.name == "expr" else (claims.check(s, run) if run else None)
                if v is None:
                    v = self._command_args(st, s)
                if v is not None:
                    out.append((s, v, st))
        return out

    def _command_args(self, st: "Statement", s: Slot) -> bool | None:
        """A claim about command-line arguments, checked against the shell
        commands (``java Prog a b`` gives args = [a, b]) of the program the
        question names."""
        kind = self.ctx.kind if self.ctx else None
        if not kind or kind.kind != "commands" or s.subject != lexicon.ROLES.get("command_arguments") \
                or s.name != "value":
            return None
        runs = [re.findall(r"\bjava\s+(\w+)((?:\s+(?![<>|])[^\s<>|]+)*)", c) for c in kind.commands]
        args = [a.split() for cmd in runs for prog, a in cmd]
        if not args:
            return None
        named = {prog for cmd in runs for prog, _ in cmd if prog in (self.question_text or "")}
        if named:
            args = [a.split() for cmd in runs for prog, a in cmd if prog in named]
        empty = all(not a for a in args)
        if s.value in ("none", "empty"):
            return empty != s.negated
        return None

    def _checkable(self, s: Slot, st: "Statement") -> bool:
        """Abstain when the run cannot speak for the claim: code the student
        wrote is checked only for what happens when it runs (a fragment may
        miss its surroundings); a program that reads input, or reads a
        variable whose value was invented, is checked only by claims that do
        not depend on those values (one variable compared with another)."""
        if s.name == "expr":
            return True
        if st.source == "answer_code":
            return s.name == "crash"
        tr = self.trace
        if tr is None:
            return True
        relative = s.name == "value" and s.value.startswith("var:")
        if (tr.sampled or tr.reads_input) and not relative:
            return False
        return True

    def contradicted_claims(self, seg: Segment) -> list[Slot]:
        return [s for s, v, _ in self.checked(seg) if v is False]

    def producers(self, s: Slot, st: "Statement") -> set[str]:
        """Concepts that produced the value a claim is about."""
        out: set[str] = set()
        ctx = self.ctx
        if s.name == "expr":
            m = re.search(r"(%|/|\*|\+|-|>=|<=|==|!=|>|<)", s.get("expr"))
            if m:
                out.add(lexicon.OP_CONCEPT.get(m.group(1), ""))
            return out
        if st.source == "answer_code":
            found = self._finding_concepts(answer=True)
            return found or (set(st.direct) - lexicon.GENERIC)
        if s.name == "value" and s.subject and s.subject == lexicon.ROLES.get("command_arguments"):
            return {s.subject}
        if s.name in ("compile", "crash", "error_time", "runs"):
            out |= self._result_concepts()
            out |= self._finding_concepts()
            return out
        if ctx is None:
            return out
        if s.name == "value" and s.subject and s.subject.startswith("var:"):
            v = s.subject[4:]
            out |= set(ctx.var_concepts.get(v, ()))
            for cs in ctx.stmts:
                if v in cs.assigns:
                    out |= set(ctx.stmt_concepts.get(cs.index, ()))
        elif s.name in ("output", "printed", "trailing_empty_line"):
            for cs in ctx.stmts:
                if cs.kind == "print":
                    out |= set(ctx.stmt_concepts.get(cs.index, ()))
        return out - (lexicon.GENERIC - set(st.direct))

    def raw_producers(self, s: Slot, st: "Statement") -> set[str]:
        """Every concept of the code that computes what a claim is about,
        generic ones included (a misinterpreter of assignment reads them)."""
        ctx = self.ctx
        if ctx is None:
            return set()
        if s.name == "value" and s.subject and s.subject.startswith("var:"):
            v = s.subject[4:]
            out = set(ctx.var_concepts.get(v, ()))
            for cs in ctx.stmts:
                if v in cs.assigns:
                    out |= set(ctx.stmt_concepts.get(cs.index, ()))
            return out
        return self.producers(s, st)

    def _result_concepts(self) -> set[str]:
        run = self.run
        if run is None:
            return set()
        o = lexicon.OUTCOME
        keys = ("compile_error", "compiling") if run.error_kind == "compile" else (
            ("run_error", "running") if run.error_kind == "run" else ("running",))
        return {o[k] for k in keys if k in o}

    def _finding_concepts(self, answer: bool = False) -> set[str]:
        if not self.trace:
            return set()
        fs = self.trace.answer_findings if answer else self.trace.findings
        return {lexicon.DECISIVE[f.pattern] for f in fs if f.pattern in lexicon.DECISIVE}

    # ---------------------------------------------------------- concept
    def read_concept(self, seg: Segment, concept: str,
                     fault: Sequence[str] = ()) -> Reading:
        """Stay on a concept. ``fault`` = concepts blamed for a wrong claim."""
        return self._cached(seg, f"N:{concept}:{','.join(fault)}",
                            lambda: self._read_concept(seg, concept, fault))

    def _read_concept(self, seg: Segment, concept: str, fault: Sequence[str]) -> Reading:
        if concept not in seg.concepts:
            return Reading(NO)
        if seg.source != "answer":
            return Reading(MATCH, evidence=f"{seg.source} shows {concept}", cls="named")
        if concept in fault:
            bad = self.contradicted_claims(seg)
            return Reading(CONTRADICT, evidence="real run contradicts: "
                           + ", ".join(f"{s.name}={s.value}" for s in bad), cls="run")
        matched, contra = [], []
        for level in ("L1", "L2", "L3", "L4"):
            for row in self.kg.parts["ways"].get(concept, {}).get(level, []):
                r = self.read_way(seg, concept, level, row)
                if r.label in (MATCH, MATCH_NLI):
                    matched.append((level, row["index"], row["way"], r.cls))
                elif r.label == CONTRADICT:
                    contra.append((level, row["index"], row["way"], r.cls))
        strong = [m for m in matched if m[3] != "named"]
        if contra and not strong:
            return Reading(CONTRADICT, evidence="contradicts way " + ", ".join(
                f"{lv} {w}" for lv, _, w, _ in contra), ways=tuple(c[:3] for c in contra), cls=contra[0][3])
        if matched:
            best = max(matched, key=lambda m: _CLASS_RANK.get(m[3], 0))
            return Reading(MATCH, evidence="matches " + ", ".join(
                f"{lv} {w} [{c}]" for lv, _, w, c in matched[:6]), ways=tuple(m[:3] for m in matched),
                cls=best[3], confidence=0.5 if best[3] == "named" else 1.0)
        return Reading(NO)

    def read_way(self, seg: Segment, concept: str, level: str, row: dict) -> Reading:
        """One has_level way of ``concept`` against an answer segment."""
        return self._cached(seg, f"W:{concept}:{level}:{row['index']}",
                            lambda: self._read_way(seg, concept, level, row))

    def _read_way(self, seg: Segment, concept: str, level: str, row: dict) -> Reading:
        if concept not in seg.concepts:
            return Reading(NO)
        evidence = row.get("evidence", "statement")
        by_name: dict[str, set[str]] = {}
        for name, value, *_ in row["slots"]:
            by_name.setdefault(name, set()).add(value)
        usable = {n: next(iter(v)) for n, v in sorted(by_name.items()) if len(v) == 1
                  and n not in claims.CHECKABLE}
        agree = disagree = 0
        for s in seg.slots:
            if s.name not in usable or s.hypothetical:
                continue
            if s.subject and s.subject != concept and not s.subject.startswith("var:") \
                    and s.subject in self.kg.knowledge.concepts:
                continue  # a rule stated about another concept
            ok = slot_agrees(s, s.name, usable[s.name])
            if ok is True and not s.implied:
                agree += 1
            elif ok is False and s.subject == concept:
                disagree += 1  # only a rule stated about this concept can contradict it
        if disagree:
            return Reading(CONTRADICT, evidence=f"{level} {row['way']}: slot disagrees", cls="rule")
        if evidence == "run":
            produced = [(s, v) for s, v, st in self.checked(seg) if concept in self.producers(s, st)]
            if any(v is False for _, v in produced) and row["rule_type"] == "OP":
                return Reading(CONTRADICT, evidence=f"{level} {row['way']}: real run contradicts", cls="run")
            if produced and all(v for _, v in produced):
                return Reading(MATCH, evidence=f"{level} {row['way']}: real run confirms "
                               + ", ".join(f"{s.name}={s.value!r}" for s, _ in produced[:3]), cls="run")
        if evidence in ("hypothetical",) and self.hypothesis_confirmed(seg, concept):
            return Reading(MATCH, evidence=f"{level} {row['way']}: the changed program confirms the prediction",
                           cls="hypothetical")
        if evidence == "diagnosis":
            diag = [(s, v) for s, v, st in self.checked(seg) if s.name in ("compile", "crash") and not s.implied
                    and concept in self.producers(s, st)]
            if diag and all(v for _, v in diag):
                return Reading(MATCH, evidence=f"{level} {row['way']}: the error is named and the run confirms it",
                               cls="diagnosis")
        if agree:
            return Reading(MATCH, evidence=f"{level} {row['way']}: rule slots agree", cls="rule")
        if row["way"] == "names_the_element" and concept in seg.direct:
            return Reading(MATCH, evidence="names the concept", confidence=0.5, cls="named")
        if self.use_nli and not row["slots"] and concept in seg.direct:
            return self._nli_read(seg, " ".join(w.text for w in self.kg.ways(concept, level)
                                                if w.index == row["index"]))
        return Reading(NO)

    def _way_text(self, concept: str, level: str, index: int) -> str:
        for w in self.kg.ways(concept, level):
            if w.index == index:
                return w.text
        return ""

    # ---------------------------------------------------- hypotheticals
    def hypothesis_runs(self, seg: Segment) -> list[tuple["Statement", "Run", "Run"]]:
        """(statement, base run, changed run) for each what-if statement with a
        change the tracer can apply."""
        out = []
        if self.tracer is None:
            return out
        for st in seg.statements:
            if not st.hypothetical or not st.changes:
                continue
            key = ("H", st.changes)
            if key not in self._cache:
                changes = [dict(c) for c in st.changes]
                starts = [c for c in changes if c.get("kind") == "start"]
                base = self.tracer.run_changes(starts) if starts else self.run
                var = self.tracer.run_changes(changes)
                self._cache[key] = (base, var)
            base, var = self._cache[key]
            if base is not None and var is not None:
                out.append((st, base, var))
        return out

    def hypothesis_verdicts(self, seg: Segment) -> list[bool]:
        verdicts = []
        for st, base, var in self.hypothesis_runs(seg):
            norm = normalize(st.text)
            only_kind = all(dict(c).get("kind") in ("loop_kind", "format", "repair") for c in st.changes)
            if lexicon.rx("same_result").search(norm):
                verdicts.append(var.output == base.output and var.error_kind == base.error_kind)
            elif lexicon.rx("differ").search(norm) and not only_kind:
                verdicts.append(var.output != base.output)
            for s in st.slots:
                if s.hypothetical and s.name in claims.CHECKABLE and not s.implied:
                    v = claims.check(s, var, variant=True)
                    if v is not None:
                        verdicts.append(v)
        return verdicts

    def hypothesis_confirmed(self, seg: Segment, concept: str) -> bool:
        if concept not in self.changed_concepts(seg) and concept not in seg.direct:
            return False
        v = self.hypothesis_verdicts(seg)
        return bool(v) and all(v)

    def changed_concepts(self, seg: Segment) -> set[str]:
        """Concepts of the code a stated change touches."""
        out: set[str] = set()
        ctx = self.ctx
        if ctx is None:
            return out
        for st in seg.statements:
            for ch in st.changes:
                c = dict(ch)
                for cs in ctx.stmts:
                    t = cs.text
                    hit = ((c.get("kind") == "loop_kind" and re.match(r"\s*do\b|\s*while\b|\s*for\b", t))
                           or (c.get("kind") == "format" and "printf" in t)
                           or (c.get("kind") == "cast" and re.sub(r"\s+", "", c.get("expr", "")) in re.sub(r"\s+", "", t))
                           or (c.get("kind") == "start" and c.get("var") in cs.reads)
                           or c.get("kind") == "repair")
                    if hit:
                        out |= set(ctx.stmt_concepts.get(cs.index, ()))
                if c.get("kind") == "repair":
                    out |= {lexicon.OUTCOME[k] for k in ("compile_error", "run_error", "compiling", "running")
                            if k in lexicon.OUTCOME}
        return out

    # ------------------------------------------------------------- edge
    def read_edge(self, seg: Segment, edge: "RelEdge") -> Reading:
        return self._cached(seg, f"E:{edge.id}", lambda: self._read_edge(seg, edge))

    def _read_edge(self, seg: Segment, edge: "RelEdge") -> Reading:
        cs = seg.direct if seg.source == "answer" else seg.concepts
        parts = self.kg.parts["edges"].get(edge.id, {}).get("parts", [])
        endpoints = (edge.src, edge.dst)
        # an endpoint is present when the segment names it or points at its code
        present = set(c for c in endpoints if c in cs or (seg.source == "answer" and c in seg.context))
        has_src, has_dst = edge.src in present, edge.dst in present
        if not (has_src or has_dst):
            return Reading(NO)
        if seg.source != "answer":
            if has_src and has_dst:
                return Reading(MATCH, (), f"{seg.source} shows both ends", cls="relation")
            return Reading(NO)
        texts = [p["text"] for p in parts if p["from"] == "logic"] + ([edge.logic] if edge.logic else [])
        sentences = [st.text for st in seg.statements if not st.hypothetical]
        vs = self.variables()
        if any(self.logic.conflict(s, x, vs) for s in sentences for x in texts):
            return Reading(CONTRADICT, (), "same comparison as the edge logic with another operator", cls="relation")
        best = max((self.logic.score(s, x, vs) for s in sentences for x in texts), default=0.0)
        if best >= self.logic.match:
            return Reading(MATCH, (), f"states the edge logic ({best:.2f})", confidence=round(best, 3),
                           cls="relation")
        meaning = self.meaning()
        if meaning is not None:
            # TF-IDF retrieved nothing decisive: compare by meaning (meaning.py)
            sim = max((meaning.states(s, texts, vs) for s in sentences), default=0.0)
            if sim >= meaning.sent_min:
                return Reading(MATCH, (), f"states the edge logic (meaning {sim:.2f})",
                               confidence=round(sim, 3), cls="relation")
        return Reading(NO)

    @staticmethod
    def _part_relevant(part: dict, s: Slot, endpoints: tuple[str, str], cs: frozenset[str]) -> bool:
        """Is slot ``s`` about this part? A slot attached to an endpoint is
        compared only with that endpoint's part (or an untagged part); an
        untagged part counts only when both endpoints are present."""
        pc = part["concept"]
        if s.subject in endpoints:
            return pc is None or pc == s.subject
        if pc is None:
            return all(e in cs for e in endpoints)
        return pc in cs

    # ---------------------------------------------------- misconception
    def read_mis(self, seg: Segment, m: "MisEdge") -> Reading:
        return self._cached(seg, f"M:{m.id}", lambda: self._read_mis(seg, m))

    def _read_mis(self, seg: Segment, m: "MisEdge") -> Reading:
        if seg.source != "answer":
            return Reading(NO)
        info = self.kg.parts["misconceptions"].get(m.id, {})
        spec = info.get("slot")
        kind = (spec or {}).get("slot_kind", "")
        lex_wrong = lex_right = False
        if spec:
            for s in seg.slots:
                if s.implied or s.name != spec["slot"]:
                    continue
                if kind == "example" and s.subject != spec.get("subject"):
                    continue
                if s.subject and not s.subject.startswith(("var:", "expr:")) and s.subject != m.concept \
                        and s.subject in self.kg.knowledge.concepts and kind != "example":
                    continue  # stated about another concept
                w = (s.value == spec["wrong_value"]) != s.negated
                r = (s.value == spec["right_value"]) != s.negated
                if w and not r:
                    lex_wrong = True
                elif r and not w:
                    lex_right = True
        mutant_conf = self._mutant_confirms(seg, m.mis)
        # a stated rule that names no concept is about what the question asks
        unattached_rule = (lex_wrong or lex_right) and kind == "rule" and m.concept in self.focus
        # a misinterpreter run speaks for a misconception only when the statement
        # is about that misconception's concept (one rewrite serves several)
        about = {c for s in mutant_conf for st in seg.statements for c in self.raw_producers(s, st)}
        relevant = m.concept in seg.concepts or unattached_rule or m.concept in about
        if not relevant:
            mutant_conf = []
        if not relevant:
            return Reading(NO)
        wrong_txt = spec["wrong_value"] if spec else m.wrong
        right_txt = spec["right_value"] if spec else m.right
        evidence = f"wrong={wrong_txt}; right={right_txt}"
        if mutant_conf:
            evidence += "; misinterpreter run confirms " + ", ".join(f"{s.name}={s.value!r}" for s in mutant_conf)
            return Reading(MATCH_WRONG, evidence=evidence + self._run_note(), cls="wrong")
        if lex_wrong and kind in ("rule", "example"):
            return Reading(MATCH_WRONG, evidence=evidence + "; the statement states the wrong rule",
                           confidence=0.9, cls="wrong")
        if lex_wrong:
            if self.contradicted_claims(seg):
                return Reading(MATCH_WRONG, evidence=evidence + self._run_note(), cls="wrong")
            no_code = self.trace is None or not (self.trace.program or self.trace.answer_run)
            if no_code and self._breaks_concept(seg, m.concept):
                return Reading(MATCH_WRONG, evidence=evidence + " (no code to confirm)", confidence=0.5, cls="wrong")
            return Reading(NO, evidence="wrong value stated but the code does not support it")
        if lex_right:
            return Reading(CONTRADICT_RIGHT, evidence=f"states the right rule ({right_txt})", cls="rule")
        if not spec and info.get("contrast") and m.concept in seg.direct:
            if self._contrast_match(seg, info["contrast"]):
                return Reading(MATCH_WRONG, evidence=f"uses the wrong belief's terms: {m.wrong}",
                               confidence=0.6, cls="wrong")
        return Reading(NO)

    def _code_decides(self, seg: Segment, mis: str) -> bool:
        """The run can tell this misconception from the correct reading: the
        program runs and the misconception's misinterpreter gives a different
        result. Then only run evidence counts, never wording alone."""
        if not self.trace:
            return False
        if any(st.source == "answer_code" for st in seg.statements):
            real, mut = self.trace.answer_run, self.trace.answer_mutants.get(mis)
        else:
            real, mut = self.trace.run, self.trace.mutants.get(mis)
        if real is None or mut is None or not (real.available or real.error_kind):
            return False
        return mis not in self.trace.indistinguishable and (
            mut.output != real.output or mut.error_kind != real.error_kind or mut.values != real.values)

    def _mutant_confirms(self, seg: Segment, mis: str) -> list[Slot]:
        """Claims the real run contradicts and the misinterpreter run confirms."""
        if not self.trace:
            return []
        out = []
        for st in seg.statements:
            if st.source == "answer_code":
                real, mut = self.trace.answer_run, self.trace.answer_mutants.get(mis)
            else:
                real, mut = self.run_for(st), self.trace.mutants.get(mis)
            if real is None or mut is None:
                continue
            for s in st.slots:
                if s.hypothetical or s.name not in claims.CHECKABLE or s.name == "expr":
                    continue
                if not self._checkable(s, st):
                    continue
                if claims.check(s, mut) is True and claims.check(s, real) is False:
                    out.append(s)
        return out

    def _run_note(self) -> str:
        run = self.run
        if run is not None and (run.available or run.error_kind):
            return f"; real run: {_run_text(run)}"
        return ""

    def _contrast_match(self, seg: Segment, contrast: dict) -> bool:
        words = set()
        for w in re.findall(r"[a-z][a-z]+", normalize(seg.text)):
            words.add(re.sub(r"(?:ing|ed|es|s)$", "", w) if len(w) > 5 else w)
        wrong = [t for t in contrast["wrong_terms"] if t in words]
        right = [t for t in contrast["right_terms"] if t in words]
        return len(wrong) >= 3 and not right

    def _breaks_concept(self, seg: Segment, concept: str) -> bool:
        """A stated slot (about this concept or unattached) disagrees with a
        single-valued slot of one of the concept's L1/L2 way rules."""
        for level in ("L1", "L2"):
            for row in self.kg.parts["ways"].get(concept, {}).get(level, []):
                vals: dict[str, set[str]] = {}
                for name, value, *_ in row["slots"]:
                    vals.setdefault(name, set()).add(value)
                for s in seg.slots:
                    if s.implied or s.subject != concept:
                        continue
                    v = vals.get(s.name)
                    if v and len(v) == 1 and slot_agrees(s, s.name, next(iter(v))) is False:
                        return True
        return False

    # -------------------------------------------------------------- NLI
    def _nli_read(self, seg: Segment, premise: str) -> Reading:
        if self._nli is None:
            from .nli import NLI

            self._nli = NLI()
        label = self._nli.entails(premise, seg.text)  # type: ignore[attr-defined]
        if label:
            return Reading(MATCH_NLI, evidence="NLI entailment", confidence=0.6, cls="rule")
        return Reading(NO)


_CLASS_RANK = {"named": 0, "rule": 1, "relation": 2, "run": 3, "diagnosis": 4, "hypothetical": 4}


def _run_text(run) -> str:
    if run.error_kind == "compile":
        return f"compile error ({run.error})"
    if run.error_kind == "run":
        return f"run-time error ({run.error})"
    if run.error_kind == "timeout":
        return "does not stop"
    return f"prints {run.output.strip()!r}"
