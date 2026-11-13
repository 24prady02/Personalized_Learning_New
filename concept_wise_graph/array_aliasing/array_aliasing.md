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

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 24 edges around this concept. The edge logic, the wrong and right rules and the exact rules of the ways are copied word for word from the graph.

## To work on (1)

- misconceptions with no L0 way linked to them: ArrayListIsArray

## What it needs first (2)

A prerequisite edge means the other concept has to be understood before `array_aliasing`.

### `array_creation` comes before `array_aliasing`

*new int[n] -- allocates n slots*

- **Edge:** `pre:array_creation->array_aliasing`
- **Exact edge logic:** Because new creates one array and the variable stores only a reference to it, assigning that variable to another makes both names refer to the same array.
- **Grounding:** book\_passage
- **Composition rule (R) of `array_aliasing` with `array_creation`:** Only new creates a distinct array; to copy, create a new array and copy each element (or use Arrays.copyOf).
- **Composition rule (R) of `array_creation` with `array_aliasing`:** Only new makes a distinct array. Assignment copies the reference, so a separate copy needs new plus an element-by-element copy.

### `array_reference` comes before `array_aliasing`

*Array name holds a memory address: the array variable stores the memory address (pointer) of the array; a[i] is found by adding i to that address*

- **Edge:** `pre:array_reference->array_aliasing`
- **Exact edge logic:** Because an array variable holds a reference, b = a copies the reference, so a and b name the same array.
- **Grounding:** book\_passage

## What it leads to (0)

These concepts need `array_aliasing` first.

No concept has this one as a prerequisite.

## Learned alongside (2)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

### `array_aliasing` alongside `array_copy`

*making a second, independent array with the same elements: create a new array and copy element by element (or Arrays.copyOf)*

- **Edge:** `par:array_copy~array_aliasing`
- **Exact edge logic:** b = a makes a second name for the same array (an alias); copying makes a second array: after a copy, changing b[i] leaves a[i] unchanged.
- **Grounding:** book\_passage
- **Composition rule (R) of `array_copy` with `array_aliasing`:** b = a makes an alias of the same array; a copy is a different array: changes through one are not seen through the other.

### `array_aliasing` alongside `printing_array_reference`

*printing an array variable prints a reference, not the elements*

- **Edge:** `par:array_aliasing~printing_array_reference`
- **Exact edge logic:** Both follow from the array variable holding a reference (memory address): assignment and == act on that reference, and println(a) prints it.
- **Grounding:** questionable
- **Composition rule (R) of `array_aliasing` with `printing_array_reference`:** Assignment, == and println(a) all act on the reference value: two aliases print the same address, while two equal-content arrays print different ones.
- **Composition rule (R) of `printing_array_reference` with `array_aliasing`:** Two aliases print the same text, and two separately created arrays with equal contents print different text, because println shows the reference that assignment and == also act on.

## Misconceptions (3)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### ArrayEqualityComparesValues

- **Edge:** `array_aliasing` &rarr; `ArrayEqualityComparesValues` (misconception)
- **Exact edge logic (the wrong rule):** a == b is true when a and b hold the same values.
- **Twin logic (the right rule):** == compares whether the two arrays are the same array, not whether their values are equal.
- **Wrong belief (on the node):** a == b is true when a and b hold the same values.
- **Correct rule (on the node):** == compares whether the two arrays are the same array, not whether their values are equal.
- **Provenance:** textbook
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [1] misconception, exact rule:** wrong rule: a == b is true when a and b hold the same values. Right rule: == compares whether a and b are the same array (same reference), not whether their elements are equal.
- **L0 way [3] inconsistent\_trace, exact rule:** Points to LT: b = a copies the reference, so every later write through b is a write to the shared array. Inconsistent application: after b = a the trace changes b[0] but leaves a[0] unchanged in its table, keeping two copies on some steps and one array on others. (here mixing in: "a == b is true when a and b hold the same values")
- **Edge `array_copy` &rarr; `ArrayEqualityComparesValues`, exact edge logic:** a == b is true when a and b hold the same values. **Twin logic:** == compares whether the two arrays are the same array, not whether their values are equal. (role: context)

### ArrayListIsArray

- **Edge:** `array_aliasing` &rarr; `ArrayListIsArray` (misconception)
- **Exact edge logic (the wrong rule):** An ArrayList is just an array, so it has a fixed length and is indexed with [].
- **Twin logic (the right rule):** An array has a fixed length and uses [] and .length; an ArrayList can grow and uses get, set and size().
- **Wrong belief (on the node):** an ArrayList is an array (borderline; beyond Chapter 1 CS1)
- **Correct rule (on the node):** An array has a fixed length and uses [] and .length; an ArrayList can grow and uses get, set and size().
- **Provenance:** published
- **Role of this concept:** context
- **L0 way linked to it:** no
- **Edge `array_creation` &rarr; `ArrayListIsArray`, exact edge logic:** an ArrayList is an array (borderline; beyond Chapter 1 CS1) **Twin logic:** An array has a fixed length and uses [] and .length; an ArrayList can grow and uses get, set and size(). (role: primary)

### AssignmentCopiesObject

- **Edge:** `array_aliasing` &rarr; `AssignmentCopiesObject` (misconception)
- **Exact edge logic (the wrong rule):** assigning a reference copies the object
- **Twin logic (the right rule):** b = a; copies only the reference, so a and b refer to the same array and b[i] = v also changes a[i].
- **Wrong belief (on the node):** assigning a reference copies the object
- **Correct rule (on the node):** b = a; copies only the reference, so a and b refer to the same array and b[i] = v also changes a[i].
- **Provenance:** published
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [2] misconception, exact rule:** wrong rule: Assigning an array reference copies the array. Right rule: b = a; copies only the reference, so a and b refer to the same array and b[i] = v also changes a[i].
- **Edge `array_copy` &rarr; `AssignmentCopiesObject`, exact edge logic:** assigning a reference copies the object **Twin logic:** b = a; copies only the reference, so a and b refer to the same array and b[i] = v also changes a[i]. (role: context)
- **Edge `assignment` &rarr; `AssignmentCopiesObject`, exact edge logic:** b = a; for an array makes b a separate copy, so changing b[i] leaves a[i] unchanged. **Twin logic:** b = a; copies only the reference, so a and b refer to the same array and b[i] = v also changes a[i]. (role: context)

## Errors (0)

An error edge states the rule that gets broken in a program, and the right rule.

The graph has no error edge from this concept.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for array aliasing: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to array aliasing agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

- **Edge:** `array_aliasing` &rarr; `array_aliasing@L0` (has_level)
- **Exact edge logic:** array aliasing -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (4 ways).

Ways (4), each with its exact rule:

- **[0] everyday\_reading** (rule type E, folk-meaning rule): Folk meaning: in maths and English, 'b = a' means b becomes an equal but independent copy, and 'a == b' means 'have the same values'. Java rule: for arrays, b = a copies only the reference, so both names denote one array, and == tests whether two names refer to the same array.
- **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `ArrayEqualityComparesValues`: wrong rule: a == b is true when a and b hold the same values. Right rule: == compares whether a and b are the same array (same reference), not whether their elements are equal.
- **[2] misconception** (rule type M, wrong rule / right rule) &rarr; `AssignmentCopiesObject`: wrong rule: Assigning an array reference copies the array. Right rule: b = a; copies only the reference, so a and b refer to the same array and b[i] = v also changes a[i].
- **[3] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `ArrayEqualityComparesValues`: Points to LT: b = a copies the reference, so every later write through b is a write to the shared array. Inconsistent application: after b = a the trace changes b[0] but leaves a[0] unchanged in its table, keeping two copies on some steps and one array on others. (here mixing in: "a == b is true when a and b hold the same values")

### L1: Unistructural / atom x text surface

L1 for array aliasing: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

- **Edge:** `array_aliasing` &rarr; `array_aliasing@L1` (has_level)
- **Exact edge logic:** array aliasing -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

Ways (2), each with its exact rule:

- **[0] names\_the\_element** (rule type N, identity rule): Identity: aliasing is the situation in which two or more array variables refer to the same array object.
- **[1] states\_the\_rule** (rule type S, declarative rule): Declarative: an assignment makes the names a and b refer to the same array; an equality test a == b checks whether the two names refer to the same array.

### L2: Multistructural / block x execution / preoperational

L2 for array aliasing: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

- **Edge:** `array_aliasing` &rarr; `array_aliasing@L2` (has_level)
- **Exact edge logic:** array aliasing -&gt; L2 (Multistructural): the answer applies the rules of array aliasing to every part of the code, in order (3 ways).

Ways (3), each with its exact rule:

- **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): Sequencing: in b = a, a is evaluated to its reference value, which is then stored in b; no element is read or copied. In a == b both reference values are evaluated and compared.
- **[1] output\_prediction** (rule type OP, evaluation / result rule): Result: for int[] a = {1, 2, 3}; int[] b = {1, 2, 3};, the test a == b is false; after b = a it is true. A read through either name gives the same element.
- **[2] one\_step\_execution** (rule type OS, state-transition rule): State transition: b = a changes only the variable b (it now holds a's reference). A later b[0] = 17 changes the one shared array, so a[0] then reads 17 too.

### L3: Relational / relations x function (concrete operational begins)

L3 for array aliasing: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

- **Edge:** `array_aliasing` &rarr; `array_aliasing@L3` (has_level)
- **Exact edge logic:** array aliasing -&gt; L3 (Relational): the answer relates the parts (4 ways).

Ways (4), each with its exact rule:

- **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Only new creates a distinct array; to copy, create a new array and copy each element (or use Arrays.copyOf).
- **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Assignment, == and println(a) all act on the reference value: two aliases print the same address, while two equal-content arrays print different ones.
- **[2] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): b = a makes a second name for the same array (an alias); copying makes a second array: after a copy, changing b[i] leaves a[i] unchanged.
- **[3] purpose\_of\_the\_whole** (rule type P, plan / role rule): Plan/role: aliasing lets two names work on one array without copying (as when an array is passed to a method), but in Chapter 1 code it is mostly a source of subtle bugs.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for array aliasing: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

- **Edge:** `array_aliasing` &rarr; `array_aliasing@L4` (has_level)
- **Exact edge logic:** array aliasing -&gt; L4 (Extended abstract): the answer reasons beyond the given code (4 ways).

Ways (4), each with its exact rule:

- **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `ArrayEqualityComparesValues`: Conservation: replacing b = a with an element-copy loop keeps b's initial contents but breaks the link, so later changes to a no longer show in b. Reassigning a = new int[n] after b = a leaves b on the old array.
- **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Applicability: assign an array variable when you want a second name for the same data. Use a copy loop or Arrays.copyOf for an independent copy, and an element loop or Arrays.equals to compare contents.
- **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: Assignment copies the reference, not the elements. Kind: silent logic error. Trigger class: b = a is used as a 'copy', and then b is modified while a is expected to stay unchanged (or the reverse)
- **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: == on arrays compares references, not contents. Kind: silent logic error. Trigger class: two separately created arrays with equal elements are compared with == (always false)

## Same topic

`array_aliasing` belongs to the topic **Memory representation and bounds checking** (`topic1.4.b`). The topic also contains: `array_bounds`, `array_copy`, `array_reference`, `loop_guard`, `primitive_vs_reference`, `printing_array_reference`, `program_state`.

## Rules of the concept (16)

- **Book** (SW-1e, p. 97 (pdf 107)): "An assignment makes the names a and b refer to the same array."
- **Book** (SW-1e, p. 112 (pdf 122)): "The expression evaluates to true only if a[] and b[] refer to the same array, not if they have the same sequence of elements."
- **Book** (SW-1.4, ): "The == operator compares whether the (memory addresses of the) two arrays are identical, not whether their corresponding values are equal."
- **E** (folk-meaning rule): Folk meaning: in maths and English, 'b = a' means b becomes an equal but independent copy, and 'a == b' means 'have the same values'. Java rule: for arrays, b = a copies only the reference, so both names denote one array, and == tests whether two names refer to the same array.
- **M** (wrong rule / right rule): ArrayEqualityComparesValues: wrong: a == b is true when a and b hold the same values. \| right: == compares whether a and b are the same array (same reference), not whether their elements are equal.
- **M** (wrong rule / right rule): AssignmentCopiesObject: wrong: Assigning an array reference copies the array. \| right: b = a; copies only the reference, so a and b refer to the same array and b[i] = v also changes a[i].
- **T** (uneven-application rule): Points to LT: b = a copies the reference, so every later write through b is a write to the shared array. Inconsistent application: after b = a the trace changes b[0] but leaves a[0] unchanged in its table, keeping two copies on some steps and one array on others.
- **N** (identity rule): Identity: aliasing is the situation in which two or more array variables refer to the same array object.
- **S** (declarative rule): Declarative: an assignment makes the names a and b refer to the same array; an equality test a == b checks whether the two names refer to the same array.
- **LT** (operational sequencing rule): Sequencing: in b = a, a is evaluated to its reference value, which is then stored in b; no element is read or copied. In a == b both reference values are evaluated and compared.
- **OP** (evaluation / result rule): Result: for int[] a = {1, 2, 3}; int[] b = {1, 2, 3};, the test a == b is false; after b = a it is true. A read through either name gives the same element.
- **OS** (state-transition rule): State transition: b = a changes only the variable b (it now holds a's reference). A later b[0] = 17 changes the one shared array, so a[0] then reads 17 too.
- **R** (composition rule (with a neighbour)): with array\_creation: Only new creates a distinct array; to copy, create a new array and copy each element (or use Arrays.copyOf).
- **R** (composition rule (with a neighbour)): with printing\_array\_reference: Assignment, == and println(a) all act on the reference value: two aliases print the same address, while two equal-content arrays print different ones.
- **P** (plan / role rule): Plan/role: aliasing lets two names work on one array without copying (as when an array is passed to a method), but in Chapter 1 code it is mostly a source of subtle bugs.
- **C** (conservation rule): Conservation: replacing b = a with an element-copy loop keeps b's initial contents but breaks the link, so later changes to a no longer show in b. Reassigning a = new int[n] after b = a leaves b on the old array.
- **D** (error rule): rule broken: Assignment copies the reference, not the elements. (silent logic error)
- **D** (error rule): rule broken: == on arrays compares references, not contents. (silent logic error)
- **X** (applicability rule): Applicability: assign an array variable when you want a second name for the same data. Use a copy loop or Arrays.copyOf for an independent copy, and an element loop or Arrays.equals to compare contents.

## How it is found in code and answers (reader block)

- **Aliases:** alias, aliasing, same array
- **Code patterns:** `(?:int|double|boolean|char|long|String|float|short|byte)\s*\[\]\s*\w+\s*=\s*[A-Za-z_]\w*\s*;`
- **Operator symbols:** none
- **Java types:** none

## The whole prerequisite chain

- **Everything it builds on (5):** `array_creation`, `array_declaration`, `array_reference`, `data_structure`, `data_type`
- **Everything that builds on it (0):** nothing

## Every edge in this view and its exact edge logic (24)

All the edges drawn in the picture, in the order: prerequisite, parallel, misconception, error, has_level, contains.

**1. `array_creation` &rarr; `array_aliasing`** (prerequisite)

- **Exact edge logic:** Because new creates one array and the variable stores only a reference to it, assigning that variable to another makes both names refer to the same array.
- **Grounding:** book\_passage
- **Composition rule (R) of `array_creation` with `array_aliasing`:** Only new makes a distinct array. Assignment copies the reference, so a separate copy needs new plus an element-by-element copy.
- **Composition rule (R) of `array_aliasing` with `array_creation`:** Only new creates a distinct array; to copy, create a new array and copy each element (or use Arrays.copyOf).

**2. `array_reference` &rarr; `array_aliasing`** (prerequisite)

- **Exact edge logic:** Because an array variable holds a reference, b = a copies the reference, so a and b name the same array.
- **Grounding:** book\_passage

**3. `array_aliasing` &harr; `printing_array_reference`** (parallel)

- **Exact edge logic:** Both follow from the array variable holding a reference (memory address): assignment and == act on that reference, and println(a) prints it.
- **Grounding:** questionable
- **Composition rule (R) of `array_aliasing` with `printing_array_reference`:** Assignment, == and println(a) all act on the reference value: two aliases print the same address, while two equal-content arrays print different ones.
- **Composition rule (R) of `printing_array_reference` with `array_aliasing`:** Two aliases print the same text, and two separately created arrays with equal contents print different text, because println shows the reference that assignment and == also act on.

**4. `array_copy` &harr; `array_aliasing`** (parallel)

- **Exact edge logic:** b = a makes a second name for the same array (an alias); copying makes a second array: after a copy, changing b[i] leaves a[i] unchanged.
- **Grounding:** book\_passage
- **Composition rule (R) of `array_copy` with `array_aliasing`:** b = a makes an alias of the same array; a copy is a different array: changes through one are not seen through the other.

**5. `array_aliasing` &rarr; `ArrayEqualityComparesValues`** (misconception)

- **Exact edge logic (the wrong rule):** a == b is true when a and b hold the same values.
- **Twin logic (the right rule):** == compares whether the two arrays are the same array, not whether their values are equal.
- **Role:** primary

**6. `array_aliasing` &rarr; `ArrayListIsArray`** (misconception)

- **Exact edge logic (the wrong rule):** An ArrayList is just an array, so it has a fixed length and is indexed with [].
- **Twin logic (the right rule):** An array has a fixed length and uses [] and .length; an ArrayList can grow and uses get, set and size().
- **Role:** context

**7. `array_aliasing` &rarr; `AssignmentCopiesObject`** (misconception)

- **Exact edge logic (the wrong rule):** assigning a reference copies the object
- **Twin logic (the right rule):** b = a; copies only the reference, so a and b refer to the same array and b[i] = v also changes a[i].
- **Role:** primary

**8. `array_copy` &rarr; `ArrayEqualityComparesValues`** (misconception)

- **Exact edge logic (the wrong rule):** a == b is true when a and b hold the same values.
- **Twin logic (the right rule):** == compares whether the two arrays are the same array, not whether their values are equal.
- **Role:** context

**9. `array_copy` &rarr; `AssignmentCopiesObject`** (misconception)

- **Exact edge logic (the wrong rule):** assigning a reference copies the object
- **Twin logic (the right rule):** b = a; copies only the reference, so a and b refer to the same array and b[i] = v also changes a[i].
- **Role:** context

**10. `array_creation` &rarr; `ArrayListIsArray`** (misconception)

- **Exact edge logic (the wrong rule):** an ArrayList is an array (borderline; beyond Chapter 1 CS1)
- **Twin logic (the right rule):** An array has a fixed length and uses [] and .length; an ArrayList can grow and uses get, set and size().
- **Role:** primary

**11. `assignment` &rarr; `AssignmentCopiesObject`** (misconception)

- **Exact edge logic (the wrong rule):** b = a; for an array makes b a separate copy, so changing b[i] leaves a[i] unchanged.
- **Twin logic (the right rule):** b = a; copies only the reference, so a and b refer to the same array and b[i] = v also changes a[i].
- **Role:** context

**12. `array_aliasing` &rarr; `array_aliasing@L0`** (has_level)

- **Exact edge logic:** array aliasing -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (4 ways).
  - **[0] everyday\_reading** (rule type E, folk-meaning rule): Folk meaning: in maths and English, 'b = a' means b becomes an equal but independent copy, and 'a == b' means 'have the same values'. Java rule: for arrays, b = a copies only the reference, so both names denote one array, and == tests whether two names refer to the same array.
  - **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `ArrayEqualityComparesValues`: wrong rule: a == b is true when a and b hold the same values. Right rule: == compares whether a and b are the same array (same reference), not whether their elements are equal.
  - **[2] misconception** (rule type M, wrong rule / right rule) &rarr; `AssignmentCopiesObject`: wrong rule: Assigning an array reference copies the array. Right rule: b = a; copies only the reference, so a and b refer to the same array and b[i] = v also changes a[i].
  - **[3] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `ArrayEqualityComparesValues`: Points to LT: b = a copies the reference, so every later write through b is a write to the shared array. Inconsistent application: after b = a the trace changes b[0] but leaves a[0] unchanged in its table, keeping two copies on some steps and one array on others. (here mixing in: "a == b is true when a and b hold the same values")

**13. `array_aliasing` &rarr; `array_aliasing@L1`** (has_level)

- **Exact edge logic:** array aliasing -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).
  - **[0] names\_the\_element** (rule type N, identity rule): Identity: aliasing is the situation in which two or more array variables refer to the same array object.
  - **[1] states\_the\_rule** (rule type S, declarative rule): Declarative: an assignment makes the names a and b refer to the same array; an equality test a == b checks whether the two names refer to the same array.

**14. `array_aliasing` &rarr; `array_aliasing@L2`** (has_level)

- **Exact edge logic:** array aliasing -&gt; L2 (Multistructural): the answer applies the rules of array aliasing to every part of the code, in order (3 ways).
  - **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): Sequencing: in b = a, a is evaluated to its reference value, which is then stored in b; no element is read or copied. In a == b both reference values are evaluated and compared.
  - **[1] output\_prediction** (rule type OP, evaluation / result rule): Result: for int[] a = {1, 2, 3}; int[] b = {1, 2, 3};, the test a == b is false; after b = a it is true. A read through either name gives the same element.
  - **[2] one\_step\_execution** (rule type OS, state-transition rule): State transition: b = a changes only the variable b (it now holds a's reference). A later b[0] = 17 changes the one shared array, so a[0] then reads 17 too.

**15. `array_aliasing` &rarr; `array_aliasing@L3`** (has_level)

- **Exact edge logic:** array aliasing -&gt; L3 (Relational): the answer relates the parts (4 ways).
  - **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Only new creates a distinct array; to copy, create a new array and copy each element (or use Arrays.copyOf).
  - **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Assignment, == and println(a) all act on the reference value: two aliases print the same address, while two equal-content arrays print different ones.
  - **[2] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): b = a makes a second name for the same array (an alias); copying makes a second array: after a copy, changing b[i] leaves a[i] unchanged.
  - **[3] purpose\_of\_the\_whole** (rule type P, plan / role rule): Plan/role: aliasing lets two names work on one array without copying (as when an array is passed to a method), but in Chapter 1 code it is mostly a source of subtle bugs.

**16. `array_aliasing` &rarr; `array_aliasing@L4`** (has_level)

- **Exact edge logic:** array aliasing -&gt; L4 (Extended abstract): the answer reasons beyond the given code (4 ways).
  - **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `ArrayEqualityComparesValues`: Conservation: replacing b = a with an element-copy loop keeps b's initial contents but breaks the link, so later changes to a no longer show in b. Reassigning a = new int[n] after b = a leaves b on the old array.
  - **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Applicability: assign an array variable when you want a second name for the same data. Use a copy loop or Arrays.copyOf for an independent copy, and an element loop or Arrays.equals to compare contents.
  - **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: Assignment copies the reference, not the elements. Kind: silent logic error. Trigger class: b = a is used as a 'copy', and then b is modified while a is expected to stay unchanged (or the reverse)
  - **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: == on arrays compares references, not contents. Kind: silent logic error. Trigger class: two separately created arrays with equal elements are compared with == (always false)

**17. `topic1.4.b` &rarr; `array_aliasing`** (contains)

- topic `topic1.4.b` contains `array_aliasing`

**18. `topic1.4.b` &rarr; `array_bounds`** (contains)

- topic `topic1.4.b` contains `array_bounds`

**19. `topic1.4.b` &rarr; `array_copy`** (contains)

- topic `topic1.4.b` contains `array_copy`

**20. `topic1.4.b` &rarr; `array_reference`** (contains)

- topic `topic1.4.b` contains `array_reference`

**21. `topic1.4.b` &rarr; `loop_guard`** (contains)

- topic `topic1.4.b` contains `loop_guard`

**22. `topic1.4.b` &rarr; `primitive_vs_reference`** (contains)

- topic `topic1.4.b` contains `primitive_vs_reference`

**23. `topic1.4.b` &rarr; `printing_array_reference`** (contains)

- topic `topic1.4.b` contains `printing_array_reference`

**24. `topic1.4.b` &rarr; `program_state`** (contains)

- topic `topic1.4.b` contains `program_state`
