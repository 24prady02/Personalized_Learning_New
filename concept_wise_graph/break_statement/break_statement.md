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

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 22 edges around this concept, each explained in the graph's own words.

## What it needs first (3)

A prerequisite edge means the other concept has to be understood before `break_statement`.

### `do_while_loop` comes before `break_statement`

*do { body } while (c); -- body first, test after*

break leaves the do-while loop at once, exactly as it leaves a while or for loop.

- **Grounding:** spec passage

### `for_loop` comes before `break_statement`

*a while with init/condition/update packaged together*

break leaves the for loop at once, without running the rest of the body or the remaining passes.

- **Grounding:** book passage

### `while_loop` comes before `break_statement`

*repeat a block while a condition holds*

break immediately exits a loop without letting it run to completion.

- **Grounding:** book passage
- **How `break_statement` combines with `while_loop`:** break gives a while loop a second exit, in the middle of the body. After the loop, the program has to tell which exit was taken by re-testing the state (as in \`if (i &gt; N/i)\`), so any variable used for that test must be declared before the loop.
- **How `while_loop` combines with `break_statement`:** break exits the loop immediately, so a while loop can end either by a false test or by a break; while (true) needs a break (or is infinite).

## What it leads to (2)

These concepts need `break_statement` first.

### `break_statement` comes before `labeled_break`

*labeled break/continue exit or continue an outer loop*

Labeled break extends break to an outer loop.

- **Grounding:** questionable
- **How `break_statement` combines with `labeled_break`:** Plain break reaches only the innermost loop. In nested loops, ending the outer loop needs \`break label;\` on a labeled outer statement (or a flag tested by the outer loop).
- **How `labeled_break` combines with `break_statement`:** An unlabeled break exits only the innermost loop or switch. Adding a label lets break exit any enclosing labeled statement, and so end several nested loops at once.

### `break_statement` comes before `switch_statement`

*switch (x) { case v: ...; break; default: ... }*

Each case of a switch normally ends with break, which exits the switch body.

- **Grounding:** book passage
- **How `break_statement` combines with `switch_statement`:** In a switch, break ends the switch body; without it, execution falls through into the next case. A break inside a switch that is inside a loop exits only the switch, not the loop.
- **How `switch_statement` combines with `break_statement`:** Each case is normally ended by break, which exits the switch body. Leaving it out makes that case fall into the next. Inside a loop, that break exits the switch, not the loop.

## Learned alongside (2)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

### `break_statement` alongside `continue_statement`

*continue -- skips to the next iteration of the innermost loop*

break ends the whole loop; continue ends only the current pass.

- **Grounding:** book passage
- **How `break_statement` combines with `continue_statement`:** Both skip the rest of the current body. break then leaves the loop (no increment, no further test); continue goes on to the increment and the next test.
- **How `continue_statement` combines with `break_statement`:** Both abandon the rest of the body; continue proceeds to the next pass (increment and test), break leaves the loop with no increment or test.

### `break_statement` alongside `flag_search_loop`

*a boolean flag that a loop sets once and never resets*

Two ways to stop a search when the item is found: break leaves the loop at once, while a boolean flag is set and tested in the loop condition so the loop ends at its next test. After either, the code must tell the found case from the loop finishing normally.

- **Grounding:** book passage

## Misconceptions (4)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### BreakEndsProgram

- **Wrong rule:** break ends the whole program.
- **Right rule:** break ends only the innermost loop (or switch); execution continues after it.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: break ends the whole program. Right rule: break ends only the innermost loop (or switch); execution continues with the statement after it.

### BreakExitsIf

- **Wrong rule:** break leaves the if statement it is written in.
- **Right rule:** break immediately exits a loop without letting it run to completion, and in a switch it exits the switch body.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: break leaves the if statement it is written in. Right rule: An if is not a break target: break immediately exits the innermost enclosing loop (or switch) without letting it run to completion.
- **Shows at level L0 as:** inconsistent trace: Applies the LT rule unevenly: on some passes the trace continues the body after break, or runs the increment and the test once more after break, so the final loop variable is one too large (e.g. i = 4 instead of 3 when 3 divides N). (here mixing in: "break leaves the if statement it is written in")

### BreakIgnored

- **Wrong rule:** break has no effect; the loop body just carries on.
- **Right rule:** break leaves the innermost loop at once; the rest of the body and later passes do not run.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: break has no effect; the loop body just carries on. Right rule: break leaves the innermost loop at once: the rest of the body, the increment, and all later passes are skipped.

### BreakIsContinue

- **Wrong rule:** break starts the next iteration of the loop.
- **Right rule:** break exits the loop immediately; continue skips to the next iteration of the loop.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: break starts the next iteration of the loop. Right rule: break exits the loop immediately; continue is the statement that skips to the next iteration.

## Errors (0)

An error edge states the rule that gets broken in a program, and the right rule.

The graph has no error edge from this concept.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for break statement: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to break statement agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

break statement -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (6 ways).

- **everyday reading** (folk-meaning rule): Folk meaning: in English 'break' means to pause, or to stop or break out of whatever you are in, so a novice reads it as leaving the enclosing if, as starting the next round, or as stopping the whole program. In Java, \`break;\` ends only the innermost enclosing loop or switch, and execution continues with the statement after it.
- **misconception** (wrong rule / right rule; shows `BreakExitsIf`): wrong rule: break leaves the if statement it is written in. Right rule: An if is not a break target: break immediately exits the innermost enclosing loop (or switch) without letting it run to completion.
- **misconception** (wrong rule / right rule; shows `BreakIsContinue`): wrong rule: break starts the next iteration of the loop. Right rule: break exits the loop immediately; continue is the statement that skips to the next iteration.
- **misconception** (wrong rule / right rule; shows `BreakEndsProgram`): wrong rule: break ends the whole program. Right rule: break ends only the innermost loop (or switch); execution continues with the statement after it.
- **misconception** (wrong rule / right rule; shows `BreakIgnored`): wrong rule: break has no effect; the loop body just carries on. Right rule: break leaves the innermost loop at once: the rest of the body, the increment, and all later passes are skipped.
- **inconsistent trace** (uneven-application rule; shows `BreakExitsIf`): Applies the LT rule unevenly: on some passes the trace continues the body after break, or runs the increment and the test once more after break, so the final loop variable is one too large (e.g. i = 4 instead of 3 when 3 divides N). (here mixing in: "break leaves the if statement it is written in")

### L1: Unistructural / atom x text surface

L1 for break statement: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

break statement -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

- **names the element** (identity rule): Jump statement: \`break;\` immediately ends the innermost enclosing while, for, do or switch.
- **states the rule** (declarative rule): \`break;\` may appear only inside a loop or switch. When executed, it completes that innermost loop or switch at once, and control passes to the statement after it. (Spec: JLS §14.15.)

### L2: Multistructural / block x execution / preoperational

L2 for break statement: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

break statement -&gt; L2 (Multistructural): the answer applies the rules of break statement to every part of the code, in order (3 ways).

- **line by line trace** (operational sequencing rule): When \`break\` executes: the remaining statements of the body are skipped, the for-loop increment and the condition are not evaluated again, and control continues at the first statement after the loop. In \`for (i = 2; i &lt;= N/i; i++) if (N % i == 0) break;\` it runs right after the test that found a divisor.
- **output prediction** (evaluation / result rule): break is a statement and produces no value. Its effect shows in the variables it leaves: after the primality loop for N = 15, i is 3 (the smallest divisor), so \`i &gt; N/i\` is false and 'is prime' is not printed.
- **one step execution** (state-transition rule): One execution of break changes no variable. It changes only the point of control (to after the loop), so every variable keeps its value at the moment of the break.

### L3: Relational / relations x function (concrete operational begins)

L3 for break statement: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

break statement -&gt; L3 (Relational): the answer relates the parts (6 ways).

- **relation to neighbour** (composition rule (with a neighbour)): break gives a while loop a second exit, in the middle of the body. After the loop, the program has to tell which exit was taken by re-testing the state (as in \`if (i &gt; N/i)\`), so any variable used for that test must be declared before the loop.
- **relation to neighbour** (composition rule (with a neighbour)): Plain break reaches only the innermost loop. In nested loops, ending the outer loop needs \`break label;\` on a labeled outer statement (or a flag tested by the outer loop).
- **relation to neighbour** (composition rule (with a neighbour)): Both skip the rest of the current body. break then leaves the loop (no increment, no further test); continue goes on to the increment and the next test.
- **relation to neighbour** (composition rule (with a neighbour)): In a switch, break ends the switch body; without it, execution falls through into the next case. A break inside a switch that is inside a loop exits only the switch, not the loop.
- **relation to neighbour** (composition rule (with a neighbour)): Two ways to stop a search when the item is found: break leaves the loop at once, while a boolean flag is set and tested in the loop condition so the loop ends at its next test. After either, the code must tell the found case from the loop finishing normally.
- **purpose of the whole** (plan / role rule): Plan: early-exit search (Soloway 'loop-and-a-half' or exit-on-found). Stop scanning as soon as the answer is known, e.g. at the first divisor; the loop variable is a stepper whose value at exit reports the find.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for break statement: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

break statement -&gt; L4 (Extended abstract): the answer reasons beyond the given code (6 ways).

- **predict a change** (conservation rule; shows `BreakExitsIf`): Removing the break keeps the loop finite but lets it run to completion. In the prime test, i then ends above N/i for every N, so composites are reported as prime. Invariant kept with break: after the loop, \`i &lt;= N/i\` holds exactly when the break was taken.
- **transfer to a new program** (applicability rule): Use break when the reason to stop is discovered in the middle of a pass (first divisor, sentinel found) and folding it into the loop condition would be awkward. Prefer a plain loop condition when the exit can be stated up front. In a method, \`return\` is often clearer. S&amp;W use break rarely.
- **diagnose an error** (error rule): rule broken: break must be inside a loop or switch. Kind: compile-time. Trigger class: \`break;\` inside an if that is not inside any loop or switch (break outside switch or loop).
- **diagnose an error** (error rule): rule broken: Statements after break in the same block can never run. Kind: compile-time. Trigger class: Code written directly after \`break;\` in the same block (unreachable statement).
- **diagnose an error** (error rule): rule broken: break exits only the innermost loop or switch. Kind: silent logic error. Trigger class: A break in an inner loop (or in a switch inside a loop) that was meant to end the outer loop: the outer loop keeps going.
- **diagnose an error** (error rule): rule broken: A variable used after the loop to tell how it ended must be in scope. Kind: compile-time. Trigger class: Declaring the loop index in the for header (\`for (int i = 2; ...)\`) and then testing \`i\` after the loop (cannot find symbol).

## Same topic

`break_statement` belongs to the topic **Other conditional and loop constructs (break, continue, switch, do-while, ?:)** (`topic1.3.g`). The topic also contains: `conditional_operator`, `continue_statement`, `do_while_loop`, `labeled_break`, `switch_statement`.

## Rules of the concept (22)

- **folk-meaning rule:** Folk meaning: in English 'break' means to pause, or to stop or break out of whatever you are in, so a novice reads it as leaving the enclosing if, as starting the next round, or as stopping the whole program. In Java, \`break;\` ends only the innermost enclosing loop or switch, and execution continues with the statement after it.
- **wrong rule / right rule:** BreakExitsIf: wrong: break leaves the if statement it is written in. \| right: An if is not a break target: break immediately exits the innermost enclosing loop (or switch) without letting it run to completion.
- **wrong rule / right rule:** BreakIsContinue: wrong: break starts the next iteration of the loop. \| right: break exits the loop immediately; continue is the statement that skips to the next iteration.
- **wrong rule / right rule:** BreakEndsProgram: wrong: break ends the whole program. \| right: break ends only the innermost loop (or switch); execution continues with the statement after it.
- **wrong rule / right rule:** BreakIgnored: wrong: break has no effect; the loop body just carries on. \| right: break leaves the innermost loop at once: the rest of the body, the increment, and all later passes are skipped.
- **uneven-application rule:** Applies the LT rule unevenly: on some passes the trace continues the body after break, or runs the increment and the test once more after break, so the final loop variable is one too large (e.g. i = 4 instead of 3 when 3 divides N).
- **identity rule:** Jump statement: \`break;\` immediately ends the innermost enclosing while, for, do or switch.
- **declarative rule:** \`break;\` may appear only inside a loop or switch. When executed, it completes that innermost loop or switch at once, and control passes to the statement after it. (Spec: JLS §14.15.)
- **operational sequencing rule:** When \`break\` executes: the remaining statements of the body are skipped, the for-loop increment and the condition are not evaluated again, and control continues at the first statement after the loop. In \`for (i = 2; i &lt;= N/i; i++) if (N % i == 0) break;\` it runs right after the test that found a divisor.
- **evaluation / result rule:** break is a statement and produces no value. Its effect shows in the variables it leaves: after the primality loop for N = 15, i is 3 (the smallest divisor), so \`i &gt; N/i\` is false and 'is prime' is not printed.
- **state-transition rule:** One execution of break changes no variable. It changes only the point of control (to after the loop), so every variable keeps its value at the moment of the break.
- **composition rule (with a neighbour):** with while\_loop: break gives a while loop a second exit, in the middle of the body. After the loop, the program has to tell which exit was taken by re-testing the state (as in \`if (i &gt; N/i)\`), so any variable used for that test must be declared before the loop.
- **composition rule (with a neighbour):** with labeled\_break: Plain break reaches only the innermost loop. In nested loops, ending the outer loop needs \`break label;\` on a labeled outer statement (or a flag tested by the outer loop).
- **composition rule (with a neighbour):** with continue\_statement: Both skip the rest of the current body. break then leaves the loop (no increment, no further test); continue goes on to the increment and the next test.
- **composition rule (with a neighbour):** with switch\_statement: In a switch, break ends the switch body; without it, execution falls through into the next case. A break inside a switch that is inside a loop exits only the switch, not the loop.
- **plan / role rule:** Plan: early-exit search (Soloway 'loop-and-a-half' or exit-on-found). Stop scanning as soon as the answer is known, e.g. at the first divisor; the loop variable is a stepper whose value at exit reports the find.
- **conservation rule:** Removing the break keeps the loop finite but lets it run to completion. In the prime test, i then ends above N/i for every N, so composites are reported as prime. Invariant kept with break: after the loop, \`i &lt;= N/i\` holds exactly when the break was taken.
- **error rule:** rule broken: break must be inside a loop or switch. (compile-time)
- **error rule:** rule broken: Statements after break in the same block can never run. (compile-time)
- **error rule:** rule broken: break exits only the innermost loop or switch. (silent logic error)
- **error rule:** rule broken: A variable used after the loop to tell how it ended must be in scope. (compile-time)
- **applicability rule:** Use break when the reason to stop is discovered in the middle of a pass (first divisor, sentinel found) and folding it into the loop condition would be awkward. Prefer a plain loop condition when the exit can be stated up front. In a method, \`return\` is often clearer. S&amp;W use break rarely.

## The whole prerequisite chain

- **Everything it builds on (16):** `arithmetic_operators`, `boolean`, `boolean_expression`, `comparison_operators`, `data_type`, `do_while_loop`, `expression`, `for_loop`, `identifier`, `literal`, `logical_operators`, `loop_control`, `loop_variable`, `primitive_type`, `variable`, `while_loop`
- **Everything that builds on it (2):** `labeled_break`, `switch_statement`
