# Think on the Graph: run MY20

This page explains, stage by stage, how the algorithm reached its result for this scenario. Each stage says what it does, why, and what its terms mean, and then shows one of the outputs of that stage from this run. Every output of every stage (all edges offered, all scores and labels, the figures) is in `MY20.ipynb` and `report.html`; the interactive graph is `MY20_G.html`.

## Input

Program:
```java
int n = (int) (Math.random() * 6) + 1;
System.out.println(n);
```
**Question.** Explain what values n can have

**Student's answer.** n is a whole number from 1 to 6, for example 4

**What the program really does.** Math.random() gives a double from 0.0 up to but not including 1.0. Times 6 it is from 0.0 up to 6.0, the cast drops the fraction to give 0 to 5, and adding 1 gives a whole number from 1 to 6. The student's answer is correct.

## Result

- **Wrong rules held:** none
- **Root cause:** none
- **Overall level:** L2
- **Level per concept:** `arithmetic_operators` L2, `explicit_cast` L2, `expression` L2, `math_random` L2, `type_conversion` L3

**Check of this result (read by hand, 2026-11-13).** The diagnosis matches the answer: nothing is held.

## The idea

The method is *Think on the Graph*. A language model is not asked "what is wrong with this answer?". Instead the program walks a **knowledge graph** of Java and asks the model only small questions about one edge at a time, each of which must be tied to the student's own words. The graph has three kinds of node: **concept** nodes (for example `integer_division`), **misconception** and **error** nodes (a wrong rule a student may believe, or a rule broken in a program), and five **level** nodes for every concept (L0 to L4). Its edges are: **prerequisite** (A must be understood before B), **parallel** (A and B are learned side by side), **misconception / error** (from a concept to a wrong rule; the edge stores the wrong rule and, as its *twin*, the right rule), and **has_level** (from a concept to one of its levels; the edge stores the *ways* a student can show that level, each with an exact rule).

Two numbers control the walk: the **width N = 3** (how many options survive each choice) and the **depth D = 3** (how many rounds the walk may take). The model here is `claude-opus-5-5`; it is used in stage 3 only.

## Stage 1. From the code to a subgraph G (no model)

This stage reads only the program, never the student's answer. Its job is to decide which part of the knowledge graph this scenario is allowed to use.

**1.1 Mask the code.** The code is **masked**: the inside of every string literal and every comment is replaced by spaces of the same length. Masking matters because the next step matches patterns: the word `for` inside a printed sentence must not count as a for loop. Lengths and line numbers stay the same, so a match can still be reported by line.

*One of the outputs at this stage:* this program has no string literal or comment, so the masked code equals the original.

**1.2 Tag concepts.** Every concept node stores a *reader block*: regular expressions that describe how the concept looks in Java, in several *channels* (code patterns, signals, operator symbols, type names). All of them are run over the masked code. Each match is a **hit**: which channel and pattern, the matched text, and the line. A concept with at least one hit is **tagged**. There is nothing learned here; the patterns in the graph are the whole "model".

*One of the outputs at this stage:* `type_conversion` is tagged: its pattern `\(\s*(?:int|double|long|float|char|short|byte)\s*…` matches `(int)` on line 1.

**1.3 Handle generic concepts.** The graph marks some concepts **generic**: they are so basic (statement, expression, assignment, a literal, `int`) that their pattern fires on almost any line of Java. If all of them were kept, every program would seem to be "about" them and the diagnosis would drift to vague places. So a tagged generic concept is kept only when the code ties it to something specific: the graph has a prerequisite or parallel edge between it and a non-generic tagged concept, or one of its *decisive* signals fired (a pattern that by itself shows the concept is the point of the code). A kept generic concept stays marked generic: the walk can reach it and it can get a level, but it cannot be a starting point by itself, and a wrong-rule label on it is treated as a shadow of a more specific one (stage 4).

*One of the outputs at this stage:* 11 concepts are tagged and kept, 3 of them generic (`expression`, `primitive_type`, `statement`).

**1.4 Cut out the subgraph G.** G consists of the kept concepts, the graph's prerequisite and parallel edges whose two ends are both kept, every misconception and error edge of those concepts, and their level nodes with all their ways. From here on the algorithm sees only G, so it can only name wrong rules that belong to concepts the code really contains. The concepts of G fall into **pieces** (groups joined by edges); the graph has no edge between two pieces, so the walk never crosses from one to another.

*One of the outputs at this stage:* G has 9 concept edges, 49 misconception / error edges and 55 level edges, in 2 pieces (sizes 9, 2).

## Stage 2. Clauses and start concepts (no model)

**2.1 Split the answer into clauses.** A **clause** is one statement the student makes. The answer is cut at sentence ends, at ';', and before 'because' and 'so' (a reason and its conclusion are separate claims); a remark in parentheses becomes its own clause. The clauses are numbered c1, c2, … This numbering is what keeps the model honest later: every label it gives must name the clause numbers it rests on, so each finding points at words the student actually wrote.

*One of the outputs at this stage:* 1 clauses. c1: “n is a whole number from 1 to 6, for example 4”

**2.2 Choose the start concepts.** The walk has to begin somewhere; these are the **start concepts** (in Think on the Graph, the *topic entities*). The candidates are the non-generic concepts of G, plus a generic one when the answer itself repeats the code text that tagged it (for example the student writes `=`). If there are more than N, they are ranked by **BM25**, the standard search-engine score: it compares the words of the answer with the words of a concept's text (its name and the texts of its edges), counting shared words, giving rare words more weight and long texts less. The top N = 3 are the start concepts. No model is used, so the same answer always starts at the same place.

*One of the outputs at this stage:* `arithmetic_operators` scores 9.57, the highest of 8 candidates; `method_call` is 4th with 4.46 and is left out. Start concepts: `arithmetic_operators`, `explicit_cast`, `math_random`.

## Stage 3. The traversal: walking G (the model is asked here)

The walk is a **beam search**. "Beam" means that at every choice only the best N = 3 options are followed, so the work stays small even when a concept has dozens of edges. It proceeds in rounds called **depths**, at most D = 3 of them plus one closing round. Throughout, the algorithm keeps four things: the **current concepts** (where it is now), the **paths** (the edges it has kept), the **evidence** (every edge that received a label, kept or not), and the set of edges it has already offered, so nothing is judged twice.

At each depth, for each current concept, the following happens.

**3.1 Edge search (no model).** The edges of the concept are collected as **candidates**. A concept that has just been entered is read *inwards*: its misconception and error edges (the wrong rules a student could hold about it) and its **level ways** (each way of each level is treated as an edge of its own, whose text is the way's exact rule). These are two separate *families*. A concept that has already been read inwards is read *outwards*: its prerequisite and parallel edges to other concepts in the same piece. So depth 1 asks "what does the answer show about these concepts?" and the later depths ask "which neighbouring concepts does that involve?".

*One of the outputs at this stage:* at `math_random`, 2 misconception / error edges and 16 level ways are offered when it is entered, and 1 concept edges when it is read outwards.

**3.2 Prune (model, first question).** There are usually far more candidates than can be judged carefully, so they are first **pruned**. The model sees the program, the question, the answer and the text of each candidate edge of one family, and returns at most N of them with a relevance score. The scores are rescaled so they add up to 1: this is the **prune score**, the share of relevance the model gives to that edge. Each family is pruned separately, so a level way never pushes out a misconception or the other way round. Edge ids the model invents are ignored.

*One of the outputs at this stage:* at `math_random` the level ways family is pruned to: L2 way “output prediction” 0.60, L4 way “predict a change” 0.25, L1 way “states the rule” 0.15.

**3.3 Label (model, second question).** Each edge that survived is now read against the numbered clauses and gets a **label**. For a misconception or error edge: **held** (the student's words state this wrong rule), **correct** (they state the right rule, its twin) or **not applied** (the answer says nothing about it). For a level way: **shown** or not applied. For a prerequisite or parallel edge: **confirmed** (the answer carries the rule from one concept into the other) or **broken** (it fails to). The misconception edges of one concept are judged together in a single question, because the same sentence can fit several wrong rules and the model should give *held* only to the one the student really claims. With the label the model must return the **clause numbers** it rests on and a **confidence** from 0 to 1. A label with no clause is discarded. This is the safeguard of the method: the model never diagnoses from its own knowledge; every label is attached to one edge of G and to the student's words.

*One of the outputs at this stage:* L2 way “output prediction” at `math_random` is labelled **shown** on clause 1 (“n is a whole number from 1 to 6, for example 4”) with confidence 0.90. The rule on that edge: “A double in [0, 1) that differs from call to call and run to run (e.g. RandomInt 1000 prints 548, then 141); (int) (Math.random() * 6) + 1 is an int…”

**3.4 Score and keep.** The **score** of a labelled edge is prune score × confidence: an edge counts for much only if it was both relevant and confidently labelled. The edges are then ranked in **tiers**. Tier 0 is a held misconception or a broken edge: these are findings about a fault and are always kept. Tier 1 is a held error. Tier 2 is everything that only confirms understanding (correct, confirmed, shown); these fill whatever is left of the N = 3 places, best score first. Kept edges are added to the paths. Every labelled edge, kept or not, is added to the evidence, because the levels in stage 6 are read from all of it.

*One of the outputs at this stage:* the score of L2 way “output prediction” is 0.60 × 0.90 = 0.54. At depth 1 the kept edges are: RandomCanReturnOne (correct, tier 2, 0.72); CastRounds (correct, tier 2, 0.56); L2 way “output prediction” (shown, tier 2, 0.54).

**3.5 Move to the next concepts.** Three things decide where the walk goes next. A kept prerequisite or parallel edge leads to the concept at its other end; that concept is **entered** and will be read inwards at the next depth, so it gets misconceptions and a level of its own. A concept with a held misconception stays current, so that its prerequisites are examined: the fault may begin further back. And any entered concept whose outward edges have not been read yet stays current until they are.

*One of the outputs at this stage:* `reached across pre:math_library->math_random, entered next: math_library`.

**3.6 Stop test (no model).** After each depth two checks are made. The **graph check**: has every entered concept had both its inward and its outward edges read? The **clause coverage** check: is every clause covered by at least one labelled rule edge (a level way does not count here, since it describes how the student reads the code, not which rule a clause applies)? If both hold, the walk stops as *sufficient*. If some clauses are still uncovered, they are matched by BM25 against the concepts not visited yet and the best N are entered. Otherwise the walk continues to depth D = 3, followed by one **closing round** in which the concepts entered last have their inward edges read, so that no concept is left half-read. The model's replies are cached by the exact text of the question, so running the same scenario again gives the same result without asking again.

*One of the outputs at this stage:* the walk stopped at depth 4 because the depth limit was reached. At the end 1 of 1 clauses were covered. The model was asked 16 prune questions and 29 label questions in all.

## Stage 4. Counting each mistake once (rules, no model)

**What this stage answers:** how many mistakes did the student really make, and at which concept does each one belong?

Stage 3 checks every concept on its own, so one wrong sentence of the student is usually flagged several times: at the concept it is really about, and again at related concepts. A **flag** is an edge that stage 3 labelled *held* (the student follows that wrong rule) or *broken* (the student did not carry a rule from one concept to the next). Stage 4 passes the flags through six fixed steps, in this order, and what is left at the end are the **mistakes**. Nothing is deleted: a flag that is not counted stays in the output, marked. Two flags rest on the **same words** when they name at least one clause in common; this is known exactly, because in 3.3 every label came with its clause numbers.

**4.1 Collect the flags.** From the paths (the edges kept in 3.4) take every edge labelled *held* and every edge labelled *broken*. These are the candidates.

*One of the outputs at this stage:* 0 kept edges labelled held; 0 labelled broken.

**4.2 An error beside a misconception.** A misconception is a wrong belief; an error node is the visible result of a belief in a program. If a concept has a held misconception and also a held error, the error is moved to the evidence list and is not counted. A held error on a concept with no held misconception stays a candidate.

*One of the outputs at this stage:* no concept has both, so nothing is moved.

**4.3 Two wrong rules on one concept.** The candidates are sorted by score, best first. If two misconceptions are held on the same concept and rest on the same words, both stay (a student can hold several), and the weaker one is marked as sharing its evidence with the stronger one.

*One of the outputs at this stage:* no two held misconceptions on one concept rest on the same words.

**4.4 One mistake, one place.** The graph can attach the same misconception to more than one concept, and gives each attachment a **role**: *primary* (the concept whose rule the misconception violates) or *context* (a concept where it also shows up). If the same misconception is held at two concepts: when exactly one of them is primary, the candidate at the other concept is dropped; otherwise, when one concept is a prerequisite of the other, the candidate at the prerequisite is dropped, so the mistake is filed at the concept that depends on it.

*One of the outputs at this stage:* no misconception is held at two concepts in a way this step merges.

**4.5 Shadows.** A held label X is a **shadow** of a candidate Y when every clause of X is also a clause of Y (X has no words of its own) and one of these is true: (a) X and Y are the same misconception, and Y sits at its primary concept while X does not; (b) X sits on a generic concept (such as `expression` or `statement`) and Y does not; (c) the concept of X is a prerequisite of the concept of Y, directly or over several prerequisite edges, and the model's confidence in X is not higher than in Y. The labels on generic concepts are tested first, then the others from low to high confidence, so the specific, confident label is the one that stays. Held labels that 3.4 did not keep are tested too. A shadow is not a mistake, cannot be the root cause and sets no level.

*One of the outputs at this stage:* no held label is a shadow.

**4.6 Broken links.** A broken prerequisite edge A → B says the student did not carry the rule of A into B. If it rests on the same words as a held misconception, it is that misconception's **consequence** and is not counted. Otherwise it is counted as a mistake at B, the concept that failed to use its prerequisite.

*One of the outputs at this stage:* no edge was labelled broken.

**Result of stage 4 in this run:** no wrong rule is held. The 4 misconception / error edges that received a label were all labelled *correct*, so no mistake is counted.

## Stage 5. Where the mistake starts: the root cause (rule, no model)

**What this stage answers:** if a teacher can fix only one thing first, which concept should it be?

Concepts build on each other: a prerequisite edge A → B in the subgraph says A must be understood before B. A mistake in A explains a mistake in B, so the search goes backwards along these edges.

**5.1 Mark the concepts with a mistake.** These are the concepts with a counted held misconception or error after stage 4, and the concepts at which a broken link was counted in 4.6.

*One of the outputs at this stage:* no concept has a held mistake.

**5.2 Walk back from each one.** Starting at each concept with a held mistake, visit all its prerequisites, then their prerequisites, and so on, as far as the subgraph goes. Each time a visited concept is itself marked in 5.1, it replaces the starting concept as the **candidate**. If none is marked, the starting concept is its own candidate.

*One of the outputs at this stage:* there is no concept to start from.

**5.3 Choose among the candidates.** The candidate with the fewest prerequisites of its own in the subgraph is the **root cause**: it stands furthest back. At a tie, the one whose held label the model gave the higher confidence is taken. Alphabetical order never decides.

*One of the outputs at this stage:* no mistake is counted, so there is no root cause.

## Stage 6. How well each concept is understood: the levels (rule, no model)

**What this stage answers:** for each concept the answer touched, how deep is the student's understanding?

| Level | In plain words |
|---|---|
| L0 | Holds a rule that contradicts Java, or reads the code in an everyday sense |
| L1 | States one correct rule, without applying it |
| L2 | Applies the rules to the code step by step |
| L3 | Relates the parts to each other and to the purpose of the whole |
| L4 | Reasons beyond the given code: predicts a change, transfers, diagnoses |

In the graph every level of a concept lists **ways**: concrete things a student at that level does, for example "output prediction" at L2. The model is never asked for a level. In 3.3 it only said which ways the answer *shows*; the level is read from where a way sits in the graph.

**6.1 Gather the evidence per concept.** Take every concept that appears in the evidence of stage 3 (kept in 3.4 or not). For each one collect two lists: the misconceptions held on it that are not shadows, and the ways shown on it.

*One of the outputs at this stage:* 6 concepts appear in the evidence: `arithmetic_operators`, `explicit_cast`, `expression`, `math_library`, `math_random`, `type_conversion`.

**6.2 Apply the first rule that fits.**

- (a) A misconception is held on the concept: the level is **L0**. The entry names the misconception.
- (b) Ways are shown and all of them are L0 ways (everyday reading, inconsistent trace): the level is **L0**.
- (c) Ways are shown and at least one is above L0: the level is the **highest** one shown. The levels build on each other (an answer that relates the parts has also applied the rules), so a lower way shown beside it is only listed.
- (d) Nothing is held and no way is shown: the concept gets no level.

A held error node is not a misconception, so rule (a) does not apply to it.

*One of the outputs at this stage:*

| Concept | Level | Rule | Why |
|---|---|---|---|
| `arithmetic_operators` | L2 | (c) | ways shown: L2 “output prediction” |
| `explicit_cast` | L2 | (c) | ways shown: L2 “output prediction” |
| `expression` | L2 | (c) | ways shown: L2 “output prediction” |
| `math_library` | none | (d) | nothing held, no way shown |
| `math_random` | L2 | (c) | ways shown: L1 “states the rule”, L2 “output prediction” |
| `type_conversion` | L3 | (c) | ways shown: L2 “output prediction”, L3 “relation to neighbour” |

## Stage 7. One level for the whole answer (rule, no model)

**What this stage answers:** where does the student stand overall?

**7.1 With a root cause.** The overall level is the level stage 6 gave to the root concept: the student stands where the mistake begins, however well the rest is handled.

**7.2 Without a mistake.** The levels of stage 6 are sorted from high to low and the one in the middle is taken: with n levels, the one at position (n − 1) ÷ 2, rounded down and counted from 0. So one weak or one strong concept does not decide for the whole answer.

*One of the outputs at this stage:* 7.2 applies: there is no root cause. The levels from high to low are L3, L2, L2, L2, L2; position (5 − 1) ÷ 2 = 2, counted from 0, is **L2**.

## The final picture

![The labelled graph at the end of the run](figure08.png)
