# fencepost_loop (`fencepost_loop`)

n items need n - 1 separators: one item handled outside the loop

Section 1.3 Conditionals and Loops, topic 1.3.f Applications (finite sums, Newton, conversion, gambler's ruin, factoring).

![The knowledge graph around fencepost_loop](fencepost_loop.png)

## At a glance

- **Needs first:** `for_loop`
- **Leads to:** nothing
- **Learned alongside:** `off_by_one_error`
- **Misconceptions:** none
- **Errors:** `FencepostExtraSeparator`
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 19 edges around this concept, each explained in the graph's own words.

## What it needs first (1)

A prerequisite edge means the other concept has to be understood before `fencepost_loop`.

### `for_loop` comes before `fencepost_loop`

*a while with init/condition/update packaged together*

A fencepost loop is a for loop with one item handled outside it.

- **Grounding:** questionable
- **How `fencepost_loop` combines with `for_loop`:** The for loop's bounds must match the handled-outside item: if a[0] is printed before the loop, the loop must start at \`i = 1\`. Starting at 0 duplicates the first item, and \`i &lt;= n\` runs past the end.
- **How `for_loop` combines with `fencepost_loop`:** A fencepost loop is a for loop that handles one item (the first or last) outside the loop so that separators come out n-1 times for n items.

## What it leads to (0)

These concepts need `fencepost_loop` first.

No concept has this one as a prerequisite.

## Learned alongside (1)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

### `fencepost_loop` alongside `off_by_one_error`

*a loop or index that runs one time too many or too few (&lt; vs &lt;=, 0..n vs 1..n, length vs length-1)*

An off-by-one error is a loop that runs once too many or too few; a fencepost loop is the correct plan for the case that needs one action more than the other.

- **Grounding:** book passage
- **How `off_by_one_error` combines with `fencepost_loop`:** When one action must happen once more (or less) than the other, the fencepost plan handles the extra case explicitly instead of risking an off-by-one.

## Misconceptions (0)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

The graph has no misconception edge from this concept.

## Errors (1)

An error edge states the rule that gets broken in a program, and the right rule.

### FencepostExtraSeparator

- **Wrong rule:** Prints item and separator together in the loop, leaving an extra separator at the end.
- **Right rule:** Handle one item outside the loop so n items get n - 1 separators.
- **Role of this concept:** primary
- **Also an edge from `off_by_one_error`:** Prints item and separator together in the loop, leaving an extra separator at the end.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for fencepost loop: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to fencepost loop agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

fencepost loop -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (1 way).

- **everyday reading** (folk-meaning rule): Folk meaning: in everyday counting each item 'comes with' its separator (each fence section with a post), so a novice prints item and separator together n times. For n items you need n − 1 separators (or n + 1 posts for n sections), so one item has to be handled outside the loop.

### L1: Unistructural / atom x text surface

L1 for fencepost loop: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

fencepost loop -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

- **names the element** (identity rule): Loop idiom: a loop that processes n items with n − 1 separators by handling one item outside the loop ('loop and a half').
- **states the rule** (declarative rule): Print the first item before the loop, then loop over the rest printing separator then item: \`System.out.print(a[0]); for (int i = 1; i &lt; n; i++) System.out.print(", " + a[i]);\` (or print item then separator for all but the last).

### L2: Multistructural / block x execution / preoperational

L2 for fencepost loop: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

fencepost loop -&gt; L2 (Multistructural): the answer applies the rules of fencepost loop to every part of the code, in order (3 ways).

- **line by line trace** (operational sequencing rule): Order: the first item is printed once before the loop test. Each pass then tests \`i &lt; n\`, prints the separator, prints a[i] and increments i, so a separator always comes before an item, never after the last one.
- **output prediction** (evaluation / result rule): For a = {1, 2, 3} the output is \`1, 2, 3\`: 3 items and exactly 2 separators, with no leading or trailing separator.
- **one step execution** (state-transition rule): One loop pass prints exactly one separator and one item and increments i by 1. The pre-loop statement prints one item and no separator.

### L3: Relational / relations x function (concrete operational begins)

L3 for fencepost loop: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

fencepost loop -&gt; L3 (Relational): the answer relates the parts (3 ways).

- **relation to neighbour** (composition rule (with a neighbour)): The for loop's bounds must match the handled-outside item: if a[0] is printed before the loop, the loop must start at \`i = 1\`. Starting at 0 duplicates the first item, and \`i &lt;= n\` runs past the end.
- **relation to neighbour** (composition rule (with a neighbour)): An off-by-one error is a loop that runs once too many or too few; a fencepost loop is the correct plan for the case that needs one action more than the other.
- **purpose of the whole** (plan / role rule): Plan: fencepost / loop-and-a-half plan. It produces separated lists (\`1, 2, 3\`), joined strings, and drawings of n posts with n − 1 rails.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for fencepost loop: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

fencepost loop -&gt; L4 (Extended abstract): the answer reasons beyond the given code (4 ways).

- **predict a change** (conservation rule): Invariant: after k passes, the output holds k + 1 items and k separators. Moving the separator after the item inside the loop breaks this and leaves a trailing separator. Swapping the outside item from first to last needs the loop to cover 0 .. n−2 instead.
- **diagnose an error** (error rule): rule broken: n items need n − 1 separators; one item must be handled outside the loop. Kind: silent logic error. Trigger class: Printing \`a[i] + ", "\` for every i: the output ends with an extra separator (\`1, 2, 3, \`). Any n ≥ 1 triggers it.
- **transfer to a new program** (applicability rule): Use a fencepost loop whenever items are joined by separators or bounded by posts (CSV lines, comma lists, drawings). It is not needed when every item gets the same surrounding text; there, a plain loop is right.
- **diagnose an error** (error rule): rule broken: Array indices run from 0 to length − 1; the item handled outside the loop must exist. Kind: run-time exception. Trigger class: An empty array (n = 0): \`print(a[0])\` before the loop throws ArrayIndexOutOfBoundsException.

## Same topic

`fencepost_loop` belongs to the topic **Applications (finite sums, Newton, conversion, gambler's ruin, factoring)** (`topic1.3.f`). The topic also contains: `accumulator_pattern`, `convergence_test`, `counter_pattern`, `debugging`, `flag_search_loop`, `loop_performance`, `monte_carlo_simulation`, `number_conversion`, `testing`.

## Rules of the concept (13)

- **folk-meaning rule:** Folk meaning: in everyday counting each item 'comes with' its separator (each fence section with a post), so a novice prints item and separator together n times. For n items you need n − 1 separators (or n + 1 posts for n sections), so one item has to be handled outside the loop.
- **uneven-application rule:** Applies the loop's LT rule unevenly: on a trace, the first item is printed both before the loop and on the first pass (loop starting at 0 instead of 1), or the separator is printed before the test on the last pass. The result is a duplicated first item or a trailing separator.
- **identity rule:** Loop idiom: a loop that processes n items with n − 1 separators by handling one item outside the loop ('loop and a half').
- **declarative rule:** Print the first item before the loop, then loop over the rest printing separator then item: \`System.out.print(a[0]); for (int i = 1; i &lt; n; i++) System.out.print(", " + a[i]);\` (or print item then separator for all but the last).
- **operational sequencing rule:** Order: the first item is printed once before the loop test. Each pass then tests \`i &lt; n\`, prints the separator, prints a[i] and increments i, so a separator always comes before an item, never after the last one.
- **evaluation / result rule:** For a = {1, 2, 3} the output is \`1, 2, 3\`: 3 items and exactly 2 separators, with no leading or trailing separator.
- **state-transition rule:** One loop pass prints exactly one separator and one item and increments i by 1. The pre-loop statement prints one item and no separator.
- **composition rule (with a neighbour):** with for\_loop: The for loop's bounds must match the handled-outside item: if a[0] is printed before the loop, the loop must start at \`i = 1\`. Starting at 0 duplicates the first item, and \`i &lt;= n\` runs past the end.
- **plan / role rule:** Plan: fencepost / loop-and-a-half plan. It produces separated lists (\`1, 2, 3\`), joined strings, and drawings of n posts with n − 1 rails.
- **conservation rule:** Invariant: after k passes, the output holds k + 1 items and k separators. Moving the separator after the item inside the loop breaks this and leaves a trailing separator. Swapping the outside item from first to last needs the loop to cover 0 .. n−2 instead.
- **error rule:** rule broken: n items need n − 1 separators; one item must be handled outside the loop. (silent logic error)
- **error rule:** rule broken: Array indices run from 0 to length − 1; the item handled outside the loop must exist. (run-time exception)
- **applicability rule:** Use a fencepost loop whenever items are joined by separators or bounded by posts (CSV lines, comma lists, drawings). It is not needed when every item gets the same surrounding text; there, a plain loop is right.

## The whole prerequisite chain

- **Everything it builds on (16):** `arithmetic_operators`, `boolean`, `boolean_expression`, `comparison_operators`, `data_type`, `do_while_loop`, `expression`, `for_loop`, `identifier`, `literal`, `logical_operators`, `loop_control`, `loop_variable`, `primitive_type`, `variable`, `while_loop`
- **Everything that builds on it (0):** nothing
