# Array name holds a memory address (`array_reference`)

the array variable stores the memory address (pointer) of the array; a[i] is found by adding i to that address

Section 1.4 1.4 Arrays, topic 1.4.b Memory representation and bounds checking.

![The knowledge graph around array_reference](array_reference.png)

## At a glance

- **Needs first:** `array_creation`, `array_declaration`
- **Leads to:** `array_aliasing`, `primitive_vs_reference`, `printing_array_reference`
- **Learned alongside:** nothing
- **Misconceptions:** none
- **Errors:** none
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 18 edges around this concept, each explained in the graph's own words.

## What it needs first (2)

A prerequisite edge means the other concept has to be understood before `array_reference`.

### `array_creation` comes before `array_reference`

*new int[n] -- allocates n slots*

When an array is created, the array name stores the memory address of its values; a[i] is found by adding i to that address.

- **Grounding:** book passage
- **How `array_reference` combines with `array_creation`:** new reserves the memory and yields the array's address, which the array variable then stores.
- **How `array_creation` combines with `array_reference`:** new yields the reference (address) of the array, and the array variable stores that reference, not the elements.

### `array_declaration` comes before `array_reference`

*int[] a; -- declares an array variable*

Declaring an array variable creates only a variable that holds a reference to an array; the array itself is a separate object.

- **Grounding:** spec passage

## What it leads to (3)

These concepts need `array_reference` first.

### `array_reference` comes before `array_aliasing`

*two variables can refer to the same array*

Because an array variable holds a reference, b = a copies the reference, so a and b name the same array.

- **Grounding:** book passage

### `array_reference` comes before `primitive_vs_reference`

*a primitive variable holds its value; an array (or String) variable holds a reference to the object stored elsewhere*

An array variable stores the memory address of the array, not its elements.

- **Grounding:** book passage
- **How `primitive_vs_reference` combines with `array_reference`:** An array variable is the standard example of a reference: its value is the memory address of the array.

### `array_reference` comes before `printing_array_reference`

*printing an array variable prints a reference, not the elements*

Printing an array variable prints the reference it holds, not the elements.

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

L0 for Array name holds a memory address: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to Array name holds a memory address agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

Array name holds a memory address -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (1 way).

- **everyday reading** (folk-meaning rule): Folk meaning: a variable is a box, so the array's values are 'inside' a. Java rule: the variable a holds only a reference (memory address, pointer) to the array object, which lives elsewhere.

### L1: Unistructural / atom x text surface

L1 for Array name holds a memory address: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

Array name holds a memory address -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

- **names the element** (identity rule): Identity: an array reference, the value of an array variable; it is the memory address of the array, called a pointer.
- **states the rule** (declarative rule): Declarative: a variable of array type holds a reference to an array object; operations on the name itself (assignment, ==, printing) act on that address.

### L2: Multistructural / block x execution / preoperational

L2 for Array name holds a memory address: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

Array name holds a memory address -&gt; L2 (Multistructural): the answer applies the rules of Array name holds a memory address to every part of the code, in order (3 ways).

- **line by line trace** (operational sequencing rule): Sequencing: for a[i], the address stored in a is read, the index i is added (scaled by the element size), and the memory at the resulting address is accessed: two elementary operations.
- **output prediction** (evaluation / result rule): Result: the value of a is a reference (printed as hexadecimal). With the array at locations 523..530, a[4] is found at location 523 + 4 = 527.
- **one step execution** (state-transition rule): State transition: assigning a reference (a = b, or a = new ...) changes only which array the variable points to; the arrays themselves are unchanged.

### L3: Relational / relations x function (concrete operational begins)

L3 for Array name holds a memory address: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

Array name holds a memory address -&gt; L3 (Relational): the answer relates the parts (3 ways).

- **relation to neighbour** (composition rule (with a neighbour)): new reserves the memory and yields the array's address, which the array variable then stores.
- **relation to neighbour** (composition rule (with a neighbour)): An array variable stores the memory address of the array, not its elements.
- **purpose of the whole** (plan / role rule): Plan/role: the model that explains constant-time indexing, aliasing, reference equality and printing of arrays.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for Array name holds a memory address: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

Array name holds a memory address -&gt; L4 (Extended abstract): the answer reasons beyond the given code (3 ways).

- **predict a change** (conservation rule): Conservation: copying a reference keeps one shared array (changes through either name are seen by both); assigning a new reference breaks the link without changing either array.
- **transfer to a new program** (applicability rule): Applicability: reason in terms of references whenever arrays are assigned, compared, printed or passed to methods. Reason in terms of elements when indexing.
- **diagnose an error** (error rule): rule broken: A reference must point to an array before it is indexed. Kind: run-time exception. Trigger class: an array variable holding null (e.g. an element of a String[][] row not yet created, or a field never assigned) is indexed (NullPointerException)

## Same topic

`array_reference` belongs to the topic **Memory representation and bounds checking** (`topic1.4.b`). The topic also contains: `array_aliasing`, `array_bounds`, `array_copy`, `loop_guard`, `primitive_vs_reference`, `printing_array_reference`, `program_state`.

## Rules of the concept (12)

- **folk-meaning rule:** Folk meaning: a variable is a box, so the array's values are 'inside' a. Java rule: the variable a holds only a reference (memory address, pointer) to the array object, which lives elsewhere.
- **uneven-application rule:** Points to LT: a[i] means fetch the address stored in a, add i, and access that memory location. Inconsistent application: the trace copies elements when a is assigned on one step but shares them on another.
- **identity rule:** Identity: an array reference, the value of an array variable; it is the memory address of the array, called a pointer.
- **declarative rule:** Declarative: a variable of array type holds a reference to an array object; operations on the name itself (assignment, ==, printing) act on that address.
- **operational sequencing rule:** Sequencing: for a[i], the address stored in a is read, the index i is added (scaled by the element size), and the memory at the resulting address is accessed: two elementary operations.
- **evaluation / result rule:** Result: the value of a is a reference (printed as hexadecimal). With the array at locations 523..530, a[4] is found at location 523 + 4 = 527.
- **state-transition rule:** State transition: assigning a reference (a = b, or a = new ...) changes only which array the variable points to; the arrays themselves are unchanged.
- **composition rule (with a neighbour):** with array\_creation: new reserves the memory and yields the array's address, which the array variable then stores.
- **plan / role rule:** Plan/role: the model that explains constant-time indexing, aliasing, reference equality and printing of arrays.
- **conservation rule:** Conservation: copying a reference keeps one shared array (changes through either name are seen by both); assigning a new reference breaks the link without changing either array.
- **error rule:** rule broken: A reference must point to an array before it is indexed. (run-time exception)
- **applicability rule:** Applicability: reason in terms of references whenever arrays are assigned, compared, printed or passed to methods. Reason in terms of elements when indexing.

## The whole prerequisite chain

- **Everything it builds on (4):** `array_creation`, `array_declaration`, `data_structure`, `data_type`
- **Everything that builds on it (3):** `array_aliasing`, `primitive_vs_reference`, `printing_array_reference`
