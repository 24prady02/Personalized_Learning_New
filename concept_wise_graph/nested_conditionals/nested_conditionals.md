# nested_conditionals (`nested_conditionals`)

else-if chains and conditionals inside conditionals

Section 1.3 Conditionals and Loops, topic 1.3.e Nesting.

![The knowledge graph around nested_conditionals](nested_conditionals.png)

## At a glance

- **Needs first:** `if_else_statement`, `if_statement`
- **Leads to:** `dangling_else`
- **Learned alongside:** `switch_statement`
- **Misconceptions:** `ElseMatchesIndentation`, `InconsistentIndentation`, `InnerIfIgnoresOuter`, `MultipleElseIfBranchesRun`, `NestedIfsInsteadOfLogicalOperators`, `SequentialIfsAreNested`
- **Errors:** none
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 27 edges around this concept. The edge logic, the wrong and right rules and the exact rules of the ways are copied word for word from the graph.

## To work on (1)

- misconceptions with no L0 way linked to them: InconsistentIndentation

## What it needs first (2)

A prerequisite edge means the other concept has to be understood before `nested_conditionals`.

### `if_else_statement` comes before `nested_conditionals`

*choose one of two blocks*

- **Edge:** `pre:if_else_statement->nested_conditionals`
- **Exact edge logic:** Nesting puts an if or if-else inside a branch of another if-else; an else-if chain is the common case where the else branch is itself an if.
- **Grounding:** book\_passage
- **Composition rule (R) of `nested_conditionals` with `if_else_statement`:** Nesting puts an if or if-else inside a branch of another if-else; when the inner statement fills the else branch it forms an else-if chain.
- **Composition rule (R) of `if_else_statement` with `nested_conditionals`:** Either branch may itself be an if or if-else, which nests conditionals; without braces an inner else pairs with the innermost if.

### `if_statement` comes before `nested_conditionals`

*run a block only when the condition holds*

- **Edge:** `pre:if_statement->nested_conditionals`
- **Exact edge logic:** An if statement can sit inside the body of another if; the inner one is tested only when the outer condition is true.
- **Grounding:** book\_passage

## What it leads to (1)

These concepts need `nested_conditionals` first.

### `nested_conditionals` comes before `dangling_else`

*an else belongs to the nearest unmatched if*

- **Edge:** `pre:nested_conditionals->dangling_else`
- **Exact edge logic:** The dangling else arises when ifs are nested without braces.
- **Grounding:** book\_passage
- **Composition rule (R) of `nested_conditionals` with `dangling_else`:** The dangling-else ambiguity arises when ifs are nested without braces: if &lt;e1&gt; if &lt;e2&gt; A else B attaches else to the inner if.
- **Composition rule (R) of `dangling_else` with `nested_conditionals`:** The dangling else arises only when ifs are nested without braces; adding braces around the inner if lets the else belong to the outer if.

## Learned alongside (1)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

### `nested_conditionals` alongside `switch_statement`

*switch (x) { case v: ...; break; default: ... }*

- **Edge:** `par:nested_conditionals~switch_statement`
- **Exact edge logic:** When there are more than two mutually exclusive alternatives, a chain of if-else statements works, but a switch statement provides a direct solution that evaluates one expression against many possible values.
- **Grounding:** book\_passage
- **Composition rule (R) of `nested_conditionals` with `switch_statement`:** For more than two mutually exclusive alternatives a chain of if-else statements works, but a switch tests one expression against many values directly.
- **Composition rule (R) of `switch_statement` with `nested_conditionals`:** A switch replaces an if-else chain only when every test is \`expr == constant\` on the same expression. Range tests such as the income-bracket chain (\`income &lt; 47450\`) must stay an if-else chain.

## Misconceptions (6)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### ElseMatchesIndentation

- **Edge:** `nested_conditionals` &rarr; `ElseMatchesIndentation` (misconception)
- **Exact edge logic (the wrong rule):** The else belongs to the if it is lined up with.
- **Twin logic (the right rule):** The else belongs to the most recent unmatched if, whatever the indentation.
- **Wrong belief (on the node):** The else belongs to the if it is lined up with.
- **Correct rule (on the node):** The else belongs to the most recent unmatched if, whatever the indentation.
- **Provenance:** textbook
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [4] misconception, exact rule:** wrong rule: The else belongs to the if it is lined up with. Right rule: The else belongs to the most recent unmatched if, whatever the indentation.
- **Edge `dangling_else` &rarr; `ElseMatchesIndentation`, exact edge logic:** The else belongs to the if it is lined up with. **Twin logic:** The else belongs to the most recent unmatched if, whatever the indentation. (role: primary)

### InconsistentIndentation

- **Edge:** `nested_conditionals` &rarr; `InconsistentIndentation` (misconception)
- **Exact edge logic (the wrong rule):** Indents nested blocks inconsistently, so the visual nesting differs from the real nesting.
- **Twin logic (the right rule):** Indent consistently, one level deeper for each nested block, so the layout shows the real nesting; the compiler ignores indentation.
- **Wrong belief (on the node):** Indents nested blocks inconsistently, so the visual nesting differs from the real nesting.
- **Correct rule (on the node):** Indent consistently, one level deeper for each nested block, so the layout shows the real nesting; the compiler ignores indentation.
- **Provenance:** rule\_dictionary
- **Role of this concept:** context
- **L0 way linked to it:** no
- **Edge `block` &rarr; `InconsistentIndentation`, exact edge logic:** Indents nested blocks inconsistently, so the visual nesting differs from the real nesting. **Twin logic:** Indent consistently, one level deeper for each nested block, so the layout shows the real nesting; the compiler ignores indentation. (role: context)
- **Edge `nested_loops` &rarr; `InconsistentIndentation`, exact edge logic:** Indents nested blocks inconsistently, so the visual nesting differs from the real nesting. **Twin logic:** Indent consistently, one level deeper for each nested block, so the layout shows the real nesting; the compiler ignores indentation. (role: context)
- **Edge `program_layout` &rarr; `InconsistentIndentation`, exact edge logic:** Indents nested blocks inconsistently, so the visual nesting differs from the real nesting. **Twin logic:** Indent consistently, one level deeper for each nested block, so the layout shows the real nesting; the compiler ignores indentation. (role: primary)

### InnerIfIgnoresOuter

- **Edge:** `nested_conditionals` &rarr; `InnerIfIgnoresOuter` (misconception)
- **Exact edge logic (the wrong rule):** An inner if runs its body whenever its own condition is true, even if the outer if condition is false.
- **Twin logic (the right rule):** The inner if is part of the outer branch: it is reached, and its condition tested, only when the outer condition is true.
- **Wrong belief (on the node):** An inner if runs its body whenever its own condition is true, even if the outer if condition is false.
- **Correct rule (on the node):** The inner if is part of the outer branch: it is reached, and its condition tested, only when the outer condition is true.
- **Provenance:** published
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [1] misconception, exact rule:** wrong rule: An inner if runs its body whenever its own condition is true, even if the outer if condition is false. Right rule: The inner if is part of the outer branch: it is reached, and its condition tested, only when the outer condition is true.
- **L0 way [3] inconsistent\_trace, exact rule:** Applies the nesting rule (LT) unevenly: on some inputs tests the inner condition even though the outer one was false, or matches an else to the if it is lined up with. (here mixing in: "An inner if runs its body whenever its own condition is true, even if the outer if condition is false")

### MultipleElseIfBranchesRun

- **Edge:** `nested_conditionals` &rarr; `MultipleElseIfBranchesRun` (misconception)
- **Exact edge logic (the wrong rule):** Every true branch of an else-if chain runs.
- **Twin logic (the right rule):** Only the first branch whose condition is true runs.
- **Wrong belief (on the node):** Every true branch of an else-if chain runs.
- **Correct rule (on the node):** Only the first branch whose condition is true runs.
- **Provenance:** published
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [5] misconception, exact rule:** wrong rule: Every true branch of an else-if chain runs. Right rule: Only the first branch whose condition is true runs.
- **Edge `else_if_chain` &rarr; `MultipleElseIfBranchesRun`, exact edge logic:** Every true branch of an else-if chain runs. **Twin logic:** Only the first branch whose condition is true runs. (role: primary)

### NestedIfsInsteadOfLogicalOperators

- **Edge:** `nested_conditionals` &rarr; `NestedIfsInsteadOfLogicalOperators` (misconception)
- **Exact edge logic (the wrong rule):** A condition on several values has to be written as nested if statements, one value per if.
- **Twin logic (the right rule):** Several conditions combine into one boolean expression with &amp;&amp; and \|\|, e.g. if (x == 0 &amp;&amp; y == 0).
- **Wrong belief (on the node):** A condition on several values has to be written as nested if statements, one value per if.
- **Correct rule (on the node):** Several conditions combine into one boolean expression with &amp;&amp; and \|\|, e.g. if (x == 0 &amp;&amp; y == 0).
- **Provenance:** published
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [6] misconception, exact rule:** wrong rule: A condition on several values has to be written as nested if statements, one value per if. Right rule: Several conditions combine into one boolean expression with &amp;&amp; and \|\|, e.g. if (x == 0 &amp;&amp; y == 0).
- **Edge `boolean_expression` &rarr; `NestedIfsInsteadOfLogicalOperators`, exact edge logic:** A condition on several values has to be written as nested if statements, one value per if. **Twin logic:** Several conditions combine into one boolean expression with &amp;&amp; and \|\|, e.g. if (x == 0 &amp;&amp; y == 0). (role: context)
- **Edge `logical_operators` &rarr; `NestedIfsInsteadOfLogicalOperators`, exact edge logic:** A condition on several values has to be written as nested if statements, one value per if. **Twin logic:** Several conditions combine into one boolean expression with &amp;&amp; and \|\|, e.g. if (x == 0 &amp;&amp; y == 0). (role: primary)

### SequentialIfsAreNested

- **Edge:** `nested_conditionals` &rarr; `SequentialIfsAreNested` (misconception)
- **Exact edge logic (the wrong rule):** Of two if statements one after the other, the second runs its body only if both conditions are true.
- **Twin logic (the right rule):** Two ifs in sequence are independent: each tests only its own condition.
- **Wrong belief (on the node):** Of two if statements one after the other, the second runs its body only if both conditions are true.
- **Correct rule (on the node):** Two ifs in sequence are independent: each tests only its own condition.
- **Provenance:** published
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [2] misconception, exact rule:** wrong rule: Of two if statements one after the other, the second runs its body only if both conditions are true. Right rule: Two ifs in sequence are independent: each tests only its own condition.
- **Edge `if_statement` &rarr; `SequentialIfsAreNested`, exact edge logic:** Of two if statements one after the other, the second runs its body only if both conditions are true. **Twin logic:** Two ifs in sequence are independent: each tests only its own condition. (role: context)

## Errors (0)

An error edge states the rule that gets broken in a program, and the right rule.

The graph has no error edge from this concept.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for nested conditionals: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to nested conditionals agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

- **Edge:** `nested_conditionals` &rarr; `nested_conditionals@L0` (has_level)
- **Exact edge logic:** nested conditionals -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (7 ways).

Ways (7), each with its exact rule:

- **[0] everyday\_reading** (rule type E, folk-meaning rule): Folk meaning: in prose, indentation and line layout show what belongs to what, and two consecutive 'if' sentences can be heard as one combined condition. The Java compiler ignores indentation: an inner if belongs to the branch that syntactically contains it, and an else pairs with the innermost unmatched if.
- **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `InnerIfIgnoresOuter`: wrong rule: An inner if runs its body whenever its own condition is true, even if the outer if condition is false. Right rule: The inner if is part of the outer branch: it is reached, and its condition tested, only when the outer condition is true.
- **[2] misconception** (rule type M, wrong rule / right rule) &rarr; `SequentialIfsAreNested`: wrong rule: Of two if statements one after the other, the second runs its body only if both conditions are true. Right rule: Two ifs in sequence are independent: each tests only its own condition.
- **[3] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `InnerIfIgnoresOuter`: Applies the nesting rule (LT) unevenly: on some inputs tests the inner condition even though the outer one was false, or matches an else to the if it is lined up with. (here mixing in: "An inner if runs its body whenever its own condition is true, even if the outer if condition is false")
- **[4] misconception** (rule type M, wrong rule / right rule) &rarr; `ElseMatchesIndentation`: wrong rule: The else belongs to the if it is lined up with. Right rule: The else belongs to the most recent unmatched if, whatever the indentation.
- **[5] misconception** (rule type M, wrong rule / right rule) &rarr; `MultipleElseIfBranchesRun`: wrong rule: Every true branch of an else-if chain runs. Right rule: Only the first branch whose condition is true runs.
- **[6] misconception** (rule type M, wrong rule / right rule) &rarr; `NestedIfsInsteadOfLogicalOperators`: wrong rule: A condition on several values has to be written as nested if statements, one value per if. Right rule: Several conditions combine into one boolean expression with &amp;&amp; and \|\|, e.g. if (x == 0 &amp;&amp; y == 0).

### L1: Unistructural / atom x text surface

L1 for nested conditionals: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

- **Edge:** `nested_conditionals` &rarr; `nested_conditionals@L1` (has_level)
- **Exact edge logic:** nested conditionals -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

Ways (2), each with its exact rule:

- **[0] names\_the\_element** (rule type N, identity rule): Nested conditionals are if or if-else statements placed inside a branch of another conditional; an else-if chain is the common special case.
- **[1] states\_the\_rule** (rule type S, declarative rule): An if/if-else is a statement, so it can be the body (branch) of another conditional; without braces an else belongs to the innermost if to which it might belong, so braces should be used to resolve ambiguities.

### L2: Multistructural / block x execution / preoperational

L2 for nested conditionals: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

- **Edge:** `nested_conditionals` &rarr; `nested_conditionals@L2` (has_level)
- **Exact edge logic:** nested conditionals -&gt; L2 (Multistructural): the answer applies the rules of nested conditionals to every part of the code, in order (3 ways).

Ways (3), each with its exact rule:

- **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): Test the outer condition; only if control enters the branch that contains the inner if is the inner condition tested; after the inner statement, control leaves the outer statement too.
- **[1] output\_prediction** (rule type OP, evaluation / result rule): The output is the action of the single path whose conditions all hold along the way: if (a &gt; b) { if (b &gt; c) X; else Y; } else Z; runs X when a &gt; b &gt; c, Y when a &gt; b and b &lt;= c, and Z otherwise.
- **[2] one\_step\_execution** (rule type OS, state-transition rule): One execution evaluates the conditions along one path only (outer, then possibly inner) and applies one leaf action; conditions on other paths are never evaluated.

### L3: Relational / relations x function (concrete operational begins)

L3 for nested conditionals: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

- **Edge:** `nested_conditionals` &rarr; `nested_conditionals@L3` (has_level)
- **Exact edge logic:** nested conditionals -&gt; L3 (Relational): the answer relates the parts (4 ways).

Ways (4), each with its exact rule:

- **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Nesting puts an if or if-else inside a branch of another if-else; when the inner statement fills the else branch it forms an else-if chain.
- **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): The dangling-else ambiguity arises when ifs are nested without braces: if &lt;e1&gt; if &lt;e2&gt; A else B attaches else to the inner if.
- **[2] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): For more than two mutually exclusive alternatives a chain of if-else statements works, but a switch tests one expression against many values directly.
- **[3] purpose\_of\_the\_whole** (rule type P, plan / role rule): Plan: decision tree - refine a case analysis step by step (e.g. find the smallest of three values, classify a value into ranges).

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for nested conditionals: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

- **Edge:** `nested_conditionals` &rarr; `nested_conditionals@L4` (has_level)
- **Exact edge logic:** nested conditionals -&gt; L4 (Extended abstract): the answer reasons beyond the given code (3 ways).

Ways (3), each with its exact rule:

- **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `InnerIfIgnoresOuter`: Combining if (c1) { if (c2) S; } into if (c1 &amp;&amp; c2) S; preserves behaviour when there are no else parts; adding or removing braces around an inner if can move an else to a different if. Swapping some branches can keep the specification only on certain inputs.
- **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Nest conditionals when a second test only makes sense once the first has succeeded or when cases form a tree; use &amp;&amp; for a simple conjunction, an else-if chain for mutually exclusive ranges, and a switch for many discrete values; one or two levels usually suffice.
- **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: Without braces an else pairs with the innermost if, whatever the indentation. Kind: silent logic error. Trigger class: if (a) if (b) X; else Y; written with else under the outer if: Y runs when a is true and b false, not when a is false.

## Same topic

`nested_conditionals` belongs to the topic **Nesting** (`topic1.3.e`). The topic also contains: `dangling_else`, `else_if_chain`, `nested_loops`.

## Rules of the concept (19)

- **Book** (SW-1e, p. 58 (pdf 68)): "In particular, we can use one or more of them in the &lt;body&gt; of another to make compound statements."
- **Book** (TJ-2e, p. 75 (pdf 97)): "you can also make complex decisions by nesting one conditional statement inside another."
- **Book** (OT-If, ): "once a condition is satisfied, the appropriate statements are executed (grade = 'C';) and the remaining conditions are not evaluated."
- **Book** (SW-1.3, ): "We can use one or more of them in the body of another statement to make compound statements."
- **E** (folk-meaning rule): Folk meaning: in prose, indentation and line layout show what belongs to what, and two consecutive 'if' sentences can be heard as one combined condition. The Java compiler ignores indentation: an inner if belongs to the branch that syntactically contains it, and an else pairs with the innermost unmatched if.
- **M** (wrong rule / right rule): ElseMatchesIndentation: wrong: The else belongs to the if it is lined up with. \| right: The else belongs to the most recent unmatched if, whatever the indentation.
- **M** (wrong rule / right rule): MultipleElseIfBranchesRun: wrong: Every true branch of an else-if chain runs. \| right: Only the first branch whose condition is true runs.
- **M** (wrong rule / right rule): NestedIfsInsteadOfLogicalOperators: wrong: A condition on several values has to be written as nested if statements, one value per if. \| right: Several conditions combine into one boolean expression with &amp;&amp; and \|\|, e.g. if (x == 0 &amp;&amp; y == 0).
- **M** (wrong rule / right rule): InnerIfIgnoresOuter: wrong: An inner if runs its body whenever its own condition is true, even if the outer if condition is false. \| right: The inner if is part of the outer branch: it is reached, and its condition tested, only when the outer condition is true.
- **M** (wrong rule / right rule): SequentialIfsAreNested: wrong: Of two if statements one after the other, the second runs its body only if both conditions are true. \| right: Two ifs in sequence are independent: each tests only its own condition.
- **T** (uneven-application rule): Applies the nesting rule (LT) unevenly: on some inputs tests the inner condition even though the outer one was false, or matches an else to the if it is lined up with.
- **N** (identity rule): Nested conditionals are if or if-else statements placed inside a branch of another conditional; an else-if chain is the common special case.
- **S** (declarative rule): An if/if-else is a statement, so it can be the body (branch) of another conditional; without braces an else belongs to the innermost if to which it might belong, so braces should be used to resolve ambiguities.
- **LT** (operational sequencing rule): Test the outer condition; only if control enters the branch that contains the inner if is the inner condition tested; after the inner statement, control leaves the outer statement too.
- **OP** (evaluation / result rule): The output is the action of the single path whose conditions all hold along the way: if (a &gt; b) { if (b &gt; c) X; else Y; } else Z; runs X when a &gt; b &gt; c, Y when a &gt; b and b &lt;= c, and Z otherwise.
- **OS** (state-transition rule): One execution evaluates the conditions along one path only (outer, then possibly inner) and applies one leaf action; conditions on other paths are never evaluated.
- **R** (composition rule (with a neighbour)): with if\_else\_statement: Nesting puts an if or if-else inside a branch of another if-else; when the inner statement fills the else branch it forms an else-if chain.
- **R** (composition rule (with a neighbour)): with dangling\_else: The dangling-else ambiguity arises when ifs are nested without braces: if &lt;e1&gt; if &lt;e2&gt; A else B attaches else to the inner if.
- **R** (composition rule (with a neighbour)): with switch\_statement: For more than two mutually exclusive alternatives a chain of if-else statements works, but a switch tests one expression against many values directly.
- **P** (plan / role rule): Plan: decision tree - refine a case analysis step by step (e.g. find the smallest of three values, classify a value into ranges).
- **C** (conservation rule): Combining if (c1) { if (c2) S; } into if (c1 &amp;&amp; c2) S; preserves behaviour when there are no else parts; adding or removing braces around an inner if can move an else to a different if. Swapping some branches can keep the specification only on certain inputs.
- **D** (error rule): rule broken: Without braces an else pairs with the innermost if, whatever the indentation. (silent logic error)
- **X** (applicability rule): Nest conditionals when a second test only makes sense once the first has succeeded or when cases form a tree; use &amp;&amp; for a simple conjunction, an else-if chain for mutually exclusive ranges, and a switch for many discrete values; one or two levels usually suffice.

## How it is found in code and answers (reader block)

- **Aliases:** nested if
- **Code patterns:** none
- **Operator symbols:** none
- **Java types:** none
- **Signal nested\_if** (scope program, decisive): `(?:\bif\s*\([^)]*\)|\belse)\s*\{(?:[^{}]|\{[^{}]*\})*?(?P<at>\bif\s*\()`
- **Signal nested\_if\_braceless** (scope program, decisive): `\bif\s*\((?:[^()]|\([^()]*\))*\)\s*(?:\{\s*)?if\s*\(`

## The whole prerequisite chain

- **Everything it builds on (18):** `arithmetic_operators`, `boolean`, `boolean_expression`, `class_declaration`, `comparison_operators`, `control_flow`, `data_type`, `expression`, `identifier`, `if_else_statement`, `if_statement`, `literal`, `logical_operators`, `main_method`, `primitive_type`, `program_text`, `statement`, `variable`
- **Everything that builds on it (1):** `dangling_else`

## Every edge in this view and its exact edge logic (27)

All the edges drawn in the picture, in the order: prerequisite, parallel, misconception, error, has_level, contains.

**1. `if_else_statement` &rarr; `nested_conditionals`** (prerequisite)

- **Exact edge logic:** Nesting puts an if or if-else inside a branch of another if-else; an else-if chain is the common case where the else branch is itself an if.
- **Grounding:** book\_passage
- **Composition rule (R) of `if_else_statement` with `nested_conditionals`:** Either branch may itself be an if or if-else, which nests conditionals; without braces an inner else pairs with the innermost if.
- **Composition rule (R) of `nested_conditionals` with `if_else_statement`:** Nesting puts an if or if-else inside a branch of another if-else; when the inner statement fills the else branch it forms an else-if chain.

**2. `if_statement` &rarr; `nested_conditionals`** (prerequisite)

- **Exact edge logic:** An if statement can sit inside the body of another if; the inner one is tested only when the outer condition is true.
- **Grounding:** book\_passage

**3. `nested_conditionals` &rarr; `dangling_else`** (prerequisite)

- **Exact edge logic:** The dangling else arises when ifs are nested without braces.
- **Grounding:** book\_passage
- **Composition rule (R) of `nested_conditionals` with `dangling_else`:** The dangling-else ambiguity arises when ifs are nested without braces: if &lt;e1&gt; if &lt;e2&gt; A else B attaches else to the inner if.
- **Composition rule (R) of `dangling_else` with `nested_conditionals`:** The dangling else arises only when ifs are nested without braces; adding braces around the inner if lets the else belong to the outer if.

**4. `nested_conditionals` &harr; `switch_statement`** (parallel)

- **Exact edge logic:** When there are more than two mutually exclusive alternatives, a chain of if-else statements works, but a switch statement provides a direct solution that evaluates one expression against many possible values.
- **Grounding:** book\_passage
- **Composition rule (R) of `nested_conditionals` with `switch_statement`:** For more than two mutually exclusive alternatives a chain of if-else statements works, but a switch tests one expression against many values directly.
- **Composition rule (R) of `switch_statement` with `nested_conditionals`:** A switch replaces an if-else chain only when every test is \`expr == constant\` on the same expression. Range tests such as the income-bracket chain (\`income &lt; 47450\`) must stay an if-else chain.

**5. `nested_conditionals` &rarr; `ElseMatchesIndentation`** (misconception)

- **Exact edge logic (the wrong rule):** The else belongs to the if it is lined up with.
- **Twin logic (the right rule):** The else belongs to the most recent unmatched if, whatever the indentation.
- **Role:** context

**6. `nested_conditionals` &rarr; `InconsistentIndentation`** (misconception)

- **Exact edge logic (the wrong rule):** Indents nested blocks inconsistently, so the visual nesting differs from the real nesting.
- **Twin logic (the right rule):** Indent consistently, one level deeper for each nested block, so the layout shows the real nesting; the compiler ignores indentation.
- **Role:** context

**7. `nested_conditionals` &rarr; `InnerIfIgnoresOuter`** (misconception)

- **Exact edge logic (the wrong rule):** An inner if runs its body whenever its own condition is true, even if the outer if condition is false.
- **Twin logic (the right rule):** The inner if is part of the outer branch: it is reached, and its condition tested, only when the outer condition is true.
- **Role:** primary

**8. `nested_conditionals` &rarr; `MultipleElseIfBranchesRun`** (misconception)

- **Exact edge logic (the wrong rule):** Every true branch of an else-if chain runs.
- **Twin logic (the right rule):** Only the first branch whose condition is true runs.
- **Role:** context

**9. `nested_conditionals` &rarr; `NestedIfsInsteadOfLogicalOperators`** (misconception)

- **Exact edge logic (the wrong rule):** A condition on several values has to be written as nested if statements, one value per if.
- **Twin logic (the right rule):** Several conditions combine into one boolean expression with &amp;&amp; and \|\|, e.g. if (x == 0 &amp;&amp; y == 0).
- **Role:** context

**10. `nested_conditionals` &rarr; `SequentialIfsAreNested`** (misconception)

- **Exact edge logic (the wrong rule):** Of two if statements one after the other, the second runs its body only if both conditions are true.
- **Twin logic (the right rule):** Two ifs in sequence are independent: each tests only its own condition.
- **Role:** primary

**11. `block` &rarr; `InconsistentIndentation`** (misconception)

- **Exact edge logic (the wrong rule):** Indents nested blocks inconsistently, so the visual nesting differs from the real nesting.
- **Twin logic (the right rule):** Indent consistently, one level deeper for each nested block, so the layout shows the real nesting; the compiler ignores indentation.
- **Role:** context

**12. `boolean_expression` &rarr; `NestedIfsInsteadOfLogicalOperators`** (misconception)

- **Exact edge logic (the wrong rule):** A condition on several values has to be written as nested if statements, one value per if.
- **Twin logic (the right rule):** Several conditions combine into one boolean expression with &amp;&amp; and \|\|, e.g. if (x == 0 &amp;&amp; y == 0).
- **Role:** context

**13. `dangling_else` &rarr; `ElseMatchesIndentation`** (misconception)

- **Exact edge logic (the wrong rule):** The else belongs to the if it is lined up with.
- **Twin logic (the right rule):** The else belongs to the most recent unmatched if, whatever the indentation.
- **Role:** primary

**14. `else_if_chain` &rarr; `MultipleElseIfBranchesRun`** (misconception)

- **Exact edge logic (the wrong rule):** Every true branch of an else-if chain runs.
- **Twin logic (the right rule):** Only the first branch whose condition is true runs.
- **Role:** primary

**15. `if_statement` &rarr; `SequentialIfsAreNested`** (misconception)

- **Exact edge logic (the wrong rule):** Of two if statements one after the other, the second runs its body only if both conditions are true.
- **Twin logic (the right rule):** Two ifs in sequence are independent: each tests only its own condition.
- **Role:** context

**16. `logical_operators` &rarr; `NestedIfsInsteadOfLogicalOperators`** (misconception)

- **Exact edge logic (the wrong rule):** A condition on several values has to be written as nested if statements, one value per if.
- **Twin logic (the right rule):** Several conditions combine into one boolean expression with &amp;&amp; and \|\|, e.g. if (x == 0 &amp;&amp; y == 0).
- **Role:** primary

**17. `nested_loops` &rarr; `InconsistentIndentation`** (misconception)

- **Exact edge logic (the wrong rule):** Indents nested blocks inconsistently, so the visual nesting differs from the real nesting.
- **Twin logic (the right rule):** Indent consistently, one level deeper for each nested block, so the layout shows the real nesting; the compiler ignores indentation.
- **Role:** context

**18. `program_layout` &rarr; `InconsistentIndentation`** (misconception)

- **Exact edge logic (the wrong rule):** Indents nested blocks inconsistently, so the visual nesting differs from the real nesting.
- **Twin logic (the right rule):** Indent consistently, one level deeper for each nested block, so the layout shows the real nesting; the compiler ignores indentation.
- **Role:** primary

**19. `nested_conditionals` &rarr; `nested_conditionals@L0`** (has_level)

- **Exact edge logic:** nested conditionals -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (7 ways).
  - **[0] everyday\_reading** (rule type E, folk-meaning rule): Folk meaning: in prose, indentation and line layout show what belongs to what, and two consecutive 'if' sentences can be heard as one combined condition. The Java compiler ignores indentation: an inner if belongs to the branch that syntactically contains it, and an else pairs with the innermost unmatched if.
  - **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `InnerIfIgnoresOuter`: wrong rule: An inner if runs its body whenever its own condition is true, even if the outer if condition is false. Right rule: The inner if is part of the outer branch: it is reached, and its condition tested, only when the outer condition is true.
  - **[2] misconception** (rule type M, wrong rule / right rule) &rarr; `SequentialIfsAreNested`: wrong rule: Of two if statements one after the other, the second runs its body only if both conditions are true. Right rule: Two ifs in sequence are independent: each tests only its own condition.
  - **[3] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `InnerIfIgnoresOuter`: Applies the nesting rule (LT) unevenly: on some inputs tests the inner condition even though the outer one was false, or matches an else to the if it is lined up with. (here mixing in: "An inner if runs its body whenever its own condition is true, even if the outer if condition is false")
  - **[4] misconception** (rule type M, wrong rule / right rule) &rarr; `ElseMatchesIndentation`: wrong rule: The else belongs to the if it is lined up with. Right rule: The else belongs to the most recent unmatched if, whatever the indentation.
  - **[5] misconception** (rule type M, wrong rule / right rule) &rarr; `MultipleElseIfBranchesRun`: wrong rule: Every true branch of an else-if chain runs. Right rule: Only the first branch whose condition is true runs.
  - **[6] misconception** (rule type M, wrong rule / right rule) &rarr; `NestedIfsInsteadOfLogicalOperators`: wrong rule: A condition on several values has to be written as nested if statements, one value per if. Right rule: Several conditions combine into one boolean expression with &amp;&amp; and \|\|, e.g. if (x == 0 &amp;&amp; y == 0).

**20. `nested_conditionals` &rarr; `nested_conditionals@L1`** (has_level)

- **Exact edge logic:** nested conditionals -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).
  - **[0] names\_the\_element** (rule type N, identity rule): Nested conditionals are if or if-else statements placed inside a branch of another conditional; an else-if chain is the common special case.
  - **[1] states\_the\_rule** (rule type S, declarative rule): An if/if-else is a statement, so it can be the body (branch) of another conditional; without braces an else belongs to the innermost if to which it might belong, so braces should be used to resolve ambiguities.

**21. `nested_conditionals` &rarr; `nested_conditionals@L2`** (has_level)

- **Exact edge logic:** nested conditionals -&gt; L2 (Multistructural): the answer applies the rules of nested conditionals to every part of the code, in order (3 ways).
  - **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): Test the outer condition; only if control enters the branch that contains the inner if is the inner condition tested; after the inner statement, control leaves the outer statement too.
  - **[1] output\_prediction** (rule type OP, evaluation / result rule): The output is the action of the single path whose conditions all hold along the way: if (a &gt; b) { if (b &gt; c) X; else Y; } else Z; runs X when a &gt; b &gt; c, Y when a &gt; b and b &lt;= c, and Z otherwise.
  - **[2] one\_step\_execution** (rule type OS, state-transition rule): One execution evaluates the conditions along one path only (outer, then possibly inner) and applies one leaf action; conditions on other paths are never evaluated.

**22. `nested_conditionals` &rarr; `nested_conditionals@L3`** (has_level)

- **Exact edge logic:** nested conditionals -&gt; L3 (Relational): the answer relates the parts (4 ways).
  - **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Nesting puts an if or if-else inside a branch of another if-else; when the inner statement fills the else branch it forms an else-if chain.
  - **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): The dangling-else ambiguity arises when ifs are nested without braces: if &lt;e1&gt; if &lt;e2&gt; A else B attaches else to the inner if.
  - **[2] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): For more than two mutually exclusive alternatives a chain of if-else statements works, but a switch tests one expression against many values directly.
  - **[3] purpose\_of\_the\_whole** (rule type P, plan / role rule): Plan: decision tree - refine a case analysis step by step (e.g. find the smallest of three values, classify a value into ranges).

**23. `nested_conditionals` &rarr; `nested_conditionals@L4`** (has_level)

- **Exact edge logic:** nested conditionals -&gt; L4 (Extended abstract): the answer reasons beyond the given code (3 ways).
  - **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `InnerIfIgnoresOuter`: Combining if (c1) { if (c2) S; } into if (c1 &amp;&amp; c2) S; preserves behaviour when there are no else parts; adding or removing braces around an inner if can move an else to a different if. Swapping some branches can keep the specification only on certain inputs.
  - **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Nest conditionals when a second test only makes sense once the first has succeeded or when cases form a tree; use &amp;&amp; for a simple conjunction, an else-if chain for mutually exclusive ranges, and a switch for many discrete values; one or two levels usually suffice.
  - **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: Without braces an else pairs with the innermost if, whatever the indentation. Kind: silent logic error. Trigger class: if (a) if (b) X; else Y; written with else under the outer if: Y runs when a is true and b false, not when a is false.

**24. `topic1.3.e` &rarr; `nested_conditionals`** (contains)

- topic `topic1.3.e` contains `nested_conditionals`

**25. `topic1.3.e` &rarr; `dangling_else`** (contains)

- topic `topic1.3.e` contains `dangling_else`

**26. `topic1.3.e` &rarr; `else_if_chain`** (contains)

- topic `topic1.3.e` contains `else_if_chain`

**27. `topic1.3.e` &rarr; `nested_loops`** (contains)

- topic `topic1.3.e` contains `nested_loops`
