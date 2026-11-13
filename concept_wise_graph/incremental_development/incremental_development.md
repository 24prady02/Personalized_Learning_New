# incremental_development (`incremental_development`)

building a program in small steps from a version that works, compiling and testing after each change

Section 1.1 Your First Program, topic 1.1.a Programming in Java: create, compile, execute. From the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`).

![The knowledge graph around incremental_development](incremental_development.png)

## Concepts associated with incremental\_development (4)

| Concept | Description | How it is associated |
| --- | --- | --- |
| **compile** | javac turns source into bytecode | same topic (topic1.1.a) |
| **debugging** | finding and fixing the cause of a wrong result or error by forming a hypothesis, changing the program and checking the prediction | builds on it (needs it)<br>composition rule (R) with it |
| **program\_text** | the source file; class name must match the filename | same topic (topic1.1.a) |
| **run** | java executes main in the JVM | prerequisite of it (it needs this)<br>composition rule (R) with it<br>same topic (topic1.1.a) |

## Every edge in this view and its full label (12)

| From | Edge | To | Full edge label |
| --- | --- | --- | --- |
| **incremental\_development** | prerequisite | **debugging** | Developing in small steps keeps debugging local: an error is in the change just made.<br>grounding: book\_passage<br>composition rule (R) of incremental\_development with debugging: Small steps make debugging local: the newest change is the first suspect.<br>composition rule (R) of debugging with incremental\_development: Small steps keep debugging short: the error is in the change just made. |
| **run** | prerequisite | **incremental\_development** | Each small step is run and checked before the next one is added.<br>grounding: book\_passage<br>composition rule (R) of incremental\_development with run: Running after each step shows at once whether the new lines do what was intended. |
| **incremental\_development** | misconception | **WriteAllThenTest** | **wrong rule:** Write the whole program first, then compile and test it all at the end.<br>**right rule:** Start with a working program and make small changes, compiling and testing after each one, so an error is always in the last change.<br>role: primary |
| **incremental\_development** | has\_level | **incremental\_development@L0** | incremental development -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (3 ways).<br>**[0] everyday\_reading** (E): Everyday writing is drafted all at once and revised at the end. A program is grown in small steps from a version that already works, compiling and running after each step.<br>**[1] misconception** (M) &rarr; WriteAllThenTest: wrong rule: Write the whole program first, then compile and test it all at the end. Right rule: Start with a working program and make small changes, compiling and testing after each one, so an error is always in the last change.<br>**[2] inconsistent\_trace** (T) &rarr; WriteAllThenTest: Applies incremental development unevenly: tests the first few steps one at a time, then adds a large block of untested code at once. (here mixing in: "Write the whole program first, then compile and test it all at the end") |
| **incremental\_development** | has\_level | **incremental\_development@L1** | incremental development -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).<br>**[0] names\_the\_element** (N): Incremental development: growing a program in small, tested steps from a version that works.<br>**[1] states\_the\_rule** (S): Start with a working program and make small, incremental changes; at any point, if there is an error, you will know where to look. Use variables for intermediate values so you can check them. |
| **incremental\_development** | has\_level | **incremental\_development@L2** | incremental development -&gt; L2 (Multistructural): the answer applies the rules of incremental development to every part of the code, in order (3 ways).<br>**[0] line\_by\_line\_trace** (LT): Sequencing: write a few lines, compile, run and check them, then add the next few; never more than one untested change at a time.<br>**[1] output\_prediction** (OP): Result: after every step there is a program that compiles and runs, and does a little more than before.<br>**[2] one\_step\_execution** (OS): State transition: one step adds a small piece of code and ends with the program compiling and passing its checks again. |
| **incremental\_development** | has\_level | **incremental\_development@L3** | incremental development -&gt; L3 (Relational): the answer relates the parts (3 ways).<br>**[0] relation\_to\_neighbour** (R): Running after each step shows at once whether the new lines do what was intended.<br>**[1] relation\_to\_neighbour** (R): Small steps make debugging local: the newest change is the first suspect.<br>**[2] purpose\_of\_the\_whole** (P): Plan: keep a working program at all times so that errors are found where they are made. |
| **incremental\_development** | has\_level | **incremental\_development@L4** | incremental development -&gt; L4 (Extended abstract): the answer reasons beyond the given code (3 ways).<br>**[0] predict\_a\_change** (C) &rarr; WriteAllThenTest: Conservation: each step must keep everything that already worked; if a step breaks it, that step is undone or fixed before going on.<br>**[1] transfer\_to\_a\_new\_program** (X): For any new program: get a minimal version running first (even just printing the inputs), then add one feature at a time, testing each.<br>**[2] diagnose\_an\_error** (D): rule broken: Compile and test after each small change. Kind: compile-time or logic error. Trigger class: many lines are written before the first compile, so the messages and wrong outputs cannot be traced to one change |
| **topic1.1.a** | contains | **compile** | topic topic1.1.a contains compile |
| **topic1.1.a** | contains | **incremental\_development** | topic topic1.1.a contains incremental\_development |
| **topic1.1.a** | contains | **program\_text** | topic topic1.1.a contains program\_text |
| **topic1.1.a** | contains | **run** | topic topic1.1.a contains run |
