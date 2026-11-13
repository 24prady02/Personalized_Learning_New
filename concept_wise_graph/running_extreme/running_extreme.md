# running_extreme (`running_extreme`)

tracking the max or min of a stream

Section 1.4 1.4 Arrays, topic 1.4.c Setting array values at compile time and at run time.

![The knowledge graph around running_extreme](running_extreme.png)

## At a glance

- **Needs first:** `array_traversal`
- **Leads to:** nothing
- **Learned alongside:** `accumulator_pattern`
- **Misconceptions:** `ExtremeStartsAtZero`
- **Errors:** none
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 13 edges around this concept. The edge logic, the wrong and right rules and the exact rules of the ways are copied word for word from the graph.

## To work on (1)

- no aliases: a student's words cannot name this concept

## What it needs first (1)

A prerequisite edge means the other concept has to be understood before `running_extreme`.

### `array_traversal` comes before `running_extreme`

*walking the array with an index loop*

- **Edge:** `pre:array_traversal->running_extreme`
- **Exact edge logic:** The running maximum is found by traversing the array once, keeping the largest value seen so far (starting from Double.NEGATIVE\_INFINITY).
- **Grounding:** book\_passage
- **Composition rule (R) of `running_extreme` with `array_traversal`:** The maximum is found in one traversal, keeping the largest value seen so far, starting from Double.NEGATIVE\_INFINITY.
- **Composition rule (R) of `array_traversal` with `running_extreme`:** The running maximum is found in one traversal that keeps the largest value seen so far, starting from Double.NEGATIVE\_INFINITY.

## What it leads to (0)

These concepts need `running_extreme` first.

No concept has this one as a prerequisite.

## Learned alongside (1)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

### `running_extreme` alongside `accumulator_pattern`

*building up a running total/result*

- **Edge:** `par:running_extreme~accumulator_pattern`
- **Exact edge logic:** Both make one pass over the values with one variable kept across passes. An accumulator (gatherer role) combines every value into it (sum += a[i]), so it starts at the identity 0.0; a running extreme (most-wanted holder) replaces it only when a better value is found (if (a[i] &gt; max) max = a[i]), so it starts at Double.NEGATIVE\_INFINITY or the first value.
- **Grounding:** book\_passage

## Misconceptions (1)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### ExtremeStartsAtZero

- **Edge:** `running_extreme` &rarr; `ExtremeStartsAtZero` (misconception)
- **Exact edge logic (the wrong rule):** The running maximum can always start at 0.
- **Twin logic (the right rule):** Start the running maximum at the most negative possible value (Double.NEGATIVE\_INFINITY, or the smallest int), so that the first value read replaces it.
- **Wrong belief (on the node):** The running maximum can always start at 0.
- **Correct rule (on the node):** Start the running maximum at the most negative possible value (Double.NEGATIVE\_INFINITY, or the smallest int), so that the first value read replaces it.
- **Provenance:** textbook
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [1] misconception, exact rule:** wrong rule: The running maximum can always start at 0. Right rule: Start the running maximum at the most negative possible value (Double.NEGATIVE\_INFINITY, or the smallest int) so that the first value read replaces it.
- **L0 way [2] inconsistent\_trace, exact rule:** Points to LT: on each pass, compare a[i] with max and assign max = a[i] only if a[i] is larger. Inconsistent application: max is overwritten without the comparison on some passes, or compared with a stale value. (here mixing in: "The running maximum can always start at 0")

## Errors (0)

An error edge states the rule that gets broken in a program, and the right rule.

The graph has no error edge from this concept.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for running extreme: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to running extreme agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

- **Edge:** `running_extreme` &rarr; `running_extreme@L0` (has_level)
- **Exact edge logic:** running extreme -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (3 ways).

Ways (3), each with its exact rule:

- **[0] everyday\_reading** (rule type E, folk-meaning rule): Folk meaning: 'the biggest so far' starts from nothing, i.e. 0, because everyday quantities are positive. Rule: the running maximum must start at a value no data can be below (Double.NEGATIVE\_INFINITY, Integer.MIN\_VALUE) or at the first element, so that the first value read replaces it.
- **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `ExtremeStartsAtZero`: wrong rule: The running maximum can always start at 0. Right rule: Start the running maximum at the most negative possible value (Double.NEGATIVE\_INFINITY, or the smallest int) so that the first value read replaces it.
- **[2] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `ExtremeStartsAtZero`: Points to LT: on each pass, compare a[i] with max and assign max = a[i] only if a[i] is larger. Inconsistent application: max is overwritten without the comparison on some passes, or compared with a stale value. (here mixing in: "The running maximum can always start at 0")

### L1: Unistructural / atom x text surface

L1 for running extreme: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

- **Edge:** `running_extreme` &rarr; `running_extreme@L1` (has_level)
- **Exact edge logic:** running extreme -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

Ways (2), each with its exact rule:

- **[0] names\_the\_element** (rule type N, identity rule): Identity: a running maximum (or minimum), a variable holding the largest (smallest) value seen so far in a pass over the data; Sajaniemi's most-wanted holder.
- **[1] states\_the\_rule** (rule type S, declarative rule): Declarative: double max = Double.NEGATIVE\_INFINITY; for (int i = 0; i &lt; N; i++) if (a[i] &gt; max) max = a[i];.

### L2: Multistructural / block x execution / preoperational

L2 for running extreme: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

- **Edge:** `running_extreme` &rarr; `running_extreme@L2` (has_level)
- **Exact edge logic:** running extreme -&gt; L2 (Multistructural): the answer applies the rules of running extreme to every part of the code, in order (3 ways).

Ways (3), each with its exact rule:

- **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): Sequencing: initialize max before the loop; in each pass evaluate a[i] &gt; max, and if it is true assign max = a[i]; read max only after the loop ends.
- **[1] output\_prediction** (rule type OP, evaluation / result rule): Result: the largest element (of the element type). For an empty array (or no input) max stays at its start value: NEGATIVE\_INFINITY, or MIN\_VALUE for int.
- **[2] one\_step\_execution** (rule type OS, state-transition rule): State transition: one pass changes max only when a[i] &gt; max; otherwise nothing changes.

### L3: Relational / relations x function (concrete operational begins)

L3 for running extreme: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

- **Edge:** `running_extreme` &rarr; `running_extreme@L3` (has_level)
- **Exact edge logic:** running extreme -&gt; L3 (Relational): the answer relates the parts (3 ways).

Ways (3), each with its exact rule:

- **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): The maximum is found in one traversal, keeping the largest value seen so far, starting from Double.NEGATIVE\_INFINITY.
- **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Both make one pass over the values with one variable kept across passes. An accumulator (gatherer role) combines every value into it (sum += a[i]), so it starts at the identity 0.0; a running extreme (most-wanted holder) replaces it only when a better value is found (if (a[i] &gt; max) max = a[i]), so it starts at Double.NEGATIVE\_INFINITY or the first value.
- **[2] purpose\_of\_the\_whole** (rule type P, plan / role rule): Plan/role: most-wanted holder (Sajaniemi). It finds the extreme in one pass with constant extra memory; the same plan tracks the minimum with &lt;.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for running extreme: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

- **Edge:** `running_extreme` &rarr; `running_extreme@L4` (has_level)
- **Exact edge logic:** running extreme -&gt; L4 (Extended abstract): the answer reasons beyond the given code (4 ways).

Ways (4), each with its exact rule:

- **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `ExtremeStartsAtZero`: Conservation: replacing &gt; by &gt;= keeps the maximum value but changes which tied position is the last one recorded. Remembering the index of the extreme instead of its value conserves the specification.
- **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Applicability: use a running extreme when only the max or min (or its position) is needed, in a single pass. For further facts such as how many items equal the maximum, keep the data (an array) and make a second pass.
- **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: The start value must not exceed every possible data value. Kind: silent logic error. Trigger class: max starts at 0 (or Double.MIN\_VALUE, which is the smallest positive double) and all data are negative, so the result is the start value
- **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: Update only when the new value beats the current extreme. Kind: silent logic error. Trigger class: the comparison is reversed (a[i] &lt; max), so the minimum is found, or max = a[i] is unconditional, so the last value is found

## Same topic

`running_extreme` belongs to the topic **Setting array values at compile time and at run time** (`topic1.4.c`). The topic also contains: `array_initializer`, `array_reversal`, `array_traversal`, `enhanced_for`.

## Rules of the concept (14)

- **Book** (SW-1e, p. 89 (pdf 99)): "find the maximum of the array values double max = Double.NEGATIVE\_INFINITY;"
- **Book** (SW-1e, p. 154 (pdf 164)): "Write a program that reads in integers (as many as the user enters) from standard input and prints out the maximum and minimum values."
- **Book** (SW-1.5, ): "first value read initialized min and max"
- **Book** (CSA, ): "If you want to set a value to the smallest possible int values use Integer.MIN\_VALUE."
- **E** (folk-meaning rule): Folk meaning: 'the biggest so far' starts from nothing, i.e. 0, because everyday quantities are positive. Rule: the running maximum must start at a value no data can be below (Double.NEGATIVE\_INFINITY, Integer.MIN\_VALUE) or at the first element, so that the first value read replaces it.
- **M** (wrong rule / right rule): ExtremeStartsAtZero: wrong: The running maximum can always start at 0. \| right: Start the running maximum at the most negative possible value (Double.NEGATIVE\_INFINITY, or the smallest int) so that the first value read replaces it.
- **T** (uneven-application rule): Points to LT: on each pass, compare a[i] with max and assign max = a[i] only if a[i] is larger. Inconsistent application: max is overwritten without the comparison on some passes, or compared with a stale value.
- **N** (identity rule): Identity: a running maximum (or minimum), a variable holding the largest (smallest) value seen so far in a pass over the data; Sajaniemi's most-wanted holder.
- **S** (declarative rule): Declarative: double max = Double.NEGATIVE\_INFINITY; for (int i = 0; i &lt; N; i++) if (a[i] &gt; max) max = a[i];.
- **LT** (operational sequencing rule): Sequencing: initialize max before the loop; in each pass evaluate a[i] &gt; max, and if it is true assign max = a[i]; read max only after the loop ends.
- **OP** (evaluation / result rule): Result: the largest element (of the element type). For an empty array (or no input) max stays at its start value: NEGATIVE\_INFINITY, or MIN\_VALUE for int.
- **OS** (state-transition rule): State transition: one pass changes max only when a[i] &gt; max; otherwise nothing changes.
- **R** (composition rule (with a neighbour)): with array\_traversal: The maximum is found in one traversal, keeping the largest value seen so far, starting from Double.NEGATIVE\_INFINITY.
- **P** (plan / role rule): Plan/role: most-wanted holder (Sajaniemi). It finds the extreme in one pass with constant extra memory; the same plan tracks the minimum with &lt;.
- **C** (conservation rule): Conservation: replacing &gt; by &gt;= keeps the maximum value but changes which tied position is the last one recorded. Remembering the index of the extreme instead of its value conserves the specification.
- **D** (error rule): rule broken: The start value must not exceed every possible data value. (silent logic error)
- **D** (error rule): rule broken: Update only when the new value beats the current extreme. (silent logic error)
- **X** (applicability rule): Applicability: use a running extreme when only the max or min (or its position) is needed, in a single pass. For further facts such as how many items equal the maximum, keep the data (an array) and make a second pass.

## How it is found in code and answers (reader block)

- **Aliases:** none
- **Code patterns:** `(?i)\bif\s*\(\s*\w+(?:\[[^\]]+\])?\s*[<>]\s*\w*(?:max|min|best|largest|smallest)\w*\s*\)`, `Math\.(?:max|min)\s*\(\s*(\w+)\s*,`, `(?i)\b\w*(?:max|min)\w*\s*=\s*\w+\s*\[[^\]]+\]\s*;`, `(?i)\bif\s*\(\s*\w+\s*\[[^\]]+\]\s*[<>]\s*\w+\s*\[\s*\w*(?:max|min|best)\w*\s*\]`
- **Operator symbols:** none
- **Java types:** none

## The whole prerequisite chain

- **Everything it builds on (23):** `arithmetic_operators`, `array_creation`, `array_declaration`, `array_initializer`, `array_traversal`, `boolean`, `boolean_expression`, `comparison_operators`, `data_structure`, `data_type`, `do_while_loop`, `expression`, `for_loop`, `identifier`, `indexing`, `length_field`, `literal`, `logical_operators`, `loop_control`, `loop_variable`, `primitive_type`, `variable`, `while_loop`
- **Everything that builds on it (0):** nothing

## Every edge in this view and its exact edge logic (13)

All the edges drawn in the picture, in the order: prerequisite, parallel, misconception, error, has_level, contains.

**1. `array_traversal` &rarr; `running_extreme`** (prerequisite)

- **Exact edge logic:** The running maximum is found by traversing the array once, keeping the largest value seen so far (starting from Double.NEGATIVE\_INFINITY).
- **Grounding:** book\_passage
- **Composition rule (R) of `array_traversal` with `running_extreme`:** The running maximum is found in one traversal that keeps the largest value seen so far, starting from Double.NEGATIVE\_INFINITY.
- **Composition rule (R) of `running_extreme` with `array_traversal`:** The maximum is found in one traversal, keeping the largest value seen so far, starting from Double.NEGATIVE\_INFINITY.

**2. `running_extreme` &harr; `accumulator_pattern`** (parallel)

- **Exact edge logic:** Both make one pass over the values with one variable kept across passes. An accumulator (gatherer role) combines every value into it (sum += a[i]), so it starts at the identity 0.0; a running extreme (most-wanted holder) replaces it only when a better value is found (if (a[i] &gt; max) max = a[i]), so it starts at Double.NEGATIVE\_INFINITY or the first value.
- **Grounding:** book\_passage

**3. `running_extreme` &rarr; `ExtremeStartsAtZero`** (misconception)

- **Exact edge logic (the wrong rule):** The running maximum can always start at 0.
- **Twin logic (the right rule):** Start the running maximum at the most negative possible value (Double.NEGATIVE\_INFINITY, or the smallest int), so that the first value read replaces it.
- **Role:** primary

**4. `running_extreme` &rarr; `running_extreme@L0`** (has_level)

- **Exact edge logic:** running extreme -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (3 ways).
  - **[0] everyday\_reading** (rule type E, folk-meaning rule): Folk meaning: 'the biggest so far' starts from nothing, i.e. 0, because everyday quantities are positive. Rule: the running maximum must start at a value no data can be below (Double.NEGATIVE\_INFINITY, Integer.MIN\_VALUE) or at the first element, so that the first value read replaces it.
  - **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `ExtremeStartsAtZero`: wrong rule: The running maximum can always start at 0. Right rule: Start the running maximum at the most negative possible value (Double.NEGATIVE\_INFINITY, or the smallest int) so that the first value read replaces it.
  - **[2] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `ExtremeStartsAtZero`: Points to LT: on each pass, compare a[i] with max and assign max = a[i] only if a[i] is larger. Inconsistent application: max is overwritten without the comparison on some passes, or compared with a stale value. (here mixing in: "The running maximum can always start at 0")

**5. `running_extreme` &rarr; `running_extreme@L1`** (has_level)

- **Exact edge logic:** running extreme -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).
  - **[0] names\_the\_element** (rule type N, identity rule): Identity: a running maximum (or minimum), a variable holding the largest (smallest) value seen so far in a pass over the data; Sajaniemi's most-wanted holder.
  - **[1] states\_the\_rule** (rule type S, declarative rule): Declarative: double max = Double.NEGATIVE\_INFINITY; for (int i = 0; i &lt; N; i++) if (a[i] &gt; max) max = a[i];.

**6. `running_extreme` &rarr; `running_extreme@L2`** (has_level)

- **Exact edge logic:** running extreme -&gt; L2 (Multistructural): the answer applies the rules of running extreme to every part of the code, in order (3 ways).
  - **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): Sequencing: initialize max before the loop; in each pass evaluate a[i] &gt; max, and if it is true assign max = a[i]; read max only after the loop ends.
  - **[1] output\_prediction** (rule type OP, evaluation / result rule): Result: the largest element (of the element type). For an empty array (or no input) max stays at its start value: NEGATIVE\_INFINITY, or MIN\_VALUE for int.
  - **[2] one\_step\_execution** (rule type OS, state-transition rule): State transition: one pass changes max only when a[i] &gt; max; otherwise nothing changes.

**7. `running_extreme` &rarr; `running_extreme@L3`** (has_level)

- **Exact edge logic:** running extreme -&gt; L3 (Relational): the answer relates the parts (3 ways).
  - **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): The maximum is found in one traversal, keeping the largest value seen so far, starting from Double.NEGATIVE\_INFINITY.
  - **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Both make one pass over the values with one variable kept across passes. An accumulator (gatherer role) combines every value into it (sum += a[i]), so it starts at the identity 0.0; a running extreme (most-wanted holder) replaces it only when a better value is found (if (a[i] &gt; max) max = a[i]), so it starts at Double.NEGATIVE\_INFINITY or the first value.
  - **[2] purpose\_of\_the\_whole** (rule type P, plan / role rule): Plan/role: most-wanted holder (Sajaniemi). It finds the extreme in one pass with constant extra memory; the same plan tracks the minimum with &lt;.

**8. `running_extreme` &rarr; `running_extreme@L4`** (has_level)

- **Exact edge logic:** running extreme -&gt; L4 (Extended abstract): the answer reasons beyond the given code (4 ways).
  - **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `ExtremeStartsAtZero`: Conservation: replacing &gt; by &gt;= keeps the maximum value but changes which tied position is the last one recorded. Remembering the index of the extreme instead of its value conserves the specification.
  - **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Applicability: use a running extreme when only the max or min (or its position) is needed, in a single pass. For further facts such as how many items equal the maximum, keep the data (an array) and make a second pass.
  - **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: The start value must not exceed every possible data value. Kind: silent logic error. Trigger class: max starts at 0 (or Double.MIN\_VALUE, which is the smallest positive double) and all data are negative, so the result is the start value
  - **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: Update only when the new value beats the current extreme. Kind: silent logic error. Trigger class: the comparison is reversed (a[i] &lt; max), so the minimum is found, or max = a[i] is unconditional, so the last value is found

**9. `topic1.4.c` &rarr; `running_extreme`** (contains)

- topic `topic1.4.c` contains `running_extreme`

**10. `topic1.4.c` &rarr; `array_initializer`** (contains)

- topic `topic1.4.c` contains `array_initializer`

**11. `topic1.4.c` &rarr; `array_reversal`** (contains)

- topic `topic1.4.c` contains `array_reversal`

**12. `topic1.4.c` &rarr; `array_traversal`** (contains)

- topic `topic1.4.c` contains `array_traversal`

**13. `topic1.4.c` &rarr; `enhanced_for`** (contains)

- topic `topic1.4.c` contains `enhanced_for`
