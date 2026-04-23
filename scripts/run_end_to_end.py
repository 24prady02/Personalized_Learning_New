"""
End-to-end demo: a single student prompt -> full Ollama response.
Exercises every trained component:
  1. Text -> Big Five (MiniLM fine-tuned on Pennebaker Essays)
  2. Big Five -> Nestor styles + strategies + recommended intervention
  3. EnhancedPersonalizedGenerator builds the prompt from the inferred state
  4. Ollama llama3.2 generates the final student-facing response
"""
import sys, os, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "3")

from src.models.nestor.nestor_bayesian_profiler import NestorBayesianProfiler
from src.orchestrator.enhanced_personalized_generator import EnhancedPersonalizedGenerator
from src.knowledge_graph.lp_index import LPIndex
import json


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
    print("=" * 72)
    print("END-TO-END: student prompt -> personality -> LLM response")
    print("=" * 72)

    # --- 1. Personality from prompt ------------------------------------------
    nestor = NestorBayesianProfiler({"nestor": {"data_dir": "data/nestor"}})
    profile = nestor.infer_from_prompt(STUDENT_PROMPT)
    p = profile['personality']
    print(f"\n[1] Big Five (source={profile['personality_source']}):")
    for k in ('openness', 'conscientiousness', 'extraversion',
             'agreeableness', 'neuroticism'):
        print(f"   {k:<18} = {p[k]:.2f}")

    ls = profile['learning_styles']
    st = profile['learning_strategies']
    print(f"\n[2] Nestor learning profile:")
    print(f"   styles:   {ls['visual_verbal']}/{ls['sensing_intuitive']}/"
          f"{ls['active_reflective']}/{ls['sequential_global']}")
    print(f"   top-3 elements:   {profile['recommended_elements']}")
    print(f"   intervention:     {profile['intervention_preference']}")

    # --- 2.5. Pull a realistic mastery dict from student_states.json -------
    #    (for this demo we use the 'beginner' profile so the LP shows some
    #     concepts ready and the next step clearly not ready)
    try:
        states = json.load(open("data/student_states.json"))
        concept_nodes = states.get("beginner", {}).get("cognitive_graph", {}).get("concept_nodes", {})
        mastery = {c: float(n.get("mastery", 0.0)) for c, n in concept_nodes.items()}
    except Exception as _e:
        print(f"   (student_states.json unavailable: {_e}; using empty mastery)")
        mastery = {}

    # --- 2.6. Query the LP for the target concept --------------------------
    target_concept = "recursion"  # in real pipeline: concept_retriever.retrieve_from_code(...)
    lp = LPIndex()
    lp_path = lp.get_path(target_concept, mastery)
    print(f"\n[2.5] LP path for target='{target_concept}':")
    if lp_path is None:
        print(f"   no progression covers '{target_concept}'")
    else:
        print(f"   {lp.render_prompt_block(lp_path)}")

    # --- 3. Build student_state + analysis the generator expects -----------
    student_state = {
        'interaction_count': 1,
        'personality':       p,
        'knowledge_state':   {'overall_mastery': 0.35, 'mastery_history': [0.35]},
        'interests':         [],
        'psychological_graph': {
            'attribution':   'internal_stable',
            'self_efficacy': 'low',
            'srl_phase':     'performance',
            'imposter_flag': 'bad at' in STUDENT_PROMPT.lower(),
            'high_anxiety':  p['neuroticism'] > 0.55,
            'flow_state':    False,
        },
        'progression_graph': {'stage': 2, 'zpd_status': 'within',
                              'scaffold_level': 4, 'has_attempt': True},
        'content_channel':   {'encoding_strength': 'surface',
                              'dual_coding': 'verbal_only', 'elaboration': False},
        'recommended_intervention': {
            'type': profile['intervention_preference'],
            'rationale': 'Inferred from prompt via Nestor text-personality pipeline.',
        },
    }
    # Emotion heuristic from Big Five + prompt text (classifier needs actions)
    emotion = 'frustrated' if p['neuroticism'] > 0.55 else 'confused'
    analysis = {
        'emotion': emotion,
        'frustration_level': float(p['neuroticism']),
        'engagement_score':  0.5,
        'bkt_update': {'p_learned_before': 0.30, 'p_learned_after': 0.35},
        'cse_kg': {
            'concept': 'recursion',
            'prerequisites': ['functions', 'base case', 'stack frames'],
            'related_concepts': ['iteration', 'divide and conquer'],
            'definition': 'A function that calls itself with a smaller input '
                          'until a base case is reached.',
        },
        'pedagogical_kg': {
            'progression': 'function call -> self-reference -> base case -> recursive step',
            'misconceptions': [
                'forgetting base case causes infinite recursion',
                'base case for factorial is n==0, not n==1',
            ],
            'cognitive_load': 'high',
            'interventions': ['worked example', 'visual trace of call stack'],
            # NEW: structured LP path injected from learning_progressions.json
            'learning_path': lp_path,
        },
        'coke': {
            'cognitive_state': emotion,
            'mental_activity': 'reasoning about self-reference',
            'behavioral_response': 'may abandon task if not scaffolded',
            'confidence': 0.40,
            'cognitive_chain': {
                'description': 'wrong output -> attributes to ability -> disengages',
            },
        },
    }

    # --- 4. Generate the response via Ollama -------------------------------
    print(f"\n[3] Invoking EnhancedPersonalizedGenerator ...")
    gen = EnhancedPersonalizedGenerator()
    print(f"   Ollama model selected: {gen._ollama_model}")

    # Intercept the Ollama HTTP call so we can both print the prompt and
    # still get the real response back.
    captured = {}
    import requests as _req
    orig_post = _req.post
    def _capture_post(url, json=None, timeout=None, **kw):
        if "ollama" in url or "11434" in url:
            captured['prompt'] = json.get('prompt', '') if json else ''
        return orig_post(url, json=json, timeout=timeout, **kw)
    _req.post = _capture_post

    t0 = time.time()
    try:
        response = gen.generate_personalized_response(
            student_id='demo_student',
            student_message=STUDENT_PROMPT,
            student_state=student_state,
            analysis=analysis,
            code=STUDENT_CODE,
        )
    finally:
        _req.post = orig_post
    elapsed = time.time() - t0

    # Show the LP block inside the assembled prompt so we can verify it's
    # actually being sent, not just constructed.
    prompt_text = captured.get('prompt', '')
    lp_start = prompt_text.find("[LP Progression")
    lp_end = prompt_text.find("\n[", lp_start + 1) if lp_start != -1 else -1
    print(f"\n[3.5] LP block as it appears inside the compiled Ollama prompt:")
    print("-" * 72)
    if lp_start == -1:
        print("   (NOT FOUND in prompt — something did not wire correctly)")
    else:
        print(prompt_text[lp_start:lp_end if lp_end != -1 else lp_start + 1200])
    print("-" * 72)
    print(f"   (full prompt length: {len(prompt_text)} chars)")

    print(f"\n[4] Ollama response ({elapsed:.1f}s, {len(response)} chars):")
    print("-" * 72)
    print(response)
    print("-" * 72)


if __name__ == "__main__":
    main()
