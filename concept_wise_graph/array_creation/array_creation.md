# array_creation (`array_creation`)

new int[n] -- allocates n slots

Section 1.4 Arrays, topic 1.4.a Arrays in Java (declare, create, initialize; indexing; length; default values).

![The knowledge graph around array_creation](array_creation.png)

## At a glance

- **Needs first:** `array_declaration`
- **Leads to:** `array_aliasing`, `array_default_values`, `array_initializer`, `array_reference`, `indexing`, `length_field`, `sampling_without_replacement`
- **Learned alongside:** nothing
- **Misconceptions:** `ArrayAllocationWithoutNew`, `ArrayBracketCountIsLength`, `ArrayCreationIsFree`, `ArrayLengthCannotBeZero`, `ArrayListIsArray`, `ArrayRangeInclusive`, `ArraysGrow`, `DeclarationCreatesArray`
- **Errors:** `NegativeArraySize`
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 39 edges around this concept, each explained in the graph's own words.

## What it needs first (1)

A prerequisite edge means the other concept has to be understood before `array_creation`.

### `array_declaration` comes before `array_creation`

*int[] a; -- declares an array variable*

double[] a; declares the array name and type; a = new double[N]; then creates the array.

- **Grounding:** book passage
- **How `array_creation` combines with `array_declaration`:** The declared element type must match the created one; in 'double[] a = new double[N];' the left side is the declaration and the right side is the creation.
- **How `array_declaration` combines with `array_creation`:** Composition: the declaration fixes the name and element type, and the creation must match it. 'double[] a = new double[N];' is legal, but 'double[] a = new int[N];' is a compile-time type error, because int[] does not convert to double[].

## What it leads to (7)

These concepts need `array_creation` first.

### `array_creation` comes before `array_aliasing`

*two variables can refer to the same array*

Because new creates one array and the variable stores only a reference to it, assigning that variable to another makes both names refer to the same array.

- **Grounding:** book passage
- **How `array_creation` combines with `array_aliasing`:** Only new makes a distinct array. Assignment copies the reference, so a separate copy needs new plus an element-by-element copy.
- **How `array_aliasing` combines with `array_creation`:** Only new creates a distinct array; to copy, create a new array and copy each element (or use Arrays.copyOf).

### `array_creation` comes before `array_default_values`

*new slots start at 0 / false / null*

new fills every slot with the type's default value: 0, 0.0, false or null.

- **Grounding:** book passage
- **How `array_creation` combines with `array_default_values`:** Creation is what puts the default value (0, 0.0, false, null) in every slot; each execution of new gives fresh defaults.
- **How `array_default_values` combines with `array_creation`:** Defaults come from creation, so every execution of new resets them; creating the array inside the trial loop gives each experiment a clean all-false grid.

### `array_creation` comes before `array_initializer`

*{1, 2, 3} literal initialization*

{v0, v1, ..., vk} is a shorthand that creates an array of length k + 1 and fills it in one step.

- **Grounding:** book passage
- **How `array_creation` combines with `array_initializer`:** An initializer {v0, ..., vk} implies creation of an array of length k+1, so new is not written.
- **How `array_initializer` combines with `array_creation`:** An initializer implies array creation: it is shorthand for new T[k+1] followed by k+1 element assignments, so new is not written.

### `array_creation` comes before `array_reference`

*Array name holds a memory address: the array variable stores the memory address (pointer) of the array; a[i] is found by adding i to that address*

When an array is created, the array name stores the memory address of its values; a[i] is found by adding i to that address.

- **Grounding:** book passage
- **How `array_creation` combines with `array_reference`:** new yields the reference (address) of the array, and the array variable stores that reference, not the elements.
- **How `array_reference` combines with `array_creation`:** new reserves the memory and yields the array's address, which the array variable then stores.

### `array_creation` comes before `indexing`

*a[i] -- 0-based access*

An array must be created with new before any of its elements a[i] can be accessed.

- **Grounding:** book passage
- **How `array_creation` combines with `indexing`:** Elements can be indexed only after creation, and the n given to new fixes the valid index range 0..n-1.
- **How `indexing` combines with `array_creation`:** An element can be indexed only after the array is created, and the n given to new sets the valid indices 0..n-1.

### `array_creation` comes before `length_field`

*a.length is a field, not a method*

The size n given to new becomes a.length and stays fixed for the array's lifetime.

- **Grounding:** book passage
- **How `array_creation` combines with `length_field`:** The size n given to new becomes a.length and never changes for that array object.
- **How `length_field` combines with `array_creation`:** The n given to new becomes a.length and stays fixed for that array object.

### `array_creation` comes before `sampling_without_replacement`

*choosing m distinct items at random*

Sampling without replacement first creates an array of all candidates (perm), then picks from the part not yet chosen.

- **Grounding:** book passage

## Learned alongside (0)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

No parallel edge touches this concept.

## Misconceptions (8)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### ArrayAllocationWithoutNew

- **Wrong rule:** Arrays are created without the new keyword.
- **Right rule:** An array is created with new (or with an initializer list in a declaration).
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: Arrays are created without the new keyword. Right rule: An array exists only after new T[n] (or an initializer list in a declaration, which implies creation) has run.

### ArrayBracketCountIsLength

- **Wrong rule:** The number of brackets in an array type or initializer is the array's length.
- **Right rule:** Brackets give the number of dimensions; the length is set at creation.
- **Role of this concept:** context
- **Shows at level L0 as:** misconception: wrong rule: The number of brackets in new int[][] is the array's length. Right rule: Bracket pairs give the number of dimensions; the length is the value of the dimension expression inside them.
- **Also an edge from `array_declaration`:** The number of brackets in an array type or initializer is the array's length.
- **Also an edge from `array_initializer`:** The number of brackets in an array type or initializer is the array's length.
- **Also an edge from `multidimensional_array`:** The number of brackets in an array type or initializer is the array's length.

### ArrayCreationIsFree

- **Wrong rule:** Creating a big array with new takes no time because the elements are not set yet.
- **Right rule:** Java initializes every element when the array is created, so creation takes time proportional to its length.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: Creating a big array with new takes no time because the elements are not set yet. Right rule: Java initializes every element when the array is created, so creation takes time proportional to its length.
- **Also an edge from `array_default_values`:** Creating a big array with new takes no time because the elements are not set yet.

### ArrayLengthCannotBeZero

- **Wrong rule:** An array cannot have length 0.
- **Right rule:** new int[0] is a legal array of length 0.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: An array cannot have length 0. Right rule: new int[0] is a legal array with a.length == 0 (no element can be indexed).
- **Also an edge from `length_field`:** An array cannot have length 0.

### ArrayListIsArray

- **Wrong rule:** an ArrayList is an array (borderline; beyond Chapter 1 CS1)
- **Right rule:** An array has a fixed length and uses [] and .length; an ArrayList can grow and uses get, set and size().
- **Role of this concept:** primary
- **Also an edge from `array_aliasing`:** An ArrayList is just an array, so it has a fixed length and is indexed with [].

### ArrayRangeInclusive

- **Wrong rule:** new int[n] has slots 0 to n, inclusive.
- **Right rule:** The slots are 0 to n - 1.
- **Role of this concept:** context
- **Shows at level L0 as:** misconception: wrong rule: new int[n] has slots 0 to n, inclusive. Right rule: new int[n] has exactly n slots, a[0] through a[n-1]; a[n] does not exist.
- **Also an edge from `indexing`:** new int[n] has slots 0 to n, inclusive.

### ArraysGrow

- **Wrong rule:** Storing a value at a[n] in an array of length n makes the array grow.
- **Right rule:** An array's length is fixed when it is created, so a[n] throws an exception.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: An array grows as you add elements. Right rule: An array's length is fixed when it is created, so writing to a[n] throws an exception instead of adding a slot.
- **Shows at level L0 as:** inconsistent trace: Points to LT: evaluate the size, allocate the array, fill it with defaults, return the reference, then assign it. Inconsistent application: the size n is treated as the last index on some lines, or the array is assumed to exist already at its declaration. (here mixing in: "an array grows as you add elements")

### DeclarationCreatesArray

- **Wrong rule:** int[] a; already makes an array that can be indexed.
- **Right rule:** The declaration only names the array; until new (or an initializer) creates it, using a[i] gives a 'variable might not have been initialized' compile-time error.
- **Role of this concept:** context
- **Shows at level L0 as:** misconception: wrong rule: int[] a; already makes an array that can be indexed. Right rule: Only new (or an initializer) creates the array; before that, using a[i] is the compile-time error 'variable a might not have been initialized'.
- **Also an edge from `array_declaration`:** int[] a; already makes an array that can be indexed.

## Errors (1)

An error edge states the rule that gets broken in a program, and the right rule.

### NegativeArraySize

- **Wrong rule:** new int[n] with a negative n creates an empty array.
- **Right rule:** Creating an array with a negative length throws NegativeArraySizeException at run time.
- **Role of this concept:** primary
- **Also an edge from `run_time_error`:** new int[n] with a negative n creates an empty array.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for array creation: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to array creation agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

array creation -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (9 ways).

- **everyday reading** (folk-meaning rule): Folk meaning: in maths, a[5] or a\_5 names element 5, and 'new' means 'fresh, empty, ready to fill', so 'new int[5]' is read as 'element 5' or as an empty list that grows. Java rule: new int[n] allocates exactly n elements, indexed 0 to n-1, each already set to the default value, and the length can never change.
- **misconception** (wrong rule / right rule; shows `ArraysGrow`): wrong rule: An array grows as you add elements. Right rule: An array's length is fixed when it is created, so writing to a[n] throws an exception instead of adding a slot.
- **misconception** (wrong rule / right rule; shows `ArrayAllocationWithoutNew`): wrong rule: Arrays are created without the new keyword. Right rule: An array exists only after new T[n] (or an initializer list in a declaration, which implies creation) has run.
- **misconception** (wrong rule / right rule; shows `ArrayLengthCannotBeZero`): wrong rule: An array cannot have length 0. Right rule: new int[0] is a legal array with a.length == 0 (no element can be indexed).
- **misconception** (wrong rule / right rule; shows `ArrayCreationIsFree`): wrong rule: Creating a big array with new takes no time because the elements are not set yet. Right rule: Java initializes every element when the array is created, so creation takes time proportional to its length.
- **inconsistent trace** (uneven-application rule; shows `ArraysGrow`): Points to LT: evaluate the size, allocate the array, fill it with defaults, return the reference, then assign it. Inconsistent application: the size n is treated as the last index on some lines, or the array is assumed to exist already at its declaration. (here mixing in: "an array grows as you add elements")
- **misconception** (wrong rule / right rule; shows `ArrayRangeInclusive`): wrong rule: new int[n] has slots 0 to n, inclusive. Right rule: new int[n] has exactly n slots, a[0] through a[n-1]; a[n] does not exist.
- **misconception** (wrong rule / right rule; shows `DeclarationCreatesArray`): wrong rule: int[] a; already makes an array that can be indexed. Right rule: Only new (or an initializer) creates the array; before that, using a[i] is the compile-time error 'variable a might not have been initialized'.
- **misconception** (wrong rule / right rule; shows `ArrayBracketCountIsLength`): wrong rule: The number of brackets in new int[][] is the array's length. Right rule: Bracket pairs give the number of dimensions; the length is the value of the dimension expression inside them.

### L1: Unistructural / atom x text surface

L1 for array creation: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

array creation -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

- **names the element** (identity rule): Identity: an array creation expression; new T[n] makes a new array object with n elements of type T and yields a reference to it.
- **states the rule** (declarative rule): Declarative: 'new T[expr]', where expr is any int-valued expression evaluated at run time; the resulting length is fixed for the array's lifetime.

### L2: Multistructural / block x execution / preoperational

L2 for array creation: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

array creation -&gt; L2 (Multistructural): the answer applies the rules of array creation to every part of the code, in order (3 ways).

- **line by line trace** (operational sequencing rule): Sequencing: (1) the dimension expression is evaluated; (2) if it is negative, NegativeArraySizeException is thrown; (3) space for n elements is reserved and every element is set to its default; (4) the expression yields the reference, which an enclosing assignment then stores.
- **output prediction** (evaluation / result rule): Result: a value of type T[], namely a reference to a new array of length n whose elements all hold the default (0, 0.0, false or null). It produces no output; printing it shows an address, not the elements.
- **one step execution** (state-transition rule): State transition: one execution creates one new array object (n new element variables at their defaults) and returns its reference. No existing variable changes until that reference is assigned.

### L3: Relational / relations x function (concrete operational begins)

L3 for array creation: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

array creation -&gt; L3 (Relational): the answer relates the parts (8 ways).

- **relation to neighbour** (composition rule (with a neighbour)): The declared element type must match the created one; in 'double[] a = new double[N];' the left side is the declaration and the right side is the creation.
- **relation to neighbour** (composition rule (with a neighbour)): Elements can be indexed only after creation, and the n given to new fixes the valid index range 0..n-1.
- **relation to neighbour** (composition rule (with a neighbour)): Creation is what puts the default value (0, 0.0, false, null) in every slot; each execution of new gives fresh defaults.
- **relation to neighbour** (composition rule (with a neighbour)): The size n given to new becomes a.length and never changes for that array object.
- **relation to neighbour** (composition rule (with a neighbour)): An initializer {v0, ..., vk} implies creation of an array of length k+1, so new is not written.
- **relation to neighbour** (composition rule (with a neighbour)): Only new makes a distinct array. Assignment copies the reference, so a separate copy needs new plus an element-by-element copy.
- **relation to neighbour** (composition rule (with a neighbour)): new yields the reference (address) of the array, and the array variable stores that reference, not the elements.
- **purpose of the whole** (plan / role rule): Plan/role: reserve storage for a number of values that may be known only at run time (e.g. N from the command line), before any value is stored.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for array creation: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

array creation -&gt; L4 (Extended abstract): the answer reasons beyond the given code (6 ways).

- **predict a change** (conservation rule; shows `ArraysGrow`): Conservation: changing n changes a.length and the valid index range but not the element type. Moving 'new' inside a loop gives a fresh array of defaults on every pass (SelfAvoidingWalk relies on this). Re-creating an array never changes arrays that other variables already refer to.
- **diagnose an error** (error rule): rule broken: The dimension expression of new must be &gt;= 0. Kind: run-time exception. Trigger class: the size evaluates to a negative int, e.g. a negative command-line value, or int overflow such as new int[N\*N\*N\*N] with N = 1000 (NegativeArraySizeException)
- **transfer to a new program** (applicability rule): Applicability: use new T[n] when the number of values is known (at least at run time) before they are stored and stays fixed. Use an initializer when the values are compile-time constants, and a resizing structure when the count is unknown in advance.
- **diagnose an error** (error rule): rule broken: An array must be allocated with new before its elements are accessed. Kind: compile-time. Trigger class: 'int[] a;' followed by a[i] = ... with no creation (variable a might not have been initialized)
- **diagnose an error** (error rule): rule broken: The dimension expression must have an integral type (int after promotion). Kind: compile-time. Trigger class: a double or long size such as new int[2.5] or new int[n] with long n (incompatible types: possible lossy conversion)
- **diagnose an error** (error rule): rule broken: The requested array must fit in the memory available to Java. Kind: run-time exception. Trigger class: a very large n such as new boolean[N+1] for huge N in PrimeSieve (OutOfMemoryError)

## Same topic

`array_creation` belongs to the topic **Arrays in Java (declare, create, initialize; indexing; length; default values)** (`topic1.4.a`). The topic also contains: `args_length`, `array_declaration`, `array_default_values`, `data_structure`, `indexing`, `length_field`, `off_by_one_error`.

## Rules of the concept (28)

- **folk-meaning rule:** Folk meaning: in maths, a[5] or a\_5 names element 5, and 'new' means 'fresh, empty, ready to fill', so 'new int[5]' is read as 'element 5' or as an empty list that grows. Java rule: new int[n] allocates exactly n elements, indexed 0 to n-1, each already set to the default value, and the length can never change.
- **wrong rule / right rule:** ArrayAllocationWithoutNew: wrong: Arrays are created without the new keyword. \| right: An array exists only after new T[n] (or an initializer list in a declaration, which implies creation) has run.
- **wrong rule / right rule:** ArrayRangeInclusive: wrong: new int[n] has slots 0 to n, inclusive. \| right: new int[n] has exactly n slots, a[0] through a[n-1]; a[n] does not exist.
- **wrong rule / right rule:** ArraysGrow: wrong: An array grows as you add elements. \| right: An array's length is fixed when it is created, so writing to a[n] throws an exception instead of adding a slot.
- **wrong rule / right rule:** DeclarationCreatesArray: wrong: int[] a; already makes an array that can be indexed. \| right: Only new (or an initializer) creates the array; before that, using a[i] is the compile-time error 'variable a might not have been initialized'.
- **wrong rule / right rule:** ArrayBracketCountIsLength: wrong: The number of brackets in new int[][] is the array's length. \| right: Bracket pairs give the number of dimensions; the length is the value of the dimension expression inside them.
- **wrong rule / right rule:** ArrayLengthCannotBeZero: wrong: An array cannot have length 0. \| right: new int[0] is a legal array with a.length == 0 (no element can be indexed).
- **wrong rule / right rule:** ArrayCreationIsFree: wrong: Creating a big array with new takes no time because the elements are not set yet. \| right: Java initializes every element when the array is created, so creation takes time proportional to its length.
- **uneven-application rule:** Points to LT: evaluate the size, allocate the array, fill it with defaults, return the reference, then assign it. Inconsistent application: the size n is treated as the last index on some lines, or the array is assumed to exist already at its declaration.
- **identity rule:** Identity: an array creation expression; new T[n] makes a new array object with n elements of type T and yields a reference to it.
- **declarative rule:** Declarative: 'new T[expr]', where expr is any int-valued expression evaluated at run time; the resulting length is fixed for the array's lifetime.
- **operational sequencing rule:** Sequencing: (1) the dimension expression is evaluated; (2) if it is negative, NegativeArraySizeException is thrown; (3) space for n elements is reserved and every element is set to its default; (4) the expression yields the reference, which an enclosing assignment then stores.
- **evaluation / result rule:** Result: a value of type T[], namely a reference to a new array of length n whose elements all hold the default (0, 0.0, false or null). It produces no output; printing it shows an address, not the elements.
- **state-transition rule:** State transition: one execution creates one new array object (n new element variables at their defaults) and returns its reference. No existing variable changes until that reference is assigned.
- **composition rule (with a neighbour):** with array\_declaration: The declared element type must match the created one; in 'double[] a = new double[N];' the left side is the declaration and the right side is the creation.
- **composition rule (with a neighbour):** with indexing: Elements can be indexed only after creation, and the n given to new fixes the valid index range 0..n-1.
- **composition rule (with a neighbour):** with array\_default\_values: Creation is what puts the default value (0, 0.0, false, null) in every slot; each execution of new gives fresh defaults.
- **composition rule (with a neighbour):** with length\_field: The size n given to new becomes a.length and never changes for that array object.
- **composition rule (with a neighbour):** with array\_initializer: An initializer {v0, ..., vk} implies creation of an array of length k+1, so new is not written.
- **composition rule (with a neighbour):** with array\_aliasing: Only new makes a distinct array. Assignment copies the reference, so a separate copy needs new plus an element-by-element copy.
- **composition rule (with a neighbour):** with array\_reference: new yields the reference (address) of the array, and the array variable stores that reference, not the elements.
- **plan / role rule:** Plan/role: reserve storage for a number of values that may be known only at run time (e.g. N from the command line), before any value is stored.
- **conservation rule:** Conservation: changing n changes a.length and the valid index range but not the element type. Moving 'new' inside a loop gives a fresh array of defaults on every pass (SelfAvoidingWalk relies on this). Re-creating an array never changes arrays that other variables already refer to.
- **error rule:** rule broken: The dimension expression of new must be &gt;= 0. (run-time exception)
- **error rule:** rule broken: An array must be allocated with new before its elements are accessed. (compile-time)
- **error rule:** rule broken: The dimension expression must have an integral type (int after promotion). (compile-time)
- **error rule:** rule broken: The requested array must fit in the memory available to Java. (run-time exception)
- **applicability rule:** Applicability: use new T[n] when the number of values is known (at least at run time) before they are stored and stays fixed. Use an initializer when the values are compile-time constants, and a resizing structure when the count is unknown in advance.

## The whole prerequisite chain

- **Everything it builds on (3):** `array_declaration`, `data_structure`, `data_type`
- **Everything that builds on it (42):** `args_length`, `array_aliasing`, `array_bounds`, `array_copy`, `array_default_values`, `array_exchange`, `array_initializer`, `array_reference`, `array_reversal`, `array_traversal`, `boolean_flag_array`, `convergence_rate`, `dangling_pages`, `enhanced_for`, `frequency_counting`, `function_plotting`, `indexing`, `input_graph`, `length_field`, `lookup_table`, `loop_guard`, `markov_chain`, `matrix_operations`, `multidimensional_array`, `normalization`, `off_by_one_error`, `power_method`, `primitive_vs_reference`, `printing_array_reference`, `ragged_array`, `random_move`, `row_major_order`, `run_time_error`, `running_extreme`, `sampling_without_replacement`, `shuffle`, `simulation_loop`, `space_time_tradeoff`, `standard_audio`, `transition_matrix`, `two_dimensional_array`, `two_models`
