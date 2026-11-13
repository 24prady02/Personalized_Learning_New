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

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 16 edges around this concept. The edge logic, the wrong and right rules and the exact rules of the ways are copied word for word from the graph.

## To work on (0)

Nothing is missing for this concept.

## What it needs first (1)

A prerequisite edge means the other concept has to be understood before `short_circuit`.

### `logical_operators` comes before `short_circuit`

*&amp;&amp; \|\| !*

- **Edge:** `pre:logical_operators->short_circuit`
- **Exact edge logic:** &amp;&amp; and \|\| evaluate their second operand only when the first has not already decided the result (false &amp;&amp; x is false, true \|\| x is true).
- **Grounding:** book\_passage
- **Composition rule (R) of `short_circuit` with `logical_operators`:** Short-circuiting is the defining evaluation order of &amp;&amp; and \|\| only; the book's other boolean operators (! and ^, and &amp; / \| if used) evaluate all their operands.
- **Composition rule (R) of `logical_operators` with `short_circuit`:** &amp;&amp; and \|\| are the short-circuit operators: in a guard such as (x != 0 &amp;&amp; y / x &gt; 1) the operand order matters, because the right test runs only when the left one allows it.

## What it leads to (0)

These concepts need `short_circuit` first.

No concept has this one as a prerequisite.

## Learned alongside (0)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

No parallel edge touches this concept.

## Misconceptions (2)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### NoShortCircuit

- **Edge:** `short_circuit` &rarr; `NoShortCircuit` (misconception)
- **Exact edge logic (the wrong rule):** In p &amp;&amp; q, both p and q are always evaluated.
- **Twin logic (the right rule):** In p &amp;&amp; q, q is evaluated only when p is true; in p \|\| q, q is evaluated only when p is false.
- **Wrong belief (on the node):** logical AND/OR always evaluate both sides (Java short-circuits them)
- **Correct rule (on the node):** In p &amp;&amp; q, q is evaluated only when p is true; in p \|\| q, q is evaluated only when p is false.
- **Provenance:** published
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [1] misconception, exact rule:** wrong rule: Logical AND/OR always evaluate both sides. Right rule: In p &amp;&amp; q, q is evaluated only when p is true; in p \|\| q, q is evaluated only when p is false.
- **L0 way [3] inconsistent\_trace, exact rule:** Points to LT (evaluate the left operand; stop if it decides; otherwise evaluate the right). Applied unevenly: on some passes of a loop the student counts the side effect of the right operand (e.g. ++i) although the left operand was already false, or lets a guarded index be read on the pass where the guard failed. (here mixing in: "logical AND/OR always evaluate both sides (Java short-circuits them)")
- **Edge `control_flow` &rarr; `NoShortCircuit`, exact edge logic:** logical AND/OR always evaluate both sides (Java short-circuits them) **Twin logic:** In p &amp;&amp; q, q is evaluated only when p is true; in p \|\| q, q is evaluated only when p is false. (role: context)

### SingleAmpersandForAnd

- **Edge:** `short_circuit` &rarr; `SingleAmpersandForAnd` (misconception)
- **Exact edge logic (the wrong rule):** &amp; and \| are the same as &amp;&amp; and \|\| for conditions, so either can be used.
- **Twin logic (the right rule):** &amp;&amp; and \|\| skip the right operand when the left decides the result; &amp; and \| always evaluate both, which fails when the right side depends on the left (e.g. x != 0 &amp; y / x &gt; 1).
- **Wrong belief (on the node):** &amp; and \| are the same as &amp;&amp; and \|\| for conditions, so either can be used.
- **Correct rule (on the node):** &amp;&amp; and \|\| skip the right operand when the left decides the result; &amp; and \| always evaluate both, which fails when the right side depends on the left (e.g. x != 0 &amp; y / x &gt; 1).
- **Provenance:** published
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [2] misconception, exact rule:** wrong rule: &amp; and \| are the same as &amp;&amp; and \|\| for conditions, so either can be used. Right rule: &amp;&amp; and \|\| skip the right operand when the left decides the result; &amp; and \| always evaluate both, which fails when the right side depends on the left (e.g. x != 0 &amp; y / x &gt; 1).
- **Edge `logical_operators` &rarr; `SingleAmpersandForAnd`, exact edge logic:** &amp; and \| are the same as &amp;&amp; and \|\| for conditions, so either can be used. **Twin logic:** &amp;&amp; and \|\| skip the right operand when the left decides the result; &amp; and \| always evaluate both, which fails when the right side depends on the left (e.g. x != 0 &amp; y / x &gt; 1). (role: context)

## Errors (0)

An error edge states the rule that gets broken in a program, and the right rule.

The graph has no error edge from this concept.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for short circuit: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to short circuit agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

- **Edge:** `short_circuit` &rarr; `short_circuit@L0` (has_level)
- **Exact edge logic:** short circuit -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (4 ways).

Ways (4), each with its exact rule:

- **[0] everyday\_reading** (rule type E, folk-meaning rule): Folk meaning: in maths and logic the value of 'p and q' is read off a truth table with both sides known, so both sides are always 'computed'. Java rule: &amp;&amp; and \|\| evaluate left to right and skip the right operand when the left already decides the result (false &amp;&amp; x, true \|\| x).
- **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `NoShortCircuit`: wrong rule: Logical AND/OR always evaluate both sides. Right rule: In p &amp;&amp; q, q is evaluated only when p is true; in p \|\| q, q is evaluated only when p is false.
- **[2] misconception** (rule type M, wrong rule / right rule) &rarr; `SingleAmpersandForAnd`: wrong rule: &amp; and \| are the same as &amp;&amp; and \|\| for conditions, so either can be used. Right rule: &amp;&amp; and \|\| skip the right operand when the left decides the result; &amp; and \| always evaluate both, which fails when the right side depends on the left (e.g. x != 0 &amp; y / x &gt; 1).
- **[3] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `NoShortCircuit`: Points to LT (evaluate the left operand; stop if it decides; otherwise evaluate the right). Applied unevenly: on some passes of a loop the student counts the side effect of the right operand (e.g. ++i) although the left operand was already false, or lets a guarded index be read on the pass where the guard failed. (here mixing in: "logical AND/OR always evaluate both sides (Java short-circuits them)")

### L1: Unistructural / atom x text surface

L1 for short circuit: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

- **Edge:** `short_circuit` &rarr; `short_circuit@L1` (has_level)
- **Exact edge logic:** short circuit -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

Ways (2), each with its exact rule:

- **[0] names\_the\_element** (rule type N, identity rule): Short-circuit evaluation is the way Java evaluates the logical operators &amp;&amp; and \|\|: the second operand is evaluated only if necessary.
- **[1] states\_the\_rule** (rule type S, declarative rule): In a &amp;&amp; b, b is evaluated only if a is true (false &amp;&amp; b is false); in a \|\| b, b is evaluated only if a is false (true \|\| b is true). &amp;, \| and ^ do not short-circuit.

### L2: Multistructural / block x execution / preoperational

L2 for short circuit: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

- **Edge:** `short_circuit` &rarr; `short_circuit@L2` (has_level)
- **Exact edge logic:** short circuit -&gt; L2 (Multistructural): the answer applies the rules of short circuit to every part of the code, in order (3 ways).

Ways (3), each with its exact rule:

- **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): Evaluate the left operand fully; if it is false (for &amp;&amp;) or true (for \|\|) the whole expression takes that value immediately; otherwise evaluate the right operand, whose value is the result.
- **[1] output\_prediction** (rule type OP, evaluation / result rule): The value is the same as under full evaluation whenever the right operand would have completed normally; with n = 0, (n != 0 &amp;&amp; 10 / n &gt; 1) is false and throws no exception.
- **[2] one\_step\_execution** (rule type OS, state-transition rule): When the right operand is skipped, none of its side effects happen: with i = 0, after (false &amp;&amp; ++i &gt; 0) i is still 0, while (true &amp;&amp; ++i &gt; 0) makes i 1.

### L3: Relational / relations x function (concrete operational begins)

L3 for short circuit: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

- **Edge:** `short_circuit` &rarr; `short_circuit@L3` (has_level)
- **Exact edge logic:** short circuit -&gt; L3 (Relational): the answer relates the parts (2 ways).

Ways (2), each with its exact rule:

- **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Short-circuiting is the defining evaluation order of &amp;&amp; and \|\| only; the book's other boolean operators (! and ^, and &amp; / \| if used) evaluate all their operands.
- **[1] purpose\_of\_the\_whole** (rule type P, plan / role rule): Guard plan: put the safety test first so the risky test runs only when it is safe, e.g. (i &lt; a.length &amp;&amp; a[i] != 0), (count != 0 &amp;&amp; sum / count &gt; 5), (str == null \|\| str.isEmpty()).

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for short circuit: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

- **Edge:** `short_circuit` &rarr; `short_circuit@L4` (has_level)
- **Exact edge logic:** short circuit -&gt; L4 (Extended abstract): the answer reasons beyond the given code (4 ways).

Ways (4), each with its exact rule:

- **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `NoShortCircuit`: Swapping the operands of a guard (a[i] != 0 &amp;&amp; i &lt; a.length) keeps the truth table but lets the risky test run first and throw; replacing &amp;&amp; by &amp; removes the protection; moving a needed side effect into the right operand makes it happen only sometimes.
- **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Rely on short-circuiting when the second test is only valid or meaningful if the first holds (bounds, zero, null) or is expensive; do not put side effects you need into the right operand.
- **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: The protecting test must be the left operand of &amp;&amp; / \|\|. Kind: run-time exception. Trigger class: A guard written after the test it protects, or with &amp; / \|: index out of bounds, divisor 0, or null when the guard condition is false.
- **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: The right operand of &amp;&amp; / \|\| is not always evaluated. Kind: silent logic error. Trigger class: A required side effect (++, assignment, method call) placed in the right operand, on runs where the left operand decides the result.

## Same topic

`short_circuit` belongs to the topic **Booleans** (`topic1.2.e`). The topic also contains: `boolean`, `boolean_expression`, `de_morgan`, `exclusive_or`, `logical_operators`.

## Rules of the concept (15)

- **Book** (TJ-2e, p. 84 (pdf 106)): "short circuit: A way of evaluating logical operators that evaluates the second operand only if necessary."
- **Book** (OT-Op2, ): "These operators exhibit "short-circuiting" behavior, which means that the second operand is evaluated only if needed."
- **Book** (Eck, ): "the computer will never perform the division, since when the computer evaluates (x != 0), it finds that the result is false"
- **E** (folk-meaning rule): Folk meaning: in maths and logic the value of 'p and q' is read off a truth table with both sides known, so both sides are always 'computed'. Java rule: &amp;&amp; and \|\| evaluate left to right and skip the right operand when the left already decides the result (false &amp;&amp; x, true \|\| x).
- **M** (wrong rule / right rule): NoShortCircuit: wrong: Logical AND/OR always evaluate both sides. \| right: In p &amp;&amp; q, q is evaluated only when p is true; in p \|\| q, q is evaluated only when p is false.
- **M** (wrong rule / right rule): SingleAmpersandForAnd: wrong: &amp; and \| are the same as &amp;&amp; and \|\| for conditions, so either can be used. \| right: &amp;&amp; and \|\| skip the right operand when the left decides the result; &amp; and \| always evaluate both, which fails when the right side depends on the left (e.g. x != 0 &amp; y / x &gt; 1).
- **T** (uneven-application rule): Points to LT (evaluate the left operand; stop if it decides; otherwise evaluate the right). Applied unevenly: on some passes of a loop the student counts the side effect of the right operand (e.g. ++i) although the left operand was already false, or lets a guarded index be read on the pass where the guard failed.
- **N** (identity rule): Short-circuit evaluation is the way Java evaluates the logical operators &amp;&amp; and \|\|: the second operand is evaluated only if necessary.
- **S** (declarative rule): In a &amp;&amp; b, b is evaluated only if a is true (false &amp;&amp; b is false); in a \|\| b, b is evaluated only if a is false (true \|\| b is true). &amp;, \| and ^ do not short-circuit.
- **LT** (operational sequencing rule): Evaluate the left operand fully; if it is false (for &amp;&amp;) or true (for \|\|) the whole expression takes that value immediately; otherwise evaluate the right operand, whose value is the result.
- **OP** (evaluation / result rule): The value is the same as under full evaluation whenever the right operand would have completed normally; with n = 0, (n != 0 &amp;&amp; 10 / n &gt; 1) is false and throws no exception.
- **OS** (state-transition rule): When the right operand is skipped, none of its side effects happen: with i = 0, after (false &amp;&amp; ++i &gt; 0) i is still 0, while (true &amp;&amp; ++i &gt; 0) makes i 1.
- **R** (composition rule (with a neighbour)): with logical\_operators: Short-circuiting is the defining evaluation order of &amp;&amp; and \|\| only; the book's other boolean operators (! and ^, and &amp; / \| if used) evaluate all their operands.
- **P** (plan / role rule): Guard plan: put the safety test first so the risky test runs only when it is safe, e.g. (i &lt; a.length &amp;&amp; a[i] != 0), (count != 0 &amp;&amp; sum / count &gt; 5), (str == null \|\| str.isEmpty()).
- **C** (conservation rule): Swapping the operands of a guard (a[i] != 0 &amp;&amp; i &lt; a.length) keeps the truth table but lets the risky test run first and throw; replacing &amp;&amp; by &amp; removes the protection; moving a needed side effect into the right operand makes it happen only sometimes.
- **D** (error rule): rule broken: The protecting test must be the left operand of &amp;&amp; / \|\|. (run-time exception)
- **D** (error rule): rule broken: The right operand of &amp;&amp; / \|\| is not always evaluated. (silent logic error)
- **X** (applicability rule): Rely on short-circuiting when the second test is only valid or meaningful if the first holds (bounds, zero, null) or is expensive; do not put side effects you need into the right operand.

## How it is found in code and answers (reader block)

- **Aliases:** short circuit, short-circuit
- **Code patterns:** `&&|\|\|`
- **Operator symbols:** none
- **Java types:** none

## The whole prerequisite chain

- **Everything it builds on (4):** `boolean`, `data_type`, `logical_operators`, `primitive_type`
- **Everything that builds on it (0):** nothing

## Every edge in this view and its exact edge logic (16)

All the edges drawn in the picture, in the order: prerequisite, parallel, misconception, error, has_level, contains.

**1. `logical_operators` &rarr; `short_circuit`** (prerequisite)

- **Exact edge logic:** &amp;&amp; and \|\| evaluate their second operand only when the first has not already decided the result (false &amp;&amp; x is false, true \|\| x is true).
- **Grounding:** book\_passage
- **Composition rule (R) of `logical_operators` with `short_circuit`:** &amp;&amp; and \|\| are the short-circuit operators: in a guard such as (x != 0 &amp;&amp; y / x &gt; 1) the operand order matters, because the right test runs only when the left one allows it.
- **Composition rule (R) of `short_circuit` with `logical_operators`:** Short-circuiting is the defining evaluation order of &amp;&amp; and \|\| only; the book's other boolean operators (! and ^, and &amp; / \| if used) evaluate all their operands.

**2. `short_circuit` &rarr; `NoShortCircuit`** (misconception)

- **Exact edge logic (the wrong rule):** In p &amp;&amp; q, both p and q are always evaluated.
- **Twin logic (the right rule):** In p &amp;&amp; q, q is evaluated only when p is true; in p \|\| q, q is evaluated only when p is false.
- **Role:** primary

**3. `short_circuit` &rarr; `SingleAmpersandForAnd`** (misconception)

- **Exact edge logic (the wrong rule):** &amp; and \| are the same as &amp;&amp; and \|\| for conditions, so either can be used.
- **Twin logic (the right rule):** &amp;&amp; and \|\| skip the right operand when the left decides the result; &amp; and \| always evaluate both, which fails when the right side depends on the left (e.g. x != 0 &amp; y / x &gt; 1).
- **Role:** primary

**4. `control_flow` &rarr; `NoShortCircuit`** (misconception)

- **Exact edge logic (the wrong rule):** logical AND/OR always evaluate both sides (Java short-circuits them)
- **Twin logic (the right rule):** In p &amp;&amp; q, q is evaluated only when p is true; in p \|\| q, q is evaluated only when p is false.
- **Role:** context

**5. `logical_operators` &rarr; `SingleAmpersandForAnd`** (misconception)

- **Exact edge logic (the wrong rule):** &amp; and \| are the same as &amp;&amp; and \|\| for conditions, so either can be used.
- **Twin logic (the right rule):** &amp;&amp; and \|\| skip the right operand when the left decides the result; &amp; and \| always evaluate both, which fails when the right side depends on the left (e.g. x != 0 &amp; y / x &gt; 1).
- **Role:** context

**6. `short_circuit` &rarr; `short_circuit@L0`** (has_level)

- **Exact edge logic:** short circuit -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (4 ways).
  - **[0] everyday\_reading** (rule type E, folk-meaning rule): Folk meaning: in maths and logic the value of 'p and q' is read off a truth table with both sides known, so both sides are always 'computed'. Java rule: &amp;&amp; and \|\| evaluate left to right and skip the right operand when the left already decides the result (false &amp;&amp; x, true \|\| x).
  - **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `NoShortCircuit`: wrong rule: Logical AND/OR always evaluate both sides. Right rule: In p &amp;&amp; q, q is evaluated only when p is true; in p \|\| q, q is evaluated only when p is false.
  - **[2] misconception** (rule type M, wrong rule / right rule) &rarr; `SingleAmpersandForAnd`: wrong rule: &amp; and \| are the same as &amp;&amp; and \|\| for conditions, so either can be used. Right rule: &amp;&amp; and \|\| skip the right operand when the left decides the result; &amp; and \| always evaluate both, which fails when the right side depends on the left (e.g. x != 0 &amp; y / x &gt; 1).
  - **[3] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `NoShortCircuit`: Points to LT (evaluate the left operand; stop if it decides; otherwise evaluate the right). Applied unevenly: on some passes of a loop the student counts the side effect of the right operand (e.g. ++i) although the left operand was already false, or lets a guarded index be read on the pass where the guard failed. (here mixing in: "logical AND/OR always evaluate both sides (Java short-circuits them)")

**7. `short_circuit` &rarr; `short_circuit@L1`** (has_level)

- **Exact edge logic:** short circuit -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).
  - **[0] names\_the\_element** (rule type N, identity rule): Short-circuit evaluation is the way Java evaluates the logical operators &amp;&amp; and \|\|: the second operand is evaluated only if necessary.
  - **[1] states\_the\_rule** (rule type S, declarative rule): In a &amp;&amp; b, b is evaluated only if a is true (false &amp;&amp; b is false); in a \|\| b, b is evaluated only if a is false (true \|\| b is true). &amp;, \| and ^ do not short-circuit.

**8. `short_circuit` &rarr; `short_circuit@L2`** (has_level)

- **Exact edge logic:** short circuit -&gt; L2 (Multistructural): the answer applies the rules of short circuit to every part of the code, in order (3 ways).
  - **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): Evaluate the left operand fully; if it is false (for &amp;&amp;) or true (for \|\|) the whole expression takes that value immediately; otherwise evaluate the right operand, whose value is the result.
  - **[1] output\_prediction** (rule type OP, evaluation / result rule): The value is the same as under full evaluation whenever the right operand would have completed normally; with n = 0, (n != 0 &amp;&amp; 10 / n &gt; 1) is false and throws no exception.
  - **[2] one\_step\_execution** (rule type OS, state-transition rule): When the right operand is skipped, none of its side effects happen: with i = 0, after (false &amp;&amp; ++i &gt; 0) i is still 0, while (true &amp;&amp; ++i &gt; 0) makes i 1.

**9. `short_circuit` &rarr; `short_circuit@L3`** (has_level)

- **Exact edge logic:** short circuit -&gt; L3 (Relational): the answer relates the parts (2 ways).
  - **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Short-circuiting is the defining evaluation order of &amp;&amp; and \|\| only; the book's other boolean operators (! and ^, and &amp; / \| if used) evaluate all their operands.
  - **[1] purpose\_of\_the\_whole** (rule type P, plan / role rule): Guard plan: put the safety test first so the risky test runs only when it is safe, e.g. (i &lt; a.length &amp;&amp; a[i] != 0), (count != 0 &amp;&amp; sum / count &gt; 5), (str == null \|\| str.isEmpty()).

**10. `short_circuit` &rarr; `short_circuit@L4`** (has_level)

- **Exact edge logic:** short circuit -&gt; L4 (Extended abstract): the answer reasons beyond the given code (4 ways).
  - **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `NoShortCircuit`: Swapping the operands of a guard (a[i] != 0 &amp;&amp; i &lt; a.length) keeps the truth table but lets the risky test run first and throw; replacing &amp;&amp; by &amp; removes the protection; moving a needed side effect into the right operand makes it happen only sometimes.
  - **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Rely on short-circuiting when the second test is only valid or meaningful if the first holds (bounds, zero, null) or is expensive; do not put side effects you need into the right operand.
  - **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: The protecting test must be the left operand of &amp;&amp; / \|\|. Kind: run-time exception. Trigger class: A guard written after the test it protects, or with &amp; / \|: index out of bounds, divisor 0, or null when the guard condition is false.
  - **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: The right operand of &amp;&amp; / \|\| is not always evaluated. Kind: silent logic error. Trigger class: A required side effect (++, assignment, method call) placed in the right operand, on runs where the left operand decides the result.

**11. `topic1.2.e` &rarr; `short_circuit`** (contains)

- topic `topic1.2.e` contains `short_circuit`

**12. `topic1.2.e` &rarr; `boolean`** (contains)

- topic `topic1.2.e` contains `boolean`

**13. `topic1.2.e` &rarr; `boolean_expression`** (contains)

- topic `topic1.2.e` contains `boolean_expression`

**14. `topic1.2.e` &rarr; `de_morgan`** (contains)

- topic `topic1.2.e` contains `de_morgan`

**15. `topic1.2.e` &rarr; `exclusive_or`** (contains)

- topic `topic1.2.e` contains `exclusive_or`

**16. `topic1.2.e` &rarr; `logical_operators`** (contains)

- topic `topic1.2.e` contains `logical_operators`
