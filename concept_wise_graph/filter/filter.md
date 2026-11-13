# filter (`filter`)

a program that reads standard input and writes standard output

Section 1.5 Input and Output, topic 1.5.d Redirection and piping (filters).

![The knowledge graph around filter](filter.png)

## At a glance

- **Needs first:** `piping`, `standard_input`
- **Leads to:** nothing
- **Learned alongside:** nothing
- **Misconceptions:** `RedirectionIsArgument`
- **Errors:** `NegativeNotFiltered`
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 17 edges around this concept, each explained in the graph's own words.

## What it needs first (2)

A prerequisite edge means the other concept has to be understood before `filter`.

### `piping` comes before `filter`

*\| connects one program's output to another's input*

A filter converts a standard input stream to a standard output stream, and piping is the mechanism that connects filters together.

- **Grounding:** book passage
- **How `filter` combines with `piping`:** Piping connects filters: the output of one becomes the input of the next, so filters compose into pipelines (\`java RandomSeq 1000 \| more\`).
- **How `piping` combines with `filter`:** Filters are the components and the pipe is the connector: \`A \| F1 \| F2\` passes the stream through each filter in turn.

### `standard_input` comes before `filter`

*StdIn -- reading a stream of values*

A filter reads its data from standard input and writes what it keeps to standard output.

- **Grounding:** book passage

## What it leads to (0)

These concepts need `filter` first.

No concept has this one as a prerequisite.

## Learned alongside (0)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

No parallel edge touches this concept.

## Misconceptions (1)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### RedirectionIsArgument

- **Wrong rule:** a redirected file shows up in args[]
- **Right rule:** With &lt; data.txt the operating system implements the standard input stream by reading from the file; the program just reads standard input and has no dependence on the source of the input stream.
- **Role of this concept:** context
- **Shows at level L0 as:** misconception: wrong rule: The file a filter processes shows up in args[]. Right rule: A filter reads only standard input. The file or upstream program is attached by &lt; or \|, and args[] carries only parameters such as lo and hi.
- **Shows at level L0 as:** inconsistent trace: Points to LT (read one value, test it, maybe print it, repeat). An uneven trace prints out-of-range values on some passes, or holds all the output until the end. (here mixing in: "a redirected file shows up in args[]")
- **Also an edge from `piping`:** a redirected file shows up in args[]
- **Also an edge from `redirection`:** java Prog &lt; in.txt puts the name in.txt into args[0].

## Errors (1)

An error edge states the rule that gets broken in a program, and the right rule.

### NegativeNotFiltered

- **Wrong rule:** Adds negative rainfall values to the total.
- **Right rule:** Values outside the range of interest must be filtered out (for example with if (t &gt;= lo &amp;&amp; t &lt;= hi)) before they are processed.
- **Role of this concept:** context
- **Also an edge from `input_validation`:** Adds negative rainfall values to the total.
- **Also an edge from `sentinel_loop`:** Adds negative rainfall values to the total.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for filter: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to filter agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

filter -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (3 ways).

- **everyday reading** (folk-meaning rule): An everyday filter (a coffee filter) removes things. In the UNIX sense a filter is any program that reads standard input and writes standard output, even one that removes nothing.
- **misconception** (wrong rule / right rule; shows `RedirectionIsArgument`): wrong rule: The file a filter processes shows up in args[]. Right rule: A filter reads only standard input. The file or upstream program is attached by &lt; or \|, and args[] carries only parameters such as lo and hi.
- **inconsistent trace** (uneven-application rule; shows `RedirectionIsArgument`): Points to LT (read one value, test it, maybe print it, repeat). An uneven trace prints out-of-range values on some passes, or holds all the output until the end. (here mixing in: "a redirected file shows up in args[]")

### L1: Unistructural / atom x text surface

L1 for filter: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

filter -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

- **names the element** (identity rule): A filter is a program that converts a standard input stream into a standard output stream.
- **states the rule** (declarative rule): A filter reads from standard input and writes to standard output, classically writing a subsequence of its input (e.g. RangeFilter keeps the values between lo and hi).

### L2: Multistructural / block x execution / preoperational

L2 for filter: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

filter -&gt; L2 (Multistructural): the answer applies the rules of filter to every part of the code, in order (3 ways).

- **line by line trace** (operational sequencing rule): Each pass of while (!StdIn.isEmpty()) reads one value t, tests lo &lt;= t &lt;= hi, and prints t right away if the test passes. Output is produced while input is still being read.
- **output prediction** (evaluation / result rule): \`java RangeFilter 100 400\` with input 358 1330 55 165 689 1014 3066 387 575 843 203 48 292 877 65 998 prints 358 165 387 203 292: the in-range values, in their original order.
- **one step execution** (state-transition rule): One pass reads one value and appends it to the output only if it passes the test. lo and hi do not change.

### L3: Relational / relations x function (concrete operational begins)

L3 for filter: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

filter -&gt; L3 (Relational): the answer relates the parts (2 ways).

- **relation to neighbour** (composition rule (with a neighbour)): Piping connects filters: the output of one becomes the input of the next, so filters compose into pipelines (\`java RandomSeq 1000 \| more\`).
- **purpose of the whole** (plan / role rule): Plan: the stream filter, a one-pass read-test-print loop that uses only a fixed number of variables. The value read is a most-recent holder and lo and hi are fixed values.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for filter: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

filter -&gt; L4 (Extended abstract): the answer reasons beyond the given code (3 ways).

- **predict a change** (conservation rule; shows `RedirectionIsArgument`): A filter keeps the relative order of the values it passes (it outputs a subsequence). Filters can be chained in any number without changing each other.
- **transfer to a new program** (applicability rule): A filter is the right tool when each output depends only on the current value, or on a fixed amount of state. Tasks that need all the values (sorting, k-th smallest, percentage above the mean) must store them in an array first.
- **diagnose an error** (error rule): rule broken: Every value must pass the range test before it is output or processed. Kind: silent logic error. Trigger class: Values outside lo..hi (e.g. negatives) are output because the test is missing or uses the wrong bounds or operators.

## Same topic

`filter` belongs to the topic **Redirection and piping (filters)** (`topic1.5.d`). The topic also contains: `data_driven_code`, `piping`, `redirection`.

## Rules of the concept (13)

- **folk-meaning rule:** An everyday filter (a coffee filter) removes things. In the UNIX sense a filter is any program that reads standard input and writes standard output, even one that removes nothing.
- **wrong rule / right rule:** RedirectionIsArgument: wrong: The file a filter processes shows up in args[]. \| right: A filter reads only standard input. The file or upstream program is attached by &lt; or \|, and args[] carries only parameters such as lo and hi.
- **uneven-application rule:** Points to LT (read one value, test it, maybe print it, repeat). An uneven trace prints out-of-range values on some passes, or holds all the output until the end.
- **identity rule:** A filter is a program that converts a standard input stream into a standard output stream.
- **declarative rule:** A filter reads from standard input and writes to standard output, classically writing a subsequence of its input (e.g. RangeFilter keeps the values between lo and hi).
- **operational sequencing rule:** Each pass of while (!StdIn.isEmpty()) reads one value t, tests lo &lt;= t &lt;= hi, and prints t right away if the test passes. Output is produced while input is still being read.
- **evaluation / result rule:** \`java RangeFilter 100 400\` with input 358 1330 55 165 689 1014 3066 387 575 843 203 48 292 877 65 998 prints 358 165 387 203 292: the in-range values, in their original order.
- **state-transition rule:** One pass reads one value and appends it to the output only if it passes the test. lo and hi do not change.
- **composition rule (with a neighbour):** with piping: Piping connects filters: the output of one becomes the input of the next, so filters compose into pipelines (\`java RandomSeq 1000 \| more\`).
- **plan / role rule:** Plan: the stream filter, a one-pass read-test-print loop that uses only a fixed number of variables. The value read is a most-recent holder and lo and hi are fixed values.
- **conservation rule:** A filter keeps the relative order of the values it passes (it outputs a subsequence). Filters can be chained in any number without changing each other.
- **error rule:** rule broken: Every value must pass the range test before it is output or processed. (silent logic error)
- **applicability rule:** A filter is the right tool when each output depends only on the current value, or on a fixed amount of state. Tasks that need all the values (sorting, k-th smallest, percentage above the mean) must store them in an array first.

## The whole prerequisite chain

- **Everything it builds on (8):** `compile`, `piping`, `program_text`, `redirection`, `run`, `standard_input`, `standard_output`, `stream_model`
- **Everything that builds on it (0):** nothing
