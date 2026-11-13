# Data structure (`data_structure`)

a method for organizing data; the one-dimensional array is the first example

Section 1.4 1.4 Arrays, topic 1.4.a Arrays in Java (declare, create, initialize; indexing; length; default values).

![The knowledge graph around data_structure](data_structure.png)

## At a glance

- **Needs first:** `data_type`
- **Leads to:** `array_declaration`
- **Learned alongside:** nothing
- **Misconceptions:** none
- **Errors:** none
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 15 edges around this concept, each explained in the graph's own words.

## What it needs first (1)

A prerequisite edge means the other concept has to be understood before `data_structure`.

### `data_type` comes before `data_structure`

*a set of values and the operations defined on them*

A data structure organizes many values of a data type; the array holds a sequence of values of one type.

- **Grounding:** book passage
- **How `data_structure` combines with `data_type`:** A data structure organizes many values of a data type; the array holds a sequence of values of one type, and its operations (create, index, length) work on that collection.
- **How `data_type` combines with `data_structure`:** A data structure such as an array holds many values of one data type. The element type limits what can be stored in a[i] and which operations apply to it.

## What it leads to (1)

These concepts need `data_structure` first.

### `data_structure` comes before `array_declaration`

*int[] a; -- declares an array variable*

An array is a data structure: one name for a sequence of values of the same type, organised by index.

- **Grounding:** book passage

## Learned alongside (0)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

No parallel edge touches this concept.

## Misconceptions (0)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

The graph has no misconception edge from this concept.

## Errors (0)

An error edge states the rule that gets broken in a program, and the right rule.

The graph has no error edge from this concept.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for Data structure: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to Data structure agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

Data structure -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (1 way).

- **everyday reading** (folk-meaning rule): Folk meaning: one variable 'remembers' everything that was put into it, so storing many values needs no special structure. Rule: a variable holds one value at a time; keeping many values for later use needs a data structure such as an array.

### L1: Unistructural / atom x text surface

L1 for Data structure: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

Data structure -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

- **names the element** (identity rule): Identity: a data structure is a method for organizing data; the one-dimensional array is the book's first example, and the two-dimensional array the second.
- **states the rule** (declarative rule): Declarative: an array is a data structure that stores a sequence of values of the same type and gives direct access to each by its index.

### L2: Multistructural / block x execution / preoperational

L2 for Data structure: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

Data structure -&gt; L2 (Multistructural): the answer applies the rules of Data structure to every part of the code, in order (3 ways).

- **line by line trace** (operational sequencing rule): Sequencing: a structure is first built (for an array: declare, create, initialize) and then accessed one element per operation.
- **output prediction** (evaluation / result rule): Result: what an array structure provides is fast access to any stored value: element i is found by adding i to the array's address.
- **one step execution** (state-transition rule): State transition: one array operation changes at most one element (an assignment) or creates a new array; reads change nothing.

### L3: Relational / relations x function (concrete operational begins)

L3 for Data structure: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

Data structure -&gt; L3 (Relational): the answer relates the parts (2 ways).

- **relation to neighbour** (composition rule (with a neighbour)): A data structure organizes many values of a data type; the array holds a sequence of values of one type, and its operations (create, index, length) work on that collection.
- **purpose of the whole** (plan / role rule): Plan/role: organize large amounts of data so it can be stored and then processed by indexing (vectors, matrices, tables, experimental results).

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for Data structure: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

Data structure -&gt; L4 (Extended abstract): the answer reasons beyond the given code (3 ways).

- **predict a change** (conservation rule): Conservation: choosing a different organization keeps the data but changes which operations are cheap. Using arrays enlarges the program state, so tracing becomes harder and invariants matter more.
- **transfer to a new program** (applicability rule): Applicability: use an array when the number of values is known when it is created and access is by integer position. Other structures (Chapter 4) fit growing collections or non-integer keys.
- **diagnose an error** (error rule): rule broken: Values needed again later must be stored in a structure, not a single variable. Kind: silent logic error. Trigger class: a task that needs a second pass over the data (e.g. count how many equal the maximum) is solved with one variable that keeps only the latest value

## Same topic

`data_structure` belongs to the topic **Arrays in Java (declare, create, initialize; indexing; length; default values)** (`topic1.4.a`). The topic also contains: `args_length`, `array_creation`, `array_declaration`, `array_default_values`, `indexing`, `length_field`, `off_by_one_error`.

## Rules of the concept (12)

- **folk-meaning rule:** Folk meaning: one variable 'remembers' everything that was put into it, so storing many values needs no special structure. Rule: a variable holds one value at a time; keeping many values for later use needs a data structure such as an array.
- **uneven-application rule:** Points to LT: a data structure is used through its operations (for an array: create, index, traverse). Inconsistent application: the array is treated as one value on some steps and as a collection of separate variables on others.
- **identity rule:** Identity: a data structure is a method for organizing data; the one-dimensional array is the book's first example, and the two-dimensional array the second.
- **declarative rule:** Declarative: an array is a data structure that stores a sequence of values of the same type and gives direct access to each by its index.
- **operational sequencing rule:** Sequencing: a structure is first built (for an array: declare, create, initialize) and then accessed one element per operation.
- **evaluation / result rule:** Result: what an array structure provides is fast access to any stored value: element i is found by adding i to the array's address.
- **state-transition rule:** State transition: one array operation changes at most one element (an assignment) or creates a new array; reads change nothing.
- **composition rule (with a neighbour):** with data\_type: A data structure organizes many values of a data type; the array holds a sequence of values of one type, and its operations (create, index, length) work on that collection.
- **plan / role rule:** Plan/role: organize large amounts of data so it can be stored and then processed by indexing (vectors, matrices, tables, experimental results).
- **conservation rule:** Conservation: choosing a different organization keeps the data but changes which operations are cheap. Using arrays enlarges the program state, so tracing becomes harder and invariants matter more.
- **error rule:** rule broken: Values needed again later must be stored in a structure, not a single variable. (silent logic error)
- **applicability rule:** Applicability: use an array when the number of values is known when it is created and access is by integer position. Other structures (Chapter 4) fit growing collections or non-integer keys.

## The whole prerequisite chain

- **Everything it builds on (1):** `data_type`
- **Everything that builds on it (44):** `args_length`, `array_aliasing`, `array_bounds`, `array_copy`, `array_creation`, `array_declaration`, `array_default_values`, `array_exchange`, `array_initializer`, `array_reference`, `array_reversal`, `array_traversal`, `boolean_flag_array`, `convergence_rate`, `dangling_pages`, `enhanced_for`, `frequency_counting`, `function_plotting`, `indexing`, `input_graph`, `length_field`, `lookup_table`, `loop_guard`, `markov_chain`, `matrix_operations`, `multidimensional_array`, `normalization`, `off_by_one_error`, `power_method`, `primitive_vs_reference`, `printing_array_reference`, `ragged_array`, `random_move`, `row_major_order`, `run_time_error`, `running_extreme`, `sampling_without_replacement`, `shuffle`, `simulation_loop`, `space_time_tradeoff`, `standard_audio`, `transition_matrix`, `two_dimensional_array`, `two_models`
