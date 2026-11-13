# array_initializer (`array_initializer`)

{1, 2, 3} literal initialization

Section 1.4 Arrays, topic 1.4.c Setting array values at compile time and at run time.

![The knowledge graph around array_initializer](array_initializer.png)

## At a glance

- **Needs first:** `array_creation`, `array_declaration`
- **Leads to:** `indexing`, `length_field`, `lookup_table`
- **Learned alongside:** nothing
- **Misconceptions:** `ArrayBracketCountIsLength`, `ArrayInitializerContentsInBrackets`
- **Errors:** none
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 20 edges around this concept, each explained in the graph's own words.

## What it needs first (2)

A prerequisite edge means the other concept has to be understood before `array_initializer`.

### `array_creation` comes before `array_initializer`

*new int[n] -- allocates n slots*

{v0, v1, ..., vk} is a shorthand that creates an array of length k + 1 and fills it in one step.

- **Grounding:** book passage
- **How `array_initializer` combines with `array_creation`:** An initializer implies array creation: it is shorthand for new T[k+1] followed by k+1 element assignments, so new is not written.
- **How `array_creation` combines with `array_initializer`:** An initializer {v0, ..., vk} implies creation of an array of length k+1, so new is not written.

### `array_declaration` comes before `array_initializer`

*int[] a; -- declares an array variable*

int[] a = {1, 2, 3}; declares the array variable and creates and fills the array in one statement.

- **Grounding:** book passage

## What it leads to (3)

These concepts need `array_initializer` first.

### `array_initializer` comes before `indexing`

*a[i] -- 0-based access*

The values listed in braces are stored at indices 0, 1, 2, ... in order, and a[i] reads the value at index i.

- **Grounding:** spec passage

### `array_initializer` comes before `length_field`

*a.length is a field, not a method*

An array made from a literal has as many elements as values listed, and a.length gives that number.

- **Grounding:** spec passage

### `array_initializer` comes before `lookup_table`

*an array of precomputed values or names indexed by position*

A lookup table is usually an array of fixed values written as a literal and read by index.

- **Grounding:** book passage

## Learned alongside (0)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

No parallel edge touches this concept.

## Misconceptions (2)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### ArrayBracketCountIsLength

- **Wrong rule:** The number of brackets in an array type or initializer is the array's length.
- **Right rule:** Brackets give the number of dimensions; the length is set at creation.
- **Role of this concept:** context
- **Shows at level L0 as:** misconception: wrong rule: The number of brackets in an array type or initializer is the array's length. Right rule: Brackets give the number of dimensions; an initializer's length is the number of values between its braces.
- **Also an edge from `array_creation`:** The number of brackets in an array type or initializer is the array's length.
- **Also an edge from `array_declaration`:** The number of brackets in an array type or initializer is the array's length.
- **Also an edge from `multidimensional_array`:** The number of brackets in an array type or initializer is the array's length.

### ArrayInitializerContentsInBrackets

- **Wrong rule:** Starting values go in square brackets, like int[] a = [v0, v1];.
- **Right rule:** Starting values go in braces, like int[] a = {v0, v1};.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: Initializer values go in [] instead of {}. Right rule: Starting values go in braces, as in int[] a = {v0, v1};; brackets only mark the type or an index.
- **Shows at level L0 as:** inconsistent trace: Points to LT: an array of length k+1 is created, then v0..vk are stored at indices 0..k in order. Inconsistent application: the trace puts the first value at index 1 for one initializer but at index 0 for another, or counts the length differently. (here mixing in: "initializer values go in [] instead of {}")

## Errors (0)

An error edge states the rule that gets broken in a program, and the right rule.

The graph has no error edge from this concept.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for array initializer: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to array initializer agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

array initializer -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (4 ways).

- **everyday reading** (folk-meaning rule): Folk meaning: in maths, braces {1, 2, 3} denote a set (unordered, no repeats) and brackets [1, 2, 3] a list, so novices write int[] a = [1, 2, 3] or expect {1, 1, 2} to have 2 elements. Java rule: braces enclose an ordered, comma-separated list whose count (repeats included) is the length.
- **misconception** (wrong rule / right rule; shows `ArrayInitializerContentsInBrackets`): wrong rule: Initializer values go in [] instead of {}. Right rule: Starting values go in braces, as in int[] a = {v0, v1};; brackets only mark the type or an index.
- **inconsistent trace** (uneven-application rule; shows `ArrayInitializerContentsInBrackets`): Points to LT: an array of length k+1 is created, then v0..vk are stored at indices 0..k in order. Inconsistent application: the trace puts the first value at index 1 for one initializer but at index 0 for another, or counts the length differently. (here mixing in: "initializer values go in [] instead of {}")
- **misconception** (wrong rule / right rule; shows `ArrayBracketCountIsLength`): wrong rule: The number of brackets in an array type or initializer is the array's length. Right rule: Brackets give the number of dimensions; an initializer's length is the number of values between its braces.

### L1: Unistructural / atom x text surface

L1 for array initializer: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

array initializer -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

- **names the element** (identity rule): Identity: an array initializer is a brace-enclosed, comma-separated list of values that creates and fills an array in one step.
- **states the rule** (declarative rule): Declarative: 'T[] a = {v0, ..., vk};' declares, creates (no new needed) and initializes an array of length k+1. For 2-D arrays each row is its own brace list. The bare form is legal only in a declaration; elsewhere write new T[]{...}.

### L2: Multistructural / block x execution / preoperational

L2 for array initializer: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

array initializer -&gt; L2 (Multistructural): the answer applies the rules of array initializer to every part of the code, in order (3 ways).

- **line by line trace** (operational sequencing rule): Sequencing: the array of length k+1 is created, the initializer expressions are evaluated left to right and stored in a[0], a[1], ..., a[k], and then the reference is assigned to a.
- **output prediction** (evaluation / result rule): Result: int[] a = {1, 2, 3}; gives a.length == 3, a[0] == 1, a[2] == 3. String[] suit = {"Clubs", "Diamonds", "Hearts", "Spades"}; gives suit.length == 4.
- **one step execution** (state-transition rule): State transition: one execution creates one array holding the listed values and sets the variable to its reference.

### L3: Relational / relations x function (concrete operational begins)

L3 for array initializer: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

array initializer -&gt; L3 (Relational): the answer relates the parts (2 ways).

- **relation to neighbour** (composition rule (with a neighbour)): An initializer implies array creation: it is shorthand for new T[k+1] followed by k+1 element assignments, so new is not written.
- **purpose of the whole** (plan / role rule): Plan/role: build small fixed tables of constants known when the program is written (suits, ranks, month names), usually used as fixed-value lookup tables.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for array initializer: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

array initializer -&gt; L4 (Extended abstract): the answer reasons beyond the given code (5 ways).

- **predict a change** (conservation rule; shows `ArrayInitializerContentsInBrackets`): Conservation: adding or removing a value changes the length. Code that uses a.length (e.g. rank.length) adapts, while code with a hard-coded size breaks. Reordering values changes which index holds which value.
- **transfer to a new program** (applicability rule): Applicability: use an initializer when all values are known at compile time and the array is small. When the values must be computed at run time, create the array with new and fill it in a loop.
- **diagnose an error** (error rule): rule broken: Initializer values are enclosed in braces. Kind: compile-time. Trigger class: brackets are used, as in int[] a = [1, 2, 3]; (illegal start of expression)
- **diagnose an error** (error rule): rule broken: The bare {...} form is allowed only in a declaration. Kind: compile-time. Trigger class: a = {1, 2, 3}; used as a later assignment (array constants can only be used in initializers)
- **diagnose an error** (error rule): rule broken: Each value must be assignable to the element type. Kind: compile-time. Trigger class: int[] a = {1, 2.5}; (incompatible types: possible lossy conversion from double to int)

## Same topic

`array_initializer` belongs to the topic **Setting array values at compile time and at run time** (`topic1.4.c`). The topic also contains: `array_reversal`, `array_traversal`, `enhanced_for`, `running_extreme`.

## Rules of the concept (16)

- **folk-meaning rule:** Folk meaning: in maths, braces {1, 2, 3} denote a set (unordered, no repeats) and brackets [1, 2, 3] a list, so novices write int[] a = [1, 2, 3] or expect {1, 1, 2} to have 2 elements. Java rule: braces enclose an ordered, comma-separated list whose count (repeats included) is the length.
- **wrong rule / right rule:** ArrayInitializerContentsInBrackets: wrong: Initializer values go in [] instead of {}. \| right: Starting values go in braces, as in int[] a = {v0, v1};; brackets only mark the type or an index.
- **wrong rule / right rule:** ArrayBracketCountIsLength: wrong: The number of brackets in an array type or initializer is the array's length. \| right: Brackets give the number of dimensions; an initializer's length is the number of values between its braces.
- **uneven-application rule:** Points to LT: an array of length k+1 is created, then v0..vk are stored at indices 0..k in order. Inconsistent application: the trace puts the first value at index 1 for one initializer but at index 0 for another, or counts the length differently.
- **identity rule:** Identity: an array initializer is a brace-enclosed, comma-separated list of values that creates and fills an array in one step.
- **declarative rule:** Declarative: 'T[] a = {v0, ..., vk};' declares, creates (no new needed) and initializes an array of length k+1. For 2-D arrays each row is its own brace list. The bare form is legal only in a declaration; elsewhere write new T[]{...}.
- **operational sequencing rule:** Sequencing: the array of length k+1 is created, the initializer expressions are evaluated left to right and stored in a[0], a[1], ..., a[k], and then the reference is assigned to a.
- **evaluation / result rule:** Result: int[] a = {1, 2, 3}; gives a.length == 3, a[0] == 1, a[2] == 3. String[] suit = {"Clubs", "Diamonds", "Hearts", "Spades"}; gives suit.length == 4.
- **state-transition rule:** State transition: one execution creates one array holding the listed values and sets the variable to its reference.
- **composition rule (with a neighbour):** with array\_creation: An initializer implies array creation: it is shorthand for new T[k+1] followed by k+1 element assignments, so new is not written.
- **plan / role rule:** Plan/role: build small fixed tables of constants known when the program is written (suits, ranks, month names), usually used as fixed-value lookup tables.
- **conservation rule:** Conservation: adding or removing a value changes the length. Code that uses a.length (e.g. rank.length) adapts, while code with a hard-coded size breaks. Reordering values changes which index holds which value.
- **error rule:** rule broken: Initializer values are enclosed in braces. (compile-time)
- **error rule:** rule broken: The bare {...} form is allowed only in a declaration. (compile-time)
- **error rule:** rule broken: Each value must be assignable to the element type. (compile-time)
- **applicability rule:** Applicability: use an initializer when all values are known at compile time and the array is small. When the values must be computed at run time, create the array with new and fill it in a loop.

## The whole prerequisite chain

- **Everything it builds on (4):** `array_creation`, `array_declaration`, `data_structure`, `data_type`
- **Everything that builds on it (36):** `args_length`, `array_bounds`, `array_copy`, `array_exchange`, `array_reversal`, `array_traversal`, `boolean_flag_array`, `convergence_rate`, `dangling_pages`, `enhanced_for`, `frequency_counting`, `function_plotting`, `indexing`, `input_graph`, `length_field`, `lookup_table`, `loop_guard`, `markov_chain`, `matrix_operations`, `multidimensional_array`, `normalization`, `off_by_one_error`, `power_method`, `ragged_array`, `random_move`, `row_major_order`, `run_time_error`, `running_extreme`, `sampling_without_replacement`, `shuffle`, `simulation_loop`, `space_time_tradeoff`, `standard_audio`, `transition_matrix`, `two_dimensional_array`, `two_models`
