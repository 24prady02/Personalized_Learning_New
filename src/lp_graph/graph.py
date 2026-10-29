"""Step 1 - the graph: load ``data/chapter1_kg.json`` for traversal.

``KG`` wraps the knowledge object (concepts, ways, misconceptions) and adds
what the graph algorithms need:

* ``out[type][source]`` / ``inn[type][target]``: adjacency per edge type,
  sorted by id;
* ``relation_edges``: prerequisite + parallel edges as ``RelEdge`` objects.
  ``stateable`` is False for ``questionable`` and ``order_only`` grounding:
  such an edge is never counted as lacking. A parallel edge is one object
  that may be walked both ways;
* ``mis_edges[concept]``: misconception / error edges as ``MisEdge``;
* ``topo`` and ``depth`` of the prerequisite DAG (validated acyclic);
* ``hop[a][b]``: undirected hop distance over relation edges (all pairs,
  precomputed once by BFS);
* ``aliases`` and ``alias_index`` for finding concepts in text;
* ``parts``: the derived data of ``data/kg_parts.json`` (edge-logic parts
  with slots, way slots, misconception slots). Built in memory when the
  file is missing or was generated from a different graph file.

Edges have no ids in the JSON, so ids are derived:
``pre:src->dst``, ``par:src~dst``, ``mis:concept->node``, ``err:concept->node``.
"""

from __future__ import annotations

import hashlib
import json
import logging
from collections import deque
from dataclasses import dataclass
from graphlib import CycleError, TopologicalSorter
from pathlib import Path

from . import lexicon
from .cues import load_cues
from .knowledge import DEFAULT_KG_PATH, PercptKnowledge, Way, load_knowledge
from .slots import normalize

log = logging.getLogger(__name__)

DEFAULT_PARTS_PATH = DEFAULT_KG_PATH.parent / "kg_parts.json"
NOT_STATEABLE = frozenset({"questionable", "order_only"})
RELATION_TYPES = ("prerequisite", "parallel")
MIS_TYPES = ("misconception", "error")
FAR = 99  # hop distance between unconnected concepts


@dataclass(frozen=True)
class RelEdge:
    """A prerequisite or parallel edge between two concepts."""

    id: str
    src: str
    dst: str
    kind: str
    logic: str
    contrast: str
    stateable: bool
    grounding: str

    def touches(self, concept: str) -> bool:
        return concept in (self.src, self.dst)

    def other(self, concept: str) -> str:
        return self.dst if concept == self.src else self.src

    @property
    def undirected_key(self) -> tuple[str, str]:
        a, b = sorted((self.src, self.dst))
        return (a, b)


@dataclass(frozen=True)
class MisEdge:
    """A misconception (or error) attached to a concept."""

    id: str
    concept: str
    mis: str
    wrong: str
    right: str
    role: str
    kind: str


def edge_id(kind: str, src: str, dst: str) -> str:
    if kind == "prerequisite":
        return f"pre:{src}->{dst}"
    if kind == "parallel":
        return f"par:{src}~{dst}"
    if kind == "error":
        return f"err:{src}->{dst}"
    return f"mis:{src}->{dst}"


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class KG:
    """The knowledge graph prepared for PPR, reading and ES-Viterbi."""

    def __init__(self, path: str | Path = DEFAULT_KG_PATH,
                 parts_path: str | Path | None = DEFAULT_PARTS_PATH) -> None:
        self.path = Path(path)
        self.parts_path = Path(parts_path) if parts_path else None
        self.knowledge: PercptKnowledge = load_knowledge(self.path)
        lexicon.load(self.knowledge.raw)  # the reader's vocabulary comes from this graph
        self.version = self.knowledge.version
        self.source_hash = file_hash(self.path)
        self.concepts: list[str] = sorted(self.knowledge.concepts)
        self._concept_set = frozenset(self.concepts)
        self.out: dict[str, dict[str, list[str]]] = {}
        self.inn: dict[str, dict[str, list[str]]] = {}
        self.relation_edges: dict[str, RelEdge] = {}
        self.mis_edges: dict[str, list[MisEdge]] = {c: [] for c in self.concepts}
        self._load_edges()
        self.rel_by_concept: dict[str, list[str]] = {c: [] for c in self.concepts}
        for eid in sorted(self.relation_edges):
            e = self.relation_edges[eid]
            self.rel_by_concept[e.src].append(eid)
            self.rel_by_concept[e.dst].append(eid)
        self.topo, self.depth = self._topological()
        self.hop = self._hop_distances()
        self.cues = load_cues()
        self.aliases = self._aliases()
        self.alias_index = self._alias_index(resolve_verbs=True)
        self.alias_index_strict = self._alias_index(resolve_verbs=False)
        self._parts: dict | None = None
        log.info("KG %s: %d concepts, %d relation edges, %d misconception edges",
                 self.version, len(self.concepts), len(self.relation_edges),
                 sum(len(v) for v in self.mis_edges.values()))

    # ------------------------------------------------------------ loading
    def _load_edges(self) -> None:
        for e in self.knowledge.raw.get("edges", []):
            kind, src, dst = e.get("type"), e.get("source"), e.get("target")
            if not kind or not src or not dst:
                continue
            self.out.setdefault(kind, {}).setdefault(src, []).append(dst)
            self.inn.setdefault(kind, {}).setdefault(dst, []).append(src)
            if kind in RELATION_TYPES and src in self._concept_set and dst in self._concept_set:
                contrast = e.get("contrast")
                if isinstance(contrast, dict):
                    contrast = contrast.get("logic") or ""
                grounding = str(e.get("grounding") or "book_passage")
                eid = edge_id(kind, src, dst)
                self.relation_edges[eid] = RelEdge(
                    eid, src, dst, kind, str(e.get("logic") or ""), str(contrast or ""),
                    grounding not in NOT_STATEABLE, grounding)
            elif kind in MIS_TYPES and src in self._concept_set:
                node = self.knowledge.misconceptions.get(dst)
                right = str(e.get("twin_logic") or (node.correct_rule if node else ""))
                wrong = str(e.get("logic") or (node.wrong_belief if node else ""))
                self.mis_edges[src].append(MisEdge(
                    edge_id(kind, src, dst), src, dst, wrong, right,
                    str(e.get("role") or ""), kind))
        for table in (self.out, self.inn):
            for kind in table:
                for k in table[kind]:
                    table[kind][k] = sorted(set(table[kind][k]))
        for c in self.mis_edges:
            self.mis_edges[c].sort(key=lambda m: m.id)

    def _topological(self) -> tuple[list[str], dict[str, int]]:
        ts: TopologicalSorter = TopologicalSorter()
        for c in self.concepts:
            ts.add(c, *self.inn.get("prerequisite", {}).get(c, []))
        try:
            ts.prepare()
        except CycleError as exc:
            raise ValueError(f"prerequisite subgraph has a cycle: {exc.args[1]}") from exc
        order: list[str] = []
        while ts.is_active():
            ready = sorted(ts.get_ready())
            order.extend(ready)
            ts.done(*ready)
        order = [c for c in order if c in self._concept_set]
        depth: dict[str, int] = {}
        for c in order:
            parents = [p for p in self.inn.get("prerequisite", {}).get(c, []) if p in depth]
            depth[c] = 1 + max((depth[p] for p in parents), default=-1)
        lonely = [c for c in self.concepts
                  if not self.inn.get("prerequisite", {}).get(c)
                  and not self.out.get("prerequisite", {}).get(c)]
        if lonely:
            log.info("concepts with no prerequisite edge: %s", ", ".join(lonely))
        self.no_prerequisite_edge = lonely
        return order, depth

    def _hop_distances(self) -> dict[str, dict[str, int]]:
        adj: dict[str, list[str]] = {c: [] for c in self.concepts}
        for e in self.relation_edges.values():
            adj[e.src].append(e.dst)
            adj[e.dst].append(e.src)
        for c in adj:
            adj[c] = sorted(set(adj[c]))
        hop: dict[str, dict[str, int]] = {}
        for s in self.concepts:
            dist = {s: 0}
            q = deque([s])
            while q:
                u = q.popleft()
                for v in adj[u]:
                    if v not in dist:
                        dist[v] = dist[u] + 1
                        q.append(v)
            hop[s] = dist
        self.adjacency = adj
        return hop

    def _aliases(self) -> dict[str, list[str]]:
        out: dict[str, list[str]] = {}
        for cid in self.concepts:
            c = self.knowledge.concepts[cid]
            names = []
            for auto in (cid, c.label):
                a = normalize(auto)
                if a and a not in lexicon.STOP_ALIASES:
                    names.append(a)
            names += [normalize(w) for w in self.cues.get(cid, {}).get("words", [])]
            out[cid] = sorted({n for n in names if n})
        return out

    def _alias_index(self, resolve_verbs: bool) -> list[tuple[str, tuple[str, ...]]]:
        table: dict[str, list[str]] = {}
        for cid in self.concepts:
            for a in self.aliases[cid]:
                table.setdefault(a, []).append(cid)
        index = {a: tuple(sorted(set(cs))) for a, cs in table.items()}
        if resolve_verbs:
            for verb, options in lexicon.VERB_RESOLVE.items():
                index[normalize(verb)] = tuple(o for o in options if o in self._concept_set)
        return sorted(index.items(), key=lambda kv: (-len(kv[0]), kv[0]))

    # ------------------------------------------------------------- access
    def hop_distance(self, a: str, b: str) -> int:
        return self.hop.get(a, {}).get(b, FAR)

    def ways(self, concept: str, level: str) -> list[Way]:
        return self.knowledge.ways_at(concept, level)

    def edges_between(self, concepts: list[str] | set[str]) -> list[RelEdge]:
        cs = set(concepts)
        return [self.relation_edges[eid] for eid in sorted(self.relation_edges)
                if self.relation_edges[eid].src in cs and self.relation_edges[eid].dst in cs]

    def prerequisite_edge(self, src: str, dst: str) -> RelEdge | None:
        return self.relation_edges.get(edge_id("prerequisite", src, dst))

    @property
    def parts(self) -> dict:
        """Derived reader data (``data/kg_parts.json``), loaded or built once."""
        if self._parts is None:
            self._parts = self._load_parts()
        return self._parts

    def _load_parts(self) -> dict:
        from .parts import build_parts

        if self.parts_path and self.parts_path.exists():
            with self.parts_path.open(encoding="utf-8") as fh:
                data = json.load(fh)
            if data.get("source_hash") == self.source_hash:
                return data
            log.warning("%s was generated from another graph file; rebuilding in memory "
                        "(run scripts/prepare_kg_parts.py)", self.parts_path.name)
        return build_parts(self)
