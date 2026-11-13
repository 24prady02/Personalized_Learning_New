# array_reversal (`array_reversal`)

reversing an array in place

Section 1.4 Arrays, topic 1.4.c Setting array values at compile time and at run time.

![The knowledge graph around array_reversal](array_reversal.png)

## At a glance

- **Needs first:** `array_exchange`, `array_traversal`, `length_field`
- **Leads to:** nothing
- **Learned alongside:** nothing
- **Misconceptions:** `OffByOneBound`, `ReverseFullLength`
- **Errors:** none
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 21 edges around this concept, each explained in the graph's own words.

## What it needs first (3)

A prerequisite edge means the other concept has to be understood before `array_reversal`.

### `array_exchange` comes before `array_reversal`

*swap a[i] and a[j] through a temporary variable*

Reversal exchanges a[i] with a[N-1-i] for each i in the first half of the array.

- **Grounding:** book passage
- **How `array_reversal` combines with `array_exchange`:** Reversal is a loop of exchanges a[i] &lt;-&gt; a[N-1-i], so it inherits the exchange idiom and its temporary variable.
- **How `array_exchange` combines with `array_reversal`:** Reversal exchanges a[i] with a[N-1-i] for each i in the first half.

### `array_traversal` comes before `array_reversal`

*walking the array with an index loop*

Reversal traverses only the first half of the array (i &lt; N/2), exchanging each a[i] with its mirror a[N-1-i].

- **Grounding:** book passage
- **How `array_reversal` combines with `array_traversal`:** Reversal traverses only the first half (i &lt; N/2) while indexing the second half through the mirror index.
- **How `array_traversal` combines with `array_reversal`:** Reversal traverses only the first half (i &lt; N/2), exchanging each a[i] with its mirror a[N-1-i].

### `length_field` comes before `array_reversal`

*a.length is a field, not a method*

Reversal pairs a[i] with a[a.length-1-i], counting back from the last index a.length-1.

- **Grounding:** book passage

## What it leads to (0)

These concepts need `array_reversal` first.

No concept has this one as a prerequisite.

## Learned alongside (0)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

No parallel edge touches this concept.

## Misconceptions (2)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### OffByOneBound

- **Wrong rule:** &lt; vs &lt;= and 0..n vs 0..n-1 are interchangeable
- **Right rule:** for (i = 0; i &lt; n; i++) runs n times with i going up to n - 1; with &lt;= it runs n + 1 times and reaches i = n.
- **Role of this concept:** context
- **Shows at level L0 as:** misconception: wrong rule: &lt; vs &lt;= and 0..n vs 0..n-1 are interchangeable. Right rule: The mirror of a[i] is a[N-1-i] (not a[N-i]), and the loop runs while i &lt; N/2.
- **Also an edge from `array_bounds`:** &lt; vs &lt;= and 0..n vs 0..n-1 are interchangeable
- **Also an edge from `array_traversal`:** &lt; vs &lt;= and 0..n vs 0..n-1 are interchangeable
- **Also an edge from `boolean_flag_array`:** &lt; vs &lt;= and 0..n vs 0..n-1 are interchangeable
- **Also an edge from `loop_control`:** i &lt; n and i &lt;= n mean the same, so the loop runs until i equals n and the last pass can use a[n].
- **Also an edge from `off_by_one_error`:** &lt; vs &lt;= and 0..n vs 0..n-1 are interchangeable
- **Also an edge from `simulation_loop`:** t &lt; T and t &lt;= T give the same number of moves.

### ReverseFullLength

- **Wrong rule:** Reversing an array needs a swap for every one of the n positions.
- **Right rule:** Swapping for i &lt; n/2 is enough; going to n undoes the reversal.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: Reversing an array needs a swap for every one of the n positions. Right rule: Swapping for i &lt; n/2 is enough; going to n undoes the reversal.
- **Shows at level L0 as:** inconsistent trace: Points to LT: for i from 0 while i &lt; N/2, save a[i] in temp, copy a[N-1-i] to a[i], and copy temp to a[N-1-i]. Inconsistent application: the trace exchanges a mirror pair on some passes but only copies one way on others, or computes the mirror with an updated i. (here mixing in: "Reversing an array needs a swap for every one of the n positions")

## Errors (0)

An error edge states the rule that gets broken in a program, and the right rule.

The graph has no error edge from this concept.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for array reversal: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to array reversal agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

array reversal -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (4 ways).

- **everyday reading** (folk-meaning rule): Folk meaning: 'reverse every element' suggests one swap per position, so the loop runs over all n positions. Java rule: each exchange moves two elements, so n/2 exchanges (i &lt; N/2) reverse the array, and n exchanges reverse it twice, restoring the original.
- **misconception** (wrong rule / right rule; shows `ReverseFullLength`): wrong rule: Reversing an array needs a swap for every one of the n positions. Right rule: Swapping for i &lt; n/2 is enough; going to n undoes the reversal.
- **inconsistent trace** (uneven-application rule; shows `ReverseFullLength`): Points to LT: for i from 0 while i &lt; N/2, save a[i] in temp, copy a[N-1-i] to a[i], and copy temp to a[N-1-i]. Inconsistent application: the trace exchanges a mirror pair on some passes but only copies one way on others, or computes the mirror with an updated i. (here mixing in: "Reversing an array needs a swap for every one of the n positions")
- **misconception** (wrong rule / right rule; shows `OffByOneBound`): wrong rule: &lt; vs &lt;= and 0..n vs 0..n-1 are interchangeable. Right rule: The mirror of a[i] is a[N-1-i] (not a[N-i]), and the loop runs while i &lt; N/2.

### L1: Unistructural / atom x text surface

L1 for array reversal: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

array reversal -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

- **names the element** (identity rule): Identity: in-place reversal rearranges an array so that a[i] and a[N-1-i] trade places for every i, without a second array.
- **states the rule** (declarative rule): Declarative: for (int i = 0; i &lt; N/2; i++) { temp = b[i]; b[i] = b[N-1-i]; b[N-1-i] = temp; }.

### L2: Multistructural / block x execution / preoperational

L2 for array reversal: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

array reversal -&gt; L2 (Multistructural): the answer applies the rules of array reversal to every part of the code, in order (3 ways).

- **line by line trace** (operational sequencing rule): Sequencing: pass i exchanges the i-th pair from the outside in: (0, N-1), (1, N-2), ... For odd N the middle element is never touched, because N/2 rounds down.
- **output prediction** (evaluation / result rule): Result: {1, 2, 3, 4, 5} becomes {5, 4, 3, 2, 1} with the same length and the same values.
- **one step execution** (state-transition rule): State transition: each pass changes exactly two elements, a[i] and a[N-1-i] (plus temp); other elements and N are unchanged.

### L3: Relational / relations x function (concrete operational begins)

L3 for array reversal: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

array reversal -&gt; L3 (Relational): the answer relates the parts (3 ways).

- **relation to neighbour** (composition rule (with a neighbour)): Reversal is a loop of exchanges a[i] &lt;-&gt; a[N-1-i], so it inherits the exchange idiom and its temporary variable.
- **relation to neighbour** (composition rule (with a neighbour)): Reversal traverses only the first half (i &lt; N/2) while indexing the second half through the mirror index.
- **purpose of the whole** (plan / role rule): Plan/role: a two-ended mirror-swap plan in which the array plays the role of an organizer, its elements rearranged in place.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for array reversal: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

array reversal -&gt; L4 (Extended abstract): the answer reasons beyond the given code (5 ways).

- **predict a change** (conservation rule; shows `ReverseFullLength`): Conservation: the multiset of values is preserved (only exchanges are used). Reversal is its own inverse: reversing twice, or running the loop to N instead of N/2, gives back the original order.
- **transfer to a new program** (applicability rule): Applicability: reverse in place when the original order is no longer needed and memory matters. When the original must be kept, copy into a new array (b[N-1-i] = a[i]) or just traverse backwards.
- **diagnose an error** (error rule): rule broken: Only the first half is traversed. Kind: silent logic error. Trigger class: the loop runs i &lt; N, so every pair is swapped twice and the array ends unchanged
- **diagnose an error** (error rule): rule broken: The mirror index is N-1-i. Kind: run-time exception. Trigger class: the mirror is written a[N-i], which is a[N] at i = 0 (ArrayIndexOutOfBoundsException)
- **diagnose an error** (error rule): rule broken: The exchange needs a temporary variable. Kind: silent logic error. Trigger class: a[i] = a[N-1-i]; a[N-1-i] = a[i]; leaves the array a palindrome of its second half

## Same topic

`array_reversal` belongs to the topic **Setting array values at compile time and at run time** (`topic1.4.c`). The topic also contains: `array_initializer`, `array_traversal`, `enhanced_for`, `running_extreme`.

## Rules of the concept (17)

- **folk-meaning rule:** Folk meaning: 'reverse every element' suggests one swap per position, so the loop runs over all n positions. Java rule: each exchange moves two elements, so n/2 exchanges (i &lt; N/2) reverse the array, and n exchanges reverse it twice, restoring the original.
- **wrong rule / right rule:** OffByOneBound: wrong: &lt; vs &lt;= and 0..n vs 0..n-1 are interchangeable. \| right: The mirror of a[i] is a[N-1-i] (not a[N-i]), and the loop runs while i &lt; N/2.
- **wrong rule / right rule:** ReverseFullLength: wrong: Reversing an array needs a swap for every one of the n positions. \| right: Swapping for i &lt; n/2 is enough; going to n undoes the reversal.
- **uneven-application rule:** Points to LT: for i from 0 while i &lt; N/2, save a[i] in temp, copy a[N-1-i] to a[i], and copy temp to a[N-1-i]. Inconsistent application: the trace exchanges a mirror pair on some passes but only copies one way on others, or computes the mirror with an updated i.
- **identity rule:** Identity: in-place reversal rearranges an array so that a[i] and a[N-1-i] trade places for every i, without a second array.
- **declarative rule:** Declarative: for (int i = 0; i &lt; N/2; i++) { temp = b[i]; b[i] = b[N-1-i]; b[N-1-i] = temp; }.
- **operational sequencing rule:** Sequencing: pass i exchanges the i-th pair from the outside in: (0, N-1), (1, N-2), ... For odd N the middle element is never touched, because N/2 rounds down.
- **evaluation / result rule:** Result: {1, 2, 3, 4, 5} becomes {5, 4, 3, 2, 1} with the same length and the same values.
- **state-transition rule:** State transition: each pass changes exactly two elements, a[i] and a[N-1-i] (plus temp); other elements and N are unchanged.
- **composition rule (with a neighbour):** with array\_exchange: Reversal is a loop of exchanges a[i] &lt;-&gt; a[N-1-i], so it inherits the exchange idiom and its temporary variable.
- **composition rule (with a neighbour):** with array\_traversal: Reversal traverses only the first half (i &lt; N/2) while indexing the second half through the mirror index.
- **plan / role rule:** Plan/role: a two-ended mirror-swap plan in which the array plays the role of an organizer, its elements rearranged in place.
- **conservation rule:** Conservation: the multiset of values is preserved (only exchanges are used). Reversal is its own inverse: reversing twice, or running the loop to N instead of N/2, gives back the original order.
- **error rule:** rule broken: Only the first half is traversed. (silent logic error)
- **error rule:** rule broken: The mirror index is N-1-i. (run-time exception)
- **error rule:** rule broken: The exchange needs a temporary variable. (silent logic error)
- **applicability rule:** Applicability: reverse in place when the original order is no longer needed and memory matters. When the original must be kept, copy into a new array (b[N-1-i] = a[i]) or just traverse backwards.

## The whole prerequisite chain

- **Everything it builds on (26):** `arithmetic_operators`, `array_creation`, `array_declaration`, `array_exchange`, `array_initializer`, `array_traversal`, `assignment`, `boolean`, `boolean_expression`, `comparison_operators`, `data_structure`, `data_type`, `declaration`, `do_while_loop`, `expression`, `for_loop`, `identifier`, `indexing`, `length_field`, `literal`, `logical_operators`, `loop_control`, `loop_variable`, `primitive_type`, `variable`, `while_loop`
- **Everything that builds on it (0):** nothing
