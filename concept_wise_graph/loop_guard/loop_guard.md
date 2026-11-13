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

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 25 edges around this concept, each explained in the graph's own words.

## What it needs first (1)

A prerequisite edge means the other concept has to be understood before `loop_guard`.

### `array_bounds` comes before `loop_guard`

*valid indices are 0 .. length-1; otherwise throws*

Because an out-of-bounds index stops the program, the while test checks the bounds before the body uses the index.

- **Grounding:** book passage
- **How `loop_guard` combines with `array_bounds`:** Because an out-of-bounds index stops the program, the guard tests the bounds before the body uses the index, and it must cover every neighbour index (x-1, x+1) the body reads.
- **How `array_bounds` combines with `loop_guard`:** Because an out-of-bounds index stops the program, the loop test checks the bounds before the body uses the index (e.g. x &gt; 0 &amp;&amp; x &lt; N-1 before a[x-1], a[x+1]).

## What it leads to (0)

These concepts need `loop_guard` first.

No concept has this one as a prerequisite.

## Learned alongside (0)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

No parallel edge touches this concept.

## Misconceptions (5)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### BodyChangeIgnoredByCondition

- **Wrong rule:** Changing the loop variable inside the body does not affect the loop condition; the loop still runs its planned number of times.
- **Right rule:** The condition is tested with the current value of the variable, including changes made in the body.
- **Role of this concept:** context
- **Shows at level L0 as:** misconception: wrong rule: Changing the loop variable inside the body does not affect the loop condition; the loop still runs its planned number of times. Right rule: The condition is tested with the current value of the variable, including changes made in the body.
- **Also an edge from `loop_variable`:** Changing the loop variable inside the body does not affect the loop condition; the loop still runs its planned number of times.

### LessGreaterSwapped

- **Wrong rule:** &lt; and &gt; mean the same thing (or a &lt; b means a is greater than b).
- **Right rule:** a &lt; b is true when a is smaller than b; a &gt; b when a is larger.
- **Role of this concept:** context
- **Shows at level L0 as:** misconception: wrong rule: &lt; and &gt; mean the same thing (or a &lt; b means a is greater than b). Right rule: a &lt; b is true when a is smaller than b; a &gt; b when a is larger.
- **Also an edge from `comparison_operators`:** &lt; and &gt; mean the same thing (or a &lt; b means a is greater than b).

### LoopConditionValidatedLater

- **Wrong rule:** If a loop condition is false at first but would become true later, the loop still runs (it repeats or skips until the condition is true, then runs until it is false).
- **Right rule:** A while loop whose condition is false at the first test runs zero times; nothing later revives it.
- **Role of this concept:** context
- **Shows at level L0 as:** misconception: wrong rule: If a loop condition is false at first but would become true later, the loop still runs. Right rule: A while loop whose condition is false at the first test runs zero times; nothing later revives it.
- **Also an edge from `while_loop`:** If a loop condition is false at first but would become true later, the loop still runs (it repeats or skips until the condition is true, then runs until it is false).

### LoopCountByIntent

- **Wrong rule:** How many times a loop runs is decided by what the program is meant to do, so it may go on after its condition is false.
- **Right rule:** The loop runs only while its condition is true when tested; it stops at the first false test.
- **Role of this concept:** context
- **Shows at level L0 as:** misconception: wrong rule: How many times a loop runs is decided by what the program is meant to do, so it may go on after its condition is false. Right rule: The loop runs only while its condition is true when tested; it stops at the first false test.
- **Also an edge from `while_loop`:** How many times a loop runs is decided by what the program is meant to do, so it may go on after its condition is false.

### LoopVariableNotUpdated

- **Wrong rule:** A while loop ends by itself even if nothing in the body changes the variable tested in the condition.
- **Right rule:** If no statement in the body changes a variable in the condition, a condition that was true stays true and the loop never ends.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: A while loop ends by itself even if nothing in the body changes the variable tested in the condition. Right rule: If no statement in the body changes a variable in the condition, a condition that was true stays true and the loop never ends.
- **Shows at level L0 as:** inconsistent trace: Points to LT: the guard is tested before every pass, and the body runs only if it is true. Inconsistent application: the trace applies the bounds test only at the first pass, or after the body has already used the out-of-range index. (here mixing in: "A while loop ends by itself even if nothing in the body changes the variable tested in the condition")
- **Also an edge from `infinite_loop`:** A while loop ends by itself even if nothing in the body changes the variable tested in the condition.
- **Also an edge from `while_loop`:** A while loop ends by itself even if nothing in the body changes the variable tested in the condition.

## Errors (0)

An error edge states the rule that gets broken in a program, and the right rule.

The graph has no error edge from this concept.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for Loop test as a guard: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to Loop test as a guard agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

Loop test as a guard -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (7 ways).

- **everyday reading** (folk-meaning rule): Folk meaning: in English, 'while the dog is in the city, keep walking' is monitored continuously, so the walk stops the instant it leaves. Java rule: the while condition is tested only before each pass, so the guard must make every index used in the body legal at that moment.
- **misconception** (wrong rule / right rule; shows `LoopVariableNotUpdated`): wrong rule: A while loop ends by itself even if nothing in the body changes the variable tested in the condition. Right rule: If no statement in the body changes a variable in the condition, a condition that was true stays true and the loop never ends.
- **inconsistent trace** (uneven-application rule; shows `LoopVariableNotUpdated`): Points to LT: the guard is tested before every pass, and the body runs only if it is true. Inconsistent application: the trace applies the bounds test only at the first pass, or after the body has already used the out-of-range index. (here mixing in: "A while loop ends by itself even if nothing in the body changes the variable tested in the condition")
- **misconception** (wrong rule / right rule; shows `BodyChangeIgnoredByCondition`): wrong rule: Changing the loop variable inside the body does not affect the loop condition; the loop still runs its planned number of times. Right rule: The condition is tested with the current value of the variable, including changes made in the body.
- **misconception** (wrong rule / right rule; shows `LoopCountByIntent`): wrong rule: How many times a loop runs is decided by what the program is meant to do, so it may go on after its condition is false. Right rule: The loop runs only while its condition is true when tested; it stops at the first false test.
- **misconception** (wrong rule / right rule; shows `LoopConditionValidatedLater`): wrong rule: If a loop condition is false at first but would become true later, the loop still runs. Right rule: A while loop whose condition is false at the first test runs zero times; nothing later revives it.
- **misconception** (wrong rule / right rule; shows `LessGreaterSwapped`): wrong rule: &lt; and &gt; mean the same thing (or a &lt; b means a is greater than b). Right rule: a &lt; b is true when a is smaller than b; a &gt; b when a is larger.

### L1: Unistructural / atom x text surface

L1 for Loop test as a guard: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

Loop test as a guard -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

- **names the element** (identity rule): Identity: a loop guard is a loop-continuation test that also guards the body against an illegal statement, typically an out-of-bounds array access.
- **states the rule** (declarative rule): Declarative: code the loop exit test so that whenever the body runs, all indices it uses are legal, e.g. while (x &gt; 0 &amp;&amp; x &lt; N-1 &amp;&amp; y &gt; 0 &amp;&amp; y &lt; N-1) before reading a[x-1][y], a[x+1][y], ...

### L2: Multistructural / block x execution / preoperational

L2 for Loop test as a guard: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

Loop test as a guard -&gt; L2 (Multistructural): the answer applies the rules of Loop test as a guard to every part of the code, in order (3 ways).

- **line by line trace** (operational sequencing rule): Sequencing: before each pass the guard is evaluated left to right, and &amp;&amp; stops at the first false operand; the body runs only if the whole guard is true; after the body the guard is tested again with the updated values.
- **output prediction** (evaluation / result rule): Result: the loop ends normally, with no exception, when an index reaches the boundary; in SelfAvoidingWalk that means the dog has escaped.
- **one step execution** (state-transition rule): State transition: one guard evaluation changes no variable; it either admits one more pass with legal indices or ends the loop.

### L3: Relational / relations x function (concrete operational begins)

L3 for Loop test as a guard: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

Loop test as a guard -&gt; L3 (Relational): the answer relates the parts (2 ways).

- **relation to neighbour** (composition rule (with a neighbour)): Because an out-of-bounds index stops the program, the guard tests the bounds before the body uses the index, and it must cover every neighbour index (x-1, x+1) the body reads.
- **purpose of the whole** (plan / role rule): Plan/role: the guard-before-use plan. A single test both terminates the loop (event: reached the edge) and protects every array access in the body.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for Loop test as a guard: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

Loop test as a guard -&gt; L4 (Extended abstract): the answer reasons beyond the given code (5 ways).

- **predict a change** (conservation rule; shows `LoopVariableNotUpdated`): Conservation: inside the body the guard's invariant holds (0 &lt; x &lt; N-1, so x-1 and x+1 are legal indices). Weakening the guard (x &gt;= 0) or putting the array test before the bounds test in &amp;&amp; breaks it.
- **transfer to a new program** (applicability rule): Applicability: use a guarded while loop when iteration continues until a data-dependent event and the body indexes an array with a moving position (walks, searches). For a full traversal, a for loop with i &lt; a.length is the simpler guard.
- **diagnose an error** (error rule): rule broken: The guard must make every index in the body legal. Kind: run-time exception. Trigger class: the guard is missing, too weak (x &gt;= 0 &amp;&amp; x &lt; N while the body reads a[x+1]), or ordered wrongly (a[i] != 0 &amp;&amp; i &lt; n) so the access happens before the bounds test (ArrayIndexOutOfBoundsException)
- **diagnose an error** (error rule): rule broken: The body must change a variable in the guard. Kind: silent logic error. Trigger class: no statement in the body updates the guarded index, so the loop never ends (infinite loop)
- **diagnose an error** (error rule): rule broken: The relational operators must express the intended bound. Kind: silent logic error. Trigger class: &lt; and &gt; (or &lt; and &lt;=) are swapped, so the loop runs zero times or one pass too many

## Same topic

`loop_guard` belongs to the topic **Memory representation and bounds checking** (`topic1.4.b`). The topic also contains: `array_aliasing`, `array_bounds`, `array_copy`, `array_reference`, `primitive_vs_reference`, `printing_array_reference`, `program_state`.

## Rules of the concept (19)

- **folk-meaning rule:** Folk meaning: in English, 'while the dog is in the city, keep walking' is monitored continuously, so the walk stops the instant it leaves. Java rule: the while condition is tested only before each pass, so the guard must make every index used in the body legal at that moment.
- **wrong rule / right rule:** BodyChangeIgnoredByCondition: wrong: Changing the loop variable inside the body does not affect the loop condition; the loop still runs its planned number of times. \| right: The condition is tested with the current value of the variable, including changes made in the body.
- **wrong rule / right rule:** LoopCountByIntent: wrong: How many times a loop runs is decided by what the program is meant to do, so it may go on after its condition is false. \| right: The loop runs only while its condition is true when tested; it stops at the first false test.
- **wrong rule / right rule:** LoopConditionValidatedLater: wrong: If a loop condition is false at first but would become true later, the loop still runs. \| right: A while loop whose condition is false at the first test runs zero times; nothing later revives it.
- **wrong rule / right rule:** LessGreaterSwapped: wrong: &lt; and &gt; mean the same thing (or a &lt; b means a is greater than b). \| right: a &lt; b is true when a is smaller than b; a &gt; b when a is larger.
- **wrong rule / right rule:** LoopVariableNotUpdated: wrong: A while loop ends by itself even if nothing in the body changes the variable tested in the condition. \| right: If no statement in the body changes a variable in the condition, a condition that was true stays true and the loop never ends.
- **uneven-application rule:** Points to LT: the guard is tested before every pass, and the body runs only if it is true. Inconsistent application: the trace applies the bounds test only at the first pass, or after the body has already used the out-of-range index.
- **identity rule:** Identity: a loop guard is a loop-continuation test that also guards the body against an illegal statement, typically an out-of-bounds array access.
- **declarative rule:** Declarative: code the loop exit test so that whenever the body runs, all indices it uses are legal, e.g. while (x &gt; 0 &amp;&amp; x &lt; N-1 &amp;&amp; y &gt; 0 &amp;&amp; y &lt; N-1) before reading a[x-1][y], a[x+1][y], ...
- **operational sequencing rule:** Sequencing: before each pass the guard is evaluated left to right, and &amp;&amp; stops at the first false operand; the body runs only if the whole guard is true; after the body the guard is tested again with the updated values.
- **evaluation / result rule:** Result: the loop ends normally, with no exception, when an index reaches the boundary; in SelfAvoidingWalk that means the dog has escaped.
- **state-transition rule:** State transition: one guard evaluation changes no variable; it either admits one more pass with legal indices or ends the loop.
- **composition rule (with a neighbour):** with array\_bounds: Because an out-of-bounds index stops the program, the guard tests the bounds before the body uses the index, and it must cover every neighbour index (x-1, x+1) the body reads.
- **plan / role rule:** Plan/role: the guard-before-use plan. A single test both terminates the loop (event: reached the edge) and protects every array access in the body.
- **conservation rule:** Conservation: inside the body the guard's invariant holds (0 &lt; x &lt; N-1, so x-1 and x+1 are legal indices). Weakening the guard (x &gt;= 0) or putting the array test before the bounds test in &amp;&amp; breaks it.
- **error rule:** rule broken: The guard must make every index in the body legal. (run-time exception)
- **error rule:** rule broken: The body must change a variable in the guard. (silent logic error)
- **error rule:** rule broken: The relational operators must express the intended bound. (silent logic error)
- **applicability rule:** Applicability: use a guarded while loop when iteration continues until a data-dependent event and the body indexes an array with a moving position (walks, searches). For a full traversal, a for loop with i &lt; a.length is the simpler guard.

## The whole prerequisite chain

- **Everything it builds on (7):** `array_bounds`, `array_creation`, `array_declaration`, `array_initializer`, `data_structure`, `data_type`, `indexing`
- **Everything that builds on it (0):** nothing
