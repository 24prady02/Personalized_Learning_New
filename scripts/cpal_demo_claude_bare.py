"""
Counterfactual: Claude with NO chat-app architecture.

Same student input, same code, same wrong answer — but the prompt is
just "here's a quiz, here's the student's reply, respond as a tutor."
No LP diagnostic, no DINA mastery, no wrong-model identification, no
KG-grounded context, no operative-mechanism hint, no comprehensive-mode
rules, no rubric. Bare Claude.

Compare with cpal_demo_claude_once.py (Claude WITH the architecture)
to isolate exactly what the diagnostic stack adds.
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

# Bare prompt — only the things any tutor would naturally have:
# the question, the code, the options, what the student picked, and what
# the student wrote. NOTHING from the chat-app architecture (no LP level,
# no wrong-model id, no operative mechanism, no KG misconceptions, no
# DINA mastery, no formatting rules).
BARE_PROMPT = (
    "You are a Java tutor. A student answered the following quiz; "
    "please respond.\n\n"
    f"Question: {QUIZ_QUESTION}\n\n"
    "Code:\n"
    f"```java\n{QUIZ_CODE}\n```\n\n"
    "Options:\n"
    + "\n".join(f"  {k}. {v}" for k, v in QUIZ_OPTIONS.items())
    + f"\n\nStudent picked {PICKED_LETTER}.\n"
    f"Correct answer is {CORRECT_LETTER}.\n\n"
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
    print("BARE CLAUDE — no chat-app architecture, no diagnostic context")
    print("=" * 70)
    print(f"Prompt length: {len(BARE_PROMPT)} chars  "
          f"(architecture-enriched prompt was 4337 chars)")
    print()
    reply, dt = call_claude(BARE_PROMPT)
    print(f"Claude replied in {dt:.1f}s, {len(reply)} chars")
    print()
    print("=" * 70)
    print("CLAUDE TUTOR REPLY (no architecture)")
    print("=" * 70)
    print(reply)
    print("=" * 70)
