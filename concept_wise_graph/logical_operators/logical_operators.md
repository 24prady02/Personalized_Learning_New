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

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 25 edges around this concept. The edge logic, the wrong and right rules and the exact rules of the ways are copied word for word from the graph.

## To work on (0)

Nothing is missing for this concept.

## What it needs first (1)

A prerequisite edge means the other concept has to be understood before `logical_operators`.

### `boolean` comes before `logical_operators`

*true/false primitive*

- **Edge:** `pre:boolean->logical_operators`
- **Exact edge logic:** &amp;&amp;, \|\| and ! are the operations defined on the boolean type: they take booleans and give a boolean.
- **Grounding:** book\_passage
- **Composition rule (R) of `logical_operators` with `boolean`:** The operands must be boolean, and the result is boolean; int operands are a compile-time error.
- **Composition rule (R) of `boolean` with `logical_operators`:** &amp;&amp;, \|\| and ! accept only boolean operands and return a boolean; applying them to ints (if (x &amp;&amp; y) with int x, y) is a compile-time error.

## What it leads to (4)

These concepts need `logical_operators` first.

### `logical_operators` comes before `boolean_expression`

*an expression that evaluates to true/false*

- **Edge:** `pre:logical_operators->boolean_expression`
- **Exact edge logic:** &amp;&amp;, \|\| and ! combine conditions p and q into one larger condition that is still true or false.
- **Grounding:** book\_passage
- **Composition rule (R) of `logical_operators` with `boolean_expression`:** Combining boolean sub-expressions with &amp;&amp;, \|\| and ! yields another boolean expression, so arbitrarily complex conditions can be built with parentheses.
- **Composition rule (R) of `boolean_expression` with `logical_operators`:** &amp;&amp;, \|\| and ! combine boolean sub-expressions into a larger one; ! binds tighter than comparisons, so negating a comparison needs parentheses: !(x &gt; 0).

### `logical_operators` comes before `de_morgan`

*!(a &amp;&amp; b) == !a \|\| !b and !(a \|\| b) == !a &amp;&amp; !b*

- **Edge:** `pre:logical_operators->de_morgan`
- **Exact edge logic:** De Morgan's laws rewrite expressions built from &amp;&amp; , \|\| and !.
- **Grounding:** book\_passage
- **Composition rule (R) of `logical_operators` with `de_morgan`:** De Morgan's laws rewrite negated &amp;&amp; / \|\| expressions: !(A &amp;&amp; B) is !A \|\| !B and !(A \|\| B) is !A &amp;&amp; !B.
- **Composition rule (R) of `de_morgan` with `logical_operators`:** De Morgan's laws relate the three logical operators: a negated &amp;&amp; becomes an \|\| of negations and a negated \|\| becomes an &amp;&amp; of negations.

### `logical_operators` comes before `exclusive_or`

*^ on booleans is true when the operands differ*

- **Edge:** `pre:logical_operators->exclusive_or`
- **Exact edge logic:** ^ on booleans is another logical operator, defined by a truth table like &amp;&amp;, \|\| and !: true exactly when its operands differ.
- **Grounding:** order\_only
- **Composition rule (R) of `logical_operators` with `exclusive_or`:** ^ on booleans is a further logical operator, true exactly when the operands differ (it equals (a \|\| b) &amp;&amp; !(a &amp;&amp; b)), but unlike &amp;&amp; and \|\| it always evaluates both operands.
- **Composition rule (R) of `exclusive_or` with `logical_operators`:** ^ belongs with &amp;&amp;, \|\| and ! as a boolean operator defined by a truth table, but it is not short-circuit and it binds tighter than &amp;&amp; and \|\|; a ^ b equals (a \|\| b) &amp;&amp; !(a &amp;&amp; b).

### `logical_operators` comes before `short_circuit`

*&amp;&amp;/\|\| stop evaluating once the result is known*

- **Edge:** `pre:logical_operators->short_circuit`
- **Exact edge logic:** &amp;&amp; and \|\| evaluate their second operand only when the first has not already decided the result (false &amp;&amp; x is false, true \|\| x is true).
- **Grounding:** book\_passage
- **Composition rule (R) of `logical_operators` with `short_circuit`:** &amp;&amp; and \|\| are the short-circuit operators: in a guard such as (x != 0 &amp;&amp; y / x &gt; 1) the operand order matters, because the right test runs only when the left one allows it.
- **Composition rule (R) of `short_circuit` with `logical_operators`:** Short-circuiting is the defining evaluation order of &amp;&amp; and \|\| only; the book's other boolean operators (! and ^, and &amp; / \| if used) evaluate all their operands.

## Learned alongside (1)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

### `logical_operators` alongside `comparison_operators`

*== != &lt; &gt; &lt;= &gt;=*

- **Edge:** `par:comparison_operators~logical_operators`
- **Exact edge logic:** Relational operators compare two numbers to give a boolean; logical operators combine booleans into one boolean.
- **Grounding:** book\_passage
- **Composition rule (R) of `logical_operators` with `comparison_operators`:** Comparisons bind tighter than &amp;&amp; and \|\|, so comparisons are evaluated first and their boolean results are then combined (month &gt;= 1 &amp;&amp; month &lt;= 12).
- **Composition rule (R) of `comparison_operators` with `logical_operators`:** Comparisons bind tighter than &amp;&amp; and \|\|, so they are evaluated first and logical operators combine their boolean results.

## Misconceptions (4)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### BooleanPrecedence

- **Edge:** `logical_operators` &rarr; `BooleanPrecedence` (misconception)
- **Exact edge logic (the wrong rule):** a \|\| b &amp;&amp; c is evaluated left to right as (a \|\| b) &amp;&amp; c.
- **Twin logic (the right rule):** &amp;&amp; binds tighter than \|\|, so it is a \|\| (b &amp;&amp; c).
- **Wrong belief (on the node):** a \|\| b &amp;&amp; c is evaluated left to right as (a \|\| b) &amp;&amp; c.
- **Correct rule (on the node):** &amp;&amp; binds tighter than \|\|, so it is a \|\| (b &amp;&amp; c).
- **Provenance:** published
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [2] misconception, exact rule:** wrong rule: a \|\| b &amp;&amp; c is evaluated left to right as (a \|\| b) &amp;&amp; c. Right rule: &amp;&amp; binds tighter than \|\|, so a \|\| b &amp;&amp; c means a \|\| (b &amp;&amp; c); with a = true, b = false, c = false the value is true, not false.
- **Edge `operator_precedence` &rarr; `BooleanPrecedence`, exact edge logic:** a \|\| b &amp;&amp; c is evaluated left to right as (a \|\| b) &amp;&amp; c. **Twin logic:** &amp;&amp; binds tighter than \|\|, so it is a \|\| (b &amp;&amp; c). (role: context)

### NestedIfsInsteadOfLogicalOperators

- **Edge:** `logical_operators` &rarr; `NestedIfsInsteadOfLogicalOperators` (misconception)
- **Exact edge logic (the wrong rule):** A condition on several values has to be written as nested if statements, one value per if.
- **Twin logic (the right rule):** Several conditions combine into one boolean expression with &amp;&amp; and \|\|, e.g. if (x == 0 &amp;&amp; y == 0).
- **Wrong belief (on the node):** A condition on several values has to be written as nested if statements, one value per if.
- **Correct rule (on the node):** Several conditions combine into one boolean expression with &amp;&amp; and \|\|, e.g. if (x == 0 &amp;&amp; y == 0).
- **Provenance:** published
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [3] misconception, exact rule:** wrong rule: A condition on several values has to be written as nested if statements, one value per if. Right rule: Several conditions combine into one boolean expression with &amp;&amp; and \|\|, e.g. if (x == 0 &amp;&amp; y == 0).
- **Edge `boolean_expression` &rarr; `NestedIfsInsteadOfLogicalOperators`, exact edge logic:** A condition on several values has to be written as nested if statements, one value per if. **Twin logic:** Several conditions combine into one boolean expression with &amp;&amp; and \|\|, e.g. if (x == 0 &amp;&amp; y == 0). (role: context)
- **Edge `nested_conditionals` &rarr; `NestedIfsInsteadOfLogicalOperators`, exact edge logic:** A condition on several values has to be written as nested if statements, one value per if. **Twin logic:** Several conditions combine into one boolean expression with &amp;&amp; and \|\|, e.g. if (x == 0 &amp;&amp; y == 0). (role: context)

### NoSingleLogicAnd

- **Edge:** `logical_operators` &rarr; `NoSingleLogicAnd` (misconception)
- **Exact edge logic (the wrong rule):** &amp; only works on bits, so p &amp; q cannot be used with booleans.
- **Twin logic (the right rule):** Java also has a &amp; operator, which the book does not use; logical and is written &amp;&amp;.
- **Wrong belief (on the node):** &amp; is only a bitwise operator
- **Correct rule (on the node):** Java also has a &amp; operator, which the book does not use; logical and is written &amp;&amp;.
- **Provenance:** published
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [1] misconception, exact rule:** wrong rule: &amp; is only a bitwise operator. Right rule: Java also has a &amp; operator, which the book does not use; on boolean operands it is a logical and that always evaluates both operands; logical and is written &amp;&amp;.
- **L0 way [4] inconsistent\_trace, exact rule:** Points to LT (! first, then &amp;&amp;, then \|\|; left operand first; right operand of &amp;&amp; / \|\| only if needed). Applied unevenly: in one row of a trace the student evaluates the right operand of &amp;&amp; although the left was false (or reads \|\| as exclusive when both operands are true) and in another row applies the rule correctly. (here mixing in: "&amp; is only a bitwise operator")

### SingleAmpersandForAnd

- **Edge:** `logical_operators` &rarr; `SingleAmpersandForAnd` (misconception)
- **Exact edge logic (the wrong rule):** &amp; and \| are the same as &amp;&amp; and \|\| for conditions, so either can be used.
- **Twin logic (the right rule):** &amp;&amp; and \|\| skip the right operand when the left decides the result; &amp; and \| always evaluate both, which fails when the right side depends on the left (e.g. x != 0 &amp; y / x &gt; 1).
- **Wrong belief (on the node):** &amp; and \| are the same as &amp;&amp; and \|\| for conditions, so either can be used.
- **Correct rule (on the node):** &amp;&amp; and \|\| skip the right operand when the left decides the result; &amp; and \| always evaluate both, which fails when the right side depends on the left (e.g. x != 0 &amp; y / x &gt; 1).
- **Provenance:** published
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [5] misconception, exact rule:** wrong rule: &amp; and \| are the same as &amp;&amp; and \|\| for conditions, so either can be used. Right rule: &amp;&amp; and \|\| skip the right operand when the left decides the result; &amp; and \| always evaluate both, which fails when the right side depends on the left (e.g. x != 0 &amp; y / x &gt; 1 throws when x is 0).
- **Edge `short_circuit` &rarr; `SingleAmpersandForAnd`, exact edge logic:** &amp; and \| are the same as &amp;&amp; and \|\| for conditions, so either can be used. **Twin logic:** &amp;&amp; and \|\| skip the right operand when the left decides the result; &amp; and \| always evaluate both, which fails when the right side depends on the left (e.g. x != 0 &amp; y / x &gt; 1). (role: primary)

## Errors (0)

An error edge states the rule that gets broken in a program, and the right rule.

The graph has no error edge from this concept.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for logical operators: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to logical operators agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

- **Edge:** `logical_operators` &rarr; `logical_operators@L0` (has_level)
- **Exact edge logic:** logical operators -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (6 ways).

Ways (6), each with its exact rule:

- **[0] everyday\_reading** (rule type E, folk-meaning rule): Folk meaning: English 'or' is often exclusive ('tea or coffee') and 'and' can join alternatives ('x is 1 and 2' meaning either value). Java rule: \|\| is inclusive (true when either or both operands are true) and &amp;&amp; is true only when both operands are true, so x == 1 &amp;&amp; x == 2 is always false.
- **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `NoSingleLogicAnd`: wrong rule: &amp; is only a bitwise operator. Right rule: Java also has a &amp; operator, which the book does not use; on boolean operands it is a logical and that always evaluates both operands; logical and is written &amp;&amp;.
- **[2] misconception** (rule type M, wrong rule / right rule) &rarr; `BooleanPrecedence`: wrong rule: a \|\| b &amp;&amp; c is evaluated left to right as (a \|\| b) &amp;&amp; c. Right rule: &amp;&amp; binds tighter than \|\|, so a \|\| b &amp;&amp; c means a \|\| (b &amp;&amp; c); with a = true, b = false, c = false the value is true, not false.
- **[3] misconception** (rule type M, wrong rule / right rule) &rarr; `NestedIfsInsteadOfLogicalOperators`: wrong rule: A condition on several values has to be written as nested if statements, one value per if. Right rule: Several conditions combine into one boolean expression with &amp;&amp; and \|\|, e.g. if (x == 0 &amp;&amp; y == 0).
- **[4] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `NoSingleLogicAnd`: Points to LT (! first, then &amp;&amp;, then \|\|; left operand first; right operand of &amp;&amp; / \|\| only if needed). Applied unevenly: in one row of a trace the student evaluates the right operand of &amp;&amp; although the left was false (or reads \|\| as exclusive when both operands are true) and in another row applies the rule correctly. (here mixing in: "&amp; is only a bitwise operator")
- **[5] misconception** (rule type M, wrong rule / right rule) &rarr; `SingleAmpersandForAnd`: wrong rule: &amp; and \| are the same as &amp;&amp; and \|\| for conditions, so either can be used. Right rule: &amp;&amp; and \|\| skip the right operand when the left decides the result; &amp; and \| always evaluate both, which fails when the right side depends on the left (e.g. x != 0 &amp; y / x &gt; 1 throws when x is 0).

### L1: Unistructural / atom x text surface

L1 for logical operators: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

- **Edge:** `logical_operators` &rarr; `logical_operators@L1` (has_level)
- **Exact edge logic:** logical operators -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

Ways (2), each with its exact rule:

- **[0] names\_the\_element** (rule type N, identity rule): Logical (boolean) operators: &amp;&amp; (and), \|\| (or) and ! (not), which take boolean operands and produce a boolean.
- **[1] states\_the\_rule** (rule type S, declarative rule): a &amp;&amp; b is true if both operands are true and false otherwise; a \|\| b is false if both are false and true otherwise; !a is the opposite of a; these definitions are given in full by truth tables.

### L2: Multistructural / block x execution / preoperational

L2 for logical operators: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

- **Edge:** `logical_operators` &rarr; `logical_operators@L2` (has_level)
- **Exact edge logic:** logical operators -&gt; L2 (Multistructural): the answer applies the rules of logical operators to every part of the code, in order (3 ways).

Ways (3), each with its exact rule:

- **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): ! is applied before &amp;&amp; and \|\|, and &amp;&amp; before \|\|; the left operand is evaluated first, and for &amp;&amp; and \|\| the right operand is evaluated only when the left has not already decided the result.
- **[1] output\_prediction** (rule type OP, evaluation / result rule): The result is a boolean: with x = 10, x &gt; 0 &amp;&amp; x &lt; 10 is false and x &lt; 0 \|\| x &gt; 10 is false; true \|\| anything is true.
- **[2] one\_step\_execution** (rule type OS, state-transition rule): The operators themselves change no variable; any side effect inside the right operand (i++, a method call) happens only if that operand is evaluated.

### L3: Relational / relations x function (concrete operational begins)

L3 for logical operators: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

- **Edge:** `logical_operators` &rarr; `logical_operators@L3` (has_level)
- **Exact edge logic:** logical operators -&gt; L3 (Relational): the answer relates the parts (7 ways).

Ways (7), each with its exact rule:

- **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Combining boolean sub-expressions with &amp;&amp;, \|\| and ! yields another boolean expression, so arbitrarily complex conditions can be built with parentheses.
- **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): &amp;&amp; and \|\| are the short-circuit operators: in a guard such as (x != 0 &amp;&amp; y / x &gt; 1) the operand order matters, because the right test runs only when the left one allows it.
- **[2] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Comparisons bind tighter than &amp;&amp; and \|\|, so comparisons are evaluated first and their boolean results are then combined (month &gt;= 1 &amp;&amp; month &lt;= 12).
- **[3] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): ^ on booleans is a further logical operator, true exactly when the operands differ (it equals (a \|\| b) &amp;&amp; !(a &amp;&amp; b)), but unlike &amp;&amp; and \|\| it always evaluates both operands.
- **[4] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): De Morgan's laws rewrite negated &amp;&amp; / \|\| expressions: !(A &amp;&amp; B) is !A \|\| !B and !(A \|\| B) is !A &amp;&amp; !B.
- **[5] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): The operands must be boolean, and the result is boolean; int operands are a compile-time error.
- **[6] purpose\_of\_the\_whole** (rule type P, plan / role rule): Used to combine several conditions into one test: a range check (lo &lt;= x &amp;&amp; x &lt;= hi), alternatives (x == 0 \|\| y == 0), a guard followed by the real test (i &lt; n &amp;&amp; a[i] != 0), or a rule built step by step as in LeapYear.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for logical operators: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

- **Edge:** `logical_operators` &rarr; `logical_operators@L4` (has_level)
- **Exact edge logic:** logical operators -&gt; L4 (Extended abstract): the answer reasons beyond the given code (5 ways).

Ways (5), each with its exact rule:

- **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `NoSingleLogicAnd`: Swapping &amp;&amp; for \|\| changes the meaning; negating a whole condition requires De Morgan (negate each term and flip the operator); swapping the operands of &amp;&amp; or \|\| keeps the truth value but can change which side effects or exceptions occur.
- **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Use &amp;&amp; and \|\| to combine conditions into a single test, ordering operands so that cheap or protective tests come first; use nested ifs only when the cases need different actions; do not use &amp; and \| for conditions.
- **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: Conditions are combined with &amp;&amp; and \|\|; &amp; and \| evaluate both operands. Kind: run-time exception. Trigger class: Using &amp; or \| where the right operand is only safe when the left decides first, e.g. x != 0 &amp; y / x &gt; 1 with x == 0 (ArithmeticException) or an out-of-range index; otherwise a silent difference only when the right side has side effects.
- **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: &amp;&amp; has higher precedence than \|\|. Kind: silent logic error. Trigger class: Mixed &amp;&amp; and \|\| without parentheses intended to group the \|\| first, e.g. a \|\| b &amp;&amp; c meant as (a \|\| b) &amp;&amp; c.
- **[4] diagnose\_an\_error** (rule type D, error rule): rule broken: Logical operators take boolean operands only. Kind: compile-time. Trigger class: Applying &amp;&amp; or \|\| to int operands (if (x &amp;&amp; y) with ints) or writing and/or as words.

## Same topic

`logical_operators` belongs to the topic **Booleans** (`topic1.2.e`). The topic also contains: `boolean`, `boolean_expression`, `de_morgan`, `exclusive_or`, `short_circuit`.

## Rules of the concept (23)

- **Book** (SW-1e, p. 25 (pdf 35)): "The most important operations defined for booleans are and (&amp;&amp;), or (\|\|), and not (!)"
- **Book** (SW-1.2, ): "The most important operators defined for the boolean are for and, or, and not."
- **E** (folk-meaning rule): Folk meaning: English 'or' is often exclusive ('tea or coffee') and 'and' can join alternatives ('x is 1 and 2' meaning either value). Java rule: \|\| is inclusive (true when either or both operands are true) and &amp;&amp; is true only when both operands are true, so x == 1 &amp;&amp; x == 2 is always false.
- **M** (wrong rule / right rule): BooleanPrecedence: wrong: a \|\| b &amp;&amp; c is evaluated left to right as (a \|\| b) &amp;&amp; c. \| right: &amp;&amp; binds tighter than \|\|, so a \|\| b &amp;&amp; c means a \|\| (b &amp;&amp; c); with a = true, b = false, c = false the value is true, not false.
- **M** (wrong rule / right rule): NoSingleLogicAnd: wrong: &amp; is only a bitwise operator. \| right: Java also has a &amp; operator, which the book does not use; on boolean operands it is a logical and that always evaluates both operands; logical and is written &amp;&amp;.
- **M** (wrong rule / right rule): NestedIfsInsteadOfLogicalOperators: wrong: A condition on several values has to be written as nested if statements, one value per if. \| right: Several conditions combine into one boolean expression with &amp;&amp; and \|\|, e.g. if (x == 0 &amp;&amp; y == 0).
- **M** (wrong rule / right rule): SingleAmpersandForAnd: wrong: &amp; and \| are the same as &amp;&amp; and \|\| for conditions, so either can be used. \| right: &amp;&amp; and \|\| skip the right operand when the left decides the result; &amp; and \| always evaluate both, which fails when the right side depends on the left (e.g. x != 0 &amp; y / x &gt; 1 throws when x is 0).
- **T** (uneven-application rule): Points to LT (! first, then &amp;&amp;, then \|\|; left operand first; right operand of &amp;&amp; / \|\| only if needed). Applied unevenly: in one row of a trace the student evaluates the right operand of &amp;&amp; although the left was false (or reads \|\| as exclusive when both operands are true) and in another row applies the rule correctly.
- **N** (identity rule): Logical (boolean) operators: &amp;&amp; (and), \|\| (or) and ! (not), which take boolean operands and produce a boolean.
- **S** (declarative rule): a &amp;&amp; b is true if both operands are true and false otherwise; a \|\| b is false if both are false and true otherwise; !a is the opposite of a; these definitions are given in full by truth tables.
- **LT** (operational sequencing rule): ! is applied before &amp;&amp; and \|\|, and &amp;&amp; before \|\|; the left operand is evaluated first, and for &amp;&amp; and \|\| the right operand is evaluated only when the left has not already decided the result.
- **OP** (evaluation / result rule): The result is a boolean: with x = 10, x &gt; 0 &amp;&amp; x &lt; 10 is false and x &lt; 0 \|\| x &gt; 10 is false; true \|\| anything is true.
- **OS** (state-transition rule): The operators themselves change no variable; any side effect inside the right operand (i++, a method call) happens only if that operand is evaluated.
- **R** (composition rule (with a neighbour)): with boolean\_expression: Combining boolean sub-expressions with &amp;&amp;, \|\| and ! yields another boolean expression, so arbitrarily complex conditions can be built with parentheses.
- **R** (composition rule (with a neighbour)): with short\_circuit: &amp;&amp; and \|\| are the short-circuit operators: in a guard such as (x != 0 &amp;&amp; y / x &gt; 1) the operand order matters, because the right test runs only when the left one allows it.
- **R** (composition rule (with a neighbour)): with comparison\_operators: Comparisons bind tighter than &amp;&amp; and \|\|, so comparisons are evaluated first and their boolean results are then combined (month &gt;= 1 &amp;&amp; month &lt;= 12).
- **R** (composition rule (with a neighbour)): with exclusive\_or: ^ on booleans is a further logical operator, true exactly when the operands differ (it equals (a \|\| b) &amp;&amp; !(a &amp;&amp; b)), but unlike &amp;&amp; and \|\| it always evaluates both operands.
- **R** (composition rule (with a neighbour)): with de\_morgan: De Morgan's laws rewrite negated &amp;&amp; / \|\| expressions: !(A &amp;&amp; B) is !A \|\| !B and !(A \|\| B) is !A &amp;&amp; !B.
- **R** (composition rule (with a neighbour)): with boolean: The operands must be boolean, and the result is boolean; int operands are a compile-time error.
- **P** (plan / role rule): Used to combine several conditions into one test: a range check (lo &lt;= x &amp;&amp; x &lt;= hi), alternatives (x == 0 \|\| y == 0), a guard followed by the real test (i &lt; n &amp;&amp; a[i] != 0), or a rule built step by step as in LeapYear.
- **C** (conservation rule): Swapping &amp;&amp; for \|\| changes the meaning; negating a whole condition requires De Morgan (negate each term and flip the operator); swapping the operands of &amp;&amp; or \|\| keeps the truth value but can change which side effects or exceptions occur.
- **D** (error rule): rule broken: Conditions are combined with &amp;&amp; and \|\|; &amp; and \| evaluate both operands. (run-time exception)
- **D** (error rule): rule broken: &amp;&amp; has higher precedence than \|\|. (silent logic error)
- **D** (error rule): rule broken: Logical operators take boolean operands only. (compile-time)
- **X** (applicability rule): Use &amp;&amp; and \|\| to combine conditions into a single test, ordering operands so that cheap or protective tests come first; use nested ifs only when the cases need different actions; do not use &amp; and \| for conditions.

## How it is found in code and answers (reader block)

- **Aliases:** and operator, or operator, logical, &amp;&amp;, \|\|
- **Code patterns:** `&&|\|\||!(?!=)`
- **Operator symbols:** none
- **Java types:** none

## The whole prerequisite chain

- **Everything it builds on (3):** `boolean`, `data_type`, `primitive_type`
- **Everything that builds on it (55):** `accumulator_pattern`, `animation`, `array_copy`, `array_reversal`, `array_traversal`, `boolean_expression`, `boolean_flag_array`, `break_statement`, `conditional_operator`, `continue_statement`, `convergence_rate`, `convergence_test`, `counter_pattern`, `dangling_else`, `de_morgan`, `do_while_loop`, `else_if_chain`, `enhanced_for`, `exclusive_or`, `fencepost_loop`, `flag_search_loop`, `for_loop`, `frequency_counting`, `function_plotting`, `if_else_statement`, `if_statement`, `increment_operators`, `infinite_loop`, `labeled_break`, `loop_body`, `loop_control`, `loop_invariant_reasoning`, `loop_performance`, `loop_scope`, `loop_variable`, `matrix_operations`, `monte_carlo_simulation`, `mouse_interaction`, `nested_conditionals`, `nested_loops`, `number_conversion`, `off_by_one_error`, `power_method`, `random_move`, `row_major_order`, `running_extreme`, `sentinel_loop`, `short_circuit`, `side_effect_order`, `simulation_loop`, `standard_audio`, `switch_statement`, `syntax_template`, `two_models`, `while_loop`

## Every edge in this view and its exact edge logic (25)

All the edges drawn in the picture, in the order: prerequisite, parallel, misconception, error, has_level, contains.

**1. `boolean` &rarr; `logical_operators`** (prerequisite)

- **Exact edge logic:** &amp;&amp;, \|\| and ! are the operations defined on the boolean type: they take booleans and give a boolean.
- **Grounding:** book\_passage
- **Composition rule (R) of `boolean` with `logical_operators`:** &amp;&amp;, \|\| and ! accept only boolean operands and return a boolean; applying them to ints (if (x &amp;&amp; y) with int x, y) is a compile-time error.
- **Composition rule (R) of `logical_operators` with `boolean`:** The operands must be boolean, and the result is boolean; int operands are a compile-time error.

**2. `logical_operators` &rarr; `boolean_expression`** (prerequisite)

- **Exact edge logic:** &amp;&amp;, \|\| and ! combine conditions p and q into one larger condition that is still true or false.
- **Grounding:** book\_passage
- **Composition rule (R) of `logical_operators` with `boolean_expression`:** Combining boolean sub-expressions with &amp;&amp;, \|\| and ! yields another boolean expression, so arbitrarily complex conditions can be built with parentheses.
- **Composition rule (R) of `boolean_expression` with `logical_operators`:** &amp;&amp;, \|\| and ! combine boolean sub-expressions into a larger one; ! binds tighter than comparisons, so negating a comparison needs parentheses: !(x &gt; 0).

**3. `logical_operators` &rarr; `de_morgan`** (prerequisite)

- **Exact edge logic:** De Morgan's laws rewrite expressions built from &amp;&amp; , \|\| and !.
- **Grounding:** book\_passage
- **Composition rule (R) of `logical_operators` with `de_morgan`:** De Morgan's laws rewrite negated &amp;&amp; / \|\| expressions: !(A &amp;&amp; B) is !A \|\| !B and !(A \|\| B) is !A &amp;&amp; !B.
- **Composition rule (R) of `de_morgan` with `logical_operators`:** De Morgan's laws relate the three logical operators: a negated &amp;&amp; becomes an \|\| of negations and a negated \|\| becomes an &amp;&amp; of negations.

**4. `logical_operators` &rarr; `exclusive_or`** (prerequisite)

- **Exact edge logic:** ^ on booleans is another logical operator, defined by a truth table like &amp;&amp;, \|\| and !: true exactly when its operands differ.
- **Grounding:** order\_only
- **Composition rule (R) of `logical_operators` with `exclusive_or`:** ^ on booleans is a further logical operator, true exactly when the operands differ (it equals (a \|\| b) &amp;&amp; !(a &amp;&amp; b)), but unlike &amp;&amp; and \|\| it always evaluates both operands.
- **Composition rule (R) of `exclusive_or` with `logical_operators`:** ^ belongs with &amp;&amp;, \|\| and ! as a boolean operator defined by a truth table, but it is not short-circuit and it binds tighter than &amp;&amp; and \|\|; a ^ b equals (a \|\| b) &amp;&amp; !(a &amp;&amp; b).

**5. `logical_operators` &rarr; `short_circuit`** (prerequisite)

- **Exact edge logic:** &amp;&amp; and \|\| evaluate their second operand only when the first has not already decided the result (false &amp;&amp; x is false, true \|\| x is true).
- **Grounding:** book\_passage
- **Composition rule (R) of `logical_operators` with `short_circuit`:** &amp;&amp; and \|\| are the short-circuit operators: in a guard such as (x != 0 &amp;&amp; y / x &gt; 1) the operand order matters, because the right test runs only when the left one allows it.
- **Composition rule (R) of `short_circuit` with `logical_operators`:** Short-circuiting is the defining evaluation order of &amp;&amp; and \|\| only; the book's other boolean operators (! and ^, and &amp; / \| if used) evaluate all their operands.

**6. `comparison_operators` &harr; `logical_operators`** (parallel)

- **Exact edge logic:** Relational operators compare two numbers to give a boolean; logical operators combine booleans into one boolean.
- **Grounding:** book\_passage
- **Composition rule (R) of `comparison_operators` with `logical_operators`:** Comparisons bind tighter than &amp;&amp; and \|\|, so they are evaluated first and logical operators combine their boolean results.
- **Composition rule (R) of `logical_operators` with `comparison_operators`:** Comparisons bind tighter than &amp;&amp; and \|\|, so comparisons are evaluated first and their boolean results are then combined (month &gt;= 1 &amp;&amp; month &lt;= 12).

**7. `logical_operators` &rarr; `BooleanPrecedence`** (misconception)

- **Exact edge logic (the wrong rule):** a \|\| b &amp;&amp; c is evaluated left to right as (a \|\| b) &amp;&amp; c.
- **Twin logic (the right rule):** &amp;&amp; binds tighter than \|\|, so it is a \|\| (b &amp;&amp; c).
- **Role:** primary

**8. `logical_operators` &rarr; `NestedIfsInsteadOfLogicalOperators`** (misconception)

- **Exact edge logic (the wrong rule):** A condition on several values has to be written as nested if statements, one value per if.
- **Twin logic (the right rule):** Several conditions combine into one boolean expression with &amp;&amp; and \|\|, e.g. if (x == 0 &amp;&amp; y == 0).
- **Role:** primary

**9. `logical_operators` &rarr; `NoSingleLogicAnd`** (misconception)

- **Exact edge logic (the wrong rule):** &amp; only works on bits, so p &amp; q cannot be used with booleans.
- **Twin logic (the right rule):** Java also has a &amp; operator, which the book does not use; logical and is written &amp;&amp;.
- **Role:** primary

**10. `logical_operators` &rarr; `SingleAmpersandForAnd`** (misconception)

- **Exact edge logic (the wrong rule):** &amp; and \| are the same as &amp;&amp; and \|\| for conditions, so either can be used.
- **Twin logic (the right rule):** &amp;&amp; and \|\| skip the right operand when the left decides the result; &amp; and \| always evaluate both, which fails when the right side depends on the left (e.g. x != 0 &amp; y / x &gt; 1).
- **Role:** context

**11. `boolean_expression` &rarr; `NestedIfsInsteadOfLogicalOperators`** (misconception)

- **Exact edge logic (the wrong rule):** A condition on several values has to be written as nested if statements, one value per if.
- **Twin logic (the right rule):** Several conditions combine into one boolean expression with &amp;&amp; and \|\|, e.g. if (x == 0 &amp;&amp; y == 0).
- **Role:** context

**12. `nested_conditionals` &rarr; `NestedIfsInsteadOfLogicalOperators`** (misconception)

- **Exact edge logic (the wrong rule):** A condition on several values has to be written as nested if statements, one value per if.
- **Twin logic (the right rule):** Several conditions combine into one boolean expression with &amp;&amp; and \|\|, e.g. if (x == 0 &amp;&amp; y == 0).
- **Role:** context

**13. `operator_precedence` &rarr; `BooleanPrecedence`** (misconception)

- **Exact edge logic (the wrong rule):** a \|\| b &amp;&amp; c is evaluated left to right as (a \|\| b) &amp;&amp; c.
- **Twin logic (the right rule):** &amp;&amp; binds tighter than \|\|, so it is a \|\| (b &amp;&amp; c).
- **Role:** context

**14. `short_circuit` &rarr; `SingleAmpersandForAnd`** (misconception)

- **Exact edge logic (the wrong rule):** &amp; and \| are the same as &amp;&amp; and \|\| for conditions, so either can be used.
- **Twin logic (the right rule):** &amp;&amp; and \|\| skip the right operand when the left decides the result; &amp; and \| always evaluate both, which fails when the right side depends on the left (e.g. x != 0 &amp; y / x &gt; 1).
- **Role:** primary

**15. `logical_operators` &rarr; `logical_operators@L0`** (has_level)

- **Exact edge logic:** logical operators -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (6 ways).
  - **[0] everyday\_reading** (rule type E, folk-meaning rule): Folk meaning: English 'or' is often exclusive ('tea or coffee') and 'and' can join alternatives ('x is 1 and 2' meaning either value). Java rule: \|\| is inclusive (true when either or both operands are true) and &amp;&amp; is true only when both operands are true, so x == 1 &amp;&amp; x == 2 is always false.
  - **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `NoSingleLogicAnd`: wrong rule: &amp; is only a bitwise operator. Right rule: Java also has a &amp; operator, which the book does not use; on boolean operands it is a logical and that always evaluates both operands; logical and is written &amp;&amp;.
  - **[2] misconception** (rule type M, wrong rule / right rule) &rarr; `BooleanPrecedence`: wrong rule: a \|\| b &amp;&amp; c is evaluated left to right as (a \|\| b) &amp;&amp; c. Right rule: &amp;&amp; binds tighter than \|\|, so a \|\| b &amp;&amp; c means a \|\| (b &amp;&amp; c); with a = true, b = false, c = false the value is true, not false.
  - **[3] misconception** (rule type M, wrong rule / right rule) &rarr; `NestedIfsInsteadOfLogicalOperators`: wrong rule: A condition on several values has to be written as nested if statements, one value per if. Right rule: Several conditions combine into one boolean expression with &amp;&amp; and \|\|, e.g. if (x == 0 &amp;&amp; y == 0).
  - **[4] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `NoSingleLogicAnd`: Points to LT (! first, then &amp;&amp;, then \|\|; left operand first; right operand of &amp;&amp; / \|\| only if needed). Applied unevenly: in one row of a trace the student evaluates the right operand of &amp;&amp; although the left was false (or reads \|\| as exclusive when both operands are true) and in another row applies the rule correctly. (here mixing in: "&amp; is only a bitwise operator")
  - **[5] misconception** (rule type M, wrong rule / right rule) &rarr; `SingleAmpersandForAnd`: wrong rule: &amp; and \| are the same as &amp;&amp; and \|\| for conditions, so either can be used. Right rule: &amp;&amp; and \|\| skip the right operand when the left decides the result; &amp; and \| always evaluate both, which fails when the right side depends on the left (e.g. x != 0 &amp; y / x &gt; 1 throws when x is 0).

**16. `logical_operators` &rarr; `logical_operators@L1`** (has_level)

- **Exact edge logic:** logical operators -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).
  - **[0] names\_the\_element** (rule type N, identity rule): Logical (boolean) operators: &amp;&amp; (and), \|\| (or) and ! (not), which take boolean operands and produce a boolean.
  - **[1] states\_the\_rule** (rule type S, declarative rule): a &amp;&amp; b is true if both operands are true and false otherwise; a \|\| b is false if both are false and true otherwise; !a is the opposite of a; these definitions are given in full by truth tables.

**17. `logical_operators` &rarr; `logical_operators@L2`** (has_level)

- **Exact edge logic:** logical operators -&gt; L2 (Multistructural): the answer applies the rules of logical operators to every part of the code, in order (3 ways).
  - **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): ! is applied before &amp;&amp; and \|\|, and &amp;&amp; before \|\|; the left operand is evaluated first, and for &amp;&amp; and \|\| the right operand is evaluated only when the left has not already decided the result.
  - **[1] output\_prediction** (rule type OP, evaluation / result rule): The result is a boolean: with x = 10, x &gt; 0 &amp;&amp; x &lt; 10 is false and x &lt; 0 \|\| x &gt; 10 is false; true \|\| anything is true.
  - **[2] one\_step\_execution** (rule type OS, state-transition rule): The operators themselves change no variable; any side effect inside the right operand (i++, a method call) happens only if that operand is evaluated.

**18. `logical_operators` &rarr; `logical_operators@L3`** (has_level)

- **Exact edge logic:** logical operators -&gt; L3 (Relational): the answer relates the parts (7 ways).
  - **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Combining boolean sub-expressions with &amp;&amp;, \|\| and ! yields another boolean expression, so arbitrarily complex conditions can be built with parentheses.
  - **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): &amp;&amp; and \|\| are the short-circuit operators: in a guard such as (x != 0 &amp;&amp; y / x &gt; 1) the operand order matters, because the right test runs only when the left one allows it.
  - **[2] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Comparisons bind tighter than &amp;&amp; and \|\|, so comparisons are evaluated first and their boolean results are then combined (month &gt;= 1 &amp;&amp; month &lt;= 12).
  - **[3] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): ^ on booleans is a further logical operator, true exactly when the operands differ (it equals (a \|\| b) &amp;&amp; !(a &amp;&amp; b)), but unlike &amp;&amp; and \|\| it always evaluates both operands.
  - **[4] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): De Morgan's laws rewrite negated &amp;&amp; / \|\| expressions: !(A &amp;&amp; B) is !A \|\| !B and !(A \|\| B) is !A &amp;&amp; !B.
  - **[5] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): The operands must be boolean, and the result is boolean; int operands are a compile-time error.
  - **[6] purpose\_of\_the\_whole** (rule type P, plan / role rule): Used to combine several conditions into one test: a range check (lo &lt;= x &amp;&amp; x &lt;= hi), alternatives (x == 0 \|\| y == 0), a guard followed by the real test (i &lt; n &amp;&amp; a[i] != 0), or a rule built step by step as in LeapYear.

**19. `logical_operators` &rarr; `logical_operators@L4`** (has_level)

- **Exact edge logic:** logical operators -&gt; L4 (Extended abstract): the answer reasons beyond the given code (5 ways).
  - **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `NoSingleLogicAnd`: Swapping &amp;&amp; for \|\| changes the meaning; negating a whole condition requires De Morgan (negate each term and flip the operator); swapping the operands of &amp;&amp; or \|\| keeps the truth value but can change which side effects or exceptions occur.
  - **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Use &amp;&amp; and \|\| to combine conditions into a single test, ordering operands so that cheap or protective tests come first; use nested ifs only when the cases need different actions; do not use &amp; and \| for conditions.
  - **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: Conditions are combined with &amp;&amp; and \|\|; &amp; and \| evaluate both operands. Kind: run-time exception. Trigger class: Using &amp; or \| where the right operand is only safe when the left decides first, e.g. x != 0 &amp; y / x &gt; 1 with x == 0 (ArithmeticException) or an out-of-range index; otherwise a silent difference only when the right side has side effects.
  - **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: &amp;&amp; has higher precedence than \|\|. Kind: silent logic error. Trigger class: Mixed &amp;&amp; and \|\| without parentheses intended to group the \|\| first, e.g. a \|\| b &amp;&amp; c meant as (a \|\| b) &amp;&amp; c.
  - **[4] diagnose\_an\_error** (rule type D, error rule): rule broken: Logical operators take boolean operands only. Kind: compile-time. Trigger class: Applying &amp;&amp; or \|\| to int operands (if (x &amp;&amp; y) with ints) or writing and/or as words.

**20. `topic1.2.e` &rarr; `logical_operators`** (contains)

- topic `topic1.2.e` contains `logical_operators`

**21. `topic1.2.e` &rarr; `boolean`** (contains)

- topic `topic1.2.e` contains `boolean`

**22. `topic1.2.e` &rarr; `boolean_expression`** (contains)

- topic `topic1.2.e` contains `boolean_expression`

**23. `topic1.2.e` &rarr; `de_morgan`** (contains)

- topic `topic1.2.e` contains `de_morgan`

**24. `topic1.2.e` &rarr; `exclusive_or`** (contains)

- topic `topic1.2.e` contains `exclusive_or`

**25. `topic1.2.e` &rarr; `short_circuit`** (contains)

- topic `topic1.2.e` contains `short_circuit`
