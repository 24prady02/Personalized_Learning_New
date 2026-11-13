# for_loop (`for_loop`)

a while with init/condition/update packaged together

Section 1.3 Conditionals and Loops, topic 1.3.d For loops (including i++ and scope).

![The knowledge graph around for_loop](for_loop.png)

## At a glance

- **Needs first:** `loop_control`
- **Leads to:** `array_traversal`, `break_statement`, `continue_statement`, `fencepost_loop`, `flag_search_loop`, `infinite_loop`, `loop_body`, `loop_scope`, `nested_loops`, `simulation_loop`
- **Learned alongside:** nothing
- **Misconceptions:** `DoubleLoopIndexCount`, `FalseLoopRepeatsNextCode`, `ForInitRepeats`, `ForIsConditional`, `ForLoopPartSkipped`, `ForUpdateBeforeBody`, `ForWhileNotInterchangeable`, `IdiomOverridesCode`, `LoopCountIsStatementCount`, `LoopHeaderIsEquations`, `LoopImpliedByOneTest`, `LoopStepAlwaysOne`, `MissingBraces`, `ProgramEndsAfterLoop`, `ReturnDoesNotExitLoop`, `SingleIterationInsteadOfLoop`
- **Errors:** `BracelessMultiStatementBody`, `ForCommaSeparators`, `SemicolonAfterIfHeader`, `SemicolonAfterLoopHeader`, `WrongIterationCount`
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 80 edges around this concept, each explained in the graph's own words.

## What it needs first (1)

A prerequisite edge means the other concept has to be understood before `for_loop`.

### `loop_control` comes before `for_loop`

*the three slots: init ; condition ; update*

The for header is exactly the three control slots, and the body runs after the test and before the update on each pass.

- **Grounding:** book passage
- **How `for_loop` combines with `loop_control`:** The for header is exactly the three loop-control slots; the body runs after the test and before the update on each pass.
- **How `loop_control` combines with `for_loop`:** The for header is exactly the three control slots, separated by semicolons; the body runs after the test and before the update.

## What it leads to (10)

These concepts need `for_loop` first.

### `for_loop` comes before `array_traversal`

*walking the array with an index loop*

for (int i = 0; i &lt; a.length; i++) gives i every valid index exactly once, in increasing order.

- **Grounding:** book passage
- **How `for_loop` combines with `array_traversal`:** for (int i = 0; i &lt; N; i++) gives i each valid index 0..N-1 exactly once in increasing order, the standard way to process every array element.
- **How `array_traversal` combines with `for_loop`:** for (int i = 0; i &lt; a.length; i++) gives i every valid index exactly once, in increasing order; the bound must be &lt; a.length, not &lt;=.

### `for_loop` comes before `break_statement`

*break -- immediately exits the innermost loop or switch*

break leaves the for loop at once, without running the rest of the body or the remaining passes.

- **Grounding:** book passage

### `for_loop` comes before `continue_statement`

*continue -- skips to the next iteration of the innermost loop*

continue skips the rest of the loop body; in a for loop control goes straight to the increment statement and then the next test.

- **Grounding:** book passage
- **How `for_loop` combines with `continue_statement`:** In a for loop, continue skips the rest of the body and transfers control directly to the increment, then the next test; this is one of the few places where the for/while equivalence fails.
- **How `continue_statement` combines with `for_loop`:** In a for loop the increment still runs after continue, so the loop always advances. This is why the for/while equivalence has an exception: in the rewritten while, a continue jumps past the \`&lt;increment&gt;;\` at the end of the body.

### `for_loop` comes before `fencepost_loop`

*n items need n - 1 separators: one item handled outside the loop*

A fencepost loop is a for loop with one item handled outside it.

- **Grounding:** questionable
- **How `for_loop` combines with `fencepost_loop`:** A fencepost loop is a for loop that handles one item (the first or last) outside the loop so that separators come out n-1 times for n items.
- **How `fencepost_loop` combines with `for_loop`:** The for loop's bounds must match the handled-outside item: if a[0] is printed before the loop, the loop must start at \`i = 1\`. Starting at 0 duplicates the first item, and \`i &lt;= n\` runs past the end.

### `for_loop` comes before `flag_search_loop`

*a boolean flag that a loop sets once and never resets*

A flag search loop sets a boolean flag inside a loop when a pass finds the condition, and leaves it set afterwards.

- **Grounding:** questionable
- **How `for_loop` combines with `flag_search_loop`:** A flag search loop is a for loop that sets a boolean flag when some pass finds the target and leaves it set afterwards; the flag must be declared before the loop.
- **How `flag_search_loop` combines with `for_loop`:** The flag must be declared before the for loop to be visible after it. The for loop's test can include \`!found\` to stop at the first find; without that, the loop runs all passes, and the flag still works because it is one-way.

### `for_loop` comes before `infinite_loop`

*a loop whose condition never becomes false*

A for loop whose condition never becomes false (or is left out) repeats forever unless a break ends it.

- **Grounding:** spec passage

### `for_loop` comes before `loop_body`

*the block repeated each pass*

The statements in braces after the for header are the loop body; they run once on every pass, between the test and the increment, exactly as in a while loop.

- **Grounding:** book passage

### `for_loop` comes before `loop_scope`

*lifetime/scope of variables in/around the loop*

A variable declared in the for header exists only from its declaration to the end of the for statement's block.

- **Grounding:** book passage
- **How `for_loop` combines with `loop_scope`:** A variable declared in the for header is in scope only in the header and the body, so it cannot be used after the loop.
- **How `loop_scope` combines with `for_loop`:** A variable declared in the for header exists only from its declaration to the end of the for statement, so for and while versions differ: in the while version the counter is still available after the loop.

### `for_loop` comes before `nested_loops`

*a loop inside a loop*

In nested loops the inner for runs its complete set of passes for every single pass of the outer for.

- **Grounding:** book passage
- **How `for_loop` combines with `nested_loops`:** A for may be the body of another for: the inner for runs its complete set of passes for every single pass of the outer one.
- **How `nested_loops` combines with `for_loop`:** Usually both loops are for loops: the inner for runs its complete set of passes for every single pass of the outer for.

### `for_loop` comes before `simulation_loop`

*take many random steps*

The simulation is a for loop over t = 0 ... T - 1 that makes one random move per pass.

- **Grounding:** book passage
- **How `for_loop` combines with `simulation_loop`:** A simulation runs a fixed number of trials with an outer for loop (for (int t = 0; t &lt; T; t++)), each trial simulated inside the body.
- **How `simulation_loop` combines with `for_loop`:** A counted for loop with t &lt; T fixes the number of moves at T; the loop variable t is scoped to the loop.

## Learned alongside (0)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

No parallel edge touches this concept.

## Misconceptions (16)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### DoubleLoopIndexCount

- **Wrong rule:** for (double x = 0.0; x &lt;= 1.0; x += 0.1) runs exactly 11 times.
- **Right rule:** Using a double as a for-loop index is legal but bad practice: the number of iterations depends on an equality test between double values, which may not give the result you expect.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: for (double x = 0.0; x &lt;= 1.0; x += 0.1) runs exactly 11 times. Right rule: Using a double as a for-loop index is legal but bad practice: the number of iterations depends on an equality test between double values, which may not give the result you expect.
- **Also an edge from `loop_control`:** for (double x = 0.0; x &lt;= 1.0; x += 0.1) runs exactly 11 times.
- **Also an edge from `loop_variable`:** for (double x = 0.0; x &lt;= 1.0; x += 0.1) runs exactly 11 times.
- **Also an edge from `off_by_one_error`:** for (double x = 0.0; x &lt;= 1.0; x += 0.1) runs exactly 11 times.

### FalseLoopRepeatsNextCode

- **Wrong rule:** A loop is an iterative if-else: while the condition is true the body repeats, and when it is false the code after the loop repeats.
- **Right rule:** Only the body is repeated; once the condition is false the code after the loop runs once.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: A loop is an iterative if-else: while the condition is true the body repeats, and when it is false the code after the loop repeats. Right rule: Only the body is repeated; once the condition is false the code after the loop runs once.
- **Also an edge from `control_flow`:** A loop is an iterative if-else: while the condition is true the body repeats, and when it is false the code after the loop repeats.
- **Also an edge from `while_loop`:** A loop is an iterative if-else: while the condition is true the body repeats, and when it is false the code after the loop repeats.

### ForInitRepeats

- **Wrong rule:** The initialization of a for loop runs again after a pass of the body.
- **Right rule:** The initialization runs exactly once, before the first condition test.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: The initialization of a for loop runs again after a pass of the body. Right rule: The initialization runs exactly once, before the first condition test.
- **Also an edge from `loop_variable`:** The initialization of a for loop runs again after a pass of the body.

### ForIsConditional

- **Wrong rule:** The body of a for statement executes at most once.
- **Right rule:** The body of a for statement runs once for every pass on which the condition is true, which can be many times.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: The body of a for statement executes at most once. Right rule: The body of a for statement runs once for every pass on which the condition is true, which can be many times.
- **Shows at level L0 as:** inconsistent trace: Applies the for sequencing rule (LT) unevenly: updates before the body on the first pass only, re-runs the init after a pass, or skips the test on some passes. (here mixing in: "The body of a for statement executes at most once")

### ForLoopPartSkipped

- **Wrong rule:** A pass of a loop may leave out one of its parts (the condition test, the body, the update, or the initialization).
- **Right rule:** Each pass of a for loop runs test, then body, then update, every time; the initialization runs once, at the start.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: A pass of a loop may leave out one of its parts (the condition test, the body, the update, or the initialization). Right rule: Each pass of a for loop runs test, then body, then update, every time; the initialization runs once, at the start.
- **Also an edge from `loop_body`:** A pass of a loop may leave out one of its parts (the condition test, the body, the update, or the initialization).
- **Also an edge from `loop_control`:** A pass of a loop may leave out one of its parts (the condition test, the body, the update, or the initialization).

### ForUpdateBeforeBody

- **Wrong rule:** The update part of a for header (e.g. i = i - 4) runs before the body on each pass, so the first pass already sees the updated value.
- **Right rule:** The update runs after the body, before the next condition test; the first pass uses the initial value.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: The update part of a for header (e.g. i = i - 4) runs before the body on each pass, so the first pass already sees the updated value. Right rule: The update runs after the body, before the next condition test; the first pass uses the initial value.
- **Also an edge from `loop_control`:** The update part of a for header (e.g. i = i - 4) runs before the body on each pass, so the first pass already sees the updated value.

### ForWhileNotInterchangeable

- **Wrong rule:** Some loops can only be written with for, others only with while.
- **Right rule:** Any for loop can be rewritten as a while loop and vice versa; for just packages init, test and update.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: Some loops can only be written with for, others only with while. Right rule: Any for loop can be rewritten as a while loop and vice versa; for just packages init, test and update.
- **Also an edge from `while_loop`:** Some loops can only be written with for, others only with while.

### IdiomOverridesCode

- **Wrong rule:** An array loop processes the whole array from index 0 to length-1 and increments its index at the end of the body, whatever the code says.
- **Right rule:** The loop visits exactly the indices that its initialisation, guard and update produce, in the order in which its statements are written.
- **Role of this concept:** context
- **Shows at level L0 as:** misconception: wrong rule: An array loop processes the whole array from index 0 to length-1 and increments its index at the end of the body, whatever the code says. Right rule: The loop visits exactly the indices that its initialisation, guard and update produce, in the order in which its statements are written.
- **Also an edge from `array_traversal`:** An array loop processes the whole array from index 0 to length-1 and increments its index at the end of the body, whatever the code says.
- **Also an edge from `increment_operators`:** An array loop processes the whole array from index 0 to length-1 and increments its index at the end of the body, whatever the code says.
- **Also an edge from `loop_control`:** An array loop processes the whole array from index 0 to length-1 and increments its index at the end of the body, whatever the code says.

### LoopCountIsStatementCount

- **Wrong rule:** The repeat count of a counted loop says how many of the body statements are executed.
- **Right rule:** The repeat count is how many times the whole body runs; every pass runs all body statements.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: The repeat count of a counted loop says how many of the body statements are executed. Right rule: The repeat count is how many times the whole body runs; every pass runs all body statements.
- **Also an edge from `loop_body`:** The repeat count of a counted loop says how many of the body statements are executed.

### LoopHeaderIsEquations

- **Wrong rule:** The initialization, condition and update of a for header are equations that all hold at the same time.
- **Right rule:** The three header parts are statements run at different moments: init once, then condition test, body, update, repeated.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: The initialization, condition and update of a for header are equations that all hold at the same time. Right rule: The three header parts are statements run at different moments: init once, then condition test, body, update, repeated.
- **Also an edge from `loop_control`:** The initialization, condition and update of a for header are equations that all hold at the same time.

### LoopImpliedByOneTest

- **Wrong rule:** Testing one case is enough; Java will repeat the test for the other values by itself.
- **Right rule:** A statement runs once each time control reaches it; repeating a test for many values needs a loop.
- **Role of this concept:** context
- **Shows at level L0 as:** misconception: wrong rule: Testing one case is enough; Java will repeat the test for the other values by itself. Right rule: A statement runs once each time control reaches it; repeating a test for many values needs a loop.
- **Also an edge from `control_flow`:** Testing one case is enough; Java will repeat the test for the other values by itself.
- **Also an edge from `while_loop`:** Testing one case is enough; Java will repeat the test for the other values by itself.

### LoopStepAlwaysOne

- **Wrong rule:** A loop variable always goes up or down by 1, whatever the update says (so i = i - 4 is read as i--).
- **Right rule:** The loop variable changes exactly as the update expression says (i += 2, i = i - 4, i \*= 2, ...).
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: A loop variable always goes up or down by 1, whatever the update says (so i = i - 4 is read as i--). Right rule: The loop variable changes exactly as the update expression says (i += 2, i = i - 4, i \*= 2, ...).
- **Also an edge from `loop_control`:** A loop variable always goes up or down by 1, whatever the update says (so i = i - 4 is read as i--).

### MissingBraces

- **Wrong rule:** Omits braces around a single-statement body of if, for or while.
- **Right rule:** Braces are optional for a single-statement body, but using them anyway avoids bugs when statements are added later.
- **Role of this concept:** context
- **Also an edge from `block`:** Omits braces around a single-statement body of if, for or while.
- **Also an edge from `if_statement`:** Omits braces around a single-statement body of if, for or while.
- **Also an edge from `while_loop`:** Omits braces around a single-statement body of if, for or while.

### ProgramEndsAfterLoop

- **Wrong rule:** When a loop finishes the program ends, so code after the loop never runs.
- **Right rule:** When the loop condition becomes false, control continues with the first statement after the loop.
- **Role of this concept:** context
- **Shows at level L0 as:** misconception: wrong rule: When a loop finishes the program ends, so code after the loop never runs. Right rule: When the loop condition becomes false, control continues with the first statement after the loop.
- **Also an edge from `control_flow`:** When a loop finishes the program ends, so code after the loop never runs.
- **Also an edge from `while_loop`:** When a loop finishes the program ends, so code after the loop never runs.

### ReturnDoesNotExitLoop

- **Wrong rule:** A return inside a loop does not end the loop; it sets a value each pass (the last one is returned) or returns several values.
- **Right rule:** When return executes, the method ends at once, so the loop stops on that pass.
- **Role of this concept:** context
- **Also an edge from `control_flow`:** A return inside a loop does not end the loop; it sets a value each pass (the last one is returned) or returns several values.
- **Also an edge from `flag_search_loop`:** A return inside a loop does not end the loop; it sets a value each pass (the last one is returned) or returns several values.

### SingleIterationInsteadOfLoop

- **Wrong rule:** A task that must be repeated is written once, without a loop, as if one pass were enough.
- **Right rule:** A step that must happen several times (or an unknown number of times) needs a loop such as while or for; code without a loop runs once.
- **Role of this concept:** context
- **Also an edge from `while_loop`:** A task that must be repeated is written once, without a loop, as if one pass were enough.

## Errors (5)

An error edge states the rule that gets broken in a program, and the right rule.

### BracelessMultiStatementBody

- **Wrong rule:** Indenting several statements under an if or for makes them all part of its body, even without braces.
- **Right rule:** Without braces only the first statement belongs to the if/for; the rest run once, after it.
- **Role of this concept:** context
- **Also an edge from `if_statement`:** Indenting several statements under an if or for makes them all part of its body, even without braces.
- **Also an edge from `loop_body`:** Indenting several statements under an if or for makes them all part of its body, even without braces.
- **Also an edge from `nested_loops`:** Indenting several statements under an if or for makes them all part of its body, even without braces.

### ForCommaSeparators

- **Wrong rule:** Writes for (int i = 0, i &lt; n, i++).
- **Right rule:** The three parts of a for header are separated by semicolons; commas only separate several statements inside the init or the update part.
- **Role of this concept:** primary

### SemicolonAfterIfHeader

- **Wrong rule:** if (x &gt; 0); System.out.println("positive"); prints only for positive x.
- **Right rule:** The ; ends the if with an empty statement, so the next line always runs.
- **Role of this concept:** context
- **Also an edge from `empty_statement`:** if (x &gt; 0); System.out.println("positive"); prints only for positive x.
- **Also an edge from `if_statement`:** if (x &gt; 0); System.out.println("positive"); prints only for positive x.
- **Also an edge from `logical_error`:** if (x &gt; 0); System.out.println("positive"); prints only for positive x.
- **Also an edge from `while_loop`:** if (x &gt; 0); System.out.println("positive"); prints only for positive x.

### SemicolonAfterLoopHeader

- **Wrong rule:** Puts a ; right after for (...) or while (...).
- **Right rule:** A ; right after the loop header is a null (empty) loop body, so the statements written after it are not repeated by the loop.
- **Role of this concept:** primary
- **Also an edge from `empty_statement`:** Puts a ; right after for (...) or while (...).
- **Also an edge from `while_loop`:** Puts a ; right after for (...) or while (...).

### WrongIterationCount

- **Wrong rule:** Updates the loop counter so that the loop runs the wrong number of times.
- **Right rule:** The init, test and update together decide the number of passes; trace them to check the count.
- **Role of this concept:** primary
- **Also an edge from `loop_control`:** Updates the loop counter so that the loop runs the wrong number of times.
- **Also an edge from `off_by_one_error`:** Updates the loop counter so that the loop runs the wrong number of times.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for for loop: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to for loop agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

for loop -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (15 ways).

- **everyday reading** (folk-meaning rule): Folk meaning: English 'for each ...' or 'for 10 times' names a whole collection or a count to be handled at once, and a maths reading treats the header as simultaneous conditions. A Java for is a while loop in compact form: one init, then test-body-update repeated, one pass at a time.
- **misconception** (wrong rule / right rule; shows `ForIsConditional`): wrong rule: The body of a for statement executes at most once. Right rule: The body of a for statement runs once for every pass on which the condition is true, which can be many times.
- **misconception** (wrong rule / right rule; shows `DoubleLoopIndexCount`): wrong rule: for (double x = 0.0; x &lt;= 1.0; x += 0.1) runs exactly 11 times. Right rule: Using a double as a for-loop index is legal but bad practice: the number of iterations depends on an equality test between double values, which may not give the result you expect.
- **misconception** (wrong rule / right rule; shows `ForWhileNotInterchangeable`): wrong rule: Some loops can only be written with for, others only with while. Right rule: Any for loop can be rewritten as a while loop and vice versa; for just packages init, test and update.
- **misconception** (wrong rule / right rule; shows `LoopHeaderIsEquations`): wrong rule: The initialization, condition and update of a for header are equations that all hold at the same time. Right rule: The three header parts are statements run at different moments: init once, then condition test, body, update, repeated.
- **misconception** (wrong rule / right rule; shows `LoopCountIsStatementCount`): wrong rule: The repeat count of a counted loop says how many of the body statements are executed. Right rule: The repeat count is how many times the whole body runs; every pass runs all body statements.
- **misconception** (wrong rule / right rule; shows `FalseLoopRepeatsNextCode`): wrong rule: A loop is an iterative if-else: while the condition is true the body repeats, and when it is false the code after the loop repeats. Right rule: Only the body is repeated; once the condition is false the code after the loop runs once.
- **misconception** (wrong rule / right rule; shows `ForLoopPartSkipped`): wrong rule: A pass of a loop may leave out one of its parts (the condition test, the body, the update, or the initialization). Right rule: Each pass of a for loop runs test, then body, then update, every time; the initialization runs once, at the start.
- **misconception** (wrong rule / right rule; shows `ForInitRepeats`): wrong rule: The initialization of a for loop runs again after a pass of the body. Right rule: The initialization runs exactly once, before the first condition test.
- **misconception** (wrong rule / right rule; shows `ForUpdateBeforeBody`): wrong rule: The update part of a for header (e.g. i = i - 4) runs before the body on each pass, so the first pass already sees the updated value. Right rule: The update runs after the body, before the next condition test; the first pass uses the initial value.
- **misconception** (wrong rule / right rule; shows `LoopStepAlwaysOne`): wrong rule: A loop variable always goes up or down by 1, whatever the update says (so i = i - 4 is read as i--). Right rule: The loop variable changes exactly as the update expression says (i += 2, i = i - 4, i \*= 2, ...).
- **inconsistent trace** (uneven-application rule; shows `ForIsConditional`): Applies the for sequencing rule (LT) unevenly: updates before the body on the first pass only, re-runs the init after a pass, or skips the test on some passes. (here mixing in: "The body of a for statement executes at most once")
- **misconception** (wrong rule / right rule; shows `LoopImpliedByOneTest`): wrong rule: Testing one case is enough; Java will repeat the test for the other values by itself. Right rule: A statement runs once each time control reaches it; repeating a test for many values needs a loop.
- **misconception** (wrong rule / right rule; shows `IdiomOverridesCode`): wrong rule: An array loop processes the whole array from index 0 to length-1 and increments its index at the end of the body, whatever the code says. Right rule: The loop visits exactly the indices that its initialisation, guard and update produce, in the order in which its statements are written.
- **misconception** (wrong rule / right rule; shows `ProgramEndsAfterLoop`): wrong rule: When a loop finishes the program ends, so code after the loop never runs. Right rule: When the loop condition becomes false, control continues with the first statement after the loop.

### L1: Unistructural / atom x text surface

L1 for for loop: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

for loop -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

- **names the element** (identity rule): The for statement is a loop that packages an initialization, a loop-continuation condition and an increment in its header around a body.
- **states the rule** (declarative rule): Syntax: for (&lt;initialize&gt;; &lt;boolean expression&gt;; &lt;increment&gt;) { &lt;statements&gt; }, with the three parts separated by semicolons; it is, with only a few exceptions, equivalent to &lt;initialize&gt;; while (&lt;boolean expression&gt;) { &lt;statements&gt; &lt;increment&gt;; }.

### L2: Multistructural / block x execution / preoperational

L2 for for loop: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

for loop -&gt; L2 (Multistructural): the answer applies the rules of for loop to every part of the code, in order (3 ways).

- **line by line trace** (operational sequencing rule): Run the initializer once; then repeatedly: test the condition (stop if false), execute the body, run the update.
- **output prediction** (evaluation / result rule): A for statement has no value; the passes it makes are fixed by its header: for (int i = 1; i &lt;= N; i++) sum += i; leaves sum = N(N+1)/2, and for (int i = 2; i &lt;= 8; i += 2) prints 2, 4, 6, 8,.
- **one step execution** (state-transition rule): One pass: the test reads the loop variable; the body applies its changes once; the update then changes the loop variable by its rule; the initializer changes state only once, before the first test.

### L3: Relational / relations x function (concrete operational begins)

L3 for for loop: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

for loop -&gt; L3 (Relational): the answer relates the parts (9 ways).

- **relation to neighbour** (composition rule (with a neighbour)): The for header is exactly the three loop-control slots; the body runs after the test and before the update on each pass.
- **relation to neighbour** (composition rule (with a neighbour)): A for may be the body of another for: the inner for runs its complete set of passes for every single pass of the outer one.
- **relation to neighbour** (composition rule (with a neighbour)): for (int i = 0; i &lt; N; i++) gives i each valid index 0..N-1 exactly once in increasing order, the standard way to process every array element.
- **relation to neighbour** (composition rule (with a neighbour)): A simulation runs a fixed number of trials with an outer for loop (for (int t = 0; t &lt; T; t++)), each trial simulated inside the body.
- **relation to neighbour** (composition rule (with a neighbour)): In a for loop, continue skips the rest of the body and transfers control directly to the increment, then the next test; this is one of the few places where the for/while equivalence fails.
- **relation to neighbour** (composition rule (with a neighbour)): A variable declared in the for header is in scope only in the header and the body, so it cannot be used after the loop.
- **relation to neighbour** (composition rule (with a neighbour)): A fencepost loop is a for loop that handles one item (the first or last) outside the loop so that separators come out n-1 times for n items.
- **relation to neighbour** (composition rule (with a neighbour)): A flag search loop is a for loop that sets a boolean flag when some pass finds the target and leaves it set afterwards; the flag must be declared before the loop.
- **purpose of the whole** (plan / role rule): Plan: counted loop / counter-controlled repetition - do the body a known number of times, with the loop variable as a stepper (index, term number, trial number).

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for for loop: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

for loop -&gt; L4 (Extended abstract): the answer reasons beyond the given code (8 ways).

- **predict a change** (conservation rule; shows `ForIsConditional`): Rewriting a for as the equivalent while (init before, update at the end of the body) keeps behaviour, except that continue then skips the update and the loop variable stays in scope after the loop. Changing the bound or the step changes the pass count predictably (&lt; to &lt;= adds one pass).
- **diagnose an error** (error rule): rule broken: The three parts of a for header are separated by semicolons; commas only separate several statements inside the init or the update. Kind: compile-time. Trigger class: Writing for (int i = 0, i &lt; n, i++): the compiler parses the commas as more declarators in the init and reports a syntax error.
- **diagnose an error** (error rule): rule broken: A ; right after while (...) or for (...) is an empty statement that is the whole loop body; the block written next is not repeated. Kind: silent logic error. Trigger class: for (...); { body } runs the body once after the loop ends; while (cond); with a cond that the empty body cannot change hangs forever (infinite loop) when cond starts true.
- **transfer to a new program** (applicability rule): Use for when there is an initialization, an increment and a continuation test and the loop variable is not needed after the loop; use while when the loop variable is needed later or the number of passes depends on what happens in the body.
- **diagnose an error** (error rule): rule broken: A ; right after if (...) is an empty statement that forms the whole then branch; the following statement or block is no longer part of the if. Kind: silent logic error. Trigger class: Any if (cond); followed by a statement or block: that statement runs for every input, whatever cond is (it compiles without error).
- **diagnose an error** (error rule): rule broken: The number of passes is fixed by the init, the test and the update together. Kind: silent logic error. Trigger class: Wrong start value, &lt; vs &lt;=, a wrong step, or an extra update of the counter in the body (or outside the loop): the loop runs too few or too many passes (off by one, or skips values).
- **diagnose an error** (error rule): rule broken: Without braces, the body of an if, while or for is exactly one statement; indentation does not add statements to it. Kind: silent logic error. Trigger class: A braceless header followed by two or more indented statements: only the first is controlled, the others run once, after the if/loop, on every input.
- **diagnose an error** (error rule): rule broken: A variable declared in the for initializer exists only inside the for statement. Kind: compile-time. Trigger class: Reading i after for (int i = 0; ...) {...}: 'cannot find symbol'.

## Same topic

`for_loop` belongs to the topic **For loops (including i++ and scope)** (`topic1.3.d`). The topic also contains: `compound_assignment`, `increment_operators`, `loop_scope`, `loop_variable`, `side_effect_order`.

## Rules of the concept (37)

- **folk-meaning rule:** Folk meaning: English 'for each ...' or 'for 10 times' names a whole collection or a count to be handled at once, and a maths reading treats the header as simultaneous conditions. A Java for is a while loop in compact form: one init, then test-body-update repeated, one pass at a time.
- **wrong rule / right rule:** ForIsConditional: wrong: The body of a for statement executes at most once. \| right: The body of a for statement runs once for every pass on which the condition is true, which can be many times.
- **wrong rule / right rule:** DoubleLoopIndexCount: wrong: for (double x = 0.0; x &lt;= 1.0; x += 0.1) runs exactly 11 times. \| right: Using a double as a for-loop index is legal but bad practice: the number of iterations depends on an equality test between double values, which may not give the result you expect.
- **wrong rule / right rule:** ForWhileNotInterchangeable: wrong: Some loops can only be written with for, others only with while. \| right: Any for loop can be rewritten as a while loop and vice versa; for just packages init, test and update.
- **wrong rule / right rule:** LoopImpliedByOneTest: wrong: Testing one case is enough; Java will repeat the test for the other values by itself. \| right: A statement runs once each time control reaches it; repeating a test for many values needs a loop.
- **wrong rule / right rule:** IdiomOverridesCode: wrong: An array loop processes the whole array from index 0 to length-1 and increments its index at the end of the body, whatever the code says. \| right: The loop visits exactly the indices that its initialisation, guard and update produce, in the order in which its statements are written.
- **wrong rule / right rule:** LoopHeaderIsEquations: wrong: The initialization, condition and update of a for header are equations that all hold at the same time. \| right: The three header parts are statements run at different moments: init once, then condition test, body, update, repeated.
- **wrong rule / right rule:** LoopCountIsStatementCount: wrong: The repeat count of a counted loop says how many of the body statements are executed. \| right: The repeat count is how many times the whole body runs; every pass runs all body statements.
- **wrong rule / right rule:** ProgramEndsAfterLoop: wrong: When a loop finishes the program ends, so code after the loop never runs. \| right: When the loop condition becomes false, control continues with the first statement after the loop.
- **wrong rule / right rule:** FalseLoopRepeatsNextCode: wrong: A loop is an iterative if-else: while the condition is true the body repeats, and when it is false the code after the loop repeats. \| right: Only the body is repeated; once the condition is false the code after the loop runs once.
- **wrong rule / right rule:** ForLoopPartSkipped: wrong: A pass of a loop may leave out one of its parts (the condition test, the body, the update, or the initialization). \| right: Each pass of a for loop runs test, then body, then update, every time; the initialization runs once, at the start.
- **wrong rule / right rule:** ForInitRepeats: wrong: The initialization of a for loop runs again after a pass of the body. \| right: The initialization runs exactly once, before the first condition test.
- **wrong rule / right rule:** ForUpdateBeforeBody: wrong: The update part of a for header (e.g. i = i - 4) runs before the body on each pass, so the first pass already sees the updated value. \| right: The update runs after the body, before the next condition test; the first pass uses the initial value.
- **wrong rule / right rule:** LoopStepAlwaysOne: wrong: A loop variable always goes up or down by 1, whatever the update says (so i = i - 4 is read as i--). \| right: The loop variable changes exactly as the update expression says (i += 2, i = i - 4, i \*= 2, ...).
- **uneven-application rule:** Applies the for sequencing rule (LT) unevenly: updates before the body on the first pass only, re-runs the init after a pass, or skips the test on some passes.
- **identity rule:** The for statement is a loop that packages an initialization, a loop-continuation condition and an increment in its header around a body.
- **declarative rule:** Syntax: for (&lt;initialize&gt;; &lt;boolean expression&gt;; &lt;increment&gt;) { &lt;statements&gt; }, with the three parts separated by semicolons; it is, with only a few exceptions, equivalent to &lt;initialize&gt;; while (&lt;boolean expression&gt;) { &lt;statements&gt; &lt;increment&gt;; }.
- **operational sequencing rule:** Run the initializer once; then repeatedly: test the condition (stop if false), execute the body, run the update.
- **evaluation / result rule:** A for statement has no value; the passes it makes are fixed by its header: for (int i = 1; i &lt;= N; i++) sum += i; leaves sum = N(N+1)/2, and for (int i = 2; i &lt;= 8; i += 2) prints 2, 4, 6, 8,.
- **state-transition rule:** One pass: the test reads the loop variable; the body applies its changes once; the update then changes the loop variable by its rule; the initializer changes state only once, before the first test.
- **composition rule (with a neighbour):** with loop\_control: The for header is exactly the three loop-control slots; the body runs after the test and before the update on each pass.
- **composition rule (with a neighbour):** with nested\_loops: A for may be the body of another for: the inner for runs its complete set of passes for every single pass of the outer one.
- **composition rule (with a neighbour):** with array\_traversal: for (int i = 0; i &lt; N; i++) gives i each valid index 0..N-1 exactly once in increasing order, the standard way to process every array element.
- **composition rule (with a neighbour):** with simulation\_loop: A simulation runs a fixed number of trials with an outer for loop (for (int t = 0; t &lt; T; t++)), each trial simulated inside the body.
- **composition rule (with a neighbour):** with continue\_statement: In a for loop, continue skips the rest of the body and transfers control directly to the increment, then the next test; this is one of the few places where the for/while equivalence fails.
- **composition rule (with a neighbour):** with loop\_scope: A variable declared in the for header is in scope only in the header and the body, so it cannot be used after the loop.
- **composition rule (with a neighbour):** with fencepost\_loop: A fencepost loop is a for loop that handles one item (the first or last) outside the loop so that separators come out n-1 times for n items.
- **composition rule (with a neighbour):** with flag\_search\_loop: A flag search loop is a for loop that sets a boolean flag when some pass finds the target and leaves it set afterwards; the flag must be declared before the loop.
- **plan / role rule:** Plan: counted loop / counter-controlled repetition - do the body a known number of times, with the loop variable as a stepper (index, term number, trial number).
- **conservation rule:** Rewriting a for as the equivalent while (init before, update at the end of the body) keeps behaviour, except that continue then skips the update and the loop variable stays in scope after the loop. Changing the bound or the step changes the pass count predictably (&lt; to &lt;= adds one pass).
- **error rule:** rule broken: The three parts of a for header are separated by semicolons; commas only separate several statements inside the init or the update. (compile-time)
- **error rule:** rule broken: A ; right after if (...) is an empty statement that forms the whole then branch; the following statement or block is no longer part of the if. (silent logic error)
- **error rule:** rule broken: A ; right after while (...) or for (...) is an empty statement that is the whole loop body; the block written next is not repeated. (silent logic error)
- **error rule:** rule broken: The number of passes is fixed by the init, the test and the update together. (silent logic error)
- **error rule:** rule broken: Without braces, the body of an if, while or for is exactly one statement; indentation does not add statements to it. (silent logic error)
- **error rule:** rule broken: A variable declared in the for initializer exists only inside the for statement. (compile-time)
- **applicability rule:** Use for when there is an initialization, an increment and a continuation test and the loop variable is not needed after the loop; use while when the loop variable is needed later or the number of passes depends on what happens in the body.

## The whole prerequisite chain

- **Everything it builds on (15):** `arithmetic_operators`, `boolean`, `boolean_expression`, `comparison_operators`, `data_type`, `do_while_loop`, `expression`, `identifier`, `literal`, `logical_operators`, `loop_control`, `loop_variable`, `primitive_type`, `variable`, `while_loop`
- **Everything that builds on it (29):** `accumulator_pattern`, `array_copy`, `array_reversal`, `array_traversal`, `boolean_flag_array`, `break_statement`, `continue_statement`, `convergence_rate`, `counter_pattern`, `enhanced_for`, `fencepost_loop`, `flag_search_loop`, `frequency_counting`, `function_plotting`, `infinite_loop`, `labeled_break`, `loop_body`, `loop_scope`, `matrix_operations`, `monte_carlo_simulation`, `nested_loops`, `power_method`, `row_major_order`, `running_extreme`, `sentinel_loop`, `simulation_loop`, `standard_audio`, `switch_statement`, `two_models`
