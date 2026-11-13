# convergence_rate (`convergence_rate`)

how many iterations the power method needs

Section 1.6 Case Study: Random Web Surfer, topic 1.6.c Mixing a Markov chain (squaring, power method).

![The knowledge graph around convergence_rate](convergence_rate.png)

## At a glance

- **Needs first:** `power_method`
- **Leads to:** nothing
- **Learned alongside:** nothing
- **Misconceptions:** `OneIterationSuffices`
- **Errors:** none
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 12 edges around this concept, each explained in the graph's own words.

## What it needs first (1)

A prerequisite edge means the other concept has to be understood before `convergence_rate`.

### `power_method` comes before `convergence_rate`

*repeated vector-matrix multiplication to compute page ranks*

The convergence rate counts how many power-method multiplications are needed for a given accuracy: about 20 for two decimal places and 20 more for three.

- **Grounding:** book passage
- **How `convergence_rate` combines with `power_method`:** T in Markov is the iteration count whose size the convergence rate fixes: about 20 per decimal digit for tiny.txt.
- **How `power_method` combines with `convergence_rate`:** The number of iterations T controls accuracy: about 20 for two decimals and 20 more for three on tiny.txt.

## What it leads to (0)

These concepts need `convergence_rate` first.

No concept has this one as a prerequisite.

## Learned alongside (0)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

No parallel edge touches this concept.

## Misconceptions (1)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### OneIterationSuffices

- **Wrong rule:** One vector-matrix multiplication gives the exact page ranks.
- **Right rule:** One multiplication gives only the probabilities after one move; the vector converges with repeated multiplication (for tiny.txt about 20 multiplications give two decimal places and about 40 give three).
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: One vector-matrix multiplication gives the exact page ranks. Right rule: Accuracy grows with iterations: about 20 multiplications give two decimal places for tiny.txt and 20 more give three.
- **Shows at level L0 as:** inconsistent trace: Applies LT (run with T, then with more T, compare digits) unevenly: e.g. comparing a run with T = 20 to one with T = 21 and concluding that unchanged digits are accurate. (here mixing in: "One vector-matrix multiplication gives the exact page ranks")
- **Also an edge from `power_method`:** One vector-matrix multiplication gives the exact page ranks.

## Errors (0)

An error edge states the rule that gets broken in a program, and the right rule.

The graph has no error edge from this concept.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for convergence rate: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to convergence rate agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

convergence rate -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (3 ways).

- **everyday reading** (folk-meaning rule): Everyday "converge" means arrive at the answer; numerically the vector only gets closer with each iteration and stops changing in the printed digits, never reaching the limit exactly.
- **misconception** (wrong rule / right rule; shows `OneIterationSuffices`): wrong rule: One vector-matrix multiplication gives the exact page ranks. Right rule: Accuracy grows with iterations: about 20 multiplications give two decimal places for tiny.txt and 20 more give three.
- **inconsistent trace** (uneven-application rule; shows `OneIterationSuffices`): Applies LT (run with T, then with more T, compare digits) unevenly: e.g. comparing a run with T = 20 to one with T = 21 and concluding that unchanged digits are accurate. (here mixing in: "One vector-matrix multiplication gives the exact page ranks")

### L1: Unistructural / atom x text surface

L1 for convergence rate: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

convergence rate -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

- **names the element** (identity rule): A performance measure: the number of iterations a method needs to reach a given number of accurate decimal places.
- **states the rule** (declarative rule): The power method needs about 20 multiplications for two decimal places and another 20 for three on tiny.txt, against tens of thousands and millions of moves for RandomSurfer; Brin and Page report 50 to 100 iterations for the web.

### L2: Multistructural / block x execution / preoperational

L2 for convergence rate: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

convergence rate -&gt; L2 (Multistructural): the answer applies the rules of convergence rate to every part of the code, in order (3 ways).

- **line by line trace** (operational sequencing rule): Run Markov with increasing T (20, 40, ...) and compare the printed vectors; the digits that stop changing are the converged ones.
- **output prediction** (evaluation / result rule): Markov 20 and 40 agree to two decimals (0.27245 vs 0.27303) and the 40-iteration vector is accurate to three.
- **one step execution** (state-transition rule): Each additional iteration shrinks the error by roughly a constant factor determined by the second largest eigenvalue of P, so a fixed number of iterations adds about one digit.

### L3: Relational / relations x function (concrete operational begins)

L3 for convergence rate: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

convergence rate -&gt; L3 (Relational): the answer relates the parts (2 ways).

- **relation to neighbour** (composition rule (with a neighbour)): T in Markov is the iteration count whose size the convergence rate fixes: about 20 per decimal digit for tiny.txt.
- **purpose of the whole** (plan / role rule): Choose the stopping point (iteration count) for an iterative method so that results are accurate to the needed digits without wasted work.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for convergence rate: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

convergence rate -&gt; L4 (Extended abstract): the answer reasons beyond the given code (3 ways).

- **predict a change** (conservation rule; shows `OneIterationSuffices`): Doubling T from 20 to 40 keeps the first two digits and adds one; changing the leap probability or the graph changes the rate (it depends on lambda2).
- **transfer to a new program** (applicability rule): Use convergence measurements whenever an iterative or sampling method must be stopped; it explains why the power method (about 20 iterations per digit) is preferred to simulation (10x moves per digit).
- **diagnose an error** (error rule): rule broken: Enough iterations must be run for the required accuracy. Kind: silent logic error. Trigger class: T chosen too small (or a simulation with too few moves): printed digits look precise but are not accurate.

## Same topic

`convergence_rate` belongs to the topic **Mixing a Markov chain (squaring, power method)** (`topic1.6.c`). The topic also contains: `markov_chain`, `power_method`, `two_models`.

## Rules of the concept (13)

- **folk-meaning rule:** Everyday "converge" means arrive at the answer; numerically the vector only gets closer with each iteration and stops changing in the printed digits, never reaching the limit exactly.
- **wrong rule / right rule:** OneIterationSuffices: wrong: One vector-matrix multiplication gives the exact page ranks. \| right: Accuracy grows with iterations: about 20 multiplications give two decimal places for tiny.txt and 20 more give three.
- **uneven-application rule:** Applies LT (run with T, then with more T, compare digits) unevenly: e.g. comparing a run with T = 20 to one with T = 21 and concluding that unchanged digits are accurate.
- **identity rule:** A performance measure: the number of iterations a method needs to reach a given number of accurate decimal places.
- **declarative rule:** The power method needs about 20 multiplications for two decimal places and another 20 for three on tiny.txt, against tens of thousands and millions of moves for RandomSurfer; Brin and Page report 50 to 100 iterations for the web.
- **operational sequencing rule:** Run Markov with increasing T (20, 40, ...) and compare the printed vectors; the digits that stop changing are the converged ones.
- **evaluation / result rule:** Markov 20 and 40 agree to two decimals (0.27245 vs 0.27303) and the 40-iteration vector is accurate to three.
- **state-transition rule:** Each additional iteration shrinks the error by roughly a constant factor determined by the second largest eigenvalue of P, so a fixed number of iterations adds about one digit.
- **composition rule (with a neighbour):** with power\_method: T in Markov is the iteration count whose size the convergence rate fixes: about 20 per decimal digit for tiny.txt.
- **plan / role rule:** Choose the stopping point (iteration count) for an iterative method so that results are accurate to the needed digits without wasted work.
- **conservation rule:** Doubling T from 20 to 40 keeps the first two digits and adds one; changing the leap probability or the graph changes the rate (it depends on lambda2).
- **error rule:** rule broken: Enough iterations must be run for the required accuracy. (silent logic error)
- **applicability rule:** Use convergence measurements whenever an iterative or sampling method must be stopped; it explains why the power method (about 20 iterations per digit) is preferred to simulation (10x moves per digit).

## The whole prerequisite chain

- **Everything it builds on (31):** `arithmetic_operators`, `array_creation`, `array_declaration`, `array_initializer`, `boolean`, `boolean_expression`, `comparison_operators`, `data_structure`, `data_type`, `do_while_loop`, `expression`, `for_loop`, `identifier`, `indexing`, `input_graph`, `literal`, `logical_operators`, `loop_control`, `loop_variable`, `markov_chain`, `matrix_operations`, `nested_loops`, `power_method`, `primitive_type`, `standard_input`, `stream_model`, `teleportation`, `transition_matrix`, `two_dimensional_array`, `variable`, `while_loop`
- **Everything that builds on it (0):** nothing
