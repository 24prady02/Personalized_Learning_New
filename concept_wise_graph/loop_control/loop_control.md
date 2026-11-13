# loop_control (`loop_control`)

the three slots: init ; condition ; update

Section 1.3 Conditionals and Loops, topic 1.3.c While loops.

![The knowledge graph around loop_control](loop_control.png)

## At a glance

- **Needs first:** `do_while_loop`, `loop_variable`, `while_loop`
- **Leads to:** `for_loop`, `increment_operators`, `infinite_loop`, `labeled_break`, `loop_performance`, `off_by_one_error`
- **Learned alongside:** nothing
- **Misconceptions:** `DoubleLoopIndexCount`, `ForLoopPartSkipped`, `ForUpdateBeforeBody`, `IdiomOverridesCode`, `InfiniteLoopUnnoticed`, `LoopHeaderIsEquations`, `LoopStepAlwaysOne`, `LoopUpdateChangesDirection`, `OffByOneBound`, `PreIncrementBeforeLoop`
- **Errors:** `WrongIterationCount`
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 52 edges around this concept. The edge logic, the wrong and right rules and the exact rules of the ways are copied word for word from the graph.

## To work on (1)

- no aliases: a student's words cannot name this concept

## What it needs first (3)

A prerequisite edge means the other concept has to be understood before `loop_control`.

### `do_while_loop` comes before `loop_control`

*do { body } while (c); -- body first, test after*

- **Edge:** `pre:do_while_loop->loop_control`
- **Exact edge logic:** A do-while loop has the same control parts as a while loop (the variable set before, the condition, the update in the body); only the test is moved after the body.
- **Grounding:** book\_passage

### `loop_variable` comes before `loop_control`

*the counter that drives the loop*

- **Edge:** `pre:loop_variable->loop_control`
- **Exact edge logic:** The init, condition and update all act on the loop variable: the init sets it, the condition tests it, the update changes it.
- **Grounding:** book\_passage
- **Composition rule (R) of `loop_control` with `loop_variable`:** All three control parts act on the loop variable: the init sets it, the condition tests it, the update changes it.
- **Composition rule (R) of `loop_variable` with `loop_control`:** The init, condition and update all act on the loop variable: the init sets it, the condition tests it, the update changes it.

### `while_loop` comes before `loop_control`

*repeat a block while a condition holds*

- **Edge:** `pre:while_loop->loop_control`
- **Exact edge logic:** A while loop has the same three control parts as a for loop, written in other places: the index set before the loop, the loop-continuation condition in the header, and the update as the last statement of the body.
- **Grounding:** book\_passage

## What it leads to (6)

These concepts need `loop_control` first.

### `loop_control` comes before `for_loop`

*a while with init/condition/update packaged together*

- **Edge:** `pre:loop_control->for_loop`
- **Exact edge logic:** The for header is exactly the three control slots, and the body runs after the test and before the update on each pass.
- **Grounding:** book\_passage
- **Composition rule (R) of `loop_control` with `for_loop`:** The for header is exactly the three control slots, separated by semicolons; the body runs after the test and before the update.
- **Composition rule (R) of `for_loop` with `loop_control`:** The for header is exactly the three loop-control slots; the body runs after the test and before the update on each pass.

### `loop_control` comes before `increment_operators`

*++ / -- (and +=)*

- **Edge:** `pre:loop_control->increment_operators`
- **Exact edge logic:** The loop update i = i + 1 comes first; ++ (and +=) are then introduced as shorthand for that update.
- **Grounding:** book\_passage
- **Composition rule (R) of `loop_control` with `increment_operators`:** The update i = i + 1 is usually written i++ (or i += k for other steps); as a whole update statement ++i and i++ are equivalent.
- **Composition rule (R) of `increment_operators` with `loop_control`:** The usual for-loop update is i++ (shorthand for i = i + 1); as a stand-alone update statement ++i and i++ give the same loop.

### `loop_control` comes before `infinite_loop`

*a loop whose condition never becomes false*

- **Edge:** `pre:loop_control->infinite_loop`
- **Exact edge logic:** A loop is infinite when its update never moves the condition towards false.
- **Grounding:** book\_passage
- **Composition rule (R) of `loop_control` with `infinite_loop`:** A loop is infinite when the update never moves the variable toward making the condition false (e.g. condition i &gt; 3 with update i = i + 1).
- **Composition rule (R) of `infinite_loop` with `loop_control`:** A loop is finite only if its update moves the control variable towards making the condition false. Wrong direction (\`i--\` with \`i &lt; n\`), wrong step (\`i += 0\` or \`x += 0.5\` on an int), or a condition that the update can step over (\`i != 10\` with \`i += 3\`) all give infinite loops.

### `loop_control` comes before `labeled_break`

*labeled break/continue exit or continue an outer loop*

- **Edge:** `pre:loop_control->labeled_break`
- **Exact edge logic:** break with a label leaves the labelled outer loop, not only the innermost one.
- **Grounding:** spec\_passage

### `loop_control` comes before `loop_performance`

*Loop performance: the running time of a loop program depends on how many iterations it makes*

- **Edge:** `pre:loop_control->loop_performance`
- **Exact edge logic:** The loop condition decides how many iterations run, so a better test (i &lt;= n/i instead of i &lt; n) makes the program much faster.
- **Grounding:** book\_passage
- **Composition rule (R) of `loop_control` with `loop_performance`:** The continuation condition fixes the number of iterations, so a sharper bound (i &lt;= n/i instead of i &lt; n) can make a program dramatically faster.
- **Composition rule (R) of `loop_performance` with `loop_control`:** The loop's condition and update set the iteration count. A tighter test that keeps correctness (i &lt;= n/i instead of i &lt; n) or a faster update (doubling instead of incrementing) can make the program dramatically faster with identical output.

### `loop_control` comes before `off_by_one_error`

*a loop or index that runs one time too many or too few (&lt; vs &lt;=, 0..n vs 1..n, length vs length-1)*

- **Edge:** `pre:loop_control->off_by_one_error`
- **Exact edge logic:** The initialization and the condition of a loop fix how many times it runs; one wrong bound makes it run once too many or too few.
- **Grounding:** book\_passage
- **Composition rule (R) of `off_by_one_error` with `loop_control`:** The start value and the condition together fix the number of passes; changing either by one changes the count by one.

## Learned alongside (0)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

No parallel edge touches this concept.

## Misconceptions (10)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### DoubleLoopIndexCount

- **Edge:** `loop_control` &rarr; `DoubleLoopIndexCount` (misconception)
- **Exact edge logic (the wrong rule):** for (double x = 0.0; x &lt;= 1.0; x += 0.1) runs exactly 11 times.
- **Twin logic (the right rule):** Using a double as a for-loop index is legal but bad practice: the number of iterations depends on an equality test between double values, which may not give the result you expect.
- **Wrong belief (on the node):** for (double x = 0.0; x &lt;= 1.0; x += 0.1) runs exactly 11 times.
- **Correct rule (on the node):** Using a double as a for-loop index is legal but bad practice: the number of iterations depends on an equality test between double values, which may not give the result you expect.
- **Provenance:** textbook
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [5] misconception, exact rule:** wrong rule: for (double x = 0.0; x &lt;= 1.0; x += 0.1) runs exactly 11 times. Right rule: Using a double as a for-loop index is legal but bad practice: the number of iterations depends on an equality test between double values, which may not give the result you expect.
- **Edge `for_loop` &rarr; `DoubleLoopIndexCount`, exact edge logic:** for (double x = 0.0; x &lt;= 1.0; x += 0.1) runs exactly 11 times. **Twin logic:** Using a double as a for-loop index is legal but bad practice: the number of iterations depends on an equality test between double values, which may not give the result you expect. (role: primary)
- **Edge `loop_variable` &rarr; `DoubleLoopIndexCount`, exact edge logic:** for (double x = 0.0; x &lt;= 1.0; x += 0.1) runs exactly 11 times. **Twin logic:** Using a double as a for-loop index is legal but bad practice: the number of iterations depends on an equality test between double values, which may not give the result you expect. (role: context)
- **Edge `off_by_one_error` &rarr; `DoubleLoopIndexCount`, exact edge logic:** for (double x = 0.0; x &lt;= 1.0; x += 0.1) runs exactly 11 times. **Twin logic:** Using a double as a for-loop index is legal but bad practice: the number of iterations depends on an equality test between double values, which may not give the result you expect. (role: context)

### ForLoopPartSkipped

- **Edge:** `loop_control` &rarr; `ForLoopPartSkipped` (misconception)
- **Exact edge logic (the wrong rule):** A pass of a loop may leave out one of its parts (the condition test, the body, the update, or the initialization).
- **Twin logic (the right rule):** Each pass of a for loop runs test, then body, then update, every time; the initialization runs once, at the start.
- **Wrong belief (on the node):** A pass of a loop may leave out one of its parts (the condition test, the body, the update, or the initialization).
- **Correct rule (on the node):** Each pass of a for loop runs test, then body, then update, every time; the initialization runs once, at the start.
- **Provenance:** published
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [8] misconception, exact rule:** wrong rule: A pass of a loop may leave out one of its parts (the condition test, the body, the update, or the initialization). Right rule: Each pass of a for loop runs test, then body, then update, every time; the initialization runs once, at the start.
- **Edge `for_loop` &rarr; `ForLoopPartSkipped`, exact edge logic:** A pass of a loop may leave out one of its parts (the condition test, the body, the update, or the initialization). **Twin logic:** Each pass of a for loop runs test, then body, then update, every time; the initialization runs once, at the start. (role: primary)
- **Edge `loop_body` &rarr; `ForLoopPartSkipped`, exact edge logic:** A pass of a loop may leave out one of its parts (the condition test, the body, the update, or the initialization). **Twin logic:** Each pass of a for loop runs test, then body, then update, every time; the initialization runs once, at the start. (role: context)

### ForUpdateBeforeBody

- **Edge:** `loop_control` &rarr; `ForUpdateBeforeBody` (misconception)
- **Exact edge logic (the wrong rule):** The update part of a for header (e.g. i = i - 4) runs before the body on each pass, so the first pass already sees the updated value.
- **Twin logic (the right rule):** The update runs after the body, before the next condition test; the first pass uses the initial value.
- **Wrong belief (on the node):** The update part of a for header (e.g. i = i - 4) runs before the body on each pass, so the first pass already sees the updated value.
- **Correct rule (on the node):** The update runs after the body, before the next condition test; the first pass uses the initial value.
- **Provenance:** published
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [9] misconception, exact rule:** wrong rule: The update part of a for header (e.g. i = i - 4) runs before the body on each pass, so the first pass already sees the updated value. Right rule: The update runs after the body, before the next condition test; the first pass uses the initial value.
- **Edge `for_loop` &rarr; `ForUpdateBeforeBody`, exact edge logic:** The update part of a for header (e.g. i = i - 4) runs before the body on each pass, so the first pass already sees the updated value. **Twin logic:** The update runs after the body, before the next condition test; the first pass uses the initial value. (role: primary)

### IdiomOverridesCode

- **Edge:** `loop_control` &rarr; `IdiomOverridesCode` (misconception)
- **Exact edge logic (the wrong rule):** An array loop processes the whole array from index 0 to length-1 and increments its index at the end of the body, whatever the code says.
- **Twin logic (the right rule):** The loop visits exactly the indices that its initialisation, guard and update produce, in the order in which its statements are written.
- **Wrong belief (on the node):** An array loop processes the whole array from index 0 to length-1 and increments its index at the end of the body, whatever the code says.
- **Correct rule (on the node):** The loop visits exactly the indices that its initialisation, guard and update produce, in the order in which its statements are written.
- **Provenance:** published
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [6] misconception, exact rule:** wrong rule: An array loop processes the whole array from index 0 to length-1 and increments its index at the end of the body, whatever the code says. Right rule: The loop visits exactly the indices that its initialisation, guard and update produce, in the order in which its statements are written.
- **Edge `array_traversal` &rarr; `IdiomOverridesCode`, exact edge logic:** An array loop processes the whole array from index 0 to length-1 and increments its index at the end of the body, whatever the code says. **Twin logic:** The loop visits exactly the indices that its initialisation, guard and update produce, in the order in which its statements are written. (role: primary)
- **Edge `for_loop` &rarr; `IdiomOverridesCode`, exact edge logic:** An array loop processes the whole array from index 0 to length-1 and increments its index at the end of the body, whatever the code says. **Twin logic:** The loop visits exactly the indices that its initialisation, guard and update produce, in the order in which its statements are written. (role: context)
- **Edge `increment_operators` &rarr; `IdiomOverridesCode`, exact edge logic:** An array loop processes the whole array from index 0 to length-1 and increments its index at the end of the body, whatever the code says. **Twin logic:** The loop visits exactly the indices that its initialisation, guard and update produce, in the order in which its statements are written. (role: context)

### InfiniteLoopUnnoticed

- **Edge:** `loop_control` &rarr; `InfiniteLoopUnnoticed` (misconception)
- **Exact edge logic (the wrong rule):** A while loop always stops on its own, even if nothing in its body can make the condition false.
- **Twin logic (the right rule):** A while loop stops only when its condition is false at a check, so if no pass changes the variables in the condition, it never stops.
- **Wrong belief (on the node):** a condition that never goes false still terminates
- **Correct rule (on the node):** A while loop stops only when its condition is false at a check, so if no pass changes the variables in the condition, it never stops.
- **Provenance:** published
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [4] misconception, exact rule:** wrong rule: a condition that never goes false still terminates. Right rule: A while loop stops only when its condition is false at a check, so if no pass changes the variables in the condition, it never stops.
- **Edge `infinite_loop` &rarr; `InfiniteLoopUnnoticed`, exact edge logic:** a condition that never goes false still terminates **Twin logic:** A while loop stops only when its condition is false at a check, so if no pass changes the variables in the condition, it never stops. (role: primary)
- **Edge `while_loop` &rarr; `InfiniteLoopUnnoticed`, exact edge logic:** a condition that never goes false still terminates **Twin logic:** A while loop stops only when its condition is false at a check, so if no pass changes the variables in the condition, it never stops. (role: context)

### LoopHeaderIsEquations

- **Edge:** `loop_control` &rarr; `LoopHeaderIsEquations` (misconception)
- **Exact edge logic (the wrong rule):** The initialization, condition and update of a for header are equations that all hold at the same time.
- **Twin logic (the right rule):** The three header parts are statements run at different moments: init once, then condition test, body, update, repeated.
- **Wrong belief (on the node):** The initialization, condition and update of a for header are equations that all hold at the same time.
- **Correct rule (on the node):** The three header parts are statements run at different moments: init once, then condition test, body, update, repeated.
- **Provenance:** published
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [7] misconception, exact rule:** wrong rule: The initialization, condition and update of a for header are equations that all hold at the same time. Right rule: The three header parts are statements run at different moments: init once, then condition test, body, update, repeated.
- **Edge `for_loop` &rarr; `LoopHeaderIsEquations`, exact edge logic:** The initialization, condition and update of a for header are equations that all hold at the same time. **Twin logic:** The three header parts are statements run at different moments: init once, then condition test, body, update, repeated. (role: primary)

### LoopStepAlwaysOne

- **Edge:** `loop_control` &rarr; `LoopStepAlwaysOne` (misconception)
- **Exact edge logic (the wrong rule):** A loop variable always goes up or down by 1, whatever the update says (so i = i - 4 is read as i--).
- **Twin logic (the right rule):** The loop variable changes exactly as the update expression says (i += 2, i = i - 4, i \*= 2, ...).
- **Wrong belief (on the node):** A loop variable always goes up or down by 1, whatever the update says (so i = i - 4 is read as i--).
- **Correct rule (on the node):** The loop variable changes exactly as the update expression says (i += 2, i = i - 4, i \*= 2, ...).
- **Provenance:** published
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [11] misconception, exact rule:** wrong rule: A loop variable always goes up or down by 1, whatever the update says (so i = i - 4 is read as i--). Right rule: The loop variable changes exactly as the update expression says (i += 2, i = i - 4, i \*= 2, ...).
- **Edge `for_loop` &rarr; `LoopStepAlwaysOne`, exact edge logic:** A loop variable always goes up or down by 1, whatever the update says (so i = i - 4 is read as i--). **Twin logic:** The loop variable changes exactly as the update expression says (i += 2, i = i - 4, i \*= 2, ...). (role: primary)

### LoopUpdateChangesDirection

- **Edge:** `loop_control` &rarr; `LoopUpdateChangesDirection` (misconception)
- **Exact edge logic (the wrong rule):** The update of the loop variable can change from pass to pass (e.g. switch direction) although the code is the same.
- **Twin logic (the right rule):** The update expression is the same on every pass; the loop variable changes by the rule written in the update.
- **Wrong belief (on the node):** The update of the loop variable can change from pass to pass (e.g. switch direction) although the code is the same.
- **Correct rule (on the node):** The update expression is the same on every pass; the loop variable changes by the rule written in the update.
- **Provenance:** published
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [10] misconception, exact rule:** wrong rule: The update of the loop variable can change from pass to pass (e.g. switch direction) although the code is the same. Right rule: The update expression is the same on every pass; the loop variable changes by the rule written in the update.
- **Edge `loop_variable` &rarr; `LoopUpdateChangesDirection`, exact edge logic:** The update of the loop variable can change from pass to pass (e.g. switch direction) although the code is the same. **Twin logic:** The update expression is the same on every pass; the loop variable changes by the rule written in the update. (role: primary)

### OffByOneBound

- **Edge:** `loop_control` &rarr; `OffByOneBound` (misconception)
- **Exact edge logic (the wrong rule):** i &lt; n and i &lt;= n mean the same, so the loop runs until i equals n and the last pass can use a[n].
- **Twin logic (the right rule):** for (i = 0; i &lt; n; i++) runs n times with i going up to n - 1; with &lt;= it runs n + 1 times and reaches i = n.
- **Wrong belief (on the node):** &lt; vs &lt;= and 0..n vs 0..n-1 are interchangeable
- **Correct rule (on the node):** for (i = 0; i &lt; n; i++) runs n times with i going up to n - 1; with &lt;= it runs n + 1 times and reaches i = n.
- **Provenance:** published
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [2] misconception, exact rule:** wrong rule: &lt; vs &lt;= and 0..n vs 0..n-1 are interchangeable. Right rule: for (i = 0; i &lt; n; i++) runs n times with i going up to n - 1; with &lt;= it runs n + 1 times and reaches i = n.
- **Edge `array_bounds` &rarr; `OffByOneBound`, exact edge logic:** &lt; vs &lt;= and 0..n vs 0..n-1 are interchangeable **Twin logic:** for (i = 0; i &lt; n; i++) runs n times with i going up to n - 1; with &lt;= it runs n + 1 times and reaches i = n. (role: context)
- **Edge `array_reversal` &rarr; `OffByOneBound`, exact edge logic:** &lt; vs &lt;= and 0..n vs 0..n-1 are interchangeable **Twin logic:** for (i = 0; i &lt; n; i++) runs n times with i going up to n - 1; with &lt;= it runs n + 1 times and reaches i = n. (role: context)
- **Edge `array_traversal` &rarr; `OffByOneBound`, exact edge logic:** &lt; vs &lt;= and 0..n vs 0..n-1 are interchangeable **Twin logic:** for (i = 0; i &lt; n; i++) runs n times with i going up to n - 1; with &lt;= it runs n + 1 times and reaches i = n. (role: context)
- **Edge `boolean_flag_array` &rarr; `OffByOneBound`, exact edge logic:** &lt; vs &lt;= and 0..n vs 0..n-1 are interchangeable **Twin logic:** for (i = 0; i &lt; n; i++) runs n times with i going up to n - 1; with &lt;= it runs n + 1 times and reaches i = n. (role: context)
- **Edge `off_by_one_error` &rarr; `OffByOneBound`, exact edge logic:** &lt; vs &lt;= and 0..n vs 0..n-1 are interchangeable **Twin logic:** for (i = 0; i &lt; n; i++) runs n times with i going up to n - 1; with &lt;= it runs n + 1 times and reaches i = n. (role: context)
- **Edge `simulation_loop` &rarr; `OffByOneBound`, exact edge logic:** t &lt; T and t &lt;= T give the same number of moves. **Twin logic:** for (t = 0; t &lt; T; t++) makes exactly T moves; with &lt;= it makes T + 1. (role: context)

### PreIncrementBeforeLoop

- **Edge:** `loop_control` &rarr; `PreIncrementBeforeLoop` (misconception)
- **Exact edge logic (the wrong rule):** With ++i in the update of for (int i = s; i &lt; n; ++i), i is increased before the body runs, so the first pass uses s + 1.
- **Twin logic (the right rule):** The update runs after each pass of the body, so with either ++i or i++ the first pass uses i = s.
- **Wrong belief (on the node):** ++i in the for-update runs before the body each pass
- **Correct rule (on the node):** The update runs after each pass of the body, so with either ++i or i++ the first pass uses i = s.
- **Provenance:** published
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [1] misconception, exact rule:** wrong rule: ++i in the for-update runs before the body each pass. Right rule: The update runs after each pass of the body, so with either ++i or i++ the first pass uses i = s.
- **L0 way [3] inconsistent\_trace, exact rule:** Applies the init-test-update rule (LT) unevenly: updates before the body on some passes, skips the test or the update on a pass, or re-runs the init. (here mixing in: "++i in the for-update runs before the body each pass")
- **Edge `increment_operators` &rarr; `PreIncrementBeforeLoop`, exact edge logic:** ++i in the for-update runs before the body each pass **Twin logic:** The update runs after each pass of the body, so with either ++i or i++ the first pass uses i = s. (role: context)

## Errors (1)

An error edge states the rule that gets broken in a program, and the right rule.

### WrongIterationCount

- **Edge:** `loop_control` &rarr; `WrongIterationCount` (error)
- **Exact edge logic (the wrong rule):** Updates the loop counter so that the loop runs the wrong number of times.
- **Twin logic (the right rule):** The init, test and update together decide the number of passes; trace them to check the count.
- **Wrong belief (on the node):** Updates the loop counter so that the loop runs the wrong number of times.
- **Correct rule (on the node):** The init, test and update together decide the number of passes; trace them to check the count.
- **Provenance:** published
- **Role of this concept:** context
- **Edge `for_loop` &rarr; `WrongIterationCount`, exact edge logic:** Updates the loop counter so that the loop runs the wrong number of times. **Twin logic:** The init, test and update together decide the number of passes; trace them to check the count. (role: primary)
- **Edge `off_by_one_error` &rarr; `WrongIterationCount`, exact edge logic:** Updates the loop counter so that the loop runs the wrong number of times. **Twin logic:** The init, test and update together decide the number of passes; trace them to check the count. (role: context)

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for loop control: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to loop control agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

- **Edge:** `loop_control` &rarr; `loop_control@L0` (has_level)
- **Exact edge logic:** loop control -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (12 ways).

Ways (12), each with its exact rule:

- **[0] everyday\_reading** (rule type E, folk-meaning rule): Folk meaning: in mathematics i = 0, i &lt; n and i = i + 1 are equations or constraints that hold at the same time (and i = i + 1 is nonsense). In Java they are three actions run at different moments: init once, test before each pass, update after each pass.
- **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `PreIncrementBeforeLoop`: wrong rule: ++i in the for-update runs before the body each pass. Right rule: The update runs after each pass of the body, so with either ++i or i++ the first pass uses i = s.
- **[2] misconception** (rule type M, wrong rule / right rule) &rarr; `OffByOneBound`: wrong rule: &lt; vs &lt;= and 0..n vs 0..n-1 are interchangeable. Right rule: for (i = 0; i &lt; n; i++) runs n times with i going up to n - 1; with &lt;= it runs n + 1 times and reaches i = n.
- **[3] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `PreIncrementBeforeLoop`: Applies the init-test-update rule (LT) unevenly: updates before the body on some passes, skips the test or the update on a pass, or re-runs the init. (here mixing in: "++i in the for-update runs before the body each pass")
- **[4] misconception** (rule type M, wrong rule / right rule) &rarr; `InfiniteLoopUnnoticed`: wrong rule: a condition that never goes false still terminates. Right rule: A while loop stops only when its condition is false at a check, so if no pass changes the variables in the condition, it never stops.
- **[5] misconception** (rule type M, wrong rule / right rule) &rarr; `DoubleLoopIndexCount`: wrong rule: for (double x = 0.0; x &lt;= 1.0; x += 0.1) runs exactly 11 times. Right rule: Using a double as a for-loop index is legal but bad practice: the number of iterations depends on an equality test between double values, which may not give the result you expect.
- **[6] misconception** (rule type M, wrong rule / right rule) &rarr; `IdiomOverridesCode`: wrong rule: An array loop processes the whole array from index 0 to length-1 and increments its index at the end of the body, whatever the code says. Right rule: The loop visits exactly the indices that its initialisation, guard and update produce, in the order in which its statements are written.
- **[7] misconception** (rule type M, wrong rule / right rule) &rarr; `LoopHeaderIsEquations`: wrong rule: The initialization, condition and update of a for header are equations that all hold at the same time. Right rule: The three header parts are statements run at different moments: init once, then condition test, body, update, repeated.
- **[8] misconception** (rule type M, wrong rule / right rule) &rarr; `ForLoopPartSkipped`: wrong rule: A pass of a loop may leave out one of its parts (the condition test, the body, the update, or the initialization). Right rule: Each pass of a for loop runs test, then body, then update, every time; the initialization runs once, at the start.
- **[9] misconception** (rule type M, wrong rule / right rule) &rarr; `ForUpdateBeforeBody`: wrong rule: The update part of a for header (e.g. i = i - 4) runs before the body on each pass, so the first pass already sees the updated value. Right rule: The update runs after the body, before the next condition test; the first pass uses the initial value.
- **[10] misconception** (rule type M, wrong rule / right rule) &rarr; `LoopUpdateChangesDirection`: wrong rule: The update of the loop variable can change from pass to pass (e.g. switch direction) although the code is the same. Right rule: The update expression is the same on every pass; the loop variable changes by the rule written in the update.
- **[11] misconception** (rule type M, wrong rule / right rule) &rarr; `LoopStepAlwaysOne`: wrong rule: A loop variable always goes up or down by 1, whatever the update says (so i = i - 4 is read as i--). Right rule: The loop variable changes exactly as the update expression says (i += 2, i = i - 4, i \*= 2, ...).

### L1: Unistructural / atom x text surface

L1 for loop control: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

- **Edge:** `loop_control` &rarr; `loop_control@L1` (has_level)
- **Exact edge logic:** loop control -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

Ways (2), each with its exact rule:

- **[0] names\_the\_element** (rule type N, identity rule): Loop control is the init / continuation condition / increment scheme on an index variable that decides how many passes a loop makes and with which values.
- **[1] states\_the\_rule** (rule type S, declarative rule): Initialize an index variable, test a loop-continuation condition on it before each pass, and increment it as the last action of each pass; for (&lt;initialize&gt;; &lt;boolean expression&gt;; &lt;increment&gt;) packages the three. Choosing the loop: for when the passes are counted by an index, while when the loop runs until a condition changes, do-while when the body must run at least once; any one can be rewritten as another, so choose the clearest.

### L2: Multistructural / block x execution / preoperational

L2 for loop control: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

- **Edge:** `loop_control` &rarr; `loop_control@L2` (has_level)
- **Exact edge logic:** loop control -&gt; L2 (Multistructural): the answer applies the rules of loop control to every part of the code, in order (3 ways).

Ways (3), each with its exact rule:

- **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): init (once) -&gt; test -&gt; body -&gt; update -&gt; test -&gt; body -&gt; update ... -&gt; test false -&gt; exit.
- **[1] output\_prediction** (rule type OP, evaluation / result rule): The number of passes and the values seen follow from the three parts: for (int i = 0; i &lt;= N; i++) makes N+1 passes with i = 0..N; with i &lt; N it makes N passes; i += 2 visits every second value.
- **[2] one\_step\_execution** (rule type OS, state-transition rule): One update changes only the loop variable, by exactly the rule written (i++ adds 1, i = i - 4 subtracts 4); one test reads it and returns true or false without changing it.

### L3: Relational / relations x function (concrete operational begins)

L3 for loop control: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

- **Edge:** `loop_control` &rarr; `loop_control@L3` (has_level)
- **Exact edge logic:** loop control -&gt; L3 (Relational): the answer relates the parts (7 ways).

Ways (7), each with its exact rule:

- **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): All three control parts act on the loop variable: the init sets it, the condition tests it, the update changes it.
- **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): The for header is exactly the three control slots, separated by semicolons; the body runs after the test and before the update.
- **[2] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): The update i = i + 1 is usually written i++ (or i += k for other steps); as a whole update statement ++i and i++ are equivalent.
- **[3] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): A loop is infinite when the update never moves the variable toward making the condition false (e.g. condition i &gt; 3 with update i = i + 1).
- **[4] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): The continuation condition fixes the number of iterations, so a sharper bound (i &lt;= n/i instead of i &lt; n) can make a program dramatically faster.
- **[5] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): The initialization and the condition of a loop fix how many times it runs; one wrong bound makes it run once too many or too few.
- **[6] purpose\_of\_the\_whole** (rule type P, plan / role rule): Plan: counter-controlled loop - the loop variable is a stepper that walks a predictable sequence of values (0..N-1, 1..N, every 2nd value) and fixes the number of passes in advance.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for loop control: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

- **Edge:** `loop_control` &rarr; `loop_control@L4` (has_level)
- **Exact edge logic:** loop control -&gt; L4 (Extended abstract): the answer reasons beyond the given code (5 ways).

Ways (5), each with its exact rule:

- **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `PreIncrementBeforeLoop`: Changing &lt; to &lt;= adds one pass; starting at 1 instead of 0 removes one; doubling the step halves the passes; reversing init and bound with i-- visits the same values in reverse order (and still processes the same set only if both ends are adjusted).
- **[1] diagnose\_an\_error** (rule type D, error rule): rule broken: The number of passes is fixed by the init, the test and the update together. Kind: silent logic error. Trigger class: Wrong start value, &lt; vs &lt;=, a wrong step, or an extra update of the counter in the body (or outside the loop): the loop runs too few or too many passes (off by one, or skips values).
- **[2] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Use explicit init/test/update control when the passes are counted or follow a fixed step; when the number of passes depends on data computed in the body, control the loop by that data (a while condition) instead.
- **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: The update must move the loop variable toward making the condition false. Kind: silent logic error. Trigger class: An update in the wrong direction or a condition that the update cannot falsify (e.g. i &gt; 3 with i++, or i != 10 with i += 3): infinite loop.
- **[4] diagnose\_an\_error** (rule type D, error rule): rule broken: Do not control a loop by an equality test on double values. Kind: silent logic error. Trigger class: for (double x = 0.0; x &lt; 1.0; x += 0.1): after ten additions x is 0.9999999999999999, so the loop makes 11 passes instead of the intended 10.

## Same topic

`loop_control` belongs to the topic **While loops** (`topic1.3.c`). The topic also contains: `loop_body`, `loop_invariant_reasoning`, `while_loop`.

## Rules of the concept (28)

- **Book** (SW-1e, p. 55 (pdf 65)): "Many loops follow this scheme: initialize an index variable to some value and then use a while loop to test a loop continuation condition involving the index variable"
- **Book** (SW-1.3, ): "Many loops follow the same basic scheme: initialize an index variable to some value and then use a while loop to test an exit condition."
- **E** (folk-meaning rule): Folk meaning: in mathematics i = 0, i &lt; n and i = i + 1 are equations or constraints that hold at the same time (and i = i + 1 is nonsense). In Java they are three actions run at different moments: init once, test before each pass, update after each pass.
- **M** (wrong rule / right rule): OffByOneBound: wrong: &lt; vs &lt;= and 0..n vs 0..n-1 are interchangeable \| right: for (i = 0; i &lt; n; i++) runs n times with i going up to n - 1; with &lt;= it runs n + 1 times and reaches i = n.
- **M** (wrong rule / right rule): PreIncrementBeforeLoop: wrong: ++i in the for-update runs before the body each pass \| right: The update runs after each pass of the body, so with either ++i or i++ the first pass uses i = s.
- **M** (wrong rule / right rule): InfiniteLoopUnnoticed: wrong: a condition that never goes false still terminates \| right: A while loop stops only when its condition is false at a check, so if no pass changes the variables in the condition, it never stops.
- **M** (wrong rule / right rule): DoubleLoopIndexCount: wrong: for (double x = 0.0; x &lt;= 1.0; x += 0.1) runs exactly 11 times. \| right: Using a double as a for-loop index is legal but bad practice: the number of iterations depends on an equality test between double values, which may not give the result you expect.
- **M** (wrong rule / right rule): IdiomOverridesCode: wrong: An array loop processes the whole array from index 0 to length-1 and increments its index at the end of the body, whatever the code says. \| right: The loop visits exactly the indices that its initialisation, guard and update produce, in the order in which its statements are written.
- **M** (wrong rule / right rule): LoopHeaderIsEquations: wrong: The initialization, condition and update of a for header are equations that all hold at the same time. \| right: The three header parts are statements run at different moments: init once, then condition test, body, update, repeated.
- **M** (wrong rule / right rule): ForLoopPartSkipped: wrong: A pass of a loop may leave out one of its parts (the condition test, the body, the update, or the initialization). \| right: Each pass of a for loop runs test, then body, then update, every time; the initialization runs once, at the start.
- **M** (wrong rule / right rule): ForUpdateBeforeBody: wrong: The update part of a for header (e.g. i = i - 4) runs before the body on each pass, so the first pass already sees the updated value. \| right: The update runs after the body, before the next condition test; the first pass uses the initial value.
- **M** (wrong rule / right rule): LoopUpdateChangesDirection: wrong: The update of the loop variable can change from pass to pass (e.g. switch direction) although the code is the same. \| right: The update expression is the same on every pass; the loop variable changes by the rule written in the update.
- **M** (wrong rule / right rule): LoopStepAlwaysOne: wrong: A loop variable always goes up or down by 1, whatever the update says (so i = i - 4 is read as i--). \| right: The loop variable changes exactly as the update expression says (i += 2, i = i - 4, i \*= 2, ...).
- **T** (uneven-application rule): Applies the init-test-update rule (LT) unevenly: updates before the body on some passes, skips the test or the update on a pass, or re-runs the init.
- **N** (identity rule): Loop control is the init / continuation condition / increment scheme on an index variable that decides how many passes a loop makes and with which values.
- **S** (declarative rule): Initialize an index variable, test a loop-continuation condition on it before each pass, and increment it as the last action of each pass; for (&lt;initialize&gt;; &lt;boolean expression&gt;; &lt;increment&gt;) packages the three. Choosing the loop: for when the passes are counted by an index, while when the loop runs until a condition changes, do-while when the body must run at least once; any one can be rewritten as another, so choose the clearest.
- **LT** (operational sequencing rule): init (once) -&gt; test -&gt; body -&gt; update -&gt; test -&gt; body -&gt; update ... -&gt; test false -&gt; exit.
- **OP** (evaluation / result rule): The number of passes and the values seen follow from the three parts: for (int i = 0; i &lt;= N; i++) makes N+1 passes with i = 0..N; with i &lt; N it makes N passes; i += 2 visits every second value.
- **OS** (state-transition rule): One update changes only the loop variable, by exactly the rule written (i++ adds 1, i = i - 4 subtracts 4); one test reads it and returns true or false without changing it.
- **R** (composition rule (with a neighbour)): with loop\_variable: All three control parts act on the loop variable: the init sets it, the condition tests it, the update changes it.
- **R** (composition rule (with a neighbour)): with for\_loop: The for header is exactly the three control slots, separated by semicolons; the body runs after the test and before the update.
- **R** (composition rule (with a neighbour)): with increment\_operators: The update i = i + 1 is usually written i++ (or i += k for other steps); as a whole update statement ++i and i++ are equivalent.
- **R** (composition rule (with a neighbour)): with infinite\_loop: A loop is infinite when the update never moves the variable toward making the condition false (e.g. condition i &gt; 3 with update i = i + 1).
- **R** (composition rule (with a neighbour)): with loop\_performance: The continuation condition fixes the number of iterations, so a sharper bound (i &lt;= n/i instead of i &lt; n) can make a program dramatically faster.
- **P** (plan / role rule): Plan: counter-controlled loop - the loop variable is a stepper that walks a predictable sequence of values (0..N-1, 1..N, every 2nd value) and fixes the number of passes in advance.
- **C** (conservation rule): Changing &lt; to &lt;= adds one pass; starting at 1 instead of 0 removes one; doubling the step halves the passes; reversing init and bound with i-- visits the same values in reverse order (and still processes the same set only if both ends are adjusted).
- **D** (error rule): rule broken: The number of passes is fixed by the init, the test and the update together. (silent logic error)
- **D** (error rule): rule broken: The update must move the loop variable toward making the condition false. (silent logic error)
- **D** (error rule): rule broken: Do not control a loop by an equality test on double values. (silent logic error)
- **X** (applicability rule): Use explicit init/test/update control when the passes are counted or follow a fixed step; when the number of passes depends on data computed in the body, control the loop by that data (a while condition) instead.

## How it is found in code and answers (reader block)

- **Aliases:** none
- **Code patterns:** `\bwhile\s*\(\s*\w+\s*(?:[<>]=?|!=)`
- **Operator symbols:** none
- **Java types:** none
- **Signal for\_header** (scope program, decisive): `\bfor\s*\(\s*[^;:()]*;[^;]*;[^)]*\)`

## The whole prerequisite chain

- **Everything it builds on (14):** `arithmetic_operators`, `boolean`, `boolean_expression`, `comparison_operators`, `data_type`, `do_while_loop`, `expression`, `identifier`, `literal`, `logical_operators`, `loop_variable`, `primitive_type`, `variable`, `while_loop`
- **Everything that builds on it (34):** `accumulator_pattern`, `array_copy`, `array_reversal`, `array_traversal`, `boolean_flag_array`, `break_statement`, `continue_statement`, `convergence_rate`, `counter_pattern`, `enhanced_for`, `fencepost_loop`, `flag_search_loop`, `for_loop`, `frequency_counting`, `function_plotting`, `increment_operators`, `infinite_loop`, `labeled_break`, `loop_body`, `loop_performance`, `loop_scope`, `matrix_operations`, `monte_carlo_simulation`, `nested_loops`, `off_by_one_error`, `power_method`, `row_major_order`, `running_extreme`, `sentinel_loop`, `side_effect_order`, `simulation_loop`, `standard_audio`, `switch_statement`, `two_models`

## Every edge in this view and its exact edge logic (52)

All the edges drawn in the picture, in the order: prerequisite, parallel, misconception, error, has_level, contains.

**1. `do_while_loop` &rarr; `loop_control`** (prerequisite)

- **Exact edge logic:** A do-while loop has the same control parts as a while loop (the variable set before, the condition, the update in the body); only the test is moved after the body.
- **Grounding:** book\_passage

**2. `loop_control` &rarr; `for_loop`** (prerequisite)

- **Exact edge logic:** The for header is exactly the three control slots, and the body runs after the test and before the update on each pass.
- **Grounding:** book\_passage
- **Composition rule (R) of `loop_control` with `for_loop`:** The for header is exactly the three control slots, separated by semicolons; the body runs after the test and before the update.
- **Composition rule (R) of `for_loop` with `loop_control`:** The for header is exactly the three loop-control slots; the body runs after the test and before the update on each pass.

**3. `loop_control` &rarr; `increment_operators`** (prerequisite)

- **Exact edge logic:** The loop update i = i + 1 comes first; ++ (and +=) are then introduced as shorthand for that update.
- **Grounding:** book\_passage
- **Composition rule (R) of `loop_control` with `increment_operators`:** The update i = i + 1 is usually written i++ (or i += k for other steps); as a whole update statement ++i and i++ are equivalent.
- **Composition rule (R) of `increment_operators` with `loop_control`:** The usual for-loop update is i++ (shorthand for i = i + 1); as a stand-alone update statement ++i and i++ give the same loop.

**4. `loop_control` &rarr; `infinite_loop`** (prerequisite)

- **Exact edge logic:** A loop is infinite when its update never moves the condition towards false.
- **Grounding:** book\_passage
- **Composition rule (R) of `loop_control` with `infinite_loop`:** A loop is infinite when the update never moves the variable toward making the condition false (e.g. condition i &gt; 3 with update i = i + 1).
- **Composition rule (R) of `infinite_loop` with `loop_control`:** A loop is finite only if its update moves the control variable towards making the condition false. Wrong direction (\`i--\` with \`i &lt; n\`), wrong step (\`i += 0\` or \`x += 0.5\` on an int), or a condition that the update can step over (\`i != 10\` with \`i += 3\`) all give infinite loops.

**5. `loop_control` &rarr; `labeled_break`** (prerequisite)

- **Exact edge logic:** break with a label leaves the labelled outer loop, not only the innermost one.
- **Grounding:** spec\_passage

**6. `loop_control` &rarr; `loop_performance`** (prerequisite)

- **Exact edge logic:** The loop condition decides how many iterations run, so a better test (i &lt;= n/i instead of i &lt; n) makes the program much faster.
- **Grounding:** book\_passage
- **Composition rule (R) of `loop_control` with `loop_performance`:** The continuation condition fixes the number of iterations, so a sharper bound (i &lt;= n/i instead of i &lt; n) can make a program dramatically faster.
- **Composition rule (R) of `loop_performance` with `loop_control`:** The loop's condition and update set the iteration count. A tighter test that keeps correctness (i &lt;= n/i instead of i &lt; n) or a faster update (doubling instead of incrementing) can make the program dramatically faster with identical output.

**7. `loop_control` &rarr; `off_by_one_error`** (prerequisite)

- **Exact edge logic:** The initialization and the condition of a loop fix how many times it runs; one wrong bound makes it run once too many or too few.
- **Grounding:** book\_passage
- **Composition rule (R) of `off_by_one_error` with `loop_control`:** The start value and the condition together fix the number of passes; changing either by one changes the count by one.

**8. `loop_variable` &rarr; `loop_control`** (prerequisite)

- **Exact edge logic:** The init, condition and update all act on the loop variable: the init sets it, the condition tests it, the update changes it.
- **Grounding:** book\_passage
- **Composition rule (R) of `loop_variable` with `loop_control`:** The init, condition and update all act on the loop variable: the init sets it, the condition tests it, the update changes it.
- **Composition rule (R) of `loop_control` with `loop_variable`:** All three control parts act on the loop variable: the init sets it, the condition tests it, the update changes it.

**9. `while_loop` &rarr; `loop_control`** (prerequisite)

- **Exact edge logic:** A while loop has the same three control parts as a for loop, written in other places: the index set before the loop, the loop-continuation condition in the header, and the update as the last statement of the body.
- **Grounding:** book\_passage

**10. `loop_control` &rarr; `DoubleLoopIndexCount`** (misconception)

- **Exact edge logic (the wrong rule):** for (double x = 0.0; x &lt;= 1.0; x += 0.1) runs exactly 11 times.
- **Twin logic (the right rule):** Using a double as a for-loop index is legal but bad practice: the number of iterations depends on an equality test between double values, which may not give the result you expect.
- **Role:** context

**11. `loop_control` &rarr; `ForLoopPartSkipped`** (misconception)

- **Exact edge logic (the wrong rule):** A pass of a loop may leave out one of its parts (the condition test, the body, the update, or the initialization).
- **Twin logic (the right rule):** Each pass of a for loop runs test, then body, then update, every time; the initialization runs once, at the start.
- **Role:** context

**12. `loop_control` &rarr; `ForUpdateBeforeBody`** (misconception)

- **Exact edge logic (the wrong rule):** The update part of a for header (e.g. i = i - 4) runs before the body on each pass, so the first pass already sees the updated value.
- **Twin logic (the right rule):** The update runs after the body, before the next condition test; the first pass uses the initial value.
- **Role:** context

**13. `loop_control` &rarr; `IdiomOverridesCode`** (misconception)

- **Exact edge logic (the wrong rule):** An array loop processes the whole array from index 0 to length-1 and increments its index at the end of the body, whatever the code says.
- **Twin logic (the right rule):** The loop visits exactly the indices that its initialisation, guard and update produce, in the order in which its statements are written.
- **Role:** context

**14. `loop_control` &rarr; `InfiniteLoopUnnoticed`** (misconception)

- **Exact edge logic (the wrong rule):** A while loop always stops on its own, even if nothing in its body can make the condition false.
- **Twin logic (the right rule):** A while loop stops only when its condition is false at a check, so if no pass changes the variables in the condition, it never stops.
- **Role:** context

**15. `loop_control` &rarr; `LoopHeaderIsEquations`** (misconception)

- **Exact edge logic (the wrong rule):** The initialization, condition and update of a for header are equations that all hold at the same time.
- **Twin logic (the right rule):** The three header parts are statements run at different moments: init once, then condition test, body, update, repeated.
- **Role:** context

**16. `loop_control` &rarr; `LoopStepAlwaysOne`** (misconception)

- **Exact edge logic (the wrong rule):** A loop variable always goes up or down by 1, whatever the update says (so i = i - 4 is read as i--).
- **Twin logic (the right rule):** The loop variable changes exactly as the update expression says (i += 2, i = i - 4, i \*= 2, ...).
- **Role:** context

**17. `loop_control` &rarr; `LoopUpdateChangesDirection`** (misconception)

- **Exact edge logic (the wrong rule):** The update of the loop variable can change from pass to pass (e.g. switch direction) although the code is the same.
- **Twin logic (the right rule):** The update expression is the same on every pass; the loop variable changes by the rule written in the update.
- **Role:** context

**18. `loop_control` &rarr; `OffByOneBound`** (misconception)

- **Exact edge logic (the wrong rule):** i &lt; n and i &lt;= n mean the same, so the loop runs until i equals n and the last pass can use a[n].
- **Twin logic (the right rule):** for (i = 0; i &lt; n; i++) runs n times with i going up to n - 1; with &lt;= it runs n + 1 times and reaches i = n.
- **Role:** primary

**19. `loop_control` &rarr; `PreIncrementBeforeLoop`** (misconception)

- **Exact edge logic (the wrong rule):** With ++i in the update of for (int i = s; i &lt; n; ++i), i is increased before the body runs, so the first pass uses s + 1.
- **Twin logic (the right rule):** The update runs after each pass of the body, so with either ++i or i++ the first pass uses i = s.
- **Role:** primary

**20. `array_bounds` &rarr; `OffByOneBound`** (misconception)

- **Exact edge logic (the wrong rule):** &lt; vs &lt;= and 0..n vs 0..n-1 are interchangeable
- **Twin logic (the right rule):** for (i = 0; i &lt; n; i++) runs n times with i going up to n - 1; with &lt;= it runs n + 1 times and reaches i = n.
- **Role:** context

**21. `array_reversal` &rarr; `OffByOneBound`** (misconception)

- **Exact edge logic (the wrong rule):** &lt; vs &lt;= and 0..n vs 0..n-1 are interchangeable
- **Twin logic (the right rule):** for (i = 0; i &lt; n; i++) runs n times with i going up to n - 1; with &lt;= it runs n + 1 times and reaches i = n.
- **Role:** context

**22. `array_traversal` &rarr; `IdiomOverridesCode`** (misconception)

- **Exact edge logic (the wrong rule):** An array loop processes the whole array from index 0 to length-1 and increments its index at the end of the body, whatever the code says.
- **Twin logic (the right rule):** The loop visits exactly the indices that its initialisation, guard and update produce, in the order in which its statements are written.
- **Role:** primary

**23. `array_traversal` &rarr; `OffByOneBound`** (misconception)

- **Exact edge logic (the wrong rule):** &lt; vs &lt;= and 0..n vs 0..n-1 are interchangeable
- **Twin logic (the right rule):** for (i = 0; i &lt; n; i++) runs n times with i going up to n - 1; with &lt;= it runs n + 1 times and reaches i = n.
- **Role:** context

**24. `boolean_flag_array` &rarr; `OffByOneBound`** (misconception)

- **Exact edge logic (the wrong rule):** &lt; vs &lt;= and 0..n vs 0..n-1 are interchangeable
- **Twin logic (the right rule):** for (i = 0; i &lt; n; i++) runs n times with i going up to n - 1; with &lt;= it runs n + 1 times and reaches i = n.
- **Role:** context

**25. `for_loop` &rarr; `DoubleLoopIndexCount`** (misconception)

- **Exact edge logic (the wrong rule):** for (double x = 0.0; x &lt;= 1.0; x += 0.1) runs exactly 11 times.
- **Twin logic (the right rule):** Using a double as a for-loop index is legal but bad practice: the number of iterations depends on an equality test between double values, which may not give the result you expect.
- **Role:** primary

**26. `for_loop` &rarr; `ForLoopPartSkipped`** (misconception)

- **Exact edge logic (the wrong rule):** A pass of a loop may leave out one of its parts (the condition test, the body, the update, or the initialization).
- **Twin logic (the right rule):** Each pass of a for loop runs test, then body, then update, every time; the initialization runs once, at the start.
- **Role:** primary

**27. `for_loop` &rarr; `ForUpdateBeforeBody`** (misconception)

- **Exact edge logic (the wrong rule):** The update part of a for header (e.g. i = i - 4) runs before the body on each pass, so the first pass already sees the updated value.
- **Twin logic (the right rule):** The update runs after the body, before the next condition test; the first pass uses the initial value.
- **Role:** primary

**28. `for_loop` &rarr; `IdiomOverridesCode`** (misconception)

- **Exact edge logic (the wrong rule):** An array loop processes the whole array from index 0 to length-1 and increments its index at the end of the body, whatever the code says.
- **Twin logic (the right rule):** The loop visits exactly the indices that its initialisation, guard and update produce, in the order in which its statements are written.
- **Role:** context

**29. `for_loop` &rarr; `LoopHeaderIsEquations`** (misconception)

- **Exact edge logic (the wrong rule):** The initialization, condition and update of a for header are equations that all hold at the same time.
- **Twin logic (the right rule):** The three header parts are statements run at different moments: init once, then condition test, body, update, repeated.
- **Role:** primary

**30. `for_loop` &rarr; `LoopStepAlwaysOne`** (misconception)

- **Exact edge logic (the wrong rule):** A loop variable always goes up or down by 1, whatever the update says (so i = i - 4 is read as i--).
- **Twin logic (the right rule):** The loop variable changes exactly as the update expression says (i += 2, i = i - 4, i \*= 2, ...).
- **Role:** primary

**31. `increment_operators` &rarr; `IdiomOverridesCode`** (misconception)

- **Exact edge logic (the wrong rule):** An array loop processes the whole array from index 0 to length-1 and increments its index at the end of the body, whatever the code says.
- **Twin logic (the right rule):** The loop visits exactly the indices that its initialisation, guard and update produce, in the order in which its statements are written.
- **Role:** context

**32. `increment_operators` &rarr; `PreIncrementBeforeLoop`** (misconception)

- **Exact edge logic (the wrong rule):** ++i in the for-update runs before the body each pass
- **Twin logic (the right rule):** The update runs after each pass of the body, so with either ++i or i++ the first pass uses i = s.
- **Role:** context

**33. `infinite_loop` &rarr; `InfiniteLoopUnnoticed`** (misconception)

- **Exact edge logic (the wrong rule):** a condition that never goes false still terminates
- **Twin logic (the right rule):** A while loop stops only when its condition is false at a check, so if no pass changes the variables in the condition, it never stops.
- **Role:** primary

**34. `loop_body` &rarr; `ForLoopPartSkipped`** (misconception)

- **Exact edge logic (the wrong rule):** A pass of a loop may leave out one of its parts (the condition test, the body, the update, or the initialization).
- **Twin logic (the right rule):** Each pass of a for loop runs test, then body, then update, every time; the initialization runs once, at the start.
- **Role:** context

**35. `loop_variable` &rarr; `DoubleLoopIndexCount`** (misconception)

- **Exact edge logic (the wrong rule):** for (double x = 0.0; x &lt;= 1.0; x += 0.1) runs exactly 11 times.
- **Twin logic (the right rule):** Using a double as a for-loop index is legal but bad practice: the number of iterations depends on an equality test between double values, which may not give the result you expect.
- **Role:** context

**36. `loop_variable` &rarr; `LoopUpdateChangesDirection`** (misconception)

- **Exact edge logic (the wrong rule):** The update of the loop variable can change from pass to pass (e.g. switch direction) although the code is the same.
- **Twin logic (the right rule):** The update expression is the same on every pass; the loop variable changes by the rule written in the update.
- **Role:** primary

**37. `off_by_one_error` &rarr; `DoubleLoopIndexCount`** (misconception)

- **Exact edge logic (the wrong rule):** for (double x = 0.0; x &lt;= 1.0; x += 0.1) runs exactly 11 times.
- **Twin logic (the right rule):** Using a double as a for-loop index is legal but bad practice: the number of iterations depends on an equality test between double values, which may not give the result you expect.
- **Role:** context

**38. `off_by_one_error` &rarr; `OffByOneBound`** (misconception)

- **Exact edge logic (the wrong rule):** &lt; vs &lt;= and 0..n vs 0..n-1 are interchangeable
- **Twin logic (the right rule):** for (i = 0; i &lt; n; i++) runs n times with i going up to n - 1; with &lt;= it runs n + 1 times and reaches i = n.
- **Role:** context

**39. `simulation_loop` &rarr; `OffByOneBound`** (misconception)

- **Exact edge logic (the wrong rule):** t &lt; T and t &lt;= T give the same number of moves.
- **Twin logic (the right rule):** for (t = 0; t &lt; T; t++) makes exactly T moves; with &lt;= it makes T + 1.
- **Role:** context

**40. `while_loop` &rarr; `InfiniteLoopUnnoticed`** (misconception)

- **Exact edge logic (the wrong rule):** a condition that never goes false still terminates
- **Twin logic (the right rule):** A while loop stops only when its condition is false at a check, so if no pass changes the variables in the condition, it never stops.
- **Role:** context

**41. `loop_control` &rarr; `WrongIterationCount`** (error)

- **Exact edge logic (the wrong rule):** Updates the loop counter so that the loop runs the wrong number of times.
- **Twin logic (the right rule):** The init, test and update together decide the number of passes; trace them to check the count.
- **Role:** context

**42. `for_loop` &rarr; `WrongIterationCount`** (error)

- **Exact edge logic (the wrong rule):** Updates the loop counter so that the loop runs the wrong number of times.
- **Twin logic (the right rule):** The init, test and update together decide the number of passes; trace them to check the count.
- **Role:** primary

**43. `off_by_one_error` &rarr; `WrongIterationCount`** (error)

- **Exact edge logic (the wrong rule):** Updates the loop counter so that the loop runs the wrong number of times.
- **Twin logic (the right rule):** The init, test and update together decide the number of passes; trace them to check the count.
- **Role:** context

**44. `loop_control` &rarr; `loop_control@L0`** (has_level)

- **Exact edge logic:** loop control -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (12 ways).
  - **[0] everyday\_reading** (rule type E, folk-meaning rule): Folk meaning: in mathematics i = 0, i &lt; n and i = i + 1 are equations or constraints that hold at the same time (and i = i + 1 is nonsense). In Java they are three actions run at different moments: init once, test before each pass, update after each pass.
  - **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `PreIncrementBeforeLoop`: wrong rule: ++i in the for-update runs before the body each pass. Right rule: The update runs after each pass of the body, so with either ++i or i++ the first pass uses i = s.
  - **[2] misconception** (rule type M, wrong rule / right rule) &rarr; `OffByOneBound`: wrong rule: &lt; vs &lt;= and 0..n vs 0..n-1 are interchangeable. Right rule: for (i = 0; i &lt; n; i++) runs n times with i going up to n - 1; with &lt;= it runs n + 1 times and reaches i = n.
  - **[3] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `PreIncrementBeforeLoop`: Applies the init-test-update rule (LT) unevenly: updates before the body on some passes, skips the test or the update on a pass, or re-runs the init. (here mixing in: "++i in the for-update runs before the body each pass")
  - **[4] misconception** (rule type M, wrong rule / right rule) &rarr; `InfiniteLoopUnnoticed`: wrong rule: a condition that never goes false still terminates. Right rule: A while loop stops only when its condition is false at a check, so if no pass changes the variables in the condition, it never stops.
  - **[5] misconception** (rule type M, wrong rule / right rule) &rarr; `DoubleLoopIndexCount`: wrong rule: for (double x = 0.0; x &lt;= 1.0; x += 0.1) runs exactly 11 times. Right rule: Using a double as a for-loop index is legal but bad practice: the number of iterations depends on an equality test between double values, which may not give the result you expect.
  - **[6] misconception** (rule type M, wrong rule / right rule) &rarr; `IdiomOverridesCode`: wrong rule: An array loop processes the whole array from index 0 to length-1 and increments its index at the end of the body, whatever the code says. Right rule: The loop visits exactly the indices that its initialisation, guard and update produce, in the order in which its statements are written.
  - **[7] misconception** (rule type M, wrong rule / right rule) &rarr; `LoopHeaderIsEquations`: wrong rule: The initialization, condition and update of a for header are equations that all hold at the same time. Right rule: The three header parts are statements run at different moments: init once, then condition test, body, update, repeated.
  - **[8] misconception** (rule type M, wrong rule / right rule) &rarr; `ForLoopPartSkipped`: wrong rule: A pass of a loop may leave out one of its parts (the condition test, the body, the update, or the initialization). Right rule: Each pass of a for loop runs test, then body, then update, every time; the initialization runs once, at the start.
  - **[9] misconception** (rule type M, wrong rule / right rule) &rarr; `ForUpdateBeforeBody`: wrong rule: The update part of a for header (e.g. i = i - 4) runs before the body on each pass, so the first pass already sees the updated value. Right rule: The update runs after the body, before the next condition test; the first pass uses the initial value.
  - **[10] misconception** (rule type M, wrong rule / right rule) &rarr; `LoopUpdateChangesDirection`: wrong rule: The update of the loop variable can change from pass to pass (e.g. switch direction) although the code is the same. Right rule: The update expression is the same on every pass; the loop variable changes by the rule written in the update.
  - **[11] misconception** (rule type M, wrong rule / right rule) &rarr; `LoopStepAlwaysOne`: wrong rule: A loop variable always goes up or down by 1, whatever the update says (so i = i - 4 is read as i--). Right rule: The loop variable changes exactly as the update expression says (i += 2, i = i - 4, i \*= 2, ...).

**45. `loop_control` &rarr; `loop_control@L1`** (has_level)

- **Exact edge logic:** loop control -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).
  - **[0] names\_the\_element** (rule type N, identity rule): Loop control is the init / continuation condition / increment scheme on an index variable that decides how many passes a loop makes and with which values.
  - **[1] states\_the\_rule** (rule type S, declarative rule): Initialize an index variable, test a loop-continuation condition on it before each pass, and increment it as the last action of each pass; for (&lt;initialize&gt;; &lt;boolean expression&gt;; &lt;increment&gt;) packages the three. Choosing the loop: for when the passes are counted by an index, while when the loop runs until a condition changes, do-while when the body must run at least once; any one can be rewritten as another, so choose the clearest.

**46. `loop_control` &rarr; `loop_control@L2`** (has_level)

- **Exact edge logic:** loop control -&gt; L2 (Multistructural): the answer applies the rules of loop control to every part of the code, in order (3 ways).
  - **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): init (once) -&gt; test -&gt; body -&gt; update -&gt; test -&gt; body -&gt; update ... -&gt; test false -&gt; exit.
  - **[1] output\_prediction** (rule type OP, evaluation / result rule): The number of passes and the values seen follow from the three parts: for (int i = 0; i &lt;= N; i++) makes N+1 passes with i = 0..N; with i &lt; N it makes N passes; i += 2 visits every second value.
  - **[2] one\_step\_execution** (rule type OS, state-transition rule): One update changes only the loop variable, by exactly the rule written (i++ adds 1, i = i - 4 subtracts 4); one test reads it and returns true or false without changing it.

**47. `loop_control` &rarr; `loop_control@L3`** (has_level)

- **Exact edge logic:** loop control -&gt; L3 (Relational): the answer relates the parts (7 ways).
  - **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): All three control parts act on the loop variable: the init sets it, the condition tests it, the update changes it.
  - **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): The for header is exactly the three control slots, separated by semicolons; the body runs after the test and before the update.
  - **[2] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): The update i = i + 1 is usually written i++ (or i += k for other steps); as a whole update statement ++i and i++ are equivalent.
  - **[3] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): A loop is infinite when the update never moves the variable toward making the condition false (e.g. condition i &gt; 3 with update i = i + 1).
  - **[4] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): The continuation condition fixes the number of iterations, so a sharper bound (i &lt;= n/i instead of i &lt; n) can make a program dramatically faster.
  - **[5] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): The initialization and the condition of a loop fix how many times it runs; one wrong bound makes it run once too many or too few.
  - **[6] purpose\_of\_the\_whole** (rule type P, plan / role rule): Plan: counter-controlled loop - the loop variable is a stepper that walks a predictable sequence of values (0..N-1, 1..N, every 2nd value) and fixes the number of passes in advance.

**48. `loop_control` &rarr; `loop_control@L4`** (has_level)

- **Exact edge logic:** loop control -&gt; L4 (Extended abstract): the answer reasons beyond the given code (5 ways).
  - **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `PreIncrementBeforeLoop`: Changing &lt; to &lt;= adds one pass; starting at 1 instead of 0 removes one; doubling the step halves the passes; reversing init and bound with i-- visits the same values in reverse order (and still processes the same set only if both ends are adjusted).
  - **[1] diagnose\_an\_error** (rule type D, error rule): rule broken: The number of passes is fixed by the init, the test and the update together. Kind: silent logic error. Trigger class: Wrong start value, &lt; vs &lt;=, a wrong step, or an extra update of the counter in the body (or outside the loop): the loop runs too few or too many passes (off by one, or skips values).
  - **[2] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Use explicit init/test/update control when the passes are counted or follow a fixed step; when the number of passes depends on data computed in the body, control the loop by that data (a while condition) instead.
  - **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: The update must move the loop variable toward making the condition false. Kind: silent logic error. Trigger class: An update in the wrong direction or a condition that the update cannot falsify (e.g. i &gt; 3 with i++, or i != 10 with i += 3): infinite loop.
  - **[4] diagnose\_an\_error** (rule type D, error rule): rule broken: Do not control a loop by an equality test on double values. Kind: silent logic error. Trigger class: for (double x = 0.0; x &lt; 1.0; x += 0.1): after ten additions x is 0.9999999999999999, so the loop makes 11 passes instead of the intended 10.

**49. `topic1.3.c` &rarr; `loop_control`** (contains)

- topic `topic1.3.c` contains `loop_control`

**50. `topic1.3.c` &rarr; `loop_body`** (contains)

- topic `topic1.3.c` contains `loop_body`

**51. `topic1.3.c` &rarr; `loop_invariant_reasoning`** (contains)

- topic `topic1.3.c` contains `loop_invariant_reasoning`

**52. `topic1.3.c` &rarr; `while_loop`** (contains)

- topic `topic1.3.c` contains `while_loop`
