# Tutor Strategy Comparison — CPAL vs. Open-Source LLM Tutors

**Generated**: 2026-05-30
**Backbone model**: `llama3.1:8b` via Ollama (same model across every strategy — the only variable is the prompt template)
**Quiz items**: drawn from CPAL's `data/quiz_bank.json` (what students actually see in the frontend)
**Strategies compared**: 7 (CPAL + 6 reproductions of open-source approaches)
**Total runs**: 28 (4 scenarios × 7 strategies)
**Raw outputs**: `output/tutor_comparison_2026-05-30_152306/results.json`

## Why reproductions, not live hosts?

Iris/Pyris, CodeHelp/Gen-Ed, CodeAid, and Ruffle&Riley all need OpenAI/Azure API keys plus multi-hour infra setup (Weaviate, Spring Artemis, Postgres, Lerna monorepos). CS50 Duck's backend (`cs50.ai`) is closed-source and Harvard-only. To make the comparison feasible and fair, I extracted each system's **prompt strategy** and ran it through the same Ollama backbone CPAL uses. The variable being measured is the **pedagogical approach**, not the model.

---

## Length / latency profile (averaged over 4 scenarios)

| Strategy | Avg tokens | Avg latency | Character |
|---|---|---|---|
| CPAL | 142 | 20s | LP-shape (rule + mechanism + walk + predict) |
| Plain LLM | 241 | 27s | Verbose, no rails |
| Iris / Pyris-style | 123 | 14s | LMS-flavoured, "refer to chapter X", probing questions |
| CodeHelp-style | 153 | 17s | "Let's take a closer look", non-revealing |
| CodeAid-style | 225 | 27s | Pseudocode-heavy, step-numbered |
| Ruffle & Riley | 80 | 10s | Single targeted question, shortest |
| CS50 Duck-style | 115 | 14s | "Quack" + Socratic prompt chain |

CPAL hits the middle of the length range and is the only strategy that consistently introduces *mechanism vocabulary* (heap, stack, reference, compile-time, runtime).

---

## Scenario 1 — `null_pointer`

**Quiz question**: Running this prints a NullPointerException at `currentRoom.describe()`. Why?
**Random student belief**: *"idk maybe its because the constructor isnt called"*

| Strategy | Verbatim opening | What it does right | What it gets wrong / weak |
|---|---|---|---|
| **CPAL** | "You're close on your explanation - it's indeed because currentRoom was declared but never assigned an object, so it holds null when describe() is called..." | Acknowledges partial correctness, introduces mechanism (heap, default-null, reference), shows what happens at runtime | Slightly verbose; mentions "reference is created on the heap" which is imprecise (the reference is on the stack/object field; the *object* would live on the heap if instantiated) |
| **Plain LLM** | "Actually, that's not entirely correct..." | Identifies null default initialization | Trails off into compile-time semantics that aren't needed; verbose |
| **Iris / Pyris** | "It seems like you're unsure about why it's throwing a NullPointerException. Let's break it down..." | Asks a probing question ("primitive or object reference?"), refers to "Section 2.3 in the course textbook" — the LMS-embedded feel | The fake section reference is hallucinated; could mislead |
| **CodeHelp** | "It seems like you're trying to get the game started... Have you considered where this currentRoom object is coming from?" | Refuses to reveal answer; pushes student to inspect their own code | Vague — "think about the lifetime" without naming the missing assignment |
| **CodeAid** | "**The Issue:** When you call currentRoom.describe(), it throws a NullPointerException..." | Step-structured (issue / pseudocode investigation / hypothesis verification) | Drops into Java-ish naming in violation of its own pseudocode-only rule |
| **Ruffle & Riley** | "Could you please clarify what the human means by 'the constructor isn't called'? Was the human expecting that the constructor would be responsible for initializing currentRoom?" | One targeted question — exactly the EMT pattern the R&R paper describes | Doesn't help the student forward in this single turn (by design — it's multi-turn) |
| **CS50 Duck** | "Quack quack! Ah, good question... Could it be related to how we're accessing the currentRoom field in the start() method?" | Pure Socratic — asks rather than tells | The duck persona ("Quack quack!") can read as patronising for adult learners |

---

## Scenario 2 — `string_equality`

**Quiz question**: This prints "different". Why?
**Random student belief**: *"== works on int so it should work on strings too, must be a jvm bug"*

| Strategy | Verbatim opening | What it does right | What it gets wrong / weak |
|---|---|---|---|
| **CPAL** | "You're trying to compare two strings using ==, but it's printing 'different'. That's because == compares object references, not content equality. The JVM sees a and b as two separate objects in memory..." | Names the mechanism (reference vs content), contrasts with literal interning, ends with a predict-this question about `new String("hello")` | Says "at compile-time, Java creates new String objects on the heap" — strictly speaking `new String()` allocates at runtime, not compile-time |
| **Plain LLM** | "Your intuition about == working with integers is correct, but unfortunately, this isn't a JVM bug..." | Clean technical write-up; cites memory allocation correctly | Doesn't follow up — feels like a textbook paragraph dumped at the student |
| **Iris / Pyris** | "It seems like you're assuming that == behaves similarly for all data types in Java, which is not quite correct..." | Precise: "specified by the language definition and is not a bug in the JVM" | Trails off mid-sentence at token cutoff |
| **CodeHelp** | "It sounds like you're trying to compare two String objects using the '==' operator. You're right that '==' does work for primitives like integers..." | Doesn't reveal the fix; asks the student to consult docs | Implicitly tells them the rule ("comparison is different for objects") — defeats own no-solution policy |
| **CodeAid** | "The student's hypothesis suggests they believe == works differently... let's visualize what happens when we compare..." | Highest-token response — walks through memory layout in detail | Spills into illustrative Java syntax — violates pseudocode-only constraint |
| **Ruffle & Riley** | "That makes sense that you think == should work similarly to integers, but can you explain why you think it's a JVM bug? What specifically about string objects leads you to believe that they should be equal when created with the same literal value?" | Shortest response by far — 54 tokens. Surfaces the metacognitive gap directly | Could leave a struggling student stuck if there's no second turn |
| **CS50 Duck** | "Quack! Ah, I see you're thinking that since == works for ints, it should work just as well for Strings... But before we consider a JVM bug, let's think about what exactly == is checking when applied to objects..." | Excellent Socratic redirect — "is it comparing contents or something else?" | Same duck-persona caveat |

---

## Scenario 3 — `integer_division`

**Quiz question**: Output is 3.0, not 3.5. Why?
**Random student belief**: *"both are ints so java throws away the decimal part"* (this belief is **mostly correct** — interesting test of the tutor's calibration)

| Strategy | Behavior | Notable |
|---|---|---|
| **CPAL** | Acknowledges student is "aware that integer division discards remainder", but pivots to *why* it rounds to 3 instead of 3.5. Names "compile-time" type resolution of `/` operator | One of the few that honors the partial correctness and pushes deeper rather than re-teaching |
| **Plain LLM** | **Factually wrong**: "it doesn't automatically perform integer division" — but Java DOES perform integer division when both operands are int | Pure hallucination |
| **Iris / Pyris** | Asks a leading question about primitive type storage | Concise, on-target |
| **CodeHelp** | Explains it as a "deliberate design choice" — adds floating-point precision rationale | Adds context the student didn't ask for |
| **CodeAid** | Step 1 (understand integer division) + Step 2 (assignment to avg) — pseudocode block | Structured but slow |
| **Ruffle & Riley** | "The statement 'java throws away the decimal part' oversimplifies the actual mechanism. Can you clarify whether Java's behavior is due to... or another aspect of integer division?" | Excellent EMT — names what student got right, points at the gap, asks one question |
| **CS50 Duck** | "What happens if we try to print out the value of `a / b` in an expression where it's not being assigned to anything?" | Beautiful Socratic redirect to the *expression* type rather than the assignment |

---

## Scenario 4 — `infinite_loop`

**Quiz question**: This loop never terminates. What's the actual cause?
**Random student belief**: *"you need i++ somewhere otherwise i stays 0"* (this belief is **correct**)

| Strategy | Behavior | Notable |
|---|---|---|
| **CPAL** | Acknowledges the correct part, then introduces runtime iteration semantics. **Factual error**: claims "loop condition i < 10 is checked at compile-time" — should be runtime per iteration | Mechanism vocab is right idea but mechanism *itself* is misstated |
| **Plain LLM** | **MAJOR FACTUAL ERROR**: claims "The statement that needs correction is: This loop never terminates" and "i is incremented inside the loop's condition". Both are wrong — the code does not have `i++` and the loop does run forever | Hallucinates `i++` into the actual code |
| **Iris / Pyris** | Asks about changing the variable type — slightly off-topic but probes thinking | Misdirected — type isn't the issue here |
| **CodeHelp** | "Where does i get updated inside the loop? Take another glance..." | Solid guided exploration without revealing the fix |
| **CodeAid** | Step-by-step pseudocode walk through the loop body — correctly identifies the missing update | Best technically accurate explanation of the four mid-length strategies |
| **Ruffle & Riley** | "If we were to place the i++ statement right after the println line... would that ensure the loop terminates?" | Perfect EMT pattern — confirms the student is right, then asks them to commit |
| **CS50 Duck** | "What value does i start with? And where does that value get updated?" | Socratic redirect that's slightly less effective here because the student already named the bug |

---

## Cross-cutting findings

### 1. Factual reliability on `llama3.1:8b`

Across 28 runs, **two strategies produced clear factual errors**:
- **Plain LLM** in `infinite_loop`: hallucinated that the code contained `i++` (it does not) and claimed the loop terminates (it doesn't)
- **CPAL** in `infinite_loop`: claimed loop condition is "checked at compile-time when the while loop is initialized" — wrong, it's checked every iteration at runtime
- **CPAL** in `string_equality`: said `new String()` allocates "at compile-time" — should be runtime

These are model-level errors, not strategy-level. The CPAL prompt *forces* the model to talk about compile-time vs runtime — but at 8B parameters the model sometimes gets the boundary wrong. The same prompt run against GPT-4 or llama3.3-70B would likely be cleaner.

### 2. Each strategy has a clear voice

The personas are all distinguishable from text alone:

- **CPAL**: rule → mechanism → walk → predict (LP-shape signature)
- **Plain LLM**: verbose, textbook tone, no follow-up
- **Iris/Pyris**: LMS-flavoured ("refer to chapter X"), probing question
- **CodeHelp**: "let's take a closer look", refuses to reveal
- **CodeAid**: pseudocode + step numbers (1, 2, 3)
- **Ruffle & Riley**: 50–90 tokens, single targeted question, EMT pattern
- **CS50 Duck**: "Quack!" + pure Socratic

### 3. Strategy-vs-belief calibration

The most interesting differentiator was Scenario 3 (`integer_division`) where the student's belief is **already mostly correct**. The strategies split:

- **Strategies that *honored* the correctness and pushed deeper**: CPAL, Ruffle & Riley, CS50 Duck
- **Strategies that *over-corrected* or re-taught from scratch**: Plain LLM, CodeAid
- **Strategies that *added orthogonal context***: CodeHelp (added design rationale), Iris (asked about type storage)

This matters: a tutor that ignores partial correctness damages student trust. CPAL's LP-shape inherently respects this because it operates on the diagnosed level, not a fixed template.

### 4. Length vs. depth trade-off

- **Ruffle & Riley (~80 tok)** is the most disciplined — refuses to spell out the answer, asks one perfect question. Good for adult/college learners who can self-direct.
- **Plain LLM (~241 tok)** burns tokens on textbook restatement without pushing the student to act.
- **CPAL (~142 tok)** lands in the middle — enough to introduce mechanism vocabulary, short enough to invite a reply.

### 5. CS50 Duck's persona has a cost

The "Quack quack!" opener appears in all four CS50 Duck responses. For middle-school or intro contexts this is fine; for adult CS101 learners it may read as patronising. The Socratic content underneath is consistently strong.

### 6. CodeAid's pseudocode rule leaks

CodeAid's prompt forbids concrete Java code but **drops into Java-ish syntax in 3 of 4 scenarios** (string_equality, integer_division, infinite_loop). At 8B-parameter scale, prompt rules of this granularity are not reliably followed.

---

## Where CPAL shows distinct value

The runs make a concrete case for CPAL's design even at the prompt-template level:

1. **Mechanism-vocabulary forcing** — CPAL is the only strategy whose responses consistently name "reference", "heap", "stack", "compile-time", "runtime", "interning". The LP-shape prompt template enforces this. Other strategies talk *around* mechanism in plain English.

2. **Diagnosis-then-teaching** — CPAL's prompt opens by acknowledging what the student got right before correcting. This pattern showed up in 3 of 4 CPAL responses; Plain LLM and Iris jumped straight to "actually that's not correct".

3. **Predict-this closing** — CPAL's L2 shape ends with a small variant question. This is the same teaching move Ruffle & Riley uses but built into a single-turn response, not a multi-agent flow.

The flip side: CPAL inherits the **factual fragility of llama3.1:8b**. Two of four runs had compile-time/runtime confusion. The other strategies didn't hit this because their prompts don't push the model into that vocabulary. **Recommendation**: gate the LP-shape's mechanism vocabulary on response review, or upgrade the backbone model — the prompt is more demanding than the small model can reliably honor.

---

## Where the other systems would beat CPAL

Honest assessment:

- **Iris/Pyris** — operational scale at university (Artemis: 2,400 concurrent students), Weaviate RAG over instructor materials, LTI integration. CPAL has none of this infrastructure.
- **Ruffle & Riley** — the cleanest "single perfect question" turn. CPAL responses are 1.8× longer on average.
- **CS50 Duck** — most rigorous "don't reveal the answer" policy. CPAL's anti-cliche prompt is good but does sometimes show the rule.
- **CodeHelp** — institutional auth + classroom enrollment + LMS integration baked into Gen-Ed. CPAL would need to add this.
- **CodeAid** — published CHI 2024 evaluation with deployment data. CPAL has internal harness PASS rates but no field deployment metrics yet.

---

## Sources

- [ls1intum/Pyris](https://github.com/ls1intum/Pyris)
- [ls1intum/Artemis](https://github.com/ls1intum/Artemis)
- [liffiton/Gen-Ed (CodeHelp)](https://github.com/liffiton/Gen-Ed)
- [MajeedKazemi/code-aid](https://github.com/MajeedKazemi/code-aid)
- [rschmucker/ruffle-and-riley](https://github.com/rschmucker/ruffle-and-riley)
- [cs50/ddb50](https://github.com/cs50/ddb50)
- Local artefacts: `scripts/compare_tutors_against_cpal.py`, `output/tutor_comparison_2026-05-30_152306/{results.json, REPORT.md}`

---

**End of report.**
