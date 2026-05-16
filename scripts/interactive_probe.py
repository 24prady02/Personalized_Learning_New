"""
Interactive backend probe — type any student message, see the FULL pipeline
react dynamically. No hardcoded scenarios; every decision is derived from
your input.

Usage:
    python scripts/interactive_probe.py
        (then type a student message at the prompt; Ctrl+D or 'quit' to exit)

What it shows per turn:
  1. Concepts resolved from your text (Tier 1 signatures + Tier 2 RAG)
  2. Per-concept rubric-grader verdict (LLM-graded against each concept's
     own L1-L4 rubric)
  3. Final LP level + diagnostic_confidence per concept
  4. Selected focus + LP-appropriate intervention type
  5. The actual generated tutor reply (qwen2.5-coder live)
  6. Audit: anti-cliche cleanness, mini-reply presence per non-focus concept

Nothing is hand-routed. Try anything — vague symptom, rule-knower,
mechanism-tracer, generaliser, off-topic, multi-concept — and see how the
focus / level / intervention / reply shape all change with your input.
"""
import sys, time
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.orchestrator.lp_diagnostic       import LPDiagnostician
from src.orchestrator.concept_resolver    import ConceptResolver
from src.orchestrator.enhanced_personalized_generator import EnhancedPersonalizedGenerator


# Intervention chosen by the focus concept's LP level — same mapping the
# orchestrator's Stage-2 LP-validity table would pick when nothing else
# overrides it (no psychological gate, no plateau, no probe).
INTV_BY_LEVEL = {
    "L1": "worked_example",    "L2": "trace_scaffold",
    "L3": "transfer_prompt",   "L4": "transfer_task",
}

ANTI_CLICHE = ["great question", "good question", "let's dive in",
               "let's dive deeper", "let's dive", "dive into", "delve into",
               "let's go deeper", "go deeper", "look into",
               "let's understand", "let's see", "let us",
               "this might be happening",
               "no worries", "don't worry", "we'll come back to that",
               "as a beginner", "remember that", "in summary", "to recap",
               "hopefully", "great job", "you're doing well",
               "doing a great job"]


def process_turn(d, r, g, msg, student_id="interactive"):
    sd = {"question": msg}
    resolved = r.resolve(sd)
    print(f"\n  resolved concepts : {[(c, round(s,2)) for c,s in resolved]}")

    multi = d.diagnose_multi(student_id=student_id, question_text=msg,
                             resolved_concepts=resolved)

    print(f"  per-concept diagnosis:")
    for c, dg in multi["diagnostics"].items():
        rg = dg.get("rubric_grade") or {}
        print(f"    {c:24s}  focus={dg.get('is_focus'):<5}  "
              f"lp={dg.get('current_lp_level')}->{dg.get('target_lp_level')}  "
              f"grader={rg.get('level','?')}({rg.get('confidence',0):.2f})  "
              f"diag_conf={dg.get('diagnostic_confidence',0):.2f}")

    focus_lvl = multi["focus"].get("current_lp_level", "L1")
    intervention_type = INTV_BY_LEVEL.get(focus_lvl, "worked_example")
    print(f"  focus_concept     : {multi['focus_concept']}  ({focus_lvl})")
    print(f"  intervention type : {intervention_type}  "
          f"(LP-validity-table pick for {focus_lvl})")

    student_state = {
        "student_id": student_id, "interaction_count": 1,
        "personality": {"openness":.5,"conscientiousness":.5,
                        "extraversion":.5,"agreeableness":.5,"neuroticism":.4},
        "knowledge_state": {"overall_mastery":
                            {"L1":0.30,"L2":0.55,"L3":0.75,"L4":0.85}[focus_lvl],
                            "mastery_history":[0.5]},
        "psychological_graph": {},
        "progression_graph":   {"stage": {"L1":1,"L2":2,"L3":4,"L4":5}[focus_lvl],
                                "scaffold_level": {"L1":4,"L2":3,"L3":2,"L4":1}[focus_lvl]},
        "content_channel":     {"encoding_strength":
                                {"L1":"surface","L2":"partial","L3":"solid","L4":"deep"}[focus_lvl]},
        "language_channel":    {},
        "recommended_intervention": {"type": intervention_type,
                                     "rationale": f"LP-{focus_lvl} appropriate"},
        "lp_diagnostic":       multi["focus"],
        "lp_diagnostic_multi": multi,
    }
    analysis = {"emotion": "confused" if focus_lvl=="L1" else "engaged",
                "frustration_level": 0.4 if focus_lvl=="L1" else 0.1,
                "engagement_score":  0.6 if focus_lvl=="L1" else 0.9}

    print(f"\n  ── generated tutor reply ──")
    t0 = time.time()
    reply = g.generate_personalized_response(
        student_id=student_id, student_message=msg,
        student_state=student_state, analysis=analysis,
    )
    dt = time.time() - t0
    for line in reply.splitlines():
        print(f"  | {line}")
    print(f"\n  (elapsed: {dt:.1f}s, {len(reply)} chars)")

    low = reply.lower()
    hits = [c for c in ANTI_CLICHE if c in low]
    focus_c = multi["focus_concept"]
    non_focus = [c for c in multi["diagnostics"] if c != focus_c]
    addressed = {c: any(p in low for p in [f"on {c}", f"on '{c}'",
                                            f"**{c}", f"### {c}"])
                 for c in non_focus}
    print(f"\n  Anti-cliche audit : "
          f"{'CLEAN' if not hits else 'HITS -> ' + str(hits)}")
    for c, ok in addressed.items():
        print(f"  Mini-reply '{c}'  : "
              f"{'PRESENT' if ok else 'MISSING'}")


def main():
    print("Initialising diagnostics (loads ST head + RAG + grader)...")
    d = LPDiagnostician(enable_rubric_grader=True)
    r = ConceptResolver()
    g = EnhancedPersonalizedGenerator()
    print(f"Ready. Grader model: {g._ollama_model}")
    print("Type a student message (or 'quit' / Ctrl+D to exit).\n")

    sid = "interactive"
    turn = 0
    while True:
        try:
            msg = input(f"student[{turn}]> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nbye"); break
        if not msg:
            continue
        if msg.lower() in ("quit", "exit", "q"):
            print("bye"); break
        print("=" * 78)
        process_turn(d, r, g, msg, student_id=sid)
        print("=" * 78)
        turn += 1


if __name__ == "__main__":
    main()
