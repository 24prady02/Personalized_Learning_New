"""
End-to-end probe with Ollama LIVE.

Part A — RubricGrader live: for several student messages, show the keyword
         classifier's verdict beside the LLM rubric-grader's verdict so you
         can see the dynamic tier doing real work (level + confidence +
         justification per case, plus diagnostic_confidence shift).

Part B — Full per-concept reply live: generate a real tutor reply for a
         multi-concept message via EnhancedPersonalizedGenerator and print
         it, so you can see whether the LP-Multi mini-replies and the
         anti-cliche guardrails actually shape the output.
"""
import os, sys, time
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.orchestrator.lp_diagnostic       import LPDiagnostician, classify_lp_level
from src.orchestrator.concept_resolver    import ConceptResolver
from src.orchestrator.enhanced_personalized_generator import EnhancedPersonalizedGenerator


def part_A_grader_live() -> None:
    print("=" * 78)
    print("PART A — Rubric grader LIVE (Ollama on)")
    print("=" * 78)
    d = LPDiagnostician(enable_rubric_grader=True)
    r = ConceptResolver()

    cases = [
        # (label, expected-ish level the grader should reach, message)
        ("L1 — pure symptom",
         "L1",
         "why is == false, they look the same to me"),
        ("L2 — names rule",
         "L2",
         "I know I have to use .equals() for strings instead of =="),
        ("L3 — mechanism trace, plain words (no jargon!)",
         "L3",
         "the two new String() calls each make their own object somewhere "
         "in memory, so == checks if those two memory spots are the same "
         "(they aren't), while .equals() walks the characters"),
        ("L4 — generalisation",
         "L4",
         "this is the same idea as comparing any two object references in "
         "Java — == is identity, .equals() is whatever the class chose to "
         "override; same principle applies to my own class"),
    ]
    for label, expected, text in cases:
        kw = classify_lp_level(text)["level"]                # keyword classifier
        diag = d.diagnose(student_id="probe",
                          concept="string_equality",
                          question_text=text)
        grade = diag.rubric_grade or {}
        agree = "AGREE" if (grade.get("level") == kw) else "DISAGREE"
        print(f"\n  CASE: {label}")
        print(f"    text          : {text[:75]}{'...' if len(text)>75 else ''}")
        print(f"    keyword cls   : {kw}")
        print(f"    rubric grader : {grade.get('level','?')}  "
              f"conf={grade.get('confidence',0):.2f}  "
              f"src={grade.get('source','?')}")
        print(f"    grader said   : {grade.get('justification','')[:120]}")
        print(f"    final LP      : {diag.current_lp_level}  "
              f"diagnostic_conf={diag.diagnostic_confidence:.2f}")
        print(f"    sources       : {kw}+{grade.get('level','?')}  -> {agree}")


def part_B_full_reply_live() -> None:
    print("\n\n" + "=" * 78)
    print("PART B — Full multi-concept reply LIVE (LP-Multi + anti-cliche on)")
    print("=" * 78)
    msg = ("my loop never stops AND the array index keeps crashing on me, "
           "what am I doing wrong")

    d = LPDiagnostician(enable_rubric_grader=False)  # focus this part on REPLY shape
    r = ConceptResolver()
    sd = {"question": msg}
    resolved = r.resolve(sd)
    multi = d.diagnose_multi(student_id="probe", question_text=msg,
                             resolved_concepts=resolved)
    print(f"\n  message : {msg}")
    print(f"  resolved: {[(c, round(s,2)) for c,s in resolved]}")
    print(f"  focus   : {multi['focus_concept']}  "
          f"others={[c for c in multi['diagnostics'] if c != multi['focus_concept']]}")

    g = EnhancedPersonalizedGenerator()
    print(f"  model   : {g._ollama_model}\n")

    student_state = {
        "student_id": "probe",
        "interaction_count": 1,
        "personality": {"openness": 0.5, "conscientiousness": 0.5,
                        "extraversion": 0.5, "agreeableness": 0.5,
                        "neuroticism": 0.4},
        "knowledge_state": {"overall_mastery": 0.30, "mastery_history": [0.30]},
        "psychological_graph": {},
        "progression_graph":   {"stage": 1, "scaffold_level": 4},
        "content_channel":     {"encoding_strength": "surface"},
        "language_channel":    {},
        "recommended_intervention": {"type": "worked_example",
                                     "rationale": "L1 -> L2 build mechanism"},
        "lp_diagnostic":       multi["focus"],
        "lp_diagnostic_multi": multi,
    }
    analysis = {"emotion": "confused", "frustration_level": 0.4,
                "engagement_score": 0.6}

    print("  ── generated tutor reply ──")
    t0 = time.time()
    reply = g.generate_personalized_response(
        student_id="probe", student_message=msg,
        student_state=student_state, analysis=analysis,
    )
    dt = time.time() - t0
    # indent for readability
    for line in reply.splitlines():
        print(f"  | {line}")
    print(f"\n  (elapsed: {dt:.1f}s, {len(reply)} chars)")

    # Anti-cliche audit — including the soft-filler "let's ..." patterns
    # that slipped past the previous run.
    cliches = ["great question", "good question", "let's dive in",
               "let's break", "let's understand", "let's see",
               "this might be happening",
               "no worries", "don't worry", "we'll come back to that",
               "as a beginner", "remember that", "in summary", "to recap",
               "hopefully"]
    low = reply.lower()
    hits = [c for c in cliches if c in low]

    # Per-concept teaching audit — does each non-focus concept get its OWN
    # mini-reply (sub-heading), not just a passing mention?
    focus_c = multi["focus_concept"]
    non_focus = [c for c in multi["diagnostics"] if c != focus_c]
    per_concept_hits = {}
    for c in non_focus:
        # The LP-Multi block instructs the model to emit a "**On <concept>:**"
        # sub-heading per non-focus concept; check that the heading appeared.
        heading = f"on {c}".lower()
        per_concept_hits[c] = (heading in low) or (
            f"**{c}" in low) or (f"### {c}" in low)

    print(f"\n  Anti-cliche audit  : "
          f"{'CLEAN' if not hits else 'CLICHES FOUND -> ' + str(hits)}")
    print(f"  Focus concept     : '{focus_c}' (taught via LP-3)")
    for c, taught in per_concept_hits.items():
        print(f"  Mini-reply '{c}' : "
              f"{'PRESENT (sub-heading found)' if taught else 'MISSING'}")


if __name__ == "__main__":
    part_A_grader_live()
    part_B_full_reply_live()
