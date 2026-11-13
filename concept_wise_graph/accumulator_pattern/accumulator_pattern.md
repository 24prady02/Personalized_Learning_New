# accumulator_pattern (`accumulator_pattern`)

building up a running total/result

Section 1.3 Conditionals and Loops, topic 1.3.f Applications (finite sums, Newton, conversion, gambler's ruin, factoring).

![The knowledge graph around accumulator_pattern](accumulator_pattern.png)

## At a glance

- **Needs first:** `compound_assignment`, `loop_body`
- **Leads to:** `sentinel_loop`
- **Learned alongside:** `counter_pattern`, `running_extreme`
- **Misconceptions:** `LoopBodyScopeImpliesLoopLifetime`, `StateChangeIgnoredAcrossPasses`, `VariableRolesInferred`
- **Errors:** `AccumulatorDeclaredInLoop`
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 34 edges around this concept, each explained in the graph's own words.

## What it needs first (2)

A prerequisite edge means the other concept has to be understood before `accumulator_pattern`.

### `compound_assignment` comes before `accumulator_pattern`

*x += e, x -= e, ... include a hidden cast*

sum += x is the usual way a running total is updated on each pass.

- **Grounding:** book passage

### `loop_body` comes before `accumulator_pattern`

*the block repeated each pass*

The accumulator update sum += x sits inside the body, so it runs once on every pass.

- **Grounding:** book passage
- **How `accumulator_pattern` combines with `loop_body`:** The update sum += x sits inside the body so it runs once per pass, while the declaration and initialization stay before the loop.
- **How `loop_body` combines with `accumulator_pattern`:** The accumulator update (sum += x) is placed inside the body so it runs once per pass, while the accumulator is declared and initialized before the loop.

## What it leads to (1)

These concepts need `accumulator_pattern` first.

### `accumulator_pattern` comes before `sentinel_loop`

*reading until a special stop value (Rainfall problem)*

Sum and count are accumulators.

- **Grounding:** questionable
- **How `accumulator_pattern` combines with `sentinel_loop`:** In a sentinel loop the sum and the count of the values read are both accumulators, updated only for values that are not the sentinel.
- **How `sentinel_loop` combines with `accumulator_pattern`:** sum (a gatherer) and count must change only for values that are not the sentinel and pass the filter. The average is computed once, after the loop.

## Learned alongside (2)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

### `accumulator_pattern` alongside `counter_pattern`

*counting occurrences across passes*

An accumulator adds the current value itself on each pass (sum += x); a counter adds 1 on each pass that matches (count++).

- **Grounding:** order only
- **How `accumulator_pattern` combines with `counter_pattern`:** A counter is an accumulator that adds 1 on each pass that matches (count++), whereas an accumulator adds the current value itself (sum += x).
- **How `counter_pattern` combines with `accumulator_pattern`:** Same skeleton (initialise before, update inside, read after); the accumulator adds the current value (\`sum += x\`), the counter adds the constant 1 on matching passes (\`count++\`). The two are often combined to compute an average \`sum / count\`, which needs a guard against \`count == 0\`.

### `accumulator_pattern` alongside `running_extreme`

*tracking the max or min of a stream*

Both make one pass over the values with one variable kept across passes. An accumulator (gatherer role) combines every value into it (sum += a[i]), so it starts at the identity 0.0; a running extreme (most-wanted holder) replaces it only when a better value is found (if (a[i] &gt; max) max = a[i]), so it starts at Double.NEGATIVE\_INFINITY or the first value.

- **Grounding:** book passage

## Misconceptions (3)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### LoopBodyScopeImpliesLoopLifetime

- **Wrong rule:** a variable declared in the loop body lives across all iterations
- **Right rule:** A variable declared inside the body is created anew on every pass and does not keep the previous pass's value.
- **Role of this concept:** context
- **Shows at level L0 as:** misconception: wrong rule: a variable declared in the loop body lives across all iterations. Right rule: A variable declared inside the body is in scope only to the end of the body, so each pass declares and initializes it afresh and it does not keep the previous pass's value.
- **Shows at level L0 as:** inconsistent trace: Applies the update rule (LT) unevenly: adds the new value to the previous total on some passes but restarts from the initial value (or forgets to add) on others. (here mixing in: "a variable declared in the loop body lives across all iterations")
- **Also an edge from `loop_scope`:** A variable declared inside the loop body keeps its value from one pass to the next.
- **Also an edge from `simulation_loop`:** Declaring page inside the simulation loop still lets the surfer continue from the previous page.
- **Also an edge from `variable`:** a variable declared in the loop body lives across all iterations

### StateChangeIgnoredAcrossPasses

- **Wrong rule:** Values changed by one pass of a loop (other than the loop variable) do not affect later passes.
- **Right rule:** Each pass starts from the state left by the previous pass, so a change in one pass carries into the next ones.
- **Role of this concept:** context
- **Shows at level L0 as:** misconception: wrong rule: Values changed by one pass of a loop (other than the loop variable) do not affect later passes. Right rule: Each pass starts from the state left by the previous pass, so a change in one pass carries into the next ones.
- **Also an edge from `loop_body`:** Values changed by one pass of a loop (other than the loop variable) do not affect later passes.
- **Also an edge from `program_state`:** Values changed by one pass of a loop (other than the loop variable) do not affect later passes.

### VariableRolesInferred

- **Wrong rule:** The computer recognises that one variable plays two roles, e.g. input value and running total, and keeps the values apart; it knows which variable is the counter and which the sum.
- **Right rule:** A variable holds one value at a time; each role (input, counter, running total) needs its own variable and explicit update.
- **Role of this concept:** context
- **Shows at level L0 as:** misconception: wrong rule: The computer recognises that one variable plays two roles, e.g. input value and running total, and keeps the values apart; it knows which variable is the counter and which the sum. Right rule: A variable holds one value at a time; each role (input, counter, running total) needs its own variable and explicit update.
- **Also an edge from `counter_pattern`:** The computer recognises that one variable plays two roles, e.g. input value and running total, and keeps the values apart; it knows which variable is the counter and which the sum.
- **Also an edge from `variable`:** The computer recognises that one variable plays two roles, e.g. input value and running total, and keeps the values apart; it knows which variable is the counter and which the sum.

## Errors (1)

An error edge states the rule that gets broken in a program, and the right rule.

### AccumulatorDeclaredInLoop

- **Wrong rule:** Declaring sum inside the loop body keeps a running total across passes.
- **Right rule:** The accumulator must be declared and initialised before the loop.
- **Role of this concept:** context
- **Also an edge from `counter_pattern`:** Declaring sum inside the loop body keeps a running total across passes.
- **Also an edge from `logical_error`:** Declaring sum inside the loop body keeps a running total across passes.
- **Also an edge from `loop_scope`:** Declaring sum inside the loop body keeps a running total across passes.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for accumulator pattern: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to accumulator pattern agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

accumulator pattern -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (5 ways).

- **everyday reading** (folk-meaning rule): Folk meaning: 'the sum' is a single mathematical quantity that simply exists, and a person adding numbers keeps the running total in mind automatically. In Java the total is a variable that must be declared and initialized before the loop and explicitly updated on every pass (sum += x).
- **misconception** (wrong rule / right rule; shows `LoopBodyScopeImpliesLoopLifetime`): wrong rule: a variable declared in the loop body lives across all iterations. Right rule: A variable declared inside the body is in scope only to the end of the body, so each pass declares and initializes it afresh and it does not keep the previous pass's value.
- **inconsistent trace** (uneven-application rule; shows `LoopBodyScopeImpliesLoopLifetime`): Applies the update rule (LT) unevenly: adds the new value to the previous total on some passes but restarts from the initial value (or forgets to add) on others. (here mixing in: "a variable declared in the loop body lives across all iterations")
- **misconception** (wrong rule / right rule; shows `VariableRolesInferred`): wrong rule: The computer recognises that one variable plays two roles, e.g. input value and running total, and keeps the values apart; it knows which variable is the counter and which the sum. Right rule: A variable holds one value at a time; each role (input, counter, running total) needs its own variable and explicit update.
- **misconception** (wrong rule / right rule; shows `StateChangeIgnoredAcrossPasses`): wrong rule: Values changed by one pass of a loop (other than the loop variable) do not affect later passes. Right rule: Each pass starts from the state left by the previous pass, so a change in one pass carries into the next ones.

### L1: Unistructural / atom x text surface

L1 for accumulator pattern: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

accumulator pattern -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

- **names the element** (identity rule): An accumulator is a variable used to accumulate results during a traversal, e.g. the running total of a sum.
- **states the rule** (declarative rule): Initialize the accumulator before the loop (0 for a sum, 1 for a product), update it once per pass in the body (total += array[i]), and use it after the loop.

### L2: Multistructural / block x execution / preoperational

L2 for accumulator pattern: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

accumulator pattern -&gt; L2 (Multistructural): the answer applies the rules of accumulator pattern to every part of the code, in order (3 ways).

- **line by line trace** (operational sequencing rule): Before the loop: total = initial value. Each pass: read total, combine with the current item, store back. After the loop: total holds the combination of all items.
- **output prediction** (evaluation / result rule): After the loop the accumulator holds the reduce result: sum of 1..N is N(N+1)/2; Harmonic(2) = 1.5; the product loop gives N!.
- **one step execution** (state-transition rule): One pass changes only the accumulator (and the loop variable): sum += x[i] turns sum = 1 into 5 when x[i] = 4.

### L3: Relational / relations x function (concrete operational begins)

L3 for accumulator pattern: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

accumulator pattern -&gt; L3 (Relational): the answer relates the parts (5 ways).

- **relation to neighbour** (composition rule (with a neighbour)): The update sum += x sits inside the body so it runs once per pass, while the declaration and initialization stay before the loop.
- **relation to neighbour** (composition rule (with a neighbour)): A counter is an accumulator that adds 1 on each pass that matches (count++), whereas an accumulator adds the current value itself (sum += x).
- **relation to neighbour** (composition rule (with a neighbour)): In a sentinel loop the sum and the count of the values read are both accumulators, updated only for values that are not the sentinel.
- **relation to neighbour** (composition rule (with a neighbour)): Both make one pass over the values with one variable kept across passes. An accumulator (gatherer role) combines every value into it (sum += a[i]), so it starts at the identity 0.0; a running extreme (most-wanted holder) replaces it only when a better value is found (if (a[i] &gt; max) max = a[i]), so it starts at Double.NEGATIVE\_INFINITY or the first value.
- **purpose of the whole** (plan / role rule): Role: gatherer - a data item accumulating the effect of individual values (running total, product, concatenated string).

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for accumulator pattern: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

accumulator pattern -&gt; L4 (Extended abstract): the answer reasons beyond the given code (5 ways).

- **predict a change** (conservation rule; shows `LoopBodyScopeImpliesLoopLifetime`): Changing the initial value shifts the result by that amount (sum starts at 1 gives sum + 1); a product starting at 0 stays 0; reordering the items does not change an integer sum (addition is commutative) but may change a floating-point sum slightly.
- **diagnose an error** (error rule): rule broken: A variable declared in the body is in scope only to the end of the body and is re-declared and re-initialized on every pass. Kind: silent logic error. Trigger class: for (...) { int sum = 0; sum += a[i]; }: sum restarts at 0 each pass, so only the last term survives; printing sum after the loop is a compile-time error (cannot find symbol) because sum is out of scope.
- **transfer to a new program** (applicability rule): Use an accumulator whenever many values must be reduced to one (sum, product, average, string); for a maximum or minimum use a most-wanted holder updated by an if instead.
- **diagnose an error** (error rule): rule broken: The accumulator must be initialized before the loop. Kind: compile-time. Trigger class: Declaring int sum; and then sum += x in the loop: 'variable sum might not have been initialized'.
- **diagnose an error** (error rule): rule broken: A sum must start at 0 and a product at 1. Kind: silent logic error. Trigger class: product initialized to 0 (result always 0) or sum initialized to the first element and then adding it again (first element counted twice).

## Same topic

`accumulator_pattern` belongs to the topic **Applications (finite sums, Newton, conversion, gambler's ruin, factoring)** (`topic1.3.f`). The topic also contains: `convergence_test`, `counter_pattern`, `debugging`, `fencepost_loop`, `flag_search_loop`, `loop_performance`, `monte_carlo_simulation`, `number_conversion`, `testing`.

## Rules of the concept (19)

- **folk-meaning rule:** Folk meaning: 'the sum' is a single mathematical quantity that simply exists, and a person adding numbers keeps the running total in mind automatically. In Java the total is a variable that must be declared and initialized before the loop and explicitly updated on every pass (sum += x).
- **wrong rule / right rule:** LoopBodyScopeImpliesLoopLifetime: wrong: a variable declared in the loop body lives across all iterations \| right: A variable declared inside the body is in scope only to the end of the body, so each pass declares and initializes it afresh and it does not keep the previous pass's value.
- **wrong rule / right rule:** VariableRolesInferred: wrong: The computer recognises that one variable plays two roles, e.g. input value and running total, and keeps the values apart; it knows which variable is the counter and which the sum. \| right: A variable holds one value at a time; each role (input, counter, running total) needs its own variable and explicit update.
- **wrong rule / right rule:** StateChangeIgnoredAcrossPasses: wrong: Values changed by one pass of a loop (other than the loop variable) do not affect later passes. \| right: Each pass starts from the state left by the previous pass, so a change in one pass carries into the next ones.
- **uneven-application rule:** Applies the update rule (LT) unevenly: adds the new value to the previous total on some passes but restarts from the initial value (or forgets to add) on others.
- **identity rule:** An accumulator is a variable used to accumulate results during a traversal, e.g. the running total of a sum.
- **declarative rule:** Initialize the accumulator before the loop (0 for a sum, 1 for a product), update it once per pass in the body (total += array[i]), and use it after the loop.
- **operational sequencing rule:** Before the loop: total = initial value. Each pass: read total, combine with the current item, store back. After the loop: total holds the combination of all items.
- **evaluation / result rule:** After the loop the accumulator holds the reduce result: sum of 1..N is N(N+1)/2; Harmonic(2) = 1.5; the product loop gives N!.
- **state-transition rule:** One pass changes only the accumulator (and the loop variable): sum += x[i] turns sum = 1 into 5 when x[i] = 4.
- **composition rule (with a neighbour):** with loop\_body: The update sum += x sits inside the body so it runs once per pass, while the declaration and initialization stay before the loop.
- **composition rule (with a neighbour):** with counter\_pattern: A counter is an accumulator that adds 1 on each pass that matches (count++), whereas an accumulator adds the current value itself (sum += x).
- **composition rule (with a neighbour):** with sentinel\_loop: In a sentinel loop the sum and the count of the values read are both accumulators, updated only for values that are not the sentinel.
- **plan / role rule:** Role: gatherer - a data item accumulating the effect of individual values (running total, product, concatenated string).
- **conservation rule:** Changing the initial value shifts the result by that amount (sum starts at 1 gives sum + 1); a product starting at 0 stays 0; reordering the items does not change an integer sum (addition is commutative) but may change a floating-point sum slightly.
- **error rule:** rule broken: A variable declared in the body is in scope only to the end of the body and is re-declared and re-initialized on every pass. (silent logic error)
- **error rule:** rule broken: The accumulator must be initialized before the loop. (compile-time)
- **error rule:** rule broken: A sum must start at 0 and a product at 1. (silent logic error)
- **applicability rule:** Use an accumulator whenever many values must be reduced to one (sum, product, average, string); for a maximum or minimum use a most-wanted holder updated by an if instead.

## The whole prerequisite chain

- **Everything it builds on (28):** `arithmetic_operators`, `assignment`, `boolean`, `boolean_expression`, `class_declaration`, `command_line_args`, `comparison_operators`, `compound_assignment`, `data_type`, `declaration`, `do_while_loop`, `explicit_cast`, `expression`, `for_loop`, `identifier`, `integer_division`, `literal`, `logical_operators`, `loop_body`, `loop_control`, `loop_variable`, `main_method`, `parsing`, `primitive_type`, `program_text`, `type_conversion`, `variable`, `while_loop`
- **Everything that builds on it (1):** `sentinel_loop`
