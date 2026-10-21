"""
Verify #4(a)+(b): does the grader now correctly grade L3 plain-words
mechanism reasoning and L4 generalisation, instead of pinning them at L2?
And does the new grader/ST-head precedence kick in when they disagree?

Runs the same 4 cases as before (L1, L2, L3 plain-words, L4 generalisation),
shows for each: keyword cls, grader, trained ST head probs (top-1), and
the FINAL current_lp_level after the new precedence rule.
"""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.orchestrator.lp_diagnostic import LPDiagnostician, classify_lp_level


CASES = [
    ("L1 symptom",      "L1",
     "why is == false, they look the same to me"),
    ("L2 rule only",    "L2",
     "I know I have to use .equals() instead of == for strings but I don't know why == fails"),
    ("L3 plain words",  "L3",
     "each new String() call makes its own object somewhere in memory, so "
     "== checks if those two memory spots are the same (they aren't), while "
     ".equals() walks the characters"),
    ("L4 generalising", "L4",
     "== is identity comparison for any reference type — for custom classes "
     "I'd override .equals() and hashCode() if I want content equality"),
]


def main():
    d = LPDiagnostician(enable_rubric_grader=True)
    print(f"{'CASE':<25} {'expect':<6} {'keyword':<8} {'grader':<10} {'ST head':<12} {'FINAL':<6} {'diag_conf':<10}")
    print("─" * 90)
    for label, expected, text in CASES:
        kw = classify_lp_level(text)["level"]
        diag = d.diagnose(student_id="probe", concept="string_equality",
                          question_text=text)
        rg = diag.rubric_grade or {}
        grader_lvl  = rg.get("level", "?")
        grader_conf = rg.get("confidence", 0)
        st_probs = diag.trained_lp_probs or {}
        if st_probs:
            st_top = max(st_probs, key=st_probs.get)
            st_str = f"{st_top}({st_probs[st_top]:.2f})"
        else:
            st_str = "—"
        verdict = "✓" if diag.current_lp_level == expected else "✗"
        print(f"{label:<25} {expected:<6} {kw:<8} "
              f"{grader_lvl}({grader_conf:.2f})  "
              f"{st_str:<12} {diag.current_lp_level:<6} "
              f"{diag.diagnostic_confidence:<10.2f} {verdict}")

    # Honest call: did any case still land short of expected?
    print()
    print("Compare to last run:")
    print("  L3 case BEFORE: grader=L2(0.80)  final=L2  ✗")
    print("  L4 case BEFORE: grader=L2(0.80)  final=L2  ✗")
    print("If L3 now=L3 or L4 now=L4 (or both), the fix is working.")


if __name__ == "__main__":
    main()
