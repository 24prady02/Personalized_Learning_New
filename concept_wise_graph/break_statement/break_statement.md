# break_statement (`break_statement`)

break -- immediately exits the innermost loop or switch

Section 1.3 Conditionals and Loops, topic 1.3.g Other conditional and loop constructs (break, continue, switch, do-while, ?:).

![The knowledge graph around break_statement](break_statement.png)

## At a glance

- **Needs first:** `do_while_loop`, `for_loop`, `while_loop`
- **Leads to:** `labeled_break`, `switch_statement`
- **Learned alongside:** `continue_statement`, `flag_search_loop`
- **Misconceptions:** `BreakEndsProgram`, `BreakExitsIf`, `BreakIgnored`, `BreakIsContinue`
- **Errors:** none
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 22 edges around this concept. The edge logic, the wrong and right rules and the exact rules of the ways are copied word for word from the graph.

## To work on (0)

Nothing is missing for this concept.

## What it needs first (3)

A prerequisite edge means the other concept has to be understood before `break_statement`.

### `do_while_loop` comes before `break_statement`

*do { body } while (c); -- body first, test after*

- **Edge:** `pre:do_while_loop->break_statement`
- **Exact edge logic:** break leaves the do-while loop at once, exactly as it leaves a while or for loop.
- **Grounding:** spec\_passage

### `for_loop` comes before `break_statement`

*a while with init/condition/update packaged together*

- **Edge:** `pre:for_loop->break_statement`
- **Exact edge logic:** break leaves the for loop at once, without running the rest of the body or the remaining passes.
- **Grounding:** book\_passage

### `while_loop` comes before `break_statement`

*repeat a block while a condition holds*

- **Edge:** `pre:while_loop->break_statement`
- **Exact edge logic:** break immediately exits a loop without letting it run to completion.
- **Grounding:** book\_passage
- **Composition rule (R) of `break_statement` with `while_loop`:** break gives a while loop a second exit, in the middle of the body. After the loop, the program has to tell which exit was taken by re-testing the state (as in \`if (i &gt; N/i)\`), so any variable used for that test must be declared before the loop.
- **Composition rule (R) of `while_loop` with `break_statement`:** break exits the loop immediately, so a while loop can end either by a false test or by a break; while (true) needs a break (or is infinite).

## What it leads to (2)

These concepts need `break_statement` first.

### `break_statement` comes before `labeled_break`

*labeled break/continue exit or continue an outer loop*

- **Edge:** `pre:break_statement->labeled_break`
- **Exact edge logic:** Labeled break extends break to an outer loop.
- **Grounding:** questionable
- **Composition rule (R) of `break_statement` with `labeled_break`:** Plain break reaches only the innermost loop. In nested loops, ending the outer loop needs \`break label;\` on a labeled outer statement (or a flag tested by the outer loop).
- **Composition rule (R) of `labeled_break` with `break_statement`:** An unlabeled break exits only the innermost loop or switch. Adding a label lets break exit any enclosing labeled statement, and so end several nested loops at once.

### `break_statement` comes before `switch_statement`

*switch (x) { case v: ...; break; default: ... }*

- **Edge:** `pre:break_statement->switch_statement`
- **Exact edge logic:** Each case of a switch normally ends with break, which exits the switch body.
- **Grounding:** book\_passage
- **Composition rule (R) of `break_statement` with `switch_statement`:** In a switch, break ends the switch body; without it, execution falls through into the next case. A break inside a switch that is inside a loop exits only the switch, not the loop.
- **Composition rule (R) of `switch_statement` with `break_statement`:** Each case is normally ended by break, which exits the switch body. Leaving it out makes that case fall into the next. Inside a loop, that break exits the switch, not the loop.

## Learned alongside (2)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

### `break_statement` alongside `continue_statement`

*continue -- skips to the next iteration of the innermost loop*

- **Edge:** `par:break_statement~continue_statement`
- **Exact edge logic:** break ends the whole loop; continue ends only the current pass.
- **Grounding:** book\_passage
- **Composition rule (R) of `break_statement` with `continue_statement`:** Both skip the rest of the current body. break then leaves the loop (no increment, no further test); continue goes on to the increment and the next test.
- **Composition rule (R) of `continue_statement` with `break_statement`:** Both abandon the rest of the body; continue proceeds to the next pass (increment and test), break leaves the loop with no increment or test.

### `break_statement` alongside `flag_search_loop`

*a boolean flag that a loop sets once and never resets*

- **Edge:** `par:flag_search_loop~break_statement`
- **Exact edge logic:** Two ways to stop a search when the item is found: break leaves the loop at once, while a boolean flag is set and tested in the loop condition so the loop ends at its next test. After either, the code must tell the found case from the loop finishing normally.
- **Grounding:** book\_passage

## Misconceptions (4)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### BreakEndsProgram

- **Edge:** `break_statement` &rarr; `BreakEndsProgram` (misconception)
- **Exact edge logic (the wrong rule):** break ends the whole program.
- **Twin logic (the right rule):** break ends only the innermost loop (or switch); execution continues after it.
- **Wrong belief (on the node):** break ends the whole program.
- **Correct rule (on the node):** break ends only the innermost loop (or switch); execution continues after it.
- **Provenance:** published
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [3] misconception, exact rule:** wrong rule: break ends the whole program. Right rule: break ends only the innermost loop (or switch); execution continues with the statement after it.

### BreakExitsIf

- **Edge:** `break_statement` &rarr; `BreakExitsIf` (misconception)
- **Exact edge logic (the wrong rule):** break leaves the if statement it is written in.
- **Twin logic (the right rule):** break immediately exits a loop without letting it run to completion, and in a switch it exits the switch body.
- **Wrong belief (on the node):** break leaves the if statement it is written in.
- **Correct rule (on the node):** break immediately exits a loop without letting it run to completion, and in a switch it exits the switch body.
- **Provenance:** textbook
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [1] misconception, exact rule:** wrong rule: break leaves the if statement it is written in. Right rule: An if is not a break target: break immediately exits the innermost enclosing loop (or switch) without letting it run to completion.
- **L0 way [5] inconsistent\_trace, exact rule:** Applies the LT rule unevenly: on some passes the trace continues the body after break, or runs the increment and the test once more after break, so the final loop variable is one too large (e.g. i = 4 instead of 3 when 3 divides N). (here mixing in: "break leaves the if statement it is written in")

### BreakIgnored

- **Edge:** `break_statement` &rarr; `BreakIgnored` (misconception)
- **Exact edge logic (the wrong rule):** break has no effect; the loop body just carries on.
- **Twin logic (the right rule):** break leaves the innermost loop at once; the rest of the body and later passes do not run.
- **Wrong belief (on the node):** break has no effect; the loop body just carries on.
- **Correct rule (on the node):** break leaves the innermost loop at once; the rest of the body and later passes do not run.
- **Provenance:** published
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [4] misconception, exact rule:** wrong rule: break has no effect; the loop body just carries on. Right rule: break leaves the innermost loop at once: the rest of the body, the increment, and all later passes are skipped.

### BreakIsContinue

- **Edge:** `break_statement` &rarr; `BreakIsContinue` (misconception)
- **Exact edge logic (the wrong rule):** break starts the next iteration of the loop.
- **Twin logic (the right rule):** break exits the loop immediately; continue skips to the next iteration of the loop.
- **Wrong belief (on the node):** break starts the next iteration of the loop.
- **Correct rule (on the node):** break exits the loop immediately; continue skips to the next iteration of the loop.
- **Provenance:** published
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [2] misconception, exact rule:** wrong rule: break starts the next iteration of the loop. Right rule: break exits the loop immediately; continue is the statement that skips to the next iteration.

## Errors (0)

An error edge states the rule that gets broken in a program, and the right rule.

The graph has no error edge from this concept.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for break statement: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to break statement agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

- **Edge:** `break_statement` &rarr; `break_statement@L0` (has_level)
- **Exact edge logic:** break statement -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (6 ways).

Ways (6), each with its exact rule:

- **[0] everyday\_reading** (rule type E, folk-meaning rule): Folk meaning: in English 'break' means to pause, or to stop or break out of whatever you are in, so a novice reads it as leaving the enclosing if, as starting the next round, or as stopping the whole program. In Java, \`break;\` ends only the innermost enclosing loop or switch, and execution continues with the statement after it.
- **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `BreakExitsIf`: wrong rule: break leaves the if statement it is written in. Right rule: An if is not a break target: break immediately exits the innermost enclosing loop (or switch) without letting it run to completion.
- **[2] misconception** (rule type M, wrong rule / right rule) &rarr; `BreakIsContinue`: wrong rule: break starts the next iteration of the loop. Right rule: break exits the loop immediately; continue is the statement that skips to the next iteration.
- **[3] misconception** (rule type M, wrong rule / right rule) &rarr; `BreakEndsProgram`: wrong rule: break ends the whole program. Right rule: break ends only the innermost loop (or switch); execution continues with the statement after it.
- **[4] misconception** (rule type M, wrong rule / right rule) &rarr; `BreakIgnored`: wrong rule: break has no effect; the loop body just carries on. Right rule: break leaves the innermost loop at once: the rest of the body, the increment, and all later passes are skipped.
- **[5] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `BreakExitsIf`: Applies the LT rule unevenly: on some passes the trace continues the body after break, or runs the increment and the test once more after break, so the final loop variable is one too large (e.g. i = 4 instead of 3 when 3 divides N). (here mixing in: "break leaves the if statement it is written in")

### L1: Unistructural / atom x text surface

L1 for break statement: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

- **Edge:** `break_statement` &rarr; `break_statement@L1` (has_level)
- **Exact edge logic:** break statement -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

Ways (2), each with its exact rule:

- **[0] names\_the\_element** (rule type N, identity rule): Jump statement: \`break;\` immediately ends the innermost enclosing while, for, do or switch.
- **[1] states\_the\_rule** (rule type S, declarative rule): \`break;\` may appear only inside a loop or switch. When executed, it completes that innermost loop or switch at once, and control passes to the statement after it. (Spec: JLS §14.15.)

### L2: Multistructural / block x execution / preoperational

L2 for break statement: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

- **Edge:** `break_statement` &rarr; `break_statement@L2` (has_level)
- **Exact edge logic:** break statement -&gt; L2 (Multistructural): the answer applies the rules of break statement to every part of the code, in order (3 ways).

Ways (3), each with its exact rule:

- **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): When \`break\` executes: the remaining statements of the body are skipped, the for-loop increment and the condition are not evaluated again, and control continues at the first statement after the loop. In \`for (i = 2; i &lt;= N/i; i++) if (N % i == 0) break;\` it runs right after the test that found a divisor.
- **[1] output\_prediction** (rule type OP, evaluation / result rule): break is a statement and produces no value. Its effect shows in the variables it leaves: after the primality loop for N = 15, i is 3 (the smallest divisor), so \`i &gt; N/i\` is false and 'is prime' is not printed.
- **[2] one\_step\_execution** (rule type OS, state-transition rule): One execution of break changes no variable. It changes only the point of control (to after the loop), so every variable keeps its value at the moment of the break.

### L3: Relational / relations x function (concrete operational begins)

L3 for break statement: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

- **Edge:** `break_statement` &rarr; `break_statement@L3` (has_level)
- **Exact edge logic:** break statement -&gt; L3 (Relational): the answer relates the parts (6 ways).

Ways (6), each with its exact rule:

- **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): break gives a while loop a second exit, in the middle of the body. After the loop, the program has to tell which exit was taken by re-testing the state (as in \`if (i &gt; N/i)\`), so any variable used for that test must be declared before the loop.
- **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Plain break reaches only the innermost loop. In nested loops, ending the outer loop needs \`break label;\` on a labeled outer statement (or a flag tested by the outer loop).
- **[2] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Both skip the rest of the current body. break then leaves the loop (no increment, no further test); continue goes on to the increment and the next test.
- **[3] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): In a switch, break ends the switch body; without it, execution falls through into the next case. A break inside a switch that is inside a loop exits only the switch, not the loop.
- **[4] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Two ways to stop a search when the item is found: break leaves the loop at once, while a boolean flag is set and tested in the loop condition so the loop ends at its next test. After either, the code must tell the found case from the loop finishing normally.
- **[5] purpose\_of\_the\_whole** (rule type P, plan / role rule): Plan: early-exit search (Soloway 'loop-and-a-half' or exit-on-found). Stop scanning as soon as the answer is known, e.g. at the first divisor; the loop variable is a stepper whose value at exit reports the find.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for break statement: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

- **Edge:** `break_statement` &rarr; `break_statement@L4` (has_level)
- **Exact edge logic:** break statement -&gt; L4 (Extended abstract): the answer reasons beyond the given code (6 ways).

Ways (6), each with its exact rule:

- **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `BreakExitsIf`: Removing the break keeps the loop finite but lets it run to completion. In the prime test, i then ends above N/i for every N, so composites are reported as prime. Invariant kept with break: after the loop, \`i &lt;= N/i\` holds exactly when the break was taken.
- **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Use break when the reason to stop is discovered in the middle of a pass (first divisor, sentinel found) and folding it into the loop condition would be awkward. Prefer a plain loop condition when the exit can be stated up front. In a method, \`return\` is often clearer. S&amp;W use break rarely.
- **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: break must be inside a loop or switch. Kind: compile-time. Trigger class: \`break;\` inside an if that is not inside any loop or switch (break outside switch or loop).
- **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: Statements after break in the same block can never run. Kind: compile-time. Trigger class: Code written directly after \`break;\` in the same block (unreachable statement).
- **[4] diagnose\_an\_error** (rule type D, error rule): rule broken: break exits only the innermost loop or switch. Kind: silent logic error. Trigger class: A break in an inner loop (or in a switch inside a loop) that was meant to end the outer loop: the outer loop keeps going.
- **[5] diagnose\_an\_error** (rule type D, error rule): rule broken: A variable used after the loop to tell how it ended must be in scope. Kind: compile-time. Trigger class: Declaring the loop index in the for header (\`for (int i = 2; ...)\`) and then testing \`i\` after the loop (cannot find symbol).

## Same topic

`break_statement` belongs to the topic **Other conditional and loop constructs (break, continue, switch, do-while, ?:)** (`topic1.3.g`). The topic also contains: `conditional_operator`, `continue_statement`, `do_while_loop`, `labeled_break`, `switch_statement`.

## Rules of the concept (22)

- **Book** (SW-1e, p. 70 (pdf 80)): "In some situations, we want to immediately exit a loop without letting it run to completion."
- **Book** (SW-1e, p. 70 (pdf 80)): "Java provides the break statement for this purpose."
- **Book** (OT-Branch, ): "An unlabeled break statement terminates the innermost switch, for, while, or do-while statement, but a labeled break terminates an outer statement."
- **E** (folk-meaning rule): Folk meaning: in English 'break' means to pause, or to stop or break out of whatever you are in, so a novice reads it as leaving the enclosing if, as starting the next round, or as stopping the whole program. In Java, \`break;\` ends only the innermost enclosing loop or switch, and execution continues with the statement after it.
- **M** (wrong rule / right rule): BreakExitsIf: wrong: break leaves the if statement it is written in. \| right: An if is not a break target: break immediately exits the innermost enclosing loop (or switch) without letting it run to completion.
- **M** (wrong rule / right rule): BreakIsContinue: wrong: break starts the next iteration of the loop. \| right: break exits the loop immediately; continue is the statement that skips to the next iteration.
- **M** (wrong rule / right rule): BreakEndsProgram: wrong: break ends the whole program. \| right: break ends only the innermost loop (or switch); execution continues with the statement after it.
- **M** (wrong rule / right rule): BreakIgnored: wrong: break has no effect; the loop body just carries on. \| right: break leaves the innermost loop at once: the rest of the body, the increment, and all later passes are skipped.
- **T** (uneven-application rule): Applies the LT rule unevenly: on some passes the trace continues the body after break, or runs the increment and the test once more after break, so the final loop variable is one too large (e.g. i = 4 instead of 3 when 3 divides N).
- **N** (identity rule): Jump statement: \`break;\` immediately ends the innermost enclosing while, for, do or switch.
- **S** (declarative rule): \`break;\` may appear only inside a loop or switch. When executed, it completes that innermost loop or switch at once, and control passes to the statement after it. (Spec: JLS §14.15.)
- **LT** (operational sequencing rule): When \`break\` executes: the remaining statements of the body are skipped, the for-loop increment and the condition are not evaluated again, and control continues at the first statement after the loop. In \`for (i = 2; i &lt;= N/i; i++) if (N % i == 0) break;\` it runs right after the test that found a divisor.
- **OP** (evaluation / result rule): break is a statement and produces no value. Its effect shows in the variables it leaves: after the primality loop for N = 15, i is 3 (the smallest divisor), so \`i &gt; N/i\` is false and 'is prime' is not printed.
- **OS** (state-transition rule): One execution of break changes no variable. It changes only the point of control (to after the loop), so every variable keeps its value at the moment of the break.
- **R** (composition rule (with a neighbour)): with while\_loop: break gives a while loop a second exit, in the middle of the body. After the loop, the program has to tell which exit was taken by re-testing the state (as in \`if (i &gt; N/i)\`), so any variable used for that test must be declared before the loop.
- **R** (composition rule (with a neighbour)): with labeled\_break: Plain break reaches only the innermost loop. In nested loops, ending the outer loop needs \`break label;\` on a labeled outer statement (or a flag tested by the outer loop).
- **R** (composition rule (with a neighbour)): with continue\_statement: Both skip the rest of the current body. break then leaves the loop (no increment, no further test); continue goes on to the increment and the next test.
- **R** (composition rule (with a neighbour)): with switch\_statement: In a switch, break ends the switch body; without it, execution falls through into the next case. A break inside a switch that is inside a loop exits only the switch, not the loop.
- **P** (plan / role rule): Plan: early-exit search (Soloway 'loop-and-a-half' or exit-on-found). Stop scanning as soon as the answer is known, e.g. at the first divisor; the loop variable is a stepper whose value at exit reports the find.
- **C** (conservation rule): Removing the break keeps the loop finite but lets it run to completion. In the prime test, i then ends above N/i for every N, so composites are reported as prime. Invariant kept with break: after the loop, \`i &lt;= N/i\` holds exactly when the break was taken.
- **D** (error rule): rule broken: break must be inside a loop or switch. (compile-time)
- **D** (error rule): rule broken: Statements after break in the same block can never run. (compile-time)
- **D** (error rule): rule broken: break exits only the innermost loop or switch. (silent logic error)
- **D** (error rule): rule broken: A variable used after the loop to tell how it ended must be in scope. (compile-time)
- **X** (applicability rule): Use break when the reason to stop is discovered in the middle of a pass (first divisor, sentinel found) and folding it into the loop condition would be awkward. Prefer a plain loop condition when the exit can be stated up front. In a method, \`return\` is often clearer. S&amp;W use break rarely.

## How it is found in code and answers (reader block)

- **Aliases:** break
- **Code patterns:** `\bbreak\s*;`
- **Operator symbols:** none
- **Java types:** none

## The whole prerequisite chain

- **Everything it builds on (16):** `arithmetic_operators`, `boolean`, `boolean_expression`, `comparison_operators`, `data_type`, `do_while_loop`, `expression`, `for_loop`, `identifier`, `literal`, `logical_operators`, `loop_control`, `loop_variable`, `primitive_type`, `variable`, `while_loop`
- **Everything that builds on it (2):** `labeled_break`, `switch_statement`

## Every edge in this view and its exact edge logic (22)

All the edges drawn in the picture, in the order: prerequisite, parallel, misconception, error, has_level, contains.

**1. `break_statement` &rarr; `labeled_break`** (prerequisite)

- **Exact edge logic:** Labeled break extends break to an outer loop.
- **Grounding:** questionable
- **Composition rule (R) of `break_statement` with `labeled_break`:** Plain break reaches only the innermost loop. In nested loops, ending the outer loop needs \`break label;\` on a labeled outer statement (or a flag tested by the outer loop).
- **Composition rule (R) of `labeled_break` with `break_statement`:** An unlabeled break exits only the innermost loop or switch. Adding a label lets break exit any enclosing labeled statement, and so end several nested loops at once.

**2. `break_statement` &rarr; `switch_statement`** (prerequisite)

- **Exact edge logic:** Each case of a switch normally ends with break, which exits the switch body.
- **Grounding:** book\_passage
- **Composition rule (R) of `break_statement` with `switch_statement`:** In a switch, break ends the switch body; without it, execution falls through into the next case. A break inside a switch that is inside a loop exits only the switch, not the loop.
- **Composition rule (R) of `switch_statement` with `break_statement`:** Each case is normally ended by break, which exits the switch body. Leaving it out makes that case fall into the next. Inside a loop, that break exits the switch, not the loop.

**3. `do_while_loop` &rarr; `break_statement`** (prerequisite)

- **Exact edge logic:** break leaves the do-while loop at once, exactly as it leaves a while or for loop.
- **Grounding:** spec\_passage

**4. `for_loop` &rarr; `break_statement`** (prerequisite)

- **Exact edge logic:** break leaves the for loop at once, without running the rest of the body or the remaining passes.
- **Grounding:** book\_passage

**5. `while_loop` &rarr; `break_statement`** (prerequisite)

- **Exact edge logic:** break immediately exits a loop without letting it run to completion.
- **Grounding:** book\_passage
- **Composition rule (R) of `while_loop` with `break_statement`:** break exits the loop immediately, so a while loop can end either by a false test or by a break; while (true) needs a break (or is infinite).
- **Composition rule (R) of `break_statement` with `while_loop`:** break gives a while loop a second exit, in the middle of the body. After the loop, the program has to tell which exit was taken by re-testing the state (as in \`if (i &gt; N/i)\`), so any variable used for that test must be declared before the loop.

**6. `break_statement` &harr; `continue_statement`** (parallel)

- **Exact edge logic:** break ends the whole loop; continue ends only the current pass.
- **Grounding:** book\_passage
- **Composition rule (R) of `break_statement` with `continue_statement`:** Both skip the rest of the current body. break then leaves the loop (no increment, no further test); continue goes on to the increment and the next test.
- **Composition rule (R) of `continue_statement` with `break_statement`:** Both abandon the rest of the body; continue proceeds to the next pass (increment and test), break leaves the loop with no increment or test.

**7. `flag_search_loop` &harr; `break_statement`** (parallel)

- **Exact edge logic:** Two ways to stop a search when the item is found: break leaves the loop at once, while a boolean flag is set and tested in the loop condition so the loop ends at its next test. After either, the code must tell the found case from the loop finishing normally.
- **Grounding:** book\_passage

**8. `break_statement` &rarr; `BreakEndsProgram`** (misconception)

- **Exact edge logic (the wrong rule):** break ends the whole program.
- **Twin logic (the right rule):** break ends only the innermost loop (or switch); execution continues after it.
- **Role:** primary

**9. `break_statement` &rarr; `BreakExitsIf`** (misconception)

- **Exact edge logic (the wrong rule):** break leaves the if statement it is written in.
- **Twin logic (the right rule):** break immediately exits a loop without letting it run to completion, and in a switch it exits the switch body.
- **Role:** primary

**10. `break_statement` &rarr; `BreakIgnored`** (misconception)

- **Exact edge logic (the wrong rule):** break has no effect; the loop body just carries on.
- **Twin logic (the right rule):** break leaves the innermost loop at once; the rest of the body and later passes do not run.
- **Role:** primary

**11. `break_statement` &rarr; `BreakIsContinue`** (misconception)

- **Exact edge logic (the wrong rule):** break starts the next iteration of the loop.
- **Twin logic (the right rule):** break exits the loop immediately; continue skips to the next iteration of the loop.
- **Role:** primary

**12. `break_statement` &rarr; `break_statement@L0`** (has_level)

- **Exact edge logic:** break statement -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (6 ways).
  - **[0] everyday\_reading** (rule type E, folk-meaning rule): Folk meaning: in English 'break' means to pause, or to stop or break out of whatever you are in, so a novice reads it as leaving the enclosing if, as starting the next round, or as stopping the whole program. In Java, \`break;\` ends only the innermost enclosing loop or switch, and execution continues with the statement after it.
  - **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `BreakExitsIf`: wrong rule: break leaves the if statement it is written in. Right rule: An if is not a break target: break immediately exits the innermost enclosing loop (or switch) without letting it run to completion.
  - **[2] misconception** (rule type M, wrong rule / right rule) &rarr; `BreakIsContinue`: wrong rule: break starts the next iteration of the loop. Right rule: break exits the loop immediately; continue is the statement that skips to the next iteration.
  - **[3] misconception** (rule type M, wrong rule / right rule) &rarr; `BreakEndsProgram`: wrong rule: break ends the whole program. Right rule: break ends only the innermost loop (or switch); execution continues with the statement after it.
  - **[4] misconception** (rule type M, wrong rule / right rule) &rarr; `BreakIgnored`: wrong rule: break has no effect; the loop body just carries on. Right rule: break leaves the innermost loop at once: the rest of the body, the increment, and all later passes are skipped.
  - **[5] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `BreakExitsIf`: Applies the LT rule unevenly: on some passes the trace continues the body after break, or runs the increment and the test once more after break, so the final loop variable is one too large (e.g. i = 4 instead of 3 when 3 divides N). (here mixing in: "break leaves the if statement it is written in")

**13. `break_statement` &rarr; `break_statement@L1`** (has_level)

- **Exact edge logic:** break statement -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).
  - **[0] names\_the\_element** (rule type N, identity rule): Jump statement: \`break;\` immediately ends the innermost enclosing while, for, do or switch.
  - **[1] states\_the\_rule** (rule type S, declarative rule): \`break;\` may appear only inside a loop or switch. When executed, it completes that innermost loop or switch at once, and control passes to the statement after it. (Spec: JLS §14.15.)

**14. `break_statement` &rarr; `break_statement@L2`** (has_level)

- **Exact edge logic:** break statement -&gt; L2 (Multistructural): the answer applies the rules of break statement to every part of the code, in order (3 ways).
  - **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): When \`break\` executes: the remaining statements of the body are skipped, the for-loop increment and the condition are not evaluated again, and control continues at the first statement after the loop. In \`for (i = 2; i &lt;= N/i; i++) if (N % i == 0) break;\` it runs right after the test that found a divisor.
  - **[1] output\_prediction** (rule type OP, evaluation / result rule): break is a statement and produces no value. Its effect shows in the variables it leaves: after the primality loop for N = 15, i is 3 (the smallest divisor), so \`i &gt; N/i\` is false and 'is prime' is not printed.
  - **[2] one\_step\_execution** (rule type OS, state-transition rule): One execution of break changes no variable. It changes only the point of control (to after the loop), so every variable keeps its value at the moment of the break.

**15. `break_statement` &rarr; `break_statement@L3`** (has_level)

- **Exact edge logic:** break statement -&gt; L3 (Relational): the answer relates the parts (6 ways).
  - **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): break gives a while loop a second exit, in the middle of the body. After the loop, the program has to tell which exit was taken by re-testing the state (as in \`if (i &gt; N/i)\`), so any variable used for that test must be declared before the loop.
  - **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Plain break reaches only the innermost loop. In nested loops, ending the outer loop needs \`break label;\` on a labeled outer statement (or a flag tested by the outer loop).
  - **[2] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Both skip the rest of the current body. break then leaves the loop (no increment, no further test); continue goes on to the increment and the next test.
  - **[3] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): In a switch, break ends the switch body; without it, execution falls through into the next case. A break inside a switch that is inside a loop exits only the switch, not the loop.
  - **[4] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Two ways to stop a search when the item is found: break leaves the loop at once, while a boolean flag is set and tested in the loop condition so the loop ends at its next test. After either, the code must tell the found case from the loop finishing normally.
  - **[5] purpose\_of\_the\_whole** (rule type P, plan / role rule): Plan: early-exit search (Soloway 'loop-and-a-half' or exit-on-found). Stop scanning as soon as the answer is known, e.g. at the first divisor; the loop variable is a stepper whose value at exit reports the find.

**16. `break_statement` &rarr; `break_statement@L4`** (has_level)

- **Exact edge logic:** break statement -&gt; L4 (Extended abstract): the answer reasons beyond the given code (6 ways).
  - **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `BreakExitsIf`: Removing the break keeps the loop finite but lets it run to completion. In the prime test, i then ends above N/i for every N, so composites are reported as prime. Invariant kept with break: after the loop, \`i &lt;= N/i\` holds exactly when the break was taken.
  - **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Use break when the reason to stop is discovered in the middle of a pass (first divisor, sentinel found) and folding it into the loop condition would be awkward. Prefer a plain loop condition when the exit can be stated up front. In a method, \`return\` is often clearer. S&amp;W use break rarely.
  - **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: break must be inside a loop or switch. Kind: compile-time. Trigger class: \`break;\` inside an if that is not inside any loop or switch (break outside switch or loop).
  - **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: Statements after break in the same block can never run. Kind: compile-time. Trigger class: Code written directly after \`break;\` in the same block (unreachable statement).
  - **[4] diagnose\_an\_error** (rule type D, error rule): rule broken: break exits only the innermost loop or switch. Kind: silent logic error. Trigger class: A break in an inner loop (or in a switch inside a loop) that was meant to end the outer loop: the outer loop keeps going.
  - **[5] diagnose\_an\_error** (rule type D, error rule): rule broken: A variable used after the loop to tell how it ended must be in scope. Kind: compile-time. Trigger class: Declaring the loop index in the for header (\`for (int i = 2; ...)\`) and then testing \`i\` after the loop (cannot find symbol).

**17. `topic1.3.g` &rarr; `break_statement`** (contains)

- topic `topic1.3.g` contains `break_statement`

**18. `topic1.3.g` &rarr; `conditional_operator`** (contains)

- topic `topic1.3.g` contains `conditional_operator`

**19. `topic1.3.g` &rarr; `continue_statement`** (contains)

- topic `topic1.3.g` contains `continue_statement`

**20. `topic1.3.g` &rarr; `do_while_loop`** (contains)

- topic `topic1.3.g` contains `do_while_loop`

**21. `topic1.3.g` &rarr; `labeled_break`** (contains)

- topic `topic1.3.g` contains `labeled_break`

**22. `topic1.3.g` &rarr; `switch_statement`** (contains)

- topic `topic1.3.g` contains `switch_statement`
