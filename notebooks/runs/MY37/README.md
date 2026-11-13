# Think on the Graph: run MY37

This page explains how the algorithm reached its result for this scenario. Every stage is explained in plain words, with the meaning of its terms, followed by one worked example with the real scores of this run. The examples follow the same thread through all stages: the concept `array_reversal`. Every output of every stage is in `MY37.ipynb` and `report.html`; the interactive graph is `MY37_G.html`.

## Input

Program:
```java
int[] a = {1, 2, 3, 4};
for (int i = 0; i < a.length; i++) {
    int t = a[i];
    a[i] = a[a.length - 1 - i];
    a[a.length - 1 - i] = t;
}
for (int i = 0; i < a.length; i++) {
    System.out.print(a[i] + " ");
}
```
**Question.** The programmer wanted to reverse the array. What does this print, and what is wrong?

**Student's answer.** 1 2 3 4, unchanged. Every pair gets swapped twice: i = 0 swaps a[0] and a[3], then i = 3 swaps them back. The loop should only run while i < a.length / 2

**What the program really does.** The loop runs over the whole array, so each pair is swapped twice and ends where it started. The program prints `1 2 3 4`. Stopping at i < a.length / 2 fixes it. The student's answer is correct.

## Result

- **Wrong rules held:** none
- **Root cause:** none
- **Overall level:** L4
- **Level per concept:** `array_exchange` L4, `array_reversal` L4, `array_traversal` L3, `for_loop` L4, `length_field` L4, `loop_control` L4, `loop_variable` L2

**Check of this result (read by hand, 2026-11-13).** The diagnosis matches the answer: nothing is held.

## The idea in short

The program does not ask a language model "what is wrong with this answer?". It walks a **knowledge graph** of Java and asks the model small questions about one edge at a time. Each answer of the model must point at the student's own words.

- A **concept** is a topic of Java, for example `integer_division`.
- A **misconception** is a wrong rule a student may believe. An **error** is a rule broken in a program.
- A **level** says how well a concept is understood, from L0 (wrong) to L4 (deep). Each concept has five.
- An **edge** joins two of these. A *prerequisite* edge says one concept must be understood before another. A *misconception* edge joins a concept to a wrong rule and also stores the right rule (its *twin*). A *level* edge joins a concept to a level and stores the **ways** a student can show that level.

Two settings control the walk: the **width N = 3** (how many options are followed at each choice) and the **depth D = 3** (how many rounds the walk takes). The model (`claude-opus-5-5`) is used only in stage 3. All other stages are fixed rules, so they always give the same result.

## Stage 1. From the code to a small graph G (no model)

This stage reads only the program, not the answer. It decides which part of the big knowledge graph this scenario may use.

**1.1 Clean the code.** Strange characters from copy and paste are replaced by normal ones. Then the text inside strings and comments is blanked out. This is called **masking**. It is needed because the next step searches the code for patterns, and a word like `for` inside a printed sentence must not be mistaken for a for loop.

**Worked example from this run.** This program has no string and no comment, so nothing is blanked.

**1.2 Find the concepts in the code.** Every concept in the graph comes with search patterns (regular expressions) that describe how it looks in Java. All patterns are tried on the code. A match is called a **hit**. A concept with at least one hit is **tagged**: the program contains it.

**Worked example from this run.** The concept `array_reversal` has the pattern `\[\s*\w+\.length\s*-\s*1\s*-\s*\w+\s*\]`. It matches `[a.length - 1 - i]` on line 4, so `array_reversal` is tagged. In total 26 concepts are tagged.

**1.3 Treat very common concepts with care.** Some concepts appear in almost every program: a statement, an expression, an assignment. The graph marks them **generic**. If they were treated like the others, every program would seem to be about them. So a generic concept is kept only when the code connects it to a specific concept, and it can never be a starting point of the walk by itself.

**Worked example from this run.** 5 of the 26 tagged concepts are generic: `assignment`, `data_type`, `expression`, `statement`, `string_literal`. The other 21 are specific and can start the walk.

**1.4 Cut out the small graph G.** G is made of the tagged concepts, the edges of the knowledge graph between them, all their misconception and error edges, and their levels. From now on the algorithm sees only G. This is a safeguard: it can only name a wrong rule that belongs to something the program really contains.

**Worked example from this run.** G has 28 edges between concepts, 158 misconception / error edges and 130 level edges. Of these, 2 misconception / error edges belong to `array_reversal`.

## Stage 2. Clauses and start concepts (no model)

**2.1 Cut the answer into clauses.** A **clause** is one thing the student claims. The answer is cut at the end of each sentence, at ';', and before 'because' and 'so'. The clauses get numbers: c1, c2, … The numbers matter later: whenever the model gives a label, it must say which clause numbers the label is based on. That way every finding can be traced back to the student's words.

**Worked example from this run.** The answer becomes 3 clauses: **c1** “1 2 3 4, unchanged” **c2** “Every pair gets swapped twice: i = 0 swaps a[0] and a[3], then i = 3 swaps them back” **c3** “The loop should only run while i < a.length / 2”

**2.2 Choose where the walk starts.** The walk needs **start concepts**. The candidates are the specific concepts of G. If there are more than N = 3, each one gets a **BM25 score**. BM25 is the score search engines use: it counts the words that the answer shares with the text of a concept, and counts a rare word for more than a common one. The N concepts with the highest scores start the walk.

**Worked example from this run.** The scores are: `array_reversal` 27.26, `array_traversal` 26.56, `loop_control` 25.06. The next one, `array_initializer` with 24.64, is below the cut. There were 23 candidates and the top 3 are taken: `array_reversal`, `array_traversal`, `loop_control`.

## Stage 3. The walk over G (the model is asked here)

The walk moves through G in rounds called **depths**. It is a **beam search**: at every choice it follows only the best N = 3 options and drops the rest. This keeps the work small, because one concept can have twenty or more edges. At each depth, the six steps below are done for every concept the walk is currently at.

**3.1 Collect the edges of the concept.** When the walk first arrives at a concept, it looks *into* it: it collects the concept's misconception and error edges (what could be believed wrongly about it) and its level ways (how it could be understood rightly). These are two separate groups. At the next depth it looks *out of* the concept: it collects the edges that lead to neighbouring concepts. The collected edges are called **candidates**.

**Worked example from this run.** When the walk arrives at `array_reversal`, it collects 15 level ways and 2 misconception / error edges.

**3.2 Prune: keep only the relevant candidates (first question to the model).** There are too many candidates to judge each one carefully. So the model is first asked a quick question: *which 3 of these rules does the answer have anything to do with?* It returns up to N edges, each with a number. The numbers are scaled so that they add up to 1. This number is the **prune score**: the share of relevance the model gives to that edge.

**Worked example from this run.** Of the 15 level ways at `array_reversal`, the model keeps L4 way “diagnose an error” (0.60) + L4 way “predict a change” (0.25) + L3 way “relation to neighbour” (0.15) = 1.00. The other 12 are dropped here and never judged.

**3.3 Label: judge each kept edge against the clauses (second question to the model).** Now the model reads each kept edge carefully and gives it a **label**:

- for a misconception or error edge: **held** (the student's words state this wrong rule), **correct** (they state the right rule instead) or **not applied** (the answer says nothing about it);
- for a level way: **shown** or not applied;
- for an edge between two concepts: **confirmed** (the student carries the rule from one concept to the other) or **broken** (the student fails to).

With each label the model must give the **clause numbers** it is based on and a **confidence** from 0 to 1 (how sure it is). A label with no clause number is thrown away. So the model cannot diagnose from its own knowledge: every label is tied to one edge of G and to words the student wrote.

**Worked example from this run.** L4 way “diagnose an error”: **shown**, based on clauses c1, c2, c3, confidence 0.95; L4 way “predict a change”: **shown**, based on clauses c1, c2, c3, confidence 0.90; L3 way “relation to neighbour”: **shown**, based on clauses c2, c3, confidence 0.85. The rule on the shown edge is: “rule broken: Only the first half is traversed. Kind: silent logic error. Trigger class: the loop runs i < N, so every pair is swapped twice and the a…” Compare it with clauses c1, c2, c3: “1 2 3 4, unchanged” / “Every pair gets swapped twice: i = 0 swaps a[0] and a[3], then i = 3…” / “The loop should only run while i < a.length / 2”.

**3.4 Score and keep.** Each labelled edge gets a **score = prune score × confidence**. An edge scores high only if it was both relevant and judged with confidence. Then the edges are sorted into **tiers** (ranks):

- **tier 0**: a held misconception or a broken edge. These point at a fault and are always kept.
- **tier 1**: a held error.
- **tier 2**: correct, confirmed or shown. These show understanding. They fill the places that are left, up to N = 3, highest score first.

The kept edges form the **paths** of the walk. Every labelled edge, kept or not, is also stored as **evidence**; the levels in stage 6 are read from all the evidence.

**Worked example from this run.** L4 way “diagnose an error”: 0.60 × 0.95 = 0.57; L4 way “predict a change”: 0.25 × 0.90 = 0.23; L3 way “relation to neighbour”: 0.15 × 0.85 = 0.13. Kept at depth 1: ReverseFullLength (correct, tier 2, score 0.85); L4 way “diagnose an error” (shown, tier 2, score 0.57); L3 way “relation to neighbour” (shown, tier 2, score 0.54).

**3.5 Decide where to go next.** A kept edge between two concepts leads the walk to the concept at its other end; that concept is **entered** and is looked into at the next depth. A concept with a held misconception stays in the walk, so that the concepts it depends on are examined too: the mistake may begin earlier.

**Worked example from this run.** The edge loop_variable → loop_control was kept (confirmed, score 0.44), so the walk enters `loop_variable` at the next depth.

**3.6 Decide whether to stop (no model).** After each depth two things are checked. First, **clause coverage**: is every clause explained by at least one labelled rule edge? Second, the **graph check**: has every entered concept been looked into and out of? If both are true, the walk stops. If not, it goes on, but never beyond depth D = 3 plus one closing round that finishes the concepts entered last.

**Worked example from this run.** c1 is covered by ReverseFullLength. c2 is covered by ReverseFullLength. c3 is covered by ReverseFullLength. In total 3 of 3 clauses are covered. The walk stopped at depth 4 because the depth limit was reached. The model was asked 20 prune questions and 43 label questions.

## Stage 4. From labels to faults (rules, no model)

A kept edge labelled *held* is a possible **fault**. But one wrong sentence often produces several labels, so four rules make sure each mistake is counted once.

- **An error next to a misconception.** A misconception is the belief; an error is what it causes in a program. If both are held on the same concept, the misconception is the fault and the error is only supporting evidence.
- **One fault, one place.** If the same misconception is held on two concepts joined by a prerequisite edge, it is counted once, at the concept the graph names as its main (*primary*) concept.
- **Shadows.** A held label on a more general concept, based only on clauses that a stronger label on a more specific concept already uses, is a **shadow**: the same sentence read a second time. A shadow is not a fault.
- **Broken edges.** A broken edge A → B means the student did not carry the rule of A into B. If it is based on the same clauses as a held misconception, it is a **consequence** of that misconception and not a separate fault.

**Worked example from this run.** No edge is held, so there is no fault. 8 misconception / error edges were labelled *correct*; the strongest is ReverseFullLength at `array_reversal` (0.90 × 0.95 = 0.85): the answer states its right rule, “Swapping for i < n/2 is enough; going to n undoes the reversal.”

## Stage 5. Root cause (rule, no model)

If several concepts have a fault, the **root cause** is the one to teach first. The rule looks at what each faulty concept depends on (its **prerequisites** in G). If a prerequisite also has a fault, the root moves back to it, because a mistake in the basis explains the mistake in what is built on it. Among the concepts found this way, the root is the one with the fewest prerequisites of its own. If two are equal, the one with the higher confidence wins.

**Worked example from this run.** There is no fault, so there is no root cause.

## Stage 6. Level of each concept (rule, no model)

Each concept gets one of five **levels**:

- **L0**: the answer holds a rule that contradicts Java, or reads the code in an everyday sense;
- **L1**: it states one correct rule but does not use it;
- **L2**: it applies the rules to the code step by step;
- **L3**: it relates the parts to each other and to the purpose of the code;
- **L4**: it reasons beyond the given code (predicts what a change would do, finds a bug).

Every level has **ways**: things a student does at that level, such as "output prediction" at L2. The model is never asked for a level. In stage 3 it only said whether a way is *shown*. The level then follows by rule: a concept is **L0** if it has a fault, or if only L0 ways are shown on it. Otherwise it gets the **highest** level among the ways shown, because each level includes the ones below it.

**Worked example from this run.** On `array_reversal` the ways shown are L3 “relation to neighbour” (score 0.13), L4 “diagnose an error” (score 0.57), L4 “predict a change” (score 0.23); the highest level among them is L4, so `array_reversal` is L4.

## Stage 7. Overall level (rule, no model)

One level is given for the whole answer. If there is a root cause, it is the level of the root concept: the student stands where the mistake begins. If there is no fault, the levels of all concepts are sorted from high to low and the middle one is taken, so that one weak or one strong concept does not decide alone.

**Worked example from this run.** There is no root cause. The levels, from high to low, are L4, L4, L4, L4, L4, L3, L2. The middle one (number 4 of 7) is L4. Overall level: **L4**.

## The final picture

![The labelled graph at the end of the run](figure08.png)
