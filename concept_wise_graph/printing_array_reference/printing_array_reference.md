# printing_array_reference (`printing_array_reference`)

printing an array variable prints a reference, not the elements

Section 1.4 Arrays, topic 1.4.b Memory representation and bounds checking.

![The knowledge graph around printing_array_reference](printing_array_reference.png)

## At a glance

- **Needs first:** `array_reference`, `println`
- **Leads to:** nothing
- **Learned alongside:** `array_aliasing`
- **Misconceptions:** `ArrayPrintsContents`
- **Errors:** none
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 17 edges around this concept. The edge logic, the wrong and right rules and the exact rules of the ways are copied word for word from the graph.

## To work on (0)

Nothing is missing for this concept.

## What it needs first (2)

A prerequisite edge means the other concept has to be understood before `printing_array_reference`.

### `array_reference` comes before `printing_array_reference`

*Array name holds a memory address: the array variable stores the memory address (pointer) of the array; a[i] is found by adding i to that address*

- **Edge:** `pre:array_reference->printing_array_reference`
- **Exact edge logic:** Printing an array variable prints the reference it holds, not the elements.
- **Grounding:** book\_passage

### `println` comes before `printing_array_reference`

*System.out.println -- output with a trailing newline*

- **Edge:** `pre:println->printing_array_reference`
- **Exact edge logic:** println of an array variable prints the array's reference, not its elements.
- **Grounding:** book\_passage

## What it leads to (0)

These concepts need `printing_array_reference` first.

No concept has this one as a prerequisite.

## Learned alongside (1)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

### `printing_array_reference` alongside `array_aliasing`

*two variables can refer to the same array*

- **Edge:** `par:array_aliasing~printing_array_reference`
- **Exact edge logic:** Both follow from the array variable holding a reference (memory address): assignment and == act on that reference, and println(a) prints it.
- **Grounding:** questionable
- **Composition rule (R) of `printing_array_reference` with `array_aliasing`:** Two aliases print the same text, and two separately created arrays with equal contents print different text, because println shows the reference that assignment and == also act on.
- **Composition rule (R) of `array_aliasing` with `printing_array_reference`:** Assignment, == and println(a) all act on the reference value: two aliases print the same address, while two equal-content arrays print different ones.

## Misconceptions (1)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### ArrayPrintsContents

- **Edge:** `printing_array_reference` &rarr; `ArrayPrintsContents` (misconception)
- **Exact edge logic (the wrong rule):** System.out.println(a) prints the elements of the array a.
- **Twin logic (the right rule):** Printing an array variable prints its memory address (a hexadecimal integer like @f62373), not its elements.
- **Wrong belief (on the node):** System.out.println(a) prints the elements of the array a.
- **Correct rule (on the node):** Printing an array variable prints its memory address (a hexadecimal integer like @f62373), not its elements.
- **Provenance:** textbook
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [1] misconception, exact rule:** wrong rule: System.out.println(a) prints the elements of the array a. Right rule: Printing an array variable prints its memory address (a hexadecimal integer like @f62373), not its elements.
- **L0 way [2] inconsistent\_trace, exact rule:** Points to LT: println(a) converts the one reference value to a String; no traversal happens. Inconsistent application: the trace prints the elements for one println(a) but an address for another. (here mixing in: "System.out.println(a) prints the elements of the array a")

## Errors (0)

An error edge states the rule that gets broken in a program, and the right rule.

The graph has no error edge from this concept.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for printing array reference: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to printing array reference agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

- **Edge:** `printing_array_reference` &rarr; `printing_array_reference@L0` (has_level)
- **Exact edge logic:** printing array reference -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (3 ways).

Ways (3), each with its exact rule:

- **[0] everyday\_reading** (rule type E, folk-meaning rule): Folk meaning: 'print a' should show what is in a, as when you print a list on paper. Java rule: System.out.println(a) converts the reference to text such as [I@bf3f7e0 (type code plus hexadecimal hash/address) and never reads the elements.
- **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `ArrayPrintsContents`: wrong rule: System.out.println(a) prints the elements of the array a. Right rule: Printing an array variable prints its memory address (a hexadecimal integer like @f62373), not its elements.
- **[2] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `ArrayPrintsContents`: Points to LT: println(a) converts the one reference value to a String; no traversal happens. Inconsistent application: the trace prints the elements for one println(a) but an address for another. (here mixing in: "System.out.println(a) prints the elements of the array a")

### L1: Unistructural / atom x text surface

L1 for printing array reference: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

- **Edge:** `printing_array_reference` &rarr; `printing_array_reference@L1` (has_level)
- **Exact edge logic:** printing array reference -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

Ways (2), each with its exact rule:

- **[0] names\_the\_element** (rule type N, identity rule): Identity: printing an array variable outputs the text form of its reference ([I@..., [D@...), not a listing of the elements.
- **[1] states\_the\_rule** (rule type S, declarative rule): Declarative: any value, including an array reference, is converted to a String when printed or concatenated; for an array this string is its type code and address.

### L2: Multistructural / block x execution / preoperational

L2 for printing array reference: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

- **Edge:** `printing_array_reference` &rarr; `printing_array_reference@L2` (has_level)
- **Exact edge logic:** printing array reference -&gt; L2 (Multistructural): the answer applies the rules of printing array reference to every part of the code, in order (3 ways).

Ways (3), each with its exact rule:

- **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): Sequencing: the argument a is evaluated to a reference, string conversion turns it into text, and println writes that text and a newline. The elements are never read.
- **[1] output\_prediction** (rule type OP, evaluation / result rule): Result: one line such as [I@bf3f7e0 for an int[] ([D@... for double[]); the hex part changes from run to run. Exception: println(char[]) has its own overload and prints the characters.
- **[2] one\_step\_execution** (rule type OS, state-transition rule): State transition: no variable or element changes; only one line of output is produced.

### L3: Relational / relations x function (concrete operational begins)

L3 for printing array reference: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

- **Edge:** `printing_array_reference` &rarr; `printing_array_reference@L3` (has_level)
- **Exact edge logic:** printing array reference -&gt; L3 (Relational): the answer relates the parts (2 ways).

Ways (2), each with its exact rule:

- **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Two aliases print the same text, and two separately created arrays with equal contents print different text, because println shows the reference that assignment and == also act on.
- **[1] purpose\_of\_the\_whole** (rule type P, plan / role rule): Plan/role: useful only as a diagnostic of identity (do two names hold the same reference?). To show the contents, traverse and print each a[i], or print Arrays.toString(a).

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for printing array reference: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

- **Edge:** `printing_array_reference` &rarr; `printing_array_reference@L4` (has_level)
- **Exact edge logic:** printing array reference -&gt; L4 (Extended abstract): the answer reasons beyond the given code (3 ways).

Ways (3), each with its exact rule:

- **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `ArrayPrintsContents`: Conservation: changing the elements does not change what println(a) prints (the same array keeps its reference). Replacing println(a) by a loop or Arrays.toString(a) changes the output to the elements.
- **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Applicability: print a reference only when debugging whether two names share an array. For output of values use an element loop (one per line or formatted) or Arrays.toString.
- **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: println of an array reference prints the reference, not the elements. Kind: silent logic error. Trigger class: an array variable (not an element) is passed to print/println or concatenated, as in "a = " + a, expecting the values

## Same topic

`printing_array_reference` belongs to the topic **Memory representation and bounds checking** (`topic1.4.b`). The topic also contains: `array_aliasing`, `array_bounds`, `array_copy`, `array_reference`, `loop_guard`, `primitive_vs_reference`, `program_state`.

## Rules of the concept (13)

- **Book** (SW-1e, p. 112 (pdf 122)): "If a[] is an array, why does System.out.println(a) print out a hexadecimal integer"
- **Book** (SW-1.4, ): "a = [D@f62373"
- **E** (folk-meaning rule): Folk meaning: 'print a' should show what is in a, as when you print a list on paper. Java rule: System.out.println(a) converts the reference to text such as [I@bf3f7e0 (type code plus hexadecimal hash/address) and never reads the elements.
- **M** (wrong rule / right rule): ArrayPrintsContents: wrong: System.out.println(a) prints the elements of the array a. \| right: Printing an array variable prints its memory address (a hexadecimal integer like @f62373), not its elements.
- **T** (uneven-application rule): Points to LT: println(a) converts the one reference value to a String; no traversal happens. Inconsistent application: the trace prints the elements for one println(a) but an address for another.
- **N** (identity rule): Identity: printing an array variable outputs the text form of its reference ([I@..., [D@...), not a listing of the elements.
- **S** (declarative rule): Declarative: any value, including an array reference, is converted to a String when printed or concatenated; for an array this string is its type code and address.
- **LT** (operational sequencing rule): Sequencing: the argument a is evaluated to a reference, string conversion turns it into text, and println writes that text and a newline. The elements are never read.
- **OP** (evaluation / result rule): Result: one line such as [I@bf3f7e0 for an int[] ([D@... for double[]); the hex part changes from run to run. Exception: println(char[]) has its own overload and prints the characters.
- **OS** (state-transition rule): State transition: no variable or element changes; only one line of output is produced.
- **R** (composition rule (with a neighbour)): with array\_aliasing: Two aliases print the same text, and two separately created arrays with equal contents print different text, because println shows the reference that assignment and == also act on.
- **P** (plan / role rule): Plan/role: useful only as a diagnostic of identity (do two names hold the same reference?). To show the contents, traverse and print each a[i], or print Arrays.toString(a).
- **C** (conservation rule): Conservation: changing the elements does not change what println(a) prints (the same array keeps its reference). Replacing println(a) by a loop or Arrays.toString(a) changes the output to the elements.
- **D** (error rule): rule broken: println of an array reference prints the reference, not the elements. (silent logic error)
- **X** (applicability rule): Applicability: print a reference only when debugging whether two names share an array. For output of values use an element loop (one per line or formatted) or Arrays.toString.

## How it is found in code and answers (reader block)

- **Aliases:** memory address, hash code, address
- **Code patterns:** none
- **Operator symbols:** none
- **Java types:** none
- **Signal array\_printed\_regex** (scope program, decisive): `\b(?:int|double|boolean|char|long|String)\s*\[\]\s*(?P<arr>\w+)[\s\S]{0,4000}?print(?:ln)?\s*\((?:[^;()]*\+\s*)?(?P=arr)\s*\)`

## The whole prerequisite chain

- **Everything it builds on (11):** `array_creation`, `array_declaration`, `array_reference`, `class_declaration`, `data_structure`, `data_type`, `main_method`, `println`, `program_text`, `statement`, `string_literal`
- **Everything that builds on it (0):** nothing

## Every edge in this view and its exact edge logic (17)

All the edges drawn in the picture, in the order: prerequisite, parallel, misconception, error, has_level, contains.

**1. `array_reference` &rarr; `printing_array_reference`** (prerequisite)

- **Exact edge logic:** Printing an array variable prints the reference it holds, not the elements.
- **Grounding:** book\_passage

**2. `println` &rarr; `printing_array_reference`** (prerequisite)

- **Exact edge logic:** println of an array variable prints the array's reference, not its elements.
- **Grounding:** book\_passage

**3. `array_aliasing` &harr; `printing_array_reference`** (parallel)

- **Exact edge logic:** Both follow from the array variable holding a reference (memory address): assignment and == act on that reference, and println(a) prints it.
- **Grounding:** questionable
- **Composition rule (R) of `array_aliasing` with `printing_array_reference`:** Assignment, == and println(a) all act on the reference value: two aliases print the same address, while two equal-content arrays print different ones.
- **Composition rule (R) of `printing_array_reference` with `array_aliasing`:** Two aliases print the same text, and two separately created arrays with equal contents print different text, because println shows the reference that assignment and == also act on.

**4. `printing_array_reference` &rarr; `ArrayPrintsContents`** (misconception)

- **Exact edge logic (the wrong rule):** System.out.println(a) prints the elements of the array a.
- **Twin logic (the right rule):** Printing an array variable prints its memory address (a hexadecimal integer like @f62373), not its elements.
- **Role:** primary

**5. `printing_array_reference` &rarr; `printing_array_reference@L0`** (has_level)

- **Exact edge logic:** printing array reference -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (3 ways).
  - **[0] everyday\_reading** (rule type E, folk-meaning rule): Folk meaning: 'print a' should show what is in a, as when you print a list on paper. Java rule: System.out.println(a) converts the reference to text such as [I@bf3f7e0 (type code plus hexadecimal hash/address) and never reads the elements.
  - **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `ArrayPrintsContents`: wrong rule: System.out.println(a) prints the elements of the array a. Right rule: Printing an array variable prints its memory address (a hexadecimal integer like @f62373), not its elements.
  - **[2] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `ArrayPrintsContents`: Points to LT: println(a) converts the one reference value to a String; no traversal happens. Inconsistent application: the trace prints the elements for one println(a) but an address for another. (here mixing in: "System.out.println(a) prints the elements of the array a")

**6. `printing_array_reference` &rarr; `printing_array_reference@L1`** (has_level)

- **Exact edge logic:** printing array reference -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).
  - **[0] names\_the\_element** (rule type N, identity rule): Identity: printing an array variable outputs the text form of its reference ([I@..., [D@...), not a listing of the elements.
  - **[1] states\_the\_rule** (rule type S, declarative rule): Declarative: any value, including an array reference, is converted to a String when printed or concatenated; for an array this string is its type code and address.

**7. `printing_array_reference` &rarr; `printing_array_reference@L2`** (has_level)

- **Exact edge logic:** printing array reference -&gt; L2 (Multistructural): the answer applies the rules of printing array reference to every part of the code, in order (3 ways).
  - **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): Sequencing: the argument a is evaluated to a reference, string conversion turns it into text, and println writes that text and a newline. The elements are never read.
  - **[1] output\_prediction** (rule type OP, evaluation / result rule): Result: one line such as [I@bf3f7e0 for an int[] ([D@... for double[]); the hex part changes from run to run. Exception: println(char[]) has its own overload and prints the characters.
  - **[2] one\_step\_execution** (rule type OS, state-transition rule): State transition: no variable or element changes; only one line of output is produced.

**8. `printing_array_reference` &rarr; `printing_array_reference@L3`** (has_level)

- **Exact edge logic:** printing array reference -&gt; L3 (Relational): the answer relates the parts (2 ways).
  - **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Two aliases print the same text, and two separately created arrays with equal contents print different text, because println shows the reference that assignment and == also act on.
  - **[1] purpose\_of\_the\_whole** (rule type P, plan / role rule): Plan/role: useful only as a diagnostic of identity (do two names hold the same reference?). To show the contents, traverse and print each a[i], or print Arrays.toString(a).

**9. `printing_array_reference` &rarr; `printing_array_reference@L4`** (has_level)

- **Exact edge logic:** printing array reference -&gt; L4 (Extended abstract): the answer reasons beyond the given code (3 ways).
  - **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `ArrayPrintsContents`: Conservation: changing the elements does not change what println(a) prints (the same array keeps its reference). Replacing println(a) by a loop or Arrays.toString(a) changes the output to the elements.
  - **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Applicability: print a reference only when debugging whether two names share an array. For output of values use an element loop (one per line or formatted) or Arrays.toString.
  - **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: println of an array reference prints the reference, not the elements. Kind: silent logic error. Trigger class: an array variable (not an element) is passed to print/println or concatenated, as in "a = " + a, expecting the values

**10. `topic1.4.b` &rarr; `printing_array_reference`** (contains)

- topic `topic1.4.b` contains `printing_array_reference`

**11. `topic1.4.b` &rarr; `array_aliasing`** (contains)

- topic `topic1.4.b` contains `array_aliasing`

**12. `topic1.4.b` &rarr; `array_bounds`** (contains)

- topic `topic1.4.b` contains `array_bounds`

**13. `topic1.4.b` &rarr; `array_copy`** (contains)

- topic `topic1.4.b` contains `array_copy`

**14. `topic1.4.b` &rarr; `array_reference`** (contains)

- topic `topic1.4.b` contains `array_reference`

**15. `topic1.4.b` &rarr; `loop_guard`** (contains)

- topic `topic1.4.b` contains `loop_guard`

**16. `topic1.4.b` &rarr; `primitive_vs_reference`** (contains)

- topic `topic1.4.b` contains `primitive_vs_reference`

**17. `topic1.4.b` &rarr; `program_state`** (contains)

- topic `topic1.4.b` contains `program_state`
