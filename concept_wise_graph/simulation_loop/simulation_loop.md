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

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 27 edges around this concept, each explained in the graph's own words.

## What it needs first (2)

A prerequisite edge means the other concept has to be understood before `simulation_loop`.

### `for_loop` comes before `simulation_loop`

*a while with init/condition/update packaged together*

The simulation is a for loop over t = 0 ... T - 1 that makes one random move per pass.

- **Grounding:** book passage
- **How `simulation_loop` combines with `for_loop`:** A counted for loop with t &lt; T fixes the number of moves at T; the loop variable t is scoped to the loop.
- **How `for_loop` combines with `simulation_loop`:** A simulation runs a fixed number of trials with an outer for loop (for (int t = 0; t &lt; T; t++)), each trial simulated inside the body.

### `random_move` comes before `simulation_loop`

*pick the next page from a cumulative-probability test*

The simulation repeats the random move T times, each move starting from the page the previous move reached.

- **Grounding:** book passage
- **How `simulation_loop` combines with `random_move`:** The loop body is one random move; page carries state from one pass to the next, so each move uses the row of the page reached last.
- **How `random_move` combines with `simulation_loop`:** Each move starts from the page the previous move produced, and the simulation repeats it T times; the next row used is p[new page].

## What it leads to (1)

These concepts need `simulation_loop` first.

### `simulation_loop` comes before `frequency_counting`

*tally visits to estimate page rank*

On each pass the simulation adds 1 to freq[page] for the page just reached.

- **Grounding:** book passage
- **How `simulation_loop` combines with `frequency_counting`:** freq[page]++ must come after the move and inside the loop, once per pass, so the counts total T.
- **How `frequency_counting` combines with `simulation_loop`:** The increment is the last statement of each pass, so the counts tally the pages reached by the T moves (sum = T).

## Learned alongside (1)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

### `simulation_loop` alongside `power_method`

*repeated vector-matrix multiplication to compute page ranks*

The power method used in Markov is far more efficient than simulating the behavior of a random surfer.

- **Grounding:** book passage
- **How `simulation_loop` combines with `power_method`:** Both compute the same page ranks; the power method gets them exactly with far fewer iterations.
- **How `power_method` combines with `simulation_loop`:** Computes the same ranks far more efficiently than simulating moves.

## Misconceptions (3)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### FewTrialsAreExact

- **Wrong rule:** A short simulation gives the exact page ranks.
- **Right rule:** A simulation only estimates the page ranks: RandomSurfer needs 10^n moves to get answers precise to n decimal places and many more moves for those answers to become accurate (tens of thousands of moves for two accurate places, millions for three).
- **Role of this concept:** context
- **Shows at level L0 as:** misconception: wrong rule: A short simulation gives the exact page ranks. Right rule: A simulation only estimates the ranks: about 10^n moves for n-digit precision, tens of thousands of moves for two accurate places and millions for three.
- **Also an edge from `frequency_counting`:** A short simulation gives the exact page ranks.
- **Also an edge from `monte_carlo_simulation`:** A short simulation gives the exact page ranks.
- **Also an edge from `two_models`:** A short simulation gives the exact page ranks.

### LoopBodyScopeImpliesLoopLifetime

- **Wrong rule:** Declaring page inside the simulation loop still lets the surfer continue from the previous page.
- **Right rule:** If page is declared inside the loop body it is recreated each pass, so it must be declared before the loop to carry the walk forward.
- **Role of this concept:** context
- **Shows at level L0 as:** misconception: wrong rule: A variable declared in the loop body lives across all iterations. Right rule: r and sum are declared inside the t-loop body and are created anew on every move; freq and page must be declared before the loop to persist.
- **Also an edge from `accumulator_pattern`:** a variable declared in the loop body lives across all iterations
- **Also an edge from `loop_scope`:** A variable declared inside the loop body keeps its value from one pass to the next.
- **Also an edge from `variable`:** a variable declared in the loop body lives across all iterations

### OffByOneBound

- **Wrong rule:** t &lt; T and t &lt;= T give the same number of moves.
- **Right rule:** for (t = 0; t &lt; T; t++) makes exactly T moves; with &lt;= it makes T + 1.
- **Role of this concept:** context
- **Shows at level L0 as:** misconception: wrong rule: &lt; vs &lt;= and 0..n vs 0..n-1 are interchangeable. Right rule: for (int t = 0; t &lt; T; t++) makes exactly T moves; with &lt;= it makes T + 1, while the ranks are still divided by T.
- **Shows at level L0 as:** inconsistent trace: Applies LT (draw r, find next page, then freq[page]++) unevenly: e.g. counting the current page before the move on some passes, or resetting sum only on the first pass. (here mixing in: "&lt; vs &lt;= and 0..n vs 0..n-1 are interchangeable")
- **Also an edge from `array_bounds`:** &lt; vs &lt;= and 0..n vs 0..n-1 are interchangeable
- **Also an edge from `array_reversal`:** &lt; vs &lt;= and 0..n vs 0..n-1 are interchangeable
- **Also an edge from `array_traversal`:** &lt; vs &lt;= and 0..n vs 0..n-1 are interchangeable
- **Also an edge from `boolean_flag_array`:** &lt; vs &lt;= and 0..n vs 0..n-1 are interchangeable
- **Also an edge from `loop_control`:** i &lt; n and i &lt;= n mean the same, so the loop runs until i equals n and the last pass can use a[n].
- **Also an edge from `off_by_one_error`:** &lt; vs &lt;= and 0..n vs 0..n-1 are interchangeable

## Errors (0)

An error edge states the rule that gets broken in a program, and the right rule.

The graph has no error edge from this concept.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for simulation loop: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to simulation loop agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

simulation loop -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (5 ways).

- **everyday reading** (folk-meaning rule): Everyday "simulate" suggests replaying a known process to get its answer; here each run of RandomSurfer draws fresh random numbers and gives different estimates (100 moves: 0.24 0.23 0.16 0.25 0.12), which only approach the page ranks as T grows.
- **misconception** (wrong rule / right rule; shows `OffByOneBound`): wrong rule: &lt; vs &lt;= and 0..n vs 0..n-1 are interchangeable. Right rule: for (int t = 0; t &lt; T; t++) makes exactly T moves; with &lt;= it makes T + 1, while the ranks are still divided by T.
- **misconception** (wrong rule / right rule; shows `FewTrialsAreExact`): wrong rule: A short simulation gives the exact page ranks. Right rule: A simulation only estimates the ranks: about 10^n moves for n-digit precision, tens of thousands of moves for two accurate places and millions for three.
- **inconsistent trace** (uneven-application rule; shows `OffByOneBound`): Applies LT (draw r, find next page, then freq[page]++) unevenly: e.g. counting the current page before the move on some passes, or resetting sum only on the first pass. (here mixing in: "&lt; vs &lt;= and 0..n vs 0..n-1 are interchangeable")
- **misconception** (wrong rule / right rule; shows `LoopBodyScopeImpliesLoopLifetime`): wrong rule: A variable declared in the loop body lives across all iterations. Right rule: r and sum are declared inside the t-loop body and are created anew on every move; freq and page must be declared before the loop to persist.

### L1: Unistructural / atom x text surface

L1 for simulation loop: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

simulation loop -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

- **names the element** (identity rule): A Monte Carlo simulation: a for loop over t = 0..T-1 that makes one random move per pass and tallies the page reached.
- **states the rule** (declarative rule): RandomSurfer reads a transition matrix, starts at page 0, makes T moves (T from the command line) according to the matrix, and counts the visits to each page.

### L2: Multistructural / block x execution / preoperational

L2 for simulation loop: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

simulation loop -&gt; L2 (Multistructural): the answer applies the rules of simulation loop to every part of the code, in order (3 ways).

- **line by line trace** (operational sequencing rule): Per pass: r = Math.random(); sum = 0.0; inner j loop picks the next page; freq[page]++; t++ and test t &lt; T. After the loop, each freq[i] is divided by T and printed.
- **output prediction** (evaluation / result rule): Prints N doubles (%8.5f) that sum to about 1 and vary between runs; 1,000,000 moves on tiny.txt gave 0.27324 0.26568 0.14581 0.24737 0.06790.
- **one step execution** (state-transition rule): One pass changes page (to the next page) and increases freq[page] by 1; t increases by 1.

### L3: Relational / relations x function (concrete operational begins)

L3 for simulation loop: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

simulation loop -&gt; L3 (Relational): the answer relates the parts (5 ways).

- **relation to neighbour** (composition rule (with a neighbour)): The loop body is one random move; page carries state from one pass to the next, so each move uses the row of the page reached last.
- **relation to neighbour** (composition rule (with a neighbour)): freq[page]++ must come after the move and inside the loop, once per pass, so the counts total T.
- **relation to neighbour** (composition rule (with a neighbour)): A counted for loop with t &lt; T fixes the number of moves at T; the loop variable t is scoped to the loop.
- **relation to neighbour** (composition rule (with a neighbour)): Both compute the same page ranks; the power method gets them exactly with far fewer iterations.
- **purpose of the whole** (plan / role rule): Monte Carlo estimation plan: repeat a random experiment many times and count outcomes; t is a stepper, page a most-recent holder, freq[] the per-page gatherers.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for simulation loop: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

simulation loop -&gt; L4 (Extended abstract): the answer reasons beyond the given code (6 ways).

- **predict a change** (conservation rule; shows `OffByOneBound`): Changing the start page keeps the limit (mixing); increasing T keeps the estimates but makes them more accurate (about 10x moves per extra digit); changing &lt; to &lt;= or the division by T breaks the normalisation.
- **transfer to a new program** (applicability rule): Use when the process is easy to simulate and a rough estimate suffices (or no matrix is available); not for accurate ranks or large models, where a huge number of trials is needed and the power method is far more efficient.
- **diagnose an error** (error rule): rule broken: Loop must run t = 0..T-1. Kind: silent logic error. Trigger class: t &lt;= T makes T+1 moves but ranks are divided by T, so they sum to slightly more than 1.
- **diagnose an error** (error rule): rule broken: A variable declared in the body is recreated each pass. Kind: silent logic error. Trigger class: int[] freq = new int[N] declared inside the loop body: counts reset every move (and freq is out of scope after the loop, a compile-time error if printed there).
- **diagnose an error** (error rule): rule broken: freq[i] / T must be floating-point division. Kind: silent logic error. Trigger class: Printing freq[i] / T without the (double) cast: every rank prints as 0 (or 1).
- **diagnose an error** (error rule): rule broken: The number of moves is args[0]. Kind: run-time exception. Trigger class: Run without a command-line argument: args[0] throws ArrayIndexOutOfBoundsException; a non-numeric argument makes Integer.parseInt throw NumberFormatException.

## Same topic

`simulation_loop` belongs to the topic **Simulation (one random move, page ranks)** (`topic1.6.b`). The topic also contains: `frequency_counting`, `random_move`.

## Rules of the concept (21)

- **folk-meaning rule:** Everyday "simulate" suggests replaying a known process to get its answer; here each run of RandomSurfer draws fresh random numbers and gives different estimates (100 moves: 0.24 0.23 0.16 0.25 0.12), which only approach the page ranks as T grows.
- **wrong rule / right rule:** FewTrialsAreExact: wrong: A short simulation gives the exact page ranks. \| right: A simulation only estimates the ranks: about 10^n moves for n-digit precision, tens of thousands of moves for two accurate places and millions for three.
- **wrong rule / right rule:** LoopBodyScopeImpliesLoopLifetime: wrong: A variable declared in the loop body lives across all iterations. \| right: r and sum are declared inside the t-loop body and are created anew on every move; freq and page must be declared before the loop to persist.
- **wrong rule / right rule:** OffByOneBound: wrong: &lt; vs &lt;= and 0..n vs 0..n-1 are interchangeable. \| right: for (int t = 0; t &lt; T; t++) makes exactly T moves; with &lt;= it makes T + 1, while the ranks are still divided by T.
- **uneven-application rule:** Applies LT (draw r, find next page, then freq[page]++) unevenly: e.g. counting the current page before the move on some passes, or resetting sum only on the first pass.
- **identity rule:** A Monte Carlo simulation: a for loop over t = 0..T-1 that makes one random move per pass and tallies the page reached.
- **declarative rule:** RandomSurfer reads a transition matrix, starts at page 0, makes T moves (T from the command line) according to the matrix, and counts the visits to each page.
- **operational sequencing rule:** Per pass: r = Math.random(); sum = 0.0; inner j loop picks the next page; freq[page]++; t++ and test t &lt; T. After the loop, each freq[i] is divided by T and printed.
- **evaluation / result rule:** Prints N doubles (%8.5f) that sum to about 1 and vary between runs; 1,000,000 moves on tiny.txt gave 0.27324 0.26568 0.14581 0.24737 0.06790.
- **state-transition rule:** One pass changes page (to the next page) and increases freq[page] by 1; t increases by 1.
- **composition rule (with a neighbour):** with random\_move: The loop body is one random move; page carries state from one pass to the next, so each move uses the row of the page reached last.
- **composition rule (with a neighbour):** with frequency\_counting: freq[page]++ must come after the move and inside the loop, once per pass, so the counts total T.
- **composition rule (with a neighbour):** with for\_loop: A counted for loop with t &lt; T fixes the number of moves at T; the loop variable t is scoped to the loop.
- **composition rule (with a neighbour):** with power\_method: Both compute the same page ranks; the power method gets them exactly with far fewer iterations.
- **plan / role rule:** Monte Carlo estimation plan: repeat a random experiment many times and count outcomes; t is a stepper, page a most-recent holder, freq[] the per-page gatherers.
- **conservation rule:** Changing the start page keeps the limit (mixing); increasing T keeps the estimates but makes them more accurate (about 10x moves per extra digit); changing &lt; to &lt;= or the division by T breaks the normalisation.
- **error rule:** rule broken: Loop must run t = 0..T-1. (silent logic error)
- **error rule:** rule broken: A variable declared in the body is recreated each pass. (silent logic error)
- **error rule:** rule broken: freq[i] / T must be floating-point division. (silent logic error)
- **error rule:** rule broken: The number of moves is args[0]. (run-time exception)
- **applicability rule:** Use when the process is easy to simulate and a rough estimate suffices (or no matrix is available); not for accurate ranks or large models, where a huge number of trials is needed and the power method is far more efficient.

## The whole prerequisite chain

- **Everything it builds on (30):** `arithmetic_operators`, `array_creation`, `array_declaration`, `array_initializer`, `boolean`, `boolean_expression`, `comparison_operators`, `data_structure`, `data_type`, `do_while_loop`, `expression`, `for_loop`, `identifier`, `indexing`, `input_graph`, `literal`, `logical_operators`, `loop_control`, `loop_variable`, `math_library`, `method_call`, `primitive_type`, `random_move`, `standard_input`, `stream_model`, `teleportation`, `transition_matrix`, `two_dimensional_array`, `variable`, `while_loop`
- **Everything that builds on it (2):** `frequency_counting`, `two_models`
