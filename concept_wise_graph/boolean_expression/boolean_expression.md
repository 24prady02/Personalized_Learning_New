# boolean_expression (`boolean_expression`)

an expression that evaluates to true/false

Section 1.2 Built-in Types of Data, topic 1.2.e Booleans.

![The knowledge graph around boolean_expression](boolean_expression.png)

## At a glance

- **Needs first:** `comparison_operators`, `logical_operators`
- **Leads to:** `if_statement`, `random_move`, `syntax_template`, `while_loop`
- **Learned alongside:** nothing
- **Misconceptions:** `ArithmeticInsteadOfBoolean`, `ChainedComparison`, `ComparisonWithBooleanLiteral`, `LoopForOneTimeTest`, `MapToBooleanWithConditionalOperator`, `MapToBooleanWithIf`, `NestedIfsInsteadOfLogicalOperators`
- **Errors:** `ElseWithCondition`
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 35 edges around this concept, each explained in the graph's own words.

## What it needs first (2)

A prerequisite edge means the other concept has to be understood before `boolean_expression`.

### `comparison_operators` comes before `boolean_expression`

*== != &lt; &gt; &lt;= &gt;=*

A comparison such as x &lt; y produces a boolean result; comparisons together with boolean logic provide the basis for decision-making.

- **Grounding:** book passage
- **How `boolean_expression` combines with `comparison_operators`:** Comparisons are the atoms of boolean expressions; because they bind tighter than &amp;&amp; and \|\|, month &gt;= 1 &amp;&amp; month &lt;= 12 groups as (month &gt;= 1) &amp;&amp; (month &lt;= 12) without parentheses.
- **How `comparison_operators` combines with `boolean_expression`:** Comparisons are the building blocks of conditions: together with boolean logic they provide the basis for decision-making.

### `logical_operators` comes before `boolean_expression`

*&amp;&amp; \|\| !*

&amp;&amp;, \|\| and ! combine conditions p and q into one larger condition that is still true or false.

- **Grounding:** book passage
- **How `boolean_expression` combines with `logical_operators`:** &amp;&amp;, \|\| and ! combine boolean sub-expressions into a larger one; ! binds tighter than comparisons, so negating a comparison needs parentheses: !(x &gt; 0).
- **How `logical_operators` combines with `boolean_expression`:** Combining boolean sub-expressions with &amp;&amp;, \|\| and ! yields another boolean expression, so arbitrarily complex conditions can be built with parentheses.

## What it leads to (4)

These concepts need `boolean_expression` first.

### `boolean_expression` comes before `if_statement`

*run a block only when the condition holds*

An if runs its block only when its boolean expression evaluates to true.

- **Grounding:** book passage
- **How `boolean_expression` combines with `if_statement`:** The if statement evaluates its boolean expression once and runs its block only when the value is true; the expression must have type boolean, so if (x = 5) with int x does not compile.
- **How `if_statement` combines with `boolean_expression`:** The condition must be a boolean expression; a non-boolean condition such as if (t = goal) with int t is a compile-time error, while if (b = false) with boolean b compiles and assigns.

### `boolean_expression` comes before `random_move`

*pick the next page from a cumulative-probability test*

The next page is chosen by testing the condition r &lt; sum for each candidate page j in turn.

- **Grounding:** book passage
- **How `boolean_expression` combines with `random_move`:** In RandomSurfer the boolean expression r &lt; sum is evaluated for each candidate page j in turn, as sum grows; the first j for which it is true is the chosen page.
- **How `random_move` combines with `boolean_expression`:** The relational test r &lt; sum decides both the chosen page and the early break; &lt; (not &lt;=) matches the half-open interval endpoint tracked by sum.

### `boolean_expression` comes before `syntax_template`

*Template notation: the book's notation for a construct: a name in angle brackets, such as &lt;boolean expression&gt;, stands for any instance of that construct*

In the template if (&lt;boolean expression&gt;) { &lt;statements&gt; }, &lt;boolean expression&gt; stands for any expression of type boolean.

- **Grounding:** book passage
- **How `boolean_expression` combines with `syntax_template`:** In the template if (&lt;boolean expression&gt;) { &lt;statements&gt; } the placeholder may be filled by any boolean-typed expression: a literal, a boolean variable, a comparison or a combination with logical operators.
- **How `syntax_template` combines with `boolean_expression`:** The \`&lt;boolean expression&gt;\` slot accepts only expressions of type boolean (\`x &gt; y\`, \`found\`, \`a &amp;&amp; b\`). An int expression or an assignment such as \`x = y\` with int x is a compile error in that slot.

### `boolean_expression` comes before `while_loop`

*repeat a block while a condition holds*

A while tests its boolean condition before every pass and stops the first time it evaluates to false.

- **Grounding:** book passage
- **How `boolean_expression` combines with `while_loop`:** The while loop re-evaluates its boolean expression before every pass and stops the first time it is false, so some variable in the expression must change in the body or the loop never ends.
- **How `while_loop` combines with `boolean_expression`:** The loop condition is a boolean expression evaluated before every pass; the loop stops the first time it is false, so the body must eventually make it false.

## Learned alongside (0)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

No parallel edge touches this concept.

## Misconceptions (7)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### ArithmeticInsteadOfBoolean

- **Wrong rule:** A true/false question is answered with arithmetic (e.g. 1 for true).
- **Right rule:** A logic question is written as a boolean expression whose value is true or false.
- **Role of this concept:** context
- **Shows at level L0 as:** misconception: wrong rule: A true/false question is answered with arithmetic (e.g. 1 for true). Right rule: A logic question is written as a boolean expression whose value is true or false, e.g. (year % 4 == 0).
- **Also an edge from `boolean`:** A true/false question is answered with arithmetic (e.g. 1 for true).

### ChainedComparison

- **Wrong rule:** 90 &lt;= grade &lt;= 100 tests whether grade is between 90 and 100.
- **Right rule:** a &lt; b &lt; c does not compile (a &lt; b is a boolean); a range test is written 90 &lt;= grade &amp;&amp; grade &lt;= 100.
- **Role of this concept:** context
- **Shows at level L0 as:** misconception: wrong rule: 90 &lt;= grade &lt;= 100 tests whether grade is between 90 and 100. Right rule: a &lt; b &lt; c does not compile (a &lt; b is a boolean, which cannot be compared with &lt;); a range test is written 90 &lt;= grade &amp;&amp; grade &lt;= 100.
- **Also an edge from `comparison_operators`:** 90 &lt;= grade &lt;= 100 tests whether grade is between 90 and 100.

### ComparisonWithBooleanLiteral

- **Wrong rule:** To test a boolean b you must write if (b == true).
- **Right rule:** if (b) already tests b, so writing == true adds nothing.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: You must write == true / == false to test a boolean. Right rule: if (b) already tests b, and if (!b) tests that it is false, so == true adds nothing.
- **Shows at level L0 as:** inconsistent trace: Points to LT (arithmetic first, then comparisons, then !, &amp;&amp;, \|\|, left to right, with short-circuit). Applied unevenly: the student evaluates &amp;&amp; before a comparison in one sub-expression, or evaluates the right operand of &amp;&amp; on a pass where the left was already false. (here mixing in: "you must write == true / == false to test a boolean")
- **Also an edge from `comparison_operators`:** you must write == true / == false to test a boolean

### LoopForOneTimeTest

- **Wrong rule:** Uses a loop where a condition needs to be tested only once.
- **Right rule:** A test made once is an if; a loop repeats.
- **Role of this concept:** context
- **Shows at level L0 as:** misconception: wrong rule: Uses a loop where a condition needs to be tested only once. Right rule: A test made once is an if; a while re-tests its condition and repeats its body for as long as the condition is true.
- **Also an edge from `if_statement`:** Uses a loop where a condition needs to be tested only once.
- **Also an edge from `while_loop`:** Uses a loop where a condition needs to be tested only once.

### MapToBooleanWithConditionalOperator

- **Wrong rule:** To get a boolean from x &gt; y you need ok = (x &gt; y) ? true : false;.
- **Right rule:** ok = (x &gt; y); already gives the boolean, so the ? : is unnecessary.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: You need ? : to turn a boolean expression into a boolean (ok = x &gt; y ? true : false). Right rule: ok = (x &gt; y); already gives the boolean, so the ? : is unnecessary.
- **Also an edge from `conditional_operator`:** you need ? : to do the same

### MapToBooleanWithIf

- **Wrong rule:** To store whether x &gt; y in a boolean you need if (x &gt; y) ok = true; else ok = false;.
- **Right rule:** ok = (x &gt; y); stores the result of the comparison directly.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: You need an if to turn a boolean expression into a boolean. Right rule: ok = (x &gt; y); stores the result of the comparison directly.
- **Also an edge from `if_statement`:** you need an if to turn a boolean expression into a boolean

### NestedIfsInsteadOfLogicalOperators

- **Wrong rule:** A condition on several values has to be written as nested if statements, one value per if.
- **Right rule:** Several conditions combine into one boolean expression with &amp;&amp; and \|\|, e.g. if (x == 0 &amp;&amp; y == 0).
- **Role of this concept:** context
- **Shows at level L0 as:** misconception: wrong rule: A condition on several values has to be written as nested if statements, one value per if. Right rule: Several conditions combine into one boolean expression with &amp;&amp; and \|\|, e.g. if (x == 0 &amp;&amp; y == 0).
- **Also an edge from `logical_operators`:** A condition on several values has to be written as nested if statements, one value per if.
- **Also an edge from `nested_conditionals`:** A condition on several values has to be written as nested if statements, one value per if.

## Errors (1)

An error edge states the rule that gets broken in a program, and the right rule.

### ElseWithCondition

- **Wrong rule:** Writes else (x &gt; 0) with a condition but no if.
- **Right rule:** else takes no condition; use else if (x &gt; 0).
- **Role of this concept:** context
- **Also an edge from `if_else_statement`:** Writes else (x &gt; 0) with a condition but no if.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for boolean expression: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to boolean expression agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

boolean expression -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (9 ways).

- **everyday reading** (folk-meaning rule): Folk meaning: maths writes a range as 90 &lt;= grade &lt;= 100 and English says 'if x is 1 or 2'. Java rule: each comparison is a separate boolean expression and they must be joined explicitly: 90 &lt;= grade &amp;&amp; grade &lt;= 100, x == 1 \|\| x == 2; 90 &lt;= grade &lt;= 100 does not compile because 90 &lt;= grade is already a boolean.
- **misconception** (wrong rule / right rule; shows `ComparisonWithBooleanLiteral`): wrong rule: You must write == true / == false to test a boolean. Right rule: if (b) already tests b, and if (!b) tests that it is false, so == true adds nothing.
- **misconception** (wrong rule / right rule; shows `MapToBooleanWithIf`): wrong rule: You need an if to turn a boolean expression into a boolean. Right rule: ok = (x &gt; y); stores the result of the comparison directly.
- **misconception** (wrong rule / right rule; shows `MapToBooleanWithConditionalOperator`): wrong rule: You need ? : to turn a boolean expression into a boolean (ok = x &gt; y ? true : false). Right rule: ok = (x &gt; y); already gives the boolean, so the ? : is unnecessary.
- **misconception** (wrong rule / right rule; shows `ArithmeticInsteadOfBoolean`): wrong rule: A true/false question is answered with arithmetic (e.g. 1 for true). Right rule: A logic question is written as a boolean expression whose value is true or false, e.g. (year % 4 == 0).
- **inconsistent trace** (uneven-application rule; shows `ComparisonWithBooleanLiteral`): Points to LT (arithmetic first, then comparisons, then !, &amp;&amp;, \|\|, left to right, with short-circuit). Applied unevenly: the student evaluates &amp;&amp; before a comparison in one sub-expression, or evaluates the right operand of &amp;&amp; on a pass where the left was already false. (here mixing in: "you must write == true / == false to test a boolean")
- **misconception** (wrong rule / right rule; shows `ChainedComparison`): wrong rule: 90 &lt;= grade &lt;= 100 tests whether grade is between 90 and 100. Right rule: a &lt; b &lt; c does not compile (a &lt; b is a boolean, which cannot be compared with &lt;); a range test is written 90 &lt;= grade &amp;&amp; grade &lt;= 100.
- **misconception** (wrong rule / right rule; shows `LoopForOneTimeTest`): wrong rule: Uses a loop where a condition needs to be tested only once. Right rule: A test made once is an if; a while re-tests its condition and repeats its body for as long as the condition is true.
- **misconception** (wrong rule / right rule; shows `NestedIfsInsteadOfLogicalOperators`): wrong rule: A condition on several values has to be written as nested if statements, one value per if. Right rule: Several conditions combine into one boolean expression with &amp;&amp; and \|\|, e.g. if (x == 0 &amp;&amp; y == 0).

### L1: Unistructural / atom x text surface

L1 for boolean expression: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

boolean expression -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

- **names the element** (identity rule): A boolean expression is any expression whose type is boolean: a boolean literal or variable, a comparison, or such parts combined with &amp;&amp;, \|\| and !.
- **states the rule** (declarative rule): A boolean expression has value true or false; it is built from comparisons (lower precedence than arithmetic, higher than boolean operators) and boolean operators; the condition of if, while and for must be one.

### L2: Multistructural / block x execution / preoperational

L2 for boolean expression: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

boolean expression -&gt; L2 (Multistructural): the answer applies the rules of boolean expression to every part of the code, in order (3 ways).

- **line by line trace** (operational sequencing rule): Operands are evaluated left to right; arithmetic sub-expressions first, then comparisons, then !, then &amp;&amp;, then \|\|; &amp;&amp; and \|\| evaluate their right operand only when the left has not decided the result.
- **output prediction** (evaluation / result rule): The value is true or false: with year = 1900, (year % 4 == 0) &amp;&amp; (year % 100 != 0) \|\| (year % 400 == 0) is false, so LeapYear prints false.
- **one step execution** (state-transition rule): Evaluating a boolean expression changes no variable (unless it contains an assignment, ++ or a method with side effects); state changes only when its value is stored, as in isLeapYear = isLeapYear &amp;&amp; (year % 100 != 0);.

### L3: Relational / relations x function (concrete operational begins)

L3 for boolean expression: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

boolean expression -&gt; L3 (Relational): the answer relates the parts (7 ways).

- **relation to neighbour** (composition rule (with a neighbour)): Comparisons are the atoms of boolean expressions; because they bind tighter than &amp;&amp; and \|\|, month &gt;= 1 &amp;&amp; month &lt;= 12 groups as (month &gt;= 1) &amp;&amp; (month &lt;= 12) without parentheses.
- **relation to neighbour** (composition rule (with a neighbour)): &amp;&amp;, \|\| and ! combine boolean sub-expressions into a larger one; ! binds tighter than comparisons, so negating a comparison needs parentheses: !(x &gt; 0).
- **relation to neighbour** (composition rule (with a neighbour)): The if statement evaluates its boolean expression once and runs its block only when the value is true; the expression must have type boolean, so if (x = 5) with int x does not compile.
- **relation to neighbour** (composition rule (with a neighbour)): The while loop re-evaluates its boolean expression before every pass and stops the first time it is false, so some variable in the expression must change in the body or the loop never ends.
- **relation to neighbour** (composition rule (with a neighbour)): In RandomSurfer the boolean expression r &lt; sum is evaluated for each candidate page j in turn, as sum grows; the first j for which it is true is the chosen page.
- **relation to neighbour** (composition rule (with a neighbour)): In the template if (&lt;boolean expression&gt;) { &lt;statements&gt; } the placeholder may be filled by any boolean-typed expression: a literal, a boolean variable, a comparison or a combination with logical operators.
- **purpose of the whole** (plan / role rule): Expresses a decision condition or guard (which branch runs, whether a loop continues) or computes a flag; common plans: range test lo &lt;= x &amp;&amp; x &lt;= hi, divisibility test n % k == 0, combined rule as in LeapYear.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for boolean expression: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

boolean expression -&gt; L4 (Extended abstract): the answer reasons beyond the given code (5 ways).

- **predict a change** (conservation rule; shows `ComparisonWithBooleanLiteral`): Rewriting with De Morgan (!(a &amp;&amp; b) as !a \|\| !b) keeps the value for every input; swapping the operands of &amp;&amp; keeps the truth value but can change whether the right operand is evaluated (and whether a guard still protects it); changing &lt; to &lt;= changes the result only at the boundary value.
- **diagnose an error** (error rule): rule broken: else takes no condition; a second condition needs else if (...). Kind: compile-time. Trigger class: Writing else (x &gt; 0) { ... } after an if block (the compiler reports e.g. 'not a statement' or '; expected').
- **transfer to a new program** (applicability rule): Use a boolean expression wherever code must decide or record a yes/no condition, and store it directly (ok = x &gt; y) rather than via if or ? :; when different outcomes are needed for several cases use an if-else chain of such expressions.
- **diagnose an error** (error rule): rule broken: The condition must be a boolean expression; = assigns, == compares. Kind: compile-time. Trigger class: if (a = b) with int a and b (with boolean variables it compiles and silently assigns).
- **diagnose an error** (error rule): rule broken: Comparisons cannot be chained; each must be joined with &amp;&amp; or \|\|. Kind: compile-time. Trigger class: Range written as a &lt; b &lt; c or 90 &lt;= grade &lt;= 100.

## Same topic

`boolean_expression` belongs to the topic **Booleans** (`topic1.2.e`). The topic also contains: `boolean`, `de_morgan`, `exclusive_or`, `logical_operators`, `short_circuit`.

## Rules of the concept (26)

- **folk-meaning rule:** Folk meaning: maths writes a range as 90 &lt;= grade &lt;= 100 and English says 'if x is 1 or 2'. Java rule: each comparison is a separate boolean expression and they must be joined explicitly: 90 &lt;= grade &amp;&amp; grade &lt;= 100, x == 1 \|\| x == 2; 90 &lt;= grade &lt;= 100 does not compile because 90 &lt;= grade is already a boolean.
- **wrong rule / right rule:** ArithmeticInsteadOfBoolean: wrong: A true/false question is answered with arithmetic (e.g. 1 for true). \| right: A logic question is written as a boolean expression whose value is true or false, e.g. (year % 4 == 0).
- **wrong rule / right rule:** ChainedComparison: wrong: 90 &lt;= grade &lt;= 100 tests whether grade is between 90 and 100. \| right: a &lt; b &lt; c does not compile (a &lt; b is a boolean, which cannot be compared with &lt;); a range test is written 90 &lt;= grade &amp;&amp; grade &lt;= 100.
- **wrong rule / right rule:** ComparisonWithBooleanLiteral: wrong: You must write == true / == false to test a boolean. \| right: if (b) already tests b, and if (!b) tests that it is false, so == true adds nothing.
- **wrong rule / right rule:** LoopForOneTimeTest: wrong: Uses a loop where a condition needs to be tested only once. \| right: A test made once is an if; a while re-tests its condition and repeats its body for as long as the condition is true.
- **wrong rule / right rule:** MapToBooleanWithConditionalOperator: wrong: You need ? : to turn a boolean expression into a boolean (ok = x &gt; y ? true : false). \| right: ok = (x &gt; y); already gives the boolean, so the ? : is unnecessary.
- **wrong rule / right rule:** MapToBooleanWithIf: wrong: You need an if to turn a boolean expression into a boolean. \| right: ok = (x &gt; y); stores the result of the comparison directly.
- **wrong rule / right rule:** NestedIfsInsteadOfLogicalOperators: wrong: A condition on several values has to be written as nested if statements, one value per if. \| right: Several conditions combine into one boolean expression with &amp;&amp; and \|\|, e.g. if (x == 0 &amp;&amp; y == 0).
- **uneven-application rule:** Points to LT (arithmetic first, then comparisons, then !, &amp;&amp;, \|\|, left to right, with short-circuit). Applied unevenly: the student evaluates &amp;&amp; before a comparison in one sub-expression, or evaluates the right operand of &amp;&amp; on a pass where the left was already false.
- **identity rule:** A boolean expression is any expression whose type is boolean: a boolean literal or variable, a comparison, or such parts combined with &amp;&amp;, \|\| and !.
- **declarative rule:** A boolean expression has value true or false; it is built from comparisons (lower precedence than arithmetic, higher than boolean operators) and boolean operators; the condition of if, while and for must be one.
- **operational sequencing rule:** Operands are evaluated left to right; arithmetic sub-expressions first, then comparisons, then !, then &amp;&amp;, then \|\|; &amp;&amp; and \|\| evaluate their right operand only when the left has not decided the result.
- **evaluation / result rule:** The value is true or false: with year = 1900, (year % 4 == 0) &amp;&amp; (year % 100 != 0) \|\| (year % 400 == 0) is false, so LeapYear prints false.
- **state-transition rule:** Evaluating a boolean expression changes no variable (unless it contains an assignment, ++ or a method with side effects); state changes only when its value is stored, as in isLeapYear = isLeapYear &amp;&amp; (year % 100 != 0);.
- **composition rule (with a neighbour):** with comparison\_operators: Comparisons are the atoms of boolean expressions; because they bind tighter than &amp;&amp; and \|\|, month &gt;= 1 &amp;&amp; month &lt;= 12 groups as (month &gt;= 1) &amp;&amp; (month &lt;= 12) without parentheses.
- **composition rule (with a neighbour):** with logical\_operators: &amp;&amp;, \|\| and ! combine boolean sub-expressions into a larger one; ! binds tighter than comparisons, so negating a comparison needs parentheses: !(x &gt; 0).
- **composition rule (with a neighbour):** with if\_statement: The if statement evaluates its boolean expression once and runs its block only when the value is true; the expression must have type boolean, so if (x = 5) with int x does not compile.
- **composition rule (with a neighbour):** with while\_loop: The while loop re-evaluates its boolean expression before every pass and stops the first time it is false, so some variable in the expression must change in the body or the loop never ends.
- **composition rule (with a neighbour):** with random\_move: In RandomSurfer the boolean expression r &lt; sum is evaluated for each candidate page j in turn, as sum grows; the first j for which it is true is the chosen page.
- **composition rule (with a neighbour):** with syntax\_template: In the template if (&lt;boolean expression&gt;) { &lt;statements&gt; } the placeholder may be filled by any boolean-typed expression: a literal, a boolean variable, a comparison or a combination with logical operators.
- **plan / role rule:** Expresses a decision condition or guard (which branch runs, whether a loop continues) or computes a flag; common plans: range test lo &lt;= x &amp;&amp; x &lt;= hi, divisibility test n % k == 0, combined rule as in LeapYear.
- **conservation rule:** Rewriting with De Morgan (!(a &amp;&amp; b) as !a \|\| !b) keeps the value for every input; swapping the operands of &amp;&amp; keeps the truth value but can change whether the right operand is evaluated (and whether a guard still protects it); changing &lt; to &lt;= changes the result only at the boundary value.
- **error rule:** rule broken: else takes no condition; a second condition needs else if (...). (compile-time)
- **error rule:** rule broken: The condition must be a boolean expression; = assigns, == compares. (compile-time)
- **error rule:** rule broken: Comparisons cannot be chained; each must be joined with &amp;&amp; or \|\|. (compile-time)
- **applicability rule:** Use a boolean expression wherever code must decide or record a yes/no condition, and store it directly (ok = x &gt; y) rather than via if or ? :; when different outcomes are needed for several cases use an if-else chain of such expressions.

## The whole prerequisite chain

- **Everything it builds on (10):** `arithmetic_operators`, `boolean`, `comparison_operators`, `data_type`, `expression`, `identifier`, `literal`, `logical_operators`, `primitive_type`, `variable`
- **Everything that builds on it (51):** `accumulator_pattern`, `animation`, `array_copy`, `array_reversal`, `array_traversal`, `boolean_flag_array`, `break_statement`, `conditional_operator`, `continue_statement`, `convergence_rate`, `convergence_test`, `counter_pattern`, `dangling_else`, `do_while_loop`, `else_if_chain`, `enhanced_for`, `fencepost_loop`, `flag_search_loop`, `for_loop`, `frequency_counting`, `function_plotting`, `if_else_statement`, `if_statement`, `increment_operators`, `infinite_loop`, `labeled_break`, `loop_body`, `loop_control`, `loop_invariant_reasoning`, `loop_performance`, `loop_scope`, `loop_variable`, `matrix_operations`, `monte_carlo_simulation`, `mouse_interaction`, `nested_conditionals`, `nested_loops`, `number_conversion`, `off_by_one_error`, `power_method`, `random_move`, `row_major_order`, `running_extreme`, `sentinel_loop`, `side_effect_order`, `simulation_loop`, `standard_audio`, `switch_statement`, `syntax_template`, `two_models`, `while_loop`
