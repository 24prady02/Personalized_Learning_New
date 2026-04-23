"""
Verify streaming end-to-end: prints tokens to stdout as they arrive, so you
can see response text start flowing while the GPU is still generating.
Also measures time-to-first-token (TTFT) vs total time.
"""
import sys, os, time, json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "3")

from src.models.nestor.nestor_bayesian_profiler import NestorBayesianProfiler
from src.orchestrator.enhanced_personalized_generator import EnhancedPersonalizedGenerator
from src.knowledge_graph.lp_index import LPIndex

STUDENT_PROMPT = (
    "Honestly I think I'm just bad at programming. Everyone in my class gets "
    "this stuff and I feel stupid for not being able to figure out why my "
    "factorial returns the wrong value for n=0. I've been staring at this "
    "for two hours and nothing I try works."
)
STUDENT_CODE = (
    "public int fact(int n) {\n"
    "    return n * fact(n - 1);\n"
    "}"
)


def main():
    nestor = NestorBayesianProfiler({"nestor": {"data_dir": "data/nestor"}})
    profile = nestor.infer_from_prompt(STUDENT_PROMPT)
    p = profile['personality']

    states = json.load(open("data/student_states.json"))
    mastery = {
        c: float(n.get("mastery", 0.0))
        for c, n in states["beginner"]["cognitive_graph"]["concept_nodes"].items()
    }
    lp = LPIndex().get_path("recursion", mastery)

    state = {
        'interaction_count': 1, 'personality': p,
        'knowledge_state': {'overall_mastery': 0.35, 'mastery_history': [0.35]},
        'interests': [],
        'psychological_graph': {
            'attribution': 'internal_stable', 'self_efficacy': 'low',
            'srl_phase': 'performance',
            'imposter_flag': True, 'high_anxiety': True, 'flow_state': False,
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
        'emotion': 'frustrated', 'frustration_level': float(p['neuroticism']),
        'engagement_score': 0.5,
        'bkt_update': {'p_learned_before': 0.30, 'p_learned_after': 0.35},
        'cse_kg': {'concept': 'recursion',
                   'prerequisites': ['functions', 'base case', 'stack frames'],
                   'related_concepts': ['iteration', 'divide and conquer'],
                   'definition': 'A function that calls itself with smaller input.'},
        'pedagogical_kg': {
            'progression': 'function call -> base case -> recursive step',
            'misconceptions': ['forgetting base case', 'n==0 not n==1'],
            'cognitive_load': 'high',
            'interventions': ['worked example'],
            'learning_path': lp,
        },
        'coke': {'cognitive_state': 'frustrated', 'mental_activity': 'recursion',
                 'behavioral_response': 'may abandon', 'confidence': 0.4,
                 'cognitive_chain': {'description': 'wrong output -> disengages'}},
    }

    gen = EnhancedPersonalizedGenerator()
    print(f"model: {gen._ollama_model}\n")
    print("=" * 72)
    print("STREAMING OUTPUT (tokens appear live):")
    print("=" * 72)

    t0 = time.time()
    first = [None]
    def on_token(s):
        if first[0] is None:
            first[0] = time.time() - t0
            print(f"\n[TTFT={first[0]:.1f}s]  ", end="", flush=True)
        print(s, end="", flush=True)

    gen._stream_callback = on_token
    resp = gen.generate_personalized_response(
        student_id='demo', student_message=STUDENT_PROMPT,
        student_state=state, analysis=analysis, code=STUDENT_CODE,
    )
    total = time.time() - t0
    print("\n")
    print("=" * 72)
    print(f"final length: {len(resp)} chars  "
          f"TTFT: {first[0]:.1f}s  total: {total:.1f}s  "
          f"perceived-wait improvement: {total - first[0]:.1f}s")
    print("=" * 72)


if __name__ == "__main__":
    main()
