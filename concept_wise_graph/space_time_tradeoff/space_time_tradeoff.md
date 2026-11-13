# Space-time tradeoff (`space_time_tradeoff`)

investing memory (an array of saved values) to save computation time

Section 1.4 1.4 Arrays, topic 1.4.e Precomputed values and simplifying repetitive code. From the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`).

![The knowledge graph around space_time_tradeoff](space_time_tradeoff.png)

## Concepts associated with space\_time\_tradeoff (2)

| Concept | Description | How it is associated |
| --- | --- | --- |
| **indexing** | a[i] -- 0-based access | prerequisite of it (it needs this) |
| **lookup\_table** | an array of precomputed values or names indexed by position | prerequisite of it (it needs this)<br>composition rule (R) with it<br>same topic (topic1.4.e) |

## Every edge in this view and its full label (9)

| From | Edge | To | Full edge label |
| --- | --- | --- | --- |
| **indexing** | prerequisite | **space\_time\_tradeoff** | Saved values are read back by index, H[i], instead of being recomputed.<br>grounding: book\_passage |
| **lookup\_table** | prerequisite | **space\_time\_tradeoff** | Saving precomputed values in an array trades memory for time: each value is computed once and then looked up.<br>grounding: book\_passage<br>composition rule (R) of lookup\_table with space\_time\_tradeoff: Storing precomputed values trades memory for time: each value is computed once and then looked up.<br>composition rule (R) of space\_time\_tradeoff with lookup\_table: The lookup table is the stored space: each value is computed once and then read by index. |
| **space\_time\_tradeoff** | has\_level | **space\_time\_tradeoff@L0** | Space-time tradeoff -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (1 way).<br>**[0] everyday\_reading** (E): Folk meaning: saving results is always better, and storing data is free. Rule: precomputation spends memory proportional to the number of saved values to save time, which pays off only when values are reused and the table fits in memory. |
| **space\_time\_tradeoff** | has\_level | **space\_time\_tradeoff@L1** | Space-time tradeoff -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).<br>**[0] names\_the\_element** (N): Identity: a space-time tradeoff invests memory (an array of saved values) to save computation time.<br>**[1] states\_the\_rule** (S): Declarative: by investing in space (saving values) we save time (no recomputation). PrimeSieve trades a boolean array of size N for speed over the two-variable trial-division method. |
| **space\_time\_tradeoff** | has\_level | **space\_time\_tradeoff@L2** | Space-time tradeoff -&gt; L2 (Multistructural): the answer applies the rules of Space-time tradeoff to every part of the code, in order (3 ways).<br>**[0] line\_by\_line\_trace** (LT): Sequencing: a precompute phase (one pass storing N values) runs first, then a use phase in which each query is one array read.<br>**[1] output\_prediction** (OP): Result: the same answers as recomputation, using about N extra memory cells and much less time per query.<br>**[2] one\_step\_execution** (OS): State transition: during precomputation each step stores one value in the table; during use each lookup changes nothing. |
| **space\_time\_tradeoff** | has\_level | **space\_time\_tradeoff@L3** | Space-time tradeoff -&gt; L3 (Relational): the answer relates the parts (2 ways).<br>**[0] relation\_to\_neighbour** (R): The lookup table is the stored space: each value is computed once and then read by index.<br>**[1] purpose\_of\_the\_whole** (P): Plan/role: speed up programs that need the same values many times (harmonic numbers, primes up to N). |
| **space\_time\_tradeoff** | has\_level | **space\_time\_tradeoff@L4** | Space-time tradeoff -&gt; L4 (Extended abstract): the answer reasons beyond the given code (4 ways).<br>**[0] predict\_a\_change** (C): Conservation: results are unchanged by precomputing. Memory grows linearly with N, so for huge N or for values used only once the tradeoff stops paying.<br>**[1] transfer\_to\_a\_new\_program** (X): Applicability: precompute when the values are needed for small N many times and memory is ample. Recompute when N is huge, memory is tight, or each value is used once.<br>**[2] diagnose\_an\_error** (D): rule broken: The table must fit in the memory Java allows. Kind: run-time exception. Trigger class: N too large for the array (OutOfMemoryError, or NegativeArraySizeException if N+1 overflows)<br>**[3] diagnose\_an\_error** (D): rule broken: Precomputation pays only when values are reused. Kind: silent logic error. Trigger class: a huge table is built for a single query, so the program is slower and larger with no benefit |
| **topic1.4.e** | contains | **lookup\_table** | topic topic1.4.e contains lookup\_table |
| **topic1.4.e** | contains | **space\_time\_tradeoff** | topic topic1.4.e contains space\_time\_tradeoff |
