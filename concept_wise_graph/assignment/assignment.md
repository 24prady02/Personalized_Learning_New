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

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 64 edges around this concept, each explained in the graph's own words.

## What it needs first (2)

A prerequisite edge means the other concept has to be understood before `assignment`.

### `declaration` comes before `assignment`

*int x; -- introduces a variable name and its type*

A variable must be declared before an assignment can store a value into it.

- **Grounding:** book passage
- **How `assignment` combines with `declaration`:** A declaration can include the first assignment (int x = 5;). Assigning to a variable that was never declared does not compile.
- **How `declaration` combines with `assignment`:** An assignment can store into a variable only after the variable's declaration, and only a value of a compatible type.

### `variable` comes before `assignment`

*a named, typed box that holds a value*

Assignment needs a declared variable on its left side to store the computed value into.

- **Grounding:** book passage
- **How `assignment` combines with `variable`:** The left side must be a declared variable whose type accepts the value. Assignment is how that variable's value changes.
- **How `variable` combines with `assignment`:** Assignment is the only statement that changes a variable, and its left-hand side must be a single variable.

## What it leads to (6)

These concepts need `assignment` first.

### `assignment` comes before `array_exchange`

*swap a[i] and a[j] through a temporary variable*

The exchange is three assignments in a fixed order through a temporary variable.

- **Grounding:** book passage
- **How `assignment` combines with `array_exchange`:** Exchanging a[i] and a[j] takes three assignments in a fixed order through a temporary, because each assignment overwrites its target.
- **How `array_exchange` combines with `assignment`:** Each of the three steps is an ordinary assignment whose left side is a single variable (here an array element), executed in order.

### `assignment` comes before `chained_assignment`

*a = b = 0 assigns right to left*

An assignment such as x = y is treated as an expression: it assigns the value of y to x and evaluates to that value.

- **Grounding:** questionable
- **How `assignment` combines with `chained_assignment`:** Because an assignment is an expression whose value is the value stored, and = groups right to left, a = b = 0 first stores 0 in b and then stores that 0 in a.
- **How `chained_assignment` combines with `assignment`:** A chain works only because an assignment is itself an expression whose value is the value stored, so it can be the right side of another =.

### `assignment` comes before `compound_assignment`

*x += e, x -= e, ... include a hidden cast*

x op= e is shorthand for the assignment x = x op e.

- **Grounding:** book passage
- **How `assignment` combines with `compound_assignment`:** x op= e is shorthand for x = x op e. The left variable's current value is fetched first and then combined with e.
- **How `compound_assignment` combines with `assignment`:** x op= e is shorthand for the assignment x = x op e, so the new value depends on the old one (x is read, then written).

### `assignment` comes before `increment_operators`

*++ / -- (and +=)*

i++ is shorthand for the assignment i = i + 1.

- **Grounding:** book passage
- **How `assignment` combines with `increment_operators`:** As a statement, i++ has the same effect as the assignment i = i + 1.
- **How `increment_operators` combines with `assignment`:** i++ is shorthand for the assignment i = i + 1 (and i += k for i = i + k), so it changes the variable's stored value.

### `assignment` comes before `program_trace`

*Trace (table of variable values): a table of the values of the variables after each statement, used to check what code does*

A trace records the value each variable holds after each assignment statement runs.

- **Grounding:** book passage
- **How `assignment` combines with `program_trace`:** A trace records the value of each variable after each assignment runs, one row per statement.
- **How `program_trace` combines with `assignment`:** Each assignment statement produces the next row of the trace, changing exactly the column of the variable on its left-hand side.

### `assignment` comes before `variable_swap`

*exchanging two variables needs a temporary*

The three assignments int t = a; a = b; b = t; exchange the values of a and b, as a trace of the variable values after each statement shows.

- **Grounding:** book passage
- **How `assignment` combines with `variable_swap`:** int t = a; a = b; b = t; works only in this order, because every assignment destroys its left variable's old value.
- **How `variable_swap` combines with `assignment`:** A swap is three assignments whose order matters, because each one overwrites the old value of its left variable.

## Learned alongside (1)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

### `assignment` alongside `comparison_operators`

*== != &lt; &gt; &lt;= &gt;=*

x = y stores the value of y in x (a statement with a side effect); x == y only tests whether the two values are equal and gives a boolean. Writing = where == is meant is a compile error with int operands and a silent bug with boolean operands.

- **Grounding:** book passage

## Misconceptions (12)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### AssignCompares

- **Wrong rule:** x = y checks whether x and y are equal.
- **Right rule:** x = y copies the value of y into x; x == y is what compares them.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: = compares two values instead of assigning. Right rule: x = y copies the value of y into x; x == y is what compares them.
- **Also an edge from `comparison_operators`:** = compares two values instead of assigning
- **Also an edge from `if_statement`:** = compares two values instead of assigning

### AssignmentAddsToTarget

- **Wrong rule:** a = b adds the value of b to the value already in a (the accumulator model).
- **Right rule:** a = b replaces the old value of a with the value of b; the old value is lost.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: a = b adds the value of b to the value already in a (the accumulator model). Right rule: a = b replaces the old value of a with the value of b; the old value is lost.

### AssignmentCopiesObject

- **Wrong rule:** b = a; for an array makes b a separate copy, so changing b[i] leaves a[i] unchanged.
- **Right rule:** b = a; copies only the reference, so a and b refer to the same array and b[i] = v also changes a[i].
- **Role of this concept:** context
- **Shows at level L0 as:** misconception: wrong rule: assigning a reference copies the object. Right rule: b = a; copies only the reference, so a and b refer to the same array and b[i] = v also changes a[i].
- **Also an edge from `array_aliasing`:** assigning a reference copies the object
- **Also an edge from `array_copy`:** assigning a reference copies the object

### AssignmentEmptiesSource

- **Wrong rule:** After b = a, a no longer holds a value, as if the value had been moved.
- **Right rule:** Assignment copies; the variable on the right keeps its value.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: After b = a, a no longer holds a value, as if the value had been moved. Right rule: Assignment copies; the variable on the right keeps its value.

### AssignmentExchangesValues

- **Wrong rule:** b = a exchanges the values of a and b.
- **Right rule:** b = a copies a into b and leaves a unchanged; an exchange needs a temporary variable and three assignments.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: b = a exchanges the values of a and b. Right rule: b = a copies a into b and leaves a unchanged; an exchange needs a temporary variable and three assignments.
- **Also an edge from `variable_swap`:** b = a exchanges the values of a and b.

### AssignmentIsEquation

- **Wrong rule:** An assignment states a lasting equality between its two sides, so y = x - y can be solved like the equation x = 2y and x = x + 5 relates two equal quantities.
- **Right rule:** An assignment is a one-time action: evaluate the right side with current values, then store the result in the left variable.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: An assignment states a lasting equality between its two sides, so y = x - y can be solved like the equation x = 2y and x = x + 5 relates two equal quantities. Right rule: An assignment is a one-time action: evaluate the right side with current values, then store the result in the left variable.
- **Also an edge from `expression`:** An assignment states a lasting equality between its two sides, so y = x - y can be solved like the equation x = 2y and x = x + 5 relates two equal quantities.

### AssignmentNotExpression

- **Wrong rule:** An assignment cannot be used inside a larger expression, so a condition like (x = read()) != v is not allowed.
- **Right rule:** An assignment is an expression whose value is the value assigned, so (x = v) both stores v in x and gives v.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: an assignment cannot be used inside a larger expression. Right rule: An assignment is an expression whose value is the value assigned, so (x = v) both stores v in x and gives v.
- **Also an edge from `chained_assignment`:** an assignment cannot be used inside a larger expression
- **Also an edge from `expression`:** An assignment cannot be used inside a larger expression, so a condition like (x = read()) != v is not allowed.
- **Also an edge from `read_loop_idiom`:** A read and a test cannot be combined, so while ((x = read()) != end) is not allowed.

### AssignmentOppositeDirection

- **Wrong rule:** a = b copies the value of a into b.
- **Right rule:** Assignment stores the value of the right side into the variable on the left.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: a = b copies the value of a into b. Right rule: Assignment stores the value of the right side into the variable on the left.

### PrintedTextIsExecuted

- **Wrong rule:** System.out.println("x is 5"); sets x to 5 (text inside the quotes is run as code).
- **Right rule:** Characters inside double quotes are printed literally; println only displays them and changes no variable. Only an assignment such as x = 5; sets x.
- **Role of this concept:** context
- **Also an edge from `println`:** System.out.println("x is 5"); sets x to 5 (text inside the quotes is run as code).
- **Also an edge from `string_literal`:** System.out.println("x is 5"); sets x to 5 (text inside the quotes is run as code).

### SwapWithoutTemp

- **Wrong rule:** a[i] = a[j]; a[j] = a[i]; exchanges the two values.
- **Right rule:** A temporary variable must save a[i] before it is overwritten.
- **Role of this concept:** context
- **Shows at level L0 as:** misconception: wrong rule: a[i] = a[j]; a[j] = a[i]; exchanges the two values. Right rule: A temporary variable must save a[i] before it is overwritten.
- **Also an edge from `array_exchange`:** a[i] = a[j]; a[j] = a[i]; exchanges the two values.
- **Also an edge from `variable_swap`:** a[i] = a[j]; a[j] = a[i]; exchanges the two values.

### VariableKeepsOldValue

- **Wrong rule:** A variable keeps its first value after a new assignment (the static model).
- **Right rule:** Each assignment or read replaces the variable's current value.
- **Role of this concept:** context
- **Shows at level L0 as:** misconception: wrong rule: A variable keeps its first value after a new assignment (the static model). Right rule: Each assignment or read replaces the variable's current value.
- **Also an edge from `variable`:** A variable keeps its first value after a new assignment (the static model).

### VariablesHoldExpressions

- **Wrong rule:** y = x + k; makes y always equal to x + k, so when x changes later, y changes too.
- **Right rule:** y = x + k; stores the value that x + k has at that moment, so later changes to x do not change y.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: = stores the expression itself, not its computed value. Right rule: y = x + k; stores the value that x + k has at that moment, so later changes to x do not change y.
- **Shows at level L0 as:** inconsistent trace: Points to LT (evaluate the right side with current values, then overwrite the left variable). Applied unevenly, a student traces one segment correctly but reads the next as simultaneous equations or as a swap, giving 15 and 15 for one segment and 5 and 10 for the other. (here mixing in: "= stores the expression itself, not its computed value")
- **Also an edge from `expression`:** = stores the expression itself, not its computed value
- **Also an edge from `variable`:** = stores the expression itself, not its computed value

## Errors (3)

An error edge states the rule that gets broken in a program, and the right rule.

### AssignToFinal

- **Wrong rule:** Assigns a new value to a variable declared final.
- **Right rule:** A final variable cannot be reassigned after it is initialized; the compiler reports an error.
- **Role of this concept:** context
- **Also an edge from `compile_time_error`:** Assigns a new value to a variable declared final.
- **Also an edge from `named_constants`:** Assigns a new value to a variable declared final.

### ExpressionOnLeftOfAssignment

- **Wrong rule:** Writes a + b = c; or 7 = a; as if = were a math equation.
- **Right rule:** The left side of an assignment must be a single variable; only the right side can be an expression.
- **Role of this concept:** primary
- **Also an edge from `expression`:** Writes a + b = c; or 7 = a; as if = were a math equation.

### RedeclareToReassign

- **Wrong rule:** Writes int x = 5; ... int x = 10; to change x.
- **Right rule:** A declaration gives a variable its name and type; a later change of value is an assignment statement such as x = 10;, not a second declaration.
- **Role of this concept:** context
- **Also an edge from `declaration`:** Writes int x = 5; ... int x = 10; to change x.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for assignment: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to assignment agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

assignment -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (13 ways).

- **everyday reading** (folk-meaning rule): In maths, = states a symmetric, lasting equality (a = b means b = a, and x = x + 5 is false). In Java, = is a one-time, directed action: evaluate the right side, then store the result in the variable on the left.
- **misconception** (wrong rule / right rule; shows `VariablesHoldExpressions`): wrong rule: = stores the expression itself, not its computed value. Right rule: y = x + k; stores the value that x + k has at that moment, so later changes to x do not change y.
- **misconception** (wrong rule / right rule; shows `AssignCompares`): wrong rule: = compares two values instead of assigning. Right rule: x = y copies the value of y into x; x == y is what compares them.
- **misconception** (wrong rule / right rule; shows `AssignmentNotExpression`): wrong rule: an assignment cannot be used inside a larger expression. Right rule: An assignment is an expression whose value is the value assigned, so (x = v) both stores v in x and gives v.
- **misconception** (wrong rule / right rule; shows `AssignmentOppositeDirection`): wrong rule: a = b copies the value of a into b. Right rule: Assignment stores the value of the right side into the variable on the left.
- **misconception** (wrong rule / right rule; shows `AssignmentAddsToTarget`): wrong rule: a = b adds the value of b to the value already in a (the accumulator model). Right rule: a = b replaces the old value of a with the value of b; the old value is lost.
- **misconception** (wrong rule / right rule; shows `AssignmentIsEquation`): wrong rule: An assignment states a lasting equality between its two sides, so y = x - y can be solved like the equation x = 2y and x = x + 5 relates two equal quantities. Right rule: An assignment is a one-time action: evaluate the right side with current values, then store the result in the left variable.
- **misconception** (wrong rule / right rule; shows `AssignmentExchangesValues`): wrong rule: b = a exchanges the values of a and b. Right rule: b = a copies a into b and leaves a unchanged; an exchange needs a temporary variable and three assignments.
- **misconception** (wrong rule / right rule; shows `AssignmentEmptiesSource`): wrong rule: After b = a, a no longer holds a value, as if the value had been moved. Right rule: Assignment copies; the variable on the right keeps its value.
- **inconsistent trace** (uneven-application rule; shows `VariablesHoldExpressions`): Points to LT (evaluate the right side with current values, then overwrite the left variable). Applied unevenly, a student traces one segment correctly but reads the next as simultaneous equations or as a swap, giving 15 and 15 for one segment and 5 and 10 for the other. (here mixing in: "= stores the expression itself, not its computed value")
- **misconception** (wrong rule / right rule; shows `SwapWithoutTemp`): wrong rule: a[i] = a[j]; a[j] = a[i]; exchanges the two values. Right rule: A temporary variable must save a[i] before it is overwritten.
- **misconception** (wrong rule / right rule; shows `AssignmentCopiesObject`): wrong rule: assigning a reference copies the object. Right rule: b = a; copies only the reference, so a and b refer to the same array and b[i] = v also changes a[i].
- **misconception** (wrong rule / right rule; shows `VariableKeepsOldValue`): wrong rule: A variable keeps its first value after a new assignment (the static model). Right rule: Each assignment or read replaces the variable's current value.

### L1: Unistructural / atom x text surface

L1 for assignment: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

assignment -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

- **names the element** (identity rule): Assignment statement: the statement variable = expression; which stores a data-type value in a variable.
- **states the rule** (declarative rule): The left-hand side must be a single variable. The right-hand side can be any expression whose type is compatible with the variable's type. = is not mathematical equality (a + b = b + a and 1 = a are illegal).

### L2: Multistructural / block x execution / preoperational

L2 for assignment: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

assignment -&gt; L2 (Multistructural): the answer applies the rules of assignment to every part of the code, in order (3 ways).

- **line by line trace** (operational sequencing rule): First the right-hand side is fully evaluated using the variables' current values (left to right). Then that value is stored in the left-hand variable, replacing its old value, and execution moves to the next statement.
- **output prediction** (evaluation / result rule): As a statement it prints nothing; its result is the new value of the left variable (after c = a + b; with a = 1234 and b = 99, c is 1333). Used as an expression, its value is the value assigned.
- **one step execution** (state-transition rule): Exactly one variable, the left one, changes, and its old value is lost. Variables on the right keep their values: x = x + 5; with x = 5 makes x 10.

### L3: Relational / relations x function (concrete operational begins)

L3 for assignment: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

assignment -&gt; L3 (Relational): the answer relates the parts (10 ways).

- **relation to neighbour** (composition rule (with a neighbour)): The left side must be a declared variable whose type accepts the value. Assignment is how that variable's value changes.
- **relation to neighbour** (composition rule (with a neighbour)): A declaration can include the first assignment (int x = 5;). Assigning to a variable that was never declared does not compile.
- **relation to neighbour** (composition rule (with a neighbour)): Exchanging a[i] and a[j] takes three assignments in a fixed order through a temporary, because each assignment overwrites its target.
- **relation to neighbour** (composition rule (with a neighbour)): int t = a; a = b; b = t; works only in this order, because every assignment destroys its left variable's old value.
- **relation to neighbour** (composition rule (with a neighbour)): x op= e is shorthand for x = x op e. The left variable's current value is fetched first and then combined with e.
- **relation to neighbour** (composition rule (with a neighbour)): Because an assignment is an expression whose value is the value stored, and = groups right to left, a = b = 0 first stores 0 in b and then stores that 0 in a.
- **relation to neighbour** (composition rule (with a neighbour)): As a statement, i++ has the same effect as the assignment i = i + 1.
- **relation to neighbour** (composition rule (with a neighbour)): A trace records the value of each variable after each assignment runs, one row per statement.
- **relation to neighbour** (composition rule (with a neighbour)): x = y stores the value of y in x (a statement with a side effect); x == y only tests whether the two values are equal and gives a boolean. Writing = where == is meant is a compile error with int operands and a silent bug with boolean operands.
- **purpose of the whole** (plan / role rule): Assignment gives a variable its value in each role: initialization, counter update (n = n + 1), gatherer update (sum = sum + x), most-wanted holder update (max = x), or temporary (t = a).

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for assignment: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

assignment -&gt; L4 (Extended abstract): the answer reasons beyond the given code (7 ways).

- **predict a change** (conservation rule; shows `VariablesHoldExpressions`): Swapping the two sides (a = b versus b = a) changes which variable changes. Reordering assignments changes the final values. An assignment cannot be undone, because the old value is lost unless it was first saved in a temporary.
- **diagnose an error** (error rule): rule broken: The left-hand side of = must be a single variable; only the right-hand side may be an arbitrary expression. Kind: compile-time. Trigger class: Any assignment whose left side is a literal or compound expression (7 = a; a + b = c;): 'unexpected type, required: variable'.
- **transfer to a new program** (applicability rule): Use assignment whenever a variable's value must be set or updated. Use == to compare, final to forbid updates, and op= or ++ for x = x op e.
- **diagnose an error** (error rule): rule broken: A local variable may be declared only once in its scope; later changes use an assignment without the type. Kind: compile-time. Trigger class: A second 'int x = ...' for a name already declared in the same or an enclosing block: 'variable x is already defined'.
- **diagnose an error** (error rule): rule broken: A final variable is assigned exactly once; it cannot be reassigned after initialization. Kind: compile-time. Trigger class: Any assignment, ++ or op= to a final variable after its initialization: 'cannot assign a value to final variable'.
- **diagnose an error** (error rule): rule broken: = assigns and == compares; a condition needs a boolean. Kind: compile-time. Trigger class: Writing if (a = b) with int a, b gives 'incompatible types: int cannot be converted to boolean'. With boolean variables it compiles and silently assigns.
- **diagnose an error** (error rule): rule broken: The assigned value's type must fit the variable's type. Kind: compile-time. Trigger class: Assigning a double to an int, an int to a String, and so on: 'incompatible types'.

## Same topic

`assignment` belongs to the topic **Data types and terminology (literals, identifiers, variables, declarations, assignment, expressions)** (`topic1.2.a`). The topic also contains: `chained_assignment`, `data_type`, `declaration`, `definite_assignment`, `expression`, `identifier`, `literal`, `named_constants`, `naming_convention`, `operator_precedence`, `primitive_type`, `program_trace`, `variable`, `variable_swap`.

## Rules of the concept (34)

- **folk-meaning rule:** In maths, = states a symmetric, lasting equality (a = b means b = a, and x = x + 5 is false). In Java, = is a one-time, directed action: evaluate the right side, then store the result in the variable on the left.
- **wrong rule / right rule:** AssignCompares: wrong: = compares two values instead of assigning \| right: x = y copies the value of y into x; x == y is what compares them.
- **wrong rule / right rule:** AssignmentNotExpression: wrong: an assignment cannot be used inside a larger expression \| right: An assignment is an expression whose value is the value assigned, so (x = v) both stores v in x and gives v.
- **wrong rule / right rule:** AssignmentOppositeDirection: wrong: a = b copies the value of a into b. \| right: Assignment stores the value of the right side into the variable on the left.
- **wrong rule / right rule:** SwapWithoutTemp: wrong: a[i] = a[j]; a[j] = a[i]; exchanges the two values. \| right: A temporary variable must save a[i] before it is overwritten.
- **wrong rule / right rule:** VariablesHoldExpressions: wrong: = stores the expression itself, not its computed value \| right: y = x + k; stores the value that x + k has at that moment, so later changes to x do not change y.
- **wrong rule / right rule:** AssignmentCopiesObject: wrong: assigning a reference copies the object \| right: b = a; copies only the reference, so a and b refer to the same array and b[i] = v also changes a[i].
- **wrong rule / right rule:** AssignmentAddsToTarget: wrong: a = b adds the value of b to the value already in a (the accumulator model). \| right: a = b replaces the old value of a with the value of b; the old value is lost.
- **wrong rule / right rule:** AssignmentIsEquation: wrong: An assignment states a lasting equality between its two sides, so y = x - y can be solved like the equation x = 2y and x = x + 5 relates two equal quantities. \| right: An assignment is a one-time action: evaluate the right side with current values, then store the result in the left variable.
- **wrong rule / right rule:** AssignmentExchangesValues: wrong: b = a exchanges the values of a and b. \| right: b = a copies a into b and leaves a unchanged; an exchange needs a temporary variable and three assignments.
- **wrong rule / right rule:** AssignmentEmptiesSource: wrong: After b = a, a no longer holds a value, as if the value had been moved. \| right: Assignment copies; the variable on the right keeps its value.
- **wrong rule / right rule:** VariableKeepsOldValue: wrong: A variable keeps its first value after a new assignment (the static model). \| right: Each assignment or read replaces the variable's current value.
- **uneven-application rule:** Points to LT (evaluate the right side with current values, then overwrite the left variable). Applied unevenly, a student traces one segment correctly but reads the next as simultaneous equations or as a swap, giving 15 and 15 for one segment and 5 and 10 for the other.
- **identity rule:** Assignment statement: the statement variable = expression; which stores a data-type value in a variable.
- **declarative rule:** The left-hand side must be a single variable. The right-hand side can be any expression whose type is compatible with the variable's type. = is not mathematical equality (a + b = b + a and 1 = a are illegal).
- **operational sequencing rule:** First the right-hand side is fully evaluated using the variables' current values (left to right). Then that value is stored in the left-hand variable, replacing its old value, and execution moves to the next statement.
- **evaluation / result rule:** As a statement it prints nothing; its result is the new value of the left variable (after c = a + b; with a = 1234 and b = 99, c is 1333). Used as an expression, its value is the value assigned.
- **state-transition rule:** Exactly one variable, the left one, changes, and its old value is lost. Variables on the right keep their values: x = x + 5; with x = 5 makes x 10.
- **composition rule (with a neighbour):** with variable: The left side must be a declared variable whose type accepts the value. Assignment is how that variable's value changes.
- **composition rule (with a neighbour):** with declaration: A declaration can include the first assignment (int x = 5;). Assigning to a variable that was never declared does not compile.
- **composition rule (with a neighbour):** with array\_exchange: Exchanging a[i] and a[j] takes three assignments in a fixed order through a temporary, because each assignment overwrites its target.
- **composition rule (with a neighbour):** with variable\_swap: int t = a; a = b; b = t; works only in this order, because every assignment destroys its left variable's old value.
- **composition rule (with a neighbour):** with compound\_assignment: x op= e is shorthand for x = x op e. The left variable's current value is fetched first and then combined with e.
- **composition rule (with a neighbour):** with chained\_assignment: Because an assignment is an expression whose value is the value stored, and = groups right to left, a = b = 0 first stores 0 in b and then stores that 0 in a.
- **composition rule (with a neighbour):** with increment\_operators: As a statement, i++ has the same effect as the assignment i = i + 1.
- **composition rule (with a neighbour):** with program\_trace: A trace records the value of each variable after each assignment runs, one row per statement.
- **plan / role rule:** Assignment gives a variable its value in each role: initialization, counter update (n = n + 1), gatherer update (sum = sum + x), most-wanted holder update (max = x), or temporary (t = a).
- **conservation rule:** Swapping the two sides (a = b versus b = a) changes which variable changes. Reordering assignments changes the final values. An assignment cannot be undone, because the old value is lost unless it was first saved in a temporary.
- **error rule:** rule broken: A local variable may be declared only once in its scope; later changes use an assignment without the type. (compile-time)
- **error rule:** rule broken: The left-hand side of = must be a single variable; only the right-hand side may be an arbitrary expression. (compile-time)
- **error rule:** rule broken: A final variable is assigned exactly once; it cannot be reassigned after initialization. (compile-time)
- **error rule:** rule broken: = assigns and == compares; a condition needs a boolean. (compile-time)
- **error rule:** rule broken: The assigned value's type must fit the variable's type. (compile-time)
- **applicability rule:** Use assignment whenever a variable's value must be set or updated. Use == to compare, final to forbid updates, and op= or ++ for x = x op e.

## The whole prerequisite chain

- **Everything it builds on (6):** `data_type`, `declaration`, `identifier`, `literal`, `primitive_type`, `variable`
- **Everything that builds on it (18):** `accumulator_pattern`, `array_exchange`, `array_reversal`, `chained_assignment`, `compound_assignment`, `counter_pattern`, `debugging`, `frequency_counting`, `increment_operators`, `monte_carlo_simulation`, `program_trace`, `sampling_without_replacement`, `sentinel_loop`, `shuffle`, `side_effect_order`, `testing`, `two_models`, `variable_swap`
