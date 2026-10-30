"""The model: a rule-based matcher plus a subgraph extractor over the knowledge graph.

Part 1, tagging (``tag_concept``, ``tag_code``): run the regex channels stored on every concept node of the KG
(``code_patterns``, ``signals``, ``operator_symbols``, ``java_types``, ``command_patterns``) over the preprocessed
code. Only the code is read; ``aliases`` (for the student's words) are never used.

Part 2, extraction (``extract_subgraph``, ``subgraph_from_code``): the concept nodes are the tagged concepts
(minus bare generic ones), then the KG's prerequisite / parallel edges between them, their misconception / error
nodes and edges, their level nodes L0..L4 with the has_level edges, and the level <-> misconception links.

There are no learned parameters: the "model" is the pattern bank stored in the KG.
"""
from __future__ import annotations

import re
from collections import defaultdict
from typing import Any

from preprocessing import Prepared
from utils import Hit, line_of, reader_blocks, rx


# ------------------------------------------------------------------ part 1: tagging

def _hit(channel: str, name: str, decisive: bool, m: re.Match[str], code: str, base: int = 0) -> Hit:
    return {
        "channel": channel,
        "name": name,
        "decisive": bool(decisive),
        "match": m.group(0),
        "line": line_of(code, base + m.start()),
    }


def tag_concept(code: str, rd: dict[str, Any], prepared: "Prepared | None" = None) -> list[Hit]:
    """Run every regex channel of one reader block against the code."""
    if rd.get("code_visible") is False:
        return []
    prep = prepared or Prepared(code)
    t = code if rd.get("code_text") == "raw" else prep.masked
    hits: list[Hit] = []

    for p in rd.get("code_patterns") or []:
        m = rx(p, re.M).search(t)
        if m:
            hits.append(_hit("pattern", p, False, m, code))

    for s in rd.get("signals") or []:
        if "regex" not in s:
            continue
        sources = s.get("sources")
        if sources and "code" not in sources:
            continue
        raw = s.get("text") == "raw"
        tt = code if raw else t
        name = s.get("name", "")
        decisive = bool(s.get("decisive"))
        if s.get("scope") == "statement":
            r = rx(s["regex"], re.M)
            for start, piece in prep.statements(raw or rd.get("code_text") == "raw"):
                m = r.search(piece)
                if m:
                    hits.append(_hit("signal", name, decisive, m, code, start))
                    break
        else:
            m = rx(s["regex"], re.M | re.S).search(tt)
            if m:
                hits.append(_hit("signal", name, decisive, m, code))

    for o in rd.get("operator_symbols") or []:
        pos = t.find(o)
        if pos >= 0:
            hits.append({"channel": "operator", "name": o, "decisive": False, "match": o, "line": line_of(code, pos)})

    for ty in rd.get("java_types") or []:
        m = rx(r"\b" + re.escape(ty) + r"\b").search(t)
        if m:
            hits.append(_hit("type", ty, False, m, code))

    cmd_patterns = rd.get("command_patterns") or []
    if cmd_patterns:
        for start, seg in prep.commands:
            for p in cmd_patterns:
                m = rx(p).search(seg)
                if m:
                    hits.append(_hit("command", p, False, m, code, start))

    return hits


def tag_code(code: str, reader: dict[str, dict[str, Any]]) -> dict[str, list[Hit]]:
    """``reader`` maps concept id -> reader block. Returns concept id -> hits
    for every concept with at least one hit."""
    tags: dict[str, list[Hit]] = {}
    prep = Prepared(code)
    for cid, rd in reader.items():
        hits = tag_concept(code, rd, prep)
        if hits:
            tags[cid] = hits
    return tags


# ------------------------------------------------------------------ part 2: extraction

class _Index:
    """Edges of the KG indexed by source and target, built once per KG object."""

    def __init__(self, kg: dict[str, Any]):
        self.out_edges: dict[str, list[dict]] = defaultdict(list)
        self.in_edges: dict[str, list[dict]] = defaultdict(list)
        for e in kg["edges"]:
            self.out_edges[e["source"]].append(e)
            self.in_edges[e["target"]].append(e)
        self.concepts = {c["id"]: c for c in kg["concepts"]}
        self.mis = {m["id"]: m for m in kg.get("misconceptions_and_errors", [])}
        self.levels = {l["id"]: l for l in kg.get("learning_levels", [])}


_index_cache: dict[int, _Index] = {}


def _index(kg: dict[str, Any]) -> _Index:
    idx = _index_cache.get(id(kg))
    if idx is None:
        idx = _Index(kg)
        _index_cache[id(kg)] = idx
    return idx


def _prune_generic(idx: "_Index", tags: dict[str, list[Hit]]) -> dict[str, list[Hit]]:
    """Drop generic concepts that neither share a relation edge with a non-generic tagged concept nor
    fired a decisive signal."""
    generic = {c for c in tags if idx.concepts.get(c, {}).get("reader", {}).get("generic")}
    specific = set(tags) - generic
    keep: dict[str, list[Hit]] = {c: h for c, h in tags.items() if c not in generic}
    for g in generic:
        decisive = any(h["decisive"] for h in tags[g])
        linked = any(e["type"] in ("prerequisite", "parallel") and (e["source"] in specific or e["target"] in specific)
                     for e in idx.out_edges.get(g, []) + idx.in_edges.get(g, []))
        if decisive or linked:
            keep[g] = tags[g]
    return keep


def _skipped_signals(rd: dict[str, Any]) -> list[str]:
    return [s.get("name", "?") for s in rd.get("signals") or [] if "regex" not in s]


def extract_subgraph(kg: dict[str, Any], tags: dict[str, list[Hit]], scenario: str | None = None, hops: int = 0,
                     keep_generic: bool = False) -> dict[str, Any]:
    """Concept nodes are the concepts whose code patterns fired, minus bare generic ones.

    A concept the KG marks ``generic`` (statement, identifier, literal, int, ...) fires on almost any Java
    line. It is kept only when the code ties it to something specific: the KG has a prerequisite or
    parallel edge between it and a non-generic tagged concept, or one of its own decisive signals fired.
    ``keep_generic=True`` keeps every tagged concept. With ``hops=1`` the source of each incoming
    prerequisite edge of a non-generic concept is added as well (one hop, never from generic concepts);
    the default adds nothing the code did not show."""
    idx = _index(kg)
    if not keep_generic:
        tags = _prune_generic(idx, tags)

    # 1. concept nodes: tagged; optionally one prerequisite hop from non-generic tagged concepts
    concepts: dict[str, dict[str, Any]] = {}
    for cid, hits in tags.items():
        if cid not in idx.concepts:
            continue
        concepts[cid] = {"id": cid, "why": "code", "hits": hits, "generic": bool(idx.concepts[cid].get("reader", {}).get("generic"))}
    for cid in (list(concepts) if hops else []):
        if concepts[cid]["generic"]:
            continue
        for e in idx.in_edges.get(cid, []):
            if e["type"] != "prerequisite":
                continue
            src = e["source"]
            if src in concepts or src not in idx.concepts:
                continue
            concepts[src] = {"id": src, "why": f"prerequisite_of:{cid}", "hits": [], "generic": bool(idx.concepts[src].get("reader", {}).get("generic"))}

    node_set = set(concepts)

    # 2. concept edges with both ends inside
    concept_edges: list[dict[str, Any]] = []
    seen: set[tuple[str, str, str]] = set()
    for cid in node_set:
        for e in idx.out_edges.get(cid, []):
            if e["type"] not in ("prerequisite", "parallel") or e["target"] not in node_set:
                continue
            key = (e["type"], e["source"], e["target"])
            if key in seen:
                continue
            seen.add(key)
            eid = f"pre:{e['source']}->{e['target']}" if e["type"] == "prerequisite" else f"par:{e['source']}~{e['target']}"
            concept_edges.append({"id": eid, "type": e["type"], "source": e["source"], "target": e["target"],
                                  "logic": e.get("logic"), "grounding": e.get("grounding")})

    # 3. misconception and error edges from concept nodes, with their target records
    mis_edges: list[dict[str, Any]] = []
    misconceptions: dict[str, dict[str, Any]] = {}
    for cid in node_set:
        for e in idx.out_edges.get(cid, []):
            if e["type"] not in ("misconception", "error"):
                continue
            pre = "mis" if e["type"] == "misconception" else "err"
            mis_edges.append({"id": f"{pre}:{e['source']}->{e['target']}", "type": e["type"], "source": e["source"],
                              "target": e["target"], "role": e.get("role"), "logic": e.get("logic"), "twin_logic": e.get("twin_logic")})
            rec = idx.mis.get(e["target"], {})
            misconceptions.setdefault(e["target"], {"id": e["target"], "kind": rec.get("kind", e["type"]),
                                                    "wrong_belief": rec.get("wrong_belief"), "correct_rule": rec.get("correct_rule")})

    # 4. level edges and nodes
    level_edges: list[dict[str, Any]] = []
    levels: dict[str, dict[str, Any]] = {}
    for cid in node_set:
        for e in idx.out_edges.get(cid, []):
            if e["type"] != "has_level":
                continue
            level_edges.append({"id": f"lvl:{e['source']}->{e['target']}", "type": "has_level", "source": e["source"],
                                "target": e["target"], "level": e.get("level"), "logic": e.get("logic"), "ways": e.get("ways") or []})
            rec = idx.levels.get(e["target"], {})
            levels[e["target"]] = {"id": e["target"], "concept": rec.get("concept", cid), "level": rec.get("level", e.get("level")),
                                   "name": rec.get("name"), "criterion": rec.get("criterion"), "deciding_question": rec.get("deciding_question")}

    # 5. level <-> misconception links (live inside the ways); edges visited in id order so the output is deterministic
    level_mis_links: list[dict[str, Any]] = []
    for le in sorted(level_edges, key=lambda e: e["id"]):
        for i, way in enumerate(le["ways"]):
            for m in way.get("linked_misconception") or []:
                level_mis_links.append({"level_node": le["target"], "misconception": m, "way": way.get("way"),
                                        "way_index": i, "rule_type": way.get("rule_type"), "exact_rule": way.get("exact_rule")})

    # connectivity of the concept nodes over the concept edges (reported, never altered)
    nbrs: dict[str, set[str]] = {c: set() for c in node_set}
    for e in concept_edges:
        nbrs[e["source"]].add(e["target"]); nbrs[e["target"]].add(e["source"])
    components: list[list[str]] = []
    seen_c: set[str] = set()
    for n in sorted(node_set):
        if n in seen_c:
            continue
        stack, comp = [n], set()
        while stack:
            x = stack.pop()
            if x in comp:
                continue
            comp.add(x); stack.extend(nbrs[x] - comp)
        seen_c |= comp; components.append(sorted(comp))

    warnings = []
    if len(components) > 1:
        warnings.append(f"concept nodes form {len(components)} pieces (the KG has no edge between them): " + " | ".join(",".join(c) for c in components))
    for cid in tags:
        for name in _skipped_signals(idx.concepts.get(cid, {}).get("reader", {})):
            warnings.append(f"{cid}.{name}: compiler-message signal, needs javac output; skipped")

    def _sort_level(l: dict) -> tuple:
        return (l["concept"] or "", l["level"] or "")

    return {
        "scenario": scenario,
        "concepts": sorted(concepts.values(), key=lambda c: c["id"]),
        "concept_edges": sorted(concept_edges, key=lambda e: e["id"]),
        "misconceptions": sorted(misconceptions.values(), key=lambda m: m["id"]),
        "mis_edges": sorted(mis_edges, key=lambda e: e["id"]),
        "levels": sorted(levels.values(), key=_sort_level),
        "level_edges": sorted(level_edges, key=lambda e: e["id"]),
        "level_mis_links": level_mis_links,
        "components": components,
        "counts": {
            "tagged": len(tags), "concepts": len(concepts), "generic": sum(1 for c in concepts.values() if c["generic"]), "from_hop": sum(1 for c in concepts.values() if c["why"] != "code"), "concept_edges": len(concept_edges),
            "misconceptions": len(misconceptions), "mis_edges": len(mis_edges), "levels": len(levels),
            "level_edges": len(level_edges), "level_mis_links": len(level_mis_links), "components": len(components),
        },
        "warnings": warnings,
    }


def subgraph_from_code(code: str, kg: dict[str, Any], scenario: str | None = None, hops: int = 0, keep_generic: bool = False) -> dict[str, Any]:
    """Tag the code with the concept patterns, then take the subgraph out."""
    return extract_subgraph(kg, tag_code(code, reader_blocks(kg)), scenario, hops, keep_generic)
