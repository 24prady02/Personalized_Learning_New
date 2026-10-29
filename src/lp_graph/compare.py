"""Step 5 of the pipeline - compare the correct route with the student route.

* **covered**   concepts / edges on both routes;
* **lacking**   on the correct route (built from the graph), missing from
  the student route; concepts only among the expected ones, edges whose
  grounding is ``questionable`` or ``order_only`` never (not stateable);
* **excessive** on the student route only;
* **broken**    edges a student statement contradicts (blocked in
  ES-Viterbi);
* **skipped**   connector concepts the student jumped over (inner nodes of
  the shortest path between the two ends of a jump);
* **corrected** misconceptions held in an earlier turn and corrected later.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from .viterbi import Route, _shortest_path

if TYPE_CHECKING:  # pragma: no cover
    from .graph import KG


@dataclass
class Comparison:
    covered_concepts: list[str] = field(default_factory=list)
    covered_edges: list[str] = field(default_factory=list)
    lacking_concepts: list[str] = field(default_factory=list)
    lacking_edges: list[str] = field(default_factory=list)
    excessive_concepts: list[str] = field(default_factory=list)
    excessive_edges: list[str] = field(default_factory=list)
    broken: list[dict] = field(default_factory=list)
    skipped: list[dict] = field(default_factory=list)
    corrected: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "covered": {"concepts": self.covered_concepts, "edges": self.covered_edges},
            "lacking": {"concepts": self.lacking_concepts, "edges": self.lacking_edges},
            "excessive": {"concepts": self.excessive_concepts, "edges": self.excessive_edges},
            "broken": self.broken,
            "skipped": self.skipped,
            "corrected": self.corrected,
        }


def compare_routes(kg: "KG", correct: Route, student: Route, broken: list[dict],
                   expected: set[str] | None = None, corrected: list[str] | None = None) -> Comparison:
    c_concepts, s_concepts = set(correct.concepts()), set(student.concepts())
    exp = c_concepts if expected is None else (set(expected) & c_concepts) | set(expected)
    c_edges, s_edges = set(correct.edges()), set(student.edges())
    lacking_edges = sorted(e for e in c_edges - s_edges
                           if e in kg.relation_edges and kg.relation_edges[e].stateable)
    skipped = []
    for st in student.steps:
        if st.move == "jump" and st.jumped_from and st.state.c_in:
            path = _shortest_path(kg, st.jumped_from, st.state.c_in)
            skipped.append({"from": st.jumped_from, "to": st.state.c_in,
                            "statements": list(st.statements),
                            "hop_distance": st.move_cost, "skipped": path[1:-1]})
    return Comparison(
        covered_concepts=sorted(c_concepts & s_concepts),
        covered_edges=sorted(c_edges & s_edges),
        lacking_concepts=sorted(exp - s_concepts),
        lacking_edges=lacking_edges,
        excessive_concepts=sorted(s_concepts - c_concepts),
        excessive_edges=sorted(s_edges - c_edges),
        broken=sorted(broken, key=lambda b: (b["edge"], b["statement"])),
        skipped=skipped,
        corrected=sorted(corrected or []),
    )
