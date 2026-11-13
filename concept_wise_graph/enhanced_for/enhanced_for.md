# enhanced_for (`enhanced_for`)

for (int x : a) -- the for-each form

Section 1.4 Arrays, topic 1.4.c Setting array values at compile time and at run time.

![The knowledge graph around enhanced_for](enhanced_for.png)

## At a glance

- **Needs first:** `array_traversal`
- **Leads to:** nothing
- **Learned alongside:** nothing
- **Misconceptions:** `ForEachIteratesOverIndices`, `ForEachVariableIsElement`
- **Errors:** none
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 13 edges around this concept. The edge logic, the wrong and right rules and the exact rules of the ways are copied word for word from the graph.

## To work on (0)

Nothing is missing for this concept.

## What it needs first (1)

A prerequisite edge means the other concept has to be understood before `enhanced_for`.

### `array_traversal` comes before `enhanced_for`

*walking the array with an index loop*

- **Edge:** `pre:array_traversal->enhanced_for`
- **Exact edge logic:** for (int x : a) is a traversal that hands the body each value a[i] instead of the index i.
- **Grounding:** book\_passage
- **Composition rule (R) of `enhanced_for` with `array_traversal`:** It is a full forward traversal with the index hidden, so it cannot skip, go backward, stop at a computed index or write a[i].
- **Composition rule (R) of `array_traversal` with `enhanced_for`:** for (int x : a) is a traversal that hands the body each value a[i] and hides the index i.

## What it leads to (0)

These concepts need `enhanced_for` first.

No concept has this one as a prerequisite.

## Learned alongside (0)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

No parallel edge touches this concept.

## Misconceptions (2)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### ForEachIteratesOverIndices

- **Edge:** `enhanced_for` &rarr; `ForEachIteratesOverIndices` (misconception)
- **Exact edge logic (the wrong rule):** In for (int x : a), x takes the index values 0, 1, ..., a.length - 1.
- **Twin logic (the right rule):** In for (int x : a), x takes the element values a[0], a[1] and so on.
- **Wrong belief (on the node):** a for-each loops over indices, not values
- **Correct rule (on the node):** In for (int x : a), x takes the element values a[0], a[1] and so on.
- **Provenance:** published
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [1] misconception, exact rule:** wrong rule: A for-each loops over indices, not values. Right rule: In for (int x : a), x takes the element values a[0], a[1], ... in order; no index is available.
- **L0 way [3] inconsistent\_trace, exact rule:** Points to LT: before each pass the next element is copied into x. Inconsistent application: the trace stores an assignment to x back into a on some passes but not on others. (here mixing in: "a for-each loops over indices, not values")

### ForEachVariableIsElement

- **Edge:** `enhanced_for` &rarr; `ForEachVariableIsElement` (misconception)
- **Exact edge logic (the wrong rule):** Assigning x = v inside for (int x : a) changes the array element.
- **Twin logic (the right rule):** x is a copy of the element, so assigning to x does not change the array.
- **Wrong belief (on the node):** assigning the for-each variable writes back into the array
- **Correct rule (on the node):** x is a copy of the element, so assigning to x does not change the array.
- **Provenance:** published
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [2] misconception, exact rule:** wrong rule: Assigning the for-each variable writes back into the array. Right rule: x is a local copy of the element (as if int x = a[i];), so assigning to x does not change the array.

## Errors (0)

An error edge states the rule that gets broken in a program, and the right rule.

The graph has no error edge from this concept.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for enhanced for: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to enhanced for agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

- **Edge:** `enhanced_for` &rarr; `enhanced_for@L0` (has_level)
- **Exact edge logic:** enhanced for -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (4 ways).

Ways (4), each with its exact rule:

- **[0] everyday\_reading** (rule type E, folk-meaning rule): Folk meaning: the English reading 'for each value in values' suggests the variable is the item itself, so changing it changes the array, or that it ranges over positions. Java rule: on each pass the variable receives a copy of the next element value; the index is hidden and the array is not changed by assigning the variable.
- **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `ForEachIteratesOverIndices`: wrong rule: A for-each loops over indices, not values. Right rule: In for (int x : a), x takes the element values a[0], a[1], ... in order; no index is available.
- **[2] misconception** (rule type M, wrong rule / right rule) &rarr; `ForEachVariableIsElement`: wrong rule: Assigning the for-each variable writes back into the array. Right rule: x is a local copy of the element (as if int x = a[i];), so assigning to x does not change the array.
- **[3] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `ForEachIteratesOverIndices`: Points to LT: before each pass the next element is copied into x. Inconsistent application: the trace stores an assignment to x back into a on some passes but not on others. (here mixing in: "a for-each loops over indices, not values")

### L1: Unistructural / atom x text surface

L1 for enhanced for: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

- **Edge:** `enhanced_for` &rarr; `enhanced_for@L1` (has_level)
- **Exact edge logic:** enhanced for -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

Ways (2), each with its exact rule:

- **[0] names\_the\_element** (rule type N, identity rule): Identity: the enhanced for loop ('for each' loop), a statement that runs its body once per element of an array, giving the body each element value.
- **[1] states\_the\_rule** (rule type S, declarative rule): Declarative: 'for (T x : a) statement', where T is the element type (or a type it converts to); x's scope is the contained statement.

### L2: Multistructural / block x execution / preoperational

L2 for enhanced for: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

- **Edge:** `enhanced_for` &rarr; `enhanced_for@L2` (has_level)
- **Exact edge logic:** enhanced for -&gt; L2 (Multistructural): the answer applies the rules of enhanced for to every part of the code, in order (3 ways).

Ways (3), each with its exact rule:

- **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): Sequencing: equivalent to for (int i = 0; i &lt; a.length; i++) { T x = a[i]; body }. The element is copied into x, the body runs, and then the next element follows, until all a.length elements are done.
- **[1] output\_prediction** (rule type OP, evaluation / result rule): Result: the body runs a.length times with x = a[0], a[1], ...; for int[] a = {1, 2, 3}, summing x gives 6. The loop itself produces no value.
- **[2] one\_step\_execution** (rule type OS, state-transition rule): State transition: each pass sets x to the next element value; assigning to x changes only x, never a[i].

### L3: Relational / relations x function (concrete operational begins)

L3 for enhanced for: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

- **Edge:** `enhanced_for` &rarr; `enhanced_for@L3` (has_level)
- **Exact edge logic:** enhanced for -&gt; L3 (Relational): the answer relates the parts (2 ways).

Ways (2), each with its exact rule:

- **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): It is a full forward traversal with the index hidden, so it cannot skip, go backward, stop at a computed index or write a[i].
- **[1] purpose\_of\_the\_whole** (rule type P, plan / role rule): Plan/role: accumulate or count over all values (gatherer or counter role) when the position is irrelevant, as in histogram counting counts[score]++.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for enhanced for: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

- **Edge:** `enhanced_for` &rarr; `enhanced_for@L4` (has_level)
- **Exact edge logic:** enhanced for -&gt; L4 (Extended abstract): the answer reasons beyond the given code (5 ways).

Ways (5), each with its exact rule:

- **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `ForEachIteratesOverIndices`: Conservation: rewriting an index loop as a for-each keeps every read of a[i] but breaks writes to the array (assigning x has no effect) and loses i, so searches can no longer report positions.
- **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Applicability: use for-each to read every element in order when the index is not needed (sums, counts, printing). Use an index loop when you need the position, write elements, visit part of the array, go backward, or compare neighbours.
- **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: The loop variable must have a type that the element type converts to. Kind: compile-time. Trigger class: for (int x : d) with d a double[] (incompatible types: possible lossy conversion)
- **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: The for-each variable is a copy; it cannot update the array. Kind: silent logic error. Trigger class: x = 0 or x \*= 2 inside the loop is meant to change the elements
- **[4] diagnose\_an\_error** (rule type D, error rule): rule broken: The enhanced for gives no index. Kind: silent logic error. Trigger class: a search written with for-each cannot report where the target is found

## Same topic

`enhanced_for` belongs to the topic **Setting array values at compile time and at run time** (`topic1.4.c`). The topic also contains: `array_initializer`, `array_reversal`, `array_traversal`, `running_extreme`.

## Rules of the concept (16)

- **Book** (TJ-2e, p. 118 (pdf 140)): "This statement is called an enhanced for loop, also known as the "for each" loop."
- **Book** (TJ-2e, p. 119 (pdf 141)): "But they are not helpful when you need to refer to the index, as in search operations"
- **Book** (OT-For, ): "This form is sometimes referred to as the enhanced for statement, and can be used to make your loops more compact and easy to read."
- **E** (folk-meaning rule): Folk meaning: the English reading 'for each value in values' suggests the variable is the item itself, so changing it changes the array, or that it ranges over positions. Java rule: on each pass the variable receives a copy of the next element value; the index is hidden and the array is not changed by assigning the variable.
- **M** (wrong rule / right rule): ForEachIteratesOverIndices: wrong: A for-each loops over indices, not values. \| right: In for (int x : a), x takes the element values a[0], a[1], ... in order; no index is available.
- **M** (wrong rule / right rule): ForEachVariableIsElement: wrong: Assigning the for-each variable writes back into the array. \| right: x is a local copy of the element (as if int x = a[i];), so assigning to x does not change the array.
- **T** (uneven-application rule): Points to LT: before each pass the next element is copied into x. Inconsistent application: the trace stores an assignment to x back into a on some passes but not on others.
- **N** (identity rule): Identity: the enhanced for loop ('for each' loop), a statement that runs its body once per element of an array, giving the body each element value.
- **S** (declarative rule): Declarative: 'for (T x : a) statement', where T is the element type (or a type it converts to); x's scope is the contained statement.
- **LT** (operational sequencing rule): Sequencing: equivalent to for (int i = 0; i &lt; a.length; i++) { T x = a[i]; body }. The element is copied into x, the body runs, and then the next element follows, until all a.length elements are done.
- **OP** (evaluation / result rule): Result: the body runs a.length times with x = a[0], a[1], ...; for int[] a = {1, 2, 3}, summing x gives 6. The loop itself produces no value.
- **OS** (state-transition rule): State transition: each pass sets x to the next element value; assigning to x changes only x, never a[i].
- **R** (composition rule (with a neighbour)): with array\_traversal: It is a full forward traversal with the index hidden, so it cannot skip, go backward, stop at a computed index or write a[i].
- **P** (plan / role rule): Plan/role: accumulate or count over all values (gatherer or counter role) when the position is irrelevant, as in histogram counting counts[score]++.
- **C** (conservation rule): Conservation: rewriting an index loop as a for-each keeps every read of a[i] but breaks writes to the array (assigning x has no effect) and loses i, so searches can no longer report positions.
- **D** (error rule): rule broken: The loop variable must have a type that the element type converts to. (compile-time)
- **D** (error rule): rule broken: The for-each variable is a copy; it cannot update the array. (silent logic error)
- **D** (error rule): rule broken: The enhanced for gives no index. (silent logic error)
- **X** (applicability rule): Applicability: use for-each to read every element in order when the index is not needed (sums, counts, printing). Use an index loop when you need the position, write elements, visit part of the array, go backward, or compare neighbours.

## How it is found in code and answers (reader block)

- **Aliases:** for each, enhanced for
- **Code patterns:** `\bfor\s*\(\s*(?:final\s+)?[\w\[\]]+\s+\w+\s*:`
- **Operator symbols:** none
- **Java types:** none

## The whole prerequisite chain

- **Everything it builds on (23):** `arithmetic_operators`, `array_creation`, `array_declaration`, `array_initializer`, `array_traversal`, `boolean`, `boolean_expression`, `comparison_operators`, `data_structure`, `data_type`, `do_while_loop`, `expression`, `for_loop`, `identifier`, `indexing`, `length_field`, `literal`, `logical_operators`, `loop_control`, `loop_variable`, `primitive_type`, `variable`, `while_loop`
- **Everything that builds on it (0):** nothing

## Every edge in this view and its exact edge logic (13)

All the edges drawn in the picture, in the order: prerequisite, parallel, misconception, error, has_level, contains.

**1. `array_traversal` &rarr; `enhanced_for`** (prerequisite)

- **Exact edge logic:** for (int x : a) is a traversal that hands the body each value a[i] instead of the index i.
- **Grounding:** book\_passage
- **Composition rule (R) of `array_traversal` with `enhanced_for`:** for (int x : a) is a traversal that hands the body each value a[i] and hides the index i.
- **Composition rule (R) of `enhanced_for` with `array_traversal`:** It is a full forward traversal with the index hidden, so it cannot skip, go backward, stop at a computed index or write a[i].

**2. `enhanced_for` &rarr; `ForEachIteratesOverIndices`** (misconception)

- **Exact edge logic (the wrong rule):** In for (int x : a), x takes the index values 0, 1, ..., a.length - 1.
- **Twin logic (the right rule):** In for (int x : a), x takes the element values a[0], a[1] and so on.
- **Role:** primary

**3. `enhanced_for` &rarr; `ForEachVariableIsElement`** (misconception)

- **Exact edge logic (the wrong rule):** Assigning x = v inside for (int x : a) changes the array element.
- **Twin logic (the right rule):** x is a copy of the element, so assigning to x does not change the array.
- **Role:** primary

**4. `enhanced_for` &rarr; `enhanced_for@L0`** (has_level)

- **Exact edge logic:** enhanced for -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (4 ways).
  - **[0] everyday\_reading** (rule type E, folk-meaning rule): Folk meaning: the English reading 'for each value in values' suggests the variable is the item itself, so changing it changes the array, or that it ranges over positions. Java rule: on each pass the variable receives a copy of the next element value; the index is hidden and the array is not changed by assigning the variable.
  - **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `ForEachIteratesOverIndices`: wrong rule: A for-each loops over indices, not values. Right rule: In for (int x : a), x takes the element values a[0], a[1], ... in order; no index is available.
  - **[2] misconception** (rule type M, wrong rule / right rule) &rarr; `ForEachVariableIsElement`: wrong rule: Assigning the for-each variable writes back into the array. Right rule: x is a local copy of the element (as if int x = a[i];), so assigning to x does not change the array.
  - **[3] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `ForEachIteratesOverIndices`: Points to LT: before each pass the next element is copied into x. Inconsistent application: the trace stores an assignment to x back into a on some passes but not on others. (here mixing in: "a for-each loops over indices, not values")

**5. `enhanced_for` &rarr; `enhanced_for@L1`** (has_level)

- **Exact edge logic:** enhanced for -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).
  - **[0] names\_the\_element** (rule type N, identity rule): Identity: the enhanced for loop ('for each' loop), a statement that runs its body once per element of an array, giving the body each element value.
  - **[1] states\_the\_rule** (rule type S, declarative rule): Declarative: 'for (T x : a) statement', where T is the element type (or a type it converts to); x's scope is the contained statement.

**6. `enhanced_for` &rarr; `enhanced_for@L2`** (has_level)

- **Exact edge logic:** enhanced for -&gt; L2 (Multistructural): the answer applies the rules of enhanced for to every part of the code, in order (3 ways).
  - **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): Sequencing: equivalent to for (int i = 0; i &lt; a.length; i++) { T x = a[i]; body }. The element is copied into x, the body runs, and then the next element follows, until all a.length elements are done.
  - **[1] output\_prediction** (rule type OP, evaluation / result rule): Result: the body runs a.length times with x = a[0], a[1], ...; for int[] a = {1, 2, 3}, summing x gives 6. The loop itself produces no value.
  - **[2] one\_step\_execution** (rule type OS, state-transition rule): State transition: each pass sets x to the next element value; assigning to x changes only x, never a[i].

**7. `enhanced_for` &rarr; `enhanced_for@L3`** (has_level)

- **Exact edge logic:** enhanced for -&gt; L3 (Relational): the answer relates the parts (2 ways).
  - **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): It is a full forward traversal with the index hidden, so it cannot skip, go backward, stop at a computed index or write a[i].
  - **[1] purpose\_of\_the\_whole** (rule type P, plan / role rule): Plan/role: accumulate or count over all values (gatherer or counter role) when the position is irrelevant, as in histogram counting counts[score]++.

**8. `enhanced_for` &rarr; `enhanced_for@L4`** (has_level)

- **Exact edge logic:** enhanced for -&gt; L4 (Extended abstract): the answer reasons beyond the given code (5 ways).
  - **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `ForEachIteratesOverIndices`: Conservation: rewriting an index loop as a for-each keeps every read of a[i] but breaks writes to the array (assigning x has no effect) and loses i, so searches can no longer report positions.
  - **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Applicability: use for-each to read every element in order when the index is not needed (sums, counts, printing). Use an index loop when you need the position, write elements, visit part of the array, go backward, or compare neighbours.
  - **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: The loop variable must have a type that the element type converts to. Kind: compile-time. Trigger class: for (int x : d) with d a double[] (incompatible types: possible lossy conversion)
  - **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: The for-each variable is a copy; it cannot update the array. Kind: silent logic error. Trigger class: x = 0 or x \*= 2 inside the loop is meant to change the elements
  - **[4] diagnose\_an\_error** (rule type D, error rule): rule broken: The enhanced for gives no index. Kind: silent logic error. Trigger class: a search written with for-each cannot report where the target is found

**9. `topic1.4.c` &rarr; `enhanced_for`** (contains)

- topic `topic1.4.c` contains `enhanced_for`

**10. `topic1.4.c` &rarr; `array_initializer`** (contains)

- topic `topic1.4.c` contains `array_initializer`

**11. `topic1.4.c` &rarr; `array_reversal`** (contains)

- topic `topic1.4.c` contains `array_reversal`

**12. `topic1.4.c` &rarr; `array_traversal`** (contains)

- topic `topic1.4.c` contains `array_traversal`

**13. `topic1.4.c` &rarr; `running_extreme`** (contains)

- topic `topic1.4.c` contains `running_extreme`
