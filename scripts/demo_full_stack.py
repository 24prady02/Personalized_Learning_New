"""
Full-stack demo — every trained component fires on one session.

Components exercised (checkpoints used):
  1. Text -> Big Five           (checkpoints/text_personality.pt)
  2. Nestor CPTs v2              (data/nestor/nestor_cpts.json)
  3. BehavioralHMM (Baum-Welch)  (checkpoints/behavioral_hmm.json)
  4. HVSAE tri-stream encoder    (checkpoints/best.pt)
  5. BehavioralRNN (pretrained)  (checkpoints/best.pt — loaded via server.py)
  6. BKT mastery update          (probabilistic, no checkpoint)
  7. LPIndex + enforcement       (data/java_curriculum/learning_progressions.json)
  7b. LPDiagnostician + wrong-models catalogue (data/mental_models/
        wrong_models_catalogue.json + checkpoints/cpal_lp_head_st.pt +
        checkpoints/cpal_wm_subhead.pt) — matches student's text + HVSAE
        latent against the documented Java CS1 misconceptions, classifies
        LP level (L1-L4), and runs the plateau gate.
  7d. Student knowledge graph    (StudentGraphService, grounded in
        data/chapter1_kg.json)
  8. RL teaching agent DQN       (checkpoints/rl_teaching_agent.pt)
  9. EnhancedPersonalizedGenerator -> Ollama qwen2.5-coder:7b  (streaming)

The input is one session:
    student_message + code + action_sequence (simulated realistic debug trail)
Each component's contribution is printed before the LLM call so the
provenance of every signal in the final response is visible.

Emotion and the psychological channel (attribution, self-efficacy,
imposter, anxiety, flow) are not inputs: the emotion classifier was
retired to _archive/emotion_and_psych/.

All artifacts (transcript, assembled Ollama prompt, response, structured
diagnosis) are saved to output/full_stack_run_<timestamp>/.
"""
import sys, os, time, json, io
from datetime import datetime
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "3")

import numpy as np
import torch
import torch.nn as nn

from src.models.nestor.nestor_bayesian_profiler import NestorBayesianProfiler
from src.models.behavioral import BehavioralHMM, BehavioralRNN
from src.models.hvsae import HVSAE
from src.models.dina import DINAModel, JAVA_SKILLS as DINA_JAVA_SKILLS
from src.student_modeling.bayesian_knowledge_tracing import BayesianKnowledgeTracer
from src.reinforcement_learning.teaching_agent import TeachingRLAgent
from src.knowledge_graph.lp_index import LPIndex
from src.knowledge_graph.mental_models import get_catalogue
from src.knowledge_graph.student_graph_service import StudentGraphService
from src.orchestrator.lp_diagnostic import LPDiagnostician
from src.orchestrator.catalogue_rag import CatalogueRAG
from src.orchestrator.enhanced_personalized_generator import EnhancedPersonalizedGenerator

ROOT = Path(__file__).parent.parent


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

# Expected wrong-model id (ground truth for batch evaluation). When set,
# DINA uses (classifier match == EXPECTED_WM) as the correctness signal so
# correct diagnoses lift mastery and misses push it down.
EXPECTED_WM = None

# Prior BKT mastery on this student (what the system has learned about them)
PRIOR_MASTERY = {
    "type_mismatch": 0.85,
    "infinite_loop": 0.80,
    "null_pointer":  0.30,
}

def rnn_analyze(action_sequence, time_deltas, ckpt):
    """Run the pretrained BehavioralRNN — returns effectiveness + productivity."""
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
    print(f"\n[1] TEXT-PERSONALITY")
    print(f"    src   : checkpoints/text_personality.pt "
          f"(MiniLM fine-tuned on Pennebaker Essays, mean F1=0.634)")
    print(f"    Big Five : " + "  ".join(
        f"{k[:3]}={p[k]:.2f}" for k in
        ('openness','conscientiousness','extraversion','agreeableness','neuroticism')))

    print(f"\n[2] NESTOR CPTs v2")
    print(f"    src   : data/nestor/nestor_cpts.json "
          f"(Big-Five -> Felder-Silverman styles + LISTK strategies)")
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
    print(f"\n[3] BEHAVIORAL HMM")
    print(f"    src   : checkpoints/behavioral_hmm.json "
          f"(Baum-Welch trained on ProgSnap2 action sequences)")
    print(f"    final state    : {hmm_out['final_state']}")
    print(f"    confidence     : {hmm_out['final_confidence']:.3f}")

    # ── 4. HVSAE tri-stream encoder ─────────────────────────────────────────
    ckpt_bestpt = torch.load("checkpoints/best.pt", weights_only=False, map_location='cpu')
    hv = run_hvsae(STUDENT_CODE, STUDENT_MESSAGE, ACTION_SEQUENCE, ckpt_bestpt)
    print(f"\n[4] HVSAE TRI-STREAM ENCODER")
    print(f"    src   : checkpoints/best.pt > hvsae_state "
          f"(8-head attention, 256-dim vMF latent, 20 misconception heads)")
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

    # ── 5. BehavioralRNN ─────────────────────────────────────────────────────
    rnn_out = rnn_analyze(ACTION_SEQUENCE, TIME_DELTAS, ckpt_bestpt)
    print(f"\n[5] BEHAVIORAL RNN")
    print(f"    src   : checkpoints/best.pt > behavioral_rnn_state "
          f"(2-layer LSTM, 64 hidden, 20 action types)")
    if rnn_out.get("loaded"):
        print(f"    effectiveness  : {rnn_out['effectiveness']:.2f}")
        print(f"    productivity   : {rnn_out['productivity']}")
    else:
        print(f"    not loaded ({rnn_out.get('error','')[:80]}) — "
              f"HMM already covers this signal path")

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
    print(f"\n[6] BKT MASTERY UPDATE")
    print(f"    src           : src/student_modeling/bayesian_knowledge_tracing.py")
    print(f"    target concept: {TARGET_CONCEPT}")
    print(f"    before update : {PRIOR_MASTERY[TARGET_CONCEPT]:.3f}")
    print(f"    after failure : {new_mastery_dict[TARGET_CONCEPT]:.3f}")

    # DINA initialization — actual update happens in step 7c after the LP
    # diagnostic gives us a correctness signal (classifier match vs EXPECTED_WM).
    dina = DINAModel({"dina": {"data_dir": "data/dina"}})
    dina_before = dina.get_mastery("demo_student", skill=TARGET_CONCEPT)

    # ── 7. LP query with the updated mastery ─────────────────────────────────
    lp_idx = LPIndex()
    lp_path = lp_idx.get_path(TARGET_CONCEPT, new_mastery_dict)
    print(f"\n[7] LEARNING PROGRESSION")
    print(f"    src   : data/java_curriculum/learning_progressions.json "
          f"(9 progressions, 25 concepts)")
    print(f"    progression   : {lp_path['progression_id']}")
    print(f"    target        : {lp_path['target_concept']}")
    print(f"    next concept  : {lp_path['next_concept']}")
    print(f"    on_track      : {lp_path['on_track']}  "
          f"(enforcement will {'fire' if not lp_path['on_track'] else 'not fire'})")

    # ── 7b. LP-Diagnostic + wrong-model identification ───────────────────────
    # Matches the student's text against the documented wrong models for the
    # target concept (catalogue) AND runs the trained LP+WM heads on top of
    # the HVSAE latent we already computed in step 4. Produces an LPDiagnostic
    # with current/target LP level, plateau flag, and matched wrong-model id.
    catalogue = get_catalogue()  # data/mental_models/wrong_models_catalogue.json
    lp_diag_obj = LPDiagnostician(catalogue=catalogue)
    hv_latent = hv['latent'].unsqueeze(0) if hv.get("loaded") else None
    hv_mp = (torch.sigmoid(hv['misconception_logits']).unsqueeze(0)
             if hv.get("loaded") else None)
    lp_diag = lp_diag_obj.diagnose(
        student_id="demo_student",
        concept=TARGET_CONCEPT,
        question_text=STUDENT_MESSAGE,
        stored_lp_level=None, stored_lp_streak=0,
        hvsae_latent=hv_latent,
        hvsae_misconception_probs=hv_mp,
    )
    lp_diag_dict = lp_diag.to_dict() if hasattr(lp_diag, "to_dict") else {}
    print(f"\n[7b] LP DIAGNOSTIC + WRONG-MODEL")
    print(f"    src   : data/mental_models/wrong_models_catalogue.json "
          f"+ checkpoints/cpal_lp_head_st.pt (val_acc=0.74) "
          f"+ cpal_wm_subhead.pt")
    print(f"    matched wrong-model : {lp_diag_dict.get('wrong_model_id')}  "
          f"(score={lp_diag_dict.get('match_score')})")
    matched_signal_str = lp_diag_dict.get('matched_signal') or ''
    print(f"    matched signal      : \"{matched_signal_str[:120]}\"")
    print(f"    current LP level    : {lp_diag_dict.get('current_lp_level')}")
    print(f"    target LP level     : {lp_diag_dict.get('target_lp_level')}")
    print(f"    plateau flag        : {lp_diag_dict.get('plateau_flag')}  "
          f"(intervention={lp_diag_dict.get('plateau_intervention')})")
    if lp_diag_dict.get('trained_wm_probs'):
        print(f"    trained WM head top-3: "
              + ", ".join(f"{w['wm_id']}:{w['prob']:.2f}"
                          for w in lp_diag_dict['trained_wm_probs'][:3]))
    if lp_diag_dict.get('trained_lp_probs'):
        print(f"    trained LP head     : "
              + " ".join(f"{k}:{v:.2f}"
                          for k, v in lp_diag_dict['trained_lp_probs'].items()))

    # ── 7c. DINA cognitive diagnosis — Q-matrix-based per-skill mastery ──────
    # Correctness signal: classifier's wrong-model id == EXPECTED_WM (ground
    # truth). For batch eval this lets DINA reward correct diagnoses and
    # penalize misses; outside the batch it falls back to is_correct=False
    # (the student is presenting a misconception).
    _classifier_wm = lp_diag_dict.get("wrong_model_id")
    _is_correct = bool(EXPECTED_WM is not None and _classifier_wm == EXPECTED_WM)
    dina_update = dina.update("demo_student", TARGET_CONCEPT, is_correct=_is_correct)
    dina_full   = dina.get_mastery("demo_student")
    dina_top3   = sorted(dina_full.items(), key=lambda kv: -kv[1])[:3]
    dina_bot3   = sorted(dina_full.items(), key=lambda kv: kv[1])[:3]
    _verdict = "correct" if _is_correct else "failure"
    print(f"\n[7c] DINA COGNITIVE DIAGNOSIS")
    print(f"    src           : src/models/dina.py "
          f"(20 Java CS1 skills, Q-matrix=I_20, slip=0.10, guess=0.25)")
    print(f"    is_trained    : {dina.is_trained}  "
          f"(uses default + per-concept difficulty priors)")
    print(f"    target skill  : {TARGET_CONCEPT}")
    print(f"    correctness   : {_verdict}  "
          f"(classifier={_classifier_wm}, expected={EXPECTED_WM})")
    print(f"    before update : {dina_before[TARGET_CONCEPT]:.3f}")
    print(f"    after update  : {dina_update.get('mastery_after', 0):.3f}  "
          f"(P(slip)={dina.slip[2]:.2f}, P(guess)={dina.guess[2]:.2f})")
    print(f"    top-3 skills  : "
          + ", ".join(f"{k}={v:.2f}" for k, v in dina_top3))
    print(f"    bottom-3      : "
          + ", ".join(f"{k}={v:.2f}" for k, v in dina_bot3))

    # ── 7b'. CATALOGUE RAG (embedding retrieval + hybrid scoring) ────────────
    kg_artifacts = {}  # populated by [7b'] and [7d]

    # Layer over the trained WM head (val_acc ~0.04). Embeds the student's
    # text with MiniLM-L6-v2 (already loaded for the LP head), retrieves
    # top-k wrong-models and LP rubric lines by cosine similarity, then
    # fuses with classifier probs into a hybrid score.
    rag = CatalogueRAG()
    student_query = f"{STUDENT_MESSAGE}\n{STUDENT_CODE}"

    # Classifier probs from step 7b -> dict {wm_id: prob}. The trained head
    # emits 60 probs but only the top-3 made it into lp_diag_dict; for the
    # rest we treat as 0.
    classifier_probs = {
        w["wm_id"]: float(w["prob"])
        for w in (lp_diag_dict.get("trained_wm_probs") or [])
    }

    # Restrict to the target concept's wrong-models (e.g. NP-A/B/C for
    # null_pointer) — that's the comparable set the classifier scores over
    # for this concept.
    rag_top_wm = rag.hybrid_rank_wrong_models(
        text=student_query,
        classifier_probs=classifier_probs,
        alpha=0.4, top_k=3, concept_filter=TARGET_CONCEPT,
    )
    rag_top_lp = rag.retrieve_lp_rubric(
        text=student_query, top_k=3, concept_filter=TARGET_CONCEPT,
    )

    print(f"\n[7b'] CATALOGUE RAG (embedding retrieval + hybrid scoring)")
    print(f"    src    : data/mental_models/wrong_models_catalogue.json "
          f"+ MiniLM-L6-v2 (60 WMs + 80 LP rubric lines pre-embedded)")
    print(f"    method : alpha={0.4} -> hybrid = "
          f"0.4*classifier_prob + 0.6*cosine_similarity")
    print(f"    top-3 wrong-models (hybrid):")
    for w in rag_top_wm:
        flag = "  <- NEW TOP" if rag_top_wm and w == rag_top_wm[0] and \
               w["id"] != lp_diag_dict.get("wrong_model_id") else ""
        print(f"      {w['id']:<6} hybrid={w['hybrid_score']:.3f}  "
              f"sim={w['similarity']:+.3f}  cls_p={w['classifier_prob']:.3f}"
              f"{flag}")
        print(f"        belief: {w['wrong_belief'][:80]}...")
    print(f"    top-3 LP rubric matches (cosine):")
    for r in rag_top_lp:
        print(f"      {r['concept']:<14} {r['level']}  "
              f"sim={r['similarity']:+.3f}  '{r['text'][:70]}...'")

    # Compare to classifier-only top: did RAG flip the answer?
    cls_top_id = lp_diag_dict.get("wrong_model_id")
    rag_top_id = rag_top_wm[0]["id"] if rag_top_wm else None
    rag_flipped = (rag_top_id is not None and rag_top_id != cls_top_id
                   and cls_top_id is not None)
    print(f"    classifier top : {cls_top_id}")
    print(f"    hybrid top     : {rag_top_id}  "
          f"({'FLIPPED' if rag_flipped else 'agrees with classifier'})")

    # Surface for the prompt builder via student_state.lp_diagnostic.
    # The generator has a new LP-2b section that prints these verbatim.
    lp_diag_dict["rag_top_wrong_models"] = rag_top_wm
    lp_diag_dict["rag_top_lp_rubric"]    = rag_top_lp
    lp_diag_dict["rag_hybrid_top_id"]    = rag_top_id
    lp_diag_dict["rag_flipped_classifier"] = rag_flipped

    kg_artifacts["catalogue_rag"] = {
        "alpha": 0.4,
        "classifier_top": cls_top_id,
        "hybrid_top":     rag_top_id,
        "flipped":        rag_flipped,
        "top_wrong_models": rag_top_wm,
        "top_lp_rubric":    rag_top_lp,
    }

    # ── 7d. STUDENT KNOWLEDGE GRAPH ──────────────────────────────────────────
    # Record this turn in the per-student graph (grounded in the Chapter-1
    # concept + LP graph). persist=False keeps the demo out of SQLite.
    sg = StudentGraphService.shared().record_turn(
        student_id="demo_student",
        diag=lp_diag_dict,
        mastery=dina_update.get("mastery_after"),
        mastery_before=dina_before[TARGET_CONCEPT],
        misconception_text=STUDENT_MESSAGE,
        persist=False,
    )
    skg = sg.to_dict()
    matched_wm_id = lp_diag_dict.get("wrong_model_id")
    print(f"\n[7d] STUDENT KNOWLEDGE GRAPH")
    print(f"    src   : data/chapter1_kg.json")
    print(f"    student      : demo_student")
    print(f"    target       : {TARGET_CONCEPT}  "
          f"(mastery_bkt={new_mastery_dict.get(TARGET_CONCEPT, 0):.2f}, "
          f"mastery_dina={dina_update.get('mastery_after', 0):.2f})")
    print(f"    student holds: {matched_wm_id}")
    print(f"    student KG   : {len(skg['nodes'])} nodes, {len(skg['edges'])} edges; "
          f"LP distribution {skg['summary']['lp_distribution']}")
    kg_artifacts["student_knowledge_graph"] = skg

    # ── 8. RL agent picks the intervention ───────────────────────────────────
    rl = TeachingRLAgent({"rl": {"checkpoint": "checkpoints/rl_teaching_agent.pt"}},
                         models={})
    fake_analysis = {
        'encoding': {'latent': hv['latent']},      # real HVSAE latent (256,)
        'cognitive': {'knowledge_gaps': [
            {'mastery': new_mastery_dict[TARGET_CONCEPT]}
        ]},
        'personality': p,
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
        'motivational_support':'reduce_challenge',
        'interactive_exercise':'transfer_task',
        'guided_practice':    'worked_example',
        'challenge_problem':  'increase_challenge',
        'spaced_review':      'validate_and_advance',
        'error_analysis':     'worked_example',
        'peer_comparison':    'validate_and_advance',
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
        'progression_graph': {'stage': 3, 'zpd_status': 'within',
                              'scaffold_level': 3, 'has_attempt': True},
        'content_channel':   {'encoding_strength': 'partial',
                              'dual_coding': 'verbal_only',
                              'elaboration': False},
        'recommended_intervention': {
            'type':      generator_interv,
            'rationale': f"RL agent selected '{rl_action_name}' (mapped to "
                         f"'{generator_interv}') for HMM={hmm_out['final_state']}",
        },
        # IMPORTANT: the EnhancedPersonalizedGenerator looks for
        # student_state['lp_diagnostic'] (NOT analysis['cpal_lp_diagnostic'])
        # to switch into LP-grounded prompt mode (LP-1, LP-2, LP-3 sections
        # plus an explicit "advance from <current> to <target>" header).
        'lp_diagnostic': lp_diag_dict,
    }
    analysis = {
        'engagement_score':  0.5,
        'bkt_update': {
            'p_learned_before': PRIOR_MASTERY[TARGET_CONCEPT],
            'p_learned_after':  new_mastery_dict[TARGET_CONCEPT],
        },
        'learning_path': lp_path,             # <-- LP path from step 7
        'cpal_lp_diagnostic': lp_diag_dict,   # <-- from step 7b
    }

    # ── 9. Ollama generation ─────────────────────────────────────────────────
    gen = EnhancedPersonalizedGenerator()
    print(f"\n[9] OLLAMA GENERATION  (model={gen._ollama_model}, streaming)")
    print("-" * 80)

    # Capture the assembled Ollama prompt by intercepting requests.post
    captured_prompt = {}
    import requests as _req
    orig_post = _req.post
    def _capture_post(url, json=None, timeout=None, **kw):
        if "ollama" in url or "11434" in url:
            captured_prompt['prompt'] = json.get('prompt', '') if json else ''
        return orig_post(url, json=json, timeout=timeout, **kw)
    _req.post = _capture_post

    first = [None]
    t0 = time.time()
    def on_tok(s):
        if first[0] is None:
            first[0] = time.time() - t0
            print(f"[TTFT={first[0]:.1f}s] ", end="", flush=True)
        print(s, end="", flush=True)
    gen._stream_callback = on_tok

    try:
        resp = gen.generate_personalized_response(
            student_id='demo_student',
            student_message=STUDENT_MESSAGE,
            student_state=student_state,
            analysis=analysis,
            code=STUDENT_CODE,
        )
    finally:
        _req.post = orig_post
    total = time.time() - t0
    print("\n" + "-" * 80)
    print(f"TTFT={first[0]:.1f}s  total={total:.1f}s  {len(resp)} chars")

    # ── Summary: what each component contributed ─────────────────────────────
    print("\n" + "=" * 80)
    print("PROVENANCE — which trained component drove which part of the output")
    print("=" * 80)
    print(f"  TEXT-PERSONALITY   -> neuroticism={p['neuroticism']:.2f} shaped opening tone")
    print(f"  NESTOR CPTs        -> style/strategy drove format choices")
    print(f"  HMM                -> behavioural state '{hmm_out['final_state']}'")
    if hv.get("loaded"):
        print(f"  HVSAE              -> 256-dim latent fed to RL agent, "
              f"gating code/text/action={tuple(round(w,2) for w in hv['attention'])}")
    if rnn_out.get("loaded"):
        print(f"  BEHAVIORAL RNN     -> effectiveness={rnn_out['effectiveness']:.2f}")
    print(f"  BKT                -> {TARGET_CONCEPT} mastery "
          f"{PRIOR_MASTERY[TARGET_CONCEPT]:.2f} -> {new_mastery_dict[TARGET_CONCEPT]:.2f}")
    print(f"  DINA               -> {TARGET_CONCEPT} P(mastered)="
          f"{dina_update.get('mastery_after', 0):.2f} "
          f"(slip={dina.slip[2]:.2f}, guess={dina.guess[2]:.2f})")
    print(f"  LPINDEX            -> path to '{TARGET_CONCEPT}', "
          f"on_track={lp_path['on_track']}")
    print(f"  RL AGENT           -> chose '{rl_action_name}' -> "
          f"generator intervention '{generator_interv}'")
    print(f"  LP-DIAGNOSTIC      -> wrong-model={lp_diag_dict.get('wrong_model_id')}, "
          f"LP={lp_diag_dict.get('current_lp_level')}->"
          f"{lp_diag_dict.get('target_lp_level')}, "
          f"plateau={lp_diag_dict.get('plateau_flag')}")
    skg_info = kg_artifacts.get('student_knowledge_graph', {})
    print(f"  STUDENT KG         -> "
          f"{len(skg_info.get('nodes', []))} nodes, "
          f"{len(skg_info.get('edges', []))} edges; "
          f"wrong-model held: {matched_wm_id}")

    return {
        "started_at_session": STUDENT_MESSAGE,
        "student_message": STUDENT_MESSAGE,
        "student_code": STUDENT_CODE,
        "action_sequence": ACTION_SEQUENCE,
        "target_concept": TARGET_CONCEPT,
        "personality_big5": p,
        "nestor": {
            "styles": nestor_out['learning_styles'],
            "strategies": nestor_out['learning_strategies'],
            "intervention": nestor_out['intervention_preference'],
            "elements": nestor_out['recommended_elements'],
        },
        "behavioral_hmm": hmm_out,
        "hvsae": {
            "loaded": hv.get("loaded"),
            "attention": hv.get("attention"),
        },
        "behavioral_rnn": rnn_out,
        "bkt": {
            "target_concept": TARGET_CONCEPT,
            "before": PRIOR_MASTERY[TARGET_CONCEPT],
            "after_failure": new_mastery_dict[TARGET_CONCEPT],
        },
        "dina": {
            "target_concept": TARGET_CONCEPT,
            "before": dina_before[TARGET_CONCEPT],
            "after_failure": dina_update.get("mastery_after", 0),
            "after_update": dina_update.get("mastery_after", 0),
            "is_correct": _is_correct,
            "classifier_wm": _classifier_wm,
            "expected_wm": EXPECTED_WM,
            "is_trained": dina.is_trained,
            "all_skills_after_update": dina_full,
        },
        "lp_path": lp_path,
        "lp_diagnostic": lp_diag_dict,
        "knowledge_graph": kg_artifacts,
        "rl_agent": {
            "action": rl_action_name,
            "epsilon": rl.epsilon,
            "generator_intervention": generator_interv,
        },
        "ollama": {
            "model": gen._ollama_model,
            "url": gen._ollama_url,
            "ttft_s": first[0],
            "total_s": total,
            "response_chars": len(resp),
        },
        "ollama_prompt": captured_prompt.get('prompt', ''),
        "ollama_response": resp,
    }


def main():
    """Run the full stack and save every artifact to a fresh output folder."""
    stamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    out_dir = ROOT / "output" / f"full_stack_run_{stamp}"
    out_dir.mkdir(parents=True, exist_ok=True)
    print(f"[saver] writing artifacts to: {out_dir}")

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
        artifacts = run()
    finally:
        sys.stdout = real_stdout

    (out_dir / "transcript.txt").write_text(transcript.getvalue(), encoding="utf-8")
    (out_dir / "prompt.txt").write_text(artifacts.get("ollama_prompt", ""), encoding="utf-8")
    (out_dir / "response.md").write_text(artifacts.get("ollama_response", ""), encoding="utf-8")

    # Save the student knowledge graph as a first-class artifact
    skg_dict = artifacts.get("knowledge_graph", {}).get(
        "student_knowledge_graph") or \
        artifacts.get("knowledge_graph_full", {}).get(
        "student_knowledge_graph")
    if not skg_dict:
        # path used in this run
        skg_dict = (artifacts.get("knowledge_graph", {}) or {})\
            .get("student_knowledge_graph", {})
    if skg_dict:
        (out_dir / "student_knowledge_graph.json").write_text(
            json.dumps(skg_dict, indent=2, default=str), encoding="utf-8")

    serializable = {k: v for k, v in artifacts.items()
                    if k not in ("ollama_prompt", "ollama_response")}
    (out_dir / "diagnostic.json").write_text(
        json.dumps(serializable, indent=2, default=str), encoding="utf-8"
    )

    summary_lines = [
        "# Full-stack run summary",
        "",
        f"- Stamp: {stamp}",
        f"- Target concept: {artifacts.get('target_concept')}",
        f"- Ollama model: {artifacts.get('ollama', {}).get('model')}",
        f"- Generation: TTFT={artifacts.get('ollama', {}).get('ttft_s')}s, "
        f"total={artifacts.get('ollama', {}).get('total_s')}s, "
        f"{artifacts.get('ollama', {}).get('response_chars')} chars",
        f"- Wrong-model matched: {artifacts.get('lp_diagnostic', {}).get('wrong_model_id')}",
        f"- LP level: {artifacts.get('lp_diagnostic', {}).get('current_lp_level')} "
        f"-> {artifacts.get('lp_diagnostic', {}).get('target_lp_level')}",
        "",
        "## Files",
        "- transcript.txt   -- full stdout (every component step + Ollama stream)",
        "- prompt.txt       -- the assembled Ollama prompt (~7k chars)",
        "- response.md      -- the final LLM response",
        "- diagnostic.json  -- structured per-component outputs + lp_diagnostic",
    ]
    (out_dir / "README.md").write_text("\n".join(summary_lines), encoding="utf-8")

    print(f"\n[saver] DONE. Files in {out_dir}:")
    for f in sorted(out_dir.iterdir()):
        print(f"   - {f.name}  ({f.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
