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

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 39 edges around this concept, each explained in the graph's own words.

## What it needs first (1)

A prerequisite edge means the other concept has to be understood before `control_flow`.

### `statement` comes before `control_flow`

*one step, terminated by ;, executed in sequence*

Control flow is the order in which statements run.

- **Grounding:** book passage
- **How `control_flow` combines with `statement`:** Control flow is defined over statements: statements are executed for their effect, and if/while/for are themselves statements that may be used wherever a statement is allowed, so they can nest.
- **How `statement` combines with `control_flow`:** Control flow is the order in which statements run; without control statements it is straight-line, each once in order.

## What it leads to (3)

These concepts need `control_flow` first.

### `control_flow` comes before `flowchart`

*Flowchart: a diagram whose paths correspond to the flow-of-control paths through a program*

A flowchart draws the flow of control: each path through the diagram is a path the program can take.

- **Grounding:** book passage
- **How `control_flow` combines with `flowchart`:** A flowchart draws control flow: each path through the diagram is a possible path of execution, with a decision box for each if or loop test.
- **How `flowchart` combines with `control_flow`:** The flowchart's arrows are the program's control flow: sequence = a straight chain, if = branch and rejoin, loop = a back arrow to the test. Nesting a loop draws a loop inside a loop, and the diagram quickly becomes complex.

### `control_flow` comes before `if_statement`

*run a block only when the condition holds*

An if changes the default top-to-bottom flow by running a block only when its condition is true.

- **Grounding:** book passage
- **How `control_flow` combines with `if_statement`:** An if changes the default top-to-bottom flow: its condition is tested once when control reaches it, its block runs only if true, and in both cases control then continues with the next statement.
- **How `if_statement` combines with `control_flow`:** An if is a fork in the control flow: one path through the body, one around it, both rejoining at the next statement.

### `control_flow` comes before `switch_statement`

*switch (x) { case v: ...; break; default: ... }*

switch directs the flow of control to one of several case labels, depending on the value of one expression.

- **Grounding:** book passage

## Learned alongside (0)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

No parallel edge touches this concept.

## Misconceptions (11)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### CodeAfterIfSkipped

- **Wrong rule:** When the then branch runs, the code after the if is skipped.
- **Right rule:** After the if finishes, execution continues with the next statement either way.
- **Role of this concept:** context
- **Shows at level L0 as:** misconception: wrong rule: When the then branch runs, the code after the if is skipped. Right rule: After the if finishes, execution continues with the next statement either way.
- **Also an edge from `if_statement`:** When the then branch runs, the code after the if is skipped.

### FalseConditionRestartsProgram

- **Wrong rule:** When an if condition is false (and there is no else), control jumps back to the start of the program.
- **Right rule:** A false condition skips the then branch and execution continues with the statement after the if statement.
- **Role of this concept:** context
- **Shows at level L0 as:** misconception: wrong rule: When an if condition is false (and there is no else), control jumps back to the start of the program. Right rule: A false condition skips the then branch and execution continues with the statement after the if statement.
- **Also an edge from `if_statement`:** When an if condition is false (and there is no else), control jumps back to the start of the program.

### FalseLoopRepeatsNextCode

- **Wrong rule:** A loop is an iterative if-else: while the condition is true the body repeats, and when it is false the code after the loop repeats.
- **Right rule:** Only the body is repeated; once the condition is false the code after the loop runs once.
- **Role of this concept:** context
- **Shows at level L0 as:** misconception: wrong rule: A loop is an iterative if-else: while the condition is true the body repeats, and when it is false the code after the loop repeats. Right rule: Only the body is repeated; once the condition is false the code after the loop runs once.
- **Also an edge from `for_loop`:** A loop is an iterative if-else: while the condition is true the body repeats, and when it is false the code after the loop repeats.
- **Also an edge from `while_loop`:** A loop is an iterative if-else: while the condition is true the body repeats, and when it is false the code after the loop repeats.

### IfConditionWatched

- **Wrong rule:** An if statement watches its condition while the program runs and fires as soon as the condition becomes true (if = whenever).
- **Right rule:** An if condition is tested once, when control reaches the if statement; later changes to the variables do not trigger the branch.
- **Role of this concept:** context
- **Shows at level L0 as:** misconception: wrong rule: An if statement watches its condition while the program runs and fires as soon as the condition becomes true (if = whenever). Right rule: An if condition is tested once, when control reaches the if statement; later changes to the variables do not trigger the branch.
- **Also an edge from `if_statement`:** An if statement watches its condition while the program runs and fires as soon as the condition becomes true (if = whenever).

### IfWaitsForCondition

- **Wrong rule:** An IF statement earlier in the program stays active and fires later, e.g. inside a later loop, when its condition becomes true.
- **Right rule:** An if is evaluated once when control reaches it; afterwards it is inactive unless control returns to it.
- **Role of this concept:** context
- **Shows at level L0 as:** misconception: wrong rule: An IF statement earlier in the program stays active and fires later, e.g. inside a later loop, when its condition becomes true. Right rule: An if is evaluated once when control reaches it; afterwards it is inactive unless control returns to it.
- **Also an edge from `if_statement`:** An IF statement earlier in the program stays active and fires later, e.g. inside a later loop, when its condition becomes true.

### LoopImpliedByOneTest

- **Wrong rule:** Testing one case is enough; Java will repeat the test for the other values by itself.
- **Right rule:** A statement runs once each time control reaches it; repeating a test for many values needs a loop.
- **Role of this concept:** context
- **Shows at level L0 as:** misconception: wrong rule: Testing one case is enough; Java will repeat the test for the other values by itself. Right rule: A statement runs once each time control reaches it; repeating a test for many values needs a loop.
- **Also an edge from `for_loop`:** Testing one case is enough; Java will repeat the test for the other values by itself.
- **Also an edge from `while_loop`:** Testing one case is enough; Java will repeat the test for the other values by itself.

### NoShortCircuit

- **Wrong rule:** logical AND/OR always evaluate both sides (Java short-circuits them)
- **Right rule:** In p &amp;&amp; q, q is evaluated only when p is true; in p \|\| q, q is evaluated only when p is false.
- **Role of this concept:** context
- **Shows at level L0 as:** misconception: wrong rule: logical AND/OR always evaluate both sides (Java short-circuits them). Right rule: In p &amp;&amp; q, q is evaluated only when p is true; in p \|\| q, q is evaluated only when p is false.
- **Also an edge from `short_circuit`:** In p &amp;&amp; q, both p and q are always evaluated.

### ProgramEndsAfterLoop

- **Wrong rule:** When a loop finishes the program ends, so code after the loop never runs.
- **Right rule:** When the loop condition becomes false, control continues with the first statement after the loop.
- **Role of this concept:** context
- **Shows at level L0 as:** misconception: wrong rule: When a loop finishes the program ends, so code after the loop never runs. Right rule: When the loop condition becomes false, control continues with the first statement after the loop.
- **Also an edge from `for_loop`:** When a loop finishes the program ends, so code after the loop never runs.
- **Also an edge from `while_loop`:** When a loop finishes the program ends, so code after the loop never runs.

### ProgramLooksAhead

- **Wrong rule:** The program knows or sees what later lines will do and acts on those goals at the current line, e.g. it stops 'at ten' because it wants to draw a box.
- **Right rule:** Each statement executes using only the current state; later lines have no effect until control reaches them.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: The program knows or sees what later lines will do and acts on those goals at the current line, e.g. it stops 'at ten' because it wants to draw a box. Right rule: Each statement executes using only the current state; later lines have no effect until control reaches them.
- **Also an edge from `if_statement`:** The program knows or sees what later lines will do and acts on those goals at the current line, e.g. it stops 'at ten' because it wants to draw a box.
- **Also an edge from `statement`:** The program knows or sees what later lines will do and acts on those goals at the current line, e.g. it stops 'at ten' because it wants to draw a box.

### ReturnDoesNotExitLoop

- **Wrong rule:** A return inside a loop does not end the loop; it sets a value each pass (the last one is returned) or returns several values.
- **Right rule:** When return executes, the method ends at once, so the loop stops on that pass.
- **Role of this concept:** primary
- **Also an edge from `flag_search_loop`:** A return inside a loop does not end the loop; it sets a value each pass (the last one is returned) or returns several values.
- **Also an edge from `for_loop`:** A return inside a loop does not end the loop; it sets a value each pass (the last one is returned) or returns several values.

### StatementsRunInAnyOrder

- **Wrong rule:** Statements in a program can run in any order.
- **Right rule:** Without control statements, statements run once each, top to bottom.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: Statements in a program can run in any order. Right rule: Without control statements, statements run once each, top to bottom.
- **Shows at level L0 as:** inconsistent trace: Applies the sequencing rule (LT) unevenly: e.g. runs a later line before an earlier one, lets an if that was already passed fire again later, or ends the program when a loop or a false if ends instead of continuing with the next statement. (here mixing in: "Statements in a program can run in any order")
- **Also an edge from `statement`:** Statements in a program can run in any order.

## Errors (0)

An error edge states the rule that gets broken in a program, and the right rule.

The graph has no error edge from this concept.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for control flow: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to control flow agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

control flow -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (12 ways).

- **everyday reading** (folk-meaning rule): Folk meaning: in everyday instructions a listener reads the whole list at once, does steps in a sensible order and infers what the writer wants. Java instead executes statements one at a time, top to bottom, each only when control reaches it, and nothing later in the program has any effect earlier.
- **misconception** (wrong rule / right rule; shows `StatementsRunInAnyOrder`): wrong rule: Statements in a program can run in any order. Right rule: Without control statements, statements run once each, top to bottom.
- **misconception** (wrong rule / right rule; shows `ProgramLooksAhead`): wrong rule: The program knows or sees what later lines will do and acts on those goals at the current line, e.g. it stops 'at ten' because it wants to draw a box. Right rule: Each statement executes using only the current state; later lines have no effect until control reaches them.
- **inconsistent trace** (uneven-application rule; shows `StatementsRunInAnyOrder`): Applies the sequencing rule (LT) unevenly: e.g. runs a later line before an earlier one, lets an if that was already passed fire again later, or ends the program when a loop or a false if ends instead of continuing with the next statement. (here mixing in: "Statements in a program can run in any order")
- **misconception** (wrong rule / right rule; shows `CodeAfterIfSkipped`): wrong rule: When the then branch runs, the code after the if is skipped. Right rule: After the if finishes, execution continues with the next statement either way.
- **misconception** (wrong rule / right rule; shows `NoShortCircuit`): wrong rule: logical AND/OR always evaluate both sides (Java short-circuits them). Right rule: In p &amp;&amp; q, q is evaluated only when p is true; in p \|\| q, q is evaluated only when p is false.
- **misconception** (wrong rule / right rule; shows `LoopImpliedByOneTest`): wrong rule: Testing one case is enough; Java will repeat the test for the other values by itself. Right rule: A statement runs once each time control reaches it; repeating a test for many values needs a loop.
- **misconception** (wrong rule / right rule; shows `IfWaitsForCondition`): wrong rule: An IF statement earlier in the program stays active and fires later, e.g. inside a later loop, when its condition becomes true. Right rule: An if is evaluated once when control reaches it; afterwards it is inactive unless control returns to it.
- **misconception** (wrong rule / right rule; shows `FalseConditionRestartsProgram`): wrong rule: When an if condition is false (and there is no else), control jumps back to the start of the program. Right rule: A false condition skips the then branch and execution continues with the statement after the if statement.
- **misconception** (wrong rule / right rule; shows `IfConditionWatched`): wrong rule: An if statement watches its condition while the program runs and fires as soon as the condition becomes true (if = whenever). Right rule: An if condition is tested once, when control reaches the if statement; later changes to the variables do not trigger the branch.
- **misconception** (wrong rule / right rule; shows `ProgramEndsAfterLoop`): wrong rule: When a loop finishes the program ends, so code after the loop never runs. Right rule: When the loop condition becomes false, control continues with the first statement after the loop.
- **misconception** (wrong rule / right rule; shows `FalseLoopRepeatsNextCode`): wrong rule: A loop is an iterative if-else: while the condition is true the body repeats, and when it is false the code after the loop repeats. Right rule: Only the body is repeated; once the condition is false the code after the loop runs once.

### L1: Unistructural / atom x text surface

L1 for control flow: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

control flow -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

- **names the element** (identity rule): Control flow is the order in which a program's statements are executed (statement sequencing); conditionals and loops are the statements that change it.
- **states the rule** (declarative rule): Without control statements every statement executes once, in the order given; a block executes its statements in order from first to last; if/if-else choose between one or two alternatives and loops repeat statements depending on a condition.

### L2: Multistructural / block x execution / preoperational

L2 for control flow: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

control flow -&gt; L2 (Multistructural): the answer applies the rules of control flow to every part of the code, in order (3 ways).

- **line by line trace** (operational sequencing rule): Execute the statement at the current point; when it completes normally, control passes to the next statement in the block. An if evaluates its condition once and then runs at most one branch; a loop evaluates its condition before each pass; after an if or a loop finishes, control continues with the statement after it.
- **output prediction** (evaluation / result rule): The output is the sequence of print statements that control actually reaches, in the order reached: e.g. TenHellos prints 1st, 2nd, 3rd Hello once each, then 4th to 10th Hello from the loop.
- **one step execution** (state-transition rule): One step executes the single statement at the current control point using the current values, updates at most the variables it assigns, and moves the control point to the next statement (or, for an if/loop test, to the chosen branch, back to the test, or past the statement).

### L3: Relational / relations x function (concrete operational begins)

L3 for control flow: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

control flow -&gt; L3 (Relational): the answer relates the parts (4 ways).

- **relation to neighbour** (composition rule (with a neighbour)): Control flow is defined over statements: statements are executed for their effect, and if/while/for are themselves statements that may be used wherever a statement is allowed, so they can nest.
- **relation to neighbour** (composition rule (with a neighbour)): An if changes the default top-to-bottom flow: its condition is tested once when control reaches it, its block runs only if true, and in both cases control then continues with the next statement.
- **relation to neighbour** (composition rule (with a neighbour)): A flowchart draws control flow: each path through the diagram is a possible path of execution, with a decision box for each if or loop test.
- **purpose of the whole** (plan / role rule): Plan: control flow lets one program do different things for different inputs (selection) and do a thing many times (repetition), so a short program can specify a potentially unlimited number of executed statements.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for control flow: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

control flow -&gt; L4 (Extended abstract): the answer reasons beyond the given code (4 ways).

- **predict a change** (conservation rule; shows `StatementsRunInAnyOrder`): Reordering two statements generally changes the result whenever one reads a variable that the other writes (e.g. swapping x = x + 1 and print(x)); reordering is safe only for statements that touch disjoint variables. Moving a statement into or out of a branch or loop body changes how many times it runs (0, 1 or n).
- **transfer to a new program** (applicability rule): Reason in terms of control flow whenever you must predict output or find why a statement did or did not run: trace which statement is reached next. Straight-line sequence suffices only when every input needs the same steps exactly once; otherwise add a conditional or a loop.
- **diagnose an error** (error rule): rule broken: A local variable must be definitely assigned on every control-flow path before it is read. Kind: compile-time. Trigger class: A variable assigned only inside an if branch (or only in a loop body) and read after it: the compiler reports 'variable might not have been initialized'.
- **diagnose an error** (error rule): rule broken: Statements run in the order written, so an update must come before the statement that needs the new value. Kind: silent logic error. Trigger class: Swapping two dependent statements (e.g. printing before updating, or incrementing the index before using it): output is shifted or off by one pass, with no error.

## Same topic

`control_flow` belongs to the topic **Control flow** (`topic1.3.a`). The topic also contains: `algorithm_pseudocode`, `flowchart`.

## Rules of the concept (25)

- **folk-meaning rule:** Folk meaning: in everyday instructions a listener reads the whole list at once, does steps in a sensible order and infers what the writer wants. Java instead executes statements one at a time, top to bottom, each only when control reaches it, and nothing later in the program has any effect earlier.
- **wrong rule / right rule:** CodeAfterIfSkipped: wrong: When the then branch runs, the code after the if is skipped. \| right: After the if finishes, execution continues with the next statement either way.
- **wrong rule / right rule:** NoShortCircuit: wrong: logical AND/OR always evaluate both sides (Java short-circuits them) \| right: In p &amp;&amp; q, q is evaluated only when p is true; in p \|\| q, q is evaluated only when p is false.
- **wrong rule / right rule:** StatementsRunInAnyOrder: wrong: Statements in a program can run in any order. \| right: Without control statements, statements run once each, top to bottom.
- **wrong rule / right rule:** LoopImpliedByOneTest: wrong: Testing one case is enough; Java will repeat the test for the other values by itself. \| right: A statement runs once each time control reaches it; repeating a test for many values needs a loop.
- **wrong rule / right rule:** IfWaitsForCondition: wrong: An IF statement earlier in the program stays active and fires later, e.g. inside a later loop, when its condition becomes true. \| right: An if is evaluated once when control reaches it; afterwards it is inactive unless control returns to it.
- **wrong rule / right rule:** ProgramLooksAhead: wrong: The program knows or sees what later lines will do and acts on those goals at the current line, e.g. it stops 'at ten' because it wants to draw a box. \| right: Each statement executes using only the current state; later lines have no effect until control reaches them.
- **wrong rule / right rule:** FalseConditionRestartsProgram: wrong: When an if condition is false (and there is no else), control jumps back to the start of the program. \| right: A false condition skips the then branch and execution continues with the statement after the if statement.
- **wrong rule / right rule:** IfConditionWatched: wrong: An if statement watches its condition while the program runs and fires as soon as the condition becomes true (if = whenever). \| right: An if condition is tested once, when control reaches the if statement; later changes to the variables do not trigger the branch.
- **wrong rule / right rule:** ProgramEndsAfterLoop: wrong: When a loop finishes the program ends, so code after the loop never runs. \| right: When the loop condition becomes false, control continues with the first statement after the loop.
- **wrong rule / right rule:** FalseLoopRepeatsNextCode: wrong: A loop is an iterative if-else: while the condition is true the body repeats, and when it is false the code after the loop repeats. \| right: Only the body is repeated; once the condition is false the code after the loop runs once.
- **uneven-application rule:** Applies the sequencing rule (LT) unevenly: e.g. runs a later line before an earlier one, lets an if that was already passed fire again later, or ends the program when a loop or a false if ends instead of continuing with the next statement.
- **identity rule:** Control flow is the order in which a program's statements are executed (statement sequencing); conditionals and loops are the statements that change it.
- **declarative rule:** Without control statements every statement executes once, in the order given; a block executes its statements in order from first to last; if/if-else choose between one or two alternatives and loops repeat statements depending on a condition.
- **operational sequencing rule:** Execute the statement at the current point; when it completes normally, control passes to the next statement in the block. An if evaluates its condition once and then runs at most one branch; a loop evaluates its condition before each pass; after an if or a loop finishes, control continues with the statement after it.
- **evaluation / result rule:** The output is the sequence of print statements that control actually reaches, in the order reached: e.g. TenHellos prints 1st, 2nd, 3rd Hello once each, then 4th to 10th Hello from the loop.
- **state-transition rule:** One step executes the single statement at the current control point using the current values, updates at most the variables it assigns, and moves the control point to the next statement (or, for an if/loop test, to the chosen branch, back to the test, or past the statement).
- **composition rule (with a neighbour):** with statement: Control flow is defined over statements: statements are executed for their effect, and if/while/for are themselves statements that may be used wherever a statement is allowed, so they can nest.
- **composition rule (with a neighbour):** with if\_statement: An if changes the default top-to-bottom flow: its condition is tested once when control reaches it, its block runs only if true, and in both cases control then continues with the next statement.
- **composition rule (with a neighbour):** with flowchart: A flowchart draws control flow: each path through the diagram is a possible path of execution, with a decision box for each if or loop test.
- **plan / role rule:** Plan: control flow lets one program do different things for different inputs (selection) and do a thing many times (repetition), so a short program can specify a potentially unlimited number of executed statements.
- **conservation rule:** Reordering two statements generally changes the result whenever one reads a variable that the other writes (e.g. swapping x = x + 1 and print(x)); reordering is safe only for statements that touch disjoint variables. Moving a statement into or out of a branch or loop body changes how many times it runs (0, 1 or n).
- **error rule:** rule broken: A local variable must be definitely assigned on every control-flow path before it is read. (compile-time)
- **error rule:** rule broken: Statements run in the order written, so an update must come before the statement that needs the new value. (silent logic error)
- **applicability rule:** Reason in terms of control flow whenever you must predict output or find why a statement did or did not run: trace which statement is reached next. Straight-line sequence suffices only when every input needs the same steps exactly once; otherwise add a conditional or a loop.

## The whole prerequisite chain

- **Everything it builds on (4):** `class_declaration`, `main_method`, `program_text`, `statement`
- **Everything that builds on it (8):** `conditional_operator`, `dangling_else`, `else_if_chain`, `flowchart`, `if_else_statement`, `if_statement`, `nested_conditionals`, `switch_statement`
