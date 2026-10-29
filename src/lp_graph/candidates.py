"""Step 2 of the pipeline - candidate concepts and the main concept.

**Personalized PageRank** picks the candidates. Graph: concept nodes only,
relation edges undirected for relatedness (prerequisite weight 1.0,
parallel 0.5). The restart vector is seeded from the concepts of the inputs:
code statements the question points at x1.0, other code x0.3, question
x0.6, answer (named directly) x0.4, answer context x0.1; generic concepts
(``lexicon.GENERIC``: declaration, variable, int, ...) x0.2 unless the
question or answer names them. Power iteration with restart 0.5, tolerance
1e-10, at most 200 iterations (numpy, deterministic).

Candidates = all seeds + the top-k non-seed nodes within 2 hops of a seed
(the *bridges*, ranked by ``pi/deg`` so hubs do not win by size), the
prerequisite parents and parallel (contrast) neighbours of the main concept,
with all relation edges among candidates and the misconception edges of
candidates (plus those of misconceptions whose misinterpreter changes the
code's result).

**Main concept** - an ordered rule, not PageRank. Over the non-generic
candidates, the largest key wins:

1. the question's target: concepts of the code that computes what the
   question asks about (a named variable, the output, the lines named), the
   commands, a construct the question names, or for a fix question the
   errors;
2. a decisive code pattern (``lexicon.DECISIVE``) in that code (or in code
   the student wrote);
3. how often the answer names the concept directly;
4. the PageRank score (without degree division);
5. the id.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

import numpy as np

from . import lexicon
from .statements import Statement

if TYPE_CHECKING:  # pragma: no cover
    from .execution import Trace
    from .graph import KG, MisEdge, RelEdge
    from .statements import CodeContext

SOURCE_WEIGHT = {"code": 1.0, "question": 0.6, "answer": 0.4, "answer_code": 0.4}
OTHER_CODE = 0.3
CONTEXT_WEIGHT = 0.1
GENERIC_FACTOR = 0.2
EDGE_WEIGHT = {"prerequisite": 1.0, "parallel": 0.5}
RESTART = 0.5
TOL = 1e-10
MAX_ITER = 200
TOP_K = 6
BRIDGE_HOPS = 2


@dataclass
class Candidates:
    """PPR result and the main concept."""

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
    raw: dict[str, float] = field(default_factory=dict)       # PageRank without degree division
    target: list[str] = field(default_factory=list)           # question-target concepts
    decisive: list[str] = field(default_factory=list)
    main_key: dict[str, list] = field(default_factory=dict)   # candidate -> its key (for the report)

    def to_dict(self) -> dict:
        return {
            "concepts": self.concepts, "bridges": self.bridges,
            "seeds": {k: round(v, 6) for k, v in sorted(self.seeds.items())},
            "seed_sources": {k: v for k, v in sorted(self.seed_sources.items())},
            "scores": {k: round(self.scores[k], 8) for k in self.rank},
            "relation_edges": [e.id for e in self.relation_edges],
            "mis_edges": [m.id for m in self.mis_edges],
            "main_concept": self.main_concept, "main_reason": self.main_reason,
            "question_target": self.target, "decisive": self.decisive,
            "main_key": {k: v for k, v in sorted(self.main_key.items(), key=lambda kv: kv[1], reverse=True)[:8]},
            "iterations": self.iterations,
        }


def seed_vector(statements: list[Statement], target_ids: set[str] = frozenset(),
                named: set[str] = frozenset()) -> tuple[dict[str, float], dict[str, list[str]]]:
    """Seed weight per concept: the sum over sources of the best weight it got
    from that source (each source once)."""
    best: dict[str, dict[str, float]] = {}
    for st in statements:
        src = st.source
        for c in st.concepts:
            if src == "code":
                w = SOURCE_WEIGHT["code"] if (not target_ids or st.id in target_ids) else OTHER_CODE
            elif src in ("answer", "question") and c not in st.direct:
                w = CONTEXT_WEIGHT
            else:
                w = SOURCE_WEIGHT[src]
            if c in lexicon.GENERIC and c not in named:
                w *= GENERIC_FACTOR
            key = "answer" if src == "answer_code" else src
            best.setdefault(c, {})[key] = max(best.get(c, {}).get(key, 0.0), w)
    seeds = {c: sum(v.values()) for c, v in best.items()}
    return seeds, {c: sorted(v) for c, v in best.items()}


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


def question_target(statements: list[Statement], ctx: "CodeContext | None",
                    trace: "Trace | None") -> tuple[set[str], set[str], set[str]]:
    """(target concepts, target code statement ids, decisive concepts there)."""
    code = [s for s in statements if s.source == "code" and not s.is_result]
    qs = [s for s in statements if s.source == "question"]
    qtypes = {t for s in qs for t in s.qtypes}
    tvars = {v for s in qs for v in s.meta.get("targets", s.variables)}
    ids: set[str] = set()
    if tvars:
        ids = {s.id for s in code if tvars & set(s.meta.get("assigns", []))}
    if not ids and "output" in qtypes:
        ids = {s.id for s in code if s.meta.get("kind") == "print"}
    if not ids:
        ids = {s.id for s in code}
    target: set[str] = set()
    for s in code:
        if s.id in ids:
            target |= set(s.meta.get("producer") or s.concepts)
    for s in qs:
        target |= set(s.direct)
    if "fix" in qtypes or "why" in qtypes:
        target |= {c for s in statements if s.is_result for c in s.concepts}
    decisive: set[str] = set()
    findings = list(trace.findings if trace else ()) + list(trace.answer_findings if trace else ())
    by_index = {s.meta.get("index"): s.id for s in code}
    for f in findings:
        if f.pattern not in lexicon.DECISIVE:
            continue
        sid = by_index.get(f.stmt_index)
        concept = lexicon.DECISIVE[f.pattern]
        if f in (trace.answer_findings if trace else ()) or sid is None or sid in ids or not ids                 or concept in target:  # e.g. the loop around the asked-about prints
            decisive.add(concept)
    return target, ids, decisive


def select(kg: "KG", statements: list[Statement], trace: "Trace | None" = None,
           top_k: int = TOP_K, ctx: "CodeContext | None" = None,
           extra_mis: set[str] = frozenset()) -> Candidates:
    """Run PPR, pick candidates and bridges, and choose the main concept."""
    target, target_ids, decisive = question_target(statements, ctx, trace)
    named = {c for s in statements if s.source in ("question", "answer", "answer_code") for c in s.direct}
    seeds, seed_sources = seed_vector(statements, target_ids, named)
    for c in decisive:
        seeds[c] = seeds.get(c, 0.0) + SOURCE_WEIGHT["code"]
        if "code" not in seed_sources.setdefault(c, []):
            seed_sources[c].append("code")
    seeds = {c: v for c, v in seeds.items() if c in kg.knowledge.concepts}
    pi, iters = personalized_pagerank(kg, seeds)
    deg = {c: max(1, len(kg.adjacency[c])) for c in kg.concepts}
    raw = {c: float(pi[i]) for i, c in enumerate(kg.concepts)}
    score = {c: raw[c] / deg[c] for c in kg.concepts}
    order = sorted(kg.concepts, key=lambda c: (-score[c], c))
    seed_set = set(seeds)
    near = {c for c in kg.concepts
            if c not in seed_set and any(kg.hop_distance(s, c) <= BRIDGE_HOPS for s in sorted(seed_set))}
    bridges = [c for c in order if c in near][:top_k]
    answer_count: dict[str, int] = {}
    for s in statements:
        if s.source in ("answer", "answer_code"):
            for c in s.direct:
                answer_count[c] = answer_count.get(c, 0) + 1
    main, reason, keys = main_concept(seed_set, target, decisive, answer_count, raw)
    if main:
        extra = [c for c in kg.knowledge.parallel.get(main, []) + kg.knowledge.prerequisites.get(main, [])
                 if c not in seed_set]
        bridges = [c for c in order if c in set(bridges) | set(extra)]
    chosen = seed_set | set(bridges)
    for m in sorted(extra_mis):
        for c in sorted(kg.concepts):
            if any(x.mis == m for x in kg.mis_edges[c]) and c in kg.knowledge.concepts:
                if c not in chosen and (c in seed_set or any(kg.hop_distance(s, c) <= 1 for s in seed_set)):
                    chosen.add(c)
    concepts = [c for c in order if c in chosen]
    rel = kg.edges_between(chosen)
    mis = [m for c in sorted(chosen) for m in kg.mis_edges[c]]
    return Candidates(concepts, seeds, seed_sources, [c for c in concepts if c not in seed_set],
                      {c: score[c] for c in concepts}, concepts, rel, mis, main, reason, iters,
                      {c: raw[c] for c in concepts}, sorted(target & set(kg.knowledge.concepts)),
                      sorted(decisive), keys)


def main_concept(seeds: set[str], target: set[str], decisive: set[str],
                 answer_count: dict[str, int], raw: dict[str, float]) -> tuple[str | None, str, dict]:
    pool = (seeds | decisive) - lexicon.GENERIC or (seeds | decisive)
    if not pool:
        return None, "no seed", {}
    keys = {c: [int(c in target), int(c in decisive), answer_count.get(c, 0), round(raw.get(c, 0.0), 10)]
            for c in pool}
    best = sorted(pool, key=lambda c: ([-x for x in keys[c]], c))[0]
    k = keys[best]
    why = []
    if k[0]:
        why.append("the question asks about it")
    if k[1]:
        why.append("decisive code pattern")
    if k[2]:
        why.append(f"the answer names it {k[2]}x")
    why.append("PageRank" if not why else "")
    return best, "; ".join(w for w in why if w), keys
