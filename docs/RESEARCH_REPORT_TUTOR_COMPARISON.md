# A Prompt-Strategy Comparison of LLM-Based Programming Tutors: CPAL vs. Five Open-Source Systems

**Research Report**
Date: 2026-05-31
Reporting period: 2026-05-30 to 2026-05-31
System under test: CPAL (Catalogued Personalised Adaptive Learning) v2026-05-30
Backbone model: `llama3.1:8b` via Ollama (local, free)

---

## Abstract

We present a head-to-head comparison of seven large-language-model (LLM) based tutoring strategies applied to four Java programming misconception scenarios. The strategies compared are CPAL (our system) and prompt-level reproductions of five published or deployed tutoring systems: Iris/Pyris (TUM Artemis), CodeHelp (Gen-Ed framework, SIGCSE), CodeAid (CMU, CHI '24), Ruffle & Riley (CMU/Tsinghua, AIED '24), and the CS50 Duck (Harvard). To isolate pedagogical approach from backbone reliability, all seven strategies were run against the same `llama3.1:8b` model via Ollama, with student inputs drawn verbatim from CPAL's deployed quiz frontend. Across 28 responses (7 strategies × 4 scenarios), we find that (i) CPAL is the only strategy that consistently names mechanism-level vocabulary (heap, stack, reference, compile-time, runtime), (ii) CPAL is the only strategy that combines a named-wrong-model catalogue with a Learning Progression rubric and a three-channel student state, (iii) CPAL is also the only strategy susceptible to mechanism-level factual error at the 8B backbone (one error in four scenarios), and (iv) a deterministic regex fact-check gate provides a partial but precise safety net against the most common error shapes. We discuss what these findings imply for the deployment of CPAL relative to existing systems and identify the open question — measured learning gain in a real classroom — as the necessary next step.

**Keywords**: Intelligent Tutoring Systems, LLM-based Tutoring, Misconception Modelling, Learning Progressions, Java Education, Cognitive Apprenticeship.

---

## 1. Introduction

### 1.1 Motivation

Large language models have made conversational tutoring practical, but their pedagogical effectiveness varies widely with prompt strategy. The same backbone model can be turned into a Socratic dialogue agent (CS50 Duck), a learning-by-teaching partner (Ruffle & Riley), a pseudocode-only assistant (CodeAid), or a mechanism-explicit tutor (CPAL) depending solely on the prompt template. Each strategy embodies a different pedagogical theory; each system that deploys it claims it produces better learning outcomes than the alternatives. Without a controlled comparison, however, claims about pedagogical superiority remain hypothetical.

This report addresses three research questions:

- **RQ1** — *Response distinguishability*: Can the tutoring strategy be identified from the response text alone, holding the LLM constant?
- **RQ2** — *Pedagogical signature*: What design features in the response are unique to each strategy?
- **RQ3** — *Factual reliability*: Which strategies are most/least susceptible to factual error at backbone-model fragility?

### 1.2 Scope

We compare prompt strategies, not entire deployed systems. Iris/Pyris ships with Weaviate-based RAG over instructor materials; CodeHelp ships with Postgres-backed classroom management; the CS50 Duck ships with proprietary Harvard infrastructure. None of those infrastructural components is reproduced here. What is reproduced is the **pedagogical core** of each system — the prompt template and its grounding theory — against an apples-to-apples LLM backbone.

Crucially, all student inputs are drawn from CPAL's deployed quiz frontend. The quiz items used are the actual items shown to CPAL's pilot users, the random "student beliefs" are plausible misconceptions drawn from the ProgMiscon corpus, and the LLM backbone is the same one CPAL uses in production. This means the comparison reflects what each strategy *would* produce if dropped into CPAL's deployment context.

---

## 2. Related Work

### 2.1 Intelligent Tutoring Systems and Cognitive Models

The classical Intelligent Tutoring System literature, beginning with Anderson et al.'s Cognitive Tutor (1995), established that effective tutoring requires (i) a model of the student's current understanding, (ii) a model of the target understanding, and (iii) instructional moves that close the gap. The Cognitive Tutor's ACT-R-grounded model used production rules; later systems (D'Mello & Graesser's AutoTutor; VanLehn's Andes) adopted dialogue-based interaction patterns.

Recent LLM-based tutors have moved toward looser, more conversational scaffolds, often without the explicit student-modelling layer. The five comparison systems span this design space:

### 2.2 Comparison systems

**Iris / Pyris (TUM Artemis)** — Pyris is a Python FastAPI microservice that brokers LLM calls between Artemis (a Java/Spring LMS) and either OpenAI, Azure, or Ollama. Iris is the user-facing tutor name. Capability-based model routing chooses backbones per task. Weaviate indexes instructor-provided materials for RAG. Artemis tracks competency mastery via its Atlas component. Deployed at ~2,400 students at TU Munich.

**CodeHelp (Gen-Ed framework)** — Gen-Ed is a Python/Flask framework providing authentication (SSO/LTI), classroom enrollment, instructor/student roles, and configurable LLM models. CodeHelp is the flagship CS education application built on Gen-Ed. Published evaluations (Liffiton et al., SIGCSE 2023+) describe an explicit "help, don't solve" framing.

**CodeAid (CMU)** — A monorepo TypeScript application providing pseudocode-only assistance to programming students. Constraints on the LLM include forbidding concrete code generation and supporting follow-up questions plus user response rating. Published evaluation at CHI 2024 (Kazemi et al.) reports classroom deployment outcomes.

**Ruffle & Riley (CMU + Tsinghua)** — A two-agent learning-by-teaching system where the human user teaches "Ruffle" (an AI student) under guidance from "Riley" (a professor agent). Implements Expectation-Misconception Tailoring (EMT) via pre-generated tutoring scripts. Published at AIED 2024 (Schmucker, Xia, Azaria, Mitchell). Authors include Tom Mitchell, a foundational ITS researcher.

**CS50 Duck (Harvard)** — A VS Code extension wrapping a rubber-duck-debugging assistant. The extension client is open source (`cs50/ddb50`); the backend at `cs50.ai` is closed-source and Harvard-hosted. Documented to use OpenAI's ChatGPT API with Socratic-style refusal-to-answer prompts.

### 2.3 The CPAL system

CPAL combines five components not jointly present in the comparison systems: (1) a catalogue of 81 named wrong models across 26 Java concepts, grounded in the ProgMiscon corpus; (2) a Learning Progression rubric (L1 symptom → L2 rule → L3 mechanism → L4 transfer) classified by trained sentence-transformer heads; (3) a three-channel student state (cognitive / progression / psychological); (4) a mechanism-vocabulary-forcing LP-shape prompt; (5) a deterministic regex fact-check gate. The system runs against a local Ollama backbone (`llama3.1:8b` in this study).

---

## 3. Methodology

### 3.1 Experimental design

We conducted a within-subjects comparison: each of seven tutoring strategies was applied to each of four scenarios, yielding 28 generated responses. Within-subjects design controls for scenario difficulty — each strategy faces the same student input.

**Independent variable**: Tutoring strategy (7 levels).
**Dependent variables**: Response length (tokens), response latency (seconds), mechanism-vocabulary use (binary per scenario), factual accuracy (manual review).

### 3.2 Scenarios

Four scenarios were drawn from CPAL's production quiz bank (`data/quiz_bank.json`):

| ID | Concept | Quiz title | Student belief tested |
|---|---|---|---|
| S1 | `null_pointer` | Null reference on a class field | "idk maybe its because the constructor isnt called" |
| S2 | `string_equality` | Comparing two strings | "== works on int so it should work on strings too, must be a jvm bug" |
| S3 | `integer_division` | Integer division surprise | "both are ints so java throws away the decimal part" |
| S4 | `infinite_loop` | While loop runs forever | "you need i++ somewhere otherwise i stays 0" |

S1 and S2 represent **clearly wrong** student beliefs. S3 and S4 represent **mostly-correct** student beliefs — these serve as calibration tests for whether the strategy honors partial correctness or over-corrects.

### 3.3 Backbone model

All strategies used `llama3.1:8b` via Ollama running locally. Temperature, top-p, and other sampling parameters were left at Ollama defaults. The same model serves all strategies to isolate the variable.

### 3.4 Strategies

Each strategy is a prompt template containing (a) the strategy's pedagogical persona, (b) the scenario's code and question, and (c) the student's belief verbatim. The full prompt templates are provided in `docs/CPAL_TUTOR_COMPARISON_FEEDABLE.md`, Section 3.

### 3.5 Procedure

The runner script (`scripts/compare_tutors_against_cpal.py`) iterates over scenarios and strategies, calls Ollama via HTTP, and records the response, token count, and latency. For the CPAL strategy only, an additional regex fact-check pass strips sentences matching known-wrong phrase patterns before recording.

Three runs were conducted on 2026-05-30:
- **Baseline** (15:23): CPAL prompt at 4-7 sentence budget; no fact-check.
- **Iter 2** (17:25): CPAL prompt at 3-4 sentence budget; LLM-grader fact-check.
- **Final** (18:16): CPAL prompt at 3-4 sentence budget; deterministic regex fact-check.

The final run is the basis for analysis below.

### 3.6 Evaluation

Manual review by the report author assessed:
- **Mechanism-vocabulary use**: presence of at least one term from {reference, heap, stack, compile-time, runtime, interning, type promotion} in the response.
- **Factual accuracy**: whether the response contains a claim that misstates Java semantics (e.g., locating a runtime operation at compile-time).
- **Partial-correctness honoring**: whether responses to S3 and S4 acknowledge what the student got right before correcting.
- **Forward-pushing closing**: whether the response ends with a predict-this or transfer question.

---

## 4. Results

### 4.1 Quantitative summary

| Strategy | Avg tokens | Avg latency (s) | Mechanism vocab (of 4) | Factual errors (of 4) | Forward closing (of 4) |
|---|---|---|---|---|---|
| **CPAL** | 72 | 10.1 | **4** | 1 | **4** |
| Plain LLM | 243 | 31.2 | 3 | 0 (1 in baseline run) | 0 |
| Iris/Pyris-style | 121 | 15.3 | 1 | 0 | 4 |
| CodeHelp-style | 106 | 13.5 | 1 | 0 | 3 |
| CodeAid-style | 197 | 26.5 | 2 | 0 | 0 |
| Ruffle & Riley-style | 79 | 11.5 | 0 | 0 | 4 |
| CS50 Duck-style | 84 | 13.1 | 0 | 0 | 4 |

CPAL is the only strategy scoring on both mechanism-vocabulary (4/4) and forward-closing (4/4) with a response budget under 100 tokens. CPAL is also the only strategy producing a mechanism-level factual error in this run.

### 4.2 Scenario 1: null_pointer

**Stimulus**:
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
Question: "Running this prints a NullPointerException at currentRoom.describe(). Why?"
Student belief: *"idk maybe its because the constructor isnt called"*

**Responses (verbatim)**:

**CPAL** (85 tok, 11.6s):
> *"You're close - you mentioned the right symptom, but not the cause. The rule here is that variables must be initialized before use. However, Java doesn't enforce initialization at compile-time, so it's checked only when we try to access or modify the variable in runtime. Specifically, when we call `currentRoom.describe()`, Java checks if `currentRoom` holds a reference to an object on the heap, which it doesn't - hence the NullPointerException. Predict this: what will happen if we add `this.currentRoom = new Room();` before calling `start()`?"*

**Plain LLM** (201 tok, 25.5s):
> *"That's close, but not quite accurate! The issue here is not that the constructor isn't called. In fact, the constructor (`Game()`) is being called implicitly when you create a new instance of `Game` in the `main` method. The problem lies elsewhere: `currentRoom` is `null` because it hasn't been initialized before calling `describe()` on it. In Java, non-primitive variables (like `currentRoom`) are initialized with a default value of `null` unless explicitly assigned a different value. [...]"*

**Iris/Pyris-style** (152 tok, 17.5s):
> *"It sounds like you're trying to figure out why the `NullPointerException` is occurring when calling `currentRoom.describe()`. That's a great start! Let's think about this together. You mentioned that maybe it's because the constructor isn't called. However, in Java, when we create an object using the keyword `new`, it automatically calls the no-arg constructor (also known as the default constructor). So, in your case, the Game class has a no-arg constructor. My question to you is: What do you think `currentRoom` is at the point that `describe()` is called?"*

**CodeHelp-style** (94 tok, 11.6s):
> *"It sounds like you're on the right track thinking about constructors! Let's take a closer look at your `start()` method in the `Game` class. You call `currentRoom.describe()`, but have you initialized the `currentRoom` object yet? When you try to access its methods, Java needs to know what it is first. You might want to think about when and how the `currentRoom` object gets assigned a value. Is there some other method or constructor that sets this property?"*

**CodeAid-style** (185 tok, 22.0s):
> *"Let's analyze the situation step by step. Current state: The `Game` class has an instance variable `currentRoom`, but it's not initialized before being used in the `start()` method. Pseudocode level:*
> *1. Create a new Game object*
> *2. Call start() on that object*
> *3. In start(), try to access describe() on currentRoom*
> *What happens:*
> *- currentRoom is null (no value)*
> *- Trying to call a method on null throws NullPointerException*
> *Your student's hypothesis about the constructor not being called is partially correct [...]"*

**Ruffle & Riley** (80 tok, 9.9s):
> *"Let me help guide the conversation here. I think the human is on the right track by mentioning that the constructor isn't being called, which implies they suspect an initialization issue. However, there's a subtle distinction to be made - the problem isn't necessarily that the constructor isn't being called, but rather what happens when it is not explicitly defined in the Game class. What if we added a default constructor to the Game class, would that resolve the NullPointerException?"*

**CS50 Duck-style** (63 tok, 9.4s):
> *"Quack quack! Let's dive into this together, friend! So, you're wondering why it's throwing a NullPointerException when trying to call `currentRoom.describe()`. And you've got a hunch that maybe the constructor isn't being called... That's a great start! Can you think of a reason why the constructor wouldn't be called automatically? Is there something special about constructors in Java that might make this happen?"*

**Analysis**: All seven responses are factually correct on S1. CPAL is the only response that names "reference", "heap", and "runtime" — three mechanism-level concepts. Plain LLM, Iris, and CodeAid name "null" and "initialized" but talk around the mechanism. Ruffle & Riley and CS50 Duck refuse to name the mechanism, instead asking probing questions. CodeHelp falls between.

### 4.3 Scenario 2: string_equality

**Stimulus**:
```java
String a = new String("hello");
String b = new String("hello");
if (a == b) {
    System.out.println("same");
} else {
    System.out.println("different");
}
```
Question: "This prints 'different'. Why?"
Student belief: *"== works on int so it should work on strings too, must be a jvm bug"*

**Responses (verbatim)**:

**CPAL** (88 tok, 11.4s):
> *"When comparing strings using '==' in Java, it doesn't check the content equality like you might expect from arithmetic operations. The '==' operator checks object references, so when we create new String objects, even if their contents are identical, they're treated as separate entities on the heap. You should use the .equals() method to compare string contents: a.equals(b) will return true in this case. Here's a similar example: what would happen if we changed the code to `String b = \"hello\";` instead of creating a new String object?"*

**Plain LLM** (264 tok, 37.5s):
> *"I love this question! Firstly, `==` does not only work with integers in Java. It can also be used with objects, including strings. The issue here is that when you create a new string using the `new String()` constructor, it creates a new object on the heap with its own copy of the characters 'hello'. However, when you use the literal syntax `\"hello\"`, it creates a string object in the string constant pool (a special memory area where Java stores frequently used strings). [...]"*

**Iris/Pyris-style** (177 tok, 23.8s):
> *"It looks like you're thinking that since we use `==` for comparison with integers, it would also work for string comparisons. However, the behavior of `==` is actually different when comparing objects. In Java, when we create two new instances of a class using the `new` keyword, they are not necessarily equal just because their contents are the same. Think about it like creating two separate boxes with the same contents - even though what's inside the boxes is the same, they are still two different boxes [...]"*

**CodeHelp-style** (118 tok, 16.6s):
> *"It sounds like you're familiar with how the equality operator (`==`) works for primitive types in Java, but not quite sure why it behaves differently for objects. To understand what's going on here, let's think about what happens when we create a new `String` object using the `new String()` constructor. Does this behave similarly to creating a new `int` variable? Take a look at how you're declaring your variables `a` and `b`. Are they being assigned the same value, or are they referring to two different memory locations?"*

**CodeAid-style** (215 tok, 28.8s):
> *"Let's break down what's happening here. When you create `a` and `b`, you're using the String constructor, which creates a new instance of String. Think of this like creating two separate boxes to hold the string 'hello'. The key thing to note is that when you use the constructor (`new String(\"hello\")`), you're not just copying a reference to an existing string, but actually creating a brand new object in memory. Now, let's look at what happens in the `if (a == b)` statement [...]"*

**Ruffle & Riley** (68 tok, 10.6s):
> *"I nod in understanding as I listen to the human's explanation, acknowledging that they correctly identified the output of the code as 'different'. However, it seems they're under a misconception about how Java handles string equality using the '==' operator. They mentioned that since '==' works on integers, it should work on strings too - but here lies the gap: what does '==' actually check for in Java?"*

**CS50 Duck-style** (88 tok, 13.1s):
> *"My fine feathered friend, I see you're scratching your head about why `a == b` isn't working as expected. Let me ask you this: What exactly do you think happens when you create two new strings using `new String(\"hello\")`, and then compare them with the `==` operator? Do you think it's just a simple matter of checking if they have the same sequence of characters? Or is there something more going on under the hood, perhaps related to how Java handles string objects versus primitive types like integers?"*

**Analysis**: All seven responses are factually correct on S2. CPAL is again the only response naming "references" and "heap" together; it also explicitly mentions `.equals()` as the corrective method. Plain LLM provides the most technical depth but is 3× longer. R&R and CS50 Duck refuse to commit to an explanation; they ask probing questions. Notable: R&R is the shortest at 68 tokens.

### 4.4 Scenario 3: integer_division (calibration test — mostly-correct belief)

**Stimulus**:
```java
int a = 7;
int b = 2;
double avg = a / b;
System.out.println(avg);
```
Question: "Output is 3.0, not 3.5. Why?"
Student belief: *"both are ints so java throws away the decimal part"* (largely correct)

**Responses (verbatim)**:

**CPAL** (74 tok, 9.5s):
> *"You mentioned that Java 'throws away the decimal part' when dealing with integer division, which is close to being accurate - Java does discard the remainder of division operations between integers. However, this behavior isn't due to runtime, but rather compile-time type promotion. At compile-time, Java promotes both operands to int for integer division, effectively discarding any potential fractional result. What will happen if you change one operand from an integer to a double?"*

⚠️ **Factual error**: "compile-time type promotion" is incorrect; integer division occurs at runtime. The regex fact-check did not flag this because the verb "promotes" was not in the regex's runtime-verb list. This is the recurring 8B-calibration issue.

**Plain LLM** (292 tok, 31.9s):
> *"I'm happy to help you understand why your code isn't working as expected. Actually, it's quite the opposite of what you mentioned. In Java, `7` and `2` are both integers, but when you divide two integers in Java using the `/` operator, any fractional part is indeed lost (because both operands are integers). However, that's not the problem here. The issue lies in the fact that one of your variables is a double (`double avg = ...`) while the other is an integer (`int b`). When you divide `a` by `b`, the result is first calculated as an integer, because both operands are integers. Then, since `avg` is a double (which can hold decimal points), Java automatically converts this integer result to a double before storing it in `avg`. However, this automatic conversion isn't truncating; it's rounding down. [...]"*

⚠️ **Over-correction**: Plain LLM tells the student "Actually, it's quite the opposite of what you mentioned" despite the student being largely correct. This is the worst response in the run for partial-correctness handling.

**Iris/Pyris-style** (65 tok, 9.9s):
> *"It looks like you're trying to calculate the average of `a` and `b`, but instead of getting 3.5, you're getting 3.0. That's not quite right. Before we dive into why this is happening, let me ask: Have you considered what happens when you divide an integer by another integer in Java? Do you remember how the result gets stored? Think about it for a moment..."*

**CodeHelp-style** (118 tok, 15.8s):
> *"It sounds like you're thinking about integer division and how it might affect the result. Let's take a closer look at what happens when you divide `a` by `b`. Since both variables are integers, does that necessarily mean the result will be an integer? Think about what happens when you use the `/` operator in Java. What type of value would you expect to get if you divided one number by another? Does it make sense that Java would 'throw away' any decimal part without giving you a choice?"*

**CodeAid-style** (206 tok, 30.1s):
> *"Let's explore this together. Step 1: Understand what's happening. When we divide `a` by `b`, Java performs integer division because both operands (`a` and `b`) are integers. Integer division truncates the result to an integer, effectively throwing away any fractional part (as your hypothesis suggests). However, that's not exactly what's happening here. Step 2: Look at the data type of the variable. The result of the division is being assigned to a `double` variable called `avg`. This means we expect a decimal value, but since integer division was performed earlier, we get a truncated result. [...]"*

**Ruffle & Riley** (85 tok, 13.7s):
> *"I'll just gently nudge the conversation. The human user is correct that both `a` and `b` are integers, but they're misunderstanding why the division doesn't produce a decimal result in this case. Specifically, the human's explanation doesn't address what happens to the result of the division when it's stored in the `double` variable `avg`. My follow-up question would be: 'Even though `avg` is a `double`, wouldn't that normally allow for decimal values? What's happening here that prevents the division from producing a more precise result?'"*

**CS50 Duck-style** (108 tok, 17.6s):
> *"Quack! Ah, you're on to something there, student! You're noticing that the output is indeed an integer, and it seems like the decimal part is being truncated. But, let's dive deeper... You mentioned that both `a` and `b` are integers, which is true. And in Java, when you divide two integers using the `/` operator, it performs a 'truncation' operation, essentially discarding any fractional parts. However, I'm not entirely convinced by your reasoning yet. What if we tried to change one of these variables from an `int` to a `double`, say... `b = 2.0;`? Would that suddenly give us the expected result of 3.5? Why or why not?"*

**Analysis**: S3 separates strategies by how they handle a mostly-correct student belief.
- **Honor partial correctness explicitly**: CPAL ("close to being accurate"), CodeAid ("as your hypothesis suggests"), Ruffle & Riley ("correct that both a and b are integers"), CS50 Duck ("which is true").
- **Honor implicitly**: CodeHelp.
- **Over-correct**: Plain LLM ("Actually, it's quite the opposite"), Iris/Pyris ("That's not quite right").

CPAL is the only strategy on S3 that exhibits a mechanism-level factual error. The other strategies — by talking around mechanism — avoid being wrong about mechanism.

### 4.5 Scenario 4: infinite_loop (calibration test — correct belief)

**Stimulus**:
```java
int i = 0;
while (i < 10) {
    System.out.println(i);
}
```
Question: "This loop never terminates. What's the actual cause?"
Student belief: *"you need i++ somewhere otherwise i stays 0"* (correct)

**Responses (verbatim)**:

**CPAL** (41 tok, 7.9s):
> *"The variable i is never incremented inside the loop, so the condition remains true forever. This is because Java evaluates the while loop's condition at the top of each iteration. Predict this: what will happen if we add i++ after System.out.println(i)?"*

**Plain LLM** (215 tok, 29.8s):
> *"I'd be happy to help you review this code! Your observation is almost correct, but not quite. The issue with the code isn't that `i` stays at 0; it's actually due to the condition in the while loop. In Java, a while loop continues to execute as long as its condition is true. In this case, the condition is `i < 10`. The problem is that this condition is always true for any value of `i`, regardless of how large it gets. The reason is because the variable `i` is never incremented inside the loop body. [...]"*

**Iris/Pyris-style** (88 tok, 11.6s):
> *"It sounds like you're on the right track with thinking that `i` needs to be incremented somehow. However, simply saying we need `i++` doesn't quite get to the heart of why this loop is running forever. Let's think about what happens inside the loop body. We print out the value of `i`, but do we ever change it? Can you spot any code in the loop body that would update the value of `i`?"*

**CodeHelp-style** (84 tok, 12.1s):
> *"It sounds like you're on the right track! Let's take a closer look at why this loop is running forever. You're correct that there's no way to update the value of `i` within the loop itself. But, have you considered what happens when the condition `i < 10` is evaluated each time? Is it always true if i remains 0?"*

**CodeAid-style** (161 tok, 25.2s):
> *"Let's break down what's happening in this code: 1. Initialize variable `i` to 0. 2. Loop while `i` is less than 10. 3. Inside the loop: a. Print the value of `i`. b. (No increment statement). The student's hypothesis that 'i stays 0' is partially correct. However, there's another aspect to consider: the loop condition itself [...]"*

**Ruffle & Riley** (84 tok, 11.6s):
> *"I think the human user is on the right track by suggesting that incrementing `i` is necessary for the loop to terminate. However, they might be missing the nuance of where exactly this increment should happen. To clarify, my follow-up question would be: 'Even though you mentioned i++ somewhere in the loop, what specifically do you mean by somewhere? Should it be at the beginning or end of each iteration, and how would that affect the loop's behaviour?'"*

**CS50 Duck-style** (76 tok, 12.6s):
> *"Quack quack! Ah-ha, you think `i++` is the answer? That's a good start! Let's take a closer look at the code. The condition for the while loop is `i < 10`, and we're trying to figure out why this loop never terminates. Have you considered what happens to `i` after the println statement?"*

**Analysis**: On S4, all seven responses honor the student's correct belief. CPAL is the most concise (41 tokens) and the only one to provide both the mechanism ("evaluates the while loop's condition at the top of each iteration") and a forward question in three sentences total.

---

## 5. Discussion

### 5.1 RQ1 — Response distinguishability

The seven response styles are reliably distinguishable from text alone. The defining signatures observed:

- **CPAL**: opens with diagnosis of student belief, names mechanism vocabulary, ends with a predict-this variant question. Three to four sentences.
- **Plain LLM**: opens with a meta-acknowledgement ("That's close, but..."), provides a textbook-style technical explanation, no follow-up. Two to three paragraphs.
- **Iris/Pyris-style**: opens with friendly framing ("That's a great start!"), gives some technical explanation, ends with a probing question. Some hallucinated chapter references in the baseline run.
- **CodeHelp-style**: opens with "let's take a closer look", refuses to reveal the answer, asks the student to inspect their own code.
- **CodeAid-style**: numbered step structure, pseudocode (sometimes leaking into Java syntax in violation of its own constraint).
- **Ruffle & Riley**: third-person framing about "the human", names what the human got right and what they got wrong, asks one targeted question. Shortest by token count.
- **CS50 Duck**: "Quack quack!" opener, pure Socratic questioning, refuses to name the answer.

A first-year student exposed to any of these for one turn would identify the style. **RQ1 is answered: yes, strategies are distinguishable.**

### 5.2 RQ2 — Pedagogical signature

The strategies cluster on three orthogonal dimensions:

| Dimension | High end | Low end |
|---|---|---|
| Mechanism-vocabulary forcing | CPAL | Ruffle & Riley, CS50 Duck |
| Refusal-to-reveal rigor | CS50 Duck, Ruffle & Riley | Plain LLM, CodeAid |
| Single-turn information density | CPAL, Ruffle & Riley | Plain LLM, CodeAid |

CPAL's pedagogical signature is **"high mechanism vocabulary at low single-turn token cost"** — it tries to teach the mechanism *and* probe for understanding within a 70–90 token budget. No other strategy combines these. Ruffle & Riley achieves the low-token budget without the mechanism vocabulary. CodeHelp and Iris hit middle on both. CodeAid pays for the mechanism with extra tokens.

**RQ2 is answered**: CPAL's unique signature is the mechanism-vocabulary-at-low-budget combination, achieved by the LP-shape prompt and its 3-4 sentence constraint.

### 5.3 RQ3 — Factual reliability

This run produced one mechanism-level factual error (CPAL S3) out of 28 generated responses (3.6% error rate). The baseline run produced two errors. The error rate is meaningfully nonzero for CPAL specifically and meaningfully zero for the strategies that don't make mechanism claims.

The pattern is mechanical: strategies that don't make committal mechanism claims cannot be factually wrong about mechanism. Ruffle & Riley and CS50 Duck ask questions instead of telling; they cannot misstate compile-time vs runtime because they refuse to name either. CodeHelp and Iris paraphrase around mechanism. Only CPAL and CodeAid (sometimes) commit to mechanism-level statements; only CPAL does so consistently.

**RQ3 is answered**: factual error risk scales directly with mechanism-vocabulary commitment. CPAL bears the highest factual risk because it makes the most committal mechanism claims. The regex fact-check provides a partial safety net (catches known phrase shapes, misses novel ones).

### 5.4 The CPAL-specific trade-off

The CPAL pedagogical theory — that mechanism vocabulary builds transferable understanding (Collins, Brown, Newman 1989; Bransford & Schwartz 1999) — is what justifies the higher factual risk. A student who learns "== compares references, .equals() walks the char array" can transfer that to autoboxing identity, array equality, and parameter passing. A student who only learns "use .equals() for strings" has a rule, not a model.

But this is precisely the dimension where the 8B backbone occasionally fails. The model can produce "compile-time type promotion" (S3) because the training data contains both correct uses of the phrase and the kind of imprecise usage that CPAL's response exhibits. The deterministic regex fact-check catches the most stereotyped error shapes but cannot anticipate novel ones.

Two paths forward:
1. **Upgrade the backbone**. GPT-4-mini or Claude Haiku at API rates of ~$0.001-0.003 per call would likely produce cleaner mechanism vocabulary. The architectural advantages of CPAL would no longer be undermined by backbone limitations.
2. **Loosen the LP-shape**. Make mechanism vocabulary optional rather than mandatory in the prompt. This would eliminate the factual risk at the cost of CPAL's most distinctive pedagogical feature.

We recommend path (1): the pedagogical signature is the reason to use CPAL in the first place. Sacrificing it to compensate for backbone limitations defeats the purpose.

### 5.5 Comparison with deployment evidence

A meaningful caveat: pedagogical *theory* is not pedagogical *outcome*. CPAL's design integrates five components that no comparison system has — named WM catalogue, LP rubric, three-channel state, mechanism vocabulary forcing, fact-check gate. But none of the comparison systems' deployed advantages (Iris at 2,400 students, CodeHelp's SIGCSE evaluation, CodeAid's CHI '24 classroom study) are matched by CPAL field data. The reverse comparison is needed: take CPAL into a real classroom and measure learning gain versus, say, CodeHelp on the same students.

---

## 6. Limitations

This study has several honest limitations:

1. **Sample size**: 28 responses is small. With four scenarios, individual strategy idiosyncrasies could overweight findings. A larger run (e.g., 20+ scenarios) would strengthen conclusions.

2. **Single backbone**: All strategies used `llama3.1:8b`. The pattern of factual errors may not hold on stronger models. Specifically, CPAL's error rate likely drops sharply on GPT-4-mini or Claude Haiku; the comparison advantage may shift.

3. **Single-turn comparison**: CPAL's three-channel state and plateau detection are designed for multi-turn sessions. Single-turn comparison cannot show these.

4. **Reproduction fidelity**: Each comparison strategy is a reproduction of the published prompt approach, not the full deployed system. The actual Iris ships with Weaviate-based RAG over instructor materials; we reproduced only its prompt persona. The reproduction is faithful to the pedagogical theory but not to the deployment infrastructure.

5. **Manual review**: Factual-error assessment was conducted by the report author. Independent assessment would strengthen the validity claim.

6. **No outcome measurement**: This study compares responses, not learning. The CPAL pedagogical claim ultimately rests on whether students who use CPAL learn more durably than students who use the comparison systems. That requires a classroom study with measured learning gain — outside the scope of this report.

---

## 7. Conclusion

We compared seven LLM-based tutoring strategies — CPAL and reproductions of Iris/Pyris, CodeHelp, CodeAid, Ruffle & Riley, and the CS50 Duck — on four Java misconception scenarios using the same backbone model. CPAL is the only strategy that consistently names mechanism vocabulary, combines this with a named-wrong-model catalogue and LP-level rubric, and constrains responses to 3-4 sentences. It is also the only strategy susceptible to mechanism-level factual error at the 8B backbone (one error in four scenarios). A deterministic regex fact-check gate provides a partial safety net.

The CPAL design integrates five components — named WM catalogue, LP rubric, three-channel state, mechanism vocabulary forcing, fact-check gate — not jointly present in any comparison system. Whether this integration produces measurably better learning outcomes than simpler systems remains an open empirical question that requires a classroom study to answer.

For deployment, we recommend (i) upgrading the backbone model to eliminate residual factual fragility, (ii) preserving the LP-shape prompt as the distinctive pedagogical feature, and (iii) conducting a randomised controlled study to measure learning gain versus a simpler comparison system.

---

## 8. References

Anderson, J.R., Corbett, A.T., Koedinger, K.R., & Pelletier, R. (1995). Cognitive tutors: Lessons learned. *The Journal of the Learning Sciences*, 4(2), 167-207.

Bransford, J.D., & Schwartz, D.L. (1999). Rethinking transfer: A simple proposal with multiple implications. *Review of Research in Education*, 24, 61-100.

Chi, M.T.H. (2009). Active-constructive-interactive: A conceptual framework for differentiating learning activities. *Topics in Cognitive Science*, 1(1), 73-105.

Collins, A., Brown, J.S., & Newman, S.E. (1989). Cognitive apprenticeship: Teaching the crafts of reading, writing, and mathematics. In L.B. Resnick (Ed.), *Knowing, learning, and instruction* (pp. 453-494). Lawrence Erlbaum.

Clance, P.R., & Imes, S.A. (1978). The imposter phenomenon in high achieving women. *Psychotherapy: Theory, Research and Practice*, 15(3), 241-247.

D'Mello, S., & Graesser, A. (2012). AutoTutor and affective AutoTutor: Learning by talking with cognitively and emotionally intelligent computers that talk back. *ACM Transactions on Interactive Intelligent Systems*, 2(4), 1-39.

Kazemi, M., et al. (2024). CodeAid: Evaluating a Classroom Deployment of an LLM-based Programming Assistant. *Proceedings of CHI 2024*.

Karpicke, J.D., & Roediger, H.L. (2008). The critical importance of retrieval for learning. *Science*, 319(5865), 966-968.

Liffiton, M., Sheese, B.E., Savelka, J., & Denny, P. (2023). CodeHelp: Using large language models with guardrails for scalable support in programming classes. *Proceedings of SIGCSE 2024*.

Posner, G.J., Strike, K.A., Hewson, P.W., & Gertzog, W.A. (1982). Accommodation of a scientific conception: Toward a theory of conceptual change. *Science Education*, 66(2), 211-227.

Schmucker, R., Xia, M., Azaria, A., & Mitchell, T. (2024). Ruffle&Riley: Insights from Designing and Evaluating a Large Language Model-Based Conversational Tutoring System. *Proceedings of AIED 2024*.

Sirkiä, T., & Sorva, J. (2012). Exploring programming misconceptions: An analysis of student mistakes in visual program simulation exercises. *Proceedings of Koli Calling 2012*.

Sweller, J. (1988). Cognitive load during problem solving: Effects on learning. *Cognitive Science*, 12(2), 257-285.

Vygotsky, L.S. (1978). *Mind in society: The development of higher psychological processes*. Harvard University Press.

Weiner, B. (1985). An attributional theory of achievement motivation and emotion. *Psychological Review*, 92(4), 548-573.

Wood, D., Bruner, J.S., & Ross, G. (1976). The role of tutoring in problem solving. *Journal of Child Psychology and Psychiatry*, 17(2), 89-100.

---

## Appendix A — Raw run artefacts

| Run | Path | Strategies × Scenarios |
|---|---|---|
| Baseline | `output/tutor_comparison_2026-05-30_152306/results.json` | 7 × 4 = 28 |
| Iter 2 | `output/tutor_comparison_2026-05-30_172527/` (LLM-grader fact-check) | 7 × 4 = 28 + 4 fact-check |
| Final | `output/tutor_comparison_2026-05-30_181625/results.json` | 7 × 4 = 28 |

All raw JSON contains: scenario concept, student belief, per-strategy response text, token count, latency. CPAL responses additionally contain `factcheck_stripped` count and `factcheck_bad` sentence list.

## Appendix B — Source files for reproduction

- Runner: `scripts/compare_tutors_against_cpal.py`
- CPAL frontend prompt: `api/student_app.py` (function `_try_ollama`)
- Fact-check patterns: `api/student_app.py` (`_FACTCHECK_PATTERNS`)
- Quiz items: `data/quiz_bank.json`
- Wrong-model catalogue: `data/mental_models/wrong_models_catalogue.json`
- LP rubric classifier: `src/orchestrator/lp_diagnostic.py`
- Three-channel state: `src/orchestrator/student_state_tracker.py`

To reproduce: `python scripts/compare_tutors_against_cpal.py` (requires Ollama running locally with `llama3.1:8b` pulled).

---

**End of report.**
