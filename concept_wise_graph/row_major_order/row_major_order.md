# Row-major and column-major order (`row_major_order`)

processing a 2-D array row by row (row-major) or column by column (column-major)

Section 1.4 1.4 Arrays, topic 1.4.g Two-dimensional arrays (ragged, matrix operations).

![The knowledge graph around row_major_order](row_major_order.png)

## At a glance

- **Needs first:** `nested_loops`, `two_dimensional_array`
- **Leads to:** nothing
- **Learned alongside:** nothing
- **Misconceptions:** none
- **Errors:** none
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 12 edges around this concept, each explained in the graph's own words.

## What it needs first (2)

A prerequisite edge means the other concept has to be understood before `row_major_order`.

### `nested_loops` comes before `row_major_order`

*a loop inside a loop*

Which loop is outside decides whether the entries are processed row by row or column by column.

- **Grounding:** book passage
- **How `row_major_order` combines with `nested_loops`:** Which loop is outside decides whether entries are processed row by row or column by column; the inner loop finishes for each outer value.
- **How `nested_loops` combines with `row_major_order`:** Which loop is outside decides the visiting order: row index outside gives row-major order, column index outside gives column-major order.

### `two_dimensional_array` comes before `row_major_order`

*an array of arrays (a[i][j])*

Row-major order visits a[i][j] row by row (outer loop over i); column-major order puts the column loop outside.

- **Grounding:** book passage
- **How `row_major_order` combines with `two_dimensional_array`:** Because a[i] is a row array, row-major order walks along each row array in turn; column-major jumps between row arrays at each step.
- **How `two_dimensional_array` combines with `row_major_order`:** Row-major order visits a[i][j] with the outer loop over rows i; column-major puts the loop over j outside.

## What it leads to (0)

These concepts need `row_major_order` first.

No concept has this one as a prerequisite.

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

L0 for Row-major and column-major order: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to Row-major and column-major order agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

Row-major and column-major order -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (1 way).

- **everyday reading** (folk-meaning rule): Folk meaning: tables are read left to right, top to bottom, as the only natural order, and 'row' and 'column' are easily swapped. Rule: the loop that is outside decides the order: an outer loop over rows i gives row-major order, an outer loop over columns j gives column-major order.

### L1: Unistructural / atom x text surface

L1 for Row-major and column-major order: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

Row-major and column-major order -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

- **names the element** (identity rule): Identity: row-major order processes a 2-D array row by row; column-major order processes it column by column.
- **states the rule** (declarative rule): Declarative: for (i &lt; M) { for (j &lt; N) ... a[i][j] } is row-major; for (j &lt; N) { for (i &lt; M) ... a[i][j] } is column-major. Both keep a[i][j] with i as the row.

### L2: Multistructural / block x execution / preoperational

L2 for Row-major and column-major order: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

Row-major and column-major order -&gt; L2 (Multistructural): the answer applies the rules of Row-major and column-major order to every part of the code, in order (3 ways).

- **line by line trace** (operational sequencing rule): Sequencing (row-major print): i = 0, j runs over 0..N-1 printing a[0][j], newline; i = 1, ... So a[0][0], a[0][1], ..., a[1][0], ... in that order.
- **output prediction** (evaluation / result rule): Result: row-major processing yields per-row results (row averages in column N, rows printed as lines); column-major yields per-column results (column averages in row M).
- **one step execution** (state-transition rule): State transition: each inner step processes one entry; each outer step completes one whole row (row-major) or column (column-major) and resets the per-row sum.

### L3: Relational / relations x function (concrete operational begins)

L3 for Row-major and column-major order: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

Row-major and column-major order -&gt; L3 (Relational): the answer relates the parts (3 ways).

- **relation to neighbour** (composition rule (with a neighbour)): Because a[i] is a row array, row-major order walks along each row array in turn; column-major jumps between row arrays at each step.
- **relation to neighbour** (composition rule (with a neighbour)): Which loop is outside decides whether entries are processed row by row or column by column; the inner loop finishes for each outer value.
- **purpose of the whole** (plan / role rule): Plan/role: choose the order that matches the result wanted, row-major for per-row results (and for printing), column-major for per-column results.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for Row-major and column-major order: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

Row-major and column-major order -&gt; L4 (Extended abstract): the answer reasons beyond the given code (4 ways).

- **predict a change** (conservation rule): Conservation: swapping the loops of an element-wise operation (copy, add) keeps the result and changes only the visiting order. For printing or per-row sums, swapping changes the output (transposed layout, column results).
- **transfer to a new program** (applicability rule): Applicability: use row-major by default in Java (rows are arrays; printing goes line by line). Use column-major when the result is per column, and remember that ragged arrays have no full columns.
- **diagnose an error** (error rule): rule broken: Each loop bound must match the index it controls (i &lt; M rows, j &lt; N columns). Kind: run-time exception. Trigger class: after swapping the loops the bounds are not swapped with them, so in a non-square array a[i][j] gets i up to N-1 (ArrayIndexOutOfBoundsException)
- **diagnose an error** (error rule): rule broken: Per-row or per-column accumulators must be reset for each outer pass. Kind: silent logic error. Trigger class: sum is declared before the outer loop, so each row average includes all earlier rows

## Same topic

`row_major_order` belongs to the topic **Two-dimensional arrays (ragged, matrix operations)** (`topic1.4.g`). The topic also contains: `matrix_operations`, `multidimensional_array`, `ragged_array`, `two_dimensional_array`.

## Rules of the concept (14)

- **folk-meaning rule:** Folk meaning: tables are read left to right, top to bottom, as the only natural order, and 'row' and 'column' are easily swapped. Rule: the loop that is outside decides the order: an outer loop over rows i gives row-major order, an outer loop over columns j gives column-major order.
- **uneven-application rule:** Points to LT: the inner loop runs through completely for each value of the outer loop. Inconsistent application: the trace advances the outer index after every inner step, or swaps which index belongs to which loop.
- **identity rule:** Identity: row-major order processes a 2-D array row by row; column-major order processes it column by column.
- **declarative rule:** Declarative: for (i &lt; M) { for (j &lt; N) ... a[i][j] } is row-major; for (j &lt; N) { for (i &lt; M) ... a[i][j] } is column-major. Both keep a[i][j] with i as the row.
- **operational sequencing rule:** Sequencing (row-major print): i = 0, j runs over 0..N-1 printing a[0][j], newline; i = 1, ... So a[0][0], a[0][1], ..., a[1][0], ... in that order.
- **evaluation / result rule:** Result: row-major processing yields per-row results (row averages in column N, rows printed as lines); column-major yields per-column results (column averages in row M).
- **state-transition rule:** State transition: each inner step processes one entry; each outer step completes one whole row (row-major) or column (column-major) and resets the per-row sum.
- **composition rule (with a neighbour):** with two\_dimensional\_array: Because a[i] is a row array, row-major order walks along each row array in turn; column-major jumps between row arrays at each step.
- **composition rule (with a neighbour):** with nested\_loops: Which loop is outside decides whether entries are processed row by row or column by column; the inner loop finishes for each outer value.
- **plan / role rule:** Plan/role: choose the order that matches the result wanted, row-major for per-row results (and for printing), column-major for per-column results.
- **conservation rule:** Conservation: swapping the loops of an element-wise operation (copy, add) keeps the result and changes only the visiting order. For printing or per-row sums, swapping changes the output (transposed layout, column results).
- **error rule:** rule broken: Each loop bound must match the index it controls (i &lt; M rows, j &lt; N columns). (run-time exception)
- **error rule:** rule broken: Per-row or per-column accumulators must be reset for each outer pass. (silent logic error)
- **applicability rule:** Applicability: use row-major by default in Java (rows are arrays; printing goes line by line). Use column-major when the result is per column, and remember that ragged arrays have no full columns.

## The whole prerequisite chain

- **Everything it builds on (23):** `arithmetic_operators`, `array_creation`, `array_declaration`, `array_initializer`, `boolean`, `boolean_expression`, `comparison_operators`, `data_structure`, `data_type`, `do_while_loop`, `expression`, `for_loop`, `identifier`, `indexing`, `literal`, `logical_operators`, `loop_control`, `loop_variable`, `nested_loops`, `primitive_type`, `two_dimensional_array`, `variable`, `while_loop`
- **Everything that builds on it (0):** nothing
