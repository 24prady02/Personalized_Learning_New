# program_layout (`program_layout`)

one statement per line and indentation that shows nesting

Section 1.1 Your First Program, topic 1.1.b Understanding a program (HelloWorld). From the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`).

![The knowledge graph around program_layout](program_layout.png)

## Concepts associated with program\_layout (10)

| Concept | Description | How it is associated |
| --- | --- | --- |
| **block** | { ... } grouping statements | prerequisite of it (it needs this)<br>composition rule (R) with it<br>shares misconception InconsistentIndentation<br>same topic (topic1.1.b) |
| **class\_declaration** | public class Name { ... } -- the outer container | same topic (topic1.1.b) |
| **comment** | // and /\* \*/ text that the compiler ignores | same topic (topic1.1.b) |
| **main\_method** | public static void main(String[] args) -- entry point | same topic (topic1.1.b) |
| **nested\_conditionals** | else-if chains and conditionals inside conditionals | shares misconception InconsistentIndentation |
| **nested\_loops** | a loop inside a loop | shares misconception InconsistentIndentation |
| **print** | System.out.print -- output with no newline | same topic (topic1.1.b) |
| **println** | System.out.println -- output with a trailing newline | same topic (topic1.1.b) |
| **statement** | one step, terminated by ;, executed in sequence | shares misconception WhitespaceIsSignificant<br>same topic (topic1.1.b) |
| **string\_literal** | "Hello, World" -- the text being printed | same topic (topic1.1.b) |

## Every edge in this view and its full label (21)

| From | Edge | To | Full edge label |
| --- | --- | --- | --- |
| **block** | prerequisite | **program\_layout** | Indentation makes the nesting of blocks visible, so the reader can see which statements belong to which block.<br>grounding: book\_passage<br>composition rule (R) of block with program\_layout: Indentation should show block nesting, but only braces define it; layout that disagrees with the braces misleads the reader, not the compiler.<br>composition rule (R) of program\_layout with block: Indentation should show which statements belong to which block; braces, not indentation, decide it, so wrong indentation misleads. |
| **block** | misconception | **InconsistentIndentation** | **wrong rule:** Indents nested blocks inconsistently, so the visual nesting differs from the real nesting.<br>**right rule:** Indent consistently, one level deeper for each nested block, so the layout shows the real nesting; the compiler ignores indentation.<br>role: context |
| **nested\_conditionals** | misconception | **InconsistentIndentation** | **wrong rule:** Indents nested blocks inconsistently, so the visual nesting differs from the real nesting.<br>**right rule:** Indent consistently, one level deeper for each nested block, so the layout shows the real nesting; the compiler ignores indentation.<br>role: context |
| **nested\_loops** | misconception | **InconsistentIndentation** | **wrong rule:** Indents nested blocks inconsistently, so the visual nesting differs from the real nesting.<br>**right rule:** Indent consistently, one level deeper for each nested block, so the layout shows the real nesting; the compiler ignores indentation.<br>role: context |
| **program\_layout** | misconception | **InconsistentIndentation** | **wrong rule:** Indents nested blocks inconsistently, so the visual nesting differs from the real nesting.<br>**right rule:** Indent consistently, one level deeper for each nested block, so the layout shows the real nesting; the compiler ignores indentation.<br>role: primary |
| **program\_layout** | misconception | **WhitespaceIsSignificant** | **wrong rule:** Line breaks and indentation change what the program does, so each statement must be on its own line.<br>**right rule:** Java compilers consider all whitespace in program text (outside quotation marks) to be equivalent; layout is for human readers.<br>role: primary |
| **statement** | misconception | **WhitespaceIsSignificant** | **wrong rule:** Line breaks and indentation change what the program does, so each statement must be on its own line.<br>**right rule:** Java compilers consider all whitespace in program text (outside quotation marks) to be equivalent; layout is for human readers.<br>role: context |
| **program\_layout** | has\_level | **program\_layout@L0** | program layout -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (3 ways).<br>**[0] everyday\_reading** (E): Everyday reading: as in poetry or Python, line breaks and indentation carry meaning. Java rule: the compiler treats all whitespace between tokens as equivalent; layout is for human readers only (some spaces separate words, e.g. public class).<br>**[1] misconception** (M) &rarr; WhitespaceIsSignificant: wrong rule: Line breaks and indentation change what the program does, so each statement must be on its own line. Right rule: Java compilers consider all whitespace in program text (outside quotation marks) to be equivalent; layout is for human readers.<br>**[2] inconsistent\_trace** (T) &rarr; WhitespaceIsSignificant: Applies the 'layout is ignored' rule unevenly: follows the braces on one trace but the indentation on another, e.g. treats a mis-indented line after a braceless if as part of the branch. (here mixing in: "Line breaks and indentation change what the program does, so each statement must be on its own line") |
| **program\_layout** | has\_level | **program\_layout@L1** | program layout -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).<br>**[0] names\_the\_element** (N): Program layout is the use of whitespace (one statement per line, indentation one level per nested block) to make program structure visible; it is a style convention, not syntax.<br>**[1] states\_the\_rule** (S): Whitespace is needed only to separate adjacent words; otherwise all whitespace is equivalent, so the whole HelloWorld program can be written on one line; by convention, indent consistently to show nesting. |
| **program\_layout** | has\_level | **program\_layout@L2** | program layout -&gt; L2 (Multistructural): the answer applies the rules of program layout to every part of the code, in order (3 ways).<br>**[0] line\_by\_line\_trace** (LT): Layout has no execution order of its own: execution follows statements and braces, regardless of lines and indentation.<br>**[1] output\_prediction** (OP): Changing layout produces the same program output; only whitespace inside string literals appears in the output.<br>**[2] one\_step\_execution** (OS): Re-formatting changes no state and no behaviour; it only changes how readable the text is. |
| **program\_layout** | has\_level | **program\_layout@L3** | program layout -&gt; L3 (Relational): the answer relates the parts (2 ways).<br>**[0] relation\_to\_neighbour** (R): Indentation should show which statements belong to which block; braces, not indentation, decide it, so wrong indentation misleads.<br>**[1] purpose\_of\_the\_whole** (P): Purpose: make the program's structure (or intended structure) apparent so it is easier to read and to find errors. |
| **program\_layout** | has\_level | **program\_layout@L4** | program layout -&gt; L4 (Extended abstract): the answer reasons beyond the given code (4 ways).<br>**[0] predict\_a\_change** (C) &rarr; WhitespaceIsSignificant: Re-indenting or re-wrapping lines (outside string literals) keeps behaviour; removing a needed space between words (publicclass) breaks compilation.<br>**[1] transfer\_to\_a\_new\_program** (X): Always use consistent indentation and one statement per line (an editor can auto-format); it matters most in nested code, and checking indentation helps spot syntax errors.<br>**[2] diagnose\_an\_error** (D): rule broken: Indentation does not create a block. Kind: silent logic error. Trigger class: a second statement indented under a braceless if or while, expected to be conditional or repeated<br>**[3] diagnose\_an\_error** (D): rule broken: Some spaces are required between words. Kind: compile-time. Trigger class: keywords run together, e.g. publicclassGoodbye |
| **topic1.1.b** | contains | **block** | topic topic1.1.b contains block |
| **topic1.1.b** | contains | **class\_declaration** | topic topic1.1.b contains class\_declaration |
| **topic1.1.b** | contains | **comment** | topic topic1.1.b contains comment |
| **topic1.1.b** | contains | **main\_method** | topic topic1.1.b contains main\_method |
| **topic1.1.b** | contains | **print** | topic topic1.1.b contains print |
| **topic1.1.b** | contains | **println** | topic topic1.1.b contains println |
| **topic1.1.b** | contains | **program\_layout** | topic topic1.1.b contains program\_layout |
| **topic1.1.b** | contains | **statement** | topic topic1.1.b contains statement |
| **topic1.1.b** | contains | **string\_literal** | topic topic1.1.b contains string\_literal |
