# switch_statement (`switch_statement`)

switch (x) { case v: ...; break; default: ... }

Section 1.3 Conditionals and Loops, topic 1.3.g Other conditional and loop constructs (break, continue, switch, do-while, ?:).

![The knowledge graph around switch_statement](switch_statement.png)

## At a glance

- **Needs first:** `break_statement`, `control_flow`
- **Leads to:** nothing
- **Learned alongside:** `else_if_chain`, `nested_conditionals`
- **Misconceptions:** `SwitchNoFallThrough`
- **Errors:** none
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 16 edges around this concept, each explained in the graph's own words.

## What it needs first (2)

A prerequisite edge means the other concept has to be understood before `switch_statement`.

### `break_statement` comes before `switch_statement`

*break -- immediately exits the innermost loop or switch*

Each case of a switch normally ends with break, which exits the switch body.

- **Grounding:** book passage
- **How `switch_statement` combines with `break_statement`:** Each case is normally ended by break, which exits the switch body. Leaving it out makes that case fall into the next. Inside a loop, that break exits the switch, not the loop.
- **How `break_statement` combines with `switch_statement`:** In a switch, break ends the switch body; without it, execution falls through into the next case. A break inside a switch that is inside a loop exits only the switch, not the loop.

### `control_flow` comes before `switch_statement`

*the order in which statements are executed*

switch directs the flow of control to one of several case labels, depending on the value of one expression.

- **Grounding:** book passage

## What it leads to (0)

These concepts need `switch_statement` first.

No concept has this one as a prerequisite.

## Learned alongside (2)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

### `switch_statement` alongside `else_if_chain`

*if ... else if ... else picks exactly one branch*

Both pick one of several alternatives. A switch compares one value with constant case labels and falls through without break; an else-if chain tests each condition in turn and runs only the first true branch.

- **Grounding:** book passage

### `switch_statement` alongside `nested_conditionals`

*else-if chains and conditionals inside conditionals*

When there are more than two mutually exclusive alternatives, a chain of if-else statements works, but a switch statement provides a direct solution that evaluates one expression against many possible values.

- **Grounding:** book passage
- **How `switch_statement` combines with `nested_conditionals`:** A switch replaces an if-else chain only when every test is \`expr == constant\` on the same expression. Range tests such as the income-bracket chain (\`income &lt; 47450\`) must stay an if-else chain.
- **How `nested_conditionals` combines with `switch_statement`:** For more than two mutually exclusive alternatives a chain of if-else statements works, but a switch tests one expression against many values directly.

## Misconceptions (1)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### SwitchNoFallThrough

- **Wrong rule:** After the matching case runs, the switch ends even without break.
- **Right rule:** Without break, statements in switch blocks fall through into the following cases.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: After the matching case runs, the switch ends even without break. Right rule: Without break, all the statements after the matching label run, including those under later case labels, until a break or the end of the switch.
- **Shows at level L0 as:** inconsistent trace: Applies the LT rule unevenly: on a trace the selector is matched correctly but execution stops at the next case label on some runs and falls through on others, or default is run even though a case matched. (here mixing in: "After the matching case runs, the switch ends even without break")

## Errors (0)

An error edge states the rule that gets broken in a program, and the right rule.

The graph has no error edge from this concept.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for switch statement: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to switch statement agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

switch statement -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (3 ways).

- **everyday reading** (folk-meaning rule): Folk meaning: everyday 'switch' means flip to one setting, and 'case' reads like 'in case of X do Y', a self-contained rule. Novices therefore expect only the matching case to run. In a Java switch statement, the case labels are only entry points: execution starts at the matching label and falls through the following cases until a break.
- **misconception** (wrong rule / right rule; shows `SwitchNoFallThrough`): wrong rule: After the matching case runs, the switch ends even without break. Right rule: Without break, all the statements after the matching label run, including those under later case labels, until a break or the end of the switch.
- **inconsistent trace** (uneven-application rule; shows `SwitchNoFallThrough`): Applies the LT rule unevenly: on a trace the selector is matched correctly but execution stops at the next case label on some runs and falls through on others, or default is run even though a case matched. (here mixing in: "After the matching case runs, the switch ends even without break")

### L1: Unistructural / atom x text surface

L1 for switch statement: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

switch statement -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

- **names the element** (identity rule): Selection statement: \`switch (expr) { case v1: ...; break; ... default: ... }\` chooses among many alternatives by the value of one expression.
- **states the rule** (declarative rule): The selector is an int-like (char, byte, short, int), String or enum expression. Case labels are distinct constants of that type, and default is optional. Control jumps to the matching label (or to default, or past the switch), and the case statements usually end with break. Without a break, execution falls through into the statements of the next case; default runs when no case matches.

### L2: Multistructural / block x execution / preoperational

L2 for switch statement: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

switch statement -&gt; L2 (Multistructural): the answer applies the rules of switch statement to every part of the code, in order (3 ways).

- **line by line trace** (operational sequencing rule): Order: evaluate the selector once; compare it with the case constants; jump to the matching label (else default, else skip the switch). Then execute the statements from there in order, through later labels, until a break or the closing brace.
- **output prediction** (evaluation / result rule): A switch statement has no value. Its result is the effect of the case(s) run: with \`day = 3\`, the S&amp;W day switch prints Wed. Without breaks, day = 5 would print Fri, then Sat.
- **one step execution** (state-transition rule): One execution evaluates the selector once (any side effect in it happens once) and runs the statements of one entry point and any cases it falls into. It changes only what those statements change.

### L3: Relational / relations x function (concrete operational begins)

L3 for switch statement: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

switch statement -&gt; L3 (Relational): the answer relates the parts (3 ways).

- **relation to neighbour** (composition rule (with a neighbour)): A switch replaces an if-else chain only when every test is \`expr == constant\` on the same expression. Range tests such as the income-bracket chain (\`income &lt; 47450\`) must stay an if-else chain.
- **relation to neighbour** (composition rule (with a neighbour)): Each case is normally ended by break, which exits the switch body. Leaving it out makes that case fall into the next. Inside a loop, that break exits the switch, not the loop.
- **purpose of the whole** (plan / role rule): Plan: multiway dispatch or lookup. It maps one discrete value (day number, menu choice, character) to one of several actions or results. Grouped labels (\`case "apple": case "banana":\`) map several values to one action.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for switch statement: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

switch statement -&gt; L4 (Extended abstract): the answer reasons beyond the given code (6 ways).

- **predict a change** (conservation rule; shows `SwitchNoFallThrough`): When every case ends with break, reordering the cases does not change behaviour (labels are distinct constants). Removing one break changes behaviour for that value only. Adding a default changes only values with no matching label.
- **transfer to a new program** (applicability rule): Use switch for more than two mutually exclusive alternatives decided by equality of one int, char, String or enum value. Use an if-else chain for ranges, doubles or unrelated conditions. Use an array lookup (S&amp;W 1.4) when each case only selects a value.
- **diagnose an error** (error rule): rule broken: Without break, execution falls through into the following cases. Kind: silent logic error. Trigger class: Any selector value whose case lacks a break: the following cases' statements also run (e.g. both Fri and Sat printed).
- **diagnose an error** (error rule): rule broken: Values that match no case do nothing unless a default is present. Kind: silent logic error. Trigger class: An out-of-range selector (day = 7) with no default: nothing happens, and a variable assigned only in the cases may stay unassigned.
- **diagnose an error** (error rule): rule broken: Case labels must be distinct compile-time constants of the selector type, and the selector may not be double, float, long or boolean. Kind: compile-time. Trigger class: Duplicate \`case 1:\` labels, a variable as a label, or \`switch (x)\` with x a double.
- **diagnose an error** (error rule): rule broken: A String selector is dereferenced. Kind: run-time exception. Trigger class: Switching on a String variable that is null throws NullPointerException.

## Same topic

`switch_statement` belongs to the topic **Other conditional and loop constructs (break, continue, switch, do-while, ?:)** (`topic1.3.g`). The topic also contains: `break_statement`, `conditional_operator`, `continue_statement`, `do_while_loop`, `labeled_break`.

## Rules of the concept (17)

- **folk-meaning rule:** Folk meaning: everyday 'switch' means flip to one setting, and 'case' reads like 'in case of X do Y', a self-contained rule. Novices therefore expect only the matching case to run. In a Java switch statement, the case labels are only entry points: execution starts at the matching label and falls through the following cases until a break.
- **wrong rule / right rule:** SwitchNoFallThrough: wrong: After the matching case runs, the switch ends even without break. \| right: Without break, all the statements after the matching label run, including those under later case labels, until a break or the end of the switch.
- **uneven-application rule:** Applies the LT rule unevenly: on a trace the selector is matched correctly but execution stops at the next case label on some runs and falls through on others, or default is run even though a case matched.
- **identity rule:** Selection statement: \`switch (expr) { case v1: ...; break; ... default: ... }\` chooses among many alternatives by the value of one expression.
- **declarative rule:** The selector is an int-like (char, byte, short, int), String or enum expression. Case labels are distinct constants of that type, and default is optional. Control jumps to the matching label (or to default, or past the switch), and the case statements usually end with break. Without a break, execution falls through into the statements of the next case; default runs when no case matches.
- **operational sequencing rule:** Order: evaluate the selector once; compare it with the case constants; jump to the matching label (else default, else skip the switch). Then execute the statements from there in order, through later labels, until a break or the closing brace.
- **evaluation / result rule:** A switch statement has no value. Its result is the effect of the case(s) run: with \`day = 3\`, the S&amp;W day switch prints Wed. Without breaks, day = 5 would print Fri, then Sat.
- **state-transition rule:** One execution evaluates the selector once (any side effect in it happens once) and runs the statements of one entry point and any cases it falls into. It changes only what those statements change.
- **composition rule (with a neighbour):** with nested\_conditionals: A switch replaces an if-else chain only when every test is \`expr == constant\` on the same expression. Range tests such as the income-bracket chain (\`income &lt; 47450\`) must stay an if-else chain.
- **composition rule (with a neighbour):** with break\_statement: Each case is normally ended by break, which exits the switch body. Leaving it out makes that case fall into the next. Inside a loop, that break exits the switch, not the loop.
- **plan / role rule:** Plan: multiway dispatch or lookup. It maps one discrete value (day number, menu choice, character) to one of several actions or results. Grouped labels (\`case "apple": case "banana":\`) map several values to one action.
- **conservation rule:** When every case ends with break, reordering the cases does not change behaviour (labels are distinct constants). Removing one break changes behaviour for that value only. Adding a default changes only values with no matching label.
- **error rule:** rule broken: Without break, execution falls through into the following cases. (silent logic error)
- **error rule:** rule broken: Values that match no case do nothing unless a default is present. (silent logic error)
- **error rule:** rule broken: Case labels must be distinct compile-time constants of the selector type, and the selector may not be double, float, long or boolean. (compile-time)
- **error rule:** rule broken: A String selector is dereferenced. (run-time exception)
- **applicability rule:** Use switch for more than two mutually exclusive alternatives decided by equality of one int, char, String or enum value. Use an if-else chain for ranges, doubles or unrelated conditions. Use an array lookup (S&amp;W 1.4) when each case only selects a value.

## The whole prerequisite chain

- **Everything it builds on (22):** `arithmetic_operators`, `boolean`, `boolean_expression`, `break_statement`, `class_declaration`, `comparison_operators`, `control_flow`, `data_type`, `do_while_loop`, `expression`, `for_loop`, `identifier`, `literal`, `logical_operators`, `loop_control`, `loop_variable`, `main_method`, `primitive_type`, `program_text`, `statement`, `variable`, `while_loop`
- **Everything that builds on it (0):** nothing
