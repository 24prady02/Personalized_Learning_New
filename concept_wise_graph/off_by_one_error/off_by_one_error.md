# off_by_one_error (`off_by_one_error`)

a loop or index that runs one time too many or too few (&lt; vs &lt;=, 0..n vs 1..n, length vs length-1)

Section 1.4 Arrays, topic 1.4.a Arrays in Java (declare, create, initialize; indexing; length; default values).

![The knowledge graph around off_by_one_error](off_by_one_error.png)

## At a glance

- **Needs first:** `indexing`, `loop_control`
- **Leads to:** nothing
- **Learned alongside:** `fencepost_loop`
- **Misconceptions:** `DoubleLoopIndexCount`, `OffByOneBound`
- **Errors:** `FencepostExtraSeparator`, `WrongIterationCount`
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 32 edges around this concept, each explained in the graph's own words.

## What it needs first (2)

A prerequisite edge means the other concept has to be understood before `off_by_one_error`.

### `indexing` comes before `off_by_one_error`

*a[i] -- 0-based access*

Indices start at 0, so the last element is a[N-1]; misreading this convention is the usual source of off-by-one errors.

- **Grounding:** book passage
- **How `off_by_one_error` combines with `indexing`:** Because indexing starts at 0, the last valid index is length-1, and that is the bound most often missed by one.

### `loop_control` comes before `off_by_one_error`

*the three slots: init ; condition ; update*

The initialization and the condition of a loop fix how many times it runs; one wrong bound makes it run once too many or too few.

- **Grounding:** book passage
- **How `off_by_one_error` combines with `loop_control`:** The start value and the condition together fix the number of passes; changing either by one changes the count by one.

## What it leads to (0)

These concepts need `off_by_one_error` first.

No concept has this one as a prerequisite.

## Learned alongside (1)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

### `off_by_one_error` alongside `fencepost_loop`

*n items need n - 1 separators: one item handled outside the loop*

An off-by-one error is a loop that runs once too many or too few; a fencepost loop is the correct plan for the case that needs one action more than the other.

- **Grounding:** book passage
- **How `off_by_one_error` combines with `fencepost_loop`:** When one action must happen once more (or less) than the other, the fencepost plan handles the extra case explicitly instead of risking an off-by-one.

## Misconceptions (2)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### DoubleLoopIndexCount

- **Wrong rule:** for (double x = 0.0; x &lt;= 1.0; x += 0.1) runs exactly 11 times.
- **Right rule:** Using a double as a for-loop index is legal but bad practice: the number of iterations depends on an equality test between double values, which may not give the result you expect.
- **Role of this concept:** context
- **Also an edge from `for_loop`:** for (double x = 0.0; x &lt;= 1.0; x += 0.1) runs exactly 11 times.
- **Also an edge from `loop_control`:** for (double x = 0.0; x &lt;= 1.0; x += 0.1) runs exactly 11 times.
- **Also an edge from `loop_variable`:** for (double x = 0.0; x &lt;= 1.0; x += 0.1) runs exactly 11 times.

### OffByOneBound

- **Wrong rule:** &lt; vs &lt;= and 0..n vs 0..n-1 are interchangeable
- **Right rule:** for (i = 0; i &lt; n; i++) runs n times with i going up to n - 1; with &lt;= it runs n + 1 times and reaches i = n.
- **Role of this concept:** context
- **Shows at level L0 as:** misconception: wrong rule: &lt; and &lt;= (and 0..n versus 0..n-1) are interchangeable in a loop bound. Right rule: i &lt; N runs N times from 0 and i &lt;= N runs N+1 times; with an array of length N only i &lt; N stays inside the indices 0..N-1.
- **Shows at level L0 as:** inconsistent trace: Applies the bound rule unevenly: writes i &lt; a.length in one loop and i &lt;= a.length in the next one over the same array. (here mixing in: "&lt; vs &lt;= and 0..n vs 0..n-1 are interchangeable")
- **Also an edge from `array_bounds`:** &lt; vs &lt;= and 0..n vs 0..n-1 are interchangeable
- **Also an edge from `array_reversal`:** &lt; vs &lt;= and 0..n vs 0..n-1 are interchangeable
- **Also an edge from `array_traversal`:** &lt; vs &lt;= and 0..n vs 0..n-1 are interchangeable
- **Also an edge from `boolean_flag_array`:** &lt; vs &lt;= and 0..n vs 0..n-1 are interchangeable
- **Also an edge from `loop_control`:** i &lt; n and i &lt;= n mean the same, so the loop runs until i equals n and the last pass can use a[n].
- **Also an edge from `simulation_loop`:** t &lt; T and t &lt;= T give the same number of moves.

## Errors (2)

An error edge states the rule that gets broken in a program, and the right rule.

### FencepostExtraSeparator

- **Wrong rule:** Prints item and separator together in the loop, leaving an extra separator at the end.
- **Right rule:** Handle one item outside the loop so n items get n - 1 separators.
- **Role of this concept:** context
- **Also an edge from `fencepost_loop`:** Prints item and separator together in the loop, leaving an extra separator at the end.

### WrongIterationCount

- **Wrong rule:** Updates the loop counter so that the loop runs the wrong number of times.
- **Right rule:** The init, test and update together decide the number of passes; trace them to check the count.
- **Role of this concept:** context
- **Also an edge from `for_loop`:** Updates the loop counter so that the loop runs the wrong number of times.
- **Also an edge from `loop_control`:** Updates the loop counter so that the loop runs the wrong number of times.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for off by one error: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to off by one error agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

off by one error -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (3 ways).

- **everyday reading** (folk-meaning rule): Everyday counting starts at 1 and 'up to N' includes N. Java arrays start at index 0 and end at N-1, and a loop with i &lt; N runs N times while i &lt;= N runs N+1 times.
- **misconception** (wrong rule / right rule; shows `OffByOneBound`): wrong rule: &lt; and &lt;= (and 0..n versus 0..n-1) are interchangeable in a loop bound. Right rule: i &lt; N runs N times from 0 and i &lt;= N runs N+1 times; with an array of length N only i &lt; N stays inside the indices 0..N-1.
- **inconsistent trace** (uneven-application rule; shows `OffByOneBound`): Applies the bound rule unevenly: writes i &lt; a.length in one loop and i &lt;= a.length in the next one over the same array. (here mixing in: "&lt; vs &lt;= and 0..n vs 0..n-1 are interchangeable")

### L1: Unistructural / atom x text surface

L1 for off by one error: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

off by one error -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

- **names the element** (identity rule): Off-by-one error: a loop or index that is one step too far or too short.
- **states the rule** (declarative rule): Indices run from 0 to N-1; a loop for (int i = 0; i &lt; N; i++) runs exactly N times. Misunderstanding the 0-based convention leads to off-by-one errors, which are hard to avoid and debug.

### L2: Multistructural / block x execution / preoperational

L2 for off by one error: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

off by one error -&gt; L2 (Multistructural): the answer applies the rules of off by one error to every part of the code, in order (3 ways).

- **line by line trace** (operational sequencing rule): Sequencing: to check a bound, trace the first pass (the start value) and the last pass (the value that makes the condition false), not only a middle pass.
- **output prediction** (evaluation / result rule): Result: for (i = 0; i &lt; 5; i++) gives i = 0..4, five passes; i &lt;= 5 gives six passes, and a[5] on an array of length 5 throws ArrayIndexOutOfBoundsException.
- **one step execution** (state-transition rule): State transition: one extra pass reads or writes one element past the end (an exception) or adds one term too many; one missing pass leaves the last element unprocessed.

### L3: Relational / relations x function (concrete operational begins)

L3 for off by one error: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

off by one error -&gt; L3 (Relational): the answer relates the parts (4 ways).

- **relation to neighbour** (composition rule (with a neighbour)): Because indexing starts at 0, the last valid index is length-1, and that is the bound most often missed by one.
- **relation to neighbour** (composition rule (with a neighbour)): The start value and the condition together fix the number of passes; changing either by one changes the count by one.
- **relation to neighbour** (composition rule (with a neighbour)): When one action must happen once more (or less) than the other, the fencepost plan handles the extra case explicitly instead of risking an off-by-one.
- **purpose of the whole** (plan / role rule): Plan: choose the bounds from the meaning (count N things, valid indices 0..N-1) and check the first and last pass, rather than guessing.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for off by one error: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

off by one error -&gt; L4 (Extended abstract): the answer reasons beyond the given code (5 ways).

- **predict a change** (conservation rule; shows `OffByOneBound`): Conservation: changing &lt; to &lt;= adds exactly one pass; starting at 1 instead of 0 removes exactly one; both keep the loop otherwise the same.
- **diagnose an error** (error rule): rule broken: The init, test and update together decide the number of passes; trace them to check the count. Kind: see node. Trigger class: see node
- **transfer to a new program** (applicability rule): Whenever writing a loop over a range or an array, write the bound from the count (i &lt; N for N passes from 0) and check the first and last values of the index by hand.
- **diagnose an error** (error rule): rule broken: A traversal of an array of length N must use indices 0..N-1. Kind: run-time exception. Trigger class: i &lt;= a.length, a[i+1] on the last pass, or a[i-1] at i = 0 (ArrayIndexOutOfBoundsException)
- **diagnose an error** (error rule): rule broken: A loop meant to run N times must run exactly N times. Kind: silent logic error. Trigger class: the loop stops one short or goes one too far, so the last element is skipped or one term too many is added

## Same topic

`off_by_one_error` belongs to the topic **Arrays in Java (declare, create, initialize; indexing; length; default values)** (`topic1.4.a`). The topic also contains: `args_length`, `array_creation`, `array_declaration`, `array_default_values`, `data_structure`, `indexing`, `length_field`.

## Rules of the concept (16)

- **folk-meaning rule:** Everyday counting starts at 1 and 'up to N' includes N. Java arrays start at index 0 and end at N-1, and a loop with i &lt; N runs N times while i &lt;= N runs N+1 times.
- **wrong rule / right rule:** OffByOneBound: wrong: &lt; and &lt;= (and 0..n versus 0..n-1) are interchangeable in a loop bound. \| right: i &lt; N runs N times from 0 and i &lt;= N runs N+1 times; with an array of length N only i &lt; N stays inside the indices 0..N-1.
- **uneven-application rule:** Applies the bound rule unevenly: writes i &lt; a.length in one loop and i &lt;= a.length in the next one over the same array.
- **identity rule:** Off-by-one error: a loop or index that is one step too far or too short.
- **declarative rule:** Indices run from 0 to N-1; a loop for (int i = 0; i &lt; N; i++) runs exactly N times. Misunderstanding the 0-based convention leads to off-by-one errors, which are hard to avoid and debug.
- **operational sequencing rule:** Sequencing: to check a bound, trace the first pass (the start value) and the last pass (the value that makes the condition false), not only a middle pass.
- **evaluation / result rule:** Result: for (i = 0; i &lt; 5; i++) gives i = 0..4, five passes; i &lt;= 5 gives six passes, and a[5] on an array of length 5 throws ArrayIndexOutOfBoundsException.
- **state-transition rule:** State transition: one extra pass reads or writes one element past the end (an exception) or adds one term too many; one missing pass leaves the last element unprocessed.
- **composition rule (with a neighbour):** with indexing: Because indexing starts at 0, the last valid index is length-1, and that is the bound most often missed by one.
- **composition rule (with a neighbour):** with loop\_control: The start value and the condition together fix the number of passes; changing either by one changes the count by one.
- **composition rule (with a neighbour):** with fencepost\_loop: When one action must happen once more (or less) than the other, the fencepost plan handles the extra case explicitly instead of risking an off-by-one.
- **plan / role rule:** Plan: choose the bounds from the meaning (count N things, valid indices 0..N-1) and check the first and last pass, rather than guessing.
- **conservation rule:** Conservation: changing &lt; to &lt;= adds exactly one pass; starting at 1 instead of 0 removes exactly one; both keep the loop otherwise the same.
- **error rule:** rule broken: A traversal of an array of length N must use indices 0..N-1. (run-time exception)
- **error rule:** rule broken: A loop meant to run N times must run exactly N times. (silent logic error)
- **applicability rule:** Whenever writing a loop over a range or an array, write the bound from the count (i &lt; N for N passes from 0) and check the first and last values of the index by hand.

## The whole prerequisite chain

- **Everything it builds on (20):** `arithmetic_operators`, `array_creation`, `array_declaration`, `array_initializer`, `boolean`, `boolean_expression`, `comparison_operators`, `data_structure`, `data_type`, `do_while_loop`, `expression`, `identifier`, `indexing`, `literal`, `logical_operators`, `loop_control`, `loop_variable`, `primitive_type`, `variable`, `while_loop`
- **Everything that builds on it (0):** nothing
