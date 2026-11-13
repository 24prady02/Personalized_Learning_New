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

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 38 edges around this concept. The edge logic, the wrong and right rules and the exact rules of the ways are copied word for word from the graph.

## To work on (0)

Nothing is missing for this concept.

## What it needs first (1)

A prerequisite edge means the other concept has to be understood before `declaration`.

### `identifier` comes before `declaration`

*a name for a variable, method or class; case-sensitive, no spaces, not a keyword*

- **Edge:** `pre:identifier->declaration`
- **Exact edge logic:** A declaration pairs a type with an identifier, e.g. int count;.
- **Grounding:** book\_passage
- **Composition rule (R) of `declaration` with `identifier`:** A declaration binds a legal identifier to a type, and that identifier must not already be declared in the same scope.
- **Composition rule (R) of `identifier` with `declaration`:** A declaration binds the identifier to a type. Every later use must repeat exactly that spelling, or the compiler cannot resolve it.

## What it leads to (3)

These concepts need `declaration` first.

### `declaration` comes before `assignment`

*= stores the computed value of the right side*

- **Edge:** `pre:declaration->assignment`
- **Exact edge logic:** A variable must be declared before an assignment can store a value into it.
- **Grounding:** book\_passage
- **Composition rule (R) of `declaration` with `assignment`:** An assignment can store into a variable only after the variable's declaration, and only a value of a compatible type.
- **Composition rule (R) of `assignment` with `declaration`:** A declaration can include the first assignment (int x = 5;). Assigning to a variable that was never declared does not compile.

### `declaration` comes before `definite_assignment`

*a local variable must be assigned before it is read*

- **Edge:** `pre:declaration->definite_assignment`
- **Exact edge logic:** A declared local variable has no defined value until it is assigned, and the compiler rejects any read before that assignment.
- **Grounding:** book\_passage
- **Composition rule (R) of `declaration` with `definite_assignment`:** A declaration without an initializer leaves a local unassigned, and any read before an assignment on every path is a compile error.
- **Composition rule (R) of `definite_assignment` with `declaration`:** A declaration without an initializer leaves the local unassigned. Writing = value in the declaration satisfies the rule at once.

### `declaration` comes before `named_constants`

*final constants in UPPER\_CASE instead of magic numbers*

- **Edge:** `pre:declaration->named_constants`
- **Exact edge logic:** A constant is a declaration marked final.
- **Grounding:** book\_passage
- **Composition rule (R) of `declaration` with `named_constants`:** Adding final to a declaration makes the variable a constant that can be assigned only once.
- **Composition rule (R) of `named_constants` with `declaration`:** A constant is an ordinary declaration with the final modifier, with the same type and scope rules.

## Learned alongside (0)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

No parallel edge touches this concept.

## Misconceptions (3)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### AnyValueInAnyVariable

- **Edge:** `declaration` &rarr; `AnyValueInAnyVariable` (misconception)
- **Exact edge logic (the wrong rule):** A variable declared int can hold 2.5 or "hi"; the type is only a label.
- **Twin logic (the right rule):** A data type is a set of values and a set of operations defined on them, so an int variable holds only int values.
- **Wrong belief (on the node):** A variable declared int can hold 2.5 or "hi"; the type is only a label.
- **Correct rule (on the node):** A data type is a set of values and a set of operations defined on them, so an int variable holds only int values.
- **Provenance:** textbook
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [3] misconception, exact rule:** wrong rule: A variable declared int can hold 2.5 or "hi"; the type is only a label. Right rule: A data type is a set of values and a set of operations defined on them, so an int variable holds only int values.
- **Edge `data_type` &rarr; `AnyValueInAnyVariable`, exact edge logic:** A variable declared int can hold 2.5 or "hi"; the type is only a label. **Twin logic:** A data type is a set of values and a set of operations defined on them, so an int variable holds only int values. (role: primary)
- **Edge `variable` &rarr; `AnyValueInAnyVariable`, exact edge logic:** A variable declared int can hold 2.5 or "hi"; the type is only a label. **Twin logic:** A data type is a set of values and a set of operations defined on them, so an int variable holds only int values. (role: context)

### DeclaredVariableHasNoMemory

- **Edge:** `declaration` &rarr; `DeclaredVariableHasNoMemory` (misconception)
- **Exact edge logic (the wrong rule):** int x; without a value sets aside no memory; the variable only exists once something is assigned.
- **Twin logic (the right rule):** A declaration creates the variable (its storage) with its type; assignment later puts a value in it.
- **Wrong belief (on the node):** int x; without a value sets aside no memory; the variable only exists once something is assigned.
- **Correct rule (on the node):** A declaration creates the variable (its storage) with its type; assignment later puts a value in it.
- **Provenance:** published
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [1] misconception, exact rule:** wrong rule: int x; without a value sets aside no memory; the variable only exists once something is assigned. Right rule: A declaration creates the variable (its storage) with its type; assignment later puts a value in it.
- **L0 way [2] inconsistent\_trace, exact rule:** Points to LT (a declaration runs once when reached and creates the variable, and later assignments only update it). Applied unevenly, a student re-creates or zeroes the variable on some passes but not others, or treats a declaration further down as already in effect. (here mixing in: "int x; without a value sets aside no memory; the variable only exists once something is assigned")
- **Edge `variable` &rarr; `DeclaredVariableHasNoMemory`, exact edge logic:** int x; without a value sets aside no memory; the variable only exists once something is assigned. **Twin logic:** A declaration creates the variable (its storage) with its type; assignment later puts a value in it. (role: context)

### LocalVariablesAutoInitialized

- **Edge:** `declaration` &rarr; `LocalVariablesAutoInitialized` (misconception)
- **Exact edge logic (the wrong rule):** local variables get a default value on their own
- **Twin logic (the right rule):** A local variable has no value until it is assigned, and using it before then does not compile.
- **Wrong belief (on the node):** local variables get a default value on their own
- **Correct rule (on the node):** A local variable has no value until it is assigned, and using it before then does not compile.
- **Provenance:** published
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [4] misconception, exact rule:** wrong rule: local variables get a default value on their own. Right rule: A local variable has no value until it is assigned, and using it before then does not compile.
- **Edge `definite_assignment` &rarr; `LocalVariablesAutoInitialized`, exact edge logic:** local variables get a default value on their own **Twin logic:** A local variable has no value until it is assigned, and using it before then does not compile. (role: primary)
- **Edge `variable` &rarr; `LocalVariablesAutoInitialized`, exact edge logic:** int x; inside main starts at 0, so x can be used before anything is assigned to it. **Twin logic:** A local variable has no value until it is assigned, and using it before then does not compile. (role: context)

## Errors (3)

An error edge states the rule that gets broken in a program, and the right rule.

### DeclarationWithoutType

- **Edge:** `declaration` &rarr; `DeclarationWithoutType` (error)
- **Exact edge logic (the wrong rule):** Writes name = value; to declare a new variable.
- **Twin logic (the right rule):** A declaration needs a type: type name = value;
- **Wrong belief (on the node):** Writes name = value; to declare a new variable.
- **Correct rule (on the node):** A declaration needs a type: type name = value;
- **Provenance:** textbook
- **Role of this concept:** primary

### RedeclareToReassign

- **Edge:** `declaration` &rarr; `RedeclareToReassign` (error)
- **Exact edge logic (the wrong rule):** Writes int x = 5; ... int x = 10; to change x.
- **Twin logic (the right rule):** A declaration gives a variable its name and type; a later change of value is an assignment statement such as x = 10;, not a second declaration.
- **Wrong belief (on the node):** Writes int x = 5; ... int x = 10; to change x.
- **Correct rule (on the node):** A declaration gives a variable its name and type; a later change of value is an assignment statement such as x = 10;, not a second declaration.
- **Provenance:** textbook
- **Role of this concept:** primary
- **Edge `assignment` &rarr; `RedeclareToReassign`, exact edge logic:** Writes int x = 5; ... int x = 10; to change x. **Twin logic:** A declaration gives a variable its name and type; a later change of value is an assignment statement such as x = 10;, not a second declaration. (role: context)

### UndeclaredOrRenamedVariable

- **Edge:** `declaration` &rarr; `UndeclaredOrRenamedVariable` (error)
- **Exact edge logic (the wrong rule):** Uses a variable that was never declared, or under a different name (studentTotal vs total).
- **Twin logic (the right rule):** Every variable must be declared, and used with exactly the declared name.
- **Wrong belief (on the node):** Uses a variable that was never declared, or under a different name (studentTotal vs total).
- **Correct rule (on the node):** Every variable must be declared, and used with exactly the declared name.
- **Provenance:** textbook
- **Role of this concept:** context
- **Edge `identifier` &rarr; `UndeclaredOrRenamedVariable`, exact edge logic:** Uses a variable that was never declared, or under a different name (studentTotal vs total). **Twin logic:** Every variable must be declared, and used with exactly the declared name. (role: context)
- **Edge `variable` &rarr; `UndeclaredOrRenamedVariable`, exact edge logic:** Uses a variable that was never declared, or under a different name (studentTotal vs total). **Twin logic:** Every variable must be declared, and used with exactly the declared name. (role: primary)

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for declaration: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to declaration agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

- **Edge:** `declaration` &rarr; `declaration@L0` (has_level)
- **Exact edge logic:** declaration -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (5 ways).

Ways (5), each with its exact rule:

- **[0] everyday\_reading** (rule type E, folk-meaning rule): In English, to 'declare' something announces a fact or gives it a value, so novices think int x; already sets x to 0, or that x = 5; alone creates x. In Java a declaration creates the variable with a type, and a local variable has no usable value until it is assigned.
- **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `DeclaredVariableHasNoMemory`: wrong rule: int x; without a value sets aside no memory; the variable only exists once something is assigned. Right rule: A declaration creates the variable (its storage) with its type; assignment later puts a value in it.
- **[2] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `DeclaredVariableHasNoMemory`: Points to LT (a declaration runs once when reached and creates the variable, and later assignments only update it). Applied unevenly, a student re-creates or zeroes the variable on some passes but not others, or treats a declaration further down as already in effect. (here mixing in: "int x; without a value sets aside no memory; the variable only exists once something is assigned")
- **[3] misconception** (rule type M, wrong rule / right rule) &rarr; `AnyValueInAnyVariable`: wrong rule: A variable declared int can hold 2.5 or "hi"; the type is only a label. Right rule: A data type is a set of values and a set of operations defined on them, so an int variable holds only int values.
- **[4] misconception** (rule type M, wrong rule / right rule) &rarr; `LocalVariablesAutoInitialized`: wrong rule: local variables get a default value on their own. Right rule: A local variable has no value until it is assigned, and using it before then does not compile.

### L1: Unistructural / atom x text surface

L1 for declaration: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

- **Edge:** `declaration` &rarr; `declaration@L1` (has_level)
- **Exact edge logic:** declaration -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

Ways (2), each with its exact rule:

- **[0] names\_the\_element** (rule type N, identity rule): Declaration statement: a statement that introduces a variable by giving its type and name, such as int count; or double x = 0.5;.
- **[1] states\_the\_rule** (rule type S, declarative rule): Syntax: type name; or type name = expression; or type a, b, c;. Each variable must be declared before it is used, only once per scope, and its type never changes.

### L2: Multistructural / block x execution / preoperational

L2 for declaration: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

- **Edge:** `declaration` &rarr; `declaration@L2` (has_level)
- **Exact edge logic:** declaration -&gt; L2 (Multistructural): the answer applies the rules of declaration to every part of the code, in order (3 ways).

Ways (3), each with its exact rule:

- **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): When execution reaches the declaration, the variable comes into being. If there is an initializer, it is evaluated and stored. The variable's scope runs from there to the end of the enclosing block, and statements in the block run first to last.
- **[1] output\_prediction** (rule type OP, evaluation / result rule): A declaration produces no value and no output. Its effect is to fix the variable's name and type for every later compile-time check.
- **[2] one\_step\_execution** (rule type OS, state-transition rule): int x; adds x to the program state with an undefined (unassigned) value. int x = 5; adds x holding 5.

### L3: Relational / relations x function (concrete operational begins)

L3 for declaration: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

- **Edge:** `declaration` &rarr; `declaration@L3` (has_level)
- **Exact edge logic:** declaration -&gt; L3 (Relational): the answer relates the parts (5 ways).

Ways (5), each with its exact rule:

- **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): A declaration binds a legal identifier to a type, and that identifier must not already be declared in the same scope.
- **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): An assignment can store into a variable only after the variable's declaration, and only a value of a compatible type.
- **[2] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): A declaration without an initializer leaves a local unassigned, and any read before an assignment on every path is a compile error.
- **[3] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Adding final to a declaration makes the variable a constant that can be assigned only once.
- **[4] purpose\_of\_the\_whole** (rule type P, plan / role rule): Declarations make the programmer's intent explicit (names and types) so the compiler can check consistency. The usual plan is to declare each variable at its point of first use.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for declaration: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

- **Edge:** `declaration` &rarr; `declaration@L4` (has_level)
- **Exact edge logic:** declaration -&gt; L4 (Extended abstract): the answer reasons beyond the given code (6 ways).

Ways (6), each with its exact rule:

- **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `DeclaredVariableHasNoMemory`: Moving a declaration into an inner block (such as a loop body) shrinks its scope and re-creates the variable on each pass, so an accumulated value is lost. Moving it out widens its scope. Changing its type changes which values and operations are legal.
- **[1] diagnose\_an\_error** (rule type D, error rule): rule broken: A local variable may be declared only once in its scope; later changes use an assignment without the type. Kind: compile-time. Trigger class: A second 'int x = ...' for a name already declared in the same or an enclosing block: 'variable x is already defined'.
- **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: A declaration must begin with a type (type name = value;); name = value; is only an assignment to an existing variable. Kind: compile-time. Trigger class: First use of a new variable written without its type (total = 0;): 'cannot find symbol' because no variable total exists.
- **[3] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Declare every variable exactly once, in the narrowest block that covers all its uses, with an initializer when the first value is known. Declare it before (outside) a loop when its value must last across iterations or be used after the loop.
- **[4] diagnose\_an\_error** (rule type D, error rule): rule broken: Every variable must be declared (with a type) before use and referred to by exactly the declared name, inside its scope. Kind: compile-time. Trigger class: Use of a name that was never declared, was declared under another name, or is used outside the block where it was declared: 'cannot find symbol' (one missing declaration can produce several errors).
- **[5] diagnose\_an\_error** (rule type D, error rule): rule broken: The initializer's type must be assignable to the declared type. Kind: compile-time. Trigger class: Declaring int x = 1.1; or String s = 123;: 'incompatible types'.

## Same topic

`declaration` belongs to the topic **Data types and terminology (literals, identifiers, variables, declarations, assignment, expressions)** (`topic1.2.a`). The topic also contains: `assignment`, `chained_assignment`, `data_type`, `definite_assignment`, `expression`, `identifier`, `literal`, `named_constants`, `naming_convention`, `operator_precedence`, `primitive_type`, `program_trace`, `variable`, `variable_swap`.

## Rules of the concept (21)

- **Book** (SW-1e, p. 16 (pdf 26)): "A declaration statement associates a variable name with a type at compile time."
- **Book** (OT-Expressions, ): "A declaration statement declares a variable."
- **Book** (RS, ): "If Java sees you declaring a variable more than once, it generates a compiler error"
- **E** (folk-meaning rule): In English, to 'declare' something announces a fact or gives it a value, so novices think int x; already sets x to 0, or that x = 5; alone creates x. In Java a declaration creates the variable with a type, and a local variable has no usable value until it is assigned.
- **M** (wrong rule / right rule): AnyValueInAnyVariable: wrong: A variable declared int can hold 2.5 or "hi"; the type is only a label. \| right: A data type is a set of values and a set of operations defined on them, so an int variable holds only int values.
- **M** (wrong rule / right rule): LocalVariablesAutoInitialized: wrong: local variables get a default value on their own \| right: A local variable has no value until it is assigned, and using it before then does not compile.
- **M** (wrong rule / right rule): DeclaredVariableHasNoMemory: wrong: int x; without a value sets aside no memory; the variable only exists once something is assigned. \| right: A declaration creates the variable (its storage) with its type; assignment later puts a value in it.
- **T** (uneven-application rule): Points to LT (a declaration runs once when reached and creates the variable, and later assignments only update it). Applied unevenly, a student re-creates or zeroes the variable on some passes but not others, or treats a declaration further down as already in effect.
- **N** (identity rule): Declaration statement: a statement that introduces a variable by giving its type and name, such as int count; or double x = 0.5;.
- **S** (declarative rule): Syntax: type name; or type name = expression; or type a, b, c;. Each variable must be declared before it is used, only once per scope, and its type never changes.
- **LT** (operational sequencing rule): When execution reaches the declaration, the variable comes into being. If there is an initializer, it is evaluated and stored. The variable's scope runs from there to the end of the enclosing block, and statements in the block run first to last.
- **OP** (evaluation / result rule): A declaration produces no value and no output. Its effect is to fix the variable's name and type for every later compile-time check.
- **OS** (state-transition rule): int x; adds x to the program state with an undefined (unassigned) value. int x = 5; adds x holding 5.
- **R** (composition rule (with a neighbour)): with identifier: A declaration binds a legal identifier to a type, and that identifier must not already be declared in the same scope.
- **R** (composition rule (with a neighbour)): with assignment: An assignment can store into a variable only after the variable's declaration, and only a value of a compatible type.
- **R** (composition rule (with a neighbour)): with definite\_assignment: A declaration without an initializer leaves a local unassigned, and any read before an assignment on every path is a compile error.
- **R** (composition rule (with a neighbour)): with named\_constants: Adding final to a declaration makes the variable a constant that can be assigned only once.
- **P** (plan / role rule): Declarations make the programmer's intent explicit (names and types) so the compiler can check consistency. The usual plan is to declare each variable at its point of first use.
- **C** (conservation rule): Moving a declaration into an inner block (such as a loop body) shrinks its scope and re-creates the variable on each pass, so an accumulated value is lost. Moving it out widens its scope. Changing its type changes which values and operations are legal.
- **D** (error rule): rule broken: A declaration must begin with a type (type name = value;); name = value; is only an assignment to an existing variable. (compile-time)
- **D** (error rule): rule broken: A local variable may be declared only once in its scope; later changes use an assignment without the type. (compile-time)
- **D** (error rule): rule broken: Every variable must be declared (with a type) before use and referred to by exactly the declared name, inside its scope. (compile-time)
- **D** (error rule): rule broken: The initializer's type must be assignable to the declared type. (compile-time)
- **X** (applicability rule): Declare every variable exactly once, in the narrowest block that covers all its uses, with an initializer when the first value is known. Declare it before (outside) a loop when its value must last across iterations or be used after the loop.

## How it is found in code and answers (reader block)

- **Aliases:** declared, declare, declares, declaring, declaration, declarations, declared as, creates a variable, creates the variable
- **Code patterns:** `(?:^|[;{(])\s*(?:final\s+)?(?:int|double|boolean|char|long|String|float|short|byte)(?:\s*\[\s*\])*\s+[A-Za-z_]\w*\s*(?:[=;,\[:]|$)`
- **Operator symbols:** none
- **Java types:** none

## The whole prerequisite chain

- **Everything it builds on (1):** `identifier`
- **Everything that builds on it (21):** `accumulator_pattern`, `array_exchange`, `array_reversal`, `assignment`, `chained_assignment`, `compound_assignment`, `counter_pattern`, `debugging`, `definite_assignment`, `frequency_counting`, `increment_operators`, `monte_carlo_simulation`, `named_constants`, `program_trace`, `sampling_without_replacement`, `sentinel_loop`, `shuffle`, `side_effect_order`, `testing`, `two_models`, `variable_swap`

## Every edge in this view and its exact edge logic (38)

All the edges drawn in the picture, in the order: prerequisite, parallel, misconception, error, has_level, contains.

**1. `declaration` &rarr; `assignment`** (prerequisite)

- **Exact edge logic:** A variable must be declared before an assignment can store a value into it.
- **Grounding:** book\_passage
- **Composition rule (R) of `declaration` with `assignment`:** An assignment can store into a variable only after the variable's declaration, and only a value of a compatible type.
- **Composition rule (R) of `assignment` with `declaration`:** A declaration can include the first assignment (int x = 5;). Assigning to a variable that was never declared does not compile.

**2. `declaration` &rarr; `definite_assignment`** (prerequisite)

- **Exact edge logic:** A declared local variable has no defined value until it is assigned, and the compiler rejects any read before that assignment.
- **Grounding:** book\_passage
- **Composition rule (R) of `declaration` with `definite_assignment`:** A declaration without an initializer leaves a local unassigned, and any read before an assignment on every path is a compile error.
- **Composition rule (R) of `definite_assignment` with `declaration`:** A declaration without an initializer leaves the local unassigned. Writing = value in the declaration satisfies the rule at once.

**3. `declaration` &rarr; `named_constants`** (prerequisite)

- **Exact edge logic:** A constant is a declaration marked final.
- **Grounding:** book\_passage
- **Composition rule (R) of `declaration` with `named_constants`:** Adding final to a declaration makes the variable a constant that can be assigned only once.
- **Composition rule (R) of `named_constants` with `declaration`:** A constant is an ordinary declaration with the final modifier, with the same type and scope rules.

**4. `identifier` &rarr; `declaration`** (prerequisite)

- **Exact edge logic:** A declaration pairs a type with an identifier, e.g. int count;.
- **Grounding:** book\_passage
- **Composition rule (R) of `identifier` with `declaration`:** A declaration binds the identifier to a type. Every later use must repeat exactly that spelling, or the compiler cannot resolve it.
- **Composition rule (R) of `declaration` with `identifier`:** A declaration binds a legal identifier to a type, and that identifier must not already be declared in the same scope.

**5. `declaration` &rarr; `AnyValueInAnyVariable`** (misconception)

- **Exact edge logic (the wrong rule):** A variable declared int can hold 2.5 or "hi"; the type is only a label.
- **Twin logic (the right rule):** A data type is a set of values and a set of operations defined on them, so an int variable holds only int values.
- **Role:** context

**6. `declaration` &rarr; `DeclaredVariableHasNoMemory`** (misconception)

- **Exact edge logic (the wrong rule):** int x; without a value sets aside no memory; the variable only exists once something is assigned.
- **Twin logic (the right rule):** A declaration creates the variable (its storage) with its type; assignment later puts a value in it.
- **Role:** primary

**7. `declaration` &rarr; `LocalVariablesAutoInitialized`** (misconception)

- **Exact edge logic (the wrong rule):** local variables get a default value on their own
- **Twin logic (the right rule):** A local variable has no value until it is assigned, and using it before then does not compile.
- **Role:** context

**8. `data_type` &rarr; `AnyValueInAnyVariable`** (misconception)

- **Exact edge logic (the wrong rule):** A variable declared int can hold 2.5 or "hi"; the type is only a label.
- **Twin logic (the right rule):** A data type is a set of values and a set of operations defined on them, so an int variable holds only int values.
- **Role:** primary

**9. `definite_assignment` &rarr; `LocalVariablesAutoInitialized`** (misconception)

- **Exact edge logic (the wrong rule):** local variables get a default value on their own
- **Twin logic (the right rule):** A local variable has no value until it is assigned, and using it before then does not compile.
- **Role:** primary

**10. `variable` &rarr; `AnyValueInAnyVariable`** (misconception)

- **Exact edge logic (the wrong rule):** A variable declared int can hold 2.5 or "hi"; the type is only a label.
- **Twin logic (the right rule):** A data type is a set of values and a set of operations defined on them, so an int variable holds only int values.
- **Role:** context

**11. `variable` &rarr; `DeclaredVariableHasNoMemory`** (misconception)

- **Exact edge logic (the wrong rule):** int x; without a value sets aside no memory; the variable only exists once something is assigned.
- **Twin logic (the right rule):** A declaration creates the variable (its storage) with its type; assignment later puts a value in it.
- **Role:** context

**12. `variable` &rarr; `LocalVariablesAutoInitialized`** (misconception)

- **Exact edge logic (the wrong rule):** int x; inside main starts at 0, so x can be used before anything is assigned to it.
- **Twin logic (the right rule):** A local variable has no value until it is assigned, and using it before then does not compile.
- **Role:** context

**13. `declaration` &rarr; `DeclarationWithoutType`** (error)

- **Exact edge logic (the wrong rule):** Writes name = value; to declare a new variable.
- **Twin logic (the right rule):** A declaration needs a type: type name = value;
- **Role:** primary

**14. `declaration` &rarr; `RedeclareToReassign`** (error)

- **Exact edge logic (the wrong rule):** Writes int x = 5; ... int x = 10; to change x.
- **Twin logic (the right rule):** A declaration gives a variable its name and type; a later change of value is an assignment statement such as x = 10;, not a second declaration.
- **Role:** primary

**15. `declaration` &rarr; `UndeclaredOrRenamedVariable`** (error)

- **Exact edge logic (the wrong rule):** Uses a variable that was never declared, or under a different name (studentTotal vs total).
- **Twin logic (the right rule):** Every variable must be declared, and used with exactly the declared name.
- **Role:** context

**16. `assignment` &rarr; `RedeclareToReassign`** (error)

- **Exact edge logic (the wrong rule):** Writes int x = 5; ... int x = 10; to change x.
- **Twin logic (the right rule):** A declaration gives a variable its name and type; a later change of value is an assignment statement such as x = 10;, not a second declaration.
- **Role:** context

**17. `identifier` &rarr; `UndeclaredOrRenamedVariable`** (error)

- **Exact edge logic (the wrong rule):** Uses a variable that was never declared, or under a different name (studentTotal vs total).
- **Twin logic (the right rule):** Every variable must be declared, and used with exactly the declared name.
- **Role:** context

**18. `variable` &rarr; `UndeclaredOrRenamedVariable`** (error)

- **Exact edge logic (the wrong rule):** Uses a variable that was never declared, or under a different name (studentTotal vs total).
- **Twin logic (the right rule):** Every variable must be declared, and used with exactly the declared name.
- **Role:** primary

**19. `declaration` &rarr; `declaration@L0`** (has_level)

- **Exact edge logic:** declaration -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (5 ways).
  - **[0] everyday\_reading** (rule type E, folk-meaning rule): In English, to 'declare' something announces a fact or gives it a value, so novices think int x; already sets x to 0, or that x = 5; alone creates x. In Java a declaration creates the variable with a type, and a local variable has no usable value until it is assigned.
  - **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `DeclaredVariableHasNoMemory`: wrong rule: int x; without a value sets aside no memory; the variable only exists once something is assigned. Right rule: A declaration creates the variable (its storage) with its type; assignment later puts a value in it.
  - **[2] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `DeclaredVariableHasNoMemory`: Points to LT (a declaration runs once when reached and creates the variable, and later assignments only update it). Applied unevenly, a student re-creates or zeroes the variable on some passes but not others, or treats a declaration further down as already in effect. (here mixing in: "int x; without a value sets aside no memory; the variable only exists once something is assigned")
  - **[3] misconception** (rule type M, wrong rule / right rule) &rarr; `AnyValueInAnyVariable`: wrong rule: A variable declared int can hold 2.5 or "hi"; the type is only a label. Right rule: A data type is a set of values and a set of operations defined on them, so an int variable holds only int values.
  - **[4] misconception** (rule type M, wrong rule / right rule) &rarr; `LocalVariablesAutoInitialized`: wrong rule: local variables get a default value on their own. Right rule: A local variable has no value until it is assigned, and using it before then does not compile.

**20. `declaration` &rarr; `declaration@L1`** (has_level)

- **Exact edge logic:** declaration -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).
  - **[0] names\_the\_element** (rule type N, identity rule): Declaration statement: a statement that introduces a variable by giving its type and name, such as int count; or double x = 0.5;.
  - **[1] states\_the\_rule** (rule type S, declarative rule): Syntax: type name; or type name = expression; or type a, b, c;. Each variable must be declared before it is used, only once per scope, and its type never changes.

**21. `declaration` &rarr; `declaration@L2`** (has_level)

- **Exact edge logic:** declaration -&gt; L2 (Multistructural): the answer applies the rules of declaration to every part of the code, in order (3 ways).
  - **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): When execution reaches the declaration, the variable comes into being. If there is an initializer, it is evaluated and stored. The variable's scope runs from there to the end of the enclosing block, and statements in the block run first to last.
  - **[1] output\_prediction** (rule type OP, evaluation / result rule): A declaration produces no value and no output. Its effect is to fix the variable's name and type for every later compile-time check.
  - **[2] one\_step\_execution** (rule type OS, state-transition rule): int x; adds x to the program state with an undefined (unassigned) value. int x = 5; adds x holding 5.

**22. `declaration` &rarr; `declaration@L3`** (has_level)

- **Exact edge logic:** declaration -&gt; L3 (Relational): the answer relates the parts (5 ways).
  - **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): A declaration binds a legal identifier to a type, and that identifier must not already be declared in the same scope.
  - **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): An assignment can store into a variable only after the variable's declaration, and only a value of a compatible type.
  - **[2] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): A declaration without an initializer leaves a local unassigned, and any read before an assignment on every path is a compile error.
  - **[3] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Adding final to a declaration makes the variable a constant that can be assigned only once.
  - **[4] purpose\_of\_the\_whole** (rule type P, plan / role rule): Declarations make the programmer's intent explicit (names and types) so the compiler can check consistency. The usual plan is to declare each variable at its point of first use.

**23. `declaration` &rarr; `declaration@L4`** (has_level)

- **Exact edge logic:** declaration -&gt; L4 (Extended abstract): the answer reasons beyond the given code (6 ways).
  - **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `DeclaredVariableHasNoMemory`: Moving a declaration into an inner block (such as a loop body) shrinks its scope and re-creates the variable on each pass, so an accumulated value is lost. Moving it out widens its scope. Changing its type changes which values and operations are legal.
  - **[1] diagnose\_an\_error** (rule type D, error rule): rule broken: A local variable may be declared only once in its scope; later changes use an assignment without the type. Kind: compile-time. Trigger class: A second 'int x = ...' for a name already declared in the same or an enclosing block: 'variable x is already defined'.
  - **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: A declaration must begin with a type (type name = value;); name = value; is only an assignment to an existing variable. Kind: compile-time. Trigger class: First use of a new variable written without its type (total = 0;): 'cannot find symbol' because no variable total exists.
  - **[3] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Declare every variable exactly once, in the narrowest block that covers all its uses, with an initializer when the first value is known. Declare it before (outside) a loop when its value must last across iterations or be used after the loop.
  - **[4] diagnose\_an\_error** (rule type D, error rule): rule broken: Every variable must be declared (with a type) before use and referred to by exactly the declared name, inside its scope. Kind: compile-time. Trigger class: Use of a name that was never declared, was declared under another name, or is used outside the block where it was declared: 'cannot find symbol' (one missing declaration can produce several errors).
  - **[5] diagnose\_an\_error** (rule type D, error rule): rule broken: The initializer's type must be assignable to the declared type. Kind: compile-time. Trigger class: Declaring int x = 1.1; or String s = 123;: 'incompatible types'.

**24. `topic1.2.a` &rarr; `declaration`** (contains)

- topic `topic1.2.a` contains `declaration`

**25. `topic1.2.a` &rarr; `assignment`** (contains)

- topic `topic1.2.a` contains `assignment`

**26. `topic1.2.a` &rarr; `chained_assignment`** (contains)

- topic `topic1.2.a` contains `chained_assignment`

**27. `topic1.2.a` &rarr; `data_type`** (contains)

- topic `topic1.2.a` contains `data_type`

**28. `topic1.2.a` &rarr; `definite_assignment`** (contains)

- topic `topic1.2.a` contains `definite_assignment`

**29. `topic1.2.a` &rarr; `expression`** (contains)

- topic `topic1.2.a` contains `expression`

**30. `topic1.2.a` &rarr; `identifier`** (contains)

- topic `topic1.2.a` contains `identifier`

**31. `topic1.2.a` &rarr; `literal`** (contains)

- topic `topic1.2.a` contains `literal`

**32. `topic1.2.a` &rarr; `named_constants`** (contains)

- topic `topic1.2.a` contains `named_constants`

**33. `topic1.2.a` &rarr; `naming_convention`** (contains)

- topic `topic1.2.a` contains `naming_convention`

**34. `topic1.2.a` &rarr; `operator_precedence`** (contains)

- topic `topic1.2.a` contains `operator_precedence`

**35. `topic1.2.a` &rarr; `primitive_type`** (contains)

- topic `topic1.2.a` contains `primitive_type`

**36. `topic1.2.a` &rarr; `program_trace`** (contains)

- topic `topic1.2.a` contains `program_trace`

**37. `topic1.2.a` &rarr; `variable`** (contains)

- topic `topic1.2.a` contains `variable`

**38. `topic1.2.a` &rarr; `variable_swap`** (contains)

- topic `topic1.2.a` contains `variable_swap`
