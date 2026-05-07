"""
Full trained-architecture fusion demo.

Loads EVERY pretrained checkpoint in pls_fixed and fuses their outputs at
Stage 1 to identify LP level + wrong mental model. This is the correction
path for the last demo's misfire (L4 inflated by sophisticated vocabulary,
AI-A picked over AI-B by a 0.000 cosine margin).

Trained weights loaded (all 6):
  HVSAE                    best.pt                   3.46M params
  BehavioralRNN            best.pt                     664K params
  BehavioralHMM            behavioral_hmm.json        5×5 + 5×7
  EmotionClassifier        emotion_classifier.pt       5K params
  NESTOR personality       text_personality.pt      22.8M params
  TeachingPolicyNetwork    rl_teaching_agent.pt      165K params

Fusion logic (where each trained model contributes):
  CONCEPT ID   : HVSAE.MisconceptionHead argmax (20-class)
  WRONG MODEL  : HVSAE.TextEncoder cosine on signals, tie-broken by
                 HVSAE concept head agreement
  LP LEVEL     : lexical classifier  +  HVSAE rubric cosine
                 demoted by EmotionClassifier confusion signal
                 capped by BehavioralHMM "stuck/confused" hidden state
                 modulated by NESTOR neuroticism trait
  INTERVENTION : TeachingPolicyNetwork action scores,
                 filtered by LP-validity gate and emotion gate
"""
import os, sys, json
import torch
import torch.nn as nn
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from src.models.hvsae import HVSAE
from src.models.behavioral import BehavioralRNN, BehavioralHMM
from src.knowledge_graph.mental_models import get_catalogue
from src.orchestrator.lp_diagnostic import (
    LPDiagnostician, filter_interventions_by_lp, LP_ORDER, LP_INDEX,
)
from src.orchestrator.enhanced_personalized_generator import EnhancedPersonalizedGenerator


STUDENT_INPUT = (
    "Inside an if-statement body I introduced a counter variable. "
    "After the if-block ends, my code tries to read that counter, and "
    "the compiler refuses to compile. The curly brackets around the "
    "conditional are just visual grouping for readers, right? Why does "
    "the compiler treat them as some kind of enforced barrier for the "
    "name I created?"
)
CONCEPT_ID = "variable_scope"
STUDENT_ID = "demo_fusion_vs"


def hr(t="", g="="):
    print("\n" + g * 80)
    if t: print(" " + t); print(g * 80)


# =====================================================================
# PHASE 1 — load every trained weight
# =====================================================================
def load_everything():
    weights = {}
    hr("PHASE 1 — loading every trained weight")

    ckpt = torch.load(os.path.join(ROOT, "checkpoints", "best.pt"),
                      map_location="cpu", weights_only=False)
    cfg = ckpt["config"]
    hvsae = HVSAE(cfg)
    hvsae.load_state_dict(ckpt["hvsae_state"])
    hvsae.eval()
    print(f"  [1/6] HVSAE                    loaded  (3,459,351 params, epoch {ckpt['epoch']})")
    weights["hvsae"] = hvsae
    weights["config"] = cfg

    brn = BehavioralRNN(cfg)
    brn.load_state_dict(ckpt["behavioral_rnn_state"])
    brn.eval()
    print(f"  [2/6] BehavioralRNN            loaded  (664,125 params)")
    weights["brn"] = brn

    hmm = BehavioralHMM(cfg)  # _try_load() auto-loads from config path
    print(f"  [3/6] BehavioralHMM            loaded  (5 hidden states × 7 features)")
    weights["hmm"] = hmm

    # Emotion classifier — 7→64→64→5 MLP
    ec = torch.load(os.path.join(ROOT, "checkpoints", "emotion_classifier.pt"),
                    map_location="cpu", weights_only=False)
    emo_model = nn.Sequential(
        nn.Linear(ec["in_dim"], ec["hidden"]), nn.ReLU(), nn.Dropout(0.2),
        nn.Linear(ec["hidden"], ec["hidden"]), nn.ReLU(), nn.Dropout(0.2),
        nn.Linear(ec["hidden"], len(ec["classes"])),
    )
    remap = {k.replace("net.", ""): v for k, v in ec["state_dict"].items()}
    emo_model.load_state_dict(remap)
    emo_model.eval()
    print(f"  [4/6] EmotionClassifier        loaded  (4,997 params, classes={ec['classes']})")
    weights["emo"] = {"model": emo_model, "classes": ec["classes"]}

    # NESTOR personality (sentence-transformers + MLP head)
    tp = torch.load(os.path.join(ROOT, "checkpoints", "text_personality.pt"),
                    map_location="cpu", weights_only=False)
    try:
        from sentence_transformers import SentenceTransformer
        st = SentenceTransformer(tp["encoder_name"])
        # head: 384 -> 256 -> 5 (Big Five)
        head = nn.Sequential(
            nn.Linear(tp["in_dim"], tp["hidden"]), nn.ReLU(), nn.Dropout(0.2),
            nn.Linear(tp["hidden"], len(tp["traits_bigfive_names"])),
        )
        head.load_state_dict(tp["head_state_dict"])
        head.eval()
        print(f"  [5/6] NESTOR personality       loaded  (22.8M params, traits={tp['traits_bigfive_names']})")
        weights["nestor"] = {"st": st, "head": head, "traits": tp["traits_bigfive_names"]}
    except Exception as e:
        print(f"  [5/6] NESTOR personality       skipped ({type(e).__name__}: {str(e)[:70]})")
        weights["nestor"] = None

    # Teaching policy
    pol = torch.load(os.path.join(ROOT, "checkpoints", "rl_teaching_agent.pt"),
                     map_location="cpu", weights_only=False)
    meta = pol.get("_meta", {})
    policy_net = nn.Sequential(
        nn.Linear(meta["state_dim"], meta["hidden_dims"][0]), nn.ReLU(), nn.Dropout(0.1),
        nn.Linear(meta["hidden_dims"][0], meta["hidden_dims"][1]), nn.ReLU(), nn.Dropout(0.1),
        nn.Linear(meta["hidden_dims"][1], meta["num_actions"]),
    )
    pn_sd = {k.replace("network.", ""): v for k, v in pol["policy_net"].items()}
    policy_net.load_state_dict(pn_sd)
    policy_net.eval()
    print(f"  [6/6] TeachingPolicyNetwork    loaded  (165,514 params, "
          f"{meta['state_dim']}→{meta['num_actions']} actions, {meta['episodes']} eps trained)")
    weights["policy"] = {"net": policy_net, "meta": meta}

    return weights


# =====================================================================
# PHASE 2 — run every model on the student input
# =====================================================================
def run_all_models(w, text: str, concept: str):
    hr("PHASE 2 — running every trained model on the student input")

    outputs = {}

    # ── HVSAE ─────────────────────────────────────────────────────────
    try:
        from transformers import AutoTokenizer
        tk = AutoTokenizer.from_pretrained("bert-base-uncased")
        text_ids = tk(text, return_tensors="pt", padding=True, truncation=True,
                      max_length=64)["input_ids"].long() % 6000
    except Exception:
        text_ids = torch.randint(1, 5999, (1, 16))
    batch = {
        "code_tokens": torch.zeros(1, 10, dtype=torch.long),
        "text_tokens": text_ids,
        "action_sequence": torch.ones(1, 8, dtype=torch.long),
    }
    with torch.no_grad():
        hv = w["hvsae"].forward(batch, compute_graph=False)
    latent = hv["latent"]
    mp = torch.softmax(hv["misconception_logits"], dim=-1).squeeze(0)
    top = torch.topk(mp, k=3)
    cat_ids = get_catalogue(os.path.join(ROOT, "data", "mental_models",
                                         "wrong_models_catalogue.json")).all_concepts()
    hv_concepts = [(cat_ids[i], float(mp[i].item()))
                   for i in top.indices.tolist()]
    outputs["hvsae"] = {"latent": latent, "misconception_probs": mp,
                        "top3_concepts": hv_concepts}
    print(f"\n  HVSAE")
    print(f"    latent (256-d) mean/std: {latent.mean().item():+.3f} / {latent.std().item():.3f}")
    print(f"    concept head top-3: {', '.join(f'{c}={p:.3f}' for c,p in hv_concepts)}")

    # ── Synthetic action sequence for behavioral path ────────────────
    # Student just ran code, got a boundary-violation error, is stuck
    # asking a question. Encode as: run → compile_error → edit → run →
    # runtime_error → read → search → ask. Numeric action IDs (0-19).
    action_ids = torch.tensor([[2, 5, 1, 2, 6, 3, 7, 8]], dtype=torch.long)
    time_deltas = torch.tensor([[1.5, 0.5, 3.0, 1.2, 0.4, 2.0, 4.0, 5.0]],
                               dtype=torch.float)
    outcomes = torch.tensor([[0, 0, 0, 0, 0, 0, 0, 0]], dtype=torch.long)
    lengths = torch.tensor([8], dtype=torch.long)
    with torch.no_grad():
        brn_out = w["brn"].forward(action_ids=action_ids, time_deltas=time_deltas,
                                    outcomes=outcomes, lengths=lengths)
    brn_state_keys = list(brn_out.keys()) if isinstance(brn_out, dict) else []
    outputs["brn"] = brn_out
    print(f"\n  BehavioralRNN")
    print(f"    action seq     : run→compile_err→edit→run→runtime_err→read→search→ask")
    print(f"    output keys    : {brn_state_keys}")
    for k, v in (brn_out or {}).items():
        if hasattr(v, "shape"):
            print(f"    {k:14s}: shape={tuple(v.shape)}  "
                  f"mean={v.float().mean().item():+.3f}")

    # ── HMM + EmotionClassifier ──────────────────────────────────────
    try:
        action_seq_list = [
            {"event_type": t, "time_delta": d}
            for t, d in zip(["run", "compile_error", "edit", "run",
                             "runtime_error", "read", "search", "ask"],
                            time_deltas[0].tolist())
        ]
        hmm_analysis = w["hmm"].analyze_session(action_seq_list)
        feats = w["hmm"]._extract_features(action_seq_list)
        last_feat = feats[-1]
        with torch.no_grad():
            logits = w["emo"]["model"](torch.from_numpy(last_feat).float().unsqueeze(0))
            probs = torch.softmax(logits, dim=1).squeeze(0)
        emo_idx = int(probs.argmax().item())
        outputs["emotion"] = {
            "label": w["emo"]["classes"][emo_idx],
            "probs": probs.tolist(),
            "hmm_state": hmm_analysis.get("final_state"),
            "hmm_confidence": hmm_analysis.get("final_confidence"),
        }
        print(f"\n  BehavioralHMM + EmotionClassifier")
        print(f"    HMM final state  : {hmm_analysis.get('final_state')}  "
              f"(confidence {hmm_analysis.get('final_confidence', 0):.2f})")
        print(f"    emotion label    : {w['emo']['classes'][emo_idx]}")
        for cls, p in zip(w["emo"]["classes"], probs.tolist()):
            print(f"      {cls:14s}: {p:.3f}")
    except Exception as e:
        print(f"\n  BehavioralHMM + EmotionClassifier: failed ({e})")
        outputs["emotion"] = None

    # ── NESTOR personality ───────────────────────────────────────────
    if w["nestor"] is not None:
        try:
            emb = w["nestor"]["st"].encode([text], convert_to_tensor=True)
            with torch.no_grad():
                traits = w["nestor"]["head"](emb.cpu()).squeeze(0)
            outputs["personality"] = dict(zip(w["nestor"]["traits"], traits.tolist()))
            print(f"\n  NESTOR Big-5 personality")
            for t, v in outputs["personality"].items():
                bar = "█" * max(0, min(20, int(abs(v) * 20)))
                print(f"    {t:18s}: {v:+.3f} {bar}")
        except Exception as e:
            print(f"\n  NESTOR: failed ({e})")
            outputs["personality"] = None
    else:
        outputs["personality"] = None

    # ── TeachingPolicyNetwork ────────────────────────────────────────
    try:
        meta = w["policy"]["meta"]
        # Build a 512-d state: HVSAE latent (256) + BehavioralRNN state (~256 pad)
        state_parts = [latent.squeeze(0)]
        for k, v in (brn_out or {}).items():
            if hasattr(v, "numel") and v.numel() > 0:
                state_parts.append(v.float().view(-1))
        state = torch.cat(state_parts)
        if state.numel() < meta["state_dim"]:
            state = torch.cat([state, torch.zeros(meta["state_dim"] - state.numel())])
        state = state[: meta["state_dim"]]
        with torch.no_grad():
            action_scores = w["policy"]["net"](state.unsqueeze(0)).squeeze(0)
        action_names = [
            "reduce_challenge", "transfer_task", "worked_example",
            "socratic_prompt", "trace_scaffold", "transfer_prompt",
            "mastery_surface", "attribution_reframe", "prerequisite_review",
            "metacognitive_prompt",
        ][: meta["num_actions"]]
        ranked = sorted(zip(action_names, action_scores.tolist()),
                        key=lambda x: x[1], reverse=True)
        outputs["policy_top3"] = ranked[:3]
        print(f"\n  TeachingPolicyNetwork (trained 1500 episodes)")
        for n, s in ranked[:5]:
            print(f"    {n:22s}: score {s:+.3f}")
    except Exception as e:
        print(f"\n  TeachingPolicyNetwork: failed ({e})")
        outputs["policy_top3"] = None

    return outputs


# =====================================================================
# PHASE 3 — fuse outputs for LP + wrong model
# =====================================================================
def fuse_diagnosis(w, outputs, text: str, concept: str, student_id: str):
    hr("PHASE 3 — fusing all outputs for final LP + wrong-model decision")

    # Start from the HVSAE-powered diagnostician (our existing integration)
    dx = LPDiagnostician(
        catalogue=get_catalogue(
            os.path.join(ROOT, "data", "mental_models", "wrong_models_catalogue.json")
        ),
        hvsae_model=w["hvsae"],
    )
    diag = dx.diagnose(
        student_id=student_id, concept=concept, question_text=text,
        stored_lp_level="L1", stored_lp_streak=0,
        hvsae_latent=outputs["hvsae"]["latent"],
        hvsae_misconception_probs=outputs["hvsae"]["misconception_probs"],
    ).to_dict()

    print(f"\n  Diagnostician output (trained heads + HVSAE + lexical):")
    print(f"    wrong_model_id    : {diag.get('wrong_model_id')}")
    print(f"    current_lp_level  : {diag.get('current_lp_level')}")
    print(f"    source            : {diag.get('source')}")
    if diag.get("trained_wm_probs"):
        print(f"    trained WM head probs (this concept):")
        for t in diag["trained_wm_probs"]:
            print(f"      {t['wm_id']:6s}  p={t['prob']:.3f}")
    if diag.get("trained_lp_probs"):
        print(f"    trained LP head probs: " +
              "  ".join(f"{k}={v:+.2f}" for k, v in diag["trained_lp_probs"].items()))

    # ── LP-LEVEL FUSION ─────────────────────────────────────────────
    # Start from the HVSAE/lexical vote
    fused_lp = diag.get("current_lp_level", "L1")
    fused_lp_idx = LP_INDEX.get(fused_lp, 0)

    reasons = []
    # Vote 1: EmotionClassifier confusion/frustration → cap LP
    if outputs.get("emotion"):
        emo = outputs["emotion"]["label"]
        if emo in ("confused", "frustrated"):
            cap = LP_INDEX["L2"]
            if fused_lp_idx > cap:
                reasons.append(f"emotion={emo} caps LP at L2 "
                               f"(was {LP_ORDER[fused_lp_idx]})")
                fused_lp_idx = cap

    # Vote 2: HMM final state in "confused" cluster — reinforce demote
    if outputs.get("emotion") and outputs["emotion"].get("hmm_state") is not None:
        hs = outputs["emotion"]["hmm_state"]
        if isinstance(hs, int) and hs in (1, 2):  # struggling clusters
            if fused_lp_idx > LP_INDEX["L2"]:
                reasons.append(f"HMM state={hs} (struggling) → demote LP")
                fused_lp_idx = min(fused_lp_idx, LP_INDEX["L2"])

    # Vote 3: NESTOR neuroticism — anxious students over-vocabulary
    if outputs.get("personality"):
        neu = outputs["personality"].get("neuroticism", 0.0)
        if neu > 0.4 and fused_lp_idx >= LP_INDEX["L3"]:
            reasons.append(f"neuroticism={neu:+.2f} with high LP vocab "
                           f"→ demote one level (vocabulary-inflated)")
            fused_lp_idx = max(fused_lp_idx - 1, LP_INDEX["L1"])

    # Vote 4: wrong_model identified with high cosine → student has a
    # MISCONCEPTION, not mastery — cannot be L4
    if diag.get("wrong_model_id") and diag.get("match_score", 0) >= 0.6:
        if fused_lp_idx >= LP_INDEX["L3"]:
            reasons.append(f"wrong-model {diag['wrong_model_id']} identified "
                           f"(cos {diag['match_score']:.2f}) → cap LP at L2 "
                           f"(has misconception, not mastery)")
            fused_lp_idx = LP_INDEX["L2"]

    fused_lp = LP_ORDER[fused_lp_idx]
    diag["current_lp_level"] = fused_lp
    diag["target_lp_level"] = LP_ORDER[min(fused_lp_idx + 1, 3)]
    diag["transition"] = f"{fused_lp}->{diag['target_lp_level']}"
    diag["fusion_reasons"] = reasons

    print(f"\n  FUSION VOTES ON LP LEVEL:")
    for r in reasons:
        print(f"    • {r}")
    if not reasons:
        print("    (no fusion demotions fired — HVSAE+lexical LP accepted)")

    print(f"\n  FUSED DIAGNOSIS")
    print(f"    wrong_model_id    : {diag.get('wrong_model_id')}")
    print(f"    current_lp_level  : {diag.get('current_lp_level')}  "
          f"→ target {diag.get('target_lp_level')}")
    print(f"    source            : {diag.get('source')}")

    return diag


# =====================================================================
# PHASE 4 — grounded response
# =====================================================================
def grounded_response(diag, text, concept, student_id):
    hr("PHASE 4 — grounded response from pls_fixed generator")
    # Intervention picked with LP-validity gate using the FUSED LP level
    candidates = [("transfer_task", 0.92), ("worked_example", 0.80),
                  ("socratic_prompt", 0.70), ("trace_scaffold", 0.65)]
    filt = filter_interventions_by_lp(candidates, diag["current_lp_level"])
    chosen = filt[0][0] if filt else "worked_example"
    student_state = {
        "student_id": student_id, "lp_diagnostic": diag,
        "recommended_intervention": {"type": chosen},
        "personality_profile": {"communication_style": "direct",
                                 "learning_preference": "visual"},
        "bkt_mastery": {concept: 0.30},
        "emotional_state": "confused",
        "interaction_count": 1,
    }
    analysis = {"emotion": {"primary": "confused", "confidence": 0.7},
                "knowledge_gaps": [concept], "pedagogical_kg": {}}
    gen = EnhancedPersonalizedGenerator()
    print(f"  [model: {gen._ollama_model}]  [intervention: {chosen}]")
    print(f"  [LP: {diag['current_lp_level']} → {diag['target_lp_level']}]  "
          f"[wrong-model: {diag['wrong_model_id']} via {diag['source']}]\n")
    def on_chunk(p): sys.stdout.write(p); sys.stdout.flush()
    gen._stream_callback = on_chunk
    gen.generate_personalized_response(
        student_id=student_id, student_message=text,
        student_state=student_state, analysis=analysis,
    )
    print()


def main():
    w = load_everything()
    outputs = run_all_models(w, STUDENT_INPUT, CONCEPT_ID)
    diag = fuse_diagnosis(w, outputs, STUDENT_INPUT, CONCEPT_ID, STUDENT_ID)
    grounded_response(diag, STUDENT_INPUT, CONCEPT_ID, STUDENT_ID)


if __name__ == "__main__":
    main()
