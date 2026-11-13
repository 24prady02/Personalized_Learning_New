# expression (`expression`)

anything that evaluates to a value

Section 1.2 Built-in Types of Data, topic 1.2.a Data types and terminology (literals, identifiers, variables, declarations, assignment, expressions).

![The knowledge graph around expression](expression.png)

## At a glance

- **Needs first:** `arithmetic_operators`, `variable`
- **Leads to:** `comparison_operators`, `conditional_operator`, `method_call`, `operator_precedence`
- **Learned alongside:** nothing
- **Misconceptions:** `AssignmentIsEquation`, `AssignmentNotExpression`, `NoAtomicExpression`, `OutsideInMethodNesting`, `ParenthesesOnlyIfArgument`, `TargetTyping`, `VariablesHoldExpressions`
- **Errors:** `ExpressionOnLeftOfAssignment`
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 47 edges around this concept, each explained in the graph's own words.

## What it needs first (2)

A prerequisite edge means the other concept has to be understood before `expression`.

### `arithmetic_operators` comes before `expression`

*+ - \* / %*

An operator combines operand values a and b into a new value, so operators build larger expressions from smaller ones.

- **Grounding:** book passage
- **How `expression` combines with `arithmetic_operators`:** Operators combine operand values into a new value, and the operand types choose the operation (int / truncates, double / does not).
- **How `arithmetic_operators` combines with `expression`:** Operators build larger expressions from smaller ones, and each operand can itself be any expression.

### `variable` comes before `expression`

*a named, typed box that holds a value*

An expression can be a literal, a variable, or operations on them; we compute with a variable by using its name in an expression.

- **Grounding:** book passage
- **How `expression` combines with `variable`:** A variable name inside an expression contributes the variable's value at the moment of evaluation.
- **How `variable` combines with `expression`:** A variable name is itself an expression whose value is the variable's current value, and it combines with operators into larger expressions.

## What it leads to (4)

These concepts need `expression` first.

### `expression` comes before `comparison_operators`

*== != &lt; &gt; &lt;= &gt;=*

Comparison operators build expressions whose value is a boolean, so one must already know what an expression is to understand a &lt; b.

- **Grounding:** order only
- **How `expression` combines with `comparison_operators`:** A comparison takes numeric expressions and yields a boolean expression, and it has lower precedence than arithmetic, so a + b &lt; c compares the sum.
- **How `comparison_operators` combines with `expression`:** A comparison is itself an expression whose value is a boolean, so it can appear anywhere a boolean is needed, including on the right of an assignment (boolean ok = x &gt; y;).

### `expression` comes before `conditional_operator`

*c ? a : b -- an expression that picks one of two values*

c ? a : b is an expression: the boolean c decides which of the two other expressions gives the value.

- **Grounding:** spec passage

### `expression` comes before `method_call`

*name(arguments) -- invokes a library method and uses its return value*

Method arguments may be expressions, and a method call can be used in expressions in the same way as variables and literals.

- **Grounding:** book passage
- **How `expression` combines with `method_call`:** A method call is an expression usable wherever a value of its return type is, and its arguments are expressions evaluated before the call.
- **How `method_call` combines with `expression`:** Arguments may be arbitrary expressions of the right type, and the call itself is an expression usable inside larger ones (Math.sin(x) \* Math.cos(y)).

### `expression` comes before `operator_precedence`

*the order operators bind in an expression*

When an expression has several operators, precedence decides which operands are combined first, and equal-precedence operators go left to right.

- **Grounding:** book passage
- **How `expression` combines with `operator_precedence`:** With several operators, precedence and left associativity decide the grouping, and parentheses override both.
- **How `operator_precedence` combines with `expression`:** Precedence decides the grouping of a multi-operator expression, and a parenthesized subexpression is evaluated as one unit with its own value.

## Learned alongside (0)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

No parallel edge touches this concept.

## Misconceptions (7)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### AssignmentIsEquation

- **Wrong rule:** An assignment states a lasting equality between its two sides, so y = x - y can be solved like the equation x = 2y and x = x + 5 relates two equal quantities.
- **Right rule:** An assignment is a one-time action: evaluate the right side with current values, then store the result in the left variable.
- **Role of this concept:** context
- **Shows at level L0 as:** misconception: wrong rule: An assignment states a lasting equality between its two sides, so y = x - y can be solved like the equation x = 2y and x = x + 5 relates two equal quantities. Right rule: An assignment is a one-time action: evaluate the right side with current values, then store the result in the left variable.
- **Also an edge from `assignment`:** An assignment states a lasting equality between its two sides, so y = x - y can be solved like the equation x = 2y and x = x + 5 relates two equal quantities.

### AssignmentNotExpression

- **Wrong rule:** An assignment cannot be used inside a larger expression, so a condition like (x = read()) != v is not allowed.
- **Right rule:** An assignment is an expression whose value is the value assigned, so (x = v) both stores v in x and gives v.
- **Role of this concept:** context
- **Shows at level L0 as:** misconception: wrong rule: an assignment cannot be used inside a larger expression. Right rule: An assignment is an expression whose value is the value assigned, so (x = v) both stores v in x and gives v.
- **Also an edge from `assignment`:** An assignment cannot be used inside a larger expression, so a condition like (x = read()) != v is not allowed.
- **Also an edge from `chained_assignment`:** an assignment cannot be used inside a larger expression
- **Also an edge from `read_loop_idiom`:** A read and a test cannot be combined, so while ((x = read()) != end) is not allowed.

### NoAtomicExpression

- **Wrong rule:** A single variable x or a literal on its own is not an expression.
- **Right rule:** A single variable or literal is an expression whose value is just that value.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: a single literal or variable "isn't an expression". Right rule: A single variable or literal is an expression whose value is just that value.
- **Shows at level L0 as:** inconsistent trace: Points to LT (replace each variable with its current value, then apply operators in precedence order). Applied unevenly, a student substitutes current values for some variables and old or future values for others, or respects precedence in one subexpression only. (here mixing in: "a single literal or variable "isn't an expression"")

### OutsideInMethodNesting

- **Wrong rule:** In f(g(x)), f runs first and then g runs.
- **Right rule:** In f(g(x)), g(x) is evaluated first and its result is passed to f.
- **Role of this concept:** context
- **Shows at level L0 as:** misconception: wrong rule: nested calls run outside-in, not arguments-first. Right rule: In f(g(x)), g(x) is evaluated first and its result is passed to f.
- **Also an edge from `method_call`:** nested calls run outside-in, not arguments-first

### ParenthesesOnlyIfArgument

- **Wrong rule:** () are optional on a no-argument call like println
- **Right rule:** A method call always needs parentheses, so an empty line is printed with System.out.println();.
- **Role of this concept:** context
- **Shows at level L0 as:** misconception: wrong rule: () are optional on a no-argument call like println. Right rule: A method call always needs parentheses, so an empty line is printed with System.out.println();.
- **Also an edge from `method_call`:** () are optional on a no-argument call like println
- **Also an edge from `print`:** println with nothing to print can be written System.out.println; without the parentheses.
- **Also an edge from `println`:** println with nothing to print can be written System.out.println; without the parentheses.

### TargetTyping

- **Wrong rule:** The type of a numerical expression depends on the type expected by the surrounding context, so double d = a / b; keeps the fraction.
- **Right rule:** The type of a numerical expression is determined by the expression, so double d = a / b; with int a and b still divides as ints.
- **Role of this concept:** context
- **Shows at level L0 as:** misconception: wrong rule: The type of a numerical expression depends on the type expected by the surrounding context, so double d = a / b; keeps the fraction. Right rule: The type of a numerical expression is determined by the expression, so double d = a / b; with int a and b still divides as ints.
- **Also an edge from `integer_division`:** The type of a numerical expression depends on the type expected by the surrounding context, so double d = a / b; keeps the fraction.
- **Also an edge from `type_conversion`:** The type of a numerical expression depends on the type expected by the surrounding context, so double d = a / b; keeps the fraction.

### VariablesHoldExpressions

- **Wrong rule:** = stores the expression itself, not its computed value
- **Right rule:** y = x + k; stores the value that x + k has at that moment, so later changes to x do not change y.
- **Role of this concept:** context
- **Shows at level L0 as:** misconception: wrong rule: = stores the expression itself, not its computed value. Right rule: y = x + k; stores the value that x + k has at that moment, so later changes to x do not change y.
- **Also an edge from `assignment`:** y = x + k; makes y always equal to x + k, so when x changes later, y changes too.
- **Also an edge from `variable`:** = stores the expression itself, not its computed value

## Errors (1)

An error edge states the rule that gets broken in a program, and the right rule.

### ExpressionOnLeftOfAssignment

- **Wrong rule:** Writes a + b = c; or 7 = a; as if = were a math equation.
- **Right rule:** The left side of an assignment must be a single variable; only the right side can be an expression.
- **Role of this concept:** context
- **Also an edge from `assignment`:** Writes a + b = c; or 7 = a; as if = were a math equation.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for expression: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to expression agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

expression -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (9 ways).

- **everyday reading** (folk-meaning rule): In maths an expression such as 7/2 or x + y names an exact number, and 'expression' means a formula with operators. In Java, any code that evaluates to a typed value is an expression, including a lone literal or variable, and with ints 7/2 evaluates to 3.
- **misconception** (wrong rule / right rule; shows `NoAtomicExpression`): wrong rule: a single literal or variable "isn't an expression". Right rule: A single variable or literal is an expression whose value is just that value.
- **inconsistent trace** (uneven-application rule; shows `NoAtomicExpression`): Points to LT (replace each variable with its current value, then apply operators in precedence order). Applied unevenly, a student substitutes current values for some variables and old or future values for others, or respects precedence in one subexpression only. (here mixing in: "a single literal or variable "isn't an expression"")
- **misconception** (wrong rule / right rule; shows `AssignmentNotExpression`): wrong rule: an assignment cannot be used inside a larger expression. Right rule: An assignment is an expression whose value is the value assigned, so (x = v) both stores v in x and gives v.
- **misconception** (wrong rule / right rule; shows `ParenthesesOnlyIfArgument`): wrong rule: () are optional on a no-argument call like println. Right rule: A method call always needs parentheses, so an empty line is printed with System.out.println();.
- **misconception** (wrong rule / right rule; shows `TargetTyping`): wrong rule: The type of a numerical expression depends on the type expected by the surrounding context, so double d = a / b; keeps the fraction. Right rule: The type of a numerical expression is determined by the expression, so double d = a / b; with int a and b still divides as ints.
- **misconception** (wrong rule / right rule; shows `VariablesHoldExpressions`): wrong rule: = stores the expression itself, not its computed value. Right rule: y = x + k; stores the value that x + k has at that moment, so later changes to x do not change y.
- **misconception** (wrong rule / right rule; shows `OutsideInMethodNesting`): wrong rule: nested calls run outside-in, not arguments-first. Right rule: In f(g(x)), g(x) is evaluated first and its result is passed to f.
- **misconception** (wrong rule / right rule; shows `AssignmentIsEquation`): wrong rule: An assignment states a lasting equality between its two sides, so y = x - y can be solved like the equation x = 2y and x = x + 5 relates two equal quantities. Right rule: An assignment is a one-time action: evaluate the right side with current values, then store the result in the left variable.

### L1: Unistructural / atom x text surface

L1 for expression: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

expression -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

- **names the element** (identity rule): Expression: a literal, a variable, or a sequence of operations (operators, method calls) on them that produces one value.
- **states the rule** (declarative rule): Each operand of an operator can itself be any expression, and a parenthesized expression has the same value as the expression inside. Every expression has a type, determined by its operators and operands.

### L2: Multistructural / block x execution / preoperational

L2 for expression: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

expression -&gt; L2 (Multistructural): the answer applies the rules of expression to every part of the code, in order (3 ways).

- **line by line trace** (operational sequencing rule): Operands are evaluated left to right, each fully before its operator is applied. Precedence and parentheses decide the grouping, and a method's arguments are all evaluated before the method is called.
- **output prediction** (evaluation / result rule): An expression produces one value of a type fixed by its operands: hour \* 60 + minute with hour = 11 and minute = 59 is the int 719.
- **one step execution** (state-transition rule): Evaluating an expression changes no variable unless it contains an assignment, ++/-- or a method with side effects. The value goes to the enclosing statement, and an expression statement discards it.

### L3: Relational / relations x function (concrete operational begins)

L3 for expression: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

expression -&gt; L3 (Relational): the answer relates the parts (6 ways).

- **relation to neighbour** (composition rule (with a neighbour)): A variable name inside an expression contributes the variable's value at the moment of evaluation.
- **relation to neighbour** (composition rule (with a neighbour)): Operators combine operand values into a new value, and the operand types choose the operation (int / truncates, double / does not).
- **relation to neighbour** (composition rule (with a neighbour)): With several operators, precedence and left associativity decide the grouping, and parentheses override both.
- **relation to neighbour** (composition rule (with a neighbour)): A comparison takes numeric expressions and yields a boolean expression, and it has lower precedence than arithmetic, so a + b &lt; c compares the sum.
- **relation to neighbour** (composition rule (with a neighbour)): A method call is an expression usable wherever a value of its return type is, and its arguments are expressions evaluated before the call.
- **purpose of the whole** (plan / role rule): Expressions compute new values from existing ones. They form the right side of every assignment, every condition, every method argument and every printed value.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for expression: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

expression -&gt; L4 (Extended abstract): the answer reasons beyond the given code (6 ways).

- **predict a change** (conservation rule; shows `NoAtomicExpression`): Adding parentheses that match the default grouping keeps the value, and rewriting with an equivalent formula (4 \* (x - 3) as 4\*x - 12) keeps it for ints. Changing one operand's type (3 to 3.0) can change both the result's type and its value.
- **transfer to a new program** (applicability rule): Use an expression wherever a value is needed. Split a long or unclear expression into named intermediate variables, and add parentheses wherever the grouping is not obvious.
- **diagnose an error** (error rule): rule broken: The left-hand side of = must be a single variable; only the right-hand side may be an arbitrary expression. Kind: compile-time. Trigger class: Any assignment whose left side is a literal or compound expression (7 = a; a + b = c;): 'unexpected type, required: variable'.
- **diagnose an error** (error rule): rule broken: Only assignments, increments, method calls and object creation can stand alone as statements. Kind: compile-time. Trigger class: A bare expression line such as x + 1; or a == b;: 'not a statement'.
- **diagnose an error** (error rule): rule broken: Operators accept only operands of suitable types. Kind: compile-time. Trigger class: Applying arithmetic to Strings ("Hello" - 1) or comparing booleans with &lt;: 'bad operand types'.
- **diagnose an error** (error rule): rule broken: An int division or remainder by zero cannot be evaluated. Kind: run-time exception. Trigger class: Any int / or % whose right operand evaluates to 0: ArithmeticException.

## Same topic

`expression` belongs to the topic **Data types and terminology (literals, identifiers, variables, declarations, assignment, expressions)** (`topic1.2.a`). The topic also contains: `assignment`, `chained_assignment`, `data_type`, `declaration`, `definite_assignment`, `identifier`, `literal`, `named_constants`, `naming_convention`, `operator_precedence`, `primitive_type`, `program_trace`, `variable`, `variable_swap`.

## Rules of the concept (26)

- **folk-meaning rule:** In maths an expression such as 7/2 or x + y names an exact number, and 'expression' means a formula with operators. In Java, any code that evaluates to a typed value is an expression, including a lone literal or variable, and with ints 7/2 evaluates to 3.
- **wrong rule / right rule:** AssignmentNotExpression: wrong: an assignment cannot be used inside a larger expression \| right: An assignment is an expression whose value is the value assigned, so (x = v) both stores v in x and gives v.
- **wrong rule / right rule:** NoAtomicExpression: wrong: a single literal or variable "isn't an expression" \| right: A single variable or literal is an expression whose value is just that value.
- **wrong rule / right rule:** ParenthesesOnlyIfArgument: wrong: () are optional on a no-argument call like println \| right: A method call always needs parentheses, so an empty line is printed with System.out.println();.
- **wrong rule / right rule:** TargetTyping: wrong: The type of a numerical expression depends on the type expected by the surrounding context, so double d = a / b; keeps the fraction. \| right: The type of a numerical expression is determined by the expression, so double d = a / b; with int a and b still divides as ints.
- **wrong rule / right rule:** VariablesHoldExpressions: wrong: = stores the expression itself, not its computed value \| right: y = x + k; stores the value that x + k has at that moment, so later changes to x do not change y.
- **wrong rule / right rule:** OutsideInMethodNesting: wrong: nested calls run outside-in, not arguments-first \| right: In f(g(x)), g(x) is evaluated first and its result is passed to f.
- **wrong rule / right rule:** AssignmentIsEquation: wrong: An assignment states a lasting equality between its two sides, so y = x - y can be solved like the equation x = 2y and x = x + 5 relates two equal quantities. \| right: An assignment is a one-time action: evaluate the right side with current values, then store the result in the left variable.
- **uneven-application rule:** Points to LT (replace each variable with its current value, then apply operators in precedence order). Applied unevenly, a student substitutes current values for some variables and old or future values for others, or respects precedence in one subexpression only.
- **identity rule:** Expression: a literal, a variable, or a sequence of operations (operators, method calls) on them that produces one value.
- **declarative rule:** Each operand of an operator can itself be any expression, and a parenthesized expression has the same value as the expression inside. Every expression has a type, determined by its operators and operands.
- **operational sequencing rule:** Operands are evaluated left to right, each fully before its operator is applied. Precedence and parentheses decide the grouping, and a method's arguments are all evaluated before the method is called.
- **evaluation / result rule:** An expression produces one value of a type fixed by its operands: hour \* 60 + minute with hour = 11 and minute = 59 is the int 719.
- **state-transition rule:** Evaluating an expression changes no variable unless it contains an assignment, ++/-- or a method with side effects. The value goes to the enclosing statement, and an expression statement discards it.
- **composition rule (with a neighbour):** with variable: A variable name inside an expression contributes the variable's value at the moment of evaluation.
- **composition rule (with a neighbour):** with arithmetic\_operators: Operators combine operand values into a new value, and the operand types choose the operation (int / truncates, double / does not).
- **composition rule (with a neighbour):** with operator\_precedence: With several operators, precedence and left associativity decide the grouping, and parentheses override both.
- **composition rule (with a neighbour):** with comparison\_operators: A comparison takes numeric expressions and yields a boolean expression, and it has lower precedence than arithmetic, so a + b &lt; c compares the sum.
- **composition rule (with a neighbour):** with method\_call: A method call is an expression usable wherever a value of its return type is, and its arguments are expressions evaluated before the call.
- **plan / role rule:** Expressions compute new values from existing ones. They form the right side of every assignment, every condition, every method argument and every printed value.
- **conservation rule:** Adding parentheses that match the default grouping keeps the value, and rewriting with an equivalent formula (4 \* (x - 3) as 4\*x - 12) keeps it for ints. Changing one operand's type (3 to 3.0) can change both the result's type and its value.
- **error rule:** rule broken: The left-hand side of = must be a single variable; only the right-hand side may be an arbitrary expression. (compile-time)
- **error rule:** rule broken: Only assignments, increments, method calls and object creation can stand alone as statements. (compile-time)
- **error rule:** rule broken: Operators accept only operands of suitable types. (compile-time)
- **error rule:** rule broken: An int division or remainder by zero cannot be evaluated. (run-time exception)
- **applicability rule:** Use an expression wherever a value is needed. Split a long or unclear expression into named intermediate variables, and add parentheses wherever the grouping is not obvious.

## The whole prerequisite chain

- **Everything it builds on (6):** `arithmetic_operators`, `data_type`, `identifier`, `literal`, `primitive_type`, `variable`
- **Everything that builds on it (65):** `accumulator_pattern`, `animation`, `api`, `array_copy`, `array_reversal`, `array_traversal`, `boolean_expression`, `boolean_flag_array`, `break_statement`, `comparison_operators`, `conditional_operator`, `continue_statement`, `convergence_rate`, `convergence_test`, `coordinate_scaling`, `counter_pattern`, `dangling_else`, `do_while_loop`, `drawing_shapes`, `else_if_chain`, `enhanced_for`, `fencepost_loop`, `flag_search_loop`, `for_loop`, `frequency_counting`, `function_plotting`, `if_else_statement`, `if_statement`, `increment_operators`, `infinite_loop`, `labeled_break`, `loop_body`, `loop_control`, `loop_invariant_reasoning`, `loop_performance`, `loop_scope`, `loop_variable`, `math_library`, `math_random`, `math_round`, `matrix_operations`, `method_call`, `monte_carlo_simulation`, `mouse_interaction`, `nested_conditionals`, `nested_loops`, `number_conversion`, `off_by_one_error`, `operator_precedence`, `power_method`, `random_move`, `row_major_order`, `running_extreme`, `sampling_without_replacement`, `sentinel_loop`, `shuffle`, `side_effect_order`, `simulation_loop`, `standard_audio`, `standard_drawing`, `switch_statement`, `syntax_template`, `trig_functions`, `two_models`, `while_loop`
