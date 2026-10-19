"""
lp_percpt — LP-level classification on the Chapter-1 knowledge graph (data/chapter1_kg.json).

Per student prompt: link the prompt to concept nodes, collect E1-E4 evidence
from the graph's own statements and edges, walk each concept's L0-L4 ladder
along its next_level edges, apply the gates, and update the student's
self-updating graph with inference rules. No model is trained.

Algorithm: docs/CPAL_LP_Classification_Algorithm.xlsx.
Entry point: src.lp_percpt.engine.get_engine().process(student_id, text, ...).
"""
from .engine import LPPercptEngine, get_engine

__all__ = ["LPPercptEngine", "get_engine"]
