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

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 15 edges around this concept. The edge logic, the wrong and right rules and the exact rules of the ways are copied word for word from the graph.

## To work on (2)

- no code pattern or signal: the code cannot tag this concept
- no aliases: a student's words cannot name this concept

## What it needs first (1)

A prerequisite edge means the other concept has to be understood before `algorithm_pseudocode`.

### `statement` comes before `algorithm_pseudocode`

*one step, terminated by ;, executed in sequence*

- **Edge:** `pre:statement->algorithm_pseudocode`
- **Exact edge logic:** An algorithm becomes a program as a sequence of statements, executed once each in the order given.
- **Grounding:** book\_passage
- **Composition rule (R) of `algorithm_pseudocode` with `statement`:** Each step of the algorithm becomes one or more statements, executed in the same order.

## What it leads to (0)

These concepts need `algorithm_pseudocode` first.

No concept has this one as a prerequisite.

## Learned alongside (1)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

### `algorithm_pseudocode` alongside `flowchart`

*Flowchart: a diagram whose paths correspond to the flow-of-control paths through a program*

- **Edge:** `par:algorithm_pseudocode~flowchart`
- **Exact edge logic:** Both describe an algorithm before it is code: a flowchart draws the flow of control as boxes and arrows, pseudocode writes the steps as English and Java text.
- **Grounding:** book\_passage
- **Composition rule (R) of `algorithm_pseudocode` with `flowchart`:** A flowchart and pseudocode describe the same algorithm: one as a diagram of the flow of control, the other as text.

## Misconceptions (2)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### ComputerFillsInIntent

- **Edge:** `algorithm_pseudocode` &rarr; `ComputerFillsInIntent` (misconception)
- **Exact edge logic (the wrong rule):** The computer fills in omitted steps or values that the programmer meant, e.g. REPEAT 4 [FORWARD 30] draws a square without a turn command.
- **Twin logic (the right rule):** The computer executes only what the code states; every needed step and value must be written.
- **Wrong belief (on the node):** The computer fills in omitted steps or values that the programmer meant, e.g. REPEAT 4 [FORWARD 30] draws a square without a turn command.
- **Correct rule (on the node):** The computer executes only what the code states; every needed step and value must be written.
- **Provenance:** published
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [3] misconception, exact rule:** wrong rule: The computer fills in omitted steps or values that the programmer meant. Right rule: The computer executes exactly the statements written, once each in the order given; nothing that was meant but not written happens.
- **Edge `loop_body` &rarr; `ComputerFillsInIntent`, exact edge logic:** The computer fills in omitted steps or values that the programmer meant, e.g. REPEAT 4 [FORWARD 30] draws a square without a turn command. **Twin logic:** The computer executes only what the code states; every needed step and value must be written. (role: context)
- **Edge `program_text` &rarr; `ComputerFillsInIntent`, exact edge logic:** The computer fills in omitted steps or values that the programmer meant, e.g. REPEAT 4 [FORWARD 30] draws a square without a turn command. **Twin logic:** The computer executes only what the code states; every needed step and value must be written. (role: context)
- **Edge `statement` &rarr; `ComputerFillsInIntent`, exact edge logic:** The computer fills in omitted steps or values that the programmer meant, e.g. REPEAT 4 [FORWARD 30] draws a square without a turn command. **Twin logic:** The computer executes only what the code states; every needed step and value must be written. (role: primary)

### PseudocodeRunsAsIs

- **Edge:** `algorithm_pseudocode` &rarr; `PseudocodeRunsAsIs` (misconception)
- **Exact edge logic (the wrong rule):** Pseudocode can be compiled and run as it is.
- **Twin logic (the right rule):** Pseudocode mixes Java and English to outline the algorithm; every English step must still be written as Java statements before the program compiles.
- **Wrong belief (on the node):** Pseudocode can be compiled and run as it is.
- **Correct rule (on the node):** Pseudocode mixes Java and English to outline the algorithm; every English step must still be written as Java statements before the program compiles.
- **Provenance:** textbook
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [1] misconception, exact rule:** wrong rule: Pseudocode can be compiled and run as it is. Right rule: Pseudocode mixes Java and English to outline the algorithm; every English step must still be written as Java statements before the program compiles.
- **L0 way [2] inconsistent\_trace, exact rule:** Applies the algorithm idea unevenly: spells out every step for one part of the problem but leaves another part as a single vague step that the computer is expected to understand. (here mixing in: "Pseudocode can be compiled and run as it is")

## Errors (0)

An error edge states the rule that gets broken in a program, and the right rule.

The graph has no error edge from this concept.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for algorithm pseudocode: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to algorithm pseudocode agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

- **Edge:** `algorithm_pseudocode` &rarr; `algorithm_pseudocode@L0` (has_level)
- **Exact edge logic:** algorithm pseudocode -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (4 ways).

Ways (4), each with its exact rule:

- **[0] everyday\_reading** (rule type E, folk-meaning rule): Everyday instructions leave steps to the reader's common sense. An algorithm lists every step that specifies how to solve the problem, and the computer does exactly those steps in order.
- **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `PseudocodeRunsAsIs`: wrong rule: Pseudocode can be compiled and run as it is. Right rule: Pseudocode mixes Java and English to outline the algorithm; every English step must still be written as Java statements before the program compiles.
- **[2] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `PseudocodeRunsAsIs`: Applies the algorithm idea unevenly: spells out every step for one part of the problem but leaves another part as a single vague step that the computer is expected to understand. (here mixing in: "Pseudocode can be compiled and run as it is")
- **[3] misconception** (rule type M, wrong rule / right rule) &rarr; `ComputerFillsInIntent`: wrong rule: The computer fills in omitted steps or values that the programmer meant. Right rule: The computer executes exactly the statements written, once each in the order given; nothing that was meant but not written happens.

### L1: Unistructural / atom x text surface

L1 for algorithm pseudocode: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

- **Edge:** `algorithm_pseudocode` &rarr; `algorithm_pseudocode@L1` (has_level)
- **Exact edge logic:** algorithm pseudocode -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

Ways (2), each with its exact rule:

- **[0] names\_the\_element** (rule type N, identity rule): Algorithm: a sequence of steps that specifies how to solve a problem; pseudocode: an outline of it in English and Java.
- **[1] states\_the\_rule** (rule type S, declarative rule): An algorithm is a sequence of steps that specifies how to solve a problem. Pseudocode outlines it with a mix of Java statements and English comments, and shows which smaller steps still have to be written.

### L2: Multistructural / block x execution / preoperational

L2 for algorithm pseudocode: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

- **Edge:** `algorithm_pseudocode` &rarr; `algorithm_pseudocode@L2` (has_level)
- **Exact edge logic:** algorithm pseudocode -&gt; L2 (Multistructural): the answer applies the rules of algorithm pseudocode to every part of the code, in order (3 ways).

Ways (3), each with its exact rule:

- **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): Sequencing: state the problem, write the steps in order in pseudocode, refine each English step until it is one or a few Java statements, then code and test.
- **[1] output\_prediction** (rule type OP, evaluation / result rule): Result: the outcome of an algorithm on an input is found by carrying out its steps by hand; Euclid's algorithm on 1440 and 408 gives 24.
- **[2] one\_step\_execution** (rule type OS, state-transition rule): State transition: one step of an algorithm changes the values it works on in one defined way, as one statement does in the program.

### L3: Relational / relations x function (concrete operational begins)

L3 for algorithm pseudocode: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

- **Edge:** `algorithm_pseudocode` &rarr; `algorithm_pseudocode@L3` (has_level)
- **Exact edge logic:** algorithm pseudocode -&gt; L3 (Relational): the answer relates the parts (3 ways).

Ways (3), each with its exact rule:

- **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Each step of the algorithm becomes one or more statements, executed in the same order.
- **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): A flowchart and pseudocode describe the same algorithm: one as a diagram of the flow of control, the other as text.
- **[2] purpose\_of\_the\_whole** (rule type P, plan / role rule): Plan: decide what the program must do, step by step, before writing Java, so that the code only translates the steps.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for algorithm pseudocode: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

- **Edge:** `algorithm_pseudocode` &rarr; `algorithm_pseudocode@L4` (has_level)
- **Exact edge logic:** algorithm pseudocode -&gt; L4 (Extended abstract): the answer reasons beyond the given code (3 ways).

Ways (3), each with its exact rule:

- **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `PseudocodeRunsAsIs`: Conservation: refining a pseudocode step into Java keeps its meaning; a different algorithm for the same problem (for example Euclid versus trying every divisor) keeps the answer but changes the number of steps.
- **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Before coding a non-trivial problem, write the algorithm as pseudocode, check it by hand on a small input, then translate each step into Java.
- **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: Every step of an algorithm must be stated. Kind: logic error. Trigger class: a step that was left implicit in the outline (an initialization, the last case, an exit test) is missing from the code

## Same topic

`algorithm_pseudocode` belongs to the topic **Control flow** (`topic1.3.a`). The topic also contains: `control_flow`, `flowchart`.

## Rules of the concept (15)

- **Book** (TJ-2e, p. 10 (pdf 32)): "An algorithm is a sequence of steps that specifies how to solve a problem."
- **Book** (TJ-2e, p. 219 (pdf 241)): "To outline this algorithm, we'll use a combination of Java statements and English comments. This technique is sometimes called pseudocode"
- **E** (folk-meaning rule): Everyday instructions leave steps to the reader's common sense. An algorithm lists every step that specifies how to solve the problem, and the computer does exactly those steps in order.
- **M** (wrong rule / right rule): PseudocodeRunsAsIs: wrong: Pseudocode can be compiled and run as it is. \| right: Pseudocode mixes Java and English to outline the algorithm; every English step must still be written as Java statements before the program compiles.
- **M** (wrong rule / right rule): ComputerFillsInIntent: wrong: The computer fills in omitted steps or values that the programmer meant. \| right: The computer executes exactly the statements written, once each in the order given; nothing that was meant but not written happens.
- **T** (uneven-application rule): Applies the algorithm idea unevenly: spells out every step for one part of the problem but leaves another part as a single vague step that the computer is expected to understand.
- **N** (identity rule): Algorithm: a sequence of steps that specifies how to solve a problem; pseudocode: an outline of it in English and Java.
- **S** (declarative rule): An algorithm is a sequence of steps that specifies how to solve a problem. Pseudocode outlines it with a mix of Java statements and English comments, and shows which smaller steps still have to be written.
- **LT** (operational sequencing rule): Sequencing: state the problem, write the steps in order in pseudocode, refine each English step until it is one or a few Java statements, then code and test.
- **OP** (evaluation / result rule): Result: the outcome of an algorithm on an input is found by carrying out its steps by hand; Euclid's algorithm on 1440 and 408 gives 24.
- **OS** (state-transition rule): State transition: one step of an algorithm changes the values it works on in one defined way, as one statement does in the program.
- **R** (composition rule (with a neighbour)): with statement: Each step of the algorithm becomes one or more statements, executed in the same order.
- **R** (composition rule (with a neighbour)): with flowchart: A flowchart and pseudocode describe the same algorithm: one as a diagram of the flow of control, the other as text.
- **P** (plan / role rule): Plan: decide what the program must do, step by step, before writing Java, so that the code only translates the steps.
- **C** (conservation rule): Conservation: refining a pseudocode step into Java keeps its meaning; a different algorithm for the same problem (for example Euclid versus trying every divisor) keeps the answer but changes the number of steps.
- **D** (error rule): rule broken: Every step of an algorithm must be stated. (logic error)
- **X** (applicability rule): Before coding a non-trivial problem, write the algorithm as pseudocode, check it by hand on a small input, then translate each step into Java.

## How it is found in code and answers (reader block)

- **Aliases:** none
- **Code patterns:** none
- **Operator symbols:** none
- **Java types:** none

## The whole prerequisite chain

- **Everything it builds on (4):** `class_declaration`, `main_method`, `program_text`, `statement`
- **Everything that builds on it (0):** nothing

## Every edge in this view and its exact edge logic (15)

All the edges drawn in the picture, in the order: prerequisite, parallel, misconception, error, has_level, contains.

**1. `statement` &rarr; `algorithm_pseudocode`** (prerequisite)

- **Exact edge logic:** An algorithm becomes a program as a sequence of statements, executed once each in the order given.
- **Grounding:** book\_passage
- **Composition rule (R) of `algorithm_pseudocode` with `statement`:** Each step of the algorithm becomes one or more statements, executed in the same order.

**2. `algorithm_pseudocode` &harr; `flowchart`** (parallel)

- **Exact edge logic:** Both describe an algorithm before it is code: a flowchart draws the flow of control as boxes and arrows, pseudocode writes the steps as English and Java text.
- **Grounding:** book\_passage
- **Composition rule (R) of `algorithm_pseudocode` with `flowchart`:** A flowchart and pseudocode describe the same algorithm: one as a diagram of the flow of control, the other as text.

**3. `algorithm_pseudocode` &rarr; `ComputerFillsInIntent`** (misconception)

- **Exact edge logic (the wrong rule):** The computer fills in omitted steps or values that the programmer meant, e.g. REPEAT 4 [FORWARD 30] draws a square without a turn command.
- **Twin logic (the right rule):** The computer executes only what the code states; every needed step and value must be written.
- **Role:** context

**4. `algorithm_pseudocode` &rarr; `PseudocodeRunsAsIs`** (misconception)

- **Exact edge logic (the wrong rule):** Pseudocode can be compiled and run as it is.
- **Twin logic (the right rule):** Pseudocode mixes Java and English to outline the algorithm; every English step must still be written as Java statements before the program compiles.
- **Role:** primary

**5. `loop_body` &rarr; `ComputerFillsInIntent`** (misconception)

- **Exact edge logic (the wrong rule):** The computer fills in omitted steps or values that the programmer meant, e.g. REPEAT 4 [FORWARD 30] draws a square without a turn command.
- **Twin logic (the right rule):** The computer executes only what the code states; every needed step and value must be written.
- **Role:** context

**6. `program_text` &rarr; `ComputerFillsInIntent`** (misconception)

- **Exact edge logic (the wrong rule):** The computer fills in omitted steps or values that the programmer meant, e.g. REPEAT 4 [FORWARD 30] draws a square without a turn command.
- **Twin logic (the right rule):** The computer executes only what the code states; every needed step and value must be written.
- **Role:** context

**7. `statement` &rarr; `ComputerFillsInIntent`** (misconception)

- **Exact edge logic (the wrong rule):** The computer fills in omitted steps or values that the programmer meant, e.g. REPEAT 4 [FORWARD 30] draws a square without a turn command.
- **Twin logic (the right rule):** The computer executes only what the code states; every needed step and value must be written.
- **Role:** primary

**8. `algorithm_pseudocode` &rarr; `algorithm_pseudocode@L0`** (has_level)

- **Exact edge logic:** algorithm pseudocode -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (4 ways).
  - **[0] everyday\_reading** (rule type E, folk-meaning rule): Everyday instructions leave steps to the reader's common sense. An algorithm lists every step that specifies how to solve the problem, and the computer does exactly those steps in order.
  - **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `PseudocodeRunsAsIs`: wrong rule: Pseudocode can be compiled and run as it is. Right rule: Pseudocode mixes Java and English to outline the algorithm; every English step must still be written as Java statements before the program compiles.
  - **[2] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `PseudocodeRunsAsIs`: Applies the algorithm idea unevenly: spells out every step for one part of the problem but leaves another part as a single vague step that the computer is expected to understand. (here mixing in: "Pseudocode can be compiled and run as it is")
  - **[3] misconception** (rule type M, wrong rule / right rule) &rarr; `ComputerFillsInIntent`: wrong rule: The computer fills in omitted steps or values that the programmer meant. Right rule: The computer executes exactly the statements written, once each in the order given; nothing that was meant but not written happens.

**9. `algorithm_pseudocode` &rarr; `algorithm_pseudocode@L1`** (has_level)

- **Exact edge logic:** algorithm pseudocode -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).
  - **[0] names\_the\_element** (rule type N, identity rule): Algorithm: a sequence of steps that specifies how to solve a problem; pseudocode: an outline of it in English and Java.
  - **[1] states\_the\_rule** (rule type S, declarative rule): An algorithm is a sequence of steps that specifies how to solve a problem. Pseudocode outlines it with a mix of Java statements and English comments, and shows which smaller steps still have to be written.

**10. `algorithm_pseudocode` &rarr; `algorithm_pseudocode@L2`** (has_level)

- **Exact edge logic:** algorithm pseudocode -&gt; L2 (Multistructural): the answer applies the rules of algorithm pseudocode to every part of the code, in order (3 ways).
  - **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): Sequencing: state the problem, write the steps in order in pseudocode, refine each English step until it is one or a few Java statements, then code and test.
  - **[1] output\_prediction** (rule type OP, evaluation / result rule): Result: the outcome of an algorithm on an input is found by carrying out its steps by hand; Euclid's algorithm on 1440 and 408 gives 24.
  - **[2] one\_step\_execution** (rule type OS, state-transition rule): State transition: one step of an algorithm changes the values it works on in one defined way, as one statement does in the program.

**11. `algorithm_pseudocode` &rarr; `algorithm_pseudocode@L3`** (has_level)

- **Exact edge logic:** algorithm pseudocode -&gt; L3 (Relational): the answer relates the parts (3 ways).
  - **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Each step of the algorithm becomes one or more statements, executed in the same order.
  - **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): A flowchart and pseudocode describe the same algorithm: one as a diagram of the flow of control, the other as text.
  - **[2] purpose\_of\_the\_whole** (rule type P, plan / role rule): Plan: decide what the program must do, step by step, before writing Java, so that the code only translates the steps.

**12. `algorithm_pseudocode` &rarr; `algorithm_pseudocode@L4`** (has_level)

- **Exact edge logic:** algorithm pseudocode -&gt; L4 (Extended abstract): the answer reasons beyond the given code (3 ways).
  - **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `PseudocodeRunsAsIs`: Conservation: refining a pseudocode step into Java keeps its meaning; a different algorithm for the same problem (for example Euclid versus trying every divisor) keeps the answer but changes the number of steps.
  - **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Before coding a non-trivial problem, write the algorithm as pseudocode, check it by hand on a small input, then translate each step into Java.
  - **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: Every step of an algorithm must be stated. Kind: logic error. Trigger class: a step that was left implicit in the outline (an initialization, the last case, an exit test) is missing from the code

**13. `topic1.3.a` &rarr; `algorithm_pseudocode`** (contains)

- topic `topic1.3.a` contains `algorithm_pseudocode`

**14. `topic1.3.a` &rarr; `control_flow`** (contains)

- topic `topic1.3.a` contains `control_flow`

**15. `topic1.3.a` &rarr; `flowchart`** (contains)

- topic `topic1.3.a` contains `flowchart`
