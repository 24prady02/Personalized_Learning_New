# filter (`filter`)

a program that reads standard input and writes standard output

Section 1.5 Input and Output, topic 1.5.d Redirection and piping (filters). From the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`).

![The knowledge graph around filter](filter.png)

## Concepts associated with filter (6)

| Concept | Description | How it is associated |
| --- | --- | --- |
| **data\_driven\_code** | keeping data in files and writing programs that read it from standard input, so the data can change without changing the program | same topic (topic1.5.d) |
| **input\_validation** | checking the next input before reading it | shares error NegativeNotFiltered |
| **piping** | \| connects one program's output to another's input | prerequisite of it (it needs this)<br>composition rule (R) with it<br>shares misconception RedirectionIsArgument<br>same topic (topic1.5.d) |
| **redirection** | &lt; / &gt; send a file in/out as standard input/output | shares misconception RedirectionIsArgument<br>same topic (topic1.5.d) |
| **sentinel\_loop** | reading until a special stop value (Rainfall problem) | shares error NegativeNotFiltered |
| **standard\_input** | StdIn -- reading a stream of values | prerequisite of it (it needs this) |

## Every edge in this view and its full label (17)

| From | Edge | To | Full edge label |
| --- | --- | --- | --- |
| **piping** | prerequisite | **filter** | A filter converts a standard input stream to a standard output stream, and piping is the mechanism that connects filters together.<br>grounding: book\_passage<br>composition rule (R) of piping with filter: Filters are the components and the pipe is the connector: \`A \| F1 \| F2\` passes the stream through each filter in turn.<br>composition rule (R) of filter with piping: Piping connects filters: the output of one becomes the input of the next, so filters compose into pipelines (\`java RandomSeq 1000 \| more\`). |
| **standard\_input** | prerequisite | **filter** | A filter reads its data from standard input and writes what it keeps to standard output.<br>grounding: book\_passage |
| **filter** | misconception | **RedirectionIsArgument** | **wrong rule:** a redirected file shows up in args[]<br>**right rule:** With &lt; data.txt the operating system implements the standard input stream by reading from the file; the program just reads standard input and has no dependence on the source of the input stream.<br>role: context |
| **piping** | misconception | **RedirectionIsArgument** | **wrong rule:** a redirected file shows up in args[]<br>**right rule:** With &lt; data.txt the operating system implements the standard input stream by reading from the file; the program just reads standard input and has no dependence on the source of the input stream.<br>role: context |
| **redirection** | misconception | **RedirectionIsArgument** | **wrong rule:** java Prog &lt; in.txt puts the name in.txt into args[0].<br>**right rule:** With &lt; data.txt the operating system implements the standard input stream by reading from the file; the program just reads standard input and has no dependence on the source of the input stream.<br>role: primary |
| **filter** | error | **NegativeNotFiltered** | **wrong rule:** Adds negative rainfall values to the total.<br>**right rule:** Values outside the range of interest must be filtered out (for example with if (t &gt;= lo &amp;&amp; t &lt;= hi)) before they are processed.<br>role: context |
| **input\_validation** | error | **NegativeNotFiltered** | **wrong rule:** Adds negative rainfall values to the total.<br>**right rule:** Values outside the range of interest must be filtered out (for example with if (t &gt;= lo &amp;&amp; t &lt;= hi)) before they are processed.<br>role: context |
| **sentinel\_loop** | error | **NegativeNotFiltered** | **wrong rule:** Adds negative rainfall values to the total.<br>**right rule:** Values outside the range of interest must be filtered out (for example with if (t &gt;= lo &amp;&amp; t &lt;= hi)) before they are processed.<br>role: primary |
| **filter** | has\_level | **filter@L0** | filter -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (3 ways).<br>**[0] everyday\_reading** (E): An everyday filter (a coffee filter) removes things. In the UNIX sense a filter is any program that reads standard input and writes standard output, even one that removes nothing.<br>**[1] misconception** (M) &rarr; RedirectionIsArgument: wrong rule: The file a filter processes shows up in args[]. Right rule: A filter reads only standard input. The file or upstream program is attached by &lt; or \|, and args[] carries only parameters such as lo and hi.<br>**[2] inconsistent\_trace** (T) &rarr; RedirectionIsArgument: Points to LT (read one value, test it, maybe print it, repeat). An uneven trace prints out-of-range values on some passes, or holds all the output until the end. (here mixing in: "a redirected file shows up in args[]") |
| **filter** | has\_level | **filter@L1** | filter -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).<br>**[0] names\_the\_element** (N): A filter is a program that converts a standard input stream into a standard output stream.<br>**[1] states\_the\_rule** (S): A filter reads from standard input and writes to standard output, classically writing a subsequence of its input (e.g. RangeFilter keeps the values between lo and hi). |
| **filter** | has\_level | **filter@L2** | filter -&gt; L2 (Multistructural): the answer applies the rules of filter to every part of the code, in order (3 ways).<br>**[0] line\_by\_line\_trace** (LT): Each pass of while (!StdIn.isEmpty()) reads one value t, tests lo &lt;= t &lt;= hi, and prints t right away if the test passes. Output is produced while input is still being read.<br>**[1] output\_prediction** (OP): \`java RangeFilter 100 400\` with input 358 1330 55 165 689 1014 3066 387 575 843 203 48 292 877 65 998 prints 358 165 387 203 292: the in-range values, in their original order.<br>**[2] one\_step\_execution** (OS): One pass reads one value and appends it to the output only if it passes the test. lo and hi do not change. |
| **filter** | has\_level | **filter@L3** | filter -&gt; L3 (Relational): the answer relates the parts (2 ways).<br>**[0] relation\_to\_neighbour** (R): Piping connects filters: the output of one becomes the input of the next, so filters compose into pipelines (\`java RandomSeq 1000 \| more\`).<br>**[1] purpose\_of\_the\_whole** (P): Plan: the stream filter, a one-pass read-test-print loop that uses only a fixed number of variables. The value read is a most-recent holder and lo and hi are fixed values. |
| **filter** | has\_level | **filter@L4** | filter -&gt; L4 (Extended abstract): the answer reasons beyond the given code (3 ways).<br>**[0] predict\_a\_change** (C) &rarr; RedirectionIsArgument: A filter keeps the relative order of the values it passes (it outputs a subsequence). Filters can be chained in any number without changing each other.<br>**[1] transfer\_to\_a\_new\_program** (X): A filter is the right tool when each output depends only on the current value, or on a fixed amount of state. Tasks that need all the values (sorting, k-th smallest, percentage above the mean) must store them in an array first.<br>**[2] diagnose\_an\_error** (D): rule broken: Every value must pass the range test before it is output or processed. Kind: silent logic error. Trigger class: Values outside lo..hi (e.g. negatives) are output because the test is missing or uses the wrong bounds or operators. |
| **topic1.5.d** | contains | **data\_driven\_code** | topic topic1.5.d contains data\_driven\_code |
| **topic1.5.d** | contains | **filter** | topic topic1.5.d contains filter |
| **topic1.5.d** | contains | **piping** | topic topic1.5.d contains piping |
| **topic1.5.d** | contains | **redirection** | topic topic1.5.d contains redirection |
