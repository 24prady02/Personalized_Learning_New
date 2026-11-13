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

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 19 edges around this concept, each explained in the graph's own words.

## What it needs first (3)

A prerequisite edge means the other concept has to be understood before `infinite_loop`.

### `for_loop` comes before `infinite_loop`

*a while with init/condition/update packaged together*

A for loop whose condition never becomes false (or is left out) repeats forever unless a break ends it.

- **Grounding:** spec passage

### `loop_control` comes before `infinite_loop`

*the three slots: init ; condition ; update*

A loop is infinite when its update never moves the condition towards false.

- **Grounding:** book passage
- **How `infinite_loop` combines with `loop_control`:** A loop is finite only if its update moves the control variable towards making the condition false. Wrong direction (\`i--\` with \`i &lt; n\`), wrong step (\`i += 0\` or \`x += 0.5\` on an int), or a condition that the update can step over (\`i != 10\` with \`i += 3\`) all give infinite loops.
- **How `loop_control` combines with `infinite_loop`:** A loop is infinite when the update never moves the variable toward making the condition false (e.g. condition i &gt; 3 with update i = i + 1).

### `while_loop` comes before `infinite_loop`

*repeat a block while a condition holds*

A while loop whose condition never becomes false never ends.

- **Grounding:** book passage

## What it leads to (0)

These concepts need `infinite_loop` first.

No concept has this one as a prerequisite.

## Learned alongside (0)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

No parallel edge touches this concept.

## Misconceptions (4)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### CompoundAssignmentNoCast

- **Wrong rule:** x += 0.5 adds one half to an int x.
- **Right rule:** x += 0.5 is x = (int) (x + 0.5), so an int x does not change.
- **Role of this concept:** context
- **Shows at level L0 as:** misconception: wrong rule: \`x += 0.5\` adds one half to an int x. Right rule: \`x += 0.5\` means \`x = (int) (x + 0.5)\`; the narrowing rounds toward zero, so a nonnegative int x keeps its value, and a loop relying on it never progresses.
- **Also an edge from `compound_assignment`:** x += 0.5 adds one half to an int x.

### InfiniteLoopUnnoticed

- **Wrong rule:** a condition that never goes false still terminates
- **Right rule:** A while loop stops only when its condition is false at a check, so if no pass changes the variables in the condition, it never stops.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: A loop whose condition never goes false will still terminate. Right rule: A while loop stops only when its condition is false at a check, so if no pass changes the variables in the condition, it never stops.
- **Shows at level L0 as:** inconsistent trace: Applies the loop LT rule unevenly: on a trace, the update is assumed to happen on every pass even when it is skipped (e.g. by continue or inside an if), or the loop is assumed to stop when the condition becomes false in the middle of the body. The traced run then ends where the real one does not. (here mixing in: "a condition that never goes false still terminates")
- **Also an edge from `loop_control`:** A while loop always stops on its own, even if nothing in its body can make the condition false.
- **Also an edge from `while_loop`:** a condition that never goes false still terminates

### JavaDetectsInfiniteLoops

- **Wrong rule:** If my loop never ends, the compiler or Java will warn me.
- **Right rule:** Java cannot detect infinite loops in general; you must check that the loop condition eventually becomes false.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: If my loop never ends, the compiler or Java will warn me. Right rule: Java cannot detect infinite loops in general (the halting problem); you must check that the condition eventually becomes false.
- **Also an edge from `while_loop`:** If my loop never ends, the compiler or Java will warn me.

### LoopVariableNotUpdated

- **Wrong rule:** A while loop ends by itself even if nothing in the body changes the variable tested in the condition.
- **Right rule:** If no statement in the body changes a variable in the condition, a condition that was true stays true and the loop never ends.
- **Role of this concept:** context
- **Shows at level L0 as:** misconception: wrong rule: A while loop ends by itself even if nothing in the body changes the variable tested in the condition. Right rule: If no statement in the body changes a variable in the condition, a condition that was true stays true and the loop never ends.
- **Also an edge from `loop_guard`:** A while loop ends by itself even if nothing in the body changes the variable tested in the condition.
- **Also an edge from `while_loop`:** A while loop ends by itself even if nothing in the body changes the variable tested in the condition.

## Errors (0)

An error edge states the rule that gets broken in a program, and the right rule.

The graph has no error edge from this concept.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for infinite loop: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to infinite loop agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

infinite loop -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (6 ways).

- **everyday reading** (folk-meaning rule): Folk meaning: in everyday instructions ('lather, rinse, repeat', 'while the road is two lanes, continue north') the reader stops sensibly or watches the condition all the time. A Java loop repeats only while its condition is true at each test, and it never stops on its own if no pass makes the condition false.
- **misconception** (wrong rule / right rule; shows `InfiniteLoopUnnoticed`): wrong rule: A loop whose condition never goes false will still terminate. Right rule: A while loop stops only when its condition is false at a check, so if no pass changes the variables in the condition, it never stops.
- **misconception** (wrong rule / right rule; shows `JavaDetectsInfiniteLoops`): wrong rule: If my loop never ends, the compiler or Java will warn me. Right rule: Java cannot detect infinite loops in general (the halting problem); you must check that the condition eventually becomes false.
- **inconsistent trace** (uneven-application rule; shows `InfiniteLoopUnnoticed`): Applies the loop LT rule unevenly: on a trace, the update is assumed to happen on every pass even when it is skipped (e.g. by continue or inside an if), or the loop is assumed to stop when the condition becomes false in the middle of the body. The traced run then ends where the real one does not. (here mixing in: "a condition that never goes false still terminates")
- **misconception** (wrong rule / right rule; shows `CompoundAssignmentNoCast`): wrong rule: \`x += 0.5\` adds one half to an int x. Right rule: \`x += 0.5\` means \`x = (int) (x + 0.5)\`; the narrowing rounds toward zero, so a nonnegative int x keeps its value, and a loop relying on it never progresses.
- **misconception** (wrong rule / right rule; shows `LoopVariableNotUpdated`): wrong rule: A while loop ends by itself even if nothing in the body changes the variable tested in the condition. Right rule: If no statement in the body changes a variable in the condition, a condition that was true stays true and the loop never ends.

### L1: Unistructural / atom x text surface

L1 for infinite loop: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

infinite loop -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

- **names the element** (identity rule): Loop bug/behaviour: a loop whose continuation condition never becomes false, so it runs until the program is killed (or overflow intervenes).
- **states the rule** (declarative rule): A while or for loop terminates only if some pass makes its condition false at a test (or a break or return runs). Otherwise it repeats forever. The compiler does not check this.

### L2: Multistructural / block x execution / preoperational

L2 for infinite loop: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

infinite loop -&gt; L2 (Multistructural): the answer applies the rules of infinite loop to every part of the code, in order (3 ways).

- **line by line trace** (operational sequencing rule): The same order as any loop: test, body, test... In an infinite loop the update either never runs or never moves the tested variables towards false, so every test yields true.
- **output prediction** (evaluation / result rule): There is no final value. Either output scrolls forever (BadHellos with \`i &gt; 3\`) or nothing happens and the program 'hangs'. Over a very long run, int overflow may eventually make the test false (BadHellos stops after about 2^31 lines).
- **one step execution** (state-transition rule): Each pass leaves the condition's variables either unchanged or moving away from false (i grows while the test is \`i &gt; 3\`). So the state after the pass satisfies the condition again.

### L3: Relational / relations x function (concrete operational begins)

L3 for infinite loop: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

infinite loop -&gt; L3 (Relational): the answer relates the parts (2 ways).

- **relation to neighbour** (composition rule (with a neighbour)): A loop is finite only if its update moves the control variable towards making the condition false. Wrong direction (\`i--\` with \`i &lt; n\`), wrong step (\`i += 0\` or \`x += 0.5\` on an int), or a condition that the update can step over (\`i != 10\` with \`i += 3\`) all give infinite loops.
- **purpose of the whole** (plan / role rule): Purpose: usually a bug. An intentional \`while (true)\` with an internal break or return is the 'loop-and-a-half' plan for servers, event loops and read-until-sentinel input.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for infinite loop: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

infinite loop -&gt; L4 (Extended abstract): the answer reasons beyond the given code (7 ways).

- **predict a change** (conservation rule; shows `InfiniteLoopUnnoticed`): Changing the condition or update can turn a terminating loop into an infinite one (\`i &lt;= 10\` to \`i &gt; 3\`), or the reverse. The termination argument (a quantity that strictly moves towards the bound on every pass) must survive any change.
- **transfer to a new program** (applicability rule): Write \`while (true)\` only when the exit is in the middle of the body and is certain (break or return on a sentinel or event). Otherwise, for each loop, state why the condition eventually becomes false. When a program seems stuck, add trace prints to tell an infinite loop from a slow one.
- **diagnose an error** (error rule): rule broken: The body must change a variable in the condition so that it eventually becomes false. Kind: silent logic error. Trigger class: A forgotten \`i++\` (or an update inside an if or after a continue): the program hangs or prints forever.
- **diagnose an error** (error rule): rule broken: An empty statement after the loop header becomes the body. Kind: silent logic error. Trigger class: \`while (i &lt; 10); { i++; }\`: the stray \`;\` is an empty body that never changes i.
- **diagnose an error** (error rule): rule broken: Tests on doubles or on exact values can be stepped over. Kind: silent logic error. Trigger class: \`for (double x = 0.0; x != 1.0; x += 0.1)\` or \`while (i != 10) i += 3;\`: the variable jumps past the stopping value.
- **diagnose an error** (error rule): rule broken: int arithmetic wraps without warning. Kind: silent logic error. Trigger class: \`for (int i = 0; i &lt;= Integer.MAX\_VALUE; i++)\`: i overflows to a negative value, so the test is never false.
- **diagnose an error** (error rule): rule broken: Code after a loop that can never complete normally is unreachable. Kind: compile-time. Trigger class: Statements after \`while (true) { ... }\` with no break (unreachable statement).

## Same topic

`infinite_loop` belongs to the topic **Infinite loops** (`topic1.3.h`). It is the only concept of that topic.

## Rules of the concept (20)

- **folk-meaning rule:** Folk meaning: in everyday instructions ('lather, rinse, repeat', 'while the road is two lanes, continue north') the reader stops sensibly or watches the condition all the time. A Java loop repeats only while its condition is true at each test, and it never stops on its own if no pass makes the condition false.
- **wrong rule / right rule:** CompoundAssignmentNoCast: wrong: \`x += 0.5\` adds one half to an int x. \| right: \`x += 0.5\` means \`x = (int) (x + 0.5)\`; the narrowing rounds toward zero, so a nonnegative int x keeps its value, and a loop relying on it never progresses.
- **wrong rule / right rule:** InfiniteLoopUnnoticed: wrong: A loop whose condition never goes false will still terminate. \| right: A while loop stops only when its condition is false at a check, so if no pass changes the variables in the condition, it never stops.
- **wrong rule / right rule:** JavaDetectsInfiniteLoops: wrong: If my loop never ends, the compiler or Java will warn me. \| right: Java cannot detect infinite loops in general (the halting problem); you must check that the condition eventually becomes false.
- **wrong rule / right rule:** LoopVariableNotUpdated: wrong: A while loop ends by itself even if nothing in the body changes the variable tested in the condition. \| right: If no statement in the body changes a variable in the condition, a condition that was true stays true and the loop never ends.
- **uneven-application rule:** Applies the loop LT rule unevenly: on a trace, the update is assumed to happen on every pass even when it is skipped (e.g. by continue or inside an if), or the loop is assumed to stop when the condition becomes false in the middle of the body. The traced run then ends where the real one does not.
- **identity rule:** Loop bug/behaviour: a loop whose continuation condition never becomes false, so it runs until the program is killed (or overflow intervenes).
- **declarative rule:** A while or for loop terminates only if some pass makes its condition false at a test (or a break or return runs). Otherwise it repeats forever. The compiler does not check this.
- **operational sequencing rule:** The same order as any loop: test, body, test... In an infinite loop the update either never runs or never moves the tested variables towards false, so every test yields true.
- **evaluation / result rule:** There is no final value. Either output scrolls forever (BadHellos with \`i &gt; 3\`) or nothing happens and the program 'hangs'. Over a very long run, int overflow may eventually make the test false (BadHellos stops after about 2^31 lines).
- **state-transition rule:** Each pass leaves the condition's variables either unchanged or moving away from false (i grows while the test is \`i &gt; 3\`). So the state after the pass satisfies the condition again.
- **composition rule (with a neighbour):** with loop\_control: A loop is finite only if its update moves the control variable towards making the condition false. Wrong direction (\`i--\` with \`i &lt; n\`), wrong step (\`i += 0\` or \`x += 0.5\` on an int), or a condition that the update can step over (\`i != 10\` with \`i += 3\`) all give infinite loops.
- **plan / role rule:** Purpose: usually a bug. An intentional \`while (true)\` with an internal break or return is the 'loop-and-a-half' plan for servers, event loops and read-until-sentinel input.
- **conservation rule:** Changing the condition or update can turn a terminating loop into an infinite one (\`i &lt;= 10\` to \`i &gt; 3\`), or the reverse. The termination argument (a quantity that strictly moves towards the bound on every pass) must survive any change.
- **error rule:** rule broken: The body must change a variable in the condition so that it eventually becomes false. (silent logic error)
- **error rule:** rule broken: An empty statement after the loop header becomes the body. (silent logic error)
- **error rule:** rule broken: Tests on doubles or on exact values can be stepped over. (silent logic error)
- **error rule:** rule broken: int arithmetic wraps without warning. (silent logic error)
- **error rule:** rule broken: Code after a loop that can never complete normally is unreachable. (compile-time)
- **applicability rule:** Write \`while (true)\` only when the exit is in the middle of the body and is certain (break or return on a sentinel or event). Otherwise, for each loop, state why the condition eventually becomes false. When a program seems stuck, add trace prints to tell an infinite loop from a slow one.

## The whole prerequisite chain

- **Everything it builds on (16):** `arithmetic_operators`, `boolean`, `boolean_expression`, `comparison_operators`, `data_type`, `do_while_loop`, `expression`, `for_loop`, `identifier`, `literal`, `logical_operators`, `loop_control`, `loop_variable`, `primitive_type`, `variable`, `while_loop`
- **Everything that builds on it (0):** nothing
