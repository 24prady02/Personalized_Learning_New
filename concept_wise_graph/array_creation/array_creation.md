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

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 39 edges around this concept. The edge logic, the wrong and right rules and the exact rules of the ways are copied word for word from the graph.

## To work on (1)

- misconceptions with no L0 way linked to them: ArrayListIsArray

## What it needs first (1)

A prerequisite edge means the other concept has to be understood before `array_creation`.

### `array_declaration` comes before `array_creation`

*int[] a; -- declares an array variable*

- **Edge:** `pre:array_declaration->array_creation`
- **Exact edge logic:** double[] a; declares the array name and type; a = new double[N]; then creates the array.
- **Grounding:** book\_passage
- **Composition rule (R) of `array_creation` with `array_declaration`:** The declared element type must match the created one; in 'double[] a = new double[N];' the left side is the declaration and the right side is the creation.
- **Composition rule (R) of `array_declaration` with `array_creation`:** Composition: the declaration fixes the name and element type, and the creation must match it. 'double[] a = new double[N];' is legal, but 'double[] a = new int[N];' is a compile-time type error, because int[] does not convert to double[].

## What it leads to (7)

These concepts need `array_creation` first.

### `array_creation` comes before `array_aliasing`

*two variables can refer to the same array*

- **Edge:** `pre:array_creation->array_aliasing`
- **Exact edge logic:** Because new creates one array and the variable stores only a reference to it, assigning that variable to another makes both names refer to the same array.
- **Grounding:** book\_passage
- **Composition rule (R) of `array_creation` with `array_aliasing`:** Only new makes a distinct array. Assignment copies the reference, so a separate copy needs new plus an element-by-element copy.
- **Composition rule (R) of `array_aliasing` with `array_creation`:** Only new creates a distinct array; to copy, create a new array and copy each element (or use Arrays.copyOf).

### `array_creation` comes before `array_default_values`

*new slots start at 0 / false / null*

- **Edge:** `pre:array_creation->array_default_values`
- **Exact edge logic:** new fills every slot with the type's default value: 0, 0.0, false or null.
- **Grounding:** book\_passage
- **Composition rule (R) of `array_creation` with `array_default_values`:** Creation is what puts the default value (0, 0.0, false, null) in every slot; each execution of new gives fresh defaults.
- **Composition rule (R) of `array_default_values` with `array_creation`:** Defaults come from creation, so every execution of new resets them; creating the array inside the trial loop gives each experiment a clean all-false grid.

### `array_creation` comes before `array_initializer`

*{1, 2, 3} literal initialization*

- **Edge:** `pre:array_creation->array_initializer`
- **Exact edge logic:** {v0, v1, ..., vk} is a shorthand that creates an array of length k + 1 and fills it in one step.
- **Grounding:** book\_passage
- **Composition rule (R) of `array_creation` with `array_initializer`:** An initializer {v0, ..., vk} implies creation of an array of length k+1, so new is not written.
- **Composition rule (R) of `array_initializer` with `array_creation`:** An initializer implies array creation: it is shorthand for new T[k+1] followed by k+1 element assignments, so new is not written.

### `array_creation` comes before `array_reference`

*Array name holds a memory address: the array variable stores the memory address (pointer) of the array; a[i] is found by adding i to that address*

- **Edge:** `pre:array_creation->array_reference`
- **Exact edge logic:** When an array is created, the array name stores the memory address of its values; a[i] is found by adding i to that address.
- **Grounding:** book\_passage
- **Composition rule (R) of `array_creation` with `array_reference`:** new yields the reference (address) of the array, and the array variable stores that reference, not the elements.
- **Composition rule (R) of `array_reference` with `array_creation`:** new reserves the memory and yields the array's address, which the array variable then stores.

### `array_creation` comes before `indexing`

*a[i] -- 0-based access*

- **Edge:** `pre:array_creation->indexing`
- **Exact edge logic:** An array must be created with new before any of its elements a[i] can be accessed.
- **Grounding:** book\_passage
- **Composition rule (R) of `array_creation` with `indexing`:** Elements can be indexed only after creation, and the n given to new fixes the valid index range 0..n-1.
- **Composition rule (R) of `indexing` with `array_creation`:** An element can be indexed only after the array is created, and the n given to new sets the valid indices 0..n-1.

### `array_creation` comes before `length_field`

*a.length is a field, not a method*

- **Edge:** `pre:array_creation->length_field`
- **Exact edge logic:** The size n given to new becomes a.length and stays fixed for the array's lifetime.
- **Grounding:** book\_passage
- **Composition rule (R) of `array_creation` with `length_field`:** The size n given to new becomes a.length and never changes for that array object.
- **Composition rule (R) of `length_field` with `array_creation`:** The n given to new becomes a.length and stays fixed for that array object.

### `array_creation` comes before `sampling_without_replacement`

*choosing m distinct items at random*

- **Edge:** `pre:array_creation->sampling_without_replacement`
- **Exact edge logic:** Sampling without replacement first creates an array of all candidates (perm), then picks from the part not yet chosen.
- **Grounding:** book\_passage

## Learned alongside (0)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

No parallel edge touches this concept.

## Misconceptions (8)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### ArrayAllocationWithoutNew

- **Edge:** `array_creation` &rarr; `ArrayAllocationWithoutNew` (misconception)
- **Exact edge logic (the wrong rule):** Arrays are created without the new keyword.
- **Twin logic (the right rule):** An array is created with new (or with an initializer list in a declaration).
- **Wrong belief (on the node):** Arrays are created without the new keyword.
- **Correct rule (on the node):** An array is created with new (or with an initializer list in a declaration).
- **Provenance:** published
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [2] misconception, exact rule:** wrong rule: Arrays are created without the new keyword. Right rule: An array exists only after new T[n] (or an initializer list in a declaration, which implies creation) has run.

### ArrayBracketCountIsLength

- **Edge:** `array_creation` &rarr; `ArrayBracketCountIsLength` (misconception)
- **Exact edge logic (the wrong rule):** The number of brackets in an array type or initializer is the array's length.
- **Twin logic (the right rule):** Brackets give the number of dimensions; the length is set at creation.
- **Wrong belief (on the node):** The number of brackets in an array type or initializer is the array's length.
- **Correct rule (on the node):** Brackets give the number of dimensions; the length is set at creation.
- **Provenance:** published
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [8] misconception, exact rule:** wrong rule: The number of brackets in new int[][] is the array's length. Right rule: Bracket pairs give the number of dimensions; the length is the value of the dimension expression inside them.
- **Edge `array_declaration` &rarr; `ArrayBracketCountIsLength`, exact edge logic:** The number of brackets in an array type or initializer is the array's length. **Twin logic:** Brackets give the number of dimensions; the length is set at creation. (role: primary)
- **Edge `array_initializer` &rarr; `ArrayBracketCountIsLength`, exact edge logic:** The number of brackets in an array type or initializer is the array's length. **Twin logic:** Brackets give the number of dimensions; the length is set at creation. (role: context)
- **Edge `multidimensional_array` &rarr; `ArrayBracketCountIsLength`, exact edge logic:** The number of brackets in an array type or initializer is the array's length. **Twin logic:** Brackets give the number of dimensions; the length is set at creation. (role: context)

### ArrayCreationIsFree

- **Edge:** `array_creation` &rarr; `ArrayCreationIsFree` (misconception)
- **Exact edge logic (the wrong rule):** Creating a big array with new takes no time because the elements are not set yet.
- **Twin logic (the right rule):** Java initializes every element when the array is created, so creation takes time proportional to its length.
- **Wrong belief (on the node):** Creating a big array with new takes no time because the elements are not set yet.
- **Correct rule (on the node):** Java initializes every element when the array is created, so creation takes time proportional to its length.
- **Provenance:** textbook
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [4] misconception, exact rule:** wrong rule: Creating a big array with new takes no time because the elements are not set yet. Right rule: Java initializes every element when the array is created, so creation takes time proportional to its length.
- **Edge `array_default_values` &rarr; `ArrayCreationIsFree`, exact edge logic:** Creating a big array with new takes no time because the elements are not set yet. **Twin logic:** Java initializes every element when the array is created, so creation takes time proportional to its length. (role: context)

### ArrayLengthCannotBeZero

- **Edge:** `array_creation` &rarr; `ArrayLengthCannotBeZero` (misconception)
- **Exact edge logic (the wrong rule):** An array cannot have length 0.
- **Twin logic (the right rule):** new int[0] is a legal array of length 0.
- **Wrong belief (on the node):** An array cannot have length 0.
- **Correct rule (on the node):** new int[0] is a legal array of length 0.
- **Provenance:** published
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [3] misconception, exact rule:** wrong rule: An array cannot have length 0. Right rule: new int[0] is a legal array with a.length == 0 (no element can be indexed).
- **Edge `length_field` &rarr; `ArrayLengthCannotBeZero`, exact edge logic:** An array cannot have length 0. **Twin logic:** new int[0] is a legal array of length 0. (role: context)

### ArrayListIsArray

- **Edge:** `array_creation` &rarr; `ArrayListIsArray` (misconception)
- **Exact edge logic (the wrong rule):** an ArrayList is an array (borderline; beyond Chapter 1 CS1)
- **Twin logic (the right rule):** An array has a fixed length and uses [] and .length; an ArrayList can grow and uses get, set and size().
- **Wrong belief (on the node):** an ArrayList is an array (borderline; beyond Chapter 1 CS1)
- **Correct rule (on the node):** An array has a fixed length and uses [] and .length; an ArrayList can grow and uses get, set and size().
- **Provenance:** published
- **Role of this concept:** primary
- **L0 way linked to it:** no
- **Edge `array_aliasing` &rarr; `ArrayListIsArray`, exact edge logic:** An ArrayList is just an array, so it has a fixed length and is indexed with []. **Twin logic:** An array has a fixed length and uses [] and .length; an ArrayList can grow and uses get, set and size(). (role: context)

### ArrayRangeInclusive

- **Edge:** `array_creation` &rarr; `ArrayRangeInclusive` (misconception)
- **Exact edge logic (the wrong rule):** new int[n] has slots 0 to n, inclusive.
- **Twin logic (the right rule):** The slots are 0 to n - 1.
- **Wrong belief (on the node):** new int[n] has slots 0 to n, inclusive.
- **Correct rule (on the node):** The slots are 0 to n - 1.
- **Provenance:** published
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [6] misconception, exact rule:** wrong rule: new int[n] has slots 0 to n, inclusive. Right rule: new int[n] has exactly n slots, a[0] through a[n-1]; a[n] does not exist.
- **Edge `indexing` &rarr; `ArrayRangeInclusive`, exact edge logic:** new int[n] has slots 0 to n, inclusive. **Twin logic:** The slots are 0 to n - 1. (role: primary)

### ArraysGrow

- **Edge:** `array_creation` &rarr; `ArraysGrow` (misconception)
- **Exact edge logic (the wrong rule):** Storing a value at a[n] in an array of length n makes the array grow.
- **Twin logic (the right rule):** An array's length is fixed when it is created, so a[n] throws an exception.
- **Wrong belief (on the node):** an array grows as you add elements
- **Correct rule (on the node):** An array's length is fixed when it is created, so a[n] throws an exception.
- **Provenance:** published
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [1] misconception, exact rule:** wrong rule: An array grows as you add elements. Right rule: An array's length is fixed when it is created, so writing to a[n] throws an exception instead of adding a slot.
- **L0 way [5] inconsistent\_trace, exact rule:** Points to LT: evaluate the size, allocate the array, fill it with defaults, return the reference, then assign it. Inconsistent application: the size n is treated as the last index on some lines, or the array is assumed to exist already at its declaration. (here mixing in: "an array grows as you add elements")

### DeclarationCreatesArray

- **Edge:** `array_creation` &rarr; `DeclarationCreatesArray` (misconception)
- **Exact edge logic (the wrong rule):** int[] a; already makes an array that can be indexed.
- **Twin logic (the right rule):** The declaration only names the array; until new (or an initializer) creates it, using a[i] gives a 'variable might not have been initialized' compile-time error.
- **Wrong belief (on the node):** int[] a; already makes an array that can be indexed.
- **Correct rule (on the node):** The declaration only names the array; until new (or an initializer) creates it, using a[i] gives a 'variable might not have been initialized' compile-time error.
- **Provenance:** textbook
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [7] misconception, exact rule:** wrong rule: int[] a; already makes an array that can be indexed. Right rule: Only new (or an initializer) creates the array; before that, using a[i] is the compile-time error 'variable a might not have been initialized'.
- **Edge `array_declaration` &rarr; `DeclarationCreatesArray`, exact edge logic:** int[] a; already makes an array that can be indexed. **Twin logic:** The declaration only names the array; until new (or an initializer) creates it, using a[i] gives a 'variable might not have been initialized' compile-time error. (role: primary)

## Errors (1)

An error edge states the rule that gets broken in a program, and the right rule.

### NegativeArraySize

- **Edge:** `array_creation` &rarr; `NegativeArraySize` (error)
- **Exact edge logic (the wrong rule):** new int[n] with a negative n creates an empty array.
- **Twin logic (the right rule):** Creating an array with a negative length throws NegativeArraySizeException at run time.
- **Wrong belief (on the node):** new int[n] with a negative n creates an empty array.
- **Correct rule (on the node):** Creating an array with a negative length throws NegativeArraySizeException at run time.
- **Provenance:** textbook
- **Role of this concept:** primary
- **Edge `run_time_error` &rarr; `NegativeArraySize`, exact edge logic:** new int[n] with a negative n creates an empty array. **Twin logic:** Creating an array with a negative length throws NegativeArraySizeException at run time. (role: context)

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for array creation: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to array creation agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

- **Edge:** `array_creation` &rarr; `array_creation@L0` (has_level)
- **Exact edge logic:** array creation -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (9 ways).

Ways (9), each with its exact rule:

- **[0] everyday\_reading** (rule type E, folk-meaning rule): Folk meaning: in maths, a[5] or a\_5 names element 5, and 'new' means 'fresh, empty, ready to fill', so 'new int[5]' is read as 'element 5' or as an empty list that grows. Java rule: new int[n] allocates exactly n elements, indexed 0 to n-1, each already set to the default value, and the length can never change.
- **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `ArraysGrow`: wrong rule: An array grows as you add elements. Right rule: An array's length is fixed when it is created, so writing to a[n] throws an exception instead of adding a slot.
- **[2] misconception** (rule type M, wrong rule / right rule) &rarr; `ArrayAllocationWithoutNew`: wrong rule: Arrays are created without the new keyword. Right rule: An array exists only after new T[n] (or an initializer list in a declaration, which implies creation) has run.
- **[3] misconception** (rule type M, wrong rule / right rule) &rarr; `ArrayLengthCannotBeZero`: wrong rule: An array cannot have length 0. Right rule: new int[0] is a legal array with a.length == 0 (no element can be indexed).
- **[4] misconception** (rule type M, wrong rule / right rule) &rarr; `ArrayCreationIsFree`: wrong rule: Creating a big array with new takes no time because the elements are not set yet. Right rule: Java initializes every element when the array is created, so creation takes time proportional to its length.
- **[5] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `ArraysGrow`: Points to LT: evaluate the size, allocate the array, fill it with defaults, return the reference, then assign it. Inconsistent application: the size n is treated as the last index on some lines, or the array is assumed to exist already at its declaration. (here mixing in: "an array grows as you add elements")
- **[6] misconception** (rule type M, wrong rule / right rule) &rarr; `ArrayRangeInclusive`: wrong rule: new int[n] has slots 0 to n, inclusive. Right rule: new int[n] has exactly n slots, a[0] through a[n-1]; a[n] does not exist.
- **[7] misconception** (rule type M, wrong rule / right rule) &rarr; `DeclarationCreatesArray`: wrong rule: int[] a; already makes an array that can be indexed. Right rule: Only new (or an initializer) creates the array; before that, using a[i] is the compile-time error 'variable a might not have been initialized'.
- **[8] misconception** (rule type M, wrong rule / right rule) &rarr; `ArrayBracketCountIsLength`: wrong rule: The number of brackets in new int[][] is the array's length. Right rule: Bracket pairs give the number of dimensions; the length is the value of the dimension expression inside them.

### L1: Unistructural / atom x text surface

L1 for array creation: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

- **Edge:** `array_creation` &rarr; `array_creation@L1` (has_level)
- **Exact edge logic:** array creation -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

Ways (2), each with its exact rule:

- **[0] names\_the\_element** (rule type N, identity rule): Identity: an array creation expression; new T[n] makes a new array object with n elements of type T and yields a reference to it.
- **[1] states\_the\_rule** (rule type S, declarative rule): Declarative: 'new T[expr]', where expr is any int-valued expression evaluated at run time; the resulting length is fixed for the array's lifetime.

### L2: Multistructural / block x execution / preoperational

L2 for array creation: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

- **Edge:** `array_creation` &rarr; `array_creation@L2` (has_level)
- **Exact edge logic:** array creation -&gt; L2 (Multistructural): the answer applies the rules of array creation to every part of the code, in order (3 ways).

Ways (3), each with its exact rule:

- **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): Sequencing: (1) the dimension expression is evaluated; (2) if it is negative, NegativeArraySizeException is thrown; (3) space for n elements is reserved and every element is set to its default; (4) the expression yields the reference, which an enclosing assignment then stores.
- **[1] output\_prediction** (rule type OP, evaluation / result rule): Result: a value of type T[], namely a reference to a new array of length n whose elements all hold the default (0, 0.0, false or null). It produces no output; printing it shows an address, not the elements.
- **[2] one\_step\_execution** (rule type OS, state-transition rule): State transition: one execution creates one new array object (n new element variables at their defaults) and returns its reference. No existing variable changes until that reference is assigned.

### L3: Relational / relations x function (concrete operational begins)

L3 for array creation: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

- **Edge:** `array_creation` &rarr; `array_creation@L3` (has_level)
- **Exact edge logic:** array creation -&gt; L3 (Relational): the answer relates the parts (8 ways).

Ways (8), each with its exact rule:

- **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): The declared element type must match the created one; in 'double[] a = new double[N];' the left side is the declaration and the right side is the creation.
- **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Elements can be indexed only after creation, and the n given to new fixes the valid index range 0..n-1.
- **[2] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Creation is what puts the default value (0, 0.0, false, null) in every slot; each execution of new gives fresh defaults.
- **[3] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): The size n given to new becomes a.length and never changes for that array object.
- **[4] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): An initializer {v0, ..., vk} implies creation of an array of length k+1, so new is not written.
- **[5] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Only new makes a distinct array. Assignment copies the reference, so a separate copy needs new plus an element-by-element copy.
- **[6] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): new yields the reference (address) of the array, and the array variable stores that reference, not the elements.
- **[7] purpose\_of\_the\_whole** (rule type P, plan / role rule): Plan/role: reserve storage for a number of values that may be known only at run time (e.g. N from the command line), before any value is stored.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for array creation: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

- **Edge:** `array_creation` &rarr; `array_creation@L4` (has_level)
- **Exact edge logic:** array creation -&gt; L4 (Extended abstract): the answer reasons beyond the given code (6 ways).

Ways (6), each with its exact rule:

- **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `ArraysGrow`: Conservation: changing n changes a.length and the valid index range but not the element type. Moving 'new' inside a loop gives a fresh array of defaults on every pass (SelfAvoidingWalk relies on this). Re-creating an array never changes arrays that other variables already refer to.
- **[1] diagnose\_an\_error** (rule type D, error rule): rule broken: The dimension expression of new must be &gt;= 0. Kind: run-time exception. Trigger class: the size evaluates to a negative int, e.g. a negative command-line value, or int overflow such as new int[N\*N\*N\*N] with N = 1000 (NegativeArraySizeException)
- **[2] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Applicability: use new T[n] when the number of values is known (at least at run time) before they are stored and stays fixed. Use an initializer when the values are compile-time constants, and a resizing structure when the count is unknown in advance.
- **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: An array must be allocated with new before its elements are accessed. Kind: compile-time. Trigger class: 'int[] a;' followed by a[i] = ... with no creation (variable a might not have been initialized)
- **[4] diagnose\_an\_error** (rule type D, error rule): rule broken: The dimension expression must have an integral type (int after promotion). Kind: compile-time. Trigger class: a double or long size such as new int[2.5] or new int[n] with long n (incompatible types: possible lossy conversion)
- **[5] diagnose\_an\_error** (rule type D, error rule): rule broken: The requested array must fit in the memory available to Java. Kind: run-time exception. Trigger class: a very large n such as new boolean[N+1] for huge N in PrimeSieve (OutOfMemoryError)

## Same topic

`array_creation` belongs to the topic **Arrays in Java (declare, create, initialize; indexing; length; default values)** (`topic1.4.a`). The topic also contains: `args_length`, `array_declaration`, `array_default_values`, `data_structure`, `indexing`, `length_field`, `off_by_one_error`.

## Rules of the concept (28)

- **Book** (SW-1e, p. 87 (pdf 97)): "To create it, you need to specify its size (the number of values)."
- **Book** (SW-1e, p. 89 (pdf 99)): "The reason that we need to explicitly create arrays at runtime is that the Java compiler cannot know how much space to reserve for the array at compile time"
- **Book** (OT-Arrays, ): "An array is a container object that holds a fixed number of values of a single type. The length of an array is established when the array is created. After creation, its length is fixed."
- **Book** (SW-1.4, ): "if we have n values, we think of them as being numbered from 0 to n-1."
- **E** (folk-meaning rule): Folk meaning: in maths, a[5] or a\_5 names element 5, and 'new' means 'fresh, empty, ready to fill', so 'new int[5]' is read as 'element 5' or as an empty list that grows. Java rule: new int[n] allocates exactly n elements, indexed 0 to n-1, each already set to the default value, and the length can never change.
- **M** (wrong rule / right rule): ArrayAllocationWithoutNew: wrong: Arrays are created without the new keyword. \| right: An array exists only after new T[n] (or an initializer list in a declaration, which implies creation) has run.
- **M** (wrong rule / right rule): ArrayRangeInclusive: wrong: new int[n] has slots 0 to n, inclusive. \| right: new int[n] has exactly n slots, a[0] through a[n-1]; a[n] does not exist.
- **M** (wrong rule / right rule): ArraysGrow: wrong: An array grows as you add elements. \| right: An array's length is fixed when it is created, so writing to a[n] throws an exception instead of adding a slot.
- **M** (wrong rule / right rule): DeclarationCreatesArray: wrong: int[] a; already makes an array that can be indexed. \| right: Only new (or an initializer) creates the array; before that, using a[i] is the compile-time error 'variable a might not have been initialized'.
- **M** (wrong rule / right rule): ArrayBracketCountIsLength: wrong: The number of brackets in new int[][] is the array's length. \| right: Bracket pairs give the number of dimensions; the length is the value of the dimension expression inside them.
- **M** (wrong rule / right rule): ArrayLengthCannotBeZero: wrong: An array cannot have length 0. \| right: new int[0] is a legal array with a.length == 0 (no element can be indexed).
- **M** (wrong rule / right rule): ArrayCreationIsFree: wrong: Creating a big array with new takes no time because the elements are not set yet. \| right: Java initializes every element when the array is created, so creation takes time proportional to its length.
- **T** (uneven-application rule): Points to LT: evaluate the size, allocate the array, fill it with defaults, return the reference, then assign it. Inconsistent application: the size n is treated as the last index on some lines, or the array is assumed to exist already at its declaration.
- **N** (identity rule): Identity: an array creation expression; new T[n] makes a new array object with n elements of type T and yields a reference to it.
- **S** (declarative rule): Declarative: 'new T[expr]', where expr is any int-valued expression evaluated at run time; the resulting length is fixed for the array's lifetime.
- **LT** (operational sequencing rule): Sequencing: (1) the dimension expression is evaluated; (2) if it is negative, NegativeArraySizeException is thrown; (3) space for n elements is reserved and every element is set to its default; (4) the expression yields the reference, which an enclosing assignment then stores.
- **OP** (evaluation / result rule): Result: a value of type T[], namely a reference to a new array of length n whose elements all hold the default (0, 0.0, false or null). It produces no output; printing it shows an address, not the elements.
- **OS** (state-transition rule): State transition: one execution creates one new array object (n new element variables at their defaults) and returns its reference. No existing variable changes until that reference is assigned.
- **R** (composition rule (with a neighbour)): with array\_declaration: The declared element type must match the created one; in 'double[] a = new double[N];' the left side is the declaration and the right side is the creation.
- **R** (composition rule (with a neighbour)): with indexing: Elements can be indexed only after creation, and the n given to new fixes the valid index range 0..n-1.
- **R** (composition rule (with a neighbour)): with array\_default\_values: Creation is what puts the default value (0, 0.0, false, null) in every slot; each execution of new gives fresh defaults.
- **R** (composition rule (with a neighbour)): with length\_field: The size n given to new becomes a.length and never changes for that array object.
- **R** (composition rule (with a neighbour)): with array\_initializer: An initializer {v0, ..., vk} implies creation of an array of length k+1, so new is not written.
- **R** (composition rule (with a neighbour)): with array\_aliasing: Only new makes a distinct array. Assignment copies the reference, so a separate copy needs new plus an element-by-element copy.
- **R** (composition rule (with a neighbour)): with array\_reference: new yields the reference (address) of the array, and the array variable stores that reference, not the elements.
- **P** (plan / role rule): Plan/role: reserve storage for a number of values that may be known only at run time (e.g. N from the command line), before any value is stored.
- **C** (conservation rule): Conservation: changing n changes a.length and the valid index range but not the element type. Moving 'new' inside a loop gives a fresh array of defaults on every pass (SelfAvoidingWalk relies on this). Re-creating an array never changes arrays that other variables already refer to.
- **D** (error rule): rule broken: The dimension expression of new must be &gt;= 0. (run-time exception)
- **D** (error rule): rule broken: An array must be allocated with new before its elements are accessed. (compile-time)
- **D** (error rule): rule broken: The dimension expression must have an integral type (int after promotion). (compile-time)
- **D** (error rule): rule broken: The requested array must fit in the memory available to Java. (run-time exception)
- **X** (applicability rule): Applicability: use new T[n] when the number of values is known (at least at run time) before they are stored and stays fixed. Use an initializer when the values are compile-time constants, and a resizing structure when the count is unknown in advance.

## How it is found in code and answers (reader block)

- **Aliases:** new array, creates an array, array creation
- **Code patterns:** `\bnew\s+\w+\s*\[`
- **Operator symbols:** none
- **Java types:** none

## The whole prerequisite chain

- **Everything it builds on (3):** `array_declaration`, `data_structure`, `data_type`
- **Everything that builds on it (42):** `args_length`, `array_aliasing`, `array_bounds`, `array_copy`, `array_default_values`, `array_exchange`, `array_initializer`, `array_reference`, `array_reversal`, `array_traversal`, `boolean_flag_array`, `convergence_rate`, `dangling_pages`, `enhanced_for`, `frequency_counting`, `function_plotting`, `indexing`, `input_graph`, `length_field`, `lookup_table`, `loop_guard`, `markov_chain`, `matrix_operations`, `multidimensional_array`, `normalization`, `off_by_one_error`, `power_method`, `primitive_vs_reference`, `printing_array_reference`, `ragged_array`, `random_move`, `row_major_order`, `run_time_error`, `running_extreme`, `sampling_without_replacement`, `shuffle`, `simulation_loop`, `space_time_tradeoff`, `standard_audio`, `transition_matrix`, `two_dimensional_array`, `two_models`

## Every edge in this view and its exact edge logic (39)

All the edges drawn in the picture, in the order: prerequisite, parallel, misconception, error, has_level, contains.

**1. `array_creation` &rarr; `array_aliasing`** (prerequisite)

- **Exact edge logic:** Because new creates one array and the variable stores only a reference to it, assigning that variable to another makes both names refer to the same array.
- **Grounding:** book\_passage
- **Composition rule (R) of `array_creation` with `array_aliasing`:** Only new makes a distinct array. Assignment copies the reference, so a separate copy needs new plus an element-by-element copy.
- **Composition rule (R) of `array_aliasing` with `array_creation`:** Only new creates a distinct array; to copy, create a new array and copy each element (or use Arrays.copyOf).

**2. `array_creation` &rarr; `array_default_values`** (prerequisite)

- **Exact edge logic:** new fills every slot with the type's default value: 0, 0.0, false or null.
- **Grounding:** book\_passage
- **Composition rule (R) of `array_creation` with `array_default_values`:** Creation is what puts the default value (0, 0.0, false, null) in every slot; each execution of new gives fresh defaults.
- **Composition rule (R) of `array_default_values` with `array_creation`:** Defaults come from creation, so every execution of new resets them; creating the array inside the trial loop gives each experiment a clean all-false grid.

**3. `array_creation` &rarr; `array_initializer`** (prerequisite)

- **Exact edge logic:** {v0, v1, ..., vk} is a shorthand that creates an array of length k + 1 and fills it in one step.
- **Grounding:** book\_passage
- **Composition rule (R) of `array_creation` with `array_initializer`:** An initializer {v0, ..., vk} implies creation of an array of length k+1, so new is not written.
- **Composition rule (R) of `array_initializer` with `array_creation`:** An initializer implies array creation: it is shorthand for new T[k+1] followed by k+1 element assignments, so new is not written.

**4. `array_creation` &rarr; `array_reference`** (prerequisite)

- **Exact edge logic:** When an array is created, the array name stores the memory address of its values; a[i] is found by adding i to that address.
- **Grounding:** book\_passage
- **Composition rule (R) of `array_creation` with `array_reference`:** new yields the reference (address) of the array, and the array variable stores that reference, not the elements.
- **Composition rule (R) of `array_reference` with `array_creation`:** new reserves the memory and yields the array's address, which the array variable then stores.

**5. `array_creation` &rarr; `indexing`** (prerequisite)

- **Exact edge logic:** An array must be created with new before any of its elements a[i] can be accessed.
- **Grounding:** book\_passage
- **Composition rule (R) of `array_creation` with `indexing`:** Elements can be indexed only after creation, and the n given to new fixes the valid index range 0..n-1.
- **Composition rule (R) of `indexing` with `array_creation`:** An element can be indexed only after the array is created, and the n given to new sets the valid indices 0..n-1.

**6. `array_creation` &rarr; `length_field`** (prerequisite)

- **Exact edge logic:** The size n given to new becomes a.length and stays fixed for the array's lifetime.
- **Grounding:** book\_passage
- **Composition rule (R) of `array_creation` with `length_field`:** The size n given to new becomes a.length and never changes for that array object.
- **Composition rule (R) of `length_field` with `array_creation`:** The n given to new becomes a.length and stays fixed for that array object.

**7. `array_creation` &rarr; `sampling_without_replacement`** (prerequisite)

- **Exact edge logic:** Sampling without replacement first creates an array of all candidates (perm), then picks from the part not yet chosen.
- **Grounding:** book\_passage

**8. `array_declaration` &rarr; `array_creation`** (prerequisite)

- **Exact edge logic:** double[] a; declares the array name and type; a = new double[N]; then creates the array.
- **Grounding:** book\_passage
- **Composition rule (R) of `array_declaration` with `array_creation`:** Composition: the declaration fixes the name and element type, and the creation must match it. 'double[] a = new double[N];' is legal, but 'double[] a = new int[N];' is a compile-time type error, because int[] does not convert to double[].
- **Composition rule (R) of `array_creation` with `array_declaration`:** The declared element type must match the created one; in 'double[] a = new double[N];' the left side is the declaration and the right side is the creation.

**9. `array_creation` &rarr; `ArrayAllocationWithoutNew`** (misconception)

- **Exact edge logic (the wrong rule):** Arrays are created without the new keyword.
- **Twin logic (the right rule):** An array is created with new (or with an initializer list in a declaration).
- **Role:** primary

**10. `array_creation` &rarr; `ArrayBracketCountIsLength`** (misconception)

- **Exact edge logic (the wrong rule):** The number of brackets in an array type or initializer is the array's length.
- **Twin logic (the right rule):** Brackets give the number of dimensions; the length is set at creation.
- **Role:** context

**11. `array_creation` &rarr; `ArrayCreationIsFree`** (misconception)

- **Exact edge logic (the wrong rule):** Creating a big array with new takes no time because the elements are not set yet.
- **Twin logic (the right rule):** Java initializes every element when the array is created, so creation takes time proportional to its length.
- **Role:** primary

**12. `array_creation` &rarr; `ArrayLengthCannotBeZero`** (misconception)

- **Exact edge logic (the wrong rule):** An array cannot have length 0.
- **Twin logic (the right rule):** new int[0] is a legal array of length 0.
- **Role:** primary

**13. `array_creation` &rarr; `ArrayListIsArray`** (misconception)

- **Exact edge logic (the wrong rule):** an ArrayList is an array (borderline; beyond Chapter 1 CS1)
- **Twin logic (the right rule):** An array has a fixed length and uses [] and .length; an ArrayList can grow and uses get, set and size().
- **Role:** primary

**14. `array_creation` &rarr; `ArrayRangeInclusive`** (misconception)

- **Exact edge logic (the wrong rule):** new int[n] has slots 0 to n, inclusive.
- **Twin logic (the right rule):** The slots are 0 to n - 1.
- **Role:** context

**15. `array_creation` &rarr; `ArraysGrow`** (misconception)

- **Exact edge logic (the wrong rule):** Storing a value at a[n] in an array of length n makes the array grow.
- **Twin logic (the right rule):** An array's length is fixed when it is created, so a[n] throws an exception.
- **Role:** primary

**16. `array_creation` &rarr; `DeclarationCreatesArray`** (misconception)

- **Exact edge logic (the wrong rule):** int[] a; already makes an array that can be indexed.
- **Twin logic (the right rule):** The declaration only names the array; until new (or an initializer) creates it, using a[i] gives a 'variable might not have been initialized' compile-time error.
- **Role:** context

**17. `array_aliasing` &rarr; `ArrayListIsArray`** (misconception)

- **Exact edge logic (the wrong rule):** An ArrayList is just an array, so it has a fixed length and is indexed with [].
- **Twin logic (the right rule):** An array has a fixed length and uses [] and .length; an ArrayList can grow and uses get, set and size().
- **Role:** context

**18. `array_declaration` &rarr; `ArrayBracketCountIsLength`** (misconception)

- **Exact edge logic (the wrong rule):** The number of brackets in an array type or initializer is the array's length.
- **Twin logic (the right rule):** Brackets give the number of dimensions; the length is set at creation.
- **Role:** primary

**19. `array_declaration` &rarr; `DeclarationCreatesArray`** (misconception)

- **Exact edge logic (the wrong rule):** int[] a; already makes an array that can be indexed.
- **Twin logic (the right rule):** The declaration only names the array; until new (or an initializer) creates it, using a[i] gives a 'variable might not have been initialized' compile-time error.
- **Role:** primary

**20. `array_default_values` &rarr; `ArrayCreationIsFree`** (misconception)

- **Exact edge logic (the wrong rule):** Creating a big array with new takes no time because the elements are not set yet.
- **Twin logic (the right rule):** Java initializes every element when the array is created, so creation takes time proportional to its length.
- **Role:** context

**21. `array_initializer` &rarr; `ArrayBracketCountIsLength`** (misconception)

- **Exact edge logic (the wrong rule):** The number of brackets in an array type or initializer is the array's length.
- **Twin logic (the right rule):** Brackets give the number of dimensions; the length is set at creation.
- **Role:** context

**22. `indexing` &rarr; `ArrayRangeInclusive`** (misconception)

- **Exact edge logic (the wrong rule):** new int[n] has slots 0 to n, inclusive.
- **Twin logic (the right rule):** The slots are 0 to n - 1.
- **Role:** primary

**23. `length_field` &rarr; `ArrayLengthCannotBeZero`** (misconception)

- **Exact edge logic (the wrong rule):** An array cannot have length 0.
- **Twin logic (the right rule):** new int[0] is a legal array of length 0.
- **Role:** context

**24. `multidimensional_array` &rarr; `ArrayBracketCountIsLength`** (misconception)

- **Exact edge logic (the wrong rule):** The number of brackets in an array type or initializer is the array's length.
- **Twin logic (the right rule):** Brackets give the number of dimensions; the length is set at creation.
- **Role:** context

**25. `array_creation` &rarr; `NegativeArraySize`** (error)

- **Exact edge logic (the wrong rule):** new int[n] with a negative n creates an empty array.
- **Twin logic (the right rule):** Creating an array with a negative length throws NegativeArraySizeException at run time.
- **Role:** primary

**26. `run_time_error` &rarr; `NegativeArraySize`** (error)

- **Exact edge logic (the wrong rule):** new int[n] with a negative n creates an empty array.
- **Twin logic (the right rule):** Creating an array with a negative length throws NegativeArraySizeException at run time.
- **Role:** context

**27. `array_creation` &rarr; `array_creation@L0`** (has_level)

- **Exact edge logic:** array creation -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (9 ways).
  - **[0] everyday\_reading** (rule type E, folk-meaning rule): Folk meaning: in maths, a[5] or a\_5 names element 5, and 'new' means 'fresh, empty, ready to fill', so 'new int[5]' is read as 'element 5' or as an empty list that grows. Java rule: new int[n] allocates exactly n elements, indexed 0 to n-1, each already set to the default value, and the length can never change.
  - **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `ArraysGrow`: wrong rule: An array grows as you add elements. Right rule: An array's length is fixed when it is created, so writing to a[n] throws an exception instead of adding a slot.
  - **[2] misconception** (rule type M, wrong rule / right rule) &rarr; `ArrayAllocationWithoutNew`: wrong rule: Arrays are created without the new keyword. Right rule: An array exists only after new T[n] (or an initializer list in a declaration, which implies creation) has run.
  - **[3] misconception** (rule type M, wrong rule / right rule) &rarr; `ArrayLengthCannotBeZero`: wrong rule: An array cannot have length 0. Right rule: new int[0] is a legal array with a.length == 0 (no element can be indexed).
  - **[4] misconception** (rule type M, wrong rule / right rule) &rarr; `ArrayCreationIsFree`: wrong rule: Creating a big array with new takes no time because the elements are not set yet. Right rule: Java initializes every element when the array is created, so creation takes time proportional to its length.
  - **[5] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `ArraysGrow`: Points to LT: evaluate the size, allocate the array, fill it with defaults, return the reference, then assign it. Inconsistent application: the size n is treated as the last index on some lines, or the array is assumed to exist already at its declaration. (here mixing in: "an array grows as you add elements")
  - **[6] misconception** (rule type M, wrong rule / right rule) &rarr; `ArrayRangeInclusive`: wrong rule: new int[n] has slots 0 to n, inclusive. Right rule: new int[n] has exactly n slots, a[0] through a[n-1]; a[n] does not exist.
  - **[7] misconception** (rule type M, wrong rule / right rule) &rarr; `DeclarationCreatesArray`: wrong rule: int[] a; already makes an array that can be indexed. Right rule: Only new (or an initializer) creates the array; before that, using a[i] is the compile-time error 'variable a might not have been initialized'.
  - **[8] misconception** (rule type M, wrong rule / right rule) &rarr; `ArrayBracketCountIsLength`: wrong rule: The number of brackets in new int[][] is the array's length. Right rule: Bracket pairs give the number of dimensions; the length is the value of the dimension expression inside them.

**28. `array_creation` &rarr; `array_creation@L1`** (has_level)

- **Exact edge logic:** array creation -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).
  - **[0] names\_the\_element** (rule type N, identity rule): Identity: an array creation expression; new T[n] makes a new array object with n elements of type T and yields a reference to it.
  - **[1] states\_the\_rule** (rule type S, declarative rule): Declarative: 'new T[expr]', where expr is any int-valued expression evaluated at run time; the resulting length is fixed for the array's lifetime.

**29. `array_creation` &rarr; `array_creation@L2`** (has_level)

- **Exact edge logic:** array creation -&gt; L2 (Multistructural): the answer applies the rules of array creation to every part of the code, in order (3 ways).
  - **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): Sequencing: (1) the dimension expression is evaluated; (2) if it is negative, NegativeArraySizeException is thrown; (3) space for n elements is reserved and every element is set to its default; (4) the expression yields the reference, which an enclosing assignment then stores.
  - **[1] output\_prediction** (rule type OP, evaluation / result rule): Result: a value of type T[], namely a reference to a new array of length n whose elements all hold the default (0, 0.0, false or null). It produces no output; printing it shows an address, not the elements.
  - **[2] one\_step\_execution** (rule type OS, state-transition rule): State transition: one execution creates one new array object (n new element variables at their defaults) and returns its reference. No existing variable changes until that reference is assigned.

**30. `array_creation` &rarr; `array_creation@L3`** (has_level)

- **Exact edge logic:** array creation -&gt; L3 (Relational): the answer relates the parts (8 ways).
  - **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): The declared element type must match the created one; in 'double[] a = new double[N];' the left side is the declaration and the right side is the creation.
  - **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Elements can be indexed only after creation, and the n given to new fixes the valid index range 0..n-1.
  - **[2] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Creation is what puts the default value (0, 0.0, false, null) in every slot; each execution of new gives fresh defaults.
  - **[3] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): The size n given to new becomes a.length and never changes for that array object.
  - **[4] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): An initializer {v0, ..., vk} implies creation of an array of length k+1, so new is not written.
  - **[5] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Only new makes a distinct array. Assignment copies the reference, so a separate copy needs new plus an element-by-element copy.
  - **[6] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): new yields the reference (address) of the array, and the array variable stores that reference, not the elements.
  - **[7] purpose\_of\_the\_whole** (rule type P, plan / role rule): Plan/role: reserve storage for a number of values that may be known only at run time (e.g. N from the command line), before any value is stored.

**31. `array_creation` &rarr; `array_creation@L4`** (has_level)

- **Exact edge logic:** array creation -&gt; L4 (Extended abstract): the answer reasons beyond the given code (6 ways).
  - **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `ArraysGrow`: Conservation: changing n changes a.length and the valid index range but not the element type. Moving 'new' inside a loop gives a fresh array of defaults on every pass (SelfAvoidingWalk relies on this). Re-creating an array never changes arrays that other variables already refer to.
  - **[1] diagnose\_an\_error** (rule type D, error rule): rule broken: The dimension expression of new must be &gt;= 0. Kind: run-time exception. Trigger class: the size evaluates to a negative int, e.g. a negative command-line value, or int overflow such as new int[N\*N\*N\*N] with N = 1000 (NegativeArraySizeException)
  - **[2] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Applicability: use new T[n] when the number of values is known (at least at run time) before they are stored and stays fixed. Use an initializer when the values are compile-time constants, and a resizing structure when the count is unknown in advance.
  - **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: An array must be allocated with new before its elements are accessed. Kind: compile-time. Trigger class: 'int[] a;' followed by a[i] = ... with no creation (variable a might not have been initialized)
  - **[4] diagnose\_an\_error** (rule type D, error rule): rule broken: The dimension expression must have an integral type (int after promotion). Kind: compile-time. Trigger class: a double or long size such as new int[2.5] or new int[n] with long n (incompatible types: possible lossy conversion)
  - **[5] diagnose\_an\_error** (rule type D, error rule): rule broken: The requested array must fit in the memory available to Java. Kind: run-time exception. Trigger class: a very large n such as new boolean[N+1] for huge N in PrimeSieve (OutOfMemoryError)

**32. `topic1.4.a` &rarr; `array_creation`** (contains)

- topic `topic1.4.a` contains `array_creation`

**33. `topic1.4.a` &rarr; `args_length`** (contains)

- topic `topic1.4.a` contains `args_length`

**34. `topic1.4.a` &rarr; `array_declaration`** (contains)

- topic `topic1.4.a` contains `array_declaration`

**35. `topic1.4.a` &rarr; `array_default_values`** (contains)

- topic `topic1.4.a` contains `array_default_values`

**36. `topic1.4.a` &rarr; `data_structure`** (contains)

- topic `topic1.4.a` contains `data_structure`

**37. `topic1.4.a` &rarr; `indexing`** (contains)

- topic `topic1.4.a` contains `indexing`

**38. `topic1.4.a` &rarr; `length_field`** (contains)

- topic `topic1.4.a` contains `length_field`

**39. `topic1.4.a` &rarr; `off_by_one_error`** (contains)

- topic `topic1.4.a` contains `off_by_one_error`
