# Think on the Graph: run MY19

This page explains how the algorithm reached its result for this scenario: each step's method, with one example from this run. Every output of every step (all edges offered, every score and label, the figures) is in `MY19.ipynb` and in `report.html`; the interactive graph is `MY19_G.html`.

## Input

Program:
```java
int a = 7, b = 2;
double q = a / b;
int r = a % b;
System.out.println(q + " " + r);
```
**Question.** Explain how Java works out q and r.

**Student's answer.** q is a double, so 7 / 2 is done with decimals and gives 3.5, and 7 % 2 is the half that is left over, 0.5.

**What the program really does.** `a / b` is integer division of two ints, 7 / 2 = 3, widened to 3.0 when stored in q. `a % b` is the whole-number remainder, 1. The program prints `3.0 1`.

## Result

- **Wrong rules held:** TargetTyping at `integer_division`
- **Root cause:** `integer_division` / TargetTyping
- **Overall level:** L0
- **Level per concept:** `arithmetic_operators` L0, `expression` L0, `integer_division` L0

**Check of this result (read by hand, 2026-11-13).** Partly right. TargetTyping is the right label for q. The second wrong statement, that 7 % 2 is 0.5, is not picked up: the graph has no misconception for reading the remainder as the fractional part.

## How the algorithm reached this result

Settings of this run: width N = 3 (how many edges survive each choice), depth D = 3, model `claude-opus-5-5`. The model is asked in step 3 only; every other step is a fixed rule.

### Step 1. From the code to a subgraph G (no model)

Only the program is read here, not the student's answer.

- **Prepare the code.** Characters that a paste changes (curly quotes, odd spaces) are mapped back to plain ones, and the inside of string literals and comments is blanked, so text inside a string can never trigger a pattern.
- **Tag concepts.** Every concept node of the knowledge graph stores regular expressions for how the concept looks in Java (code patterns, signals, operator symbols, type names). All of them are run over the prepared code. A match is a *hit* (which pattern, which text, which line), and a concept with at least one hit is tagged.
- **Mark generic concepts.** Concepts that match nearly any program (statement, expression, assignment) are marked generic: they stay in G but cannot be a starting point by themselves.
- **Cut out G.** G is the tagged concepts, the graph's prerequisite and parallel edges between them, all their misconception and error edges, and their five level nodes (L0 to L4) with the ways of each level. Everything later is restricted to G, so the result can only name things the code actually contains.

*In this run:* `integer_division` is tagged because its signal `int_vars_one_decl_div` matches `int a = 7, b = 2; double q = a / b` on line 1. In all 12 concepts are tagged (4 generic). G has 10 concept edges, 46 misconception / error edges and 60 level edges, in 3 connected pieces.

### Step 2. Clauses and start concepts (no model)

- **Clauses.** The answer is cut at sentence ends, at ';' and before 'because' / 'so', and the pieces are numbered c1, c2, … Every label made later must name the clause numbers it rests on, so each finding is tied to the student's own words.
- **Start concepts.** The candidates are the tagged, non-generic concepts (plus a generic one when the answer repeats the code text that tagged it). If there are more than N, each is scored by BM25, a word-overlap score between the answer and the concept's text (its name and the texts of its edges), and the top N start the walk.

*In this run:* 2 clauses; c1 is “q is a double”. For the start, `integer_division` scores 16.07, the highest of 8 candidates; `string_concatenation` is 4th with 7.66 and is left out. Start concepts: `integer_division`, `arithmetic_operators`, `remainder_operator`.

### Step 3. The walk over G (the model is asked here, twice per choice)

The walk goes depth by depth. For each current concept:

1. **Edge search (no model).** A concept that has just been entered offers its misconception / error edges and its level ways (each way of a level is an edge of its own, whose text is the way's exact rule). A concept already read offers its prerequisite and parallel edges. An edge already kept is not offered again.
2. **Prune (model).** The model sees the code, the question, the answer and the offered edges, and returns at most 3 of them with a relevance score; the scores are rescaled to add up to 1. Misconception edges and level ways are pruned separately, so they never compete for the same place.
3. **Label (model).** Each surviving edge is read against the numbered clauses. A misconception or error edge is labelled *held* (the answer states this wrong rule), *correct* (it states the right rule) or *not applied*. A level way is *shown* or *not applied*. A concept edge is *confirmed* or *broken*. The reply must give the clause numbers and a confidence between 0 and 1; a label with no clause is thrown away. The model therefore never judges from its own knowledge: each label points at one edge of G and at the student's words.
4. **Score and keep.** Score = prune score × confidence. Held misconceptions and broken edges are always kept; held errors come next; correct, confirmed and shown labels fill what is left of the 3 places by score. Every labelled edge is recorded as evidence, kept or not.
5. **Move on.** The concept at the far end of a kept concept edge is entered and read at the next depth. A concept with a held misconception stays current, so that its prerequisites are examined (the fault may start further back).
6. **Stop test (no model).** The walk may stop when every clause is covered by a labelled rule edge and every entered concept has had its edges read. Clauses still uncovered pull in unvisited concepts by BM25. Otherwise it runs to depth 3, plus one closing round in which the last concepts entered get their own edges read.

*In this run:* at `integer_division` 6 misconception edges are offered; **TargetTyping** gets prune score 0.55 and is labelled **held** on clauses 1, 2 with confidence 0.90, so its score is 0.55 × 0.90 = 0.49. Concepts read at each depth: depth 1: `integer_division`, `arithmetic_operators`, `remainder_operator`; depth 2: `integer_division`, `arithmetic_operators`, `remainder_operator`; depth 3: `arithmetic_operators`, `integer_division`, `remainder_operator`, `expression`. The model was asked 11 prune and 22 label questions. The walk stopped at depth 3: every clause was covered and no entered concept had an unread edge.

### Step 4. From labels to faults (rules, no model)

Every kept edge labelled *held* is a candidate fault. Rules then remove double counting:

- **Error beside a misconception.** A held error on a concept that also has a held misconception is evidence for it, not a second fault.
- **One fault, one place.** The same misconception held at both ends of a prerequisite edge is filed once: at the concept the graph marks as primary for it, otherwise at the dependent concept.
- **Shadows.** A held label on a prerequisite or generic concept that rests only on clauses a stronger, more specific label already rests on is a shadow of that label (one wrong sentence read twice). It stays in the record but is not a fault, cannot be the root and sets no level.
- **Broken edges.** A prerequisite edge A → B labelled *broken* means the rule of A was not carried into B, so the fault sits at B. If it rests on the same clauses as a held misconception it is that misconception's consequence, not a fault of its own.

*In this run:* the fault is **TargetTyping** at `integer_division`. For TargetTyping the graph's wrong rule is “The type of a numerical expression depends on the type expected by the surrounding context, so double d = a / b; keeps the fraction.” and the right rule is “The type of a numerical expression is determined by the expression, so double d = a / b; with int a and b still divides as ints.”; it rests on “q is a double; so 7 / 2 is done with decimals and gives 3.5, and 7 % 2 is the half that i…”. 1 shadow: TargetTyping at `expression`. 4 broken edges (e.g. `pre:arithmetic_operators->integer_division`), 4 of them consequences of a held misconception.

### Step 5. Root cause (rule)

From each faulty concept the rule walks backwards over the prerequisite edges of G. Whenever a prerequisite also has a fault, the candidate moves back to it, because a fault in what a concept depends on explains the fault in the concept. Among the candidates, the root is the one with the fewest prerequisites of its own (the one furthest back); at a tie, the one whose label has the higher confidence.

*In this run:* only `integer_division` has a fault, and none of its prerequisites in G (`arithmetic_operators`) has one, so it is the root.

### Step 6. Level of each concept (rule, no model)

The model never names a level. It only says whether a *way* is shown, and the level is where that way sits in the graph (L0 contradicts Java, L1 states a rule, L2 applies the rules step by step, L3 relates the parts, L4 reasons beyond the given code). A concept is **L0** if a fault is kept on it, or if every way shown on it is an L0 way. Otherwise it gets the **highest** level among the ways shown, because the levels build on each other. A concept with no fault and no way shown gets no level.

*In this run:* `integer_division` keeps TargetTyping, so it is L0; on `expression` the ways shown are L0 “everyday reading”, so it is L0.

### Step 7. Overall level (rule)

With a root cause, the overall level is the level of the root concept: the student stands where the fault starts. Without one, it is the level reached on at least half of the concepts the answer touched, so one weaker concept does not pull the whole answer down.

*In this run:* the root is `integer_division` and its level is L0. **Overall level: L0.**

## The final picture

![The labelled graph at the end of the run](figure07.png)
