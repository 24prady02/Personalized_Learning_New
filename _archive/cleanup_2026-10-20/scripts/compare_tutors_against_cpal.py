"""
Head-to-head LLM tutor comparison.

What this does
--------------
1. Picks N quiz items from CPAL's frontend bank (data/quiz_bank.json) — these
   are the actual prompts a CPAL student sees.
2. For each item, generates a plausible "random" student belief (the kind
   of free-text answer a real student would type into the CPAL Step-2
   textbox).
3. Runs the same (question + student belief) tuple through several LLM
   tutoring STRATEGIES, all using the same Ollama backbone (llama3.1:8b)
   so the variable being compared is the strategy, not the model:
     - CPAL                  (the LP-shape prompt from api/student_app.py)
     - Plain LLM             (no scaffolding, baseline)
     - Iris / Pyris-style    (Artemis programming-exercise tutor, no solutions)
     - CodeHelp-style        (Gen-Ed framework, "help don't solve")
     - CodeAid-style         (pseudocode-only assistant)
     - Ruffle&Riley-style    (two-agent learning-by-teaching, Riley voice)
     - CS50-Duck-style       (Socratic, refuses direct answers)
4. Saves all responses verbatim to JSON + a side-by-side comparison report.

Why reproductions and not live hosts?
-------------------------------------
The 5 comparison repos require OpenAI/Azure keys (or, for CS50 Duck, a
closed-source Harvard backend) and multi-hour infra setup. Reproducing
their *prompt strategy* against the same Ollama model gives an
apples-to-apples comparison of pedagogical approach.
"""
from __future__ import annotations
import json
import random
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List

import requests

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

MODEL    = "llama3.1:8b"   # reverted from qwen2.5:14b — qwen 2x slower
OLLAMA   = "http://localhost:11434/api/generate"
TIMEOUT  = 90


# ── student "random" beliefs — plausible misconception text per concept ────
RANDOM_BELIEFS: Dict[str, List[str]] = {
    "null_pointer": [
        "i think the code is broken because currentRoom is null and java doesnt know what to do",
        "the Room object was never made so it just crashes",
        "idk maybe its because the constructor isnt called",
    ],
    "type_mismatch": [
        "java reads left to right so it appends 5 as a string at the end",
        "the + operator works differently when one side is a string",
        "score becomes a string after + so 5 is added as text not a number",
    ],
    "infinite_loop": [
        "i forgot to increment i so the condition never changes",
        "the loop runs forever because nothing inside changes i",
        "you need i++ somewhere otherwise i stays 0",
    ],
    "string_equality": [
        "== works on int so it should work on strings too, must be a jvm bug",
        "i think both strings have the same chars but different addresses",
        "java compares the variable names a and b not the actual text",
    ],
    "assignment_vs_compare": [
        "the compiler doesnt like x = 0 because thats setting not comparing",
        "you should use == instead of = inside the if",
        "i thought = also compared things in java",
    ],
    "integer_division": [
        "both are ints so java throws away the decimal part",
        "i think int division rounds down because computers cant do decimals easily",
        "you need to cast one of them to double for it to actually divide",
    ],
}


# ── tutoring strategies (prompt templates) ────────────────────────────────

def cpal_prompt(item: Dict, belief: str) -> str:
    """CPAL's prompt (tightened 2026-05-30 — 3-4 sentence budget,
    matches api/student_app.py)."""
    correct = next(o for o in item["options"] if o.get("correct"))
    anti_cliche = (
        "STYLE: open with the diagnosis or example, never a preamble. Every "
        "sentence must either name a specific false belief, name a specific "
        "Java mechanism, show concrete code/trace, or ask a predict-this "
        "question. Banned phrases: \"great question\", \"let's dive\", "
        "\"let's break this down\", \"let's understand\", \"don't worry\", "
        "\"as a beginner\", \"hopefully\", \"in summary\", \"great job\"."
    )
    lp_shape = (
        "L2 — student knows the rule, not the mechanism. Acknowledge the rule "
        "in ONE phrase; name the operative mechanism step (compile-time vs "
        "runtime; heap vs stack vs reference; condition checked before/after "
        "iteration); end with a predict-this question on a small variant."
    )
    return (
        "You are a Java tutor for a first-year student. Respond in 3-4 short "
        "sentences — be disciplined and tight, every sentence must earn its "
        "place. Do NOT mention mastery, scores, levels, models, BKT, DINA, "
        "LP, or any internal metric. Address the student directly.\n\n"
        f"{anti_cliche}\n\n"
        f"Topic: {item['title']} ({item['concept']})\n\n"
        f"Code:\n{item['code']}\n\n"
        f"Question: {item['question']}\n"
        f"Correct option ({correct['key']}): {correct['text']}\n"
        f"Student wrote in their own words: \"{belief}\"\n\n"
        f"PEDAGOGICAL SHAPE for this turn:\n{lp_shape}\n\n"
        "Write the response now."
    )


# ── Fact-check pass (same scope as api/student_app._factcheck_mechanism_claims) ──
_FACTCHECK_PROMPT = """You are a Java expert reviewing a tutor's reply for ONE specific category of factual error.

ONLY flag a sentence if it makes ONE of these specific mistakes:
  A. Says something happens "at compile-time" when it actually happens at runtime
     (e.g. "Java creates new String objects on the heap at compile-time" - WRONG;
      the allocation happens at runtime).
  B. Says a loop condition is "checked at compile-time" or "initialized at compile-time"
     (loop conditions are evaluated at runtime, every iteration).
  C. Says a primitive int / boolean is stored "on the heap" (primitives in local
     variables and parameters live on the stack; only object fields live on the heap).
  D. Says == on String objects compares values / contents (== compares references).

Reply with a JSON object:
  {{"ok": true}}                                if no error of the above kinds
  {{"ok": false, "bad_sentences": ["<verbatim sentence to remove>", ...]}}

Do NOT flag anything outside the four categories above. Only output the JSON.

Tutor reply to review:
\"\"\"
{reply}
\"\"\"
"""


import re as _fc_re

_FACTCHECK_PATTERNS = [
    # A-fwd: "at compile-time" → runtime verb
    (_fc_re.compile(
        r"\bat compile[- ]time\b[^.!?]*\b("
        r"allocate[ds]?|create[ds]?|check[ds]?|initiali[sz]e[ds]?|"
        r"stor(?:e[ds]?|ing)|happen[ds]?|evaluate[ds]?|"
        r"hands? back|knows? (?:you'?re )?dividing|performs? an integer division"
        r")\b",
        _fc_re.IGNORECASE),
     "compile-time confused with runtime"),
    # A-rev: runtime verb → "at compile-time" ("checking references at compile-time")
    (_fc_re.compile(
        r"\b(check(?:s|ing|ed)?|evaluat(?:es|ing|ed)?|compar(?:es|ing|ed)?|"
        r"compute[ds]?|computing|resolv(?:es|ing|ed)?|"
        r"allocate[ds]?|allocating|caus(?:es|ed|ing)|"
        r"throw(?:s|ing|n)?|raise[ds]?|raising|"
        r"happen[s]?|happening|occur[s]?|occurring|"
        r"(?:integer )?division|"
        r"executes?|executing|run[s]?|running)\b[^.!?]*"
        r"\bat compile[- ]time\b",
        _fc_re.IGNORECASE),
     "runtime operation incorrectly placed at compile-time"),
    (_fc_re.compile(
        r"\bloop (?:condition|index|counter)[^.!?]*\bat compile[- ]time\b",
        _fc_re.IGNORECASE),
     "loop condition incorrectly said to be compile-time"),
    (_fc_re.compile(
        r"\b(?:primitive|local int|local boolean|local variable)\b[^.!?]*"
        r"\bstor(?:e[ds]?|ing)\b[^.!?]*\bon the heap\b",
        _fc_re.IGNORECASE),
     "primitive incorrectly said to be on the heap"),
    (_fc_re.compile(
        r"==[^.!?]*\bString[s]?\b[^.!?]*\bcompares? (?:contents?|values?)\b",
        _fc_re.IGNORECASE),
     "== said to compare contents on String"),
]


def factcheck(reply: str) -> Dict:
    """Deterministic regex fact-check (mirrors api/student_app.py).
    Strips sentences containing literal phrase-shapes known to be wrong.
    Zero false positives by construction."""
    if not reply or len(reply.split()) < 6:
        return {"cleaned": reply, "stripped_count": 0, "bad": []}
    try:
        sentences = _fc_re.split(r'(?<=[.!?])\s+', reply)
        clean = []
        stripped = []
        for s in sentences:
            hit = None
            for pat, label in _FACTCHECK_PATTERNS:
                if pat.search(s):
                    hit = label
                    break
            if hit:
                stripped.append((label := hit, s.strip()))
            else:
                clean.append(s)
        if not stripped:
            return {"cleaned": reply, "stripped_count": 0, "bad": []}
        cleaned = " ".join(clean).strip()
        # Don't gut the response — if stripping leaves less than 25 tokens,
        # the result is too short to teach anything. Better to keep the
        # original with the error flagged for downstream review than to
        # ship an uninformative response.
        if len(cleaned.split()) < 25:
            return {"cleaned": reply, "stripped_count": 0,
                     "bad": [],
                     "note": f"would_have_stripped_{len(stripped)}_but_too_short"}
        return {"cleaned": cleaned,
                "stripped_count": len(stripped),
                "bad": [s for _, s in stripped]}
    except Exception as e:
        print(f"  [factcheck] fell through: {e}")
        return {"cleaned": reply, "stripped_count": 0, "bad": []}


def plain_prompt(item: Dict, belief: str) -> str:
    """Baseline — no scaffolding, no rails. What you'd get from a naive call."""
    return (
        f"A student is learning Java and asked about this code:\n\n"
        f"{item['code']}\n\nQuestion: {item['question']}\n\n"
        f"Student's explanation: \"{belief}\"\n\n"
        f"Reply to the student."
    )


def iris_prompt(item: Dict, belief: str) -> str:
    """Iris / Pyris (Artemis) style — programming-exercise tutor with a
    no-direct-solutions guard and structured course context, modelled
    after the Iris programming-exercise pipeline."""
    return (
        "You are Iris, an AI tutor embedded in the Artemis learning platform. "
        "You support a first-year student on a programming exercise. You must "
        "NEVER reveal the solution code directly. Guide the student to the "
        "answer through hints, questions, and references to course concepts. "
        "If the student is on the wrong track, point at the relevant Java "
        "concept and ask a probing question — do not write the corrected code "
        "for them.\n\n"
        "Course context: Introductory Java — references, objects, primitives.\n\n"
        f"Exercise:\n{item['code']}\n\n"
        f"Question to the student: {item['question']}\n"
        f"Student's current explanation: \"{belief}\"\n\n"
        "Respond as Iris."
    )


def codehelp_prompt(item: Dict, belief: str) -> str:
    """Gen-Ed / CodeHelp style — explicit 'help, don't solve' framing the
    CodeHelp paper describes (Liffiton et al., SIGCSE)."""
    return (
        "You are CodeHelp, an assistant for a college CS course. You answer "
        "students' coding questions WITHOUT giving them the solution. You may "
        "explain concepts, point out where to look in their code, or rephrase "
        "the error, but you must NOT write the corrected code or directly "
        "name the bug fix.\n\n"
        f"Student's code:\n{item['code']}\n\nIssue: {item['question']}\n"
        f"Student wrote: \"{belief}\"\n\n"
        "Reply helpfully without revealing the answer."
    )


def codeaid_prompt(item: Dict, belief: str) -> str:
    """CodeAid style — pseudo-code only, no direct code solutions, supports
    follow-up questions, learner-rated responses (per the CHI '24 paper)."""
    return (
        "You are CodeAid, a programming tutor that helps students learn. You "
        "are allowed to give PSEUDOCODE but NEVER concrete Java code. Walk "
        "through the logic at a conceptual level. If the student needs to fix "
        "something, describe the steps in plain English or pseudocode — never "
        "show them the literal Java to type.\n\n"
        f"Code under discussion:\n{item['code']}\n\n"
        f"Problem the student is facing: {item['question']}\n"
        f"Student's hypothesis: \"{belief}\"\n\n"
        "Respond with pseudocode-level guidance."
    )


def ruffle_riley_prompt(item: Dict, belief: str) -> str:
    """Ruffle & Riley style — two-agent learning-by-teaching. The student
    is teaching Ruffle (an AI student); Riley (the professor agent) gently
    prompts. We simulate the Riley voice for one turn."""
    return (
        "You are Riley, a calm professor agent. Your colleague Ruffle is an "
        "AI student who is supposed to learn from the human user. Right now "
        "the human is explaining a Java concept to Ruffle. Your job is to "
        "gently nudge the conversation so that Ruffle ends up understanding "
        "the correct mechanism, by asking a single targeted follow-up "
        "question to the human user — not by lecturing. Use the "
        "expectation-misconception tailoring approach: identify what the "
        "human got right, what they got wrong, and ask ONE question that "
        "surfaces the gap.\n\n"
        f"Code Ruffle is looking at:\n{item['code']}\n\n"
        f"Question Ruffle has: {item['question']}\n"
        f"Human's explanation to Ruffle: \"{belief}\"\n\n"
        "As Riley, write one paragraph: acknowledge what the human said, "
        "name the gap, ask one targeted question."
    )


def cs50_duck_prompt(item: Dict, belief: str) -> str:
    """CS50 Duck style — Socratic, never gives the answer, channels rubber-
    duck-debugging energy. Modelled after CS50's public duck policy."""
    return (
        "You are the CS50 Duck, a rubber-duck debugger powered by ChatGPT. "
        "Your role is to help students think through their code by asking "
        "questions and reflecting their reasoning back to them. You NEVER "
        "give the answer directly. You NEVER write corrected code. You ask "
        "questions in the spirit of Socratic dialogue, like a thoughtful TA "
        "who wants the student to reach the conclusion themselves.\n\n"
        f"Student's code:\n{item['code']}\n\n"
        f"Student's question: {item['question']}\n"
        f"Student's current thinking: \"{belief}\"\n\n"
        "Reply as the CS50 Duck."
    )


STRATEGIES = {
    "CPAL":             cpal_prompt,
    "Plain LLM":        plain_prompt,
    "Iris/Pyris-style": iris_prompt,
    "CodeHelp-style":   codehelp_prompt,
    "CodeAid-style":    codeaid_prompt,
    "Ruffle&Riley":     ruffle_riley_prompt,
    "CS50 Duck-style":  cs50_duck_prompt,
}


# ── runner ──────────────────────────────────────────────────────────────────

def call_ollama(prompt: str) -> Dict:
    t0 = time.time()
    try:
        r = requests.post(OLLAMA,
                          json={"model": MODEL, "prompt": prompt, "stream": False},
                          timeout=TIMEOUT)
        r.raise_for_status()
        text = (r.json().get("response") or "").strip()
        return {"text": text, "tokens": len(text.split()),
                "latency_s": round(time.time() - t0, 2), "error": None}
    except Exception as e:
        return {"text": "", "tokens": 0,
                "latency_s": round(time.time() - t0, 2), "error": str(e)}


def main():
    random.seed(42)
    quiz = json.loads((ROOT / "data" / "quiz_bank.json").read_text(encoding="utf-8"))
    items_by_concept = {it["concept"]: it for it in quiz["items"]}
    # Pick 4 representative concepts (spread across LP signal types)
    chosen_concepts = ["null_pointer", "string_equality", "integer_division",
                       "infinite_loop"]

    scenarios = []
    for c in chosen_concepts:
        item = items_by_concept[c]
        belief = random.choice(RANDOM_BELIEFS[c])
        scenarios.append({"item": item, "belief": belief, "concept": c})

    results: List[Dict] = []
    out_dir = ROOT / "output" / f"tutor_comparison_{datetime.now().strftime('%Y-%m-%d_%H%M%S')}"
    out_dir.mkdir(parents=True, exist_ok=True)
    report: List[str] = []
    report.append(f"# Tutor strategy comparison — {datetime.now().isoformat(timespec='seconds')}")
    report.append(f"_Backbone model: `{MODEL}` (same model across all strategies — "
                   "the only variable is the prompt template.)_\n")
    report.append(f"**Strategies compared**: {len(STRATEGIES)}")
    report.append(f"**Scenarios**: {len(scenarios)}")
    report.append("")

    for sc in scenarios:
        item, belief, concept = sc["item"], sc["belief"], sc["concept"]
        print(f"\n=== Scenario: {concept} ===")
        print(f"Student wrote: {belief!r}")
        report.append(f"\n---\n\n## Scenario — concept: `{concept}`\n")
        report.append(f"**Quiz question**: {item['question']}\n")
        report.append(f"**Code**:\n```java\n{item['code']}\n```\n")
        report.append(f"**Random student belief** (typed in Step-2 box):\n"
                       f"> {belief}\n")

        scenario_results = {"concept": concept, "belief": belief,
                             "question": item["question"], "responses": {}}
        for strat_name, prompt_fn in STRATEGIES.items():
            print(f"  -> {strat_name} ...", end=" ", flush=True)
            prompt = prompt_fn(item, belief)
            resp = call_ollama(prompt)
            # Apply fact-check ONLY to CPAL — the other strategies don't
            # push the model into the compile-time/runtime/heap/stack
            # vocabulary, so the gate would have nothing to catch on them
            # and only adds latency.
            if strat_name == "CPAL" and not resp.get("error") and resp["text"]:
                fc = factcheck(resp["text"])
                resp["raw_text"] = resp["text"]
                resp["text"] = fc["cleaned"]
                resp["tokens"] = len(resp["text"].split())
                resp["factcheck_stripped"] = fc["stripped_count"]
                resp["factcheck_bad"] = fc["bad"]
            scenario_results["responses"][strat_name] = resp
            extra = ""
            if strat_name == "CPAL" and resp.get("factcheck_stripped"):
                extra = f"  [fact-check stripped {resp['factcheck_stripped']}]"
            print(f"{resp['tokens']} tok in {resp['latency_s']}s"
                   + (f"  [ERROR: {resp['error']}]" if resp['error'] else "")
                   + extra)
        results.append(scenario_results)

        report.append("### Responses\n")
        for strat_name, resp in scenario_results["responses"].items():
            report.append(f"**{strat_name}**  _({resp['tokens']} tok, "
                           f"{resp['latency_s']}s)_:\n")
            report.append("> " + (resp["text"] or "_(empty)_").replace("\n", "\n> "))
            report.append("")

    (out_dir / "results.json").write_text(
        json.dumps(results, indent=2, default=str, ensure_ascii=False),
        encoding="utf-8")
    (out_dir / "REPORT.md").write_text("\n".join(report), encoding="utf-8")
    print(f"\n[done] wrote {out_dir}")
    return out_dir


if __name__ == "__main__":
    main()
