# Trace (table of variable values) (`program_trace`)

a table of the values of the variables after each statement, used to check what code does

Section 1.2 1.2 Built-in Types of Data, topic 1.2.a Data types and terminology (literals, identifiers, variables, declarations, assignment, expressions).

![The knowledge graph around program_trace](program_trace.png)

## At a glance

- **Needs first:** `assignment`
- **Leads to:** `testing`
- **Learned alongside:** nothing
- **Misconceptions:** none
- **Errors:** none
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 22 edges around this concept, each explained in the graph's own words.

## What it needs first (1)

A prerequisite edge means the other concept has to be understood before `program_trace`.

### `assignment` comes before `program_trace`

*= stores the computed value of the right side*

A trace records the value each variable holds after each assignment statement runs.

- **Grounding:** book passage
- **How `program_trace` combines with `assignment`:** Each assignment statement produces the next row of the trace, changing exactly the column of the variable on its left-hand side.
- **How `assignment` combines with `program_trace`:** A trace records the value of each variable after each assignment runs, one row per statement.

## What it leads to (1)

These concepts need `program_trace` first.

### `program_trace` comes before `testing`

*running a program on chosen inputs, including boundary and unusual ones, and comparing the output with what it should be*

A test needs an expected result, and the expected result comes from tracing what the program should do, step by step.

- **Grounding:** book passage
- **How `testing` combines with `program_trace`:** The expected output of a test comes from a hand trace of what the program should do for that input.

## Learned alongside (0)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

No parallel edge touches this concept.

## Misconceptions (0)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

The graph has no misconception edge from this concept.

## Errors (0)

An error edge states the rule that gets broken in a program, and the right rule.

The graph has no error edge from this concept.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for Trace (table of variable values): the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to Trace (table of variable values) agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

Trace (table of variable values) -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (1 way).

- **everyday reading** (folk-meaning rule): Folk meaning: code is read like prose or a set of maths equations, all true at once, and 'tracing' means sketching it over. Java (notional machine) rule: statements execute one at a time in order and change variable values, so a trace is a table with one row per executed statement showing each variable's current value.

### L1: Unistructural / atom x text surface

L1 for Trace (table of variable values): the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

Trace (table of variable values) -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

- **names the element** (identity rule): A trace is a table of the values of the program's variables after each statement, used to examine what code does.
- **states the rule** (declarative rule): A trace has one column per variable and one row per executed statement, in execution order; each row shows the value of every variable after that statement, with a declared but unassigned variable shown as undefined.

### L2: Multistructural / block x execution / preoperational

L2 for Trace (table of variable values): the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

Trace (table of variable values) -&gt; L2 (Multistructural): the answer applies the rules of Trace (table of variable values) to every part of the code, in order (3 ways).

- **line by line trace** (operational sequencing rule): Follow the flow of control: take the next statement to execute (re-visiting loop bodies on each pass), evaluate it using the current row's values, and write a new row with the variables it changed; continue until the program ends.
- **output prediction** (evaluation / result rule): The last row gives the final values (and any printed output follows from them): for int t = a; a = b; b = t; starting from a = 1234, b = 99, the final row is a = 99, b = 1234, t = 1234.
- **one step execution** (state-transition rule): Each row differs from the previous one only in the variable(s) assigned by that statement; all other columns are copied unchanged.

### L3: Relational / relations x function (concrete operational begins)

L3 for Trace (table of variable values): the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

Trace (table of variable values) -&gt; L3 (Relational): the answer relates the parts (3 ways).

- **relation to neighbour** (composition rule (with a neighbour)): Each assignment statement produces the next row of the trace, changing exactly the column of the variable on its left-hand side.
- **relation to neighbour** (composition rule (with a neighbour)): A test needs an expected result, and the expected result comes from tracing what the program should do, step by step.
- **purpose of the whole** (plan / role rule): Used to check or discover what a piece of code does (e.g. convince yourself that three statements swap a and b) and to debug; tracing a few rows often reveals the purpose of the whole.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for Trace (table of variable values): the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

Trace (table of variable values) -&gt; L4 (Extended abstract): the answer reasons beyond the given code (3 ways).

- **predict a change** (conservation rule): A trace shows the effect of a change: reordering the swap's statements (int t = a; b = t; a = b;) produces a different final row in which both variables hold the original a; the trace of the correct swap keeps the invariant that the old value of a is saved in t before a is overwritten.
- **transfer to a new program** (applicability rule): Trace small or unfamiliar code, loops and suspected bugs by hand; for larger programs, reason about what the parts compute (roles, invariants) or let the program print its variables, since a mental trace can hold only a few values at once.
- **diagnose an error** (error rule): rule broken: Each row must be computed from the current values, in execution order. Kind: silent logic error. Trigger class: Long traces or loops that overload working memory: stale or wrong values carried into later rows, giving a wrong predicted output.

## Same topic

`program_trace` belongs to the topic **Data types and terminology (literals, identifiers, variables, declarations, assignment, expressions)** (`topic1.2.a`). The topic also contains: `assignment`, `chained_assignment`, `data_type`, `declaration`, `definite_assignment`, `expression`, `identifier`, `literal`, `named_constants`, `naming_convention`, `operator_precedence`, `primitive_type`, `variable`, `variable_swap`.

## Rules of the concept (12)

- **folk-meaning rule:** Folk meaning: code is read like prose or a set of maths equations, all true at once, and 'tracing' means sketching it over. Java (notional machine) rule: statements execute one at a time in order and change variable values, so a trace is a table with one row per executed statement showing each variable's current value.
- **uneven-application rule:** Points to LT (one row per executed statement, in execution order, computed from the previous row's values). Applied unevenly: the student uses a stale or wrong value of a variable in some rows, skips rows for repeated loop passes, or records a value change that the statement did not make.
- **identity rule:** A trace is a table of the values of the program's variables after each statement, used to examine what code does.
- **declarative rule:** A trace has one column per variable and one row per executed statement, in execution order; each row shows the value of every variable after that statement, with a declared but unassigned variable shown as undefined.
- **operational sequencing rule:** Follow the flow of control: take the next statement to execute (re-visiting loop bodies on each pass), evaluate it using the current row's values, and write a new row with the variables it changed; continue until the program ends.
- **evaluation / result rule:** The last row gives the final values (and any printed output follows from them): for int t = a; a = b; b = t; starting from a = 1234, b = 99, the final row is a = 99, b = 1234, t = 1234.
- **state-transition rule:** Each row differs from the previous one only in the variable(s) assigned by that statement; all other columns are copied unchanged.
- **composition rule (with a neighbour):** with assignment: Each assignment statement produces the next row of the trace, changing exactly the column of the variable on its left-hand side.
- **plan / role rule:** Used to check or discover what a piece of code does (e.g. convince yourself that three statements swap a and b) and to debug; tracing a few rows often reveals the purpose of the whole.
- **conservation rule:** A trace shows the effect of a change: reordering the swap's statements (int t = a; b = t; a = b;) produces a different final row in which both variables hold the original a; the trace of the correct swap keeps the invariant that the old value of a is saved in t before a is overwritten.
- **error rule:** rule broken: Each row must be computed from the current values, in execution order. (silent logic error)
- **applicability rule:** Trace small or unfamiliar code, loops and suspected bugs by hand; for larger programs, reason about what the parts compute (roles, invariants) or let the program print its variables, since a mental trace can hold only a few values at once.

## The whole prerequisite chain

- **Everything it builds on (7):** `assignment`, `data_type`, `declaration`, `identifier`, `literal`, `primitive_type`, `variable`
- **Everything that builds on it (2):** `debugging`, `testing`
