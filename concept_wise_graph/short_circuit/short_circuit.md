# short_circuit (`short_circuit`)

&amp;&amp;/\|\| stop evaluating once the result is known

Section 1.2 Built-in Types of Data, topic 1.2.e Booleans.

![The knowledge graph around short_circuit](short_circuit.png)

## At a glance

- **Needs first:** `logical_operators`
- **Leads to:** nothing
- **Learned alongside:** nothing
- **Misconceptions:** `NoShortCircuit`, `SingleAmpersandForAnd`
- **Errors:** none
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 16 edges around this concept, each explained in the graph's own words.

## What it needs first (1)

A prerequisite edge means the other concept has to be understood before `short_circuit`.

### `logical_operators` comes before `short_circuit`

*&amp;&amp; \|\| !*

&amp;&amp; and \|\| evaluate their second operand only when the first has not already decided the result (false &amp;&amp; x is false, true \|\| x is true).

- **Grounding:** book passage
- **How `short_circuit` combines with `logical_operators`:** Short-circuiting is the defining evaluation order of &amp;&amp; and \|\| only; the book's other boolean operators (! and ^, and &amp; / \| if used) evaluate all their operands.
- **How `logical_operators` combines with `short_circuit`:** &amp;&amp; and \|\| are the short-circuit operators: in a guard such as (x != 0 &amp;&amp; y / x &gt; 1) the operand order matters, because the right test runs only when the left one allows it.

## What it leads to (0)

These concepts need `short_circuit` first.

No concept has this one as a prerequisite.

## Learned alongside (0)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

No parallel edge touches this concept.

## Misconceptions (2)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### NoShortCircuit

- **Wrong rule:** In p &amp;&amp; q, both p and q are always evaluated.
- **Right rule:** In p &amp;&amp; q, q is evaluated only when p is true; in p \|\| q, q is evaluated only when p is false.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: Logical AND/OR always evaluate both sides. Right rule: In p &amp;&amp; q, q is evaluated only when p is true; in p \|\| q, q is evaluated only when p is false.
- **Shows at level L0 as:** inconsistent trace: Points to LT (evaluate the left operand; stop if it decides; otherwise evaluate the right). Applied unevenly: on some passes of a loop the student counts the side effect of the right operand (e.g. ++i) although the left operand was already false, or lets a guarded index be read on the pass where the guard failed. (here mixing in: "logical AND/OR always evaluate both sides (Java short-circuits them)")
- **Also an edge from `control_flow`:** logical AND/OR always evaluate both sides (Java short-circuits them)

### SingleAmpersandForAnd

- **Wrong rule:** &amp; and \| are the same as &amp;&amp; and \|\| for conditions, so either can be used.
- **Right rule:** &amp;&amp; and \|\| skip the right operand when the left decides the result; &amp; and \| always evaluate both, which fails when the right side depends on the left (e.g. x != 0 &amp; y / x &gt; 1).
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: &amp; and \| are the same as &amp;&amp; and \|\| for conditions, so either can be used. Right rule: &amp;&amp; and \|\| skip the right operand when the left decides the result; &amp; and \| always evaluate both, which fails when the right side depends on the left (e.g. x != 0 &amp; y / x &gt; 1).
- **Also an edge from `logical_operators`:** &amp; and \| are the same as &amp;&amp; and \|\| for conditions, so either can be used.

## Errors (0)

An error edge states the rule that gets broken in a program, and the right rule.

The graph has no error edge from this concept.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for short circuit: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to short circuit agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

short circuit -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (4 ways).

- **everyday reading** (folk-meaning rule): Folk meaning: in maths and logic the value of 'p and q' is read off a truth table with both sides known, so both sides are always 'computed'. Java rule: &amp;&amp; and \|\| evaluate left to right and skip the right operand when the left already decides the result (false &amp;&amp; x, true \|\| x).
- **misconception** (wrong rule / right rule; shows `NoShortCircuit`): wrong rule: Logical AND/OR always evaluate both sides. Right rule: In p &amp;&amp; q, q is evaluated only when p is true; in p \|\| q, q is evaluated only when p is false.
- **misconception** (wrong rule / right rule; shows `SingleAmpersandForAnd`): wrong rule: &amp; and \| are the same as &amp;&amp; and \|\| for conditions, so either can be used. Right rule: &amp;&amp; and \|\| skip the right operand when the left decides the result; &amp; and \| always evaluate both, which fails when the right side depends on the left (e.g. x != 0 &amp; y / x &gt; 1).
- **inconsistent trace** (uneven-application rule; shows `NoShortCircuit`): Points to LT (evaluate the left operand; stop if it decides; otherwise evaluate the right). Applied unevenly: on some passes of a loop the student counts the side effect of the right operand (e.g. ++i) although the left operand was already false, or lets a guarded index be read on the pass where the guard failed. (here mixing in: "logical AND/OR always evaluate both sides (Java short-circuits them)")

### L1: Unistructural / atom x text surface

L1 for short circuit: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

short circuit -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

- **names the element** (identity rule): Short-circuit evaluation is the way Java evaluates the logical operators &amp;&amp; and \|\|: the second operand is evaluated only if necessary.
- **states the rule** (declarative rule): In a &amp;&amp; b, b is evaluated only if a is true (false &amp;&amp; b is false); in a \|\| b, b is evaluated only if a is false (true \|\| b is true). &amp;, \| and ^ do not short-circuit.

### L2: Multistructural / block x execution / preoperational

L2 for short circuit: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

short circuit -&gt; L2 (Multistructural): the answer applies the rules of short circuit to every part of the code, in order (3 ways).

- **line by line trace** (operational sequencing rule): Evaluate the left operand fully; if it is false (for &amp;&amp;) or true (for \|\|) the whole expression takes that value immediately; otherwise evaluate the right operand, whose value is the result.
- **output prediction** (evaluation / result rule): The value is the same as under full evaluation whenever the right operand would have completed normally; with n = 0, (n != 0 &amp;&amp; 10 / n &gt; 1) is false and throws no exception.
- **one step execution** (state-transition rule): When the right operand is skipped, none of its side effects happen: with i = 0, after (false &amp;&amp; ++i &gt; 0) i is still 0, while (true &amp;&amp; ++i &gt; 0) makes i 1.

### L3: Relational / relations x function (concrete operational begins)

L3 for short circuit: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

short circuit -&gt; L3 (Relational): the answer relates the parts (2 ways).

- **relation to neighbour** (composition rule (with a neighbour)): Short-circuiting is the defining evaluation order of &amp;&amp; and \|\| only; the book's other boolean operators (! and ^, and &amp; / \| if used) evaluate all their operands.
- **purpose of the whole** (plan / role rule): Guard plan: put the safety test first so the risky test runs only when it is safe, e.g. (i &lt; a.length &amp;&amp; a[i] != 0), (count != 0 &amp;&amp; sum / count &gt; 5), (str == null \|\| str.isEmpty()).

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for short circuit: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

short circuit -&gt; L4 (Extended abstract): the answer reasons beyond the given code (4 ways).

- **predict a change** (conservation rule; shows `NoShortCircuit`): Swapping the operands of a guard (a[i] != 0 &amp;&amp; i &lt; a.length) keeps the truth table but lets the risky test run first and throw; replacing &amp;&amp; by &amp; removes the protection; moving a needed side effect into the right operand makes it happen only sometimes.
- **transfer to a new program** (applicability rule): Rely on short-circuiting when the second test is only valid or meaningful if the first holds (bounds, zero, null) or is expensive; do not put side effects you need into the right operand.
- **diagnose an error** (error rule): rule broken: The protecting test must be the left operand of &amp;&amp; / \|\|. Kind: run-time exception. Trigger class: A guard written after the test it protects, or with &amp; / \|: index out of bounds, divisor 0, or null when the guard condition is false.
- **diagnose an error** (error rule): rule broken: The right operand of &amp;&amp; / \|\| is not always evaluated. Kind: silent logic error. Trigger class: A required side effect (++, assignment, method call) placed in the right operand, on runs where the left operand decides the result.

## Same topic

`short_circuit` belongs to the topic **Booleans** (`topic1.2.e`). The topic also contains: `boolean`, `boolean_expression`, `de_morgan`, `exclusive_or`, `logical_operators`.

## Rules of the concept (15)

- **folk-meaning rule:** Folk meaning: in maths and logic the value of 'p and q' is read off a truth table with both sides known, so both sides are always 'computed'. Java rule: &amp;&amp; and \|\| evaluate left to right and skip the right operand when the left already decides the result (false &amp;&amp; x, true \|\| x).
- **wrong rule / right rule:** NoShortCircuit: wrong: Logical AND/OR always evaluate both sides. \| right: In p &amp;&amp; q, q is evaluated only when p is true; in p \|\| q, q is evaluated only when p is false.
- **wrong rule / right rule:** SingleAmpersandForAnd: wrong: &amp; and \| are the same as &amp;&amp; and \|\| for conditions, so either can be used. \| right: &amp;&amp; and \|\| skip the right operand when the left decides the result; &amp; and \| always evaluate both, which fails when the right side depends on the left (e.g. x != 0 &amp; y / x &gt; 1).
- **uneven-application rule:** Points to LT (evaluate the left operand; stop if it decides; otherwise evaluate the right). Applied unevenly: on some passes of a loop the student counts the side effect of the right operand (e.g. ++i) although the left operand was already false, or lets a guarded index be read on the pass where the guard failed.
- **identity rule:** Short-circuit evaluation is the way Java evaluates the logical operators &amp;&amp; and \|\|: the second operand is evaluated only if necessary.
- **declarative rule:** In a &amp;&amp; b, b is evaluated only if a is true (false &amp;&amp; b is false); in a \|\| b, b is evaluated only if a is false (true \|\| b is true). &amp;, \| and ^ do not short-circuit.
- **operational sequencing rule:** Evaluate the left operand fully; if it is false (for &amp;&amp;) or true (for \|\|) the whole expression takes that value immediately; otherwise evaluate the right operand, whose value is the result.
- **evaluation / result rule:** The value is the same as under full evaluation whenever the right operand would have completed normally; with n = 0, (n != 0 &amp;&amp; 10 / n &gt; 1) is false and throws no exception.
- **state-transition rule:** When the right operand is skipped, none of its side effects happen: with i = 0, after (false &amp;&amp; ++i &gt; 0) i is still 0, while (true &amp;&amp; ++i &gt; 0) makes i 1.
- **composition rule (with a neighbour):** with logical\_operators: Short-circuiting is the defining evaluation order of &amp;&amp; and \|\| only; the book's other boolean operators (! and ^, and &amp; / \| if used) evaluate all their operands.
- **plan / role rule:** Guard plan: put the safety test first so the risky test runs only when it is safe, e.g. (i &lt; a.length &amp;&amp; a[i] != 0), (count != 0 &amp;&amp; sum / count &gt; 5), (str == null \|\| str.isEmpty()).
- **conservation rule:** Swapping the operands of a guard (a[i] != 0 &amp;&amp; i &lt; a.length) keeps the truth table but lets the risky test run first and throw; replacing &amp;&amp; by &amp; removes the protection; moving a needed side effect into the right operand makes it happen only sometimes.
- **error rule:** rule broken: The protecting test must be the left operand of &amp;&amp; / \|\|. (run-time exception)
- **error rule:** rule broken: The right operand of &amp;&amp; / \|\| is not always evaluated. (silent logic error)
- **applicability rule:** Rely on short-circuiting when the second test is only valid or meaningful if the first holds (bounds, zero, null) or is expensive; do not put side effects you need into the right operand.

## The whole prerequisite chain

- **Everything it builds on (4):** `boolean`, `data_type`, `logical_operators`, `primitive_type`
- **Everything that builds on it (0):** nothing
