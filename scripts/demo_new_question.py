"""
Fresh demo — different question (NullPointerException, not factorial), different
personality signal (exploratory, not anxious), and a mastery profile where the
student IS ready for the target concept so the pipeline teaches it directly.
"""
import sys, os, time, json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "3")

from src.models.nestor.nestor_bayesian_profiler import NestorBayesianProfiler
from src.orchestrator.enhanced_personalized_generator import EnhancedPersonalizedGenerator
from src.knowledge_graph.lp_index import LPIndex


PROMPT = (
    "Hey, I've been building a small text-adventure game in Java and I keep "
    "getting NullPointerExceptions whenever I call methods on the Room "
    "object I just created. Here's what I have — can you explain what's "
    "actually going on underneath? I'd rather understand *why* this happens "
    "than just patch it, if that makes sense."
)
CODE = (
    "public class Game {\n"
    "    Room currentRoom;\n"
    "    public void start() {\n"
    "        currentRoom.describe();   // crash here\n"
    "    }\n"
    "}\n"
    "\n"
    "public class Room {\n"
    "    String name;\n"
    "    public void describe() {\n"
    "        System.out.println(\"You are in \" + name);\n"
    "    }\n"
    "}"
)

# Student has mastered type_mismatch already (the one prereq for null_pointer)
MASTERY = {
    "type_mismatch": 0.85,
    "infinite_loop": 0.80,
    "null_pointer":  0.30,   # the current target — not yet mastered
}


def main():
    nestor = NestorBayesianProfiler({"nestor": {"data_dir": "data/nestor"}})
    profile = nestor.infer_from_prompt(PROMPT)
    p = profile["personality"]

    lp = LPIndex().get_path("null_pointer", MASTERY)

    print("=" * 78)
    print("NEW DEMO — NullPointerException in a text-adventure game")
    print("=" * 78)
    print(f"\n[Pipeline signals]")
    print(f"  Big Five      : "
          + "  ".join(f"{k[:3]}={p[k]:.2f}" for k in
                      ('openness','conscientiousness','extraversion',
                       'agreeableness','neuroticism')))
    print(f"  style         : {profile['learning_styles']['visual_verbal']}/"
          f"{profile['learning_styles']['sensing_intuitive']}/"
          f"{profile['learning_styles']['active_reflective']}/"
          f"{profile['learning_styles']['sequential_global']}")
    print(f"  intervention  : {profile['intervention_preference']}")
    print(f"  elements      : {profile['recommended_elements']}")
    print(f"  LP next step  : {lp['next_concept']}  "
          f"(on_track={lp['on_track']})")
    print(f"  mastery on target: {MASTERY['null_pointer']:.2f} / 0.75")

    state = {
        'interaction_count': 1, 'personality': p,
        'knowledge_state': {'overall_mastery': 0.65,
                            'mastery_history': [0.60, 0.65]},
        'interests': [],
        'psychological_graph': {
            'attribution': 'internal_stable',
            'self_efficacy': 'growth',
            'srl_phase': 'forethought',
            'imposter_flag': False,
            'high_anxiety':  p['neuroticism'] > 0.55,
            'flow_state':    p['openness'] > 0.60,
        },
        'progression_graph': {'stage': 3, 'zpd_status': 'within',
                              'scaffold_level': 3, 'has_attempt': True},
        'content_channel': {'encoding_strength': 'partial',
                            'dual_coding': 'verbal_only', 'elaboration': True},
        'recommended_intervention': {
            'type': profile['intervention_preference'],
            'rationale': 'Inferred from exploratory prompt.'},
    }
    analysis = {
        'emotion': 'curious', 'frustration_level': 0.25,
        'engagement_score': 0.80,
        'bkt_update': {'p_learned_before': 0.28, 'p_learned_after': 0.30},
        'cse_kg': {
            'concept': 'null_pointer',
            'prerequisites': ['references', 'object instantiation (new)',
                              'heap vs stack'],
            'related_concepts': ['NullPointerException', 'default values',
                                 'Optional<T>'],
            'definition': 'Accessing a member via a reference whose value is '
                          'null — the JVM throws NullPointerException because '
                          'there is no object on the heap to dereference.',
        },
        'pedagogical_kg': {
            'progression': 'object reference -> new operator -> null default -> '
                           'dereference check',
            'misconceptions': [
                'declaring a reference also creates the object',
                'Java auto-initializes object fields to a usable default',
                'null means "no value" rather than "no object allocated"',
            ],
            'cognitive_load': 'medium',
            'interventions': ['worked example', 'visual heap diagram'],
            'learning_path': lp,
        },
        'coke': {
            'cognitive_state': 'curious',
            'mental_activity': 'reasoning about memory model',
            'behavioral_response': 'continues exploration',
            'confidence': 0.65,
            'cognitive_chain': {
                'description': 'asks for why, not just fix -> high elaboration',
            },
        },
    }

    gen = EnhancedPersonalizedGenerator()
    print(f"\n[Running] model={gen._ollama_model} (streaming)\n")
    print("-" * 78)
    first = [None]
    t0 = time.time()
    def on_token(s):
        if first[0] is None:
            first[0] = time.time() - t0
            print(f"[TTFT={first[0]:.1f}s] ", end="", flush=True)
        print(s, end="", flush=True)
    gen._stream_callback = on_token
    resp = gen.generate_personalized_response(
        student_id='demo_game', student_message=PROMPT,
        student_state=state, analysis=analysis, code=CODE,
    )
    total = time.time() - t0
    print("\n" + "-" * 78)
    print(f"TTFT={first[0]:.1f}s   total={total:.1f}s   {len(resp)} chars")


if __name__ == "__main__":
    main()
