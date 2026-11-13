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

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 25 edges around this concept. The edge logic, the wrong and right rules and the exact rules of the ways are copied word for word from the graph.

## To work on (1)

- no aliases: a student's words cannot name this concept

## What it needs first (3)

A prerequisite edge means the other concept has to be understood before `transition_matrix`.

### `input_graph` comes before `transition_matrix`

*read the page links from input*

- **Edge:** `pre:input_graph->transition_matrix`
- **Exact edge logic:** The links read from input fill counts[i][j], and each row of the transition matrix is built from those counts.
- **Grounding:** book\_passage
- **Composition rule (R) of `transition_matrix` with `input_graph`:** Row i depends only on the tallies read for page i (counts[i][] and outDegree[i]); the matrix cannot be computed until all links have been read.
- **Composition rule (R) of `input_graph` with `transition_matrix`:** The tallies constrain the matrix: row i of the matrix is computed only from counts[i][] and outDegree[i], so a mistake in reading pair order (i/j swapped) moves probability mass into the wrong row.

### `teleportation` comes before `transition_matrix`

*the 90-10 rule: follow a link or jump to a random page*

- **Edge:** `pre:teleportation->transition_matrix`
- **Exact edge logic:** The 90-10 rule says the surfer follows a random link 90 percent of the time and jumps to a random page 10 percent of the time, and each transition-matrix entry is computed from it.
- **Grounding:** questionable
- **Composition rule (R) of `transition_matrix` with `teleportation`:** The .10/N term, added to every entry, is the teleport (random-page) part of each row; the .90 factor scales the link part so the two parts sum to 1.
- **Composition rule (R) of `teleportation` with `transition_matrix`:** Every entry is built as link part plus leap part; the .90 and .10 weights must sum to 1 for each row to remain a distribution.

### `two_dimensional_array` comes before `transition_matrix`

*an array of arrays (a[i][j])*

- **Edge:** `pre:two_dimensional_array->transition_matrix`
- **Exact edge logic:** The transition matrix is a 2-D double array p[i][j], with one row array per page.
- **Grounding:** book\_passage
- **Composition rule (R) of `transition_matrix` with `two_dimensional_array`:** The matrix is double[N][N]: p[i] is the row array for page i and p[i][j] an element; indices must be in 0..N-1 and the first index is the row (from-page).
- **Composition rule (R) of `two_dimensional_array` with `transition_matrix`:** The transition matrix is a 2-D double array p[i][j] with one row per page; each row holds a probability distribution.

## What it leads to (4)

These concepts need `transition_matrix` first.

### `transition_matrix` comes before `dangling_pages`

*pages with no outgoing links*

- **Edge:** `pre:transition_matrix->dangling_pages`
- **Exact edge logic:** Transition assumes that every page has an outgoing link; Exercise 1.6.3 handles a page with no outgoing links by filling its row of the transition matrix with 1/N.
- **Grounding:** book\_passage
- **Composition rule (R) of `transition_matrix` with `dangling_pages`:** Transition's formula is valid only if every outDegree[i] &gt; 0; a page with no outlinks must have its row filled with 1/N.
- **Composition rule (R) of `dangling_pages` with `transition_matrix`:** A dangling page is the case where the matrix formula breaks (division by outDegree 0); the 1/N row replaces it so the matrix stays stochastic.

### `transition_matrix` comes before `markov_chain`

*random process where the next state depends only on the current state*

- **Edge:** `pre:transition_matrix->markov_chain`
- **Exact edge logic:** The transition matrix specifies the probability of each move, and the random process those probabilities define is a Markov chain.
- **Grounding:** book\_passage
- **Composition rule (R) of `transition_matrix` with `markov_chain`:** A matrix whose rows are probability distributions defines a Markov chain: the next page depends only on the current page's row.
- **Composition rule (R) of `markov_chain` with `transition_matrix`:** The chain is defined by the matrix: it must be square with every row a probability distribution.

### `transition_matrix` comes before `normalization`

*scaling a row so its probabilities sum to 1*

- **Edge:** `pre:transition_matrix->normalization`
- **Exact edge logic:** Each row of the transition matrix must be a probability distribution, so counts[i][j] is divided by outDegree[i] (scaled by .90, plus .10/N) to make row i sum to 1.
- **Grounding:** book\_passage
- **Composition rule (R) of `transition_matrix` with `normalization`:** Dividing counts[i][j] by outDegree[i] (after scaling by .90) and adding .10/N is the normalisation that makes row i sum to 1; the double operand .90 keeps the division from being integer division.
- **Composition rule (R) of `normalization` with `transition_matrix`:** Normalisation is applied row by row: every entry of row i is divided by the same total outDegree[i], which is what makes the row a distribution the matrix requires.

### `transition_matrix` comes before `random_move`

*pick the next page from a cumulative-probability test*

- **Edge:** `pre:transition_matrix->random_move`
- **Exact edge logic:** Row p[i] is the probability distribution used to choose the next page when the surfer is on page i.
- **Grounding:** book\_passage
- **Composition rule (R) of `transition_matrix` with `random_move`:** The random move reads one row p[page] as a 1-D array and accumulates its entries; it only works if that row sums to 1.
- **Composition rule (R) of `random_move` with `transition_matrix`:** Reads exactly one row p[page]; the row must sum to 1, otherwise r can exceed the final sum and no j is chosen.

## Learned alongside (0)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

No parallel edge touches this concept.

## Misconceptions (3)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### MultidimensionalArray

- **Edge:** `transition_matrix` &rarr; `MultidimensionalArray` (misconception)
- **Exact edge logic (the wrong rule):** The transition matrix is one block of n \* n numbers, so p[i] on its own means nothing.
- **Twin logic (the right rule):** p[i] is the row array of page i, holding the probabilities of moving from page i to every page.
- **Wrong belief (on the node):** a 2-D array is one thing, not an array of arrays
- **Correct rule (on the node):** A 2-D array is an array of m row arrays, so a[i] is a 1-D array of length n.
- **Provenance:** published
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [1] misconception, exact rule:** wrong rule: A 2-D array is one thing, not an array of arrays. Right rule: Java represents p[][] as an array of N row arrays; p[page] is itself a 1-D double array (the distribution used by the random move).
- **Edge `two_dimensional_array` &rarr; `MultidimensionalArray`, exact edge logic:** int[m][n] is one block of m \* n values, so a[i] on its own means nothing. **Twin logic:** A 2-D array is an array of m row arrays, so a[i] is a 1-D array of length n. (role: primary)

### NoJaggedArrays

- **Edge:** `transition_matrix` &rarr; `NoJaggedArrays` (misconception)
- **Exact edge logic (the wrong rule):** Every row of the transition matrix must be stored with the same length because 2-D arrays are always rectangular.
- **Twin logic (the right rule):** Each p[i] is its own row array; the surfer's matrix is square only because every page has a row of n probabilities.
- **Wrong belief (on the node):** multi-dimensional arrays must be rectangular
- **Correct rule (on the node):** Each row a[i] is its own array, so rows can have different lengths a[i].length.
- **Provenance:** published
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [2] misconception, exact rule:** wrong rule: Multi-dimensional arrays must be rectangular. Right rule: Each row is its own array, so rows can differ in length (a ragged array); the transition matrix is created square with new double[N][N].
- **Edge `ragged_array` &rarr; `NoJaggedArrays`, exact edge logic:** multi-dimensional arrays must be rectangular **Twin logic:** Each row a[i] is its own array, so rows can have different lengths a[i].length. (role: primary)
- **Edge `two_dimensional_array` &rarr; `NoJaggedArrays`, exact edge logic:** Every row of a 2-D array must have the same length. **Twin logic:** Each row a[i] is its own array, so rows can have different lengths a[i].length. (role: context)

### RowsNeedNotSumToOne

- **Edge:** `transition_matrix` &rarr; `RowsNeedNotSumToOne` (misconception)
- **Exact edge logic (the wrong rule):** A page with no outgoing links can have an all-zero row.
- **Twin logic (the right rule):** Each row is a probability distribution; a page with no links is made equally likely to move to every page.
- **Wrong belief (on the node):** A page with no outgoing links can have an all-zero row.
- **Correct rule (on the node):** Each row is a probability distribution; a page with no links is made equally likely to move to every page.
- **Provenance:** textbook
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [3] misconception, exact rule:** wrong rule: A page with no outgoing links can have an all-zero row. Right rule: Every row must be a probability distribution summing to 1; a page with no links gets 1/N in every column.
- **Edge `dangling_pages` &rarr; `RowsNeedNotSumToOne`, exact edge logic:** A page with no outgoing links can have an all-zero row. **Twin logic:** Each row is a probability distribution; a page with no links is made equally likely to move to every page. (role: primary)
- **Edge `normalization` &rarr; `RowsNeedNotSumToOne`, exact edge logic:** A page with no outgoing links can have an all-zero row. **Twin logic:** Each row is a probability distribution; a page with no links is made equally likely to move to every page. (role: context)

## Errors (0)

An error edge states the rule that gets broken in a program, and the right rule.

The graph has no error edge from this concept.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for transition matrix: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to transition matrix agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

- **Edge:** `transition_matrix` &rarr; `transition_matrix@L0` (has_level)
- **Exact edge logic:** transition matrix -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (4 ways).

Ways (4), each with its exact rule:

- **[0] everyday\_reading** (rule type E, folk-meaning rule): In maths classes a transition matrix is often written column-wise (column = from), and "matrix" suggests a table of counts; in SW p[i][j] is a probability, row i = the page the surfer is on, column j = the page moved to, and each row sums to 1.
- **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `MultidimensionalArray`: wrong rule: A 2-D array is one thing, not an array of arrays. Right rule: Java represents p[][] as an array of N row arrays; p[page] is itself a 1-D double array (the distribution used by the random move).
- **[2] misconception** (rule type M, wrong rule / right rule) &rarr; `NoJaggedArrays`: wrong rule: Multi-dimensional arrays must be rectangular. Right rule: Each row is its own array, so rows can differ in length (a ragged array); the transition matrix is created square with new double[N][N].
- **[3] misconception** (rule type M, wrong rule / right rule) &rarr; `RowsNeedNotSumToOne`: wrong rule: A page with no outgoing links can have an all-zero row. Right rule: Every row must be a probability distribution summing to 1; a page with no links gets 1/N in every column.

### L1: Unistructural / atom x text surface

L1 for transition matrix: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

- **Edge:** `transition_matrix` &rarr; `transition_matrix@L1` (has_level)
- **Exact edge logic:** transition matrix -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

Ways (2), each with its exact rule:

- **[0] names\_the\_element** (rule type N, identity rule): A data structure: an N-by-N two-dimensional double array p[][] (a stochastic matrix) whose entry p[i][j] is the probability of moving from page i to page j.
- **[1] states\_the\_rule** (rule type S, declarative rule): Entry (i, j) is the probability that the surfer on page i moves to page j; by the 90-10 rule it is .90\*counts[i][j]/outDegree[i] + .10/N, and every row is a discrete probability distribution summing to 1.

### L2: Multistructural / block x execution / preoperational

L2 for transition matrix: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

- **Edge:** `transition_matrix` &rarr; `transition_matrix@L2` (has_level)
- **Exact edge logic:** transition matrix -&gt; L2 (Multistructural): the answer applies the rules of transition matrix to every part of the code, in order (3 ways).

Ways (3), each with its exact rule:

- **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): Three steps in order: read N and create counts[][] and outDegree[]; read all links and accumulate counts; then, row by row (outer i) and column by column (inner j), compute and print one probability; the header "N N" is printed before the rows.
- **[1] output\_prediction** (rule type OP, evaluation / result rule): Output is a matrix file: the row and column counts, then N rows of N doubles printed with %8.5f; for tiny.txt row 0 is 0.02000 0.92000 0.02000 0.02000 0.02000 and row 1 is 0.02000 0.02000 0.38000 0.38000 0.20000.
- **[2] one\_step\_execution** (rule type OS, state-transition rule): One inner-loop pass evaluates one double p for the current (i, j) from counts[i][j], outDegree[i] and N, and prints it; no array is modified by this phase.

### L3: Relational / relations x function (concrete operational begins)

L3 for transition matrix: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

- **Edge:** `transition_matrix` &rarr; `transition_matrix@L3` (has_level)
- **Exact edge logic:** transition matrix -&gt; L3 (Relational): the answer relates the parts (8 ways).

Ways (8), each with its exact rule:

- **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Row i depends only on the tallies read for page i (counts[i][] and outDegree[i]); the matrix cannot be computed until all links have been read.
- **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Dividing counts[i][j] by outDegree[i] (after scaling by .90) and adding .10/N is the normalisation that makes row i sum to 1; the double operand .90 keeps the division from being integer division.
- **[2] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): The random move reads one row p[page] as a 1-D array and accumulates its entries; it only works if that row sums to 1.
- **[3] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): The matrix is double[N][N]: p[i] is the row array for page i and p[i][j] an element; indices must be in 0..N-1 and the first index is the row (from-page).
- **[4] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): A matrix whose rows are probability distributions defines a Markov chain: the next page depends only on the current page's row.
- **[5] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Transition's formula is valid only if every outDegree[i] &gt; 0; a page with no outlinks must have its row filled with 1/N.
- **[6] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): The .10/N term, added to every entry, is the teleport (random-page) part of each row; the .90 factor scales the link part so the two parts sum to 1.
- **[7] purpose\_of\_the\_whole** (rule type P, plan / role rule): Specifies completely the surfer's behaviour as data; Transition is a filter turning the list-of-links representation into a matrix that RandomSurfer and Markov both read.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for transition matrix: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

- **Edge:** `transition_matrix` &rarr; `transition_matrix@L4` (has_level)
- **Exact edge logic:** transition matrix -&gt; L4 (Extended abstract): the answer reasons beyond the given code (5 ways).

Ways (5), each with its exact rule:

- **[0] predict\_a\_change** (rule type C, conservation rule): Invariant: every row sums to 1. Changing the split to 80-20 or 95-5 keeps it (the two weights still sum to 1) but changes the ranks; changing .10/N to .10, or omitting the leap term, breaks it.
- **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Right tool when the model has few enough pages that N\*N doubles fit in memory and both simulation and the power method need per-pair probabilities; not for millions of pages (trillions of entries).
- **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: outDegree[i] must be &gt; 0 (no dangling pages). Kind: silent logic error. Trigger class: A page with no outlinks: .90\*counts[i][j] is the double 0.0 and 0.0/0 gives NaN, so the whole row prints NaN with no exception.
- **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: Each row must sum to 1. Kind: silent logic error. Trigger class: Any row whose entries do not sum to 1 (wrong scaling, missing leap term, unhandled dangling page) makes the RandomSurfer move fail.
- **[4] diagnose\_an\_error** (rule type D, error rule): rule broken: Indices i, j must be in 0..N-1. Kind: run-time exception. Trigger class: Link with page &gt;= N, or loop bound &lt;= N: ArrayIndexOutOfBoundsException.

## Same topic

`transition_matrix` belongs to the topic **Input format and transition matrix** (`topic1.6.a`). The topic also contains: `dangling_pages`, `input_graph`, `normalization`, `teleportation`.

## Rules of the concept (23)

- **Book** (SW-1e, p. 164 (pdf 174)): "With N web pages, we define an N-by-N matrix such that the entry in row i and column j is the probability that the random surfer moves to page j when on page i."
- **Book** (SW-1.6, p. 164 (pdf 174)): "the entry in row i and column j is the probability that the random surfer moves to page j when on page i."
- **Book** (SW-1.6, p. 164 (pdf 174)): "the entry in row i and column j is the probability that the random surfer moves to page j when on page i"
- **E** (folk-meaning rule): In maths classes a transition matrix is often written column-wise (column = from), and "matrix" suggests a table of counts; in SW p[i][j] is a probability, row i = the page the surfer is on, column j = the page moved to, and each row sums to 1.
- **M** (wrong rule / right rule): MultidimensionalArray: wrong: A 2-D array is one thing, not an array of arrays. \| right: Java represents p[][] as an array of N row arrays; p[page] is itself a 1-D double array (the distribution used by the random move).
- **M** (wrong rule / right rule): NoJaggedArrays: wrong: Multi-dimensional arrays must be rectangular. \| right: Each row is its own array, so rows can differ in length (a ragged array); the transition matrix is created square with new double[N][N].
- **M** (wrong rule / right rule): RowsNeedNotSumToOne: wrong: A page with no outgoing links can have an all-zero row. \| right: Every row must be a probability distribution summing to 1; a page with no links gets 1/N in every column.
- **T** (uneven-application rule): Applies LT (for each row i, for each column j: .90\*counts[i][j]/outDegree[i] + .10/N) unevenly: e.g. adds the .10/N leap term only to entries that have a link, or divides by outDegree[j] (the column page) on some entries, so some rows no longer sum to 1.
- **N** (identity rule): A data structure: an N-by-N two-dimensional double array p[][] (a stochastic matrix) whose entry p[i][j] is the probability of moving from page i to page j.
- **S** (declarative rule): Entry (i, j) is the probability that the surfer on page i moves to page j; by the 90-10 rule it is .90\*counts[i][j]/outDegree[i] + .10/N, and every row is a discrete probability distribution summing to 1.
- **LT** (operational sequencing rule): Three steps in order: read N and create counts[][] and outDegree[]; read all links and accumulate counts; then, row by row (outer i) and column by column (inner j), compute and print one probability; the header "N N" is printed before the rows.
- **OP** (evaluation / result rule): Output is a matrix file: the row and column counts, then N rows of N doubles printed with %8.5f; for tiny.txt row 0 is 0.02000 0.92000 0.02000 0.02000 0.02000 and row 1 is 0.02000 0.02000 0.38000 0.38000 0.20000.
- **OS** (state-transition rule): One inner-loop pass evaluates one double p for the current (i, j) from counts[i][j], outDegree[i] and N, and prints it; no array is modified by this phase.
- **R** (composition rule (with a neighbour)): with input\_graph: Row i depends only on the tallies read for page i (counts[i][] and outDegree[i]); the matrix cannot be computed until all links have been read.
- **R** (composition rule (with a neighbour)): with normalization: Dividing counts[i][j] by outDegree[i] (after scaling by .90) and adding .10/N is the normalisation that makes row i sum to 1; the double operand .90 keeps the division from being integer division.
- **R** (composition rule (with a neighbour)): with random\_move: The random move reads one row p[page] as a 1-D array and accumulates its entries; it only works if that row sums to 1.
- **R** (composition rule (with a neighbour)): with two\_dimensional\_array: The matrix is double[N][N]: p[i] is the row array for page i and p[i][j] an element; indices must be in 0..N-1 and the first index is the row (from-page).
- **R** (composition rule (with a neighbour)): with markov\_chain: A matrix whose rows are probability distributions defines a Markov chain: the next page depends only on the current page's row.
- **R** (composition rule (with a neighbour)): with dangling\_pages: Transition's formula is valid only if every outDegree[i] &gt; 0; a page with no outlinks must have its row filled with 1/N.
- **R** (composition rule (with a neighbour)): with teleportation: The .10/N term, added to every entry, is the teleport (random-page) part of each row; the .90 factor scales the link part so the two parts sum to 1.
- **P** (plan / role rule): Specifies completely the surfer's behaviour as data; Transition is a filter turning the list-of-links representation into a matrix that RandomSurfer and Markov both read.
- **C** (conservation rule): Invariant: every row sums to 1. Changing the split to 80-20 or 95-5 keeps it (the two weights still sum to 1) but changes the ranks; changing .10/N to .10, or omitting the leap term, breaks it.
- **D** (error rule): rule broken: outDegree[i] must be &gt; 0 (no dangling pages). (silent logic error)
- **D** (error rule): rule broken: Each row must sum to 1. (silent logic error)
- **D** (error rule): rule broken: Indices i, j must be in 0..N-1. (run-time exception)
- **X** (applicability rule): Right tool when the model has few enough pages that N\*N doubles fit in memory and both simulation and the power method need per-pair probabilities; not for millions of pages (trillions of entries).

## How it is found in code and answers (reader block)

- **Aliases:** none
- **Code patterns:** `\b(?:p|P|trans\w*|prob\w*)\s*\[[^\]]+\]\s*\[[^\]]+\]\s*=`, `\bdouble\s*\[\]\s*\[\]\s*(?:p|P|trans\w*|prob\w*)\b`
- **Operator symbols:** none
- **Java types:** none

## The whole prerequisite chain

- **Everything it builds on (11):** `array_creation`, `array_declaration`, `array_initializer`, `data_structure`, `data_type`, `indexing`, `input_graph`, `standard_input`, `stream_model`, `teleportation`, `two_dimensional_array`
- **Everything that builds on it (9):** `convergence_rate`, `dangling_pages`, `frequency_counting`, `markov_chain`, `normalization`, `power_method`, `random_move`, `simulation_loop`, `two_models`

## Every edge in this view and its exact edge logic (25)

All the edges drawn in the picture, in the order: prerequisite, parallel, misconception, error, has_level, contains.

**1. `input_graph` &rarr; `transition_matrix`** (prerequisite)

- **Exact edge logic:** The links read from input fill counts[i][j], and each row of the transition matrix is built from those counts.
- **Grounding:** book\_passage
- **Composition rule (R) of `input_graph` with `transition_matrix`:** The tallies constrain the matrix: row i of the matrix is computed only from counts[i][] and outDegree[i], so a mistake in reading pair order (i/j swapped) moves probability mass into the wrong row.
- **Composition rule (R) of `transition_matrix` with `input_graph`:** Row i depends only on the tallies read for page i (counts[i][] and outDegree[i]); the matrix cannot be computed until all links have been read.

**2. `teleportation` &rarr; `transition_matrix`** (prerequisite)

- **Exact edge logic:** The 90-10 rule says the surfer follows a random link 90 percent of the time and jumps to a random page 10 percent of the time, and each transition-matrix entry is computed from it.
- **Grounding:** questionable
- **Composition rule (R) of `teleportation` with `transition_matrix`:** Every entry is built as link part plus leap part; the .90 and .10 weights must sum to 1 for each row to remain a distribution.
- **Composition rule (R) of `transition_matrix` with `teleportation`:** The .10/N term, added to every entry, is the teleport (random-page) part of each row; the .90 factor scales the link part so the two parts sum to 1.

**3. `transition_matrix` &rarr; `dangling_pages`** (prerequisite)

- **Exact edge logic:** Transition assumes that every page has an outgoing link; Exercise 1.6.3 handles a page with no outgoing links by filling its row of the transition matrix with 1/N.
- **Grounding:** book\_passage
- **Composition rule (R) of `transition_matrix` with `dangling_pages`:** Transition's formula is valid only if every outDegree[i] &gt; 0; a page with no outlinks must have its row filled with 1/N.
- **Composition rule (R) of `dangling_pages` with `transition_matrix`:** A dangling page is the case where the matrix formula breaks (division by outDegree 0); the 1/N row replaces it so the matrix stays stochastic.

**4. `transition_matrix` &rarr; `markov_chain`** (prerequisite)

- **Exact edge logic:** The transition matrix specifies the probability of each move, and the random process those probabilities define is a Markov chain.
- **Grounding:** book\_passage
- **Composition rule (R) of `transition_matrix` with `markov_chain`:** A matrix whose rows are probability distributions defines a Markov chain: the next page depends only on the current page's row.
- **Composition rule (R) of `markov_chain` with `transition_matrix`:** The chain is defined by the matrix: it must be square with every row a probability distribution.

**5. `transition_matrix` &rarr; `normalization`** (prerequisite)

- **Exact edge logic:** Each row of the transition matrix must be a probability distribution, so counts[i][j] is divided by outDegree[i] (scaled by .90, plus .10/N) to make row i sum to 1.
- **Grounding:** book\_passage
- **Composition rule (R) of `transition_matrix` with `normalization`:** Dividing counts[i][j] by outDegree[i] (after scaling by .90) and adding .10/N is the normalisation that makes row i sum to 1; the double operand .90 keeps the division from being integer division.
- **Composition rule (R) of `normalization` with `transition_matrix`:** Normalisation is applied row by row: every entry of row i is divided by the same total outDegree[i], which is what makes the row a distribution the matrix requires.

**6. `transition_matrix` &rarr; `random_move`** (prerequisite)

- **Exact edge logic:** Row p[i] is the probability distribution used to choose the next page when the surfer is on page i.
- **Grounding:** book\_passage
- **Composition rule (R) of `transition_matrix` with `random_move`:** The random move reads one row p[page] as a 1-D array and accumulates its entries; it only works if that row sums to 1.
- **Composition rule (R) of `random_move` with `transition_matrix`:** Reads exactly one row p[page]; the row must sum to 1, otherwise r can exceed the final sum and no j is chosen.

**7. `two_dimensional_array` &rarr; `transition_matrix`** (prerequisite)

- **Exact edge logic:** The transition matrix is a 2-D double array p[i][j], with one row array per page.
- **Grounding:** book\_passage
- **Composition rule (R) of `two_dimensional_array` with `transition_matrix`:** The transition matrix is a 2-D double array p[i][j] with one row per page; each row holds a probability distribution.
- **Composition rule (R) of `transition_matrix` with `two_dimensional_array`:** The matrix is double[N][N]: p[i] is the row array for page i and p[i][j] an element; indices must be in 0..N-1 and the first index is the row (from-page).

**8. `transition_matrix` &rarr; `MultidimensionalArray`** (misconception)

- **Exact edge logic (the wrong rule):** The transition matrix is one block of n \* n numbers, so p[i] on its own means nothing.
- **Twin logic (the right rule):** p[i] is the row array of page i, holding the probabilities of moving from page i to every page.
- **Role:** context

**9. `transition_matrix` &rarr; `NoJaggedArrays`** (misconception)

- **Exact edge logic (the wrong rule):** Every row of the transition matrix must be stored with the same length because 2-D arrays are always rectangular.
- **Twin logic (the right rule):** Each p[i] is its own row array; the surfer's matrix is square only because every page has a row of n probabilities.
- **Role:** context

**10. `transition_matrix` &rarr; `RowsNeedNotSumToOne`** (misconception)

- **Exact edge logic (the wrong rule):** A page with no outgoing links can have an all-zero row.
- **Twin logic (the right rule):** Each row is a probability distribution; a page with no links is made equally likely to move to every page.
- **Role:** context

**11. `dangling_pages` &rarr; `RowsNeedNotSumToOne`** (misconception)

- **Exact edge logic (the wrong rule):** A page with no outgoing links can have an all-zero row.
- **Twin logic (the right rule):** Each row is a probability distribution; a page with no links is made equally likely to move to every page.
- **Role:** primary

**12. `normalization` &rarr; `RowsNeedNotSumToOne`** (misconception)

- **Exact edge logic (the wrong rule):** A page with no outgoing links can have an all-zero row.
- **Twin logic (the right rule):** Each row is a probability distribution; a page with no links is made equally likely to move to every page.
- **Role:** context

**13. `ragged_array` &rarr; `NoJaggedArrays`** (misconception)

- **Exact edge logic (the wrong rule):** multi-dimensional arrays must be rectangular
- **Twin logic (the right rule):** Each row a[i] is its own array, so rows can have different lengths a[i].length.
- **Role:** primary

**14. `two_dimensional_array` &rarr; `MultidimensionalArray`** (misconception)

- **Exact edge logic (the wrong rule):** int[m][n] is one block of m \* n values, so a[i] on its own means nothing.
- **Twin logic (the right rule):** A 2-D array is an array of m row arrays, so a[i] is a 1-D array of length n.
- **Role:** primary

**15. `two_dimensional_array` &rarr; `NoJaggedArrays`** (misconception)

- **Exact edge logic (the wrong rule):** Every row of a 2-D array must have the same length.
- **Twin logic (the right rule):** Each row a[i] is its own array, so rows can have different lengths a[i].length.
- **Role:** context

**16. `transition_matrix` &rarr; `transition_matrix@L0`** (has_level)

- **Exact edge logic:** transition matrix -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (4 ways).
  - **[0] everyday\_reading** (rule type E, folk-meaning rule): In maths classes a transition matrix is often written column-wise (column = from), and "matrix" suggests a table of counts; in SW p[i][j] is a probability, row i = the page the surfer is on, column j = the page moved to, and each row sums to 1.
  - **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `MultidimensionalArray`: wrong rule: A 2-D array is one thing, not an array of arrays. Right rule: Java represents p[][] as an array of N row arrays; p[page] is itself a 1-D double array (the distribution used by the random move).
  - **[2] misconception** (rule type M, wrong rule / right rule) &rarr; `NoJaggedArrays`: wrong rule: Multi-dimensional arrays must be rectangular. Right rule: Each row is its own array, so rows can differ in length (a ragged array); the transition matrix is created square with new double[N][N].
  - **[3] misconception** (rule type M, wrong rule / right rule) &rarr; `RowsNeedNotSumToOne`: wrong rule: A page with no outgoing links can have an all-zero row. Right rule: Every row must be a probability distribution summing to 1; a page with no links gets 1/N in every column.

**17. `transition_matrix` &rarr; `transition_matrix@L1`** (has_level)

- **Exact edge logic:** transition matrix -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).
  - **[0] names\_the\_element** (rule type N, identity rule): A data structure: an N-by-N two-dimensional double array p[][] (a stochastic matrix) whose entry p[i][j] is the probability of moving from page i to page j.
  - **[1] states\_the\_rule** (rule type S, declarative rule): Entry (i, j) is the probability that the surfer on page i moves to page j; by the 90-10 rule it is .90\*counts[i][j]/outDegree[i] + .10/N, and every row is a discrete probability distribution summing to 1.

**18. `transition_matrix` &rarr; `transition_matrix@L2`** (has_level)

- **Exact edge logic:** transition matrix -&gt; L2 (Multistructural): the answer applies the rules of transition matrix to every part of the code, in order (3 ways).
  - **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): Three steps in order: read N and create counts[][] and outDegree[]; read all links and accumulate counts; then, row by row (outer i) and column by column (inner j), compute and print one probability; the header "N N" is printed before the rows.
  - **[1] output\_prediction** (rule type OP, evaluation / result rule): Output is a matrix file: the row and column counts, then N rows of N doubles printed with %8.5f; for tiny.txt row 0 is 0.02000 0.92000 0.02000 0.02000 0.02000 and row 1 is 0.02000 0.02000 0.38000 0.38000 0.20000.
  - **[2] one\_step\_execution** (rule type OS, state-transition rule): One inner-loop pass evaluates one double p for the current (i, j) from counts[i][j], outDegree[i] and N, and prints it; no array is modified by this phase.

**19. `transition_matrix` &rarr; `transition_matrix@L3`** (has_level)

- **Exact edge logic:** transition matrix -&gt; L3 (Relational): the answer relates the parts (8 ways).
  - **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Row i depends only on the tallies read for page i (counts[i][] and outDegree[i]); the matrix cannot be computed until all links have been read.
  - **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Dividing counts[i][j] by outDegree[i] (after scaling by .90) and adding .10/N is the normalisation that makes row i sum to 1; the double operand .90 keeps the division from being integer division.
  - **[2] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): The random move reads one row p[page] as a 1-D array and accumulates its entries; it only works if that row sums to 1.
  - **[3] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): The matrix is double[N][N]: p[i] is the row array for page i and p[i][j] an element; indices must be in 0..N-1 and the first index is the row (from-page).
  - **[4] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): A matrix whose rows are probability distributions defines a Markov chain: the next page depends only on the current page's row.
  - **[5] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Transition's formula is valid only if every outDegree[i] &gt; 0; a page with no outlinks must have its row filled with 1/N.
  - **[6] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): The .10/N term, added to every entry, is the teleport (random-page) part of each row; the .90 factor scales the link part so the two parts sum to 1.
  - **[7] purpose\_of\_the\_whole** (rule type P, plan / role rule): Specifies completely the surfer's behaviour as data; Transition is a filter turning the list-of-links representation into a matrix that RandomSurfer and Markov both read.

**20. `transition_matrix` &rarr; `transition_matrix@L4`** (has_level)

- **Exact edge logic:** transition matrix -&gt; L4 (Extended abstract): the answer reasons beyond the given code (5 ways).
  - **[0] predict\_a\_change** (rule type C, conservation rule): Invariant: every row sums to 1. Changing the split to 80-20 or 95-5 keeps it (the two weights still sum to 1) but changes the ranks; changing .10/N to .10, or omitting the leap term, breaks it.
  - **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Right tool when the model has few enough pages that N\*N doubles fit in memory and both simulation and the power method need per-pair probabilities; not for millions of pages (trillions of entries).
  - **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: outDegree[i] must be &gt; 0 (no dangling pages). Kind: silent logic error. Trigger class: A page with no outlinks: .90\*counts[i][j] is the double 0.0 and 0.0/0 gives NaN, so the whole row prints NaN with no exception.
  - **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: Each row must sum to 1. Kind: silent logic error. Trigger class: Any row whose entries do not sum to 1 (wrong scaling, missing leap term, unhandled dangling page) makes the RandomSurfer move fail.
  - **[4] diagnose\_an\_error** (rule type D, error rule): rule broken: Indices i, j must be in 0..N-1. Kind: run-time exception. Trigger class: Link with page &gt;= N, or loop bound &lt;= N: ArrayIndexOutOfBoundsException.

**21. `topic1.6.a` &rarr; `transition_matrix`** (contains)

- topic `topic1.6.a` contains `transition_matrix`

**22. `topic1.6.a` &rarr; `dangling_pages`** (contains)

- topic `topic1.6.a` contains `dangling_pages`

**23. `topic1.6.a` &rarr; `input_graph`** (contains)

- topic `topic1.6.a` contains `input_graph`

**24. `topic1.6.a` &rarr; `normalization`** (contains)

- topic `topic1.6.a` contains `normalization`

**25. `topic1.6.a` &rarr; `teleportation`** (contains)

- topic `topic1.6.a` contains `teleportation`
