# testing (`testing`)

running a program on chosen inputs, including boundary and unusual ones, and comparing the output with what it should be

Section 1.3 Conditionals and Loops, topic 1.3.f Applications (finite sums, Newton, conversion, gambler's ruin, factoring). From the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`).

![The knowledge graph around testing](testing.png)

## Concepts associated with testing (15)

| Concept | Description | How it is associated |
| --- | --- | --- |
| **accumulator\_pattern** | building up a running total/result | same topic (topic1.3.f) |
| **compile** | javac turns source into bytecode | shares misconception CompilesMeansWorks |
| **compile\_time\_error** | an error javac reports before the program can run (syntax, types) | shares misconception CompilesMeansWorks |
| **convergence\_test** | stopping a loop when a floating-point result is close enough | same topic (topic1.3.f) |
| **counter\_pattern** | counting occurrences across passes | same topic (topic1.3.f) |
| **debugging** | finding and fixing the cause of a wrong result or error by forming a hypothesis, changing the program and checking the prediction | builds on it (needs it)<br>composition rule (R) with it<br>same topic (topic1.3.f) |
| **fencepost\_loop** | n items need n - 1 separators: one item handled outside the loop | same topic (topic1.3.f) |
| **flag\_search\_loop** | a boolean flag that a loop sets once and never resets | same topic (topic1.3.f) |
| **logical\_error** | the program runs but computes the wrong result | shares misconception CompilesMeansWorks |
| **loop\_performance** | the running time of a loop program depends on how many iterations it makes | same topic (topic1.3.f) |
| **monte\_carlo\_simulation** | estimating a probability by repeating random trials | same topic (topic1.3.f) |
| **number\_conversion** | converting an integer to its binary representation by casting out powers of 2 in a loop | same topic (topic1.3.f) |
| **program\_trace** | a table of the values of the variables after each statement, used to check what code does | prerequisite of it (it needs this)<br>composition rule (R) with it |
| **run** | java executes main in the JVM | prerequisite of it (it needs this)<br>composition rule (R) with it |
| **run\_time\_error** | an error raised while the program executes (e.g. ArrayIndexOutOfBounds, NumberFormatException) | shares misconception CompilesMeansWorks |

## Every edge in this view and its full label (24)

| From | Edge | To | Full edge label |
| --- | --- | --- | --- |
| **program\_trace** | prerequisite | **testing** | A test needs an expected result, and the expected result comes from tracing what the program should do, step by step.<br>grounding: book\_passage<br>composition rule (R) of testing with program\_trace: The expected output of a test comes from a hand trace of what the program should do for that input. |
| **run** | prerequisite | **testing** | A program is tested by running it on chosen inputs and comparing what it prints with what it should print.<br>grounding: book\_passage<br>composition rule (R) of testing with run: Each test is one run with one input: java Name followed by the test arguments (or with input redirected from a file). |
| **testing** | prerequisite | **debugging** | A failing test is what starts debugging: testing finds that something is wrong, debugging finds why.<br>grounding: book\_passage<br>composition rule (R) of testing with debugging: A failing test starts debugging; after the fix, the same test is run again to confirm it.<br>composition rule (R) of debugging with testing: Testing tells that a program is wrong; debugging finds why. The failing test is re-run after the fix. |
| **compile** | misconception | **CompilesMeansWorks** | **wrong rule:** Code that compiles is code that works.<br>**right rule:** Code that compiles can still have run-time and logical errors.<br>role: primary |
| **compile\_time\_error** | misconception | **CompilesMeansWorks** | **wrong rule:** Code that compiles is code that works.<br>**right rule:** Code that compiles can still have run-time and logical errors.<br>role: context |
| **logical\_error** | misconception | **CompilesMeansWorks** | **wrong rule:** Code that compiles is code that works.<br>**right rule:** Code that compiles can still have run-time and logical errors.<br>role: context |
| **run\_time\_error** | misconception | **CompilesMeansWorks** | **wrong rule:** Code that compiles is code that works.<br>**right rule:** Code that compiles can still have run-time and logical errors.<br>role: context |
| **testing** | misconception | **CompilesMeansWorks** | **wrong rule:** Code that compiles is code that works.<br>**right rule:** Code that compiles can still have run-time and logical errors.<br>role: context |
| **testing** | misconception | **OneTestProvesCorrect** | **wrong rule:** If a program gives the right output for one input, it is correct.<br>**right rule:** One passing run shows only that this input works; a program is checked by running it on numerous inputs, including boundary and unusual ones.<br>role: primary |
| **testing** | has\_level | **testing@L0** | testing -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (4 ways).<br>**[0] everyday\_reading** (E): Everyday 'test' means trying something once to see whether it works. A program test runs the program on several chosen inputs, each with an expected output worked out in advance, and compares the two.<br>**[1] misconception** (M) &rarr; OneTestProvesCorrect: wrong rule: If a program gives the right output for one input, it is correct. Right rule: One passing run shows only that this input works; check the program on numerous inputs, including boundary and unusual ones.<br>**[2] inconsistent\_trace** (T) &rarr; OneTestProvesCorrect: Applies the testing rule unevenly: checks the output for one input against an expected value, but accepts the output for another input without working out what it should be. (here mixing in: "If a program gives the right output for one input, it is correct")<br>**[3] misconception** (M) &rarr; CompilesMeansWorks: wrong rule: Code that compiles is code that works. Right rule: Compiling checks only the form of the code; whether it does the right thing is found by running and testing it. |
| **testing** | has\_level | **testing@L1** | testing -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).<br>**[0] names\_the\_element** (N): Testing: running the program on chosen inputs and comparing each output with the expected output.<br>**[1] states\_the\_rule** (S): Write the program, then run and test it: choose inputs, work out the expected output of each in advance, run the program on each, and compare. Include the boundary cases (0, 1, the largest value, an empty input). |
| **testing** | has\_level | **testing@L2** | testing -&gt; L2 (Multistructural): the answer applies the rules of testing to every part of the code, in order (3 ways).<br>**[0] line\_by\_line\_trace** (LT): Sequencing: first decide the inputs and expected outputs, then run the program once per input, then compare each output with its expectation; a mismatch is recorded before anything is changed.<br>**[1] output\_prediction** (OP): Result: for each input the test gives pass (output equals expectation) or fail; the program is accepted only when every chosen input passes.<br>**[2] one\_step\_execution** (OS): State transition: one test run leaves the program unchanged and adds one pass or fail to what is known about it. |
| **testing** | has\_level | **testing@L3** | testing -&gt; L3 (Relational): the answer relates the parts (4 ways).<br>**[0] relation\_to\_neighbour** (R): Each test is one run with one input: java Name followed by the test arguments (or with input redirected from a file).<br>**[1] relation\_to\_neighbour** (R): The expected output of a test comes from a hand trace of what the program should do for that input.<br>**[2] relation\_to\_neighbour** (R): A failing test starts debugging; after the fix, the same test is run again to confirm it.<br>**[3] purpose\_of\_the\_whole** (P): Plan: tests give evidence that a program does what it should for the inputs that matter, and catch the cases where it does not. |
| **testing** | has\_level | **testing@L4** | testing -&gt; L4 (Extended abstract): the answer reasons beyond the given code (3 ways).<br>**[0] predict\_a\_change** (C) &rarr; OneTestProvesCorrect: Conservation: after any change to the program, the earlier tests must still pass; a fix for one input that breaks another is caught by re-running them all.<br>**[1] transfer\_to\_a\_new\_program** (X): Test every program you write, before using its output: on the given example, on the boundary values, and on an input whose answer you can work out by hand.<br>**[2] diagnose\_an\_error** (D): rule broken: A program is checked on several inputs, including the boundary cases. Kind: silent logic error. Trigger class: only the example input is tried, so a bug that shows for 0, 1, a negative value, the largest value or an empty input is never seen |
| **topic1.3.f** | contains | **accumulator\_pattern** | topic topic1.3.f contains accumulator\_pattern |
| **topic1.3.f** | contains | **convergence\_test** | topic topic1.3.f contains convergence\_test |
| **topic1.3.f** | contains | **counter\_pattern** | topic topic1.3.f contains counter\_pattern |
| **topic1.3.f** | contains | **debugging** | topic topic1.3.f contains debugging |
| **topic1.3.f** | contains | **fencepost\_loop** | topic topic1.3.f contains fencepost\_loop |
| **topic1.3.f** | contains | **flag\_search\_loop** | topic topic1.3.f contains flag\_search\_loop |
| **topic1.3.f** | contains | **loop\_performance** | topic topic1.3.f contains loop\_performance |
| **topic1.3.f** | contains | **monte\_carlo\_simulation** | topic topic1.3.f contains monte\_carlo\_simulation |
| **topic1.3.f** | contains | **number\_conversion** | topic topic1.3.f contains number\_conversion |
| **topic1.3.f** | contains | **testing** | topic topic1.3.f contains testing |
