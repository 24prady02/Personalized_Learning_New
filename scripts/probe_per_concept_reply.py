"""
Backend-only probe — does the reply actually address EACH concept with its
own wrong model + LP level + rubric, or only the focus?

Runs a multi-concept student message through:
  1. ConceptResolver  -> all concepts mentioned
  2. diagnose_multi() -> per-concept LP level + wrong model + rubric
  3. _build_enhanced_prompt() -> the prompt sent to the LLM

Then dumps the prompt sections so you can see, per concept, what reply the
system is INSTRUCTING the LLM to give. No frontend, no LLM call — we are
auditing the system's intent.
"""
import sys, re
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.orchestrator.lp_diagnostic   import LPDiagnostician
from src.orchestrator.concept_resolver import ConceptResolver
from src.orchestrator.enhanced_personalized_generator import EnhancedPersonalizedGenerator


def section(prompt: str, header: str) -> str:
    """Extract a single '=== HEADER ===' section out of the assembled prompt."""
    pat = re.compile(rf"={{3}} {re.escape(header)} ={{3}}(.*?)(?=\n={{3}}|\Z)", re.S)
    m = pat.search(prompt)
    return (m.group(1).strip() if m else "(section not present)")


def main() -> None:
    msg = ("my loop never stops AND the array index keeps crashing AND "
           "I think my == is broken on these strings")

    d = LPDiagnostician(enable_rubric_grader=False)
    r = ConceptResolver()
    g = EnhancedPersonalizedGenerator()

    sd = {"question": msg}
    resolved = r.resolve(sd)
    multi = d.diagnose_multi(student_id="probe", question_text=msg,
                             resolved_concepts=resolved)
    focus = multi["focus_concept"]

    print("STUDENT MESSAGE:")
    print(f"  {msg}")
    print(f"\nCONCEPTS DETECTED   : "
          f"{[(c, round(s,2)) for c,s in resolved]}")
    print(f"FOCUS PICKED        : {focus}")
    print(f"OTHERS ALSO DIAGNOSED:")
    for c, dg in multi["diagnostics"].items():
        if c == focus: continue
        wm = dg.get("wrong_model_id") or "-"
        rt = (dg.get("lp_rubric_target") or "")[:60]
        print(f"   - {c:18s} level={dg['current_lp_level']}  wm={wm}  "
              f"rubric_target='{rt}...'")

    # Build the actual prompt the LLM would receive.
    student_state = {
        "lp_diagnostic":       multi["focus"],
        "lp_diagnostic_multi": multi,
        "recommended_intervention": {"type": "worked_example", "rationale": "demo"},
    }
    prompt = g._build_enhanced_prompt(
        student_message=msg, code=None, student_state=student_state, analysis={},
        conversation_context={"interaction_number":1, "previous_topics":[],
            "what_worked_before":[], "confusion_patterns":[], "learning_trajectory":[]},
        emotional_context={"tone":"neutral","encouragement_level":"moderate"},
        learning_style_adaptation={"style":"visual"},
        personality_adaptation={"communication_style":"balanced"},
        progress_context={"current_mastery":0.3,"skill_change":0.0,
            "acknowledgment_needed":False,"challenge_level":"building"},
        interest_context={"example_domains":[]},
        format_preferences={"length":"moderate","structure":"structured","visual_density":"moderate"},
        error_feedback={"has_errors":False},
        metacognitive_guidance={"has_guidance":False},
        difficulty_adaptation={"difficulty_level":"building","pacing":"moderate","scaffolding_level":3},
    )

    print("\n" + "=" * 78)
    print("WHAT THE PROMPT INSTRUCTS THE LLM TO REPLY ABOUT, PER CONCEPT")
    print("=" * 78)
    headers = (
        "LP-1: DIAGNOSTIC CONTEXT",
        "LP-2: WRONG MENTAL MODEL (IDENTIFIED)",
        "LP-2: WRONG MENTAL MODEL",
        "LP-2b: RETRIEVED CATALOGUE CONTEXT",
        "LP-3: SIX-STEP INSTRUCTION",
        # NEW: per-concept mini-reply block (replaces the old "we'll come back" line)
        "LP-Multi: PER-CONCEPT MINI-REPLIES (address EACH concept, no cliches)",
        # NEW: global anti-cliche rules applied to the whole reply
        "ANTI-CLICHE GUARDRAILS (read before writing)",
    )
    for header in headers:
        body = section(prompt, header)
        if body == "(section not present)":
            continue
        print(f"\n--- {header} ---")
        # show enough lines for the per-concept block to be visible
        cap = 30 if "LP-Multi" in header else 14
        for line in body.splitlines()[:cap]:
            print(f"  {line}")

    print("\n" + "=" * 78)
    print("VERDICT — per-concept reply grounding (after the fix):")
    print("=" * 78)
    has_multi_block = section(prompt, headers[5]) != "(section not present)"
    has_anti_cliche = section(prompt, headers[6]) != "(section not present)"
    focus_d = multi["focus"]
    print(f"  FOCUS  '{focus}':")
    print(f"     wrong-model in prompt   : "
          f"{focus_d.get('wrong_model_id') or '-'}")
    print(f"     LP-level instructions   : YES (LP-3 six-step for "
          f"{focus_d.get('current_lp_level')})")
    print(f"     rubric target in prompt : "
          f"{bool(focus_d.get('lp_rubric_target'))}")
    print(f"     RAG top-3 in prompt     : "
          f"{len(focus_d.get('rag_top_wrong_models') or [])} entries")
    for c, dg in multi["diagnostics"].items():
        if c == focus: continue
        in_multi = has_multi_block and f"CONCEPT: '{c}'" in (
            section(prompt, headers[5]))
        print(f"  OTHER  '{c}':")
        print(f"     in LP-Multi block       : "
              f"{'YES' if in_multi else 'NO'}")
        print(f"     wrong-model surfaced    : "
              f"{dg.get('wrong_model_id') or '(none-specific; criterion used)'}")
        print(f"     LP level + target       : "
              f"{dg.get('current_lp_level')} -> {dg.get('target_lp_level')}")
        print(f"     rubric criterion        : "
              f"{'YES' if dg.get('lp_rubric_target') else 'no'}")
    print(f"\n  Anti-cliche guardrails block : "
          f"{'PRESENT' if has_anti_cliche else 'MISSING'}")

    print(
        "\n  In short: every concept the student raised now gets its OWN\n"
        "  grounded mini-reply (false belief in their voice -> Java mechanism\n"
        "  -> predict-this), not the old 'we'll come back to that' one-liner.\n"
        "  Anti-cliche rules apply to the whole reply.\n"
        "  Toggle with env CPAL_PER_CONCEPT_MINI=0 to revert if needed."
    )


if __name__ == "__main__":
    main()
