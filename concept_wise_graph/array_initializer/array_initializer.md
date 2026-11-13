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

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 20 edges around this concept. The edge logic, the wrong and right rules and the exact rules of the ways are copied word for word from the graph.

## To work on (0)

Nothing is missing for this concept.

## What it needs first (2)

A prerequisite edge means the other concept has to be understood before `array_initializer`.

### `array_creation` comes before `array_initializer`

*new int[n] -- allocates n slots*

- **Edge:** `pre:array_creation->array_initializer`
- **Exact edge logic:** {v0, v1, ..., vk} is a shorthand that creates an array of length k + 1 and fills it in one step.
- **Grounding:** book\_passage
- **Composition rule (R) of `array_initializer` with `array_creation`:** An initializer implies array creation: it is shorthand for new T[k+1] followed by k+1 element assignments, so new is not written.
- **Composition rule (R) of `array_creation` with `array_initializer`:** An initializer {v0, ..., vk} implies creation of an array of length k+1, so new is not written.

### `array_declaration` comes before `array_initializer`

*int[] a; -- declares an array variable*

- **Edge:** `pre:array_declaration->array_initializer`
- **Exact edge logic:** int[] a = {1, 2, 3}; declares the array variable and creates and fills the array in one statement.
- **Grounding:** book\_passage

## What it leads to (3)

These concepts need `array_initializer` first.

### `array_initializer` comes before `indexing`

*a[i] -- 0-based access*

- **Edge:** `pre:array_initializer->indexing`
- **Exact edge logic:** The values listed in braces are stored at indices 0, 1, 2, ... in order, and a[i] reads the value at index i.
- **Grounding:** spec\_passage

### `array_initializer` comes before `length_field`

*a.length is a field, not a method*

- **Edge:** `pre:array_initializer->length_field`
- **Exact edge logic:** An array made from a literal has as many elements as values listed, and a.length gives that number.
- **Grounding:** spec\_passage

### `array_initializer` comes before `lookup_table`

*an array of precomputed values or names indexed by position*

- **Edge:** `pre:array_initializer->lookup_table`
- **Exact edge logic:** A lookup table is usually an array of fixed values written as a literal and read by index.
- **Grounding:** book\_passage

## Learned alongside (0)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

No parallel edge touches this concept.

## Misconceptions (2)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### ArrayBracketCountIsLength

- **Edge:** `array_initializer` &rarr; `ArrayBracketCountIsLength` (misconception)
- **Exact edge logic (the wrong rule):** The number of brackets in an array type or initializer is the array's length.
- **Twin logic (the right rule):** Brackets give the number of dimensions; the length is set at creation.
- **Wrong belief (on the node):** The number of brackets in an array type or initializer is the array's length.
- **Correct rule (on the node):** Brackets give the number of dimensions; the length is set at creation.
- **Provenance:** published
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [3] misconception, exact rule:** wrong rule: The number of brackets in an array type or initializer is the array's length. Right rule: Brackets give the number of dimensions; an initializer's length is the number of values between its braces.
- **Edge `array_creation` &rarr; `ArrayBracketCountIsLength`, exact edge logic:** The number of brackets in an array type or initializer is the array's length. **Twin logic:** Brackets give the number of dimensions; the length is set at creation. (role: context)
- **Edge `array_declaration` &rarr; `ArrayBracketCountIsLength`, exact edge logic:** The number of brackets in an array type or initializer is the array's length. **Twin logic:** Brackets give the number of dimensions; the length is set at creation. (role: primary)
- **Edge `multidimensional_array` &rarr; `ArrayBracketCountIsLength`, exact edge logic:** The number of brackets in an array type or initializer is the array's length. **Twin logic:** Brackets give the number of dimensions; the length is set at creation. (role: context)

### ArrayInitializerContentsInBrackets

- **Edge:** `array_initializer` &rarr; `ArrayInitializerContentsInBrackets` (misconception)
- **Exact edge logic (the wrong rule):** Starting values go in square brackets, like int[] a = [v0, v1];.
- **Twin logic (the right rule):** Starting values go in braces, like int[] a = {v0, v1};.
- **Wrong belief (on the node):** initializer values go in [] instead of {}
- **Correct rule (on the node):** Starting values go in braces, like int[] a = {v0, v1};.
- **Provenance:** published
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [1] misconception, exact rule:** wrong rule: Initializer values go in [] instead of {}. Right rule: Starting values go in braces, as in int[] a = {v0, v1};; brackets only mark the type or an index.
- **L0 way [2] inconsistent\_trace, exact rule:** Points to LT: an array of length k+1 is created, then v0..vk are stored at indices 0..k in order. Inconsistent application: the trace puts the first value at index 1 for one initializer but at index 0 for another, or counts the length differently. (here mixing in: "initializer values go in [] instead of {}")

## Errors (0)

An error edge states the rule that gets broken in a program, and the right rule.

The graph has no error edge from this concept.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for array initializer: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to array initializer agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

- **Edge:** `array_initializer` &rarr; `array_initializer@L0` (has_level)
- **Exact edge logic:** array initializer -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (4 ways).

Ways (4), each with its exact rule:

- **[0] everyday\_reading** (rule type E, folk-meaning rule): Folk meaning: in maths, braces {1, 2, 3} denote a set (unordered, no repeats) and brackets [1, 2, 3] a list, so novices write int[] a = [1, 2, 3] or expect {1, 1, 2} to have 2 elements. Java rule: braces enclose an ordered, comma-separated list whose count (repeats included) is the length.
- **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `ArrayInitializerContentsInBrackets`: wrong rule: Initializer values go in [] instead of {}. Right rule: Starting values go in braces, as in int[] a = {v0, v1};; brackets only mark the type or an index.
- **[2] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `ArrayInitializerContentsInBrackets`: Points to LT: an array of length k+1 is created, then v0..vk are stored at indices 0..k in order. Inconsistent application: the trace puts the first value at index 1 for one initializer but at index 0 for another, or counts the length differently. (here mixing in: "initializer values go in [] instead of {}")
- **[3] misconception** (rule type M, wrong rule / right rule) &rarr; `ArrayBracketCountIsLength`: wrong rule: The number of brackets in an array type or initializer is the array's length. Right rule: Brackets give the number of dimensions; an initializer's length is the number of values between its braces.

### L1: Unistructural / atom x text surface

L1 for array initializer: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

- **Edge:** `array_initializer` &rarr; `array_initializer@L1` (has_level)
- **Exact edge logic:** array initializer -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

Ways (2), each with its exact rule:

- **[0] names\_the\_element** (rule type N, identity rule): Identity: an array initializer is a brace-enclosed, comma-separated list of values that creates and fills an array in one step.
- **[1] states\_the\_rule** (rule type S, declarative rule): Declarative: 'T[] a = {v0, ..., vk};' declares, creates (no new needed) and initializes an array of length k+1. For 2-D arrays each row is its own brace list. The bare form is legal only in a declaration; elsewhere write new T[]{...}.

### L2: Multistructural / block x execution / preoperational

L2 for array initializer: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

- **Edge:** `array_initializer` &rarr; `array_initializer@L2` (has_level)
- **Exact edge logic:** array initializer -&gt; L2 (Multistructural): the answer applies the rules of array initializer to every part of the code, in order (3 ways).

Ways (3), each with its exact rule:

- **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): Sequencing: the array of length k+1 is created, the initializer expressions are evaluated left to right and stored in a[0], a[1], ..., a[k], and then the reference is assigned to a.
- **[1] output\_prediction** (rule type OP, evaluation / result rule): Result: int[] a = {1, 2, 3}; gives a.length == 3, a[0] == 1, a[2] == 3. String[] suit = {"Clubs", "Diamonds", "Hearts", "Spades"}; gives suit.length == 4.
- **[2] one\_step\_execution** (rule type OS, state-transition rule): State transition: one execution creates one array holding the listed values and sets the variable to its reference.

### L3: Relational / relations x function (concrete operational begins)

L3 for array initializer: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

- **Edge:** `array_initializer` &rarr; `array_initializer@L3` (has_level)
- **Exact edge logic:** array initializer -&gt; L3 (Relational): the answer relates the parts (2 ways).

Ways (2), each with its exact rule:

- **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): An initializer implies array creation: it is shorthand for new T[k+1] followed by k+1 element assignments, so new is not written.
- **[1] purpose\_of\_the\_whole** (rule type P, plan / role rule): Plan/role: build small fixed tables of constants known when the program is written (suits, ranks, month names), usually used as fixed-value lookup tables.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for array initializer: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

- **Edge:** `array_initializer` &rarr; `array_initializer@L4` (has_level)
- **Exact edge logic:** array initializer -&gt; L4 (Extended abstract): the answer reasons beyond the given code (5 ways).

Ways (5), each with its exact rule:

- **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `ArrayInitializerContentsInBrackets`: Conservation: adding or removing a value changes the length. Code that uses a.length (e.g. rank.length) adapts, while code with a hard-coded size breaks. Reordering values changes which index holds which value.
- **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Applicability: use an initializer when all values are known at compile time and the array is small. When the values must be computed at run time, create the array with new and fill it in a loop.
- **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: Initializer values are enclosed in braces. Kind: compile-time. Trigger class: brackets are used, as in int[] a = [1, 2, 3]; (illegal start of expression)
- **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: The bare {...} form is allowed only in a declaration. Kind: compile-time. Trigger class: a = {1, 2, 3}; used as a later assignment (array constants can only be used in initializers)
- **[4] diagnose\_an\_error** (rule type D, error rule): rule broken: Each value must be assignable to the element type. Kind: compile-time. Trigger class: int[] a = {1, 2.5}; (incompatible types: possible lossy conversion from double to int)

## Same topic

`array_initializer` belongs to the topic **Setting array values at compile time and at run time** (`topic1.4.c`). The topic also contains: `array_reversal`, `array_traversal`, `enhanced_for`, `running_extreme`.

## Rules of the concept (16)

- **Book** (SW-1e, p. 91 (pdf 101)): "When we have a small number of literal values that we want to keep in array, we can declare and initialize it by listing the values between curly braces, separated by commas."
- **Book** (OT-Arrays, ): "Here the length of the array is determined by the number of values provided between braces and separated by commas."
- **Book** (SW-1.4, ): "we can initialize it by listing the values between curly braces, separated by a comma."
- **E** (folk-meaning rule): Folk meaning: in maths, braces {1, 2, 3} denote a set (unordered, no repeats) and brackets [1, 2, 3] a list, so novices write int[] a = [1, 2, 3] or expect {1, 1, 2} to have 2 elements. Java rule: braces enclose an ordered, comma-separated list whose count (repeats included) is the length.
- **M** (wrong rule / right rule): ArrayInitializerContentsInBrackets: wrong: Initializer values go in [] instead of {}. \| right: Starting values go in braces, as in int[] a = {v0, v1};; brackets only mark the type or an index.
- **M** (wrong rule / right rule): ArrayBracketCountIsLength: wrong: The number of brackets in an array type or initializer is the array's length. \| right: Brackets give the number of dimensions; an initializer's length is the number of values between its braces.
- **T** (uneven-application rule): Points to LT: an array of length k+1 is created, then v0..vk are stored at indices 0..k in order. Inconsistent application: the trace puts the first value at index 1 for one initializer but at index 0 for another, or counts the length differently.
- **N** (identity rule): Identity: an array initializer is a brace-enclosed, comma-separated list of values that creates and fills an array in one step.
- **S** (declarative rule): Declarative: 'T[] a = {v0, ..., vk};' declares, creates (no new needed) and initializes an array of length k+1. For 2-D arrays each row is its own brace list. The bare form is legal only in a declaration; elsewhere write new T[]{...}.
- **LT** (operational sequencing rule): Sequencing: the array of length k+1 is created, the initializer expressions are evaluated left to right and stored in a[0], a[1], ..., a[k], and then the reference is assigned to a.
- **OP** (evaluation / result rule): Result: int[] a = {1, 2, 3}; gives a.length == 3, a[0] == 1, a[2] == 3. String[] suit = {"Clubs", "Diamonds", "Hearts", "Spades"}; gives suit.length == 4.
- **OS** (state-transition rule): State transition: one execution creates one array holding the listed values and sets the variable to its reference.
- **R** (composition rule (with a neighbour)): with array\_creation: An initializer implies array creation: it is shorthand for new T[k+1] followed by k+1 element assignments, so new is not written.
- **P** (plan / role rule): Plan/role: build small fixed tables of constants known when the program is written (suits, ranks, month names), usually used as fixed-value lookup tables.
- **C** (conservation rule): Conservation: adding or removing a value changes the length. Code that uses a.length (e.g. rank.length) adapts, while code with a hard-coded size breaks. Reordering values changes which index holds which value.
- **D** (error rule): rule broken: Initializer values are enclosed in braces. (compile-time)
- **D** (error rule): rule broken: The bare {...} form is allowed only in a declaration. (compile-time)
- **D** (error rule): rule broken: Each value must be assignable to the element type. (compile-time)
- **X** (applicability rule): Applicability: use an initializer when all values are known at compile time and the array is small. When the values must be computed at run time, create the array with new and fill it in a loop.

## How it is found in code and answers (reader block)

- **Aliases:** array initializer, curly braces
- **Code patterns:** `=\s*\{`, `\bnew\s+\w+\s*\[\s*\]\s*\{`
- **Operator symbols:** none
- **Java types:** none

## The whole prerequisite chain

- **Everything it builds on (4):** `array_creation`, `array_declaration`, `data_structure`, `data_type`
- **Everything that builds on it (36):** `args_length`, `array_bounds`, `array_copy`, `array_exchange`, `array_reversal`, `array_traversal`, `boolean_flag_array`, `convergence_rate`, `dangling_pages`, `enhanced_for`, `frequency_counting`, `function_plotting`, `indexing`, `input_graph`, `length_field`, `lookup_table`, `loop_guard`, `markov_chain`, `matrix_operations`, `multidimensional_array`, `normalization`, `off_by_one_error`, `power_method`, `ragged_array`, `random_move`, `row_major_order`, `run_time_error`, `running_extreme`, `sampling_without_replacement`, `shuffle`, `simulation_loop`, `space_time_tradeoff`, `standard_audio`, `transition_matrix`, `two_dimensional_array`, `two_models`

## Every edge in this view and its exact edge logic (20)

All the edges drawn in the picture, in the order: prerequisite, parallel, misconception, error, has_level, contains.

**1. `array_creation` &rarr; `array_initializer`** (prerequisite)

- **Exact edge logic:** {v0, v1, ..., vk} is a shorthand that creates an array of length k + 1 and fills it in one step.
- **Grounding:** book\_passage
- **Composition rule (R) of `array_creation` with `array_initializer`:** An initializer {v0, ..., vk} implies creation of an array of length k+1, so new is not written.
- **Composition rule (R) of `array_initializer` with `array_creation`:** An initializer implies array creation: it is shorthand for new T[k+1] followed by k+1 element assignments, so new is not written.

**2. `array_declaration` &rarr; `array_initializer`** (prerequisite)

- **Exact edge logic:** int[] a = {1, 2, 3}; declares the array variable and creates and fills the array in one statement.
- **Grounding:** book\_passage

**3. `array_initializer` &rarr; `indexing`** (prerequisite)

- **Exact edge logic:** The values listed in braces are stored at indices 0, 1, 2, ... in order, and a[i] reads the value at index i.
- **Grounding:** spec\_passage

**4. `array_initializer` &rarr; `length_field`** (prerequisite)

- **Exact edge logic:** An array made from a literal has as many elements as values listed, and a.length gives that number.
- **Grounding:** spec\_passage

**5. `array_initializer` &rarr; `lookup_table`** (prerequisite)

- **Exact edge logic:** A lookup table is usually an array of fixed values written as a literal and read by index.
- **Grounding:** book\_passage

**6. `array_initializer` &rarr; `ArrayBracketCountIsLength`** (misconception)

- **Exact edge logic (the wrong rule):** The number of brackets in an array type or initializer is the array's length.
- **Twin logic (the right rule):** Brackets give the number of dimensions; the length is set at creation.
- **Role:** context

**7. `array_initializer` &rarr; `ArrayInitializerContentsInBrackets`** (misconception)

- **Exact edge logic (the wrong rule):** Starting values go in square brackets, like int[] a = [v0, v1];.
- **Twin logic (the right rule):** Starting values go in braces, like int[] a = {v0, v1};.
- **Role:** primary

**8. `array_creation` &rarr; `ArrayBracketCountIsLength`** (misconception)

- **Exact edge logic (the wrong rule):** The number of brackets in an array type or initializer is the array's length.
- **Twin logic (the right rule):** Brackets give the number of dimensions; the length is set at creation.
- **Role:** context

**9. `array_declaration` &rarr; `ArrayBracketCountIsLength`** (misconception)

- **Exact edge logic (the wrong rule):** The number of brackets in an array type or initializer is the array's length.
- **Twin logic (the right rule):** Brackets give the number of dimensions; the length is set at creation.
- **Role:** primary

**10. `multidimensional_array` &rarr; `ArrayBracketCountIsLength`** (misconception)

- **Exact edge logic (the wrong rule):** The number of brackets in an array type or initializer is the array's length.
- **Twin logic (the right rule):** Brackets give the number of dimensions; the length is set at creation.
- **Role:** context

**11. `array_initializer` &rarr; `array_initializer@L0`** (has_level)

- **Exact edge logic:** array initializer -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (4 ways).
  - **[0] everyday\_reading** (rule type E, folk-meaning rule): Folk meaning: in maths, braces {1, 2, 3} denote a set (unordered, no repeats) and brackets [1, 2, 3] a list, so novices write int[] a = [1, 2, 3] or expect {1, 1, 2} to have 2 elements. Java rule: braces enclose an ordered, comma-separated list whose count (repeats included) is the length.
  - **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `ArrayInitializerContentsInBrackets`: wrong rule: Initializer values go in [] instead of {}. Right rule: Starting values go in braces, as in int[] a = {v0, v1};; brackets only mark the type or an index.
  - **[2] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `ArrayInitializerContentsInBrackets`: Points to LT: an array of length k+1 is created, then v0..vk are stored at indices 0..k in order. Inconsistent application: the trace puts the first value at index 1 for one initializer but at index 0 for another, or counts the length differently. (here mixing in: "initializer values go in [] instead of {}")
  - **[3] misconception** (rule type M, wrong rule / right rule) &rarr; `ArrayBracketCountIsLength`: wrong rule: The number of brackets in an array type or initializer is the array's length. Right rule: Brackets give the number of dimensions; an initializer's length is the number of values between its braces.

**12. `array_initializer` &rarr; `array_initializer@L1`** (has_level)

- **Exact edge logic:** array initializer -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).
  - **[0] names\_the\_element** (rule type N, identity rule): Identity: an array initializer is a brace-enclosed, comma-separated list of values that creates and fills an array in one step.
  - **[1] states\_the\_rule** (rule type S, declarative rule): Declarative: 'T[] a = {v0, ..., vk};' declares, creates (no new needed) and initializes an array of length k+1. For 2-D arrays each row is its own brace list. The bare form is legal only in a declaration; elsewhere write new T[]{...}.

**13. `array_initializer` &rarr; `array_initializer@L2`** (has_level)

- **Exact edge logic:** array initializer -&gt; L2 (Multistructural): the answer applies the rules of array initializer to every part of the code, in order (3 ways).
  - **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): Sequencing: the array of length k+1 is created, the initializer expressions are evaluated left to right and stored in a[0], a[1], ..., a[k], and then the reference is assigned to a.
  - **[1] output\_prediction** (rule type OP, evaluation / result rule): Result: int[] a = {1, 2, 3}; gives a.length == 3, a[0] == 1, a[2] == 3. String[] suit = {"Clubs", "Diamonds", "Hearts", "Spades"}; gives suit.length == 4.
  - **[2] one\_step\_execution** (rule type OS, state-transition rule): State transition: one execution creates one array holding the listed values and sets the variable to its reference.

**14. `array_initializer` &rarr; `array_initializer@L3`** (has_level)

- **Exact edge logic:** array initializer -&gt; L3 (Relational): the answer relates the parts (2 ways).
  - **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): An initializer implies array creation: it is shorthand for new T[k+1] followed by k+1 element assignments, so new is not written.
  - **[1] purpose\_of\_the\_whole** (rule type P, plan / role rule): Plan/role: build small fixed tables of constants known when the program is written (suits, ranks, month names), usually used as fixed-value lookup tables.

**15. `array_initializer` &rarr; `array_initializer@L4`** (has_level)

- **Exact edge logic:** array initializer -&gt; L4 (Extended abstract): the answer reasons beyond the given code (5 ways).
  - **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `ArrayInitializerContentsInBrackets`: Conservation: adding or removing a value changes the length. Code that uses a.length (e.g. rank.length) adapts, while code with a hard-coded size breaks. Reordering values changes which index holds which value.
  - **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Applicability: use an initializer when all values are known at compile time and the array is small. When the values must be computed at run time, create the array with new and fill it in a loop.
  - **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: Initializer values are enclosed in braces. Kind: compile-time. Trigger class: brackets are used, as in int[] a = [1, 2, 3]; (illegal start of expression)
  - **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: The bare {...} form is allowed only in a declaration. Kind: compile-time. Trigger class: a = {1, 2, 3}; used as a later assignment (array constants can only be used in initializers)
  - **[4] diagnose\_an\_error** (rule type D, error rule): rule broken: Each value must be assignable to the element type. Kind: compile-time. Trigger class: int[] a = {1, 2.5}; (incompatible types: possible lossy conversion from double to int)

**16. `topic1.4.c` &rarr; `array_initializer`** (contains)

- topic `topic1.4.c` contains `array_initializer`

**17. `topic1.4.c` &rarr; `array_reversal`** (contains)

- topic `topic1.4.c` contains `array_reversal`

**18. `topic1.4.c` &rarr; `array_traversal`** (contains)

- topic `topic1.4.c` contains `array_traversal`

**19. `topic1.4.c` &rarr; `enhanced_for`** (contains)

- topic `topic1.4.c` contains `enhanced_for`

**20. `topic1.4.c` &rarr; `running_extreme`** (contains)

- topic `topic1.4.c` contains `running_extreme`
