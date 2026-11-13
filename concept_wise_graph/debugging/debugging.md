# debugging (`debugging`)

finding and fixing the cause of a wrong result or error by forming a hypothesis, changing the program and checking the prediction

Section 1.3 Conditionals and Loops, topic 1.3.f Applications (finite sums, Newton, conversion, gambler's ruin, factoring).

![The knowledge graph around debugging](debugging.png)

## At a glance

- **Needs first:** `incremental_development`, `logical_error`, `reading_error_messages`, `testing`
- **Leads to:** nothing
- **Learned alongside:** nothing
- **Misconceptions:** `CompilerSuggestionIsFix`, `ErrorLineIsFaultLine`, `FixEveryErrorMessage`, `TrialAndErrorDebugging`
- **Errors:** none
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 28 edges around this concept, each explained in the graph's own words.

## What it needs first (4)

A prerequisite edge means the other concept has to be understood before `debugging`.

### `incremental_development` comes before `debugging`

*building a program in small steps from a version that works, compiling and testing after each change*

Developing in small steps keeps debugging local: an error is in the change just made.

- **Grounding:** book passage
- **How `debugging` combines with `incremental_development`:** Small steps keep debugging short: the error is in the change just made.
- **How `incremental_development` combines with `debugging`:** Small steps make debugging local: the newest change is the first suspect.

### `logical_error` comes before `debugging`

*the program runs but computes the wrong result*

Debugging is mostly the search for logic errors, which give wrong output without any message.

- **Grounding:** book passage
- **How `debugging` combines with `logical_error`:** A logic error gives no message, so it is found only by comparing actual values with expected ones.

### `reading_error_messages` comes before `debugging`

*how to read compiler error messages: first error first; reported line may follow the real fault*

Reading an error message tells you where to start looking; debugging goes on from there to the cause.

- **Grounding:** book passage
- **How `debugging` combines with `reading_error_messages`:** An error message gives the place where Java noticed the problem; the cause may be earlier, so it is the start of the search, not the answer.

### `testing` comes before `debugging`

*running a program on chosen inputs, including boundary and unusual ones, and comparing the output with what it should be*

A failing test is what starts debugging: testing finds that something is wrong, debugging finds why.

- **Grounding:** book passage
- **How `debugging` combines with `testing`:** Testing tells that a program is wrong; debugging finds why. The failing test is re-run after the fix.
- **How `testing` combines with `debugging`:** A failing test starts debugging; after the fix, the same test is run again to confirm it.

## What it leads to (0)

These concepts need `debugging` first.

No concept has this one as a prerequisite.

## Learned alongside (0)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

No parallel edge touches this concept.

## Misconceptions (4)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### CompilerSuggestionIsFix

- **Wrong rule:** Doing exactly what the compiler message suggests will fix the error.
- **Right rule:** An error message is evidence that something is wrong, but its suggested remedy may be wrong; find the actual cause.
- **Role of this concept:** context
- **Also an edge from `compile_time_error`:** Doing exactly what the compiler message suggests will fix the error.
- **Also an edge from `reading_error_messages`:** Doing exactly what the compiler message suggests will fix the error.

### ErrorLineIsFaultLine

- **Wrong rule:** The line number in a javac error is always the line that has the mistake.
- **Right rule:** The compiler reports where it noticed the problem, which can be after the real fault; for example, omitting the second left brace of HelloWorld produces errors reported on later lines.
- **Role of this concept:** context
- **Also an edge from `compile_time_error`:** The line number in a javac error is always the line that has the mistake.
- **Also an edge from `reading_error_messages`:** The line number in a javac error is always the line that has the mistake.

### FixEveryErrorMessage

- **Wrong rule:** Each error message is a separate mistake that needs its own fix.
- **Right rule:** One fault can produce several messages; fix the first and recompile.
- **Role of this concept:** context
- **Also an edge from `reading_error_messages`:** Each error message is a separate mistake that needs its own fix.

### TrialAndErrorDebugging

- **Wrong rule:** Debugging means changing the code until the error goes away.
- **Right rule:** Debugging is like an experiment: form a hypothesis about what is wrong, change the program, and check that the result matches the prediction.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: Debugging means changing the code until the error goes away. Right rule: Debugging is like an experiment: form a hypothesis about what is wrong, change the program, and check that the result matches the prediction.
- **Shows at level L0 as:** inconsistent trace: Applies the debugging method unevenly: forms a hypothesis for the first bug, then makes random changes for the next one. (here mixing in: "Debugging means changing the code until the error goes away")

## Errors (0)

An error edge states the rule that gets broken in a program, and the right rule.

The graph has no error edge from this concept.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for debugging: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to debugging agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

debugging -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (3 ways).

- **everyday reading** (folk-meaning rule): Everyday 'fixing' means trying changes until a problem goes away. In programming, debugging finds the cause first: form a hypothesis, change the program, and check that the result is the one predicted.
- **misconception** (wrong rule / right rule; shows `TrialAndErrorDebugging`): wrong rule: Debugging means changing the code until the error goes away. Right rule: Debugging is like an experiment: form a hypothesis about what is wrong, change the program, and check that the result matches the prediction.
- **inconsistent trace** (uneven-application rule; shows `TrialAndErrorDebugging`): Applies the debugging method unevenly: forms a hypothesis for the first bug, then makes random changes for the next one. (here mixing in: "Debugging means changing the code until the error goes away")

### L1: Unistructural / atom x text surface

L1 for debugging: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

debugging -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

- **names the element** (identity rule): Debugging: finding and removing the cause of a wrong result or an error.
- **states the rule** (declarative rule): Debug like an experimental scientist: once you have an idea of what is going wrong, modify the program and try again; if the hypothesis was right, you can predict the result of the change.

### L2: Multistructural / block x execution / preoperational

L2 for debugging: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

debugging -&gt; L2 (Multistructural): the answer applies the rules of debugging to every part of the code, in order (3 ways).

- **line by line trace** (operational sequencing rule): Sequencing: reproduce the failure, locate where the actual values first differ from the expected ones (by tracing or by printing intermediate values), form a hypothesis, change one thing, and run again.
- **output prediction** (evaluation / result rule): Result: a fix is accepted when the failing input now gives the expected output and the earlier tests still pass.
- **one step execution** (state-transition rule): State transition: each debugging step changes one thing in the program and either confirms or rejects one hypothesis.

### L3: Relational / relations x function (concrete operational begins)

L3 for debugging: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

debugging -&gt; L3 (Relational): the answer relates the parts (5 ways).

- **relation to neighbour** (composition rule (with a neighbour)): Testing tells that a program is wrong; debugging finds why. The failing test is re-run after the fix.
- **relation to neighbour** (composition rule (with a neighbour)): An error message gives the place where Java noticed the problem; the cause may be earlier, so it is the start of the search, not the answer.
- **relation to neighbour** (composition rule (with a neighbour)): A logic error gives no message, so it is found only by comparing actual values with expected ones.
- **relation to neighbour** (composition rule (with a neighbour)): Small steps keep debugging short: the error is in the change just made.
- **purpose of the whole** (plan / role rule): Plan: turn a failing program into a working one by finding the cause of each failure, not by guessing.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for debugging: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

debugging -&gt; L4 (Extended abstract): the answer reasons beyond the given code (3 ways).

- **predict a change** (conservation rule; shows `TrialAndErrorDebugging`): Conservation: a correct fix removes the cause for the whole class of inputs that failed, and changes nothing for inputs that already worked.
- **transfer to a new program** (applicability rule): When a program fails: reproduce the failure, print or trace intermediate values to find where they first go wrong, fix that, and re-run all the tests.
- **diagnose an error** (error rule): rule broken: Find the cause before changing code. Kind: logic error. Trigger class: changes are made at random until one test passes, so the bug survives for other inputs or a new bug is added

## Same topic

`debugging` belongs to the topic **Applications (finite sums, Newton, conversion, gambler's ruin, factoring)** (`topic1.3.f`). The topic also contains: `accumulator_pattern`, `convergence_test`, `counter_pattern`, `fencepost_loop`, `flag_search_loop`, `loop_performance`, `monte_carlo_simulation`, `number_conversion`, `testing`.

## Rules of the concept (16)

- **folk-meaning rule:** Everyday 'fixing' means trying changes until a problem goes away. In programming, debugging finds the cause first: form a hypothesis, change the program, and check that the result is the one predicted.
- **wrong rule / right rule:** TrialAndErrorDebugging: wrong: Debugging means changing the code until the error goes away. \| right: Debugging is like an experiment: form a hypothesis about what is wrong, change the program, and check that the result matches the prediction.
- **uneven-application rule:** Applies the debugging method unevenly: forms a hypothesis for the first bug, then makes random changes for the next one.
- **identity rule:** Debugging: finding and removing the cause of a wrong result or an error.
- **declarative rule:** Debug like an experimental scientist: once you have an idea of what is going wrong, modify the program and try again; if the hypothesis was right, you can predict the result of the change.
- **operational sequencing rule:** Sequencing: reproduce the failure, locate where the actual values first differ from the expected ones (by tracing or by printing intermediate values), form a hypothesis, change one thing, and run again.
- **evaluation / result rule:** Result: a fix is accepted when the failing input now gives the expected output and the earlier tests still pass.
- **state-transition rule:** State transition: each debugging step changes one thing in the program and either confirms or rejects one hypothesis.
- **composition rule (with a neighbour):** with testing: Testing tells that a program is wrong; debugging finds why. The failing test is re-run after the fix.
- **composition rule (with a neighbour):** with reading\_error\_messages: An error message gives the place where Java noticed the problem; the cause may be earlier, so it is the start of the search, not the answer.
- **composition rule (with a neighbour):** with logical\_error: A logic error gives no message, so it is found only by comparing actual values with expected ones.
- **composition rule (with a neighbour):** with incremental\_development: Small steps keep debugging short: the error is in the change just made.
- **plan / role rule:** Plan: turn a failing program into a working one by finding the cause of each failure, not by guessing.
- **conservation rule:** Conservation: a correct fix removes the cause for the whole class of inputs that failed, and changes nothing for inputs that already worked.
- **error rule:** rule broken: Find the cause before changing code. (logic error)
- **applicability rule:** When a program fails: reproduce the failure, print or trace intermediate values to find where they first go wrong, fix that, and re-run all the tests.

## The whole prerequisite chain

- **Everything it builds on (20):** `assignment`, `class_declaration`, `compile`, `compile_time_error`, `data_type`, `declaration`, `empty_statement`, `identifier`, `incremental_development`, `literal`, `logical_error`, `main_method`, `primitive_type`, `program_text`, `program_trace`, `reading_error_messages`, `run`, `statement`, `testing`, `variable`
- **Everything that builds on it (0):** nothing
