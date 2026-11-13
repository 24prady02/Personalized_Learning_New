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

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 17 edges around this concept, each explained in the graph's own words.

## What it needs first (1)

A prerequisite edge means the other concept has to be understood before `multidimensional_array`.

### `two_dimensional_array` comes before `multidimensional_array`

*an array of arrays (a[i][j])*

Higher dimensions generalise 2-D arrays.

- **Grounding:** book passage
- **How `multidimensional_array` combines with `two_dimensional_array`:** A 3-D array generalizes 2-D: a[i] is itself a 2-D array, and the same declaration, creation and indexing rules apply one level deeper.
- **How `two_dimensional_array` combines with `multidimensional_array`:** The same notation extends to any number of dimensions: a[i][j][k] for double[][][].

## What it leads to (0)

These concepts need `multidimensional_array` first.

No concept has this one as a prerequisite.

## Learned alongside (0)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

No parallel edge touches this concept.

## Misconceptions (2)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### ArrayBracketCountIsLength

- **Wrong rule:** The number of brackets in an array type or initializer is the array's length.
- **Right rule:** Brackets give the number of dimensions; the length is set at creation.
- **Role of this concept:** context
- **Shows at level L0 as:** misconception: wrong rule: The number of brackets in an array type or initializer is the array's length. Right rule: Brackets give the number of dimensions; the length of each level is set at creation.
- **Also an edge from `array_creation`:** The number of brackets in an array type or initializer is the array's length.
- **Also an edge from `array_declaration`:** The number of brackets in an array type or initializer is the array's length.
- **Also an edge from `array_initializer`:** The number of brackets in an array type or initializer is the array's length.

### ArrayRankIsLength

- **Wrong rule:** The number of dimensions of an array is its length.
- **Right rule:** Rank (number of dimensions) and length are different.
- **Role of this concept:** context
- **Shows at level L0 as:** misconception: wrong rule: The number of dimensions of an array is its length. Right rule: Rank (number of bracket pairs) and length are different: new double[5][5][5] has rank 3 and a.length 5.
- **Shows at level L0 as:** inconsistent trace: Points to LT: a[i][j][k] is evaluated left to right, each index selecting a sub-array of one lower dimension. Inconsistent application: the trace mixes up which index selects which level. (here mixing in: "The number of dimensions of an array is its length")
- **Also an edge from `two_dimensional_array`:** The number of dimensions of an array is its length.

## Errors (0)

An error edge states the rule that gets broken in a program, and the right rule.

The graph has no error edge from this concept.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for multidimensional array: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to multidimensional array agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

multidimensional array -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (4 ways).

- **everyday reading** (folk-meaning rule): Folk meaning: '3-D' suggests three elements, or one solid block. Java rule: each bracket pair adds one level of nesting, so double[][][] is an array of 2-D arrays, and its length is set at creation.
- **misconception** (wrong rule / right rule; shows `ArrayRankIsLength`): wrong rule: The number of dimensions of an array is its length. Right rule: Rank (number of bracket pairs) and length are different: new double[5][5][5] has rank 3 and a.length 5.
- **inconsistent trace** (uneven-application rule; shows `ArrayRankIsLength`): Points to LT: a[i][j][k] is evaluated left to right, each index selecting a sub-array of one lower dimension. Inconsistent application: the trace mixes up which index selects which level. (here mixing in: "The number of dimensions of an array is its length")
- **misconception** (wrong rule / right rule; shows `ArrayBracketCountIsLength`): wrong rule: The number of brackets in an array type or initializer is the array's length. Right rule: Brackets give the number of dimensions; the length of each level is set at creation.

### L1: Unistructural / atom x text surface

L1 for multidimensional array: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

multidimensional array -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

- **names the element** (identity rule): Identity: a multidimensional array, an array with three or more indices built as nested arrays of arrays.
- **states the rule** (declarative rule): Declarative: double[][][] a = new double[N][N][N]; refer to an entry as a[i][j][k].

### L2: Multistructural / block x execution / preoperational

L2 for multidimensional array: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

multidimensional array -&gt; L2 (Multistructural): the answer applies the rules of multidimensional array to every part of the code, in order (3 ways).

- **line by line trace** (operational sequencing rule): Sequencing: a[i] (a 2-D array) is evaluated, then [j] (a 1-D row), then [k] (the element); each step is bounds-checked against the length of that level.
- **output prediction** (evaluation / result rule): Result: new double[N][N][N] holds N\*N\*N doubles, all 0.0; a.length is N, and a[i] is a double[][].
- **one step execution** (state-transition rule): State transition: a[i][j][k] = v changes one element; nothing else changes.

### L3: Relational / relations x function (concrete operational begins)

L3 for multidimensional array: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

multidimensional array -&gt; L3 (Relational): the answer relates the parts (2 ways).

- **relation to neighbour** (composition rule (with a neighbour)): A 3-D array generalizes 2-D: a[i] is itself a 2-D array, and the same declaration, creation and indexing rules apply one level deeper.
- **purpose of the whole** (plan / role rule): Plan/role: model data with three or more coordinates, e.g. a 3-D lattice for self-avoiding walks or physical space.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for multidimensional array: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

multidimensional array -&gt; L4 (Extended abstract): the answer reasons beyond the given code (4 ways).

- **predict a change** (conservation rule; shows `ArrayRankIsLength`): Conservation: adding a dimension multiplies memory and creation time by the new extent (N^3 values for N per side), because creation time is proportional to the number of elements.
- **transfer to a new program** (applicability rule): Applicability: use one when data naturally has three or more integer coordinates and N is small enough for N^3 storage. Use 2-D or 1-D arrays when fewer indices suffice.
- **diagnose an error** (error rule): rule broken: The total size must be a non-negative int and fit in memory. Kind: run-time exception. Trigger class: large N in new double[N][N][N] exhausts memory (OutOfMemoryError), or a negative dimension (NegativeArraySizeException)
- **diagnose an error** (error rule): rule broken: Each index must be within its own level. Kind: run-time exception. Trigger class: an index &gt;= the length of its level (ArrayIndexOutOfBoundsException)

## Same topic

`multidimensional_array` belongs to the topic **Two-dimensional arrays (ragged, matrix operations)** (`topic1.4.g`). The topic also contains: `matrix_operations`, `ragged_array`, `row_major_order`, `two_dimensional_array`.

## Rules of the concept (15)

- **folk-meaning rule:** Folk meaning: '3-D' suggests three elements, or one solid block. Java rule: each bracket pair adds one level of nesting, so double[][][] is an array of 2-D arrays, and its length is set at creation.
- **wrong rule / right rule:** ArrayRankIsLength: wrong: The number of dimensions of an array is its length. \| right: Rank (number of bracket pairs) and length are different: new double[5][5][5] has rank 3 and a.length 5.
- **wrong rule / right rule:** ArrayBracketCountIsLength: wrong: The number of brackets in an array type or initializer is the array's length. \| right: Brackets give the number of dimensions; the length of each level is set at creation.
- **uneven-application rule:** Points to LT: a[i][j][k] is evaluated left to right, each index selecting a sub-array of one lower dimension. Inconsistent application: the trace mixes up which index selects which level.
- **identity rule:** Identity: a multidimensional array, an array with three or more indices built as nested arrays of arrays.
- **declarative rule:** Declarative: double[][][] a = new double[N][N][N]; refer to an entry as a[i][j][k].
- **operational sequencing rule:** Sequencing: a[i] (a 2-D array) is evaluated, then [j] (a 1-D row), then [k] (the element); each step is bounds-checked against the length of that level.
- **evaluation / result rule:** Result: new double[N][N][N] holds N\*N\*N doubles, all 0.0; a.length is N, and a[i] is a double[][].
- **state-transition rule:** State transition: a[i][j][k] = v changes one element; nothing else changes.
- **composition rule (with a neighbour):** with two\_dimensional\_array: A 3-D array generalizes 2-D: a[i] is itself a 2-D array, and the same declaration, creation and indexing rules apply one level deeper.
- **plan / role rule:** Plan/role: model data with three or more coordinates, e.g. a 3-D lattice for self-avoiding walks or physical space.
- **conservation rule:** Conservation: adding a dimension multiplies memory and creation time by the new extent (N^3 values for N per side), because creation time is proportional to the number of elements.
- **error rule:** rule broken: The total size must be a non-negative int and fit in memory. (run-time exception)
- **error rule:** rule broken: Each index must be within its own level. (run-time exception)
- **applicability rule:** Applicability: use one when data naturally has three or more integer coordinates and N is small enough for N^3 storage. Use 2-D or 1-D arrays when fewer indices suffice.

## The whole prerequisite chain

- **Everything it builds on (7):** `array_creation`, `array_declaration`, `array_initializer`, `data_structure`, `data_type`, `indexing`, `two_dimensional_array`
- **Everything that builds on it (0):** nothing
