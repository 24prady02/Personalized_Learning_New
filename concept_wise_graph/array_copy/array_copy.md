# array_copy (`array_copy`)

making a second, independent array with the same elements: create a new array and copy element by element (or Arrays.copyOf)

Section 1.4 Arrays, topic 1.4.b Memory representation and bounds checking.

![The knowledge graph around array_copy](array_copy.png)

## At a glance

- **Needs first:** `array_traversal`
- **Leads to:** nothing
- **Learned alongside:** `array_aliasing`
- **Misconceptions:** `ArrayEqualityComparesValues`, `AssignmentCopiesObject`
- **Errors:** none
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 20 edges around this concept. The edge logic, the wrong and right rules and the exact rules of the ways are copied word for word from the graph.

## To work on (0)

Nothing is missing for this concept.

## What it needs first (1)

A prerequisite edge means the other concept has to be understood before `array_copy`.

### `array_traversal` comes before `array_copy`

*walking the array with an index loop*

- **Edge:** `pre:array_traversal->array_copy`
- **Exact edge logic:** The elements are copied one at a time by a loop over every index.
- **Grounding:** book\_passage
- **Composition rule (R) of `array_copy` with `array_traversal`:** The copy is a traversal of every index of the original.

## What it leads to (0)

These concepts need `array_copy` first.

No concept has this one as a prerequisite.

## Learned alongside (1)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

### `array_copy` alongside `array_aliasing`

*two variables can refer to the same array*

- **Edge:** `par:array_copy~array_aliasing`
- **Exact edge logic:** b = a makes a second name for the same array (an alias); copying makes a second array: after a copy, changing b[i] leaves a[i] unchanged.
- **Grounding:** book\_passage
- **Composition rule (R) of `array_copy` with `array_aliasing`:** b = a makes an alias of the same array; a copy is a different array: changes through one are not seen through the other.

## Misconceptions (2)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### ArrayEqualityComparesValues

- **Edge:** `array_copy` &rarr; `ArrayEqualityComparesValues` (misconception)
- **Exact edge logic (the wrong rule):** a == b is true when a and b hold the same values.
- **Twin logic (the right rule):** == compares whether the two arrays are the same array, not whether their values are equal.
- **Wrong belief (on the node):** a == b is true when a and b hold the same values.
- **Correct rule (on the node):** == compares whether the two arrays are the same array, not whether their values are equal.
- **Provenance:** textbook
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [3] misconception, exact rule:** wrong rule: a == b is true when a and b hold the same values. Right rule: == compares whether a and b are the same array, so a copy and its original are not ==, even with equal elements.
- **Edge `array_aliasing` &rarr; `ArrayEqualityComparesValues`, exact edge logic:** a == b is true when a and b hold the same values. **Twin logic:** == compares whether the two arrays are the same array, not whether their values are equal. (role: primary)

### AssignmentCopiesObject

- **Edge:** `array_copy` &rarr; `AssignmentCopiesObject` (misconception)
- **Exact edge logic (the wrong rule):** assigning a reference copies the object
- **Twin logic (the right rule):** b = a; copies only the reference, so a and b refer to the same array and b[i] = v also changes a[i].
- **Wrong belief (on the node):** assigning a reference copies the object
- **Correct rule (on the node):** b = a; copies only the reference, so a and b refer to the same array and b[i] = v also changes a[i].
- **Provenance:** published
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [1] misconception, exact rule:** wrong rule: Assigning an array reference copies the array. Right rule: b = a copies only the reference, so a and b refer to the same array; to copy, create a new array and copy each element.
- **L0 way [2] inconsistent\_trace, exact rule:** Applies the copy rule unevenly: copies element by element in one place but writes b = a in another and expects b to be independent. (here mixing in: "assigning a reference copies the object")
- **Edge `array_aliasing` &rarr; `AssignmentCopiesObject`, exact edge logic:** assigning a reference copies the object **Twin logic:** b = a; copies only the reference, so a and b refer to the same array and b[i] = v also changes a[i]. (role: primary)
- **Edge `assignment` &rarr; `AssignmentCopiesObject`, exact edge logic:** b = a; for an array makes b a separate copy, so changing b[i] leaves a[i] unchanged. **Twin logic:** b = a; copies only the reference, so a and b refer to the same array and b[i] = v also changes a[i]. (role: context)

## Errors (0)

An error edge states the rule that gets broken in a program, and the right rule.

The graph has no error edge from this concept.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for array copy: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to array copy agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

- **Edge:** `array_copy` &rarr; `array_copy@L0` (has_level)
- **Exact edge logic:** array copy -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (4 ways).

Ways (4), each with its exact rule:

- **[0] everyday\_reading** (rule type E, folk-meaning rule): Everyday 'copy' (b = a, like copying a value onto paper) suggests a second, separate thing. For arrays, b = a only copies the reference; a separate copy needs a new array with each element copied.
- **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `AssignmentCopiesObject`: wrong rule: Assigning an array reference copies the array. Right rule: b = a copies only the reference, so a and b refer to the same array; to copy, create a new array and copy each element.
- **[2] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `AssignmentCopiesObject`: Applies the copy rule unevenly: copies element by element in one place but writes b = a in another and expects b to be independent. (here mixing in: "assigning a reference copies the object")
- **[3] misconception** (rule type M, wrong rule / right rule) &rarr; `ArrayEqualityComparesValues`: wrong rule: a == b is true when a and b hold the same values. Right rule: == compares whether a and b are the same array, so a copy and its original are not ==, even with equal elements.

### L1: Unistructural / atom x text surface

L1 for array copy: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

- **Edge:** `array_copy` &rarr; `array_copy@L1` (has_level)
- **Exact edge logic:** array copy -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

Ways (2), each with its exact rule:

- **[0] names\_the\_element** (rule type N, identity rule): Array copy: a second, independent array holding the same elements as the first.
- **[1] states\_the\_rule** (rule type S, declarative rule): To copy an array, create a new array of the same length and copy the elements one by one: double[] b = new double[N]; for (int i = 0; i &lt; N; i++) b[i] = a[i]; (java.util.Arrays.copyOf does the same).

### L2: Multistructural / block x execution / preoperational

L2 for array copy: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

- **Edge:** `array_copy` &rarr; `array_copy@L2` (has_level)
- **Exact edge logic:** array copy -&gt; L2 (Multistructural): the answer applies the rules of array copy to every part of the code, in order (3 ways).

Ways (3), each with its exact rule:

- **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): Sequencing: new creates the second array first, then the loop copies a[0], a[1], ... in order into b[0], b[1], ...; after the loop, a and b are separate arrays with equal elements.
- **[1] output\_prediction** (rule type OP, evaluation / result rule): Result: after copying, b[i] == a[i] for every i, but a == b is false; after b[0] = 9, a[0] is unchanged.
- **[2] one\_step\_execution** (rule type OS, state-transition rule): State transition: each pass of the copy loop sets one element of the new array and leaves the original unchanged.

### L3: Relational / relations x function (concrete operational begins)

L3 for array copy: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

- **Edge:** `array_copy` &rarr; `array_copy@L3` (has_level)
- **Exact edge logic:** array copy -&gt; L3 (Relational): the answer relates the parts (3 ways).

Ways (3), each with its exact rule:

- **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): The copy is a traversal of every index of the original.
- **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): b = a makes an alias of the same array; a copy is a different array: changes through one are not seen through the other.
- **[2] purpose\_of\_the\_whole** (rule type P, plan / role rule): Plan: copy an array when the original must stay unchanged while the copy is modified (for example shuffling or sorting a copy).

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for array copy: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

- **Edge:** `array_copy` &rarr; `array_copy@L4` (has_level)
- **Exact edge logic:** array copy -&gt; L4 (Extended abstract): the answer reasons beyond the given code (3 ways).

Ways (3), each with its exact rule:

- **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `AssignmentCopiesObject`: Conservation: changing the copy never changes the original, and the reverse; with an alias every change is shared.
- **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): When an algorithm must change an array but the original is still needed, work on a copy made with new and a loop (or Arrays.copyOf).
- **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: Assignment copies the reference, not the elements. Kind: silent logic error. Trigger class: b = a is used as a copy and then b is modified while a is expected to stay unchanged

## Same topic

`array_copy` belongs to the topic **Memory representation and bounds checking** (`topic1.4.b`). The topic also contains: `array_aliasing`, `array_bounds`, `array_reference`, `loop_guard`, `primitive_vs_reference`, `printing_array_reference`, `program_state`.

## Rules of the concept (15)

- **Book** (SW-1e, p. 89 (pdf 99)): "copy to another array double[] b = new double[N]; for (int i = 0; i &lt; N; i++) b[i] = a[i];"
- **Book** (TJ-2e, p. 112 (pdf 134)): "If you actually want to copy the array, not just the reference, you have to create a new array and copy the elements from one to the other"
- **E** (folk-meaning rule): Everyday 'copy' (b = a, like copying a value onto paper) suggests a second, separate thing. For arrays, b = a only copies the reference; a separate copy needs a new array with each element copied.
- **M** (wrong rule / right rule): AssignmentCopiesObject: wrong: Assigning an array reference copies the array. \| right: b = a copies only the reference, so a and b refer to the same array; to copy, create a new array and copy each element.
- **M** (wrong rule / right rule): ArrayEqualityComparesValues: wrong: a == b is true when a and b hold the same values. \| right: == compares whether a and b are the same array, so a copy and its original are not ==, even with equal elements.
- **T** (uneven-application rule): Applies the copy rule unevenly: copies element by element in one place but writes b = a in another and expects b to be independent.
- **N** (identity rule): Array copy: a second, independent array holding the same elements as the first.
- **S** (declarative rule): To copy an array, create a new array of the same length and copy the elements one by one: double[] b = new double[N]; for (int i = 0; i &lt; N; i++) b[i] = a[i]; (java.util.Arrays.copyOf does the same).
- **LT** (operational sequencing rule): Sequencing: new creates the second array first, then the loop copies a[0], a[1], ... in order into b[0], b[1], ...; after the loop, a and b are separate arrays with equal elements.
- **OP** (evaluation / result rule): Result: after copying, b[i] == a[i] for every i, but a == b is false; after b[0] = 9, a[0] is unchanged.
- **OS** (state-transition rule): State transition: each pass of the copy loop sets one element of the new array and leaves the original unchanged.
- **R** (composition rule (with a neighbour)): with array\_traversal: The copy is a traversal of every index of the original.
- **R** (composition rule (with a neighbour)): with array\_aliasing: b = a makes an alias of the same array; a copy is a different array: changes through one are not seen through the other.
- **P** (plan / role rule): Plan: copy an array when the original must stay unchanged while the copy is modified (for example shuffling or sorting a copy).
- **C** (conservation rule): Conservation: changing the copy never changes the original, and the reverse; with an alias every change is shared.
- **D** (error rule): rule broken: Assignment copies the reference, not the elements. (silent logic error)
- **X** (applicability rule): When an algorithm must change an array but the original is still needed, work on a copy made with new and a loop (or Arrays.copyOf).

## How it is found in code and answers (reader block)

- **Aliases:** copy of the array, exact copy, copies the array
- **Code patterns:** `\bSystem\.arraycopy\s*\(`, `\bArrays\.copyOf\w*\s*\(`, `\.clone\s*\(\s*\)`
- **Operator symbols:** none
- **Java types:** none
- **Signal copy\_loop** (scope statement, decisive): `\b(?P<var>\w+)\s*\[\s*(\w+)\s*\]\s*=\s*(?!(?P=var)\b)(\w+)\s*\[\s*\2\s*\]\s*;?\s*$`

## The whole prerequisite chain

- **Everything it builds on (23):** `arithmetic_operators`, `array_creation`, `array_declaration`, `array_initializer`, `array_traversal`, `boolean`, `boolean_expression`, `comparison_operators`, `data_structure`, `data_type`, `do_while_loop`, `expression`, `for_loop`, `identifier`, `indexing`, `length_field`, `literal`, `logical_operators`, `loop_control`, `loop_variable`, `primitive_type`, `variable`, `while_loop`
- **Everything that builds on it (0):** nothing

## Every edge in this view and its exact edge logic (20)

All the edges drawn in the picture, in the order: prerequisite, parallel, misconception, error, has_level, contains.

**1. `array_traversal` &rarr; `array_copy`** (prerequisite)

- **Exact edge logic:** The elements are copied one at a time by a loop over every index.
- **Grounding:** book\_passage
- **Composition rule (R) of `array_copy` with `array_traversal`:** The copy is a traversal of every index of the original.

**2. `array_copy` &harr; `array_aliasing`** (parallel)

- **Exact edge logic:** b = a makes a second name for the same array (an alias); copying makes a second array: after a copy, changing b[i] leaves a[i] unchanged.
- **Grounding:** book\_passage
- **Composition rule (R) of `array_copy` with `array_aliasing`:** b = a makes an alias of the same array; a copy is a different array: changes through one are not seen through the other.

**3. `array_copy` &rarr; `ArrayEqualityComparesValues`** (misconception)

- **Exact edge logic (the wrong rule):** a == b is true when a and b hold the same values.
- **Twin logic (the right rule):** == compares whether the two arrays are the same array, not whether their values are equal.
- **Role:** context

**4. `array_copy` &rarr; `AssignmentCopiesObject`** (misconception)

- **Exact edge logic (the wrong rule):** assigning a reference copies the object
- **Twin logic (the right rule):** b = a; copies only the reference, so a and b refer to the same array and b[i] = v also changes a[i].
- **Role:** context

**5. `array_aliasing` &rarr; `ArrayEqualityComparesValues`** (misconception)

- **Exact edge logic (the wrong rule):** a == b is true when a and b hold the same values.
- **Twin logic (the right rule):** == compares whether the two arrays are the same array, not whether their values are equal.
- **Role:** primary

**6. `array_aliasing` &rarr; `AssignmentCopiesObject`** (misconception)

- **Exact edge logic (the wrong rule):** assigning a reference copies the object
- **Twin logic (the right rule):** b = a; copies only the reference, so a and b refer to the same array and b[i] = v also changes a[i].
- **Role:** primary

**7. `assignment` &rarr; `AssignmentCopiesObject`** (misconception)

- **Exact edge logic (the wrong rule):** b = a; for an array makes b a separate copy, so changing b[i] leaves a[i] unchanged.
- **Twin logic (the right rule):** b = a; copies only the reference, so a and b refer to the same array and b[i] = v also changes a[i].
- **Role:** context

**8. `array_copy` &rarr; `array_copy@L0`** (has_level)

- **Exact edge logic:** array copy -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (4 ways).
  - **[0] everyday\_reading** (rule type E, folk-meaning rule): Everyday 'copy' (b = a, like copying a value onto paper) suggests a second, separate thing. For arrays, b = a only copies the reference; a separate copy needs a new array with each element copied.
  - **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `AssignmentCopiesObject`: wrong rule: Assigning an array reference copies the array. Right rule: b = a copies only the reference, so a and b refer to the same array; to copy, create a new array and copy each element.
  - **[2] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `AssignmentCopiesObject`: Applies the copy rule unevenly: copies element by element in one place but writes b = a in another and expects b to be independent. (here mixing in: "assigning a reference copies the object")
  - **[3] misconception** (rule type M, wrong rule / right rule) &rarr; `ArrayEqualityComparesValues`: wrong rule: a == b is true when a and b hold the same values. Right rule: == compares whether a and b are the same array, so a copy and its original are not ==, even with equal elements.

**9. `array_copy` &rarr; `array_copy@L1`** (has_level)

- **Exact edge logic:** array copy -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).
  - **[0] names\_the\_element** (rule type N, identity rule): Array copy: a second, independent array holding the same elements as the first.
  - **[1] states\_the\_rule** (rule type S, declarative rule): To copy an array, create a new array of the same length and copy the elements one by one: double[] b = new double[N]; for (int i = 0; i &lt; N; i++) b[i] = a[i]; (java.util.Arrays.copyOf does the same).

**10. `array_copy` &rarr; `array_copy@L2`** (has_level)

- **Exact edge logic:** array copy -&gt; L2 (Multistructural): the answer applies the rules of array copy to every part of the code, in order (3 ways).
  - **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): Sequencing: new creates the second array first, then the loop copies a[0], a[1], ... in order into b[0], b[1], ...; after the loop, a and b are separate arrays with equal elements.
  - **[1] output\_prediction** (rule type OP, evaluation / result rule): Result: after copying, b[i] == a[i] for every i, but a == b is false; after b[0] = 9, a[0] is unchanged.
  - **[2] one\_step\_execution** (rule type OS, state-transition rule): State transition: each pass of the copy loop sets one element of the new array and leaves the original unchanged.

**11. `array_copy` &rarr; `array_copy@L3`** (has_level)

- **Exact edge logic:** array copy -&gt; L3 (Relational): the answer relates the parts (3 ways).
  - **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): The copy is a traversal of every index of the original.
  - **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): b = a makes an alias of the same array; a copy is a different array: changes through one are not seen through the other.
  - **[2] purpose\_of\_the\_whole** (rule type P, plan / role rule): Plan: copy an array when the original must stay unchanged while the copy is modified (for example shuffling or sorting a copy).

**12. `array_copy` &rarr; `array_copy@L4`** (has_level)

- **Exact edge logic:** array copy -&gt; L4 (Extended abstract): the answer reasons beyond the given code (3 ways).
  - **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `AssignmentCopiesObject`: Conservation: changing the copy never changes the original, and the reverse; with an alias every change is shared.
  - **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): When an algorithm must change an array but the original is still needed, work on a copy made with new and a loop (or Arrays.copyOf).
  - **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: Assignment copies the reference, not the elements. Kind: silent logic error. Trigger class: b = a is used as a copy and then b is modified while a is expected to stay unchanged

**13. `topic1.4.b` &rarr; `array_copy`** (contains)

- topic `topic1.4.b` contains `array_copy`

**14. `topic1.4.b` &rarr; `array_aliasing`** (contains)

- topic `topic1.4.b` contains `array_aliasing`

**15. `topic1.4.b` &rarr; `array_bounds`** (contains)

- topic `topic1.4.b` contains `array_bounds`

**16. `topic1.4.b` &rarr; `array_reference`** (contains)

- topic `topic1.4.b` contains `array_reference`

**17. `topic1.4.b` &rarr; `loop_guard`** (contains)

- topic `topic1.4.b` contains `loop_guard`

**18. `topic1.4.b` &rarr; `primitive_vs_reference`** (contains)

- topic `topic1.4.b` contains `primitive_vs_reference`

**19. `topic1.4.b` &rarr; `printing_array_reference`** (contains)

- topic `topic1.4.b` contains `printing_array_reference`

**20. `topic1.4.b` &rarr; `program_state`** (contains)

- topic `topic1.4.b` contains `program_state`
