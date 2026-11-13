# conditional_operator (`conditional_operator`)

c ? a : b -- an expression that picks one of two values

Section 1.3 Conditionals and Loops, topic 1.3.g Other conditional and loop constructs (break, continue, switch, do-while, ?:).

![The knowledge graph around conditional_operator](conditional_operator.png)

## At a glance

- **Needs first:** `expression`, `if_else_statement`
- **Leads to:** nothing
- **Learned alongside:** nothing
- **Misconceptions:** `MapToBooleanWithConditionalOperator`
- **Errors:** none
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 15 edges around this concept, each explained in the graph's own words.

## What it needs first (2)

A prerequisite edge means the other concept has to be understood before `conditional_operator`.

### `expression` comes before `conditional_operator`

*anything that evaluates to a value*

c ? a : b is an expression: the boolean c decides which of the two other expressions gives the value.

- **Grounding:** spec passage

### `if_else_statement` comes before `conditional_operator`

*choose one of two blocks*

c ? a : b is the expression form of if (c) ... else ....

- **Grounding:** questionable
- **How `conditional_operator` combines with `if_else_statement`:** \`v = c ? a : b;\` is the expression form of \`if (c) v = a; else v = b;\`. It can be used inside a larger expression (an argument or concatenation), but it cannot replace an if-else whose branches are statements without values.
- **How `if_else_statement` combines with `conditional_operator`:** c ? a : b is the expression form of if (c) v = a; else v = b;: it yields a value of one branch, evaluating only the selected operand.

## What it leads to (0)

These concepts need `conditional_operator` first.

No concept has this one as a prerequisite.

## Learned alongside (0)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

No parallel edge touches this concept.

## Misconceptions (1)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### MapToBooleanWithConditionalOperator

- **Wrong rule:** you need ? : to do the same
- **Right rule:** ok = (x &gt; y); already gives the boolean, so the ? : is unnecessary.
- **Role of this concept:** context
- **Shows at level L0 as:** misconception: wrong rule: To map a boolean expression to a boolean, a conditional operator is necessary (\`ok = (x &gt; y) ? true : false;\`). Right rule: A comparison already has type boolean, so \`ok = (x &gt; y);\` gives the same value; the ? : is redundant.
- **Shows at level L0 as:** inconsistent trace: Applies the LT rule unevenly: on a trace, both the second and third operands are evaluated (so side effects like \`i++\` happen twice), or the operand chosen does not match the condition. (here mixing in: "you need ? : to do the same")
- **Also an edge from `boolean_expression`:** To get a boolean from x &gt; y you need ok = (x &gt; y) ? true : false;.

## Errors (0)

An error edge states the rule that gets broken in a program, and the right rule.

The graph has no error edge from this concept.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for conditional operator: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to conditional operator agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

conditional operator -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (3 ways).

- **everyday reading** (folk-meaning rule): Folk meaning: in everyday text '?' marks a question and ':' introduces an explanation or list, so \`x &gt; y ? x : y\` reads as 'is x &gt; y? x, y' with no clear meaning, or as a statement that does something. In Java \`c ? a : b\` is an expression whose value is a if c is true and b otherwise.
- **misconception** (wrong rule / right rule; shows `MapToBooleanWithConditionalOperator`): wrong rule: To map a boolean expression to a boolean, a conditional operator is necessary (\`ok = (x &gt; y) ? true : false;\`). Right rule: A comparison already has type boolean, so \`ok = (x &gt; y);\` gives the same value; the ? : is redundant.
- **inconsistent trace** (uneven-application rule; shows `MapToBooleanWithConditionalOperator`): Applies the LT rule unevenly: on a trace, both the second and third operands are evaluated (so side effects like \`i++\` happen twice), or the operand chosen does not match the condition. (here mixing in: "you need ? : to do the same")

### L1: Unistructural / atom x text surface

L1 for conditional operator: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

conditional operator -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

- **names the element** (identity rule): Operator: the conditional operator \`? :\`, Java's only ternary operator. \`c ? a : b\` is an expression that picks one of two values.
- **states the rule** (declarative rule): The first operand must be boolean. If it is true the value is the second operand, otherwise the third. The two value operands must have compatible types; for numeric operands, binary numeric promotion applies. (Spec: JLS §15.25.)

### L2: Multistructural / block x execution / preoperational

L2 for conditional operator: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

conditional operator -&gt; L2 (Multistructural): the answer applies the rules of conditional operator to every part of the code, in order (3 ways).

- **line by line trace** (operational sequencing rule): Order: evaluate the condition first; then evaluate exactly one of the other operands (the second if true, the third if false); the unchosen operand is never evaluated. ? : groups right to left and has lower precedence than + and the comparisons.
- **output prediction** (evaluation / result rule): The result is a value, not an action. \`(x &gt; y) ? x : y\` with x = 3, y = 7 is 7. Numeric operands are promoted, so \`true ? 1 : 2.0\` is 1.0 (a double), and its type must fit the target of the assignment.
- **one step execution** (state-transition rule): Evaluating ? : changes no variable itself; it returns the chosen operand's value. Only side effects inside the condition or the chosen operand happen (in \`c ? i++ : j++\`, exactly one of i, j changes).

### L3: Relational / relations x function (concrete operational begins)

L3 for conditional operator: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

conditional operator -&gt; L3 (Relational): the answer relates the parts (2 ways).

- **relation to neighbour** (composition rule (with a neighbour)): \`v = c ? a : b;\` is the expression form of \`if (c) v = a; else v = b;\`. It can be used inside a larger expression (an argument or concatenation), but it cannot replace an if-else whose branches are statements without values.
- **purpose of the whole** (plan / role rule): Plan: select-a-value. It picks one of two values in one expression: max/min (\`m = a &gt; b ? a : b\`, a most-wanted-holder update), absolute value, singular/plural wording, or a default for a missing value.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for conditional operator: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

conditional operator -&gt; L4 (Extended abstract): the answer reasons beyond the given code (6 ways).

- **predict a change** (conservation rule; shows `MapToBooleanWithConditionalOperator`): Negating the condition and swapping the two value operands keeps the result. Changing a value operand's type can change the result type (int to double) and break an assignment to an int. Nesting ? : inside ? : keeps meaning but quickly harms readability.
- **transfer to a new program** (applicability rule): Use ? : for a short choice between two values inside an expression (max, a label, a default). Use an if-else statement when the branches do actions, are long, or nest. Use the boolean expression itself when the choice is between true and false.
- **diagnose an error** (error rule): rule broken: The first operand of ? : must be boolean. Kind: compile-time. Trigger class: An int or other non-boolean condition, e.g. \`n ? a : b\` with int n.
- **diagnose an error** (error rule): rule broken: A conditional expression is not a statement. Kind: compile-time. Trigger class: Using it on its own for its side effects, e.g. \`x &gt; 0 ? a++ : b++;\` (not a statement).
- **diagnose an error** (error rule): rule broken: The result type is the promoted type of both value operands. Kind: compile-time. Trigger class: \`int m = c ? 1 : 2.5;\` (possible lossy conversion from double to int).
- **diagnose an error** (error rule): rule broken: ? : has lower precedence than + and comparisons. Kind: compile-time. Trigger class: \`"max " + x &gt; y ? x : y\` parses as \`("max " + x) &gt; y\`, comparing a String with an int; parenthesise the conditional.

## Same topic

`conditional_operator` belongs to the topic **Other conditional and loop constructs (break, continue, switch, do-while, ?:)** (`topic1.3.g`). The topic also contains: `break_statement`, `continue_statement`, `do_while_loop`, `labeled_break`, `switch_statement`.

## Rules of the concept (16)

- **folk-meaning rule:** Folk meaning: in everyday text '?' marks a question and ':' introduces an explanation or list, so \`x &gt; y ? x : y\` reads as 'is x &gt; y? x, y' with no clear meaning, or as a statement that does something. In Java \`c ? a : b\` is an expression whose value is a if c is true and b otherwise.
- **wrong rule / right rule:** MapToBooleanWithConditionalOperator: wrong: To map a boolean expression to a boolean, a conditional operator is necessary (\`ok = (x &gt; y) ? true : false;\`). \| right: A comparison already has type boolean, so \`ok = (x &gt; y);\` gives the same value; the ? : is redundant.
- **uneven-application rule:** Applies the LT rule unevenly: on a trace, both the second and third operands are evaluated (so side effects like \`i++\` happen twice), or the operand chosen does not match the condition.
- **identity rule:** Operator: the conditional operator \`? :\`, Java's only ternary operator. \`c ? a : b\` is an expression that picks one of two values.
- **declarative rule:** The first operand must be boolean. If it is true the value is the second operand, otherwise the third. The two value operands must have compatible types; for numeric operands, binary numeric promotion applies. (Spec: JLS §15.25.)
- **operational sequencing rule:** Order: evaluate the condition first; then evaluate exactly one of the other operands (the second if true, the third if false); the unchosen operand is never evaluated. ? : groups right to left and has lower precedence than + and the comparisons.
- **evaluation / result rule:** The result is a value, not an action. \`(x &gt; y) ? x : y\` with x = 3, y = 7 is 7. Numeric operands are promoted, so \`true ? 1 : 2.0\` is 1.0 (a double), and its type must fit the target of the assignment.
- **state-transition rule:** Evaluating ? : changes no variable itself; it returns the chosen operand's value. Only side effects inside the condition or the chosen operand happen (in \`c ? i++ : j++\`, exactly one of i, j changes).
- **composition rule (with a neighbour):** with if\_else\_statement: \`v = c ? a : b;\` is the expression form of \`if (c) v = a; else v = b;\`. It can be used inside a larger expression (an argument or concatenation), but it cannot replace an if-else whose branches are statements without values.
- **plan / role rule:** Plan: select-a-value. It picks one of two values in one expression: max/min (\`m = a &gt; b ? a : b\`, a most-wanted-holder update), absolute value, singular/plural wording, or a default for a missing value.
- **conservation rule:** Negating the condition and swapping the two value operands keeps the result. Changing a value operand's type can change the result type (int to double) and break an assignment to an int. Nesting ? : inside ? : keeps meaning but quickly harms readability.
- **error rule:** rule broken: The first operand of ? : must be boolean. (compile-time)
- **error rule:** rule broken: A conditional expression is not a statement. (compile-time)
- **error rule:** rule broken: The result type is the promoted type of both value operands. (compile-time)
- **error rule:** rule broken: ? : has lower precedence than + and comparisons. (compile-time)
- **applicability rule:** Use ? : for a short choice between two values inside an expression (max, a label, a default). Use an if-else statement when the branches do actions, are long, or nest. Use the boolean expression itself when the choice is between true and false.

## The whole prerequisite chain

- **Everything it builds on (18):** `arithmetic_operators`, `boolean`, `boolean_expression`, `class_declaration`, `comparison_operators`, `control_flow`, `data_type`, `expression`, `identifier`, `if_else_statement`, `if_statement`, `literal`, `logical_operators`, `main_method`, `primitive_type`, `program_text`, `statement`, `variable`
- **Everything that builds on it (0):** nothing
