# infinite_loop (`infinite_loop`)

a loop whose condition never becomes false

Section 1.3 Conditionals and Loops, topic 1.3.h Infinite loops.

![The knowledge graph around infinite_loop](infinite_loop.png)

## At a glance

- **Needs first:** `for_loop`, `loop_control`, `while_loop`
- **Leads to:** nothing
- **Learned alongside:** nothing
- **Misconceptions:** `CompoundAssignmentNoCast`, `InfiniteLoopUnnoticed`, `JavaDetectsInfiniteLoops`, `LoopVariableNotUpdated`
- **Errors:** none
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 19 edges around this concept. The edge logic, the wrong and right rules and the exact rules of the ways are copied word for word from the graph.

## To work on (0)

Nothing is missing for this concept.

## What it needs first (3)

A prerequisite edge means the other concept has to be understood before `infinite_loop`.

### `for_loop` comes before `infinite_loop`

*a while with init/condition/update packaged together*

- **Edge:** `pre:for_loop->infinite_loop`
- **Exact edge logic:** A for loop whose condition never becomes false (or is left out) repeats forever unless a break ends it.
- **Grounding:** spec\_passage

### `loop_control` comes before `infinite_loop`

*the three slots: init ; condition ; update*

- **Edge:** `pre:loop_control->infinite_loop`
- **Exact edge logic:** A loop is infinite when its update never moves the condition towards false.
- **Grounding:** book\_passage
- **Composition rule (R) of `infinite_loop` with `loop_control`:** A loop is finite only if its update moves the control variable towards making the condition false. Wrong direction (\`i--\` with \`i &lt; n\`), wrong step (\`i += 0\` or \`x += 0.5\` on an int), or a condition that the update can step over (\`i != 10\` with \`i += 3\`) all give infinite loops.
- **Composition rule (R) of `loop_control` with `infinite_loop`:** A loop is infinite when the update never moves the variable toward making the condition false (e.g. condition i &gt; 3 with update i = i + 1).

### `while_loop` comes before `infinite_loop`

*repeat a block while a condition holds*

- **Edge:** `pre:while_loop->infinite_loop`
- **Exact edge logic:** A while loop whose condition never becomes false never ends.
- **Grounding:** book\_passage

## What it leads to (0)

These concepts need `infinite_loop` first.

No concept has this one as a prerequisite.

## Learned alongside (0)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

No parallel edge touches this concept.

## Misconceptions (4)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### CompoundAssignmentNoCast

- **Edge:** `infinite_loop` &rarr; `CompoundAssignmentNoCast` (misconception)
- **Exact edge logic (the wrong rule):** x += 0.5 adds one half to an int x.
- **Twin logic (the right rule):** x += 0.5 is x = (int) (x + 0.5), so an int x does not change.
- **Wrong belief (on the node):** x += 0.5 adds one half to an int x.
- **Correct rule (on the node):** x += 0.5 is x = (int) (x + 0.5), so an int x does not change.
- **Provenance:** textbook
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [4] misconception, exact rule:** wrong rule: \`x += 0.5\` adds one half to an int x. Right rule: \`x += 0.5\` means \`x = (int) (x + 0.5)\`; the narrowing rounds toward zero, so a nonnegative int x keeps its value, and a loop relying on it never progresses.
- **Edge `compound_assignment` &rarr; `CompoundAssignmentNoCast`, exact edge logic:** x += 0.5 adds one half to an int x. **Twin logic:** x += 0.5 is x = (int) (x + 0.5), so an int x does not change. (role: primary)

### InfiniteLoopUnnoticed

- **Edge:** `infinite_loop` &rarr; `InfiniteLoopUnnoticed` (misconception)
- **Exact edge logic (the wrong rule):** a condition that never goes false still terminates
- **Twin logic (the right rule):** A while loop stops only when its condition is false at a check, so if no pass changes the variables in the condition, it never stops.
- **Wrong belief (on the node):** a condition that never goes false still terminates
- **Correct rule (on the node):** A while loop stops only when its condition is false at a check, so if no pass changes the variables in the condition, it never stops.
- **Provenance:** published
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [1] misconception, exact rule:** wrong rule: A loop whose condition never goes false will still terminate. Right rule: A while loop stops only when its condition is false at a check, so if no pass changes the variables in the condition, it never stops.
- **L0 way [3] inconsistent\_trace, exact rule:** Applies the loop LT rule unevenly: on a trace, the update is assumed to happen on every pass even when it is skipped (e.g. by continue or inside an if), or the loop is assumed to stop when the condition becomes false in the middle of the body. The traced run then ends where the real one does not. (here mixing in: "a condition that never goes false still terminates")
- **Edge `loop_control` &rarr; `InfiniteLoopUnnoticed`, exact edge logic:** A while loop always stops on its own, even if nothing in its body can make the condition false. **Twin logic:** A while loop stops only when its condition is false at a check, so if no pass changes the variables in the condition, it never stops. (role: context)
- **Edge `while_loop` &rarr; `InfiniteLoopUnnoticed`, exact edge logic:** a condition that never goes false still terminates **Twin logic:** A while loop stops only when its condition is false at a check, so if no pass changes the variables in the condition, it never stops. (role: context)

### JavaDetectsInfiniteLoops

- **Edge:** `infinite_loop` &rarr; `JavaDetectsInfiniteLoops` (misconception)
- **Exact edge logic (the wrong rule):** If my loop never ends, the compiler or Java will warn me.
- **Twin logic (the right rule):** Java cannot detect infinite loops in general; you must check that the loop condition eventually becomes false.
- **Wrong belief (on the node):** If my loop never ends, the compiler or Java will warn me.
- **Correct rule (on the node):** Java cannot detect infinite loops in general; you must check that the loop condition eventually becomes false.
- **Provenance:** textbook
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [2] misconception, exact rule:** wrong rule: If my loop never ends, the compiler or Java will warn me. Right rule: Java cannot detect infinite loops in general (the halting problem); you must check that the condition eventually becomes false.
- **Edge `while_loop` &rarr; `JavaDetectsInfiniteLoops`, exact edge logic:** If my loop never ends, the compiler or Java will warn me. **Twin logic:** Java cannot detect infinite loops in general; you must check that the loop condition eventually becomes false. (role: context)

### LoopVariableNotUpdated

- **Edge:** `infinite_loop` &rarr; `LoopVariableNotUpdated` (misconception)
- **Exact edge logic (the wrong rule):** A while loop ends by itself even if nothing in the body changes the variable tested in the condition.
- **Twin logic (the right rule):** If no statement in the body changes a variable in the condition, a condition that was true stays true and the loop never ends.
- **Wrong belief (on the node):** A while loop ends by itself even if nothing in the body changes the variable tested in the condition.
- **Correct rule (on the node):** If no statement in the body changes a variable in the condition, a condition that was true stays true and the loop never ends.
- **Provenance:** published
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [5] misconception, exact rule:** wrong rule: A while loop ends by itself even if nothing in the body changes the variable tested in the condition. Right rule: If no statement in the body changes a variable in the condition, a condition that was true stays true and the loop never ends.
- **Edge `loop_guard` &rarr; `LoopVariableNotUpdated`, exact edge logic:** A while loop ends by itself even if nothing in the body changes the variable tested in the condition. **Twin logic:** If no statement in the body changes a variable in the condition, a condition that was true stays true and the loop never ends. (role: primary)
- **Edge `while_loop` &rarr; `LoopVariableNotUpdated`, exact edge logic:** A while loop ends by itself even if nothing in the body changes the variable tested in the condition. **Twin logic:** If no statement in the body changes a variable in the condition, a condition that was true stays true and the loop never ends. (role: context)

## Errors (0)

An error edge states the rule that gets broken in a program, and the right rule.

The graph has no error edge from this concept.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for infinite loop: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to infinite loop agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

- **Edge:** `infinite_loop` &rarr; `infinite_loop@L0` (has_level)
- **Exact edge logic:** infinite loop -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (6 ways).

Ways (6), each with its exact rule:

- **[0] everyday\_reading** (rule type E, folk-meaning rule): Folk meaning: in everyday instructions ('lather, rinse, repeat', 'while the road is two lanes, continue north') the reader stops sensibly or watches the condition all the time. A Java loop repeats only while its condition is true at each test, and it never stops on its own if no pass makes the condition false.
- **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `InfiniteLoopUnnoticed`: wrong rule: A loop whose condition never goes false will still terminate. Right rule: A while loop stops only when its condition is false at a check, so if no pass changes the variables in the condition, it never stops.
- **[2] misconception** (rule type M, wrong rule / right rule) &rarr; `JavaDetectsInfiniteLoops`: wrong rule: If my loop never ends, the compiler or Java will warn me. Right rule: Java cannot detect infinite loops in general (the halting problem); you must check that the condition eventually becomes false.
- **[3] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `InfiniteLoopUnnoticed`: Applies the loop LT rule unevenly: on a trace, the update is assumed to happen on every pass even when it is skipped (e.g. by continue or inside an if), or the loop is assumed to stop when the condition becomes false in the middle of the body. The traced run then ends where the real one does not. (here mixing in: "a condition that never goes false still terminates")
- **[4] misconception** (rule type M, wrong rule / right rule) &rarr; `CompoundAssignmentNoCast`: wrong rule: \`x += 0.5\` adds one half to an int x. Right rule: \`x += 0.5\` means \`x = (int) (x + 0.5)\`; the narrowing rounds toward zero, so a nonnegative int x keeps its value, and a loop relying on it never progresses.
- **[5] misconception** (rule type M, wrong rule / right rule) &rarr; `LoopVariableNotUpdated`: wrong rule: A while loop ends by itself even if nothing in the body changes the variable tested in the condition. Right rule: If no statement in the body changes a variable in the condition, a condition that was true stays true and the loop never ends.

### L1: Unistructural / atom x text surface

L1 for infinite loop: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

- **Edge:** `infinite_loop` &rarr; `infinite_loop@L1` (has_level)
- **Exact edge logic:** infinite loop -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

Ways (2), each with its exact rule:

- **[0] names\_the\_element** (rule type N, identity rule): Loop bug/behaviour: a loop whose continuation condition never becomes false, so it runs until the program is killed (or overflow intervenes).
- **[1] states\_the\_rule** (rule type S, declarative rule): A while or for loop terminates only if some pass makes its condition false at a test (or a break or return runs). Otherwise it repeats forever. The compiler does not check this.

### L2: Multistructural / block x execution / preoperational

L2 for infinite loop: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

- **Edge:** `infinite_loop` &rarr; `infinite_loop@L2` (has_level)
- **Exact edge logic:** infinite loop -&gt; L2 (Multistructural): the answer applies the rules of infinite loop to every part of the code, in order (3 ways).

Ways (3), each with its exact rule:

- **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): The same order as any loop: test, body, test... In an infinite loop the update either never runs or never moves the tested variables towards false, so every test yields true.
- **[1] output\_prediction** (rule type OP, evaluation / result rule): There is no final value. Either output scrolls forever (BadHellos with \`i &gt; 3\`) or nothing happens and the program 'hangs'. Over a very long run, int overflow may eventually make the test false (BadHellos stops after about 2^31 lines).
- **[2] one\_step\_execution** (rule type OS, state-transition rule): Each pass leaves the condition's variables either unchanged or moving away from false (i grows while the test is \`i &gt; 3\`). So the state after the pass satisfies the condition again.

### L3: Relational / relations x function (concrete operational begins)

L3 for infinite loop: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

- **Edge:** `infinite_loop` &rarr; `infinite_loop@L3` (has_level)
- **Exact edge logic:** infinite loop -&gt; L3 (Relational): the answer relates the parts (2 ways).

Ways (2), each with its exact rule:

- **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): A loop is finite only if its update moves the control variable towards making the condition false. Wrong direction (\`i--\` with \`i &lt; n\`), wrong step (\`i += 0\` or \`x += 0.5\` on an int), or a condition that the update can step over (\`i != 10\` with \`i += 3\`) all give infinite loops.
- **[1] purpose\_of\_the\_whole** (rule type P, plan / role rule): Purpose: usually a bug. An intentional \`while (true)\` with an internal break or return is the 'loop-and-a-half' plan for servers, event loops and read-until-sentinel input.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for infinite loop: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

- **Edge:** `infinite_loop` &rarr; `infinite_loop@L4` (has_level)
- **Exact edge logic:** infinite loop -&gt; L4 (Extended abstract): the answer reasons beyond the given code (7 ways).

Ways (7), each with its exact rule:

- **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `InfiniteLoopUnnoticed`: Changing the condition or update can turn a terminating loop into an infinite one (\`i &lt;= 10\` to \`i &gt; 3\`), or the reverse. The termination argument (a quantity that strictly moves towards the bound on every pass) must survive any change.
- **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Write \`while (true)\` only when the exit is in the middle of the body and is certain (break or return on a sentinel or event). Otherwise, for each loop, state why the condition eventually becomes false. When a program seems stuck, add trace prints to tell an infinite loop from a slow one.
- **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: The body must change a variable in the condition so that it eventually becomes false. Kind: silent logic error. Trigger class: A forgotten \`i++\` (or an update inside an if or after a continue): the program hangs or prints forever.
- **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: An empty statement after the loop header becomes the body. Kind: silent logic error. Trigger class: \`while (i &lt; 10); { i++; }\`: the stray \`;\` is an empty body that never changes i.
- **[4] diagnose\_an\_error** (rule type D, error rule): rule broken: Tests on doubles or on exact values can be stepped over. Kind: silent logic error. Trigger class: \`for (double x = 0.0; x != 1.0; x += 0.1)\` or \`while (i != 10) i += 3;\`: the variable jumps past the stopping value.
- **[5] diagnose\_an\_error** (rule type D, error rule): rule broken: int arithmetic wraps without warning. Kind: silent logic error. Trigger class: \`for (int i = 0; i &lt;= Integer.MAX\_VALUE; i++)\`: i overflows to a negative value, so the test is never false.
- **[6] diagnose\_an\_error** (rule type D, error rule): rule broken: Code after a loop that can never complete normally is unreachable. Kind: compile-time. Trigger class: Statements after \`while (true) { ... }\` with no break (unreachable statement).

## Same topic

`infinite_loop` belongs to the topic **Infinite loops** (`topic1.3.h`). It is the only concept of that topic.

## Rules of the concept (20)

- **Book** (SW-1e, p. 72 (pdf 82)): "what if the loop-continuation condition in a while loop is always satisfied?"
- **Book** (TJ-2e, p. 103 (pdf 125)): "infinite loop: A loop whose condition is always true."
- **Book** (OT-For, ): "The three expressions of the for loop are optional; an infinite loop can be created as follows:"
- **Book** (LI, ): "If the loop-continuation-condition in a for loop is omitted, it is implicitly true."
- **E** (folk-meaning rule): Folk meaning: in everyday instructions ('lather, rinse, repeat', 'while the road is two lanes, continue north') the reader stops sensibly or watches the condition all the time. A Java loop repeats only while its condition is true at each test, and it never stops on its own if no pass makes the condition false.
- **M** (wrong rule / right rule): CompoundAssignmentNoCast: wrong: \`x += 0.5\` adds one half to an int x. \| right: \`x += 0.5\` means \`x = (int) (x + 0.5)\`; the narrowing rounds toward zero, so a nonnegative int x keeps its value, and a loop relying on it never progresses.
- **M** (wrong rule / right rule): InfiniteLoopUnnoticed: wrong: A loop whose condition never goes false will still terminate. \| right: A while loop stops only when its condition is false at a check, so if no pass changes the variables in the condition, it never stops.
- **M** (wrong rule / right rule): JavaDetectsInfiniteLoops: wrong: If my loop never ends, the compiler or Java will warn me. \| right: Java cannot detect infinite loops in general (the halting problem); you must check that the condition eventually becomes false.
- **M** (wrong rule / right rule): LoopVariableNotUpdated: wrong: A while loop ends by itself even if nothing in the body changes the variable tested in the condition. \| right: If no statement in the body changes a variable in the condition, a condition that was true stays true and the loop never ends.
- **T** (uneven-application rule): Applies the loop LT rule unevenly: on a trace, the update is assumed to happen on every pass even when it is skipped (e.g. by continue or inside an if), or the loop is assumed to stop when the condition becomes false in the middle of the body. The traced run then ends where the real one does not.
- **N** (identity rule): Loop bug/behaviour: a loop whose continuation condition never becomes false, so it runs until the program is killed (or overflow intervenes).
- **S** (declarative rule): A while or for loop terminates only if some pass makes its condition false at a test (or a break or return runs). Otherwise it repeats forever. The compiler does not check this.
- **LT** (operational sequencing rule): The same order as any loop: test, body, test... In an infinite loop the update either never runs or never moves the tested variables towards false, so every test yields true.
- **OP** (evaluation / result rule): There is no final value. Either output scrolls forever (BadHellos with \`i &gt; 3\`) or nothing happens and the program 'hangs'. Over a very long run, int overflow may eventually make the test false (BadHellos stops after about 2^31 lines).
- **OS** (state-transition rule): Each pass leaves the condition's variables either unchanged or moving away from false (i grows while the test is \`i &gt; 3\`). So the state after the pass satisfies the condition again.
- **R** (composition rule (with a neighbour)): with loop\_control: A loop is finite only if its update moves the control variable towards making the condition false. Wrong direction (\`i--\` with \`i &lt; n\`), wrong step (\`i += 0\` or \`x += 0.5\` on an int), or a condition that the update can step over (\`i != 10\` with \`i += 3\`) all give infinite loops.
- **P** (plan / role rule): Purpose: usually a bug. An intentional \`while (true)\` with an internal break or return is the 'loop-and-a-half' plan for servers, event loops and read-until-sentinel input.
- **C** (conservation rule): Changing the condition or update can turn a terminating loop into an infinite one (\`i &lt;= 10\` to \`i &gt; 3\`), or the reverse. The termination argument (a quantity that strictly moves towards the bound on every pass) must survive any change.
- **D** (error rule): rule broken: The body must change a variable in the condition so that it eventually becomes false. (silent logic error)
- **D** (error rule): rule broken: An empty statement after the loop header becomes the body. (silent logic error)
- **D** (error rule): rule broken: Tests on doubles or on exact values can be stepped over. (silent logic error)
- **D** (error rule): rule broken: int arithmetic wraps without warning. (silent logic error)
- **D** (error rule): rule broken: Code after a loop that can never complete normally is unreachable. (compile-time)
- **X** (applicability rule): Write \`while (true)\` only when the exit is in the middle of the body and is certain (break or return on a sentinel or event). Otherwise, for each loop, state why the condition eventually becomes false. When a program seems stuck, add trace prints to tell an infinite loop from a slow one.

## How it is found in code and answers (reader block)

- **Aliases:** infinite loop, forever, never stops, never ends, endless
- **Code patterns:** `while\s*\(\s*true\s*\)`, `for\s*\(\s*;\s*;\s*\)`
- **Operator symbols:** none
- **Java types:** none

## The whole prerequisite chain

- **Everything it builds on (16):** `arithmetic_operators`, `boolean`, `boolean_expression`, `comparison_operators`, `data_type`, `do_while_loop`, `expression`, `for_loop`, `identifier`, `literal`, `logical_operators`, `loop_control`, `loop_variable`, `primitive_type`, `variable`, `while_loop`
- **Everything that builds on it (0):** nothing

## Every edge in this view and its exact edge logic (19)

All the edges drawn in the picture, in the order: prerequisite, parallel, misconception, error, has_level, contains.

**1. `for_loop` &rarr; `infinite_loop`** (prerequisite)

- **Exact edge logic:** A for loop whose condition never becomes false (or is left out) repeats forever unless a break ends it.
- **Grounding:** spec\_passage

**2. `loop_control` &rarr; `infinite_loop`** (prerequisite)

- **Exact edge logic:** A loop is infinite when its update never moves the condition towards false.
- **Grounding:** book\_passage
- **Composition rule (R) of `loop_control` with `infinite_loop`:** A loop is infinite when the update never moves the variable toward making the condition false (e.g. condition i &gt; 3 with update i = i + 1).
- **Composition rule (R) of `infinite_loop` with `loop_control`:** A loop is finite only if its update moves the control variable towards making the condition false. Wrong direction (\`i--\` with \`i &lt; n\`), wrong step (\`i += 0\` or \`x += 0.5\` on an int), or a condition that the update can step over (\`i != 10\` with \`i += 3\`) all give infinite loops.

**3. `while_loop` &rarr; `infinite_loop`** (prerequisite)

- **Exact edge logic:** A while loop whose condition never becomes false never ends.
- **Grounding:** book\_passage

**4. `infinite_loop` &rarr; `CompoundAssignmentNoCast`** (misconception)

- **Exact edge logic (the wrong rule):** x += 0.5 adds one half to an int x.
- **Twin logic (the right rule):** x += 0.5 is x = (int) (x + 0.5), so an int x does not change.
- **Role:** context

**5. `infinite_loop` &rarr; `InfiniteLoopUnnoticed`** (misconception)

- **Exact edge logic (the wrong rule):** a condition that never goes false still terminates
- **Twin logic (the right rule):** A while loop stops only when its condition is false at a check, so if no pass changes the variables in the condition, it never stops.
- **Role:** primary

**6. `infinite_loop` &rarr; `JavaDetectsInfiniteLoops`** (misconception)

- **Exact edge logic (the wrong rule):** If my loop never ends, the compiler or Java will warn me.
- **Twin logic (the right rule):** Java cannot detect infinite loops in general; you must check that the loop condition eventually becomes false.
- **Role:** primary

**7. `infinite_loop` &rarr; `LoopVariableNotUpdated`** (misconception)

- **Exact edge logic (the wrong rule):** A while loop ends by itself even if nothing in the body changes the variable tested in the condition.
- **Twin logic (the right rule):** If no statement in the body changes a variable in the condition, a condition that was true stays true and the loop never ends.
- **Role:** context

**8. `compound_assignment` &rarr; `CompoundAssignmentNoCast`** (misconception)

- **Exact edge logic (the wrong rule):** x += 0.5 adds one half to an int x.
- **Twin logic (the right rule):** x += 0.5 is x = (int) (x + 0.5), so an int x does not change.
- **Role:** primary

**9. `loop_control` &rarr; `InfiniteLoopUnnoticed`** (misconception)

- **Exact edge logic (the wrong rule):** A while loop always stops on its own, even if nothing in its body can make the condition false.
- **Twin logic (the right rule):** A while loop stops only when its condition is false at a check, so if no pass changes the variables in the condition, it never stops.
- **Role:** context

**10. `loop_guard` &rarr; `LoopVariableNotUpdated`** (misconception)

- **Exact edge logic (the wrong rule):** A while loop ends by itself even if nothing in the body changes the variable tested in the condition.
- **Twin logic (the right rule):** If no statement in the body changes a variable in the condition, a condition that was true stays true and the loop never ends.
- **Role:** primary

**11. `while_loop` &rarr; `InfiniteLoopUnnoticed`** (misconception)

- **Exact edge logic (the wrong rule):** a condition that never goes false still terminates
- **Twin logic (the right rule):** A while loop stops only when its condition is false at a check, so if no pass changes the variables in the condition, it never stops.
- **Role:** context

**12. `while_loop` &rarr; `JavaDetectsInfiniteLoops`** (misconception)

- **Exact edge logic (the wrong rule):** If my loop never ends, the compiler or Java will warn me.
- **Twin logic (the right rule):** Java cannot detect infinite loops in general; you must check that the loop condition eventually becomes false.
- **Role:** context

**13. `while_loop` &rarr; `LoopVariableNotUpdated`** (misconception)

- **Exact edge logic (the wrong rule):** A while loop ends by itself even if nothing in the body changes the variable tested in the condition.
- **Twin logic (the right rule):** If no statement in the body changes a variable in the condition, a condition that was true stays true and the loop never ends.
- **Role:** context

**14. `infinite_loop` &rarr; `infinite_loop@L0`** (has_level)

- **Exact edge logic:** infinite loop -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (6 ways).
  - **[0] everyday\_reading** (rule type E, folk-meaning rule): Folk meaning: in everyday instructions ('lather, rinse, repeat', 'while the road is two lanes, continue north') the reader stops sensibly or watches the condition all the time. A Java loop repeats only while its condition is true at each test, and it never stops on its own if no pass makes the condition false.
  - **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `InfiniteLoopUnnoticed`: wrong rule: A loop whose condition never goes false will still terminate. Right rule: A while loop stops only when its condition is false at a check, so if no pass changes the variables in the condition, it never stops.
  - **[2] misconception** (rule type M, wrong rule / right rule) &rarr; `JavaDetectsInfiniteLoops`: wrong rule: If my loop never ends, the compiler or Java will warn me. Right rule: Java cannot detect infinite loops in general (the halting problem); you must check that the condition eventually becomes false.
  - **[3] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `InfiniteLoopUnnoticed`: Applies the loop LT rule unevenly: on a trace, the update is assumed to happen on every pass even when it is skipped (e.g. by continue or inside an if), or the loop is assumed to stop when the condition becomes false in the middle of the body. The traced run then ends where the real one does not. (here mixing in: "a condition that never goes false still terminates")
  - **[4] misconception** (rule type M, wrong rule / right rule) &rarr; `CompoundAssignmentNoCast`: wrong rule: \`x += 0.5\` adds one half to an int x. Right rule: \`x += 0.5\` means \`x = (int) (x + 0.5)\`; the narrowing rounds toward zero, so a nonnegative int x keeps its value, and a loop relying on it never progresses.
  - **[5] misconception** (rule type M, wrong rule / right rule) &rarr; `LoopVariableNotUpdated`: wrong rule: A while loop ends by itself even if nothing in the body changes the variable tested in the condition. Right rule: If no statement in the body changes a variable in the condition, a condition that was true stays true and the loop never ends.

**15. `infinite_loop` &rarr; `infinite_loop@L1`** (has_level)

- **Exact edge logic:** infinite loop -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).
  - **[0] names\_the\_element** (rule type N, identity rule): Loop bug/behaviour: a loop whose continuation condition never becomes false, so it runs until the program is killed (or overflow intervenes).
  - **[1] states\_the\_rule** (rule type S, declarative rule): A while or for loop terminates only if some pass makes its condition false at a test (or a break or return runs). Otherwise it repeats forever. The compiler does not check this.

**16. `infinite_loop` &rarr; `infinite_loop@L2`** (has_level)

- **Exact edge logic:** infinite loop -&gt; L2 (Multistructural): the answer applies the rules of infinite loop to every part of the code, in order (3 ways).
  - **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): The same order as any loop: test, body, test... In an infinite loop the update either never runs or never moves the tested variables towards false, so every test yields true.
  - **[1] output\_prediction** (rule type OP, evaluation / result rule): There is no final value. Either output scrolls forever (BadHellos with \`i &gt; 3\`) or nothing happens and the program 'hangs'. Over a very long run, int overflow may eventually make the test false (BadHellos stops after about 2^31 lines).
  - **[2] one\_step\_execution** (rule type OS, state-transition rule): Each pass leaves the condition's variables either unchanged or moving away from false (i grows while the test is \`i &gt; 3\`). So the state after the pass satisfies the condition again.

**17. `infinite_loop` &rarr; `infinite_loop@L3`** (has_level)

- **Exact edge logic:** infinite loop -&gt; L3 (Relational): the answer relates the parts (2 ways).
  - **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): A loop is finite only if its update moves the control variable towards making the condition false. Wrong direction (\`i--\` with \`i &lt; n\`), wrong step (\`i += 0\` or \`x += 0.5\` on an int), or a condition that the update can step over (\`i != 10\` with \`i += 3\`) all give infinite loops.
  - **[1] purpose\_of\_the\_whole** (rule type P, plan / role rule): Purpose: usually a bug. An intentional \`while (true)\` with an internal break or return is the 'loop-and-a-half' plan for servers, event loops and read-until-sentinel input.

**18. `infinite_loop` &rarr; `infinite_loop@L4`** (has_level)

- **Exact edge logic:** infinite loop -&gt; L4 (Extended abstract): the answer reasons beyond the given code (7 ways).
  - **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `InfiniteLoopUnnoticed`: Changing the condition or update can turn a terminating loop into an infinite one (\`i &lt;= 10\` to \`i &gt; 3\`), or the reverse. The termination argument (a quantity that strictly moves towards the bound on every pass) must survive any change.
  - **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Write \`while (true)\` only when the exit is in the middle of the body and is certain (break or return on a sentinel or event). Otherwise, for each loop, state why the condition eventually becomes false. When a program seems stuck, add trace prints to tell an infinite loop from a slow one.
  - **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: The body must change a variable in the condition so that it eventually becomes false. Kind: silent logic error. Trigger class: A forgotten \`i++\` (or an update inside an if or after a continue): the program hangs or prints forever.
  - **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: An empty statement after the loop header becomes the body. Kind: silent logic error. Trigger class: \`while (i &lt; 10); { i++; }\`: the stray \`;\` is an empty body that never changes i.
  - **[4] diagnose\_an\_error** (rule type D, error rule): rule broken: Tests on doubles or on exact values can be stepped over. Kind: silent logic error. Trigger class: \`for (double x = 0.0; x != 1.0; x += 0.1)\` or \`while (i != 10) i += 3;\`: the variable jumps past the stopping value.
  - **[5] diagnose\_an\_error** (rule type D, error rule): rule broken: int arithmetic wraps without warning. Kind: silent logic error. Trigger class: \`for (int i = 0; i &lt;= Integer.MAX\_VALUE; i++)\`: i overflows to a negative value, so the test is never false.
  - **[6] diagnose\_an\_error** (rule type D, error rule): rule broken: Code after a loop that can never complete normally is unreachable. Kind: compile-time. Trigger class: Statements after \`while (true) { ... }\` with no break (unreachable statement).

**19. `topic1.3.h` &rarr; `infinite_loop`** (contains)

- topic `topic1.3.h` contains `infinite_loop`
