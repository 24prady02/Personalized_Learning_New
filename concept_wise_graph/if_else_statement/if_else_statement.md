# if_else_statement (`if_else_statement`)

choose one of two blocks

Section 1.3 Conditionals and Loops, topic 1.3.b If statements.

![The knowledge graph around if_else_statement](if_else_statement.png)

## At a glance

- **Needs first:** `if_statement`
- **Leads to:** `conditional_operator`, `else_if_chain`, `nested_conditionals`
- **Learned alongside:** nothing
- **Misconceptions:** `BothBranchesExecute`, `BranchChosenByIntent`, `ConditionalIsSequence`, `DuplicateCodeInBranches`, `ElseAlwaysExecutes`
- **Errors:** `ElseWithCondition`
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 21 edges around this concept. The edge logic, the wrong and right rules and the exact rules of the ways are copied word for word from the graph.

## To work on (0)

Nothing is missing for this concept.

## What it needs first (1)

A prerequisite edge means the other concept has to be understood before `if_else_statement`.

### `if_statement` comes before `if_else_statement`

*run a block only when the condition holds*

- **Edge:** `pre:if_statement->if_else_statement`
- **Exact edge logic:** if-else extends if with a second block that runs exactly when the condition is false.
- **Grounding:** book\_passage
- **Composition rule (R) of `if_else_statement` with `if_statement`:** if-else is an if with a second branch for the false case; dropping the else gives a plain if in which the false case does nothing.
- **Composition rule (R) of `if_statement` with `if_else_statement`:** if-else extends if with a second branch that runs exactly when the condition is false; a lone if has an implicit empty else-case.

## What it leads to (3)

These concepts need `if_else_statement` first.

### `if_else_statement` comes before `conditional_operator`

*c ? a : b -- an expression that picks one of two values*

- **Edge:** `pre:if_else_statement->conditional_operator`
- **Exact edge logic:** c ? a : b is the expression form of if (c) ... else ....
- **Grounding:** questionable
- **Composition rule (R) of `if_else_statement` with `conditional_operator`:** c ? a : b is the expression form of if (c) v = a; else v = b;: it yields a value of one branch, evaluating only the selected operand.
- **Composition rule (R) of `conditional_operator` with `if_else_statement`:** \`v = c ? a : b;\` is the expression form of \`if (c) v = a; else v = b;\`. It can be used inside a larger expression (an argument or concatenation), but it cannot replace an if-else whose branches are statements without values.

### `if_else_statement` comes before `else_if_chain`

*if ... else if ... else picks exactly one branch*

- **Edge:** `pre:if_else_statement->else_if_chain`
- **Exact edge logic:** An else-if chain is an if-else whose else part is another if.
- **Grounding:** book\_passage
- **Composition rule (R) of `if_else_statement` with `else_if_chain`:** An else-if chain is an if-else whose else part is another if-else, repeated; the final else catches all remaining cases.
- **Composition rule (R) of `else_if_chain` with `if_else_statement`:** An else-if chain is an if-else whose else part is another if-else, so every rule of if-else (one test, one branch) applies at each link.

### `if_else_statement` comes before `nested_conditionals`

*else-if chains and conditionals inside conditionals*

- **Edge:** `pre:if_else_statement->nested_conditionals`
- **Exact edge logic:** Nesting puts an if or if-else inside a branch of another if-else; an else-if chain is the common case where the else branch is itself an if.
- **Grounding:** book\_passage
- **Composition rule (R) of `if_else_statement` with `nested_conditionals`:** Either branch may itself be an if or if-else, which nests conditionals; without braces an inner else pairs with the innermost if.
- **Composition rule (R) of `nested_conditionals` with `if_else_statement`:** Nesting puts an if or if-else inside a branch of another if-else; when the inner statement fills the else branch it forms an else-if chain.

## Learned alongside (0)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

No parallel edge touches this concept.

## Misconceptions (5)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### BothBranchesExecute

- **Edge:** `if_else_statement` &rarr; `BothBranchesExecute` (misconception)
- **Exact edge logic (the wrong rule):** Both the then branch and the else branch run.
- **Twin logic (the right rule):** Exactly one of the two branches runs.
- **Wrong belief (on the node):** Both the then branch and the else branch run.
- **Correct rule (on the node):** Exactly one of the two branches runs.
- **Provenance:** published
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [3] misconception, exact rule:** wrong rule: Both the then branch and the else branch run. Right rule: Exactly one of the two branches runs.

### BranchChosenByIntent

- **Edge:** `if_else_statement` &rarr; `BranchChosenByIntent` (misconception)
- **Exact edge logic (the wrong rule):** Which branch runs is decided by what the programmer meant or by code outside the if, not by whether the condition is true.
- **Twin logic (the right rule):** The then branch runs exactly when the condition evaluates to true at the moment it is tested; otherwise the else branch (if any) runs.
- **Wrong belief (on the node):** Which branch runs is decided by what the programmer meant or by code outside the if, not by whether the condition is true.
- **Correct rule (on the node):** The then branch runs exactly when the condition evaluates to true at the moment it is tested; otherwise the else branch (if any) runs.
- **Provenance:** published
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [6] misconception, exact rule:** wrong rule: Which branch runs is decided by what the programmer meant or by code outside the if, not by whether the condition is true. Right rule: The then branch runs exactly when the condition evaluates to true at the moment it is tested; otherwise the else branch (if any) runs.
- **Edge `if_statement` &rarr; `BranchChosenByIntent`, exact edge logic:** Which branch runs is decided by what the programmer meant or by code outside the if, not by whether the condition is true. **Twin logic:** The then branch runs exactly when the condition evaluates to true at the moment it is tested; otherwise the else branch (if any) runs. (role: primary)

### ConditionalIsSequence

- **Edge:** `if_else_statement` &rarr; `ConditionalIsSequence` (misconception)
- **Exact edge logic (the wrong rule):** if (c) A else B is the same as if (c) A followed by if (!c) B.
- **Twin logic (the right rule):** In if-else, c is tested once and exactly one of A or B runs, even if A changes the variables that c uses.
- **Wrong belief (on the node):** if-else is the same as two separate ifs
- **Correct rule (on the node):** In if-else, c is tested once and exactly one of A or B runs, even if A changes the variables that c uses.
- **Provenance:** published
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [1] misconception, exact rule:** wrong rule: if-else is the same as two separate ifs. Right rule: In if-else, c is tested once and exactly one of A or B runs, even if A changes the variables that c uses.
- **L0 way [5] inconsistent\_trace, exact rule:** Applies the if-else rule (LT) unevenly: on some traces runs both branches, re-tests the condition after the then branch to decide whether to run the else branch, or runs the else branch whatever the condition. (here mixing in: "if-else is the same as two separate ifs")

### DuplicateCodeInBranches

- **Edge:** `if_else_statement` &rarr; `DuplicateCodeInBranches` (misconception)
- **Exact edge logic (the wrong rule):** Writes the same statements in both branches of an if-else.
- **Twin logic (the right rule):** Code common to both branches belongs before or after the if-else.
- **Wrong belief (on the node):** Writes the same statements in both branches of an if-else.
- **Correct rule (on the node):** Code common to both branches belongs before or after the if-else.
- **Provenance:** textbook
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [4] misconception, exact rule:** wrong rule: Writes the same statements in both branches of an if-else. Right rule: Code common to both branches belongs before or after the if-else.

### ElseAlwaysExecutes

- **Edge:** `if_else_statement` &rarr; `ElseAlwaysExecutes` (misconception)
- **Exact edge logic (the wrong rule):** The else branch of an if-else statement always executes.
- **Twin logic (the right rule):** The else branch runs only when the if condition is false.
- **Wrong belief (on the node):** The else branch of an if-else statement always executes.
- **Correct rule (on the node):** The else branch runs only when the if condition is false.
- **Provenance:** published
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [2] misconception, exact rule:** wrong rule: The else branch of an if-else statement always executes. Right rule: The else branch runs only when the if condition is false.

## Errors (1)

An error edge states the rule that gets broken in a program, and the right rule.

### ElseWithCondition

- **Edge:** `if_else_statement` &rarr; `ElseWithCondition` (error)
- **Exact edge logic (the wrong rule):** Writes else (x &gt; 0) with a condition but no if.
- **Twin logic (the right rule):** else takes no condition; use else if (x &gt; 0).
- **Wrong belief (on the node):** Writes else (x &gt; 0) with a condition but no if.
- **Correct rule (on the node):** else takes no condition; use else if (x &gt; 0).
- **Provenance:** published
- **Role of this concept:** primary
- **Edge `boolean_expression` &rarr; `ElseWithCondition`, exact edge logic:** Writes else (x &gt; 0) with a condition but no if. **Twin logic:** else takes no condition; use else if (x &gt; 0). (role: context)

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for if else statement: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to if else statement agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

- **Edge:** `if_else_statement` &rarr; `if_else_statement@L0` (has_level)
- **Exact edge logic:** if else statement -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (7 ways).

Ways (7), each with its exact rule:

- **[0] everyday\_reading** (rule type E, folk-meaning rule): Folk meaning: in English 'otherwise' can be heard as 'and then also', and 'if ... else ...' as two separate rules that are each checked. In Java the condition is tested once and exactly one of the two branches runs.
- **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `ConditionalIsSequence`: wrong rule: if-else is the same as two separate ifs. Right rule: In if-else, c is tested once and exactly one of A or B runs, even if A changes the variables that c uses.
- **[2] misconception** (rule type M, wrong rule / right rule) &rarr; `ElseAlwaysExecutes`: wrong rule: The else branch of an if-else statement always executes. Right rule: The else branch runs only when the if condition is false.
- **[3] misconception** (rule type M, wrong rule / right rule) &rarr; `BothBranchesExecute`: wrong rule: Both the then branch and the else branch run. Right rule: Exactly one of the two branches runs.
- **[4] misconception** (rule type M, wrong rule / right rule) &rarr; `DuplicateCodeInBranches`: wrong rule: Writes the same statements in both branches of an if-else. Right rule: Code common to both branches belongs before or after the if-else.
- **[5] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `ConditionalIsSequence`: Applies the if-else rule (LT) unevenly: on some traces runs both branches, re-tests the condition after the then branch to decide whether to run the else branch, or runs the else branch whatever the condition. (here mixing in: "if-else is the same as two separate ifs")
- **[6] misconception** (rule type M, wrong rule / right rule) &rarr; `BranchChosenByIntent`: wrong rule: Which branch runs is decided by what the programmer meant or by code outside the if, not by whether the condition is true. Right rule: The then branch runs exactly when the condition evaluates to true at the moment it is tested; otherwise the else branch (if any) runs.

### L1: Unistructural / atom x text surface

L1 for if else statement: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

- **Edge:** `if_else_statement` &rarr; `if_else_statement@L1` (has_level)
- **Exact edge logic:** if else statement -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

Ways (2), each with its exact rule:

- **[0] names\_the\_element** (rule type N, identity rule): The if-else statement is a two-way conditional: it executes one of two statements (or blocks) depending on a boolean condition.
- **[1] states\_the\_rule** (rule type S, declarative rule): Syntax: if (&lt;boolean expression&gt;) &lt;statements T&gt; else &lt;statements F&gt;; it executes one or the other, but not both: T if the condition is true, F otherwise.

### L2: Multistructural / block x execution / preoperational

L2 for if else statement: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

- **Edge:** `if_else_statement` &rarr; `if_else_statement@L2` (has_level)
- **Exact edge logic:** if else statement -&gt; L2 (Multistructural): the answer applies the rules of if else statement to every part of the code, in order (3 ways).

Ways (3), each with its exact rule:

- **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): Evaluate the condition once; if true execute the then branch, otherwise execute the else branch; then continue with the statement after the whole if-else (the condition is not re-tested).
- **[1] output\_prediction** (rule type OP, evaluation / result rule): Exactly one branch's effects occur; e.g. if (x &gt; y) max = x; else max = y; leaves max equal to the larger value, and the coin flip prints either Heads or Tails, never both.
- **[2] one\_step\_execution** (rule type OS, state-transition rule): One execution reads the condition's variables and applies the effects of exactly one branch; a change made by the then branch to the condition's variables cannot cause the else branch to run.

### L3: Relational / relations x function (concrete operational begins)

L3 for if else statement: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

- **Edge:** `if_else_statement` &rarr; `if_else_statement@L3` (has_level)
- **Exact edge logic:** if else statement -&gt; L3 (Relational): the answer relates the parts (5 ways).

Ways (5), each with its exact rule:

- **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): if-else is an if with a second branch for the false case; dropping the else gives a plain if in which the false case does nothing.
- **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Either branch may itself be an if or if-else, which nests conditionals; without braces an inner else pairs with the innermost if.
- **[2] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): c ? a : b is the expression form of if (c) v = a; else v = b;: it yields a value of one branch, evaluating only the selected operand.
- **[3] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): An else-if chain is an if-else whose else part is another if-else, repeated; the final else catches all remaining cases.
- **[4] purpose\_of\_the\_whole** (rule type P, plan / role rule): Plan: two-way choice / alternative action - compute one of two results (max of two values, heads or tails, error message or quotient).

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for if else statement: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

- **Edge:** `if_else_statement` &rarr; `if_else_statement@L4` (has_level)
- **Exact edge logic:** if else statement -&gt; L4 (Extended abstract): the answer reasons beyond the given code (5 ways).

Ways (5), each with its exact rule:

- **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `ConditionalIsSequence`: Swapping the two branches and negating the condition preserves behaviour; swapping the branches alone inverts it. Replacing if-else with two separate ifs is not equivalent when the then branch changes a variable used in the condition.
- **[1] diagnose\_an\_error** (rule type D, error rule): rule broken: else takes no condition: it is the branch for the false case of the preceding if; a further test needs else if (...). Kind: compile-time. Trigger class: Writing else (x &gt; 0) stmt; the compiler reads (x &gt; 0) as the start of an expression statement, which is not a valid statement, and reports an error.
- **[2] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Use if-else when exactly one of two actions must happen; use a plain if when nothing happens in the false case, an else-if chain or switch for more than two mutually exclusive cases, and c ? a : b when you only need to choose a value.
- **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: Code common to both branches belongs before or after the if-else. Kind: silent logic error. Trigger class: A statement duplicated in both branches and later edited in only one: the two cases silently diverge.
- **[4] diagnose\_an\_error** (rule type D, error rule): rule broken: An else must directly follow the then statement of an if. Kind: compile-time. Trigger class: if (c) x = 1; y = 2; else x = 0;: the else has no matching if ('else without if').

## Same topic

`if_else_statement` belongs to the topic **If statements** (`topic1.3.b`). The topic also contains: `empty_statement`, `if_statement`, `syntax_template`.

## Rules of the concept (22)

- **Book** (SW-1e, p. 47 (pdf 57)): "depending on whether the boolean expression is true or false, as in the following template: if (&lt;boolean expression&gt;) &lt;statements T&gt; else &lt;statements F&gt;"
- **Book** (OT-If, ): "The if-then-else statement provides a secondary path of execution when an "if" clause evaluates to false."
- **Book** (SW-1.3, p. 46 (pdf 56)): "Most computations require different actions for different inputs."
- **E** (folk-meaning rule): Folk meaning: in English 'otherwise' can be heard as 'and then also', and 'if ... else ...' as two separate rules that are each checked. In Java the condition is tested once and exactly one of the two branches runs.
- **M** (wrong rule / right rule): BothBranchesExecute: wrong: Both the then branch and the else branch run. \| right: Exactly one of the two branches runs.
- **M** (wrong rule / right rule): ConditionalIsSequence: wrong: if-else is the same as two separate ifs \| right: In if-else, c is tested once and exactly one of A or B runs, even if A changes the variables that c uses.
- **M** (wrong rule / right rule): DuplicateCodeInBranches: wrong: Writes the same statements in both branches of an if-else. \| right: Code common to both branches belongs before or after the if-else.
- **M** (wrong rule / right rule): ElseAlwaysExecutes: wrong: The else branch of an if-else statement always executes. \| right: The else branch runs only when the if condition is false.
- **M** (wrong rule / right rule): BranchChosenByIntent: wrong: Which branch runs is decided by what the programmer meant or by code outside the if, not by whether the condition is true. \| right: The then branch runs exactly when the condition evaluates to true at the moment it is tested; otherwise the else branch (if any) runs.
- **T** (uneven-application rule): Applies the if-else rule (LT) unevenly: on some traces runs both branches, re-tests the condition after the then branch to decide whether to run the else branch, or runs the else branch whatever the condition.
- **N** (identity rule): The if-else statement is a two-way conditional: it executes one of two statements (or blocks) depending on a boolean condition.
- **S** (declarative rule): Syntax: if (&lt;boolean expression&gt;) &lt;statements T&gt; else &lt;statements F&gt;; it executes one or the other, but not both: T if the condition is true, F otherwise.
- **LT** (operational sequencing rule): Evaluate the condition once; if true execute the then branch, otherwise execute the else branch; then continue with the statement after the whole if-else (the condition is not re-tested).
- **OP** (evaluation / result rule): Exactly one branch's effects occur; e.g. if (x &gt; y) max = x; else max = y; leaves max equal to the larger value, and the coin flip prints either Heads or Tails, never both.
- **OS** (state-transition rule): One execution reads the condition's variables and applies the effects of exactly one branch; a change made by the then branch to the condition's variables cannot cause the else branch to run.
- **R** (composition rule (with a neighbour)): with if\_statement: if-else is an if with a second branch for the false case; dropping the else gives a plain if in which the false case does nothing.
- **R** (composition rule (with a neighbour)): with nested\_conditionals: Either branch may itself be an if or if-else, which nests conditionals; without braces an inner else pairs with the innermost if.
- **R** (composition rule (with a neighbour)): with conditional\_operator: c ? a : b is the expression form of if (c) v = a; else v = b;: it yields a value of one branch, evaluating only the selected operand.
- **R** (composition rule (with a neighbour)): with else\_if\_chain: An else-if chain is an if-else whose else part is another if-else, repeated; the final else catches all remaining cases.
- **P** (plan / role rule): Plan: two-way choice / alternative action - compute one of two results (max of two values, heads or tails, error message or quotient).
- **C** (conservation rule): Swapping the two branches and negating the condition preserves behaviour; swapping the branches alone inverts it. Replacing if-else with two separate ifs is not equivalent when the then branch changes a variable used in the condition.
- **D** (error rule): rule broken: else takes no condition: it is the branch for the false case of the preceding if; a further test needs else if (...). (compile-time)
- **D** (error rule): rule broken: Code common to both branches belongs before or after the if-else. (silent logic error)
- **D** (error rule): rule broken: An else must directly follow the then statement of an if. (compile-time)
- **X** (applicability rule): Use if-else when exactly one of two actions must happen; use a plain if when nothing happens in the false case, an else-if chain or switch for more than two mutually exclusive cases, and c ? a : b when you only need to choose a value.

## How it is found in code and answers (reader block)

- **Aliases:** else, if else, else branch
- **Code patterns:** `\belse\b`
- **Operator symbols:** none
- **Java types:** none

## The whole prerequisite chain

- **Everything it builds on (17):** `arithmetic_operators`, `boolean`, `boolean_expression`, `class_declaration`, `comparison_operators`, `control_flow`, `data_type`, `expression`, `identifier`, `if_statement`, `literal`, `logical_operators`, `main_method`, `primitive_type`, `program_text`, `statement`, `variable`
- **Everything that builds on it (4):** `conditional_operator`, `dangling_else`, `else_if_chain`, `nested_conditionals`

## Every edge in this view and its exact edge logic (21)

All the edges drawn in the picture, in the order: prerequisite, parallel, misconception, error, has_level, contains.

**1. `if_else_statement` &rarr; `conditional_operator`** (prerequisite)

- **Exact edge logic:** c ? a : b is the expression form of if (c) ... else ....
- **Grounding:** questionable
- **Composition rule (R) of `if_else_statement` with `conditional_operator`:** c ? a : b is the expression form of if (c) v = a; else v = b;: it yields a value of one branch, evaluating only the selected operand.
- **Composition rule (R) of `conditional_operator` with `if_else_statement`:** \`v = c ? a : b;\` is the expression form of \`if (c) v = a; else v = b;\`. It can be used inside a larger expression (an argument or concatenation), but it cannot replace an if-else whose branches are statements without values.

**2. `if_else_statement` &rarr; `else_if_chain`** (prerequisite)

- **Exact edge logic:** An else-if chain is an if-else whose else part is another if.
- **Grounding:** book\_passage
- **Composition rule (R) of `if_else_statement` with `else_if_chain`:** An else-if chain is an if-else whose else part is another if-else, repeated; the final else catches all remaining cases.
- **Composition rule (R) of `else_if_chain` with `if_else_statement`:** An else-if chain is an if-else whose else part is another if-else, so every rule of if-else (one test, one branch) applies at each link.

**3. `if_else_statement` &rarr; `nested_conditionals`** (prerequisite)

- **Exact edge logic:** Nesting puts an if or if-else inside a branch of another if-else; an else-if chain is the common case where the else branch is itself an if.
- **Grounding:** book\_passage
- **Composition rule (R) of `if_else_statement` with `nested_conditionals`:** Either branch may itself be an if or if-else, which nests conditionals; without braces an inner else pairs with the innermost if.
- **Composition rule (R) of `nested_conditionals` with `if_else_statement`:** Nesting puts an if or if-else inside a branch of another if-else; when the inner statement fills the else branch it forms an else-if chain.

**4. `if_statement` &rarr; `if_else_statement`** (prerequisite)

- **Exact edge logic:** if-else extends if with a second block that runs exactly when the condition is false.
- **Grounding:** book\_passage
- **Composition rule (R) of `if_statement` with `if_else_statement`:** if-else extends if with a second branch that runs exactly when the condition is false; a lone if has an implicit empty else-case.
- **Composition rule (R) of `if_else_statement` with `if_statement`:** if-else is an if with a second branch for the false case; dropping the else gives a plain if in which the false case does nothing.

**5. `if_else_statement` &rarr; `BothBranchesExecute`** (misconception)

- **Exact edge logic (the wrong rule):** Both the then branch and the else branch run.
- **Twin logic (the right rule):** Exactly one of the two branches runs.
- **Role:** primary

**6. `if_else_statement` &rarr; `BranchChosenByIntent`** (misconception)

- **Exact edge logic (the wrong rule):** Which branch runs is decided by what the programmer meant or by code outside the if, not by whether the condition is true.
- **Twin logic (the right rule):** The then branch runs exactly when the condition evaluates to true at the moment it is tested; otherwise the else branch (if any) runs.
- **Role:** context

**7. `if_else_statement` &rarr; `ConditionalIsSequence`** (misconception)

- **Exact edge logic (the wrong rule):** if (c) A else B is the same as if (c) A followed by if (!c) B.
- **Twin logic (the right rule):** In if-else, c is tested once and exactly one of A or B runs, even if A changes the variables that c uses.
- **Role:** primary

**8. `if_else_statement` &rarr; `DuplicateCodeInBranches`** (misconception)

- **Exact edge logic (the wrong rule):** Writes the same statements in both branches of an if-else.
- **Twin logic (the right rule):** Code common to both branches belongs before or after the if-else.
- **Role:** primary

**9. `if_else_statement` &rarr; `ElseAlwaysExecutes`** (misconception)

- **Exact edge logic (the wrong rule):** The else branch of an if-else statement always executes.
- **Twin logic (the right rule):** The else branch runs only when the if condition is false.
- **Role:** primary

**10. `if_statement` &rarr; `BranchChosenByIntent`** (misconception)

- **Exact edge logic (the wrong rule):** Which branch runs is decided by what the programmer meant or by code outside the if, not by whether the condition is true.
- **Twin logic (the right rule):** The then branch runs exactly when the condition evaluates to true at the moment it is tested; otherwise the else branch (if any) runs.
- **Role:** primary

**11. `if_else_statement` &rarr; `ElseWithCondition`** (error)

- **Exact edge logic (the wrong rule):** Writes else (x &gt; 0) with a condition but no if.
- **Twin logic (the right rule):** else takes no condition; use else if (x &gt; 0).
- **Role:** primary

**12. `boolean_expression` &rarr; `ElseWithCondition`** (error)

- **Exact edge logic (the wrong rule):** Writes else (x &gt; 0) with a condition but no if.
- **Twin logic (the right rule):** else takes no condition; use else if (x &gt; 0).
- **Role:** context

**13. `if_else_statement` &rarr; `if_else_statement@L0`** (has_level)

- **Exact edge logic:** if else statement -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (7 ways).
  - **[0] everyday\_reading** (rule type E, folk-meaning rule): Folk meaning: in English 'otherwise' can be heard as 'and then also', and 'if ... else ...' as two separate rules that are each checked. In Java the condition is tested once and exactly one of the two branches runs.
  - **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `ConditionalIsSequence`: wrong rule: if-else is the same as two separate ifs. Right rule: In if-else, c is tested once and exactly one of A or B runs, even if A changes the variables that c uses.
  - **[2] misconception** (rule type M, wrong rule / right rule) &rarr; `ElseAlwaysExecutes`: wrong rule: The else branch of an if-else statement always executes. Right rule: The else branch runs only when the if condition is false.
  - **[3] misconception** (rule type M, wrong rule / right rule) &rarr; `BothBranchesExecute`: wrong rule: Both the then branch and the else branch run. Right rule: Exactly one of the two branches runs.
  - **[4] misconception** (rule type M, wrong rule / right rule) &rarr; `DuplicateCodeInBranches`: wrong rule: Writes the same statements in both branches of an if-else. Right rule: Code common to both branches belongs before or after the if-else.
  - **[5] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `ConditionalIsSequence`: Applies the if-else rule (LT) unevenly: on some traces runs both branches, re-tests the condition after the then branch to decide whether to run the else branch, or runs the else branch whatever the condition. (here mixing in: "if-else is the same as two separate ifs")
  - **[6] misconception** (rule type M, wrong rule / right rule) &rarr; `BranchChosenByIntent`: wrong rule: Which branch runs is decided by what the programmer meant or by code outside the if, not by whether the condition is true. Right rule: The then branch runs exactly when the condition evaluates to true at the moment it is tested; otherwise the else branch (if any) runs.

**14. `if_else_statement` &rarr; `if_else_statement@L1`** (has_level)

- **Exact edge logic:** if else statement -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).
  - **[0] names\_the\_element** (rule type N, identity rule): The if-else statement is a two-way conditional: it executes one of two statements (or blocks) depending on a boolean condition.
  - **[1] states\_the\_rule** (rule type S, declarative rule): Syntax: if (&lt;boolean expression&gt;) &lt;statements T&gt; else &lt;statements F&gt;; it executes one or the other, but not both: T if the condition is true, F otherwise.

**15. `if_else_statement` &rarr; `if_else_statement@L2`** (has_level)

- **Exact edge logic:** if else statement -&gt; L2 (Multistructural): the answer applies the rules of if else statement to every part of the code, in order (3 ways).
  - **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): Evaluate the condition once; if true execute the then branch, otherwise execute the else branch; then continue with the statement after the whole if-else (the condition is not re-tested).
  - **[1] output\_prediction** (rule type OP, evaluation / result rule): Exactly one branch's effects occur; e.g. if (x &gt; y) max = x; else max = y; leaves max equal to the larger value, and the coin flip prints either Heads or Tails, never both.
  - **[2] one\_step\_execution** (rule type OS, state-transition rule): One execution reads the condition's variables and applies the effects of exactly one branch; a change made by the then branch to the condition's variables cannot cause the else branch to run.

**16. `if_else_statement` &rarr; `if_else_statement@L3`** (has_level)

- **Exact edge logic:** if else statement -&gt; L3 (Relational): the answer relates the parts (5 ways).
  - **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): if-else is an if with a second branch for the false case; dropping the else gives a plain if in which the false case does nothing.
  - **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Either branch may itself be an if or if-else, which nests conditionals; without braces an inner else pairs with the innermost if.
  - **[2] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): c ? a : b is the expression form of if (c) v = a; else v = b;: it yields a value of one branch, evaluating only the selected operand.
  - **[3] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): An else-if chain is an if-else whose else part is another if-else, repeated; the final else catches all remaining cases.
  - **[4] purpose\_of\_the\_whole** (rule type P, plan / role rule): Plan: two-way choice / alternative action - compute one of two results (max of two values, heads or tails, error message or quotient).

**17. `if_else_statement` &rarr; `if_else_statement@L4`** (has_level)

- **Exact edge logic:** if else statement -&gt; L4 (Extended abstract): the answer reasons beyond the given code (5 ways).
  - **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `ConditionalIsSequence`: Swapping the two branches and negating the condition preserves behaviour; swapping the branches alone inverts it. Replacing if-else with two separate ifs is not equivalent when the then branch changes a variable used in the condition.
  - **[1] diagnose\_an\_error** (rule type D, error rule): rule broken: else takes no condition: it is the branch for the false case of the preceding if; a further test needs else if (...). Kind: compile-time. Trigger class: Writing else (x &gt; 0) stmt; the compiler reads (x &gt; 0) as the start of an expression statement, which is not a valid statement, and reports an error.
  - **[2] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Use if-else when exactly one of two actions must happen; use a plain if when nothing happens in the false case, an else-if chain or switch for more than two mutually exclusive cases, and c ? a : b when you only need to choose a value.
  - **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: Code common to both branches belongs before or after the if-else. Kind: silent logic error. Trigger class: A statement duplicated in both branches and later edited in only one: the two cases silently diverge.
  - **[4] diagnose\_an\_error** (rule type D, error rule): rule broken: An else must directly follow the then statement of an if. Kind: compile-time. Trigger class: if (c) x = 1; y = 2; else x = 0;: the else has no matching if ('else without if').

**18. `topic1.3.b` &rarr; `if_else_statement`** (contains)

- topic `topic1.3.b` contains `if_else_statement`

**19. `topic1.3.b` &rarr; `empty_statement`** (contains)

- topic `topic1.3.b` contains `empty_statement`

**20. `topic1.3.b` &rarr; `if_statement`** (contains)

- topic `topic1.3.b` contains `if_statement`

**21. `topic1.3.b` &rarr; `syntax_template`** (contains)

- topic `topic1.3.b` contains `syntax_template`
