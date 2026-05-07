"""
Proof that LP level actually drives model instruction.

Same student input → forced at L1, L2, L3, L4 in turn. For each we:
  1. Print the LP-1/LP-2/LP-3 sections of the real prompt (so you can
     see the instruction the LLM is told to follow changes by level).
  2. Call Ollama and print the response.

If LP level were decorative, all four responses would look similar.
If LP integration is real, L1 should be surface/example-heavy, L3
should skip re-explanation and push transfer, etc.
"""
import os, sys, copy
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from src.knowledge_graph.mental_models import get_catalogue
from src.orchestrator.lp_diagnostic import LPDiagnostician, filter_interventions_by_lp
from src.orchestrator.enhanced_personalized_generator import EnhancedPersonalizedGenerator


STUDENT_INPUT = (
    "I made two strings with the same text so they should be equal, but "
    "when I use == it returns false. Why isn't it working?"
)
CONCEPT_ID = "string_equality"
STUDENT_ID = "demo_lp_check"


def hr(t=""):
    print("\n" + "=" * 74)
    if t: print(t); print("=" * 74)


def build_prompt_for_level(gen, diag, forced_level, intervention):
    """Build the real prompt by monkey-patching diag's level then invoking
    _build_enhanced_prompt exactly as generate_personalized_response does."""
    diag2 = dict(diag)
    diag2["current_lp_level"] = forced_level
    diag2["target_lp_level"] = {"L1": "L2", "L2": "L3", "L3": "L4", "L4": "L4"}[forced_level]
    diag2["transition"] = f"{forced_level} -> {diag2['target_lp_level']}"

    student_state = {
        "student_id": STUDENT_ID,
        "lp_diagnostic": diag2,
        "recommended_intervention": {"type": intervention},
        "personality_profile": {"communication_style": "direct",
                                 "learning_preference": "visual"},
        "bkt_mastery": {CONCEPT_ID: 0.30},
        "emotional_state": "neutral",
        "interaction_count": 1,
    }
    analysis = {
        "emotion": {"primary": "neutral", "confidence": 0.6},
        "knowledge_gaps": [CONCEPT_ID],
        "pedagogical_kg": {},
    }

    # Run the same helper funcs generate_personalized_response runs so
    # _build_enhanced_prompt has every kwarg it expects.
    conv = gen._build_conversation_context(STUDENT_ID, student_state, analysis)
    emo  = gen._adapt_emotional_tone(analysis, student_state)
    ls   = gen._adapt_to_learning_style(student_state, analysis)
    per  = gen._adapt_to_personality(student_state)
    prog = gen._build_progress_context(student_state, analysis)
    ic   = gen._build_interest_context(student_state)
    fmt  = gen._get_format_preferences(student_state)
    err  = gen._build_error_feedback(None, None, analysis)
    meta = gen._generate_metacognitive_guidance(student_state, analysis)
    diff = gen._adapt_difficulty_and_pacing(student_state, analysis)

    prompt = gen._build_enhanced_prompt(
        student_message=STUDENT_INPUT, code=None,
        student_state=student_state, analysis=analysis,
        conversation_context=conv, emotional_context=emo,
        learning_style_adaptation=ls, personality_adaptation=per,
        progress_context=prog, interest_context=ic,
        format_preferences=fmt, error_feedback=err,
        metacognitive_guidance=meta, difficulty_adaptation=diff,
        adaptive_analysis=None,
    )
    return prompt, student_state, analysis


def extract_lp_sections(prompt: str) -> str:
    """Slice out the LP-1..LP-3 block so we can print just the CPAL parts."""
    start = prompt.find("=== LP-1: DIAGNOSTIC CONTEXT")
    if start < 0: return "(no LP sections present)"
    end = prompt.find("=== CONVERSATION", start)
    if end < 0: end = prompt.find("=== EMOTIONAL", start)
    if end < 0: end = start + 3500
    return prompt[start:end].rstrip()


def call_ollama(gen, student_state, analysis, tag):
    sys.stdout.write(f"\n[streaming {tag} response]\n")
    sys.stdout.flush()
    def on_chunk(p):
        sys.stdout.write(p); sys.stdout.flush()
    gen._stream_callback = on_chunk
    r = gen.generate_personalized_response(
        student_id=STUDENT_ID, student_message=STUDENT_INPUT,
        student_state=student_state, analysis=analysis,
        code=None, code_analysis=None, adaptive_analysis=None,
    )
    gen._stream_callback = None
    return r


def main():
    cat = get_catalogue(
        os.path.join(ROOT, "data", "mental_models", "wrong_models_catalogue.json")
    )
    diag = LPDiagnostician(catalogue=cat).diagnose(
        student_id=STUDENT_ID, concept=CONCEPT_ID,
        question_text=STUDENT_INPUT,
        stored_lp_level="L1", stored_lp_streak=0,
    ).to_dict()

    hr("NATURAL DIAGNOSIS")
    print(f"  actual LP level detected  : {diag['current_lp_level']}")
    print(f"  wrong model matched       : {diag['wrong_model_id']} (score {diag.get('match_score',0):.2f})")
    print(f"  (we'll override the level to L1/L2/L3/L4 below for comparison)")

    gen = EnhancedPersonalizedGenerator()
    hr(f"Ollama model: {gen._ollama_model}")

    # Which intervention is valid per level? Use the LP-validity gate.
    candidates = [("transfer_task", 0.92), ("worked_example", 0.80),
                  ("socratic_prompt", 0.70), ("trace_scaffold", 0.65),
                  ("transfer_prompt", 0.55)]
    for lvl in ("L1", "L2", "L3", "L4"):
        filt = filter_interventions_by_lp(candidates, lvl)
        intervention = filt[0][0] if filt else "worked_example"

        hr(f"LEVEL {lvl}   (valid intervention: {intervention})")
        prompt, ss, an = build_prompt_for_level(gen, diag, lvl, intervention)
        print("\n--- LP-1/LP-2/LP-3 block actually sent to Ollama ---")
        print(extract_lp_sections(prompt))
        # Cap the prompt length shown — user cares about CPAL block only.
        resp = call_ollama(gen, ss, an, lvl)
        print(f"\n--- end {lvl} ---")
        # Save full response to a file for later inspection
        out_path = os.path.join(ROOT, "output", f"cpal_lp_demo_{lvl}.txt")
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(resp)
        print(f"(full response saved to {out_path})")


if __name__ == "__main__":
    main()
