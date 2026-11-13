# comparison_operators (`comparison_operators`)

== != &lt; &gt; &lt;= &gt;=

Section 1.2 Built-in Types of Data, topic 1.2.f Comparisons.

![The knowledge graph around comparison_operators](comparison_operators.png)

## At a glance

- **Needs first:** `boolean`, `expression`
- **Leads to:** `boolean_expression`
- **Learned alongside:** `assignment`, `logical_operators`
- **Misconceptions:** `AssignCompares`, `ChainedComparison`, `ComparisonWithBooleanLiteral`, `EqualityOperatorComparesObjectsValues`, `EqualsComparesReferences`, `LessGreaterSwapped`, `StringRelationalComparison`
- **Errors:** `ReversedRelationalOperator`
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 29 edges around this concept. The edge logic, the wrong and right rules and the exact rules of the ways are copied word for word from the graph.

## To work on (0)

Nothing is missing for this concept.

## What it needs first (2)

A prerequisite edge means the other concept has to be understood before `comparison_operators`.

### `boolean` comes before `comparison_operators`

*true/false primitive*

- **Edge:** `pre:boolean->comparison_operators`
- **Exact edge logic:** A comparison such as a &lt; b takes two numbers and produces a boolean result.
- **Grounding:** book\_passage
- **Composition rule (R) of `comparison_operators` with `boolean`:** Comparisons take numbers and produce a boolean; boolean values themselves can be compared only with == and != (not &lt;), and testing them against true is unnecessary.
- **Composition rule (R) of `boolean` with `comparison_operators`:** Comparisons are the main producers of boolean values: they take two numbers and return true or false, which can then be stored in a boolean variable.

### `expression` comes before `comparison_operators`

*anything that evaluates to a value*

- **Edge:** `pre:expression->comparison_operators`
- **Exact edge logic:** Comparison operators build expressions whose value is a boolean, so one must already know what an expression is to understand a &lt; b.
- **Grounding:** order\_only
- **Composition rule (R) of `comparison_operators` with `expression`:** A comparison is itself an expression whose value is a boolean, so it can appear anywhere a boolean is needed, including on the right of an assignment (boolean ok = x &gt; y;).
- **Composition rule (R) of `expression` with `comparison_operators`:** A comparison takes numeric expressions and yields a boolean expression, and it has lower precedence than arithmetic, so a + b &lt; c compares the sum.

## What it leads to (1)

These concepts need `comparison_operators` first.

### `comparison_operators` comes before `boolean_expression`

*an expression that evaluates to true/false*

- **Edge:** `pre:comparison_operators->boolean_expression`
- **Exact edge logic:** A comparison such as x &lt; y produces a boolean result; comparisons together with boolean logic provide the basis for decision-making.
- **Grounding:** book\_passage
- **Composition rule (R) of `comparison_operators` with `boolean_expression`:** Comparisons are the building blocks of conditions: together with boolean logic they provide the basis for decision-making.
- **Composition rule (R) of `boolean_expression` with `comparison_operators`:** Comparisons are the atoms of boolean expressions; because they bind tighter than &amp;&amp; and \|\|, month &gt;= 1 &amp;&amp; month &lt;= 12 groups as (month &gt;= 1) &amp;&amp; (month &lt;= 12) without parentheses.

## Learned alongside (2)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

### `comparison_operators` alongside `assignment`

*= stores the computed value of the right side*

- **Edge:** `par:assignment~comparison_operators`
- **Exact edge logic:** x = y stores the value of y in x (a statement with a side effect); x == y only tests whether the two values are equal and gives a boolean. Writing = where == is meant is a compile error with int operands and a silent bug with boolean operands.
- **Grounding:** book\_passage

### `comparison_operators` alongside `logical_operators`

*&amp;&amp; \|\| !*

- **Edge:** `par:comparison_operators~logical_operators`
- **Exact edge logic:** Relational operators compare two numbers to give a boolean; logical operators combine booleans into one boolean.
- **Grounding:** book\_passage
- **Composition rule (R) of `comparison_operators` with `logical_operators`:** Comparisons bind tighter than &amp;&amp; and \|\|, so they are evaluated first and logical operators combine their boolean results.
- **Composition rule (R) of `logical_operators` with `comparison_operators`:** Comparisons bind tighter than &amp;&amp; and \|\|, so comparisons are evaluated first and their boolean results are then combined (month &gt;= 1 &amp;&amp; month &lt;= 12).

## Misconceptions (7)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### AssignCompares

- **Edge:** `comparison_operators` &rarr; `AssignCompares` (misconception)
- **Exact edge logic (the wrong rule):** = compares two values instead of assigning
- **Twin logic (the right rule):** x = y copies the value of y into x; x == y is what compares them.
- **Wrong belief (on the node):** = compares two values instead of assigning
- **Correct rule (on the node):** x = y copies the value of y into x; x == y is what compares them.
- **Provenance:** published
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [6] misconception, exact rule:** wrong rule: = compares two values instead of assigning. Right rule: x = y copies the value of y into x; x == y is what compares them and produces a boolean.
- **Edge `assignment` &rarr; `AssignCompares`, exact edge logic:** x = y checks whether x and y are equal. **Twin logic:** x = y copies the value of y into x; x == y is what compares them. (role: primary)
- **Edge `if_statement` &rarr; `AssignCompares`, exact edge logic:** = compares two values instead of assigning **Twin logic:** x = y copies the value of y into x; x == y is what compares them. (role: context)

### ChainedComparison

- **Edge:** `comparison_operators` &rarr; `ChainedComparison` (misconception)
- **Exact edge logic (the wrong rule):** 90 &lt;= grade &lt;= 100 tests whether grade is between 90 and 100.
- **Twin logic (the right rule):** a &lt; b &lt; c does not compile (a &lt; b is a boolean); a range test is written 90 &lt;= grade &amp;&amp; grade &lt;= 100.
- **Wrong belief (on the node):** 90 &lt;= grade &lt;= 100 tests whether grade is between 90 and 100.
- **Correct rule (on the node):** a &lt; b &lt; c does not compile (a &lt; b is a boolean); a range test is written 90 &lt;= grade &amp;&amp; grade &lt;= 100.
- **Provenance:** textbook
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [1] misconception, exact rule:** wrong rule: 90 &lt;= grade &lt;= 100 tests whether grade is between 90 and 100. Right rule: a &lt; b &lt; c does not compile (a &lt; b is a boolean); a range test is written 90 &lt;= grade &amp;&amp; grade &lt;= 100.
- **L0 way [5] inconsistent\_trace, exact rule:** Points to LT (evaluate both operands, promote to a common type, then compare). Applied unevenly: the student treats &lt; as &lt;= on the boundary pass of a loop, or compares an int with a double as ints on one line and as doubles on another. (here mixing in: "90 &lt;= grade &lt;= 100 tests whether grade is between 90 and 100")
- **Edge `boolean_expression` &rarr; `ChainedComparison`, exact edge logic:** 90 &lt;= grade &lt;= 100 tests whether grade is between 90 and 100. **Twin logic:** a &lt; b &lt; c does not compile (a &lt; b is a boolean); a range test is written 90 &lt;= grade &amp;&amp; grade &lt;= 100. (role: context)

### ComparisonWithBooleanLiteral

- **Edge:** `comparison_operators` &rarr; `ComparisonWithBooleanLiteral` (misconception)
- **Exact edge logic (the wrong rule):** you must write == true / == false to test a boolean
- **Twin logic (the right rule):** if (b) already tests b, so writing == true adds nothing.
- **Wrong belief (on the node):** you must write == true / == false to test a boolean
- **Correct rule (on the node):** if (b) already tests b, so writing == true adds nothing.
- **Provenance:** published
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [7] misconception, exact rule:** wrong rule: You must write == true / == false to test a boolean. Right rule: if (b) already tests b, so writing == true adds nothing.
- **Edge `boolean_expression` &rarr; `ComparisonWithBooleanLiteral`, exact edge logic:** To test a boolean b you must write if (b == true). **Twin logic:** if (b) already tests b, so writing == true adds nothing. (role: primary)

### EqualityOperatorComparesObjectsValues

- **Edge:** `comparison_operators` &rarr; `EqualityOperatorComparesObjectsValues` (misconception)
- **Exact edge logic (the wrong rule):** s == t is true whenever the two Strings contain the same text.
- **Twin logic (the right rule):** s == t is true only when s and t refer to the same object; s.equals(t) compares the text.
- **Wrong belief (on the node):** == compares contents (the String == bug)
- **Correct rule (on the node):** s == t is true only when s and t refer to the same object; s.equals(t) compares the text.
- **Provenance:** published
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [2] misconception, exact rule:** wrong rule: == compares the contents of two Strings. Right rule: s == t is true only when s and t refer to the same object; "abc" == "ab" + x is false even when x is "c"; s.equals(t) compares the text.
- **Edge `primitive_vs_reference` &rarr; `EqualityOperatorComparesObjectsValues`, exact edge logic:** == compares contents (the String == bug) **Twin logic:** s == t is true only when s and t refer to the same object; s.equals(t) compares the text. (role: context)
- **Edge `string_type` &rarr; `EqualityOperatorComparesObjectsValues`, exact edge logic:** s == t is true whenever the two Strings contain the same text. **Twin logic:** s == t is true only when s and t refer to the same object; s.equals(t) compares the text. (role: context)

### EqualsComparesReferences

- **Edge:** `comparison_operators` &rarr; `EqualsComparesReferences` (misconception)
- **Exact edge logic (the wrong rule):** .equals() compares references, not contents
- **Twin logic (the right rule):** s.equals(t) checks whether the two Strings contain the same characters.
- **Wrong belief (on the node):** .equals() compares references, not contents
- **Correct rule (on the node):** s.equals(t) checks whether the two Strings contain the same characters.
- **Provenance:** published
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [8] misconception, exact rule:** wrong rule: .equals() compares references, not contents. Right rule: s.equals(t) checks whether the two Strings contain the same characters; it is == that compares references.
- **Edge `method_call` &rarr; `EqualsComparesReferences`, exact edge logic:** .equals() compares references, not contents **Twin logic:** s.equals(t) checks whether the two Strings contain the same characters. (role: context)
- **Edge `string_type` &rarr; `EqualsComparesReferences`, exact edge logic:** s.equals(t) checks whether s and t are the same object. **Twin logic:** s.equals(t) checks whether the two Strings contain the same characters. (role: primary)

### LessGreaterSwapped

- **Edge:** `comparison_operators` &rarr; `LessGreaterSwapped` (misconception)
- **Exact edge logic (the wrong rule):** &lt; and &gt; mean the same thing (or a &lt; b means a is greater than b).
- **Twin logic (the right rule):** a &lt; b is true when a is smaller than b; a &gt; b when a is larger.
- **Wrong belief (on the node):** &lt; and &gt; mean the same thing (or a &lt; b means a is greater than b).
- **Correct rule (on the node):** a &lt; b is true when a is smaller than b; a &gt; b when a is larger.
- **Provenance:** published
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [4] misconception, exact rule:** wrong rule: &lt; and &gt; mean the same thing (or a &lt; b means a is greater than b). Right rule: a &lt; b is true when a is smaller than b; a &gt; b when a is larger.
- **Edge `loop_guard` &rarr; `LessGreaterSwapped`, exact edge logic:** &lt; and &gt; mean the same thing (or a &lt; b means a is greater than b). **Twin logic:** a &lt; b is true when a is smaller than b; a &gt; b when a is larger. (role: context)

### StringRelationalComparison

- **Edge:** `comparison_operators` &rarr; `StringRelationalComparison` (misconception)
- **Exact edge logic (the wrong rule):** s &lt; t compares two Strings alphabetically.
- **Twin logic (the right rule):** &lt; and &gt; are defined only for primitive types; comparing Strings with them does not compile.
- **Wrong belief (on the node):** s &lt; t compares two Strings alphabetically.
- **Correct rule (on the node):** &lt; and &gt; are defined only for primitive types; comparing Strings with them does not compile.
- **Provenance:** textbook
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [3] misconception, exact rule:** wrong rule: s &lt; t compares two Strings alphabetically. Right rule: &lt; and &gt; are defined only for primitive types; comparing Strings with them does not compile (use s.compareTo(t)).
- **Edge `string_type` &rarr; `StringRelationalComparison`, exact edge logic:** s &lt; t compares two Strings alphabetically. **Twin logic:** &lt; and &gt; are defined only for primitive types; comparing Strings with them does not compile. (role: context)

## Errors (1)

An error edge states the rule that gets broken in a program, and the right rule.

### ReversedRelationalOperator

- **Edge:** `comparison_operators` &rarr; `ReversedRelationalOperator` (error)
- **Exact edge logic (the wrong rule):** Writes =&lt; or =&gt; instead of &lt;= and &gt;=.
- **Twin logic (the right rule):** The operators are written &lt;= and &gt;=.
- **Wrong belief (on the node):** Writes =&lt; or =&gt; instead of &lt;= and &gt;=.
- **Correct rule (on the node):** The operators are written &lt;= and &gt;=.
- **Provenance:** published
- **Role of this concept:** primary

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for comparison operators: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to comparison operators agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

- **Edge:** `comparison_operators` &rarr; `comparison_operators@L0` (has_level)
- **Exact edge logic:** comparison operators -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (9 ways).

Ways (9), each with its exact rule:

- **[0] everyday\_reading** (rule type E, folk-meaning rule): Folk meaning: in maths = states that two things are equal, and inequalities can be chained (a &lt; b &lt; c) or spoken as 'equal or less than' (=&lt;). Java rule: = assigns while == compares; the operators are spelled &lt;= and &gt;= only; a &lt; b &lt; c does not compile; and on Strings == compares references.
- **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `ChainedComparison`: wrong rule: 90 &lt;= grade &lt;= 100 tests whether grade is between 90 and 100. Right rule: a &lt; b &lt; c does not compile (a &lt; b is a boolean); a range test is written 90 &lt;= grade &amp;&amp; grade &lt;= 100.
- **[2] misconception** (rule type M, wrong rule / right rule) &rarr; `EqualityOperatorComparesObjectsValues`: wrong rule: == compares the contents of two Strings. Right rule: s == t is true only when s and t refer to the same object; "abc" == "ab" + x is false even when x is "c"; s.equals(t) compares the text.
- **[3] misconception** (rule type M, wrong rule / right rule) &rarr; `StringRelationalComparison`: wrong rule: s &lt; t compares two Strings alphabetically. Right rule: &lt; and &gt; are defined only for primitive types; comparing Strings with them does not compile (use s.compareTo(t)).
- **[4] misconception** (rule type M, wrong rule / right rule) &rarr; `LessGreaterSwapped`: wrong rule: &lt; and &gt; mean the same thing (or a &lt; b means a is greater than b). Right rule: a &lt; b is true when a is smaller than b; a &gt; b when a is larger.
- **[5] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `ChainedComparison`: Points to LT (evaluate both operands, promote to a common type, then compare). Applied unevenly: the student treats &lt; as &lt;= on the boundary pass of a loop, or compares an int with a double as ints on one line and as doubles on another. (here mixing in: "90 &lt;= grade &lt;= 100 tests whether grade is between 90 and 100")
- **[6] misconception** (rule type M, wrong rule / right rule) &rarr; `AssignCompares`: wrong rule: = compares two values instead of assigning. Right rule: x = y copies the value of y into x; x == y is what compares them and produces a boolean.
- **[7] misconception** (rule type M, wrong rule / right rule) &rarr; `ComparisonWithBooleanLiteral`: wrong rule: You must write == true / == false to test a boolean. Right rule: if (b) already tests b, so writing == true adds nothing.
- **[8] misconception** (rule type M, wrong rule / right rule) &rarr; `EqualsComparesReferences`: wrong rule: .equals() compares references, not contents. Right rule: s.equals(t) checks whether the two Strings contain the same characters; it is == that compares references.

### L1: Unistructural / atom x text surface

L1 for comparison operators: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

- **Edge:** `comparison_operators` &rarr; `comparison_operators@L1` (has_level)
- **Exact edge logic:** comparison operators -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

Ways (2), each with its exact rule:

- **[0] names\_the\_element** (rule type N, identity rule): Comparison (relational) operators ==, !=, &lt;, &lt;=, &gt;, &gt;= are mixed-type operators: they take two operands of a numeric type and produce a boolean.
- **[1] states\_the\_rule** (rule type S, declarative rule): ==, !=, &lt;, &lt;=, &gt;, &gt;= are defined for each primitive numeric type and produce a boolean; they have lower precedence than arithmetic and higher than boolean operators; &lt; and &gt; are not defined for Strings, and == on non-primitive types compares identity.

### L2: Multistructural / block x execution / preoperational

L2 for comparison operators: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

- **Edge:** `comparison_operators` &rarr; `comparison_operators@L2` (has_level)
- **Exact edge logic:** comparison operators -&gt; L2 (Multistructural): the answer applies the rules of comparison operators to every part of the code, in order (3 ways).

Ways (3), each with its exact rule:

- **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): Evaluate the left operand (including its arithmetic), then the right operand; if their types differ, promote the narrower one (int to double); then compare and produce true or false.
- **[1] output\_prediction** (rule type OP, evaluation / result rule): The result is a boolean: (2 &lt;= 2) is true, 2 &lt; 2 is false, (x &lt; 3.1) is true for int x = 3; any comparison involving NaN, even NaN == NaN, is false.
- **[2] one\_step\_execution** (rule type OS, state-transition rule): A comparison changes no variable and only returns a boolean, unlike =, which changes the value of the variable on its left.

### L3: Relational / relations x function (concrete operational begins)

L3 for comparison operators: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

- **Edge:** `comparison_operators` &rarr; `comparison_operators@L3` (has_level)
- **Exact edge logic:** comparison operators -&gt; L3 (Relational): the answer relates the parts (6 ways).

Ways (6), each with its exact rule:

- **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): A comparison is itself an expression whose value is a boolean, so it can appear anywhere a boolean is needed, including on the right of an assignment (boolean ok = x &gt; y;).
- **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Comparisons are the building blocks of conditions: together with boolean logic they provide the basis for decision-making.
- **[2] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Comparisons bind tighter than &amp;&amp; and \|\|, so they are evaluated first and logical operators combine their boolean results.
- **[3] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Comparisons take numbers and produce a boolean; boolean values themselves can be compared only with == and != (not &lt;), and testing them against true is unnecessary.
- **[4] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): x = y stores the value of y in x (a statement with a side effect); x == y only tests whether the two values are equal and gives a boolean. Writing = where == is meant is a compile error with int operands and a silent bug with boolean operands.
- **[5] purpose\_of\_the\_whole** (rule type P, plan / role rule): Used to test a numeric condition: thresholds and sign checks, range tests, divisibility (n % k == 0), loop continuation (i &lt; N), sentinel checks, and running-extreme updates (if (x &gt; max) max = x).

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for comparison operators: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

- **Edge:** `comparison_operators` &rarr; `comparison_operators@L4` (has_level)
- **Exact edge logic:** comparison operators -&gt; L4 (Extended abstract): the answer reasons beyond the given code (7 ways).

Ways (7), each with its exact rule:

- **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `ChainedComparison`: Changing &lt; to &lt;= (or &gt; to &gt;=) changes the result only at the boundary value, which in a loop guard means one more or one fewer iteration (off-by-one); mirroring the comparison (a &lt; b to b &gt; a) preserves the value; negating it gives the complementary operator (!(a &lt; b) is a &gt;= b).
- **[1] diagnose\_an\_error** (rule type D, error rule): rule broken: The operators are written &lt;= and &gt;=. Kind: compile-time. Trigger class: Writing =&lt; or =&gt; (e.g. if (x =&gt; 0)).
- **[2] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Use comparison operators for numeric and char tests; for Strings use equals (or compareTo); for computed doubles use a tolerance; for booleans use the variable itself instead of == true.
- **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: == compares, = assigns. Kind: compile-time. Trigger class: if (a = b) with int operands (with boolean operands it compiles and silently assigns).
- **[4] diagnose\_an\_error** (rule type D, error rule): rule broken: == on Strings compares references, not text. Kind: silent logic error. Trigger class: Comparing a String built at run time (input, concatenation) with a literal using ==.
- **[5] diagnose\_an\_error** (rule type D, error rule): rule broken: &lt; and &gt; are defined only for primitive types; comparisons cannot be chained; both operands must be compatible. Kind: compile-time. Trigger class: s &lt; t on Strings, a &lt; b &lt; c, or 5 &lt; "6".
- **[6] diagnose\_an\_error** (rule type D, error rule): rule broken: Computed doubles should not be compared with ==. Kind: silent logic error. Trigger class: == between doubles produced by arithmetic, e.g. (0.1 + 0.1 + 0.1 == 0.3).

## Same topic

`comparison_operators` belongs to the topic **Comparisons** (`topic1.2.f`). It is the only concept of that topic.

## Rules of the concept (26)

- **Book** (SW-1e, p. 26 (pdf 36)): "The most important operators of this kind are the comparison operators ==, !=, &lt;, &lt;=, &gt;, and &gt;=, which all are defined for each primitive numeric type and produce a boolean result."
- **Book** (SW-1e, p. 28 (pdf 38)): "The comparison operations have lower precedence than arithmetic operators and higher precedence than boolean operators"
- **Book** (OT-Op2, ): "Keep in mind that you must use "==", not "=", when testing if two primitive values are equal."
- **Book** (SW-1.2, ): "The comparison operators are mixed-type operations that take operands of one type and produce a result of type boolean."
- **E** (folk-meaning rule): Folk meaning: in maths = states that two things are equal, and inequalities can be chained (a &lt; b &lt; c) or spoken as 'equal or less than' (=&lt;). Java rule: = assigns while == compares; the operators are spelled &lt;= and &gt;= only; a &lt; b &lt; c does not compile; and on Strings == compares references.
- **M** (wrong rule / right rule): AssignCompares: wrong: = compares two values instead of assigning. \| right: x = y copies the value of y into x; x == y is what compares them and produces a boolean.
- **M** (wrong rule / right rule): ChainedComparison: wrong: 90 &lt;= grade &lt;= 100 tests whether grade is between 90 and 100. \| right: a &lt; b &lt; c does not compile (a &lt; b is a boolean); a range test is written 90 &lt;= grade &amp;&amp; grade &lt;= 100.
- **M** (wrong rule / right rule): ComparisonWithBooleanLiteral: wrong: You must write == true / == false to test a boolean. \| right: if (b) already tests b, so writing == true adds nothing.
- **M** (wrong rule / right rule): EqualsComparesReferences: wrong: .equals() compares references, not contents. \| right: s.equals(t) checks whether the two Strings contain the same characters; it is == that compares references.
- **M** (wrong rule / right rule): EqualityOperatorComparesObjectsValues: wrong: == compares the contents of two Strings. \| right: s == t is true only when s and t refer to the same object; "abc" == "ab" + x is false even when x is "c"; s.equals(t) compares the text.
- **M** (wrong rule / right rule): StringRelationalComparison: wrong: s &lt; t compares two Strings alphabetically. \| right: &lt; and &gt; are defined only for primitive types; comparing Strings with them does not compile (use s.compareTo(t)).
- **M** (wrong rule / right rule): LessGreaterSwapped: wrong: &lt; and &gt; mean the same thing (or a &lt; b means a is greater than b). \| right: a &lt; b is true when a is smaller than b; a &gt; b when a is larger.
- **T** (uneven-application rule): Points to LT (evaluate both operands, promote to a common type, then compare). Applied unevenly: the student treats &lt; as &lt;= on the boundary pass of a loop, or compares an int with a double as ints on one line and as doubles on another.
- **N** (identity rule): Comparison (relational) operators ==, !=, &lt;, &lt;=, &gt;, &gt;= are mixed-type operators: they take two operands of a numeric type and produce a boolean.
- **S** (declarative rule): ==, !=, &lt;, &lt;=, &gt;, &gt;= are defined for each primitive numeric type and produce a boolean; they have lower precedence than arithmetic and higher than boolean operators; &lt; and &gt; are not defined for Strings, and == on non-primitive types compares identity.
- **LT** (operational sequencing rule): Evaluate the left operand (including its arithmetic), then the right operand; if their types differ, promote the narrower one (int to double); then compare and produce true or false.
- **OP** (evaluation / result rule): The result is a boolean: (2 &lt;= 2) is true, 2 &lt; 2 is false, (x &lt; 3.1) is true for int x = 3; any comparison involving NaN, even NaN == NaN, is false.
- **OS** (state-transition rule): A comparison changes no variable and only returns a boolean, unlike =, which changes the value of the variable on its left.
- **R** (composition rule (with a neighbour)): with expression: A comparison is itself an expression whose value is a boolean, so it can appear anywhere a boolean is needed, including on the right of an assignment (boolean ok = x &gt; y;).
- **R** (composition rule (with a neighbour)): with boolean\_expression: Comparisons are the building blocks of conditions: together with boolean logic they provide the basis for decision-making.
- **R** (composition rule (with a neighbour)): with logical\_operators: Comparisons bind tighter than &amp;&amp; and \|\|, so they are evaluated first and logical operators combine their boolean results.
- **R** (composition rule (with a neighbour)): with boolean: Comparisons take numbers and produce a boolean; boolean values themselves can be compared only with == and != (not &lt;), and testing them against true is unnecessary.
- **P** (plan / role rule): Used to test a numeric condition: thresholds and sign checks, range tests, divisibility (n % k == 0), loop continuation (i &lt; N), sentinel checks, and running-extreme updates (if (x &gt; max) max = x).
- **C** (conservation rule): Changing &lt; to &lt;= (or &gt; to &gt;=) changes the result only at the boundary value, which in a loop guard means one more or one fewer iteration (off-by-one); mirroring the comparison (a &lt; b to b &gt; a) preserves the value; negating it gives the complementary operator (!(a &lt; b) is a &gt;= b).
- **D** (error rule): rule broken: The operators are written &lt;= and &gt;=. (compile-time)
- **D** (error rule): rule broken: == compares, = assigns. (compile-time)
- **D** (error rule): rule broken: == on Strings compares references, not text. (silent logic error)
- **D** (error rule): rule broken: &lt; and &gt; are defined only for primitive types; comparisons cannot be chained; both operands must be compatible. (compile-time)
- **D** (error rule): rule broken: Computed doubles should not be compared with ==. (silent logic error)
- **X** (applicability rule): Use comparison operators for numeric and char tests; for Strings use equals (or compareTo); for computed doubles use a tolerance; for booleans use the variable itself instead of == true.

## How it is found in code and answers (reader block)

- **Aliases:** comparison, compares, less than, greater than, equal to, ==
- **Code patterns:** `^(?![ \t]*(?:[%$]|javac?\b))[^\n]*?(?:[<>]=?|==|!=)`
- **Operator symbols:** none
- **Java types:** none

## The whole prerequisite chain

- **Everything it builds on (8):** `arithmetic_operators`, `boolean`, `data_type`, `expression`, `identifier`, `literal`, `primitive_type`, `variable`
- **Everything that builds on it (52):** `accumulator_pattern`, `animation`, `array_copy`, `array_reversal`, `array_traversal`, `boolean_expression`, `boolean_flag_array`, `break_statement`, `conditional_operator`, `continue_statement`, `convergence_rate`, `convergence_test`, `counter_pattern`, `dangling_else`, `do_while_loop`, `else_if_chain`, `enhanced_for`, `fencepost_loop`, `flag_search_loop`, `for_loop`, `frequency_counting`, `function_plotting`, `if_else_statement`, `if_statement`, `increment_operators`, `infinite_loop`, `labeled_break`, `loop_body`, `loop_control`, `loop_invariant_reasoning`, `loop_performance`, `loop_scope`, `loop_variable`, `matrix_operations`, `monte_carlo_simulation`, `mouse_interaction`, `nested_conditionals`, `nested_loops`, `number_conversion`, `off_by_one_error`, `power_method`, `random_move`, `row_major_order`, `running_extreme`, `sentinel_loop`, `side_effect_order`, `simulation_loop`, `standard_audio`, `switch_statement`, `syntax_template`, `two_models`, `while_loop`

## Every edge in this view and its exact edge logic (29)

All the edges drawn in the picture, in the order: prerequisite, parallel, misconception, error, has_level, contains.

**1. `boolean` &rarr; `comparison_operators`** (prerequisite)

- **Exact edge logic:** A comparison such as a &lt; b takes two numbers and produces a boolean result.
- **Grounding:** book\_passage
- **Composition rule (R) of `boolean` with `comparison_operators`:** Comparisons are the main producers of boolean values: they take two numbers and return true or false, which can then be stored in a boolean variable.
- **Composition rule (R) of `comparison_operators` with `boolean`:** Comparisons take numbers and produce a boolean; boolean values themselves can be compared only with == and != (not &lt;), and testing them against true is unnecessary.

**2. `comparison_operators` &rarr; `boolean_expression`** (prerequisite)

- **Exact edge logic:** A comparison such as x &lt; y produces a boolean result; comparisons together with boolean logic provide the basis for decision-making.
- **Grounding:** book\_passage
- **Composition rule (R) of `comparison_operators` with `boolean_expression`:** Comparisons are the building blocks of conditions: together with boolean logic they provide the basis for decision-making.
- **Composition rule (R) of `boolean_expression` with `comparison_operators`:** Comparisons are the atoms of boolean expressions; because they bind tighter than &amp;&amp; and \|\|, month &gt;= 1 &amp;&amp; month &lt;= 12 groups as (month &gt;= 1) &amp;&amp; (month &lt;= 12) without parentheses.

**3. `expression` &rarr; `comparison_operators`** (prerequisite)

- **Exact edge logic:** Comparison operators build expressions whose value is a boolean, so one must already know what an expression is to understand a &lt; b.
- **Grounding:** order\_only
- **Composition rule (R) of `expression` with `comparison_operators`:** A comparison takes numeric expressions and yields a boolean expression, and it has lower precedence than arithmetic, so a + b &lt; c compares the sum.
- **Composition rule (R) of `comparison_operators` with `expression`:** A comparison is itself an expression whose value is a boolean, so it can appear anywhere a boolean is needed, including on the right of an assignment (boolean ok = x &gt; y;).

**4. `assignment` &harr; `comparison_operators`** (parallel)

- **Exact edge logic:** x = y stores the value of y in x (a statement with a side effect); x == y only tests whether the two values are equal and gives a boolean. Writing = where == is meant is a compile error with int operands and a silent bug with boolean operands.
- **Grounding:** book\_passage

**5. `comparison_operators` &harr; `logical_operators`** (parallel)

- **Exact edge logic:** Relational operators compare two numbers to give a boolean; logical operators combine booleans into one boolean.
- **Grounding:** book\_passage
- **Composition rule (R) of `comparison_operators` with `logical_operators`:** Comparisons bind tighter than &amp;&amp; and \|\|, so they are evaluated first and logical operators combine their boolean results.
- **Composition rule (R) of `logical_operators` with `comparison_operators`:** Comparisons bind tighter than &amp;&amp; and \|\|, so comparisons are evaluated first and their boolean results are then combined (month &gt;= 1 &amp;&amp; month &lt;= 12).

**6. `comparison_operators` &rarr; `AssignCompares`** (misconception)

- **Exact edge logic (the wrong rule):** = compares two values instead of assigning
- **Twin logic (the right rule):** x = y copies the value of y into x; x == y is what compares them.
- **Role:** context

**7. `comparison_operators` &rarr; `ChainedComparison`** (misconception)

- **Exact edge logic (the wrong rule):** 90 &lt;= grade &lt;= 100 tests whether grade is between 90 and 100.
- **Twin logic (the right rule):** a &lt; b &lt; c does not compile (a &lt; b is a boolean); a range test is written 90 &lt;= grade &amp;&amp; grade &lt;= 100.
- **Role:** primary

**8. `comparison_operators` &rarr; `ComparisonWithBooleanLiteral`** (misconception)

- **Exact edge logic (the wrong rule):** you must write == true / == false to test a boolean
- **Twin logic (the right rule):** if (b) already tests b, so writing == true adds nothing.
- **Role:** context

**9. `comparison_operators` &rarr; `EqualityOperatorComparesObjectsValues`** (misconception)

- **Exact edge logic (the wrong rule):** s == t is true whenever the two Strings contain the same text.
- **Twin logic (the right rule):** s == t is true only when s and t refer to the same object; s.equals(t) compares the text.
- **Role:** primary

**10. `comparison_operators` &rarr; `EqualsComparesReferences`** (misconception)

- **Exact edge logic (the wrong rule):** .equals() compares references, not contents
- **Twin logic (the right rule):** s.equals(t) checks whether the two Strings contain the same characters.
- **Role:** context

**11. `comparison_operators` &rarr; `LessGreaterSwapped`** (misconception)

- **Exact edge logic (the wrong rule):** &lt; and &gt; mean the same thing (or a &lt; b means a is greater than b).
- **Twin logic (the right rule):** a &lt; b is true when a is smaller than b; a &gt; b when a is larger.
- **Role:** primary

**12. `comparison_operators` &rarr; `StringRelationalComparison`** (misconception)

- **Exact edge logic (the wrong rule):** s &lt; t compares two Strings alphabetically.
- **Twin logic (the right rule):** &lt; and &gt; are defined only for primitive types; comparing Strings with them does not compile.
- **Role:** primary

**13. `assignment` &rarr; `AssignCompares`** (misconception)

- **Exact edge logic (the wrong rule):** x = y checks whether x and y are equal.
- **Twin logic (the right rule):** x = y copies the value of y into x; x == y is what compares them.
- **Role:** primary

**14. `boolean_expression` &rarr; `ChainedComparison`** (misconception)

- **Exact edge logic (the wrong rule):** 90 &lt;= grade &lt;= 100 tests whether grade is between 90 and 100.
- **Twin logic (the right rule):** a &lt; b &lt; c does not compile (a &lt; b is a boolean); a range test is written 90 &lt;= grade &amp;&amp; grade &lt;= 100.
- **Role:** context

**15. `boolean_expression` &rarr; `ComparisonWithBooleanLiteral`** (misconception)

- **Exact edge logic (the wrong rule):** To test a boolean b you must write if (b == true).
- **Twin logic (the right rule):** if (b) already tests b, so writing == true adds nothing.
- **Role:** primary

**16. `if_statement` &rarr; `AssignCompares`** (misconception)

- **Exact edge logic (the wrong rule):** = compares two values instead of assigning
- **Twin logic (the right rule):** x = y copies the value of y into x; x == y is what compares them.
- **Role:** context

**17. `loop_guard` &rarr; `LessGreaterSwapped`** (misconception)

- **Exact edge logic (the wrong rule):** &lt; and &gt; mean the same thing (or a &lt; b means a is greater than b).
- **Twin logic (the right rule):** a &lt; b is true when a is smaller than b; a &gt; b when a is larger.
- **Role:** context

**18. `method_call` &rarr; `EqualsComparesReferences`** (misconception)

- **Exact edge logic (the wrong rule):** .equals() compares references, not contents
- **Twin logic (the right rule):** s.equals(t) checks whether the two Strings contain the same characters.
- **Role:** context

**19. `primitive_vs_reference` &rarr; `EqualityOperatorComparesObjectsValues`** (misconception)

- **Exact edge logic (the wrong rule):** == compares contents (the String == bug)
- **Twin logic (the right rule):** s == t is true only when s and t refer to the same object; s.equals(t) compares the text.
- **Role:** context

**20. `string_type` &rarr; `EqualityOperatorComparesObjectsValues`** (misconception)

- **Exact edge logic (the wrong rule):** s == t is true whenever the two Strings contain the same text.
- **Twin logic (the right rule):** s == t is true only when s and t refer to the same object; s.equals(t) compares the text.
- **Role:** context

**21. `string_type` &rarr; `EqualsComparesReferences`** (misconception)

- **Exact edge logic (the wrong rule):** s.equals(t) checks whether s and t are the same object.
- **Twin logic (the right rule):** s.equals(t) checks whether the two Strings contain the same characters.
- **Role:** primary

**22. `string_type` &rarr; `StringRelationalComparison`** (misconception)

- **Exact edge logic (the wrong rule):** s &lt; t compares two Strings alphabetically.
- **Twin logic (the right rule):** &lt; and &gt; are defined only for primitive types; comparing Strings with them does not compile.
- **Role:** context

**23. `comparison_operators` &rarr; `ReversedRelationalOperator`** (error)

- **Exact edge logic (the wrong rule):** Writes =&lt; or =&gt; instead of &lt;= and &gt;=.
- **Twin logic (the right rule):** The operators are written &lt;= and &gt;=.
- **Role:** primary

**24. `comparison_operators` &rarr; `comparison_operators@L0`** (has_level)

- **Exact edge logic:** comparison operators -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (9 ways).
  - **[0] everyday\_reading** (rule type E, folk-meaning rule): Folk meaning: in maths = states that two things are equal, and inequalities can be chained (a &lt; b &lt; c) or spoken as 'equal or less than' (=&lt;). Java rule: = assigns while == compares; the operators are spelled &lt;= and &gt;= only; a &lt; b &lt; c does not compile; and on Strings == compares references.
  - **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `ChainedComparison`: wrong rule: 90 &lt;= grade &lt;= 100 tests whether grade is between 90 and 100. Right rule: a &lt; b &lt; c does not compile (a &lt; b is a boolean); a range test is written 90 &lt;= grade &amp;&amp; grade &lt;= 100.
  - **[2] misconception** (rule type M, wrong rule / right rule) &rarr; `EqualityOperatorComparesObjectsValues`: wrong rule: == compares the contents of two Strings. Right rule: s == t is true only when s and t refer to the same object; "abc" == "ab" + x is false even when x is "c"; s.equals(t) compares the text.
  - **[3] misconception** (rule type M, wrong rule / right rule) &rarr; `StringRelationalComparison`: wrong rule: s &lt; t compares two Strings alphabetically. Right rule: &lt; and &gt; are defined only for primitive types; comparing Strings with them does not compile (use s.compareTo(t)).
  - **[4] misconception** (rule type M, wrong rule / right rule) &rarr; `LessGreaterSwapped`: wrong rule: &lt; and &gt; mean the same thing (or a &lt; b means a is greater than b). Right rule: a &lt; b is true when a is smaller than b; a &gt; b when a is larger.
  - **[5] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `ChainedComparison`: Points to LT (evaluate both operands, promote to a common type, then compare). Applied unevenly: the student treats &lt; as &lt;= on the boundary pass of a loop, or compares an int with a double as ints on one line and as doubles on another. (here mixing in: "90 &lt;= grade &lt;= 100 tests whether grade is between 90 and 100")
  - **[6] misconception** (rule type M, wrong rule / right rule) &rarr; `AssignCompares`: wrong rule: = compares two values instead of assigning. Right rule: x = y copies the value of y into x; x == y is what compares them and produces a boolean.
  - **[7] misconception** (rule type M, wrong rule / right rule) &rarr; `ComparisonWithBooleanLiteral`: wrong rule: You must write == true / == false to test a boolean. Right rule: if (b) already tests b, so writing == true adds nothing.
  - **[8] misconception** (rule type M, wrong rule / right rule) &rarr; `EqualsComparesReferences`: wrong rule: .equals() compares references, not contents. Right rule: s.equals(t) checks whether the two Strings contain the same characters; it is == that compares references.

**25. `comparison_operators` &rarr; `comparison_operators@L1`** (has_level)

- **Exact edge logic:** comparison operators -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).
  - **[0] names\_the\_element** (rule type N, identity rule): Comparison (relational) operators ==, !=, &lt;, &lt;=, &gt;, &gt;= are mixed-type operators: they take two operands of a numeric type and produce a boolean.
  - **[1] states\_the\_rule** (rule type S, declarative rule): ==, !=, &lt;, &lt;=, &gt;, &gt;= are defined for each primitive numeric type and produce a boolean; they have lower precedence than arithmetic and higher than boolean operators; &lt; and &gt; are not defined for Strings, and == on non-primitive types compares identity.

**26. `comparison_operators` &rarr; `comparison_operators@L2`** (has_level)

- **Exact edge logic:** comparison operators -&gt; L2 (Multistructural): the answer applies the rules of comparison operators to every part of the code, in order (3 ways).
  - **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): Evaluate the left operand (including its arithmetic), then the right operand; if their types differ, promote the narrower one (int to double); then compare and produce true or false.
  - **[1] output\_prediction** (rule type OP, evaluation / result rule): The result is a boolean: (2 &lt;= 2) is true, 2 &lt; 2 is false, (x &lt; 3.1) is true for int x = 3; any comparison involving NaN, even NaN == NaN, is false.
  - **[2] one\_step\_execution** (rule type OS, state-transition rule): A comparison changes no variable and only returns a boolean, unlike =, which changes the value of the variable on its left.

**27. `comparison_operators` &rarr; `comparison_operators@L3`** (has_level)

- **Exact edge logic:** comparison operators -&gt; L3 (Relational): the answer relates the parts (6 ways).
  - **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): A comparison is itself an expression whose value is a boolean, so it can appear anywhere a boolean is needed, including on the right of an assignment (boolean ok = x &gt; y;).
  - **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Comparisons are the building blocks of conditions: together with boolean logic they provide the basis for decision-making.
  - **[2] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Comparisons bind tighter than &amp;&amp; and \|\|, so they are evaluated first and logical operators combine their boolean results.
  - **[3] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Comparisons take numbers and produce a boolean; boolean values themselves can be compared only with == and != (not &lt;), and testing them against true is unnecessary.
  - **[4] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): x = y stores the value of y in x (a statement with a side effect); x == y only tests whether the two values are equal and gives a boolean. Writing = where == is meant is a compile error with int operands and a silent bug with boolean operands.
  - **[5] purpose\_of\_the\_whole** (rule type P, plan / role rule): Used to test a numeric condition: thresholds and sign checks, range tests, divisibility (n % k == 0), loop continuation (i &lt; N), sentinel checks, and running-extreme updates (if (x &gt; max) max = x).

**28. `comparison_operators` &rarr; `comparison_operators@L4`** (has_level)

- **Exact edge logic:** comparison operators -&gt; L4 (Extended abstract): the answer reasons beyond the given code (7 ways).
  - **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `ChainedComparison`: Changing &lt; to &lt;= (or &gt; to &gt;=) changes the result only at the boundary value, which in a loop guard means one more or one fewer iteration (off-by-one); mirroring the comparison (a &lt; b to b &gt; a) preserves the value; negating it gives the complementary operator (!(a &lt; b) is a &gt;= b).
  - **[1] diagnose\_an\_error** (rule type D, error rule): rule broken: The operators are written &lt;= and &gt;=. Kind: compile-time. Trigger class: Writing =&lt; or =&gt; (e.g. if (x =&gt; 0)).
  - **[2] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Use comparison operators for numeric and char tests; for Strings use equals (or compareTo); for computed doubles use a tolerance; for booleans use the variable itself instead of == true.
  - **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: == compares, = assigns. Kind: compile-time. Trigger class: if (a = b) with int operands (with boolean operands it compiles and silently assigns).
  - **[4] diagnose\_an\_error** (rule type D, error rule): rule broken: == on Strings compares references, not text. Kind: silent logic error. Trigger class: Comparing a String built at run time (input, concatenation) with a literal using ==.
  - **[5] diagnose\_an\_error** (rule type D, error rule): rule broken: &lt; and &gt; are defined only for primitive types; comparisons cannot be chained; both operands must be compatible. Kind: compile-time. Trigger class: s &lt; t on Strings, a &lt; b &lt; c, or 5 &lt; "6".
  - **[6] diagnose\_an\_error** (rule type D, error rule): rule broken: Computed doubles should not be compared with ==. Kind: silent logic error. Trigger class: == between doubles produced by arithmetic, e.g. (0.1 + 0.1 + 0.1 == 0.3).

**29. `topic1.2.f` &rarr; `comparison_operators`** (contains)

- topic `topic1.2.f` contains `comparison_operators`
