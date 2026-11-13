# Trace (table of variable values) (`program_trace`)

a table of the values of the variables after each statement, used to check what code does

Section 1.2 1.2 Built-in Types of Data, topic 1.2.a Data types and terminology (literals, identifiers, variables, declarations, assignment, expressions). From the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`).

![The knowledge graph around program_trace](program_trace.png)

## Concepts associated with program\_trace (15)

| Concept | Description | How it is associated |
| --- | --- | --- |
| **assignment** | = stores the computed value of the right side | prerequisite of it (it needs this)<br>composition rule (R) with it<br>same topic (topic1.2.a) |
| **chained\_assignment** | a = b = 0 assigns right to left | same topic (topic1.2.a) |
| **data\_type** | a set of values and the operations defined on them | same topic (topic1.2.a) |
| **declaration** | int x; -- introduces a variable name and its type | same topic (topic1.2.a) |
| **definite\_assignment** | a local variable must be assigned before it is read | same topic (topic1.2.a) |
| **expression** | anything that evaluates to a value | same topic (topic1.2.a) |
| **identifier** | a name for a variable, method or class; case-sensitive, no spaces, not a keyword | same topic (topic1.2.a) |
| **literal** | a constant value written in code (42, 3.14, true, 'a', "hi") | same topic (topic1.2.a) |
| **named\_constants** | final constants in UPPER\_CASE instead of magic numbers | same topic (topic1.2.a) |
| **naming\_convention** | choosing meaningful names: full words, lowerCamelCase, single letters only for throwaway loop counters | same topic (topic1.2.a) |
| **operator\_precedence** | the order operators bind in an expression | same topic (topic1.2.a) |
| **primitive\_type** | int, double, boolean, char | same topic (topic1.2.a) |
| **testing** | running a program on chosen inputs, including boundary and unusual ones, and comparing the output with what it should be | builds on it (needs it)<br>composition rule (R) with it |
| **variable** | a named, typed box that holds a value | same topic (topic1.2.a) |
| **variable\_swap** | exchanging two variables needs a temporary | same topic (topic1.2.a) |

## Every edge in this view and its full label (22)

| From | Edge | To | Full edge label |
| --- | --- | --- | --- |
| **assignment** | prerequisite | **program\_trace** | A trace records the value each variable holds after each assignment statement runs.<br>grounding: book\_passage<br>composition rule (R) of assignment with program\_trace: A trace records the value of each variable after each assignment runs, one row per statement.<br>composition rule (R) of program\_trace with assignment: Each assignment statement produces the next row of the trace, changing exactly the column of the variable on its left-hand side. |
| **program\_trace** | prerequisite | **testing** | A test needs an expected result, and the expected result comes from tracing what the program should do, step by step.<br>grounding: book\_passage<br>composition rule (R) of testing with program\_trace: The expected output of a test comes from a hand trace of what the program should do for that input. |
| **program\_trace** | has\_level | **program\_trace@L0** | Trace (table of variable values) -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (1 way).<br>**[0] everyday\_reading** (E): Folk meaning: code is read like prose or a set of maths equations, all true at once, and 'tracing' means sketching it over. Java (notional machine) rule: statements execute one at a time in order and change variable values, so a trace is a table with one row per executed statement showing each variable's current value. |
| **program\_trace** | has\_level | **program\_trace@L1** | Trace (table of variable values) -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).<br>**[0] names\_the\_element** (N): A trace is a table of the values of the program's variables after each statement, used to examine what code does.<br>**[1] states\_the\_rule** (S): A trace has one column per variable and one row per executed statement, in execution order; each row shows the value of every variable after that statement, with a declared but unassigned variable shown as undefined. |
| **program\_trace** | has\_level | **program\_trace@L2** | Trace (table of variable values) -&gt; L2 (Multistructural): the answer applies the rules of Trace (table of variable values) to every part of the code, in order (3 ways).<br>**[0] line\_by\_line\_trace** (LT): Follow the flow of control: take the next statement to execute (re-visiting loop bodies on each pass), evaluate it using the current row's values, and write a new row with the variables it changed; continue until the program ends.<br>**[1] output\_prediction** (OP): The last row gives the final values (and any printed output follows from them): for int t = a; a = b; b = t; starting from a = 1234, b = 99, the final row is a = 99, b = 1234, t = 1234.<br>**[2] one\_step\_execution** (OS): Each row differs from the previous one only in the variable(s) assigned by that statement; all other columns are copied unchanged. |
| **program\_trace** | has\_level | **program\_trace@L3** | Trace (table of variable values) -&gt; L3 (Relational): the answer relates the parts (3 ways).<br>**[0] relation\_to\_neighbour** (R): Each assignment statement produces the next row of the trace, changing exactly the column of the variable on its left-hand side.<br>**[1] relation\_to\_neighbour** (R): A test needs an expected result, and the expected result comes from tracing what the program should do, step by step.<br>**[2] purpose\_of\_the\_whole** (P): Used to check or discover what a piece of code does (e.g. convince yourself that three statements swap a and b) and to debug; tracing a few rows often reveals the purpose of the whole. |
| **program\_trace** | has\_level | **program\_trace@L4** | Trace (table of variable values) -&gt; L4 (Extended abstract): the answer reasons beyond the given code (3 ways).<br>**[0] predict\_a\_change** (C): A trace shows the effect of a change: reordering the swap's statements (int t = a; b = t; a = b;) produces a different final row in which both variables hold the original a; the trace of the correct swap keeps the invariant that the old value of a is saved in t before a is overwritten.<br>**[1] transfer\_to\_a\_new\_program** (X): Trace small or unfamiliar code, loops and suspected bugs by hand; for larger programs, reason about what the parts compute (roles, invariants) or let the program print its variables, since a mental trace can hold only a few values at once.<br>**[2] diagnose\_an\_error** (D): rule broken: Each row must be computed from the current values, in execution order. Kind: silent logic error. Trigger class: Long traces or loops that overload working memory: stale or wrong values carried into later rows, giving a wrong predicted output. |
| **topic1.2.a** | contains | **assignment** | topic topic1.2.a contains assignment |
| **topic1.2.a** | contains | **chained\_assignment** | topic topic1.2.a contains chained\_assignment |
| **topic1.2.a** | contains | **data\_type** | topic topic1.2.a contains data\_type |
| **topic1.2.a** | contains | **declaration** | topic topic1.2.a contains declaration |
| **topic1.2.a** | contains | **definite\_assignment** | topic topic1.2.a contains definite\_assignment |
| **topic1.2.a** | contains | **expression** | topic topic1.2.a contains expression |
| **topic1.2.a** | contains | **identifier** | topic topic1.2.a contains identifier |
| **topic1.2.a** | contains | **literal** | topic topic1.2.a contains literal |
| **topic1.2.a** | contains | **named\_constants** | topic topic1.2.a contains named\_constants |
| **topic1.2.a** | contains | **naming\_convention** | topic topic1.2.a contains naming\_convention |
| **topic1.2.a** | contains | **operator\_precedence** | topic topic1.2.a contains operator\_precedence |
| **topic1.2.a** | contains | **primitive\_type** | topic topic1.2.a contains primitive\_type |
| **topic1.2.a** | contains | **program\_trace** | topic topic1.2.a contains program\_trace |
| **topic1.2.a** | contains | **variable** | topic topic1.2.a contains variable |
| **topic1.2.a** | contains | **variable\_swap** | topic topic1.2.a contains variable\_swap |
