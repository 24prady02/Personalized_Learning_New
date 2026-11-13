# Loop test as a guard (`loop_guard`)

putting the bounds check in the loop condition so the body never makes an out-of-bounds array access

Section 1.4 1.4 Arrays, topic 1.4.b Memory representation and bounds checking.

![The knowledge graph around loop_guard](loop_guard.png)

## At a glance

- **Needs first:** `array_bounds`
- **Leads to:** nothing
- **Learned alongside:** nothing
- **Misconceptions:** `BodyChangeIgnoredByCondition`, `LessGreaterSwapped`, `LoopConditionValidatedLater`, `LoopCountByIntent`, `LoopVariableNotUpdated`
- **Errors:** none
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 25 edges around this concept. The edge logic, the wrong and right rules and the exact rules of the ways are copied word for word from the graph.

## To work on (0)

Nothing is missing for this concept.

## What it needs first (1)

A prerequisite edge means the other concept has to be understood before `loop_guard`.

### `array_bounds` comes before `loop_guard`

*valid indices are 0 .. length-1; otherwise throws*

- **Edge:** `pre:array_bounds->loop_guard`
- **Exact edge logic:** Because an out-of-bounds index stops the program, the while test checks the bounds before the body uses the index.
- **Grounding:** book\_passage
- **Composition rule (R) of `loop_guard` with `array_bounds`:** Because an out-of-bounds index stops the program, the guard tests the bounds before the body uses the index, and it must cover every neighbour index (x-1, x+1) the body reads.
- **Composition rule (R) of `array_bounds` with `loop_guard`:** Because an out-of-bounds index stops the program, the loop test checks the bounds before the body uses the index (e.g. x &gt; 0 &amp;&amp; x &lt; N-1 before a[x-1], a[x+1]).

## What it leads to (0)

These concepts need `loop_guard` first.

No concept has this one as a prerequisite.

## Learned alongside (0)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

No parallel edge touches this concept.

## Misconceptions (5)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### BodyChangeIgnoredByCondition

- **Edge:** `loop_guard` &rarr; `BodyChangeIgnoredByCondition` (misconception)
- **Exact edge logic (the wrong rule):** Changing the loop variable inside the body does not affect the loop condition; the loop still runs its planned number of times.
- **Twin logic (the right rule):** The condition is tested with the current value of the variable, including changes made in the body.
- **Wrong belief (on the node):** Changing the loop variable inside the body does not affect the loop condition; the loop still runs its planned number of times.
- **Correct rule (on the node):** The condition is tested with the current value of the variable, including changes made in the body.
- **Provenance:** published
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [3] misconception, exact rule:** wrong rule: Changing the loop variable inside the body does not affect the loop condition; the loop still runs its planned number of times. Right rule: The condition is tested with the current value of the variable, including changes made in the body.
- **Edge `loop_variable` &rarr; `BodyChangeIgnoredByCondition`, exact edge logic:** Changing the loop variable inside the body does not affect the loop condition; the loop still runs its planned number of times. **Twin logic:** The condition is tested with the current value of the variable, including changes made in the body. (role: primary)

### LessGreaterSwapped

- **Edge:** `loop_guard` &rarr; `LessGreaterSwapped` (misconception)
- **Exact edge logic (the wrong rule):** &lt; and &gt; mean the same thing (or a &lt; b means a is greater than b).
- **Twin logic (the right rule):** a &lt; b is true when a is smaller than b; a &gt; b when a is larger.
- **Wrong belief (on the node):** &lt; and &gt; mean the same thing (or a &lt; b means a is greater than b).
- **Correct rule (on the node):** a &lt; b is true when a is smaller than b; a &gt; b when a is larger.
- **Provenance:** published
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [6] misconception, exact rule:** wrong rule: &lt; and &gt; mean the same thing (or a &lt; b means a is greater than b). Right rule: a &lt; b is true when a is smaller than b; a &gt; b when a is larger.
- **Edge `comparison_operators` &rarr; `LessGreaterSwapped`, exact edge logic:** &lt; and &gt; mean the same thing (or a &lt; b means a is greater than b). **Twin logic:** a &lt; b is true when a is smaller than b; a &gt; b when a is larger. (role: primary)

### LoopConditionValidatedLater

- **Edge:** `loop_guard` &rarr; `LoopConditionValidatedLater` (misconception)
- **Exact edge logic (the wrong rule):** If a loop condition is false at first but would become true later, the loop still runs (it repeats or skips until the condition is true, then runs until it is false).
- **Twin logic (the right rule):** A while loop whose condition is false at the first test runs zero times; nothing later revives it.
- **Wrong belief (on the node):** If a loop condition is false at first but would become true later, the loop still runs (it repeats or skips until the condition is true, then runs until it is false).
- **Correct rule (on the node):** A while loop whose condition is false at the first test runs zero times; nothing later revives it.
- **Provenance:** published
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [5] misconception, exact rule:** wrong rule: If a loop condition is false at first but would become true later, the loop still runs. Right rule: A while loop whose condition is false at the first test runs zero times; nothing later revives it.
- **Edge `while_loop` &rarr; `LoopConditionValidatedLater`, exact edge logic:** If a loop condition is false at first but would become true later, the loop still runs (it repeats or skips until the condition is true, then runs until it is false). **Twin logic:** A while loop whose condition is false at the first test runs zero times; nothing later revives it. (role: primary)

### LoopCountByIntent

- **Edge:** `loop_guard` &rarr; `LoopCountByIntent` (misconception)
- **Exact edge logic (the wrong rule):** How many times a loop runs is decided by what the program is meant to do, so it may go on after its condition is false.
- **Twin logic (the right rule):** The loop runs only while its condition is true when tested; it stops at the first false test.
- **Wrong belief (on the node):** How many times a loop runs is decided by what the program is meant to do, so it may go on after its condition is false.
- **Correct rule (on the node):** The loop runs only while its condition is true when tested; it stops at the first false test.
- **Provenance:** published
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [4] misconception, exact rule:** wrong rule: How many times a loop runs is decided by what the program is meant to do, so it may go on after its condition is false. Right rule: The loop runs only while its condition is true when tested; it stops at the first false test.
- **Edge `while_loop` &rarr; `LoopCountByIntent`, exact edge logic:** How many times a loop runs is decided by what the program is meant to do, so it may go on after its condition is false. **Twin logic:** The loop runs only while its condition is true when tested; it stops at the first false test. (role: primary)

### LoopVariableNotUpdated

- **Edge:** `loop_guard` &rarr; `LoopVariableNotUpdated` (misconception)
- **Exact edge logic (the wrong rule):** A while loop ends by itself even if nothing in the body changes the variable tested in the condition.
- **Twin logic (the right rule):** If no statement in the body changes a variable in the condition, a condition that was true stays true and the loop never ends.
- **Wrong belief (on the node):** A while loop ends by itself even if nothing in the body changes the variable tested in the condition.
- **Correct rule (on the node):** If no statement in the body changes a variable in the condition, a condition that was true stays true and the loop never ends.
- **Provenance:** published
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [1] misconception, exact rule:** wrong rule: A while loop ends by itself even if nothing in the body changes the variable tested in the condition. Right rule: If no statement in the body changes a variable in the condition, a condition that was true stays true and the loop never ends.
- **L0 way [2] inconsistent\_trace, exact rule:** Points to LT: the guard is tested before every pass, and the body runs only if it is true. Inconsistent application: the trace applies the bounds test only at the first pass, or after the body has already used the out-of-range index. (here mixing in: "A while loop ends by itself even if nothing in the body changes the variable tested in the condition")
- **Edge `infinite_loop` &rarr; `LoopVariableNotUpdated`, exact edge logic:** A while loop ends by itself even if nothing in the body changes the variable tested in the condition. **Twin logic:** If no statement in the body changes a variable in the condition, a condition that was true stays true and the loop never ends. (role: context)
- **Edge `while_loop` &rarr; `LoopVariableNotUpdated`, exact edge logic:** A while loop ends by itself even if nothing in the body changes the variable tested in the condition. **Twin logic:** If no statement in the body changes a variable in the condition, a condition that was true stays true and the loop never ends. (role: context)

## Errors (0)

An error edge states the rule that gets broken in a program, and the right rule.

The graph has no error edge from this concept.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for Loop test as a guard: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to Loop test as a guard agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

- **Edge:** `loop_guard` &rarr; `loop_guard@L0` (has_level)
- **Exact edge logic:** Loop test as a guard -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (7 ways).

Ways (7), each with its exact rule:

- **[0] everyday\_reading** (rule type E, folk-meaning rule): Folk meaning: in English, 'while the dog is in the city, keep walking' is monitored continuously, so the walk stops the instant it leaves. Java rule: the while condition is tested only before each pass, so the guard must make every index used in the body legal at that moment.
- **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `LoopVariableNotUpdated`: wrong rule: A while loop ends by itself even if nothing in the body changes the variable tested in the condition. Right rule: If no statement in the body changes a variable in the condition, a condition that was true stays true and the loop never ends.
- **[2] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `LoopVariableNotUpdated`: Points to LT: the guard is tested before every pass, and the body runs only if it is true. Inconsistent application: the trace applies the bounds test only at the first pass, or after the body has already used the out-of-range index. (here mixing in: "A while loop ends by itself even if nothing in the body changes the variable tested in the condition")
- **[3] misconception** (rule type M, wrong rule / right rule) &rarr; `BodyChangeIgnoredByCondition`: wrong rule: Changing the loop variable inside the body does not affect the loop condition; the loop still runs its planned number of times. Right rule: The condition is tested with the current value of the variable, including changes made in the body.
- **[4] misconception** (rule type M, wrong rule / right rule) &rarr; `LoopCountByIntent`: wrong rule: How many times a loop runs is decided by what the program is meant to do, so it may go on after its condition is false. Right rule: The loop runs only while its condition is true when tested; it stops at the first false test.
- **[5] misconception** (rule type M, wrong rule / right rule) &rarr; `LoopConditionValidatedLater`: wrong rule: If a loop condition is false at first but would become true later, the loop still runs. Right rule: A while loop whose condition is false at the first test runs zero times; nothing later revives it.
- **[6] misconception** (rule type M, wrong rule / right rule) &rarr; `LessGreaterSwapped`: wrong rule: &lt; and &gt; mean the same thing (or a &lt; b means a is greater than b). Right rule: a &lt; b is true when a is smaller than b; a &gt; b when a is larger.

### L1: Unistructural / atom x text surface

L1 for Loop test as a guard: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

- **Edge:** `loop_guard` &rarr; `loop_guard@L1` (has_level)
- **Exact edge logic:** Loop test as a guard -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

Ways (2), each with its exact rule:

- **[0] names\_the\_element** (rule type N, identity rule): Identity: a loop guard is a loop-continuation test that also guards the body against an illegal statement, typically an out-of-bounds array access.
- **[1] states\_the\_rule** (rule type S, declarative rule): Declarative: code the loop exit test so that whenever the body runs, all indices it uses are legal, e.g. while (x &gt; 0 &amp;&amp; x &lt; N-1 &amp;&amp; y &gt; 0 &amp;&amp; y &lt; N-1) before reading a[x-1][y], a[x+1][y], ...

### L2: Multistructural / block x execution / preoperational

L2 for Loop test as a guard: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

- **Edge:** `loop_guard` &rarr; `loop_guard@L2` (has_level)
- **Exact edge logic:** Loop test as a guard -&gt; L2 (Multistructural): the answer applies the rules of Loop test as a guard to every part of the code, in order (3 ways).

Ways (3), each with its exact rule:

- **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): Sequencing: before each pass the guard is evaluated left to right, and &amp;&amp; stops at the first false operand; the body runs only if the whole guard is true; after the body the guard is tested again with the updated values.
- **[1] output\_prediction** (rule type OP, evaluation / result rule): Result: the loop ends normally, with no exception, when an index reaches the boundary; in SelfAvoidingWalk that means the dog has escaped.
- **[2] one\_step\_execution** (rule type OS, state-transition rule): State transition: one guard evaluation changes no variable; it either admits one more pass with legal indices or ends the loop.

### L3: Relational / relations x function (concrete operational begins)

L3 for Loop test as a guard: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

- **Edge:** `loop_guard` &rarr; `loop_guard@L3` (has_level)
- **Exact edge logic:** Loop test as a guard -&gt; L3 (Relational): the answer relates the parts (2 ways).

Ways (2), each with its exact rule:

- **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Because an out-of-bounds index stops the program, the guard tests the bounds before the body uses the index, and it must cover every neighbour index (x-1, x+1) the body reads.
- **[1] purpose\_of\_the\_whole** (rule type P, plan / role rule): Plan/role: the guard-before-use plan. A single test both terminates the loop (event: reached the edge) and protects every array access in the body.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for Loop test as a guard: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

- **Edge:** `loop_guard` &rarr; `loop_guard@L4` (has_level)
- **Exact edge logic:** Loop test as a guard -&gt; L4 (Extended abstract): the answer reasons beyond the given code (5 ways).

Ways (5), each with its exact rule:

- **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `LoopVariableNotUpdated`: Conservation: inside the body the guard's invariant holds (0 &lt; x &lt; N-1, so x-1 and x+1 are legal indices). Weakening the guard (x &gt;= 0) or putting the array test before the bounds test in &amp;&amp; breaks it.
- **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Applicability: use a guarded while loop when iteration continues until a data-dependent event and the body indexes an array with a moving position (walks, searches). For a full traversal, a for loop with i &lt; a.length is the simpler guard.
- **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: The guard must make every index in the body legal. Kind: run-time exception. Trigger class: the guard is missing, too weak (x &gt;= 0 &amp;&amp; x &lt; N while the body reads a[x+1]), or ordered wrongly (a[i] != 0 &amp;&amp; i &lt; n) so the access happens before the bounds test (ArrayIndexOutOfBoundsException)
- **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: The body must change a variable in the guard. Kind: silent logic error. Trigger class: no statement in the body updates the guarded index, so the loop never ends (infinite loop)
- **[4] diagnose\_an\_error** (rule type D, error rule): rule broken: The relational operators must express the intended bound. Kind: silent logic error. Trigger class: &lt; and &gt; (or &lt; and &lt;=) are swapped, so the loop runs zero times or one pass too many

## Same topic

`loop_guard` belongs to the topic **Memory representation and bounds checking** (`topic1.4.b`). The topic also contains: `array_aliasing`, `array_bounds`, `array_copy`, `array_reference`, `primitive_vs_reference`, `printing_array_reference`, `program_state`.

## Rules of the concept (19)

- **Book** (SW-1e, p. 108 (pdf 118)): "we code the loop exit test in the while statement as a guard against an illegal statement in the body of the loop"
- **E** (folk-meaning rule): Folk meaning: in English, 'while the dog is in the city, keep walking' is monitored continuously, so the walk stops the instant it leaves. Java rule: the while condition is tested only before each pass, so the guard must make every index used in the body legal at that moment.
- **M** (wrong rule / right rule): BodyChangeIgnoredByCondition: wrong: Changing the loop variable inside the body does not affect the loop condition; the loop still runs its planned number of times. \| right: The condition is tested with the current value of the variable, including changes made in the body.
- **M** (wrong rule / right rule): LoopCountByIntent: wrong: How many times a loop runs is decided by what the program is meant to do, so it may go on after its condition is false. \| right: The loop runs only while its condition is true when tested; it stops at the first false test.
- **M** (wrong rule / right rule): LoopConditionValidatedLater: wrong: If a loop condition is false at first but would become true later, the loop still runs. \| right: A while loop whose condition is false at the first test runs zero times; nothing later revives it.
- **M** (wrong rule / right rule): LessGreaterSwapped: wrong: &lt; and &gt; mean the same thing (or a &lt; b means a is greater than b). \| right: a &lt; b is true when a is smaller than b; a &gt; b when a is larger.
- **M** (wrong rule / right rule): LoopVariableNotUpdated: wrong: A while loop ends by itself even if nothing in the body changes the variable tested in the condition. \| right: If no statement in the body changes a variable in the condition, a condition that was true stays true and the loop never ends.
- **T** (uneven-application rule): Points to LT: the guard is tested before every pass, and the body runs only if it is true. Inconsistent application: the trace applies the bounds test only at the first pass, or after the body has already used the out-of-range index.
- **N** (identity rule): Identity: a loop guard is a loop-continuation test that also guards the body against an illegal statement, typically an out-of-bounds array access.
- **S** (declarative rule): Declarative: code the loop exit test so that whenever the body runs, all indices it uses are legal, e.g. while (x &gt; 0 &amp;&amp; x &lt; N-1 &amp;&amp; y &gt; 0 &amp;&amp; y &lt; N-1) before reading a[x-1][y], a[x+1][y], ...
- **LT** (operational sequencing rule): Sequencing: before each pass the guard is evaluated left to right, and &amp;&amp; stops at the first false operand; the body runs only if the whole guard is true; after the body the guard is tested again with the updated values.
- **OP** (evaluation / result rule): Result: the loop ends normally, with no exception, when an index reaches the boundary; in SelfAvoidingWalk that means the dog has escaped.
- **OS** (state-transition rule): State transition: one guard evaluation changes no variable; it either admits one more pass with legal indices or ends the loop.
- **R** (composition rule (with a neighbour)): with array\_bounds: Because an out-of-bounds index stops the program, the guard tests the bounds before the body uses the index, and it must cover every neighbour index (x-1, x+1) the body reads.
- **P** (plan / role rule): Plan/role: the guard-before-use plan. A single test both terminates the loop (event: reached the edge) and protects every array access in the body.
- **C** (conservation rule): Conservation: inside the body the guard's invariant holds (0 &lt; x &lt; N-1, so x-1 and x+1 are legal indices). Weakening the guard (x &gt;= 0) or putting the array test before the bounds test in &amp;&amp; breaks it.
- **D** (error rule): rule broken: The guard must make every index in the body legal. (run-time exception)
- **D** (error rule): rule broken: The body must change a variable in the guard. (silent logic error)
- **D** (error rule): rule broken: The relational operators must express the intended bound. (silent logic error)
- **X** (applicability rule): Applicability: use a guarded while loop when iteration continues until a data-dependent event and the body indexes an array with a moving position (walks, searches). For a full traversal, a for loop with i &lt; a.length is the simpler guard.

## How it is found in code and answers (reader block)

- **Aliases:** loop condition, guard, loop test
- **Code patterns:** `\w+\s*<\s*\w+\.length\s*&&`, `&&\s*\w+\s*<\s*\w+\.length`, `\b\w+\s*(?:<\s*\w+(?:\.length)?|>=\s*0)\s*&&\s*[^;]*\w\s*\[`
- **Operator symbols:** none
- **Java types:** none

## The whole prerequisite chain

- **Everything it builds on (7):** `array_bounds`, `array_creation`, `array_declaration`, `array_initializer`, `data_structure`, `data_type`, `indexing`
- **Everything that builds on it (0):** nothing

## Every edge in this view and its exact edge logic (25)

All the edges drawn in the picture, in the order: prerequisite, parallel, misconception, error, has_level, contains.

**1. `array_bounds` &rarr; `loop_guard`** (prerequisite)

- **Exact edge logic:** Because an out-of-bounds index stops the program, the while test checks the bounds before the body uses the index.
- **Grounding:** book\_passage
- **Composition rule (R) of `array_bounds` with `loop_guard`:** Because an out-of-bounds index stops the program, the loop test checks the bounds before the body uses the index (e.g. x &gt; 0 &amp;&amp; x &lt; N-1 before a[x-1], a[x+1]).
- **Composition rule (R) of `loop_guard` with `array_bounds`:** Because an out-of-bounds index stops the program, the guard tests the bounds before the body uses the index, and it must cover every neighbour index (x-1, x+1) the body reads.

**2. `loop_guard` &rarr; `BodyChangeIgnoredByCondition`** (misconception)

- **Exact edge logic (the wrong rule):** Changing the loop variable inside the body does not affect the loop condition; the loop still runs its planned number of times.
- **Twin logic (the right rule):** The condition is tested with the current value of the variable, including changes made in the body.
- **Role:** context

**3. `loop_guard` &rarr; `LessGreaterSwapped`** (misconception)

- **Exact edge logic (the wrong rule):** &lt; and &gt; mean the same thing (or a &lt; b means a is greater than b).
- **Twin logic (the right rule):** a &lt; b is true when a is smaller than b; a &gt; b when a is larger.
- **Role:** context

**4. `loop_guard` &rarr; `LoopConditionValidatedLater`** (misconception)

- **Exact edge logic (the wrong rule):** If a loop condition is false at first but would become true later, the loop still runs (it repeats or skips until the condition is true, then runs until it is false).
- **Twin logic (the right rule):** A while loop whose condition is false at the first test runs zero times; nothing later revives it.
- **Role:** context

**5. `loop_guard` &rarr; `LoopCountByIntent`** (misconception)

- **Exact edge logic (the wrong rule):** How many times a loop runs is decided by what the program is meant to do, so it may go on after its condition is false.
- **Twin logic (the right rule):** The loop runs only while its condition is true when tested; it stops at the first false test.
- **Role:** context

**6. `loop_guard` &rarr; `LoopVariableNotUpdated`** (misconception)

- **Exact edge logic (the wrong rule):** A while loop ends by itself even if nothing in the body changes the variable tested in the condition.
- **Twin logic (the right rule):** If no statement in the body changes a variable in the condition, a condition that was true stays true and the loop never ends.
- **Role:** primary

**7. `comparison_operators` &rarr; `LessGreaterSwapped`** (misconception)

- **Exact edge logic (the wrong rule):** &lt; and &gt; mean the same thing (or a &lt; b means a is greater than b).
- **Twin logic (the right rule):** a &lt; b is true when a is smaller than b; a &gt; b when a is larger.
- **Role:** primary

**8. `infinite_loop` &rarr; `LoopVariableNotUpdated`** (misconception)

- **Exact edge logic (the wrong rule):** A while loop ends by itself even if nothing in the body changes the variable tested in the condition.
- **Twin logic (the right rule):** If no statement in the body changes a variable in the condition, a condition that was true stays true and the loop never ends.
- **Role:** context

**9. `loop_variable` &rarr; `BodyChangeIgnoredByCondition`** (misconception)

- **Exact edge logic (the wrong rule):** Changing the loop variable inside the body does not affect the loop condition; the loop still runs its planned number of times.
- **Twin logic (the right rule):** The condition is tested with the current value of the variable, including changes made in the body.
- **Role:** primary

**10. `while_loop` &rarr; `LoopConditionValidatedLater`** (misconception)

- **Exact edge logic (the wrong rule):** If a loop condition is false at first but would become true later, the loop still runs (it repeats or skips until the condition is true, then runs until it is false).
- **Twin logic (the right rule):** A while loop whose condition is false at the first test runs zero times; nothing later revives it.
- **Role:** primary

**11. `while_loop` &rarr; `LoopCountByIntent`** (misconception)

- **Exact edge logic (the wrong rule):** How many times a loop runs is decided by what the program is meant to do, so it may go on after its condition is false.
- **Twin logic (the right rule):** The loop runs only while its condition is true when tested; it stops at the first false test.
- **Role:** primary

**12. `while_loop` &rarr; `LoopVariableNotUpdated`** (misconception)

- **Exact edge logic (the wrong rule):** A while loop ends by itself even if nothing in the body changes the variable tested in the condition.
- **Twin logic (the right rule):** If no statement in the body changes a variable in the condition, a condition that was true stays true and the loop never ends.
- **Role:** context

**13. `loop_guard` &rarr; `loop_guard@L0`** (has_level)

- **Exact edge logic:** Loop test as a guard -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (7 ways).
  - **[0] everyday\_reading** (rule type E, folk-meaning rule): Folk meaning: in English, 'while the dog is in the city, keep walking' is monitored continuously, so the walk stops the instant it leaves. Java rule: the while condition is tested only before each pass, so the guard must make every index used in the body legal at that moment.
  - **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `LoopVariableNotUpdated`: wrong rule: A while loop ends by itself even if nothing in the body changes the variable tested in the condition. Right rule: If no statement in the body changes a variable in the condition, a condition that was true stays true and the loop never ends.
  - **[2] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `LoopVariableNotUpdated`: Points to LT: the guard is tested before every pass, and the body runs only if it is true. Inconsistent application: the trace applies the bounds test only at the first pass, or after the body has already used the out-of-range index. (here mixing in: "A while loop ends by itself even if nothing in the body changes the variable tested in the condition")
  - **[3] misconception** (rule type M, wrong rule / right rule) &rarr; `BodyChangeIgnoredByCondition`: wrong rule: Changing the loop variable inside the body does not affect the loop condition; the loop still runs its planned number of times. Right rule: The condition is tested with the current value of the variable, including changes made in the body.
  - **[4] misconception** (rule type M, wrong rule / right rule) &rarr; `LoopCountByIntent`: wrong rule: How many times a loop runs is decided by what the program is meant to do, so it may go on after its condition is false. Right rule: The loop runs only while its condition is true when tested; it stops at the first false test.
  - **[5] misconception** (rule type M, wrong rule / right rule) &rarr; `LoopConditionValidatedLater`: wrong rule: If a loop condition is false at first but would become true later, the loop still runs. Right rule: A while loop whose condition is false at the first test runs zero times; nothing later revives it.
  - **[6] misconception** (rule type M, wrong rule / right rule) &rarr; `LessGreaterSwapped`: wrong rule: &lt; and &gt; mean the same thing (or a &lt; b means a is greater than b). Right rule: a &lt; b is true when a is smaller than b; a &gt; b when a is larger.

**14. `loop_guard` &rarr; `loop_guard@L1`** (has_level)

- **Exact edge logic:** Loop test as a guard -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).
  - **[0] names\_the\_element** (rule type N, identity rule): Identity: a loop guard is a loop-continuation test that also guards the body against an illegal statement, typically an out-of-bounds array access.
  - **[1] states\_the\_rule** (rule type S, declarative rule): Declarative: code the loop exit test so that whenever the body runs, all indices it uses are legal, e.g. while (x &gt; 0 &amp;&amp; x &lt; N-1 &amp;&amp; y &gt; 0 &amp;&amp; y &lt; N-1) before reading a[x-1][y], a[x+1][y], ...

**15. `loop_guard` &rarr; `loop_guard@L2`** (has_level)

- **Exact edge logic:** Loop test as a guard -&gt; L2 (Multistructural): the answer applies the rules of Loop test as a guard to every part of the code, in order (3 ways).
  - **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): Sequencing: before each pass the guard is evaluated left to right, and &amp;&amp; stops at the first false operand; the body runs only if the whole guard is true; after the body the guard is tested again with the updated values.
  - **[1] output\_prediction** (rule type OP, evaluation / result rule): Result: the loop ends normally, with no exception, when an index reaches the boundary; in SelfAvoidingWalk that means the dog has escaped.
  - **[2] one\_step\_execution** (rule type OS, state-transition rule): State transition: one guard evaluation changes no variable; it either admits one more pass with legal indices or ends the loop.

**16. `loop_guard` &rarr; `loop_guard@L3`** (has_level)

- **Exact edge logic:** Loop test as a guard -&gt; L3 (Relational): the answer relates the parts (2 ways).
  - **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Because an out-of-bounds index stops the program, the guard tests the bounds before the body uses the index, and it must cover every neighbour index (x-1, x+1) the body reads.
  - **[1] purpose\_of\_the\_whole** (rule type P, plan / role rule): Plan/role: the guard-before-use plan. A single test both terminates the loop (event: reached the edge) and protects every array access in the body.

**17. `loop_guard` &rarr; `loop_guard@L4`** (has_level)

- **Exact edge logic:** Loop test as a guard -&gt; L4 (Extended abstract): the answer reasons beyond the given code (5 ways).
  - **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `LoopVariableNotUpdated`: Conservation: inside the body the guard's invariant holds (0 &lt; x &lt; N-1, so x-1 and x+1 are legal indices). Weakening the guard (x &gt;= 0) or putting the array test before the bounds test in &amp;&amp; breaks it.
  - **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Applicability: use a guarded while loop when iteration continues until a data-dependent event and the body indexes an array with a moving position (walks, searches). For a full traversal, a for loop with i &lt; a.length is the simpler guard.
  - **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: The guard must make every index in the body legal. Kind: run-time exception. Trigger class: the guard is missing, too weak (x &gt;= 0 &amp;&amp; x &lt; N while the body reads a[x+1]), or ordered wrongly (a[i] != 0 &amp;&amp; i &lt; n) so the access happens before the bounds test (ArrayIndexOutOfBoundsException)
  - **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: The body must change a variable in the guard. Kind: silent logic error. Trigger class: no statement in the body updates the guarded index, so the loop never ends (infinite loop)
  - **[4] diagnose\_an\_error** (rule type D, error rule): rule broken: The relational operators must express the intended bound. Kind: silent logic error. Trigger class: &lt; and &gt; (or &lt; and &lt;=) are swapped, so the loop runs zero times or one pass too many

**18. `topic1.4.b` &rarr; `loop_guard`** (contains)

- topic `topic1.4.b` contains `loop_guard`

**19. `topic1.4.b` &rarr; `array_aliasing`** (contains)

- topic `topic1.4.b` contains `array_aliasing`

**20. `topic1.4.b` &rarr; `array_bounds`** (contains)

- topic `topic1.4.b` contains `array_bounds`

**21. `topic1.4.b` &rarr; `array_copy`** (contains)

- topic `topic1.4.b` contains `array_copy`

**22. `topic1.4.b` &rarr; `array_reference`** (contains)

- topic `topic1.4.b` contains `array_reference`

**23. `topic1.4.b` &rarr; `primitive_vs_reference`** (contains)

- topic `topic1.4.b` contains `primitive_vs_reference`

**24. `topic1.4.b` &rarr; `printing_array_reference`** (contains)

- topic `topic1.4.b` contains `printing_array_reference`

**25. `topic1.4.b` &rarr; `program_state`** (contains)

- topic `topic1.4.b` contains `program_state`
