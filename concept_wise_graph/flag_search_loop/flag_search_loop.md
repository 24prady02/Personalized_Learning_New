# flag_search_loop (`flag_search_loop`)

a boolean flag that a loop sets once and never resets

Section 1.3 Conditionals and Loops, topic 1.3.f Applications (finite sums, Newton, conversion, gambler's ruin, factoring).

![The knowledge graph around flag_search_loop](flag_search_loop.png)

## At a glance

- **Needs first:** `for_loop`
- **Leads to:** nothing
- **Learned alongside:** `break_statement`
- **Misconceptions:** `FlagResetInLoop`, `ReturnDoesNotExitLoop`
- **Errors:** `LoopIgnoresCodeBefore`
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 24 edges around this concept, each explained in the graph's own words.

## What it needs first (1)

A prerequisite edge means the other concept has to be understood before `flag_search_loop`.

### `for_loop` comes before `flag_search_loop`

*a while with init/condition/update packaged together*

A flag search loop sets a boolean flag inside a loop when a pass finds the condition, and leaves it set afterwards.

- **Grounding:** questionable
- **How `flag_search_loop` combines with `for_loop`:** The flag must be declared before the for loop to be visible after it. The for loop's test can include \`!found\` to stop at the first find; without that, the loop runs all passes, and the flag still works because it is one-way.
- **How `for_loop` combines with `flag_search_loop`:** A flag search loop is a for loop that sets a boolean flag when some pass finds the target and leaves it set afterwards; the flag must be declared before the loop.

## What it leads to (0)

These concepts need `flag_search_loop` first.

No concept has this one as a prerequisite.

## Learned alongside (1)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

### `flag_search_loop` alongside `break_statement`

*break -- immediately exits the innermost loop or switch*

Two ways to stop a search when the item is found: break leaves the loop at once, while a boolean flag is set and tested in the loop condition so the loop ends at its next test. After either, the code must tell the found case from the loop finishing normally.

- **Grounding:** book passage

## Misconceptions (2)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### FlagResetInLoop

- **Wrong rule:** A search flag should be set back to true whenever a test fails.
- **Right rule:** Once the flag records a find, the loop must not reset it.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: A search flag should be set back (to false/true) whenever a test fails. Right rule: A search flag is a one-way flag: once a pass records a find, no later pass may reset it, so the loop body contains only \`if (match) found = true;\` with no else.
- **Shows at level L0 as:** inconsistent trace: Applies the LT rule unevenly: on a trace, the flag is updated on non-matching passes as if there were an else, or the trace forgets that the flag carries over from the previous pass. The traced final flag then reflects only the last element. (here mixing in: "A search flag should be set back to true whenever a test fails")

### ReturnDoesNotExitLoop

- **Wrong rule:** A return inside a loop does not end the loop; it sets a value each pass (the last one is returned) or returns several values.
- **Right rule:** When return executes, the method ends at once, so the loop stops on that pass.
- **Role of this concept:** context
- **Also an edge from `control_flow`:** A return inside a loop does not end the loop; it sets a value each pass (the last one is returned) or returns several values.
- **Also an edge from `for_loop`:** A return inside a loop does not end the loop; it sets a value each pass (the last one is returned) or returns several values.

## Errors (1)

An error edge states the rule that gets broken in a program, and the right rule.

### LoopIgnoresCodeBefore

- **Wrong rule:** Initializes the flag before the loop so that the loop condition is already false, and the loop body never runs.
- **Right rule:** A while loop tests its condition before the first pass: if the values set before the loop make the condition false, the body never runs.
- **Role of this concept:** context
- **Also an edge from `logical_error`:** Initializes the flag before the loop so that the loop condition is already false, and the loop body never runs.
- **Also an edge from `while_loop`:** Initializes the flag before the loop so that the loop condition is already false, and the loop body never runs.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for flag search loop: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to flag search loop agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

flag search loop -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (3 ways).

- **everyday reading** (folk-meaning rule): Folk meaning: in English, 'found' or 'is OK' describes the current item, so a novice writes \`found = (a[i] == target);\` on every pass. In a search, the flag must record whether any pass so far matched: it is set once (\`if (a[i] == target) found = true;\`) and never reset.
- **misconception** (wrong rule / right rule; shows `FlagResetInLoop`): wrong rule: A search flag should be set back (to false/true) whenever a test fails. Right rule: A search flag is a one-way flag: once a pass records a find, no later pass may reset it, so the loop body contains only \`if (match) found = true;\` with no else.
- **inconsistent trace** (uneven-application rule; shows `FlagResetInLoop`): Applies the LT rule unevenly: on a trace, the flag is updated on non-matching passes as if there were an else, or the trace forgets that the flag carries over from the previous pass. The traced final flag then reflects only the last element. (here mixing in: "A search flag should be set back to true whenever a test fails")

### L1: Unistructural / atom x text surface

L1 for flag search loop: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

flag search loop -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

- **names the element** (identity rule): Loop plan: a boolean flag variable initialised before a loop and set by the loop when a condition is found, recording whether the condition held on any pass.
- **states the rule** (declarative rule): \`boolean found = false; for (int i = 0; i &lt; n; i++) if (a[i] == target) found = true;\` To stop early, add the flag to the test: \`while (i &lt; n &amp;&amp; !found)\`.

### L2: Multistructural / block x execution / preoperational

L2 for flag search loop: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

flag search loop -&gt; L2 (Multistructural): the answer applies the rules of flag search loop to every part of the code, in order (3 ways).

- **line by line trace** (operational sequencing rule): Order: initialise the flag once before the loop. On each pass, test the loop condition (which may include \`!found\`), then evaluate the guard, and only if it is true assign \`found = true\`. Read the flag after the loop.
- **output prediction** (evaluation / result rule): The result is a boolean: true if at least one pass satisfied the guard, false if none did (including zero passes). For {3, 5, 7} and target 5, found is true.
- **one step execution** (state-transition rule): A matching pass changes only the flag, from false to true (and it stays true). A non-matching pass changes nothing. \`found = true\` as a statement has the value true, which is discarded.

### L3: Relational / relations x function (concrete operational begins)

L3 for flag search loop: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

flag search loop -&gt; L3 (Relational): the answer relates the parts (3 ways).

- **relation to neighbour** (composition rule (with a neighbour)): The flag must be declared before the for loop to be visible after it. The for loop's test can include \`!found\` to stop at the first find; without that, the loop runs all passes, and the flag still works because it is one-way.
- **relation to neighbour** (composition rule (with a neighbour)): Two ways to stop a search when the item is found: break leaves the loop at once, while a boolean flag is set and tested in the loop condition so the loop ends at its next test. After either, the code must tell the found case from the loop finishing normally.
- **purpose of the whole** (plan / role rule): Plan: search / existence-check plan. The flag plays the Sajaniemi one-way flag role. It answers 'is there any element with property P?' or 'is the array sorted?'.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for flag search loop: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

flag search loop -&gt; L4 (Extended abstract): the answer reasons beyond the given code (5 ways).

- **predict a change** (conservation rule; shows `FlagResetInLoop`): Invariant: after k passes, found == (some element among the first k matched). Adding an else that resets the flag breaks the invariant, as does replacing the guard with \`found = (a[i] == target)\`. Adding \`!found\` to the loop test keeps the result and only saves passes. Initialising the flag to true breaks the result for inputs with no match.
- **transfer to a new program** (applicability rule): Use a flag when you need a yes/no answer after a loop, or a stopping condition that is set in the middle of a pass. In a method, \`return\` from inside the loop (or \`break\`) is often simpler. Use a counter when you need how many, not whether.
- **diagnose an error** (error rule): rule broken: A while loop tests its condition before the first pass: if the values set before the loop make the condition false, the body never runs. Kind: silent logic error. Trigger class: Initialising the flag so that the loop test is already false (e.g. \`boolean found = true; while (!found) {...}\`): the search never runs.
- **diagnose an error** (error rule): rule broken: A search flag is one-way: it must not be reassigned on every pass. Kind: silent logic error. Trigger class: \`found = (a[i] == target);\` or an else branch that sets \`found = false\`: the result reflects only the last element and fails when the match is not last.
- **diagnose an error** (error rule): rule broken: Using = instead of == on a boolean flag assigns instead of testing. Kind: silent logic error. Trigger class: \`if (found = false)\` compiles (boolean assignment) and is always false; write \`if (!found)\`.

## Same topic

`flag_search_loop` belongs to the topic **Applications (finite sums, Newton, conversion, gambler's ruin, factoring)** (`topic1.3.f`). The topic also contains: `accumulator_pattern`, `convergence_test`, `counter_pattern`, `debugging`, `fencepost_loop`, `loop_performance`, `monte_carlo_simulation`, `number_conversion`, `testing`.

## Rules of the concept (15)

- **folk-meaning rule:** Folk meaning: in English, 'found' or 'is OK' describes the current item, so a novice writes \`found = (a[i] == target);\` on every pass. In a search, the flag must record whether any pass so far matched: it is set once (\`if (a[i] == target) found = true;\`) and never reset.
- **wrong rule / right rule:** FlagResetInLoop: wrong: A search flag should be set back (to false/true) whenever a test fails. \| right: A search flag is a one-way flag: once a pass records a find, no later pass may reset it, so the loop body contains only \`if (match) found = true;\` with no else.
- **uneven-application rule:** Applies the LT rule unevenly: on a trace, the flag is updated on non-matching passes as if there were an else, or the trace forgets that the flag carries over from the previous pass. The traced final flag then reflects only the last element.
- **identity rule:** Loop plan: a boolean flag variable initialised before a loop and set by the loop when a condition is found, recording whether the condition held on any pass.
- **declarative rule:** \`boolean found = false; for (int i = 0; i &lt; n; i++) if (a[i] == target) found = true;\` To stop early, add the flag to the test: \`while (i &lt; n &amp;&amp; !found)\`.
- **operational sequencing rule:** Order: initialise the flag once before the loop. On each pass, test the loop condition (which may include \`!found\`), then evaluate the guard, and only if it is true assign \`found = true\`. Read the flag after the loop.
- **evaluation / result rule:** The result is a boolean: true if at least one pass satisfied the guard, false if none did (including zero passes). For {3, 5, 7} and target 5, found is true.
- **state-transition rule:** A matching pass changes only the flag, from false to true (and it stays true). A non-matching pass changes nothing. \`found = true\` as a statement has the value true, which is discarded.
- **composition rule (with a neighbour):** with for\_loop: The flag must be declared before the for loop to be visible after it. The for loop's test can include \`!found\` to stop at the first find; without that, the loop runs all passes, and the flag still works because it is one-way.
- **plan / role rule:** Plan: search / existence-check plan. The flag plays the Sajaniemi one-way flag role. It answers 'is there any element with property P?' or 'is the array sorted?'.
- **conservation rule:** Invariant: after k passes, found == (some element among the first k matched). Adding an else that resets the flag breaks the invariant, as does replacing the guard with \`found = (a[i] == target)\`. Adding \`!found\` to the loop test keeps the result and only saves passes. Initialising the flag to true breaks the result for inputs with no match.
- **error rule:** rule broken: A while loop tests its condition before the first pass: if the values set before the loop make the condition false, the body never runs. (silent logic error)
- **error rule:** rule broken: A search flag is one-way: it must not be reassigned on every pass. (silent logic error)
- **error rule:** rule broken: Using = instead of == on a boolean flag assigns instead of testing. (silent logic error)
- **applicability rule:** Use a flag when you need a yes/no answer after a loop, or a stopping condition that is set in the middle of a pass. In a method, \`return\` from inside the loop (or \`break\`) is often simpler. Use a counter when you need how many, not whether.

## The whole prerequisite chain

- **Everything it builds on (16):** `arithmetic_operators`, `boolean`, `boolean_expression`, `comparison_operators`, `data_type`, `do_while_loop`, `expression`, `for_loop`, `identifier`, `literal`, `logical_operators`, `loop_control`, `loop_variable`, `primitive_type`, `variable`, `while_loop`
- **Everything that builds on it (0):** nothing
