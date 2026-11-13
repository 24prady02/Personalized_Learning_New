# dangling_pages (`dangling_pages`)

pages with no outgoing links

Section 1.6 Case Study: Random Web Surfer, topic 1.6.a Input format and transition matrix.

![The knowledge graph around dangling_pages](dangling_pages.png)

## At a glance

- **Needs first:** `transition_matrix`
- **Leads to:** nothing
- **Learned alongside:** nothing
- **Misconceptions:** `RowsNeedNotSumToOne`
- **Errors:** none
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 14 edges around this concept, each explained in the graph's own words.

## What it needs first (1)

A prerequisite edge means the other concept has to be understood before `dangling_pages`.

### `transition_matrix` comes before `dangling_pages`

*a 2-D array of move probabilities (rows sum to 1)*

Transition assumes that every page has an outgoing link; Exercise 1.6.3 handles a page with no outgoing links by filling its row of the transition matrix with 1/N.

- **Grounding:** book passage
- **How `dangling_pages` combines with `transition_matrix`:** A dangling page is the case where the matrix formula breaks (division by outDegree 0); the 1/N row replaces it so the matrix stays stochastic.
- **How `transition_matrix` combines with `dangling_pages`:** Transition's formula is valid only if every outDegree[i] &gt; 0; a page with no outlinks must have its row filled with 1/N.

## What it leads to (0)

These concepts need `dangling_pages` first.

No concept has this one as a prerequisite.

## Learned alongside (0)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

No parallel edge touches this concept.

## Misconceptions (1)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### RowsNeedNotSumToOne

- **Wrong rule:** A page with no outgoing links can have an all-zero row.
- **Right rule:** Each row is a probability distribution; a page with no links is made equally likely to move to every page.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: A page with no outgoing links can have an all-zero row. Right rule: Every row must sum to 1; fill the row of a page with no outgoing links with 1/N (equally likely to go to every page).
- **Shows at level L0 as:** inconsistent trace: Applies LT (test outDegree[i] == 0 before dividing; if so use 1.0/N for the whole row) unevenly: e.g. tests only on the first column, or still adds the .10/N leap term to the 1/N entries so the row sums to more than 1. (here mixing in: "A page with no outgoing links can have an all-zero row")
- **Also an edge from `normalization`:** A page with no outgoing links can have an all-zero row.
- **Also an edge from `transition_matrix`:** A page with no outgoing links can have an all-zero row.

## Errors (0)

An error edge states the rule that gets broken in a program, and the right rule.

The graph has no error edge from this concept.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for dangling pages: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to dangling pages agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

dangling pages -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (3 ways).

- **everyday reading** (folk-meaning rule): Everyday reading of a "dead-end" page is that the surfer just stops or stays there; in the model the surfer always goes somewhere, so a page with no outlinks must still have a full probability row (1/N to every page).
- **misconception** (wrong rule / right rule; shows `RowsNeedNotSumToOne`): wrong rule: A page with no outgoing links can have an all-zero row. Right rule: Every row must sum to 1; fill the row of a page with no outgoing links with 1/N (equally likely to go to every page).
- **inconsistent trace** (uneven-application rule; shows `RowsNeedNotSumToOne`): Applies LT (test outDegree[i] == 0 before dividing; if so use 1.0/N for the whole row) unevenly: e.g. tests only on the first column, or still adds the .10/N leap term to the 1/N entries so the row sums to more than 1. (here mixing in: "A page with no outgoing links can have an all-zero row")

### L1: Unistructural / atom x text surface

L1 for dangling pages: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

dangling pages -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

- **names the element** (identity rule): A page with no outgoing links (outDegree 0), also called a dangling page or sink; spider traps are sets of such pages.
- **states the rule** (declarative rule): Transition assumes there are none; to handle them, fill the row of every page with no outgoing links with 1/N, which keeps the matrix stochastic.

### L2: Multistructural / block x execution / preoperational

L2 for dangling pages: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

dangling pages -&gt; L2 (Multistructural): the answer applies the rules of dangling pages to every part of the code, in order (3 ways).

- **line by line trace** (operational sequencing rule): For row i: first test outDegree[i] == 0; if true every p[i][j] = 1.0/N; otherwise use .90\*counts[i][j]/outDegree[i] + .10/N. The test must come before the division.
- **output prediction** (evaluation / result rule): A dangling page's row is N equal entries 1/N (for N = 5, 0.20000 each), summing to 1.
- **one step execution** (state-transition rule): Handling one dangling entry sets p[i][j] to the double 1.0/N; counts and outDegree are unchanged.

### L3: Relational / relations x function (concrete operational begins)

L3 for dangling pages: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

dangling pages -&gt; L3 (Relational): the answer relates the parts (2 ways).

- **relation to neighbour** (composition rule (with a neighbour)): A dangling page is the case where the matrix formula breaks (division by outDegree 0); the 1/N row replaces it so the matrix stays stochastic.
- **purpose of the whole** (plan / role rule): A guard / special-case plan: detect the zero-total case and substitute a uniform distribution so later code (random move, power method) can assume every row sums to 1.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for dangling pages: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

dangling pages -&gt; L4 (Extended abstract): the answer reasons beyond the given code (4 ways).

- **predict a change** (conservation rule; shows `RowsNeedNotSumToOne`): Filling with 1/N keeps the row-sum invariant; writing 1/N with int operands (0) or leaving the row as computed (NaN) breaks it, and RandomSurfer then fails.
- **transfer to a new program** (applicability rule): Needed whenever the input may contain pages with no outlinks (as the real web does, e.g. spider traps); unnecessary when every page has at least one outlink, as Transition assumes.
- **diagnose an error** (error rule): rule broken: Transition assumes no page lacks outlinks. Kind: silent logic error. Trigger class: Input with a page that never appears as i: its row is NaN (0.0/0), and RandomSurfer's test r &lt; sum is always false on that row, so the surfer never leaves.
- **diagnose an error** (error rule): rule broken: 1/N must be computed in floating point. Kind: silent logic error. Trigger class: Fill value written as 1/N with int N &gt; 1: every entry is 0 and the row sums to 0.

## Same topic

`dangling_pages` belongs to the topic **Input format and transition matrix** (`topic1.6.a`). The topic also contains: `input_graph`, `normalization`, `teleportation`, `transition_matrix`.

## Rules of the concept (14)

- **folk-meaning rule:** Everyday reading of a "dead-end" page is that the surfer just stops or stays there; in the model the surfer always goes somewhere, so a page with no outlinks must still have a full probability row (1/N to every page).
- **wrong rule / right rule:** RowsNeedNotSumToOne: wrong: A page with no outgoing links can have an all-zero row. \| right: Every row must sum to 1; fill the row of a page with no outgoing links with 1/N (equally likely to go to every page).
- **uneven-application rule:** Applies LT (test outDegree[i] == 0 before dividing; if so use 1.0/N for the whole row) unevenly: e.g. tests only on the first column, or still adds the .10/N leap term to the 1/N entries so the row sums to more than 1.
- **identity rule:** A page with no outgoing links (outDegree 0), also called a dangling page or sink; spider traps are sets of such pages.
- **declarative rule:** Transition assumes there are none; to handle them, fill the row of every page with no outgoing links with 1/N, which keeps the matrix stochastic.
- **operational sequencing rule:** For row i: first test outDegree[i] == 0; if true every p[i][j] = 1.0/N; otherwise use .90\*counts[i][j]/outDegree[i] + .10/N. The test must come before the division.
- **evaluation / result rule:** A dangling page's row is N equal entries 1/N (for N = 5, 0.20000 each), summing to 1.
- **state-transition rule:** Handling one dangling entry sets p[i][j] to the double 1.0/N; counts and outDegree are unchanged.
- **composition rule (with a neighbour):** with transition\_matrix: A dangling page is the case where the matrix formula breaks (division by outDegree 0); the 1/N row replaces it so the matrix stays stochastic.
- **plan / role rule:** A guard / special-case plan: detect the zero-total case and substitute a uniform distribution so later code (random move, power method) can assume every row sums to 1.
- **conservation rule:** Filling with 1/N keeps the row-sum invariant; writing 1/N with int operands (0) or leaving the row as computed (NaN) breaks it, and RandomSurfer then fails.
- **error rule:** rule broken: Transition assumes no page lacks outlinks. (silent logic error)
- **error rule:** rule broken: 1/N must be computed in floating point. (silent logic error)
- **applicability rule:** Needed whenever the input may contain pages with no outlinks (as the real web does, e.g. spider traps); unnecessary when every page has at least one outlink, as Transition assumes.

## The whole prerequisite chain

- **Everything it builds on (12):** `array_creation`, `array_declaration`, `array_initializer`, `data_structure`, `data_type`, `indexing`, `input_graph`, `standard_input`, `stream_model`, `teleportation`, `transition_matrix`, `two_dimensional_array`
- **Everything that builds on it (0):** nothing
