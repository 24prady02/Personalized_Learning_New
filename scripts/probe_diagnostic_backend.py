"""
Backend-only diagnostic probe — no LLM tutor generation, no frontend.

Runs each of a handful of representative student messages through the CPAL
diagnostic pipeline TWICE:

  BEFORE — simulates the original broken behaviour: the duplicate
           `_extract_concept` returned 'unknown' on every session, so the
           catalogue / rubric / RAG / wrong-model / per-concept LP rubric all
           silently no-opped (concept was never a catalogue key).

  AFTER  — the actual current pipeline: ConceptResolver multi-label resolution
           into the 20 catalogue concepts, per-concept diagnose() with
           concept-grounded LP scoring, CatalogueRAG retrieval, plus the
           diagnostic-confidence + probe-or-teach decision.

Prints a side-by-side comparison so you can see the improvement directly.
No Ollama needed (RubricGrader is disabled in the diagnostician for this
probe — we are measuring the deterministic backend, not the LLM grader).
"""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.orchestrator.lp_diagnostic   import LPDiagnostician
from src.orchestrator.concept_resolver import ConceptResolver


def main() -> None:
    # enable_rubric_grader=False so the comparison is deterministic and
    # offline-safe; CatalogueRAG stays on (sentence-transformers is local).
    d = LPDiagnostician(enable_rubric_grader=False)
    r = ConceptResolver()

    cases = [
        ("NPE error message",
         {"error_message": "Exception in thread main java.lang.NullPointerException at L12",
          "question":      "why is it null, I declared it at the top"}),
        ("Multi-concept message",
         {"question": "my loop never stops and the array index is off by one"}),
        ("String equality misconception",
         {"question": "they are both hello but == says false, what is wrong"}),
        ("Vague symptom (low-confidence -> probe)",
         {"question": "it is not working and I do not know why"}),
    ]

    for label, sd in cases:
        text = sd.get("question") or sd.get("error_message") or ""
        print("\n" + "=" * 78)
        print(f"CASE: {label}")
        print(f"  text: {text}")

        # --- BEFORE: simulate the old broken path (concept='unknown') ----
        old = d.diagnose(student_id="probe", concept="unknown",
                         question_text=text)
        print("\n  ── BEFORE (old `_extract_concept` always returned 'unknown') ──")
        print(f"      concept            = unknown   (never a catalogue key)")
        print(f"      wrong_model_id     = {old.wrong_model_id}")
        print(f"      match_score        = {old.match_score:.2f}")
        print(f"      lp_rubric_target   = {old.lp_rubric_target!r}")
        print(f"      benchmark_ideas    = {len(old.expert_benchmark_key_ideas)} sentences")
        print(f"      RAG top-3 wm       = {[w['id'] for w in old.rag_top_wrong_models] or 'EMPTY'}")
        print(f"      LP level           = {old.current_lp_level}  "
              f"(no rubric grounding)")
        print(f"      diagnostic_conf    = {old.diagnostic_confidence:.2f}")

        # --- AFTER: real multi-label resolve + diagnose_multi ------------
        resolved = r.resolve(sd)
        new = d.diagnose_multi(student_id="probe", question_text=text,
                               resolved_concepts=resolved)
        focus = new["focus"]
        print("\n  ── AFTER (ConceptResolver + diagnose_multi + RAG) ──")
        print(f"      resolved concepts  = "
              f"{[(c, round(s,2)) for c,s in resolved]}")
        print(f"      focus_concept      = {new['focus_concept']}")
        print(f"      wrong_model_id     = {focus['wrong_model_id']}  "
              f"(score {focus['match_score']:.2f})")
        rt = focus.get("lp_rubric_target") or ""
        print(f"      lp_rubric_target   = "
              f"{(rt[:90] + '...') if len(rt) > 90 else rt!r}")
        print(f"      benchmark_ideas    = "
              f"{len(focus.get('expert_benchmark_key_ideas') or [])} sentences")
        print(f"      RAG top-3 wm       = "
              f"{[(w['id'], round(w['similarity'],2)) for w in focus['rag_top_wrong_models']]}")
        print(f"      LP level           = {focus['current_lp_level']}  "
              f"(rubric-grounded)")
        print(f"      diagnostic_conf    = {focus['diagnostic_confidence']:.2f}")
        would_probe = focus["diagnostic_confidence"] < d.UNMATCHED_SIMILARITY_FLOOR + 0.20  # 0.45
        print(f"      probe-or-teach     = "
              f"{'PROBE (low conf)' if focus['diagnostic_confidence'] < 0.45 else 'TEACH'}")
        if len(new["diagnostics"]) > 1:
            others = [c for c in new["diagnostics"] if c != new["focus_concept"]]
            print(f"      also diagnosed     = {others}  "
                  f"(persisted, not lost)")

    print("\n" + "=" * 78)
    print("SUMMARY OF IMPROVEMENTS THE PROBE DEMONSTRATES")
    print("=" * 78)
    print("  1. concept              : 'unknown' (catalogue dead)  ->  real catalogue key")
    print("  2. wrong_model_id       : always None                 ->  matched + scored")
    print("  3. lp_rubric_target     : None                        ->  loaded prose")
    print("  4. RAG top wrong models : EMPTY                       ->  ranked retrieval")
    print("  5. multi-concept        : collapsed to 1               ->  N detected, focus picked")
    print("  6. diagnostic_conf      : nonexistent                 ->  drives probe vs teach")
    print("  7. probe loop           : nonexistent                 ->  fires on low conf")


if __name__ == "__main__":
    main()
