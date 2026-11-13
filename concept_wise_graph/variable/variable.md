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

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 63 edges around this concept, each explained in the graph's own words.

## What it needs first (2)

A prerequisite edge means the other concept has to be understood before `variable`.

### `identifier` comes before `variable`

*a name for a variable, method or class; case-sensitive, no spaces, not a keyword*

Every variable is named by an identifier that follows the naming rules.

- **Grounding:** book passage
- **How `variable` combines with `identifier`:** Each variable is named by an identifier, which must be legal and unique within the variable's scope.
- **How `identifier` combines with `variable`:** Each variable is named by one identifier, which must be unique within its scope: declaring a second local with the same name in that scope is a compile error.

### `literal` comes before `variable`

*a constant value written in code (42, 3.14, true, 'a', "hi")*

A variable of type t is given a value of type t, often written as a literal.

- **Grounding:** order only
- **How `variable` combines with `literal`:** Literals commonly give variables their values, and the literal's type must fit the variable's type (int x = 1.1; is rejected).
- **How `literal` combines with `variable`:** Literals commonly initialize variables. The literal's type must equal or widen to the variable's type: double y = 1; widens, but int x = 1.1; is an error.

## What it leads to (4)

These concepts need `variable` first.

### `variable` comes before `assignment`

*= stores the computed value of the right side*

Assignment needs a declared variable on its left side to store the computed value into.

- **Grounding:** book passage
- **How `variable` combines with `assignment`:** Assignment is the only statement that changes a variable, and its left-hand side must be a single variable.
- **How `assignment` combines with `variable`:** The left side must be a declared variable whose type accepts the value. Assignment is how that variable's value changes.

### `variable` comes before `expression`

*anything that evaluates to a value*

An expression can be a literal, a variable, or operations on them; we compute with a variable by using its name in an expression.

- **Grounding:** book passage
- **How `variable` combines with `expression`:** A variable name is itself an expression whose value is the variable's current value, and it combines with operators into larger expressions.
- **How `expression` combines with `variable`:** A variable name inside an expression contributes the variable's value at the moment of evaluation.

### `variable` comes before `naming_convention`

*choosing meaningful names: full words, lowerCamelCase, single letters only for throwaway loop counters*

Each variable gets a name; the convention says the name should describe what the variable holds.

- **Grounding:** book passage
- **How `variable` combines with `naming_convention`:** A variable's name should describe what it holds (lowerCamelCase), but the name has no effect on its value.
- **How `naming_convention` combines with `variable`:** Each variable's name should describe what it holds (count, sum, maxSoFar). Single letters suit only short-lived loop indices.

### `variable` comes before `program_state`

*Program state: the information needed to know what a program will do next: the values of its variables and array entries and the next statement*

Without arrays, a program's state is the values of its variables plus the next statement to run.

- **Grounding:** book passage
- **How `variable` combines with `program_state`:** The current values of all variables make up the program's state. A trace records each variable's value after each statement.
- **How `program_state` combines with `variable`:** Without arrays the state is the values of the variables plus the next statement; each array element adds one more variable to the state.

## Learned alongside (0)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

No parallel edge touches this concept.

## Misconceptions (14)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### AnyValueInAnyVariable

- **Wrong rule:** A variable declared int can hold 2.5 or "hi"; the type is only a label.
- **Right rule:** A data type is a set of values and a set of operations defined on them, so an int variable holds only int values.
- **Role of this concept:** context
- **Shows at level L0 as:** misconception: wrong rule: A variable declared int can hold 2.5 or "hi"; the type is only a label. Right rule: A data type is a set of values and a set of operations defined on them, so an int variable holds only int values.
- **Also an edge from `data_type`:** A variable declared int can hold 2.5 or "hi"; the type is only a label.
- **Also an edge from `declaration`:** A variable declared int can hold 2.5 or "hi"; the type is only a label.

### ArrayElementNotVariable

- **Wrong rule:** An array element a[i] is not a variable, so it cannot be read into directly or used inside another index, as in a[a[i]].
- **Right rule:** Each element a[i] is a variable of the element type and can be used anywhere a variable of that type can, including as an index.
- **Role of this concept:** context
- **Shows at level L0 as:** misconception: wrong rule: An array element a[i] is not a variable, so it cannot be read into directly or used inside another index, as in a[a[i]]. Right rule: Each element a[i] is a variable of the element type and can be used anywhere a variable of that type can, including as an index.
- **Also an edge from `indexing`:** An array element a[i] is not a variable, so it cannot be read into directly or used inside another index, as in a[a[i]].

### DeclaredVariableHasNoMemory

- **Wrong rule:** int x; without a value sets aside no memory; the variable only exists once something is assigned.
- **Right rule:** A declaration creates the variable (its storage) with its type; assignment later puts a value in it.
- **Role of this concept:** context
- **Shows at level L0 as:** misconception: wrong rule: int x; without a value sets aside no memory; the variable only exists once something is assigned. Right rule: A declaration creates the variable (its storage) with its type; assignment later puts a value in it.
- **Also an edge from `declaration`:** int x; without a value sets aside no memory; the variable only exists once something is assigned.

### LocalVarOutsideScope

- **Wrong rule:** A variable declared inside a block can be used anywhere in the program, like a global.
- **Right rule:** A local variable exists only from its declaration to the end of its block.
- **Role of this concept:** context
- **Shows at level L0 as:** misconception: wrong rule: A variable declared inside a block can be used anywhere in the program, like a global. Right rule: A local variable exists only from its declaration to the end of its block.
- **Also an edge from `block`:** A variable declared inside a block can be used anywhere in the program, like a global.
- **Also an edge from `loop_scope`:** A variable declared inside a block can be used anywhere in the program, like a global.

### LocalVariablesAutoInitialized

- **Wrong rule:** int x; inside main starts at 0, so x can be used before anything is assigned to it.
- **Right rule:** A local variable has no value until it is assigned, and using it before then does not compile.
- **Role of this concept:** context
- **Shows at level L0 as:** misconception: wrong rule: local variables get a default value on their own. Right rule: A local variable has no value until it is assigned, and using it before then does not compile.
- **Also an edge from `declaration`:** local variables get a default value on their own
- **Also an edge from `definite_assignment`:** local variables get a default value on their own

### LoopBodyScopeImpliesLoopLifetime

- **Wrong rule:** a variable declared in the loop body lives across all iterations
- **Right rule:** A variable declared inside the body is created anew on every pass and does not keep the previous pass's value.
- **Role of this concept:** context
- **Shows at level L0 as:** misconception: wrong rule: a variable declared in the loop body lives across all iterations. Right rule: A variable declared inside the body is created anew on every pass and does not keep the previous pass's value.
- **Also an edge from `accumulator_pattern`:** a variable declared in the loop body lives across all iterations
- **Also an edge from `loop_scope`:** A variable declared inside the loop body keeps its value from one pass to the next.
- **Also an edge from `simulation_loop`:** Declaring page inside the simulation loop still lets the surfer continue from the previous page.

### MultiValueVariable

- **Wrong rule:** A variable can contain more than one value.
- **Right rule:** A variable holds exactly one value at a time; assigning a new value replaces the old one.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: A variable can contain more than one value. Right rule: A variable holds exactly one value at a time; assigning a new value replaces the old one.

### NameGivesMeaning

- **Wrong rule:** Naming a variable max (or average) makes it hold the largest value (or the average) without code that computes it.
- **Right rule:** A name only labels the variable for human readers; only the statements that assign to it decide its value.
- **Role of this concept:** context
- **Shows at level L0 as:** misconception: wrong rule: Naming a variable max (or average) makes it hold the largest value (or the average) without code that computes it. Right rule: A name only labels the variable for human readers; only the statements that assign to it decide its value.
- **Also an edge from `naming_convention`:** Naming a variable max (or average) makes it hold the largest value (or the average) without code that computes it.

### NoReservedWords

- **Wrong rule:** A keyword such as int or class can be used as a variable name.
- **Right rule:** Keywords are reserved by Java and cannot be used as variable names.
- **Role of this concept:** context
- **Shows at level L0 as:** misconception: wrong rule: keywords may be reused as identifiers. Right rule: Keywords are reserved by Java and cannot be used as variable names.
- **Also an edge from `identifier`:** A keyword such as int or class can be used as a variable name.

### RereadIntoVariableInvalid

- **Wrong rule:** Reading a second input value into a variable that already holds one is an error, so the program cannot run.
- **Right rule:** A later read simply overwrites the variable's current value.
- **Role of this concept:** context
- **Shows at level L0 as:** misconception: wrong rule: Reading a second input value into a variable that already holds one is an error, so the program cannot run. Right rule: A later read simply overwrites the variable's current value.
- **Also an edge from `standard_input`:** Reading a second input value into a variable that already holds one is an error, so the program cannot run.

### VariableKeepsOldValue

- **Wrong rule:** A variable keeps its first value after a new assignment (the static model).
- **Right rule:** Each assignment or read replaces the variable's current value.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: A variable keeps its first value after a new assignment (the static model). Right rule: Each assignment or read replaces the variable's current value.
- **Also an edge from `assignment`:** A variable keeps its first value after a new assignment (the static model).

### VariableRolesInferred

- **Wrong rule:** The computer recognises that one variable plays two roles, e.g. input value and running total, and keeps the values apart; it knows which variable is the counter and which the sum.
- **Right rule:** A variable holds one value at a time; each role (input, counter, running total) needs its own variable and explicit update.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: The computer recognises that one variable plays two roles, e.g. input value and running total, and keeps the values apart; it knows which variable is the counter and which the sum. Right rule: A variable holds one value at a time; each role (input, counter, running total) needs its own variable and explicit update.
- **Also an edge from `accumulator_pattern`:** The computer recognises that one variable plays two roles, e.g. input value and running total, and keeps the values apart; it knows which variable is the counter and which the sum.
- **Also an edge from `counter_pattern`:** The computer recognises that one variable plays two roles, e.g. input value and running total, and keeps the values apart; it knows which variable is the counter and which the sum.

### VariablesHoldExpressions

- **Wrong rule:** = stores the expression itself, not its computed value
- **Right rule:** y = x + k; stores the value that x + k has at that moment, so later changes to x do not change y.
- **Role of this concept:** context
- **Shows at level L0 as:** misconception: wrong rule: = stores the expression itself, not its computed value. Right rule: y = x + k; stores the value that x + k has at that moment, so later changes to x do not change y.
- **Also an edge from `assignment`:** y = x + k; makes y always equal to x + k, so when x changes later, y changes too.
- **Also an edge from `expression`:** = stores the expression itself, not its computed value

### VariablesHoldObjects

- **Wrong rule:** A String or array variable contains the whole object inside it.
- **Right rule:** A reference variable holds only a reference to the object, which is stored separately.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: a reference variable holds the whole object, not a reference. Right rule: A reference variable holds only a reference to the object, which is stored separately.
- **Shows at level L0 as:** inconsistent trace: Points to LT (a read gives the current value, and each assignment replaces it). Applied unevenly, a student updates the value after some assignments but keeps the first value after others, or switches between a memory model and an equation model across tasks (y = x - y read as x = 2y). (here mixing in: "a reference variable holds the whole object, not a reference")
- **Also an edge from `primitive_vs_reference`:** a reference variable holds the whole object, not a reference

## Errors (1)

An error edge states the rule that gets broken in a program, and the right rule.

### UndeclaredOrRenamedVariable

- **Wrong rule:** Uses a variable that was never declared, or under a different name (studentTotal vs total).
- **Right rule:** Every variable must be declared, and used with exactly the declared name.
- **Role of this concept:** primary
- **Also an edge from `declaration`:** Uses a variable that was never declared, or under a different name (studentTotal vs total).
- **Also an edge from `identifier`:** Uses a variable that was never declared, or under a different name (studentTotal vs total).

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for variable: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to variable agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

variable -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (16 ways).

- **everyday reading** (folk-meaning rule): In algebra a variable is an unknown that keeps one value throughout an equation (x in x = 2y), and the 'box' metaphor suggests it can hold several things. In Java a variable is a named storage location holding exactly one value at a time, and that value changes as statements run.
- **misconception** (wrong rule / right rule; shows `VariablesHoldObjects`): wrong rule: a reference variable holds the whole object, not a reference. Right rule: A reference variable holds only a reference to the object, which is stored separately.
- **misconception** (wrong rule / right rule; shows `MultiValueVariable`): wrong rule: A variable can contain more than one value. Right rule: A variable holds exactly one value at a time; assigning a new value replaces the old one.
- **misconception** (wrong rule / right rule; shows `VariableRolesInferred`): wrong rule: The computer recognises that one variable plays two roles, e.g. input value and running total, and keeps the values apart; it knows which variable is the counter and which the sum. Right rule: A variable holds one value at a time; each role (input, counter, running total) needs its own variable and explicit update.
- **misconception** (wrong rule / right rule; shows `VariableKeepsOldValue`): wrong rule: A variable keeps its first value after a new assignment (the static model). Right rule: Each assignment or read replaces the variable's current value.
- **inconsistent trace** (uneven-application rule; shows `VariablesHoldObjects`): Points to LT (a read gives the current value, and each assignment replaces it). Applied unevenly, a student updates the value after some assignments but keeps the first value after others, or switches between a memory model and an equation model across tasks (y = x - y read as x = 2y). (here mixing in: "a reference variable holds the whole object, not a reference")
- **misconception** (wrong rule / right rule; shows `LocalVarOutsideScope`): wrong rule: A variable declared inside a block can be used anywhere in the program, like a global. Right rule: A local variable exists only from its declaration to the end of its block.
- **misconception** (wrong rule / right rule; shows `LoopBodyScopeImpliesLoopLifetime`): wrong rule: a variable declared in the loop body lives across all iterations. Right rule: A variable declared inside the body is created anew on every pass and does not keep the previous pass's value.
- **misconception** (wrong rule / right rule; shows `NameGivesMeaning`): wrong rule: Naming a variable max (or average) makes it hold the largest value (or the average) without code that computes it. Right rule: A name only labels the variable for human readers; only the statements that assign to it decide its value.
- **misconception** (wrong rule / right rule; shows `VariablesHoldExpressions`): wrong rule: = stores the expression itself, not its computed value. Right rule: y = x + k; stores the value that x + k has at that moment, so later changes to x do not change y.
- **misconception** (wrong rule / right rule; shows `AnyValueInAnyVariable`): wrong rule: A variable declared int can hold 2.5 or "hi"; the type is only a label. Right rule: A data type is a set of values and a set of operations defined on them, so an int variable holds only int values.
- **misconception** (wrong rule / right rule; shows `LocalVariablesAutoInitialized`): wrong rule: local variables get a default value on their own. Right rule: A local variable has no value until it is assigned, and using it before then does not compile.
- **misconception** (wrong rule / right rule; shows `NoReservedWords`): wrong rule: keywords may be reused as identifiers. Right rule: Keywords are reserved by Java and cannot be used as variable names.
- **misconception** (wrong rule / right rule; shows `DeclaredVariableHasNoMemory`): wrong rule: int x; without a value sets aside no memory; the variable only exists once something is assigned. Right rule: A declaration creates the variable (its storage) with its type; assignment later puts a value in it.
- **misconception** (wrong rule / right rule; shows `RereadIntoVariableInvalid`): wrong rule: Reading a second input value into a variable that already holds one is an error, so the program cannot run. Right rule: A later read simply overwrites the variable's current value.
- **misconception** (wrong rule / right rule; shows `ArrayElementNotVariable`): wrong rule: An array element a[i] is not a variable, so it cannot be read into directly or used inside another index, as in a[a[i]]. Right rule: Each element a[i] is a variable of the element type and can be used anywhere a variable of that type can, including as an index.

### L1: Unistructural / atom x text surface

L1 for variable: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

variable -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

- **names the element** (identity rule): Variable: a name that refers to a typed storage location holding one data-type value.
- **states the rule** (declarative rule): A variable must be declared with a type before use. It always holds a value of that type, must be assigned before it is read, and can be used only within its scope (from its declaration to the end of the enclosing block).

### L2: Multistructural / block x execution / preoperational

L2 for variable: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

variable -&gt; L2 (Multistructural): the answer applies the rules of variable to every part of the code, in order (3 ways).

- **line by line trace** (operational sequencing rule): Each time execution reaches an expression that uses the variable, its current value is fetched at that moment. An assignment to it takes effect only after its right-hand side has been fully evaluated.
- **output prediction** (evaluation / result rule): A variable in an expression yields the value most recently assigned to it, with its declared type. After int a = 5; int b = a; a = 3;, a is 3 and b is 5.
- **one step execution** (state-transition rule): Only an assignment or an input read into the variable changes it, and it changes only that variable, replacing the old value. Other variables keep their values.

### L3: Relational / relations x function (concrete operational begins)

L3 for variable: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

variable -&gt; L3 (Relational): the answer relates the parts (7 ways).

- **relation to neighbour** (composition rule (with a neighbour)): Literals commonly give variables their values, and the literal's type must fit the variable's type (int x = 1.1; is rejected).
- **relation to neighbour** (composition rule (with a neighbour)): Assignment is the only statement that changes a variable, and its left-hand side must be a single variable.
- **relation to neighbour** (composition rule (with a neighbour)): A variable name is itself an expression whose value is the variable's current value, and it combines with operators into larger expressions.
- **relation to neighbour** (composition rule (with a neighbour)): Each variable is named by an identifier, which must be legal and unique within the variable's scope.
- **relation to neighbour** (composition rule (with a neighbour)): A variable's name should describe what it holds (lowerCamelCase), but the name has no effect on its value.
- **relation to neighbour** (composition rule (with a neighbour)): The current values of all variables make up the program's state. A trace records each variable's value after each statement.
- **purpose of the whole** (plan / role rule): Variables keep track of values that change as a computation unfolds, each in one role (Sajaniemi): fixed value, stepper, most-recent holder, gatherer (running total), most-wanted holder, follower, one-way flag or temporary.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for variable: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

variable -&gt; L4 (Extended abstract): the answer reasons beyond the given code (6 ways).

- **predict a change** (conservation rule; shows `VariablesHoldObjects`): Renaming a variable consistently keeps behavior. Reordering statements that write and read it changes results (a = b; b = a; is not a swap). Moving its declaration into a loop body narrows its scope and resets it on every pass.
- **diagnose an error** (error rule): rule broken: Every variable must be declared (with a type) before use and referred to by exactly the declared name, inside its scope. Kind: compile-time. Trigger class: Use of a name that was never declared, was declared under another name, or is used outside the block where it was declared: 'cannot find symbol' (one missing declaration can produce several errors).
- **transfer to a new program** (applicability rule): Use a variable when a value must be remembered, changes during the computation, or deserves a name as an intermediate result. Use a final constant for a value that never changes, and an array when many values of one type must all be kept.
- **diagnose an error** (error rule): rule broken: A local variable must be assigned before it is read. Kind: compile-time. Trigger class: A read on a path where no assignment has happened (declared without initializer, or assigned only inside an if or loop): 'variable might not have been initialized'.
- **diagnose an error** (error rule): rule broken: A variable can be used only inside its scope. Kind: compile-time. Trigger class: Using a variable after the block, loop body or for header where it was declared has ended: 'cannot find symbol'.
- **diagnose an error** (error rule): rule broken: One variable holds one value, so each role needs its own variable. Kind: silent logic error. Trigger class: Reusing the same variable as both input value and running total (or counter): the earlier value is overwritten.

## Same topic

`variable` belongs to the topic **Data types and terminology (literals, identifiers, variables, declarations, assignment, expressions)** (`topic1.2.a`). The topic also contains: `assignment`, `chained_assignment`, `data_type`, `declaration`, `definite_assignment`, `expression`, `identifier`, `literal`, `named_constants`, `naming_convention`, `operator_precedence`, `primitive_type`, `program_trace`, `variable_swap`.

## Rules of the concept (34)

- **folk-meaning rule:** In algebra a variable is an unknown that keeps one value throughout an equation (x in x = 2y), and the 'box' metaphor suggests it can hold several things. In Java a variable is a named storage location holding exactly one value at a time, and that value changes as statements run.
- **wrong rule / right rule:** LocalVarOutsideScope: wrong: A variable declared inside a block can be used anywhere in the program, like a global. \| right: A local variable exists only from its declaration to the end of its block.
- **wrong rule / right rule:** LoopBodyScopeImpliesLoopLifetime: wrong: a variable declared in the loop body lives across all iterations \| right: A variable declared inside the body is created anew on every pass and does not keep the previous pass's value.
- **wrong rule / right rule:** MultiValueVariable: wrong: A variable can contain more than one value. \| right: A variable holds exactly one value at a time; assigning a new value replaces the old one.
- **wrong rule / right rule:** NameGivesMeaning: wrong: Naming a variable max (or average) makes it hold the largest value (or the average) without code that computes it. \| right: A name only labels the variable for human readers; only the statements that assign to it decide its value.
- **wrong rule / right rule:** VariablesHoldExpressions: wrong: = stores the expression itself, not its computed value \| right: y = x + k; stores the value that x + k has at that moment, so later changes to x do not change y.
- **wrong rule / right rule:** VariablesHoldObjects: wrong: a reference variable holds the whole object, not a reference \| right: A reference variable holds only a reference to the object, which is stored separately.
- **wrong rule / right rule:** AnyValueInAnyVariable: wrong: A variable declared int can hold 2.5 or "hi"; the type is only a label. \| right: A data type is a set of values and a set of operations defined on them, so an int variable holds only int values.
- **wrong rule / right rule:** LocalVariablesAutoInitialized: wrong: local variables get a default value on their own \| right: A local variable has no value until it is assigned, and using it before then does not compile.
- **wrong rule / right rule:** NoReservedWords: wrong: keywords may be reused as identifiers \| right: Keywords are reserved by Java and cannot be used as variable names.
- **wrong rule / right rule:** DeclaredVariableHasNoMemory: wrong: int x; without a value sets aside no memory; the variable only exists once something is assigned. \| right: A declaration creates the variable (its storage) with its type; assignment later puts a value in it.
- **wrong rule / right rule:** VariableRolesInferred: wrong: The computer recognises that one variable plays two roles, e.g. input value and running total, and keeps the values apart; it knows which variable is the counter and which the sum. \| right: A variable holds one value at a time; each role (input, counter, running total) needs its own variable and explicit update.
- **wrong rule / right rule:** VariableKeepsOldValue: wrong: A variable keeps its first value after a new assignment (the static model). \| right: Each assignment or read replaces the variable's current value.
- **wrong rule / right rule:** RereadIntoVariableInvalid: wrong: Reading a second input value into a variable that already holds one is an error, so the program cannot run. \| right: A later read simply overwrites the variable's current value.
- **wrong rule / right rule:** ArrayElementNotVariable: wrong: An array element a[i] is not a variable, so it cannot be read into directly or used inside another index, as in a[a[i]]. \| right: Each element a[i] is a variable of the element type and can be used anywhere a variable of that type can, including as an index.
- **uneven-application rule:** Points to LT (a read gives the current value, and each assignment replaces it). Applied unevenly, a student updates the value after some assignments but keeps the first value after others, or switches between a memory model and an equation model across tasks (y = x - y read as x = 2y).
- **identity rule:** Variable: a name that refers to a typed storage location holding one data-type value.
- **declarative rule:** A variable must be declared with a type before use. It always holds a value of that type, must be assigned before it is read, and can be used only within its scope (from its declaration to the end of the enclosing block).
- **operational sequencing rule:** Each time execution reaches an expression that uses the variable, its current value is fetched at that moment. An assignment to it takes effect only after its right-hand side has been fully evaluated.
- **evaluation / result rule:** A variable in an expression yields the value most recently assigned to it, with its declared type. After int a = 5; int b = a; a = 3;, a is 3 and b is 5.
- **state-transition rule:** Only an assignment or an input read into the variable changes it, and it changes only that variable, replacing the old value. Other variables keep their values.
- **composition rule (with a neighbour):** with literal: Literals commonly give variables their values, and the literal's type must fit the variable's type (int x = 1.1; is rejected).
- **composition rule (with a neighbour):** with assignment: Assignment is the only statement that changes a variable, and its left-hand side must be a single variable.
- **composition rule (with a neighbour):** with expression: A variable name is itself an expression whose value is the variable's current value, and it combines with operators into larger expressions.
- **composition rule (with a neighbour):** with identifier: Each variable is named by an identifier, which must be legal and unique within the variable's scope.
- **composition rule (with a neighbour):** with naming\_convention: A variable's name should describe what it holds (lowerCamelCase), but the name has no effect on its value.
- **composition rule (with a neighbour):** with program\_state: The current values of all variables make up the program's state. A trace records each variable's value after each statement.
- **plan / role rule:** Variables keep track of values that change as a computation unfolds, each in one role (Sajaniemi): fixed value, stepper, most-recent holder, gatherer (running total), most-wanted holder, follower, one-way flag or temporary.
- **conservation rule:** Renaming a variable consistently keeps behavior. Reordering statements that write and read it changes results (a = b; b = a; is not a swap). Moving its declaration into a loop body narrows its scope and resets it on every pass.
- **error rule:** rule broken: Every variable must be declared (with a type) before use and referred to by exactly the declared name, inside its scope. (compile-time)
- **error rule:** rule broken: A local variable must be assigned before it is read. (compile-time)
- **error rule:** rule broken: A variable can be used only inside its scope. (compile-time)
- **error rule:** rule broken: One variable holds one value, so each role needs its own variable. (silent logic error)
- **applicability rule:** Use a variable when a value must be remembered, changes during the computation, or deserves a name as an intermediate result. Use a final constant for a value that never changes, and an array when many values of one type must all be kept.

## The whole prerequisite chain

- **Everything it builds on (4):** `data_type`, `identifier`, `literal`, `primitive_type`
- **Everything that builds on it (77):** `accumulator_pattern`, `animation`, `api`, `array_copy`, `array_exchange`, `array_reversal`, `array_traversal`, `assignment`, `boolean_expression`, `boolean_flag_array`, `break_statement`, `chained_assignment`, `comparison_operators`, `compound_assignment`, `conditional_operator`, `continue_statement`, `convergence_rate`, `convergence_test`, `coordinate_scaling`, `counter_pattern`, `dangling_else`, `debugging`, `do_while_loop`, `drawing_shapes`, `else_if_chain`, `enhanced_for`, `expression`, `fencepost_loop`, `flag_search_loop`, `for_loop`, `frequency_counting`, `function_plotting`, `if_else_statement`, `if_statement`, `increment_operators`, `infinite_loop`, `labeled_break`, `loop_body`, `loop_control`, `loop_invariant_reasoning`, `loop_performance`, `loop_scope`, `loop_variable`, `math_library`, `math_random`, `math_round`, `matrix_operations`, `method_call`, `monte_carlo_simulation`, `mouse_interaction`, `named_constants`, `naming_convention`, `nested_conditionals`, `nested_loops`, `number_conversion`, `off_by_one_error`, `operator_precedence`, `power_method`, `program_state`, `program_trace`, `random_move`, `row_major_order`, `running_extreme`, `sampling_without_replacement`, `sentinel_loop`, `shuffle`, `side_effect_order`, `simulation_loop`, `standard_audio`, `standard_drawing`, `switch_statement`, `syntax_template`, `testing`, `trig_functions`, `two_models`, `variable_swap`, `while_loop`
