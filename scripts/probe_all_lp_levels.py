"""
Probe every LP level (L1, L2, L3, L4) end-to-end with Ollama live.

For each level, run a calibrated student message through the full pipeline
and show:
  - resolved concept(s) + per-concept grader verdict
  - chosen focus + intervention type
  - the actual generated tutor reply
  - audit: did the reply match the LP level pedagogy?
      L1 = worked example, code, line-by-line, predict-this
      L2 = mechanism trace with compile-time/runtime/heap language
      L3 = transfer prompt to a NOVEL application (not re-teaching basics)
      L4 = design rationale / edge case / no re-teaching

The user's brief: "all Learning Levels need to be explained or understood".
This probe verifies each level produces a distinct, level-appropriate output.
"""
import os, sys, time
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.orchestrator.lp_diagnostic       import LPDiagnostician, classify_lp_level
from src.orchestrator.concept_resolver    import ConceptResolver
from src.orchestrator.enhanced_personalized_generator import EnhancedPersonalizedGenerator


CASES = [
    # (label, expected_level, intervention_for_level, message)
    ("L1 — pure symptom (single concept)", "L1", "worked_example",
     "why is == false on my two strings, they look the same to me"),
    ("L2 — knows rule, no mechanism",      "L2", "trace_scaffold",
     "I know I have to use .equals() instead of == for strings but I don't "
     "know why == fails"),
    ("L3 — articulates mechanism (plain words)", "L3", "transfer_prompt",
     "each new String() call makes its own object somewhere in memory, so "
     "== checks if those two memory spots are the same (they aren't), while "
     ".equals() walks the characters"),
    ("L4 — generalisation across concepts",  "L4", "transfer_task",
     "I think the same principle applies everywhere — == compares addresses "
     "for any object reference in Java, not just String, so my custom Point "
     "class will need .equals() too. And the same idea about an infinite "
     "loop applies to any for/while/do-while. Why did Java's designers make "
     "== reference equality by default?"),
]

LEVEL_AUDIT_CUES = {
    "L1": {"want": ["```java", "rule", "predict", "check"],
           "avoid": ["transfer", "design choice", "tradeoff", "generalise",
                    "generalize"]},
    "L2": {"want": ["compile-time", "runtime", "heap", "reference", "trace",
                    "address"],
           "avoid": []},
    "L3": {"want": ["novel", "same principle", "applies to", "transfer",
                    "different concept", "another", "shared mechanism"],
           "avoid": ["worked example", "let's start with the basics"]},
    "L4": {"want": ["design", "tradeoff", "trade-off", "rationale", "why java",
                    "edge case", "principle", "generalise", "generalize",
                    "extend"],
           "avoid": ["worked example", "let's start with the basics",
                     "as a beginner"]},
}

ANTI_CLICHE = ["great question", "good question", "let's dive in",
               "let's dive deeper", "let's dive", "dive into", "delve into",
               "let's go deeper", "go deeper", "look into",
               "let's understand", "let's see", "let us",
               "this might be happening",
               "no worries", "don't worry", "we'll come back to that",
               "as a beginner", "remember that", "in summary", "to recap",
               "hopefully"]


def run_case(label, expected_level, intervention_type, msg) -> None:
    print("\n" + "=" * 78)
    print(f"CASE: {label}   (expected level: {expected_level})")
    print("=" * 78)
    print(f"  message: {msg[:90]}{'...' if len(msg)>90 else ''}")

    d = LPDiagnostician(enable_rubric_grader=True)
    r = ConceptResolver()
    g = EnhancedPersonalizedGenerator()
    sd = {"question": msg}
    resolved = r.resolve(sd)
    print(f"  resolved: {[(c, round(s,2)) for c,s in resolved]}")

    multi = d.diagnose_multi(student_id="probe", question_text=msg,
                             resolved_concepts=resolved)
    print(f"\n  ── per-concept grader + diagnosis ──")
    for c, dg in multi["diagnostics"].items():
        rg = dg.get("rubric_grade") or {}
        print(f"    {c:24s}  focus={dg.get('is_focus'):<5}  "
              f"final={dg.get('current_lp_level')}  "
              f"grader={rg.get('level','?')}(conf {rg.get('confidence',0):.2f})  "
              f"diag_conf={dg.get('diagnostic_confidence',0):.2f}")

    focus_lvl = multi["focus"].get("current_lp_level", "L1")
    print(f"\n  focus_concept     : {multi['focus_concept']}")
    print(f"  focus level       : {focus_lvl}   (expected ~{expected_level})")
    print(f"  intervention type : {intervention_type}")

    # Build minimal student state with the chosen intervention
    student_state = {
        "student_id": "probe", "interaction_count": 1,
        "personality": {"openness":.6,"conscientiousness":.5,
                        "extraversion":.5,"agreeableness":.5,"neuroticism":.4},
        "knowledge_state": {"overall_mastery": 0.30 if focus_lvl=="L1" else
                                                (0.55 if focus_lvl=="L2" else 0.80),
                            "mastery_history": [0.30]},
        "psychological_graph": {},
        "progression_graph":   {"stage": {"L1":1,"L2":2,"L3":4,"L4":5}.get(focus_lvl,1),
                                "scaffold_level": {"L1":4,"L2":3,"L3":2,"L4":1}.get(focus_lvl,3)},
        "content_channel":     {"encoding_strength":
                                {"L1":"surface","L2":"partial","L3":"solid","L4":"deep"}.get(focus_lvl)},
        "language_channel":    {},
        "recommended_intervention": {"type": intervention_type,
                                     "rationale": f"level-appropriate for {focus_lvl}"},
        "lp_diagnostic":       multi["focus"],
        "lp_diagnostic_multi": multi,
    }
    analysis = {"emotion": "confused" if focus_lvl=="L1" else "engaged",
                "frustration_level": 0.4 if focus_lvl=="L1" else 0.1,
                "engagement_score": 0.6 if focus_lvl=="L1" else 0.9}

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

    low = reply.lower()
    # Anti-cliche
    cliche_hits = [c for c in ANTI_CLICHE if c in low]
    # Level-shape audit
    cues = LEVEL_AUDIT_CUES[focus_lvl]
    want_hits = [w for w in cues["want"] if w in low]
    avoid_hits = [w for w in cues["avoid"] if w in low]
    # Per-concept addressing
    focus_c = multi["focus_concept"]
    non_focus = [c for c in multi["diagnostics"] if c != focus_c]
    addressed = {c: (f"on {c}".lower() in low or
                     f"on '{c}'".lower() in low or
                     f"**{c}" in low or f"### {c}" in low)
                 for c in non_focus}

    print(f"\n  Anti-cliche audit       : "
          f"{'CLEAN' if not cliche_hits else 'HITS -> ' + str(cliche_hits)}")
    print(f"  {focus_lvl} shape cues present : {want_hits or 'NONE — wrong shape'}")
    if avoid_hits:
        print(f"  {focus_lvl} shape cues to AVOID present (bad): {avoid_hits}")
    for c, ok in addressed.items():
        print(f"  Mini-reply '{c}'         : "
              f"{'PRESENT' if ok else 'MISSING'}")


if __name__ == "__main__":
    for label, exp, intv, msg in CASES:
        run_case(label, exp, intv, msg)
