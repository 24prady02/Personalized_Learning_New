# end_of_input (`end_of_input`)

StdIn.isEmpty() and the end-of-file keystroke

Section 1.5 Input and Output, topic 1.5.c Standard input. From the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`).

![The knowledge graph around end_of_input](end_of_input.png)

## Concepts associated with end\_of\_input (7)

| Concept | Description | How it is associated |
| --- | --- | --- |
| **input\_format** | StdIn reads whitespace-separated tokens of the expected type | same topic (topic1.5.c) |
| **input\_validation** | checking the next input before reading it | same topic (topic1.5.c) |
| **interactive\_input** | the user's input can change the program's control flow while it runs | same topic (topic1.5.c) |
| **read\_loop\_idiom** | reading until end-of-input | prerequisite of it (it needs this)<br>composition rule (R) with it<br>shares error ReadPastEndOfInput<br>same topic (topic1.5.c) |
| **sentinel\_loop** | reading until a special stop value (Rainfall problem) | same topic (topic1.5.c) |
| **standard\_input** | StdIn -- reading a stream of values | shares error ReadPastEndOfInput<br>same topic (topic1.5.c) |
| **token\_vs\_line\_input** | reading tokens (readInt) versus whole lines (readLine) | same topic (topic1.5.c) |

## Every edge in this view and its full label (18)

| From | Edge | To | Full edge label |
| --- | --- | --- | --- |
| **read\_loop\_idiom** | prerequisite | **end\_of\_input** | The read loop runs until StdIn.isEmpty() returns true, which happens when the user types the end-of-file sequence (&lt;ctrl-d&gt;).<br>grounding: book\_passage<br>composition rule (R) of read\_loop\_idiom with end\_of\_input: The loop ends only when isEmpty() becomes true: at the end of a redirected file, or after the end-of-file keystroke (&lt;ctrl-d&gt;, or &lt;ctrl-z&gt; on some systems).<br>composition rule (R) of end\_of\_input with read\_loop\_idiom: isEmpty() is the condition of the read loop, so the loop ends exactly when end-of-file is reached (&lt;ctrl-d&gt; at the keyboard, end of file with &lt;). |
| **end\_of\_input** | misconception | **IsEmptyMeansBlankLine** | **wrong rule:** StdIn.isEmpty() becomes true when the user presses Enter on an empty line.<br>**right rule:** isEmpty() is true only when no more values remain: at the end of a redirected file, or after the end-of-file sequence (&lt;ctrl-d&gt;, or &lt;ctrl-z&gt; on some systems, on a line by itself) is typed; an empty line is just whitespace.<br>role: primary |
| **end\_of\_input** | error | **ReadPastEndOfInput** | **wrong rule:** Calls StdIn.readInt() again after the input has run out.<br>**right rule:** Reading after standard input is exhausted is a run-time error; test StdIn.isEmpty() before each read.<br>role: primary |
| **read\_loop\_idiom** | error | **ReadPastEndOfInput** | **wrong rule:** Calls StdIn.readInt() again after the input has run out.<br>**right rule:** Reading after standard input is exhausted is a run-time error; test StdIn.isEmpty() before each read.<br>role: context |
| **standard\_input** | error | **ReadPastEndOfInput** | **wrong rule:** Calls StdIn.readInt() again after the input has run out.<br>**right rule:** Reading after standard input is exhausted is a run-time error; test StdIn.isEmpty() before each read.<br>role: context |
| **end\_of\_input** | has\_level | **end\_of\_input@L0** | end of input -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (3 ways).<br>**[0] everyday\_reading** (E): Everyday 'empty' and 'done' suggest that a blank line, or pressing Enter, ends the input. For StdIn, a blank line is only whitespace: input ends only when the end-of-file signal arrives.<br>**[1] misconception** (M) &rarr; IsEmptyMeansBlankLine: wrong rule: StdIn.isEmpty() becomes true when the user presses Enter on an empty line. Right rule: isEmpty() is true only when no tokens remain: at the end of a redirected file, or after the end-of-file sequence (&lt;ctrl-d&gt;, or &lt;ctrl-z&gt; on some systems, on a line by itself). An empty line is just whitespace.<br>**[2] inconsistent\_trace** (T) &rarr; IsEmptyMeansBlankLine: Points to LT (isEmpty() waits until it can decide; it returns true only after end-of-file). An uneven trace ends the loop at a blank line on some passes, or counts the end-of-file keystroke as a value. (here mixing in: "StdIn.isEmpty() becomes true when the user presses Enter on an empty line") |
| **end\_of\_input** | has\_level | **end\_of\_input@L1** | end of input -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).<br>**[0] names\_the\_element** (N): End of input is the end-of-file condition of the input stream. Typing the end-of-file sequence or reaching the end of a redirected file signals it, and StdIn.isEmpty() tests it.<br>**[1] states\_the\_rule** (S): isEmpty() returns true if standard input has no more values (only whitespace may be left). At a terminal the book signals the end with &lt;ctrl-d&gt;; the other widely used convention is &lt;ctrl-z&gt;. |
| **end\_of\_input** | has\_level | **end\_of\_input@L2** | end of input -&gt; L2 (Multistructural): the answer applies the rules of end of input to every part of the code, in order (3 ways).<br>**[0] line\_by\_line\_trace** (LT): When isEmpty() is called at a terminal, it blocks until a token arrives (it returns false) or the end-of-file sequence is typed (it returns true). With a redirected file, it returns true right after the last token.<br>**[1] output\_prediction** (OP): isEmpty() returns a boolean: true if there are no more values, false otherwise.<br>**[2] one\_step\_execution** (OS): isEmpty() consumes no value (at most it skips whitespace) and returns a boolean. Only the read that follows advances past a token. |
| **end\_of\_input** | has\_level | **end\_of\_input@L3** | end of input -&gt; L3 (Relational): the answer relates the parts (2 ways).<br>**[0] relation\_to\_neighbour** (R): isEmpty() is the condition of the read loop, so the loop ends exactly when end-of-file is reached (&lt;ctrl-d&gt; at the keyboard, end of file with &lt;).<br>**[1] purpose\_of\_the\_whole** (P): Role: the termination signal of a process-until-done loop, used when the amount of data is unknown. |
| **end\_of\_input** | has\_level | **end\_of\_input@L4** | end of input -&gt; L4 (Extended abstract): the answer reasons beyond the given code (4 ways).<br>**[0] predict\_a\_change** (C) &rarr; IsEmptyMeansBlankLine: Adding blank lines or trailing spaces at the end of the input keeps isEmpty()'s answer (still true at the end). Adding any token changes it.<br>**[1] diagnose\_an\_error** (D): rule broken: Reading after the stream is exhausted is an error. Test isEmpty() first. Kind: run-time exception. Trigger class: Any read after the end-of-file signal or after the last token of the file.<br>**[2] transfer\_to\_a\_new\_program** (X): Ending on end-of-file is right when data come from a file or a pipe, or the count is unknown. For human typists a count or a sentinel can be clearer, because the end-of-file key differs between systems.<br>**[3] diagnose\_an\_error** (D): rule broken: The end must be signalled with the system's end-of-file key. Kind: silent logic error. Trigger class: At a terminal the user presses Enter, or uses the other system's key, so isEmpty() keeps waiting and the program seems to hang. |
| **topic1.5.c** | contains | **end\_of\_input** | topic topic1.5.c contains end\_of\_input |
| **topic1.5.c** | contains | **input\_format** | topic topic1.5.c contains input\_format |
| **topic1.5.c** | contains | **input\_validation** | topic topic1.5.c contains input\_validation |
| **topic1.5.c** | contains | **interactive\_input** | topic topic1.5.c contains interactive\_input |
| **topic1.5.c** | contains | **read\_loop\_idiom** | topic topic1.5.c contains read\_loop\_idiom |
| **topic1.5.c** | contains | **sentinel\_loop** | topic topic1.5.c contains sentinel\_loop |
| **topic1.5.c** | contains | **standard\_input** | topic topic1.5.c contains standard\_input |
| **topic1.5.c** | contains | **token\_vs\_line\_input** | topic topic1.5.c contains token\_vs\_line\_input |
