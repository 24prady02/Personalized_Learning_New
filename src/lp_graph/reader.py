"""Step 3 of the pipeline - the reader: MATCH | CONTRADICT | NO.

``Reader.read_*`` compares a *segment* (1-3 consecutive statements, so a
contrast split over two clauses can be read as one) with one candidate
element:

* **Concept way (stay)** - the segment's slots against the slots of the
  concept's has_level way rules (L1-L4). MATCH if every addressed slot
  agrees, CONTRADICT if one disagrees. ``names_the_element`` (L1) matches
  when the concept is named and nothing contradicts it; output-prediction
  and trace ways (L2) also match when the real run confirms a claim.
* **Relation edge** - against the edge-logic parts in ``kg.parts``. MATCH
  only if both endpoints are named (directly, or through a code variable /
  pronoun) and every addressed part agrees *with the slot attached to the
  part's own concept* ("println stays on the same line" is compared with
  the println part, not the print part). CONTRADICT if a part disagrees.
* **Misconception pair** - MATCH_WRONG if the segment states the wrong
  value (``kg.parts`` misconception slot) and the code backs that reading:
  the real run contradicts the statement, or the misinterpreter run
  (``trace.mutants[mis]``) confirms it. CONTRADICT_RIGHT if it states the
  right value. A statement the real run contradicts with no misconception
  matched is WRONG_UNLISTED.

Code and question segments are the truth: they MATCH every concept and
edge they show unless a part contradicts the run, and never a misconception.

With ``use_nli`` an optional cross-encoder may label relation-edge parts and
ways that have no slots (MATCH_NLI, lower confidence); it is never used for
misconceptions.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Sequence

from . import claims
from .slots import Slot, slot_agrees

if TYPE_CHECKING:  # pragma: no cover
    from .execution import Trace
    from .graph import KG, MisEdge, RelEdge
    from .statements import Statement

MATCH = "MATCH"
MATCH_NLI = "MATCH_NLI"
CONTRADICT = "CONTRADICT"
NO = "NO"
MATCH_WRONG = "MATCH-WRONG"
CONTRADICT_RIGHT = "CONTRADICT-RIGHT"
WRONG_UNLISTED = "WRONG_UNLISTED"

ENTERS = frozenset({MATCH, MATCH_NLI, MATCH_WRONG})
L2_RUN_WAYS = frozenset({"OP", "OS", "LT"})


@dataclass(frozen=True)
class Reading:
    label: str
    part_ids: tuple[str, ...] = ()
    evidence: str = ""
    confidence: float = 1.0
    ways: tuple[tuple[str, int, str], ...] = ()   # (level, index, way) matched

    def to_dict(self) -> dict:
        d = {"label": self.label, "evidence": self.evidence}
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
        return self.statements[0].source

    @property
    def concepts(self) -> frozenset[str]:
        return frozenset(c for s in self.statements for c in s.concepts)

    @property
    def slots(self) -> tuple[Slot, ...]:
        return tuple(sl for s in self.statements for sl in s.slots)

    @property
    def text(self) -> str:
        return " / ".join(s.text for s in self.statements)


@dataclass
class Reader:
    kg: "KG"
    trace: "Trace | None"
    main_concept: str | None = None
    use_nli: bool = False
    _cache: dict = field(default_factory=dict)
    _nli: object = None

    # ---------------------------------------------------------- helpers
    def _cached(self, seg: Segment, key: str, fn) -> Reading:
        k = (seg.ids, key)
        if k not in self._cache:
            self._cache[k] = fn()
        return self._cache[k]

    @property
    def run(self):
        return self.trace.run if self.trace else None

    def contradicted_claims(self, seg: Segment) -> list[Slot]:
        if seg.source != "answer" or self.run is None:
            return []
        return claims.contradicted(seg.slots, self.run)

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
            return Reading(MATCH, evidence=f"{seg.source} shows {concept}")
        if concept in fault:
            bad = self.contradicted_claims(seg)
            return Reading(CONTRADICT, evidence="real run contradicts: "
                           + ", ".join(f"{s.name}={s.value}" for s in bad))
        matched, contra = [], []
        for level in ("L1", "L2", "L3", "L4"):
            for row in self.kg.parts["ways"].get(concept, {}).get(level, []):
                r = self.read_way(seg, concept, level, row)
                if r.label in (MATCH, MATCH_NLI):
                    matched.append((level, row["index"], row["way"]))
                elif r.label == CONTRADICT:
                    contra.append((level, row["index"], row["way"]))
        strong = [m for m in matched if m[2] != "names_the_element"]
        if contra and not strong:
            return Reading(CONTRADICT, evidence="contradicts way " + ", ".join(
                f"{lv} {w}" for lv, _, w in contra), ways=tuple(contra))
        if matched:
            return Reading(MATCH, evidence="matches " + ", ".join(
                f"{lv} {w}" for lv, _, w in matched), ways=tuple(matched))
        return Reading(NO)

    def read_way(self, seg: Segment, concept: str, level: str, row: dict) -> Reading:
        """One has_level way of ``concept`` against an answer segment."""
        return self._cached(seg, f"W:{concept}:{level}:{row['index']}",
                            lambda: self._read_way(seg, concept, level, row))

    def _read_way(self, seg: Segment, concept: str, level: str, row: dict) -> Reading:
        if concept not in seg.concepts:
            return Reading(NO)
        by_name: dict[str, set[str]] = {}
        for name, value, *_ in row["slots"]:
            by_name.setdefault(name, set()).add(value)
        usable = {n: next(iter(v)) for n, v in sorted(by_name.items()) if len(v) == 1}
        agree = disagree = 0
        for s in seg.slots:
            if s.name not in usable:
                continue
            ok = slot_agrees(s, s.name, usable[s.name])
            if ok is True and not s.implied:
                agree += 1
            elif ok is False:
                disagree += 1
        if disagree:
            return Reading(CONTRADICT, evidence=f"{level} {row['way']}: slot disagrees")
        if level == "L2" and row["rule_type"] in L2_RUN_WAYS and self.run is not None:
            if claims.confirmed(seg.slots, self.run):
                return Reading(MATCH, evidence=f"{level} {row['way']}: real run confirms")
            if self.contradicted_claims(seg) and row["rule_type"] == "OP":
                return Reading(CONTRADICT, evidence=f"{level} {row['way']}: real run contradicts")
        if agree:
            return Reading(MATCH, evidence=f"{level} {row['way']}: slots agree")
        if row["way"] == "names_the_element":
            return Reading(MATCH, evidence="names the concept", confidence=0.5)
        if self.use_nli and not row["slots"]:
            return self._nli_read(seg, " ".join(w.text for w in self.kg.ways(concept, level)
                                                if w.index == row["index"]))
        return Reading(NO)

    # ------------------------------------------------------------- edge
    def read_edge(self, seg: Segment, edge: "RelEdge") -> Reading:
        return self._cached(seg, f"E:{edge.id}", lambda: self._read_edge(seg, edge))

    def _read_edge(self, seg: Segment, edge: "RelEdge") -> Reading:
        cs = seg.concepts
        has_src, has_dst = edge.src in cs, edge.dst in cs
        if not (has_src or has_dst):
            return Reading(NO)
        parts = self.kg.parts["edges"].get(edge.id, {}).get("parts", [])
        endpoints = (edge.src, edge.dst)
        agree_parts: list[str] = []
        bad_parts: list[str] = []
        for s in seg.slots:
            outcomes = []
            for p in parts:
                if not self._part_relevant(p, s, endpoints, cs):
                    continue
                vals = [v for n, v, *_ in p["slots"] if n == s.name]
                if not vals:
                    continue
                ok = any(slot_agrees(s, s.name, v) for v in vals)
                outcomes.append((p["id"], ok))
            if not outcomes:
                continue
            subj_is_endpoint = s.subject in endpoints
            if not subj_is_endpoint and len({ok for _, ok in outcomes}) > 1:
                continue  # an unattached slot that fits one part and not the other says nothing
            for pid, ok in outcomes:
                if ok and not s.implied:
                    agree_parts.append(pid)
                elif not ok:
                    bad_parts.append(pid)
        if seg.source != "answer":
            if has_src and has_dst and not bad_parts:
                return Reading(MATCH, tuple(sorted(set(agree_parts))), f"{seg.source} shows both ends")
            return Reading(NO)
        # a contradiction needs both ends named, or a slot attached to an endpoint
        attached = any(s.subject in endpoints for s in seg.slots)
        if bad_parts and ((has_src and has_dst) or attached):
            return Reading(CONTRADICT, tuple(sorted(set(bad_parts))),
                           "statement disagrees with " + ", ".join(sorted(set(bad_parts))))
        if has_src and has_dst and agree_parts:
            return Reading(MATCH, tuple(sorted(set(agree_parts))), "all addressed parts agree")
        if has_src and has_dst and self.use_nli:
            return self._nli_read(seg, edge.logic + " " + edge.contrast)
        return Reading(NO)

    @staticmethod
    def _part_relevant(part: dict, s: Slot, endpoints: tuple[str, str], cs: frozenset[str]) -> bool:
        """Is slot ``s`` about this part? A slot attached to an endpoint is
        compared only with that endpoint's part (or an untagged part); an
        untagged part counts only when both endpoints are named."""
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
        lex_wrong = lex_right = False
        if spec:
            for s in seg.slots:
                if s.implied or s.name != spec["slot"]:
                    continue
                # exact value equality here: "0" is not the word "default"
                w = (s.value == spec["wrong_value"]) != s.negated
                r = (s.value == spec["right_value"]) != s.negated
                if w and not r:
                    lex_wrong = True
                elif r and not w:
                    lex_right = True
        run = self.run
        real_contra = bool(run is not None and claims.contradicted(seg.slots, run))
        mutant = self.trace.mutants.get(m.mis) if self.trace else None
        mutant_conf: list[Slot] = []
        if mutant is not None and run is not None:
            mutant_conf = [s for s in seg.slots if s.name in claims.CHECKABLE
                           and claims.check(s, mutant) is True and claims.check(s, run) is False]
        relevant = m.concept in seg.concepts or bool(mutant_conf)
        if not relevant:
            return Reading(NO)
        if lex_wrong or mutant_conf:
            evidence = (f"wrong={spec['wrong_value'] if spec else m.wrong}; "
                        f"right={spec['right_value'] if spec else m.right}")
            if mutant_conf:
                evidence += "; misinterpreter run confirms " + ", ".join(
                    f"{s.name}={s.value}" for s in mutant_conf)
            if run is not None and (run.available or run.error_kind):
                evidence += f"; real run: {_run_text(run)}"
            if real_contra or mutant_conf:
                return Reading(MATCH_WRONG, evidence=evidence)
            no_code = self.trace is None or not self.trace.program
            # without code, the wrong value must also break the concept's own rule
            if lex_wrong and no_code and self._breaks_concept(seg, m.concept):
                return Reading(MATCH_WRONG, evidence=evidence + " (no code to confirm)", confidence=0.5)
            return Reading(NO, evidence="wrong value stated but the code does not support it")
        if lex_right:
            return Reading(CONTRADICT_RIGHT, evidence=f"states the right rule ({spec['right_value']})")
        return Reading(NO)

    def _breaks_concept(self, seg: Segment, concept: str) -> bool:
        """A stated slot (about this concept or unattached) disagrees with a
        single-valued slot of one of the concept's L1/L2 way rules."""
        for level in ("L1", "L2"):
            for row in self.kg.parts["ways"].get(concept, {}).get(level, []):
                vals: dict[str, set[str]] = {}
                for name, value, *_ in row["slots"]:
                    vals.setdefault(name, set()).add(value)
                for s in seg.slots:
                    if s.implied or (s.subject and s.subject != concept
                                     and not s.subject.startswith("var:")):
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
            return Reading(MATCH_NLI, evidence="NLI entailment", confidence=0.6)
        return Reading(NO)


def _run_text(run) -> str:
    if run.error_kind == "compile":
        return f"compile error ({run.error})"
    if run.error_kind == "run":
        return f"run-time error ({run.error})"
    if run.error_kind == "timeout":
        return "does not stop"
    return f"prints {run.output.strip()!r}"
