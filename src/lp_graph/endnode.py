"""Reading the end node of a concept's misconception and level edges.

A relation edge has both ends known (two concepts found in the code), so
reading it is a question of topic. A misconception or level edge has only its
start known (the concept); its end must be chosen among siblings that share
almost all their words. That is done in two steps, like concepts are found:

1. **PageRank finds the candidate end nodes.** Personalized PageRank runs over
   concepts *and* misconception nodes (a misconception is linked to every
   concept it is attached to). One sentence seeds its concepts (named 1, pointed
   at 0.5) and the misconceptions whose wrong belief shares anchors with it
   (TF-IDF score). Sibling misconceptions of a concept differ in which other
   concepts they connect to, so the graph separates them. Per concept, the
   siblings with at least the average rank are the candidates.
2. **Reading the edge logic decides.** The sentence is compared with every
   candidate's wrong belief and with the concept's correct rules at once; only
   phrases that tell one text apart from all the others count (meaning.py).
   The closest text wins if it leads the next one by the graph-calibrated
   margin. If a correct rule wins, no misconception is held and the
   candidates count against.

The **level** end node is read from the *form* of the reasoning, which the
statement already records: a what-if (hypothetical / stated change) -> L4; a
link word (because, so ...) between two concepts -> L3; a stated value,
output or run -> L2; otherwise a rule -> L1. Similarity to the concept's way
texts only confirms that the sentence is about the concept.
"""

from __future__ import annotations

from functools import lru_cache
from typing import TYPE_CHECKING

import numpy as np

from . import lexicon
from .candidates import EDGE_WEIGHT, MAX_ITER, RESTART, TOL

if TYPE_CHECKING:  # pragma: no cover
    from .candidates import Candidates
    from .graph import KG
    from .reader import Reader
    from .statements import Statement


# ------------------------------------------------------------- PageRank
@lru_cache(maxsize=4)
def _matrix(kg_id: int, kg: "KG") -> tuple[dict[str, int], np.ndarray, np.ndarray]:
    names = list(kg.concepts) + sorted({"mis:" + m.mis for ms in kg.mis_edges.values() for m in ms})
    idx = {n: i for i, n in enumerate(names)}
    w = np.zeros((len(names), len(names)))
    for eid in sorted(kg.relation_edges):
        e = kg.relation_edges[eid]
        a, b = idx[e.src], idx[e.dst]
        w[a, b] += EDGE_WEIGHT[e.kind]
        w[b, a] += EDGE_WEIGHT[e.kind]
    for c, ms in kg.mis_edges.items():
        for m in ms:
            a, b = idx[c], idx["mis:" + m.mis]
            w[a, b] += 1.0
            w[b, a] += 1.0
    deg = w.sum(axis=1)
    p = np.divide(w, deg[:, None], out=np.zeros_like(w), where=deg[:, None] > 0)
    return idx, p, deg


def mis_rank(kg: "KG", reader: "Reader", st: "Statement", mis_edges) -> dict[str, float]:
    """PageRank of each misconception node, seeded by one sentence."""
    idx, p, deg = _matrix(id(kg), kg)
    s = np.zeros(len(idx))
    for c in st.direct:
        if c in idx:
            s[idx[c]] += 1.0
    for c in st.concepts:
        if c in idx and c not in st.direct:
            s[idx[c]] += 0.5
    vs = reader.variables()
    for m in mis_edges:
        if m.wrong:
            sc = reader.logic.score(st.text, m.wrong, vs)
            if sc > 0:
                s[idx["mis:" + m.mis]] += sc
    if s.sum() == 0:
        return {}
    s = s / s.sum()
    pi = s.copy()
    for _ in range(MAX_ITER):
        nxt = RESTART * s + (1 - RESTART) * (pi @ p) + (1 - RESTART) * pi[deg == 0].sum() * s
        if np.abs(nxt - pi).sum() < TOL:
            pi = nxt
            break
        pi = nxt
    return {name[4:]: float(pi[i]) for name, i in idx.items() if name.startswith("mis:")}


# ------------------------------------------------- reading among siblings
def _distinct(meaning, text: str, others: list[str]) -> list[tuple[str, bool]]:
    """Phrases of ``text`` that no single phrase of the other texts covers."""
    covers = [meaning.words(q) for o in others for q, _ in meaning.phrases(o)]
    return [(p, n) for p, n in meaning.phrases(text) if not any(meaning.words(p) <= c for c in covers)]


def _closeness(meaning, clause: str, keys: list[tuple[str, bool]]) -> tuple[float, float]:
    """(same-polarity closeness, crossed-polarity closeness) of the clause's
    phrases to the keys."""
    ps = meaning.phrases(clause)
    if not ps or not keys:
        return 0.0, 0.0
    S = meaning.embed([p for p, _ in ps]) @ meaning.embed([k for k, _ in keys]).T
    same = cross = 0.0
    for i, (_, pn) in enumerate(ps):
        for j, (_, kn) in enumerate(keys):
            if pn == kn:
                same = max(same, float(S[i, j]))
            else:
                cross = max(cross, float(S[i, j]))
    return same, cross


def read_mis(kg: "KG", reader: "Reader", cands: "Candidates", st: "Statement") -> dict[str, float]:
    """Signed evidence per misconception edge id for one sentence, in units of
    the calibrated margin: > 0 for the one candidate the sentence means, < 0
    for candidates when the sentence means a correct rule."""
    meaning = reader.meaning()
    if meaning is None:
        return {}
    vs = reader.variables()
    out: dict[str, float] = {}
    cset = set(cands.concepts)
    by_concept: dict[str, list] = {}
    for m in cands.mis_edges:
        if m.concept in cset and m.concept in st.concepts and m.wrong and m.right:
            by_concept.setdefault(m.concept, []).append(m)
    if not by_concept:
        return out
    rank = mis_rank(kg, reader, st, [m for ms in by_concept.values() for m in ms])
    for c, sibs in by_concept.items():
        # retrieval: the sentence shares an anchor with the concept's edge logic
        if not any(reader.logic.score(st.text, x, vs) > 0 for m in sibs for x in (m.wrong, m.right)):
            continue
        ranks = [rank.get(m.mis, 0.0) for m in sibs]
        mean = sum(ranks) / len(ranks)
        cand = [m for m, r in zip(sibs, ranks) if r > 0 and r >= mean]
        if not cand:
            continue
        rights = sorted({m.right for m in sibs})
        wrongs = {m.id: m.wrong for m in cand}
        scores: dict[str, float] = {}
        cross_right = 0.0
        for m in cand:
            others = [w for k, w in wrongs.items() if k != m.id] + rights
            same, cross = _closeness(meaning, st.text, _distinct(meaning, m.wrong, others))
            scores[m.id] = same
            cross_right = max(cross_right, cross)    # "not <wrong belief>" supports a correct rule
        r_same = 0.0
        for r in rights:
            others = list(wrongs.values()) + [x for x in rights if x != r]
            same, cross = _closeness(meaning, st.text, _distinct(meaning, r, others))
            r_same = max(r_same, same)
        correct = max(r_same, cross_right)
        ordered = sorted(scores.items(), key=lambda kv: (-kv[1], kv[0]))
        top_id, top = ordered[0]
        second = max(ordered[1][1] if len(ordered) > 1 else 0.0, correct)
        if top - second >= meaning.margin:
            out[top_id] = (top - second) / meaning.margin
        elif correct - top >= meaning.margin:
            for mid, v in scores.items():
                out[mid] = -(correct - v) / meaning.margin
    return out


# ----------------------------------------------------------------- level
def form_level(st: "Statement") -> str:
    """The level the form of the reasoning shows."""
    if st.hypothetical or st.changes:
        return "L4"
    if st.link_words and len(set(st.concepts)) >= 2:
        return "L3"
    if any(lexicon.SLOT_KIND.get(s.name) in ("example", "outcome") for s in st.slots if not s.implied):
        return "L2"
    return "L1"


# ------------------------------------------------ level from the concept's ways
def _slot_match(st: "Statement", slots) -> bool:
    """A non-implied slot of the statement equals one of the way's / part's
    slots (name, value, negation)."""
    have = {(s.name, s.value, s.negated) for s in st.slots if not s.implied}
    return any((x[0], x[1], bool(x[2])) in have for x in slots or ())


def _gate(st: "Statement", row: dict) -> bool:
    """The way's own requirements (from the graph): its required neighbours
    are in the sentence, and the sentence carries the way's kind of evidence."""
    if any(r not in st.concepts for r in row.get("requires", [])):
        return False
    ev = row.get("evidence", "statement")
    if ev == "run":
        return any(lexicon.SLOT_KIND.get(s.name) in ("example", "outcome") for s in st.slots if not s.implied) \
            or any(ch.isdigit() for ch in st.text)
    if ev == "hypothetical":
        return bool(st.hypothetical or st.changes)
    if ev == "diagnosis":
        return bool(st.negated or any(s.negated for s in st.slots) or st.corrects)
    return True


def read_level(kg: "KG", reader: "Reader", c: str, st: "Statement") -> tuple[str, float, str] | None:
    """(level, prize, way) the sentence shows for concept c, read against all
    of the concept's ways; None when the sentence is not about c."""
    meaning = reader.meaning()
    vs = reader.variables()
    ways = []
    for lv in ("L1", "L2", "L3", "L4"):
        rows = kg.parts["ways"].get(c, {}).get(lv, [])
        for i, w in enumerate(kg.ways(c, lv)):
            row = rows[i] if i < len(rows) else {}
            if w.text:
                ways.append((lv, w.text, row))
    if not ways:
        return None
    topic = max(reader.logic.score(st.text, t, vs) for _, t, _ in ways) / reader.logic.match
    if meaning is not None:
        topic = max(topic, meaning.states(st.text, [t for _, t, _ in ways], vs) / meaning.sent_min)
    if topic < 1:
        return None
    open_ = [(lv, t, row) for lv, t, row in ways if _gate(st, row)]
    # an exact slot match with a way's own slots decides (highest such level)
    exact = [(lv, row) for lv, t, row in open_ if _slot_match(st, row.get("slots"))]
    if exact:
        lv, row = max(exact, key=lambda x: x[0])
        return lv, 2.0, row.get("way", "")
    if meaning is not None and len({lv for lv, _, _ in open_}) > 1:
        texts = [t for _, t, _ in ways]
        scored = []
        for lv, t, row in open_:
            same, _ = _closeness(meaning, st.text, _distinct(meaning, t, [x for x in texts if x != t]))
            scored.append((same, lv, row.get("way", "")))
        scored.sort(key=lambda x: (-x[0], x[1]))
        top = scored[0]
        other = max((s for s, lv, _ in scored if lv != top[1]), default=0.0)
        if top[0] - other >= meaning.margin:
            return top[1], 1.0 + (top[0] - other) / meaning.margin, top[2]
    # the concept is the topic but no way stands out: it is named (L1)
    return "L1", topic, "names_the_element"
