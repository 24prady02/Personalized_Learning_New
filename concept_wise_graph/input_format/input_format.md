# input_format (`input_format`)

StdIn reads whitespace-separated tokens of the expected type

Section 1.5 Input and Output, topic 1.5.c Standard input.

![The knowledge graph around input_format](input_format.png)

## At a glance

- **Needs first:** `standard_input`
- **Leads to:** `input_validation`
- **Learned alongside:** nothing
- **Misconceptions:** none
- **Errors:** `InputTypeMismatch`
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 19 edges around this concept, each explained in the graph's own words.

## What it needs first (1)

A prerequisite edge means the other concept has to be understood before `input_format`.

### `standard_input` comes before `input_format`

*StdIn -- reading a stream of values*

Input format rules apply to every StdIn read.

- **Grounding:** book passage
- **How `input_format` combines with `standard_input`:** Every StdIn read applies these format rules. The type of the method called decides which tokens are legal.
- **How `standard_input` combines with `input_format`:** The method called fixes the type the next token must have: readInt needs an int literal, and readDouble accepts 5 or 5.0.

## What it leads to (1)

These concepts need `input_format` first.

### `input_format` comes before `input_validation`

*checking the next input before reading it*

Validation guards against input-format errors.

- **Grounding:** book passage
- **How `input_format` combines with `input_validation`:** A token in the wrong format makes a read throw, so validation must check before reading (e.g. Scanner.hasNextDouble) or read a String and test it.
- **How `input_validation` combines with `input_format`:** Format errors throw at the read, so the type test must run before it. StdIn has no hasNextInt, so either read a String and parse it, or rely on the file's format.

## Learned alongside (0)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

No parallel edge touches this concept.

## Misconceptions (0)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

The graph has no misconception edge from this concept.

## Errors (1)

An error edge states the rule that gets broken in a program, and the right rule.

### InputTypeMismatch

- **Wrong rule:** StdIn.readInt() accepts any typed text such as abc or 12.2.
- **Right rule:** If the next token is not an int (e.g. abc, 12.2, true), StdIn.readInt() throws a NumberFormatException at run time (Scanner.nextInt throws InputMismatchException).
- **Role of this concept:** primary
- **Also an edge from `input_validation`:** StdIn.readInt() accepts any typed text such as abc or 12.2.
- **Also an edge from `run_time_error`:** StdIn.readInt() accepts any typed text such as abc or 12.2.
- **Also an edge from `standard_input`:** StdIn.readInt() accepts any typed text such as abc or 12.2.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for input format: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to input format agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

input format -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (1 way).

- **everyday reading** (folk-meaning rule): In everyday writing, layout carries meaning: one value per line, '1,000' with a comma, '12.' as a number. To StdIn, any run of whitespace is one separator, a token is a maximal run of non-whitespace, and it must be written as a Java literal of the expected type.

### L1: Unistructural / atom x text surface

L1 for input format: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

input format -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

- **names the element** (identity rule): Input format is the contract for the text on standard input: whitespace-separated tokens, each one a literal of the type the program asks for next.
- **states the rule** (declarative rule): StdIn treats consecutive whitespace (spaces, tabs, newlines) as one space. Whenever the program expects a value of a type, the next token must be a value of that type.

### L2: Multistructural / block x execution / preoperational

L2 for input format: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

input format -&gt; L2 (Multistructural): the answer applies the rules of input format to every part of the code, in order (3 ways).

- **line by line trace** (operational sequencing rule): For each token read, leading whitespace is skipped, then the maximal non-whitespace run is taken and parsed. At a terminal, characters reach the program only a whole line at a time, after &lt;return&gt;.
- **output prediction** (evaluation / result rule): The input \`  144\n\t233 \` gives readInt() 144, then 233. readDouble() on \`5\` gives 5.0. readInt() on \`12.2\` throws.
- **one step execution** (state-transition rule): One token read consumes the leading whitespace and one token, and leaves the whitespace after it.

### L3: Relational / relations x function (concrete operational begins)

L3 for input format: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

input format -&gt; L3 (Relational): the answer relates the parts (3 ways).

- **relation to neighbour** (composition rule (with a neighbour)): Every StdIn read applies these format rules. The type of the method called decides which tokens are legal.
- **relation to neighbour** (composition rule (with a neighbour)): A token in the wrong format makes a read throw, so validation must check before reading (e.g. Scanner.hasNextDouble) or read a String and test it.
- **purpose of the whole** (plan / role rule): A shared format convention lets independently produced data files feed a program. PlotFilter, for example, expects the first four numbers to be the bounding box.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for input format: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

input format -&gt; L4 (Extended abstract): the answer reasons beyond the given code (3 ways).

- **predict a change** (conservation rule): Reformatting whitespace (spaces to newlines, extra blanks, tabs) keeps every read's result. Changing a token's form (5 to 5.0, or adding a comma) can break readInt.
- **diagnose an error** (error rule): rule broken: The next token must be a literal of the requested type. Kind: run-time exception. Trigger class: Tokens like abc, 12.2, true or 1,000 when readInt() is called.
- **transfer to a new program** (applicability rule): Whitespace-token format suits numeric data and single-word strings. When values contain spaces, or the line structure matters, use readLine.

## Same topic

`input_format` belongs to the topic **Standard input** (`topic1.5.c`). The topic also contains: `end_of_input`, `input_validation`, `interactive_input`, `read_loop_idiom`, `sentinel_loop`, `standard_input`, `token_vs_line_input`.

## Rules of the concept (13)

- **folk-meaning rule:** In everyday writing, layout carries meaning: one value per line, '1,000' with a comma, '12.' as a number. To StdIn, any run of whitespace is one separator, a token is a maximal run of non-whitespace, and it must be written as a Java literal of the expected type.
- **uneven-application rule:** Points to LT (skip whitespace, take one maximal token, parse it). An uneven trace treats a line break or extra blanks as an empty value on some reads, or splits one token in two.
- **identity rule:** Input format is the contract for the text on standard input: whitespace-separated tokens, each one a literal of the type the program asks for next.
- **declarative rule:** StdIn treats consecutive whitespace (spaces, tabs, newlines) as one space. Whenever the program expects a value of a type, the next token must be a value of that type.
- **operational sequencing rule:** For each token read, leading whitespace is skipped, then the maximal non-whitespace run is taken and parsed. At a terminal, characters reach the program only a whole line at a time, after &lt;return&gt;.
- **evaluation / result rule:** The input \`  144\n\t233 \` gives readInt() 144, then 233. readDouble() on \`5\` gives 5.0. readInt() on \`12.2\` throws.
- **state-transition rule:** One token read consumes the leading whitespace and one token, and leaves the whitespace after it.
- **composition rule (with a neighbour):** with standard\_input: Every StdIn read applies these format rules. The type of the method called decides which tokens are legal.
- **composition rule (with a neighbour):** with input\_validation: A token in the wrong format makes a read throw, so validation must check before reading (e.g. Scanner.hasNextDouble) or read a String and test it.
- **plan / role rule:** A shared format convention lets independently produced data files feed a program. PlotFilter, for example, expects the first four numbers to be the bounding box.
- **conservation rule:** Reformatting whitespace (spaces to newlines, extra blanks, tabs) keeps every read's result. Changing a token's form (5 to 5.0, or adding a comma) can break readInt.
- **error rule:** rule broken: The next token must be a literal of the requested type. (run-time exception)
- **applicability rule:** Whitespace-token format suits numeric data and single-word strings. When values contain spaces, or the line structure matters, use readLine.

## The whole prerequisite chain

- **Everything it builds on (2):** `standard_input`, `stream_model`
- **Everything that builds on it (1):** `input_validation`
