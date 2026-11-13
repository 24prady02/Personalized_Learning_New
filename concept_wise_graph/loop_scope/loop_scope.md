# loop_scope (`loop_scope`)

lifetime/scope of variables in/around the loop

Section 1.3 Conditionals and Loops, topic 1.3.d For loops (including i++ and scope).

![The knowledge graph around loop_scope](loop_scope.png)

## At a glance

- **Needs first:** `for_loop`
- **Leads to:** nothing
- **Learned alongside:** nothing
- **Misconceptions:** `ForVariableScopeBeyondLoop`, `LocalVarOutsideScope`, `LoopBodyScopeImpliesLoopLifetime`, `LoopVariableLifetimeScope`
- **Errors:** `AccumulatorDeclaredInLoop`
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 26 edges around this concept. The edge logic, the wrong and right rules and the exact rules of the ways are copied word for word from the graph.

## To work on (1)

- no aliases: a student's words cannot name this concept

## What it needs first (1)

A prerequisite edge means the other concept has to be understood before `loop_scope`.

### `for_loop` comes before `loop_scope`

*a while with init/condition/update packaged together*

- **Edge:** `pre:for_loop->loop_scope`
- **Exact edge logic:** A variable declared in the for header exists only from its declaration to the end of the for statement's block.
- **Grounding:** book\_passage
- **Composition rule (R) of `loop_scope` with `for_loop`:** A variable declared in the for header exists only from its declaration to the end of the for statement, so for and while versions differ: in the while version the counter is still available after the loop.
- **Composition rule (R) of `for_loop` with `loop_scope`:** A variable declared in the for header is in scope only in the header and the body, so it cannot be used after the loop.

## What it leads to (0)

These concepts need `loop_scope` first.

No concept has this one as a prerequisite.

## Learned alongside (0)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

No parallel edge touches this concept.

## Misconceptions (4)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### ForVariableScopeBeyondLoop

- **Edge:** `loop_scope` &rarr; `ForVariableScopeBeyondLoop` (misconception)
- **Exact edge logic (the wrong rule):** i declared in the for header can still be used after the loop has ended.
- **Twin logic (the right rule):** i declared in the for header exists only inside the loop, so using it after the loop does not compile.
- **Wrong belief (on the node):** i declared in the for header can still be used after the loop has ended.
- **Correct rule (on the node):** i declared in the for header exists only inside the loop, so using it after the loop does not compile.
- **Provenance:** published
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [3] misconception, exact rule:** wrong rule: i declared in the for header can still be used after the loop has ended. Right rule: i declared in the for header exists only inside the loop, so using it after the loop does not compile.

### LocalVarOutsideScope

- **Edge:** `loop_scope` &rarr; `LocalVarOutsideScope` (misconception)
- **Exact edge logic (the wrong rule):** A variable declared inside a block can be used anywhere in the program, like a global.
- **Twin logic (the right rule):** A local variable exists only from its declaration to the end of its block.
- **Wrong belief (on the node):** A variable declared inside a block can be used anywhere in the program, like a global.
- **Correct rule (on the node):** A local variable exists only from its declaration to the end of its block.
- **Provenance:** published
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [4] misconception, exact rule:** wrong rule: A variable declared inside a block can be used anywhere in the program, like a global. Right rule: A local variable exists only from its declaration to the end of its block.
- **Edge `block` &rarr; `LocalVarOutsideScope`, exact edge logic:** A variable declared inside a block can be used anywhere in the program, like a global. **Twin logic:** A local variable exists only from its declaration to the end of its block. (role: context)
- **Edge `variable` &rarr; `LocalVarOutsideScope`, exact edge logic:** A variable declared inside a block can be used anywhere in the program, like a global. **Twin logic:** A local variable exists only from its declaration to the end of its block. (role: context)

### LoopBodyScopeImpliesLoopLifetime

- **Edge:** `loop_scope` &rarr; `LoopBodyScopeImpliesLoopLifetime` (misconception)
- **Exact edge logic (the wrong rule):** A variable declared inside the loop body keeps its value from one pass to the next.
- **Twin logic (the right rule):** A variable declared inside the body is created anew on every pass and does not keep the previous pass's value.
- **Wrong belief (on the node):** a variable declared in the loop body lives across all iterations
- **Correct rule (on the node):** A variable declared inside the body is created anew on every pass and does not keep the previous pass's value.
- **Provenance:** published
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [1] misconception, exact rule:** wrong rule: a variable declared in the loop body lives across all iterations. Right rule: A variable declared inside the body is in scope only to the end of the body, so each pass declares and initializes it afresh and it does not keep the previous pass's value.
- **L0 way [5] inconsistent\_trace, exact rule:** Applies the scope rule (LT) unevenly: lets a body variable keep its value from the last pass on some passes but not others, or uses the for variable after the loop in one place but not another. (here mixing in: "a variable declared in the loop body lives across all iterations")
- **Edge `accumulator_pattern` &rarr; `LoopBodyScopeImpliesLoopLifetime`, exact edge logic:** a variable declared in the loop body lives across all iterations **Twin logic:** A variable declared inside the body is created anew on every pass and does not keep the previous pass's value. (role: context)
- **Edge `simulation_loop` &rarr; `LoopBodyScopeImpliesLoopLifetime`, exact edge logic:** Declaring page inside the simulation loop still lets the surfer continue from the previous page. **Twin logic:** If page is declared inside the loop body it is recreated each pass, so it must be declared before the loop to carry the walk forward. (role: context)
- **Edge `variable` &rarr; `LoopBodyScopeImpliesLoopLifetime`, exact edge logic:** a variable declared in the loop body lives across all iterations **Twin logic:** A variable declared inside the body is created anew on every pass and does not keep the previous pass's value. (role: context)

### LoopVariableLifetimeScope

- **Edge:** `loop_scope` &rarr; `LoopVariableLifetimeScope` (misconception)
- **Exact edge logic (the wrong rule):** The for variable i is a new variable on every pass rather than one variable changed by the update.
- **Twin logic (the right rule):** The for variable i is created once by the init, and the update changes that same variable on every pass.
- **Wrong belief (on the node):** The for variable i is a new variable on every pass rather than one variable changed by the update.
- **Correct rule (on the node):** The for variable i is created once by the init, and the update changes that same variable on every pass.
- **Provenance:** published
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [2] misconception, exact rule:** wrong rule: The for variable i is a new variable on every pass rather than one variable changed by the update. Right rule: The for variable i is created once by the init, the update changes that same variable on every pass, and i exists only until the end of the for statement.
- **Edge `loop_variable` &rarr; `LoopVariableLifetimeScope`, exact edge logic:** The for variable i is a new variable on every pass rather than one variable changed by the update. **Twin logic:** The for variable i is created once by the init, and the update changes that same variable on every pass. (role: context)

## Errors (1)

An error edge states the rule that gets broken in a program, and the right rule.

### AccumulatorDeclaredInLoop

- **Edge:** `loop_scope` &rarr; `AccumulatorDeclaredInLoop` (error)
- **Exact edge logic (the wrong rule):** Declaring sum inside the loop body keeps a running total across passes.
- **Twin logic (the right rule):** The accumulator must be declared and initialised before the loop.
- **Wrong belief (on the node):** Declaring sum inside the loop body keeps a running total across passes.
- **Correct rule (on the node):** The accumulator must be declared and initialised before the loop.
- **Provenance:** textbook
- **Role of this concept:** primary
- **Edge `accumulator_pattern` &rarr; `AccumulatorDeclaredInLoop`, exact edge logic:** Declaring sum inside the loop body keeps a running total across passes. **Twin logic:** The accumulator must be declared and initialised before the loop. (role: context)
- **Edge `counter_pattern` &rarr; `AccumulatorDeclaredInLoop`, exact edge logic:** Declaring sum inside the loop body keeps a running total across passes. **Twin logic:** The accumulator must be declared and initialised before the loop. (role: context)
- **Edge `logical_error` &rarr; `AccumulatorDeclaredInLoop`, exact edge logic:** Declaring sum inside the loop body keeps a running total across passes. **Twin logic:** The accumulator must be declared and initialised before the loop. (role: context)

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for loop scope: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to loop scope agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

- **Edge:** `loop_scope` &rarr; `loop_scope@L0` (has_level)
- **Exact edge logic:** loop scope -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (6 ways).

Ways (6), each with its exact rule:

- **[0] everyday\_reading** (rule type E, folk-meaning rule): Folk meaning: once a name is introduced ('let i be ...') it can be referred to for the rest of the text, and something introduced inside a repeated step keeps existing across repetitions. In Java a local variable exists only from its declaration to the end of its block, and a for header counts as part of the loop's block.
- **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `LoopBodyScopeImpliesLoopLifetime`: wrong rule: a variable declared in the loop body lives across all iterations. Right rule: A variable declared inside the body is in scope only to the end of the body, so each pass declares and initializes it afresh and it does not keep the previous pass's value.
- **[2] misconception** (rule type M, wrong rule / right rule) &rarr; `LoopVariableLifetimeScope`: wrong rule: The for variable i is a new variable on every pass rather than one variable changed by the update. Right rule: The for variable i is created once by the init, the update changes that same variable on every pass, and i exists only until the end of the for statement.
- **[3] misconception** (rule type M, wrong rule / right rule) &rarr; `ForVariableScopeBeyondLoop`: wrong rule: i declared in the for header can still be used after the loop has ended. Right rule: i declared in the for header exists only inside the loop, so using it after the loop does not compile.
- **[4] misconception** (rule type M, wrong rule / right rule) &rarr; `LocalVarOutsideScope`: wrong rule: A variable declared inside a block can be used anywhere in the program, like a global. Right rule: A local variable exists only from its declaration to the end of its block.
- **[5] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `LoopBodyScopeImpliesLoopLifetime`: Applies the scope rule (LT) unevenly: lets a body variable keep its value from the last pass on some passes but not others, or uses the for variable after the loop in one place but not another. (here mixing in: "a variable declared in the loop body lives across all iterations")

### L1: Unistructural / atom x text surface

L1 for loop scope: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

- **Edge:** `loop_scope` &rarr; `loop_scope@L1` (has_level)
- **Exact edge logic:** loop scope -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

Ways (2), each with its exact rule:

- **[0] names\_the\_element** (rule type N, identity rule): Scope is the part of the program where a variable is defined (can be used); for loops, the header is in the same block as the body.
- **[1] states\_the\_rule** (rule type S, declarative rule): A local variable's scope is the rest of the block after its declaration; a variable declared in a for initializer is in scope in the header and the body only; redeclaring a local variable inside its scope is a compile-time error.

### L2: Multistructural / block x execution / preoperational

L2 for loop scope: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

- **Edge:** `loop_scope` &rarr; `loop_scope@L2` (has_level)
- **Exact edge logic:** loop scope -&gt; L2 (Multistructural): the answer applies the rules of loop scope to every part of the code, in order (3 ways).

Ways (3), each with its exact rule:

- **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): Each time control enters a block, its declarations run in order, creating and (if initialized) setting those variables; when the block ends they cease to exist. For a loop body this happens on every pass; for the for-header variable once, at the init.
- **[1] output\_prediction** (rule type OP, evaluation / result rule): A variable declared inside the body starts from its initializer on every pass (int s = 0; inside the body gives s = 0 at the start of each pass); a for-header variable cannot be printed after the loop (compile error).
- **[2] one\_step\_execution** (rule type OS, state-transition rule): Entering the body creates its local variables afresh; leaving it removes them; values left in variables declared before the loop persist into the next pass.

### L3: Relational / relations x function (concrete operational begins)

L3 for loop scope: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

- **Edge:** `loop_scope` &rarr; `loop_scope@L3` (has_level)
- **Exact edge logic:** loop scope -&gt; L3 (Relational): the answer relates the parts (2 ways).

Ways (2), each with its exact rule:

- **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): A variable declared in the for header exists only from its declaration to the end of the for statement, so for and while versions differ: in the while version the counter is still available after the loop.
- **[1] purpose\_of\_the\_whole** (rule type P, plan / role rule): Plan: keep each variable as local as possible - declare a loop index in the for header when it is not needed afterwards, and declare variables that must survive the loop (accumulators, counters, loop variables needed later) before it.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for loop scope: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

- **Edge:** `loop_scope` &rarr; `loop_scope@L4` (has_level)
- **Exact edge logic:** loop scope -&gt; L4 (Extended abstract): the answer reasons beyond the given code (5 ways).

Ways (5), each with its exact rule:

- **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `LoopBodyScopeImpliesLoopLifetime`: Moving a declaration from before the loop into the body re-initializes the variable every pass and makes it unusable after the loop; moving a for-header declaration out (int i; for (i = 0; ...)) keeps the loop's behaviour and makes i usable after it.
- **[1] diagnose\_an\_error** (rule type D, error rule): rule broken: A variable declared in the body is in scope only to the end of the body and is re-declared and re-initialized on every pass. Kind: silent logic error. Trigger class: for (...) { int sum = 0; sum += a[i]; }: sum restarts at 0 each pass, so only the last term survives; printing sum after the loop is a compile-time error (cannot find symbol) because sum is out of scope.
- **[2] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Declare the index in the for header when it is used only inside the loop; declare it before the loop when its final value is needed (as in the break-based primality test) and declare running results before the loop.
- **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: A for-header variable is out of scope after the loop. Kind: compile-time. Trigger class: Using i after for (int i = ...) {...}: 'cannot find symbol'.
- **[4] diagnose\_an\_error** (rule type D, error rule): rule broken: A local variable cannot be redeclared in its own scope. Kind: compile-time. Trigger class: Declaring int i inside a for (int i ...) body, or an inner for (int i ...) inside an outer for (int i ...): 'variable i is already defined'.

## Same topic

`loop_scope` belongs to the topic **For loops (including i++ and scope)** (`topic1.3.d`). The topic also contains: `compound_assignment`, `for_loop`, `increment_operators`, `loop_variable`, `side_effect_order`.

## Rules of the concept (18)

- **Book** (SW-1e, p. 56 (pdf 66)): "The scope of a variable is the part of the program where it is defined."
- **Book** (SW-1e, p. 56 (pdf 66)): "For this purpose, the code in the for loop header is considered to be in the same block as the for loop body."
- **Book** (OT-For, ): "The scope of this variable extends from its declaration to the end of the block governed by the for statement, so it can be used in the termination and increment expressions as well."
- **Book** (GJS, ): "Instead, local variables are declared close to the point they are first used (within reason), to minimize their scope."
- **Book** (SW-1.3, ): "The scope of a variable is the part of the program that can refer to that variable by name."
- **E** (folk-meaning rule): Folk meaning: once a name is introduced ('let i be ...') it can be referred to for the rest of the text, and something introduced inside a repeated step keeps existing across repetitions. In Java a local variable exists only from its declaration to the end of its block, and a for header counts as part of the loop's block.
- **M** (wrong rule / right rule): ForVariableScopeBeyondLoop: wrong: i declared in the for header can still be used after the loop has ended. \| right: i declared in the for header exists only inside the loop, so using it after the loop does not compile.
- **M** (wrong rule / right rule): LocalVarOutsideScope: wrong: A variable declared inside a block can be used anywhere in the program, like a global. \| right: A local variable exists only from its declaration to the end of its block.
- **M** (wrong rule / right rule): LoopBodyScopeImpliesLoopLifetime: wrong: a variable declared in the loop body lives across all iterations \| right: A variable declared inside the body is in scope only to the end of the body, so each pass declares and initializes it afresh and it does not keep the previous pass's value.
- **M** (wrong rule / right rule): LoopVariableLifetimeScope: wrong: The for variable i is a new variable on every pass rather than one variable changed by the update. \| right: The for variable i is created once by the init, the update changes that same variable on every pass, and i exists only until the end of the for statement.
- **T** (uneven-application rule): Applies the scope rule (LT) unevenly: lets a body variable keep its value from the last pass on some passes but not others, or uses the for variable after the loop in one place but not another.
- **N** (identity rule): Scope is the part of the program where a variable is defined (can be used); for loops, the header is in the same block as the body.
- **S** (declarative rule): A local variable's scope is the rest of the block after its declaration; a variable declared in a for initializer is in scope in the header and the body only; redeclaring a local variable inside its scope is a compile-time error.
- **LT** (operational sequencing rule): Each time control enters a block, its declarations run in order, creating and (if initialized) setting those variables; when the block ends they cease to exist. For a loop body this happens on every pass; for the for-header variable once, at the init.
- **OP** (evaluation / result rule): A variable declared inside the body starts from its initializer on every pass (int s = 0; inside the body gives s = 0 at the start of each pass); a for-header variable cannot be printed after the loop (compile error).
- **OS** (state-transition rule): Entering the body creates its local variables afresh; leaving it removes them; values left in variables declared before the loop persist into the next pass.
- **R** (composition rule (with a neighbour)): with for\_loop: A variable declared in the for header exists only from its declaration to the end of the for statement, so for and while versions differ: in the while version the counter is still available after the loop.
- **P** (plan / role rule): Plan: keep each variable as local as possible - declare a loop index in the for header when it is not needed afterwards, and declare variables that must survive the loop (accumulators, counters, loop variables needed later) before it.
- **C** (conservation rule): Moving a declaration from before the loop into the body re-initializes the variable every pass and makes it unusable after the loop; moving a for-header declaration out (int i; for (i = 0; ...)) keeps the loop's behaviour and makes i usable after it.
- **D** (error rule): rule broken: A variable declared in the body is in scope only to the end of the body and is re-declared and re-initialized on every pass. (silent logic error)
- **D** (error rule): rule broken: A for-header variable is out of scope after the loop. (compile-time)
- **D** (error rule): rule broken: A local variable cannot be redeclared in its own scope. (compile-time)
- **X** (applicability rule): Declare the index in the for header when it is used only inside the loop; declare it before the loop when its final value is needed (as in the break-based primality test) and declare running results before the loop.

## How it is found in code and answers (reader block)

- **Aliases:** none
- **Code patterns:** `\bfor\s*\(\s*(?:int|long|double|char)\s+\w+`
- **Operator symbols:** none
- **Java types:** none

## The whole prerequisite chain

- **Everything it builds on (16):** `arithmetic_operators`, `boolean`, `boolean_expression`, `comparison_operators`, `data_type`, `do_while_loop`, `expression`, `for_loop`, `identifier`, `literal`, `logical_operators`, `loop_control`, `loop_variable`, `primitive_type`, `variable`, `while_loop`
- **Everything that builds on it (0):** nothing

## Every edge in this view and its exact edge logic (26)

All the edges drawn in the picture, in the order: prerequisite, parallel, misconception, error, has_level, contains.

**1. `for_loop` &rarr; `loop_scope`** (prerequisite)

- **Exact edge logic:** A variable declared in the for header exists only from its declaration to the end of the for statement's block.
- **Grounding:** book\_passage
- **Composition rule (R) of `for_loop` with `loop_scope`:** A variable declared in the for header is in scope only in the header and the body, so it cannot be used after the loop.
- **Composition rule (R) of `loop_scope` with `for_loop`:** A variable declared in the for header exists only from its declaration to the end of the for statement, so for and while versions differ: in the while version the counter is still available after the loop.

**2. `loop_scope` &rarr; `ForVariableScopeBeyondLoop`** (misconception)

- **Exact edge logic (the wrong rule):** i declared in the for header can still be used after the loop has ended.
- **Twin logic (the right rule):** i declared in the for header exists only inside the loop, so using it after the loop does not compile.
- **Role:** primary

**3. `loop_scope` &rarr; `LocalVarOutsideScope`** (misconception)

- **Exact edge logic (the wrong rule):** A variable declared inside a block can be used anywhere in the program, like a global.
- **Twin logic (the right rule):** A local variable exists only from its declaration to the end of its block.
- **Role:** primary

**4. `loop_scope` &rarr; `LoopBodyScopeImpliesLoopLifetime`** (misconception)

- **Exact edge logic (the wrong rule):** A variable declared inside the loop body keeps its value from one pass to the next.
- **Twin logic (the right rule):** A variable declared inside the body is created anew on every pass and does not keep the previous pass's value.
- **Role:** primary

**5. `loop_scope` &rarr; `LoopVariableLifetimeScope`** (misconception)

- **Exact edge logic (the wrong rule):** The for variable i is a new variable on every pass rather than one variable changed by the update.
- **Twin logic (the right rule):** The for variable i is created once by the init, and the update changes that same variable on every pass.
- **Role:** primary

**6. `accumulator_pattern` &rarr; `LoopBodyScopeImpliesLoopLifetime`** (misconception)

- **Exact edge logic (the wrong rule):** a variable declared in the loop body lives across all iterations
- **Twin logic (the right rule):** A variable declared inside the body is created anew on every pass and does not keep the previous pass's value.
- **Role:** context

**7. `block` &rarr; `LocalVarOutsideScope`** (misconception)

- **Exact edge logic (the wrong rule):** A variable declared inside a block can be used anywhere in the program, like a global.
- **Twin logic (the right rule):** A local variable exists only from its declaration to the end of its block.
- **Role:** context

**8. `loop_variable` &rarr; `LoopVariableLifetimeScope`** (misconception)

- **Exact edge logic (the wrong rule):** The for variable i is a new variable on every pass rather than one variable changed by the update.
- **Twin logic (the right rule):** The for variable i is created once by the init, and the update changes that same variable on every pass.
- **Role:** context

**9. `simulation_loop` &rarr; `LoopBodyScopeImpliesLoopLifetime`** (misconception)

- **Exact edge logic (the wrong rule):** Declaring page inside the simulation loop still lets the surfer continue from the previous page.
- **Twin logic (the right rule):** If page is declared inside the loop body it is recreated each pass, so it must be declared before the loop to carry the walk forward.
- **Role:** context

**10. `variable` &rarr; `LocalVarOutsideScope`** (misconception)

- **Exact edge logic (the wrong rule):** A variable declared inside a block can be used anywhere in the program, like a global.
- **Twin logic (the right rule):** A local variable exists only from its declaration to the end of its block.
- **Role:** context

**11. `variable` &rarr; `LoopBodyScopeImpliesLoopLifetime`** (misconception)

- **Exact edge logic (the wrong rule):** a variable declared in the loop body lives across all iterations
- **Twin logic (the right rule):** A variable declared inside the body is created anew on every pass and does not keep the previous pass's value.
- **Role:** context

**12. `loop_scope` &rarr; `AccumulatorDeclaredInLoop`** (error)

- **Exact edge logic (the wrong rule):** Declaring sum inside the loop body keeps a running total across passes.
- **Twin logic (the right rule):** The accumulator must be declared and initialised before the loop.
- **Role:** primary

**13. `accumulator_pattern` &rarr; `AccumulatorDeclaredInLoop`** (error)

- **Exact edge logic (the wrong rule):** Declaring sum inside the loop body keeps a running total across passes.
- **Twin logic (the right rule):** The accumulator must be declared and initialised before the loop.
- **Role:** context

**14. `counter_pattern` &rarr; `AccumulatorDeclaredInLoop`** (error)

- **Exact edge logic (the wrong rule):** Declaring sum inside the loop body keeps a running total across passes.
- **Twin logic (the right rule):** The accumulator must be declared and initialised before the loop.
- **Role:** context

**15. `logical_error` &rarr; `AccumulatorDeclaredInLoop`** (error)

- **Exact edge logic (the wrong rule):** Declaring sum inside the loop body keeps a running total across passes.
- **Twin logic (the right rule):** The accumulator must be declared and initialised before the loop.
- **Role:** context

**16. `loop_scope` &rarr; `loop_scope@L0`** (has_level)

- **Exact edge logic:** loop scope -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (6 ways).
  - **[0] everyday\_reading** (rule type E, folk-meaning rule): Folk meaning: once a name is introduced ('let i be ...') it can be referred to for the rest of the text, and something introduced inside a repeated step keeps existing across repetitions. In Java a local variable exists only from its declaration to the end of its block, and a for header counts as part of the loop's block.
  - **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `LoopBodyScopeImpliesLoopLifetime`: wrong rule: a variable declared in the loop body lives across all iterations. Right rule: A variable declared inside the body is in scope only to the end of the body, so each pass declares and initializes it afresh and it does not keep the previous pass's value.
  - **[2] misconception** (rule type M, wrong rule / right rule) &rarr; `LoopVariableLifetimeScope`: wrong rule: The for variable i is a new variable on every pass rather than one variable changed by the update. Right rule: The for variable i is created once by the init, the update changes that same variable on every pass, and i exists only until the end of the for statement.
  - **[3] misconception** (rule type M, wrong rule / right rule) &rarr; `ForVariableScopeBeyondLoop`: wrong rule: i declared in the for header can still be used after the loop has ended. Right rule: i declared in the for header exists only inside the loop, so using it after the loop does not compile.
  - **[4] misconception** (rule type M, wrong rule / right rule) &rarr; `LocalVarOutsideScope`: wrong rule: A variable declared inside a block can be used anywhere in the program, like a global. Right rule: A local variable exists only from its declaration to the end of its block.
  - **[5] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `LoopBodyScopeImpliesLoopLifetime`: Applies the scope rule (LT) unevenly: lets a body variable keep its value from the last pass on some passes but not others, or uses the for variable after the loop in one place but not another. (here mixing in: "a variable declared in the loop body lives across all iterations")

**17. `loop_scope` &rarr; `loop_scope@L1`** (has_level)

- **Exact edge logic:** loop scope -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).
  - **[0] names\_the\_element** (rule type N, identity rule): Scope is the part of the program where a variable is defined (can be used); for loops, the header is in the same block as the body.
  - **[1] states\_the\_rule** (rule type S, declarative rule): A local variable's scope is the rest of the block after its declaration; a variable declared in a for initializer is in scope in the header and the body only; redeclaring a local variable inside its scope is a compile-time error.

**18. `loop_scope` &rarr; `loop_scope@L2`** (has_level)

- **Exact edge logic:** loop scope -&gt; L2 (Multistructural): the answer applies the rules of loop scope to every part of the code, in order (3 ways).
  - **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): Each time control enters a block, its declarations run in order, creating and (if initialized) setting those variables; when the block ends they cease to exist. For a loop body this happens on every pass; for the for-header variable once, at the init.
  - **[1] output\_prediction** (rule type OP, evaluation / result rule): A variable declared inside the body starts from its initializer on every pass (int s = 0; inside the body gives s = 0 at the start of each pass); a for-header variable cannot be printed after the loop (compile error).
  - **[2] one\_step\_execution** (rule type OS, state-transition rule): Entering the body creates its local variables afresh; leaving it removes them; values left in variables declared before the loop persist into the next pass.

**19. `loop_scope` &rarr; `loop_scope@L3`** (has_level)

- **Exact edge logic:** loop scope -&gt; L3 (Relational): the answer relates the parts (2 ways).
  - **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): A variable declared in the for header exists only from its declaration to the end of the for statement, so for and while versions differ: in the while version the counter is still available after the loop.
  - **[1] purpose\_of\_the\_whole** (rule type P, plan / role rule): Plan: keep each variable as local as possible - declare a loop index in the for header when it is not needed afterwards, and declare variables that must survive the loop (accumulators, counters, loop variables needed later) before it.

**20. `loop_scope` &rarr; `loop_scope@L4`** (has_level)

- **Exact edge logic:** loop scope -&gt; L4 (Extended abstract): the answer reasons beyond the given code (5 ways).
  - **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `LoopBodyScopeImpliesLoopLifetime`: Moving a declaration from before the loop into the body re-initializes the variable every pass and makes it unusable after the loop; moving a for-header declaration out (int i; for (i = 0; ...)) keeps the loop's behaviour and makes i usable after it.
  - **[1] diagnose\_an\_error** (rule type D, error rule): rule broken: A variable declared in the body is in scope only to the end of the body and is re-declared and re-initialized on every pass. Kind: silent logic error. Trigger class: for (...) { int sum = 0; sum += a[i]; }: sum restarts at 0 each pass, so only the last term survives; printing sum after the loop is a compile-time error (cannot find symbol) because sum is out of scope.
  - **[2] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Declare the index in the for header when it is used only inside the loop; declare it before the loop when its final value is needed (as in the break-based primality test) and declare running results before the loop.
  - **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: A for-header variable is out of scope after the loop. Kind: compile-time. Trigger class: Using i after for (int i = ...) {...}: 'cannot find symbol'.
  - **[4] diagnose\_an\_error** (rule type D, error rule): rule broken: A local variable cannot be redeclared in its own scope. Kind: compile-time. Trigger class: Declaring int i inside a for (int i ...) body, or an inner for (int i ...) inside an outer for (int i ...): 'variable i is already defined'.

**21. `topic1.3.d` &rarr; `loop_scope`** (contains)

- topic `topic1.3.d` contains `loop_scope`

**22. `topic1.3.d` &rarr; `compound_assignment`** (contains)

- topic `topic1.3.d` contains `compound_assignment`

**23. `topic1.3.d` &rarr; `for_loop`** (contains)

- topic `topic1.3.d` contains `for_loop`

**24. `topic1.3.d` &rarr; `increment_operators`** (contains)

- topic `topic1.3.d` contains `increment_operators`

**25. `topic1.3.d` &rarr; `loop_variable`** (contains)

- topic `topic1.3.d` contains `loop_variable`

**26. `topic1.3.d` &rarr; `side_effect_order`** (contains)

- topic `topic1.3.d` contains `side_effect_order`
