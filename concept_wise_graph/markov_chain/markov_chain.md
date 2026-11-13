# markov_chain (`markov_chain`)

random process where the next state depends only on the current state

Section 1.6 Case Study: Random Web Surfer, topic 1.6.c Mixing a Markov chain (squaring, power method).

![The knowledge graph around markov_chain](markov_chain.png)

## At a glance

- **Needs first:** `transition_matrix`
- **Leads to:** `power_method`
- **Learned alongside:** nothing
- **Misconceptions:** `StartPageMatters`
- **Errors:** none
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 14 edges around this concept. The edge logic, the wrong and right rules and the exact rules of the ways are copied word for word from the graph.

## To work on (0)

Nothing is missing for this concept.

## What it needs first (1)

A prerequisite edge means the other concept has to be understood before `markov_chain`.

### `transition_matrix` comes before `markov_chain`

*a 2-D array of move probabilities (rows sum to 1)*

- **Edge:** `pre:transition_matrix->markov_chain`
- **Exact edge logic:** The transition matrix specifies the probability of each move, and the random process those probabilities define is a Markov chain.
- **Grounding:** book\_passage
- **Composition rule (R) of `markov_chain` with `transition_matrix`:** The chain is defined by the matrix: it must be square with every row a probability distribution.
- **Composition rule (R) of `transition_matrix` with `markov_chain`:** A matrix whose rows are probability distributions defines a Markov chain: the next page depends only on the current page's row.

## What it leads to (1)

These concepts need `markov_chain` first.

### `markov_chain` comes before `power_method`

*repeated vector-matrix multiplication to compute page ranks*

- **Edge:** `pre:markov_chain->power_method`
- **Exact edge logic:** Each multiplication advances the chain's probabilities by one move.
- **Grounding:** book\_passage
- **Composition rule (R) of `markov_chain` with `power_method`:** Each vector-matrix multiplication advances the chain's probabilities by one move; repeating it approaches the stationary vector.
- **Composition rule (R) of `power_method` with `markov_chain`:** Each multiplication is one move of the chain; convergence is the chain's mixing.

## Learned alongside (0)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

No parallel edge touches this concept.

## Misconceptions (1)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### StartPageMatters

- **Edge:** `markov_chain` &rarr; `StartPageMatters` (misconception)
- **Exact edge logic (the wrong rule):** The page ranks depend on which page the surfer starts from.
- **Twin logic (the right rule):** For the random-surfer chain the long-run probabilities do not depend on the starting page.
- **Wrong belief (on the node):** The page ranks depend on which page the surfer starts from.
- **Correct rule (on the node):** For the random-surfer chain the long-run probabilities do not depend on the starting page.
- **Provenance:** derived
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [1] misconception, exact rule:** wrong rule: The page ranks depend on which page the surfer starts from. Right rule: For the random-surfer chain the long-run probabilities are the same for all starting pages (basic limit theorem); that is why RandomSurfer can start at page 0.
- **L0 way [2] inconsistent\_trace, exact rule:** Applies LT (each step uses the row of the current state) unevenly: e.g. on some steps using the starting page's row instead of the current page's row. (here mixing in: "The page ranks depend on which page the surfer starts from")
- **Edge `power_method` &rarr; `StartPageMatters`, exact edge logic:** The page ranks depend on which page the surfer starts from. **Twin logic:** For the random-surfer chain the long-run probabilities do not depend on the starting page. (role: context)
- **Edge `two_models` &rarr; `StartPageMatters`, exact edge logic:** The page ranks depend on which page the surfer starts from. **Twin logic:** For the random-surfer chain the long-run probabilities do not depend on the starting page. (role: context)

## Errors (0)

An error edge states the rule that gets broken in a program, and the right rule.

The graph has no error edge from this concept.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for markov chain: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to markov chain agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

- **Edge:** `markov_chain` &rarr; `markov_chain@L0` (has_level)
- **Exact edge logic:** markov chain -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (3 ways).

Ways (3), each with its exact rule:

- **[0] everyday\_reading** (rule type E, folk-meaning rule): Everyday "chain" of events suggests the whole history matters; in a Markov chain the next state depends only on the current state, through that state's row of the transition matrix.
- **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `StartPageMatters`: wrong rule: The page ranks depend on which page the surfer starts from. Right rule: For the random-surfer chain the long-run probabilities are the same for all starting pages (basic limit theorem); that is why RandomSurfer can start at page 0.
- **[2] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `StartPageMatters`: Applies LT (each step uses the row of the current state) unevenly: e.g. on some steps using the starting page's row instead of the current page's row. (here mixing in: "The page ranks depend on which page the surfer starts from")

### L1: Unistructural / atom x text surface

L1 for markov chain: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

- **Edge:** `markov_chain` &rarr; `markov_chain@L1` (has_level)
- **Exact edge logic:** markov chain -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

Ways (2), each with its exact rule:

- **[0] names\_the\_element** (rule type N, identity rule): A mathematical model: a random process on states (pages) whose moves are given by a transition matrix.
- **[1] states\_the\_rule** (rule type S, declarative rule): The surfer's random process is a Markov chain; by the basic limit theorem the probability of eventually ending on any page is the same for all starting pages (mixing), though not all chains mix.

### L2: Multistructural / block x execution / preoperational

L2 for markov chain: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

- **Edge:** `markov_chain` &rarr; `markov_chain@L2` (has_level)
- **Exact edge logic:** markov chain -&gt; L2 (Multistructural): the answer applies the rules of markov chain to every part of the code, in order (3 ways).

Ways (3), each with its exact rule:

- **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): State sequence: from the current page i, choose the next page j with probability p[i][j]; repeat from j. In probability form, the t-step distribution is the (t-1)-step distribution times the matrix.
- **[1] output\_prediction** (rule type OP, evaluation / result rule): Produces the stationary probabilities (page ranks): for tiny.txt about .27 .27 .15 .25 .07.
- **[2] one\_step\_execution** (rule type OS, state-transition rule): One step moves the state from page i to a page j drawn from row i; in matrix form, one multiplication turns the distribution after t-1 moves into the distribution after t moves.

### L3: Relational / relations x function (concrete operational begins)

L3 for markov chain: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

- **Edge:** `markov_chain` &rarr; `markov_chain@L3` (has_level)
- **Exact edge logic:** markov chain -&gt; L3 (Relational): the answer relates the parts (3 ways).

Ways (3), each with its exact rule:

- **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): The chain is defined by the matrix: it must be square with every row a probability distribution.
- **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Each vector-matrix multiplication advances the chain's probabilities by one move; repeating it approaches the stationary vector.
- **[2] purpose\_of\_the\_whole** (rule type P, plan / role rule): Model a memoryless random process to compute its long-run behaviour (page ranks) instead of following one surfer.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for markov chain: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

- **Edge:** `markov_chain` &rarr; `markov_chain@L4` (has_level)
- **Exact edge logic:** markov chain -&gt; L4 (Extended abstract): the answer reasons beyond the given code (4 ways).

Ways (4), each with its exact rule:

- **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `StartPageMatters`: Changing the start state keeps the limiting distribution (if the chain mixes); removing the random leap can break mixing; squaring the matrix gives two-step probabilities.
- **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Right model when the next state depends only on the current state with fixed probabilities (web surfing, many random processes); its limit theorem gives start-independent results only for chains that mix.
- **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: Each row must be a probability distribution. Kind: silent logic error. Trigger class: A non-stochastic row (sum not 1, e.g. dangling page or bad scaling): simulation and multiplication give wrong probabilities.
- **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: The chain must mix for start-independent ranks. Kind: silent logic error. Trigger class: No random leap and a spider trap: the surfer gets stuck and results depend on where it starts.

## Same topic

`markov_chain` belongs to the topic **Mixing a Markov chain (squaring, power method)** (`topic1.6.c`). The topic also contains: `convergence_rate`, `power_method`, `two_models`.

## Rules of the concept (15)

- **Book** (SW-1e, p. 168 (pdf 178)): "The random process that describes the surfer's behavior is known as a Markov chain"
- **Book** (SW-1.6, p. 168 (pdf 178)): "The random process that describes the surfer's behavior is known as a Markov chain."
- **E** (folk-meaning rule): Everyday "chain" of events suggests the whole history matters; in a Markov chain the next state depends only on the current state, through that state's row of the transition matrix.
- **M** (wrong rule / right rule): StartPageMatters: wrong: The page ranks depend on which page the surfer starts from. \| right: For the random-surfer chain the long-run probabilities are the same for all starting pages (basic limit theorem); that is why RandomSurfer can start at page 0.
- **T** (uneven-application rule): Applies LT (each step uses the row of the current state) unevenly: e.g. on some steps using the starting page's row instead of the current page's row.
- **N** (identity rule): A mathematical model: a random process on states (pages) whose moves are given by a transition matrix.
- **S** (declarative rule): The surfer's random process is a Markov chain; by the basic limit theorem the probability of eventually ending on any page is the same for all starting pages (mixing), though not all chains mix.
- **LT** (operational sequencing rule): State sequence: from the current page i, choose the next page j with probability p[i][j]; repeat from j. In probability form, the t-step distribution is the (t-1)-step distribution times the matrix.
- **OP** (evaluation / result rule): Produces the stationary probabilities (page ranks): for tiny.txt about .27 .27 .15 .25 .07.
- **OS** (state-transition rule): One step moves the state from page i to a page j drawn from row i; in matrix form, one multiplication turns the distribution after t-1 moves into the distribution after t moves.
- **R** (composition rule (with a neighbour)): with transition\_matrix: The chain is defined by the matrix: it must be square with every row a probability distribution.
- **R** (composition rule (with a neighbour)): with power\_method: Each vector-matrix multiplication advances the chain's probabilities by one move; repeating it approaches the stationary vector.
- **P** (plan / role rule): Model a memoryless random process to compute its long-run behaviour (page ranks) instead of following one surfer.
- **C** (conservation rule): Changing the start state keeps the limiting distribution (if the chain mixes); removing the random leap can break mixing; squaring the matrix gives two-step probabilities.
- **D** (error rule): rule broken: Each row must be a probability distribution. (silent logic error)
- **D** (error rule): rule broken: The chain must mix for start-independent ranks. (silent logic error)
- **X** (applicability rule): Right model when the next state depends only on the current state with fixed probabilities (web surfing, many random processes); its limit theorem gives start-independent results only for chains that mix.

## How it is found in code and answers (reader block)

- **Aliases:** markov chain, random surfer, page rank, page ranks, pagerank, starting page, long run, long-run
- **Code patterns:** `\bMarkov\w*\b`, `\bRandomSurfer\b`, `\bpage\s*=\s*\w+\s*;`
- **Operator symbols:** none
- **Java types:** none

## The whole prerequisite chain

- **Everything it builds on (12):** `array_creation`, `array_declaration`, `array_initializer`, `data_structure`, `data_type`, `indexing`, `input_graph`, `standard_input`, `stream_model`, `teleportation`, `transition_matrix`, `two_dimensional_array`
- **Everything that builds on it (3):** `convergence_rate`, `power_method`, `two_models`

## Every edge in this view and its exact edge logic (14)

All the edges drawn in the picture, in the order: prerequisite, parallel, misconception, error, has_level, contains.

**1. `markov_chain` &rarr; `power_method`** (prerequisite)

- **Exact edge logic:** Each multiplication advances the chain's probabilities by one move.
- **Grounding:** book\_passage
- **Composition rule (R) of `markov_chain` with `power_method`:** Each vector-matrix multiplication advances the chain's probabilities by one move; repeating it approaches the stationary vector.
- **Composition rule (R) of `power_method` with `markov_chain`:** Each multiplication is one move of the chain; convergence is the chain's mixing.

**2. `transition_matrix` &rarr; `markov_chain`** (prerequisite)

- **Exact edge logic:** The transition matrix specifies the probability of each move, and the random process those probabilities define is a Markov chain.
- **Grounding:** book\_passage
- **Composition rule (R) of `transition_matrix` with `markov_chain`:** A matrix whose rows are probability distributions defines a Markov chain: the next page depends only on the current page's row.
- **Composition rule (R) of `markov_chain` with `transition_matrix`:** The chain is defined by the matrix: it must be square with every row a probability distribution.

**3. `markov_chain` &rarr; `StartPageMatters`** (misconception)

- **Exact edge logic (the wrong rule):** The page ranks depend on which page the surfer starts from.
- **Twin logic (the right rule):** For the random-surfer chain the long-run probabilities do not depend on the starting page.
- **Role:** primary

**4. `power_method` &rarr; `StartPageMatters`** (misconception)

- **Exact edge logic (the wrong rule):** The page ranks depend on which page the surfer starts from.
- **Twin logic (the right rule):** For the random-surfer chain the long-run probabilities do not depend on the starting page.
- **Role:** context

**5. `two_models` &rarr; `StartPageMatters`** (misconception)

- **Exact edge logic (the wrong rule):** The page ranks depend on which page the surfer starts from.
- **Twin logic (the right rule):** For the random-surfer chain the long-run probabilities do not depend on the starting page.
- **Role:** context

**6. `markov_chain` &rarr; `markov_chain@L0`** (has_level)

- **Exact edge logic:** markov chain -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (3 ways).
  - **[0] everyday\_reading** (rule type E, folk-meaning rule): Everyday "chain" of events suggests the whole history matters; in a Markov chain the next state depends only on the current state, through that state's row of the transition matrix.
  - **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `StartPageMatters`: wrong rule: The page ranks depend on which page the surfer starts from. Right rule: For the random-surfer chain the long-run probabilities are the same for all starting pages (basic limit theorem); that is why RandomSurfer can start at page 0.
  - **[2] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `StartPageMatters`: Applies LT (each step uses the row of the current state) unevenly: e.g. on some steps using the starting page's row instead of the current page's row. (here mixing in: "The page ranks depend on which page the surfer starts from")

**7. `markov_chain` &rarr; `markov_chain@L1`** (has_level)

- **Exact edge logic:** markov chain -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).
  - **[0] names\_the\_element** (rule type N, identity rule): A mathematical model: a random process on states (pages) whose moves are given by a transition matrix.
  - **[1] states\_the\_rule** (rule type S, declarative rule): The surfer's random process is a Markov chain; by the basic limit theorem the probability of eventually ending on any page is the same for all starting pages (mixing), though not all chains mix.

**8. `markov_chain` &rarr; `markov_chain@L2`** (has_level)

- **Exact edge logic:** markov chain -&gt; L2 (Multistructural): the answer applies the rules of markov chain to every part of the code, in order (3 ways).
  - **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): State sequence: from the current page i, choose the next page j with probability p[i][j]; repeat from j. In probability form, the t-step distribution is the (t-1)-step distribution times the matrix.
  - **[1] output\_prediction** (rule type OP, evaluation / result rule): Produces the stationary probabilities (page ranks): for tiny.txt about .27 .27 .15 .25 .07.
  - **[2] one\_step\_execution** (rule type OS, state-transition rule): One step moves the state from page i to a page j drawn from row i; in matrix form, one multiplication turns the distribution after t-1 moves into the distribution after t moves.

**9. `markov_chain` &rarr; `markov_chain@L3`** (has_level)

- **Exact edge logic:** markov chain -&gt; L3 (Relational): the answer relates the parts (3 ways).
  - **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): The chain is defined by the matrix: it must be square with every row a probability distribution.
  - **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Each vector-matrix multiplication advances the chain's probabilities by one move; repeating it approaches the stationary vector.
  - **[2] purpose\_of\_the\_whole** (rule type P, plan / role rule): Model a memoryless random process to compute its long-run behaviour (page ranks) instead of following one surfer.

**10. `markov_chain` &rarr; `markov_chain@L4`** (has_level)

- **Exact edge logic:** markov chain -&gt; L4 (Extended abstract): the answer reasons beyond the given code (4 ways).
  - **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `StartPageMatters`: Changing the start state keeps the limiting distribution (if the chain mixes); removing the random leap can break mixing; squaring the matrix gives two-step probabilities.
  - **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Right model when the next state depends only on the current state with fixed probabilities (web surfing, many random processes); its limit theorem gives start-independent results only for chains that mix.
  - **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: Each row must be a probability distribution. Kind: silent logic error. Trigger class: A non-stochastic row (sum not 1, e.g. dangling page or bad scaling): simulation and multiplication give wrong probabilities.
  - **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: The chain must mix for start-independent ranks. Kind: silent logic error. Trigger class: No random leap and a spider trap: the surfer gets stuck and results depend on where it starts.

**11. `topic1.6.c` &rarr; `markov_chain`** (contains)

- topic `topic1.6.c` contains `markov_chain`

**12. `topic1.6.c` &rarr; `convergence_rate`** (contains)

- topic `topic1.6.c` contains `convergence_rate`

**13. `topic1.6.c` &rarr; `power_method`** (contains)

- topic `topic1.6.c` contains `power_method`

**14. `topic1.6.c` &rarr; `two_models`** (contains)

- topic `topic1.6.c` contains `two_models`
