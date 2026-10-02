"""
student_graph.py — the self-updating student graph (Steps 10 and 12).

One graph per student, laid over the percpt graph. Per concept it keeps the
`demonstrates` links (evidence by turn), each misconception's latest status,
the `reached` level node, and its flags. After every prompt:

  Stability gates (Step 10)
    G16 No silent drop   evidence accumulates; a level falls only through G13 or G9
    G17 Jump             a rise of >= JUMP levels in one prompt is provisional until repeated
    G18 Repetition       clauses seen before on this concept add no evidence
    G19 Inferred-only    inferred levels never satisfy requirements or trigger gaps
    G20 Staleness        newest evidence for the level older than STALE sessions -> stale
    G21 Teacher override a pinned level is never lowered by the gates

  Inference rules (Step 12), run to a fixpoint
    R1 Accumulate  R2 Position  R3 Misconception cap  R4 Repair  R5 Prerequisite inference
    R6 Gap  R7 At risk  R8 Plateau  R9 Frontier
"""
from __future__ import annotations

import json
import os
import tempfile
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Set

from .evidence import MET, UNCERTAIN, ConceptEvidence
from .knowledge import PercptKnowledge
from .ladder import LEVELS, walk
from .thresholds import JUMP, PLATEAU, STALE


@dataclass
class Node:
    concept: str
    observed: bool = False
    evidence: Dict[str, List[Dict]] = field(default_factory=lambda: {"E1": [], "E2": [], "E3": [], "E4": []})
    contested: List[Dict] = field(default_factory=list)       # evidence voided by a wrong trace (G9)
    uncertain: Dict[str, int] = field(default_factory=dict)   # check -> turn it was last uncertain
    misconceptions: Dict[str, Dict] = field(default_factory=dict)  # id -> {status, turn, boundary}
    level: int = 0
    uncertain_toward: Optional[int] = None
    stop_reason: str = ""
    provisional: bool = False
    pinned_level: Optional[int] = None
    inferred_level: Optional[int] = None
    history: List[List[int]] = field(default_factory=list)   # [turn, level]
    clause_keys: List[str] = field(default_factory=list)
    plateau: bool = False
    stale: bool = False
    at_risk: List[str] = field(default_factory=list)          # misconception ids putting it at risk
    frontier: bool = False
    confidence: str = ""
    last_gates: List[str] = field(default_factory=list)
    last_turn: int = 0

    @property
    def held(self) -> Set[str]:
        return {m for m, s in self.misconceptions.items() if s["status"] == "held"}

    def checks(self) -> Dict[str, str]:
        out = {}
        for e in ("E1", "E2", "E3", "E4"):
            if self.evidence[e]:
                out[e] = MET
            elif e in self.uncertain:
                out[e] = UNCERTAIN
            else:
                out[e] = "not_met"
        return out


class StudentGraph:
    def __init__(self, student_id: str, kg: PercptKnowledge):
        self.student_id = student_id
        self.kg = kg
        self.turn = 0
        self.sessions: List[str] = []
        self.nodes: Dict[str, Node] = {}
        self.gaps: List[List[str]] = []          # [prerequisite, concept]

    # ── persistence ─────────────────────────────────────────────────────────
    def to_dict(self) -> Dict:
        return {"student_id": self.student_id, "turn": self.turn, "sessions": self.sessions,
                "graph_version": self.kg.version, "gaps": self.gaps,
                "nodes": {k: asdict(v) for k, v in self.nodes.items()}}

    @classmethod
    def from_dict(cls, d: Dict, kg: PercptKnowledge) -> "StudentGraph":
        g = cls(d["student_id"], kg)
        g.turn = d.get("turn", 0)
        g.sessions = d.get("sessions", [])
        g.gaps = d.get("gaps", [])
        for k, v in d.get("nodes", {}).items():
            if k in kg.concepts:
                g.nodes[k] = Node(**v)
        return g

    def save(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        fd, tmp = tempfile.mkstemp(dir=path.parent, suffix=".tmp")
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            json.dump(self.to_dict(), fh, indent=1)
        os.replace(tmp, path)

    # ── per-prompt update ───────────────────────────────────────────────────
    def node(self, cid: str) -> Node:
        if cid not in self.nodes:
            self.nodes[cid] = Node(cid)
        return self.nodes[cid]

    def begin_turn(self, session_id: Optional[str]) -> None:
        self.turn += 1
        sid = session_id or (self.sessions[-1] if self.sessions else "s1")
        if not self.sessions or self.sessions[-1] != sid:
            self.sessions.append(sid)

    @property
    def session_index(self) -> int:
        return len(self.sessions) - 1

    def apply(self, ev: ConceptEvidence, prompt_level: int) -> Dict:
        """Write one concept's prompt evidence into its node (R1-R4, G9, G16-G21)."""
        c = self.kg.concepts[ev.concept]
        n = self.node(ev.concept)
        before = n.level if n.observed else 0
        was_observed = n.observed
        n.observed, n.frontier, n.last_turn = True, False, self.turn
        gates = list(ev.gates)

        # G18 Repetition: nothing new if every clause was seen before on this concept
        new_keys = [k for k in ev.clause_keys if k not in n.clause_keys]
        repeated = bool(ev.clause_keys) and not new_keys
        if repeated:
            gates.append("repetition")
        else:
            n.clause_keys.extend(new_keys)
            # R1 Accumulate: a demonstrates link per met requirement
            for it in ev.items:
                if it.check in n.evidence and it.status == MET:
                    n.evidence[it.check].append({"turn": self.turn, "session": self.session_index,
                                                 "clause": it.clause, "statement": it.statement,
                                                 "score": round(it.score, 3)})
            for check, status in ev.checks.items():
                if status == UNCERTAIN and not n.evidence[check]:
                    n.uncertain[check] = self.turn
                elif status == MET:
                    n.uncertain.pop(check, None)
            # Misconceptions: latest observation wins
            for mid in ev.held:
                prev = n.misconceptions.get(mid, {}).get("status")
                n.misconceptions[mid] = {"status": "held", "turn": self.turn, "boundary": mid in c.boundary}
                if prev == "refuted":
                    gates.append("regression")
            for mid in ev.refuted:
                prev = n.misconceptions.get(mid, {}).get("status")
                n.misconceptions[mid] = {"status": "refuted", "turn": self.turn, "boundary": mid in c.boundary}
                if prev == "held":       # R4 Repair counts as E4 evidence
                    n.evidence["E4"].append({"turn": self.turn, "session": self.session_index,
                                             "clause": "", "statement": f"repaired {mid}", "score": 1.0})
                    gates.append("repair")
            # G9 Wrong trace: earlier E2+ evidence must be shown again
            if ev.wrong_trace and ev.checks["E2"] != MET:
                for e in ("E2", "E3", "E4"):
                    n.contested.extend({**x, "check": e} for x in n.evidence[e])
                    n.evidence[e] = []

        # R2 Position + R3 cap: re-walk the ladder on all accumulated evidence
        held_boundary = n.held & c.boundary
        res = walk(n.checks(), held_boundary)
        level = res.level
        n.uncertain_toward, n.stop_reason = res.uncertain_toward, res.stop_reason
        if res.blocked_by:
            gates.append("boundary_misconception")

        # G21 Teacher override
        if n.pinned_level is not None and level < n.pinned_level:
            level = n.pinned_level
            gates.append("teacher_override")

        # G17 Jump: provisional until a later prompt shows the same level
        if not repeated:
            if level - before >= JUMP:
                n.provisional = True
                gates.append("jump")
            elif n.provisional and prompt_level >= level:
                n.provisional = False
        n.level = level
        if not repeated:
            n.history.append([self.turn, level])

        # R8 Plateau
        recent = [lv for _, lv in n.history[-PLATEAU:]]
        n.plateau = len(recent) == PLATEAU and len(set(recent)) == 1

        # G20 Staleness: newest evidence for the reached level
        req = {1: "E1", 2: "E2", 3: "E3", 4: "E4"}.get(level)
        newest = max((x["session"] for x in n.evidence.get(req, [])), default=None) if req else None
        n.stale = newest is not None and self.session_index - newest > STALE

        n.last_gates = gates
        return {"before": before, "first_touch": not was_observed, "repeated": repeated}

    def set_override(self, cid: str, level: int) -> None:
        """G21: a teacher pins a level for a concept."""
        n = self.node(cid)
        n.pinned_level = level
        n.observed = True
        n.level = max(n.level, level)

    # ── Step 12: inference rules to a fixpoint ─────────────────────────────
    def infer(self) -> None:
        changed = True
        while changed:
            changed = False
            observed = {k: v for k, v in self.nodes.items() if v.observed}
            # R5 Prerequisite inference (G19: marked inferred, never overrides observed)
            for cid, n in observed.items():
                if n.level >= 2:
                    for p in self.kg.concepts[cid].prerequisites:
                        pn = self.node(p)
                        if not pn.observed and (pn.inferred_level or 0) < 1:
                            pn.inferred_level = 1
                            pn.frontier = False
                            changed = True
            # R7 At risk: a held misconception flags every concept it is linked to
            for cid, n in observed.items():
                for mid in n.held:
                    for other in self.kg.misconceptions[mid].concepts:
                        if other in self.kg.concepts:
                            on = self.node(other)
                            if mid not in on.at_risk:
                                on.at_risk.append(mid)
                                changed = True
            # R9 Frontier: neighbours of engaged concepts, not yet assessed
            for cid in observed:
                for nb in self.kg.concepts[cid].neighbours:
                    nn = self.node(nb)
                    if not nn.observed and nn.inferred_level is None and not nn.frontier:
                        nn.frontier = True
                        changed = True
        # Misconceptions no longer held clear their at-risk marks
        held_now = {m for n in self.nodes.values() if n.observed for m in n.held}
        for n in self.nodes.values():
            n.at_risk = [m for m in n.at_risk if m in held_now]
        # R6 Gap: observed prerequisite lower than the concept it feeds (G19: observed only)
        self.gaps = []
        for cid, n in self.nodes.items():
            if not n.observed:
                continue
            for p in sorted(self.kg.concepts[cid].prerequisites):
                pn = self.nodes.get(p)
                if pn is not None and pn.observed and pn.level < n.level:
                    self.gaps.append([p, cid])

    def prerequisite_blocked(self, cid: str) -> List[str]:
        """G14: prerequisites of `cid` holding a boundary misconception."""
        out = []
        for p in self.kg.concepts[cid].prerequisites:
            pn = self.nodes.get(p)
            if pn is not None and pn.observed and (pn.held & self.kg.concepts[p].boundary):
                out.append(p)
        return out

    def summary(self) -> Dict:
        obs = [n for n in self.nodes.values() if n.observed]
        dist = {lv: 0 for lv in LEVELS}
        for n in obs:
            dist[LEVELS[n.level]] += 1
        return {"observed": len(obs),
                "inferred": sum(1 for n in self.nodes.values() if not n.observed and n.inferred_level),
                "frontier": sum(1 for n in self.nodes.values() if n.frontier),
                "level_distribution": dist, "gaps": len(self.gaps),
                "held_misconceptions": sorted({m for n in obs for m in n.held}),
                "plateaus": sorted(n.concept for n in obs if n.plateau),
                "provisional": sorted(n.concept for n in obs if n.provisional)}
