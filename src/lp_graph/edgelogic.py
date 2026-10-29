"""Edge-logic reader: which edge logic, and which side of it, a clause expresses.

In the graph every piece of knowledge is edge logic:

* a relation edge (prerequisite / parallel) has its ``logic`` (and parts);
* a misconception edge has ``logic`` (the wrong belief) and ``twin_logic``
  (the correct rule);
* a has_level edge has one ``edge_logic`` text per way of reaching the level.

``EdgeLogicReader`` compares a student clause with any of these texts by the
**anchors** they share: code tokens (operators, ``length``, ``println``),
numbers and content words (stop words dropped, simple suffixes stripped; both
lists are in the graph's language section). Each anchor is weighted by how
rare it is across all edge-logic texts of the graph (inverse document
frequency), so ``minus``, ``%`` or ``starting`` count for more than ``value``.
Program variables (and the one-letter names of graph examples) all become the
anchor ``VAR``, so ``sensorReadings.length - 2`` and ``a.length - 1`` share
``VAR length -``.

* ``score(clause, text)`` - the harmonic mean of how much of the clause the
  text explains and how much of the text the clause covers (best over the
  text's sentences);
* ``side(clause, a, b)`` - which of two opposite texts the clause expresses:
  the higher score, with negation breaking a near tie;
* ``conflict(clause, text)`` - the same comparison with a different operator
  (``i <= a.length`` against ``i < a.length``).

The match threshold is fixed from graph pairs only (``calibrate``): pairs the
graph states as paraphrases must match, unrelated far-apart edges must not.
No student answer and no gold label is used.
"""

from __future__ import annotations

import math
import re
from functools import lru_cache
from typing import TYPE_CHECKING, Iterable

from . import lexicon

if TYPE_CHECKING:  # pragma: no cover
    from .graph import KG

_TOKEN = re.compile(r"<=|>=|==|!=|\+\+|--|\+=|-=|\*=|/=|&&|\|\||[A-Za-z_][A-Za-z_0-9]*|\d+(?:\.\d+)?|[%<>/*+\-=!]")
_COMPARE = re.compile(r"([A-Za-z_][\w.]*|\d+)\s*(<=|>=|<|>|==|!=)\s*([A-Za-z_][\w.]*(?:\s*[-+]\s*\d+)?|\d+)")
_SENT = re.compile(r"(?<=[.;!?])\s+|\s+(?=(?:while|whereas|but)\s)")
DEFAULT_MATCH = 0.3


class EdgeLogicReader:
    def __init__(self, kg: "KG") -> None:
        self.kg = kg
        texts = list(_graph_texts(kg))
        df: dict[str, int] = {}
        for t in texts:
            for tok in set(self.tokens(t)):
                df[tok] = df.get(tok, 0) + 1
        n = max(1, len(texts))
        self.idf = {tok: math.log((n + 1) / (c + 1)) + 1.0 for tok, c in df.items()}
        self.default_idf = math.log(n + 1) + 1.0
        self.match = DEFAULT_MATCH
        self.match = self.calibrate()
        self.margin = 0.0
        self.margin = self.calibrate_margin()

    # ------------------------------------------------------------ tokens
    def tokens(self, text: str, variables: Iterable[str] = ()) -> list[str]:
        vars_ = {v.lower() for v in variables}
        out = []
        negated = 0  # content words still inside the scope of "no" / "not"
        for raw in _TOKEN.findall(text or ""):
            tok = raw.lower()
            if tok[0].isalpha() or tok[0] == "_":
                if tok in lexicon.NEGATION:
                    negated = 3
                    continue
                if tok in vars_ or (len(tok) == 1 and raw.islower()) or re.search(r"\d", tok) or (
                        raw != raw.lower() and raw[0].islower() and not raw.isupper()):
                    out.append("VAR")
                    continue
                if tok in lexicon.STOPWORDS:
                    continue
                for suf in lexicon.SUFFIXES:
                    if len(tok) > len(suf) + 3 and tok.endswith(suf):
                        tok = tok[: -len(suf)]
                        break
                if len(tok) > 4 and tok.endswith("e"):  # estimate / estimates / estimated
                    tok = tok[:-1]
                if negated:  # "no newline difference" does not share "newline" with "adds a newline"
                    tok = "not_" + tok
                    negated -= 1
            out.append(tok)
        return out

    def weight(self, tok: str) -> float:
        return self.idf.get(tok, self.default_idf)

    # ------------------------------------------------------------- score
    def _score_one(self, a: list[str], b: list[str]) -> float:
        sa, sb = set(a), set(b)
        if not sa or not sb:
            return 0.0
        shared = sum(self.weight(t) for t in sa & sb)
        if shared == 0:
            return 0.0
        ca = shared / sum(self.weight(t) for t in sa)
        cb = shared / sum(self.weight(t) for t in sb)
        return 2 * ca * cb / (ca + cb)

    def score(self, clause: str, text: str, variables: Iterable[str] = ()) -> float:
        """Best match of the clause with the text or one of its sentences."""
        a = self.tokens(clause, variables)
        parts = [text] + [p for p in _SENT.split(text or "") if len(p) > 8]
        return max((self._score_one(a, self.tokens(p)) for p in parts), default=0.0)

    def matches(self, clause: str, text: str, variables: Iterable[str] = ()) -> bool:
        return self.score(clause, text, variables) >= self.match

    @staticmethod
    def negated(text: str) -> bool:
        words = re.findall(r"[a-z]+", (text or "").lower())
        return any(w in lexicon.NEGATION for w in words)

    def side(self, clause: str, a: str, b: str, variables: Iterable[str] = ()) -> tuple[str | None, float]:
        """("a" | "b" | None, best score): which of two opposite texts the
        clause expresses. The clause must be about them (best score at least
        ``match``); then only the anchors that tell the two sides apart count -
        those of a missing from b and of b missing from a. The side whose
        distinguishing anchors the clause uses more wins; with none on either
        side, negation decides (the side whose polarity equals the clause's),
        else None."""
        sa, sb = self.score(clause, a, variables), self.score(clause, b, variables)
        best = max(sa, sb)
        if best < self.match:
            return None, best
        c = set(self.tokens(clause, variables))
        ta, tb = set(self.tokens(a)), set(self.tokens(b))
        only_a = sum(self.weight(t) for t in c & (ta - tb))
        only_b = sum(self.weight(t) for t in c & (tb - ta))
        if only_a != only_b and max(only_a, only_b) > 0:
            return ("a" if only_a > only_b else "b"), best
        neg = self.negated(clause)
        pa, pb = self.negated(a) == neg, self.negated(b) == neg
        if pa != pb:
            return ("a" if pa else "b"), best
        return None, best

    def conflict(self, clause: str, text: str, variables: Iterable[str] = ()) -> bool:
        """The clause compares the same things as the text with another operator."""
        def comps(t: str, vs: Iterable[str]) -> list[tuple[str, str, str]]:
            out = []
            for m in _COMPARE.finditer(t or ""):
                left = " ".join(self.tokens(m.group(1), vs)) or m.group(1)
                right = " ".join(self.tokens(m.group(3), vs)) or m.group(3)
                out.append((left, m.group(2), right))
            return out
        mine, theirs = comps(clause, variables), comps(text, ())
        return any(l1 == l2 and r1 == r2 and o1 != o2 for l1, o1, r1 in mine for l2, o2, r2 in theirs)

    # ------------------------------------------------------- calibration
    def calibrate_margin(self) -> float:
        """Margin from graph pairs only. For every misconception whose node
        restates its wrong belief or its correct rule in other words, score the
        restatement against both sides of the edge. The margin is the smallest
        lead that at most 10% of the correct-rule restatements have towards the
        wrong side (so a correct statement is rarely flagged)."""
        nodes = {m["id"]: m for m in self.kg.knowledge.raw.get("misconceptions_and_errors", [])}
        leads_right = []
        for ms in self.kg.mis_edges.values():
            for m in ms:
                node = nodes.get(m.mis, {})
                cr = node.get("correct_rule")
                if m.wrong and m.right and cr and cr != m.right:
                    leads_right.append(self.score(cr, m.wrong) - self.score(cr, m.right))
        if not leads_right:
            return 0.1
        leads_right.sort()
        return round(max(0.05, leads_right[int(0.9 * (len(leads_right) - 1))]), 3)

    def calibrate(self) -> float:
        """Threshold from graph pairs only: the smallest score that 90% of the
        graph's paraphrase pairs reach, raised until at most 5% of unrelated
        far-apart edge parts pass."""
        pos, neg = _graph_pairs(self.kg)
        ps = sorted(self.score(a, b) for a, b in pos)
        ns = sorted(self.score(a, b) for a, b in neg)
        if not ps or not ns:
            return DEFAULT_MATCH
        t = ps[int(0.1 * len(ps))]
        cap = ns[min(len(ns) - 1, int(0.95 * len(ns)))]
        return round(max(t, cap, 0.1), 3)


def _graph_texts(kg: "KG") -> Iterable[str]:
    for e in kg.relation_edges.values():
        if e.logic:
            yield e.logic
        if e.contrast:
            yield e.contrast
    for ms in kg.mis_edges.values():
        for m in ms:
            if m.wrong:
                yield m.wrong
            if m.right:
                yield m.right
    for c in kg.concepts:
        for lv in ("L0", "L1", "L2", "L3", "L4"):
            for w in kg.ways(c, lv):
                if w.text:
                    yield w.text


def _graph_pairs(kg: "KG") -> tuple[list[tuple[str, str]], list[tuple[str, str]]]:
    """Paraphrases the graph states (an edge's correct rule and its node's
    correct rule; an edge's wrong belief and the node's) and unrelated pairs
    (logic of edges four or more hops apart)."""
    nodes = {m["id"]: m for m in kg.knowledge.raw.get("misconceptions_and_errors", [])}
    pos = []
    for ms in kg.mis_edges.values():
        for m in ms:
            node = nodes.get(m.mis, {})
            if m.right and node.get("correct_rule") and m.right != node["correct_rule"]:
                pos.append((m.right, node["correct_rule"]))
            if m.wrong and node.get("wrong_belief") and m.wrong != node["wrong_belief"]:
                pos.append((m.wrong, node["wrong_belief"]))
    edges = sorted(kg.relation_edges.values(), key=lambda e: e.id)
    neg = []
    for i, e in enumerate(edges):
        f = edges[(i * 7 + 3) % len(edges)]
        if e.logic and f.logic and kg.hop_distance(e.src, f.src) >= 4:
            neg.append((e.logic, f.logic))
    return pos, neg


@lru_cache(maxsize=4)
def _reader_for(kg_id: int, kg: "KG") -> EdgeLogicReader:
    return EdgeLogicReader(kg)


def reader_for(kg: "KG") -> EdgeLogicReader:
    """One reader per graph (its IDF table and threshold are built once)."""
    return _reader_for(id(kg), kg)
