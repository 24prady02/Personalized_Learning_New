# read_loop_idiom (`read_loop_idiom`)

reading until end-of-input

Section 1.5 Input and Output, topic 1.5.c Standard input.

![The knowledge graph around read_loop_idiom](read_loop_idiom.png)

## At a glance

- **Needs first:** `standard_input`
- **Leads to:** `end_of_input`, `sentinel_loop`
- **Learned alongside:** nothing
- **Misconceptions:** `AssignmentNotExpression`, `InputReadOnceBeforeLoop`
- **Errors:** `ReadPastEndOfInput`
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 25 edges around this concept, each explained in the graph's own words.

## What it needs first (1)

A prerequisite edge means the other concept has to be understood before `read_loop_idiom`.

### `standard_input` comes before `read_loop_idiom`

*StdIn -- reading a stream of values*

The read loop repeats StdIn reads until StdIn.isEmpty() returns true.

- **Grounding:** book passage
- **How `read_loop_idiom` combines with `standard_input`:** isEmpty() false guarantees only one more token. A body that reads k values per pass assumes the input count is a multiple of k.
- **How `standard_input` combines with `read_loop_idiom`:** To read an unknown number of values, each read must be guarded by !StdIn.isEmpty() as the condition of a while loop whose body reads.

## What it leads to (2)

These concepts need `read_loop_idiom` first.

### `read_loop_idiom` comes before `end_of_input`

*StdIn.isEmpty() and the end-of-file keystroke*

The read loop runs until StdIn.isEmpty() returns true, which happens when the user types the end-of-file sequence (&lt;ctrl-d&gt;).

- **Grounding:** book passage
- **How `read_loop_idiom` combines with `end_of_input`:** The loop ends only when isEmpty() becomes true: at the end of a redirected file, or after the end-of-file keystroke (&lt;ctrl-d&gt;, or &lt;ctrl-z&gt; on some systems).
- **How `end_of_input` combines with `read_loop_idiom`:** isEmpty() is the condition of the read loop, so the loop ends exactly when end-of-file is reached (&lt;ctrl-d&gt; at the keyboard, end of file with &lt;).

### `read_loop_idiom` comes before `sentinel_loop`

*reading until a special stop value (Rainfall problem)*

The sentinel loop is a read loop with its own stop value.

- **Grounding:** questionable
- **How `read_loop_idiom` combines with `sentinel_loop`:** A sentinel loop keeps the read-then-test structure but stops on a special data value instead of, or as well as, isEmpty(). The sentinel must be tested before it is processed.
- **How `sentinel_loop` combines with `read_loop_idiom`:** The sentinel test replaces, or is added to, the isEmpty() test. If the sentinel may be missing, keep !StdIn.isEmpty() in the condition so the program does not read past the end.

## Learned alongside (0)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

No parallel edge touches this concept.

## Misconceptions (2)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### AssignmentNotExpression

- **Wrong rule:** A read and a test cannot be combined, so while ((x = read()) != end) is not allowed.
- **Right rule:** while ((x = read()) != end) reads a value into x and tests that same value in one expression.
- **Role of this concept:** context
- **Shows at level L0 as:** misconception: wrong rule: An assignment cannot be used inside a larger expression. Right rule: An assignment is an expression whose value is the value assigned, so (x = v) both stores v in x and yields v. This is used, for example, in while ((line = in.readLine()) != null).
- **Also an edge from `assignment`:** An assignment cannot be used inside a larger expression, so a condition like (x = read()) != v is not allowed.
- **Also an edge from `chained_assignment`:** an assignment cannot be used inside a larger expression
- **Also an edge from `expression`:** An assignment cannot be used inside a larger expression, so a condition like (x = read()) != v is not allowed.

### InputReadOnceBeforeLoop

- **Wrong rule:** Reading a value once before the loop is enough; the loop will process each new input value.
- **Right rule:** A read loop must read the next value inside the body on every pass; otherwise it keeps processing the same value.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: Reading a value once before the loop is enough; the loop will process each new input value. Right rule: The read must be inside the loop body so that every pass consumes a new value.
- **Shows at level L0 as:** inconsistent trace: Points to LT (test !isEmpty(), then read, then process, on every pass). An uneven trace processes the old value before reading on some passes, or reads twice on one pass. (here mixing in: "Reading a value once before the loop is enough; the loop will process each new input value")
- **Also an edge from `standard_input`:** Reading a value once before the loop is enough; the loop will process each new input value.

## Errors (1)

An error edge states the rule that gets broken in a program, and the right rule.

### ReadPastEndOfInput

- **Wrong rule:** Calls StdIn.readInt() again after the input has run out.
- **Right rule:** Reading after standard input is exhausted is a run-time error; test StdIn.isEmpty() before each read.
- **Role of this concept:** context
- **Also an edge from `end_of_input`:** Calls StdIn.readInt() again after the input has run out.
- **Also an edge from `standard_input`:** Calls StdIn.readInt() again after the input has run out.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for read loop idiom: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to read loop idiom agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

read loop idiom -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (4 ways).

- **everyday reading** (folk-meaning rule): Everyday 'read until the end' assumes you know how long the text is, and 'empty' suggests a blank screen or line. The stream's length is unknown to the program, and isEmpty() is true only when no more tokens remain.
- **misconception** (wrong rule / right rule; shows `InputReadOnceBeforeLoop`): wrong rule: Reading a value once before the loop is enough; the loop will process each new input value. Right rule: The read must be inside the loop body so that every pass consumes a new value.
- **inconsistent trace** (uneven-application rule; shows `InputReadOnceBeforeLoop`): Points to LT (test !isEmpty(), then read, then process, on every pass). An uneven trace processes the old value before reading on some passes, or reads twice on one pass. (here mixing in: "Reading a value once before the loop is enough; the loop will process each new input value")
- **misconception** (wrong rule / right rule; shows `AssignmentNotExpression`): wrong rule: An assignment cannot be used inside a larger expression. Right rule: An assignment is an expression whose value is the value assigned, so (x = v) both stores v in x and yields v. This is used, for example, in while ((line = in.readLine()) != null).

### L1: Unistructural / atom x text surface

L1 for read loop idiom: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

read loop idiom -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

- **names the element** (identity rule): The read loop is an input idiom: a while loop whose condition is !StdIn.isEmpty() and whose body reads one value and processes it.
- **states the rule** (declarative rule): Before each read, call StdIn.isEmpty() to check whether more values remain. isEmpty() is true when only whitespace is left.

### L2: Multistructural / block x execution / preoperational

L2 for read loop idiom: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

read loop idiom -&gt; L2 (Multistructural): the answer applies the rules of read loop idiom to every part of the code, in order (3 ways).

- **line by line trace** (operational sequencing rule): Each pass: evaluate !StdIn.isEmpty(). If it is true, read one value, then process it (e.g. sum += value; cnt++;) and go back to the test. If it is false, leave the loop and run the code after it (e.g. compute and print the average).
- **output prediction** (evaluation / result rule): After the loop, every value has been read exactly once and the accumulators hold their totals. Average with input 10.0 5.0 6.0 3.0 7.0 32.0 &lt;ctrl-d&gt; prints Average is 10.5.
- **one step execution** (state-transition rule): One pass consumes exactly one value (or one fixed group, e.g. an x, y pair) and updates the loop's accumulators. The isEmpty() test consumes nothing.

### L3: Relational / relations x function (concrete operational begins)

L3 for read loop idiom: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

read loop idiom -&gt; L3 (Relational): the answer relates the parts (4 ways).

- **relation to neighbour** (composition rule (with a neighbour)): isEmpty() false guarantees only one more token. A body that reads k values per pass assumes the input count is a multiple of k.
- **relation to neighbour** (composition rule (with a neighbour)): The loop ends only when isEmpty() becomes true: at the end of a redirected file, or after the end-of-file keystroke (&lt;ctrl-d&gt;, or &lt;ctrl-z&gt; on some systems).
- **relation to neighbour** (composition rule (with a neighbour)): A sentinel loop keeps the read-then-test structure but stops on a special data value instead of, or as well as, isEmpty(). The sentinel must be tested before it is processed.
- **purpose of the whole** (plan / role rule): Plan: the process-all-input loop (Soloway's read/process loop). sum is a gatherer and cnt a counter (stepper), and value is a most-recent holder.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for read loop idiom: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

read loop idiom -&gt; L4 (Extended abstract): the answer reasons beyond the given code (4 ways).

- **predict a change** (conservation rule; shows `InputReadOnceBeforeLoop`): The loop works for any input length, including 0 (the body is skipped). With empty input, though, Average's sum / cnt is 0.0/0 = NaN. Moving the read out of the loop breaks it, so one value is reused forever.
- **transfer to a new program** (applicability rule): Use the read loop when the number of values is unknown and all input should be processed. When N is given first, use a counted for loop (AddInts). Use a sentinel loop when a stop value marks the end.
- **diagnose an error** (error rule): rule broken: Every read needs a preceding isEmpty() check that guarantees a value. Kind: run-time exception. Trigger class: A body that reads more values than remain (two reads per pass with an odd count), or a condition that does not test isEmpty().
- **diagnose an error** (error rule): rule broken: Do not divide by a count of 0. Kind: silent logic error. Trigger class: Empty input: the double average sum / cnt evaluates to NaN instead of stopping (it would be ArithmeticException if both were int).

## Same topic

`read_loop_idiom` belongs to the topic **Standard input** (`topic1.5.c`). The topic also contains: `end_of_input`, `input_format`, `input_validation`, `interactive_input`, `sentinel_loop`, `standard_input`, `token_vs_line_input`.

## Rules of the concept (17)

- **folk-meaning rule:** Everyday 'read until the end' assumes you know how long the text is, and 'empty' suggests a blank screen or line. The stream's length is unknown to the program, and isEmpty() is true only when no more tokens remain.
- **wrong rule / right rule:** AssignmentNotExpression: wrong: An assignment cannot be used inside a larger expression. \| right: An assignment is an expression whose value is the value assigned, so (x = v) both stores v in x and yields v. This is used, for example, in while ((line = in.readLine()) != null).
- **wrong rule / right rule:** InputReadOnceBeforeLoop: wrong: Reading a value once before the loop is enough; the loop will process each new input value. \| right: The read must be inside the loop body so that every pass consumes a new value.
- **uneven-application rule:** Points to LT (test !isEmpty(), then read, then process, on every pass). An uneven trace processes the old value before reading on some passes, or reads twice on one pass.
- **identity rule:** The read loop is an input idiom: a while loop whose condition is !StdIn.isEmpty() and whose body reads one value and processes it.
- **declarative rule:** Before each read, call StdIn.isEmpty() to check whether more values remain. isEmpty() is true when only whitespace is left.
- **operational sequencing rule:** Each pass: evaluate !StdIn.isEmpty(). If it is true, read one value, then process it (e.g. sum += value; cnt++;) and go back to the test. If it is false, leave the loop and run the code after it (e.g. compute and print the average).
- **evaluation / result rule:** After the loop, every value has been read exactly once and the accumulators hold their totals. Average with input 10.0 5.0 6.0 3.0 7.0 32.0 &lt;ctrl-d&gt; prints Average is 10.5.
- **state-transition rule:** One pass consumes exactly one value (or one fixed group, e.g. an x, y pair) and updates the loop's accumulators. The isEmpty() test consumes nothing.
- **composition rule (with a neighbour):** with standard\_input: isEmpty() false guarantees only one more token. A body that reads k values per pass assumes the input count is a multiple of k.
- **composition rule (with a neighbour):** with end\_of\_input: The loop ends only when isEmpty() becomes true: at the end of a redirected file, or after the end-of-file keystroke (&lt;ctrl-d&gt;, or &lt;ctrl-z&gt; on some systems).
- **composition rule (with a neighbour):** with sentinel\_loop: A sentinel loop keeps the read-then-test structure but stops on a special data value instead of, or as well as, isEmpty(). The sentinel must be tested before it is processed.
- **plan / role rule:** Plan: the process-all-input loop (Soloway's read/process loop). sum is a gatherer and cnt a counter (stepper), and value is a most-recent holder.
- **conservation rule:** The loop works for any input length, including 0 (the body is skipped). With empty input, though, Average's sum / cnt is 0.0/0 = NaN. Moving the read out of the loop breaks it, so one value is reused forever.
- **error rule:** rule broken: Every read needs a preceding isEmpty() check that guarantees a value. (run-time exception)
- **error rule:** rule broken: Do not divide by a count of 0. (silent logic error)
- **applicability rule:** Use the read loop when the number of values is unknown and all input should be processed. When N is given first, use a counted for loop (AddInts). Use a sentinel loop when a stop value marks the end.

## The whole prerequisite chain

- **Everything it builds on (2):** `standard_input`, `stream_model`
- **Everything that builds on it (2):** `end_of_input`, `sentinel_loop`
