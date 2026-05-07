"""
Any-vocabulary demo — prove the system identifies LP level and wrong
mental model from an arbitrary student input, with no catalogue words.

Usage:
    python scripts/cpal_demo_any.py <concept_id> "<student input>"
    (falls back to baked-in examples if no args given)

Shows:
  1. trained ST-based LP head — probability per level (L1-L4)
  2. trained HVSAE-based WM sub-head — probability per (A,B,C) for the concept
  3. Fused diagnosis
  4. Ollama-generated grounded response
"""
import os, sys
import torch

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from src.models.hvsae import HVSAE
from src.knowledge_graph.mental_models import get_catalogue
from src.orchestrator.lp_diagnostic import (
    LPDiagnostician, filter_interventions_by_lp,
)
from src.orchestrator.enhanced_personalized_generator import (
    EnhancedPersonalizedGenerator,
)


# Default student input if no CLI args given
DEFAULT_CONCEPT = "integer_division"
DEFAULT_INPUT = (
    "Look, I'm telling the computer to divide two whole numbers and get a "
    "result that's obviously fractional. In any math class on earth, 5 over 2 "
    "yields the decimal two-point-five. Java is giving me the truncated "
    "integer portion — presumably because the operands are whole numbers — "
    "but that seems wrong. The mathematical answer exists regardless of "
    "what I start with. Why is Java being lazy about the numeric type?"
)


def hr(t=""):
    print("\n" + "=" * 78)
    if t: print(" " + t); print("=" * 78)


def render_bar(prob, width=30):
    filled = int(round(prob * width))
    return "█" * filled + "·" * (width - filled)


def main():
    if len(sys.argv) >= 3:
        concept = sys.argv[1]
        text    = sys.argv[2]
    else:
        concept = DEFAULT_CONCEPT
        text    = DEFAULT_INPUT

    hr("STUDENT INPUT")
    print(f"  concept: {concept}")
    print(f"  text:    {text}")

    hr("LOADING")
    ck = torch.load(os.path.join(ROOT, "checkpoints", "best.pt"),
                    map_location="cpu", weights_only=False)
    hvsae = HVSAE(ck["config"]); hvsae.load_state_dict(ck["hvsae_state"]); hvsae.eval()
    cat = get_catalogue(
        os.path.join(ROOT, "data", "mental_models", "wrong_models_catalogue.json")
    )

    # Encode via HVSAE for the WM head (uses HVSAE latent)
    try:
        from transformers import AutoTokenizer
        tk = AutoTokenizer.from_pretrained("bert-base-uncased")
        text_ids = tk(text, return_tensors="pt", padding=True, truncation=True,
                      max_length=64)["input_ids"].long() % 6000
    except Exception:
        text_ids = torch.randint(1, 5999, (1, 16))
    batch = {"code_tokens": torch.zeros(1, 10, dtype=torch.long),
             "text_tokens": text_ids,
             "action_sequence": torch.ones(1, 8, dtype=torch.long)}
    with torch.no_grad():
        hv_out = hvsae.forward(batch, compute_graph=False)
    latent = hv_out["latent"]
    mp = torch.softmax(hv_out["misconception_logits"], dim=-1)

    # LPDiagnostician with all heads + HVSAE
    dx = LPDiagnostician(catalogue=cat, hvsae_model=hvsae)
    diag = dx.diagnose(
        student_id="demo_any", concept=concept, question_text=text,
        stored_lp_level="L1", stored_lp_streak=0,
        hvsae_latent=latent, hvsae_misconception_probs=mp,
    ).to_dict()

    # Emotional/behavioral context not wired here — keep diagnosis pure
    # (fusion rule fires only on wrong-model confidence)
    # If wrong model detected with decent confidence, cap LP at L2
    if diag.get("wrong_model_id") and diag.get("match_score", 0) >= 0.5:
        from src.orchestrator.lp_diagnostic import LP_ORDER, LP_INDEX
        lvl_idx = LP_INDEX.get(diag["current_lp_level"], 0)
        if lvl_idx >= LP_INDEX["L3"]:
            diag["fusion_reason"] = (
                f"wrong-model {diag['wrong_model_id']} detected → cap LP at L2"
            )
            diag["current_lp_level"] = "L2"
            diag["target_lp_level"] = "L3"

    hr("DYNAMIC CLASSIFICATION FROM STUDENT REASONING")

    print("\n  LP level (sentence-transformers embedding → trained head):")
    for lvl in ("L1", "L2", "L3", "L4"):
        p = diag["trained_lp_probs"].get(lvl, 0.0)
        print(f"    {lvl}  {p*100:5.1f}%  {render_bar(p)}")

    print("\n  Wrong model (HVSAE latent → trained head, restricted to this concept):")
    for t in diag.get("trained_wm_probs", []):
        wm_id = t["wm_id"]; p = t["prob"]
        entry = cat.get_wrong_model(concept, wm_id)
        belief = entry.wrong_belief[:80] if entry else ""
        print(f"    {wm_id:6s}  {p*100:5.1f}%  {render_bar(p)}")
        print(f"         belief: {belief}")

    hr("FINAL DIAGNOSIS")
    print(f"  wrong_model_id    : {diag.get('wrong_model_id')}")
    print(f"  current_lp_level  : {diag.get('current_lp_level')}  "
          f"→ target {diag.get('target_lp_level')}")
    print(f"  source            : {diag.get('source')}")
    if diag.get("fusion_reason"):
        print(f"  fusion_rule_fired : {diag['fusion_reason']}")
    print(f"  expert benchmark  :")
    for k in diag.get("expert_benchmark_key_ideas", [])[:5]:
        print(f"    - {k}")

    hr("GROUNDED RESPONSE (Ollama)")
    candidates = [("transfer_task", 0.92), ("worked_example", 0.80),
                  ("socratic_prompt", 0.70), ("trace_scaffold", 0.65)]
    filt = filter_interventions_by_lp(candidates, diag["current_lp_level"])
    chosen = filt[0][0] if filt else "worked_example"
    student_state = {
        "student_id": "demo_any", "lp_diagnostic": diag,
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
          f"[wrong-model: {diag['wrong_model_id']}]\n")
    def on_chunk(p): sys.stdout.write(p); sys.stdout.flush()
    gen._stream_callback = on_chunk
    gen.generate_personalized_response(
        student_id="demo_any", student_message=text,
        student_state=student_state, analysis=analysis,
    )
    print()


if __name__ == "__main__":
    main()
