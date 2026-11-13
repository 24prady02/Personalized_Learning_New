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

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 34 edges around this concept. The edge logic, the wrong and right rules and the exact rules of the ways are copied word for word from the graph.

## To work on (0)

Nothing is missing for this concept.

## What it needs first (2)

A prerequisite edge means the other concept has to be understood before `accumulator_pattern`.

### `compound_assignment` comes before `accumulator_pattern`

*x += e, x -= e, ... include a hidden cast*

- **Edge:** `pre:compound_assignment->accumulator_pattern`
- **Exact edge logic:** sum += x is the usual way a running total is updated on each pass.
- **Grounding:** book\_passage

### `loop_body` comes before `accumulator_pattern`

*the block repeated each pass*

- **Edge:** `pre:loop_body->accumulator_pattern`
- **Exact edge logic:** The accumulator update sum += x sits inside the body, so it runs once on every pass.
- **Grounding:** book\_passage
- **Composition rule (R) of `accumulator_pattern` with `loop_body`:** The update sum += x sits inside the body so it runs once per pass, while the declaration and initialization stay before the loop.
- **Composition rule (R) of `loop_body` with `accumulator_pattern`:** The accumulator update (sum += x) is placed inside the body so it runs once per pass, while the accumulator is declared and initialized before the loop.

## What it leads to (1)

These concepts need `accumulator_pattern` first.

### `accumulator_pattern` comes before `sentinel_loop`

*reading until a special stop value (Rainfall problem)*

- **Edge:** `pre:accumulator_pattern->sentinel_loop`
- **Exact edge logic:** Sum and count are accumulators.
- **Grounding:** questionable
- **Composition rule (R) of `accumulator_pattern` with `sentinel_loop`:** In a sentinel loop the sum and the count of the values read are both accumulators, updated only for values that are not the sentinel.
- **Composition rule (R) of `sentinel_loop` with `accumulator_pattern`:** sum (a gatherer) and count must change only for values that are not the sentinel and pass the filter. The average is computed once, after the loop.

## Learned alongside (2)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

### `accumulator_pattern` alongside `counter_pattern`

*counting occurrences across passes*

- **Edge:** `par:accumulator_pattern~counter_pattern`
- **Exact edge logic:** An accumulator adds the current value itself on each pass (sum += x); a counter adds 1 on each pass that matches (count++).
- **Grounding:** order\_only
- **Composition rule (R) of `accumulator_pattern` with `counter_pattern`:** A counter is an accumulator that adds 1 on each pass that matches (count++), whereas an accumulator adds the current value itself (sum += x).
- **Composition rule (R) of `counter_pattern` with `accumulator_pattern`:** Same skeleton (initialise before, update inside, read after); the accumulator adds the current value (\`sum += x\`), the counter adds the constant 1 on matching passes (\`count++\`). The two are often combined to compute an average \`sum / count\`, which needs a guard against \`count == 0\`.

### `accumulator_pattern` alongside `running_extreme`

*tracking the max or min of a stream*

- **Edge:** `par:running_extreme~accumulator_pattern`
- **Exact edge logic:** Both make one pass over the values with one variable kept across passes. An accumulator (gatherer role) combines every value into it (sum += a[i]), so it starts at the identity 0.0; a running extreme (most-wanted holder) replaces it only when a better value is found (if (a[i] &gt; max) max = a[i]), so it starts at Double.NEGATIVE\_INFINITY or the first value.
- **Grounding:** book\_passage

## Misconceptions (3)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### LoopBodyScopeImpliesLoopLifetime

- **Edge:** `accumulator_pattern` &rarr; `LoopBodyScopeImpliesLoopLifetime` (misconception)
- **Exact edge logic (the wrong rule):** a variable declared in the loop body lives across all iterations
- **Twin logic (the right rule):** A variable declared inside the body is created anew on every pass and does not keep the previous pass's value.
- **Wrong belief (on the node):** a variable declared in the loop body lives across all iterations
- **Correct rule (on the node):** A variable declared inside the body is created anew on every pass and does not keep the previous pass's value.
- **Provenance:** published
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [1] misconception, exact rule:** wrong rule: a variable declared in the loop body lives across all iterations. Right rule: A variable declared inside the body is in scope only to the end of the body, so each pass declares and initializes it afresh and it does not keep the previous pass's value.
- **L0 way [2] inconsistent\_trace, exact rule:** Applies the update rule (LT) unevenly: adds the new value to the previous total on some passes but restarts from the initial value (or forgets to add) on others. (here mixing in: "a variable declared in the loop body lives across all iterations")
- **Edge `loop_scope` &rarr; `LoopBodyScopeImpliesLoopLifetime`, exact edge logic:** A variable declared inside the loop body keeps its value from one pass to the next. **Twin logic:** A variable declared inside the body is created anew on every pass and does not keep the previous pass's value. (role: primary)
- **Edge `simulation_loop` &rarr; `LoopBodyScopeImpliesLoopLifetime`, exact edge logic:** Declaring page inside the simulation loop still lets the surfer continue from the previous page. **Twin logic:** If page is declared inside the loop body it is recreated each pass, so it must be declared before the loop to carry the walk forward. (role: context)
- **Edge `variable` &rarr; `LoopBodyScopeImpliesLoopLifetime`, exact edge logic:** a variable declared in the loop body lives across all iterations **Twin logic:** A variable declared inside the body is created anew on every pass and does not keep the previous pass's value. (role: context)

### StateChangeIgnoredAcrossPasses

- **Edge:** `accumulator_pattern` &rarr; `StateChangeIgnoredAcrossPasses` (misconception)
- **Exact edge logic (the wrong rule):** Values changed by one pass of a loop (other than the loop variable) do not affect later passes.
- **Twin logic (the right rule):** Each pass starts from the state left by the previous pass, so a change in one pass carries into the next ones.
- **Wrong belief (on the node):** Values changed by one pass of a loop (other than the loop variable) do not affect later passes.
- **Correct rule (on the node):** Each pass starts from the state left by the previous pass, so a change in one pass carries into the next ones.
- **Provenance:** published
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [4] misconception, exact rule:** wrong rule: Values changed by one pass of a loop (other than the loop variable) do not affect later passes. Right rule: Each pass starts from the state left by the previous pass, so a change in one pass carries into the next ones.
- **Edge `loop_body` &rarr; `StateChangeIgnoredAcrossPasses`, exact edge logic:** Values changed by one pass of a loop (other than the loop variable) do not affect later passes. **Twin logic:** Each pass starts from the state left by the previous pass, so a change in one pass carries into the next ones. (role: primary)
- **Edge `program_state` &rarr; `StateChangeIgnoredAcrossPasses`, exact edge logic:** Values changed by one pass of a loop (other than the loop variable) do not affect later passes. **Twin logic:** Each pass starts from the state left by the previous pass, so a change in one pass carries into the next ones. (role: context)

### VariableRolesInferred

- **Edge:** `accumulator_pattern` &rarr; `VariableRolesInferred` (misconception)
- **Exact edge logic (the wrong rule):** The computer recognises that one variable plays two roles, e.g. input value and running total, and keeps the values apart; it knows which variable is the counter and which the sum.
- **Twin logic (the right rule):** A variable holds one value at a time; each role (input, counter, running total) needs its own variable and explicit update.
- **Wrong belief (on the node):** The computer recognises that one variable plays two roles, e.g. input value and running total, and keeps the values apart; it knows which variable is the counter and which the sum.
- **Correct rule (on the node):** A variable holds one value at a time; each role (input, counter, running total) needs its own variable and explicit update.
- **Provenance:** published
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [3] misconception, exact rule:** wrong rule: The computer recognises that one variable plays two roles, e.g. input value and running total, and keeps the values apart; it knows which variable is the counter and which the sum. Right rule: A variable holds one value at a time; each role (input, counter, running total) needs its own variable and explicit update.
- **Edge `counter_pattern` &rarr; `VariableRolesInferred`, exact edge logic:** The computer recognises that one variable plays two roles, e.g. input value and running total, and keeps the values apart; it knows which variable is the counter and which the sum. **Twin logic:** A variable holds one value at a time; each role (input, counter, running total) needs its own variable and explicit update. (role: context)
- **Edge `variable` &rarr; `VariableRolesInferred`, exact edge logic:** The computer recognises that one variable plays two roles, e.g. input value and running total, and keeps the values apart; it knows which variable is the counter and which the sum. **Twin logic:** A variable holds one value at a time; each role (input, counter, running total) needs its own variable and explicit update. (role: primary)

## Errors (1)

An error edge states the rule that gets broken in a program, and the right rule.

### AccumulatorDeclaredInLoop

- **Edge:** `accumulator_pattern` &rarr; `AccumulatorDeclaredInLoop` (error)
- **Exact edge logic (the wrong rule):** Declaring sum inside the loop body keeps a running total across passes.
- **Twin logic (the right rule):** The accumulator must be declared and initialised before the loop.
- **Wrong belief (on the node):** Declaring sum inside the loop body keeps a running total across passes.
- **Correct rule (on the node):** The accumulator must be declared and initialised before the loop.
- **Provenance:** textbook
- **Role of this concept:** context
- **Edge `counter_pattern` &rarr; `AccumulatorDeclaredInLoop`, exact edge logic:** Declaring sum inside the loop body keeps a running total across passes. **Twin logic:** The accumulator must be declared and initialised before the loop. (role: context)
- **Edge `logical_error` &rarr; `AccumulatorDeclaredInLoop`, exact edge logic:** Declaring sum inside the loop body keeps a running total across passes. **Twin logic:** The accumulator must be declared and initialised before the loop. (role: context)
- **Edge `loop_scope` &rarr; `AccumulatorDeclaredInLoop`, exact edge logic:** Declaring sum inside the loop body keeps a running total across passes. **Twin logic:** The accumulator must be declared and initialised before the loop. (role: primary)

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for accumulator pattern: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to accumulator pattern agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

- **Edge:** `accumulator_pattern` &rarr; `accumulator_pattern@L0` (has_level)
- **Exact edge logic:** accumulator pattern -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (5 ways).

Ways (5), each with its exact rule:

- **[0] everyday\_reading** (rule type E, folk-meaning rule): Folk meaning: 'the sum' is a single mathematical quantity that simply exists, and a person adding numbers keeps the running total in mind automatically. In Java the total is a variable that must be declared and initialized before the loop and explicitly updated on every pass (sum += x).
- **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `LoopBodyScopeImpliesLoopLifetime`: wrong rule: a variable declared in the loop body lives across all iterations. Right rule: A variable declared inside the body is in scope only to the end of the body, so each pass declares and initializes it afresh and it does not keep the previous pass's value.
- **[2] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `LoopBodyScopeImpliesLoopLifetime`: Applies the update rule (LT) unevenly: adds the new value to the previous total on some passes but restarts from the initial value (or forgets to add) on others. (here mixing in: "a variable declared in the loop body lives across all iterations")
- **[3] misconception** (rule type M, wrong rule / right rule) &rarr; `VariableRolesInferred`: wrong rule: The computer recognises that one variable plays two roles, e.g. input value and running total, and keeps the values apart; it knows which variable is the counter and which the sum. Right rule: A variable holds one value at a time; each role (input, counter, running total) needs its own variable and explicit update.
- **[4] misconception** (rule type M, wrong rule / right rule) &rarr; `StateChangeIgnoredAcrossPasses`: wrong rule: Values changed by one pass of a loop (other than the loop variable) do not affect later passes. Right rule: Each pass starts from the state left by the previous pass, so a change in one pass carries into the next ones.

### L1: Unistructural / atom x text surface

L1 for accumulator pattern: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

- **Edge:** `accumulator_pattern` &rarr; `accumulator_pattern@L1` (has_level)
- **Exact edge logic:** accumulator pattern -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

Ways (2), each with its exact rule:

- **[0] names\_the\_element** (rule type N, identity rule): An accumulator is a variable used to accumulate results during a traversal, e.g. the running total of a sum.
- **[1] states\_the\_rule** (rule type S, declarative rule): Initialize the accumulator before the loop (0 for a sum, 1 for a product), update it once per pass in the body (total += array[i]), and use it after the loop.

### L2: Multistructural / block x execution / preoperational

L2 for accumulator pattern: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

- **Edge:** `accumulator_pattern` &rarr; `accumulator_pattern@L2` (has_level)
- **Exact edge logic:** accumulator pattern -&gt; L2 (Multistructural): the answer applies the rules of accumulator pattern to every part of the code, in order (3 ways).

Ways (3), each with its exact rule:

- **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): Before the loop: total = initial value. Each pass: read total, combine with the current item, store back. After the loop: total holds the combination of all items.
- **[1] output\_prediction** (rule type OP, evaluation / result rule): After the loop the accumulator holds the reduce result: sum of 1..N is N(N+1)/2; Harmonic(2) = 1.5; the product loop gives N!.
- **[2] one\_step\_execution** (rule type OS, state-transition rule): One pass changes only the accumulator (and the loop variable): sum += x[i] turns sum = 1 into 5 when x[i] = 4.

### L3: Relational / relations x function (concrete operational begins)

L3 for accumulator pattern: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

- **Edge:** `accumulator_pattern` &rarr; `accumulator_pattern@L3` (has_level)
- **Exact edge logic:** accumulator pattern -&gt; L3 (Relational): the answer relates the parts (5 ways).

Ways (5), each with its exact rule:

- **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): The update sum += x sits inside the body so it runs once per pass, while the declaration and initialization stay before the loop.
- **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): A counter is an accumulator that adds 1 on each pass that matches (count++), whereas an accumulator adds the current value itself (sum += x).
- **[2] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): In a sentinel loop the sum and the count of the values read are both accumulators, updated only for values that are not the sentinel.
- **[3] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Both make one pass over the values with one variable kept across passes. An accumulator (gatherer role) combines every value into it (sum += a[i]), so it starts at the identity 0.0; a running extreme (most-wanted holder) replaces it only when a better value is found (if (a[i] &gt; max) max = a[i]), so it starts at Double.NEGATIVE\_INFINITY or the first value.
- **[4] purpose\_of\_the\_whole** (rule type P, plan / role rule): Role: gatherer - a data item accumulating the effect of individual values (running total, product, concatenated string).

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for accumulator pattern: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

- **Edge:** `accumulator_pattern` &rarr; `accumulator_pattern@L4` (has_level)
- **Exact edge logic:** accumulator pattern -&gt; L4 (Extended abstract): the answer reasons beyond the given code (5 ways).

Ways (5), each with its exact rule:

- **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `LoopBodyScopeImpliesLoopLifetime`: Changing the initial value shifts the result by that amount (sum starts at 1 gives sum + 1); a product starting at 0 stays 0; reordering the items does not change an integer sum (addition is commutative) but may change a floating-point sum slightly.
- **[1] diagnose\_an\_error** (rule type D, error rule): rule broken: A variable declared in the body is in scope only to the end of the body and is re-declared and re-initialized on every pass. Kind: silent logic error. Trigger class: for (...) { int sum = 0; sum += a[i]; }: sum restarts at 0 each pass, so only the last term survives; printing sum after the loop is a compile-time error (cannot find symbol) because sum is out of scope.
- **[2] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Use an accumulator whenever many values must be reduced to one (sum, product, average, string); for a maximum or minimum use a most-wanted holder updated by an if instead.
- **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: The accumulator must be initialized before the loop. Kind: compile-time. Trigger class: Declaring int sum; and then sum += x in the loop: 'variable sum might not have been initialized'.
- **[4] diagnose\_an\_error** (rule type D, error rule): rule broken: A sum must start at 0 and a product at 1. Kind: silent logic error. Trigger class: product initialized to 0 (result always 0) or sum initialized to the first element and then adding it again (first element counted twice).

## Same topic

`accumulator_pattern` belongs to the topic **Applications (finite sums, Newton, conversion, gambler's ruin, factoring)** (`topic1.3.f`). The topic also contains: `convergence_test`, `counter_pattern`, `debugging`, `fencepost_loop`, `flag_search_loop`, `loop_performance`, `monte_carlo_simulation`, `number_conversion`, `testing`.

## Rules of the concept (19)

- **Book** (TJ-2e, p. 114 (pdf 136)): "A variable used this way is sometimes called an accumulator, because it "accumulates" the running total."
- **Book** (SW-1.3, ): "It uses two variables-one as an index that controls a loop, and the other to accumulate a computational result."
- **E** (folk-meaning rule): Folk meaning: 'the sum' is a single mathematical quantity that simply exists, and a person adding numbers keeps the running total in mind automatically. In Java the total is a variable that must be declared and initialized before the loop and explicitly updated on every pass (sum += x).
- **M** (wrong rule / right rule): LoopBodyScopeImpliesLoopLifetime: wrong: a variable declared in the loop body lives across all iterations \| right: A variable declared inside the body is in scope only to the end of the body, so each pass declares and initializes it afresh and it does not keep the previous pass's value.
- **M** (wrong rule / right rule): VariableRolesInferred: wrong: The computer recognises that one variable plays two roles, e.g. input value and running total, and keeps the values apart; it knows which variable is the counter and which the sum. \| right: A variable holds one value at a time; each role (input, counter, running total) needs its own variable and explicit update.
- **M** (wrong rule / right rule): StateChangeIgnoredAcrossPasses: wrong: Values changed by one pass of a loop (other than the loop variable) do not affect later passes. \| right: Each pass starts from the state left by the previous pass, so a change in one pass carries into the next ones.
- **T** (uneven-application rule): Applies the update rule (LT) unevenly: adds the new value to the previous total on some passes but restarts from the initial value (or forgets to add) on others.
- **N** (identity rule): An accumulator is a variable used to accumulate results during a traversal, e.g. the running total of a sum.
- **S** (declarative rule): Initialize the accumulator before the loop (0 for a sum, 1 for a product), update it once per pass in the body (total += array[i]), and use it after the loop.
- **LT** (operational sequencing rule): Before the loop: total = initial value. Each pass: read total, combine with the current item, store back. After the loop: total holds the combination of all items.
- **OP** (evaluation / result rule): After the loop the accumulator holds the reduce result: sum of 1..N is N(N+1)/2; Harmonic(2) = 1.5; the product loop gives N!.
- **OS** (state-transition rule): One pass changes only the accumulator (and the loop variable): sum += x[i] turns sum = 1 into 5 when x[i] = 4.
- **R** (composition rule (with a neighbour)): with loop\_body: The update sum += x sits inside the body so it runs once per pass, while the declaration and initialization stay before the loop.
- **R** (composition rule (with a neighbour)): with counter\_pattern: A counter is an accumulator that adds 1 on each pass that matches (count++), whereas an accumulator adds the current value itself (sum += x).
- **R** (composition rule (with a neighbour)): with sentinel\_loop: In a sentinel loop the sum and the count of the values read are both accumulators, updated only for values that are not the sentinel.
- **P** (plan / role rule): Role: gatherer - a data item accumulating the effect of individual values (running total, product, concatenated string).
- **C** (conservation rule): Changing the initial value shifts the result by that amount (sum starts at 1 gives sum + 1); a product starting at 0 stays 0; reordering the items does not change an integer sum (addition is commutative) but may change a floating-point sum slightly.
- **D** (error rule): rule broken: A variable declared in the body is in scope only to the end of the body and is re-declared and re-initialized on every pass. (silent logic error)
- **D** (error rule): rule broken: The accumulator must be initialized before the loop. (compile-time)
- **D** (error rule): rule broken: A sum must start at 0 and a product at 1. (silent logic error)
- **X** (applicability rule): Use an accumulator whenever many values must be reduced to one (sum, product, average, string); for a maximum or minimum use a most-wanted holder updated by an if instead.

## How it is found in code and answers (reader block)

- **Aliases:** accumulator, running sum, running total
- **Code patterns:** `\b\w+(?:\s*\[[^\]]*\])?\s*(?:\+=|\*=)(?!\s*1\s*;)\s*[^;]+;`, `\b(\w+)\s*=\s*\1\s*[+*](?![+*=])(?!\s*1\s*;)\s*[^;]+;`
- **Operator symbols:** none
- **Java types:** none

## The whole prerequisite chain

- **Everything it builds on (28):** `arithmetic_operators`, `assignment`, `boolean`, `boolean_expression`, `class_declaration`, `command_line_args`, `comparison_operators`, `compound_assignment`, `data_type`, `declaration`, `do_while_loop`, `explicit_cast`, `expression`, `for_loop`, `identifier`, `integer_division`, `literal`, `logical_operators`, `loop_body`, `loop_control`, `loop_variable`, `main_method`, `parsing`, `primitive_type`, `program_text`, `type_conversion`, `variable`, `while_loop`
- **Everything that builds on it (1):** `sentinel_loop`

## Every edge in this view and its exact edge logic (34)

All the edges drawn in the picture, in the order: prerequisite, parallel, misconception, error, has_level, contains.

**1. `accumulator_pattern` &rarr; `sentinel_loop`** (prerequisite)

- **Exact edge logic:** Sum and count are accumulators.
- **Grounding:** questionable
- **Composition rule (R) of `accumulator_pattern` with `sentinel_loop`:** In a sentinel loop the sum and the count of the values read are both accumulators, updated only for values that are not the sentinel.
- **Composition rule (R) of `sentinel_loop` with `accumulator_pattern`:** sum (a gatherer) and count must change only for values that are not the sentinel and pass the filter. The average is computed once, after the loop.

**2. `compound_assignment` &rarr; `accumulator_pattern`** (prerequisite)

- **Exact edge logic:** sum += x is the usual way a running total is updated on each pass.
- **Grounding:** book\_passage

**3. `loop_body` &rarr; `accumulator_pattern`** (prerequisite)

- **Exact edge logic:** The accumulator update sum += x sits inside the body, so it runs once on every pass.
- **Grounding:** book\_passage
- **Composition rule (R) of `loop_body` with `accumulator_pattern`:** The accumulator update (sum += x) is placed inside the body so it runs once per pass, while the accumulator is declared and initialized before the loop.
- **Composition rule (R) of `accumulator_pattern` with `loop_body`:** The update sum += x sits inside the body so it runs once per pass, while the declaration and initialization stay before the loop.

**4. `accumulator_pattern` &harr; `counter_pattern`** (parallel)

- **Exact edge logic:** An accumulator adds the current value itself on each pass (sum += x); a counter adds 1 on each pass that matches (count++).
- **Grounding:** order\_only
- **Composition rule (R) of `accumulator_pattern` with `counter_pattern`:** A counter is an accumulator that adds 1 on each pass that matches (count++), whereas an accumulator adds the current value itself (sum += x).
- **Composition rule (R) of `counter_pattern` with `accumulator_pattern`:** Same skeleton (initialise before, update inside, read after); the accumulator adds the current value (\`sum += x\`), the counter adds the constant 1 on matching passes (\`count++\`). The two are often combined to compute an average \`sum / count\`, which needs a guard against \`count == 0\`.

**5. `running_extreme` &harr; `accumulator_pattern`** (parallel)

- **Exact edge logic:** Both make one pass over the values with one variable kept across passes. An accumulator (gatherer role) combines every value into it (sum += a[i]), so it starts at the identity 0.0; a running extreme (most-wanted holder) replaces it only when a better value is found (if (a[i] &gt; max) max = a[i]), so it starts at Double.NEGATIVE\_INFINITY or the first value.
- **Grounding:** book\_passage

**6. `accumulator_pattern` &rarr; `LoopBodyScopeImpliesLoopLifetime`** (misconception)

- **Exact edge logic (the wrong rule):** a variable declared in the loop body lives across all iterations
- **Twin logic (the right rule):** A variable declared inside the body is created anew on every pass and does not keep the previous pass's value.
- **Role:** context

**7. `accumulator_pattern` &rarr; `StateChangeIgnoredAcrossPasses`** (misconception)

- **Exact edge logic (the wrong rule):** Values changed by one pass of a loop (other than the loop variable) do not affect later passes.
- **Twin logic (the right rule):** Each pass starts from the state left by the previous pass, so a change in one pass carries into the next ones.
- **Role:** context

**8. `accumulator_pattern` &rarr; `VariableRolesInferred`** (misconception)

- **Exact edge logic (the wrong rule):** The computer recognises that one variable plays two roles, e.g. input value and running total, and keeps the values apart; it knows which variable is the counter and which the sum.
- **Twin logic (the right rule):** A variable holds one value at a time; each role (input, counter, running total) needs its own variable and explicit update.
- **Role:** context

**9. `counter_pattern` &rarr; `VariableRolesInferred`** (misconception)

- **Exact edge logic (the wrong rule):** The computer recognises that one variable plays two roles, e.g. input value and running total, and keeps the values apart; it knows which variable is the counter and which the sum.
- **Twin logic (the right rule):** A variable holds one value at a time; each role (input, counter, running total) needs its own variable and explicit update.
- **Role:** context

**10. `loop_body` &rarr; `StateChangeIgnoredAcrossPasses`** (misconception)

- **Exact edge logic (the wrong rule):** Values changed by one pass of a loop (other than the loop variable) do not affect later passes.
- **Twin logic (the right rule):** Each pass starts from the state left by the previous pass, so a change in one pass carries into the next ones.
- **Role:** primary

**11. `loop_scope` &rarr; `LoopBodyScopeImpliesLoopLifetime`** (misconception)

- **Exact edge logic (the wrong rule):** A variable declared inside the loop body keeps its value from one pass to the next.
- **Twin logic (the right rule):** A variable declared inside the body is created anew on every pass and does not keep the previous pass's value.
- **Role:** primary

**12. `program_state` &rarr; `StateChangeIgnoredAcrossPasses`** (misconception)

- **Exact edge logic (the wrong rule):** Values changed by one pass of a loop (other than the loop variable) do not affect later passes.
- **Twin logic (the right rule):** Each pass starts from the state left by the previous pass, so a change in one pass carries into the next ones.
- **Role:** context

**13. `simulation_loop` &rarr; `LoopBodyScopeImpliesLoopLifetime`** (misconception)

- **Exact edge logic (the wrong rule):** Declaring page inside the simulation loop still lets the surfer continue from the previous page.
- **Twin logic (the right rule):** If page is declared inside the loop body it is recreated each pass, so it must be declared before the loop to carry the walk forward.
- **Role:** context

**14. `variable` &rarr; `LoopBodyScopeImpliesLoopLifetime`** (misconception)

- **Exact edge logic (the wrong rule):** a variable declared in the loop body lives across all iterations
- **Twin logic (the right rule):** A variable declared inside the body is created anew on every pass and does not keep the previous pass's value.
- **Role:** context

**15. `variable` &rarr; `VariableRolesInferred`** (misconception)

- **Exact edge logic (the wrong rule):** The computer recognises that one variable plays two roles, e.g. input value and running total, and keeps the values apart; it knows which variable is the counter and which the sum.
- **Twin logic (the right rule):** A variable holds one value at a time; each role (input, counter, running total) needs its own variable and explicit update.
- **Role:** primary

**16. `accumulator_pattern` &rarr; `AccumulatorDeclaredInLoop`** (error)

- **Exact edge logic (the wrong rule):** Declaring sum inside the loop body keeps a running total across passes.
- **Twin logic (the right rule):** The accumulator must be declared and initialised before the loop.
- **Role:** context

**17. `counter_pattern` &rarr; `AccumulatorDeclaredInLoop`** (error)

- **Exact edge logic (the wrong rule):** Declaring sum inside the loop body keeps a running total across passes.
- **Twin logic (the right rule):** The accumulator must be declared and initialised before the loop.
- **Role:** context

**18. `logical_error` &rarr; `AccumulatorDeclaredInLoop`** (error)

- **Exact edge logic (the wrong rule):** Declaring sum inside the loop body keeps a running total across passes.
- **Twin logic (the right rule):** The accumulator must be declared and initialised before the loop.
- **Role:** context

**19. `loop_scope` &rarr; `AccumulatorDeclaredInLoop`** (error)

- **Exact edge logic (the wrong rule):** Declaring sum inside the loop body keeps a running total across passes.
- **Twin logic (the right rule):** The accumulator must be declared and initialised before the loop.
- **Role:** primary

**20. `accumulator_pattern` &rarr; `accumulator_pattern@L0`** (has_level)

- **Exact edge logic:** accumulator pattern -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (5 ways).
  - **[0] everyday\_reading** (rule type E, folk-meaning rule): Folk meaning: 'the sum' is a single mathematical quantity that simply exists, and a person adding numbers keeps the running total in mind automatically. In Java the total is a variable that must be declared and initialized before the loop and explicitly updated on every pass (sum += x).
  - **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `LoopBodyScopeImpliesLoopLifetime`: wrong rule: a variable declared in the loop body lives across all iterations. Right rule: A variable declared inside the body is in scope only to the end of the body, so each pass declares and initializes it afresh and it does not keep the previous pass's value.
  - **[2] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `LoopBodyScopeImpliesLoopLifetime`: Applies the update rule (LT) unevenly: adds the new value to the previous total on some passes but restarts from the initial value (or forgets to add) on others. (here mixing in: "a variable declared in the loop body lives across all iterations")
  - **[3] misconception** (rule type M, wrong rule / right rule) &rarr; `VariableRolesInferred`: wrong rule: The computer recognises that one variable plays two roles, e.g. input value and running total, and keeps the values apart; it knows which variable is the counter and which the sum. Right rule: A variable holds one value at a time; each role (input, counter, running total) needs its own variable and explicit update.
  - **[4] misconception** (rule type M, wrong rule / right rule) &rarr; `StateChangeIgnoredAcrossPasses`: wrong rule: Values changed by one pass of a loop (other than the loop variable) do not affect later passes. Right rule: Each pass starts from the state left by the previous pass, so a change in one pass carries into the next ones.

**21. `accumulator_pattern` &rarr; `accumulator_pattern@L1`** (has_level)

- **Exact edge logic:** accumulator pattern -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).
  - **[0] names\_the\_element** (rule type N, identity rule): An accumulator is a variable used to accumulate results during a traversal, e.g. the running total of a sum.
  - **[1] states\_the\_rule** (rule type S, declarative rule): Initialize the accumulator before the loop (0 for a sum, 1 for a product), update it once per pass in the body (total += array[i]), and use it after the loop.

**22. `accumulator_pattern` &rarr; `accumulator_pattern@L2`** (has_level)

- **Exact edge logic:** accumulator pattern -&gt; L2 (Multistructural): the answer applies the rules of accumulator pattern to every part of the code, in order (3 ways).
  - **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): Before the loop: total = initial value. Each pass: read total, combine with the current item, store back. After the loop: total holds the combination of all items.
  - **[1] output\_prediction** (rule type OP, evaluation / result rule): After the loop the accumulator holds the reduce result: sum of 1..N is N(N+1)/2; Harmonic(2) = 1.5; the product loop gives N!.
  - **[2] one\_step\_execution** (rule type OS, state-transition rule): One pass changes only the accumulator (and the loop variable): sum += x[i] turns sum = 1 into 5 when x[i] = 4.

**23. `accumulator_pattern` &rarr; `accumulator_pattern@L3`** (has_level)

- **Exact edge logic:** accumulator pattern -&gt; L3 (Relational): the answer relates the parts (5 ways).
  - **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): The update sum += x sits inside the body so it runs once per pass, while the declaration and initialization stay before the loop.
  - **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): A counter is an accumulator that adds 1 on each pass that matches (count++), whereas an accumulator adds the current value itself (sum += x).
  - **[2] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): In a sentinel loop the sum and the count of the values read are both accumulators, updated only for values that are not the sentinel.
  - **[3] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Both make one pass over the values with one variable kept across passes. An accumulator (gatherer role) combines every value into it (sum += a[i]), so it starts at the identity 0.0; a running extreme (most-wanted holder) replaces it only when a better value is found (if (a[i] &gt; max) max = a[i]), so it starts at Double.NEGATIVE\_INFINITY or the first value.
  - **[4] purpose\_of\_the\_whole** (rule type P, plan / role rule): Role: gatherer - a data item accumulating the effect of individual values (running total, product, concatenated string).

**24. `accumulator_pattern` &rarr; `accumulator_pattern@L4`** (has_level)

- **Exact edge logic:** accumulator pattern -&gt; L4 (Extended abstract): the answer reasons beyond the given code (5 ways).
  - **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `LoopBodyScopeImpliesLoopLifetime`: Changing the initial value shifts the result by that amount (sum starts at 1 gives sum + 1); a product starting at 0 stays 0; reordering the items does not change an integer sum (addition is commutative) but may change a floating-point sum slightly.
  - **[1] diagnose\_an\_error** (rule type D, error rule): rule broken: A variable declared in the body is in scope only to the end of the body and is re-declared and re-initialized on every pass. Kind: silent logic error. Trigger class: for (...) { int sum = 0; sum += a[i]; }: sum restarts at 0 each pass, so only the last term survives; printing sum after the loop is a compile-time error (cannot find symbol) because sum is out of scope.
  - **[2] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Use an accumulator whenever many values must be reduced to one (sum, product, average, string); for a maximum or minimum use a most-wanted holder updated by an if instead.
  - **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: The accumulator must be initialized before the loop. Kind: compile-time. Trigger class: Declaring int sum; and then sum += x in the loop: 'variable sum might not have been initialized'.
  - **[4] diagnose\_an\_error** (rule type D, error rule): rule broken: A sum must start at 0 and a product at 1. Kind: silent logic error. Trigger class: product initialized to 0 (result always 0) or sum initialized to the first element and then adding it again (first element counted twice).

**25. `topic1.3.f` &rarr; `accumulator_pattern`** (contains)

- topic `topic1.3.f` contains `accumulator_pattern`

**26. `topic1.3.f` &rarr; `convergence_test`** (contains)

- topic `topic1.3.f` contains `convergence_test`

**27. `topic1.3.f` &rarr; `counter_pattern`** (contains)

- topic `topic1.3.f` contains `counter_pattern`

**28. `topic1.3.f` &rarr; `debugging`** (contains)

- topic `topic1.3.f` contains `debugging`

**29. `topic1.3.f` &rarr; `fencepost_loop`** (contains)

- topic `topic1.3.f` contains `fencepost_loop`

**30. `topic1.3.f` &rarr; `flag_search_loop`** (contains)

- topic `topic1.3.f` contains `flag_search_loop`

**31. `topic1.3.f` &rarr; `loop_performance`** (contains)

- topic `topic1.3.f` contains `loop_performance`

**32. `topic1.3.f` &rarr; `monte_carlo_simulation`** (contains)

- topic `topic1.3.f` contains `monte_carlo_simulation`

**33. `topic1.3.f` &rarr; `number_conversion`** (contains)

- topic `topic1.3.f` contains `number_conversion`

**34. `topic1.3.f` &rarr; `testing`** (contains)

- topic `topic1.3.f` contains `testing`
