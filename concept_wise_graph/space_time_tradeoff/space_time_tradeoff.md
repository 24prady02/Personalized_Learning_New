# Space-time tradeoff (`space_time_tradeoff`)

investing memory (an array of saved values) to save computation time

Section 1.4 1.4 Arrays, topic 1.4.e Precomputed values and simplifying repetitive code.

![The knowledge graph around space_time_tradeoff](space_time_tradeoff.png)

## At a glance

- **Needs first:** `indexing`, `lookup_table`
- **Leads to:** nothing
- **Learned alongside:** nothing
- **Misconceptions:** none
- **Errors:** none
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 9 edges around this concept, each explained in the graph's own words.

## What it needs first (2)

A prerequisite edge means the other concept has to be understood before `space_time_tradeoff`.

### `indexing` comes before `space_time_tradeoff`

*a[i] -- 0-based access*

Saved values are read back by index, H[i], instead of being recomputed.

- **Grounding:** book passage

### `lookup_table` comes before `space_time_tradeoff`

*an array of precomputed values or names indexed by position*

Saving precomputed values in an array trades memory for time: each value is computed once and then looked up.

- **Grounding:** book passage
- **How `space_time_tradeoff` combines with `lookup_table`:** The lookup table is the stored space: each value is computed once and then read by index.
- **How `lookup_table` combines with `space_time_tradeoff`:** Storing precomputed values trades memory for time: each value is computed once and then looked up.

## What it leads to (0)

These concepts need `space_time_tradeoff` first.

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

L0 for Space-time tradeoff: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to Space-time tradeoff agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

Space-time tradeoff -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (1 way).

- **everyday reading** (folk-meaning rule): Folk meaning: saving results is always better, and storing data is free. Rule: precomputation spends memory proportional to the number of saved values to save time, which pays off only when values are reused and the table fits in memory.

### L1: Unistructural / atom x text surface

L1 for Space-time tradeoff: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

Space-time tradeoff -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

- **names the element** (identity rule): Identity: a space-time tradeoff invests memory (an array of saved values) to save computation time.
- **states the rule** (declarative rule): Declarative: by investing in space (saving values) we save time (no recomputation). PrimeSieve trades a boolean array of size N for speed over the two-variable trial-division method.

### L2: Multistructural / block x execution / preoperational

L2 for Space-time tradeoff: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

Space-time tradeoff -&gt; L2 (Multistructural): the answer applies the rules of Space-time tradeoff to every part of the code, in order (3 ways).

- **line by line trace** (operational sequencing rule): Sequencing: a precompute phase (one pass storing N values) runs first, then a use phase in which each query is one array read.
- **output prediction** (evaluation / result rule): Result: the same answers as recomputation, using about N extra memory cells and much less time per query.
- **one step execution** (state-transition rule): State transition: during precomputation each step stores one value in the table; during use each lookup changes nothing.

### L3: Relational / relations x function (concrete operational begins)

L3 for Space-time tradeoff: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

Space-time tradeoff -&gt; L3 (Relational): the answer relates the parts (2 ways).

- **relation to neighbour** (composition rule (with a neighbour)): The lookup table is the stored space: each value is computed once and then read by index.
- **purpose of the whole** (plan / role rule): Plan/role: speed up programs that need the same values many times (harmonic numbers, primes up to N).

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for Space-time tradeoff: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

Space-time tradeoff -&gt; L4 (Extended abstract): the answer reasons beyond the given code (4 ways).

- **predict a change** (conservation rule): Conservation: results are unchanged by precomputing. Memory grows linearly with N, so for huge N or for values used only once the tradeoff stops paying.
- **transfer to a new program** (applicability rule): Applicability: precompute when the values are needed for small N many times and memory is ample. Recompute when N is huge, memory is tight, or each value is used once.
- **diagnose an error** (error rule): rule broken: The table must fit in the memory Java allows. Kind: run-time exception. Trigger class: N too large for the array (OutOfMemoryError, or NegativeArraySizeException if N+1 overflows)
- **diagnose an error** (error rule): rule broken: Precomputation pays only when values are reused. Kind: silent logic error. Trigger class: a huge table is built for a single query, so the program is slower and larger with no benefit

## Same topic

`space_time_tradeoff` belongs to the topic **Precomputed values and simplifying repetitive code** (`topic1.4.e`). The topic also contains: `lookup_table`.

## Rules of the concept (13)

- **folk-meaning rule:** Folk meaning: saving results is always better, and storing data is free. Rule: precomputation spends memory proportional to the number of saved values to save time, which pays off only when values are reused and the table fits in memory.
- **uneven-application rule:** Points to LT: precompute every value once, then answer each query by lookup. Inconsistent application: the trace recomputes some values despite the table, or reads entries before they are computed.
- **identity rule:** Identity: a space-time tradeoff invests memory (an array of saved values) to save computation time.
- **declarative rule:** Declarative: by investing in space (saving values) we save time (no recomputation). PrimeSieve trades a boolean array of size N for speed over the two-variable trial-division method.
- **operational sequencing rule:** Sequencing: a precompute phase (one pass storing N values) runs first, then a use phase in which each query is one array read.
- **evaluation / result rule:** Result: the same answers as recomputation, using about N extra memory cells and much less time per query.
- **state-transition rule:** State transition: during precomputation each step stores one value in the table; during use each lookup changes nothing.
- **composition rule (with a neighbour):** with lookup\_table: The lookup table is the stored space: each value is computed once and then read by index.
- **plan / role rule:** Plan/role: speed up programs that need the same values many times (harmonic numbers, primes up to N).
- **conservation rule:** Conservation: results are unchanged by precomputing. Memory grows linearly with N, so for huge N or for values used only once the tradeoff stops paying.
- **error rule:** rule broken: The table must fit in the memory Java allows. (run-time exception)
- **error rule:** rule broken: Precomputation pays only when values are reused. (silent logic error)
- **applicability rule:** Applicability: precompute when the values are needed for small N many times and memory is ample. Recompute when N is huge, memory is tight, or each value is used once.

## The whole prerequisite chain

- **Everything it builds on (7):** `array_creation`, `array_declaration`, `array_initializer`, `data_structure`, `data_type`, `indexing`, `lookup_table`
- **Everything that builds on it (0):** nothing
