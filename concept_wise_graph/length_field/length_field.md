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

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 22 edges around this concept. The edge logic, the wrong and right rules and the exact rules of the ways are copied word for word from the graph.

## To work on (0)

Nothing is missing for this concept.

## What it needs first (2)

A prerequisite edge means the other concept has to be understood before `length_field`.

### `array_creation` comes before `length_field`

*new int[n] -- allocates n slots*

- **Edge:** `pre:array_creation->length_field`
- **Exact edge logic:** The size n given to new becomes a.length and stays fixed for the array's lifetime.
- **Grounding:** book\_passage
- **Composition rule (R) of `length_field` with `array_creation`:** The n given to new becomes a.length and stays fixed for that array object.
- **Composition rule (R) of `array_creation` with `length_field`:** The size n given to new becomes a.length and never changes for that array object.

### `array_initializer` comes before `length_field`

*{1, 2, 3} literal initialization*

- **Edge:** `pre:array_initializer->length_field`
- **Exact edge logic:** An array made from a literal has as many elements as values listed, and a.length gives that number.
- **Grounding:** spec\_passage

## What it leads to (3)

These concepts need `length_field` first.

### `length_field` comes before `args_length`

*args.length gives the number of command-line arguments*

- **Edge:** `pre:length_field->args_length`
- **Exact edge logic:** args is an ordinary String array, so args.length is its length field and counts the command-line arguments.
- **Grounding:** order\_only
- **Composition rule (R) of `length_field` with `args_length`:** args is an ordinary String[], so args.length is its length field and counts the command-line arguments (0 when none are typed).
- **Composition rule (R) of `args_length` with `length_field`:** args.length is the ordinary array length field applied to the String[] args.

### `length_field` comes before `array_reversal`

*reversing an array in place*

- **Edge:** `pre:length_field->array_reversal`
- **Exact edge logic:** Reversal pairs a[i] with a[a.length-1-i], counting back from the last index a.length-1.
- **Grounding:** book\_passage

### `length_field` comes before `array_traversal`

*walking the array with an index loop*

- **Edge:** `pre:length_field->array_traversal`
- **Exact edge logic:** A traversal loop runs its index from 0 while it is below a.length, so it visits every element once.
- **Grounding:** book\_passage

## Learned alongside (0)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

No parallel edge touches this concept.

## Misconceptions (2)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### ArrayHasLengthMethod

- **Edge:** `length_field` &rarr; `ArrayHasLengthMethod` (misconception)
- **Exact edge logic (the wrong rule):** The size of an array is found by calling a.length().
- **Twin logic (the right rule):** An array's size is the field a.length, written without parentheses.
- **Wrong belief (on the node):** you call length() instead of using the length field
- **Correct rule (on the node):** An array's size is the field a.length, written without parentheses.
- **Provenance:** published
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [1] misconception, exact rule:** wrong rule: You call length() instead of using the length field. Right rule: An array's size is the field a.length, written without parentheses; length() is a String method.
- **L0 way [2] inconsistent\_trace, exact rule:** Points to LT: a.length is read every time the loop test i &lt; a.length runs. Inconsistent application: the trace uses a.length as the last valid index on some passes (as if the test were &lt;=). (here mixing in: "you call length() instead of using the length field")
- **Edge `method_call` &rarr; `ArrayHasLengthMethod`, exact edge logic:** you call length() instead of using the length field **Twin logic:** An array's size is the field a.length, written without parentheses. (role: context)

### ArrayLengthCannotBeZero

- **Edge:** `length_field` &rarr; `ArrayLengthCannotBeZero` (misconception)
- **Exact edge logic (the wrong rule):** An array cannot have length 0.
- **Twin logic (the right rule):** new int[0] is a legal array of length 0.
- **Wrong belief (on the node):** An array cannot have length 0.
- **Correct rule (on the node):** new int[0] is a legal array of length 0.
- **Provenance:** published
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [3] misconception, exact rule:** wrong rule: An array cannot have length 0. Right rule: new int[0] is a legal array with length 0; args is such an array when no arguments are typed.
- **Edge `array_creation` &rarr; `ArrayLengthCannotBeZero`, exact edge logic:** An array cannot have length 0. **Twin logic:** new int[0] is a legal array of length 0. (role: primary)

## Errors (0)

An error edge states the rule that gets broken in a program, and the right rule.

The graph has no error edge from this concept.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for length field: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to length field agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

- **Edge:** `length_field` &rarr; `length_field@L0` (has_level)
- **Exact edge logic:** length field -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (4 ways).

Ways (4), each with its exact rule:

- **[0] everyday\_reading** (rule type E, folk-meaning rule): Folk meaning: 'length' is something you ask for, like s.length() for a String, and in everyday counting 'length 10' suggests the last item is number 10. Java rule: a.length is a final field written without parentheses, equal to the number of elements, so the last index is a.length-1.
- **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `ArrayHasLengthMethod`: wrong rule: You call length() instead of using the length field. Right rule: An array's size is the field a.length, written without parentheses; length() is a String method.
- **[2] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `ArrayHasLengthMethod`: Points to LT: a.length is read every time the loop test i &lt; a.length runs. Inconsistent application: the trace uses a.length as the last valid index on some passes (as if the test were &lt;=). (here mixing in: "you call length() instead of using the length field")
- **[3] misconception** (rule type M, wrong rule / right rule) &rarr; `ArrayLengthCannotBeZero`: wrong rule: An array cannot have length 0. Right rule: new int[0] is a legal array with length 0; args is such an array when no arguments are typed.

### L1: Unistructural / atom x text surface

L1 for length field: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

- **Edge:** `length_field` &rarr; `length_field@L1` (has_level)
- **Exact edge logic:** length field -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

Ways (2), each with its exact rule:

- **[0] names\_the\_element** (rule type N, identity rule): Identity: a.length is the public final instance field that every array has, holding its number of elements.
- **[1] states\_the\_rule** (rule type S, declarative rule): Declarative: the length of array a is written a.length (no parentheses); it equals the size given at creation, may be zero, cannot be assigned, and the last element is a[a.length-1].

### L2: Multistructural / block x execution / preoperational

L2 for length field: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

- **Edge:** `length_field` &rarr; `length_field@L2` (has_level)
- **Exact edge logic:** length field -&gt; L2 (Multistructural): the answer applies the rules of length field to every part of the code, in order (3 ways).

Ways (3), each with its exact rule:

- **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): Sequencing: a is evaluated first (a null a throws NullPointerException), then the length field of the array a refers to now is read. In 'for (int i = 0; i &lt; a.length; i++)' it is re-read at each test.
- **[1] output\_prediction** (rule type OP, evaluation / result rule): Result: an int &gt;= 0 equal to the number of elements: new double[8].length is 8, {1, 2, 3}.length is 3, and the last element is a[a.length-1].
- **[2] one\_step\_execution** (rule type OS, state-transition rule): State transition: reading a.length changes nothing. Assigning 'a.length = 5' is impossible (a final field), so only making a refer to a different array changes the value later read as a.length.

### L3: Relational / relations x function (concrete operational begins)

L3 for length field: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

- **Edge:** `length_field` &rarr; `length_field@L3` (has_level)
- **Exact edge logic:** length field -&gt; L3 (Relational): the answer relates the parts (3 ways).

Ways (3), each with its exact rule:

- **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): The n given to new becomes a.length and stays fixed for that array object.
- **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): args is an ordinary String[], so args.length is its length field and counts the command-line arguments (0 when none are typed).
- **[2] purpose\_of\_the\_whole** (rule type P, plan / role rule): Plan/role: a fixed value (Sajaniemi) that lets code adapt to any array size instead of a hard-coded magic number, e.g. loop bounds and the last element.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for length field: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

- **Edge:** `length_field` &rarr; `length_field@L4` (has_level)
- **Exact edge logic:** length field -&gt; L4 (Extended abstract): the answer reasons beyond the given code (5 ways).

Ways (5), each with its exact rule:

- **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `ArrayHasLengthMethod`: Conservation: for a given array object a.length never changes, so loops bounded by a.length stay correct when the array is created with a different size. Reassigning a to another array changes a.length.
- **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Applicability: use a.length wherever code must follow the array's real size (loop bounds, last element, copying); use a[i].length for each row of a possibly ragged 2-D array; use s.length() for Strings.
- **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: length is a field, not a method. Kind: compile-time. Trigger class: a.length() is written for an array (cannot find symbol: method length())
- **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: length is final and cannot be assigned. Kind: compile-time. Trigger class: 'a.length = n;' (cannot assign a value to final variable length)
- **[4] diagnose\_an\_error** (rule type D, error rule): rule broken: The last valid index is a.length-1. Kind: run-time exception. Trigger class: a[a.length] or a loop with i &lt;= a.length (ArrayIndexOutOfBoundsException)

## Same topic

`length_field` belongs to the topic **Arrays in Java (declare, create, initialize; indexing; length; default values)** (`topic1.4.a`). The topic also contains: `args_length`, `array_creation`, `array_declaration`, `array_default_values`, `data_structure`, `indexing`, `off_by_one_error`.

## Rules of the concept (17)

- **Book** (SW-1e, p. 89 (pdf 99)): "Java's standard mechanism is to allow a program to refer to the length of an array a[] with the code a.length"
- **Book** (OT-Arrays, ): "Finally, you can use the built-in length property to determine the size of any array."
- **Book** (SW-1.4, ): "You can refer to the length of an a[] in your program with the code a.length."
- **E** (folk-meaning rule): Folk meaning: 'length' is something you ask for, like s.length() for a String, and in everyday counting 'length 10' suggests the last item is number 10. Java rule: a.length is a final field written without parentheses, equal to the number of elements, so the last index is a.length-1.
- **M** (wrong rule / right rule): ArrayHasLengthMethod: wrong: You call length() instead of using the length field. \| right: An array's size is the field a.length, written without parentheses; length() is a String method.
- **M** (wrong rule / right rule): ArrayLengthCannotBeZero: wrong: An array cannot have length 0. \| right: new int[0] is a legal array with length 0; args is such an array when no arguments are typed.
- **T** (uneven-application rule): Points to LT: a.length is read every time the loop test i &lt; a.length runs. Inconsistent application: the trace uses a.length as the last valid index on some passes (as if the test were &lt;=).
- **N** (identity rule): Identity: a.length is the public final instance field that every array has, holding its number of elements.
- **S** (declarative rule): Declarative: the length of array a is written a.length (no parentheses); it equals the size given at creation, may be zero, cannot be assigned, and the last element is a[a.length-1].
- **LT** (operational sequencing rule): Sequencing: a is evaluated first (a null a throws NullPointerException), then the length field of the array a refers to now is read. In 'for (int i = 0; i &lt; a.length; i++)' it is re-read at each test.
- **OP** (evaluation / result rule): Result: an int &gt;= 0 equal to the number of elements: new double[8].length is 8, {1, 2, 3}.length is 3, and the last element is a[a.length-1].
- **OS** (state-transition rule): State transition: reading a.length changes nothing. Assigning 'a.length = 5' is impossible (a final field), so only making a refer to a different array changes the value later read as a.length.
- **R** (composition rule (with a neighbour)): with array\_creation: The n given to new becomes a.length and stays fixed for that array object.
- **R** (composition rule (with a neighbour)): with args\_length: args is an ordinary String[], so args.length is its length field and counts the command-line arguments (0 when none are typed).
- **P** (plan / role rule): Plan/role: a fixed value (Sajaniemi) that lets code adapt to any array size instead of a hard-coded magic number, e.g. loop bounds and the last element.
- **C** (conservation rule): Conservation: for a given array object a.length never changes, so loops bounded by a.length stay correct when the array is created with a different size. Reassigning a to another array changes a.length.
- **D** (error rule): rule broken: length is a field, not a method. (compile-time)
- **D** (error rule): rule broken: length is final and cannot be assigned. (compile-time)
- **D** (error rule): rule broken: The last valid index is a.length-1. (run-time exception)
- **X** (applicability rule): Applicability: use a.length wherever code must follow the array's real size (loop bounds, last element, copying); use a[i].length for each row of a possibly ragged 2-D array; use s.length() for Strings.

## How it is found in code and answers (reader block)

- **Aliases:** length, .length
- **Code patterns:** `\.length\b(?!\s*\()`
- **Operator symbols:** none
- **Java types:** none
- **Signal array\_length\_called\_as\_method** (scope program, decisive): `(?:\]\s*(\w+)\s*(?:=|;|,)|\b(\w+)\s*\[\s*\]\s*=)[\s\S]{0,4000}?\b(?:\1|\2)\s*\.\s*length\s*\(\s*\)`

## The whole prerequisite chain

- **Everything it builds on (5):** `array_creation`, `array_declaration`, `array_initializer`, `data_structure`, `data_type`
- **Everything that builds on it (9):** `args_length`, `array_copy`, `array_reversal`, `array_traversal`, `boolean_flag_array`, `enhanced_for`, `function_plotting`, `running_extreme`, `standard_audio`

## Every edge in this view and its exact edge logic (22)

All the edges drawn in the picture, in the order: prerequisite, parallel, misconception, error, has_level, contains.

**1. `array_creation` &rarr; `length_field`** (prerequisite)

- **Exact edge logic:** The size n given to new becomes a.length and stays fixed for the array's lifetime.
- **Grounding:** book\_passage
- **Composition rule (R) of `array_creation` with `length_field`:** The size n given to new becomes a.length and never changes for that array object.
- **Composition rule (R) of `length_field` with `array_creation`:** The n given to new becomes a.length and stays fixed for that array object.

**2. `array_initializer` &rarr; `length_field`** (prerequisite)

- **Exact edge logic:** An array made from a literal has as many elements as values listed, and a.length gives that number.
- **Grounding:** spec\_passage

**3. `length_field` &rarr; `args_length`** (prerequisite)

- **Exact edge logic:** args is an ordinary String array, so args.length is its length field and counts the command-line arguments.
- **Grounding:** order\_only
- **Composition rule (R) of `length_field` with `args_length`:** args is an ordinary String[], so args.length is its length field and counts the command-line arguments (0 when none are typed).
- **Composition rule (R) of `args_length` with `length_field`:** args.length is the ordinary array length field applied to the String[] args.

**4. `length_field` &rarr; `array_reversal`** (prerequisite)

- **Exact edge logic:** Reversal pairs a[i] with a[a.length-1-i], counting back from the last index a.length-1.
- **Grounding:** book\_passage

**5. `length_field` &rarr; `array_traversal`** (prerequisite)

- **Exact edge logic:** A traversal loop runs its index from 0 while it is below a.length, so it visits every element once.
- **Grounding:** book\_passage

**6. `length_field` &rarr; `ArrayHasLengthMethod`** (misconception)

- **Exact edge logic (the wrong rule):** The size of an array is found by calling a.length().
- **Twin logic (the right rule):** An array's size is the field a.length, written without parentheses.
- **Role:** primary

**7. `length_field` &rarr; `ArrayLengthCannotBeZero`** (misconception)

- **Exact edge logic (the wrong rule):** An array cannot have length 0.
- **Twin logic (the right rule):** new int[0] is a legal array of length 0.
- **Role:** context

**8. `array_creation` &rarr; `ArrayLengthCannotBeZero`** (misconception)

- **Exact edge logic (the wrong rule):** An array cannot have length 0.
- **Twin logic (the right rule):** new int[0] is a legal array of length 0.
- **Role:** primary

**9. `method_call` &rarr; `ArrayHasLengthMethod`** (misconception)

- **Exact edge logic (the wrong rule):** you call length() instead of using the length field
- **Twin logic (the right rule):** An array's size is the field a.length, written without parentheses.
- **Role:** context

**10. `length_field` &rarr; `length_field@L0`** (has_level)

- **Exact edge logic:** length field -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (4 ways).
  - **[0] everyday\_reading** (rule type E, folk-meaning rule): Folk meaning: 'length' is something you ask for, like s.length() for a String, and in everyday counting 'length 10' suggests the last item is number 10. Java rule: a.length is a final field written without parentheses, equal to the number of elements, so the last index is a.length-1.
  - **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `ArrayHasLengthMethod`: wrong rule: You call length() instead of using the length field. Right rule: An array's size is the field a.length, written without parentheses; length() is a String method.
  - **[2] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `ArrayHasLengthMethod`: Points to LT: a.length is read every time the loop test i &lt; a.length runs. Inconsistent application: the trace uses a.length as the last valid index on some passes (as if the test were &lt;=). (here mixing in: "you call length() instead of using the length field")
  - **[3] misconception** (rule type M, wrong rule / right rule) &rarr; `ArrayLengthCannotBeZero`: wrong rule: An array cannot have length 0. Right rule: new int[0] is a legal array with length 0; args is such an array when no arguments are typed.

**11. `length_field` &rarr; `length_field@L1`** (has_level)

- **Exact edge logic:** length field -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).
  - **[0] names\_the\_element** (rule type N, identity rule): Identity: a.length is the public final instance field that every array has, holding its number of elements.
  - **[1] states\_the\_rule** (rule type S, declarative rule): Declarative: the length of array a is written a.length (no parentheses); it equals the size given at creation, may be zero, cannot be assigned, and the last element is a[a.length-1].

**12. `length_field` &rarr; `length_field@L2`** (has_level)

- **Exact edge logic:** length field -&gt; L2 (Multistructural): the answer applies the rules of length field to every part of the code, in order (3 ways).
  - **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): Sequencing: a is evaluated first (a null a throws NullPointerException), then the length field of the array a refers to now is read. In 'for (int i = 0; i &lt; a.length; i++)' it is re-read at each test.
  - **[1] output\_prediction** (rule type OP, evaluation / result rule): Result: an int &gt;= 0 equal to the number of elements: new double[8].length is 8, {1, 2, 3}.length is 3, and the last element is a[a.length-1].
  - **[2] one\_step\_execution** (rule type OS, state-transition rule): State transition: reading a.length changes nothing. Assigning 'a.length = 5' is impossible (a final field), so only making a refer to a different array changes the value later read as a.length.

**13. `length_field` &rarr; `length_field@L3`** (has_level)

- **Exact edge logic:** length field -&gt; L3 (Relational): the answer relates the parts (3 ways).
  - **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): The n given to new becomes a.length and stays fixed for that array object.
  - **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): args is an ordinary String[], so args.length is its length field and counts the command-line arguments (0 when none are typed).
  - **[2] purpose\_of\_the\_whole** (rule type P, plan / role rule): Plan/role: a fixed value (Sajaniemi) that lets code adapt to any array size instead of a hard-coded magic number, e.g. loop bounds and the last element.

**14. `length_field` &rarr; `length_field@L4`** (has_level)

- **Exact edge logic:** length field -&gt; L4 (Extended abstract): the answer reasons beyond the given code (5 ways).
  - **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `ArrayHasLengthMethod`: Conservation: for a given array object a.length never changes, so loops bounded by a.length stay correct when the array is created with a different size. Reassigning a to another array changes a.length.
  - **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Applicability: use a.length wherever code must follow the array's real size (loop bounds, last element, copying); use a[i].length for each row of a possibly ragged 2-D array; use s.length() for Strings.
  - **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: length is a field, not a method. Kind: compile-time. Trigger class: a.length() is written for an array (cannot find symbol: method length())
  - **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: length is final and cannot be assigned. Kind: compile-time. Trigger class: 'a.length = n;' (cannot assign a value to final variable length)
  - **[4] diagnose\_an\_error** (rule type D, error rule): rule broken: The last valid index is a.length-1. Kind: run-time exception. Trigger class: a[a.length] or a loop with i &lt;= a.length (ArrayIndexOutOfBoundsException)

**15. `topic1.4.a` &rarr; `length_field`** (contains)

- topic `topic1.4.a` contains `length_field`

**16. `topic1.4.a` &rarr; `args_length`** (contains)

- topic `topic1.4.a` contains `args_length`

**17. `topic1.4.a` &rarr; `array_creation`** (contains)

- topic `topic1.4.a` contains `array_creation`

**18. `topic1.4.a` &rarr; `array_declaration`** (contains)

- topic `topic1.4.a` contains `array_declaration`

**19. `topic1.4.a` &rarr; `array_default_values`** (contains)

- topic `topic1.4.a` contains `array_default_values`

**20. `topic1.4.a` &rarr; `data_structure`** (contains)

- topic `topic1.4.a` contains `data_structure`

**21. `topic1.4.a` &rarr; `indexing`** (contains)

- topic `topic1.4.a` contains `indexing`

**22. `topic1.4.a` &rarr; `off_by_one_error`** (contains)

- topic `topic1.4.a` contains `off_by_one_error`
