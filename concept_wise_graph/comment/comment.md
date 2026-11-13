# comment (`comment`)

// and /\* \*/ text that the compiler ignores

Section 1.1 Your First Program, topic 1.1.b Understanding a program (HelloWorld). From the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`).

![The knowledge graph around comment](comment.png)

## Concepts associated with comment (10)

| Concept | Description | How it is associated |
| --- | --- | --- |
| **block** | { ... } grouping statements | same topic (topic1.1.b) |
| **class\_declaration** | public class Name { ... } -- the outer container | same topic (topic1.1.b) |
| **compile\_time\_error** | an error javac reports before the program can run (syntax, types) | shares error UnclosedComment |
| **main\_method** | public static void main(String[] args) -- entry point | same topic (topic1.1.b) |
| **print** | System.out.print -- output with no newline | same topic (topic1.1.b) |
| **println** | System.out.println -- output with a trailing newline | same topic (topic1.1.b) |
| **program\_layout** | one statement per line and indentation that shows nesting | same topic (topic1.1.b) |
| **program\_text** | the source file; class name must match the filename | prerequisite of it (it needs this)<br>composition rule (R) with it |
| **statement** | one step, terminated by ;, executed in sequence | same topic (topic1.1.b) |
| **string\_literal** | "Hello, World" -- the text being printed | same topic (topic1.1.b) |

## Every edge in this view and its full label (19)

| From | Edge | To | Full edge label |
| --- | --- | --- | --- |
| **program\_text** | prerequisite | **comment** | Comments are part of the program text in Name.java but are ignored when it is compiled.<br>grounding: book\_passage<br>composition rule (R) of program\_text with comment: Comments are part of the program text but are discarded when it is compiled: they may appear anywhere a whitespace may appear and never change Name.class's behaviour.<br>composition rule (R) of comment with program\_text: Comments are part of the program text in Name.java but are dropped when it is compiled, so they cannot affect Name.class's behaviour. |
| **comment** | misconception | **CommentIsExecuted** | **wrong rule:** A comment line is run like a statement.<br>**right rule:** The compiler ignores comments: everything from // to the end of the line and everything between /\* and \*/.<br>role: primary |
| **comment** | error | **SpacedCommentDelimiter** | **wrong rule:** Writes / \* comment \* / with spaces inside the delimiters.<br>**right rule:** The delimiters /\* and \*/ must be written without spaces.<br>role: primary |
| **comment** | error | **UnclosedComment** | **wrong rule:** Opens a comment with /\* and never closes it.<br>**right rule:** A /\* comment is the text between /\* and \*/, so the closing \*/ is required.<br>role: primary |
| **compile\_time\_error** | error | **UnclosedComment** | **wrong rule:** Opens a comment with /\* and never closes it.<br>**right rule:** A /\* comment is the text between /\* and \*/, so the closing \*/ is required.<br>role: context |
| **comment** | has\_level | **comment@L0** | comment -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (3 ways).<br>**[0] everyday\_reading** (E): Everyday reading: text written in a program is an instruction the computer reads and obeys. Java rule: comments (// to end of line, /\* ... \*/) are ignored by the compiler and have no effect on execution; they are for human readers.<br>**[1] misconception** (M) &rarr; CommentIsExecuted: wrong rule: A comment line is run like a statement. Right rule: The compiler ignores comments: everything from // to the end of the line and everything between /\* and \*/.<br>**[2] inconsistent\_trace** (T) &rarr; CommentIsExecuted: Applies the skip rule unevenly: skips one comment while tracing but 'executes' another (e.g. a commented-out println), or forgets that // ends at the line break. (here mixing in: "A comment line is run like a statement") |
| **comment** | has\_level | **comment@L1** | comment -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).<br>**[0] names\_the\_element** (N): A comment is explanatory text in the program that the compiler ignores.<br>**[1] states\_the\_rule** (S): A comment is either text between /\* and \*/ or text from // to the end of the line; the compiler ignores it. A comment that starts with /\*\* is a documentation (Javadoc) comment, written before a class or method; tools turn it into API documentation. |
| **comment** | has\_level | **comment@L2** | comment -&gt; L2 (Multistructural): the answer applies the rules of comment to every part of the code, in order (3 ways).<br>**[0] line\_by\_line\_trace** (LT): Comments are removed when the source is read by the compiler, so they never take part in execution order; tracing skips them.<br>**[1] output\_prediction** (OP): A comment produces no value and no output.<br>**[2] one\_step\_execution** (OS): A comment changes no state; adding one and recompiling leaves the program's behaviour identical. |
| **comment** | has\_level | **comment@L3** | comment -&gt; L3 (Relational): the answer relates the parts (2 ways).<br>**[0] relation\_to\_neighbour** (R): Comments are part of the program text in Name.java but are dropped when it is compiled, so they cannot affect Name.class's behaviour.<br>**[1] purpose\_of\_the\_whole** (P): Purpose: explain what the code does and why, for other programmers and your future self; also used to disable code temporarily. |
| **comment** | has\_level | **comment@L4** | comment -&gt; L4 (Extended abstract): the answer reasons beyond the given code (4 ways).<br>**[0] predict\_a\_change** (C) &rarr; CommentIsExecuted: Adding, removing or editing a comment keeps behaviour unchanged, as long as the delimiters stay intact; deleting a closing \*/ or turning a statement into a comment changes the program.<br>**[1] diagnose\_an\_error** (D): rule broken: A /\* comment needs its closing \*/. Kind: compile-time. Trigger class: a /\* with no matching \*/: the rest of the file becomes comment, so javac reports an unclosed comment or reached end of file<br>**[2] diagnose\_an\_error** (D): rule broken: /\* and \*/ are two-character tokens with no space inside. Kind: compile-time. Trigger class: writing / \* ... \* /: the slashes and stars are read as operators, producing syntax errors<br>**[3] transfer\_to\_a\_new\_program** (X): Use comments to document intent where the code alone is unclear; do not rely on them to change what the program does, and keep them in step with the code. |
| **topic1.1.b** | contains | **block** | topic topic1.1.b contains block |
| **topic1.1.b** | contains | **class\_declaration** | topic topic1.1.b contains class\_declaration |
| **topic1.1.b** | contains | **comment** | topic topic1.1.b contains comment |
| **topic1.1.b** | contains | **main\_method** | topic topic1.1.b contains main\_method |
| **topic1.1.b** | contains | **print** | topic topic1.1.b contains print |
| **topic1.1.b** | contains | **println** | topic topic1.1.b contains println |
| **topic1.1.b** | contains | **program\_layout** | topic topic1.1.b contains program\_layout |
| **topic1.1.b** | contains | **statement** | topic topic1.1.b contains statement |
| **topic1.1.b** | contains | **string\_literal** | topic topic1.1.b contains string\_literal |
