# array_default_values (`array_default_values`)

new slots start at 0 / false / null

Section 1.4 Arrays, topic 1.4.a Arrays in Java (declare, create, initialize; indexing; length; default values).

![The knowledge graph around array_default_values](array_default_values.png)

## At a glance

- **Needs first:** `array_creation`
- **Leads to:** `boolean_flag_array`
- **Learned alongside:** `definite_assignment`
- **Misconceptions:** `ArrayCreationIsFree`, `NewArrayHoldsGarbage`
- **Errors:** none
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 21 edges around this concept. The edge logic, the wrong and right rules and the exact rules of the ways are copied word for word from the graph.

## To work on (0)

Nothing is missing for this concept.

## What it needs first (1)

A prerequisite edge means the other concept has to be understood before `array_default_values`.

### `array_creation` comes before `array_default_values`

*new int[n] -- allocates n slots*

- **Edge:** `pre:array_creation->array_default_values`
- **Exact edge logic:** new fills every slot with the type's default value: 0, 0.0, false or null.
- **Grounding:** book\_passage
- **Composition rule (R) of `array_default_values` with `array_creation`:** Defaults come from creation, so every execution of new resets them; creating the array inside the trial loop gives each experiment a clean all-false grid.
- **Composition rule (R) of `array_creation` with `array_default_values`:** Creation is what puts the default value (0, 0.0, false, null) in every slot; each execution of new gives fresh defaults.

## What it leads to (1)

These concepts need `array_default_values` first.

### `array_default_values` comes before `boolean_flag_array`

*boolean[] used to mark which values are seen (coupon collector, sieve)*

- **Edge:** `pre:array_default_values->boolean_flag_array`
- **Exact edge logic:** new boolean[n] starts every flag at false.
- **Grounding:** order\_only
- **Composition rule (R) of `array_default_values` with `boolean_flag_array`:** new boolean[n] starts every flag at false ('not seen yet'), so CouponCollector needs no initialization loop. PrimeSieve needs true as its start value and so must loop to set it.
- **Composition rule (R) of `boolean_flag_array` with `array_default_values`:** new boolean[n] starts every flag at false, which CouponCollector relies on; PrimeSieve needs true and so sets it with a loop.

## Learned alongside (1)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

### `array_default_values` alongside `definite_assignment`

*a local variable must be assigned before it is read*

- **Edge:** `par:definite_assignment~array_default_values`
- **Exact edge logic:** A local variable has no value until it is assigned: using it first is a compile-time error. An array element is given a default value (0, 0.0, false) when the array is created with new, so it can be read before any assignment.
- **Grounding:** book\_passage

## Misconceptions (2)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### ArrayCreationIsFree

- **Edge:** `array_default_values` &rarr; `ArrayCreationIsFree` (misconception)
- **Exact edge logic (the wrong rule):** Creating a big array with new takes no time because the elements are not set yet.
- **Twin logic (the right rule):** Java initializes every element when the array is created, so creation takes time proportional to its length.
- **Wrong belief (on the node):** Creating a big array with new takes no time because the elements are not set yet.
- **Correct rule (on the node):** Java initializes every element when the array is created, so creation takes time proportional to its length.
- **Provenance:** textbook
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [3] misconception, exact rule:** wrong rule: Creating a big array with new takes no time because the elements are not set yet. Right rule: Because Java sets every element to its default at creation, creating an array takes time proportional to its length.
- **Edge `array_creation` &rarr; `ArrayCreationIsFree`, exact edge logic:** Creating a big array with new takes no time because the elements are not set yet. **Twin logic:** Java initializes every element when the array is created, so creation takes time proportional to its length. (role: primary)

### NewArrayHoldsGarbage

- **Edge:** `array_default_values` &rarr; `NewArrayHoldsGarbage` (misconception)
- **Exact edge logic (the wrong rule):** The slots of a new int[n] hold unpredictable values until assigned.
- **Twin logic (the right rule):** new fills every element with a default: 0 for numeric types, false for boolean, null for String and other non-primitive types.
- **Wrong belief (on the node):** The slots of a new int[n] hold unpredictable values until assigned.
- **Correct rule (on the node):** new fills every element with a default: 0 for numeric types, false for boolean, null for String and other non-primitive types.
- **Provenance:** published
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [1] misconception, exact rule:** wrong rule: The slots of a new int[n] hold unpredictable values until assigned. Right rule: new fills every element with a default: 0 for numeric types, false for boolean, null for String and other non-primitive types.
- **L0 way [2] inconsistent\_trace, exact rule:** Points to LT: creation stores the default in every element before any statement can read one. Inconsistent application: the trace reads a fresh a[i] as 0 on one pass but as 'empty' or 'unknown' on another, or gives a new boolean[] the value true. (here mixing in: "The slots of a new int[n] hold unpredictable values until assigned")
- **Edge `boolean_flag_array` &rarr; `NewArrayHoldsGarbage`, exact edge logic:** The slots of a new int[n] hold unpredictable values until assigned. **Twin logic:** new fills every element with a default: 0 for numeric types, false for boolean, null for String and other non-primitive types. (role: context)
- **Edge `primitive_type` &rarr; `NewArrayHoldsGarbage`, exact edge logic:** The slots of a new int[n] hold unpredictable values until assigned. **Twin logic:** new fills every element with a default: 0 for numeric types, false for boolean, null for String and other non-primitive types. (role: context)

## Errors (0)

An error edge states the rule that gets broken in a program, and the right rule.

The graph has no error edge from this concept.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for array default values: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to array default values agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

- **Edge:** `array_default_values` &rarr; `array_default_values@L0` (has_level)
- **Exact edge logic:** array default values -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (4 ways).

Ways (4), each with its exact rule:

- **[0] everyday\_reading** (rule type E, folk-meaning rule): Folk meaning: an everyday new box is 'empty' (nothing in it), and C-trained intuition says new memory holds garbage. Java rule: every element of a new array holds a definite default (0 for numbers, 0.0 for double, false for boolean, null for String and other reference types).
- **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `NewArrayHoldsGarbage`: wrong rule: The slots of a new int[n] hold unpredictable values until assigned. Right rule: new fills every element with a default: 0 for numeric types, false for boolean, null for String and other non-primitive types.
- **[2] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `NewArrayHoldsGarbage`: Points to LT: creation stores the default in every element before any statement can read one. Inconsistent application: the trace reads a fresh a[i] as 0 on one pass but as 'empty' or 'unknown' on another, or gives a new boolean[] the value true. (here mixing in: "The slots of a new int[n] hold unpredictable values until assigned")
- **[3] misconception** (rule type M, wrong rule / right rule) &rarr; `ArrayCreationIsFree`: wrong rule: Creating a big array with new takes no time because the elements are not set yet. Right rule: Because Java sets every element to its default at creation, creating an array takes time proportional to its length.

### L1: Unistructural / atom x text surface

L1 for array default values: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

- **Edge:** `array_default_values` &rarr; `array_default_values@L1` (has_level)
- **Exact edge logic:** array default values -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

Ways (2), each with its exact rule:

- **[0] names\_the\_element** (rule type N, identity rule): Identity: the initial value Java gives each element of a newly created array: zero for numeric types, false for boolean, null for references.
- **[1] states\_the\_rule** (rule type S, declarative rule): Declarative: 'The default initial value is zero for all numbers and false for type boolean'; for String and other non-primitive types it is null. The same holds for every entry of a 2-D array.

### L2: Multistructural / block x execution / preoperational

L2 for array default values: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

- **Edge:** `array_default_values` &rarr; `array_default_values@L2` (has_level)
- **Exact edge logic:** array default values -&gt; L2 (Multistructural): the answer applies the rules of array default values to every part of the code, in order (3 ways).

Ways (3), each with its exact rule:

- **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): Sequencing: defaults are stored during creation, before the reference is returned. An explicit initialization loop that follows simply overwrites them, so the loop is needed only for a non-default start value.
- **[1] output\_prediction** (rule type OP, evaluation / result rule): Result: reading an element never assigned gives 0 in an int[], 0.0 in a double[], false in a boolean[] and null in a String[] (println prints the text null).
- **[2] one\_step\_execution** (rule type OS, state-transition rule): State transition: the creation step sets all n element variables to the default in one go. Reading a default changes nothing.

### L3: Relational / relations x function (concrete operational begins)

L3 for array default values: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

- **Edge:** `array_default_values` &rarr; `array_default_values@L3` (has_level)
- **Exact edge logic:** array default values -&gt; L3 (Relational): the answer relates the parts (4 ways).

Ways (4), each with its exact rule:

- **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Defaults come from creation, so every execution of new resets them; creating the array inside the trial loop gives each experiment a clean all-false grid.
- **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): new boolean[n] starts every flag at false ('not seen yet'), so CouponCollector needs no initialization loop. PrimeSieve needs true as its start value and so must loop to set it.
- **[2] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): A local variable has no value until it is assigned: using it first is a compile-time error. An array element is given a default value (0, 0.0, false) when the array is created with new, so it can be read before any assignment.
- **[3] purpose\_of\_the\_whole** (rule type P, plan / role rule): Plan/role: lets counter and flag arrays (counts[], found[]) start at 0 or false, ready to accumulate, with no initialization loop; the book calls this using Java's default array initialization convention.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for array default values: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

- **Edge:** `array_default_values` &rarr; `array_default_values@L4` (has_level)
- **Exact edge logic:** array default values -&gt; L4 (Extended abstract): the answer reasons beyond the given code (4 ways).

Ways (4), each with its exact rule:

- **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `NewArrayHoldsGarbage`: Conservation: changing the element type changes the default (int 0, double 0.0, boolean false, String null). Moving the creation into a loop resets the defaults on each pass. Adding an explicit loop that stores the default changes nothing.
- **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Applicability: rely on the defaults when the needed start value is exactly 0, 0.0, false or null (counters, flags, accumulators). Write an initialization loop for any other start value. Plain local variables get no default, so the convenience applies only to array elements.
- **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: Defaults are 0/false/null; any other start value must be assigned explicitly. Kind: silent logic error. Trigger class: the code assumes a non-default start value without setting it, e.g. PrimeSieve with its 'isPrime[i] = true' loop removed counts 0 primes
- **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: Elements of a reference-type array start as null, which refers to no object. Kind: run-time exception. Trigger class: a method is called on an element of a new String[] (or other object array) before it is assigned, e.g. s[0].length() (NullPointerException)

## Same topic

`array_default_values` belongs to the topic **Arrays in Java (declare, create, initialize; indexing; length; default values)** (`topic1.4.a`). The topic also contains: `args_length`, `array_creation`, `array_declaration`, `data_structure`, `indexing`, `length_field`, `off_by_one_error`.

## Rules of the concept (16)

- **Book** (SW-1e, p. 87 (pdf 97)): "The default initial value is zero for all numbers and false for type boolean."
- **Book** (SW-1e, p. 87 (pdf 97)): "For String and other non-primitive types, the default is the value null"
- **Book** (SW-1.4, ): "The default initial value is 0 for all numeric primitive types and false for type boolean."
- **E** (folk-meaning rule): Folk meaning: an everyday new box is 'empty' (nothing in it), and C-trained intuition says new memory holds garbage. Java rule: every element of a new array holds a definite default (0 for numbers, 0.0 for double, false for boolean, null for String and other reference types).
- **M** (wrong rule / right rule): NewArrayHoldsGarbage: wrong: The slots of a new int[n] hold unpredictable values until assigned. \| right: new fills every element with a default: 0 for numeric types, false for boolean, null for String and other non-primitive types.
- **M** (wrong rule / right rule): ArrayCreationIsFree: wrong: Creating a big array with new takes no time because the elements are not set yet. \| right: Because Java sets every element to its default at creation, creating an array takes time proportional to its length.
- **T** (uneven-application rule): Points to LT: creation stores the default in every element before any statement can read one. Inconsistent application: the trace reads a fresh a[i] as 0 on one pass but as 'empty' or 'unknown' on another, or gives a new boolean[] the value true.
- **N** (identity rule): Identity: the initial value Java gives each element of a newly created array: zero for numeric types, false for boolean, null for references.
- **S** (declarative rule): Declarative: 'The default initial value is zero for all numbers and false for type boolean'; for String and other non-primitive types it is null. The same holds for every entry of a 2-D array.
- **LT** (operational sequencing rule): Sequencing: defaults are stored during creation, before the reference is returned. An explicit initialization loop that follows simply overwrites them, so the loop is needed only for a non-default start value.
- **OP** (evaluation / result rule): Result: reading an element never assigned gives 0 in an int[], 0.0 in a double[], false in a boolean[] and null in a String[] (println prints the text null).
- **OS** (state-transition rule): State transition: the creation step sets all n element variables to the default in one go. Reading a default changes nothing.
- **R** (composition rule (with a neighbour)): with array\_creation: Defaults come from creation, so every execution of new resets them; creating the array inside the trial loop gives each experiment a clean all-false grid.
- **R** (composition rule (with a neighbour)): with boolean\_flag\_array: new boolean[n] starts every flag at false ('not seen yet'), so CouponCollector needs no initialization loop. PrimeSieve needs true as its start value and so must loop to set it.
- **P** (plan / role rule): Plan/role: lets counter and flag arrays (counts[], found[]) start at 0 or false, ready to accumulate, with no initialization loop; the book calls this using Java's default array initialization convention.
- **C** (conservation rule): Conservation: changing the element type changes the default (int 0, double 0.0, boolean false, String null). Moving the creation into a loop resets the defaults on each pass. Adding an explicit loop that stores the default changes nothing.
- **D** (error rule): rule broken: Defaults are 0/false/null; any other start value must be assigned explicitly. (silent logic error)
- **D** (error rule): rule broken: Elements of a reference-type array start as null, which refers to no object. (run-time exception)
- **X** (applicability rule): Applicability: rely on the defaults when the needed start value is exactly 0, 0.0, false or null (counters, flags, accumulators). Write an initialization loop for any other start value. Plain local variables get no default, so the convenience applies only to array elements.

## How it is found in code and answers (reader block)

- **Aliases:** array default, array defaults, array element, array elements, default value, default values, defaults to zero
- **Code patterns:** `\bnew\s+(?:int|double|boolean|char|long|String|float|short|byte)\s*\[[^\]]+\]\s*;`
- **Operator symbols:** none
- **Java types:** none

## The whole prerequisite chain

- **Everything it builds on (4):** `array_creation`, `array_declaration`, `data_structure`, `data_type`
- **Everything that builds on it (1):** `boolean_flag_array`

## Every edge in this view and its exact edge logic (21)

All the edges drawn in the picture, in the order: prerequisite, parallel, misconception, error, has_level, contains.

**1. `array_creation` &rarr; `array_default_values`** (prerequisite)

- **Exact edge logic:** new fills every slot with the type's default value: 0, 0.0, false or null.
- **Grounding:** book\_passage
- **Composition rule (R) of `array_creation` with `array_default_values`:** Creation is what puts the default value (0, 0.0, false, null) in every slot; each execution of new gives fresh defaults.
- **Composition rule (R) of `array_default_values` with `array_creation`:** Defaults come from creation, so every execution of new resets them; creating the array inside the trial loop gives each experiment a clean all-false grid.

**2. `array_default_values` &rarr; `boolean_flag_array`** (prerequisite)

- **Exact edge logic:** new boolean[n] starts every flag at false.
- **Grounding:** order\_only
- **Composition rule (R) of `array_default_values` with `boolean_flag_array`:** new boolean[n] starts every flag at false ('not seen yet'), so CouponCollector needs no initialization loop. PrimeSieve needs true as its start value and so must loop to set it.
- **Composition rule (R) of `boolean_flag_array` with `array_default_values`:** new boolean[n] starts every flag at false, which CouponCollector relies on; PrimeSieve needs true and so sets it with a loop.

**3. `definite_assignment` &harr; `array_default_values`** (parallel)

- **Exact edge logic:** A local variable has no value until it is assigned: using it first is a compile-time error. An array element is given a default value (0, 0.0, false) when the array is created with new, so it can be read before any assignment.
- **Grounding:** book\_passage

**4. `array_default_values` &rarr; `ArrayCreationIsFree`** (misconception)

- **Exact edge logic (the wrong rule):** Creating a big array with new takes no time because the elements are not set yet.
- **Twin logic (the right rule):** Java initializes every element when the array is created, so creation takes time proportional to its length.
- **Role:** context

**5. `array_default_values` &rarr; `NewArrayHoldsGarbage`** (misconception)

- **Exact edge logic (the wrong rule):** The slots of a new int[n] hold unpredictable values until assigned.
- **Twin logic (the right rule):** new fills every element with a default: 0 for numeric types, false for boolean, null for String and other non-primitive types.
- **Role:** primary

**6. `array_creation` &rarr; `ArrayCreationIsFree`** (misconception)

- **Exact edge logic (the wrong rule):** Creating a big array with new takes no time because the elements are not set yet.
- **Twin logic (the right rule):** Java initializes every element when the array is created, so creation takes time proportional to its length.
- **Role:** primary

**7. `boolean_flag_array` &rarr; `NewArrayHoldsGarbage`** (misconception)

- **Exact edge logic (the wrong rule):** The slots of a new int[n] hold unpredictable values until assigned.
- **Twin logic (the right rule):** new fills every element with a default: 0 for numeric types, false for boolean, null for String and other non-primitive types.
- **Role:** context

**8. `primitive_type` &rarr; `NewArrayHoldsGarbage`** (misconception)

- **Exact edge logic (the wrong rule):** The slots of a new int[n] hold unpredictable values until assigned.
- **Twin logic (the right rule):** new fills every element with a default: 0 for numeric types, false for boolean, null for String and other non-primitive types.
- **Role:** context

**9. `array_default_values` &rarr; `array_default_values@L0`** (has_level)

- **Exact edge logic:** array default values -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (4 ways).
  - **[0] everyday\_reading** (rule type E, folk-meaning rule): Folk meaning: an everyday new box is 'empty' (nothing in it), and C-trained intuition says new memory holds garbage. Java rule: every element of a new array holds a definite default (0 for numbers, 0.0 for double, false for boolean, null for String and other reference types).
  - **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `NewArrayHoldsGarbage`: wrong rule: The slots of a new int[n] hold unpredictable values until assigned. Right rule: new fills every element with a default: 0 for numeric types, false for boolean, null for String and other non-primitive types.
  - **[2] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `NewArrayHoldsGarbage`: Points to LT: creation stores the default in every element before any statement can read one. Inconsistent application: the trace reads a fresh a[i] as 0 on one pass but as 'empty' or 'unknown' on another, or gives a new boolean[] the value true. (here mixing in: "The slots of a new int[n] hold unpredictable values until assigned")
  - **[3] misconception** (rule type M, wrong rule / right rule) &rarr; `ArrayCreationIsFree`: wrong rule: Creating a big array with new takes no time because the elements are not set yet. Right rule: Because Java sets every element to its default at creation, creating an array takes time proportional to its length.

**10. `array_default_values` &rarr; `array_default_values@L1`** (has_level)

- **Exact edge logic:** array default values -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).
  - **[0] names\_the\_element** (rule type N, identity rule): Identity: the initial value Java gives each element of a newly created array: zero for numeric types, false for boolean, null for references.
  - **[1] states\_the\_rule** (rule type S, declarative rule): Declarative: 'The default initial value is zero for all numbers and false for type boolean'; for String and other non-primitive types it is null. The same holds for every entry of a 2-D array.

**11. `array_default_values` &rarr; `array_default_values@L2`** (has_level)

- **Exact edge logic:** array default values -&gt; L2 (Multistructural): the answer applies the rules of array default values to every part of the code, in order (3 ways).
  - **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): Sequencing: defaults are stored during creation, before the reference is returned. An explicit initialization loop that follows simply overwrites them, so the loop is needed only for a non-default start value.
  - **[1] output\_prediction** (rule type OP, evaluation / result rule): Result: reading an element never assigned gives 0 in an int[], 0.0 in a double[], false in a boolean[] and null in a String[] (println prints the text null).
  - **[2] one\_step\_execution** (rule type OS, state-transition rule): State transition: the creation step sets all n element variables to the default in one go. Reading a default changes nothing.

**12. `array_default_values` &rarr; `array_default_values@L3`** (has_level)

- **Exact edge logic:** array default values -&gt; L3 (Relational): the answer relates the parts (4 ways).
  - **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Defaults come from creation, so every execution of new resets them; creating the array inside the trial loop gives each experiment a clean all-false grid.
  - **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): new boolean[n] starts every flag at false ('not seen yet'), so CouponCollector needs no initialization loop. PrimeSieve needs true as its start value and so must loop to set it.
  - **[2] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): A local variable has no value until it is assigned: using it first is a compile-time error. An array element is given a default value (0, 0.0, false) when the array is created with new, so it can be read before any assignment.
  - **[3] purpose\_of\_the\_whole** (rule type P, plan / role rule): Plan/role: lets counter and flag arrays (counts[], found[]) start at 0 or false, ready to accumulate, with no initialization loop; the book calls this using Java's default array initialization convention.

**13. `array_default_values` &rarr; `array_default_values@L4`** (has_level)

- **Exact edge logic:** array default values -&gt; L4 (Extended abstract): the answer reasons beyond the given code (4 ways).
  - **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `NewArrayHoldsGarbage`: Conservation: changing the element type changes the default (int 0, double 0.0, boolean false, String null). Moving the creation into a loop resets the defaults on each pass. Adding an explicit loop that stores the default changes nothing.
  - **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Applicability: rely on the defaults when the needed start value is exactly 0, 0.0, false or null (counters, flags, accumulators). Write an initialization loop for any other start value. Plain local variables get no default, so the convenience applies only to array elements.
  - **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: Defaults are 0/false/null; any other start value must be assigned explicitly. Kind: silent logic error. Trigger class: the code assumes a non-default start value without setting it, e.g. PrimeSieve with its 'isPrime[i] = true' loop removed counts 0 primes
  - **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: Elements of a reference-type array start as null, which refers to no object. Kind: run-time exception. Trigger class: a method is called on an element of a new String[] (or other object array) before it is assigned, e.g. s[0].length() (NullPointerException)

**14. `topic1.4.a` &rarr; `array_default_values`** (contains)

- topic `topic1.4.a` contains `array_default_values`

**15. `topic1.4.a` &rarr; `args_length`** (contains)

- topic `topic1.4.a` contains `args_length`

**16. `topic1.4.a` &rarr; `array_creation`** (contains)

- topic `topic1.4.a` contains `array_creation`

**17. `topic1.4.a` &rarr; `array_declaration`** (contains)

- topic `topic1.4.a` contains `array_declaration`

**18. `topic1.4.a` &rarr; `data_structure`** (contains)

- topic `topic1.4.a` contains `data_structure`

**19. `topic1.4.a` &rarr; `indexing`** (contains)

- topic `topic1.4.a` contains `indexing`

**20. `topic1.4.a` &rarr; `length_field`** (contains)

- topic `topic1.4.a` contains `length_field`

**21. `topic1.4.a` &rarr; `off_by_one_error`** (contains)

- topic `topic1.4.a` contains `off_by_one_error`
