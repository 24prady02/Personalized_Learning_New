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

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 26 edges around this concept. The edge logic, the wrong and right rules and the exact rules of the ways are copied word for word from the graph.

## To work on (0)

Nothing is missing for this concept.

## What it needs first (1)

A prerequisite edge means the other concept has to be understood before `array_declaration`.

### `data_structure` comes before `array_declaration`

*Data structure: a method for organizing data; the one-dimensional array is the first example*

- **Edge:** `pre:data_structure->array_declaration`
- **Exact edge logic:** An array is a data structure: one name for a sequence of values of the same type, organised by index.
- **Grounding:** book\_passage

## What it leads to (3)

These concepts need `array_declaration` first.

### `array_declaration` comes before `array_creation`

*new int[n] -- allocates n slots*

- **Edge:** `pre:array_declaration->array_creation`
- **Exact edge logic:** double[] a; declares the array name and type; a = new double[N]; then creates the array.
- **Grounding:** book\_passage
- **Composition rule (R) of `array_declaration` with `array_creation`:** Composition: the declaration fixes the name and element type, and the creation must match it. 'double[] a = new double[N];' is legal, but 'double[] a = new int[N];' is a compile-time type error, because int[] does not convert to double[].
- **Composition rule (R) of `array_creation` with `array_declaration`:** The declared element type must match the created one; in 'double[] a = new double[N];' the left side is the declaration and the right side is the creation.

### `array_declaration` comes before `array_initializer`

*{1, 2, 3} literal initialization*

- **Edge:** `pre:array_declaration->array_initializer`
- **Exact edge logic:** int[] a = {1, 2, 3}; declares the array variable and creates and fills the array in one statement.
- **Grounding:** book\_passage

### `array_declaration` comes before `array_reference`

*Array name holds a memory address: the array variable stores the memory address (pointer) of the array; a[i] is found by adding i to that address*

- **Edge:** `pre:array_declaration->array_reference`
- **Exact edge logic:** Declaring an array variable creates only a variable that holds a reference to an array; the array itself is a separate object.
- **Grounding:** spec\_passage

## Learned alongside (0)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

No parallel edge touches this concept.

## Misconceptions (4)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### ArrayBracketCountIsLength

- **Edge:** `array_declaration` &rarr; `ArrayBracketCountIsLength` (misconception)
- **Exact edge logic (the wrong rule):** The number of brackets in an array type or initializer is the array's length.
- **Twin logic (the right rule):** Brackets give the number of dimensions; the length is set at creation.
- **Wrong belief (on the node):** The number of brackets in an array type or initializer is the array's length.
- **Correct rule (on the node):** Brackets give the number of dimensions; the length is set at creation.
- **Provenance:** published
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [3] misconception, exact rule:** wrong rule: The number of brackets in an array type is the array's length. Right rule: Each bracket pair adds one dimension (int[] is 1-D, int[][] is 2-D); the length is not part of the type and is fixed only when the array is created.
- **Edge `array_creation` &rarr; `ArrayBracketCountIsLength`, exact edge logic:** The number of brackets in an array type or initializer is the array's length. **Twin logic:** Brackets give the number of dimensions; the length is set at creation. (role: context)
- **Edge `array_initializer` &rarr; `ArrayBracketCountIsLength`, exact edge logic:** The number of brackets in an array type or initializer is the array's length. **Twin logic:** Brackets give the number of dimensions; the length is set at creation. (role: context)
- **Edge `multidimensional_array` &rarr; `ArrayBracketCountIsLength`, exact edge logic:** The number of brackets in an array type or initializer is the array's length. **Twin logic:** Brackets give the number of dimensions; the length is set at creation. (role: context)

### ArrayElementsUntyped

- **Edge:** `array_declaration` &rarr; `ArrayElementsUntyped` (misconception)
- **Exact edge logic (the wrong rule):** An array can hold elements of any type.
- **Twin logic (the right rule):** All elements of an array have the declared element type.
- **Wrong belief (on the node):** An array can hold elements of any type.
- **Correct rule (on the node):** All elements of an array have the declared element type.
- **Provenance:** published
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [2] misconception, exact rule:** wrong rule: An array can hold elements of any type. Right rule: Every element of an array has the declared element type: an int[] holds only int values, a String[] only String references.

### DeclarationCreatesArray

- **Edge:** `array_declaration` &rarr; `DeclarationCreatesArray` (misconception)
- **Exact edge logic (the wrong rule):** int[] a; already makes an array that can be indexed.
- **Twin logic (the right rule):** The declaration only names the array; until new (or an initializer) creates it, using a[i] gives a 'variable might not have been initialized' compile-time error.
- **Wrong belief (on the node):** int[] a; already makes an array that can be indexed.
- **Correct rule (on the node):** The declaration only names the array; until new (or an initializer) creates it, using a[i] gives a 'variable might not have been initialized' compile-time error.
- **Provenance:** textbook
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [1] misconception, exact rule:** wrong rule: int[] a; already makes an array that can be indexed. Right rule: The declaration only names the array variable; until new (or an initializer) creates the array, a[i] gives the compile-time error 'variable a might not have been initialized'.
- **L0 way [4] inconsistent\_trace, exact rule:** Points to LT: declare, then create, then initialize, in that order. Inconsistent application: the trace treats a as already created on some lines (reading a[i] straight after 'int[] a;') while requiring new on others. (here mixing in: "int[] a; already makes an array that can be indexed")
- **Edge `array_creation` &rarr; `DeclarationCreatesArray`, exact edge logic:** int[] a; already makes an array that can be indexed. **Twin logic:** The declaration only names the array; until new (or an initializer) creates it, using a[i] gives a 'variable might not have been initialized' compile-time error. (role: context)

### ElementNameIsWholeArray

- **Edge:** `array_declaration` &rarr; `ElementNameIsWholeArray` (misconception)
- **Exact edge logic (the wrong rule):** X[i] names the whole array, not one element.
- **Twin logic (the right rule):** The array is a; a[i] is the single element at index i.
- **Wrong belief (on the node):** X[i] names the whole array, not one element.
- **Correct rule (on the node):** The array is a; a[i] is the single element at index i.
- **Provenance:** published
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [5] misconception, exact rule:** wrong rule: X[i] names the whole array, not one element. Right rule: The name a (written a[] in the book) denotes the whole array; a[i] denotes the single element at index i.
- **Edge `indexing` &rarr; `ElementNameIsWholeArray`, exact edge logic:** X[i] names the whole array, not one element. **Twin logic:** The array is a; a[i] is the single element at index i. (role: primary)

## Errors (0)

An error edge states the rule that gets broken in a program, and the right rule.

The graph has no error edge from this concept.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for array declaration: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to array declaration agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

- **Edge:** `array_declaration` &rarr; `array_declaration@L0` (has_level)
- **Exact edge logic:** array declaration -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (6 ways).

Ways (6), each with its exact rule:

- **[0] everyday\_reading** (rule type E, folk-meaning rule): Folk meaning: in maths and English, writing 'int[] a' reads as 'a is an array of ints', as if naming a list brings it into existence. Java rule: the declaration only creates a variable that can hold a reference to an int array; no array object or element space exists until new or an initializer creates one.
- **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `DeclarationCreatesArray`: wrong rule: int[] a; already makes an array that can be indexed. Right rule: The declaration only names the array variable; until new (or an initializer) creates the array, a[i] gives the compile-time error 'variable a might not have been initialized'.
- **[2] misconception** (rule type M, wrong rule / right rule) &rarr; `ArrayElementsUntyped`: wrong rule: An array can hold elements of any type. Right rule: Every element of an array has the declared element type: an int[] holds only int values, a String[] only String references.
- **[3] misconception** (rule type M, wrong rule / right rule) &rarr; `ArrayBracketCountIsLength`: wrong rule: The number of brackets in an array type is the array's length. Right rule: Each bracket pair adds one dimension (int[] is 1-D, int[][] is 2-D); the length is not part of the type and is fixed only when the array is created.
- **[4] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `DeclarationCreatesArray`: Points to LT: declare, then create, then initialize, in that order. Inconsistent application: the trace treats a as already created on some lines (reading a[i] straight after 'int[] a;') while requiring new on others. (here mixing in: "int[] a; already makes an array that can be indexed")
- **[5] misconception** (rule type M, wrong rule / right rule) &rarr; `ElementNameIsWholeArray`: wrong rule: X[i] names the whole array, not one element. Right rule: The name a (written a[] in the book) denotes the whole array; a[i] denotes the single element at index i.

### L1: Unistructural / atom x text surface

L1 for array declaration: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

- **Edge:** `array_declaration` &rarr; `array_declaration@L1` (has_level)
- **Exact edge logic:** array declaration -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

Ways (2), each with its exact rule:

- **[0] names\_the\_element** (rule type N, identity rule): Identity: a local variable declaration whose type is T[]; it introduces a name for a reference to an array whose elements have type T.
- **[1] states\_the\_rule** (rule type S, declarative rule): Declarative: 'T[] name;' declares an array variable of element type T (the C-style 'T name[]' is also legal); the length is not part of the type, so 'int[5] a;' is illegal.

### L2: Multistructural / block x execution / preoperational

L2 for array declaration: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

- **Edge:** `array_declaration` &rarr; `array_declaration@L2` (has_level)
- **Exact edge logic:** array declaration -&gt; L2 (Multistructural): the answer applies the rules of array declaration to every part of the code, in order (3 ways).

Ways (3), each with its exact rule:

- **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): Sequencing: 'double[] a;' only adds the variable a. In 'double[] a = new double[N];' the right side runs first (N is evaluated, the array is allocated and filled with defaults), and then the reference is stored in a.
- **[1] output\_prediction** (rule type OP, evaluation / result rule): Result: a declaration produces no value and no output. A declared but unassigned local array variable cannot be read at all, so any use of a or a[i] before an assignment is rejected at compile time.
- **[2] one\_step\_execution** (rule type OS, state-transition rule): State transition: after 'int[] a;' the state gains a variable a with no value (not definitely assigned). No array object and no element variables exist yet.

### L3: Relational / relations x function (concrete operational begins)

L3 for array declaration: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

- **Edge:** `array_declaration` &rarr; `array_declaration@L3` (has_level)
- **Exact edge logic:** array declaration -&gt; L3 (Relational): the answer relates the parts (2 ways).

Ways (2), each with its exact rule:

- **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Composition: the declaration fixes the name and element type, and the creation must match it. 'double[] a = new double[N];' is legal, but 'double[] a = new int[N];' is a compile-time type error, because int[] does not convert to double[].
- **[1] purpose\_of\_the\_whole** (rule type P, plan / role rule): Plan/role: give one name to a whole sequence of same-type values, so a program reaches any of N values as a[i] instead of declaring N separate variables a0, a1, ...

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for array declaration: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

- **Edge:** `array_declaration` &rarr; `array_declaration@L4` (has_level)
- **Exact edge logic:** array declaration -&gt; L4 (Extended abstract): the answer reasons beyond the given code (4 ways).

Ways (4), each with its exact rule:

- **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `DeclarationCreatesArray`: Conservation: rewriting 'int[] a' as 'int a[]' keeps the meaning. Changing the element type changes which values may be stored and the default values. Deleting the creation step breaks the program at compile time.
- **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Applicability: declare an array when a program must hold many values of one type and reach them by position. Do not use one for a single value, for values of different types, or for a collection that must grow as values arrive (a resizing structure such as ArrayList fits that case).
- **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: An array variable must refer to a created array before it is used (definite assignment). Kind: compile-time. Trigger class: a[i] is read or written after 'int[] a;' with no 'a = new int[n]' or initializer on every path to that use
- **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: All elements have the declared element type. Kind: compile-time. Trigger class: a value or array of a different type is stored, e.g. 'int[] a = new double[5];' or 'a[0] = 2.5;' for an int[] a (incompatible types / possible lossy conversion)

## Same topic

`array_declaration` belongs to the topic **Arrays in Java (declare, create, initialize; indexing; length; default values)** (`topic1.4.a`). The topic also contains: `args_length`, `array_creation`, `array_default_values`, `data_structure`, `indexing`, `length_field`, `off_by_one_error`.

## Rules of the concept (17)

- **Book** (SW-1e, p. 87 (pdf 97)): "Making an array in a Java program involves three distinct steps"
- **Book** (SW-1e, p. 87 (pdf 97)): "To declare the array, you need to specify a name and the type of data it will contain."
- **Book** (OT-Arrays, ): "As with variables of other types, the declaration does not actually create an array; it simply tells the compiler that this variable will hold an array of the specified type."
- **Book** (SW-1.4, ): "if we have n values, we think of them as being numbered from 0 to n-1."
- **E** (folk-meaning rule): Folk meaning: in maths and English, writing 'int[] a' reads as 'a is an array of ints', as if naming a list brings it into existence. Java rule: the declaration only creates a variable that can hold a reference to an int array; no array object or element space exists until new or an initializer creates one.
- **M** (wrong rule / right rule): ArrayElementsUntyped: wrong: An array can hold elements of any type. \| right: Every element of an array has the declared element type: an int[] holds only int values, a String[] only String references.
- **M** (wrong rule / right rule): DeclarationCreatesArray: wrong: int[] a; already makes an array that can be indexed. \| right: The declaration only names the array variable; until new (or an initializer) creates the array, a[i] gives the compile-time error 'variable a might not have been initialized'.
- **M** (wrong rule / right rule): ArrayBracketCountIsLength: wrong: The number of brackets in an array type is the array's length. \| right: Each bracket pair adds one dimension (int[] is 1-D, int[][] is 2-D); the length is not part of the type and is fixed only when the array is created.
- **M** (wrong rule / right rule): ElementNameIsWholeArray: wrong: X[i] names the whole array, not one element. \| right: The name a (written a[] in the book) denotes the whole array; a[i] denotes the single element at index i.
- **T** (uneven-application rule): Points to LT: declare, then create, then initialize, in that order. Inconsistent application: the trace treats a as already created on some lines (reading a[i] straight after 'int[] a;') while requiring new on others.
- **N** (identity rule): Identity: a local variable declaration whose type is T[]; it introduces a name for a reference to an array whose elements have type T.
- **S** (declarative rule): Declarative: 'T[] name;' declares an array variable of element type T (the C-style 'T name[]' is also legal); the length is not part of the type, so 'int[5] a;' is illegal.
- **LT** (operational sequencing rule): Sequencing: 'double[] a;' only adds the variable a. In 'double[] a = new double[N];' the right side runs first (N is evaluated, the array is allocated and filled with defaults), and then the reference is stored in a.
- **OP** (evaluation / result rule): Result: a declaration produces no value and no output. A declared but unassigned local array variable cannot be read at all, so any use of a or a[i] before an assignment is rejected at compile time.
- **OS** (state-transition rule): State transition: after 'int[] a;' the state gains a variable a with no value (not definitely assigned). No array object and no element variables exist yet.
- **R** (composition rule (with a neighbour)): with array\_creation: Composition: the declaration fixes the name and element type, and the creation must match it. 'double[] a = new double[N];' is legal, but 'double[] a = new int[N];' is a compile-time type error, because int[] does not convert to double[].
- **P** (plan / role rule): Plan/role: give one name to a whole sequence of same-type values, so a program reaches any of N values as a[i] instead of declaring N separate variables a0, a1, ...
- **C** (conservation rule): Conservation: rewriting 'int[] a' as 'int a[]' keeps the meaning. Changing the element type changes which values may be stored and the default values. Deleting the creation step breaks the program at compile time.
- **D** (error rule): rule broken: An array variable must refer to a created array before it is used (definite assignment). (compile-time)
- **D** (error rule): rule broken: All elements have the declared element type. (compile-time)
- **X** (applicability rule): Applicability: declare an array when a program must hold many values of one type and reach them by position. Do not use one for a single value, for values of different types, or for a collection that must grow as values arrive (a resizing structure such as ArrayList fits that case).

## How it is found in code and answers (reader block)

- **Aliases:** array declaration
- **Code patterns:** `(?:int|double|boolean|char|long|String|float|short|byte)\s*\[\s*\]\s*\w+`, `\b(?:int|double|boolean|char|long|String|float|short|byte)\s+\w+\s*\[\s*\]`
- **Operator symbols:** none
- **Java types:** none

## The whole prerequisite chain

- **Everything it builds on (2):** `data_structure`, `data_type`
- **Everything that builds on it (43):** `args_length`, `array_aliasing`, `array_bounds`, `array_copy`, `array_creation`, `array_default_values`, `array_exchange`, `array_initializer`, `array_reference`, `array_reversal`, `array_traversal`, `boolean_flag_array`, `convergence_rate`, `dangling_pages`, `enhanced_for`, `frequency_counting`, `function_plotting`, `indexing`, `input_graph`, `length_field`, `lookup_table`, `loop_guard`, `markov_chain`, `matrix_operations`, `multidimensional_array`, `normalization`, `off_by_one_error`, `power_method`, `primitive_vs_reference`, `printing_array_reference`, `ragged_array`, `random_move`, `row_major_order`, `run_time_error`, `running_extreme`, `sampling_without_replacement`, `shuffle`, `simulation_loop`, `space_time_tradeoff`, `standard_audio`, `transition_matrix`, `two_dimensional_array`, `two_models`

## Every edge in this view and its exact edge logic (26)

All the edges drawn in the picture, in the order: prerequisite, parallel, misconception, error, has_level, contains.

**1. `array_declaration` &rarr; `array_creation`** (prerequisite)

- **Exact edge logic:** double[] a; declares the array name and type; a = new double[N]; then creates the array.
- **Grounding:** book\_passage
- **Composition rule (R) of `array_declaration` with `array_creation`:** Composition: the declaration fixes the name and element type, and the creation must match it. 'double[] a = new double[N];' is legal, but 'double[] a = new int[N];' is a compile-time type error, because int[] does not convert to double[].
- **Composition rule (R) of `array_creation` with `array_declaration`:** The declared element type must match the created one; in 'double[] a = new double[N];' the left side is the declaration and the right side is the creation.

**2. `array_declaration` &rarr; `array_initializer`** (prerequisite)

- **Exact edge logic:** int[] a = {1, 2, 3}; declares the array variable and creates and fills the array in one statement.
- **Grounding:** book\_passage

**3. `array_declaration` &rarr; `array_reference`** (prerequisite)

- **Exact edge logic:** Declaring an array variable creates only a variable that holds a reference to an array; the array itself is a separate object.
- **Grounding:** spec\_passage

**4. `data_structure` &rarr; `array_declaration`** (prerequisite)

- **Exact edge logic:** An array is a data structure: one name for a sequence of values of the same type, organised by index.
- **Grounding:** book\_passage

**5. `array_declaration` &rarr; `ArrayBracketCountIsLength`** (misconception)

- **Exact edge logic (the wrong rule):** The number of brackets in an array type or initializer is the array's length.
- **Twin logic (the right rule):** Brackets give the number of dimensions; the length is set at creation.
- **Role:** primary

**6. `array_declaration` &rarr; `ArrayElementsUntyped`** (misconception)

- **Exact edge logic (the wrong rule):** An array can hold elements of any type.
- **Twin logic (the right rule):** All elements of an array have the declared element type.
- **Role:** primary

**7. `array_declaration` &rarr; `DeclarationCreatesArray`** (misconception)

- **Exact edge logic (the wrong rule):** int[] a; already makes an array that can be indexed.
- **Twin logic (the right rule):** The declaration only names the array; until new (or an initializer) creates it, using a[i] gives a 'variable might not have been initialized' compile-time error.
- **Role:** primary

**8. `array_declaration` &rarr; `ElementNameIsWholeArray`** (misconception)

- **Exact edge logic (the wrong rule):** X[i] names the whole array, not one element.
- **Twin logic (the right rule):** The array is a; a[i] is the single element at index i.
- **Role:** context

**9. `array_creation` &rarr; `ArrayBracketCountIsLength`** (misconception)

- **Exact edge logic (the wrong rule):** The number of brackets in an array type or initializer is the array's length.
- **Twin logic (the right rule):** Brackets give the number of dimensions; the length is set at creation.
- **Role:** context

**10. `array_creation` &rarr; `DeclarationCreatesArray`** (misconception)

- **Exact edge logic (the wrong rule):** int[] a; already makes an array that can be indexed.
- **Twin logic (the right rule):** The declaration only names the array; until new (or an initializer) creates it, using a[i] gives a 'variable might not have been initialized' compile-time error.
- **Role:** context

**11. `array_initializer` &rarr; `ArrayBracketCountIsLength`** (misconception)

- **Exact edge logic (the wrong rule):** The number of brackets in an array type or initializer is the array's length.
- **Twin logic (the right rule):** Brackets give the number of dimensions; the length is set at creation.
- **Role:** context

**12. `indexing` &rarr; `ElementNameIsWholeArray`** (misconception)

- **Exact edge logic (the wrong rule):** X[i] names the whole array, not one element.
- **Twin logic (the right rule):** The array is a; a[i] is the single element at index i.
- **Role:** primary

**13. `multidimensional_array` &rarr; `ArrayBracketCountIsLength`** (misconception)

- **Exact edge logic (the wrong rule):** The number of brackets in an array type or initializer is the array's length.
- **Twin logic (the right rule):** Brackets give the number of dimensions; the length is set at creation.
- **Role:** context

**14. `array_declaration` &rarr; `array_declaration@L0`** (has_level)

- **Exact edge logic:** array declaration -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (6 ways).
  - **[0] everyday\_reading** (rule type E, folk-meaning rule): Folk meaning: in maths and English, writing 'int[] a' reads as 'a is an array of ints', as if naming a list brings it into existence. Java rule: the declaration only creates a variable that can hold a reference to an int array; no array object or element space exists until new or an initializer creates one.
  - **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `DeclarationCreatesArray`: wrong rule: int[] a; already makes an array that can be indexed. Right rule: The declaration only names the array variable; until new (or an initializer) creates the array, a[i] gives the compile-time error 'variable a might not have been initialized'.
  - **[2] misconception** (rule type M, wrong rule / right rule) &rarr; `ArrayElementsUntyped`: wrong rule: An array can hold elements of any type. Right rule: Every element of an array has the declared element type: an int[] holds only int values, a String[] only String references.
  - **[3] misconception** (rule type M, wrong rule / right rule) &rarr; `ArrayBracketCountIsLength`: wrong rule: The number of brackets in an array type is the array's length. Right rule: Each bracket pair adds one dimension (int[] is 1-D, int[][] is 2-D); the length is not part of the type and is fixed only when the array is created.
  - **[4] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `DeclarationCreatesArray`: Points to LT: declare, then create, then initialize, in that order. Inconsistent application: the trace treats a as already created on some lines (reading a[i] straight after 'int[] a;') while requiring new on others. (here mixing in: "int[] a; already makes an array that can be indexed")
  - **[5] misconception** (rule type M, wrong rule / right rule) &rarr; `ElementNameIsWholeArray`: wrong rule: X[i] names the whole array, not one element. Right rule: The name a (written a[] in the book) denotes the whole array; a[i] denotes the single element at index i.

**15. `array_declaration` &rarr; `array_declaration@L1`** (has_level)

- **Exact edge logic:** array declaration -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).
  - **[0] names\_the\_element** (rule type N, identity rule): Identity: a local variable declaration whose type is T[]; it introduces a name for a reference to an array whose elements have type T.
  - **[1] states\_the\_rule** (rule type S, declarative rule): Declarative: 'T[] name;' declares an array variable of element type T (the C-style 'T name[]' is also legal); the length is not part of the type, so 'int[5] a;' is illegal.

**16. `array_declaration` &rarr; `array_declaration@L2`** (has_level)

- **Exact edge logic:** array declaration -&gt; L2 (Multistructural): the answer applies the rules of array declaration to every part of the code, in order (3 ways).
  - **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): Sequencing: 'double[] a;' only adds the variable a. In 'double[] a = new double[N];' the right side runs first (N is evaluated, the array is allocated and filled with defaults), and then the reference is stored in a.
  - **[1] output\_prediction** (rule type OP, evaluation / result rule): Result: a declaration produces no value and no output. A declared but unassigned local array variable cannot be read at all, so any use of a or a[i] before an assignment is rejected at compile time.
  - **[2] one\_step\_execution** (rule type OS, state-transition rule): State transition: after 'int[] a;' the state gains a variable a with no value (not definitely assigned). No array object and no element variables exist yet.

**17. `array_declaration` &rarr; `array_declaration@L3`** (has_level)

- **Exact edge logic:** array declaration -&gt; L3 (Relational): the answer relates the parts (2 ways).
  - **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Composition: the declaration fixes the name and element type, and the creation must match it. 'double[] a = new double[N];' is legal, but 'double[] a = new int[N];' is a compile-time type error, because int[] does not convert to double[].
  - **[1] purpose\_of\_the\_whole** (rule type P, plan / role rule): Plan/role: give one name to a whole sequence of same-type values, so a program reaches any of N values as a[i] instead of declaring N separate variables a0, a1, ...

**18. `array_declaration` &rarr; `array_declaration@L4`** (has_level)

- **Exact edge logic:** array declaration -&gt; L4 (Extended abstract): the answer reasons beyond the given code (4 ways).
  - **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `DeclarationCreatesArray`: Conservation: rewriting 'int[] a' as 'int a[]' keeps the meaning. Changing the element type changes which values may be stored and the default values. Deleting the creation step breaks the program at compile time.
  - **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Applicability: declare an array when a program must hold many values of one type and reach them by position. Do not use one for a single value, for values of different types, or for a collection that must grow as values arrive (a resizing structure such as ArrayList fits that case).
  - **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: An array variable must refer to a created array before it is used (definite assignment). Kind: compile-time. Trigger class: a[i] is read or written after 'int[] a;' with no 'a = new int[n]' or initializer on every path to that use
  - **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: All elements have the declared element type. Kind: compile-time. Trigger class: a value or array of a different type is stored, e.g. 'int[] a = new double[5];' or 'a[0] = 2.5;' for an int[] a (incompatible types / possible lossy conversion)

**19. `topic1.4.a` &rarr; `array_declaration`** (contains)

- topic `topic1.4.a` contains `array_declaration`

**20. `topic1.4.a` &rarr; `args_length`** (contains)

- topic `topic1.4.a` contains `args_length`

**21. `topic1.4.a` &rarr; `array_creation`** (contains)

- topic `topic1.4.a` contains `array_creation`

**22. `topic1.4.a` &rarr; `array_default_values`** (contains)

- topic `topic1.4.a` contains `array_default_values`

**23. `topic1.4.a` &rarr; `data_structure`** (contains)

- topic `topic1.4.a` contains `data_structure`

**24. `topic1.4.a` &rarr; `indexing`** (contains)

- topic `topic1.4.a` contains `indexing`

**25. `topic1.4.a` &rarr; `length_field`** (contains)

- topic `topic1.4.a` contains `length_field`

**26. `topic1.4.a` &rarr; `off_by_one_error`** (contains)

- topic `topic1.4.a` contains `off_by_one_error`
