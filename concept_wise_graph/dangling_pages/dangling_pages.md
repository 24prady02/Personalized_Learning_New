# dangling_pages (`dangling_pages`)

pages with no outgoing links

Section 1.6 Case Study: Random Web Surfer, topic 1.6.a Input format and transition matrix. From the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`).

![The knowledge graph around dangling_pages](dangling_pages.png)

## Concepts associated with dangling\_pages (4)

| Concept | Description | How it is associated |
| --- | --- | --- |
| **input\_graph** | read the page links from input | same topic (topic1.6.a) |
| **normalization** | scaling a row so its probabilities sum to 1 | shares misconception RowsNeedNotSumToOne<br>same topic (topic1.6.a) |
| **teleportation** | the 90-10 rule: follow a link or jump to a random page | same topic (topic1.6.a) |
| **transition\_matrix** | a 2-D array of move probabilities (rows sum to 1) | prerequisite of it (it needs this)<br>composition rule (R) with it<br>shares misconception RowsNeedNotSumToOne<br>same topic (topic1.6.a) |

## Every edge in this view and its full label (14)

| From | Edge | To | Full edge label |
| --- | --- | --- | --- |
| **transition\_matrix** | prerequisite | **dangling\_pages** | Transition assumes that every page has an outgoing link; Exercise 1.6.3 handles a page with no outgoing links by filling its row of the transition matrix with 1/N.<br>grounding: book\_passage<br>composition rule (R) of transition\_matrix with dangling\_pages: Transition's formula is valid only if every outDegree[i] &gt; 0; a page with no outlinks must have its row filled with 1/N.<br>composition rule (R) of dangling\_pages with transition\_matrix: A dangling page is the case where the matrix formula breaks (division by outDegree 0); the 1/N row replaces it so the matrix stays stochastic. |
| **dangling\_pages** | misconception | **RowsNeedNotSumToOne** | **wrong rule:** A page with no outgoing links can have an all-zero row.<br>**right rule:** Each row is a probability distribution; a page with no links is made equally likely to move to every page.<br>role: primary |
| **normalization** | misconception | **RowsNeedNotSumToOne** | **wrong rule:** A page with no outgoing links can have an all-zero row.<br>**right rule:** Each row is a probability distribution; a page with no links is made equally likely to move to every page.<br>role: context |
| **transition\_matrix** | misconception | **RowsNeedNotSumToOne** | **wrong rule:** A page with no outgoing links can have an all-zero row.<br>**right rule:** Each row is a probability distribution; a page with no links is made equally likely to move to every page.<br>role: context |
| **dangling\_pages** | has\_level | **dangling\_pages@L0** | dangling pages -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (3 ways).<br>**[0] everyday\_reading** (E): Everyday reading of a "dead-end" page is that the surfer just stops or stays there; in the model the surfer always goes somewhere, so a page with no outlinks must still have a full probability row (1/N to every page).<br>**[1] misconception** (M) &rarr; RowsNeedNotSumToOne: wrong rule: A page with no outgoing links can have an all-zero row. Right rule: Every row must sum to 1; fill the row of a page with no outgoing links with 1/N (equally likely to go to every page).<br>**[2] inconsistent\_trace** (T) &rarr; RowsNeedNotSumToOne: Applies LT (test outDegree[i] == 0 before dividing; if so use 1.0/N for the whole row) unevenly: e.g. tests only on the first column, or still adds the .10/N leap term to the 1/N entries so the row sums to more than 1. (here mixing in: "A page with no outgoing links can have an all-zero row") |
| **dangling\_pages** | has\_level | **dangling\_pages@L1** | dangling pages -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).<br>**[0] names\_the\_element** (N): A page with no outgoing links (outDegree 0), also called a dangling page or sink; spider traps are sets of such pages.<br>**[1] states\_the\_rule** (S): Transition assumes there are none; to handle them, fill the row of every page with no outgoing links with 1/N, which keeps the matrix stochastic. |
| **dangling\_pages** | has\_level | **dangling\_pages@L2** | dangling pages -&gt; L2 (Multistructural): the answer applies the rules of dangling pages to every part of the code, in order (3 ways).<br>**[0] line\_by\_line\_trace** (LT): For row i: first test outDegree[i] == 0; if true every p[i][j] = 1.0/N; otherwise use .90\*counts[i][j]/outDegree[i] + .10/N. The test must come before the division.<br>**[1] output\_prediction** (OP): A dangling page's row is N equal entries 1/N (for N = 5, 0.20000 each), summing to 1.<br>**[2] one\_step\_execution** (OS): Handling one dangling entry sets p[i][j] to the double 1.0/N; counts and outDegree are unchanged. |
| **dangling\_pages** | has\_level | **dangling\_pages@L3** | dangling pages -&gt; L3 (Relational): the answer relates the parts (2 ways).<br>**[0] relation\_to\_neighbour** (R): A dangling page is the case where the matrix formula breaks (division by outDegree 0); the 1/N row replaces it so the matrix stays stochastic.<br>**[1] purpose\_of\_the\_whole** (P): A guard / special-case plan: detect the zero-total case and substitute a uniform distribution so later code (random move, power method) can assume every row sums to 1. |
| **dangling\_pages** | has\_level | **dangling\_pages@L4** | dangling pages -&gt; L4 (Extended abstract): the answer reasons beyond the given code (4 ways).<br>**[0] predict\_a\_change** (C) &rarr; RowsNeedNotSumToOne: Filling with 1/N keeps the row-sum invariant; writing 1/N with int operands (0) or leaving the row as computed (NaN) breaks it, and RandomSurfer then fails.<br>**[1] transfer\_to\_a\_new\_program** (X): Needed whenever the input may contain pages with no outlinks (as the real web does, e.g. spider traps); unnecessary when every page has at least one outlink, as Transition assumes.<br>**[2] diagnose\_an\_error** (D): rule broken: Transition assumes no page lacks outlinks. Kind: silent logic error. Trigger class: Input with a page that never appears as i: its row is NaN (0.0/0), and RandomSurfer's test r &lt; sum is always false on that row, so the surfer never leaves.<br>**[3] diagnose\_an\_error** (D): rule broken: 1/N must be computed in floating point. Kind: silent logic error. Trigger class: Fill value written as 1/N with int N &gt; 1: every entry is 0 and the row sums to 0. |
| **topic1.6.a** | contains | **dangling\_pages** | topic topic1.6.a contains dangling\_pages |
| **topic1.6.a** | contains | **input\_graph** | topic topic1.6.a contains input\_graph |
| **topic1.6.a** | contains | **normalization** | topic topic1.6.a contains normalization |
| **topic1.6.a** | contains | **teleportation** | topic topic1.6.a contains teleportation |
| **topic1.6.a** | contains | **transition\_matrix** | topic topic1.6.a contains transition\_matrix |
