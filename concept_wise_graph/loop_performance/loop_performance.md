# Loop performance (`loop_performance`)

the running time of a loop program depends on how many iterations it makes

Section 1.3 1.3 Conditionals and Loops, topic 1.3.f Applications (finite sums, Newton, conversion, gambler's ruin, factoring). From the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`).

![The knowledge graph around loop_performance](loop_performance.png)

## Concepts associated with loop\_performance (10)

| Concept | Description | How it is associated |
| --- | --- | --- |
| **accumulator\_pattern** | building up a running total/result | same topic (topic1.3.f) |
| **convergence\_test** | stopping a loop when a floating-point result is close enough | same topic (topic1.3.f) |
| **counter\_pattern** | counting occurrences across passes | same topic (topic1.3.f) |
| **debugging** | finding and fixing the cause of a wrong result or error by forming a hypothesis, changing the program and checking the prediction | same topic (topic1.3.f) |
| **fencepost\_loop** | n items need n - 1 separators: one item handled outside the loop | same topic (topic1.3.f) |
| **flag\_search\_loop** | a boolean flag that a loop sets once and never resets | same topic (topic1.3.f) |
| **loop\_control** | the three slots: init ; condition ; update | prerequisite of it (it needs this)<br>composition rule (R) with it |
| **monte\_carlo\_simulation** | estimating a probability by repeating random trials | same topic (topic1.3.f) |
| **number\_conversion** | converting an integer to its binary representation by casting out powers of 2 in a loop | same topic (topic1.3.f) |
| **testing** | running a program on chosen inputs, including boundary and unusual ones, and comparing the output with what it should be | same topic (topic1.3.f) |

## Every edge in this view and its full label (16)

| From | Edge | To | Full edge label |
| --- | --- | --- | --- |
| **loop\_control** | prerequisite | **loop\_performance** | The loop condition decides how many iterations run, so a better test (i &lt;= n/i instead of i &lt; n) makes the program much faster.<br>grounding: book\_passage<br>composition rule (R) of loop\_control with loop\_performance: The continuation condition fixes the number of iterations, so a sharper bound (i &lt;= n/i instead of i &lt; n) can make a program dramatically faster.<br>composition rule (R) of loop\_performance with loop\_control: The loop's condition and update set the iteration count. A tighter test that keeps correctness (i &lt;= n/i instead of i &lt; n) or a faster update (doubling instead of incrementing) can make the program dramatically faster with identical output. |
| **loop\_performance** | has\_level | **loop\_performance@L0** | Loop performance -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (1 way).<br>**[0] everyday\_reading** (E): Folk meaning: 'computers are so fast it doesn't matter how many steps', so any correct loop is good enough. In fact running time grows with the number of iterations: an n-step loop over 10^18 values never finishes, while a √n-step loop finishes in seconds. |
| **loop\_performance** | has\_level | **loop\_performance@L1** | Loop performance -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).<br>**[0] names\_the\_element** (N): Performance concept: the running time of a loop program is roughly (number of iterations) × (cost per iteration), and the loop condition determines the number of iterations.<br>**[1] states\_the\_rule** (S): Running time is proportional to the total number of times the innermost statements execute. Nested loops multiply their counts, so Gambler takes T × (average bets), and changing a bound from n to √n changes the feasible input from about 10^9 to about 10^18. |
| **loop\_performance** | has\_level | **loop\_performance@L2** | Loop performance -&gt; L2 (Multistructural): the answer applies the rules of Loop performance to every part of the code, in order (3 ways).<br>**[0] line\_by\_line\_trace** (LT): Order of the estimate: count the passes of the outer loop; for each, count the passes of the inner loop; multiply (or sum); multiply by the cost of one pass of the innermost body.<br>**[1] output\_prediction** (OP): The result is an iteration count or time estimate. \`for (i = 2; i &lt;= n/i; i++)\` runs about √n times, against about n times for \`i &lt; n\`. Gambler 500 2500 100 makes about 100 × 10^6 bets (nearly 100 million random numbers).<br>**[2] one\_step\_execution** (OS): Each extra pass adds a constant amount of work. Adding 1 to the bound of a single loop adds one pass, while adding 1 to the bound of an outer loop adds a full run of the inner loop. |
| **loop\_performance** | has\_level | **loop\_performance@L3** | Loop performance -&gt; L3 (Relational): the answer relates the parts (2 ways).<br>**[0] relation\_to\_neighbour** (R): The loop's condition and update set the iteration count. A tighter test that keeps correctness (i &lt;= n/i instead of i &lt; n) or a faster update (doubling instead of incrementing) can make the program dramatically faster with identical output.<br>**[1] purpose\_of\_the\_whole** (P): Purpose: to predict whether a program will finish in reasonable time for its inputs, and to choose among correct loop formulations (bounds, nesting, reuse of previous results). |
| **loop\_performance** | has\_level | **loop\_performance@L4** | Loop performance -&gt; L4 (Extended abstract): the answer reasons beyond the given code (5 ways).<br>**[0] predict\_a\_change** (C): Changing the factoring test from \`i &lt; n\` to \`i &lt;= n/i\` keeps the output identical (by the invariant) and cuts iterations from about n to about √n. Reusing the previous term in the e^x loop keeps the sum and removes the inner loop.<br>**[1] transfer\_to\_a\_new\_program** (X): Think about loop performance whenever the iteration count grows with large inputs (factoring, prime counting, simulations, nested loops). For small fixed counts (TenHellos), clarity matters more than speed. Experiment with timings to compare formulations.<br>**[2] diagnose\_an\_error** (D): rule broken: Iteration count must be kept feasible for the input size. Kind: silent logic error. Trigger class: A naive bound (\`i &lt; n\` when factoring an 18-digit number, or counting primes up to 10 million by trial division): the program appears to hang.<br>**[3] diagnose\_an\_error** (D): rule broken: Do not recompute in an inner loop what the previous pass already computed. Kind: silent logic error. Trigger class: Recomputing each Taylor term from scratch in a nested loop: correct output but needlessly slow.<br>**[4] diagnose\_an\_error** (D): rule broken: Nested-loop cost is the product of the counts. Kind: silent logic error. Trigger class: Large T times long trials in a simulation (Gambler 100000 200000 100): run time explodes. |
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
