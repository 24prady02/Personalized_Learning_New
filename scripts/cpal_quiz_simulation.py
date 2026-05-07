"""
5-scenario quiz simulation.

For each scenario:
  - Code snippet
  - Multiple-choice options
  - Student's pick
  - Student's reasoning for that pick

The choice + reasoning is processed by the full CPAL pipeline:
  - HVSAE encoding
  - Trained LP head (sentence-transformers) → 4-class distribution
  - Trained WM sub-head (HVSAE latent) → 3-class distribution for concept
  - Fusion rules
  - Ollama grounded response

Writes a single Markdown report to output/cpal_quiz_report.md.
"""
import os, sys, json, time
from pathlib import Path
import torch

ROOT = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, str(ROOT))

from src.models.hvsae import HVSAE
from src.knowledge_graph.mental_models import get_catalogue
from src.orchestrator.lp_diagnostic import (
    LPDiagnostician, filter_interventions_by_lp, LP_INDEX, LP_ORDER,
)
from src.orchestrator.enhanced_personalized_generator import (
    EnhancedPersonalizedGenerator,
)


SCENARIOS = [
    # -----------------------------------------------------------------
    {
        "id": 1,
        "concept": "string_equality",
        "code": (
            'String a = new String("hello");\n'
            'String b = new String("hello");\n'
            'System.out.println(a == b);'
        ),
        "question": "What does this print?",
        "options": {
            "A": "true — both strings contain 'hello'",
            "B": "false — they are different objects",
            "C": "Compile error",
            "D": "The word 'hello' prints twice",
        },
        "student_pick": "A",
        "student_reasoning": (
            "Both variables a and b are holding the text 'hello'. If you "
            "compare them with ==, Java should check that they say the same "
            "thing — which they do. Otherwise how would you ever test if two "
            "strings match? A comparison operator has to look inside the "
            "objects to tell if they're the same, or it wouldn't be useful."
        ),
        "correct_answer": "B",
        "expected_wm": "SE-A",  # == compares content (student's stated belief)
    },
    # -----------------------------------------------------------------
    {
        "id": 2,
        "concept": "integer_division",
        "code": (
            'double result = 5 / 2;\n'
            'System.out.println(result);'
        ),
        "question": "What does this print?",
        "options": {
            "A": "2.5",
            "B": "2.0",
            "C": "2",
            "D": "Compile error — mismatched types",
        },
        "student_pick": "A",
        "student_reasoning": (
            "Mathematically, five divided by two is two and a half. I told "
            "Java to store the result in a double, which holds decimal "
            "numbers, so it should preserve the fractional part. The "
            "destination type determines how the computation is carried out "
            "— since I asked for a double, I should get 2.5."
        ),
        "correct_answer": "B",  # 2.0 because int/int → int, then widened
        "expected_wm": "ID-B",  # type determined by result not operands
    },
    # -----------------------------------------------------------------
    {
        "id": 3,
        "concept": "null_pointer",
        "code": (
            'public class Widget {\n'
            '    private String label;\n'
            '    public String describe() {\n'
            '        return label.toUpperCase();\n'
            '    }\n'
            '}\n'
            '// elsewhere:\n'
            'Widget w = new Widget();\n'
            'System.out.println(w.describe());'
        ),
        "question": "What happens at runtime?",
        "options": {
            "A": "Prints empty string",
            "B": 'Prints "LABEL" (name of the field in uppercase)',
            "C": "Throws NullPointerException",
            "D": "Compile error",
        },
        "student_pick": "B",
        "student_reasoning": (
            "I declared a field called label — I gave it a name. The field "
            "is defined at the top of the class, so Java knows it exists. "
            "When I call describe, it takes the label I named and converts "
            "it to uppercase. Since the field is literally called 'label', "
            "and I've told Java that's its identity, that's what gets "
            "converted. B seems right."
        ),
        "correct_answer": "C",
        "expected_wm": "NP-A",  # Declaring creates the object
    },
    # -----------------------------------------------------------------
    {
        "id": 4,
        "concept": "array_index",
        "code": (
            'int[] arr = {10, 20, 30, 40, 50};\n'
            'System.out.println(arr[5]);'
        ),
        "question": "What does this print?",
        "options": {
            "A": "50 (the fifth element)",
            "B": "10 (the first element)",
            "C": "0 (default int)",
            "D": "ArrayIndexOutOfBoundsException",
        },
        "student_pick": "A",
        "student_reasoning": (
            "The array has five numbers: 10, 20, 30, 40, 50. So the fifth "
            "one is 50. When I write arr[5], I'm asking for the fifth slot "
            "— that's the one holding 50. Counting starts from one when "
            "we're talking about positions, and arr[5] means position 5."
        ),
        "correct_answer": "D",
        "expected_wm": "AI-A",  # arrays start at 1
    },
    # -----------------------------------------------------------------
    {
        "id": 5,
        "concept": "variable_scope",
        "code": (
            'for (int i = 0; i < 3; i++) {\n'
            '    int total = i * 10;\n'
            '}\n'
            'System.out.println(total);'
        ),
        "question": "What happens here?",
        "options": {
            "A": "Prints 20 (last value of total)",
            "B": "Prints 0 (initial value)",
            "C": "Compile error",
            "D": "Prints 30",
        },
        "student_pick": "A",
        "student_reasoning": (
            "Inside the loop, total gets assigned i*10 each iteration. The "
            "last time through, i=2 so total=20. Once the variable has been "
            "given a value, it holds that value — it's not like Java forgets "
            "things. total was just declared inside the loop, but the "
            "assignment happened, so 20 stays there afterward."
        ),
        "correct_answer": "C",
        "expected_wm": "VS-C",  # variables in loop persist after
    },
]


def bar(p, w=24):
    f = int(round(p * w))
    return "█" * f + "·" * (w - f)


def diagnose(scenario, hvsae, cat, diagnostician, tokenizer):
    """Run full diagnosis on one scenario."""
    text = (
        f"Quiz: {scenario['question']}\n"
        f"Code:\n{scenario['code']}\n"
        f"My pick: option {scenario['student_pick']} "
        f"({scenario['options'][scenario['student_pick']]})\n"
        f"My reasoning: {scenario['student_reasoning']}"
    )

    # HVSAE forward
    if tokenizer is not None:
        text_ids = tokenizer(text, return_tensors="pt", padding=True,
                             truncation=True, max_length=128
                             )["input_ids"].long() % 6000
    else:
        text_ids = torch.randint(1, 5999, (1, 16))
    batch = {"code_tokens": torch.zeros(1, 10, dtype=torch.long),
             "text_tokens": text_ids,
             "action_sequence": torch.ones(1, 8, dtype=torch.long)}
    with torch.no_grad():
        hv_out = hvsae.forward(batch, compute_graph=False)
    latent = hv_out["latent"]
    mp = torch.softmax(hv_out["misconception_logits"], dim=-1)

    diag = diagnostician.diagnose(
        student_id=f"quiz_{scenario['id']}",
        concept=scenario["concept"],
        question_text=scenario["student_reasoning"],
        stored_lp_level="L1", stored_lp_streak=0,
        hvsae_latent=latent, hvsae_misconception_probs=mp,
    ).to_dict()

    # Fusion: wrong-model present + reasoning is rule-ish → cap at L2
    lvl_idx = LP_INDEX.get(diag["current_lp_level"], 0)
    fusion_note = None
    if diag.get("wrong_model_id") and diag.get("match_score", 0) >= 0.4 \
            and lvl_idx >= LP_INDEX["L3"]:
        fusion_note = (f"wrong-model {diag['wrong_model_id']} with "
                       f"conf {diag['match_score']:.2f} → cap LP at L2")
        lvl_idx = LP_INDEX["L2"]
    diag["current_lp_level"] = LP_ORDER[lvl_idx]
    diag["target_lp_level"]  = LP_ORDER[min(lvl_idx + 1, 3)]
    diag["fusion_note"]      = fusion_note

    return diag, text


def generate_response(scenario, diag, gen):
    candidates = [("transfer_task", 0.92), ("worked_example", 0.80),
                  ("socratic_prompt", 0.70), ("trace_scaffold", 0.65)]
    filt = filter_interventions_by_lp(candidates, diag["current_lp_level"])
    chosen = filt[0][0] if filt else "worked_example"
    student_state = {
        "student_id": f"quiz_{scenario['id']}",
        "lp_diagnostic": diag,
        "recommended_intervention": {"type": chosen},
        "personality_profile": {"communication_style": "direct",
                                "learning_preference": "visual"},
        "bkt_mastery": {scenario["concept"]: 0.30},
        "emotional_state": "confused",
        "interaction_count": 1,
    }
    analysis = {"emotion": {"primary": "confused", "confidence": 0.7},
                "knowledge_gaps": [scenario["concept"]], "pedagogical_kg": {}}
    msg = (
        f"I was given this quiz question:\n\n{scenario['question']}\n\n"
        f"Code:\n```java\n{scenario['code']}\n```\n\n"
        f"I picked option {scenario['student_pick']}: "
        f"{scenario['options'][scenario['student_pick']]}\n\n"
        f"My reasoning: {scenario['student_reasoning']}"
    )
    return chosen, gen.generate_personalized_response(
        student_id=f"quiz_{scenario['id']}",
        student_message=msg,
        student_state=student_state,
        analysis=analysis, code=scenario["code"],
    )


def main():
    print("Loading HVSAE + catalogue + diagnostician + generator...")
    ck = torch.load(ROOT / "checkpoints" / "best.pt",
                    map_location="cpu", weights_only=False)
    hvsae = HVSAE(ck["config"]); hvsae.load_state_dict(ck["hvsae_state"]); hvsae.eval()
    cat = get_catalogue(
        ROOT / "data" / "mental_models" / "wrong_models_catalogue.json"
    )
    try:
        from transformers import AutoTokenizer
        tk = AutoTokenizer.from_pretrained("bert-base-uncased")
    except Exception:
        tk = None
    dx = LPDiagnostician(catalogue=cat, hvsae_model=hvsae)
    gen = EnhancedPersonalizedGenerator()

    results = []
    for scenario in SCENARIOS:
        print(f"\n[Scenario {scenario['id']}] concept={scenario['concept']} "
              f"pick={scenario['student_pick']} (correct={scenario['correct_answer']})")
        t0 = time.time()
        diag, combined_text = diagnose(scenario, hvsae, cat, dx, tk)
        print(f"  LP head: " + " ".join(
            f"{k}={diag['trained_lp_probs'].get(k,0)*100:.0f}%"
            for k in ("L1","L2","L3","L4")
        ))
        print(f"  WM head: " + " ".join(
            f"{t['wm_id']}={t['prob']*100:.0f}%"
            for t in diag.get("trained_wm_probs", [])
        ))
        print(f"  final: LP={diag['current_lp_level']} "
              f"wm={diag['wrong_model_id']} "
              f"source={diag['source']}")
        chosen, response = generate_response(scenario, diag, gen)
        results.append({
            "scenario":   scenario,
            "diagnosis":  diag,
            "intervention": chosen,
            "response":   response,
            "elapsed_s":  time.time() - t0,
        })
        print(f"  elapsed={results[-1]['elapsed_s']:.1f}s")

    # --- Compile markdown report ---
    out_path = ROOT / "output" / "cpal_quiz_report.md"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    lines = []
    lines.append("# CPAL Quiz Simulation — 5-Scenario Diagnostic Report\n")
    lines.append(f"Generated from: `pls_fixed/scripts/cpal_quiz_simulation.py`  \n")
    lines.append(f"Components exercised: HVSAE + trained LP head (sentence-transformers) + trained WM sub-head (HVSAE latent) + fusion rules + Ollama generator  \n")
    lines.append(f"5 scenarios × 5 concepts × 3 wrong models each = diagnostic signal across the catalogue.\n")
    lines.append(f"\n---\n")

    for r in results:
        s = r["scenario"]
        diag = r["diagnosis"]
        lines.append(f"\n## Scenario {s['id']} — `{s['concept']}`\n")
        lines.append(f"### Quiz\n")
        lines.append(f"**Question:** {s['question']}\n")
        lines.append(f"**Code:**\n```java\n{s['code']}\n```\n")
        lines.append(f"**Options:**\n")
        for k, v in s["options"].items():
            marker = " ← picked" if k == s["student_pick"] else ""
            correct = " ✓" if k == s["correct_answer"] else ""
            lines.append(f"- **{k}.** {v}{marker}{correct}\n")
        lines.append(f"\n**Student's reasoning:**  \n> {s['student_reasoning']}\n")

        lines.append(f"\n### Diagnosis (all trained components)\n")
        lines.append(f"**LP level distribution** (sentence-transformers → 4-class head, val_acc 0.743):\n\n")
        lines.append("```\n")
        for lvl in ("L1", "L2", "L3", "L4"):
            p = diag.get("trained_lp_probs", {}).get(lvl, 0.0)
            pick = " ← top" if p == max(diag.get("trained_lp_probs", {lvl:0}).values()) else ""
            lines.append(f"{lvl}  {p*100:5.1f}%  {bar(p)}{pick}\n")
        lines.append("```\n")

        lines.append(f"\n**Wrong-model distribution** (HVSAE latent → sub-head restricted to `{s['concept']}`):\n\n")
        lines.append("```\n")
        top_prob = max((t["prob"] for t in diag.get("trained_wm_probs", [])), default=0)
        for t in diag.get("trained_wm_probs", []):
            pick = " ← top" if t["prob"] == top_prob else ""
            lines.append(f"{t['wm_id']:6s} {t['prob']*100:5.1f}%  {bar(t['prob'])}{pick}\n")
        lines.append("```\n")
        for t in diag.get("trained_wm_probs", []):
            wm = get_catalogue(ROOT / "data" / "mental_models" / "wrong_models_catalogue.json").get_wrong_model(s["concept"], t["wm_id"])
            if wm:
                lines.append(f"- `{t['wm_id']}` belief: *\"{wm.wrong_belief}\"*\n")

        lines.append(f"\n**HVSAE concept-head top-3** (20-class over all concepts, independent of the assumed concept):\n\n")
        lines.append("```\n")
        for ct in diag.get("hvsae_concept_top3", []):
            lines.append(f"  {ct['concept_id']:22s} p={ct['prob']:.3f}\n")
        lines.append("```\n")

        lines.append(f"\n**LP-DIAGNOSIS SUMMARY:**\n\n")
        lines.append(f"| Field | Value |\n|---|---|\n")
        lines.append(f"| Concept (assumed) | `{s['concept']}` |\n")
        lines.append(f"| Wrong model identified | **{diag['wrong_model_id']}** via `{diag['source']}` |\n")
        wm = get_catalogue(ROOT / "data" / "mental_models" / "wrong_models_catalogue.json").get_wrong_model(s["concept"], diag['wrong_model_id'])
        if wm:
            lines.append(f"| Wrong belief | *{wm.wrong_belief}* |\n")
            lines.append(f"| Origin | *{wm.origin}* |\n")
        lines.append(f"| LP level (current → target) | **{diag['current_lp_level']} → {diag['target_lp_level']}** |\n")
        lines.append(f"| Confidence (match_score) | {diag.get('match_score', 0):.3f} |\n")
        if diag.get("fusion_note"):
            lines.append(f"| Fusion rule fired | {diag['fusion_note']} |\n")
        lines.append(f"| Intervention picked | `{r['intervention']}` (LP-valid for {diag['current_lp_level']}) |\n")

        lines.append(f"\n**Expert benchmark (L3 mechanism to convey):**\n")
        for k in diag.get("expert_benchmark_key_ideas", [])[:5]:
            lines.append(f"- {k}\n")

        lines.append(f"\n**Author-expected diagnosis vs. what the system picked:**\n")
        match = "✓" if diag["wrong_model_id"] == s["expected_wm"] else "✗"
        lines.append(f"- Expected: `{s['expected_wm']}`  |  Got: `{diag['wrong_model_id']}`  |  {match}\n")

        lines.append(f"\n### Generated tutor response ({r['intervention']}, qwen2.5-coder:7b)\n\n")
        lines.append("---\n\n")
        lines.append(r["response"].rstrip() + "\n\n")
        lines.append("---\n")
        lines.append(f"\n_Total pipeline time for this scenario: {r['elapsed_s']:.1f}s_\n")

    # Aggregate table
    lines.append(f"\n## Summary across 5 scenarios\n\n")
    lines.append(f"| # | Concept | Expected WM | Got WM | Match | LP | Intervention |\n")
    lines.append(f"|---|---|---|---|---|---|---|\n")
    correct_wm = 0
    for r in results:
        s = r["scenario"]; d = r["diagnosis"]
        ok = "✓" if d["wrong_model_id"] == s["expected_wm"] else "✗"
        if ok == "✓": correct_wm += 1
        lines.append(
            f"| {s['id']} | `{s['concept']}` | `{s['expected_wm']}` | "
            f"`{d['wrong_model_id']}` | {ok} | "
            f"{d['current_lp_level']} | `{r['intervention']}` |\n"
        )
    lines.append(f"\n**WM hit rate: {correct_wm}/5**\n")

    with open(out_path, "w", encoding="utf-8") as f:
        f.writelines(lines)
    print(f"\n✓ Report written to: {out_path}")


if __name__ == "__main__":
    main()
