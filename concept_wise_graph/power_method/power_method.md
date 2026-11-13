# power_method (`power_method`)

repeated vector-matrix multiplication to compute page ranks

Section 1.6 Case Study: Random Web Surfer, topic 1.6.c Mixing a Markov chain (squaring, power method).

![The knowledge graph around power_method](power_method.png)

## At a glance

- **Needs first:** `markov_chain`, `matrix_operations`, `two_dimensional_array`
- **Leads to:** `convergence_rate`, `two_models`
- **Learned alongside:** `simulation_loop`
- **Misconceptions:** `MatrixProductCommutes`, `OneIterationSuffices`, `StartPageMatters`
- **Errors:** none
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 22 edges around this concept. The edge logic, the wrong and right rules and the exact rules of the ways are copied word for word from the graph.

## To work on (1)

- no aliases: a student's words cannot name this concept

## What it needs first (3)

A prerequisite edge means the other concept has to be understood before `power_method`.

### `markov_chain` comes before `power_method`

*random process where the next state depends only on the current state*

- **Edge:** `pre:markov_chain->power_method`
- **Exact edge logic:** Each multiplication advances the chain's probabilities by one move.
- **Grounding:** book\_passage
- **Composition rule (R) of `power_method` with `markov_chain`:** Each multiplication is one move of the chain; convergence is the chain's mixing.
- **Composition rule (R) of `markov_chain` with `power_method`:** Each vector-matrix multiplication advances the chain's probabilities by one move; repeating it approaches the stationary vector.

### `matrix_operations` comes before `power_method`

*matrix addition and multiplication with nested loops*

- **Edge:** `pre:matrix_operations->power_method`
- **Exact edge logic:** The power method is repeated vector-matrix multiplication.
- **Grounding:** book\_passage
- **Composition rule (R) of `power_method` with `matrix_operations`:** Each iteration is a vector-matrix product: newRank[j] is the dot product of rank[] and column j of p[][], computed with nested for loops.
- **Composition rule (R) of `matrix_operations` with `power_method`:** The power method repeats vector-matrix multiplication rather than matrix-matrix multiplication, because that is all it needs.

### `two_dimensional_array` comes before `power_method`

*an array of arrays (a[i][j])*

- **Edge:** `pre:two_dimensional_array->power_method`
- **Exact edge logic:** The power method multiplies the rank vector by the transition matrix, stored as a two-dimensional array p[i][j].
- **Grounding:** book\_passage

## What it leads to (2)

These concepts need `power_method` first.

### `power_method` comes before `convergence_rate`

*how many iterations the power method needs*

- **Edge:** `pre:power_method->convergence_rate`
- **Exact edge logic:** The convergence rate counts how many power-method multiplications are needed for a given accuracy: about 20 for two decimal places and 20 more for three.
- **Grounding:** book\_passage
- **Composition rule (R) of `power_method` with `convergence_rate`:** The number of iterations T controls accuracy: about 20 for two decimals and 20 more for three on tiny.txt.
- **Composition rule (R) of `convergence_rate` with `power_method`:** T in Markov is the iteration count whose size the convergence rate fixes: about 20 per decimal digit for tiny.txt.

### `power_method` comes before `two_models`

*simulation vs. repeated matrix multiplication (mixing)*

- **Edge:** `pre:power_method->two_models`
- **Exact edge logic:** The power method computes the move probabilities exactly (up to floating-point precision), in contrast to the simulation, which produces an estimate and needs more iterations to get a more accurate estimate.
- **Grounding:** book\_passage
- **Composition rule (R) of `power_method` with `two_models`:** Gives the move probabilities exactly (up to floating-point precision), whereas the simulation only estimates them.
- **Composition rule (R) of `two_models` with `power_method`:** The exact side of the comparison; it reaches two decimals in 20 iterations versus tens of thousands of moves.

## Learned alongside (1)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

### `power_method` alongside `simulation_loop`

*take many random steps*

- **Edge:** `par:simulation_loop~power_method`
- **Exact edge logic:** The power method used in Markov is far more efficient than simulating the behavior of a random surfer.
- **Grounding:** book\_passage
- **Composition rule (R) of `power_method` with `simulation_loop`:** Computes the same ranks far more efficiently than simulating moves.
- **Composition rule (R) of `simulation_loop` with `power_method`:** Both compute the same page ranks; the power method gets them exactly with far fewer iterations.

## Misconceptions (3)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### MatrixProductCommutes

- **Edge:** `power_method` &rarr; `MatrixProductCommutes` (misconception)
- **Exact edge logic (the wrong rule):** A \* B and B \* A are the same matrix.
- **Twin logic (the right rule):** Matrix multiplication is not commutative; changing the order may change the product.
- **Wrong belief (on the node):** A \* B and B \* A are the same matrix.
- **Correct rule (on the node):** Matrix multiplication is not commutative; changing the order may change the product.
- **Provenance:** textbook
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [3] misconception, exact rule:** wrong rule: A \* B and B \* A are the same matrix. Right rule: Matrix multiplication is not commutative: c[i][j] is row i of the left factor dotted with column j of the right; rank \* p (row vector times matrix) is the page-rank update, p \* rank is a different vector.
- **Edge `matrix_operations` &rarr; `MatrixProductCommutes`, exact edge logic:** A \* B and B \* A are the same matrix. **Twin logic:** Matrix multiplication is not commutative; changing the order may change the product. (role: primary)

### OneIterationSuffices

- **Edge:** `power_method` &rarr; `OneIterationSuffices` (misconception)
- **Exact edge logic (the wrong rule):** One vector-matrix multiplication gives the exact page ranks.
- **Twin logic (the right rule):** One multiplication gives only the probabilities after one move; the vector converges with repeated multiplication (for tiny.txt about 20 multiplications give two decimal places and about 40 give three).
- **Wrong belief (on the node):** One vector-matrix multiplication gives the exact page ranks.
- **Correct rule (on the node):** One multiplication gives only the probabilities after one move; the vector converges with repeated multiplication (for tiny.txt about 20 multiplications give two decimal places and about 40 give three).
- **Provenance:** derived
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [2] misconception, exact rule:** wrong rule: One vector-matrix multiplication gives the exact page ranks. Right rule: One multiplication gives the probabilities after one move ([.02 .92 .02 .02 .02] from page 0); about 20 multiplications give two decimal places and 20 more give three.
- **Edge `convergence_rate` &rarr; `OneIterationSuffices`, exact edge logic:** One vector-matrix multiplication gives the exact page ranks. **Twin logic:** One multiplication gives only the probabilities after one move; the vector converges with repeated multiplication (for tiny.txt about 20 multiplications give two decimal places and about 40 give three). (role: primary)

### StartPageMatters

- **Edge:** `power_method` &rarr; `StartPageMatters` (misconception)
- **Exact edge logic (the wrong rule):** The page ranks depend on which page the surfer starts from.
- **Twin logic (the right rule):** For the random-surfer chain the long-run probabilities do not depend on the starting page.
- **Wrong belief (on the node):** The page ranks depend on which page the surfer starts from.
- **Correct rule (on the node):** For the random-surfer chain the long-run probabilities do not depend on the starting page.
- **Provenance:** derived
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [1] misconception, exact rule:** wrong rule: The page ranks depend on which page the surfer starts from. Right rule: The iteration converges to the same vector no matter where it starts; Markov starts from [1.0 0 0 0 0] only for convenience.
- **L0 way [4] inconsistent\_trace, exact rule:** Applies LT (compute all of newRank from the old rank, then copy) unevenly: e.g. on some passes writing rank[j] directly so later j use partly updated values, or forgetting to recreate newRank so sums accumulate. (here mixing in: "The page ranks depend on which page the surfer starts from")
- **Edge `markov_chain` &rarr; `StartPageMatters`, exact edge logic:** The page ranks depend on which page the surfer starts from. **Twin logic:** For the random-surfer chain the long-run probabilities do not depend on the starting page. (role: primary)
- **Edge `two_models` &rarr; `StartPageMatters`, exact edge logic:** The page ranks depend on which page the surfer starts from. **Twin logic:** For the random-surfer chain the long-run probabilities do not depend on the starting page. (role: context)

## Errors (0)

An error edge states the rule that gets broken in a program, and the right rule.

The graph has no error edge from this concept.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for power method: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to power method agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

- **Edge:** `power_method` &rarr; `power_method@L0` (has_level)
- **Exact edge logic:** power method -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (5 ways).

Ways (5), each with its exact rule:

- **[0] everyday\_reading** (rule type E, folk-meaning rule): "Power" suggests strength or Math.pow on a number; here it means raising the transition matrix to the t-th power by multiplying a probability vector by p[][] t times.
- **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `StartPageMatters`: wrong rule: The page ranks depend on which page the surfer starts from. Right rule: The iteration converges to the same vector no matter where it starts; Markov starts from [1.0 0 0 0 0] only for convenience.
- **[2] misconception** (rule type M, wrong rule / right rule) &rarr; `OneIterationSuffices`: wrong rule: One vector-matrix multiplication gives the exact page ranks. Right rule: One multiplication gives the probabilities after one move ([.02 .92 .02 .02 .02] from page 0); about 20 multiplications give two decimal places and 20 more give three.
- **[3] misconception** (rule type M, wrong rule / right rule) &rarr; `MatrixProductCommutes`: wrong rule: A \* B and B \* A are the same matrix. Right rule: Matrix multiplication is not commutative: c[i][j] is row i of the left factor dotted with column j of the right; rank \* p (row vector times matrix) is the page-rank update, p \* rank is a different vector.
- **[4] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `StartPageMatters`: Applies LT (compute all of newRank from the old rank, then copy) unevenly: e.g. on some passes writing rank[j] directly so later j use partly updated values, or forgetting to recreate newRank so sums accumulate. (here mixing in: "The page ranks depend on which page the surfer starts from")

### L1: Unistructural / atom x text surface

L1 for power method: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

- **Edge:** `power_method` &rarr; `power_method@L1` (has_level)
- **Exact edge logic:** power method -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

Ways (2), each with its exact rule:

- **[0] names\_the\_element** (rule type N, identity rule): An iterative algorithm: repeated vector-matrix multiplication of a probability vector by the transition matrix.
- **[1] states\_the\_rule** (rule type S, declarative rule): The vector of probabilities after t steps is the vector after t-1 steps times the transition matrix; by the basic limit theorem this converges to the same vector from any start.

### L2: Multistructural / block x execution / preoperational

L2 for power method: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

- **Edge:** `power_method` &rarr; `power_method@L2` (has_level)
- **Exact edge logic:** power method -&gt; L2 (Multistructural): the answer applies the rules of power method to every part of the code, in order (3 ways).

Ways (3), each with its exact rule:

- **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): rank = [1, 0, ..., 0]; for each t: create newRank (zeros); for each j, for each k, newRank[j] += rank[k]\*p[k][j]; then copy newRank into rank. Finally print rank.
- **[1] output\_prediction** (rule type OP, evaluation / result rule): Prints the page-rank vector after T multiplications: Markov 20 gives 0.27245 0.26515 0.14669 0.24764 0.06806 and Markov 40 gives 0.27303 0.26573 0.14618 0.24723 0.06783.
- **[2] one\_step\_execution** (rule type OS, state-transition rule): One iteration replaces every rank[j] with the dot product of the old rank and column j of p; the vector still sums to 1.

### L3: Relational / relations x function (concrete operational begins)

L3 for power method: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

- **Edge:** `power_method` &rarr; `power_method@L3` (has_level)
- **Exact edge logic:** power method -&gt; L3 (Relational): the answer relates the parts (6 ways).

Ways (6), each with its exact rule:

- **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Each iteration is a vector-matrix product: newRank[j] is the dot product of rank[] and column j of p[][], computed with nested for loops.
- **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Each multiplication is one move of the chain; convergence is the chain's mixing.
- **[2] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Gives the move probabilities exactly (up to floating-point precision), whereas the simulation only estimates them.
- **[3] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): The number of iterations T controls accuracy: about 20 for two decimals and 20 more for three on tiny.txt.
- **[4] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Computes the same ranks far more efficiently than simulating moves.
- **[5] purpose\_of\_the\_whole** (rule type P, plan / role rule): Iterative-refinement plan: repeat the same update until the vector stops changing; newRank[j] is a gatherer (dot product), rank is the state vector replaced each pass.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for power method: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

- **Edge:** `power_method` &rarr; `power_method@L4` (has_level)
- **Exact edge logic:** power method -&gt; L4 (Extended abstract): the answer reasons beyond the given code (6 ways).

Ways (6), each with its exact rule:

- **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `StartPageMatters`: Changing the start vector keeps the limit; more iterations keep the result and add digits; updating rank in place, or using p[j][k] instead of p[k][j], breaks the computation.
- **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Use when the transition matrix fits in memory and accurate ranks are needed: far more efficient than simulation; still too slow for the whole web, and repeated squaring is an alternative.
- **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: The new vector must be computed from the old vector only. Kind: silent logic error. Trigger class: rank[j] updated in place (no newRank): later columns use already-updated ranks, so the result is not rank \* p (though it may still converge).
- **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: newRank must start at zero each iteration. Kind: silent logic error. Trigger class: newRank created once outside the t loop: sums accumulate across iterations and the vector grows beyond 1.
- **[4] diagnose\_an\_error** (rule type D, error rule): rule broken: The update is rank (row) times p: use column j of p, p[k][j]. Kind: silent logic error. Trigger class: Using p[j][k] (row j) computes p \* rank instead, which does not give the page ranks.
- **[5] diagnose\_an\_error** (rule type D, error rule): rule broken: Many iterations are needed for convergence. Kind: silent logic error. Trigger class: T too small (e.g. 1 or 2): prints the 1- or 2-move probabilities, not the ranks.

## Same topic

`power_method` belongs to the topic **Mixing a Markov chain (squaring, power method)** (`topic1.6.c`). The topic also contains: `convergence_rate`, `markov_chain`, `two_models`.

## Rules of the concept (22)

- **Book** (SW-1e, p. 172 (pdf 182)): "However, matrix-matrix multiplication is expensive, and we are actually interested in a vector-matrix calculation."
- **Book** (SW-1.6, p. 172 (pdf 182)): "matrix–matrix multiplication is expensive, and we are actually interested in a vector–matrix calculation"
- **E** (folk-meaning rule): "Power" suggests strength or Math.pow on a number; here it means raising the transition matrix to the t-th power by multiplying a probability vector by p[][] t times.
- **M** (wrong rule / right rule): MatrixProductCommutes: wrong: A \* B and B \* A are the same matrix. \| right: Matrix multiplication is not commutative: c[i][j] is row i of the left factor dotted with column j of the right; rank \* p (row vector times matrix) is the page-rank update, p \* rank is a different vector.
- **M** (wrong rule / right rule): OneIterationSuffices: wrong: One vector-matrix multiplication gives the exact page ranks. \| right: One multiplication gives the probabilities after one move ([.02 .92 .02 .02 .02] from page 0); about 20 multiplications give two decimal places and 20 more give three.
- **M** (wrong rule / right rule): StartPageMatters: wrong: The page ranks depend on which page the surfer starts from. \| right: The iteration converges to the same vector no matter where it starts; Markov starts from [1.0 0 0 0 0] only for convenience.
- **T** (uneven-application rule): Applies LT (compute all of newRank from the old rank, then copy) unevenly: e.g. on some passes writing rank[j] directly so later j use partly updated values, or forgetting to recreate newRank so sums accumulate.
- **N** (identity rule): An iterative algorithm: repeated vector-matrix multiplication of a probability vector by the transition matrix.
- **S** (declarative rule): The vector of probabilities after t steps is the vector after t-1 steps times the transition matrix; by the basic limit theorem this converges to the same vector from any start.
- **LT** (operational sequencing rule): rank = [1, 0, ..., 0]; for each t: create newRank (zeros); for each j, for each k, newRank[j] += rank[k]\*p[k][j]; then copy newRank into rank. Finally print rank.
- **OP** (evaluation / result rule): Prints the page-rank vector after T multiplications: Markov 20 gives 0.27245 0.26515 0.14669 0.24764 0.06806 and Markov 40 gives 0.27303 0.26573 0.14618 0.24723 0.06783.
- **OS** (state-transition rule): One iteration replaces every rank[j] with the dot product of the old rank and column j of p; the vector still sums to 1.
- **R** (composition rule (with a neighbour)): with matrix\_operations: Each iteration is a vector-matrix product: newRank[j] is the dot product of rank[] and column j of p[][], computed with nested for loops.
- **R** (composition rule (with a neighbour)): with markov\_chain: Each multiplication is one move of the chain; convergence is the chain's mixing.
- **R** (composition rule (with a neighbour)): with two\_models: Gives the move probabilities exactly (up to floating-point precision), whereas the simulation only estimates them.
- **R** (composition rule (with a neighbour)): with convergence\_rate: The number of iterations T controls accuracy: about 20 for two decimals and 20 more for three on tiny.txt.
- **R** (composition rule (with a neighbour)): with simulation\_loop: Computes the same ranks far more efficiently than simulating moves.
- **P** (plan / role rule): Iterative-refinement plan: repeat the same update until the vector stops changing; newRank[j] is a gatherer (dot product), rank is the state vector replaced each pass.
- **C** (conservation rule): Changing the start vector keeps the limit; more iterations keep the result and add digits; updating rank in place, or using p[j][k] instead of p[k][j], breaks the computation.
- **D** (error rule): rule broken: The new vector must be computed from the old vector only. (silent logic error)
- **D** (error rule): rule broken: newRank must start at zero each iteration. (silent logic error)
- **D** (error rule): rule broken: The update is rank (row) times p: use column j of p, p[k][j]. (silent logic error)
- **D** (error rule): rule broken: Many iterations are needed for convergence. (silent logic error)
- **X** (applicability rule): Use when the transition matrix fits in memory and accurate ranks are needed: far more efficient than simulation; still too slow for the whole web, and repeated squaring is an alternative.

## How it is found in code and answers (reader block)

- **Aliases:** none
- **Code patterns:** `\bMarkov\b`, `\bnewRanks?\b`, `\branks?\s*\[[^\]]+\]\s*\+=\s*\w+\s*\[[^\]]+\]\s*\*\s*\w+\s*\[[^\]]+\]\s*\[[^\]]+\]`
- **Operator symbols:** none
- **Java types:** none

## The whole prerequisite chain

- **Everything it builds on (30):** `arithmetic_operators`, `array_creation`, `array_declaration`, `array_initializer`, `boolean`, `boolean_expression`, `comparison_operators`, `data_structure`, `data_type`, `do_while_loop`, `expression`, `for_loop`, `identifier`, `indexing`, `input_graph`, `literal`, `logical_operators`, `loop_control`, `loop_variable`, `markov_chain`, `matrix_operations`, `nested_loops`, `primitive_type`, `standard_input`, `stream_model`, `teleportation`, `transition_matrix`, `two_dimensional_array`, `variable`, `while_loop`
- **Everything that builds on it (2):** `convergence_rate`, `two_models`

## Every edge in this view and its exact edge logic (22)

All the edges drawn in the picture, in the order: prerequisite, parallel, misconception, error, has_level, contains.

**1. `markov_chain` &rarr; `power_method`** (prerequisite)

- **Exact edge logic:** Each multiplication advances the chain's probabilities by one move.
- **Grounding:** book\_passage
- **Composition rule (R) of `markov_chain` with `power_method`:** Each vector-matrix multiplication advances the chain's probabilities by one move; repeating it approaches the stationary vector.
- **Composition rule (R) of `power_method` with `markov_chain`:** Each multiplication is one move of the chain; convergence is the chain's mixing.

**2. `matrix_operations` &rarr; `power_method`** (prerequisite)

- **Exact edge logic:** The power method is repeated vector-matrix multiplication.
- **Grounding:** book\_passage
- **Composition rule (R) of `matrix_operations` with `power_method`:** The power method repeats vector-matrix multiplication rather than matrix-matrix multiplication, because that is all it needs.
- **Composition rule (R) of `power_method` with `matrix_operations`:** Each iteration is a vector-matrix product: newRank[j] is the dot product of rank[] and column j of p[][], computed with nested for loops.

**3. `power_method` &rarr; `convergence_rate`** (prerequisite)

- **Exact edge logic:** The convergence rate counts how many power-method multiplications are needed for a given accuracy: about 20 for two decimal places and 20 more for three.
- **Grounding:** book\_passage
- **Composition rule (R) of `power_method` with `convergence_rate`:** The number of iterations T controls accuracy: about 20 for two decimals and 20 more for three on tiny.txt.
- **Composition rule (R) of `convergence_rate` with `power_method`:** T in Markov is the iteration count whose size the convergence rate fixes: about 20 per decimal digit for tiny.txt.

**4. `power_method` &rarr; `two_models`** (prerequisite)

- **Exact edge logic:** The power method computes the move probabilities exactly (up to floating-point precision), in contrast to the simulation, which produces an estimate and needs more iterations to get a more accurate estimate.
- **Grounding:** book\_passage
- **Composition rule (R) of `power_method` with `two_models`:** Gives the move probabilities exactly (up to floating-point precision), whereas the simulation only estimates them.
- **Composition rule (R) of `two_models` with `power_method`:** The exact side of the comparison; it reaches two decimals in 20 iterations versus tens of thousands of moves.

**5. `two_dimensional_array` &rarr; `power_method`** (prerequisite)

- **Exact edge logic:** The power method multiplies the rank vector by the transition matrix, stored as a two-dimensional array p[i][j].
- **Grounding:** book\_passage

**6. `simulation_loop` &harr; `power_method`** (parallel)

- **Exact edge logic:** The power method used in Markov is far more efficient than simulating the behavior of a random surfer.
- **Grounding:** book\_passage
- **Composition rule (R) of `simulation_loop` with `power_method`:** Both compute the same page ranks; the power method gets them exactly with far fewer iterations.
- **Composition rule (R) of `power_method` with `simulation_loop`:** Computes the same ranks far more efficiently than simulating moves.

**7. `power_method` &rarr; `MatrixProductCommutes`** (misconception)

- **Exact edge logic (the wrong rule):** A \* B and B \* A are the same matrix.
- **Twin logic (the right rule):** Matrix multiplication is not commutative; changing the order may change the product.
- **Role:** context

**8. `power_method` &rarr; `OneIterationSuffices`** (misconception)

- **Exact edge logic (the wrong rule):** One vector-matrix multiplication gives the exact page ranks.
- **Twin logic (the right rule):** One multiplication gives only the probabilities after one move; the vector converges with repeated multiplication (for tiny.txt about 20 multiplications give two decimal places and about 40 give three).
- **Role:** context

**9. `power_method` &rarr; `StartPageMatters`** (misconception)

- **Exact edge logic (the wrong rule):** The page ranks depend on which page the surfer starts from.
- **Twin logic (the right rule):** For the random-surfer chain the long-run probabilities do not depend on the starting page.
- **Role:** context

**10. `convergence_rate` &rarr; `OneIterationSuffices`** (misconception)

- **Exact edge logic (the wrong rule):** One vector-matrix multiplication gives the exact page ranks.
- **Twin logic (the right rule):** One multiplication gives only the probabilities after one move; the vector converges with repeated multiplication (for tiny.txt about 20 multiplications give two decimal places and about 40 give three).
- **Role:** primary

**11. `markov_chain` &rarr; `StartPageMatters`** (misconception)

- **Exact edge logic (the wrong rule):** The page ranks depend on which page the surfer starts from.
- **Twin logic (the right rule):** For the random-surfer chain the long-run probabilities do not depend on the starting page.
- **Role:** primary

**12. `matrix_operations` &rarr; `MatrixProductCommutes`** (misconception)

- **Exact edge logic (the wrong rule):** A \* B and B \* A are the same matrix.
- **Twin logic (the right rule):** Matrix multiplication is not commutative; changing the order may change the product.
- **Role:** primary

**13. `two_models` &rarr; `StartPageMatters`** (misconception)

- **Exact edge logic (the wrong rule):** The page ranks depend on which page the surfer starts from.
- **Twin logic (the right rule):** For the random-surfer chain the long-run probabilities do not depend on the starting page.
- **Role:** context

**14. `power_method` &rarr; `power_method@L0`** (has_level)

- **Exact edge logic:** power method -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (5 ways).
  - **[0] everyday\_reading** (rule type E, folk-meaning rule): "Power" suggests strength or Math.pow on a number; here it means raising the transition matrix to the t-th power by multiplying a probability vector by p[][] t times.
  - **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `StartPageMatters`: wrong rule: The page ranks depend on which page the surfer starts from. Right rule: The iteration converges to the same vector no matter where it starts; Markov starts from [1.0 0 0 0 0] only for convenience.
  - **[2] misconception** (rule type M, wrong rule / right rule) &rarr; `OneIterationSuffices`: wrong rule: One vector-matrix multiplication gives the exact page ranks. Right rule: One multiplication gives the probabilities after one move ([.02 .92 .02 .02 .02] from page 0); about 20 multiplications give two decimal places and 20 more give three.
  - **[3] misconception** (rule type M, wrong rule / right rule) &rarr; `MatrixProductCommutes`: wrong rule: A \* B and B \* A are the same matrix. Right rule: Matrix multiplication is not commutative: c[i][j] is row i of the left factor dotted with column j of the right; rank \* p (row vector times matrix) is the page-rank update, p \* rank is a different vector.
  - **[4] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `StartPageMatters`: Applies LT (compute all of newRank from the old rank, then copy) unevenly: e.g. on some passes writing rank[j] directly so later j use partly updated values, or forgetting to recreate newRank so sums accumulate. (here mixing in: "The page ranks depend on which page the surfer starts from")

**15. `power_method` &rarr; `power_method@L1`** (has_level)

- **Exact edge logic:** power method -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).
  - **[0] names\_the\_element** (rule type N, identity rule): An iterative algorithm: repeated vector-matrix multiplication of a probability vector by the transition matrix.
  - **[1] states\_the\_rule** (rule type S, declarative rule): The vector of probabilities after t steps is the vector after t-1 steps times the transition matrix; by the basic limit theorem this converges to the same vector from any start.

**16. `power_method` &rarr; `power_method@L2`** (has_level)

- **Exact edge logic:** power method -&gt; L2 (Multistructural): the answer applies the rules of power method to every part of the code, in order (3 ways).
  - **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): rank = [1, 0, ..., 0]; for each t: create newRank (zeros); for each j, for each k, newRank[j] += rank[k]\*p[k][j]; then copy newRank into rank. Finally print rank.
  - **[1] output\_prediction** (rule type OP, evaluation / result rule): Prints the page-rank vector after T multiplications: Markov 20 gives 0.27245 0.26515 0.14669 0.24764 0.06806 and Markov 40 gives 0.27303 0.26573 0.14618 0.24723 0.06783.
  - **[2] one\_step\_execution** (rule type OS, state-transition rule): One iteration replaces every rank[j] with the dot product of the old rank and column j of p; the vector still sums to 1.

**17. `power_method` &rarr; `power_method@L3`** (has_level)

- **Exact edge logic:** power method -&gt; L3 (Relational): the answer relates the parts (6 ways).
  - **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Each iteration is a vector-matrix product: newRank[j] is the dot product of rank[] and column j of p[][], computed with nested for loops.
  - **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Each multiplication is one move of the chain; convergence is the chain's mixing.
  - **[2] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Gives the move probabilities exactly (up to floating-point precision), whereas the simulation only estimates them.
  - **[3] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): The number of iterations T controls accuracy: about 20 for two decimals and 20 more for three on tiny.txt.
  - **[4] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Computes the same ranks far more efficiently than simulating moves.
  - **[5] purpose\_of\_the\_whole** (rule type P, plan / role rule): Iterative-refinement plan: repeat the same update until the vector stops changing; newRank[j] is a gatherer (dot product), rank is the state vector replaced each pass.

**18. `power_method` &rarr; `power_method@L4`** (has_level)

- **Exact edge logic:** power method -&gt; L4 (Extended abstract): the answer reasons beyond the given code (6 ways).
  - **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `StartPageMatters`: Changing the start vector keeps the limit; more iterations keep the result and add digits; updating rank in place, or using p[j][k] instead of p[k][j], breaks the computation.
  - **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Use when the transition matrix fits in memory and accurate ranks are needed: far more efficient than simulation; still too slow for the whole web, and repeated squaring is an alternative.
  - **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: The new vector must be computed from the old vector only. Kind: silent logic error. Trigger class: rank[j] updated in place (no newRank): later columns use already-updated ranks, so the result is not rank \* p (though it may still converge).
  - **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: newRank must start at zero each iteration. Kind: silent logic error. Trigger class: newRank created once outside the t loop: sums accumulate across iterations and the vector grows beyond 1.
  - **[4] diagnose\_an\_error** (rule type D, error rule): rule broken: The update is rank (row) times p: use column j of p, p[k][j]. Kind: silent logic error. Trigger class: Using p[j][k] (row j) computes p \* rank instead, which does not give the page ranks.
  - **[5] diagnose\_an\_error** (rule type D, error rule): rule broken: Many iterations are needed for convergence. Kind: silent logic error. Trigger class: T too small (e.g. 1 or 2): prints the 1- or 2-move probabilities, not the ranks.

**19. `topic1.6.c` &rarr; `power_method`** (contains)

- topic `topic1.6.c` contains `power_method`

**20. `topic1.6.c` &rarr; `convergence_rate`** (contains)

- topic `topic1.6.c` contains `convergence_rate`

**21. `topic1.6.c` &rarr; `markov_chain`** (contains)

- topic `topic1.6.c` contains `markov_chain`

**22. `topic1.6.c` &rarr; `two_models`** (contains)

- topic `topic1.6.c` contains `two_models`
