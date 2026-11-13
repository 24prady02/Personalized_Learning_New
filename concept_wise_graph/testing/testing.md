# testing (`testing`)

running a program on chosen inputs, including boundary and unusual ones, and comparing the output with what it should be

Section 1.3 Conditionals and Loops, topic 1.3.f Applications (finite sums, Newton, conversion, gambler's ruin, factoring).

![The knowledge graph around testing](testing.png)

## At a glance

- **Needs first:** `program_trace`, `run`
- **Leads to:** `debugging`
- **Learned alongside:** nothing
- **Misconceptions:** `CompilesMeansWorks`, `OneTestProvesCorrect`
- **Errors:** none
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 24 edges around this concept, each explained in the graph's own words.

## What it needs first (2)

A prerequisite edge means the other concept has to be understood before `testing`.

### `program_trace` comes before `testing`

*Trace (table of variable values): a table of the values of the variables after each statement, used to check what code does*

A test needs an expected result, and the expected result comes from tracing what the program should do, step by step.

- **Grounding:** book passage
- **How `testing` combines with `program_trace`:** The expected output of a test comes from a hand trace of what the program should do for that input.

### `run` comes before `testing`

*java executes main in the JVM*

A program is tested by running it on chosen inputs and comparing what it prints with what it should print.

- **Grounding:** book passage
- **How `testing` combines with `run`:** Each test is one run with one input: java Name followed by the test arguments (or with input redirected from a file).

## What it leads to (1)

These concepts need `testing` first.

### `testing` comes before `debugging`

*finding and fixing the cause of a wrong result or error by forming a hypothesis, changing the program and checking the prediction*

A failing test is what starts debugging: testing finds that something is wrong, debugging finds why.

- **Grounding:** book passage
- **How `testing` combines with `debugging`:** A failing test starts debugging; after the fix, the same test is run again to confirm it.
- **How `debugging` combines with `testing`:** Testing tells that a program is wrong; debugging finds why. The failing test is re-run after the fix.

## Learned alongside (0)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

No parallel edge touches this concept.

## Misconceptions (2)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### CompilesMeansWorks

- **Wrong rule:** Code that compiles is code that works.
- **Right rule:** Code that compiles can still have run-time and logical errors.
- **Role of this concept:** context
- **Shows at level L0 as:** misconception: wrong rule: Code that compiles is code that works. Right rule: Compiling checks only the form of the code; whether it does the right thing is found by running and testing it.
- **Also an edge from `compile`:** Code that compiles is code that works.
- **Also an edge from `compile_time_error`:** Code that compiles is code that works.
- **Also an edge from `logical_error`:** Code that compiles is code that works.
- **Also an edge from `run_time_error`:** Code that compiles is code that works.

### OneTestProvesCorrect

- **Wrong rule:** If a program gives the right output for one input, it is correct.
- **Right rule:** One passing run shows only that this input works; a program is checked by running it on numerous inputs, including boundary and unusual ones.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: If a program gives the right output for one input, it is correct. Right rule: One passing run shows only that this input works; check the program on numerous inputs, including boundary and unusual ones.
- **Shows at level L0 as:** inconsistent trace: Applies the testing rule unevenly: checks the output for one input against an expected value, but accepts the output for another input without working out what it should be. (here mixing in: "If a program gives the right output for one input, it is correct")

## Errors (0)

An error edge states the rule that gets broken in a program, and the right rule.

The graph has no error edge from this concept.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for testing: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to testing agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

testing -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (4 ways).

- **everyday reading** (folk-meaning rule): Everyday 'test' means trying something once to see whether it works. A program test runs the program on several chosen inputs, each with an expected output worked out in advance, and compares the two.
- **misconception** (wrong rule / right rule; shows `OneTestProvesCorrect`): wrong rule: If a program gives the right output for one input, it is correct. Right rule: One passing run shows only that this input works; check the program on numerous inputs, including boundary and unusual ones.
- **inconsistent trace** (uneven-application rule; shows `OneTestProvesCorrect`): Applies the testing rule unevenly: checks the output for one input against an expected value, but accepts the output for another input without working out what it should be. (here mixing in: "If a program gives the right output for one input, it is correct")
- **misconception** (wrong rule / right rule; shows `CompilesMeansWorks`): wrong rule: Code that compiles is code that works. Right rule: Compiling checks only the form of the code; whether it does the right thing is found by running and testing it.

### L1: Unistructural / atom x text surface

L1 for testing: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

testing -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

- **names the element** (identity rule): Testing: running the program on chosen inputs and comparing each output with the expected output.
- **states the rule** (declarative rule): Write the program, then run and test it: choose inputs, work out the expected output of each in advance, run the program on each, and compare. Include the boundary cases (0, 1, the largest value, an empty input).

### L2: Multistructural / block x execution / preoperational

L2 for testing: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

testing -&gt; L2 (Multistructural): the answer applies the rules of testing to every part of the code, in order (3 ways).

- **line by line trace** (operational sequencing rule): Sequencing: first decide the inputs and expected outputs, then run the program once per input, then compare each output with its expectation; a mismatch is recorded before anything is changed.
- **output prediction** (evaluation / result rule): Result: for each input the test gives pass (output equals expectation) or fail; the program is accepted only when every chosen input passes.
- **one step execution** (state-transition rule): State transition: one test run leaves the program unchanged and adds one pass or fail to what is known about it.

### L3: Relational / relations x function (concrete operational begins)

L3 for testing: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

testing -&gt; L3 (Relational): the answer relates the parts (4 ways).

- **relation to neighbour** (composition rule (with a neighbour)): Each test is one run with one input: java Name followed by the test arguments (or with input redirected from a file).
- **relation to neighbour** (composition rule (with a neighbour)): The expected output of a test comes from a hand trace of what the program should do for that input.
- **relation to neighbour** (composition rule (with a neighbour)): A failing test starts debugging; after the fix, the same test is run again to confirm it.
- **purpose of the whole** (plan / role rule): Plan: tests give evidence that a program does what it should for the inputs that matter, and catch the cases where it does not.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for testing: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

testing -&gt; L4 (Extended abstract): the answer reasons beyond the given code (3 ways).

- **predict a change** (conservation rule; shows `OneTestProvesCorrect`): Conservation: after any change to the program, the earlier tests must still pass; a fix for one input that breaks another is caught by re-running them all.
- **transfer to a new program** (applicability rule): Test every program you write, before using its output: on the given example, on the boundary values, and on an input whose answer you can work out by hand.
- **diagnose an error** (error rule): rule broken: A program is checked on several inputs, including the boundary cases. Kind: silent logic error. Trigger class: only the example input is tried, so a bug that shows for 0, 1, a negative value, the largest value or an empty input is never seen

## Same topic

`testing` belongs to the topic **Applications (finite sums, Newton, conversion, gambler's ruin, factoring)** (`topic1.3.f`). The topic also contains: `accumulator_pattern`, `convergence_test`, `counter_pattern`, `debugging`, `fencepost_loop`, `flag_search_loop`, `loop_performance`, `monte_carlo_simulation`, `number_conversion`.

## Rules of the concept (16)

- **folk-meaning rule:** Everyday 'test' means trying something once to see whether it works. A program test runs the program on several chosen inputs, each with an expected output worked out in advance, and compares the two.
- **wrong rule / right rule:** OneTestProvesCorrect: wrong: If a program gives the right output for one input, it is correct. \| right: One passing run shows only that this input works; check the program on numerous inputs, including boundary and unusual ones.
- **wrong rule / right rule:** CompilesMeansWorks: wrong: Code that compiles is code that works. \| right: Compiling checks only the form of the code; whether it does the right thing is found by running and testing it.
- **uneven-application rule:** Applies the testing rule unevenly: checks the output for one input against an expected value, but accepts the output for another input without working out what it should be.
- **identity rule:** Testing: running the program on chosen inputs and comparing each output with the expected output.
- **declarative rule:** Write the program, then run and test it: choose inputs, work out the expected output of each in advance, run the program on each, and compare. Include the boundary cases (0, 1, the largest value, an empty input).
- **operational sequencing rule:** Sequencing: first decide the inputs and expected outputs, then run the program once per input, then compare each output with its expectation; a mismatch is recorded before anything is changed.
- **evaluation / result rule:** Result: for each input the test gives pass (output equals expectation) or fail; the program is accepted only when every chosen input passes.
- **state-transition rule:** State transition: one test run leaves the program unchanged and adds one pass or fail to what is known about it.
- **composition rule (with a neighbour):** with run: Each test is one run with one input: java Name followed by the test arguments (or with input redirected from a file).
- **composition rule (with a neighbour):** with program\_trace: The expected output of a test comes from a hand trace of what the program should do for that input.
- **composition rule (with a neighbour):** with debugging: A failing test starts debugging; after the fix, the same test is run again to confirm it.
- **plan / role rule:** Plan: tests give evidence that a program does what it should for the inputs that matter, and catch the cases where it does not.
- **conservation rule:** Conservation: after any change to the program, the earlier tests must still pass; a fix for one input that breaks another is caught by re-running them all.
- **error rule:** rule broken: A program is checked on several inputs, including the boundary cases. (silent logic error)
- **applicability rule:** Test every program you write, before using its output: on the given example, on the boundary values, and on an input whose answer you can work out by hand.

## The whole prerequisite chain

- **Everything it builds on (11):** `assignment`, `compile`, `data_type`, `declaration`, `identifier`, `literal`, `primitive_type`, `program_text`, `program_trace`, `run`, `variable`
- **Everything that builds on it (1):** `debugging`
