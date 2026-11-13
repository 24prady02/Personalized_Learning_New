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

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 27 edges around this concept, each explained in the graph's own words.

## What it needs first (2)

A prerequisite edge means the other concept has to be understood before `nested_conditionals`.

### `if_else_statement` comes before `nested_conditionals`

*choose one of two blocks*

Nesting puts an if or if-else inside a branch of another if-else; an else-if chain is the common case where the else branch is itself an if.

- **Grounding:** book passage
- **How `nested_conditionals` combines with `if_else_statement`:** Nesting puts an if or if-else inside a branch of another if-else; when the inner statement fills the else branch it forms an else-if chain.
- **How `if_else_statement` combines with `nested_conditionals`:** Either branch may itself be an if or if-else, which nests conditionals; without braces an inner else pairs with the innermost if.

### `if_statement` comes before `nested_conditionals`

*run a block only when the condition holds*

An if statement can sit inside the body of another if; the inner one is tested only when the outer condition is true.

- **Grounding:** book passage

## What it leads to (1)

These concepts need `nested_conditionals` first.

### `nested_conditionals` comes before `dangling_else`

*an else belongs to the nearest unmatched if*

The dangling else arises when ifs are nested without braces.

- **Grounding:** book passage
- **How `nested_conditionals` combines with `dangling_else`:** The dangling-else ambiguity arises when ifs are nested without braces: if &lt;e1&gt; if &lt;e2&gt; A else B attaches else to the inner if.
- **How `dangling_else` combines with `nested_conditionals`:** The dangling else arises only when ifs are nested without braces; adding braces around the inner if lets the else belong to the outer if.

## Learned alongside (1)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

### `nested_conditionals` alongside `switch_statement`

*switch (x) { case v: ...; break; default: ... }*

When there are more than two mutually exclusive alternatives, a chain of if-else statements works, but a switch statement provides a direct solution that evaluates one expression against many possible values.

- **Grounding:** book passage
- **How `nested_conditionals` combines with `switch_statement`:** For more than two mutually exclusive alternatives a chain of if-else statements works, but a switch tests one expression against many values directly.
- **How `switch_statement` combines with `nested_conditionals`:** A switch replaces an if-else chain only when every test is \`expr == constant\` on the same expression. Range tests such as the income-bracket chain (\`income &lt; 47450\`) must stay an if-else chain.

## Misconceptions (6)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### ElseMatchesIndentation

- **Wrong rule:** The else belongs to the if it is lined up with.
- **Right rule:** The else belongs to the most recent unmatched if, whatever the indentation.
- **Role of this concept:** context
- **Shows at level L0 as:** misconception: wrong rule: The else belongs to the if it is lined up with. Right rule: The else belongs to the most recent unmatched if, whatever the indentation.
- **Also an edge from `dangling_else`:** The else belongs to the if it is lined up with.

### InconsistentIndentation

- **Wrong rule:** Indents nested blocks inconsistently, so the visual nesting differs from the real nesting.
- **Right rule:** Indent consistently, one level deeper for each nested block, so the layout shows the real nesting; the compiler ignores indentation.
- **Role of this concept:** context
- **Also an edge from `block`:** Indents nested blocks inconsistently, so the visual nesting differs from the real nesting.
- **Also an edge from `nested_loops`:** Indents nested blocks inconsistently, so the visual nesting differs from the real nesting.
- **Also an edge from `program_layout`:** Indents nested blocks inconsistently, so the visual nesting differs from the real nesting.

### InnerIfIgnoresOuter

- **Wrong rule:** An inner if runs its body whenever its own condition is true, even if the outer if condition is false.
- **Right rule:** The inner if is part of the outer branch: it is reached, and its condition tested, only when the outer condition is true.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: An inner if runs its body whenever its own condition is true, even if the outer if condition is false. Right rule: The inner if is part of the outer branch: it is reached, and its condition tested, only when the outer condition is true.
- **Shows at level L0 as:** inconsistent trace: Applies the nesting rule (LT) unevenly: on some inputs tests the inner condition even though the outer one was false, or matches an else to the if it is lined up with. (here mixing in: "An inner if runs its body whenever its own condition is true, even if the outer if condition is false")

### MultipleElseIfBranchesRun

- **Wrong rule:** Every true branch of an else-if chain runs.
- **Right rule:** Only the first branch whose condition is true runs.
- **Role of this concept:** context
- **Shows at level L0 as:** misconception: wrong rule: Every true branch of an else-if chain runs. Right rule: Only the first branch whose condition is true runs.
- **Also an edge from `else_if_chain`:** Every true branch of an else-if chain runs.

### NestedIfsInsteadOfLogicalOperators

- **Wrong rule:** A condition on several values has to be written as nested if statements, one value per if.
- **Right rule:** Several conditions combine into one boolean expression with &amp;&amp; and \|\|, e.g. if (x == 0 &amp;&amp; y == 0).
- **Role of this concept:** context
- **Shows at level L0 as:** misconception: wrong rule: A condition on several values has to be written as nested if statements, one value per if. Right rule: Several conditions combine into one boolean expression with &amp;&amp; and \|\|, e.g. if (x == 0 &amp;&amp; y == 0).
- **Also an edge from `boolean_expression`:** A condition on several values has to be written as nested if statements, one value per if.
- **Also an edge from `logical_operators`:** A condition on several values has to be written as nested if statements, one value per if.

### SequentialIfsAreNested

- **Wrong rule:** Of two if statements one after the other, the second runs its body only if both conditions are true.
- **Right rule:** Two ifs in sequence are independent: each tests only its own condition.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: Of two if statements one after the other, the second runs its body only if both conditions are true. Right rule: Two ifs in sequence are independent: each tests only its own condition.
- **Also an edge from `if_statement`:** Of two if statements one after the other, the second runs its body only if both conditions are true.

## Errors (0)

An error edge states the rule that gets broken in a program, and the right rule.

The graph has no error edge from this concept.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for nested conditionals: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to nested conditionals agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

nested conditionals -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (7 ways).

- **everyday reading** (folk-meaning rule): Folk meaning: in prose, indentation and line layout show what belongs to what, and two consecutive 'if' sentences can be heard as one combined condition. The Java compiler ignores indentation: an inner if belongs to the branch that syntactically contains it, and an else pairs with the innermost unmatched if.
- **misconception** (wrong rule / right rule; shows `InnerIfIgnoresOuter`): wrong rule: An inner if runs its body whenever its own condition is true, even if the outer if condition is false. Right rule: The inner if is part of the outer branch: it is reached, and its condition tested, only when the outer condition is true.
- **misconception** (wrong rule / right rule; shows `SequentialIfsAreNested`): wrong rule: Of two if statements one after the other, the second runs its body only if both conditions are true. Right rule: Two ifs in sequence are independent: each tests only its own condition.
- **inconsistent trace** (uneven-application rule; shows `InnerIfIgnoresOuter`): Applies the nesting rule (LT) unevenly: on some inputs tests the inner condition even though the outer one was false, or matches an else to the if it is lined up with. (here mixing in: "An inner if runs its body whenever its own condition is true, even if the outer if condition is false")
- **misconception** (wrong rule / right rule; shows `ElseMatchesIndentation`): wrong rule: The else belongs to the if it is lined up with. Right rule: The else belongs to the most recent unmatched if, whatever the indentation.
- **misconception** (wrong rule / right rule; shows `MultipleElseIfBranchesRun`): wrong rule: Every true branch of an else-if chain runs. Right rule: Only the first branch whose condition is true runs.
- **misconception** (wrong rule / right rule; shows `NestedIfsInsteadOfLogicalOperators`): wrong rule: A condition on several values has to be written as nested if statements, one value per if. Right rule: Several conditions combine into one boolean expression with &amp;&amp; and \|\|, e.g. if (x == 0 &amp;&amp; y == 0).

### L1: Unistructural / atom x text surface

L1 for nested conditionals: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

nested conditionals -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

- **names the element** (identity rule): Nested conditionals are if or if-else statements placed inside a branch of another conditional; an else-if chain is the common special case.
- **states the rule** (declarative rule): An if/if-else is a statement, so it can be the body (branch) of another conditional; without braces an else belongs to the innermost if to which it might belong, so braces should be used to resolve ambiguities.

### L2: Multistructural / block x execution / preoperational

L2 for nested conditionals: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

nested conditionals -&gt; L2 (Multistructural): the answer applies the rules of nested conditionals to every part of the code, in order (3 ways).

- **line by line trace** (operational sequencing rule): Test the outer condition; only if control enters the branch that contains the inner if is the inner condition tested; after the inner statement, control leaves the outer statement too.
- **output prediction** (evaluation / result rule): The output is the action of the single path whose conditions all hold along the way: if (a &gt; b) { if (b &gt; c) X; else Y; } else Z; runs X when a &gt; b &gt; c, Y when a &gt; b and b &lt;= c, and Z otherwise.
- **one step execution** (state-transition rule): One execution evaluates the conditions along one path only (outer, then possibly inner) and applies one leaf action; conditions on other paths are never evaluated.

### L3: Relational / relations x function (concrete operational begins)

L3 for nested conditionals: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

nested conditionals -&gt; L3 (Relational): the answer relates the parts (4 ways).

- **relation to neighbour** (composition rule (with a neighbour)): Nesting puts an if or if-else inside a branch of another if-else; when the inner statement fills the else branch it forms an else-if chain.
- **relation to neighbour** (composition rule (with a neighbour)): The dangling-else ambiguity arises when ifs are nested without braces: if &lt;e1&gt; if &lt;e2&gt; A else B attaches else to the inner if.
- **relation to neighbour** (composition rule (with a neighbour)): For more than two mutually exclusive alternatives a chain of if-else statements works, but a switch tests one expression against many values directly.
- **purpose of the whole** (plan / role rule): Plan: decision tree - refine a case analysis step by step (e.g. find the smallest of three values, classify a value into ranges).

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for nested conditionals: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

nested conditionals -&gt; L4 (Extended abstract): the answer reasons beyond the given code (3 ways).

- **predict a change** (conservation rule; shows `InnerIfIgnoresOuter`): Combining if (c1) { if (c2) S; } into if (c1 &amp;&amp; c2) S; preserves behaviour when there are no else parts; adding or removing braces around an inner if can move an else to a different if. Swapping some branches can keep the specification only on certain inputs.
- **transfer to a new program** (applicability rule): Nest conditionals when a second test only makes sense once the first has succeeded or when cases form a tree; use &amp;&amp; for a simple conjunction, an else-if chain for mutually exclusive ranges, and a switch for many discrete values; one or two levels usually suffice.
- **diagnose an error** (error rule): rule broken: Without braces an else pairs with the innermost if, whatever the indentation. Kind: silent logic error. Trigger class: if (a) if (b) X; else Y; written with else under the outer if: Y runs when a is true and b false, not when a is false.

## Same topic

`nested_conditionals` belongs to the topic **Nesting** (`topic1.3.e`). The topic also contains: `dangling_else`, `else_if_chain`, `nested_loops`.

## Rules of the concept (19)

- **folk-meaning rule:** Folk meaning: in prose, indentation and line layout show what belongs to what, and two consecutive 'if' sentences can be heard as one combined condition. The Java compiler ignores indentation: an inner if belongs to the branch that syntactically contains it, and an else pairs with the innermost unmatched if.
- **wrong rule / right rule:** ElseMatchesIndentation: wrong: The else belongs to the if it is lined up with. \| right: The else belongs to the most recent unmatched if, whatever the indentation.
- **wrong rule / right rule:** MultipleElseIfBranchesRun: wrong: Every true branch of an else-if chain runs. \| right: Only the first branch whose condition is true runs.
- **wrong rule / right rule:** NestedIfsInsteadOfLogicalOperators: wrong: A condition on several values has to be written as nested if statements, one value per if. \| right: Several conditions combine into one boolean expression with &amp;&amp; and \|\|, e.g. if (x == 0 &amp;&amp; y == 0).
- **wrong rule / right rule:** InnerIfIgnoresOuter: wrong: An inner if runs its body whenever its own condition is true, even if the outer if condition is false. \| right: The inner if is part of the outer branch: it is reached, and its condition tested, only when the outer condition is true.
- **wrong rule / right rule:** SequentialIfsAreNested: wrong: Of two if statements one after the other, the second runs its body only if both conditions are true. \| right: Two ifs in sequence are independent: each tests only its own condition.
- **uneven-application rule:** Applies the nesting rule (LT) unevenly: on some inputs tests the inner condition even though the outer one was false, or matches an else to the if it is lined up with.
- **identity rule:** Nested conditionals are if or if-else statements placed inside a branch of another conditional; an else-if chain is the common special case.
- **declarative rule:** An if/if-else is a statement, so it can be the body (branch) of another conditional; without braces an else belongs to the innermost if to which it might belong, so braces should be used to resolve ambiguities.
- **operational sequencing rule:** Test the outer condition; only if control enters the branch that contains the inner if is the inner condition tested; after the inner statement, control leaves the outer statement too.
- **evaluation / result rule:** The output is the action of the single path whose conditions all hold along the way: if (a &gt; b) { if (b &gt; c) X; else Y; } else Z; runs X when a &gt; b &gt; c, Y when a &gt; b and b &lt;= c, and Z otherwise.
- **state-transition rule:** One execution evaluates the conditions along one path only (outer, then possibly inner) and applies one leaf action; conditions on other paths are never evaluated.
- **composition rule (with a neighbour):** with if\_else\_statement: Nesting puts an if or if-else inside a branch of another if-else; when the inner statement fills the else branch it forms an else-if chain.
- **composition rule (with a neighbour):** with dangling\_else: The dangling-else ambiguity arises when ifs are nested without braces: if &lt;e1&gt; if &lt;e2&gt; A else B attaches else to the inner if.
- **composition rule (with a neighbour):** with switch\_statement: For more than two mutually exclusive alternatives a chain of if-else statements works, but a switch tests one expression against many values directly.
- **plan / role rule:** Plan: decision tree - refine a case analysis step by step (e.g. find the smallest of three values, classify a value into ranges).
- **conservation rule:** Combining if (c1) { if (c2) S; } into if (c1 &amp;&amp; c2) S; preserves behaviour when there are no else parts; adding or removing braces around an inner if can move an else to a different if. Swapping some branches can keep the specification only on certain inputs.
- **error rule:** rule broken: Without braces an else pairs with the innermost if, whatever the indentation. (silent logic error)
- **applicability rule:** Nest conditionals when a second test only makes sense once the first has succeeded or when cases form a tree; use &amp;&amp; for a simple conjunction, an else-if chain for mutually exclusive ranges, and a switch for many discrete values; one or two levels usually suffice.

## The whole prerequisite chain

- **Everything it builds on (18):** `arithmetic_operators`, `boolean`, `boolean_expression`, `class_declaration`, `comparison_operators`, `control_flow`, `data_type`, `expression`, `identifier`, `if_else_statement`, `if_statement`, `literal`, `logical_operators`, `main_method`, `primitive_type`, `program_text`, `statement`, `variable`
- **Everything that builds on it (1):** `dangling_else`
