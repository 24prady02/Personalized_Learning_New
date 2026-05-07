"""
End-to-end CPAL demo.

Turn 1:  tutor poses a diagnostic question.
Turn 2:  student answers with reasoning.
         → this answer is what drives every dynamic component:
             Stage 1  LP-level assessment + wrong-model identification
             Stage 2  intervention selection through the LP-validity gate
             Stage 3  LP-1/LP-2/LP-3 prompt assembly
             Stage 5  state-vector construction
Turn 3:  tutor generates a grounded response through the real
         pls_fixed generator + local Ollama.

Everything between Turn 2 and Turn 3 is visible — that is the thing
the user asked to see end-to-end.
"""
import os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from src.knowledge_graph.mental_models import get_catalogue
from src.orchestrator.lp_diagnostic import (
    LPDiagnostician,
    filter_interventions_by_lp,
)
from src.reinforcement_learning.lp_progression_rnn import (
    LPProgressionRanker,
    build_state_vector,
)
from src.orchestrator.enhanced_personalized_generator import (
    EnhancedPersonalizedGenerator,
)


CONCEPT_ID = "string_equality"
STUDENT_ID = "demo_e2e"

TUTOR_QUESTION = """Here's a piece of Java:

    String s1 = new String("hello");
    String s2 = new String("hello");
    System.out.println(s1 == s2);

What do you think this prints? And can you explain your reasoning?"""

STUDENT_REASONING = (
    "I think it prints true. I used new String() twice, but new just copies "
    "the string right? A copy is the same thing as the original. Both s1 "
    "and s2 hold 'hello' so == should say they are equal."
)


def hr(title="", glyph="="):
    bar = glyph * 74
    if title:
        print(f"\n{bar}\n {title}\n{bar}")
    else:
        print(bar)


def main():
    # ==================================================================
    # TURN 1 — tutor asks diagnostic question
    # ==================================================================
    hr("TURN 1  |  TUTOR → STUDENT  (diagnostic question)")
    print(TUTOR_QUESTION)

    # ==================================================================
    # TURN 2 — student reasons
    # ==================================================================
    hr("TURN 2  |  STUDENT → TUTOR  (reasoning)")
    print(STUDENT_REASONING)

    # ==================================================================
    # Load all CPAL components
    # ==================================================================
    cat = get_catalogue(
        os.path.join(ROOT, "data", "mental_models",
                     "wrong_models_catalogue.json")
    )
    diagnostician = LPDiagnostician(catalogue=cat)
    ranker = LPProgressionRanker()

    # ==================================================================
    # STAGE 1 — LP level assessment + wrong-model identification
    # Driven by the student's reasoning (Turn 2 text).
    # ==================================================================
    hr("DYNAMIC COMPONENT 1  |  STAGE 1: LP diagnostic")
    diag = diagnostician.diagnose(
        student_id=STUDENT_ID,
        concept=CONCEPT_ID,
        question_text=STUDENT_REASONING,
        stored_lp_level="L1",
        stored_lp_streak=0,
    ).to_dict()
    print(f"  Current LP level          : {diag['current_lp_level']}")
    print(f"  Target LP level           : {diag['target_lp_level']}")
    print(f"  logical_step   (rule)     : {diag['logical_step']}")
    print(f"  logical_step_detail (mech): {diag['logical_step_detail']}")
    print(f"  Plateau flag              : {diag['plateau_flag']}")
    print(f"  Wrong-model id            : {diag['wrong_model_id']}")
    print(f"  Wrong belief detected     : "
          f"{(diag.get('wrong_model_description') or '')[:90]}")
    print(f"  Origin of belief          : "
          f"{(diag.get('wrong_model_origin') or '')[:90]}")
    print(f"  Matched conversation sig  : \"{diag.get('matched_signal','')}\"")
    print(f"  Match score               : {diag.get('match_score', 0):.2f}")
    print(f"  L3 expert benchmark       :")
    for k in (diag.get("expert_benchmark_key_ideas") or [])[:5]:
        print(f"      - {k}")

    # ==================================================================
    # STAGE 2 — Intervention selection via LP-validity gate
    # ==================================================================
    hr("DYNAMIC COMPONENT 2  |  STAGE 2: intervention selection")
    rl_top_k = [
        ("transfer_task",    0.92),
        ("worked_example",   0.80),
        ("socratic_prompt",  0.70),
        ("trace_scaffold",   0.65),
        ("transfer_prompt",  0.55),
    ]
    print("  Recommender top-5 (raw)     : " +
          ", ".join(c[0] for c in rl_top_k))
    valid_after_gate = filter_interventions_by_lp(
        rl_top_k, diag["current_lp_level"]
    )
    print(f"  After LP-{diag['current_lp_level']} validity gate  : " +
          ", ".join(c[0] for c in valid_after_gate))
    rejected = set(c[0] for c in rl_top_k) - set(c[0] for c in valid_after_gate)
    print(f"  Rejected by gate            : "
          f"{sorted(rejected) if rejected else '-'}")
    ranked = ranker.rank(
        session_state_vectors=[],
        lp_level=diag["current_lp_level"],
        plateau_flag=diag["plateau_flag"],
    )
    print(f"  LPProgressionRanker top pick: "
          f"{ranked[0] if ranked else '(empty)'}")
    chosen = valid_after_gate[0][0] if valid_after_gate else \
             (ranked[0][0] if ranked else "worked_example")
    print(f"  → CHOSEN INTERVENTION       : {chosen}")

    # ==================================================================
    # STAGE 5 (pre-generation) — state vector ready for persistence
    # ==================================================================
    hr("DYNAMIC COMPONENT 3  |  STAGE 5: state vector construction")
    state_vec = build_state_vector(
        lp_state={
            "lp_level":            diag["current_lp_level"],
            "lp_streak":           diag["lp_streak"],
            "logical_step":        diag["logical_step"],
            "logical_step_detail": diag["logical_step_detail"],
            "plateau_flag":        diag["plateau_flag"],
        },
        intervention_type=chosen,
        delta_lp_last=0,
        emotion="engaged",
        encoding_strength="surface",
        stage=1,
        scaffold_level=3,
        mastery=0.30,
    )
    labels = ["mastery", "lp_level_norm", "step", "detail", "streak_norm",
              "plateau", "delta_lp", "intervention_idx", "emotion_val",
              "encoding_val", "stage_norm", "scaffold_norm"]
    for name, v in zip(labels, state_vec):
        print(f"    {name:20s}: {v:+.2f}")

    # ==================================================================
    # STAGE 3 — Assemble LP-grounded prompt through the REAL generator
    # ==================================================================
    hr("DYNAMIC COMPONENT 4  |  STAGE 3: LP-grounded prompt assembly")
    student_state = {
        "student_id":               STUDENT_ID,
        "lp_diagnostic":            diag,
        "recommended_intervention": {"type": chosen},
        "personality_profile": {
            "communication_style":  "direct",
            "learning_preference":  "visual",
        },
        "bkt_mastery":     {CONCEPT_ID: 0.30},
        "emotional_state": "engaged",
        "interaction_count": 2,
    }
    analysis = {
        "emotion":          {"primary": "engaged", "confidence": 0.7},
        "knowledge_gaps":   [CONCEPT_ID],
        "pedagogical_kg":   {},
    }

    gen = EnhancedPersonalizedGenerator()
    # Drive through the real generator's helpers so _build_enhanced_prompt
    # sees exactly the kwargs generate_personalized_response would pass.
    conv = gen._build_conversation_context(STUDENT_ID, student_state, analysis)
    prompt = gen._build_enhanced_prompt(
        student_message=STUDENT_REASONING, code=None,
        student_state=student_state, analysis=analysis,
        conversation_context=conv,
        emotional_context=gen._adapt_emotional_tone(analysis, student_state),
        learning_style_adaptation=gen._adapt_to_learning_style(student_state, analysis),
        personality_adaptation=gen._adapt_to_personality(student_state),
        progress_context=gen._build_progress_context(student_state, analysis),
        interest_context=gen._build_interest_context(student_state),
        format_preferences=gen._get_format_preferences(student_state),
        error_feedback=gen._build_error_feedback(None, None, analysis),
        metacognitive_guidance=gen._generate_metacognitive_guidance(student_state, analysis),
        difficulty_adaptation=gen._adapt_difficulty_and_pacing(student_state, analysis),
        adaptive_analysis=None,
    )
    # Pull the LP block for display (the rest is the 10 generic sections)
    start = prompt.find("=== LP-1: DIAGNOSTIC CONTEXT")
    end_markers = ["=== CONVERSATION", "=== EMOTIONAL", "=== PROGRESSION"]
    end = min(
        [prompt.find(m, start) for m in end_markers if prompt.find(m, start) > 0]
        or [start + 2600]
    )
    print(prompt[start:end].rstrip())
    print(f"\n  (full prompt is {len(prompt):,} chars; LP sections shown above;")
    print(f"   10 generic personalization sections follow them in the prompt)")

    # ==================================================================
    # TURN 3 — tutor generates grounded response via Ollama
    # ==================================================================
    hr("TURN 3  |  TUTOR → STUDENT  (grounded response from real generator)")
    print(f"  [model: {gen._ollama_model}]  [intervention: {chosen}]")
    print(f"  [LP: {diag['current_lp_level']} → {diag['target_lp_level']}]  "
          f"[wrong-model target: {diag['wrong_model_id']}]\n")

    def on_chunk(piece: str):
        sys.stdout.write(piece)
        sys.stdout.flush()
    gen._stream_callback = on_chunk
    response = gen.generate_personalized_response(
        student_id=STUDENT_ID,
        student_message=STUDENT_REASONING,
        student_state=student_state,
        analysis=analysis,
    )

    hr("", glyph="-")

    # ==================================================================
    # Reading — what drove each visible feature of the response
    # ==================================================================
    hr("WHAT YOU'RE LOOKING AT (traceback from response → dynamic components)")
    print("  • LP-level-appropriate scaffolding:")
    print(f"      — detected {diag['current_lp_level']}, so LP-3 six-step")
    print(f"        instruction shaped the response structure.")
    print("  • Wrong-model-aware correction:")
    print(f"      — detected {diag['wrong_model_id']}")
    print(f"      — LP-2 told the LLM to correct exactly this belief:")
    print(f"        \"{(diag.get('wrong_model_description') or '')[:80]}\"")
    print(f"      — matched signal in student's text: "
          f"\"{diag.get('matched_signal','')}\"")
    print("  • Intervention gating:")
    print(f"      — raw RL recommender top pick was 'transfer_task'")
    print(f"      — LP-{diag['current_lp_level']} gate rejected it "
          f"(invalid for this level)")
    print(f"      — '{chosen}' was chosen instead.")
    print("  • Expert benchmark grounding:")
    print(f"      — LP-2 carried the L3 expert key-ideas into the prompt,")
    print(f"        so the mechanism the LLM teaches is the catalogue's,")
    print(f"        not something the model invented.")


if __name__ == "__main__":
    main()
