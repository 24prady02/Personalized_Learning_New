# Notes: how the rule was made, the results in full, files and limits

This folder holds the rule that turns the per-concept levels of one student answer into **one overall level**, the
steps by which the rule was arrived at, and the 20 scenarios LP01 to LP20 on which it was tested. Every scenario was run
through the whole pipeline (Stage 1 to Stage 7) and has its own folder under `runs/`, with the step report as
`README.md` and as a notebook (`<id>.ipynb`), the figures, the diagnosis and the trace.

## Summary

| Set | Overall level matches | Held misconceptions match | Root cause matches |
|---|---|---|---|
| LP01 to LP20 (loop program) | 19 / 20 | 17 / 20 | 16 / 20 |
"Matches" means agreement with the expected result of the scenario file. The expected results were set by design,
not by independent human raters, so these numbers measure agreement with the design, not accuracy against graded
answers.

## How the overall level is calculated

Every run in `runs/` gets its overall level in the same four steps. The README and the notebook of each run show
these steps with that run's own numbers.

1. **Find the parts of the answer.** One answer touches several concepts, for example the `for` loop, its body and
   `i++`. Each concept the student says something about gets its own level, L0 to L4, from what the student wrote
   about it. These are the *components*. Very general concepts (such as "statement") are left out.
2. **Is a real mistake held?** If the student holds a wrong rule about Java (a misconception or an error), the
   overall level is **L0**, however well the other parts are done. An answer built on a wrong rule is L0.
3. **If there is no mistake, count.** Count how many components are at each level. The level that most components
   have is the overall level. If two levels have the same count, the lower one is taken.
4. **Check how far apart the parts are.** If all components are within one level of each other, the answer is
   *coherent*. If they are two or more levels apart, it is marked *LOW coherence*: the one number hides real
   differences, so read the component table too.

Two examples from this folder:

- **LP04** (a mistake is held). Seven components: 3 at L0 and 4 at L2. The student holds the wrong rule
  BodyChangeIgnoredByCondition, so the overall level is **L0**, with LOW coherence.
- **LP15** (no mistake). Five components: 4 at L3 and 1 at L2. Most are at L3, so the overall level is **L3**,
  coherent.

If no concept gets a level at all (LP20: the bare output "5 5" with no reason), the answer gets no level.

## The rule

**Per component.** A component is a concept the answer touches. Its level is decided as in the main README
(Stage 6): L0 when a misconception is held on it or only L0 ways are shown; otherwise the highest level at which a
way is shown; no level when nothing is shown. The model only says whether a way is shown, citing the student's
clauses; it is never asked for a level.

**Overall.**

1. **Components.** The non-generic concepts that have a level, plus any concept where a real mistake is held (a held
   misconception or error that is not a shadow). A held mistake on a concept without a level counts as L0.
2. **A real mistake is held** (the walk names a root cause): the overall level is **L0**.
3. **No mistake is held:** the overall level is the level that the **largest share** of components shows; on a tie,
   the lower level. No component, no level.
4. **Beside the level,** always report the share of components at each level and the coherence flag: coherent when
   the component levels are at most one level apart, otherwise LOW coherence.

The code is `src/overall_level.py`.

**Where each step comes from.**

| Step | Source |
|---|---|
| Components are levelled one by one, by indicators (ways) | LP test instructions, after Jin et al. 2019 (progress variables) and Jin, Lima & Wang 2025 (analytic rubrics) |
| A misconception held on a component makes that component L0 | LP test instructions, after Lister et al. 2006 and Teague & Lister 2014 |
| Step 2: a held mistake makes the whole answer L0 | **This project's own step.** It extends the component rule to the whole answer; no source states it. The expected results of the test instructions agree with it (every answer with a held wrong rule is expected L0). |
| Step 3: largest share; step 4: shares and coherence | LP test instructions, after Jin et al. 2019 (Table 4, pp. 1337 to 1338) |
| Tie goes to the lower level | LP test instructions (their own adaptation, because one number is required) |

## Sources of the logic

The quotations and page numbers below are those given in the LP test instructions for these scenarios; they were not
checked again against the papers here.

**The three papers by Jin et al., and what is taken from each**

| Paper | What it says (as quoted) | What is taken from it |
|---|---|---|
| Jin et al. 2019, *IJSE*, p. 1325 | “some researchers identify multiple progress variables of an LP, with each progress variable elaborating the development in one dimension of the LP” | Each component is one progress variable and gets its own level. |
| Jin, Lima & Wang 2025, *EM:IP*, p. 2 | “Analytic rubrics specify indicators to be detected from students’ responses”; analytic scoring “often results in greater details and precision” | Score by indicators (the ways) for each component, not by one overall impression. |
| Jin, Lima & Wang 2025, p. 5 | “analytical rubrics that contain item-specific indicators for each LP level”; multi-part answers “were combined into a single response to allow for a comprehensive analysis of student reasoning” | One answer is one unit of evidence; its components are read together to give it one level. |
| Jin et al. 2019, p. 1337 | “Most students in our study provided responses at different levels for different assessment items” | A single level can hide real differences, so check before giving one. |
| Jin et al. 2019, p. 1337 | “If the result shows evidence of ‘knowledge-in-pieces’ (e.g. probabilities of responses at different levels are about the same) … we cannot make any inferences about the students’ levels” | The coherence check; when it fails, the single level is flagged. |
| Jin et al. 2019, p. 1338 | “each student produced responses at adjacent levels, suggesting that those students’ ideas are coherent to a certain degree” | Adjacent levels mean coherent. |
| Jin et al. 2019, pp. 1338–1339, Table 4 | Level classification probabilities per student, for example Student 210: L2 .68, L3 .32; Student 220: L1 .50, L2 .50, described as “rely on Level 1 and Level 2 reasoning” | Report the share at each level; the level with the largest share is the level; a 50/50 split covers both. |
| Jin et al. 2017, *JRST*, pp. 862–863 | Scores fitted with the partial credit model (Wright Map); “we used the resulting person proficiencies from the item response model analysis” | With many students and items, the full method is a partial credit model. |

**The level of one component**

| Rule | Source |
|---|---|
| A misconception is held on the concept (not a shadow): L0, whatever else is shown | Lister et al. 2006, p. 2: a prestructural response manifests “a significant misconception of programming”; Teague & Lister 2014, p. 1; ProgMiscon (Chiodini et al. 2021), p. 2 |
| Only L0 ways are shown (everyday reading, inconsistent trace): L0 | Pea 1986, p. 2; Teague & Lister 2014, p. 1 (“cannot trace code”) |
| Otherwise the highest level at which a way is shown; one shown way is enough | Lister et al. 2006, p. 2 (the SOLO levels build on each other); Jin, Lima & Wang 2025, p. 6 (an answer is scored at the level whose indicator it shows) |
| No way shown and no mistake: no level | Workbook boundary: “a bare correct output is not levelled” |

The levels, their ways and their indicators are defined before any student data (Jin et al. 2019, p. 6) and are the
SOLO levels for code (Lister et al. 2006) matched to the neo-Piagetian stages (Lister 2011; Teague & Lister 2014).

**What is from Jin et al. and what is adapted or added**

- *From Jin et al.:* levels per progress variable, analytic indicators, the coherence check, adjacent levels meaning
  coherent, and reporting the shares across levels.
- *Adapted (by the LP test instructions):* Jin et al. apply this across many items and students with a partial
  credit model and posterior probabilities; here it is applied across the components of one answer with simple
  shares, and a tie is resolved to the lower level because one number is required.
- *Added by this project, with no source:* step 2 of the rule, that a held mistake makes the whole answer L0. It
  extends the component rule of Lister et al. 2006 to the whole answer. Under Jin et al. 2019, p. 1337, an answer
  whose components are far apart would get no single level, which is why the shares and the coherence flag are always
  reported beside the L0. The confidence limit of 0.60 for ways above L2 is also this project's own.
- *Where the sources disagree:* Jimoyiannis (2011) codes some misconception-driven answers at L1 to L2, not L0, and
  modifying given code as L3, not L4 (also Vrachnos & Jimoyiannis 2017).

## How the rule was made

Each row is one step, run on LP01 to LP20 and scored against the expected results.

| Step | What was tried | Overall (final rule) | Overall (share rule alone) | Held | Root | Kept? |
|---|---|---|---|---|---|---|
| 1 | The share rule of the test instructions, on the pipeline as pushed | 18 | 16 | 15 | 14 | starting point |
| 2 | Two corrections to the rules of Stages 4 and 6 (`--rule-fixes`) | 18 | 17 | 16 | 15 | yes |
| 3 | Stricter Stage 3 questions (`--label-v3`) | 18 | 13 | 16 | 14 | **no**, switched off |
| 4 | Graph correction: MissingBraces is a style note, not a misconception | 19 | 16 | 17 | 16 | yes |
| 5 | Steps 2 and 4 together with the stricter questions of step 3 | 18 | 13 | 17 | 15 | **no** |

**Step 1: why the share rule alone is not enough.** With the share rule, an answer built on one wrong rule came
out L2 in LP02, LP04 and LP05: the component with the mistake is L0, but the other components are traced correctly
at L2 and outvote it. The pipeline's own Stage 7 rule (the level of the root-cause concept) gave L0 there, but failed
elsewhere: it counted generic concepts (LP20, a bare "5 5", got L2) and it read no L0 from a held error (LP05). The
final rule takes the part of each that works: a held mistake decides (step 2), and the share rule decides only when
there is no mistake (step 3), over non-generic components.

**Step 2: two rule corrections** (setting `rule_fixes`, in `src/traverse.py`).
- *Stage 4.* An error on a concept was set aside as mere evidence when a misconception was held on the same concept.
  If that misconception was then dropped as a shadow, the concept was left with nothing. Now the error counts again,
  unless it rests on the words of a misconception that is counted elsewhere. This restored the missing-semicolon error
  in LP18.
- *Stage 6.* When the root cause carries a held error and no misconception, the root concept is L0. Before, it kept
  a level from its shown ways (LP05: L2) or had none (MY35: empty overall level).
- On the 40 MY scenarios these two change only MY35 (overall level empty to L0); no held misconception and no root
  cause moves.

**Step 3: stricter questions, tried and dropped.** The model was told to mark a wrong rule as held only when a
clause states it or its reason, and the question for ways above L2 was tightened. It fixed LP09 and removed some
false labels (LP01, LP07), but it also marked a stated wrong rule as only "consistent" (LP02) and lowered correct
high levels (LP14, LP19). Net effect: no gain on the final rule and a loss on the share rule (17 to 13). The code is
still there, off (`--label-v3`). Tried once more on the corrected graph (step 5), it again scored below the version without it, so the
version used in this folder is steps 2 and 4 with the original questions.

**Step 4: a graph correction.** In LP19 the student writes a correct one-statement `for` loop without braces. The
graph had a misconception MissingBraces ("omits braces around a single-statement body") whose own right rule says
braces are optional there. The label was correct by the text of the node, and under step 2 it made a correct L4
answer L0. Leaving out optional braces is a style choice, not a wrong belief, so the record is now marked
`style_only` in `data/raw/chapter1_kg_updated.json` and Stage 1 (`src/model.py`) does not offer such edges to the
walk. The node and edge counts of the graph file are unchanged.

## The scenarios: LP01 to LP20 (loop program)

Program (LP17 and LP18 use the program as written, with the two missing `;` and lowercase `system`):

```java
int i, n = 5;
for (i = 1; i < n; i++)
    i++;
    System.out.println(i);
System.out.println(i);
```

### How the question for each level is structured

A question does not fix the level of an answer; it opens the door to a level, and the answer decides how far the
student goes through it. So the questions are built in two layers.

**1. Each level needs a question that asks for that kind of thinking.** A student can only show a level if the
question gives room for it.

| Level | What the question has to ask for | How the question is worded | What the answer must then do (and where the level stops) |
|---|---|---|---|
| L0 prestructural | nothing special: any question can bring out a wrong rule or an everyday reading | any of the questions below | reads the code in the everyday sense, or applies a wrong rule the language disproves. A single slip in an otherwise correct trace is L2 with an error, not L0. |
| L1 unistructural | a reason ("Explain your reasoning") | a count or value question | names the parts or states the rule, without applying it to the values. Applying it to this code's values is L2. |
| L2 multistructural | the values, step by step | "What is printed? Explain, pass by pass…", "What is the value of i when…" | executes each statement in order, justifies the output value by value, or gives the change one pass makes. A bare correct output is not levelled; stating the purpose of the whole is L3. |
| L3 relational | how the parts work together, or the purpose for every input, with tracing ruled out | "Without tracing line by line, explain what this code does for any value of n" | explains how one construct works with another in the same code, or says what the code does for all inputs, deduced from the code. A purpose guessed from traced cases is L2. |
| L4 extended abstract | something beyond the given code: a change, an error, a new program | "What would be printed if braces were put around…? Explain without tracing the new code", "Will this compile? What happens when you run it?", "Write a loop that…, and explain how it relates to this loop" | predicts what a change keeps or breaks without re-tracing; names the rule broken, the kind of error and the inputs that trigger it; or uses the construct in a new problem. Re-tracing the changed code is L2; fixing one given failing case is L3. |

Two features of the wording carry the higher levels. "Without tracing" closes the L2 route, so that an answer has to
relate or generalise to answer at all. And a question about code that is not on the page (a change, a new loop)
cannot be answered by reading off values, so it reaches L4.

**2. The same question is answered at several levels.** Because the level comes from the answer, each lower-level
question has several answers written for it, one for each level or way it can bring out. This is what tests the rule:
the question stays the same and only the student's reasoning changes.

| Question | What it asks for | Highest level it is built to reach | Answers written for it (level and way each one shows) |
|---|---|---|---|
| Q1. How many times does the body of the for loop run? Explain your reasoning. | a count, with the reason | any level up to L3: the count needs the two i++ to be put together | [LP03](runs/LP03/) L0: misconception; [LP05](runs/LP05/) L0: misconception; [LP12](runs/LP12/) L2: one step execution; [LP14](runs/LP14/) L3: relation to neighbour |
| Q2. How many times is System.out.println executed? Explain your reasoning. | a count, with the reason | L0 to L2: it turns on what the body of the loop is | [LP02](runs/LP02/) L0: misconception; [LP08](runs/LP08/) L1: names the element; [LP09](runs/LP09/) L1: states the rule |
| Q3. What is the value of i when the second println runs? Explain how i gets that value. | one value, with how it comes about | L0 to L2: a value and its justification | [LP04](runs/LP04/) L0: misconception; [LP11](runs/LP11/) L2: output prediction |
| Q4. What is printed? Explain, pass by pass, what happens to i. | the output, pass by pass | L2: it asks for a trace | [LP01](runs/LP01/) L0: everyday reading; [LP06](runs/LP06/) L0: misconception; [LP07](runs/LP07/) L0: inconsistent trace; [LP10](runs/LP10/) L2: line by line trace; [LP13](runs/LP13/) L2: line by line trace; [LP20](runs/LP20/) not levelled: none (bare correct output) |
| Q5. Without tracing line by line, explain what this code does for any value of n. | the purpose, for every input, without a trace | L3: purpose of the whole | [LP15](runs/LP15/) L3: purpose of the whole |
| Q6. What would be printed if braces { } were put around the two indented lines? Explain without tracing the new code line by line. | the effect of a change to the code, without a new trace | L4: predict a change | [LP16](runs/LP16/) L4: predict a change |
| Q7. Will this compile? What happens when you run it? Explain your reasoning. | whether the program as written is correct, and why | L4: diagnose an error | [LP17](runs/LP17/) L4: diagnose an error; [LP18](runs/LP18/) L0: misconception |
| Q8. Write a loop that prints every odd number smaller than n, and explain how it relates to this loop. | a new piece of code, related to the given one | L4: transfer to a new program | [LP19](runs/LP19/) L4: transfer to a new program |

Read across a row: Q4 ("What is printed? Explain, pass by pass…") has six answers. Three are L0 for three different
reasons (an everyday reading, a wrong rule, an inconsistent trace), two are L2 traces (one of them with a slip, which
stays L2), and one is the bare output "5 5", which gets no level. The questions built for L3 and L4 have one answer
each, written at the level the question asks for; LP18 answers the L4 question Q7 with two wrong rules and is L0.

**Boundary cases built into the set.** Three answers sit exactly on a line between two levels, to check that the
rule puts them on the right side: LP04 (the right value for a wrong reason: L0, not L2), LP13 (a correct trace with
one slip: L2, not L0) and LP20 (a bare correct output: no level).

### The logic that points each question and answer to its level

For each of the 20 scenarios: the question, the student's answer, the words in the answer that decide the level, the
indicator of that level (the "way") with the line where the level stops, and the reasoning from the words to the
level. The indicators and the lines between levels are those of the LP test instructions.

#### [LP01](runs/LP01/): L0, everyday reading

- **Question.** What is printed? Explain, pass by pass, what happens to i.
- **Student's answer.** It counts from 1 to 5, so it prints 1, 2, 3, 4, 5. 'For i from 1 to n' means do it for each number.
- **Words that decide.** “'For i from 1 to n' means do it for each number”
- **Indicator of this level.** The answer reads the code with the everyday or maths meaning of its words.
- **Where this level stops.** Any correct, programming-specific statement makes it L1 or higher.
- **Why the answer points to this level.** The student explains the header by what the English words mean, not by any rule of Java: no test, no update, no body is mentioned. Nothing in the answer is a programming statement, so it cannot be L1. That is the everyday reading, L0.
- **What the run gave.** Overall L0 (held mistake); expected L0; match: yes. The calculation is in the [run's README](runs/LP01/).

#### [LP02](runs/LP02/): L0, misconception

- **Question.** How many times is System.out.println executed? Explain your reasoning.
- **Student's answer.** println runs 3 times. The indented println is inside the loop, so it runs on both passes and prints 2 and 4, and then the last println prints 5.
- **Words that decide.** “The indented println is inside the loop, so it runs on both passes”
- **Indicator of this level.** The answer applies a documented wrong rule that the language disproves.
- **Where this level stops.** A single slip in an otherwise rule-correct trace is L2 with an error.
- **Why the answer points to this level.** The student states a rule: indentation puts a statement in the loop body. Java disproves it (without braces the body is one statement). The passes themselves are counted correctly, but the answer rests on the wrong rule, so it is L0 and not an L2 trace with a slip.
- **Wrong rule expected.** StatementAfterLoopInBody, at `loop_body`.
- **What the run gave.** Overall L0 (held mistake); expected L0; match: yes. The calculation is in the [run's README](runs/LP02/).

#### [LP03](runs/LP03/): L0, misconception

- **Question.** How many times does the body of the for loop run? Explain your reasoning.
- **Student's answer.** The body runs 4 times, for i = 1, 2, 3 and 4. The header says i < 5 and i++, so it runs 4 times; the i++ inside the body does not change how many times the loop runs.
- **Words that decide.** “the i++ inside the body does not change how many times the loop runs”
- **Indicator of this level.** The answer applies a documented wrong rule that the language disproves.
- **Where this level stops.** A single slip in an otherwise rule-correct trace is L2 with an error.
- **Why the answer points to this level.** The student says outright that a change to the loop variable in the body does not reach the condition. That is a wrong rule (BodyChangeIgnoredByCondition), stated as the reason for the count of 4. L0.
- **Wrong rule expected.** BodyChangeIgnoredByCondition, at `loop_variable`.
- **What the run gave.** Overall L0 (held mistake); expected L0; match: yes. The calculation is in the [run's README](runs/LP03/).

#### [LP04](runs/LP04/): L0, misconception

- **Question.** What is the value of i when the second println runs? Explain how i gets that value.
- **Student's answer.** i is 5. The loop runs for i = 1, 2, 3, 4 and stops when i reaches 5; the i++ in the body does not affect the count.
- **Words that decide.** “the i++ in the body does not affect the count”
- **Indicator of this level.** The answer applies a documented wrong rule that the language disproves.
- **Where this level stops.** A single slip in an otherwise rule-correct trace is L2 with an error.
- **Why the answer points to this level.** Boundary case. The value given, 5, is correct, so a reader looking only at the output would say L2. But the reason is the same wrong rule as in LP03, and under that rule the loop would run for i = 1, 2, 3, 4. A right value reached by a wrong rule is L0, not L2.
- **Wrong rule expected.** BodyChangeIgnoredByCondition, at `loop_variable`.
- **What the run gave.** Overall L0 (held mistake); expected L0; match: yes. The calculation is in the [run's README](runs/LP04/).

#### [LP05](runs/LP05/): L0, misconception

- **Question.** How many times does the body of the for loop run? Explain your reasoning.
- **Student's answer.** The body runs once. i++ adds 2, so after the body i is 3, and the update makes it 5. Then 5 < 5 is false, so the loop stops.
- **Words that decide.** “i++ adds 2”
- **Indicator of this level.** The answer applies a documented wrong rule that the language disproves.
- **Where this level stops.** A single slip in an otherwise rule-correct trace is L2 with an error.
- **Why the answer points to this level.** The student states a wrong rule about the operator itself (IncrementByTwo) and builds the whole count on it. The rest of the reasoning is consistent with that rule, so it is a held misconception, L0, not a slip.
- **Wrong rule expected.** IncrementByTwo, at `increment_operators`.
- **What the run gave.** Overall L0 (held mistake); expected L0; match: yes. The calculation is in the [run's README](runs/LP05/).

#### [LP06](runs/LP06/): L0, misconception

- **Question.** What is printed? Explain, pass by pass, what happens to i.
- **Student's answer.** It never stops. Each pass starts again with i = 1, so i goes 1, 2, 3 and back to 1, and the println lines are never reached.
- **Words that decide.** “Each pass starts again with i = 1”
- **Indicator of this level.** The answer applies a documented wrong rule that the language disproves.
- **Where this level stops.** A single slip in an otherwise rule-correct trace is L2 with an error.
- **Why the answer points to this level.** The student says the initialisation of the for header runs again on every pass (ForInitRepeats), which Java disproves: it runs once. The conclusion (it never stops) follows from that wrong rule. L0.
- **Wrong rule expected.** ForInitRepeats, at `for_loop`.
- **What the run gave.** Overall L0 (held mistake); expected L0; match: yes. The calculation is in the [run's README](runs/LP06/).

#### [LP07](runs/LP07/): L0, inconsistent trace

- **Question.** What is printed? Explain, pass by pass, what happens to i.
- **Student's answer.** Pass 1: i++ makes i 2 and println prints 2, then the update makes it 3. Pass 2: i++ makes it 4 and the update makes it 5. 5 < 5 is false, so the loop stops and the last line prints 5. Output: 2 and 5.
- **Words that decide.** “Pass 1: i++ makes i 2 and println prints 2 … Pass 2: i++ makes it 4 and the update makes it 5”
- **Indicator of this level.** The answer applies the right rule at one place and a wrong rule at another in the same trace.
- **Where this level stops.** A slip under one consistent, correct rule is L2 with an error.
- **Why the answer points to this level.** On pass 1 the println is treated as part of the body; on pass 2 it is not. The same trace applies the right rule in one place and a wrong one in another, with no rule stated. That is an inconsistent trace, L0. It is not L2, because a slip under one consistent rule would treat both passes the same way.
- **What the run gave.** Overall L0 (held mistake); expected L0; match: yes. The calculation is in the [run's README](runs/LP07/).

#### [LP08](runs/LP08/): L1, names the element

- **Question.** How many times is System.out.println executed? Explain your reasoning.
- **Student's answer.** The program has two System.out.println statements and one for loop. The for loop has a header with a start, a condition and an update, and a body.
- **Words that decide.** “The for loop has a header with a start, a condition and an update, and a body”
- **Indicator of this level.** The answer names or describes the construct correctly.
- **Where this level stops.** Covering every part of the code in order is L2.
- **Why the answer points to this level.** The student names the parts of the program correctly and stops there: no count is given, although the question asks for one. Naming the construct is L1. Going through every part in order with its values would be L2.
- **What the run gave.** Overall L1 (largest share); expected L1; match: yes. The calculation is in the [run's README](runs/LP08/).

#### [LP09](runs/LP09/): L1, states the rule

- **Question.** How many times is System.out.println executed? Explain your reasoning.
- **Student's answer.** Without braces a for loop repeats only the one statement right after its header. The indentation does not matter, so the println lines are not part of the loop.
- **Words that decide.** “Without braces a for loop repeats only the one statement right after its header”
- **Indicator of this level.** The answer states the rule, without applying it to the values.
- **Where this level stops.** Applying it to this code's values is L2.
- **Why the answer points to this level.** The student states the correct rule in general terms. The rule is never applied to the values of this program (no count of println is given). Stating a rule without applying it is L1; applying it to this code's values would be L2.
- **What the run gave.** Overall L4 (largest share); expected L1; match: NO. The calculation is in the [run's README](runs/LP09/).

#### [LP10](runs/LP10/): L2, line by line trace

- **Question.** What is printed? Explain, pass by pass, what happens to i.
- **Student's answer.** i starts at 1. 1 < 5 is true, the body i++ makes i 2, the update makes it 3. 3 < 5 is true, the body makes it 4, the update makes it 5. 5 < 5 is false, so the loop stops. Only i++ was in the loop. Then the two println lines print 5 and 5.
- **Words that decide.** “1 < 5 is true, the body i++ makes i 2, the update makes it 3. 3 < 5 is true …”
- **Indicator of this level.** The answer executes each statement in order with its values.
- **Where this level stops.** Stating the purpose of the whole is L3.
- **Why the answer points to this level.** Every statement is executed in order with its value: test, body, update, test again, then the two println lines. All of it is correct and consistent. That is a line-by-line trace, L2. The student does not say what the code is for, which would be L3.
- **What the run gave.** Overall L2 (largest share); expected L2; match: yes. The calculation is in the [run's README](runs/LP10/).

#### [LP11](runs/LP11/): L2, output prediction

- **Question.** What is the value of i when the second println runs? Explain how i gets that value.
- **Student's answer.** i is 5. The loop leaves when the test 5 < 5 fails, so i is 5 at that point, and nothing after the loop changes i. Both println lines print 5.
- **Words that decide.** “The loop leaves when the test 5 < 5 fails, so i is 5 at that point”
- **Indicator of this level.** The answer gives the output and justifies it value by value.
- **Where this level stops.** A bare correct output is not levelled.
- **Why the answer points to this level.** The student gives the output and justifies it from a value of the program (the failed test). An output with a value-by-value reason is output prediction, L2. The same output with no reason (LP20) is not levelled.
- **What the run gave.** Overall L2 (largest share); expected L2; match: yes. The calculation is in the [run's README](runs/LP11/).

#### [LP12](runs/LP12/): L2, one step execution

- **Question.** How many times does the body of the for loop run? Explain your reasoning.
- **Student's answer.** On one pass i goes up by 2: once by the i++ in the body and once by the i++ in the update. So after the first pass i is 3 instead of 2.
- **Words that decide.** “On one pass i goes up by 2: once by the i++ in the body and once by the i++ in the update”
- **Indicator of this level.** The answer gives the change one execution makes.
- **Where this level stops.** One step of a longer fragment is L1.
- **Why the answer points to this level.** The student gives the change that one pass makes, correctly, and does not go on to the count the question asks for. The change of one execution is one-step execution, L2.
- **What the run gave.** Overall L2 (largest share); expected L2; match: yes. The calculation is in the [run's README](runs/LP12/).

#### [LP13](runs/LP13/): L2, line by line trace

- **Question.** What is printed? Explain, pass by pass, what happens to i.
- **Student's answer.** i starts at 1. 1 < 5, the body makes i 2, the update makes it 3. 3 < 5, the body makes it 4, the update makes it 5. 5 < 5 is false, so it stops. Then it prints 5 and 4.
- **Words that decide.** “5 < 5 is false, so it stops. Then it prints 5 and 4”
- **Indicator of this level.** The answer executes each statement in order with its values.
- **Where this level stops.** Stating the purpose of the whole is L3.
- **Why the answer points to this level.** Boundary case. The trace is correct and consistent to the end of the loop; only the last value (4) is a slip. One slip under one correct rule is L2 with an error. It is not L0, because no wrong rule is applied and the right rule is not dropped anywhere else.
- **What the run gave.** Overall L2 (largest share); expected L2; match: yes. The calculation is in the [run's README](runs/LP13/).

#### [LP14](runs/LP14/): L3, relation to neighbour

- **Question.** How many times does the body of the for loop run? Explain your reasoning.
- **Student's answer.** Twice. The body's i++ and the header's i++ change the same variable, so the condition sees i as 1, then 3, then 5 and fails on the third test. Because there are no braces the body is only i++; the indented println is after the loop.
- **Words that decide.** “The body's i++ and the header's i++ change the same variable, so the condition sees i as 1, then 3, then 5”
- **Indicator of this level.** The answer explains how the concept works with another construct in the same code.
- **Where this level stops.** Two separate correct rules are L1; running them in sequence is L2.
- **Why the answer points to this level.** The student explains how two constructs of the same code work together (the increment in the body and the one in the header, on one variable, as seen by the condition) and what the missing braces mean for the body. Relating one concept to its neighbour is L3. Two correct rules stated side by side would be L1, and running them in sequence L2.
- **What the run gave.** Overall L3 (largest share); expected L3; match: yes. The calculation is in the [run's README](runs/LP14/).

#### [LP15](runs/LP15/): L3, purpose of the whole

- **Question.** Without tracing line by line, explain what this code does for any value of n.
- **Student's answer.** Whatever n is, i starts at 1 and goes up by 2 on every pass, so the loop stops at the first odd number that is n or more. The program prints that number twice. For n = 5 that is 5; for n = 6 it would be 7.
- **Words that decide.** “Whatever n is … the loop stops at the first odd number that is n or more”
- **Indicator of this level.** The answer says what the code does for all inputs, deduced from the code.
- **Where this level stops.** A purpose guessed from traced cases is L2.
- **Why the answer points to this level.** The student says what the code does for every n, deduced from the code (i goes up by 2 from 1), and checks it on two values. A purpose for all inputs is L3. Had the purpose been guessed from the traced case n = 5 only, it would be L2.
- **What the run gave.** Overall L3 (largest share); expected L3; match: yes. The calculation is in the [run's README](runs/LP15/).

#### [LP16](runs/LP16/): L4, predict a change

- **Question.** What would be printed if braces { } were put around the two indented lines? Explain without tracing the new code line by line.
- **Student's answer.** Then the println is in the body and runs on every pass, after the i++ and before the update. The passes do not change (the test still sees 1 and then 3), so it prints 2 and 4 inside the loop, and the last println still prints 5.
- **Words that decide.** “Then the println is in the body and runs on every pass … The passes do not change”
- **Indicator of this level.** The answer predicts what a change keeps or breaks, without re-tracing.
- **Where this level stops.** Re-tracing the changed code is L2.
- **Why the answer points to this level.** The student predicts what the braces change (the println is repeated) and what they keep (the passes), without tracing the new code. Predicting a change is L4. Re-tracing the changed program step by step would be L2.
- **What the run gave.** Overall L4 (largest share); expected L4; match: yes. The calculation is in the [run's README](runs/LP16/).

#### [LP17](runs/LP17/): L4, diagnose an error

- **Question.** Will this compile? What happens when you run it? Explain your reasoning.
- **Student's answer.** It does not compile. Line 1 and line 4 are missing the ; at the end, so javac reports ';' expected. After those are fixed, system.out still fails because Java is case-sensitive: there is no package called system, it must be System. Even then the indentation is misleading: without braces only i++ is in the loop, a silent logic error whenever a braceless loop is followed by indented lines.
- **Words that decide.** “javac reports ';' expected … Java is case-sensitive … a silent logic error whenever a braceless loop is followed by indented lines”
- **Indicator of this level.** The answer names the rule broken, the kind of error and the inputs that trigger it.
- **Where this level stops.** Fixing one given failing case is L3.
- **Why the answer points to this level.** For each fault the student names the rule broken, the kind of error (two compile errors and a silent logic error) and when it occurs. That is diagnosing an error, L4. Repairing one failing case without naming the rule would be L3.
- **What the run gave.** Overall L4 (largest share); expected L4; match: yes. The calculation is in the [run's README](runs/LP17/).

#### [LP18](runs/LP18/): L0, misconception

- **Question.** Will this compile? What happens when you run it? Explain your reasoning.
- **Student's answer.** Yes, it compiles and prints 5 twice. The missing ; do not matter because each statement is on its own line, and system.out is the same as System.out.
- **Words that decide.** “The missing ; do not matter … system.out is the same as System.out”
- **Indicator of this level.** The answer applies a documented wrong rule that the language disproves.
- **Where this level stops.** A single slip in an otherwise rule-correct trace is L2 with an error.
- **Why the answer points to this level.** The question is the L4 question of LP17, but the answer states two wrong rules: a statement needs no terminator, and names are not case-sensitive. Java disproves both (the program does not compile). Wrong rules held: L0, whatever the question was built for.
- **Wrong rule expected.** IdentifierCaseInsensitive, StatementNeedsNoTerminator, at `statement`.
- **What the run gave.** Overall L0 (held mistake); expected L0; match: yes. The calculation is in the [run's README](runs/LP18/).

#### [LP19](runs/LP19/): L4, transfer to a new program

- **Question.** Write a loop that prints every odd number smaller than n, and explain how it relates to this loop.
- **Student's answer.** for (int i = 1; i < n; i += 2) System.out.println(i); This does on purpose what the given loop does by accident: the given loop also steps i by 2, because i++ is in both the body and the header. If I wanted more than one statement repeated I would add braces.
- **Words that decide.** “for (int i = 1; i < n; i += 2) … This does on purpose what the given loop does by accident”
- **Indicator of this level.** The answer uses the construct in an unseen problem, knowing when it is the right tool.
- **Where this level stops.** Reproducing a familiar program is L1 to L3.
- **Why the answer points to this level.** The student writes a loop for a problem that is not on the page, chooses the right construct for it (a step of 2 in the header) and relates it to the given loop. Using the construct in a new problem is transfer, L4.
- **What the run gave.** Overall L4 (largest share); expected L4; match: yes. The calculation is in the [run's README](runs/LP19/).

#### [LP20](runs/LP20/): not levelled

- **Question.** What is printed? Explain, pass by pass, what happens to i.
- **Student's answer.** 5 5
- **Words that decide.** “5 5”
- **Indicator.** No indicator of any level is shown.
- **Where this level stops.** An output with a reason, value by value, would be L2 (output prediction).
- **Why the answer points to this level.** Boundary case. The output is correct, but there is no reason at all, so nothing can be read from it: it may be a guess, and it may hide a wrong rule that happens to give the same output. A bare correct output is not levelled.
- **What the run gave.** Overall no level (no component); expected no level; match: yes. The calculation is in the [run's README](runs/LP20/).


### Results

| Scenario | Components (system) | Held | Root cause | Overall | Decided by | Shares | Expected | Match |
|---|---|---|---|---|---|---|---|---|
| [LP01](runs/LP01/) | for_loop L0, increment_operators L0, loop_body L0, loop_control L0, loop_variable L0 | IdiomOverridesCode at increment_operators, BodyChangeIgnoredByCondition at loop_variable, ComputerFillsInIntent at loop_body | loop_variable / BodyChangeIgnoredByCondition | **L0** | held mistake | L0 1.00; coherent | L0 | yes |
| [LP02](runs/LP02/) | control_flow L2, for_loop L2, increment_operators L2, loop_body L0, loop_control L2, loop_variable L2, println L2, statement L0 | BracelessMultiStatementBody at for_loop, WhitespaceIsSignificant at statement, BracelessMultiStatementBody at loop_body | statement / WhitespaceIsSignificant | **L0** | held mistake | L0 0.25, L2 0.75; LOW coherence | L0 | yes |
| [LP03](runs/LP03/) | for_loop L2, increment_operators L0, loop_body L0, loop_control L0, loop_variable L0 | BodyChangeIgnoredByCondition at loop_variable, IdiomOverridesCode at increment_operators, StateChangeIgnoredAcrossPasses at loop_body, WrongIterationCount at for_loop | loop_variable / BodyChangeIgnoredByCondition | **L0** | held mistake | L0 0.80, L2 0.20; LOW coherence | L0 | yes |
| [LP04](runs/LP04/) | comparison_operators L2, control_flow L2, for_loop L2, increment_operators L0, loop_body L0, loop_control L2, loop_variable L0 | BodyChangeIgnoredByCondition at loop_variable, IdiomOverridesCode at increment_operators, ForLoopPartSkipped at loop_body | loop_variable / BodyChangeIgnoredByCondition | **L0** | held mistake | L0 0.43, L2 0.57; LOW coherence | L0 | yes |
| [LP05](runs/LP05/) | for_loop L2, increment_operators L0, loop_control L0, loop_variable L2 | IncrementByTwo at increment_operators, WrongIterationCount at for_loop, WrongIterationCount at loop_control | loop_control / WrongIterationCount | **L0** | held mistake | L0 0.50, L2 0.50; LOW coherence | L0 | yes |
| [LP06](runs/LP06/) | for_loop L0, increment_operators L2, loop_body L0, loop_control L0, loop_variable L0 | ForInitRepeats at for_loop, StateChangeIgnoredAcrossPasses at loop_body | for_loop / ForInitRepeats | **L0** | held mistake | L0 0.80, L2 0.20; LOW coherence | L0 | yes |
| [LP07](runs/LP07/) | for_loop L2, increment_operators L2, loop_body L2, loop_control L0, loop_variable L2, println L2, statement L0 | WhitespaceIsSignificant at statement, BracelessMultiStatementBody at loop_body, ForLoopPartSkipped at loop_control | statement / WhitespaceIsSignificant | **L0** | held mistake | L0 0.29, L2 0.71; LOW coherence | L0 | yes |
| [LP08](runs/LP08/) | control_flow L1, for_loop L1, loop_body L1, loop_control L1, println L1 | none | none | **L1** | largest share | L1 1.00; coherent | L1 | yes |
| [LP09](runs/LP09/) | control_flow L3, for_loop L4, loop_body L4 | none | none | **L4** | largest share | L3 0.33, L4 0.67; coherent | L1 | NO |
| [LP10](runs/LP10/) | for_loop L3, increment_operators L2, loop_body L2, loop_control L2, loop_variable L2, println L3 | none | none | **L2** | largest share | L2 0.67, L3 0.33; coherent | L2 | yes |
| [LP11](runs/LP11/) | loop_body L1, loop_control L2, loop_variable L3, println L2 | none | none | **L2** | largest share | L1 0.25, L2 0.50, L3 0.25; LOW coherence | L2 | yes |
| [LP12](runs/LP12/) | for_loop L2, increment_operators L2, loop_body L2, loop_control L2, loop_variable L2 | none | none | **L2** | largest share | L2 1.00; coherent | L2 | yes |
| [LP13](runs/LP13/) | for_loop L2, increment_operators L2, loop_body L2, loop_control L3, loop_variable L2, println L2 | none | none | **L2** | largest share | L2 0.83, L3 0.17; coherent | L2 | yes |
| [LP14](runs/LP14/) | for_loop L4, increment_operators L3, loop_body L4, loop_control L3, loop_variable L2 | none | none | **L3** | largest share | L2 0.20, L3 0.40, L4 0.40; LOW coherence | L3 | yes |
| [LP15](runs/LP15/) | for_loop L3, increment_operators L3, loop_body L2, loop_control L3, loop_variable L3 | none | none | **L3** | largest share | L2 0.20, L3 0.80; coherent | L3 | yes |
| [LP16](runs/LP16/) | for_loop L3, increment_operators L2, loop_body L4, loop_control L4, loop_variable L4 | none | none | **L4** | largest share | L2 0.20, L3 0.20, L4 0.60; LOW coherence | L4 | yes |
| [LP17](runs/LP17/) | compile_time_error L4, control_flow L3, for_loop L4, loop_body L4, println L4 | none | none | **L4** | largest share | L3 0.20, L4 0.80; coherent | L4 | yes |
| [LP18](runs/LP18/) | compile_time_error L0, control_flow L2, println L0, statement L0 | IdentifierCaseInsensitive at println, StatementNeedsNoTerminator at statement | statement / StatementNeedsNoTerminator | **L0** | held mistake | L0 0.75, L2 0.25; LOW coherence | L0 | yes |
| [LP19](runs/LP19/) | increment_operators L4, loop_body L2, loop_control L4, loop_variable L4 | none | none | **L4** | largest share | L2 0.25, L4 0.75; LOW coherence | L4 | yes |
| [LP20](runs/LP20/) | none | none | none | **no level** | no component | no component | no level | yes |

### What still does not match

**Overall level, 1 of 20.**
- **LP09** (expected L1, got L4). The student only states the braces rule. The text of the L4 way "diagnose an error" on `for_loop` and `loop_body` contains that same rule, and the model marked the way as shown, although the answer never calls anything an error. No mistake is held, so the largest share decides, and two of three components are L4.

**Held misconceptions, 3 of 20.** In all three the overall level is still right.
- **LP01** (none expected). The everyday reading is found, but the model also holds BodyChangeIgnoredByCondition, IdiomOverridesCode and ComputerFillsInIntent, which the student never states: "it counts from 1 to 5" is an output those rules would also predict.
- **LP02** (StatementAfterLoopInBody expected). The model holds WhitespaceIsSignificant and the error BracelessMultiStatementBody instead: neighbouring rules about the same mistake.
- **LP07** (none expected, an inconsistent trace). WhitespaceIsSignificant, ForLoopPartSkipped and BracelessMultiStatementBody are held.

**Root cause, 4 of 20.** LP01, LP02 and LP07 follow from the held labels above (in LP02 and LP07 the root lands on the generic `statement`). In **LP05** the expected misconception IncrementByTwo is held, but the root goes to `loop_control` with the error WrongIterationCount, because `loop_control` is a prerequisite of `increment_operators`.

Most of these come from the labels the model gives in Stage 3, which the rules of Stages 4 to 7 take as given.


## Files

| File | What it holds |
|---|---|
| `runs/<id>/README.md` | every output of the run, step by step, with the figures |
| `runs/<id>/<id>.ipynb` | the same as a notebook |
| `runs/<id>/diagnosis.json`, `subgraph.json`, `input.json`, `traverse_log.txt`, `report.html`, `<id>_G.html` | the result of Stages 2 to 7, the Stage 1 subgraph, the input, the trace, the report as one page and the interactive graph |
| `results_LP.md`, `results_LP.csv` | one row per scenario: components, held, root cause, overall level, shares, expected, match |
| `scenarios_loop_LP.json` | the 20 scenarios (a copy of the file in `data/raw/`), with the expected result of each |

## How to run it again

```
python src/evaluate.py --scenarios data/raw/scenarios_loop_LP.json --no-figures --results results/lp --log experiments/logs/subgraph_report_lp.txt
python src/traverse.py --all --scenarios data/raw/scenarios_loop_LP.json --rule-fixes
python src/overall_level.py --scenarios data/raw/scenarios_loop_LP.json --out LP_level_classified/results_LP
```

The model's replies are
stored in `experiments/llm_cache`, so a rerun asks nothing new. `--rule-fixes` is needed because the setting is off
in `experiments/config.json` (the 40 MY runs in `scenario_explanations/` were made without it).

## Limits

- The expected levels were set by design, not by independent human raters, and the rule was worked out on these same
  20 scenarios. It has not been tested on answers it was not built on.
- Step 2 of the rule has no source. Jin et al. 2019 would give no single level to an answer whose components are far
  apart (p. 1337); here such an answer gets L0 when a mistake is held, with the LOW coherence flag beside it.
- Under step 2, one wrong held label makes a whole answer L0. The overall level is therefore as reliable as the
  misconception labels of Stage 3.
- Each scenario was run once; run-to-run variation of the model was not measured.
- LP17 and LP18: `identifier` is a generic concept, so Stage 1 leaves it out and IdentifierCaseInsensitive can only
  attach at `println`.
