# Think on the Graph: run MY18

This page explains, stage by stage, how the algorithm reached its result for this scenario. Each stage says what it does, why, and what its terms mean, and then shows two or three of the outputs of that stage from this run. Every output of every stage (all edges offered, all scores and labels, the figures) is in `MY18.ipynb` and `report.html`; the interactive graph is `MY18_G.html`.

## Input

Program:
```java
int[] a = {5, 10, 15};
for (int i = 0; i <= a.length; i++) {
    System.out.println(a[i]);
}
```
**Question.** Explain which indexes the loop visits and why

**Student's answer.** i goes from 0 to a.length. Using <= or < makes no difference here, because both go through the whole array, so it visits each element once.

**What the program really does.** With `i <= a.length` the loop visits the indexes 0, 1, 2 and 3. Index 3 does not exist, so after printing 5, 10, 15 the program stops with ArrayIndexOutOfBoundsException. `<` and `<=` are not the same here.

## Result

- **Wrong rules held:** OffByOneBound at `off_by_one_error`
- **Root cause:** `off_by_one_error` / OffByOneBound
- **Overall level:** L0
- **Level per concept:** `array_traversal` L0, `length_field` L0, `loop_variable` L3, `off_by_one_error` L0

**Check of this result (read by hand, 2026-11-13).** The diagnosis matches the answer.

## The idea

The method is *Think on the Graph*. A language model is not asked "what is wrong with this answer?". Instead the program walks a **knowledge graph** of Java and asks the model only small questions about one edge at a time, each of which must be tied to the student's own words. The graph has three kinds of node: **concept** nodes (for example `integer_division`), **misconception** and **error** nodes (a wrong rule a student may believe, or a rule broken in a program), and five **level** nodes for every concept (L0 to L4). Its edges are: **prerequisite** (A must be understood before B), **parallel** (A and B are learned side by side), **misconception / error** (from a concept to a wrong rule; the edge stores the wrong rule and, as its *twin*, the right rule), and **has_level** (from a concept to one of its levels; the edge stores the *ways* a student can show that level, each with an exact rule).

Two numbers control the walk: the **width N = 3** (how many options survive each choice) and the **depth D = 3** (how many rounds the walk may take). The model here is `claude-opus-5-5`; it is used in stage 3 only.

## Stage 1. From the code to a subgraph G (no model)

This stage reads only the program, never the student's answer. Its job is to decide which part of the knowledge graph this scenario is allowed to use.

**1.1 Prepare the code.** Pasted code often carries look-alike characters (curly quotes, non-breaking spaces); these are mapped to the plain ones. Then the code is **masked**: the inside of every string literal and every comment is replaced by spaces of the same length. Masking matters because the next step matches patterns: the word `for` inside a printed sentence must not count as a for loop. Lengths and line numbers stay the same, so a match can still be reported by line.

*One of the outputs at this stage:* this program has no string literal or comment, so the masked code is the same as the original.

**1.2 Tag concepts.** Every concept node stores a *reader block*: regular expressions that describe how the concept looks in Java, in several *channels* (code patterns, signals, operator symbols, type names). All of them are run over the masked code. Each match is a **hit**: which channel and pattern, the matched text, and the line. A concept with at least one hit is **tagged**. There is nothing learned here; the patterns in the graph are the whole "model".

*Some of the outputs at this stage:*

- `off_by_one_error` is tagged: its signal `loop_past_end` matches `for (int i = 0; i <= a.length` on line 2
- `array_traversal` is tagged: its pattern `\bfor\s*\([^;]*;[^;]*\.length\b` matches `for (int i = 0; i <= a.length` on line 2
- `for_loop` is tagged: its pattern `\bfor\s*\(` matches `for (` on line 2

**1.3 Handle generic concepts.** The graph marks some concepts **generic**: they are so basic (statement, expression, assignment, a literal, `int`) that their pattern fires on almost any line of Java. If all of them were kept, every program would seem to be "about" them and the diagnosis would drift to vague places. So a tagged generic concept is kept only when the code ties it to something specific: the graph has a prerequisite or parallel edge between it and a non-generic tagged concept, or one of its *decisive* signals fired (a pattern that by itself shows the concept is the point of the code). A kept generic concept stays marked generic: the walk can reach it and it can get a level, but it cannot be a starting point by itself, and a wrong-rule label on it is treated as a shadow of a more specific one (stage 4).

*Some of the outputs at this stage:*

- 23 concepts are tagged and kept, 4 of them generic
- `assignment` is generic; it is kept because the code ties it to a specific concept (it matched `=` on line 1)
- `data_type` is generic; it is kept because the code ties it to a specific concept (it matched `int` on line 1)

**1.4 Cut out the subgraph G.** G consists of the kept concepts, the graph's prerequisite and parallel edges whose two ends are both kept, every misconception and error edge of those concepts, and their level nodes with all their ways. From here on the algorithm sees only G, so it can only name wrong rules that belong to concepts the code really contains. The concepts of G fall into **pieces** (groups joined by edges); the graph has no edge between two pieces, so the walk never crosses from one to another.

*Some of the outputs at this stage:*

- G has 23 concept edges, 159 misconception / error edges and 115 level edges, in 2 pieces (sizes 20, 3)
- a concept edge of G: indexing → off_by_one_error (prerequisite): “Indices start at 0, so the last element is a[N-1]; misreading this convention is the usual source of off-by-o…”
- a misconception edge of G: `off_by_one_error` → FencepostExtraSeparator: “Prints item and separator together in the loop, leaving an extra separator at the end.”

## Stage 2. Clauses and start concepts (no model)

**2.1 Split the answer into clauses.** A **clause** is one statement the student makes. The answer is cut at sentence ends, at ';', and before 'because' and 'so' (a reason and its conclusion are separate claims); a remark in parentheses becomes its own clause. The clauses are numbered c1, c2, … This numbering is what keeps the model honest later: every label it gives must name the clause numbers it rests on, so each finding points at words the student actually wrote.

*Some of the outputs at this stage:*

- c1: “i goes from 0 to a.length”
- c2: “Using <= or < makes no difference here”
- c3: “because both go through the whole array”

**2.2 Choose the start concepts.** The walk has to begin somewhere; these are the **start concepts** (in Think on the Graph, the *topic entities*). The candidates are the non-generic concepts of G, plus a generic one when the answer itself repeats the code text that tagged it (for example the student writes `=`). If there are more than N, they are ranked by **BM25**, the standard search-engine score: it compares the words of the answer with the words of a concept's text (its name and the texts of its edges), counting shared words, giving rare words more weight and long texts less. The top N = 3 are the start concepts. No model is used, so the same answer always starts at the same place.

*Some of the outputs at this stage:*

- `array_traversal` scores 22.33, the highest: chosen
- `loop_control` scores 17.93: chosen
- `indexing` scores 14.08, which is 4th of 20: left out

## Stage 3. The traversal: walking G (the model is asked here)

The walk is a **beam search**. "Beam" means that at every choice only the best N = 3 options are followed, so the work stays small even when a concept has dozens of edges. It proceeds in rounds called **depths**, at most D = 3 of them plus one closing round. Throughout, the algorithm keeps four things: the **current concepts** (where it is now), the **paths** (the edges it has kept), the **evidence** (every edge that received a label, kept or not), and the set of edges it has already offered, so nothing is judged twice.

At each depth, for each current concept, the following happens.

**3.1 Edge search (no model).** The edges of the concept are collected as **candidates**. A concept that has just been entered is read *inwards*: its misconception and error edges (the wrong rules a student could hold about it) and its **level ways** (each way of each level is treated as an edge of its own, whose text is the way's exact rule). These are two separate *families*. A concept that has already been read inwards is read *outwards*: its prerequisite and parallel edges to other concepts in the same piece. So depth 1 asks "what does the answer show about these concepts?" and the later depths ask "which neighbouring concepts does that involve?".

*Some of the outputs at this stage:*

- at `array_traversal`, 6 misconception / error edges are offered
- at `array_traversal`, 22 level ways are offered
- at `loop_control`, 11 misconception / error edges are offered

**3.2 Prune (model, first question).** There are usually far more candidates than can be judged carefully, so they are first **pruned**. The model sees the program, the question, the answer and the text of each candidate edge of one family, and returns at most N of them with a relevance score. The scores are rescaled so they add up to 1: this is the **prune score**, the share of relevance the model gives to that edge. Each family is pruned separately, so a level way never pushes out a misconception or the other way round. Edge ids the model invents are ignored.

*Some of the outputs at this stage:*

- at `off_by_one_error` the misconception family is pruned to: OffByOneBound 0.75, WrongIterationCount 0.20, FencepostExtraSeparator 0.05
- at `array_traversal` the misconception family is pruned to: OffByOneBound 0.60, IdiomOverridesCode 0.30, ArrayUseScansAllCells 0.10
- at `array_traversal` the level ways family is pruned to: L0 way “everyday reading” 0.50, L4 way “diagnose an error” 0.30, L3 way “relation to neighbour” 0.20

**3.3 Label (model, second question).** Each edge that survived is now read against the numbered clauses and gets a **label**. For a misconception or error edge: **held** (the student's words state this wrong rule), **correct** (they state the right rule, its twin) or **not applied** (the answer says nothing about it). For a level way: **shown** or not applied. For a prerequisite or parallel edge: **confirmed** (the answer carries the rule from one concept into the other) or **broken** (it fails to). The misconception edges of one concept are judged together in a single question, because the same sentence can fit several wrong rules and the model should give *held* only to the one the student really claims. With the label the model must return the **clause numbers** it rests on and a **confidence** from 0 to 1. A label with no clause is discarded. This is the safeguard of the method: the model never diagnoses from its own knowledge; every label is attached to one edge of G and to the student's words.

*Some of the outputs at this stage:*

- OffByOneBound at `off_by_one_error` is labelled **held** on clauses 1, 2, 3, 4 with confidence 0.95. The rule on that edge: “< vs <= and 0..n vs 0..n-1 are interchangeable”
- LoopOutputSameEachPass at `loop_variable` is labelled **correct** on clauses 1, 4 with confidence 0.60. The rule on that edge: “A loop prints the same thing on every pass; the changing loop variable does not affect what the body does.”
- L0 way “everyday reading” at `array_traversal` is labelled **shown** on clauses 2, 3, 4 with confidence 0.90. The rule on that edge: “Folk meaning: 'go through the list' in English means look at every item once, first to last, so an array loop is assume…”

**3.4 Score and keep.** The **score** of a labelled edge is prune score × confidence: an edge counts for much only if it was both relevant and confidently labelled. The edges are then ranked in **tiers**. Tier 0 is a held misconception or a broken edge: these are findings about a fault and are always kept. Tier 1 is a held error. Tier 2 is everything that only confirms understanding (correct, confirmed, shown); these fill whatever is left of the N = 3 places, best score first. Kept edges are added to the paths. Every labelled edge, kept or not, is added to the evidence, because the levels in stage 6 are read from all of it.

*Some of the outputs at this stage:*

- the score of OffByOneBound at `off_by_one_error` is 0.75 × 0.95 = 0.71
- the score of LoopOutputSameEachPass at `loop_variable` is 0.40 × 0.60 = 0.24
- kept at depth 1: OffByOneBound (held, tier 0, 0.57); OffByOneBound (held, tier 0, 0.55); IdiomOverridesCode (held, tier 0, 0.54); IdiomOverridesCode (held, tier 0, 0.19)

**3.5 Move to the next concepts.** Three things decide where the walk goes next. A kept prerequisite or parallel edge leads to the concept at its other end; that concept is **entered** and will be read inwards at the next depth, so it gets misconceptions and a level of its own. A concept with a held misconception stays current, so that its prerequisites are examined: the fault may begin further back. And any entered concept whose outward edges have not been read yet stays current until they are.

*Some of the outputs at this stage:*

- the kept edge loop_control → off_by_one_error leads to a new concept, entered next: `off_by_one_error`
- the kept edge length_field → array_traversal leads to a new concept, entered next: `length_field`
- the kept edge loop_variable → loop_control leads to a new concept, entered next: `loop_variable`

**3.6 Stop test (no model).** After each depth two checks are made. The **graph check**: has every entered concept had both its inward and its outward edges read? The **clause coverage** check: is every clause covered by at least one labelled rule edge (a level way does not count here, since it describes how the student reads the code, not which rule a clause applies)? If both hold, the walk stops as *sufficient*. If some clauses are still uncovered, they are matched by BM25 against the concepts not visited yet and the best N are entered. Otherwise the walk continues to depth D = 3, followed by one **closing round** in which the concepts entered last have their inward edges read, so that no concept is left half-read. The model's replies are cached by the exact text of the question, so running the same scenario again gives the same result without asking again.

*Some of the outputs at this stage:*

- after depth 3: 4 of 4 clauses covered
- after depth 4: 4 of 4 clauses covered
- the walk stopped at depth 4 because the depth limit was reached; the model was asked 20 prune questions and 40 label questions in all

## Stage 4. From labels to faults (rules, no model)

The walk leaves a set of labelled edges. Each kept edge labelled *held* is a candidate **fault**, but one wrong sentence usually lights up several edges, so fixed rules remove the double counting. Nothing is deleted from the record; the rules only decide what counts as a fault.

- **Error beside a misconception.** An error node describes a consequence in a program; a misconception describes the belief behind it. A held error on a concept that also has a held misconception is therefore kept as evidence, not as a second fault.
- **One fault, one place.** The graph can attach the same misconception to two concepts joined by a prerequisite edge. On each such edge the graph gives the concept a **role**: *primary* (the concept whose rule the misconception violates) or *context* (a concept where it also shows up). If the misconception is held at both ends, it is filed once, at the primary concept, or at the dependent concept when the roles do not decide.
- **Shadows.** A held label is a **shadow** when it sits on a prerequisite or on a generic concept and rests only on clauses that a stronger, more specific label already rests on. It is the same wrong sentence read a second time at a vaguer place. A shadow is kept in the record but is not a fault, cannot be the root cause and does not set a level.
- **Broken edges.** A prerequisite edge A → B labelled *broken* says the student did not carry the rule of A into B, so the fault sits at B. If the broken edge rests on the same clauses as a held misconception, it is that misconception's **consequence**, not a separate fault.

*Some of the outputs at this stage:*

- fault: **OffByOneBound** at `off_by_one_error`. Wrong rule: “< vs <= and 0..n vs 0..n-1 are interchangeable” Its twin, the right rule: “for (i = 0; i < n; i++) runs n times with i going up to n - 1; with <= it runs n + 1 times and reaches i = n.”
- shadow: OffByOneBound at `array_traversal` is a shadow of OffByOneBound (5 shadows in all)
- broken edge: loop_control → off_by_one_error, a consequence of OffByOneBound (5 broken edges in all)

## Stage 5. Root cause (rule, no model)

Several concepts may carry a fault, and the **root cause** is the one to teach first. The rule uses the prerequisite edges of G. From each faulty concept it walks backwards (from a concept to what it depends on). Whenever a concept reached that way also has a fault of its own, the candidate moves back to it, because a fault in what a concept depends on explains the fault in the concept. Among the candidates found, the root is the one with the fewest prerequisites of its own in G, that is, the one furthest back; at a tie, the one whose label the model gave the higher confidence. Alphabetical order never decides.

*Some of the outputs at this stage:*

- `off_by_one_error` has a fault (confidence 0.95); its prerequisites in G: `indexing`, `loop_control`
- the root is `off_by_one_error` with OffByOneBound: it is the only faulty concept and none of its prerequisites has a fault

## Stage 6. Level of each concept (rule, no model)

Every concept has five **levels**, taken from the SOLO taxonomy: **L0** prestructural (the answer holds a rule that contradicts Java, or reads the code in an everyday sense), **L1** unistructural (it states one correct rule without applying it), **L2** multistructural (it applies the rules to the code step by step), **L3** relational (it relates the parts to each other and to the purpose of the whole), **L4** extended abstract (it reasons beyond the given code: predicts a change, transfers, diagnoses). Each level has **ways**, concrete things a student does at that level, such as "output prediction" at L2 or "predict a change" at L4.

The model is never asked for a level. In stage 3 it only said whether a way was *shown*; the level is read from where that way sits in the graph. The rule: a concept is **L0** if a fault is kept on it, or if the only ways shown on it are L0 ways. Otherwise it gets the **highest** level among the ways shown, because the levels build on each other (an answer that relates the parts has also applied the rules). A concept with no fault and no way shown gets no level.

*Some of the outputs at this stage:*

- `off_by_one_error` keeps OffByOneBound, so it is L0
- on `length_field` the ways shown are L0 “inconsistent trace”, L0 “everyday reading”, so it is L0
- on `loop_variable` the ways shown are L0 “everyday reading”, L2 “output prediction”, L3 “relation to neighbour”, so it is L3

## Stage 7. Overall level (rule, no model)

One level is reported for the whole answer. If there is a root cause, it is the level of the root concept: the student stands where the fault begins, however well the rest is handled. If there is no fault, it is the level reached on at least half of the concepts the answer touched (the levels are sorted from high to low and the middle one is taken), so that a single weaker concept does not pull the whole answer down and a single strong one does not lift it.

*The output of this stage:* the root is `off_by_one_error` and its level is L0, so the overall level is **L0**.

## The final picture

![The labelled graph at the end of the run](figure08.png)
