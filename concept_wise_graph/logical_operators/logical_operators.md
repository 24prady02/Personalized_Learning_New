# logical_operators (`logical_operators`)

&amp;&amp; \|\| !

Section 1.2 Built-in Types of Data, topic 1.2.e Booleans.

![The knowledge graph around logical_operators](logical_operators.png)

## At a glance

- **Needs first:** `boolean`
- **Leads to:** `boolean_expression`, `de_morgan`, `exclusive_or`, `short_circuit`
- **Learned alongside:** `comparison_operators`
- **Misconceptions:** `BooleanPrecedence`, `NestedIfsInsteadOfLogicalOperators`, `NoSingleLogicAnd`, `SingleAmpersandForAnd`
- **Errors:** none
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 25 edges around this concept, each explained in the graph's own words.

## What it needs first (1)

A prerequisite edge means the other concept has to be understood before `logical_operators`.

### `boolean` comes before `logical_operators`

*true/false primitive*

&amp;&amp;, \|\| and ! are the operations defined on the boolean type: they take booleans and give a boolean.

- **Grounding:** book passage
- **How `logical_operators` combines with `boolean`:** The operands must be boolean, and the result is boolean; int operands are a compile-time error.
- **How `boolean` combines with `logical_operators`:** &amp;&amp;, \|\| and ! accept only boolean operands and return a boolean; applying them to ints (if (x &amp;&amp; y) with int x, y) is a compile-time error.

## What it leads to (4)

These concepts need `logical_operators` first.

### `logical_operators` comes before `boolean_expression`

*an expression that evaluates to true/false*

&amp;&amp;, \|\| and ! combine conditions p and q into one larger condition that is still true or false.

- **Grounding:** book passage
- **How `logical_operators` combines with `boolean_expression`:** Combining boolean sub-expressions with &amp;&amp;, \|\| and ! yields another boolean expression, so arbitrarily complex conditions can be built with parentheses.
- **How `boolean_expression` combines with `logical_operators`:** &amp;&amp;, \|\| and ! combine boolean sub-expressions into a larger one; ! binds tighter than comparisons, so negating a comparison needs parentheses: !(x &gt; 0).

### `logical_operators` comes before `de_morgan`

*!(a &amp;&amp; b) == !a \|\| !b and !(a \|\| b) == !a &amp;&amp; !b*

De Morgan's laws rewrite expressions built from &amp;&amp; , \|\| and !.

- **Grounding:** book passage
- **How `logical_operators` combines with `de_morgan`:** De Morgan's laws rewrite negated &amp;&amp; / \|\| expressions: !(A &amp;&amp; B) is !A \|\| !B and !(A \|\| B) is !A &amp;&amp; !B.
- **How `de_morgan` combines with `logical_operators`:** De Morgan's laws relate the three logical operators: a negated &amp;&amp; becomes an \|\| of negations and a negated \|\| becomes an &amp;&amp; of negations.

### `logical_operators` comes before `exclusive_or`

*^ on booleans is true when the operands differ*

^ on booleans is another logical operator, defined by a truth table like &amp;&amp;, \|\| and !: true exactly when its operands differ.

- **Grounding:** order only
- **How `logical_operators` combines with `exclusive_or`:** ^ on booleans is a further logical operator, true exactly when the operands differ (it equals (a \|\| b) &amp;&amp; !(a &amp;&amp; b)), but unlike &amp;&amp; and \|\| it always evaluates both operands.
- **How `exclusive_or` combines with `logical_operators`:** ^ belongs with &amp;&amp;, \|\| and ! as a boolean operator defined by a truth table, but it is not short-circuit and it binds tighter than &amp;&amp; and \|\|; a ^ b equals (a \|\| b) &amp;&amp; !(a &amp;&amp; b).

### `logical_operators` comes before `short_circuit`

*&amp;&amp;/\|\| stop evaluating once the result is known*

&amp;&amp; and \|\| evaluate their second operand only when the first has not already decided the result (false &amp;&amp; x is false, true \|\| x is true).

- **Grounding:** book passage
- **How `logical_operators` combines with `short_circuit`:** &amp;&amp; and \|\| are the short-circuit operators: in a guard such as (x != 0 &amp;&amp; y / x &gt; 1) the operand order matters, because the right test runs only when the left one allows it.
- **How `short_circuit` combines with `logical_operators`:** Short-circuiting is the defining evaluation order of &amp;&amp; and \|\| only; the book's other boolean operators (! and ^, and &amp; / \| if used) evaluate all their operands.

## Learned alongside (1)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

### `logical_operators` alongside `comparison_operators`

*== != &lt; &gt; &lt;= &gt;=*

Relational operators compare two numbers to give a boolean; logical operators combine booleans into one boolean.

- **Grounding:** book passage
- **How `logical_operators` combines with `comparison_operators`:** Comparisons bind tighter than &amp;&amp; and \|\|, so comparisons are evaluated first and their boolean results are then combined (month &gt;= 1 &amp;&amp; month &lt;= 12).
- **How `comparison_operators` combines with `logical_operators`:** Comparisons bind tighter than &amp;&amp; and \|\|, so they are evaluated first and logical operators combine their boolean results.

## Misconceptions (4)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### BooleanPrecedence

- **Wrong rule:** a \|\| b &amp;&amp; c is evaluated left to right as (a \|\| b) &amp;&amp; c.
- **Right rule:** &amp;&amp; binds tighter than \|\|, so it is a \|\| (b &amp;&amp; c).
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: a \|\| b &amp;&amp; c is evaluated left to right as (a \|\| b) &amp;&amp; c. Right rule: &amp;&amp; binds tighter than \|\|, so a \|\| b &amp;&amp; c means a \|\| (b &amp;&amp; c); with a = true, b = false, c = false the value is true, not false.
- **Also an edge from `operator_precedence`:** a \|\| b &amp;&amp; c is evaluated left to right as (a \|\| b) &amp;&amp; c.

### NestedIfsInsteadOfLogicalOperators

- **Wrong rule:** A condition on several values has to be written as nested if statements, one value per if.
- **Right rule:** Several conditions combine into one boolean expression with &amp;&amp; and \|\|, e.g. if (x == 0 &amp;&amp; y == 0).
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: A condition on several values has to be written as nested if statements, one value per if. Right rule: Several conditions combine into one boolean expression with &amp;&amp; and \|\|, e.g. if (x == 0 &amp;&amp; y == 0).
- **Also an edge from `boolean_expression`:** A condition on several values has to be written as nested if statements, one value per if.
- **Also an edge from `nested_conditionals`:** A condition on several values has to be written as nested if statements, one value per if.

### NoSingleLogicAnd

- **Wrong rule:** &amp; only works on bits, so p &amp; q cannot be used with booleans.
- **Right rule:** Java also has a &amp; operator, which the book does not use; logical and is written &amp;&amp;.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: &amp; is only a bitwise operator. Right rule: Java also has a &amp; operator, which the book does not use; on boolean operands it is a logical and that always evaluates both operands; logical and is written &amp;&amp;.
- **Shows at level L0 as:** inconsistent trace: Points to LT (! first, then &amp;&amp;, then \|\|; left operand first; right operand of &amp;&amp; / \|\| only if needed). Applied unevenly: in one row of a trace the student evaluates the right operand of &amp;&amp; although the left was false (or reads \|\| as exclusive when both operands are true) and in another row applies the rule correctly. (here mixing in: "&amp; is only a bitwise operator")

### SingleAmpersandForAnd

- **Wrong rule:** &amp; and \| are the same as &amp;&amp; and \|\| for conditions, so either can be used.
- **Right rule:** &amp;&amp; and \|\| skip the right operand when the left decides the result; &amp; and \| always evaluate both, which fails when the right side depends on the left (e.g. x != 0 &amp; y / x &gt; 1).
- **Role of this concept:** context
- **Shows at level L0 as:** misconception: wrong rule: &amp; and \| are the same as &amp;&amp; and \|\| for conditions, so either can be used. Right rule: &amp;&amp; and \|\| skip the right operand when the left decides the result; &amp; and \| always evaluate both, which fails when the right side depends on the left (e.g. x != 0 &amp; y / x &gt; 1 throws when x is 0).
- **Also an edge from `short_circuit`:** &amp; and \| are the same as &amp;&amp; and \|\| for conditions, so either can be used.

## Errors (0)

An error edge states the rule that gets broken in a program, and the right rule.

The graph has no error edge from this concept.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for logical operators: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to logical operators agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

logical operators -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (6 ways).

- **everyday reading** (folk-meaning rule): Folk meaning: English 'or' is often exclusive ('tea or coffee') and 'and' can join alternatives ('x is 1 and 2' meaning either value). Java rule: \|\| is inclusive (true when either or both operands are true) and &amp;&amp; is true only when both operands are true, so x == 1 &amp;&amp; x == 2 is always false.
- **misconception** (wrong rule / right rule; shows `NoSingleLogicAnd`): wrong rule: &amp; is only a bitwise operator. Right rule: Java also has a &amp; operator, which the book does not use; on boolean operands it is a logical and that always evaluates both operands; logical and is written &amp;&amp;.
- **misconception** (wrong rule / right rule; shows `BooleanPrecedence`): wrong rule: a \|\| b &amp;&amp; c is evaluated left to right as (a \|\| b) &amp;&amp; c. Right rule: &amp;&amp; binds tighter than \|\|, so a \|\| b &amp;&amp; c means a \|\| (b &amp;&amp; c); with a = true, b = false, c = false the value is true, not false.
- **misconception** (wrong rule / right rule; shows `NestedIfsInsteadOfLogicalOperators`): wrong rule: A condition on several values has to be written as nested if statements, one value per if. Right rule: Several conditions combine into one boolean expression with &amp;&amp; and \|\|, e.g. if (x == 0 &amp;&amp; y == 0).
- **inconsistent trace** (uneven-application rule; shows `NoSingleLogicAnd`): Points to LT (! first, then &amp;&amp;, then \|\|; left operand first; right operand of &amp;&amp; / \|\| only if needed). Applied unevenly: in one row of a trace the student evaluates the right operand of &amp;&amp; although the left was false (or reads \|\| as exclusive when both operands are true) and in another row applies the rule correctly. (here mixing in: "&amp; is only a bitwise operator")
- **misconception** (wrong rule / right rule; shows `SingleAmpersandForAnd`): wrong rule: &amp; and \| are the same as &amp;&amp; and \|\| for conditions, so either can be used. Right rule: &amp;&amp; and \|\| skip the right operand when the left decides the result; &amp; and \| always evaluate both, which fails when the right side depends on the left (e.g. x != 0 &amp; y / x &gt; 1 throws when x is 0).

### L1: Unistructural / atom x text surface

L1 for logical operators: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

logical operators -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

- **names the element** (identity rule): Logical (boolean) operators: &amp;&amp; (and), \|\| (or) and ! (not), which take boolean operands and produce a boolean.
- **states the rule** (declarative rule): a &amp;&amp; b is true if both operands are true and false otherwise; a \|\| b is false if both are false and true otherwise; !a is the opposite of a; these definitions are given in full by truth tables.

### L2: Multistructural / block x execution / preoperational

L2 for logical operators: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

logical operators -&gt; L2 (Multistructural): the answer applies the rules of logical operators to every part of the code, in order (3 ways).

- **line by line trace** (operational sequencing rule): ! is applied before &amp;&amp; and \|\|, and &amp;&amp; before \|\|; the left operand is evaluated first, and for &amp;&amp; and \|\| the right operand is evaluated only when the left has not already decided the result.
- **output prediction** (evaluation / result rule): The result is a boolean: with x = 10, x &gt; 0 &amp;&amp; x &lt; 10 is false and x &lt; 0 \|\| x &gt; 10 is false; true \|\| anything is true.
- **one step execution** (state-transition rule): The operators themselves change no variable; any side effect inside the right operand (i++, a method call) happens only if that operand is evaluated.

### L3: Relational / relations x function (concrete operational begins)

L3 for logical operators: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

logical operators -&gt; L3 (Relational): the answer relates the parts (7 ways).

- **relation to neighbour** (composition rule (with a neighbour)): Combining boolean sub-expressions with &amp;&amp;, \|\| and ! yields another boolean expression, so arbitrarily complex conditions can be built with parentheses.
- **relation to neighbour** (composition rule (with a neighbour)): &amp;&amp; and \|\| are the short-circuit operators: in a guard such as (x != 0 &amp;&amp; y / x &gt; 1) the operand order matters, because the right test runs only when the left one allows it.
- **relation to neighbour** (composition rule (with a neighbour)): Comparisons bind tighter than &amp;&amp; and \|\|, so comparisons are evaluated first and their boolean results are then combined (month &gt;= 1 &amp;&amp; month &lt;= 12).
- **relation to neighbour** (composition rule (with a neighbour)): ^ on booleans is a further logical operator, true exactly when the operands differ (it equals (a \|\| b) &amp;&amp; !(a &amp;&amp; b)), but unlike &amp;&amp; and \|\| it always evaluates both operands.
- **relation to neighbour** (composition rule (with a neighbour)): De Morgan's laws rewrite negated &amp;&amp; / \|\| expressions: !(A &amp;&amp; B) is !A \|\| !B and !(A \|\| B) is !A &amp;&amp; !B.
- **relation to neighbour** (composition rule (with a neighbour)): The operands must be boolean, and the result is boolean; int operands are a compile-time error.
- **purpose of the whole** (plan / role rule): Used to combine several conditions into one test: a range check (lo &lt;= x &amp;&amp; x &lt;= hi), alternatives (x == 0 \|\| y == 0), a guard followed by the real test (i &lt; n &amp;&amp; a[i] != 0), or a rule built step by step as in LeapYear.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for logical operators: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

logical operators -&gt; L4 (Extended abstract): the answer reasons beyond the given code (5 ways).

- **predict a change** (conservation rule; shows `NoSingleLogicAnd`): Swapping &amp;&amp; for \|\| changes the meaning; negating a whole condition requires De Morgan (negate each term and flip the operator); swapping the operands of &amp;&amp; or \|\| keeps the truth value but can change which side effects or exceptions occur.
- **transfer to a new program** (applicability rule): Use &amp;&amp; and \|\| to combine conditions into a single test, ordering operands so that cheap or protective tests come first; use nested ifs only when the cases need different actions; do not use &amp; and \| for conditions.
- **diagnose an error** (error rule): rule broken: Conditions are combined with &amp;&amp; and \|\|; &amp; and \| evaluate both operands. Kind: run-time exception. Trigger class: Using &amp; or \| where the right operand is only safe when the left decides first, e.g. x != 0 &amp; y / x &gt; 1 with x == 0 (ArithmeticException) or an out-of-range index; otherwise a silent difference only when the right side has side effects.
- **diagnose an error** (error rule): rule broken: &amp;&amp; has higher precedence than \|\|. Kind: silent logic error. Trigger class: Mixed &amp;&amp; and \|\| without parentheses intended to group the \|\| first, e.g. a \|\| b &amp;&amp; c meant as (a \|\| b) &amp;&amp; c.
- **diagnose an error** (error rule): rule broken: Logical operators take boolean operands only. Kind: compile-time. Trigger class: Applying &amp;&amp; or \|\| to int operands (if (x &amp;&amp; y) with ints) or writing and/or as words.

## Same topic

`logical_operators` belongs to the topic **Booleans** (`topic1.2.e`). The topic also contains: `boolean`, `boolean_expression`, `de_morgan`, `exclusive_or`, `short_circuit`.

## Rules of the concept (23)

- **folk-meaning rule:** Folk meaning: English 'or' is often exclusive ('tea or coffee') and 'and' can join alternatives ('x is 1 and 2' meaning either value). Java rule: \|\| is inclusive (true when either or both operands are true) and &amp;&amp; is true only when both operands are true, so x == 1 &amp;&amp; x == 2 is always false.
- **wrong rule / right rule:** BooleanPrecedence: wrong: a \|\| b &amp;&amp; c is evaluated left to right as (a \|\| b) &amp;&amp; c. \| right: &amp;&amp; binds tighter than \|\|, so a \|\| b &amp;&amp; c means a \|\| (b &amp;&amp; c); with a = true, b = false, c = false the value is true, not false.
- **wrong rule / right rule:** NoSingleLogicAnd: wrong: &amp; is only a bitwise operator. \| right: Java also has a &amp; operator, which the book does not use; on boolean operands it is a logical and that always evaluates both operands; logical and is written &amp;&amp;.
- **wrong rule / right rule:** NestedIfsInsteadOfLogicalOperators: wrong: A condition on several values has to be written as nested if statements, one value per if. \| right: Several conditions combine into one boolean expression with &amp;&amp; and \|\|, e.g. if (x == 0 &amp;&amp; y == 0).
- **wrong rule / right rule:** SingleAmpersandForAnd: wrong: &amp; and \| are the same as &amp;&amp; and \|\| for conditions, so either can be used. \| right: &amp;&amp; and \|\| skip the right operand when the left decides the result; &amp; and \| always evaluate both, which fails when the right side depends on the left (e.g. x != 0 &amp; y / x &gt; 1 throws when x is 0).
- **uneven-application rule:** Points to LT (! first, then &amp;&amp;, then \|\|; left operand first; right operand of &amp;&amp; / \|\| only if needed). Applied unevenly: in one row of a trace the student evaluates the right operand of &amp;&amp; although the left was false (or reads \|\| as exclusive when both operands are true) and in another row applies the rule correctly.
- **identity rule:** Logical (boolean) operators: &amp;&amp; (and), \|\| (or) and ! (not), which take boolean operands and produce a boolean.
- **declarative rule:** a &amp;&amp; b is true if both operands are true and false otherwise; a \|\| b is false if both are false and true otherwise; !a is the opposite of a; these definitions are given in full by truth tables.
- **operational sequencing rule:** ! is applied before &amp;&amp; and \|\|, and &amp;&amp; before \|\|; the left operand is evaluated first, and for &amp;&amp; and \|\| the right operand is evaluated only when the left has not already decided the result.
- **evaluation / result rule:** The result is a boolean: with x = 10, x &gt; 0 &amp;&amp; x &lt; 10 is false and x &lt; 0 \|\| x &gt; 10 is false; true \|\| anything is true.
- **state-transition rule:** The operators themselves change no variable; any side effect inside the right operand (i++, a method call) happens only if that operand is evaluated.
- **composition rule (with a neighbour):** with boolean\_expression: Combining boolean sub-expressions with &amp;&amp;, \|\| and ! yields another boolean expression, so arbitrarily complex conditions can be built with parentheses.
- **composition rule (with a neighbour):** with short\_circuit: &amp;&amp; and \|\| are the short-circuit operators: in a guard such as (x != 0 &amp;&amp; y / x &gt; 1) the operand order matters, because the right test runs only when the left one allows it.
- **composition rule (with a neighbour):** with comparison\_operators: Comparisons bind tighter than &amp;&amp; and \|\|, so comparisons are evaluated first and their boolean results are then combined (month &gt;= 1 &amp;&amp; month &lt;= 12).
- **composition rule (with a neighbour):** with exclusive\_or: ^ on booleans is a further logical operator, true exactly when the operands differ (it equals (a \|\| b) &amp;&amp; !(a &amp;&amp; b)), but unlike &amp;&amp; and \|\| it always evaluates both operands.
- **composition rule (with a neighbour):** with de\_morgan: De Morgan's laws rewrite negated &amp;&amp; / \|\| expressions: !(A &amp;&amp; B) is !A \|\| !B and !(A \|\| B) is !A &amp;&amp; !B.
- **composition rule (with a neighbour):** with boolean: The operands must be boolean, and the result is boolean; int operands are a compile-time error.
- **plan / role rule:** Used to combine several conditions into one test: a range check (lo &lt;= x &amp;&amp; x &lt;= hi), alternatives (x == 0 \|\| y == 0), a guard followed by the real test (i &lt; n &amp;&amp; a[i] != 0), or a rule built step by step as in LeapYear.
- **conservation rule:** Swapping &amp;&amp; for \|\| changes the meaning; negating a whole condition requires De Morgan (negate each term and flip the operator); swapping the operands of &amp;&amp; or \|\| keeps the truth value but can change which side effects or exceptions occur.
- **error rule:** rule broken: Conditions are combined with &amp;&amp; and \|\|; &amp; and \| evaluate both operands. (run-time exception)
- **error rule:** rule broken: &amp;&amp; has higher precedence than \|\|. (silent logic error)
- **error rule:** rule broken: Logical operators take boolean operands only. (compile-time)
- **applicability rule:** Use &amp;&amp; and \|\| to combine conditions into a single test, ordering operands so that cheap or protective tests come first; use nested ifs only when the cases need different actions; do not use &amp; and \| for conditions.

## The whole prerequisite chain

- **Everything it builds on (3):** `boolean`, `data_type`, `primitive_type`
- **Everything that builds on it (55):** `accumulator_pattern`, `animation`, `array_copy`, `array_reversal`, `array_traversal`, `boolean_expression`, `boolean_flag_array`, `break_statement`, `conditional_operator`, `continue_statement`, `convergence_rate`, `convergence_test`, `counter_pattern`, `dangling_else`, `de_morgan`, `do_while_loop`, `else_if_chain`, `enhanced_for`, `exclusive_or`, `fencepost_loop`, `flag_search_loop`, `for_loop`, `frequency_counting`, `function_plotting`, `if_else_statement`, `if_statement`, `increment_operators`, `infinite_loop`, `labeled_break`, `loop_body`, `loop_control`, `loop_invariant_reasoning`, `loop_performance`, `loop_scope`, `loop_variable`, `matrix_operations`, `monte_carlo_simulation`, `mouse_interaction`, `nested_conditionals`, `nested_loops`, `number_conversion`, `off_by_one_error`, `power_method`, `random_move`, `row_major_order`, `running_extreme`, `sentinel_loop`, `short_circuit`, `side_effect_order`, `simulation_loop`, `standard_audio`, `switch_statement`, `syntax_template`, `two_models`, `while_loop`
