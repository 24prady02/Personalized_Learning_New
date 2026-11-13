# continue_statement (`continue_statement`)

continue -- skips to the next iteration of the innermost loop

Section 1.3 Conditionals and Loops, topic 1.3.g Other conditional and loop constructs (break, continue, switch, do-while, ?:).

![The knowledge graph around continue_statement](continue_statement.png)

## At a glance

- **Needs first:** `do_while_loop`, `for_loop`, `while_loop`
- **Leads to:** nothing
- **Learned alongside:** `break_statement`
- **Misconceptions:** `ContinueExitsLoop`, `ContinueIgnored`
- **Errors:** none
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 17 edges around this concept, each explained in the graph's own words.

## What it needs first (3)

A prerequisite edge means the other concept has to be understood before `continue_statement`.

### `do_while_loop` comes before `continue_statement`

*do { body } while (c); -- body first, test after*

continue ends the current pass of the do-while loop and goes on to the loop test.

- **Grounding:** spec passage

### `for_loop` comes before `continue_statement`

*a while with init/condition/update packaged together*

continue skips the rest of the loop body; in a for loop control goes straight to the increment statement and then the next test.

- **Grounding:** book passage
- **How `continue_statement` combines with `for_loop`:** In a for loop the increment still runs after continue, so the loop always advances. This is why the for/while equivalence has an exception: in the rewritten while, a continue jumps past the \`&lt;increment&gt;;\` at the end of the body.
- **How `for_loop` combines with `continue_statement`:** In a for loop, continue skips the rest of the body and transfers control directly to the increment, then the next test; this is one of the few places where the for/while equivalence fails.

### `while_loop` comes before `continue_statement`

*repeat a block while a condition holds*

continue ends the current pass of the while loop and goes straight back to the loop test.

- **Grounding:** book passage

## What it leads to (0)

These concepts need `continue_statement` first.

No concept has this one as a prerequisite.

## Learned alongside (1)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

### `continue_statement` alongside `break_statement`

*break -- immediately exits the innermost loop or switch*

break ends the whole loop; continue ends only the current pass.

- **Grounding:** book passage
- **How `continue_statement` combines with `break_statement`:** Both abandon the rest of the body; continue proceeds to the next pass (increment and test), break leaves the loop with no increment or test.
- **How `break_statement` combines with `continue_statement`:** Both skip the rest of the current body. break then leaves the loop (no increment, no further test); continue goes on to the increment and the next test.

## Misconceptions (2)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### ContinueExitsLoop

- **Wrong rule:** continue ends the loop.
- **Right rule:** continue skips the rest of the current pass: control transfers directly to the increment statement for the next iteration of the loop.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: continue ends the loop. Right rule: continue skips only the rest of the current pass: in a for loop, control transfers directly to the increment and then the next test, and the loop goes on while the test is true.
- **Shows at level L0 as:** inconsistent trace: Applies the LT rule unevenly: on some passes the trace runs the statements after continue, or skips the for-loop increment, so the traced counts or outputs include items that should be skipped. (here mixing in: "continue ends the loop")

### ContinueIgnored

- **Wrong rule:** continue means carry on with the rest of the loop body, so it has no effect.
- **Right rule:** continue skips the rest of the current iteration.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: continue means carry on with the rest of the loop body, so it has no effect. Right rule: continue skips every statement after it in the current pass.

## Errors (0)

An error edge states the rule that gets broken in a program, and the right rule.

The graph has no error edge from this concept.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for continue statement: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to continue statement agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

continue statement -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (4 ways).

- **everyday reading** (folk-meaning rule): Folk meaning: in English 'continue' means carry on with what you are doing, so a novice reads \`continue;\` as 'keep executing the rest of the body' (no effect) or as 'continue after the loop'. In Java it abandons the rest of the current pass and goes straight to the next iteration.
- **misconception** (wrong rule / right rule; shows `ContinueExitsLoop`): wrong rule: continue ends the loop. Right rule: continue skips only the rest of the current pass: in a for loop, control transfers directly to the increment and then the next test, and the loop goes on while the test is true.
- **misconception** (wrong rule / right rule; shows `ContinueIgnored`): wrong rule: continue means carry on with the rest of the loop body, so it has no effect. Right rule: continue skips every statement after it in the current pass.
- **inconsistent trace** (uneven-application rule; shows `ContinueExitsLoop`): Applies the LT rule unevenly: on some passes the trace runs the statements after continue, or skips the for-loop increment, so the traced counts or outputs include items that should be skipped. (here mixing in: "continue ends the loop")

### L1: Unistructural / atom x text surface

L1 for continue statement: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

continue statement -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

- **names the element** (identity rule): Jump statement: \`continue;\` ends the current iteration of the innermost enclosing loop and starts the next one.
- **states the rule** (declarative rule): \`continue;\` may appear only inside a loop. When executed, the rest of the body is skipped. In a for loop control goes to the increment; in a while or do-while it goes to the condition test. (Spec: JLS §14.16.)

### L2: Multistructural / block x execution / preoperational

L2 for continue statement: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

continue statement -&gt; L2 (Multistructural): the answer applies the rules of continue statement to every part of the code, in order (3 ways).

- **line by line trace** (operational sequencing rule): Order after continue in \`for (init; test; inc) body\`: skip the remaining body statements, execute inc, evaluate test, and run the next pass if it is true. In a while loop there is no separate inc, so control goes directly to the test.
- **output prediction** (evaluation / result rule): continue produces no value. Its effect is on what the loop outputs: \`for (int i = 0; i &lt; 5; i++) { if (i % 2 == 0) continue; System.out.print(i); }\` prints 13.
- **one step execution** (state-transition rule): One execution changes no variable; it only moves control to the increment (for) or the test (while). The variables keep their values, and the statements skipped in this pass make no changes.

### L3: Relational / relations x function (concrete operational begins)

L3 for continue statement: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

continue statement -&gt; L3 (Relational): the answer relates the parts (3 ways).

- **relation to neighbour** (composition rule (with a neighbour)): In a for loop the increment still runs after continue, so the loop always advances. This is why the for/while equivalence has an exception: in the rewritten while, a continue jumps past the \`&lt;increment&gt;;\` at the end of the body.
- **relation to neighbour** (composition rule (with a neighbour)): Both abandon the rest of the body; continue proceeds to the next pass (increment and test), break leaves the loop with no increment or test.
- **purpose of the whole** (plan / role rule): Plan: skip/filter plan. It guards the rest of the body against items that should not be processed (e.g. skip non-matching or invalid entries), avoiding a deeply nested if.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for continue statement: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

continue statement -&gt; L4 (Extended abstract): the answer reasons beyond the given code (5 ways).

- **predict a change** (conservation rule; shows `ContinueExitsLoop`): Replacing \`if (c) continue; rest;\` with \`if (!c) { rest; }\` keeps the behaviour. Moving the continue below the update in a while loop, or the update below the continue, changes whether the loop advances.
- **transfer to a new program** (applicability rule): Use continue to skip items early in a long loop body when the alternative is a deeply nested if. Avoid it in while loops whose update is at the end of the body, and avoid it when a simple if around the work is clearer. S&amp;W rarely use it.
- **diagnose an error** (error rule): rule broken: continue must be inside a loop. Kind: compile-time. Trigger class: \`continue;\` in a switch or if that is not inside any loop (continue outside of loop).
- **diagnose an error** (error rule): rule broken: In a while loop continue goes straight to the test, skipping an update placed later in the body. Kind: silent logic error. Trigger class: \`while (i &lt; n) { if (skip(i)) continue; ...; i++; }\`: once a skipped i is reached, i never changes and the loop runs forever.
- **diagnose an error** (error rule): rule broken: Statements after continue in the same block can never run. Kind: compile-time. Trigger class: Code directly after \`continue;\` in the same block (unreachable statement).

## Same topic

`continue_statement` belongs to the topic **Other conditional and loop constructs (break, continue, switch, do-while, ?:)** (`topic1.3.g`). The topic also contains: `break_statement`, `conditional_operator`, `do_while_loop`, `labeled_break`, `switch_statement`.

## Rules of the concept (17)

- **folk-meaning rule:** Folk meaning: in English 'continue' means carry on with what you are doing, so a novice reads \`continue;\` as 'keep executing the rest of the body' (no effect) or as 'continue after the loop'. In Java it abandons the rest of the current pass and goes straight to the next iteration.
- **wrong rule / right rule:** ContinueExitsLoop: wrong: continue ends the loop. \| right: continue skips only the rest of the current pass: in a for loop, control transfers directly to the increment and then the next test, and the loop goes on while the test is true.
- **wrong rule / right rule:** ContinueIgnored: wrong: continue means carry on with the rest of the loop body, so it has no effect. \| right: continue skips every statement after it in the current pass.
- **uneven-application rule:** Applies the LT rule unevenly: on some passes the trace runs the statements after continue, or skips the for-loop increment, so the traced counts or outputs include items that should be skipped.
- **identity rule:** Jump statement: \`continue;\` ends the current iteration of the innermost enclosing loop and starts the next one.
- **declarative rule:** \`continue;\` may appear only inside a loop. When executed, the rest of the body is skipped. In a for loop control goes to the increment; in a while or do-while it goes to the condition test. (Spec: JLS §14.16.)
- **operational sequencing rule:** Order after continue in \`for (init; test; inc) body\`: skip the remaining body statements, execute inc, evaluate test, and run the next pass if it is true. In a while loop there is no separate inc, so control goes directly to the test.
- **evaluation / result rule:** continue produces no value. Its effect is on what the loop outputs: \`for (int i = 0; i &lt; 5; i++) { if (i % 2 == 0) continue; System.out.print(i); }\` prints 13.
- **state-transition rule:** One execution changes no variable; it only moves control to the increment (for) or the test (while). The variables keep their values, and the statements skipped in this pass make no changes.
- **composition rule (with a neighbour):** with for\_loop: In a for loop the increment still runs after continue, so the loop always advances. This is why the for/while equivalence has an exception: in the rewritten while, a continue jumps past the \`&lt;increment&gt;;\` at the end of the body.
- **composition rule (with a neighbour):** with break\_statement: Both abandon the rest of the body; continue proceeds to the next pass (increment and test), break leaves the loop with no increment or test.
- **plan / role rule:** Plan: skip/filter plan. It guards the rest of the body against items that should not be processed (e.g. skip non-matching or invalid entries), avoiding a deeply nested if.
- **conservation rule:** Replacing \`if (c) continue; rest;\` with \`if (!c) { rest; }\` keeps the behaviour. Moving the continue below the update in a while loop, or the update below the continue, changes whether the loop advances.
- **error rule:** rule broken: continue must be inside a loop. (compile-time)
- **error rule:** rule broken: In a while loop continue goes straight to the test, skipping an update placed later in the body. (silent logic error)
- **error rule:** rule broken: Statements after continue in the same block can never run. (compile-time)
- **applicability rule:** Use continue to skip items early in a long loop body when the alternative is a deeply nested if. Avoid it in while loops whose update is at the end of the body, and avoid it when a simple if around the work is clearer. S&amp;W rarely use it.

## The whole prerequisite chain

- **Everything it builds on (16):** `arithmetic_operators`, `boolean`, `boolean_expression`, `comparison_operators`, `data_type`, `do_while_loop`, `expression`, `for_loop`, `identifier`, `literal`, `logical_operators`, `loop_control`, `loop_variable`, `primitive_type`, `variable`, `while_loop`
- **Everything that builds on it (0):** nothing
