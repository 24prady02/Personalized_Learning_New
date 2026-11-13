# array_declaration (`array_declaration`)

int[] a; -- declares an array variable

Section 1.4 Arrays, topic 1.4.a Arrays in Java (declare, create, initialize; indexing; length; default values).

![The knowledge graph around array_declaration](array_declaration.png)

## At a glance

- **Needs first:** `data_structure`
- **Leads to:** `array_creation`, `array_initializer`, `array_reference`
- **Learned alongside:** nothing
- **Misconceptions:** `ArrayBracketCountIsLength`, `ArrayElementsUntyped`, `DeclarationCreatesArray`, `ElementNameIsWholeArray`
- **Errors:** none
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 26 edges around this concept, each explained in the graph's own words.

## What it needs first (1)

A prerequisite edge means the other concept has to be understood before `array_declaration`.

### `data_structure` comes before `array_declaration`

*Data structure: a method for organizing data; the one-dimensional array is the first example*

An array is a data structure: one name for a sequence of values of the same type, organised by index.

- **Grounding:** book passage

## What it leads to (3)

These concepts need `array_declaration` first.

### `array_declaration` comes before `array_creation`

*new int[n] -- allocates n slots*

double[] a; declares the array name and type; a = new double[N]; then creates the array.

- **Grounding:** book passage
- **How `array_declaration` combines with `array_creation`:** Composition: the declaration fixes the name and element type, and the creation must match it. 'double[] a = new double[N];' is legal, but 'double[] a = new int[N];' is a compile-time type error, because int[] does not convert to double[].
- **How `array_creation` combines with `array_declaration`:** The declared element type must match the created one; in 'double[] a = new double[N];' the left side is the declaration and the right side is the creation.

### `array_declaration` comes before `array_initializer`

*{1, 2, 3} literal initialization*

int[] a = {1, 2, 3}; declares the array variable and creates and fills the array in one statement.

- **Grounding:** book passage

### `array_declaration` comes before `array_reference`

*Array name holds a memory address: the array variable stores the memory address (pointer) of the array; a[i] is found by adding i to that address*

Declaring an array variable creates only a variable that holds a reference to an array; the array itself is a separate object.

- **Grounding:** spec passage

## Learned alongside (0)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

No parallel edge touches this concept.

## Misconceptions (4)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### ArrayBracketCountIsLength

- **Wrong rule:** The number of brackets in an array type or initializer is the array's length.
- **Right rule:** Brackets give the number of dimensions; the length is set at creation.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: The number of brackets in an array type is the array's length. Right rule: Each bracket pair adds one dimension (int[] is 1-D, int[][] is 2-D); the length is not part of the type and is fixed only when the array is created.
- **Also an edge from `array_creation`:** The number of brackets in an array type or initializer is the array's length.
- **Also an edge from `array_initializer`:** The number of brackets in an array type or initializer is the array's length.
- **Also an edge from `multidimensional_array`:** The number of brackets in an array type or initializer is the array's length.

### ArrayElementsUntyped

- **Wrong rule:** An array can hold elements of any type.
- **Right rule:** All elements of an array have the declared element type.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: An array can hold elements of any type. Right rule: Every element of an array has the declared element type: an int[] holds only int values, a String[] only String references.

### DeclarationCreatesArray

- **Wrong rule:** int[] a; already makes an array that can be indexed.
- **Right rule:** The declaration only names the array; until new (or an initializer) creates it, using a[i] gives a 'variable might not have been initialized' compile-time error.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: int[] a; already makes an array that can be indexed. Right rule: The declaration only names the array variable; until new (or an initializer) creates the array, a[i] gives the compile-time error 'variable a might not have been initialized'.
- **Shows at level L0 as:** inconsistent trace: Points to LT: declare, then create, then initialize, in that order. Inconsistent application: the trace treats a as already created on some lines (reading a[i] straight after 'int[] a;') while requiring new on others. (here mixing in: "int[] a; already makes an array that can be indexed")
- **Also an edge from `array_creation`:** int[] a; already makes an array that can be indexed.

### ElementNameIsWholeArray

- **Wrong rule:** X[i] names the whole array, not one element.
- **Right rule:** The array is a; a[i] is the single element at index i.
- **Role of this concept:** context
- **Shows at level L0 as:** misconception: wrong rule: X[i] names the whole array, not one element. Right rule: The name a (written a[] in the book) denotes the whole array; a[i] denotes the single element at index i.
- **Also an edge from `indexing`:** X[i] names the whole array, not one element.

## Errors (0)

An error edge states the rule that gets broken in a program, and the right rule.

The graph has no error edge from this concept.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for array declaration: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to array declaration agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

array declaration -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (6 ways).

- **everyday reading** (folk-meaning rule): Folk meaning: in maths and English, writing 'int[] a' reads as 'a is an array of ints', as if naming a list brings it into existence. Java rule: the declaration only creates a variable that can hold a reference to an int array; no array object or element space exists until new or an initializer creates one.
- **misconception** (wrong rule / right rule; shows `DeclarationCreatesArray`): wrong rule: int[] a; already makes an array that can be indexed. Right rule: The declaration only names the array variable; until new (or an initializer) creates the array, a[i] gives the compile-time error 'variable a might not have been initialized'.
- **misconception** (wrong rule / right rule; shows `ArrayElementsUntyped`): wrong rule: An array can hold elements of any type. Right rule: Every element of an array has the declared element type: an int[] holds only int values, a String[] only String references.
- **misconception** (wrong rule / right rule; shows `ArrayBracketCountIsLength`): wrong rule: The number of brackets in an array type is the array's length. Right rule: Each bracket pair adds one dimension (int[] is 1-D, int[][] is 2-D); the length is not part of the type and is fixed only when the array is created.
- **inconsistent trace** (uneven-application rule; shows `DeclarationCreatesArray`): Points to LT: declare, then create, then initialize, in that order. Inconsistent application: the trace treats a as already created on some lines (reading a[i] straight after 'int[] a;') while requiring new on others. (here mixing in: "int[] a; already makes an array that can be indexed")
- **misconception** (wrong rule / right rule; shows `ElementNameIsWholeArray`): wrong rule: X[i] names the whole array, not one element. Right rule: The name a (written a[] in the book) denotes the whole array; a[i] denotes the single element at index i.

### L1: Unistructural / atom x text surface

L1 for array declaration: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

array declaration -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

- **names the element** (identity rule): Identity: a local variable declaration whose type is T[]; it introduces a name for a reference to an array whose elements have type T.
- **states the rule** (declarative rule): Declarative: 'T[] name;' declares an array variable of element type T (the C-style 'T name[]' is also legal); the length is not part of the type, so 'int[5] a;' is illegal.

### L2: Multistructural / block x execution / preoperational

L2 for array declaration: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

array declaration -&gt; L2 (Multistructural): the answer applies the rules of array declaration to every part of the code, in order (3 ways).

- **line by line trace** (operational sequencing rule): Sequencing: 'double[] a;' only adds the variable a. In 'double[] a = new double[N];' the right side runs first (N is evaluated, the array is allocated and filled with defaults), and then the reference is stored in a.
- **output prediction** (evaluation / result rule): Result: a declaration produces no value and no output. A declared but unassigned local array variable cannot be read at all, so any use of a or a[i] before an assignment is rejected at compile time.
- **one step execution** (state-transition rule): State transition: after 'int[] a;' the state gains a variable a with no value (not definitely assigned). No array object and no element variables exist yet.

### L3: Relational / relations x function (concrete operational begins)

L3 for array declaration: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

array declaration -&gt; L3 (Relational): the answer relates the parts (2 ways).

- **relation to neighbour** (composition rule (with a neighbour)): Composition: the declaration fixes the name and element type, and the creation must match it. 'double[] a = new double[N];' is legal, but 'double[] a = new int[N];' is a compile-time type error, because int[] does not convert to double[].
- **purpose of the whole** (plan / role rule): Plan/role: give one name to a whole sequence of same-type values, so a program reaches any of N values as a[i] instead of declaring N separate variables a0, a1, ...

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for array declaration: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

array declaration -&gt; L4 (Extended abstract): the answer reasons beyond the given code (4 ways).

- **predict a change** (conservation rule; shows `DeclarationCreatesArray`): Conservation: rewriting 'int[] a' as 'int a[]' keeps the meaning. Changing the element type changes which values may be stored and the default values. Deleting the creation step breaks the program at compile time.
- **transfer to a new program** (applicability rule): Applicability: declare an array when a program must hold many values of one type and reach them by position. Do not use one for a single value, for values of different types, or for a collection that must grow as values arrive (a resizing structure such as ArrayList fits that case).
- **diagnose an error** (error rule): rule broken: An array variable must refer to a created array before it is used (definite assignment). Kind: compile-time. Trigger class: a[i] is read or written after 'int[] a;' with no 'a = new int[n]' or initializer on every path to that use
- **diagnose an error** (error rule): rule broken: All elements have the declared element type. Kind: compile-time. Trigger class: a value or array of a different type is stored, e.g. 'int[] a = new double[5];' or 'a[0] = 2.5;' for an int[] a (incompatible types / possible lossy conversion)

## Same topic

`array_declaration` belongs to the topic **Arrays in Java (declare, create, initialize; indexing; length; default values)** (`topic1.4.a`). The topic also contains: `args_length`, `array_creation`, `array_default_values`, `data_structure`, `indexing`, `length_field`, `off_by_one_error`.

## Rules of the concept (17)

- **folk-meaning rule:** Folk meaning: in maths and English, writing 'int[] a' reads as 'a is an array of ints', as if naming a list brings it into existence. Java rule: the declaration only creates a variable that can hold a reference to an int array; no array object or element space exists until new or an initializer creates one.
- **wrong rule / right rule:** ArrayElementsUntyped: wrong: An array can hold elements of any type. \| right: Every element of an array has the declared element type: an int[] holds only int values, a String[] only String references.
- **wrong rule / right rule:** DeclarationCreatesArray: wrong: int[] a; already makes an array that can be indexed. \| right: The declaration only names the array variable; until new (or an initializer) creates the array, a[i] gives the compile-time error 'variable a might not have been initialized'.
- **wrong rule / right rule:** ArrayBracketCountIsLength: wrong: The number of brackets in an array type is the array's length. \| right: Each bracket pair adds one dimension (int[] is 1-D, int[][] is 2-D); the length is not part of the type and is fixed only when the array is created.
- **wrong rule / right rule:** ElementNameIsWholeArray: wrong: X[i] names the whole array, not one element. \| right: The name a (written a[] in the book) denotes the whole array; a[i] denotes the single element at index i.
- **uneven-application rule:** Points to LT: declare, then create, then initialize, in that order. Inconsistent application: the trace treats a as already created on some lines (reading a[i] straight after 'int[] a;') while requiring new on others.
- **identity rule:** Identity: a local variable declaration whose type is T[]; it introduces a name for a reference to an array whose elements have type T.
- **declarative rule:** Declarative: 'T[] name;' declares an array variable of element type T (the C-style 'T name[]' is also legal); the length is not part of the type, so 'int[5] a;' is illegal.
- **operational sequencing rule:** Sequencing: 'double[] a;' only adds the variable a. In 'double[] a = new double[N];' the right side runs first (N is evaluated, the array is allocated and filled with defaults), and then the reference is stored in a.
- **evaluation / result rule:** Result: a declaration produces no value and no output. A declared but unassigned local array variable cannot be read at all, so any use of a or a[i] before an assignment is rejected at compile time.
- **state-transition rule:** State transition: after 'int[] a;' the state gains a variable a with no value (not definitely assigned). No array object and no element variables exist yet.
- **composition rule (with a neighbour):** with array\_creation: Composition: the declaration fixes the name and element type, and the creation must match it. 'double[] a = new double[N];' is legal, but 'double[] a = new int[N];' is a compile-time type error, because int[] does not convert to double[].
- **plan / role rule:** Plan/role: give one name to a whole sequence of same-type values, so a program reaches any of N values as a[i] instead of declaring N separate variables a0, a1, ...
- **conservation rule:** Conservation: rewriting 'int[] a' as 'int a[]' keeps the meaning. Changing the element type changes which values may be stored and the default values. Deleting the creation step breaks the program at compile time.
- **error rule:** rule broken: An array variable must refer to a created array before it is used (definite assignment). (compile-time)
- **error rule:** rule broken: All elements have the declared element type. (compile-time)
- **applicability rule:** Applicability: declare an array when a program must hold many values of one type and reach them by position. Do not use one for a single value, for values of different types, or for a collection that must grow as values arrive (a resizing structure such as ArrayList fits that case).

## The whole prerequisite chain

- **Everything it builds on (2):** `data_structure`, `data_type`
- **Everything that builds on it (43):** `args_length`, `array_aliasing`, `array_bounds`, `array_copy`, `array_creation`, `array_default_values`, `array_exchange`, `array_initializer`, `array_reference`, `array_reversal`, `array_traversal`, `boolean_flag_array`, `convergence_rate`, `dangling_pages`, `enhanced_for`, `frequency_counting`, `function_plotting`, `indexing`, `input_graph`, `length_field`, `lookup_table`, `loop_guard`, `markov_chain`, `matrix_operations`, `multidimensional_array`, `normalization`, `off_by_one_error`, `power_method`, `primitive_vs_reference`, `printing_array_reference`, `ragged_array`, `random_move`, `row_major_order`, `run_time_error`, `running_extreme`, `sampling_without_replacement`, `shuffle`, `simulation_loop`, `space_time_tradeoff`, `standard_audio`, `transition_matrix`, `two_dimensional_array`, `two_models`
