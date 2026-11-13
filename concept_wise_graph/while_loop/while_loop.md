# while_loop (`while_loop`)

repeat a block while a condition holds

Section 1.3 Conditionals and Loops, topic 1.3.c While loops.

![The knowledge graph around while_loop](while_loop.png)

## At a glance

- **Needs first:** `boolean_expression`
- **Leads to:** `animation`, `break_statement`, `continue_statement`, `convergence_test`, `do_while_loop`, `infinite_loop`, `loop_body`, `loop_control`, `loop_invariant_reasoning`, `loop_variable`, `number_conversion`, `sentinel_loop`
- **Learned alongside:** `if_statement`
- **Misconceptions:** `FalseLoopRepeatsNextCode`, `ForWhileNotInterchangeable`, `IfIsLoop`, `InfiniteLoopUnnoticed`, `JavaDetectsInfiniteLoops`, `LoopBodyAlwaysOnce`, `LoopConditionValidatedLater`, `LoopCountByIntent`, `LoopForOneTimeTest`, `LoopImpliedByOneTest`, `LoopTerminatingCondition`, `LoopVariableNotUpdated`, `MissingBraces`, `ProgramEndsAfterLoop`, `SingleIterationInsteadOfLoop`, `WhileStopsMidBody`
- **Errors:** `LoopIgnoresCodeBefore`, `SemicolonAfterIfHeader`, `SemicolonAfterLoopHeader`
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 73 edges around this concept. The edge logic, the wrong and right rules and the exact rules of the ways are copied word for word from the graph.

## To work on (1)

- misconceptions with no L0 way linked to them: MissingBraces

## What it needs first (1)

A prerequisite edge means the other concept has to be understood before `while_loop`.

### `boolean_expression` comes before `while_loop`

*an expression that evaluates to true/false*

- **Edge:** `pre:boolean_expression->while_loop`
- **Exact edge logic:** A while tests its boolean condition before every pass and stops the first time it evaluates to false.
- **Grounding:** book\_passage
- **Composition rule (R) of `while_loop` with `boolean_expression`:** The loop condition is a boolean expression evaluated before every pass; the loop stops the first time it is false, so the body must eventually make it false.
- **Composition rule (R) of `boolean_expression` with `while_loop`:** The while loop re-evaluates its boolean expression before every pass and stops the first time it is false, so some variable in the expression must change in the body or the loop never ends.

## What it leads to (12)

These concepts need `while_loop` first.

### `while_loop` comes before `animation`

*StdDraw animation: clear, draw, show, pause in a loop*

- **Edge:** `pre:while_loop->animation`
- **Exact edge logic:** BouncingBall repeats erase, draw at the new position, and show with a pause inside a while (true) loop.
- **Grounding:** book\_passage
- **Composition rule (R) of `while_loop` with `animation`:** An animation repeats clear/draw/show/pause steps inside a loop, typically one that runs indefinitely.
- **Composition rule (R) of `animation` with `while_loop`:** The frame loop is while (true): it never ends by its condition, so the animation runs until the window or program is closed.

### `while_loop` comes before `break_statement`

*break -- immediately exits the innermost loop or switch*

- **Edge:** `pre:while_loop->break_statement`
- **Exact edge logic:** break immediately exits a loop without letting it run to completion.
- **Grounding:** book\_passage
- **Composition rule (R) of `while_loop` with `break_statement`:** break exits the loop immediately, so a while loop can end either by a false test or by a break; while (true) needs a break (or is infinite).
- **Composition rule (R) of `break_statement` with `while_loop`:** break gives a while loop a second exit, in the middle of the body. After the loop, the program has to tell which exit was taken by re-testing the state (as in \`if (i &gt; N/i)\`), so any variable used for that test must be declared before the loop.

### `while_loop` comes before `continue_statement`

*continue -- skips to the next iteration of the innermost loop*

- **Edge:** `pre:while_loop->continue_statement`
- **Exact edge logic:** continue ends the current pass of the while loop and goes straight back to the loop test.
- **Grounding:** book\_passage

### `while_loop` comes before `convergence_test`

*stopping a loop when a floating-point result is close enough*

- **Edge:** `pre:while_loop->convergence_test`
- **Exact edge logic:** The convergence test is the condition of a while loop that keeps refining an estimate until the error is below a tolerance.
- **Grounding:** book\_passage
- **Composition rule (R) of `while_loop` with `convergence_test`:** A convergence test is the while condition that keeps refining an estimate until the error is within tolerance, e.g. while (Math.abs(t - c/t) &gt; epsilon \* t).
- **Composition rule (R) of `convergence_test` with `while_loop`:** The convergence test is the while condition, evaluated before every pass. The body must move the estimate closer (t = (c/t + t)/2.0), or the condition stays true and the loop never ends.

### `while_loop` comes before `do_while_loop`

*do { body } while (c); -- body first, test after*

- **Edge:** `pre:while_loop->do_while_loop`
- **Exact edge logic:** do { body } while (c); is a while loop whose test is moved to the bottom.
- **Grounding:** book\_passage
- **Composition rule (R) of `while_loop` with `do_while_loop`:** do { body } while (c); means the same as while (c) { body } except that the first test is omitted, so the body runs at least once.
- **Composition rule (R) of `do_while_loop` with `while_loop`:** do { S } while (c); equals \`S; while (c) { S }\`. If c is initially true it behaves exactly like \`while (c) { S }\`; if c is initially false it still runs S once where the while runs it zero times.

### `while_loop` comes before `infinite_loop`

*a loop whose condition never becomes false*

- **Edge:** `pre:while_loop->infinite_loop`
- **Exact edge logic:** A while loop whose condition never becomes false never ends.
- **Grounding:** book\_passage

### `while_loop` comes before `loop_body`

*the block repeated each pass*

- **Edge:** `pre:while_loop->loop_body`
- **Exact edge logic:** The loop body is the block of statements that a while (or for) loop repeats on each pass.
- **Grounding:** book\_passage
- **Composition rule (R) of `while_loop` with `loop_body`:** The body is the block that the while repeats; it runs only after a true test and is completed before the next test.
- **Composition rule (R) of `loop_body` with `while_loop`:** The body is what the while repeats; the condition is tested only between complete executions of it.

### `while_loop` comes before `loop_control`

*the three slots: init ; condition ; update*

- **Edge:** `pre:while_loop->loop_control`
- **Exact edge logic:** A while loop has the same three control parts as a for loop, written in other places: the index set before the loop, the loop-continuation condition in the header, and the update as the last statement of the body.
- **Grounding:** book\_passage

### `while_loop` comes before `loop_invariant_reasoning`

*Reasoning about loops: convincing yourself a loop is correct by stating facts that hold each time through it and why it terminates*

- **Edge:** `pre:while_loop->loop_invariant_reasoning`
- **Exact edge logic:** To reason about a while loop you state what stays true on every pass and why the condition eventually becomes false.
- **Grounding:** book\_passage
- **Composition rule (R) of `while_loop` with `loop_invariant_reasoning`:** To trust a while loop, state what stays true on every pass and why the condition eventually becomes false (e.g. v is always a power of 2, v increases, so the loop terminates).
- **Composition rule (R) of `loop_invariant_reasoning` with `while_loop`:** The invariant is stated at the while test. The while condition supplies the extra fact available inside the body (v ≤ N/2, so 2v ≤ N), and its negation supplies the extra fact after the loop (2v &gt; N).

### `while_loop` comes before `loop_variable`

*the counter that drives the loop*

- **Edge:** `pre:while_loop->loop_variable`
- **Exact edge logic:** A loop variable is a counter that the loop initializes, tests in its condition and increments on each pass.
- **Grounding:** book\_passage
- **Composition rule (R) of `while_loop` with `loop_variable`:** The while condition usually tests a loop variable that is initialized before the loop and updated in the body; if the body never changes it, the loop never ends.
- **Composition rule (R) of `loop_variable` with `while_loop`:** In a while loop the loop variable is declared and initialized before the loop and updated inside the body, so it remains available after the loop.

### `while_loop` comes before `number_conversion`

*Number conversion (binary): converting an integer to its binary representation by casting out powers of 2 in a loop*

- **Edge:** `pre:while_loop->number_conversion`
- **Exact edge logic:** Binary conversion repeats one step in a while loop: find the largest power of 2 not above n, output a bit and subtract.
- **Grounding:** book\_passage
- **Composition rule (R) of `while_loop` with `number_conversion`:** Binary conversion uses while loops: one to find the largest power of 2 &lt;= N, and one to cast out powers of 2 in decreasing order.
- **Composition rule (R) of `number_conversion` with `while_loop`:** Two while loops in sequence: the first's exit state (v = largest power of 2 ≤ N) is the second's starting state. The second runs once per bit and ends when integer halving takes v from 1 to 0.

### `while_loop` comes before `sentinel_loop`

*reading until a special stop value (Rainfall problem)*

- **Edge:** `pre:while_loop->sentinel_loop`
- **Exact edge logic:** A sentinel loop is a while loop whose condition tests each value read against the stop value.
- **Grounding:** spec\_passage

## Learned alongside (1)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

### `while_loop` alongside `if_statement`

*run a block only when the condition holds*

- **Edge:** `par:if_statement~while_loop`
- **Exact edge logic:** if and while have the same form, but if tests its condition once and runs the block at most once, while while tests again after every pass and repeats the block as long as the condition is true.
- **Grounding:** book\_passage

## Misconceptions (16)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### FalseLoopRepeatsNextCode

- **Edge:** `while_loop` &rarr; `FalseLoopRepeatsNextCode` (misconception)
- **Exact edge logic (the wrong rule):** A loop is an iterative if-else: while the condition is true the body repeats, and when it is false the code after the loop repeats.
- **Twin logic (the right rule):** Only the body is repeated; once the condition is false the code after the loop runs once.
- **Wrong belief (on the node):** A loop is an iterative if-else: while the condition is true the body repeats, and when it is false the code after the loop repeats.
- **Correct rule (on the node):** Only the body is repeated; once the condition is false the code after the loop runs once.
- **Provenance:** published
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [15] misconception, exact rule:** wrong rule: A loop is an iterative if-else: while the condition is true the body repeats, and when it is false the code after the loop repeats. Right rule: Only the body is repeated; once the condition is false the code after the loop runs once.
- **Edge `control_flow` &rarr; `FalseLoopRepeatsNextCode`, exact edge logic:** A loop is an iterative if-else: while the condition is true the body repeats, and when it is false the code after the loop repeats. **Twin logic:** Only the body is repeated; once the condition is false the code after the loop runs once. (role: context)
- **Edge `for_loop` &rarr; `FalseLoopRepeatsNextCode`, exact edge logic:** A loop is an iterative if-else: while the condition is true the body repeats, and when it is false the code after the loop repeats. **Twin logic:** Only the body is repeated; once the condition is false the code after the loop runs once. (role: primary)

### ForWhileNotInterchangeable

- **Edge:** `while_loop` &rarr; `ForWhileNotInterchangeable` (misconception)
- **Exact edge logic (the wrong rule):** Some loops can only be written with for, others only with while.
- **Twin logic (the right rule):** Any for loop can be rewritten as a while loop and vice versa; for just packages init, test and update.
- **Wrong belief (on the node):** Some loops can only be written with for, others only with while.
- **Correct rule (on the node):** Any for loop can be rewritten as a while loop and vice versa; for just packages init, test and update.
- **Provenance:** textbook
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [14] misconception, exact rule:** wrong rule: Some loops can only be written with for, others only with while. Right rule: Any for loop can be rewritten as a while loop and vice versa; for just packages init, test and update.
- **Edge `for_loop` &rarr; `ForWhileNotInterchangeable`, exact edge logic:** Some loops can only be written with for, others only with while. **Twin logic:** Any for loop can be rewritten as a while loop and vice versa; for just packages init, test and update. (role: primary)

### IfIsLoop

- **Edge:** `while_loop` &rarr; `IfIsLoop` (misconception)
- **Exact edge logic (the wrong rule):** A while loop runs its body once when the condition is true, just like an if.
- **Twin logic (the right rule):** A while tests its condition again after every pass and keeps repeating while the condition stays true.
- **Wrong belief (on the node):** an if body repeats while its condition holds
- **Correct rule (on the node):** An if body runs at most once; only a loop repeats its body.
- **Provenance:** published
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [10] misconception, exact rule:** wrong rule: an if body repeats while its condition holds. Right rule: An if body runs at most once; only a loop repeats its body.
- **Edge `if_statement` &rarr; `IfIsLoop`, exact edge logic:** The if body keeps repeating as long as its condition stays true. **Twin logic:** An if body runs at most once; only a loop repeats its body. (role: primary)

### InfiniteLoopUnnoticed

- **Edge:** `while_loop` &rarr; `InfiniteLoopUnnoticed` (misconception)
- **Exact edge logic (the wrong rule):** a condition that never goes false still terminates
- **Twin logic (the right rule):** A while loop stops only when its condition is false at a check, so if no pass changes the variables in the condition, it never stops.
- **Wrong belief (on the node):** a condition that never goes false still terminates
- **Correct rule (on the node):** A while loop stops only when its condition is false at a check, so if no pass changes the variables in the condition, it never stops.
- **Provenance:** published
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [12] misconception, exact rule:** wrong rule: a condition that never goes false still terminates. Right rule: A while loop stops only when its condition is false at a check, so if no pass changes the variables in the condition, it never stops.
- **Edge `infinite_loop` &rarr; `InfiniteLoopUnnoticed`, exact edge logic:** a condition that never goes false still terminates **Twin logic:** A while loop stops only when its condition is false at a check, so if no pass changes the variables in the condition, it never stops. (role: primary)
- **Edge `loop_control` &rarr; `InfiniteLoopUnnoticed`, exact edge logic:** A while loop always stops on its own, even if nothing in its body can make the condition false. **Twin logic:** A while loop stops only when its condition is false at a check, so if no pass changes the variables in the condition, it never stops. (role: context)

### JavaDetectsInfiniteLoops

- **Edge:** `while_loop` &rarr; `JavaDetectsInfiniteLoops` (misconception)
- **Exact edge logic (the wrong rule):** If my loop never ends, the compiler or Java will warn me.
- **Twin logic (the right rule):** Java cannot detect infinite loops in general; you must check that the loop condition eventually becomes false.
- **Wrong belief (on the node):** If my loop never ends, the compiler or Java will warn me.
- **Correct rule (on the node):** Java cannot detect infinite loops in general; you must check that the loop condition eventually becomes false.
- **Provenance:** textbook
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [13] misconception, exact rule:** wrong rule: If my loop never ends, the compiler or Java will warn me. Right rule: Java cannot detect infinite loops in general; you must check that the loop condition eventually becomes false.
- **Edge `infinite_loop` &rarr; `JavaDetectsInfiniteLoops`, exact edge logic:** If my loop never ends, the compiler or Java will warn me. **Twin logic:** Java cannot detect infinite loops in general; you must check that the loop condition eventually becomes false. (role: primary)

### LoopBodyAlwaysOnce

- **Edge:** `while_loop` &rarr; `LoopBodyAlwaysOnce` (misconception)
- **Exact edge logic (the wrong rule):** The loop body always runs at least once, even if the condition is false at the start.
- **Twin logic (the right rule):** A while or for body runs zero times when the condition is false at the start.
- **Wrong belief (on the node):** The loop body always runs at least once, even if the condition is false at the start.
- **Correct rule (on the node):** A while or for body runs zero times when the condition is false at the start.
- **Provenance:** published
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [11] misconception, exact rule:** wrong rule: The loop body always runs at least once, even if the condition is false at the start. Right rule: A while or for body runs zero times when the condition is false at the start.
- **Edge `loop_body` &rarr; `LoopBodyAlwaysOnce`, exact edge logic:** The loop body always runs at least once, even if the condition is false at the start. **Twin logic:** A while or for body runs zero times when the condition is false at the start. (role: context)

### LoopConditionValidatedLater

- **Edge:** `while_loop` &rarr; `LoopConditionValidatedLater` (misconception)
- **Exact edge logic (the wrong rule):** If a loop condition is false at first but would become true later, the loop still runs (it repeats or skips until the condition is true, then runs until it is false).
- **Twin logic (the right rule):** A while loop whose condition is false at the first test runs zero times; nothing later revives it.
- **Wrong belief (on the node):** If a loop condition is false at first but would become true later, the loop still runs (it repeats or skips until the condition is true, then runs until it is false).
- **Correct rule (on the node):** A while loop whose condition is false at the first test runs zero times; nothing later revives it.
- **Provenance:** published
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [7] misconception, exact rule:** wrong rule: If a loop condition is false at first but would become true later, the loop still runs (it repeats or skips until the condition is true, then runs until it is false). Right rule: A while loop whose condition is false at the first test runs zero times; nothing later revives it.
- **Edge `loop_guard` &rarr; `LoopConditionValidatedLater`, exact edge logic:** If a loop condition is false at first but would become true later, the loop still runs (it repeats or skips until the condition is true, then runs until it is false). **Twin logic:** A while loop whose condition is false at the first test runs zero times; nothing later revives it. (role: context)

### LoopCountByIntent

- **Edge:** `while_loop` &rarr; `LoopCountByIntent` (misconception)
- **Exact edge logic (the wrong rule):** How many times a loop runs is decided by what the program is meant to do, so it may go on after its condition is false.
- **Twin logic (the right rule):** The loop runs only while its condition is true when tested; it stops at the first false test.
- **Wrong belief (on the node):** How many times a loop runs is decided by what the program is meant to do, so it may go on after its condition is false.
- **Correct rule (on the node):** The loop runs only while its condition is true when tested; it stops at the first false test.
- **Provenance:** published
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [6] misconception, exact rule:** wrong rule: How many times a loop runs is decided by what the program is meant to do, so it may go on after its condition is false. Right rule: The loop runs only while its condition is true when tested; it stops at the first false test.
- **Edge `loop_guard` &rarr; `LoopCountByIntent`, exact edge logic:** How many times a loop runs is decided by what the program is meant to do, so it may go on after its condition is false. **Twin logic:** The loop runs only while its condition is true when tested; it stops at the first false test. (role: context)

### LoopForOneTimeTest

- **Edge:** `while_loop` &rarr; `LoopForOneTimeTest` (misconception)
- **Exact edge logic (the wrong rule):** Uses a loop where a condition needs to be tested only once.
- **Twin logic (the right rule):** A test made once is an if; a loop repeats.
- **Wrong belief (on the node):** Uses a loop where a condition needs to be tested only once.
- **Correct rule (on the node):** A test made once is an if; a loop repeats.
- **Provenance:** published
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [3] misconception, exact rule:** wrong rule: Uses a loop where a condition needs to be tested only once. Right rule: A test made once is an if; a loop repeats.
- **Edge `boolean_expression` &rarr; `LoopForOneTimeTest`, exact edge logic:** Uses a loop where a condition needs to be tested only once. **Twin logic:** A test made once is an if; a loop repeats. (role: context)
- **Edge `if_statement` &rarr; `LoopForOneTimeTest`, exact edge logic:** Uses a loop where a condition needs to be tested only once. **Twin logic:** A test made once is an if; a loop repeats. (role: context)

### LoopImpliedByOneTest

- **Edge:** `while_loop` &rarr; `LoopImpliedByOneTest` (misconception)
- **Exact edge logic (the wrong rule):** Testing one case is enough; Java will repeat the test for the other values by itself.
- **Twin logic (the right rule):** A statement runs once each time control reaches it; repeating a test for many values needs a loop.
- **Wrong belief (on the node):** Testing one case is enough; Java will repeat the test for the other values by itself.
- **Correct rule (on the node):** A statement runs once each time control reaches it; repeating a test for many values needs a loop.
- **Provenance:** published
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [4] misconception, exact rule:** wrong rule: Testing one case is enough; Java will repeat the test for the other values by itself. Right rule: A statement runs once each time control reaches it; repeating a test for many values needs a loop.
- **Edge `control_flow` &rarr; `LoopImpliedByOneTest`, exact edge logic:** Testing one case is enough; Java will repeat the test for the other values by itself. **Twin logic:** A statement runs once each time control reaches it; repeating a test for many values needs a loop. (role: context)
- **Edge `for_loop` &rarr; `LoopImpliedByOneTest`, exact edge logic:** Testing one case is enough; Java will repeat the test for the other values by itself. **Twin logic:** A statement runs once each time control reaches it; repeating a test for many values needs a loop. (role: context)

### LoopTerminatingCondition

- **Edge:** `while_loop` &rarr; `LoopTerminatingCondition` (misconception)
- **Exact edge logic (the wrong rule):** For and while loops end when the condition becomes true.
- **Twin logic (the right rule):** A for or while loop ends when its condition becomes false.
- **Wrong belief (on the node):** For and while loops end when the condition becomes true.
- **Correct rule (on the node):** A for or while loop ends when its condition becomes false.
- **Provenance:** published
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [1] misconception, exact rule:** wrong rule: For and while loops end when the condition becomes true. Right rule: A for or while loop ends when its condition becomes false.
- **L0 way [9] inconsistent\_trace, exact rule:** Applies the while rule (LT) unevenly: tests the condition before some passes but not others, stops in the middle of a body on one pass, or runs the first pass without testing. (here mixing in: "For and while loops end when the condition becomes true")

### LoopVariableNotUpdated

- **Edge:** `while_loop` &rarr; `LoopVariableNotUpdated` (misconception)
- **Exact edge logic (the wrong rule):** A while loop ends by itself even if nothing in the body changes the variable tested in the condition.
- **Twin logic (the right rule):** If no statement in the body changes a variable in the condition, a condition that was true stays true and the loop never ends.
- **Wrong belief (on the node):** A while loop ends by itself even if nothing in the body changes the variable tested in the condition.
- **Correct rule (on the node):** If no statement in the body changes a variable in the condition, a condition that was true stays true and the loop never ends.
- **Provenance:** published
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [16] misconception, exact rule:** wrong rule: A while loop ends by itself even if nothing in the body changes the variable tested in the condition. Right rule: If no statement in the body changes a variable in the condition, a condition that was true stays true and the loop never ends.
- **Edge `infinite_loop` &rarr; `LoopVariableNotUpdated`, exact edge logic:** A while loop ends by itself even if nothing in the body changes the variable tested in the condition. **Twin logic:** If no statement in the body changes a variable in the condition, a condition that was true stays true and the loop never ends. (role: context)
- **Edge `loop_guard` &rarr; `LoopVariableNotUpdated`, exact edge logic:** A while loop ends by itself even if nothing in the body changes the variable tested in the condition. **Twin logic:** If no statement in the body changes a variable in the condition, a condition that was true stays true and the loop never ends. (role: primary)

### MissingBraces

- **Edge:** `while_loop` &rarr; `MissingBraces` (misconception)
- **Exact edge logic (the wrong rule):** Omits braces around a single-statement body of if, for or while.
- **Twin logic (the right rule):** Braces are optional for a single-statement body, but using them anyway avoids bugs when statements are added later.
- **Wrong belief (on the node):** Omits braces around a single-statement body of if, for or while.
- **Correct rule (on the node):** Braces are optional for a single-statement body, but using them anyway avoids bugs when statements are added later.
- **Provenance:** rule\_dictionary
- **Role of this concept:** context
- **L0 way linked to it:** no
- **Edge `block` &rarr; `MissingBraces`, exact edge logic:** Omits braces around a single-statement body of if, for or while. **Twin logic:** Braces are optional for a single-statement body, but using them anyway avoids bugs when statements are added later. (role: context)
- **Edge `for_loop` &rarr; `MissingBraces`, exact edge logic:** Omits braces around a single-statement body of if, for or while. **Twin logic:** Braces are optional for a single-statement body, but using them anyway avoids bugs when statements are added later. (role: context)
- **Edge `if_statement` &rarr; `MissingBraces`, exact edge logic:** Omits braces around a single-statement body of if, for or while. **Twin logic:** Braces are optional for a single-statement body, but using them anyway avoids bugs when statements are added later. (role: primary)

### ProgramEndsAfterLoop

- **Edge:** `while_loop` &rarr; `ProgramEndsAfterLoop` (misconception)
- **Exact edge logic (the wrong rule):** When a loop finishes the program ends, so code after the loop never runs.
- **Twin logic (the right rule):** When the loop condition becomes false, control continues with the first statement after the loop.
- **Wrong belief (on the node):** When a loop finishes the program ends, so code after the loop never runs.
- **Correct rule (on the node):** When the loop condition becomes false, control continues with the first statement after the loop.
- **Provenance:** published
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [5] misconception, exact rule:** wrong rule: When a loop finishes the program ends, so code after the loop never runs. Right rule: When the loop condition becomes false, control continues with the first statement after the loop.
- **Edge `control_flow` &rarr; `ProgramEndsAfterLoop`, exact edge logic:** When a loop finishes the program ends, so code after the loop never runs. **Twin logic:** When the loop condition becomes false, control continues with the first statement after the loop. (role: context)
- **Edge `for_loop` &rarr; `ProgramEndsAfterLoop`, exact edge logic:** When a loop finishes the program ends, so code after the loop never runs. **Twin logic:** When the loop condition becomes false, control continues with the first statement after the loop. (role: context)

### SingleIterationInsteadOfLoop

- **Edge:** `while_loop` &rarr; `SingleIterationInsteadOfLoop` (misconception)
- **Exact edge logic (the wrong rule):** A task that must be repeated is written once, without a loop, as if one pass were enough.
- **Twin logic (the right rule):** A step that must happen several times (or an unknown number of times) needs a loop such as while or for; code without a loop runs once.
- **Wrong belief (on the node):** A task that must be repeated is written once, without a loop, as if one pass were enough.
- **Correct rule (on the node):** A step that must happen several times (or an unknown number of times) needs a loop such as while or for; code without a loop runs once.
- **Provenance:** published
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [8] misconception, exact rule:** wrong rule: A task that must be repeated is written once, without a loop, as if one pass were enough. Right rule: A step that must happen several times (or an unknown number of times) needs a loop such as while or for; code without a loop runs once.
- **Edge `for_loop` &rarr; `SingleIterationInsteadOfLoop`, exact edge logic:** A task that must be repeated is written once, without a loop, as if one pass were enough. **Twin logic:** A step that must happen several times (or an unknown number of times) needs a loop such as while or for; code without a loop runs once. (role: context)

### WhileStopsMidBody

- **Edge:** `while_loop` &rarr; `WhileStopsMidBody` (misconception)
- **Exact edge logic (the wrong rule):** The loop stops the moment the condition becomes false, even in the middle of the body.
- **Twin logic (the right rule):** The condition is tested only before each pass, so the whole body finishes before the loop can stop.
- **Wrong belief (on the node):** The loop stops the moment the condition becomes false, even in the middle of the body.
- **Correct rule (on the node):** The condition is tested only before each pass, so the whole body finishes before the loop can stop.
- **Provenance:** published
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [2] misconception, exact rule:** wrong rule: The loop stops the moment the condition becomes false, even in the middle of the body. Right rule: The condition is tested only before each pass, so the whole body finishes before the loop can stop.
- **Edge `loop_body` &rarr; `WhileStopsMidBody`, exact edge logic:** The loop stops the moment the condition becomes false, even in the middle of the body. **Twin logic:** The condition is tested only before each pass, so the whole body finishes before the loop can stop. (role: context)

## Errors (3)

An error edge states the rule that gets broken in a program, and the right rule.

### LoopIgnoresCodeBefore

- **Edge:** `while_loop` &rarr; `LoopIgnoresCodeBefore` (error)
- **Exact edge logic (the wrong rule):** Initializes the flag before the loop so that the loop condition is already false, and the loop body never runs.
- **Twin logic (the right rule):** A while loop tests its condition before the first pass: if the values set before the loop make the condition false, the body never runs.
- **Wrong belief (on the node):** Initializes the flag before the loop so that the loop condition is already false, and the loop body never runs.
- **Correct rule (on the node):** A while loop tests its condition before the first pass: if the values set before the loop make the condition false, the body never runs.
- **Provenance:** published
- **Role of this concept:** primary
- **Edge `flag_search_loop` &rarr; `LoopIgnoresCodeBefore`, exact edge logic:** Initializes the flag before the loop so that the loop condition is already false, and the loop body never runs. **Twin logic:** A while loop tests its condition before the first pass: if the values set before the loop make the condition false, the body never runs. (role: context)
- **Edge `logical_error` &rarr; `LoopIgnoresCodeBefore`, exact edge logic:** Initializes the flag before the loop so that the loop condition is already false, and the loop body never runs. **Twin logic:** A while loop tests its condition before the first pass: if the values set before the loop make the condition false, the body never runs. (role: context)

### SemicolonAfterIfHeader

- **Edge:** `while_loop` &rarr; `SemicolonAfterIfHeader` (error)
- **Exact edge logic (the wrong rule):** if (x &gt; 0); System.out.println("positive"); prints only for positive x.
- **Twin logic (the right rule):** The ; ends the if with an empty statement, so the next line always runs.
- **Wrong belief (on the node):** if (x &gt; 0); System.out.println("positive"); prints only for positive x.
- **Correct rule (on the node):** The ; ends the if with an empty statement, so the next line always runs.
- **Provenance:** published
- **Role of this concept:** context
- **Edge `empty_statement` &rarr; `SemicolonAfterIfHeader`, exact edge logic:** if (x &gt; 0); System.out.println("positive"); prints only for positive x. **Twin logic:** The ; ends the if with an empty statement, so the next line always runs. (role: context)
- **Edge `for_loop` &rarr; `SemicolonAfterIfHeader`, exact edge logic:** if (x &gt; 0); System.out.println("positive"); prints only for positive x. **Twin logic:** The ; ends the if with an empty statement, so the next line always runs. (role: context)
- **Edge `if_statement` &rarr; `SemicolonAfterIfHeader`, exact edge logic:** if (x &gt; 0); System.out.println("positive"); prints only for positive x. **Twin logic:** The ; ends the if with an empty statement, so the next line always runs. (role: primary)
- **Edge `logical_error` &rarr; `SemicolonAfterIfHeader`, exact edge logic:** if (x &gt; 0); System.out.println("positive"); prints only for positive x. **Twin logic:** The ; ends the if with an empty statement, so the next line always runs. (role: context)

### SemicolonAfterLoopHeader

- **Edge:** `while_loop` &rarr; `SemicolonAfterLoopHeader` (error)
- **Exact edge logic (the wrong rule):** Puts a ; right after for (...) or while (...).
- **Twin logic (the right rule):** A ; right after the loop header is a null (empty) loop body, so the statements written after it are not repeated by the loop.
- **Wrong belief (on the node):** Puts a ; right after for (...) or while (...).
- **Correct rule (on the node):** A ; right after the loop header is a null (empty) loop body, so the statements written after it are not repeated by the loop.
- **Provenance:** textbook
- **Role of this concept:** context
- **Edge `empty_statement` &rarr; `SemicolonAfterLoopHeader`, exact edge logic:** Puts a ; right after for (...) or while (...). **Twin logic:** A ; right after the loop header is a null (empty) loop body, so the statements written after it are not repeated by the loop. (role: context)
- **Edge `for_loop` &rarr; `SemicolonAfterLoopHeader`, exact edge logic:** Puts a ; right after for (...) or while (...). **Twin logic:** A ; right after the loop header is a null (empty) loop body, so the statements written after it are not repeated by the loop. (role: primary)

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for while loop: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to while loop agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

- **Edge:** `while_loop` &rarr; `while_loop@L0` (has_level)
- **Exact edge logic:** while loop -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (17 ways).

Ways (17), each with its exact rule:

- **[0] everyday\_reading** (rule type E, folk-meaning rule): Folk meaning: English 'while' means 'during the time that', so the activity stops the instant the condition stops holding (the 'while demon'). A Java while tests its condition only before each pass; a pass that has started always finishes.
- **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `LoopTerminatingCondition`: wrong rule: For and while loops end when the condition becomes true. Right rule: A for or while loop ends when its condition becomes false.
- **[2] misconception** (rule type M, wrong rule / right rule) &rarr; `WhileStopsMidBody`: wrong rule: The loop stops the moment the condition becomes false, even in the middle of the body. Right rule: The condition is tested only before each pass, so the whole body finishes before the loop can stop.
- **[3] misconception** (rule type M, wrong rule / right rule) &rarr; `LoopForOneTimeTest`: wrong rule: Uses a loop where a condition needs to be tested only once. Right rule: A test made once is an if; a loop repeats.
- **[4] misconception** (rule type M, wrong rule / right rule) &rarr; `LoopImpliedByOneTest`: wrong rule: Testing one case is enough; Java will repeat the test for the other values by itself. Right rule: A statement runs once each time control reaches it; repeating a test for many values needs a loop.
- **[5] misconception** (rule type M, wrong rule / right rule) &rarr; `ProgramEndsAfterLoop`: wrong rule: When a loop finishes the program ends, so code after the loop never runs. Right rule: When the loop condition becomes false, control continues with the first statement after the loop.
- **[6] misconception** (rule type M, wrong rule / right rule) &rarr; `LoopCountByIntent`: wrong rule: How many times a loop runs is decided by what the program is meant to do, so it may go on after its condition is false. Right rule: The loop runs only while its condition is true when tested; it stops at the first false test.
- **[7] misconception** (rule type M, wrong rule / right rule) &rarr; `LoopConditionValidatedLater`: wrong rule: If a loop condition is false at first but would become true later, the loop still runs (it repeats or skips until the condition is true, then runs until it is false). Right rule: A while loop whose condition is false at the first test runs zero times; nothing later revives it.
- **[8] misconception** (rule type M, wrong rule / right rule) &rarr; `SingleIterationInsteadOfLoop`: wrong rule: A task that must be repeated is written once, without a loop, as if one pass were enough. Right rule: A step that must happen several times (or an unknown number of times) needs a loop such as while or for; code without a loop runs once.
- **[9] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `LoopTerminatingCondition`: Applies the while rule (LT) unevenly: tests the condition before some passes but not others, stops in the middle of a body on one pass, or runs the first pass without testing. (here mixing in: "For and while loops end when the condition becomes true")
- **[10] misconception** (rule type M, wrong rule / right rule) &rarr; `IfIsLoop`: wrong rule: an if body repeats while its condition holds. Right rule: An if body runs at most once; only a loop repeats its body.
- **[11] misconception** (rule type M, wrong rule / right rule) &rarr; `LoopBodyAlwaysOnce`: wrong rule: The loop body always runs at least once, even if the condition is false at the start. Right rule: A while or for body runs zero times when the condition is false at the start.
- **[12] misconception** (rule type M, wrong rule / right rule) &rarr; `InfiniteLoopUnnoticed`: wrong rule: a condition that never goes false still terminates. Right rule: A while loop stops only when its condition is false at a check, so if no pass changes the variables in the condition, it never stops.
- **[13] misconception** (rule type M, wrong rule / right rule) &rarr; `JavaDetectsInfiniteLoops`: wrong rule: If my loop never ends, the compiler or Java will warn me. Right rule: Java cannot detect infinite loops in general; you must check that the loop condition eventually becomes false.
- **[14] misconception** (rule type M, wrong rule / right rule) &rarr; `ForWhileNotInterchangeable`: wrong rule: Some loops can only be written with for, others only with while. Right rule: Any for loop can be rewritten as a while loop and vice versa; for just packages init, test and update.
- **[15] misconception** (rule type M, wrong rule / right rule) &rarr; `FalseLoopRepeatsNextCode`: wrong rule: A loop is an iterative if-else: while the condition is true the body repeats, and when it is false the code after the loop repeats. Right rule: Only the body is repeated; once the condition is false the code after the loop runs once.
- **[16] misconception** (rule type M, wrong rule / right rule) &rarr; `LoopVariableNotUpdated`: wrong rule: A while loop ends by itself even if nothing in the body changes the variable tested in the condition. Right rule: If no statement in the body changes a variable in the condition, a condition that was true stays true and the loop never ends.

### L1: Unistructural / atom x text surface

L1 for while loop: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

- **Edge:** `while_loop` &rarr; `while_loop@L1` (has_level)
- **Exact edge logic:** while loop -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

Ways (2), each with its exact rule:

- **[0] names\_the\_element** (rule type N, identity rule): The while statement is a loop (iteration statement): it repeats a body as long as a boolean condition is true.
- **[1] states\_the\_rule** (rule type S, declarative rule): Syntax: while (&lt;boolean expression&gt;) { &lt;statements&gt; } (braces optional for one statement). Meaning: if the expression is false do nothing; if true, execute the body, then check the expression again, and continue as long as it is true.

### L2: Multistructural / block x execution / preoperational

L2 for while loop: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

- **Edge:** `while_loop` &rarr; `while_loop@L2` (has_level)
- **Exact edge logic:** while loop -&gt; L2 (Multistructural): the answer applies the rules of while loop to every part of the code, in order (3 ways).

Ways (3), each with its exact rule:

- **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): 1. Evaluate the condition. 2. If false, skip the body and continue after the loop. 3. If true, execute the whole body, then go back to step 1.
- **[1] output\_prediction** (rule type OP, evaluation / result rule): A while statement has no value; its result is the state and output after the passes it made: e.g. TenHellos with i = 4 and i &lt;= 10 prints 4th to 10th Hello (7 passes) and leaves i = 11.
- **[2] one\_step\_execution** (rule type OS, state-transition rule): One pass: test the condition with the current values, then (if true) apply every body statement once in order; the variables assigned in the body change and nothing else; a false test ends the loop with the state unchanged.

### L3: Relational / relations x function (concrete operational begins)

L3 for while loop: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

- **Edge:** `while_loop` &rarr; `while_loop@L3` (has_level)
- **Exact edge logic:** while loop -&gt; L3 (Relational): the answer relates the parts (11 ways).

Ways (11), each with its exact rule:

- **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): The loop condition is a boolean expression evaluated before every pass; the loop stops the first time it is false, so the body must eventually make it false.
- **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): do { body } while (c); means the same as while (c) { body } except that the first test is omitted, so the body runs at least once.
- **[2] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): break exits the loop immediately, so a while loop can end either by a false test or by a break; while (true) needs a break (or is infinite).
- **[3] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): An animation repeats clear/draw/show/pause steps inside a loop, typically one that runs indefinitely.
- **[4] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): A convergence test is the while condition that keeps refining an estimate until the error is within tolerance, e.g. while (Math.abs(t - c/t) &gt; epsilon \* t).
- **[5] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): The body is the block that the while repeats; it runs only after a true test and is completed before the next test.
- **[6] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): The while condition usually tests a loop variable that is initialized before the loop and updated in the body; if the body never changes it, the loop never ends.
- **[7] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): To trust a while loop, state what stays true on every pass and why the condition eventually becomes false (e.g. v is always a power of 2, v increases, so the loop terminates).
- **[8] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Binary conversion uses while loops: one to find the largest power of 2 &lt;= N, and one to cast out powers of 2 in decreasing order.
- **[9] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): if and while have the same form, but if tests its condition once and runs the block at most once, while while tests again after every pass and repeats the block as long as the condition is true.
- **[10] purpose\_of\_the\_whole** (rule type P, plan / role rule): Plan: indefinite (event-controlled) repetition - repeat until something happens whose number of passes is not known in advance (until convergence, until broke or goal); the condition variable is often a stepper or most-recent holder.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for while loop: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

- **Edge:** `while_loop` &rarr; `while_loop@L4` (has_level)
- **Exact edge logic:** while loop -&gt; L4 (Extended abstract): the answer reasons beyond the given code (6 ways).

Ways (6), each with its exact rule:

- **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `LoopTerminatingCondition`: Changing &lt; to &lt;= adds exactly one pass at the boundary; removing the update from the body makes a loop that was entered never end; a condition that is false initially gives zero passes whatever the body does. Rewriting as for (init; cond; update) preserves behaviour if no continue is involved.
- **[1] diagnose\_an\_error** (rule type D, error rule): rule broken: A while loop tests its condition before the first pass, using the values set before the loop. Kind: silent logic error. Trigger class: Initializations before the loop that already make the condition false (e.g. boolean done = true; while (!done) ...): the body runs zero times and no error is reported.
- **[2] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Use while when the number of passes depends on what happens during the loop (convergence, input, simulation) or the loop variable is needed after the loop; use for for counted loops, do-while when the body must run at least once, and if when the test is needed only once.
- **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: A ; right after if (...) is an empty statement that forms the whole then branch; the following statement or block is no longer part of the if. Kind: silent logic error. Trigger class: Any if (cond); followed by a statement or block: that statement runs for every input, whatever cond is (it compiles without error).
- **[4] diagnose\_an\_error** (rule type D, error rule): rule broken: A ; right after while (...) or for (...) is an empty statement that is the whole loop body; the block written next is not repeated. Kind: silent logic error. Trigger class: for (...); { body } runs the body once after the loop ends; while (cond); with a cond that the empty body cannot change hangs forever (infinite loop) when cond starts true.
- **[5] diagnose\_an\_error** (rule type D, error rule): rule broken: The body must eventually make the condition false. Kind: silent logic error. Trigger class: No body statement changes a variable in the condition, or the update moves away from the bound (e.g. while (i &gt; 3) i = i + 1;): infinite loop, endless output or a hang; Java cannot detect it in general.

## Same topic

`while_loop` belongs to the topic **While loops** (`topic1.3.c`). The topic also contains: `loop_body`, `loop_control`, `loop_invariant_reasoning`.

## Rules of the concept (38)

- **Book** (SW-1e, p. 49 (pdf 59)): "The while statement has the same form as the if statement (the only difference being the use of the keyword while instead of if), but the meaning is quite different."
- **Book** (OT-While, ): "The while statement continues testing the expression and executing its block until the expression evaluates to false."
- **Book** (SW-1.3, ): "The while loop enables us to execute a group of statements many times."
- **E** (folk-meaning rule): Folk meaning: English 'while' means 'during the time that', so the activity stops the instant the condition stops holding (the 'while demon'). A Java while tests its condition only before each pass; a pass that has started always finishes.
- **M** (wrong rule / right rule): IfIsLoop: wrong: an if body repeats while its condition holds \| right: An if body runs at most once; only a loop repeats its body.
- **M** (wrong rule / right rule): LoopBodyAlwaysOnce: wrong: The loop body always runs at least once, even if the condition is false at the start. \| right: A while or for body runs zero times when the condition is false at the start.
- **M** (wrong rule / right rule): LoopForOneTimeTest: wrong: Uses a loop where a condition needs to be tested only once. \| right: A test made once is an if; a loop repeats.
- **M** (wrong rule / right rule): LoopTerminatingCondition: wrong: For and while loops end when the condition becomes true. \| right: A for or while loop ends when its condition becomes false.
- **M** (wrong rule / right rule): WhileStopsMidBody: wrong: The loop stops the moment the condition becomes false, even in the middle of the body. \| right: The condition is tested only before each pass, so the whole body finishes before the loop can stop.
- **M** (wrong rule / right rule): InfiniteLoopUnnoticed: wrong: a condition that never goes false still terminates \| right: A while loop stops only when its condition is false at a check, so if no pass changes the variables in the condition, it never stops.
- **M** (wrong rule / right rule): JavaDetectsInfiniteLoops: wrong: If my loop never ends, the compiler or Java will warn me. \| right: Java cannot detect infinite loops in general; you must check that the loop condition eventually becomes false.
- **M** (wrong rule / right rule): ForWhileNotInterchangeable: wrong: Some loops can only be written with for, others only with while. \| right: Any for loop can be rewritten as a while loop and vice versa; for just packages init, test and update.
- **M** (wrong rule / right rule): LoopImpliedByOneTest: wrong: Testing one case is enough; Java will repeat the test for the other values by itself. \| right: A statement runs once each time control reaches it; repeating a test for many values needs a loop.
- **M** (wrong rule / right rule): ProgramEndsAfterLoop: wrong: When a loop finishes the program ends, so code after the loop never runs. \| right: When the loop condition becomes false, control continues with the first statement after the loop.
- **M** (wrong rule / right rule): FalseLoopRepeatsNextCode: wrong: A loop is an iterative if-else: while the condition is true the body repeats, and when it is false the code after the loop repeats. \| right: Only the body is repeated; once the condition is false the code after the loop runs once.
- **M** (wrong rule / right rule): LoopCountByIntent: wrong: How many times a loop runs is decided by what the program is meant to do, so it may go on after its condition is false. \| right: The loop runs only while its condition is true when tested; it stops at the first false test.
- **M** (wrong rule / right rule): LoopConditionValidatedLater: wrong: If a loop condition is false at first but would become true later, the loop still runs (it repeats or skips until the condition is true, then runs until it is false). \| right: A while loop whose condition is false at the first test runs zero times; nothing later revives it.
- **M** (wrong rule / right rule): LoopVariableNotUpdated: wrong: A while loop ends by itself even if nothing in the body changes the variable tested in the condition. \| right: If no statement in the body changes a variable in the condition, a condition that was true stays true and the loop never ends.
- **M** (wrong rule / right rule): SingleIterationInsteadOfLoop: wrong: A task that must be repeated is written once, without a loop, as if one pass were enough. \| right: A step that must happen several times (or an unknown number of times) needs a loop such as while or for; code without a loop runs once.
- **T** (uneven-application rule): Applies the while rule (LT) unevenly: tests the condition before some passes but not others, stops in the middle of a body on one pass, or runs the first pass without testing.
- **N** (identity rule): The while statement is a loop (iteration statement): it repeats a body as long as a boolean condition is true.
- **S** (declarative rule): Syntax: while (&lt;boolean expression&gt;) { &lt;statements&gt; } (braces optional for one statement). Meaning: if the expression is false do nothing; if true, execute the body, then check the expression again, and continue as long as it is true.
- **LT** (operational sequencing rule): 1. Evaluate the condition. 2. If false, skip the body and continue after the loop. 3. If true, execute the whole body, then go back to step 1.
- **OP** (evaluation / result rule): A while statement has no value; its result is the state and output after the passes it made: e.g. TenHellos with i = 4 and i &lt;= 10 prints 4th to 10th Hello (7 passes) and leaves i = 11.
- **OS** (state-transition rule): One pass: test the condition with the current values, then (if true) apply every body statement once in order; the variables assigned in the body change and nothing else; a false test ends the loop with the state unchanged.
- **R** (composition rule (with a neighbour)): with boolean\_expression: The loop condition is a boolean expression evaluated before every pass; the loop stops the first time it is false, so the body must eventually make it false.
- **R** (composition rule (with a neighbour)): with do\_while\_loop: do { body } while (c); means the same as while (c) { body } except that the first test is omitted, so the body runs at least once.
- **R** (composition rule (with a neighbour)): with break\_statement: break exits the loop immediately, so a while loop can end either by a false test or by a break; while (true) needs a break (or is infinite).
- **R** (composition rule (with a neighbour)): with animation: An animation repeats clear/draw/show/pause steps inside a loop, typically one that runs indefinitely.
- **R** (composition rule (with a neighbour)): with convergence\_test: A convergence test is the while condition that keeps refining an estimate until the error is within tolerance, e.g. while (Math.abs(t - c/t) &gt; epsilon \* t).
- **R** (composition rule (with a neighbour)): with loop\_body: The body is the block that the while repeats; it runs only after a true test and is completed before the next test.
- **R** (composition rule (with a neighbour)): with loop\_variable: The while condition usually tests a loop variable that is initialized before the loop and updated in the body; if the body never changes it, the loop never ends.
- **R** (composition rule (with a neighbour)): with loop\_invariant\_reasoning: To trust a while loop, state what stays true on every pass and why the condition eventually becomes false (e.g. v is always a power of 2, v increases, so the loop terminates).
- **R** (composition rule (with a neighbour)): with number\_conversion: Binary conversion uses while loops: one to find the largest power of 2 &lt;= N, and one to cast out powers of 2 in decreasing order.
- **P** (plan / role rule): Plan: indefinite (event-controlled) repetition - repeat until something happens whose number of passes is not known in advance (until convergence, until broke or goal); the condition variable is often a stepper or most-recent holder.
- **C** (conservation rule): Changing &lt; to &lt;= adds exactly one pass at the boundary; removing the update from the body makes a loop that was entered never end; a condition that is false initially gives zero passes whatever the body does. Rewriting as for (init; cond; update) preserves behaviour if no continue is involved.
- **D** (error rule): rule broken: A ; right after if (...) is an empty statement that forms the whole then branch; the following statement or block is no longer part of the if. (silent logic error)
- **D** (error rule): rule broken: A ; right after while (...) or for (...) is an empty statement that is the whole loop body; the block written next is not repeated. (silent logic error)
- **D** (error rule): rule broken: A while loop tests its condition before the first pass, using the values set before the loop. (silent logic error)
- **D** (error rule): rule broken: The body must eventually make the condition false. (silent logic error)
- **X** (applicability rule): Use while when the number of passes depends on what happens during the loop (convergence, input, simulation) or the loop variable is needed after the loop; use for for counted loops, do-while when the body must run at least once, and if when the test is needed only once.

## How it is found in code and answers (reader block)

- **Aliases:** while loop, while condition
- **Code patterns:** `(?:^|[;{)])[ \t]*while\s*\((?![^)\n]*\)\s*;)`
- **Operator symbols:** none
- **Java types:** none

## The whole prerequisite chain

- **Everything it builds on (11):** `arithmetic_operators`, `boolean`, `boolean_expression`, `comparison_operators`, `data_type`, `expression`, `identifier`, `literal`, `logical_operators`, `primitive_type`, `variable`
- **Everything that builds on it (42):** `accumulator_pattern`, `animation`, `array_copy`, `array_reversal`, `array_traversal`, `boolean_flag_array`, `break_statement`, `continue_statement`, `convergence_rate`, `convergence_test`, `counter_pattern`, `do_while_loop`, `enhanced_for`, `fencepost_loop`, `flag_search_loop`, `for_loop`, `frequency_counting`, `function_plotting`, `increment_operators`, `infinite_loop`, `labeled_break`, `loop_body`, `loop_control`, `loop_invariant_reasoning`, `loop_performance`, `loop_scope`, `loop_variable`, `matrix_operations`, `monte_carlo_simulation`, `mouse_interaction`, `nested_loops`, `number_conversion`, `off_by_one_error`, `power_method`, `row_major_order`, `running_extreme`, `sentinel_loop`, `side_effect_order`, `simulation_loop`, `standard_audio`, `switch_statement`, `two_models`

## Every edge in this view and its exact edge logic (73)

All the edges drawn in the picture, in the order: prerequisite, parallel, misconception, error, has_level, contains.

**1. `boolean_expression` &rarr; `while_loop`** (prerequisite)

- **Exact edge logic:** A while tests its boolean condition before every pass and stops the first time it evaluates to false.
- **Grounding:** book\_passage
- **Composition rule (R) of `boolean_expression` with `while_loop`:** The while loop re-evaluates its boolean expression before every pass and stops the first time it is false, so some variable in the expression must change in the body or the loop never ends.
- **Composition rule (R) of `while_loop` with `boolean_expression`:** The loop condition is a boolean expression evaluated before every pass; the loop stops the first time it is false, so the body must eventually make it false.

**2. `while_loop` &rarr; `animation`** (prerequisite)

- **Exact edge logic:** BouncingBall repeats erase, draw at the new position, and show with a pause inside a while (true) loop.
- **Grounding:** book\_passage
- **Composition rule (R) of `while_loop` with `animation`:** An animation repeats clear/draw/show/pause steps inside a loop, typically one that runs indefinitely.
- **Composition rule (R) of `animation` with `while_loop`:** The frame loop is while (true): it never ends by its condition, so the animation runs until the window or program is closed.

**3. `while_loop` &rarr; `break_statement`** (prerequisite)

- **Exact edge logic:** break immediately exits a loop without letting it run to completion.
- **Grounding:** book\_passage
- **Composition rule (R) of `while_loop` with `break_statement`:** break exits the loop immediately, so a while loop can end either by a false test or by a break; while (true) needs a break (or is infinite).
- **Composition rule (R) of `break_statement` with `while_loop`:** break gives a while loop a second exit, in the middle of the body. After the loop, the program has to tell which exit was taken by re-testing the state (as in \`if (i &gt; N/i)\`), so any variable used for that test must be declared before the loop.

**4. `while_loop` &rarr; `continue_statement`** (prerequisite)

- **Exact edge logic:** continue ends the current pass of the while loop and goes straight back to the loop test.
- **Grounding:** book\_passage

**5. `while_loop` &rarr; `convergence_test`** (prerequisite)

- **Exact edge logic:** The convergence test is the condition of a while loop that keeps refining an estimate until the error is below a tolerance.
- **Grounding:** book\_passage
- **Composition rule (R) of `while_loop` with `convergence_test`:** A convergence test is the while condition that keeps refining an estimate until the error is within tolerance, e.g. while (Math.abs(t - c/t) &gt; epsilon \* t).
- **Composition rule (R) of `convergence_test` with `while_loop`:** The convergence test is the while condition, evaluated before every pass. The body must move the estimate closer (t = (c/t + t)/2.0), or the condition stays true and the loop never ends.

**6. `while_loop` &rarr; `do_while_loop`** (prerequisite)

- **Exact edge logic:** do { body } while (c); is a while loop whose test is moved to the bottom.
- **Grounding:** book\_passage
- **Composition rule (R) of `while_loop` with `do_while_loop`:** do { body } while (c); means the same as while (c) { body } except that the first test is omitted, so the body runs at least once.
- **Composition rule (R) of `do_while_loop` with `while_loop`:** do { S } while (c); equals \`S; while (c) { S }\`. If c is initially true it behaves exactly like \`while (c) { S }\`; if c is initially false it still runs S once where the while runs it zero times.

**7. `while_loop` &rarr; `infinite_loop`** (prerequisite)

- **Exact edge logic:** A while loop whose condition never becomes false never ends.
- **Grounding:** book\_passage

**8. `while_loop` &rarr; `loop_body`** (prerequisite)

- **Exact edge logic:** The loop body is the block of statements that a while (or for) loop repeats on each pass.
- **Grounding:** book\_passage
- **Composition rule (R) of `while_loop` with `loop_body`:** The body is the block that the while repeats; it runs only after a true test and is completed before the next test.
- **Composition rule (R) of `loop_body` with `while_loop`:** The body is what the while repeats; the condition is tested only between complete executions of it.

**9. `while_loop` &rarr; `loop_control`** (prerequisite)

- **Exact edge logic:** A while loop has the same three control parts as a for loop, written in other places: the index set before the loop, the loop-continuation condition in the header, and the update as the last statement of the body.
- **Grounding:** book\_passage

**10. `while_loop` &rarr; `loop_invariant_reasoning`** (prerequisite)

- **Exact edge logic:** To reason about a while loop you state what stays true on every pass and why the condition eventually becomes false.
- **Grounding:** book\_passage
- **Composition rule (R) of `while_loop` with `loop_invariant_reasoning`:** To trust a while loop, state what stays true on every pass and why the condition eventually becomes false (e.g. v is always a power of 2, v increases, so the loop terminates).
- **Composition rule (R) of `loop_invariant_reasoning` with `while_loop`:** The invariant is stated at the while test. The while condition supplies the extra fact available inside the body (v ≤ N/2, so 2v ≤ N), and its negation supplies the extra fact after the loop (2v &gt; N).

**11. `while_loop` &rarr; `loop_variable`** (prerequisite)

- **Exact edge logic:** A loop variable is a counter that the loop initializes, tests in its condition and increments on each pass.
- **Grounding:** book\_passage
- **Composition rule (R) of `while_loop` with `loop_variable`:** The while condition usually tests a loop variable that is initialized before the loop and updated in the body; if the body never changes it, the loop never ends.
- **Composition rule (R) of `loop_variable` with `while_loop`:** In a while loop the loop variable is declared and initialized before the loop and updated inside the body, so it remains available after the loop.

**12. `while_loop` &rarr; `number_conversion`** (prerequisite)

- **Exact edge logic:** Binary conversion repeats one step in a while loop: find the largest power of 2 not above n, output a bit and subtract.
- **Grounding:** book\_passage
- **Composition rule (R) of `while_loop` with `number_conversion`:** Binary conversion uses while loops: one to find the largest power of 2 &lt;= N, and one to cast out powers of 2 in decreasing order.
- **Composition rule (R) of `number_conversion` with `while_loop`:** Two while loops in sequence: the first's exit state (v = largest power of 2 ≤ N) is the second's starting state. The second runs once per bit and ends when integer halving takes v from 1 to 0.

**13. `while_loop` &rarr; `sentinel_loop`** (prerequisite)

- **Exact edge logic:** A sentinel loop is a while loop whose condition tests each value read against the stop value.
- **Grounding:** spec\_passage

**14. `if_statement` &harr; `while_loop`** (parallel)

- **Exact edge logic:** if and while have the same form, but if tests its condition once and runs the block at most once, while while tests again after every pass and repeats the block as long as the condition is true.
- **Grounding:** book\_passage

**15. `while_loop` &rarr; `FalseLoopRepeatsNextCode`** (misconception)

- **Exact edge logic (the wrong rule):** A loop is an iterative if-else: while the condition is true the body repeats, and when it is false the code after the loop repeats.
- **Twin logic (the right rule):** Only the body is repeated; once the condition is false the code after the loop runs once.
- **Role:** context

**16. `while_loop` &rarr; `ForWhileNotInterchangeable`** (misconception)

- **Exact edge logic (the wrong rule):** Some loops can only be written with for, others only with while.
- **Twin logic (the right rule):** Any for loop can be rewritten as a while loop and vice versa; for just packages init, test and update.
- **Role:** context

**17. `while_loop` &rarr; `IfIsLoop`** (misconception)

- **Exact edge logic (the wrong rule):** A while loop runs its body once when the condition is true, just like an if.
- **Twin logic (the right rule):** A while tests its condition again after every pass and keeps repeating while the condition stays true.
- **Role:** context

**18. `while_loop` &rarr; `InfiniteLoopUnnoticed`** (misconception)

- **Exact edge logic (the wrong rule):** a condition that never goes false still terminates
- **Twin logic (the right rule):** A while loop stops only when its condition is false at a check, so if no pass changes the variables in the condition, it never stops.
- **Role:** context

**19. `while_loop` &rarr; `JavaDetectsInfiniteLoops`** (misconception)

- **Exact edge logic (the wrong rule):** If my loop never ends, the compiler or Java will warn me.
- **Twin logic (the right rule):** Java cannot detect infinite loops in general; you must check that the loop condition eventually becomes false.
- **Role:** context

**20. `while_loop` &rarr; `LoopBodyAlwaysOnce`** (misconception)

- **Exact edge logic (the wrong rule):** The loop body always runs at least once, even if the condition is false at the start.
- **Twin logic (the right rule):** A while or for body runs zero times when the condition is false at the start.
- **Role:** primary

**21. `while_loop` &rarr; `LoopConditionValidatedLater`** (misconception)

- **Exact edge logic (the wrong rule):** If a loop condition is false at first but would become true later, the loop still runs (it repeats or skips until the condition is true, then runs until it is false).
- **Twin logic (the right rule):** A while loop whose condition is false at the first test runs zero times; nothing later revives it.
- **Role:** primary

**22. `while_loop` &rarr; `LoopCountByIntent`** (misconception)

- **Exact edge logic (the wrong rule):** How many times a loop runs is decided by what the program is meant to do, so it may go on after its condition is false.
- **Twin logic (the right rule):** The loop runs only while its condition is true when tested; it stops at the first false test.
- **Role:** primary

**23. `while_loop` &rarr; `LoopForOneTimeTest`** (misconception)

- **Exact edge logic (the wrong rule):** Uses a loop where a condition needs to be tested only once.
- **Twin logic (the right rule):** A test made once is an if; a loop repeats.
- **Role:** primary

**24. `while_loop` &rarr; `LoopImpliedByOneTest`** (misconception)

- **Exact edge logic (the wrong rule):** Testing one case is enough; Java will repeat the test for the other values by itself.
- **Twin logic (the right rule):** A statement runs once each time control reaches it; repeating a test for many values needs a loop.
- **Role:** primary

**25. `while_loop` &rarr; `LoopTerminatingCondition`** (misconception)

- **Exact edge logic (the wrong rule):** For and while loops end when the condition becomes true.
- **Twin logic (the right rule):** A for or while loop ends when its condition becomes false.
- **Role:** primary

**26. `while_loop` &rarr; `LoopVariableNotUpdated`** (misconception)

- **Exact edge logic (the wrong rule):** A while loop ends by itself even if nothing in the body changes the variable tested in the condition.
- **Twin logic (the right rule):** If no statement in the body changes a variable in the condition, a condition that was true stays true and the loop never ends.
- **Role:** context

**27. `while_loop` &rarr; `MissingBraces`** (misconception)

- **Exact edge logic (the wrong rule):** Omits braces around a single-statement body of if, for or while.
- **Twin logic (the right rule):** Braces are optional for a single-statement body, but using them anyway avoids bugs when statements are added later.
- **Role:** context

**28. `while_loop` &rarr; `ProgramEndsAfterLoop`** (misconception)

- **Exact edge logic (the wrong rule):** When a loop finishes the program ends, so code after the loop never runs.
- **Twin logic (the right rule):** When the loop condition becomes false, control continues with the first statement after the loop.
- **Role:** primary

**29. `while_loop` &rarr; `SingleIterationInsteadOfLoop`** (misconception)

- **Exact edge logic (the wrong rule):** A task that must be repeated is written once, without a loop, as if one pass were enough.
- **Twin logic (the right rule):** A step that must happen several times (or an unknown number of times) needs a loop such as while or for; code without a loop runs once.
- **Role:** primary

**30. `while_loop` &rarr; `WhileStopsMidBody`** (misconception)

- **Exact edge logic (the wrong rule):** The loop stops the moment the condition becomes false, even in the middle of the body.
- **Twin logic (the right rule):** The condition is tested only before each pass, so the whole body finishes before the loop can stop.
- **Role:** primary

**31. `block` &rarr; `MissingBraces`** (misconception)

- **Exact edge logic (the wrong rule):** Omits braces around a single-statement body of if, for or while.
- **Twin logic (the right rule):** Braces are optional for a single-statement body, but using them anyway avoids bugs when statements are added later.
- **Role:** context

**32. `boolean_expression` &rarr; `LoopForOneTimeTest`** (misconception)

- **Exact edge logic (the wrong rule):** Uses a loop where a condition needs to be tested only once.
- **Twin logic (the right rule):** A test made once is an if; a loop repeats.
- **Role:** context

**33. `control_flow` &rarr; `FalseLoopRepeatsNextCode`** (misconception)

- **Exact edge logic (the wrong rule):** A loop is an iterative if-else: while the condition is true the body repeats, and when it is false the code after the loop repeats.
- **Twin logic (the right rule):** Only the body is repeated; once the condition is false the code after the loop runs once.
- **Role:** context

**34. `control_flow` &rarr; `LoopImpliedByOneTest`** (misconception)

- **Exact edge logic (the wrong rule):** Testing one case is enough; Java will repeat the test for the other values by itself.
- **Twin logic (the right rule):** A statement runs once each time control reaches it; repeating a test for many values needs a loop.
- **Role:** context

**35. `control_flow` &rarr; `ProgramEndsAfterLoop`** (misconception)

- **Exact edge logic (the wrong rule):** When a loop finishes the program ends, so code after the loop never runs.
- **Twin logic (the right rule):** When the loop condition becomes false, control continues with the first statement after the loop.
- **Role:** context

**36. `for_loop` &rarr; `FalseLoopRepeatsNextCode`** (misconception)

- **Exact edge logic (the wrong rule):** A loop is an iterative if-else: while the condition is true the body repeats, and when it is false the code after the loop repeats.
- **Twin logic (the right rule):** Only the body is repeated; once the condition is false the code after the loop runs once.
- **Role:** primary

**37. `for_loop` &rarr; `ForWhileNotInterchangeable`** (misconception)

- **Exact edge logic (the wrong rule):** Some loops can only be written with for, others only with while.
- **Twin logic (the right rule):** Any for loop can be rewritten as a while loop and vice versa; for just packages init, test and update.
- **Role:** primary

**38. `for_loop` &rarr; `LoopImpliedByOneTest`** (misconception)

- **Exact edge logic (the wrong rule):** Testing one case is enough; Java will repeat the test for the other values by itself.
- **Twin logic (the right rule):** A statement runs once each time control reaches it; repeating a test for many values needs a loop.
- **Role:** context

**39. `for_loop` &rarr; `MissingBraces`** (misconception)

- **Exact edge logic (the wrong rule):** Omits braces around a single-statement body of if, for or while.
- **Twin logic (the right rule):** Braces are optional for a single-statement body, but using them anyway avoids bugs when statements are added later.
- **Role:** context

**40. `for_loop` &rarr; `ProgramEndsAfterLoop`** (misconception)

- **Exact edge logic (the wrong rule):** When a loop finishes the program ends, so code after the loop never runs.
- **Twin logic (the right rule):** When the loop condition becomes false, control continues with the first statement after the loop.
- **Role:** context

**41. `for_loop` &rarr; `SingleIterationInsteadOfLoop`** (misconception)

- **Exact edge logic (the wrong rule):** A task that must be repeated is written once, without a loop, as if one pass were enough.
- **Twin logic (the right rule):** A step that must happen several times (or an unknown number of times) needs a loop such as while or for; code without a loop runs once.
- **Role:** context

**42. `if_statement` &rarr; `IfIsLoop`** (misconception)

- **Exact edge logic (the wrong rule):** The if body keeps repeating as long as its condition stays true.
- **Twin logic (the right rule):** An if body runs at most once; only a loop repeats its body.
- **Role:** primary

**43. `if_statement` &rarr; `LoopForOneTimeTest`** (misconception)

- **Exact edge logic (the wrong rule):** Uses a loop where a condition needs to be tested only once.
- **Twin logic (the right rule):** A test made once is an if; a loop repeats.
- **Role:** context

**44. `if_statement` &rarr; `MissingBraces`** (misconception)

- **Exact edge logic (the wrong rule):** Omits braces around a single-statement body of if, for or while.
- **Twin logic (the right rule):** Braces are optional for a single-statement body, but using them anyway avoids bugs when statements are added later.
- **Role:** primary

**45. `infinite_loop` &rarr; `InfiniteLoopUnnoticed`** (misconception)

- **Exact edge logic (the wrong rule):** a condition that never goes false still terminates
- **Twin logic (the right rule):** A while loop stops only when its condition is false at a check, so if no pass changes the variables in the condition, it never stops.
- **Role:** primary

**46. `infinite_loop` &rarr; `JavaDetectsInfiniteLoops`** (misconception)

- **Exact edge logic (the wrong rule):** If my loop never ends, the compiler or Java will warn me.
- **Twin logic (the right rule):** Java cannot detect infinite loops in general; you must check that the loop condition eventually becomes false.
- **Role:** primary

**47. `infinite_loop` &rarr; `LoopVariableNotUpdated`** (misconception)

- **Exact edge logic (the wrong rule):** A while loop ends by itself even if nothing in the body changes the variable tested in the condition.
- **Twin logic (the right rule):** If no statement in the body changes a variable in the condition, a condition that was true stays true and the loop never ends.
- **Role:** context

**48. `loop_body` &rarr; `LoopBodyAlwaysOnce`** (misconception)

- **Exact edge logic (the wrong rule):** The loop body always runs at least once, even if the condition is false at the start.
- **Twin logic (the right rule):** A while or for body runs zero times when the condition is false at the start.
- **Role:** context

**49. `loop_body` &rarr; `WhileStopsMidBody`** (misconception)

- **Exact edge logic (the wrong rule):** The loop stops the moment the condition becomes false, even in the middle of the body.
- **Twin logic (the right rule):** The condition is tested only before each pass, so the whole body finishes before the loop can stop.
- **Role:** context

**50. `loop_control` &rarr; `InfiniteLoopUnnoticed`** (misconception)

- **Exact edge logic (the wrong rule):** A while loop always stops on its own, even if nothing in its body can make the condition false.
- **Twin logic (the right rule):** A while loop stops only when its condition is false at a check, so if no pass changes the variables in the condition, it never stops.
- **Role:** context

**51. `loop_guard` &rarr; `LoopConditionValidatedLater`** (misconception)

- **Exact edge logic (the wrong rule):** If a loop condition is false at first but would become true later, the loop still runs (it repeats or skips until the condition is true, then runs until it is false).
- **Twin logic (the right rule):** A while loop whose condition is false at the first test runs zero times; nothing later revives it.
- **Role:** context

**52. `loop_guard` &rarr; `LoopCountByIntent`** (misconception)

- **Exact edge logic (the wrong rule):** How many times a loop runs is decided by what the program is meant to do, so it may go on after its condition is false.
- **Twin logic (the right rule):** The loop runs only while its condition is true when tested; it stops at the first false test.
- **Role:** context

**53. `loop_guard` &rarr; `LoopVariableNotUpdated`** (misconception)

- **Exact edge logic (the wrong rule):** A while loop ends by itself even if nothing in the body changes the variable tested in the condition.
- **Twin logic (the right rule):** If no statement in the body changes a variable in the condition, a condition that was true stays true and the loop never ends.
- **Role:** primary

**54. `while_loop` &rarr; `LoopIgnoresCodeBefore`** (error)

- **Exact edge logic (the wrong rule):** Initializes the flag before the loop so that the loop condition is already false, and the loop body never runs.
- **Twin logic (the right rule):** A while loop tests its condition before the first pass: if the values set before the loop make the condition false, the body never runs.
- **Role:** primary

**55. `while_loop` &rarr; `SemicolonAfterIfHeader`** (error)

- **Exact edge logic (the wrong rule):** if (x &gt; 0); System.out.println("positive"); prints only for positive x.
- **Twin logic (the right rule):** The ; ends the if with an empty statement, so the next line always runs.
- **Role:** context

**56. `while_loop` &rarr; `SemicolonAfterLoopHeader`** (error)

- **Exact edge logic (the wrong rule):** Puts a ; right after for (...) or while (...).
- **Twin logic (the right rule):** A ; right after the loop header is a null (empty) loop body, so the statements written after it are not repeated by the loop.
- **Role:** context

**57. `empty_statement` &rarr; `SemicolonAfterIfHeader`** (error)

- **Exact edge logic (the wrong rule):** if (x &gt; 0); System.out.println("positive"); prints only for positive x.
- **Twin logic (the right rule):** The ; ends the if with an empty statement, so the next line always runs.
- **Role:** context

**58. `empty_statement` &rarr; `SemicolonAfterLoopHeader`** (error)

- **Exact edge logic (the wrong rule):** Puts a ; right after for (...) or while (...).
- **Twin logic (the right rule):** A ; right after the loop header is a null (empty) loop body, so the statements written after it are not repeated by the loop.
- **Role:** context

**59. `flag_search_loop` &rarr; `LoopIgnoresCodeBefore`** (error)

- **Exact edge logic (the wrong rule):** Initializes the flag before the loop so that the loop condition is already false, and the loop body never runs.
- **Twin logic (the right rule):** A while loop tests its condition before the first pass: if the values set before the loop make the condition false, the body never runs.
- **Role:** context

**60. `for_loop` &rarr; `SemicolonAfterIfHeader`** (error)

- **Exact edge logic (the wrong rule):** if (x &gt; 0); System.out.println("positive"); prints only for positive x.
- **Twin logic (the right rule):** The ; ends the if with an empty statement, so the next line always runs.
- **Role:** context

**61. `for_loop` &rarr; `SemicolonAfterLoopHeader`** (error)

- **Exact edge logic (the wrong rule):** Puts a ; right after for (...) or while (...).
- **Twin logic (the right rule):** A ; right after the loop header is a null (empty) loop body, so the statements written after it are not repeated by the loop.
- **Role:** primary

**62. `if_statement` &rarr; `SemicolonAfterIfHeader`** (error)

- **Exact edge logic (the wrong rule):** if (x &gt; 0); System.out.println("positive"); prints only for positive x.
- **Twin logic (the right rule):** The ; ends the if with an empty statement, so the next line always runs.
- **Role:** primary

**63. `logical_error` &rarr; `LoopIgnoresCodeBefore`** (error)

- **Exact edge logic (the wrong rule):** Initializes the flag before the loop so that the loop condition is already false, and the loop body never runs.
- **Twin logic (the right rule):** A while loop tests its condition before the first pass: if the values set before the loop make the condition false, the body never runs.
- **Role:** context

**64. `logical_error` &rarr; `SemicolonAfterIfHeader`** (error)

- **Exact edge logic (the wrong rule):** if (x &gt; 0); System.out.println("positive"); prints only for positive x.
- **Twin logic (the right rule):** The ; ends the if with an empty statement, so the next line always runs.
- **Role:** context

**65. `while_loop` &rarr; `while_loop@L0`** (has_level)

- **Exact edge logic:** while loop -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (17 ways).
  - **[0] everyday\_reading** (rule type E, folk-meaning rule): Folk meaning: English 'while' means 'during the time that', so the activity stops the instant the condition stops holding (the 'while demon'). A Java while tests its condition only before each pass; a pass that has started always finishes.
  - **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `LoopTerminatingCondition`: wrong rule: For and while loops end when the condition becomes true. Right rule: A for or while loop ends when its condition becomes false.
  - **[2] misconception** (rule type M, wrong rule / right rule) &rarr; `WhileStopsMidBody`: wrong rule: The loop stops the moment the condition becomes false, even in the middle of the body. Right rule: The condition is tested only before each pass, so the whole body finishes before the loop can stop.
  - **[3] misconception** (rule type M, wrong rule / right rule) &rarr; `LoopForOneTimeTest`: wrong rule: Uses a loop where a condition needs to be tested only once. Right rule: A test made once is an if; a loop repeats.
  - **[4] misconception** (rule type M, wrong rule / right rule) &rarr; `LoopImpliedByOneTest`: wrong rule: Testing one case is enough; Java will repeat the test for the other values by itself. Right rule: A statement runs once each time control reaches it; repeating a test for many values needs a loop.
  - **[5] misconception** (rule type M, wrong rule / right rule) &rarr; `ProgramEndsAfterLoop`: wrong rule: When a loop finishes the program ends, so code after the loop never runs. Right rule: When the loop condition becomes false, control continues with the first statement after the loop.
  - **[6] misconception** (rule type M, wrong rule / right rule) &rarr; `LoopCountByIntent`: wrong rule: How many times a loop runs is decided by what the program is meant to do, so it may go on after its condition is false. Right rule: The loop runs only while its condition is true when tested; it stops at the first false test.
  - **[7] misconception** (rule type M, wrong rule / right rule) &rarr; `LoopConditionValidatedLater`: wrong rule: If a loop condition is false at first but would become true later, the loop still runs (it repeats or skips until the condition is true, then runs until it is false). Right rule: A while loop whose condition is false at the first test runs zero times; nothing later revives it.
  - **[8] misconception** (rule type M, wrong rule / right rule) &rarr; `SingleIterationInsteadOfLoop`: wrong rule: A task that must be repeated is written once, without a loop, as if one pass were enough. Right rule: A step that must happen several times (or an unknown number of times) needs a loop such as while or for; code without a loop runs once.
  - **[9] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `LoopTerminatingCondition`: Applies the while rule (LT) unevenly: tests the condition before some passes but not others, stops in the middle of a body on one pass, or runs the first pass without testing. (here mixing in: "For and while loops end when the condition becomes true")
  - **[10] misconception** (rule type M, wrong rule / right rule) &rarr; `IfIsLoop`: wrong rule: an if body repeats while its condition holds. Right rule: An if body runs at most once; only a loop repeats its body.
  - **[11] misconception** (rule type M, wrong rule / right rule) &rarr; `LoopBodyAlwaysOnce`: wrong rule: The loop body always runs at least once, even if the condition is false at the start. Right rule: A while or for body runs zero times when the condition is false at the start.
  - **[12] misconception** (rule type M, wrong rule / right rule) &rarr; `InfiniteLoopUnnoticed`: wrong rule: a condition that never goes false still terminates. Right rule: A while loop stops only when its condition is false at a check, so if no pass changes the variables in the condition, it never stops.
  - **[13] misconception** (rule type M, wrong rule / right rule) &rarr; `JavaDetectsInfiniteLoops`: wrong rule: If my loop never ends, the compiler or Java will warn me. Right rule: Java cannot detect infinite loops in general; you must check that the loop condition eventually becomes false.
  - **[14] misconception** (rule type M, wrong rule / right rule) &rarr; `ForWhileNotInterchangeable`: wrong rule: Some loops can only be written with for, others only with while. Right rule: Any for loop can be rewritten as a while loop and vice versa; for just packages init, test and update.
  - **[15] misconception** (rule type M, wrong rule / right rule) &rarr; `FalseLoopRepeatsNextCode`: wrong rule: A loop is an iterative if-else: while the condition is true the body repeats, and when it is false the code after the loop repeats. Right rule: Only the body is repeated; once the condition is false the code after the loop runs once.
  - **[16] misconception** (rule type M, wrong rule / right rule) &rarr; `LoopVariableNotUpdated`: wrong rule: A while loop ends by itself even if nothing in the body changes the variable tested in the condition. Right rule: If no statement in the body changes a variable in the condition, a condition that was true stays true and the loop never ends.

**66. `while_loop` &rarr; `while_loop@L1`** (has_level)

- **Exact edge logic:** while loop -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).
  - **[0] names\_the\_element** (rule type N, identity rule): The while statement is a loop (iteration statement): it repeats a body as long as a boolean condition is true.
  - **[1] states\_the\_rule** (rule type S, declarative rule): Syntax: while (&lt;boolean expression&gt;) { &lt;statements&gt; } (braces optional for one statement). Meaning: if the expression is false do nothing; if true, execute the body, then check the expression again, and continue as long as it is true.

**67. `while_loop` &rarr; `while_loop@L2`** (has_level)

- **Exact edge logic:** while loop -&gt; L2 (Multistructural): the answer applies the rules of while loop to every part of the code, in order (3 ways).
  - **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): 1. Evaluate the condition. 2. If false, skip the body and continue after the loop. 3. If true, execute the whole body, then go back to step 1.
  - **[1] output\_prediction** (rule type OP, evaluation / result rule): A while statement has no value; its result is the state and output after the passes it made: e.g. TenHellos with i = 4 and i &lt;= 10 prints 4th to 10th Hello (7 passes) and leaves i = 11.
  - **[2] one\_step\_execution** (rule type OS, state-transition rule): One pass: test the condition with the current values, then (if true) apply every body statement once in order; the variables assigned in the body change and nothing else; a false test ends the loop with the state unchanged.

**68. `while_loop` &rarr; `while_loop@L3`** (has_level)

- **Exact edge logic:** while loop -&gt; L3 (Relational): the answer relates the parts (11 ways).
  - **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): The loop condition is a boolean expression evaluated before every pass; the loop stops the first time it is false, so the body must eventually make it false.
  - **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): do { body } while (c); means the same as while (c) { body } except that the first test is omitted, so the body runs at least once.
  - **[2] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): break exits the loop immediately, so a while loop can end either by a false test or by a break; while (true) needs a break (or is infinite).
  - **[3] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): An animation repeats clear/draw/show/pause steps inside a loop, typically one that runs indefinitely.
  - **[4] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): A convergence test is the while condition that keeps refining an estimate until the error is within tolerance, e.g. while (Math.abs(t - c/t) &gt; epsilon \* t).
  - **[5] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): The body is the block that the while repeats; it runs only after a true test and is completed before the next test.
  - **[6] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): The while condition usually tests a loop variable that is initialized before the loop and updated in the body; if the body never changes it, the loop never ends.
  - **[7] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): To trust a while loop, state what stays true on every pass and why the condition eventually becomes false (e.g. v is always a power of 2, v increases, so the loop terminates).
  - **[8] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Binary conversion uses while loops: one to find the largest power of 2 &lt;= N, and one to cast out powers of 2 in decreasing order.
  - **[9] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): if and while have the same form, but if tests its condition once and runs the block at most once, while while tests again after every pass and repeats the block as long as the condition is true.
  - **[10] purpose\_of\_the\_whole** (rule type P, plan / role rule): Plan: indefinite (event-controlled) repetition - repeat until something happens whose number of passes is not known in advance (until convergence, until broke or goal); the condition variable is often a stepper or most-recent holder.

**69. `while_loop` &rarr; `while_loop@L4`** (has_level)

- **Exact edge logic:** while loop -&gt; L4 (Extended abstract): the answer reasons beyond the given code (6 ways).
  - **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `LoopTerminatingCondition`: Changing &lt; to &lt;= adds exactly one pass at the boundary; removing the update from the body makes a loop that was entered never end; a condition that is false initially gives zero passes whatever the body does. Rewriting as for (init; cond; update) preserves behaviour if no continue is involved.
  - **[1] diagnose\_an\_error** (rule type D, error rule): rule broken: A while loop tests its condition before the first pass, using the values set before the loop. Kind: silent logic error. Trigger class: Initializations before the loop that already make the condition false (e.g. boolean done = true; while (!done) ...): the body runs zero times and no error is reported.
  - **[2] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Use while when the number of passes depends on what happens during the loop (convergence, input, simulation) or the loop variable is needed after the loop; use for for counted loops, do-while when the body must run at least once, and if when the test is needed only once.
  - **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: A ; right after if (...) is an empty statement that forms the whole then branch; the following statement or block is no longer part of the if. Kind: silent logic error. Trigger class: Any if (cond); followed by a statement or block: that statement runs for every input, whatever cond is (it compiles without error).
  - **[4] diagnose\_an\_error** (rule type D, error rule): rule broken: A ; right after while (...) or for (...) is an empty statement that is the whole loop body; the block written next is not repeated. Kind: silent logic error. Trigger class: for (...); { body } runs the body once after the loop ends; while (cond); with a cond that the empty body cannot change hangs forever (infinite loop) when cond starts true.
  - **[5] diagnose\_an\_error** (rule type D, error rule): rule broken: The body must eventually make the condition false. Kind: silent logic error. Trigger class: No body statement changes a variable in the condition, or the update moves away from the bound (e.g. while (i &gt; 3) i = i + 1;): infinite loop, endless output or a hang; Java cannot detect it in general.

**70. `topic1.3.c` &rarr; `while_loop`** (contains)

- topic `topic1.3.c` contains `while_loop`

**71. `topic1.3.c` &rarr; `loop_body`** (contains)

- topic `topic1.3.c` contains `loop_body`

**72. `topic1.3.c` &rarr; `loop_control`** (contains)

- topic `topic1.3.c` contains `loop_control`

**73. `topic1.3.c` &rarr; `loop_invariant_reasoning`** (contains)

- topic `topic1.3.c` contains `loop_invariant_reasoning`
