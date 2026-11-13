# loop_variable (`loop_variable`)

the counter that drives the loop

Section 1.3 Conditionals and Loops, topic 1.3.d For loops (including i++ and scope).

![The knowledge graph around loop_variable](loop_variable.png)

## At a glance

- **Needs first:** `while_loop`
- **Leads to:** `loop_control`
- **Learned alongside:** nothing
- **Misconceptions:** `BodyChangeIgnoredByCondition`, `DoubleLoopIndexCount`, `ForInitRepeats`, `LoopOutputSameEachPass`, `LoopUpdateChangesDirection`, `LoopVariableLifetimeScope`, `LoopVariableLimitsValues`
- **Errors:** none
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 28 edges around this concept, each explained in the graph's own words.

## What it needs first (1)

A prerequisite edge means the other concept has to be understood before `loop_variable`.

### `while_loop` comes before `loop_variable`

*repeat a block while a condition holds*

A loop variable is a counter that the loop initializes, tests in its condition and increments on each pass.

- **Grounding:** book passage
- **How `loop_variable` combines with `while_loop`:** In a while loop the loop variable is declared and initialized before the loop and updated inside the body, so it remains available after the loop.
- **How `while_loop` combines with `loop_variable`:** The while condition usually tests a loop variable that is initialized before the loop and updated in the body; if the body never changes it, the loop never ends.

## What it leads to (1)

These concepts need `loop_variable` first.

### `loop_variable` comes before `loop_control`

*the three slots: init ; condition ; update*

The init, condition and update all act on the loop variable: the init sets it, the condition tests it, the update changes it.

- **Grounding:** book passage
- **How `loop_variable` combines with `loop_control`:** The init, condition and update all act on the loop variable: the init sets it, the condition tests it, the update changes it.
- **How `loop_control` combines with `loop_variable`:** All three control parts act on the loop variable: the init sets it, the condition tests it, the update changes it.

## Learned alongside (0)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

No parallel edge touches this concept.

## Misconceptions (7)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### BodyChangeIgnoredByCondition

- **Wrong rule:** Changing the loop variable inside the body does not affect the loop condition; the loop still runs its planned number of times.
- **Right rule:** The condition is tested with the current value of the variable, including changes made in the body.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: Changing the loop variable inside the body does not affect the loop condition; the loop still runs its planned number of times. Right rule: The condition is tested with the current value of the variable, including changes made in the body.
- **Also an edge from `loop_guard`:** Changing the loop variable inside the body does not affect the loop condition; the loop still runs its planned number of times.

### DoubleLoopIndexCount

- **Wrong rule:** for (double x = 0.0; x &lt;= 1.0; x += 0.1) runs exactly 11 times.
- **Right rule:** Using a double as a for-loop index is legal but bad practice: the number of iterations depends on an equality test between double values, which may not give the result you expect.
- **Role of this concept:** context
- **Shows at level L0 as:** misconception: wrong rule: for (double x = 0.0; x &lt;= 1.0; x += 0.1) runs exactly 11 times. Right rule: Using a double as a for-loop index is legal but bad practice: the number of iterations depends on an equality test between double values, which may not give the result you expect.
- **Also an edge from `for_loop`:** for (double x = 0.0; x &lt;= 1.0; x += 0.1) runs exactly 11 times.
- **Also an edge from `loop_control`:** for (double x = 0.0; x &lt;= 1.0; x += 0.1) runs exactly 11 times.
- **Also an edge from `off_by_one_error`:** for (double x = 0.0; x &lt;= 1.0; x += 0.1) runs exactly 11 times.

### ForInitRepeats

- **Wrong rule:** The initialization of a for loop runs again after a pass of the body.
- **Right rule:** The initialization runs exactly once, before the first condition test.
- **Role of this concept:** context
- **Shows at level L0 as:** misconception: wrong rule: The initialization of a for loop runs again after a pass of the body. Right rule: The initialization runs exactly once, before the first condition test.
- **Also an edge from `for_loop`:** The initialization of a for loop runs again after a pass of the body.

### LoopOutputSameEachPass

- **Wrong rule:** A loop prints the same thing on every pass; the changing loop variable does not affect what the body does.
- **Right rule:** The body uses the current value of the loop variable, so its output can differ on each pass.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: A loop prints the same thing on every pass; the changing loop variable does not affect what the body does. Right rule: The body uses the current value of the loop variable, so its output can differ on each pass.
- **Also an edge from `loop_body`:** A loop prints the same thing on every pass; the changing loop variable does not affect what the body does.

### LoopUpdateChangesDirection

- **Wrong rule:** The update of the loop variable can change from pass to pass (e.g. switch direction) although the code is the same.
- **Right rule:** The update expression is the same on every pass; the loop variable changes by the rule written in the update.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: The update of the loop variable can change from pass to pass (e.g. switch direction) although the code is the same. Right rule: The update expression is the same on every pass; the loop variable changes by the rule written in the update.
- **Shows at level L0 as:** inconsistent trace: Applies the init-test-update rule (LT, loop\_control) unevenly to the loop variable: forgets one update, applies a different step on some passes, or re-initializes it mid-loop. (here mixing in: "The update of the loop variable can change from pass to pass (e.g. switch direction) although the code is the same")
- **Also an edge from `loop_control`:** The update of the loop variable can change from pass to pass (e.g. switch direction) although the code is the same.

### LoopVariableLifetimeScope

- **Wrong rule:** The for variable i is a new variable on every pass rather than one variable changed by the update.
- **Right rule:** The for variable i is created once by the init, and the update changes that same variable on every pass.
- **Role of this concept:** context
- **Shows at level L0 as:** misconception: wrong rule: The for variable i is a new variable on every pass rather than one variable changed by the update. Right rule: The for variable i is created once by the init, the update changes that same variable on every pass, and i exists only until the end of the for statement.
- **Also an edge from `loop_scope`:** The for variable i is a new variable on every pass rather than one variable changed by the update.

### LoopVariableLimitsValues

- **Wrong rule:** The range of the loop variable limits the values that can be read or printed inside the loop.
- **Right rule:** The loop variable only counts passes; other values read or printed in the body are not bounded by it.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: The range of the loop variable limits the values that can be read or printed inside the loop. Right rule: The loop variable only counts passes; other values read or printed in the body are not bounded by it.

## Errors (0)

An error edge states the rule that gets broken in a program, and the right rule.

The graph has no error edge from this concept.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for loop variable: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to loop variable agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

loop variable -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (9 ways).

- **everyday reading** (folk-meaning rule): Folk meaning: in maths a variable like the i in a sum ranges over all its values at once, and 'i from 1 to 10' is a set. A Java loop variable is one storage location holding one value at a time, changed step by step by the update.
- **misconception** (wrong rule / right rule; shows `LoopUpdateChangesDirection`): wrong rule: The update of the loop variable can change from pass to pass (e.g. switch direction) although the code is the same. Right rule: The update expression is the same on every pass; the loop variable changes by the rule written in the update.
- **misconception** (wrong rule / right rule; shows `BodyChangeIgnoredByCondition`): wrong rule: Changing the loop variable inside the body does not affect the loop condition; the loop still runs its planned number of times. Right rule: The condition is tested with the current value of the variable, including changes made in the body.
- **misconception** (wrong rule / right rule; shows `LoopOutputSameEachPass`): wrong rule: A loop prints the same thing on every pass; the changing loop variable does not affect what the body does. Right rule: The body uses the current value of the loop variable, so its output can differ on each pass.
- **misconception** (wrong rule / right rule; shows `LoopVariableLimitsValues`): wrong rule: The range of the loop variable limits the values that can be read or printed inside the loop. Right rule: The loop variable only counts passes; other values read or printed in the body are not bounded by it.
- **inconsistent trace** (uneven-application rule; shows `LoopUpdateChangesDirection`): Applies the init-test-update rule (LT, loop\_control) unevenly to the loop variable: forgets one update, applies a different step on some passes, or re-initializes it mid-loop. (here mixing in: "The update of the loop variable can change from pass to pass (e.g. switch direction) although the code is the same")
- **misconception** (wrong rule / right rule; shows `LoopVariableLifetimeScope`): wrong rule: The for variable i is a new variable on every pass rather than one variable changed by the update. Right rule: The for variable i is created once by the init, the update changes that same variable on every pass, and i exists only until the end of the for statement.
- **misconception** (wrong rule / right rule; shows `DoubleLoopIndexCount`): wrong rule: for (double x = 0.0; x &lt;= 1.0; x += 0.1) runs exactly 11 times. Right rule: Using a double as a for-loop index is legal but bad practice: the number of iterations depends on an equality test between double values, which may not give the result you expect.
- **misconception** (wrong rule / right rule; shows `ForInitRepeats`): wrong rule: The initialization of a for loop runs again after a pass of the body. Right rule: The initialization runs exactly once, before the first condition test.

### L1: Unistructural / atom x text surface

L1 for loop variable: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

loop variable -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

- **names the element** (identity rule): A loop variable (loop-control counter, index) is a variable that is initialized, tested and updated in order to control a loop.
- **states the rule** (declarative rule): The loop variable is set once by the initialization, tested by the continuation condition before each pass and updated (usually incremented) at the end of each pass; declared in a for header, it is not available after the loop.

### L2: Multistructural / block x execution / preoperational

L2 for loop variable: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

loop variable -&gt; L2 (Multistructural): the answer applies the rules of loop variable to every part of the code, in order (3 ways).

- **line by line trace** (operational sequencing rule): Its value is set by the init, read by the test, read by the body, then changed by the update, and the cycle repeats; the body sees the value set by the previous update.
- **output prediction** (evaluation / result rule): Across passes the loop variable takes a predictable sequence of values, e.g. 4, 5, ..., 10 in TenHellos, and after a while loop it holds the first value that failed the test (11).
- **one step execution** (state-transition rule): One update changes only the loop variable (i = i + 1 turns 4 into 5); one test reads it and yields true or false; an assignment to it in the body changes what the next test sees.

### L3: Relational / relations x function (concrete operational begins)

L3 for loop variable: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

loop variable -&gt; L3 (Relational): the answer relates the parts (3 ways).

- **relation to neighbour** (composition rule (with a neighbour)): The init, condition and update all act on the loop variable: the init sets it, the condition tests it, the update changes it.
- **relation to neighbour** (composition rule (with a neighbour)): In a while loop the loop variable is declared and initialized before the loop and updated inside the body, so it remains available after the loop.
- **purpose of the whole** (plan / role rule): Role: stepper - a variable stepping through a systematic, predictable succession of values; it counts passes and often serves as an index.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for loop variable: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

loop variable -&gt; L4 (Extended abstract): the answer reasons beyond the given code (3 ways).

- **predict a change** (conservation rule; shows `LoopUpdateChangesDirection`): Shifting the start and the bound by the same amount keeps the number of passes but changes the values the body sees; assigning to the loop variable inside the body changes the pass count.
- **transfer to a new program** (applicability rule): Use a dedicated loop variable (int) when passes are counted or indexed; do not use a double loop variable, and do not reuse it for other roles inside the body.
- **diagnose an error** (error rule): rule broken: Update the loop variable only in the update part (or in one place in a while body). Kind: silent logic error. Trigger class: An extra i++ in the body (or modifying i elsewhere): passes are skipped or repeated, and the loop may overshoot an != bound and never end.

## Same topic

`loop_variable` belongs to the topic **For loops (including i++ and scope)** (`topic1.3.d`). The topic also contains: `compound_assignment`, `for_loop`, `increment_operators`, `loop_scope`, `side_effect_order`.

## Rules of the concept (20)

- **folk-meaning rule:** Folk meaning: in maths a variable like the i in a sum ranges over all its values at once, and 'i from 1 to 10' is a set. A Java loop variable is one storage location holding one value at a time, changed step by step by the update.
- **wrong rule / right rule:** LoopVariableLifetimeScope: wrong: The for variable i is a new variable on every pass rather than one variable changed by the update. \| right: The for variable i is created once by the init, the update changes that same variable on every pass, and i exists only until the end of the for statement.
- **wrong rule / right rule:** DoubleLoopIndexCount: wrong: for (double x = 0.0; x &lt;= 1.0; x += 0.1) runs exactly 11 times. \| right: Using a double as a for-loop index is legal but bad practice: the number of iterations depends on an equality test between double values, which may not give the result you expect.
- **wrong rule / right rule:** ForInitRepeats: wrong: The initialization of a for loop runs again after a pass of the body. \| right: The initialization runs exactly once, before the first condition test.
- **wrong rule / right rule:** LoopUpdateChangesDirection: wrong: The update of the loop variable can change from pass to pass (e.g. switch direction) although the code is the same. \| right: The update expression is the same on every pass; the loop variable changes by the rule written in the update.
- **wrong rule / right rule:** BodyChangeIgnoredByCondition: wrong: Changing the loop variable inside the body does not affect the loop condition; the loop still runs its planned number of times. \| right: The condition is tested with the current value of the variable, including changes made in the body.
- **wrong rule / right rule:** LoopOutputSameEachPass: wrong: A loop prints the same thing on every pass; the changing loop variable does not affect what the body does. \| right: The body uses the current value of the loop variable, so its output can differ on each pass.
- **wrong rule / right rule:** LoopVariableLimitsValues: wrong: The range of the loop variable limits the values that can be read or printed inside the loop. \| right: The loop variable only counts passes; other values read or printed in the body are not bounded by it.
- **uneven-application rule:** Applies the init-test-update rule (LT, loop\_control) unevenly to the loop variable: forgets one update, applies a different step on some passes, or re-initializes it mid-loop.
- **identity rule:** A loop variable (loop-control counter, index) is a variable that is initialized, tested and updated in order to control a loop.
- **declarative rule:** The loop variable is set once by the initialization, tested by the continuation condition before each pass and updated (usually incremented) at the end of each pass; declared in a for header, it is not available after the loop.
- **operational sequencing rule:** Its value is set by the init, read by the test, read by the body, then changed by the update, and the cycle repeats; the body sees the value set by the previous update.
- **evaluation / result rule:** Across passes the loop variable takes a predictable sequence of values, e.g. 4, 5, ..., 10 in TenHellos, and after a while loop it holds the first value that failed the test (11).
- **state-transition rule:** One update changes only the loop variable (i = i + 1 turns 4 into 5); one test reads it and yields true or false; an assignment to it in the body changes what the next test sees.
- **composition rule (with a neighbour):** with loop\_control: The init, condition and update all act on the loop variable: the init sets it, the condition tests it, the update changes it.
- **composition rule (with a neighbour):** with while\_loop: In a while loop the loop variable is declared and initialized before the loop and updated inside the body, so it remains available after the loop.
- **plan / role rule:** Role: stepper - a variable stepping through a systematic, predictable succession of values; it counts passes and often serves as an index.
- **conservation rule:** Shifting the start and the bound by the same amount keeps the number of passes but changes the values the body sees; assigning to the loop variable inside the body changes the pass count.
- **error rule:** rule broken: Update the loop variable only in the update part (or in one place in a while body). (silent logic error)
- **applicability rule:** Use a dedicated loop variable (int) when passes are counted or indexed; do not use a double loop variable, and do not reuse it for other roles inside the body.

## The whole prerequisite chain

- **Everything it builds on (12):** `arithmetic_operators`, `boolean`, `boolean_expression`, `comparison_operators`, `data_type`, `expression`, `identifier`, `literal`, `logical_operators`, `primitive_type`, `variable`, `while_loop`
- **Everything that builds on it (35):** `accumulator_pattern`, `array_copy`, `array_reversal`, `array_traversal`, `boolean_flag_array`, `break_statement`, `continue_statement`, `convergence_rate`, `counter_pattern`, `enhanced_for`, `fencepost_loop`, `flag_search_loop`, `for_loop`, `frequency_counting`, `function_plotting`, `increment_operators`, `infinite_loop`, `labeled_break`, `loop_body`, `loop_control`, `loop_performance`, `loop_scope`, `matrix_operations`, `monte_carlo_simulation`, `nested_loops`, `off_by_one_error`, `power_method`, `row_major_order`, `running_extreme`, `sentinel_loop`, `side_effect_order`, `simulation_loop`, `standard_audio`, `switch_statement`, `two_models`
