# Flowchart (`flowchart`)

a diagram whose paths correspond to the flow-of-control paths through a program

Section 1.3 1.3 Conditionals and Loops, topic 1.3.a Control flow.

![The knowledge graph around flowchart](flowchart.png)

## At a glance

- **Needs first:** `control_flow`
- **Leads to:** nothing
- **Learned alongside:** `algorithm_pseudocode`
- **Misconceptions:** none
- **Errors:** none
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 10 edges around this concept, each explained in the graph's own words.

## What it needs first (1)

A prerequisite edge means the other concept has to be understood before `flowchart`.

### `control_flow` comes before `flowchart`

*the order in which statements are executed*

A flowchart draws the flow of control: each path through the diagram is a path the program can take.

- **Grounding:** book passage
- **How `flowchart` combines with `control_flow`:** The flowchart's arrows are the program's control flow: sequence = a straight chain, if = branch and rejoin, loop = a back arrow to the test. Nesting a loop draws a loop inside a loop, and the diagram quickly becomes complex.
- **How `control_flow` combines with `flowchart`:** A flowchart draws control flow: each path through the diagram is a possible path of execution, with a decision box for each if or loop test.

## What it leads to (0)

These concepts need `flowchart` first.

No concept has this one as a prerequisite.

## Learned alongside (1)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

### `flowchart` alongside `algorithm_pseudocode`

*an algorithm is a sequence of steps that solves a problem; pseudocode outlines it in English and Java before it is coded*

Both describe an algorithm before it is code: a flowchart draws the flow of control as boxes and arrows, pseudocode writes the steps as English and Java text.

- **Grounding:** book passage
- **How `algorithm_pseudocode` combines with `flowchart`:** A flowchart and pseudocode describe the same algorithm: one as a diagram of the flow of control, the other as text.

## Misconceptions (0)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

The graph has no misconception edge from this concept.

## Errors (0)

An error edge states the rule that gets broken in a program, and the right rule.

The graph has no error edge from this concept.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for Flowchart: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to Flowchart agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

Flowchart -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (1 way).

- **everyday reading** (folk-meaning rule): Folk meaning: an everyday flowchart is a static picture or a decision tree read top to bottom once, so a novice reads a loop-back arrow as decoration and the diamond as a one-time question. In a program flowchart, each path is a possible execution, and an arrow returning to a diamond means the test is evaluated again.

### L1: Unistructural / atom x text surface

L1 for Flowchart: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

Flowchart -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

- **names the element** (identity rule): Diagram: a flowchart is a diagram of control flow. Boxes are statements, diamonds are boolean tests with yes/no exits, and arrows show the order of execution.
- **states the rule** (declarative rule): Every path through the flowchart corresponds to a flow-of-control path through the program. An if is a diamond whose branches rejoin; a while is a diamond whose yes branch runs the body and returns to the diamond.

### L2: Multistructural / block x execution / preoperational

L2 for Flowchart: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

Flowchart -&gt; L2 (Multistructural): the answer applies the rules of Flowchart to every part of the code, in order (3 ways).

- **line by line trace** (operational sequencing rule): Execution order: start at the entry; execute each box when reached; at a diamond evaluate the condition and follow the yes or no arrow; follow back arrows to re-test; stop at the exit.
- **output prediction** (evaluation / result rule): The result of reading a flowchart for given inputs is the path taken (the sequence of boxes and branch choices) and so the output. For \`if (x &gt; y) max = x; else max = y;\` with x = 2, y = 5, the path goes to the no branch and sets max = 5.
- **one step execution** (state-transition rule): One step moves along one arrow: either execute one box (changing the variables it assigns) or evaluate one diamond (changing nothing, choosing yes or no).

### L3: Relational / relations x function (concrete operational begins)

L3 for Flowchart: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

Flowchart -&gt; L3 (Relational): the answer relates the parts (3 ways).

- **relation to neighbour** (composition rule (with a neighbour)): The flowchart's arrows are the program's control flow: sequence = a straight chain, if = branch and rejoin, loop = a back arrow to the test. Nesting a loop draws a loop inside a loop, and the diagram quickly becomes complex.
- **relation to neighbour** (composition rule (with a neighbour)): Both describe an algorithm before it is code: a flowchart draws the flow of control as boxes and arrows, pseudocode writes the steps as English and Java text.
- **purpose of the whole** (plan / role rule): Purpose: to visualise and understand the control flow of basic building blocks (if, while, for) and to check where each path leads. It is not a way to design whole modern programs.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for Flowchart: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

Flowchart -&gt; L4 (Extended abstract): the answer reasons beyond the given code (4 ways).

- **predict a change** (conservation rule): Moving the back arrow from the diamond to the body box changes a while into a do-while (test after). Removing the back arrow turns the loop into an if. Swapping the yes and no labels swaps the branches.
- **transfer to a new program** (applicability rule): Use a flowchart to understand a single if, while, for or a small nesting. For larger programs, use indentation, traces and a limited set of structured constructs instead: flowcharts of complex control flow are hard to read.
- **diagnose an error** (error rule): rule broken: A loop's back arrow must return to the test, not straight to the body. Kind: silent logic error. Trigger class: Drawing or tracing the while body as repeating without re-checking the diamond: the body runs again after the condition is false.
- **diagnose an error** (error rule): rule broken: A diamond must have both yes and no exits. Kind: silent logic error. Trigger class: Omitting the no path (e.g. for an if without else, or a loop exit): the diagram has no path for the false case.

## Same topic

`flowchart` belongs to the topic **Control flow** (`topic1.3.a`). The topic also contains: `algorithm_pseudocode`, `control_flow`.

## Rules of the concept (13)

- **folk-meaning rule:** Folk meaning: an everyday flowchart is a static picture or a decision tree read top to bottom once, so a novice reads a loop-back arrow as decoration and the diamond as a one-time question. In a program flowchart, each path is a possible execution, and an arrow returning to a diamond means the test is evaluated again.
- **uneven-application rule:** Applies the path-following rule unevenly: on some passes the trace takes the yes branch without re-evaluating the diamond, or does not follow the back arrow to the test. Loops are then traced as ifs (one pass).
- **identity rule:** Diagram: a flowchart is a diagram of control flow. Boxes are statements, diamonds are boolean tests with yes/no exits, and arrows show the order of execution.
- **declarative rule:** Every path through the flowchart corresponds to a flow-of-control path through the program. An if is a diamond whose branches rejoin; a while is a diamond whose yes branch runs the body and returns to the diamond.
- **operational sequencing rule:** Execution order: start at the entry; execute each box when reached; at a diamond evaluate the condition and follow the yes or no arrow; follow back arrows to re-test; stop at the exit.
- **evaluation / result rule:** The result of reading a flowchart for given inputs is the path taken (the sequence of boxes and branch choices) and so the output. For \`if (x &gt; y) max = x; else max = y;\` with x = 2, y = 5, the path goes to the no branch and sets max = 5.
- **state-transition rule:** One step moves along one arrow: either execute one box (changing the variables it assigns) or evaluate one diamond (changing nothing, choosing yes or no).
- **composition rule (with a neighbour):** with control\_flow: The flowchart's arrows are the program's control flow: sequence = a straight chain, if = branch and rejoin, loop = a back arrow to the test. Nesting a loop draws a loop inside a loop, and the diagram quickly becomes complex.
- **plan / role rule:** Purpose: to visualise and understand the control flow of basic building blocks (if, while, for) and to check where each path leads. It is not a way to design whole modern programs.
- **conservation rule:** Moving the back arrow from the diamond to the body box changes a while into a do-while (test after). Removing the back arrow turns the loop into an if. Swapping the yes and no labels swaps the branches.
- **error rule:** rule broken: A loop's back arrow must return to the test, not straight to the body. (silent logic error)
- **error rule:** rule broken: A diamond must have both yes and no exits. (silent logic error)
- **applicability rule:** Use a flowchart to understand a single if, while, for or a small nesting. For larger programs, use indentation, traces and a limited set of structured constructs instead: flowcharts of complex control flow are hard to read.

## The whole prerequisite chain

- **Everything it builds on (5):** `class_declaration`, `control_flow`, `main_method`, `program_text`, `statement`
- **Everything that builds on it (0):** nothing
