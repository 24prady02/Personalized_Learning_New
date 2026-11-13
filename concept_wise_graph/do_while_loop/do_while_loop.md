# do_while_loop (`do_while_loop`)

do { body } while (c); -- body first, test after

Section 1.3 Conditionals and Loops, topic 1.3.g Other conditional and loop constructs (break, continue, switch, do-while, ?:). From the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`).

![The knowledge graph around do_while_loop](do_while_loop.png)

## Concepts associated with do\_while\_loop (8)

| Concept | Description | How it is associated |
| --- | --- | --- |
| **break\_statement** | break -- immediately exits the innermost loop or switch | builds on it (needs it)<br>same topic (topic1.3.g) |
| **conditional\_operator** | c ? a : b -- an expression that picks one of two values | same topic (topic1.3.g) |
| **continue\_statement** | continue -- skips to the next iteration of the innermost loop | builds on it (needs it)<br>same topic (topic1.3.g) |
| **labeled\_break** | labeled break/continue exit or continue an outer loop | same topic (topic1.3.g) |
| **loop\_body** | the block repeated each pass | builds on it (needs it) |
| **loop\_control** | the three slots: init ; condition ; update | builds on it (needs it) |
| **switch\_statement** | switch (x) { case v: ...; break; default: ... } | same topic (topic1.3.g) |
| **while\_loop** | repeat a block while a condition holds | prerequisite of it (it needs this)<br>composition rule (R) with it |

## Every edge in this view and its full label (17)

| From | Edge | To | Full edge label |
| --- | --- | --- | --- |
| **do\_while\_loop** | prerequisite | **break\_statement** | break leaves the do-while loop at once, exactly as it leaves a while or for loop.<br>grounding: spec\_passage |
| **do\_while\_loop** | prerequisite | **continue\_statement** | continue ends the current pass of the do-while loop and goes on to the loop test.<br>grounding: spec\_passage |
| **do\_while\_loop** | prerequisite | **loop\_body** | The block between do and while is the loop body; it runs first and is repeated while the condition holds.<br>grounding: book\_passage |
| **do\_while\_loop** | prerequisite | **loop\_control** | A do-while loop has the same control parts as a while loop (the variable set before, the condition, the update in the body); only the test is moved after the body.<br>grounding: book\_passage |
| **while\_loop** | prerequisite | **do\_while\_loop** | do { body } while (c); is a while loop whose test is moved to the bottom.<br>grounding: book\_passage<br>composition rule (R) of while\_loop with do\_while\_loop: do { body } while (c); means the same as while (c) { body } except that the first test is omitted, so the body runs at least once.<br>composition rule (R) of do\_while\_loop with while\_loop: do { S } while (c); equals \`S; while (c) { S }\`. If c is initially true it behaves exactly like \`while (c) { S }\`; if c is initially false it still runs S once where the while runs it zero times. |
| **do\_while\_loop** | misconception | **DoWhileTestsFirst** | **wrong rule:** A do-while whose condition starts false runs its body zero times.<br>**right rule:** The statements within the do block are always executed at least once.<br>role: primary |
| **do\_while\_loop** | has\_level | **do\_while\_loop@L0** | do while loop -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (3 ways).<br>**[0] everyday\_reading** (E): Folk meaning: in English 'do X while Y' means do X during the time that Y holds, with Y watched continuously, as in the 'while demon'. In Java the condition is tested only at the bottom, after each complete pass of the body, and the first pass always runs.<br>**[1] misconception** (M) &rarr; DoWhileTestsFirst: wrong rule: A do-while whose condition starts false runs its body zero times. Right rule: The first test is omitted: the body always runs at least once, and the condition is checked only after each pass.<br>**[2] inconsistent\_trace** (T) &rarr; DoWhileTestsFirst: Applies the LT rule unevenly: on a trace, the condition is tested before the first pass on some runs (as for while) and after it on others, or one more pass is run after the condition becomes false. The traced number of passes is off by one. (here mixing in: "A do-while whose condition starts false runs its body zero times") |
| **do\_while\_loop** | has\_level | **do\_while\_loop@L1** | do while loop -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).<br>**[0] names\_the\_element** (N): Loop statement: \`do { body } while (cond);\` is a loop whose test comes after the body, so the body runs one or more times.<br>**[1] states\_the\_rule** (S): \`do { &lt;statements&gt; } while (&lt;boolean expression&gt;);\` (note the final semicolon) means the same as the corresponding while loop except that the first test of the condition is omitted. (Spec: JLS §14.13.) |
| **do\_while\_loop** | has\_level | **do\_while\_loop@L2** | do while loop -&gt; L2 (Multistructural): the answer applies the rules of do while loop to every part of the code, in order (3 ways).<br>**[0] line\_by\_line\_trace** (LT): Order: execute the body; evaluate the condition; if true, execute the body again and re-test; stop the first time the condition is false at the bottom test.<br>**[1] output\_prediction** (OP): do-while produces no value. Its result is the state after the last pass. In the unit-disk example, x and y end inside the disk after about 4/π ≈ 1.27 passes on average.<br>**[2] one\_step\_execution** (OS): One pass runs every statement of the body once (e.g. new random x and y) and then evaluates the condition, a boolean that decides whether another pass follows. The test changes nothing unless it has side effects. |
| **do\_while\_loop** | has\_level | **do\_while\_loop@L3** | do while loop -&gt; L3 (Relational): the answer relates the parts (2 ways).<br>**[0] relation\_to\_neighbour** (R): do { S } while (c); equals \`S; while (c) { S }\`. If c is initially true it behaves exactly like \`while (c) { S }\`; if c is initially false it still runs S once where the while runs it zero times.<br>**[1] purpose\_of\_the\_whole** (P): Plan: generate-and-test (rejection sampling) or read-then-validate. Produce a candidate, test it, and repeat until it is acceptable, e.g. a random point in the unit disk. |
| **do\_while\_loop** | has\_level | **do\_while\_loop@L4** | do while loop -&gt; L4 (Extended abstract): the answer reasons beyond the given code (5 ways).<br>**[0] predict\_a\_change** (C) &rarr; DoWhileTestsFirst: Converting do-while to while keeps behaviour whenever the condition is true before the first pass, and breaks it (0 passes vs 1) when it is false. Moving the body's variables out of the block doesn't change the passes, but it is needed for the condition to see them.<br>**[1] transfer\_to\_a\_new\_program** (X): Use do-while when the body must run at least once before the test makes sense: generate-and-reject, prompt-and-validate, or a menu loop. Use while when zero passes must be possible, and for when there is an index with initialise/test/increment.<br>**[2] diagnose\_an\_error** (D): rule broken: A variable declared inside the do block is out of scope in the while condition. Kind: compile-time. Trigger class: \`do { double x = ...; } while (x &gt; 1.0);\` (cannot find symbol x): declare x before the do.<br>**[3] diagnose\_an\_error** (D): rule broken: The do-while statement ends with a semicolon after the condition. Kind: compile-time. Trigger class: Omitting the \`;\` after \`while (cond)\` (';' expected).<br>**[4] diagnose\_an\_error** (D): rule broken: The body runs at least once even if the condition is false. Kind: silent logic error. Trigger class: Using do-while for a task that must allow zero passes (e.g. processing an empty input or N = 0): one spurious pass runs. |
| **topic1.3.g** | contains | **break\_statement** | topic topic1.3.g contains break\_statement |
| **topic1.3.g** | contains | **conditional\_operator** | topic topic1.3.g contains conditional\_operator |
| **topic1.3.g** | contains | **continue\_statement** | topic topic1.3.g contains continue\_statement |
| **topic1.3.g** | contains | **do\_while\_loop** | topic topic1.3.g contains do\_while\_loop |
| **topic1.3.g** | contains | **labeled\_break** | topic topic1.3.g contains labeled\_break |
| **topic1.3.g** | contains | **switch\_statement** | topic topic1.3.g contains switch\_statement |
