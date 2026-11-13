# transition_matrix (`transition_matrix`)

a 2-D array of move probabilities (rows sum to 1)

Section 1.6 Case Study: Random Web Surfer, topic 1.6.a Input format and transition matrix.

![The knowledge graph around transition_matrix](transition_matrix.png)

## At a glance

- **Needs first:** `input_graph`, `teleportation`, `two_dimensional_array`
- **Leads to:** `dangling_pages`, `markov_chain`, `normalization`, `random_move`
- **Learned alongside:** nothing
- **Misconceptions:** `MultidimensionalArray`, `NoJaggedArrays`, `RowsNeedNotSumToOne`
- **Errors:** none
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 25 edges around this concept, each explained in the graph's own words.

## What it needs first (3)

A prerequisite edge means the other concept has to be understood before `transition_matrix`.

### `input_graph` comes before `transition_matrix`

*read the page links from input*

The links read from input fill counts[i][j], and each row of the transition matrix is built from those counts.

- **Grounding:** book passage
- **How `transition_matrix` combines with `input_graph`:** Row i depends only on the tallies read for page i (counts[i][] and outDegree[i]); the matrix cannot be computed until all links have been read.
- **How `input_graph` combines with `transition_matrix`:** The tallies constrain the matrix: row i of the matrix is computed only from counts[i][] and outDegree[i], so a mistake in reading pair order (i/j swapped) moves probability mass into the wrong row.

### `teleportation` comes before `transition_matrix`

*the 90-10 rule: follow a link or jump to a random page*

The 90-10 rule says the surfer follows a random link 90 percent of the time and jumps to a random page 10 percent of the time, and each transition-matrix entry is computed from it.

- **Grounding:** questionable
- **How `transition_matrix` combines with `teleportation`:** The .10/N term, added to every entry, is the teleport (random-page) part of each row; the .90 factor scales the link part so the two parts sum to 1.
- **How `teleportation` combines with `transition_matrix`:** Every entry is built as link part plus leap part; the .90 and .10 weights must sum to 1 for each row to remain a distribution.

### `two_dimensional_array` comes before `transition_matrix`

*an array of arrays (a[i][j])*

The transition matrix is a 2-D double array p[i][j], with one row array per page.

- **Grounding:** book passage
- **How `transition_matrix` combines with `two_dimensional_array`:** The matrix is double[N][N]: p[i] is the row array for page i and p[i][j] an element; indices must be in 0..N-1 and the first index is the row (from-page).
- **How `two_dimensional_array` combines with `transition_matrix`:** The transition matrix is a 2-D double array p[i][j] with one row per page; each row holds a probability distribution.

## What it leads to (4)

These concepts need `transition_matrix` first.

### `transition_matrix` comes before `dangling_pages`

*pages with no outgoing links*

Transition assumes that every page has an outgoing link; Exercise 1.6.3 handles a page with no outgoing links by filling its row of the transition matrix with 1/N.

- **Grounding:** book passage
- **How `transition_matrix` combines with `dangling_pages`:** Transition's formula is valid only if every outDegree[i] &gt; 0; a page with no outlinks must have its row filled with 1/N.
- **How `dangling_pages` combines with `transition_matrix`:** A dangling page is the case where the matrix formula breaks (division by outDegree 0); the 1/N row replaces it so the matrix stays stochastic.

### `transition_matrix` comes before `markov_chain`

*random process where the next state depends only on the current state*

The transition matrix specifies the probability of each move, and the random process those probabilities define is a Markov chain.

- **Grounding:** book passage
- **How `transition_matrix` combines with `markov_chain`:** A matrix whose rows are probability distributions defines a Markov chain: the next page depends only on the current page's row.
- **How `markov_chain` combines with `transition_matrix`:** The chain is defined by the matrix: it must be square with every row a probability distribution.

### `transition_matrix` comes before `normalization`

*scaling a row so its probabilities sum to 1*

Each row of the transition matrix must be a probability distribution, so counts[i][j] is divided by outDegree[i] (scaled by .90, plus .10/N) to make row i sum to 1.

- **Grounding:** book passage
- **How `transition_matrix` combines with `normalization`:** Dividing counts[i][j] by outDegree[i] (after scaling by .90) and adding .10/N is the normalisation that makes row i sum to 1; the double operand .90 keeps the division from being integer division.
- **How `normalization` combines with `transition_matrix`:** Normalisation is applied row by row: every entry of row i is divided by the same total outDegree[i], which is what makes the row a distribution the matrix requires.

### `transition_matrix` comes before `random_move`

*pick the next page from a cumulative-probability test*

Row p[i] is the probability distribution used to choose the next page when the surfer is on page i.

- **Grounding:** book passage
- **How `transition_matrix` combines with `random_move`:** The random move reads one row p[page] as a 1-D array and accumulates its entries; it only works if that row sums to 1.
- **How `random_move` combines with `transition_matrix`:** Reads exactly one row p[page]; the row must sum to 1, otherwise r can exceed the final sum and no j is chosen.

## Learned alongside (0)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

No parallel edge touches this concept.

## Misconceptions (3)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### MultidimensionalArray

- **Wrong rule:** The transition matrix is one block of n \* n numbers, so p[i] on its own means nothing.
- **Right rule:** p[i] is the row array of page i, holding the probabilities of moving from page i to every page.
- **Role of this concept:** context
- **Shows at level L0 as:** misconception: wrong rule: A 2-D array is one thing, not an array of arrays. Right rule: Java represents p[][] as an array of N row arrays; p[page] is itself a 1-D double array (the distribution used by the random move).
- **Also an edge from `two_dimensional_array`:** int[m][n] is one block of m \* n values, so a[i] on its own means nothing.

### NoJaggedArrays

- **Wrong rule:** Every row of the transition matrix must be stored with the same length because 2-D arrays are always rectangular.
- **Right rule:** Each p[i] is its own row array; the surfer's matrix is square only because every page has a row of n probabilities.
- **Role of this concept:** context
- **Shows at level L0 as:** misconception: wrong rule: Multi-dimensional arrays must be rectangular. Right rule: Each row is its own array, so rows can differ in length (a ragged array); the transition matrix is created square with new double[N][N].
- **Also an edge from `ragged_array`:** multi-dimensional arrays must be rectangular
- **Also an edge from `two_dimensional_array`:** Every row of a 2-D array must have the same length.

### RowsNeedNotSumToOne

- **Wrong rule:** A page with no outgoing links can have an all-zero row.
- **Right rule:** Each row is a probability distribution; a page with no links is made equally likely to move to every page.
- **Role of this concept:** context
- **Shows at level L0 as:** misconception: wrong rule: A page with no outgoing links can have an all-zero row. Right rule: Every row must be a probability distribution summing to 1; a page with no links gets 1/N in every column.
- **Also an edge from `dangling_pages`:** A page with no outgoing links can have an all-zero row.
- **Also an edge from `normalization`:** A page with no outgoing links can have an all-zero row.

## Errors (0)

An error edge states the rule that gets broken in a program, and the right rule.

The graph has no error edge from this concept.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for transition matrix: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to transition matrix agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

transition matrix -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (4 ways).

- **everyday reading** (folk-meaning rule): In maths classes a transition matrix is often written column-wise (column = from), and "matrix" suggests a table of counts; in SW p[i][j] is a probability, row i = the page the surfer is on, column j = the page moved to, and each row sums to 1.
- **misconception** (wrong rule / right rule; shows `MultidimensionalArray`): wrong rule: A 2-D array is one thing, not an array of arrays. Right rule: Java represents p[][] as an array of N row arrays; p[page] is itself a 1-D double array (the distribution used by the random move).
- **misconception** (wrong rule / right rule; shows `NoJaggedArrays`): wrong rule: Multi-dimensional arrays must be rectangular. Right rule: Each row is its own array, so rows can differ in length (a ragged array); the transition matrix is created square with new double[N][N].
- **misconception** (wrong rule / right rule; shows `RowsNeedNotSumToOne`): wrong rule: A page with no outgoing links can have an all-zero row. Right rule: Every row must be a probability distribution summing to 1; a page with no links gets 1/N in every column.

### L1: Unistructural / atom x text surface

L1 for transition matrix: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

transition matrix -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

- **names the element** (identity rule): A data structure: an N-by-N two-dimensional double array p[][] (a stochastic matrix) whose entry p[i][j] is the probability of moving from page i to page j.
- **states the rule** (declarative rule): Entry (i, j) is the probability that the surfer on page i moves to page j; by the 90-10 rule it is .90\*counts[i][j]/outDegree[i] + .10/N, and every row is a discrete probability distribution summing to 1.

### L2: Multistructural / block x execution / preoperational

L2 for transition matrix: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

transition matrix -&gt; L2 (Multistructural): the answer applies the rules of transition matrix to every part of the code, in order (3 ways).

- **line by line trace** (operational sequencing rule): Three steps in order: read N and create counts[][] and outDegree[]; read all links and accumulate counts; then, row by row (outer i) and column by column (inner j), compute and print one probability; the header "N N" is printed before the rows.
- **output prediction** (evaluation / result rule): Output is a matrix file: the row and column counts, then N rows of N doubles printed with %8.5f; for tiny.txt row 0 is 0.02000 0.92000 0.02000 0.02000 0.02000 and row 1 is 0.02000 0.02000 0.38000 0.38000 0.20000.
- **one step execution** (state-transition rule): One inner-loop pass evaluates one double p for the current (i, j) from counts[i][j], outDegree[i] and N, and prints it; no array is modified by this phase.

### L3: Relational / relations x function (concrete operational begins)

L3 for transition matrix: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

transition matrix -&gt; L3 (Relational): the answer relates the parts (8 ways).

- **relation to neighbour** (composition rule (with a neighbour)): Row i depends only on the tallies read for page i (counts[i][] and outDegree[i]); the matrix cannot be computed until all links have been read.
- **relation to neighbour** (composition rule (with a neighbour)): Dividing counts[i][j] by outDegree[i] (after scaling by .90) and adding .10/N is the normalisation that makes row i sum to 1; the double operand .90 keeps the division from being integer division.
- **relation to neighbour** (composition rule (with a neighbour)): The random move reads one row p[page] as a 1-D array and accumulates its entries; it only works if that row sums to 1.
- **relation to neighbour** (composition rule (with a neighbour)): The matrix is double[N][N]: p[i] is the row array for page i and p[i][j] an element; indices must be in 0..N-1 and the first index is the row (from-page).
- **relation to neighbour** (composition rule (with a neighbour)): A matrix whose rows are probability distributions defines a Markov chain: the next page depends only on the current page's row.
- **relation to neighbour** (composition rule (with a neighbour)): Transition's formula is valid only if every outDegree[i] &gt; 0; a page with no outlinks must have its row filled with 1/N.
- **relation to neighbour** (composition rule (with a neighbour)): The .10/N term, added to every entry, is the teleport (random-page) part of each row; the .90 factor scales the link part so the two parts sum to 1.
- **purpose of the whole** (plan / role rule): Specifies completely the surfer's behaviour as data; Transition is a filter turning the list-of-links representation into a matrix that RandomSurfer and Markov both read.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for transition matrix: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

transition matrix -&gt; L4 (Extended abstract): the answer reasons beyond the given code (5 ways).

- **predict a change** (conservation rule): Invariant: every row sums to 1. Changing the split to 80-20 or 95-5 keeps it (the two weights still sum to 1) but changes the ranks; changing .10/N to .10, or omitting the leap term, breaks it.
- **transfer to a new program** (applicability rule): Right tool when the model has few enough pages that N\*N doubles fit in memory and both simulation and the power method need per-pair probabilities; not for millions of pages (trillions of entries).
- **diagnose an error** (error rule): rule broken: outDegree[i] must be &gt; 0 (no dangling pages). Kind: silent logic error. Trigger class: A page with no outlinks: .90\*counts[i][j] is the double 0.0 and 0.0/0 gives NaN, so the whole row prints NaN with no exception.
- **diagnose an error** (error rule): rule broken: Each row must sum to 1. Kind: silent logic error. Trigger class: Any row whose entries do not sum to 1 (wrong scaling, missing leap term, unhandled dangling page) makes the RandomSurfer move fail.
- **diagnose an error** (error rule): rule broken: Indices i, j must be in 0..N-1. Kind: run-time exception. Trigger class: Link with page &gt;= N, or loop bound &lt;= N: ArrayIndexOutOfBoundsException.

## Same topic

`transition_matrix` belongs to the topic **Input format and transition matrix** (`topic1.6.a`). The topic also contains: `dangling_pages`, `input_graph`, `normalization`, `teleportation`.

## Rules of the concept (23)

- **folk-meaning rule:** In maths classes a transition matrix is often written column-wise (column = from), and "matrix" suggests a table of counts; in SW p[i][j] is a probability, row i = the page the surfer is on, column j = the page moved to, and each row sums to 1.
- **wrong rule / right rule:** MultidimensionalArray: wrong: A 2-D array is one thing, not an array of arrays. \| right: Java represents p[][] as an array of N row arrays; p[page] is itself a 1-D double array (the distribution used by the random move).
- **wrong rule / right rule:** NoJaggedArrays: wrong: Multi-dimensional arrays must be rectangular. \| right: Each row is its own array, so rows can differ in length (a ragged array); the transition matrix is created square with new double[N][N].
- **wrong rule / right rule:** RowsNeedNotSumToOne: wrong: A page with no outgoing links can have an all-zero row. \| right: Every row must be a probability distribution summing to 1; a page with no links gets 1/N in every column.
- **uneven-application rule:** Applies LT (for each row i, for each column j: .90\*counts[i][j]/outDegree[i] + .10/N) unevenly: e.g. adds the .10/N leap term only to entries that have a link, or divides by outDegree[j] (the column page) on some entries, so some rows no longer sum to 1.
- **identity rule:** A data structure: an N-by-N two-dimensional double array p[][] (a stochastic matrix) whose entry p[i][j] is the probability of moving from page i to page j.
- **declarative rule:** Entry (i, j) is the probability that the surfer on page i moves to page j; by the 90-10 rule it is .90\*counts[i][j]/outDegree[i] + .10/N, and every row is a discrete probability distribution summing to 1.
- **operational sequencing rule:** Three steps in order: read N and create counts[][] and outDegree[]; read all links and accumulate counts; then, row by row (outer i) and column by column (inner j), compute and print one probability; the header "N N" is printed before the rows.
- **evaluation / result rule:** Output is a matrix file: the row and column counts, then N rows of N doubles printed with %8.5f; for tiny.txt row 0 is 0.02000 0.92000 0.02000 0.02000 0.02000 and row 1 is 0.02000 0.02000 0.38000 0.38000 0.20000.
- **state-transition rule:** One inner-loop pass evaluates one double p for the current (i, j) from counts[i][j], outDegree[i] and N, and prints it; no array is modified by this phase.
- **composition rule (with a neighbour):** with input\_graph: Row i depends only on the tallies read for page i (counts[i][] and outDegree[i]); the matrix cannot be computed until all links have been read.
- **composition rule (with a neighbour):** with normalization: Dividing counts[i][j] by outDegree[i] (after scaling by .90) and adding .10/N is the normalisation that makes row i sum to 1; the double operand .90 keeps the division from being integer division.
- **composition rule (with a neighbour):** with random\_move: The random move reads one row p[page] as a 1-D array and accumulates its entries; it only works if that row sums to 1.
- **composition rule (with a neighbour):** with two\_dimensional\_array: The matrix is double[N][N]: p[i] is the row array for page i and p[i][j] an element; indices must be in 0..N-1 and the first index is the row (from-page).
- **composition rule (with a neighbour):** with markov\_chain: A matrix whose rows are probability distributions defines a Markov chain: the next page depends only on the current page's row.
- **composition rule (with a neighbour):** with dangling\_pages: Transition's formula is valid only if every outDegree[i] &gt; 0; a page with no outlinks must have its row filled with 1/N.
- **composition rule (with a neighbour):** with teleportation: The .10/N term, added to every entry, is the teleport (random-page) part of each row; the .90 factor scales the link part so the two parts sum to 1.
- **plan / role rule:** Specifies completely the surfer's behaviour as data; Transition is a filter turning the list-of-links representation into a matrix that RandomSurfer and Markov both read.
- **conservation rule:** Invariant: every row sums to 1. Changing the split to 80-20 or 95-5 keeps it (the two weights still sum to 1) but changes the ranks; changing .10/N to .10, or omitting the leap term, breaks it.
- **error rule:** rule broken: outDegree[i] must be &gt; 0 (no dangling pages). (silent logic error)
- **error rule:** rule broken: Each row must sum to 1. (silent logic error)
- **error rule:** rule broken: Indices i, j must be in 0..N-1. (run-time exception)
- **applicability rule:** Right tool when the model has few enough pages that N\*N doubles fit in memory and both simulation and the power method need per-pair probabilities; not for millions of pages (trillions of entries).

## The whole prerequisite chain

- **Everything it builds on (11):** `array_creation`, `array_declaration`, `array_initializer`, `data_structure`, `data_type`, `indexing`, `input_graph`, `standard_input`, `stream_model`, `teleportation`, `two_dimensional_array`
- **Everything that builds on it (9):** `convergence_rate`, `dangling_pages`, `frequency_counting`, `markov_chain`, `normalization`, `power_method`, `random_move`, `simulation_loop`, `two_models`
