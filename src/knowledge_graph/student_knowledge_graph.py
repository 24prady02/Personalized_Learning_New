"""
student_knowledge_graph.py — per-student knowledge graph grounded in the
Chapter-1 concept + LP graph (data/chapter1_kg.json).

This is the central data structure CPAL revolves around. Each student's graph
is the part of the Chapter-1 graph that student has touched. Each node carries
everything CPAL has inferred about that student's relationship to that concept:

    LP level             (L0 / L1 / L2 / L3 / L4)       <- LPDiagnostician
    diagnostic_confidence (0.0 - 1.0)                    <- LPDiagnostician
    DINA mastery         (0.0 - 1.0)                     <- DINAModel
    wrong_models         (list of matched WM IDs)        <- match_wrong_model
    misconceptions       (free-text notes per turn)
    last_seen            (timestamp)
    turn_count           (int)

Edges are inherited from the Chapter-1 graph:
    prereq    (the concept needs this one first)
    leads_to  (this concept is a prerequisite of that one)
    parallel  (sibling construct, e.g. print / println)

The graph grows incrementally: after every student turn the pipeline calls
`update_from_diagnosis(diag, mastery)` to add or update the touched concept's
node, and `expand_neighbours()` to bring in its 1-hop Chapter-1 neighbours so
the teacher view can see what surrounds the concept being learned.

Concepts outside Chapter 1 (e.g. null_pointer) are kept as standalone nodes
under their own id, with no neighbours.

Persisted to SQLite via db_store.upsert_student_graph().
"""
from __future__ import annotations

import time
from dataclasses import dataclass, field, asdict, fields
from typing import Any, Dict, List, Optional, Set, Tuple

from .chapter1_graph import Chapter1Graph, get_chapter1_graph

LP_LEVELS = ("L0", "L1", "L2", "L3", "L4")


@dataclass
class GraphNode:
    """One concept the student has touched, grounded in the Chapter-1 graph. Carries every
    per-turn CPAL analysis (LP, mastery, WM, channel state, intervention,
    RL reward, probe, fact-check) so the student knowledge graph is the
    single source of truth the wireframe / teacher / parent views read from.
    """
    # Identity
    cpal_concept: str                     # CPAL-internal Java concept id
    concept_id: str                       # Chapter-1 concept id (or the raw id if outside Chapter 1)
    label: str = ""                       # short display label from the Chapter-1 graph
    chapter: str = ""                     # Chapter-1 chapter id ("" if outside Chapter 1)
    in_chapter1: bool = False
    # LPDiagnostician outputs
    lp_level: str = "L1"                  # current LP level (L0-L4)
    diagnostic_confidence: float = 0.0    # last diagnostic_confidence
    # DINA mastery
    mastery: float = 0.30                 # DINA probability of mastery
    mastery_delta: float = 0.0            # Δmastery this turn
    # Wrong-model catalogue
    wrong_models: List[str] = field(default_factory=list)
    wrong_models_refuted: List[str] = field(default_factory=list)
    misconception_notes: List[str] = field(default_factory=list)
    # Channel state (StudentStateTracker). The psychological/emotion
    # channel was removed; old payloads carrying it are ignored on load.
    cognitive: Dict[str, Any] = field(default_factory=dict)       # encoding_strength, dual_coding, ...
    progression: Dict[str, Any] = field(default_factory=dict)     # stage, zpd_position, scaffold_level
    # Intervention chosen by InterventionSelector
    intervention: Dict[str, Any] = field(default_factory=dict)    # {type, rationale, gate_triggered}
    # RL reward breakdown (RewardCalculator)
    reward: Dict[str, Any] = field(default_factory=dict)          # {total, breakdown: {learning_gain, engagement, ...}}
    # Heuristic post-correction flags (the 5 named heuristics in lp_diagnostic.py)
    heuristics: Dict[str, bool] = field(default_factory=lambda: {
        "substance_penalty":     False,
        "mech_vocab_bump":       False,
        "l2_rule_naming":        False,
        "parroting_downgrade":   False,
        "transfer_upgrade":      False,
    })
    # Probe-loop state
    probe_state: Dict[str, Any] = field(default_factory=lambda: {"count": 0, "cap": 8, "criteria": []})
    # Fact-check pass result
    fact_check: Dict[str, Any] = field(default_factory=lambda: {"passed": True, "stripped": 0})
    # Bookkeeping
    last_seen: float = field(default_factory=time.time)
    turn_count: int = 0
    lp_history: List[str] = field(default_factory=list)
    is_neighbour_only: bool = False       # True if pulled in as a graph neighbour but never directly engaged

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class GraphEdge:
    """Typed edge between two concepts (always Chapter-1-graph-derived)."""
    src: str            # concept id
    dst: str            # concept id
    rel: str            # 'prereq' | 'leads_to' | 'parallel'

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def key(self) -> Tuple[str, str, str]:
        return (self.src, self.dst, self.rel)


class StudentKnowledgeGraph:
    """Per-student graph that accumulates as the student interacts.

    Lifecycle:
        sg = StudentKnowledgeGraph(student_id="maya")
        diag = LPDiagnostician.diagnose(...)
        mastery = DINA.update(...).get("mastery_after")
        sg.update_from_diagnosis(diag, mastery)
        sg.expand_neighbours(diag.concept, depth=1)
        db_store.upsert_student_graph(student_id, sg.to_dict())
    """

    def __init__(self, student_id: str,
                 graph: Optional[Chapter1Graph] = None):
        self.student_id = student_id
        self.graph = graph or get_chapter1_graph()
        self.nodes: Dict[str, GraphNode] = {}     # keyed by concept_id
        self.edges: Set[Tuple[str, str, str]] = set()
        self.created_at = time.time()
        self.updated_at = self.created_at

    # ── Node management ────────────────────────────────────────────────────

    def _resolve(self, cpal_concept: str) -> str:
        """Map a CPAL concept id to its Chapter-1 concept id (or keep it as-is
        when the concept is outside Chapter 1)."""
        return self.graph.canonical(cpal_concept)

    def _new_node(self, concept_id: str, cpal_concept: str,
                  is_neighbour: bool) -> GraphNode:
        info = self.graph.concept_info(concept_id) or {}
        return GraphNode(
            cpal_concept=cpal_concept,
            concept_id=concept_id,
            label=info.get("label", concept_id),
            chapter=info.get("chapter", ""),
            in_chapter1=bool(info),
            is_neighbour_only=is_neighbour,
        )

    def get_or_create_node(self, cpal_concept: str,
                           is_neighbour: bool = False) -> GraphNode:
        cid = self._resolve(cpal_concept)
        if cid not in self.nodes:
            self.nodes[cid] = self._new_node(cid, cpal_concept, is_neighbour)
        return self.nodes[cid]

    def update_from_diagnosis(self, diag: Any,
                              mastery: Optional[float] = None,
                              misconception_text: str = "",
                              three_channel: Optional[Dict[str, Any]] = None,
                              intervention: Optional[Dict[str, Any]] = None,
                              reward: Optional[Dict[str, Any]] = None,
                              heuristics: Optional[Dict[str, bool]] = None,
                              probe_state: Optional[Dict[str, Any]] = None,
                              fact_check: Optional[Dict[str, Any]] = None,
                              mastery_before: Optional[float] = None
                              ) -> GraphNode:
        """Write the result of one diagnose() turn into the graph.

        `diag` is expected to be either an LPDiagnostic instance or a dict with
        keys: concept, current_lp_level, diagnostic_confidence, wrong_model_id.

        Optional kwargs let the caller attach every other CPAL per-turn analysis
        to this node so the student graph is the single source of truth for
        student_state_tracker, intervention selector, RL reward, heuristic flags,
        probe loop and fact-check.
        """
        if hasattr(diag, "to_dict"):
            d = diag.to_dict()
        elif isinstance(diag, dict):
            d = diag
        else:
            d = {}

        concept = d.get("concept") or d.get("cpal_concept") or "unknown"
        node = self.get_or_create_node(concept, is_neighbour=False)
        node.is_neighbour_only = False    # promote from neighbour to engaged
        node.lp_level = d.get("current_lp_level") or node.lp_level
        node.diagnostic_confidence = float(d.get("diagnostic_confidence") or node.diagnostic_confidence)
        node.lp_history.append(node.lp_level)
        node.turn_count += 1
        node.last_seen = time.time()
        if mastery is not None:
            prev = mastery_before if mastery_before is not None else node.mastery
            node.mastery = float(mastery)
            node.mastery_delta = round(node.mastery - float(prev), 4)
        # Wrong-model accounting
        wm = d.get("wrong_model_id")
        if wm and wm not in node.wrong_models:
            node.wrong_models.append(wm)
        # Refutation rule: once the student articulates the mechanism (L3+)
        # on a concept, ALL previously-matched WMs for that concept are
        # considered refuted.
        if node.lp_level in ("L3", "L4"):
            for past_wm in node.wrong_models:
                if past_wm not in node.wrong_models_refuted:
                    node.wrong_models_refuted.append(past_wm)
        if misconception_text:
            node.misconception_notes.append(misconception_text[:200])
        # Attach the rest of the CPAL per-turn analyses (each merged onto
        # the existing dict so partial updates are fine).
        if three_channel:
            node.cognitive.update(three_channel.get("cognitive") or {})
            node.progression.update(three_channel.get("progression") or {})
        if intervention:
            node.intervention = dict(intervention)
        if reward:
            node.reward = dict(reward)
        if heuristics:
            for k, v in heuristics.items():
                node.heuristics[k] = bool(v)
        if probe_state:
            node.probe_state = dict(probe_state)
        if fact_check:
            node.fact_check = dict(fact_check)
        self.updated_at = time.time()
        return node

    def expand_neighbours(self, cpal_concept: str, depth: int = 1) -> int:
        """Pull in the concept's Chapter-1 neighbours (prerequisites, the
        concepts it leads to, parallel constructs) as is_neighbour_only=True
        nodes. Returns the count of new nodes added.
        """
        center = self._resolve(cpal_concept)
        if not self.graph.exists(center):
            return 0
        added = 0
        neighbours = self.graph.get_neighbours(center)
        for rel, key in (("prereq", "prerequisites"),
                         ("leads_to", "leads_to"),
                         ("parallel", "parallel")):
            for n in neighbours[key][:5]:
                if n not in self.nodes:
                    self.nodes[n] = self._new_node(n, n, is_neighbour=True)
                    added += 1
                self.edges.add((center, n, rel))
        self.updated_at = time.time()
        return added

    # ── Queries used by teacher / parent / wireframe ─────────────────────

    def engaged_nodes(self) -> List[GraphNode]:
        """Concepts the student has directly worked on (not just neighbours)."""
        return [n for n in self.nodes.values() if not n.is_neighbour_only]

    def neighbour_nodes(self) -> List[GraphNode]:
        return [n for n in self.nodes.values() if n.is_neighbour_only]

    def active_wrong_models(self) -> List[Tuple[str, str]]:
        """All WMs currently NOT refuted, with their concept slug."""
        out = []
        for n in self.engaged_nodes():
            for wm in n.wrong_models:
                if wm not in n.wrong_models_refuted:
                    out.append((wm, n.concept_id))
        return out

    def average_mastery(self) -> float:
        engaged = self.engaged_nodes()
        if not engaged:
            return 0.0
        return sum(n.mastery for n in engaged) / len(engaged)

    def lp_distribution(self) -> Dict[str, int]:
        out = {lv: 0 for lv in LP_LEVELS}
        for n in self.engaged_nodes():
            if n.lp_level in out:
                out[n.lp_level] += 1
        return out

    def to_dict(self) -> Dict[str, Any]:
        """Full serialization for SQLite/JSON storage and frontend rendering."""
        return {
            "student_id":  self.student_id,
            "created_at":  self.created_at,
            "updated_at":  self.updated_at,
            "nodes":       [n.to_dict() for n in self.nodes.values()],
            "edges":       [{"src": s, "dst": d, "rel": r} for (s, d, r) in self.edges],
            "summary": {
                "engaged_count":    len(self.engaged_nodes()),
                "neighbour_count":  len(self.neighbour_nodes()),
                "avg_mastery":      round(self.average_mastery(), 3),
                "lp_distribution":  self.lp_distribution(),
                "active_wms":       self.active_wrong_models(),
            },
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any],
                  graph: Optional[Chapter1Graph] = None) -> "StudentKnowledgeGraph":
        sg = cls(student_id=d.get("student_id", "unknown"), graph=graph)
        known = {f.name for f in fields(GraphNode)}
        sg.created_at = d.get("created_at", time.time())
        sg.updated_at = d.get("updated_at", sg.created_at)
        for nd in d.get("nodes", []):
            nd = dict(nd)
            if "concept_id" not in nd:    # graphs saved before the CSO removal
                nd["concept_id"] = sg._resolve(nd.get("cpal_concept") or nd.get("cso_slug", "unknown"))
            node = GraphNode(**{k: v for k, v in nd.items() if k in known})
            sg.nodes[node.concept_id] = node
        for ed in d.get("edges", []):
            sg.edges.add((ed["src"], ed["dst"], ed["rel"]))
        return sg
