# token_vs_line_input (`token_vs_line_input`)

reading tokens (readInt) versus whole lines (readLine)

Section 1.5 Input and Output, topic 1.5.c Standard input. From the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`).

![The knowledge graph around token_vs_line_input](token_vs_line_input.png)

## Concepts associated with token\_vs\_line\_input (7)

| Concept | Description | How it is associated |
| --- | --- | --- |
| **end\_of\_input** | StdIn.isEmpty() and the end-of-file keystroke | same topic (topic1.5.c) |
| **input\_format** | StdIn reads whitespace-separated tokens of the expected type | same topic (topic1.5.c) |
| **input\_validation** | checking the next input before reading it | same topic (topic1.5.c) |
| **interactive\_input** | the user's input can change the program's control flow while it runs | same topic (topic1.5.c) |
| **read\_loop\_idiom** | reading until end-of-input | same topic (topic1.5.c) |
| **sentinel\_loop** | reading until a special stop value (Rainfall problem) | same topic (topic1.5.c) |
| **standard\_input** | StdIn -- reading a stream of values | prerequisite of it (it needs this)<br>composition rule (R) with it<br>shares misconception NextLineAfterNextInt<br>same topic (topic1.5.c) |

## Every edge in this view and its full label (16)

| From | Edge | To | Full edge label |
| --- | --- | --- | --- |
| **standard\_input** | prerequisite | **token\_vs\_line\_input** | They are standard-input operations.<br>grounding: book\_passage<br>composition rule (R) of standard\_input with token\_vs\_line\_input: Token reads (readInt, readString) and line reads (readLine) share one position. A token read leaves the rest of its line for the next readLine, so it is best not to mix the two.<br>composition rule (R) of token\_vs\_line\_input with standard\_input: Both kinds of call share the single StdIn position, so a token read changes what the next readLine returns. Mixing them needs care. |
| **standard\_input** | misconception | **NextLineAfterNextInt** | **wrong rule:** A line read after a number read returns the next line typed.<br>**right rule:** The number read leaves the newline, so the line read returns "" unless the newline is consumed first.<br>role: context |
| **token\_vs\_line\_input** | misconception | **NextLineAfterNextInt** | **wrong rule:** A line read after a number read returns the next line typed.<br>**right rule:** The number read leaves the newline, so the line read returns "" unless the newline is consumed first.<br>role: primary |
| **token\_vs\_line\_input** | has\_level | **token\_vs\_line\_input@L0** | token vs line input -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (3 ways).<br>**[0] everyday\_reading** (E): Everyday 'read a line' means the next full line you see. readLine() returns the rest of the current line from the read position. A preceding readInt() stops right after the number, so the 'line' may be empty.<br>**[1] misconception** (M) &rarr; NextLineAfterNextInt: wrong rule: A line read after a number read returns the next line typed. Right rule: After readInt(), the position is just past the number. readLine() returns the rest of that line ("" if nothing follows) and consumes the line separator; a second readLine() is needed for the next line.<br>**[2] inconsistent\_trace** (T) &rarr; NextLineAfterNextInt: Points to LT (token reads stop after the token; readLine reads to the end of the current line). An uneven trace skips the leftover line separator after a token read on some passes. (here mixing in: "A line read after a number read returns the next line typed") |
| **token\_vs\_line\_input** | has\_level | **token\_vs\_line\_input@L1** | token vs line input -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).<br>**[0] names\_the\_element** (N): StdIn's read methods come in two categories: token-based (readInt, readDouble, readString, ... separated by whitespace) and line- or text-based (readLine, readAll).<br>**[1] states\_the\_rule** (S): A token is a maximal run of non-whitespace characters. readLine() reads and returns the rest of the line without its separator. It is best not to mix the two categories in one program. |
| **token\_vs\_line\_input** | has\_level | **token\_vs\_line\_input@L2** | token vs line input -&gt; L2 (Multistructural): the answer applies the rules of token vs line input to every part of the code, in order (3 ways).<br>**[0] line\_by\_line\_trace** (LT): A token read skips whitespace, including line breaks, before the token and stops immediately after it. readLine() collects characters from the current position up to the line separator, consumes the separator, and returns them without it.<br>**[1] output\_prediction** (OP): For input \`42\nhello world\n\`: readInt() gives 42, then readLine() gives "", then readLine() gives "hello world". readString() on \`hello world\` gives "hello".<br>**[2] one\_step\_execution** (OS): A token read advances past one token and leaves the line separator. A readLine() advances past exactly one line separator. Each returns what it consumed (minus the separator). |
| **token\_vs\_line\_input** | has\_level | **token\_vs\_line\_input@L3** | token vs line input -&gt; L3 (Relational): the answer relates the parts (2 ways).<br>**[0] relation\_to\_neighbour** (R): Both kinds of call share the single StdIn position, so a token read changes what the next readLine returns. Mixing them needs care.<br>**[1] purpose\_of\_the\_whole** (P): Token reads suit streams of numbers or words. Line reads suit line-structured records, e.g. a name with spaces followed by numbers on each line. |
| **token\_vs\_line\_input** | has\_level | **token\_vs\_line\_input@L4** | token vs line input -&gt; L4 (Extended abstract): the answer reasons beyond the given code (4 ways).<br>**[0] predict\_a\_change** (C) &rarr; NextLineAfterNextInt: Replacing line breaks with spaces in the input leaves every token read unchanged but changes what readLine returns.<br>**[1] transfer\_to\_a\_new\_program** (X): Use token reads when values are separated by arbitrary whitespace. Use readLine when line boundaries or spaces inside a value matter. Avoid mixing the two in one program.<br>**[2] diagnose\_an\_error** (D): rule broken: A token read leaves the rest of its line unread. Kind: silent logic error. Trigger class: readInt() followed by readLine() on line-per-record input: the line read returns "" and the records are shifted.<br>**[3] diagnose\_an\_error** (D): rule broken: Line reads must stop at end of input. Kind: run-time exception. Trigger class: Using the result of readLine() after the input is exhausted (no line left). |
| **topic1.5.c** | contains | **end\_of\_input** | topic topic1.5.c contains end\_of\_input |
| **topic1.5.c** | contains | **input\_format** | topic topic1.5.c contains input\_format |
| **topic1.5.c** | contains | **input\_validation** | topic topic1.5.c contains input\_validation |
| **topic1.5.c** | contains | **interactive\_input** | topic topic1.5.c contains interactive\_input |
| **topic1.5.c** | contains | **read\_loop\_idiom** | topic topic1.5.c contains read\_loop\_idiom |
| **topic1.5.c** | contains | **sentinel\_loop** | topic topic1.5.c contains sentinel\_loop |
| **topic1.5.c** | contains | **standard\_input** | topic topic1.5.c contains standard\_input |
| **topic1.5.c** | contains | **token\_vs\_line\_input** | topic topic1.5.c contains token\_vs\_line\_input |
