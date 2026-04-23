"""
Same student prompt, three different mastery profiles — prove the LP
pipeline actually differentiates the teaching plan per student.

Profiles:
  * beginner   — all concepts ~0.15 mastery
  * intermediate — mastered early Java (type_mismatch, infinite_loop,
                    null_pointer, string_equality, variable_scope ~0.85) but
                    everything later is ~0.30
  * advanced   — mastered full Week 1-5 path (~0.85) — recursion prereqs
                  all satisfied

For each: show the LP path, the enforcement decision, and the first
~15 lines of the Ollama response. Expect very different teaching plans.
"""
import sys, os, time, json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "3")

import requests
from src.models.nestor.nestor_bayesian_profiler import NestorBayesianProfiler
from src.orchestrator.enhanced_personalized_generator import EnhancedPersonalizedGenerator
from src.knowledge_graph.lp_index import LPIndex

PROMPT = (
    "I'm trying to understand recursion but my factorial function returns "
    "the wrong value for n=0. Can you help me figure out what's wrong?"
)
CODE = "public int fact(int n) {\n    return n * fact(n - 1);\n}"

WEEK1 = ["type_mismatch", "infinite_loop"]
WEEK2 = ["null_pointer", "string_equality", "variable_scope",
         "assignment_vs_compare", "integer_division", "scanner_buffer"]
WEEK3 = ["array_index", "missing_return", "array_not_allocated",
         "boolean_operators", "sentinel_loop", "unreachable_code",
         "string_immutability"]
WEEK4 = ["no_default_constructor", "static_vs_instance",
         "foreach_no_modify", "overloading"]
WEEK5 = ["generics_primitives"]
LATE  = ["object_oriented", "functions", "error_handling"]

ALL_RECURSION_PREREQS = WEEK1 + WEEK2 + WEEK3 + WEEK4 + WEEK5 + LATE

PROFILES = {
    "beginner":     {c: 0.15 for c in ALL_RECURSION_PREREQS},
    "intermediate": {
        **{c: 0.85 for c in WEEK1 + WEEK2[:3]},  # strong on early stuff
        **{c: 0.30 for c in WEEK2[3:] + WEEK3 + WEEK4 + WEEK5 + LATE},
    },
    "advanced": {
        **{c: 0.85 for c in WEEK1 + WEEK2 + WEEK3 + WEEK4 + WEEK5},
        **{c: 0.80 for c in LATE},
    },
}


def run_profile(name, mastery, nestor, gen):
    print("\n" + "=" * 78)
    print(f"PROFILE: {name}")
    print("=" * 78)
    # LP lookup
    lp = LPIndex().get_path("recursion", mastery)
    print(f"\n[LP] on_track={lp['on_track']}  "
          f"next_concept={lp['next_concept']}  "
          f"target={lp['target_concept']}")

    nxt_step = next(s for s in lp["path"] if s["concept"] == lp["next_concept"])
    print(f"     next step mastery = {nxt_step['current_mastery']:.2f} / "
          f"{nxt_step['required_mastery']:.2f}  "
          f"{'READY' if nxt_step['ready'] else 'NOT READY'}")
    print(f"     enforcement will fire: {not lp['on_track']}")

    # Personality from prompt (same for all three profiles — prompt is identical)
    profile = nestor.infer_from_prompt(PROMPT)
    p = profile["personality"]

    state = {
        'interaction_count': 1, 'personality': p,
        'knowledge_state': {'overall_mastery': sum(mastery.values())/max(len(mastery),1),
                            'mastery_history': [sum(mastery.values())/max(len(mastery),1)]},
        'interests': [],
        'psychological_graph': {
            'attribution': 'internal_stable', 'self_efficacy': 'moderate',
            'srl_phase': 'performance',
            'imposter_flag': False,
            'high_anxiety': p['neuroticism'] > 0.55,
            'flow_state': False,
        },
        'progression_graph': {'stage': 2, 'zpd_status': 'within',
                              'scaffold_level': 4, 'has_attempt': True},
        'content_channel': {'encoding_strength': 'surface',
                            'dual_coding': 'verbal_only', 'elaboration': False},
        'recommended_intervention': {
            'type': profile['intervention_preference'],
            'rationale': 'Inferred from prompt.'},
    }
    analysis = {
        'emotion': 'confused', 'frustration_level': 0.4,
        'engagement_score': 0.6,
        'bkt_update': {'p_learned_before': 0.50, 'p_learned_after': 0.55},
        'cse_kg': {'concept': 'recursion',
                   'prerequisites': ['functions', 'base case', 'stack frames'],
                   'related_concepts': ['iteration', 'divide and conquer'],
                   'definition': 'A function that calls itself with a smaller '
                                 'input until a base case is reached.'},
        'pedagogical_kg': {
            'progression': 'function call -> base case -> recursive step',
            'misconceptions': ['forgetting base case causes infinite recursion',
                               'base case for factorial is n==0, not n==1'],
            'cognitive_load': 'high',
            'interventions': ['worked example'],
            'learning_path': lp,
        },
        'coke': {'cognitive_state': 'confused',
                 'mental_activity': 'reasoning about recursion',
                 'behavioral_response': 'continues engagement',
                 'confidence': 0.55,
                 'cognitive_chain': {'description': 'mild confusion, engaged'}},
    }

    t0 = time.time()
    resp = gen.generate_personalized_response(
        student_id=f'demo_{name}', student_message=PROMPT,
        student_state=state, analysis=analysis, code=CODE,
    )
    elapsed = time.time() - t0
    print(f"\n[Ollama {gen._ollama_model}] {elapsed:.1f}s, {len(resp)} chars")
    print("-" * 78)
    # first ~20 lines
    preview = "\n".join(resp.splitlines()[:20])
    print(preview)
    if len(resp.splitlines()) > 20:
        print(f"... [+{len(resp.splitlines()) - 20} more lines]")
    print("-" * 78)


def main():
    nestor = NestorBayesianProfiler({"nestor": {"data_dir": "data/nestor"}})
    gen = EnhancedPersonalizedGenerator()
    gen._stream_callback = None  # keep stdout clean
    print(f"using model: {gen._ollama_model}")

    for name, mastery in PROFILES.items():
        run_profile(name, mastery, nestor, gen)


if __name__ == "__main__":
    main()
