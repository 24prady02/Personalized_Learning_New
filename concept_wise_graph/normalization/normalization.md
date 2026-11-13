# normalization (`normalization`)

scaling a row so its probabilities sum to 1

Section 1.6 Case Study: Random Web Surfer, topic 1.6.a Input format and transition matrix.

![The knowledge graph around normalization](normalization.png)

## At a glance

- **Needs first:** `integer_division`, `transition_matrix`
- **Leads to:** nothing
- **Learned alongside:** nothing
- **Misconceptions:** `IntegerProbability`, `RowsNeedNotSumToOne`
- **Errors:** none
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 16 edges around this concept. The edge logic, the wrong and right rules and the exact rules of the ways are copied word for word from the graph.

## To work on (1)

- no aliases: a student's words cannot name this concept

## What it needs first (2)

A prerequisite edge means the other concept has to be understood before `normalization`.

### `integer_division` comes before `normalization`

*/ on two ints truncates; % is the remainder*

- **Edge:** `pre:integer_division->normalization`
- **Exact edge logic:** Normalising must divide as doubles, because with two ints counts / total truncates to 0 whenever counts &lt; total.
- **Grounding:** order\_only
- **Composition rule (R) of `normalization` with `integer_division`:** Type flow decides the result: with a double operand anywhere to the left (.90\*...) the division is floating-point; with two ints it truncates (2/5 == 0).
- **Composition rule (R) of `integer_division` with `normalization`:** Normalizing counts must divide as doubles. With two ints, counts / total truncates to 0 whenever counts &lt; total.

### `transition_matrix` comes before `normalization`

*a 2-D array of move probabilities (rows sum to 1)*

- **Edge:** `pre:transition_matrix->normalization`
- **Exact edge logic:** Each row of the transition matrix must be a probability distribution, so counts[i][j] is divided by outDegree[i] (scaled by .90, plus .10/N) to make row i sum to 1.
- **Grounding:** book\_passage
- **Composition rule (R) of `normalization` with `transition_matrix`:** Normalisation is applied row by row: every entry of row i is divided by the same total outDegree[i], which is what makes the row a distribution the matrix requires.
- **Composition rule (R) of `transition_matrix` with `normalization`:** Dividing counts[i][j] by outDegree[i] (after scaling by .90) and adding .10/N is the normalisation that makes row i sum to 1; the double operand .90 keeps the division from being integer division.

## What it leads to (0)

These concepts need `normalization` first.

No concept has this one as a prerequisite.

## Learned alongside (0)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

No parallel edge touches this concept.

## Misconceptions (2)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### IntegerProbability

- **Edge:** `normalization` &rarr; `IntegerProbability` (misconception)
- **Exact edge logic (the wrong rule):** counts[i][j] / degree[i] gives the correct probability because the result is stored in a double.
- **Twin logic (the right rule):** counts[i][j] / outDegree[i] with two int operands is integer division and gives 0 whenever counts &lt; outDegree; SW's Transition avoids it by multiplying by .90 first, and RandomSurfer casts with (double) freq[i] / T.
- **Wrong belief (on the node):** probabilities computed with integer division stay correct
- **Correct rule (on the node):** counts[i][j] / outDegree[i] with two int operands is integer division and gives 0 whenever counts &lt; outDegree; SW's Transition avoids it by multiplying by .90 first, and RandomSurfer casts with (double) freq[i] / T.
- **Provenance:** textbook
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [1] misconception, exact rule:** wrong rule: Probabilities computed with integer division stay correct. Right rule: counts[i][j]/outDegree[i] with two int operands truncates (0 whenever counts &lt; outDegree); Transition multiplies by .90 first so the division is double, and RandomSurfer casts with (double) freq[i] / T.
- **L0 way [2] inconsistent\_trace, exact rule:** Applies LT (left to right: .90\*counts, then / outDegree, then + .10/N) unevenly: e.g. dividing before the double factor on some entries (int division), or adding .10/N once per row instead of to every entry. (here mixing in: "probabilities computed with integer division stay correct")

### RowsNeedNotSumToOne

- **Edge:** `normalization` &rarr; `RowsNeedNotSumToOne` (misconception)
- **Exact edge logic (the wrong rule):** A page with no outgoing links can have an all-zero row.
- **Twin logic (the right rule):** Each row is a probability distribution; a page with no links is made equally likely to move to every page.
- **Wrong belief (on the node):** A page with no outgoing links can have an all-zero row.
- **Correct rule (on the node):** Each row is a probability distribution; a page with no links is made equally likely to move to every page.
- **Provenance:** textbook
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [3] misconception, exact rule:** wrong rule: A page with no outgoing links can have an all-zero row. Right rule: Normalising requires a non-zero total; a page with no links is given 1/N in every column so its row still sums to 1.
- **Edge `dangling_pages` &rarr; `RowsNeedNotSumToOne`, exact edge logic:** A page with no outgoing links can have an all-zero row. **Twin logic:** Each row is a probability distribution; a page with no links is made equally likely to move to every page. (role: primary)
- **Edge `transition_matrix` &rarr; `RowsNeedNotSumToOne`, exact edge logic:** A page with no outgoing links can have an all-zero row. **Twin logic:** Each row is a probability distribution; a page with no links is made equally likely to move to every page. (role: context)

## Errors (0)

An error edge states the rule that gets broken in a program, and the right rule.

The graph has no error edge from this concept.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for normalization: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to normalization agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

- **Edge:** `normalization` &rarr; `normalization@L0` (has_level)
- **Exact edge logic:** normalization -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (4 ways).

Ways (4), each with its exact rule:

- **[0] everyday\_reading** (rule type E, folk-meaning rule): In maths, a/b of two whole numbers is a fraction (2/5 = 0.4); in Java, if both operands are int, / discards the fractional part (2/5 is 0), so a probability computed as counts[i][j]/outDegree[i] is 0 or 1.
- **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `IntegerProbability`: wrong rule: Probabilities computed with integer division stay correct. Right rule: counts[i][j]/outDegree[i] with two int operands truncates (0 whenever counts &lt; outDegree); Transition multiplies by .90 first so the division is double, and RandomSurfer casts with (double) freq[i] / T.
- **[2] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `IntegerProbability`: Applies LT (left to right: .90\*counts, then / outDegree, then + .10/N) unevenly: e.g. dividing before the double factor on some entries (int division), or adding .10/N once per row instead of to every entry. (here mixing in: "probabilities computed with integer division stay correct")
- **[3] misconception** (rule type M, wrong rule / right rule) &rarr; `RowsNeedNotSumToOne`: wrong rule: A page with no outgoing links can have an all-zero row. Right rule: Normalising requires a non-zero total; a page with no links is given 1/N in every column so its row still sums to 1.

### L1: Unistructural / atom x text surface

L1 for normalization: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

- **Edge:** `normalization` &rarr; `normalization@L1` (has_level)
- **Exact edge logic:** normalization -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

Ways (2), each with its exact rule:

- **[0] names\_the\_element** (rule type N, identity rule): A computation: scaling the non-negative weights of a row by their total so that the row becomes a discrete probability distribution summing to 1.
- **[1] states\_the\_rule** (rule type S, declarative rule): Multiply counts[i][j] by .90/outDegree[i] and add .10/N to each entry; the resulting entries of each row sum to 1.

### L2: Multistructural / block x execution / preoperational

L2 for normalization: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

- **Edge:** `normalization` &rarr; `normalization@L2` (has_level)
- **Exact edge logic:** normalization -&gt; L2 (Multistructural): the answer applies the rules of normalization to every part of the code, in order (3 ways).

Ways (3), each with its exact rule:

- **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): In .90\*counts[i][j]/outDegree[i] + .10/N, \* and / evaluate left to right before +: .90\*counts[i][j] first (int promoted to double), then divided by outDegree[i], then .10/N is computed and added.
- **[1] output\_prediction** (rule type OP, evaluation / result rule): Produces a double in [0, 1]; for tiny.txt page 1 (counts 0 0 2 2 1, outDegree 5) the row is .02 .02 .38 .38 .20, and the row sums to 1 up to floating-point rounding.
- **[2] one\_step\_execution** (rule type OS, state-transition rule): One evaluation reads counts[i][j], outDegree[i] and N and yields one double p; nothing in counts or outDegree changes.

### L3: Relational / relations x function (concrete operational begins)

L3 for normalization: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

- **Edge:** `normalization` &rarr; `normalization@L3` (has_level)
- **Exact edge logic:** normalization -&gt; L3 (Relational): the answer relates the parts (3 ways).

Ways (3), each with its exact rule:

- **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Normalisation is applied row by row: every entry of row i is divided by the same total outDegree[i], which is what makes the row a distribution the matrix requires.
- **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Type flow decides the result: with a double operand anywhere to the left (.90\*...) the division is floating-point; with two ints it truncates (2/5 == 0).
- **[2] purpose\_of\_the\_whole** (rule type P, plan / role rule): Turn raw counts into probabilities (the "divide each count by the total" plan); the same plan turns visit counts freq[i] into rank estimates freq[i]/T.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for normalization: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

- **Edge:** `normalization` &rarr; `normalization@L4` (has_level)
- **Exact edge logic:** normalization -&gt; L4 (Extended abstract): the answer reasons beyond the given code (5 ways).

Ways (5), each with its exact rule:

- **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `IntegerProbability`: Invariant: weights sum to 1, since .90\*(sum of counts/outDegree) + N\*(.10/N) = .90 + .10. Changing .90 to .80 without changing .10 breaks it; reordering to counts[i][j]/outDegree[i]\*.90 breaks it silently via int division.
- **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Use whenever counts or weights must become probabilities (matrix rows, visit frequencies); not needed when the values already form a distribution, and not possible for a zero total (dangling page) without a special case.
- **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: Division of two ints truncates. Kind: silent logic error. Trigger class: counts[i][j]/outDegree[i] or freq[i]/T written with two int operands: every probability with numerator &lt; denominator becomes 0.
- **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: Divisor (total) must be non-zero. Kind: silent logic error. Trigger class: outDegree[i] == 0 in the double expression .90\*counts[i][j]/outDegree[i]: result NaN, no exception.
- **[4] diagnose\_an\_error** (rule type D, error rule): rule broken: Integer division by zero is undefined. Kind: run-time exception. Trigger class: An all-int version counts[i][j]/outDegree[i] with outDegree[i] == 0 throws ArithmeticException.

## Same topic

`normalization` belongs to the topic **Input format and transition matrix** (`topic1.6.a`). The topic also contains: `dangling_pages`, `input_graph`, `teleportation`, `transition_matrix`.

## Rules of the concept (17)

- **Book** (SW-1e, p. 164 (pdf 174)): "The transition matrix is significant because each row represents a discrete probability distribution"
- **Book** (SW-1.6, ): "make that page equally likely to transition to every other page"
- **E** (folk-meaning rule): In maths, a/b of two whole numbers is a fraction (2/5 = 0.4); in Java, if both operands are int, / discards the fractional part (2/5 is 0), so a probability computed as counts[i][j]/outDegree[i] is 0 or 1.
- **M** (wrong rule / right rule): IntegerProbability: wrong: Probabilities computed with integer division stay correct. \| right: counts[i][j]/outDegree[i] with two int operands truncates (0 whenever counts &lt; outDegree); Transition multiplies by .90 first so the division is double, and RandomSurfer casts with (double) freq[i] / T.
- **M** (wrong rule / right rule): RowsNeedNotSumToOne: wrong: A page with no outgoing links can have an all-zero row. \| right: Normalising requires a non-zero total; a page with no links is given 1/N in every column so its row still sums to 1.
- **T** (uneven-application rule): Applies LT (left to right: .90\*counts, then / outDegree, then + .10/N) unevenly: e.g. dividing before the double factor on some entries (int division), or adding .10/N once per row instead of to every entry.
- **N** (identity rule): A computation: scaling the non-negative weights of a row by their total so that the row becomes a discrete probability distribution summing to 1.
- **S** (declarative rule): Multiply counts[i][j] by .90/outDegree[i] and add .10/N to each entry; the resulting entries of each row sum to 1.
- **LT** (operational sequencing rule): In .90\*counts[i][j]/outDegree[i] + .10/N, \* and / evaluate left to right before +: .90\*counts[i][j] first (int promoted to double), then divided by outDegree[i], then .10/N is computed and added.
- **OP** (evaluation / result rule): Produces a double in [0, 1]; for tiny.txt page 1 (counts 0 0 2 2 1, outDegree 5) the row is .02 .02 .38 .38 .20, and the row sums to 1 up to floating-point rounding.
- **OS** (state-transition rule): One evaluation reads counts[i][j], outDegree[i] and N and yields one double p; nothing in counts or outDegree changes.
- **R** (composition rule (with a neighbour)): with transition\_matrix: Normalisation is applied row by row: every entry of row i is divided by the same total outDegree[i], which is what makes the row a distribution the matrix requires.
- **R** (composition rule (with a neighbour)): with integer\_division: Type flow decides the result: with a double operand anywhere to the left (.90\*...) the division is floating-point; with two ints it truncates (2/5 == 0).
- **P** (plan / role rule): Turn raw counts into probabilities (the "divide each count by the total" plan); the same plan turns visit counts freq[i] into rank estimates freq[i]/T.
- **C** (conservation rule): Invariant: weights sum to 1, since .90\*(sum of counts/outDegree) + N\*(.10/N) = .90 + .10. Changing .90 to .80 without changing .10 breaks it; reordering to counts[i][j]/outDegree[i]\*.90 breaks it silently via int division.
- **D** (error rule): rule broken: Division of two ints truncates. (silent logic error)
- **D** (error rule): rule broken: Divisor (total) must be non-zero. (silent logic error)
- **D** (error rule): rule broken: Integer division by zero is undefined. (run-time exception)
- **X** (applicability rule): Use whenever counts or weights must become probabilities (matrix rows, visit frequencies); not needed when the values already form a distribution, and not possible for a zero total (dangling page) without a special case.

## How it is found in code and answers (reader block)

- **Aliases:** none
- **Code patterns:** `\w+\s*\[[^\]]+\](?:\s*\[[^\]]+\])?\s*=\s*(?:\(\s*double\s*\)\s*)?\w+\s*\[[^\]]+\](?:\s*\[[^\]]+\])?\s*/\s*[A-Za-z_]\w*(?:\s*\[[^\]]+\])?\s*;`
- **Operator symbols:** none
- **Java types:** none

## The whole prerequisite chain

- **Everything it builds on (14):** `arithmetic_operators`, `array_creation`, `array_declaration`, `array_initializer`, `data_structure`, `data_type`, `indexing`, `input_graph`, `integer_division`, `standard_input`, `stream_model`, `teleportation`, `transition_matrix`, `two_dimensional_array`
- **Everything that builds on it (0):** nothing

## Every edge in this view and its exact edge logic (16)

All the edges drawn in the picture, in the order: prerequisite, parallel, misconception, error, has_level, contains.

**1. `integer_division` &rarr; `normalization`** (prerequisite)

- **Exact edge logic:** Normalising must divide as doubles, because with two ints counts / total truncates to 0 whenever counts &lt; total.
- **Grounding:** order\_only
- **Composition rule (R) of `integer_division` with `normalization`:** Normalizing counts must divide as doubles. With two ints, counts / total truncates to 0 whenever counts &lt; total.
- **Composition rule (R) of `normalization` with `integer_division`:** Type flow decides the result: with a double operand anywhere to the left (.90\*...) the division is floating-point; with two ints it truncates (2/5 == 0).

**2. `transition_matrix` &rarr; `normalization`** (prerequisite)

- **Exact edge logic:** Each row of the transition matrix must be a probability distribution, so counts[i][j] is divided by outDegree[i] (scaled by .90, plus .10/N) to make row i sum to 1.
- **Grounding:** book\_passage
- **Composition rule (R) of `transition_matrix` with `normalization`:** Dividing counts[i][j] by outDegree[i] (after scaling by .90) and adding .10/N is the normalisation that makes row i sum to 1; the double operand .90 keeps the division from being integer division.
- **Composition rule (R) of `normalization` with `transition_matrix`:** Normalisation is applied row by row: every entry of row i is divided by the same total outDegree[i], which is what makes the row a distribution the matrix requires.

**3. `normalization` &rarr; `IntegerProbability`** (misconception)

- **Exact edge logic (the wrong rule):** counts[i][j] / degree[i] gives the correct probability because the result is stored in a double.
- **Twin logic (the right rule):** counts[i][j] / outDegree[i] with two int operands is integer division and gives 0 whenever counts &lt; outDegree; SW's Transition avoids it by multiplying by .90 first, and RandomSurfer casts with (double) freq[i] / T.
- **Role:** primary

**4. `normalization` &rarr; `RowsNeedNotSumToOne`** (misconception)

- **Exact edge logic (the wrong rule):** A page with no outgoing links can have an all-zero row.
- **Twin logic (the right rule):** Each row is a probability distribution; a page with no links is made equally likely to move to every page.
- **Role:** context

**5. `dangling_pages` &rarr; `RowsNeedNotSumToOne`** (misconception)

- **Exact edge logic (the wrong rule):** A page with no outgoing links can have an all-zero row.
- **Twin logic (the right rule):** Each row is a probability distribution; a page with no links is made equally likely to move to every page.
- **Role:** primary

**6. `transition_matrix` &rarr; `RowsNeedNotSumToOne`** (misconception)

- **Exact edge logic (the wrong rule):** A page with no outgoing links can have an all-zero row.
- **Twin logic (the right rule):** Each row is a probability distribution; a page with no links is made equally likely to move to every page.
- **Role:** context

**7. `normalization` &rarr; `normalization@L0`** (has_level)

- **Exact edge logic:** normalization -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (4 ways).
  - **[0] everyday\_reading** (rule type E, folk-meaning rule): In maths, a/b of two whole numbers is a fraction (2/5 = 0.4); in Java, if both operands are int, / discards the fractional part (2/5 is 0), so a probability computed as counts[i][j]/outDegree[i] is 0 or 1.
  - **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `IntegerProbability`: wrong rule: Probabilities computed with integer division stay correct. Right rule: counts[i][j]/outDegree[i] with two int operands truncates (0 whenever counts &lt; outDegree); Transition multiplies by .90 first so the division is double, and RandomSurfer casts with (double) freq[i] / T.
  - **[2] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `IntegerProbability`: Applies LT (left to right: .90\*counts, then / outDegree, then + .10/N) unevenly: e.g. dividing before the double factor on some entries (int division), or adding .10/N once per row instead of to every entry. (here mixing in: "probabilities computed with integer division stay correct")
  - **[3] misconception** (rule type M, wrong rule / right rule) &rarr; `RowsNeedNotSumToOne`: wrong rule: A page with no outgoing links can have an all-zero row. Right rule: Normalising requires a non-zero total; a page with no links is given 1/N in every column so its row still sums to 1.

**8. `normalization` &rarr; `normalization@L1`** (has_level)

- **Exact edge logic:** normalization -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).
  - **[0] names\_the\_element** (rule type N, identity rule): A computation: scaling the non-negative weights of a row by their total so that the row becomes a discrete probability distribution summing to 1.
  - **[1] states\_the\_rule** (rule type S, declarative rule): Multiply counts[i][j] by .90/outDegree[i] and add .10/N to each entry; the resulting entries of each row sum to 1.

**9. `normalization` &rarr; `normalization@L2`** (has_level)

- **Exact edge logic:** normalization -&gt; L2 (Multistructural): the answer applies the rules of normalization to every part of the code, in order (3 ways).
  - **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): In .90\*counts[i][j]/outDegree[i] + .10/N, \* and / evaluate left to right before +: .90\*counts[i][j] first (int promoted to double), then divided by outDegree[i], then .10/N is computed and added.
  - **[1] output\_prediction** (rule type OP, evaluation / result rule): Produces a double in [0, 1]; for tiny.txt page 1 (counts 0 0 2 2 1, outDegree 5) the row is .02 .02 .38 .38 .20, and the row sums to 1 up to floating-point rounding.
  - **[2] one\_step\_execution** (rule type OS, state-transition rule): One evaluation reads counts[i][j], outDegree[i] and N and yields one double p; nothing in counts or outDegree changes.

**10. `normalization` &rarr; `normalization@L3`** (has_level)

- **Exact edge logic:** normalization -&gt; L3 (Relational): the answer relates the parts (3 ways).
  - **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Normalisation is applied row by row: every entry of row i is divided by the same total outDegree[i], which is what makes the row a distribution the matrix requires.
  - **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Type flow decides the result: with a double operand anywhere to the left (.90\*...) the division is floating-point; with two ints it truncates (2/5 == 0).
  - **[2] purpose\_of\_the\_whole** (rule type P, plan / role rule): Turn raw counts into probabilities (the "divide each count by the total" plan); the same plan turns visit counts freq[i] into rank estimates freq[i]/T.

**11. `normalization` &rarr; `normalization@L4`** (has_level)

- **Exact edge logic:** normalization -&gt; L4 (Extended abstract): the answer reasons beyond the given code (5 ways).
  - **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `IntegerProbability`: Invariant: weights sum to 1, since .90\*(sum of counts/outDegree) + N\*(.10/N) = .90 + .10. Changing .90 to .80 without changing .10 breaks it; reordering to counts[i][j]/outDegree[i]\*.90 breaks it silently via int division.
  - **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Use whenever counts or weights must become probabilities (matrix rows, visit frequencies); not needed when the values already form a distribution, and not possible for a zero total (dangling page) without a special case.
  - **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: Division of two ints truncates. Kind: silent logic error. Trigger class: counts[i][j]/outDegree[i] or freq[i]/T written with two int operands: every probability with numerator &lt; denominator becomes 0.
  - **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: Divisor (total) must be non-zero. Kind: silent logic error. Trigger class: outDegree[i] == 0 in the double expression .90\*counts[i][j]/outDegree[i]: result NaN, no exception.
  - **[4] diagnose\_an\_error** (rule type D, error rule): rule broken: Integer division by zero is undefined. Kind: run-time exception. Trigger class: An all-int version counts[i][j]/outDegree[i] with outDegree[i] == 0 throws ArithmeticException.

**12. `topic1.6.a` &rarr; `normalization`** (contains)

- topic `topic1.6.a` contains `normalization`

**13. `topic1.6.a` &rarr; `dangling_pages`** (contains)

- topic `topic1.6.a` contains `dangling_pages`

**14. `topic1.6.a` &rarr; `input_graph`** (contains)

- topic `topic1.6.a` contains `input_graph`

**15. `topic1.6.a` &rarr; `teleportation`** (contains)

- topic `topic1.6.a` contains `teleportation`

**16. `topic1.6.a` &rarr; `transition_matrix`** (contains)

- topic `topic1.6.a` contains `transition_matrix`
