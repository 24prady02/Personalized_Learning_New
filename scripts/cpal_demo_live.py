"""
Live CPAL demo: runs one realistic student input through the integrated
pipeline and prints the LP diagnosis, the LP-grounded prompt sections the
generator would send to the LLM, a simulated student reply, the post-reply
classification with delta_lp, and the reward breakdown.

This exercises the real modules in src/ — no mocks.
"""
import os, sys, json
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from src.knowledge_graph.mental_models import get_catalogue
from src.orchestrator.lp_diagnostic import (
    LPDiagnostician,
    filter_interventions_by_lp,
    classify_post_reply,
)
from src.reinforcement_learning.lp_progression_rnn import (
    LPProgressionRanker,
    build_state_vector,
)
from src.reinforcement_learning.reward_function import RewardCalculator


def hr(title=""):
    bar = "=" * 70
    if title:
        print(f"\n{bar}\n{title}\n{bar}")
    else:
        print(bar)


STUDENT_INPUT = (
    "I made two strings with the same text so they should be equal, but "
    "when I use == it returns false. I printed them both and they look "
    "identical. Why isn't it working? It should just compare the text."
)
CONCEPT_ID = "string_equality"
STUDENT_ID = "demo_student_001"


def main():
    cat = get_catalogue(
        os.path.join(ROOT, "data", "mental_models", "wrong_models_catalogue.json")
    )
    diagnostician = LPDiagnostician(catalogue=cat)
    ranker = LPProgressionRanker()

    hr("STUDENT INPUT")
    print(STUDENT_INPUT)
    print(f"\nconcept = {CONCEPT_ID}   student_id = {STUDENT_ID}")

    hr("STAGE 1 — LP DIAGNOSTIC")
    diag = diagnostician.diagnose(
        student_id=STUDENT_ID,
        concept=CONCEPT_ID,
        question_text=STUDENT_INPUT,
        stored_lp_level="L1",
        stored_lp_streak=0,
    )
    d = diag.to_dict()
    print(f"  current_lp_level    : {d['current_lp_level']}")
    print(f"  target_lp_level     : {d['target_lp_level']}")
    print(f"  logical_step        : {d['logical_step']}")
    print(f"  logical_step_detail : {d['logical_step_detail']}")
    print(f"  plateau_flag        : {d['plateau_flag']}")
    print(f"  wrong_model_id      : {d['wrong_model_id']}")
    print(f"  wrong_model_belief  : {(d.get('wrong_model_description') or '')[:120]}")
    print(f"  matched_signal      : {d.get('matched_signal', '')}")
    print(f"  match_score         : {d.get('match_score', 0):.2f}")

    hr("STAGE 2 — INTERVENTION SELECTION (LP-validity gate)")
    candidates = [
        ("transfer_task", 0.92),
        ("worked_example", 0.80),
        ("socratic_prompt", 0.70),
        ("trace_scaffold", 0.65),
        ("transfer_prompt", 0.55),
    ]
    filtered = filter_interventions_by_lp(candidates, d["current_lp_level"])
    print(f"  recommender top-5       : {[c[0] for c in candidates]}")
    print(f"  after LP-{d['current_lp_level']} gate      : {[c[0] for c in filtered]}")
    ranked = ranker.rank(
        session_state_vectors=[],
        lp_level=d["current_lp_level"],
        plateau_flag=d["plateau_flag"],
    )
    top_ranker = ranked[0] if ranked else None
    print(f"  LPProgressionRanker top : {top_ranker}")
    chosen_intervention = (filtered[0][0] if filtered else top_ranker[0])
    print(f"  → chosen intervention   : {chosen_intervention}")

    hr("STAGE 3 — LP-GROUNDED PROMPT SECTIONS")
    print("  (these are what _build_enhanced_prompt would inject at the top of")
    print("   the LLM prompt, before the existing 10 sections)\n")

    rubric = cat.get_lp_rubric(CONCEPT_ID) or {}
    header = (
        f"You are tutoring a student on **{CONCEPT_ID}**. They are currently "
        f"at **{d['current_lp_level']}**. Your job this turn: move them to "
        f"**{d['target_lp_level']}**."
    )
    print("--- HEADER (LP-grounded) ---")
    print(header)

    print("\n--- LP-1: DIAGNOSTIC CONTEXT ---")
    print(f"  current level       : {d['current_lp_level']} — {rubric.get(d['current_lp_level'], '')[:100]}")
    print(f"  target level        : {d['target_lp_level']} — {rubric.get(d['target_lp_level'], '')[:100]}")
    print(f"  streak at level     : {d['lp_streak']}")
    print(f"  plateau             : {d['plateau_flag']}")

    print("\n--- LP-2: WRONG MENTAL MODEL ---")
    if d["wrong_model_id"]:
        print(f"  identified model    : {d['wrong_model_id']}")
        print(f"  wrong belief        : {d.get('wrong_model_description', '')}")
        print(f"  origin              : {d.get('wrong_model_origin', '')}")
        print(f"  matched signal      : \"{d.get('matched_signal', '')}\"")
        print(f"  L3 expert benchmark :")
        for k in (d.get("expert_benchmark_key_ideas") or [])[:5]:
            print(f"      - {k}")
    else:
        print("  (no wrong model matched — proceed with generic scaffold)")

    print("\n--- LP-3: SIX-STEP INSTRUCTION (L1 variant) ---")
    l1_steps = [
        "1. Acknowledge what the student observed (they see == returning false).",
        "2. DO NOT restate the rule. Instead, elicit: ask what they think == is comparing.",
        "3. Introduce the word 'reference' as a new vocabulary item tied to a concrete image.",
        "4. Walk a memory-diagram: show two heap boxes for the two new Strings with different addresses.",
        "5. Run ==: compare the two addresses side-by-side. Show false.",
        "6. Close with a prediction question: 'If I use .equals(), what will it compare?'",
    ]
    for s in l1_steps:
        print(f"  {s}")

    hr("GENERATED RESPONSE (what the LLM would produce given the above prompt)")
    response = (
        f"You've caught something that trips up almost everyone learning Java — the two strings\n"
        f"LOOK identical, but == is returning false. Let's figure out what == is actually doing.\n\n"
        f"Before I explain: when you write `s1 == s2`, what do you think Java is comparing? The\n"
        f"characters one by one? The 'value' of the string? Pause for a second on that.\n\n"
        f"Here's the piece that's missing. When you write:\n"
        f"    String s1 = new String(\"hello\");\n"
        f"    String s2 = new String(\"hello\");\n"
        f"Java makes TWO separate objects in memory — two different boxes. Imagine they live at\n"
        f"addresses 0x1A4 and 0x2F8. Each box happens to contain the letters h-e-l-l-o, but\n"
        f"they are two distinct boxes.\n\n"
        f"Now: `s1 == s2` doesn't look inside the boxes. It compares the ADDRESSES — 0x1A4 vs\n"
        f"0x2F8. Different addresses → false. The content is identical; the boxes are not.\n\n"
        f"Quick check for you: if you switched to `s1.equals(s2)`, what do you think that\n"
        f"would compare — the addresses, or what's inside the boxes?"
    )
    print(response)

    hr("STAGE 4 — SIMULATED STUDENT REPLY + POST-REPLY CLASSIFICATION")
    student_reply = (
        "oh so == is comparing where the strings live in memory, the addresses, "
        "not the letters. And .equals() would look inside each box and compare "
        "the characters. Each new String() makes a separate box."
    )
    print(f"  student_reply: {student_reply}\n")
    ls, lsd, post_lvl = classify_post_reply(student_reply)
    pre = d["current_lp_level"]
    level_idx = {"L1": 1, "L2": 2, "L3": 3, "L4": 4}
    delta_lp = level_idx[post_lvl] - level_idx[pre]
    print(f"  post_lp_level       : {post_lvl}")
    print(f"  logical_step        : {ls}")
    print(f"  logical_step_detail : {lsd}")
    print(f"  delta_lp            : {delta_lp:+d}  ({pre} → {post_lvl})")

    hr("STAGE 5 — STATE VECTOR + REWARD")
    vec = build_state_vector(
        lp_state={
            "lp_level": pre,
            "lp_streak": 0,
            "logical_step": d["logical_step"],
            "logical_step_detail": d["logical_step_detail"],
            "plateau_flag": d["plateau_flag"],
        },
        intervention_type=chosen_intervention,
        delta_lp_last=delta_lp,
        emotion="confident",
        encoding_strength="surface",
        stage=2,
        scaffold_level=3,
        mastery=0.45,
    )
    print(f"  state_vector (12-d) : [{', '.join(f'{x:.2f}' for x in vec)}]")

    reward_calc = RewardCalculator(config={})
    session_data_for_reward = {
        "emotion": "confused",
    }
    student_response_payload = {
        "mastery_before": 0.30,
        "mastery_after": 0.45,
        "engagement_score": 0.75,
        "emotion_after": "engaged",
        "zpd_status": "at_boundary",
        "attribution_before": "neutral",
        "attribution_after": "neutral",
        "intervention_type": chosen_intervention,
        "delta_lp": delta_lp,
        "lp_level_before": pre,
        "lp_level_after": post_lvl,
        "plateau_flag_before": d["plateau_flag"],
    }
    total = reward_calc.calculate_reward(
        session_data=session_data_for_reward,
        action_taken=0,
        student_response=student_response_payload,
    )
    print(f"  reward weights      : {reward_calc.weights}")
    print(f"  total reward        : {total:+.3f}")
    print(f"  (lp_gain weight 0.25 is active; delta_lp={delta_lp:+d})")

    hr("DONE — all 5 CPAL stages produced output")


if __name__ == "__main__":
    main()
