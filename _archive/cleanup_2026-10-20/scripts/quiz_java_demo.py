"""
Java MCQ quiz demo — same flow as scripts/cpal_quiz_simulation.py
but stripped to a single, clean scenario you can re-run any time.

Pipeline:
  1. Show Java code + MCQ options (correct option known).
  2. Student picks (wrong, on purpose).
  3. Ollama (qwen2.5-coder:7b) does ONE structured pass:
       (a) wrong-belief analysis     -- matched against the wrong_models
                                        catalogue entry for this concept
       (b) LP level classification   -- L1-L4 using the catalogue's rubric
                                        for THIS concept
       (c) intervention selection
       (d) corrected response        -- personalised to the wrong belief
                                        and LP level

All artifacts saved to output/quiz_java_run_<timestamp>/.
"""
import sys, os, json, time, re
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))
os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "3")

import requests


# ----- pick a concept from the wrong_models catalogue ----------------------
CATALOGUE_PATH = ROOT / "cpal_integration" / "data" / "wrong_models_catalogue.json"
CONCEPT = "integer_division"  # ID-B: type determined by result, not operands

# ----- the scenario --------------------------------------------------------
SCENARIO = {
    "id": "java_integer_division",
    "concept": CONCEPT,
    "language": "Java",
    "code": (
        'double result = 5 / 2;\n'
        'System.out.println(result);'
    ),
    "question": "What does this print?",
    "options": {
        "A": "2.5  -- five divided by two is two and a half",
        "B": "2.0  -- int/int returns int (2), then widened to double",
        "C": "2    -- just plain int division",
        "D": "Compile error -- mismatched types",
    },
    "correct_answer": "B",
    "student_pick": "A",
    "student_reasoning": (
        "I declared the result as a double, so Java should know to compute "
        "the division as a decimal. The destination type tells Java what "
        "kind of arithmetic to do -- since I asked for a double, I should "
        "get 2.5. The whole point of writing 'double' on the left is so the "
        "answer can hold the fractional part. Otherwise why would Java "
        "let me write that?"
    ),
}


# ----- prompt construction -------------------------------------------------
def build_diagnostic_prompt(scenario, concept_entry):
    wrong_models_block = "\n".join(
        f'  - {wm["id"]}: "{wm["wrong_belief"]}"  (origin: {wm["origin"]})'
        for wm in concept_entry["wrong_models"]
    )
    rubric = concept_entry["lp_rubric"]
    rubric_block = "\n".join(f"  {lvl}: {rubric[lvl]}" for lvl in ("L1", "L2", "L3", "L4"))

    s = scenario
    return f"""You are a Java pedagogy diagnostician. A CS1 student answered a multiple-choice question incorrectly. Diagnose their wrong mental model and learning-progression (LP) level using the catalogue + rubric below, then write a corrected, personalised response.

=== STUDENT'S QUIZ ATTEMPT ===
Concept: {s['concept']}
Question: {s['question']}
Code:
```java
{s['code']}
```
Options:
A. {s['options']['A']}
B. {s['options']['B']}
C. {s['options']['C']}
D. {s['options']['D']}

Correct answer: {s['correct_answer']}
Student picked: {s['student_pick']}  ({s['options'][s['student_pick']]})
Student reasoning: "{s['student_reasoning']}"

=== WRONG-MODELS CATALOGUE FOR THIS CONCEPT ===
You MUST pick the wrong_belief id from this list (or "none" if none fits):
{wrong_models_block}

=== LP RUBRIC FOR THIS CONCEPT ===
{rubric_block}

=== YOUR TASK -- TWO-PART OUTPUT ===

PART 1: a JSON object (and NOTHING else inside the JSON) with EXACTLY these keys:

{{
  "wrong_belief": {{
    "id": "<one of the catalogue ids above, e.g. SE-A>",
    "summary": "<one sentence naming the false rule the student is using>",
    "origin": "<copy from the catalogue entry>",
    "matched_signal": "<the exact phrase from the student's reasoning that proves it>",
    "confidence": <float 0..1>,
    "alternatives_rejected": [
      {{"id": "<other catalogue id>", "rejected_because": "<one sentence>"}}
    ]
  }},
  "lp_level": {{
    "current": "<L1|L2|L3|L4>",
    "target": "<one level above current, capped at L4>",
    "evidence": [
      "<bullet citing student text + the rubric clause it matches>",
      "<bullet 2>"
    ]
  }},
  "intervention": "<one of: worked_example, socratic_prompt, visual_analogy, trace_scaffold>"
}}

PART 2: the corrected response as plain prose, NOT inside the JSON, after a literal divider line.

The 400-700 word student-facing explanation MUST: (1) gently name and correct the wrong belief by quoting the student's own words, (2) trace what actually happens line by line, including any relevant ASCII diagram (memory layout, evaluation order, type promotion -- whatever fits the concept), (3) show the fix and contrast its trace with the wrong path, (4) end with a one-sentence transfer question that checks the corrected mental model. Tone: supportive, not condescending. Use Java -- not Python.

OUTPUT FORMAT (exactly this, no markdown fences):

<JSON object here>
===CORRECTED_RESPONSE===
<the 400-700 word prose here, including code blocks, ASCII diagrams, etc>
===END==="""


def call_ollama(prompt, model="qwen2.5-coder:7b",
                url="http://127.0.0.1:11434/api/generate"):
    t0 = time.time()
    chunks, first = [], None
    resp = requests.post(
        url,
        json={"model": model, "prompt": prompt, "stream": True,
              "options": {"temperature": 0.2}},
        timeout=600, stream=True,
    )
    resp.raise_for_status()
    for line in resp.iter_lines(decode_unicode=True):
        if not line:
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        piece = obj.get("response", "")
        if piece:
            if first is None:
                first = time.time() - t0
            chunks.append(piece)
        if obj.get("done"):
            break
    return "".join(chunks).strip(), {
        "ttft_s": first, "total_s": time.time() - t0,
        "model": model, "chunks": len(chunks),
    }


def extract_json(s):
    s = s.strip()
    s = re.sub(r"^```(?:json)?\s*", "", s)
    s = re.sub(r"\s*```$", "", s)
    start = s.find("{")
    if start == -1:
        raise ValueError("no JSON object found")
    depth, in_str, esc = 0, False, False
    for i in range(start, len(s)):
        c = s[i]
        if esc:
            esc = False
            continue
        if c == "\\":
            esc = True
            continue
        if c == '"':
            in_str = not in_str
            continue
        if in_str:
            continue
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return json.loads(s[start:i + 1])
    raise ValueError("unterminated JSON object")


def main():
    stamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    out_dir = ROOT / "output" / f"quiz_java_run_{stamp}"
    out_dir.mkdir(parents=True, exist_ok=True)
    print(f"[saver] writing artifacts to: {out_dir}")

    catalogue = json.loads(CATALOGUE_PATH.read_text(encoding="utf-8"))
    concept_entry = catalogue["concepts"][CONCEPT]

    print("=" * 72)
    print(f"JAVA QUIZ DEMO -- concept: {CONCEPT}")
    print("=" * 72)
    print("\n[1] Code:")
    for ln in SCENARIO["code"].splitlines():
        print(f"   {ln}")
    print(f"\n[2] Question: {SCENARIO['question']}")
    print("    Options:")
    for k, v in SCENARIO["options"].items():
        marker = " <- student" if k == SCENARIO["student_pick"] else \
                 " (correct) " if k == SCENARIO["correct_answer"] else ""
        print(f"      {k}. {v}{marker}")
    print(f"\n[3] Student reasoning:")
    print(f"    \"{SCENARIO['student_reasoning']}\"")

    prompt = build_diagnostic_prompt(SCENARIO, concept_entry)
    (out_dir / "prompt.txt").write_text(prompt, encoding="utf-8")
    print(f"\n[4] Sending diagnostic prompt to Ollama ({len(prompt)} chars) ...")

    raw, meta = call_ollama(prompt)
    print(f"    Ollama: model={meta['model']}  TTFT={meta['ttft_s']:.1f}s  "
          f"total={meta['total_s']:.1f}s  chunks={meta['chunks']}")

    (out_dir / "raw_response.txt").write_text(raw, encoding="utf-8")

    # Split the two-part output: JSON object, then divider, then prose
    divider = "===CORRECTED_RESPONSE==="
    if divider in raw:
        json_part, _, rest = raw.partition(divider)
        end_idx = rest.find("===END===")
        prose = rest[:end_idx].strip() if end_idx != -1 else rest.strip()
    else:
        json_part = raw
        prose = ""

    try:
        parsed = extract_json(json_part)
    except Exception as e:
        print(f"\n[!] Failed to parse JSON from model output: {e}")
        print("    Raw response saved to raw_response.txt")
        return

    parsed["corrected_response"] = prose
    (out_dir / "diagnosis.json").write_text(
        json.dumps(parsed, indent=2), encoding="utf-8"
    )

    print(f"\n[5] WRONG-BELIEF ANALYSIS")
    wb = parsed.get("wrong_belief", {})
    print(f"    id:         {wb.get('id')}")
    print(f"    summary:    {wb.get('summary')}")
    print(f"    origin:     {wb.get('origin')}")
    print(f"    matched:    \"{wb.get('matched_signal')}\"")
    print(f"    confidence: {wb.get('confidence')}")
    for alt in wb.get("alternatives_rejected", []):
        print(f"    rejected {alt.get('id')}: {alt.get('rejected_because')}")

    lp = parsed.get("lp_level", {})
    print(f"\n[6] LP LEVEL")
    print(f"    current: {lp.get('current')}")
    print(f"    target:  {lp.get('target')}")
    print(f"    evidence:")
    for e in lp.get("evidence", []):
        print(f"      - {e}")

    print(f"\n[7] INTERVENTION SELECTED: {parsed.get('intervention')}")

    print(f"\n[8] CORRECTED RESPONSE")
    print("-" * 72)
    print(parsed.get("corrected_response", ""))
    print("-" * 72)

    (out_dir / "corrected_response.md").write_text(
        parsed.get("corrected_response", ""), encoding="utf-8"
    )

    summary = {
        "scenario": SCENARIO,
        "catalogue_concept_entry": concept_entry,
        "ollama": meta,
        "diagnosis": parsed,
    }
    (out_dir / "full_run.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )

    print(f"\n[saver] DONE. Files:")
    for f in sorted(out_dir.iterdir()):
        print(f"   - {f.name}  ({f.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
