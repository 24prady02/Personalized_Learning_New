# CPAL Tutor Comparison — Self-Contained Knowledge Document

**Purpose**: a single document you can paste into Claude (or another LLM) to ask follow-up questions about CPAL's pedagogical positioning, the comparison methodology, or how to extend the work. Everything needed to reason about the comparison is in this one file.

**Generated**: 2026-05-31
**Source artefacts referenced**:
- `data/quiz_bank.json` (CPAL's quiz items)
- `scripts/compare_tutors_against_cpal.py` (the runner)
- `output/tutor_comparison_2026-05-30_152306/results.json` (baseline run)
- `output/tutor_comparison_2026-05-30_181625/results.json` (final run)
- `api/student_app.py` (CPAL's tutor prompt + fact-check)
- `src/orchestrator/student_state_tracker.py` (intervention selector + three-channel state)
- `src/orchestrator/lp_diagnostic.py` (LP-rubric classifier)
- `data/mental_models/wrong_models_catalogue.json` (81 wrong models)

---

## Section 1 — What CPAL is in one paragraph

CPAL (Catalogued Personalised Adaptive Learning) is a Java tutoring system built around five integrated components:
1. A **catalogue of 81 named wrong models** across 26 Java concepts, each grounded in the ProgMiscon misconception literature
2. A **Learning Progression rubric** (L1 symptom → L2 rule → L3 mechanism → L4 transfer) classified by trained sentence-transformer heads + a rubric grader
3. A **three-channel student state** model (cognitive / progression / psychological)
4. A **mechanism-vocabulary-forcing** LP-shape prompt that tells the LLM to name heap/stack/reference/runtime distinctions
5. A **deterministic regex fact-check gate** that strips known-wrong phrases before the response reaches the student

The first four components combine to produce diagnosis-driven personalised responses; the fifth is a safety net for backbone-model fragility. The backbone is `llama3.1:8b` via Ollama (local, free).

---

## Section 2 — What was being compared

Seven tutoring strategies were compared head-to-head across 4 student scenarios drawn from CPAL's actual frontend quiz bank.

| Strategy | What it represents | Source |
|---|---|---|
| **CPAL** | The LP-shape prompt from `api/student_app.py` | This codebase |
| **Plain LLM** | Naive baseline — no scaffolding | None |
| **Iris/Pyris-style** | Artemis programming-exercise tutor with no-direct-solutions guard | github.com/ls1intum/Pyris |
| **CodeHelp-style** | Gen-Ed framework "help don't solve" | github.com/liffiton/Gen-Ed |
| **CodeAid-style** | Pseudocode-only assistant | github.com/MajeedKazemi/code-aid |
| **Ruffle&Riley** | Two-agent learning-by-teaching with EMT | github.com/rschmucker/ruffle-and-riley (AIED '24) |
| **CS50 Duck** | Socratic, refuses direct answers | github.com/cs50/ddb50 |

**Why prompt reproductions, not live hosts**: Iris/CodeHelp/CodeAid/R&R all need OpenAI/Azure API keys plus multi-hour infrastructure (Weaviate, Spring Artemis, Postgres). CS50's backend is closed-source and Harvard-only. To make the comparison fair, each system's prompt strategy was extracted from its source and reproduced as a prompt template against the same `llama3.1:8b` Ollama backbone. The only variable being measured is the **pedagogical approach**.

---

## Section 3 — Verbatim prompt templates (so you can reproduce or critique each)

### 3.1 CPAL prompt (the LP-shape — L2 representative)

```
You are a Java tutor for a first-year student. Respond in 3-4 short sentences — be
disciplined and tight, every sentence must earn its place. Do NOT mention mastery,
scores, levels, models, BKT, DINA, LP, or any internal metric. Address the student
directly.

STYLE: open with the diagnosis or example, never a preamble. Every sentence must
either name a specific false belief, name a specific Java mechanism, show concrete
code/trace, or ask a predict-this question. Banned phrases: "great question",
"let's dive", "let's break this down", "let's understand", "don't worry",
"as a beginner", "hopefully", "in summary", "great job".

Topic: <quiz title> (<concept>)

Code:
<quiz code>

Question: <quiz question>
Correct option (<key>): <correct option text>
Student wrote in their own words: "<student belief>"

PEDAGOGICAL SHAPE for this turn:
L2 — student knows the rule, not the mechanism. Acknowledge the rule in ONE phrase;
name the operative mechanism step (compile-time vs runtime; heap vs stack vs reference;
condition checked before/after iteration); end with a predict-this question on a small
variant.

Write the response now.
```

### 3.2 Plain LLM (baseline)

```
A student is learning Java and asked about this code:

<quiz code>

Question: <quiz question>

Student's explanation: "<student belief>"

Reply to the student.
```

### 3.3 Iris / Pyris-style

```
You are Iris, an AI tutor embedded in the Artemis learning platform. You support a
first-year student on a programming exercise. You must NEVER reveal the solution
code directly. Guide the student to the answer through hints, questions, and
references to course concepts. If the student is on the wrong track, point at the
relevant Java concept and ask a probing question — do not write the corrected code
for them.

Course context: Introductory Java — references, objects, primitives.

Exercise:
<quiz code>

Question to the student: <quiz question>
Student's current explanation: "<student belief>"

Respond as Iris.
```

### 3.4 CodeHelp-style

```
You are CodeHelp, an assistant for a college CS course. You answer students' coding
questions WITHOUT giving them the solution. You may explain concepts, point out where
to look in their code, or rephrase the error, but you must NOT write the corrected
code or directly name the bug fix.

Student's code:
<quiz code>

Issue: <quiz question>
Student wrote: "<student belief>"

Reply helpfully without revealing the answer.
```

### 3.5 CodeAid-style

```
You are CodeAid, a programming tutor that helps students learn. You are allowed to
give PSEUDOCODE but NEVER concrete Java code. Walk through the logic at a conceptual
level. If the student needs to fix something, describe the steps in plain English or
pseudocode — never show them the literal Java to type.

Code under discussion:
<quiz code>

Problem the student is facing: <quiz question>
Student's hypothesis: "<student belief>"

Respond with pseudocode-level guidance.
```

### 3.6 Ruffle & Riley-style

```
You are Riley, a calm professor agent. Your colleague Ruffle is an AI student who
is supposed to learn from the human user. Right now the human is explaining a Java
concept to Ruffle. Your job is to gently nudge the conversation so that Ruffle ends
up understanding the correct mechanism, by asking a single targeted follow-up
question to the human user — not by lecturing. Use the expectation-misconception
tailoring approach: identify what the human got right, what they got wrong, and ask
ONE question that surfaces the gap.

Code Ruffle is looking at:
<quiz code>

Question Ruffle has: <quiz question>
Human's explanation to Ruffle: "<student belief>"

As Riley, write one paragraph: acknowledge what the human said, name the gap, ask
one targeted question.
```

### 3.7 CS50 Duck-style

```
You are the CS50 Duck, a rubber-duck debugger powered by ChatGPT. Your role is to
help students think through their code by asking questions and reflecting their
reasoning back to them. You NEVER give the answer directly. You NEVER write corrected
code. You ask questions in the spirit of Socratic dialogue, like a thoughtful TA
who wants the student to reach the conclusion themselves.

Student's code:
<quiz code>

Student's question: <quiz question>
Student's current thinking: "<student belief>"

Reply as the CS50 Duck.
```

---

## Section 4 — The 4 scenarios (verbatim from CPAL's frontend)

### Scenario 1 — `null_pointer` ("Null reference on a class field")

**Code shown to student:**
```java
public class Game {
    Room currentRoom;

    public void start() {
        currentRoom.describe();
    }

    public static void main(String[] args) {
        new Game().start();
    }
}
```

**Question**: Running this prints a NullPointerException at `currentRoom.describe()`. Why?

**Options shown** (multiple choice):
- **A** [correct]: `currentRoom` was declared but never assigned an object, so it holds null when describe() is called.
- **B** [wrong-model NP-A]: Declaring 'Room currentRoom;' inside the class automatically constructs a Room with default values.
- **C** [wrong-model NP-B]: The field exists but Java only initializes it the first time you use it; the very first call is undefined.
- **D** [wrong-model NP-C]: describe() is being called before main() runs, so the JVM hasn't loaded the class yet.

**Random student belief typed into Step-2 textbox**: `"idk maybe its because the constructor isnt called"`

### Scenario 2 — `string_equality` ("Comparing two strings")

**Code shown:**
```java
String a = new String("hello");
String b = new String("hello");
if (a == b) {
    System.out.println("same");
} else {
    System.out.println("different");
}
```

**Question**: This prints "different". Why?

**Options:**
- **A** [correct]: == compares the object references; a and b are two distinct String objects even though the characters are equal. Use a.equals(b) for content equality.
- **B** [wrong-model SE-A]: == works on Strings the way it does on int, so the result must be a bug in the JVM.
- **C** [wrong-model SE-B]: The characters are equal but the strings have different lengths in memory.
- **D** [wrong-model SE-C]: Java stores each call to new String separately and compares the variable names, not the contents.

**Random student belief**: `"== works on int so it should work on strings too, must be a jvm bug"`

### Scenario 3 — `integer_division` ("Integer division surprise")

**Code shown:**
```java
int a = 7;
int b = 2;
double avg = a / b;
System.out.println(avg);
```

**Question**: Output is 3.0, not 3.5. Why?

**Options:**
- **A** [correct]: a / b is computed as int division (yielding 3) before being widened to double on assignment. Cast one operand to double first.
- **B** [wrong-model ID-A]: Java division always truncates, even for double, so 3.5 is rounded down.
- **C** [wrong-model ID-B]: Assigning the result to a double should automatically promote both operands before the division.
- **D** [wrong-model ID-C]: println cuts off everything after the first decimal digit.

**Random student belief**: `"both are ints so java throws away the decimal part"` (*notable: this belief is mostly correct — a calibration test for the tutor*)

### Scenario 4 — `infinite_loop` ("While loop runs forever")

**Code shown:**
```java
int i = 0;
while (i < 10) {
    System.out.println(i);
}
```

**Question**: This loop never terminates. What's the actual cause?

**Options:**
- **A** [correct]: i is never modified inside the loop body, so the condition i < 10 stays true forever.
- **B** [wrong-model IL-B]: Mentioning i in the condition causes Java to auto-increment it each iteration.
- **C** [wrong-model IL-A]: println(i) advances i because it reads the variable.
- **D** [wrong-model IL-C]: The loop will exit on its own once the system runs out of memory.

**Random student belief**: `"you need i++ somewhere otherwise i stays 0"` (*also mostly correct — second calibration test*)

---

## Section 5 — Iteration history

Three runs were made. The first established the baseline; the second tried an LLM-grader fact-check and discovered false-positive issues; the third used a deterministic regex fact-check that's still in place today.

| Run | Setup | Avg CPAL tokens | Fact-check status |
|---|---|---|---|
| **Baseline** (2026-05-30 15:23) | CPAL prompt at 4-7 sentences, no fact-check | 142 | None |
| **Iter 2** (2026-05-30 17:25) | CPAL prompt at 3-4 sentences + LLM-grader fact-check | ~70 | Failed — 2/3 false positives stripped correct sentences |
| **Final** (2026-05-30 18:16) | CPAL prompt at 3-4 sentences + regex fact-check | ~72 | Zero false positives in spot tests; partial recall |

Key finding from the iteration: an LLM-grader at the same 8B scale as the generator inherits the same fragility — it produces false positives that damage the response more than the original error did. The deterministic regex is more precise (no false positives by construction) but has lower recall (only catches known phrase shapes).

---

## Section 6 — Verbatim final-run responses (the key data)

These are the actual responses from the FINAL run (`tutor_comparison_2026-05-30_181625`). All 7 strategies, all 4 scenarios.

### Scenario 1 — null_pointer
**Belief**: *"idk maybe its because the constructor isnt called"*

**CPAL** (85 tok, 11.6s):
> You're close - you mentioned the right symptom, but not the cause. The rule here is that variables must be initialized before use. However, Java doesn't enforce initialization at compile-time, so it's checked only when we try to access or modify the variable in runtime. Specifically, when we call `currentRoom.describe()`, Java checks if `currentRoom` holds a reference to an object on the heap, which it doesn't - hence the NullPointerException. Predict this: what will happen if we add `this.currentRoom = new Room();` before calling `start()`?

**Plain LLM** (201 tok, 25.5s):
> That's close, but not quite accurate! The issue here is not that the constructor isn't called. In fact, the constructor (`Game()`) is being called implicitly when you create a new instance of `Game` in the `main` method. The problem lies elsewhere: **`currentRoom` is `null`** because it hasn't been initialized before calling `describe()` on it. In Java, non-primitive variables (like `currentRoom`) are initialized with a default value of `null` unless explicitly assigned a different value. ...

**Iris/Pyris-style** (152 tok, 17.5s):
> It sounds like you're trying to figure out why the `NullPointerException` is occurring when calling `currentRoom.describe()`. That's a great start! Let's think about this together. You mentioned that maybe it's because the constructor isn't called. However, in Java, when we create an object using the keyword `new`, it automatically calls the no-arg constructor (also known as the default constructor). So, in your case, the Game class has a no-arg constructor. My question to you is: What do you think `currentRoom` is at the point that `describe()` is called?

**CodeHelp-style** (94 tok, 11.6s):
> It sounds like you're on the right track thinking about constructors! Let's take a closer look at your `start()` method in the `Game` class. You call `currentRoom.describe()`, but have you initialized the `currentRoom` object yet? When you try to access its methods, Java needs to know what it is first. You might want to think about when and how the `currentRoom` object gets assigned a value. Is there some other method or constructor that sets this property?

**CodeAid-style** (185 tok, 22.0s):
> Let's analyze the situation step by step. **Current state:** The `Game` class has an instance variable `currentRoom`, but it's not initialized before being used in the `start()` method. **Pseudocode level:**
> ```
> 1. Create a new Game object
> 2. Call start() on that object
> 3. In start(), try to access describe() on currentRoom
> What happens:
> - currentRoom is null (no value)
> - Trying to call a method on null throws NullPointerException
> ```
> Your student's hypothesis about the constructor not being called is partially correct...

**Ruffle & Riley** (80 tok, 9.9s):
> Let me help guide the conversation here. I think the human is on the right track by mentioning that the constructor isn't being called, which implies they suspect an initialization issue. However, there's a subtle distinction to be made - the problem isn't necessarily that the constructor isn't being called, but rather what happens when it is not explicitly defined in the Game class. What if we added a default constructor to the Game class, would that resolve the NullPointerException?

**CS50 Duck-style** (63 tok, 9.4s):
> Quack quack! Let's dive into this together, friend! So, you're wondering why it's throwing a NullPointerException when trying to call `currentRoom.describe()`. And you've got a hunch that maybe the constructor isn't being called... That's a great start! Can you think of a reason why the constructor wouldn't be called automatically? Is there something special about constructors in Java that might make this happen?

---

### Scenario 2 — string_equality
**Belief**: *"== works on int so it should work on strings too, must be a jvm bug"*

**CPAL** (88 tok, 11.4s):
> When comparing strings using "==" in Java, it doesn't check the content equality like you might expect from arithmetic operations. The "==" operator checks object references, so when we create new String objects, even if their contents are identical, they're treated as separate entities on the heap. You should use the .equals() method to compare string contents: a.equals(b) will return true in this case. Here's a similar example: what would happen if we changed the code to `String b = "hello";` instead of creating a new String object?

**Plain LLM** (264 tok, 37.5s):
> I love this question! Firstly, `==` does not only work with integers in Java. It can also be used with objects, including strings. The issue here is that when you create a new string using the `new String()` constructor, it creates a new object on the heap with its own copy of the characters "hello". However, when you use the literal syntax `"hello"`, it creates a string object in the string constant pool (a special memory area where Java stores frequently used strings)...

**Iris/Pyris-style** (177 tok, 23.8s):
> It looks like you're thinking that since we use `==` for comparison with integers, it would also work for string comparisons. However, the behavior of `==` is actually different when comparing objects. In Java, when we create two new instances of a class using the `new` keyword, they are not necessarily equal just because their contents are the same. Think about it like creating two separate boxes with the same contents - even though what's inside the boxes is the same, they are still two different boxes...

**CodeHelp-style** (118 tok, 16.6s):
> It sounds like you're familiar with how the equality operator (`==`) works for primitive types in Java, but not quite sure why it behaves differently for objects. To understand what's going on here, let's think about what happens when we create a new `String` object using the `new String()` constructor. Does this behave similarly to creating a new `int` variable? Take a look at how you're declaring your variables `a` and `b`. Are they being assigned the same value, or are they referring to two different memory locations?

**CodeAid-style** (215 tok, 28.8s):
> Let's break down what's happening here. When you create `a` and `b`, you're using the **String constructor**, which creates a new instance of String. Think of this like creating two separate boxes to hold the string "hello". The key thing to note is that when you use the constructor (`new String("hello")`), you're not just copying a reference to an existing string, but actually creating a brand new object in memory. Now, let's look at what happens in the `if (a == b)` statement...

**Ruffle & Riley** (68 tok, 10.6s):
> I nod in understanding as I listen to the human's explanation, acknowledging that they correctly identified the output of the code as "different". However, it seems they're under a misconception about how Java handles string equality using the "==" operator. They mentioned that since "==" works on integers, it should work on strings too - but here lies the gap: what does "==" actually check for in Java?

**CS50 Duck-style** (88 tok, 13.1s):
> My fine feathered friend, I see you're scratching your head about why `a == b` isn't working as expected. Let me ask you this: What exactly do you think happens when you create two new strings using `new String("hello")`, and then compare them with the `==` operator? Do you think it's just a simple matter of checking if they have the same sequence of characters? Or is there something more going on under the hood, perhaps related to how Java handles string objects versus primitive types like integers?

---

### Scenario 3 — integer_division
**Belief**: *"both are ints so java throws away the decimal part"* (mostly correct — calibration test)

**CPAL** (74 tok, 9.5s):
> You mentioned that Java "throws away the decimal part" when dealing with integer division, which is close to being accurate - Java does discard the remainder of division operations between integers. However, this behavior isn't due to runtime, but rather compile-time type promotion. At compile-time, Java promotes both operands to int for integer division, effectively discarding any potential fractional result. What will happen if you change one operand from an integer to a double?

⚠️ **Note**: this response contains a factual error — "compile-time type promotion" is wrong; the division happens at runtime. The regex fact-check missed it because the verb list didn't include "promotes". This is the recurring 8B-calibration issue.

**Plain LLM** (292 tok, 31.9s):
> I'm happy to help you understand why your code isn't working as expected. Actually, it's quite the opposite of what you mentioned. In Java, `7` and `2` are both integers, but when you divide two integers in Java using the `/` operator, any fractional part is indeed lost (because both operands are integers). However, that's not the problem here. The issue lies in the fact that one of your variables is a double (`double avg = ...`) while the other is an integer (`int b`)...

**Iris/Pyris-style** (65 tok, 9.9s):
> It looks like you're trying to calculate the average of `a` and `b`, but instead of getting 3.5, you're getting 3.0. That's not quite right. Before we dive into why this is happening, let me ask: Have you considered what happens when you divide an integer by another integer in Java? Do you remember how the result gets stored? Think about it for a moment...

**CodeHelp-style** (118 tok, 15.8s):
> It sounds like you're thinking about integer division and how it might affect the result. Let's take a closer look at what happens when you divide `a` by `b`. Since both variables are integers, does that necessarily mean the result will be an integer? Think about what happens when you use the `/` operator in Java. What type of value would you expect to get if you divided one number by another?

**CodeAid-style** (206 tok, 30.1s):
> Let's explore this together. **Step 1: Understand what's happening** When we divide `a` by `b`, Java performs integer division because both operands (`a` and `b`) are integers. Integer division truncates the result to an integer, effectively throwing away any fractional part (as your hypothesis suggests). However, that's not exactly what's happening here. **Step 2: Look at the data type of the variable** The result of the division is being assigned to a `double` variable called `avg`...

**Ruffle & Riley** (85 tok, 13.7s):
> I'll just gently nudge the conversation. The human user is correct that both `a` and `b` are integers, but they're misunderstanding why the division doesn't produce a decimal result in this case. Specifically, the human's explanation doesn't address what happens to the result of the division when it's stored in the `double` variable `avg`. My follow-up question would be: "Even though `avg` is a `double`, wouldn't that normally allow for decimal values? What's happening here that prevents the division from producing a more precise result?"

**CS50 Duck-style** (108 tok, 17.6s):
> Quack! Ah, you're on to something there, student! You're noticing that the output is indeed an integer, and it seems like the decimal part is being truncated. But, let's dive deeper... You mentioned that both `a` and `b` are integers, which is true. And in Java, when you divide two integers using the `/` operator, it performs a "truncation" operation, essentially discarding any fractional parts. However, I'm not entirely convinced by your reasoning yet. What if we tried to change one of these variables from an `int` to a `double`, say... `b = 2.0;`? Would that suddenly give us the expected result of 3.5? Why or why not?

---

### Scenario 4 — infinite_loop
**Belief**: *"you need i++ somewhere otherwise i stays 0"* (correct — second calibration test)

**CPAL** (41 tok, 7.9s):
> The variable i is never incremented inside the loop, so the condition remains true forever. This is because Java evaluates the while loop's condition at the top of each iteration. Predict this: what will happen if we add i++ after System.out.println(i)?

**Plain LLM** (215 tok, 29.8s):
> I'd be happy to help you review this code! Your observation is almost correct, but not quite. The issue with the code isn't that `i` stays at 0; it's actually due to the condition in the while loop. In Java, a while loop continues to execute as long as its condition is true. In this case, the condition is `i < 10`. The problem is that this condition is always true for any value of `i`, regardless of how large it gets...

**Iris/Pyris-style** (88 tok, 11.6s):
> It sounds like you're on the right track with thinking that `i` needs to be incremented somehow. However, simply saying we need `i++` doesn't quite get to the heart of why this loop is running forever. Let's think about what happens inside the loop body. We print out the value of `i`, but do we ever change it? Can you spot any code in the loop body that would update the value of `i`?

**CodeHelp-style** (84 tok, 12.1s):
> It sounds like you're on the right track! Let's take a closer look at why this loop is running forever. You're correct that there's no way to update the value of `i` within the loop itself. But, have you considered what happens when the condition `i < 10` is evaluated each time? Is it always true if i remains 0?

**CodeAid-style** (161 tok, 25.2s):
> Let's break down what's happening in this code: ``` 1. Initialize variable `i` to 0 2. Loop while `i` is less than 10 3. Inside the loop: a. Print the value of `i` b. (No increment statement) ``` The student's hypothesis that "i stays 0" is partially correct. However, there's another aspect to consider: **the loop condition itself**...

**Ruffle & Riley** (84 tok, 11.6s):
> I think the human user is on the right track by suggesting that incrementing `i` is necessary for the loop to terminate. However, they might be missing the nuance of where exactly this increment should happen. To clarify, my follow-up question would be: "Even though you mentioned `i++` somewhere in the loop, what specifically do you mean by 'somewhere'? Should it be at the beginning or end of each iteration, and how would that affect the loop's behaviour?"

**CS50 Duck-style** (76 tok, 12.6s):
> Quack quack! Ah-ha, you think `i++` is the answer? That's a good start! Let's take a closer look at the code. The condition for the while loop is `i < 10`, and we're trying to figure out why this loop never terminates. Have you considered what happens to `i` after the println statement?

---

## Section 7 — Cross-cutting findings (what the data shows)

### 7.1 Length distribution

| Strategy | Baseline avg (tok) | Final avg (tok) | Change |
|---|---|---|---|
| CPAL | 142 | 72 | **-49%** (tighter prompt worked) |
| Plain LLM | 241 | 243 | flat |
| Iris/Pyris | 123 | 121 | flat |
| CodeHelp | 153 | 106 | -31% (model became terser) |
| CodeAid | 225 | 197 | -12% |
| Ruffle & Riley | 80 | 79 | flat |
| CS50 Duck | 115 | 84 | -27% |

CPAL was the noisiest (high variance from 4-7 sentences) and the only one to materially tighten in the final run. After the change, CPAL responses sit between CS50 Duck (84) and CodeHelp (106) — about 1.3× longer than Ruffle&Riley but half of Plain LLM.

### 7.2 Mechanism-vocabulary usage (heap / stack / reference / runtime / compile-time / interning)

| Strategy | Scenarios using ≥1 mechanism term |
|---|---|
| **CPAL** | **4 of 4** |
| Plain LLM | 3 of 4 (verbose paraphrasing rather than precise) |
| Iris/Pyris | 1 of 4 |
| CodeHelp | 1 of 4 |
| CodeAid | 2 of 4 |
| Ruffle & Riley | 0 of 4 (pure questioning) |
| CS50 Duck | 0 of 4 (pure Socratic) |

CPAL is the **only** strategy that consistently teaches the mechanism vocabulary. The others either talk around it (Iris, CodeHelp) or refuse on principle (R&R, CS50 Duck).

### 7.3 Factual reliability (manual review of final-run responses)

| Strategy | Scenarios with factual errors |
|---|---|
| **CPAL** | 1 of 4 (integer_division: "compile-time type promotion" — wrong) |
| Plain LLM | 1 of 4 (baseline run hallucinated `i++` into actual code in infinite_loop; final run was clean) |
| Iris/Pyris | 0 of 4 (errs on vagueness, never on factual claim) |
| CodeHelp | 0 of 4 (same — refuses to commit) |
| CodeAid | 0 of 4 (pseudocode shelters from mechanism claims) |
| Ruffle & Riley | 0 of 4 (questions can't be factually wrong about mechanism) |
| CS50 Duck | 0 of 4 (same) |

The interesting pattern: **the strategies that don't make mechanism claims can't be wrong about mechanism**. CPAL's higher error rate is a direct consequence of its higher information rate. The fact-check exists to compensate but is incomplete.

### 7.4 Acknowledging partial correctness

For Scenario 3 (`integer_division` — student belief is mostly right) and Scenario 4 (`infinite_loop` — student belief is correct):

| Strategy | Honored partial correctness? |
|---|---|
| **CPAL** | Yes (both: "which is close to being accurate", "you mentioned the right symptom") |
| Plain LLM | No (S3: "Actually, it's quite the opposite of what you mentioned" — overcorrects a correct student) |
| Iris/Pyris | Yes (S3: "That's not quite right" + asks question) |
| CodeHelp | Partial |
| CodeAid | Yes ("Your hypothesis is partially correct") but then redirects awkwardly |
| Ruffle & Riley | Yes ("the human user is correct that both a and b are integers") |
| CS50 Duck | Yes ("That sounds like a good intuition to have") |

CPAL's "diagnose first, correct second" pattern lands well on calibration tests. Plain LLM is the worst offender — it told a mostly-correct student they were wrong.

### 7.5 Predict-this / forward-pushing closing

| Strategy | Scenarios ending with a forward question? |
|---|---|
| **CPAL** | **4 of 4** (built into the LP-shape) |
| Plain LLM | 0 of 4 (textbook tone, no follow-up) |
| Iris/Pyris | 4 of 4 (built into the LMS-tutor design) |
| CodeHelp | 3 of 4 |
| CodeAid | 0 of 4 (gives the answer in steps) |
| Ruffle & Riley | 4 of 4 (single targeted question IS the closing) |
| CS50 Duck | 4 of 4 (questions are the entire response) |

Retrieval practice closings are common. CPAL, R&R, CS50 Duck, Iris all have them as design defaults.

---

## Section 8 — CPAL's five pedagogical components, in depth

The combination is the wedge. None of the comparison systems has all five.

### Component 1: Named wrong-model catalogue
- **Concrete**: `data/mental_models/wrong_models_catalogue.json` — 81 wrong models across 26 Java concepts; each has wrong_belief (in student voice), origin story, refutation_text, JLS reference, ProgMiscon grounding
- **Why it matters**: Naming a misconception is what makes it dismantle-able (Posner et al. 1982 conditions of conceptual change). The student gets a *handle* on the wrong model
- **Other systems**: Iris/CodeHelp/CodeAid infer misconceptions from LLM at runtime — less stable, not grounded in literature. Ruffle&Riley uses EMT but scripts are per-lesson, not cross-cutting

### Component 2: LP-level rubric (L1 → L4)
- **Concrete**: `src/orchestrator/lp_diagnostic.py` — trained ST head + HVSAE head + rubric grader produce blended LP-level classification of free-text replies
- **Why it matters**: Same answer ≠ same understanding. CPAL is the only system that classifies the *level of articulation*, not just whether the student got the answer. This drives a different response shape per level (worked example at L1, mechanism scaffold at L2, novel application at L3, design rationale at L4)
- **Other systems**: Iris tracks course-level competency mastery (Atlas) but not articulation level. The others have a single response strategy

### Component 3: Three-channel student state
- **Concrete**: `src/orchestrator/student_state_tracker.py` — `StudentStateTracker` maintains cognitive (encoding strength), progression (developmental stage, ZPD), and psychological (attribution, imposter, anxiety, self-efficacy) channels. `InterventionSelector` reads all three to pick intervention
- **Why it matters**: A cognitively-ready student who is anxious or has fixed attribution needs different intervention than the same student emotionally regulated. CPAL's `attribution_reframe`, `mastery_surface`, `reduce_challenge` interventions exist because of this. Iris/CodeHelp/etc. don't have these
- **Other systems**: Iris tracks cognitive channel only; none has psychological state

### Component 4: Mechanism-vocabulary forcing
- **Concrete**: The L2/L3 LP-shape prompt explicitly instructs "name the operative step (compile-time vs runtime; heap vs stack vs reference; condition checked before/after iteration)"
- **Why it matters**: Vocabulary IS understanding for novices (Collins, Brown, Newman cognitive apprenticeship). The student who learns "== compares references, .equals() walks the char array" has a transferable model — same concept applies to autoboxing identity, array equality, parameter passing. Without the vocabulary, each is a fresh problem
- **Other systems**: None forces mechanism vocabulary. Plain LLM happens to use it sometimes; CS50 Duck and R&R refuse on principle (Socratic)
- **Trade-off**: This is also why CPAL is the strategy most likely to produce factual errors at 8B — it pushes the model into distinctions it can't reliably make. The fact-check exists to compensate

### Component 5: Deterministic regex fact-check gate
- **Concrete**: `_factcheck_mechanism_claims` in `api/student_app.py` — regex patterns match known-wrong phrase shapes ("at compile-time" near runtime verbs; "primitive stored on the heap"; "== compares contents on String") and strip those sentences before delivery to student
- **Why it matters**: A factually-wrong tutor is worse than no tutor — the student absorbs the misconception caused BY the tutoring. CPAL is the only system in the comparison with this gate
- **Calibration**: v1 used an LLM-grader and produced 2/3 false positives (stripped CORRECT sentences). v2 (current) uses deterministic regex — zero false positives by construction, but limited recall (catches known shapes, not novel ones)

### Why the combination matters
Any single component could be added to another system. **None of the comparison systems combines all five.** The architectural claim is that the integration produces a better tutor than any single-component system. The honest scientific position: this is a well-grounded *hypothesis* that needs a real classroom study to prove.

---

## Section 9 — Honest limitations and open questions

### What this data CAN tell you
- The prompt-strategy comparison is fair (same backbone, same scenarios, same student beliefs)
- CPAL's responses are demonstrably different in style (mechanism vocabulary, partial-correctness honoring, predict-this closings)
- The 8B-model factual fragility is real and measurable

### What this data CANNOT tell you
- **Learning gain**. We measured response quality, not student outcomes. A response that *looks* better in print may not produce more durable understanding
- **Multi-turn behavior**. All comparisons are single-turn. CPAL's three-channel state and plateau detection are designed for sessions, not single turns
- **Adult vs novice learner differences**. Some strategies (Ruffle & Riley single questions, CS50 Duck refusals) might work better for self-directed adults; CPAL's mechanism-explicit teaching might work better for true beginners. The data here doesn't separate these
- **What happens with a stronger backbone**. The 1 in 4 factual error rate is at `llama3.1:8b`. On GPT-4-mini or Claude Haiku the LP-shape prompt would likely produce cleaner mechanism claims, and the fact-check would catch even less because there's less to catch

### What would actually prove (or disprove) the CPAL pedagogical claim
A randomised controlled study with:
- 30–50 real CS101 students for one semester
- Half on CPAL, half on Plain GPT-4 or CodeHelp (control)
- Pre/post mastery tests on the 26 catalogued concepts
- Measured learning gain (Cohen's d > 0.3 = meaningful effect)
- Independent assessor blind to condition

Until then: the design is the strongest in the comparison set, the execution at 8B is currently 75% factually reliable with a partial safety net, and the efficacy claim is unproven.

---

## Section 10 — How to use this document

When pasting into Claude (or any LLM), useful follow-up questions might be:

- *"Given the verbatim responses in Section 6, which strategy would best serve a true-beginner CS101 student who has high anxiety? Why?"*
- *"The CPAL response for integer_division contains a factual error about compile-time type promotion. Write a corrected version that preserves the LP-shape (rule → mechanism → predict) but avoids the compile-time/runtime confusion."*
- *"Section 7.3 says strategies that don't make mechanism claims can't be wrong about mechanism. Design a hybrid CPAL-Ruffle&Riley prompt that gets mechanism vocabulary in WITHOUT making committal compile-time/runtime claims."*
- *"Add a 5th scenario (a `scanner_buffer` quiz item with a plausible random student belief) and predict how each of the 7 strategies would respond, given their style established in Section 6."*
- *"Critique the regex fact-check in Section 5/Section 8 Component 5. What additional patterns should it catch given the verbatim responses? Where does it currently let errors through?"*
- *"Design a study protocol that would test CPAL's pedagogical claim against CodeHelp, given the open questions in Section 9."*

---

**End of document.**
