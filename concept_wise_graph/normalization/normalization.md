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

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 16 edges around this concept, each explained in the graph's own words.

## What it needs first (2)

A prerequisite edge means the other concept has to be understood before `normalization`.

### `integer_division` comes before `normalization`

*/ on two ints truncates; % is the remainder*

Normalising must divide as doubles, because with two ints counts / total truncates to 0 whenever counts &lt; total.

- **Grounding:** order only
- **How `normalization` combines with `integer_division`:** Type flow decides the result: with a double operand anywhere to the left (.90\*...) the division is floating-point; with two ints it truncates (2/5 == 0).
- **How `integer_division` combines with `normalization`:** Normalizing counts must divide as doubles. With two ints, counts / total truncates to 0 whenever counts &lt; total.

### `transition_matrix` comes before `normalization`

*a 2-D array of move probabilities (rows sum to 1)*

Each row of the transition matrix must be a probability distribution, so counts[i][j] is divided by outDegree[i] (scaled by .90, plus .10/N) to make row i sum to 1.

- **Grounding:** book passage
- **How `normalization` combines with `transition_matrix`:** Normalisation is applied row by row: every entry of row i is divided by the same total outDegree[i], which is what makes the row a distribution the matrix requires.
- **How `transition_matrix` combines with `normalization`:** Dividing counts[i][j] by outDegree[i] (after scaling by .90) and adding .10/N is the normalisation that makes row i sum to 1; the double operand .90 keeps the division from being integer division.

## What it leads to (0)

These concepts need `normalization` first.

No concept has this one as a prerequisite.

## Learned alongside (0)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

No parallel edge touches this concept.

## Misconceptions (2)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### IntegerProbability

- **Wrong rule:** counts[i][j] / degree[i] gives the correct probability because the result is stored in a double.
- **Right rule:** counts[i][j] / outDegree[i] with two int operands is integer division and gives 0 whenever counts &lt; outDegree; SW's Transition avoids it by multiplying by .90 first, and RandomSurfer casts with (double) freq[i] / T.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: Probabilities computed with integer division stay correct. Right rule: counts[i][j]/outDegree[i] with two int operands truncates (0 whenever counts &lt; outDegree); Transition multiplies by .90 first so the division is double, and RandomSurfer casts with (double) freq[i] / T.
- **Shows at level L0 as:** inconsistent trace: Applies LT (left to right: .90\*counts, then / outDegree, then + .10/N) unevenly: e.g. dividing before the double factor on some entries (int division), or adding .10/N once per row instead of to every entry. (here mixing in: "probabilities computed with integer division stay correct")

### RowsNeedNotSumToOne

- **Wrong rule:** A page with no outgoing links can have an all-zero row.
- **Right rule:** Each row is a probability distribution; a page with no links is made equally likely to move to every page.
- **Role of this concept:** context
- **Shows at level L0 as:** misconception: wrong rule: A page with no outgoing links can have an all-zero row. Right rule: Normalising requires a non-zero total; a page with no links is given 1/N in every column so its row still sums to 1.
- **Also an edge from `dangling_pages`:** A page with no outgoing links can have an all-zero row.
- **Also an edge from `transition_matrix`:** A page with no outgoing links can have an all-zero row.

## Errors (0)

An error edge states the rule that gets broken in a program, and the right rule.

The graph has no error edge from this concept.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for normalization: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to normalization agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

normalization -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (4 ways).

- **everyday reading** (folk-meaning rule): In maths, a/b of two whole numbers is a fraction (2/5 = 0.4); in Java, if both operands are int, / discards the fractional part (2/5 is 0), so a probability computed as counts[i][j]/outDegree[i] is 0 or 1.
- **misconception** (wrong rule / right rule; shows `IntegerProbability`): wrong rule: Probabilities computed with integer division stay correct. Right rule: counts[i][j]/outDegree[i] with two int operands truncates (0 whenever counts &lt; outDegree); Transition multiplies by .90 first so the division is double, and RandomSurfer casts with (double) freq[i] / T.
- **inconsistent trace** (uneven-application rule; shows `IntegerProbability`): Applies LT (left to right: .90\*counts, then / outDegree, then + .10/N) unevenly: e.g. dividing before the double factor on some entries (int division), or adding .10/N once per row instead of to every entry. (here mixing in: "probabilities computed with integer division stay correct")
- **misconception** (wrong rule / right rule; shows `RowsNeedNotSumToOne`): wrong rule: A page with no outgoing links can have an all-zero row. Right rule: Normalising requires a non-zero total; a page with no links is given 1/N in every column so its row still sums to 1.

### L1: Unistructural / atom x text surface

L1 for normalization: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

normalization -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

- **names the element** (identity rule): A computation: scaling the non-negative weights of a row by their total so that the row becomes a discrete probability distribution summing to 1.
- **states the rule** (declarative rule): Multiply counts[i][j] by .90/outDegree[i] and add .10/N to each entry; the resulting entries of each row sum to 1.

### L2: Multistructural / block x execution / preoperational

L2 for normalization: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

normalization -&gt; L2 (Multistructural): the answer applies the rules of normalization to every part of the code, in order (3 ways).

- **line by line trace** (operational sequencing rule): In .90\*counts[i][j]/outDegree[i] + .10/N, \* and / evaluate left to right before +: .90\*counts[i][j] first (int promoted to double), then divided by outDegree[i], then .10/N is computed and added.
- **output prediction** (evaluation / result rule): Produces a double in [0, 1]; for tiny.txt page 1 (counts 0 0 2 2 1, outDegree 5) the row is .02 .02 .38 .38 .20, and the row sums to 1 up to floating-point rounding.
- **one step execution** (state-transition rule): One evaluation reads counts[i][j], outDegree[i] and N and yields one double p; nothing in counts or outDegree changes.

### L3: Relational / relations x function (concrete operational begins)

L3 for normalization: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

normalization -&gt; L3 (Relational): the answer relates the parts (3 ways).

- **relation to neighbour** (composition rule (with a neighbour)): Normalisation is applied row by row: every entry of row i is divided by the same total outDegree[i], which is what makes the row a distribution the matrix requires.
- **relation to neighbour** (composition rule (with a neighbour)): Type flow decides the result: with a double operand anywhere to the left (.90\*...) the division is floating-point; with two ints it truncates (2/5 == 0).
- **purpose of the whole** (plan / role rule): Turn raw counts into probabilities (the "divide each count by the total" plan); the same plan turns visit counts freq[i] into rank estimates freq[i]/T.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for normalization: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

normalization -&gt; L4 (Extended abstract): the answer reasons beyond the given code (5 ways).

- **predict a change** (conservation rule; shows `IntegerProbability`): Invariant: weights sum to 1, since .90\*(sum of counts/outDegree) + N\*(.10/N) = .90 + .10. Changing .90 to .80 without changing .10 breaks it; reordering to counts[i][j]/outDegree[i]\*.90 breaks it silently via int division.
- **transfer to a new program** (applicability rule): Use whenever counts or weights must become probabilities (matrix rows, visit frequencies); not needed when the values already form a distribution, and not possible for a zero total (dangling page) without a special case.
- **diagnose an error** (error rule): rule broken: Division of two ints truncates. Kind: silent logic error. Trigger class: counts[i][j]/outDegree[i] or freq[i]/T written with two int operands: every probability with numerator &lt; denominator becomes 0.
- **diagnose an error** (error rule): rule broken: Divisor (total) must be non-zero. Kind: silent logic error. Trigger class: outDegree[i] == 0 in the double expression .90\*counts[i][j]/outDegree[i]: result NaN, no exception.
- **diagnose an error** (error rule): rule broken: Integer division by zero is undefined. Kind: run-time exception. Trigger class: An all-int version counts[i][j]/outDegree[i] with outDegree[i] == 0 throws ArithmeticException.

## Same topic

`normalization` belongs to the topic **Input format and transition matrix** (`topic1.6.a`). The topic also contains: `dangling_pages`, `input_graph`, `teleportation`, `transition_matrix`.

## Rules of the concept (17)

- **folk-meaning rule:** In maths, a/b of two whole numbers is a fraction (2/5 = 0.4); in Java, if both operands are int, / discards the fractional part (2/5 is 0), so a probability computed as counts[i][j]/outDegree[i] is 0 or 1.
- **wrong rule / right rule:** IntegerProbability: wrong: Probabilities computed with integer division stay correct. \| right: counts[i][j]/outDegree[i] with two int operands truncates (0 whenever counts &lt; outDegree); Transition multiplies by .90 first so the division is double, and RandomSurfer casts with (double) freq[i] / T.
- **wrong rule / right rule:** RowsNeedNotSumToOne: wrong: A page with no outgoing links can have an all-zero row. \| right: Normalising requires a non-zero total; a page with no links is given 1/N in every column so its row still sums to 1.
- **uneven-application rule:** Applies LT (left to right: .90\*counts, then / outDegree, then + .10/N) unevenly: e.g. dividing before the double factor on some entries (int division), or adding .10/N once per row instead of to every entry.
- **identity rule:** A computation: scaling the non-negative weights of a row by their total so that the row becomes a discrete probability distribution summing to 1.
- **declarative rule:** Multiply counts[i][j] by .90/outDegree[i] and add .10/N to each entry; the resulting entries of each row sum to 1.
- **operational sequencing rule:** In .90\*counts[i][j]/outDegree[i] + .10/N, \* and / evaluate left to right before +: .90\*counts[i][j] first (int promoted to double), then divided by outDegree[i], then .10/N is computed and added.
- **evaluation / result rule:** Produces a double in [0, 1]; for tiny.txt page 1 (counts 0 0 2 2 1, outDegree 5) the row is .02 .02 .38 .38 .20, and the row sums to 1 up to floating-point rounding.
- **state-transition rule:** One evaluation reads counts[i][j], outDegree[i] and N and yields one double p; nothing in counts or outDegree changes.
- **composition rule (with a neighbour):** with transition\_matrix: Normalisation is applied row by row: every entry of row i is divided by the same total outDegree[i], which is what makes the row a distribution the matrix requires.
- **composition rule (with a neighbour):** with integer\_division: Type flow decides the result: with a double operand anywhere to the left (.90\*...) the division is floating-point; with two ints it truncates (2/5 == 0).
- **plan / role rule:** Turn raw counts into probabilities (the "divide each count by the total" plan); the same plan turns visit counts freq[i] into rank estimates freq[i]/T.
- **conservation rule:** Invariant: weights sum to 1, since .90\*(sum of counts/outDegree) + N\*(.10/N) = .90 + .10. Changing .90 to .80 without changing .10 breaks it; reordering to counts[i][j]/outDegree[i]\*.90 breaks it silently via int division.
- **error rule:** rule broken: Division of two ints truncates. (silent logic error)
- **error rule:** rule broken: Divisor (total) must be non-zero. (silent logic error)
- **error rule:** rule broken: Integer division by zero is undefined. (run-time exception)
- **applicability rule:** Use whenever counts or weights must become probabilities (matrix rows, visit frequencies); not needed when the values already form a distribution, and not possible for a zero total (dangling page) without a special case.

## The whole prerequisite chain

- **Everything it builds on (14):** `arithmetic_operators`, `array_creation`, `array_declaration`, `array_initializer`, `data_structure`, `data_type`, `indexing`, `input_graph`, `integer_division`, `standard_input`, `stream_model`, `teleportation`, `transition_matrix`, `two_dimensional_array`
- **Everything that builds on it (0):** nothing
