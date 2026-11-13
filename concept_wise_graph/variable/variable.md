# variable (`variable`)

a named, typed box that holds a value

Section 1.2 Built-in Types of Data, topic 1.2.a Data types and terminology (literals, identifiers, variables, declarations, assignment, expressions).

![The knowledge graph around variable](variable.png)

## At a glance

- **Needs first:** `identifier`, `literal`
- **Leads to:** `assignment`, `expression`, `naming_convention`, `program_state`
- **Learned alongside:** nothing
- **Misconceptions:** `AnyValueInAnyVariable`, `ArrayElementNotVariable`, `DeclaredVariableHasNoMemory`, `LocalVarOutsideScope`, `LocalVariablesAutoInitialized`, `LoopBodyScopeImpliesLoopLifetime`, `MultiValueVariable`, `NameGivesMeaning`, `NoReservedWords`, `RereadIntoVariableInvalid`, `VariableKeepsOldValue`, `VariableRolesInferred`, `VariablesHoldExpressions`, `VariablesHoldObjects`
- **Errors:** `UndeclaredOrRenamedVariable`
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 63 edges around this concept. The edge logic, the wrong and right rules and the exact rules of the ways are copied word for word from the graph.

## To work on (0)

Nothing is missing for this concept.

## What it needs first (2)

A prerequisite edge means the other concept has to be understood before `variable`.

### `identifier` comes before `variable`

*a name for a variable, method or class; case-sensitive, no spaces, not a keyword*

- **Edge:** `pre:identifier->variable`
- **Exact edge logic:** Every variable is named by an identifier that follows the naming rules.
- **Grounding:** book\_passage
- **Composition rule (R) of `variable` with `identifier`:** Each variable is named by an identifier, which must be legal and unique within the variable's scope.
- **Composition rule (R) of `identifier` with `variable`:** Each variable is named by one identifier, which must be unique within its scope: declaring a second local with the same name in that scope is a compile error.

### `literal` comes before `variable`

*a constant value written in code (42, 3.14, true, 'a', "hi")*

- **Edge:** `pre:literal->variable`
- **Exact edge logic:** A variable of type t is given a value of type t, often written as a literal.
- **Grounding:** order\_only
- **Composition rule (R) of `variable` with `literal`:** Literals commonly give variables their values, and the literal's type must fit the variable's type (int x = 1.1; is rejected).
- **Composition rule (R) of `literal` with `variable`:** Literals commonly initialize variables. The literal's type must equal or widen to the variable's type: double y = 1; widens, but int x = 1.1; is an error.

## What it leads to (4)

These concepts need `variable` first.

### `variable` comes before `assignment`

*= stores the computed value of the right side*

- **Edge:** `pre:variable->assignment`
- **Exact edge logic:** Assignment needs a declared variable on its left side to store the computed value into.
- **Grounding:** book\_passage
- **Composition rule (R) of `variable` with `assignment`:** Assignment is the only statement that changes a variable, and its left-hand side must be a single variable.
- **Composition rule (R) of `assignment` with `variable`:** The left side must be a declared variable whose type accepts the value. Assignment is how that variable's value changes.

### `variable` comes before `expression`

*anything that evaluates to a value*

- **Edge:** `pre:variable->expression`
- **Exact edge logic:** An expression can be a literal, a variable, or operations on them; we compute with a variable by using its name in an expression.
- **Grounding:** book\_passage
- **Composition rule (R) of `variable` with `expression`:** A variable name is itself an expression whose value is the variable's current value, and it combines with operators into larger expressions.
- **Composition rule (R) of `expression` with `variable`:** A variable name inside an expression contributes the variable's value at the moment of evaluation.

### `variable` comes before `naming_convention`

*choosing meaningful names: full words, lowerCamelCase, single letters only for throwaway loop counters*

- **Edge:** `pre:variable->naming_convention`
- **Exact edge logic:** Each variable gets a name; the convention says the name should describe what the variable holds.
- **Grounding:** book\_passage
- **Composition rule (R) of `variable` with `naming_convention`:** A variable's name should describe what it holds (lowerCamelCase), but the name has no effect on its value.
- **Composition rule (R) of `naming_convention` with `variable`:** Each variable's name should describe what it holds (count, sum, maxSoFar). Single letters suit only short-lived loop indices.

### `variable` comes before `program_state`

*Program state: the information needed to know what a program will do next: the values of its variables and array entries and the next statement*

- **Edge:** `pre:variable->program_state`
- **Exact edge logic:** Without arrays, a program's state is the values of its variables plus the next statement to run.
- **Grounding:** book\_passage
- **Composition rule (R) of `variable` with `program_state`:** The current values of all variables make up the program's state. A trace records each variable's value after each statement.
- **Composition rule (R) of `program_state` with `variable`:** Without arrays the state is the values of the variables plus the next statement; each array element adds one more variable to the state.

## Learned alongside (0)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

No parallel edge touches this concept.

## Misconceptions (14)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### AnyValueInAnyVariable

- **Edge:** `variable` &rarr; `AnyValueInAnyVariable` (misconception)
- **Exact edge logic (the wrong rule):** A variable declared int can hold 2.5 or "hi"; the type is only a label.
- **Twin logic (the right rule):** A data type is a set of values and a set of operations defined on them, so an int variable holds only int values.
- **Wrong belief (on the node):** A variable declared int can hold 2.5 or "hi"; the type is only a label.
- **Correct rule (on the node):** A data type is a set of values and a set of operations defined on them, so an int variable holds only int values.
- **Provenance:** textbook
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [10] misconception, exact rule:** wrong rule: A variable declared int can hold 2.5 or "hi"; the type is only a label. Right rule: A data type is a set of values and a set of operations defined on them, so an int variable holds only int values.
- **Edge `data_type` &rarr; `AnyValueInAnyVariable`, exact edge logic:** A variable declared int can hold 2.5 or "hi"; the type is only a label. **Twin logic:** A data type is a set of values and a set of operations defined on them, so an int variable holds only int values. (role: primary)
- **Edge `declaration` &rarr; `AnyValueInAnyVariable`, exact edge logic:** A variable declared int can hold 2.5 or "hi"; the type is only a label. **Twin logic:** A data type is a set of values and a set of operations defined on them, so an int variable holds only int values. (role: context)

### ArrayElementNotVariable

- **Edge:** `variable` &rarr; `ArrayElementNotVariable` (misconception)
- **Exact edge logic (the wrong rule):** An array element a[i] is not a variable, so it cannot be read into directly or used inside another index, as in a[a[i]].
- **Twin logic (the right rule):** Each element a[i] is a variable of the element type and can be used anywhere a variable of that type can, including as an index.
- **Wrong belief (on the node):** An array element a[i] is not a variable, so it cannot be read into directly or used inside another index, as in a[a[i]].
- **Correct rule (on the node):** Each element a[i] is a variable of the element type and can be used anywhere a variable of that type can, including as an index.
- **Provenance:** published
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [15] misconception, exact rule:** wrong rule: An array element a[i] is not a variable, so it cannot be read into directly or used inside another index, as in a[a[i]]. Right rule: Each element a[i] is a variable of the element type and can be used anywhere a variable of that type can, including as an index.
- **Edge `indexing` &rarr; `ArrayElementNotVariable`, exact edge logic:** An array element a[i] is not a variable, so it cannot be read into directly or used inside another index, as in a[a[i]]. **Twin logic:** Each element a[i] is a variable of the element type and can be used anywhere a variable of that type can, including as an index. (role: primary)

### DeclaredVariableHasNoMemory

- **Edge:** `variable` &rarr; `DeclaredVariableHasNoMemory` (misconception)
- **Exact edge logic (the wrong rule):** int x; without a value sets aside no memory; the variable only exists once something is assigned.
- **Twin logic (the right rule):** A declaration creates the variable (its storage) with its type; assignment later puts a value in it.
- **Wrong belief (on the node):** int x; without a value sets aside no memory; the variable only exists once something is assigned.
- **Correct rule (on the node):** A declaration creates the variable (its storage) with its type; assignment later puts a value in it.
- **Provenance:** published
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [13] misconception, exact rule:** wrong rule: int x; without a value sets aside no memory; the variable only exists once something is assigned. Right rule: A declaration creates the variable (its storage) with its type; assignment later puts a value in it.
- **Edge `declaration` &rarr; `DeclaredVariableHasNoMemory`, exact edge logic:** int x; without a value sets aside no memory; the variable only exists once something is assigned. **Twin logic:** A declaration creates the variable (its storage) with its type; assignment later puts a value in it. (role: primary)

### LocalVarOutsideScope

- **Edge:** `variable` &rarr; `LocalVarOutsideScope` (misconception)
- **Exact edge logic (the wrong rule):** A variable declared inside a block can be used anywhere in the program, like a global.
- **Twin logic (the right rule):** A local variable exists only from its declaration to the end of its block.
- **Wrong belief (on the node):** A variable declared inside a block can be used anywhere in the program, like a global.
- **Correct rule (on the node):** A local variable exists only from its declaration to the end of its block.
- **Provenance:** published
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [6] misconception, exact rule:** wrong rule: A variable declared inside a block can be used anywhere in the program, like a global. Right rule: A local variable exists only from its declaration to the end of its block.
- **Edge `block` &rarr; `LocalVarOutsideScope`, exact edge logic:** A variable declared inside a block can be used anywhere in the program, like a global. **Twin logic:** A local variable exists only from its declaration to the end of its block. (role: context)
- **Edge `loop_scope` &rarr; `LocalVarOutsideScope`, exact edge logic:** A variable declared inside a block can be used anywhere in the program, like a global. **Twin logic:** A local variable exists only from its declaration to the end of its block. (role: primary)

### LocalVariablesAutoInitialized

- **Edge:** `variable` &rarr; `LocalVariablesAutoInitialized` (misconception)
- **Exact edge logic (the wrong rule):** int x; inside main starts at 0, so x can be used before anything is assigned to it.
- **Twin logic (the right rule):** A local variable has no value until it is assigned, and using it before then does not compile.
- **Wrong belief (on the node):** local variables get a default value on their own
- **Correct rule (on the node):** A local variable has no value until it is assigned, and using it before then does not compile.
- **Provenance:** published
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [11] misconception, exact rule:** wrong rule: local variables get a default value on their own. Right rule: A local variable has no value until it is assigned, and using it before then does not compile.
- **Edge `declaration` &rarr; `LocalVariablesAutoInitialized`, exact edge logic:** local variables get a default value on their own **Twin logic:** A local variable has no value until it is assigned, and using it before then does not compile. (role: context)
- **Edge `definite_assignment` &rarr; `LocalVariablesAutoInitialized`, exact edge logic:** local variables get a default value on their own **Twin logic:** A local variable has no value until it is assigned, and using it before then does not compile. (role: primary)

### LoopBodyScopeImpliesLoopLifetime

- **Edge:** `variable` &rarr; `LoopBodyScopeImpliesLoopLifetime` (misconception)
- **Exact edge logic (the wrong rule):** a variable declared in the loop body lives across all iterations
- **Twin logic (the right rule):** A variable declared inside the body is created anew on every pass and does not keep the previous pass's value.
- **Wrong belief (on the node):** a variable declared in the loop body lives across all iterations
- **Correct rule (on the node):** A variable declared inside the body is created anew on every pass and does not keep the previous pass's value.
- **Provenance:** published
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [7] misconception, exact rule:** wrong rule: a variable declared in the loop body lives across all iterations. Right rule: A variable declared inside the body is created anew on every pass and does not keep the previous pass's value.
- **Edge `accumulator_pattern` &rarr; `LoopBodyScopeImpliesLoopLifetime`, exact edge logic:** a variable declared in the loop body lives across all iterations **Twin logic:** A variable declared inside the body is created anew on every pass and does not keep the previous pass's value. (role: context)
- **Edge `loop_scope` &rarr; `LoopBodyScopeImpliesLoopLifetime`, exact edge logic:** A variable declared inside the loop body keeps its value from one pass to the next. **Twin logic:** A variable declared inside the body is created anew on every pass and does not keep the previous pass's value. (role: primary)
- **Edge `simulation_loop` &rarr; `LoopBodyScopeImpliesLoopLifetime`, exact edge logic:** Declaring page inside the simulation loop still lets the surfer continue from the previous page. **Twin logic:** If page is declared inside the loop body it is recreated each pass, so it must be declared before the loop to carry the walk forward. (role: context)

### MultiValueVariable

- **Edge:** `variable` &rarr; `MultiValueVariable` (misconception)
- **Exact edge logic (the wrong rule):** A variable can contain more than one value.
- **Twin logic (the right rule):** A variable holds exactly one value at a time; assigning a new value replaces the old one.
- **Wrong belief (on the node):** A variable can contain more than one value.
- **Correct rule (on the node):** A variable holds exactly one value at a time; assigning a new value replaces the old one.
- **Provenance:** published
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [2] misconception, exact rule:** wrong rule: A variable can contain more than one value. Right rule: A variable holds exactly one value at a time; assigning a new value replaces the old one.

### NameGivesMeaning

- **Edge:** `variable` &rarr; `NameGivesMeaning` (misconception)
- **Exact edge logic (the wrong rule):** Naming a variable max (or average) makes it hold the largest value (or the average) without code that computes it.
- **Twin logic (the right rule):** A name only labels the variable for human readers; only the statements that assign to it decide its value.
- **Wrong belief (on the node):** Naming a variable max (or average) makes it hold the largest value (or the average) without code that computes it.
- **Correct rule (on the node):** A name only labels the variable for human readers; only the statements that assign to it decide its value.
- **Provenance:** published
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [8] misconception, exact rule:** wrong rule: Naming a variable max (or average) makes it hold the largest value (or the average) without code that computes it. Right rule: A name only labels the variable for human readers; only the statements that assign to it decide its value.
- **Edge `naming_convention` &rarr; `NameGivesMeaning`, exact edge logic:** Naming a variable max (or average) makes it hold the largest value (or the average) without code that computes it. **Twin logic:** A name only labels the variable for human readers; only the statements that assign to it decide its value. (role: primary)

### NoReservedWords

- **Edge:** `variable` &rarr; `NoReservedWords` (misconception)
- **Exact edge logic (the wrong rule):** A keyword such as int or class can be used as a variable name.
- **Twin logic (the right rule):** Keywords are reserved by Java and cannot be used as variable names.
- **Wrong belief (on the node):** keywords may be reused as identifiers
- **Correct rule (on the node):** Keywords are reserved by Java and cannot be used as variable names.
- **Provenance:** published
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [12] misconception, exact rule:** wrong rule: keywords may be reused as identifiers. Right rule: Keywords are reserved by Java and cannot be used as variable names.
- **Edge `identifier` &rarr; `NoReservedWords`, exact edge logic:** A keyword such as int or class can be used as a variable name. **Twin logic:** Keywords are reserved by Java and cannot be used as variable names. (role: primary)

### RereadIntoVariableInvalid

- **Edge:** `variable` &rarr; `RereadIntoVariableInvalid` (misconception)
- **Exact edge logic (the wrong rule):** Reading a second input value into a variable that already holds one is an error, so the program cannot run.
- **Twin logic (the right rule):** A later read simply overwrites the variable's current value.
- **Wrong belief (on the node):** Reading a second input value into a variable that already holds one is an error, so the program cannot run.
- **Correct rule (on the node):** A later read simply overwrites the variable's current value.
- **Provenance:** published
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [14] misconception, exact rule:** wrong rule: Reading a second input value into a variable that already holds one is an error, so the program cannot run. Right rule: A later read simply overwrites the variable's current value.
- **Edge `standard_input` &rarr; `RereadIntoVariableInvalid`, exact edge logic:** Reading a second input value into a variable that already holds one is an error, so the program cannot run. **Twin logic:** A later read simply overwrites the variable's current value. (role: primary)

### VariableKeepsOldValue

- **Edge:** `variable` &rarr; `VariableKeepsOldValue` (misconception)
- **Exact edge logic (the wrong rule):** A variable keeps its first value after a new assignment (the static model).
- **Twin logic (the right rule):** Each assignment or read replaces the variable's current value.
- **Wrong belief (on the node):** A variable keeps its first value after a new assignment (the static model).
- **Correct rule (on the node):** Each assignment or read replaces the variable's current value.
- **Provenance:** published
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [4] misconception, exact rule:** wrong rule: A variable keeps its first value after a new assignment (the static model). Right rule: Each assignment or read replaces the variable's current value.
- **Edge `assignment` &rarr; `VariableKeepsOldValue`, exact edge logic:** A variable keeps its first value after a new assignment (the static model). **Twin logic:** Each assignment or read replaces the variable's current value. (role: context)

### VariableRolesInferred

- **Edge:** `variable` &rarr; `VariableRolesInferred` (misconception)
- **Exact edge logic (the wrong rule):** The computer recognises that one variable plays two roles, e.g. input value and running total, and keeps the values apart; it knows which variable is the counter and which the sum.
- **Twin logic (the right rule):** A variable holds one value at a time; each role (input, counter, running total) needs its own variable and explicit update.
- **Wrong belief (on the node):** The computer recognises that one variable plays two roles, e.g. input value and running total, and keeps the values apart; it knows which variable is the counter and which the sum.
- **Correct rule (on the node):** A variable holds one value at a time; each role (input, counter, running total) needs its own variable and explicit update.
- **Provenance:** published
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [3] misconception, exact rule:** wrong rule: The computer recognises that one variable plays two roles, e.g. input value and running total, and keeps the values apart; it knows which variable is the counter and which the sum. Right rule: A variable holds one value at a time; each role (input, counter, running total) needs its own variable and explicit update.
- **Edge `accumulator_pattern` &rarr; `VariableRolesInferred`, exact edge logic:** The computer recognises that one variable plays two roles, e.g. input value and running total, and keeps the values apart; it knows which variable is the counter and which the sum. **Twin logic:** A variable holds one value at a time; each role (input, counter, running total) needs its own variable and explicit update. (role: context)
- **Edge `counter_pattern` &rarr; `VariableRolesInferred`, exact edge logic:** The computer recognises that one variable plays two roles, e.g. input value and running total, and keeps the values apart; it knows which variable is the counter and which the sum. **Twin logic:** A variable holds one value at a time; each role (input, counter, running total) needs its own variable and explicit update. (role: context)

### VariablesHoldExpressions

- **Edge:** `variable` &rarr; `VariablesHoldExpressions` (misconception)
- **Exact edge logic (the wrong rule):** = stores the expression itself, not its computed value
- **Twin logic (the right rule):** y = x + k; stores the value that x + k has at that moment, so later changes to x do not change y.
- **Wrong belief (on the node):** = stores the expression itself, not its computed value
- **Correct rule (on the node):** y = x + k; stores the value that x + k has at that moment, so later changes to x do not change y.
- **Provenance:** published
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [9] misconception, exact rule:** wrong rule: = stores the expression itself, not its computed value. Right rule: y = x + k; stores the value that x + k has at that moment, so later changes to x do not change y.
- **Edge `assignment` &rarr; `VariablesHoldExpressions`, exact edge logic:** y = x + k; makes y always equal to x + k, so when x changes later, y changes too. **Twin logic:** y = x + k; stores the value that x + k has at that moment, so later changes to x do not change y. (role: primary)
- **Edge `expression` &rarr; `VariablesHoldExpressions`, exact edge logic:** = stores the expression itself, not its computed value **Twin logic:** y = x + k; stores the value that x + k has at that moment, so later changes to x do not change y. (role: context)

### VariablesHoldObjects

- **Edge:** `variable` &rarr; `VariablesHoldObjects` (misconception)
- **Exact edge logic (the wrong rule):** A String or array variable contains the whole object inside it.
- **Twin logic (the right rule):** A reference variable holds only a reference to the object, which is stored separately.
- **Wrong belief (on the node):** a reference variable holds the whole object, not a reference
- **Correct rule (on the node):** A reference variable holds only a reference to the object, which is stored separately.
- **Provenance:** published
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [1] misconception, exact rule:** wrong rule: a reference variable holds the whole object, not a reference. Right rule: A reference variable holds only a reference to the object, which is stored separately.
- **L0 way [5] inconsistent\_trace, exact rule:** Points to LT (a read gives the current value, and each assignment replaces it). Applied unevenly, a student updates the value after some assignments but keeps the first value after others, or switches between a memory model and an equation model across tasks (y = x - y read as x = 2y). (here mixing in: "a reference variable holds the whole object, not a reference")
- **Edge `primitive_vs_reference` &rarr; `VariablesHoldObjects`, exact edge logic:** a reference variable holds the whole object, not a reference **Twin logic:** A reference variable holds only a reference to the object, which is stored separately. (role: context)

## Errors (1)

An error edge states the rule that gets broken in a program, and the right rule.

### UndeclaredOrRenamedVariable

- **Edge:** `variable` &rarr; `UndeclaredOrRenamedVariable` (error)
- **Exact edge logic (the wrong rule):** Uses a variable that was never declared, or under a different name (studentTotal vs total).
- **Twin logic (the right rule):** Every variable must be declared, and used with exactly the declared name.
- **Wrong belief (on the node):** Uses a variable that was never declared, or under a different name (studentTotal vs total).
- **Correct rule (on the node):** Every variable must be declared, and used with exactly the declared name.
- **Provenance:** textbook
- **Role of this concept:** primary
- **Edge `declaration` &rarr; `UndeclaredOrRenamedVariable`, exact edge logic:** Uses a variable that was never declared, or under a different name (studentTotal vs total). **Twin logic:** Every variable must be declared, and used with exactly the declared name. (role: context)
- **Edge `identifier` &rarr; `UndeclaredOrRenamedVariable`, exact edge logic:** Uses a variable that was never declared, or under a different name (studentTotal vs total). **Twin logic:** Every variable must be declared, and used with exactly the declared name. (role: context)

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for variable: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to variable agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

- **Edge:** `variable` &rarr; `variable@L0` (has_level)
- **Exact edge logic:** variable -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (16 ways).

Ways (16), each with its exact rule:

- **[0] everyday\_reading** (rule type E, folk-meaning rule): In algebra a variable is an unknown that keeps one value throughout an equation (x in x = 2y), and the 'box' metaphor suggests it can hold several things. In Java a variable is a named storage location holding exactly one value at a time, and that value changes as statements run.
- **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `VariablesHoldObjects`: wrong rule: a reference variable holds the whole object, not a reference. Right rule: A reference variable holds only a reference to the object, which is stored separately.
- **[2] misconception** (rule type M, wrong rule / right rule) &rarr; `MultiValueVariable`: wrong rule: A variable can contain more than one value. Right rule: A variable holds exactly one value at a time; assigning a new value replaces the old one.
- **[3] misconception** (rule type M, wrong rule / right rule) &rarr; `VariableRolesInferred`: wrong rule: The computer recognises that one variable plays two roles, e.g. input value and running total, and keeps the values apart; it knows which variable is the counter and which the sum. Right rule: A variable holds one value at a time; each role (input, counter, running total) needs its own variable and explicit update.
- **[4] misconception** (rule type M, wrong rule / right rule) &rarr; `VariableKeepsOldValue`: wrong rule: A variable keeps its first value after a new assignment (the static model). Right rule: Each assignment or read replaces the variable's current value.
- **[5] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `VariablesHoldObjects`: Points to LT (a read gives the current value, and each assignment replaces it). Applied unevenly, a student updates the value after some assignments but keeps the first value after others, or switches between a memory model and an equation model across tasks (y = x - y read as x = 2y). (here mixing in: "a reference variable holds the whole object, not a reference")
- **[6] misconception** (rule type M, wrong rule / right rule) &rarr; `LocalVarOutsideScope`: wrong rule: A variable declared inside a block can be used anywhere in the program, like a global. Right rule: A local variable exists only from its declaration to the end of its block.
- **[7] misconception** (rule type M, wrong rule / right rule) &rarr; `LoopBodyScopeImpliesLoopLifetime`: wrong rule: a variable declared in the loop body lives across all iterations. Right rule: A variable declared inside the body is created anew on every pass and does not keep the previous pass's value.
- **[8] misconception** (rule type M, wrong rule / right rule) &rarr; `NameGivesMeaning`: wrong rule: Naming a variable max (or average) makes it hold the largest value (or the average) without code that computes it. Right rule: A name only labels the variable for human readers; only the statements that assign to it decide its value.
- **[9] misconception** (rule type M, wrong rule / right rule) &rarr; `VariablesHoldExpressions`: wrong rule: = stores the expression itself, not its computed value. Right rule: y = x + k; stores the value that x + k has at that moment, so later changes to x do not change y.
- **[10] misconception** (rule type M, wrong rule / right rule) &rarr; `AnyValueInAnyVariable`: wrong rule: A variable declared int can hold 2.5 or "hi"; the type is only a label. Right rule: A data type is a set of values and a set of operations defined on them, so an int variable holds only int values.
- **[11] misconception** (rule type M, wrong rule / right rule) &rarr; `LocalVariablesAutoInitialized`: wrong rule: local variables get a default value on their own. Right rule: A local variable has no value until it is assigned, and using it before then does not compile.
- **[12] misconception** (rule type M, wrong rule / right rule) &rarr; `NoReservedWords`: wrong rule: keywords may be reused as identifiers. Right rule: Keywords are reserved by Java and cannot be used as variable names.
- **[13] misconception** (rule type M, wrong rule / right rule) &rarr; `DeclaredVariableHasNoMemory`: wrong rule: int x; without a value sets aside no memory; the variable only exists once something is assigned. Right rule: A declaration creates the variable (its storage) with its type; assignment later puts a value in it.
- **[14] misconception** (rule type M, wrong rule / right rule) &rarr; `RereadIntoVariableInvalid`: wrong rule: Reading a second input value into a variable that already holds one is an error, so the program cannot run. Right rule: A later read simply overwrites the variable's current value.
- **[15] misconception** (rule type M, wrong rule / right rule) &rarr; `ArrayElementNotVariable`: wrong rule: An array element a[i] is not a variable, so it cannot be read into directly or used inside another index, as in a[a[i]]. Right rule: Each element a[i] is a variable of the element type and can be used anywhere a variable of that type can, including as an index.

### L1: Unistructural / atom x text surface

L1 for variable: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

- **Edge:** `variable` &rarr; `variable@L1` (has_level)
- **Exact edge logic:** variable -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

Ways (2), each with its exact rule:

- **[0] names\_the\_element** (rule type N, identity rule): Variable: a name that refers to a typed storage location holding one data-type value.
- **[1] states\_the\_rule** (rule type S, declarative rule): A variable must be declared with a type before use. It always holds a value of that type, must be assigned before it is read, and can be used only within its scope (from its declaration to the end of the enclosing block).

### L2: Multistructural / block x execution / preoperational

L2 for variable: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

- **Edge:** `variable` &rarr; `variable@L2` (has_level)
- **Exact edge logic:** variable -&gt; L2 (Multistructural): the answer applies the rules of variable to every part of the code, in order (3 ways).

Ways (3), each with its exact rule:

- **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): Each time execution reaches an expression that uses the variable, its current value is fetched at that moment. An assignment to it takes effect only after its right-hand side has been fully evaluated.
- **[1] output\_prediction** (rule type OP, evaluation / result rule): A variable in an expression yields the value most recently assigned to it, with its declared type. After int a = 5; int b = a; a = 3;, a is 3 and b is 5.
- **[2] one\_step\_execution** (rule type OS, state-transition rule): Only an assignment or an input read into the variable changes it, and it changes only that variable, replacing the old value. Other variables keep their values.

### L3: Relational / relations x function (concrete operational begins)

L3 for variable: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

- **Edge:** `variable` &rarr; `variable@L3` (has_level)
- **Exact edge logic:** variable -&gt; L3 (Relational): the answer relates the parts (7 ways).

Ways (7), each with its exact rule:

- **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Literals commonly give variables their values, and the literal's type must fit the variable's type (int x = 1.1; is rejected).
- **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Assignment is the only statement that changes a variable, and its left-hand side must be a single variable.
- **[2] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): A variable name is itself an expression whose value is the variable's current value, and it combines with operators into larger expressions.
- **[3] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Each variable is named by an identifier, which must be legal and unique within the variable's scope.
- **[4] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): A variable's name should describe what it holds (lowerCamelCase), but the name has no effect on its value.
- **[5] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): The current values of all variables make up the program's state. A trace records each variable's value after each statement.
- **[6] purpose\_of\_the\_whole** (rule type P, plan / role rule): Variables keep track of values that change as a computation unfolds, each in one role (Sajaniemi): fixed value, stepper, most-recent holder, gatherer (running total), most-wanted holder, follower, one-way flag or temporary.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for variable: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

- **Edge:** `variable` &rarr; `variable@L4` (has_level)
- **Exact edge logic:** variable -&gt; L4 (Extended abstract): the answer reasons beyond the given code (6 ways).

Ways (6), each with its exact rule:

- **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `VariablesHoldObjects`: Renaming a variable consistently keeps behavior. Reordering statements that write and read it changes results (a = b; b = a; is not a swap). Moving its declaration into a loop body narrows its scope and resets it on every pass.
- **[1] diagnose\_an\_error** (rule type D, error rule): rule broken: Every variable must be declared (with a type) before use and referred to by exactly the declared name, inside its scope. Kind: compile-time. Trigger class: Use of a name that was never declared, was declared under another name, or is used outside the block where it was declared: 'cannot find symbol' (one missing declaration can produce several errors).
- **[2] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Use a variable when a value must be remembered, changes during the computation, or deserves a name as an intermediate result. Use a final constant for a value that never changes, and an array when many values of one type must all be kept.
- **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: A local variable must be assigned before it is read. Kind: compile-time. Trigger class: A read on a path where no assignment has happened (declared without initializer, or assigned only inside an if or loop): 'variable might not have been initialized'.
- **[4] diagnose\_an\_error** (rule type D, error rule): rule broken: A variable can be used only inside its scope. Kind: compile-time. Trigger class: Using a variable after the block, loop body or for header where it was declared has ended: 'cannot find symbol'.
- **[5] diagnose\_an\_error** (rule type D, error rule): rule broken: One variable holds one value, so each role needs its own variable. Kind: silent logic error. Trigger class: Reusing the same variable as both input value and running total (or counter): the earlier value is overwritten.

## Same topic

`variable` belongs to the topic **Data types and terminology (literals, identifiers, variables, declarations, assignment, expressions)** (`topic1.2.a`). The topic also contains: `assignment`, `chained_assignment`, `data_type`, `declaration`, `definite_assignment`, `expression`, `identifier`, `literal`, `named_constants`, `naming_convention`, `operator_precedence`, `primitive_type`, `program_trace`, `variable_swap`.

## Rules of the concept (34)

- **Book** (SW-1e, p. 15 (pdf 25)): "A variable is a name that we use to refer to a data-type value."
- **Book** (OT-Datatypes, ): "Local variables are slightly different; the compiler never assigns a default value to an uninitialized local variable."
- **E** (folk-meaning rule): In algebra a variable is an unknown that keeps one value throughout an equation (x in x = 2y), and the 'box' metaphor suggests it can hold several things. In Java a variable is a named storage location holding exactly one value at a time, and that value changes as statements run.
- **M** (wrong rule / right rule): LocalVarOutsideScope: wrong: A variable declared inside a block can be used anywhere in the program, like a global. \| right: A local variable exists only from its declaration to the end of its block.
- **M** (wrong rule / right rule): LoopBodyScopeImpliesLoopLifetime: wrong: a variable declared in the loop body lives across all iterations \| right: A variable declared inside the body is created anew on every pass and does not keep the previous pass's value.
- **M** (wrong rule / right rule): MultiValueVariable: wrong: A variable can contain more than one value. \| right: A variable holds exactly one value at a time; assigning a new value replaces the old one.
- **M** (wrong rule / right rule): NameGivesMeaning: wrong: Naming a variable max (or average) makes it hold the largest value (or the average) without code that computes it. \| right: A name only labels the variable for human readers; only the statements that assign to it decide its value.
- **M** (wrong rule / right rule): VariablesHoldExpressions: wrong: = stores the expression itself, not its computed value \| right: y = x + k; stores the value that x + k has at that moment, so later changes to x do not change y.
- **M** (wrong rule / right rule): VariablesHoldObjects: wrong: a reference variable holds the whole object, not a reference \| right: A reference variable holds only a reference to the object, which is stored separately.
- **M** (wrong rule / right rule): AnyValueInAnyVariable: wrong: A variable declared int can hold 2.5 or "hi"; the type is only a label. \| right: A data type is a set of values and a set of operations defined on them, so an int variable holds only int values.
- **M** (wrong rule / right rule): LocalVariablesAutoInitialized: wrong: local variables get a default value on their own \| right: A local variable has no value until it is assigned, and using it before then does not compile.
- **M** (wrong rule / right rule): NoReservedWords: wrong: keywords may be reused as identifiers \| right: Keywords are reserved by Java and cannot be used as variable names.
- **M** (wrong rule / right rule): DeclaredVariableHasNoMemory: wrong: int x; without a value sets aside no memory; the variable only exists once something is assigned. \| right: A declaration creates the variable (its storage) with its type; assignment later puts a value in it.
- **M** (wrong rule / right rule): VariableRolesInferred: wrong: The computer recognises that one variable plays two roles, e.g. input value and running total, and keeps the values apart; it knows which variable is the counter and which the sum. \| right: A variable holds one value at a time; each role (input, counter, running total) needs its own variable and explicit update.
- **M** (wrong rule / right rule): VariableKeepsOldValue: wrong: A variable keeps its first value after a new assignment (the static model). \| right: Each assignment or read replaces the variable's current value.
- **M** (wrong rule / right rule): RereadIntoVariableInvalid: wrong: Reading a second input value into a variable that already holds one is an error, so the program cannot run. \| right: A later read simply overwrites the variable's current value.
- **M** (wrong rule / right rule): ArrayElementNotVariable: wrong: An array element a[i] is not a variable, so it cannot be read into directly or used inside another index, as in a[a[i]]. \| right: Each element a[i] is a variable of the element type and can be used anywhere a variable of that type can, including as an index.
- **T** (uneven-application rule): Points to LT (a read gives the current value, and each assignment replaces it). Applied unevenly, a student updates the value after some assignments but keeps the first value after others, or switches between a memory model and an equation model across tasks (y = x - y read as x = 2y).
- **N** (identity rule): Variable: a name that refers to a typed storage location holding one data-type value.
- **S** (declarative rule): A variable must be declared with a type before use. It always holds a value of that type, must be assigned before it is read, and can be used only within its scope (from its declaration to the end of the enclosing block).
- **LT** (operational sequencing rule): Each time execution reaches an expression that uses the variable, its current value is fetched at that moment. An assignment to it takes effect only after its right-hand side has been fully evaluated.
- **OP** (evaluation / result rule): A variable in an expression yields the value most recently assigned to it, with its declared type. After int a = 5; int b = a; a = 3;, a is 3 and b is 5.
- **OS** (state-transition rule): Only an assignment or an input read into the variable changes it, and it changes only that variable, replacing the old value. Other variables keep their values.
- **R** (composition rule (with a neighbour)): with literal: Literals commonly give variables their values, and the literal's type must fit the variable's type (int x = 1.1; is rejected).
- **R** (composition rule (with a neighbour)): with assignment: Assignment is the only statement that changes a variable, and its left-hand side must be a single variable.
- **R** (composition rule (with a neighbour)): with expression: A variable name is itself an expression whose value is the variable's current value, and it combines with operators into larger expressions.
- **R** (composition rule (with a neighbour)): with identifier: Each variable is named by an identifier, which must be legal and unique within the variable's scope.
- **R** (composition rule (with a neighbour)): with naming\_convention: A variable's name should describe what it holds (lowerCamelCase), but the name has no effect on its value.
- **R** (composition rule (with a neighbour)): with program\_state: The current values of all variables make up the program's state. A trace records each variable's value after each statement.
- **P** (plan / role rule): Variables keep track of values that change as a computation unfolds, each in one role (Sajaniemi): fixed value, stepper, most-recent holder, gatherer (running total), most-wanted holder, follower, one-way flag or temporary.
- **C** (conservation rule): Renaming a variable consistently keeps behavior. Reordering statements that write and read it changes results (a = b; b = a; is not a swap). Moving its declaration into a loop body narrows its scope and resets it on every pass.
- **D** (error rule): rule broken: Every variable must be declared (with a type) before use and referred to by exactly the declared name, inside its scope. (compile-time)
- **D** (error rule): rule broken: A local variable must be assigned before it is read. (compile-time)
- **D** (error rule): rule broken: A variable can be used only inside its scope. (compile-time)
- **D** (error rule): rule broken: One variable holds one value, so each role needs its own variable. (silent logic error)
- **X** (applicability rule): Use a variable when a value must be remembered, changes during the computation, or deserves a name as an intermediate result. Use a final constant for a value that never changes, and an array when many values of one type must all be kept.

## How it is found in code and answers (reader block)

- **Aliases:** variable, variables, local variable, local variables
- **Code patterns:** `(?:^|[;{(,])\s*(?:final\s+)?(?:int|double|boolean|char|long|String|float|short|byte)(?:\s*\[\s*\])*\s+[A-Za-z_]\w*\s*(?:[=;,)\[:]|$)`
- **Operator symbols:** none
- **Java types:** none

## The whole prerequisite chain

- **Everything it builds on (4):** `data_type`, `identifier`, `literal`, `primitive_type`
- **Everything that builds on it (77):** `accumulator_pattern`, `animation`, `api`, `array_copy`, `array_exchange`, `array_reversal`, `array_traversal`, `assignment`, `boolean_expression`, `boolean_flag_array`, `break_statement`, `chained_assignment`, `comparison_operators`, `compound_assignment`, `conditional_operator`, `continue_statement`, `convergence_rate`, `convergence_test`, `coordinate_scaling`, `counter_pattern`, `dangling_else`, `debugging`, `do_while_loop`, `drawing_shapes`, `else_if_chain`, `enhanced_for`, `expression`, `fencepost_loop`, `flag_search_loop`, `for_loop`, `frequency_counting`, `function_plotting`, `if_else_statement`, `if_statement`, `increment_operators`, `infinite_loop`, `labeled_break`, `loop_body`, `loop_control`, `loop_invariant_reasoning`, `loop_performance`, `loop_scope`, `loop_variable`, `math_library`, `math_random`, `math_round`, `matrix_operations`, `method_call`, `monte_carlo_simulation`, `mouse_interaction`, `named_constants`, `naming_convention`, `nested_conditionals`, `nested_loops`, `number_conversion`, `off_by_one_error`, `operator_precedence`, `power_method`, `program_state`, `program_trace`, `random_move`, `row_major_order`, `running_extreme`, `sampling_without_replacement`, `sentinel_loop`, `shuffle`, `side_effect_order`, `simulation_loop`, `standard_audio`, `standard_drawing`, `switch_statement`, `syntax_template`, `testing`, `trig_functions`, `two_models`, `variable_swap`, `while_loop`

## Every edge in this view and its exact edge logic (63)

All the edges drawn in the picture, in the order: prerequisite, parallel, misconception, error, has_level, contains.

**1. `identifier` &rarr; `variable`** (prerequisite)

- **Exact edge logic:** Every variable is named by an identifier that follows the naming rules.
- **Grounding:** book\_passage
- **Composition rule (R) of `identifier` with `variable`:** Each variable is named by one identifier, which must be unique within its scope: declaring a second local with the same name in that scope is a compile error.
- **Composition rule (R) of `variable` with `identifier`:** Each variable is named by an identifier, which must be legal and unique within the variable's scope.

**2. `literal` &rarr; `variable`** (prerequisite)

- **Exact edge logic:** A variable of type t is given a value of type t, often written as a literal.
- **Grounding:** order\_only
- **Composition rule (R) of `literal` with `variable`:** Literals commonly initialize variables. The literal's type must equal or widen to the variable's type: double y = 1; widens, but int x = 1.1; is an error.
- **Composition rule (R) of `variable` with `literal`:** Literals commonly give variables their values, and the literal's type must fit the variable's type (int x = 1.1; is rejected).

**3. `variable` &rarr; `assignment`** (prerequisite)

- **Exact edge logic:** Assignment needs a declared variable on its left side to store the computed value into.
- **Grounding:** book\_passage
- **Composition rule (R) of `variable` with `assignment`:** Assignment is the only statement that changes a variable, and its left-hand side must be a single variable.
- **Composition rule (R) of `assignment` with `variable`:** The left side must be a declared variable whose type accepts the value. Assignment is how that variable's value changes.

**4. `variable` &rarr; `expression`** (prerequisite)

- **Exact edge logic:** An expression can be a literal, a variable, or operations on them; we compute with a variable by using its name in an expression.
- **Grounding:** book\_passage
- **Composition rule (R) of `variable` with `expression`:** A variable name is itself an expression whose value is the variable's current value, and it combines with operators into larger expressions.
- **Composition rule (R) of `expression` with `variable`:** A variable name inside an expression contributes the variable's value at the moment of evaluation.

**5. `variable` &rarr; `naming_convention`** (prerequisite)

- **Exact edge logic:** Each variable gets a name; the convention says the name should describe what the variable holds.
- **Grounding:** book\_passage
- **Composition rule (R) of `variable` with `naming_convention`:** A variable's name should describe what it holds (lowerCamelCase), but the name has no effect on its value.
- **Composition rule (R) of `naming_convention` with `variable`:** Each variable's name should describe what it holds (count, sum, maxSoFar). Single letters suit only short-lived loop indices.

**6. `variable` &rarr; `program_state`** (prerequisite)

- **Exact edge logic:** Without arrays, a program's state is the values of its variables plus the next statement to run.
- **Grounding:** book\_passage
- **Composition rule (R) of `variable` with `program_state`:** The current values of all variables make up the program's state. A trace records each variable's value after each statement.
- **Composition rule (R) of `program_state` with `variable`:** Without arrays the state is the values of the variables plus the next statement; each array element adds one more variable to the state.

**7. `variable` &rarr; `AnyValueInAnyVariable`** (misconception)

- **Exact edge logic (the wrong rule):** A variable declared int can hold 2.5 or "hi"; the type is only a label.
- **Twin logic (the right rule):** A data type is a set of values and a set of operations defined on them, so an int variable holds only int values.
- **Role:** context

**8. `variable` &rarr; `ArrayElementNotVariable`** (misconception)

- **Exact edge logic (the wrong rule):** An array element a[i] is not a variable, so it cannot be read into directly or used inside another index, as in a[a[i]].
- **Twin logic (the right rule):** Each element a[i] is a variable of the element type and can be used anywhere a variable of that type can, including as an index.
- **Role:** context

**9. `variable` &rarr; `DeclaredVariableHasNoMemory`** (misconception)

- **Exact edge logic (the wrong rule):** int x; without a value sets aside no memory; the variable only exists once something is assigned.
- **Twin logic (the right rule):** A declaration creates the variable (its storage) with its type; assignment later puts a value in it.
- **Role:** context

**10. `variable` &rarr; `LocalVarOutsideScope`** (misconception)

- **Exact edge logic (the wrong rule):** A variable declared inside a block can be used anywhere in the program, like a global.
- **Twin logic (the right rule):** A local variable exists only from its declaration to the end of its block.
- **Role:** context

**11. `variable` &rarr; `LocalVariablesAutoInitialized`** (misconception)

- **Exact edge logic (the wrong rule):** int x; inside main starts at 0, so x can be used before anything is assigned to it.
- **Twin logic (the right rule):** A local variable has no value until it is assigned, and using it before then does not compile.
- **Role:** context

**12. `variable` &rarr; `LoopBodyScopeImpliesLoopLifetime`** (misconception)

- **Exact edge logic (the wrong rule):** a variable declared in the loop body lives across all iterations
- **Twin logic (the right rule):** A variable declared inside the body is created anew on every pass and does not keep the previous pass's value.
- **Role:** context

**13. `variable` &rarr; `MultiValueVariable`** (misconception)

- **Exact edge logic (the wrong rule):** A variable can contain more than one value.
- **Twin logic (the right rule):** A variable holds exactly one value at a time; assigning a new value replaces the old one.
- **Role:** primary

**14. `variable` &rarr; `NameGivesMeaning`** (misconception)

- **Exact edge logic (the wrong rule):** Naming a variable max (or average) makes it hold the largest value (or the average) without code that computes it.
- **Twin logic (the right rule):** A name only labels the variable for human readers; only the statements that assign to it decide its value.
- **Role:** context

**15. `variable` &rarr; `NoReservedWords`** (misconception)

- **Exact edge logic (the wrong rule):** A keyword such as int or class can be used as a variable name.
- **Twin logic (the right rule):** Keywords are reserved by Java and cannot be used as variable names.
- **Role:** context

**16. `variable` &rarr; `RereadIntoVariableInvalid`** (misconception)

- **Exact edge logic (the wrong rule):** Reading a second input value into a variable that already holds one is an error, so the program cannot run.
- **Twin logic (the right rule):** A later read simply overwrites the variable's current value.
- **Role:** context

**17. `variable` &rarr; `VariableKeepsOldValue`** (misconception)

- **Exact edge logic (the wrong rule):** A variable keeps its first value after a new assignment (the static model).
- **Twin logic (the right rule):** Each assignment or read replaces the variable's current value.
- **Role:** primary

**18. `variable` &rarr; `VariableRolesInferred`** (misconception)

- **Exact edge logic (the wrong rule):** The computer recognises that one variable plays two roles, e.g. input value and running total, and keeps the values apart; it knows which variable is the counter and which the sum.
- **Twin logic (the right rule):** A variable holds one value at a time; each role (input, counter, running total) needs its own variable and explicit update.
- **Role:** primary

**19. `variable` &rarr; `VariablesHoldExpressions`** (misconception)

- **Exact edge logic (the wrong rule):** = stores the expression itself, not its computed value
- **Twin logic (the right rule):** y = x + k; stores the value that x + k has at that moment, so later changes to x do not change y.
- **Role:** context

**20. `variable` &rarr; `VariablesHoldObjects`** (misconception)

- **Exact edge logic (the wrong rule):** A String or array variable contains the whole object inside it.
- **Twin logic (the right rule):** A reference variable holds only a reference to the object, which is stored separately.
- **Role:** primary

**21. `accumulator_pattern` &rarr; `LoopBodyScopeImpliesLoopLifetime`** (misconception)

- **Exact edge logic (the wrong rule):** a variable declared in the loop body lives across all iterations
- **Twin logic (the right rule):** A variable declared inside the body is created anew on every pass and does not keep the previous pass's value.
- **Role:** context

**22. `accumulator_pattern` &rarr; `VariableRolesInferred`** (misconception)

- **Exact edge logic (the wrong rule):** The computer recognises that one variable plays two roles, e.g. input value and running total, and keeps the values apart; it knows which variable is the counter and which the sum.
- **Twin logic (the right rule):** A variable holds one value at a time; each role (input, counter, running total) needs its own variable and explicit update.
- **Role:** context

**23. `assignment` &rarr; `VariableKeepsOldValue`** (misconception)

- **Exact edge logic (the wrong rule):** A variable keeps its first value after a new assignment (the static model).
- **Twin logic (the right rule):** Each assignment or read replaces the variable's current value.
- **Role:** context

**24. `assignment` &rarr; `VariablesHoldExpressions`** (misconception)

- **Exact edge logic (the wrong rule):** y = x + k; makes y always equal to x + k, so when x changes later, y changes too.
- **Twin logic (the right rule):** y = x + k; stores the value that x + k has at that moment, so later changes to x do not change y.
- **Role:** primary

**25. `block` &rarr; `LocalVarOutsideScope`** (misconception)

- **Exact edge logic (the wrong rule):** A variable declared inside a block can be used anywhere in the program, like a global.
- **Twin logic (the right rule):** A local variable exists only from its declaration to the end of its block.
- **Role:** context

**26. `counter_pattern` &rarr; `VariableRolesInferred`** (misconception)

- **Exact edge logic (the wrong rule):** The computer recognises that one variable plays two roles, e.g. input value and running total, and keeps the values apart; it knows which variable is the counter and which the sum.
- **Twin logic (the right rule):** A variable holds one value at a time; each role (input, counter, running total) needs its own variable and explicit update.
- **Role:** context

**27. `data_type` &rarr; `AnyValueInAnyVariable`** (misconception)

- **Exact edge logic (the wrong rule):** A variable declared int can hold 2.5 or "hi"; the type is only a label.
- **Twin logic (the right rule):** A data type is a set of values and a set of operations defined on them, so an int variable holds only int values.
- **Role:** primary

**28. `declaration` &rarr; `AnyValueInAnyVariable`** (misconception)

- **Exact edge logic (the wrong rule):** A variable declared int can hold 2.5 or "hi"; the type is only a label.
- **Twin logic (the right rule):** A data type is a set of values and a set of operations defined on them, so an int variable holds only int values.
- **Role:** context

**29. `declaration` &rarr; `DeclaredVariableHasNoMemory`** (misconception)

- **Exact edge logic (the wrong rule):** int x; without a value sets aside no memory; the variable only exists once something is assigned.
- **Twin logic (the right rule):** A declaration creates the variable (its storage) with its type; assignment later puts a value in it.
- **Role:** primary

**30. `declaration` &rarr; `LocalVariablesAutoInitialized`** (misconception)

- **Exact edge logic (the wrong rule):** local variables get a default value on their own
- **Twin logic (the right rule):** A local variable has no value until it is assigned, and using it before then does not compile.
- **Role:** context

**31. `definite_assignment` &rarr; `LocalVariablesAutoInitialized`** (misconception)

- **Exact edge logic (the wrong rule):** local variables get a default value on their own
- **Twin logic (the right rule):** A local variable has no value until it is assigned, and using it before then does not compile.
- **Role:** primary

**32. `expression` &rarr; `VariablesHoldExpressions`** (misconception)

- **Exact edge logic (the wrong rule):** = stores the expression itself, not its computed value
- **Twin logic (the right rule):** y = x + k; stores the value that x + k has at that moment, so later changes to x do not change y.
- **Role:** context

**33. `identifier` &rarr; `NoReservedWords`** (misconception)

- **Exact edge logic (the wrong rule):** A keyword such as int or class can be used as a variable name.
- **Twin logic (the right rule):** Keywords are reserved by Java and cannot be used as variable names.
- **Role:** primary

**34. `indexing` &rarr; `ArrayElementNotVariable`** (misconception)

- **Exact edge logic (the wrong rule):** An array element a[i] is not a variable, so it cannot be read into directly or used inside another index, as in a[a[i]].
- **Twin logic (the right rule):** Each element a[i] is a variable of the element type and can be used anywhere a variable of that type can, including as an index.
- **Role:** primary

**35. `loop_scope` &rarr; `LocalVarOutsideScope`** (misconception)

- **Exact edge logic (the wrong rule):** A variable declared inside a block can be used anywhere in the program, like a global.
- **Twin logic (the right rule):** A local variable exists only from its declaration to the end of its block.
- **Role:** primary

**36. `loop_scope` &rarr; `LoopBodyScopeImpliesLoopLifetime`** (misconception)

- **Exact edge logic (the wrong rule):** A variable declared inside the loop body keeps its value from one pass to the next.
- **Twin logic (the right rule):** A variable declared inside the body is created anew on every pass and does not keep the previous pass's value.
- **Role:** primary

**37. `naming_convention` &rarr; `NameGivesMeaning`** (misconception)

- **Exact edge logic (the wrong rule):** Naming a variable max (or average) makes it hold the largest value (or the average) without code that computes it.
- **Twin logic (the right rule):** A name only labels the variable for human readers; only the statements that assign to it decide its value.
- **Role:** primary

**38. `primitive_vs_reference` &rarr; `VariablesHoldObjects`** (misconception)

- **Exact edge logic (the wrong rule):** a reference variable holds the whole object, not a reference
- **Twin logic (the right rule):** A reference variable holds only a reference to the object, which is stored separately.
- **Role:** context

**39. `simulation_loop` &rarr; `LoopBodyScopeImpliesLoopLifetime`** (misconception)

- **Exact edge logic (the wrong rule):** Declaring page inside the simulation loop still lets the surfer continue from the previous page.
- **Twin logic (the right rule):** If page is declared inside the loop body it is recreated each pass, so it must be declared before the loop to carry the walk forward.
- **Role:** context

**40. `standard_input` &rarr; `RereadIntoVariableInvalid`** (misconception)

- **Exact edge logic (the wrong rule):** Reading a second input value into a variable that already holds one is an error, so the program cannot run.
- **Twin logic (the right rule):** A later read simply overwrites the variable's current value.
- **Role:** primary

**41. `variable` &rarr; `UndeclaredOrRenamedVariable`** (error)

- **Exact edge logic (the wrong rule):** Uses a variable that was never declared, or under a different name (studentTotal vs total).
- **Twin logic (the right rule):** Every variable must be declared, and used with exactly the declared name.
- **Role:** primary

**42. `declaration` &rarr; `UndeclaredOrRenamedVariable`** (error)

- **Exact edge logic (the wrong rule):** Uses a variable that was never declared, or under a different name (studentTotal vs total).
- **Twin logic (the right rule):** Every variable must be declared, and used with exactly the declared name.
- **Role:** context

**43. `identifier` &rarr; `UndeclaredOrRenamedVariable`** (error)

- **Exact edge logic (the wrong rule):** Uses a variable that was never declared, or under a different name (studentTotal vs total).
- **Twin logic (the right rule):** Every variable must be declared, and used with exactly the declared name.
- **Role:** context

**44. `variable` &rarr; `variable@L0`** (has_level)

- **Exact edge logic:** variable -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (16 ways).
  - **[0] everyday\_reading** (rule type E, folk-meaning rule): In algebra a variable is an unknown that keeps one value throughout an equation (x in x = 2y), and the 'box' metaphor suggests it can hold several things. In Java a variable is a named storage location holding exactly one value at a time, and that value changes as statements run.
  - **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `VariablesHoldObjects`: wrong rule: a reference variable holds the whole object, not a reference. Right rule: A reference variable holds only a reference to the object, which is stored separately.
  - **[2] misconception** (rule type M, wrong rule / right rule) &rarr; `MultiValueVariable`: wrong rule: A variable can contain more than one value. Right rule: A variable holds exactly one value at a time; assigning a new value replaces the old one.
  - **[3] misconception** (rule type M, wrong rule / right rule) &rarr; `VariableRolesInferred`: wrong rule: The computer recognises that one variable plays two roles, e.g. input value and running total, and keeps the values apart; it knows which variable is the counter and which the sum. Right rule: A variable holds one value at a time; each role (input, counter, running total) needs its own variable and explicit update.
  - **[4] misconception** (rule type M, wrong rule / right rule) &rarr; `VariableKeepsOldValue`: wrong rule: A variable keeps its first value after a new assignment (the static model). Right rule: Each assignment or read replaces the variable's current value.
  - **[5] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `VariablesHoldObjects`: Points to LT (a read gives the current value, and each assignment replaces it). Applied unevenly, a student updates the value after some assignments but keeps the first value after others, or switches between a memory model and an equation model across tasks (y = x - y read as x = 2y). (here mixing in: "a reference variable holds the whole object, not a reference")
  - **[6] misconception** (rule type M, wrong rule / right rule) &rarr; `LocalVarOutsideScope`: wrong rule: A variable declared inside a block can be used anywhere in the program, like a global. Right rule: A local variable exists only from its declaration to the end of its block.
  - **[7] misconception** (rule type M, wrong rule / right rule) &rarr; `LoopBodyScopeImpliesLoopLifetime`: wrong rule: a variable declared in the loop body lives across all iterations. Right rule: A variable declared inside the body is created anew on every pass and does not keep the previous pass's value.
  - **[8] misconception** (rule type M, wrong rule / right rule) &rarr; `NameGivesMeaning`: wrong rule: Naming a variable max (or average) makes it hold the largest value (or the average) without code that computes it. Right rule: A name only labels the variable for human readers; only the statements that assign to it decide its value.
  - **[9] misconception** (rule type M, wrong rule / right rule) &rarr; `VariablesHoldExpressions`: wrong rule: = stores the expression itself, not its computed value. Right rule: y = x + k; stores the value that x + k has at that moment, so later changes to x do not change y.
  - **[10] misconception** (rule type M, wrong rule / right rule) &rarr; `AnyValueInAnyVariable`: wrong rule: A variable declared int can hold 2.5 or "hi"; the type is only a label. Right rule: A data type is a set of values and a set of operations defined on them, so an int variable holds only int values.
  - **[11] misconception** (rule type M, wrong rule / right rule) &rarr; `LocalVariablesAutoInitialized`: wrong rule: local variables get a default value on their own. Right rule: A local variable has no value until it is assigned, and using it before then does not compile.
  - **[12] misconception** (rule type M, wrong rule / right rule) &rarr; `NoReservedWords`: wrong rule: keywords may be reused as identifiers. Right rule: Keywords are reserved by Java and cannot be used as variable names.
  - **[13] misconception** (rule type M, wrong rule / right rule) &rarr; `DeclaredVariableHasNoMemory`: wrong rule: int x; without a value sets aside no memory; the variable only exists once something is assigned. Right rule: A declaration creates the variable (its storage) with its type; assignment later puts a value in it.
  - **[14] misconception** (rule type M, wrong rule / right rule) &rarr; `RereadIntoVariableInvalid`: wrong rule: Reading a second input value into a variable that already holds one is an error, so the program cannot run. Right rule: A later read simply overwrites the variable's current value.
  - **[15] misconception** (rule type M, wrong rule / right rule) &rarr; `ArrayElementNotVariable`: wrong rule: An array element a[i] is not a variable, so it cannot be read into directly or used inside another index, as in a[a[i]]. Right rule: Each element a[i] is a variable of the element type and can be used anywhere a variable of that type can, including as an index.

**45. `variable` &rarr; `variable@L1`** (has_level)

- **Exact edge logic:** variable -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).
  - **[0] names\_the\_element** (rule type N, identity rule): Variable: a name that refers to a typed storage location holding one data-type value.
  - **[1] states\_the\_rule** (rule type S, declarative rule): A variable must be declared with a type before use. It always holds a value of that type, must be assigned before it is read, and can be used only within its scope (from its declaration to the end of the enclosing block).

**46. `variable` &rarr; `variable@L2`** (has_level)

- **Exact edge logic:** variable -&gt; L2 (Multistructural): the answer applies the rules of variable to every part of the code, in order (3 ways).
  - **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): Each time execution reaches an expression that uses the variable, its current value is fetched at that moment. An assignment to it takes effect only after its right-hand side has been fully evaluated.
  - **[1] output\_prediction** (rule type OP, evaluation / result rule): A variable in an expression yields the value most recently assigned to it, with its declared type. After int a = 5; int b = a; a = 3;, a is 3 and b is 5.
  - **[2] one\_step\_execution** (rule type OS, state-transition rule): Only an assignment or an input read into the variable changes it, and it changes only that variable, replacing the old value. Other variables keep their values.

**47. `variable` &rarr; `variable@L3`** (has_level)

- **Exact edge logic:** variable -&gt; L3 (Relational): the answer relates the parts (7 ways).
  - **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Literals commonly give variables their values, and the literal's type must fit the variable's type (int x = 1.1; is rejected).
  - **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Assignment is the only statement that changes a variable, and its left-hand side must be a single variable.
  - **[2] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): A variable name is itself an expression whose value is the variable's current value, and it combines with operators into larger expressions.
  - **[3] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Each variable is named by an identifier, which must be legal and unique within the variable's scope.
  - **[4] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): A variable's name should describe what it holds (lowerCamelCase), but the name has no effect on its value.
  - **[5] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): The current values of all variables make up the program's state. A trace records each variable's value after each statement.
  - **[6] purpose\_of\_the\_whole** (rule type P, plan / role rule): Variables keep track of values that change as a computation unfolds, each in one role (Sajaniemi): fixed value, stepper, most-recent holder, gatherer (running total), most-wanted holder, follower, one-way flag or temporary.

**48. `variable` &rarr; `variable@L4`** (has_level)

- **Exact edge logic:** variable -&gt; L4 (Extended abstract): the answer reasons beyond the given code (6 ways).
  - **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `VariablesHoldObjects`: Renaming a variable consistently keeps behavior. Reordering statements that write and read it changes results (a = b; b = a; is not a swap). Moving its declaration into a loop body narrows its scope and resets it on every pass.
  - **[1] diagnose\_an\_error** (rule type D, error rule): rule broken: Every variable must be declared (with a type) before use and referred to by exactly the declared name, inside its scope. Kind: compile-time. Trigger class: Use of a name that was never declared, was declared under another name, or is used outside the block where it was declared: 'cannot find symbol' (one missing declaration can produce several errors).
  - **[2] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Use a variable when a value must be remembered, changes during the computation, or deserves a name as an intermediate result. Use a final constant for a value that never changes, and an array when many values of one type must all be kept.
  - **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: A local variable must be assigned before it is read. Kind: compile-time. Trigger class: A read on a path where no assignment has happened (declared without initializer, or assigned only inside an if or loop): 'variable might not have been initialized'.
  - **[4] diagnose\_an\_error** (rule type D, error rule): rule broken: A variable can be used only inside its scope. Kind: compile-time. Trigger class: Using a variable after the block, loop body or for header where it was declared has ended: 'cannot find symbol'.
  - **[5] diagnose\_an\_error** (rule type D, error rule): rule broken: One variable holds one value, so each role needs its own variable. Kind: silent logic error. Trigger class: Reusing the same variable as both input value and running total (or counter): the earlier value is overwritten.

**49. `topic1.2.a` &rarr; `variable`** (contains)

- topic `topic1.2.a` contains `variable`

**50. `topic1.2.a` &rarr; `assignment`** (contains)

- topic `topic1.2.a` contains `assignment`

**51. `topic1.2.a` &rarr; `chained_assignment`** (contains)

- topic `topic1.2.a` contains `chained_assignment`

**52. `topic1.2.a` &rarr; `data_type`** (contains)

- topic `topic1.2.a` contains `data_type`

**53. `topic1.2.a` &rarr; `declaration`** (contains)

- topic `topic1.2.a` contains `declaration`

**54. `topic1.2.a` &rarr; `definite_assignment`** (contains)

- topic `topic1.2.a` contains `definite_assignment`

**55. `topic1.2.a` &rarr; `expression`** (contains)

- topic `topic1.2.a` contains `expression`

**56. `topic1.2.a` &rarr; `identifier`** (contains)

- topic `topic1.2.a` contains `identifier`

**57. `topic1.2.a` &rarr; `literal`** (contains)

- topic `topic1.2.a` contains `literal`

**58. `topic1.2.a` &rarr; `named_constants`** (contains)

- topic `topic1.2.a` contains `named_constants`

**59. `topic1.2.a` &rarr; `naming_convention`** (contains)

- topic `topic1.2.a` contains `naming_convention`

**60. `topic1.2.a` &rarr; `operator_precedence`** (contains)

- topic `topic1.2.a` contains `operator_precedence`

**61. `topic1.2.a` &rarr; `primitive_type`** (contains)

- topic `topic1.2.a` contains `primitive_type`

**62. `topic1.2.a` &rarr; `program_trace`** (contains)

- topic `topic1.2.a` contains `program_trace`

**63. `topic1.2.a` &rarr; `variable_swap`** (contains)

- topic `topic1.2.a` contains `variable_swap`
