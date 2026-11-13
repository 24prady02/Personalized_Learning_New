# lookup_table (`lookup_table`)

an array of precomputed values or names indexed by position

Section 1.4 Arrays, topic 1.4.e Precomputed values and simplifying repetitive code.

![The knowledge graph around lookup_table](lookup_table.png)

## At a glance

- **Needs first:** `array_initializer`, `indexing`
- **Leads to:** `space_time_tradeoff`
- **Learned alongside:** nothing
- **Misconceptions:** `ArrayIndexStartsAtOne`
- **Errors:** none
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 12 edges around this concept. The edge logic, the wrong and right rules and the exact rules of the ways are copied word for word from the graph.

## To work on (1)

- no aliases: a student's words cannot name this concept

## What it needs first (2)

A prerequisite edge means the other concept has to be understood before `lookup_table`.

### `array_initializer` comes before `lookup_table`

*{1, 2, 3} literal initialization*

- **Edge:** `pre:array_initializer->lookup_table`
- **Exact edge logic:** A lookup table is usually an array of fixed values written as a literal and read by index.
- **Grounding:** book\_passage

### `indexing` comes before `lookup_table`

*a[i] -- 0-based access*

- **Edge:** `pre:indexing->lookup_table`
- **Exact edge logic:** A lookup table is read by index, a[i].
- **Grounding:** book\_passage
- **Composition rule (R) of `lookup_table` with `indexing`:** The key itself is the index (months[m], rank[i]), so keys must fall in 0..length-1.
- **Composition rule (R) of `indexing` with `lookup_table`:** A lookup table uses a data value as the index (months[m]), so the data must lie in 0..length-1.

## What it leads to (1)

These concepts need `lookup_table` first.

### `lookup_table` comes before `space_time_tradeoff`

*Space-time tradeoff: investing memory (an array of saved values) to save computation time*

- **Edge:** `pre:lookup_table->space_time_tradeoff`
- **Exact edge logic:** Saving precomputed values in an array trades memory for time: each value is computed once and then looked up.
- **Grounding:** book\_passage
- **Composition rule (R) of `lookup_table` with `space_time_tradeoff`:** Storing precomputed values trades memory for time: each value is computed once and then looked up.
- **Composition rule (R) of `space_time_tradeoff` with `lookup_table`:** The lookup table is the stored space: each value is computed once and then read by index.

## Learned alongside (0)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

No parallel edge touches this concept.

## Misconceptions (1)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### ArrayIndexStartsAtOne

- **Edge:** `lookup_table` &rarr; `ArrayIndexStartsAtOne` (misconception)
- **Exact edge logic (the wrong rule):** The first element of a is a[1].
- **Twin logic (the right rule):** Numbering begins with 0; the first element is a[0].
- **Wrong belief (on the node):** The first element of a is a[1].
- **Correct rule (on the node):** Numbering begins with 0; the first element is a[0].
- **Provenance:** published
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [1] misconception, exact rule:** wrong rule: The first element of a is a[1]. Right rule: Numbering begins with 0; a 1-based key needs a padding slot at index 0 or the index key-1.
- **L0 way [2] inconsistent\_trace, exact rule:** Points to LT: compute the index from the data, then read the table entry. Inconsistent application: 1 is subtracted from the key on some lookups but not on others, or the padding slot is counted as January. (here mixing in: "The first element of a is a[1]")
- **Edge `indexing` &rarr; `ArrayIndexStartsAtOne`, exact edge logic:** The first element of a is a[1]. **Twin logic:** Numbering begins with 0; the first element is a[0]. (role: primary)

## Errors (0)

An error edge states the rule that gets broken in a program, and the right rule.

The graph has no error edge from this concept.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for lookup table: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to lookup table agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

- **Edge:** `lookup_table` &rarr; `lookup_table@L0` (has_level)
- **Exact edge logic:** lookup table -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (3 ways).

Ways (3), each with its exact rule:

- **[0] everyday\_reading** (rule type E, folk-meaning rule): Folk meaning: everyday tables are numbered from 1 (month 1 is January) and are looked up by scanning. Java rule: array tables are 0-origin and are read directly by index, so either waste slot 0 (months[0] = "") or subtract 1 from the key.
- **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `ArrayIndexStartsAtOne`: wrong rule: The first element of a is a[1]. Right rule: Numbering begins with 0; a 1-based key needs a padding slot at index 0 or the index key-1.
- **[2] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `ArrayIndexStartsAtOne`: Points to LT: compute the index from the data, then read the table entry. Inconsistent application: 1 is subtracted from the key on some lookups but not on others, or the padding slot is counted as January. (here mixing in: "The first element of a is a[1]")

### L1: Unistructural / atom x text surface

L1 for lookup table: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

- **Edge:** `lookup_table` &rarr; `lookup_table@L1` (has_level)
- **Exact edge logic:** lookup table -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

Ways (2), each with its exact rule:

- **[0] names\_the\_element** (rule type N, identity rule): Identity: a lookup table is an array whose element i holds a precomputed value or name for i, read by indexing.
- **[1] states\_the\_rule** (rule type S, declarative rule): Declarative: build the table once (initializer or loop), e.g. String[] months = {"", "Jan", ..., "Dec"}; or H[i] = H[i-1] + 1.0/i; then use months[m] or H[i] in place of recomputing.

### L2: Multistructural / block x execution / preoperational

L2 for lookup table: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

- **Edge:** `lookup_table` &rarr; `lookup_table@L2` (has_level)
- **Exact edge logic:** lookup table -&gt; L2 (Multistructural): the answer applies the rules of lookup table to every part of the code, in order (3 ways).

Ways (3), each with its exact rule:

- **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): Sequencing: the whole table is built before the first lookup. Each lookup evaluates the index expression, checks the bounds and reads one element.
- **[1] output\_prediction** (rule type OP, evaluation / result rule): Result: months[m] is the name of month m for m = 1..12 (months[0] is the empty string); H[i] is the i-th harmonic number.
- **[2] one\_step\_execution** (rule type OS, state-transition rule): State transition: a lookup changes nothing; only the building phase stores values (one element per step).

### L3: Relational / relations x function (concrete operational begins)

L3 for lookup table: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

- **Edge:** `lookup_table` &rarr; `lookup_table@L3` (has_level)
- **Exact edge logic:** lookup table -&gt; L3 (Relational): the answer relates the parts (3 ways).

Ways (3), each with its exact rule:

- **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): The key itself is the index (months[m], rank[i]), so keys must fall in 0..length-1.
- **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Storing precomputed values trades memory for time: each value is computed once and then looked up.
- **[2] purpose\_of\_the\_whole** (rule type P, plan / role rule): Plan/role: the table is a fixed value (Sajaniemi). It replaces long if-else chains or repeated computation with one indexed read.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for lookup table: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

- **Edge:** `lookup_table` &rarr; `lookup_table@L4` (has_level)
- **Exact edge logic:** lookup table -&gt; L4 (Extended abstract): the answer reasons beyond the given code (4 ways).

Ways (4), each with its exact rule:

- **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `ArrayIndexStartsAtOne`: Conservation: adding entries at the end keeps existing lookups valid. Removing the padding slot shifts every entry down one, so months[1] becomes Feb (off by one). Changing a stored value changes every lookup of it.
- **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Applicability: use a table when the same values are needed many times for small integer keys. It is not effective for huge key ranges, for values needed only once, or for keys that are not small integers.
- **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: Keys must map to legal indices. Kind: run-time exception. Trigger class: a key outside the table, e.g. months[13] or months[0-1] (ArrayIndexOutOfBoundsException)
- **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: The key-to-index mapping must match the table layout. Kind: silent logic error. Trigger class: a 1-based key used with a table that has no padding slot, so every lookup returns the next entry

## Same topic

`lookup_table` belongs to the topic **Precomputed values and simplifying repetitive code** (`topic1.4.e`). The topic also contains: `space_time_tradeoff`.

## Rules of the concept (15)

- **Book** (SW-1e, p. 91 (pdf 101)): "This code uses the idiom introduced in SECTION 1.2 to generate random indices and then uses the indices"
- **Book** (SW-1.4, ): "by investing in space (to save the values) we save time."
- **E** (folk-meaning rule): Folk meaning: everyday tables are numbered from 1 (month 1 is January) and are looked up by scanning. Java rule: array tables are 0-origin and are read directly by index, so either waste slot 0 (months[0] = "") or subtract 1 from the key.
- **M** (wrong rule / right rule): ArrayIndexStartsAtOne: wrong: The first element of a is a[1]. \| right: Numbering begins with 0; a 1-based key needs a padding slot at index 0 or the index key-1.
- **T** (uneven-application rule): Points to LT: compute the index from the data, then read the table entry. Inconsistent application: 1 is subtracted from the key on some lookups but not on others, or the padding slot is counted as January.
- **N** (identity rule): Identity: a lookup table is an array whose element i holds a precomputed value or name for i, read by indexing.
- **S** (declarative rule): Declarative: build the table once (initializer or loop), e.g. String[] months = {"", "Jan", ..., "Dec"}; or H[i] = H[i-1] + 1.0/i; then use months[m] or H[i] in place of recomputing.
- **LT** (operational sequencing rule): Sequencing: the whole table is built before the first lookup. Each lookup evaluates the index expression, checks the bounds and reads one element.
- **OP** (evaluation / result rule): Result: months[m] is the name of month m for m = 1..12 (months[0] is the empty string); H[i] is the i-th harmonic number.
- **OS** (state-transition rule): State transition: a lookup changes nothing; only the building phase stores values (one element per step).
- **R** (composition rule (with a neighbour)): with indexing: The key itself is the index (months[m], rank[i]), so keys must fall in 0..length-1.
- **R** (composition rule (with a neighbour)): with space\_time\_tradeoff: Storing precomputed values trades memory for time: each value is computed once and then looked up.
- **P** (plan / role rule): Plan/role: the table is a fixed value (Sajaniemi). It replaces long if-else chains or repeated computation with one indexed read.
- **C** (conservation rule): Conservation: adding entries at the end keeps existing lookups valid. Removing the padding slot shifts every entry down one, so months[1] becomes Feb (off by one). Changing a stored value changes every lookup of it.
- **D** (error rule): rule broken: Keys must map to legal indices. (run-time exception)
- **D** (error rule): rule broken: The key-to-index mapping must match the table layout. (silent logic error)
- **X** (applicability rule): Applicability: use a table when the same values are needed many times for small integer keys. It is not effective for huge key ranges, for values needed only once, or for keys that are not small integers.

## How it is found in code and answers (reader block)

- **Aliases:** none
- **Code patterns:** `\b(?:String|int|double|char)\s*\[\]\s*\w+\s*=\s*\{(?=\s*[\"'])`, `\w+\s*\[\s*\w+\s*[%/]\s*\d+\s*\]`
- **Operator symbols:** none
- **Java types:** none

## The whole prerequisite chain

- **Everything it builds on (6):** `array_creation`, `array_declaration`, `array_initializer`, `data_structure`, `data_type`, `indexing`
- **Everything that builds on it (1):** `space_time_tradeoff`

## Every edge in this view and its exact edge logic (12)

All the edges drawn in the picture, in the order: prerequisite, parallel, misconception, error, has_level, contains.

**1. `array_initializer` &rarr; `lookup_table`** (prerequisite)

- **Exact edge logic:** A lookup table is usually an array of fixed values written as a literal and read by index.
- **Grounding:** book\_passage

**2. `indexing` &rarr; `lookup_table`** (prerequisite)

- **Exact edge logic:** A lookup table is read by index, a[i].
- **Grounding:** book\_passage
- **Composition rule (R) of `indexing` with `lookup_table`:** A lookup table uses a data value as the index (months[m]), so the data must lie in 0..length-1.
- **Composition rule (R) of `lookup_table` with `indexing`:** The key itself is the index (months[m], rank[i]), so keys must fall in 0..length-1.

**3. `lookup_table` &rarr; `space_time_tradeoff`** (prerequisite)

- **Exact edge logic:** Saving precomputed values in an array trades memory for time: each value is computed once and then looked up.
- **Grounding:** book\_passage
- **Composition rule (R) of `lookup_table` with `space_time_tradeoff`:** Storing precomputed values trades memory for time: each value is computed once and then looked up.
- **Composition rule (R) of `space_time_tradeoff` with `lookup_table`:** The lookup table is the stored space: each value is computed once and then read by index.

**4. `lookup_table` &rarr; `ArrayIndexStartsAtOne`** (misconception)

- **Exact edge logic (the wrong rule):** The first element of a is a[1].
- **Twin logic (the right rule):** Numbering begins with 0; the first element is a[0].
- **Role:** context

**5. `indexing` &rarr; `ArrayIndexStartsAtOne`** (misconception)

- **Exact edge logic (the wrong rule):** The first element of a is a[1].
- **Twin logic (the right rule):** Numbering begins with 0; the first element is a[0].
- **Role:** primary

**6. `lookup_table` &rarr; `lookup_table@L0`** (has_level)

- **Exact edge logic:** lookup table -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (3 ways).
  - **[0] everyday\_reading** (rule type E, folk-meaning rule): Folk meaning: everyday tables are numbered from 1 (month 1 is January) and are looked up by scanning. Java rule: array tables are 0-origin and are read directly by index, so either waste slot 0 (months[0] = "") or subtract 1 from the key.
  - **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `ArrayIndexStartsAtOne`: wrong rule: The first element of a is a[1]. Right rule: Numbering begins with 0; a 1-based key needs a padding slot at index 0 or the index key-1.
  - **[2] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `ArrayIndexStartsAtOne`: Points to LT: compute the index from the data, then read the table entry. Inconsistent application: 1 is subtracted from the key on some lookups but not on others, or the padding slot is counted as January. (here mixing in: "The first element of a is a[1]")

**7. `lookup_table` &rarr; `lookup_table@L1`** (has_level)

- **Exact edge logic:** lookup table -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).
  - **[0] names\_the\_element** (rule type N, identity rule): Identity: a lookup table is an array whose element i holds a precomputed value or name for i, read by indexing.
  - **[1] states\_the\_rule** (rule type S, declarative rule): Declarative: build the table once (initializer or loop), e.g. String[] months = {"", "Jan", ..., "Dec"}; or H[i] = H[i-1] + 1.0/i; then use months[m] or H[i] in place of recomputing.

**8. `lookup_table` &rarr; `lookup_table@L2`** (has_level)

- **Exact edge logic:** lookup table -&gt; L2 (Multistructural): the answer applies the rules of lookup table to every part of the code, in order (3 ways).
  - **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): Sequencing: the whole table is built before the first lookup. Each lookup evaluates the index expression, checks the bounds and reads one element.
  - **[1] output\_prediction** (rule type OP, evaluation / result rule): Result: months[m] is the name of month m for m = 1..12 (months[0] is the empty string); H[i] is the i-th harmonic number.
  - **[2] one\_step\_execution** (rule type OS, state-transition rule): State transition: a lookup changes nothing; only the building phase stores values (one element per step).

**9. `lookup_table` &rarr; `lookup_table@L3`** (has_level)

- **Exact edge logic:** lookup table -&gt; L3 (Relational): the answer relates the parts (3 ways).
  - **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): The key itself is the index (months[m], rank[i]), so keys must fall in 0..length-1.
  - **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Storing precomputed values trades memory for time: each value is computed once and then looked up.
  - **[2] purpose\_of\_the\_whole** (rule type P, plan / role rule): Plan/role: the table is a fixed value (Sajaniemi). It replaces long if-else chains or repeated computation with one indexed read.

**10. `lookup_table` &rarr; `lookup_table@L4`** (has_level)

- **Exact edge logic:** lookup table -&gt; L4 (Extended abstract): the answer reasons beyond the given code (4 ways).
  - **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `ArrayIndexStartsAtOne`: Conservation: adding entries at the end keeps existing lookups valid. Removing the padding slot shifts every entry down one, so months[1] becomes Feb (off by one). Changing a stored value changes every lookup of it.
  - **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Applicability: use a table when the same values are needed many times for small integer keys. It is not effective for huge key ranges, for values needed only once, or for keys that are not small integers.
  - **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: Keys must map to legal indices. Kind: run-time exception. Trigger class: a key outside the table, e.g. months[13] or months[0-1] (ArrayIndexOutOfBoundsException)
  - **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: The key-to-index mapping must match the table layout. Kind: silent logic error. Trigger class: a 1-based key used with a table that has no padding slot, so every lookup returns the next entry

**11. `topic1.4.e` &rarr; `lookup_table`** (contains)

- topic `topic1.4.e` contains `lookup_table`

**12. `topic1.4.e` &rarr; `space_time_tradeoff`** (contains)

- topic `topic1.4.e` contains `space_time_tradeoff`
