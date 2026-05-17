"""
One-shot demo: run the chat app's full prompt-construction pipeline for
SE-1 (string_equality) with the same student input we tested via the
tunnel, then send the resulting prompt to the Claude CLI (--print)
instead of Ollama. This isolates the generation model as the only
variable so the comparison is apples-to-apples.

NOT wired into the chat app permanently — invoked only when you want to
see what the same architecture produces with a stronger generator.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

QUIZ = {
    "id":             "SE-1",
    "concept":        "string_equality",
    "question":       "What does this print?",
    "code": (
        'String a = new String("hello");\n'
        'String b = new String("hello");\n'
        'System.out.println(a == b);'
    ),
    "options": {
        "A": "true — both strings contain 'hello'",
        "B": "false — they are different objects",
        "C": "Compile error",
        "D": "The word 'hello' prints twice",
    },
    "correct_answer": "B",
}

PICKED_LETTER = "A"
PICKED_TEXT   = QUIZ["options"]["A"]
STUDENT_REASONING = (
    "Both a and b are strings containing hello so == should return true "
    "because the contents match"
)
CORRECT = (PICKED_LETTER == QUIZ["correct_answer"])  # False

# The per-concept operative-step mapping the chat app uses to force the
# LLM to name the right Java mechanism in section 3.
OPERATIVE_STEP_FOR_SE = (
    "ADDRESS COMPARISON — == compares the two reference addresses, NOT the "
    "character content."
)


def _build_kg_context(reg, concept: str, code: str, error_message: str = "") -> str:
    """Same logic as cpal_chat_app._kg_context_block — duplicated here so
    the script is self-contained."""
    parts = []
    try:
        info = reg.pedagogical_kg.get_concept_full_info(concept) or {}
        ped = info.get("pedagogical_data") or {}
        misc = ped.get("common_misconceptions") or []
        if misc:
            names = [(m.get("description") or m.get("id") or "").strip()[:80]
                     for m in misc[:3]]
            names = [n for n in names if n]
            if names:
                parts.append("Pedagogical-KG misconceptions: "
                             + " | ".join(names))
        load = ped.get("cognitive_load") or {}
        if load:
            total = load.get("total")
            factors = load.get("factors") or []
            if total is not None or factors:
                parts.append(
                    f"Pedagogical-KG cognitive load: total={total}"
                    + (f"  factors={', '.join(factors[:4])}"
                       if factors else ""))
        dom = info.get("domain_knowledge") or {}
        rel = dom.get("related_concepts") or []
        if rel:
            short = []
            for r in rel[:4]:
                uri = r.get("concept", "") if isinstance(r, dict) else str(r)
                short.append(uri.rsplit("/", 1)[-1])
            parts.append("CSE-KG related concepts: " + ", ".join(short))
    except Exception as e:
        print(f"[ped_kg] {e}", file=sys.stderr)
    try:
        if code or error_message:
            related = reg.concept_retriever.retrieve_from_code(
                code or "", error_message or "", top_k=5) or []
            if related:
                parts.append("CSE-KG retrieved from code: "
                             + ", ".join(related[:5]))
    except Exception as e:
        print(f"[csekg] {e}", file=sys.stderr)
    if not parts:
        return ""
    return ("KG-GROUNDED CONTEXT (use to anchor your explanation; do "
            "not recite verbatim):\n  - " + "\n  - ".join(parts) + "\n\n")


def _build_prompt(reg) -> str:
    """Reconstruct exactly the prompt cpal_chat_app._stream_teach builds
    for SE-1 + the student input above. Pulls real values from the
    registry: DINA mastery, ST-WM-head + LP-rubric diagnosis, KG context."""

    # Step 1: update DINA + BKT so the mastery line reflects this turn.
    mastery = {}
    try:
        reg.dina.update("demo_claude", QUIZ["concept"], CORRECT)
        m = reg.dina.get_mastery("demo_claude", QUIZ["concept"]) or {}
        mastery["dina"] = float(m.get(QUIZ["concept"], 0.3))
    except Exception:
        mastery["dina"] = 0.3
    try:
        reg.bkt.update_knowledge("demo_claude", QUIZ["concept"], CORRECT)
        st = reg.bkt.get_student_knowledge_state("demo_claude") or {}
        mastery["bkt"] = float(st.get(QUIZ["concept"], mastery["dina"]))
    except Exception:
        mastery["bkt"] = mastery["dina"]

    # Step 2: run the real LP diagnostician on the student reasoning.
    diag = reg.lp_diagnostician.diagnose(
        student_id="demo_claude",
        concept=QUIZ["concept"],
        question_text=STUDENT_REASONING,
    ).to_dict()

    wm_id     = diag.get("wrong_model_id") or ""
    wm_desc   = diag.get("wrong_model_description") or ""
    wm_origin = diag.get("wrong_model_origin") or ""
    cur_lvl   = diag.get("current_lp_level", "L1")
    tgt_lvl   = diag.get("target_lp_level", "L3")
    benchmark = "; ".join(diag.get("expert_benchmark_key_ideas") or [])

    # Step 3: KG-grounded context block.
    kg_context = _build_kg_context(reg, QUIZ["concept"], QUIZ["code"])

    # Step 4: assemble the comprehensive prompt — this is the SAME text
    # cpal_chat_app builds; abbreviated rule sections elided here for
    # readability but the LLM gets the full one.
    wb_block = ""
    if wm_id and wm_desc:
        wb_block = (
            "MATCHED WRONG BELIEF (address THIS ONE, never the RAG "
            "candidates):\n"
            f"  id:     {wm_id}\n"
            f"  belief: {wm_desc}\n"
            f"  origin: {wm_origin}\n\n"
        )

    comprehensive_header = (
        "COMPREHENSIVE MODE — Learning Progression synthesis (NO multi-"
        "probe; this is the ONE teaching turn).\n"
        f"Student is at {cur_lvl}, target {tgt_lvl}.\n\n"
        f"STUDENT WROTE (verbatim, you must QUOTE FROM THIS in section 1 "
        f"and in the misconception section):\n  \"{STUDENT_REASONING}\"\n\n"
        f"{wb_block}"
        f"OPERATIVE MECHANISM (you MUST name this exact concept in "
        f"section 3, not just narrate around it):\n  "
        f"{OPERATIVE_STEP_FOR_SE}\n\n"
        "Produce a reply that EXPLICITLY walks the Learning Progression "
        "from L1 to L4 — SIX sections, in this exact order, with these "
        "exact friendly sub-headings (the student never sees L1/L2/L3/L4 "
        "labels but you must follow the progression):\n\n"
        "  ### What you noticed\n"
        "    (L1 — symptom layer) Confirm in ONE sentence what the "
        "program did or didn't do. QUOTE a phrase from the student's "
        "verbatim text above. Do NOT just say 'that's correct'; "
        "confirm-by-quoting.\n\n"
        "  ### The rule\n"
        "    (L2 — rule layer) State the Java rule in ONE plain sentence. "
        "No mechanism yet — the next section is for that.\n\n"
        "  ### What Java actually does, step by step\n"
        "    (L3 — mechanism layer, the CORE) NAME the operative "
        "mechanism above EXPLICITLY in the first sentence. Then walk "
        "through the execution at that step in 3-6 numbered lines, "
        "naming stack/heap/reference/address/compile-time/runtime as "
        "relevant. Include a small ASCII memory diagram (string_equality "
        "requires one). Anchor to the rubric's key ideas: "
        f"{benchmark}\n\n"
        "  ### Where else this shows up\n"
        "    (L4 — generalisation, REQUIRED). State the UNDERLYING "
        "PRINCIPLE in one sentence, then name ONE *structurally "
        "different* Java situation where the same operative mechanism "
        "fires. For string_equality, name `==` on Integer.valueOf(200) "
        "and the autoboxing identity cache, OR an analogous reference-"
        "type comparison — NOT another String == case.\n\n"
        "  ### The misconception we just untangled\n"
        "    QUOTE the student's exact imprecise phrase (it MUST be a "
        "contiguous substring of the student's verbatim text above) and "
        "contrast it with the corrected mechanism in ONE sentence each. "
        "Format: \"You wrote *'...'* — precise version: ...\". Do NOT "
        "paraphrase the student; quote them.\n\n"
        "  ### Predict this\n"
        "    ONE concrete predict-the-output question on a code variant "
        "that distinguishes a near-miss (e.g. a literal vs `new String` "
        "comparison, or an Integer.valueOf within vs outside the "
        "-128..127 cache).\n\n"
        "HARD RULES:\n"
        "  - All six sub-headings; skip ONLY the misconception section "
        "    if no wrong belief matched.\n"
        "  - L4 MUST be present and MUST be structurally different from "
        "    the case you just explained.\n"
        "  - L3 MUST name the OPERATIVE MECHANISM above explicitly.\n"
        "  - Misconception section MUST quote the student verbatim.\n"
        "  - No filler openers ('great question', 'let's dive in').\n\n"
    )

    mastery_line = (
        f"DINA mastery on '{QUIZ['concept']}': {mastery['dina']:.2f}  |  "
        f"BKT: {mastery['bkt']:.2f}\n\n"
    )

    tutor_input = (
        f"{comprehensive_header}"
        f"{kg_context}"
        f"{mastery_line}"
        f"Student was given this quiz:\n"
        f"Q: {QUIZ['question']}\n\n"
        f"Code:\n```java\n{QUIZ['code']}\n```\n\n"
        f"Options:\n" + "\n".join(
            f"  {k}. {v}" for k, v in QUIZ["options"].items()) +
        f"\n\nStudent picked {PICKED_LETTER}: {PICKED_TEXT}\n"
        f"Correct answer is {QUIZ['correct_answer']}: "
        f"{QUIZ['options'][QUIZ['correct_answer']]}\n"
        f"Student was {'CORRECT' if CORRECT else 'INCORRECT'}.\n\n"
        f"Student's accumulated reasoning across the chat:\n"
        f"{STUDENT_REASONING}\n"
    )

    return tutor_input, diag, mastery


def _call_claude(prompt: str) -> str:
    """Pipe the prompt to `claude --print` and capture stdout. Uses the
    same OAuth auth as the current Claude Code session — no API key
    required. We disable tools so the model just answers (no agentic
    side effects).

    On Windows the `claude` shim is a .ps1 wrapper, not an .exe — we
    invoke PowerShell explicitly so subprocess can find it.
    """
    # System prompt is omitted — the user prompt is fully self-contained
    # (COMPREHENSIVE MODE rules + KG context + mastery + quiz + student
    # input), so a separate system prompt would only add ambiguity. Tools
    # are disabled so Claude just answers without trying to read files.
    if os.name == "nt":
        cmd = [
            "powershell.exe",
            "-NoProfile",
            "-ExecutionPolicy", "Bypass",
            "-Command",
            "claude --print --tools \"\" --disable-slash-commands "
            "--model opus"
        ]
    else:
        cmd = [
            "claude", "--print",
            "--tools", "",
            "--disable-slash-commands",
            "--model", "opus",
        ]
    t0 = time.time()
    res = subprocess.run(
        cmd,
        input=prompt,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=300,
    )
    dt = time.time() - t0
    if res.returncode != 0:
        sys.stderr.write(f"[claude-cli stderr]\n{res.stderr}\n")
        raise RuntimeError(f"claude CLI exited {res.returncode}")
    return res.stdout, dt


def main():
    print("=" * 70)
    print("Loading CPAL registry...")
    print("=" * 70)
    from src.system_registry import get_registry
    reg = get_registry()

    print()
    print("=" * 70)
    print("Building prompt from real diagnostics (DINA + BKT + LP + KG)...")
    print("=" * 70)
    prompt, diag, mastery = _build_prompt(reg)
    print(f"  DINA mastery (after this turn): {mastery['dina']:.3f}")
    print(f"  BKT mastery (after this turn):  {mastery['bkt']:.3f}")
    print(f"  LP diagnosis: current={diag.get('current_lp_level')}  "
          f"target={diag.get('target_lp_level')}  "
          f"conf={diag.get('diagnostic_confidence', 0):.2f}")
    print(f"  Matched wrong-model: "
          f"{diag.get('wrong_model_id') or '(none)'} "
          f"via {diag.get('source')}")
    print(f"  Prompt length: {len(prompt)} chars")

    print()
    print("=" * 70)
    print("Sending to Claude CLI (model=opus)...")
    print("=" * 70)
    reply, dt = _call_claude(prompt)
    print(f"  Claude replied in {dt:.1f}s, {len(reply)} chars")

    print()
    print("=" * 70)
    print("CLAUDE TUTOR REPLY (same prompt that fed llama3.1:8b earlier)")
    print("=" * 70)
    print(reply)
    print("=" * 70)


if __name__ == "__main__":
    main()
