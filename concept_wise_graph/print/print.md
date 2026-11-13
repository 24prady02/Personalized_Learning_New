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

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 25 edges around this concept. The edge logic, the wrong and right rules and the exact rules of the ways are copied word for word from the graph.

## To work on (0)

Nothing is missing for this concept.

## What it needs first (2)

A prerequisite edge means the other concept has to be understood before `print`.

### `statement` comes before `print`

*one step, terminated by ;, executed in sequence*

- **Edge:** `pre:statement->print`
- **Exact edge logic:** System.out.print(s); is itself a statement, so it runs at its own place in the sequence of statements.
- **Grounding:** book\_passage
- **Composition rule (R) of `print` with `statement`:** System.out.print(s); is a statement, so its output appears at its place in the statement sequence.
- **Composition rule (R) of `statement` with `print`:** System.out.print(s); is a statement, so its output appears exactly at its place in the sequence, with no newline.

### `string_literal` comes before `print`

*"Hello, World" -- the text being printed*

- **Edge:** `pre:string_literal->print`
- **Exact edge logic:** print("s") outputs exactly the characters between the quotes, without the quotes.
- **Grounding:** book\_passage
- **Composition rule (R) of `print` with `string_literal`:** print("s") outputs exactly the characters between the quotes, without the quotes; spaces inside the quotes are printed.
- **Composition rule (R) of `string_literal` with `print`:** print("s") outputs exactly the characters between the quotes, without the quotes.

## What it leads to (0)

These concepts need `print` first.

No concept has this one as a prerequisite.

## Learned alongside (1)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

### `print` alongside `println`

*System.out.println -- output with a trailing newline*

- **Edge:** `par:print~println`
- **Exact edge logic:** print leaves the cursor on the same line after printing; println moves the cursor to the next line after printing.
- **Grounding:** book\_passage
- **Composition rule (R) of `print` with `println`:** print leaves the cursor on the same line; println ends the line; a line built from several prints should end with println.
- **Composition rule (R) of `println` with `print`:** print leaves the cursor on the line; println ends it; several prints followed by one println make one line.

## Misconceptions (2)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### ParenthesesOnlyIfArgument

- **Edge:** `print` &rarr; `ParenthesesOnlyIfArgument` (misconception)
- **Exact edge logic (the wrong rule):** println with nothing to print can be written System.out.println; without the parentheses.
- **Twin logic (the right rule):** A method call always needs parentheses, so an empty line is printed with System.out.println();.
- **Wrong belief (on the node):** () are optional on a no-argument call like println
- **Correct rule (on the node):** A method call always needs parentheses, so an empty line is printed with System.out.println();.
- **Provenance:** published
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [3] misconception, exact rule:** wrong rule: () are optional on a call with no argument. Right rule: A method call always needs parentheses after the name.
- **Edge `expression` &rarr; `ParenthesesOnlyIfArgument`, exact edge logic:** () are optional on a no-argument call like println **Twin logic:** A method call always needs parentheses, so an empty line is printed with System.out.println();. (role: context)
- **Edge `method_call` &rarr; `ParenthesesOnlyIfArgument`, exact edge logic:** () are optional on a no-argument call like println **Twin logic:** A method call always needs parentheses, so an empty line is printed with System.out.println();. (role: primary)
- **Edge `println` &rarr; `ParenthesesOnlyIfArgument`, exact edge logic:** println with nothing to print can be written System.out.println; without the parentheses. **Twin logic:** A method call always needs parentheses, so an empty line is printed with System.out.println();. (role: context)

### RepeatedOutputVariablePrintedOnce

- **Edge:** `print` &rarr; `RepeatedOutputVariablePrintedOnce` (misconception)
- **Exact edge logic (the wrong rule):** An output statement that names the same variable twice (WRITE y, x, y) prints it only once.
- **Twin logic (the right rule):** Each expression in the output list is printed, so a repeated variable prints its value each time.
- **Wrong belief (on the node):** An output statement that names the same variable twice (WRITE y, x, y) prints it only once.
- **Correct rule (on the node):** Each expression in the output list is printed, so a repeated variable prints its value each time.
- **Provenance:** published
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [1] misconception, exact rule:** wrong rule: An output statement that names the same variable twice prints it only once. Right rule: Each expression in the output is printed, so a repeated variable prints its value each time.
- **L0 way [2] inconsistent\_trace, exact rule:** Applies the print rule (LT) unevenly: inserts a line break after a print on one line but not another, or drops a repeated value. (here mixing in: "An output statement that names the same variable twice (WRITE y, x, y) prints it only once")
- **Edge `standard_output` &rarr; `RepeatedOutputVariablePrintedOnce`, exact edge logic:** An output statement that names the same variable twice (WRITE y, x, y) prints it only once. **Twin logic:** Each expression in the output list is printed, so a repeated variable prints its value each time. (role: context)

## Errors (1)

An error edge states the rule that gets broken in a program, and the right rule.

### PrintWithoutFinalNewline

- **Edge:** `print` &rarr; `PrintWithoutFinalNewline` (error)
- **Exact edge logic (the wrong rule):** Ends the output with print and expects it to appear right away.
- **Twin logic (the right rule):** Finish a line of print calls with println; some systems hold print output until a newline is printed.
- **Wrong belief (on the node):** Ends the output with print and expects it to appear right away.
- **Correct rule (on the node):** Finish a line of print calls with println; some systems hold print output until a newline is printed.
- **Provenance:** textbook
- **Role of this concept:** primary
- **Edge `println` &rarr; `PrintWithoutFinalNewline`, exact edge logic:** Ends the output with print and expects it to appear right away. **Twin logic:** Finish a line of print calls with println; some systems hold print output until a newline is printed. (role: context)

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for print: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to print agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

- **Edge:** `print` &rarr; `print@L0` (has_level)
- **Exact edge logic:** print -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (4 ways).

Ways (4), each with its exact rule:

- **[0] everyday\_reading** (rule type E, folk-meaning rule): Everyday meaning: 'print' means send to a printer, and an output command lists each distinct name once. Java rule: System.out.print(x) displays x's characters in the terminal at the current position, with no newline, every time it runs.
- **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `RepeatedOutputVariablePrintedOnce`: wrong rule: An output statement that names the same variable twice prints it only once. Right rule: Each expression in the output is printed, so a repeated variable prints its value each time.
- **[2] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `RepeatedOutputVariablePrintedOnce`: Applies the print rule (LT) unevenly: inserts a line break after a print on one line but not another, or drops a repeated value. (here mixing in: "An output statement that names the same variable twice (WRITE y, x, y) prints it only once")
- **[3] misconception** (rule type M, wrong rule / right rule) &rarr; `ParenthesesOnlyIfArgument`: wrong rule: () are optional on a call with no argument. Right rule: A method call always needs parentheses after the name.

### L1: Unistructural / atom x text surface

L1 for print: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

- **Edge:** `print` &rarr; `print@L1` (has_level)
- **Exact edge logic:** print -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

Ways (2), each with its exact rule:

- **[0] names\_the\_element** (rule type N, identity rule): System.out.print(x) is a library method call (on the PrintStream System.out) that displays x in the terminal without ending the line.
- **[1] states\_the\_rule** (rule type S, declarative rule): print(String s) prints the string (or "null" for a null reference); print(int) etc. print the value's string form; no line terminator is written.

### L2: Multistructural / block x execution / preoperational

L2 for print: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

- **Edge:** `print` &rarr; `print@L2` (has_level)
- **Exact edge logic:** print -&gt; L2 (Multistructural): the answer applies the rules of print to every part of the code, in order (3 ways).

Ways (3), each with its exact rule:

- **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): The argument expression is evaluated first, converted to a string, then its characters are written at the current output position; the next output continues right after them.
- **[1] output\_prediction** (rule type OP, evaluation / result rule): Output is exactly the characters of the value (a string literal without its quotes, a number in decimal) and nothing else: print("Goodbye, "); println("cruel world"); prints Goodbye, cruel world on one line.
- **[2] one\_step\_execution** (rule type OS, state-transition rule): One call appends the value's characters to the output and leaves the cursor on the same line; it changes no variable and returns nothing (void).

### L3: Relational / relations x function (concrete operational begins)

L3 for print: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

- **Edge:** `print` &rarr; `print@L3` (has_level)
- **Exact edge logic:** print -&gt; L3 (Relational): the answer relates the parts (4 ways).

Ways (4), each with its exact rule:

- **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): System.out.print(s); is a statement, so its output appears at its place in the statement sequence.
- **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): print("s") outputs exactly the characters between the quotes, without the quotes; spaces inside the quotes are printed.
- **[2] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): print leaves the cursor on the same line; println ends the line; a line built from several prints should end with println.
- **[3] purpose\_of\_the\_whole** (rule type P, plan / role rule): Purpose: build one line of output from several pieces (a prompt, labels and values) before ending it with println.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for print: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

- **Edge:** `print` &rarr; `print@L4` (has_level)
- **Exact edge logic:** print -&gt; L4 (Extended abstract): the answer reasons beyond the given code (4 ways).

Ways (4), each with its exact rule:

- **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `RepeatedOutputVariablePrintedOnce`: Changing print to println (or back) moves the following output to a new line (or the same line) but keeps the characters printed; swapping two print statements swaps their text.
- **[1] diagnose\_an\_error** (rule type D, error rule): rule broken: Finish a line of print calls with println. Kind: silent logic error. Trigger class: the last output of the program is a print: on some systems the text is held and not shown, or the prompt appears on the same line
- **[2] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Use print when more output must follow on the same line (prompts, items in a row); use println to end a line, and printf when the number format matters.
- **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: A method call needs parentheses and correct case. Kind: compile-time. Trigger class: System.out.print "x"; or System.out.Print(x)

## Same topic

`print` belongs to the topic **Understanding a program (HelloWorld)** (`topic1.1.b`). The topic also contains: `block`, `class_declaration`, `comment`, `main_method`, `println`, `program_layout`, `statement`, `string_literal`.

## Rules of the concept (17)

- **Book** (SW-1e, p. 7 (pdf 17)): "calls on System.out.print() to print in the terminal window the message"
- **Book** (API-PrintStream, ): "print(String s): Prints a string."
- **E** (folk-meaning rule): Everyday meaning: 'print' means send to a printer, and an output command lists each distinct name once. Java rule: System.out.print(x) displays x's characters in the terminal at the current position, with no newline, every time it runs.
- **M** (wrong rule / right rule): ParenthesesOnlyIfArgument: wrong: () are optional on a call with no argument. \| right: A method call always needs parentheses after the name.
- **M** (wrong rule / right rule): RepeatedOutputVariablePrintedOnce: wrong: An output statement that names the same variable twice prints it only once. \| right: Each expression in the output is printed, so a repeated variable prints its value each time.
- **T** (uneven-application rule): Applies the print rule (LT) unevenly: inserts a line break after a print on one line but not another, or drops a repeated value.
- **N** (identity rule): System.out.print(x) is a library method call (on the PrintStream System.out) that displays x in the terminal without ending the line.
- **S** (declarative rule): print(String s) prints the string (or "null" for a null reference); print(int) etc. print the value's string form; no line terminator is written.
- **LT** (operational sequencing rule): The argument expression is evaluated first, converted to a string, then its characters are written at the current output position; the next output continues right after them.
- **OP** (evaluation / result rule): Output is exactly the characters of the value (a string literal without its quotes, a number in decimal) and nothing else: print("Goodbye, "); println("cruel world"); prints Goodbye, cruel world on one line.
- **OS** (state-transition rule): One call appends the value's characters to the output and leaves the cursor on the same line; it changes no variable and returns nothing (void).
- **R** (composition rule (with a neighbour)): with statement: System.out.print(s); is a statement, so its output appears at its place in the statement sequence.
- **R** (composition rule (with a neighbour)): with string\_literal: print("s") outputs exactly the characters between the quotes, without the quotes; spaces inside the quotes are printed.
- **R** (composition rule (with a neighbour)): with println: print leaves the cursor on the same line; println ends the line; a line built from several prints should end with println.
- **P** (plan / role rule): Purpose: build one line of output from several pieces (a prompt, labels and values) before ending it with println.
- **C** (conservation rule): Changing print to println (or back) moves the following output to a new line (or the same line) but keeps the characters printed; swapping two print statements swaps their text.
- **D** (error rule): rule broken: Finish a line of print calls with println (silent logic error)
- **D** (error rule): rule broken: A method call needs parentheses and correct case (compile-time)
- **X** (applicability rule): Use print when more output must follow on the same line (prompts, items in a row); use println to end a line, and printf when the number format matters.

## How it is found in code and answers (reader block)

- **Aliases:** print, system.out.print
- **Code patterns:** `System\.out\.print\s*\(`, `StdOut\.print\s*\(`, `\bSystem\.out\.print\s*\(`, `\bStdOut\.print\s*\(`, `System\.err\.print\s*\(`
- **Operator symbols:** none
- **Java types:** none

## The whole prerequisite chain

- **Everything it builds on (5):** `class_declaration`, `main_method`, `program_text`, `statement`, `string_literal`
- **Everything that builds on it (0):** nothing

## Every edge in this view and its exact edge logic (25)

All the edges drawn in the picture, in the order: prerequisite, parallel, misconception, error, has_level, contains.

**1. `statement` &rarr; `print`** (prerequisite)

- **Exact edge logic:** System.out.print(s); is itself a statement, so it runs at its own place in the sequence of statements.
- **Grounding:** book\_passage
- **Composition rule (R) of `statement` with `print`:** System.out.print(s); is a statement, so its output appears exactly at its place in the sequence, with no newline.
- **Composition rule (R) of `print` with `statement`:** System.out.print(s); is a statement, so its output appears at its place in the statement sequence.

**2. `string_literal` &rarr; `print`** (prerequisite)

- **Exact edge logic:** print("s") outputs exactly the characters between the quotes, without the quotes.
- **Grounding:** book\_passage
- **Composition rule (R) of `string_literal` with `print`:** print("s") outputs exactly the characters between the quotes, without the quotes.
- **Composition rule (R) of `print` with `string_literal`:** print("s") outputs exactly the characters between the quotes, without the quotes; spaces inside the quotes are printed.

**3. `print` &harr; `println`** (parallel)

- **Exact edge logic:** print leaves the cursor on the same line after printing; println moves the cursor to the next line after printing.
- **Grounding:** book\_passage
- **Composition rule (R) of `print` with `println`:** print leaves the cursor on the same line; println ends the line; a line built from several prints should end with println.
- **Composition rule (R) of `println` with `print`:** print leaves the cursor on the line; println ends it; several prints followed by one println make one line.

**4. `print` &rarr; `ParenthesesOnlyIfArgument`** (misconception)

- **Exact edge logic (the wrong rule):** println with nothing to print can be written System.out.println; without the parentheses.
- **Twin logic (the right rule):** A method call always needs parentheses, so an empty line is printed with System.out.println();.
- **Role:** context

**5. `print` &rarr; `RepeatedOutputVariablePrintedOnce`** (misconception)

- **Exact edge logic (the wrong rule):** An output statement that names the same variable twice (WRITE y, x, y) prints it only once.
- **Twin logic (the right rule):** Each expression in the output list is printed, so a repeated variable prints its value each time.
- **Role:** primary

**6. `expression` &rarr; `ParenthesesOnlyIfArgument`** (misconception)

- **Exact edge logic (the wrong rule):** () are optional on a no-argument call like println
- **Twin logic (the right rule):** A method call always needs parentheses, so an empty line is printed with System.out.println();.
- **Role:** context

**7. `method_call` &rarr; `ParenthesesOnlyIfArgument`** (misconception)

- **Exact edge logic (the wrong rule):** () are optional on a no-argument call like println
- **Twin logic (the right rule):** A method call always needs parentheses, so an empty line is printed with System.out.println();.
- **Role:** primary

**8. `println` &rarr; `ParenthesesOnlyIfArgument`** (misconception)

- **Exact edge logic (the wrong rule):** println with nothing to print can be written System.out.println; without the parentheses.
- **Twin logic (the right rule):** A method call always needs parentheses, so an empty line is printed with System.out.println();.
- **Role:** context

**9. `standard_output` &rarr; `RepeatedOutputVariablePrintedOnce`** (misconception)

- **Exact edge logic (the wrong rule):** An output statement that names the same variable twice (WRITE y, x, y) prints it only once.
- **Twin logic (the right rule):** Each expression in the output list is printed, so a repeated variable prints its value each time.
- **Role:** context

**10. `print` &rarr; `PrintWithoutFinalNewline`** (error)

- **Exact edge logic (the wrong rule):** Ends the output with print and expects it to appear right away.
- **Twin logic (the right rule):** Finish a line of print calls with println; some systems hold print output until a newline is printed.
- **Role:** primary

**11. `println` &rarr; `PrintWithoutFinalNewline`** (error)

- **Exact edge logic (the wrong rule):** Ends the output with print and expects it to appear right away.
- **Twin logic (the right rule):** Finish a line of print calls with println; some systems hold print output until a newline is printed.
- **Role:** context

**12. `print` &rarr; `print@L0`** (has_level)

- **Exact edge logic:** print -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (4 ways).
  - **[0] everyday\_reading** (rule type E, folk-meaning rule): Everyday meaning: 'print' means send to a printer, and an output command lists each distinct name once. Java rule: System.out.print(x) displays x's characters in the terminal at the current position, with no newline, every time it runs.
  - **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `RepeatedOutputVariablePrintedOnce`: wrong rule: An output statement that names the same variable twice prints it only once. Right rule: Each expression in the output is printed, so a repeated variable prints its value each time.
  - **[2] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `RepeatedOutputVariablePrintedOnce`: Applies the print rule (LT) unevenly: inserts a line break after a print on one line but not another, or drops a repeated value. (here mixing in: "An output statement that names the same variable twice (WRITE y, x, y) prints it only once")
  - **[3] misconception** (rule type M, wrong rule / right rule) &rarr; `ParenthesesOnlyIfArgument`: wrong rule: () are optional on a call with no argument. Right rule: A method call always needs parentheses after the name.

**13. `print` &rarr; `print@L1`** (has_level)

- **Exact edge logic:** print -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).
  - **[0] names\_the\_element** (rule type N, identity rule): System.out.print(x) is a library method call (on the PrintStream System.out) that displays x in the terminal without ending the line.
  - **[1] states\_the\_rule** (rule type S, declarative rule): print(String s) prints the string (or "null" for a null reference); print(int) etc. print the value's string form; no line terminator is written.

**14. `print` &rarr; `print@L2`** (has_level)

- **Exact edge logic:** print -&gt; L2 (Multistructural): the answer applies the rules of print to every part of the code, in order (3 ways).
  - **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): The argument expression is evaluated first, converted to a string, then its characters are written at the current output position; the next output continues right after them.
  - **[1] output\_prediction** (rule type OP, evaluation / result rule): Output is exactly the characters of the value (a string literal without its quotes, a number in decimal) and nothing else: print("Goodbye, "); println("cruel world"); prints Goodbye, cruel world on one line.
  - **[2] one\_step\_execution** (rule type OS, state-transition rule): One call appends the value's characters to the output and leaves the cursor on the same line; it changes no variable and returns nothing (void).

**15. `print` &rarr; `print@L3`** (has_level)

- **Exact edge logic:** print -&gt; L3 (Relational): the answer relates the parts (4 ways).
  - **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): System.out.print(s); is a statement, so its output appears at its place in the statement sequence.
  - **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): print("s") outputs exactly the characters between the quotes, without the quotes; spaces inside the quotes are printed.
  - **[2] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): print leaves the cursor on the same line; println ends the line; a line built from several prints should end with println.
  - **[3] purpose\_of\_the\_whole** (rule type P, plan / role rule): Purpose: build one line of output from several pieces (a prompt, labels and values) before ending it with println.

**16. `print` &rarr; `print@L4`** (has_level)

- **Exact edge logic:** print -&gt; L4 (Extended abstract): the answer reasons beyond the given code (4 ways).
  - **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `RepeatedOutputVariablePrintedOnce`: Changing print to println (or back) moves the following output to a new line (or the same line) but keeps the characters printed; swapping two print statements swaps their text.
  - **[1] diagnose\_an\_error** (rule type D, error rule): rule broken: Finish a line of print calls with println. Kind: silent logic error. Trigger class: the last output of the program is a print: on some systems the text is held and not shown, or the prompt appears on the same line
  - **[2] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Use print when more output must follow on the same line (prompts, items in a row); use println to end a line, and printf when the number format matters.
  - **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: A method call needs parentheses and correct case. Kind: compile-time. Trigger class: System.out.print "x"; or System.out.Print(x)

**17. `topic1.1.b` &rarr; `print`** (contains)

- topic `topic1.1.b` contains `print`

**18. `topic1.1.b` &rarr; `block`** (contains)

- topic `topic1.1.b` contains `block`

**19. `topic1.1.b` &rarr; `class_declaration`** (contains)

- topic `topic1.1.b` contains `class_declaration`

**20. `topic1.1.b` &rarr; `comment`** (contains)

- topic `topic1.1.b` contains `comment`

**21. `topic1.1.b` &rarr; `main_method`** (contains)

- topic `topic1.1.b` contains `main_method`

**22. `topic1.1.b` &rarr; `println`** (contains)

- topic `topic1.1.b` contains `println`

**23. `topic1.1.b` &rarr; `program_layout`** (contains)

- topic `topic1.1.b` contains `program_layout`

**24. `topic1.1.b` &rarr; `statement`** (contains)

- topic `topic1.1.b` contains `statement`

**25. `topic1.1.b` &rarr; `string_literal`** (contains)

- topic `topic1.1.b` contains `string_literal`
