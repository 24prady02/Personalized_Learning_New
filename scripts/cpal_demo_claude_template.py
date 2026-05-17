"""
Controlled ablation: same formatting template as the chat app, but with
every diagnostic fact stripped out. Isolates "what the format prompt
alone does" from "what the diagnostic stack adds."

Removed vs the chat-app's enriched prompt:
  - DINA + BKT mastery numbers
  - LP level current/target (no L1..L4 diagnosis)
  - MATCHED WRONG BELIEF block (no WM-ID, no belief text, no origin)
  - OPERATIVE MECHANISM hint (no "ADDRESS COMPARISON" naming from the
    chat-app's hand-curated _OPERATIVE_STEP table)
  - KG-grounded context (no pedagogical-KG misconceptions, no CSE-KG)
  - expert benchmark key-ideas line

Kept (all template-only — not architecture):
  - COMPREHENSIVE MODE header asking for the L1→L4 walk
  - The six section requirements
  - VERBATIM-QUOTE rule
  - ANTI-CIRCULARITY rule
  - ASCII-DIAGRAM rule
  - MECHANISM-ACCURACY rule
  - HARD RULES list

If template-only Claude produces an output comparable to enriched
Claude, the architecture's contribution is mostly the format. If
enriched Claude is materially better on diagnostic specificity (right
wrong-model named, right LP level targeted, right operative
mechanism), the architecture is doing real work.
"""
from __future__ import annotations

import os
import subprocess
import sys
import time

QUIZ_QUESTION = "What does this print?"
QUIZ_CODE = (
    'String a = new String("hello");\n'
    'String b = new String("hello");\n'
    'System.out.println(a == b);'
)
QUIZ_OPTIONS = {
    "A": "true — both strings contain 'hello'",
    "B": "false — they are different objects",
    "C": "Compile error",
    "D": "The word 'hello' prints twice",
}
PICKED_LETTER = "A"
CORRECT_LETTER = "B"
STUDENT_REASONING = (
    "Both a and b are strings containing hello so == should return true "
    "because the contents match"
)

TEMPLATE_ONLY_PROMPT = (
    "COMPREHENSIVE MODE — Learning Progression synthesis (NO multi-probe; "
    "this is the ONE teaching turn).\n\n"
    f"STUDENT WROTE (verbatim, you must QUOTE FROM THIS in section 1 and "
    f"in the misconception section):\n  \"{STUDENT_REASONING}\"\n\n"
    "Produce a reply that EXPLICITLY walks the Learning Progression from "
    "L1 to L4 — SIX sections, in this exact order, with these exact "
    "friendly sub-headings (the student never sees L1/L2/L3/L4 labels but "
    "you must follow the progression):\n\n"
    "  ### What you noticed\n"
    "    (L1 — symptom layer) Confirm in ONE sentence what the program "
    "did or didn't do. QUOTE a phrase from the student's verbatim text "
    "above.\n\n"
    "  ### The rule\n"
    "    (L2 — rule layer) State the Java rule in ONE plain sentence.\n\n"
    "  ### What Java actually does, step by step\n"
    "    (L3 — mechanism layer, the CORE). Name the operative Java "
    "mechanism explicitly in the first sentence. Walk through execution "
    "in 3-6 numbered lines naming stack/heap/reference/address/"
    "compile-time/runtime as relevant. Include a small ASCII memory "
    "diagram.\n\n"
    "  ### Where else this shows up\n"
    "    (L4 — generalisation, REQUIRED). State the UNDERLYING PRINCIPLE "
    "in one sentence, then name ONE *structurally different* Java "
    "situation where the same mechanism fires — NOT a paraphrase of the "
    "same case.\n\n"
    "  ### The misconception we just untangled\n"
    "    QUOTE the student's exact imprecise phrase from the verbatim "
    "text and contrast it with the corrected mechanism in ONE sentence "
    "each. Format: \"You wrote *'...'* — precise version: ...\".\n\n"
    "  ### Predict this\n"
    "    ONE concrete predict-the-output question on a code variant that "
    "distinguishes a near-miss.\n\n"
    "HARD RULES:\n"
    "  - All six sub-headings present.\n"
    "  - L4 MUST be structurally different from the case you just "
    "    explained.\n"
    "  - Misconception section MUST quote the student verbatim "
    "    (contiguous substring of the student's text above).\n"
    "  - No filler openers.\n\n"
    "VERBATIM-QUOTE RULE: text between *' and '* MUST be contiguous "
    "substring of the student's verbatim text. If no contiguous phrase "
    "fits, write: \"You didn't quite say this in so many words, but your "
    "answer treats X as if it were Y.\"\n\n"
    "MECHANISM-ACCURACY: never call a widening conversion a type "
    "mismatch. If the program compiles, no type mismatch exists.\n\n"
    "ASCII-DIAGRAM RULE: show DATA FLOW or MEMORY LAYOUT, not phase "
    "labels. compile-time/runtime are phases, not memory regions.\n\n"
    f"Student was given this quiz:\n"
    f"Q: {QUIZ_QUESTION}\n\n"
    f"Code:\n```java\n{QUIZ_CODE}\n```\n\n"
    f"Options:\n"
    + "\n".join(f"  {k}. {v}" for k, v in QUIZ_OPTIONS.items())
    + f"\n\nStudent picked {PICKED_LETTER}: {QUIZ_OPTIONS[PICKED_LETTER]}\n"
    f"Correct answer is {CORRECT_LETTER}: {QUIZ_OPTIONS[CORRECT_LETTER]}\n"
    f"Student was {'CORRECT' if PICKED_LETTER == CORRECT_LETTER else 'INCORRECT'}.\n\n"
    f"Student's reasoning:\n{STUDENT_REASONING}\n"
)


def call_claude(prompt: str) -> tuple[str, float]:
    if os.name == "nt":
        cmd = [
            "powershell.exe",
            "-NoProfile",
            "-ExecutionPolicy", "Bypass",
            "-Command",
            "claude --print --tools \"\" --disable-slash-commands "
            "--model opus",
        ]
    else:
        cmd = ["claude", "--print", "--tools", "",
               "--disable-slash-commands", "--model", "opus"]
    t0 = time.time()
    res = subprocess.run(cmd, input=prompt, capture_output=True,
                          text=True, encoding="utf-8", errors="replace",
                          timeout=300)
    dt = time.time() - t0
    if res.returncode != 0:
        sys.stderr.write(f"[claude-cli stderr]\n{res.stderr}\n")
        raise RuntimeError(f"claude exited {res.returncode}")
    return res.stdout, dt


if __name__ == "__main__":
    print("=" * 70)
    print("TEMPLATE-ONLY CLAUDE")
    print("  - Same 6-section format rules as the chat app")
    print("  - NO DINA, NO LP level, NO WM-ID, NO KG, NO operative-mechanism")
    print("=" * 70)
    print(f"Prompt length: {len(TEMPLATE_ONLY_PROMPT)} chars  "
          "(enriched was 4337, bare was 522)")
    print()
    reply, dt = call_claude(TEMPLATE_ONLY_PROMPT)
    print(f"Claude replied in {dt:.1f}s, {len(reply)} chars")
    print()
    print("=" * 70)
    print("CLAUDE TUTOR REPLY (template only, no architecture facts)")
    print("=" * 70)
    print(reply)
    print("=" * 70)
