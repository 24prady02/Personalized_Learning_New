"""
Full-stack demo — every trained component fires on one session.

Components exercised (checkpoints used):
  1. Text -> Big Five           (checkpoints/text_personality.pt)
  2. Nestor CPTs v2              (data/nestor/nestor_cpts.json)
  3. BehavioralHMM (Baum-Welch)  (checkpoints/behavioral_hmm.json)
  4. Emotion classifier MLP      (checkpoints/emotion_classifier.pt)
  5. BehavioralRNN (pretrained)  (checkpoints/best.pt — loaded via server.py)
  6. BKT mastery update          (probabilistic, no checkpoint)
  7. LPIndex + enforcement       (data/pedagogical_kg/learning_progressions.json)
  8. RL teaching agent DQN       (checkpoints/rl_teaching_agent.pt)
  9. EnhancedPersonalizedGenerator -> Ollama qwen2.5-coder:7b  (streaming)

The input is one session:
    student_message + code + action_sequence (simulated realistic debug trail)
Each component's contribution is printed before the LLM call so the
provenance of every signal in the final response is visible.
"""
import sys, os, time, json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "3")

import numpy as np
import torch
import torch.nn as nn

from src.models.nestor.nestor_bayesian_profiler import NestorBayesianProfiler
from src.models.behavioral import BehavioralHMM, BehavioralRNN
from src.models.hvsae import HVSAE
from src.student_modeling.bayesian_knowledge_tracing import BayesianKnowledgeTracer
from src.reinforcement_learning.teaching_agent import TeachingRLAgent
from src.knowledge_graph.lp_index import LPIndex
from src.orchestrator.enhanced_personalized_generator import EnhancedPersonalizedGenerator


# ─── Session inputs ──────────────────────────────────────────────────────────
STUDENT_MESSAGE = (
    "My Java program keeps crashing with NullPointerException. I created a "
    "Room object but calling describe() on it blows up. I've tried adding "
    "initializers but nothing works. Can you help me figure out what I'm "
    "missing?"
)
STUDENT_CODE = (
    "public class Game {\n"
    "    Room currentRoom;\n"
    "    public void start() { currentRoom.describe(); }\n"
    "}"
)
# A realistic debugging trajectory this student went through
ACTION_SEQUENCE = [
    "File.Open",        "File.Edit",        "Run.Program",
    "Run.Error",        "File.Edit",        "Run.Program",
    "Run.Error",        "Webpage.Open",     "Resource.View",
    "File.Edit",        "Run.Program",      "Compile.Error",
    "File.Edit",        "Run.Program",      "Run.Error",
]
TIME_DELTAS = [10, 45, 2, 1, 60, 2, 1, 30, 120, 90, 2, 1, 30, 2, 1]
TARGET_CONCEPT = "null_pointer"  # from concept extraction on code+error

# Prior BKT mastery on this student (what the system has learned about them)
PRIOR_MASTERY = {
    "type_mismatch": 0.85,
    "infinite_loop": 0.80,
    "null_pointer":  0.30,
}

EMOTION_CLASSES = ['neutral', 'confused', 'frustrated', 'engaged', 'understanding']


def load_emotion_mlp():
    data = torch.load("checkpoints/emotion_classifier.pt",
                      weights_only=False, map_location='cpu')
    model = nn.Sequential(
        nn.Linear(7, 64), nn.ReLU(), nn.Dropout(0.2),
        nn.Linear(64, 64), nn.ReLU(), nn.Dropout(0.2),
        nn.Linear(64, 5),
    )
    sd = {k.replace("net.", ""): v for k, v in data["state_dict"].items()}
    model.load_state_dict(sd)
    model.eval()
    return model, data.get("classes", EMOTION_CLASSES)


def rnn_analyze(action_sequence, time_deltas, ckpt):
    """Run the pretrained BehavioralRNN — returns emotion label + effectiveness."""
    try:
        rnn = BehavioralRNN({
            'behavioral': {'num_actions': 20, 'action_embedding_dim': 32,
                           'hidden_dim': 64, 'num_layers': 2}
        })
        # best.pt bundles multiple models under 'behavioral_rnn_state'
        if 'behavioral_rnn_state' in ckpt:
            rnn.load_state_dict(ckpt['behavioral_rnn_state'], strict=False)
        rnn.eval()

        action_ids = torch.tensor([[BehavioralRNN.action_to_id(a)
                                    for a in action_sequence]], dtype=torch.long)
        t_d = torch.tensor([time_deltas], dtype=torch.float)
        out = torch.zeros_like(action_ids, dtype=torch.float)
        lengths = torch.tensor([len(action_sequence)], dtype=torch.long)
        a = rnn.analyze_strategy(action_ids, t_d, out, lengths)
        def _first(x): return x[0] if isinstance(x, list) else x
        return {
            "emotion": _first(a.get("emotion", ["neutral"])),
            "emotion_confidence": _first(a.get("emotion_confidence", [0.5])),
            "effectiveness": _first(a.get("effectiveness", [0.5])),
            "productivity":  _first(a.get("productivity", ["medium"])),
            "loaded": True,
        }
    except Exception as e:
        return {"loaded": False, "error": str(e)}


# ─── HVSAE tokenizers (simple, bounded by trained vocab sizes) ───────────────

def tokenize_code(code: str, max_len: int = 256, vocab: int = 8000):
    """Char-level bucket hash into CodeEncoder's vocab."""
    ids = [(ord(c) % (vocab - 1)) + 1 for c in code[:max_len]]
    while len(ids) < 32:   # min length so BiLSTM has something
        ids.append(0)
    return torch.tensor([ids], dtype=torch.long)


def tokenize_text(text: str, max_len: int = 128, vocab: int = 6000):
    """Word-level bucket hash into TextEncoder's vocab."""
    toks = text.lower().split()[:max_len]
    ids = [(abs(hash(t)) % (vocab - 1)) + 1 for t in toks]
    while len(ids) < 16:
        ids.append(0)
    return torch.tensor([ids], dtype=torch.long)


def tokenize_actions(action_sequence, max_len: int = 64):
    """Map action names to 0-19 IDs via BehavioralRNN.action_to_id."""
    ids = [BehavioralRNN.action_to_id(a) for a in action_sequence[:max_len]]
    while len(ids) < 8:
        ids.append(0)
    return torch.tensor([ids], dtype=torch.long)


def run_hvsae(code, text, actions, ckpt):
    """Load HVSAE from hvsae_state, encode the session, return latent+misconceptions."""
    try:
        model = HVSAE({'hvsae': {'beta': 0.1}})
        if 'hvsae_state' in ckpt:
            model.load_state_dict(ckpt['hvsae_state'], strict=False)
        model.eval()
        batch = {
            'code_tokens':     tokenize_code(code),
            'text_tokens':     tokenize_text(text),
            'action_sequence': tokenize_actions(actions),
        }
        with torch.no_grad():
            out = model(batch)
        return {
            "loaded":           True,
            "latent":           out['latent'].squeeze(0),      # (256,)
            "attention":        out['attention_weights'].squeeze(0).tolist(),
            "misconception_logits": out['misconception_logits'].squeeze(0),
        }
    except Exception as e:
        return {"loaded": False, "error": str(e),
                "latent": torch.zeros(256)}


# ─── Orchestrate every component ─────────────────────────────────────────────

def run():
    print("=" * 80)
    print("FULL-STACK DEMO — every trained component fires on one session")
    print("=" * 80)

    # ── 1. Text -> Big Five + Nestor CPTs ────────────────────────────────────
    nestor = NestorBayesianProfiler({"nestor": {"data_dir": "data/nestor"}})
    nestor_out = nestor.infer_from_prompt(STUDENT_MESSAGE)
    p = nestor_out["personality"]
    print(f"\n[1] TEXT-PERSONALITY (checkpoints/text_personality.pt)")
    print(f"    Big Five : " + "  ".join(
        f"{k[:3]}={p[k]:.2f}" for k in
        ('openness','conscientiousness','extraversion','agreeableness','neuroticism')))

    print(f"\n[2] NESTOR CPTs v2 (data/nestor/nestor_cpts.json)")
    print(f"    styles   : {nestor_out['learning_styles']['visual_verbal']}/"
          f"{nestor_out['learning_styles']['sensing_intuitive']}/"
          f"{nestor_out['learning_styles']['active_reflective']}/"
          f"{nestor_out['learning_styles']['sequential_global']}")
    print(f"    strat    : "
          + "  ".join(f"{k[:4]}={v:.2f}" for k, v in
                      nestor_out['learning_strategies'].items()
                      if k.endswith('_score')))
    print(f"    interv   : {nestor_out['intervention_preference']}")
    print(f"    elements : {nestor_out['recommended_elements']}")

    # ── 3. BehavioralHMM on action sequence ──────────────────────────────────
    hmm = BehavioralHMM({'behavioral':
                         {'hmm_checkpoint': 'checkpoints/behavioral_hmm.json'}})
    hmm_out = hmm.analyze_session(ACTION_SEQUENCE)
    print(f"\n[3] BEHAVIORAL HMM (Baum-Welch trained, checkpoints/behavioral_hmm.json)")
    print(f"    final state    : {hmm_out['final_state']}")
    print(f"    confidence     : {hmm_out['final_confidence']:.3f}")

    # ── 4. Emotion classifier MLP on HMM feature window ──────────────────────
    emo_model, emo_classes = load_emotion_mlp()
    feats = hmm._extract_features(ACTION_SEQUENCE)
    last_feat = torch.from_numpy(feats[-1]).float().unsqueeze(0)
    with torch.no_grad():
        probs = torch.softmax(emo_model(last_feat), dim=1).squeeze(0).tolist()
    emo_idx = int(np.argmax(probs))
    emo_label = emo_classes[emo_idx]
    print(f"\n[4] EMOTION MLP (checkpoints/emotion_classifier.pt)")
    print(f"    predicted emotion : {emo_label}  ({probs[emo_idx]*100:.0f}% confidence)")
    print(f"    distribution      : "
          + "  ".join(f"{c}:{probs[i]*100:.0f}%" for i, c in enumerate(emo_classes)))

    # ── 5a. HVSAE tri-stream encoder ─────────────────────────────────────────
    ckpt_bestpt = torch.load("checkpoints/best.pt", weights_only=False, map_location='cpu')
    hv = run_hvsae(STUDENT_CODE, STUDENT_MESSAGE, ACTION_SEQUENCE, ckpt_bestpt)
    print(f"\n[5a] HVSAE tri-stream encoder (checkpoints/best.pt > hvsae_state)")
    if hv["loaded"]:
        print(f"    latent shape          : {tuple(hv['latent'].shape)}")
        print(f"    fusion attention      : "
              f"code={hv['attention'][0]:.2f}  "
              f"text={hv['attention'][1]:.2f}  "
              f"action={hv['attention'][2]:.2f}")
        ml = hv['misconception_logits']
        top = torch.topk(torch.sigmoid(ml), k=3)
        print(f"    top-3 misconception probs (of 20 concept heads): "
              f"{[(int(i), round(v.item(), 3)) for i, v in zip(top.indices, top.values)]}")
    else:
        print(f"    load failed: {hv['error'][:100]}")

    # ── 5b. BehavioralRNN ─────────────────────────────────────────────────────
    rnn_out = rnn_analyze(ACTION_SEQUENCE, TIME_DELTAS, ckpt_bestpt)
    print(f"\n[5b] BEHAVIORAL RNN (checkpoints/best.pt > behavioral_rnn_state)")
    if rnn_out.get("loaded"):
        print(f"    emotion        : {rnn_out['emotion']} "
              f"({rnn_out['emotion_confidence']:.2f})")
        print(f"    effectiveness  : {rnn_out['effectiveness']:.2f}")
        print(f"    productivity   : {rnn_out['productivity']}")
    else:
        print(f"    not loaded ({rnn_out.get('error','')[:80]}) — "
              f"HMM+Emotion MLP already cover this signal path")

    # ── 6. BKT mastery update ────────────────────────────────────────────────
    bkt = BayesianKnowledgeTracer()
    bkt.initialize_student("demo_student", list(PRIOR_MASTERY.keys()))
    # seed prior mastery
    for skill, m in PRIOR_MASTERY.items():
        bkt.student_states["demo_student"][skill]["p_learned"] = m
    # the last Run.Error on the target concept is negative evidence
    bkt_update = bkt.update_knowledge("demo_student", TARGET_CONCEPT,
                                      is_correct=False)
    new_mastery_dict = {
        s: bkt.student_states["demo_student"][s]["p_learned"]
        for s in PRIOR_MASTERY
    }
    print(f"\n[6] BKT MASTERY UPDATE (src/student_modeling/bayesian_knowledge_tracing.py)")
    print(f"    target concept : {TARGET_CONCEPT}")
    print(f"    before update  : {PRIOR_MASTERY[TARGET_CONCEPT]:.3f}")
    print(f"    after failure  : {new_mastery_dict[TARGET_CONCEPT]:.3f}")

    # ── 7. LP query with the updated mastery ─────────────────────────────────
    lp_idx = LPIndex()
    lp_path = lp_idx.get_path(TARGET_CONCEPT, new_mastery_dict)
    print(f"\n[7] LEARNING PROGRESSION (data/pedagogical_kg/learning_progressions.json)")
    print(f"    progression   : {lp_path['progression_id']}")
    print(f"    target        : {lp_path['target_concept']}")
    print(f"    next concept  : {lp_path['next_concept']}")
    print(f"    on_track      : {lp_path['on_track']}  "
          f"(enforcement will {'fire' if not lp_path['on_track'] else 'not fire'})")

    # ── 8. RL agent picks the intervention ───────────────────────────────────
    rl = TeachingRLAgent({"rl": {"checkpoint": "checkpoints/rl_teaching_agent.pt"}},
                         models={})
    fake_analysis = {
        'encoding': {'latent': hv['latent']},      # real HVSAE latent (256,)
        'cognitive': {'knowledge_gaps': [
            {'mastery': new_mastery_dict[TARGET_CONCEPT]}
        ]},
        'behavioral': {'emotional_state': emo_label
                       if emo_label in ['frustrated','engaged','confused']
                       else 'confused'},
        'psychological': {'personality': p},
        'history': {'interventions': []},
    }
    session_for_rl = {
        'time_stuck': sum(TIME_DELTAS),
        'action_sequence': ACTION_SEQUENCE,
    }
    state_vec = rl.get_state_representation(session_for_rl, fake_analysis)
    with torch.no_grad():
        q = rl.policy_net(state_vec.unsqueeze(0))
        rl_action_idx = int(q.argmax().item())
    rl_action_name = rl.actions[rl_action_idx]
    print(f"\n[8] RL TEACHING AGENT (checkpoints/rl_teaching_agent.pt, DQN)")
    print(f"    epsilon        : {rl.epsilon:.2f} (exploit mode)")
    print(f"    selected action: {rl_action_name}")
    print(f"    top-3 Q-values : "
          + ", ".join(f"{rl.actions[i]}:{q[0,i].item():+.2f}"
                      for i in q[0].argsort(descending=True)[:3].tolist()))

    # ── Build the generator's state + analysis ───────────────────────────────
    # Map RL action to the intervention-map keys the generator knows
    rl_to_generator_interv = {
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
    generator_interv = rl_to_generator_interv.get(rl_action_name, 'worked_example')

    student_state = {
        'interaction_count': 1,
        'personality':       p,
        'knowledge_state':   {
            'overall_mastery': float(np.mean(list(new_mastery_dict.values()))),
            'mastery_history': [PRIOR_MASTERY[TARGET_CONCEPT],
                                new_mastery_dict[TARGET_CONCEPT]],
        },
        'interests': [],
        'psychological_graph': {
            'attribution':   'internal_unstable',
            'self_efficacy': 'moderate',
            'srl_phase':     'monitoring',
            'imposter_flag': False,
            'high_anxiety':  p['neuroticism'] > 0.55,
            'flow_state':    hmm_out['final_state'] in ['making_progress','understanding'],
        },
        'progression_graph': {'stage': 3, 'zpd_status': 'within',
                              'scaffold_level': 3, 'has_attempt': True},
        'content_channel':   {'encoding_strength': 'partial',
                              'dual_coding': 'verbal_only',
                              'elaboration': False},
        'recommended_intervention': {
            'type':      generator_interv,
            'rationale': f"RL agent selected '{rl_action_name}' (mapped to "
                         f"'{generator_interv}') for HMM={hmm_out['final_state']}, "
                         f"emotion={emo_label}",
        },
    }
    analysis = {
        'emotion':           emo_label,
        'frustration_level': float(p['neuroticism']),
        'engagement_score':  float(0.5 + 0.2 *
                                    (1 if emo_label == 'engaged' else 0)),
        'bkt_update': {
            'p_learned_before': PRIOR_MASTERY[TARGET_CONCEPT],
            'p_learned_after':  new_mastery_dict[TARGET_CONCEPT],
        },
        'cse_kg': {
            'concept': 'null_pointer',
            'prerequisites': ['references', 'object instantiation', 'heap vs stack'],
            'related_concepts': ['NullPointerException', 'Optional', 'default field values'],
            'definition': 'Accessing a member via a reference whose value is null '
                          '— the JVM throws NullPointerException because there is '
                          'no object on the heap to dereference.',
        },
        'pedagogical_kg': {
            'progression': 'declare ref -> new to allocate -> dereference safely',
            'misconceptions': [
                'declaring a reference also creates the object',
                'Java auto-initializes fields to usable defaults',
                'null means "no value" rather than "no allocation"',
            ],
            'cognitive_load': 'medium',
            'interventions': ['worked example', 'heap diagram'],
            'learning_path':  lp_path,        # <-- LP path from step 7
        },
        'coke': {
            'cognitive_state': emo_label,     # <-- from emotion MLP (step 4)
            'mental_activity': 'debugging reference failure',
            'behavioral_response': 'persistent — multiple attempts',
            'confidence':          probs[emo_idx],
            'cognitive_chain': {
                'description': f"HMM says '{hmm_out['final_state']}'; "
                               f"emotion MLP says '{emo_label}'. Student has run "
                               f"into repeated Run.Errors. RL picked "
                               f"'{rl_action_name}' to break the loop.",
            },
        },
    }

    # ── 9. Ollama generation ─────────────────────────────────────────────────
    gen = EnhancedPersonalizedGenerator()
    print(f"\n[9] OLLAMA GENERATION  (model={gen._ollama_model}, streaming)")
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
        student_id='demo_student',
        student_message=STUDENT_MESSAGE,
        student_state=student_state,
        analysis=analysis,
        code=STUDENT_CODE,
    )
    total = time.time() - t0
    print("\n" + "-" * 80)
    print(f"TTFT={first[0]:.1f}s  total={total:.1f}s  {len(resp)} chars")

    # ── Summary: what each component contributed ─────────────────────────────
    print("\n" + "=" * 80)
    print("PROVENANCE — which trained component drove which part of the output")
    print("=" * 80)
    print(f"  TEXT-PERSONALITY   -> neuroticism={p['neuroticism']:.2f} shaped opening tone")
    print(f"  NESTOR CPTs        -> style/strategy drove format choices")
    print(f"  HMM                -> state '{hmm_out['final_state']}' set psychological_graph")
    print(f"  EMOTION MLP        -> '{emo_label}' used as coke.cognitive_state")
    if hv.get("loaded"):
        print(f"  HVSAE              -> 256-dim latent fed to RL agent, "
              f"gating code/text/action={tuple(round(w,2) for w in hv['attention'])}")
    if rnn_out.get("loaded"):
        print(f"  BEHAVIORAL RNN     -> '{rnn_out['emotion']}' cross-check")
    print(f"  BKT                -> {TARGET_CONCEPT} mastery "
          f"{PRIOR_MASTERY[TARGET_CONCEPT]:.2f} -> {new_mastery_dict[TARGET_CONCEPT]:.2f}")
    print(f"  LPINDEX            -> path to '{TARGET_CONCEPT}', "
          f"on_track={lp_path['on_track']}")
    print(f"  RL AGENT           -> chose '{rl_action_name}' -> "
          f"generator intervention '{generator_interv}'")


if __name__ == "__main__":
    run()
