"""
Grounded CPAL demo — uses the REAL EnhancedPersonalizedGenerator from
pls_fixed. CPAL Stage 1 (diagnose) produces lp_diagnostic, which we
inject into student_state exactly as orchestrator._generate_content
does. Then generator.generate_personalized_response(...) builds the
LP-grounded prompt (LP-1/LP-2/LP-3 sections) and streams through the
local Ollama model.

This is the "grounded response" path — the response you see below is
produced by the same generator the orchestrator uses in process_session.
"""
import os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from src.knowledge_graph.mental_models import get_catalogue
from src.orchestrator.lp_diagnostic import LPDiagnostician, filter_interventions_by_lp
from src.reinforcement_learning.lp_progression_rnn import LPProgressionRanker
from src.orchestrator.enhanced_personalized_generator import EnhancedPersonalizedGenerator


STUDENT_INPUT = (
    "I made two strings with the same text so they should be equal, but "
    "when I use == it returns false. I printed them both and they look "
    "identical. Why isn't it working? It should just compare the text."
)
CONCEPT_ID = "string_equality"
STUDENT_ID = "demo_student_001"


def hr(t=""):
    print("\n" + "=" * 72)
    if t:
        print(t)
        print("=" * 72)


def main():
    # --- Stage 1: diagnose ------------------------------------------------
    cat = get_catalogue(
        os.path.join(ROOT, "data", "mental_models", "wrong_models_catalogue.json")
    )
    diag = LPDiagnostician(catalogue=cat).diagnose(
        student_id=STUDENT_ID,
        concept=CONCEPT_ID,
        question_text=STUDENT_INPUT,
        stored_lp_level="L1",
        stored_lp_streak=0,
    ).to_dict()

    # --- Stage 2: LP-validity gate → pick intervention --------------------
    candidates = [
        ("transfer_task", 0.92),
        ("worked_example", 0.80),
        ("socratic_prompt", 0.70),
        ("trace_scaffold", 0.65),
    ]
    filtered = filter_interventions_by_lp(candidates, diag["current_lp_level"])
    chosen = filtered[0][0] if filtered else "worked_example"

    hr("CPAL STAGE 1/2 RESULT")
    print(f"  student_input      : {STUDENT_INPUT[:70]}...")
    print(f"  concept            : {CONCEPT_ID}")
    print(f"  LP level           : {diag['current_lp_level']} → {diag['target_lp_level']}")
    print(f"  wrong model        : {diag['wrong_model_id']}  (score={diag.get('match_score', 0):.2f})")
    print(f"  matched signal     : {diag.get('matched_signal', '')}")
    print(f"  plateau            : {diag['plateau_flag']}")
    print(f"  intervention chosen: {chosen}  (after LP-{diag['current_lp_level']} gate)")

    # --- Build student_state the way orchestrator._generate_content does -
    student_state = {
        "student_id": STUDENT_ID,
        "lp_diagnostic": diag,
        "recommended_intervention": {"type": chosen},
        # minimal fields the generator's other 10 sections read:
        "personality_profile": {
            "communication_style": "direct",
            "learning_preference": "visual",
        },
        "bkt_mastery": {CONCEPT_ID: 0.30},
        "emotional_state": "confused",
        "interaction_count": 1,
    }
    analysis = {
        "emotion": {"primary": "confused", "confidence": 0.7},
        "knowledge_gaps": [CONCEPT_ID],
        "pedagogical_kg": {},
    }

    # --- Build prompt via REAL generator, then stream Ollama --------------
    gen = EnhancedPersonalizedGenerator()
    hr(f"OLLAMA MODEL IN USE: {gen._ollama_model}")

    print("\n[Streaming response from Ollama — this is the grounded output]\n")

    # Token streaming so we can see it arrive live
    chunks_seen = []
    def on_chunk(piece: str):
        sys.stdout.write(piece)
        sys.stdout.flush()
        chunks_seen.append(piece)
    gen._stream_callback = on_chunk

    try:
        response = gen.generate_personalized_response(
            student_id=STUDENT_ID,
            student_message=STUDENT_INPUT,
            student_state=student_state,
            analysis=analysis,
            code=None,
            code_analysis=None,
            adaptive_analysis=None,
        )
    except Exception as e:
        print(f"\n[generator raised] {type(e).__name__}: {e}")
        return

    hr("FULL RESPONSE (final)")
    print(response)

    hr("WHAT MADE THIS RESPONSE GROUNDED")
    print("  * LP diagnosis flowed into student_state['lp_diagnostic'].")
    print(f"  * Generator's _build_enhanced_prompt injected LP-1/LP-2/LP-3")
    print(f"    sections above its existing 10 sections.")
    print(f"  * LP-2 section carried wrong-model {diag['wrong_model_id']}'s")
    print(f"    specific belief + the L3 expert benchmark — Ollama was")
    print(f"    instructed to address that exact misconception and nothing")
    print(f"    else.")
    print(f"  * LP-3 section carried the level-specific 6-step instruction")
    print(f"    for an L{diag['current_lp_level'][1]} student (not generic).")


if __name__ == "__main__":
    main()
