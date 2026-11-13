# length_field (`length_field`)

a.length is a field, not a method

Section 1.4 Arrays, topic 1.4.a Arrays in Java (declare, create, initialize; indexing; length; default values).

![The knowledge graph around length_field](length_field.png)

## At a glance

- **Needs first:** `array_creation`, `array_initializer`
- **Leads to:** `args_length`, `array_reversal`, `array_traversal`
- **Learned alongside:** nothing
- **Misconceptions:** `ArrayHasLengthMethod`, `ArrayLengthCannotBeZero`
- **Errors:** none
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 22 edges around this concept, each explained in the graph's own words.

## What it needs first (2)

A prerequisite edge means the other concept has to be understood before `length_field`.

### `array_creation` comes before `length_field`

*new int[n] -- allocates n slots*

The size n given to new becomes a.length and stays fixed for the array's lifetime.

- **Grounding:** book passage
- **How `length_field` combines with `array_creation`:** The n given to new becomes a.length and stays fixed for that array object.
- **How `array_creation` combines with `length_field`:** The size n given to new becomes a.length and never changes for that array object.

### `array_initializer` comes before `length_field`

*{1, 2, 3} literal initialization*

An array made from a literal has as many elements as values listed, and a.length gives that number.

- **Grounding:** spec passage

## What it leads to (3)

These concepts need `length_field` first.

### `length_field` comes before `args_length`

*args.length gives the number of command-line arguments*

args is an ordinary String array, so args.length is its length field and counts the command-line arguments.

- **Grounding:** order only
- **How `length_field` combines with `args_length`:** args is an ordinary String[], so args.length is its length field and counts the command-line arguments (0 when none are typed).
- **How `args_length` combines with `length_field`:** args.length is the ordinary array length field applied to the String[] args.

### `length_field` comes before `array_reversal`

*reversing an array in place*

Reversal pairs a[i] with a[a.length-1-i], counting back from the last index a.length-1.

- **Grounding:** book passage

### `length_field` comes before `array_traversal`

*walking the array with an index loop*

A traversal loop runs its index from 0 while it is below a.length, so it visits every element once.

- **Grounding:** book passage

## Learned alongside (0)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

No parallel edge touches this concept.

## Misconceptions (2)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### ArrayHasLengthMethod

- **Wrong rule:** The size of an array is found by calling a.length().
- **Right rule:** An array's size is the field a.length, written without parentheses.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: You call length() instead of using the length field. Right rule: An array's size is the field a.length, written without parentheses; length() is a String method.
- **Shows at level L0 as:** inconsistent trace: Points to LT: a.length is read every time the loop test i &lt; a.length runs. Inconsistent application: the trace uses a.length as the last valid index on some passes (as if the test were &lt;=). (here mixing in: "you call length() instead of using the length field")
- **Also an edge from `method_call`:** you call length() instead of using the length field

### ArrayLengthCannotBeZero

- **Wrong rule:** An array cannot have length 0.
- **Right rule:** new int[0] is a legal array of length 0.
- **Role of this concept:** context
- **Shows at level L0 as:** misconception: wrong rule: An array cannot have length 0. Right rule: new int[0] is a legal array with length 0; args is such an array when no arguments are typed.
- **Also an edge from `array_creation`:** An array cannot have length 0.

## Errors (0)

An error edge states the rule that gets broken in a program, and the right rule.

The graph has no error edge from this concept.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for length field: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to length field agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

length field -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (4 ways).

- **everyday reading** (folk-meaning rule): Folk meaning: 'length' is something you ask for, like s.length() for a String, and in everyday counting 'length 10' suggests the last item is number 10. Java rule: a.length is a final field written without parentheses, equal to the number of elements, so the last index is a.length-1.
- **misconception** (wrong rule / right rule; shows `ArrayHasLengthMethod`): wrong rule: You call length() instead of using the length field. Right rule: An array's size is the field a.length, written without parentheses; length() is a String method.
- **inconsistent trace** (uneven-application rule; shows `ArrayHasLengthMethod`): Points to LT: a.length is read every time the loop test i &lt; a.length runs. Inconsistent application: the trace uses a.length as the last valid index on some passes (as if the test were &lt;=). (here mixing in: "you call length() instead of using the length field")
- **misconception** (wrong rule / right rule; shows `ArrayLengthCannotBeZero`): wrong rule: An array cannot have length 0. Right rule: new int[0] is a legal array with length 0; args is such an array when no arguments are typed.

### L1: Unistructural / atom x text surface

L1 for length field: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

length field -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

- **names the element** (identity rule): Identity: a.length is the public final instance field that every array has, holding its number of elements.
- **states the rule** (declarative rule): Declarative: the length of array a is written a.length (no parentheses); it equals the size given at creation, may be zero, cannot be assigned, and the last element is a[a.length-1].

### L2: Multistructural / block x execution / preoperational

L2 for length field: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

length field -&gt; L2 (Multistructural): the answer applies the rules of length field to every part of the code, in order (3 ways).

- **line by line trace** (operational sequencing rule): Sequencing: a is evaluated first (a null a throws NullPointerException), then the length field of the array a refers to now is read. In 'for (int i = 0; i &lt; a.length; i++)' it is re-read at each test.
- **output prediction** (evaluation / result rule): Result: an int &gt;= 0 equal to the number of elements: new double[8].length is 8, {1, 2, 3}.length is 3, and the last element is a[a.length-1].
- **one step execution** (state-transition rule): State transition: reading a.length changes nothing. Assigning 'a.length = 5' is impossible (a final field), so only making a refer to a different array changes the value later read as a.length.

### L3: Relational / relations x function (concrete operational begins)

L3 for length field: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

length field -&gt; L3 (Relational): the answer relates the parts (3 ways).

- **relation to neighbour** (composition rule (with a neighbour)): The n given to new becomes a.length and stays fixed for that array object.
- **relation to neighbour** (composition rule (with a neighbour)): args is an ordinary String[], so args.length is its length field and counts the command-line arguments (0 when none are typed).
- **purpose of the whole** (plan / role rule): Plan/role: a fixed value (Sajaniemi) that lets code adapt to any array size instead of a hard-coded magic number, e.g. loop bounds and the last element.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for length field: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

length field -&gt; L4 (Extended abstract): the answer reasons beyond the given code (5 ways).

- **predict a change** (conservation rule; shows `ArrayHasLengthMethod`): Conservation: for a given array object a.length never changes, so loops bounded by a.length stay correct when the array is created with a different size. Reassigning a to another array changes a.length.
- **transfer to a new program** (applicability rule): Applicability: use a.length wherever code must follow the array's real size (loop bounds, last element, copying); use a[i].length for each row of a possibly ragged 2-D array; use s.length() for Strings.
- **diagnose an error** (error rule): rule broken: length is a field, not a method. Kind: compile-time. Trigger class: a.length() is written for an array (cannot find symbol: method length())
- **diagnose an error** (error rule): rule broken: length is final and cannot be assigned. Kind: compile-time. Trigger class: 'a.length = n;' (cannot assign a value to final variable length)
- **diagnose an error** (error rule): rule broken: The last valid index is a.length-1. Kind: run-time exception. Trigger class: a[a.length] or a loop with i &lt;= a.length (ArrayIndexOutOfBoundsException)

## Same topic

`length_field` belongs to the topic **Arrays in Java (declare, create, initialize; indexing; length; default values)** (`topic1.4.a`). The topic also contains: `args_length`, `array_creation`, `array_declaration`, `array_default_values`, `data_structure`, `indexing`, `off_by_one_error`.

## Rules of the concept (17)

- **folk-meaning rule:** Folk meaning: 'length' is something you ask for, like s.length() for a String, and in everyday counting 'length 10' suggests the last item is number 10. Java rule: a.length is a final field written without parentheses, equal to the number of elements, so the last index is a.length-1.
- **wrong rule / right rule:** ArrayHasLengthMethod: wrong: You call length() instead of using the length field. \| right: An array's size is the field a.length, written without parentheses; length() is a String method.
- **wrong rule / right rule:** ArrayLengthCannotBeZero: wrong: An array cannot have length 0. \| right: new int[0] is a legal array with length 0; args is such an array when no arguments are typed.
- **uneven-application rule:** Points to LT: a.length is read every time the loop test i &lt; a.length runs. Inconsistent application: the trace uses a.length as the last valid index on some passes (as if the test were &lt;=).
- **identity rule:** Identity: a.length is the public final instance field that every array has, holding its number of elements.
- **declarative rule:** Declarative: the length of array a is written a.length (no parentheses); it equals the size given at creation, may be zero, cannot be assigned, and the last element is a[a.length-1].
- **operational sequencing rule:** Sequencing: a is evaluated first (a null a throws NullPointerException), then the length field of the array a refers to now is read. In 'for (int i = 0; i &lt; a.length; i++)' it is re-read at each test.
- **evaluation / result rule:** Result: an int &gt;= 0 equal to the number of elements: new double[8].length is 8, {1, 2, 3}.length is 3, and the last element is a[a.length-1].
- **state-transition rule:** State transition: reading a.length changes nothing. Assigning 'a.length = 5' is impossible (a final field), so only making a refer to a different array changes the value later read as a.length.
- **composition rule (with a neighbour):** with array\_creation: The n given to new becomes a.length and stays fixed for that array object.
- **composition rule (with a neighbour):** with args\_length: args is an ordinary String[], so args.length is its length field and counts the command-line arguments (0 when none are typed).
- **plan / role rule:** Plan/role: a fixed value (Sajaniemi) that lets code adapt to any array size instead of a hard-coded magic number, e.g. loop bounds and the last element.
- **conservation rule:** Conservation: for a given array object a.length never changes, so loops bounded by a.length stay correct when the array is created with a different size. Reassigning a to another array changes a.length.
- **error rule:** rule broken: length is a field, not a method. (compile-time)
- **error rule:** rule broken: length is final and cannot be assigned. (compile-time)
- **error rule:** rule broken: The last valid index is a.length-1. (run-time exception)
- **applicability rule:** Applicability: use a.length wherever code must follow the array's real size (loop bounds, last element, copying); use a[i].length for each row of a possibly ragged 2-D array; use s.length() for Strings.

## The whole prerequisite chain

- **Everything it builds on (5):** `array_creation`, `array_declaration`, `array_initializer`, `data_structure`, `data_type`
- **Everything that builds on it (9):** `args_length`, `array_copy`, `array_reversal`, `array_traversal`, `boolean_flag_array`, `enhanced_for`, `function_plotting`, `running_extreme`, `standard_audio`
