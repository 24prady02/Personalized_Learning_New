"""
answer_graph.py — classify a student answer by building its own small graph,
the way the Chapter-1 graph was built: semantic matching proposes the edges,
NLI decides them, and each edge carries the has_level edge logic it matches.

    answer node --has_level(Lk, way)--> concept      (the answer shows that way)
    answer node --holds-->              misconception (an L0 misconception way)

Steps for one answer (the question part asked and the code are the context):

  1. Candidate concepts: the concepts the answer is linked to (identify, with
     the question's concepts as a prior), plus the concepts whose way rules
     are semantically closest to the answer.
  2. Every way of every has_level edge (L0-L4) of each candidate is a
     hypothesis: its rule sentences (L0: the everyday or wrong reading).
     A way is matched when the answer is on its topic (MiniLM similarity
     >= SIM_GATE) and the answer, read with its question, entails the rule
     more than the question alone does:
         support = NLI(question + answer => rule) - NLI(question => rule)
     The subtraction keeps the question from earning the student a level.
  3. Code-run edges: values the run confirms are L2 ways; claims the run
     contradicts are wrong traces (L0 inconsistent_trace when they are at
     least as many as the confirmed ones); a misconception whose run gives
     the student's values is an L0 misconception edge.
  4. Optional question-form edges (mode "full"): the engine's answers to a
     part that asks beyond the code (L4) or why / fix (L3).
  5. Level of each concept = the highest level with a matched way; L0 when an
     L0 way is matched at least as strongly as any higher one; L1 when the
     answer is on the concept's topic but shows no way; otherwise not assessed.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from functools import lru_cache
from typing import Dict, List, Optional, Tuple

from . import models
from .identify import identify
from .knowledge import Concept, PercptKnowledge, Way

SIM_GATE = 0.35        # answer must be this similar to a way rule before NLI is asked
EDGE = 0.50            # support needed for a has_level edge
TOPIC = 0.45           # on the concept's topic (description / facts) -> L1 names_the_element
N_SEM_EXTRA = 2        # extra candidate concepts from way-rule similarity
LEVELS = ("L0", "L1", "L2", "L3", "L4")


@lru_cache(maxsize=2)
def _nli_model(name: str):
    from sentence_transformers import CrossEncoder
    m = CrossEncoder(name)
    labels = {v.lower(): int(k) for k, v in m.model.config.id2label.items()}
    return m, labels


def nli(pairs: List[Tuple[str, str]], name: str) -> List[Dict[str, float]]:
    if not pairs:
        return []
    m, labels = _nli_model(name)
    probs = m.predict(pairs, apply_softmax=True, show_progress_bar=False, batch_size=64)
    return [{k: float(p[i]) for k, i in labels.items()} for p in probs]


@dataclass
class Edge:
    concept: str
    level: str
    way: str
    support: float
    rule: str = ""
    source: str = "nli"            # nli | run | question
    misconception: Optional[str] = None

    def to_dict(self) -> Dict:
        return {"concept": self.concept, "level": self.level, "way": self.way, "support": round(self.support, 3),
                "rule": self.rule[:200], "source": self.source, "misconception": self.misconception}


@dataclass
class AnswerGraph:
    edges: List[Edge] = field(default_factory=list)
    levels: Dict[str, Optional[str]] = field(default_factory=dict)    # concept -> level (None: not assessed)
    reasons: Dict[str, str] = field(default_factory=dict)
    topic: Dict[str, float] = field(default_factory=dict)

    def best_level(self) -> Optional[str]:
        lv = [l for l in self.levels.values() if l]
        return max(lv) if lv else None

    def main_concept(self) -> Optional[str]:
        """The assessed concept the answer is most about."""
        lv = {c: l for c, l in self.levels.items() if l}
        return max(lv, key=lambda c: self.topic.get(c, 0)) if lv else None


def _hypotheses(c: Concept) -> List[Tuple[str, Way, str]]:
    """(level, way, rule sentence) for every way of every has_level edge; the
    inconsistent_trace way is decided by the code run, not by wording."""
    out = []
    for lv in LEVELS:
        for w in c.ways.get(lv, []):
            if w.name == "inconsistent_trace":
                continue
            for r in w.rules:
                r = re.sub(r"^\s*(?:rule broken|Kind|Trigger class)\s*:\s*", "", r).strip()
                if len(r) > 12:
                    out.append((lv, w, r))
    return out


def _clauses(text: str) -> List[str]:
    parts = [p.strip(" ,") for p in re.split(r"(?<=[.!?;])\s+|\n+", text or "") if p.strip(" ,")]
    return [p for p in parts if len(p) > 3] or [text.strip()]


def build(text: str, asked: str, code: str, kg: PercptKnowledge, nli_name: str,
          run_edges: Optional[List[Edge]] = None, question_edges: Optional[List[Edge]] = None) -> AnswerGraph:
    g = AnswerGraph()
    answer = (text or "").strip()
    clauses = _clauses(answer)
    units = list(dict.fromkeys(clauses + [answer]))      # each clause and the whole answer

    # 1 — candidate concepts
    hits = identify(answer, kg, code=code, asked=asked)
    cands = [h.concept for h in hits]
    all_hyp = {cid: _hypotheses(kg.concepts[cid]) for cid in kg.concepts}
    flat = [(cid, r) for cid, hs in all_hyp.items() for _, _, r in hs]
    sim_all = models.similarity(units, [r for _, r in flat])
    best: Dict[str, float] = {}
    for j, (cid, _) in enumerate(flat):
        best[cid] = max(best.get(cid, 0.0), float(sim_all[:, j].max()))
    for cid in sorted(best, key=lambda k: -best[k]):
        if len(cands) >= len(hits) + N_SEM_EXTRA:
            break
        if cid not in cands:
            cands.append(cid)

    # topic similarity (description and facts) for the L1 fallback
    for cid in cands:
        c = kg.concepts[cid]
        tgt = [f"{c.label.replace('_', ' ')}: {c.description}"] + c.facts
        g.topic[cid] = float(models.similarity(units, tgt).max())

    # 2 — every way of every has_level edge, decided by NLI
    pairs, where = [], []
    q = (asked or "").strip()
    for cid in cands:
        hyps = all_hyp[cid]
        if not hyps:
            continue
        sim = models.similarity(units, [r for _, _, r in hyps])
        for j, (lv, w, r) in enumerate(hyps):
            if float(sim[:, j].max()) < SIM_GATE:
                continue
            for u in units:
                pairs.append(((f"{q} {u}" if q else u), r)); where.append((cid, lv, w, r, "qa"))
            if q:
                pairs.append((q, r)); where.append((cid, lv, w, r, "q"))
    res = nli(pairs, nli_name)
    qa: Dict[Tuple, float] = {}
    qonly: Dict[Tuple, float] = {}
    for (cid, lv, w, r, kind), p in zip(where, res):
        key = (cid, lv, w.name, r)
        val = p["entailment"] if p["contradiction"] < 0.3 else 0.0
        if kind == "qa":
            qa[key] = max(qa.get(key, 0.0), val)
        else:
            qonly[key] = val
    ways_of = {(cid, lv, w.name, r): w for cid in cands for lv, w, r in all_hyp[cid]}
    for key, e in qa.items():
        support = e - qonly.get(key, 0.0)
        if support >= EDGE:
            cid, lv, wname, r = key
            w = ways_of[key]
            if w.requires and not any(t in kg.concepts and t in cands for t in w.requires):
                continue                       # a relation way needs the concept it relates to
            g.edges.append(Edge(cid, lv, wname, support, r, "nli",
                                w.misconceptions[0] if (lv == "L0" and w.misconceptions) else None))

    # 3-4 — code-run and question-form edges
    for e in (run_edges or []) + (question_edges or []):
        if e.concept not in cands:
            cands.append(e.concept)
            g.topic.setdefault(e.concept, 0.5)
        g.edges.append(e)

    # 5 — level per concept (highest way shown; L0 when its way is at least as strong)
    for cid in cands:
        es = [e for e in g.edges if e.concept == cid]
        up = [e for e in es if e.level != "L0"]
        l0 = [e for e in es if e.level == "L0"]
        best_up = max(up, key=lambda e: (e.level, e.support)) if up else None
        best_l0 = max(l0, key=lambda e: e.support) if l0 else None
        if best_l0 and (not up or best_l0.support >= max(e.support for e in up)):
            g.levels[cid] = "L0"
            g.reasons[cid] = f"L0 {best_l0.way} ({best_l0.source}, {best_l0.support:.2f}): {best_l0.rule[:90]}"
        elif best_up:
            g.levels[cid] = best_up.level
            g.reasons[cid] = f"{best_up.level} {best_up.way} ({best_up.source}, {best_up.support:.2f}): {best_up.rule[:90]}"
        elif g.topic.get(cid, 0) >= TOPIC:
            g.levels[cid] = "L1"
            g.reasons[cid] = f"L1 names_the_element (on topic, {g.topic[cid]:.2f}); no way matched"
        else:
            g.levels[cid] = None
            g.reasons[cid] = "not assessed: no way matched and off topic"
    return g
