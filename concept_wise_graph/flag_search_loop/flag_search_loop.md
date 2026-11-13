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

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 24 edges around this concept. The edge logic, the wrong and right rules and the exact rules of the ways are copied word for word from the graph.

## To work on (2)

- misconceptions with no L0 way linked to them: ReturnDoesNotExitLoop
- no aliases: a student's words cannot name this concept

## What it needs first (1)

A prerequisite edge means the other concept has to be understood before `flag_search_loop`.

### `for_loop` comes before `flag_search_loop`

*a while with init/condition/update packaged together*

- **Edge:** `pre:for_loop->flag_search_loop`
- **Exact edge logic:** A flag search loop sets a boolean flag inside a loop when a pass finds the condition, and leaves it set afterwards.
- **Grounding:** questionable
- **Composition rule (R) of `flag_search_loop` with `for_loop`:** The flag must be declared before the for loop to be visible after it. The for loop's test can include \`!found\` to stop at the first find; without that, the loop runs all passes, and the flag still works because it is one-way.
- **Composition rule (R) of `for_loop` with `flag_search_loop`:** A flag search loop is a for loop that sets a boolean flag when some pass finds the target and leaves it set afterwards; the flag must be declared before the loop.

## What it leads to (0)

These concepts need `flag_search_loop` first.

No concept has this one as a prerequisite.

## Learned alongside (1)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

### `flag_search_loop` alongside `break_statement`

*break -- immediately exits the innermost loop or switch*

- **Edge:** `par:flag_search_loop~break_statement`
- **Exact edge logic:** Two ways to stop a search when the item is found: break leaves the loop at once, while a boolean flag is set and tested in the loop condition so the loop ends at its next test. After either, the code must tell the found case from the loop finishing normally.
- **Grounding:** book\_passage

## Misconceptions (2)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### FlagResetInLoop

- **Edge:** `flag_search_loop` &rarr; `FlagResetInLoop` (misconception)
- **Exact edge logic (the wrong rule):** A search flag should be set back to true whenever a test fails.
- **Twin logic (the right rule):** Once the flag records a find, the loop must not reset it.
- **Wrong belief (on the node):** A search flag should be set back to true whenever a test fails.
- **Correct rule (on the node):** Once the flag records a find, the loop must not reset it.
- **Provenance:** textbook
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [1] misconception, exact rule:** wrong rule: A search flag should be set back (to false/true) whenever a test fails. Right rule: A search flag is a one-way flag: once a pass records a find, no later pass may reset it, so the loop body contains only \`if (match) found = true;\` with no else.
- **L0 way [2] inconsistent\_trace, exact rule:** Applies the LT rule unevenly: on a trace, the flag is updated on non-matching passes as if there were an else, or the trace forgets that the flag carries over from the previous pass. The traced final flag then reflects only the last element. (here mixing in: "A search flag should be set back to true whenever a test fails")

### ReturnDoesNotExitLoop

- **Edge:** `flag_search_loop` &rarr; `ReturnDoesNotExitLoop` (misconception)
- **Exact edge logic (the wrong rule):** A return inside a loop does not end the loop; it sets a value each pass (the last one is returned) or returns several values.
- **Twin logic (the right rule):** When return executes, the method ends at once, so the loop stops on that pass.
- **Wrong belief (on the node):** A return inside a loop does not end the loop; it sets a value each pass (the last one is returned) or returns several values.
- **Correct rule (on the node):** When return executes, the method ends at once, so the loop stops on that pass.
- **Provenance:** published
- **Role of this concept:** context
- **L0 way linked to it:** no
- **Edge `control_flow` &rarr; `ReturnDoesNotExitLoop`, exact edge logic:** A return inside a loop does not end the loop; it sets a value each pass (the last one is returned) or returns several values. **Twin logic:** When return executes, the method ends at once, so the loop stops on that pass. (role: primary)
- **Edge `for_loop` &rarr; `ReturnDoesNotExitLoop`, exact edge logic:** A return inside a loop does not end the loop; it sets a value each pass (the last one is returned) or returns several values. **Twin logic:** When return executes, the method ends at once, so the loop stops on that pass. (role: context)

## Errors (1)

An error edge states the rule that gets broken in a program, and the right rule.

### LoopIgnoresCodeBefore

- **Edge:** `flag_search_loop` &rarr; `LoopIgnoresCodeBefore` (error)
- **Exact edge logic (the wrong rule):** Initializes the flag before the loop so that the loop condition is already false, and the loop body never runs.
- **Twin logic (the right rule):** A while loop tests its condition before the first pass: if the values set before the loop make the condition false, the body never runs.
- **Wrong belief (on the node):** Initializes the flag before the loop so that the loop condition is already false, and the loop body never runs.
- **Correct rule (on the node):** A while loop tests its condition before the first pass: if the values set before the loop make the condition false, the body never runs.
- **Provenance:** published
- **Role of this concept:** context
- **Edge `logical_error` &rarr; `LoopIgnoresCodeBefore`, exact edge logic:** Initializes the flag before the loop so that the loop condition is already false, and the loop body never runs. **Twin logic:** A while loop tests its condition before the first pass: if the values set before the loop make the condition false, the body never runs. (role: context)
- **Edge `while_loop` &rarr; `LoopIgnoresCodeBefore`, exact edge logic:** Initializes the flag before the loop so that the loop condition is already false, and the loop body never runs. **Twin logic:** A while loop tests its condition before the first pass: if the values set before the loop make the condition false, the body never runs. (role: primary)

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for flag search loop: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to flag search loop agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

- **Edge:** `flag_search_loop` &rarr; `flag_search_loop@L0` (has_level)
- **Exact edge logic:** flag search loop -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (3 ways).

Ways (3), each with its exact rule:

- **[0] everyday\_reading** (rule type E, folk-meaning rule): Folk meaning: in English, 'found' or 'is OK' describes the current item, so a novice writes \`found = (a[i] == target);\` on every pass. In a search, the flag must record whether any pass so far matched: it is set once (\`if (a[i] == target) found = true;\`) and never reset.
- **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `FlagResetInLoop`: wrong rule: A search flag should be set back (to false/true) whenever a test fails. Right rule: A search flag is a one-way flag: once a pass records a find, no later pass may reset it, so the loop body contains only \`if (match) found = true;\` with no else.
- **[2] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `FlagResetInLoop`: Applies the LT rule unevenly: on a trace, the flag is updated on non-matching passes as if there were an else, or the trace forgets that the flag carries over from the previous pass. The traced final flag then reflects only the last element. (here mixing in: "A search flag should be set back to true whenever a test fails")

### L1: Unistructural / atom x text surface

L1 for flag search loop: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

- **Edge:** `flag_search_loop` &rarr; `flag_search_loop@L1` (has_level)
- **Exact edge logic:** flag search loop -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

Ways (2), each with its exact rule:

- **[0] names\_the\_element** (rule type N, identity rule): Loop plan: a boolean flag variable initialised before a loop and set by the loop when a condition is found, recording whether the condition held on any pass.
- **[1] states\_the\_rule** (rule type S, declarative rule): \`boolean found = false; for (int i = 0; i &lt; n; i++) if (a[i] == target) found = true;\` To stop early, add the flag to the test: \`while (i &lt; n &amp;&amp; !found)\`.

### L2: Multistructural / block x execution / preoperational

L2 for flag search loop: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

- **Edge:** `flag_search_loop` &rarr; `flag_search_loop@L2` (has_level)
- **Exact edge logic:** flag search loop -&gt; L2 (Multistructural): the answer applies the rules of flag search loop to every part of the code, in order (3 ways).

Ways (3), each with its exact rule:

- **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): Order: initialise the flag once before the loop. On each pass, test the loop condition (which may include \`!found\`), then evaluate the guard, and only if it is true assign \`found = true\`. Read the flag after the loop.
- **[1] output\_prediction** (rule type OP, evaluation / result rule): The result is a boolean: true if at least one pass satisfied the guard, false if none did (including zero passes). For {3, 5, 7} and target 5, found is true.
- **[2] one\_step\_execution** (rule type OS, state-transition rule): A matching pass changes only the flag, from false to true (and it stays true). A non-matching pass changes nothing. \`found = true\` as a statement has the value true, which is discarded.

### L3: Relational / relations x function (concrete operational begins)

L3 for flag search loop: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

- **Edge:** `flag_search_loop` &rarr; `flag_search_loop@L3` (has_level)
- **Exact edge logic:** flag search loop -&gt; L3 (Relational): the answer relates the parts (3 ways).

Ways (3), each with its exact rule:

- **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): The flag must be declared before the for loop to be visible after it. The for loop's test can include \`!found\` to stop at the first find; without that, the loop runs all passes, and the flag still works because it is one-way.
- **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Two ways to stop a search when the item is found: break leaves the loop at once, while a boolean flag is set and tested in the loop condition so the loop ends at its next test. After either, the code must tell the found case from the loop finishing normally.
- **[2] purpose\_of\_the\_whole** (rule type P, plan / role rule): Plan: search / existence-check plan. The flag plays the Sajaniemi one-way flag role. It answers 'is there any element with property P?' or 'is the array sorted?'.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for flag search loop: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

- **Edge:** `flag_search_loop` &rarr; `flag_search_loop@L4` (has_level)
- **Exact edge logic:** flag search loop -&gt; L4 (Extended abstract): the answer reasons beyond the given code (5 ways).

Ways (5), each with its exact rule:

- **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `FlagResetInLoop`: Invariant: after k passes, found == (some element among the first k matched). Adding an else that resets the flag breaks the invariant, as does replacing the guard with \`found = (a[i] == target)\`. Adding \`!found\` to the loop test keeps the result and only saves passes. Initialising the flag to true breaks the result for inputs with no match.
- **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Use a flag when you need a yes/no answer after a loop, or a stopping condition that is set in the middle of a pass. In a method, \`return\` from inside the loop (or \`break\`) is often simpler. Use a counter when you need how many, not whether.
- **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: A while loop tests its condition before the first pass: if the values set before the loop make the condition false, the body never runs. Kind: silent logic error. Trigger class: Initialising the flag so that the loop test is already false (e.g. \`boolean found = true; while (!found) {...}\`): the search never runs.
- **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: A search flag is one-way: it must not be reassigned on every pass. Kind: silent logic error. Trigger class: \`found = (a[i] == target);\` or an else branch that sets \`found = false\`: the result reflects only the last element and fails when the match is not last.
- **[4] diagnose\_an\_error** (rule type D, error rule): rule broken: Using = instead of == on a boolean flag assigns instead of testing. Kind: silent logic error. Trigger class: \`if (found = false)\` compiles (boolean assignment) and is always false; write \`if (!found)\`.

## Same topic

`flag_search_loop` belongs to the topic **Applications (finite sums, Newton, conversion, gambler's ruin, factoring)** (`topic1.3.f`). The topic also contains: `accumulator_pattern`, `convergence_test`, `counter_pattern`, `debugging`, `fencepost_loop`, `loop_performance`, `monte_carlo_simulation`, `number_conversion`, `testing`.

## Rules of the concept (15)

- **Book** (TJ-2e, p. 84 (pdf 106)): "flag: A variable (usually boolean) that represents a condition or status."
- **Book** (RS-web, ): "if the code finds a factor of the number, prime will be set to false, but on the next pass through the loop, if the next number isn't a factor, prime will be reset to true again."
- **E** (folk-meaning rule): Folk meaning: in English, 'found' or 'is OK' describes the current item, so a novice writes \`found = (a[i] == target);\` on every pass. In a search, the flag must record whether any pass so far matched: it is set once (\`if (a[i] == target) found = true;\`) and never reset.
- **M** (wrong rule / right rule): FlagResetInLoop: wrong: A search flag should be set back (to false/true) whenever a test fails. \| right: A search flag is a one-way flag: once a pass records a find, no later pass may reset it, so the loop body contains only \`if (match) found = true;\` with no else.
- **T** (uneven-application rule): Applies the LT rule unevenly: on a trace, the flag is updated on non-matching passes as if there were an else, or the trace forgets that the flag carries over from the previous pass. The traced final flag then reflects only the last element.
- **N** (identity rule): Loop plan: a boolean flag variable initialised before a loop and set by the loop when a condition is found, recording whether the condition held on any pass.
- **S** (declarative rule): \`boolean found = false; for (int i = 0; i &lt; n; i++) if (a[i] == target) found = true;\` To stop early, add the flag to the test: \`while (i &lt; n &amp;&amp; !found)\`.
- **LT** (operational sequencing rule): Order: initialise the flag once before the loop. On each pass, test the loop condition (which may include \`!found\`), then evaluate the guard, and only if it is true assign \`found = true\`. Read the flag after the loop.
- **OP** (evaluation / result rule): The result is a boolean: true if at least one pass satisfied the guard, false if none did (including zero passes). For {3, 5, 7} and target 5, found is true.
- **OS** (state-transition rule): A matching pass changes only the flag, from false to true (and it stays true). A non-matching pass changes nothing. \`found = true\` as a statement has the value true, which is discarded.
- **R** (composition rule (with a neighbour)): with for\_loop: The flag must be declared before the for loop to be visible after it. The for loop's test can include \`!found\` to stop at the first find; without that, the loop runs all passes, and the flag still works because it is one-way.
- **P** (plan / role rule): Plan: search / existence-check plan. The flag plays the Sajaniemi one-way flag role. It answers 'is there any element with property P?' or 'is the array sorted?'.
- **C** (conservation rule): Invariant: after k passes, found == (some element among the first k matched). Adding an else that resets the flag breaks the invariant, as does replacing the guard with \`found = (a[i] == target)\`. Adding \`!found\` to the loop test keeps the result and only saves passes. Initialising the flag to true breaks the result for inputs with no match.
- **D** (error rule): rule broken: A while loop tests its condition before the first pass: if the values set before the loop make the condition false, the body never runs. (silent logic error)
- **D** (error rule): rule broken: A search flag is one-way: it must not be reassigned on every pass. (silent logic error)
- **D** (error rule): rule broken: Using = instead of == on a boolean flag assigns instead of testing. (silent logic error)
- **X** (applicability rule): Use a flag when you need a yes/no answer after a loop, or a stopping condition that is set in the middle of a pass. In a method, \`return\` from inside the loop (or \`break\`) is often simpler. Use a counter when you need how many, not whether.

## How it is found in code and answers (reader block)

- **Aliases:** none
- **Code patterns:** none
- **Operator symbols:** none
- **Java types:** none
- **Signal flag\_set\_in\_loop** (scope program, decisive): `\bboolean\s+(\w+)\s*=\s*(?:true|false)\s*;[\s\S]{0,4000}?\b(?:for|while)\b[\s\S]{0,4000}?\b\1\s*=\s*(?:true|false)`

## The whole prerequisite chain

- **Everything it builds on (16):** `arithmetic_operators`, `boolean`, `boolean_expression`, `comparison_operators`, `data_type`, `do_while_loop`, `expression`, `for_loop`, `identifier`, `literal`, `logical_operators`, `loop_control`, `loop_variable`, `primitive_type`, `variable`, `while_loop`
- **Everything that builds on it (0):** nothing

## Every edge in this view and its exact edge logic (24)

All the edges drawn in the picture, in the order: prerequisite, parallel, misconception, error, has_level, contains.

**1. `for_loop` &rarr; `flag_search_loop`** (prerequisite)

- **Exact edge logic:** A flag search loop sets a boolean flag inside a loop when a pass finds the condition, and leaves it set afterwards.
- **Grounding:** questionable
- **Composition rule (R) of `for_loop` with `flag_search_loop`:** A flag search loop is a for loop that sets a boolean flag when some pass finds the target and leaves it set afterwards; the flag must be declared before the loop.
- **Composition rule (R) of `flag_search_loop` with `for_loop`:** The flag must be declared before the for loop to be visible after it. The for loop's test can include \`!found\` to stop at the first find; without that, the loop runs all passes, and the flag still works because it is one-way.

**2. `flag_search_loop` &harr; `break_statement`** (parallel)

- **Exact edge logic:** Two ways to stop a search when the item is found: break leaves the loop at once, while a boolean flag is set and tested in the loop condition so the loop ends at its next test. After either, the code must tell the found case from the loop finishing normally.
- **Grounding:** book\_passage

**3. `flag_search_loop` &rarr; `FlagResetInLoop`** (misconception)

- **Exact edge logic (the wrong rule):** A search flag should be set back to true whenever a test fails.
- **Twin logic (the right rule):** Once the flag records a find, the loop must not reset it.
- **Role:** primary

**4. `flag_search_loop` &rarr; `ReturnDoesNotExitLoop`** (misconception)

- **Exact edge logic (the wrong rule):** A return inside a loop does not end the loop; it sets a value each pass (the last one is returned) or returns several values.
- **Twin logic (the right rule):** When return executes, the method ends at once, so the loop stops on that pass.
- **Role:** context

**5. `control_flow` &rarr; `ReturnDoesNotExitLoop`** (misconception)

- **Exact edge logic (the wrong rule):** A return inside a loop does not end the loop; it sets a value each pass (the last one is returned) or returns several values.
- **Twin logic (the right rule):** When return executes, the method ends at once, so the loop stops on that pass.
- **Role:** primary

**6. `for_loop` &rarr; `ReturnDoesNotExitLoop`** (misconception)

- **Exact edge logic (the wrong rule):** A return inside a loop does not end the loop; it sets a value each pass (the last one is returned) or returns several values.
- **Twin logic (the right rule):** When return executes, the method ends at once, so the loop stops on that pass.
- **Role:** context

**7. `flag_search_loop` &rarr; `LoopIgnoresCodeBefore`** (error)

- **Exact edge logic (the wrong rule):** Initializes the flag before the loop so that the loop condition is already false, and the loop body never runs.
- **Twin logic (the right rule):** A while loop tests its condition before the first pass: if the values set before the loop make the condition false, the body never runs.
- **Role:** context

**8. `logical_error` &rarr; `LoopIgnoresCodeBefore`** (error)

- **Exact edge logic (the wrong rule):** Initializes the flag before the loop so that the loop condition is already false, and the loop body never runs.
- **Twin logic (the right rule):** A while loop tests its condition before the first pass: if the values set before the loop make the condition false, the body never runs.
- **Role:** context

**9. `while_loop` &rarr; `LoopIgnoresCodeBefore`** (error)

- **Exact edge logic (the wrong rule):** Initializes the flag before the loop so that the loop condition is already false, and the loop body never runs.
- **Twin logic (the right rule):** A while loop tests its condition before the first pass: if the values set before the loop make the condition false, the body never runs.
- **Role:** primary

**10. `flag_search_loop` &rarr; `flag_search_loop@L0`** (has_level)

- **Exact edge logic:** flag search loop -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (3 ways).
  - **[0] everyday\_reading** (rule type E, folk-meaning rule): Folk meaning: in English, 'found' or 'is OK' describes the current item, so a novice writes \`found = (a[i] == target);\` on every pass. In a search, the flag must record whether any pass so far matched: it is set once (\`if (a[i] == target) found = true;\`) and never reset.
  - **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `FlagResetInLoop`: wrong rule: A search flag should be set back (to false/true) whenever a test fails. Right rule: A search flag is a one-way flag: once a pass records a find, no later pass may reset it, so the loop body contains only \`if (match) found = true;\` with no else.
  - **[2] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `FlagResetInLoop`: Applies the LT rule unevenly: on a trace, the flag is updated on non-matching passes as if there were an else, or the trace forgets that the flag carries over from the previous pass. The traced final flag then reflects only the last element. (here mixing in: "A search flag should be set back to true whenever a test fails")

**11. `flag_search_loop` &rarr; `flag_search_loop@L1`** (has_level)

- **Exact edge logic:** flag search loop -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).
  - **[0] names\_the\_element** (rule type N, identity rule): Loop plan: a boolean flag variable initialised before a loop and set by the loop when a condition is found, recording whether the condition held on any pass.
  - **[1] states\_the\_rule** (rule type S, declarative rule): \`boolean found = false; for (int i = 0; i &lt; n; i++) if (a[i] == target) found = true;\` To stop early, add the flag to the test: \`while (i &lt; n &amp;&amp; !found)\`.

**12. `flag_search_loop` &rarr; `flag_search_loop@L2`** (has_level)

- **Exact edge logic:** flag search loop -&gt; L2 (Multistructural): the answer applies the rules of flag search loop to every part of the code, in order (3 ways).
  - **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): Order: initialise the flag once before the loop. On each pass, test the loop condition (which may include \`!found\`), then evaluate the guard, and only if it is true assign \`found = true\`. Read the flag after the loop.
  - **[1] output\_prediction** (rule type OP, evaluation / result rule): The result is a boolean: true if at least one pass satisfied the guard, false if none did (including zero passes). For {3, 5, 7} and target 5, found is true.
  - **[2] one\_step\_execution** (rule type OS, state-transition rule): A matching pass changes only the flag, from false to true (and it stays true). A non-matching pass changes nothing. \`found = true\` as a statement has the value true, which is discarded.

**13. `flag_search_loop` &rarr; `flag_search_loop@L3`** (has_level)

- **Exact edge logic:** flag search loop -&gt; L3 (Relational): the answer relates the parts (3 ways).
  - **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): The flag must be declared before the for loop to be visible after it. The for loop's test can include \`!found\` to stop at the first find; without that, the loop runs all passes, and the flag still works because it is one-way.
  - **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Two ways to stop a search when the item is found: break leaves the loop at once, while a boolean flag is set and tested in the loop condition so the loop ends at its next test. After either, the code must tell the found case from the loop finishing normally.
  - **[2] purpose\_of\_the\_whole** (rule type P, plan / role rule): Plan: search / existence-check plan. The flag plays the Sajaniemi one-way flag role. It answers 'is there any element with property P?' or 'is the array sorted?'.

**14. `flag_search_loop` &rarr; `flag_search_loop@L4`** (has_level)

- **Exact edge logic:** flag search loop -&gt; L4 (Extended abstract): the answer reasons beyond the given code (5 ways).
  - **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `FlagResetInLoop`: Invariant: after k passes, found == (some element among the first k matched). Adding an else that resets the flag breaks the invariant, as does replacing the guard with \`found = (a[i] == target)\`. Adding \`!found\` to the loop test keeps the result and only saves passes. Initialising the flag to true breaks the result for inputs with no match.
  - **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Use a flag when you need a yes/no answer after a loop, or a stopping condition that is set in the middle of a pass. In a method, \`return\` from inside the loop (or \`break\`) is often simpler. Use a counter when you need how many, not whether.
  - **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: A while loop tests its condition before the first pass: if the values set before the loop make the condition false, the body never runs. Kind: silent logic error. Trigger class: Initialising the flag so that the loop test is already false (e.g. \`boolean found = true; while (!found) {...}\`): the search never runs.
  - **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: A search flag is one-way: it must not be reassigned on every pass. Kind: silent logic error. Trigger class: \`found = (a[i] == target);\` or an else branch that sets \`found = false\`: the result reflects only the last element and fails when the match is not last.
  - **[4] diagnose\_an\_error** (rule type D, error rule): rule broken: Using = instead of == on a boolean flag assigns instead of testing. Kind: silent logic error. Trigger class: \`if (found = false)\` compiles (boolean assignment) and is always false; write \`if (!found)\`.

**15. `topic1.3.f` &rarr; `flag_search_loop`** (contains)

- topic `topic1.3.f` contains `flag_search_loop`

**16. `topic1.3.f` &rarr; `accumulator_pattern`** (contains)

- topic `topic1.3.f` contains `accumulator_pattern`

**17. `topic1.3.f` &rarr; `convergence_test`** (contains)

- topic `topic1.3.f` contains `convergence_test`

**18. `topic1.3.f` &rarr; `counter_pattern`** (contains)

- topic `topic1.3.f` contains `counter_pattern`

**19. `topic1.3.f` &rarr; `debugging`** (contains)

- topic `topic1.3.f` contains `debugging`

**20. `topic1.3.f` &rarr; `fencepost_loop`** (contains)

- topic `topic1.3.f` contains `fencepost_loop`

**21. `topic1.3.f` &rarr; `loop_performance`** (contains)

- topic `topic1.3.f` contains `loop_performance`

**22. `topic1.3.f` &rarr; `monte_carlo_simulation`** (contains)

- topic `topic1.3.f` contains `monte_carlo_simulation`

**23. `topic1.3.f` &rarr; `number_conversion`** (contains)

- topic `topic1.3.f` contains `number_conversion`

**24. `topic1.3.f` &rarr; `testing`** (contains)

- topic `topic1.3.f` contains `testing`
