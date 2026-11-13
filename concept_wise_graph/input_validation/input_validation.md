# input_validation (`input_validation`)

checking the next input before reading it

Section 1.5 Input and Output, topic 1.5.c Standard input.

![The knowledge graph around input_validation](input_validation.png)

## At a glance

- **Needs first:** `input_format`
- **Leads to:** nothing
- **Learned alongside:** nothing
- **Misconceptions:** none
- **Errors:** `InputTypeMismatch`, `NegativeNotFiltered`
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 21 edges around this concept. The edge logic, the wrong and right rules and the exact rules of the ways are copied word for word from the graph.

## To work on (1)

- no aliases: a student's words cannot name this concept

## What it needs first (1)

A prerequisite edge means the other concept has to be understood before `input_validation`.

### `input_format` comes before `input_validation`

*StdIn reads whitespace-separated tokens of the expected type*

- **Edge:** `pre:input_format->input_validation`
- **Exact edge logic:** Validation guards against input-format errors.
- **Grounding:** book\_passage
- **Composition rule (R) of `input_validation` with `input_format`:** Format errors throw at the read, so the type test must run before it. StdIn has no hasNextInt, so either read a String and parse it, or rely on the file's format.
- **Composition rule (R) of `input_format` with `input_validation`:** A token in the wrong format makes a read throw, so validation must check before reading (e.g. Scanner.hasNextDouble) or read a String and test it.

## What it leads to (0)

These concepts need `input_validation` first.

No concept has this one as a prerequisite.

## Learned alongside (0)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

No parallel edge touches this concept.

## Misconceptions (0)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

The graph has no misconception edge from this concept.

## Errors (2)

An error edge states the rule that gets broken in a program, and the right rule.

### InputTypeMismatch

- **Edge:** `input_validation` &rarr; `InputTypeMismatch` (error)
- **Exact edge logic (the wrong rule):** StdIn.readInt() accepts any typed text such as abc or 12.2.
- **Twin logic (the right rule):** If the next token is not an int (e.g. abc, 12.2, true), StdIn.readInt() throws a NumberFormatException at run time (Scanner.nextInt throws InputMismatchException).
- **Wrong belief (on the node):** StdIn.readInt() accepts any typed text such as abc or 12.2.
- **Correct rule (on the node):** If the next token is not an int (e.g. abc, 12.2, true), StdIn.readInt() throws a NumberFormatException at run time (Scanner.nextInt throws InputMismatchException).
- **Provenance:** textbook
- **Role of this concept:** context
- **Edge `input_format` &rarr; `InputTypeMismatch`, exact edge logic:** StdIn.readInt() accepts any typed text such as abc or 12.2. **Twin logic:** If the next token is not an int (e.g. abc, 12.2, true), StdIn.readInt() throws a NumberFormatException at run time (Scanner.nextInt throws InputMismatchException). (role: primary)
- **Edge `run_time_error` &rarr; `InputTypeMismatch`, exact edge logic:** StdIn.readInt() accepts any typed text such as abc or 12.2. **Twin logic:** If the next token is not an int (e.g. abc, 12.2, true), StdIn.readInt() throws a NumberFormatException at run time (Scanner.nextInt throws InputMismatchException). (role: context)
- **Edge `standard_input` &rarr; `InputTypeMismatch`, exact edge logic:** StdIn.readInt() accepts any typed text such as abc or 12.2. **Twin logic:** If the next token is not an int (e.g. abc, 12.2, true), StdIn.readInt() throws a NumberFormatException at run time (Scanner.nextInt throws InputMismatchException). (role: context)

### NegativeNotFiltered

- **Edge:** `input_validation` &rarr; `NegativeNotFiltered` (error)
- **Exact edge logic (the wrong rule):** Adds negative rainfall values to the total.
- **Twin logic (the right rule):** Values outside the range of interest must be filtered out (for example with if (t &gt;= lo &amp;&amp; t &lt;= hi)) before they are processed.
- **Wrong belief (on the node):** Adds negative rainfall values to the total.
- **Correct rule (on the node):** Values outside the range of interest must be filtered out (for example with if (t &gt;= lo &amp;&amp; t &lt;= hi)) before they are processed.
- **Provenance:** published
- **Role of this concept:** context
- **Edge `filter` &rarr; `NegativeNotFiltered`, exact edge logic:** Adds negative rainfall values to the total. **Twin logic:** Values outside the range of interest must be filtered out (for example with if (t &gt;= lo &amp;&amp; t &lt;= hi)) before they are processed. (role: context)
- **Edge `sentinel_loop` &rarr; `NegativeNotFiltered`, exact edge logic:** Adds negative rainfall values to the total. **Twin logic:** Values outside the range of interest must be filtered out (for example with if (t &gt;= lo &amp;&amp; t &lt;= hi)) before they are processed. (role: primary)

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for input validation: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to input validation agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

- **Edge:** `input_validation` &rarr; `input_validation@L0` (has_level)
- **Exact edge logic:** input validation -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (1 way).

Ways (1), each with its exact rule:

- **[0] everyday\_reading** (rule type E, folk-meaning rule): In everyday checking, something is checked after it has been accepted and stored. Novices place the check after the assignment. In code, the check must come before the value is read or stored, or a bad token has already thrown or polluted the data.

### L1: Unistructural / atom x text surface

L1 for input validation: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

- **Edge:** `input_validation` &rarr; `input_validation@L1` (has_level)
- **Exact edge logic:** input validation -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

Ways (2), each with its exact rule:

- **[0] names\_the\_element** (rule type N, identity rule): Input validation is guard code that checks that input is available, well-formed and in range before the program uses it (StdIn.isEmpty(), Scanner.hasNextDouble(), range tests).
- **[1] states\_the\_rule** (rule type S, declarative rule): Test before reading: StdIn.isEmpty() tells whether more input is available, and hasNextDouble() tells whether the next token can be read as a double. If the test fails, report the error or prompt again instead of reading.

### L2: Multistructural / block x execution / preoperational

L2 for input validation: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

- **Edge:** `input_validation` &rarr; `input_validation@L2` (has_level)
- **Exact edge logic:** input validation -&gt; L2 (Multistructural): the answer applies the rules of input validation to every part of the code, in order (3 ways).

Ways (3), each with its exact rule:

- **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): Order: availability check, then type check, then read, then range check, then use. On failure, skip or re-prompt (a while loop when the number of wrong tries is unknown).
- **[1] output\_prediction** (rule type OP, evaluation / result rule): The checks return booleans. A validated program prints an error message, or prompts again, on bad input instead of crashing with an exception.
- **[2] one\_step\_execution** (rule type OS, state-transition rule): A check (isEmpty, hasNextDouble) consumes nothing. Only the read that follows, or an explicit in.next() that discards a bad token, advances the stream.

### L3: Relational / relations x function (concrete operational begins)

L3 for input validation: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

- **Edge:** `input_validation` &rarr; `input_validation@L3` (has_level)
- **Exact edge logic:** input validation -&gt; L3 (Relational): the answer relates the parts (2 ways).

Ways (2), each with its exact rule:

- **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Format errors throw at the read, so the type test must run before it. StdIn has no hasNextInt, so either read a String and parse it, or rely on the file's format.
- **[1] purpose\_of\_the\_whole** (rule type P, plan / role rule): Role: a guard. Plan: the input-validation (re-prompt) loop, which keeps asking until the value is acceptable.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for input validation: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

- **Edge:** `input_validation` &rarr; `input_validation@L4` (has_level)
- **Exact edge logic:** input validation -&gt; L4 (Extended abstract): the answer reasons beyond the given code (4 ways).

Ways (4), each with its exact rule:

- **[0] predict\_a\_change** (rule type C, conservation rule): Adding validation leaves the output for valid input unchanged and changes behaviour only for invalid input.
- **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Validate at the boundary where external data (users, files) enter the program, especially in interactive programs, where every possible input must be planned for. It is unnecessary for values the program itself generated.
- **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: Check the token type before reading it as a number. Kind: run-time exception. Trigger class: Non-numeric or wrongly typed tokens (abc, 12.2 for an int) reach readInt()/nextInt().
- **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: Values outside the valid range must be filtered out before use. Kind: silent logic error. Trigger class: Out-of-range data (negative rainfall, values outside lo..hi) are processed because no range test comes before the update.

## Same topic

`input_validation` belongs to the topic **Standard input** (`topic1.5.c`). The topic also contains: `end_of_input`, `input_format`, `interactive_input`, `read_loop_idiom`, `sentinel_loop`, `standard_input`, `token_vs_line_input`.

## Rules of the concept (13)

- **Book** (SW-1e, p. 152 (pdf 162)): "StdIn.isEmpty() allows you to avoid such an error by checking whether there is more input available."
- **Book** (TJ-2e, p. 82 (pdf 104)): "The Scanner class provides hasNextDouble, which checks whether the next input can be interpreted as a double."
- **Book** (RS, ): "Scanner Lookahead"
- **E** (folk-meaning rule): In everyday checking, something is checked after it has been accepted and stored. Novices place the check after the assignment. In code, the check must come before the value is read or stored, or a bad token has already thrown or polluted the data.
- **T** (uneven-application rule): Points to LT (test first, then read or store). An uneven trace reads or stores the value before checking on some passes.
- **N** (identity rule): Input validation is guard code that checks that input is available, well-formed and in range before the program uses it (StdIn.isEmpty(), Scanner.hasNextDouble(), range tests).
- **S** (declarative rule): Test before reading: StdIn.isEmpty() tells whether more input is available, and hasNextDouble() tells whether the next token can be read as a double. If the test fails, report the error or prompt again instead of reading.
- **LT** (operational sequencing rule): Order: availability check, then type check, then read, then range check, then use. On failure, skip or re-prompt (a while loop when the number of wrong tries is unknown).
- **OP** (evaluation / result rule): The checks return booleans. A validated program prints an error message, or prompts again, on bad input instead of crashing with an exception.
- **OS** (state-transition rule): A check (isEmpty, hasNextDouble) consumes nothing. Only the read that follows, or an explicit in.next() that discards a bad token, advances the stream.
- **R** (composition rule (with a neighbour)): with input\_format: Format errors throw at the read, so the type test must run before it. StdIn has no hasNextInt, so either read a String and parse it, or rely on the file's format.
- **P** (plan / role rule): Role: a guard. Plan: the input-validation (re-prompt) loop, which keeps asking until the value is acceptable.
- **C** (conservation rule): Adding validation leaves the output for valid input unchanged and changes behaviour only for invalid input.
- **D** (error rule): rule broken: Check the token type before reading it as a number. (run-time exception)
- **D** (error rule): rule broken: Values outside the valid range must be filtered out before use. (silent logic error)
- **X** (applicability rule): Validate at the boundary where external data (users, files) enter the program, especially in interactive programs, where every possible input must be planned for. It is unnecessary for values the program itself generated.

## How it is found in code and answers (reader block)

- **Aliases:** none
- **Code patterns:** `if\s*\(\s*!?\s*(?:StdIn\.(?:isEmpty|hasNext\w*)|\w+\.hasNext\w*)\s*\(`, `\bif\s*\(\s*args\.length\s*(?:[<>!=]=?)`
- **Operator symbols:** none
- **Java types:** none

## The whole prerequisite chain

- **Everything it builds on (3):** `input_format`, `standard_input`, `stream_model`
- **Everything that builds on it (0):** nothing

## Every edge in this view and its exact edge logic (21)

All the edges drawn in the picture, in the order: prerequisite, parallel, misconception, error, has_level, contains.

**1. `input_format` &rarr; `input_validation`** (prerequisite)

- **Exact edge logic:** Validation guards against input-format errors.
- **Grounding:** book\_passage
- **Composition rule (R) of `input_format` with `input_validation`:** A token in the wrong format makes a read throw, so validation must check before reading (e.g. Scanner.hasNextDouble) or read a String and test it.
- **Composition rule (R) of `input_validation` with `input_format`:** Format errors throw at the read, so the type test must run before it. StdIn has no hasNextInt, so either read a String and parse it, or rely on the file's format.

**2. `input_validation` &rarr; `InputTypeMismatch`** (error)

- **Exact edge logic (the wrong rule):** StdIn.readInt() accepts any typed text such as abc or 12.2.
- **Twin logic (the right rule):** If the next token is not an int (e.g. abc, 12.2, true), StdIn.readInt() throws a NumberFormatException at run time (Scanner.nextInt throws InputMismatchException).
- **Role:** context

**3. `input_validation` &rarr; `NegativeNotFiltered`** (error)

- **Exact edge logic (the wrong rule):** Adds negative rainfall values to the total.
- **Twin logic (the right rule):** Values outside the range of interest must be filtered out (for example with if (t &gt;= lo &amp;&amp; t &lt;= hi)) before they are processed.
- **Role:** context

**4. `filter` &rarr; `NegativeNotFiltered`** (error)

- **Exact edge logic (the wrong rule):** Adds negative rainfall values to the total.
- **Twin logic (the right rule):** Values outside the range of interest must be filtered out (for example with if (t &gt;= lo &amp;&amp; t &lt;= hi)) before they are processed.
- **Role:** context

**5. `input_format` &rarr; `InputTypeMismatch`** (error)

- **Exact edge logic (the wrong rule):** StdIn.readInt() accepts any typed text such as abc or 12.2.
- **Twin logic (the right rule):** If the next token is not an int (e.g. abc, 12.2, true), StdIn.readInt() throws a NumberFormatException at run time (Scanner.nextInt throws InputMismatchException).
- **Role:** primary

**6. `run_time_error` &rarr; `InputTypeMismatch`** (error)

- **Exact edge logic (the wrong rule):** StdIn.readInt() accepts any typed text such as abc or 12.2.
- **Twin logic (the right rule):** If the next token is not an int (e.g. abc, 12.2, true), StdIn.readInt() throws a NumberFormatException at run time (Scanner.nextInt throws InputMismatchException).
- **Role:** context

**7. `sentinel_loop` &rarr; `NegativeNotFiltered`** (error)

- **Exact edge logic (the wrong rule):** Adds negative rainfall values to the total.
- **Twin logic (the right rule):** Values outside the range of interest must be filtered out (for example with if (t &gt;= lo &amp;&amp; t &lt;= hi)) before they are processed.
- **Role:** primary

**8. `standard_input` &rarr; `InputTypeMismatch`** (error)

- **Exact edge logic (the wrong rule):** StdIn.readInt() accepts any typed text such as abc or 12.2.
- **Twin logic (the right rule):** If the next token is not an int (e.g. abc, 12.2, true), StdIn.readInt() throws a NumberFormatException at run time (Scanner.nextInt throws InputMismatchException).
- **Role:** context

**9. `input_validation` &rarr; `input_validation@L0`** (has_level)

- **Exact edge logic:** input validation -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (1 way).
  - **[0] everyday\_reading** (rule type E, folk-meaning rule): In everyday checking, something is checked after it has been accepted and stored. Novices place the check after the assignment. In code, the check must come before the value is read or stored, or a bad token has already thrown or polluted the data.

**10. `input_validation` &rarr; `input_validation@L1`** (has_level)

- **Exact edge logic:** input validation -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).
  - **[0] names\_the\_element** (rule type N, identity rule): Input validation is guard code that checks that input is available, well-formed and in range before the program uses it (StdIn.isEmpty(), Scanner.hasNextDouble(), range tests).
  - **[1] states\_the\_rule** (rule type S, declarative rule): Test before reading: StdIn.isEmpty() tells whether more input is available, and hasNextDouble() tells whether the next token can be read as a double. If the test fails, report the error or prompt again instead of reading.

**11. `input_validation` &rarr; `input_validation@L2`** (has_level)

- **Exact edge logic:** input validation -&gt; L2 (Multistructural): the answer applies the rules of input validation to every part of the code, in order (3 ways).
  - **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): Order: availability check, then type check, then read, then range check, then use. On failure, skip or re-prompt (a while loop when the number of wrong tries is unknown).
  - **[1] output\_prediction** (rule type OP, evaluation / result rule): The checks return booleans. A validated program prints an error message, or prompts again, on bad input instead of crashing with an exception.
  - **[2] one\_step\_execution** (rule type OS, state-transition rule): A check (isEmpty, hasNextDouble) consumes nothing. Only the read that follows, or an explicit in.next() that discards a bad token, advances the stream.

**12. `input_validation` &rarr; `input_validation@L3`** (has_level)

- **Exact edge logic:** input validation -&gt; L3 (Relational): the answer relates the parts (2 ways).
  - **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Format errors throw at the read, so the type test must run before it. StdIn has no hasNextInt, so either read a String and parse it, or rely on the file's format.
  - **[1] purpose\_of\_the\_whole** (rule type P, plan / role rule): Role: a guard. Plan: the input-validation (re-prompt) loop, which keeps asking until the value is acceptable.

**13. `input_validation` &rarr; `input_validation@L4`** (has_level)

- **Exact edge logic:** input validation -&gt; L4 (Extended abstract): the answer reasons beyond the given code (4 ways).
  - **[0] predict\_a\_change** (rule type C, conservation rule): Adding validation leaves the output for valid input unchanged and changes behaviour only for invalid input.
  - **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Validate at the boundary where external data (users, files) enter the program, especially in interactive programs, where every possible input must be planned for. It is unnecessary for values the program itself generated.
  - **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: Check the token type before reading it as a number. Kind: run-time exception. Trigger class: Non-numeric or wrongly typed tokens (abc, 12.2 for an int) reach readInt()/nextInt().
  - **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: Values outside the valid range must be filtered out before use. Kind: silent logic error. Trigger class: Out-of-range data (negative rainfall, values outside lo..hi) are processed because no range test comes before the update.

**14. `topic1.5.c` &rarr; `input_validation`** (contains)

- topic `topic1.5.c` contains `input_validation`

**15. `topic1.5.c` &rarr; `end_of_input`** (contains)

- topic `topic1.5.c` contains `end_of_input`

**16. `topic1.5.c` &rarr; `input_format`** (contains)

- topic `topic1.5.c` contains `input_format`

**17. `topic1.5.c` &rarr; `interactive_input`** (contains)

- topic `topic1.5.c` contains `interactive_input`

**18. `topic1.5.c` &rarr; `read_loop_idiom`** (contains)

- topic `topic1.5.c` contains `read_loop_idiom`

**19. `topic1.5.c` &rarr; `sentinel_loop`** (contains)

- topic `topic1.5.c` contains `sentinel_loop`

**20. `topic1.5.c` &rarr; `standard_input`** (contains)

- topic `topic1.5.c` contains `standard_input`

**21. `topic1.5.c` &rarr; `token_vs_line_input`** (contains)

- topic `topic1.5.c` contains `token_vs_line_input`
