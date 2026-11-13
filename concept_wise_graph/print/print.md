# print (`print`)

System.out.print -- output with no newline

Section 1.1 Your First Program, topic 1.1.b Understanding a program (HelloWorld).

![The knowledge graph around print](print.png)

## At a glance

- **Needs first:** `statement`, `string_literal`
- **Leads to:** nothing
- **Learned alongside:** `println`
- **Misconceptions:** `ParenthesesOnlyIfArgument`, `RepeatedOutputVariablePrintedOnce`
- **Errors:** `PrintWithoutFinalNewline`
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 25 edges around this concept, each explained in the graph's own words.

## What it needs first (2)

A prerequisite edge means the other concept has to be understood before `print`.

### `statement` comes before `print`

*one step, terminated by ;, executed in sequence*

System.out.print(s); is itself a statement, so it runs at its own place in the sequence of statements.

- **Grounding:** book passage
- **How `print` combines with `statement`:** System.out.print(s); is a statement, so its output appears at its place in the statement sequence.
- **How `statement` combines with `print`:** System.out.print(s); is a statement, so its output appears exactly at its place in the sequence, with no newline.

### `string_literal` comes before `print`

*"Hello, World" -- the text being printed*

print("s") outputs exactly the characters between the quotes, without the quotes.

- **Grounding:** book passage
- **How `print` combines with `string_literal`:** print("s") outputs exactly the characters between the quotes, without the quotes; spaces inside the quotes are printed.
- **How `string_literal` combines with `print`:** print("s") outputs exactly the characters between the quotes, without the quotes.

## What it leads to (0)

These concepts need `print` first.

No concept has this one as a prerequisite.

## Learned alongside (1)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

### `print` alongside `println`

*System.out.println -- output with a trailing newline*

print leaves the cursor on the same line after printing; println moves the cursor to the next line after printing.

- **Grounding:** book passage
- **How `print` combines with `println`:** print leaves the cursor on the same line; println ends the line; a line built from several prints should end with println.
- **How `println` combines with `print`:** print leaves the cursor on the line; println ends it; several prints followed by one println make one line.

## Misconceptions (2)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### ParenthesesOnlyIfArgument

- **Wrong rule:** println with nothing to print can be written System.out.println; without the parentheses.
- **Right rule:** A method call always needs parentheses, so an empty line is printed with System.out.println();.
- **Role of this concept:** context
- **Shows at level L0 as:** misconception: wrong rule: () are optional on a call with no argument. Right rule: A method call always needs parentheses after the name.
- **Also an edge from `expression`:** () are optional on a no-argument call like println
- **Also an edge from `method_call`:** () are optional on a no-argument call like println
- **Also an edge from `println`:** println with nothing to print can be written System.out.println; without the parentheses.

### RepeatedOutputVariablePrintedOnce

- **Wrong rule:** An output statement that names the same variable twice (WRITE y, x, y) prints it only once.
- **Right rule:** Each expression in the output list is printed, so a repeated variable prints its value each time.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: An output statement that names the same variable twice prints it only once. Right rule: Each expression in the output is printed, so a repeated variable prints its value each time.
- **Shows at level L0 as:** inconsistent trace: Applies the print rule (LT) unevenly: inserts a line break after a print on one line but not another, or drops a repeated value. (here mixing in: "An output statement that names the same variable twice (WRITE y, x, y) prints it only once")
- **Also an edge from `standard_output`:** An output statement that names the same variable twice (WRITE y, x, y) prints it only once.

## Errors (1)

An error edge states the rule that gets broken in a program, and the right rule.

### PrintWithoutFinalNewline

- **Wrong rule:** Ends the output with print and expects it to appear right away.
- **Right rule:** Finish a line of print calls with println; some systems hold print output until a newline is printed.
- **Role of this concept:** primary
- **Also an edge from `println`:** Ends the output with print and expects it to appear right away.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for print: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to print agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

print -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (4 ways).

- **everyday reading** (folk-meaning rule): Everyday meaning: 'print' means send to a printer, and an output command lists each distinct name once. Java rule: System.out.print(x) displays x's characters in the terminal at the current position, with no newline, every time it runs.
- **misconception** (wrong rule / right rule; shows `RepeatedOutputVariablePrintedOnce`): wrong rule: An output statement that names the same variable twice prints it only once. Right rule: Each expression in the output is printed, so a repeated variable prints its value each time.
- **inconsistent trace** (uneven-application rule; shows `RepeatedOutputVariablePrintedOnce`): Applies the print rule (LT) unevenly: inserts a line break after a print on one line but not another, or drops a repeated value. (here mixing in: "An output statement that names the same variable twice (WRITE y, x, y) prints it only once")
- **misconception** (wrong rule / right rule; shows `ParenthesesOnlyIfArgument`): wrong rule: () are optional on a call with no argument. Right rule: A method call always needs parentheses after the name.

### L1: Unistructural / atom x text surface

L1 for print: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

print -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

- **names the element** (identity rule): System.out.print(x) is a library method call (on the PrintStream System.out) that displays x in the terminal without ending the line.
- **states the rule** (declarative rule): print(String s) prints the string (or "null" for a null reference); print(int) etc. print the value's string form; no line terminator is written.

### L2: Multistructural / block x execution / preoperational

L2 for print: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

print -&gt; L2 (Multistructural): the answer applies the rules of print to every part of the code, in order (3 ways).

- **line by line trace** (operational sequencing rule): The argument expression is evaluated first, converted to a string, then its characters are written at the current output position; the next output continues right after them.
- **output prediction** (evaluation / result rule): Output is exactly the characters of the value (a string literal without its quotes, a number in decimal) and nothing else: print("Goodbye, "); println("cruel world"); prints Goodbye, cruel world on one line.
- **one step execution** (state-transition rule): One call appends the value's characters to the output and leaves the cursor on the same line; it changes no variable and returns nothing (void).

### L3: Relational / relations x function (concrete operational begins)

L3 for print: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

print -&gt; L3 (Relational): the answer relates the parts (4 ways).

- **relation to neighbour** (composition rule (with a neighbour)): System.out.print(s); is a statement, so its output appears at its place in the statement sequence.
- **relation to neighbour** (composition rule (with a neighbour)): print("s") outputs exactly the characters between the quotes, without the quotes; spaces inside the quotes are printed.
- **relation to neighbour** (composition rule (with a neighbour)): print leaves the cursor on the same line; println ends the line; a line built from several prints should end with println.
- **purpose of the whole** (plan / role rule): Purpose: build one line of output from several pieces (a prompt, labels and values) before ending it with println.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for print: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

print -&gt; L4 (Extended abstract): the answer reasons beyond the given code (4 ways).

- **predict a change** (conservation rule; shows `RepeatedOutputVariablePrintedOnce`): Changing print to println (or back) moves the following output to a new line (or the same line) but keeps the characters printed; swapping two print statements swaps their text.
- **diagnose an error** (error rule): rule broken: Finish a line of print calls with println. Kind: silent logic error. Trigger class: the last output of the program is a print: on some systems the text is held and not shown, or the prompt appears on the same line
- **transfer to a new program** (applicability rule): Use print when more output must follow on the same line (prompts, items in a row); use println to end a line, and printf when the number format matters.
- **diagnose an error** (error rule): rule broken: A method call needs parentheses and correct case. Kind: compile-time. Trigger class: System.out.print "x"; or System.out.Print(x)

## Same topic

`print` belongs to the topic **Understanding a program (HelloWorld)** (`topic1.1.b`). The topic also contains: `block`, `class_declaration`, `comment`, `main_method`, `println`, `program_layout`, `statement`, `string_literal`.

## Rules of the concept (17)

- **folk-meaning rule:** Everyday meaning: 'print' means send to a printer, and an output command lists each distinct name once. Java rule: System.out.print(x) displays x's characters in the terminal at the current position, with no newline, every time it runs.
- **wrong rule / right rule:** ParenthesesOnlyIfArgument: wrong: () are optional on a call with no argument. \| right: A method call always needs parentheses after the name.
- **wrong rule / right rule:** RepeatedOutputVariablePrintedOnce: wrong: An output statement that names the same variable twice prints it only once. \| right: Each expression in the output is printed, so a repeated variable prints its value each time.
- **uneven-application rule:** Applies the print rule (LT) unevenly: inserts a line break after a print on one line but not another, or drops a repeated value.
- **identity rule:** System.out.print(x) is a library method call (on the PrintStream System.out) that displays x in the terminal without ending the line.
- **declarative rule:** print(String s) prints the string (or "null" for a null reference); print(int) etc. print the value's string form; no line terminator is written.
- **operational sequencing rule:** The argument expression is evaluated first, converted to a string, then its characters are written at the current output position; the next output continues right after them.
- **evaluation / result rule:** Output is exactly the characters of the value (a string literal without its quotes, a number in decimal) and nothing else: print("Goodbye, "); println("cruel world"); prints Goodbye, cruel world on one line.
- **state-transition rule:** One call appends the value's characters to the output and leaves the cursor on the same line; it changes no variable and returns nothing (void).
- **composition rule (with a neighbour):** with statement: System.out.print(s); is a statement, so its output appears at its place in the statement sequence.
- **composition rule (with a neighbour):** with string\_literal: print("s") outputs exactly the characters between the quotes, without the quotes; spaces inside the quotes are printed.
- **composition rule (with a neighbour):** with println: print leaves the cursor on the same line; println ends the line; a line built from several prints should end with println.
- **plan / role rule:** Purpose: build one line of output from several pieces (a prompt, labels and values) before ending it with println.
- **conservation rule:** Changing print to println (or back) moves the following output to a new line (or the same line) but keeps the characters printed; swapping two print statements swaps their text.
- **error rule:** rule broken: Finish a line of print calls with println (silent logic error)
- **error rule:** rule broken: A method call needs parentheses and correct case (compile-time)
- **applicability rule:** Use print when more output must follow on the same line (prompts, items in a row); use println to end a line, and printf when the number format matters.

## The whole prerequisite chain

- **Everything it builds on (5):** `class_declaration`, `main_method`, `program_text`, `statement`, `string_literal`
- **Everything that builds on it (0):** nothing
