# two_models (`two_models`)

simulation vs. repeated matrix multiplication (mixing)

Section 1.6 Case Study: Random Web Surfer, topic 1.6.c Mixing a Markov chain (squaring, power method).

![The knowledge graph around two_models](two_models.png)

## At a glance

- **Needs first:** `frequency_counting`, `power_method`
- **Leads to:** nothing
- **Learned alongside:** nothing
- **Misconceptions:** `FewTrialsAreExact`, `ManyDigitsMeanAccurate`, `StartPageMatters`
- **Errors:** none
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 21 edges around this concept, each explained in the graph's own words.

## What it needs first (2)

A prerequisite edge means the other concept has to be understood before `two_models`.

### `frequency_counting` comes before `two_models`

*tally visits to estimate page rank*

The visit fractions freq[j] / T estimate the same page ranks that repeated matrix multiplication computes.

- **Grounding:** book passage
- **How `two_models` combines with `frequency_counting`:** freq[j]/T is the simulation's estimate of the same ranks; it carries sampling error the power method does not.
- **How `frequency_counting` combines with `two_models`:** freq[i]/T converges to the same page ranks the power method computes, but only as an estimate.

### `power_method` comes before `two_models`

*repeated vector-matrix multiplication to compute page ranks*

The power method computes the move probabilities exactly (up to floating-point precision), in contrast to the simulation, which produces an estimate and needs more iterations to get a more accurate estimate.

- **Grounding:** book passage
- **How `two_models` combines with `power_method`:** The exact side of the comparison; it reaches two decimals in 20 iterations versus tens of thousands of moves.
- **How `power_method` combines with `two_models`:** Gives the move probabilities exactly (up to floating-point precision), whereas the simulation only estimates them.

## What it leads to (0)

These concepts need `two_models` first.

No concept has this one as a prerequisite.

## Learned alongside (0)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

No parallel edge touches this concept.

## Misconceptions (3)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### FewTrialsAreExact

- **Wrong rule:** A short simulation gives the exact page ranks.
- **Right rule:** A simulation only estimates the page ranks: RandomSurfer needs 10^n moves to get answers precise to n decimal places and many more moves for those answers to become accurate (tens of thousands of moves for two accurate places, millions for three).
- **Role of this concept:** context
- **Shows at level L0 as:** misconception: wrong rule: A short simulation gives the exact page ranks. Right rule: Simulation estimates; tens of thousands of moves give two accurate places and millions give three, whereas the power method needs about 20 and 40 multiplications.
- **Also an edge from `frequency_counting`:** A short simulation gives the exact page ranks.
- **Also an edge from `monte_carlo_simulation`:** A short simulation gives the exact page ranks.
- **Also an edge from `simulation_loop`:** A short simulation gives the exact page ranks.

### ManyDigitsMeanAccurate

- **Wrong rule:** A result printed with many decimal places must be accurate to those places.
- **Right rule:** A program does not produce accurate answers simply because it can print numbers to many decimal places of precision; ensuring accuracy is often the most difficult challenge.
- **Role of this concept:** context
- **Shows at level L0 as:** misconception: wrong rule: A result printed with many decimal places must be accurate to those places. Right rule: Both programs print five decimals; only the power method after enough iterations is accurate to them.
- **Also an edge from `formatted_output`:** A result printed with many decimal places must be accurate to those places.
- **Also an edge from `frequency_counting`:** A result printed with many decimal places must be accurate to those places.

### StartPageMatters

- **Wrong rule:** The page ranks depend on which page the surfer starts from.
- **Right rule:** For the random-surfer chain the long-run probabilities do not depend on the starting page.
- **Role of this concept:** context
- **Shows at level L0 as:** misconception: wrong rule: The page ranks depend on which page the surfer starts from. Right rule: Both models converge to the same probabilities from any start page.
- **Shows at level L0 as:** inconsistent trace: Applies the two LTs unevenly: e.g. treats one RandomSurfer move as if it advanced the whole probability vector, or one Markov iteration as if it were one sampled move. (here mixing in: "The page ranks depend on which page the surfer starts from")
- **Also an edge from `markov_chain`:** The page ranks depend on which page the surfer starts from.
- **Also an edge from `power_method`:** The page ranks depend on which page the surfer starts from.

## Errors (0)

An error edge states the rule that gets broken in a program, and the right rule.

The graph has no error edge from this concept.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for two models: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to two models agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

two models -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (5 ways).

- **everyday reading** (folk-meaning rule): Everyday "model" suggests each program has its own answer; the page ranks are a property of the web model, and simulation and the power method are two ways of computing the same numbers.
- **misconception** (wrong rule / right rule; shows `StartPageMatters`): wrong rule: The page ranks depend on which page the surfer starts from. Right rule: Both models converge to the same probabilities from any start page.
- **misconception** (wrong rule / right rule; shows `FewTrialsAreExact`): wrong rule: A short simulation gives the exact page ranks. Right rule: Simulation estimates; tens of thousands of moves give two accurate places and millions give three, whereas the power method needs about 20 and 40 multiplications.
- **inconsistent trace** (uneven-application rule; shows `StartPageMatters`): Applies the two LTs unevenly: e.g. treats one RandomSurfer move as if it advanced the whole probability vector, or one Markov iteration as if it were one sampled move. (here mixing in: "The page ranks depend on which page the surfer starts from")
- **misconception** (wrong rule / right rule; shows `ManyDigitsMeanAccurate`): wrong rule: A result printed with many decimal places must be accurate to those places. Right rule: Both programs print five decimals; only the power method after enough iterations is accurate to them.

### L1: Unistructural / atom x text surface

L1 for two models: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

two models -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

- **names the element** (identity rule): Two computational approaches to page ranks: simulating a random surfer and counting visits, versus mixing the Markov chain by repeated vector-matrix multiplication.
- **states the rule** (declarative rule): Mixing guarantees a start-independent limit; the power method computes it exactly (up to floating-point precision), whereas the simulation produces an estimate that needs more iterations for more accuracy.

### L2: Multistructural / block x execution / preoperational

L2 for two models: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

two models -&gt; L2 (Multistructural): the answer applies the rules of two models to every part of the code, in order (3 ways).

- **line by line trace** (operational sequencing rule): Simulation: for T moves, draw r, pick next page, count; then divide counts by T. Power method: for T iterations, multiply the vector by p[][] and replace it; then print the vector.
- **output prediction** (evaluation / result rule): Both yield about .273 .266 .146 .247 .068 for tiny.txt (RandomSurfer 1000000 vs Markov 40); page 0 beats page 1 by 27.3% to 26.6%.
- **one step execution** (state-transition rule): One simulation step changes one page variable and one count; one power-method step changes every entry of the probability vector.

### L3: Relational / relations x function (concrete operational begins)

L3 for two models: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

two models -&gt; L3 (Relational): the answer relates the parts (3 ways).

- **relation to neighbour** (composition rule (with a neighbour)): freq[j]/T is the simulation's estimate of the same ranks; it carries sampling error the power method does not.
- **relation to neighbour** (composition rule (with a neighbour)): The exact side of the comparison; it reaches two decimals in 20 iterations versus tens of thousands of moves.
- **purpose of the whole** (plan / role rule): Cross-check and choose a method: agreement of an independent estimate (simulation) with the exact computation validates both and shows the cost of each.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for two models: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

two models -&gt; L4 (Extended abstract): the answer reasons beyond the given code (3 ways).

- **predict a change** (conservation rule; shows `StartPageMatters`): Changing T or the start page keeps the common limit; rerunning the simulation changes its digits while Markov is deterministic.
- **transfer to a new program** (applicability rule): Simulate when the process is easy to run but its probabilities are hard to write down; use the power method when the matrix is known and fits in memory, since it is far more efficient.
- **diagnose an error** (error rule): rule broken: Agreement must be judged at the accuracy each method reaches. Kind: silent logic error. Trigger class: Comparing the two outputs digit by digit at five decimals after a short simulation: differences come from sampling error, not from a bug.

## Same topic

`two_models` belongs to the topic **Mixing a Markov chain (squaring, power method)** (`topic1.6.c`). The topic also contains: `convergence_rate`, `markov_chain`, `power_method`.

## Rules of the concept (16)

- **folk-meaning rule:** Everyday "model" suggests each program has its own answer; the page ranks are a property of the web model, and simulation and the power method are two ways of computing the same numbers.
- **wrong rule / right rule:** FewTrialsAreExact: wrong: A short simulation gives the exact page ranks. \| right: Simulation estimates; tens of thousands of moves give two accurate places and millions give three, whereas the power method needs about 20 and 40 multiplications.
- **wrong rule / right rule:** StartPageMatters: wrong: The page ranks depend on which page the surfer starts from. \| right: Both models converge to the same probabilities from any start page.
- **wrong rule / right rule:** ManyDigitsMeanAccurate: wrong: A result printed with many decimal places must be accurate to those places. \| right: Both programs print five decimals; only the power method after enough iterations is accurate to them.
- **uneven-application rule:** Applies the two LTs unevenly: e.g. treats one RandomSurfer move as if it advanced the whole probability vector, or one Markov iteration as if it were one sampled move.
- **identity rule:** Two computational approaches to page ranks: simulating a random surfer and counting visits, versus mixing the Markov chain by repeated vector-matrix multiplication.
- **declarative rule:** Mixing guarantees a start-independent limit; the power method computes it exactly (up to floating-point precision), whereas the simulation produces an estimate that needs more iterations for more accuracy.
- **operational sequencing rule:** Simulation: for T moves, draw r, pick next page, count; then divide counts by T. Power method: for T iterations, multiply the vector by p[][] and replace it; then print the vector.
- **evaluation / result rule:** Both yield about .273 .266 .146 .247 .068 for tiny.txt (RandomSurfer 1000000 vs Markov 40); page 0 beats page 1 by 27.3% to 26.6%.
- **state-transition rule:** One simulation step changes one page variable and one count; one power-method step changes every entry of the probability vector.
- **composition rule (with a neighbour):** with frequency\_counting: freq[j]/T is the simulation's estimate of the same ranks; it carries sampling error the power method does not.
- **composition rule (with a neighbour):** with power\_method: The exact side of the comparison; it reaches two decimals in 20 iterations versus tens of thousands of moves.
- **plan / role rule:** Cross-check and choose a method: agreement of an independent estimate (simulation) with the exact computation validates both and shows the cost of each.
- **conservation rule:** Changing T or the start page keeps the common limit; rerunning the simulation changes its digits while Markov is deterministic.
- **error rule:** rule broken: Agreement must be judged at the accuracy each method reaches. (silent logic error)
- **applicability rule:** Simulate when the process is easy to run but its probabilities are hard to write down; use the power method when the matrix is known and fits in memory, since it is far more efficient.

## The whole prerequisite chain

- **Everything it builds on (41):** `arithmetic_operators`, `array_creation`, `array_declaration`, `array_initializer`, `assignment`, `boolean`, `boolean_expression`, `comparison_operators`, `counter_pattern`, `data_structure`, `data_type`, `declaration`, `do_while_loop`, `expression`, `for_loop`, `frequency_counting`, `identifier`, `increment_operators`, `indexing`, `input_graph`, `literal`, `logical_operators`, `loop_body`, `loop_control`, `loop_variable`, `markov_chain`, `math_library`, `matrix_operations`, `method_call`, `nested_loops`, `power_method`, `primitive_type`, `random_move`, `simulation_loop`, `standard_input`, `stream_model`, `teleportation`, `transition_matrix`, `two_dimensional_array`, `variable`, `while_loop`
- **Everything that builds on it (0):** nothing
