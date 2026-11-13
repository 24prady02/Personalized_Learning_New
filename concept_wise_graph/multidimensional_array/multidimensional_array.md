# multidimensional_array (`multidimensional_array`)

arrays with three or more indices

Section 1.4 Arrays, topic 1.4.g Two-dimensional arrays (ragged, matrix operations).

![The knowledge graph around multidimensional_array](multidimensional_array.png)

## At a glance

- **Needs first:** `two_dimensional_array`
- **Leads to:** nothing
- **Learned alongside:** nothing
- **Misconceptions:** `ArrayBracketCountIsLength`, `ArrayRankIsLength`
- **Errors:** none
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 17 edges around this concept. The edge logic, the wrong and right rules and the exact rules of the ways are copied word for word from the graph.

## To work on (1)

- no aliases: a student's words cannot name this concept

## What it needs first (1)

A prerequisite edge means the other concept has to be understood before `multidimensional_array`.

### `two_dimensional_array` comes before `multidimensional_array`

*an array of arrays (a[i][j])*

- **Edge:** `pre:two_dimensional_array->multidimensional_array`
- **Exact edge logic:** Higher dimensions generalise 2-D arrays.
- **Grounding:** book\_passage
- **Composition rule (R) of `multidimensional_array` with `two_dimensional_array`:** A 3-D array generalizes 2-D: a[i] is itself a 2-D array, and the same declaration, creation and indexing rules apply one level deeper.
- **Composition rule (R) of `two_dimensional_array` with `multidimensional_array`:** The same notation extends to any number of dimensions: a[i][j][k] for double[][][].

## What it leads to (0)

These concepts need `multidimensional_array` first.

No concept has this one as a prerequisite.

## Learned alongside (0)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

No parallel edge touches this concept.

## Misconceptions (2)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### ArrayBracketCountIsLength

- **Edge:** `multidimensional_array` &rarr; `ArrayBracketCountIsLength` (misconception)
- **Exact edge logic (the wrong rule):** The number of brackets in an array type or initializer is the array's length.
- **Twin logic (the right rule):** Brackets give the number of dimensions; the length is set at creation.
- **Wrong belief (on the node):** The number of brackets in an array type or initializer is the array's length.
- **Correct rule (on the node):** Brackets give the number of dimensions; the length is set at creation.
- **Provenance:** published
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [3] misconception, exact rule:** wrong rule: The number of brackets in an array type or initializer is the array's length. Right rule: Brackets give the number of dimensions; the length of each level is set at creation.
- **Edge `array_creation` &rarr; `ArrayBracketCountIsLength`, exact edge logic:** The number of brackets in an array type or initializer is the array's length. **Twin logic:** Brackets give the number of dimensions; the length is set at creation. (role: context)
- **Edge `array_declaration` &rarr; `ArrayBracketCountIsLength`, exact edge logic:** The number of brackets in an array type or initializer is the array's length. **Twin logic:** Brackets give the number of dimensions; the length is set at creation. (role: primary)
- **Edge `array_initializer` &rarr; `ArrayBracketCountIsLength`, exact edge logic:** The number of brackets in an array type or initializer is the array's length. **Twin logic:** Brackets give the number of dimensions; the length is set at creation. (role: context)

### ArrayRankIsLength

- **Edge:** `multidimensional_array` &rarr; `ArrayRankIsLength` (misconception)
- **Exact edge logic (the wrong rule):** The number of dimensions of an array is its length.
- **Twin logic (the right rule):** Rank (number of dimensions) and length are different.
- **Wrong belief (on the node):** The number of dimensions of an array is its length.
- **Correct rule (on the node):** Rank (number of dimensions) and length are different.
- **Provenance:** published
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [1] misconception, exact rule:** wrong rule: The number of dimensions of an array is its length. Right rule: Rank (number of bracket pairs) and length are different: new double[5][5][5] has rank 3 and a.length 5.
- **L0 way [2] inconsistent\_trace, exact rule:** Points to LT: a[i][j][k] is evaluated left to right, each index selecting a sub-array of one lower dimension. Inconsistent application: the trace mixes up which index selects which level. (here mixing in: "The number of dimensions of an array is its length")
- **Edge `two_dimensional_array` &rarr; `ArrayRankIsLength`, exact edge logic:** The number of dimensions of an array is its length. **Twin logic:** Rank (number of dimensions) and length are different. (role: primary)

## Errors (0)

An error edge states the rule that gets broken in a program, and the right rule.

The graph has no error edge from this concept.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for multidimensional array: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to multidimensional array agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

- **Edge:** `multidimensional_array` &rarr; `multidimensional_array@L0` (has_level)
- **Exact edge logic:** multidimensional array -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (4 ways).

Ways (4), each with its exact rule:

- **[0] everyday\_reading** (rule type E, folk-meaning rule): Folk meaning: '3-D' suggests three elements, or one solid block. Java rule: each bracket pair adds one level of nesting, so double[][][] is an array of 2-D arrays, and its length is set at creation.
- **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `ArrayRankIsLength`: wrong rule: The number of dimensions of an array is its length. Right rule: Rank (number of bracket pairs) and length are different: new double[5][5][5] has rank 3 and a.length 5.
- **[2] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `ArrayRankIsLength`: Points to LT: a[i][j][k] is evaluated left to right, each index selecting a sub-array of one lower dimension. Inconsistent application: the trace mixes up which index selects which level. (here mixing in: "The number of dimensions of an array is its length")
- **[3] misconception** (rule type M, wrong rule / right rule) &rarr; `ArrayBracketCountIsLength`: wrong rule: The number of brackets in an array type or initializer is the array's length. Right rule: Brackets give the number of dimensions; the length of each level is set at creation.

### L1: Unistructural / atom x text surface

L1 for multidimensional array: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

- **Edge:** `multidimensional_array` &rarr; `multidimensional_array@L1` (has_level)
- **Exact edge logic:** multidimensional array -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

Ways (2), each with its exact rule:

- **[0] names\_the\_element** (rule type N, identity rule): Identity: a multidimensional array, an array with three or more indices built as nested arrays of arrays.
- **[1] states\_the\_rule** (rule type S, declarative rule): Declarative: double[][][] a = new double[N][N][N]; refer to an entry as a[i][j][k].

### L2: Multistructural / block x execution / preoperational

L2 for multidimensional array: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

- **Edge:** `multidimensional_array` &rarr; `multidimensional_array@L2` (has_level)
- **Exact edge logic:** multidimensional array -&gt; L2 (Multistructural): the answer applies the rules of multidimensional array to every part of the code, in order (3 ways).

Ways (3), each with its exact rule:

- **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): Sequencing: a[i] (a 2-D array) is evaluated, then [j] (a 1-D row), then [k] (the element); each step is bounds-checked against the length of that level.
- **[1] output\_prediction** (rule type OP, evaluation / result rule): Result: new double[N][N][N] holds N\*N\*N doubles, all 0.0; a.length is N, and a[i] is a double[][].
- **[2] one\_step\_execution** (rule type OS, state-transition rule): State transition: a[i][j][k] = v changes one element; nothing else changes.

### L3: Relational / relations x function (concrete operational begins)

L3 for multidimensional array: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

- **Edge:** `multidimensional_array` &rarr; `multidimensional_array@L3` (has_level)
- **Exact edge logic:** multidimensional array -&gt; L3 (Relational): the answer relates the parts (2 ways).

Ways (2), each with its exact rule:

- **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): A 3-D array generalizes 2-D: a[i] is itself a 2-D array, and the same declaration, creation and indexing rules apply one level deeper.
- **[1] purpose\_of\_the\_whole** (rule type P, plan / role rule): Plan/role: model data with three or more coordinates, e.g. a 3-D lattice for self-avoiding walks or physical space.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for multidimensional array: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

- **Edge:** `multidimensional_array` &rarr; `multidimensional_array@L4` (has_level)
- **Exact edge logic:** multidimensional array -&gt; L4 (Extended abstract): the answer reasons beyond the given code (4 ways).

Ways (4), each with its exact rule:

- **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `ArrayRankIsLength`: Conservation: adding a dimension multiplies memory and creation time by the new extent (N^3 values for N per side), because creation time is proportional to the number of elements.
- **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Applicability: use one when data naturally has three or more integer coordinates and N is small enough for N^3 storage. Use 2-D or 1-D arrays when fewer indices suffice.
- **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: The total size must be a non-negative int and fit in memory. Kind: run-time exception. Trigger class: large N in new double[N][N][N] exhausts memory (OutOfMemoryError), or a negative dimension (NegativeArraySizeException)
- **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: Each index must be within its own level. Kind: run-time exception. Trigger class: an index &gt;= the length of its level (ArrayIndexOutOfBoundsException)

## Same topic

`multidimensional_array` belongs to the topic **Two-dimensional arrays (ragged, matrix operations)** (`topic1.4.g`). The topic also contains: `matrix_operations`, `ragged_array`, `row_major_order`, `two_dimensional_array`.

## Rules of the concept (15)

- **Book** (SW-1e, p. 107 (pdf 117)): "For instance, we can declare and initialize a three-dimensional array with the code double[][][] a = new double[N][N][N]"
- **Book** (SW-1.4, p. 107 (pdf 117)): "double[][][] a = new double[n][n][n]; and then refer to an entry with code like a[i][j][k]."
- **E** (folk-meaning rule): Folk meaning: '3-D' suggests three elements, or one solid block. Java rule: each bracket pair adds one level of nesting, so double[][][] is an array of 2-D arrays, and its length is set at creation.
- **M** (wrong rule / right rule): ArrayRankIsLength: wrong: The number of dimensions of an array is its length. \| right: Rank (number of bracket pairs) and length are different: new double[5][5][5] has rank 3 and a.length 5.
- **M** (wrong rule / right rule): ArrayBracketCountIsLength: wrong: The number of brackets in an array type or initializer is the array's length. \| right: Brackets give the number of dimensions; the length of each level is set at creation.
- **T** (uneven-application rule): Points to LT: a[i][j][k] is evaluated left to right, each index selecting a sub-array of one lower dimension. Inconsistent application: the trace mixes up which index selects which level.
- **N** (identity rule): Identity: a multidimensional array, an array with three or more indices built as nested arrays of arrays.
- **S** (declarative rule): Declarative: double[][][] a = new double[N][N][N]; refer to an entry as a[i][j][k].
- **LT** (operational sequencing rule): Sequencing: a[i] (a 2-D array) is evaluated, then [j] (a 1-D row), then [k] (the element); each step is bounds-checked against the length of that level.
- **OP** (evaluation / result rule): Result: new double[N][N][N] holds N\*N\*N doubles, all 0.0; a.length is N, and a[i] is a double[][].
- **OS** (state-transition rule): State transition: a[i][j][k] = v changes one element; nothing else changes.
- **R** (composition rule (with a neighbour)): with two\_dimensional\_array: A 3-D array generalizes 2-D: a[i] is itself a 2-D array, and the same declaration, creation and indexing rules apply one level deeper.
- **P** (plan / role rule): Plan/role: model data with three or more coordinates, e.g. a 3-D lattice for self-avoiding walks or physical space.
- **C** (conservation rule): Conservation: adding a dimension multiplies memory and creation time by the new extent (N^3 values for N per side), because creation time is proportional to the number of elements.
- **D** (error rule): rule broken: The total size must be a non-negative int and fit in memory. (run-time exception)
- **D** (error rule): rule broken: Each index must be within its own level. (run-time exception)
- **X** (applicability rule): Applicability: use one when data naturally has three or more integer coordinates and N is small enough for N^3 storage. Use 2-D or 1-D arrays when fewer indices suffice.

## How it is found in code and answers (reader block)

- **Aliases:** none
- **Code patterns:** `\[\s*\]\s*\[\s*\]\s*\[\s*\]`, `\w\s*\[[^\]]+\]\s*\[[^\]]+\]\s*\[[^\]]+\]`
- **Operator symbols:** none
- **Java types:** none

## The whole prerequisite chain

- **Everything it builds on (7):** `array_creation`, `array_declaration`, `array_initializer`, `data_structure`, `data_type`, `indexing`, `two_dimensional_array`
- **Everything that builds on it (0):** nothing

## Every edge in this view and its exact edge logic (17)

All the edges drawn in the picture, in the order: prerequisite, parallel, misconception, error, has_level, contains.

**1. `two_dimensional_array` &rarr; `multidimensional_array`** (prerequisite)

- **Exact edge logic:** Higher dimensions generalise 2-D arrays.
- **Grounding:** book\_passage
- **Composition rule (R) of `two_dimensional_array` with `multidimensional_array`:** The same notation extends to any number of dimensions: a[i][j][k] for double[][][].
- **Composition rule (R) of `multidimensional_array` with `two_dimensional_array`:** A 3-D array generalizes 2-D: a[i] is itself a 2-D array, and the same declaration, creation and indexing rules apply one level deeper.

**2. `multidimensional_array` &rarr; `ArrayBracketCountIsLength`** (misconception)

- **Exact edge logic (the wrong rule):** The number of brackets in an array type or initializer is the array's length.
- **Twin logic (the right rule):** Brackets give the number of dimensions; the length is set at creation.
- **Role:** context

**3. `multidimensional_array` &rarr; `ArrayRankIsLength`** (misconception)

- **Exact edge logic (the wrong rule):** The number of dimensions of an array is its length.
- **Twin logic (the right rule):** Rank (number of dimensions) and length are different.
- **Role:** context

**4. `array_creation` &rarr; `ArrayBracketCountIsLength`** (misconception)

- **Exact edge logic (the wrong rule):** The number of brackets in an array type or initializer is the array's length.
- **Twin logic (the right rule):** Brackets give the number of dimensions; the length is set at creation.
- **Role:** context

**5. `array_declaration` &rarr; `ArrayBracketCountIsLength`** (misconception)

- **Exact edge logic (the wrong rule):** The number of brackets in an array type or initializer is the array's length.
- **Twin logic (the right rule):** Brackets give the number of dimensions; the length is set at creation.
- **Role:** primary

**6. `array_initializer` &rarr; `ArrayBracketCountIsLength`** (misconception)

- **Exact edge logic (the wrong rule):** The number of brackets in an array type or initializer is the array's length.
- **Twin logic (the right rule):** Brackets give the number of dimensions; the length is set at creation.
- **Role:** context

**7. `two_dimensional_array` &rarr; `ArrayRankIsLength`** (misconception)

- **Exact edge logic (the wrong rule):** The number of dimensions of an array is its length.
- **Twin logic (the right rule):** Rank (number of dimensions) and length are different.
- **Role:** primary

**8. `multidimensional_array` &rarr; `multidimensional_array@L0`** (has_level)

- **Exact edge logic:** multidimensional array -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (4 ways).
  - **[0] everyday\_reading** (rule type E, folk-meaning rule): Folk meaning: '3-D' suggests three elements, or one solid block. Java rule: each bracket pair adds one level of nesting, so double[][][] is an array of 2-D arrays, and its length is set at creation.
  - **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `ArrayRankIsLength`: wrong rule: The number of dimensions of an array is its length. Right rule: Rank (number of bracket pairs) and length are different: new double[5][5][5] has rank 3 and a.length 5.
  - **[2] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `ArrayRankIsLength`: Points to LT: a[i][j][k] is evaluated left to right, each index selecting a sub-array of one lower dimension. Inconsistent application: the trace mixes up which index selects which level. (here mixing in: "The number of dimensions of an array is its length")
  - **[3] misconception** (rule type M, wrong rule / right rule) &rarr; `ArrayBracketCountIsLength`: wrong rule: The number of brackets in an array type or initializer is the array's length. Right rule: Brackets give the number of dimensions; the length of each level is set at creation.

**9. `multidimensional_array` &rarr; `multidimensional_array@L1`** (has_level)

- **Exact edge logic:** multidimensional array -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).
  - **[0] names\_the\_element** (rule type N, identity rule): Identity: a multidimensional array, an array with three or more indices built as nested arrays of arrays.
  - **[1] states\_the\_rule** (rule type S, declarative rule): Declarative: double[][][] a = new double[N][N][N]; refer to an entry as a[i][j][k].

**10. `multidimensional_array` &rarr; `multidimensional_array@L2`** (has_level)

- **Exact edge logic:** multidimensional array -&gt; L2 (Multistructural): the answer applies the rules of multidimensional array to every part of the code, in order (3 ways).
  - **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): Sequencing: a[i] (a 2-D array) is evaluated, then [j] (a 1-D row), then [k] (the element); each step is bounds-checked against the length of that level.
  - **[1] output\_prediction** (rule type OP, evaluation / result rule): Result: new double[N][N][N] holds N\*N\*N doubles, all 0.0; a.length is N, and a[i] is a double[][].
  - **[2] one\_step\_execution** (rule type OS, state-transition rule): State transition: a[i][j][k] = v changes one element; nothing else changes.

**11. `multidimensional_array` &rarr; `multidimensional_array@L3`** (has_level)

- **Exact edge logic:** multidimensional array -&gt; L3 (Relational): the answer relates the parts (2 ways).
  - **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): A 3-D array generalizes 2-D: a[i] is itself a 2-D array, and the same declaration, creation and indexing rules apply one level deeper.
  - **[1] purpose\_of\_the\_whole** (rule type P, plan / role rule): Plan/role: model data with three or more coordinates, e.g. a 3-D lattice for self-avoiding walks or physical space.

**12. `multidimensional_array` &rarr; `multidimensional_array@L4`** (has_level)

- **Exact edge logic:** multidimensional array -&gt; L4 (Extended abstract): the answer reasons beyond the given code (4 ways).
  - **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `ArrayRankIsLength`: Conservation: adding a dimension multiplies memory and creation time by the new extent (N^3 values for N per side), because creation time is proportional to the number of elements.
  - **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Applicability: use one when data naturally has three or more integer coordinates and N is small enough for N^3 storage. Use 2-D or 1-D arrays when fewer indices suffice.
  - **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: The total size must be a non-negative int and fit in memory. Kind: run-time exception. Trigger class: large N in new double[N][N][N] exhausts memory (OutOfMemoryError), or a negative dimension (NegativeArraySizeException)
  - **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: Each index must be within its own level. Kind: run-time exception. Trigger class: an index &gt;= the length of its level (ArrayIndexOutOfBoundsException)

**13. `topic1.4.g` &rarr; `multidimensional_array`** (contains)

- topic `topic1.4.g` contains `multidimensional_array`

**14. `topic1.4.g` &rarr; `matrix_operations`** (contains)

- topic `topic1.4.g` contains `matrix_operations`

**15. `topic1.4.g` &rarr; `ragged_array`** (contains)

- topic `topic1.4.g` contains `ragged_array`

**16. `topic1.4.g` &rarr; `row_major_order`** (contains)

- topic `topic1.4.g` contains `row_major_order`

**17. `topic1.4.g` &rarr; `two_dimensional_array`** (contains)

- topic `topic1.4.g` contains `two_dimensional_array`
