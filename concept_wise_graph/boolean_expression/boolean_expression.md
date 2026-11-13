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

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 35 edges around this concept. The edge logic, the wrong and right rules and the exact rules of the ways are copied word for word from the graph.

## To work on (0)

Nothing is missing for this concept.

## What it needs first (2)

A prerequisite edge means the other concept has to be understood before `boolean_expression`.

### `comparison_operators` comes before `boolean_expression`

*== != &lt; &gt; &lt;= &gt;=*

- **Edge:** `pre:comparison_operators->boolean_expression`
- **Exact edge logic:** A comparison such as x &lt; y produces a boolean result; comparisons together with boolean logic provide the basis for decision-making.
- **Grounding:** book\_passage
- **Composition rule (R) of `boolean_expression` with `comparison_operators`:** Comparisons are the atoms of boolean expressions; because they bind tighter than &amp;&amp; and \|\|, month &gt;= 1 &amp;&amp; month &lt;= 12 groups as (month &gt;= 1) &amp;&amp; (month &lt;= 12) without parentheses.
- **Composition rule (R) of `comparison_operators` with `boolean_expression`:** Comparisons are the building blocks of conditions: together with boolean logic they provide the basis for decision-making.

### `logical_operators` comes before `boolean_expression`

*&amp;&amp; \|\| !*

- **Edge:** `pre:logical_operators->boolean_expression`
- **Exact edge logic:** &amp;&amp;, \|\| and ! combine conditions p and q into one larger condition that is still true or false.
- **Grounding:** book\_passage
- **Composition rule (R) of `boolean_expression` with `logical_operators`:** &amp;&amp;, \|\| and ! combine boolean sub-expressions into a larger one; ! binds tighter than comparisons, so negating a comparison needs parentheses: !(x &gt; 0).
- **Composition rule (R) of `logical_operators` with `boolean_expression`:** Combining boolean sub-expressions with &amp;&amp;, \|\| and ! yields another boolean expression, so arbitrarily complex conditions can be built with parentheses.

## What it leads to (4)

These concepts need `boolean_expression` first.

### `boolean_expression` comes before `if_statement`

*run a block only when the condition holds*

- **Edge:** `pre:boolean_expression->if_statement`
- **Exact edge logic:** An if runs its block only when its boolean expression evaluates to true.
- **Grounding:** book\_passage
- **Composition rule (R) of `boolean_expression` with `if_statement`:** The if statement evaluates its boolean expression once and runs its block only when the value is true; the expression must have type boolean, so if (x = 5) with int x does not compile.
- **Composition rule (R) of `if_statement` with `boolean_expression`:** The condition must be a boolean expression; a non-boolean condition such as if (t = goal) with int t is a compile-time error, while if (b = false) with boolean b compiles and assigns.

### `boolean_expression` comes before `random_move`

*pick the next page from a cumulative-probability test*

- **Edge:** `pre:boolean_expression->random_move`
- **Exact edge logic:** The next page is chosen by testing the condition r &lt; sum for each candidate page j in turn.
- **Grounding:** book\_passage
- **Composition rule (R) of `boolean_expression` with `random_move`:** In RandomSurfer the boolean expression r &lt; sum is evaluated for each candidate page j in turn, as sum grows; the first j for which it is true is the chosen page.
- **Composition rule (R) of `random_move` with `boolean_expression`:** The relational test r &lt; sum decides both the chosen page and the early break; &lt; (not &lt;=) matches the half-open interval endpoint tracked by sum.

### `boolean_expression` comes before `syntax_template`

*Template notation: the book's notation for a construct: a name in angle brackets, such as &lt;boolean expression&gt;, stands for any instance of that construct*

- **Edge:** `pre:boolean_expression->syntax_template`
- **Exact edge logic:** In the template if (&lt;boolean expression&gt;) { &lt;statements&gt; }, &lt;boolean expression&gt; stands for any expression of type boolean.
- **Grounding:** book\_passage
- **Composition rule (R) of `boolean_expression` with `syntax_template`:** In the template if (&lt;boolean expression&gt;) { &lt;statements&gt; } the placeholder may be filled by any boolean-typed expression: a literal, a boolean variable, a comparison or a combination with logical operators.
- **Composition rule (R) of `syntax_template` with `boolean_expression`:** The \`&lt;boolean expression&gt;\` slot accepts only expressions of type boolean (\`x &gt; y\`, \`found\`, \`a &amp;&amp; b\`). An int expression or an assignment such as \`x = y\` with int x is a compile error in that slot.

### `boolean_expression` comes before `while_loop`

*repeat a block while a condition holds*

- **Edge:** `pre:boolean_expression->while_loop`
- **Exact edge logic:** A while tests its boolean condition before every pass and stops the first time it evaluates to false.
- **Grounding:** book\_passage
- **Composition rule (R) of `boolean_expression` with `while_loop`:** The while loop re-evaluates its boolean expression before every pass and stops the first time it is false, so some variable in the expression must change in the body or the loop never ends.
- **Composition rule (R) of `while_loop` with `boolean_expression`:** The loop condition is a boolean expression evaluated before every pass; the loop stops the first time it is false, so the body must eventually make it false.

## Learned alongside (0)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

No parallel edge touches this concept.

## Misconceptions (7)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### ArithmeticInsteadOfBoolean

- **Edge:** `boolean_expression` &rarr; `ArithmeticInsteadOfBoolean` (misconception)
- **Exact edge logic (the wrong rule):** A true/false question is answered with arithmetic (e.g. 1 for true).
- **Twin logic (the right rule):** A logic question is written as a boolean expression whose value is true or false.
- **Wrong belief (on the node):** A true/false question is answered with arithmetic (e.g. 1 for true).
- **Correct rule (on the node):** A logic question is written as a boolean expression whose value is true or false.
- **Provenance:** published
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [4] misconception, exact rule:** wrong rule: A true/false question is answered with arithmetic (e.g. 1 for true). Right rule: A logic question is written as a boolean expression whose value is true or false, e.g. (year % 4 == 0).
- **Edge `boolean` &rarr; `ArithmeticInsteadOfBoolean`, exact edge logic:** A true/false question is answered with arithmetic (e.g. 1 for true). **Twin logic:** A logic question is written as a boolean expression whose value is true or false. (role: primary)

### ChainedComparison

- **Edge:** `boolean_expression` &rarr; `ChainedComparison` (misconception)
- **Exact edge logic (the wrong rule):** 90 &lt;= grade &lt;= 100 tests whether grade is between 90 and 100.
- **Twin logic (the right rule):** a &lt; b &lt; c does not compile (a &lt; b is a boolean); a range test is written 90 &lt;= grade &amp;&amp; grade &lt;= 100.
- **Wrong belief (on the node):** 90 &lt;= grade &lt;= 100 tests whether grade is between 90 and 100.
- **Correct rule (on the node):** a &lt; b &lt; c does not compile (a &lt; b is a boolean); a range test is written 90 &lt;= grade &amp;&amp; grade &lt;= 100.
- **Provenance:** textbook
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [6] misconception, exact rule:** wrong rule: 90 &lt;= grade &lt;= 100 tests whether grade is between 90 and 100. Right rule: a &lt; b &lt; c does not compile (a &lt; b is a boolean, which cannot be compared with &lt;); a range test is written 90 &lt;= grade &amp;&amp; grade &lt;= 100.
- **Edge `comparison_operators` &rarr; `ChainedComparison`, exact edge logic:** 90 &lt;= grade &lt;= 100 tests whether grade is between 90 and 100. **Twin logic:** a &lt; b &lt; c does not compile (a &lt; b is a boolean); a range test is written 90 &lt;= grade &amp;&amp; grade &lt;= 100. (role: primary)

### ComparisonWithBooleanLiteral

- **Edge:** `boolean_expression` &rarr; `ComparisonWithBooleanLiteral` (misconception)
- **Exact edge logic (the wrong rule):** To test a boolean b you must write if (b == true).
- **Twin logic (the right rule):** if (b) already tests b, so writing == true adds nothing.
- **Wrong belief (on the node):** you must write == true / == false to test a boolean
- **Correct rule (on the node):** if (b) already tests b, so writing == true adds nothing.
- **Provenance:** published
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [1] misconception, exact rule:** wrong rule: You must write == true / == false to test a boolean. Right rule: if (b) already tests b, and if (!b) tests that it is false, so == true adds nothing.
- **L0 way [5] inconsistent\_trace, exact rule:** Points to LT (arithmetic first, then comparisons, then !, &amp;&amp;, \|\|, left to right, with short-circuit). Applied unevenly: the student evaluates &amp;&amp; before a comparison in one sub-expression, or evaluates the right operand of &amp;&amp; on a pass where the left was already false. (here mixing in: "you must write == true / == false to test a boolean")
- **Edge `comparison_operators` &rarr; `ComparisonWithBooleanLiteral`, exact edge logic:** you must write == true / == false to test a boolean **Twin logic:** if (b) already tests b, so writing == true adds nothing. (role: context)

### LoopForOneTimeTest

- **Edge:** `boolean_expression` &rarr; `LoopForOneTimeTest` (misconception)
- **Exact edge logic (the wrong rule):** Uses a loop where a condition needs to be tested only once.
- **Twin logic (the right rule):** A test made once is an if; a loop repeats.
- **Wrong belief (on the node):** Uses a loop where a condition needs to be tested only once.
- **Correct rule (on the node):** A test made once is an if; a loop repeats.
- **Provenance:** published
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [7] misconception, exact rule:** wrong rule: Uses a loop where a condition needs to be tested only once. Right rule: A test made once is an if; a while re-tests its condition and repeats its body for as long as the condition is true.
- **Edge `if_statement` &rarr; `LoopForOneTimeTest`, exact edge logic:** Uses a loop where a condition needs to be tested only once. **Twin logic:** A test made once is an if; a loop repeats. (role: context)
- **Edge `while_loop` &rarr; `LoopForOneTimeTest`, exact edge logic:** Uses a loop where a condition needs to be tested only once. **Twin logic:** A test made once is an if; a loop repeats. (role: primary)

### MapToBooleanWithConditionalOperator

- **Edge:** `boolean_expression` &rarr; `MapToBooleanWithConditionalOperator` (misconception)
- **Exact edge logic (the wrong rule):** To get a boolean from x &gt; y you need ok = (x &gt; y) ? true : false;.
- **Twin logic (the right rule):** ok = (x &gt; y); already gives the boolean, so the ? : is unnecessary.
- **Wrong belief (on the node):** you need ? : to do the same
- **Correct rule (on the node):** ok = (x &gt; y); already gives the boolean, so the ? : is unnecessary.
- **Provenance:** published
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [3] misconception, exact rule:** wrong rule: You need ? : to turn a boolean expression into a boolean (ok = x &gt; y ? true : false). Right rule: ok = (x &gt; y); already gives the boolean, so the ? : is unnecessary.
- **Edge `conditional_operator` &rarr; `MapToBooleanWithConditionalOperator`, exact edge logic:** you need ? : to do the same **Twin logic:** ok = (x &gt; y); already gives the boolean, so the ? : is unnecessary. (role: context)

### MapToBooleanWithIf

- **Edge:** `boolean_expression` &rarr; `MapToBooleanWithIf` (misconception)
- **Exact edge logic (the wrong rule):** To store whether x &gt; y in a boolean you need if (x &gt; y) ok = true; else ok = false;.
- **Twin logic (the right rule):** ok = (x &gt; y); stores the result of the comparison directly.
- **Wrong belief (on the node):** you need an if to turn a boolean expression into a boolean
- **Correct rule (on the node):** ok = (x &gt; y); stores the result of the comparison directly.
- **Provenance:** published
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [2] misconception, exact rule:** wrong rule: You need an if to turn a boolean expression into a boolean. Right rule: ok = (x &gt; y); stores the result of the comparison directly.
- **Edge `if_statement` &rarr; `MapToBooleanWithIf`, exact edge logic:** you need an if to turn a boolean expression into a boolean **Twin logic:** ok = (x &gt; y); stores the result of the comparison directly. (role: context)

### NestedIfsInsteadOfLogicalOperators

- **Edge:** `boolean_expression` &rarr; `NestedIfsInsteadOfLogicalOperators` (misconception)
- **Exact edge logic (the wrong rule):** A condition on several values has to be written as nested if statements, one value per if.
- **Twin logic (the right rule):** Several conditions combine into one boolean expression with &amp;&amp; and \|\|, e.g. if (x == 0 &amp;&amp; y == 0).
- **Wrong belief (on the node):** A condition on several values has to be written as nested if statements, one value per if.
- **Correct rule (on the node):** Several conditions combine into one boolean expression with &amp;&amp; and \|\|, e.g. if (x == 0 &amp;&amp; y == 0).
- **Provenance:** published
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [8] misconception, exact rule:** wrong rule: A condition on several values has to be written as nested if statements, one value per if. Right rule: Several conditions combine into one boolean expression with &amp;&amp; and \|\|, e.g. if (x == 0 &amp;&amp; y == 0).
- **Edge `logical_operators` &rarr; `NestedIfsInsteadOfLogicalOperators`, exact edge logic:** A condition on several values has to be written as nested if statements, one value per if. **Twin logic:** Several conditions combine into one boolean expression with &amp;&amp; and \|\|, e.g. if (x == 0 &amp;&amp; y == 0). (role: primary)
- **Edge `nested_conditionals` &rarr; `NestedIfsInsteadOfLogicalOperators`, exact edge logic:** A condition on several values has to be written as nested if statements, one value per if. **Twin logic:** Several conditions combine into one boolean expression with &amp;&amp; and \|\|, e.g. if (x == 0 &amp;&amp; y == 0). (role: context)

## Errors (1)

An error edge states the rule that gets broken in a program, and the right rule.

### ElseWithCondition

- **Edge:** `boolean_expression` &rarr; `ElseWithCondition` (error)
- **Exact edge logic (the wrong rule):** Writes else (x &gt; 0) with a condition but no if.
- **Twin logic (the right rule):** else takes no condition; use else if (x &gt; 0).
- **Wrong belief (on the node):** Writes else (x &gt; 0) with a condition but no if.
- **Correct rule (on the node):** else takes no condition; use else if (x &gt; 0).
- **Provenance:** published
- **Role of this concept:** context
- **Edge `if_else_statement` &rarr; `ElseWithCondition`, exact edge logic:** Writes else (x &gt; 0) with a condition but no if. **Twin logic:** else takes no condition; use else if (x &gt; 0). (role: primary)

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for boolean expression: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to boolean expression agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

- **Edge:** `boolean_expression` &rarr; `boolean_expression@L0` (has_level)
- **Exact edge logic:** boolean expression -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (9 ways).

Ways (9), each with its exact rule:

- **[0] everyday\_reading** (rule type E, folk-meaning rule): Folk meaning: maths writes a range as 90 &lt;= grade &lt;= 100 and English says 'if x is 1 or 2'. Java rule: each comparison is a separate boolean expression and they must be joined explicitly: 90 &lt;= grade &amp;&amp; grade &lt;= 100, x == 1 \|\| x == 2; 90 &lt;= grade &lt;= 100 does not compile because 90 &lt;= grade is already a boolean.
- **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `ComparisonWithBooleanLiteral`: wrong rule: You must write == true / == false to test a boolean. Right rule: if (b) already tests b, and if (!b) tests that it is false, so == true adds nothing.
- **[2] misconception** (rule type M, wrong rule / right rule) &rarr; `MapToBooleanWithIf`: wrong rule: You need an if to turn a boolean expression into a boolean. Right rule: ok = (x &gt; y); stores the result of the comparison directly.
- **[3] misconception** (rule type M, wrong rule / right rule) &rarr; `MapToBooleanWithConditionalOperator`: wrong rule: You need ? : to turn a boolean expression into a boolean (ok = x &gt; y ? true : false). Right rule: ok = (x &gt; y); already gives the boolean, so the ? : is unnecessary.
- **[4] misconception** (rule type M, wrong rule / right rule) &rarr; `ArithmeticInsteadOfBoolean`: wrong rule: A true/false question is answered with arithmetic (e.g. 1 for true). Right rule: A logic question is written as a boolean expression whose value is true or false, e.g. (year % 4 == 0).
- **[5] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `ComparisonWithBooleanLiteral`: Points to LT (arithmetic first, then comparisons, then !, &amp;&amp;, \|\|, left to right, with short-circuit). Applied unevenly: the student evaluates &amp;&amp; before a comparison in one sub-expression, or evaluates the right operand of &amp;&amp; on a pass where the left was already false. (here mixing in: "you must write == true / == false to test a boolean")
- **[6] misconception** (rule type M, wrong rule / right rule) &rarr; `ChainedComparison`: wrong rule: 90 &lt;= grade &lt;= 100 tests whether grade is between 90 and 100. Right rule: a &lt; b &lt; c does not compile (a &lt; b is a boolean, which cannot be compared with &lt;); a range test is written 90 &lt;= grade &amp;&amp; grade &lt;= 100.
- **[7] misconception** (rule type M, wrong rule / right rule) &rarr; `LoopForOneTimeTest`: wrong rule: Uses a loop where a condition needs to be tested only once. Right rule: A test made once is an if; a while re-tests its condition and repeats its body for as long as the condition is true.
- **[8] misconception** (rule type M, wrong rule / right rule) &rarr; `NestedIfsInsteadOfLogicalOperators`: wrong rule: A condition on several values has to be written as nested if statements, one value per if. Right rule: Several conditions combine into one boolean expression with &amp;&amp; and \|\|, e.g. if (x == 0 &amp;&amp; y == 0).

### L1: Unistructural / atom x text surface

L1 for boolean expression: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

- **Edge:** `boolean_expression` &rarr; `boolean_expression@L1` (has_level)
- **Exact edge logic:** boolean expression -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

Ways (2), each with its exact rule:

- **[0] names\_the\_element** (rule type N, identity rule): A boolean expression is any expression whose type is boolean: a boolean literal or variable, a comparison, or such parts combined with &amp;&amp;, \|\| and !.
- **[1] states\_the\_rule** (rule type S, declarative rule): A boolean expression has value true or false; it is built from comparisons (lower precedence than arithmetic, higher than boolean operators) and boolean operators; the condition of if, while and for must be one.

### L2: Multistructural / block x execution / preoperational

L2 for boolean expression: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

- **Edge:** `boolean_expression` &rarr; `boolean_expression@L2` (has_level)
- **Exact edge logic:** boolean expression -&gt; L2 (Multistructural): the answer applies the rules of boolean expression to every part of the code, in order (3 ways).

Ways (3), each with its exact rule:

- **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): Operands are evaluated left to right; arithmetic sub-expressions first, then comparisons, then !, then &amp;&amp;, then \|\|; &amp;&amp; and \|\| evaluate their right operand only when the left has not decided the result.
- **[1] output\_prediction** (rule type OP, evaluation / result rule): The value is true or false: with year = 1900, (year % 4 == 0) &amp;&amp; (year % 100 != 0) \|\| (year % 400 == 0) is false, so LeapYear prints false.
- **[2] one\_step\_execution** (rule type OS, state-transition rule): Evaluating a boolean expression changes no variable (unless it contains an assignment, ++ or a method with side effects); state changes only when its value is stored, as in isLeapYear = isLeapYear &amp;&amp; (year % 100 != 0);.

### L3: Relational / relations x function (concrete operational begins)

L3 for boolean expression: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

- **Edge:** `boolean_expression` &rarr; `boolean_expression@L3` (has_level)
- **Exact edge logic:** boolean expression -&gt; L3 (Relational): the answer relates the parts (7 ways).

Ways (7), each with its exact rule:

- **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Comparisons are the atoms of boolean expressions; because they bind tighter than &amp;&amp; and \|\|, month &gt;= 1 &amp;&amp; month &lt;= 12 groups as (month &gt;= 1) &amp;&amp; (month &lt;= 12) without parentheses.
- **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): &amp;&amp;, \|\| and ! combine boolean sub-expressions into a larger one; ! binds tighter than comparisons, so negating a comparison needs parentheses: !(x &gt; 0).
- **[2] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): The if statement evaluates its boolean expression once and runs its block only when the value is true; the expression must have type boolean, so if (x = 5) with int x does not compile.
- **[3] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): The while loop re-evaluates its boolean expression before every pass and stops the first time it is false, so some variable in the expression must change in the body or the loop never ends.
- **[4] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): In RandomSurfer the boolean expression r &lt; sum is evaluated for each candidate page j in turn, as sum grows; the first j for which it is true is the chosen page.
- **[5] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): In the template if (&lt;boolean expression&gt;) { &lt;statements&gt; } the placeholder may be filled by any boolean-typed expression: a literal, a boolean variable, a comparison or a combination with logical operators.
- **[6] purpose\_of\_the\_whole** (rule type P, plan / role rule): Expresses a decision condition or guard (which branch runs, whether a loop continues) or computes a flag; common plans: range test lo &lt;= x &amp;&amp; x &lt;= hi, divisibility test n % k == 0, combined rule as in LeapYear.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for boolean expression: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

- **Edge:** `boolean_expression` &rarr; `boolean_expression@L4` (has_level)
- **Exact edge logic:** boolean expression -&gt; L4 (Extended abstract): the answer reasons beyond the given code (5 ways).

Ways (5), each with its exact rule:

- **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `ComparisonWithBooleanLiteral`: Rewriting with De Morgan (!(a &amp;&amp; b) as !a \|\| !b) keeps the value for every input; swapping the operands of &amp;&amp; keeps the truth value but can change whether the right operand is evaluated (and whether a guard still protects it); changing &lt; to &lt;= changes the result only at the boundary value.
- **[1] diagnose\_an\_error** (rule type D, error rule): rule broken: else takes no condition; a second condition needs else if (...). Kind: compile-time. Trigger class: Writing else (x &gt; 0) { ... } after an if block (the compiler reports e.g. 'not a statement' or '; expected').
- **[2] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Use a boolean expression wherever code must decide or record a yes/no condition, and store it directly (ok = x &gt; y) rather than via if or ? :; when different outcomes are needed for several cases use an if-else chain of such expressions.
- **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: The condition must be a boolean expression; = assigns, == compares. Kind: compile-time. Trigger class: if (a = b) with int a and b (with boolean variables it compiles and silently assigns).
- **[4] diagnose\_an\_error** (rule type D, error rule): rule broken: Comparisons cannot be chained; each must be joined with &amp;&amp; or \|\|. Kind: compile-time. Trigger class: Range written as a &lt; b &lt; c or 90 &lt;= grade &lt;= 100.

## Same topic

`boolean_expression` belongs to the topic **Booleans** (`topic1.2.e`). The topic also contains: `boolean`, `de_morgan`, `exclusive_or`, `logical_operators`, `short_circuit`.

## Rules of the concept (26)

- **Book** (SW-1e, p. 28 (pdf 38)): "Comparison operations, together with boolean logic, provide the basis for decision-making in Java programs."
- **Book** (SW-1.2, ): "The comparison operators are mixed-type operations that take operands of one type and produce a result of type boolean."
- **E** (folk-meaning rule): Folk meaning: maths writes a range as 90 &lt;= grade &lt;= 100 and English says 'if x is 1 or 2'. Java rule: each comparison is a separate boolean expression and they must be joined explicitly: 90 &lt;= grade &amp;&amp; grade &lt;= 100, x == 1 \|\| x == 2; 90 &lt;= grade &lt;= 100 does not compile because 90 &lt;= grade is already a boolean.
- **M** (wrong rule / right rule): ArithmeticInsteadOfBoolean: wrong: A true/false question is answered with arithmetic (e.g. 1 for true). \| right: A logic question is written as a boolean expression whose value is true or false, e.g. (year % 4 == 0).
- **M** (wrong rule / right rule): ChainedComparison: wrong: 90 &lt;= grade &lt;= 100 tests whether grade is between 90 and 100. \| right: a &lt; b &lt; c does not compile (a &lt; b is a boolean, which cannot be compared with &lt;); a range test is written 90 &lt;= grade &amp;&amp; grade &lt;= 100.
- **M** (wrong rule / right rule): ComparisonWithBooleanLiteral: wrong: You must write == true / == false to test a boolean. \| right: if (b) already tests b, and if (!b) tests that it is false, so == true adds nothing.
- **M** (wrong rule / right rule): LoopForOneTimeTest: wrong: Uses a loop where a condition needs to be tested only once. \| right: A test made once is an if; a while re-tests its condition and repeats its body for as long as the condition is true.
- **M** (wrong rule / right rule): MapToBooleanWithConditionalOperator: wrong: You need ? : to turn a boolean expression into a boolean (ok = x &gt; y ? true : false). \| right: ok = (x &gt; y); already gives the boolean, so the ? : is unnecessary.
- **M** (wrong rule / right rule): MapToBooleanWithIf: wrong: You need an if to turn a boolean expression into a boolean. \| right: ok = (x &gt; y); stores the result of the comparison directly.
- **M** (wrong rule / right rule): NestedIfsInsteadOfLogicalOperators: wrong: A condition on several values has to be written as nested if statements, one value per if. \| right: Several conditions combine into one boolean expression with &amp;&amp; and \|\|, e.g. if (x == 0 &amp;&amp; y == 0).
- **T** (uneven-application rule): Points to LT (arithmetic first, then comparisons, then !, &amp;&amp;, \|\|, left to right, with short-circuit). Applied unevenly: the student evaluates &amp;&amp; before a comparison in one sub-expression, or evaluates the right operand of &amp;&amp; on a pass where the left was already false.
- **N** (identity rule): A boolean expression is any expression whose type is boolean: a boolean literal or variable, a comparison, or such parts combined with &amp;&amp;, \|\| and !.
- **S** (declarative rule): A boolean expression has value true or false; it is built from comparisons (lower precedence than arithmetic, higher than boolean operators) and boolean operators; the condition of if, while and for must be one.
- **LT** (operational sequencing rule): Operands are evaluated left to right; arithmetic sub-expressions first, then comparisons, then !, then &amp;&amp;, then \|\|; &amp;&amp; and \|\| evaluate their right operand only when the left has not decided the result.
- **OP** (evaluation / result rule): The value is true or false: with year = 1900, (year % 4 == 0) &amp;&amp; (year % 100 != 0) \|\| (year % 400 == 0) is false, so LeapYear prints false.
- **OS** (state-transition rule): Evaluating a boolean expression changes no variable (unless it contains an assignment, ++ or a method with side effects); state changes only when its value is stored, as in isLeapYear = isLeapYear &amp;&amp; (year % 100 != 0);.
- **R** (composition rule (with a neighbour)): with comparison\_operators: Comparisons are the atoms of boolean expressions; because they bind tighter than &amp;&amp; and \|\|, month &gt;= 1 &amp;&amp; month &lt;= 12 groups as (month &gt;= 1) &amp;&amp; (month &lt;= 12) without parentheses.
- **R** (composition rule (with a neighbour)): with logical\_operators: &amp;&amp;, \|\| and ! combine boolean sub-expressions into a larger one; ! binds tighter than comparisons, so negating a comparison needs parentheses: !(x &gt; 0).
- **R** (composition rule (with a neighbour)): with if\_statement: The if statement evaluates its boolean expression once and runs its block only when the value is true; the expression must have type boolean, so if (x = 5) with int x does not compile.
- **R** (composition rule (with a neighbour)): with while\_loop: The while loop re-evaluates its boolean expression before every pass and stops the first time it is false, so some variable in the expression must change in the body or the loop never ends.
- **R** (composition rule (with a neighbour)): with random\_move: In RandomSurfer the boolean expression r &lt; sum is evaluated for each candidate page j in turn, as sum grows; the first j for which it is true is the chosen page.
- **R** (composition rule (with a neighbour)): with syntax\_template: In the template if (&lt;boolean expression&gt;) { &lt;statements&gt; } the placeholder may be filled by any boolean-typed expression: a literal, a boolean variable, a comparison or a combination with logical operators.
- **P** (plan / role rule): Expresses a decision condition or guard (which branch runs, whether a loop continues) or computes a flag; common plans: range test lo &lt;= x &amp;&amp; x &lt;= hi, divisibility test n % k == 0, combined rule as in LeapYear.
- **C** (conservation rule): Rewriting with De Morgan (!(a &amp;&amp; b) as !a \|\| !b) keeps the value for every input; swapping the operands of &amp;&amp; keeps the truth value but can change whether the right operand is evaluated (and whether a guard still protects it); changing &lt; to &lt;= changes the result only at the boundary value.
- **D** (error rule): rule broken: else takes no condition; a second condition needs else if (...). (compile-time)
- **D** (error rule): rule broken: The condition must be a boolean expression; = assigns, == compares. (compile-time)
- **D** (error rule): rule broken: Comparisons cannot be chained; each must be joined with &amp;&amp; or \|\|. (compile-time)
- **X** (applicability rule): Use a boolean expression wherever code must decide or record a yes/no condition, and store it directly (ok = x &gt; y) rather than via if or ? :; when different outcomes are needed for several cases use an if-else chain of such expressions.

## How it is found in code and answers (reader block)

- **Aliases:** boolean expression, condition, conditions
- **Code patterns:** `\b(?:if|while)\s*\(`, `\bfor\s*\([^;]*;[^;]+;`, `\bboolean\s+\w+\s*=\s*[^;]*(?:[<>=!]=?|&&|\|\|)`
- **Operator symbols:** none
- **Java types:** none

## The whole prerequisite chain

- **Everything it builds on (10):** `arithmetic_operators`, `boolean`, `comparison_operators`, `data_type`, `expression`, `identifier`, `literal`, `logical_operators`, `primitive_type`, `variable`
- **Everything that builds on it (51):** `accumulator_pattern`, `animation`, `array_copy`, `array_reversal`, `array_traversal`, `boolean_flag_array`, `break_statement`, `conditional_operator`, `continue_statement`, `convergence_rate`, `convergence_test`, `counter_pattern`, `dangling_else`, `do_while_loop`, `else_if_chain`, `enhanced_for`, `fencepost_loop`, `flag_search_loop`, `for_loop`, `frequency_counting`, `function_plotting`, `if_else_statement`, `if_statement`, `increment_operators`, `infinite_loop`, `labeled_break`, `loop_body`, `loop_control`, `loop_invariant_reasoning`, `loop_performance`, `loop_scope`, `loop_variable`, `matrix_operations`, `monte_carlo_simulation`, `mouse_interaction`, `nested_conditionals`, `nested_loops`, `number_conversion`, `off_by_one_error`, `power_method`, `random_move`, `row_major_order`, `running_extreme`, `sentinel_loop`, `side_effect_order`, `simulation_loop`, `standard_audio`, `switch_statement`, `syntax_template`, `two_models`, `while_loop`

## Every edge in this view and its exact edge logic (35)

All the edges drawn in the picture, in the order: prerequisite, parallel, misconception, error, has_level, contains.

**1. `boolean_expression` &rarr; `if_statement`** (prerequisite)

- **Exact edge logic:** An if runs its block only when its boolean expression evaluates to true.
- **Grounding:** book\_passage
- **Composition rule (R) of `boolean_expression` with `if_statement`:** The if statement evaluates its boolean expression once and runs its block only when the value is true; the expression must have type boolean, so if (x = 5) with int x does not compile.
- **Composition rule (R) of `if_statement` with `boolean_expression`:** The condition must be a boolean expression; a non-boolean condition such as if (t = goal) with int t is a compile-time error, while if (b = false) with boolean b compiles and assigns.

**2. `boolean_expression` &rarr; `random_move`** (prerequisite)

- **Exact edge logic:** The next page is chosen by testing the condition r &lt; sum for each candidate page j in turn.
- **Grounding:** book\_passage
- **Composition rule (R) of `boolean_expression` with `random_move`:** In RandomSurfer the boolean expression r &lt; sum is evaluated for each candidate page j in turn, as sum grows; the first j for which it is true is the chosen page.
- **Composition rule (R) of `random_move` with `boolean_expression`:** The relational test r &lt; sum decides both the chosen page and the early break; &lt; (not &lt;=) matches the half-open interval endpoint tracked by sum.

**3. `boolean_expression` &rarr; `syntax_template`** (prerequisite)

- **Exact edge logic:** In the template if (&lt;boolean expression&gt;) { &lt;statements&gt; }, &lt;boolean expression&gt; stands for any expression of type boolean.
- **Grounding:** book\_passage
- **Composition rule (R) of `boolean_expression` with `syntax_template`:** In the template if (&lt;boolean expression&gt;) { &lt;statements&gt; } the placeholder may be filled by any boolean-typed expression: a literal, a boolean variable, a comparison or a combination with logical operators.
- **Composition rule (R) of `syntax_template` with `boolean_expression`:** The \`&lt;boolean expression&gt;\` slot accepts only expressions of type boolean (\`x &gt; y\`, \`found\`, \`a &amp;&amp; b\`). An int expression or an assignment such as \`x = y\` with int x is a compile error in that slot.

**4. `boolean_expression` &rarr; `while_loop`** (prerequisite)

- **Exact edge logic:** A while tests its boolean condition before every pass and stops the first time it evaluates to false.
- **Grounding:** book\_passage
- **Composition rule (R) of `boolean_expression` with `while_loop`:** The while loop re-evaluates its boolean expression before every pass and stops the first time it is false, so some variable in the expression must change in the body or the loop never ends.
- **Composition rule (R) of `while_loop` with `boolean_expression`:** The loop condition is a boolean expression evaluated before every pass; the loop stops the first time it is false, so the body must eventually make it false.

**5. `comparison_operators` &rarr; `boolean_expression`** (prerequisite)

- **Exact edge logic:** A comparison such as x &lt; y produces a boolean result; comparisons together with boolean logic provide the basis for decision-making.
- **Grounding:** book\_passage
- **Composition rule (R) of `comparison_operators` with `boolean_expression`:** Comparisons are the building blocks of conditions: together with boolean logic they provide the basis for decision-making.
- **Composition rule (R) of `boolean_expression` with `comparison_operators`:** Comparisons are the atoms of boolean expressions; because they bind tighter than &amp;&amp; and \|\|, month &gt;= 1 &amp;&amp; month &lt;= 12 groups as (month &gt;= 1) &amp;&amp; (month &lt;= 12) without parentheses.

**6. `logical_operators` &rarr; `boolean_expression`** (prerequisite)

- **Exact edge logic:** &amp;&amp;, \|\| and ! combine conditions p and q into one larger condition that is still true or false.
- **Grounding:** book\_passage
- **Composition rule (R) of `logical_operators` with `boolean_expression`:** Combining boolean sub-expressions with &amp;&amp;, \|\| and ! yields another boolean expression, so arbitrarily complex conditions can be built with parentheses.
- **Composition rule (R) of `boolean_expression` with `logical_operators`:** &amp;&amp;, \|\| and ! combine boolean sub-expressions into a larger one; ! binds tighter than comparisons, so negating a comparison needs parentheses: !(x &gt; 0).

**7. `boolean_expression` &rarr; `ArithmeticInsteadOfBoolean`** (misconception)

- **Exact edge logic (the wrong rule):** A true/false question is answered with arithmetic (e.g. 1 for true).
- **Twin logic (the right rule):** A logic question is written as a boolean expression whose value is true or false.
- **Role:** context

**8. `boolean_expression` &rarr; `ChainedComparison`** (misconception)

- **Exact edge logic (the wrong rule):** 90 &lt;= grade &lt;= 100 tests whether grade is between 90 and 100.
- **Twin logic (the right rule):** a &lt; b &lt; c does not compile (a &lt; b is a boolean); a range test is written 90 &lt;= grade &amp;&amp; grade &lt;= 100.
- **Role:** context

**9. `boolean_expression` &rarr; `ComparisonWithBooleanLiteral`** (misconception)

- **Exact edge logic (the wrong rule):** To test a boolean b you must write if (b == true).
- **Twin logic (the right rule):** if (b) already tests b, so writing == true adds nothing.
- **Role:** primary

**10. `boolean_expression` &rarr; `LoopForOneTimeTest`** (misconception)

- **Exact edge logic (the wrong rule):** Uses a loop where a condition needs to be tested only once.
- **Twin logic (the right rule):** A test made once is an if; a loop repeats.
- **Role:** context

**11. `boolean_expression` &rarr; `MapToBooleanWithConditionalOperator`** (misconception)

- **Exact edge logic (the wrong rule):** To get a boolean from x &gt; y you need ok = (x &gt; y) ? true : false;.
- **Twin logic (the right rule):** ok = (x &gt; y); already gives the boolean, so the ? : is unnecessary.
- **Role:** primary

**12. `boolean_expression` &rarr; `MapToBooleanWithIf`** (misconception)

- **Exact edge logic (the wrong rule):** To store whether x &gt; y in a boolean you need if (x &gt; y) ok = true; else ok = false;.
- **Twin logic (the right rule):** ok = (x &gt; y); stores the result of the comparison directly.
- **Role:** primary

**13. `boolean_expression` &rarr; `NestedIfsInsteadOfLogicalOperators`** (misconception)

- **Exact edge logic (the wrong rule):** A condition on several values has to be written as nested if statements, one value per if.
- **Twin logic (the right rule):** Several conditions combine into one boolean expression with &amp;&amp; and \|\|, e.g. if (x == 0 &amp;&amp; y == 0).
- **Role:** context

**14. `boolean` &rarr; `ArithmeticInsteadOfBoolean`** (misconception)

- **Exact edge logic (the wrong rule):** A true/false question is answered with arithmetic (e.g. 1 for true).
- **Twin logic (the right rule):** A logic question is written as a boolean expression whose value is true or false.
- **Role:** primary

**15. `comparison_operators` &rarr; `ChainedComparison`** (misconception)

- **Exact edge logic (the wrong rule):** 90 &lt;= grade &lt;= 100 tests whether grade is between 90 and 100.
- **Twin logic (the right rule):** a &lt; b &lt; c does not compile (a &lt; b is a boolean); a range test is written 90 &lt;= grade &amp;&amp; grade &lt;= 100.
- **Role:** primary

**16. `comparison_operators` &rarr; `ComparisonWithBooleanLiteral`** (misconception)

- **Exact edge logic (the wrong rule):** you must write == true / == false to test a boolean
- **Twin logic (the right rule):** if (b) already tests b, so writing == true adds nothing.
- **Role:** context

**17. `conditional_operator` &rarr; `MapToBooleanWithConditionalOperator`** (misconception)

- **Exact edge logic (the wrong rule):** you need ? : to do the same
- **Twin logic (the right rule):** ok = (x &gt; y); already gives the boolean, so the ? : is unnecessary.
- **Role:** context

**18. `if_statement` &rarr; `LoopForOneTimeTest`** (misconception)

- **Exact edge logic (the wrong rule):** Uses a loop where a condition needs to be tested only once.
- **Twin logic (the right rule):** A test made once is an if; a loop repeats.
- **Role:** context

**19. `if_statement` &rarr; `MapToBooleanWithIf`** (misconception)

- **Exact edge logic (the wrong rule):** you need an if to turn a boolean expression into a boolean
- **Twin logic (the right rule):** ok = (x &gt; y); stores the result of the comparison directly.
- **Role:** context

**20. `logical_operators` &rarr; `NestedIfsInsteadOfLogicalOperators`** (misconception)

- **Exact edge logic (the wrong rule):** A condition on several values has to be written as nested if statements, one value per if.
- **Twin logic (the right rule):** Several conditions combine into one boolean expression with &amp;&amp; and \|\|, e.g. if (x == 0 &amp;&amp; y == 0).
- **Role:** primary

**21. `nested_conditionals` &rarr; `NestedIfsInsteadOfLogicalOperators`** (misconception)

- **Exact edge logic (the wrong rule):** A condition on several values has to be written as nested if statements, one value per if.
- **Twin logic (the right rule):** Several conditions combine into one boolean expression with &amp;&amp; and \|\|, e.g. if (x == 0 &amp;&amp; y == 0).
- **Role:** context

**22. `while_loop` &rarr; `LoopForOneTimeTest`** (misconception)

- **Exact edge logic (the wrong rule):** Uses a loop where a condition needs to be tested only once.
- **Twin logic (the right rule):** A test made once is an if; a loop repeats.
- **Role:** primary

**23. `boolean_expression` &rarr; `ElseWithCondition`** (error)

- **Exact edge logic (the wrong rule):** Writes else (x &gt; 0) with a condition but no if.
- **Twin logic (the right rule):** else takes no condition; use else if (x &gt; 0).
- **Role:** context

**24. `if_else_statement` &rarr; `ElseWithCondition`** (error)

- **Exact edge logic (the wrong rule):** Writes else (x &gt; 0) with a condition but no if.
- **Twin logic (the right rule):** else takes no condition; use else if (x &gt; 0).
- **Role:** primary

**25. `boolean_expression` &rarr; `boolean_expression@L0`** (has_level)

- **Exact edge logic:** boolean expression -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (9 ways).
  - **[0] everyday\_reading** (rule type E, folk-meaning rule): Folk meaning: maths writes a range as 90 &lt;= grade &lt;= 100 and English says 'if x is 1 or 2'. Java rule: each comparison is a separate boolean expression and they must be joined explicitly: 90 &lt;= grade &amp;&amp; grade &lt;= 100, x == 1 \|\| x == 2; 90 &lt;= grade &lt;= 100 does not compile because 90 &lt;= grade is already a boolean.
  - **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `ComparisonWithBooleanLiteral`: wrong rule: You must write == true / == false to test a boolean. Right rule: if (b) already tests b, and if (!b) tests that it is false, so == true adds nothing.
  - **[2] misconception** (rule type M, wrong rule / right rule) &rarr; `MapToBooleanWithIf`: wrong rule: You need an if to turn a boolean expression into a boolean. Right rule: ok = (x &gt; y); stores the result of the comparison directly.
  - **[3] misconception** (rule type M, wrong rule / right rule) &rarr; `MapToBooleanWithConditionalOperator`: wrong rule: You need ? : to turn a boolean expression into a boolean (ok = x &gt; y ? true : false). Right rule: ok = (x &gt; y); already gives the boolean, so the ? : is unnecessary.
  - **[4] misconception** (rule type M, wrong rule / right rule) &rarr; `ArithmeticInsteadOfBoolean`: wrong rule: A true/false question is answered with arithmetic (e.g. 1 for true). Right rule: A logic question is written as a boolean expression whose value is true or false, e.g. (year % 4 == 0).
  - **[5] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `ComparisonWithBooleanLiteral`: Points to LT (arithmetic first, then comparisons, then !, &amp;&amp;, \|\|, left to right, with short-circuit). Applied unevenly: the student evaluates &amp;&amp; before a comparison in one sub-expression, or evaluates the right operand of &amp;&amp; on a pass where the left was already false. (here mixing in: "you must write == true / == false to test a boolean")
  - **[6] misconception** (rule type M, wrong rule / right rule) &rarr; `ChainedComparison`: wrong rule: 90 &lt;= grade &lt;= 100 tests whether grade is between 90 and 100. Right rule: a &lt; b &lt; c does not compile (a &lt; b is a boolean, which cannot be compared with &lt;); a range test is written 90 &lt;= grade &amp;&amp; grade &lt;= 100.
  - **[7] misconception** (rule type M, wrong rule / right rule) &rarr; `LoopForOneTimeTest`: wrong rule: Uses a loop where a condition needs to be tested only once. Right rule: A test made once is an if; a while re-tests its condition and repeats its body for as long as the condition is true.
  - **[8] misconception** (rule type M, wrong rule / right rule) &rarr; `NestedIfsInsteadOfLogicalOperators`: wrong rule: A condition on several values has to be written as nested if statements, one value per if. Right rule: Several conditions combine into one boolean expression with &amp;&amp; and \|\|, e.g. if (x == 0 &amp;&amp; y == 0).

**26. `boolean_expression` &rarr; `boolean_expression@L1`** (has_level)

- **Exact edge logic:** boolean expression -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).
  - **[0] names\_the\_element** (rule type N, identity rule): A boolean expression is any expression whose type is boolean: a boolean literal or variable, a comparison, or such parts combined with &amp;&amp;, \|\| and !.
  - **[1] states\_the\_rule** (rule type S, declarative rule): A boolean expression has value true or false; it is built from comparisons (lower precedence than arithmetic, higher than boolean operators) and boolean operators; the condition of if, while and for must be one.

**27. `boolean_expression` &rarr; `boolean_expression@L2`** (has_level)

- **Exact edge logic:** boolean expression -&gt; L2 (Multistructural): the answer applies the rules of boolean expression to every part of the code, in order (3 ways).
  - **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): Operands are evaluated left to right; arithmetic sub-expressions first, then comparisons, then !, then &amp;&amp;, then \|\|; &amp;&amp; and \|\| evaluate their right operand only when the left has not decided the result.
  - **[1] output\_prediction** (rule type OP, evaluation / result rule): The value is true or false: with year = 1900, (year % 4 == 0) &amp;&amp; (year % 100 != 0) \|\| (year % 400 == 0) is false, so LeapYear prints false.
  - **[2] one\_step\_execution** (rule type OS, state-transition rule): Evaluating a boolean expression changes no variable (unless it contains an assignment, ++ or a method with side effects); state changes only when its value is stored, as in isLeapYear = isLeapYear &amp;&amp; (year % 100 != 0);.

**28. `boolean_expression` &rarr; `boolean_expression@L3`** (has_level)

- **Exact edge logic:** boolean expression -&gt; L3 (Relational): the answer relates the parts (7 ways).
  - **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Comparisons are the atoms of boolean expressions; because they bind tighter than &amp;&amp; and \|\|, month &gt;= 1 &amp;&amp; month &lt;= 12 groups as (month &gt;= 1) &amp;&amp; (month &lt;= 12) without parentheses.
  - **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): &amp;&amp;, \|\| and ! combine boolean sub-expressions into a larger one; ! binds tighter than comparisons, so negating a comparison needs parentheses: !(x &gt; 0).
  - **[2] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): The if statement evaluates its boolean expression once and runs its block only when the value is true; the expression must have type boolean, so if (x = 5) with int x does not compile.
  - **[3] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): The while loop re-evaluates its boolean expression before every pass and stops the first time it is false, so some variable in the expression must change in the body or the loop never ends.
  - **[4] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): In RandomSurfer the boolean expression r &lt; sum is evaluated for each candidate page j in turn, as sum grows; the first j for which it is true is the chosen page.
  - **[5] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): In the template if (&lt;boolean expression&gt;) { &lt;statements&gt; } the placeholder may be filled by any boolean-typed expression: a literal, a boolean variable, a comparison or a combination with logical operators.
  - **[6] purpose\_of\_the\_whole** (rule type P, plan / role rule): Expresses a decision condition or guard (which branch runs, whether a loop continues) or computes a flag; common plans: range test lo &lt;= x &amp;&amp; x &lt;= hi, divisibility test n % k == 0, combined rule as in LeapYear.

**29. `boolean_expression` &rarr; `boolean_expression@L4`** (has_level)

- **Exact edge logic:** boolean expression -&gt; L4 (Extended abstract): the answer reasons beyond the given code (5 ways).
  - **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `ComparisonWithBooleanLiteral`: Rewriting with De Morgan (!(a &amp;&amp; b) as !a \|\| !b) keeps the value for every input; swapping the operands of &amp;&amp; keeps the truth value but can change whether the right operand is evaluated (and whether a guard still protects it); changing &lt; to &lt;= changes the result only at the boundary value.
  - **[1] diagnose\_an\_error** (rule type D, error rule): rule broken: else takes no condition; a second condition needs else if (...). Kind: compile-time. Trigger class: Writing else (x &gt; 0) { ... } after an if block (the compiler reports e.g. 'not a statement' or '; expected').
  - **[2] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Use a boolean expression wherever code must decide or record a yes/no condition, and store it directly (ok = x &gt; y) rather than via if or ? :; when different outcomes are needed for several cases use an if-else chain of such expressions.
  - **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: The condition must be a boolean expression; = assigns, == compares. Kind: compile-time. Trigger class: if (a = b) with int a and b (with boolean variables it compiles and silently assigns).
  - **[4] diagnose\_an\_error** (rule type D, error rule): rule broken: Comparisons cannot be chained; each must be joined with &amp;&amp; or \|\|. Kind: compile-time. Trigger class: Range written as a &lt; b &lt; c or 90 &lt;= grade &lt;= 100.

**30. `topic1.2.e` &rarr; `boolean_expression`** (contains)

- topic `topic1.2.e` contains `boolean_expression`

**31. `topic1.2.e` &rarr; `boolean`** (contains)

- topic `topic1.2.e` contains `boolean`

**32. `topic1.2.e` &rarr; `de_morgan`** (contains)

- topic `topic1.2.e` contains `de_morgan`

**33. `topic1.2.e` &rarr; `exclusive_or`** (contains)

- topic `topic1.2.e` contains `exclusive_or`

**34. `topic1.2.e` &rarr; `logical_operators`** (contains)

- topic `topic1.2.e` contains `logical_operators`

**35. `topic1.2.e` &rarr; `short_circuit`** (contains)

- topic `topic1.2.e` contains `short_circuit`
