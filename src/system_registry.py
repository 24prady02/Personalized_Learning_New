"""
System registry — single-process singleton wiring every non-Nestor
component the CPAL stack exposes.

This mirrors api/server.py's startup_event so any front-end (the Gradio
chat app on port 7860, future REST/WebSocket apps, batch scripts) can
import one object and get the same fully-wired stack instead of
re-implementing the init dance.

Excluded by design (Nestor): NestorBayesianNetwork, NestorBayesianProfiler,
PersonalityProfiler, InterventionRecommender.

No emotion classifier and no psychological channel are registered:
emotion and psychological state are not used as inputs.

Mastery tracking (DINA, BKT), the teaching-action choice (TeachingRLAgent,
LPProgressionRanker, InterventionOrchestrator), hierarchical RL and the
dynamic KG updater were archived to _archive/mastery_and_teaching_choice/
on 2026-10-01. The stack now serves LP-level classification and the
student concept map.

Usage:
    from src.system_registry import get_registry
    reg = get_registry()             # idempotent, cached after first call
    diag = reg.lp_diagnostician.diagnose(student_id, concept, text)
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
    """Container for every CPAL component the chat app needs.

    History (2026-05-25): LPProgressionRanker was previously dormant;
    re-enabled this revision so the runtime stack matches the
    methodology described in the paper. Nestor remains out of scope
    (see scripts/cpal_chat_app.py header note). Components that fail
    to load no-op gracefully (the _try wrapper records the failure and
    callers handle None)."""
    config: Dict[str, Any] = field(default_factory=dict)

    # Encoder + behavioral
    hvsae: Any = None
    behavioral_rnn: Any = None
    behavioral_hmm: Any = None

    # Knowledge graph (Chapter-1 concept + LP graph)
    chapter1_graph: Any = None

    # Content generation
    content_generator: Any = None       # HVSAE-backed decoder
    enhanced_generator: Any = None      # Ollama-backed enhanced gen


    # Catalogue + diagnostician
    catalogue: Any = None
    lp_diagnostician: Any = None

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
    print("[Registry] Building CPAL stack (LP classification + concept map)...")

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

    # ── Knowledge graph ──────────────────────────────────────────────────
    # The Chapter-1 concept + LP graph (data/chapter1_kg.json).
    # CSE-KG, Pedagogical KG and COKE were retired to _archive/.
    from src.knowledge_graph.chapter1_graph import get_chapter1_graph

    reg.chapter1_graph = _try(reg, "chapter1_graph", lambda: get_chapter1_graph())

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
