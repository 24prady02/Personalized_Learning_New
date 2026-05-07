"""
Code-chunk + student-reasoning demo.

Shows:
  - The Java code the student is looking at
  - The student's reasoning about the code
  - LP level head distribution (which level is their reasoning at?)
  - WM head distribution (which of the 3 wrong models for this concept?)
  - Diagnosis with fusion
  - Grounded response generated through the real pls_fixed pipeline
"""
import os, sys, torch
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from src.models.hvsae import HVSAE
from src.knowledge_graph.mental_models import get_catalogue
from src.orchestrator.lp_diagnostic import (
    LPDiagnostician, filter_interventions_by_lp, LP_INDEX, LP_ORDER,
)
from src.orchestrator.enhanced_personalized_generator import (
    EnhancedPersonalizedGenerator,
)


# =========================================================================
# SCENARIO
# =========================================================================
CONCEPT = "boolean_operators"

CODE_CHUNK = """int score = 50;

if (score >= 0 || score <= 100) {
    System.out.println("Valid score");
} else {
    System.out.println("Out of range");
}"""

STUDENT_REASONING = (
    "I'm trying to validate that a score sits in the 0-to-100 range. I used "
    "|| because — thinking about it in English — I want the score to be "
    "positive OR at most 100; as long as either bound is satisfied the value "
    "should count. But when I plug in score = 200, the program still prints "
    "'Valid score', which is clearly wrong. If || is 'or' and at least one "
    "side is true the whole check should pass... isn't that what I want for a "
    "range check? Both && and || seem like they should work here since the "
    "conditions are basically saying the same thing from two directions."
)


def bar(p, w=28):
    f = int(round(p * w))
    return "█" * f + "·" * (w - f)


def hr(t="", g="="):
    print("\n" + g * 80)
    if t: print(" " + t); print(g * 80)


def main():
    # =====================================================================
    hr("TURN 1 — STUDENT SHOWS TUTOR A CODE CHUNK AND EXPLAINS", "#")
    print("\n  CODE the student is looking at:")
    print("  " + "─" * 72)
    for line in CODE_CHUNK.splitlines():
        print(f"    {line}")
    print("  " + "─" * 72)
    print(f"\n  STUDENT'S REASONING:")
    for line in STUDENT_REASONING.split(". "):
        if line.strip():
            print(f"    {line.strip().rstrip('.')}.")

    # =====================================================================
    hr("LOADING MODELS")
    ck = torch.load(os.path.join(ROOT, "checkpoints", "best.pt"),
                    map_location="cpu", weights_only=False)
    hvsae = HVSAE(ck["config"])
    hvsae.load_state_dict(ck["hvsae_state"])
    hvsae.eval()
    cat = get_catalogue(
        os.path.join(ROOT, "data", "mental_models",
                     "wrong_models_catalogue.json")
    )
    print("  ✓ HVSAE loaded, catalogue loaded")

    # HVSAE forward on the combined code + reasoning (for latent + misconception)
    full_input = STUDENT_REASONING + "\nCODE:\n" + CODE_CHUNK
    try:
        from transformers import AutoTokenizer
        tk = AutoTokenizer.from_pretrained("bert-base-uncased")
        text_ids = tk(full_input, return_tensors="pt", padding=True,
                      truncation=True, max_length=128)["input_ids"].long() % 6000
    except Exception:
        text_ids = torch.randint(1, 5999, (1, 16))
    batch = {"code_tokens": torch.zeros(1, 10, dtype=torch.long),
             "text_tokens": text_ids,
             "action_sequence": torch.ones(1, 8, dtype=torch.long)}
    with torch.no_grad():
        hv_out = hvsae.forward(batch, compute_graph=False)
    latent = hv_out["latent"]
    mp = torch.softmax(hv_out["misconception_logits"], dim=-1)
    print("  ✓ HVSAE forward run on [reasoning + code]")

    # =====================================================================
    hr("DIAGNOSIS — all trained heads reading the student reasoning")
    dx = LPDiagnostician(catalogue=cat, hvsae_model=hvsae)
    diag = dx.diagnose(
        student_id="demo_code", concept=CONCEPT, question_text=STUDENT_REASONING,
        stored_lp_level="L1", stored_lp_streak=0,
        hvsae_latent=latent, hvsae_misconception_probs=mp,
    ).to_dict()

    print(f"\n  CONCEPT UNDER EXAMINATION: {CONCEPT}")
    print(f"  (catalogue defines 3 wrong models for this concept: "
          f"{[wm['id'] for wm in __import__('json').load(open(os.path.join(ROOT, 'data', 'mental_models', 'wrong_models_catalogue.json'), encoding='utf-8'))['concepts'][CONCEPT]['wrong_models']]})")

    print(f"\n  ┌─ LP LEVEL — sentence-transformers → 4-class head ─┐")
    lp_probs = diag.get("trained_lp_probs", {})
    lp_pick = max(lp_probs, key=lp_probs.get) if lp_probs else None
    for lvl in ("L1", "L2", "L3", "L4"):
        p = lp_probs.get(lvl, 0.0)
        mark = "  ← pick" if lvl == lp_pick else ""
        print(f"    {lvl}   {p*100:5.1f}%  {bar(p)}{mark}")

    print(f"\n  ┌─ WRONG MODEL — HVSAE latent → trained sub-head restricted to {CONCEPT} ─┐")
    for t in diag.get("trained_wm_probs", []):
        wm = cat.get_wrong_model(CONCEPT, t["wm_id"])
        belief = (wm.wrong_belief if wm else "")
        is_pick = (t == max(diag["trained_wm_probs"], key=lambda x: x["prob"]))
        mark = "  ← pick" if is_pick else ""
        print(f"    {t['wm_id']:6s} {t['prob']*100:5.1f}%  {bar(t['prob'])}{mark}")
        print(f"           belief: \"{belief}\"")

    # Fusion
    reasons = []
    lvl_idx = LP_INDEX.get(diag["current_lp_level"], 0)
    if diag.get("wrong_model_id") and diag.get("match_score", 0) >= 0.4 \
            and lvl_idx >= LP_INDEX["L3"]:
        reasons.append(
            f"wrong-model {diag['wrong_model_id']} detected (conf "
            f"{diag['match_score']:.2f}) → cap LP at L2 (misconception present)"
        )
        lvl_idx = LP_INDEX["L2"]
    diag["current_lp_level"] = LP_ORDER[lvl_idx]
    diag["target_lp_level"]  = LP_ORDER[min(lvl_idx + 1, 3)]

    print(f"\n  ┌─ FINAL DIAGNOSIS (after fusion) ─┐")
    print(f"    wrong_model_id   : {diag['wrong_model_id']}  "
          f"(via {diag['source']})")
    wm = cat.get_wrong_model(CONCEPT, diag['wrong_model_id'])
    if wm:
        print(f"    wrong belief     : {wm.wrong_belief}")
        print(f"    origin           : {wm.origin}")
    print(f"    LP level         : {diag['current_lp_level']}  "
          f"→ target {diag['target_lp_level']}")
    if reasons:
        print(f"    fusion           : {reasons[0]}")
    print(f"    L3 benchmark     :")
    for k in diag.get("expert_benchmark_key_ideas", [])[:5]:
        print(f"      - {k}")

    # =====================================================================
    hr("GROUNDED RESPONSE")
    candidates = [("transfer_task", 0.92), ("worked_example", 0.80),
                  ("socratic_prompt", 0.70), ("trace_scaffold", 0.65)]
    filt = filter_interventions_by_lp(candidates, diag["current_lp_level"])
    chosen = filt[0][0] if filt else "worked_example"

    student_state = {
        "student_id": "demo_code",
        "lp_diagnostic": diag,
        "recommended_intervention": {"type": chosen},
        "personality_profile": {"communication_style": "direct",
                                "learning_preference": "visual"},
        "bkt_mastery": {CONCEPT: 0.30},
        "emotional_state": "confused",
        "interaction_count": 1,
    }
    analysis = {"emotion": {"primary": "confused", "confidence": 0.7},
                "knowledge_gaps": [CONCEPT], "pedagogical_kg": {}}

    gen = EnhancedPersonalizedGenerator()
    print(f"  [model: {gen._ollama_model}]  [intervention: {chosen}]")
    print(f"  [LP: {diag['current_lp_level']} → {diag['target_lp_level']}]  "
          f"[wrong-model: {diag['wrong_model_id']}]\n")
    full_msg = (
        f"Here is the code I'm looking at:\n\n{CODE_CHUNK}\n\n"
        f"{STUDENT_REASONING}"
    )
    def on_chunk(p): sys.stdout.write(p); sys.stdout.flush()
    gen._stream_callback = on_chunk
    gen.generate_personalized_response(
        student_id="demo_code", student_message=full_msg,
        student_state=student_state, analysis=analysis, code=CODE_CHUNK,
    )
    print()


if __name__ == "__main__":
    main()
