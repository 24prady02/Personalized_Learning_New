"""
System registry — single-process singleton wiring every non-Nestor
component the CPAL stack exposes.

This mirrors api/server.py's startup_event so any front-end (the Gradio
chat app on port 7860, future REST/WebSocket apps, batch scripts) can
import one object and get the same fully-wired stack instead of
re-implementing the init dance.

Excluded by design (Nestor): NestorBayesianNetwork, NestorBayesianProfiler,
PersonalityProfiler, InterventionRecommender. The orchestrator's
psychological-assessment paths gracefully no-op when these are absent
(see orchestrator.py:_assess_psychological_state — returns
{personality: {}, learning_style: {}, source: 'none'} when both are
missing) so the rest of the pipeline runs untouched.

Usage:
    from src.system_registry import get_registry
    reg = get_registry()             # idempotent, cached after first call
    intervention = reg.orchestrator.process_session(session_data)
    reg.dina.update(student_id, skill, is_correct)
    mastery = reg.dina.get_mastery(student_id, skill)
"""
from __future__ import annotations

import os
import sys
from dataclasses import dataclass, field
from pathlib import Path
from threading import Lock
from typing import Any, Dict, Optional

import yaml

ROOT = Path(__file__).resolve().parent.parent


@dataclass
class SystemRegistry:
    """Container for every non-Nestor component the chat app needs."""
    config: Dict[str, Any] = field(default_factory=dict)

    # Encoder + behavioral
    hvsae: Any = None
    behavioral_rnn: Any = None
    behavioral_hmm: Any = None

    # Cognitive student modeling
    dina: Any = None
    bkt: Any = None  # BayesianKnowledgeTracer

    # Knowledge graphs
    cse_kg_client: Any = None
    concept_retriever: Any = None
    query_engine: Any = None
    pedagogical_kg: Any = None
    coke_graph: Any = None
    graph_fusion: Any = None

    # Explanation generators (KG-grounded)
    unified_explanation_generator: Any = None
    adaptive_explainer: Any = None
    error_explanation_mapper: Any = None

    # Content generation
    content_generator: Any = None       # HVSAE-backed decoder
    enhanced_generator: Any = None      # Ollama-backed enhanced gen

    # Reinforcement learning
    teaching_rl_agent: Any = None
    hierarchical_rl: Any = None
    dynamic_kg_updater: Any = None

    # Catalogue + diagnostician + orchestrator
    catalogue: Any = None
    lp_diagnostician: Any = None
    orchestrator: Any = None

    # Per-component init status — diagnostic only
    status: Dict[str, str] = field(default_factory=dict)


_REGISTRY: Optional[SystemRegistry] = None
_REGISTRY_LOCK = Lock()


def _load_config() -> Dict[str, Any]:
    cfg_path = ROOT / "configs" / "config.yaml"
    with open(cfg_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def _try(reg: SystemRegistry, name: str, fn):
    """Run a constructor; record success/failure but keep going so one
    bad component doesn't kill the whole stack. The chat app then falls
    back gracefully wherever the missing component is consulted."""
    try:
        result = fn()
        reg.status[name] = "ok"
        return result
    except Exception as e:
        reg.status[name] = f"failed: {type(e).__name__}: {e}"
        print(f"[Registry] {name} init failed: {e}")
        return None


def _build_registry() -> SystemRegistry:
    import torch

    reg = SystemRegistry()
    reg.config = _load_config()
    cfg = reg.config
    print("[Registry] Building full CPAL stack (Nestor excluded)...")

    # ── HVSAE + behavioral ────────────────────────────────────────────────
    from src.models.hvsae import HVSAE
    from src.models.behavioral import BehavioralRNN, BehavioralHMM

    reg.hvsae = _try(reg, "hvsae", lambda: HVSAE(cfg))
    reg.behavioral_rnn = _try(reg, "behavioral_rnn",
                              lambda: BehavioralRNN(cfg))
    reg.behavioral_hmm = _try(reg, "behavioral_hmm",
                              lambda: BehavioralHMM(cfg))

    ckpt_path = ROOT / "checkpoints" / "best.pt"
    if ckpt_path.exists():
        try:
            ck = torch.load(ckpt_path, map_location="cpu",
                            weights_only=False)
            if reg.hvsae is not None and "hvsae_state" in ck:
                reg.hvsae.load_state_dict(ck["hvsae_state"])
                reg.hvsae.eval()
            if (reg.behavioral_rnn is not None
                    and "behavioral_rnn_state" in ck):
                reg.behavioral_rnn.load_state_dict(ck["behavioral_rnn_state"])
                reg.behavioral_rnn.eval()
            reg.status["best.pt"] = "loaded"
            print("[Registry] Loaded checkpoints/best.pt (HVSAE+RNN)")
        except Exception as e:
            reg.status["best.pt"] = f"failed: {e}"
            print(f"[Registry] best.pt load failed: {e}")
    else:
        reg.status["best.pt"] = "missing"

    # ── Cognitive student models ──────────────────────────────────────────
    from src.models.dina import DINAModel
    from src.student_modeling.bayesian_knowledge_tracing import (
        BayesianKnowledgeTracer,
    )
    # DINA writes/reads data/dina/dina_params.json — create the dir so
    # first-touch updates don't silently lose state.
    (ROOT / cfg.get("dina", {}).get("data_dir", "data/dina")).mkdir(
        parents=True, exist_ok=True)
    reg.dina = _try(reg, "dina", lambda: DINAModel(cfg))
    reg.bkt = _try(reg, "bkt", lambda: BayesianKnowledgeTracer())

    # ── Knowledge graphs ─────────────────────────────────────────────────
    from src.knowledge_graph.cse_kg_client import CSEKGClient
    from src.knowledge_graph.query_engine import QueryEngine, ConceptRetriever
    from src.knowledge_graph.pedagogical_kg_integration import (
        PedagogicalKGIntegration,
    )
    from src.knowledge_graph.coke_cognitive_graph import COKECognitiveGraph
    from src.knowledge_graph.graph_fusion import GraphFusion
    from src.knowledge_graph.adaptive_explanation_generator import (
        AdaptiveExplanationGenerator,
    )
    from src.knowledge_graph.unified_explanation_generator import (
        UnifiedExplanationGenerator,
    )
    from src.knowledge_graph.error_explanation_mapper import (
        ErrorExplanationMapper,
    )

    reg.cse_kg_client = _try(reg, "cse_kg_client",
                              lambda: CSEKGClient(cfg))
    if reg.cse_kg_client is not None:
        reg.query_engine = _try(reg, "query_engine",
                                 lambda: QueryEngine(reg.cse_kg_client))
        reg.concept_retriever = _try(reg, "concept_retriever",
                                      lambda: ConceptRetriever(reg.cse_kg_client))

    reg.pedagogical_kg = _try(reg, "pedagogical_kg",
                               lambda: PedagogicalKGIntegration(cfg))
    coke_cfg = cfg.get("coke", {"enabled": True,
                                 "data_dir": "data/pedagogical_kg"})
    # COKECognitiveGraph reads pedagogical_kg.data_dir for coke_chains.json
    # but has hardcoded defaults if the file is missing — safe to init either way.
    reg.coke_graph = _try(reg, "coke_graph",
                           lambda: COKECognitiveGraph(coke_cfg))
    reg.graph_fusion = _try(reg, "graph_fusion",
                             lambda: GraphFusion(cfg))

    if reg.pedagogical_kg is not None:
        reg.unified_explanation_generator = _try(
            reg, "unified_explanation_generator",
            lambda: UnifiedExplanationGenerator(
                cfg,
                pedagogical_builder=reg.pedagogical_kg.pedagogical_builder,
                coke_graph=reg.coke_graph,
            ),
        )
    reg.adaptive_explainer = _try(reg, "adaptive_explainer",
                                   lambda: AdaptiveExplanationGenerator(cfg))
    reg.error_explanation_mapper = _try(
        reg, "error_explanation_mapper",
        lambda: ErrorExplanationMapper(
            cfg,
            pedagogical_builder=getattr(reg.pedagogical_kg,
                                         "pedagogical_builder", None),
            coke_graph=reg.coke_graph,
        ),
    )

    # ── Content generation ───────────────────────────────────────────────
    from src.orchestrator.content_generator import PersonalizedContentGenerator
    from src.orchestrator.enhanced_personalized_generator import (
        EnhancedPersonalizedGenerator,
    )
    if reg.hvsae is not None:
        reg.content_generator = _try(
            reg, "content_generator",
            lambda: PersonalizedContentGenerator(cfg, reg.hvsae),
        )
    reg.enhanced_generator = _try(reg, "enhanced_generator",
                                   lambda: EnhancedPersonalizedGenerator())

    # ── Catalogue + diagnostician ────────────────────────────────────────
    from src.knowledge_graph.mental_models import get_catalogue
    from src.orchestrator.lp_diagnostic import LPDiagnostician

    reg.catalogue = _try(reg, "catalogue", lambda: get_catalogue())
    reg.lp_diagnostician = _try(
        reg, "lp_diagnostician",
        lambda: LPDiagnostician(catalogue=reg.catalogue,
                                 hvsae_model=reg.hvsae,
                                 enable_rubric_grader=True,
                                 enable_catalogue_rag=True),
    )

    # ── Reinforcement learning ───────────────────────────────────────────
    # Models dict mirrors what server.py passes to the orchestrator and RL
    # agents — minus Nestor's nestor_profiler/personality_profiler/
    # intervention_recommender. The orchestrator already handles their
    # absence (.get() returns None and the psych-assessment path no-ops).
    models = {
        "hvsae":                          reg.hvsae,
        "behavioral_rnn":                 reg.behavioral_rnn,
        "behavioral_hmm":                 reg.behavioral_hmm,
        "dina":                           reg.dina,
        "bkt":                            reg.bkt,
        "cse_kg_client":                  reg.cse_kg_client,
        "concept_retriever":              reg.concept_retriever,
        "query_engine":                   reg.query_engine,
        "pedagogical_kg":                 reg.pedagogical_kg,
        "coke_graph":                     reg.coke_graph,
        "graph_fusion":                   reg.graph_fusion,
        "unified_explanation_generator":  reg.unified_explanation_generator,
        "adaptive_explainer":             reg.adaptive_explainer,
        "error_explanation_mapper":       reg.error_explanation_mapper,
        "content_generator":              reg.content_generator,
        "enhanced_generator":             reg.enhanced_generator,
        "catalogue":                      reg.catalogue,
        "lp_diagnostician":               reg.lp_diagnostician,
    }

    from src.reinforcement_learning.teaching_agent import TeachingRLAgent
    from src.reinforcement_learning.hierarchical_multi_task_rl import (
        HierarchicalMultiTaskRL,
    )
    from src.reinforcement_learning.knowledge_graph_updater import (
        DynamicKGUpdater,
    )

    reg.teaching_rl_agent = _try(reg, "teaching_rl_agent",
                                  lambda: TeachingRLAgent(cfg, models))
    reg.hierarchical_rl = _try(reg, "hierarchical_rl",
                                lambda: HierarchicalMultiTaskRL(cfg))
    reg.dynamic_kg_updater = _try(reg, "dynamic_kg_updater",
                                   lambda: DynamicKGUpdater(cfg, models))

    models["teaching_rl_agent"] = reg.teaching_rl_agent
    models["hierarchical_rl"]   = reg.hierarchical_rl

    # ── Orchestrator (last — depends on everything above) ────────────────
    from src.orchestrator.orchestrator import InterventionOrchestrator
    reg.orchestrator = _try(
        reg, "orchestrator",
        lambda: InterventionOrchestrator(
            cfg, models, use_rl=True, use_hierarchical_rl=False),
    )

    # ── Summary ──────────────────────────────────────────────────────────
    ok    = sum(1 for v in reg.status.values()
                 if v == "ok" or v == "loaded")
    fail  = sum(1 for v in reg.status.values() if v.startswith("failed"))
    miss  = sum(1 for v in reg.status.values() if v == "missing")
    print(f"[Registry] Ready. components: {ok} ok, {fail} failed, "
          f"{miss} missing-checkpoint")
    if fail:
        print("[Registry] Failed components:")
        for k, v in reg.status.items():
            if v.startswith("failed"):
                print(f"  - {k}: {v}")
    return reg


def get_registry() -> SystemRegistry:
    """Return the singleton registry, building it on first call.
    Thread-safe; safe to call from Gradio handlers."""
    global _REGISTRY
    if _REGISTRY is not None:
        return _REGISTRY
    with _REGISTRY_LOCK:
        if _REGISTRY is None:
            _REGISTRY = _build_registry()
    return _REGISTRY
