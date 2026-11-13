# sentinel_loop (`sentinel_loop`)

reading until a special stop value (Rainfall problem)

Section 1.5 Input and Output, topic 1.5.c Standard input.

![The knowledge graph around sentinel_loop](sentinel_loop.png)

## At a glance

- **Needs first:** `accumulator_pattern`, `read_loop_idiom`, `while_loop`
- **Leads to:** nothing
- **Learned alongside:** nothing
- **Misconceptions:** `SentinelProcessed`
- **Errors:** `AverageWithoutZeroGuard`, `NegativeNotFiltered`
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 22 edges around this concept, each explained in the graph's own words.

## What it needs first (3)

A prerequisite edge means the other concept has to be understood before `sentinel_loop`.

### `accumulator_pattern` comes before `sentinel_loop`

*building up a running total/result*

Sum and count are accumulators.

- **Grounding:** questionable
- **How `sentinel_loop` combines with `accumulator_pattern`:** sum (a gatherer) and count must change only for values that are not the sentinel and pass the filter. The average is computed once, after the loop.
- **How `accumulator_pattern` combines with `sentinel_loop`:** In a sentinel loop the sum and the count of the values read are both accumulators, updated only for values that are not the sentinel.

### `read_loop_idiom` comes before `sentinel_loop`

*reading until end-of-input*

The sentinel loop is a read loop with its own stop value.

- **Grounding:** questionable
- **How `sentinel_loop` combines with `read_loop_idiom`:** The sentinel test replaces, or is added to, the isEmpty() test. If the sentinel may be missing, keep !StdIn.isEmpty() in the condition so the program does not read past the end.
- **How `read_loop_idiom` combines with `sentinel_loop`:** A sentinel loop keeps the read-then-test structure but stops on a special data value instead of, or as well as, isEmpty(). The sentinel must be tested before it is processed.

### `while_loop` comes before `sentinel_loop`

*repeat a block while a condition holds*

A sentinel loop is a while loop whose condition tests each value read against the stop value.

- **Grounding:** spec passage

## What it leads to (0)

These concepts need `sentinel_loop` first.

No concept has this one as a prerequisite.

## Learned alongside (0)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

No parallel edge touches this concept.

## Misconceptions (1)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### SentinelProcessed

- **Wrong rule:** The sentinel value (e.g. 999999) is added to the total like the other values.
- **Right rule:** The loop stops at the sentinel without processing it.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: The sentinel value (e.g. 99999) is added to the total like the other values. Right rule: The value is tested against the sentinel before it is processed. The loop stops at the sentinel, which is never added or counted.
- **Shows at level L0 as:** inconsistent trace: Points to LT (read, test for the sentinel, then process). An uneven trace processes before testing on the last pass, so the sentinel is included that time. (here mixing in: "The sentinel value (e.g. 999999) is added to the total like the other values")

## Errors (2)

An error edge states the rule that gets broken in a program, and the right rule.

### AverageWithoutZeroGuard

- **Wrong rule:** Computes sum / count without checking that count is above 0.
- **Right rule:** If no value was read (count is 0), do not compute the average: with int operands sum / count is a division by zero, a run-time exception that stops the program; with a double sum the division does not stop the program and gives a meaningless value instead of an average.
- **Role of this concept:** primary
- **Also an edge from `division_by_zero`:** Computes sum / count without checking that count is above 0.

### NegativeNotFiltered

- **Wrong rule:** Adds negative rainfall values to the total.
- **Right rule:** Values outside the range of interest must be filtered out (for example with if (t &gt;= lo &amp;&amp; t &lt;= hi)) before they are processed.
- **Role of this concept:** primary
- **Also an edge from `filter`:** Adds negative rainfall values to the total.
- **Also an edge from `input_validation`:** Adds negative rainfall values to the total.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for sentinel loop: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to sentinel loop agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

sentinel loop -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (3 ways).

- **everyday reading** (folk-meaning rule): In everyday lists the last number written is part of the data. A sentinel such as 99999 is a stop marker, not data, so it must not be summed or counted.
- **misconception** (wrong rule / right rule; shows `SentinelProcessed`): wrong rule: The sentinel value (e.g. 99999) is added to the total like the other values. Right rule: The value is tested against the sentinel before it is processed. The loop stops at the sentinel, which is never added or counted.
- **inconsistent trace** (uneven-application rule; shows `SentinelProcessed`): Points to LT (read, test for the sentinel, then process). An uneven trace processes before testing on the last pass, so the sentinel is included that time. (here mixing in: "The sentinel value (e.g. 999999) is added to the total like the other values")

### L1: Unistructural / atom x text surface

L1 for sentinel loop: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

sentinel loop -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

- **names the element** (identity rule): A sentinel loop is a read loop that stops when it reads a designated stop value that cannot occur as real data (the Rainfall problem).
- **states the rule** (declarative rule): Read a value; while it is not the sentinel, process it and read the next one. The sentinel is never processed.

### L2: Multistructural / block x execution / preoperational

L2 for sentinel loop: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

sentinel loop -&gt; L2 (Multistructural): the answer applies the rules of sentinel loop to every part of the code, in order (3 ways).

- **line by line trace** (operational sequencing rule): A priming read comes before the loop, then each pass runs: test value != SENTINEL, process (sum += v; count++), then read the next value at the end of the body. An equivalent form is while (true) { v = read; if (v == SENTINEL) break; process; }.
- **output prediction** (evaluation / result rule): With input 3 -1 5 99999 7, keeping only non-negative values, the Rainfall average is (3+5)/2 = 4.0. The 7 after the sentinel is never read.
- **one step execution** (state-transition rule): One pass reads one value. If it is the sentinel, the loop ends with sum and count unchanged; otherwise the (valid) value updates sum and count.

### L3: Relational / relations x function (concrete operational begins)

L3 for sentinel loop: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

sentinel loop -&gt; L3 (Relational): the answer relates the parts (3 ways).

- **relation to neighbour** (composition rule (with a neighbour)): The sentinel test replaces, or is added to, the isEmpty() test. If the sentinel may be missing, keep !StdIn.isEmpty() in the condition so the program does not read past the end.
- **relation to neighbour** (composition rule (with a neighbour)): sum (a gatherer) and count must change only for values that are not the sentinel and pass the filter. The average is computed once, after the loop.
- **purpose of the whole** (plan / role rule): Plan: Soloway's sentinel-controlled running-total loop (Rainfall). Roles: sum is a gatherer, count a stepper, and the value read a most-recent holder.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for sentinel loop: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

sentinel loop -&gt; L4 (Extended abstract): the answer reasons beyond the given code (6 ways).

- **predict a change** (conservation rule; shows `SentinelProcessed`): Changing the sentinel keeps the behaviour only if the new value cannot occur in the data. Moving the test after the processing step breaks the invariant that the sentinel is never processed.
- **diagnose an error** (error rule): rule broken: Check count &gt; 0 before computing sum / count. Kind: run-time exception. Trigger class: The sentinel is the first value (count stays 0). With int operands this gives ArithmeticException (/ by zero); with a double sum it gives NaN silently.
- **diagnose an error** (error rule): rule broken: Only values in the range of interest may be processed. Kind: silent logic error. Trigger class: Inputs below 0 (or outside lo..hi) are added to the total because no if (t &gt;= lo &amp;&amp; t &lt;= hi) guard comes before the update.
- **transfer to a new program** (applicability rule): Use a sentinel when the data stream marks its own end with a value outside the valid range (keyed entry with no end-of-file). If every value could be real data, use isEmpty() or a count instead.
- **diagnose an error** (error rule): rule broken: The sentinel must appear, or the loop must also test isEmpty(). Kind: run-time exception. Trigger class: The input ends without the sentinel, so the next read happens after the input is exhausted.
- **diagnose an error** (error rule): rule broken: The sentinel must not be included in the computation. Kind: silent logic error. Trigger class: A process-then-test ordering adds 99999 to sum and count once.

## Same topic

`sentinel_loop` belongs to the topic **Standard input** (`topic1.5.c`). The topic also contains: `end_of_input`, `input_format`, `input_validation`, `interactive_input`, `read_loop_idiom`, `standard_input`, `token_vs_line_input`.

## Rules of the concept (17)

- **folk-meaning rule:** In everyday lists the last number written is part of the data. A sentinel such as 99999 is a stop marker, not data, so it must not be summed or counted.
- **wrong rule / right rule:** SentinelProcessed: wrong: The sentinel value (e.g. 99999) is added to the total like the other values. \| right: The value is tested against the sentinel before it is processed. The loop stops at the sentinel, which is never added or counted.
- **uneven-application rule:** Points to LT (read, test for the sentinel, then process). An uneven trace processes before testing on the last pass, so the sentinel is included that time.
- **identity rule:** A sentinel loop is a read loop that stops when it reads a designated stop value that cannot occur as real data (the Rainfall problem).
- **declarative rule:** Read a value; while it is not the sentinel, process it and read the next one. The sentinel is never processed.
- **operational sequencing rule:** A priming read comes before the loop, then each pass runs: test value != SENTINEL, process (sum += v; count++), then read the next value at the end of the body. An equivalent form is while (true) { v = read; if (v == SENTINEL) break; process; }.
- **evaluation / result rule:** With input 3 -1 5 99999 7, keeping only non-negative values, the Rainfall average is (3+5)/2 = 4.0. The 7 after the sentinel is never read.
- **state-transition rule:** One pass reads one value. If it is the sentinel, the loop ends with sum and count unchanged; otherwise the (valid) value updates sum and count.
- **composition rule (with a neighbour):** with read\_loop\_idiom: The sentinel test replaces, or is added to, the isEmpty() test. If the sentinel may be missing, keep !StdIn.isEmpty() in the condition so the program does not read past the end.
- **composition rule (with a neighbour):** with accumulator\_pattern: sum (a gatherer) and count must change only for values that are not the sentinel and pass the filter. The average is computed once, after the loop.
- **plan / role rule:** Plan: Soloway's sentinel-controlled running-total loop (Rainfall). Roles: sum is a gatherer, count a stepper, and the value read a most-recent holder.
- **conservation rule:** Changing the sentinel keeps the behaviour only if the new value cannot occur in the data. Moving the test after the processing step breaks the invariant that the sentinel is never processed.
- **error rule:** rule broken: Check count &gt; 0 before computing sum / count. (run-time exception)
- **error rule:** rule broken: Only values in the range of interest may be processed. (silent logic error)
- **error rule:** rule broken: The sentinel must appear, or the loop must also test isEmpty(). (run-time exception)
- **error rule:** rule broken: The sentinel must not be included in the computation. (silent logic error)
- **applicability rule:** Use a sentinel when the data stream marks its own end with a value outside the valid range (keyed entry with no end-of-file). If every value could be real data, use isEmpty() or a count instead.

## The whole prerequisite chain

- **Everything it builds on (32):** `accumulator_pattern`, `arithmetic_operators`, `assignment`, `boolean`, `boolean_expression`, `class_declaration`, `command_line_args`, `comparison_operators`, `compound_assignment`, `data_type`, `declaration`, `do_while_loop`, `explicit_cast`, `expression`, `for_loop`, `identifier`, `integer_division`, `literal`, `logical_operators`, `loop_body`, `loop_control`, `loop_variable`, `main_method`, `parsing`, `primitive_type`, `program_text`, `read_loop_idiom`, `standard_input`, `stream_model`, `type_conversion`, `variable`, `while_loop`
- **Everything that builds on it (0):** nothing
