"""Meaning reader: student wording -> the meaning of edge logic (no LLM, no code run).

The edge logic of the graph is fixed; what changes from student to student is
the wording. So reading is split in two:

1. **what the student means** (dynamic). The clause is cut into phrases with a
   dependency parse (spaCy: noun chunks, verb phrases with their objects,
   particles and modifiers; a phrase is negated when it holds or governs a
   negation). Each phrase is compared by meaning (a small pretrained sentence
   encoder, all-MiniLM-L6-v2, run locally) with the phrases of the edge logic.
2. **is that meaning right** (fixed). For a misconception edge only the
   phrases that tell the two sides apart count: phrases of the wrong belief
   with an anchor the correct rule lacks, and the reverse. The side whose
   distinguishing phrases the clause comes closest to wins (a phrase under the
   opposite polarity supports the other side). Relation edges and level ways
   are matched by the meaning of the whole sentence.

TF-IDF (edgelogic) only retrieves: an edge is compared only when the clause
shares an anchor with it. All thresholds come from graph texts only
(``calibrate``): the graph's restatements of correct rules and wrong beliefs
must land on their side, unrelated far-apart texts must not match.
"""

from __future__ import annotations

from functools import lru_cache
from typing import TYPE_CHECKING, Iterable

import numpy as np

from . import lexicon

if TYPE_CHECKING:  # pragma: no cover
    from .edgelogic import EdgeLogicReader
    from .graph import KG

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
_PHRASE_DEPS = {"dobj", "pobj", "prt", "advmod", "acomp", "attr", "prep", "xcomp", "neg", "dative", "oprd"}


class MeaningReader:
    def __init__(self, kg: "KG", logic: "EdgeLogicReader") -> None:
        import spacy
        from sentence_transformers import SentenceTransformer

        self.kg, self.logic = kg, logic
        self.nlp = spacy.load("en_core_web_sm", disable=["ner"])
        self.enc = SentenceTransformer(MODEL_NAME)
        self._emb: dict[str, np.ndarray] = {}
        self._phr: dict[str, list[tuple[str, bool]]] = {}
        self._keys: dict[tuple[str, str], tuple[list, list]] = {}
        self.side_min, self.margin, self.sent_min = 0.5, 0.05, 0.6
        self.side_min, self.margin, self.sent_min = self.calibrate()

    # ----------------------------------------------------------- encoder
    def embed(self, texts: list[str]) -> np.ndarray:
        missing = [t for t in dict.fromkeys(texts) if t not in self._emb]
        if missing:
            for t, v in zip(missing, self.enc.encode(missing, normalize_embeddings=True, batch_size=64)):
                self._emb[t] = v
        return np.stack([self._emb[t] for t in texts]) if texts else np.zeros((0, 384))

    def sim(self, a: str, b: str) -> float:
        va, vb = self.embed([a, b])
        return float(va @ vb)

    # ----------------------------------------------------------- phrases
    def words(self, phrase: str) -> frozenset[str]:
        """Content words of a phrase (no variables, numbers or operators):
        what a meaning comparison can judge."""
        return frozenset(t for t in self.logic.tokens(phrase)
                         if t != "VAR" and t.replace("not_", "")[:1].isalpha())

    def phrases(self, text: str, whole: bool = False) -> list[tuple[str, bool]]:
        """(phrase, negated) of a text: noun chunks and verb / adjective
        phrases with a content word; the whole sentences only when asked or
        when there is no such phrase."""
        key = text + ("|whole" if whole else "")
        if key in self._phr:
            return self._phr[key]
        doc = self.nlp(text or "")
        out: dict[str, bool] = {}

        def add(tokens) -> None:
            toks = sorted(tokens, key=lambda t: t.i)
            if not toks:
                return
            words = [t.text for t in toks]
            s = " ".join(words).strip()
            if len(s) < 2:
                return
            # negated when the negation attaches to the phrase's head word
            # ("no" in "behave the same (no newline difference)" negates
            # "difference", not "behave")
            ids = {t.i for t in toks}
            root = next((t for t in toks if t.head.i not in ids or t.head.i == t.i), toks[0])
            neg = any(c.dep_ == "neg" or c.lower_ in lexicon.NEGATION for c in root.children)
            out[s] = out.get(s, False) or neg

        for chunk in doc.noun_chunks:
            add(list(chunk))
        for tok in doc:
            if tok.pos_ in ("VERB", "AUX", "ADJ"):
                span = [tok]
                for ch in tok.children:
                    if ch.dep_ in _PHRASE_DEPS:
                        span.extend(t for t in ch.subtree)
                if 1 < len(span) <= 14:
                    add(span)
        res = [(s, n) for s, n in out.items() if self.words(s)]
        if whole or not res:
            res += [(str(s).strip(), False) for s in doc.sents if self.words(str(s))]
        self._phr[key] = res
        return res

    def keys(self, a: str, b: str) -> tuple[list[tuple[str, bool]], list[tuple[str, bool]]]:
        """The phrases of a and of b that tell them apart: a phrase counts for
        its side when it has a content anchor the other side lacks."""
        k = (a, b)
        if k in self._keys:
            return self._keys[k]
        def distinct(text: str, other: str) -> list[tuple[str, bool]]:
            # a phrase tells its side apart when no single phrase of the other
            # side holds all its content words
            others = [self.words(q) for q, _ in self.phrases(other)]
            return [(p, n) for p, n in self.phrases(text)
                    if not any(self.words(p) <= o for o in others)]

        res = (distinct(a, b), distinct(b, a))
        self._keys[k] = res
        return res

    # ------------------------------------------------------------- reads
    def side_scores(self, clause: str, a: str, b: str) -> tuple[float, float]:
        """How close the clause's phrases come to a's and to b's distinguishing
        phrases; a phrase of opposite polarity counts for the other side."""
        ka, kb = self.keys(a, b)
        ps = self.phrases(clause)
        if not ps or not ka or not kb:
            return 0.0, 0.0
        P = self.embed([p for p, _ in ps])
        sa = sb = 0.0
        for keys, mine in ((ka, "a"), (kb, "b")):
            K = self.embed([k for k, _ in keys])
            S = P @ K.T
            for i, (_, pn) in enumerate(ps):
                for j, (_, kn) in enumerate(keys):
                    v = float(S[i, j])
                    to_a = (mine == "a") == (pn == kn)
                    if to_a:
                        sa = max(sa, v)
                    else:
                        sb = max(sb, v)
        return sa, sb

    def side(self, clause: str, a: str, b: str, variables: Iterable[str] = ()) -> tuple[str | None, float]:
        """("a" | "b" | None, closeness): which of two opposite texts the clause
        means. Retrieved only when the clause shares an anchor with them."""
        if max(self.logic.score(clause, a, variables), self.logic.score(clause, b, variables)) <= 0:
            return None, 0.0
        sa, sb = self.side_scores(clause, a, b)
        best = max(sa, sb)
        if best < self.side_min or abs(sa - sb) < self.margin:
            return None, best
        return ("a" if sa > sb else "b"), best

    def states(self, clause: str, texts: list[str], variables: Iterable[str] = ()) -> float:
        """Best meaning similarity of the clause with any of the texts (or their
        sentences) it shares an anchor with; 0 when none is retrieved."""
        best = 0.0
        for t in texts:
            if not t or self.logic.score(clause, t, variables) <= 0:
                continue
            parts = [t] + [s for s, _ in self.phrases(t, whole=True) if len(s) > 8]
            sims = self.embed([clause]) @ self.embed(parts).T
            best = max(best, float(sims.max()))
        return best

    # ------------------------------------------------------- calibration
    def calibrate(self) -> tuple[float, float, float]:
        """Thresholds from graph texts only.

        * side: each misconception node's own restatement of its correct rule
          and of its wrong belief is read against the edge's two sides. The
          margin is the larger of the lead that at most 10% of restatements
          give to the wrong side and the lead that at most 5% of restatements
          of an unrelated misconception (concepts four or more hops apart)
          give to either side.
        * sentence: the graph's paraphrase pairs must reach it (10th
          percentile), unrelated far-apart edge logic must not (95th).
        """
        from .edgelogic import _graph_pairs

        nodes = {m["id"]: m for m in self.kg.knowledge.raw.get("misconceptions_and_errors", [])}
        edges = [m for ms in self.kg.mis_edges.values() for m in ms if m.wrong and m.right]
        wrong_lead, close, far = [], [], []
        for i, m in enumerate(edges):
            node = nodes.get(m.mis, {})
            for text, own in ((node.get("correct_rule"), "b"), (node.get("wrong_belief"), "a")):
                if not text or text in (m.wrong, m.right):
                    continue
                sa, sb = self.side_scores(text, m.wrong, m.right)
                wrong_lead.append((sa - sb) if own == "b" else (sb - sa))
                close.append(max(sa, sb))
            other = edges[(i * 7 + 3) % len(edges)]
            o_node = nodes.get(other.mis, {})
            if o_node.get("correct_rule") and self.kg.hop_distance(m.concept, other.concept) >= 4:
                fa, fb = self.side_scores(o_node["correct_rule"], m.wrong, m.right)
                far.append(abs(fa - fb))
        margin = None
        if wrong_lead and far:
            wrong_lead.sort(); far.sort()
            margin = round(max(0.02, wrong_lead[int(0.9 * (len(wrong_lead) - 1))],
                               far[int(0.95 * (len(far) - 1))]), 3)
        side_min = 0.0   # TF-IDF retrieval and the margin decide
        pos, neg = _graph_pairs(self.kg)
        ps = sorted(self.sim(a, b) for a, b in pos)
        ns = sorted(self.sim(a, b) for a, b in neg)
        sent_min = round(max(ps[int(0.1 * len(ps))], ns[int(0.95 * (len(ns) - 1))]), 3) if ps and ns else 0.6
        return side_min, margin or 0.05, sent_min


@lru_cache(maxsize=4)
def _meaning_for(kg_id: int, kg: "KG", logic: "EdgeLogicReader") -> MeaningReader:
    return MeaningReader(kg, logic)


def meaning_for(kg: "KG", logic: "EdgeLogicReader") -> MeaningReader:
    return _meaning_for(id(kg), kg, logic)
