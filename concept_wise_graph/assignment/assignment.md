# assignment (`assignment`)

= stores the computed value of the right side

Section 1.2 Built-in Types of Data, topic 1.2.a Data types and terminology (literals, identifiers, variables, declarations, assignment, expressions).

![The knowledge graph around assignment](assignment.png)

## At a glance

- **Needs first:** `declaration`, `variable`
- **Leads to:** `array_exchange`, `chained_assignment`, `compound_assignment`, `increment_operators`, `program_trace`, `variable_swap`
- **Learned alongside:** `comparison_operators`
- **Misconceptions:** `AssignCompares`, `AssignmentAddsToTarget`, `AssignmentCopiesObject`, `AssignmentEmptiesSource`, `AssignmentExchangesValues`, `AssignmentIsEquation`, `AssignmentNotExpression`, `AssignmentOppositeDirection`, `PrintedTextIsExecuted`, `SwapWithoutTemp`, `VariableKeepsOldValue`, `VariablesHoldExpressions`
- **Errors:** `AssignToFinal`, `ExpressionOnLeftOfAssignment`, `RedeclareToReassign`
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 64 edges around this concept. The edge logic, the wrong and right rules and the exact rules of the ways are copied word for word from the graph.

## To work on (1)

- misconceptions with no L0 way linked to them: PrintedTextIsExecuted

## What it needs first (2)

A prerequisite edge means the other concept has to be understood before `assignment`.

### `declaration` comes before `assignment`

*int x; -- introduces a variable name and its type*

- **Edge:** `pre:declaration->assignment`
- **Exact edge logic:** A variable must be declared before an assignment can store a value into it.
- **Grounding:** book\_passage
- **Composition rule (R) of `assignment` with `declaration`:** A declaration can include the first assignment (int x = 5;). Assigning to a variable that was never declared does not compile.
- **Composition rule (R) of `declaration` with `assignment`:** An assignment can store into a variable only after the variable's declaration, and only a value of a compatible type.

### `variable` comes before `assignment`

*a named, typed box that holds a value*

- **Edge:** `pre:variable->assignment`
- **Exact edge logic:** Assignment needs a declared variable on its left side to store the computed value into.
- **Grounding:** book\_passage
- **Composition rule (R) of `assignment` with `variable`:** The left side must be a declared variable whose type accepts the value. Assignment is how that variable's value changes.
- **Composition rule (R) of `variable` with `assignment`:** Assignment is the only statement that changes a variable, and its left-hand side must be a single variable.

## What it leads to (6)

These concepts need `assignment` first.

### `assignment` comes before `array_exchange`

*swap a[i] and a[j] through a temporary variable*

- **Edge:** `pre:assignment->array_exchange`
- **Exact edge logic:** The exchange is three assignments in a fixed order through a temporary variable.
- **Grounding:** book\_passage
- **Composition rule (R) of `assignment` with `array_exchange`:** Exchanging a[i] and a[j] takes three assignments in a fixed order through a temporary, because each assignment overwrites its target.
- **Composition rule (R) of `array_exchange` with `assignment`:** Each of the three steps is an ordinary assignment whose left side is a single variable (here an array element), executed in order.

### `assignment` comes before `chained_assignment`

*a = b = 0 assigns right to left*

- **Edge:** `pre:assignment->chained_assignment`
- **Exact edge logic:** An assignment such as x = y is treated as an expression: it assigns the value of y to x and evaluates to that value.
- **Grounding:** questionable
- **Composition rule (R) of `assignment` with `chained_assignment`:** Because an assignment is an expression whose value is the value stored, and = groups right to left, a = b = 0 first stores 0 in b and then stores that 0 in a.
- **Composition rule (R) of `chained_assignment` with `assignment`:** A chain works only because an assignment is itself an expression whose value is the value stored, so it can be the right side of another =.

### `assignment` comes before `compound_assignment`

*x += e, x -= e, ... include a hidden cast*

- **Edge:** `pre:assignment->compound_assignment`
- **Exact edge logic:** x op= e is shorthand for the assignment x = x op e.
- **Grounding:** book\_passage
- **Composition rule (R) of `assignment` with `compound_assignment`:** x op= e is shorthand for x = x op e. The left variable's current value is fetched first and then combined with e.
- **Composition rule (R) of `compound_assignment` with `assignment`:** x op= e is shorthand for the assignment x = x op e, so the new value depends on the old one (x is read, then written).

### `assignment` comes before `increment_operators`

*++ / -- (and +=)*

- **Edge:** `pre:assignment->increment_operators`
- **Exact edge logic:** i++ is shorthand for the assignment i = i + 1.
- **Grounding:** book\_passage
- **Composition rule (R) of `assignment` with `increment_operators`:** As a statement, i++ has the same effect as the assignment i = i + 1.
- **Composition rule (R) of `increment_operators` with `assignment`:** i++ is shorthand for the assignment i = i + 1 (and i += k for i = i + k), so it changes the variable's stored value.

### `assignment` comes before `program_trace`

*Trace (table of variable values): a table of the values of the variables after each statement, used to check what code does*

- **Edge:** `pre:assignment->program_trace`
- **Exact edge logic:** A trace records the value each variable holds after each assignment statement runs.
- **Grounding:** book\_passage
- **Composition rule (R) of `assignment` with `program_trace`:** A trace records the value of each variable after each assignment runs, one row per statement.
- **Composition rule (R) of `program_trace` with `assignment`:** Each assignment statement produces the next row of the trace, changing exactly the column of the variable on its left-hand side.

### `assignment` comes before `variable_swap`

*exchanging two variables needs a temporary*

- **Edge:** `pre:assignment->variable_swap`
- **Exact edge logic:** The three assignments int t = a; a = b; b = t; exchange the values of a and b, as a trace of the variable values after each statement shows.
- **Grounding:** book\_passage
- **Composition rule (R) of `assignment` with `variable_swap`:** int t = a; a = b; b = t; works only in this order, because every assignment destroys its left variable's old value.
- **Composition rule (R) of `variable_swap` with `assignment`:** A swap is three assignments whose order matters, because each one overwrites the old value of its left variable.

## Learned alongside (1)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

### `assignment` alongside `comparison_operators`

*== != &lt; &gt; &lt;= &gt;=*

- **Edge:** `par:assignment~comparison_operators`
- **Exact edge logic:** x = y stores the value of y in x (a statement with a side effect); x == y only tests whether the two values are equal and gives a boolean. Writing = where == is meant is a compile error with int operands and a silent bug with boolean operands.
- **Grounding:** book\_passage

## Misconceptions (12)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### AssignCompares

- **Edge:** `assignment` &rarr; `AssignCompares` (misconception)
- **Exact edge logic (the wrong rule):** x = y checks whether x and y are equal.
- **Twin logic (the right rule):** x = y copies the value of y into x; x == y is what compares them.
- **Wrong belief (on the node):** = compares two values instead of assigning
- **Correct rule (on the node):** x = y copies the value of y into x; x == y is what compares them.
- **Provenance:** published
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [2] misconception, exact rule:** wrong rule: = compares two values instead of assigning. Right rule: x = y copies the value of y into x; x == y is what compares them.
- **Edge `comparison_operators` &rarr; `AssignCompares`, exact edge logic:** = compares two values instead of assigning **Twin logic:** x = y copies the value of y into x; x == y is what compares them. (role: context)
- **Edge `if_statement` &rarr; `AssignCompares`, exact edge logic:** = compares two values instead of assigning **Twin logic:** x = y copies the value of y into x; x == y is what compares them. (role: context)

### AssignmentAddsToTarget

- **Edge:** `assignment` &rarr; `AssignmentAddsToTarget` (misconception)
- **Exact edge logic (the wrong rule):** a = b adds the value of b to the value already in a (the accumulator model).
- **Twin logic (the right rule):** a = b replaces the old value of a with the value of b; the old value is lost.
- **Wrong belief (on the node):** a = b adds the value of b to the value already in a (the accumulator model).
- **Correct rule (on the node):** a = b replaces the old value of a with the value of b; the old value is lost.
- **Provenance:** published
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [5] misconception, exact rule:** wrong rule: a = b adds the value of b to the value already in a (the accumulator model). Right rule: a = b replaces the old value of a with the value of b; the old value is lost.

### AssignmentCopiesObject

- **Edge:** `assignment` &rarr; `AssignmentCopiesObject` (misconception)
- **Exact edge logic (the wrong rule):** b = a; for an array makes b a separate copy, so changing b[i] leaves a[i] unchanged.
- **Twin logic (the right rule):** b = a; copies only the reference, so a and b refer to the same array and b[i] = v also changes a[i].
- **Wrong belief (on the node):** assigning a reference copies the object
- **Correct rule (on the node):** b = a; copies only the reference, so a and b refer to the same array and b[i] = v also changes a[i].
- **Provenance:** published
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [11] misconception, exact rule:** wrong rule: assigning a reference copies the object. Right rule: b = a; copies only the reference, so a and b refer to the same array and b[i] = v also changes a[i].
- **Edge `array_aliasing` &rarr; `AssignmentCopiesObject`, exact edge logic:** assigning a reference copies the object **Twin logic:** b = a; copies only the reference, so a and b refer to the same array and b[i] = v also changes a[i]. (role: primary)
- **Edge `array_copy` &rarr; `AssignmentCopiesObject`, exact edge logic:** assigning a reference copies the object **Twin logic:** b = a; copies only the reference, so a and b refer to the same array and b[i] = v also changes a[i]. (role: context)

### AssignmentEmptiesSource

- **Edge:** `assignment` &rarr; `AssignmentEmptiesSource` (misconception)
- **Exact edge logic (the wrong rule):** After b = a, a no longer holds a value, as if the value had been moved.
- **Twin logic (the right rule):** Assignment copies; the variable on the right keeps its value.
- **Wrong belief (on the node):** After b = a, a no longer holds a value, as if the value had been moved.
- **Correct rule (on the node):** Assignment copies; the variable on the right keeps its value.
- **Provenance:** published
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [8] misconception, exact rule:** wrong rule: After b = a, a no longer holds a value, as if the value had been moved. Right rule: Assignment copies; the variable on the right keeps its value.

### AssignmentExchangesValues

- **Edge:** `assignment` &rarr; `AssignmentExchangesValues` (misconception)
- **Exact edge logic (the wrong rule):** b = a exchanges the values of a and b.
- **Twin logic (the right rule):** b = a copies a into b and leaves a unchanged; an exchange needs a temporary variable and three assignments.
- **Wrong belief (on the node):** b = a exchanges the values of a and b.
- **Correct rule (on the node):** b = a copies a into b and leaves a unchanged; an exchange needs a temporary variable and three assignments.
- **Provenance:** published
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [7] misconception, exact rule:** wrong rule: b = a exchanges the values of a and b. Right rule: b = a copies a into b and leaves a unchanged; an exchange needs a temporary variable and three assignments.
- **Edge `variable_swap` &rarr; `AssignmentExchangesValues`, exact edge logic:** b = a exchanges the values of a and b. **Twin logic:** b = a copies a into b and leaves a unchanged; an exchange needs a temporary variable and three assignments. (role: context)

### AssignmentIsEquation

- **Edge:** `assignment` &rarr; `AssignmentIsEquation` (misconception)
- **Exact edge logic (the wrong rule):** An assignment states a lasting equality between its two sides, so y = x - y can be solved like the equation x = 2y and x = x + 5 relates two equal quantities.
- **Twin logic (the right rule):** An assignment is a one-time action: evaluate the right side with current values, then store the result in the left variable.
- **Wrong belief (on the node):** An assignment states a lasting equality between its two sides, so y = x - y can be solved like the equation x = 2y and x = x + 5 relates two equal quantities.
- **Correct rule (on the node):** An assignment is a one-time action: evaluate the right side with current values, then store the result in the left variable.
- **Provenance:** published
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [6] misconception, exact rule:** wrong rule: An assignment states a lasting equality between its two sides, so y = x - y can be solved like the equation x = 2y and x = x + 5 relates two equal quantities. Right rule: An assignment is a one-time action: evaluate the right side with current values, then store the result in the left variable.
- **Edge `expression` &rarr; `AssignmentIsEquation`, exact edge logic:** An assignment states a lasting equality between its two sides, so y = x - y can be solved like the equation x = 2y and x = x + 5 relates two equal quantities. **Twin logic:** An assignment is a one-time action: evaluate the right side with current values, then store the result in the left variable. (role: context)

### AssignmentNotExpression

- **Edge:** `assignment` &rarr; `AssignmentNotExpression` (misconception)
- **Exact edge logic (the wrong rule):** An assignment cannot be used inside a larger expression, so a condition like (x = read()) != v is not allowed.
- **Twin logic (the right rule):** An assignment is an expression whose value is the value assigned, so (x = v) both stores v in x and gives v.
- **Wrong belief (on the node):** an assignment cannot be used inside a larger expression
- **Correct rule (on the node):** An assignment is an expression whose value is the value assigned, so (x = v) both stores v in x and gives v.
- **Provenance:** published
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [3] misconception, exact rule:** wrong rule: an assignment cannot be used inside a larger expression. Right rule: An assignment is an expression whose value is the value assigned, so (x = v) both stores v in x and gives v.
- **Edge `chained_assignment` &rarr; `AssignmentNotExpression`, exact edge logic:** an assignment cannot be used inside a larger expression **Twin logic:** An assignment is an expression whose value is the value assigned, so (x = v) both stores v in x and gives v. (role: context)
- **Edge `expression` &rarr; `AssignmentNotExpression`, exact edge logic:** An assignment cannot be used inside a larger expression, so a condition like (x = read()) != v is not allowed. **Twin logic:** An assignment is an expression whose value is the value assigned, so (x = v) both stores v in x and gives v. (role: context)
- **Edge `read_loop_idiom` &rarr; `AssignmentNotExpression`, exact edge logic:** A read and a test cannot be combined, so while ((x = read()) != end) is not allowed. **Twin logic:** while ((x = read()) != end) reads a value into x and tests that same value in one expression. (role: context)

### AssignmentOppositeDirection

- **Edge:** `assignment` &rarr; `AssignmentOppositeDirection` (misconception)
- **Exact edge logic (the wrong rule):** a = b copies the value of a into b.
- **Twin logic (the right rule):** Assignment stores the value of the right side into the variable on the left.
- **Wrong belief (on the node):** a = b copies the value of a into b.
- **Correct rule (on the node):** Assignment stores the value of the right side into the variable on the left.
- **Provenance:** published
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [4] misconception, exact rule:** wrong rule: a = b copies the value of a into b. Right rule: Assignment stores the value of the right side into the variable on the left.

### PrintedTextIsExecuted

- **Edge:** `assignment` &rarr; `PrintedTextIsExecuted` (misconception)
- **Exact edge logic (the wrong rule):** System.out.println("x is 5"); sets x to 5 (text inside the quotes is run as code).
- **Twin logic (the right rule):** Characters inside double quotes are printed literally; println only displays them and changes no variable. Only an assignment such as x = 5; sets x.
- **Wrong belief (on the node):** System.out.println("x is 5"); sets x to 5 (text inside the quotes is run as code).
- **Correct rule (on the node):** Characters inside double quotes are printed literally; println only displays them and changes no variable. Only an assignment such as x = 5; sets x.
- **Provenance:** scenario
- **Role of this concept:** context
- **L0 way linked to it:** no
- **Edge `println` &rarr; `PrintedTextIsExecuted`, exact edge logic:** System.out.println("x is 5"); sets x to 5 (text inside the quotes is run as code). **Twin logic:** Characters inside double quotes are printed literally; println only displays them and changes no variable. Only an assignment such as x = 5; sets x. (role: primary)
- **Edge `string_literal` &rarr; `PrintedTextIsExecuted`, exact edge logic:** System.out.println("x is 5"); sets x to 5 (text inside the quotes is run as code). **Twin logic:** Characters inside double quotes are printed literally; println only displays them and changes no variable. Only an assignment such as x = 5; sets x. (role: context)

### SwapWithoutTemp

- **Edge:** `assignment` &rarr; `SwapWithoutTemp` (misconception)
- **Exact edge logic (the wrong rule):** a[i] = a[j]; a[j] = a[i]; exchanges the two values.
- **Twin logic (the right rule):** A temporary variable must save a[i] before it is overwritten.
- **Wrong belief (on the node):** a[i] = a[j]; a[j] = a[i]; exchanges the two values.
- **Correct rule (on the node):** A temporary variable must save a[i] before it is overwritten.
- **Provenance:** textbook
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [10] misconception, exact rule:** wrong rule: a[i] = a[j]; a[j] = a[i]; exchanges the two values. Right rule: A temporary variable must save a[i] before it is overwritten.
- **Edge `array_exchange` &rarr; `SwapWithoutTemp`, exact edge logic:** a[i] = a[j]; a[j] = a[i]; exchanges the two values. **Twin logic:** A temporary variable must save a[i] before it is overwritten. (role: primary)
- **Edge `variable_swap` &rarr; `SwapWithoutTemp`, exact edge logic:** a[i] = a[j]; a[j] = a[i]; exchanges the two values. **Twin logic:** A temporary variable must save a[i] before it is overwritten. (role: context)

### VariableKeepsOldValue

- **Edge:** `assignment` &rarr; `VariableKeepsOldValue` (misconception)
- **Exact edge logic (the wrong rule):** A variable keeps its first value after a new assignment (the static model).
- **Twin logic (the right rule):** Each assignment or read replaces the variable's current value.
- **Wrong belief (on the node):** A variable keeps its first value after a new assignment (the static model).
- **Correct rule (on the node):** Each assignment or read replaces the variable's current value.
- **Provenance:** published
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [12] misconception, exact rule:** wrong rule: A variable keeps its first value after a new assignment (the static model). Right rule: Each assignment or read replaces the variable's current value.
- **Edge `variable` &rarr; `VariableKeepsOldValue`, exact edge logic:** A variable keeps its first value after a new assignment (the static model). **Twin logic:** Each assignment or read replaces the variable's current value. (role: primary)

### VariablesHoldExpressions

- **Edge:** `assignment` &rarr; `VariablesHoldExpressions` (misconception)
- **Exact edge logic (the wrong rule):** y = x + k; makes y always equal to x + k, so when x changes later, y changes too.
- **Twin logic (the right rule):** y = x + k; stores the value that x + k has at that moment, so later changes to x do not change y.
- **Wrong belief (on the node):** = stores the expression itself, not its computed value
- **Correct rule (on the node):** y = x + k; stores the value that x + k has at that moment, so later changes to x do not change y.
- **Provenance:** published
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [1] misconception, exact rule:** wrong rule: = stores the expression itself, not its computed value. Right rule: y = x + k; stores the value that x + k has at that moment, so later changes to x do not change y.
- **L0 way [9] inconsistent\_trace, exact rule:** Points to LT (evaluate the right side with current values, then overwrite the left variable). Applied unevenly, a student traces one segment correctly but reads the next as simultaneous equations or as a swap, giving 15 and 15 for one segment and 5 and 10 for the other. (here mixing in: "= stores the expression itself, not its computed value")
- **Edge `expression` &rarr; `VariablesHoldExpressions`, exact edge logic:** = stores the expression itself, not its computed value **Twin logic:** y = x + k; stores the value that x + k has at that moment, so later changes to x do not change y. (role: context)
- **Edge `variable` &rarr; `VariablesHoldExpressions`, exact edge logic:** = stores the expression itself, not its computed value **Twin logic:** y = x + k; stores the value that x + k has at that moment, so later changes to x do not change y. (role: context)

## Errors (3)

An error edge states the rule that gets broken in a program, and the right rule.

### AssignToFinal

- **Edge:** `assignment` &rarr; `AssignToFinal` (error)
- **Exact edge logic (the wrong rule):** Assigns a new value to a variable declared final.
- **Twin logic (the right rule):** A final variable cannot be reassigned after it is initialized; the compiler reports an error.
- **Wrong belief (on the node):** Assigns a new value to a variable declared final.
- **Correct rule (on the node):** A final variable cannot be reassigned after it is initialized; the compiler reports an error.
- **Provenance:** published
- **Role of this concept:** context
- **Edge `compile_time_error` &rarr; `AssignToFinal`, exact edge logic:** Assigns a new value to a variable declared final. **Twin logic:** A final variable cannot be reassigned after it is initialized; the compiler reports an error. (role: context)
- **Edge `named_constants` &rarr; `AssignToFinal`, exact edge logic:** Assigns a new value to a variable declared final. **Twin logic:** A final variable cannot be reassigned after it is initialized; the compiler reports an error. (role: primary)

### ExpressionOnLeftOfAssignment

- **Edge:** `assignment` &rarr; `ExpressionOnLeftOfAssignment` (error)
- **Exact edge logic (the wrong rule):** Writes a + b = c; or 7 = a; as if = were a math equation.
- **Twin logic (the right rule):** The left side of an assignment must be a single variable; only the right side can be an expression.
- **Wrong belief (on the node):** Writes a + b = c; or 7 = a; as if = were a math equation.
- **Correct rule (on the node):** The left side of an assignment must be a single variable; only the right side can be an expression.
- **Provenance:** textbook
- **Role of this concept:** primary
- **Edge `expression` &rarr; `ExpressionOnLeftOfAssignment`, exact edge logic:** Writes a + b = c; or 7 = a; as if = were a math equation. **Twin logic:** The left side of an assignment must be a single variable; only the right side can be an expression. (role: context)

### RedeclareToReassign

- **Edge:** `assignment` &rarr; `RedeclareToReassign` (error)
- **Exact edge logic (the wrong rule):** Writes int x = 5; ... int x = 10; to change x.
- **Twin logic (the right rule):** A declaration gives a variable its name and type; a later change of value is an assignment statement such as x = 10;, not a second declaration.
- **Wrong belief (on the node):** Writes int x = 5; ... int x = 10; to change x.
- **Correct rule (on the node):** A declaration gives a variable its name and type; a later change of value is an assignment statement such as x = 10;, not a second declaration.
- **Provenance:** textbook
- **Role of this concept:** context
- **Edge `declaration` &rarr; `RedeclareToReassign`, exact edge logic:** Writes int x = 5; ... int x = 10; to change x. **Twin logic:** A declaration gives a variable its name and type; a later change of value is an assignment statement such as x = 10;, not a second declaration. (role: primary)

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for assignment: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to assignment agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

- **Edge:** `assignment` &rarr; `assignment@L0` (has_level)
- **Exact edge logic:** assignment -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (13 ways).

Ways (13), each with its exact rule:

- **[0] everyday\_reading** (rule type E, folk-meaning rule): In maths, = states a symmetric, lasting equality (a = b means b = a, and x = x + 5 is false). In Java, = is a one-time, directed action: evaluate the right side, then store the result in the variable on the left.
- **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `VariablesHoldExpressions`: wrong rule: = stores the expression itself, not its computed value. Right rule: y = x + k; stores the value that x + k has at that moment, so later changes to x do not change y.
- **[2] misconception** (rule type M, wrong rule / right rule) &rarr; `AssignCompares`: wrong rule: = compares two values instead of assigning. Right rule: x = y copies the value of y into x; x == y is what compares them.
- **[3] misconception** (rule type M, wrong rule / right rule) &rarr; `AssignmentNotExpression`: wrong rule: an assignment cannot be used inside a larger expression. Right rule: An assignment is an expression whose value is the value assigned, so (x = v) both stores v in x and gives v.
- **[4] misconception** (rule type M, wrong rule / right rule) &rarr; `AssignmentOppositeDirection`: wrong rule: a = b copies the value of a into b. Right rule: Assignment stores the value of the right side into the variable on the left.
- **[5] misconception** (rule type M, wrong rule / right rule) &rarr; `AssignmentAddsToTarget`: wrong rule: a = b adds the value of b to the value already in a (the accumulator model). Right rule: a = b replaces the old value of a with the value of b; the old value is lost.
- **[6] misconception** (rule type M, wrong rule / right rule) &rarr; `AssignmentIsEquation`: wrong rule: An assignment states a lasting equality between its two sides, so y = x - y can be solved like the equation x = 2y and x = x + 5 relates two equal quantities. Right rule: An assignment is a one-time action: evaluate the right side with current values, then store the result in the left variable.
- **[7] misconception** (rule type M, wrong rule / right rule) &rarr; `AssignmentExchangesValues`: wrong rule: b = a exchanges the values of a and b. Right rule: b = a copies a into b and leaves a unchanged; an exchange needs a temporary variable and three assignments.
- **[8] misconception** (rule type M, wrong rule / right rule) &rarr; `AssignmentEmptiesSource`: wrong rule: After b = a, a no longer holds a value, as if the value had been moved. Right rule: Assignment copies; the variable on the right keeps its value.
- **[9] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `VariablesHoldExpressions`: Points to LT (evaluate the right side with current values, then overwrite the left variable). Applied unevenly, a student traces one segment correctly but reads the next as simultaneous equations or as a swap, giving 15 and 15 for one segment and 5 and 10 for the other. (here mixing in: "= stores the expression itself, not its computed value")
- **[10] misconception** (rule type M, wrong rule / right rule) &rarr; `SwapWithoutTemp`: wrong rule: a[i] = a[j]; a[j] = a[i]; exchanges the two values. Right rule: A temporary variable must save a[i] before it is overwritten.
- **[11] misconception** (rule type M, wrong rule / right rule) &rarr; `AssignmentCopiesObject`: wrong rule: assigning a reference copies the object. Right rule: b = a; copies only the reference, so a and b refer to the same array and b[i] = v also changes a[i].
- **[12] misconception** (rule type M, wrong rule / right rule) &rarr; `VariableKeepsOldValue`: wrong rule: A variable keeps its first value after a new assignment (the static model). Right rule: Each assignment or read replaces the variable's current value.

### L1: Unistructural / atom x text surface

L1 for assignment: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

- **Edge:** `assignment` &rarr; `assignment@L1` (has_level)
- **Exact edge logic:** assignment -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

Ways (2), each with its exact rule:

- **[0] names\_the\_element** (rule type N, identity rule): Assignment statement: the statement variable = expression; which stores a data-type value in a variable.
- **[1] states\_the\_rule** (rule type S, declarative rule): The left-hand side must be a single variable. The right-hand side can be any expression whose type is compatible with the variable's type. = is not mathematical equality (a + b = b + a and 1 = a are illegal).

### L2: Multistructural / block x execution / preoperational

L2 for assignment: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

- **Edge:** `assignment` &rarr; `assignment@L2` (has_level)
- **Exact edge logic:** assignment -&gt; L2 (Multistructural): the answer applies the rules of assignment to every part of the code, in order (3 ways).

Ways (3), each with its exact rule:

- **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): First the right-hand side is fully evaluated using the variables' current values (left to right). Then that value is stored in the left-hand variable, replacing its old value, and execution moves to the next statement.
- **[1] output\_prediction** (rule type OP, evaluation / result rule): As a statement it prints nothing; its result is the new value of the left variable (after c = a + b; with a = 1234 and b = 99, c is 1333). Used as an expression, its value is the value assigned.
- **[2] one\_step\_execution** (rule type OS, state-transition rule): Exactly one variable, the left one, changes, and its old value is lost. Variables on the right keep their values: x = x + 5; with x = 5 makes x 10.

### L3: Relational / relations x function (concrete operational begins)

L3 for assignment: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

- **Edge:** `assignment` &rarr; `assignment@L3` (has_level)
- **Exact edge logic:** assignment -&gt; L3 (Relational): the answer relates the parts (10 ways).

Ways (10), each with its exact rule:

- **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): The left side must be a declared variable whose type accepts the value. Assignment is how that variable's value changes.
- **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): A declaration can include the first assignment (int x = 5;). Assigning to a variable that was never declared does not compile.
- **[2] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Exchanging a[i] and a[j] takes three assignments in a fixed order through a temporary, because each assignment overwrites its target.
- **[3] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): int t = a; a = b; b = t; works only in this order, because every assignment destroys its left variable's old value.
- **[4] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): x op= e is shorthand for x = x op e. The left variable's current value is fetched first and then combined with e.
- **[5] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Because an assignment is an expression whose value is the value stored, and = groups right to left, a = b = 0 first stores 0 in b and then stores that 0 in a.
- **[6] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): As a statement, i++ has the same effect as the assignment i = i + 1.
- **[7] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): A trace records the value of each variable after each assignment runs, one row per statement.
- **[8] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): x = y stores the value of y in x (a statement with a side effect); x == y only tests whether the two values are equal and gives a boolean. Writing = where == is meant is a compile error with int operands and a silent bug with boolean operands.
- **[9] purpose\_of\_the\_whole** (rule type P, plan / role rule): Assignment gives a variable its value in each role: initialization, counter update (n = n + 1), gatherer update (sum = sum + x), most-wanted holder update (max = x), or temporary (t = a).

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for assignment: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

- **Edge:** `assignment` &rarr; `assignment@L4` (has_level)
- **Exact edge logic:** assignment -&gt; L4 (Extended abstract): the answer reasons beyond the given code (7 ways).

Ways (7), each with its exact rule:

- **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `VariablesHoldExpressions`: Swapping the two sides (a = b versus b = a) changes which variable changes. Reordering assignments changes the final values. An assignment cannot be undone, because the old value is lost unless it was first saved in a temporary.
- **[1] diagnose\_an\_error** (rule type D, error rule): rule broken: The left-hand side of = must be a single variable; only the right-hand side may be an arbitrary expression. Kind: compile-time. Trigger class: Any assignment whose left side is a literal or compound expression (7 = a; a + b = c;): 'unexpected type, required: variable'.
- **[2] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Use assignment whenever a variable's value must be set or updated. Use == to compare, final to forbid updates, and op= or ++ for x = x op e.
- **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: A local variable may be declared only once in its scope; later changes use an assignment without the type. Kind: compile-time. Trigger class: A second 'int x = ...' for a name already declared in the same or an enclosing block: 'variable x is already defined'.
- **[4] diagnose\_an\_error** (rule type D, error rule): rule broken: A final variable is assigned exactly once; it cannot be reassigned after initialization. Kind: compile-time. Trigger class: Any assignment, ++ or op= to a final variable after its initialization: 'cannot assign a value to final variable'.
- **[5] diagnose\_an\_error** (rule type D, error rule): rule broken: = assigns and == compares; a condition needs a boolean. Kind: compile-time. Trigger class: Writing if (a = b) with int a, b gives 'incompatible types: int cannot be converted to boolean'. With boolean variables it compiles and silently assigns.
- **[6] diagnose\_an\_error** (rule type D, error rule): rule broken: The assigned value's type must fit the variable's type. Kind: compile-time. Trigger class: Assigning a double to an int, an int to a String, and so on: 'incompatible types'.

## Same topic

`assignment` belongs to the topic **Data types and terminology (literals, identifiers, variables, declarations, assignment, expressions)** (`topic1.2.a`). The topic also contains: `chained_assignment`, `data_type`, `declaration`, `definite_assignment`, `expression`, `identifier`, `literal`, `named_constants`, `naming_convention`, `operator_precedence`, `primitive_type`, `program_trace`, `variable`, `variable_swap`.

## Rules of the concept (34)

- **Book** (SW-1e, p. 16 (pdf 26)): "An assignment statement associates a data-type value with a variable."
- **Book** (SW-1e, p. 16 (pdf 26)): "The left-hand side of an assignment statement must be a single variable; the right-hand side can be an arbitrary expression that produces values of the type."
- **Book** (OT-Op1, ): "it assigns the value on its right to the operand on its left"
- **Book** (SW-1.2, p. 15 (pdf 25)): "The next three lines are assignment statements that change the values of the variables."
- **E** (folk-meaning rule): In maths, = states a symmetric, lasting equality (a = b means b = a, and x = x + 5 is false). In Java, = is a one-time, directed action: evaluate the right side, then store the result in the variable on the left.
- **M** (wrong rule / right rule): AssignCompares: wrong: = compares two values instead of assigning \| right: x = y copies the value of y into x; x == y is what compares them.
- **M** (wrong rule / right rule): AssignmentNotExpression: wrong: an assignment cannot be used inside a larger expression \| right: An assignment is an expression whose value is the value assigned, so (x = v) both stores v in x and gives v.
- **M** (wrong rule / right rule): AssignmentOppositeDirection: wrong: a = b copies the value of a into b. \| right: Assignment stores the value of the right side into the variable on the left.
- **M** (wrong rule / right rule): SwapWithoutTemp: wrong: a[i] = a[j]; a[j] = a[i]; exchanges the two values. \| right: A temporary variable must save a[i] before it is overwritten.
- **M** (wrong rule / right rule): VariablesHoldExpressions: wrong: = stores the expression itself, not its computed value \| right: y = x + k; stores the value that x + k has at that moment, so later changes to x do not change y.
- **M** (wrong rule / right rule): AssignmentCopiesObject: wrong: assigning a reference copies the object \| right: b = a; copies only the reference, so a and b refer to the same array and b[i] = v also changes a[i].
- **M** (wrong rule / right rule): AssignmentAddsToTarget: wrong: a = b adds the value of b to the value already in a (the accumulator model). \| right: a = b replaces the old value of a with the value of b; the old value is lost.
- **M** (wrong rule / right rule): AssignmentIsEquation: wrong: An assignment states a lasting equality between its two sides, so y = x - y can be solved like the equation x = 2y and x = x + 5 relates two equal quantities. \| right: An assignment is a one-time action: evaluate the right side with current values, then store the result in the left variable.
- **M** (wrong rule / right rule): AssignmentExchangesValues: wrong: b = a exchanges the values of a and b. \| right: b = a copies a into b and leaves a unchanged; an exchange needs a temporary variable and three assignments.
- **M** (wrong rule / right rule): AssignmentEmptiesSource: wrong: After b = a, a no longer holds a value, as if the value had been moved. \| right: Assignment copies; the variable on the right keeps its value.
- **M** (wrong rule / right rule): VariableKeepsOldValue: wrong: A variable keeps its first value after a new assignment (the static model). \| right: Each assignment or read replaces the variable's current value.
- **T** (uneven-application rule): Points to LT (evaluate the right side with current values, then overwrite the left variable). Applied unevenly, a student traces one segment correctly but reads the next as simultaneous equations or as a swap, giving 15 and 15 for one segment and 5 and 10 for the other.
- **N** (identity rule): Assignment statement: the statement variable = expression; which stores a data-type value in a variable.
- **S** (declarative rule): The left-hand side must be a single variable. The right-hand side can be any expression whose type is compatible with the variable's type. = is not mathematical equality (a + b = b + a and 1 = a are illegal).
- **LT** (operational sequencing rule): First the right-hand side is fully evaluated using the variables' current values (left to right). Then that value is stored in the left-hand variable, replacing its old value, and execution moves to the next statement.
- **OP** (evaluation / result rule): As a statement it prints nothing; its result is the new value of the left variable (after c = a + b; with a = 1234 and b = 99, c is 1333). Used as an expression, its value is the value assigned.
- **OS** (state-transition rule): Exactly one variable, the left one, changes, and its old value is lost. Variables on the right keep their values: x = x + 5; with x = 5 makes x 10.
- **R** (composition rule (with a neighbour)): with variable: The left side must be a declared variable whose type accepts the value. Assignment is how that variable's value changes.
- **R** (composition rule (with a neighbour)): with declaration: A declaration can include the first assignment (int x = 5;). Assigning to a variable that was never declared does not compile.
- **R** (composition rule (with a neighbour)): with array\_exchange: Exchanging a[i] and a[j] takes three assignments in a fixed order through a temporary, because each assignment overwrites its target.
- **R** (composition rule (with a neighbour)): with variable\_swap: int t = a; a = b; b = t; works only in this order, because every assignment destroys its left variable's old value.
- **R** (composition rule (with a neighbour)): with compound\_assignment: x op= e is shorthand for x = x op e. The left variable's current value is fetched first and then combined with e.
- **R** (composition rule (with a neighbour)): with chained\_assignment: Because an assignment is an expression whose value is the value stored, and = groups right to left, a = b = 0 first stores 0 in b and then stores that 0 in a.
- **R** (composition rule (with a neighbour)): with increment\_operators: As a statement, i++ has the same effect as the assignment i = i + 1.
- **R** (composition rule (with a neighbour)): with program\_trace: A trace records the value of each variable after each assignment runs, one row per statement.
- **P** (plan / role rule): Assignment gives a variable its value in each role: initialization, counter update (n = n + 1), gatherer update (sum = sum + x), most-wanted holder update (max = x), or temporary (t = a).
- **C** (conservation rule): Swapping the two sides (a = b versus b = a) changes which variable changes. Reordering assignments changes the final values. An assignment cannot be undone, because the old value is lost unless it was first saved in a temporary.
- **D** (error rule): rule broken: A local variable may be declared only once in its scope; later changes use an assignment without the type. (compile-time)
- **D** (error rule): rule broken: The left-hand side of = must be a single variable; only the right-hand side may be an arbitrary expression. (compile-time)
- **D** (error rule): rule broken: A final variable is assigned exactly once; it cannot be reassigned after initialization. (compile-time)
- **D** (error rule): rule broken: = assigns and == compares; a condition needs a boolean. (compile-time)
- **D** (error rule): rule broken: The assigned value's type must fit the variable's type. (compile-time)
- **X** (applicability rule): Use assignment whenever a variable's value must be set or updated. Use == to compare, final to forbid updates, and op= or ++ for x = x op e.

## How it is found in code and answers (reader block)

- **Aliases:** assigned, assign, assigns, assignment, set to, is set, stored in, store, stores
- **Code patterns:** `(?<![=!<>+\-*/%&|^])=(?!=)`
- **Operator symbols:** none
- **Java types:** none

## The whole prerequisite chain

- **Everything it builds on (6):** `data_type`, `declaration`, `identifier`, `literal`, `primitive_type`, `variable`
- **Everything that builds on it (18):** `accumulator_pattern`, `array_exchange`, `array_reversal`, `chained_assignment`, `compound_assignment`, `counter_pattern`, `debugging`, `frequency_counting`, `increment_operators`, `monte_carlo_simulation`, `program_trace`, `sampling_without_replacement`, `sentinel_loop`, `shuffle`, `side_effect_order`, `testing`, `two_models`, `variable_swap`

## Every edge in this view and its exact edge logic (64)

All the edges drawn in the picture, in the order: prerequisite, parallel, misconception, error, has_level, contains.

**1. `assignment` &rarr; `array_exchange`** (prerequisite)

- **Exact edge logic:** The exchange is three assignments in a fixed order through a temporary variable.
- **Grounding:** book\_passage
- **Composition rule (R) of `assignment` with `array_exchange`:** Exchanging a[i] and a[j] takes three assignments in a fixed order through a temporary, because each assignment overwrites its target.
- **Composition rule (R) of `array_exchange` with `assignment`:** Each of the three steps is an ordinary assignment whose left side is a single variable (here an array element), executed in order.

**2. `assignment` &rarr; `chained_assignment`** (prerequisite)

- **Exact edge logic:** An assignment such as x = y is treated as an expression: it assigns the value of y to x and evaluates to that value.
- **Grounding:** questionable
- **Composition rule (R) of `assignment` with `chained_assignment`:** Because an assignment is an expression whose value is the value stored, and = groups right to left, a = b = 0 first stores 0 in b and then stores that 0 in a.
- **Composition rule (R) of `chained_assignment` with `assignment`:** A chain works only because an assignment is itself an expression whose value is the value stored, so it can be the right side of another =.

**3. `assignment` &rarr; `compound_assignment`** (prerequisite)

- **Exact edge logic:** x op= e is shorthand for the assignment x = x op e.
- **Grounding:** book\_passage
- **Composition rule (R) of `assignment` with `compound_assignment`:** x op= e is shorthand for x = x op e. The left variable's current value is fetched first and then combined with e.
- **Composition rule (R) of `compound_assignment` with `assignment`:** x op= e is shorthand for the assignment x = x op e, so the new value depends on the old one (x is read, then written).

**4. `assignment` &rarr; `increment_operators`** (prerequisite)

- **Exact edge logic:** i++ is shorthand for the assignment i = i + 1.
- **Grounding:** book\_passage
- **Composition rule (R) of `assignment` with `increment_operators`:** As a statement, i++ has the same effect as the assignment i = i + 1.
- **Composition rule (R) of `increment_operators` with `assignment`:** i++ is shorthand for the assignment i = i + 1 (and i += k for i = i + k), so it changes the variable's stored value.

**5. `assignment` &rarr; `program_trace`** (prerequisite)

- **Exact edge logic:** A trace records the value each variable holds after each assignment statement runs.
- **Grounding:** book\_passage
- **Composition rule (R) of `assignment` with `program_trace`:** A trace records the value of each variable after each assignment runs, one row per statement.
- **Composition rule (R) of `program_trace` with `assignment`:** Each assignment statement produces the next row of the trace, changing exactly the column of the variable on its left-hand side.

**6. `assignment` &rarr; `variable_swap`** (prerequisite)

- **Exact edge logic:** The three assignments int t = a; a = b; b = t; exchange the values of a and b, as a trace of the variable values after each statement shows.
- **Grounding:** book\_passage
- **Composition rule (R) of `assignment` with `variable_swap`:** int t = a; a = b; b = t; works only in this order, because every assignment destroys its left variable's old value.
- **Composition rule (R) of `variable_swap` with `assignment`:** A swap is three assignments whose order matters, because each one overwrites the old value of its left variable.

**7. `declaration` &rarr; `assignment`** (prerequisite)

- **Exact edge logic:** A variable must be declared before an assignment can store a value into it.
- **Grounding:** book\_passage
- **Composition rule (R) of `declaration` with `assignment`:** An assignment can store into a variable only after the variable's declaration, and only a value of a compatible type.
- **Composition rule (R) of `assignment` with `declaration`:** A declaration can include the first assignment (int x = 5;). Assigning to a variable that was never declared does not compile.

**8. `variable` &rarr; `assignment`** (prerequisite)

- **Exact edge logic:** Assignment needs a declared variable on its left side to store the computed value into.
- **Grounding:** book\_passage
- **Composition rule (R) of `variable` with `assignment`:** Assignment is the only statement that changes a variable, and its left-hand side must be a single variable.
- **Composition rule (R) of `assignment` with `variable`:** The left side must be a declared variable whose type accepts the value. Assignment is how that variable's value changes.

**9. `assignment` &harr; `comparison_operators`** (parallel)

- **Exact edge logic:** x = y stores the value of y in x (a statement with a side effect); x == y only tests whether the two values are equal and gives a boolean. Writing = where == is meant is a compile error with int operands and a silent bug with boolean operands.
- **Grounding:** book\_passage

**10. `assignment` &rarr; `AssignCompares`** (misconception)

- **Exact edge logic (the wrong rule):** x = y checks whether x and y are equal.
- **Twin logic (the right rule):** x = y copies the value of y into x; x == y is what compares them.
- **Role:** primary

**11. `assignment` &rarr; `AssignmentAddsToTarget`** (misconception)

- **Exact edge logic (the wrong rule):** a = b adds the value of b to the value already in a (the accumulator model).
- **Twin logic (the right rule):** a = b replaces the old value of a with the value of b; the old value is lost.
- **Role:** primary

**12. `assignment` &rarr; `AssignmentCopiesObject`** (misconception)

- **Exact edge logic (the wrong rule):** b = a; for an array makes b a separate copy, so changing b[i] leaves a[i] unchanged.
- **Twin logic (the right rule):** b = a; copies only the reference, so a and b refer to the same array and b[i] = v also changes a[i].
- **Role:** context

**13. `assignment` &rarr; `AssignmentEmptiesSource`** (misconception)

- **Exact edge logic (the wrong rule):** After b = a, a no longer holds a value, as if the value had been moved.
- **Twin logic (the right rule):** Assignment copies; the variable on the right keeps its value.
- **Role:** primary

**14. `assignment` &rarr; `AssignmentExchangesValues`** (misconception)

- **Exact edge logic (the wrong rule):** b = a exchanges the values of a and b.
- **Twin logic (the right rule):** b = a copies a into b and leaves a unchanged; an exchange needs a temporary variable and three assignments.
- **Role:** primary

**15. `assignment` &rarr; `AssignmentIsEquation`** (misconception)

- **Exact edge logic (the wrong rule):** An assignment states a lasting equality between its two sides, so y = x - y can be solved like the equation x = 2y and x = x + 5 relates two equal quantities.
- **Twin logic (the right rule):** An assignment is a one-time action: evaluate the right side with current values, then store the result in the left variable.
- **Role:** primary

**16. `assignment` &rarr; `AssignmentNotExpression`** (misconception)

- **Exact edge logic (the wrong rule):** An assignment cannot be used inside a larger expression, so a condition like (x = read()) != v is not allowed.
- **Twin logic (the right rule):** An assignment is an expression whose value is the value assigned, so (x = v) both stores v in x and gives v.
- **Role:** primary

**17. `assignment` &rarr; `AssignmentOppositeDirection`** (misconception)

- **Exact edge logic (the wrong rule):** a = b copies the value of a into b.
- **Twin logic (the right rule):** Assignment stores the value of the right side into the variable on the left.
- **Role:** primary

**18. `assignment` &rarr; `PrintedTextIsExecuted`** (misconception)

- **Exact edge logic (the wrong rule):** System.out.println("x is 5"); sets x to 5 (text inside the quotes is run as code).
- **Twin logic (the right rule):** Characters inside double quotes are printed literally; println only displays them and changes no variable. Only an assignment such as x = 5; sets x.
- **Role:** context

**19. `assignment` &rarr; `SwapWithoutTemp`** (misconception)

- **Exact edge logic (the wrong rule):** a[i] = a[j]; a[j] = a[i]; exchanges the two values.
- **Twin logic (the right rule):** A temporary variable must save a[i] before it is overwritten.
- **Role:** context

**20. `assignment` &rarr; `VariableKeepsOldValue`** (misconception)

- **Exact edge logic (the wrong rule):** A variable keeps its first value after a new assignment (the static model).
- **Twin logic (the right rule):** Each assignment or read replaces the variable's current value.
- **Role:** context

**21. `assignment` &rarr; `VariablesHoldExpressions`** (misconception)

- **Exact edge logic (the wrong rule):** y = x + k; makes y always equal to x + k, so when x changes later, y changes too.
- **Twin logic (the right rule):** y = x + k; stores the value that x + k has at that moment, so later changes to x do not change y.
- **Role:** primary

**22. `array_aliasing` &rarr; `AssignmentCopiesObject`** (misconception)

- **Exact edge logic (the wrong rule):** assigning a reference copies the object
- **Twin logic (the right rule):** b = a; copies only the reference, so a and b refer to the same array and b[i] = v also changes a[i].
- **Role:** primary

**23. `array_copy` &rarr; `AssignmentCopiesObject`** (misconception)

- **Exact edge logic (the wrong rule):** assigning a reference copies the object
- **Twin logic (the right rule):** b = a; copies only the reference, so a and b refer to the same array and b[i] = v also changes a[i].
- **Role:** context

**24. `array_exchange` &rarr; `SwapWithoutTemp`** (misconception)

- **Exact edge logic (the wrong rule):** a[i] = a[j]; a[j] = a[i]; exchanges the two values.
- **Twin logic (the right rule):** A temporary variable must save a[i] before it is overwritten.
- **Role:** primary

**25. `chained_assignment` &rarr; `AssignmentNotExpression`** (misconception)

- **Exact edge logic (the wrong rule):** an assignment cannot be used inside a larger expression
- **Twin logic (the right rule):** An assignment is an expression whose value is the value assigned, so (x = v) both stores v in x and gives v.
- **Role:** context

**26. `comparison_operators` &rarr; `AssignCompares`** (misconception)

- **Exact edge logic (the wrong rule):** = compares two values instead of assigning
- **Twin logic (the right rule):** x = y copies the value of y into x; x == y is what compares them.
- **Role:** context

**27. `expression` &rarr; `AssignmentIsEquation`** (misconception)

- **Exact edge logic (the wrong rule):** An assignment states a lasting equality between its two sides, so y = x - y can be solved like the equation x = 2y and x = x + 5 relates two equal quantities.
- **Twin logic (the right rule):** An assignment is a one-time action: evaluate the right side with current values, then store the result in the left variable.
- **Role:** context

**28. `expression` &rarr; `AssignmentNotExpression`** (misconception)

- **Exact edge logic (the wrong rule):** An assignment cannot be used inside a larger expression, so a condition like (x = read()) != v is not allowed.
- **Twin logic (the right rule):** An assignment is an expression whose value is the value assigned, so (x = v) both stores v in x and gives v.
- **Role:** context

**29. `expression` &rarr; `VariablesHoldExpressions`** (misconception)

- **Exact edge logic (the wrong rule):** = stores the expression itself, not its computed value
- **Twin logic (the right rule):** y = x + k; stores the value that x + k has at that moment, so later changes to x do not change y.
- **Role:** context

**30. `if_statement` &rarr; `AssignCompares`** (misconception)

- **Exact edge logic (the wrong rule):** = compares two values instead of assigning
- **Twin logic (the right rule):** x = y copies the value of y into x; x == y is what compares them.
- **Role:** context

**31. `println` &rarr; `PrintedTextIsExecuted`** (misconception)

- **Exact edge logic (the wrong rule):** System.out.println("x is 5"); sets x to 5 (text inside the quotes is run as code).
- **Twin logic (the right rule):** Characters inside double quotes are printed literally; println only displays them and changes no variable. Only an assignment such as x = 5; sets x.
- **Role:** primary

**32. `read_loop_idiom` &rarr; `AssignmentNotExpression`** (misconception)

- **Exact edge logic (the wrong rule):** A read and a test cannot be combined, so while ((x = read()) != end) is not allowed.
- **Twin logic (the right rule):** while ((x = read()) != end) reads a value into x and tests that same value in one expression.
- **Role:** context

**33. `string_literal` &rarr; `PrintedTextIsExecuted`** (misconception)

- **Exact edge logic (the wrong rule):** System.out.println("x is 5"); sets x to 5 (text inside the quotes is run as code).
- **Twin logic (the right rule):** Characters inside double quotes are printed literally; println only displays them and changes no variable. Only an assignment such as x = 5; sets x.
- **Role:** context

**34. `variable` &rarr; `VariableKeepsOldValue`** (misconception)

- **Exact edge logic (the wrong rule):** A variable keeps its first value after a new assignment (the static model).
- **Twin logic (the right rule):** Each assignment or read replaces the variable's current value.
- **Role:** primary

**35. `variable` &rarr; `VariablesHoldExpressions`** (misconception)

- **Exact edge logic (the wrong rule):** = stores the expression itself, not its computed value
- **Twin logic (the right rule):** y = x + k; stores the value that x + k has at that moment, so later changes to x do not change y.
- **Role:** context

**36. `variable_swap` &rarr; `AssignmentExchangesValues`** (misconception)

- **Exact edge logic (the wrong rule):** b = a exchanges the values of a and b.
- **Twin logic (the right rule):** b = a copies a into b and leaves a unchanged; an exchange needs a temporary variable and three assignments.
- **Role:** context

**37. `variable_swap` &rarr; `SwapWithoutTemp`** (misconception)

- **Exact edge logic (the wrong rule):** a[i] = a[j]; a[j] = a[i]; exchanges the two values.
- **Twin logic (the right rule):** A temporary variable must save a[i] before it is overwritten.
- **Role:** context

**38. `assignment` &rarr; `AssignToFinal`** (error)

- **Exact edge logic (the wrong rule):** Assigns a new value to a variable declared final.
- **Twin logic (the right rule):** A final variable cannot be reassigned after it is initialized; the compiler reports an error.
- **Role:** context

**39. `assignment` &rarr; `ExpressionOnLeftOfAssignment`** (error)

- **Exact edge logic (the wrong rule):** Writes a + b = c; or 7 = a; as if = were a math equation.
- **Twin logic (the right rule):** The left side of an assignment must be a single variable; only the right side can be an expression.
- **Role:** primary

**40. `assignment` &rarr; `RedeclareToReassign`** (error)

- **Exact edge logic (the wrong rule):** Writes int x = 5; ... int x = 10; to change x.
- **Twin logic (the right rule):** A declaration gives a variable its name and type; a later change of value is an assignment statement such as x = 10;, not a second declaration.
- **Role:** context

**41. `compile_time_error` &rarr; `AssignToFinal`** (error)

- **Exact edge logic (the wrong rule):** Assigns a new value to a variable declared final.
- **Twin logic (the right rule):** A final variable cannot be reassigned after it is initialized; the compiler reports an error.
- **Role:** context

**42. `declaration` &rarr; `RedeclareToReassign`** (error)

- **Exact edge logic (the wrong rule):** Writes int x = 5; ... int x = 10; to change x.
- **Twin logic (the right rule):** A declaration gives a variable its name and type; a later change of value is an assignment statement such as x = 10;, not a second declaration.
- **Role:** primary

**43. `expression` &rarr; `ExpressionOnLeftOfAssignment`** (error)

- **Exact edge logic (the wrong rule):** Writes a + b = c; or 7 = a; as if = were a math equation.
- **Twin logic (the right rule):** The left side of an assignment must be a single variable; only the right side can be an expression.
- **Role:** context

**44. `named_constants` &rarr; `AssignToFinal`** (error)

- **Exact edge logic (the wrong rule):** Assigns a new value to a variable declared final.
- **Twin logic (the right rule):** A final variable cannot be reassigned after it is initialized; the compiler reports an error.
- **Role:** primary

**45. `assignment` &rarr; `assignment@L0`** (has_level)

- **Exact edge logic:** assignment -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (13 ways).
  - **[0] everyday\_reading** (rule type E, folk-meaning rule): In maths, = states a symmetric, lasting equality (a = b means b = a, and x = x + 5 is false). In Java, = is a one-time, directed action: evaluate the right side, then store the result in the variable on the left.
  - **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `VariablesHoldExpressions`: wrong rule: = stores the expression itself, not its computed value. Right rule: y = x + k; stores the value that x + k has at that moment, so later changes to x do not change y.
  - **[2] misconception** (rule type M, wrong rule / right rule) &rarr; `AssignCompares`: wrong rule: = compares two values instead of assigning. Right rule: x = y copies the value of y into x; x == y is what compares them.
  - **[3] misconception** (rule type M, wrong rule / right rule) &rarr; `AssignmentNotExpression`: wrong rule: an assignment cannot be used inside a larger expression. Right rule: An assignment is an expression whose value is the value assigned, so (x = v) both stores v in x and gives v.
  - **[4] misconception** (rule type M, wrong rule / right rule) &rarr; `AssignmentOppositeDirection`: wrong rule: a = b copies the value of a into b. Right rule: Assignment stores the value of the right side into the variable on the left.
  - **[5] misconception** (rule type M, wrong rule / right rule) &rarr; `AssignmentAddsToTarget`: wrong rule: a = b adds the value of b to the value already in a (the accumulator model). Right rule: a = b replaces the old value of a with the value of b; the old value is lost.
  - **[6] misconception** (rule type M, wrong rule / right rule) &rarr; `AssignmentIsEquation`: wrong rule: An assignment states a lasting equality between its two sides, so y = x - y can be solved like the equation x = 2y and x = x + 5 relates two equal quantities. Right rule: An assignment is a one-time action: evaluate the right side with current values, then store the result in the left variable.
  - **[7] misconception** (rule type M, wrong rule / right rule) &rarr; `AssignmentExchangesValues`: wrong rule: b = a exchanges the values of a and b. Right rule: b = a copies a into b and leaves a unchanged; an exchange needs a temporary variable and three assignments.
  - **[8] misconception** (rule type M, wrong rule / right rule) &rarr; `AssignmentEmptiesSource`: wrong rule: After b = a, a no longer holds a value, as if the value had been moved. Right rule: Assignment copies; the variable on the right keeps its value.
  - **[9] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `VariablesHoldExpressions`: Points to LT (evaluate the right side with current values, then overwrite the left variable). Applied unevenly, a student traces one segment correctly but reads the next as simultaneous equations or as a swap, giving 15 and 15 for one segment and 5 and 10 for the other. (here mixing in: "= stores the expression itself, not its computed value")
  - **[10] misconception** (rule type M, wrong rule / right rule) &rarr; `SwapWithoutTemp`: wrong rule: a[i] = a[j]; a[j] = a[i]; exchanges the two values. Right rule: A temporary variable must save a[i] before it is overwritten.
  - **[11] misconception** (rule type M, wrong rule / right rule) &rarr; `AssignmentCopiesObject`: wrong rule: assigning a reference copies the object. Right rule: b = a; copies only the reference, so a and b refer to the same array and b[i] = v also changes a[i].
  - **[12] misconception** (rule type M, wrong rule / right rule) &rarr; `VariableKeepsOldValue`: wrong rule: A variable keeps its first value after a new assignment (the static model). Right rule: Each assignment or read replaces the variable's current value.

**46. `assignment` &rarr; `assignment@L1`** (has_level)

- **Exact edge logic:** assignment -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).
  - **[0] names\_the\_element** (rule type N, identity rule): Assignment statement: the statement variable = expression; which stores a data-type value in a variable.
  - **[1] states\_the\_rule** (rule type S, declarative rule): The left-hand side must be a single variable. The right-hand side can be any expression whose type is compatible with the variable's type. = is not mathematical equality (a + b = b + a and 1 = a are illegal).

**47. `assignment` &rarr; `assignment@L2`** (has_level)

- **Exact edge logic:** assignment -&gt; L2 (Multistructural): the answer applies the rules of assignment to every part of the code, in order (3 ways).
  - **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): First the right-hand side is fully evaluated using the variables' current values (left to right). Then that value is stored in the left-hand variable, replacing its old value, and execution moves to the next statement.
  - **[1] output\_prediction** (rule type OP, evaluation / result rule): As a statement it prints nothing; its result is the new value of the left variable (after c = a + b; with a = 1234 and b = 99, c is 1333). Used as an expression, its value is the value assigned.
  - **[2] one\_step\_execution** (rule type OS, state-transition rule): Exactly one variable, the left one, changes, and its old value is lost. Variables on the right keep their values: x = x + 5; with x = 5 makes x 10.

**48. `assignment` &rarr; `assignment@L3`** (has_level)

- **Exact edge logic:** assignment -&gt; L3 (Relational): the answer relates the parts (10 ways).
  - **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): The left side must be a declared variable whose type accepts the value. Assignment is how that variable's value changes.
  - **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): A declaration can include the first assignment (int x = 5;). Assigning to a variable that was never declared does not compile.
  - **[2] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Exchanging a[i] and a[j] takes three assignments in a fixed order through a temporary, because each assignment overwrites its target.
  - **[3] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): int t = a; a = b; b = t; works only in this order, because every assignment destroys its left variable's old value.
  - **[4] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): x op= e is shorthand for x = x op e. The left variable's current value is fetched first and then combined with e.
  - **[5] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Because an assignment is an expression whose value is the value stored, and = groups right to left, a = b = 0 first stores 0 in b and then stores that 0 in a.
  - **[6] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): As a statement, i++ has the same effect as the assignment i = i + 1.
  - **[7] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): A trace records the value of each variable after each assignment runs, one row per statement.
  - **[8] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): x = y stores the value of y in x (a statement with a side effect); x == y only tests whether the two values are equal and gives a boolean. Writing = where == is meant is a compile error with int operands and a silent bug with boolean operands.
  - **[9] purpose\_of\_the\_whole** (rule type P, plan / role rule): Assignment gives a variable its value in each role: initialization, counter update (n = n + 1), gatherer update (sum = sum + x), most-wanted holder update (max = x), or temporary (t = a).

**49. `assignment` &rarr; `assignment@L4`** (has_level)

- **Exact edge logic:** assignment -&gt; L4 (Extended abstract): the answer reasons beyond the given code (7 ways).
  - **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `VariablesHoldExpressions`: Swapping the two sides (a = b versus b = a) changes which variable changes. Reordering assignments changes the final values. An assignment cannot be undone, because the old value is lost unless it was first saved in a temporary.
  - **[1] diagnose\_an\_error** (rule type D, error rule): rule broken: The left-hand side of = must be a single variable; only the right-hand side may be an arbitrary expression. Kind: compile-time. Trigger class: Any assignment whose left side is a literal or compound expression (7 = a; a + b = c;): 'unexpected type, required: variable'.
  - **[2] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Use assignment whenever a variable's value must be set or updated. Use == to compare, final to forbid updates, and op= or ++ for x = x op e.
  - **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: A local variable may be declared only once in its scope; later changes use an assignment without the type. Kind: compile-time. Trigger class: A second 'int x = ...' for a name already declared in the same or an enclosing block: 'variable x is already defined'.
  - **[4] diagnose\_an\_error** (rule type D, error rule): rule broken: A final variable is assigned exactly once; it cannot be reassigned after initialization. Kind: compile-time. Trigger class: Any assignment, ++ or op= to a final variable after its initialization: 'cannot assign a value to final variable'.
  - **[5] diagnose\_an\_error** (rule type D, error rule): rule broken: = assigns and == compares; a condition needs a boolean. Kind: compile-time. Trigger class: Writing if (a = b) with int a, b gives 'incompatible types: int cannot be converted to boolean'. With boolean variables it compiles and silently assigns.
  - **[6] diagnose\_an\_error** (rule type D, error rule): rule broken: The assigned value's type must fit the variable's type. Kind: compile-time. Trigger class: Assigning a double to an int, an int to a String, and so on: 'incompatible types'.

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

**63. `topic1.2.a` &rarr; `variable`** (contains)

- topic `topic1.2.a` contains `variable`

**64. `topic1.2.a` &rarr; `variable_swap`** (contains)

- topic `topic1.2.a` contains `variable_swap`
