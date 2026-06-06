"""
student_knowledge_graph.py — per-student knowledge graph grounded in CSO v3.5.

This is the central data structure CPAL now revolves around. Each student's
graph is a subgraph of CSO v3.5 limited to the concepts that student has
touched. Each node carries everything CPAL has inferred about that student's
relationship to that concept:

    LP level             (L1 / L2 / L3 / L4)            ← LPDiagnostician
    diagnostic_confidence (0.0 - 1.0)                    ← LPDiagnostician
    DINA mastery         (0.0 - 1.0)                     ← DINAModel
    wrong_models         (list of matched WM IDs)        ← match_wrong_model
    misconceptions       (free-text notes per turn)
    last_seen            (timestamp)
    turn_count           (int)

Edges are inherited from CSO:
    prereq    (CSO superTopicOf / contributedBy)
    related   (CSO relatedEquivalent)
    sub_topic (CSO inverse superTopicOf)

The graph grows incrementally — every time the student submits text, the
pipeline calls `update_from_diagnosis(diag, dina_mastery)` to add or update
the touched concept's node, and `expand_neighbours()` to bring in 1-hop CSO
neighbours so the teacher / parent view can see what's connected to what
the student is currently learning.

Persisted to SQLite via db_store.upsert_student_graph().
"""
from __future__ import annotations

import json
import time
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional, Set, Tuple

from .cso_traversal import get_cso, CSOTraversal


# Map CPAL's internal Java concept IDs to CSO slugs so the student graph is
# anchored in the ontology. (CPAL concepts are coarse; CSO equivalents may
# be either broader or narrower — pick whichever maps cleanly.)
# CPAL concept -> CSO slug. All targets verified to exist in CSO v3.5
# (the slugs that didn't exist were replaced by their nearest broader topic
# that does).
CPAL_TO_CSO = {
    "type_mismatch":          "computer_programming_languages",
    "infinite_loop":          "computer_programming",
    "null_pointer":           "computer_programming",
    "string_equality":        "string_matching",
    "variable_scope":         "computer_programming_languages",
    "assignment_vs_compare":  "computer_programming_languages",
    "integer_division":       "computer_arithmetic",
    "scanner_buffer":         "user_interfaces",
    "array_index":            "computer_programming",
    "missing_return":         "computer_programming_languages",
    "array_not_allocated":    "memory_management",
    "boolean_operators":      "computer_programming_languages",
    "sentinel_loop":          "computer_programming",
    "unreachable_code":       "computer_programming",
    "string_immutability":    "object_oriented_programming",
    "no_default_constructor": "object_oriented_programming",
    "static_vs_instance":     "object_oriented_programming",
    "foreach_no_modify":      "computer_programming",
    "overloading":            "object_oriented_programming",
    "generics_primitives":    "computer_programming_languages",
    # Chapter 1.1 (Princeton §1.1 Hello World) specific
    "hello_world":            "computer_programming",
    "command_line_args":      "user_interfaces",
    "main_method":            "object_oriented_programming",
    "println":                "user_interfaces",
    "compile_vs_runtime":     "compilers",
    "syntax_errors":          "compilers",
}

# Fallback used when neither CPAL_TO_CSO nor the raw concept name resolves
# to a CSO node — anchors orphan concepts at the broad CS-programming level
# so the student graph still grows instead of stalling.
_FALLBACK_CSO_SLUG = "computer_programming"


@dataclass
class GraphNode:
    """One concept the student has touched, grounded in CSO. Carries every
    per-turn CPAL analysis (LP, mastery, WM, 3-channel state, intervention,
    RL reward, probe, fact-check) so the student knowledge graph is the
    single source of truth the wireframe / teacher / parent views read from.
    """
    # Identity
    cpal_concept: str                     # CPAL-internal Java concept id
    cso_slug: str                         # canonical CSO topic slug
    # LPDiagnostician outputs
    lp_level: str = "L1"                  # current LP level (L1-L4)
    diagnostic_confidence: float = 0.0    # last diagnostic_confidence
    # DINA mastery
    mastery: float = 0.30                 # DINA probability of mastery
    mastery_delta: float = 0.0            # Δmastery this turn
    # Wrong-model catalogue
    wrong_models: List[str] = field(default_factory=list)
    wrong_models_refuted: List[str] = field(default_factory=list)
    misconception_notes: List[str] = field(default_factory=list)
    # Three-channel state (StudentStateTracker)
    cognitive: Dict[str, Any] = field(default_factory=dict)       # encoding_strength, dual_coding, ...
    progression: Dict[str, Any] = field(default_factory=dict)     # stage, zpd_position, scaffold_level
    psychological: Dict[str, Any] = field(default_factory=dict)   # attribution, imposter, anxiety, efficacy
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
    is_neighbour_only: bool = False       # True if pulled in via CSO traversal but never directly engaged

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class GraphEdge:
    """Typed edge between two concepts (always CSO-derived)."""
    src: str            # CSO slug
    dst: str            # CSO slug
    rel: str            # 'prereq' | 'related' | 'sub_topic' | 'contributes_to'

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
                 cso: Optional[CSOTraversal] = None):
        self.student_id = student_id
        self.cso = cso or get_cso()
        self.nodes: Dict[str, GraphNode] = {}     # keyed by CSO slug
        self.edges: Set[Tuple[str, str, str]] = set()
        self.created_at = time.time()
        self.updated_at = self.created_at

    # ── Node management ────────────────────────────────────────────────────

    def _resolve_slug(self, cpal_concept: str) -> str:
        """Map CPAL concept -> CSO slug, with three fallbacks:
            1. explicit CPAL_TO_CSO mapping
            2. the raw concept name (if it happens to exist in CSO)
            3. a broad CS-programming anchor so the graph still grows
        Then run CSO's canonical() to follow any aliases.
        """
        slug = CPAL_TO_CSO.get(cpal_concept, cpal_concept)
        if not self.cso.exists(slug):
            slug = _FALLBACK_CSO_SLUG
        return self.cso.canonical(slug)

    def get_or_create_node(self, cpal_concept: str,
                           is_neighbour: bool = False) -> GraphNode:
        slug = self._resolve_slug(cpal_concept)
        if slug not in self.nodes:
            self.nodes[slug] = GraphNode(
                cpal_concept=cpal_concept,
                cso_slug=slug,
                is_neighbour_only=is_neighbour,
            )
        return self.nodes[slug]

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
            node.psychological.update(three_channel.get("psychological") or {})
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
        """Pull in CSO neighbours of the touched concept so the graph shows
        related areas the student hasn't yet engaged with. Added as
        is_neighbour_only=True nodes. Returns count of new nodes added.
        """
        center = self._resolve_slug(cpal_concept)
        if not self.cso.exists(center):
            return 0
        added = 0
        neighbours = self.cso.get_neighbours(center)

        def _add_edge(src: str, dst: str, rel: str) -> None:
            self.edges.add((src, dst, rel))

        # parents -> prereq edges
        for p in neighbours["parents"][:5]:
            if p not in self.nodes:
                self.nodes[p] = GraphNode(cpal_concept=p, cso_slug=p, is_neighbour_only=True)
                added += 1
            _add_edge(center, p, "prereq")
        # children -> sub_topic edges
        for c in neighbours["children"][:5]:
            if c not in self.nodes:
                self.nodes[c] = GraphNode(cpal_concept=c, cso_slug=c, is_neighbour_only=True)
                added += 1
            _add_edge(center, c, "sub_topic")
        # related -> related edges
        for r in neighbours["related"][:5]:
            if r not in self.nodes:
                self.nodes[r] = GraphNode(cpal_concept=r, cso_slug=r, is_neighbour_only=True)
                added += 1
            _add_edge(center, r, "related")
        # contributes_to -> prereq (the targets of contribution help with this)
        for t in neighbours["contributes_to"][:5]:
            if t not in self.nodes:
                self.nodes[t] = GraphNode(cpal_concept=t, cso_slug=t, is_neighbour_only=True)
                added += 1
            _add_edge(center, t, "contributes_to")
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
                    out.append((wm, n.cso_slug))
        return out

    def average_mastery(self) -> float:
        engaged = self.engaged_nodes()
        if not engaged:
            return 0.0
        return sum(n.mastery for n in engaged) / len(engaged)

    def lp_distribution(self) -> Dict[str, int]:
        out = {"L1": 0, "L2": 0, "L3": 0, "L4": 0}
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
                  cso: Optional[CSOTraversal] = None) -> "StudentKnowledgeGraph":
        sg = cls(student_id=d.get("student_id", "unknown"), cso=cso)
        sg.created_at = d.get("created_at", time.time())
        sg.updated_at = d.get("updated_at", sg.created_at)
        for nd in d.get("nodes", []):
            node = GraphNode(**nd)
            sg.nodes[node.cso_slug] = node
        for ed in d.get("edges", []):
            sg.edges.add((ed["src"], ed["dst"], ed["rel"]))
        return sg
