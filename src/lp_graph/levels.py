"""Step 6 of the pipeline - level per concept, root cause, consistency.

Levels are computed for **every concept with a reading** (not only the
concepts the ES-Viterbi route lands on); the route adds its walked edges.
Only the student's last turn counts, and inside a turn a self-correction
("oh wait, ...") replaces what came before it.

Per concept, in this order:

1. **L0 (named)** if a misconception of the concept is MATCH-WRONG (citing
   the has_level L0 way whose ``linked_misconception`` matches, if any);
2. **L0 (WRONG_UNLISTED)** if a claim the concept produced is contradicted
   by the run, or a stated rule contradicts one of its ways - a missing
   misconception node never turns a wrong answer into a positive level;
3. else the highest level whose evidence the readings carry (the evidence
   class of reader.py):

   ====  ===============================================================
   L1    the concept is named, or a stated rule agrees with a way
   L2    a claim about this code that the run confirms, produced by it
   L3    a relation to a neighbour (a walked edge to a way's
         ``requires_concept``, or an edge MATCH), with L2 or better; or a
         correct diagnosis (an error named and confirmed by compile / run)
   L4    a what-if prediction that the changed program confirms
   ====  ===============================================================

4. ``none`` if nothing was read about it.

**Root cause**: reverse BFS up the prerequisite edges from each L0 concept
(no depth cap), stopping at the first ancestor layer the student shows (an
ancestor the answer names directly that is not itself L0). The concept just
below that ancestor is the gap. Gaps are ranked by (L0 concepts explained
desc, depth, id). A parallel / contrast neighbour whose rule gives exactly
the wrong value the student used (e.g. array elements default to 0) is
reported as the likely source.

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
from .reader import CONTRADICT, MATCH, MATCH_NLI, MATCH_WRONG, Reader, Segment
from .viterbi import Route

if TYPE_CHECKING:  # pragma: no cover
    from .graph import KG
    from .statements import Statement

LADDER = ("L1", "L2", "L3", "L4")



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


def effective(answer: list["Statement"]) -> list["Statement"]:
    """The statements that decide the level: the last turn, from its last
    self-correction on."""
    if not answer:
        return []
    last = max(s.turn for s in answer)
    turn = [s for s in answer if s.turn == last]
    starts = [k for k, s in enumerate(turn) if s.corrects]
    return turn[starts[0]:] if starts else turn


def compute_levels(kg: "KG", reader: Reader, route: Route, statements: dict[str, "Statement"],
                   broken_edges: set[str], readings: list[dict] | None = None,
                   candidates: list[str] | None = None, main: str | None = None) -> dict[str, LevelResult]:
    answer = [s for s in statements.values() if s.source in ("answer", "answer_code")]
    answer.sort(key=lambda s: s.order)
    eff = effective(answer)
    eff_ids = {s.id for s in eff}
    rows = [r for r in (readings or []) if r["statement"] in eff_ids]
    # a wrong claim a matched misconception explains is not blamed on other concepts too
    explained = {r["statement"] for r in rows if r["kind"] == "misconception" and r["label"] == MATCH_WRONG}
    where = landed(route)
    edge_steps = [st for st in route.steps if st.state.kind == "E"]
    concepts = set(c for c in where) | {r["concept"] for r in rows if r.get("concept")}
    # a concept reached through an edge the student states is read too
    concepts |= {c for r in rows if r["kind"] == "edge" and r["label"] == MATCH for c in r.get("endpoints", ())}
    if candidates is not None:
        concepts &= set(candidates) | set(where)
    results: dict[str, LevelResult] = {}
    for c in sorted(concepts):
        c_rows = [r for r in rows if r.get("concept") == c]
        sids = sorted({r["statement"] for r in c_rows} |
                      {sid for seg in where.get(c, []) for sid in seg if sid in eff_ids}, key=_sid_order)
        wrong = [r for r in c_rows if r["kind"] == "misconception" and r["label"] == MATCH_WRONG]
        if wrong:
            best = sorted(wrong, key=lambda r: (r.get("role") != "primary", -r.get("confidence", 1.0), r["id"]))[0]
            mis = best["element"].split(" ")[0]
            results[c] = LevelResult(c, "L0", sids, [], mis, _l0_way(kg, c, mis))
            continue
        # a contradicted claim the concept produced; a stated rule that
        # contradicts a way counts only for the concept the question is about
        bad = [r for r in c_rows if r["kind"] == "concept" and r["label"] == CONTRADICT
               and (r.get("class") == "run" or c == main) and (r["statement"] not in explained or c == main)]
        if bad and c == main and all(r["statement"] in explained for r in bad):
            # the main concept's wrong claim is the misconception matched in that statement
            mis_row = next(r for r in rows if r["kind"] == "misconception" and r["label"] == MATCH_WRONG
                           and r["statement"] in {b["statement"] for b in bad})
            mis = mis_row["element"].split(" ")[0]
            results[c] = LevelResult(c, "L0", sids, [], mis, _l0_way(kg, c, mis),
                                     note=f"its claim is wrong as {mis} predicts (on {mis_row['concept']})")
            continue
        if bad:
            results[c] = LevelResult(c, "L0", sids, [], None, None,
                                     note="WRONG_UNLISTED: " + "; ".join(r["evidence"] for r in bad[:2]))
            continue
        hits = []
        for r in c_rows:
            if r["kind"] != "concept" or r["label"] not in (MATCH, MATCH_NLI):
                continue
            hits.append({"level": lexicon.CLASS_LEVEL.get(r.get("class", "named"), "L1"),
                         "class": r.get("class", "named"), "statements": [r["statement"]],
                         "evidence": r["evidence"]})
        needs = {n for row in kg.parts["ways"].get(c, {}).get("L3", []) for n in row["requires"]}
        for r in rows:
            if r["kind"] == "edge" and r["label"] == MATCH and c in r.get("endpoints", ()):
                other = next((x for x in r["endpoints"] if x != c), None)
                # L3 only through the neighbour an L3 way of this concept requires;
                # any other stated edge shows the concept is reached (L1)
                # only an edge whose logic the student restates explains the relation
                stated = r.get("source") not in ("reasoning",) and str(r.get("evidence", "")).startswith(("states the edge logic", "NLI"))
                lv = "L3" if (other in needs and stated) else "L1"
                hits.append({"level": lv, "class": "relation" if lv == "L3" else "named",
                             "statements": [r["statement"]], "evidence": f"states edge {r['id']}"})
        for st in edge_steps:
            if c in (st.state.c_in, st.state.c_out) and any(sid in eff_ids for sid in st.statements):
                other = st.state.c_out if st.state.c_in == c else st.state.c_in
                needs = {n for row in kg.parts["ways"].get(c, {}).get("L3", []) for n in row["requires"]}
                if other in needs and st.reading.label == MATCH and str(st.reading.evidence).startswith("states the edge logic"):
                    hits.append({"level": "L3", "class": "relation", "statements": list(st.statements),
                                 "evidence": f"walked edge {st.state.edge} to {other}"})
        hits = _l3_gate(kg, c, hits, statements)
        level = _level_of(hits)
        results[c] = LevelResult(c, level, sids, sorted(_dedupe(hits), key=lambda h: h["level"]))
    _consistency(kg, results, broken_edges)
    _inconsistent_trace(kg, results, {st.state.edge for st in edge_steps}, broken_edges)
    return results


def _l3_gate(kg: "KG", c: str, hits: list[dict], statements: dict) -> list[dict]:
    """LP_GRAPH_L3GATE=1: each L3 hit is tested on its own. The premise is the
    student sentences the hit came from; the hypothesis is the logic of the
    relation edge the hit came from (or, for an L3 not read from an edge, this
    concept's own L3 way texts). The hit stays only if the reader (conceptnli)
    finds that logic entailed (p >= 0.5); the other hits stay."""
    import os
    import re

    if os.environ.get("LP_GRAPH_L3GATE", "0") != "1" or not any(h["level"] == "L3" for h in hits):
        return hits
    from . import conceptnli

    ways = [w.text for w in kg.ways(c, "L3") if w.text]
    kept = []
    for h in hits:
        if h["level"] != "L3":
            kept.append(h)
            continue
        sts = sorted((statements[i] for i in h.get("statements", []) if i in statements), key=lambda s: s.order)
        premise = " ".join(s.text for s in sts if s.source in ("answer", "answer_code"))
        m = re.search(r"edge (\S+)", h.get("evidence", ""))
        e = kg.relation_edges.get(m.group(1)) if m else None
        texts = [e.logic] if e is not None and e.logic else ([] if e is not None else ways)
        if premise.strip() and texts and max(p for p, _ in conceptnli.test(premise[:800], texts)) >= 0.5:
            kept.append(h)
    return kept


def _level_of(hits: list[dict]) -> str:
    have = {h["level"] for h in hits}
    if not have:
        return "none"
    if "L4" in have:
        return "L4"
    if "L3" in have and ("L2" in have or any(h["class"] == "diagnosis" for h in hits)):
        return "L3"
    if "L2" in have:
        return "L2"
    return "L1"


def misconception_report(readings: list[dict], statements: dict[str, "Statement"],
                         kg: "KG") -> list[dict]:
    """Every misconception read (MATCH-WRONG), with status: held, or
    corrected when only earlier turns / text before a correction show it."""
    answer = sorted((s for s in statements.values() if s.source in ("answer", "answer_code")),
                    key=lambda s: s.order)
    eff_ids = {s.id for s in effective(answer)}
    out: dict[tuple[str, str], dict] = {}
    for r in readings:
        if r["kind"] != "misconception" or r["label"] != MATCH_WRONG:
            continue
        mis = r["element"].split(" ")[0]
        key = (r["concept"], mis)
        d = out.setdefault(key, {"id": mis, "concept": r["concept"], "statements": [], "evidence": r["evidence"],
                                 "role": r.get("role", ""), "confidence": r.get("confidence", 1.0)})
        d["statements"] = sorted(set(d["statements"]) | {r["statement"]}, key=_sid_order)
    rows = []
    for (c, mis), d in sorted(out.items()):
        edge = next((m for m in kg.mis_edges.get(c, []) if m.mis == mis), None)
        d["wrong"] = edge.wrong if edge else ""
        d["right"] = edge.right if edge else ""
        d["status"] = "held" if set(d["statements"]) & eff_ids else "corrected"
        rows.append(d)
    return rows


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


def _dedupe(hits: list[dict]) -> list[dict]:
    seen, out = set(), []
    for h in hits:
        k = (h["level"], h["evidence"])
        if k not in seen:
            seen.add(k)
            out.append(h)
    return out


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
    """``answer_concepts`` must be the concepts the answer names directly."""
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


__all__ = ["LevelResult", "RootCause", "compute_levels", "root_causes", "level_index",
           "misconception_report", "effective"]
