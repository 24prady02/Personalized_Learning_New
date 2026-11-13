# standard_input (`standard_input`)

StdIn -- reading a stream of values

Section 1.5 Input and Output, topic 1.5.c Standard input.

![The knowledge graph around standard_input](standard_input.png)

## At a glance

- **Needs first:** `stream_model`
- **Leads to:** `filter`, `input_format`, `input_graph`, `interactive_input`, `read_loop_idiom`, `redirection`, `token_vs_line_input`
- **Learned alongside:** `command_line_args`, `standard_drawing`, `standard_output`
- **Misconceptions:** `InputReadOnceBeforeLoop`, `NextLineAfterNextInt`, `RereadIntoVariableInvalid`, `StdInRereads`
- **Errors:** `InputTypeMismatch`, `ReadPastEndOfInput`, `StdLibraryNotInDirectory`
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 42 edges around this concept, each explained in the graph's own words.

## What it needs first (1)

A prerequisite edge means the other concept has to be understood before `standard_input`.

### `stream_model` comes before `standard_input`

*input and output as sequential streams*

StdIn reads a stream: values arrive in order and each value is consumed once.

- **Grounding:** book passage
- **How `standard_input` combines with `stream_model`:** Every StdIn call takes from the same stream position, so values are delivered once, in order.
- **How `stream_model` combines with `standard_input`:** All StdIn calls in a program share one input position. A read before a loop and reads inside the loop therefore take successive values, never the same one.

## What it leads to (7)

These concepts need `standard_input` first.

### `standard_input` comes before `filter`

*a program that reads standard input and writes standard output*

A filter reads its data from standard input and writes what it keeps to standard output.

- **Grounding:** book passage

### `standard_input` comes before `input_format`

*StdIn reads whitespace-separated tokens of the expected type*

Input format rules apply to every StdIn read.

- **Grounding:** book passage
- **How `standard_input` combines with `input_format`:** The method called fixes the type the next token must have: readInt needs an int literal, and readDouble accepts 5 or 5.0.
- **How `input_format` combines with `standard_input`:** Every StdIn read applies these format rules. The type of the method called decides which tokens are legal.

### `standard_input` comes before `input_graph`

*read the page links from input*

The graph is read from standard input: first the number of pages n, then the link pairs i j.

- **Grounding:** book passage
- **How `standard_input` combines with `input_graph`:** The reads must follow the file's layout: one readInt() for n first, then pairs of readInt() for each link i j until isEmpty().
- **How `input_graph` combines with `standard_input`:** The graph is consumed through StdIn as whitespace-separated tokens: readInt() for N, then a !StdIn.isEmpty() loop reading pairs; each value is consumed once, so the read order fixes which number is N, which is i and which is j.

### `standard_input` comes before `interactive_input`

*the user's input can change the program's control flow while it runs*

Standard input can be read at any time while the program runs, so the user can type values that change its control flow during execution.

- **Grounding:** book passage
- **How `standard_input` combines with `interactive_input`:** Because a read can run at any point in execution, a read inside a loop lets each typed value decide the next branch.
- **How `interactive_input` combines with `standard_input`:** Because a StdIn read can run at any point, a read placed inside the game loop lets each reply choose the branch taken in that round.

### `standard_input` comes before `read_loop_idiom`

*reading until end-of-input*

The read loop repeats StdIn reads until StdIn.isEmpty() returns true.

- **Grounding:** book passage
- **How `standard_input` combines with `read_loop_idiom`:** To read an unknown number of values, each read must be guarded by !StdIn.isEmpty() as the condition of a while loop whose body reads.
- **How `read_loop_idiom` combines with `standard_input`:** isEmpty() false guarantees only one more token. A body that reads k values per pass assumes the input count is a multiple of k.

### `standard_input` comes before `redirection`

*&lt; / &gt; send a file in/out as standard input/output*

&lt; file makes the contents of the file the standard input stream.

- **Grounding:** book passage
- **How `standard_input` combines with `redirection`:** With \`&lt; file\` the same StdIn calls read from the file instead of the keyboard. The program text does not change.
- **How `redirection` combines with `standard_input`:** \`&lt; file\` makes the file's contents the standard input stream: the same StdIn calls read the file's tokens in order.

### `standard_input` comes before `token_vs_line_input`

*reading tokens (readInt) versus whole lines (readLine)*

They are standard-input operations.

- **Grounding:** book passage
- **How `standard_input` combines with `token_vs_line_input`:** Token reads (readInt, readString) and line reads (readLine) share one position. A token read leaves the rest of its line for the next readLine, so it is best not to mix the two.
- **How `token_vs_line_input` combines with `standard_input`:** Both kinds of call share the single StdIn position, so a token read changes what the next readLine returns. Mixing them needs care.

## Learned alongside (3)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

### `standard_input` alongside `command_line_args`

*args[] -- strings passed at launch*

Command-line arguments are a fixed number of strings given once when the program starts (args[]); standard input is a stream of any length read while the program runs (StdIn.readInt()). Both arrive as text and must be parsed into numbers.

- **Grounding:** book passage

### `standard_input` alongside `standard_drawing`

*StdDraw -- graphical output (book-specific)*

Like StdIn, StdDraw is a library downloaded from the booksite; StdIn brings values into the program, while StdDraw produces drawings as output.

- **Grounding:** book passage
- **How `standard_input` combines with `standard_drawing`:** StdIn values can drive StdDraw output. PlotFilter reads x, y pairs and draws a point for each, after scaling from the first four numbers.
- **How `standard_drawing` combines with `standard_input`:** StdIn values can be drawn directly: PlotFilter reads the bounding box, then point coordinates, and calls StdDraw.point for each pair. Both libraries must be downloaded into the program's directory.

### `standard_input` alongside `standard_output`

*StdOut / System.out*

StdIn takes values in from the input stream; StdOut sends values out to the output stream.

- **Grounding:** book passage
- **How `standard_input` combines with `standard_output`:** The program turns the input stream into the output stream: values read with StdIn are processed and the results are written with StdOut. The two streams are independent.
- **How `standard_output` combines with `standard_input`:** A prompt printed with print (not println) shows on the same line where the user then types, before the following StdIn read blocks. Output and input are separate streams.

## Misconceptions (4)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### InputReadOnceBeforeLoop

- **Wrong rule:** Reading a value once before the loop is enough; the loop will process each new input value.
- **Right rule:** A read loop must read the next value inside the body on every pass; otherwise it keeps processing the same value.
- **Role of this concept:** context
- **Shows at level L0 as:** misconception: wrong rule: Reading a value once before the loop is enough; the loop will process each new input value. Right rule: A loop must call a read inside its body on every pass. A single read before the loop gives one value, which is processed over and over.
- **Also an edge from `read_loop_idiom`:** Reading a value once before the loop is enough; the loop will process each new input value.

### NextLineAfterNextInt

- **Wrong rule:** A line read after a number read returns the next line typed.
- **Right rule:** The number read leaves the newline, so the line read returns "" unless the newline is consumed first.
- **Role of this concept:** context
- **Shows at level L0 as:** misconception: wrong rule: A line read after a number read returns the next line typed. Right rule: readInt() stops right after the number and leaves the rest of that line, including the line separator. A following readLine() returns that rest (often ""), not the next line.
- **Also an edge from `token_vs_line_input`:** A line read after a number read returns the next line typed.

### RereadIntoVariableInvalid

- **Wrong rule:** Reading a second input value into a variable that already holds one is an error, so the program cannot run.
- **Right rule:** A later read simply overwrites the variable's current value.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: Reading a second input value into a variable that already holds one is an error, so the program cannot run. Right rule: A later read assigns a new value, which overwrites the old one. y = StdIn.readInt(); y = StdIn.readInt(); is legal, and y keeps the second value.
- **Also an edge from `variable`:** Reading a second input value into a variable that already holds one is an error, so the program cannot run.

### StdInRereads

- **Wrong rule:** Calling StdIn.readInt() twice returns the same value twice.
- **Right rule:** The program consumes values when it reads them, so each call returns the next value.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: Calling StdIn.readInt() twice returns the same value twice. Right rule: Each read consumes its value, so the second call returns the next value.
- **Shows at level L0 as:** inconsistent trace: Points to LT (each call blocks, then consumes exactly one token, in order). An uneven trace gives a variable a value that was already consumed, skips a token on some reads, or merges two READs into one. (here mixing in: "Calling StdIn.readInt() twice returns the same value twice")
- **Also an edge from `stream_model`:** Calling StdIn.readInt() twice returns the same value twice.

## Errors (3)

An error edge states the rule that gets broken in a program, and the right rule.

### InputTypeMismatch

- **Wrong rule:** StdIn.readInt() accepts any typed text such as abc or 12.2.
- **Right rule:** If the next token is not an int (e.g. abc, 12.2, true), StdIn.readInt() throws a NumberFormatException at run time (Scanner.nextInt throws InputMismatchException).
- **Role of this concept:** context
- **Also an edge from `input_format`:** StdIn.readInt() accepts any typed text such as abc or 12.2.
- **Also an edge from `input_validation`:** StdIn.readInt() accepts any typed text such as abc or 12.2.
- **Also an edge from `run_time_error`:** StdIn.readInt() accepts any typed text such as abc or 12.2.

### ReadPastEndOfInput

- **Wrong rule:** Calls StdIn.readInt() again after the input has run out.
- **Right rule:** Reading after standard input is exhausted is a run-time error; test StdIn.isEmpty() before each read.
- **Role of this concept:** context
- **Also an edge from `end_of_input`:** Calls StdIn.readInt() again after the input has run out.
- **Also an edge from `read_loop_idiom`:** Calls StdIn.readInt() again after the input has run out.

### StdLibraryNotInDirectory

- **Wrong rule:** Uses StdIn (or StdDraw/StdAudio) without StdIn.java in the working directory.
- **Right rule:** The Std\* libraries are not built into Java; StdIn.java etc. must be in the same directory (or on the classpath), otherwise Java reports NoClassDefFoundError.
- **Role of this concept:** primary
- **Also an edge from `standard_audio`:** Uses StdIn (or StdDraw/StdAudio) without StdIn.java in the working directory.
- **Also an edge from `standard_drawing`:** Uses StdIn (or StdDraw/StdAudio) without StdIn.java in the working directory.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for standard input: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to standard input agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

standard input -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (6 ways).

- **everyday reading** (folk-meaning rule): In everyday reading of \`INPUT A\` or \`readInt\`, the command looks like it inputs the letter A, or 'looks at' a number without using it up. In fact a read takes the next token from the input stream, converts it, and returns the value, which the program must store (e.g. int a = StdIn.readInt()).
- **misconception** (wrong rule / right rule; shows `StdInRereads`): wrong rule: Calling StdIn.readInt() twice returns the same value twice. Right rule: Each read consumes its value, so the second call returns the next value.
- **misconception** (wrong rule / right rule; shows `RereadIntoVariableInvalid`): wrong rule: Reading a second input value into a variable that already holds one is an error, so the program cannot run. Right rule: A later read assigns a new value, which overwrites the old one. y = StdIn.readInt(); y = StdIn.readInt(); is legal, and y keeps the second value.
- **inconsistent trace** (uneven-application rule; shows `StdInRereads`): Points to LT (each call blocks, then consumes exactly one token, in order). An uneven trace gives a variable a value that was already consumed, skips a token on some reads, or merges two READs into one. (here mixing in: "Calling StdIn.readInt() twice returns the same value twice")
- **misconception** (wrong rule / right rule; shows `NextLineAfterNextInt`): wrong rule: A line read after a number read returns the next line typed. Right rule: readInt() stops right after the number and leaves the rest of that line, including the line separator. A following readLine() returns that rest (often ""), not the next line.
- **misconception** (wrong rule / right rule; shows `InputReadOnceBeforeLoop`): wrong rule: Reading a value once before the loop is enough; the loop will process each new input value. Right rule: A loop must call a read inside its body on every pass. A single read before the loop gives one value, which is processed over and over.

### L1: Unistructural / atom x text surface

L1 for standard input: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

standard input -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

- **names the element** (identity rule): StdIn is a booksite library of static methods that read typed values from the standard input stream: isEmpty, readInt, readDouble, readLong, readBoolean, readChar, readString, readLine, readAll.
- **states the rule** (declarative rule): StdIn reads from a stream that may be empty or may contain values separated by whitespace. readInt() reads the next token, parses it as an int and returns it, and the token must have the type the method expects. Outside the book's StdIn library, standard Java reads keyboard input with java.util.Scanner (nextInt(), nextDouble(), nextLine()); a token of the wrong type stops the program with InputMismatchException.

### L2: Multistructural / block x execution / preoperational

L2 for standard input: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

standard input -&gt; L2 (Multistructural): the answer applies the rules of standard input to every part of the code, in order (3 ways).

- **line by line trace** (operational sequencing rule): When execution reaches a read, the program blocks until a complete token is available (at the terminal, until &lt;return&gt;). The read then parses the token and returns, the assignment stores the value, and the next statement runs.
- **output prediction** (evaluation / result rule): readInt returns an int, readDouble a double, readString a String, readBoolean a boolean. AddInts 4 with input 144 233 377 1024 prints Sum is 1778.
- **one step execution** (state-transition rule): One read moves the input position past one token and returns its value. Assigning that value overwrites the variable's previous value. No other variable changes.

### L3: Relational / relations x function (concrete operational begins)

L3 for standard input: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

standard input -&gt; L3 (Relational): the answer relates the parts (11 ways).

- **relation to neighbour** (composition rule (with a neighbour)): Every StdIn call takes from the same stream position, so values are delivered once, in order.
- **relation to neighbour** (composition rule (with a neighbour)): To read an unknown number of values, each read must be guarded by !StdIn.isEmpty() as the condition of a while loop whose body reads.
- **relation to neighbour** (composition rule (with a neighbour)): With \`&lt; file\` the same StdIn calls read from the file instead of the keyboard. The program text does not change.
- **relation to neighbour** (composition rule (with a neighbour)): The reads must follow the file's layout: one readInt() for n first, then pairs of readInt() for each link i j until isEmpty().
- **relation to neighbour** (composition rule (with a neighbour)): The program turns the input stream into the output stream: values read with StdIn are processed and the results are written with StdOut. The two streams are independent.
- **relation to neighbour** (composition rule (with a neighbour)): StdIn values can drive StdDraw output. PlotFilter reads x, y pairs and draws a point for each, after scaling from the first four numbers.
- **relation to neighbour** (composition rule (with a neighbour)): The method called fixes the type the next token must have: readInt needs an int literal, and readDouble accepts 5 or 5.0.
- **relation to neighbour** (composition rule (with a neighbour)): Because a read can run at any point in execution, a read inside a loop lets each typed value decide the next branch.
- **relation to neighbour** (composition rule (with a neighbour)): Token reads (readInt, readString) and line reads (readLine) share one position. A token read leaves the rest of its line for the next readLine, so it is best not to mix the two.
- **relation to neighbour** (composition rule (with a neighbour)): Command-line arguments are a fixed number of strings given once when the program starts (args[]); standard input is a stream of any length read while the program runs (StdIn.readInt()). Both arrive as text and must be parsed into numbers.
- **purpose of the whole** (plan / role rule): StdIn brings an unbounded amount of data into a running program. The variable that receives each read plays the Sajaniemi role of most-recent holder.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for standard input: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

standard input -&gt; L4 (Extended abstract): the answer reasons beyond the given code (5 ways).

- **predict a change** (conservation rule; shows `StdInRereads`): Changing the input data changes the results without recompiling. Swapping two reads swaps the values the two variables get. Changing readInt to readDouble accepts more inputs; the reverse breaks on tokens like 12.2.
- **diagnose an error** (error rule): rule broken: StdIn/StdOut/StdDraw/StdAudio are not part of Java; their files must be in the working directory or on the classpath. Kind: run-time exception. Trigger class: StdIn.class is absent when the program runs: java.lang.NoClassDefFoundError: StdIn. If StdIn.java is absent when compiling, javac reports 'cannot find symbol' instead.
- **transfer to a new program** (applicability rule): Use StdIn when the amount of data is large or unknown, comes from a file or another program, or must be supplied while the program runs. Use command-line arguments for a few parameters fixed at launch.
- **diagnose an error** (error rule): rule broken: The next token must parse as the requested type. Kind: run-time exception. Trigger class: The next token is not an int literal, e.g. abc, 12.2 or true for readInt(). StdIn throws NumberFormatException in the book's version and InputMismatchException in the booksite/Scanner version.
- **diagnose an error** (error rule): rule broken: A read requires a remaining value; test StdIn.isEmpty() first. Kind: run-time exception. Trigger class: More reads than values: a fixed-count loop with too few inputs, or an unguarded read after EOF.

## Same topic

`standard_input` belongs to the topic **Standard input** (`topic1.5.c`). The topic also contains: `end_of_input`, `input_format`, `input_validation`, `interactive_input`, `read_loop_idiom`, `sentinel_loop`, `token_vs_line_input`.

## Rules of the concept (26)

- **folk-meaning rule:** In everyday reading of \`INPUT A\` or \`readInt\`, the command looks like it inputs the letter A, or 'looks at' a number without using it up. In fact a read takes the next token from the input stream, converts it, and returns the value, which the program must store (e.g. int a = StdIn.readInt()).
- **wrong rule / right rule:** NextLineAfterNextInt: wrong: A line read after a number read returns the next line typed. \| right: readInt() stops right after the number and leaves the rest of that line, including the line separator. A following readLine() returns that rest (often ""), not the next line.
- **wrong rule / right rule:** StdInRereads: wrong: Calling StdIn.readInt() twice returns the same value twice. \| right: Each read consumes its value, so the second call returns the next value.
- **wrong rule / right rule:** RereadIntoVariableInvalid: wrong: Reading a second input value into a variable that already holds one is an error, so the program cannot run. \| right: A later read assigns a new value, which overwrites the old one. y = StdIn.readInt(); y = StdIn.readInt(); is legal, and y keeps the second value.
- **wrong rule / right rule:** InputReadOnceBeforeLoop: wrong: Reading a value once before the loop is enough; the loop will process each new input value. \| right: A loop must call a read inside its body on every pass. A single read before the loop gives one value, which is processed over and over.
- **uneven-application rule:** Points to LT (each call blocks, then consumes exactly one token, in order). An uneven trace gives a variable a value that was already consumed, skips a token on some reads, or merges two READs into one.
- **identity rule:** StdIn is a booksite library of static methods that read typed values from the standard input stream: isEmpty, readInt, readDouble, readLong, readBoolean, readChar, readString, readLine, readAll.
- **declarative rule:** StdIn reads from a stream that may be empty or may contain values separated by whitespace. readInt() reads the next token, parses it as an int and returns it, and the token must have the type the method expects. Outside the book's StdIn library, standard Java reads keyboard input with java.util.Scanner (nextInt(), nextDouble(), nextLine()); a token of the wrong type stops the program with InputMismatchException.
- **operational sequencing rule:** When execution reaches a read, the program blocks until a complete token is available (at the terminal, until &lt;return&gt;). The read then parses the token and returns, the assignment stores the value, and the next statement runs.
- **evaluation / result rule:** readInt returns an int, readDouble a double, readString a String, readBoolean a boolean. AddInts 4 with input 144 233 377 1024 prints Sum is 1778.
- **state-transition rule:** One read moves the input position past one token and returns its value. Assigning that value overwrites the variable's previous value. No other variable changes.
- **composition rule (with a neighbour):** with stream\_model: Every StdIn call takes from the same stream position, so values are delivered once, in order.
- **composition rule (with a neighbour):** with read\_loop\_idiom: To read an unknown number of values, each read must be guarded by !StdIn.isEmpty() as the condition of a while loop whose body reads.
- **composition rule (with a neighbour):** with redirection: With \`&lt; file\` the same StdIn calls read from the file instead of the keyboard. The program text does not change.
- **composition rule (with a neighbour):** with input\_graph: The reads must follow the file's layout: one readInt() for n first, then pairs of readInt() for each link i j until isEmpty().
- **composition rule (with a neighbour):** with standard\_output: The program turns the input stream into the output stream: values read with StdIn are processed and the results are written with StdOut. The two streams are independent.
- **composition rule (with a neighbour):** with standard\_drawing: StdIn values can drive StdDraw output. PlotFilter reads x, y pairs and draws a point for each, after scaling from the first four numbers.
- **composition rule (with a neighbour):** with input\_format: The method called fixes the type the next token must have: readInt needs an int literal, and readDouble accepts 5 or 5.0.
- **composition rule (with a neighbour):** with interactive\_input: Because a read can run at any point in execution, a read inside a loop lets each typed value decide the next branch.
- **composition rule (with a neighbour):** with token\_vs\_line\_input: Token reads (readInt, readString) and line reads (readLine) share one position. A token read leaves the rest of its line for the next readLine, so it is best not to mix the two.
- **plan / role rule:** StdIn brings an unbounded amount of data into a running program. The variable that receives each read plays the Sajaniemi role of most-recent holder.
- **conservation rule:** Changing the input data changes the results without recompiling. Swapping two reads swaps the values the two variables get. Changing readInt to readDouble accepts more inputs; the reverse breaks on tokens like 12.2.
- **error rule:** rule broken: The next token must parse as the requested type. (run-time exception)
- **error rule:** rule broken: A read requires a remaining value; test StdIn.isEmpty() first. (run-time exception)
- **error rule:** rule broken: StdIn/StdOut/StdDraw/StdAudio are not part of Java; their files must be in the working directory or on the classpath. (run-time exception)
- **applicability rule:** Use StdIn when the amount of data is large or unknown, comes from a file or another program, or must be supplied while the program runs. Use command-line arguments for a few parameters fixed at launch.

## The whole prerequisite chain

- **Everything it builds on (1):** `stream_model`
- **Everything that builds on it (22):** `convergence_rate`, `dangling_pages`, `data_driven_code`, `end_of_input`, `filter`, `frequency_counting`, `input_format`, `input_graph`, `input_validation`, `interactive_input`, `markov_chain`, `normalization`, `piping`, `power_method`, `random_move`, `read_loop_idiom`, `redirection`, `sentinel_loop`, `simulation_loop`, `token_vs_line_input`, `transition_matrix`, `two_models`
