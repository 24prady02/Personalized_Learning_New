# algorithm_pseudocode (`algorithm_pseudocode`)

an algorithm is a sequence of steps that solves a problem; pseudocode outlines it in English and Java before it is coded

Section 1.3 Conditionals and Loops, topic 1.3.a Control flow.

![The knowledge graph around algorithm_pseudocode](algorithm_pseudocode.png)

## At a glance

- **Needs first:** `statement`
- **Leads to:** nothing
- **Learned alongside:** `flowchart`
- **Misconceptions:** `ComputerFillsInIntent`, `PseudocodeRunsAsIs`
- **Errors:** none
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 15 edges around this concept, each explained in the graph's own words.

## What it needs first (1)

A prerequisite edge means the other concept has to be understood before `algorithm_pseudocode`.

### `statement` comes before `algorithm_pseudocode`

*one step, terminated by ;, executed in sequence*

An algorithm becomes a program as a sequence of statements, executed once each in the order given.

- **Grounding:** book passage
- **How `algorithm_pseudocode` combines with `statement`:** Each step of the algorithm becomes one or more statements, executed in the same order.

## What it leads to (0)

These concepts need `algorithm_pseudocode` first.

No concept has this one as a prerequisite.

## Learned alongside (1)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

### `algorithm_pseudocode` alongside `flowchart`

*Flowchart: a diagram whose paths correspond to the flow-of-control paths through a program*

Both describe an algorithm before it is code: a flowchart draws the flow of control as boxes and arrows, pseudocode writes the steps as English and Java text.

- **Grounding:** book passage
- **How `algorithm_pseudocode` combines with `flowchart`:** A flowchart and pseudocode describe the same algorithm: one as a diagram of the flow of control, the other as text.

## Misconceptions (2)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### ComputerFillsInIntent

- **Wrong rule:** The computer fills in omitted steps or values that the programmer meant, e.g. REPEAT 4 [FORWARD 30] draws a square without a turn command.
- **Right rule:** The computer executes only what the code states; every needed step and value must be written.
- **Role of this concept:** context
- **Shows at level L0 as:** misconception: wrong rule: The computer fills in omitted steps or values that the programmer meant. Right rule: The computer executes exactly the statements written, once each in the order given; nothing that was meant but not written happens.
- **Also an edge from `loop_body`:** The computer fills in omitted steps or values that the programmer meant, e.g. REPEAT 4 [FORWARD 30] draws a square without a turn command.
- **Also an edge from `program_text`:** The computer fills in omitted steps or values that the programmer meant, e.g. REPEAT 4 [FORWARD 30] draws a square without a turn command.
- **Also an edge from `statement`:** The computer fills in omitted steps or values that the programmer meant, e.g. REPEAT 4 [FORWARD 30] draws a square without a turn command.

### PseudocodeRunsAsIs

- **Wrong rule:** Pseudocode can be compiled and run as it is.
- **Right rule:** Pseudocode mixes Java and English to outline the algorithm; every English step must still be written as Java statements before the program compiles.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: Pseudocode can be compiled and run as it is. Right rule: Pseudocode mixes Java and English to outline the algorithm; every English step must still be written as Java statements before the program compiles.
- **Shows at level L0 as:** inconsistent trace: Applies the algorithm idea unevenly: spells out every step for one part of the problem but leaves another part as a single vague step that the computer is expected to understand. (here mixing in: "Pseudocode can be compiled and run as it is")

## Errors (0)

An error edge states the rule that gets broken in a program, and the right rule.

The graph has no error edge from this concept.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for algorithm pseudocode: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to algorithm pseudocode agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

algorithm pseudocode -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (4 ways).

- **everyday reading** (folk-meaning rule): Everyday instructions leave steps to the reader's common sense. An algorithm lists every step that specifies how to solve the problem, and the computer does exactly those steps in order.
- **misconception** (wrong rule / right rule; shows `PseudocodeRunsAsIs`): wrong rule: Pseudocode can be compiled and run as it is. Right rule: Pseudocode mixes Java and English to outline the algorithm; every English step must still be written as Java statements before the program compiles.
- **inconsistent trace** (uneven-application rule; shows `PseudocodeRunsAsIs`): Applies the algorithm idea unevenly: spells out every step for one part of the problem but leaves another part as a single vague step that the computer is expected to understand. (here mixing in: "Pseudocode can be compiled and run as it is")
- **misconception** (wrong rule / right rule; shows `ComputerFillsInIntent`): wrong rule: The computer fills in omitted steps or values that the programmer meant. Right rule: The computer executes exactly the statements written, once each in the order given; nothing that was meant but not written happens.

### L1: Unistructural / atom x text surface

L1 for algorithm pseudocode: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

algorithm pseudocode -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

- **names the element** (identity rule): Algorithm: a sequence of steps that specifies how to solve a problem; pseudocode: an outline of it in English and Java.
- **states the rule** (declarative rule): An algorithm is a sequence of steps that specifies how to solve a problem. Pseudocode outlines it with a mix of Java statements and English comments, and shows which smaller steps still have to be written.

### L2: Multistructural / block x execution / preoperational

L2 for algorithm pseudocode: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

algorithm pseudocode -&gt; L2 (Multistructural): the answer applies the rules of algorithm pseudocode to every part of the code, in order (3 ways).

- **line by line trace** (operational sequencing rule): Sequencing: state the problem, write the steps in order in pseudocode, refine each English step until it is one or a few Java statements, then code and test.
- **output prediction** (evaluation / result rule): Result: the outcome of an algorithm on an input is found by carrying out its steps by hand; Euclid's algorithm on 1440 and 408 gives 24.
- **one step execution** (state-transition rule): State transition: one step of an algorithm changes the values it works on in one defined way, as one statement does in the program.

### L3: Relational / relations x function (concrete operational begins)

L3 for algorithm pseudocode: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

algorithm pseudocode -&gt; L3 (Relational): the answer relates the parts (3 ways).

- **relation to neighbour** (composition rule (with a neighbour)): Each step of the algorithm becomes one or more statements, executed in the same order.
- **relation to neighbour** (composition rule (with a neighbour)): A flowchart and pseudocode describe the same algorithm: one as a diagram of the flow of control, the other as text.
- **purpose of the whole** (plan / role rule): Plan: decide what the program must do, step by step, before writing Java, so that the code only translates the steps.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for algorithm pseudocode: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

algorithm pseudocode -&gt; L4 (Extended abstract): the answer reasons beyond the given code (3 ways).

- **predict a change** (conservation rule; shows `PseudocodeRunsAsIs`): Conservation: refining a pseudocode step into Java keeps its meaning; a different algorithm for the same problem (for example Euclid versus trying every divisor) keeps the answer but changes the number of steps.
- **transfer to a new program** (applicability rule): Before coding a non-trivial problem, write the algorithm as pseudocode, check it by hand on a small input, then translate each step into Java.
- **diagnose an error** (error rule): rule broken: Every step of an algorithm must be stated. Kind: logic error. Trigger class: a step that was left implicit in the outline (an initialization, the last case, an exit test) is missing from the code

## Same topic

`algorithm_pseudocode` belongs to the topic **Control flow** (`topic1.3.a`). The topic also contains: `control_flow`, `flowchart`.

## Rules of the concept (15)

- **folk-meaning rule:** Everyday instructions leave steps to the reader's common sense. An algorithm lists every step that specifies how to solve the problem, and the computer does exactly those steps in order.
- **wrong rule / right rule:** PseudocodeRunsAsIs: wrong: Pseudocode can be compiled and run as it is. \| right: Pseudocode mixes Java and English to outline the algorithm; every English step must still be written as Java statements before the program compiles.
- **wrong rule / right rule:** ComputerFillsInIntent: wrong: The computer fills in omitted steps or values that the programmer meant. \| right: The computer executes exactly the statements written, once each in the order given; nothing that was meant but not written happens.
- **uneven-application rule:** Applies the algorithm idea unevenly: spells out every step for one part of the problem but leaves another part as a single vague step that the computer is expected to understand.
- **identity rule:** Algorithm: a sequence of steps that specifies how to solve a problem; pseudocode: an outline of it in English and Java.
- **declarative rule:** An algorithm is a sequence of steps that specifies how to solve a problem. Pseudocode outlines it with a mix of Java statements and English comments, and shows which smaller steps still have to be written.
- **operational sequencing rule:** Sequencing: state the problem, write the steps in order in pseudocode, refine each English step until it is one or a few Java statements, then code and test.
- **evaluation / result rule:** Result: the outcome of an algorithm on an input is found by carrying out its steps by hand; Euclid's algorithm on 1440 and 408 gives 24.
- **state-transition rule:** State transition: one step of an algorithm changes the values it works on in one defined way, as one statement does in the program.
- **composition rule (with a neighbour):** with statement: Each step of the algorithm becomes one or more statements, executed in the same order.
- **composition rule (with a neighbour):** with flowchart: A flowchart and pseudocode describe the same algorithm: one as a diagram of the flow of control, the other as text.
- **plan / role rule:** Plan: decide what the program must do, step by step, before writing Java, so that the code only translates the steps.
- **conservation rule:** Conservation: refining a pseudocode step into Java keeps its meaning; a different algorithm for the same problem (for example Euclid versus trying every divisor) keeps the answer but changes the number of steps.
- **error rule:** rule broken: Every step of an algorithm must be stated. (logic error)
- **applicability rule:** Before coding a non-trivial problem, write the algorithm as pseudocode, check it by hand on a small input, then translate each step into Java.

## The whole prerequisite chain

- **Everything it builds on (4):** `class_declaration`, `main_method`, `program_text`, `statement`
- **Everything that builds on it (0):** nothing
