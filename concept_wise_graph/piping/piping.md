# piping (`piping`)

\| connects one program's output to another's input

Section 1.5 Input and Output, topic 1.5.d Redirection and piping (filters).

![The knowledge graph around piping](piping.png)

## At a glance

- **Needs first:** `redirection`, `run`
- **Leads to:** `filter`
- **Learned alongside:** nothing
- **Misconceptions:** `RedirectionIsArgument`
- **Errors:** none
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 15 edges around this concept, each explained in the graph's own words.

## What it needs first (2)

A prerequisite edge means the other concept has to be understood before `piping`.

### `redirection` comes before `piping`

*&lt; / &gt; send a file in/out as standard input/output*

A pipe A \| B connects A's standard output directly to B's standard input, with no file in between.

- **Grounding:** book passage
- **How `piping` combines with `redirection`:** A pipe has the same effect as \`&gt; file\` then \`&lt; file\`, but there is no intermediate file, so the data size is not limited by disk space.
- **How `redirection` combines with `piping`:** \`A &gt; f\` followed by \`B &lt; f\` has the same effect as \`A \| B\`, except that the pipe creates no file.

### `run` comes before `piping`

*java executes main in the JVM*

Piping joins the commands that run two programs, so one program's output becomes the other's input.

- **Grounding:** book passage

## What it leads to (1)

These concepts need `piping` first.

### `piping` comes before `filter`

*a program that reads standard input and writes standard output*

A filter converts a standard input stream to a standard output stream, and piping is the mechanism that connects filters together.

- **Grounding:** book passage
- **How `piping` combines with `filter`:** Filters are the components and the pipe is the connector: \`A \| F1 \| F2\` passes the stream through each filter in turn.
- **How `filter` combines with `piping`:** Piping connects filters: the output of one becomes the input of the next, so filters compose into pipelines (\`java RandomSeq 1000 \| more\`).

## Learned alongside (0)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

No parallel edge touches this concept.

## Misconceptions (1)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### RedirectionIsArgument

- **Wrong rule:** a redirected file shows up in args[]
- **Right rule:** With &lt; data.txt the operating system implements the standard input stream by reading from the file; the program just reads standard input and has no dependence on the source of the input stream.
- **Role of this concept:** context
- **Shows at level L0 as:** misconception: wrong rule: A redirected (piped) stream shows up in args[]. Right rule: With \`A \| B\`, B's standard input is A's output stream. It is not an argument, and B just reads standard input as if someone were typing it.
- **Shows at level L0 as:** inconsistent trace: Points to LT (A's writes are added to the end of the shared stream and B's reads take from its front, interleaved by the OS). An uneven trace runs A to completion into a file first, or sends B's output back into A. (here mixing in: "a redirected file shows up in args[]")
- **Also an edge from `filter`:** a redirected file shows up in args[]
- **Also an edge from `redirection`:** java Prog &lt; in.txt puts the name in.txt into args[0].

## Errors (0)

An error edge states the rule that gets broken in a program, and the right rule.

The graph has no error edge from this concept.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for piping: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to piping agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

piping -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (3 ways).

- **everyday reading** (folk-meaning rule): In maths \`\|\` means 'divides', absolute value or 'or'. In a command line, \`A \| B\` connects A's standard output to B's standard input.
- **misconception** (wrong rule / right rule; shows `RedirectionIsArgument`): wrong rule: A redirected (piped) stream shows up in args[]. Right rule: With \`A \| B\`, B's standard input is A's output stream. It is not an argument, and B just reads standard input as if someone were typing it.
- **inconsistent trace** (uneven-application rule; shows `RedirectionIsArgument`): Points to LT (A's writes are added to the end of the shared stream and B's reads take from its front, interleaved by the OS). An uneven trace runs A to completion into a file first, or sends B's output back into A. (here mixing in: "a redirected file shows up in args[]")

### L1: Unistructural / atom x text surface

L1 for piping: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

piping -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

- **names the element** (identity rule): Piping is an operating-system mechanism (\`\|\`) that makes one program's standard output the next program's standard input.
- **states the rule** (declarative rule): \`java RandomSeq 1000 \| java Average\` specifies that RandomSeq's standard output and Average's standard input are the same stream.

### L2: Multistructural / block x execution / preoperational

L2 for piping: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

piping -&gt; L2 (Multistructural): the answer applies the rules of piping to every part of the code, in order (3 ways).

- **line by line trace** (operational sequencing rule): The two programs run together. Each println in A adds a string to the end of the stream, and each read in B removes one from the beginning. The OS decides the interleaving, and the result does not depend on it.
- **output prediction** (evaluation / result rule): Only the last program's standard output appears. \`java RandomSeq 100000 \| java Average\` prints a single line such as Average is 0.5000499417963857.
- **one step execution** (state-transition rule): One write by A makes one more item available to B. One read by B consumes it. No file is created.

### L3: Relational / relations x function (concrete operational begins)

L3 for piping: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

piping -&gt; L3 (Relational): the answer relates the parts (3 ways).

- **relation to neighbour** (composition rule (with a neighbour)): A pipe has the same effect as \`&gt; file\` then \`&lt; file\`, but there is no intermediate file, so the data size is not limited by disk space.
- **relation to neighbour** (composition rule (with a neighbour)): Filters are the components and the pipe is the connector: \`A \| F1 \| F2\` passes the stream through each filter in turn.
- **purpose of the whole** (plan / role rule): Piping composes small programs into a pipeline and removes the limit on stream size.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for piping: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

piping -&gt; L4 (Extended abstract): the answer reasons beyond the given code (3 ways).

- **predict a change** (conservation rule; shows `RedirectionIsArgument`): Replacing \`A \| B\` with \`A &gt; f; B &lt; f\` keeps the result. Changing A's output format (e.g. adding a label) breaks B's typed reads.
- **transfer to a new program** (applicability rule): Use a pipe when one program's output is exactly the next program's input and the intermediate data need not be kept. Use redirection to a file when it must be saved or reused.
- **diagnose an error** (error rule): rule broken: The upstream output must match the downstream input format. Kind: run-time exception. Trigger class: A prints labels such as \`Average is 0.5\`, and B reads them with readDouble(): NumberFormatException on the token \`Average\`.

## Same topic

`piping` belongs to the topic **Redirection and piping (filters)** (`topic1.5.d`). The topic also contains: `data_driven_code`, `filter`, `redirection`.

## Rules of the concept (14)

- **folk-meaning rule:** In maths \`\|\` means 'divides', absolute value or 'or'. In a command line, \`A \| B\` connects A's standard output to B's standard input.
- **wrong rule / right rule:** RedirectionIsArgument: wrong: A redirected (piped) stream shows up in args[]. \| right: With \`A \| B\`, B's standard input is A's output stream. It is not an argument, and B just reads standard input as if someone were typing it.
- **uneven-application rule:** Points to LT (A's writes are added to the end of the shared stream and B's reads take from its front, interleaved by the OS). An uneven trace runs A to completion into a file first, or sends B's output back into A.
- **identity rule:** Piping is an operating-system mechanism (\`\|\`) that makes one program's standard output the next program's standard input.
- **declarative rule:** \`java RandomSeq 1000 \| java Average\` specifies that RandomSeq's standard output and Average's standard input are the same stream.
- **operational sequencing rule:** The two programs run together. Each println in A adds a string to the end of the stream, and each read in B removes one from the beginning. The OS decides the interleaving, and the result does not depend on it.
- **evaluation / result rule:** Only the last program's standard output appears. \`java RandomSeq 100000 \| java Average\` prints a single line such as Average is 0.5000499417963857.
- **state-transition rule:** One write by A makes one more item available to B. One read by B consumes it. No file is created.
- **composition rule (with a neighbour):** with redirection: A pipe has the same effect as \`&gt; file\` then \`&lt; file\`, but there is no intermediate file, so the data size is not limited by disk space.
- **composition rule (with a neighbour):** with filter: Filters are the components and the pipe is the connector: \`A \| F1 \| F2\` passes the stream through each filter in turn.
- **plan / role rule:** Piping composes small programs into a pipeline and removes the limit on stream size.
- **conservation rule:** Replacing \`A \| B\` with \`A &gt; f; B &lt; f\` keeps the result. Changing A's output format (e.g. adding a label) breaks B's typed reads.
- **error rule:** rule broken: The upstream output must match the downstream input format. (run-time exception)
- **applicability rule:** Use a pipe when one program's output is exactly the next program's input and the intermediate data need not be kept. Use redirection to a file when it must be saved or reused.

## The whole prerequisite chain

- **Everything it builds on (7):** `compile`, `program_text`, `redirection`, `run`, `standard_input`, `standard_output`, `stream_model`
- **Everything that builds on it (1):** `filter`
