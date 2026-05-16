"""
Probe with grader ON across LP levels: does the system grade EACH concept
the student raised AND produce a level-appropriate reply for each?

Two scenarios:
  CASE A — low-level multi-concept (typical student, confused on 2 concepts).
  CASE B — L4-level multi-concept (student generalising across 2 concepts).

For each case the probe shows:
  - per-concept rubric_grader verdict (level, confidence, justification)
  - per-concept final LP level + diagnostic_confidence
  - selected focus + intervention type
  - the actual generated tutor reply
  - audit: does the reply address each concept? Is it level-appropriate?
"""
import os, sys, time
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.orchestrator.lp_diagnostic       import LPDiagnostician, classify_lp_level
from src.orchestrator.concept_resolver    import ConceptResolver
from src.orchestrator.enhanced_personalized_generator import EnhancedPersonalizedGenerator


CASE_A_msg = (
    "my loop never stops AND the array index keeps crashing on me, "
    "what am I doing wrong"
)
# Crafted to show L4 generalisation on TWO concepts at once: the student
# is connecting a mechanism (== compares addresses) to a broader rule
# (any object reference) AND doing the same with the loop-update mechanism
# across loop variants.
CASE_B_msg = (
    "I think the same principle applies everywhere — == compares addresses "
    "for any object reference in Java, not just String, so my custom Point "
    "class will need .equals() too. And the same idea about an infinite "
    "loop applies to any for/while/do-while: if the condition variable "
    "is never updated, the condition is always true. Why did Java's "
    "designers make == reference equality by default?"
)


def run_case(label: str, msg: str, intervention_default: str) -> None:
    print("\n" + "=" * 78)
    print(f"CASE: {label}")
    print("=" * 78)
    print(f"  message: {msg}")

    d = LPDiagnostician(enable_rubric_grader=True)
    r = ConceptResolver()
    g = EnhancedPersonalizedGenerator()
    sd = {"question": msg}
    resolved = r.resolve(sd)
    print(f"  resolved concepts: {[(c, round(s,2)) for c,s in resolved]}")

    # Per-concept grading via diagnose_multi (each concept calls diagnose,
    # which calls the rubric grader against THAT concept's rubric).
    multi = d.diagnose_multi(student_id="probe", question_text=msg,
                             resolved_concepts=resolved)
    print(f"\n  ── per-concept grader + diagnosis ──")
    for c, dg in multi["diagnostics"].items():
        rg = dg.get("rubric_grade") or {}
        kw = classify_lp_level(msg)["level"]
        print(f"\n    CONCEPT  '{c}'  (focus={dg.get('is_focus')})")
        print(f"      keyword classifier  : {kw}")
        print(f"      rubric grader       : {rg.get('level','?')}  "
              f"conf={rg.get('confidence', 0):.2f}")
        print(f"      grader said         : {(rg.get('justification') or '')[:140]}")
        print(f"      final LP level      : {dg.get('current_lp_level')}  "
              f"target={dg.get('target_lp_level')}")
        print(f"      diagnostic_conf     : {dg.get('diagnostic_confidence', 0):.2f}")
        print(f"      wrong_model_id      : {dg.get('wrong_model_id') or '(none-specific)'}")

    # Pick a level-appropriate intervention for the focus.
    focus_level = multi["focus"].get("current_lp_level", "L1")
    intervention_type = {
        "L1": "worked_example", "L2": "trace_scaffold",
        "L3": "transfer_prompt", "L4": "transfer_task",
    }.get(focus_level, intervention_default)
    print(f"\n  focus_concept     : {multi['focus_concept']}")
    print(f"  focus level       : {focus_level}")
    print(f"  intervention type : {intervention_type}  (level-appropriate)")

    student_state = {
        "student_id": "probe", "interaction_count": 1,
        "personality": {"openness":.6,"conscientiousness":.5,
                        "extraversion":.5,"agreeableness":.5,"neuroticism":.4},
        "knowledge_state": {"overall_mastery": 0.30 if focus_level=="L1" else 0.75,
                            "mastery_history":[0.30 if focus_level=="L1" else 0.75]},
        "psychological_graph": {},
        "progression_graph":   {"stage": 1 if focus_level=="L1" else 4,
                                "scaffold_level": 4 if focus_level=="L1" else 1},
        "content_channel":     {"encoding_strength":
                                "surface" if focus_level=="L1" else "deep"},
        "language_channel":    {},
        "recommended_intervention": {"type": intervention_type,
                                     "rationale": f"level-appropriate for {focus_level}"},
        "lp_diagnostic":       multi["focus"],
        "lp_diagnostic_multi": multi,
    }
    analysis = {"emotion": "confused" if focus_level=="L1" else "engaged",
                "frustration_level": 0.4 if focus_level=="L1" else 0.1,
                "engagement_score":  0.6 if focus_level=="L1" else 0.9}

    print(f"\n  ── generated tutor reply ──")
    t0 = time.time()
    reply = g.generate_personalized_response(
        student_id="probe", student_message=msg,
        student_state=student_state, analysis=analysis,
    )
    dt = time.time() - t0
    for line in reply.splitlines():
        print(f"  | {line}")
    print(f"\n  (elapsed: {dt:.1f}s, {len(reply)} chars)")

    # Audits
    cliches = ["great question","good question","let's dive in","let's break",
               "let's understand","let's see","this might be happening",
               "no worries","don't worry","we'll come back to that",
               "as a beginner","remember that","in summary","to recap","hopefully"]
    low = reply.lower()
    hits = [c for c in cliches if c in low]
    focus_c = multi["focus_concept"]
    non_focus = [c for c in multi["diagnostics"] if c != focus_c]
    per_concept_hits = {}
    for c in non_focus:
        heading = f"on {c}".lower()
        per_concept_hits[c] = (heading in low) or f"**{c}" in low or f"### {c}" in low

    print(f"\n  Anti-cliche audit          : "
          f"{'CLEAN' if not hits else 'CLICHES -> ' + str(hits)}")
    print(f"  Focus concept addressed    : '{focus_c}' (intervention={intervention_type})")
    for c, taught in per_concept_hits.items():
        print(f"  Non-focus '{c}' mini-reply : "
              f"{'PRESENT (sub-heading found)' if taught else 'MISSING'}")
    if focus_level in ("L3", "L4"):
        # L3/L4 quality check: did the reply use TRANSFER / generalisation
        # vocabulary, or did it slip into L1/L2 worked-example mode?
        transfer_cues = ["same principle","applies to","generalise","generalize",
                         "design choice","design rationale","why java","tradeoff",
                         "trade-off","extend","novel","another case","analogous"]
        transfer_hits = [t for t in transfer_cues if t in low]
        worked_example_cues = ["here's a simple example","```java"]
        we_hits = [w for w in worked_example_cues if w in low]
        print(f"  L3/L4 transfer cues used   : {transfer_hits or 'NONE — too L1-shaped'}")
        if we_hits and not transfer_hits:
            print(f"  WARNING: reply opens a worked example without transfer "
                  f"framing — wrong shape for {focus_level}")


if __name__ == "__main__":
    run_case("A — low-level (L1 confused, two concepts)",
             CASE_A_msg, intervention_default="worked_example")
    run_case("B — L4 generalisation (student transferring across two concepts)",
             CASE_B_msg, intervention_default="transfer_task")
