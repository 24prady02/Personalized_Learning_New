"""Level and misconception from the edge logic alone.

For each concept the answer touches, the candidate edges are the concept's
own edges in the graph:

* every has_level edge (each way of L1..L4, with its edge logic);
* every misconception edge (its wrong belief; held = L0).

The reader (conceptnli: the student's answer as premise, the edge logic as
hypothesis) gives P(entailment) for each edge. The edge whose logic the
answer most likely expresses decides: its level, or L0 with that
misconception. If no edge is entailed with P >= 0.5, the concept gets no
level from this answer. No other rule is used.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from . import conceptnli

if TYPE_CHECKING:  # pragma: no cover
    from .candidates import Candidates
    from .graph import KG
    from .statements import Statement

LEVELS = ("L1", "L2", "L3", "L4")
MIN_P = 0.5


def classify(kg: "KG", cands: "Candidates", a_st: list["Statement"], answer: str) -> dict[str, dict]:
    """concept -> {"level", "edge", "p", "misconception" | None, "text"}."""
    touched = set().union(*(set(s.concepts) for s in a_st if s.source in ("answer", "answer_code"))) \
        if a_st else set()
    premise = (answer or "")[:800]
    out: dict[str, dict] = {}
    for c in sorted(set(cands.concepts) & touched):
        edges = []
        for lv in LEVELS:
            for i, w in enumerate(kg.ways(c, lv)):
                if w.text:
                    edges.append({"level": lv, "edge": f"has_level:{c}->{lv}#{i}", "misconception": None,
                                  "text": w.text})
        for m in kg.mis_edges.get(c, []):
            if m.wrong:
                edges.append({"level": "L0", "edge": m.id, "misconception": m.mis, "text": m.wrong})
        if not edges:
            continue
        res = conceptnli.test(premise, [e["text"] for e in edges])
        best = max(range(len(edges)), key=lambda k: (res[k][0], -k))
        p = res[best][0]
        if p >= MIN_P:
            out[c] = {**edges[best], "p": round(p, 3)}
    return out
