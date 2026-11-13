# declaration (`declaration`)

int x; -- introduces a variable name and its type

Section 1.2 Built-in Types of Data, topic 1.2.a Data types and terminology (literals, identifiers, variables, declarations, assignment, expressions).

![The knowledge graph around declaration](declaration.png)

## At a glance

- **Needs first:** `identifier`
- **Leads to:** `assignment`, `definite_assignment`, `named_constants`
- **Learned alongside:** nothing
- **Misconceptions:** `AnyValueInAnyVariable`, `DeclaredVariableHasNoMemory`, `LocalVariablesAutoInitialized`
- **Errors:** `DeclarationWithoutType`, `RedeclareToReassign`, `UndeclaredOrRenamedVariable`
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 38 edges around this concept, each explained in the graph's own words.

## What it needs first (1)

A prerequisite edge means the other concept has to be understood before `declaration`.

### `identifier` comes before `declaration`

*a name for a variable, method or class; case-sensitive, no spaces, not a keyword*

A declaration pairs a type with an identifier, e.g. int count;.

- **Grounding:** book passage
- **How `declaration` combines with `identifier`:** A declaration binds a legal identifier to a type, and that identifier must not already be declared in the same scope.
- **How `identifier` combines with `declaration`:** A declaration binds the identifier to a type. Every later use must repeat exactly that spelling, or the compiler cannot resolve it.

## What it leads to (3)

These concepts need `declaration` first.

### `declaration` comes before `assignment`

*= stores the computed value of the right side*

A variable must be declared before an assignment can store a value into it.

- **Grounding:** book passage
- **How `declaration` combines with `assignment`:** An assignment can store into a variable only after the variable's declaration, and only a value of a compatible type.
- **How `assignment` combines with `declaration`:** A declaration can include the first assignment (int x = 5;). Assigning to a variable that was never declared does not compile.

### `declaration` comes before `definite_assignment`

*a local variable must be assigned before it is read*

A declared local variable has no defined value until it is assigned, and the compiler rejects any read before that assignment.

- **Grounding:** book passage
- **How `declaration` combines with `definite_assignment`:** A declaration without an initializer leaves a local unassigned, and any read before an assignment on every path is a compile error.
- **How `definite_assignment` combines with `declaration`:** A declaration without an initializer leaves the local unassigned. Writing = value in the declaration satisfies the rule at once.

### `declaration` comes before `named_constants`

*final constants in UPPER\_CASE instead of magic numbers*

A constant is a declaration marked final.

- **Grounding:** book passage
- **How `declaration` combines with `named_constants`:** Adding final to a declaration makes the variable a constant that can be assigned only once.
- **How `named_constants` combines with `declaration`:** A constant is an ordinary declaration with the final modifier, with the same type and scope rules.

## Learned alongside (0)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

No parallel edge touches this concept.

## Misconceptions (3)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### AnyValueInAnyVariable

- **Wrong rule:** A variable declared int can hold 2.5 or "hi"; the type is only a label.
- **Right rule:** A data type is a set of values and a set of operations defined on them, so an int variable holds only int values.
- **Role of this concept:** context
- **Shows at level L0 as:** misconception: wrong rule: A variable declared int can hold 2.5 or "hi"; the type is only a label. Right rule: A data type is a set of values and a set of operations defined on them, so an int variable holds only int values.
- **Also an edge from `data_type`:** A variable declared int can hold 2.5 or "hi"; the type is only a label.
- **Also an edge from `variable`:** A variable declared int can hold 2.5 or "hi"; the type is only a label.

### DeclaredVariableHasNoMemory

- **Wrong rule:** int x; without a value sets aside no memory; the variable only exists once something is assigned.
- **Right rule:** A declaration creates the variable (its storage) with its type; assignment later puts a value in it.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: int x; without a value sets aside no memory; the variable only exists once something is assigned. Right rule: A declaration creates the variable (its storage) with its type; assignment later puts a value in it.
- **Shows at level L0 as:** inconsistent trace: Points to LT (a declaration runs once when reached and creates the variable, and later assignments only update it). Applied unevenly, a student re-creates or zeroes the variable on some passes but not others, or treats a declaration further down as already in effect. (here mixing in: "int x; without a value sets aside no memory; the variable only exists once something is assigned")
- **Also an edge from `variable`:** int x; without a value sets aside no memory; the variable only exists once something is assigned.

### LocalVariablesAutoInitialized

- **Wrong rule:** local variables get a default value on their own
- **Right rule:** A local variable has no value until it is assigned, and using it before then does not compile.
- **Role of this concept:** context
- **Shows at level L0 as:** misconception: wrong rule: local variables get a default value on their own. Right rule: A local variable has no value until it is assigned, and using it before then does not compile.
- **Also an edge from `definite_assignment`:** local variables get a default value on their own
- **Also an edge from `variable`:** int x; inside main starts at 0, so x can be used before anything is assigned to it.

## Errors (3)

An error edge states the rule that gets broken in a program, and the right rule.

### DeclarationWithoutType

- **Wrong rule:** Writes name = value; to declare a new variable.
- **Right rule:** A declaration needs a type: type name = value;
- **Role of this concept:** primary

### RedeclareToReassign

- **Wrong rule:** Writes int x = 5; ... int x = 10; to change x.
- **Right rule:** A declaration gives a variable its name and type; a later change of value is an assignment statement such as x = 10;, not a second declaration.
- **Role of this concept:** primary
- **Also an edge from `assignment`:** Writes int x = 5; ... int x = 10; to change x.

### UndeclaredOrRenamedVariable

- **Wrong rule:** Uses a variable that was never declared, or under a different name (studentTotal vs total).
- **Right rule:** Every variable must be declared, and used with exactly the declared name.
- **Role of this concept:** context
- **Also an edge from `identifier`:** Uses a variable that was never declared, or under a different name (studentTotal vs total).
- **Also an edge from `variable`:** Uses a variable that was never declared, or under a different name (studentTotal vs total).

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for declaration: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to declaration agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

declaration -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (5 ways).

- **everyday reading** (folk-meaning rule): In English, to 'declare' something announces a fact or gives it a value, so novices think int x; already sets x to 0, or that x = 5; alone creates x. In Java a declaration creates the variable with a type, and a local variable has no usable value until it is assigned.
- **misconception** (wrong rule / right rule; shows `DeclaredVariableHasNoMemory`): wrong rule: int x; without a value sets aside no memory; the variable only exists once something is assigned. Right rule: A declaration creates the variable (its storage) with its type; assignment later puts a value in it.
- **inconsistent trace** (uneven-application rule; shows `DeclaredVariableHasNoMemory`): Points to LT (a declaration runs once when reached and creates the variable, and later assignments only update it). Applied unevenly, a student re-creates or zeroes the variable on some passes but not others, or treats a declaration further down as already in effect. (here mixing in: "int x; without a value sets aside no memory; the variable only exists once something is assigned")
- **misconception** (wrong rule / right rule; shows `AnyValueInAnyVariable`): wrong rule: A variable declared int can hold 2.5 or "hi"; the type is only a label. Right rule: A data type is a set of values and a set of operations defined on them, so an int variable holds only int values.
- **misconception** (wrong rule / right rule; shows `LocalVariablesAutoInitialized`): wrong rule: local variables get a default value on their own. Right rule: A local variable has no value until it is assigned, and using it before then does not compile.

### L1: Unistructural / atom x text surface

L1 for declaration: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

declaration -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

- **names the element** (identity rule): Declaration statement: a statement that introduces a variable by giving its type and name, such as int count; or double x = 0.5;.
- **states the rule** (declarative rule): Syntax: type name; or type name = expression; or type a, b, c;. Each variable must be declared before it is used, only once per scope, and its type never changes.

### L2: Multistructural / block x execution / preoperational

L2 for declaration: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

declaration -&gt; L2 (Multistructural): the answer applies the rules of declaration to every part of the code, in order (3 ways).

- **line by line trace** (operational sequencing rule): When execution reaches the declaration, the variable comes into being. If there is an initializer, it is evaluated and stored. The variable's scope runs from there to the end of the enclosing block, and statements in the block run first to last.
- **output prediction** (evaluation / result rule): A declaration produces no value and no output. Its effect is to fix the variable's name and type for every later compile-time check.
- **one step execution** (state-transition rule): int x; adds x to the program state with an undefined (unassigned) value. int x = 5; adds x holding 5.

### L3: Relational / relations x function (concrete operational begins)

L3 for declaration: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

declaration -&gt; L3 (Relational): the answer relates the parts (5 ways).

- **relation to neighbour** (composition rule (with a neighbour)): A declaration binds a legal identifier to a type, and that identifier must not already be declared in the same scope.
- **relation to neighbour** (composition rule (with a neighbour)): An assignment can store into a variable only after the variable's declaration, and only a value of a compatible type.
- **relation to neighbour** (composition rule (with a neighbour)): A declaration without an initializer leaves a local unassigned, and any read before an assignment on every path is a compile error.
- **relation to neighbour** (composition rule (with a neighbour)): Adding final to a declaration makes the variable a constant that can be assigned only once.
- **purpose of the whole** (plan / role rule): Declarations make the programmer's intent explicit (names and types) so the compiler can check consistency. The usual plan is to declare each variable at its point of first use.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for declaration: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

declaration -&gt; L4 (Extended abstract): the answer reasons beyond the given code (6 ways).

- **predict a change** (conservation rule; shows `DeclaredVariableHasNoMemory`): Moving a declaration into an inner block (such as a loop body) shrinks its scope and re-creates the variable on each pass, so an accumulated value is lost. Moving it out widens its scope. Changing its type changes which values and operations are legal.
- **diagnose an error** (error rule): rule broken: A local variable may be declared only once in its scope; later changes use an assignment without the type. Kind: compile-time. Trigger class: A second 'int x = ...' for a name already declared in the same or an enclosing block: 'variable x is already defined'.
- **diagnose an error** (error rule): rule broken: A declaration must begin with a type (type name = value;); name = value; is only an assignment to an existing variable. Kind: compile-time. Trigger class: First use of a new variable written without its type (total = 0;): 'cannot find symbol' because no variable total exists.
- **transfer to a new program** (applicability rule): Declare every variable exactly once, in the narrowest block that covers all its uses, with an initializer when the first value is known. Declare it before (outside) a loop when its value must last across iterations or be used after the loop.
- **diagnose an error** (error rule): rule broken: Every variable must be declared (with a type) before use and referred to by exactly the declared name, inside its scope. Kind: compile-time. Trigger class: Use of a name that was never declared, was declared under another name, or is used outside the block where it was declared: 'cannot find symbol' (one missing declaration can produce several errors).
- **diagnose an error** (error rule): rule broken: The initializer's type must be assignable to the declared type. Kind: compile-time. Trigger class: Declaring int x = 1.1; or String s = 123;: 'incompatible types'.

## Same topic

`declaration` belongs to the topic **Data types and terminology (literals, identifiers, variables, declarations, assignment, expressions)** (`topic1.2.a`). The topic also contains: `assignment`, `chained_assignment`, `data_type`, `definite_assignment`, `expression`, `identifier`, `literal`, `named_constants`, `naming_convention`, `operator_precedence`, `primitive_type`, `program_trace`, `variable`, `variable_swap`.

## Rules of the concept (21)

- **folk-meaning rule:** In English, to 'declare' something announces a fact or gives it a value, so novices think int x; already sets x to 0, or that x = 5; alone creates x. In Java a declaration creates the variable with a type, and a local variable has no usable value until it is assigned.
- **wrong rule / right rule:** AnyValueInAnyVariable: wrong: A variable declared int can hold 2.5 or "hi"; the type is only a label. \| right: A data type is a set of values and a set of operations defined on them, so an int variable holds only int values.
- **wrong rule / right rule:** LocalVariablesAutoInitialized: wrong: local variables get a default value on their own \| right: A local variable has no value until it is assigned, and using it before then does not compile.
- **wrong rule / right rule:** DeclaredVariableHasNoMemory: wrong: int x; without a value sets aside no memory; the variable only exists once something is assigned. \| right: A declaration creates the variable (its storage) with its type; assignment later puts a value in it.
- **uneven-application rule:** Points to LT (a declaration runs once when reached and creates the variable, and later assignments only update it). Applied unevenly, a student re-creates or zeroes the variable on some passes but not others, or treats a declaration further down as already in effect.
- **identity rule:** Declaration statement: a statement that introduces a variable by giving its type and name, such as int count; or double x = 0.5;.
- **declarative rule:** Syntax: type name; or type name = expression; or type a, b, c;. Each variable must be declared before it is used, only once per scope, and its type never changes.
- **operational sequencing rule:** When execution reaches the declaration, the variable comes into being. If there is an initializer, it is evaluated and stored. The variable's scope runs from there to the end of the enclosing block, and statements in the block run first to last.
- **evaluation / result rule:** A declaration produces no value and no output. Its effect is to fix the variable's name and type for every later compile-time check.
- **state-transition rule:** int x; adds x to the program state with an undefined (unassigned) value. int x = 5; adds x holding 5.
- **composition rule (with a neighbour):** with identifier: A declaration binds a legal identifier to a type, and that identifier must not already be declared in the same scope.
- **composition rule (with a neighbour):** with assignment: An assignment can store into a variable only after the variable's declaration, and only a value of a compatible type.
- **composition rule (with a neighbour):** with definite\_assignment: A declaration without an initializer leaves a local unassigned, and any read before an assignment on every path is a compile error.
- **composition rule (with a neighbour):** with named\_constants: Adding final to a declaration makes the variable a constant that can be assigned only once.
- **plan / role rule:** Declarations make the programmer's intent explicit (names and types) so the compiler can check consistency. The usual plan is to declare each variable at its point of first use.
- **conservation rule:** Moving a declaration into an inner block (such as a loop body) shrinks its scope and re-creates the variable on each pass, so an accumulated value is lost. Moving it out widens its scope. Changing its type changes which values and operations are legal.
- **error rule:** rule broken: A declaration must begin with a type (type name = value;); name = value; is only an assignment to an existing variable. (compile-time)
- **error rule:** rule broken: A local variable may be declared only once in its scope; later changes use an assignment without the type. (compile-time)
- **error rule:** rule broken: Every variable must be declared (with a type) before use and referred to by exactly the declared name, inside its scope. (compile-time)
- **error rule:** rule broken: The initializer's type must be assignable to the declared type. (compile-time)
- **applicability rule:** Declare every variable exactly once, in the narrowest block that covers all its uses, with an initializer when the first value is known. Declare it before (outside) a loop when its value must last across iterations or be used after the loop.

## The whole prerequisite chain

- **Everything it builds on (1):** `identifier`
- **Everything that builds on it (21):** `accumulator_pattern`, `array_exchange`, `array_reversal`, `assignment`, `chained_assignment`, `compound_assignment`, `counter_pattern`, `debugging`, `definite_assignment`, `frequency_counting`, `increment_operators`, `monte_carlo_simulation`, `named_constants`, `program_trace`, `sampling_without_replacement`, `sentinel_loop`, `shuffle`, `side_effect_order`, `testing`, `two_models`, `variable_swap`
