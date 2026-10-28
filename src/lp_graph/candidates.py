"""Step 2 of the pipeline - Personalized PageRank picks the candidate concepts.

Graph: concept nodes only, relation edges undirected for relatedness
(prerequisite weight 1.0, parallel 0.5). The restart vector is seeded from
the concepts of the three inputs - code x1.0, question x0.6, answer x0.4 -
and normalised. Power iteration with restart 0.5, tolerance 1e-10, at most
200 iterations (numpy, deterministic). Nodes are ranked by ``pi[v]/deg(v)``
(degree correction, so hubs do not win by size), ties by id.

Candidates = all seeds + the top-k non-seed nodes within 2 hops of a seed
(the *bridges*), with all relation edges among candidates and all
misconception edges of candidates. The parallel (contrast) neighbours of the
main concept are added as bridges too, so a value borrowed from a contrast
concept (array elements default to 0) can be read.

Main concept = the highest-ranked code or question seed, unless the code
shows a decisive pattern (``lexicon.DECISIVE``), which forces its concept.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

import numpy as np

from . import lexicon
from .statements import Statement

if TYPE_CHECKING:  # pragma: no cover
    from .execution import Trace
    from .graph import KG, MisEdge, RelEdge

SOURCE_WEIGHT = {"code": 1.0, "question": 0.6, "answer": 0.4}
EDGE_WEIGHT = {"prerequisite": 1.0, "parallel": 0.5}
RESTART = 0.5
TOL = 1e-10
MAX_ITER = 200
TOP_K = 6
BRIDGE_HOPS = 2


@dataclass
class Candidates:
    """PPR result."""

    concepts: list[str]                 # seeds + bridges, by rank
    seeds: dict[str, float]             # concept -> seed weight (before normalising)
    seed_sources: dict[str, list[str]]  # concept -> sources it was seeded from
    bridges: list[str]
    scores: dict[str, float]            # degree-corrected score of every candidate
    rank: list[str]                     # all candidates by corrected score
    relation_edges: list["RelEdge"]
    mis_edges: list["MisEdge"]
    main_concept: str | None
    main_reason: str
    iterations: int

    def to_dict(self) -> dict:
        return {
            "concepts": self.concepts, "bridges": self.bridges,
            "seeds": {k: round(v, 6) for k, v in sorted(self.seeds.items())},
            "seed_sources": {k: v for k, v in sorted(self.seed_sources.items())},
            "scores": {k: round(self.scores[k], 8) for k in self.rank},
            "relation_edges": [e.id for e in self.relation_edges],
            "mis_edges": [m.id for m in self.mis_edges],
            "main_concept": self.main_concept, "main_reason": self.main_reason,
            "iterations": self.iterations,
        }


def seed_vector(statements: list[Statement]) -> tuple[dict[str, float], dict[str, list[str]]]:
    """Seed weight per concept: the sum of its source weights (each source once)."""
    sources: dict[str, set[str]] = {}
    for st in statements:
        for c in st.concepts:
            sources.setdefault(c, set()).add(st.source)
    seeds = {c: sum(SOURCE_WEIGHT[s] for s in sorted(srcs)) for c, srcs in sources.items()}
    return seeds, {c: sorted(s) for c, s in sources.items()}


def personalized_pagerank(kg: "KG", seeds: dict[str, float]) -> tuple[np.ndarray, int]:
    """Stationary vector over ``kg.concepts`` (fixed order)."""
    idx = {c: i for i, c in enumerate(kg.concepts)}
    n = len(kg.concepts)
    w = np.zeros((n, n))
    for eid in sorted(kg.relation_edges):
        e = kg.relation_edges[eid]
        a, b = idx[e.src], idx[e.dst]
        w[a, b] += EDGE_WEIGHT[e.kind]
        w[b, a] += EDGE_WEIGHT[e.kind]
    deg = w.sum(axis=1)
    p = np.divide(w, deg[:, None], out=np.zeros_like(w), where=deg[:, None] > 0)
    s = np.zeros(n)
    for c in sorted(seeds):
        if c in idx:
            s[idx[c]] = seeds[c]
    if s.sum() == 0:
        s[:] = 1.0
    s = s / s.sum()
    pi = s.copy()
    it = 0
    for it in range(1, MAX_ITER + 1):
        nxt = RESTART * s + (1 - RESTART) * (pi @ p)
        dangling = (1 - RESTART) * pi[deg == 0].sum()
        nxt += dangling * s
        if np.abs(nxt - pi).sum() < TOL:
            pi = nxt
            break
        pi = nxt
    return pi, it


def select(kg: "KG", statements: list[Statement], trace: "Trace | None" = None,
           top_k: int = TOP_K) -> Candidates:
    """Run PPR and pick candidates, bridges and the main concept."""
    seeds, seed_sources = seed_vector(statements)
    seeds = {c: v for c, v in seeds.items() if c in kg.knowledge.concepts}
    pi, iters = personalized_pagerank(kg, seeds)
    deg = {c: max(1, len(kg.adjacency[c])) for c in kg.concepts}
    score = {c: float(pi[i]) / deg[c] for i, c in enumerate(kg.concepts)}
    order = sorted(kg.concepts, key=lambda c: (-score[c], c))
    seed_set = set(seeds)
    near = {c for c in kg.concepts
            if c not in seed_set and any(kg.hop_distance(s, c) <= BRIDGE_HOPS for s in sorted(seed_set))}
    bridges = [c for c in order if c in near][:top_k]
    main, reason = main_concept(order, seed_sources, trace)
    # contrast neighbours of the main concept are always bridges: the root
    # cause step looks for a wrong value borrowed from them
    if main in kg.knowledge.parallel:
        extra = [c for c in kg.knowledge.parallel[main] if c not in seed_set and c not in bridges]
        bridges = [c for c in order if c in set(bridges) | set(extra)]
    chosen = seed_set | set(bridges)
    concepts = [c for c in order if c in chosen]
    rel = kg.edges_between(chosen)
    mis = [m for c in sorted(chosen) for m in kg.mis_edges[c]]
    return Candidates(concepts, seeds, seed_sources, bridges,
                      {c: score[c] for c in concepts}, concepts, rel, mis, main, reason, iters)


def main_concept(order: list[str], seed_sources: dict[str, list[str]],
                 trace: "Trace | None") -> tuple[str | None, str]:
    for f in (trace.findings if trace else ()):
        if f.pattern in lexicon.DECISIVE:
            return lexicon.DECISIVE[f.pattern], f"decisive code pattern: {f.pattern} ({f.message})"
    for c in order:
        srcs = seed_sources.get(c, [])
        if "code" in srcs or "question" in srcs:
            return c, "highest-ranked code/question seed"
    for c in order:
        if c in seed_sources:
            return c, "highest-ranked seed (answer only)"
    return None, "no seed"
