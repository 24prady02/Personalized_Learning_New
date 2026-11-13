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

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 33 edges around this concept, each explained in the graph's own words.

## What it needs first (2)

A prerequisite edge means the other concept has to be understood before `println`.

### `statement` comes before `println`

*one step, terminated by ;, executed in sequence*

System.out.println(s); is itself a statement, so its line of output appears at its own place in the sequence.

- **Grounding:** book passage
- **How `println` combines with `statement`:** System.out.println(s); is a statement, so its line of output appears at its own place in the sequence.
- **How `statement` combines with `println`:** System.out.println(s); is a statement, so its line of output appears at its place in the sequence; swapping two println statements swaps the output lines.

### `string_literal` comes before `println`

*"Hello, World" -- the text being printed*

println("s") outputs exactly the characters between the quotes and then ends the line.

- **Grounding:** book passage
- **How `println` combines with `string_literal`:** println("s") outputs exactly the characters between the quotes and then ends the line.
- **How `string_literal` combines with `println`:** println("s") outputs exactly the characters between the quotes and then ends the line.

## What it leads to (1)

These concepts need `println` first.

### `println` comes before `printing_array_reference`

*printing an array variable prints a reference, not the elements*

println of an array variable prints the array's reference, not its elements.

- **Grounding:** book passage

## Learned alongside (2)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

### `println` alongside `formatted_output`

*printf with a format string such as %d, %.2f, %s*

println prints each number with all its digits and ends the line; printf formats each value by its conversion code and starts a new line only when \n is in the format string.

- **Grounding:** book passage
- **How `println` combines with `formatted_output`:** println prints numbers with all their digits and always ends the line; printf formats each value by its conversion code and ends the line only where the format has %n or \n.
- **How `formatted_output` combines with `println`:** println prints a double with all its digits (about 15 places) and always ends the line. printf("%.2f\n", x) controls the digits and ends the line only because of \n.

### `println` alongside `print`

*System.out.print -- output with no newline*

print leaves the cursor on the same line after printing; println moves the cursor to the next line after printing.

- **Grounding:** book passage
- **How `println` combines with `print`:** print leaves the cursor on the line; println ends it; several prints followed by one println make one line.
- **How `print` combines with `println`:** print leaves the cursor on the same line; println ends the line; a line built from several prints should end with println.

## Misconceptions (5)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### IdentifierCaseInsensitive

- **Wrong rule:** System.out.Println and System.out.println name the same method.
- **Right rule:** Java is case-sensitive: names of variables, methods and classes that differ only in capitalization are different names.
- **Role of this concept:** context
- **Shows at level L0 as:** misconception: wrong rule: System.out.Println and System.out.println name the same method. Right rule: Java is case-sensitive: names that differ only in capitalization are different names.
- **Also an edge from `identifier`:** System.out.Println and System.out.println name the same method.

### ParenthesesOnlyIfArgument

- **Wrong rule:** println with nothing to print can be written System.out.println; without the parentheses.
- **Right rule:** A method call always needs parentheses, so an empty line is printed with System.out.println();.
- **Role of this concept:** context
- **Shows at level L0 as:** misconception: wrong rule: () are optional on a no-argument call like println. Right rule: A method call always needs parentheses, so an empty line is printed with System.out.println();.
- **Also an edge from `expression`:** () are optional on a no-argument call like println
- **Also an edge from `method_call`:** () are optional on a no-argument call like println
- **Also an edge from `print`:** println with nothing to print can be written System.out.println; without the parentheses.

### PrintEqualsPrintln

- **Wrong rule:** print and println do the same thing, so print(s1); print(s2); puts s1 and s2 on separate lines.
- **Right rule:** println ends the line after printing and print does not, so print(s1); print(s2); puts s1 and s2 on the same line.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: print and println behave the same. Right rule: println ends the line after printing and print does not, so print(s1); print(s2); puts s1 and s2 on the same line.
- **Shows at level L0 as:** inconsistent trace: Applies the println rule (print, then end line) unevenly: puts the newline before the text on one call and after it on another, or forgets that the next output starts on a new line. (here mixing in: "print and println behave the same (no newline difference)")
- **Also an edge from `standard_output`:** print and println behave the same (no newline difference)

### PrintNewLineFirst

- **Wrong rule:** println(s) prints a newline and then s.
- **Right rule:** println(s) prints s and then the newline.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: println(s) prints a newline and then s. Right rule: println(s) prints s and then the line terminator.

### PrintedTextIsExecuted

- **Wrong rule:** System.out.println("x is 5"); sets x to 5 (text inside the quotes is run as code).
- **Right rule:** Characters inside double quotes are printed literally; println only displays them and changes no variable. Only an assignment such as x = 5; sets x.
- **Role of this concept:** primary
- **Also an edge from `assignment`:** System.out.println("x is 5"); sets x to 5 (text inside the quotes is run as code).
- **Also an edge from `string_literal`:** System.out.println("x is 5"); sets x to 5 (text inside the quotes is run as code).

## Errors (1)

An error edge states the rule that gets broken in a program, and the right rule.

### PrintWithoutFinalNewline

- **Wrong rule:** Ends the output with print and expects it to appear right away.
- **Right rule:** Finish a line of print calls with println; some systems hold print output until a newline is printed.
- **Role of this concept:** context
- **Also an edge from `print`:** Ends the output with print and expects it to appear right away.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for println: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to println agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

println -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (6 ways).

- **everyday reading** (folk-meaning rule): Everyday reading: 'println' is just 'print', and 'new line' is something you do before writing. Java rule: println(x) prints x and then ends the line; println() alone just ends the line.
- **misconception** (wrong rule / right rule; shows `PrintEqualsPrintln`): wrong rule: print and println behave the same. Right rule: println ends the line after printing and print does not, so print(s1); print(s2); puts s1 and s2 on the same line.
- **misconception** (wrong rule / right rule; shows `PrintNewLineFirst`): wrong rule: println(s) prints a newline and then s. Right rule: println(s) prints s and then the line terminator.
- **inconsistent trace** (uneven-application rule; shows `PrintEqualsPrintln`): Applies the println rule (print, then end line) unevenly: puts the newline before the text on one call and after it on another, or forgets that the next output starts on a new line. (here mixing in: "print and println behave the same (no newline difference)")
- **misconception** (wrong rule / right rule; shows `IdentifierCaseInsensitive`): wrong rule: System.out.Println and System.out.println name the same method. Right rule: Java is case-sensitive: names that differ only in capitalization are different names.
- **misconception** (wrong rule / right rule; shows `ParenthesesOnlyIfArgument`): wrong rule: () are optional on a no-argument call like println. Right rule: A method call always needs parentheses, so an empty line is printed with System.out.println();.

### L1: Unistructural / atom x text surface

L1 for println: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

println -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

- **names the element** (identity rule): System.out.println is a library method that prints its argument followed by a line terminator ('print line').
- **states the rule** (declarative rule): println(String x) behaves as though it calls print(x) and then println(); println() terminates the current line by writing the line separator string.

### L2: Multistructural / block x execution / preoperational

L2 for println: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

println -&gt; L2 (Multistructural): the answer applies the rules of println to every part of the code, in order (3 ways).

- **line by line trace** (operational sequencing rule): Evaluate the argument, print its characters at the current position, then write the line separator so the cursor moves to the beginning of the next line.
- **output prediction** (evaluation / result rule): Output is the value's characters followed by a line break: println("Hello, "); println("World!"); prints two lines.
- **one step execution** (state-transition rule): One call appends the text and a line separator to the output; the cursor ends at the start of the next line; no variable changes and nothing is returned.

### L3: Relational / relations x function (concrete operational begins)

L3 for println: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

println -&gt; L3 (Relational): the answer relates the parts (5 ways).

- **relation to neighbour** (composition rule (with a neighbour)): System.out.println(s); is a statement, so its line of output appears at its own place in the sequence.
- **relation to neighbour** (composition rule (with a neighbour)): println("s") outputs exactly the characters between the quotes and then ends the line.
- **relation to neighbour** (composition rule (with a neighbour)): print leaves the cursor on the line; println ends it; several prints followed by one println make one line.
- **relation to neighbour** (composition rule (with a neighbour)): println prints numbers with all their digits and always ends the line; printf formats each value by its conversion code and ends the line only where the format has %n or \n.
- **purpose of the whole** (plan / role rule): Purpose: produce one complete line of output, e.g. each result on its own line, or end a line built with print.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for println: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

println -&gt; L4 (Extended abstract): the answer reasons beyond the given code (5 ways).

- **predict a change** (conservation rule; shows `PrintEqualsPrintln`): Replacing println with print joins the next output onto the same line (a typical logic error); the characters printed stay the same.
- **transfer to a new program** (applicability rule): Use println when each output item belongs on its own line or to end a line; use print to continue a line and printf to control number formatting.
- **diagnose an error** (error rule): rule broken: Finish a line of print calls with println. Kind: silent logic error. Trigger class: output ends with print, so the last line may not be shown or runs into the shell prompt
- **diagnose an error** (error rule): rule broken: Method names are case-sensitive. Kind: compile-time. Trigger class: System.out.Println or system.out.println: cannot find symbol
- **diagnose an error** (error rule): rule broken: Calls need parentheses. Kind: compile-time. Trigger class: System.out.println; without ()

## Same topic

`println` belongs to the topic **Understanding a program (HelloWorld)** (`topic1.1.b`). The topic also contains: `block`, `class_declaration`, `comment`, `main_method`, `print`, `program_layout`, `statement`, `string_literal`.

## Rules of the concept (21)

- **folk-meaning rule:** Everyday reading: 'println' is just 'print', and 'new line' is something you do before writing. Java rule: println(x) prints x and then ends the line; println() alone just ends the line.
- **wrong rule / right rule:** IdentifierCaseInsensitive: wrong: System.out.Println and System.out.println name the same method. \| right: Java is case-sensitive: names that differ only in capitalization are different names.
- **wrong rule / right rule:** ParenthesesOnlyIfArgument: wrong: () are optional on a no-argument call like println. \| right: A method call always needs parentheses, so an empty line is printed with System.out.println();.
- **wrong rule / right rule:** PrintEqualsPrintln: wrong: print and println behave the same. \| right: println ends the line after printing and print does not, so print(s1); print(s2); puts s1 and s2 on the same line.
- **wrong rule / right rule:** PrintNewLineFirst: wrong: println(s) prints a newline and then s. \| right: println(s) prints s and then the line terminator.
- **uneven-application rule:** Applies the println rule (print, then end line) unevenly: puts the newline before the text on one call and after it on another, or forgets that the next output starts on a new line.
- **identity rule:** System.out.println is a library method that prints its argument followed by a line terminator ('print line').
- **declarative rule:** println(String x) behaves as though it calls print(x) and then println(); println() terminates the current line by writing the line separator string.
- **operational sequencing rule:** Evaluate the argument, print its characters at the current position, then write the line separator so the cursor moves to the beginning of the next line.
- **evaluation / result rule:** Output is the value's characters followed by a line break: println("Hello, "); println("World!"); prints two lines.
- **state-transition rule:** One call appends the text and a line separator to the output; the cursor ends at the start of the next line; no variable changes and nothing is returned.
- **composition rule (with a neighbour):** with statement: System.out.println(s); is a statement, so its line of output appears at its own place in the sequence.
- **composition rule (with a neighbour):** with string\_literal: println("s") outputs exactly the characters between the quotes and then ends the line.
- **composition rule (with a neighbour):** with print: print leaves the cursor on the line; println ends it; several prints followed by one println make one line.
- **composition rule (with a neighbour):** with formatted\_output: println prints numbers with all their digits and always ends the line; printf formats each value by its conversion code and ends the line only where the format has %n or \n.
- **plan / role rule:** Purpose: produce one complete line of output, e.g. each result on its own line, or end a line built with print.
- **conservation rule:** Replacing println with print joins the next output onto the same line (a typical logic error); the characters printed stay the same.
- **error rule:** rule broken: Finish a line of print calls with println (silent logic error)
- **error rule:** rule broken: Method names are case-sensitive (compile-time)
- **error rule:** rule broken: Calls need parentheses (compile-time)
- **applicability rule:** Use println when each output item belongs on its own line or to end a line; use print to continue a line and printf to control number formatting.

## The whole prerequisite chain

- **Everything it builds on (5):** `class_declaration`, `main_method`, `program_text`, `statement`, `string_literal`
- **Everything that builds on it (1):** `printing_array_reference`
