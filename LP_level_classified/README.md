# One overall level for an answer: the rule, how it was made, and the 20 test scenarios

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

## How the overall level is calculated, in simple words

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

### How each question provides each type

| Scenario | Level and way tested | Question | Student answer | Why the answer is this way |
|---|---|---|---|---|
| [LP01](runs/LP01/) | L0: everyday reading | What is printed? Explain, pass by pass, what happens to i. | It counts from 1 to 5, so it prints 1, 2, 3, 4, 5. 'For i from 1 to n' means do it for each number. | Reads the header as English 'for each number 1 to 5'; no Java rule applied. |
| [LP02](runs/LP02/) | L0: misconception | How many times is System.out.println executed? Explain your reasoning. | println runs 3 times. The indented println is inside the loop, so it runs on both passes and prints 2 and 4, and then the last println prints 5. | The key trap: indentation read as the body. The real body is only i++. Wrong rule: StatementAfterLoopInBody. |
| [LP03](runs/LP03/) | L0: misconception | How many times does the body of the for loop run? Explain your reasoning. | The body runs 4 times, for i = 1, 2, 3 and 4. The header says i < 5 and i++, so it runs 4 times; the i++ inside the body does not change how many times the loop runs. | States the wrong rule: the i++ in the body does not change the count. Wrong rule: BodyChangeIgnoredByCondition. |
| [LP04](runs/LP04/) | L0: misconception | What is the value of i when the second println runs? Explain how i gets that value. | i is 5. The loop runs for i = 1, 2, 3, 4 and stops when i reaches 5; the i++ in the body does not affect the count. | Boundary case: the value (5) is right but the reason is the wrong rule, so it is L0, not L2. Wrong rule: BodyChangeIgnoredByCondition. |
| [LP05](runs/LP05/) | L0: misconception | How many times does the body of the for loop run? Explain your reasoning. | The body runs once. i++ adds 2, so after the body i is 3, and the update makes it 5. Then 5 < 5 is false, so the loop stops. | States the wrong rule: i++ adds 2. Wrong rule: IncrementByTwo. |
| [LP06](runs/LP06/) | L0: misconception | What is printed? Explain, pass by pass, what happens to i. | It never stops. Each pass starts again with i = 1, so i goes 1, 2, 3 and back to 1, and the println lines are never reached. | States the wrong rule: each pass starts again with i = 1. Wrong rule: ForInitRepeats. |
| [LP07](runs/LP07/) | L0: inconsistent trace | What is printed? Explain, pass by pass, what happens to i. | Pass 1: i++ makes i 2 and println prints 2, then the update makes it 3. Pass 2: i++ makes it 4 and the update makes it 5. 5 < 5 is false, so the loop stops and the last line prints 5. Output: 2 and 5. | Treats println as part of the body on pass 1 only: the right rule in one place, a wrong one in another. |
| [LP08](runs/LP08/) | L1: names the element | How many times is System.out.println executed? Explain your reasoning. | The program has two System.out.println statements and one for loop. The for loop has a header with a start, a condition and an update, and a body. | Names the parts correctly; gives no count. Covering every part in order would be L2. |
| [LP09](runs/LP09/) | L1: states the rule | How many times is System.out.println executed? Explain your reasoning. | Without braces a for loop repeats only the one statement right after its header. The indentation does not matter, so the println lines are not part of the loop. | States the right rule but never applies it to the values (no count). Applying it would be L2. |
| [LP10](runs/LP10/) | L2: line by line trace | What is printed? Explain, pass by pass, what happens to i. | i starts at 1. 1 < 5 is true, the body i++ makes i 2, the update makes it 3. 3 < 5 is true, the body makes it 4, the update makes it 5. 5 < 5 is false, so the loop stops. Only i++ was in the loop. Then the two println lines print 5 and 5. | Executes every statement in order with its values. |
| [LP11](runs/LP11/) | L2: output prediction | What is the value of i when the second println runs? Explain how i gets that value. | i is 5. The loop leaves when the test 5 < 5 fails, so i is 5 at that point, and nothing after the loop changes i. Both println lines print 5. | Gives the value and justifies it from the failed test. |
| [LP12](runs/LP12/) | L2: one step execution | How many times does the body of the for loop run? Explain your reasoning. | On one pass i goes up by 2: once by the i++ in the body and once by the i++ in the update. So after the first pass i is 3 instead of 2. | Gives the change one pass makes; does not finish the count. |
| [LP13](runs/LP13/) | L2: line by line trace | What is printed? Explain, pass by pass, what happens to i. | i starts at 1. 1 < 5, the body makes i 2, the update makes it 3. 3 < 5, the body makes it 4, the update makes it 5. 5 < 5 is false, so it stops. Then it prints 5 and 4. | Boundary case: a correct, consistent trace with one slip at the end is L2 with an error, not L0. |
| [LP14](runs/LP14/) | L3: relation to neighbour | How many times does the body of the for loop run? Explain your reasoning. | Twice. The body's i++ and the header's i++ change the same variable, so the condition sees i as 1, then 3, then 5 and fails on the third test. Because there are no braces the body is only i++; the indented println is after the loop. | Explains how the body's i++ and the header's i++ work on the same variable, and what the missing braces mean for the body. |
| [LP15](runs/LP15/) | L3: purpose of the whole | Without tracing line by line, explain what this code does for any value of n. | Whatever n is, i starts at 1 and goes up by 2 on every pass, so the loop stops at the first odd number that is n or more. The program prints that number twice. For n = 5 that is 5; for n = 6 it would be 7. | Purpose deduced from the code for all n, not guessed from traced cases (that would be L2). |
| [LP16](runs/LP16/) | L4: predict a change | What would be printed if braces { } were put around the two indented lines? Explain without tracing the new code line by line. | Then the println is in the body and runs on every pass, after the i++ and before the update. The passes do not change (the test still sees 1 and then 3), so it prints 2 and 4 inside the loop, and the last println still prints 5. | Predicts what braces would change without re-tracing. Expected output 2, 4, 5. |
| [LP17](runs/LP17/) | L4: diagnose an error | Will this compile? What happens when you run it? Explain your reasoning. | It does not compile. Line 1 and line 4 are missing the ; at the end, so javac reports ';' expected. After those are fixed, system.out still fails because Java is case-sensitive: there is no package called system, it must be System. Even then the indentation is misleading: without braces only i++ is in the loop, a silent logic error whenever a braceless loop is followed by indented lines. | Names the rules broken, the kind of each error and when it bites (program as written, with the missing ; and system). |
| [LP18](runs/LP18/) | L0: misconception | Will this compile? What happens when you run it? Explain your reasoning. | Yes, it compiles and prints 5 twice. The missing ; do not matter because each statement is on its own line, and system.out is the same as System.out. | Two mistakes: a statement needs no ; and system is the same as System (program as written). Wrong rule: IdentifierCaseInsensitive, StatementNeedsNoTerminator. |
| [LP19](runs/LP19/) | L4: transfer to a new program | Write a loop that prints every odd number smaller than n, and explain how it relates to this loop. | for (int i = 1; i < n; i += 2) System.out.println(i); This does on purpose what the given loop does by accident: the given loop also steps i by 2, because i++ is in both the body and the header. If I wanted more than one statement repeated I would add braces. | Uses the construct in a new problem and relates it to the given loop. |
| [LP20](runs/LP20/) | not levelled: none (bare correct output) | What is printed? Explain, pass by pass, what happens to i. | 5 5 | Boundary case: a bare correct output with no reason is not levelled. |

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
