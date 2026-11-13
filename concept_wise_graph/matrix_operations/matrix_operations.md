# matrix_operations (`matrix_operations`)

matrix addition and multiplication with nested loops

Section 1.4 Arrays, topic 1.4.g Two-dimensional arrays (ragged, matrix operations).

![The knowledge graph around matrix_operations](matrix_operations.png)

## At a glance

- **Needs first:** `nested_loops`, `two_dimensional_array`
- **Leads to:** `power_method`
- **Learned alongside:** nothing
- **Misconceptions:** `ColumnLikeRow`, `MatrixProductCommutes`, `MatrixProductIsElementwise`, `WholeArrayArithmetic`
- **Errors:** none
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 20 edges around this concept. The edge logic, the wrong and right rules and the exact rules of the ways are copied word for word from the graph.

## To work on (1)

- no aliases: a student's words cannot name this concept

## What it needs first (2)

A prerequisite edge means the other concept has to be understood before `matrix_operations`.

### `nested_loops` comes before `matrix_operations`

*a loop inside a loop*

- **Edge:** `pre:nested_loops->matrix_operations`
- **Exact edge logic:** Matrix addition uses two nested loops over i and j, and matrix multiplication adds a third inner loop over k to compute each dot product c[i][j].
- **Grounding:** book\_passage
- **Composition rule (R) of `matrix_operations` with `nested_loops`:** Addition uses two nested loops (i, j); multiplication adds a third inner loop over k for each dot product.
- **Composition rule (R) of `nested_loops` with `matrix_operations`:** Matrix addition uses two nested loops over i and j; matrix multiplication adds a third, innermost loop over k for each dot product.

### `two_dimensional_array` comes before `matrix_operations`

*an array of arrays (a[i][j])*

- **Edge:** `pre:two_dimensional_array->matrix_operations`
- **Exact edge logic:** Matrix operations index a[i][j] in nested loops.
- **Grounding:** book\_passage
- **Composition rule (R) of `matrix_operations` with `two_dimensional_array`:** Matrices are stored as 2-D arrays and read entry by entry as a[i][j].
- **Composition rule (R) of `two_dimensional_array` with `matrix_operations`:** Matrix operations index a[i][j] in nested loops (two for addition, three for multiplication).

## What it leads to (1)

These concepts need `matrix_operations` first.

### `matrix_operations` comes before `power_method`

*repeated vector-matrix multiplication to compute page ranks*

- **Edge:** `pre:matrix_operations->power_method`
- **Exact edge logic:** The power method is repeated vector-matrix multiplication.
- **Grounding:** book\_passage
- **Composition rule (R) of `matrix_operations` with `power_method`:** The power method repeats vector-matrix multiplication rather than matrix-matrix multiplication, because that is all it needs.
- **Composition rule (R) of `power_method` with `matrix_operations`:** Each iteration is a vector-matrix product: newRank[j] is the dot product of rank[] and column j of p[][], computed with nested for loops.

## Learned alongside (0)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

No parallel edge touches this concept.

## Misconceptions (4)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### ColumnLikeRow

- **Edge:** `matrix_operations` &rarr; `ColumnLikeRow` (misconception)
- **Exact edge logic (the wrong rule):** Column j of a 2-D array can be picked out as a 1-D array, just like row a[i].
- **Twin logic (the right rule):** a[i] is row i (a 1-D array), but there is no expression for a column; loop over i and use a[i][j].
- **Wrong belief (on the node):** Column j of a 2-D array can be picked out as a 1-D array, just like row a[i].
- **Correct rule (on the node):** a[i] is row i (a 1-D array), but there is no expression for a column; loop over i and use a[i][j].
- **Provenance:** textbook
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [5] misconception, exact rule:** wrong rule: Column j of a 2-D array can be picked out as a 1-D array, just like row a[i]. Right rule: There is no column expression; the product reads column j of b element by element as b[k][j] in the k loop.
- **Edge `two_dimensional_array` &rarr; `ColumnLikeRow`, exact edge logic:** Column j of a 2-D array can be picked out as a 1-D array, just like row a[i]. **Twin logic:** a[i] is row i (a 1-D array), but there is no expression for a column; loop over i and use a[i][j]. (role: primary)

### MatrixProductCommutes

- **Edge:** `matrix_operations` &rarr; `MatrixProductCommutes` (misconception)
- **Exact edge logic (the wrong rule):** A \* B and B \* A are the same matrix.
- **Twin logic (the right rule):** Matrix multiplication is not commutative; changing the order may change the product.
- **Wrong belief (on the node):** A \* B and B \* A are the same matrix.
- **Correct rule (on the node):** Matrix multiplication is not commutative; changing the order may change the product.
- **Provenance:** textbook
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [2] misconception, exact rule:** wrong rule: A \* B and B \* A are the same matrix. Right rule: Matrix multiplication is not commutative; changing the order may change the product, and for non-square matrices one order may not even be defined.
- **Edge `power_method` &rarr; `MatrixProductCommutes`, exact edge logic:** A \* B and B \* A are the same matrix. **Twin logic:** Matrix multiplication is not commutative; changing the order may change the product. (role: context)

### MatrixProductIsElementwise

- **Edge:** `matrix_operations` &rarr; `MatrixProductIsElementwise` (misconception)
- **Exact edge logic (the wrong rule):** c[i][j] = a[i][j] \* b[i][j] computes the matrix product.
- **Twin logic (the right rule):** c[i][j] is the dot product of row i of a with column j of b.
- **Wrong belief (on the node):** c[i][j] = a[i][j] \* b[i][j] computes the matrix product.
- **Correct rule (on the node):** c[i][j] is the dot product of row i of a with column j of b.
- **Provenance:** derived
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [1] misconception, exact rule:** wrong rule: c[i][j] = a[i][j] \* b[i][j] computes the matrix product. Right rule: c[i][j] is the dot product of row i of a with column j of b: the sum over k of a[i][k]\*b[k][j].
- **L0 way [3] inconsistent\_trace, exact rule:** Points to LT: the innermost k loop finishes accumulating c[i][j] before j moves on. Inconsistent application: c[i][j] is reset inside the k loop on some passes, or a[k][i] is used instead of a[i][k]. (here mixing in: "c[i][j] = a[i][j] \* b[i][j] computes the matrix product")

### WholeArrayArithmetic

- **Edge:** `matrix_operations` &rarr; `WholeArrayArithmetic` (misconception)
- **Exact edge logic (the wrong rule):** a = a + b adds the arrays element by element.
- **Twin logic (the right rule):** Java has no arithmetic on whole arrays; write a loop that adds a[i] + b[i] for each i.
- **Wrong belief (on the node):** a = a + b adds the arrays element by element.
- **Correct rule (on the node):** Java has no arithmetic on whole arrays; write a loop that adds a[i] + b[i] for each i.
- **Provenance:** textbook
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [4] misconception, exact rule:** wrong rule: a = a + b adds the arrays element by element. Right rule: Java has no arithmetic on whole arrays; write nested loops that compute c[i][j] = a[i][j] + b[i][j].
- **Edge `array_traversal` &rarr; `WholeArrayArithmetic`, exact edge logic:** a = a + b adds the arrays element by element. **Twin logic:** Java has no arithmetic on whole arrays; write a loop that adds a[i] + b[i] for each i. (role: primary)

## Errors (0)

An error edge states the rule that gets broken in a program, and the right rule.

The graph has no error edge from this concept.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for matrix operations: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to matrix operations agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

- **Edge:** `matrix_operations` &rarr; `matrix_operations@L0` (has_level)
- **Exact edge logic:** matrix operations -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (6 ways).

Ways (6), each with its exact rule:

- **[0] everyday\_reading** (rule type E, folk-meaning rule): Folk meaning: 'multiply two tables' suggests multiplying matching entries (as addition adds them), and ordinary multiplication commutes. Rule: each product entry c[i][j] is the dot product of row i of a and column j of b, and AB generally differs from BA.
- **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `MatrixProductIsElementwise`: wrong rule: c[i][j] = a[i][j] \* b[i][j] computes the matrix product. Right rule: c[i][j] is the dot product of row i of a with column j of b: the sum over k of a[i][k]\*b[k][j].
- **[2] misconception** (rule type M, wrong rule / right rule) &rarr; `MatrixProductCommutes`: wrong rule: A \* B and B \* A are the same matrix. Right rule: Matrix multiplication is not commutative; changing the order may change the product, and for non-square matrices one order may not even be defined.
- **[3] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `MatrixProductIsElementwise`: Points to LT: the innermost k loop finishes accumulating c[i][j] before j moves on. Inconsistent application: c[i][j] is reset inside the k loop on some passes, or a[k][i] is used instead of a[i][k]. (here mixing in: "c[i][j] = a[i][j] \* b[i][j] computes the matrix product")
- **[4] misconception** (rule type M, wrong rule / right rule) &rarr; `WholeArrayArithmetic`: wrong rule: a = a + b adds the arrays element by element. Right rule: Java has no arithmetic on whole arrays; write nested loops that compute c[i][j] = a[i][j] + b[i][j].
- **[5] misconception** (rule type M, wrong rule / right rule) &rarr; `ColumnLikeRow`: wrong rule: Column j of a 2-D array can be picked out as a 1-D array, just like row a[i]. Right rule: There is no column expression; the product reads column j of b element by element as b[k][j] in the k loop.

### L1: Unistructural / atom x text surface

L1 for matrix operations: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

- **Edge:** `matrix_operations` &rarr; `matrix_operations@L1` (has_level)
- **Exact edge logic:** matrix operations -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

Ways (2), each with its exact rule:

- **[0] names\_the\_element** (rule type N, identity rule): Identity: matrix addition and multiplication implemented with nested for loops over 2-D arrays.
- **[1] states\_the\_rule** (rule type S, declarative rule): Declarative: sum c[i][j] = a[i][j] + b[i][j]; product c[i][j] = sum over k of a[i][k]\*b[k][j]; the product is defined only when the columns of a equal the rows of b.

### L2: Multistructural / block x execution / preoperational

L2 for matrix operations: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

- **Edge:** `matrix_operations` &rarr; `matrix_operations@L2` (has_level)
- **Exact edge logic:** matrix operations -&gt; L2 (Multistructural): the answer applies the rules of matrix operations to every part of the code, in order (3 ways).

Ways (3), each with its exact rule:

- **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): Sequencing: create c (all 0.0); for each i, for each j, for k = 0..N-1 add a[i][k]\*b[k][j] into c[i][j]. The k loop completes for each (i, j) before j increases.
- **[1] output\_prediction** (rule type OP, evaluation / result rule): Result: a new N-by-N double matrix c. In the book's example c[1][2] = .3\*.5 + .6\*.1 + .1\*.4 = .25.
- **[2] one\_step\_execution** (rule type OS, state-transition rule): State transition: one innermost step adds one product a[i][k]\*b[k][j] to c[i][j]; nothing else changes.

### L3: Relational / relations x function (concrete operational begins)

L3 for matrix operations: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

- **Edge:** `matrix_operations` &rarr; `matrix_operations@L3` (has_level)
- **Exact edge logic:** matrix operations -&gt; L3 (Relational): the answer relates the parts (4 ways).

Ways (4), each with its exact rule:

- **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Matrices are stored as 2-D arrays and read entry by entry as a[i][j].
- **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Addition uses two nested loops (i, j); multiplication adds a third inner loop over k for each dot product.
- **[2] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): The power method repeats vector-matrix multiplication rather than matrix-matrix multiplication, because that is all it needs.
- **[3] purpose\_of\_the\_whole** (rule type P, plan / role rule): Plan/role: c[i][j] is a gatherer (running sum) for one dot product. The whole computation implements linear-algebra operations used throughout science and engineering.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for matrix operations: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

- **Edge:** `matrix_operations` &rarr; `matrix_operations@L4` (has_level)
- **Exact edge logic:** matrix operations -&gt; L4 (Extended abstract): the answer reasons beyond the given code (5 ways).

Ways (5), each with its exact rule:

- **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `MatrixProductIsElementwise`: Conservation: reordering the i, j, k loops keeps the product (only the summation order changes); swapping a and b changes it. Reusing a c that is not zeroed adds the old values in.
- **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Applicability: use nested-loop matrix code for small and moderate matrices. When only a vector times a matrix is needed (power method), use vector-matrix multiplication, which is far cheaper than matrix-matrix.
- **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: The product sums a[i][k]\*b[k][j] over k. Kind: silent logic error. Trigger class: the element-wise c[i][j] = a[i][j]\*b[i][j] is used for the product
- **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: Columns of a must equal rows of b. Kind: run-time exception. Trigger class: non-square matrices with mismatched inner dimensions, or loop bounds swapped (ArrayIndexOutOfBoundsException)
- **[4] diagnose\_an\_error** (rule type D, error rule): rule broken: Arrays have no arithmetic operators. Kind: compile-time. Trigger class: c = a + b or a \* b written for 2-D arrays (bad operand types)

## Same topic

`matrix_operations` belongs to the topic **Two-dimensional arrays (ragged, matrix operations)** (`topic1.4.g`). The topic also contains: `multidimensional_array`, `ragged_array`, `row_major_order`, `two_dimensional_array`.

## Rules of the concept (20)

- **Book** (SW-1e, p. 103 (pdf 113)): "We use nested for loops for many array-processing operations."
- **Book** (SW-1.4, ): "is computed by taking the dot product of row i of a[] with column j of b[]."
- **Book** (LA-Nicholson, ): "If the order of the factors in a product of matrices is changed, the product matrix may change (or may not be defined)."
- **E** (folk-meaning rule): Folk meaning: 'multiply two tables' suggests multiplying matching entries (as addition adds them), and ordinary multiplication commutes. Rule: each product entry c[i][j] is the dot product of row i of a and column j of b, and AB generally differs from BA.
- **M** (wrong rule / right rule): MatrixProductCommutes: wrong: A \* B and B \* A are the same matrix. \| right: Matrix multiplication is not commutative; changing the order may change the product, and for non-square matrices one order may not even be defined.
- **M** (wrong rule / right rule): MatrixProductIsElementwise: wrong: c[i][j] = a[i][j] \* b[i][j] computes the matrix product. \| right: c[i][j] is the dot product of row i of a with column j of b: the sum over k of a[i][k]\*b[k][j].
- **M** (wrong rule / right rule): WholeArrayArithmetic: wrong: a = a + b adds the arrays element by element. \| right: Java has no arithmetic on whole arrays; write nested loops that compute c[i][j] = a[i][j] + b[i][j].
- **M** (wrong rule / right rule): ColumnLikeRow: wrong: Column j of a 2-D array can be picked out as a 1-D array, just like row a[i]. \| right: There is no column expression; the product reads column j of b element by element as b[k][j] in the k loop.
- **T** (uneven-application rule): Points to LT: the innermost k loop finishes accumulating c[i][j] before j moves on. Inconsistent application: c[i][j] is reset inside the k loop on some passes, or a[k][i] is used instead of a[i][k].
- **N** (identity rule): Identity: matrix addition and multiplication implemented with nested for loops over 2-D arrays.
- **S** (declarative rule): Declarative: sum c[i][j] = a[i][j] + b[i][j]; product c[i][j] = sum over k of a[i][k]\*b[k][j]; the product is defined only when the columns of a equal the rows of b.
- **LT** (operational sequencing rule): Sequencing: create c (all 0.0); for each i, for each j, for k = 0..N-1 add a[i][k]\*b[k][j] into c[i][j]. The k loop completes for each (i, j) before j increases.
- **OP** (evaluation / result rule): Result: a new N-by-N double matrix c. In the book's example c[1][2] = .3\*.5 + .6\*.1 + .1\*.4 = .25.
- **OS** (state-transition rule): State transition: one innermost step adds one product a[i][k]\*b[k][j] to c[i][j]; nothing else changes.
- **R** (composition rule (with a neighbour)): with two\_dimensional\_array: Matrices are stored as 2-D arrays and read entry by entry as a[i][j].
- **R** (composition rule (with a neighbour)): with nested\_loops: Addition uses two nested loops (i, j); multiplication adds a third inner loop over k for each dot product.
- **R** (composition rule (with a neighbour)): with power\_method: The power method repeats vector-matrix multiplication rather than matrix-matrix multiplication, because that is all it needs.
- **P** (plan / role rule): Plan/role: c[i][j] is a gatherer (running sum) for one dot product. The whole computation implements linear-algebra operations used throughout science and engineering.
- **C** (conservation rule): Conservation: reordering the i, j, k loops keeps the product (only the summation order changes); swapping a and b changes it. Reusing a c that is not zeroed adds the old values in.
- **D** (error rule): rule broken: The product sums a[i][k]\*b[k][j] over k. (silent logic error)
- **D** (error rule): rule broken: Columns of a must equal rows of b. (run-time exception)
- **D** (error rule): rule broken: Arrays have no arithmetic operators. (compile-time)
- **X** (applicability rule): Applicability: use nested-loop matrix code for small and moderate matrices. When only a vector times a matrix is needed (power method), use vector-matrix multiplication, which is far cheaper than matrix-matrix.

## How it is found in code and answers (reader block)

- **Aliases:** none
- **Code patterns:** `\w\s*\[\s*\w+\s*\]\s*\[\s*\w+\s*\]\s*\+=\s*\w+\s*\[[^\]]+\]\s*\[[^\]]+\]\s*\*`, `\w\s*\[\s*\w+\s*\]\s*\[\s*\w+\s*\]\s*=\s*\w+\s*\[\s*\w+\s*\]\s*\[\s*\w+\s*\]\s*[+\-]\s*\w+\s*\[`, `\w\s*\[\s*(\w+)\s*\]\s*\[\s*(\w+)\s*\]\s*=\s*\w+\s*\[\s*\2\s*\]\s*\[\s*\1\s*\]`
- **Operator symbols:** none
- **Java types:** none

## The whole prerequisite chain

- **Everything it builds on (23):** `arithmetic_operators`, `array_creation`, `array_declaration`, `array_initializer`, `boolean`, `boolean_expression`, `comparison_operators`, `data_structure`, `data_type`, `do_while_loop`, `expression`, `for_loop`, `identifier`, `indexing`, `literal`, `logical_operators`, `loop_control`, `loop_variable`, `nested_loops`, `primitive_type`, `two_dimensional_array`, `variable`, `while_loop`
- **Everything that builds on it (3):** `convergence_rate`, `power_method`, `two_models`

## Every edge in this view and its exact edge logic (20)

All the edges drawn in the picture, in the order: prerequisite, parallel, misconception, error, has_level, contains.

**1. `matrix_operations` &rarr; `power_method`** (prerequisite)

- **Exact edge logic:** The power method is repeated vector-matrix multiplication.
- **Grounding:** book\_passage
- **Composition rule (R) of `matrix_operations` with `power_method`:** The power method repeats vector-matrix multiplication rather than matrix-matrix multiplication, because that is all it needs.
- **Composition rule (R) of `power_method` with `matrix_operations`:** Each iteration is a vector-matrix product: newRank[j] is the dot product of rank[] and column j of p[][], computed with nested for loops.

**2. `nested_loops` &rarr; `matrix_operations`** (prerequisite)

- **Exact edge logic:** Matrix addition uses two nested loops over i and j, and matrix multiplication adds a third inner loop over k to compute each dot product c[i][j].
- **Grounding:** book\_passage
- **Composition rule (R) of `nested_loops` with `matrix_operations`:** Matrix addition uses two nested loops over i and j; matrix multiplication adds a third, innermost loop over k for each dot product.
- **Composition rule (R) of `matrix_operations` with `nested_loops`:** Addition uses two nested loops (i, j); multiplication adds a third inner loop over k for each dot product.

**3. `two_dimensional_array` &rarr; `matrix_operations`** (prerequisite)

- **Exact edge logic:** Matrix operations index a[i][j] in nested loops.
- **Grounding:** book\_passage
- **Composition rule (R) of `two_dimensional_array` with `matrix_operations`:** Matrix operations index a[i][j] in nested loops (two for addition, three for multiplication).
- **Composition rule (R) of `matrix_operations` with `two_dimensional_array`:** Matrices are stored as 2-D arrays and read entry by entry as a[i][j].

**4. `matrix_operations` &rarr; `ColumnLikeRow`** (misconception)

- **Exact edge logic (the wrong rule):** Column j of a 2-D array can be picked out as a 1-D array, just like row a[i].
- **Twin logic (the right rule):** a[i] is row i (a 1-D array), but there is no expression for a column; loop over i and use a[i][j].
- **Role:** context

**5. `matrix_operations` &rarr; `MatrixProductCommutes`** (misconception)

- **Exact edge logic (the wrong rule):** A \* B and B \* A are the same matrix.
- **Twin logic (the right rule):** Matrix multiplication is not commutative; changing the order may change the product.
- **Role:** primary

**6. `matrix_operations` &rarr; `MatrixProductIsElementwise`** (misconception)

- **Exact edge logic (the wrong rule):** c[i][j] = a[i][j] \* b[i][j] computes the matrix product.
- **Twin logic (the right rule):** c[i][j] is the dot product of row i of a with column j of b.
- **Role:** primary

**7. `matrix_operations` &rarr; `WholeArrayArithmetic`** (misconception)

- **Exact edge logic (the wrong rule):** a = a + b adds the arrays element by element.
- **Twin logic (the right rule):** Java has no arithmetic on whole arrays; write a loop that adds a[i] + b[i] for each i.
- **Role:** context

**8. `array_traversal` &rarr; `WholeArrayArithmetic`** (misconception)

- **Exact edge logic (the wrong rule):** a = a + b adds the arrays element by element.
- **Twin logic (the right rule):** Java has no arithmetic on whole arrays; write a loop that adds a[i] + b[i] for each i.
- **Role:** primary

**9. `power_method` &rarr; `MatrixProductCommutes`** (misconception)

- **Exact edge logic (the wrong rule):** A \* B and B \* A are the same matrix.
- **Twin logic (the right rule):** Matrix multiplication is not commutative; changing the order may change the product.
- **Role:** context

**10. `two_dimensional_array` &rarr; `ColumnLikeRow`** (misconception)

- **Exact edge logic (the wrong rule):** Column j of a 2-D array can be picked out as a 1-D array, just like row a[i].
- **Twin logic (the right rule):** a[i] is row i (a 1-D array), but there is no expression for a column; loop over i and use a[i][j].
- **Role:** primary

**11. `matrix_operations` &rarr; `matrix_operations@L0`** (has_level)

- **Exact edge logic:** matrix operations -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (6 ways).
  - **[0] everyday\_reading** (rule type E, folk-meaning rule): Folk meaning: 'multiply two tables' suggests multiplying matching entries (as addition adds them), and ordinary multiplication commutes. Rule: each product entry c[i][j] is the dot product of row i of a and column j of b, and AB generally differs from BA.
  - **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `MatrixProductIsElementwise`: wrong rule: c[i][j] = a[i][j] \* b[i][j] computes the matrix product. Right rule: c[i][j] is the dot product of row i of a with column j of b: the sum over k of a[i][k]\*b[k][j].
  - **[2] misconception** (rule type M, wrong rule / right rule) &rarr; `MatrixProductCommutes`: wrong rule: A \* B and B \* A are the same matrix. Right rule: Matrix multiplication is not commutative; changing the order may change the product, and for non-square matrices one order may not even be defined.
  - **[3] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `MatrixProductIsElementwise`: Points to LT: the innermost k loop finishes accumulating c[i][j] before j moves on. Inconsistent application: c[i][j] is reset inside the k loop on some passes, or a[k][i] is used instead of a[i][k]. (here mixing in: "c[i][j] = a[i][j] \* b[i][j] computes the matrix product")
  - **[4] misconception** (rule type M, wrong rule / right rule) &rarr; `WholeArrayArithmetic`: wrong rule: a = a + b adds the arrays element by element. Right rule: Java has no arithmetic on whole arrays; write nested loops that compute c[i][j] = a[i][j] + b[i][j].
  - **[5] misconception** (rule type M, wrong rule / right rule) &rarr; `ColumnLikeRow`: wrong rule: Column j of a 2-D array can be picked out as a 1-D array, just like row a[i]. Right rule: There is no column expression; the product reads column j of b element by element as b[k][j] in the k loop.

**12. `matrix_operations` &rarr; `matrix_operations@L1`** (has_level)

- **Exact edge logic:** matrix operations -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).
  - **[0] names\_the\_element** (rule type N, identity rule): Identity: matrix addition and multiplication implemented with nested for loops over 2-D arrays.
  - **[1] states\_the\_rule** (rule type S, declarative rule): Declarative: sum c[i][j] = a[i][j] + b[i][j]; product c[i][j] = sum over k of a[i][k]\*b[k][j]; the product is defined only when the columns of a equal the rows of b.

**13. `matrix_operations` &rarr; `matrix_operations@L2`** (has_level)

- **Exact edge logic:** matrix operations -&gt; L2 (Multistructural): the answer applies the rules of matrix operations to every part of the code, in order (3 ways).
  - **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): Sequencing: create c (all 0.0); for each i, for each j, for k = 0..N-1 add a[i][k]\*b[k][j] into c[i][j]. The k loop completes for each (i, j) before j increases.
  - **[1] output\_prediction** (rule type OP, evaluation / result rule): Result: a new N-by-N double matrix c. In the book's example c[1][2] = .3\*.5 + .6\*.1 + .1\*.4 = .25.
  - **[2] one\_step\_execution** (rule type OS, state-transition rule): State transition: one innermost step adds one product a[i][k]\*b[k][j] to c[i][j]; nothing else changes.

**14. `matrix_operations` &rarr; `matrix_operations@L3`** (has_level)

- **Exact edge logic:** matrix operations -&gt; L3 (Relational): the answer relates the parts (4 ways).
  - **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Matrices are stored as 2-D arrays and read entry by entry as a[i][j].
  - **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Addition uses two nested loops (i, j); multiplication adds a third inner loop over k for each dot product.
  - **[2] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): The power method repeats vector-matrix multiplication rather than matrix-matrix multiplication, because that is all it needs.
  - **[3] purpose\_of\_the\_whole** (rule type P, plan / role rule): Plan/role: c[i][j] is a gatherer (running sum) for one dot product. The whole computation implements linear-algebra operations used throughout science and engineering.

**15. `matrix_operations` &rarr; `matrix_operations@L4`** (has_level)

- **Exact edge logic:** matrix operations -&gt; L4 (Extended abstract): the answer reasons beyond the given code (5 ways).
  - **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `MatrixProductIsElementwise`: Conservation: reordering the i, j, k loops keeps the product (only the summation order changes); swapping a and b changes it. Reusing a c that is not zeroed adds the old values in.
  - **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Applicability: use nested-loop matrix code for small and moderate matrices. When only a vector times a matrix is needed (power method), use vector-matrix multiplication, which is far cheaper than matrix-matrix.
  - **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: The product sums a[i][k]\*b[k][j] over k. Kind: silent logic error. Trigger class: the element-wise c[i][j] = a[i][j]\*b[i][j] is used for the product
  - **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: Columns of a must equal rows of b. Kind: run-time exception. Trigger class: non-square matrices with mismatched inner dimensions, or loop bounds swapped (ArrayIndexOutOfBoundsException)
  - **[4] diagnose\_an\_error** (rule type D, error rule): rule broken: Arrays have no arithmetic operators. Kind: compile-time. Trigger class: c = a + b or a \* b written for 2-D arrays (bad operand types)

**16. `topic1.4.g` &rarr; `matrix_operations`** (contains)

- topic `topic1.4.g` contains `matrix_operations`

**17. `topic1.4.g` &rarr; `multidimensional_array`** (contains)

- topic `topic1.4.g` contains `multidimensional_array`

**18. `topic1.4.g` &rarr; `ragged_array`** (contains)

- topic `topic1.4.g` contains `ragged_array`

**19. `topic1.4.g` &rarr; `row_major_order`** (contains)

- topic `topic1.4.g` contains `row_major_order`

**20. `topic1.4.g` &rarr; `two_dimensional_array`** (contains)

- topic `topic1.4.g` contains `two_dimensional_array`
