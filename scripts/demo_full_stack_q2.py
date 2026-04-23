"""
Full-stack demo #2 — different question, different student, different signals.

New scenario:
  Question  : Java string comparison bug (== vs .equals())
  Personality tone: methodical, curious — not anxious
  Action seq: shorter, fewer errors — student iterates quickly
  Mastery   : advanced beginner — has null_pointer mastered, target is
              string_equality which is the actual Week-2 concept here
"""
import sys, os, time, json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "3")

import numpy as np
import torch

# Reuse every helper from the canonical demo
sys.path.insert(0, str(Path(__file__).parent))
from demo_full_stack import (
    load_emotion_mlp, rnn_analyze, run_hvsae, EMOTION_CLASSES,
)
from src.models.nestor.nestor_bayesian_profiler import NestorBayesianProfiler
from src.models.behavioral import BehavioralHMM
from src.student_modeling.bayesian_knowledge_tracing import BayesianKnowledgeTracer
from src.reinforcement_learning.teaching_agent import TeachingRLAgent
from src.knowledge_graph.lp_index import LPIndex
from src.orchestrator.enhanced_personalized_generator import EnhancedPersonalizedGenerator


# ─── Fresh inputs for this session ────────────────────────────────────────────
STUDENT_MESSAGE = (
    "Quick Java question — I'm reading user input and comparing it to a "
    "literal, but the if-branch never fires even when I type exactly what "
    "it should match. I've tried trimming the string and printing it out "
    "to check, and it looks identical. What am I missing about how Java "
    "compares strings under the hood?"
)
STUDENT_CODE = (
    "import java.util.Scanner;\n"
    "\n"
    "public class Greeter {\n"
    "    public static void main(String[] args) {\n"
    "        Scanner sc = new Scanner(System.in);\n"
    "        String answer = sc.nextLine().trim();\n"
    "        if (answer == \"yes\") {\n"
    "            System.out.println(\"great!\");\n"
    "        } else {\n"
    "            System.out.println(\"ok, maybe next time\");\n"
    "        }\n"
    "    }\n"
    "}"
)
ACTION_SEQUENCE = [
    "File.Open",        "File.Edit",        "Run.Program",
    "Run.Error",        "File.Edit",        "Run.Program",
    "Run.Error",        "Webpage.Open",     "Resource.View",
    "Webpage.Close",    "File.Edit",        "Run.Program",
]
TIME_DELTAS = [5, 60, 2, 1, 45, 2, 1, 20, 180, 15, 55, 2]
TARGET_CONCEPT = "string_equality"

# This student has mastered earlier Week-2 stuff but string_equality is new
PRIOR_MASTERY = {
    "type_mismatch":  0.88,
    "infinite_loop":  0.80,
    "null_pointer":   0.78,
    "string_equality": 0.25,
}


def run():
    print("=" * 80)
    print("FULL-STACK DEMO #2 — string-equality bug, curious/methodical student")
    print("=" * 80)

    # 1+2. Text-personality + Nestor
    nestor = NestorBayesianProfiler({"nestor": {"data_dir": "data/nestor"}})
    n_out = nestor.infer_from_prompt(STUDENT_MESSAGE)
    p = n_out["personality"]
    print(f"\n[1] TEXT-PERSONALITY (MiniLM fine-tuned on Essays)")
    print(f"    Big Five : " + "  ".join(
        f"{k[:3]}={p[k]:.2f}" for k in
        ('openness','conscientiousness','extraversion','agreeableness','neuroticism')))

    print(f"\n[2] NESTOR CPTs v2")
    print(f"    styles       : {n_out['learning_styles']['visual_verbal']}/"
          f"{n_out['learning_styles']['sensing_intuitive']}/"
          f"{n_out['learning_styles']['active_reflective']}/"
          f"{n_out['learning_styles']['sequential_global']}")
    print(f"    intervention : {n_out['intervention_preference']}")
    print(f"    elements     : {n_out['recommended_elements']}")

    # 3. HMM
    hmm = BehavioralHMM({'behavioral': {'hmm_checkpoint': 'checkpoints/behavioral_hmm.json'}})
    h = hmm.analyze_session(ACTION_SEQUENCE)
    print(f"\n[3] HMM state : {h['final_state']}  (conf {h['final_confidence']:.2f})")

    # 4. Emotion MLP
    emo_model, emo_classes = load_emotion_mlp()
    feats = hmm._extract_features(ACTION_SEQUENCE)
    last = torch.from_numpy(feats[-1]).float().unsqueeze(0)
    with torch.no_grad():
        probs = torch.softmax(emo_model(last), dim=1).squeeze(0).tolist()
    emo_label = emo_classes[int(np.argmax(probs))]
    print(f"\n[4] EMOTION MLP : {emo_label}  ({max(probs)*100:.0f}%)")
    print(f"    dist: " + "  ".join(
        f"{c}:{probs[i]*100:.0f}%" for i, c in enumerate(emo_classes)))

    # 5a. HVSAE
    ckpt = torch.load("checkpoints/best.pt", weights_only=False, map_location='cpu')
    hv = run_hvsae(STUDENT_CODE, STUDENT_MESSAGE, ACTION_SEQUENCE, ckpt)
    print(f"\n[5a] HVSAE : latent {tuple(hv['latent'].shape)}  "
          f"gate code={hv['attention'][0]:.2f} text={hv['attention'][1]:.2f} action={hv['attention'][2]:.2f}")
    top = torch.topk(torch.sigmoid(hv['misconception_logits']), k=3)
    print(f"    top-3 misconception heads: "
          + "  ".join(f"#{int(i)}:{v.item():.2f}" for i, v in zip(top.indices, top.values)))

    # 5b. RNN
    r = rnn_analyze(ACTION_SEQUENCE, TIME_DELTAS, ckpt)
    print(f"\n[5b] RNN   : emotion={r['emotion']}  eff={r['effectiveness']:.2f}  prod={r['productivity']}")

    # 6. BKT
    bkt = BayesianKnowledgeTracer()
    bkt.initialize_student("s2", list(PRIOR_MASTERY.keys()))
    for sk, m in PRIOR_MASTERY.items():
        bkt.student_states["s2"][sk]["p_learned"] = m
    bkt.update_knowledge("s2", TARGET_CONCEPT, is_correct=False)
    post = {sk: bkt.student_states["s2"][sk]["p_learned"] for sk in PRIOR_MASTERY}
    print(f"\n[6] BKT    : {TARGET_CONCEPT} "
          f"{PRIOR_MASTERY[TARGET_CONCEPT]:.2f} -> {post[TARGET_CONCEPT]:.2f}")

    # 7. LP
    lp = LPIndex().get_path(TARGET_CONCEPT, post)
    print(f"\n[7] LP     : next={lp['next_concept']}  on_track={lp['on_track']}  "
          f"(enforcement {'FIRES' if not lp['on_track'] else 'skipped'})")

    # 8. RL
    rl = TeachingRLAgent({"rl": {"checkpoint": "checkpoints/rl_teaching_agent.pt"}},
                         models={})
    rl_analysis = {
        'encoding': {'latent': hv['latent']},
        'cognitive': {'knowledge_gaps': [{'mastery': post[TARGET_CONCEPT]}]},
        'behavioral': {'emotional_state':
            emo_label if emo_label in ['frustrated','engaged','confused'] else 'confused'},
        'psychological': {'personality': p},
        'history': {'interventions': []},
    }
    rl_session = {'time_stuck': sum(TIME_DELTAS), 'action_sequence': ACTION_SEQUENCE}
    state_vec = rl.get_state_representation(rl_session, rl_analysis)
    with torch.no_grad():
        q = rl.policy_net(state_vec.unsqueeze(0))
        rl_idx = int(q.argmax().item())
    rl_action = rl.actions[rl_idx]
    top3_q = q[0].argsort(descending=True)[:3].tolist()
    print(f"\n[8] RL     : picks '{rl_action}'  "
          f"top-3 Q: "
          + ", ".join(f"{rl.actions[i]}:{q[0,i].item():+.2f}" for i in top3_q))

    # Build state+analysis for the generator
    rl_to_gen = {
        'visual_explanation': 'worked_example',
        'worked_example':     'worked_example',
        'conceptual_deepdive':'validate_and_advance',
        'motivational_support':'attribution_reframe',
        'interactive_exercise':'transfer_task',
        'guided_practice':    'worked_example',
        'challenge_problem':  'increase_challenge',
        'spaced_review':      'validate_and_advance',
        'error_analysis':     'worked_example',
        'peer_comparison':    'mastery_surface',
    }
    gen_interv = rl_to_gen.get(rl_action, 'worked_example')

    student_state = {
        'interaction_count': 1,
        'personality':       p,
        'knowledge_state':   {
            'overall_mastery': float(np.mean(list(post.values()))),
            'mastery_history': [PRIOR_MASTERY[TARGET_CONCEPT], post[TARGET_CONCEPT]],
        },
        'interests': [],
        'psychological_graph': {
            'attribution': 'internal_unstable', 'self_efficacy': 'growth',
            'srl_phase': 'forethought', 'imposter_flag': False,
            'high_anxiety': p['neuroticism'] > 0.55,
            'flow_state': h['final_state'] in ['making_progress','understanding'],
        },
        'progression_graph': {'stage': 3, 'zpd_status': 'within',
                              'scaffold_level': 3, 'has_attempt': True},
        'content_channel': {'encoding_strength': 'partial',
                            'dual_coding': 'verbal_only', 'elaboration': True},
        'recommended_intervention': {
            'type': gen_interv,
            'rationale': f"RL '{rl_action}' -> generator '{gen_interv}', "
                         f"HMM={h['final_state']}, emotion MLP={emo_label}",
        },
    }
    analysis = {
        'emotion': emo_label, 'frustration_level': float(p['neuroticism']),
        'engagement_score': 0.7,
        'bkt_update': {'p_learned_before': PRIOR_MASTERY[TARGET_CONCEPT],
                       'p_learned_after':  post[TARGET_CONCEPT]},
        'cse_kg': {
            'concept': 'string_equality',
            'prerequisites': ['references', 'object vs primitive', 'intern pool'],
            'related_concepts': ['.equals()', 'String.intern()', 'hashCode/equals contract'],
            'definition': 'In Java, == compares reference identity for '
                          'objects; .equals() compares logical content. '
                          'String literals may share references via the '
                          'intern pool, which makes == appear to work by '
                          'accident, but Scanner.nextLine() returns a fresh '
                          'String object so == fails.',
        },
        'pedagogical_kg': {
            'progression': 'value vs reference -> == for refs -> .equals() for content',
            'misconceptions': [
                '== compares string content (it does not)',
                'since literals compare with ==, all strings do',
                'trim() fixes comparison (it does not — still returns a new object)',
            ],
            'cognitive_load': 'medium',
            'interventions': ['worked example', 'heap trace'],
            'learning_path': lp,
        },
        'coke': {
            'cognitive_state': emo_label,
            'mental_activity': 'debugging equality check',
            'behavioral_response': 'persistent, non-anxious',
            'confidence': float(max(probs)),
            'cognitive_chain': {
                'description': f"HMM={h['final_state']}, Emotion MLP={emo_label}, "
                               f"HVSAE gate=action-weighted, RL picks {rl_action}. "
                               f"Student tried trim/print — is genuinely exploring."
            },
        },
    }

    # 9. Generation
    gen = EnhancedPersonalizedGenerator()
    print(f"\n[9] OLLAMA ({gen._ollama_model}, streaming)")
    print("-" * 80)
    first = [None]
    t0 = time.time()
    def on_tok(s):
        if first[0] is None:
            first[0] = time.time() - t0
            print(f"[TTFT={first[0]:.1f}s] ", end="", flush=True)
        print(s, end="", flush=True)
    gen._stream_callback = on_tok
    resp = gen.generate_personalized_response(
        student_id='s2', student_message=STUDENT_MESSAGE,
        student_state=student_state, analysis=analysis, code=STUDENT_CODE,
    )
    total = time.time() - t0
    print("\n" + "-" * 80)
    print(f"TTFT={first[0]:.1f}s  total={total:.1f}s  {len(resp)} chars")

    print("\n" + "=" * 80)
    print("PROVENANCE — how each trained component shaped this response")
    print("=" * 80)
    print(f"  TEXT-PERSONALITY : openness={p['openness']:.2f}, neuroticism={p['neuroticism']:.2f}")
    print(f"  NESTOR           : {n_out['learning_styles']['visual_verbal']}/"
          f"{n_out['learning_styles']['active_reflective']} style, "
          f"interv={n_out['intervention_preference']}")
    print(f"  HMM              : {h['final_state']}")
    print(f"  EMOTION MLP      : {emo_label}")
    print(f"  HVSAE            : action-weighted fusion (gate={hv['attention'][2]:.2f})")
    print(f"  RNN              : emotion={r['emotion']} eff={r['effectiveness']:.2f}")
    print(f"  BKT              : {TARGET_CONCEPT} {PRIOR_MASTERY[TARGET_CONCEPT]:.2f} -> {post[TARGET_CONCEPT]:.2f}")
    print(f"  LP               : on_track={lp['on_track']} (target reached)")
    print(f"  RL               : {rl_action}")


if __name__ == "__main__":
    run()
