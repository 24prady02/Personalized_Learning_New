# primitive_vs_reference (`primitive_vs_reference`)

a primitive variable holds its value; an array (or String) variable holds a reference to the object stored elsewhere

Section 1.4 Arrays, topic 1.4.b Memory representation and bounds checking.

![The knowledge graph around primitive_vs_reference](primitive_vs_reference.png)

## At a glance

- **Needs first:** `array_reference`, `primitive_type`
- **Leads to:** nothing
- **Learned alongside:** nothing
- **Misconceptions:** `EqualityOperatorComparesObjectsValues`, `StringIsPrimitive`, `VariablesHoldObjects`
- **Errors:** none
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 23 edges around this concept. The edge logic, the wrong and right rules and the exact rules of the ways are copied word for word from the graph.

## To work on (2)

- misconceptions with no L0 way linked to them: EqualityOperatorComparesObjectsValues
- no aliases: a student's words cannot name this concept

## What it needs first (2)

A prerequisite edge means the other concept has to be understood before `primitive_vs_reference`.

### `array_reference` comes before `primitive_vs_reference`

*Array name holds a memory address: the array variable stores the memory address (pointer) of the array; a[i] is found by adding i to that address*

- **Edge:** `pre:array_reference->primitive_vs_reference`
- **Exact edge logic:** An array variable stores the memory address of the array, not its elements.
- **Grounding:** book\_passage
- **Composition rule (R) of `primitive_vs_reference` with `array_reference`:** An array variable is the standard example of a reference: its value is the memory address of the array.

### `primitive_type` comes before `primitive_vs_reference`

*int, double, boolean, char*

- **Edge:** `pre:primitive_type->primitive_vs_reference`
- **Exact edge logic:** A variable of a primitive type stores the value itself in its own memory.
- **Grounding:** book\_passage
- **Composition rule (R) of `primitive_vs_reference` with `primitive_type`:** The eight primitive types are the ones whose variables hold the value itself.

## What it leads to (0)

These concepts need `primitive_vs_reference` first.

No concept has this one as a prerequisite.

## Learned alongside (0)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

No parallel edge touches this concept.

## Misconceptions (3)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### EqualityOperatorComparesObjectsValues

- **Edge:** `primitive_vs_reference` &rarr; `EqualityOperatorComparesObjectsValues` (misconception)
- **Exact edge logic (the wrong rule):** == compares contents (the String == bug)
- **Twin logic (the right rule):** s == t is true only when s and t refer to the same object; s.equals(t) compares the text.
- **Wrong belief (on the node):** == compares contents (the String == bug)
- **Correct rule (on the node):** s == t is true only when s and t refer to the same object; s.equals(t) compares the text.
- **Provenance:** published
- **Role of this concept:** context
- **L0 way linked to it:** no
- **Edge `comparison_operators` &rarr; `EqualityOperatorComparesObjectsValues`, exact edge logic:** s == t is true whenever the two Strings contain the same text. **Twin logic:** s == t is true only when s and t refer to the same object; s.equals(t) compares the text. (role: primary)
- **Edge `string_type` &rarr; `EqualityOperatorComparesObjectsValues`, exact edge logic:** s == t is true whenever the two Strings contain the same text. **Twin logic:** s == t is true only when s and t refer to the same object; s.equals(t) compares the text. (role: context)

### StringIsPrimitive

- **Edge:** `primitive_vs_reference` &rarr; `StringIsPrimitive` (misconception)
- **Exact edge logic (the wrong rule):** String is a primitive type like int.
- **Twin logic (the right rule):** String is not a primitive type; it is a class whose values are objects, although Java gives it some built-in support (literals, +).
- **Wrong belief (on the node):** String is a primitive type like int.
- **Correct rule (on the node):** String is not a primitive type; it is a class whose values are objects, although Java gives it some built-in support (literals, +).
- **Provenance:** derived
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [3] misconception, exact rule:** wrong rule: String is a primitive type like int. Right rule: Java has eight primitive types; String is not one of them, and a String variable holds a reference.
- **Edge `primitive_type` &rarr; `StringIsPrimitive`, exact edge logic:** String is a primitive type like int. **Twin logic:** String is not a primitive type; it is a class whose values are objects, although Java gives it some built-in support (literals, +). (role: primary)
- **Edge `string_type` &rarr; `StringIsPrimitive`, exact edge logic:** String is a primitive type like int. **Twin logic:** String is not a primitive type; it is a class whose values are objects, although Java gives it some built-in support (literals, +). (role: context)

### VariablesHoldObjects

- **Edge:** `primitive_vs_reference` &rarr; `VariablesHoldObjects` (misconception)
- **Exact edge logic (the wrong rule):** a reference variable holds the whole object, not a reference
- **Twin logic (the right rule):** A reference variable holds only a reference to the object, which is stored separately.
- **Wrong belief (on the node):** a reference variable holds the whole object, not a reference
- **Correct rule (on the node):** A reference variable holds only a reference to the object, which is stored separately.
- **Provenance:** published
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [1] misconception, exact rule:** wrong rule: A reference variable holds the whole object, not a reference. Right rule: An array variable stores a reference (the memory address) to the array, not the elements.
- **L0 way [2] inconsistent\_trace, exact rule:** Applies the model unevenly: treats int x = y as copying a value (correct) but also treats b = a for arrays as copying all the elements. (here mixing in: "a reference variable holds the whole object, not a reference")
- **Edge `variable` &rarr; `VariablesHoldObjects`, exact edge logic:** A String or array variable contains the whole object inside it. **Twin logic:** A reference variable holds only a reference to the object, which is stored separately. (role: primary)

## Errors (0)

An error edge states the rule that gets broken in a program, and the right rule.

The graph has no error edge from this concept.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for primitive vs reference: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to primitive vs reference agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

- **Edge:** `primitive_vs_reference` &rarr; `primitive_vs_reference@L0` (has_level)
- **Exact edge logic:** primitive vs reference -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (4 ways).

Ways (4), each with its exact rule:

- **[0] everyday\_reading** (rule type E, folk-meaning rule): Everyday thinking pictures a variable as a box that holds the thing itself. That is true for int, double, char and boolean; an array variable holds only the address of the array, which is stored elsewhere.
- **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `VariablesHoldObjects`: wrong rule: A reference variable holds the whole object, not a reference. Right rule: An array variable stores a reference (the memory address) to the array, not the elements.
- **[2] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `VariablesHoldObjects`: Applies the model unevenly: treats int x = y as copying a value (correct) but also treats b = a for arrays as copying all the elements. (here mixing in: "a reference variable holds the whole object, not a reference")
- **[3] misconception** (rule type M, wrong rule / right rule) &rarr; `StringIsPrimitive`: wrong rule: String is a primitive type like int. Right rule: Java has eight primitive types; String is not one of them, and a String variable holds a reference.

### L1: Unistructural / atom x text surface

L1 for primitive vs reference: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

- **Edge:** `primitive_vs_reference` &rarr; `primitive_vs_reference@L1` (has_level)
- **Exact edge logic:** primitive vs reference -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

Ways (2), each with its exact rule:

- **[0] names\_the\_element** (rule type N, identity rule): Primitive versus reference variable: the first holds its value, the second holds the address of an object.
- **[1] states\_the\_rule** (rule type S, declarative rule): When you declare a variable of a primitive type, Java reserves memory that stores its value. An array variable stores a reference to the array: Java treats the array name as a variable whose value is the memory address of the array.

### L2: Multistructural / block x execution / preoperational

L2 for primitive vs reference: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

- **Edge:** `primitive_vs_reference` &rarr; `primitive_vs_reference@L2` (has_level)
- **Exact edge logic:** primitive vs reference -&gt; L2 (Multistructural): the answer applies the rules of primitive vs reference to every part of the code, in order (3 ways).

Ways (3), each with its exact rule:

- **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): Sequencing: x = y copies the value of y into x; b = a copies the address in a into b. In both cases the right side is evaluated first and its value stored, but the value of an array variable is an address.
- **[1] output\_prediction** (rule type OP, evaluation / result rule): Result: after int y = x; y++, x is unchanged; after int[] b = a; b[0]++, a[0] has changed too, because a and b refer to the same array.
- **[2] one\_step\_execution** (rule type OS, state-transition rule): State transition: assigning to a primitive variable changes only that variable; assigning to an element through a reference changes the array that every reference to it sees.

### L3: Relational / relations x function (concrete operational begins)

L3 for primitive vs reference: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

- **Edge:** `primitive_vs_reference` &rarr; `primitive_vs_reference@L3` (has_level)
- **Exact edge logic:** primitive vs reference -&gt; L3 (Relational): the answer relates the parts (3 ways).

Ways (3), each with its exact rule:

- **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): The eight primitive types are the ones whose variables hold the value itself.
- **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): An array variable is the standard example of a reference: its value is the memory address of the array.
- **[2] purpose\_of\_the\_whole** (rule type P, plan / role rule): Plan: the model predicts when an assignment shares data (arrays, Strings) and when it copies it (primitives), which decides when a copy is needed.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for primitive vs reference: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

- **Edge:** `primitive_vs_reference` &rarr; `primitive_vs_reference@L4` (has_level)
- **Exact edge logic:** primitive vs reference -&gt; L4 (Extended abstract): the answer reasons beyond the given code (3 ways).

Ways (3), each with its exact rule:

- **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `VariablesHoldObjects`: Conservation: changing a primitive copy never affects the original; changing an array through any reference affects every alias.
- **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Draw a memory diagram (value in a box for primitives, an arrow to the array for references) whenever code assigns or compares arrays.
- **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: == on references compares addresses. Kind: silent logic error. Trigger class: two arrays with the same elements are compared with == and found unequal (or two Strings with the same text)

## Same topic

`primitive_vs_reference` belongs to the topic **Memory representation and bounds checking** (`topic1.4.b`). The topic also contains: `array_aliasing`, `array_bounds`, `array_copy`, `array_reference`, `loop_guard`, `printing_array_reference`, `program_state`.

## Rules of the concept (15)

- **Book** (SW-1e, p. 97 (pdf 107)): "it just performs the standard operation as if the array name were a variable whose value is the memory address of the array."
- **Book** (TJ-2e, p. 147 (pdf 169)): "Not everything in Java is an object: int, double, char, and boolean are primitive types. When you declare a variable with a primitive type, Java reserves a small amount of memory to store its value."
- **Book** (TJ-2e, p. 148 (pdf 170)): "As you learned in Section 7.2, an array variable stores a reference to an array."
- **E** (folk-meaning rule): Everyday thinking pictures a variable as a box that holds the thing itself. That is true for int, double, char and boolean; an array variable holds only the address of the array, which is stored elsewhere.
- **M** (wrong rule / right rule): VariablesHoldObjects: wrong: A reference variable holds the whole object, not a reference. \| right: An array variable stores a reference (the memory address) to the array, not the elements.
- **M** (wrong rule / right rule): StringIsPrimitive: wrong: String is a primitive type like int. \| right: Java has eight primitive types; String is not one of them, and a String variable holds a reference.
- **T** (uneven-application rule): Applies the model unevenly: treats int x = y as copying a value (correct) but also treats b = a for arrays as copying all the elements.
- **N** (identity rule): Primitive versus reference variable: the first holds its value, the second holds the address of an object.
- **S** (declarative rule): When you declare a variable of a primitive type, Java reserves memory that stores its value. An array variable stores a reference to the array: Java treats the array name as a variable whose value is the memory address of the array.
- **LT** (operational sequencing rule): Sequencing: x = y copies the value of y into x; b = a copies the address in a into b. In both cases the right side is evaluated first and its value stored, but the value of an array variable is an address.
- **OP** (evaluation / result rule): Result: after int y = x; y++, x is unchanged; after int[] b = a; b[0]++, a[0] has changed too, because a and b refer to the same array.
- **OS** (state-transition rule): State transition: assigning to a primitive variable changes only that variable; assigning to an element through a reference changes the array that every reference to it sees.
- **R** (composition rule (with a neighbour)): with primitive\_type: The eight primitive types are the ones whose variables hold the value itself.
- **R** (composition rule (with a neighbour)): with array\_reference: An array variable is the standard example of a reference: its value is the memory address of the array.
- **P** (plan / role rule): Plan: the model predicts when an assignment shares data (arrays, Strings) and when it copies it (primitives), which decides when a copy is needed.
- **C** (conservation rule): Conservation: changing a primitive copy never affects the original; changing an array through any reference affects every alias.
- **D** (error rule): rule broken: == on references compares addresses. (silent logic error)
- **X** (applicability rule): Draw a memory diagram (value in a box for primitives, an arrow to the array for references) whenever code assigns or compares arrays.

## How it is found in code and answers (reader block)

- **Aliases:** none
- **Code patterns:** `(?:int|double|boolean|char|long|String|float|short|byte)\s*\[\]\s*\w+\s*=\s*[A-Za-z_]\w*\s*;`
- **Operator symbols:** none
- **Java types:** none
- **Signal array\_compared** (scope program): `(?:int|double|boolean|char|long|String|float|short|byte)\s*\[\]\s*(\w+)[\s\S]{0,2000}?\b\1\s*(?:==|!=)\s*\w+`

## The whole prerequisite chain

- **Everything it builds on (6):** `array_creation`, `array_declaration`, `array_reference`, `data_structure`, `data_type`, `primitive_type`
- **Everything that builds on it (0):** nothing

## Every edge in this view and its exact edge logic (23)

All the edges drawn in the picture, in the order: prerequisite, parallel, misconception, error, has_level, contains.

**1. `array_reference` &rarr; `primitive_vs_reference`** (prerequisite)

- **Exact edge logic:** An array variable stores the memory address of the array, not its elements.
- **Grounding:** book\_passage
- **Composition rule (R) of `primitive_vs_reference` with `array_reference`:** An array variable is the standard example of a reference: its value is the memory address of the array.

**2. `primitive_type` &rarr; `primitive_vs_reference`** (prerequisite)

- **Exact edge logic:** A variable of a primitive type stores the value itself in its own memory.
- **Grounding:** book\_passage
- **Composition rule (R) of `primitive_vs_reference` with `primitive_type`:** The eight primitive types are the ones whose variables hold the value itself.

**3. `primitive_vs_reference` &rarr; `EqualityOperatorComparesObjectsValues`** (misconception)

- **Exact edge logic (the wrong rule):** == compares contents (the String == bug)
- **Twin logic (the right rule):** s == t is true only when s and t refer to the same object; s.equals(t) compares the text.
- **Role:** context

**4. `primitive_vs_reference` &rarr; `StringIsPrimitive`** (misconception)

- **Exact edge logic (the wrong rule):** String is a primitive type like int.
- **Twin logic (the right rule):** String is not a primitive type; it is a class whose values are objects, although Java gives it some built-in support (literals, +).
- **Role:** context

**5. `primitive_vs_reference` &rarr; `VariablesHoldObjects`** (misconception)

- **Exact edge logic (the wrong rule):** a reference variable holds the whole object, not a reference
- **Twin logic (the right rule):** A reference variable holds only a reference to the object, which is stored separately.
- **Role:** context

**6. `comparison_operators` &rarr; `EqualityOperatorComparesObjectsValues`** (misconception)

- **Exact edge logic (the wrong rule):** s == t is true whenever the two Strings contain the same text.
- **Twin logic (the right rule):** s == t is true only when s and t refer to the same object; s.equals(t) compares the text.
- **Role:** primary

**7. `primitive_type` &rarr; `StringIsPrimitive`** (misconception)

- **Exact edge logic (the wrong rule):** String is a primitive type like int.
- **Twin logic (the right rule):** String is not a primitive type; it is a class whose values are objects, although Java gives it some built-in support (literals, +).
- **Role:** primary

**8. `string_type` &rarr; `EqualityOperatorComparesObjectsValues`** (misconception)

- **Exact edge logic (the wrong rule):** s == t is true whenever the two Strings contain the same text.
- **Twin logic (the right rule):** s == t is true only when s and t refer to the same object; s.equals(t) compares the text.
- **Role:** context

**9. `string_type` &rarr; `StringIsPrimitive`** (misconception)

- **Exact edge logic (the wrong rule):** String is a primitive type like int.
- **Twin logic (the right rule):** String is not a primitive type; it is a class whose values are objects, although Java gives it some built-in support (literals, +).
- **Role:** context

**10. `variable` &rarr; `VariablesHoldObjects`** (misconception)

- **Exact edge logic (the wrong rule):** A String or array variable contains the whole object inside it.
- **Twin logic (the right rule):** A reference variable holds only a reference to the object, which is stored separately.
- **Role:** primary

**11. `primitive_vs_reference` &rarr; `primitive_vs_reference@L0`** (has_level)

- **Exact edge logic:** primitive vs reference -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (4 ways).
  - **[0] everyday\_reading** (rule type E, folk-meaning rule): Everyday thinking pictures a variable as a box that holds the thing itself. That is true for int, double, char and boolean; an array variable holds only the address of the array, which is stored elsewhere.
  - **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `VariablesHoldObjects`: wrong rule: A reference variable holds the whole object, not a reference. Right rule: An array variable stores a reference (the memory address) to the array, not the elements.
  - **[2] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `VariablesHoldObjects`: Applies the model unevenly: treats int x = y as copying a value (correct) but also treats b = a for arrays as copying all the elements. (here mixing in: "a reference variable holds the whole object, not a reference")
  - **[3] misconception** (rule type M, wrong rule / right rule) &rarr; `StringIsPrimitive`: wrong rule: String is a primitive type like int. Right rule: Java has eight primitive types; String is not one of them, and a String variable holds a reference.

**12. `primitive_vs_reference` &rarr; `primitive_vs_reference@L1`** (has_level)

- **Exact edge logic:** primitive vs reference -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).
  - **[0] names\_the\_element** (rule type N, identity rule): Primitive versus reference variable: the first holds its value, the second holds the address of an object.
  - **[1] states\_the\_rule** (rule type S, declarative rule): When you declare a variable of a primitive type, Java reserves memory that stores its value. An array variable stores a reference to the array: Java treats the array name as a variable whose value is the memory address of the array.

**13. `primitive_vs_reference` &rarr; `primitive_vs_reference@L2`** (has_level)

- **Exact edge logic:** primitive vs reference -&gt; L2 (Multistructural): the answer applies the rules of primitive vs reference to every part of the code, in order (3 ways).
  - **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): Sequencing: x = y copies the value of y into x; b = a copies the address in a into b. In both cases the right side is evaluated first and its value stored, but the value of an array variable is an address.
  - **[1] output\_prediction** (rule type OP, evaluation / result rule): Result: after int y = x; y++, x is unchanged; after int[] b = a; b[0]++, a[0] has changed too, because a and b refer to the same array.
  - **[2] one\_step\_execution** (rule type OS, state-transition rule): State transition: assigning to a primitive variable changes only that variable; assigning to an element through a reference changes the array that every reference to it sees.

**14. `primitive_vs_reference` &rarr; `primitive_vs_reference@L3`** (has_level)

- **Exact edge logic:** primitive vs reference -&gt; L3 (Relational): the answer relates the parts (3 ways).
  - **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): The eight primitive types are the ones whose variables hold the value itself.
  - **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): An array variable is the standard example of a reference: its value is the memory address of the array.
  - **[2] purpose\_of\_the\_whole** (rule type P, plan / role rule): Plan: the model predicts when an assignment shares data (arrays, Strings) and when it copies it (primitives), which decides when a copy is needed.

**15. `primitive_vs_reference` &rarr; `primitive_vs_reference@L4`** (has_level)

- **Exact edge logic:** primitive vs reference -&gt; L4 (Extended abstract): the answer reasons beyond the given code (3 ways).
  - **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `VariablesHoldObjects`: Conservation: changing a primitive copy never affects the original; changing an array through any reference affects every alias.
  - **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Draw a memory diagram (value in a box for primitives, an arrow to the array for references) whenever code assigns or compares arrays.
  - **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: == on references compares addresses. Kind: silent logic error. Trigger class: two arrays with the same elements are compared with == and found unequal (or two Strings with the same text)

**16. `topic1.4.b` &rarr; `primitive_vs_reference`** (contains)

- topic `topic1.4.b` contains `primitive_vs_reference`

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

**22. `topic1.4.b` &rarr; `printing_array_reference`** (contains)

- topic `topic1.4.b` contains `printing_array_reference`

**23. `topic1.4.b` &rarr; `program_state`** (contains)

- topic `topic1.4.b` contains `program_state`
