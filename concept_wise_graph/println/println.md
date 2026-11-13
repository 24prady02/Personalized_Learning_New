# println (`println`)

System.out.println -- output with a trailing newline

Section 1.1 Your First Program, topic 1.1.b Understanding a program (HelloWorld).

![The knowledge graph around println](println.png)

## At a glance

- **Needs first:** `statement`, `string_literal`
- **Leads to:** `printing_array_reference`
- **Learned alongside:** `formatted_output`, `print`
- **Misconceptions:** `IdentifierCaseInsensitive`, `ParenthesesOnlyIfArgument`, `PrintEqualsPrintln`, `PrintNewLineFirst`, `PrintedTextIsExecuted`
- **Errors:** `PrintWithoutFinalNewline`
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 33 edges around this concept. The edge logic, the wrong and right rules and the exact rules of the ways are copied word for word from the graph.

## To work on (1)

- misconceptions with no L0 way linked to them: PrintedTextIsExecuted

## What it needs first (2)

A prerequisite edge means the other concept has to be understood before `println`.

### `statement` comes before `println`

*one step, terminated by ;, executed in sequence*

- **Edge:** `pre:statement->println`
- **Exact edge logic:** System.out.println(s); is itself a statement, so its line of output appears at its own place in the sequence.
- **Grounding:** book\_passage
- **Composition rule (R) of `println` with `statement`:** System.out.println(s); is a statement, so its line of output appears at its own place in the sequence.
- **Composition rule (R) of `statement` with `println`:** System.out.println(s); is a statement, so its line of output appears at its place in the sequence; swapping two println statements swaps the output lines.

### `string_literal` comes before `println`

*"Hello, World" -- the text being printed*

- **Edge:** `pre:string_literal->println`
- **Exact edge logic:** println("s") outputs exactly the characters between the quotes and then ends the line.
- **Grounding:** book\_passage
- **Composition rule (R) of `println` with `string_literal`:** println("s") outputs exactly the characters between the quotes and then ends the line.
- **Composition rule (R) of `string_literal` with `println`:** println("s") outputs exactly the characters between the quotes and then ends the line.

## What it leads to (1)

These concepts need `println` first.

### `println` comes before `printing_array_reference`

*printing an array variable prints a reference, not the elements*

- **Edge:** `pre:println->printing_array_reference`
- **Exact edge logic:** println of an array variable prints the array's reference, not its elements.
- **Grounding:** book\_passage

## Learned alongside (2)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

### `println` alongside `formatted_output`

*printf with a format string such as %d, %.2f, %s*

- **Edge:** `par:println~formatted_output`
- **Exact edge logic:** println prints each number with all its digits and ends the line; printf formats each value by its conversion code and starts a new line only when \n is in the format string.
- **Grounding:** book\_passage
- **Composition rule (R) of `println` with `formatted_output`:** println prints numbers with all their digits and always ends the line; printf formats each value by its conversion code and ends the line only where the format has %n or \n.
- **Composition rule (R) of `formatted_output` with `println`:** println prints a double with all its digits (about 15 places) and always ends the line. printf("%.2f\n", x) controls the digits and ends the line only because of \n.

### `println` alongside `print`

*System.out.print -- output with no newline*

- **Edge:** `par:print~println`
- **Exact edge logic:** print leaves the cursor on the same line after printing; println moves the cursor to the next line after printing.
- **Grounding:** book\_passage
- **Composition rule (R) of `println` with `print`:** print leaves the cursor on the line; println ends it; several prints followed by one println make one line.
- **Composition rule (R) of `print` with `println`:** print leaves the cursor on the same line; println ends the line; a line built from several prints should end with println.

## Misconceptions (5)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### IdentifierCaseInsensitive

- **Edge:** `println` &rarr; `IdentifierCaseInsensitive` (misconception)
- **Exact edge logic (the wrong rule):** System.out.Println and System.out.println name the same method.
- **Twin logic (the right rule):** Java is case-sensitive: names of variables, methods and classes that differ only in capitalization are different names.
- **Wrong belief (on the node):** System.out.Println and System.out.println name the same method.
- **Correct rule (on the node):** Java is case-sensitive: names of variables, methods and classes that differ only in capitalization are different names.
- **Provenance:** textbook
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [4] misconception, exact rule:** wrong rule: System.out.Println and System.out.println name the same method. Right rule: Java is case-sensitive: names that differ only in capitalization are different names.
- **Edge `identifier` &rarr; `IdentifierCaseInsensitive`, exact edge logic:** System.out.Println and System.out.println name the same method. **Twin logic:** Java is case-sensitive: names of variables, methods and classes that differ only in capitalization are different names. (role: primary)

### ParenthesesOnlyIfArgument

- **Edge:** `println` &rarr; `ParenthesesOnlyIfArgument` (misconception)
- **Exact edge logic (the wrong rule):** println with nothing to print can be written System.out.println; without the parentheses.
- **Twin logic (the right rule):** A method call always needs parentheses, so an empty line is printed with System.out.println();.
- **Wrong belief (on the node):** () are optional on a no-argument call like println
- **Correct rule (on the node):** A method call always needs parentheses, so an empty line is printed with System.out.println();.
- **Provenance:** published
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [5] misconception, exact rule:** wrong rule: () are optional on a no-argument call like println. Right rule: A method call always needs parentheses, so an empty line is printed with System.out.println();.
- **Edge `expression` &rarr; `ParenthesesOnlyIfArgument`, exact edge logic:** () are optional on a no-argument call like println **Twin logic:** A method call always needs parentheses, so an empty line is printed with System.out.println();. (role: context)
- **Edge `method_call` &rarr; `ParenthesesOnlyIfArgument`, exact edge logic:** () are optional on a no-argument call like println **Twin logic:** A method call always needs parentheses, so an empty line is printed with System.out.println();. (role: primary)
- **Edge `print` &rarr; `ParenthesesOnlyIfArgument`, exact edge logic:** println with nothing to print can be written System.out.println; without the parentheses. **Twin logic:** A method call always needs parentheses, so an empty line is printed with System.out.println();. (role: context)

### PrintEqualsPrintln

- **Edge:** `println` &rarr; `PrintEqualsPrintln` (misconception)
- **Exact edge logic (the wrong rule):** print and println do the same thing, so print(s1); print(s2); puts s1 and s2 on separate lines.
- **Twin logic (the right rule):** println ends the line after printing and print does not, so print(s1); print(s2); puts s1 and s2 on the same line.
- **Wrong belief (on the node):** print and println behave the same (no newline difference)
- **Correct rule (on the node):** println ends the line after printing and print does not, so print(s1); print(s2); puts s1 and s2 on the same line.
- **Provenance:** derived
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [1] misconception, exact rule:** wrong rule: print and println behave the same. Right rule: println ends the line after printing and print does not, so print(s1); print(s2); puts s1 and s2 on the same line.
- **L0 way [3] inconsistent\_trace, exact rule:** Applies the println rule (print, then end line) unevenly: puts the newline before the text on one call and after it on another, or forgets that the next output starts on a new line. (here mixing in: "print and println behave the same (no newline difference)")
- **Edge `standard_output` &rarr; `PrintEqualsPrintln`, exact edge logic:** print and println behave the same (no newline difference) **Twin logic:** println ends the line after printing and print does not, so print(s1); print(s2); puts s1 and s2 on the same line. (role: context)

### PrintNewLineFirst

- **Edge:** `println` &rarr; `PrintNewLineFirst` (misconception)
- **Exact edge logic (the wrong rule):** println(s) prints a newline and then s.
- **Twin logic (the right rule):** println(s) prints s and then the newline.
- **Wrong belief (on the node):** println(s) prints a newline and then s.
- **Correct rule (on the node):** println(s) prints s and then the newline.
- **Provenance:** published
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [2] misconception, exact rule:** wrong rule: println(s) prints a newline and then s. Right rule: println(s) prints s and then the line terminator.

### PrintedTextIsExecuted

- **Edge:** `println` &rarr; `PrintedTextIsExecuted` (misconception)
- **Exact edge logic (the wrong rule):** System.out.println("x is 5"); sets x to 5 (text inside the quotes is run as code).
- **Twin logic (the right rule):** Characters inside double quotes are printed literally; println only displays them and changes no variable. Only an assignment such as x = 5; sets x.
- **Wrong belief (on the node):** System.out.println("x is 5"); sets x to 5 (text inside the quotes is run as code).
- **Correct rule (on the node):** Characters inside double quotes are printed literally; println only displays them and changes no variable. Only an assignment such as x = 5; sets x.
- **Provenance:** scenario
- **Role of this concept:** primary
- **L0 way linked to it:** no
- **Edge `assignment` &rarr; `PrintedTextIsExecuted`, exact edge logic:** System.out.println("x is 5"); sets x to 5 (text inside the quotes is run as code). **Twin logic:** Characters inside double quotes are printed literally; println only displays them and changes no variable. Only an assignment such as x = 5; sets x. (role: context)
- **Edge `string_literal` &rarr; `PrintedTextIsExecuted`, exact edge logic:** System.out.println("x is 5"); sets x to 5 (text inside the quotes is run as code). **Twin logic:** Characters inside double quotes are printed literally; println only displays them and changes no variable. Only an assignment such as x = 5; sets x. (role: context)

## Errors (1)

An error edge states the rule that gets broken in a program, and the right rule.

### PrintWithoutFinalNewline

- **Edge:** `println` &rarr; `PrintWithoutFinalNewline` (error)
- **Exact edge logic (the wrong rule):** Ends the output with print and expects it to appear right away.
- **Twin logic (the right rule):** Finish a line of print calls with println; some systems hold print output until a newline is printed.
- **Wrong belief (on the node):** Ends the output with print and expects it to appear right away.
- **Correct rule (on the node):** Finish a line of print calls with println; some systems hold print output until a newline is printed.
- **Provenance:** textbook
- **Role of this concept:** context
- **Edge `print` &rarr; `PrintWithoutFinalNewline`, exact edge logic:** Ends the output with print and expects it to appear right away. **Twin logic:** Finish a line of print calls with println; some systems hold print output until a newline is printed. (role: primary)

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for println: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to println agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

- **Edge:** `println` &rarr; `println@L0` (has_level)
- **Exact edge logic:** println -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (6 ways).

Ways (6), each with its exact rule:

- **[0] everyday\_reading** (rule type E, folk-meaning rule): Everyday reading: 'println' is just 'print', and 'new line' is something you do before writing. Java rule: println(x) prints x and then ends the line; println() alone just ends the line.
- **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `PrintEqualsPrintln`: wrong rule: print and println behave the same. Right rule: println ends the line after printing and print does not, so print(s1); print(s2); puts s1 and s2 on the same line.
- **[2] misconception** (rule type M, wrong rule / right rule) &rarr; `PrintNewLineFirst`: wrong rule: println(s) prints a newline and then s. Right rule: println(s) prints s and then the line terminator.
- **[3] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `PrintEqualsPrintln`: Applies the println rule (print, then end line) unevenly: puts the newline before the text on one call and after it on another, or forgets that the next output starts on a new line. (here mixing in: "print and println behave the same (no newline difference)")
- **[4] misconception** (rule type M, wrong rule / right rule) &rarr; `IdentifierCaseInsensitive`: wrong rule: System.out.Println and System.out.println name the same method. Right rule: Java is case-sensitive: names that differ only in capitalization are different names.
- **[5] misconception** (rule type M, wrong rule / right rule) &rarr; `ParenthesesOnlyIfArgument`: wrong rule: () are optional on a no-argument call like println. Right rule: A method call always needs parentheses, so an empty line is printed with System.out.println();.

### L1: Unistructural / atom x text surface

L1 for println: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

- **Edge:** `println` &rarr; `println@L1` (has_level)
- **Exact edge logic:** println -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

Ways (2), each with its exact rule:

- **[0] names\_the\_element** (rule type N, identity rule): System.out.println is a library method that prints its argument followed by a line terminator ('print line').
- **[1] states\_the\_rule** (rule type S, declarative rule): println(String x) behaves as though it calls print(x) and then println(); println() terminates the current line by writing the line separator string.

### L2: Multistructural / block x execution / preoperational

L2 for println: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

- **Edge:** `println` &rarr; `println@L2` (has_level)
- **Exact edge logic:** println -&gt; L2 (Multistructural): the answer applies the rules of println to every part of the code, in order (3 ways).

Ways (3), each with its exact rule:

- **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): Evaluate the argument, print its characters at the current position, then write the line separator so the cursor moves to the beginning of the next line.
- **[1] output\_prediction** (rule type OP, evaluation / result rule): Output is the value's characters followed by a line break: println("Hello, "); println("World!"); prints two lines.
- **[2] one\_step\_execution** (rule type OS, state-transition rule): One call appends the text and a line separator to the output; the cursor ends at the start of the next line; no variable changes and nothing is returned.

### L3: Relational / relations x function (concrete operational begins)

L3 for println: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

- **Edge:** `println` &rarr; `println@L3` (has_level)
- **Exact edge logic:** println -&gt; L3 (Relational): the answer relates the parts (5 ways).

Ways (5), each with its exact rule:

- **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): System.out.println(s); is a statement, so its line of output appears at its own place in the sequence.
- **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): println("s") outputs exactly the characters between the quotes and then ends the line.
- **[2] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): print leaves the cursor on the line; println ends it; several prints followed by one println make one line.
- **[3] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): println prints numbers with all their digits and always ends the line; printf formats each value by its conversion code and ends the line only where the format has %n or \n.
- **[4] purpose\_of\_the\_whole** (rule type P, plan / role rule): Purpose: produce one complete line of output, e.g. each result on its own line, or end a line built with print.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for println: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

- **Edge:** `println` &rarr; `println@L4` (has_level)
- **Exact edge logic:** println -&gt; L4 (Extended abstract): the answer reasons beyond the given code (5 ways).

Ways (5), each with its exact rule:

- **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `PrintEqualsPrintln`: Replacing println with print joins the next output onto the same line (a typical logic error); the characters printed stay the same.
- **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Use println when each output item belongs on its own line or to end a line; use print to continue a line and printf to control number formatting.
- **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: Finish a line of print calls with println. Kind: silent logic error. Trigger class: output ends with print, so the last line may not be shown or runs into the shell prompt
- **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: Method names are case-sensitive. Kind: compile-time. Trigger class: System.out.Println or system.out.println: cannot find symbol
- **[4] diagnose\_an\_error** (rule type D, error rule): rule broken: Calls need parentheses. Kind: compile-time. Trigger class: System.out.println; without ()

## Same topic

`println` belongs to the topic **Understanding a program (HelloWorld)** (`topic1.1.b`). The topic also contains: `block`, `class_declaration`, `comment`, `main_method`, `print`, `program_layout`, `statement`, `string_literal`.

## Rules of the concept (21)

- **Book** (SW-1e, p. 7 (pdf 17)): "the second statement calls on System.out.println() to terminate the line."
- **Book** (OT-Hello, ): "uses the System class from the core library to print the "Hello World!" message to standard output."
- **Book** (API-PrintStream, ): "println(String x): Prints a String and then terminate the line. This method behaves as though it invokes print(String) and then println()."
- **E** (folk-meaning rule): Everyday reading: 'println' is just 'print', and 'new line' is something you do before writing. Java rule: println(x) prints x and then ends the line; println() alone just ends the line.
- **M** (wrong rule / right rule): IdentifierCaseInsensitive: wrong: System.out.Println and System.out.println name the same method. \| right: Java is case-sensitive: names that differ only in capitalization are different names.
- **M** (wrong rule / right rule): ParenthesesOnlyIfArgument: wrong: () are optional on a no-argument call like println. \| right: A method call always needs parentheses, so an empty line is printed with System.out.println();.
- **M** (wrong rule / right rule): PrintEqualsPrintln: wrong: print and println behave the same. \| right: println ends the line after printing and print does not, so print(s1); print(s2); puts s1 and s2 on the same line.
- **M** (wrong rule / right rule): PrintNewLineFirst: wrong: println(s) prints a newline and then s. \| right: println(s) prints s and then the line terminator.
- **T** (uneven-application rule): Applies the println rule (print, then end line) unevenly: puts the newline before the text on one call and after it on another, or forgets that the next output starts on a new line.
- **N** (identity rule): System.out.println is a library method that prints its argument followed by a line terminator ('print line').
- **S** (declarative rule): println(String x) behaves as though it calls print(x) and then println(); println() terminates the current line by writing the line separator string.
- **LT** (operational sequencing rule): Evaluate the argument, print its characters at the current position, then write the line separator so the cursor moves to the beginning of the next line.
- **OP** (evaluation / result rule): Output is the value's characters followed by a line break: println("Hello, "); println("World!"); prints two lines.
- **OS** (state-transition rule): One call appends the text and a line separator to the output; the cursor ends at the start of the next line; no variable changes and nothing is returned.
- **R** (composition rule (with a neighbour)): with statement: System.out.println(s); is a statement, so its line of output appears at its own place in the sequence.
- **R** (composition rule (with a neighbour)): with string\_literal: println("s") outputs exactly the characters between the quotes and then ends the line.
- **R** (composition rule (with a neighbour)): with print: print leaves the cursor on the line; println ends it; several prints followed by one println make one line.
- **R** (composition rule (with a neighbour)): with formatted\_output: println prints numbers with all their digits and always ends the line; printf formats each value by its conversion code and ends the line only where the format has %n or \n.
- **P** (plan / role rule): Purpose: produce one complete line of output, e.g. each result on its own line, or end a line built with print.
- **C** (conservation rule): Replacing println with print joins the next output onto the same line (a typical logic error); the characters printed stay the same.
- **D** (error rule): rule broken: Finish a line of print calls with println (silent logic error)
- **D** (error rule): rule broken: Method names are case-sensitive (compile-time)
- **D** (error rule): rule broken: Calls need parentheses (compile-time)
- **X** (applicability rule): Use println when each output item belongs on its own line or to end a line; use print to continue a line and printf to control number formatting.

## How it is found in code and answers (reader block)

- **Aliases:** println, print line, system.out.println, printline
- **Code patterns:** `System\.out\.println\s*\(`, `StdOut\.println\s*\(`, `System\.err\.println\s*\(`
- **Operator symbols:** none
- **Java types:** none

## The whole prerequisite chain

- **Everything it builds on (5):** `class_declaration`, `main_method`, `program_text`, `statement`, `string_literal`
- **Everything that builds on it (1):** `printing_array_reference`

## Every edge in this view and its exact edge logic (33)

All the edges drawn in the picture, in the order: prerequisite, parallel, misconception, error, has_level, contains.

**1. `println` &rarr; `printing_array_reference`** (prerequisite)

- **Exact edge logic:** println of an array variable prints the array's reference, not its elements.
- **Grounding:** book\_passage

**2. `statement` &rarr; `println`** (prerequisite)

- **Exact edge logic:** System.out.println(s); is itself a statement, so its line of output appears at its own place in the sequence.
- **Grounding:** book\_passage
- **Composition rule (R) of `statement` with `println`:** System.out.println(s); is a statement, so its line of output appears at its place in the sequence; swapping two println statements swaps the output lines.
- **Composition rule (R) of `println` with `statement`:** System.out.println(s); is a statement, so its line of output appears at its own place in the sequence.

**3. `string_literal` &rarr; `println`** (prerequisite)

- **Exact edge logic:** println("s") outputs exactly the characters between the quotes and then ends the line.
- **Grounding:** book\_passage
- **Composition rule (R) of `string_literal` with `println`:** println("s") outputs exactly the characters between the quotes and then ends the line.
- **Composition rule (R) of `println` with `string_literal`:** println("s") outputs exactly the characters between the quotes and then ends the line.

**4. `print` &harr; `println`** (parallel)

- **Exact edge logic:** print leaves the cursor on the same line after printing; println moves the cursor to the next line after printing.
- **Grounding:** book\_passage
- **Composition rule (R) of `print` with `println`:** print leaves the cursor on the same line; println ends the line; a line built from several prints should end with println.
- **Composition rule (R) of `println` with `print`:** print leaves the cursor on the line; println ends it; several prints followed by one println make one line.

**5. `println` &harr; `formatted_output`** (parallel)

- **Exact edge logic:** println prints each number with all its digits and ends the line; printf formats each value by its conversion code and starts a new line only when \n is in the format string.
- **Grounding:** book\_passage
- **Composition rule (R) of `println` with `formatted_output`:** println prints numbers with all their digits and always ends the line; printf formats each value by its conversion code and ends the line only where the format has %n or \n.
- **Composition rule (R) of `formatted_output` with `println`:** println prints a double with all its digits (about 15 places) and always ends the line. printf("%.2f\n", x) controls the digits and ends the line only because of \n.

**6. `println` &rarr; `IdentifierCaseInsensitive`** (misconception)

- **Exact edge logic (the wrong rule):** System.out.Println and System.out.println name the same method.
- **Twin logic (the right rule):** Java is case-sensitive: names of variables, methods and classes that differ only in capitalization are different names.
- **Role:** context

**7. `println` &rarr; `ParenthesesOnlyIfArgument`** (misconception)

- **Exact edge logic (the wrong rule):** println with nothing to print can be written System.out.println; without the parentheses.
- **Twin logic (the right rule):** A method call always needs parentheses, so an empty line is printed with System.out.println();.
- **Role:** context

**8. `println` &rarr; `PrintEqualsPrintln`** (misconception)

- **Exact edge logic (the wrong rule):** print and println do the same thing, so print(s1); print(s2); puts s1 and s2 on separate lines.
- **Twin logic (the right rule):** println ends the line after printing and print does not, so print(s1); print(s2); puts s1 and s2 on the same line.
- **Role:** primary

**9. `println` &rarr; `PrintNewLineFirst`** (misconception)

- **Exact edge logic (the wrong rule):** println(s) prints a newline and then s.
- **Twin logic (the right rule):** println(s) prints s and then the newline.
- **Role:** primary

**10. `println` &rarr; `PrintedTextIsExecuted`** (misconception)

- **Exact edge logic (the wrong rule):** System.out.println("x is 5"); sets x to 5 (text inside the quotes is run as code).
- **Twin logic (the right rule):** Characters inside double quotes are printed literally; println only displays them and changes no variable. Only an assignment such as x = 5; sets x.
- **Role:** primary

**11. `assignment` &rarr; `PrintedTextIsExecuted`** (misconception)

- **Exact edge logic (the wrong rule):** System.out.println("x is 5"); sets x to 5 (text inside the quotes is run as code).
- **Twin logic (the right rule):** Characters inside double quotes are printed literally; println only displays them and changes no variable. Only an assignment such as x = 5; sets x.
- **Role:** context

**12. `expression` &rarr; `ParenthesesOnlyIfArgument`** (misconception)

- **Exact edge logic (the wrong rule):** () are optional on a no-argument call like println
- **Twin logic (the right rule):** A method call always needs parentheses, so an empty line is printed with System.out.println();.
- **Role:** context

**13. `identifier` &rarr; `IdentifierCaseInsensitive`** (misconception)

- **Exact edge logic (the wrong rule):** System.out.Println and System.out.println name the same method.
- **Twin logic (the right rule):** Java is case-sensitive: names of variables, methods and classes that differ only in capitalization are different names.
- **Role:** primary

**14. `method_call` &rarr; `ParenthesesOnlyIfArgument`** (misconception)

- **Exact edge logic (the wrong rule):** () are optional on a no-argument call like println
- **Twin logic (the right rule):** A method call always needs parentheses, so an empty line is printed with System.out.println();.
- **Role:** primary

**15. `print` &rarr; `ParenthesesOnlyIfArgument`** (misconception)

- **Exact edge logic (the wrong rule):** println with nothing to print can be written System.out.println; without the parentheses.
- **Twin logic (the right rule):** A method call always needs parentheses, so an empty line is printed with System.out.println();.
- **Role:** context

**16. `standard_output` &rarr; `PrintEqualsPrintln`** (misconception)

- **Exact edge logic (the wrong rule):** print and println behave the same (no newline difference)
- **Twin logic (the right rule):** println ends the line after printing and print does not, so print(s1); print(s2); puts s1 and s2 on the same line.
- **Role:** context

**17. `string_literal` &rarr; `PrintedTextIsExecuted`** (misconception)

- **Exact edge logic (the wrong rule):** System.out.println("x is 5"); sets x to 5 (text inside the quotes is run as code).
- **Twin logic (the right rule):** Characters inside double quotes are printed literally; println only displays them and changes no variable. Only an assignment such as x = 5; sets x.
- **Role:** context

**18. `println` &rarr; `PrintWithoutFinalNewline`** (error)

- **Exact edge logic (the wrong rule):** Ends the output with print and expects it to appear right away.
- **Twin logic (the right rule):** Finish a line of print calls with println; some systems hold print output until a newline is printed.
- **Role:** context

**19. `print` &rarr; `PrintWithoutFinalNewline`** (error)

- **Exact edge logic (the wrong rule):** Ends the output with print and expects it to appear right away.
- **Twin logic (the right rule):** Finish a line of print calls with println; some systems hold print output until a newline is printed.
- **Role:** primary

**20. `println` &rarr; `println@L0`** (has_level)

- **Exact edge logic:** println -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (6 ways).
  - **[0] everyday\_reading** (rule type E, folk-meaning rule): Everyday reading: 'println' is just 'print', and 'new line' is something you do before writing. Java rule: println(x) prints x and then ends the line; println() alone just ends the line.
  - **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `PrintEqualsPrintln`: wrong rule: print and println behave the same. Right rule: println ends the line after printing and print does not, so print(s1); print(s2); puts s1 and s2 on the same line.
  - **[2] misconception** (rule type M, wrong rule / right rule) &rarr; `PrintNewLineFirst`: wrong rule: println(s) prints a newline and then s. Right rule: println(s) prints s and then the line terminator.
  - **[3] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `PrintEqualsPrintln`: Applies the println rule (print, then end line) unevenly: puts the newline before the text on one call and after it on another, or forgets that the next output starts on a new line. (here mixing in: "print and println behave the same (no newline difference)")
  - **[4] misconception** (rule type M, wrong rule / right rule) &rarr; `IdentifierCaseInsensitive`: wrong rule: System.out.Println and System.out.println name the same method. Right rule: Java is case-sensitive: names that differ only in capitalization are different names.
  - **[5] misconception** (rule type M, wrong rule / right rule) &rarr; `ParenthesesOnlyIfArgument`: wrong rule: () are optional on a no-argument call like println. Right rule: A method call always needs parentheses, so an empty line is printed with System.out.println();.

**21. `println` &rarr; `println@L1`** (has_level)

- **Exact edge logic:** println -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).
  - **[0] names\_the\_element** (rule type N, identity rule): System.out.println is a library method that prints its argument followed by a line terminator ('print line').
  - **[1] states\_the\_rule** (rule type S, declarative rule): println(String x) behaves as though it calls print(x) and then println(); println() terminates the current line by writing the line separator string.

**22. `println` &rarr; `println@L2`** (has_level)

- **Exact edge logic:** println -&gt; L2 (Multistructural): the answer applies the rules of println to every part of the code, in order (3 ways).
  - **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): Evaluate the argument, print its characters at the current position, then write the line separator so the cursor moves to the beginning of the next line.
  - **[1] output\_prediction** (rule type OP, evaluation / result rule): Output is the value's characters followed by a line break: println("Hello, "); println("World!"); prints two lines.
  - **[2] one\_step\_execution** (rule type OS, state-transition rule): One call appends the text and a line separator to the output; the cursor ends at the start of the next line; no variable changes and nothing is returned.

**23. `println` &rarr; `println@L3`** (has_level)

- **Exact edge logic:** println -&gt; L3 (Relational): the answer relates the parts (5 ways).
  - **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): System.out.println(s); is a statement, so its line of output appears at its own place in the sequence.
  - **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): println("s") outputs exactly the characters between the quotes and then ends the line.
  - **[2] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): print leaves the cursor on the line; println ends it; several prints followed by one println make one line.
  - **[3] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): println prints numbers with all their digits and always ends the line; printf formats each value by its conversion code and ends the line only where the format has %n or \n.
  - **[4] purpose\_of\_the\_whole** (rule type P, plan / role rule): Purpose: produce one complete line of output, e.g. each result on its own line, or end a line built with print.

**24. `println` &rarr; `println@L4`** (has_level)

- **Exact edge logic:** println -&gt; L4 (Extended abstract): the answer reasons beyond the given code (5 ways).
  - **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `PrintEqualsPrintln`: Replacing println with print joins the next output onto the same line (a typical logic error); the characters printed stay the same.
  - **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Use println when each output item belongs on its own line or to end a line; use print to continue a line and printf to control number formatting.
  - **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: Finish a line of print calls with println. Kind: silent logic error. Trigger class: output ends with print, so the last line may not be shown or runs into the shell prompt
  - **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: Method names are case-sensitive. Kind: compile-time. Trigger class: System.out.Println or system.out.println: cannot find symbol
  - **[4] diagnose\_an\_error** (rule type D, error rule): rule broken: Calls need parentheses. Kind: compile-time. Trigger class: System.out.println; without ()

**25. `topic1.1.b` &rarr; `println`** (contains)

- topic `topic1.1.b` contains `println`

**26. `topic1.1.b` &rarr; `block`** (contains)

- topic `topic1.1.b` contains `block`

**27. `topic1.1.b` &rarr; `class_declaration`** (contains)

- topic `topic1.1.b` contains `class_declaration`

**28. `topic1.1.b` &rarr; `comment`** (contains)

- topic `topic1.1.b` contains `comment`

**29. `topic1.1.b` &rarr; `main_method`** (contains)

- topic `topic1.1.b` contains `main_method`

**30. `topic1.1.b` &rarr; `print`** (contains)

- topic `topic1.1.b` contains `print`

**31. `topic1.1.b` &rarr; `program_layout`** (contains)

- topic `topic1.1.b` contains `program_layout`

**32. `topic1.1.b` &rarr; `statement`** (contains)

- topic `topic1.1.b` contains `statement`

**33. `topic1.1.b` &rarr; `string_literal`** (contains)

- topic `topic1.1.b` contains `string_literal`
