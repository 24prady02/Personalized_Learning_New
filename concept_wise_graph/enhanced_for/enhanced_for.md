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

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 13 edges around this concept, each explained in the graph's own words.

## What it needs first (1)

A prerequisite edge means the other concept has to be understood before `enhanced_for`.

### `array_traversal` comes before `enhanced_for`

*walking the array with an index loop*

for (int x : a) is a traversal that hands the body each value a[i] instead of the index i.

- **Grounding:** book passage
- **How `enhanced_for` combines with `array_traversal`:** It is a full forward traversal with the index hidden, so it cannot skip, go backward, stop at a computed index or write a[i].
- **How `array_traversal` combines with `enhanced_for`:** for (int x : a) is a traversal that hands the body each value a[i] and hides the index i.

## What it leads to (0)

These concepts need `enhanced_for` first.

No concept has this one as a prerequisite.

## Learned alongside (0)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

No parallel edge touches this concept.

## Misconceptions (2)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### ForEachIteratesOverIndices

- **Wrong rule:** In for (int x : a), x takes the index values 0, 1, ..., a.length - 1.
- **Right rule:** In for (int x : a), x takes the element values a[0], a[1] and so on.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: A for-each loops over indices, not values. Right rule: In for (int x : a), x takes the element values a[0], a[1], ... in order; no index is available.
- **Shows at level L0 as:** inconsistent trace: Points to LT: before each pass the next element is copied into x. Inconsistent application: the trace stores an assignment to x back into a on some passes but not on others. (here mixing in: "a for-each loops over indices, not values")

### ForEachVariableIsElement

- **Wrong rule:** Assigning x = v inside for (int x : a) changes the array element.
- **Right rule:** x is a copy of the element, so assigning to x does not change the array.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: Assigning the for-each variable writes back into the array. Right rule: x is a local copy of the element (as if int x = a[i];), so assigning to x does not change the array.

## Errors (0)

An error edge states the rule that gets broken in a program, and the right rule.

The graph has no error edge from this concept.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for enhanced for: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to enhanced for agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

enhanced for -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (4 ways).

- **everyday reading** (folk-meaning rule): Folk meaning: the English reading 'for each value in values' suggests the variable is the item itself, so changing it changes the array, or that it ranges over positions. Java rule: on each pass the variable receives a copy of the next element value; the index is hidden and the array is not changed by assigning the variable.
- **misconception** (wrong rule / right rule; shows `ForEachIteratesOverIndices`): wrong rule: A for-each loops over indices, not values. Right rule: In for (int x : a), x takes the element values a[0], a[1], ... in order; no index is available.
- **misconception** (wrong rule / right rule; shows `ForEachVariableIsElement`): wrong rule: Assigning the for-each variable writes back into the array. Right rule: x is a local copy of the element (as if int x = a[i];), so assigning to x does not change the array.
- **inconsistent trace** (uneven-application rule; shows `ForEachIteratesOverIndices`): Points to LT: before each pass the next element is copied into x. Inconsistent application: the trace stores an assignment to x back into a on some passes but not on others. (here mixing in: "a for-each loops over indices, not values")

### L1: Unistructural / atom x text surface

L1 for enhanced for: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

enhanced for -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

- **names the element** (identity rule): Identity: the enhanced for loop ('for each' loop), a statement that runs its body once per element of an array, giving the body each element value.
- **states the rule** (declarative rule): Declarative: 'for (T x : a) statement', where T is the element type (or a type it converts to); x's scope is the contained statement.

### L2: Multistructural / block x execution / preoperational

L2 for enhanced for: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

enhanced for -&gt; L2 (Multistructural): the answer applies the rules of enhanced for to every part of the code, in order (3 ways).

- **line by line trace** (operational sequencing rule): Sequencing: equivalent to for (int i = 0; i &lt; a.length; i++) { T x = a[i]; body }. The element is copied into x, the body runs, and then the next element follows, until all a.length elements are done.
- **output prediction** (evaluation / result rule): Result: the body runs a.length times with x = a[0], a[1], ...; for int[] a = {1, 2, 3}, summing x gives 6. The loop itself produces no value.
- **one step execution** (state-transition rule): State transition: each pass sets x to the next element value; assigning to x changes only x, never a[i].

### L3: Relational / relations x function (concrete operational begins)

L3 for enhanced for: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

enhanced for -&gt; L3 (Relational): the answer relates the parts (2 ways).

- **relation to neighbour** (composition rule (with a neighbour)): It is a full forward traversal with the index hidden, so it cannot skip, go backward, stop at a computed index or write a[i].
- **purpose of the whole** (plan / role rule): Plan/role: accumulate or count over all values (gatherer or counter role) when the position is irrelevant, as in histogram counting counts[score]++.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for enhanced for: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

enhanced for -&gt; L4 (Extended abstract): the answer reasons beyond the given code (5 ways).

- **predict a change** (conservation rule; shows `ForEachIteratesOverIndices`): Conservation: rewriting an index loop as a for-each keeps every read of a[i] but breaks writes to the array (assigning x has no effect) and loses i, so searches can no longer report positions.
- **transfer to a new program** (applicability rule): Applicability: use for-each to read every element in order when the index is not needed (sums, counts, printing). Use an index loop when you need the position, write elements, visit part of the array, go backward, or compare neighbours.
- **diagnose an error** (error rule): rule broken: The loop variable must have a type that the element type converts to. Kind: compile-time. Trigger class: for (int x : d) with d a double[] (incompatible types: possible lossy conversion)
- **diagnose an error** (error rule): rule broken: The for-each variable is a copy; it cannot update the array. Kind: silent logic error. Trigger class: x = 0 or x \*= 2 inside the loop is meant to change the elements
- **diagnose an error** (error rule): rule broken: The enhanced for gives no index. Kind: silent logic error. Trigger class: a search written with for-each cannot report where the target is found

## Same topic

`enhanced_for` belongs to the topic **Setting array values at compile time and at run time** (`topic1.4.c`). The topic also contains: `array_initializer`, `array_reversal`, `array_traversal`, `running_extreme`.

## Rules of the concept (16)

- **folk-meaning rule:** Folk meaning: the English reading 'for each value in values' suggests the variable is the item itself, so changing it changes the array, or that it ranges over positions. Java rule: on each pass the variable receives a copy of the next element value; the index is hidden and the array is not changed by assigning the variable.
- **wrong rule / right rule:** ForEachIteratesOverIndices: wrong: A for-each loops over indices, not values. \| right: In for (int x : a), x takes the element values a[0], a[1], ... in order; no index is available.
- **wrong rule / right rule:** ForEachVariableIsElement: wrong: Assigning the for-each variable writes back into the array. \| right: x is a local copy of the element (as if int x = a[i];), so assigning to x does not change the array.
- **uneven-application rule:** Points to LT: before each pass the next element is copied into x. Inconsistent application: the trace stores an assignment to x back into a on some passes but not on others.
- **identity rule:** Identity: the enhanced for loop ('for each' loop), a statement that runs its body once per element of an array, giving the body each element value.
- **declarative rule:** Declarative: 'for (T x : a) statement', where T is the element type (or a type it converts to); x's scope is the contained statement.
- **operational sequencing rule:** Sequencing: equivalent to for (int i = 0; i &lt; a.length; i++) { T x = a[i]; body }. The element is copied into x, the body runs, and then the next element follows, until all a.length elements are done.
- **evaluation / result rule:** Result: the body runs a.length times with x = a[0], a[1], ...; for int[] a = {1, 2, 3}, summing x gives 6. The loop itself produces no value.
- **state-transition rule:** State transition: each pass sets x to the next element value; assigning to x changes only x, never a[i].
- **composition rule (with a neighbour):** with array\_traversal: It is a full forward traversal with the index hidden, so it cannot skip, go backward, stop at a computed index or write a[i].
- **plan / role rule:** Plan/role: accumulate or count over all values (gatherer or counter role) when the position is irrelevant, as in histogram counting counts[score]++.
- **conservation rule:** Conservation: rewriting an index loop as a for-each keeps every read of a[i] but breaks writes to the array (assigning x has no effect) and loses i, so searches can no longer report positions.
- **error rule:** rule broken: The loop variable must have a type that the element type converts to. (compile-time)
- **error rule:** rule broken: The for-each variable is a copy; it cannot update the array. (silent logic error)
- **error rule:** rule broken: The enhanced for gives no index. (silent logic error)
- **applicability rule:** Applicability: use for-each to read every element in order when the index is not needed (sums, counts, printing). Use an index loop when you need the position, write elements, visit part of the array, go backward, or compare neighbours.

## The whole prerequisite chain

- **Everything it builds on (23):** `arithmetic_operators`, `array_creation`, `array_declaration`, `array_initializer`, `array_traversal`, `boolean`, `boolean_expression`, `comparison_operators`, `data_structure`, `data_type`, `do_while_loop`, `expression`, `for_loop`, `identifier`, `indexing`, `length_field`, `literal`, `logical_operators`, `loop_control`, `loop_variable`, `primitive_type`, `variable`, `while_loop`
- **Everything that builds on it (0):** nothing
