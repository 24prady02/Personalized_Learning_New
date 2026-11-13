# else_if_chain (`else_if_chain`)

if ... else if ... else picks exactly one branch

Section 1.3 Conditionals and Loops, topic 1.3.e Nesting.

![The knowledge graph around else_if_chain](else_if_chain.png)

## At a glance

- **Needs first:** `if_else_statement`
- **Leads to:** nothing
- **Learned alongside:** `switch_statement`
- **Misconceptions:** `ElsIf`, `ElseIfChainExitsEarly`, `ElseIfOrderIgnored`, `MultipleElseIfBranchesRun`
- **Errors:** none
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 16 edges around this concept, each explained in the graph's own words.

## What it needs first (1)

A prerequisite edge means the other concept has to be understood before `else_if_chain`.

### `if_else_statement` comes before `else_if_chain`

*choose one of two blocks*

An else-if chain is an if-else whose else part is another if.

- **Grounding:** book passage
- **How `else_if_chain` combines with `if_else_statement`:** An else-if chain is an if-else whose else part is another if-else, so every rule of if-else (one test, one branch) applies at each link.
- **How `if_else_statement` combines with `else_if_chain`:** An else-if chain is an if-else whose else part is another if-else, repeated; the final else catches all remaining cases.

## What it leads to (0)

These concepts need `else_if_chain` first.

No concept has this one as a prerequisite.

## Learned alongside (1)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

### `else_if_chain` alongside `switch_statement`

*switch (x) { case v: ...; break; default: ... }*

Both pick one of several alternatives. A switch compares one value with constant case labels and falls through without break; an else-if chain tests each condition in turn and runs only the first true branch.

- **Grounding:** book passage

## Misconceptions (4)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### ElsIf

- **Wrong rule:** Java has an elsif keyword for multi-way branches.
- **Right rule:** Multi-way branches are written else if.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: Java has an elsif keyword for multi-way branches. Right rule: Multi-way branches are written else if.
- **Shows at level L0 as:** inconsistent trace: Applies the chain rule (LT) unevenly: stops at the first true condition on some inputs but continues testing (and running branches) on others. (here mixing in: "Java has an elsif keyword for multi-way branches")

### ElseIfChainExitsEarly

- **Wrong rule:** An else-if chain can finish before it has tested all its conditions, even when no branch has run.
- **Right rule:** The conditions of an else-if chain are tested in order until one is true; only then, or after the last test (and the final else), does the chain end.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: An else-if chain can finish before it has tested all its conditions, even when no branch has run. Right rule: The conditions of an else-if chain are tested in order until one is true; only then, or after the last test (and the final else), does the chain end.

### ElseIfOrderIgnored

- **Wrong rule:** The conditions of an else-if chain can be tested in any order (e.g. the matching or most specific one first).
- **Right rule:** The conditions are tested top to bottom and the first true one wins, so their order changes the result when conditions overlap.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: The conditions of an else-if chain can be tested in any order (e.g. the matching or most specific one first). Right rule: The conditions are tested top to bottom and the first true one wins, so their order changes the result when conditions overlap.

### MultipleElseIfBranchesRun

- **Wrong rule:** Every true branch of an else-if chain runs.
- **Right rule:** Only the first branch whose condition is true runs.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: Every true branch of an else-if chain runs. Right rule: Only the first branch whose condition is true runs.
- **Also an edge from `nested_conditionals`:** Every true branch of an else-if chain runs.

## Errors (0)

An error edge states the rule that gets broken in a program, and the right rule.

The graph has no error edge from this concept.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for else if chain: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to else if chain agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

else if chain -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (6 ways).

- **everyday reading** (folk-meaning rule): Folk meaning: a list of rules 'if A ...; else if B ...' reads like a set of independent rules where every one that applies is followed, in any order. In Java the conditions are tested top to bottom and only the first true branch runs.
- **misconception** (wrong rule / right rule; shows `ElsIf`): wrong rule: Java has an elsif keyword for multi-way branches. Right rule: Multi-way branches are written else if.
- **misconception** (wrong rule / right rule; shows `MultipleElseIfBranchesRun`): wrong rule: Every true branch of an else-if chain runs. Right rule: Only the first branch whose condition is true runs.
- **misconception** (wrong rule / right rule; shows `ElseIfChainExitsEarly`): wrong rule: An else-if chain can finish before it has tested all its conditions, even when no branch has run. Right rule: The conditions of an else-if chain are tested in order until one is true; only then, or after the last test (and the final else), does the chain end.
- **misconception** (wrong rule / right rule; shows `ElseIfOrderIgnored`): wrong rule: The conditions of an else-if chain can be tested in any order (e.g. the matching or most specific one first). Right rule: The conditions are tested top to bottom and the first true one wins, so their order changes the result when conditions overlap.
- **inconsistent trace** (uneven-application rule; shows `ElsIf`): Applies the chain rule (LT) unevenly: stops at the first true condition on some inputs but continues testing (and running branches) on others. (here mixing in: "Java has an elsif keyword for multi-way branches")

### L1: Unistructural / atom x text surface

L1 for else if chain: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

else if chain -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

- **names the element** (identity rule): An else-if chain (multiway if-else) is a sequence of if-else statements in which each else is another if, choosing among mutually exclusive possibilities.
- **states the rule** (declarative rule): Written if (c1) S1 else if (c2) S2 ... else Sn; the ifs are nested to test from among a number of mutually exclusive possibilities, and the final else needs no condition.

### L2: Multistructural / block x execution / preoperational

L2 for else if chain: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

else if chain -&gt; L2 (Multistructural): the answer applies the rules of else if chain to every part of the code, in order (3 ways).

- **line by line trace** (operational sequencing rule): Test c1; if true run S1 and leave the chain; otherwise test c2, and so on; if no condition is true, run the final else (if any); then continue after the chain.
- **output prediction** (evaluation / result rule): Exactly one branch (or none, without a final else) runs: in the tax example an income of 100000 gives rate .25, because income &lt; 47450 is false and income &lt; 114650 is the first true test.
- **one step execution** (state-transition rule): One execution evaluates conditions in order until the first true one, applies that branch's changes, and skips all later tests.

### L3: Relational / relations x function (concrete operational begins)

L3 for else if chain: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

else if chain -&gt; L3 (Relational): the answer relates the parts (2 ways).

- **relation to neighbour** (composition rule (with a neighbour)): An else-if chain is an if-else whose else part is another if-else, so every rule of if-else (one test, one branch) applies at each link.
- **purpose of the whole** (plan / role rule): Plan: multiway selection / classification into ranges - pick one category for a value (tax bracket, sign of x, grade).

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for else if chain: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

else if chain -&gt; L4 (Extended abstract): the answer reasons beyond the given code (4 ways).

- **predict a change** (conservation rule; shows `ElsIf`): Reordering the tests preserves behaviour only if the conditions are mutually exclusive; with overlapping, ordered thresholds (income &lt; 47450, &lt; 114650 ...) swapping two tests changes the result. Replacing else if by separate ifs makes several branches run.
- **transfer to a new program** (applicability rule): Use an else-if chain when exactly one of several mutually exclusive, ordered conditions applies; use separate ifs when several actions may apply, and a switch when testing one expression against many fixed values.
- **diagnose an error** (error rule): rule broken: Java has no elsif/elif keyword; the chain is written else if. Kind: compile-time. Trigger class: Writing elsif (c) or elif (c): the compiler reports a missing semicolon or unknown symbol.
- **diagnose an error** (error rule): rule broken: The first true condition wins, so a broader test placed earlier hides later ones. Kind: silent logic error. Trigger class: if (x &lt; 100) ... else if (x &lt; 10) ...: the second branch is unreachable for every input; no compiler error.

## Same topic

`else_if_chain` belongs to the topic **Nesting** (`topic1.3.e`). The topic also contains: `dangling_else`, `nested_conditionals`, `nested_loops`.

## Rules of the concept (17)

- **folk-meaning rule:** Folk meaning: a list of rules 'if A ...; else if B ...' reads like a set of independent rules where every one that applies is followed, in any order. In Java the conditions are tested top to bottom and only the first true branch runs.
- **wrong rule / right rule:** ElsIf: wrong: Java has an elsif keyword for multi-way branches. \| right: Multi-way branches are written else if.
- **wrong rule / right rule:** MultipleElseIfBranchesRun: wrong: Every true branch of an else-if chain runs. \| right: Only the first branch whose condition is true runs.
- **wrong rule / right rule:** ElseIfChainExitsEarly: wrong: An else-if chain can finish before it has tested all its conditions, even when no branch has run. \| right: The conditions of an else-if chain are tested in order until one is true; only then, or after the last test (and the final else), does the chain end.
- **wrong rule / right rule:** ElseIfOrderIgnored: wrong: The conditions of an else-if chain can be tested in any order (e.g. the matching or most specific one first). \| right: The conditions are tested top to bottom and the first true one wins, so their order changes the result when conditions overlap.
- **uneven-application rule:** Applies the chain rule (LT) unevenly: stops at the first true condition on some inputs but continues testing (and running branches) on others.
- **identity rule:** An else-if chain (multiway if-else) is a sequence of if-else statements in which each else is another if, choosing among mutually exclusive possibilities.
- **declarative rule:** Written if (c1) S1 else if (c2) S2 ... else Sn; the ifs are nested to test from among a number of mutually exclusive possibilities, and the final else needs no condition.
- **operational sequencing rule:** Test c1; if true run S1 and leave the chain; otherwise test c2, and so on; if no condition is true, run the final else (if any); then continue after the chain.
- **evaluation / result rule:** Exactly one branch (or none, without a final else) runs: in the tax example an income of 100000 gives rate .25, because income &lt; 47450 is false and income &lt; 114650 is the first true test.
- **state-transition rule:** One execution evaluates conditions in order until the first true one, applies that branch's changes, and skips all later tests.
- **composition rule (with a neighbour):** with if\_else\_statement: An else-if chain is an if-else whose else part is another if-else, so every rule of if-else (one test, one branch) applies at each link.
- **plan / role rule:** Plan: multiway selection / classification into ranges - pick one category for a value (tax bracket, sign of x, grade).
- **conservation rule:** Reordering the tests preserves behaviour only if the conditions are mutually exclusive; with overlapping, ordered thresholds (income &lt; 47450, &lt; 114650 ...) swapping two tests changes the result. Replacing else if by separate ifs makes several branches run.
- **error rule:** rule broken: Java has no elsif/elif keyword; the chain is written else if. (compile-time)
- **error rule:** rule broken: The first true condition wins, so a broader test placed earlier hides later ones. (silent logic error)
- **applicability rule:** Use an else-if chain when exactly one of several mutually exclusive, ordered conditions applies; use separate ifs when several actions may apply, and a switch when testing one expression against many fixed values.

## The whole prerequisite chain

- **Everything it builds on (18):** `arithmetic_operators`, `boolean`, `boolean_expression`, `class_declaration`, `comparison_operators`, `control_flow`, `data_type`, `expression`, `identifier`, `if_else_statement`, `if_statement`, `literal`, `logical_operators`, `main_method`, `primitive_type`, `program_text`, `statement`, `variable`
- **Everything that builds on it (0):** nothing
