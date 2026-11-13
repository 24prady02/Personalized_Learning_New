# Program state (`program_state`)

the information needed to know what a program will do next: the values of its variables and array entries and the next statement

Section 1.4 1.4 Arrays, topic 1.4.b Memory representation and bounds checking.

![The knowledge graph around program_state](program_state.png)

## At a glance

- **Needs first:** `variable`
- **Leads to:** nothing
- **Learned alongside:** nothing
- **Misconceptions:** `StateChangeIgnoredAcrossPasses`
- **Errors:** none
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 17 edges around this concept. The edge logic, the wrong and right rules and the exact rules of the ways are copied word for word from the graph.

## To work on (2)

- no code pattern or signal: the code cannot tag this concept
- no aliases: a student's words cannot name this concept

## What it needs first (1)

A prerequisite edge means the other concept has to be understood before `program_state`.

### `variable` comes before `program_state`

*a named, typed box that holds a value*

- **Edge:** `pre:variable->program_state`
- **Exact edge logic:** Without arrays, a program's state is the values of its variables plus the next statement to run.
- **Grounding:** book\_passage
- **Composition rule (R) of `program_state` with `variable`:** Without arrays the state is the values of the variables plus the next statement; each array element adds one more variable to the state.
- **Composition rule (R) of `variable` with `program_state`:** The current values of all variables make up the program's state. A trace records each variable's value after each statement.

## What it leads to (0)

These concepts need `program_state` first.

No concept has this one as a prerequisite.

## Learned alongside (0)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

No parallel edge touches this concept.

## Misconceptions (1)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### StateChangeIgnoredAcrossPasses

- **Edge:** `program_state` &rarr; `StateChangeIgnoredAcrossPasses` (misconception)
- **Exact edge logic (the wrong rule):** Values changed by one pass of a loop (other than the loop variable) do not affect later passes.
- **Twin logic (the right rule):** Each pass starts from the state left by the previous pass, so a change in one pass carries into the next ones.
- **Wrong belief (on the node):** Values changed by one pass of a loop (other than the loop variable) do not affect later passes.
- **Correct rule (on the node):** Each pass starts from the state left by the previous pass, so a change in one pass carries into the next ones.
- **Provenance:** published
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [1] misconception, exact rule:** wrong rule: Values changed by one pass of a loop (other than the loop variable) do not affect later passes. Right rule: Each pass starts from the state left by the previous pass, so a change in one pass carries into the next ones.
- **Edge `accumulator_pattern` &rarr; `StateChangeIgnoredAcrossPasses`, exact edge logic:** Values changed by one pass of a loop (other than the loop variable) do not affect later passes. **Twin logic:** Each pass starts from the state left by the previous pass, so a change in one pass carries into the next ones. (role: context)
- **Edge `loop_body` &rarr; `StateChangeIgnoredAcrossPasses`, exact edge logic:** Values changed by one pass of a loop (other than the loop variable) do not affect later passes. **Twin logic:** Each pass starts from the state left by the previous pass, so a change in one pass carries into the next ones. (role: primary)

## Errors (0)

An error edge states the rule that gets broken in a program, and the right rule.

The graph has no error edge from this concept.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for Program state: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to Program state agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

- **Edge:** `program_state` &rarr; `program_state@L0` (has_level)
- **Exact edge logic:** Program state -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (2 ways).

Ways (2), each with its exact rule:

- **[0] everyday\_reading** (rule type E, folk-meaning rule): Folk meaning: program statements read like maths equations, timeless relations among values. Java rule: each statement changes the state (the values of variables and array entries), and the next statement starts from the changed state.
- **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `StateChangeIgnoredAcrossPasses`: wrong rule: Values changed by one pass of a loop (other than the loop variable) do not affect later passes. Right rule: Each pass starts from the state left by the previous pass, so a change in one pass carries into the next ones.

### L1: Unistructural / atom x text surface

L1 for Program state: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

- **Edge:** `program_state` &rarr; `program_state@L1` (has_level)
- **Exact edge logic:** Program state -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

Ways (2), each with its exact rule:

- **[0] names\_the\_element** (rule type N, identity rule): Identity: the state of a program is the information needed to know what it will do next: the values of its variables (and array entries) and which statement runs next.
- **[1] states\_the\_rule** (rule type S, declarative rule): Declarative: in a program without arrays, knowing the variable values and the next statement determines what the program does next; arrays add one state component per element.

### L2: Multistructural / block x execution / preoperational

L2 for Program state: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

- **Edge:** `program_state` &rarr; `program_state@L2` (has_level)
- **Exact edge logic:** Program state -&gt; L2 (Multistructural): the answer applies the rules of Program state to every part of the code, in order (3 ways).

Ways (3), each with its exact rule:

- **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): Sequencing: statements in a block execute in order, first to last, so the state seen by each statement is the result of all earlier ones.
- **[1] output\_prediction** (rule type OP, evaluation / result rule): Result: the output from any point on is determined by the current state; equal states give the same future behaviour (apart from Math.random and input).
- **[2] one\_step\_execution** (rule type OS, state-transition rule): State transition: each assignment changes exactly one variable or one array element; tracing tracks these changes.

### L3: Relational / relations x function (concrete operational begins)

L3 for Program state: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

- **Edge:** `program_state` &rarr; `program_state@L3` (has_level)
- **Exact edge logic:** Program state -&gt; L3 (Relational): the answer relates the parts (2 ways).

Ways (2), each with its exact rule:

- **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Without arrays the state is the values of the variables plus the next statement; each array element adds one more variable to the state.
- **[1] purpose\_of\_the\_whole** (rule type P, plan / role rule): Plan/role: tracing (a trace table of the state after each step) is how programs are understood and debugged; with large arrays one checks invariants among state components instead.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for Program state: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

- **Edge:** `program_state` &rarr; `program_state@L4` (has_level)
- **Exact edge logic:** Program state -&gt; L4 (Extended abstract): the answer reasons beyond the given code (3 ways).

Ways (3), each with its exact rule:

- **[0] predict\_a\_change** (rule type C, conservation rule): Conservation: an invariant such as 'valcnt equals the number of true entries in found[]' holds after every pass; a change that breaks it signals a bug.
- **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Applicability: trace the full state for small programs. When arrays make the state too large to track, reason with invariants and partial traces instead.
- **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: Each pass starts from the state left by the previous one. Kind: silent logic error. Trigger class: an accumulator is not reset between outer passes (sum declared before the row loop), so later rows include earlier rows' totals

## Same topic

`program_state` belongs to the topic **Memory representation and bounds checking** (`topic1.4.b`). The topic also contains: `array_aliasing`, `array_bounds`, `array_copy`, `array_reference`, `loop_guard`, `primitive_vs_reference`, `printing_array_reference`.

## Rules of the concept (13)

- **Book** (SW-1e, p. 111 (pdf 121)): "The state of a program can be defined as the information you need to know to understand what a program is doing."
- **E** (folk-meaning rule): Folk meaning: program statements read like maths equations, timeless relations among values. Java rule: each statement changes the state (the values of variables and array entries), and the next statement starts from the changed state.
- **M** (wrong rule / right rule): StateChangeIgnoredAcrossPasses: wrong: Values changed by one pass of a loop (other than the loop variable) do not affect later passes. \| right: Each pass starts from the state left by the previous pass, so a change in one pass carries into the next ones.
- **T** (uneven-application rule): Points to LT: statements execute one at a time, and each starts from the state the previous one left. Inconsistent application: a trace table updates a variable on some steps but carries a stale value on others.
- **N** (identity rule): Identity: the state of a program is the information needed to know what it will do next: the values of its variables (and array entries) and which statement runs next.
- **S** (declarative rule): Declarative: in a program without arrays, knowing the variable values and the next statement determines what the program does next; arrays add one state component per element.
- **LT** (operational sequencing rule): Sequencing: statements in a block execute in order, first to last, so the state seen by each statement is the result of all earlier ones.
- **OP** (evaluation / result rule): Result: the output from any point on is determined by the current state; equal states give the same future behaviour (apart from Math.random and input).
- **OS** (state-transition rule): State transition: each assignment changes exactly one variable or one array element; tracing tracks these changes.
- **R** (composition rule (with a neighbour)): with variable: Without arrays the state is the values of the variables plus the next statement; each array element adds one more variable to the state.
- **P** (plan / role rule): Plan/role: tracing (a trace table of the state after each step) is how programs are understood and debugged; with large arrays one checks invariants among state components instead.
- **C** (conservation rule): Conservation: an invariant such as 'valcnt equals the number of true entries in found[]' holds after every pass; a change that breaks it signals a bug.
- **D** (error rule): rule broken: Each pass starts from the state left by the previous one. (silent logic error)
- **X** (applicability rule): Applicability: trace the full state for small programs. When arrays make the state too large to track, reason with invariants and partial traces instead.

## How it is found in code and answers (reader block)

- **Aliases:** none
- **Code patterns:** none
- **Operator symbols:** none
- **Java types:** none

## The whole prerequisite chain

- **Everything it builds on (5):** `data_type`, `identifier`, `literal`, `primitive_type`, `variable`
- **Everything that builds on it (0):** nothing

## Every edge in this view and its exact edge logic (17)

All the edges drawn in the picture, in the order: prerequisite, parallel, misconception, error, has_level, contains.

**1. `variable` &rarr; `program_state`** (prerequisite)

- **Exact edge logic:** Without arrays, a program's state is the values of its variables plus the next statement to run.
- **Grounding:** book\_passage
- **Composition rule (R) of `variable` with `program_state`:** The current values of all variables make up the program's state. A trace records each variable's value after each statement.
- **Composition rule (R) of `program_state` with `variable`:** Without arrays the state is the values of the variables plus the next statement; each array element adds one more variable to the state.

**2. `program_state` &rarr; `StateChangeIgnoredAcrossPasses`** (misconception)

- **Exact edge logic (the wrong rule):** Values changed by one pass of a loop (other than the loop variable) do not affect later passes.
- **Twin logic (the right rule):** Each pass starts from the state left by the previous pass, so a change in one pass carries into the next ones.
- **Role:** context

**3. `accumulator_pattern` &rarr; `StateChangeIgnoredAcrossPasses`** (misconception)

- **Exact edge logic (the wrong rule):** Values changed by one pass of a loop (other than the loop variable) do not affect later passes.
- **Twin logic (the right rule):** Each pass starts from the state left by the previous pass, so a change in one pass carries into the next ones.
- **Role:** context

**4. `loop_body` &rarr; `StateChangeIgnoredAcrossPasses`** (misconception)

- **Exact edge logic (the wrong rule):** Values changed by one pass of a loop (other than the loop variable) do not affect later passes.
- **Twin logic (the right rule):** Each pass starts from the state left by the previous pass, so a change in one pass carries into the next ones.
- **Role:** primary

**5. `program_state` &rarr; `program_state@L0`** (has_level)

- **Exact edge logic:** Program state -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (2 ways).
  - **[0] everyday\_reading** (rule type E, folk-meaning rule): Folk meaning: program statements read like maths equations, timeless relations among values. Java rule: each statement changes the state (the values of variables and array entries), and the next statement starts from the changed state.
  - **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `StateChangeIgnoredAcrossPasses`: wrong rule: Values changed by one pass of a loop (other than the loop variable) do not affect later passes. Right rule: Each pass starts from the state left by the previous pass, so a change in one pass carries into the next ones.

**6. `program_state` &rarr; `program_state@L1`** (has_level)

- **Exact edge logic:** Program state -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).
  - **[0] names\_the\_element** (rule type N, identity rule): Identity: the state of a program is the information needed to know what it will do next: the values of its variables (and array entries) and which statement runs next.
  - **[1] states\_the\_rule** (rule type S, declarative rule): Declarative: in a program without arrays, knowing the variable values and the next statement determines what the program does next; arrays add one state component per element.

**7. `program_state` &rarr; `program_state@L2`** (has_level)

- **Exact edge logic:** Program state -&gt; L2 (Multistructural): the answer applies the rules of Program state to every part of the code, in order (3 ways).
  - **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): Sequencing: statements in a block execute in order, first to last, so the state seen by each statement is the result of all earlier ones.
  - **[1] output\_prediction** (rule type OP, evaluation / result rule): Result: the output from any point on is determined by the current state; equal states give the same future behaviour (apart from Math.random and input).
  - **[2] one\_step\_execution** (rule type OS, state-transition rule): State transition: each assignment changes exactly one variable or one array element; tracing tracks these changes.

**8. `program_state` &rarr; `program_state@L3`** (has_level)

- **Exact edge logic:** Program state -&gt; L3 (Relational): the answer relates the parts (2 ways).
  - **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Without arrays the state is the values of the variables plus the next statement; each array element adds one more variable to the state.
  - **[1] purpose\_of\_the\_whole** (rule type P, plan / role rule): Plan/role: tracing (a trace table of the state after each step) is how programs are understood and debugged; with large arrays one checks invariants among state components instead.

**9. `program_state` &rarr; `program_state@L4`** (has_level)

- **Exact edge logic:** Program state -&gt; L4 (Extended abstract): the answer reasons beyond the given code (3 ways).
  - **[0] predict\_a\_change** (rule type C, conservation rule): Conservation: an invariant such as 'valcnt equals the number of true entries in found[]' holds after every pass; a change that breaks it signals a bug.
  - **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Applicability: trace the full state for small programs. When arrays make the state too large to track, reason with invariants and partial traces instead.
  - **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: Each pass starts from the state left by the previous one. Kind: silent logic error. Trigger class: an accumulator is not reset between outer passes (sum declared before the row loop), so later rows include earlier rows' totals

**10. `topic1.4.b` &rarr; `program_state`** (contains)

- topic `topic1.4.b` contains `program_state`

**11. `topic1.4.b` &rarr; `array_aliasing`** (contains)

- topic `topic1.4.b` contains `array_aliasing`

**12. `topic1.4.b` &rarr; `array_bounds`** (contains)

- topic `topic1.4.b` contains `array_bounds`

**13. `topic1.4.b` &rarr; `array_copy`** (contains)

- topic `topic1.4.b` contains `array_copy`

**14. `topic1.4.b` &rarr; `array_reference`** (contains)

- topic `topic1.4.b` contains `array_reference`

**15. `topic1.4.b` &rarr; `loop_guard`** (contains)

- topic `topic1.4.b` contains `loop_guard`

**16. `topic1.4.b` &rarr; `primitive_vs_reference`** (contains)

- topic `topic1.4.b` contains `primitive_vs_reference`

**17. `topic1.4.b` &rarr; `printing_array_reference`** (contains)

- topic `topic1.4.b` contains `printing_array_reference`
