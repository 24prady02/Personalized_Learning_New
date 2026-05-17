"""
CPAL chat interface (quiz-first) — Gradio app wrapping the full diagnosis +
grounded-response pipeline.

Flow:
  1. Pick a quiz from the bank (or enter a custom one)
  2. See the question + code + multiple-choice options
  3. Select the option you'd pick
  4. Write your reasoning for that pick
  5. Submit → diagnosis panel fills in (LP + wrong-model distributions),
     tutor response streams in the chat below

Run:
    python scripts/cpal_chat_app.py                   # localhost:7860
    python scripts/cpal_chat_app.py --share           # public gradio.live
    python scripts/cpal_chat_app.py --port 8080       # custom port
"""
import os, re, sys, argparse
from pathlib import Path
from threading import Lock
from typing import Optional
import torch

ROOT = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, str(ROOT))

import gradio as gr

from src.models.hvsae import HVSAE
from src.knowledge_graph.mental_models import get_catalogue
from src.orchestrator.lp_diagnostic import (
    LPDiagnostician, filter_interventions_by_lp, LP_INDEX, LP_ORDER,
)
from src.orchestrator.enhanced_personalized_generator import (
    EnhancedPersonalizedGenerator,
)


# =========================================================================
# Quiz bank
# =========================================================================
QUIZZES = [
    {
        "id": "SE-1",
        "concept": "string_equality",
        "question": "What does this print?",
        "code": (
            'String a = new String("hello");\n'
            'String b = new String("hello");\n'
            'System.out.println(a == b);'
        ),
        "options": {
            "A": "true — both strings contain 'hello'",
            "B": "false — they are different objects",
            "C": "Compile error",
            "D": "The word 'hello' prints twice",
        },
        "correct_answer": "B",
    },
    {
        "id": "ID-1",
        "concept": "integer_division",
        "question": "What does this print?",
        "code": (
            'double result = 5 / 2;\n'
            'System.out.println(result);'
        ),
        "options": {
            "A": "2.5",
            "B": "2.0",
            "C": "2",
            "D": "Compile error — mismatched types",
        },
        "correct_answer": "B",
    },
    {
        "id": "NP-1",
        "concept": "null_pointer",
        "question": "What happens at runtime when this is called?",
        "code": (
            'public class Widget {\n'
            '    private String label;\n'
            '    public String describe() {\n'
            '        return label.toUpperCase();\n'
            '    }\n'
            '}\n'
            '// elsewhere:\n'
            'Widget w = new Widget();\n'
            'System.out.println(w.describe());'
        ),
        "options": {
            "A": "Prints empty string",
            "B": 'Prints "LABEL" (the field name, uppercased)',
            "C": "Throws NullPointerException",
            "D": "Compile error — label not initialized",
        },
        "correct_answer": "C",
    },
    {
        "id": "AI-1",
        "concept": "array_index",
        "question": "What does this print?",
        "code": (
            'int[] arr = {10, 20, 30, 40, 50};\n'
            'System.out.println(arr[5]);'
        ),
        "options": {
            "A": "50 (the fifth element)",
            "B": "10 (the first element)",
            "C": "0 (default int)",
            "D": "ArrayIndexOutOfBoundsException",
        },
        "correct_answer": "D",
    },
    {
        "id": "VS-1",
        "concept": "variable_scope",
        "question": "What happens here?",
        "code": (
            'for (int i = 0; i < 3; i++) {\n'
            '    int total = i * 10;\n'
            '}\n'
            'System.out.println(total);'
        ),
        "options": {
            "A": "Prints 20 (last value of total)",
            "B": "Prints 0 (initial value)",
            "C": "Compile error",
            "D": "Prints 30",
        },
        "correct_answer": "C",
    },
    {
        "id": "BO-1",
        "concept": "boolean_operators",
        "question": "What does this print when score = 200?",
        "code": (
            'int score = 200;\n'
            'if (score >= 0 || score <= 100) {\n'
            '    System.out.println("Valid");\n'
            '} else {\n'
            '    System.out.println("Out of range");\n'
            '}'
        ),
        "options": {
            "A": "Valid",
            "B": "Out of range",
            "C": "Nothing — compile error",
            "D": "Valid, then Out of range",
        },
        "correct_answer": "A",
    },
    {
        "id": "IL-1",
        "concept": "infinite_loop",
        "question": "What happens when this runs?",
        "code": (
            'int i = 0;\n'
            'while (i < 10) {\n'
            '    System.out.println("value: " + i);\n'
            '}'
        ),
        "options": {
            "A": "Prints 'value: 0' through 'value: 9' and stops",
            "B": "Prints 'value: 0' forever",
            "C": "Prints nothing",
            "D": "Compile error",
        },
        "correct_answer": "B",
    },
]
QUIZ_BY_ID = {q["id"]: q for q in QUIZZES}
QUIZ_CHOICES = [(f"{q['id']} — {q['concept']} — {q['question'][:48]}", q["id"])
                for q in QUIZZES]


# =========================================================================
# Load models once — via the system registry so DINA, BKT, behavioral,
# CSE-KG, pedagogical KG, CoKE, graph fusion, RL teaching agent,
# hierarchical RL, dynamic KG updater, error mapper, and the orchestrator
# all fire alongside the LP diagnostician. Nestor is intentionally
# excluded (per scope).
# =========================================================================
print("Loading full CPAL stack via system_registry...")
from src.system_registry import get_registry
REG = get_registry()
# Module-level handles preserve the rest of this file's existing references
# (HVSAE_MODEL, CATALOGUE, DX, GEN) without rewriting every call site.
HVSAE_MODEL = REG.hvsae
CATALOGUE   = REG.catalogue
DX          = REG.lp_diagnostician
GEN         = REG.enhanced_generator
try:
    from transformers import AutoTokenizer
    TOKENIZER = AutoTokenizer.from_pretrained("bert-base-uncased")
except Exception:
    TOKENIZER = None
_GEN_LOCK = Lock()
print("Ready.")


# =========================================================================
# Registry-component glue
# -------------------------------------------------------------------------
# These helpers thread the chat app through every non-Nestor CPAL component
# so each turn:
#   - DINA and BKT update real per-student mastery and write to disk
#   - Pedagogical KG and CSE-KG retrieval supplies KG-grounded context
#     that gets injected into the LLM prompt
#   - ErrorExplanationMapper resolves code/error symptoms to root causes
#   - TeachingRLAgent picks an intervention type from the learned policy
#   - DynamicKGUpdater learns prerequisite + misconception patterns from
#     observed (concept, correct/incorrect) interactions
# All calls are wrapped in try/except so a missing/dead component never
# breaks the chat — it just silently drops that enrichment for the turn.
# =========================================================================

def _update_mastery(student_id: str, concept: str, is_correct: bool) -> dict:
    """Update DINA + BKT and return the post-update mastery dict so the
    LLM prompt can be shaped by REAL student state instead of the
    hard-coded 0.30 placeholder."""
    out = {}
    try:
        if REG.dina is not None:
            REG.dina.update(student_id, concept, bool(is_correct))
            # get_mastery returns a {skill: probability} dict even when
            # `skill` is specified — extract the float for the focus skill.
            mdict = REG.dina.get_mastery(student_id, concept) or {}
            if concept in mdict:
                out["dina_mastery"] = float(mdict[concept])
    except Exception as e:
        print(f"[CPAL/mastery] DINA update failed: {e}")
    try:
        if REG.bkt is not None:
            REG.bkt.update_knowledge(student_id, concept, bool(is_correct))
            st = REG.bkt.get_student_knowledge_state(student_id) or {}
            if concept in st:
                out["bkt_mastery"] = float(st[concept])
    except Exception as e:
        print(f"[CPAL/mastery] BKT update failed: {e}")
    return out


def _kg_context_block(concept: str, code: str = "",
                      error_message: str = "") -> str:
    """Build a KG-grounded context block to inject into the tutor prompt.
    Pulls from pedagogical KG (misconceptions/cognitive load), CSE-KG
    (related concepts/prerequisites), and ErrorExplanationMapper (root
    causes for code/error symptoms). Returns '' if nothing useful is
    available so the prompt stays clean."""
    parts = []
    try:
        if REG.pedagogical_kg is not None:
            info = REG.pedagogical_kg.get_concept_full_info(concept) or {}
            ped = info.get("pedagogical_data") or {}
            misc = ped.get("common_misconceptions") or []
            if misc:
                names = [
                    (m.get("description") or m.get("id") or "").strip()[:80]
                    for m in misc[:3]
                ]
                names = [n for n in names if n]
                if names:
                    parts.append(
                        "Pedagogical-KG misconceptions: "
                        + " | ".join(names))
            load = ped.get("cognitive_load") or {}
            if load:
                total = load.get("total")
                factors = load.get("factors") or []
                if total is not None or factors:
                    parts.append(
                        f"Pedagogical-KG cognitive load: total={total}"
                        + (f"  factors={', '.join(factors[:4])}"
                           if factors else ""))
            dom = info.get("domain_knowledge") or {}
            rel = dom.get("related_concepts") or []
            if rel:
                # The KG stores URIs like http://cse-kg.org/ontology/NP-A
                # — strip the prefix so the prompt stays readable.
                short = []
                for r in rel[:4]:
                    uri = r.get("concept", "") if isinstance(r, dict) else str(r)
                    short.append(uri.rsplit("/", 1)[-1])
                parts.append("CSE-KG related concepts: " + ", ".join(short))
    except Exception as e:
        print(f"[CPAL/KG] pedagogical_kg lookup failed: {e}")
    try:
        if REG.concept_retriever is not None and (code or error_message):
            related = REG.concept_retriever.retrieve_from_code(
                code or "", error_message or "", top_k=5) or []
            if related:
                parts.append(
                    "CSE-KG retrieved from code: " + ", ".join(related[:5]))
    except Exception as e:
        print(f"[CPAL/KG] CSE-KG retrieval failed: {e}")
    try:
        if (REG.error_explanation_mapper is not None
                and (code or error_message)):
            expl = REG.error_explanation_mapper.generate_explanation(
                code=code or None,
                error_message=error_message or None,
                student_data={"concept": concept},
            ) or {}
            # Schema: when an error pattern is matched, expl has fields
            # like 'root_cause', 'explanation', 'strategy'. When no pattern
            # matches, expl is {"error_detected": False, ...} — skip then.
            if expl.get("error_detected", True):
                root = (expl.get("root_cause")
                        or expl.get("explanation")
                        or expl.get("strategy"))
                if root:
                    root_str = str(root).strip().split("\n")[0][:280]
                    if root_str:
                        parts.append(f"Error-mapper root cause: {root_str}")
    except Exception as e:
        print(f"[CPAL/KG] error_explanation_mapper failed: {e}")
    if not parts:
        return ""
    return "KG-GROUNDED CONTEXT (use to anchor your explanation; do not " \
           "recite verbatim):\n  - " + "\n  - ".join(parts) + "\n\n"


def _rl_recommended_intervention(student_id: str, concept: str,
                                 mastery: float = 0.3,
                                 emotion: str = "neutral",
                                 lp_level: str = "L1",
                                 hvsae_latent=None) -> tuple:
    """Ask the trained RL teaching agent which intervention type to use
    this turn. Returns (action_str, action_id, q_value, state_vec) so
    callers can later feed the (state_vec, action_id, reward) triple back
    into the agent's replay buffer via store_experience() — enabling the
    policy to LEARN from chat interactions, not just infer.

    Falls back to ('worked_example', 5, 0.0, None) if anything goes
    wrong so the chat keeps working without RL.
    """
    fallback = ("worked_example", 5, 0.0, None)
    try:
        import torch as _t
        agent = REG.teaching_rl_agent
        if agent is None:
            return fallback
        if hvsae_latent is None:
            hvsae_latent = _t.zeros(256)
        session_data = {
            "student_id":      student_id,
            "time_stuck":      0.0,
            "action_sequence": [],
        }
        analysis = {
            "encoding":   {"latent": hvsae_latent.detach().view(-1).float()},
            "cognitive":  {"knowledge_gaps": [{"concept": concept,
                                                 "mastery": float(mastery)}]},
            "behavioral": {"emotional_state": emotion},
            "psychological": {"personality": {}},
            "history":    {"interventions": []},
        }
        try:
            state_vec = agent.get_state_representation(session_data, analysis)
        except Exception:
            state_vec = _t.zeros(agent.state_dim)
        # training=False → no epsilon exploration on inference; we still
        # capture (state, action, q) for the replay buffer.
        action_id, q_value = agent.select_action(state_vec, training=False)
        action_str = agent.actions.get(int(action_id), "worked_example")
        return (action_str, int(action_id), float(q_value), state_vec)
    except Exception as e:
        print(f"[CPAL/RL] teaching agent action selection failed: {e}")
        return fallback


def _rl_finalise_previous(state: dict, current_dina: float,
                          current_emotion: str, current_lp: str,
                          current_state_vec=None,
                          engagement_signal: float = 0.5) -> None:
    """Close out the previous turn's RL step: compute reward from the
    delta between (pending_rl snapshot) and (current signals), push the
    (s, a, r, s') experience into the replay buffer, and run one DQN
    update. Called at the START of each new student turn before picking
    the next action — so the agent's Q-net actually learns from chat.

    Reward heuristic (no graded answer mid-chat, so we approximate):
      learning_gain  = clamp((dina_now - dina_before) * 4, -1, 1)
      engagement     = 2 * (engagement_signal - 0.5)
      emotion_delta  = +0.5 if confused->engaged, -0.5 if engaged->confused
      lp_gain        = +1.0 if LP level advanced, -0.5 if regressed
    Combined: weighted average (weights mirror reward_function.py roughly).
    """
    try:
        pending = state.get("pending_rl") or {}
        if not pending or REG.teaching_rl_agent is None:
            return
        import torch as _t

        agent = REG.teaching_rl_agent
        s_before     = pending.get("state_vec")
        action_id    = int(pending.get("action_id", 5))
        dina_before  = float(pending.get("dina", 0.3))
        emotion_before = pending.get("emotion", "neutral")
        lp_before    = pending.get("lp_level", "L1")

        if s_before is None:
            state.pop("pending_rl", None)
            return
        if current_state_vec is None:
            current_state_vec = _t.zeros(agent.state_dim)

        # ── reward components ──────────────────────────────────────────
        gain     = float(current_dina) - dina_before
        learning_gain = max(-1.0, min(1.0, gain * 4.0))

        engagement    = max(-1.0, min(1.0, 2.0 * (engagement_signal - 0.5)))

        emo_score = {"frustrated": -1.0, "confused": -0.5, "neutral": 0.0,
                     "engaged": 0.5, "confident": 1.0}
        emotion_delta = (emo_score.get(current_emotion, 0.0)
                          - emo_score.get(emotion_before, 0.0))

        lp_order = {"L1": 1, "L2": 2, "L3": 3, "L4": 4}
        lp_delta = lp_order.get(current_lp, 1) - lp_order.get(lp_before, 1)
        if lp_delta > 0:    lp_gain =  1.0
        elif lp_delta < 0:  lp_gain = -0.5
        else:               lp_gain =  0.0

        # Weights roughly match reward_function.py's split.
        reward = (0.30 * learning_gain
                  + 0.20 * engagement
                  + 0.20 * emotion_delta
                  + 0.30 * lp_gain)

        # Store + learn.
        agent.store_experience(s_before, action_id, float(reward),
                                current_state_vec, done=False)
        loss = None
        try:
            loss = agent.learn_from_experience()
        except Exception as _e:
            print(f"[CPAL/RL] learn_from_experience failed: {_e}")

        steps = getattr(agent, "steps", None)
        loss_str = f"loss={loss:.3f}" if isinstance(loss, (int, float)) else "loss=skip"
        print(f"[CPAL/RL] store_experience action={agent.actions.get(action_id)} "
              f"reward={reward:+.3f} ({loss_str}) buffer={len(agent.memory)} "
              f"steps={steps}", flush=True)

        # Stash the latest reward/loss/steps so the status pill can show them.
        state["last_rl_reward"] = float(reward)
        state["last_rl_loss"]   = loss if isinstance(loss, (int, float)) else None
        state["last_rl_steps"]  = int(steps) if isinstance(steps, int) else None

        # Pending RL slot is now consumed.
        state.pop("pending_rl", None)
    except Exception as e:
        print(f"[CPAL/RL] _rl_finalise_previous failed: {e}")


def _dynamic_kg_learn(student_id: str, concept: str, is_correct: bool,
                      intervention_type: str = "worked_example") -> None:
    """Feed this turn's outcome into the dynamic KG updater so prerequisite
    strengths, misconception frequencies, and intervention effectiveness
    accumulate across sessions."""
    try:
        updater = REG.dynamic_kg_updater
        if updater is None:
            return
        updater.update_from_interaction(
            session_data={
                "student_id":  student_id,
                "concept":     concept,
                "intervention": intervention_type,
            },
            student_outcome={"mastery_delta": 0.1 if is_correct else -0.05},
            success=bool(is_correct),
        )
    except Exception as e:
        print(f"[CPAL/RL] dynamic_kg update failed: {e}")


# ──────────────────────────────────────────────────────────────────────────
# CPAL teach-turn context builders — populate the `analysis` dict so the
# generator's KNOWLEDGE GRAPHS (MUST REFERENCE IN RESPONSE) section, LP-Multi
# mini-replies block, and 3-channel psychological state section all fire
# with real data instead of empty dicts.
# ──────────────────────────────────────────────────────────────────────────

def _build_cse_kg_block(concept: str) -> dict:
    """Pull concept info + prerequisites + related concepts from CSE-KG.
    Shape matches what enhanced_personalized_generator expects in
    analysis['cse_kg']: {concept, prerequisites, related_concepts, definition}.
    """
    out = {}
    try:
        if REG.cse_kg_client is None:
            return out
        info = REG.cse_kg_client.get_concept_info(concept) or {}
        out["concept"]    = concept
        out["definition"] = (info.get("description")
                              or info.get("label")
                              or "")
        try:
            prereqs = REG.cse_kg_client.get_prerequisites(concept) or []
            # Strip URI prefix for readability
            out["prerequisites"] = [
                (p.rsplit("/", 1)[-1] if isinstance(p, str) else str(p))
                for p in prereqs[:5]
            ]
        except Exception:
            out["prerequisites"] = []
        related = info.get("related_concepts") or []
        out["related_concepts"] = [
            (r.get("concept", "").rsplit("/", 1)[-1]
             if isinstance(r, dict) else str(r))
            for r in related[:5]
        ]
    except Exception as e:
        print(f"[CPAL/CSE-KG] build failed: {e}")
    return out


def _build_pedagogical_kg_block(concept: str) -> dict:
    """Shape pedagogical KG output into the structure the generator's
    Pedagogical-KG section reads: {progression, misconceptions,
    cognitive_load, interventions, learning_path}.
    """
    out = {}
    try:
        if REG.pedagogical_kg is None:
            return out
        info = REG.pedagogical_kg.get_concept_full_info(concept) or {}
        ped  = info.get("pedagogical_data") or {}
        out["progression"] = ped.get("progression") or ped.get(
            "difficulty_level", "")
        miscs = ped.get("common_misconceptions") or []
        out["misconceptions"] = [
            (m.get("description") or m.get("id") or "")[:120]
            for m in miscs[:3]
            if (m.get("description") or m.get("id"))
        ]
        load = ped.get("cognitive_load") or {}
        if load:
            out["cognitive_load"] = (
                f"total={load.get('total', '?')} "
                f"intrinsic={load.get('intrinsic', '?')} "
                f"germane={load.get('germane', '?')}")
        else:
            out["cognitive_load"] = ""
        interventions = ped.get("recommended_interventions") or []
        if isinstance(interventions, list):
            out["interventions"] = [str(i)[:60] for i in interventions[:4]]
        else:
            out["interventions"] = []
    except Exception as e:
        print(f"[CPAL/Ped-KG] build failed: {e}")
    return out


def _build_coke_block(session_data: dict) -> dict:
    """Run COKECognitiveGraph theory-of-mind inference on this turn's
    text + code; shape into analysis['coke']."""
    out = {}
    try:
        if REG.coke_graph is None:
            return out
        tom = REG.coke_graph.infer_theory_of_mind(session_data) or {}
        out["cognitive_state"]     = tom.get("predicted_cognitive_state",
                                              tom.get("cognitive_state", ""))
        out["mental_activity"]     = tom.get("mental_activity", "")
        out["behavioral_response"] = tom.get("predicted_behavioral_response",
                                              tom.get("behavioral_response", ""))
        out["confidence"]          = float(tom.get("confidence", 0.5))
        chain = tom.get("cognitive_chain") or {}
        if chain:
            out["cognitive_chain"] = {
                "description": chain.get("description", "")
            }
    except Exception as e:
        print(f"[CPAL/COKE] build failed: {e}")
    return out


def _run_three_channel(student_id: str, session_data: dict) -> dict:
    """Run the language/structure/content three-channel analysis via the
    orchestrator's state_tracker. Populates analysis['psychological_state']
    so the generator's PSYCHOLOGICAL STATE section fires."""
    try:
        tracker = getattr(REG.orchestrator, "state_tracker", None)
        if tracker is None:
            return {}
        result = tracker.analyse_prompt(student_id, session_data) or {}
        return result
    except Exception as e:
        print(f"[CPAL/3-Channel] analyse_prompt failed: {e}")
        return {}


def _run_diagnose_multi(student_id: str,
                        question_text: str,
                        session_data: dict,
                        hvsae_latent=None,
                        hvsae_misconception_probs=None) -> dict:
    """Run multi-concept diagnosis so the generator's LP-Multi
    PER-CONCEPT MINI-REPLIES block has data to fire on. Returns the
    {focus, focus_concept, diagnostics: {concept: diag_dict}} shape."""
    try:
        resolver = getattr(REG.orchestrator, "concept_resolver", None)
        diagn    = REG.lp_diagnostician
        tracker  = getattr(REG.orchestrator, "state_tracker", None)
        if resolver is None or diagn is None:
            return {}
        resolved = resolver.resolve(session_data) or []
        # Pull stored LP per resolved concept
        stored_lp = {}
        if tracker is not None:
            for c, _conf in resolved:
                if c and c != "unknown":
                    try:
                        stored_lp[c] = tracker.load_lp_state(
                            student_id, c) or {}
                    except Exception:
                        stored_lp[c] = {}
        multi = diagn.diagnose_multi(
            student_id=student_id,
            question_text=question_text,
            resolved_concepts=resolved,
            stored_lp=stored_lp,
            hvsae_latent=hvsae_latent,
            hvsae_misconception_probs=hvsae_misconception_probs,
        )
        # diagnose_multi returns an object with .to_dict() OR a dict already;
        # normalise to dict-of-dicts for downstream consumption.
        if hasattr(multi, "to_dict"):
            return multi.to_dict()
        if isinstance(multi, dict):
            # Per-concept diag objects → dicts
            diags = multi.get("diagnostics") or {}
            normalised = {}
            for c, d in diags.items():
                normalised[c] = d.to_dict() if hasattr(d, "to_dict") else d
            return {
                "focus_concept": multi.get("focus_concept"),
                "focus":         (multi.get("focus").to_dict()
                                   if hasattr(multi.get("focus"), "to_dict")
                                   else multi.get("focus")),
                "diagnostics":   normalised,
            }
        return {}
    except Exception as e:
        print(f"[CPAL/LP-Multi] diagnose_multi failed: {e}")
        return {}


# =========================================================================
# Diagnosis helpers
# =========================================================================
def _hvsae_forward(text):
    if TOKENIZER is not None:
        ids = TOKENIZER(text, return_tensors="pt", padding=True,
                        truncation=True, max_length=128
                        )["input_ids"].long() % 6000
    else:
        ids = torch.randint(1, 5999, (1, 16))
    batch = {"code_tokens": torch.zeros(1, 10, dtype=torch.long),
             "text_tokens": ids,
             "action_sequence": torch.ones(1, 8, dtype=torch.long)}
    with torch.no_grad():
        out = HVSAE_MODEL.forward(batch, compute_graph=False)
    return out["latent"], torch.softmax(out["misconception_logits"], dim=-1)


def _diagnose(student_reasoning, concept_id, code, question, picked_option):
    full_text = (
        f"Quiz: {question}\n"
        f"My pick: {picked_option}\n"
        f"My reasoning: {student_reasoning}\n"
        f"Code:\n{code}"
    )
    latent, mp = _hvsae_forward(full_text)
    diag = DX.diagnose(
        student_id="chat_user",
        concept=concept_id,
        question_text=student_reasoning,
        stored_lp_level="L1", stored_lp_streak=0,
        hvsae_latent=latent, hvsae_misconception_probs=mp,
    ).to_dict()
    lvl_idx = LP_INDEX.get(diag["current_lp_level"], 0)
    if diag.get("wrong_model_id") and diag.get("match_score", 0) >= 0.4 \
            and lvl_idx >= LP_INDEX["L3"]:
        diag["fusion_note"] = (
            f"wrong-model {diag['wrong_model_id']} with conf "
            f"{diag['match_score']:.2f} → cap LP at L2")
        lvl_idx = LP_INDEX["L2"]
    else:
        diag["fusion_note"] = None
    diag["current_lp_level"] = LP_ORDER[lvl_idx]
    diag["target_lp_level"]  = LP_ORDER[min(lvl_idx + 1, 3)]
    return diag


def _format_diag(diag, concept_id):
    out = []
    out.append(f"### 🔍 Diagnosis\n")
    out.append(f"- **Concept**: `{concept_id}`\n")
    out.append(f"- **Wrong model**: **{diag.get('wrong_model_id') or '—'}** "
               f"(via `{diag.get('source')}`)\n")
    wm = CATALOGUE.get_wrong_model(concept_id,
                                    diag.get("wrong_model_id") or "")
    if wm:
        out.append(f"  - *belief*: {wm.wrong_belief}\n")
        out.append(f"  - *origin*: {wm.origin}\n")
    out.append(f"- **LP**: {diag['current_lp_level']} → target "
               f"{diag['target_lp_level']}\n")
    if diag.get("fusion_note"):
        out.append(f"- **Fusion rule fired**: {diag['fusion_note']}\n")
    out.append(f"\n#### LP-level distribution\n")
    for lvl in ("L1", "L2", "L3", "L4"):
        p = diag.get("trained_lp_probs", {}).get(lvl, 0.0)
        bar_len = int(round(p * 25))
        out.append(f"`{lvl}` {p*100:5.1f}% {'█'*bar_len}{'·'*(25-bar_len)}\n")
    out.append(f"\n#### Wrong-model distribution (within concept)\n")
    for t in diag.get("trained_wm_probs", []):
        p = t["prob"]
        bar_len = int(round(p * 25))
        out.append(f"`{t['wm_id']:6s}` {p*100:5.1f}% "
                   f"{'█'*bar_len}{'·'*(25-bar_len)}\n")
    out.append(f"\n#### Expert benchmark (L3 mechanism)\n")
    for k in diag.get("expert_benchmark_key_ideas", [])[:5]:
        out.append(f"- {k}\n")
    return "".join(out)


# =========================================================================
# UI callbacks
# =========================================================================
_PICKED_STYLE = (
    "display:block; background:#1e293b; color:#ffffff; font-style:italic; "
    "padding:8px 12px; border-radius:0 0 8px 8px; margin-top:-2px; "
    "border:1px solid #334155; border-top:none;"
)

def _quiz_card_md(q, picked_option_full=None):
    md = (
        f"**Quiz {q['id']} — `{q['concept']}`**  \n"
        f"{q['question']}\n"
        f"```java\n{q['code']}\n```"
    )
    if picked_option_full:
        safe = picked_option_full.replace("<", "&lt;").replace(">", "&gt;")
        md += f'\n<span style="{_PICKED_STYLE}">Your pick: {safe}</span>'
    return md


def on_select_quiz(quiz_id):
    q = QUIZ_BY_ID.get(quiz_id)
    if not q:
        return "", "", gr.update(choices=[], value=None), gr.update(value="", visible=False)
    md = _quiz_card_md(q)
    choices = [f"{k}. {v}" for k, v in q["options"].items()]
    return md, "", gr.update(choices=choices, value=None), gr.update(value="", visible=False)


def on_pick_option(quiz_id, picked_option_full):
    """Re-render the quiz card so the picked option appears in white italic
    directly under the code snippet."""
    q = QUIZ_BY_ID.get(quiz_id)
    if q is None:
        return gr.update()
    return _quiz_card_md(q, picked_option_full)


def _render_user_bubble(q, picked_option_text, reasoning):
    safe_pick = (picked_option_text or "").replace("<", "&lt;").replace(">", "&gt;")
    return (
        f"**Quiz {q['id']}** — *{q['concept']}*  \n"
        f"{q['question']}\n"
        f"```java\n{q['code']}\n```\n"
        f'<span style="{_PICKED_STYLE}">My pick: {safe_pick}</span>\n\n'
        f"**My reasoning:** {reasoning}"
    )


# =========================================================================
# Ongoing chat — multi-turn probe ladder + comprehensive-answer stage
# =========================================================================
# The system keeps probing as long as the student's belief isn't confidently
# at the target level. When a "stage" is reached (confidence high enough OR
# most sub-criteria demonstrated OR student requested OR chat depth cap),
# the tutor stops probing and produces a COMPREHENSIVE synthesis instead of
# another short reply. Probes themselves are dynamic — the question text is
# generated by the LLM per turn (see src/orchestrator/depth_probe.py).

CHAT_PROBE_CONFIDENCE_FLOOR   = 0.55   # under this -> still probing
CHAT_COMPREHENSIVE_CONF_FLOOR = 0.82   # at/above this -> stage reached
CHAT_MAX_PROBES               = 8      # hard cap; before this, the
                                       #   stage-reached detector usually
                                       #   triggers earlier.
# Regex patterns indicating the student is asking us to just give the answer.
_STUDENT_GIVE_UP = re.compile(
    r"\b(just (tell|give|show) me|"
    r"i give up|i don't know|idk\b|"
    r"reveal( the)? answer|show( the)? answer|"
    r"explain it|skip the (quiz|check))\b",
    re.I,
)


def _student_requested_answer(text: str) -> bool:
    return bool(_STUDENT_GIVE_UP.search(text or ""))


def _detect_other_concepts(student_text: str, quiz_concept: str) -> list:
    """Run ConceptResolver on the student's free-form text and return concept
    IDs OTHER than the quiz's tagged concept that the student also mentioned
    — so the chat can surface multi-concept awareness even though the quiz
    item is single-concept by design.

    Returns up to 3 other concepts, ranked by ConceptResolver confidence,
    above a low floor. Empty list when nothing additional was detected.
    """
    try:
        from src.orchestrator.concept_resolver import ConceptResolver
        # Lazily build a resolver — cheap (signature scoring + RAG lazy).
        global _CONCEPT_RESOLVER
        if "_CONCEPT_RESOLVER" not in globals():
            _CONCEPT_RESOLVER = ConceptResolver()
        ranked = _CONCEPT_RESOLVER.resolve({"question": student_text or ""})
    except Exception:
        return []
    others = [(c, s) for c, s in ranked
              if c != quiz_concept and c != "unknown" and s >= 0.25]
    return others[:3]


def _status_pill_with_diag(state: dict, diag: dict, base_status: str) -> str:
    """Append the STUDENT-FACING status line + a collapsible HTML <details>
    block holding the geeky tutor internals (LP level, conf, facet count).
    Native HTML <details> means no new Gradio component is needed; the
    research/engineer view is one click away and the default view stays
    beginner-friendly."""
    if not state or not diag:
        return base_status
    try:
        others = _detect_other_concepts(
            state.get("accumulated_belief", ""),
            QUIZ_BY_ID[state["quiz_id"]]["concept"] if state.get("quiz_id") else "",
        )
        friendly_line = _status_md(state, diag, others)
        details_block = _tutor_details_md(state, diag)
    except Exception:
        friendly_line = ""
        details_block = ""
    if not friendly_line:
        return base_status
    return (
        f"{base_status}  \n"
        f"<small>{friendly_line}</small>\n\n"
        f"<details><summary>"
        f"<small style=\"color:#64748b\">"
        f"Show tutor details (LP level, confidence, facets)</small>"
        f"</summary>\n\n"
        f"{details_block}\n\n"
        f"</details>"
    )


# Plain-language mapping for catalogue concept_ids — used in the
# student-facing status line so "null_pointer" reads as "NullPointerException"
# rather than the snake_case internal id. Falls back to title-casing.
_CONCEPT_FRIENDLY = {
    "null_pointer":         "NullPointerException",
    "string_equality":      "string equality (== vs .equals)",
    "integer_division":     "integer division",
    "array_index":          "array index out of bounds",
    "infinite_loop":        "infinite loop",
    "static_vs_instance":   "static vs instance",
    "type_mismatch":        "type mismatch",
    "variable_scope":       "variable scope",
    "assignment_vs_compare":"= vs ==",
    "scanner_buffer":       "Scanner.nextLine after nextInt",
    "missing_return":       "missing return",
    "array_not_allocated":  "uninitialised array",
    "boolean_operators":    "boolean && and ||",
    "sentinel_loop":        "sentinel-controlled loop",
    "unreachable_code":     "unreachable code",
    "string_immutability":  "string immutability",
    "no_default_constructor":"missing default constructor",
    "foreach_no_modify":    "for-each can't modify the array",
    "overloading":          "method overloading",
    "generics_primitives":  "generics with primitives",
}

# Plain-language label for LP levels — student never sees "L1/L2/L3/L4",
# they see what the level MEANS pedagogically.
_LP_FRIENDLY = {
    "L1": "just starting",
    "L2": "you know the rule",
    "L3": "you can explain the mechanism",
    "L4": "you can generalise",
}


def _friendly_concept(c: Optional[str]) -> str:
    if not c:
        return "this concept"
    return _CONCEPT_FRIENDLY.get(c, c.replace("_", " ").title())


def _status_md(state: dict, diag: dict, other_concepts: list) -> str:
    """Compose the STUDENT-FACING one-line status header.

    No L1/L2/L3/L4 jargon, no "conf 0.55", no snake_case concept_ids. The
    geeky internal state (LP levels, raw confidences, criterion counts) is
    moved into the optional collapsible 'Show tutor details' expander —
    not shown by default.
    """
    focus = state.get("pending_concept_id") or (
        state.get("quiz_id") and QUIZ_BY_ID[state["quiz_id"]]["concept"]
    )
    friendly_focus = _friendly_concept(focus)

    # Multi-turn probe ladder is OFF — no "N quick checks in" counter to
    # show. The student sees just the focus concept and (after diagnosis)
    # the LP transition. Everything else lives in the details expander.
    parts = [f"📚 Working on: **{friendly_focus}**"]
    if other_concepts:
        also = ", ".join(_friendly_concept(c) for c, _ in other_concepts[:2])
        parts.append(f"you also touched on: {also}")
    return "  ·  ".join(parts)


def _tutor_details_md(state: dict, diag: dict) -> str:
    """The geeky internals — LP level transition, facets probed/total,
    diagnostic confidence, last probe reason. Shown inside the optional
    'Show tutor details' expander so the engineer/researcher view is still
    available without polluting the student-facing UI."""
    focus = state.get("pending_concept_id") or (
        state.get("quiz_id") and QUIZ_BY_ID[state["quiz_id"]]["concept"]
    )
    cur   = diag.get("current_lp_level", "?")
    tgt   = diag.get("target_lp_level", "?")
    cur_plain = _LP_FRIENDLY.get(cur, cur)
    tgt_plain = _LP_FRIENDLY.get(tgt, tgt)
    target_sub = (diag.get("lp_sub_criteria") or {}).get(tgt) or []
    probed = [c for c in (state.get("probed_criteria") or [])
              if c in target_sub]
    conf  = float(diag.get("diagnostic_confidence", 0.0))
    rg = diag.get("rubric_grade") or {}
    # RL agent footer — surfaces the trained policy's per-turn action,
    # Q-value, last reward, training-step counter, and last DQN loss so
    # the user can see RL firing AND learning across turns. Hidden when
    # no RL data is on `state` (e.g. first message after clear_chat).
    rl_action = state.get("last_rl_action")
    rl_q      = state.get("last_rl_q")
    rl_reward = state.get("last_rl_reward")
    rl_steps  = state.get("last_rl_steps")
    rl_loss   = state.get("last_rl_loss")
    rl_lines  = ""
    if rl_action is not None:
        rl_lines += f"- **RL action chosen:** `{rl_action}`"
        if isinstance(rl_q, (int, float)):
            rl_lines += f"  (Q = {rl_q:+.3f})"
        rl_lines += "\n"
    if rl_steps is not None:
        rl_lines += (
            f"- **RL training steps:** {rl_steps}"
            + (f"  (last reward {rl_reward:+.3f})"
               if isinstance(rl_reward, (int, float)) else "")
            + (f"  (loss {rl_loss:.3f})"
               if isinstance(rl_loss, (int, float)) else "")
            + "\n")
    elif isinstance(rl_reward, (int, float)):
        rl_lines += f"- **Last RL reward:** {rl_reward:+.3f}\n"

    return (
        f"- **Concept:** `{focus}`\n"
        f"- **Level:** `{cur}` ({cur_plain}) → `{tgt}` ({tgt_plain})\n"
        f"- **Facets at target level probed:** {len(probed)} / {len(target_sub)}\n"
        f"- **Diagnostic confidence:** {conf:.2f}\n"
        f"- **Grader verdict:** `{rg.get('level','?')}` (conf {rg.get('confidence',0):.2f})\n"
        f"- **Last probe reason:** {state.get('pending_probe_reason') or '—'}\n"
        + rl_lines
    )


def _stage_reached(state: dict, diag: dict) -> Optional[str]:
    """Return a non-empty string naming the stage trigger, or None if not yet.

    Triggers (any one is sufficient):
      * 'force'              — caller forced via 'Reveal full answer'
      * 'student_request'    — accumulated belief contains an explicit request
      * 'high_confidence'    — diagnostic_confidence >= CHAT_COMPREHENSIVE_CONF_FLOOR
      * 'sub_criteria_done'  — every sub-criterion at target level has been probed
      * 'cap'                — CHAT_MAX_PROBES probes already issued
    """
    if state.get("force_comprehensive"):
        return "force"
    if _student_requested_answer(state.get("accumulated_belief", "")):
        return "student_request"
    conf = float(diag.get("diagnostic_confidence", 0.0))
    if conf >= CHAT_COMPREHENSIVE_CONF_FLOOR:
        return "high_confidence"
    target = diag.get("target_lp_level") or "L3"
    sub_map = diag.get("lp_sub_criteria") or {}
    sub = sub_map.get(target) or []
    if sub and all(c in state.get("probed_criteria", []) for c in sub):
        return "sub_criteria_done"
    if state.get("probe_count", 0) >= CHAT_MAX_PROBES:
        return "cap"
    return None


def _pick_focus_concept(state: dict) -> str:
    """Multi-concept focus picker. Cycles through concepts: the quiz's
    tagged concept FIRST, then any others the student raised in their
    free-form belief that haven't been satisfied yet. Returns the concept
    the next probe should target.

    Once a concept's ladder is satisfied (stage_reached fired for it), it
    gets appended to state["concepts_done"]. The next call to this picker
    pivots focus to the next unsatisfied concept — that's the multi-concept
    probing the chat now actually runs (was just a 'also detected' list).
    """
    quiz_concept = QUIZ_BY_ID[state["quiz_id"]]["concept"]
    done = list(state.get("concepts_done") or [])
    # Candidate order: quiz concept first, then ConceptResolver hits.
    others = _detect_other_concepts(
        state.get("accumulated_belief", ""), quiz_concept,
    )
    candidates = [quiz_concept] + [c for c, _ in others
                                     if c != quiz_concept]
    # Keep current focus if it's still unsatisfied.
    cur = state.get("current_focus_concept")
    if cur and cur in candidates and cur not in done:
        return cur
    # Pivot to the first unsatisfied candidate.
    for c in candidates:
        if c not in done:
            return c
    # Everything satisfied — stay on the quiz concept (caller will detect
    # all_concepts_done and produce the comprehensive synthesis).
    return quiz_concept


def _decide_probe_or_teach(state: dict):
    """Re-diagnose on the accumulated belief and decide probe vs teach.

    Composes deep-diagnostic with multi-turn / multi-facet / MULTI-CONCEPT:
      Step 0 — pick the focus CONCEPT (multi-concept ladder: quiz concept
               first, then any others detected in free-form text that
               haven't been satisfied yet).
      Tier 1 — DEPTH PROBE for the focus concept (jargon trap / similarity).
      Tier 2 — per-facet sub-criterion probe for the focus concept.
      Tier 3 — teach (probe-cap reached / confidence satisfied / etc.).

    When a concept's ladder is satisfied, it's appended to concepts_done
    and the next turn pivots to the next unsatisfied concept (with a
    short bridge message in the chat). Only when EVERY concept is done
    (or force-comprehensive fires) do we produce the full synthesis.

    Returns:
      ("probe", criterion_key_or_text, target_level, state, diag)
      ("teach", None,                   None,         state, diag)
    Pivots between concepts recursively — when the current concept's ladder
    is satisfied and another concept needs probing, this function recurses
    on the new focus and sets state["bridge_message"] so the caller can
    surface a short "Now let's look at <next>" line in the chat.
    """
    # Recursion guard — never pivot more than 4 concepts in a single turn.
    if state.get("_pivot_depth", 0) > 4:
        state["stage_trigger"] = "all_concepts_done"
        # Build a minimal diag so callers don't NPE.
        diag_fallback = {"current_lp_level": "L1", "target_lp_level": "L2",
                         "diagnostic_confidence": 1.0}
        return ("teach", None, None, state, diag_fallback)
    # Reset the pivot guard once per call from a real entry point.
    # (Recursive pivots already increment it; this initialises on first call.)
    state.setdefault("_pivot_depth", 0)

    # Step 0 — multi-concept focus selection.
    focus_concept = _pick_focus_concept(state)
    previous_focus = state.get("current_focus_concept")
    pivoted = (previous_focus is not None
               and previous_focus != focus_concept)
    state["current_focus_concept"] = focus_concept
    if pivoted:
        # New focus concept — reset the ladder counters so this concept gets
        # its own probe budget. The accumulated belief stays (the student's
        # whole reasoning is still graded for each concept).
        state["probe_count"]     = 0
        state["probed_criteria"] = []

    q = QUIZ_BY_ID[state["quiz_id"]]
    # Diagnose against the FOCUS concept (not always the quiz's tagged one).
    diag = _diagnose(
        state["accumulated_belief"], focus_concept, q["code"],
        q["question"], state["picked_option_full"],
    )
    conf = float(diag.get("diagnostic_confidence", 1.0))

    # Stage-reached check FIRST. When fired for a NON-force trigger, mark
    # the current focus concept as "done" and check if there are more
    # concepts to probe — if so, return a 'pivot' decision so the caller
    # emits a bridge message instead of the comprehensive synthesis. Only
    # 'force' (or all concepts done) goes straight to comprehensive.
    stage = _stage_reached(state, diag)
    if stage is not None:
        if stage != "force":
            done = state.setdefault("concepts_done", [])
            if focus_concept not in done:
                done.append(focus_concept)
            # Are there more concepts to cover?
            quiz_concept = QUIZ_BY_ID[state["quiz_id"]]["concept"]
            others = _detect_other_concepts(
                state.get("accumulated_belief", ""), quiz_concept,
            )
            candidates = [quiz_concept] + [c for c, _ in others
                                            if c != quiz_concept]
            next_concept = next((c for c in candidates if c not in done), None)
            if next_concept and next_concept != focus_concept:
                # Pivot — set a bridge message the caller can prepend to the
                # next probe, then RECURSE so the new focus's probe is
                # selected immediately (no extra round-trip needed).
                state["stage_trigger"]         = None
                state["current_focus_concept"] = next_concept
                state["probe_count"]           = 0
                state["probed_criteria"]       = []
                state["bridge_message"] = (
                    f"👍 Got what we needed on "
                    f"**{_friendly_concept(focus_concept)}**. "
                    f"Now let's look at "
                    f"**{_friendly_concept(next_concept)}**, "
                    f"which you also touched on."
                )
                state["_pivot_depth"] = state.get("_pivot_depth", 0) + 1
                return _decide_probe_or_teach(state)
            # Every concept done — fall through to comprehensive synthesis.
            stage = "all_concepts_done"
        state["stage_trigger"] = stage
        return ("teach", None, None, state, diag)

    if (conf < CHAT_PROBE_CONFIDENCE_FLOOR
            and state["probe_count"] < CHAT_MAX_PROBES):
        target = diag.get("target_lp_level") or "L3"

        # Tier 1 — depth probe. select_depth_probe returns a DepthProbe whose
        # `question` text is the ready-to-show probe. We stash it on `state`
        # so _probe_question_md_for can render the depth question (not a
        # generic "in your own words why is this true" wrapper).
        try:
            from src.orchestrator.depth_probe import select_depth_probe
            dp = select_depth_probe(
                state["accumulated_belief"], CATALOGUE, q["concept"],
                already_probed=state["probed_criteria"],
            )
        except Exception as _e:
            dp = None
        if dp is not None:
            state["probed_criteria"].append(dp.criterion_key)
            state["probe_count"] += 1
            state["pending_probe_text"]   = dp.question
            state["pending_probe_reason"] = dp.reason
            state["pending_concept_id"]   = q["concept"]
            state["pending_facet_pos"]    = None     # depth probes aren't facet-numbered
            state["pending_facet_total"]  = None
            return ("probe", dp.criterion_key, target, state, diag)

        # Tier 2 — per-criterion sub-rubric (multi-facet ladder).
        sub_map = diag.get("lp_sub_criteria") or {}
        sub = sub_map.get(target) or []
        for i, c in enumerate(sub, start=1):
            if c not in state["probed_criteria"]:
                state["probed_criteria"].append(c)
                state["probe_count"] += 1
                state["pending_probe_text"]   = None    # render via wrapper
                state["pending_probe_reason"] = "sub_criterion"
                state["pending_concept_id"]   = q["concept"]
                # Position of THIS criterion in the target-level facet list,
                # 1-indexed, plus total facets. Lets the UI show e.g.
                # "facet 2/5" so the student sees the multi-facet ladder
                # progressing.
                state["pending_facet_pos"]    = i
                state["pending_facet_total"]  = len(sub)
                return ("probe", c, target, state, diag)
    # Catch-all teach: confidence is in the "between" zone (>= probe floor
    # but < comprehensive floor) AND no probe candidate was found, OR
    # probe_count is at cap. Either way, mark this as a default-trigger
    # teach so _stream_teach still builds the LP-shaped comprehensive
    # header (with rubric/sub-criteria/plateau/etc. wired in) instead of
    # falling back to the EnhancedPersonalizedGenerator's generic
    # per-intervention template.
    state["stage_trigger"] = "default"
    return ("teach", None, None, state, diag)


def _probe_question_md(criterion: str, target: str,
                       round_n: int, round_max: int,
                       depth_text: Optional[str] = None,
                       depth_reason: Optional[str] = None,
                       concept_id: Optional[str] = None,
                       facet_pos: Optional[int] = None,
                       facet_total: Optional[int] = None) -> str:
    """Render the probe question with FULL per-facet / per-concept labelling
    so the student can see which sub-skill of which concept is being probed.

    Format (sub-criterion probe):
       **Quick check 2** · `null_pointer` · facet 2/5 (L3 mechanism)
       In your own words — can you explain *why* this is true?
       > new allocates a heap object and returns its address

    Format (depth probe — jargon / similarity):
       **Quick check 3** · `string_equality` · depth check — vocabulary
       [LLM-generated probe text targeting the specific student wording]
    """
    # Header line — student-friendly: plain concept name + "check N of M"
    # (instead of "facet N/M (L3 criterion)" which is internal jargon).
    parts = [f"**Quick check {round_n}**"]
    friendly = _friendly_concept(concept_id) if concept_id else ""
    if friendly:
        parts.append(friendly)
    if depth_text:
        tag = {
            "jargon_trap":            "let's check what you mean by this term",
            "high_sim_to_wrong":      "let's pin down what's actually happening",
            "dynamic_sim_to_wrong":   "let's pin down what's actually happening",
            "dynamic_vocab_density":  "let's trace what you wrote",
        }.get(depth_reason or "", "quick depth check")
        parts.append(f"<span style=\"color:#64748b\">({tag})</span>")
        header = " · ".join(parts)
        return f"{header}\n\n{depth_text}"

    if facet_pos and facet_total:
        parts.append(f"check {facet_pos} of {facet_total}")
    header = " · ".join(parts)
    c = (criterion or "").strip().rstrip(".")
    return (
        f"{header}\n\n"
        f"In your own words — can you explain *why* this is true?\n\n"
        f"> {c}"
    )


def stream_response(quiz_id, picked_option_full, reasoning, history, state):
    """Initial submit. Validates inputs, initialises the probe-ladder state,
    then either fires a probe (showing the probe panel) or streams the tutor
    teach reply. Outputs:
      (history, status, probe_panel_visibility, probe_question_md,
       probe_input_clear, state)
    """
    if not quiz_id:
        yield (history, gr.update(value="⚠️ Select a quiz first.", visible=True),
               gr.update(visible=False), "", "", state)
        return
    q = QUIZ_BY_ID.get(quiz_id)
    if q is None:
        yield (history, gr.update(value="⚠️ Unknown quiz.", visible=True),
               gr.update(visible=False), "", "", state)
        return
    if not picked_option_full:
        yield (history, gr.update(value="⚠️ Pick an option (A/B/C/D) before submitting.", visible=True),
               gr.update(visible=False), "", "", state)
        return
    if not reasoning.strip():
        yield (history, gr.update(value="⚠️ Write your reasoning for this pick, then submit.", visible=True),
               gr.update(visible=False), "", "", state)
        return

    # Parse letter off the option string "A. ..."
    picked_letter = picked_option_full.strip()[:1].upper()
    picked_text   = q["options"].get(picked_letter, picked_option_full)
    correct = (picked_letter == q["correct_answer"])

    # Update DINA + BKT mastery now that we know correctness for this MCQ.
    # The returned dict is stashed on `state` and threaded into the LLM
    # prompt so the tutor reply is shaped by REAL mastery, not a 0.30 stub.
    mastery_now = _update_mastery("chat_user", q["concept"], correct)

    # Build the correct/wrong status pill text up front so we can show it
    # IMMEDIATELY on submission — before diagnosis and the LLM run.
    if correct:
        status_template = "✅ **Correct!** Read your tutor's explanation below."
    else:
        status_template = (
            f"❌ You picked **{picked_letter}**, but the correct answer is "
            f"**{q['correct_answer']}** — {q['options'][q['correct_answer']]}. "
            f"Your tutor will walk you through it below."
        )

    # Fresh chat state for this question. Multi-turn probe ladder is now
    # DISABLED — every first turn goes straight to comprehensive synthesis
    # (force_comprehensive=True). All upstream diagnosis (ConceptResolver,
    # LPDiagnostician, RubricGrader, CatalogueRAG, depth_probe,
    # lp_sub_criteria) still runs and feeds the synthesis prompt — we just
    # don't ping-pong with the student to iteratively elicit; we trust the
    # diagnosis on the initial belief and produce a high-quality LP-shaped
    # teaching reply once. Follow-up student messages are free-form Q&A
    # against the same diagnosis.
    state = {
        "quiz_id":             quiz_id,
        "picked_option_full":  picked_option_full,
        "picked_letter":       picked_letter,
        "picked_text":         picked_text,
        "is_correct":          correct,
        "status_template":     status_template,
        "accumulated_belief":  reasoning.strip(),
        "probe_count":         0,
        "probed_criteria":     [],
        "user_bubble":         _render_user_bubble(q, picked_text, reasoning),
        "pending_probe_text":  None,
        "pending_probe_reason": None,
        # Multi-probe RE-ENABLED — every first turn now runs the probe
        # ladder when diagnostic_confidence is below CHAT_PROBE_CONFIDENCE_FLOOR.
        # _stage_reached fires the comprehensive synthesis only when one of:
        #   force / student_request / high_confidence / sub_criteria_done / cap.
        "force_comprehensive": False,
        "stage_trigger":       None,
        # awaiting_followup is False at the start of every quiz item — the
        # first message is always a Quick-check answer or initial reasoning,
        # never a follow-up. _stream_teach sets it to True after a teach.
        "awaiting_followup":   False,
        "last_diag":           None,
        # Vestigial multi-concept state (still tracked for the diagnosis
        # picker, but no longer drives back-and-forth probes).
        "concepts_done":            [],
        "current_focus_concept":    None,
        "_pivot_depth":             0,
        "bridge_message":           None,
        # Registry-driven turn state — read by _stream_teach to shape the
        # prompt (real mastery, RL action) and by _stream_teach's tail to
        # feed the dynamic KG updater.
        "mastery_now":              mastery_now,
    }

    # Decide on the FIRST belief: probe or teach?
    decision, criterion, target_level, state, diag = _decide_probe_or_teach(state)
    if decision == "probe":
        # Push the user bubble so the conversation shows what the student wrote,
        # then surface the probe panel with the targeted question.
        # If a multi-concept pivot happened during decide(), surface the
        # bridge message in its OWN assistant bubble so the student sees
        # "Now let's look at X" before the next probe question.
        bridge = state.pop("bridge_message", None)
        history = list(history) + [
            {"role": "user", "content": state["user_bubble"]},
        ]
        if bridge:
            history.append({"role": "assistant", "content": bridge})
        history.append({
            "role": "assistant",
            "content": _probe_question_md(
                 criterion, target_level, state["probe_count"], CHAT_MAX_PROBES,
                 depth_text=state.get("pending_probe_text"),
                 depth_reason=state.get("pending_probe_reason"),
                 concept_id=state.get("pending_concept_id"),
                 facet_pos=state.get("pending_facet_pos"),
                 facet_total=state.get("pending_facet_total"),
             ),
        })
        enriched = _status_pill_with_diag(
            state, diag,
            status_template + "  ·  *quick check before the answer…*",
        )
        yield (history,
               gr.update(value=enriched, visible=True),
               gr.update(visible=True),
               _probe_question_md(
                   criterion, target_level, state["probe_count"], CHAT_MAX_PROBES,
                   depth_text=state.get("pending_probe_text"),
                   depth_reason=state.get("pending_probe_reason"),
                   concept_id=state.get("pending_concept_id"),
                   facet_pos=state.get("pending_facet_pos"),
                   facet_total=state.get("pending_facet_total"),
               ),
               "",
               state)
        return

    # Otherwise stream the full teach reply.
    yield from _stream_teach(state, diag, history)


_MISCONCEPTION_QUOTE_RE = re.compile(
    # "You wrote" (optionally with colon) followed by an opening quote
    # marker — single, double, smart-quote, or markdown-bold-italic wrap
    # — then the candidate quote, then a matching closing quote marker.
    r"You wrote\s*[:]?\s*"
    r"(?:\*+\s*[‘'\"]|[‘'\"])"
    r"(?P<quote>[^*\"‘’']{6,400}?)"
    r"(?:[’'\"]\s*\*+|[’'\"])",
    re.IGNORECASE,
)
_WS_RE = re.compile(r"\s+")


def _sanitise_misconception_quote(reply_text: str, student_text: str) -> str:
    """Catch LLM-fabricated misconception quotes.

    The COMPREHENSIVE MODE prompt demands the misconception section quote
    the student verbatim, but llama3.x sometimes paraphrases the wrong-
    belief catalogue entry and puts THAT inside quote marks instead —
    pretending the student wrote it. That's worse than no quote: it
    misattributes a sentence the student didn't write.

    This validator scans the LLM reply for `You wrote "X"` (or `*'X'*`)
    patterns and checks whether X is a contiguous substring of the
    student's actual reasoning (whitespace + case + trailing-punctuation
    tolerant). If X is genuine, it's left alone. If X is fabricated, the
    attribution is rewritten to an honest "you didn't say this in so many
    words, but your answer implies it" — so the following "— precise
    version: ..." still reads naturally.

    Idempotent. Safe on text with no misconception section.
    """
    if not reply_text or not student_text:
        return reply_text
    student_norm = _WS_RE.sub(" ", student_text.lower()).strip()
    if not student_norm:
        return reply_text

    def _is_verbatim(quote: str) -> bool:
        q = _WS_RE.sub(" ", quote.lower()).strip().strip(".;:!?\"'")
        if len(q) < 8:
            # Too short to be a meaningful fabrication risk — let it pass.
            return True
        if q in student_norm:
            return True
        # Tolerate trailing-fragment edits (LLM dropped a final word).
        if len(q) > 30 and q[:-10] in student_norm:
            return True
        return False

    def _replace(m: "re.Match") -> str:
        if _is_verbatim(m.group("quote")):
            return m.group(0)
        # Fabricated — rewrite the attribution prefix. The text after the
        # match (typically "— precise version: ...") remains intact and
        # reads cleanly after this honest opener.
        return ("You didn't say this in so many words, but your answer "
                "treats it as if it were true")

    return _MISCONCEPTION_QUOTE_RE.sub(_replace, reply_text)


def _stream_teach(state, diag, history):
    """Stream the LLM tutor reply using the accumulated belief in `state`.
    Outputs the 6-tuple shape stream_response uses so Gradio reconciles it
    with the same set of outputs."""
    q = QUIZ_BY_ID[state["quiz_id"]]
    correct        = state["is_correct"]
    picked_letter  = state["picked_letter"]
    picked_text    = state["picked_text"]
    status_template = state["status_template"]
    reasoning      = state["accumulated_belief"]

    # Append user bubble + assistant placeholder. Skip user bubble if we
    # already appended it during a prior probe round.
    thinking_placeholder = (
        '<span style="color:#64748b; font-style:italic;">'
        'Tutor is thinking…</span>'
    )
    already_has_user = (history and history[-1].get("role") == "assistant"
                        and "Quick check" in (history[-1].get("content") or ""))
    if already_has_user:
        # Last turn was a probe — replace the probe question with the typing
        # indicator and add a fresh user bubble for the probe answer trail.
        history = list(history[:-1]) + [
            {"role": "user",
             "content": f"*(probe answers so far)* {reasoning}"},
            {"role": "assistant", "content": thinking_placeholder},
        ]
    else:
        history = list(history) + [
            {"role": "user", "content": state["user_bubble"]},
            {"role": "assistant", "content": thinking_placeholder},
        ]

    # Ongoing-chat mode: keep the chat panel VISIBLE through every teach
    # reply (was visible=False = hide-after-teach in the old one-shot mode).
    # The student can keep messaging until they start a new quiz.
    enriched = _status_pill_with_diag(state, diag, status_template)
    yield (history,
           gr.update(value=enriched, visible=True),
           gr.update(visible=True), "", "", state)

    # Intervention via LP-validity gate (static LP filter — preserved)
    # then refined by the trained RL teaching agent if it picks a different
    # type that still passes the LP gate.
    cands = [("transfer_task", 0.92), ("worked_example", 0.80),
             ("socratic_prompt", 0.70), ("trace_scaffold", 0.65)]
    filt = filter_interventions_by_lp(cands, diag["current_lp_level"])
    chosen = filt[0][0] if filt else "worked_example"
    dina_now = float((state.get("mastery_now") or {}).get(
        "dina_mastery", 0.30))
    bkt_now  = float((state.get("mastery_now") or {}).get(
        "bkt_mastery", dina_now))
    emotion_now = "confused" if not correct else "engaged"
    # Re-encode the student's accumulated belief with HVSAE so the RL agent
    # gets a real latent (matches what get_state_representation expects).
    try:
        latent_for_rl, _mp = _hvsae_forward(reasoning)
        latent_for_rl = latent_for_rl.squeeze(0)
    except Exception:
        latent_for_rl = None

    # CLOSE the PREVIOUS RL step first (if there is one) — compute reward
    # from the delta between then and now, push (s, a, r, s') into the
    # replay buffer, run one DQN update. This is what turns "RL inference"
    # into "RL learning" inside the chat.
    _curr_state_vec = None
    try:
        if REG.teaching_rl_agent is not None and latent_for_rl is not None:
            _sd_tmp = {"student_id": "chat_user",
                        "time_stuck": 0.0, "action_sequence": []}
            _an_tmp = {
                "encoding":   {"latent": latent_for_rl.detach().view(-1).float()},
                "cognitive":  {"knowledge_gaps":
                                [{"concept": q["concept"], "mastery": dina_now}]},
                "behavioral": {"emotional_state": emotion_now},
                "psychological": {"personality": {}},
                "history":    {"interventions": []},
            }
            _curr_state_vec = REG.teaching_rl_agent.get_state_representation(
                _sd_tmp, _an_tmp)
    except Exception:
        _curr_state_vec = None
    # engagement_signal = 1.0 if student wrote a substantive reasoning,
    # 0.3 if "i dont know"-style. Length is a coarse proxy.
    _eng = 0.7 if len((reasoning or "").split()) >= 8 else 0.3
    _rl_finalise_previous(state, current_dina=dina_now,
                          current_emotion=emotion_now,
                          current_lp=diag["current_lp_level"],
                          current_state_vec=_curr_state_vec,
                          engagement_signal=_eng)

    rl_action, rl_action_id, rl_q, rl_state_vec = _rl_recommended_intervention(
        "chat_user", q["concept"],
        mastery=dina_now, emotion=emotion_now,
        lp_level=diag["current_lp_level"],
        hvsae_latent=latent_for_rl,
    )
    rl_valid = {t for t, _ in filt}
    if rl_action in rl_valid:
        chosen = rl_action
    # Stash for NEXT turn's _rl_finalise_previous (so we learn from this
    # action's outcome).
    state["pending_rl"] = {
        "state_vec": rl_state_vec, "action_id": rl_action_id,
        "dina": dina_now, "emotion": emotion_now,
        "lp_level": diag["current_lp_level"],
    }
    state["last_rl_action"] = rl_action
    state["last_rl_q"]      = rl_q
    print(f"[CPAL/Teach-RL] action={rl_action} (id={rl_action_id}) "
          f"q={rl_q:+.3f} lp={diag['current_lp_level']} dina={dina_now:.2f}",
          flush=True)

    # ── Build the session_data dict the registry components expect ──────
    # Used by analyse_prompt (3-channel), infer_theory_of_mind (COKE),
    # and diagnose_multi (LP-Multi). Same shape the orchestrator uses.
    session_data_for_ctx = {
        "student_id": "chat_user",
        "question":   reasoning,
        "code":       q["code"],
        "error_message": "",
        "conversation": [{"role": "user", "content": reasoning}],
        "action_sequence": [],
        "time_stuck": 0.0,
    }

    # ── Populate the analysis dict so the generator's KNOWLEDGE GRAPHS
    #    (MUST REFERENCE) section + 3-channel block fire with real data.
    cse_kg_block        = _build_cse_kg_block(q["concept"])
    pedagogical_kg_block = _build_pedagogical_kg_block(q["concept"])
    coke_block          = _build_coke_block(session_data_for_ctx)
    three_channel_block = _run_three_channel("chat_user", session_data_for_ctx)

    # ── Run multi-concept diagnosis so the LP-Multi mini-replies block
    #    has data when the student touches more than one concept.
    try:
        _latent_for_multi, _mp_for_multi = _hvsae_forward(reasoning)
        _latent_for_multi = _latent_for_multi.squeeze(0)
    except Exception:
        _latent_for_multi, _mp_for_multi = None, None
    lp_diagnostic_multi = _run_diagnose_multi(
        "chat_user", reasoning, session_data_for_ctx,
        hvsae_latent=_latent_for_multi,
        hvsae_misconception_probs=_mp_for_multi,
    )

    print(f"[CPAL/Teach] cse_kg={'OK' if cse_kg_block else 'empty'}  "
          f"ped_kg={'OK' if pedagogical_kg_block else 'empty'}  "
          f"coke={'OK' if coke_block else 'empty'}  "
          f"3ch={'OK' if three_channel_block else 'empty'}  "
          f"lp_multi={len((lp_diagnostic_multi or {}).get('diagnostics', {}))} concepts",
          flush=True)

    student_state = {
        "student_id": "chat_user",
        "lp_diagnostic": diag,
        "lp_diagnostic_multi": lp_diagnostic_multi,
        "recommended_intervention": {"type": chosen, "rl_action": rl_action},
        "personality_profile": {"communication_style": "direct",
                                "learning_preference": "visual"},
        "bkt_mastery":  {q["concept"]: bkt_now},
        "dina_mastery": {q["concept"]: dina_now},
        "emotional_state": emotion_now,
        "interaction_count": len(history) + 1,
    }
    analysis = {
        "emotion": {"primary": "confused" if not correct else "engaged",
                    "confidence": 0.7},
        "knowledge_gaps":  [q["concept"]],
        "cse_kg":          cse_kg_block,
        "pedagogical_kg":  pedagogical_kg_block,
        "coke":            coke_block,
        "psychological_state": three_channel_block,
        "encoding":        {"latent": _latent_for_multi}
                            if _latent_for_multi is not None else {},
    }

    # Build the message the generator sees. When stage_trigger is set we
    # inject COMPREHENSIVE MODE instructions so the generator produces a
    # multi-section synthesis (confirm what student showed → address gaps
    # → walk the full L3 mechanism → transfer question), not just another
    # short probe-style reply.
    stage_trigger = state.get("stage_trigger")
    probed_so_far = state.get("probed_criteria") or []
    # Wrong-belief — pull the SINGLE matched one from the diagnosis. The
    # comprehensive answer addresses THIS belief only, not the RAG top-3
    # candidates (which are FYI context, NOT separate things to teach).
    # Chat-app no longer builds its own comprehensive_header. All LP-grounded
    # prompt construction (LP-1 diagnostic context, LP-2 wrong-model, LP-2b
    # RAG, LP-3 per-level six-step, LP-Multi per-concept mini-replies) lives
    # in src/orchestrator/enhanced_personalized_generator.py:_build_enhanced_prompt
    # and pulls every field it needs from student_state['lp_diagnostic'] (the
    # `diag` dict assigned to student_state below). The INLINE LP RUBRIC
    # rendering instruction is added inside the generator's LP-1 section so
    # the prompt has a single, coherent LP teaching structure (not two
    # competing ones — the duplication was confusing the LLM into honoring
    # neither). Fields the generator reads from diag: current_lp_level,
    # target_lp_level, wrong_model_id/description/origin, matched_signal,
    # expert_benchmark_key_ideas, lp_rubric_current, lp_rubric_target,
    # lp_sub_criteria, plateau_flag, plateau_intervention,
    # diagnostic_confidence, rag_top_wrong_models, rubric_grade.

    # comprehensive_header retired (commit history: 8c88a37 added it,
    # 4d87f99 made it the only mode, today's commit reverts it once the
    # generator's _build_enhanced_prompt was confirmed to cover the same
    # ground via LP-1/LP-2/LP-2b/LP-3/LP-Multi/PROBE MODE sections).
    comprehensive_header = ""
    kg_context = _kg_context_block(
        concept=q["concept"], code=q["code"], error_message="")
    mastery_line = (
        f"DINA mastery on '{q['concept']}': {dina_now:.2f}  |  "
        f"BKT: {bkt_now:.2f}  |  RL-recommended intervention: {rl_action}\n\n"
    )
    tutor_input = (
        f"{comprehensive_header}"
        f"{kg_context}"
        f"{mastery_line}"
        f"Student was given this quiz:\n"
        f"Q: {q['question']}\n\n"
        f"Code:\n```java\n{q['code']}\n```\n\n"
        f"Options:\n" + "\n".join(f"  {k}. {v}" for k, v in q["options"].items()) +
        f"\n\nStudent picked {picked_letter}: {picked_text}\n"
        f"Correct answer is {q['correct_answer']}: "
        f"{q['options'][q['correct_answer']]}\n"
        f"Student was {'CORRECT' if correct else 'INCORRECT'}.\n\n"
        f"Student's accumulated reasoning across the chat:\n{reasoning}"
    )

    buffer = {"text": ""}
    def on_chunk(piece):
        buffer["text"] += piece

    import threading, time
    done = {"flag": False, "err": None}

    def runner():
        try:
            GEN._stream_callback = on_chunk
            GEN.generate_personalized_response(
                student_id="chat_user",
                student_message=tutor_input,
                student_state=student_state,
                analysis=analysis,
                code=q["code"],
            )
        except Exception as e:
            done["err"] = str(e)
        finally:
            done["flag"] = True

    t = threading.Thread(target=runner, daemon=True)
    t.start()

    typing_enriched = _status_pill_with_diag(
        state, diag, status_template + "  ·  *tutor is typing…*",
    )
    last_len = 0
    while not done["flag"]:
        time.sleep(0.15)
        if len(buffer["text"]) > last_len:
            last_len = len(buffer["text"])
            history[-1]["content"] = buffer["text"]
            yield (history,
                   gr.update(value=typing_enriched, visible=True),
                   gr.update(visible=True), "", "", state)

    if done["err"]:
        history[-1]["content"] = f"❌ Generation failed: {done['err']}"
    else:
        final_text = buffer["text"] or "(empty response)"
        # Post-generation guardrail — catch fabricated misconception
        # quotes the LLM still produces despite the prompt rule.
        final_text = _sanitise_misconception_quote(
            final_text, state.get("accumulated_belief") or ""
        )
        history[-1]["content"] = final_text

    # Multi-probe RE-ENABLED. After a comprehensive synthesis, the next
    # follow-up turn re-runs the diagnostic on the accumulated belief and
    # may either probe again (if confidence dropped) or land in another
    # synthesis. Don't pin force_comprehensive=True any more — let
    # _stage_reached decide each turn from real diagnostic confidence.
    state["force_comprehensive"] = False
    state["stage_trigger"]       = None
    # Mark that the next student message is a free-form follow-up, not a
    # probe answer. on_probe_answer reads this and routes to
    # _stream_followup (which doesn't re-diagnose against the LP rubric
    # and doesn't re-fire the probe ladder — it just answers the question
    # using the chat history as context).
    state["awaiting_followup"] = True
    # Stash the diagnostic so _stream_followup can reference the wrong-model
    # + LP level without re-running diagnose() on every follow-up turn.
    state["last_diag"] = diag

    # Feed this turn's outcome into the dynamic KG updater so prerequisite
    # strengths, misconception frequencies, and intervention effectiveness
    # accumulate across sessions.
    _dynamic_kg_learn("chat_user", q["concept"], correct,
                      intervention_type=chosen)

    enriched_final = _status_pill_with_diag(state, diag, status_template)
    yield (history,
           gr.update(value=enriched_final, visible=True),
           gr.update(visible=True), "", "", state)


def on_reveal_answer(history, state):
    """Force the comprehensive synthesis on the next turn, regardless of
    confidence or remaining probe budget. Sets the force flag and routes
    through _decide_probe_or_teach — which returns ('teach', ...) when
    force_comprehensive is set, taking the comprehensive branch in
    _stream_teach."""
    if not state or not state.get("quiz_id"):
        yield (history,
               gr.update(value="(no active question — submit your reasoning first)",
                          visible=True),
               gr.update(visible=False), "", "", state)
        return
    state["force_comprehensive"] = True
    # Re-decide with the force flag — will land in the teach branch with
    # stage_trigger="force".
    decision, criterion, target_level, state, diag = _decide_probe_or_teach(state)
    # decision is always "teach" when force_comprehensive is True.
    yield from _stream_teach(state, diag, history)


_FOLLOWUP_OLLAMA_URL = "http://localhost:11434/api/generate"

# Map every RL teaching-agent action to a follow-up-specific reply shape.
# These are the actions in TeachingRLAgent.actions (0-9). The trained
# policy picks one per turn; the matching instruction here shapes the
# follow-up reply so the policy's decision affects what the student
# actually sees, not just an internal log line.
_RL_ACTION_SHAPING = {
    "visual_explanation":  ("Include a small ASCII diagram or visual "
                             "layout (memory cells, stack/heap, control "
                             "flow) so the answer is partly visual."),
    "guided_practice":     ("Walk through the answer in clearly numbered "
                             "1-2-3 steps; pause after the key step with "
                             "\"so far, are you with me?\"-style framing."),
    "interactive_exercise":("Ask the student to predict / trace ONE small "
                             "concrete thing before giving the full answer "
                             "— turn it into a mini-exchange."),
    "conceptual_deepdive": ("Go deeper on the WHY: name the underlying "
                             "Java language design principle and connect "
                             "it to the broader concept family."),
    "motivational_support":("Open with one sentence acknowledging the "
                             "specific thing the student got right in "
                             "the prior turn, then answer the question."),
    "worked_example":      ("Show a short Java code snippet (5-10 lines) "
                             "that directly answers the question; "
                             "annotate the load-bearing line."),
    "peer_comparison":     ("Frame as \"a common student belief is X, but "
                             "actually Y\" — name the misconception, then "
                             "correct it."),
    "spaced_review":       ("Briefly recap the key mechanism from the "
                             "previous turn (one sentence) before "
                             "answering, so the student's working memory "
                             "is loaded."),
    "challenge_problem":   ("After answering the question in 2 sentences, "
                             "raise the bar with one harder variant or "
                             "edge case for the student to think about."),
    "error_analysis":      ("Address the question by walking through what "
                             "would go wrong if the student's intuition "
                             "were applied — then show the correct path."),
}


def _stream_followup(state, history, question):
    """Stream a focused reply to a free-form follow-up question after the
    comprehensive teach turn has fired. The reply is shaped by:

      * the trained RL teaching agent's chosen action (10 actions; the
        policy was trained over 8138 prior teaching steps),
      * current DINA + BKT mastery (re-fetched per turn — they don't
        change on a follow-up but the values shape tone/depth),
      * the LP diagnostic stashed from the previous teach turn (current
        level, target level, matched wrong-model, target sub-criteria —
        no re-diagnosis runs on a follow-up because the rubric is for
        graded answers, not free-form questions),
      * pedagogical KG misconceptions + CSE-KG related concepts via
        the registry's _kg_context_block helper.

    Output goes through a direct Ollama stream (not the EnhancedPersonal-
    izedGenerator's heavy LP-3 template — that fires once per teach turn,
    not per follow-up).
    """
    import json, threading, time as _time
    import requests as _req
    import torch as _torch

    q = QUIZ_BY_ID.get(state.get("quiz_id")) or {}
    concept = q.get("concept", "this concept")
    friendly = _friendly_concept(concept)
    code = q.get("code", "")
    diag = state.get("last_diag") or {}
    wm_id   = diag.get("wrong_model_id") or ""
    wm_desc = diag.get("wrong_model_description") or ""
    cur_lvl = diag.get("current_lp_level") or "L1"
    tgt_lvl = diag.get("target_lp_level") or "L3"
    sub_target = (diag.get("lp_sub_criteria") or {}).get(tgt_lvl) or []
    diag_conf  = float(diag.get("diagnostic_confidence", 0.0))
    benchmark = "; ".join(diag.get("expert_benchmark_key_ideas") or [])

    # Per-turn mastery refresh (mastery may have updated since the teach
    # turn if any quiz answers happened in between — defensive read).
    try:
        dina_dict = REG.dina.get_mastery("chat_user", concept) or {}
        dina_now = float(dina_dict.get(concept, 0.30))
    except Exception:
        dina_now = 0.30
    try:
        bkt_state = REG.bkt.get_student_knowledge_state("chat_user") or {}
        bkt_now = float(bkt_state.get(concept, dina_now))
    except Exception:
        bkt_now = dina_now

    # RL action selection — use HVSAE latent of the follow-up question
    # text so the policy sees this turn's content, not a stale latent.
    try:
        latent_for_rl, _mp = _hvsae_forward(question)
        latent_for_rl = latent_for_rl.squeeze(0)
    except Exception:
        latent_for_rl = None
    # Emotion proxy: low mastery + a "why doesn't this work" style
    # question implies frustration; high mastery + a probing question
    # implies engagement.
    emotion = "confused" if dina_now < 0.4 else "engaged"

    # CLOSE the previous RL step (the teach turn's action). engagement_signal
    # is high here because the student took the trouble to ask a follow-up
    # rather than abandoning the chat.
    _curr_state_vec_fu = None
    try:
        if REG.teaching_rl_agent is not None and latent_for_rl is not None:
            _sd_tmp = {"student_id": "chat_user",
                        "time_stuck": 0.0, "action_sequence": []}
            _an_tmp = {
                "encoding":   {"latent": latent_for_rl.detach().view(-1).float()},
                "cognitive":  {"knowledge_gaps":
                                [{"concept": concept, "mastery": dina_now}]},
                "behavioral": {"emotional_state": emotion},
                "psychological": {"personality": {}},
                "history":    {"interventions": []},
            }
            _curr_state_vec_fu = REG.teaching_rl_agent.get_state_representation(
                _sd_tmp, _an_tmp)
    except Exception:
        _curr_state_vec_fu = None
    _rl_finalise_previous(state, current_dina=dina_now,
                          current_emotion=emotion, current_lp=cur_lvl,
                          current_state_vec=_curr_state_vec_fu,
                          engagement_signal=0.85)

    rl_action, rl_action_id, rl_q, rl_state_vec = _rl_recommended_intervention(
        "chat_user", concept,
        mastery=dina_now, emotion=emotion, lp_level=cur_lvl,
        hvsae_latent=latent_for_rl,
    )
    action_shape = _RL_ACTION_SHAPING.get(
        rl_action,
        "Reply directly to the question in 3-6 sentences.")
    # Stash for the NEXT turn's _rl_finalise_previous.
    state["pending_rl"] = {
        "state_vec": rl_state_vec, "action_id": rl_action_id,
        "dina": dina_now, "emotion": emotion, "lp_level": cur_lvl,
    }
    state["last_rl_action"] = rl_action
    state["last_rl_q"]      = rl_q
    print(f"[CPAL/Followup] concept={concept} lp={cur_lvl}->{tgt_lvl} "
          f"dina={dina_now:.2f} bkt={bkt_now:.2f} emotion={emotion} "
          f"rl_action={rl_action} q={rl_q:+.3f}", flush=True)

    # KG-grounded context (pedagogical KG + CSE-KG + error mapper).
    kg_context = _kg_context_block(
        concept=concept, code=code, error_message="")

    # Trim chat history to the most recent exchanges so the prompt stays
    # within the model's effective window. Strip the user_bubble markdown
    # framing so the model sees clean conversational text.
    convo_lines = []
    for msg in (history or [])[-10:]:
        role = msg.get("role", "")
        content = (msg.get("content") or "").strip()
        if not content:
            continue
        if role == "user" and "**My reasoning:**" in content:
            content = content.split("**My reasoning:**", 1)[1].strip()
        convo_lines.append(
            f"{'Student' if role == 'user' else 'Tutor'}: {content[:1200]}")
    convo_text = "\n\n".join(convo_lines)

    wb_line = ""
    if wm_id and wm_desc:
        wb_line = (
            f"Earlier diagnosed wrong-belief (refer to it only if the "
            f"follow-up relates): id={wm_id} — {wm_desc[:160]}\n")
    sub_line = ""
    if sub_target:
        sub_line = (
            f"Target-level ({tgt_lvl}) facets the student still needs to "
            f"demonstrate: " + "; ".join(c.strip().rstrip(".")
                                          for c in sub_target[:4]) + "\n")
    conf_line = ""
    if diag_conf:
        hedge = ("  (LOW diagnostic confidence — soften assertions; "
                  "invite the student to push back)") if diag_conf < 0.5 else ""
        conf_line = f"Diagnostic confidence: {diag_conf:.2f}{hedge}\n"

    followup_prompt = (
        f"You are the Java tutor in an ongoing conversation about "
        f"'{friendly}'. The student already received the comprehensive "
        f"teach reply and is now asking a follow-up.\n\n"
        f"=== STUDENT STATE (use to shape depth/tone, don't recite) ===\n"
        f"LP level: {cur_lvl} → target {tgt_lvl}\n"
        f"DINA mastery on '{concept}': {dina_now:.2f}  |  BKT: {bkt_now:.2f}\n"
        f"{conf_line}"
        f"{wb_line}"
        f"{sub_line}"
        + (f"L3 expert benchmark (anchor): {benchmark}\n" if benchmark else "")
        + (f"\n{kg_context}" if kg_context else "")
        + f"\n=== RL TEACHING-AGENT DECISION (FOLLOW THIS SHAPE) ===\n"
        f"Action chosen by the trained RL policy: **{rl_action}**\n"
        f"Reply shape required by this action: {action_shape}\n\n"
        f"=== RECENT CONVERSATION (most recent at the bottom) ===\n"
        f"{convo_text}\n\n"
        f"=== STUDENT'S NEW FOLLOW-UP MESSAGE ===\n"
        f"{question}\n\n"
        f"=== HOW TO REPLY ===\n"
        f"- Answer the follow-up directly. Do NOT restart the lesson.\n"
        f"- Honor the RL-chosen reply shape above.\n"
        f"- Match the depth of the question — short questions get short "
        f"answers (2-4 sentences); 'show me' questions get a small code "
        f"snippet; 'why' questions get the underlying reason.\n"
        f"- If the question is off-topic, gently redirect back to "
        f"'{friendly}' in one sentence then answer.\n"
        f"- If the student's mastery is below 0.40, prefer one concrete "
        f"example over abstract principle. Above 0.70, you can name the "
        f"design rationale and skip the basics.\n"
    )

    # Push user bubble + thinking placeholder
    thinking = ('<span style="color:#64748b; font-style:italic;">'
                'Tutor is thinking…</span>')
    history = list(history) + [
        {"role": "user",       "content": question},
        {"role": "assistant",  "content": thinking},
    ]
    enriched = _status_pill_with_diag(
        state, state.get("last_diag") or {},
        state.get("status_template", "") + "  ·  *tutor is typing…*",
    )
    yield (history,
           gr.update(value=enriched, visible=True),
           gr.update(visible=True), "", "", state)

    # Stream via direct Ollama call (skip EnhancedPersonalizedGenerator's
    # heavy LP-3 template — this is post-teach Q&A, not a teach turn).
    buf = {"text": "", "err": None, "done": False}
    model = (os.environ.get("CPAL_OLLAMA_MODEL")
             or getattr(GEN, "_ollama_model", None)
             or "llama3.1:8b")

    def _runner():
        try:
            r = _req.post(
                _FOLLOWUP_OLLAMA_URL,
                json={"model": model, "prompt": followup_prompt,
                       "stream": True,
                       "options": {"temperature": 0.6,
                                    "num_predict": 600}},
                stream=True, timeout=120,
            )
            r.raise_for_status()
            for line in r.iter_lines(decode_unicode=True):
                if not line:
                    continue
                try:
                    chunk = json.loads(line)
                except Exception:
                    continue
                piece = chunk.get("response", "")
                if piece:
                    buf["text"] += piece
                if chunk.get("done"):
                    break
        except Exception as e:
            buf["err"] = str(e)
        finally:
            buf["done"] = True

    t = threading.Thread(target=_runner, daemon=True)
    t.start()
    last_len = 0
    while not buf["done"]:
        _time.sleep(0.15)
        if len(buf["text"]) > last_len:
            last_len = len(buf["text"])
            history[-1]["content"] = buf["text"]
            yield (history,
                   gr.update(value=enriched, visible=True),
                   gr.update(visible=True), "", "", state)

    if buf["err"]:
        history[-1]["content"] = f"❌ Follow-up generation failed: {buf['err']}"
    else:
        history[-1]["content"] = buf["text"] or "(empty response)"

    # Chain: the next student message is also a follow-up.
    state["awaiting_followup"] = True
    final_enriched = _status_pill_with_diag(
        state, state.get("last_diag") or {}, state.get("status_template", ""))
    yield (history,
           gr.update(value=final_enriched, visible=True),
           gr.update(visible=True), "", "", state)


def on_probe_answer(probe_answer, history, state):
    """Two-mode handler:
      (a) If state.awaiting_followup is True (set after a teach turn), the
          student's message is treated as a free-form follow-up — route to
          _stream_followup which answers the question using chat history
          as context (no LP re-diagnosis, no probe ladder).
      (b) Otherwise the student is in the multi-turn probe ladder and the
          message is graded as a Quick-check answer — re-diagnose, then
          either probe again or fire the teach reply.
    """
    if not state or not state.get("quiz_id"):
        yield (history, gr.update(value="(no active question)", visible=True),
               gr.update(visible=False), "", "", state)
        return
    ans = (probe_answer or "").strip()
    if not ans:
        yield (history, gr.update(value="⚠️ Write a message before sending.",
                                   visible=True),
               gr.update(visible=True),    # keep panel visible
               "",                          # don't overwrite
               "",                          # clear input
               state)
        return

    # Mode (a) — free-form follow-up after the comprehensive teach turn.
    if state.get("awaiting_followup"):
        # Reset the flag immediately so a follow-up that itself triggers
        # another follow-up doesn't recurse on stale state. _stream_followup
        # sets awaiting_followup=True again at the end of a successful turn.
        state["awaiting_followup"] = False
        yield from _stream_followup(state, history, ans)
        return

    # Mode (b) — Quick-check answer in the probe ladder. Existing behavior.
    # Append the probe answer to accumulated belief.
    state["accumulated_belief"] = (
        (state["accumulated_belief"] + "  " + ans).strip()
    )

    decision, criterion, target_level, state, diag = _decide_probe_or_teach(state)
    if decision == "probe":
        # Replace the last assistant bubble (the previous probe question)
        # with the next probe question.
        next_q_md = _probe_question_md(
            criterion, target_level, state["probe_count"], CHAT_MAX_PROBES,
            depth_text=state.get("pending_probe_text"),
            depth_reason=state.get("pending_probe_reason"),
            concept_id=state.get("pending_concept_id"),
            facet_pos=state.get("pending_facet_pos"),
            facet_total=state.get("pending_facet_total"),
        )
        # Multi-concept pivot bridge — surfaced before the next probe so
        # the student sees the transition between concepts in the chat.
        bridge_in_answer = state.pop("bridge_message", None)
        if bridge_in_answer:
            next_q_md = f"{bridge_in_answer}\n\n{next_q_md}"
        if history and history[-1].get("role") == "assistant":
            history = list(history[:-1]) + [
                {"role": "user",  "content": f"*(quick-check answer)* {ans}"},
                {"role": "assistant", "content": next_q_md},
            ]
        else:
            history = list(history) + [
                {"role": "user",  "content": f"*(quick-check answer)* {ans}"},
                {"role": "assistant", "content": next_q_md},
            ]
        yield (history,
               gr.update(value=state["status_template"]
                                + "  ·  *one more check before the answer…*",
                          visible=True),
               gr.update(visible=True),
               next_q_md, "", state)
        return

    # Teach — stream the full reply using the accumulated belief.
    yield from _stream_teach(state, diag, history)


def clear_chat():
    # Resets the chat state and hides the chat input panel until the
    # student submits initial reasoning again.
    empty_state = {
        "quiz_id": None, "picked_option_full": None, "picked_letter": None,
        "picked_text": None, "is_correct": False, "status_template": "",
        "accumulated_belief": "", "probe_count": 0, "probed_criteria": [],
        "user_bubble": "",
        # Dynamic-chat + multi-concept additions
        "pending_probe_text": None, "pending_probe_reason": None,
        "force_comprehensive": False, "stage_trigger": None,
        "concepts_done": [], "current_focus_concept": None,
        "_pivot_depth": 0, "bridge_message": None,
        "awaiting_followup": False, "last_diag": None,
    }
    return ([], gr.update(value="", visible=False),
            gr.update(visible=False), "", "", empty_state)


# =========================================================================
# UI
# =========================================================================
def build_app():
    with gr.Blocks(
        title="CPAL Tutor",
        theme=gr.themes.Soft(primary_hue="indigo", neutral_hue="slate"),
        css="""
        .gradio-container { max-width: 900px !important; margin: 0 auto !important; }
        .quiz-card  { background: transparent !important;
                      border: none !important; padding: 4px 0 !important; }
        .quiz-card p           { margin: 4px 0 !important; }
        .quiz-card pre         { margin: 6px 0 2px !important; }
        .quiz-card h1, .quiz-card h2, .quiz-card h3, .quiz-card h4 {
            margin: 0 0 6px !important;
        }

        /* ───── Kill the white code-block background EVERYWHERE ───── */
        /* Cover every wrapper Gradio / Prism may put around a code block:
           the <pre>, the <code> child, any div with code/codeblock/highlight
           in its class, and every descendant element. */
        .gradio-container pre,
        .gradio-container pre *,
        .gradio-container code,
        .gradio-container pre code,
        .gradio-container [class*="code"],
        .gradio-container [class*="codeblock"],
        .gradio-container [class*="code-block"],
        .gradio-container [class*="highlight"],
        .gradio-container .md pre,
        .gradio-container .md pre *,
        .gradio-container .message pre,
        .gradio-container .message pre *,
        .quiz-card pre,
        .quiz-card pre * {
            background: #1e293b !important;
            background-color: #1e293b !important;
            color: #f1f5f9 !important;
        }
        /* Outer pre keeps padding + rounded border; inner spans/code stay flat */
        .gradio-container pre {
            border: 1px solid #334155 !important;
            border-radius: 8px !important;
            padding: 12px !important;
        }
        .gradio-container pre code,
        .gradio-container pre code * {
            background: transparent !important;
            background-color: transparent !important;
        }

        /* The "picked option" line that sits with the code snippet */
        .picked-option {
            display: block;
            background: #1e293b;
            color: #ffffff;
            font-style: italic;
            padding: 8px 12px;
            border-radius: 0 0 8px 8px;
            margin-top: -2px;
            border: 1px solid #334155;
            border-top: none;
        }
        .status-pill { padding: 10px 14px; border-radius: 8px;
                       background: #eef2ff; border: 1px solid #c7d2fe;
                       font-size: 14px; }
        .status-pill p { margin: 0 !important; }
        .hero h1 { margin-bottom: 4px; }
        .hero p  { color: #4b5563; margin-top: 0; }

        /* ───── Kill the white "generating" overlay flash ─────
           Gradio shows a translucent white loading layer over the chatbot
           while a function is running. That's the white patch with no text.
           Hide every loader / progress / status indicator. */
        .gradio-container .progress,
        .gradio-container .progress-bar,
        .gradio-container .progress-text,
        .gradio-container .status,
        .gradio-container [class*="status-tracker"],
        .gradio-container [class*="generating"],
        .gradio-container [class*="loading"],
        .gradio-container .eta-bar,
        .gradio-container [data-testid="progress"] {
            display: none !important;
        }
        /* Make sure the chatbot frame itself is transparent, not white */
        .gradio-container .chatbot { background: transparent !important; }
        """,
    ) as app:
        gr.Markdown(
            """
            <div class="hero">

            # 🎓 CPAL Tutor

            Your personalized Java learning assistant. Pick a quiz, share your
            thinking, and get a tailored explanation.

            </div>
            """
        )

        quiz_dd = gr.Dropdown(
            choices=QUIZ_CHOICES,
            value=QUIZ_CHOICES[0][1],
            label="📝 Choose a quiz",
            interactive=True,
        )
        quiz_card = gr.Markdown("", elem_classes=["quiz-card"])
        option_radio = gr.Radio(
            choices=[],
            label="Your answer",
            interactive=True,
        )
        reasoning_box = gr.Textbox(
            label="Why did you pick that?",
            lines=3,
            placeholder="Tell the tutor what made you choose this answer…",
        )
        with gr.Row():
            submit_btn = gr.Button("Get tutor response  →",
                                    variant="primary", scale=3)
            clear_btn  = gr.Button("Clear chat", scale=1)
        status = gr.Markdown("", elem_classes=["status-pill"], visible=False)

        # Ongoing chat panel — hidden until first submit, then always
        # visible. Multi-turn probing is OFF, so this is now purely a
        # follow-up-question chat. Student-facing status (plain language,
        # no L1-L4 jargon) is in the `status` pill above; the geeky
        # internals (raw LP, conf) sit inside the collapsible details
        # panel below so engineers/researchers can still inspect them.
        with gr.Group(visible=False) as probe_panel:
            # Multi-probe RE-ENABLED — probe_question_md shows the current
            # Quick-check question above the input. Handlers fill it via
            # gr.update(value=..., visible=True) when a probe fires.
            probe_question_md = gr.Markdown("", visible=True)
            probe_input = gr.Textbox(
                label="Ask the tutor a follow-up",
                lines=3,
                placeholder=("Answer the Quick-check above, or ask anything — "
                             "\"why does Java do that?\", "
                             "\"can you give another example?\", "
                             "paste more code, etc."),
            )
            with gr.Row():
                probe_submit_btn = gr.Button("Send  →", variant="primary",
                                              scale=4)
                # Multi-probe back on — reveal_btn lets the student jump
                # straight to the comprehensive synthesis (skip remaining
                # Quick-checks). Sets force_comprehensive=True and routes
                # through _decide_probe_or_teach → teach branch.
                reveal_btn = gr.Button("Reveal full answer", scale=1,
                                       visible=True)

        chatbot = gr.Chatbot(
            label="Your tutor",
            type="messages",
            height=560,
            show_copy_button=True,
            avatar_images=(None, None),
        )

        # Ongoing-chat state — accumulated belief grows with every turn;
        # multi-probe RE-ENABLED so probed_criteria/probe_count are live;
        # force_comprehensive defaults False (each turn re-decides).
        probe_state = gr.State({
            "quiz_id": None, "picked_option_full": None, "picked_letter": None,
            "picked_text": None, "is_correct": False, "status_template": "",
            "accumulated_belief": "", "probe_count": 0, "probed_criteria": [],
            "user_bubble": "",
            "pending_probe_text": None, "pending_probe_reason": None,
            "force_comprehensive": False, "stage_trigger": None,
            "concepts_done": [], "current_focus_concept": None,
            "_pivot_depth": 0, "bridge_message": None,
            "awaiting_followup": False, "last_diag": None,
        })

        # Populate quiz card on load + on dropdown change.
        # show_progress="hidden" kills Gradio's white loading overlay so the
        # UI doesn't flash white while these events run.
        app.load(on_select_quiz, inputs=[quiz_dd],
                 outputs=[quiz_card, reasoning_box, option_radio, status],
                 show_progress="hidden")
        quiz_dd.change(on_select_quiz, inputs=[quiz_dd],
                       outputs=[quiz_card, reasoning_box, option_radio, status],
                       show_progress="hidden")

        # When the user picks an option, re-render the card to overlay the
        # picked option in white italic right under the code snippet.
        option_radio.change(on_pick_option,
                            inputs=[quiz_dd, option_radio],
                            outputs=[quiz_card],
                            show_progress="hidden")

        # Submit — initial belief. Either fires a probe (shows probe_panel)
        # or streams the tutor reply. The 6-tuple output reconciles
        # chatbot/status/probe_panel/probe_question_md/probe_input/state.
        submit_btn.click(
            stream_response,
            inputs=[quiz_dd, option_radio, reasoning_box, chatbot, probe_state],
            outputs=[chatbot, status, probe_panel, probe_question_md,
                     probe_input, probe_state],
            show_progress="hidden",
        )

        # Probe answer / chat message — appends to accumulated belief,
        # re-decides. After the first submit this becomes the persistent
        # chat input; works for both probe rounds and post-comprehensive
        # follow-ups.
        probe_submit_btn.click(
            on_probe_answer,
            inputs=[probe_input, chatbot, probe_state],
            outputs=[chatbot, status, probe_panel, probe_question_md,
                     probe_input, probe_state],
            show_progress="hidden",
        )

        # Reveal full answer — skips remaining probes and produces the
        # comprehensive synthesis on the next turn.
        reveal_btn.click(
            on_reveal_answer,
            inputs=[chatbot, probe_state],
            outputs=[chatbot, status, probe_panel, probe_question_md,
                     probe_input, probe_state],
            show_progress="hidden",
        )

        clear_btn.click(
            clear_chat, None,
            [chatbot, status, probe_panel, probe_question_md,
             probe_input, probe_state],
            show_progress="hidden",
        )

    return app


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--share", action="store_true",
                        help="expose via gradio.live public URL (72h)")
    parser.add_argument("--port", type=int, default=7860)
    parser.add_argument("--host", default="127.0.0.1")
    args = parser.parse_args()

    app = build_app()
    app.launch(
        server_name=args.host,
        server_port=args.port,
        share=args.share,
    )
