# Think on the Graph: run MY26

This page explains, stage by stage, how the algorithm reached its result for this scenario. Each stage says what it does, why, and what its terms mean, and then shows two or three of the outputs of that stage from this run. Every output of every stage (all edges offered, all scores and labels, the figures) is in `MY26.ipynb` and `report.html`; the interactive graph is `MY26_G.html`.

## Input

Program:
```java
int total = 50;
int count = 0;
System.out.println(total / count);
```
**Question.** Will this compile? What happens when you run it? Explain your reasoning

**Student's answer.** It won’t compile. Dividing by zero isn’t allowed, so the compiler stops you before it runs.” Actual: it compiles, then crashes at run time with ArithmeticException: / by zero.

**What the program really does.** The program compiles: count is a variable, so the compiler does not know its value. When it runs, the integer division 50 / 0 throws ArithmeticException: / by zero, and nothing is printed.

## Result

- **Wrong rules held:** DivisionByZeroIsCompileError at `division_by_zero`
- **Root cause:** `division_by_zero` / DivisionByZeroIsCompileError
- **Overall level:** L0
- **Level per concept:** `division_by_zero` L0, `integer_division` L4, `run_time_error` L0

**Check of this result (read by hand, 2026-11-13).** The diagnosis matches the answer. One flaw in the input: the line beginning 'Actual:' was pasted into the answer box, so it was read as part of the student's answer and is listed as an unexplained clause.

## The idea

The method is *Think on the Graph*. A language model is not asked "what is wrong with this answer?". Instead the program walks a **knowledge graph** of Java and asks the model only small questions about one edge at a time, each of which must be tied to the student's own words. The graph has three kinds of node: **concept** nodes (for example `integer_division`), **misconception** and **error** nodes (a wrong rule a student may believe, or a rule broken in a program), and five **level** nodes for every concept (L0 to L4). Its edges are: **prerequisite** (A must be understood before B), **parallel** (A and B are learned side by side), **misconception / error** (from a concept to a wrong rule; the edge stores the wrong rule and, as its *twin*, the right rule), and **has_level** (from a concept to one of its levels; the edge stores the *ways* a student can show that level, each with an exact rule).

Two numbers control the walk: the **width N = 3** (how many options survive each choice) and the **depth D = 3** (how many rounds the walk may take). The model here is `claude-opus-5-5`; it is used in stage 3 only.

## Stage 1. From the code to a subgraph G (no model)

This stage reads only the program, never the student's answer. Its job is to decide which part of the knowledge graph this scenario is allowed to use.

**1.1 Prepare the code.** Pasted code often carries look-alike characters (curly quotes, non-breaking spaces); these are mapped to the plain ones. Then the code is **masked**: the inside of every string literal and every comment is replaced by spaces of the same length. Masking matters because the next step matches patterns: the word `for` inside a printed sentence must not count as a for loop. Lengths and line numbers stay the same, so a match can still be reported by line.

*One of the outputs at this stage:* this program has no string literal or comment, so the masked code is the same as the original.

**1.2 Tag concepts.** Every concept node stores a *reader block*: regular expressions that describe how the concept looks in Java, in several *channels* (code patterns, signals, operator symbols, type names). All of them are run over the masked code. Each match is a **hit**: which channel and pattern, the matched text, and the line. A concept with at least one hit is **tagged**. There is nothing learned here; the patterns in the graph are the whole "model".

*Some of the outputs at this stage:*

- `division_by_zero` is tagged: its signal `zero_divisor_in_variable` matches `int count = 0; System.out.println(total…` on line 2
- `integer_division` is tagged: its signal `int_vars_two_decls_div` matches `int total = 50; int count = 0; System.o…` on line 1
- `println` is tagged: its pattern `System\.out\.println\s*\(` matches `System.out.println(` on line 3

**1.3 Handle generic concepts.** The graph marks some concepts **generic**: they are so basic (statement, expression, assignment, a literal, `int`) that their pattern fires on almost any line of Java. If all of them were kept, every program would seem to be "about" them and the diagnosis would drift to vague places. So a tagged generic concept is kept only when the code ties it to something specific: the graph has a prerequisite or parallel edge between it and a non-generic tagged concept, or one of its *decisive* signals fired (a pattern that by itself shows the concept is the point of the code). A kept generic concept stays marked generic: the walk can reach it and it can get a level, but it cannot be a starting point by itself, and a wrong-rule label on it is treated as a shadow of a more specific one (stage 4).

*Some of the outputs at this stage:*

- 7 concepts are tagged and kept, 2 of them generic
- `expression` is generic; it is kept because the code ties it to a specific concept (it matched `l /` on line 3)
- `statement` is generic; it is kept because the code ties it to a specific concept (it matched `;` on line 1)

**1.4 Cut out the subgraph G.** G consists of the kept concepts, the graph's prerequisite and parallel edges whose two ends are both kept, every misconception and error edge of those concepts, and their level nodes with all their ways. From here on the algorithm sees only G, so it can only name wrong rules that belong to concepts the code really contains. The concepts of G fall into **pieces** (groups joined by edges); the graph has no edge between two pieces, so the walk never crosses from one to another.

*Some of the outputs at this stage:*

- G has 5 concept edges, 38 misconception / error edges and 35 level edges, in 2 pieces (sizes 5, 2)
- a concept edge of G: arithmetic_operators → division_by_zero (prerequisite): “Integer division by zero (1/0) generates a run-time exception, while floating-point 1.0/0.0 is legal and has…”
- a misconception edge of G: `division_by_zero` → AverageWithoutZeroGuard: “Computes sum / count without checking that count is above 0.”

## Stage 2. Clauses and start concepts (no model)

**2.1 Split the answer into clauses.** A **clause** is one statement the student makes. The answer is cut at sentence ends, at ';', and before 'because' and 'so' (a reason and its conclusion are separate claims); a remark in parentheses becomes its own clause. The clauses are numbered c1, c2, … This numbering is what keeps the model honest later: every label it gives must name the clause numbers it rests on, so each finding points at words the student actually wrote.

*Some of the outputs at this stage:*

- c1: “It wont compile”
- c2: “Dividing by zero isnt allowed”
- c3: “so the compiler stops you before it runs”

**2.2 Choose the start concepts.** The walk has to begin somewhere; these are the **start concepts** (in Think on the Graph, the *topic entities*). The candidates are the non-generic concepts of G, plus a generic one when the answer itself repeats the code text that tagged it (for example the student writes `=`). If there are more than N, they are ranked by **BM25**, the standard search-engine score: it compares the words of the answer with the words of a concept's text (its name and the texts of its edges), counting shared words, giving rare words more weight and long texts less. The top N = 3 are the start concepts. No model is used, so the same answer always starts at the same place.

*Some of the outputs at this stage:*

- `division_by_zero` scores 17.10, the highest: chosen
- `run_time_error` scores 15.59: chosen
- `integer_division` scores 5.84, which is 4th of 5: left out

## Stage 3. The traversal: walking G (the model is asked here)

The walk is a **beam search**. "Beam" means that at every choice only the best N = 3 options are followed, so the work stays small even when a concept has dozens of edges. It proceeds in rounds called **depths**, at most D = 3 of them plus one closing round. Throughout, the algorithm keeps four things: the **current concepts** (where it is now), the **paths** (the edges it has kept), the **evidence** (every edge that received a label, kept or not), and the set of edges it has already offered, so nothing is judged twice.

At each depth, for each current concept, the following happens.

**3.1 Edge search (no model).** The edges of the concept are collected as **candidates**. A concept that has just been entered is read *inwards*: its misconception and error edges (the wrong rules a student could hold about it) and its **level ways** (each way of each level is treated as an edge of its own, whose text is the way's exact rule). These are two separate *families*. A concept that has already been read inwards is read *outwards*: its prerequisite and parallel edges to other concepts in the same piece. So depth 1 asks "what does the answer show about these concepts?" and the later depths ask "which neighbouring concepts does that involve?".

*Some of the outputs at this stage:*

- at `division_by_zero`, 3 misconception / error edges are offered
- at `division_by_zero`, 15 level ways are offered
- at `run_time_error`, 7 misconception / error edges are offered

**3.2 Prune (model, first question).** There are usually far more candidates than can be judged carefully, so they are first **pruned**. The model sees the program, the question, the answer and the text of each candidate edge of one family, and returns at most N of them with a relevance score. The scores are rescaled so they add up to 1: this is the **prune score**, the share of relevance the model gives to that edge. Each family is pruned separately, so a level way never pushes out a misconception or the other way round. Edge ids the model invents are ignored.

*Some of the outputs at this stage:*

- at `division_by_zero` the misconception family is pruned to: DivisionByZeroIsCompileError 0.80, ZeroDivisionAlwaysCrashes 0.15, AverageWithoutZeroGuard 0.05
- at `division_by_zero` the level ways family is pruned to: L0 way “everyday reading” 0.70, L4 way “diagnose an error” 0.15, L2 way “output prediction” 0.15
- at `run_time_error` the misconception family is pruned to: DivisionByZeroIsCompileError 0.80, CompilesMeansWorks 0.15, NegativeArraySize 0.05

**3.3 Label (model, second question).** Each edge that survived is now read against the numbered clauses and gets a **label**. For a misconception or error edge: **held** (the student's words state this wrong rule), **correct** (they state the right rule, its twin) or **not applied** (the answer says nothing about it). For a level way: **shown** or not applied. For a prerequisite or parallel edge: **confirmed** (the answer carries the rule from one concept into the other) or **broken** (it fails to). The misconception edges of one concept are judged together in a single question, because the same sentence can fit several wrong rules and the model should give *held* only to the one the student really claims. With the label the model must return the **clause numbers** it rests on and a **confidence** from 0 to 1. A label with no clause is discarded. This is the safeguard of the method: the model never diagnoses from its own knowledge; every label is attached to one edge of G and to the student's words.

*Some of the outputs at this stage:*

- DivisionByZeroIsCompileError at `division_by_zero` is labelled **held** on clauses 1, 2, 3 with confidence 0.95. The rule on that edge: “System.out.println(5 / 0); is rejected by the compiler.”
- L0 way “everyday reading” at `division_by_zero` is labelled **shown** on clauses 1, 2, 3 with confidence 0.93. The rule on that edge: “Folk meaning: in maths division by zero is 'impossible', so every x / 0 must be rejected, ideally by the compiler. Java…”
- division_by_zero → run_time_error at `division_by_zero` is labelled **broken** on clauses 1, 3 with confidence 0.95. The rule on that edge: “Dividing an int by zero compiles but throws ArithmeticException when the program runs: a run-time error.”

**3.4 Score and keep.** The **score** of a labelled edge is prune score × confidence: an edge counts for much only if it was both relevant and confidently labelled. The edges are then ranked in **tiers**. Tier 0 is a held misconception or a broken edge: these are findings about a fault and are always kept. Tier 1 is a held error. Tier 2 is everything that only confirms understanding (correct, confirmed, shown); these fill whatever is left of the N = 3 places, best score first. Kept edges are added to the paths. Every labelled edge, kept or not, is added to the evidence, because the levels in stage 6 are read from all of it.

*Some of the outputs at this stage:*

- the score of DivisionByZeroIsCompileError at `division_by_zero` is 0.80 × 0.95 = 0.76
- the score of L0 way “everyday reading” at `division_by_zero` is 0.70 × 0.93 = 0.65
- kept at depth 1: DivisionByZeroIsCompileError (held, tier 0, 0.76); DivisionByZeroIsCompileError (held, tier 0, 0.76); L0 way “everyday reading” (shown, tier 2, 0.65)

**3.5 Move to the next concepts.** Three things decide where the walk goes next. A kept prerequisite or parallel edge leads to the concept at its other end; that concept is **entered** and will be read inwards at the next depth, so it gets misconceptions and a level of its own. A concept with a held misconception stays current, so that its prerequisites are examined: the fault may begin further back. And any entered concept whose outward edges have not been read yet stays current until they are.

*One of the outputs at this stage:* uncovered clauses bring in: arithmetic_operators (4.12), integer_division (2.02)

**3.6 Stop test (no model).** After each depth two checks are made. The **graph check**: has every entered concept had both its inward and its outward edges read? The **clause coverage** check: is every clause covered by at least one labelled rule edge (a level way does not count here, since it describes how the student reads the code, not which rule a clause applies)? If both hold, the walk stops as *sufficient*. If some clauses are still uncovered, they are matched by BM25 against the concepts not visited yet and the best N are entered. Otherwise the walk continues to depth D = 3, followed by one **closing round** in which the concepts entered last have their inward edges read, so that no concept is left half-read. The model's replies are cached by the exact text of the question, so running the same scenario again gives the same result without asking again.

*Some of the outputs at this stage:*

- after depth 2: 3 of 4 clauses covered
- after depth 3: 3 of 4 clauses covered
- the walk stopped at depth 3 because no concept was left to go to; the model was asked 13 prune questions and 23 label questions in all

## Stage 4. From labels to faults (rules, no model)

The walk leaves a set of labelled edges. Each kept edge labelled *held* is a candidate **fault**, but one wrong sentence usually lights up several edges, so fixed rules remove the double counting. Nothing is deleted from the record; the rules only decide what counts as a fault.

- **Error beside a misconception.** An error node describes a consequence in a program; a misconception describes the belief behind it. A held error on a concept that also has a held misconception is therefore kept as evidence, not as a second fault.
- **One fault, one place.** The graph can attach the same misconception to two concepts joined by a prerequisite edge. On each such edge the graph gives the concept a **role**: *primary* (the concept whose rule the misconception violates) or *context* (a concept where it also shows up). If the misconception is held at both ends, it is filed once, at the primary concept, or at the dependent concept when the roles do not decide.
- **Shadows.** A held label is a **shadow** when it sits on a prerequisite or on a generic concept and rests only on clauses that a stronger, more specific label already rests on. It is the same wrong sentence read a second time at a vaguer place. A shadow is kept in the record but is not a fault, cannot be the root cause and does not set a level.
- **Broken edges.** A prerequisite edge A → B labelled *broken* says the student did not carry the rule of A into B, so the fault sits at B. If the broken edge rests on the same clauses as a held misconception, it is that misconception's **consequence**, not a separate fault.

*Some of the outputs at this stage:*

- fault: **DivisionByZeroIsCompileError** at `division_by_zero`. Wrong rule: “System.out.println(5 / 0); is rejected by the compiler.” Its twin, the right rule: “It compiles; the ArithmeticException happens when the program runs.”
- shadow: DivisionByZeroIsCompileError at `run_time_error` is a shadow of DivisionByZeroIsCompileError
- broken edge: division_by_zero → run_time_error, a consequence of DivisionByZeroIsCompileError (2 broken edges in all)

## Stage 5. Root cause (rule, no model)

Several concepts may carry a fault, and the **root cause** is the one to teach first. The rule uses the prerequisite edges of G. From each faulty concept it walks backwards (from a concept to what it depends on). Whenever a concept reached that way also has a fault of its own, the candidate moves back to it, because a fault in what a concept depends on explains the fault in the concept. Among the candidates found, the root is the one with the fewest prerequisites of its own in G, that is, the one furthest back; at a tie, the one whose label the model gave the higher confidence. Alphabetical order never decides.

*Some of the outputs at this stage:*

- `division_by_zero` has a fault (confidence 0.95); its prerequisites in G: `arithmetic_operators`
- the root is `division_by_zero` with DivisionByZeroIsCompileError: it is the only faulty concept and none of its prerequisites has a fault

## Stage 6. Level of each concept (rule, no model)

Every concept has five **levels**, taken from the SOLO taxonomy: **L0** prestructural (the answer holds a rule that contradicts Java, or reads the code in an everyday sense), **L1** unistructural (it states one correct rule without applying it), **L2** multistructural (it applies the rules to the code step by step), **L3** relational (it relates the parts to each other and to the purpose of the whole), **L4** extended abstract (it reasons beyond the given code: predicts a change, transfers, diagnoses). Each level has **ways**, concrete things a student does at that level, such as "output prediction" at L2 or "predict a change" at L4.

The model is never asked for a level. In stage 3 it only said whether a way was *shown*; the level is read from where that way sits in the graph. The rule: a concept is **L0** if a fault is kept on it, or if the only ways shown on it are L0 ways. Otherwise it gets the **highest** level among the ways shown, because the levels build on each other (an answer that relates the parts has also applied the rules). A concept with no fault and no way shown gets no level.

*Some of the outputs at this stage:*

- `division_by_zero` keeps DivisionByZeroIsCompileError, so it is L0
- on `run_time_error` the ways shown are L0 “everyday reading”, so it is L0
- on `integer_division` the ways shown are L4 “diagnose an error”, so it is L4

## Stage 7. Overall level (rule, no model)

One level is reported for the whole answer. If there is a root cause, it is the level of the root concept: the student stands where the fault begins, however well the rest is handled. If there is no fault, it is the level reached on at least half of the concepts the answer touched (the levels are sorted from high to low and the middle one is taken), so that a single weaker concept does not pull the whole answer down and a single strong one does not lift it.

*The output of this stage:* the root is `division_by_zero` and its level is L0, so the overall level is **L0**.

Clauses that no edge covered: “Actual: it compiles, then crashes at run time with ArithmeticException: / by zero”.

## The final picture

![The labelled graph at the end of the run](figure07.png)
