# Program state (`program_state`)

the information needed to know what a program will do next: the values of its variables and array entries and the next statement

Section 1.4 1.4 Arrays, topic 1.4.b Memory representation and bounds checking. From the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`).

![The knowledge graph around program_state](program_state.png)

## Concepts associated with program\_state (10)

| Concept | Description | How it is associated |
| --- | --- | --- |
| **accumulator\_pattern** | building up a running total/result | shares misconception StateChangeIgnoredAcrossPasses |
| **array\_aliasing** | two variables can refer to the same array | same topic (topic1.4.b) |
| **array\_bounds** | valid indices are 0 .. length-1; otherwise throws | same topic (topic1.4.b) |
| **array\_copy** | making a second, independent array with the same elements: create a new array and copy element by element (or Arrays.copyOf) | same topic (topic1.4.b) |
| **array\_reference** | the array variable stores the memory address (pointer) of the array; a[i] is found by adding i to that address | same topic (topic1.4.b) |
| **loop\_body** | the block repeated each pass | shares misconception StateChangeIgnoredAcrossPasses |
| **loop\_guard** | putting the bounds check in the loop condition so the body never makes an out-of-bounds array access | same topic (topic1.4.b) |
| **primitive\_vs\_reference** | a primitive variable holds its value; an array (or String) variable holds a reference to the object stored elsewhere | same topic (topic1.4.b) |
| **printing\_array\_reference** | printing an array variable prints a reference, not the elements | same topic (topic1.4.b) |
| **variable** | a named, typed box that holds a value | prerequisite of it (it needs this)<br>composition rule (R) with it |

## Every edge in this view and its full label (17)

| From | Edge | To | Full edge label |
| --- | --- | --- | --- |
| **variable** | prerequisite | **program\_state** | Without arrays, a program's state is the values of its variables plus the next statement to run.<br>grounding: book\_passage<br>composition rule (R) of variable with program\_state: The current values of all variables make up the program's state. A trace records each variable's value after each statement.<br>composition rule (R) of program\_state with variable: Without arrays the state is the values of the variables plus the next statement; each array element adds one more variable to the state. |
| **accumulator\_pattern** | misconception | **StateChangeIgnoredAcrossPasses** | **wrong rule:** Values changed by one pass of a loop (other than the loop variable) do not affect later passes.<br>**right rule:** Each pass starts from the state left by the previous pass, so a change in one pass carries into the next ones.<br>role: context |
| **loop\_body** | misconception | **StateChangeIgnoredAcrossPasses** | **wrong rule:** Values changed by one pass of a loop (other than the loop variable) do not affect later passes.<br>**right rule:** Each pass starts from the state left by the previous pass, so a change in one pass carries into the next ones.<br>role: primary |
| **program\_state** | misconception | **StateChangeIgnoredAcrossPasses** | **wrong rule:** Values changed by one pass of a loop (other than the loop variable) do not affect later passes.<br>**right rule:** Each pass starts from the state left by the previous pass, so a change in one pass carries into the next ones.<br>role: context |
| **program\_state** | has\_level | **program\_state@L0** | Program state -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (2 ways).<br>**[0] everyday\_reading** (E): Folk meaning: program statements read like maths equations, timeless relations among values. Java rule: each statement changes the state (the values of variables and array entries), and the next statement starts from the changed state.<br>**[1] misconception** (M) &rarr; StateChangeIgnoredAcrossPasses: wrong rule: Values changed by one pass of a loop (other than the loop variable) do not affect later passes. Right rule: Each pass starts from the state left by the previous pass, so a change in one pass carries into the next ones. |
| **program\_state** | has\_level | **program\_state@L1** | Program state -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).<br>**[0] names\_the\_element** (N): Identity: the state of a program is the information needed to know what it will do next: the values of its variables (and array entries) and which statement runs next.<br>**[1] states\_the\_rule** (S): Declarative: in a program without arrays, knowing the variable values and the next statement determines what the program does next; arrays add one state component per element. |
| **program\_state** | has\_level | **program\_state@L2** | Program state -&gt; L2 (Multistructural): the answer applies the rules of Program state to every part of the code, in order (3 ways).<br>**[0] line\_by\_line\_trace** (LT): Sequencing: statements in a block execute in order, first to last, so the state seen by each statement is the result of all earlier ones.<br>**[1] output\_prediction** (OP): Result: the output from any point on is determined by the current state; equal states give the same future behaviour (apart from Math.random and input).<br>**[2] one\_step\_execution** (OS): State transition: each assignment changes exactly one variable or one array element; tracing tracks these changes. |
| **program\_state** | has\_level | **program\_state@L3** | Program state -&gt; L3 (Relational): the answer relates the parts (2 ways).<br>**[0] relation\_to\_neighbour** (R): Without arrays the state is the values of the variables plus the next statement; each array element adds one more variable to the state.<br>**[1] purpose\_of\_the\_whole** (P): Plan/role: tracing (a trace table of the state after each step) is how programs are understood and debugged; with large arrays one checks invariants among state components instead. |
| **program\_state** | has\_level | **program\_state@L4** | Program state -&gt; L4 (Extended abstract): the answer reasons beyond the given code (3 ways).<br>**[0] predict\_a\_change** (C): Conservation: an invariant such as 'valcnt equals the number of true entries in found[]' holds after every pass; a change that breaks it signals a bug.<br>**[1] transfer\_to\_a\_new\_program** (X): Applicability: trace the full state for small programs. When arrays make the state too large to track, reason with invariants and partial traces instead.<br>**[2] diagnose\_an\_error** (D): rule broken: Each pass starts from the state left by the previous one. Kind: silent logic error. Trigger class: an accumulator is not reset between outer passes (sum declared before the row loop), so later rows include earlier rows' totals |
| **topic1.4.b** | contains | **array\_aliasing** | topic topic1.4.b contains array\_aliasing |
| **topic1.4.b** | contains | **array\_bounds** | topic topic1.4.b contains array\_bounds |
| **topic1.4.b** | contains | **array\_copy** | topic topic1.4.b contains array\_copy |
| **topic1.4.b** | contains | **array\_reference** | topic topic1.4.b contains array\_reference |
| **topic1.4.b** | contains | **loop\_guard** | topic topic1.4.b contains loop\_guard |
| **topic1.4.b** | contains | **primitive\_vs\_reference** | topic topic1.4.b contains primitive\_vs\_reference |
| **topic1.4.b** | contains | **printing\_array\_reference** | topic topic1.4.b contains printing\_array\_reference |
| **topic1.4.b** | contains | **program\_state** | topic topic1.4.b contains program\_state |
