"""
End-to-end runner that ALSO saves all artifacts to a new output folder.

Identical pipeline to scripts/run_end_to_end.py, but writes:
  output/end_to_end_run_<timestamp>/
    transcript.txt   - everything printed to stdout
    prompt.txt       - the full assembled Ollama prompt
    response.md      - the final LLM response
    analysis.json    - structured personality/nestor/LP/state/analysis
"""
import sys, os, time, json, io
from contextlib import redirect_stdout
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))
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


def run_pipeline():
    """Run the full pipeline, return a dict with every artifact."""
    artifacts = {
        "student_prompt": STUDENT_PROMPT,
        "student_code": STUDENT_CODE,
        "started_at": datetime.utcnow().isoformat() + "Z",
    }

    print("=" * 72)
    print("END-TO-END: student prompt -> personality -> LLM response")
    print("=" * 72)

    # --- 1. Personality from prompt ----------------------------------------
    nestor = NestorBayesianProfiler({"nestor": {"data_dir": str(ROOT / "data" / "nestor")}})
    profile = nestor.infer_from_prompt(STUDENT_PROMPT)
    p = profile['personality']
    print(f"\n[1] Big Five (source={profile['personality_source']}):")
    for k in ('openness', 'conscientiousness', 'extraversion',
             'agreeableness', 'neuroticism'):
        print(f"   {k:<18} = {p[k]:.2f}")

    ls = profile['learning_styles']
    print(f"\n[2] Nestor learning profile:")
    print(f"   styles:   {ls['visual_verbal']}/{ls['sensing_intuitive']}/"
          f"{ls['active_reflective']}/{ls['sequential_global']}")
    print(f"   top-3 elements:   {profile['recommended_elements']}")
    print(f"   intervention:     {profile['intervention_preference']}")

    artifacts["nestor_profile"] = profile

    # --- 2.5. mastery from student_states.json -----------------------------
    try:
        states = json.load(open(ROOT / "data" / "student_states.json"))
        concept_nodes = states.get("beginner", {}).get("cognitive_graph", {}).get("concept_nodes", {})
        mastery = {c: float(n.get("mastery", 0.0)) for c, n in concept_nodes.items()}
    except Exception as _e:
        print(f"   (student_states.json unavailable: {_e}; using empty mastery)")
        mastery = {}

    artifacts["mastery"] = mastery

    # --- 2.6. LP path ------------------------------------------------------
    target_concept = "recursion"
    lp = LPIndex()
    lp_path = lp.get_path(target_concept, mastery)
    print(f"\n[2.5] LP path for target='{target_concept}':")
    if lp_path is None:
        print(f"   no progression covers '{target_concept}'")
    else:
        print(f"   {lp.render_prompt_block(lp_path)}")

    artifacts["lp_target"] = target_concept
    artifacts["lp_path"] = lp_path

    # --- 3. Build state + analysis -----------------------------------------
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

    artifacts["student_state"] = student_state
    artifacts["analysis"] = analysis

    # --- 4. Generate via Ollama --------------------------------------------
    print(f"\n[3] Invoking EnhancedPersonalizedGenerator ...")
    gen = EnhancedPersonalizedGenerator()
    print(f"   Ollama model selected: {gen._ollama_model}")

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

    prompt_text = captured.get('prompt', '')

    artifacts["ollama_model"] = gen._ollama_model
    artifacts["ollama_url"] = gen._ollama_url
    artifacts["full_prompt"] = prompt_text
    artifacts["response"] = response
    artifacts["elapsed_seconds"] = elapsed

    lp_start = prompt_text.find("[LP Progression")
    lp_end = prompt_text.find("\n[", lp_start + 1) if lp_start != -1 else -1
    print(f"\n[3.5] LP block as it appears inside the compiled Ollama prompt:")
    print("-" * 72)
    if lp_start == -1:
        print("   (NOT FOUND in prompt)")
    else:
        print(prompt_text[lp_start:lp_end if lp_end != -1 else lp_start + 1200])
    print("-" * 72)
    print(f"   (full prompt length: {len(prompt_text)} chars)")

    print(f"\n[4] Ollama response ({elapsed:.1f}s, {len(response)} chars):")
    print("-" * 72)
    print(response)
    print("-" * 72)

    artifacts["finished_at"] = datetime.utcnow().isoformat() + "Z"
    return artifacts


def main():
    stamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    out_dir = ROOT / "output" / f"end_to_end_run_{stamp}"
    out_dir.mkdir(parents=True, exist_ok=True)
    print(f"[saver] writing artifacts to: {out_dir}")

    # Tee stdout: print live AND capture for transcript.txt
    class Tee:
        def __init__(self, *streams): self.streams = streams
        def write(self, s):
            for st in self.streams: st.write(s)
        def flush(self):
            for st in self.streams: st.flush()

    transcript = io.StringIO()
    real_stdout = sys.stdout
    sys.stdout = Tee(real_stdout, transcript)
    try:
        artifacts = run_pipeline()
    finally:
        sys.stdout = real_stdout

    (out_dir / "transcript.txt").write_text(transcript.getvalue(), encoding="utf-8")
    (out_dir / "prompt.txt").write_text(artifacts.get("full_prompt", ""), encoding="utf-8")
    (out_dir / "response.md").write_text(artifacts.get("response", ""), encoding="utf-8")

    serializable = {k: v for k, v in artifacts.items() if k not in ("full_prompt", "response")}
    (out_dir / "analysis.json").write_text(
        json.dumps(serializable, indent=2, default=str), encoding="utf-8"
    )

    summary_lines = [
        f"# End-to-end run summary",
        f"",
        f"- Started: {artifacts['started_at']}",
        f"- Finished: {artifacts['finished_at']}",
        f"- Ollama model: {artifacts['ollama_model']}",
        f"- Ollama URL: {artifacts['ollama_url']}",
        f"- Generation time: {artifacts['elapsed_seconds']:.1f}s",
        f"- Prompt length: {len(artifacts.get('full_prompt',''))} chars",
        f"- Response length: {len(artifacts.get('response',''))} chars",
        f"",
        f"## Files",
        f"- transcript.txt - full stdout of the run",
        f"- prompt.txt - the full assembled Ollama prompt",
        f"- response.md - the final LLM response",
        f"- analysis.json - structured personality/Nestor/LP/state/analysis",
    ]
    (out_dir / "README.md").write_text("\n".join(summary_lines), encoding="utf-8")

    print(f"\n[saver] DONE. Artifacts in: {out_dir}")
    for f in sorted(out_dir.iterdir()):
        print(f"   - {f.name}  ({f.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
