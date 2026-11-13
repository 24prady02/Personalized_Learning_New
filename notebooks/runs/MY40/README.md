# Think on the Graph: run MY40

This page explains how the algorithm reached its result for this scenario: each step's method, with one example from this run. Every output of every step (all edges offered, every score and label, the figures) is in `MY40.ipynb` and in `report.html`; the interactive graph is `MY40_G.html`.

## Input

Program:
```java
double[] p = {0.2, 0.5, 0.3};
int[] freq = new int[3];
for (int t = 0; t < 10; t++) {
    double r = Math.random();
    double sum = 0.0;
    int j = 0;
    while (r >= sum + p[j]) {
        sum += p[j];
        j++;
    }
    freq[j]++;
}
System.out.println(freq[1]);
```
**Question.** What does the program print, and why?

**Student's answer.** 5. Page 1 has probability 0.5, so in 10 steps the surfer goes there exactly 5 times.” Actual: it varies from run to run; five runs gave 6, 4, 8, 5 and 6.

**What the program really does.** Each pass draws a random number and counts which page it lands on. Page 1 is chosen with probability 0.5 on each pass, so freq[1] is 5 only on average: the printed number changes from run to run (five runs gave 6, 4, 8, 5 and 6).

## Result

- **Wrong rules held:** ProbabilityIsPrediction at `math_random`
- **Root cause:** `math_random` / ProbabilityIsPrediction
- **Overall level:** L0
- **Level per concept:** `for_loop` L3, `loop_control` L3, `math_library` L2, `math_random` L0, `println` L2, `statement` L0

**Check of this result (read by hand, 2026-11-13).** The diagnosis matches the answer. Two flaws: the line beginning 'Actual:' was pasted into the answer box, and the root sits on math_random because the code patterns do not tag the simulation concept for this program.

## How the algorithm reached this result

Settings of this run: width N = 3 (how many edges survive each choice), depth D = 3, model `claude-opus-5-5`. The model is asked in step 3 only; every other step is a fixed rule.

### Step 1. From the code to a subgraph G (no model)

Only the program is read here, not the student's answer.

- **Prepare the code.** Characters that a paste changes (curly quotes, odd spaces) are mapped back to plain ones, and the inside of string literals and comments is blanked, so text inside a string can never trigger a pattern.
- **Tag concepts.** Every concept node of the knowledge graph stores regular expressions for how the concept looks in Java (code patterns, signals, operator symbols, type names). All of them are run over the prepared code. A match is a *hit* (which pattern, which text, which line), and a concept with at least one hit is tagged.
- **Mark generic concepts.** Concepts that match nearly any program (statement, expression, assignment) are marked generic: they stay in G but cannot be a starting point by themselves.
- **Cut out G.** G is the tagged concepts, the graph's prerequisite and parallel edges between them, all their misconception and error edges, and their five level nodes (L0 to L4) with the ways of each level. Everything later is restricted to G, so the result can only name things the code actually contains.

*In this run:* `math_random` is tagged because its pattern `Math\.random\s*\(` matches `Math.random(` on line 4. In all 31 concepts are tagged (4 generic). G has 37 concept edges, 205 misconception / error edges and 155 level edges, in 3 connected pieces.

### Step 2. Clauses and start concepts (no model)

- **Clauses.** The answer is cut at sentence ends, at ';' and before 'because' / 'so', and the pieces are numbered c1, c2, … Every label made later must name the clause numbers it rests on, so each finding is tied to the student's own words.
- **Start concepts.** The candidates are the tagged, non-generic concepts (plus a generic one when the answer repeats the code text that tagged it). If there are more than N, each is scored by BM25, a word-overlap score between the answer and the concept's text (its name and the texts of its edges), and the top N start the walk.

*In this run:* 5 clauses; c1 is “5”. For the start, `arithmetic_operators` scores 36.94, the highest of 28 candidates; `loop_control` is 4th with 17.39 and is left out. Start concepts: `arithmetic_operators`, `compound_assignment`, `println`.

### Step 3. The walk over G (the model is asked here, twice per choice)

The walk goes depth by depth. For each current concept:

1. **Edge search (no model).** A concept that has just been entered offers its misconception / error edges and its level ways (each way of a level is an edge of its own, whose text is the way's exact rule). A concept already read offers its prerequisite and parallel edges. An edge already kept is not offered again.
2. **Prune (model).** The model sees the code, the question, the answer and the offered edges, and returns at most 3 of them with a relevance score; the scores are rescaled to add up to 1. Misconception edges and level ways are pruned separately, so they never compete for the same place.
3. **Label (model).** Each surviving edge is read against the numbered clauses. A misconception or error edge is labelled *held* (the answer states this wrong rule), *correct* (it states the right rule) or *not applied*. A level way is *shown* or *not applied*. A concept edge is *confirmed* or *broken*. The reply must give the clause numbers and a confidence between 0 and 1; a label with no clause is thrown away. The model therefore never judges from its own knowledge: each label points at one edge of G and at the student's words.
4. **Score and keep.** Score = prune score × confidence. Held misconceptions and broken edges are always kept; held errors come next; correct, confirmed and shown labels fill what is left of the 3 places by score. Every labelled edge is recorded as evidence, kept or not.
5. **Move on.** The concept at the far end of a kept concept edge is entered and read at the next depth. A concept with a held misconception stays current, so that its prerequisites are examined (the fault may start further back).
6. **Stop test (no model).** The walk may stop when every clause is covered by a labelled rule edge and every entered concept has had its edges read. Clauses still uncovered pull in unvisited concepts by BM25. Otherwise it runs to depth 3, plus one closing round in which the last concepts entered get their own edges read.

*In this run:* at `math_random` 2 misconception edges are offered; **ProbabilityIsPrediction** gets prune score 0.95 and is labelled **held** on clauses 1, 2, 3 with confidence 0.85, so its score is 0.95 × 0.85 = 0.81. Concepts read at each depth: depth 1: `arithmetic_operators`, `compound_assignment`, `println`; depth 2: `arithmetic_operators`, `compound_assignment`, `println`, `loop_control`, `for_loop`, `math_random`; depth 3: `math_random`, `loop_control`, `for_loop`, `statement`, `loop_body`, `nested_loops`; depth 4: `math_library`, `control_flow`, `method_call`, `array_creation`. The model was asked 32 prune and 64 label questions. The walk stopped at depth 4: the depth limit was reached.

### Step 4. From labels to faults (rules, no model)

Every kept edge labelled *held* is a candidate fault. Rules then remove double counting:

- **Error beside a misconception.** A held error on a concept that also has a held misconception is evidence for it, not a second fault.
- **One fault, one place.** The same misconception held at both ends of a prerequisite edge is filed once: at the concept the graph marks as primary for it, otherwise at the dependent concept.
- **Shadows.** A held label on a prerequisite or generic concept that rests only on clauses a stronger, more specific label already rests on is a shadow of that label (one wrong sentence read twice). It stays in the record but is not a fault, cannot be the root and sets no level.
- **Broken edges.** A prerequisite edge A → B labelled *broken* means the rule of A was not carried into B, so the fault sits at B. If it rests on the same clauses as a held misconception it is that misconception's consequence, not a fault of its own.

*In this run:* the fault is **ProbabilityIsPrediction** at `math_random`. For ProbabilityIsPrediction the graph's wrong rule is “A probability (e.g. 70%) predicts what the next single trial will do.” and the right rule is “A probability describes the long-run frequency over many trials, not one outcome.”; it rests on “5; Page 1 has probability 0.5; so in 10 steps the surfer goes there exactly 5 times”. 1 broken edge (e.g. `pre:math_library->math_random`), 1 of them consequences of a held misconception.

### Step 5. Root cause (rule)

From each faulty concept the rule walks backwards over the prerequisite edges of G. Whenever a prerequisite also has a fault, the candidate moves back to it, because a fault in what a concept depends on explains the fault in the concept. Among the candidates, the root is the one with the fewest prerequisites of its own (the one furthest back); at a tie, the one whose label has the higher confidence.

*In this run:* only `math_random` has a fault, and none of its prerequisites in G (`math_library`) has one, so it is the root.

### Step 6. Level of each concept (rule, no model)

The model never names a level. It only says whether a *way* is shown, and the level is where that way sits in the graph (L0 contradicts Java, L1 states a rule, L2 applies the rules step by step, L3 relates the parts, L4 reasons beyond the given code). A concept is **L0** if a fault is kept on it, or if every way shown on it is an L0 way. Otherwise it gets the **highest** level among the ways shown, because the levels build on each other. A concept with no fault and no way shown gets no level.

*In this run:* `math_random` keeps ProbabilityIsPrediction, so it is L0; on `loop_control` the ways shown are L1 “names the element”, L3 “purpose of the whole”, so it is L3.

### Step 7. Overall level (rule)

With a root cause, the overall level is the level of the root concept: the student stands where the fault starts. Without one, it is the level reached on at least half of the concepts the answer touched, so one weaker concept does not pull the whole answer down.

*In this run:* the root is `math_random` and its level is L0. **Overall level: L0.**

## The final picture

![The labelled graph at the end of the run](figure08.png)
