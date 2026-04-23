"""
CSE-KG 2.0 Integration Module
Computer Science Knowledge Graph for domain knowledge
"""

from .cse_kg_client import CSEKGClient
from .graph_fusion import GraphFusion
from .query_engine import QueryEngine, ConceptRetriever
from .pedagogical_kg_builder import PedagogicalKGBuilder
from .pedagogical_kg_schema import (
    PedagogicalKGSchema,
    Misconception,
    LearningProgression,
    CognitiveLoad,
    Intervention,
    ConceptPedagogicalData
)
from .pedagogical_kg_integration import PedagogicalKGIntegration
from .coke_cognitive_graph import COKECognitiveGraph, CognitiveState, BehavioralResponse

try:
    from .gikt_knowledge_tracing import GIKTModel, GIKTKnowledgeTracer
except ImportError:
    GIKTModel, GIKTKnowledgeTracer = None, None  # torch_geometric not installed

try:
    from .coke_gikt_integration import COKEGIKTIntegration
except ImportError:
    COKEGIKTIntegration = None  # torch_geometric not installed

from .error_explanation_mapper import ErrorExplanationMapper, ErrorType, RootCauseType
from .unified_explanation_generator import UnifiedExplanationGenerator
from .adaptive_explanation_generator import AdaptiveExplanationGenerator

__all__ = [
    "CSEKGClient",
    "GraphFusion",
    "QueryEngine",
    "ConceptRetriever",
    "PedagogicalKGBuilder",
    "PedagogicalKGSchema",
    "Misconception",
    "LearningProgression",
    "CognitiveLoad",
    "Intervention",
    "ConceptPedagogicalData",
    "PedagogicalKGIntegration",
    "COKECognitiveGraph",
    "CognitiveState",
    "BehavioralResponse",
    "GIKTModel",
    "GIKTKnowledgeTracer",
    "COKEGIKTIntegration",
    "ErrorExplanationMapper",
    "ErrorType",
    "RootCauseType",
    "UnifiedExplanationGenerator",
    "AdaptiveExplanationGenerator",
]
