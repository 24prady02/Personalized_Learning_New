"""
A/B compare two Ollama models on the *same* fully-built prompt from the
personalized pipeline (prompt -> Big Five -> Nestor -> LP -> enforcement).

Captures the prompt that run_end_to_end produces, then fires it at each
model and prints responses side-by-side so the user can judge quality.
"""
import sys, os, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "3")

import json
import requests
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


def build_state_and_analysis():
    nestor = NestorBayesianProfiler({"nestor": {"data_dir": "data/nestor"}})
    profile = nestor.infer_from_prompt(STUDENT_PROMPT)
    p = profile['personality']

    try:
        states = json.load(open("data/student_states.json"))
        concept_nodes = (states.get("beginner", {})
                         .get("cognitive_graph", {}).get("concept_nodes", {}))
        mastery = {c: float(n.get("mastery", 0.0)) for c, n in concept_nodes.items()}
    except Exception:
        mastery = {}

    lp = LPIndex().get_path("recursion", mastery)

    state = {
        'interaction_count': 1,
        'personality':       p,
        'knowledge_state':   {'overall_mastery': 0.35, 'mastery_history': [0.35]},
        'interests':         [],
        'psychological_graph': {
            'attribution': 'internal_stable', 'self_efficacy': 'low',
            'srl_phase': 'performance',
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
    emotion = 'frustrated' if p['neuroticism'] > 0.55 else 'confused'
    analysis = {
        'emotion': emotion, 'frustration_level': float(p['neuroticism']),
        'engagement_score': 0.5,
        'bkt_update': {'p_learned_before': 0.30, 'p_learned_after': 0.35},
        'cse_kg': {'concept': 'recursion',
                   'prerequisites': ['functions', 'base case', 'stack frames'],
                   'related_concepts': ['iteration', 'divide and conquer'],
                   'definition': 'A function that calls itself with a smaller '
                                 'input until a base case is reached.'},
        'pedagogical_kg': {
            'progression': 'function call -> self-reference -> base case -> recursive step',
            'misconceptions': [
                'forgetting base case causes infinite recursion',
                'base case for factorial is n==0, not n==1',
            ],
            'cognitive_load': 'high',
            'interventions': ['worked example', 'visual trace of call stack'],
            'learning_path': lp,
        },
        'coke': {'cognitive_state': emotion,
                 'mental_activity': 'reasoning about self-reference',
                 'behavioral_response': 'may abandon task if not scaffolded',
                 'confidence': 0.40,
                 'cognitive_chain': {
                     'description': 'wrong output -> attributes to ability -> disengages'
                 }},
    }
    return state, analysis


def capture_prompt(gen, state, analysis):
    """Use the generator to build the prompt but intercept the HTTP call so
    we get the exact prompt string without waiting for inference."""
    captured = {}
    import requests as _req
    orig_post = _req.post
    def _cap(url, json=None, timeout=None, **kw):
        captured['prompt'] = json.get('prompt', '') if json else ''
        # return a dummy response so generator keeps running
        class _Stub:
            def raise_for_status(self): pass
            def json(self_): return {'response': '__captured__'}
        return _Stub()
    _req.post = _cap
    try:
        gen.generate_personalized_response(
            student_id='demo', student_message=STUDENT_PROMPT,
            student_state=state, analysis=analysis, code=STUDENT_CODE,
        )
    finally:
        _req.post = orig_post
    return captured['prompt']


def run_on_model(prompt, model):
    t0 = time.time()
    resp = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": model, "prompt": prompt, "stream": False,
              "options": {"temperature": 0.7}},
        timeout=600,
    )
    resp.raise_for_status()
    out = resp.json().get('response', '').strip()
    return out, time.time() - t0


def main():
    models_to_try = sys.argv[1:] or ["llama3.2", "qwen2.5-coder:7b"]
    state, analysis = build_state_and_analysis()
    gen = EnhancedPersonalizedGenerator()
    prompt = capture_prompt(gen, state, analysis)
    print(f"[compare] using built prompt of {len(prompt)} chars")

    # quickly check which requested models are actually installed
    tags = requests.get("http://localhost:11434/api/tags", timeout=5).json()
    have = {m['name'] for m in tags.get('models', [])}
    have_short = {n.split(':')[0] for n in have}

    for m in models_to_try:
        base = m.split(':')[0]
        if m not in have and base not in have_short:
            print(f"\n### {m} — NOT INSTALLED, skipping")
            print(f"    pull with:  ollama pull {m}")
            continue
        print(f"\n### {m}")
        try:
            out, elapsed = run_on_model(prompt, m)
        except Exception as e:
            print(f"    inference failed: {e}")
            continue
        print(f"   ({elapsed:.1f}s, {len(out)} chars)")
        print("-" * 72)
        print(out)
        print("-" * 72)


if __name__ == "__main__":
    main()
