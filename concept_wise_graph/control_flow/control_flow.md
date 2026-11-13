# control_flow (`control_flow`)

the order in which statements are executed

Section 1.3 Conditionals and Loops, topic 1.3.a Control flow.

![The knowledge graph around control_flow](control_flow.png)

## At a glance

- **Needs first:** `statement`
- **Leads to:** `flowchart`, `if_statement`, `switch_statement`
- **Learned alongside:** nothing
- **Misconceptions:** `CodeAfterIfSkipped`, `FalseConditionRestartsProgram`, `FalseLoopRepeatsNextCode`, `IfConditionWatched`, `IfWaitsForCondition`, `LoopImpliedByOneTest`, `NoShortCircuit`, `ProgramEndsAfterLoop`, `ProgramLooksAhead`, `ReturnDoesNotExitLoop`, `StatementsRunInAnyOrder`
- **Errors:** none
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 39 edges around this concept. The edge logic, the wrong and right rules and the exact rules of the ways are copied word for word from the graph.

## To work on (2)

- misconceptions with no L0 way linked to them: ReturnDoesNotExitLoop
- no aliases: a student's words cannot name this concept

## What it needs first (1)

A prerequisite edge means the other concept has to be understood before `control_flow`.

### `statement` comes before `control_flow`

*one step, terminated by ;, executed in sequence*

- **Edge:** `pre:statement->control_flow`
- **Exact edge logic:** Control flow is the order in which statements run.
- **Grounding:** book\_passage
- **Composition rule (R) of `control_flow` with `statement`:** Control flow is defined over statements: statements are executed for their effect, and if/while/for are themselves statements that may be used wherever a statement is allowed, so they can nest.
- **Composition rule (R) of `statement` with `control_flow`:** Control flow is the order in which statements run; without control statements it is straight-line, each once in order.

## What it leads to (3)

These concepts need `control_flow` first.

### `control_flow` comes before `flowchart`

*Flowchart: a diagram whose paths correspond to the flow-of-control paths through a program*

- **Edge:** `pre:control_flow->flowchart`
- **Exact edge logic:** A flowchart draws the flow of control: each path through the diagram is a path the program can take.
- **Grounding:** book\_passage
- **Composition rule (R) of `control_flow` with `flowchart`:** A flowchart draws control flow: each path through the diagram is a possible path of execution, with a decision box for each if or loop test.
- **Composition rule (R) of `flowchart` with `control_flow`:** The flowchart's arrows are the program's control flow: sequence = a straight chain, if = branch and rejoin, loop = a back arrow to the test. Nesting a loop draws a loop inside a loop, and the diagram quickly becomes complex.

### `control_flow` comes before `if_statement`

*run a block only when the condition holds*

- **Edge:** `pre:control_flow->if_statement`
- **Exact edge logic:** An if changes the default top-to-bottom flow by running a block only when its condition is true.
- **Grounding:** book\_passage
- **Composition rule (R) of `control_flow` with `if_statement`:** An if changes the default top-to-bottom flow: its condition is tested once when control reaches it, its block runs only if true, and in both cases control then continues with the next statement.
- **Composition rule (R) of `if_statement` with `control_flow`:** An if is a fork in the control flow: one path through the body, one around it, both rejoining at the next statement.

### `control_flow` comes before `switch_statement`

*switch (x) { case v: ...; break; default: ... }*

- **Edge:** `pre:control_flow->switch_statement`
- **Exact edge logic:** switch directs the flow of control to one of several case labels, depending on the value of one expression.
- **Grounding:** book\_passage

## Learned alongside (0)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

No parallel edge touches this concept.

## Misconceptions (11)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### CodeAfterIfSkipped

- **Edge:** `control_flow` &rarr; `CodeAfterIfSkipped` (misconception)
- **Exact edge logic (the wrong rule):** When the then branch runs, the code after the if is skipped.
- **Twin logic (the right rule):** After the if finishes, execution continues with the next statement either way.
- **Wrong belief (on the node):** When the then branch runs, the code after the if is skipped.
- **Correct rule (on the node):** After the if finishes, execution continues with the next statement either way.
- **Provenance:** published
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [4] misconception, exact rule:** wrong rule: When the then branch runs, the code after the if is skipped. Right rule: After the if finishes, execution continues with the next statement either way.
- **Edge `if_statement` &rarr; `CodeAfterIfSkipped`, exact edge logic:** When the then branch runs, the code after the if is skipped. **Twin logic:** After the if finishes, execution continues with the next statement either way. (role: primary)

### FalseConditionRestartsProgram

- **Edge:** `control_flow` &rarr; `FalseConditionRestartsProgram` (misconception)
- **Exact edge logic (the wrong rule):** When an if condition is false (and there is no else), control jumps back to the start of the program.
- **Twin logic (the right rule):** A false condition skips the then branch and execution continues with the statement after the if statement.
- **Wrong belief (on the node):** When an if condition is false (and there is no else), control jumps back to the start of the program.
- **Correct rule (on the node):** A false condition skips the then branch and execution continues with the statement after the if statement.
- **Provenance:** published
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [8] misconception, exact rule:** wrong rule: When an if condition is false (and there is no else), control jumps back to the start of the program. Right rule: A false condition skips the then branch and execution continues with the statement after the if statement.
- **Edge `if_statement` &rarr; `FalseConditionRestartsProgram`, exact edge logic:** When an if condition is false (and there is no else), control jumps back to the start of the program. **Twin logic:** A false condition skips the then branch and execution continues with the statement after the if statement. (role: primary)

### FalseLoopRepeatsNextCode

- **Edge:** `control_flow` &rarr; `FalseLoopRepeatsNextCode` (misconception)
- **Exact edge logic (the wrong rule):** A loop is an iterative if-else: while the condition is true the body repeats, and when it is false the code after the loop repeats.
- **Twin logic (the right rule):** Only the body is repeated; once the condition is false the code after the loop runs once.
- **Wrong belief (on the node):** A loop is an iterative if-else: while the condition is true the body repeats, and when it is false the code after the loop repeats.
- **Correct rule (on the node):** Only the body is repeated; once the condition is false the code after the loop runs once.
- **Provenance:** published
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [11] misconception, exact rule:** wrong rule: A loop is an iterative if-else: while the condition is true the body repeats, and when it is false the code after the loop repeats. Right rule: Only the body is repeated; once the condition is false the code after the loop runs once.
- **Edge `for_loop` &rarr; `FalseLoopRepeatsNextCode`, exact edge logic:** A loop is an iterative if-else: while the condition is true the body repeats, and when it is false the code after the loop repeats. **Twin logic:** Only the body is repeated; once the condition is false the code after the loop runs once. (role: primary)
- **Edge `while_loop` &rarr; `FalseLoopRepeatsNextCode`, exact edge logic:** A loop is an iterative if-else: while the condition is true the body repeats, and when it is false the code after the loop repeats. **Twin logic:** Only the body is repeated; once the condition is false the code after the loop runs once. (role: context)

### IfConditionWatched

- **Edge:** `control_flow` &rarr; `IfConditionWatched` (misconception)
- **Exact edge logic (the wrong rule):** An if statement watches its condition while the program runs and fires as soon as the condition becomes true (if = whenever).
- **Twin logic (the right rule):** An if condition is tested once, when control reaches the if statement; later changes to the variables do not trigger the branch.
- **Wrong belief (on the node):** An if statement watches its condition while the program runs and fires as soon as the condition becomes true (if = whenever).
- **Correct rule (on the node):** An if condition is tested once, when control reaches the if statement; later changes to the variables do not trigger the branch.
- **Provenance:** published
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [9] misconception, exact rule:** wrong rule: An if statement watches its condition while the program runs and fires as soon as the condition becomes true (if = whenever). Right rule: An if condition is tested once, when control reaches the if statement; later changes to the variables do not trigger the branch.
- **Edge `if_statement` &rarr; `IfConditionWatched`, exact edge logic:** An if statement watches its condition while the program runs and fires as soon as the condition becomes true (if = whenever). **Twin logic:** An if condition is tested once, when control reaches the if statement; later changes to the variables do not trigger the branch. (role: primary)

### IfWaitsForCondition

- **Edge:** `control_flow` &rarr; `IfWaitsForCondition` (misconception)
- **Exact edge logic (the wrong rule):** An IF statement earlier in the program stays active and fires later, e.g. inside a later loop, when its condition becomes true.
- **Twin logic (the right rule):** An if is evaluated once when control reaches it; afterwards it is inactive unless control returns to it.
- **Wrong belief (on the node):** An IF statement earlier in the program stays active and fires later, e.g. inside a later loop, when its condition becomes true.
- **Correct rule (on the node):** An if is evaluated once when control reaches it; afterwards it is inactive unless control returns to it.
- **Provenance:** published
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [7] misconception, exact rule:** wrong rule: An IF statement earlier in the program stays active and fires later, e.g. inside a later loop, when its condition becomes true. Right rule: An if is evaluated once when control reaches it; afterwards it is inactive unless control returns to it.
- **Edge `if_statement` &rarr; `IfWaitsForCondition`, exact edge logic:** An IF statement earlier in the program stays active and fires later, e.g. inside a later loop, when its condition becomes true. **Twin logic:** An if is evaluated once when control reaches it; afterwards it is inactive unless control returns to it. (role: primary)

### LoopImpliedByOneTest

- **Edge:** `control_flow` &rarr; `LoopImpliedByOneTest` (misconception)
- **Exact edge logic (the wrong rule):** Testing one case is enough; Java will repeat the test for the other values by itself.
- **Twin logic (the right rule):** A statement runs once each time control reaches it; repeating a test for many values needs a loop.
- **Wrong belief (on the node):** Testing one case is enough; Java will repeat the test for the other values by itself.
- **Correct rule (on the node):** A statement runs once each time control reaches it; repeating a test for many values needs a loop.
- **Provenance:** published
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [6] misconception, exact rule:** wrong rule: Testing one case is enough; Java will repeat the test for the other values by itself. Right rule: A statement runs once each time control reaches it; repeating a test for many values needs a loop.
- **Edge `for_loop` &rarr; `LoopImpliedByOneTest`, exact edge logic:** Testing one case is enough; Java will repeat the test for the other values by itself. **Twin logic:** A statement runs once each time control reaches it; repeating a test for many values needs a loop. (role: context)
- **Edge `while_loop` &rarr; `LoopImpliedByOneTest`, exact edge logic:** Testing one case is enough; Java will repeat the test for the other values by itself. **Twin logic:** A statement runs once each time control reaches it; repeating a test for many values needs a loop. (role: primary)

### NoShortCircuit

- **Edge:** `control_flow` &rarr; `NoShortCircuit` (misconception)
- **Exact edge logic (the wrong rule):** logical AND/OR always evaluate both sides (Java short-circuits them)
- **Twin logic (the right rule):** In p &amp;&amp; q, q is evaluated only when p is true; in p \|\| q, q is evaluated only when p is false.
- **Wrong belief (on the node):** logical AND/OR always evaluate both sides (Java short-circuits them)
- **Correct rule (on the node):** In p &amp;&amp; q, q is evaluated only when p is true; in p \|\| q, q is evaluated only when p is false.
- **Provenance:** published
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [5] misconception, exact rule:** wrong rule: logical AND/OR always evaluate both sides (Java short-circuits them). Right rule: In p &amp;&amp; q, q is evaluated only when p is true; in p \|\| q, q is evaluated only when p is false.
- **Edge `short_circuit` &rarr; `NoShortCircuit`, exact edge logic:** In p &amp;&amp; q, both p and q are always evaluated. **Twin logic:** In p &amp;&amp; q, q is evaluated only when p is true; in p \|\| q, q is evaluated only when p is false. (role: primary)

### ProgramEndsAfterLoop

- **Edge:** `control_flow` &rarr; `ProgramEndsAfterLoop` (misconception)
- **Exact edge logic (the wrong rule):** When a loop finishes the program ends, so code after the loop never runs.
- **Twin logic (the right rule):** When the loop condition becomes false, control continues with the first statement after the loop.
- **Wrong belief (on the node):** When a loop finishes the program ends, so code after the loop never runs.
- **Correct rule (on the node):** When the loop condition becomes false, control continues with the first statement after the loop.
- **Provenance:** published
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [10] misconception, exact rule:** wrong rule: When a loop finishes the program ends, so code after the loop never runs. Right rule: When the loop condition becomes false, control continues with the first statement after the loop.
- **Edge `for_loop` &rarr; `ProgramEndsAfterLoop`, exact edge logic:** When a loop finishes the program ends, so code after the loop never runs. **Twin logic:** When the loop condition becomes false, control continues with the first statement after the loop. (role: context)
- **Edge `while_loop` &rarr; `ProgramEndsAfterLoop`, exact edge logic:** When a loop finishes the program ends, so code after the loop never runs. **Twin logic:** When the loop condition becomes false, control continues with the first statement after the loop. (role: primary)

### ProgramLooksAhead

- **Edge:** `control_flow` &rarr; `ProgramLooksAhead` (misconception)
- **Exact edge logic (the wrong rule):** The program knows or sees what later lines will do and acts on those goals at the current line, e.g. it stops 'at ten' because it wants to draw a box.
- **Twin logic (the right rule):** Each statement executes using only the current state; later lines have no effect until control reaches them.
- **Wrong belief (on the node):** The program knows or sees what later lines will do and acts on those goals at the current line, e.g. it stops 'at ten' because it wants to draw a box.
- **Correct rule (on the node):** Each statement executes using only the current state; later lines have no effect until control reaches them.
- **Provenance:** published
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [2] misconception, exact rule:** wrong rule: The program knows or sees what later lines will do and acts on those goals at the current line, e.g. it stops 'at ten' because it wants to draw a box. Right rule: Each statement executes using only the current state; later lines have no effect until control reaches them.
- **Edge `if_statement` &rarr; `ProgramLooksAhead`, exact edge logic:** The program knows or sees what later lines will do and acts on those goals at the current line, e.g. it stops 'at ten' because it wants to draw a box. **Twin logic:** Each statement executes using only the current state; later lines have no effect until control reaches them. (role: context)
- **Edge `statement` &rarr; `ProgramLooksAhead`, exact edge logic:** The program knows or sees what later lines will do and acts on those goals at the current line, e.g. it stops 'at ten' because it wants to draw a box. **Twin logic:** Each statement executes using only the current state; later lines have no effect until control reaches them. (role: context)

### ReturnDoesNotExitLoop

- **Edge:** `control_flow` &rarr; `ReturnDoesNotExitLoop` (misconception)
- **Exact edge logic (the wrong rule):** A return inside a loop does not end the loop; it sets a value each pass (the last one is returned) or returns several values.
- **Twin logic (the right rule):** When return executes, the method ends at once, so the loop stops on that pass.
- **Wrong belief (on the node):** A return inside a loop does not end the loop; it sets a value each pass (the last one is returned) or returns several values.
- **Correct rule (on the node):** When return executes, the method ends at once, so the loop stops on that pass.
- **Provenance:** published
- **Role of this concept:** primary
- **L0 way linked to it:** no
- **Edge `flag_search_loop` &rarr; `ReturnDoesNotExitLoop`, exact edge logic:** A return inside a loop does not end the loop; it sets a value each pass (the last one is returned) or returns several values. **Twin logic:** When return executes, the method ends at once, so the loop stops on that pass. (role: context)
- **Edge `for_loop` &rarr; `ReturnDoesNotExitLoop`, exact edge logic:** A return inside a loop does not end the loop; it sets a value each pass (the last one is returned) or returns several values. **Twin logic:** When return executes, the method ends at once, so the loop stops on that pass. (role: context)

### StatementsRunInAnyOrder

- **Edge:** `control_flow` &rarr; `StatementsRunInAnyOrder` (misconception)
- **Exact edge logic (the wrong rule):** Statements in a program can run in any order.
- **Twin logic (the right rule):** Without control statements, statements run once each, top to bottom.
- **Wrong belief (on the node):** Statements in a program can run in any order.
- **Correct rule (on the node):** Without control statements, statements run once each, top to bottom.
- **Provenance:** published
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [1] misconception, exact rule:** wrong rule: Statements in a program can run in any order. Right rule: Without control statements, statements run once each, top to bottom.
- **L0 way [3] inconsistent\_trace, exact rule:** Applies the sequencing rule (LT) unevenly: e.g. runs a later line before an earlier one, lets an if that was already passed fire again later, or ends the program when a loop or a false if ends instead of continuing with the next statement. (here mixing in: "Statements in a program can run in any order")
- **Edge `statement` &rarr; `StatementsRunInAnyOrder`, exact edge logic:** Statements in a program can run in any order. **Twin logic:** Without control statements, statements run once each, top to bottom. (role: context)

## Errors (0)

An error edge states the rule that gets broken in a program, and the right rule.

The graph has no error edge from this concept.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for control flow: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to control flow agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

- **Edge:** `control_flow` &rarr; `control_flow@L0` (has_level)
- **Exact edge logic:** control flow -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (12 ways).

Ways (12), each with its exact rule:

- **[0] everyday\_reading** (rule type E, folk-meaning rule): Folk meaning: in everyday instructions a listener reads the whole list at once, does steps in a sensible order and infers what the writer wants. Java instead executes statements one at a time, top to bottom, each only when control reaches it, and nothing later in the program has any effect earlier.
- **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `StatementsRunInAnyOrder`: wrong rule: Statements in a program can run in any order. Right rule: Without control statements, statements run once each, top to bottom.
- **[2] misconception** (rule type M, wrong rule / right rule) &rarr; `ProgramLooksAhead`: wrong rule: The program knows or sees what later lines will do and acts on those goals at the current line, e.g. it stops 'at ten' because it wants to draw a box. Right rule: Each statement executes using only the current state; later lines have no effect until control reaches them.
- **[3] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `StatementsRunInAnyOrder`: Applies the sequencing rule (LT) unevenly: e.g. runs a later line before an earlier one, lets an if that was already passed fire again later, or ends the program when a loop or a false if ends instead of continuing with the next statement. (here mixing in: "Statements in a program can run in any order")
- **[4] misconception** (rule type M, wrong rule / right rule) &rarr; `CodeAfterIfSkipped`: wrong rule: When the then branch runs, the code after the if is skipped. Right rule: After the if finishes, execution continues with the next statement either way.
- **[5] misconception** (rule type M, wrong rule / right rule) &rarr; `NoShortCircuit`: wrong rule: logical AND/OR always evaluate both sides (Java short-circuits them). Right rule: In p &amp;&amp; q, q is evaluated only when p is true; in p \|\| q, q is evaluated only when p is false.
- **[6] misconception** (rule type M, wrong rule / right rule) &rarr; `LoopImpliedByOneTest`: wrong rule: Testing one case is enough; Java will repeat the test for the other values by itself. Right rule: A statement runs once each time control reaches it; repeating a test for many values needs a loop.
- **[7] misconception** (rule type M, wrong rule / right rule) &rarr; `IfWaitsForCondition`: wrong rule: An IF statement earlier in the program stays active and fires later, e.g. inside a later loop, when its condition becomes true. Right rule: An if is evaluated once when control reaches it; afterwards it is inactive unless control returns to it.
- **[8] misconception** (rule type M, wrong rule / right rule) &rarr; `FalseConditionRestartsProgram`: wrong rule: When an if condition is false (and there is no else), control jumps back to the start of the program. Right rule: A false condition skips the then branch and execution continues with the statement after the if statement.
- **[9] misconception** (rule type M, wrong rule / right rule) &rarr; `IfConditionWatched`: wrong rule: An if statement watches its condition while the program runs and fires as soon as the condition becomes true (if = whenever). Right rule: An if condition is tested once, when control reaches the if statement; later changes to the variables do not trigger the branch.
- **[10] misconception** (rule type M, wrong rule / right rule) &rarr; `ProgramEndsAfterLoop`: wrong rule: When a loop finishes the program ends, so code after the loop never runs. Right rule: When the loop condition becomes false, control continues with the first statement after the loop.
- **[11] misconception** (rule type M, wrong rule / right rule) &rarr; `FalseLoopRepeatsNextCode`: wrong rule: A loop is an iterative if-else: while the condition is true the body repeats, and when it is false the code after the loop repeats. Right rule: Only the body is repeated; once the condition is false the code after the loop runs once.

### L1: Unistructural / atom x text surface

L1 for control flow: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

- **Edge:** `control_flow` &rarr; `control_flow@L1` (has_level)
- **Exact edge logic:** control flow -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

Ways (2), each with its exact rule:

- **[0] names\_the\_element** (rule type N, identity rule): Control flow is the order in which a program's statements are executed (statement sequencing); conditionals and loops are the statements that change it.
- **[1] states\_the\_rule** (rule type S, declarative rule): Without control statements every statement executes once, in the order given; a block executes its statements in order from first to last; if/if-else choose between one or two alternatives and loops repeat statements depending on a condition.

### L2: Multistructural / block x execution / preoperational

L2 for control flow: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

- **Edge:** `control_flow` &rarr; `control_flow@L2` (has_level)
- **Exact edge logic:** control flow -&gt; L2 (Multistructural): the answer applies the rules of control flow to every part of the code, in order (3 ways).

Ways (3), each with its exact rule:

- **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): Execute the statement at the current point; when it completes normally, control passes to the next statement in the block. An if evaluates its condition once and then runs at most one branch; a loop evaluates its condition before each pass; after an if or a loop finishes, control continues with the statement after it.
- **[1] output\_prediction** (rule type OP, evaluation / result rule): The output is the sequence of print statements that control actually reaches, in the order reached: e.g. TenHellos prints 1st, 2nd, 3rd Hello once each, then 4th to 10th Hello from the loop.
- **[2] one\_step\_execution** (rule type OS, state-transition rule): One step executes the single statement at the current control point using the current values, updates at most the variables it assigns, and moves the control point to the next statement (or, for an if/loop test, to the chosen branch, back to the test, or past the statement).

### L3: Relational / relations x function (concrete operational begins)

L3 for control flow: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

- **Edge:** `control_flow` &rarr; `control_flow@L3` (has_level)
- **Exact edge logic:** control flow -&gt; L3 (Relational): the answer relates the parts (4 ways).

Ways (4), each with its exact rule:

- **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Control flow is defined over statements: statements are executed for their effect, and if/while/for are themselves statements that may be used wherever a statement is allowed, so they can nest.
- **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): An if changes the default top-to-bottom flow: its condition is tested once when control reaches it, its block runs only if true, and in both cases control then continues with the next statement.
- **[2] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): A flowchart draws control flow: each path through the diagram is a possible path of execution, with a decision box for each if or loop test.
- **[3] purpose\_of\_the\_whole** (rule type P, plan / role rule): Plan: control flow lets one program do different things for different inputs (selection) and do a thing many times (repetition), so a short program can specify a potentially unlimited number of executed statements.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for control flow: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

- **Edge:** `control_flow` &rarr; `control_flow@L4` (has_level)
- **Exact edge logic:** control flow -&gt; L4 (Extended abstract): the answer reasons beyond the given code (4 ways).

Ways (4), each with its exact rule:

- **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `StatementsRunInAnyOrder`: Reordering two statements generally changes the result whenever one reads a variable that the other writes (e.g. swapping x = x + 1 and print(x)); reordering is safe only for statements that touch disjoint variables. Moving a statement into or out of a branch or loop body changes how many times it runs (0, 1 or n).
- **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Reason in terms of control flow whenever you must predict output or find why a statement did or did not run: trace which statement is reached next. Straight-line sequence suffices only when every input needs the same steps exactly once; otherwise add a conditional or a loop.
- **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: A local variable must be definitely assigned on every control-flow path before it is read. Kind: compile-time. Trigger class: A variable assigned only inside an if branch (or only in a loop body) and read after it: the compiler reports 'variable might not have been initialized'.
- **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: Statements run in the order written, so an update must come before the statement that needs the new value. Kind: silent logic error. Trigger class: Swapping two dependent statements (e.g. printing before updating, or incrementing the index before using it): output is shifted or off by one pass, with no error.

## Same topic

`control_flow` belongs to the topic **Control flow** (`topic1.3.a`). The topic also contains: `algorithm_pseudocode`, `flowchart`.

## Rules of the concept (25)

- **Book** (SW-1e, p. 46 (pdf 56)): "each of the statements in the program is executed once, in the order given."
- **Book** (SW-1e, p. 70 (pdf 80)): "The if and if-else statements allow one or two alternatives in directing the flow of control."
- **Book** (OT-Expressions, ): "Finally, control flow statements regulate the order in which statements get executed."
- **E** (folk-meaning rule): Folk meaning: in everyday instructions a listener reads the whole list at once, does steps in a sensible order and infers what the writer wants. Java instead executes statements one at a time, top to bottom, each only when control reaches it, and nothing later in the program has any effect earlier.
- **M** (wrong rule / right rule): CodeAfterIfSkipped: wrong: When the then branch runs, the code after the if is skipped. \| right: After the if finishes, execution continues with the next statement either way.
- **M** (wrong rule / right rule): NoShortCircuit: wrong: logical AND/OR always evaluate both sides (Java short-circuits them) \| right: In p &amp;&amp; q, q is evaluated only when p is true; in p \|\| q, q is evaluated only when p is false.
- **M** (wrong rule / right rule): StatementsRunInAnyOrder: wrong: Statements in a program can run in any order. \| right: Without control statements, statements run once each, top to bottom.
- **M** (wrong rule / right rule): LoopImpliedByOneTest: wrong: Testing one case is enough; Java will repeat the test for the other values by itself. \| right: A statement runs once each time control reaches it; repeating a test for many values needs a loop.
- **M** (wrong rule / right rule): IfWaitsForCondition: wrong: An IF statement earlier in the program stays active and fires later, e.g. inside a later loop, when its condition becomes true. \| right: An if is evaluated once when control reaches it; afterwards it is inactive unless control returns to it.
- **M** (wrong rule / right rule): ProgramLooksAhead: wrong: The program knows or sees what later lines will do and acts on those goals at the current line, e.g. it stops 'at ten' because it wants to draw a box. \| right: Each statement executes using only the current state; later lines have no effect until control reaches them.
- **M** (wrong rule / right rule): FalseConditionRestartsProgram: wrong: When an if condition is false (and there is no else), control jumps back to the start of the program. \| right: A false condition skips the then branch and execution continues with the statement after the if statement.
- **M** (wrong rule / right rule): IfConditionWatched: wrong: An if statement watches its condition while the program runs and fires as soon as the condition becomes true (if = whenever). \| right: An if condition is tested once, when control reaches the if statement; later changes to the variables do not trigger the branch.
- **M** (wrong rule / right rule): ProgramEndsAfterLoop: wrong: When a loop finishes the program ends, so code after the loop never runs. \| right: When the loop condition becomes false, control continues with the first statement after the loop.
- **M** (wrong rule / right rule): FalseLoopRepeatsNextCode: wrong: A loop is an iterative if-else: while the condition is true the body repeats, and when it is false the code after the loop repeats. \| right: Only the body is repeated; once the condition is false the code after the loop runs once.
- **T** (uneven-application rule): Applies the sequencing rule (LT) unevenly: e.g. runs a later line before an earlier one, lets an if that was already passed fire again later, or ends the program when a loop or a false if ends instead of continuing with the next statement.
- **N** (identity rule): Control flow is the order in which a program's statements are executed (statement sequencing); conditionals and loops are the statements that change it.
- **S** (declarative rule): Without control statements every statement executes once, in the order given; a block executes its statements in order from first to last; if/if-else choose between one or two alternatives and loops repeat statements depending on a condition.
- **LT** (operational sequencing rule): Execute the statement at the current point; when it completes normally, control passes to the next statement in the block. An if evaluates its condition once and then runs at most one branch; a loop evaluates its condition before each pass; after an if or a loop finishes, control continues with the statement after it.
- **OP** (evaluation / result rule): The output is the sequence of print statements that control actually reaches, in the order reached: e.g. TenHellos prints 1st, 2nd, 3rd Hello once each, then 4th to 10th Hello from the loop.
- **OS** (state-transition rule): One step executes the single statement at the current control point using the current values, updates at most the variables it assigns, and moves the control point to the next statement (or, for an if/loop test, to the chosen branch, back to the test, or past the statement).
- **R** (composition rule (with a neighbour)): with statement: Control flow is defined over statements: statements are executed for their effect, and if/while/for are themselves statements that may be used wherever a statement is allowed, so they can nest.
- **R** (composition rule (with a neighbour)): with if\_statement: An if changes the default top-to-bottom flow: its condition is tested once when control reaches it, its block runs only if true, and in both cases control then continues with the next statement.
- **R** (composition rule (with a neighbour)): with flowchart: A flowchart draws control flow: each path through the diagram is a possible path of execution, with a decision box for each if or loop test.
- **P** (plan / role rule): Plan: control flow lets one program do different things for different inputs (selection) and do a thing many times (repetition), so a short program can specify a potentially unlimited number of executed statements.
- **C** (conservation rule): Reordering two statements generally changes the result whenever one reads a variable that the other writes (e.g. swapping x = x + 1 and print(x)); reordering is safe only for statements that touch disjoint variables. Moving a statement into or out of a branch or loop body changes how many times it runs (0, 1 or n).
- **D** (error rule): rule broken: A local variable must be definitely assigned on every control-flow path before it is read. (compile-time)
- **D** (error rule): rule broken: Statements run in the order written, so an update must come before the statement that needs the new value. (silent logic error)
- **X** (applicability rule): Reason in terms of control flow whenever you must predict output or find why a statement did or did not run: trace which statement is reached next. Straight-line sequence suffices only when every input needs the same steps exactly once; otherwise add a conditional or a loop.

## How it is found in code and answers (reader block)

- **Aliases:** none
- **Code patterns:** `\b(?:if|while|for|switch)\s*\(`, `\bdo\s*\{`, `\b(?:break|continue|return)\s*;`
- **Operator symbols:** none
- **Java types:** none

## The whole prerequisite chain

- **Everything it builds on (4):** `class_declaration`, `main_method`, `program_text`, `statement`
- **Everything that builds on it (8):** `conditional_operator`, `dangling_else`, `else_if_chain`, `flowchart`, `if_else_statement`, `if_statement`, `nested_conditionals`, `switch_statement`

## Every edge in this view and its exact edge logic (39)

All the edges drawn in the picture, in the order: prerequisite, parallel, misconception, error, has_level, contains.

**1. `control_flow` &rarr; `flowchart`** (prerequisite)

- **Exact edge logic:** A flowchart draws the flow of control: each path through the diagram is a path the program can take.
- **Grounding:** book\_passage
- **Composition rule (R) of `control_flow` with `flowchart`:** A flowchart draws control flow: each path through the diagram is a possible path of execution, with a decision box for each if or loop test.
- **Composition rule (R) of `flowchart` with `control_flow`:** The flowchart's arrows are the program's control flow: sequence = a straight chain, if = branch and rejoin, loop = a back arrow to the test. Nesting a loop draws a loop inside a loop, and the diagram quickly becomes complex.

**2. `control_flow` &rarr; `if_statement`** (prerequisite)

- **Exact edge logic:** An if changes the default top-to-bottom flow by running a block only when its condition is true.
- **Grounding:** book\_passage
- **Composition rule (R) of `control_flow` with `if_statement`:** An if changes the default top-to-bottom flow: its condition is tested once when control reaches it, its block runs only if true, and in both cases control then continues with the next statement.
- **Composition rule (R) of `if_statement` with `control_flow`:** An if is a fork in the control flow: one path through the body, one around it, both rejoining at the next statement.

**3. `control_flow` &rarr; `switch_statement`** (prerequisite)

- **Exact edge logic:** switch directs the flow of control to one of several case labels, depending on the value of one expression.
- **Grounding:** book\_passage

**4. `statement` &rarr; `control_flow`** (prerequisite)

- **Exact edge logic:** Control flow is the order in which statements run.
- **Grounding:** book\_passage
- **Composition rule (R) of `statement` with `control_flow`:** Control flow is the order in which statements run; without control statements it is straight-line, each once in order.
- **Composition rule (R) of `control_flow` with `statement`:** Control flow is defined over statements: statements are executed for their effect, and if/while/for are themselves statements that may be used wherever a statement is allowed, so they can nest.

**5. `control_flow` &rarr; `CodeAfterIfSkipped`** (misconception)

- **Exact edge logic (the wrong rule):** When the then branch runs, the code after the if is skipped.
- **Twin logic (the right rule):** After the if finishes, execution continues with the next statement either way.
- **Role:** context

**6. `control_flow` &rarr; `FalseConditionRestartsProgram`** (misconception)

- **Exact edge logic (the wrong rule):** When an if condition is false (and there is no else), control jumps back to the start of the program.
- **Twin logic (the right rule):** A false condition skips the then branch and execution continues with the statement after the if statement.
- **Role:** context

**7. `control_flow` &rarr; `FalseLoopRepeatsNextCode`** (misconception)

- **Exact edge logic (the wrong rule):** A loop is an iterative if-else: while the condition is true the body repeats, and when it is false the code after the loop repeats.
- **Twin logic (the right rule):** Only the body is repeated; once the condition is false the code after the loop runs once.
- **Role:** context

**8. `control_flow` &rarr; `IfConditionWatched`** (misconception)

- **Exact edge logic (the wrong rule):** An if statement watches its condition while the program runs and fires as soon as the condition becomes true (if = whenever).
- **Twin logic (the right rule):** An if condition is tested once, when control reaches the if statement; later changes to the variables do not trigger the branch.
- **Role:** context

**9. `control_flow` &rarr; `IfWaitsForCondition`** (misconception)

- **Exact edge logic (the wrong rule):** An IF statement earlier in the program stays active and fires later, e.g. inside a later loop, when its condition becomes true.
- **Twin logic (the right rule):** An if is evaluated once when control reaches it; afterwards it is inactive unless control returns to it.
- **Role:** context

**10. `control_flow` &rarr; `LoopImpliedByOneTest`** (misconception)

- **Exact edge logic (the wrong rule):** Testing one case is enough; Java will repeat the test for the other values by itself.
- **Twin logic (the right rule):** A statement runs once each time control reaches it; repeating a test for many values needs a loop.
- **Role:** context

**11. `control_flow` &rarr; `NoShortCircuit`** (misconception)

- **Exact edge logic (the wrong rule):** logical AND/OR always evaluate both sides (Java short-circuits them)
- **Twin logic (the right rule):** In p &amp;&amp; q, q is evaluated only when p is true; in p \|\| q, q is evaluated only when p is false.
- **Role:** context

**12. `control_flow` &rarr; `ProgramEndsAfterLoop`** (misconception)

- **Exact edge logic (the wrong rule):** When a loop finishes the program ends, so code after the loop never runs.
- **Twin logic (the right rule):** When the loop condition becomes false, control continues with the first statement after the loop.
- **Role:** context

**13. `control_flow` &rarr; `ProgramLooksAhead`** (misconception)

- **Exact edge logic (the wrong rule):** The program knows or sees what later lines will do and acts on those goals at the current line, e.g. it stops 'at ten' because it wants to draw a box.
- **Twin logic (the right rule):** Each statement executes using only the current state; later lines have no effect until control reaches them.
- **Role:** primary

**14. `control_flow` &rarr; `ReturnDoesNotExitLoop`** (misconception)

- **Exact edge logic (the wrong rule):** A return inside a loop does not end the loop; it sets a value each pass (the last one is returned) or returns several values.
- **Twin logic (the right rule):** When return executes, the method ends at once, so the loop stops on that pass.
- **Role:** primary

**15. `control_flow` &rarr; `StatementsRunInAnyOrder`** (misconception)

- **Exact edge logic (the wrong rule):** Statements in a program can run in any order.
- **Twin logic (the right rule):** Without control statements, statements run once each, top to bottom.
- **Role:** primary

**16. `flag_search_loop` &rarr; `ReturnDoesNotExitLoop`** (misconception)

- **Exact edge logic (the wrong rule):** A return inside a loop does not end the loop; it sets a value each pass (the last one is returned) or returns several values.
- **Twin logic (the right rule):** When return executes, the method ends at once, so the loop stops on that pass.
- **Role:** context

**17. `for_loop` &rarr; `FalseLoopRepeatsNextCode`** (misconception)

- **Exact edge logic (the wrong rule):** A loop is an iterative if-else: while the condition is true the body repeats, and when it is false the code after the loop repeats.
- **Twin logic (the right rule):** Only the body is repeated; once the condition is false the code after the loop runs once.
- **Role:** primary

**18. `for_loop` &rarr; `LoopImpliedByOneTest`** (misconception)

- **Exact edge logic (the wrong rule):** Testing one case is enough; Java will repeat the test for the other values by itself.
- **Twin logic (the right rule):** A statement runs once each time control reaches it; repeating a test for many values needs a loop.
- **Role:** context

**19. `for_loop` &rarr; `ProgramEndsAfterLoop`** (misconception)

- **Exact edge logic (the wrong rule):** When a loop finishes the program ends, so code after the loop never runs.
- **Twin logic (the right rule):** When the loop condition becomes false, control continues with the first statement after the loop.
- **Role:** context

**20. `for_loop` &rarr; `ReturnDoesNotExitLoop`** (misconception)

- **Exact edge logic (the wrong rule):** A return inside a loop does not end the loop; it sets a value each pass (the last one is returned) or returns several values.
- **Twin logic (the right rule):** When return executes, the method ends at once, so the loop stops on that pass.
- **Role:** context

**21. `if_statement` &rarr; `CodeAfterIfSkipped`** (misconception)

- **Exact edge logic (the wrong rule):** When the then branch runs, the code after the if is skipped.
- **Twin logic (the right rule):** After the if finishes, execution continues with the next statement either way.
- **Role:** primary

**22. `if_statement` &rarr; `FalseConditionRestartsProgram`** (misconception)

- **Exact edge logic (the wrong rule):** When an if condition is false (and there is no else), control jumps back to the start of the program.
- **Twin logic (the right rule):** A false condition skips the then branch and execution continues with the statement after the if statement.
- **Role:** primary

**23. `if_statement` &rarr; `IfConditionWatched`** (misconception)

- **Exact edge logic (the wrong rule):** An if statement watches its condition while the program runs and fires as soon as the condition becomes true (if = whenever).
- **Twin logic (the right rule):** An if condition is tested once, when control reaches the if statement; later changes to the variables do not trigger the branch.
- **Role:** primary

**24. `if_statement` &rarr; `IfWaitsForCondition`** (misconception)

- **Exact edge logic (the wrong rule):** An IF statement earlier in the program stays active and fires later, e.g. inside a later loop, when its condition becomes true.
- **Twin logic (the right rule):** An if is evaluated once when control reaches it; afterwards it is inactive unless control returns to it.
- **Role:** primary

**25. `if_statement` &rarr; `ProgramLooksAhead`** (misconception)

- **Exact edge logic (the wrong rule):** The program knows or sees what later lines will do and acts on those goals at the current line, e.g. it stops 'at ten' because it wants to draw a box.
- **Twin logic (the right rule):** Each statement executes using only the current state; later lines have no effect until control reaches them.
- **Role:** context

**26. `short_circuit` &rarr; `NoShortCircuit`** (misconception)

- **Exact edge logic (the wrong rule):** In p &amp;&amp; q, both p and q are always evaluated.
- **Twin logic (the right rule):** In p &amp;&amp; q, q is evaluated only when p is true; in p \|\| q, q is evaluated only when p is false.
- **Role:** primary

**27. `statement` &rarr; `ProgramLooksAhead`** (misconception)

- **Exact edge logic (the wrong rule):** The program knows or sees what later lines will do and acts on those goals at the current line, e.g. it stops 'at ten' because it wants to draw a box.
- **Twin logic (the right rule):** Each statement executes using only the current state; later lines have no effect until control reaches them.
- **Role:** context

**28. `statement` &rarr; `StatementsRunInAnyOrder`** (misconception)

- **Exact edge logic (the wrong rule):** Statements in a program can run in any order.
- **Twin logic (the right rule):** Without control statements, statements run once each, top to bottom.
- **Role:** context

**29. `while_loop` &rarr; `FalseLoopRepeatsNextCode`** (misconception)

- **Exact edge logic (the wrong rule):** A loop is an iterative if-else: while the condition is true the body repeats, and when it is false the code after the loop repeats.
- **Twin logic (the right rule):** Only the body is repeated; once the condition is false the code after the loop runs once.
- **Role:** context

**30. `while_loop` &rarr; `LoopImpliedByOneTest`** (misconception)

- **Exact edge logic (the wrong rule):** Testing one case is enough; Java will repeat the test for the other values by itself.
- **Twin logic (the right rule):** A statement runs once each time control reaches it; repeating a test for many values needs a loop.
- **Role:** primary

**31. `while_loop` &rarr; `ProgramEndsAfterLoop`** (misconception)

- **Exact edge logic (the wrong rule):** When a loop finishes the program ends, so code after the loop never runs.
- **Twin logic (the right rule):** When the loop condition becomes false, control continues with the first statement after the loop.
- **Role:** primary

**32. `control_flow` &rarr; `control_flow@L0`** (has_level)

- **Exact edge logic:** control flow -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (12 ways).
  - **[0] everyday\_reading** (rule type E, folk-meaning rule): Folk meaning: in everyday instructions a listener reads the whole list at once, does steps in a sensible order and infers what the writer wants. Java instead executes statements one at a time, top to bottom, each only when control reaches it, and nothing later in the program has any effect earlier.
  - **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `StatementsRunInAnyOrder`: wrong rule: Statements in a program can run in any order. Right rule: Without control statements, statements run once each, top to bottom.
  - **[2] misconception** (rule type M, wrong rule / right rule) &rarr; `ProgramLooksAhead`: wrong rule: The program knows or sees what later lines will do and acts on those goals at the current line, e.g. it stops 'at ten' because it wants to draw a box. Right rule: Each statement executes using only the current state; later lines have no effect until control reaches them.
  - **[3] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `StatementsRunInAnyOrder`: Applies the sequencing rule (LT) unevenly: e.g. runs a later line before an earlier one, lets an if that was already passed fire again later, or ends the program when a loop or a false if ends instead of continuing with the next statement. (here mixing in: "Statements in a program can run in any order")
  - **[4] misconception** (rule type M, wrong rule / right rule) &rarr; `CodeAfterIfSkipped`: wrong rule: When the then branch runs, the code after the if is skipped. Right rule: After the if finishes, execution continues with the next statement either way.
  - **[5] misconception** (rule type M, wrong rule / right rule) &rarr; `NoShortCircuit`: wrong rule: logical AND/OR always evaluate both sides (Java short-circuits them). Right rule: In p &amp;&amp; q, q is evaluated only when p is true; in p \|\| q, q is evaluated only when p is false.
  - **[6] misconception** (rule type M, wrong rule / right rule) &rarr; `LoopImpliedByOneTest`: wrong rule: Testing one case is enough; Java will repeat the test for the other values by itself. Right rule: A statement runs once each time control reaches it; repeating a test for many values needs a loop.
  - **[7] misconception** (rule type M, wrong rule / right rule) &rarr; `IfWaitsForCondition`: wrong rule: An IF statement earlier in the program stays active and fires later, e.g. inside a later loop, when its condition becomes true. Right rule: An if is evaluated once when control reaches it; afterwards it is inactive unless control returns to it.
  - **[8] misconception** (rule type M, wrong rule / right rule) &rarr; `FalseConditionRestartsProgram`: wrong rule: When an if condition is false (and there is no else), control jumps back to the start of the program. Right rule: A false condition skips the then branch and execution continues with the statement after the if statement.
  - **[9] misconception** (rule type M, wrong rule / right rule) &rarr; `IfConditionWatched`: wrong rule: An if statement watches its condition while the program runs and fires as soon as the condition becomes true (if = whenever). Right rule: An if condition is tested once, when control reaches the if statement; later changes to the variables do not trigger the branch.
  - **[10] misconception** (rule type M, wrong rule / right rule) &rarr; `ProgramEndsAfterLoop`: wrong rule: When a loop finishes the program ends, so code after the loop never runs. Right rule: When the loop condition becomes false, control continues with the first statement after the loop.
  - **[11] misconception** (rule type M, wrong rule / right rule) &rarr; `FalseLoopRepeatsNextCode`: wrong rule: A loop is an iterative if-else: while the condition is true the body repeats, and when it is false the code after the loop repeats. Right rule: Only the body is repeated; once the condition is false the code after the loop runs once.

**33. `control_flow` &rarr; `control_flow@L1`** (has_level)

- **Exact edge logic:** control flow -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).
  - **[0] names\_the\_element** (rule type N, identity rule): Control flow is the order in which a program's statements are executed (statement sequencing); conditionals and loops are the statements that change it.
  - **[1] states\_the\_rule** (rule type S, declarative rule): Without control statements every statement executes once, in the order given; a block executes its statements in order from first to last; if/if-else choose between one or two alternatives and loops repeat statements depending on a condition.

**34. `control_flow` &rarr; `control_flow@L2`** (has_level)

- **Exact edge logic:** control flow -&gt; L2 (Multistructural): the answer applies the rules of control flow to every part of the code, in order (3 ways).
  - **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): Execute the statement at the current point; when it completes normally, control passes to the next statement in the block. An if evaluates its condition once and then runs at most one branch; a loop evaluates its condition before each pass; after an if or a loop finishes, control continues with the statement after it.
  - **[1] output\_prediction** (rule type OP, evaluation / result rule): The output is the sequence of print statements that control actually reaches, in the order reached: e.g. TenHellos prints 1st, 2nd, 3rd Hello once each, then 4th to 10th Hello from the loop.
  - **[2] one\_step\_execution** (rule type OS, state-transition rule): One step executes the single statement at the current control point using the current values, updates at most the variables it assigns, and moves the control point to the next statement (or, for an if/loop test, to the chosen branch, back to the test, or past the statement).

**35. `control_flow` &rarr; `control_flow@L3`** (has_level)

- **Exact edge logic:** control flow -&gt; L3 (Relational): the answer relates the parts (4 ways).
  - **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Control flow is defined over statements: statements are executed for their effect, and if/while/for are themselves statements that may be used wherever a statement is allowed, so they can nest.
  - **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): An if changes the default top-to-bottom flow: its condition is tested once when control reaches it, its block runs only if true, and in both cases control then continues with the next statement.
  - **[2] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): A flowchart draws control flow: each path through the diagram is a possible path of execution, with a decision box for each if or loop test.
  - **[3] purpose\_of\_the\_whole** (rule type P, plan / role rule): Plan: control flow lets one program do different things for different inputs (selection) and do a thing many times (repetition), so a short program can specify a potentially unlimited number of executed statements.

**36. `control_flow` &rarr; `control_flow@L4`** (has_level)

- **Exact edge logic:** control flow -&gt; L4 (Extended abstract): the answer reasons beyond the given code (4 ways).
  - **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `StatementsRunInAnyOrder`: Reordering two statements generally changes the result whenever one reads a variable that the other writes (e.g. swapping x = x + 1 and print(x)); reordering is safe only for statements that touch disjoint variables. Moving a statement into or out of a branch or loop body changes how many times it runs (0, 1 or n).
  - **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Reason in terms of control flow whenever you must predict output or find why a statement did or did not run: trace which statement is reached next. Straight-line sequence suffices only when every input needs the same steps exactly once; otherwise add a conditional or a loop.
  - **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: A local variable must be definitely assigned on every control-flow path before it is read. Kind: compile-time. Trigger class: A variable assigned only inside an if branch (or only in a loop body) and read after it: the compiler reports 'variable might not have been initialized'.
  - **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: Statements run in the order written, so an update must come before the statement that needs the new value. Kind: silent logic error. Trigger class: Swapping two dependent statements (e.g. printing before updating, or incrementing the index before using it): output is shifted or off by one pass, with no error.

**37. `topic1.3.a` &rarr; `control_flow`** (contains)

- topic `topic1.3.a` contains `control_flow`

**38. `topic1.3.a` &rarr; `algorithm_pseudocode`** (contains)

- topic `topic1.3.a` contains `algorithm_pseudocode`

**39. `topic1.3.a` &rarr; `flowchart`** (contains)

- topic `topic1.3.a` contains `flowchart`
