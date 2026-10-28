"""Step 6 of the pipeline - level per concept, root cause, consistency.

Level per concept the student route lands on:

1. **L0** if a misconception state of that concept is on the route (citing
   the has_level L0 way whose ``linked_misconception`` matches, if any).
2. Else climb **L1 -> L4**: a level is met if >=1 of its ways is MATCHed by
   the statements on that concept. L3 also accepts a matched relation edge
   to a neighbour named in a way's ``requires_concept``; L4 needs a
   predict-a-change / transfer / diagnose way matched in a hypothetical
   statement ("if ... would ..."). Stop at the first level not met.
3. ``none`` if no statement landed on the concept.

**Root cause**: reverse BFS up the prerequisite edges from each L0 concept
(no depth cap), stopping at the first ancestor layer the student shows (an
ancestor named in the answer that is not itself L0). The concept just below
that ancestor is the gap. Gaps are ranked by (L0 concepts explained desc,
depth, id). A parallel / contrast neighbour whose rule gives exactly the
wrong value the student used (e.g. array elements default to 0) is reported
as the likely source.

**Consistency**: a topological sweep caps a concept at L1 (and flags it) if
it is >=L2 while a prerequisite edge into it is broken. Likewise an edge the
student states and later contradicts (an inconsistent trace) caps both
endpoints at L1.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from . import lexicon
from .knowledge import LEVELS
from .reader import MATCH, MATCH_NLI, Reader, Segment
from .viterbi import Route

if TYPE_CHECKING:  # pragma: no cover
    from .graph import KG
    from .statements import Statement

LADDER = ("L1", "L2", "L3", "L4")
L4_WAYS = frozenset({"predict_a_change", "transfer_to_a_new_program", "diagnose_an_error"})


@dataclass
class LevelResult:
    concept: str
    level: str                      # L0..L4 | none
    statements: list[str] = field(default_factory=list)
    ways: list[dict] = field(default_factory=list)
    misconception: str | None = None
    l0_way: dict | None = None
    capped: bool = False
    note: str = ""

    def to_dict(self) -> dict:
        d = {"level": self.level, "statements": self.statements, "ways": self.ways}
        if self.misconception:
            d["misconception"] = self.misconception
        if self.l0_way:
            d["l0_way"] = self.l0_way
        if self.capped:
            d["capped"] = True
        if self.note:
            d["note"] = self.note
        return d


def landed(route: Route) -> dict[str, list[tuple[str, ...]]]:
    """concept -> statement-id tuples of the route steps touching it."""
    out: dict[str, list[tuple[str, ...]]] = {}
    for st in route.steps:
        for c in sorted({x for x in (st.state.c_in, st.state.c_out) if x}):
            out.setdefault(c, []).append(st.statements)
    return out


def compute_levels(kg: "KG", reader: Reader, route: Route,
                   statements: dict[str, "Statement"], broken_edges: set[str]) -> dict[str, LevelResult]:
    where = landed(route)
    results: dict[str, LevelResult] = {}
    mis_steps = {st.state.c_in: st for st in route.steps if st.state.kind == "M"}
    edge_steps = [st for st in route.steps if st.state.kind == "E"]
    for c in sorted(where):
        sids = sorted({sid for seg in where[c] for sid in seg}, key=_sid_order)
        if c in mis_steps:
            st = mis_steps[c]
            results[c] = LevelResult(c, "L0", sids, [], st.state.mis, _l0_way(kg, c, st.state.mis))
            continue
        # each step's segment, and each of its statements on its own
        segs = [Segment(tuple(statements[i] for i in seg)) for seg in where[c]]
        segs += [Segment((statements[i],)) for seg in where[c] if len(seg) > 1 for i in seg]
        met, ways = "none", []
        for lv in LADDER:
            hits = _level_hits(kg, reader, c, lv, segs, edge_steps)
            if not hits:
                break
            met = lv
            ways.extend(hits)
        results[c] = LevelResult(c, met, sids, ways)
    _consistency(kg, results, broken_edges)
    _inconsistent_trace(kg, results, {st.state.edge for st in edge_steps}, broken_edges)
    return results


def _inconsistent_trace(kg: "KG", results: dict[str, LevelResult], walked: set[str | None],
                        broken_edges: set[str]) -> None:
    """An edge the student both states and later contradicts is an
    inconsistent trace: its endpoints are capped at L1."""
    for eid in sorted(e for e in walked if e and e in broken_edges):
        e = kg.relation_edges[eid]
        for c in (e.src, e.dst):
            r = results.get(c)
            if r and r.level in ("L2", "L3", "L4"):
                r.level, r.capped = "L1", True
                r.ways = [w for w in r.ways if w["level"] == "L1"]
                r.note = f"capped at L1: edge {eid} both stated and contradicted"


def _sid_order(sid: str) -> tuple:
    return (sid[0], int(sid[1:]) if sid[1:].isdigit() else 0)


def _l0_way(kg: "KG", concept: str, mis: str | None) -> dict | None:
    for w in kg.ways(concept, "L0"):
        if mis and mis in w.misconceptions:
            return {"level": "L0", "index": w.index, "way": w.way}
    return None


def _level_hits(kg: "KG", reader: Reader, c: str, lv: str, segs: list[Segment],
                edge_steps: list) -> list[dict]:
    hits: list[dict] = []
    for row in kg.parts["ways"].get(c, {}).get(lv, []):
        for seg in segs:
            r = reader.read_way(seg, c, lv, row)
            if r.label not in (MATCH, MATCH_NLI):
                continue
            if lv == "L3" and row["way"] == "relation_to_neighbour":
                continue  # decided by the matched edge below
            if lv == "L4" and (row["way"] not in L4_WAYS or not _hypothetical(seg)):
                continue
            if lv in ("L3", "L4") and r.confidence < 1.0:
                continue  # merely naming the concept never climbs this high
            hits.append({"level": lv, "index": row["index"], "way": row["way"],
                         "statements": list(seg.ids), "evidence": r.evidence})
            break
    if lv == "L3":
        for row in kg.parts["ways"].get(c, {}).get("L3", []):
            needs = set(row["requires"])
            for st in edge_steps:
                other = st.state.c_out if st.state.c_in == c else (
                    st.state.c_in if st.state.c_out == c else None)
                if other and other in needs:
                    hits.append({"level": "L3", "index": row["index"], "way": row["way"],
                                 "statements": list(st.statements),
                                 "evidence": f"matched edge {st.state.edge}"})
                    break
    return _dedupe(hits)


def _dedupe(hits: list[dict]) -> list[dict]:
    seen, out = set(), []
    for h in hits:
        k = (h["level"], h["index"])
        if k not in seen:
            seen.add(k)
            out.append(h)
    return out


def _hypothetical(seg: Segment) -> bool:
    words = " ".join(s.text.lower() for s in seg.statements).split()
    return any(w.strip(",.") in lexicon.HYPOTHETICAL for w in words)


def _consistency(kg: "KG", results: dict[str, LevelResult], broken_edges: set[str]) -> None:
    for c in kg.topo:
        r = results.get(c)
        if not r or r.level in ("none", "L0", "L1"):
            continue
        for p in kg.inn.get("prerequisite", {}).get(c, []):
            e = kg.prerequisite_edge(p, c)
            if e and e.id in broken_edges:
                r.level, r.capped = "L1", True
                r.ways = [w for w in r.ways if w["level"] == "L1"]
                r.note = f"capped at L1: prerequisite edge {e.id} is broken"
                break


# ------------------------------------------------------------ root cause

@dataclass
class RootCause:
    concept: str                  # the gap
    via: str | None               # the first ancestor the student shows
    link: str | None              # edge via -> concept
    explains: list[str]
    depth: int
    contrast: list[dict] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {"concept": self.concept, "via": self.via, "link": self.link,
                "explains": self.explains, "depth": self.depth, "contrast": self.contrast}


def root_causes(kg: "KG", levels: dict[str, LevelResult], route: Route,
                answer_concepts: set[str]) -> list[RootCause]:
    l0 = sorted(c for c, r in levels.items() if r.level == "L0")
    shown = {c for c in answer_concepts if levels.get(c, LevelResult(c, "none")).level != "L0"}
    gaps: dict[tuple[str, str | None], set[str]] = {}
    for c in l0:
        for gap, via in _first_shown_ancestors(kg, c, shown):
            gaps.setdefault((gap, via), set()).add(c)
    out = []
    for (gap, via), explained in gaps.items():
        link = kg.prerequisite_edge(via, gap).id if via and kg.prerequisite_edge(via, gap) else None
        out.append(RootCause(gap, via, link, sorted(explained), kg.depth.get(gap, 0)))
    out.sort(key=lambda r: (-len(r.explains), r.depth, r.concept, r.via or ""))
    for rc in out:
        for c in rc.explains:
            rc.contrast.extend(contrast_sources(kg, c, levels[c].misconception, route))
    return out


def _first_shown_ancestors(kg: "KG", start: str, shown: set[str]) -> list[tuple[str, str | None]]:
    """Reverse BFS by layers; the first layer with a shown ancestor stops it."""
    layer, visited = [start], {start}
    while layer:
        found, nxt = [], []
        for node in sorted(layer):
            for p in kg.inn.get("prerequisite", {}).get(node, []):
                if p in shown:
                    found.append((node, p))
                elif p not in visited:
                    visited.add(p)
                    nxt.append(p)
        if found:
            return sorted(set(found))
        layer = sorted(set(nxt))
    return [(start, None)]


def contrast_sources(kg: "KG", concept: str, mis: str | None, route: Route) -> list[dict]:
    """Neighbours whose own rule gives the wrong value the student used."""
    if not mis:
        return []
    spec = None
    for m in kg.mis_edges.get(concept, []):
        if m.mis == mis:
            spec = kg.parts["misconceptions"].get(m.id, {}).get("slot")
    if not spec:
        return []
    out = []
    for eid in kg.rel_by_concept.get(concept, []):
        e = kg.relation_edges[eid]
        other = e.other(concept)
        for p in kg.parts["edges"].get(eid, {}).get("parts", []):
            if p["concept"] != other:
                continue
            if any(n == spec["slot"] and v == spec["wrong_value"] for n, v, *_ in p["slots"]):
                out.append({"neighbour": other, "edge": eid, "kind": e.kind, "text": p["text"]})
                break
    return out


def level_index(level: str) -> int:
    return LEVELS.index(level) if level in LEVELS else -1


__all__ = ["LevelResult", "RootCause", "compute_levels", "root_causes", "level_index"]
