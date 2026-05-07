"""
Unseen-paraphrase CPAL demo — genuinely diverse student vocabulary,
concept = array_index, intended wrong model = AI-B.

Compares overlap-only baseline vs. HVSAE-powered semantic matcher,
then generates the grounded response through the real pls_fixed
generator + Ollama. Also shows what HVSAE's 20-class misconception
head *independently* predicts about the concept.
"""
import os, sys, torch
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from src.models.hvsae import HVSAE
from src.knowledge_graph.mental_models import get_catalogue
from src.orchestrator.lp_diagnostic import LPDiagnostician, filter_interventions_by_lp
from src.orchestrator.enhanced_personalized_generator import EnhancedPersonalizedGenerator


STUDENT_INPUT = (
    "When I query the size property of my numeric collection I get back a "
    "count of seven, so naturally I tried reading the seventh slot to grab "
    "the tail element, but the runtime throws a boundary violation. Why is "
    "the final addressable position not the same as the reported cardinality? "
    "That seems counterintuitive — the count tells me how many entries exist, "
    "so the highest reachable one should be labeled the same."
)
CONCEPT_ID = "array_index"
STUDENT_ID = "demo_unseen"


def hr(t="", g="="):
    print("\n" + g * 78)
    if t: print(" " + t); print(g * 78)


def show(label, diag):
    print(f"\n  {label}")
    print(f"    source              : {diag.get('source')}")
    print(f"    wrong_model_id      : {diag.get('wrong_model_id')}")
    print(f"    match_score         : {diag.get('match_score', 0):.3f}")
    print(f"    matched_signal      : \"{diag.get('matched_signal','')}\"")
    print(f"    current_lp_level    : {diag.get('current_lp_level')}  "
          f"→ target {diag.get('target_lp_level')}")
    if diag.get("semantic_wm_top3"):
        print(f"    semantic WM top-3   :")
        for t in diag["semantic_wm_top3"]:
            print(f"      {t['wm_id']:6s} cos={t['score']:+.3f}  ← \"{t['signal'][:58]}\"")
    if diag.get("semantic_lp_scores"):
        ss = diag["semantic_lp_scores"]
        print(f"    semantic LP cosines : " +
              "  ".join(f"{k}={v:+.2f}" for k, v in ss.items()))
    if diag.get("hvsae_concept_top3"):
        print(f"    HVSAE concept top-3 (20-class head, independent):")
        for t in diag["hvsae_concept_top3"]:
            print(f"      {t['concept_id']:22s}  p={t['prob']:.3f}")


def main():
    hr("STUDENT INPUT  (array_index / expected: AI-B)")
    print(STUDENT_INPUT)
    print(f"\n  concept = {CONCEPT_ID}")

    hr("LOADING TRAINED HVSAE")
    ckpt = torch.load(os.path.join(ROOT, "checkpoints", "best.pt"),
                      map_location="cpu", weights_only=False)
    hvsae = HVSAE(ckpt["config"])
    hvsae.load_state_dict(ckpt["hvsae_state"])
    hvsae.eval()
    print(f"  epoch={ckpt['epoch']}  best_val_loss={ckpt['best_val_loss']:.2e}")

    cat = get_catalogue(
        os.path.join(ROOT, "data", "mental_models", "wrong_models_catalogue.json")
    )

    # --- Baseline (overlap-only) --------------------------------------
    hr("BASELINE — overlap matcher only")
    baseline = LPDiagnostician(catalogue=cat, hvsae_model=None).diagnose(
        student_id=STUDENT_ID, concept=CONCEPT_ID,
        question_text=STUDENT_INPUT,
        stored_lp_level="L1", stored_lp_streak=0,
    ).to_dict()
    show("diagnosis:", baseline)

    # --- HVSAE-powered dynamic diagnosis ------------------------------
    hr("HVSAE-POWERED DIAGNOSIS — dynamic (semantic matcher)")
    dx = LPDiagnostician(catalogue=cat, hvsae_model=hvsae)
    from transformers import AutoTokenizer
    try:
        tk = AutoTokenizer.from_pretrained("bert-base-uncased")
        text_ids = tk(STUDENT_INPUT, return_tensors="pt", padding=True,
                      truncation=True, max_length=64)["input_ids"].long() % 6000
    except Exception:
        text_ids = torch.randint(1, 5999, (1, 16))
    batch = {
        "code_tokens":     torch.zeros(1, 10, dtype=torch.long),
        "text_tokens":     text_ids,
        "action_sequence": torch.ones(1, 8, dtype=torch.long),
    }
    with torch.no_grad():
        hv_out = hvsae.forward(batch, compute_graph=False)
    misconception_probs = torch.softmax(hv_out["misconception_logits"], dim=-1)
    hv_latent = hv_out["latent"]

    hvsae_diag = dx.diagnose(
        student_id=STUDENT_ID, concept=CONCEPT_ID,
        question_text=STUDENT_INPUT,
        stored_lp_level="L1", stored_lp_streak=0,
        hvsae_latent=hv_latent,
        hvsae_misconception_probs=misconception_probs,
    ).to_dict()
    show("diagnosis:", hvsae_diag)

    # --- Verdict
    hr("OUTCOME")
    b_wm, h_wm = baseline.get("wrong_model_id"), hvsae_diag.get("wrong_model_id")
    print(f"  baseline (overlap) : {b_wm}")
    print(f"  dynamic (HVSAE)    : {h_wm}")
    print(f"  expected (author)  : AI-B")

    # --- Grounded response via real generator ------------------------
    candidates = [("transfer_task", 0.92), ("worked_example", 0.80),
                  ("socratic_prompt", 0.70), ("trace_scaffold", 0.65)]
    filt = filter_interventions_by_lp(candidates, hvsae_diag["current_lp_level"])
    chosen = filt[0][0] if filt else "worked_example"

    hr("GENERATED RESPONSE  (real generator + Ollama)")
    student_state = {
        "student_id": STUDENT_ID,
        "lp_diagnostic": hvsae_diag,
        "recommended_intervention": {"type": chosen},
        "personality_profile": {"communication_style": "direct",
                                 "learning_preference": "visual"},
        "bkt_mastery": {CONCEPT_ID: 0.30},
        "emotional_state": "confused",
        "interaction_count": 1,
    }
    analysis = {
        "emotion": {"primary": "confused", "confidence": 0.7},
        "knowledge_gaps": [CONCEPT_ID],
        "pedagogical_kg": {},
    }
    gen = EnhancedPersonalizedGenerator()
    print(f"  [model: {gen._ollama_model}]   [intervention: {chosen}]")
    print(f"  [LP: {hvsae_diag['current_lp_level']} → "
          f"{hvsae_diag['target_lp_level']}]   "
          f"[wrong-model: {hvsae_diag['wrong_model_id']} via "
          f"{hvsae_diag['source']} score={hvsae_diag['match_score']:.2f}]\n")
    def on_chunk(p): sys.stdout.write(p); sys.stdout.flush()
    gen._stream_callback = on_chunk
    gen.generate_personalized_response(
        student_id=STUDENT_ID, student_message=STUDENT_INPUT,
        student_state=student_state, analysis=analysis,
    )
    print()


if __name__ == "__main__":
    main()
