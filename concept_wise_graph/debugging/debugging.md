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

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 28 edges around this concept. The edge logic, the wrong and right rules and the exact rules of the ways are copied word for word from the graph.

## To work on (3)

- misconceptions with no L0 way linked to them: ErrorLineIsFaultLine, FixEveryErrorMessage, CompilerSuggestionIsFix
- no code pattern or signal: the code cannot tag this concept
- no aliases: a student's words cannot name this concept

## What it needs first (4)

A prerequisite edge means the other concept has to be understood before `debugging`.

### `incremental_development` comes before `debugging`

*building a program in small steps from a version that works, compiling and testing after each change*

- **Edge:** `pre:incremental_development->debugging`
- **Exact edge logic:** Developing in small steps keeps debugging local: an error is in the change just made.
- **Grounding:** book\_passage
- **Composition rule (R) of `debugging` with `incremental_development`:** Small steps keep debugging short: the error is in the change just made.
- **Composition rule (R) of `incremental_development` with `debugging`:** Small steps make debugging local: the newest change is the first suspect.

### `logical_error` comes before `debugging`

*the program runs but computes the wrong result*

- **Edge:** `pre:logical_error->debugging`
- **Exact edge logic:** Debugging is mostly the search for logic errors, which give wrong output without any message.
- **Grounding:** book\_passage
- **Composition rule (R) of `debugging` with `logical_error`:** A logic error gives no message, so it is found only by comparing actual values with expected ones.

### `reading_error_messages` comes before `debugging`

*how to read compiler error messages: first error first; reported line may follow the real fault*

- **Edge:** `pre:reading_error_messages->debugging`
- **Exact edge logic:** Reading an error message tells you where to start looking; debugging goes on from there to the cause.
- **Grounding:** book\_passage
- **Composition rule (R) of `debugging` with `reading_error_messages`:** An error message gives the place where Java noticed the problem; the cause may be earlier, so it is the start of the search, not the answer.

### `testing` comes before `debugging`

*running a program on chosen inputs, including boundary and unusual ones, and comparing the output with what it should be*

- **Edge:** `pre:testing->debugging`
- **Exact edge logic:** A failing test is what starts debugging: testing finds that something is wrong, debugging finds why.
- **Grounding:** book\_passage
- **Composition rule (R) of `debugging` with `testing`:** Testing tells that a program is wrong; debugging finds why. The failing test is re-run after the fix.
- **Composition rule (R) of `testing` with `debugging`:** A failing test starts debugging; after the fix, the same test is run again to confirm it.

## What it leads to (0)

These concepts need `debugging` first.

No concept has this one as a prerequisite.

## Learned alongside (0)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

No parallel edge touches this concept.

## Misconceptions (4)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### CompilerSuggestionIsFix

- **Edge:** `debugging` &rarr; `CompilerSuggestionIsFix` (misconception)
- **Exact edge logic (the wrong rule):** Doing exactly what the compiler message suggests will fix the error.
- **Twin logic (the right rule):** An error message is evidence that something is wrong, but its suggested remedy may be wrong; find the actual cause.
- **Wrong belief (on the node):** Doing exactly what the compiler message suggests will fix the error.
- **Correct rule (on the node):** An error message is evidence that something is wrong, but its suggested remedy may be wrong; find the actual cause.
- **Provenance:** textbook
- **Role of this concept:** context
- **L0 way linked to it:** no
- **Edge `compile_time_error` &rarr; `CompilerSuggestionIsFix`, exact edge logic:** Doing exactly what the compiler message suggests will fix the error. **Twin logic:** An error message is evidence that something is wrong, but its suggested remedy may be wrong; find the actual cause. (role: context)
- **Edge `reading_error_messages` &rarr; `CompilerSuggestionIsFix`, exact edge logic:** Doing exactly what the compiler message suggests will fix the error. **Twin logic:** An error message is evidence that something is wrong, but its suggested remedy may be wrong; find the actual cause. (role: primary)

### ErrorLineIsFaultLine

- **Edge:** `debugging` &rarr; `ErrorLineIsFaultLine` (misconception)
- **Exact edge logic (the wrong rule):** The line number in a javac error is always the line that has the mistake.
- **Twin logic (the right rule):** The compiler reports where it noticed the problem, which can be after the real fault; for example, omitting the second left brace of HelloWorld produces errors reported on later lines.
- **Wrong belief (on the node):** The line number in a javac error is always the line that has the mistake.
- **Correct rule (on the node):** The compiler reports where it noticed the problem, which can be after the real fault; for example, omitting the second left brace of HelloWorld produces errors reported on later lines.
- **Provenance:** textbook
- **Role of this concept:** context
- **L0 way linked to it:** no
- **Edge `compile_time_error` &rarr; `ErrorLineIsFaultLine`, exact edge logic:** The line number in a javac error is always the line that has the mistake. **Twin logic:** The compiler reports where it noticed the problem, which can be after the real fault; for example, omitting the second left brace of HelloWorld produces errors reported on later lines. (role: context)
- **Edge `reading_error_messages` &rarr; `ErrorLineIsFaultLine`, exact edge logic:** The line number in a javac error is always the line that has the mistake. **Twin logic:** The compiler reports where it noticed the problem, which can be after the real fault; for example, omitting the second left brace of HelloWorld produces errors reported on later lines. (role: primary)

### FixEveryErrorMessage

- **Edge:** `debugging` &rarr; `FixEveryErrorMessage` (misconception)
- **Exact edge logic (the wrong rule):** Each error message is a separate mistake that needs its own fix.
- **Twin logic (the right rule):** One fault can produce several messages; fix the first and recompile.
- **Wrong belief (on the node):** Each error message is a separate mistake that needs its own fix.
- **Correct rule (on the node):** One fault can produce several messages; fix the first and recompile.
- **Provenance:** textbook
- **Role of this concept:** context
- **L0 way linked to it:** no
- **Edge `reading_error_messages` &rarr; `FixEveryErrorMessage`, exact edge logic:** Each error message is a separate mistake that needs its own fix. **Twin logic:** One fault can produce several messages; fix the first and recompile. (role: primary)

### TrialAndErrorDebugging

- **Edge:** `debugging` &rarr; `TrialAndErrorDebugging` (misconception)
- **Exact edge logic (the wrong rule):** Debugging means changing the code until the error goes away.
- **Twin logic (the right rule):** Debugging is like an experiment: form a hypothesis about what is wrong, change the program, and check that the result matches the prediction.
- **Wrong belief (on the node):** Debugging means changing the code until the error goes away.
- **Correct rule (on the node):** Debugging is like an experiment: form a hypothesis about what is wrong, change the program, and check that the result matches the prediction.
- **Provenance:** textbook
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [1] misconception, exact rule:** wrong rule: Debugging means changing the code until the error goes away. Right rule: Debugging is like an experiment: form a hypothesis about what is wrong, change the program, and check that the result matches the prediction.
- **L0 way [2] inconsistent\_trace, exact rule:** Applies the debugging method unevenly: forms a hypothesis for the first bug, then makes random changes for the next one. (here mixing in: "Debugging means changing the code until the error goes away")

## Errors (0)

An error edge states the rule that gets broken in a program, and the right rule.

The graph has no error edge from this concept.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for debugging: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to debugging agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

- **Edge:** `debugging` &rarr; `debugging@L0` (has_level)
- **Exact edge logic:** debugging -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (3 ways).

Ways (3), each with its exact rule:

- **[0] everyday\_reading** (rule type E, folk-meaning rule): Everyday 'fixing' means trying changes until a problem goes away. In programming, debugging finds the cause first: form a hypothesis, change the program, and check that the result is the one predicted.
- **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `TrialAndErrorDebugging`: wrong rule: Debugging means changing the code until the error goes away. Right rule: Debugging is like an experiment: form a hypothesis about what is wrong, change the program, and check that the result matches the prediction.
- **[2] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `TrialAndErrorDebugging`: Applies the debugging method unevenly: forms a hypothesis for the first bug, then makes random changes for the next one. (here mixing in: "Debugging means changing the code until the error goes away")

### L1: Unistructural / atom x text surface

L1 for debugging: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

- **Edge:** `debugging` &rarr; `debugging@L1` (has_level)
- **Exact edge logic:** debugging -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

Ways (2), each with its exact rule:

- **[0] names\_the\_element** (rule type N, identity rule): Debugging: finding and removing the cause of a wrong result or an error.
- **[1] states\_the\_rule** (rule type S, declarative rule): Debug like an experimental scientist: once you have an idea of what is going wrong, modify the program and try again; if the hypothesis was right, you can predict the result of the change.

### L2: Multistructural / block x execution / preoperational

L2 for debugging: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

- **Edge:** `debugging` &rarr; `debugging@L2` (has_level)
- **Exact edge logic:** debugging -&gt; L2 (Multistructural): the answer applies the rules of debugging to every part of the code, in order (3 ways).

Ways (3), each with its exact rule:

- **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): Sequencing: reproduce the failure, locate where the actual values first differ from the expected ones (by tracing or by printing intermediate values), form a hypothesis, change one thing, and run again.
- **[1] output\_prediction** (rule type OP, evaluation / result rule): Result: a fix is accepted when the failing input now gives the expected output and the earlier tests still pass.
- **[2] one\_step\_execution** (rule type OS, state-transition rule): State transition: each debugging step changes one thing in the program and either confirms or rejects one hypothesis.

### L3: Relational / relations x function (concrete operational begins)

L3 for debugging: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

- **Edge:** `debugging` &rarr; `debugging@L3` (has_level)
- **Exact edge logic:** debugging -&gt; L3 (Relational): the answer relates the parts (5 ways).

Ways (5), each with its exact rule:

- **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Testing tells that a program is wrong; debugging finds why. The failing test is re-run after the fix.
- **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): An error message gives the place where Java noticed the problem; the cause may be earlier, so it is the start of the search, not the answer.
- **[2] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): A logic error gives no message, so it is found only by comparing actual values with expected ones.
- **[3] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Small steps keep debugging short: the error is in the change just made.
- **[4] purpose\_of\_the\_whole** (rule type P, plan / role rule): Plan: turn a failing program into a working one by finding the cause of each failure, not by guessing.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for debugging: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

- **Edge:** `debugging` &rarr; `debugging@L4` (has_level)
- **Exact edge logic:** debugging -&gt; L4 (Extended abstract): the answer reasons beyond the given code (3 ways).

Ways (3), each with its exact rule:

- **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `TrialAndErrorDebugging`: Conservation: a correct fix removes the cause for the whole class of inputs that failed, and changes nothing for inputs that already worked.
- **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): When a program fails: reproduce the failure, print or trace intermediate values to find where they first go wrong, fix that, and re-run all the tests.
- **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: Find the cause before changing code. Kind: logic error. Trigger class: changes are made at random until one test passes, so the bug survives for other inputs or a new bug is added

## Same topic

`debugging` belongs to the topic **Applications (finite sums, Newton, conversion, gambler's ruin, factoring)** (`topic1.3.f`). The topic also contains: `accumulator_pattern`, `convergence_test`, `counter_pattern`, `fencepost_loop`, `flag_search_loop`, `loop_performance`, `monte_carlo_simulation`, `number_conversion`, `testing`.

## Rules of the concept (16)

- **Book** (SW-1e, p. 177 (pdf 187)): "is that debugging is difficult."
- **Book** (TJ-2e, p. 11 (pdf 33)): "Debugging is like an experimental science: once you have an idea about what is going wrong, you modify your program and try again."
- **E** (folk-meaning rule): Everyday 'fixing' means trying changes until a problem goes away. In programming, debugging finds the cause first: form a hypothesis, change the program, and check that the result is the one predicted.
- **M** (wrong rule / right rule): TrialAndErrorDebugging: wrong: Debugging means changing the code until the error goes away. \| right: Debugging is like an experiment: form a hypothesis about what is wrong, change the program, and check that the result matches the prediction.
- **T** (uneven-application rule): Applies the debugging method unevenly: forms a hypothesis for the first bug, then makes random changes for the next one.
- **N** (identity rule): Debugging: finding and removing the cause of a wrong result or an error.
- **S** (declarative rule): Debug like an experimental scientist: once you have an idea of what is going wrong, modify the program and try again; if the hypothesis was right, you can predict the result of the change.
- **LT** (operational sequencing rule): Sequencing: reproduce the failure, locate where the actual values first differ from the expected ones (by tracing or by printing intermediate values), form a hypothesis, change one thing, and run again.
- **OP** (evaluation / result rule): Result: a fix is accepted when the failing input now gives the expected output and the earlier tests still pass.
- **OS** (state-transition rule): State transition: each debugging step changes one thing in the program and either confirms or rejects one hypothesis.
- **R** (composition rule (with a neighbour)): with testing: Testing tells that a program is wrong; debugging finds why. The failing test is re-run after the fix.
- **R** (composition rule (with a neighbour)): with reading\_error\_messages: An error message gives the place where Java noticed the problem; the cause may be earlier, so it is the start of the search, not the answer.
- **R** (composition rule (with a neighbour)): with logical\_error: A logic error gives no message, so it is found only by comparing actual values with expected ones.
- **R** (composition rule (with a neighbour)): with incremental\_development: Small steps keep debugging short: the error is in the change just made.
- **P** (plan / role rule): Plan: turn a failing program into a working one by finding the cause of each failure, not by guessing.
- **C** (conservation rule): Conservation: a correct fix removes the cause for the whole class of inputs that failed, and changes nothing for inputs that already worked.
- **D** (error rule): rule broken: Find the cause before changing code. (logic error)
- **X** (applicability rule): When a program fails: reproduce the failure, print or trace intermediate values to find where they first go wrong, fix that, and re-run all the tests.

## How it is found in code and answers (reader block)

- **Aliases:** none
- **Code patterns:** none
- **Operator symbols:** none
- **Java types:** none

## The whole prerequisite chain

- **Everything it builds on (20):** `assignment`, `class_declaration`, `compile`, `compile_time_error`, `data_type`, `declaration`, `empty_statement`, `identifier`, `incremental_development`, `literal`, `logical_error`, `main_method`, `primitive_type`, `program_text`, `program_trace`, `reading_error_messages`, `run`, `statement`, `testing`, `variable`
- **Everything that builds on it (0):** nothing

## Every edge in this view and its exact edge logic (28)

All the edges drawn in the picture, in the order: prerequisite, parallel, misconception, error, has_level, contains.

**1. `incremental_development` &rarr; `debugging`** (prerequisite)

- **Exact edge logic:** Developing in small steps keeps debugging local: an error is in the change just made.
- **Grounding:** book\_passage
- **Composition rule (R) of `incremental_development` with `debugging`:** Small steps make debugging local: the newest change is the first suspect.
- **Composition rule (R) of `debugging` with `incremental_development`:** Small steps keep debugging short: the error is in the change just made.

**2. `logical_error` &rarr; `debugging`** (prerequisite)

- **Exact edge logic:** Debugging is mostly the search for logic errors, which give wrong output without any message.
- **Grounding:** book\_passage
- **Composition rule (R) of `debugging` with `logical_error`:** A logic error gives no message, so it is found only by comparing actual values with expected ones.

**3. `reading_error_messages` &rarr; `debugging`** (prerequisite)

- **Exact edge logic:** Reading an error message tells you where to start looking; debugging goes on from there to the cause.
- **Grounding:** book\_passage
- **Composition rule (R) of `debugging` with `reading_error_messages`:** An error message gives the place where Java noticed the problem; the cause may be earlier, so it is the start of the search, not the answer.

**4. `testing` &rarr; `debugging`** (prerequisite)

- **Exact edge logic:** A failing test is what starts debugging: testing finds that something is wrong, debugging finds why.
- **Grounding:** book\_passage
- **Composition rule (R) of `testing` with `debugging`:** A failing test starts debugging; after the fix, the same test is run again to confirm it.
- **Composition rule (R) of `debugging` with `testing`:** Testing tells that a program is wrong; debugging finds why. The failing test is re-run after the fix.

**5. `debugging` &rarr; `CompilerSuggestionIsFix`** (misconception)

- **Exact edge logic (the wrong rule):** Doing exactly what the compiler message suggests will fix the error.
- **Twin logic (the right rule):** An error message is evidence that something is wrong, but its suggested remedy may be wrong; find the actual cause.
- **Role:** context

**6. `debugging` &rarr; `ErrorLineIsFaultLine`** (misconception)

- **Exact edge logic (the wrong rule):** The line number in a javac error is always the line that has the mistake.
- **Twin logic (the right rule):** The compiler reports where it noticed the problem, which can be after the real fault; for example, omitting the second left brace of HelloWorld produces errors reported on later lines.
- **Role:** context

**7. `debugging` &rarr; `FixEveryErrorMessage`** (misconception)

- **Exact edge logic (the wrong rule):** Each error message is a separate mistake that needs its own fix.
- **Twin logic (the right rule):** One fault can produce several messages; fix the first and recompile.
- **Role:** context

**8. `debugging` &rarr; `TrialAndErrorDebugging`** (misconception)

- **Exact edge logic (the wrong rule):** Debugging means changing the code until the error goes away.
- **Twin logic (the right rule):** Debugging is like an experiment: form a hypothesis about what is wrong, change the program, and check that the result matches the prediction.
- **Role:** primary

**9. `compile_time_error` &rarr; `CompilerSuggestionIsFix`** (misconception)

- **Exact edge logic (the wrong rule):** Doing exactly what the compiler message suggests will fix the error.
- **Twin logic (the right rule):** An error message is evidence that something is wrong, but its suggested remedy may be wrong; find the actual cause.
- **Role:** context

**10. `compile_time_error` &rarr; `ErrorLineIsFaultLine`** (misconception)

- **Exact edge logic (the wrong rule):** The line number in a javac error is always the line that has the mistake.
- **Twin logic (the right rule):** The compiler reports where it noticed the problem, which can be after the real fault; for example, omitting the second left brace of HelloWorld produces errors reported on later lines.
- **Role:** context

**11. `reading_error_messages` &rarr; `CompilerSuggestionIsFix`** (misconception)

- **Exact edge logic (the wrong rule):** Doing exactly what the compiler message suggests will fix the error.
- **Twin logic (the right rule):** An error message is evidence that something is wrong, but its suggested remedy may be wrong; find the actual cause.
- **Role:** primary

**12. `reading_error_messages` &rarr; `ErrorLineIsFaultLine`** (misconception)

- **Exact edge logic (the wrong rule):** The line number in a javac error is always the line that has the mistake.
- **Twin logic (the right rule):** The compiler reports where it noticed the problem, which can be after the real fault; for example, omitting the second left brace of HelloWorld produces errors reported on later lines.
- **Role:** primary

**13. `reading_error_messages` &rarr; `FixEveryErrorMessage`** (misconception)

- **Exact edge logic (the wrong rule):** Each error message is a separate mistake that needs its own fix.
- **Twin logic (the right rule):** One fault can produce several messages; fix the first and recompile.
- **Role:** primary

**14. `debugging` &rarr; `debugging@L0`** (has_level)

- **Exact edge logic:** debugging -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (3 ways).
  - **[0] everyday\_reading** (rule type E, folk-meaning rule): Everyday 'fixing' means trying changes until a problem goes away. In programming, debugging finds the cause first: form a hypothesis, change the program, and check that the result is the one predicted.
  - **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `TrialAndErrorDebugging`: wrong rule: Debugging means changing the code until the error goes away. Right rule: Debugging is like an experiment: form a hypothesis about what is wrong, change the program, and check that the result matches the prediction.
  - **[2] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `TrialAndErrorDebugging`: Applies the debugging method unevenly: forms a hypothesis for the first bug, then makes random changes for the next one. (here mixing in: "Debugging means changing the code until the error goes away")

**15. `debugging` &rarr; `debugging@L1`** (has_level)

- **Exact edge logic:** debugging -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).
  - **[0] names\_the\_element** (rule type N, identity rule): Debugging: finding and removing the cause of a wrong result or an error.
  - **[1] states\_the\_rule** (rule type S, declarative rule): Debug like an experimental scientist: once you have an idea of what is going wrong, modify the program and try again; if the hypothesis was right, you can predict the result of the change.

**16. `debugging` &rarr; `debugging@L2`** (has_level)

- **Exact edge logic:** debugging -&gt; L2 (Multistructural): the answer applies the rules of debugging to every part of the code, in order (3 ways).
  - **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): Sequencing: reproduce the failure, locate where the actual values first differ from the expected ones (by tracing or by printing intermediate values), form a hypothesis, change one thing, and run again.
  - **[1] output\_prediction** (rule type OP, evaluation / result rule): Result: a fix is accepted when the failing input now gives the expected output and the earlier tests still pass.
  - **[2] one\_step\_execution** (rule type OS, state-transition rule): State transition: each debugging step changes one thing in the program and either confirms or rejects one hypothesis.

**17. `debugging` &rarr; `debugging@L3`** (has_level)

- **Exact edge logic:** debugging -&gt; L3 (Relational): the answer relates the parts (5 ways).
  - **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Testing tells that a program is wrong; debugging finds why. The failing test is re-run after the fix.
  - **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): An error message gives the place where Java noticed the problem; the cause may be earlier, so it is the start of the search, not the answer.
  - **[2] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): A logic error gives no message, so it is found only by comparing actual values with expected ones.
  - **[3] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Small steps keep debugging short: the error is in the change just made.
  - **[4] purpose\_of\_the\_whole** (rule type P, plan / role rule): Plan: turn a failing program into a working one by finding the cause of each failure, not by guessing.

**18. `debugging` &rarr; `debugging@L4`** (has_level)

- **Exact edge logic:** debugging -&gt; L4 (Extended abstract): the answer reasons beyond the given code (3 ways).
  - **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `TrialAndErrorDebugging`: Conservation: a correct fix removes the cause for the whole class of inputs that failed, and changes nothing for inputs that already worked.
  - **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): When a program fails: reproduce the failure, print or trace intermediate values to find where they first go wrong, fix that, and re-run all the tests.
  - **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: Find the cause before changing code. Kind: logic error. Trigger class: changes are made at random until one test passes, so the bug survives for other inputs or a new bug is added

**19. `topic1.3.f` &rarr; `debugging`** (contains)

- topic `topic1.3.f` contains `debugging`

**20. `topic1.3.f` &rarr; `accumulator_pattern`** (contains)

- topic `topic1.3.f` contains `accumulator_pattern`

**21. `topic1.3.f` &rarr; `convergence_test`** (contains)

- topic `topic1.3.f` contains `convergence_test`

**22. `topic1.3.f` &rarr; `counter_pattern`** (contains)

- topic `topic1.3.f` contains `counter_pattern`

**23. `topic1.3.f` &rarr; `fencepost_loop`** (contains)

- topic `topic1.3.f` contains `fencepost_loop`

**24. `topic1.3.f` &rarr; `flag_search_loop`** (contains)

- topic `topic1.3.f` contains `flag_search_loop`

**25. `topic1.3.f` &rarr; `loop_performance`** (contains)

- topic `topic1.3.f` contains `loop_performance`

**26. `topic1.3.f` &rarr; `monte_carlo_simulation`** (contains)

- topic `topic1.3.f` contains `monte_carlo_simulation`

**27. `topic1.3.f` &rarr; `number_conversion`** (contains)

- topic `topic1.3.f` contains `number_conversion`

**28. `topic1.3.f` &rarr; `testing`** (contains)

- topic `topic1.3.f` contains `testing`
