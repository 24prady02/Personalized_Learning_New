"""
Does the system actually understand wrong mental models, or is it just
matching anything with score 1.00? Test it.

We feed 5 student inputs:
  1. Pure SE-A signal     ('content comparison' misconception)
  2. Pure SE-B signal     ('new() makes a copy' misconception)
  3. Pure SE-C signal     ('== and .equals are the same' misconception)
  4. Different concept    (null_pointer — must NOT match string_equality)
  5. Generic question     (no wrong-model signals — must return None)

For each input we print: matched id, belief, matched signal, score.
"""
import os, sys, json
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from src.knowledge_graph.mental_models import get_catalogue
from src.orchestrator.lp_diagnostic import LPDiagnostician


CATALOGUE_PATH = os.path.join(ROOT, "data", "mental_models",
                              "wrong_models_catalogue.json")
cat = get_catalogue(CATALOGUE_PATH)
diagnostician = LPDiagnostician(catalogue=cat)

# First print the ground truth: what does the catalogue SAY the three
# string_equality wrong models are?
with open(CATALOGUE_PATH, encoding="utf-8") as f:
    raw = json.load(f)
print("\n--- GROUND TRUTH (catalogue) for string_equality ---")
for wm in raw["concepts"]["string_equality"]["wrong_models"]:
    print(f"  [{wm['id']}] belief: {wm['wrong_belief'][:80]}")
    for s in wm["conversation_signals"]:
        print(f"       signal: \"{s}\"")

TESTS = [
    # (tag, concept, student_input, expected_wm_id)
    ("SE-A-pure",
     "string_equality",
     "Both strings look identical when I print them. The text is the same "
     "but == still returns false. Why?",
     "SE-A"),
    ("SE-B-pure",
     "string_equality",
     "I made two strings with the same text so they should be equal. "
     "I used new String() twice — new just copies the string right, so "
     "a copy is the same thing as the original.",
     "SE-B"),
    ("SE-C-pure",
     "string_equality",
     "Isn't .equals() just the longer way to write ==? They should do "
     "the same thing — what's the difference really?",
     "SE-C"),
    ("cross-concept (null_pointer input, we ask it to diagnose against string_equality)",
     "string_equality",
     "I get a NullPointerException when I call .length() on a variable "
     "that I declared but never assigned.",
     None),  # should NOT match string_equality models
    ("generic (no signals)",
     "string_equality",
     "Can you explain Java strings?",
     None),
]

print("\n--- DIAGNOSTIC RESULTS ---\n")
for tag, concept, text, expected in TESTS:
    diag = diagnostician.diagnose(
        student_id="t", concept=concept, question_text=text,
        stored_lp_level="L1", stored_lp_streak=0,
    ).to_dict()
    got = diag.get("wrong_model_id")
    sig = diag.get("matched_signal", "") or ""
    score = diag.get("match_score", 0) or 0
    belief = (diag.get("wrong_model_description") or "")[:70]
    ok = "PASS" if got == expected else "FAIL"
    print(f"[{ok}] {tag}")
    print(f"     input    : \"{text[:90]}...\"" if len(text) > 90
          else f"     input    : \"{text}\"")
    print(f"     expected : {expected}")
    print(f"     got      : {got}  (score={score:.2f})")
    if got:
        print(f"     belief   : {belief}")
        print(f"     signal   : \"{sig}\"")
    print()
