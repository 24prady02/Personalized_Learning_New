# Reasoning about loops (`loop_invariant_reasoning`)

convincing yourself a loop is correct by stating facts that hold each time through it and why it terminates

Section 1.3 1.3 Conditionals and Loops, topic 1.3.c While loops.

![The knowledge graph around loop_invariant_reasoning](loop_invariant_reasoning.png)

## At a glance

- **Needs first:** `while_loop`
- **Leads to:** nothing
- **Learned alongside:** nothing
- **Misconceptions:** none
- **Errors:** none
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 10 edges around this concept, each explained in the graph's own words.

## What it needs first (1)

A prerequisite edge means the other concept has to be understood before `loop_invariant_reasoning`.

### `while_loop` comes before `loop_invariant_reasoning`

*repeat a block while a condition holds*

To reason about a while loop you state what stays true on every pass and why the condition eventually becomes false.

- **Grounding:** book passage
- **How `loop_invariant_reasoning` combines with `while_loop`:** The invariant is stated at the while test. The while condition supplies the extra fact available inside the body (v ≤ N/2, so 2v ≤ N), and its negation supplies the extra fact after the loop (2v &gt; N).
- **How `while_loop` combines with `loop_invariant_reasoning`:** To trust a while loop, state what stays true on every pass and why the condition eventually becomes false (e.g. v is always a power of 2, v increases, so the loop terminates).

## What it leads to (0)

These concepts need `loop_invariant_reasoning` first.

No concept has this one as a prerequisite.

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

L0 for Reasoning about loops: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to Reasoning about loops agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

Reasoning about loops -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (1 way).

- **everyday reading** (folk-meaning rule): Folk meaning: in everyday life 'convincing yourself' means trying a few cases, so a novice thinks a loop is correct because it worked on the inputs tried. Loop reasoning requires a fact that holds before every test, a reason it survives each pass, and a reason the loop ends, so the argument covers any number of iterations.

### L1: Unistructural / atom x text surface

L1 for Reasoning about loops: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

Reasoning about loops -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

- **names the element** (identity rule): Reasoning method: arguing that a loop is correct by stating facts (invariants) that hold each time through it, plus a reason the loop terminates.
- **states the rule** (declarative rule): For \`int v = 1; while (v &lt;= N/2) v = 2\*v;\`: (1) v is always a power of 2; (2) v is never greater than N; (3) v increases each pass, so the loop terminates; (4) after the loop, 2\*v &gt; N. So v is the largest power of 2 that is ≤ N.

### L2: Multistructural / block x execution / preoperational

L2 for Reasoning about loops: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

Reasoning about loops -&gt; L2 (Multistructural): the answer applies the rules of Reasoning about loops to every part of the code, in order (3 ways).

- **line by line trace** (operational sequencing rule): Order of the argument: show the fact holds after initialisation (before the first test); assume it holds at a test that is true, and show that one execution of the body restores it; show that a measure moves towards making the test false; at exit, combine the fact with the false test.
- **output prediction** (evaluation / result rule): The product is a proven postcondition: after the loop, the invariant AND NOT(condition) holds. For example, v is a power of 2, v ≤ N and 2v &gt; N, so v is the largest power of 2 ≤ N (N = 13 gives 8).
- **one step execution** (state-transition rule): One pass maps a state satisfying the invariant to another state satisfying it. \`v = 2\*v\` (when v ≤ N/2) keeps v a power of 2 and ≤ N, and strictly increases v.

### L3: Relational / relations x function (concrete operational begins)

L3 for Reasoning about loops: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

Reasoning about loops -&gt; L3 (Relational): the answer relates the parts (2 ways).

- **relation to neighbour** (composition rule (with a neighbour)): The invariant is stated at the while test. The while condition supplies the extra fact available inside the body (v ≤ N/2, so 2v ≤ N), and its negation supplies the extra fact after the loop (2v &gt; N).
- **purpose of the whole** (plan / role rule): Purpose: to confirm that a loop computes what is intended for all inputs, not just traced ones, and that it terminates. It is essential for loops like Factors and Binary whose correctness is not obvious.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for Reasoning about loops: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

Reasoning about loops -&gt; L4 (Extended abstract): the answer reasons beyond the given code (5 ways).

- **predict a change** (conservation rule): A change keeps the loop correct only if it keeps the invariant and the progress measure. Changing the test to \`v &lt;= N\` breaks 'v is never greater than N', so the result doubles. Removing the update breaks progress, and the loop runs forever.
- **transfer to a new program** (applicability rule): Use invariant reasoning when a loop's correctness is not evident from a few traces (Factors, Binary, Newton's method) or when changing a loop's bound for performance. Use traces with print statements to check the reasoning on small cases.
- **diagnose an error** (error rule): rule broken: The invariant must hold before the first test. Kind: silent logic error. Trigger class: A wrong initial value (v = 0 is not a power of 2, and the loop never grows it): the argument and the result fail.
- **diagnose an error** (error rule): rule broken: Each pass must re-establish the invariant. Kind: silent logic error. Trigger class: A test or update that lets the last pass overshoot (\`while (v &lt;= N) v = 2\*v;\`): v ends greater than N.
- **diagnose an error** (error rule): rule broken: Some quantity must strictly progress towards making the condition false. Kind: silent logic error. Trigger class: No progress measure (e.g. Collatz-style updates, or a missing update): the termination argument fails, and the loop may run forever.

## Same topic

`loop_invariant_reasoning` belongs to the topic **While loops** (`topic1.3.c`). The topic also contains: `loop_body`, `loop_control`, `while_loop`.

## Rules of the concept (14)

- **folk-meaning rule:** Folk meaning: in everyday life 'convincing yourself' means trying a few cases, so a novice thinks a loop is correct because it worked on the inputs tried. Loop reasoning requires a fact that holds before every test, a reason it survives each pass, and a reason the loop ends, so the argument covers any number of iterations.
- **uneven-application rule:** Applies the reasoning unevenly: the invariant is checked at the start but not after a pass, or at the top of the body on some passes and after the update on others. A loop that breaks the invariant on the last pass then looks correct.
- **identity rule:** Reasoning method: arguing that a loop is correct by stating facts (invariants) that hold each time through it, plus a reason the loop terminates.
- **declarative rule:** For \`int v = 1; while (v &lt;= N/2) v = 2\*v;\`: (1) v is always a power of 2; (2) v is never greater than N; (3) v increases each pass, so the loop terminates; (4) after the loop, 2\*v &gt; N. So v is the largest power of 2 that is ≤ N.
- **operational sequencing rule:** Order of the argument: show the fact holds after initialisation (before the first test); assume it holds at a test that is true, and show that one execution of the body restores it; show that a measure moves towards making the test false; at exit, combine the fact with the false test.
- **evaluation / result rule:** The product is a proven postcondition: after the loop, the invariant AND NOT(condition) holds. For example, v is a power of 2, v ≤ N and 2v &gt; N, so v is the largest power of 2 ≤ N (N = 13 gives 8).
- **state-transition rule:** One pass maps a state satisfying the invariant to another state satisfying it. \`v = 2\*v\` (when v ≤ N/2) keeps v a power of 2 and ≤ N, and strictly increases v.
- **composition rule (with a neighbour):** with while\_loop: The invariant is stated at the while test. The while condition supplies the extra fact available inside the body (v ≤ N/2, so 2v ≤ N), and its negation supplies the extra fact after the loop (2v &gt; N).
- **plan / role rule:** Purpose: to confirm that a loop computes what is intended for all inputs, not just traced ones, and that it terminates. It is essential for loops like Factors and Binary whose correctness is not obvious.
- **conservation rule:** A change keeps the loop correct only if it keeps the invariant and the progress measure. Changing the test to \`v &lt;= N\` breaks 'v is never greater than N', so the result doubles. Removing the update breaks progress, and the loop runs forever.
- **error rule:** rule broken: The invariant must hold before the first test. (silent logic error)
- **error rule:** rule broken: Each pass must re-establish the invariant. (silent logic error)
- **error rule:** rule broken: Some quantity must strictly progress towards making the condition false. (silent logic error)
- **applicability rule:** Use invariant reasoning when a loop's correctness is not evident from a few traces (Factors, Binary, Newton's method) or when changing a loop's bound for performance. Use traces with print statements to check the reasoning on small cases.

## The whole prerequisite chain

- **Everything it builds on (12):** `arithmetic_operators`, `boolean`, `boolean_expression`, `comparison_operators`, `data_type`, `expression`, `identifier`, `literal`, `logical_operators`, `primitive_type`, `variable`, `while_loop`
- **Everything that builds on it (0):** nothing
