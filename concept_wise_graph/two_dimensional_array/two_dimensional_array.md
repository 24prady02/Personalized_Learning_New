# two_dimensional_array (`two_dimensional_array`)

an array of arrays (a[i][j])

Section 1.4 Arrays, topic 1.4.g Two-dimensional arrays (ragged, matrix operations).

![The knowledge graph around two_dimensional_array](two_dimensional_array.png)

## At a glance

- **Needs first:** `indexing`
- **Leads to:** `input_graph`, `matrix_operations`, `multidimensional_array`, `power_method`, `ragged_array`, `row_major_order`, `transition_matrix`
- **Learned alongside:** nothing
- **Misconceptions:** `ArrayElementTypeRepeats`, `ArrayRankIsLength`, `ColumnLikeRow`, `MultidimensionalArray`, `NoJaggedArrays`, `OnlyInnermostArrayElements`, `RaggedRowsSameLength`
- **Errors:** none
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 31 edges around this concept. The edge logic, the wrong and right rules and the exact rules of the ways are copied word for word from the graph.

## To work on (0)

Nothing is missing for this concept.

## What it needs first (1)

A prerequisite edge means the other concept has to be understood before `two_dimensional_array`.

### `indexing` comes before `two_dimensional_array`

*a[i] -- 0-based access*

- **Edge:** `pre:indexing->two_dimensional_array`
- **Exact edge logic:** A 1-D array uses one index a[i]; a 2-D array uses two, a[i][j], where the first index chooses the row array.
- **Grounding:** book\_passage
- **Composition rule (R) of `two_dimensional_array` with `indexing`:** A 2-D array uses two indices, and the first chooses the row array: a[i][j] is (a[i])[j].
- **Composition rule (R) of `indexing` with `two_dimensional_array`:** a[i] on a 2-D array yields row i (itself a 1-D array), and a[i][j] then indexes into that row.

## What it leads to (7)

These concepts need `two_dimensional_array` first.

### `two_dimensional_array` comes before `input_graph`

*read the page links from input*

- **Edge:** `pre:two_dimensional_array->input_graph`
- **Exact edge logic:** The links read from input are counted in a two-dimensional array, counts[i][j].
- **Grounding:** book\_passage

### `two_dimensional_array` comes before `matrix_operations`

*matrix addition and multiplication with nested loops*

- **Edge:** `pre:two_dimensional_array->matrix_operations`
- **Exact edge logic:** Matrix operations index a[i][j] in nested loops.
- **Grounding:** book\_passage
- **Composition rule (R) of `two_dimensional_array` with `matrix_operations`:** Matrix operations index a[i][j] in nested loops (two for addition, three for multiplication).
- **Composition rule (R) of `matrix_operations` with `two_dimensional_array`:** Matrices are stored as 2-D arrays and read entry by entry as a[i][j].

### `two_dimensional_array` comes before `multidimensional_array`

*arrays with three or more indices*

- **Edge:** `pre:two_dimensional_array->multidimensional_array`
- **Exact edge logic:** Higher dimensions generalise 2-D arrays.
- **Grounding:** book\_passage
- **Composition rule (R) of `two_dimensional_array` with `multidimensional_array`:** The same notation extends to any number of dimensions: a[i][j][k] for double[][][].
- **Composition rule (R) of `multidimensional_array` with `two_dimensional_array`:** A 3-D array generalizes 2-D: a[i] is itself a 2-D array, and the same declaration, creation and indexing rules apply one level deeper.

### `two_dimensional_array` comes before `power_method`

*repeated vector-matrix multiplication to compute page ranks*

- **Edge:** `pre:two_dimensional_array->power_method`
- **Exact edge logic:** The power method multiplies the rank vector by the transition matrix, stored as a two-dimensional array p[i][j].
- **Grounding:** book\_passage

### `two_dimensional_array` comes before `ragged_array`

*a 2-D array whose rows have different lengths*

- **Edge:** `pre:two_dimensional_array->ragged_array`
- **Exact edge logic:** There is no requirement that all rows in a two-dimensional array have the same length; an array with rows of nonuniform length is known as a ragged array.
- **Grounding:** book\_passage
- **Composition rule (R) of `two_dimensional_array` with `ragged_array`:** Since each row is a separate array, rows may have different lengths; such arrays are ragged.
- **Composition rule (R) of `ragged_array` with `two_dimensional_array`:** Ragged arrays exist because a 2-D array is an array of arrays: each row is an independent 1-D array with its own length.

### `two_dimensional_array` comes before `row_major_order`

*Row-major and column-major order: processing a 2-D array row by row (row-major) or column by column (column-major)*

- **Edge:** `pre:two_dimensional_array->row_major_order`
- **Exact edge logic:** Row-major order visits a[i][j] row by row (outer loop over i); column-major order puts the column loop outside.
- **Grounding:** book\_passage
- **Composition rule (R) of `two_dimensional_array` with `row_major_order`:** Row-major order visits a[i][j] with the outer loop over rows i; column-major puts the loop over j outside.
- **Composition rule (R) of `row_major_order` with `two_dimensional_array`:** Because a[i] is a row array, row-major order walks along each row array in turn; column-major jumps between row arrays at each step.

### `two_dimensional_array` comes before `transition_matrix`

*a 2-D array of move probabilities (rows sum to 1)*

- **Edge:** `pre:two_dimensional_array->transition_matrix`
- **Exact edge logic:** The transition matrix is a 2-D double array p[i][j], with one row array per page.
- **Grounding:** book\_passage
- **Composition rule (R) of `two_dimensional_array` with `transition_matrix`:** The transition matrix is a 2-D double array p[i][j] with one row per page; each row holds a probability distribution.
- **Composition rule (R) of `transition_matrix` with `two_dimensional_array`:** The matrix is double[N][N]: p[i] is the row array for page i and p[i][j] an element; indices must be in 0..N-1 and the first index is the row (from-page).

## Learned alongside (0)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

No parallel edge touches this concept.

## Misconceptions (7)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### ArrayElementTypeRepeats

- **Edge:** `two_dimensional_array` &rarr; `ArrayElementTypeRepeats` (misconception)
- **Exact edge logic (the wrong rule):** A 2-D int array type is written int[] int[].
- **Twin logic (the right rule):** It is written int[][].
- **Wrong belief (on the node):** A 2-D int array type is written int[] int[].
- **Correct rule (on the node):** It is written int[][].
- **Provenance:** published
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [2] misconception, exact rule:** wrong rule: A 2-D int array type is written int[] int[]. Right rule: It is written int[][]: one element type followed by one bracket pair per dimension.

### ArrayRankIsLength

- **Edge:** `two_dimensional_array` &rarr; `ArrayRankIsLength` (misconception)
- **Exact edge logic (the wrong rule):** The number of dimensions of an array is its length.
- **Twin logic (the right rule):** Rank (number of dimensions) and length are different.
- **Wrong belief (on the node):** The number of dimensions of an array is its length.
- **Correct rule (on the node):** Rank (number of dimensions) and length are different.
- **Provenance:** published
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [6] misconception, exact rule:** wrong rule: The number of dimensions of an array is its length. Right rule: Rank (number of bracket pairs) and length (number of elements, a.length) are different; a double[][] of size 10-by-3 has a.length == 10.
- **Edge `multidimensional_array` &rarr; `ArrayRankIsLength`, exact edge logic:** The number of dimensions of an array is its length. **Twin logic:** Rank (number of dimensions) and length are different. (role: context)

### ColumnLikeRow

- **Edge:** `two_dimensional_array` &rarr; `ColumnLikeRow` (misconception)
- **Exact edge logic (the wrong rule):** Column j of a 2-D array can be picked out as a 1-D array, just like row a[i].
- **Twin logic (the right rule):** a[i] is row i (a 1-D array), but there is no expression for a column; loop over i and use a[i][j].
- **Wrong belief (on the node):** Column j of a 2-D array can be picked out as a 1-D array, just like row a[i].
- **Correct rule (on the node):** a[i] is row i (a 1-D array), but there is no expression for a column; loop over i and use a[i][j].
- **Provenance:** textbook
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [3] misconception, exact rule:** wrong rule: Column j of a 2-D array can be picked out as a 1-D array, just like row a[i]. Right rule: a[i] is row i (a 1-D array), but there is no expression for a column; loop over i and use a[i][j].
- **Edge `matrix_operations` &rarr; `ColumnLikeRow`, exact edge logic:** Column j of a 2-D array can be picked out as a 1-D array, just like row a[i]. **Twin logic:** a[i] is row i (a 1-D array), but there is no expression for a column; loop over i and use a[i][j]. (role: context)

### MultidimensionalArray

- **Edge:** `two_dimensional_array` &rarr; `MultidimensionalArray` (misconception)
- **Exact edge logic (the wrong rule):** int[m][n] is one block of m \* n values, so a[i] on its own means nothing.
- **Twin logic (the right rule):** A 2-D array is an array of m row arrays, so a[i] is a 1-D array of length n.
- **Wrong belief (on the node):** a 2-D array is one thing, not an array of arrays
- **Correct rule (on the node):** A 2-D array is an array of m row arrays, so a[i] is a 1-D array of length n.
- **Provenance:** published
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [4] misconception, exact rule:** wrong rule: A 2-D array is one thing, not an array of arrays. Right rule: A 2-D array is an array of m row arrays, so a[i] is a 1-D array of length n.
- **Edge `transition_matrix` &rarr; `MultidimensionalArray`, exact edge logic:** The transition matrix is one block of n \* n numbers, so p[i] on its own means nothing. **Twin logic:** p[i] is the row array of page i, holding the probabilities of moving from page i to every page. (role: context)

### NoJaggedArrays

- **Edge:** `two_dimensional_array` &rarr; `NoJaggedArrays` (misconception)
- **Exact edge logic (the wrong rule):** Every row of a 2-D array must have the same length.
- **Twin logic (the right rule):** Each row a[i] is its own array, so rows can have different lengths a[i].length.
- **Wrong belief (on the node):** multi-dimensional arrays must be rectangular
- **Correct rule (on the node):** Each row a[i] is its own array, so rows can have different lengths a[i].length.
- **Provenance:** published
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [8] misconception, exact rule:** wrong rule: Multi-dimensional arrays must be rectangular. Right rule: Each row a[i] is its own array, so rows can have different lengths a[i].length.
- **Edge `ragged_array` &rarr; `NoJaggedArrays`, exact edge logic:** multi-dimensional arrays must be rectangular **Twin logic:** Each row a[i] is its own array, so rows can have different lengths a[i].length. (role: primary)
- **Edge `transition_matrix` &rarr; `NoJaggedArrays`, exact edge logic:** Every row of the transition matrix must be stored with the same length because 2-D arrays are always rectangular. **Twin logic:** Each p[i] is its own row array; the surfer's matrix is square only because every page has a row of n probabilities. (role: context)

### OnlyInnermostArrayElements

- **Edge:** `two_dimensional_array` &rarr; `OnlyInnermostArrayElements` (misconception)
- **Exact edge logic (the wrong rule):** Only single elements a[i][j] can be used, not whole rows a[i].
- **Twin logic (the right rule):** a[i] gives the whole row i, which can be used like any 1-D array.
- **Wrong belief (on the node):** only the innermost elements are accessible
- **Correct rule (on the node):** a[i] gives the whole row i, which can be used like any 1-D array.
- **Provenance:** published
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [1] misconception, exact rule:** wrong rule: Only the innermost elements are accessible. Right rule: a[i] gives the whole row i, which can be used like any 1-D array.
- **L0 way [5] inconsistent\_trace, exact rule:** Points to LT: a[i][j] is evaluated as (a[i])[j], first the row and then the element in it. Inconsistent application: the first index is taken as the row on some steps and as the column on others. (here mixing in: "only the innermost elements are accessible")

### RaggedRowsSameLength

- **Edge:** `two_dimensional_array` &rarr; `RaggedRowsSameLength` (misconception)
- **Exact edge logic (the wrong rule):** All rows of a 2-D array have the same length, so one N works for every row.
- **Twin logic (the right rule):** Rows may differ in length; use a[i].length for row i.
- **Wrong belief (on the node):** All rows of a 2-D array have the same length, so one N works for every row.
- **Correct rule (on the node):** Rows may differ in length; use a[i].length for row i.
- **Provenance:** textbook
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [7] misconception, exact rule:** wrong rule: All rows of a 2-D array have the same length, so one N works for every row. Right rule: Rows may differ in length; use a[i].length for row i.
- **Edge `ragged_array` &rarr; `RaggedRowsSameLength`, exact edge logic:** All rows of a 2-D array have the same length, so one N works for every row. **Twin logic:** Rows may differ in length; use a[i].length for row i. (role: primary)

## Errors (0)

An error edge states the rule that gets broken in a program, and the right rule.

The graph has no error edge from this concept.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for two dimensional array: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to two dimensional array agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

- **Edge:** `two_dimensional_array` &rarr; `two_dimensional_array@L0` (has_level)
- **Exact edge logic:** two dimensional array -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (9 ways).

Ways (9), each with its exact rule:

- **[0] everyday\_reading** (rule type E, folk-meaning rule): Folk meaning: a table or matrix is one grid in which rows and columns are symmetric, so a column should be as easy to pick out as a row. Java rule: a 2-D array is an array of row arrays; a[i] is row i, a[i][j] an element, and there is no expression for a column.
- **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `OnlyInnermostArrayElements`: wrong rule: Only the innermost elements are accessible. Right rule: a[i] gives the whole row i, which can be used like any 1-D array.
- **[2] misconception** (rule type M, wrong rule / right rule) &rarr; `ArrayElementTypeRepeats`: wrong rule: A 2-D int array type is written int[] int[]. Right rule: It is written int[][]: one element type followed by one bracket pair per dimension.
- **[3] misconception** (rule type M, wrong rule / right rule) &rarr; `ColumnLikeRow`: wrong rule: Column j of a 2-D array can be picked out as a 1-D array, just like row a[i]. Right rule: a[i] is row i (a 1-D array), but there is no expression for a column; loop over i and use a[i][j].
- **[4] misconception** (rule type M, wrong rule / right rule) &rarr; `MultidimensionalArray`: wrong rule: A 2-D array is one thing, not an array of arrays. Right rule: A 2-D array is an array of m row arrays, so a[i] is a 1-D array of length n.
- **[5] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `OnlyInnermostArrayElements`: Points to LT: a[i][j] is evaluated as (a[i])[j], first the row and then the element in it. Inconsistent application: the first index is taken as the row on some steps and as the column on others. (here mixing in: "only the innermost elements are accessible")
- **[6] misconception** (rule type M, wrong rule / right rule) &rarr; `ArrayRankIsLength`: wrong rule: The number of dimensions of an array is its length. Right rule: Rank (number of bracket pairs) and length (number of elements, a.length) are different; a double[][] of size 10-by-3 has a.length == 10.
- **[7] misconception** (rule type M, wrong rule / right rule) &rarr; `RaggedRowsSameLength`: wrong rule: All rows of a 2-D array have the same length, so one N works for every row. Right rule: Rows may differ in length; use a[i].length for row i.
- **[8] misconception** (rule type M, wrong rule / right rule) &rarr; `NoJaggedArrays`: wrong rule: Multi-dimensional arrays must be rectangular. Right rule: Each row a[i] is its own array, so rows can have different lengths a[i].length.

### L1: Unistructural / atom x text surface

L1 for two dimensional array: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

- **Edge:** `two_dimensional_array` &rarr; `two_dimensional_array@L1` (has_level)
- **Exact edge logic:** two dimensional array -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

Ways (2), each with its exact rule:

- **[0] names\_the\_element** (rule type N, identity rule): Identity: a two-dimensional array, an array of arrays used to represent a table or matrix with M rows and N columns.
- **[1] states\_the\_rule** (rule type S, declarative rule): Declarative: declare double[][] a; create with new double[M][N] (rows first, then columns); refer to row i, column j as a[i][j]. Entries start at 0 (numbers) or false (boolean).

### L2: Multistructural / block x execution / preoperational

L2 for two dimensional array: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

- **Edge:** `two_dimensional_array` &rarr; `two_dimensional_array@L2` (has_level)
- **Exact edge logic:** two dimensional array -&gt; L2 (Multistructural): the answer applies the rules of two dimensional array to every part of the code, in order (3 ways).

Ways (3), each with its exact rule:

- **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): Sequencing: new double[M][N] creates an array of M references and then M row arrays of N defaults. a[i][j] evaluates a[i] (checked against a.length = M) and then [j] (checked against a[i].length).
- **[1] output\_prediction** (rule type OP, evaluation / result rule): Result: a[i][j] has the element type; a.length is the number of rows M; a[i].length is the length of row i; a[i] is a double[] row.
- **[2] one\_step\_execution** (rule type OS, state-transition rule): State transition: a[i][j] = v changes one element of row i; a[i] = new double[K] replaces the whole row i with a new array; other rows are untouched.

### L3: Relational / relations x function (concrete operational begins)

L3 for two dimensional array: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

- **Edge:** `two_dimensional_array` &rarr; `two_dimensional_array@L3` (has_level)
- **Exact edge logic:** two dimensional array -&gt; L3 (Relational): the answer relates the parts (7 ways).

Ways (7), each with its exact rule:

- **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): The transition matrix is a 2-D double array p[i][j] with one row per page; each row holds a probability distribution.
- **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): A 2-D array uses two indices, and the first chooses the row array: a[i][j] is (a[i])[j].
- **[2] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Since each row is a separate array, rows may have different lengths; such arrays are ragged.
- **[3] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Matrix operations index a[i][j] in nested loops (two for addition, three for multiplication).
- **[4] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): The same notation extends to any number of dimensions: a[i][j][k] for double[][][].
- **[5] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Row-major order visits a[i][j] with the outer loop over rows i; column-major puts the loop over j outside.
- **[6] purpose\_of\_the\_whole** (rule type P, plan / role rule): Plan/role: store tables, matrices, grids and images indexed by row and column (grades by student and test, lattice intersections, pixels).

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for two dimensional array: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

- **Edge:** `two_dimensional_array` &rarr; `two_dimensional_array@L4` (has_level)
- **Exact edge logic:** two dimensional array -&gt; L4 (Extended abstract): the answer reasons beyond the given code (4 ways).

Ways (4), each with its exact rule:

- **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `OnlyInnermostArrayElements`: Conservation: swapping the loop order for an element-wise operation keeps the result but changes the processing order. Swapping the indices (a[j][i]) transposes and goes out of bounds when M != N.
- **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Applicability: use a 2-D array for data naturally indexed by two integers (rows by columns). Use a ragged array when rows differ, a 1-D array when one index suffices, and higher dimensions for 3-D models.
- **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: Indices must be within each dimension (i &lt; a.length, j &lt; a[i].length). Kind: run-time exception. Trigger class: row and column bounds swapped in a non-square M-by-N array, or j bounded by N on a shorter ragged row (ArrayIndexOutOfBoundsException)
- **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: The type is written with one bracket pair per dimension. Kind: compile-time. Trigger class: int[] int[] a; or assigning an int[] where an int[][] is required (incompatible types)

## Same topic

`two_dimensional_array` belongs to the topic **Two-dimensional arrays (ragged, matrix operations)** (`topic1.4.g`). The topic also contains: `matrix_operations`, `multidimensional_array`, `ragged_array`, `row_major_order`.

## Rules of the concept (25)

- **Book** (SW-1e, p. 103 (pdf 113)): "Java represents a two-dimensional array as an array of arrays."
- **Book** (OT-Arrays, ): "In the Java programming language, a multidimensional array is an array whose components are themselves arrays."
- **Book** (SW-1.4, ): "Java represents a two-dimensional array as an array of arrays ... we can use the code a[i] to refer to the ith row (which is a one-dimensional array)."
- **E** (folk-meaning rule): Folk meaning: a table or matrix is one grid in which rows and columns are symmetric, so a column should be as easy to pick out as a row. Java rule: a 2-D array is an array of row arrays; a[i] is row i, a[i][j] an element, and there is no expression for a column.
- **M** (wrong rule / right rule): ArrayElementTypeRepeats: wrong: A 2-D int array type is written int[] int[]. \| right: It is written int[][]: one element type followed by one bracket pair per dimension.
- **M** (wrong rule / right rule): ArrayRankIsLength: wrong: The number of dimensions of an array is its length. \| right: Rank (number of bracket pairs) and length (number of elements, a.length) are different; a double[][] of size 10-by-3 has a.length == 10.
- **M** (wrong rule / right rule): OnlyInnermostArrayElements: wrong: Only the innermost elements are accessible. \| right: a[i] gives the whole row i, which can be used like any 1-D array.
- **M** (wrong rule / right rule): ColumnLikeRow: wrong: Column j of a 2-D array can be picked out as a 1-D array, just like row a[i]. \| right: a[i] is row i (a 1-D array), but there is no expression for a column; loop over i and use a[i][j].
- **M** (wrong rule / right rule): RaggedRowsSameLength: wrong: All rows of a 2-D array have the same length, so one N works for every row. \| right: Rows may differ in length; use a[i].length for row i.
- **M** (wrong rule / right rule): MultidimensionalArray: wrong: A 2-D array is one thing, not an array of arrays. \| right: A 2-D array is an array of m row arrays, so a[i] is a 1-D array of length n.
- **M** (wrong rule / right rule): NoJaggedArrays: wrong: Multi-dimensional arrays must be rectangular. \| right: Each row a[i] is its own array, so rows can have different lengths a[i].length.
- **T** (uneven-application rule): Points to LT: a[i][j] is evaluated as (a[i])[j], first the row and then the element in it. Inconsistent application: the first index is taken as the row on some steps and as the column on others.
- **N** (identity rule): Identity: a two-dimensional array, an array of arrays used to represent a table or matrix with M rows and N columns.
- **S** (declarative rule): Declarative: declare double[][] a; create with new double[M][N] (rows first, then columns); refer to row i, column j as a[i][j]. Entries start at 0 (numbers) or false (boolean).
- **LT** (operational sequencing rule): Sequencing: new double[M][N] creates an array of M references and then M row arrays of N defaults. a[i][j] evaluates a[i] (checked against a.length = M) and then [j] (checked against a[i].length).
- **OP** (evaluation / result rule): Result: a[i][j] has the element type; a.length is the number of rows M; a[i].length is the length of row i; a[i] is a double[] row.
- **OS** (state-transition rule): State transition: a[i][j] = v changes one element of row i; a[i] = new double[K] replaces the whole row i with a new array; other rows are untouched.
- **R** (composition rule (with a neighbour)): with transition\_matrix: The transition matrix is a 2-D double array p[i][j] with one row per page; each row holds a probability distribution.
- **R** (composition rule (with a neighbour)): with indexing: A 2-D array uses two indices, and the first chooses the row array: a[i][j] is (a[i])[j].
- **R** (composition rule (with a neighbour)): with ragged\_array: Since each row is a separate array, rows may have different lengths; such arrays are ragged.
- **R** (composition rule (with a neighbour)): with matrix\_operations: Matrix operations index a[i][j] in nested loops (two for addition, three for multiplication).
- **R** (composition rule (with a neighbour)): with multidimensional\_array: The same notation extends to any number of dimensions: a[i][j][k] for double[][][].
- **R** (composition rule (with a neighbour)): with row\_major\_order: Row-major order visits a[i][j] with the outer loop over rows i; column-major puts the loop over j outside.
- **P** (plan / role rule): Plan/role: store tables, matrices, grids and images indexed by row and column (grades by student and test, lattice intersections, pixels).
- **C** (conservation rule): Conservation: swapping the loop order for an element-wise operation keeps the result but changes the processing order. Swapping the indices (a[j][i]) transposes and goes out of bounds when M != N.
- **D** (error rule): rule broken: Indices must be within each dimension (i &lt; a.length, j &lt; a[i].length). (run-time exception)
- **D** (error rule): rule broken: The type is written with one bracket pair per dimension. (compile-time)
- **X** (applicability rule): Applicability: use a 2-D array for data naturally indexed by two integers (rows by columns). Use a ragged array when rows differ, a 1-D array when one index suffices, and higher dimensions for 3-D models.

## How it is found in code and answers (reader block)

- **Aliases:** 2d array, two dimensional, matrix, row, column
- **Code patterns:** `\[\s*\]\s*\[\s*\]`, `\w\s*\[[^\]]+\]\s*\[[^\]]+\]`, `\bnew\s+\w+\s*\[[^\]]*\]\s*\[[^\]]*\]`
- **Operator symbols:** none
- **Java types:** none

## The whole prerequisite chain

- **Everything it builds on (6):** `array_creation`, `array_declaration`, `array_initializer`, `data_structure`, `data_type`, `indexing`
- **Everything that builds on it (15):** `convergence_rate`, `dangling_pages`, `frequency_counting`, `input_graph`, `markov_chain`, `matrix_operations`, `multidimensional_array`, `normalization`, `power_method`, `ragged_array`, `random_move`, `row_major_order`, `simulation_loop`, `transition_matrix`, `two_models`

## Every edge in this view and its exact edge logic (31)

All the edges drawn in the picture, in the order: prerequisite, parallel, misconception, error, has_level, contains.

**1. `indexing` &rarr; `two_dimensional_array`** (prerequisite)

- **Exact edge logic:** A 1-D array uses one index a[i]; a 2-D array uses two, a[i][j], where the first index chooses the row array.
- **Grounding:** book\_passage
- **Composition rule (R) of `indexing` with `two_dimensional_array`:** a[i] on a 2-D array yields row i (itself a 1-D array), and a[i][j] then indexes into that row.
- **Composition rule (R) of `two_dimensional_array` with `indexing`:** A 2-D array uses two indices, and the first chooses the row array: a[i][j] is (a[i])[j].

**2. `two_dimensional_array` &rarr; `input_graph`** (prerequisite)

- **Exact edge logic:** The links read from input are counted in a two-dimensional array, counts[i][j].
- **Grounding:** book\_passage

**3. `two_dimensional_array` &rarr; `matrix_operations`** (prerequisite)

- **Exact edge logic:** Matrix operations index a[i][j] in nested loops.
- **Grounding:** book\_passage
- **Composition rule (R) of `two_dimensional_array` with `matrix_operations`:** Matrix operations index a[i][j] in nested loops (two for addition, three for multiplication).
- **Composition rule (R) of `matrix_operations` with `two_dimensional_array`:** Matrices are stored as 2-D arrays and read entry by entry as a[i][j].

**4. `two_dimensional_array` &rarr; `multidimensional_array`** (prerequisite)

- **Exact edge logic:** Higher dimensions generalise 2-D arrays.
- **Grounding:** book\_passage
- **Composition rule (R) of `two_dimensional_array` with `multidimensional_array`:** The same notation extends to any number of dimensions: a[i][j][k] for double[][][].
- **Composition rule (R) of `multidimensional_array` with `two_dimensional_array`:** A 3-D array generalizes 2-D: a[i] is itself a 2-D array, and the same declaration, creation and indexing rules apply one level deeper.

**5. `two_dimensional_array` &rarr; `power_method`** (prerequisite)

- **Exact edge logic:** The power method multiplies the rank vector by the transition matrix, stored as a two-dimensional array p[i][j].
- **Grounding:** book\_passage

**6. `two_dimensional_array` &rarr; `ragged_array`** (prerequisite)

- **Exact edge logic:** There is no requirement that all rows in a two-dimensional array have the same length; an array with rows of nonuniform length is known as a ragged array.
- **Grounding:** book\_passage
- **Composition rule (R) of `two_dimensional_array` with `ragged_array`:** Since each row is a separate array, rows may have different lengths; such arrays are ragged.
- **Composition rule (R) of `ragged_array` with `two_dimensional_array`:** Ragged arrays exist because a 2-D array is an array of arrays: each row is an independent 1-D array with its own length.

**7. `two_dimensional_array` &rarr; `row_major_order`** (prerequisite)

- **Exact edge logic:** Row-major order visits a[i][j] row by row (outer loop over i); column-major order puts the column loop outside.
- **Grounding:** book\_passage
- **Composition rule (R) of `two_dimensional_array` with `row_major_order`:** Row-major order visits a[i][j] with the outer loop over rows i; column-major puts the loop over j outside.
- **Composition rule (R) of `row_major_order` with `two_dimensional_array`:** Because a[i] is a row array, row-major order walks along each row array in turn; column-major jumps between row arrays at each step.

**8. `two_dimensional_array` &rarr; `transition_matrix`** (prerequisite)

- **Exact edge logic:** The transition matrix is a 2-D double array p[i][j], with one row array per page.
- **Grounding:** book\_passage
- **Composition rule (R) of `two_dimensional_array` with `transition_matrix`:** The transition matrix is a 2-D double array p[i][j] with one row per page; each row holds a probability distribution.
- **Composition rule (R) of `transition_matrix` with `two_dimensional_array`:** The matrix is double[N][N]: p[i] is the row array for page i and p[i][j] an element; indices must be in 0..N-1 and the first index is the row (from-page).

**9. `two_dimensional_array` &rarr; `ArrayElementTypeRepeats`** (misconception)

- **Exact edge logic (the wrong rule):** A 2-D int array type is written int[] int[].
- **Twin logic (the right rule):** It is written int[][].
- **Role:** primary

**10. `two_dimensional_array` &rarr; `ArrayRankIsLength`** (misconception)

- **Exact edge logic (the wrong rule):** The number of dimensions of an array is its length.
- **Twin logic (the right rule):** Rank (number of dimensions) and length are different.
- **Role:** primary

**11. `two_dimensional_array` &rarr; `ColumnLikeRow`** (misconception)

- **Exact edge logic (the wrong rule):** Column j of a 2-D array can be picked out as a 1-D array, just like row a[i].
- **Twin logic (the right rule):** a[i] is row i (a 1-D array), but there is no expression for a column; loop over i and use a[i][j].
- **Role:** primary

**12. `two_dimensional_array` &rarr; `MultidimensionalArray`** (misconception)

- **Exact edge logic (the wrong rule):** int[m][n] is one block of m \* n values, so a[i] on its own means nothing.
- **Twin logic (the right rule):** A 2-D array is an array of m row arrays, so a[i] is a 1-D array of length n.
- **Role:** primary

**13. `two_dimensional_array` &rarr; `NoJaggedArrays`** (misconception)

- **Exact edge logic (the wrong rule):** Every row of a 2-D array must have the same length.
- **Twin logic (the right rule):** Each row a[i] is its own array, so rows can have different lengths a[i].length.
- **Role:** context

**14. `two_dimensional_array` &rarr; `OnlyInnermostArrayElements`** (misconception)

- **Exact edge logic (the wrong rule):** Only single elements a[i][j] can be used, not whole rows a[i].
- **Twin logic (the right rule):** a[i] gives the whole row i, which can be used like any 1-D array.
- **Role:** primary

**15. `two_dimensional_array` &rarr; `RaggedRowsSameLength`** (misconception)

- **Exact edge logic (the wrong rule):** All rows of a 2-D array have the same length, so one N works for every row.
- **Twin logic (the right rule):** Rows may differ in length; use a[i].length for row i.
- **Role:** context

**16. `matrix_operations` &rarr; `ColumnLikeRow`** (misconception)

- **Exact edge logic (the wrong rule):** Column j of a 2-D array can be picked out as a 1-D array, just like row a[i].
- **Twin logic (the right rule):** a[i] is row i (a 1-D array), but there is no expression for a column; loop over i and use a[i][j].
- **Role:** context

**17. `multidimensional_array` &rarr; `ArrayRankIsLength`** (misconception)

- **Exact edge logic (the wrong rule):** The number of dimensions of an array is its length.
- **Twin logic (the right rule):** Rank (number of dimensions) and length are different.
- **Role:** context

**18. `ragged_array` &rarr; `NoJaggedArrays`** (misconception)

- **Exact edge logic (the wrong rule):** multi-dimensional arrays must be rectangular
- **Twin logic (the right rule):** Each row a[i] is its own array, so rows can have different lengths a[i].length.
- **Role:** primary

**19. `ragged_array` &rarr; `RaggedRowsSameLength`** (misconception)

- **Exact edge logic (the wrong rule):** All rows of a 2-D array have the same length, so one N works for every row.
- **Twin logic (the right rule):** Rows may differ in length; use a[i].length for row i.
- **Role:** primary

**20. `transition_matrix` &rarr; `MultidimensionalArray`** (misconception)

- **Exact edge logic (the wrong rule):** The transition matrix is one block of n \* n numbers, so p[i] on its own means nothing.
- **Twin logic (the right rule):** p[i] is the row array of page i, holding the probabilities of moving from page i to every page.
- **Role:** context

**21. `transition_matrix` &rarr; `NoJaggedArrays`** (misconception)

- **Exact edge logic (the wrong rule):** Every row of the transition matrix must be stored with the same length because 2-D arrays are always rectangular.
- **Twin logic (the right rule):** Each p[i] is its own row array; the surfer's matrix is square only because every page has a row of n probabilities.
- **Role:** context

**22. `two_dimensional_array` &rarr; `two_dimensional_array@L0`** (has_level)

- **Exact edge logic:** two dimensional array -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (9 ways).
  - **[0] everyday\_reading** (rule type E, folk-meaning rule): Folk meaning: a table or matrix is one grid in which rows and columns are symmetric, so a column should be as easy to pick out as a row. Java rule: a 2-D array is an array of row arrays; a[i] is row i, a[i][j] an element, and there is no expression for a column.
  - **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `OnlyInnermostArrayElements`: wrong rule: Only the innermost elements are accessible. Right rule: a[i] gives the whole row i, which can be used like any 1-D array.
  - **[2] misconception** (rule type M, wrong rule / right rule) &rarr; `ArrayElementTypeRepeats`: wrong rule: A 2-D int array type is written int[] int[]. Right rule: It is written int[][]: one element type followed by one bracket pair per dimension.
  - **[3] misconception** (rule type M, wrong rule / right rule) &rarr; `ColumnLikeRow`: wrong rule: Column j of a 2-D array can be picked out as a 1-D array, just like row a[i]. Right rule: a[i] is row i (a 1-D array), but there is no expression for a column; loop over i and use a[i][j].
  - **[4] misconception** (rule type M, wrong rule / right rule) &rarr; `MultidimensionalArray`: wrong rule: A 2-D array is one thing, not an array of arrays. Right rule: A 2-D array is an array of m row arrays, so a[i] is a 1-D array of length n.
  - **[5] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `OnlyInnermostArrayElements`: Points to LT: a[i][j] is evaluated as (a[i])[j], first the row and then the element in it. Inconsistent application: the first index is taken as the row on some steps and as the column on others. (here mixing in: "only the innermost elements are accessible")
  - **[6] misconception** (rule type M, wrong rule / right rule) &rarr; `ArrayRankIsLength`: wrong rule: The number of dimensions of an array is its length. Right rule: Rank (number of bracket pairs) and length (number of elements, a.length) are different; a double[][] of size 10-by-3 has a.length == 10.
  - **[7] misconception** (rule type M, wrong rule / right rule) &rarr; `RaggedRowsSameLength`: wrong rule: All rows of a 2-D array have the same length, so one N works for every row. Right rule: Rows may differ in length; use a[i].length for row i.
  - **[8] misconception** (rule type M, wrong rule / right rule) &rarr; `NoJaggedArrays`: wrong rule: Multi-dimensional arrays must be rectangular. Right rule: Each row a[i] is its own array, so rows can have different lengths a[i].length.

**23. `two_dimensional_array` &rarr; `two_dimensional_array@L1`** (has_level)

- **Exact edge logic:** two dimensional array -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).
  - **[0] names\_the\_element** (rule type N, identity rule): Identity: a two-dimensional array, an array of arrays used to represent a table or matrix with M rows and N columns.
  - **[1] states\_the\_rule** (rule type S, declarative rule): Declarative: declare double[][] a; create with new double[M][N] (rows first, then columns); refer to row i, column j as a[i][j]. Entries start at 0 (numbers) or false (boolean).

**24. `two_dimensional_array` &rarr; `two_dimensional_array@L2`** (has_level)

- **Exact edge logic:** two dimensional array -&gt; L2 (Multistructural): the answer applies the rules of two dimensional array to every part of the code, in order (3 ways).
  - **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): Sequencing: new double[M][N] creates an array of M references and then M row arrays of N defaults. a[i][j] evaluates a[i] (checked against a.length = M) and then [j] (checked against a[i].length).
  - **[1] output\_prediction** (rule type OP, evaluation / result rule): Result: a[i][j] has the element type; a.length is the number of rows M; a[i].length is the length of row i; a[i] is a double[] row.
  - **[2] one\_step\_execution** (rule type OS, state-transition rule): State transition: a[i][j] = v changes one element of row i; a[i] = new double[K] replaces the whole row i with a new array; other rows are untouched.

**25. `two_dimensional_array` &rarr; `two_dimensional_array@L3`** (has_level)

- **Exact edge logic:** two dimensional array -&gt; L3 (Relational): the answer relates the parts (7 ways).
  - **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): The transition matrix is a 2-D double array p[i][j] with one row per page; each row holds a probability distribution.
  - **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): A 2-D array uses two indices, and the first chooses the row array: a[i][j] is (a[i])[j].
  - **[2] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Since each row is a separate array, rows may have different lengths; such arrays are ragged.
  - **[3] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Matrix operations index a[i][j] in nested loops (two for addition, three for multiplication).
  - **[4] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): The same notation extends to any number of dimensions: a[i][j][k] for double[][][].
  - **[5] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Row-major order visits a[i][j] with the outer loop over rows i; column-major puts the loop over j outside.
  - **[6] purpose\_of\_the\_whole** (rule type P, plan / role rule): Plan/role: store tables, matrices, grids and images indexed by row and column (grades by student and test, lattice intersections, pixels).

**26. `two_dimensional_array` &rarr; `two_dimensional_array@L4`** (has_level)

- **Exact edge logic:** two dimensional array -&gt; L4 (Extended abstract): the answer reasons beyond the given code (4 ways).
  - **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `OnlyInnermostArrayElements`: Conservation: swapping the loop order for an element-wise operation keeps the result but changes the processing order. Swapping the indices (a[j][i]) transposes and goes out of bounds when M != N.
  - **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Applicability: use a 2-D array for data naturally indexed by two integers (rows by columns). Use a ragged array when rows differ, a 1-D array when one index suffices, and higher dimensions for 3-D models.
  - **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: Indices must be within each dimension (i &lt; a.length, j &lt; a[i].length). Kind: run-time exception. Trigger class: row and column bounds swapped in a non-square M-by-N array, or j bounded by N on a shorter ragged row (ArrayIndexOutOfBoundsException)
  - **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: The type is written with one bracket pair per dimension. Kind: compile-time. Trigger class: int[] int[] a; or assigning an int[] where an int[][] is required (incompatible types)

**27. `topic1.4.g` &rarr; `two_dimensional_array`** (contains)

- topic `topic1.4.g` contains `two_dimensional_array`

**28. `topic1.4.g` &rarr; `matrix_operations`** (contains)

- topic `topic1.4.g` contains `matrix_operations`

**29. `topic1.4.g` &rarr; `multidimensional_array`** (contains)

- topic `topic1.4.g` contains `multidimensional_array`

**30. `topic1.4.g` &rarr; `ragged_array`** (contains)

- topic `topic1.4.g` contains `ragged_array`

**31. `topic1.4.g` &rarr; `row_major_order`** (contains)

- topic `topic1.4.g` contains `row_major_order`
