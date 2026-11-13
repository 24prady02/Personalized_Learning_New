# ragged_array (`ragged_array`)

a 2-D array whose rows have different lengths

Section 1.4 Arrays, topic 1.4.g Two-dimensional arrays (ragged, matrix operations).

![The knowledge graph around ragged_array](ragged_array.png)

## At a glance

- **Needs first:** `two_dimensional_array`
- **Leads to:** nothing
- **Learned alongside:** nothing
- **Misconceptions:** `NoJaggedArrays`, `RaggedRowsSameLength`
- **Errors:** none
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 16 edges around this concept, each explained in the graph's own words.

## What it needs first (1)

A prerequisite edge means the other concept has to be understood before `ragged_array`.

### `two_dimensional_array` comes before `ragged_array`

*an array of arrays (a[i][j])*

There is no requirement that all rows in a two-dimensional array have the same length; an array with rows of nonuniform length is known as a ragged array.

- **Grounding:** book passage
- **How `ragged_array` combines with `two_dimensional_array`:** Ragged arrays exist because a 2-D array is an array of arrays: each row is an independent 1-D array with its own length.
- **How `two_dimensional_array` combines with `ragged_array`:** Since each row is a separate array, rows may have different lengths; such arrays are ragged.

## What it leads to (0)

These concepts need `ragged_array` first.

No concept has this one as a prerequisite.

## Learned alongside (0)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

No parallel edge touches this concept.

## Misconceptions (2)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### NoJaggedArrays

- **Wrong rule:** multi-dimensional arrays must be rectangular
- **Right rule:** Each row a[i] is its own array, so rows can have different lengths a[i].length.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: Multi-dimensional arrays must be rectangular. Right rule: Each row a[i] is its own array, so rows can have different lengths a[i].length.
- **Also an edge from `transition_matrix`:** Every row of the transition matrix must be stored with the same length because 2-D arrays are always rectangular.
- **Also an edge from `two_dimensional_array`:** Every row of a 2-D array must have the same length.

### RaggedRowsSameLength

- **Wrong rule:** All rows of a 2-D array have the same length, so one N works for every row.
- **Right rule:** Rows may differ in length; use a[i].length for row i.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: All rows of a 2-D array have the same length, so one N works for every row. Right rule: Rows may differ in length; use a[i].length for row i.
- **Shows at level L0 as:** inconsistent trace: Points to LT: the inner bound a[i].length is re-evaluated for each row. Inconsistent application: the trace uses row 0's length (or N) for every row, sometimes over-running a short row and sometimes stopping early in a long one. (here mixing in: "All rows of a 2-D array have the same length, so one N works for every row")
- **Also an edge from `two_dimensional_array`:** All rows of a 2-D array have the same length, so one N works for every row.

## Errors (0)

An error edge states the rule that gets broken in a program, and the right rule.

The graph has no error edge from this concept.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for ragged array: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to ragged array agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

ragged array -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (4 ways).

- **everyday reading** (folk-meaning rule): Folk meaning: a 'table' has the same number of columns in every row, so one width N serves all rows. Java rule: each row is a separate array, so rows may have different lengths, and code must use a[i].length for row i.
- **misconception** (wrong rule / right rule; shows `RaggedRowsSameLength`): wrong rule: All rows of a 2-D array have the same length, so one N works for every row. Right rule: Rows may differ in length; use a[i].length for row i.
- **misconception** (wrong rule / right rule; shows `NoJaggedArrays`): wrong rule: Multi-dimensional arrays must be rectangular. Right rule: Each row a[i] is its own array, so rows can have different lengths a[i].length.
- **inconsistent trace** (uneven-application rule; shows `RaggedRowsSameLength`): Points to LT: the inner bound a[i].length is re-evaluated for each row. Inconsistent application: the trace uses row 0's length (or N) for every row, sometimes over-running a short row and sometimes stopping early in a long one. (here mixing in: "All rows of a 2-D array have the same length, so one N works for every row")

### L1: Unistructural / atom x text surface

L1 for ragged array: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

ragged array -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

- **names the element** (identity rule): Identity: a ragged array is a two-dimensional array whose rows have different (nonuniform) lengths.
- **states the rule** (declarative rule): Declarative: there is no requirement that rows have the same length. Process row i up to a[i].length: for (i &lt; a.length) for (j &lt; a[i].length).

### L2: Multistructural / block x execution / preoperational

L2 for ragged array: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

ragged array -&gt; L2 (Multistructural): the answer applies the rules of ragged array to every part of the code, in order (3 ways).

- **line by line trace** (operational sequencing rule): Sequencing: the outer loop runs i over 0..a.length-1; for each i the inner loop bound a[i].length is read for that row, and then j runs over 0..a[i].length-1.
- **output prediction** (evaluation / result rule): Result: rows of different widths, e.g. a Pascal's-triangle array whose row N has N+1 entries; a[i].length differs from row to row.
- **one step execution** (state-transition rule): State transition: creating a row with a[i] = new double[i+1] sets the length of that row only; element writes change one entry.

### L3: Relational / relations x function (concrete operational begins)

L3 for ragged array: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

ragged array -&gt; L3 (Relational): the answer relates the parts (2 ways).

- **relation to neighbour** (composition rule (with a neighbour)): Ragged arrays exist because a 2-D array is an array of arrays: each row is an independent 1-D array with its own length.
- **purpose of the whole** (plan / role rule): Plan/role: store triangular or uneven data (binomial coefficients, lists of varying length) without wasting space on unused entries.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for ragged array: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

ragged array -&gt; L4 (Extended abstract): the answer reasons beyond the given code (4 ways).

- **predict a change** (conservation rule; shows `RaggedRowsSameLength`): Conservation: code written with a[i].length also works for rectangular arrays, but code written with a fixed N breaks on ragged ones; each later solution should still work for the earlier cases.
- **transfer to a new program** (applicability rule): Applicability: use a ragged array when rows naturally differ in length. When all rows have equal length, a rectangular array with M and N is simpler, and the book normally uses that.
- **diagnose an error** (error rule): rule broken: Each row must be processed up to its own length. Kind: run-time exception. Trigger class: the inner loop uses N or a[0].length, and a shorter row is indexed past its end (ArrayIndexOutOfBoundsException)
- **diagnose an error** (error rule): rule broken: Each row must be processed up to its own length. Kind: silent logic error. Trigger class: the inner bound is shorter than a longer row, so its last entries are silently skipped

## Same topic

`ragged_array` belongs to the topic **Two-dimensional arrays (ragged, matrix operations)** (`topic1.4.g`). The topic also contains: `matrix_operations`, `multidimensional_array`, `row_major_order`, `two_dimensional_array`.

## Rules of the concept (15)

- **folk-meaning rule:** Folk meaning: a 'table' has the same number of columns in every row, so one width N serves all rows. Java rule: each row is a separate array, so rows may have different lengths, and code must use a[i].length for row i.
- **wrong rule / right rule:** RaggedRowsSameLength: wrong: All rows of a 2-D array have the same length, so one N works for every row. \| right: Rows may differ in length; use a[i].length for row i.
- **wrong rule / right rule:** NoJaggedArrays: wrong: Multi-dimensional arrays must be rectangular. \| right: Each row a[i] is its own array, so rows can have different lengths a[i].length.
- **uneven-application rule:** Points to LT: the inner bound a[i].length is re-evaluated for each row. Inconsistent application: the trace uses row 0's length (or N) for every row, sometimes over-running a short row and sometimes stopping early in a long one.
- **identity rule:** Identity: a ragged array is a two-dimensional array whose rows have different (nonuniform) lengths.
- **declarative rule:** Declarative: there is no requirement that rows have the same length. Process row i up to a[i].length: for (i &lt; a.length) for (j &lt; a[i].length).
- **operational sequencing rule:** Sequencing: the outer loop runs i over 0..a.length-1; for each i the inner loop bound a[i].length is read for that row, and then j runs over 0..a[i].length-1.
- **evaluation / result rule:** Result: rows of different widths, e.g. a Pascal's-triangle array whose row N has N+1 entries; a[i].length differs from row to row.
- **state-transition rule:** State transition: creating a row with a[i] = new double[i+1] sets the length of that row only; element writes change one entry.
- **composition rule (with a neighbour):** with two\_dimensional\_array: Ragged arrays exist because a 2-D array is an array of arrays: each row is an independent 1-D array with its own length.
- **plan / role rule:** Plan/role: store triangular or uneven data (binomial coefficients, lists of varying length) without wasting space on unused entries.
- **conservation rule:** Conservation: code written with a[i].length also works for rectangular arrays, but code written with a fixed N breaks on ragged ones; each later solution should still work for the earlier cases.
- **error rule:** rule broken: Each row must be processed up to its own length. (run-time exception)
- **error rule:** rule broken: Each row must be processed up to its own length. (silent logic error)
- **applicability rule:** Applicability: use a ragged array when rows naturally differ in length. When all rows have equal length, a rectangular array with M and N is simpler, and the book normally uses that.

## The whole prerequisite chain

- **Everything it builds on (7):** `array_creation`, `array_declaration`, `array_initializer`, `data_structure`, `data_type`, `indexing`, `two_dimensional_array`
- **Everything that builds on it (0):** nothing
