# standard_output (`standard_output`)

StdOut / System.out

Section 1.5 Input and Output, topic 1.5.b Standard output and formatted printing.

![The knowledge graph around standard_output](standard_output.png)

## At a glance

- **Needs first:** `stream_model`
- **Leads to:** `formatted_output`, `redirection`
- **Learned alongside:** `standard_drawing`, `standard_input`
- **Misconceptions:** `PrintEqualsPrintln`, `PrintfAddsNewline`, `RepeatedOutputVariablePrintedOnce`
- **Errors:** none
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 18 edges around this concept, each explained in the graph's own words.

## What it needs first (1)

A prerequisite edge means the other concept has to be understood before `standard_output`.

### `stream_model` comes before `standard_output`

*input and output as sequential streams*

StdOut writes a stream: each print appends its text to the end of the output.

- **Grounding:** book passage
- **How `standard_output` combines with `stream_model`:** Each output call appends to the end of the single output stream, so the order of output is the order of execution.
- **How `stream_model` combines with `standard_output`:** All StdOut/System.out calls write to one output stream in execution order, and text already written cannot be taken back.

## What it leads to (2)

These concepts need `standard_output` first.

### `standard_output` comes before `formatted_output`

*printf with a format string such as %d, %.2f, %s*

printf writes to standard output, like print, but formats each value first.

- **Grounding:** book passage
- **How `standard_output` combines with `formatted_output`:** printf writes to the same stream as print and println, so mixed calls appear in call order. Unlike println, printf ends a line only when the format contains \n.
- **How `formatted_output` combines with `standard_output`:** printf output goes into the same stream as print/println and lands at the point in the stream where it was called. It does not end the line.

### `standard_output` comes before `redirection`

*&lt; / &gt; send a file in/out as standard input/output*

&gt; file sends everything written to standard output into the file instead of the screen.

- **Grounding:** book passage
- **How `standard_output` combines with `redirection`:** With \`&gt; file\`, every print/println/printf writes to the file and nothing appears in the terminal. The program code is unchanged.
- **How `redirection` combines with `standard_output`:** \`&gt; file\` diverts all standard output (print, println, printf) into the file, so nothing appears in the terminal.

## Learned alongside (2)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

### `standard_output` alongside `standard_drawing`

*StdDraw -- graphical output (book-specific)*

StdOut writes text to the output stream; StdDraw draws shapes at (x, y) coordinates in a window.

- **Grounding:** book passage
- **How `standard_output` combines with `standard_drawing`:** StdOut text and StdDraw pictures are independent outputs: printing does not draw, and drawing does not print.
- **How `standard_drawing` combines with `standard_output`:** StdOut writes text to a stream, while StdDraw draws in a separate window at (x, y) coordinates. Neither affects the other.

### `standard_output` alongside `standard_input`

*StdIn -- reading a stream of values*

StdIn takes values in from the input stream; StdOut sends values out to the output stream.

- **Grounding:** book passage
- **How `standard_output` combines with `standard_input`:** A prompt printed with print (not println) shows on the same line where the user then types, before the following StdIn read blocks. Output and input are separate streams.
- **How `standard_input` combines with `standard_output`:** The program turns the input stream into the output stream: values read with StdIn are processed and the results are written with StdOut. The two streams are independent.

## Misconceptions (3)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### PrintEqualsPrintln

- **Wrong rule:** print and println behave the same (no newline difference)
- **Right rule:** println ends the line after printing and print does not, so print(s1); print(s2); puts s1 and s2 on the same line.
- **Role of this concept:** context
- **Shows at level L0 as:** misconception: wrong rule: print and println behave the same (no newline difference). Right rule: println(s) prints s and then ends the line, but print(s) does not, so print("a"); print("b"); gives ab on one line.
- **Shows at level L0 as:** inconsistent trace: Points to LT (output appears in the order the output calls execute, with a line break only after println). An uneven trace drops a repeated value, puts output lines out of order, or adds line breaks after print on some calls. (here mixing in: "print and println behave the same (no newline difference)")
- **Also an edge from `println`:** print and println do the same thing, so print(s1); print(s2); puts s1 and s2 on separate lines.

### PrintfAddsNewline

- **Wrong rule:** printf() ends the line like println().
- **Right rule:** printf() does not add a newline; put \n in the format string to end the line.
- **Role of this concept:** context
- **Shows at level L0 as:** misconception: wrong rule: printf() ends the line like println(). Right rule: printf() adds no newline. Put \n (or %n) in the format string to end the line.
- **Also an edge from `formatted_output`:** printf() ends the line like println().

### RepeatedOutputVariablePrintedOnce

- **Wrong rule:** An output statement that names the same variable twice (WRITE y, x, y) prints it only once.
- **Right rule:** Each expression in the output list is printed, so a repeated variable prints its value each time.
- **Role of this concept:** context
- **Shows at level L0 as:** misconception: wrong rule: An output statement that names the same variable twice (WRITE y, x, y) prints it only once. Right rule: Every expression in the output is printed, so System.out.println(y + " " + x + " " + y) with x=6, y=9 prints 9 6 9.
- **Also an edge from `print`:** An output statement that names the same variable twice (WRITE y, x, y) prints it only once.

## Errors (0)

An error edge states the rule that gets broken in a program, and the right rule.

The graph has no error edge from this concept.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for standard output: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to standard output agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

standard output -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (5 ways).

- **everyday reading** (folk-meaning rule): Novices take output text literally, as if it acted on the program: printing "The value of X is 1" is read as setting X to 1. They also take 'print' to mean producing a finished line. In Java, print only appends characters to the output stream; it changes no variables and ends the line only for println.
- **misconception** (wrong rule / right rule; shows `PrintEqualsPrintln`): wrong rule: print and println behave the same (no newline difference). Right rule: println(s) prints s and then ends the line, but print(s) does not, so print("a"); print("b"); gives ab on one line.
- **inconsistent trace** (uneven-application rule; shows `PrintEqualsPrintln`): Points to LT (output appears in the order the output calls execute, with a line break only after println). An uneven trace drops a repeated value, puts output lines out of order, or adds line breaks after print on some calls. (here mixing in: "print and println behave the same (no newline difference)")
- **misconception** (wrong rule / right rule; shows `PrintfAddsNewline`): wrong rule: printf() ends the line like println(). Right rule: printf() adds no newline. Put \n (or %n) in the format string to end the line.
- **misconception** (wrong rule / right rule; shows `RepeatedOutputVariablePrintedOnce`): wrong rule: An output statement that names the same variable twice (WRITE y, x, y) prints it only once. Right rule: Every expression in the output is printed, so System.out.println(y + " " + x + " " + y) with x=6, y=9 prints 9 6 9.

### L1: Unistructural / atom x text surface

L1 for standard output: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

standard output -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

- **names the element** (identity rule): Standard output (System.out, StdOut) is the library abstraction for a program's text output: an output stream of characters written by print, println and printf.
- **states the rule** (declarative rule): print(s) writes s. println(s) writes s and then the line separator. println() only ends the line. A null String prints as "null". By default the stream goes to the terminal window.

### L2: Multistructural / block x execution / preoperational

L2 for standard output: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

standard output -&gt; L2 (Multistructural): the answer applies the rules of standard output to every part of the code, in order (3 ways).

- **line by line trace** (operational sequencing rule): First the argument expression is evaluated, e.g. the concatenation "Sum is " + sum. Then its string form is appended, and println appends the line separator after it. Successive calls appear in execution order.
- **output prediction** (evaluation / result rule): The output is the argument's string form. System.out.println(Math.PI) prints 3.141592653589793 (all digits), and println("Sum is " + 1778) prints Sum is 1778 followed by a newline. The methods return void.
- **one step execution** (state-transition rule): One call appends text to the output (println also appends the line separator). It changes no variables and returns nothing.

### L3: Relational / relations x function (concrete operational begins)

L3 for standard output: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

standard output -&gt; L3 (Relational): the answer relates the parts (6 ways).

- **relation to neighbour** (composition rule (with a neighbour)): Each output call appends to the end of the single output stream, so the order of output is the order of execution.
- **relation to neighbour** (composition rule (with a neighbour)): With \`&gt; file\`, every print/println/printf writes to the file and nothing appears in the terminal. The program code is unchanged.
- **relation to neighbour** (composition rule (with a neighbour)): A prompt printed with print (not println) shows on the same line where the user then types, before the following StdIn read blocks. Output and input are separate streams.
- **relation to neighbour** (composition rule (with a neighbour)): StdOut text and StdDraw pictures are independent outputs: printing does not draw, and drawing does not print.
- **relation to neighbour** (composition rule (with a neighbour)): printf writes to the same stream as print and println, so mixed calls appear in call order. Unlike println, printf ends a line only when the format contains \n.
- **purpose of the whole** (plan / role rule): Standard output reports results (to a person, or to a file or program further down the line). Plan: an 'output' step after a computation, or one println per item inside a loop to list values.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for standard output: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

standard output -&gt; L4 (Extended abstract): the answer reasons beyond the given code (5 ways).

- **predict a change** (conservation rule; shows `PrintEqualsPrintln`): Switching System.out.print/println to StdOut.print/println keeps the output. Changing println to print keeps every character but removes the line break, so lines join.
- **transfer to a new program** (applicability rule): Use standard output for text results meant for a reader or for the next program in a pipeline. Use printf when digits or column widths matter, and StdDraw/StdAudio for pictures and sound.
- **diagnose an error** (error rule): rule broken: Output order and line breaks follow the order of the calls and the print/println choice. Kind: silent logic error. Trigger class: Output statements in the wrong order, or a missing println, so text fragments run together (e.g. the next prompt ends up on the same line).
- **diagnose an error** (error rule): rule broken: PrintStream methods never throw IOException; a write failure only sets an internal flag. Kind: silent logic error. Trigger class: Output to a closed or failing destination: nothing is reported unless checkError() is called.
- **diagnose an error** (error rule): rule broken: println/print take a single argument; pieces must be joined with +. Kind: compile-time. Trigger class: Calls like System.out.println("x =", x) with a comma-separated argument list: 'no suitable method found'.

## Same topic

`standard_output` belongs to the topic **Standard output and formatted printing** (`topic1.5.b`). The topic also contains: `formatted_output`.

## Rules of the concept (21)

- **folk-meaning rule:** Novices take output text literally, as if it acted on the program: printing "The value of X is 1" is read as setting X to 1. They also take 'print' to mean producing a finished line. In Java, print only appends characters to the output stream; it changes no variables and ends the line only for println.
- **wrong rule / right rule:** PrintEqualsPrintln: wrong: print and println behave the same (no newline difference). \| right: println(s) prints s and then ends the line, but print(s) does not, so print("a"); print("b"); gives ab on one line.
- **wrong rule / right rule:** PrintfAddsNewline: wrong: printf() ends the line like println(). \| right: printf() adds no newline. Put \n (or %n) in the format string to end the line.
- **wrong rule / right rule:** RepeatedOutputVariablePrintedOnce: wrong: An output statement that names the same variable twice (WRITE y, x, y) prints it only once. \| right: Every expression in the output is printed, so System.out.println(y + " " + x + " " + y) with x=6, y=9 prints 9 6 9.
- **uneven-application rule:** Points to LT (output appears in the order the output calls execute, with a line break only after println). An uneven trace drops a repeated value, puts output lines out of order, or adds line breaks after print on some calls.
- **identity rule:** Standard output (System.out, StdOut) is the library abstraction for a program's text output: an output stream of characters written by print, println and printf.
- **declarative rule:** print(s) writes s. println(s) writes s and then the line separator. println() only ends the line. A null String prints as "null". By default the stream goes to the terminal window.
- **operational sequencing rule:** First the argument expression is evaluated, e.g. the concatenation "Sum is " + sum. Then its string form is appended, and println appends the line separator after it. Successive calls appear in execution order.
- **evaluation / result rule:** The output is the argument's string form. System.out.println(Math.PI) prints 3.141592653589793 (all digits), and println("Sum is " + 1778) prints Sum is 1778 followed by a newline. The methods return void.
- **state-transition rule:** One call appends text to the output (println also appends the line separator). It changes no variables and returns nothing.
- **composition rule (with a neighbour):** with stream\_model: Each output call appends to the end of the single output stream, so the order of output is the order of execution.
- **composition rule (with a neighbour):** with redirection: With \`&gt; file\`, every print/println/printf writes to the file and nothing appears in the terminal. The program code is unchanged.
- **composition rule (with a neighbour):** with standard\_input: A prompt printed with print (not println) shows on the same line where the user then types, before the following StdIn read blocks. Output and input are separate streams.
- **composition rule (with a neighbour):** with standard\_drawing: StdOut text and StdDraw pictures are independent outputs: printing does not draw, and drawing does not print.
- **composition rule (with a neighbour):** with formatted\_output: printf writes to the same stream as print and println, so mixed calls appear in call order. Unlike println, printf ends a line only when the format contains \n.
- **plan / role rule:** Standard output reports results (to a person, or to a file or program further down the line). Plan: an 'output' step after a computation, or one println per item inside a loop to list values.
- **conservation rule:** Switching System.out.print/println to StdOut.print/println keeps the output. Changing println to print keeps every character but removes the line break, so lines join.
- **error rule:** rule broken: Output order and line breaks follow the order of the calls and the print/println choice. (silent logic error)
- **error rule:** rule broken: PrintStream methods never throw IOException; a write failure only sets an internal flag. (silent logic error)
- **error rule:** rule broken: println/print take a single argument; pieces must be joined with +. (compile-time)
- **applicability rule:** Use standard output for text results meant for a reader or for the next program in a pipeline. Use printf when digits or column widths matter, and StdDraw/StdAudio for pictures and sound.

## The whole prerequisite chain

- **Everything it builds on (1):** `stream_model`
- **Everything that builds on it (5):** `data_driven_code`, `filter`, `formatted_output`, `piping`, `redirection`
