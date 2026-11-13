# array_aliasing (`array_aliasing`)

two variables can refer to the same array

Section 1.4 Arrays, topic 1.4.b Memory representation and bounds checking.

![The knowledge graph around array_aliasing](array_aliasing.png)

## At a glance

- **Needs first:** `array_creation`, `array_reference`
- **Leads to:** nothing
- **Learned alongside:** `array_copy`, `printing_array_reference`
- **Misconceptions:** `ArrayEqualityComparesValues`, `ArrayListIsArray`, `AssignmentCopiesObject`
- **Errors:** none
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 24 edges around this concept, each explained in the graph's own words.

## What it needs first (2)

A prerequisite edge means the other concept has to be understood before `array_aliasing`.

### `array_creation` comes before `array_aliasing`

*new int[n] -- allocates n slots*

Because new creates one array and the variable stores only a reference to it, assigning that variable to another makes both names refer to the same array.

- **Grounding:** book passage
- **How `array_aliasing` combines with `array_creation`:** Only new creates a distinct array; to copy, create a new array and copy each element (or use Arrays.copyOf).
- **How `array_creation` combines with `array_aliasing`:** Only new makes a distinct array. Assignment copies the reference, so a separate copy needs new plus an element-by-element copy.

### `array_reference` comes before `array_aliasing`

*Array name holds a memory address: the array variable stores the memory address (pointer) of the array; a[i] is found by adding i to that address*

Because an array variable holds a reference, b = a copies the reference, so a and b name the same array.

- **Grounding:** book passage

## What it leads to (0)

These concepts need `array_aliasing` first.

No concept has this one as a prerequisite.

## Learned alongside (2)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

### `array_aliasing` alongside `array_copy`

*making a second, independent array with the same elements: create a new array and copy element by element (or Arrays.copyOf)*

b = a makes a second name for the same array (an alias); copying makes a second array: after a copy, changing b[i] leaves a[i] unchanged.

- **Grounding:** book passage
- **How `array_copy` combines with `array_aliasing`:** b = a makes an alias of the same array; a copy is a different array: changes through one are not seen through the other.

### `array_aliasing` alongside `printing_array_reference`

*printing an array variable prints a reference, not the elements*

Both follow from the array variable holding a reference (memory address): assignment and == act on that reference, and println(a) prints it.

- **Grounding:** questionable
- **How `array_aliasing` combines with `printing_array_reference`:** Assignment, == and println(a) all act on the reference value: two aliases print the same address, while two equal-content arrays print different ones.
- **How `printing_array_reference` combines with `array_aliasing`:** Two aliases print the same text, and two separately created arrays with equal contents print different text, because println shows the reference that assignment and == also act on.

## Misconceptions (3)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### ArrayEqualityComparesValues

- **Wrong rule:** a == b is true when a and b hold the same values.
- **Right rule:** == compares whether the two arrays are the same array, not whether their values are equal.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: a == b is true when a and b hold the same values. Right rule: == compares whether a and b are the same array (same reference), not whether their elements are equal.
- **Shows at level L0 as:** inconsistent trace: Points to LT: b = a copies the reference, so every later write through b is a write to the shared array. Inconsistent application: after b = a the trace changes b[0] but leaves a[0] unchanged in its table, keeping two copies on some steps and one array on others. (here mixing in: "a == b is true when a and b hold the same values")
- **Also an edge from `array_copy`:** a == b is true when a and b hold the same values.

### ArrayListIsArray

- **Wrong rule:** An ArrayList is just an array, so it has a fixed length and is indexed with [].
- **Right rule:** An array has a fixed length and uses [] and .length; an ArrayList can grow and uses get, set and size().
- **Role of this concept:** context
- **Also an edge from `array_creation`:** an ArrayList is an array (borderline; beyond Chapter 1 CS1)

### AssignmentCopiesObject

- **Wrong rule:** assigning a reference copies the object
- **Right rule:** b = a; copies only the reference, so a and b refer to the same array and b[i] = v also changes a[i].
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: Assigning an array reference copies the array. Right rule: b = a; copies only the reference, so a and b refer to the same array and b[i] = v also changes a[i].
- **Also an edge from `array_copy`:** assigning a reference copies the object
- **Also an edge from `assignment`:** b = a; for an array makes b a separate copy, so changing b[i] leaves a[i] unchanged.

## Errors (0)

An error edge states the rule that gets broken in a program, and the right rule.

The graph has no error edge from this concept.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for array aliasing: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to array aliasing agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

array aliasing -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (4 ways).

- **everyday reading** (folk-meaning rule): Folk meaning: in maths and English, 'b = a' means b becomes an equal but independent copy, and 'a == b' means 'have the same values'. Java rule: for arrays, b = a copies only the reference, so both names denote one array, and == tests whether two names refer to the same array.
- **misconception** (wrong rule / right rule; shows `ArrayEqualityComparesValues`): wrong rule: a == b is true when a and b hold the same values. Right rule: == compares whether a and b are the same array (same reference), not whether their elements are equal.
- **misconception** (wrong rule / right rule; shows `AssignmentCopiesObject`): wrong rule: Assigning an array reference copies the array. Right rule: b = a; copies only the reference, so a and b refer to the same array and b[i] = v also changes a[i].
- **inconsistent trace** (uneven-application rule; shows `ArrayEqualityComparesValues`): Points to LT: b = a copies the reference, so every later write through b is a write to the shared array. Inconsistent application: after b = a the trace changes b[0] but leaves a[0] unchanged in its table, keeping two copies on some steps and one array on others. (here mixing in: "a == b is true when a and b hold the same values")

### L1: Unistructural / atom x text surface

L1 for array aliasing: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

array aliasing -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

- **names the element** (identity rule): Identity: aliasing is the situation in which two or more array variables refer to the same array object.
- **states the rule** (declarative rule): Declarative: an assignment makes the names a and b refer to the same array; an equality test a == b checks whether the two names refer to the same array.

### L2: Multistructural / block x execution / preoperational

L2 for array aliasing: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

array aliasing -&gt; L2 (Multistructural): the answer applies the rules of array aliasing to every part of the code, in order (3 ways).

- **line by line trace** (operational sequencing rule): Sequencing: in b = a, a is evaluated to its reference value, which is then stored in b; no element is read or copied. In a == b both reference values are evaluated and compared.
- **output prediction** (evaluation / result rule): Result: for int[] a = {1, 2, 3}; int[] b = {1, 2, 3};, the test a == b is false; after b = a it is true. A read through either name gives the same element.
- **one step execution** (state-transition rule): State transition: b = a changes only the variable b (it now holds a's reference). A later b[0] = 17 changes the one shared array, so a[0] then reads 17 too.

### L3: Relational / relations x function (concrete operational begins)

L3 for array aliasing: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

array aliasing -&gt; L3 (Relational): the answer relates the parts (4 ways).

- **relation to neighbour** (composition rule (with a neighbour)): Only new creates a distinct array; to copy, create a new array and copy each element (or use Arrays.copyOf).
- **relation to neighbour** (composition rule (with a neighbour)): Assignment, == and println(a) all act on the reference value: two aliases print the same address, while two equal-content arrays print different ones.
- **relation to neighbour** (composition rule (with a neighbour)): b = a makes a second name for the same array (an alias); copying makes a second array: after a copy, changing b[i] leaves a[i] unchanged.
- **purpose of the whole** (plan / role rule): Plan/role: aliasing lets two names work on one array without copying (as when an array is passed to a method), but in Chapter 1 code it is mostly a source of subtle bugs.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for array aliasing: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

array aliasing -&gt; L4 (Extended abstract): the answer reasons beyond the given code (4 ways).

- **predict a change** (conservation rule; shows `ArrayEqualityComparesValues`): Conservation: replacing b = a with an element-copy loop keeps b's initial contents but breaks the link, so later changes to a no longer show in b. Reassigning a = new int[n] after b = a leaves b on the old array.
- **transfer to a new program** (applicability rule): Applicability: assign an array variable when you want a second name for the same data. Use a copy loop or Arrays.copyOf for an independent copy, and an element loop or Arrays.equals to compare contents.
- **diagnose an error** (error rule): rule broken: Assignment copies the reference, not the elements. Kind: silent logic error. Trigger class: b = a is used as a 'copy', and then b is modified while a is expected to stay unchanged (or the reverse)
- **diagnose an error** (error rule): rule broken: == on arrays compares references, not contents. Kind: silent logic error. Trigger class: two separately created arrays with equal elements are compared with == (always false)

## Same topic

`array_aliasing` belongs to the topic **Memory representation and bounds checking** (`topic1.4.b`). The topic also contains: `array_bounds`, `array_copy`, `array_reference`, `loop_guard`, `primitive_vs_reference`, `printing_array_reference`, `program_state`.

## Rules of the concept (16)

- **folk-meaning rule:** Folk meaning: in maths and English, 'b = a' means b becomes an equal but independent copy, and 'a == b' means 'have the same values'. Java rule: for arrays, b = a copies only the reference, so both names denote one array, and == tests whether two names refer to the same array.
- **wrong rule / right rule:** ArrayEqualityComparesValues: wrong: a == b is true when a and b hold the same values. \| right: == compares whether a and b are the same array (same reference), not whether their elements are equal.
- **wrong rule / right rule:** AssignmentCopiesObject: wrong: Assigning an array reference copies the array. \| right: b = a; copies only the reference, so a and b refer to the same array and b[i] = v also changes a[i].
- **uneven-application rule:** Points to LT: b = a copies the reference, so every later write through b is a write to the shared array. Inconsistent application: after b = a the trace changes b[0] but leaves a[0] unchanged in its table, keeping two copies on some steps and one array on others.
- **identity rule:** Identity: aliasing is the situation in which two or more array variables refer to the same array object.
- **declarative rule:** Declarative: an assignment makes the names a and b refer to the same array; an equality test a == b checks whether the two names refer to the same array.
- **operational sequencing rule:** Sequencing: in b = a, a is evaluated to its reference value, which is then stored in b; no element is read or copied. In a == b both reference values are evaluated and compared.
- **evaluation / result rule:** Result: for int[] a = {1, 2, 3}; int[] b = {1, 2, 3};, the test a == b is false; after b = a it is true. A read through either name gives the same element.
- **state-transition rule:** State transition: b = a changes only the variable b (it now holds a's reference). A later b[0] = 17 changes the one shared array, so a[0] then reads 17 too.
- **composition rule (with a neighbour):** with array\_creation: Only new creates a distinct array; to copy, create a new array and copy each element (or use Arrays.copyOf).
- **composition rule (with a neighbour):** with printing\_array\_reference: Assignment, == and println(a) all act on the reference value: two aliases print the same address, while two equal-content arrays print different ones.
- **plan / role rule:** Plan/role: aliasing lets two names work on one array without copying (as when an array is passed to a method), but in Chapter 1 code it is mostly a source of subtle bugs.
- **conservation rule:** Conservation: replacing b = a with an element-copy loop keeps b's initial contents but breaks the link, so later changes to a no longer show in b. Reassigning a = new int[n] after b = a leaves b on the old array.
- **error rule:** rule broken: Assignment copies the reference, not the elements. (silent logic error)
- **error rule:** rule broken: == on arrays compares references, not contents. (silent logic error)
- **applicability rule:** Applicability: assign an array variable when you want a second name for the same data. Use a copy loop or Arrays.copyOf for an independent copy, and an element loop or Arrays.equals to compare contents.

## The whole prerequisite chain

- **Everything it builds on (5):** `array_creation`, `array_declaration`, `array_reference`, `data_structure`, `data_type`
- **Everything that builds on it (0):** nothing
