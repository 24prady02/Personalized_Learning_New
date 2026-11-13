# counter_pattern (`counter_pattern`)

counting occurrences across passes

Section 1.3 Conditionals and Loops, topic 1.3.f Applications (finite sums, Newton, conversion, gambler's ruin, factoring).

![The knowledge graph around counter_pattern](counter_pattern.png)

## At a glance

- **Needs first:** `increment_operators`, `loop_body`
- **Leads to:** `frequency_counting`, `monte_carlo_simulation`
- **Learned alongside:** `accumulator_pattern`
- **Misconceptions:** `VariableRolesInferred`
- **Errors:** `AccumulatorDeclaredInLoop`
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 27 edges around this concept, each explained in the graph's own words.

## What it needs first (2)

A prerequisite edge means the other concept has to be understood before `counter_pattern`.

### `increment_operators` comes before `counter_pattern`

*++ / -- (and +=)*

A counter is updated with count++, adding one on each pass that matches.

- **Grounding:** book passage

### `loop_body` comes before `counter_pattern`

*the block repeated each pass*

count++ sits inside the body, usually under an if, so it runs once on every pass that matches.

- **Grounding:** order only
- **How `counter_pattern` combines with `loop_body`:** The \`count++\` (with its guard) must be inside the loop body, while the declaration \`int count = 0;\` must be outside and before it. Inside the body it runs once for each matching pass. After the loop it runs only once, so the count is at most 1.
- **How `loop_body` combines with `counter_pattern`:** count++ sits inside the body, often under an if, so it runs once on each pass that matches; the counter is declared before the loop.

## What it leads to (2)

These concepts need `counter_pattern` first.

### `counter_pattern` comes before `frequency_counting`

*tally visits to estimate page rank*

Frequency counting keeps one counter per value in an array, freq[page]++.

- **Grounding:** book passage

### `counter_pattern` comes before `monte_carlo_simulation`

*estimating a probability by repeating random trials*

Counting successes is the counter pattern.

- **Grounding:** book passage
- **How `counter_pattern` combines with `monte_carlo_simulation`:** A Monte Carlo estimate is the counter divided by the number of trials (\`(double) wins / T\`). So the counter has to be initialised once, before the trial loop, and must not be reset inside it.
- **How `monte_carlo_simulation` combines with `counter_pattern`:** Successes are tallied by a counter declared before the trial loop and incremented once per successful trial. The estimate is that counter divided by T, computed as a double or as \`100\*wins/T\` for a whole-number percentage.

## Learned alongside (1)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

### `counter_pattern` alongside `accumulator_pattern`

*building up a running total/result*

An accumulator adds the current value itself on each pass (sum += x); a counter adds 1 on each pass that matches (count++).

- **Grounding:** order only
- **How `counter_pattern` combines with `accumulator_pattern`:** Same skeleton (initialise before, update inside, read after); the accumulator adds the current value (\`sum += x\`), the counter adds the constant 1 on matching passes (\`count++\`). The two are often combined to compute an average \`sum / count\`, which needs a guard against \`count == 0\`.
- **How `accumulator_pattern` combines with `counter_pattern`:** A counter is an accumulator that adds 1 on each pass that matches (count++), whereas an accumulator adds the current value itself (sum += x).

## Misconceptions (1)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### VariableRolesInferred

- **Wrong rule:** The computer recognises that one variable plays two roles, e.g. input value and running total, and keeps the values apart; it knows which variable is the counter and which the sum.
- **Right rule:** A variable holds one value at a time; each role (input, counter, running total) needs its own variable and explicit update.
- **Role of this concept:** context
- **Shows at level L0 as:** misconception: wrong rule: Java recognises which variable is the counter and which is the running total, and keeps their values apart even if one variable is used for both. Right rule: A variable holds one value at a time and Java infers no roles: a counter needs its own variable, initialised before the loop (\`int wins = 0;\`) and updated only by its own statement (\`wins++\`).
- **Also an edge from `accumulator_pattern`:** The computer recognises that one variable plays two roles, e.g. input value and running total, and keeps the values apart; it knows which variable is the counter and which the sum.
- **Also an edge from `variable`:** The computer recognises that one variable plays two roles, e.g. input value and running total, and keeps the values apart; it knows which variable is the counter and which the sum.

## Errors (1)

An error edge states the rule that gets broken in a program, and the right rule.

### AccumulatorDeclaredInLoop

- **Wrong rule:** Declaring sum inside the loop body keeps a running total across passes.
- **Right rule:** The accumulator must be declared and initialised before the loop.
- **Role of this concept:** context
- **Also an edge from `accumulator_pattern`:** Declaring sum inside the loop body keeps a running total across passes.
- **Also an edge from `logical_error`:** Declaring sum inside the loop body keeps a running total across passes.
- **Also an edge from `loop_scope`:** Declaring sum inside the loop body keeps a running total across passes.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for counter pattern: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to counter pattern agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

counter pattern -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (2 ways).

- **everyday reading** (folk-meaning rule): Folk meaning: 'count' in everyday speech is done by looking at the whole collection at once, so a novice expects \`count\` to 'know' how many items matched. In Java a counter is just an int that changes only when \`count++\` executes, once per matching pass, starting from the value it was given before the loop.
- **misconception** (wrong rule / right rule; shows `VariableRolesInferred`): wrong rule: Java recognises which variable is the counter and which is the running total, and keeps their values apart even if one variable is used for both. Right rule: A variable holds one value at a time and Java infers no roles: a counter needs its own variable, initialised before the loop (\`int wins = 0;\`) and updated only by its own statement (\`wins++\`).

### L1: Unistructural / atom x text surface

L1 for counter pattern: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

counter pattern -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

- **names the element** (identity rule): Loop plan (Soloway counter plan): an int variable set to 0 before a loop and increased by 1 on each pass that meets a condition, so it ends holding the number of matches.
- **states the rule** (declarative rule): Declare and initialise the counter before the loop (\`int wins = 0;\`); inside the loop guard \`wins++\` with the condition being counted (\`if (cash == goal) wins++;\`); read it after the loop.

### L2: Multistructural / block x execution / preoperational

L2 for counter pattern: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

counter pattern -&gt; L2 (Multistructural): the answer applies the rules of counter pattern to every part of the code, in order (3 ways).

- **line by line trace** (operational sequencing rule): Order: the initialisation \`count = 0\` runs once before the loop; then on each pass the loop test, the guard (\`if (...)\`) and, only when the guard is true, \`count++\`; the counter is read once after the loop ends.
- **output prediction** (evaluation / result rule): The result is an int equal to the number of passes on which the guard was true (0 if none); it is between 0 and the number of passes. Turning it into a rate with ints truncates: \`100\*wins/T\` with wins = 503, T = 1000 prints 50.
- **one step execution** (state-transition rule): One matching pass changes only the counter, by exactly +1 (\`wins++\` turns 7 into 8); a non-matching pass leaves it unchanged. \`count++\` as a statement returns nothing that is used.

### L3: Relational / relations x function (concrete operational begins)

L3 for counter pattern: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

counter pattern -&gt; L3 (Relational): the answer relates the parts (4 ways).

- **relation to neighbour** (composition rule (with a neighbour)): The \`count++\` (with its guard) must be inside the loop body, while the declaration \`int count = 0;\` must be outside and before it. Inside the body it runs once for each matching pass. After the loop it runs only once, so the count is at most 1.
- **relation to neighbour** (composition rule (with a neighbour)): Same skeleton (initialise before, update inside, read after); the accumulator adds the current value (\`sum += x\`), the counter adds the constant 1 on matching passes (\`count++\`). The two are often combined to compute an average \`sum / count\`, which needs a guard against \`count == 0\`.
- **relation to neighbour** (composition rule (with a neighbour)): A Monte Carlo estimate is the counter divided by the number of trials (\`(double) wins / T\`). So the counter has to be initialised once, before the trial loop, and must not be reset inside it.
- **purpose of the whole** (plan / role rule): Plan: counting plan; the counter variable plays a Sajaniemi 'stepper'-like counting role (Soloway's counter variable). Its job is to answer 'how many passes satisfied P?', e.g. wins or number of bets.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for counter pattern: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

counter pattern -&gt; L4 (Extended abstract): the answer reasons beyond the given code (6 ways).

- **predict a change** (conservation rule): Invariant: after k passes, count equals the number of matching passes among those k. Moving the guard or the update changes the count. Moving \`count++\` out of the \`if\` turns it into a pass counter. Starting at 1 instead of 0 makes every result one too high. Reordering statements that do not touch count leaves it unchanged.
- **diagnose an error** (error rule): rule broken: The counter/accumulator must be declared and initialised before the loop. \`int count = 0;\` inside the body re-creates and resets it on every pass. Kind: silent logic error. Trigger class: Any loop with two or more passes: the count never exceeds 1 (or holds only the last pass).
- **transfer to a new program** (applicability rule): Use a counter when the question is 'how many' (wins, bets, primes, distinct values); use an accumulator when it is 'how much in total', and a boolean flag when you only need 'whether any'. When you need a count for each of many values, use an array of counters (a histogram) instead of many separate variables.
- **diagnose an error** (error rule): rule broken: A variable declared inside the loop body is out of scope after the loop. Kind: compile-time. Trigger class: Printing or using a counter after the loop when it was declared inside the body (cannot find symbol).
- **diagnose an error** (error rule): rule broken: Integer division truncates: a rate computed as \`count / total\` with ints is 0 whenever count &lt; total. Kind: silent logic error. Trigger class: Converting a count to a fraction or percentage with int operands (e.g. \`wins / T\`) instead of \`(double) wins / T\` or \`100\*wins/T\`.
- **diagnose an error** (error rule): rule broken: A local counter must be definitely assigned before it is read. Kind: compile-time. Trigger class: Declaring \`int count;\` without \`= 0\` and then executing \`count++\` (variable might not have been initialized).

## Same topic

`counter_pattern` belongs to the topic **Applications (finite sums, Newton, conversion, gambler's ruin, factoring)** (`topic1.3.f`). The topic also contains: `accumulator_pattern`, `convergence_test`, `debugging`, `fencepost_loop`, `flag_search_loop`, `loop_performance`, `monte_carlo_simulation`, `number_conversion`, `testing`.

## Rules of the concept (18)

- **folk-meaning rule:** Folk meaning: 'count' in everyday speech is done by looking at the whole collection at once, so a novice expects \`count\` to 'know' how many items matched. In Java a counter is just an int that changes only when \`count++\` executes, once per matching pass, starting from the value it was given before the loop.
- **wrong rule / right rule:** VariableRolesInferred: wrong: Java recognises which variable is the counter and which is the running total, and keeps their values apart even if one variable is used for both. \| right: A variable holds one value at a time and Java infers no roles: a counter needs its own variable, initialised before the loop (\`int wins = 0;\`) and updated only by its own statement (\`wins++\`).
- **uneven-application rule:** Applies the LT rule (test the condition, then \`count++\` only on passes where it holds) unevenly: increments on a pass whose test was false, skips one matching pass, or forgets that the counter keeps its value from the previous pass, so the traced final count is off by one or more.
- **identity rule:** Loop plan (Soloway counter plan): an int variable set to 0 before a loop and increased by 1 on each pass that meets a condition, so it ends holding the number of matches.
- **declarative rule:** Declare and initialise the counter before the loop (\`int wins = 0;\`); inside the loop guard \`wins++\` with the condition being counted (\`if (cash == goal) wins++;\`); read it after the loop.
- **operational sequencing rule:** Order: the initialisation \`count = 0\` runs once before the loop; then on each pass the loop test, the guard (\`if (...)\`) and, only when the guard is true, \`count++\`; the counter is read once after the loop ends.
- **evaluation / result rule:** The result is an int equal to the number of passes on which the guard was true (0 if none); it is between 0 and the number of passes. Turning it into a rate with ints truncates: \`100\*wins/T\` with wins = 503, T = 1000 prints 50.
- **state-transition rule:** One matching pass changes only the counter, by exactly +1 (\`wins++\` turns 7 into 8); a non-matching pass leaves it unchanged. \`count++\` as a statement returns nothing that is used.
- **composition rule (with a neighbour):** with loop\_body: The \`count++\` (with its guard) must be inside the loop body, while the declaration \`int count = 0;\` must be outside and before it. Inside the body it runs once for each matching pass. After the loop it runs only once, so the count is at most 1.
- **composition rule (with a neighbour):** with accumulator\_pattern: Same skeleton (initialise before, update inside, read after); the accumulator adds the current value (\`sum += x\`), the counter adds the constant 1 on matching passes (\`count++\`). The two are often combined to compute an average \`sum / count\`, which needs a guard against \`count == 0\`.
- **composition rule (with a neighbour):** with monte\_carlo\_simulation: A Monte Carlo estimate is the counter divided by the number of trials (\`(double) wins / T\`). So the counter has to be initialised once, before the trial loop, and must not be reset inside it.
- **plan / role rule:** Plan: counting plan; the counter variable plays a Sajaniemi 'stepper'-like counting role (Soloway's counter variable). Its job is to answer 'how many passes satisfied P?', e.g. wins or number of bets.
- **conservation rule:** Invariant: after k passes, count equals the number of matching passes among those k. Moving the guard or the update changes the count. Moving \`count++\` out of the \`if\` turns it into a pass counter. Starting at 1 instead of 0 makes every result one too high. Reordering statements that do not touch count leaves it unchanged.
- **error rule:** rule broken: The counter/accumulator must be declared and initialised before the loop. \`int count = 0;\` inside the body re-creates and resets it on every pass. (silent logic error)
- **error rule:** rule broken: A variable declared inside the loop body is out of scope after the loop. (compile-time)
- **error rule:** rule broken: Integer division truncates: a rate computed as \`count / total\` with ints is 0 whenever count &lt; total. (silent logic error)
- **error rule:** rule broken: A local counter must be definitely assigned before it is read. (compile-time)
- **applicability rule:** Use a counter when the question is 'how many' (wins, bets, primes, distinct values); use an accumulator when it is 'how much in total', and a boolean flag when you only need 'whether any'. When you need a count for each of many values, use an array of counters (a histogram) instead of many separate variables.

## The whole prerequisite chain

- **Everything it builds on (20):** `arithmetic_operators`, `assignment`, `boolean`, `boolean_expression`, `comparison_operators`, `data_type`, `declaration`, `do_while_loop`, `expression`, `for_loop`, `identifier`, `increment_operators`, `literal`, `logical_operators`, `loop_body`, `loop_control`, `loop_variable`, `primitive_type`, `variable`, `while_loop`
- **Everything that builds on it (3):** `frequency_counting`, `monte_carlo_simulation`, `two_models`
