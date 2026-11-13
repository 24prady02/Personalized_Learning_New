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

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 16 edges around this concept. The edge logic, the wrong and right rules and the exact rules of the ways are copied word for word from the graph.

## To work on (0)

Nothing is missing for this concept.

## What it needs first (2)

A prerequisite edge means the other concept has to be understood before `switch_statement`.

### `break_statement` comes before `switch_statement`

*break -- immediately exits the innermost loop or switch*

- **Edge:** `pre:break_statement->switch_statement`
- **Exact edge logic:** Each case of a switch normally ends with break, which exits the switch body.
- **Grounding:** book\_passage
- **Composition rule (R) of `switch_statement` with `break_statement`:** Each case is normally ended by break, which exits the switch body. Leaving it out makes that case fall into the next. Inside a loop, that break exits the switch, not the loop.
- **Composition rule (R) of `break_statement` with `switch_statement`:** In a switch, break ends the switch body; without it, execution falls through into the next case. A break inside a switch that is inside a loop exits only the switch, not the loop.

### `control_flow` comes before `switch_statement`

*the order in which statements are executed*

- **Edge:** `pre:control_flow->switch_statement`
- **Exact edge logic:** switch directs the flow of control to one of several case labels, depending on the value of one expression.
- **Grounding:** book\_passage

## What it leads to (0)

These concepts need `switch_statement` first.

No concept has this one as a prerequisite.

## Learned alongside (2)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

### `switch_statement` alongside `else_if_chain`

*if ... else if ... else picks exactly one branch*

- **Edge:** `par:switch_statement~else_if_chain`
- **Exact edge logic:** Both pick one of several alternatives. A switch compares one value with constant case labels and falls through without break; an else-if chain tests each condition in turn and runs only the first true branch.
- **Grounding:** book\_passage

### `switch_statement` alongside `nested_conditionals`

*else-if chains and conditionals inside conditionals*

- **Edge:** `par:nested_conditionals~switch_statement`
- **Exact edge logic:** When there are more than two mutually exclusive alternatives, a chain of if-else statements works, but a switch statement provides a direct solution that evaluates one expression against many possible values.
- **Grounding:** book\_passage
- **Composition rule (R) of `switch_statement` with `nested_conditionals`:** A switch replaces an if-else chain only when every test is \`expr == constant\` on the same expression. Range tests such as the income-bracket chain (\`income &lt; 47450\`) must stay an if-else chain.
- **Composition rule (R) of `nested_conditionals` with `switch_statement`:** For more than two mutually exclusive alternatives a chain of if-else statements works, but a switch tests one expression against many values directly.

## Misconceptions (1)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### SwitchNoFallThrough

- **Edge:** `switch_statement` &rarr; `SwitchNoFallThrough` (misconception)
- **Exact edge logic (the wrong rule):** After the matching case runs, the switch ends even without break.
- **Twin logic (the right rule):** Without break, statements in switch blocks fall through into the following cases.
- **Wrong belief (on the node):** After the matching case runs, the switch ends even without break.
- **Correct rule (on the node):** Without break, statements in switch blocks fall through into the following cases.
- **Provenance:** textbook
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [1] misconception, exact rule:** wrong rule: After the matching case runs, the switch ends even without break. Right rule: Without break, all the statements after the matching label run, including those under later case labels, until a break or the end of the switch.
- **L0 way [2] inconsistent\_trace, exact rule:** Applies the LT rule unevenly: on a trace the selector is matched correctly but execution stops at the next case label on some runs and falls through on others, or default is run even though a case matched. (here mixing in: "After the matching case runs, the switch ends even without break")

## Errors (0)

An error edge states the rule that gets broken in a program, and the right rule.

The graph has no error edge from this concept.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for switch statement: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to switch statement agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

- **Edge:** `switch_statement` &rarr; `switch_statement@L0` (has_level)
- **Exact edge logic:** switch statement -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (3 ways).

Ways (3), each with its exact rule:

- **[0] everyday\_reading** (rule type E, folk-meaning rule): Folk meaning: everyday 'switch' means flip to one setting, and 'case' reads like 'in case of X do Y', a self-contained rule. Novices therefore expect only the matching case to run. In a Java switch statement, the case labels are only entry points: execution starts at the matching label and falls through the following cases until a break.
- **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `SwitchNoFallThrough`: wrong rule: After the matching case runs, the switch ends even without break. Right rule: Without break, all the statements after the matching label run, including those under later case labels, until a break or the end of the switch.
- **[2] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `SwitchNoFallThrough`: Applies the LT rule unevenly: on a trace the selector is matched correctly but execution stops at the next case label on some runs and falls through on others, or default is run even though a case matched. (here mixing in: "After the matching case runs, the switch ends even without break")

### L1: Unistructural / atom x text surface

L1 for switch statement: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

- **Edge:** `switch_statement` &rarr; `switch_statement@L1` (has_level)
- **Exact edge logic:** switch statement -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

Ways (2), each with its exact rule:

- **[0] names\_the\_element** (rule type N, identity rule): Selection statement: \`switch (expr) { case v1: ...; break; ... default: ... }\` chooses among many alternatives by the value of one expression.
- **[1] states\_the\_rule** (rule type S, declarative rule): The selector is an int-like (char, byte, short, int), String or enum expression. Case labels are distinct constants of that type, and default is optional. Control jumps to the matching label (or to default, or past the switch), and the case statements usually end with break. Without a break, execution falls through into the statements of the next case; default runs when no case matches.

### L2: Multistructural / block x execution / preoperational

L2 for switch statement: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

- **Edge:** `switch_statement` &rarr; `switch_statement@L2` (has_level)
- **Exact edge logic:** switch statement -&gt; L2 (Multistructural): the answer applies the rules of switch statement to every part of the code, in order (3 ways).

Ways (3), each with its exact rule:

- **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): Order: evaluate the selector once; compare it with the case constants; jump to the matching label (else default, else skip the switch). Then execute the statements from there in order, through later labels, until a break or the closing brace.
- **[1] output\_prediction** (rule type OP, evaluation / result rule): A switch statement has no value. Its result is the effect of the case(s) run: with \`day = 3\`, the S&amp;W day switch prints Wed. Without breaks, day = 5 would print Fri, then Sat.
- **[2] one\_step\_execution** (rule type OS, state-transition rule): One execution evaluates the selector once (any side effect in it happens once) and runs the statements of one entry point and any cases it falls into. It changes only what those statements change.

### L3: Relational / relations x function (concrete operational begins)

L3 for switch statement: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

- **Edge:** `switch_statement` &rarr; `switch_statement@L3` (has_level)
- **Exact edge logic:** switch statement -&gt; L3 (Relational): the answer relates the parts (3 ways).

Ways (3), each with its exact rule:

- **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): A switch replaces an if-else chain only when every test is \`expr == constant\` on the same expression. Range tests such as the income-bracket chain (\`income &lt; 47450\`) must stay an if-else chain.
- **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Each case is normally ended by break, which exits the switch body. Leaving it out makes that case fall into the next. Inside a loop, that break exits the switch, not the loop.
- **[2] purpose\_of\_the\_whole** (rule type P, plan / role rule): Plan: multiway dispatch or lookup. It maps one discrete value (day number, menu choice, character) to one of several actions or results. Grouped labels (\`case "apple": case "banana":\`) map several values to one action.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for switch statement: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

- **Edge:** `switch_statement` &rarr; `switch_statement@L4` (has_level)
- **Exact edge logic:** switch statement -&gt; L4 (Extended abstract): the answer reasons beyond the given code (6 ways).

Ways (6), each with its exact rule:

- **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `SwitchNoFallThrough`: When every case ends with break, reordering the cases does not change behaviour (labels are distinct constants). Removing one break changes behaviour for that value only. Adding a default changes only values with no matching label.
- **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Use switch for more than two mutually exclusive alternatives decided by equality of one int, char, String or enum value. Use an if-else chain for ranges, doubles or unrelated conditions. Use an array lookup (S&amp;W 1.4) when each case only selects a value.
- **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: Without break, execution falls through into the following cases. Kind: silent logic error. Trigger class: Any selector value whose case lacks a break: the following cases' statements also run (e.g. both Fri and Sat printed).
- **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: Values that match no case do nothing unless a default is present. Kind: silent logic error. Trigger class: An out-of-range selector (day = 7) with no default: nothing happens, and a variable assigned only in the cases may stay unassigned.
- **[4] diagnose\_an\_error** (rule type D, error rule): rule broken: Case labels must be distinct compile-time constants of the selector type, and the selector may not be double, float, long or boolean. Kind: compile-time. Trigger class: Duplicate \`case 1:\` labels, a variable as a label, or \`switch (x)\` with x a double.
- **[5] diagnose\_an\_error** (rule type D, error rule): rule broken: A String selector is dereferenced. Kind: run-time exception. Trigger class: Switching on a String variable that is null throws NullPointerException.

## Same topic

`switch_statement` belongs to the topic **Other conditional and loop constructs (break, continue, switch, do-while, ?:)** (`topic1.3.g`). The topic also contains: `break_statement`, `conditional_operator`, `continue_statement`, `do_while_loop`, `labeled_break`.

## Rules of the concept (17)

- **Book** (SW-1e, p. 70 (pdf 80)): "We could use a sequence or a chain of if-else statements, but the Java switch statement provides a direct solution."
- **Book** (OT-Switch, ): "The break statements are necessary because without them, statements in switch blocks fall through:"
- **Book** (OT-Switch, ): "The default section handles all values that are not explicitly handled by one of the case sections."
- **Book** (LI, ): "Once a case is matched, the statements starting from the matched case are executed until a break statement or the end of the switch statement is reached. This is referred to as fall-through behavior."
- **E** (folk-meaning rule): Folk meaning: everyday 'switch' means flip to one setting, and 'case' reads like 'in case of X do Y', a self-contained rule. Novices therefore expect only the matching case to run. In a Java switch statement, the case labels are only entry points: execution starts at the matching label and falls through the following cases until a break.
- **M** (wrong rule / right rule): SwitchNoFallThrough: wrong: After the matching case runs, the switch ends even without break. \| right: Without break, all the statements after the matching label run, including those under later case labels, until a break or the end of the switch.
- **T** (uneven-application rule): Applies the LT rule unevenly: on a trace the selector is matched correctly but execution stops at the next case label on some runs and falls through on others, or default is run even though a case matched.
- **N** (identity rule): Selection statement: \`switch (expr) { case v1: ...; break; ... default: ... }\` chooses among many alternatives by the value of one expression.
- **S** (declarative rule): The selector is an int-like (char, byte, short, int), String or enum expression. Case labels are distinct constants of that type, and default is optional. Control jumps to the matching label (or to default, or past the switch), and the case statements usually end with break. Without a break, execution falls through into the statements of the next case; default runs when no case matches.
- **LT** (operational sequencing rule): Order: evaluate the selector once; compare it with the case constants; jump to the matching label (else default, else skip the switch). Then execute the statements from there in order, through later labels, until a break or the closing brace.
- **OP** (evaluation / result rule): A switch statement has no value. Its result is the effect of the case(s) run: with \`day = 3\`, the S&amp;W day switch prints Wed. Without breaks, day = 5 would print Fri, then Sat.
- **OS** (state-transition rule): One execution evaluates the selector once (any side effect in it happens once) and runs the statements of one entry point and any cases it falls into. It changes only what those statements change.
- **R** (composition rule (with a neighbour)): with nested\_conditionals: A switch replaces an if-else chain only when every test is \`expr == constant\` on the same expression. Range tests such as the income-bracket chain (\`income &lt; 47450\`) must stay an if-else chain.
- **R** (composition rule (with a neighbour)): with break\_statement: Each case is normally ended by break, which exits the switch body. Leaving it out makes that case fall into the next. Inside a loop, that break exits the switch, not the loop.
- **P** (plan / role rule): Plan: multiway dispatch or lookup. It maps one discrete value (day number, menu choice, character) to one of several actions or results. Grouped labels (\`case "apple": case "banana":\`) map several values to one action.
- **C** (conservation rule): When every case ends with break, reordering the cases does not change behaviour (labels are distinct constants). Removing one break changes behaviour for that value only. Adding a default changes only values with no matching label.
- **D** (error rule): rule broken: Without break, execution falls through into the following cases. (silent logic error)
- **D** (error rule): rule broken: Values that match no case do nothing unless a default is present. (silent logic error)
- **D** (error rule): rule broken: Case labels must be distinct compile-time constants of the selector type, and the selector may not be double, float, long or boolean. (compile-time)
- **D** (error rule): rule broken: A String selector is dereferenced. (run-time exception)
- **X** (applicability rule): Use switch for more than two mutually exclusive alternatives decided by equality of one int, char, String or enum value. Use an if-else chain for ranges, doubles or unrelated conditions. Use an array lookup (S&amp;W 1.4) when each case only selects a value.

## How it is found in code and answers (reader block)

- **Aliases:** switch, switch statement
- **Code patterns:** `\bswitch\s*\(`, `\bcase\b[^:;]*:`, `\bdefault\s*:`
- **Operator symbols:** none
- **Java types:** none
- **Signal switch\_fallthrough** (scope program, decisive): `\bcase\b[^:]*:\s*(?:(?!\bbreak\b)[^;{}:])+;\s*(?P<at>case\b|default\b)`

## The whole prerequisite chain

- **Everything it builds on (22):** `arithmetic_operators`, `boolean`, `boolean_expression`, `break_statement`, `class_declaration`, `comparison_operators`, `control_flow`, `data_type`, `do_while_loop`, `expression`, `for_loop`, `identifier`, `literal`, `logical_operators`, `loop_control`, `loop_variable`, `main_method`, `primitive_type`, `program_text`, `statement`, `variable`, `while_loop`
- **Everything that builds on it (0):** nothing

## Every edge in this view and its exact edge logic (16)

All the edges drawn in the picture, in the order: prerequisite, parallel, misconception, error, has_level, contains.

**1. `break_statement` &rarr; `switch_statement`** (prerequisite)

- **Exact edge logic:** Each case of a switch normally ends with break, which exits the switch body.
- **Grounding:** book\_passage
- **Composition rule (R) of `break_statement` with `switch_statement`:** In a switch, break ends the switch body; without it, execution falls through into the next case. A break inside a switch that is inside a loop exits only the switch, not the loop.
- **Composition rule (R) of `switch_statement` with `break_statement`:** Each case is normally ended by break, which exits the switch body. Leaving it out makes that case fall into the next. Inside a loop, that break exits the switch, not the loop.

**2. `control_flow` &rarr; `switch_statement`** (prerequisite)

- **Exact edge logic:** switch directs the flow of control to one of several case labels, depending on the value of one expression.
- **Grounding:** book\_passage

**3. `nested_conditionals` &harr; `switch_statement`** (parallel)

- **Exact edge logic:** When there are more than two mutually exclusive alternatives, a chain of if-else statements works, but a switch statement provides a direct solution that evaluates one expression against many possible values.
- **Grounding:** book\_passage
- **Composition rule (R) of `nested_conditionals` with `switch_statement`:** For more than two mutually exclusive alternatives a chain of if-else statements works, but a switch tests one expression against many values directly.
- **Composition rule (R) of `switch_statement` with `nested_conditionals`:** A switch replaces an if-else chain only when every test is \`expr == constant\` on the same expression. Range tests such as the income-bracket chain (\`income &lt; 47450\`) must stay an if-else chain.

**4. `switch_statement` &harr; `else_if_chain`** (parallel)

- **Exact edge logic:** Both pick one of several alternatives. A switch compares one value with constant case labels and falls through without break; an else-if chain tests each condition in turn and runs only the first true branch.
- **Grounding:** book\_passage

**5. `switch_statement` &rarr; `SwitchNoFallThrough`** (misconception)

- **Exact edge logic (the wrong rule):** After the matching case runs, the switch ends even without break.
- **Twin logic (the right rule):** Without break, statements in switch blocks fall through into the following cases.
- **Role:** primary

**6. `switch_statement` &rarr; `switch_statement@L0`** (has_level)

- **Exact edge logic:** switch statement -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (3 ways).
  - **[0] everyday\_reading** (rule type E, folk-meaning rule): Folk meaning: everyday 'switch' means flip to one setting, and 'case' reads like 'in case of X do Y', a self-contained rule. Novices therefore expect only the matching case to run. In a Java switch statement, the case labels are only entry points: execution starts at the matching label and falls through the following cases until a break.
  - **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `SwitchNoFallThrough`: wrong rule: After the matching case runs, the switch ends even without break. Right rule: Without break, all the statements after the matching label run, including those under later case labels, until a break or the end of the switch.
  - **[2] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `SwitchNoFallThrough`: Applies the LT rule unevenly: on a trace the selector is matched correctly but execution stops at the next case label on some runs and falls through on others, or default is run even though a case matched. (here mixing in: "After the matching case runs, the switch ends even without break")

**7. `switch_statement` &rarr; `switch_statement@L1`** (has_level)

- **Exact edge logic:** switch statement -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).
  - **[0] names\_the\_element** (rule type N, identity rule): Selection statement: \`switch (expr) { case v1: ...; break; ... default: ... }\` chooses among many alternatives by the value of one expression.
  - **[1] states\_the\_rule** (rule type S, declarative rule): The selector is an int-like (char, byte, short, int), String or enum expression. Case labels are distinct constants of that type, and default is optional. Control jumps to the matching label (or to default, or past the switch), and the case statements usually end with break. Without a break, execution falls through into the statements of the next case; default runs when no case matches.

**8. `switch_statement` &rarr; `switch_statement@L2`** (has_level)

- **Exact edge logic:** switch statement -&gt; L2 (Multistructural): the answer applies the rules of switch statement to every part of the code, in order (3 ways).
  - **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): Order: evaluate the selector once; compare it with the case constants; jump to the matching label (else default, else skip the switch). Then execute the statements from there in order, through later labels, until a break or the closing brace.
  - **[1] output\_prediction** (rule type OP, evaluation / result rule): A switch statement has no value. Its result is the effect of the case(s) run: with \`day = 3\`, the S&amp;W day switch prints Wed. Without breaks, day = 5 would print Fri, then Sat.
  - **[2] one\_step\_execution** (rule type OS, state-transition rule): One execution evaluates the selector once (any side effect in it happens once) and runs the statements of one entry point and any cases it falls into. It changes only what those statements change.

**9. `switch_statement` &rarr; `switch_statement@L3`** (has_level)

- **Exact edge logic:** switch statement -&gt; L3 (Relational): the answer relates the parts (3 ways).
  - **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): A switch replaces an if-else chain only when every test is \`expr == constant\` on the same expression. Range tests such as the income-bracket chain (\`income &lt; 47450\`) must stay an if-else chain.
  - **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Each case is normally ended by break, which exits the switch body. Leaving it out makes that case fall into the next. Inside a loop, that break exits the switch, not the loop.
  - **[2] purpose\_of\_the\_whole** (rule type P, plan / role rule): Plan: multiway dispatch or lookup. It maps one discrete value (day number, menu choice, character) to one of several actions or results. Grouped labels (\`case "apple": case "banana":\`) map several values to one action.

**10. `switch_statement` &rarr; `switch_statement@L4`** (has_level)

- **Exact edge logic:** switch statement -&gt; L4 (Extended abstract): the answer reasons beyond the given code (6 ways).
  - **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `SwitchNoFallThrough`: When every case ends with break, reordering the cases does not change behaviour (labels are distinct constants). Removing one break changes behaviour for that value only. Adding a default changes only values with no matching label.
  - **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Use switch for more than two mutually exclusive alternatives decided by equality of one int, char, String or enum value. Use an if-else chain for ranges, doubles or unrelated conditions. Use an array lookup (S&amp;W 1.4) when each case only selects a value.
  - **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: Without break, execution falls through into the following cases. Kind: silent logic error. Trigger class: Any selector value whose case lacks a break: the following cases' statements also run (e.g. both Fri and Sat printed).
  - **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: Values that match no case do nothing unless a default is present. Kind: silent logic error. Trigger class: An out-of-range selector (day = 7) with no default: nothing happens, and a variable assigned only in the cases may stay unassigned.
  - **[4] diagnose\_an\_error** (rule type D, error rule): rule broken: Case labels must be distinct compile-time constants of the selector type, and the selector may not be double, float, long or boolean. Kind: compile-time. Trigger class: Duplicate \`case 1:\` labels, a variable as a label, or \`switch (x)\` with x a double.
  - **[5] diagnose\_an\_error** (rule type D, error rule): rule broken: A String selector is dereferenced. Kind: run-time exception. Trigger class: Switching on a String variable that is null throws NullPointerException.

**11. `topic1.3.g` &rarr; `switch_statement`** (contains)

- topic `topic1.3.g` contains `switch_statement`

**12. `topic1.3.g` &rarr; `break_statement`** (contains)

- topic `topic1.3.g` contains `break_statement`

**13. `topic1.3.g` &rarr; `conditional_operator`** (contains)

- topic `topic1.3.g` contains `conditional_operator`

**14. `topic1.3.g` &rarr; `continue_statement`** (contains)

- topic `topic1.3.g` contains `continue_statement`

**15. `topic1.3.g` &rarr; `do_while_loop`** (contains)

- topic `topic1.3.g` contains `do_while_loop`

**16. `topic1.3.g` &rarr; `labeled_break`** (contains)

- topic `topic1.3.g` contains `labeled_break`
