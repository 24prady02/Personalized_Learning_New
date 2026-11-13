# operator_precedence (`operator_precedence`)

the order operators bind in an expression

Section 1.2 Built-in Types of Data, topic 1.2.a Data types and terminology (literals, identifiers, variables, declarations, assignment, expressions).

![The knowledge graph around operator_precedence](operator_precedence.png)

## At a glance

- **Needs first:** `expression`
- **Leads to:** nothing
- **Learned alongside:** nothing
- **Misconceptions:** `ArithmeticPlusPrecedes`, `BooleanPrecedence`, `CastAppliesToWholeExpression`, `MissingClarifyingParentheses`, `StringPlusLeftToRight`, `WrongOperatorOrder`
- **Errors:** none
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 32 edges around this concept. The edge logic, the wrong and right rules and the exact rules of the ways are copied word for word from the graph.

## To work on (1)

- misconceptions with no L0 way linked to them: MissingClarifyingParentheses

## What it needs first (1)

A prerequisite edge means the other concept has to be understood before `operator_precedence`.

### `expression` comes before `operator_precedence`

*anything that evaluates to a value*

- **Edge:** `pre:expression->operator_precedence`
- **Exact edge logic:** When an expression has several operators, precedence decides which operands are combined first, and equal-precedence operators go left to right.
- **Grounding:** book\_passage
- **Composition rule (R) of `operator_precedence` with `expression`:** Precedence decides the grouping of a multi-operator expression, and a parenthesized subexpression is evaluated as one unit with its own value.
- **Composition rule (R) of `expression` with `operator_precedence`:** With several operators, precedence and left associativity decide the grouping, and parentheses override both.

## What it leads to (0)

These concepts need `operator_precedence` first.

No concept has this one as a prerequisite.

## Learned alongside (0)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

No parallel edge touches this concept.

## Misconceptions (6)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### ArithmeticPlusPrecedes

- **Edge:** `operator_precedence` &rarr; `ArithmeticPlusPrecedes` (misconception)
- **Exact edge logic (the wrong rule):** In "s" + a + b, the numbers a and b are added first and their sum is joined to s.
- **Twin logic (the right rule):** Both uses of + have the same precedence and are evaluated left to right, so "s" + a + b joins a and then b as text; only "s" + (a + b) adds them first.
- **Wrong belief (on the node):** arithmetic + binds tighter than string-concatenation +
- **Correct rule (on the node):** Both uses of + have the same precedence and are evaluated left to right, so "s" + a + b joins a and then b as text; only "s" + (a + b) adds them first.
- **Provenance:** published
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [1] misconception, exact rule:** wrong rule: arithmetic + binds tighter than string-concatenation +. Right rule: Both uses of + have the same precedence and are evaluated left to right, so "s" + a + b joins a and then b as text; only "s" + (a + b) adds them first.
- **L0 way [3] inconsistent\_trace, exact rule:** Points to LT (group by precedence, then left to right for operators of equal precedence). Applied unevenly, a student applies \* before + in one place but reads G \* m1 \* m2 / r \* r as dividing by r squared. (here mixing in: "arithmetic + binds tighter than string-concatenation +")
- **Edge `string_concatenation` &rarr; `ArithmeticPlusPrecedes`, exact edge logic:** In "s" + a + b, the numbers a and b are added first and their sum is joined to s. **Twin logic:** Both uses of + have the same precedence and are evaluated left to right, so "s" + a + b joins a and then b as text; only "s" + (a + b) adds them first. (role: primary)

### BooleanPrecedence

- **Edge:** `operator_precedence` &rarr; `BooleanPrecedence` (misconception)
- **Exact edge logic (the wrong rule):** a \|\| b &amp;&amp; c is evaluated left to right as (a \|\| b) &amp;&amp; c.
- **Twin logic (the right rule):** &amp;&amp; binds tighter than \|\|, so it is a \|\| (b &amp;&amp; c).
- **Wrong belief (on the node):** a \|\| b &amp;&amp; c is evaluated left to right as (a \|\| b) &amp;&amp; c.
- **Correct rule (on the node):** &amp;&amp; binds tighter than \|\|, so it is a \|\| (b &amp;&amp; c).
- **Provenance:** published
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [4] misconception, exact rule:** wrong rule: a \|\| b &amp;&amp; c is evaluated left to right as (a \|\| b) &amp;&amp; c. Right rule: &amp;&amp; binds tighter than \|\|, so it is a \|\| (b &amp;&amp; c).
- **Edge `logical_operators` &rarr; `BooleanPrecedence`, exact edge logic:** a \|\| b &amp;&amp; c is evaluated left to right as (a \|\| b) &amp;&amp; c. **Twin logic:** &amp;&amp; binds tighter than \|\|, so it is a \|\| (b &amp;&amp; c). (role: primary)

### CastAppliesToWholeExpression

- **Edge:** `operator_precedence` &rarr; `CastAppliesToWholeExpression` (misconception)
- **Exact edge logic (the wrong rule):** (int) 2.5 / 0.15 casts the whole quotient to int.
- **Twin logic (the right rule):** The cast applies only to what comes right after it, here 2.5.
- **Wrong belief (on the node):** (int) 2.5 / 0.15 casts the whole quotient to int.
- **Correct rule (on the node):** The cast applies only to what comes right after it, here 2.5.
- **Provenance:** textbook
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [5] misconception, exact rule:** wrong rule: (int) 2.5 / 0.15 casts the whole quotient to int. Right rule: The cast applies only to what comes right after it, here 2.5.
- **Edge `explicit_cast` &rarr; `CastAppliesToWholeExpression`, exact edge logic:** (int) 2.5 / 0.15 casts the whole quotient to int. **Twin logic:** The cast applies only to what comes right after it, here 2.5. (role: primary)

### MissingClarifyingParentheses

- **Edge:** `operator_precedence` &rarr; `MissingClarifyingParentheses` (misconception)
- **Exact edge logic (the wrong rule):** Writes compound expressions such as a + b \* c / d - e % f with no parentheses, relying on the reader to know precedence.
- **Twin logic (the right rule):** When writing compound expressions, be explicit and indicate with parentheses which operators should be evaluated first.
- **Wrong belief (on the node):** Writes compound expressions such as a + b \* c / d - e % f with no parentheses, relying on the reader to know precedence.
- **Correct rule (on the node):** When writing compound expressions, be explicit and indicate with parentheses which operators should be evaluated first.
- **Provenance:** rule\_dictionary
- **Role of this concept:** primary
- **L0 way linked to it:** no

### StringPlusLeftToRight

- **Edge:** `operator_precedence` &rarr; `StringPlusLeftToRight` (misconception)
- **Exact edge logic (the wrong rule):** 2 + 3 + "bc" and "bc" + 2 + 3 give the same text.
- **Twin logic (the right rule):** + is evaluated left to right: 2 + 3 + "bc" is "5bc" but "bc" + 2 + 3 is "bc23".
- **Wrong belief (on the node):** 2 + 3 + "bc" and "bc" + 2 + 3 give the same text.
- **Correct rule (on the node):** + is evaluated left to right: 2 + 3 + "bc" is "5bc" but "bc" + 2 + 3 is "bc23".
- **Provenance:** textbook
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [6] misconception, exact rule:** wrong rule: 2 + 3 + "bc" and "bc" + 2 + 3 give the same text. Right rule: + is evaluated left to right: 2 + 3 + "bc" is "5bc" but "bc" + 2 + 3 is "bc23".
- **Edge `string_concatenation` &rarr; `StringPlusLeftToRight`, exact edge logic:** 2 + 3 + "bc" and "bc" + 2 + 3 give the same text. **Twin logic:** + is evaluated left to right: 2 + 3 + "bc" is "5bc" but "bc" + 2 + 3 is "bc23". (role: context)
- **Edge `string_conversion` &rarr; `StringPlusLeftToRight`, exact edge logic:** 2 + 3 + "bc" and "bc" + 2 + 3 give the same text. **Twin logic:** + is evaluated left to right: 2 + 3 + "bc" is "5bc" but "bc" + 2 + 3 is "bc23". (role: primary)

### WrongOperatorOrder

- **Edge:** `operator_precedence` &rarr; `WrongOperatorOrder` (misconception)
- **Exact edge logic (the wrong rule):** G \* m1 \* m2 / r \* r divides by r squared.
- **Twin logic (the right rule):** \* and / are applied left to right, so it divides by r and then multiplies by r; use / (r \* r).
- **Wrong belief (on the node):** G \* m1 \* m2 / r \* r divides by r squared.
- **Correct rule (on the node):** \* and / are applied left to right, so it divides by r and then multiplies by r; use / (r \* r).
- **Provenance:** published
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [2] misconception, exact rule:** wrong rule: G \* m1 \* m2 / r \* r divides by r squared. Right rule: \* and / are applied left to right, so it divides by r and then multiplies by r; use / (r \* r).

## Errors (0)

An error edge states the rule that gets broken in a program, and the right rule.

The graph has no error edge from this concept.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for operator precedence: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to operator precedence agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

- **Edge:** `operator_precedence` &rarr; `operator_precedence@L0` (has_level)
- **Exact edge logic:** operator precedence -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (7 ways).

Ways (7), each with its exact rule:

- **[0] everyday\_reading** (rule type E, folk-meaning rule): School order of operations (PEMDAS/BODMAS) covers only arithmetic, so novices read other operators left to right as in English, or treat ^ as a power. Java's precedence table also places casts above \* / %, comparisons below + -, &amp;&amp; above \|\|, and = lowest.
- **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `ArithmeticPlusPrecedes`: wrong rule: arithmetic + binds tighter than string-concatenation +. Right rule: Both uses of + have the same precedence and are evaluated left to right, so "s" + a + b joins a and then b as text; only "s" + (a + b) adds them first.
- **[2] misconception** (rule type M, wrong rule / right rule) &rarr; `WrongOperatorOrder`: wrong rule: G \* m1 \* m2 / r \* r divides by r squared. Right rule: \* and / are applied left to right, so it divides by r and then multiplies by r; use / (r \* r).
- **[3] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `ArithmeticPlusPrecedes`: Points to LT (group by precedence, then left to right for operators of equal precedence). Applied unevenly, a student applies \* before + in one place but reads G \* m1 \* m2 / r \* r as dividing by r squared. (here mixing in: "arithmetic + binds tighter than string-concatenation +")
- **[4] misconception** (rule type M, wrong rule / right rule) &rarr; `BooleanPrecedence`: wrong rule: a \|\| b &amp;&amp; c is evaluated left to right as (a \|\| b) &amp;&amp; c. Right rule: &amp;&amp; binds tighter than \|\|, so it is a \|\| (b &amp;&amp; c).
- **[5] misconception** (rule type M, wrong rule / right rule) &rarr; `CastAppliesToWholeExpression`: wrong rule: (int) 2.5 / 0.15 casts the whole quotient to int. Right rule: The cast applies only to what comes right after it, here 2.5.
- **[6] misconception** (rule type M, wrong rule / right rule) &rarr; `StringPlusLeftToRight`: wrong rule: 2 + 3 + "bc" and "bc" + 2 + 3 give the same text. Right rule: + is evaluated left to right: 2 + 3 + "bc" is "5bc" but "bc" + 2 + 3 is "bc23".

### L1: Unistructural / atom x text surface

L1 for operator precedence: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

- **Edge:** `operator_precedence` &rarr; `operator_precedence@L1` (has_level)
- **Exact edge logic:** operator precedence -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

Ways (2), each with its exact rule:

- **[0] names\_the\_element** (rule type N, identity rule): Operator precedence (order of operations): the rules that decide which operator binds its operands first, with associativity breaking ties.
- **[1] states\_the\_rule** (rule type S, declarative rule): \* / % bind before + -, and operators of equal precedence group left to right (a-b-c is (a-b)-c). Casts bind tighter than arithmetic, comparisons are below arithmetic and above &amp;&amp; and \|\|, and parentheses override everything. Operators of equal precedence are applied left to right: a-b-c is (a-b)-c, 1 + 2 + "Hello" is "3Hello" but "Hello" + 1 + 2 is "Hello12".

### L2: Multistructural / block x execution / preoperational

L2 for operator precedence: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

- **Edge:** `operator_precedence` &rarr; `operator_precedence@L2` (has_level)
- **Exact edge logic:** operator precedence -&gt; L2 (Multistructural): the answer applies the rules of operator precedence to every part of the code, in order (3 ways).

Ways (3), each with its exact rule:

- **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): Grouping is fixed first: innermost parentheses, then casts and unary operators, \* / %, + -, comparisons, &amp;&amp;, \|\|, and finally =. Within a level grouping goes left to right, and operands are then evaluated left to right inside that grouping.
- **[1] output\_prediction** (rule type OP, evaluation / result rule): 1 + 2 \* 3 is 7. 3 + 5 / 2 is 5. 3 - 5 - 2 is -4. 2 + 3 + "bc" is "5bc" but "bc" + 2 + 3 is "bc23".
- **[2] one\_step\_execution** (rule type OS, state-transition rule): Precedence changes no variable. It only decides which intermediate value is computed next: in minute \* 100 / 60 with minute = 59, 5900 is computed before the division.

### L3: Relational / relations x function (concrete operational begins)

L3 for operator precedence: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

- **Edge:** `operator_precedence` &rarr; `operator_precedence@L3` (has_level)
- **Exact edge logic:** operator precedence -&gt; L3 (Relational): the answer relates the parts (2 ways).

Ways (2), each with its exact rule:

- **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Precedence decides the grouping of a multi-operator expression, and a parenthesized subexpression is evaluated as one unit with its own value.
- **[1] purpose\_of\_the\_whole** (rule type P, plan / role rule): Precedence lets compact formulas read like maths notation. Programmers add parentheses to state the intended grouping, e.g. (a + b) / 2 for an average.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for operator precedence: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

- **Edge:** `operator_precedence` &rarr; `operator_precedence@L4` (has_level)
- **Exact edge logic:** operator precedence -&gt; L4 (Extended abstract): the answer reasons beyond the given code (5 ways).

Ways (5), each with its exact rule:

- **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `ArithmeticPlusPrecedes`: Adding parentheses that match precedence keeps the value ((minute \* 100) / 60). Parentheses that change the grouping change it (3 - (5 - 2) is 0, not -4). Reordering equal-precedence int operations can also change it (59 / 60 \* 100 is 0).
- **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Rely on precedence for ordinary arithmetic. Add parentheses whenever the expression mixes levels that readers may not know (casts, &amp;&amp; with \|\|, + with Strings, chains of \* and /). Break very long formulas into named intermediate variables.
- **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: \* and / have equal precedence and group left to right; + binds weaker than / . Kind: silent logic error. Trigger class: Maths formulas typed without parentheses: G \* m1 \* m2 / r \* r, (a + b / 2) for an average, or x / 2 \* pi.
- **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: Comparisons yield booleans, and &lt; is not defined between a boolean and an int. Kind: compile-time. Trigger class: Chained comparisons such as a &lt; b &lt; c: 'bad operand types for binary operator &lt;'.
- **[4] diagnose\_an\_error** (rule type D, error rule): rule broken: + groups left to right, so once a String appears, later + operators concatenate. Kind: silent logic error. Trigger class: Printing "sum: " + a + b without parentheses around a + b.

## Same topic

`operator_precedence` belongs to the topic **Data types and terminology (literals, identifiers, variables, declarations, assignment, expressions)** (`topic1.2.a`). The topic also contains: `assignment`, `chained_assignment`, `data_type`, `declaration`, `definite_assignment`, `expression`, `identifier`, `literal`, `named_constants`, `naming_convention`, `primitive_type`, `program_trace`, `variable`, `variable_swap`.

## Rules of the concept (19)

- **Book** (SW-1e, p. 17 (pdf 27)): "When arithmetic operators have the same precedence, the order is determined by left-associativity, so that a-b-c and (a-b)-c represent the same sequence of operations."
- **Book** (OT-Expressions, ): "Operators that have a higher precedence get evaluated first."
- **Book** (OT-Expressions, ): "When writing compound expressions, be explicit and indicate with parentheses which operators should be evaluated first."
- **E** (folk-meaning rule): School order of operations (PEMDAS/BODMAS) covers only arithmetic, so novices read other operators left to right as in English, or treat ^ as a power. Java's precedence table also places casts above \* / %, comparisons below + -, &amp;&amp; above \|\|, and = lowest.
- **M** (wrong rule / right rule): ArithmeticPlusPrecedes: wrong: arithmetic + binds tighter than string-concatenation + \| right: Both uses of + have the same precedence and are evaluated left to right, so "s" + a + b joins a and then b as text; only "s" + (a + b) adds them first.
- **M** (wrong rule / right rule): BooleanPrecedence: wrong: a \|\| b &amp;&amp; c is evaluated left to right as (a \|\| b) &amp;&amp; c. \| right: &amp;&amp; binds tighter than \|\|, so it is a \|\| (b &amp;&amp; c).
- **M** (wrong rule / right rule): CastAppliesToWholeExpression: wrong: (int) 2.5 / 0.15 casts the whole quotient to int. \| right: The cast applies only to what comes right after it, here 2.5.
- **M** (wrong rule / right rule): StringPlusLeftToRight: wrong: 2 + 3 + "bc" and "bc" + 2 + 3 give the same text. \| right: + is evaluated left to right: 2 + 3 + "bc" is "5bc" but "bc" + 2 + 3 is "bc23".
- **M** (wrong rule / right rule): WrongOperatorOrder: wrong: G \* m1 \* m2 / r \* r divides by r squared. \| right: \* and / are applied left to right, so it divides by r and then multiplies by r; use / (r \* r).
- **T** (uneven-application rule): Points to LT (group by precedence, then left to right for operators of equal precedence). Applied unevenly, a student applies \* before + in one place but reads G \* m1 \* m2 / r \* r as dividing by r squared.
- **N** (identity rule): Operator precedence (order of operations): the rules that decide which operator binds its operands first, with associativity breaking ties.
- **S** (declarative rule): \* / % bind before + -, and operators of equal precedence group left to right (a-b-c is (a-b)-c). Casts bind tighter than arithmetic, comparisons are below arithmetic and above &amp;&amp; and \|\|, and parentheses override everything. Operators of equal precedence are applied left to right: a-b-c is (a-b)-c, 1 + 2 + "Hello" is "3Hello" but "Hello" + 1 + 2 is "Hello12".
- **LT** (operational sequencing rule): Grouping is fixed first: innermost parentheses, then casts and unary operators, \* / %, + -, comparisons, &amp;&amp;, \|\|, and finally =. Within a level grouping goes left to right, and operands are then evaluated left to right inside that grouping.
- **OP** (evaluation / result rule): 1 + 2 \* 3 is 7. 3 + 5 / 2 is 5. 3 - 5 - 2 is -4. 2 + 3 + "bc" is "5bc" but "bc" + 2 + 3 is "bc23".
- **OS** (state-transition rule): Precedence changes no variable. It only decides which intermediate value is computed next: in minute \* 100 / 60 with minute = 59, 5900 is computed before the division.
- **R** (composition rule (with a neighbour)): with expression: Precedence decides the grouping of a multi-operator expression, and a parenthesized subexpression is evaluated as one unit with its own value.
- **P** (plan / role rule): Precedence lets compact formulas read like maths notation. Programmers add parentheses to state the intended grouping, e.g. (a + b) / 2 for an average.
- **C** (conservation rule): Adding parentheses that match precedence keeps the value ((minute \* 100) / 60). Parentheses that change the grouping change it (3 - (5 - 2) is 0, not -4). Reordering equal-precedence int operations can also change it (59 / 60 \* 100 is 0).
- **D** (error rule): rule broken: \* and / have equal precedence and group left to right; + binds weaker than / . (silent logic error)
- **D** (error rule): rule broken: Comparisons yield booleans, and &lt; is not defined between a boolean and an int. (compile-time)
- **D** (error rule): rule broken: + groups left to right, so once a String appears, later + operators concatenate. (silent logic error)
- **X** (applicability rule): Rely on precedence for ordinary arithmetic. Add parentheses whenever the expression mixes levels that readers may not know (casts, &amp;&amp; with \|\|, + with Strings, chains of \* and /). Break very long formulas into named intermediate variables.

## How it is found in code and answers (reader block)

- **Aliases:** precedence, order of operations
- **Code patterns:** `\w\s*[+\-]\s*\w+\s*[*/%]\s*\w`, `\w\s*[*/%]\s*\w+\s*[+\-]\s*\w`, `[*/%]\s*\w+\s*(?:==|!=|[<>]=?)\s*\w+\s*(?:&&|\|\|)`, `(?:==|!=|[<>]=?)\s*\w+\s*(?:&&|\|\|)\s*\w+\s*(?:==|!=|[<>]=?)`, `\(\s*\w+\s*[+\-]\s*\w+\s*\)\s*[*/%]|[*/%]\s*\(\s*\w+\s*[+\-]\s*\w+\s*\)`, `\w\s*[*/%]\s*\w+\s*[*/%]\s*\w`
- **Operator symbols:** none
- **Java types:** none

## The whole prerequisite chain

- **Everything it builds on (7):** `arithmetic_operators`, `data_type`, `expression`, `identifier`, `literal`, `primitive_type`, `variable`
- **Everything that builds on it (0):** nothing

## Every edge in this view and its exact edge logic (32)

All the edges drawn in the picture, in the order: prerequisite, parallel, misconception, error, has_level, contains.

**1. `expression` &rarr; `operator_precedence`** (prerequisite)

- **Exact edge logic:** When an expression has several operators, precedence decides which operands are combined first, and equal-precedence operators go left to right.
- **Grounding:** book\_passage
- **Composition rule (R) of `expression` with `operator_precedence`:** With several operators, precedence and left associativity decide the grouping, and parentheses override both.
- **Composition rule (R) of `operator_precedence` with `expression`:** Precedence decides the grouping of a multi-operator expression, and a parenthesized subexpression is evaluated as one unit with its own value.

**2. `operator_precedence` &rarr; `ArithmeticPlusPrecedes`** (misconception)

- **Exact edge logic (the wrong rule):** In "s" + a + b, the numbers a and b are added first and their sum is joined to s.
- **Twin logic (the right rule):** Both uses of + have the same precedence and are evaluated left to right, so "s" + a + b joins a and then b as text; only "s" + (a + b) adds them first.
- **Role:** context

**3. `operator_precedence` &rarr; `BooleanPrecedence`** (misconception)

- **Exact edge logic (the wrong rule):** a \|\| b &amp;&amp; c is evaluated left to right as (a \|\| b) &amp;&amp; c.
- **Twin logic (the right rule):** &amp;&amp; binds tighter than \|\|, so it is a \|\| (b &amp;&amp; c).
- **Role:** context

**4. `operator_precedence` &rarr; `CastAppliesToWholeExpression`** (misconception)

- **Exact edge logic (the wrong rule):** (int) 2.5 / 0.15 casts the whole quotient to int.
- **Twin logic (the right rule):** The cast applies only to what comes right after it, here 2.5.
- **Role:** context

**5. `operator_precedence` &rarr; `MissingClarifyingParentheses`** (misconception)

- **Exact edge logic (the wrong rule):** Writes compound expressions such as a + b \* c / d - e % f with no parentheses, relying on the reader to know precedence.
- **Twin logic (the right rule):** When writing compound expressions, be explicit and indicate with parentheses which operators should be evaluated first.
- **Role:** primary

**6. `operator_precedence` &rarr; `StringPlusLeftToRight`** (misconception)

- **Exact edge logic (the wrong rule):** 2 + 3 + "bc" and "bc" + 2 + 3 give the same text.
- **Twin logic (the right rule):** + is evaluated left to right: 2 + 3 + "bc" is "5bc" but "bc" + 2 + 3 is "bc23".
- **Role:** context

**7. `operator_precedence` &rarr; `WrongOperatorOrder`** (misconception)

- **Exact edge logic (the wrong rule):** G \* m1 \* m2 / r \* r divides by r squared.
- **Twin logic (the right rule):** \* and / are applied left to right, so it divides by r and then multiplies by r; use / (r \* r).
- **Role:** primary

**8. `explicit_cast` &rarr; `CastAppliesToWholeExpression`** (misconception)

- **Exact edge logic (the wrong rule):** (int) 2.5 / 0.15 casts the whole quotient to int.
- **Twin logic (the right rule):** The cast applies only to what comes right after it, here 2.5.
- **Role:** primary

**9. `logical_operators` &rarr; `BooleanPrecedence`** (misconception)

- **Exact edge logic (the wrong rule):** a \|\| b &amp;&amp; c is evaluated left to right as (a \|\| b) &amp;&amp; c.
- **Twin logic (the right rule):** &amp;&amp; binds tighter than \|\|, so it is a \|\| (b &amp;&amp; c).
- **Role:** primary

**10. `string_concatenation` &rarr; `ArithmeticPlusPrecedes`** (misconception)

- **Exact edge logic (the wrong rule):** In "s" + a + b, the numbers a and b are added first and their sum is joined to s.
- **Twin logic (the right rule):** Both uses of + have the same precedence and are evaluated left to right, so "s" + a + b joins a and then b as text; only "s" + (a + b) adds them first.
- **Role:** primary

**11. `string_concatenation` &rarr; `StringPlusLeftToRight`** (misconception)

- **Exact edge logic (the wrong rule):** 2 + 3 + "bc" and "bc" + 2 + 3 give the same text.
- **Twin logic (the right rule):** + is evaluated left to right: 2 + 3 + "bc" is "5bc" but "bc" + 2 + 3 is "bc23".
- **Role:** context

**12. `string_conversion` &rarr; `StringPlusLeftToRight`** (misconception)

- **Exact edge logic (the wrong rule):** 2 + 3 + "bc" and "bc" + 2 + 3 give the same text.
- **Twin logic (the right rule):** + is evaluated left to right: 2 + 3 + "bc" is "5bc" but "bc" + 2 + 3 is "bc23".
- **Role:** primary

**13. `operator_precedence` &rarr; `operator_precedence@L0`** (has_level)

- **Exact edge logic:** operator precedence -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (7 ways).
  - **[0] everyday\_reading** (rule type E, folk-meaning rule): School order of operations (PEMDAS/BODMAS) covers only arithmetic, so novices read other operators left to right as in English, or treat ^ as a power. Java's precedence table also places casts above \* / %, comparisons below + -, &amp;&amp; above \|\|, and = lowest.
  - **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `ArithmeticPlusPrecedes`: wrong rule: arithmetic + binds tighter than string-concatenation +. Right rule: Both uses of + have the same precedence and are evaluated left to right, so "s" + a + b joins a and then b as text; only "s" + (a + b) adds them first.
  - **[2] misconception** (rule type M, wrong rule / right rule) &rarr; `WrongOperatorOrder`: wrong rule: G \* m1 \* m2 / r \* r divides by r squared. Right rule: \* and / are applied left to right, so it divides by r and then multiplies by r; use / (r \* r).
  - **[3] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `ArithmeticPlusPrecedes`: Points to LT (group by precedence, then left to right for operators of equal precedence). Applied unevenly, a student applies \* before + in one place but reads G \* m1 \* m2 / r \* r as dividing by r squared. (here mixing in: "arithmetic + binds tighter than string-concatenation +")
  - **[4] misconception** (rule type M, wrong rule / right rule) &rarr; `BooleanPrecedence`: wrong rule: a \|\| b &amp;&amp; c is evaluated left to right as (a \|\| b) &amp;&amp; c. Right rule: &amp;&amp; binds tighter than \|\|, so it is a \|\| (b &amp;&amp; c).
  - **[5] misconception** (rule type M, wrong rule / right rule) &rarr; `CastAppliesToWholeExpression`: wrong rule: (int) 2.5 / 0.15 casts the whole quotient to int. Right rule: The cast applies only to what comes right after it, here 2.5.
  - **[6] misconception** (rule type M, wrong rule / right rule) &rarr; `StringPlusLeftToRight`: wrong rule: 2 + 3 + "bc" and "bc" + 2 + 3 give the same text. Right rule: + is evaluated left to right: 2 + 3 + "bc" is "5bc" but "bc" + 2 + 3 is "bc23".

**14. `operator_precedence` &rarr; `operator_precedence@L1`** (has_level)

- **Exact edge logic:** operator precedence -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).
  - **[0] names\_the\_element** (rule type N, identity rule): Operator precedence (order of operations): the rules that decide which operator binds its operands first, with associativity breaking ties.
  - **[1] states\_the\_rule** (rule type S, declarative rule): \* / % bind before + -, and operators of equal precedence group left to right (a-b-c is (a-b)-c). Casts bind tighter than arithmetic, comparisons are below arithmetic and above &amp;&amp; and \|\|, and parentheses override everything. Operators of equal precedence are applied left to right: a-b-c is (a-b)-c, 1 + 2 + "Hello" is "3Hello" but "Hello" + 1 + 2 is "Hello12".

**15. `operator_precedence` &rarr; `operator_precedence@L2`** (has_level)

- **Exact edge logic:** operator precedence -&gt; L2 (Multistructural): the answer applies the rules of operator precedence to every part of the code, in order (3 ways).
  - **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): Grouping is fixed first: innermost parentheses, then casts and unary operators, \* / %, + -, comparisons, &amp;&amp;, \|\|, and finally =. Within a level grouping goes left to right, and operands are then evaluated left to right inside that grouping.
  - **[1] output\_prediction** (rule type OP, evaluation / result rule): 1 + 2 \* 3 is 7. 3 + 5 / 2 is 5. 3 - 5 - 2 is -4. 2 + 3 + "bc" is "5bc" but "bc" + 2 + 3 is "bc23".
  - **[2] one\_step\_execution** (rule type OS, state-transition rule): Precedence changes no variable. It only decides which intermediate value is computed next: in minute \* 100 / 60 with minute = 59, 5900 is computed before the division.

**16. `operator_precedence` &rarr; `operator_precedence@L3`** (has_level)

- **Exact edge logic:** operator precedence -&gt; L3 (Relational): the answer relates the parts (2 ways).
  - **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Precedence decides the grouping of a multi-operator expression, and a parenthesized subexpression is evaluated as one unit with its own value.
  - **[1] purpose\_of\_the\_whole** (rule type P, plan / role rule): Precedence lets compact formulas read like maths notation. Programmers add parentheses to state the intended grouping, e.g. (a + b) / 2 for an average.

**17. `operator_precedence` &rarr; `operator_precedence@L4`** (has_level)

- **Exact edge logic:** operator precedence -&gt; L4 (Extended abstract): the answer reasons beyond the given code (5 ways).
  - **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `ArithmeticPlusPrecedes`: Adding parentheses that match precedence keeps the value ((minute \* 100) / 60). Parentheses that change the grouping change it (3 - (5 - 2) is 0, not -4). Reordering equal-precedence int operations can also change it (59 / 60 \* 100 is 0).
  - **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Rely on precedence for ordinary arithmetic. Add parentheses whenever the expression mixes levels that readers may not know (casts, &amp;&amp; with \|\|, + with Strings, chains of \* and /). Break very long formulas into named intermediate variables.
  - **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: \* and / have equal precedence and group left to right; + binds weaker than / . Kind: silent logic error. Trigger class: Maths formulas typed without parentheses: G \* m1 \* m2 / r \* r, (a + b / 2) for an average, or x / 2 \* pi.
  - **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: Comparisons yield booleans, and &lt; is not defined between a boolean and an int. Kind: compile-time. Trigger class: Chained comparisons such as a &lt; b &lt; c: 'bad operand types for binary operator &lt;'.
  - **[4] diagnose\_an\_error** (rule type D, error rule): rule broken: + groups left to right, so once a String appears, later + operators concatenate. Kind: silent logic error. Trigger class: Printing "sum: " + a + b without parentheses around a + b.

**18. `topic1.2.a` &rarr; `operator_precedence`** (contains)

- topic `topic1.2.a` contains `operator_precedence`

**19. `topic1.2.a` &rarr; `assignment`** (contains)

- topic `topic1.2.a` contains `assignment`

**20. `topic1.2.a` &rarr; `chained_assignment`** (contains)

- topic `topic1.2.a` contains `chained_assignment`

**21. `topic1.2.a` &rarr; `data_type`** (contains)

- topic `topic1.2.a` contains `data_type`

**22. `topic1.2.a` &rarr; `declaration`** (contains)

- topic `topic1.2.a` contains `declaration`

**23. `topic1.2.a` &rarr; `definite_assignment`** (contains)

- topic `topic1.2.a` contains `definite_assignment`

**24. `topic1.2.a` &rarr; `expression`** (contains)

- topic `topic1.2.a` contains `expression`

**25. `topic1.2.a` &rarr; `identifier`** (contains)

- topic `topic1.2.a` contains `identifier`

**26. `topic1.2.a` &rarr; `literal`** (contains)

- topic `topic1.2.a` contains `literal`

**27. `topic1.2.a` &rarr; `named_constants`** (contains)

- topic `topic1.2.a` contains `named_constants`

**28. `topic1.2.a` &rarr; `naming_convention`** (contains)

- topic `topic1.2.a` contains `naming_convention`

**29. `topic1.2.a` &rarr; `primitive_type`** (contains)

- topic `topic1.2.a` contains `primitive_type`

**30. `topic1.2.a` &rarr; `program_trace`** (contains)

- topic `topic1.2.a` contains `program_trace`

**31. `topic1.2.a` &rarr; `variable`** (contains)

- topic `topic1.2.a` contains `variable`

**32. `topic1.2.a` &rarr; `variable_swap`** (contains)

- topic `topic1.2.a` contains `variable_swap`
