# simulation_loop (`simulation_loop`)

take many random steps

Section 1.6 Case Study: Random Web Surfer, topic 1.6.b Simulation (one random move, page ranks).

![The knowledge graph around simulation_loop](simulation_loop.png)

## At a glance

- **Needs first:** `for_loop`, `random_move`
- **Leads to:** `frequency_counting`
- **Learned alongside:** `power_method`
- **Misconceptions:** `FewTrialsAreExact`, `LoopBodyScopeImpliesLoopLifetime`, `OffByOneBound`
- **Errors:** none
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 27 edges around this concept. The edge logic, the wrong and right rules and the exact rules of the ways are copied word for word from the graph.

## To work on (1)

- no aliases: a student's words cannot name this concept

## What it needs first (2)

A prerequisite edge means the other concept has to be understood before `simulation_loop`.

### `for_loop` comes before `simulation_loop`

*a while with init/condition/update packaged together*

- **Edge:** `pre:for_loop->simulation_loop`
- **Exact edge logic:** The simulation is a for loop over t = 0 ... T - 1 that makes one random move per pass.
- **Grounding:** book\_passage
- **Composition rule (R) of `simulation_loop` with `for_loop`:** A counted for loop with t &lt; T fixes the number of moves at T; the loop variable t is scoped to the loop.
- **Composition rule (R) of `for_loop` with `simulation_loop`:** A simulation runs a fixed number of trials with an outer for loop (for (int t = 0; t &lt; T; t++)), each trial simulated inside the body.

### `random_move` comes before `simulation_loop`

*pick the next page from a cumulative-probability test*

- **Edge:** `pre:random_move->simulation_loop`
- **Exact edge logic:** The simulation repeats the random move T times, each move starting from the page the previous move reached.
- **Grounding:** book\_passage
- **Composition rule (R) of `simulation_loop` with `random_move`:** The loop body is one random move; page carries state from one pass to the next, so each move uses the row of the page reached last.
- **Composition rule (R) of `random_move` with `simulation_loop`:** Each move starts from the page the previous move produced, and the simulation repeats it T times; the next row used is p[new page].

## What it leads to (1)

These concepts need `simulation_loop` first.

### `simulation_loop` comes before `frequency_counting`

*tally visits to estimate page rank*

- **Edge:** `pre:simulation_loop->frequency_counting`
- **Exact edge logic:** On each pass the simulation adds 1 to freq[page] for the page just reached.
- **Grounding:** book\_passage
- **Composition rule (R) of `simulation_loop` with `frequency_counting`:** freq[page]++ must come after the move and inside the loop, once per pass, so the counts total T.
- **Composition rule (R) of `frequency_counting` with `simulation_loop`:** The increment is the last statement of each pass, so the counts tally the pages reached by the T moves (sum = T).

## Learned alongside (1)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

### `simulation_loop` alongside `power_method`

*repeated vector-matrix multiplication to compute page ranks*

- **Edge:** `par:simulation_loop~power_method`
- **Exact edge logic:** The power method used in Markov is far more efficient than simulating the behavior of a random surfer.
- **Grounding:** book\_passage
- **Composition rule (R) of `simulation_loop` with `power_method`:** Both compute the same page ranks; the power method gets them exactly with far fewer iterations.
- **Composition rule (R) of `power_method` with `simulation_loop`:** Computes the same ranks far more efficiently than simulating moves.

## Misconceptions (3)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### FewTrialsAreExact

- **Edge:** `simulation_loop` &rarr; `FewTrialsAreExact` (misconception)
- **Exact edge logic (the wrong rule):** A short simulation gives the exact page ranks.
- **Twin logic (the right rule):** A simulation only estimates the page ranks: RandomSurfer needs 10^n moves to get answers precise to n decimal places and many more moves for those answers to become accurate (tens of thousands of moves for two accurate places, millions for three).
- **Wrong belief (on the node):** A short simulation gives the exact page ranks.
- **Correct rule (on the node):** A simulation only estimates the page ranks: RandomSurfer needs 10^n moves to get answers precise to n decimal places and many more moves for those answers to become accurate (tens of thousands of moves for two accurate places, millions for three).
- **Provenance:** published
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [2] misconception, exact rule:** wrong rule: A short simulation gives the exact page ranks. Right rule: A simulation only estimates the ranks: about 10^n moves for n-digit precision, tens of thousands of moves for two accurate places and millions for three.
- **Edge `frequency_counting` &rarr; `FewTrialsAreExact`, exact edge logic:** A short simulation gives the exact page ranks. **Twin logic:** A simulation only estimates the page ranks: RandomSurfer needs 10^n moves to get answers precise to n decimal places and many more moves for those answers to become accurate (tens of thousands of moves for two accurate places, millions for three). (role: primary)
- **Edge `monte_carlo_simulation` &rarr; `FewTrialsAreExact`, exact edge logic:** A short simulation gives the exact page ranks. **Twin logic:** A simulation only estimates the page ranks: RandomSurfer needs 10^n moves to get answers precise to n decimal places and many more moves for those answers to become accurate (tens of thousands of moves for two accurate places, millions for three). (role: context)
- **Edge `two_models` &rarr; `FewTrialsAreExact`, exact edge logic:** A short simulation gives the exact page ranks. **Twin logic:** A simulation only estimates the page ranks: RandomSurfer needs 10^n moves to get answers precise to n decimal places and many more moves for those answers to become accurate (tens of thousands of moves for two accurate places, millions for three). (role: context)

### LoopBodyScopeImpliesLoopLifetime

- **Edge:** `simulation_loop` &rarr; `LoopBodyScopeImpliesLoopLifetime` (misconception)
- **Exact edge logic (the wrong rule):** Declaring page inside the simulation loop still lets the surfer continue from the previous page.
- **Twin logic (the right rule):** If page is declared inside the loop body it is recreated each pass, so it must be declared before the loop to carry the walk forward.
- **Wrong belief (on the node):** a variable declared in the loop body lives across all iterations
- **Correct rule (on the node):** A variable declared inside the body is created anew on every pass and does not keep the previous pass's value.
- **Provenance:** published
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [4] misconception, exact rule:** wrong rule: A variable declared in the loop body lives across all iterations. Right rule: r and sum are declared inside the t-loop body and are created anew on every move; freq and page must be declared before the loop to persist.
- **Edge `accumulator_pattern` &rarr; `LoopBodyScopeImpliesLoopLifetime`, exact edge logic:** a variable declared in the loop body lives across all iterations **Twin logic:** A variable declared inside the body is created anew on every pass and does not keep the previous pass's value. (role: context)
- **Edge `loop_scope` &rarr; `LoopBodyScopeImpliesLoopLifetime`, exact edge logic:** A variable declared inside the loop body keeps its value from one pass to the next. **Twin logic:** A variable declared inside the body is created anew on every pass and does not keep the previous pass's value. (role: primary)
- **Edge `variable` &rarr; `LoopBodyScopeImpliesLoopLifetime`, exact edge logic:** a variable declared in the loop body lives across all iterations **Twin logic:** A variable declared inside the body is created anew on every pass and does not keep the previous pass's value. (role: context)

### OffByOneBound

- **Edge:** `simulation_loop` &rarr; `OffByOneBound` (misconception)
- **Exact edge logic (the wrong rule):** t &lt; T and t &lt;= T give the same number of moves.
- **Twin logic (the right rule):** for (t = 0; t &lt; T; t++) makes exactly T moves; with &lt;= it makes T + 1.
- **Wrong belief (on the node):** &lt; vs &lt;= and 0..n vs 0..n-1 are interchangeable
- **Correct rule (on the node):** for (i = 0; i &lt; n; i++) runs n times with i going up to n - 1; with &lt;= it runs n + 1 times and reaches i = n.
- **Provenance:** published
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [1] misconception, exact rule:** wrong rule: &lt; vs &lt;= and 0..n vs 0..n-1 are interchangeable. Right rule: for (int t = 0; t &lt; T; t++) makes exactly T moves; with &lt;= it makes T + 1, while the ranks are still divided by T.
- **L0 way [3] inconsistent\_trace, exact rule:** Applies LT (draw r, find next page, then freq[page]++) unevenly: e.g. counting the current page before the move on some passes, or resetting sum only on the first pass. (here mixing in: "&lt; vs &lt;= and 0..n vs 0..n-1 are interchangeable")
- **Edge `array_bounds` &rarr; `OffByOneBound`, exact edge logic:** &lt; vs &lt;= and 0..n vs 0..n-1 are interchangeable **Twin logic:** for (i = 0; i &lt; n; i++) runs n times with i going up to n - 1; with &lt;= it runs n + 1 times and reaches i = n. (role: context)
- **Edge `array_reversal` &rarr; `OffByOneBound`, exact edge logic:** &lt; vs &lt;= and 0..n vs 0..n-1 are interchangeable **Twin logic:** for (i = 0; i &lt; n; i++) runs n times with i going up to n - 1; with &lt;= it runs n + 1 times and reaches i = n. (role: context)
- **Edge `array_traversal` &rarr; `OffByOneBound`, exact edge logic:** &lt; vs &lt;= and 0..n vs 0..n-1 are interchangeable **Twin logic:** for (i = 0; i &lt; n; i++) runs n times with i going up to n - 1; with &lt;= it runs n + 1 times and reaches i = n. (role: context)
- **Edge `boolean_flag_array` &rarr; `OffByOneBound`, exact edge logic:** &lt; vs &lt;= and 0..n vs 0..n-1 are interchangeable **Twin logic:** for (i = 0; i &lt; n; i++) runs n times with i going up to n - 1; with &lt;= it runs n + 1 times and reaches i = n. (role: context)
- **Edge `loop_control` &rarr; `OffByOneBound`, exact edge logic:** i &lt; n and i &lt;= n mean the same, so the loop runs until i equals n and the last pass can use a[n]. **Twin logic:** for (i = 0; i &lt; n; i++) runs n times with i going up to n - 1; with &lt;= it runs n + 1 times and reaches i = n. (role: primary)
- **Edge `off_by_one_error` &rarr; `OffByOneBound`, exact edge logic:** &lt; vs &lt;= and 0..n vs 0..n-1 are interchangeable **Twin logic:** for (i = 0; i &lt; n; i++) runs n times with i going up to n - 1; with &lt;= it runs n + 1 times and reaches i = n. (role: context)

## Errors (0)

An error edge states the rule that gets broken in a program, and the right rule.

The graph has no error edge from this concept.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for simulation loop: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to simulation loop agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

- **Edge:** `simulation_loop` &rarr; `simulation_loop@L0` (has_level)
- **Exact edge logic:** simulation loop -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (5 ways).

Ways (5), each with its exact rule:

- **[0] everyday\_reading** (rule type E, folk-meaning rule): Everyday "simulate" suggests replaying a known process to get its answer; here each run of RandomSurfer draws fresh random numbers and gives different estimates (100 moves: 0.24 0.23 0.16 0.25 0.12), which only approach the page ranks as T grows.
- **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `OffByOneBound`: wrong rule: &lt; vs &lt;= and 0..n vs 0..n-1 are interchangeable. Right rule: for (int t = 0; t &lt; T; t++) makes exactly T moves; with &lt;= it makes T + 1, while the ranks are still divided by T.
- **[2] misconception** (rule type M, wrong rule / right rule) &rarr; `FewTrialsAreExact`: wrong rule: A short simulation gives the exact page ranks. Right rule: A simulation only estimates the ranks: about 10^n moves for n-digit precision, tens of thousands of moves for two accurate places and millions for three.
- **[3] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `OffByOneBound`: Applies LT (draw r, find next page, then freq[page]++) unevenly: e.g. counting the current page before the move on some passes, or resetting sum only on the first pass. (here mixing in: "&lt; vs &lt;= and 0..n vs 0..n-1 are interchangeable")
- **[4] misconception** (rule type M, wrong rule / right rule) &rarr; `LoopBodyScopeImpliesLoopLifetime`: wrong rule: A variable declared in the loop body lives across all iterations. Right rule: r and sum are declared inside the t-loop body and are created anew on every move; freq and page must be declared before the loop to persist.

### L1: Unistructural / atom x text surface

L1 for simulation loop: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

- **Edge:** `simulation_loop` &rarr; `simulation_loop@L1` (has_level)
- **Exact edge logic:** simulation loop -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

Ways (2), each with its exact rule:

- **[0] names\_the\_element** (rule type N, identity rule): A Monte Carlo simulation: a for loop over t = 0..T-1 that makes one random move per pass and tallies the page reached.
- **[1] states\_the\_rule** (rule type S, declarative rule): RandomSurfer reads a transition matrix, starts at page 0, makes T moves (T from the command line) according to the matrix, and counts the visits to each page.

### L2: Multistructural / block x execution / preoperational

L2 for simulation loop: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

- **Edge:** `simulation_loop` &rarr; `simulation_loop@L2` (has_level)
- **Exact edge logic:** simulation loop -&gt; L2 (Multistructural): the answer applies the rules of simulation loop to every part of the code, in order (3 ways).

Ways (3), each with its exact rule:

- **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): Per pass: r = Math.random(); sum = 0.0; inner j loop picks the next page; freq[page]++; t++ and test t &lt; T. After the loop, each freq[i] is divided by T and printed.
- **[1] output\_prediction** (rule type OP, evaluation / result rule): Prints N doubles (%8.5f) that sum to about 1 and vary between runs; 1,000,000 moves on tiny.txt gave 0.27324 0.26568 0.14581 0.24737 0.06790.
- **[2] one\_step\_execution** (rule type OS, state-transition rule): One pass changes page (to the next page) and increases freq[page] by 1; t increases by 1.

### L3: Relational / relations x function (concrete operational begins)

L3 for simulation loop: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

- **Edge:** `simulation_loop` &rarr; `simulation_loop@L3` (has_level)
- **Exact edge logic:** simulation loop -&gt; L3 (Relational): the answer relates the parts (5 ways).

Ways (5), each with its exact rule:

- **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): The loop body is one random move; page carries state from one pass to the next, so each move uses the row of the page reached last.
- **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): freq[page]++ must come after the move and inside the loop, once per pass, so the counts total T.
- **[2] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): A counted for loop with t &lt; T fixes the number of moves at T; the loop variable t is scoped to the loop.
- **[3] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Both compute the same page ranks; the power method gets them exactly with far fewer iterations.
- **[4] purpose\_of\_the\_whole** (rule type P, plan / role rule): Monte Carlo estimation plan: repeat a random experiment many times and count outcomes; t is a stepper, page a most-recent holder, freq[] the per-page gatherers.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for simulation loop: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

- **Edge:** `simulation_loop` &rarr; `simulation_loop@L4` (has_level)
- **Exact edge logic:** simulation loop -&gt; L4 (Extended abstract): the answer reasons beyond the given code (6 ways).

Ways (6), each with its exact rule:

- **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `OffByOneBound`: Changing the start page keeps the limit (mixing); increasing T keeps the estimates but makes them more accurate (about 10x moves per extra digit); changing &lt; to &lt;= or the division by T breaks the normalisation.
- **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Use when the process is easy to simulate and a rough estimate suffices (or no matrix is available); not for accurate ranks or large models, where a huge number of trials is needed and the power method is far more efficient.
- **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: Loop must run t = 0..T-1. Kind: silent logic error. Trigger class: t &lt;= T makes T+1 moves but ranks are divided by T, so they sum to slightly more than 1.
- **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: A variable declared in the body is recreated each pass. Kind: silent logic error. Trigger class: int[] freq = new int[N] declared inside the loop body: counts reset every move (and freq is out of scope after the loop, a compile-time error if printed there).
- **[4] diagnose\_an\_error** (rule type D, error rule): rule broken: freq[i] / T must be floating-point division. Kind: silent logic error. Trigger class: Printing freq[i] / T without the (double) cast: every rank prints as 0 (or 1).
- **[5] diagnose\_an\_error** (rule type D, error rule): rule broken: The number of moves is args[0]. Kind: run-time exception. Trigger class: Run without a command-line argument: args[0] throws ArrayIndexOutOfBoundsException; a non-numeric argument makes Integer.parseInt throw NumberFormatException.

## Same topic

`simulation_loop` belongs to the topic **Simulation (one random move, page ranks)** (`topic1.6.b`). The topic also contains: `frequency_counting`, `random_move`.

## Rules of the concept (21)

- **Book** (SW-1e, p. 166 (pdf 176)): "It counts the number of times that the surfer visits each page."
- **Book** (SW-1.6, p. 166 (pdf 176)): "Dividing that count by the number of moves yields an estimate of the probability that a random surfer winds up on the page. This probability is known as the page's rank"
- **E** (folk-meaning rule): Everyday "simulate" suggests replaying a known process to get its answer; here each run of RandomSurfer draws fresh random numbers and gives different estimates (100 moves: 0.24 0.23 0.16 0.25 0.12), which only approach the page ranks as T grows.
- **M** (wrong rule / right rule): FewTrialsAreExact: wrong: A short simulation gives the exact page ranks. \| right: A simulation only estimates the ranks: about 10^n moves for n-digit precision, tens of thousands of moves for two accurate places and millions for three.
- **M** (wrong rule / right rule): LoopBodyScopeImpliesLoopLifetime: wrong: A variable declared in the loop body lives across all iterations. \| right: r and sum are declared inside the t-loop body and are created anew on every move; freq and page must be declared before the loop to persist.
- **M** (wrong rule / right rule): OffByOneBound: wrong: &lt; vs &lt;= and 0..n vs 0..n-1 are interchangeable. \| right: for (int t = 0; t &lt; T; t++) makes exactly T moves; with &lt;= it makes T + 1, while the ranks are still divided by T.
- **T** (uneven-application rule): Applies LT (draw r, find next page, then freq[page]++) unevenly: e.g. counting the current page before the move on some passes, or resetting sum only on the first pass.
- **N** (identity rule): A Monte Carlo simulation: a for loop over t = 0..T-1 that makes one random move per pass and tallies the page reached.
- **S** (declarative rule): RandomSurfer reads a transition matrix, starts at page 0, makes T moves (T from the command line) according to the matrix, and counts the visits to each page.
- **LT** (operational sequencing rule): Per pass: r = Math.random(); sum = 0.0; inner j loop picks the next page; freq[page]++; t++ and test t &lt; T. After the loop, each freq[i] is divided by T and printed.
- **OP** (evaluation / result rule): Prints N doubles (%8.5f) that sum to about 1 and vary between runs; 1,000,000 moves on tiny.txt gave 0.27324 0.26568 0.14581 0.24737 0.06790.
- **OS** (state-transition rule): One pass changes page (to the next page) and increases freq[page] by 1; t increases by 1.
- **R** (composition rule (with a neighbour)): with random\_move: The loop body is one random move; page carries state from one pass to the next, so each move uses the row of the page reached last.
- **R** (composition rule (with a neighbour)): with frequency\_counting: freq[page]++ must come after the move and inside the loop, once per pass, so the counts total T.
- **R** (composition rule (with a neighbour)): with for\_loop: A counted for loop with t &lt; T fixes the number of moves at T; the loop variable t is scoped to the loop.
- **R** (composition rule (with a neighbour)): with power\_method: Both compute the same page ranks; the power method gets them exactly with far fewer iterations.
- **P** (plan / role rule): Monte Carlo estimation plan: repeat a random experiment many times and count outcomes; t is a stepper, page a most-recent holder, freq[] the per-page gatherers.
- **C** (conservation rule): Changing the start page keeps the limit (mixing); increasing T keeps the estimates but makes them more accurate (about 10x moves per extra digit); changing &lt; to &lt;= or the division by T breaks the normalisation.
- **D** (error rule): rule broken: Loop must run t = 0..T-1. (silent logic error)
- **D** (error rule): rule broken: A variable declared in the body is recreated each pass. (silent logic error)
- **D** (error rule): rule broken: freq[i] / T must be floating-point division. (silent logic error)
- **D** (error rule): rule broken: The number of moves is args[0]. (run-time exception)
- **X** (applicability rule): Use when the process is easy to simulate and a rough estimate suffices (or no matrix is available); not for accurate ranks or large models, where a huge number of trials is needed and the power method is far more efficient.

## How it is found in code and answers (reader block)

- **Aliases:** none
- **Code patterns:** `(?i)\b(?:trials|moves|steps)\b`, `\bRandomSurfer\b`
- **Operator symbols:** none
- **Java types:** none

## The whole prerequisite chain

- **Everything it builds on (30):** `arithmetic_operators`, `array_creation`, `array_declaration`, `array_initializer`, `boolean`, `boolean_expression`, `comparison_operators`, `data_structure`, `data_type`, `do_while_loop`, `expression`, `for_loop`, `identifier`, `indexing`, `input_graph`, `literal`, `logical_operators`, `loop_control`, `loop_variable`, `math_library`, `method_call`, `primitive_type`, `random_move`, `standard_input`, `stream_model`, `teleportation`, `transition_matrix`, `two_dimensional_array`, `variable`, `while_loop`
- **Everything that builds on it (2):** `frequency_counting`, `two_models`

## Every edge in this view and its exact edge logic (27)

All the edges drawn in the picture, in the order: prerequisite, parallel, misconception, error, has_level, contains.

**1. `for_loop` &rarr; `simulation_loop`** (prerequisite)

- **Exact edge logic:** The simulation is a for loop over t = 0 ... T - 1 that makes one random move per pass.
- **Grounding:** book\_passage
- **Composition rule (R) of `for_loop` with `simulation_loop`:** A simulation runs a fixed number of trials with an outer for loop (for (int t = 0; t &lt; T; t++)), each trial simulated inside the body.
- **Composition rule (R) of `simulation_loop` with `for_loop`:** A counted for loop with t &lt; T fixes the number of moves at T; the loop variable t is scoped to the loop.

**2. `random_move` &rarr; `simulation_loop`** (prerequisite)

- **Exact edge logic:** The simulation repeats the random move T times, each move starting from the page the previous move reached.
- **Grounding:** book\_passage
- **Composition rule (R) of `random_move` with `simulation_loop`:** Each move starts from the page the previous move produced, and the simulation repeats it T times; the next row used is p[new page].
- **Composition rule (R) of `simulation_loop` with `random_move`:** The loop body is one random move; page carries state from one pass to the next, so each move uses the row of the page reached last.

**3. `simulation_loop` &rarr; `frequency_counting`** (prerequisite)

- **Exact edge logic:** On each pass the simulation adds 1 to freq[page] for the page just reached.
- **Grounding:** book\_passage
- **Composition rule (R) of `simulation_loop` with `frequency_counting`:** freq[page]++ must come after the move and inside the loop, once per pass, so the counts total T.
- **Composition rule (R) of `frequency_counting` with `simulation_loop`:** The increment is the last statement of each pass, so the counts tally the pages reached by the T moves (sum = T).

**4. `simulation_loop` &harr; `power_method`** (parallel)

- **Exact edge logic:** The power method used in Markov is far more efficient than simulating the behavior of a random surfer.
- **Grounding:** book\_passage
- **Composition rule (R) of `simulation_loop` with `power_method`:** Both compute the same page ranks; the power method gets them exactly with far fewer iterations.
- **Composition rule (R) of `power_method` with `simulation_loop`:** Computes the same ranks far more efficiently than simulating moves.

**5. `simulation_loop` &rarr; `FewTrialsAreExact`** (misconception)

- **Exact edge logic (the wrong rule):** A short simulation gives the exact page ranks.
- **Twin logic (the right rule):** A simulation only estimates the page ranks: RandomSurfer needs 10^n moves to get answers precise to n decimal places and many more moves for those answers to become accurate (tens of thousands of moves for two accurate places, millions for three).
- **Role:** context

**6. `simulation_loop` &rarr; `LoopBodyScopeImpliesLoopLifetime`** (misconception)

- **Exact edge logic (the wrong rule):** Declaring page inside the simulation loop still lets the surfer continue from the previous page.
- **Twin logic (the right rule):** If page is declared inside the loop body it is recreated each pass, so it must be declared before the loop to carry the walk forward.
- **Role:** context

**7. `simulation_loop` &rarr; `OffByOneBound`** (misconception)

- **Exact edge logic (the wrong rule):** t &lt; T and t &lt;= T give the same number of moves.
- **Twin logic (the right rule):** for (t = 0; t &lt; T; t++) makes exactly T moves; with &lt;= it makes T + 1.
- **Role:** context

**8. `accumulator_pattern` &rarr; `LoopBodyScopeImpliesLoopLifetime`** (misconception)

- **Exact edge logic (the wrong rule):** a variable declared in the loop body lives across all iterations
- **Twin logic (the right rule):** A variable declared inside the body is created anew on every pass and does not keep the previous pass's value.
- **Role:** context

**9. `array_bounds` &rarr; `OffByOneBound`** (misconception)

- **Exact edge logic (the wrong rule):** &lt; vs &lt;= and 0..n vs 0..n-1 are interchangeable
- **Twin logic (the right rule):** for (i = 0; i &lt; n; i++) runs n times with i going up to n - 1; with &lt;= it runs n + 1 times and reaches i = n.
- **Role:** context

**10. `array_reversal` &rarr; `OffByOneBound`** (misconception)

- **Exact edge logic (the wrong rule):** &lt; vs &lt;= and 0..n vs 0..n-1 are interchangeable
- **Twin logic (the right rule):** for (i = 0; i &lt; n; i++) runs n times with i going up to n - 1; with &lt;= it runs n + 1 times and reaches i = n.
- **Role:** context

**11. `array_traversal` &rarr; `OffByOneBound`** (misconception)

- **Exact edge logic (the wrong rule):** &lt; vs &lt;= and 0..n vs 0..n-1 are interchangeable
- **Twin logic (the right rule):** for (i = 0; i &lt; n; i++) runs n times with i going up to n - 1; with &lt;= it runs n + 1 times and reaches i = n.
- **Role:** context

**12. `boolean_flag_array` &rarr; `OffByOneBound`** (misconception)

- **Exact edge logic (the wrong rule):** &lt; vs &lt;= and 0..n vs 0..n-1 are interchangeable
- **Twin logic (the right rule):** for (i = 0; i &lt; n; i++) runs n times with i going up to n - 1; with &lt;= it runs n + 1 times and reaches i = n.
- **Role:** context

**13. `frequency_counting` &rarr; `FewTrialsAreExact`** (misconception)

- **Exact edge logic (the wrong rule):** A short simulation gives the exact page ranks.
- **Twin logic (the right rule):** A simulation only estimates the page ranks: RandomSurfer needs 10^n moves to get answers precise to n decimal places and many more moves for those answers to become accurate (tens of thousands of moves for two accurate places, millions for three).
- **Role:** primary

**14. `loop_control` &rarr; `OffByOneBound`** (misconception)

- **Exact edge logic (the wrong rule):** i &lt; n and i &lt;= n mean the same, so the loop runs until i equals n and the last pass can use a[n].
- **Twin logic (the right rule):** for (i = 0; i &lt; n; i++) runs n times with i going up to n - 1; with &lt;= it runs n + 1 times and reaches i = n.
- **Role:** primary

**15. `loop_scope` &rarr; `LoopBodyScopeImpliesLoopLifetime`** (misconception)

- **Exact edge logic (the wrong rule):** A variable declared inside the loop body keeps its value from one pass to the next.
- **Twin logic (the right rule):** A variable declared inside the body is created anew on every pass and does not keep the previous pass's value.
- **Role:** primary

**16. `monte_carlo_simulation` &rarr; `FewTrialsAreExact`** (misconception)

- **Exact edge logic (the wrong rule):** A short simulation gives the exact page ranks.
- **Twin logic (the right rule):** A simulation only estimates the page ranks: RandomSurfer needs 10^n moves to get answers precise to n decimal places and many more moves for those answers to become accurate (tens of thousands of moves for two accurate places, millions for three).
- **Role:** context

**17. `off_by_one_error` &rarr; `OffByOneBound`** (misconception)

- **Exact edge logic (the wrong rule):** &lt; vs &lt;= and 0..n vs 0..n-1 are interchangeable
- **Twin logic (the right rule):** for (i = 0; i &lt; n; i++) runs n times with i going up to n - 1; with &lt;= it runs n + 1 times and reaches i = n.
- **Role:** context

**18. `two_models` &rarr; `FewTrialsAreExact`** (misconception)

- **Exact edge logic (the wrong rule):** A short simulation gives the exact page ranks.
- **Twin logic (the right rule):** A simulation only estimates the page ranks: RandomSurfer needs 10^n moves to get answers precise to n decimal places and many more moves for those answers to become accurate (tens of thousands of moves for two accurate places, millions for three).
- **Role:** context

**19. `variable` &rarr; `LoopBodyScopeImpliesLoopLifetime`** (misconception)

- **Exact edge logic (the wrong rule):** a variable declared in the loop body lives across all iterations
- **Twin logic (the right rule):** A variable declared inside the body is created anew on every pass and does not keep the previous pass's value.
- **Role:** context

**20. `simulation_loop` &rarr; `simulation_loop@L0`** (has_level)

- **Exact edge logic:** simulation loop -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (5 ways).
  - **[0] everyday\_reading** (rule type E, folk-meaning rule): Everyday "simulate" suggests replaying a known process to get its answer; here each run of RandomSurfer draws fresh random numbers and gives different estimates (100 moves: 0.24 0.23 0.16 0.25 0.12), which only approach the page ranks as T grows.
  - **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `OffByOneBound`: wrong rule: &lt; vs &lt;= and 0..n vs 0..n-1 are interchangeable. Right rule: for (int t = 0; t &lt; T; t++) makes exactly T moves; with &lt;= it makes T + 1, while the ranks are still divided by T.
  - **[2] misconception** (rule type M, wrong rule / right rule) &rarr; `FewTrialsAreExact`: wrong rule: A short simulation gives the exact page ranks. Right rule: A simulation only estimates the ranks: about 10^n moves for n-digit precision, tens of thousands of moves for two accurate places and millions for three.
  - **[3] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `OffByOneBound`: Applies LT (draw r, find next page, then freq[page]++) unevenly: e.g. counting the current page before the move on some passes, or resetting sum only on the first pass. (here mixing in: "&lt; vs &lt;= and 0..n vs 0..n-1 are interchangeable")
  - **[4] misconception** (rule type M, wrong rule / right rule) &rarr; `LoopBodyScopeImpliesLoopLifetime`: wrong rule: A variable declared in the loop body lives across all iterations. Right rule: r and sum are declared inside the t-loop body and are created anew on every move; freq and page must be declared before the loop to persist.

**21. `simulation_loop` &rarr; `simulation_loop@L1`** (has_level)

- **Exact edge logic:** simulation loop -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).
  - **[0] names\_the\_element** (rule type N, identity rule): A Monte Carlo simulation: a for loop over t = 0..T-1 that makes one random move per pass and tallies the page reached.
  - **[1] states\_the\_rule** (rule type S, declarative rule): RandomSurfer reads a transition matrix, starts at page 0, makes T moves (T from the command line) according to the matrix, and counts the visits to each page.

**22. `simulation_loop` &rarr; `simulation_loop@L2`** (has_level)

- **Exact edge logic:** simulation loop -&gt; L2 (Multistructural): the answer applies the rules of simulation loop to every part of the code, in order (3 ways).
  - **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): Per pass: r = Math.random(); sum = 0.0; inner j loop picks the next page; freq[page]++; t++ and test t &lt; T. After the loop, each freq[i] is divided by T and printed.
  - **[1] output\_prediction** (rule type OP, evaluation / result rule): Prints N doubles (%8.5f) that sum to about 1 and vary between runs; 1,000,000 moves on tiny.txt gave 0.27324 0.26568 0.14581 0.24737 0.06790.
  - **[2] one\_step\_execution** (rule type OS, state-transition rule): One pass changes page (to the next page) and increases freq[page] by 1; t increases by 1.

**23. `simulation_loop` &rarr; `simulation_loop@L3`** (has_level)

- **Exact edge logic:** simulation loop -&gt; L3 (Relational): the answer relates the parts (5 ways).
  - **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): The loop body is one random move; page carries state from one pass to the next, so each move uses the row of the page reached last.
  - **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): freq[page]++ must come after the move and inside the loop, once per pass, so the counts total T.
  - **[2] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): A counted for loop with t &lt; T fixes the number of moves at T; the loop variable t is scoped to the loop.
  - **[3] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Both compute the same page ranks; the power method gets them exactly with far fewer iterations.
  - **[4] purpose\_of\_the\_whole** (rule type P, plan / role rule): Monte Carlo estimation plan: repeat a random experiment many times and count outcomes; t is a stepper, page a most-recent holder, freq[] the per-page gatherers.

**24. `simulation_loop` &rarr; `simulation_loop@L4`** (has_level)

- **Exact edge logic:** simulation loop -&gt; L4 (Extended abstract): the answer reasons beyond the given code (6 ways).
  - **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `OffByOneBound`: Changing the start page keeps the limit (mixing); increasing T keeps the estimates but makes them more accurate (about 10x moves per extra digit); changing &lt; to &lt;= or the division by T breaks the normalisation.
  - **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Use when the process is easy to simulate and a rough estimate suffices (or no matrix is available); not for accurate ranks or large models, where a huge number of trials is needed and the power method is far more efficient.
  - **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: Loop must run t = 0..T-1. Kind: silent logic error. Trigger class: t &lt;= T makes T+1 moves but ranks are divided by T, so they sum to slightly more than 1.
  - **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: A variable declared in the body is recreated each pass. Kind: silent logic error. Trigger class: int[] freq = new int[N] declared inside the loop body: counts reset every move (and freq is out of scope after the loop, a compile-time error if printed there).
  - **[4] diagnose\_an\_error** (rule type D, error rule): rule broken: freq[i] / T must be floating-point division. Kind: silent logic error. Trigger class: Printing freq[i] / T without the (double) cast: every rank prints as 0 (or 1).
  - **[5] diagnose\_an\_error** (rule type D, error rule): rule broken: The number of moves is args[0]. Kind: run-time exception. Trigger class: Run without a command-line argument: args[0] throws ArrayIndexOutOfBoundsException; a non-numeric argument makes Integer.parseInt throw NumberFormatException.

**25. `topic1.6.b` &rarr; `simulation_loop`** (contains)

- topic `topic1.6.b` contains `simulation_loop`

**26. `topic1.6.b` &rarr; `frequency_counting`** (contains)

- topic `topic1.6.b` contains `frequency_counting`

**27. `topic1.6.b` &rarr; `random_move`** (contains)

- topic `topic1.6.b` contains `random_move`
