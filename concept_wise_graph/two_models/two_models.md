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

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 21 edges around this concept. The edge logic, the wrong and right rules and the exact rules of the ways are copied word for word from the graph.

## To work on (0)

Nothing is missing for this concept.

## What it needs first (2)

A prerequisite edge means the other concept has to be understood before `two_models`.

### `frequency_counting` comes before `two_models`

*tally visits to estimate page rank*

- **Edge:** `pre:frequency_counting->two_models`
- **Exact edge logic:** The visit fractions freq[j] / T estimate the same page ranks that repeated matrix multiplication computes.
- **Grounding:** book\_passage
- **Composition rule (R) of `two_models` with `frequency_counting`:** freq[j]/T is the simulation's estimate of the same ranks; it carries sampling error the power method does not.
- **Composition rule (R) of `frequency_counting` with `two_models`:** freq[i]/T converges to the same page ranks the power method computes, but only as an estimate.

### `power_method` comes before `two_models`

*repeated vector-matrix multiplication to compute page ranks*

- **Edge:** `pre:power_method->two_models`
- **Exact edge logic:** The power method computes the move probabilities exactly (up to floating-point precision), in contrast to the simulation, which produces an estimate and needs more iterations to get a more accurate estimate.
- **Grounding:** book\_passage
- **Composition rule (R) of `two_models` with `power_method`:** The exact side of the comparison; it reaches two decimals in 20 iterations versus tens of thousands of moves.
- **Composition rule (R) of `power_method` with `two_models`:** Gives the move probabilities exactly (up to floating-point precision), whereas the simulation only estimates them.

## What it leads to (0)

These concepts need `two_models` first.

No concept has this one as a prerequisite.

## Learned alongside (0)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

No parallel edge touches this concept.

## Misconceptions (3)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### FewTrialsAreExact

- **Edge:** `two_models` &rarr; `FewTrialsAreExact` (misconception)
- **Exact edge logic (the wrong rule):** A short simulation gives the exact page ranks.
- **Twin logic (the right rule):** A simulation only estimates the page ranks: RandomSurfer needs 10^n moves to get answers precise to n decimal places and many more moves for those answers to become accurate (tens of thousands of moves for two accurate places, millions for three).
- **Wrong belief (on the node):** A short simulation gives the exact page ranks.
- **Correct rule (on the node):** A simulation only estimates the page ranks: RandomSurfer needs 10^n moves to get answers precise to n decimal places and many more moves for those answers to become accurate (tens of thousands of moves for two accurate places, millions for three).
- **Provenance:** published
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [2] misconception, exact rule:** wrong rule: A short simulation gives the exact page ranks. Right rule: Simulation estimates; tens of thousands of moves give two accurate places and millions give three, whereas the power method needs about 20 and 40 multiplications.
- **Edge `frequency_counting` &rarr; `FewTrialsAreExact`, exact edge logic:** A short simulation gives the exact page ranks. **Twin logic:** A simulation only estimates the page ranks: RandomSurfer needs 10^n moves to get answers precise to n decimal places and many more moves for those answers to become accurate (tens of thousands of moves for two accurate places, millions for three). (role: primary)
- **Edge `monte_carlo_simulation` &rarr; `FewTrialsAreExact`, exact edge logic:** A short simulation gives the exact page ranks. **Twin logic:** A simulation only estimates the page ranks: RandomSurfer needs 10^n moves to get answers precise to n decimal places and many more moves for those answers to become accurate (tens of thousands of moves for two accurate places, millions for three). (role: context)
- **Edge `simulation_loop` &rarr; `FewTrialsAreExact`, exact edge logic:** A short simulation gives the exact page ranks. **Twin logic:** A simulation only estimates the page ranks: RandomSurfer needs 10^n moves to get answers precise to n decimal places and many more moves for those answers to become accurate (tens of thousands of moves for two accurate places, millions for three). (role: context)

### ManyDigitsMeanAccurate

- **Edge:** `two_models` &rarr; `ManyDigitsMeanAccurate` (misconception)
- **Exact edge logic (the wrong rule):** A result printed with many decimal places must be accurate to those places.
- **Twin logic (the right rule):** A program does not produce accurate answers simply because it can print numbers to many decimal places of precision; ensuring accuracy is often the most difficult challenge.
- **Wrong belief (on the node):** A result printed with many decimal places must be accurate to those places.
- **Correct rule (on the node):** A program does not produce accurate answers simply because it can print numbers to many decimal places of precision; ensuring accuracy is often the most difficult challenge.
- **Provenance:** textbook
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [4] misconception, exact rule:** wrong rule: A result printed with many decimal places must be accurate to those places. Right rule: Both programs print five decimals; only the power method after enough iterations is accurate to them.
- **Edge `formatted_output` &rarr; `ManyDigitsMeanAccurate`, exact edge logic:** A result printed with many decimal places must be accurate to those places. **Twin logic:** A program does not produce accurate answers simply because it can print numbers to many decimal places of precision; ensuring accuracy is often the most difficult challenge. (role: context)
- **Edge `frequency_counting` &rarr; `ManyDigitsMeanAccurate`, exact edge logic:** A result printed with many decimal places must be accurate to those places. **Twin logic:** A program does not produce accurate answers simply because it can print numbers to many decimal places of precision; ensuring accuracy is often the most difficult challenge. (role: primary)

### StartPageMatters

- **Edge:** `two_models` &rarr; `StartPageMatters` (misconception)
- **Exact edge logic (the wrong rule):** The page ranks depend on which page the surfer starts from.
- **Twin logic (the right rule):** For the random-surfer chain the long-run probabilities do not depend on the starting page.
- **Wrong belief (on the node):** The page ranks depend on which page the surfer starts from.
- **Correct rule (on the node):** For the random-surfer chain the long-run probabilities do not depend on the starting page.
- **Provenance:** derived
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [1] misconception, exact rule:** wrong rule: The page ranks depend on which page the surfer starts from. Right rule: Both models converge to the same probabilities from any start page.
- **L0 way [3] inconsistent\_trace, exact rule:** Applies the two LTs unevenly: e.g. treats one RandomSurfer move as if it advanced the whole probability vector, or one Markov iteration as if it were one sampled move. (here mixing in: "The page ranks depend on which page the surfer starts from")
- **Edge `markov_chain` &rarr; `StartPageMatters`, exact edge logic:** The page ranks depend on which page the surfer starts from. **Twin logic:** For the random-surfer chain the long-run probabilities do not depend on the starting page. (role: primary)
- **Edge `power_method` &rarr; `StartPageMatters`, exact edge logic:** The page ranks depend on which page the surfer starts from. **Twin logic:** For the random-surfer chain the long-run probabilities do not depend on the starting page. (role: context)

## Errors (0)

An error edge states the rule that gets broken in a program, and the right rule.

The graph has no error edge from this concept.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for two models: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to two models agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

- **Edge:** `two_models` &rarr; `two_models@L0` (has_level)
- **Exact edge logic:** two models -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (5 ways).

Ways (5), each with its exact rule:

- **[0] everyday\_reading** (rule type E, folk-meaning rule): Everyday "model" suggests each program has its own answer; the page ranks are a property of the web model, and simulation and the power method are two ways of computing the same numbers.
- **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `StartPageMatters`: wrong rule: The page ranks depend on which page the surfer starts from. Right rule: Both models converge to the same probabilities from any start page.
- **[2] misconception** (rule type M, wrong rule / right rule) &rarr; `FewTrialsAreExact`: wrong rule: A short simulation gives the exact page ranks. Right rule: Simulation estimates; tens of thousands of moves give two accurate places and millions give three, whereas the power method needs about 20 and 40 multiplications.
- **[3] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `StartPageMatters`: Applies the two LTs unevenly: e.g. treats one RandomSurfer move as if it advanced the whole probability vector, or one Markov iteration as if it were one sampled move. (here mixing in: "The page ranks depend on which page the surfer starts from")
- **[4] misconception** (rule type M, wrong rule / right rule) &rarr; `ManyDigitsMeanAccurate`: wrong rule: A result printed with many decimal places must be accurate to those places. Right rule: Both programs print five decimals; only the power method after enough iterations is accurate to them.

### L1: Unistructural / atom x text surface

L1 for two models: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

- **Edge:** `two_models` &rarr; `two_models@L1` (has_level)
- **Exact edge logic:** two models -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

Ways (2), each with its exact rule:

- **[0] names\_the\_element** (rule type N, identity rule): Two computational approaches to page ranks: simulating a random surfer and counting visits, versus mixing the Markov chain by repeated vector-matrix multiplication.
- **[1] states\_the\_rule** (rule type S, declarative rule): Mixing guarantees a start-independent limit; the power method computes it exactly (up to floating-point precision), whereas the simulation produces an estimate that needs more iterations for more accuracy.

### L2: Multistructural / block x execution / preoperational

L2 for two models: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

- **Edge:** `two_models` &rarr; `two_models@L2` (has_level)
- **Exact edge logic:** two models -&gt; L2 (Multistructural): the answer applies the rules of two models to every part of the code, in order (3 ways).

Ways (3), each with its exact rule:

- **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): Simulation: for T moves, draw r, pick next page, count; then divide counts by T. Power method: for T iterations, multiply the vector by p[][] and replace it; then print the vector.
- **[1] output\_prediction** (rule type OP, evaluation / result rule): Both yield about .273 .266 .146 .247 .068 for tiny.txt (RandomSurfer 1000000 vs Markov 40); page 0 beats page 1 by 27.3% to 26.6%.
- **[2] one\_step\_execution** (rule type OS, state-transition rule): One simulation step changes one page variable and one count; one power-method step changes every entry of the probability vector.

### L3: Relational / relations x function (concrete operational begins)

L3 for two models: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

- **Edge:** `two_models` &rarr; `two_models@L3` (has_level)
- **Exact edge logic:** two models -&gt; L3 (Relational): the answer relates the parts (3 ways).

Ways (3), each with its exact rule:

- **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): freq[j]/T is the simulation's estimate of the same ranks; it carries sampling error the power method does not.
- **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): The exact side of the comparison; it reaches two decimals in 20 iterations versus tens of thousands of moves.
- **[2] purpose\_of\_the\_whole** (rule type P, plan / role rule): Cross-check and choose a method: agreement of an independent estimate (simulation) with the exact computation validates both and shows the cost of each.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for two models: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

- **Edge:** `two_models` &rarr; `two_models@L4` (has_level)
- **Exact edge logic:** two models -&gt; L4 (Extended abstract): the answer reasons beyond the given code (3 ways).

Ways (3), each with its exact rule:

- **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `StartPageMatters`: Changing T or the start page keeps the common limit; rerunning the simulation changes its digits while Markov is deterministic.
- **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Simulate when the process is easy to run but its probabilities are hard to write down; use the power method when the matrix is known and fits in memory, since it is far more efficient.
- **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: Agreement must be judged at the accuracy each method reaches. Kind: silent logic error. Trigger class: Comparing the two outputs digit by digit at five decimals after a short simulation: differences come from sampling error, not from a bug.

## Same topic

`two_models` belongs to the topic **Mixing a Markov chain (squaring, power method)** (`topic1.6.c`). The topic also contains: `convergence_rate`, `markov_chain`, `power_method`.

## Rules of the concept (16)

- **Book** (SW-1e, p. 168 (pdf 178)): "matter where the surfer starts, the process eventually stabilizes to a point where further surfing provides no further information."
- **Book** (SW-1e, p. 168 (pdf 178)): "This phenomenon is known as mixing."
- **Book** (SW-1.6, p. 172 (pdf 182)): "calculate the probabilities for three moves by multiplying by p[][] again"
- **E** (folk-meaning rule): Everyday "model" suggests each program has its own answer; the page ranks are a property of the web model, and simulation and the power method are two ways of computing the same numbers.
- **M** (wrong rule / right rule): FewTrialsAreExact: wrong: A short simulation gives the exact page ranks. \| right: Simulation estimates; tens of thousands of moves give two accurate places and millions give three, whereas the power method needs about 20 and 40 multiplications.
- **M** (wrong rule / right rule): StartPageMatters: wrong: The page ranks depend on which page the surfer starts from. \| right: Both models converge to the same probabilities from any start page.
- **M** (wrong rule / right rule): ManyDigitsMeanAccurate: wrong: A result printed with many decimal places must be accurate to those places. \| right: Both programs print five decimals; only the power method after enough iterations is accurate to them.
- **T** (uneven-application rule): Applies the two LTs unevenly: e.g. treats one RandomSurfer move as if it advanced the whole probability vector, or one Markov iteration as if it were one sampled move.
- **N** (identity rule): Two computational approaches to page ranks: simulating a random surfer and counting visits, versus mixing the Markov chain by repeated vector-matrix multiplication.
- **S** (declarative rule): Mixing guarantees a start-independent limit; the power method computes it exactly (up to floating-point precision), whereas the simulation produces an estimate that needs more iterations for more accuracy.
- **LT** (operational sequencing rule): Simulation: for T moves, draw r, pick next page, count; then divide counts by T. Power method: for T iterations, multiply the vector by p[][] and replace it; then print the vector.
- **OP** (evaluation / result rule): Both yield about .273 .266 .146 .247 .068 for tiny.txt (RandomSurfer 1000000 vs Markov 40); page 0 beats page 1 by 27.3% to 26.6%.
- **OS** (state-transition rule): One simulation step changes one page variable and one count; one power-method step changes every entry of the probability vector.
- **R** (composition rule (with a neighbour)): with frequency\_counting: freq[j]/T is the simulation's estimate of the same ranks; it carries sampling error the power method does not.
- **R** (composition rule (with a neighbour)): with power\_method: The exact side of the comparison; it reaches two decimals in 20 iterations versus tens of thousands of moves.
- **P** (plan / role rule): Cross-check and choose a method: agreement of an independent estimate (simulation) with the exact computation validates both and shows the cost of each.
- **C** (conservation rule): Changing T or the start page keeps the common limit; rerunning the simulation changes its digits while Markov is deterministic.
- **D** (error rule): rule broken: Agreement must be judged at the accuracy each method reaches. (silent logic error)
- **X** (applicability rule): Simulate when the process is easy to run but its probabilities are hard to write down; use the power method when the matrix is known and fits in memory, since it is far more efficient.

## How it is found in code and answers (reader block)

- **Aliases:** estimates, estimate, simulation versus, mixing
- **Code patterns:** none
- **Operator symbols:** none
- **Java types:** none
- **Signal both\_programs** (scope program, decisive): `\bRandomSurfer\b[\s\S]*\bMarkov\b|\bMarkov\b[\s\S]*\bRandomSurfer\b`

## The whole prerequisite chain

- **Everything it builds on (41):** `arithmetic_operators`, `array_creation`, `array_declaration`, `array_initializer`, `assignment`, `boolean`, `boolean_expression`, `comparison_operators`, `counter_pattern`, `data_structure`, `data_type`, `declaration`, `do_while_loop`, `expression`, `for_loop`, `frequency_counting`, `identifier`, `increment_operators`, `indexing`, `input_graph`, `literal`, `logical_operators`, `loop_body`, `loop_control`, `loop_variable`, `markov_chain`, `math_library`, `matrix_operations`, `method_call`, `nested_loops`, `power_method`, `primitive_type`, `random_move`, `simulation_loop`, `standard_input`, `stream_model`, `teleportation`, `transition_matrix`, `two_dimensional_array`, `variable`, `while_loop`
- **Everything that builds on it (0):** nothing

## Every edge in this view and its exact edge logic (21)

All the edges drawn in the picture, in the order: prerequisite, parallel, misconception, error, has_level, contains.

**1. `frequency_counting` &rarr; `two_models`** (prerequisite)

- **Exact edge logic:** The visit fractions freq[j] / T estimate the same page ranks that repeated matrix multiplication computes.
- **Grounding:** book\_passage
- **Composition rule (R) of `frequency_counting` with `two_models`:** freq[i]/T converges to the same page ranks the power method computes, but only as an estimate.
- **Composition rule (R) of `two_models` with `frequency_counting`:** freq[j]/T is the simulation's estimate of the same ranks; it carries sampling error the power method does not.

**2. `power_method` &rarr; `two_models`** (prerequisite)

- **Exact edge logic:** The power method computes the move probabilities exactly (up to floating-point precision), in contrast to the simulation, which produces an estimate and needs more iterations to get a more accurate estimate.
- **Grounding:** book\_passage
- **Composition rule (R) of `power_method` with `two_models`:** Gives the move probabilities exactly (up to floating-point precision), whereas the simulation only estimates them.
- **Composition rule (R) of `two_models` with `power_method`:** The exact side of the comparison; it reaches two decimals in 20 iterations versus tens of thousands of moves.

**3. `two_models` &rarr; `FewTrialsAreExact`** (misconception)

- **Exact edge logic (the wrong rule):** A short simulation gives the exact page ranks.
- **Twin logic (the right rule):** A simulation only estimates the page ranks: RandomSurfer needs 10^n moves to get answers precise to n decimal places and many more moves for those answers to become accurate (tens of thousands of moves for two accurate places, millions for three).
- **Role:** context

**4. `two_models` &rarr; `ManyDigitsMeanAccurate`** (misconception)

- **Exact edge logic (the wrong rule):** A result printed with many decimal places must be accurate to those places.
- **Twin logic (the right rule):** A program does not produce accurate answers simply because it can print numbers to many decimal places of precision; ensuring accuracy is often the most difficult challenge.
- **Role:** context

**5. `two_models` &rarr; `StartPageMatters`** (misconception)

- **Exact edge logic (the wrong rule):** The page ranks depend on which page the surfer starts from.
- **Twin logic (the right rule):** For the random-surfer chain the long-run probabilities do not depend on the starting page.
- **Role:** context

**6. `formatted_output` &rarr; `ManyDigitsMeanAccurate`** (misconception)

- **Exact edge logic (the wrong rule):** A result printed with many decimal places must be accurate to those places.
- **Twin logic (the right rule):** A program does not produce accurate answers simply because it can print numbers to many decimal places of precision; ensuring accuracy is often the most difficult challenge.
- **Role:** context

**7. `frequency_counting` &rarr; `FewTrialsAreExact`** (misconception)

- **Exact edge logic (the wrong rule):** A short simulation gives the exact page ranks.
- **Twin logic (the right rule):** A simulation only estimates the page ranks: RandomSurfer needs 10^n moves to get answers precise to n decimal places and many more moves for those answers to become accurate (tens of thousands of moves for two accurate places, millions for three).
- **Role:** primary

**8. `frequency_counting` &rarr; `ManyDigitsMeanAccurate`** (misconception)

- **Exact edge logic (the wrong rule):** A result printed with many decimal places must be accurate to those places.
- **Twin logic (the right rule):** A program does not produce accurate answers simply because it can print numbers to many decimal places of precision; ensuring accuracy is often the most difficult challenge.
- **Role:** primary

**9. `markov_chain` &rarr; `StartPageMatters`** (misconception)

- **Exact edge logic (the wrong rule):** The page ranks depend on which page the surfer starts from.
- **Twin logic (the right rule):** For the random-surfer chain the long-run probabilities do not depend on the starting page.
- **Role:** primary

**10. `monte_carlo_simulation` &rarr; `FewTrialsAreExact`** (misconception)

- **Exact edge logic (the wrong rule):** A short simulation gives the exact page ranks.
- **Twin logic (the right rule):** A simulation only estimates the page ranks: RandomSurfer needs 10^n moves to get answers precise to n decimal places and many more moves for those answers to become accurate (tens of thousands of moves for two accurate places, millions for three).
- **Role:** context

**11. `power_method` &rarr; `StartPageMatters`** (misconception)

- **Exact edge logic (the wrong rule):** The page ranks depend on which page the surfer starts from.
- **Twin logic (the right rule):** For the random-surfer chain the long-run probabilities do not depend on the starting page.
- **Role:** context

**12. `simulation_loop` &rarr; `FewTrialsAreExact`** (misconception)

- **Exact edge logic (the wrong rule):** A short simulation gives the exact page ranks.
- **Twin logic (the right rule):** A simulation only estimates the page ranks: RandomSurfer needs 10^n moves to get answers precise to n decimal places and many more moves for those answers to become accurate (tens of thousands of moves for two accurate places, millions for three).
- **Role:** context

**13. `two_models` &rarr; `two_models@L0`** (has_level)

- **Exact edge logic:** two models -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (5 ways).
  - **[0] everyday\_reading** (rule type E, folk-meaning rule): Everyday "model" suggests each program has its own answer; the page ranks are a property of the web model, and simulation and the power method are two ways of computing the same numbers.
  - **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `StartPageMatters`: wrong rule: The page ranks depend on which page the surfer starts from. Right rule: Both models converge to the same probabilities from any start page.
  - **[2] misconception** (rule type M, wrong rule / right rule) &rarr; `FewTrialsAreExact`: wrong rule: A short simulation gives the exact page ranks. Right rule: Simulation estimates; tens of thousands of moves give two accurate places and millions give three, whereas the power method needs about 20 and 40 multiplications.
  - **[3] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `StartPageMatters`: Applies the two LTs unevenly: e.g. treats one RandomSurfer move as if it advanced the whole probability vector, or one Markov iteration as if it were one sampled move. (here mixing in: "The page ranks depend on which page the surfer starts from")
  - **[4] misconception** (rule type M, wrong rule / right rule) &rarr; `ManyDigitsMeanAccurate`: wrong rule: A result printed with many decimal places must be accurate to those places. Right rule: Both programs print five decimals; only the power method after enough iterations is accurate to them.

**14. `two_models` &rarr; `two_models@L1`** (has_level)

- **Exact edge logic:** two models -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).
  - **[0] names\_the\_element** (rule type N, identity rule): Two computational approaches to page ranks: simulating a random surfer and counting visits, versus mixing the Markov chain by repeated vector-matrix multiplication.
  - **[1] states\_the\_rule** (rule type S, declarative rule): Mixing guarantees a start-independent limit; the power method computes it exactly (up to floating-point precision), whereas the simulation produces an estimate that needs more iterations for more accuracy.

**15. `two_models` &rarr; `two_models@L2`** (has_level)

- **Exact edge logic:** two models -&gt; L2 (Multistructural): the answer applies the rules of two models to every part of the code, in order (3 ways).
  - **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): Simulation: for T moves, draw r, pick next page, count; then divide counts by T. Power method: for T iterations, multiply the vector by p[][] and replace it; then print the vector.
  - **[1] output\_prediction** (rule type OP, evaluation / result rule): Both yield about .273 .266 .146 .247 .068 for tiny.txt (RandomSurfer 1000000 vs Markov 40); page 0 beats page 1 by 27.3% to 26.6%.
  - **[2] one\_step\_execution** (rule type OS, state-transition rule): One simulation step changes one page variable and one count; one power-method step changes every entry of the probability vector.

**16. `two_models` &rarr; `two_models@L3`** (has_level)

- **Exact edge logic:** two models -&gt; L3 (Relational): the answer relates the parts (3 ways).
  - **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): freq[j]/T is the simulation's estimate of the same ranks; it carries sampling error the power method does not.
  - **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): The exact side of the comparison; it reaches two decimals in 20 iterations versus tens of thousands of moves.
  - **[2] purpose\_of\_the\_whole** (rule type P, plan / role rule): Cross-check and choose a method: agreement of an independent estimate (simulation) with the exact computation validates both and shows the cost of each.

**17. `two_models` &rarr; `two_models@L4`** (has_level)

- **Exact edge logic:** two models -&gt; L4 (Extended abstract): the answer reasons beyond the given code (3 ways).
  - **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `StartPageMatters`: Changing T or the start page keeps the common limit; rerunning the simulation changes its digits while Markov is deterministic.
  - **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Simulate when the process is easy to run but its probabilities are hard to write down; use the power method when the matrix is known and fits in memory, since it is far more efficient.
  - **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: Agreement must be judged at the accuracy each method reaches. Kind: silent logic error. Trigger class: Comparing the two outputs digit by digit at five decimals after a short simulation: differences come from sampling error, not from a bug.

**18. `topic1.6.c` &rarr; `two_models`** (contains)

- topic `topic1.6.c` contains `two_models`

**19. `topic1.6.c` &rarr; `convergence_rate`** (contains)

- topic `topic1.6.c` contains `convergence_rate`

**20. `topic1.6.c` &rarr; `markov_chain`** (contains)

- topic `topic1.6.c` contains `markov_chain`

**21. `topic1.6.c` &rarr; `power_method`** (contains)

- topic `topic1.6.c` contains `power_method`
