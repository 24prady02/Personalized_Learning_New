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

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 25 edges around this concept. The edge logic, the wrong and right rules and the exact rules of the ways are copied word for word from the graph.

## To work on (1)

- no aliases: a student's words cannot name this concept

## What it needs first (1)

A prerequisite edge means the other concept has to be understood before `read_loop_idiom`.

### `standard_input` comes before `read_loop_idiom`

*StdIn -- reading a stream of values*

- **Edge:** `pre:standard_input->read_loop_idiom`
- **Exact edge logic:** The read loop repeats StdIn reads until StdIn.isEmpty() returns true.
- **Grounding:** book\_passage
- **Composition rule (R) of `read_loop_idiom` with `standard_input`:** isEmpty() false guarantees only one more token. A body that reads k values per pass assumes the input count is a multiple of k.
- **Composition rule (R) of `standard_input` with `read_loop_idiom`:** To read an unknown number of values, each read must be guarded by !StdIn.isEmpty() as the condition of a while loop whose body reads.

## What it leads to (2)

These concepts need `read_loop_idiom` first.

### `read_loop_idiom` comes before `end_of_input`

*StdIn.isEmpty() and the end-of-file keystroke*

- **Edge:** `pre:read_loop_idiom->end_of_input`
- **Exact edge logic:** The read loop runs until StdIn.isEmpty() returns true, which happens when the user types the end-of-file sequence (&lt;ctrl-d&gt;).
- **Grounding:** book\_passage
- **Composition rule (R) of `read_loop_idiom` with `end_of_input`:** The loop ends only when isEmpty() becomes true: at the end of a redirected file, or after the end-of-file keystroke (&lt;ctrl-d&gt;, or &lt;ctrl-z&gt; on some systems).
- **Composition rule (R) of `end_of_input` with `read_loop_idiom`:** isEmpty() is the condition of the read loop, so the loop ends exactly when end-of-file is reached (&lt;ctrl-d&gt; at the keyboard, end of file with &lt;).

### `read_loop_idiom` comes before `sentinel_loop`

*reading until a special stop value (Rainfall problem)*

- **Edge:** `pre:read_loop_idiom->sentinel_loop`
- **Exact edge logic:** The sentinel loop is a read loop with its own stop value.
- **Grounding:** questionable
- **Composition rule (R) of `read_loop_idiom` with `sentinel_loop`:** A sentinel loop keeps the read-then-test structure but stops on a special data value instead of, or as well as, isEmpty(). The sentinel must be tested before it is processed.
- **Composition rule (R) of `sentinel_loop` with `read_loop_idiom`:** The sentinel test replaces, or is added to, the isEmpty() test. If the sentinel may be missing, keep !StdIn.isEmpty() in the condition so the program does not read past the end.

## Learned alongside (0)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

No parallel edge touches this concept.

## Misconceptions (2)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### AssignmentNotExpression

- **Edge:** `read_loop_idiom` &rarr; `AssignmentNotExpression` (misconception)
- **Exact edge logic (the wrong rule):** A read and a test cannot be combined, so while ((x = read()) != end) is not allowed.
- **Twin logic (the right rule):** while ((x = read()) != end) reads a value into x and tests that same value in one expression.
- **Wrong belief (on the node):** an assignment cannot be used inside a larger expression
- **Correct rule (on the node):** An assignment is an expression whose value is the value assigned, so (x = v) both stores v in x and gives v.
- **Provenance:** published
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [3] misconception, exact rule:** wrong rule: An assignment cannot be used inside a larger expression. Right rule: An assignment is an expression whose value is the value assigned, so (x = v) both stores v in x and yields v. This is used, for example, in while ((line = in.readLine()) != null).
- **Edge `assignment` &rarr; `AssignmentNotExpression`, exact edge logic:** An assignment cannot be used inside a larger expression, so a condition like (x = read()) != v is not allowed. **Twin logic:** An assignment is an expression whose value is the value assigned, so (x = v) both stores v in x and gives v. (role: primary)
- **Edge `chained_assignment` &rarr; `AssignmentNotExpression`, exact edge logic:** an assignment cannot be used inside a larger expression **Twin logic:** An assignment is an expression whose value is the value assigned, so (x = v) both stores v in x and gives v. (role: context)
- **Edge `expression` &rarr; `AssignmentNotExpression`, exact edge logic:** An assignment cannot be used inside a larger expression, so a condition like (x = read()) != v is not allowed. **Twin logic:** An assignment is an expression whose value is the value assigned, so (x = v) both stores v in x and gives v. (role: context)

### InputReadOnceBeforeLoop

- **Edge:** `read_loop_idiom` &rarr; `InputReadOnceBeforeLoop` (misconception)
- **Exact edge logic (the wrong rule):** Reading a value once before the loop is enough; the loop will process each new input value.
- **Twin logic (the right rule):** A read loop must read the next value inside the body on every pass; otherwise it keeps processing the same value.
- **Wrong belief (on the node):** Reading a value once before the loop is enough; the loop will process each new input value.
- **Correct rule (on the node):** A read loop must read the next value inside the body on every pass; otherwise it keeps processing the same value.
- **Provenance:** published
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [1] misconception, exact rule:** wrong rule: Reading a value once before the loop is enough; the loop will process each new input value. Right rule: The read must be inside the loop body so that every pass consumes a new value.
- **L0 way [2] inconsistent\_trace, exact rule:** Points to LT (test !isEmpty(), then read, then process, on every pass). An uneven trace processes the old value before reading on some passes, or reads twice on one pass. (here mixing in: "Reading a value once before the loop is enough; the loop will process each new input value")
- **Edge `standard_input` &rarr; `InputReadOnceBeforeLoop`, exact edge logic:** Reading a value once before the loop is enough; the loop will process each new input value. **Twin logic:** A read loop must read the next value inside the body on every pass; otherwise it keeps processing the same value. (role: context)

## Errors (1)

An error edge states the rule that gets broken in a program, and the right rule.

### ReadPastEndOfInput

- **Edge:** `read_loop_idiom` &rarr; `ReadPastEndOfInput` (error)
- **Exact edge logic (the wrong rule):** Calls StdIn.readInt() again after the input has run out.
- **Twin logic (the right rule):** Reading after standard input is exhausted is a run-time error; test StdIn.isEmpty() before each read.
- **Wrong belief (on the node):** Calls StdIn.readInt() again after the input has run out.
- **Correct rule (on the node):** Reading after standard input is exhausted is a run-time error; test StdIn.isEmpty() before each read.
- **Provenance:** textbook
- **Role of this concept:** context
- **Edge `end_of_input` &rarr; `ReadPastEndOfInput`, exact edge logic:** Calls StdIn.readInt() again after the input has run out. **Twin logic:** Reading after standard input is exhausted is a run-time error; test StdIn.isEmpty() before each read. (role: primary)
- **Edge `standard_input` &rarr; `ReadPastEndOfInput`, exact edge logic:** Calls StdIn.readInt() again after the input has run out. **Twin logic:** Reading after standard input is exhausted is a run-time error; test StdIn.isEmpty() before each read. (role: context)

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for read loop idiom: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to read loop idiom agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

- **Edge:** `read_loop_idiom` &rarr; `read_loop_idiom@L0` (has_level)
- **Exact edge logic:** read loop idiom -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (4 ways).

Ways (4), each with its exact rule:

- **[0] everyday\_reading** (rule type E, folk-meaning rule): Everyday 'read until the end' assumes you know how long the text is, and 'empty' suggests a blank screen or line. The stream's length is unknown to the program, and isEmpty() is true only when no more tokens remain.
- **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `InputReadOnceBeforeLoop`: wrong rule: Reading a value once before the loop is enough; the loop will process each new input value. Right rule: The read must be inside the loop body so that every pass consumes a new value.
- **[2] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `InputReadOnceBeforeLoop`: Points to LT (test !isEmpty(), then read, then process, on every pass). An uneven trace processes the old value before reading on some passes, or reads twice on one pass. (here mixing in: "Reading a value once before the loop is enough; the loop will process each new input value")
- **[3] misconception** (rule type M, wrong rule / right rule) &rarr; `AssignmentNotExpression`: wrong rule: An assignment cannot be used inside a larger expression. Right rule: An assignment is an expression whose value is the value assigned, so (x = v) both stores v in x and yields v. This is used, for example, in while ((line = in.readLine()) != null).

### L1: Unistructural / atom x text surface

L1 for read loop idiom: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

- **Edge:** `read_loop_idiom` &rarr; `read_loop_idiom@L1` (has_level)
- **Exact edge logic:** read loop idiom -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

Ways (2), each with its exact rule:

- **[0] names\_the\_element** (rule type N, identity rule): The read loop is an input idiom: a while loop whose condition is !StdIn.isEmpty() and whose body reads one value and processes it.
- **[1] states\_the\_rule** (rule type S, declarative rule): Before each read, call StdIn.isEmpty() to check whether more values remain. isEmpty() is true when only whitespace is left.

### L2: Multistructural / block x execution / preoperational

L2 for read loop idiom: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

- **Edge:** `read_loop_idiom` &rarr; `read_loop_idiom@L2` (has_level)
- **Exact edge logic:** read loop idiom -&gt; L2 (Multistructural): the answer applies the rules of read loop idiom to every part of the code, in order (3 ways).

Ways (3), each with its exact rule:

- **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): Each pass: evaluate !StdIn.isEmpty(). If it is true, read one value, then process it (e.g. sum += value; cnt++;) and go back to the test. If it is false, leave the loop and run the code after it (e.g. compute and print the average).
- **[1] output\_prediction** (rule type OP, evaluation / result rule): After the loop, every value has been read exactly once and the accumulators hold their totals. Average with input 10.0 5.0 6.0 3.0 7.0 32.0 &lt;ctrl-d&gt; prints Average is 10.5.
- **[2] one\_step\_execution** (rule type OS, state-transition rule): One pass consumes exactly one value (or one fixed group, e.g. an x, y pair) and updates the loop's accumulators. The isEmpty() test consumes nothing.

### L3: Relational / relations x function (concrete operational begins)

L3 for read loop idiom: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

- **Edge:** `read_loop_idiom` &rarr; `read_loop_idiom@L3` (has_level)
- **Exact edge logic:** read loop idiom -&gt; L3 (Relational): the answer relates the parts (4 ways).

Ways (4), each with its exact rule:

- **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): isEmpty() false guarantees only one more token. A body that reads k values per pass assumes the input count is a multiple of k.
- **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): The loop ends only when isEmpty() becomes true: at the end of a redirected file, or after the end-of-file keystroke (&lt;ctrl-d&gt;, or &lt;ctrl-z&gt; on some systems).
- **[2] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): A sentinel loop keeps the read-then-test structure but stops on a special data value instead of, or as well as, isEmpty(). The sentinel must be tested before it is processed.
- **[3] purpose\_of\_the\_whole** (rule type P, plan / role rule): Plan: the process-all-input loop (Soloway's read/process loop). sum is a gatherer and cnt a counter (stepper), and value is a most-recent holder.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for read loop idiom: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

- **Edge:** `read_loop_idiom` &rarr; `read_loop_idiom@L4` (has_level)
- **Exact edge logic:** read loop idiom -&gt; L4 (Extended abstract): the answer reasons beyond the given code (4 ways).

Ways (4), each with its exact rule:

- **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `InputReadOnceBeforeLoop`: The loop works for any input length, including 0 (the body is skipped). With empty input, though, Average's sum / cnt is 0.0/0 = NaN. Moving the read out of the loop breaks it, so one value is reused forever.
- **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Use the read loop when the number of values is unknown and all input should be processed. When N is given first, use a counted for loop (AddInts). Use a sentinel loop when a stop value marks the end.
- **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: Every read needs a preceding isEmpty() check that guarantees a value. Kind: run-time exception. Trigger class: A body that reads more values than remain (two reads per pass with an odd count), or a condition that does not test isEmpty().
- **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: Do not divide by a count of 0. Kind: silent logic error. Trigger class: Empty input: the double average sum / cnt evaluates to NaN instead of stopping (it would be ArithmeticException if both were int).

## Same topic

`read_loop_idiom` belongs to the topic **Standard input** (`topic1.5.c`). The topic also contains: `end_of_input`, `input_format`, `input_validation`, `interactive_input`, `sentinel_loop`, `standard_input`, `token_vs_line_input`.

## Rules of the concept (17)

- **Book** (SW-1e, p. 131 (pdf 141)): "Before reading each number, the program uses the method StdIn.isEmpty() to check whether there are any more numbers in the input stream."
- **Book** (SW-1.5, ): "Our StdIn library takes data from a standard input stream that contains a sequence of values separated by whitespace ... your program consumes values when it reads them."
- **E** (folk-meaning rule): Everyday 'read until the end' assumes you know how long the text is, and 'empty' suggests a blank screen or line. The stream's length is unknown to the program, and isEmpty() is true only when no more tokens remain.
- **M** (wrong rule / right rule): AssignmentNotExpression: wrong: An assignment cannot be used inside a larger expression. \| right: An assignment is an expression whose value is the value assigned, so (x = v) both stores v in x and yields v. This is used, for example, in while ((line = in.readLine()) != null).
- **M** (wrong rule / right rule): InputReadOnceBeforeLoop: wrong: Reading a value once before the loop is enough; the loop will process each new input value. \| right: The read must be inside the loop body so that every pass consumes a new value.
- **T** (uneven-application rule): Points to LT (test !isEmpty(), then read, then process, on every pass). An uneven trace processes the old value before reading on some passes, or reads twice on one pass.
- **N** (identity rule): The read loop is an input idiom: a while loop whose condition is !StdIn.isEmpty() and whose body reads one value and processes it.
- **S** (declarative rule): Before each read, call StdIn.isEmpty() to check whether more values remain. isEmpty() is true when only whitespace is left.
- **LT** (operational sequencing rule): Each pass: evaluate !StdIn.isEmpty(). If it is true, read one value, then process it (e.g. sum += value; cnt++;) and go back to the test. If it is false, leave the loop and run the code after it (e.g. compute and print the average).
- **OP** (evaluation / result rule): After the loop, every value has been read exactly once and the accumulators hold their totals. Average with input 10.0 5.0 6.0 3.0 7.0 32.0 &lt;ctrl-d&gt; prints Average is 10.5.
- **OS** (state-transition rule): One pass consumes exactly one value (or one fixed group, e.g. an x, y pair) and updates the loop's accumulators. The isEmpty() test consumes nothing.
- **R** (composition rule (with a neighbour)): with standard\_input: isEmpty() false guarantees only one more token. A body that reads k values per pass assumes the input count is a multiple of k.
- **R** (composition rule (with a neighbour)): with end\_of\_input: The loop ends only when isEmpty() becomes true: at the end of a redirected file, or after the end-of-file keystroke (&lt;ctrl-d&gt;, or &lt;ctrl-z&gt; on some systems).
- **R** (composition rule (with a neighbour)): with sentinel\_loop: A sentinel loop keeps the read-then-test structure but stops on a special data value instead of, or as well as, isEmpty(). The sentinel must be tested before it is processed.
- **P** (plan / role rule): Plan: the process-all-input loop (Soloway's read/process loop). sum is a gatherer and cnt a counter (stepper), and value is a most-recent holder.
- **C** (conservation rule): The loop works for any input length, including 0 (the body is skipped). With empty input, though, Average's sum / cnt is 0.0/0 = NaN. Moving the read out of the loop breaks it, so one value is reused forever.
- **D** (error rule): rule broken: Every read needs a preceding isEmpty() check that guarantees a value. (run-time exception)
- **D** (error rule): rule broken: Do not divide by a count of 0. (silent logic error)
- **X** (applicability rule): Use the read loop when the number of values is unknown and all input should be processed. When N is given first, use a counted for loop (AddInts). Use a sentinel loop when a stop value marks the end.

## How it is found in code and answers (reader block)

- **Aliases:** none
- **Code patterns:** `while\s*\(\s*!\s*StdIn\.isEmpty\s*\(\s*\)\s*\)`, `while\s*\(\s*\w+\.hasNext\w*\s*\(\s*\)\s*\)`
- **Operator symbols:** none
- **Java types:** none

## The whole prerequisite chain

- **Everything it builds on (2):** `standard_input`, `stream_model`
- **Everything that builds on it (2):** `end_of_input`, `sentinel_loop`

## Every edge in this view and its exact edge logic (25)

All the edges drawn in the picture, in the order: prerequisite, parallel, misconception, error, has_level, contains.

**1. `read_loop_idiom` &rarr; `end_of_input`** (prerequisite)

- **Exact edge logic:** The read loop runs until StdIn.isEmpty() returns true, which happens when the user types the end-of-file sequence (&lt;ctrl-d&gt;).
- **Grounding:** book\_passage
- **Composition rule (R) of `read_loop_idiom` with `end_of_input`:** The loop ends only when isEmpty() becomes true: at the end of a redirected file, or after the end-of-file keystroke (&lt;ctrl-d&gt;, or &lt;ctrl-z&gt; on some systems).
- **Composition rule (R) of `end_of_input` with `read_loop_idiom`:** isEmpty() is the condition of the read loop, so the loop ends exactly when end-of-file is reached (&lt;ctrl-d&gt; at the keyboard, end of file with &lt;).

**2. `read_loop_idiom` &rarr; `sentinel_loop`** (prerequisite)

- **Exact edge logic:** The sentinel loop is a read loop with its own stop value.
- **Grounding:** questionable
- **Composition rule (R) of `read_loop_idiom` with `sentinel_loop`:** A sentinel loop keeps the read-then-test structure but stops on a special data value instead of, or as well as, isEmpty(). The sentinel must be tested before it is processed.
- **Composition rule (R) of `sentinel_loop` with `read_loop_idiom`:** The sentinel test replaces, or is added to, the isEmpty() test. If the sentinel may be missing, keep !StdIn.isEmpty() in the condition so the program does not read past the end.

**3. `standard_input` &rarr; `read_loop_idiom`** (prerequisite)

- **Exact edge logic:** The read loop repeats StdIn reads until StdIn.isEmpty() returns true.
- **Grounding:** book\_passage
- **Composition rule (R) of `standard_input` with `read_loop_idiom`:** To read an unknown number of values, each read must be guarded by !StdIn.isEmpty() as the condition of a while loop whose body reads.
- **Composition rule (R) of `read_loop_idiom` with `standard_input`:** isEmpty() false guarantees only one more token. A body that reads k values per pass assumes the input count is a multiple of k.

**4. `read_loop_idiom` &rarr; `AssignmentNotExpression`** (misconception)

- **Exact edge logic (the wrong rule):** A read and a test cannot be combined, so while ((x = read()) != end) is not allowed.
- **Twin logic (the right rule):** while ((x = read()) != end) reads a value into x and tests that same value in one expression.
- **Role:** context

**5. `read_loop_idiom` &rarr; `InputReadOnceBeforeLoop`** (misconception)

- **Exact edge logic (the wrong rule):** Reading a value once before the loop is enough; the loop will process each new input value.
- **Twin logic (the right rule):** A read loop must read the next value inside the body on every pass; otherwise it keeps processing the same value.
- **Role:** primary

**6. `assignment` &rarr; `AssignmentNotExpression`** (misconception)

- **Exact edge logic (the wrong rule):** An assignment cannot be used inside a larger expression, so a condition like (x = read()) != v is not allowed.
- **Twin logic (the right rule):** An assignment is an expression whose value is the value assigned, so (x = v) both stores v in x and gives v.
- **Role:** primary

**7. `chained_assignment` &rarr; `AssignmentNotExpression`** (misconception)

- **Exact edge logic (the wrong rule):** an assignment cannot be used inside a larger expression
- **Twin logic (the right rule):** An assignment is an expression whose value is the value assigned, so (x = v) both stores v in x and gives v.
- **Role:** context

**8. `expression` &rarr; `AssignmentNotExpression`** (misconception)

- **Exact edge logic (the wrong rule):** An assignment cannot be used inside a larger expression, so a condition like (x = read()) != v is not allowed.
- **Twin logic (the right rule):** An assignment is an expression whose value is the value assigned, so (x = v) both stores v in x and gives v.
- **Role:** context

**9. `standard_input` &rarr; `InputReadOnceBeforeLoop`** (misconception)

- **Exact edge logic (the wrong rule):** Reading a value once before the loop is enough; the loop will process each new input value.
- **Twin logic (the right rule):** A read loop must read the next value inside the body on every pass; otherwise it keeps processing the same value.
- **Role:** context

**10. `read_loop_idiom` &rarr; `ReadPastEndOfInput`** (error)

- **Exact edge logic (the wrong rule):** Calls StdIn.readInt() again after the input has run out.
- **Twin logic (the right rule):** Reading after standard input is exhausted is a run-time error; test StdIn.isEmpty() before each read.
- **Role:** context

**11. `end_of_input` &rarr; `ReadPastEndOfInput`** (error)

- **Exact edge logic (the wrong rule):** Calls StdIn.readInt() again after the input has run out.
- **Twin logic (the right rule):** Reading after standard input is exhausted is a run-time error; test StdIn.isEmpty() before each read.
- **Role:** primary

**12. `standard_input` &rarr; `ReadPastEndOfInput`** (error)

- **Exact edge logic (the wrong rule):** Calls StdIn.readInt() again after the input has run out.
- **Twin logic (the right rule):** Reading after standard input is exhausted is a run-time error; test StdIn.isEmpty() before each read.
- **Role:** context

**13. `read_loop_idiom` &rarr; `read_loop_idiom@L0`** (has_level)

- **Exact edge logic:** read loop idiom -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (4 ways).
  - **[0] everyday\_reading** (rule type E, folk-meaning rule): Everyday 'read until the end' assumes you know how long the text is, and 'empty' suggests a blank screen or line. The stream's length is unknown to the program, and isEmpty() is true only when no more tokens remain.
  - **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `InputReadOnceBeforeLoop`: wrong rule: Reading a value once before the loop is enough; the loop will process each new input value. Right rule: The read must be inside the loop body so that every pass consumes a new value.
  - **[2] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `InputReadOnceBeforeLoop`: Points to LT (test !isEmpty(), then read, then process, on every pass). An uneven trace processes the old value before reading on some passes, or reads twice on one pass. (here mixing in: "Reading a value once before the loop is enough; the loop will process each new input value")
  - **[3] misconception** (rule type M, wrong rule / right rule) &rarr; `AssignmentNotExpression`: wrong rule: An assignment cannot be used inside a larger expression. Right rule: An assignment is an expression whose value is the value assigned, so (x = v) both stores v in x and yields v. This is used, for example, in while ((line = in.readLine()) != null).

**14. `read_loop_idiom` &rarr; `read_loop_idiom@L1`** (has_level)

- **Exact edge logic:** read loop idiom -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).
  - **[0] names\_the\_element** (rule type N, identity rule): The read loop is an input idiom: a while loop whose condition is !StdIn.isEmpty() and whose body reads one value and processes it.
  - **[1] states\_the\_rule** (rule type S, declarative rule): Before each read, call StdIn.isEmpty() to check whether more values remain. isEmpty() is true when only whitespace is left.

**15. `read_loop_idiom` &rarr; `read_loop_idiom@L2`** (has_level)

- **Exact edge logic:** read loop idiom -&gt; L2 (Multistructural): the answer applies the rules of read loop idiom to every part of the code, in order (3 ways).
  - **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): Each pass: evaluate !StdIn.isEmpty(). If it is true, read one value, then process it (e.g. sum += value; cnt++;) and go back to the test. If it is false, leave the loop and run the code after it (e.g. compute and print the average).
  - **[1] output\_prediction** (rule type OP, evaluation / result rule): After the loop, every value has been read exactly once and the accumulators hold their totals. Average with input 10.0 5.0 6.0 3.0 7.0 32.0 &lt;ctrl-d&gt; prints Average is 10.5.
  - **[2] one\_step\_execution** (rule type OS, state-transition rule): One pass consumes exactly one value (or one fixed group, e.g. an x, y pair) and updates the loop's accumulators. The isEmpty() test consumes nothing.

**16. `read_loop_idiom` &rarr; `read_loop_idiom@L3`** (has_level)

- **Exact edge logic:** read loop idiom -&gt; L3 (Relational): the answer relates the parts (4 ways).
  - **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): isEmpty() false guarantees only one more token. A body that reads k values per pass assumes the input count is a multiple of k.
  - **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): The loop ends only when isEmpty() becomes true: at the end of a redirected file, or after the end-of-file keystroke (&lt;ctrl-d&gt;, or &lt;ctrl-z&gt; on some systems).
  - **[2] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): A sentinel loop keeps the read-then-test structure but stops on a special data value instead of, or as well as, isEmpty(). The sentinel must be tested before it is processed.
  - **[3] purpose\_of\_the\_whole** (rule type P, plan / role rule): Plan: the process-all-input loop (Soloway's read/process loop). sum is a gatherer and cnt a counter (stepper), and value is a most-recent holder.

**17. `read_loop_idiom` &rarr; `read_loop_idiom@L4`** (has_level)

- **Exact edge logic:** read loop idiom -&gt; L4 (Extended abstract): the answer reasons beyond the given code (4 ways).
  - **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `InputReadOnceBeforeLoop`: The loop works for any input length, including 0 (the body is skipped). With empty input, though, Average's sum / cnt is 0.0/0 = NaN. Moving the read out of the loop breaks it, so one value is reused forever.
  - **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Use the read loop when the number of values is unknown and all input should be processed. When N is given first, use a counted for loop (AddInts). Use a sentinel loop when a stop value marks the end.
  - **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: Every read needs a preceding isEmpty() check that guarantees a value. Kind: run-time exception. Trigger class: A body that reads more values than remain (two reads per pass with an odd count), or a condition that does not test isEmpty().
  - **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: Do not divide by a count of 0. Kind: silent logic error. Trigger class: Empty input: the double average sum / cnt evaluates to NaN instead of stopping (it would be ArithmeticException if both were int).

**18. `topic1.5.c` &rarr; `read_loop_idiom`** (contains)

- topic `topic1.5.c` contains `read_loop_idiom`

**19. `topic1.5.c` &rarr; `end_of_input`** (contains)

- topic `topic1.5.c` contains `end_of_input`

**20. `topic1.5.c` &rarr; `input_format`** (contains)

- topic `topic1.5.c` contains `input_format`

**21. `topic1.5.c` &rarr; `input_validation`** (contains)

- topic `topic1.5.c` contains `input_validation`

**22. `topic1.5.c` &rarr; `interactive_input`** (contains)

- topic `topic1.5.c` contains `interactive_input`

**23. `topic1.5.c` &rarr; `sentinel_loop`** (contains)

- topic `topic1.5.c` contains `sentinel_loop`

**24. `topic1.5.c` &rarr; `standard_input`** (contains)

- topic `topic1.5.c` contains `standard_input`

**25. `topic1.5.c` &rarr; `token_vs_line_input`** (contains)

- topic `topic1.5.c` contains `token_vs_line_input`
