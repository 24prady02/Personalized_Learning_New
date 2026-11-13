# loop_body (`loop_body`)

the block repeated each pass

Section 1.3 Conditionals and Loops, topic 1.3.c While loops.

![The knowledge graph around loop_body](loop_body.png)

## At a glance

- **Needs first:** `do_while_loop`, `for_loop`, `while_loop`
- **Leads to:** `accumulator_pattern`, `counter_pattern`
- **Learned alongside:** nothing
- **Misconceptions:** `ComputerFillsInIntent`, `ForLoopPartSkipped`, `IfInLoopUnchecked`, `LoopBodyAlwaysOnce`, `LoopBodyStatementOutsideLoop`, `LoopCountIsStatementCount`, `LoopOutputSameEachPass`, `LoopRunsStatementsSeparately`, `StateChangeIgnoredAcrossPasses`, `StatementAfterLoopInBody`, `WhileStopsMidBody`
- **Errors:** `BracelessMultiStatementBody`
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 43 edges around this concept. The edge logic, the wrong and right rules and the exact rules of the ways are copied word for word from the graph.

## To work on (0)

Nothing is missing for this concept.

## What it needs first (3)

A prerequisite edge means the other concept has to be understood before `loop_body`.

### `do_while_loop` comes before `loop_body`

*do { body } while (c); -- body first, test after*

- **Edge:** `pre:do_while_loop->loop_body`
- **Exact edge logic:** The block between do and while is the loop body; it runs first and is repeated while the condition holds.
- **Grounding:** book\_passage

### `for_loop` comes before `loop_body`

*a while with init/condition/update packaged together*

- **Edge:** `pre:for_loop->loop_body`
- **Exact edge logic:** The statements in braces after the for header are the loop body; they run once on every pass, between the test and the increment, exactly as in a while loop.
- **Grounding:** book\_passage

### `while_loop` comes before `loop_body`

*repeat a block while a condition holds*

- **Edge:** `pre:while_loop->loop_body`
- **Exact edge logic:** The loop body is the block of statements that a while (or for) loop repeats on each pass.
- **Grounding:** book\_passage
- **Composition rule (R) of `loop_body` with `while_loop`:** The body is what the while repeats; the condition is tested only between complete executions of it.
- **Composition rule (R) of `while_loop` with `loop_body`:** The body is the block that the while repeats; it runs only after a true test and is completed before the next test.

## What it leads to (2)

These concepts need `loop_body` first.

### `loop_body` comes before `accumulator_pattern`

*building up a running total/result*

- **Edge:** `pre:loop_body->accumulator_pattern`
- **Exact edge logic:** The accumulator update sum += x sits inside the body, so it runs once on every pass.
- **Grounding:** book\_passage
- **Composition rule (R) of `loop_body` with `accumulator_pattern`:** The accumulator update (sum += x) is placed inside the body so it runs once per pass, while the accumulator is declared and initialized before the loop.
- **Composition rule (R) of `accumulator_pattern` with `loop_body`:** The update sum += x sits inside the body so it runs once per pass, while the declaration and initialization stay before the loop.

### `loop_body` comes before `counter_pattern`

*counting occurrences across passes*

- **Edge:** `pre:loop_body->counter_pattern`
- **Exact edge logic:** count++ sits inside the body, usually under an if, so it runs once on every pass that matches.
- **Grounding:** order\_only
- **Composition rule (R) of `loop_body` with `counter_pattern`:** count++ sits inside the body, often under an if, so it runs once on each pass that matches; the counter is declared before the loop.
- **Composition rule (R) of `counter_pattern` with `loop_body`:** The \`count++\` (with its guard) must be inside the loop body, while the declaration \`int count = 0;\` must be outside and before it. Inside the body it runs once for each matching pass. After the loop it runs only once, so the count is at most 1.

## Learned alongside (0)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

No parallel edge touches this concept.

## Misconceptions (11)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### ComputerFillsInIntent

- **Edge:** `loop_body` &rarr; `ComputerFillsInIntent` (misconception)
- **Exact edge logic (the wrong rule):** The computer fills in omitted steps or values that the programmer meant, e.g. REPEAT 4 [FORWARD 30] draws a square without a turn command.
- **Twin logic (the right rule):** The computer executes only what the code states; every needed step and value must be written.
- **Wrong belief (on the node):** The computer fills in omitted steps or values that the programmer meant, e.g. REPEAT 4 [FORWARD 30] draws a square without a turn command.
- **Correct rule (on the node):** The computer executes only what the code states; every needed step and value must be written.
- **Provenance:** published
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [8] misconception, exact rule:** wrong rule: The computer fills in omitted steps or values that the programmer meant, e.g. REPEAT 4 [FORWARD 30] draws a square without a turn command. Right rule: The computer executes only what the code states; every needed step and value must be written.
- **Edge `algorithm_pseudocode` &rarr; `ComputerFillsInIntent`, exact edge logic:** The computer fills in omitted steps or values that the programmer meant, e.g. REPEAT 4 [FORWARD 30] draws a square without a turn command. **Twin logic:** The computer executes only what the code states; every needed step and value must be written. (role: context)
- **Edge `program_text` &rarr; `ComputerFillsInIntent`, exact edge logic:** The computer fills in omitted steps or values that the programmer meant, e.g. REPEAT 4 [FORWARD 30] draws a square without a turn command. **Twin logic:** The computer executes only what the code states; every needed step and value must be written. (role: context)
- **Edge `statement` &rarr; `ComputerFillsInIntent`, exact edge logic:** The computer fills in omitted steps or values that the programmer meant, e.g. REPEAT 4 [FORWARD 30] draws a square without a turn command. **Twin logic:** The computer executes only what the code states; every needed step and value must be written. (role: primary)

### ForLoopPartSkipped

- **Edge:** `loop_body` &rarr; `ForLoopPartSkipped` (misconception)
- **Exact edge logic (the wrong rule):** A pass of a loop may leave out one of its parts (the condition test, the body, the update, or the initialization).
- **Twin logic (the right rule):** Each pass of a for loop runs test, then body, then update, every time; the initialization runs once, at the start.
- **Wrong belief (on the node):** A pass of a loop may leave out one of its parts (the condition test, the body, the update, or the initialization).
- **Correct rule (on the node):** Each pass of a for loop runs test, then body, then update, every time; the initialization runs once, at the start.
- **Provenance:** published
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [11] misconception, exact rule:** wrong rule: A pass of a loop may leave out one of its parts (the condition test, the body, the update, or the initialization). Right rule: Each pass of a for loop runs test, then body, then update, every time; the initialization runs once, at the start.
- **Edge `for_loop` &rarr; `ForLoopPartSkipped`, exact edge logic:** A pass of a loop may leave out one of its parts (the condition test, the body, the update, or the initialization). **Twin logic:** Each pass of a for loop runs test, then body, then update, every time; the initialization runs once, at the start. (role: primary)
- **Edge `loop_control` &rarr; `ForLoopPartSkipped`, exact edge logic:** A pass of a loop may leave out one of its parts (the condition test, the body, the update, or the initialization). **Twin logic:** Each pass of a for loop runs test, then body, then update, every time; the initialization runs once, at the start. (role: context)

### IfInLoopUnchecked

- **Edge:** `loop_body` &rarr; `IfInLoopUnchecked` (misconception)
- **Exact edge logic (the wrong rule):** An if inside a loop body runs its branch on every pass without testing its condition.
- **Twin logic (the right rule):** The if condition is tested again on every pass, with the current values, so the branch runs only on passes where it is true.
- **Wrong belief (on the node):** An if inside a loop body runs its branch on every pass without testing its condition.
- **Correct rule (on the node):** The if condition is tested again on every pass, with the current values, so the branch runs only on passes where it is true.
- **Provenance:** published
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [9] misconception, exact rule:** wrong rule: An if inside a loop body runs its branch on every pass without testing its condition. Right rule: The if condition is tested again on every pass, with the current values, so the branch runs only on passes where it is true.
- **Edge `if_statement` &rarr; `IfInLoopUnchecked`, exact edge logic:** An if inside a loop body runs its branch on every pass without testing its condition. **Twin logic:** The if condition is tested again on every pass, with the current values, so the branch runs only on passes where it is true. (role: primary)

### LoopBodyAlwaysOnce

- **Edge:** `loop_body` &rarr; `LoopBodyAlwaysOnce` (misconception)
- **Exact edge logic (the wrong rule):** The loop body always runs at least once, even if the condition is false at the start.
- **Twin logic (the right rule):** A while or for body runs zero times when the condition is false at the start.
- **Wrong belief (on the node):** The loop body always runs at least once, even if the condition is false at the start.
- **Correct rule (on the node):** A while or for body runs zero times when the condition is false at the start.
- **Provenance:** published
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [1] misconception, exact rule:** wrong rule: The loop body always runs at least once, even if the condition is false at the start. Right rule: A while or for body runs zero times when the condition is false at the start.
- **L0 way [6] inconsistent\_trace, exact rule:** Applies the body rule (LT) unevenly: runs all body statements on some passes but only some on others, includes the statement after the loop on some passes, or uses stale values from the first pass later. (here mixing in: "The loop body always runs at least once, even if the condition is false at the start")
- **Edge `while_loop` &rarr; `LoopBodyAlwaysOnce`, exact edge logic:** The loop body always runs at least once, even if the condition is false at the start. **Twin logic:** A while or for body runs zero times when the condition is false at the start. (role: primary)

### LoopBodyStatementOutsideLoop

- **Edge:** `loop_body` &rarr; `LoopBodyStatementOutsideLoop` (misconception)
- **Exact edge logic (the wrong rule):** Some statements inside the braces of a loop body are not repeated; they run once, before or after the loop.
- **Twin logic (the right rule):** Every statement inside the loop braces is part of the body and runs on every pass.
- **Wrong belief (on the node):** Some statements inside the braces of a loop body are not repeated; they run once, before or after the loop.
- **Correct rule (on the node):** Every statement inside the loop braces is part of the body and runs on every pass.
- **Provenance:** published
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [2] misconception, exact rule:** wrong rule: Some statements inside the braces of a loop body are not repeated; they run once, before or after the loop. Right rule: Every statement inside the loop braces is part of the body and runs on every pass.
- **Edge `block` &rarr; `LoopBodyStatementOutsideLoop`, exact edge logic:** Some statements inside the braces of a loop body are not repeated; they run once, before or after the loop. **Twin logic:** Every statement inside the loop braces is part of the body and runs on every pass. (role: context)

### LoopCountIsStatementCount

- **Edge:** `loop_body` &rarr; `LoopCountIsStatementCount` (misconception)
- **Exact edge logic (the wrong rule):** The repeat count of a counted loop says how many of the body statements are executed.
- **Twin logic (the right rule):** The repeat count is how many times the whole body runs; every pass runs all body statements.
- **Wrong belief (on the node):** The repeat count of a counted loop says how many of the body statements are executed.
- **Correct rule (on the node):** The repeat count is how many times the whole body runs; every pass runs all body statements.
- **Provenance:** published
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [10] misconception, exact rule:** wrong rule: The repeat count of a counted loop says how many of the body statements are executed. Right rule: The repeat count is how many times the whole body runs; every pass runs all body statements.
- **Edge `for_loop` &rarr; `LoopCountIsStatementCount`, exact edge logic:** The repeat count of a counted loop says how many of the body statements are executed. **Twin logic:** The repeat count is how many times the whole body runs; every pass runs all body statements. (role: primary)

### LoopOutputSameEachPass

- **Edge:** `loop_body` &rarr; `LoopOutputSameEachPass` (misconception)
- **Exact edge logic (the wrong rule):** A loop prints the same thing on every pass; the changing loop variable does not affect what the body does.
- **Twin logic (the right rule):** The body uses the current value of the loop variable, so its output can differ on each pass.
- **Wrong belief (on the node):** A loop prints the same thing on every pass; the changing loop variable does not affect what the body does.
- **Correct rule (on the node):** The body uses the current value of the loop variable, so its output can differ on each pass.
- **Provenance:** published
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [12] misconception, exact rule:** wrong rule: A loop prints the same thing on every pass; the changing loop variable does not affect what the body does. Right rule: The body uses the current value of the loop variable, so its output can differ on each pass.
- **Edge `loop_variable` &rarr; `LoopOutputSameEachPass`, exact edge logic:** A loop prints the same thing on every pass; the changing loop variable does not affect what the body does. **Twin logic:** The body uses the current value of the loop variable, so its output can differ on each pass. (role: primary)

### LoopRunsStatementsSeparately

- **Edge:** `loop_body` &rarr; `LoopRunsStatementsSeparately` (misconception)
- **Exact edge logic (the wrong rule):** A loop runs its first body statement all N times, then its second body statement all N times.
- **Twin logic (the right rule):** Each pass runs the whole body in order, so the body statements interleave: S1, S2, S1, S2, ...
- **Wrong belief (on the node):** A loop runs its first body statement all N times, then its second body statement all N times.
- **Correct rule (on the node):** Each pass runs the whole body in order, so the body statements interleave: S1, S2, S1, S2, ...
- **Provenance:** published
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [4] misconception, exact rule:** wrong rule: A loop runs its first body statement all N times, then its second body statement all N times. Right rule: Each pass runs the whole body in order, so the body statements interleave: S1, S2, S1, S2, ...

### StateChangeIgnoredAcrossPasses

- **Edge:** `loop_body` &rarr; `StateChangeIgnoredAcrossPasses` (misconception)
- **Exact edge logic (the wrong rule):** Values changed by one pass of a loop (other than the loop variable) do not affect later passes.
- **Twin logic (the right rule):** Each pass starts from the state left by the previous pass, so a change in one pass carries into the next ones.
- **Wrong belief (on the node):** Values changed by one pass of a loop (other than the loop variable) do not affect later passes.
- **Correct rule (on the node):** Each pass starts from the state left by the previous pass, so a change in one pass carries into the next ones.
- **Provenance:** published
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [5] misconception, exact rule:** wrong rule: Values changed by one pass of a loop (other than the loop variable) do not affect later passes. Right rule: Each pass starts from the state left by the previous pass, so a change in one pass carries into the next ones.
- **Edge `accumulator_pattern` &rarr; `StateChangeIgnoredAcrossPasses`, exact edge logic:** Values changed by one pass of a loop (other than the loop variable) do not affect later passes. **Twin logic:** Each pass starts from the state left by the previous pass, so a change in one pass carries into the next ones. (role: context)
- **Edge `program_state` &rarr; `StateChangeIgnoredAcrossPasses`, exact edge logic:** Values changed by one pass of a loop (other than the loop variable) do not affect later passes. **Twin logic:** Each pass starts from the state left by the previous pass, so a change in one pass carries into the next ones. (role: context)

### StatementAfterLoopInBody

- **Edge:** `loop_body` &rarr; `StatementAfterLoopInBody` (misconception)
- **Exact edge logic (the wrong rule):** A statement written after the loop is repeated with the loop body.
- **Twin logic (the right rule):** The body ends at the closing brace (or after its single statement); code after it runs once, after the loop ends.
- **Wrong belief (on the node):** A statement written after the loop is repeated with the loop body.
- **Correct rule (on the node):** The body ends at the closing brace (or after its single statement); code after it runs once, after the loop ends.
- **Provenance:** published
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [3] misconception, exact rule:** wrong rule: A statement written after the loop is repeated with the loop body. Right rule: The body ends at the closing brace (or after its single statement); code after it runs once, after the loop ends.
- **Edge `block` &rarr; `StatementAfterLoopInBody`, exact edge logic:** A statement written after the loop is repeated with the loop body. **Twin logic:** The body ends at the closing brace (or after its single statement); code after it runs once, after the loop ends. (role: context)

### WhileStopsMidBody

- **Edge:** `loop_body` &rarr; `WhileStopsMidBody` (misconception)
- **Exact edge logic (the wrong rule):** The loop stops the moment the condition becomes false, even in the middle of the body.
- **Twin logic (the right rule):** The condition is tested only before each pass, so the whole body finishes before the loop can stop.
- **Wrong belief (on the node):** The loop stops the moment the condition becomes false, even in the middle of the body.
- **Correct rule (on the node):** The condition is tested only before each pass, so the whole body finishes before the loop can stop.
- **Provenance:** published
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [7] misconception, exact rule:** wrong rule: The loop stops the moment the condition becomes false, even in the middle of the body. Right rule: The condition is tested only before each pass, so the whole body finishes before the loop can stop.
- **Edge `while_loop` &rarr; `WhileStopsMidBody`, exact edge logic:** The loop stops the moment the condition becomes false, even in the middle of the body. **Twin logic:** The condition is tested only before each pass, so the whole body finishes before the loop can stop. (role: primary)

## Errors (1)

An error edge states the rule that gets broken in a program, and the right rule.

### BracelessMultiStatementBody

- **Edge:** `loop_body` &rarr; `BracelessMultiStatementBody` (error)
- **Exact edge logic (the wrong rule):** Indenting several statements under an if or for makes them all part of its body, even without braces.
- **Twin logic (the right rule):** Without braces only the first statement belongs to the if/for; the rest run once, after it.
- **Wrong belief (on the node):** Indenting several statements under an if or for makes them all part of its body, even without braces.
- **Correct rule (on the node):** Without braces only the first statement belongs to the if/for; the rest run once, after it.
- **Provenance:** textbook
- **Role of this concept:** primary
- **Edge `for_loop` &rarr; `BracelessMultiStatementBody`, exact edge logic:** Indenting several statements under an if or for makes them all part of its body, even without braces. **Twin logic:** Without braces only the first statement belongs to the if/for; the rest run once, after it. (role: context)
- **Edge `if_statement` &rarr; `BracelessMultiStatementBody`, exact edge logic:** Indenting several statements under an if or for makes them all part of its body, even without braces. **Twin logic:** Without braces only the first statement belongs to the if/for; the rest run once, after it. (role: context)
- **Edge `nested_loops` &rarr; `BracelessMultiStatementBody`, exact edge logic:** Indenting several statements under an if or for makes them all part of its body, even without braces. **Twin logic:** Without braces only the first statement belongs to the if/for; the rest run once, after it. (role: context)

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for loop body: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to loop body agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

- **Edge:** `loop_body` &rarr; `loop_body@L0` (has_level)
- **Exact edge logic:** loop body -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (13 ways).

Ways (13), each with its exact rule:

- **[0] everyday\_reading** (rule type E, folk-meaning rule): Folk meaning: an everyday 'repeat this' instruction can be read loosely - a helper fills in missing steps, does each step N times in turn, or stops partway. A Java loop body is exactly the statements inside its braces (or one statement), all executed in order on every pass.
- **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `LoopBodyAlwaysOnce`: wrong rule: The loop body always runs at least once, even if the condition is false at the start. Right rule: A while or for body runs zero times when the condition is false at the start.
- **[2] misconception** (rule type M, wrong rule / right rule) &rarr; `LoopBodyStatementOutsideLoop`: wrong rule: Some statements inside the braces of a loop body are not repeated; they run once, before or after the loop. Right rule: Every statement inside the loop braces is part of the body and runs on every pass.
- **[3] misconception** (rule type M, wrong rule / right rule) &rarr; `StatementAfterLoopInBody`: wrong rule: A statement written after the loop is repeated with the loop body. Right rule: The body ends at the closing brace (or after its single statement); code after it runs once, after the loop ends.
- **[4] misconception** (rule type M, wrong rule / right rule) &rarr; `LoopRunsStatementsSeparately`: wrong rule: A loop runs its first body statement all N times, then its second body statement all N times. Right rule: Each pass runs the whole body in order, so the body statements interleave: S1, S2, S1, S2, ...
- **[5] misconception** (rule type M, wrong rule / right rule) &rarr; `StateChangeIgnoredAcrossPasses`: wrong rule: Values changed by one pass of a loop (other than the loop variable) do not affect later passes. Right rule: Each pass starts from the state left by the previous pass, so a change in one pass carries into the next ones.
- **[6] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `LoopBodyAlwaysOnce`: Applies the body rule (LT) unevenly: runs all body statements on some passes but only some on others, includes the statement after the loop on some passes, or uses stale values from the first pass later. (here mixing in: "The loop body always runs at least once, even if the condition is false at the start")
- **[7] misconception** (rule type M, wrong rule / right rule) &rarr; `WhileStopsMidBody`: wrong rule: The loop stops the moment the condition becomes false, even in the middle of the body. Right rule: The condition is tested only before each pass, so the whole body finishes before the loop can stop.
- **[8] misconception** (rule type M, wrong rule / right rule) &rarr; `ComputerFillsInIntent`: wrong rule: The computer fills in omitted steps or values that the programmer meant, e.g. REPEAT 4 [FORWARD 30] draws a square without a turn command. Right rule: The computer executes only what the code states; every needed step and value must be written.
- **[9] misconception** (rule type M, wrong rule / right rule) &rarr; `IfInLoopUnchecked`: wrong rule: An if inside a loop body runs its branch on every pass without testing its condition. Right rule: The if condition is tested again on every pass, with the current values, so the branch runs only on passes where it is true.
- **[10] misconception** (rule type M, wrong rule / right rule) &rarr; `LoopCountIsStatementCount`: wrong rule: The repeat count of a counted loop says how many of the body statements are executed. Right rule: The repeat count is how many times the whole body runs; every pass runs all body statements.
- **[11] misconception** (rule type M, wrong rule / right rule) &rarr; `ForLoopPartSkipped`: wrong rule: A pass of a loop may leave out one of its parts (the condition test, the body, the update, or the initialization). Right rule: Each pass of a for loop runs test, then body, then update, every time; the initialization runs once, at the start.
- **[12] misconception** (rule type M, wrong rule / right rule) &rarr; `LoopOutputSameEachPass`: wrong rule: A loop prints the same thing on every pass; the changing loop variable does not affect what the body does. Right rule: The body uses the current value of the loop variable, so its output can differ on each pass.

### L1: Unistructural / atom x text surface

L1 for loop body: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

- **Edge:** `loop_body` &rarr; `loop_body@L1` (has_level)
- **Exact edge logic:** loop body -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

Ways (2), each with its exact rule:

- **[0] names\_the\_element** (rule type N, identity rule): The loop body is the statement block that a loop repeats on each pass.
- **[1] states\_the\_rule** (rule type S, declarative rule): The body is the block after the loop header; braces are optional only if it is a single statement, in which case only that one statement is repeated.

### L2: Multistructural / block x execution / preoperational

L2 for loop body: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

- **Edge:** `loop_body` &rarr; `loop_body@L2` (has_level)
- **Exact edge logic:** loop body -&gt; L2 (Multistructural): the answer applies the rules of loop body to every part of the code, in order (3 ways).

Ways (3), each with its exact rule:

- **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): On each pass the body's statements run in order, first to last, after a true test (and, in a for loop, before the update); the next pass starts from the state left by this one.
- **[1] output\_prediction** (rule type OP, evaluation / result rule): The body's output on each pass depends on the current values, so successive passes can print different lines: TenHellos prints '4th Hello', '5th Hello', ...; the number of executions of each body statement equals the number of passes.
- **[2] one\_step\_execution** (rule type OS, state-transition rule): One pass of the body changes exactly the variables it assigns (e.g. print i and v, double v, increment i) and these changes carry into the next test and pass.

### L3: Relational / relations x function (concrete operational begins)

L3 for loop body: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

- **Edge:** `loop_body` &rarr; `loop_body@L3` (has_level)
- **Exact edge logic:** loop body -&gt; L3 (Relational): the answer relates the parts (4 ways).

Ways (4), each with its exact rule:

- **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): The accumulator update (sum += x) is placed inside the body so it runs once per pass, while the accumulator is declared and initialized before the loop.
- **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): count++ sits inside the body, often under an if, so it runs once on each pass that matches; the counter is declared before the loop.
- **[2] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): The body is what the while repeats; the condition is tested only between complete executions of it.
- **[3] purpose\_of\_the\_whole** (rule type P, plan / role rule): Plan: the body is the 'process one item / one step' part of a loop plan: each pass performs the same process on a new value (next element, next bet, next term).

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for loop body: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

- **Edge:** `loop_body` &rarr; `loop_body@L4` (has_level)
- **Exact edge logic:** loop body -&gt; L4 (Extended abstract): the answer reasons beyond the given code (3 ways).

Ways (3), each with its exact rule:

- **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `LoopBodyAlwaysOnce`: Moving a statement from inside the body to after the loop changes it from running once per pass to once in total (and vice versa); reordering two body statements that share a variable changes the results (e.g. increment before vs after use).
- **[1] diagnose\_an\_error** (rule type D, error rule): rule broken: Without braces, the body of an if, while or for is exactly one statement; indentation does not add statements to it. Kind: silent logic error. Trigger class: A braceless header followed by two or more indented statements: only the first is controlled, the others run once, after the if/loop, on every input.
- **[2] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Put inside the body exactly what must happen once per pass; put set-up before the loop and final reporting after it. Always brace a multi-statement body.

## Same topic

`loop_body` belongs to the topic **While loops** (`topic1.3.c`). The topic also contains: `loop_control`, `loop_invariant_reasoning`, `while_loop`.

## Rules of the concept (25)

- **Book** (SW-1e, p. 49 (pdf 59)): "We often refer to the statement block in a loop as the body of the loop."
- **Book** (SW-1e, p. 49 (pdf 59)): "As with the if statement, the braces are optional if a while loop body has just one statement."
- **Book** (SW-1.3, ): "The while loop enables us to execute a group of statements many times."
- **E** (folk-meaning rule): Folk meaning: an everyday 'repeat this' instruction can be read loosely - a helper fills in missing steps, does each step N times in turn, or stops partway. A Java loop body is exactly the statements inside its braces (or one statement), all executed in order on every pass.
- **M** (wrong rule / right rule): LoopBodyAlwaysOnce: wrong: The loop body always runs at least once, even if the condition is false at the start. \| right: A while or for body runs zero times when the condition is false at the start.
- **M** (wrong rule / right rule): WhileStopsMidBody: wrong: The loop stops the moment the condition becomes false, even in the middle of the body. \| right: The condition is tested only before each pass, so the whole body finishes before the loop can stop.
- **M** (wrong rule / right rule): ComputerFillsInIntent: wrong: The computer fills in omitted steps or values that the programmer meant, e.g. REPEAT 4 [FORWARD 30] draws a square without a turn command. \| right: The computer executes only what the code states; every needed step and value must be written.
- **M** (wrong rule / right rule): IfInLoopUnchecked: wrong: An if inside a loop body runs its branch on every pass without testing its condition. \| right: The if condition is tested again on every pass, with the current values, so the branch runs only on passes where it is true.
- **M** (wrong rule / right rule): LoopCountIsStatementCount: wrong: The repeat count of a counted loop says how many of the body statements are executed. \| right: The repeat count is how many times the whole body runs; every pass runs all body statements.
- **M** (wrong rule / right rule): LoopBodyStatementOutsideLoop: wrong: Some statements inside the braces of a loop body are not repeated; they run once, before or after the loop. \| right: Every statement inside the loop braces is part of the body and runs on every pass.
- **M** (wrong rule / right rule): StatementAfterLoopInBody: wrong: A statement written after the loop is repeated with the loop body. \| right: The body ends at the closing brace (or after its single statement); code after it runs once, after the loop ends.
- **M** (wrong rule / right rule): ForLoopPartSkipped: wrong: A pass of a loop may leave out one of its parts (the condition test, the body, the update, or the initialization). \| right: Each pass of a for loop runs test, then body, then update, every time; the initialization runs once, at the start.
- **M** (wrong rule / right rule): LoopRunsStatementsSeparately: wrong: A loop runs its first body statement all N times, then its second body statement all N times. \| right: Each pass runs the whole body in order, so the body statements interleave: S1, S2, S1, S2, ...
- **M** (wrong rule / right rule): LoopOutputSameEachPass: wrong: A loop prints the same thing on every pass; the changing loop variable does not affect what the body does. \| right: The body uses the current value of the loop variable, so its output can differ on each pass.
- **M** (wrong rule / right rule): StateChangeIgnoredAcrossPasses: wrong: Values changed by one pass of a loop (other than the loop variable) do not affect later passes. \| right: Each pass starts from the state left by the previous pass, so a change in one pass carries into the next ones.
- **T** (uneven-application rule): Applies the body rule (LT) unevenly: runs all body statements on some passes but only some on others, includes the statement after the loop on some passes, or uses stale values from the first pass later.
- **N** (identity rule): The loop body is the statement block that a loop repeats on each pass.
- **S** (declarative rule): The body is the block after the loop header; braces are optional only if it is a single statement, in which case only that one statement is repeated.
- **LT** (operational sequencing rule): On each pass the body's statements run in order, first to last, after a true test (and, in a for loop, before the update); the next pass starts from the state left by this one.
- **OP** (evaluation / result rule): The body's output on each pass depends on the current values, so successive passes can print different lines: TenHellos prints '4th Hello', '5th Hello', ...; the number of executions of each body statement equals the number of passes.
- **OS** (state-transition rule): One pass of the body changes exactly the variables it assigns (e.g. print i and v, double v, increment i) and these changes carry into the next test and pass.
- **R** (composition rule (with a neighbour)): with accumulator\_pattern: The accumulator update (sum += x) is placed inside the body so it runs once per pass, while the accumulator is declared and initialized before the loop.
- **R** (composition rule (with a neighbour)): with counter\_pattern: count++ sits inside the body, often under an if, so it runs once on each pass that matches; the counter is declared before the loop.
- **R** (composition rule (with a neighbour)): with while\_loop: The body is what the while repeats; the condition is tested only between complete executions of it.
- **P** (plan / role rule): Plan: the body is the 'process one item / one step' part of a loop plan: each pass performs the same process on a new value (next element, next bet, next term).
- **C** (conservation rule): Moving a statement from inside the body to after the loop changes it from running once per pass to once in total (and vice versa); reordering two body statements that share a variable changes the results (e.g. increment before vs after use).
- **D** (error rule): rule broken: Without braces, the body of an if, while or for is exactly one statement; indentation does not add statements to it. (silent logic error)
- **X** (applicability rule): Put inside the body exactly what must happen once per pass; put set-up before the loop and final reporting after it. Always brace a multi-statement body.

## How it is found in code and answers (reader block)

- **Aliases:** loop body, body of the loop, inside the loop
- **Code patterns:** `\b(?:for|while)\s*\(`, `\bdo\s*\{`
- **Operator symbols:** none
- **Java types:** none

## The whole prerequisite chain

- **Everything it builds on (16):** `arithmetic_operators`, `boolean`, `boolean_expression`, `comparison_operators`, `data_type`, `do_while_loop`, `expression`, `for_loop`, `identifier`, `literal`, `logical_operators`, `loop_control`, `loop_variable`, `primitive_type`, `variable`, `while_loop`
- **Everything that builds on it (6):** `accumulator_pattern`, `counter_pattern`, `frequency_counting`, `monte_carlo_simulation`, `sentinel_loop`, `two_models`

## Every edge in this view and its exact edge logic (43)

All the edges drawn in the picture, in the order: prerequisite, parallel, misconception, error, has_level, contains.

**1. `do_while_loop` &rarr; `loop_body`** (prerequisite)

- **Exact edge logic:** The block between do and while is the loop body; it runs first and is repeated while the condition holds.
- **Grounding:** book\_passage

**2. `for_loop` &rarr; `loop_body`** (prerequisite)

- **Exact edge logic:** The statements in braces after the for header are the loop body; they run once on every pass, between the test and the increment, exactly as in a while loop.
- **Grounding:** book\_passage

**3. `loop_body` &rarr; `accumulator_pattern`** (prerequisite)

- **Exact edge logic:** The accumulator update sum += x sits inside the body, so it runs once on every pass.
- **Grounding:** book\_passage
- **Composition rule (R) of `loop_body` with `accumulator_pattern`:** The accumulator update (sum += x) is placed inside the body so it runs once per pass, while the accumulator is declared and initialized before the loop.
- **Composition rule (R) of `accumulator_pattern` with `loop_body`:** The update sum += x sits inside the body so it runs once per pass, while the declaration and initialization stay before the loop.

**4. `loop_body` &rarr; `counter_pattern`** (prerequisite)

- **Exact edge logic:** count++ sits inside the body, usually under an if, so it runs once on every pass that matches.
- **Grounding:** order\_only
- **Composition rule (R) of `loop_body` with `counter_pattern`:** count++ sits inside the body, often under an if, so it runs once on each pass that matches; the counter is declared before the loop.
- **Composition rule (R) of `counter_pattern` with `loop_body`:** The \`count++\` (with its guard) must be inside the loop body, while the declaration \`int count = 0;\` must be outside and before it. Inside the body it runs once for each matching pass. After the loop it runs only once, so the count is at most 1.

**5. `while_loop` &rarr; `loop_body`** (prerequisite)

- **Exact edge logic:** The loop body is the block of statements that a while (or for) loop repeats on each pass.
- **Grounding:** book\_passage
- **Composition rule (R) of `while_loop` with `loop_body`:** The body is the block that the while repeats; it runs only after a true test and is completed before the next test.
- **Composition rule (R) of `loop_body` with `while_loop`:** The body is what the while repeats; the condition is tested only between complete executions of it.

**6. `loop_body` &rarr; `ComputerFillsInIntent`** (misconception)

- **Exact edge logic (the wrong rule):** The computer fills in omitted steps or values that the programmer meant, e.g. REPEAT 4 [FORWARD 30] draws a square without a turn command.
- **Twin logic (the right rule):** The computer executes only what the code states; every needed step and value must be written.
- **Role:** context

**7. `loop_body` &rarr; `ForLoopPartSkipped`** (misconception)

- **Exact edge logic (the wrong rule):** A pass of a loop may leave out one of its parts (the condition test, the body, the update, or the initialization).
- **Twin logic (the right rule):** Each pass of a for loop runs test, then body, then update, every time; the initialization runs once, at the start.
- **Role:** context

**8. `loop_body` &rarr; `IfInLoopUnchecked`** (misconception)

- **Exact edge logic (the wrong rule):** An if inside a loop body runs its branch on every pass without testing its condition.
- **Twin logic (the right rule):** The if condition is tested again on every pass, with the current values, so the branch runs only on passes where it is true.
- **Role:** context

**9. `loop_body` &rarr; `LoopBodyAlwaysOnce`** (misconception)

- **Exact edge logic (the wrong rule):** The loop body always runs at least once, even if the condition is false at the start.
- **Twin logic (the right rule):** A while or for body runs zero times when the condition is false at the start.
- **Role:** context

**10. `loop_body` &rarr; `LoopBodyStatementOutsideLoop`** (misconception)

- **Exact edge logic (the wrong rule):** Some statements inside the braces of a loop body are not repeated; they run once, before or after the loop.
- **Twin logic (the right rule):** Every statement inside the loop braces is part of the body and runs on every pass.
- **Role:** primary

**11. `loop_body` &rarr; `LoopCountIsStatementCount`** (misconception)

- **Exact edge logic (the wrong rule):** The repeat count of a counted loop says how many of the body statements are executed.
- **Twin logic (the right rule):** The repeat count is how many times the whole body runs; every pass runs all body statements.
- **Role:** context

**12. `loop_body` &rarr; `LoopOutputSameEachPass`** (misconception)

- **Exact edge logic (the wrong rule):** A loop prints the same thing on every pass; the changing loop variable does not affect what the body does.
- **Twin logic (the right rule):** The body uses the current value of the loop variable, so its output can differ on each pass.
- **Role:** context

**13. `loop_body` &rarr; `LoopRunsStatementsSeparately`** (misconception)

- **Exact edge logic (the wrong rule):** A loop runs its first body statement all N times, then its second body statement all N times.
- **Twin logic (the right rule):** Each pass runs the whole body in order, so the body statements interleave: S1, S2, S1, S2, ...
- **Role:** primary

**14. `loop_body` &rarr; `StateChangeIgnoredAcrossPasses`** (misconception)

- **Exact edge logic (the wrong rule):** Values changed by one pass of a loop (other than the loop variable) do not affect later passes.
- **Twin logic (the right rule):** Each pass starts from the state left by the previous pass, so a change in one pass carries into the next ones.
- **Role:** primary

**15. `loop_body` &rarr; `StatementAfterLoopInBody`** (misconception)

- **Exact edge logic (the wrong rule):** A statement written after the loop is repeated with the loop body.
- **Twin logic (the right rule):** The body ends at the closing brace (or after its single statement); code after it runs once, after the loop ends.
- **Role:** primary

**16. `loop_body` &rarr; `WhileStopsMidBody`** (misconception)

- **Exact edge logic (the wrong rule):** The loop stops the moment the condition becomes false, even in the middle of the body.
- **Twin logic (the right rule):** The condition is tested only before each pass, so the whole body finishes before the loop can stop.
- **Role:** context

**17. `accumulator_pattern` &rarr; `StateChangeIgnoredAcrossPasses`** (misconception)

- **Exact edge logic (the wrong rule):** Values changed by one pass of a loop (other than the loop variable) do not affect later passes.
- **Twin logic (the right rule):** Each pass starts from the state left by the previous pass, so a change in one pass carries into the next ones.
- **Role:** context

**18. `algorithm_pseudocode` &rarr; `ComputerFillsInIntent`** (misconception)

- **Exact edge logic (the wrong rule):** The computer fills in omitted steps or values that the programmer meant, e.g. REPEAT 4 [FORWARD 30] draws a square without a turn command.
- **Twin logic (the right rule):** The computer executes only what the code states; every needed step and value must be written.
- **Role:** context

**19. `block` &rarr; `LoopBodyStatementOutsideLoop`** (misconception)

- **Exact edge logic (the wrong rule):** Some statements inside the braces of a loop body are not repeated; they run once, before or after the loop.
- **Twin logic (the right rule):** Every statement inside the loop braces is part of the body and runs on every pass.
- **Role:** context

**20. `block` &rarr; `StatementAfterLoopInBody`** (misconception)

- **Exact edge logic (the wrong rule):** A statement written after the loop is repeated with the loop body.
- **Twin logic (the right rule):** The body ends at the closing brace (or after its single statement); code after it runs once, after the loop ends.
- **Role:** context

**21. `for_loop` &rarr; `ForLoopPartSkipped`** (misconception)

- **Exact edge logic (the wrong rule):** A pass of a loop may leave out one of its parts (the condition test, the body, the update, or the initialization).
- **Twin logic (the right rule):** Each pass of a for loop runs test, then body, then update, every time; the initialization runs once, at the start.
- **Role:** primary

**22. `for_loop` &rarr; `LoopCountIsStatementCount`** (misconception)

- **Exact edge logic (the wrong rule):** The repeat count of a counted loop says how many of the body statements are executed.
- **Twin logic (the right rule):** The repeat count is how many times the whole body runs; every pass runs all body statements.
- **Role:** primary

**23. `if_statement` &rarr; `IfInLoopUnchecked`** (misconception)

- **Exact edge logic (the wrong rule):** An if inside a loop body runs its branch on every pass without testing its condition.
- **Twin logic (the right rule):** The if condition is tested again on every pass, with the current values, so the branch runs only on passes where it is true.
- **Role:** primary

**24. `loop_control` &rarr; `ForLoopPartSkipped`** (misconception)

- **Exact edge logic (the wrong rule):** A pass of a loop may leave out one of its parts (the condition test, the body, the update, or the initialization).
- **Twin logic (the right rule):** Each pass of a for loop runs test, then body, then update, every time; the initialization runs once, at the start.
- **Role:** context

**25. `loop_variable` &rarr; `LoopOutputSameEachPass`** (misconception)

- **Exact edge logic (the wrong rule):** A loop prints the same thing on every pass; the changing loop variable does not affect what the body does.
- **Twin logic (the right rule):** The body uses the current value of the loop variable, so its output can differ on each pass.
- **Role:** primary

**26. `program_state` &rarr; `StateChangeIgnoredAcrossPasses`** (misconception)

- **Exact edge logic (the wrong rule):** Values changed by one pass of a loop (other than the loop variable) do not affect later passes.
- **Twin logic (the right rule):** Each pass starts from the state left by the previous pass, so a change in one pass carries into the next ones.
- **Role:** context

**27. `program_text` &rarr; `ComputerFillsInIntent`** (misconception)

- **Exact edge logic (the wrong rule):** The computer fills in omitted steps or values that the programmer meant, e.g. REPEAT 4 [FORWARD 30] draws a square without a turn command.
- **Twin logic (the right rule):** The computer executes only what the code states; every needed step and value must be written.
- **Role:** context

**28. `statement` &rarr; `ComputerFillsInIntent`** (misconception)

- **Exact edge logic (the wrong rule):** The computer fills in omitted steps or values that the programmer meant, e.g. REPEAT 4 [FORWARD 30] draws a square without a turn command.
- **Twin logic (the right rule):** The computer executes only what the code states; every needed step and value must be written.
- **Role:** primary

**29. `while_loop` &rarr; `LoopBodyAlwaysOnce`** (misconception)

- **Exact edge logic (the wrong rule):** The loop body always runs at least once, even if the condition is false at the start.
- **Twin logic (the right rule):** A while or for body runs zero times when the condition is false at the start.
- **Role:** primary

**30. `while_loop` &rarr; `WhileStopsMidBody`** (misconception)

- **Exact edge logic (the wrong rule):** The loop stops the moment the condition becomes false, even in the middle of the body.
- **Twin logic (the right rule):** The condition is tested only before each pass, so the whole body finishes before the loop can stop.
- **Role:** primary

**31. `loop_body` &rarr; `BracelessMultiStatementBody`** (error)

- **Exact edge logic (the wrong rule):** Indenting several statements under an if or for makes them all part of its body, even without braces.
- **Twin logic (the right rule):** Without braces only the first statement belongs to the if/for; the rest run once, after it.
- **Role:** primary

**32. `for_loop` &rarr; `BracelessMultiStatementBody`** (error)

- **Exact edge logic (the wrong rule):** Indenting several statements under an if or for makes them all part of its body, even without braces.
- **Twin logic (the right rule):** Without braces only the first statement belongs to the if/for; the rest run once, after it.
- **Role:** context

**33. `if_statement` &rarr; `BracelessMultiStatementBody`** (error)

- **Exact edge logic (the wrong rule):** Indenting several statements under an if or for makes them all part of its body, even without braces.
- **Twin logic (the right rule):** Without braces only the first statement belongs to the if/for; the rest run once, after it.
- **Role:** context

**34. `nested_loops` &rarr; `BracelessMultiStatementBody`** (error)

- **Exact edge logic (the wrong rule):** Indenting several statements under an if or for makes them all part of its body, even without braces.
- **Twin logic (the right rule):** Without braces only the first statement belongs to the if/for; the rest run once, after it.
- **Role:** context

**35. `loop_body` &rarr; `loop_body@L0`** (has_level)

- **Exact edge logic:** loop body -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (13 ways).
  - **[0] everyday\_reading** (rule type E, folk-meaning rule): Folk meaning: an everyday 'repeat this' instruction can be read loosely - a helper fills in missing steps, does each step N times in turn, or stops partway. A Java loop body is exactly the statements inside its braces (or one statement), all executed in order on every pass.
  - **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `LoopBodyAlwaysOnce`: wrong rule: The loop body always runs at least once, even if the condition is false at the start. Right rule: A while or for body runs zero times when the condition is false at the start.
  - **[2] misconception** (rule type M, wrong rule / right rule) &rarr; `LoopBodyStatementOutsideLoop`: wrong rule: Some statements inside the braces of a loop body are not repeated; they run once, before or after the loop. Right rule: Every statement inside the loop braces is part of the body and runs on every pass.
  - **[3] misconception** (rule type M, wrong rule / right rule) &rarr; `StatementAfterLoopInBody`: wrong rule: A statement written after the loop is repeated with the loop body. Right rule: The body ends at the closing brace (or after its single statement); code after it runs once, after the loop ends.
  - **[4] misconception** (rule type M, wrong rule / right rule) &rarr; `LoopRunsStatementsSeparately`: wrong rule: A loop runs its first body statement all N times, then its second body statement all N times. Right rule: Each pass runs the whole body in order, so the body statements interleave: S1, S2, S1, S2, ...
  - **[5] misconception** (rule type M, wrong rule / right rule) &rarr; `StateChangeIgnoredAcrossPasses`: wrong rule: Values changed by one pass of a loop (other than the loop variable) do not affect later passes. Right rule: Each pass starts from the state left by the previous pass, so a change in one pass carries into the next ones.
  - **[6] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `LoopBodyAlwaysOnce`: Applies the body rule (LT) unevenly: runs all body statements on some passes but only some on others, includes the statement after the loop on some passes, or uses stale values from the first pass later. (here mixing in: "The loop body always runs at least once, even if the condition is false at the start")
  - **[7] misconception** (rule type M, wrong rule / right rule) &rarr; `WhileStopsMidBody`: wrong rule: The loop stops the moment the condition becomes false, even in the middle of the body. Right rule: The condition is tested only before each pass, so the whole body finishes before the loop can stop.
  - **[8] misconception** (rule type M, wrong rule / right rule) &rarr; `ComputerFillsInIntent`: wrong rule: The computer fills in omitted steps or values that the programmer meant, e.g. REPEAT 4 [FORWARD 30] draws a square without a turn command. Right rule: The computer executes only what the code states; every needed step and value must be written.
  - **[9] misconception** (rule type M, wrong rule / right rule) &rarr; `IfInLoopUnchecked`: wrong rule: An if inside a loop body runs its branch on every pass without testing its condition. Right rule: The if condition is tested again on every pass, with the current values, so the branch runs only on passes where it is true.
  - **[10] misconception** (rule type M, wrong rule / right rule) &rarr; `LoopCountIsStatementCount`: wrong rule: The repeat count of a counted loop says how many of the body statements are executed. Right rule: The repeat count is how many times the whole body runs; every pass runs all body statements.
  - **[11] misconception** (rule type M, wrong rule / right rule) &rarr; `ForLoopPartSkipped`: wrong rule: A pass of a loop may leave out one of its parts (the condition test, the body, the update, or the initialization). Right rule: Each pass of a for loop runs test, then body, then update, every time; the initialization runs once, at the start.
  - **[12] misconception** (rule type M, wrong rule / right rule) &rarr; `LoopOutputSameEachPass`: wrong rule: A loop prints the same thing on every pass; the changing loop variable does not affect what the body does. Right rule: The body uses the current value of the loop variable, so its output can differ on each pass.

**36. `loop_body` &rarr; `loop_body@L1`** (has_level)

- **Exact edge logic:** loop body -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).
  - **[0] names\_the\_element** (rule type N, identity rule): The loop body is the statement block that a loop repeats on each pass.
  - **[1] states\_the\_rule** (rule type S, declarative rule): The body is the block after the loop header; braces are optional only if it is a single statement, in which case only that one statement is repeated.

**37. `loop_body` &rarr; `loop_body@L2`** (has_level)

- **Exact edge logic:** loop body -&gt; L2 (Multistructural): the answer applies the rules of loop body to every part of the code, in order (3 ways).
  - **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): On each pass the body's statements run in order, first to last, after a true test (and, in a for loop, before the update); the next pass starts from the state left by this one.
  - **[1] output\_prediction** (rule type OP, evaluation / result rule): The body's output on each pass depends on the current values, so successive passes can print different lines: TenHellos prints '4th Hello', '5th Hello', ...; the number of executions of each body statement equals the number of passes.
  - **[2] one\_step\_execution** (rule type OS, state-transition rule): One pass of the body changes exactly the variables it assigns (e.g. print i and v, double v, increment i) and these changes carry into the next test and pass.

**38. `loop_body` &rarr; `loop_body@L3`** (has_level)

- **Exact edge logic:** loop body -&gt; L3 (Relational): the answer relates the parts (4 ways).
  - **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): The accumulator update (sum += x) is placed inside the body so it runs once per pass, while the accumulator is declared and initialized before the loop.
  - **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): count++ sits inside the body, often under an if, so it runs once on each pass that matches; the counter is declared before the loop.
  - **[2] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): The body is what the while repeats; the condition is tested only between complete executions of it.
  - **[3] purpose\_of\_the\_whole** (rule type P, plan / role rule): Plan: the body is the 'process one item / one step' part of a loop plan: each pass performs the same process on a new value (next element, next bet, next term).

**39. `loop_body` &rarr; `loop_body@L4`** (has_level)

- **Exact edge logic:** loop body -&gt; L4 (Extended abstract): the answer reasons beyond the given code (3 ways).
  - **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `LoopBodyAlwaysOnce`: Moving a statement from inside the body to after the loop changes it from running once per pass to once in total (and vice versa); reordering two body statements that share a variable changes the results (e.g. increment before vs after use).
  - **[1] diagnose\_an\_error** (rule type D, error rule): rule broken: Without braces, the body of an if, while or for is exactly one statement; indentation does not add statements to it. Kind: silent logic error. Trigger class: A braceless header followed by two or more indented statements: only the first is controlled, the others run once, after the if/loop, on every input.
  - **[2] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Put inside the body exactly what must happen once per pass; put set-up before the loop and final reporting after it. Always brace a multi-statement body.

**40. `topic1.3.c` &rarr; `loop_body`** (contains)

- topic `topic1.3.c` contains `loop_body`

**41. `topic1.3.c` &rarr; `loop_control`** (contains)

- topic `topic1.3.c` contains `loop_control`

**42. `topic1.3.c` &rarr; `loop_invariant_reasoning`** (contains)

- topic `topic1.3.c` contains `loop_invariant_reasoning`

**43. `topic1.3.c` &rarr; `while_loop`** (contains)

- topic `topic1.3.c` contains `while_loop`
