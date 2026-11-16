# Think on the Graph: run MY14

This page explains, stage by stage, how the algorithm reached its result for this scenario. Each stage says what it does, why, and what its terms mean, and then shows one of the outputs of that stage from this run. Every output of every stage (all edges offered, all scores and labels, the figures) is in `MY14.ipynb` and `report.html`; the interactive graph is `MY14_G.html`.

## Input

Program:
```java
for (int i = 0; i < 10; i += 3) {
    System.out.println(i);
}
```
**Question.** Explain how i changes from one pass of the loop to the next.

**Student's answer.** A for loop moves i on by one each pass, so i goes 0, 1, 2 and so on up to 9.

**What the program really does.** The update is `i += 3`, so i goes 0, 3, 6, 9 and those four values are printed. Then i is 12, the condition `i < 10` is false and the loop ends.

## Result

- **Wrong rules held:** LoopStepAlwaysOne at `for_loop`
- **Root cause:** `for_loop` / LoopStepAlwaysOne
- **Overall level:** L0
- **Level per concept:** `for_loop` L0, `loop_variable` L2

**Check of this result (read by hand, 2026-11-13).** The diagnosis matches the answer.

## The idea

The method is *Think on the Graph*. A language model is not asked "what is wrong with this answer?". Instead the program walks a **knowledge graph** of Java and asks the model only small questions about one edge at a time, each of which must be tied to the student's own words. The graph has three kinds of node: **concept** nodes (for example `integer_division`), **misconception** and **error** nodes (a wrong rule a student may believe, or a rule broken in a program), and five **level** nodes for every concept (L0 to L4). Its edges are: **prerequisite** (A must be understood before B), **parallel** (A and B are learned side by side), **misconception / error** (from a concept to a wrong rule; the edge stores the wrong rule and, as its *twin*, the right rule), and **has_level** (from a concept to one of its levels; the edge stores the *ways* a student can show that level, each with an exact rule).

Two numbers control the walk: the **width N = 3** (how many options survive each choice) and the **depth D = 3** (how many rounds the walk may take). The model here is `claude-opus-5-5`; it is used in stage 3 only.

## Stage 1. From the code to a subgraph G (no model)

This stage reads only the program, never the student's answer. Its job is to decide which part of the knowledge graph this scenario is allowed to use.

**1.1 Mask the code.** The code is **masked**: the inside of every string literal and every comment is replaced by spaces of the same length. Masking matters because the next step matches patterns: the word `for` inside a printed sentence must not count as a for loop. Lengths and line numbers stay the same, so a match can still be reported by line.

*One of the outputs at this stage:* this program has no string literal or comment, so the masked code equals the original.

**1.2 Tag concepts.** Every concept node stores a *reader block*: regular expressions that describe how the concept looks in Java, in several *channels* (code patterns, signals, operator symbols, type names). All of them are run over the masked code. Each match is a **hit**: which channel and pattern, the matched text, and the line. A concept with at least one hit is **tagged**. There is nothing learned here; the patterns in the graph are the whole "model".

*One of the outputs at this stage:* `for_loop` is tagged: its pattern `\bfor\s*\(` matches `for (` on line 1.

**1.3 Handle generic concepts.** The graph marks some concepts **generic**: they are so basic (statement, expression, assignment, a literal, `int`) that their pattern fires on almost any line of Java. If all of them were kept, every program would seem to be "about" them and the diagnosis would drift to vague places. So a tagged generic concept is kept only when the code ties it to something specific: the graph has a prerequisite or parallel edge between it and a non-generic tagged concept, or one of its *decisive* signals fired (a pattern that by itself shows the concept is the point of the code). A kept generic concept stays marked generic: the walk can reach it and it can get a level, but it cannot be a starting point by itself, and a wrong-rule label on it is treated as a shadow of a more specific one (stage 4).

*One of the outputs at this stage:* 14 concepts are tagged and kept, 3 of them generic (`assignment`, `expression`, `statement`).

**1.4 Cut out the subgraph G.** G consists of the kept concepts, the graph's prerequisite and parallel edges whose two ends are both kept, every misconception and error edge of those concepts, and their level nodes with all their ways. From here on the algorithm sees only G, so it can only name wrong rules that belong to concepts the code really contains. The concepts of G fall into **pieces** (groups joined by edges); the graph has no edge between two pieces, so the walk never crosses from one to another.

*One of the outputs at this stage:* G has 12 concept edges, 123 misconception / error edges and 70 level edges, in 2 pieces (sizes 11, 3).

## Stage 2. Clauses and start concepts (no model)

**2.1 Split the answer into clauses.** A **clause** is one statement the student makes. The answer is cut at sentence ends, at ';', and before 'because' and 'so' (a reason and its conclusion are separate claims); a remark in parentheses becomes its own clause. The clauses are numbered c1, c2, … This numbering is what keeps the model honest later: every label it gives must name the clause numbers it rests on, so each finding points at words the student actually wrote.

*One of the outputs at this stage:* 3 clauses. c1: “A for loop moves i on by one each pass” c2: “so i goes 0, 1, 2 and” …

**2.2 Choose the start concepts.** The walk has to begin somewhere; these are the **start concepts** (in Think on the Graph, the *topic entities*). The candidates are the non-generic concepts of G, plus a generic one when the answer itself repeats the code text that tagged it (for example the student writes `=`). If there are more than N, they are ranked by **BM25**, the standard search-engine score: it compares the words of the answer with the words of a concept's text (its name and the texts of its edges), counting shared words, giving rare words more weight and long texts less. The top N = 3 are the start concepts. No model is used, so the same answer always starts at the same place.

*One of the outputs at this stage:* `loop_control` scores 17.13, the highest of 11 candidates; `compound_assignment` is 4th with 7.78 and is left out. Start concepts: `loop_control`, `for_loop`, `loop_variable`.

## Stage 3. The traversal: walking G (the model is asked here)

The walk is a **beam search**. "Beam" means that at every choice only the best N = 3 options are followed, so the work stays small even when a concept has dozens of edges. It proceeds in rounds called **depths**, at most D = 3 of them plus one closing round. Throughout, the algorithm keeps four things: the **current concepts** (where it is now), the **paths** (the edges it has kept), the **evidence** (every edge that received a label, kept or not), and the set of edges it has already offered, so nothing is judged twice.

At each depth, for each current concept, the following happens.

**3.1 Edge search (no model).** The edges of the concept are collected as **candidates**. A concept that has just been entered is read *inwards*: its misconception and error edges (the wrong rules a student could hold about it) and its **level ways** (each way of each level is treated as an edge of its own, whose text is the way's exact rule). These are two separate *families*. A concept that has already been read inwards is read *outwards*: its prerequisite and parallel edges to other concepts in the same piece. So depth 1 asks "what does the answer show about these concepts?" and the later depths ask "which neighbouring concepts does that involve?".

*One of the outputs at this stage:* at `for_loop`, 21 misconception / error edges and 24 level ways are offered when it is entered, and 2 concept edges when it is read outwards.

**3.2 Prune (model, first question).** There are usually far more candidates than can be judged carefully, so they are first **pruned**. The model sees the program, the question, the answer and the text of each candidate edge of one family, and returns at most N of them with a relevance score. The scores are rescaled so they add up to 1: this is the **prune score**, the share of relevance the model gives to that edge. Each family is pruned separately, so a level way never pushes out a misconception or the other way round. Edge ids the model invents are ignored.

*One of the outputs at this stage:* at `for_loop` the misconception family is pruned to: LoopStepAlwaysOne 0.60, IdiomOverridesCode 0.25, WrongIterationCount 0.15.

**3.3 Label (model, second question).** Each edge that survived is now read against the numbered clauses and gets a **label**. For a misconception or error edge: **held** (the student's words state this wrong rule), **correct** (they state the right rule, its twin) or **not applied** (the answer says nothing about it). For a level way: **shown** or not applied. For a prerequisite or parallel edge: **confirmed** (the answer carries the rule from one concept into the other) or **broken** (it fails to). The misconception edges of one concept are judged together in a single question, because the same sentence can fit several wrong rules and the model should give *held* only to the one the student really claims. With the label the model must return the **clause numbers** it rests on and a **confidence** from 0 to 1. A label with no clause is discarded. This is the safeguard of the method: the model never diagnoses from its own knowledge; every label is attached to one edge of G and to the student's words.

*One of the outputs at this stage:* LoopStepAlwaysOne at `for_loop` is labelled **held** on clauses 1, 2, 3 (“A for loop moves i on by one each pass; so i goes 0, 1, 2 and; so on up to 9”) with confidence 0.95. The rule on that edge: “A loop variable always goes up or down by 1, whatever the update says (so i = i - 4 is read as i--).”

**3.4 Score and keep.** The **score** of a labelled edge is prune score × confidence: an edge counts for much only if it was both relevant and confidently labelled. The edges are then ranked in **tiers**. Tier 0 is a held misconception or a broken edge: these are findings about a fault and are always kept. Tier 1 is a held error. Tier 2 is everything that only confirms understanding (correct, confirmed, shown); these fill whatever is left of the N = 3 places, best score first. Kept edges are added to the paths. Every labelled edge, kept or not, is added to the evidence, because the levels in stage 6 are read from all of it.

*One of the outputs at this stage:* the score of LoopStepAlwaysOne is 0.60 × 0.95 = 0.57. At depth 1 the kept edges are: LoopStepAlwaysOne (held, tier 0, 0.57); LoopStepAlwaysOne (held, tier 0, 0.57); WrongIterationCount (held, tier 1, 0.09).

**3.5 Move to the next concepts.** Three things decide where the walk goes next. A kept prerequisite or parallel edge leads to the concept at its other end; that concept is **entered** and will be read inwards at the next depth, so it gets misconceptions and a level of its own. A concept with a held misconception stays current, so that its prerequisites are examined: the fault may begin further back. And any entered concept whose outward edges have not been read yet stays current until they are.

*One of the outputs at this stage:* no kept edge led to a concept that had not been entered already.

**3.6 Stop test (no model).** After each depth two checks are made. The **graph check**: has every entered concept had both its inward and its outward edges read? The **clause coverage** check: is every clause covered by at least one labelled rule edge (a level way does not count here, since it describes how the student reads the code, not which rule a clause applies)? If both hold, the walk stops as *sufficient*. If some clauses are still uncovered, they are matched by BM25 against the concepts not visited yet and the best N are entered. Otherwise the walk continues to depth D = 3, followed by one **closing round** in which the concepts entered last have their inward edges read, so that no concept is left half-read. The model's replies are cached by the exact text of the question, so running the same scenario again gives the same result without asking again.

*One of the outputs at this stage:* the walk stopped at depth 2 because every clause was covered and no entered concept had an unread edge. At the end 3 of 3 clauses were covered. The model was asked 8 prune questions and 16 label questions in all.

## Stage 4. Counting each mistake once (rules, no model)

**What this stage answers:** how many mistakes did the student really make, and at which concept does each one belong?

**Why it is needed.** Stage 3 checks every concept on its own. So one wrong sentence of the student is usually flagged several times: at the concept it is really about, and again at related concepts. A flag here means an edge that stage 3 labelled *held* (the student follows that wrong rule) or *broken* (the student did not carry a rule from one concept to the next). Stage 4 goes through the flags with fixed rules and decides which ones count as a **mistake**. Nothing is deleted: a flag that is not counted stays in the record, marked as a repeat.

| What stage 3 flagged | What stage 4 does with it |
|---|---|
| The same wrong rule at two linked concepts | Counts it once, at the concept the wrong rule is really about |
| A wrong rule at a more basic or more general concept, shown by the same words as a more specific one | Treats it as a repeat of the specific one (the output calls it a **shadow**) |
| A wrong belief, and beside it an error node (the visible result of that belief in a program) | Counts the belief; the error is kept as evidence for it |
| A broken link between two concepts, shown by the same words as a wrong belief | Treats it as a result of that belief (a **consequence**), not as a second mistake |
| A broken link with words of its own | Counts it as a mistake at the concept the link leads to |

**In this run.** One mistake is counted:

- **LoopStepAlwaysOne** at `for_loop`. The student's words: “A for loop moves i on by one each pass; so i goes 0, 1, 2 and; so on up to 9”. The wrong rule in the graph: “A loop variable always goes up or down by 1, whatever the update says (so i = i - 4 is read as i--).” The right rule: “The loop variable changes exactly as the update expression says (i += 2, i = i - 4, i *= 2, ...).”

Flagged by stage 3 but not counted a second time:

- LoopStepAlwaysOne at `loop_control` (a repeat of LoopStepAlwaysOne, shown by the same words)
- WrongIterationCount at `loop_control` (an error node, kept as evidence)
- 2 broken links (loop_variable → loop_control, loop_control → for_loop), each a result of a counted mistake

## Stage 5. Where the mistake starts: the root cause (rule, no model)

**What this stage answers:** if a teacher can fix only one thing first, which concept should it be?

Concepts build on each other: the graph says which concept must be understood before another (its **prerequisite**). A mistake in a prerequisite explains mistakes in what is built on it. So the rule is:

1. Start at each concept that has a counted mistake.
2. Go back along its prerequisites. If a prerequisite also has a counted mistake, move back to it.
3. The concept furthest back is the **root cause**. If two are equally far back, the one the model was more sure about is taken.

With only one counted mistake, its concept is the root cause.

**In this run.** Only `for_loop` has a counted mistake. Its prerequisites in the subgraph (`loop_control`) have none, so the root cause is `for_loop` with LoopStepAlwaysOne.

## Stage 6. How well each concept is understood: the levels (rule, no model)

**What this stage answers:** for each concept the answer touched, how deep is the student's understanding?

The scale has five levels (from the SOLO taxonomy):

| Level | In plain words |
|---|---|
| L0 | Holds a rule that contradicts Java, or reads the code in an everyday sense |
| L1 | States one correct rule, without applying it |
| L2 | Applies the rules to the code step by step |
| L3 | Relates the parts to each other and to the purpose of the whole |
| L4 | Reasons beyond the given code: predicts a change, transfers, diagnoses |

In the graph every level of a concept lists **ways**: concrete things a student at that level does, for example "output prediction" at L2. In stage 3 the model only said which ways the answer *shows*. It was never asked for a level. The level follows by rule:

1. A concept with a counted mistake (a held misconception that is not a repeat) is **L0**.
2. Otherwise the concept gets the **highest** level among the ways shown, because the levels build on each other.
3. A concept with no mistake and no way shown gets no level.

**In this run.**

| Concept | Level | Why |
|---|---|---|
| `for_loop` | L0 | holds LoopStepAlwaysOne |
| `loop_variable` | L2 | ways shown: L2 “output prediction”, L2 “one step execution” |

## Stage 7. One level for the whole answer (rule, no model)

**What this stage answers:** where does the student stand overall?

- If there is a root cause, the overall level is the level of the root concept: the student stands where the mistake begins, however well the rest is handled.
- If there is no mistake, the levels of stage 6 are sorted from high to low and the middle one is taken, so one weak or one strong concept does not decide for the whole answer.

**In this run.** The root cause is `for_loop` and its level is L0, so the overall level is **L0**.

## The final picture

![The labelled graph at the end of the run](figure06.png)
