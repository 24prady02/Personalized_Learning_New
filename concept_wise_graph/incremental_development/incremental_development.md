# incremental_development (`incremental_development`)

building a program in small steps from a version that works, compiling and testing after each change

Section 1.1 Your First Program, topic 1.1.a Programming in Java: create, compile, execute.

![The knowledge graph around incremental_development](incremental_development.png)

## At a glance

- **Needs first:** `run`
- **Leads to:** `debugging`
- **Learned alongside:** nothing
- **Misconceptions:** `WriteAllThenTest`
- **Errors:** none
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 12 edges around this concept, each explained in the graph's own words.

## What it needs first (1)

A prerequisite edge means the other concept has to be understood before `incremental_development`.

### `run` comes before `incremental_development`

*java executes main in the JVM*

Each small step is run and checked before the next one is added.

- **Grounding:** book passage
- **How `incremental_development` combines with `run`:** Running after each step shows at once whether the new lines do what was intended.

## What it leads to (1)

These concepts need `incremental_development` first.

### `incremental_development` comes before `debugging`

*finding and fixing the cause of a wrong result or error by forming a hypothesis, changing the program and checking the prediction*

Developing in small steps keeps debugging local: an error is in the change just made.

- **Grounding:** book passage
- **How `incremental_development` combines with `debugging`:** Small steps make debugging local: the newest change is the first suspect.
- **How `debugging` combines with `incremental_development`:** Small steps keep debugging short: the error is in the change just made.

## Learned alongside (0)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

No parallel edge touches this concept.

## Misconceptions (1)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### WriteAllThenTest

- **Wrong rule:** Write the whole program first, then compile and test it all at the end.
- **Right rule:** Start with a working program and make small changes, compiling and testing after each one, so an error is always in the last change.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: Write the whole program first, then compile and test it all at the end. Right rule: Start with a working program and make small changes, compiling and testing after each one, so an error is always in the last change.
- **Shows at level L0 as:** inconsistent trace: Applies incremental development unevenly: tests the first few steps one at a time, then adds a large block of untested code at once. (here mixing in: "Write the whole program first, then compile and test it all at the end")

## Errors (0)

An error edge states the rule that gets broken in a program, and the right rule.

The graph has no error edge from this concept.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for incremental development: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to incremental development agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

incremental development -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (3 ways).

- **everyday reading** (folk-meaning rule): Everyday writing is drafted all at once and revised at the end. A program is grown in small steps from a version that already works, compiling and running after each step.
- **misconception** (wrong rule / right rule; shows `WriteAllThenTest`): wrong rule: Write the whole program first, then compile and test it all at the end. Right rule: Start with a working program and make small changes, compiling and testing after each one, so an error is always in the last change.
- **inconsistent trace** (uneven-application rule; shows `WriteAllThenTest`): Applies incremental development unevenly: tests the first few steps one at a time, then adds a large block of untested code at once. (here mixing in: "Write the whole program first, then compile and test it all at the end")

### L1: Unistructural / atom x text surface

L1 for incremental development: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

incremental development -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

- **names the element** (identity rule): Incremental development: growing a program in small, tested steps from a version that works.
- **states the rule** (declarative rule): Start with a working program and make small, incremental changes; at any point, if there is an error, you will know where to look. Use variables for intermediate values so you can check them.

### L2: Multistructural / block x execution / preoperational

L2 for incremental development: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

incremental development -&gt; L2 (Multistructural): the answer applies the rules of incremental development to every part of the code, in order (3 ways).

- **line by line trace** (operational sequencing rule): Sequencing: write a few lines, compile, run and check them, then add the next few; never more than one untested change at a time.
- **output prediction** (evaluation / result rule): Result: after every step there is a program that compiles and runs, and does a little more than before.
- **one step execution** (state-transition rule): State transition: one step adds a small piece of code and ends with the program compiling and passing its checks again.

### L3: Relational / relations x function (concrete operational begins)

L3 for incremental development: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

incremental development -&gt; L3 (Relational): the answer relates the parts (3 ways).

- **relation to neighbour** (composition rule (with a neighbour)): Running after each step shows at once whether the new lines do what was intended.
- **relation to neighbour** (composition rule (with a neighbour)): Small steps make debugging local: the newest change is the first suspect.
- **purpose of the whole** (plan / role rule): Plan: keep a working program at all times so that errors are found where they are made.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for incremental development: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

incremental development -&gt; L4 (Extended abstract): the answer reasons beyond the given code (3 ways).

- **predict a change** (conservation rule; shows `WriteAllThenTest`): Conservation: each step must keep everything that already worked; if a step breaks it, that step is undone or fixed before going on.
- **transfer to a new program** (applicability rule): For any new program: get a minimal version running first (even just printing the inputs), then add one feature at a time, testing each.
- **diagnose an error** (error rule): rule broken: Compile and test after each small change. Kind: compile-time or logic error. Trigger class: many lines are written before the first compile, so the messages and wrong outputs cannot be traced to one change

## Same topic

`incremental_development` belongs to the topic **Programming in Java: create, compile, execute** (`topic1.1.a`). The topic also contains: `compile`, `program_text`, `run`.

## Rules of the concept (14)

- **folk-meaning rule:** Everyday writing is drafted all at once and revised at the end. A program is grown in small steps from a version that already works, compiling and running after each step.
- **wrong rule / right rule:** WriteAllThenTest: wrong: Write the whole program first, then compile and test it all at the end. \| right: Start with a working program and make small changes, compiling and testing after each one, so an error is always in the last change.
- **uneven-application rule:** Applies incremental development unevenly: tests the first few steps one at a time, then adds a large block of untested code at once.
- **identity rule:** Incremental development: growing a program in small, tested steps from a version that works.
- **declarative rule:** Start with a working program and make small, incremental changes; at any point, if there is an error, you will know where to look. Use variables for intermediate values so you can check them.
- **operational sequencing rule:** Sequencing: write a few lines, compile, run and check them, then add the next few; never more than one untested change at a time.
- **evaluation / result rule:** Result: after every step there is a program that compiles and runs, and does a little more than before.
- **state-transition rule:** State transition: one step adds a small piece of code and ends with the program compiling and passing its checks again.
- **composition rule (with a neighbour):** with run: Running after each step shows at once whether the new lines do what was intended.
- **composition rule (with a neighbour):** with debugging: Small steps make debugging local: the newest change is the first suspect.
- **plan / role rule:** Plan: keep a working program at all times so that errors are found where they are made.
- **conservation rule:** Conservation: each step must keep everything that already worked; if a step breaks it, that step is undone or fixed before going on.
- **error rule:** rule broken: Compile and test after each small change. (compile-time or logic error)
- **applicability rule:** For any new program: get a minimal version running first (even just printing the inputs), then add one feature at a time, testing each.

## The whole prerequisite chain

- **Everything it builds on (3):** `compile`, `program_text`, `run`
- **Everything that builds on it (1):** `debugging`
