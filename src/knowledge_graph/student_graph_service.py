"""
student_graph_service.py — orchestrates per-student-graph updates after each
diagnose() turn. Single entry-point that callers (chat app, student app, tests)
use to keep CPAL's central data structure in sync.

Usage (from cpal_chat_app or api/student_app):

    from src.knowledge_graph.student_graph_service import StudentGraphService
    svc = StudentGraphService.shared()

    # After running LPDiagnostician.diagnose(...) and DINA.update(...):
    sg = svc.record_turn(
        student_id  = "maya",
        diag        = diag_object,        # LPDiagnostic
        mastery     = mastery_after,      # float from DINA
        misconception_text = student_reply,
        expand_cso  = True,               # bring in CSO neighbours
    )
    payload = sg.to_dict()                # for SQLite + frontend
"""
from __future__ import annotations

from typing import Any, Dict, Optional

from .student_knowledge_graph import StudentKnowledgeGraph
from .cso_traversal import get_cso

_INSTANCE: Optional["StudentGraphService"] = None


class StudentGraphService:
    """Manages the in-memory cache of student knowledge graphs and persistence.

    In-memory cache is keyed by student_id. On first access we try to load
    from SQLite (db_store.get_student_graph); on each write we upsert back.
    Both ends soft-fail so the service still works without the DB layer.
    """

    def __init__(self) -> None:
        self._cache: Dict[str, StudentKnowledgeGraph] = {}
        self._cso = get_cso()

    @classmethod
    def shared(cls) -> "StudentGraphService":
        global _INSTANCE
        if _INSTANCE is None:
            _INSTANCE = cls()
        return _INSTANCE

    # ── DB helpers (soft-fail if persistence layer absent) ────────────────

    def _try_load_from_db(self, student_id: str) -> Optional[StudentKnowledgeGraph]:
        try:
            from src.persistence.db_store import get_db
            payload = get_db().get_student_graph(student_id)
            if payload:
                return StudentKnowledgeGraph.from_dict(payload, cso=self._cso)
        except Exception:
            pass
        return None

    def _try_save_to_db(self, sg: StudentKnowledgeGraph) -> None:
        try:
            from src.persistence.db_store import get_db
            get_db().upsert_student_graph(sg.student_id, sg.to_dict())
        except Exception:
            pass

    # ── Public API ────────────────────────────────────────────────────────

    def get(self, student_id: str) -> StudentKnowledgeGraph:
        """Return (and lazily load) the graph for a student."""
        if student_id not in self._cache:
            loaded = self._try_load_from_db(student_id)
            if loaded is None:
                loaded = StudentKnowledgeGraph(student_id=student_id, cso=self._cso)
            self._cache[student_id] = loaded
        return self._cache[student_id]

    def record_turn(self, student_id: str,
                    diag: Any,
                    mastery: Optional[float] = None,
                    misconception_text: str = "",
                    three_channel: Optional[Dict[str, Any]] = None,
                    intervention: Optional[Dict[str, Any]] = None,
                    reward: Optional[Dict[str, Any]] = None,
                    heuristics: Optional[Dict[str, bool]] = None,
                    probe_state: Optional[Dict[str, Any]] = None,
                    fact_check: Optional[Dict[str, Any]] = None,
                    mastery_before: Optional[float] = None,
                    expand_cso: bool = True,
                    persist: bool = True) -> StudentKnowledgeGraph:
        """Single call to update the student graph from one diagnose() turn.

        Pipeline:
          1. Fetch / lazy-create the student graph.
          2. Update the touched node with diagnosis + ALL per-turn analyses
             (three-channel state, intervention, RL reward, heuristic flags,
             probe state, fact-check) so the graph is the single source of
             truth for the wireframe / teacher / parent views.
          3. (Optional) Expand 1-hop CSO neighbours.
          4. (Optional) Persist the snapshot to SQLite.

        Returns the in-memory graph for the caller to render / serialize.
        """
        sg = self.get(student_id)
        node = sg.update_from_diagnosis(
            diag, mastery=mastery,
            misconception_text=misconception_text,
            three_channel=three_channel,
            intervention=intervention,
            reward=reward,
            heuristics=heuristics,
            probe_state=probe_state,
            fact_check=fact_check,
            mastery_before=mastery_before,
        )
        if expand_cso:
            sg.expand_neighbours(node.cpal_concept, depth=1)
        if persist:
            self._try_save_to_db(sg)
        return sg

    def render_payload(self, student_id: str) -> Dict[str, Any]:
        """Convenience: return the to_dict() of a student's graph for the UI."""
        return self.get(student_id).to_dict()
