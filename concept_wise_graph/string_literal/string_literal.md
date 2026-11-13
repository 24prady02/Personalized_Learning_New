# string_literal (`string_literal`)

"Hello, World" -- the text being printed

Section 1.1 Your First Program, topic 1.1.b Understanding a program (HelloWorld). From the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`).

![The knowledge graph around string_literal](string_literal.png)

## Concepts associated with string\_literal (11)

| Concept | Description | How it is associated |
| --- | --- | --- |
| **assignment** | = stores the computed value of the right side | shares misconception PrintedTextIsExecuted |
| **block** | { ... } grouping statements | same topic (topic1.1.b) |
| **class\_declaration** | public class Name { ... } -- the outer container | same topic (topic1.1.b) |
| **comment** | // and /\* \*/ text that the compiler ignores | same topic (topic1.1.b) |
| **compile\_time\_error** | an error javac reports before the program can run (syntax, types) | shares error UnclosedStringLiteral |
| **escape\_sequences** | backslash codes inside literals: '\t' tab, '\n' newline | builds on it (needs it)<br>composition rule (R) with it |
| **main\_method** | public static void main(String[] args) -- entry point | same topic (topic1.1.b) |
| **print** | System.out.print -- output with no newline | builds on it (needs it)<br>composition rule (R) with it<br>same topic (topic1.1.b) |
| **println** | System.out.println -- output with a trailing newline | builds on it (needs it)<br>composition rule (R) with it<br>shares misconception PrintedTextIsExecuted<br>same topic (topic1.1.b) |
| **program\_layout** | one statement per line and indentation that shows nesting | same topic (topic1.1.b) |
| **statement** | one step, terminated by ;, executed in sequence | same topic (topic1.1.b) |

## Every edge in this view and its full label (24)

| From | Edge | To | Full edge label |
| --- | --- | --- | --- |
| **string\_literal** | prerequisite | **escape\_sequences** | Escape sequences are written inside string or char literals.<br>grounding: book\_passage<br>composition rule (R) of string\_literal with escape\_sequences: Escape sequences (\n, \t, \", \\) are written inside string or char literals to stand for one character that cannot be typed directly.<br>composition rule (R) of escape\_sequences with string\_literal: Escapes are written inside "..." or '...'. \" puts a double quote inside a String literal without ending it. |
| **string\_literal** | prerequisite | **print** | print("s") outputs exactly the characters between the quotes, without the quotes.<br>grounding: book\_passage<br>composition rule (R) of string\_literal with print: print("s") outputs exactly the characters between the quotes, without the quotes.<br>composition rule (R) of print with string\_literal: print("s") outputs exactly the characters between the quotes, without the quotes; spaces inside the quotes are printed. |
| **string\_literal** | prerequisite | **println** | println("s") outputs exactly the characters between the quotes and then ends the line.<br>grounding: book\_passage<br>composition rule (R) of string\_literal with println: println("s") outputs exactly the characters between the quotes and then ends the line.<br>composition rule (R) of println with string\_literal: println("s") outputs exactly the characters between the quotes and then ends the line. |
| **assignment** | misconception | **PrintedTextIsExecuted** | **wrong rule:** System.out.println("x is 5"); sets x to 5 (text inside the quotes is run as code).<br>**right rule:** Characters inside double quotes are printed literally; println only displays them and changes no variable. Only an assignment such as x = 5; sets x.<br>role: context |
| **println** | misconception | **PrintedTextIsExecuted** | **wrong rule:** System.out.println("x is 5"); sets x to 5 (text inside the quotes is run as code).<br>**right rule:** Characters inside double quotes are printed literally; println only displays them and changes no variable. Only an assignment such as x = 5; sets x.<br>role: primary |
| **string\_literal** | misconception | **PrintedTextIsExecuted** | **wrong rule:** System.out.println("x is 5"); sets x to 5 (text inside the quotes is run as code).<br>**right rule:** Characters inside double quotes are printed literally; println only displays them and changes no variable. Only an assignment such as x = 5; sets x.<br>role: context |
| **compile\_time\_error** | error | **UnclosedStringLiteral** | **wrong rule:** A string literal can be left without its closing quote.<br>**right rule:** A String literal is enclosed in a pair of double quotes.<br>role: context |
| **string\_literal** | error | **SingleQuotedString** | **wrong rule:** Writes a string literal in single quotes: 'Hello'.<br>**right rule:** String literals use double quotes; single quotes are for one char.<br>role: primary |
| **string\_literal** | error | **StringLiteralSpansLines** | **wrong rule:** Breaks a string literal across two lines of code.<br>**right rule:** String literals must not span more than one line of a program.<br>role: primary |
| **string\_literal** | error | **UnclosedStringLiteral** | **wrong rule:** A string literal can be left without its closing quote.<br>**right rule:** A String literal is enclosed in a pair of double quotes.<br>role: primary |
| **string\_literal** | has\_level | **string\_literal@L0** | string literal -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (1 way).<br>**[0] everyday\_reading** (E): Everyday reading: quotation marks are just decoration, and spacing inside them is tidied up like ordinary text; single and double quotes mean the same thing. Java rule: characters within double quotes are taken literally (every space counts), the quotes are not part of the value, and single quotes are for one char. |
| **string\_literal** | has\_level | **string\_literal@L1** | string literal -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).<br>**[0] names\_the\_element** (N): A string literal is a sequence of characters written in double quotes in the source code, e.g. "Hello, World"; it is a value of type String.<br>**[1] states\_the\_rule** (S): A String literal is enclosed in a pair of double quotes; everything inside is taken literally, special characters such as " and newline are written with escape sequences, and the literal must close on the same source line. |
| **string\_literal** | has\_level | **string\_literal@L2** | string literal -&gt; L2 (Multistructural): the answer applies the rules of string literal to every part of the code, in order (3 ways).<br>**[0] line\_by\_line\_trace** (LT): The literal is a constant: it is fixed at compile time and simply supplies its value when the expression containing it is evaluated.<br>**[1] output\_prediction** (OP): Value is the String of the characters between the quotes (escape sequences replaced by the characters they stand for), without the quotes: "Hi, " has 4 characters, and printing it shows Hi, followed by a space.<br>**[2] one\_step\_execution** (OS): Evaluating a literal changes no state; it just yields the same String value every time. |
| **string\_literal** | has\_level | **string\_literal@L3** | string literal -&gt; L3 (Relational): the answer relates the parts (4 ways).<br>**[0] relation\_to\_neighbour** (R): print("s") outputs exactly the characters between the quotes, without the quotes.<br>**[1] relation\_to\_neighbour** (R): println("s") outputs exactly the characters between the quotes and then ends the line.<br>**[2] relation\_to\_neighbour** (R): Escape sequences (\n, \t, \", \\) are written inside string or char literals to stand for one character that cannot be typed directly.<br>**[3] purpose\_of\_the\_whole** (P): Purpose: state fixed text exactly, such as messages, labels and prompts, so you can precisely specify what gets printed. |
| **string\_literal** | has\_level | **string\_literal@L4** | string literal -&gt; L4 (Extended abstract): the answer reasons beyond the given code (6 ways).<br>**[0] predict\_a\_change** (C): Changing any character inside the quotes (including adding a space) changes the output by exactly that character; changing spaces outside the quotes changes nothing.<br>**[1] diagnose\_an\_error** (D): rule broken: A String literal is enclosed in a pair of double quotes. Kind: compile-time. Trigger class: a missing closing (or opening) quote; the compiler may get very confused and report errors elsewhere<br>**[2] diagnose\_an\_error** (D): rule broken: String literals use double quotes; single quotes are for one char. Kind: compile-time. Trigger class: 'Hello' (more than one character in single quotes): unclosed character literal<br>**[3] diagnose\_an\_error** (D): rule broken: A string literal must not span source lines. Kind: compile-time. Trigger class: a line break inside "...": unclosed string literal<br>**[4] transfer\_to\_a\_new\_program** (X): Use a string literal for fixed text known when the program is written; use args, input or variables for text that varies between runs, and char literals for a single character.<br>**[5] diagnose\_an\_error** (D): rule broken: A double quote inside a string must be escaped. Kind: compile-time. Trigger class: "She said "Hi"" without \" |
| **topic1.1.b** | contains | **block** | topic topic1.1.b contains block |
| **topic1.1.b** | contains | **class\_declaration** | topic topic1.1.b contains class\_declaration |
| **topic1.1.b** | contains | **comment** | topic topic1.1.b contains comment |
| **topic1.1.b** | contains | **main\_method** | topic topic1.1.b contains main\_method |
| **topic1.1.b** | contains | **print** | topic topic1.1.b contains print |
| **topic1.1.b** | contains | **println** | topic topic1.1.b contains println |
| **topic1.1.b** | contains | **program\_layout** | topic topic1.1.b contains program\_layout |
| **topic1.1.b** | contains | **statement** | topic topic1.1.b contains statement |
| **topic1.1.b** | contains | **string\_literal** | topic topic1.1.b contains string\_literal |
