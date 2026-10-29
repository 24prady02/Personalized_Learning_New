"""Step 4 of the pipeline - ES-Viterbi (Element-State Semi-Markov Viterbi).

Lines the statements up, in order, with graph elements and returns the best
route (the concept map).

States
    ``N(c)`` stay on concept c; ``E(e)`` walk relation edge e (parallel
    edges both ways, prerequisite edges also backwards with
    ``reversed=True``); ``M(c, mis)`` a misconception of c; ``NOISE``.

Emission
    A segment of 1-3 consecutive statements may enter a state only if the
    reader says MATCH (concept way / edge) or MATCH-WRONG (misconception).
    NOISE takes one statement and is always allowed.

Move costs (integers, no weights)
    stay on the same concept / misconception 0; concept -> edge -> next
    concept along a matched edge 0; jump between concepts not linked by a
    matched edge = hop distance, capped at 3, and 1 between concepts the
    same code statement uses (the code links them); NOISE 1; +1 for a state
    on a generic concept (declaration, variable, int ...) the segment does
    not name. An edge a segment contradicts is blocked for it (the pipeline
    reports it as a broken link).

Start
    an anchor concept (code / question seed) costs 0; any other candidate
    costs its hop distance to the nearest anchor.

Ties are broken by (cost, evidence weakness, jumps, -edges walked, steps,
state ids): run-confirmed or rule evidence beats an edge match, which beats
merely naming a concept. The result is deterministic.

The *correct* route is not decoded from the code lines: ``graph_route``
builds it from the graph (the expected concepts joined by their shortest
stateable paths), so the comparison is like with like. The best and second-best
routes are returned. If the best route costs more than 1 per statement
(a list-like answer), a best connected subgraph over the matched elements
is computed as well.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Sequence

from . import lexicon
from .reader import ENTERS, Reader, Reading, Segment

if TYPE_CHECKING:  # pragma: no cover
    from .candidates import Candidates
    from .graph import KG
    from .statements import Statement

MAX_SEGMENT = 3
NOISE_COST = 1
K_BEST = 2
JUMP_CAP = 3
GENERIC_COST = 1
WORDING_COST = 1   # a reading from wording alone (TF-IDF) costs more than code evidence
TEXT_ONLY = "text-only"
MATCH_GRAPH = "GRAPH"


@dataclass(frozen=True)
class State:
    id: str
    kind: str                  # N | E | M | NOISE
    c_in: str | None
    c_out: str | None
    edge: str | None = None
    mis: str | None = None
    reversed: bool = False
    weak: int = 0              # tie-break only: 0 strongest evidence

    def label(self) -> str:
        if self.kind == "N":
            return f"N({self.c_in})"
        if self.kind == "E":
            if self.reversed:
                return f"E({self.c_in} -> {self.c_out}, against the prerequisite)"
            return f"E({self.c_in} -> {self.c_out})"
        if self.kind == "M":
            return f"M({self.c_in}, {self.mis})"
        return "NOISE"


@dataclass(frozen=True)
class Step:
    state: State
    statements: tuple[str, ...]
    move: str          # start | stay | edge | jump | noise
    move_cost: int
    reading: Reading
    jumped_from: str | None = None

    def to_dict(self) -> dict:
        d = {"state": self.state.label(), "kind": self.state.kind,
             "statements": list(self.statements), "move": self.move,
             "move_cost": self.move_cost, "reading": self.reading.to_dict()}
        if self.state.edge:
            d["edge"] = self.state.edge
            d["reversed"] = self.state.reversed
        if self.state.mis:
            d["misconception"] = self.state.mis
        if self.jumped_from:
            d["jumped_from"] = self.jumped_from
        return d


@dataclass
class Route:
    steps: list[Step] = field(default_factory=list)
    cost: int = 0
    jumps: int = 0
    n_statements: int = 0

    def concept_path(self) -> list[str]:
        path: list[str] = []
        for st in self.steps:
            for c in (st.state.c_in, st.state.c_out):
                if c and (not path or path[-1] != c):
                    path.append(c)
        return path

    def edges(self) -> list[str]:
        return [s.state.edge for s in self.steps if s.state.kind == "E" and s.state.edge]

    def concepts(self) -> list[str]:
        return sorted({c for s in self.steps for c in (s.state.c_in, s.state.c_out) if c})

    def misconceptions(self) -> list[Step]:
        return [s for s in self.steps if s.state.kind == "M"]

    def mean_cost(self) -> float:
        return self.cost / self.n_statements if self.n_statements else 0.0

    def to_dict(self) -> dict:
        return {"cost": self.cost, "jumps": self.jumps,
                "concept_path": self.concept_path(), "edges": self.edges(),
                "steps": [s.to_dict() for s in self.steps]}


@dataclass(frozen=True)
class _Entry:
    cost: int
    jumps: int
    weak: int
    edges: int
    path: tuple[Step, ...]
    last: str | None

    def key(self) -> tuple:
        return (self.cost, self.weak, self.jumps, -self.edges, len(self.path),
                tuple(s.state.id for s in self.path))


def build_states(kg: "KG", cands: "Candidates") -> list[State]:
    states: list[State] = []
    for c in sorted(cands.concepts):
        states.append(State(f"N:{c}", "N", c, c))
    for e in cands.relation_edges:
        states.append(State(f"E:{e.id}:fwd", "E", e.src, e.dst, e.id))
        states.append(State(f"E:{e.id}:back", "E", e.dst, e.src, e.id,
                            reversed=e.kind == "prerequisite"))
    for m in cands.mis_edges:
        weak = (0 if m.concept == cands.main_concept else 1) + (0 if m.role == "primary" else 1)
        states.append(State(f"M:{m.concept}:{m.mis}", "M", m.concept, m.concept,
                            mis=m.mis, weak=weak))
    states.append(State("NOISE", "NOISE", None, None, weak=0))
    return sorted(states, key=lambda s: s.id)


class ESViterbi:
    """ES-Viterbi over one statement sequence."""

    def __init__(self, kg: "KG", cands: "Candidates", reader: Reader,
                 anchors: Sequence[str], fault: dict[str, tuple[str, ...]] | None = None,
                 co_use: set[frozenset[str]] | None = None,
                 blocked: set[tuple[str, str]] | None = None) -> None:
        self.kg = kg
        self.cands = cands
        self.reader = reader
        self.anchors = sorted(set(anchors))
        self.states = build_states(kg, cands)
        self.mis_by_state = {f"M:{m.concept}:{m.mis}": m for m in cands.mis_edges}
        self.edge_by_id = {e.id: e for e in cands.relation_edges}
        self.fault = fault or {}
        self.co_use = co_use or set()
        self.blocked = blocked or set()   # (edge id, statement id) the statement breaks

    # ---------------------------------------------------------- emission
    def emission(self, seg: Segment, s: State) -> Reading | None:
        if s.kind == "NOISE":
            return Reading("NOISE") if len(seg.statements) == 1 else None
        if s.kind == "N":
            fault = tuple(sorted({c for sid in seg.ids for c in self.fault.get(sid, ())}))
            r = self.reader.read_concept(seg, s.c_in, fault)
        elif s.kind == "E":
            if any((s.edge, sid) in self.blocked for sid in seg.ids):
                return None
            r = self.reader.read_edge(seg, self.edge_by_id[s.edge])
        else:
            m = self.mis_by_state[s.id]
            r = self.reader.read_mis(seg, m)
            if r.label not in ENTERS:
                r = self._wording_mis(seg, m)
        if s.kind == "N" and r.label not in ENTERS:
            r = self._wording_way(seg, s.c_in)
        return r if r.label in ENTERS else None

    def _wording_mis(self, seg: Segment, m) -> Reading:
        """The segment expresses the wrong side of the misconception edge's logic
        (TF-IDF anchors), where the code cannot decide. Weaker than code evidence."""
        if seg.source != "answer" or not (m.wrong and m.right) or m.concept not in seg.concepts \
                or any(st.hypothetical for st in seg.statements) or self.reader._code_decides(seg, m.mis):
            return Reading("NO")
        import os

        meaning = self.reader.meaning()
        if meaning is not None:
            side, score = meaning.side(seg.text, m.wrong, m.right, self.reader.variables())
        elif os.environ.get("LP_GRAPH_NATLOGIC", "0") == "1":
            from . import natlogic

            nl = natlogic.side(self.reader.logic, seg.text, m.wrong, m.right, self.reader.variables())
            side, score = ("a" if nl == "wrong" else "b" if nl == "right" else None),                 self.reader.logic.score(seg.text, m.wrong, self.reader.variables())
        else:
            side, score = self.reader.logic.side(seg.text, m.wrong, m.right, self.reader.variables())
        if side == "a":
            return Reading("MATCH-WRONG", evidence=f"wording expresses the wrong belief ({score:.2f}): {m.wrong}",
                           confidence=round(score, 3), cls=TEXT_ONLY)
        return Reading("NO")

    def _wording_way(self, seg: Segment, concept: str) -> Reading:
        """The segment states the edge logic of one of the concept's L1 ways
        (TF-IDF anchors). Weaker than code evidence."""
        if seg.source != "answer" or concept not in seg.concepts:
            return Reading("NO")
        meaning = self.reader.meaning()
        if meaning is not None:
            # every level's ways, by meaning; the closest way gives the level
            scored = []
            for lv in ("L1", "L2", "L3", "L4"):
                texts = [w.text for w in self.kg.ways(concept, lv) if w.text]
                if texts:
                    scored.append((meaning.states(seg.text, texts, self.reader.variables()), lv))
            if scored:
                sim, lv = max(scored)
                if sim >= meaning.sent_min:
                    return Reading("MATCH", evidence=f"wording states an {lv} way (meaning {sim:.2f})",
                                   confidence=round(sim, 3), cls=TEXT_ONLY)
            return Reading("NO")
        best = 0.0
        for w in self.kg.ways(concept, "L1"):
            if w.text:
                best = max(best, self.reader.logic.score(seg.text, w.text, self.reader.variables()))
        if best >= self.reader.logic.match:
            return Reading("MATCH", evidence=f"wording states an L1 way ({best:.2f})",
                           confidence=round(best, 3), cls=TEXT_ONLY)
        return Reading("NO")

    def _weak(self, s: State, r: Reading) -> int:
        """Tie-break: run / rule evidence before an edge match before naming,
        and the main concept first."""
        if s.kind == "N":
            rank = {"hypothetical": 0, "diagnosis": 0, "run": 0, "rule": 1, "relation": 1}.get(r.cls, 3)
            return rank + (0 if s.c_in == self.cands.main_concept else 1)
        if s.kind == "E":
            # an edge whose logic the segment states is the strongest reading of
            # that segment: the route walks it (with ties, more edges walked win)
            return 0 if r.evidence.startswith("states the edge logic") else 2
        return s.weak

    # -------------------------------------------------------- transition
    def _start_cost(self, c: str) -> int:
        if not self.anchors or c in self.anchors:
            return 0
        return min(self.kg.hop_distance(a, c) for a in self.anchors)

    def _move(self, last: str | None, s: State, first: bool) -> tuple[str, int, int]:
        """(move, cost, jumps added) from concept ``last`` into state ``s``."""
        if s.kind == "NOISE":
            return "noise", NOISE_COST, 0
        if first or last is None:
            return "start", min(self._start_cost(s.c_in), JUMP_CAP), 0
        if last == s.c_in:
            return ("edge" if s.kind == "E" else "stay"), 0, 0
        if frozenset((last, s.c_in)) in self.co_use:
            return "jump", 1, 1
        return "jump", min(self.kg.hop_distance(last, s.c_in), JUMP_CAP), 1

    # --------------------------------------------------------------- run
    def run(self, statements: Sequence["Statement"]) -> tuple[Route, Route | None]:
        stm = list(statements)
        T = len(stm)
        if T == 0:
            return Route(), None
        cells: dict[int, dict[tuple, list[_Entry]]] = {0: {("START", None): [_Entry(0, 0, 0, 0, (), None)]}}
        for t_end in range(1, T + 1):
            cell: dict[tuple, list[_Entry]] = {}
            for L in range(1, MAX_SEGMENT + 1):
                t0 = t_end - L
                if t0 < 0:
                    break
                seg = Segment(tuple(stm[t0:t_end]))
                prev = cells.get(t0, {})
                if not prev:
                    continue
                for s in self.states:
                    r = self.emission(seg, s)
                    if r is None:
                        continue
                    weak = self._weak(s, r)
                    extra = GENERIC_COST if (s.kind == "N" and s.c_in in lexicon.GENERIC
                                             and s.c_in not in seg.direct) else 0
                    if r.cls == TEXT_ONLY:
                        extra += WORDING_COST
                    for pkey in sorted(prev, key=lambda k: (k[0], k[1] or "")):
                        for ent in prev[pkey]:
                            move, mc, dj = self._move(ent.last, s, t0 == 0 or ent.last is None)
                            mc += extra
                            step = Step(s, seg.ids, move, mc, r,
                                        ent.last if move == "jump" else None)
                            last = ent.last if s.kind == "NOISE" else s.c_out
                            new = _Entry(ent.cost + mc, ent.jumps + dj, ent.weak + weak,
                                         ent.edges + (s.kind == "E"), ent.path + (step,), last)
                            _push(cell, (s.id, last), new)
            cells[t_end] = cell
        finals = sorted((e for lst in cells[T].values() for e in lst), key=lambda e: e.key())
        routes = [self._route(e, T) for e in finals[:K_BEST]]
        return routes[0], (routes[1] if len(routes) > 1 else None)

    @staticmethod
    def _route(e: _Entry, T: int) -> Route:
        return Route(list(e.path), e.cost, e.jumps, T)


def _push(cell: dict[tuple, list[_Entry]], key: tuple, entry: _Entry) -> None:
    lst = cell.setdefault(key, [])
    lst.append(entry)
    lst.sort(key=lambda e: e.key())
    del lst[K_BEST:]


# -------------------------------------------------------------- fallback

def connected_subgraph(kg: "KG", concepts: Sequence[str]) -> dict:
    """Union of shortest paths joining the matched concepts (list-like answers).

    Exact enough at this size: BFS shortest paths (neighbours sorted, so the
    same path every time) from the first matched concept to every other.
    """
    cs = sorted(set(concepts))
    if not cs:
        return {"concepts": [], "edges": []}
    root = cs[0]
    nodes, edges = {root}, set()
    for target in cs[1:]:
        path = _shortest_path(kg, root, target)
        if not path:
            nodes.add(target)
            continue
        nodes.update(path)
        for a, b in zip(path, path[1:]):
            edges.add(_edge_between(kg, a, b))
    return {"concepts": sorted(nodes), "edges": sorted(e for e in edges if e)}


def _shortest_path(kg: "KG", a: str, b: str) -> list[str]:
    prev = {a: None}
    q = deque([a])
    while q:
        u = q.popleft()
        if u == b:
            break
        for v in kg.adjacency[u]:
            if v not in prev:
                prev[v] = u
                q.append(v)
    if b not in prev:
        return []
    path = [b]
    while prev[path[-1]] is not None:
        path.append(prev[path[-1]])
    return path[::-1]


def _edge_between(kg: "KG", a: str, b: str) -> str | None:
    for eid in kg.rel_by_concept.get(a, []):
        e = kg.relation_edges[eid]
        if e.other(a) == b:
            return eid
    return None


# ------------------------------------------------------- the correct route

def graph_route(kg: "KG", expected: Sequence[str], order: Sequence[str] = ()) -> Route:
    """The correct route built from the graph: the expected concepts (in code
    order, then by id) joined by their shortest stateable paths (at most
    JUMP_CAP edges), plus every contrast edge between two expected concepts.
    A concept with no such path stands alone."""
    cs = [c for c in dict.fromkeys(list(order) + sorted(expected)) if c in kg.hop]
    steps: list[Step] = []
    seen_edges: set[str] = set()
    placed: list[str] = []
    for c in cs:
        best = None
        for p in placed:
            path = _shortest_path(kg, p, c)
            if not path or len(path) - 1 > JUMP_CAP:
                continue
            eids = [_edge_between(kg, a, b) for a, b in zip(path, path[1:])]
            if all(e and kg.relation_edges[e].stateable for e in eids):
                if best is None or len(path) < len(best):
                    best = path
        if best:
            for a, b in zip(best, best[1:]):
                eid = _edge_between(kg, a, b)
                if eid in seen_edges:
                    continue
                seen_edges.add(eid)
                e = kg.relation_edges[eid]
                rev = e.kind == "prerequisite" and e.src != a
                sid = f"E:{eid}:" + ("back" if rev else "fwd")
                steps.append(Step(State(sid, "E", a, b, eid, reversed=rev), ("graph",), "edge", 0,
                                  Reading(MATCH_GRAPH)))
        else:
            steps.append(Step(State(f"N:{c}", "N", c, c), ("graph",), "start", 0, Reading(MATCH_GRAPH)))
        placed.append(c)
    exp = set(cs)
    for eid in sorted(kg.relation_edges):
        e = kg.relation_edges[eid]
        if e.kind == "parallel" and e.src in exp and e.dst in exp and eid not in seen_edges:
            seen_edges.add(eid)
            steps.append(Step(State(f"E:{eid}:fwd", "E", e.src, e.dst, eid), ("graph",), "edge", 0,
                              Reading(MATCH_GRAPH)))
    return Route(steps, 0, 0, len(steps))
