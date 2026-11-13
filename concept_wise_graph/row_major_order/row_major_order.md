# Row-major and column-major order (`row_major_order`)

processing a 2-D array row by row (row-major) or column by column (column-major)

Section 1.4 1.4 Arrays, topic 1.4.g Two-dimensional arrays (ragged, matrix operations). From the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`).

![The knowledge graph around row_major_order](row_major_order.png)

## Concepts associated with row\_major\_order (5)

| Concept | Description | How it is associated |
| --- | --- | --- |
| **matrix\_operations** | matrix addition and multiplication with nested loops | same topic (topic1.4.g) |
| **multidimensional\_array** | arrays with three or more indices | same topic (topic1.4.g) |
| **nested\_loops** | a loop inside a loop | prerequisite of it (it needs this)<br>composition rule (R) with it |
| **ragged\_array** | a 2-D array whose rows have different lengths | same topic (topic1.4.g) |
| **two\_dimensional\_array** | an array of arrays (a[i][j]) | prerequisite of it (it needs this)<br>composition rule (R) with it<br>same topic (topic1.4.g) |

## Every edge in this view and its full label (12)

| From | Edge | To | Full edge label |
| --- | --- | --- | --- |
| **nested\_loops** | prerequisite | **row\_major\_order** | Which loop is outside decides whether the entries are processed row by row or column by column.<br>grounding: book\_passage<br>composition rule (R) of nested\_loops with row\_major\_order: Which loop is outside decides the visiting order: row index outside gives row-major order, column index outside gives column-major order.<br>composition rule (R) of row\_major\_order with nested\_loops: Which loop is outside decides whether entries are processed row by row or column by column; the inner loop finishes for each outer value. |
| **two\_dimensional\_array** | prerequisite | **row\_major\_order** | Row-major order visits a[i][j] row by row (outer loop over i); column-major order puts the column loop outside.<br>grounding: book\_passage<br>composition rule (R) of two\_dimensional\_array with row\_major\_order: Row-major order visits a[i][j] with the outer loop over rows i; column-major puts the loop over j outside.<br>composition rule (R) of row\_major\_order with two\_dimensional\_array: Because a[i] is a row array, row-major order walks along each row array in turn; column-major jumps between row arrays at each step. |
| **row\_major\_order** | has\_level | **row\_major\_order@L0** | Row-major and column-major order -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (1 way).<br>**[0] everyday\_reading** (E): Folk meaning: tables are read left to right, top to bottom, as the only natural order, and 'row' and 'column' are easily swapped. Rule: the loop that is outside decides the order: an outer loop over rows i gives row-major order, an outer loop over columns j gives column-major order. |
| **row\_major\_order** | has\_level | **row\_major\_order@L1** | Row-major and column-major order -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).<br>**[0] names\_the\_element** (N): Identity: row-major order processes a 2-D array row by row; column-major order processes it column by column.<br>**[1] states\_the\_rule** (S): Declarative: for (i &lt; M) { for (j &lt; N) ... a[i][j] } is row-major; for (j &lt; N) { for (i &lt; M) ... a[i][j] } is column-major. Both keep a[i][j] with i as the row. |
| **row\_major\_order** | has\_level | **row\_major\_order@L2** | Row-major and column-major order -&gt; L2 (Multistructural): the answer applies the rules of Row-major and column-major order to every part of the code, in order (3 ways).<br>**[0] line\_by\_line\_trace** (LT): Sequencing (row-major print): i = 0, j runs over 0..N-1 printing a[0][j], newline; i = 1, ... So a[0][0], a[0][1], ..., a[1][0], ... in that order.<br>**[1] output\_prediction** (OP): Result: row-major processing yields per-row results (row averages in column N, rows printed as lines); column-major yields per-column results (column averages in row M).<br>**[2] one\_step\_execution** (OS): State transition: each inner step processes one entry; each outer step completes one whole row (row-major) or column (column-major) and resets the per-row sum. |
| **row\_major\_order** | has\_level | **row\_major\_order@L3** | Row-major and column-major order -&gt; L3 (Relational): the answer relates the parts (3 ways).<br>**[0] relation\_to\_neighbour** (R): Because a[i] is a row array, row-major order walks along each row array in turn; column-major jumps between row arrays at each step.<br>**[1] relation\_to\_neighbour** (R): Which loop is outside decides whether entries are processed row by row or column by column; the inner loop finishes for each outer value.<br>**[2] purpose\_of\_the\_whole** (P): Plan/role: choose the order that matches the result wanted, row-major for per-row results (and for printing), column-major for per-column results. |
| **row\_major\_order** | has\_level | **row\_major\_order@L4** | Row-major and column-major order -&gt; L4 (Extended abstract): the answer reasons beyond the given code (4 ways).<br>**[0] predict\_a\_change** (C): Conservation: swapping the loops of an element-wise operation (copy, add) keeps the result and changes only the visiting order. For printing or per-row sums, swapping changes the output (transposed layout, column results).<br>**[1] transfer\_to\_a\_new\_program** (X): Applicability: use row-major by default in Java (rows are arrays; printing goes line by line). Use column-major when the result is per column, and remember that ragged arrays have no full columns.<br>**[2] diagnose\_an\_error** (D): rule broken: Each loop bound must match the index it controls (i &lt; M rows, j &lt; N columns). Kind: run-time exception. Trigger class: after swapping the loops the bounds are not swapped with them, so in a non-square array a[i][j] gets i up to N-1 (ArrayIndexOutOfBoundsException)<br>**[3] diagnose\_an\_error** (D): rule broken: Per-row or per-column accumulators must be reset for each outer pass. Kind: silent logic error. Trigger class: sum is declared before the outer loop, so each row average includes all earlier rows |
| **topic1.4.g** | contains | **matrix\_operations** | topic topic1.4.g contains matrix\_operations |
| **topic1.4.g** | contains | **multidimensional\_array** | topic topic1.4.g contains multidimensional\_array |
| **topic1.4.g** | contains | **ragged\_array** | topic topic1.4.g contains ragged\_array |
| **topic1.4.g** | contains | **row\_major\_order** | topic topic1.4.g contains row\_major\_order |
| **topic1.4.g** | contains | **two\_dimensional\_array** | topic topic1.4.g contains two\_dimensional\_array |
