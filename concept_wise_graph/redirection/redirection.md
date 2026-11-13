# redirection (`redirection`)

&lt; / &gt; send a file in/out as standard input/output

Section 1.5 Input and Output, topic 1.5.d Redirection and piping (filters).

![The knowledge graph around redirection](redirection.png)

## At a glance

- **Needs first:** `run`, `standard_input`, `standard_output`
- **Leads to:** `data_driven_code`, `piping`
- **Learned alongside:** nothing
- **Misconceptions:** `RedirectionIsArgument`
- **Errors:** none
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 17 edges around this concept, each explained in the graph's own words.

## What it needs first (3)

A prerequisite edge means the other concept has to be understood before `redirection`.

### `run` comes before `redirection`

*java executes main in the JVM*

Redirection is written on the command that runs a program, with &lt; or &gt;.

- **Grounding:** book passage

### `standard_input` comes before `redirection`

*StdIn -- reading a stream of values*

&lt; file makes the contents of the file the standard input stream.

- **Grounding:** book passage
- **How `redirection` combines with `standard_input`:** \`&lt; file\` makes the file's contents the standard input stream: the same StdIn calls read the file's tokens in order.
- **How `standard_input` combines with `redirection`:** With \`&lt; file\` the same StdIn calls read from the file instead of the keyboard. The program text does not change.

### `standard_output` comes before `redirection`

*StdOut / System.out*

&gt; file sends everything written to standard output into the file instead of the screen.

- **Grounding:** book passage
- **How `redirection` combines with `standard_output`:** \`&gt; file\` diverts all standard output (print, println, printf) into the file, so nothing appears in the terminal.
- **How `standard_output` combines with `redirection`:** With \`&gt; file\`, every print/println/printf writes to the file and nothing appears in the terminal. The program code is unchanged.

## What it leads to (2)

These concepts need `redirection` first.

### `redirection` comes before `data_driven_code`

*Data-driven code: keeping data in files and writing programs that read it from standard input, so the data can change without changing the program*

Redirecting a file to standard input lets the same program process different data files without being changed.

- **Grounding:** book passage
- **How `redirection` combines with `data_driven_code`:** Redirecting different files into the same program changes the data it processes without changing the program.
- **How `data_driven_code` combines with `redirection`:** Redirecting a different data file to standard input changes what the unchanged program processes.

### `redirection` comes before `piping`

*\| connects one program's output to another's input*

A pipe A \| B connects A's standard output directly to B's standard input, with no file in between.

- **Grounding:** book passage
- **How `redirection` combines with `piping`:** \`A &gt; f\` followed by \`B &lt; f\` has the same effect as \`A \| B\`, except that the pipe creates no file.
- **How `piping` combines with `redirection`:** A pipe has the same effect as \`&gt; file\` then \`&lt; file\`, but there is no intermediate file, so the data size is not limited by disk space.

## Learned alongside (0)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

No parallel edge touches this concept.

## Misconceptions (1)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### RedirectionIsArgument

- **Wrong rule:** java Prog &lt; in.txt puts the name in.txt into args[0].
- **Right rule:** With &lt; data.txt the operating system implements the standard input stream by reading from the file; the program just reads standard input and has no dependence on the source of the input stream.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: A redirected file shows up in args[]. Right rule: With \`&lt; data.txt\` the operating system supplies standard input from the file. args[] does not contain it, and the program just reads standard input whatever the source.
- **Shows at level L0 as:** inconsistent trace: Points to LT (the OS connects the file before the program runs; reads come from the file and writes go only to the file). An uneven trace shows output on the screen as well as in the file, or treats the file name as a command-line argument. (here mixing in: "a redirected file shows up in args[]")
- **Also an edge from `filter`:** a redirected file shows up in args[]
- **Also an edge from `piping`:** a redirected file shows up in args[]

## Errors (0)

An error edge states the rule that gets broken in a program, and the right rule.

The graph has no error edge from this concept.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for redirection: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to redirection agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

redirection -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (3 ways).

- **everyday reading** (folk-meaning rule): In maths \`&lt;\` and \`&gt;\` mean less-than and greater-than. In a command line they are directives to the operating system: \`&lt; file\` makes the file the standard input and \`&gt; file\` sends standard output to the file. They are not part of Java or of args[].
- **misconception** (wrong rule / right rule; shows `RedirectionIsArgument`): wrong rule: A redirected file shows up in args[]. Right rule: With \`&lt; data.txt\` the operating system supplies standard input from the file. args[] does not contain it, and the program just reads standard input whatever the source.
- **inconsistent trace** (uneven-application rule; shows `RedirectionIsArgument`): Points to LT (the OS connects the file before the program runs; reads come from the file and writes go only to the file). An uneven trace shows output on the screen as well as in the file, or treats the file name as a command-line argument. (here mixing in: "a redirected file shows up in args[]")

### L1: Unistructural / atom x text surface

L1 for redirection: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

redirection -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

- **names the element** (identity rule): Redirection is an operating-system (shell) mechanism that connects a program's standard input or standard output to a file.
- **states the rule** (declarative rule): \`java P &gt; data.txt\` writes standard output to data.txt instead of the terminal. \`java P &lt; data.txt\` makes StdIn read from data.txt. The program itself is not changed.

### L2: Multistructural / block x execution / preoperational

L2 for redirection: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

redirection -&gt; L2 (Multistructural): the answer applies the rules of redirection to every part of the code, in order (3 ways).

- **line by line trace** (operational sequencing rule): The shell opens the file and connects it before main starts. Each StdIn read then takes the next value from the file, and each print appends text at the end of the output file.
- **output prediction** (evaluation / result rule): \`java RandomSeq 1000 &gt; data.txt\` prints nothing in the terminal and leaves a file of 1,000 values. \`java Average &lt; data.txt\` prints their average.
- **one step execution** (state-transition rule): Each read or print still does exactly what it does at a terminal; only the source or destination is a file (one print appends to the file).

### L3: Relational / relations x function (concrete operational begins)

L3 for redirection: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

redirection -&gt; L3 (Relational): the answer relates the parts (5 ways).

- **relation to neighbour** (composition rule (with a neighbour)): \`&gt; file\` diverts all standard output (print, println, printf) into the file, so nothing appears in the terminal.
- **relation to neighbour** (composition rule (with a neighbour)): \`&lt; file\` makes the file's contents the standard input stream: the same StdIn calls read the file's tokens in order.
- **relation to neighbour** (composition rule (with a neighbour)): \`A &gt; f\` followed by \`B &lt; f\` has the same effect as \`A \| B\`, except that the pipe creates no file.
- **relation to neighbour** (composition rule (with a neighbour)): Redirecting different files into the same program changes the data it processes without changing the program.
- **purpose of the whole** (plan / role rule): Redirection saves output for later and feeds large amounts of data from files, without typing.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for redirection: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

redirection -&gt; L4 (Extended abstract): the answer reasons beyond the given code (5 ways).

- **predict a change** (conservation rule; shows `RedirectionIsArgument`): The program is unchanged whether its input or output is the terminal or a file: the I/O abstraction is conserved. Changing only the file changes only the data.
- **transfer to a new program** (applicability rule): Use redirection when the data are in a file or the results should be saved. When a program needs several input or output files at once, use In/Out instead (one standard stream each way).
- **diagnose an error** (error rule): rule broken: \`&gt; file\` replaces the file's previous contents. Kind: silent logic error. Trigger class: Redirecting output onto an existing data file (or onto the input file itself) overwrites it.
- **diagnose an error** (error rule): rule broken: The input file must exist and be readable. Kind: launch error. Trigger class: \`java Average &lt; missing.txt\`: the shell reports that the file does not exist, and the program never starts.
- **diagnose an error** (error rule): rule broken: A redirected file is finite. Kind: run-time exception. Trigger class: The program reads more values than the file contains.

## Same topic

`redirection` belongs to the topic **Redirection and piping (filters)** (`topic1.5.d`). The topic also contains: `data_driven_code`, `filter`, `piping`.

## Rules of the concept (18)

- **folk-meaning rule:** In maths \`&lt;\` and \`&gt;\` mean less-than and greater-than. In a command line they are directives to the operating system: \`&lt; file\` makes the file the standard input and \`&gt; file\` sends standard output to the file. They are not part of Java or of args[].
- **wrong rule / right rule:** RedirectionIsArgument: wrong: A redirected file shows up in args[]. \| right: With \`&lt; data.txt\` the operating system supplies standard input from the file. args[] does not contain it, and the program just reads standard input whatever the source.
- **uneven-application rule:** Points to LT (the OS connects the file before the program runs; reads come from the file and writes go only to the file). An uneven trace shows output on the screen as well as in the file, or treats the file name as a command-line argument.
- **identity rule:** Redirection is an operating-system (shell) mechanism that connects a program's standard input or standard output to a file.
- **declarative rule:** \`java P &gt; data.txt\` writes standard output to data.txt instead of the terminal. \`java P &lt; data.txt\` makes StdIn read from data.txt. The program itself is not changed.
- **operational sequencing rule:** The shell opens the file and connects it before main starts. Each StdIn read then takes the next value from the file, and each print appends text at the end of the output file.
- **evaluation / result rule:** \`java RandomSeq 1000 &gt; data.txt\` prints nothing in the terminal and leaves a file of 1,000 values. \`java Average &lt; data.txt\` prints their average.
- **state-transition rule:** Each read or print still does exactly what it does at a terminal; only the source or destination is a file (one print appends to the file).
- **composition rule (with a neighbour):** with standard\_output: \`&gt; file\` diverts all standard output (print, println, printf) into the file, so nothing appears in the terminal.
- **composition rule (with a neighbour):** with standard\_input: \`&lt; file\` makes the file's contents the standard input stream: the same StdIn calls read the file's tokens in order.
- **composition rule (with a neighbour):** with piping: \`A &gt; f\` followed by \`B &lt; f\` has the same effect as \`A \| B\`, except that the pipe creates no file.
- **composition rule (with a neighbour):** with data\_driven\_code: Redirecting different files into the same program changes the data it processes without changing the program.
- **plan / role rule:** Redirection saves output for later and feeds large amounts of data from files, without typing.
- **conservation rule:** The program is unchanged whether its input or output is the terminal or a file: the I/O abstraction is conserved. Changing only the file changes only the data.
- **error rule:** rule broken: \`&gt; file\` replaces the file's previous contents. (silent logic error)
- **error rule:** rule broken: The input file must exist and be readable. (launch error)
- **error rule:** rule broken: A redirected file is finite. (run-time exception)
- **applicability rule:** Use redirection when the data are in a file or the results should be saved. When a program needs several input or output files at once, use In/Out instead (one standard stream each way).

## The whole prerequisite chain

- **Everything it builds on (6):** `compile`, `program_text`, `run`, `standard_input`, `standard_output`, `stream_model`
- **Everything that builds on it (3):** `data_driven_code`, `filter`, `piping`
