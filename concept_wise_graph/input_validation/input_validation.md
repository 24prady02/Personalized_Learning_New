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

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 21 edges around this concept, each explained in the graph's own words.

## What it needs first (1)

A prerequisite edge means the other concept has to be understood before `input_validation`.

### `input_format` comes before `input_validation`

*StdIn reads whitespace-separated tokens of the expected type*

Validation guards against input-format errors.

- **Grounding:** book passage
- **How `input_validation` combines with `input_format`:** Format errors throw at the read, so the type test must run before it. StdIn has no hasNextInt, so either read a String and parse it, or rely on the file's format.
- **How `input_format` combines with `input_validation`:** A token in the wrong format makes a read throw, so validation must check before reading (e.g. Scanner.hasNextDouble) or read a String and test it.

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

- **Wrong rule:** StdIn.readInt() accepts any typed text such as abc or 12.2.
- **Right rule:** If the next token is not an int (e.g. abc, 12.2, true), StdIn.readInt() throws a NumberFormatException at run time (Scanner.nextInt throws InputMismatchException).
- **Role of this concept:** context
- **Also an edge from `input_format`:** StdIn.readInt() accepts any typed text such as abc or 12.2.
- **Also an edge from `run_time_error`:** StdIn.readInt() accepts any typed text such as abc or 12.2.
- **Also an edge from `standard_input`:** StdIn.readInt() accepts any typed text such as abc or 12.2.

### NegativeNotFiltered

- **Wrong rule:** Adds negative rainfall values to the total.
- **Right rule:** Values outside the range of interest must be filtered out (for example with if (t &gt;= lo &amp;&amp; t &lt;= hi)) before they are processed.
- **Role of this concept:** context
- **Also an edge from `filter`:** Adds negative rainfall values to the total.
- **Also an edge from `sentinel_loop`:** Adds negative rainfall values to the total.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for input validation: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to input validation agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

input validation -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (1 way).

- **everyday reading** (folk-meaning rule): In everyday checking, something is checked after it has been accepted and stored. Novices place the check after the assignment. In code, the check must come before the value is read or stored, or a bad token has already thrown or polluted the data.

### L1: Unistructural / atom x text surface

L1 for input validation: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

input validation -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

- **names the element** (identity rule): Input validation is guard code that checks that input is available, well-formed and in range before the program uses it (StdIn.isEmpty(), Scanner.hasNextDouble(), range tests).
- **states the rule** (declarative rule): Test before reading: StdIn.isEmpty() tells whether more input is available, and hasNextDouble() tells whether the next token can be read as a double. If the test fails, report the error or prompt again instead of reading.

### L2: Multistructural / block x execution / preoperational

L2 for input validation: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

input validation -&gt; L2 (Multistructural): the answer applies the rules of input validation to every part of the code, in order (3 ways).

- **line by line trace** (operational sequencing rule): Order: availability check, then type check, then read, then range check, then use. On failure, skip or re-prompt (a while loop when the number of wrong tries is unknown).
- **output prediction** (evaluation / result rule): The checks return booleans. A validated program prints an error message, or prompts again, on bad input instead of crashing with an exception.
- **one step execution** (state-transition rule): A check (isEmpty, hasNextDouble) consumes nothing. Only the read that follows, or an explicit in.next() that discards a bad token, advances the stream.

### L3: Relational / relations x function (concrete operational begins)

L3 for input validation: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

input validation -&gt; L3 (Relational): the answer relates the parts (2 ways).

- **relation to neighbour** (composition rule (with a neighbour)): Format errors throw at the read, so the type test must run before it. StdIn has no hasNextInt, so either read a String and parse it, or rely on the file's format.
- **purpose of the whole** (plan / role rule): Role: a guard. Plan: the input-validation (re-prompt) loop, which keeps asking until the value is acceptable.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for input validation: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

input validation -&gt; L4 (Extended abstract): the answer reasons beyond the given code (4 ways).

- **predict a change** (conservation rule): Adding validation leaves the output for valid input unchanged and changes behaviour only for invalid input.
- **transfer to a new program** (applicability rule): Validate at the boundary where external data (users, files) enter the program, especially in interactive programs, where every possible input must be planned for. It is unnecessary for values the program itself generated.
- **diagnose an error** (error rule): rule broken: Check the token type before reading it as a number. Kind: run-time exception. Trigger class: Non-numeric or wrongly typed tokens (abc, 12.2 for an int) reach readInt()/nextInt().
- **diagnose an error** (error rule): rule broken: Values outside the valid range must be filtered out before use. Kind: silent logic error. Trigger class: Out-of-range data (negative rainfall, values outside lo..hi) are processed because no range test comes before the update.

## Same topic

`input_validation` belongs to the topic **Standard input** (`topic1.5.c`). The topic also contains: `end_of_input`, `input_format`, `interactive_input`, `read_loop_idiom`, `sentinel_loop`, `standard_input`, `token_vs_line_input`.

## Rules of the concept (13)

- **folk-meaning rule:** In everyday checking, something is checked after it has been accepted and stored. Novices place the check after the assignment. In code, the check must come before the value is read or stored, or a bad token has already thrown or polluted the data.
- **uneven-application rule:** Points to LT (test first, then read or store). An uneven trace reads or stores the value before checking on some passes.
- **identity rule:** Input validation is guard code that checks that input is available, well-formed and in range before the program uses it (StdIn.isEmpty(), Scanner.hasNextDouble(), range tests).
- **declarative rule:** Test before reading: StdIn.isEmpty() tells whether more input is available, and hasNextDouble() tells whether the next token can be read as a double. If the test fails, report the error or prompt again instead of reading.
- **operational sequencing rule:** Order: availability check, then type check, then read, then range check, then use. On failure, skip or re-prompt (a while loop when the number of wrong tries is unknown).
- **evaluation / result rule:** The checks return booleans. A validated program prints an error message, or prompts again, on bad input instead of crashing with an exception.
- **state-transition rule:** A check (isEmpty, hasNextDouble) consumes nothing. Only the read that follows, or an explicit in.next() that discards a bad token, advances the stream.
- **composition rule (with a neighbour):** with input\_format: Format errors throw at the read, so the type test must run before it. StdIn has no hasNextInt, so either read a String and parse it, or rely on the file's format.
- **plan / role rule:** Role: a guard. Plan: the input-validation (re-prompt) loop, which keeps asking until the value is acceptable.
- **conservation rule:** Adding validation leaves the output for valid input unchanged and changes behaviour only for invalid input.
- **error rule:** rule broken: Check the token type before reading it as a number. (run-time exception)
- **error rule:** rule broken: Values outside the valid range must be filtered out before use. (silent logic error)
- **applicability rule:** Validate at the boundary where external data (users, files) enter the program, especially in interactive programs, where every possible input must be planned for. It is unnecessary for values the program itself generated.

## The whole prerequisite chain

- **Everything it builds on (3):** `input_format`, `standard_input`, `stream_model`
- **Everything that builds on it (0):** nothing
