# monte_carlo_simulation (`monte_carlo_simulation`)

estimating a probability by repeating random trials

Section 1.3 Conditionals and Loops, topic 1.3.f Applications (finite sums, Newton, conversion, gambler's ruin, factoring).

![The knowledge graph around monte_carlo_simulation](monte_carlo_simulation.png)

## At a glance

- **Needs first:** `counter_pattern`, `math_random`
- **Leads to:** nothing
- **Learned alongside:** nothing
- **Misconceptions:** `FewTrialsAreExact`, `ProbabilityIsPrediction`
- **Errors:** none
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 23 edges around this concept, each explained in the graph's own words.

## What it needs first (2)

A prerequisite edge means the other concept has to be understood before `monte_carlo_simulation`.

### `counter_pattern` comes before `monte_carlo_simulation`

*counting occurrences across passes*

Counting successes is the counter pattern.

- **Grounding:** book passage
- **How `monte_carlo_simulation` combines with `counter_pattern`:** Successes are tallied by a counter declared before the trial loop and incremented once per successful trial. The estimate is that counter divided by T, computed as a double or as \`100\*wins/T\` for a whole-number percentage.
- **How `counter_pattern` combines with `monte_carlo_simulation`:** A Monte Carlo estimate is the counter divided by the number of trials (\`(double) wins / T\`). So the counter has to be initialised once, before the trial loop, and must not be reset inside it.

### `math_random` comes before `monte_carlo_simulation`

*Math.random() and scaling to an int range*

Each trial uses Math.random().

- **Grounding:** book passage
- **How `monte_carlo_simulation` combines with `math_random`:** Each random event is driven by Math.random(), which returns a double in [0, 1). An event of probability p is simulated as \`Math.random() &lt; p\`, e.g. \`&lt; 0.5\` for a fair bet.
- **How `math_random` combines with `monte_carlo_simulation`:** Each trial of a Monte Carlo simulation draws fresh values with Math.random(); estimates become reliable only over many trials.

## What it leads to (0)

These concepts need `monte_carlo_simulation` first.

No concept has this one as a prerequisite.

## Learned alongside (0)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

No parallel edge touches this concept.

## Misconceptions (2)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### FewTrialsAreExact

- **Wrong rule:** A short simulation gives the exact page ranks.
- **Right rule:** A simulation only estimates the page ranks: RandomSurfer needs 10^n moves to get answers precise to n decimal places and many more moves for those answers to become accurate (tens of thousands of moves for two accurate places, millions for three).
- **Role of this concept:** context
- **Shows at level L0 as:** misconception: wrong rule: A short simulation gives the exact page ranks (or probabilities). Right rule: A simulation only estimates: RandomSurfer needs 10^n moves for n-decimal precision and many more for accuracy (tens of thousands of moves for two places, millions for three).
- **Shows at level L0 as:** inconsistent trace: Applies the LT rule (run a trial, update the counters, repeat T times, divide at the end) unevenly: resets the per-trial state (cash = stake) only once rather than once per trial, or divides inside the loop, so the traced estimate mixes trials. (here mixing in: "A short simulation gives the exact page ranks")
- **Also an edge from `frequency_counting`:** A short simulation gives the exact page ranks.
- **Also an edge from `simulation_loop`:** A short simulation gives the exact page ranks.
- **Also an edge from `two_models`:** A short simulation gives the exact page ranks.

### ProbabilityIsPrediction

- **Wrong rule:** A probability (e.g. 70%) predicts what the next single trial will do.
- **Right rule:** A probability describes the long-run frequency over many trials, not one outcome.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: A probability (e.g. 70%) predicts what the next single trial will do. Right rule: A probability is the long-run fraction of successes over many trials. A simulation estimates it as count / trials, and one trial can come out either way.
- **Also an edge from `math_random`:** A probability (e.g. 70%) predicts what the next single trial will do.

## Errors (0)

An error edge states the rule that gets broken in a program, and the right rule.

The graph has no error edge from this concept.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for monte carlo simulation: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to monte carlo simulation agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

monte carlo simulation -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (4 ways).

- **everyday reading** (folk-meaning rule): Folk meaning: in everyday speech a 70% chance or a single experiment 'tells what will happen', and 'random' means unpredictable and never repeating. A Monte Carlo program gives only an estimate (successes / trials) whose accuracy grows with the number of trials, and Math.random() is pseudo-random, not truly random.
- **misconception** (wrong rule / right rule; shows `FewTrialsAreExact`): wrong rule: A short simulation gives the exact page ranks (or probabilities). Right rule: A simulation only estimates: RandomSurfer needs 10^n moves for n-decimal precision and many more for accuracy (tens of thousands of moves for two places, millions for three).
- **misconception** (wrong rule / right rule; shows `ProbabilityIsPrediction`): wrong rule: A probability (e.g. 70%) predicts what the next single trial will do. Right rule: A probability is the long-run fraction of successes over many trials. A simulation estimates it as count / trials, and one trial can come out either way.
- **inconsistent trace** (uneven-application rule; shows `FewTrialsAreExact`): Applies the LT rule (run a trial, update the counters, repeat T times, divide at the end) unevenly: resets the per-trial state (cash = stake) only once rather than once per trial, or divides inside the loop, so the traced estimate mixes trials. (here mixing in: "A short simulation gives the exact page ranks")

### L1: Unistructural / atom x text surface

L1 for monte carlo simulation: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

monte carlo simulation -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

- **names the element** (identity rule): Simulation technique: estimating a probability or expected value by repeating many independent random trials with Math.random() and averaging the outcomes.
- **states the rule** (declarative rule): Run T independent trials in an outer loop, each starting from fresh state; count successes (and accumulate costs). Report \`successes / T\` (and \`total / T\`) as the estimates.

### L2: Multistructural / block x execution / preoperational

L2 for monte carlo simulation: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

monte carlo simulation -&gt; L2 (Multistructural): the answer applies the rules of monte carlo simulation to every part of the code, in order (3 ways).

- **line by line trace** (operational sequencing rule): Order: initialise the counters once; then, for each trial, reset the trial state, run the inner random process to its end (\`while (cash &gt; 0 &amp;&amp; cash &lt; goal)\`), and update the counters; divide and print only after all T trials.
- **output prediction** (evaluation / result rule): The output is an estimate that varies from run to run and gets close to the true value as T grows. Gambler 10 20 1000 prints about 50% wins and about 100 bets, close to the theory: stake/goal and stake × (goal − stake).
- **one step execution** (state-transition rule): One trial resets its own state (cash = stake), consumes random numbers and changes only the summary counters: wins goes up by 0 or 1, and bets goes up by the number of bets made in that trial.

### L3: Relational / relations x function (concrete operational begins)

L3 for monte carlo simulation: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

monte carlo simulation -&gt; L3 (Relational): the answer relates the parts (3 ways).

- **relation to neighbour** (composition rule (with a neighbour)): Each random event is driven by Math.random(), which returns a double in [0, 1). An event of probability p is simulated as \`Math.random() &lt; p\`, e.g. \`&lt; 0.5\` for a fair bet.
- **relation to neighbour** (composition rule (with a neighbour)): Successes are tallied by a counter declared before the trial loop and incremented once per successful trial. The estimate is that counter divided by T, computed as a double or as \`100\*wins/T\` for a whole-number percentage.
- **purpose of the whole** (plan / role rule): Plan: simulate-and-count (Monte Carlo). It answers questions that are hard to solve analytically, and it checks analytic results. Roles: trial index = stepper, wins = counter, bets = gatherer.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for monte carlo simulation: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

monte carlo simulation -&gt; L4 (Extended abstract): the answer reasons beyond the given code (6 ways).

- **predict a change** (conservation rule; shows `FewTrialsAreExact`): Increasing T keeps the expected estimate and narrows its spread (about 10^n trials per decimal digit), but raises running time in proportion to T. Changing the success test or probability changes what is estimated. Re-running with the same T gives a slightly different number.
- **transfer to a new program** (applicability rule): Use Monte Carlo when an answer is a probability or average of a random process that is hard to analyse (gambler's ruin with a bet limit, Monty Hall, random walks, page ranks). Avoid it when an exact formula or deterministic computation exists and is cheap, or when you need more accuracy than the trial budget can give.
- **diagnose an error** (error rule): rule broken: Each trial must start from fresh state. Kind: silent logic error. Trigger class: Declaring or initialising the trial state (\`int cash = stake;\`) before the outer for loop: every trial after the first starts at 0 or goal and ends immediately.
- **diagnose an error** (error rule): rule broken: Estimates from few trials are unreliable. Kind: silent logic error. Trigger class: Small T (e.g. 10 trials): the printed probability can be far from the true value.
- **diagnose an error** (error rule): rule broken: Integer division truncates the estimate. Kind: silent logic error. Trigger class: Computing \`wins / T\` with ints gives 0 whenever wins &lt; T.
- **diagnose an error** (error rule): rule broken: Running time grows with T times the length of each trial. Kind: silent logic error. Trigger class: Large stakes or goals (\`java Gambler 100000 200000 100\`): the program seems to hang.

## Same topic

`monte_carlo_simulation` belongs to the topic **Applications (finite sums, Newton, conversion, gambler's ruin, factoring)** (`topic1.3.f`). The topic also contains: `accumulator_pattern`, `convergence_test`, `counter_pattern`, `debugging`, `fencepost_loop`, `flag_search_loop`, `loop_performance`, `number_conversion`, `testing`.

## Rules of the concept (18)

- **folk-meaning rule:** Folk meaning: in everyday speech a 70% chance or a single experiment 'tells what will happen', and 'random' means unpredictable and never repeating. A Monte Carlo program gives only an estimate (successes / trials) whose accuracy grows with the number of trials, and Math.random() is pseudo-random, not truly random.
- **wrong rule / right rule:** FewTrialsAreExact: wrong: A short simulation gives the exact page ranks (or probabilities). \| right: A simulation only estimates: RandomSurfer needs 10^n moves for n-decimal precision and many more for accuracy (tens of thousands of moves for two places, millions for three).
- **wrong rule / right rule:** ProbabilityIsPrediction: wrong: A probability (e.g. 70%) predicts what the next single trial will do. \| right: A probability is the long-run fraction of successes over many trials. A simulation estimates it as count / trials, and one trial can come out either way.
- **uneven-application rule:** Applies the LT rule (run a trial, update the counters, repeat T times, divide at the end) unevenly: resets the per-trial state (cash = stake) only once rather than once per trial, or divides inside the loop, so the traced estimate mixes trials.
- **identity rule:** Simulation technique: estimating a probability or expected value by repeating many independent random trials with Math.random() and averaging the outcomes.
- **declarative rule:** Run T independent trials in an outer loop, each starting from fresh state; count successes (and accumulate costs). Report \`successes / T\` (and \`total / T\`) as the estimates.
- **operational sequencing rule:** Order: initialise the counters once; then, for each trial, reset the trial state, run the inner random process to its end (\`while (cash &gt; 0 &amp;&amp; cash &lt; goal)\`), and update the counters; divide and print only after all T trials.
- **evaluation / result rule:** The output is an estimate that varies from run to run and gets close to the true value as T grows. Gambler 10 20 1000 prints about 50% wins and about 100 bets, close to the theory: stake/goal and stake × (goal − stake).
- **state-transition rule:** One trial resets its own state (cash = stake), consumes random numbers and changes only the summary counters: wins goes up by 0 or 1, and bets goes up by the number of bets made in that trial.
- **composition rule (with a neighbour):** with math\_random: Each random event is driven by Math.random(), which returns a double in [0, 1). An event of probability p is simulated as \`Math.random() &lt; p\`, e.g. \`&lt; 0.5\` for a fair bet.
- **composition rule (with a neighbour):** with counter\_pattern: Successes are tallied by a counter declared before the trial loop and incremented once per successful trial. The estimate is that counter divided by T, computed as a double or as \`100\*wins/T\` for a whole-number percentage.
- **plan / role rule:** Plan: simulate-and-count (Monte Carlo). It answers questions that are hard to solve analytically, and it checks analytic results. Roles: trial index = stepper, wins = counter, bets = gatherer.
- **conservation rule:** Increasing T keeps the expected estimate and narrows its spread (about 10^n trials per decimal digit), but raises running time in proportion to T. Changing the success test or probability changes what is estimated. Re-running with the same T gives a slightly different number.
- **error rule:** rule broken: Each trial must start from fresh state. (silent logic error)
- **error rule:** rule broken: Estimates from few trials are unreliable. (silent logic error)
- **error rule:** rule broken: Integer division truncates the estimate. (silent logic error)
- **error rule:** rule broken: Running time grows with T times the length of each trial. (silent logic error)
- **applicability rule:** Use Monte Carlo when an answer is a probability or average of a random process that is hard to analyse (gambler's ruin with a bet limit, Monty Hall, random walks, page ranks). Avoid it when an exact formula or deterministic computation exists and is cheap, or when you need more accuracy than the trial budget can give.

## The whole prerequisite chain

- **Everything it builds on (32):** `arithmetic_operators`, `assignment`, `boolean`, `boolean_expression`, `class_declaration`, `command_line_args`, `comparison_operators`, `counter_pattern`, `data_type`, `declaration`, `do_while_loop`, `explicit_cast`, `expression`, `for_loop`, `identifier`, `increment_operators`, `integer_division`, `literal`, `logical_operators`, `loop_body`, `loop_control`, `loop_variable`, `main_method`, `math_library`, `math_random`, `method_call`, `parsing`, `primitive_type`, `program_text`, `type_conversion`, `variable`, `while_loop`
- **Everything that builds on it (0):** nothing
