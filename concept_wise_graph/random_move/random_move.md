# random_move (`random_move`)

pick the next page from a cumulative-probability test

Section 1.6 Case Study: Random Web Surfer, topic 1.6.b Simulation (one random move, page ranks).

![The knowledge graph around random_move](random_move.png)

## At a glance

- **Needs first:** `boolean_expression`, `math_library`, `transition_matrix`
- **Leads to:** `simulation_loop`
- **Learned alongside:** nothing
- **Misconceptions:** `CumulativeOffByOne`
- **Errors:** none
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 13 edges around this concept, each explained in the graph's own words.

## What it needs first (3)

A prerequisite edge means the other concept has to be understood before `random_move`.

### `boolean_expression` comes before `random_move`

*an expression that evaluates to true/false*

The next page is chosen by testing the condition r &lt; sum for each candidate page j in turn.

- **Grounding:** book passage
- **How `random_move` combines with `boolean_expression`:** The relational test r &lt; sum decides both the chosen page and the early break; &lt; (not &lt;=) matches the half-open interval endpoint tracked by sum.
- **How `boolean_expression` combines with `random_move`:** In RandomSurfer the boolean expression r &lt; sum is evaluated for each candidate page j in turn, as sum grows; the first j for which it is true is the chosen page.

### `math_library` comes before `random_move`

*Math.abs, Math.sqrt, Math.max, Math.random, Math.round ...*

The random move draws r with Math.random() and then finds the interval of row p[page] that contains r.

- **Grounding:** book passage
- **How `random_move` combines with `math_library`:** Math.random() supplies one uniform double in [0, 1) per move; it must be called once before the j loop, not inside it.
- **How `math_library` combines with `random_move`:** The random move draws r = Math.random() once per move and compares it with growing cumulative sums of row p[page] to find which interval contains it.

### `transition_matrix` comes before `random_move`

*a 2-D array of move probabilities (rows sum to 1)*

Row p[i] is the probability distribution used to choose the next page when the surfer is on page i.

- **Grounding:** book passage
- **How `random_move` combines with `transition_matrix`:** Reads exactly one row p[page]; the row must sum to 1, otherwise r can exceed the final sum and no j is chosen.
- **How `transition_matrix` combines with `random_move`:** The random move reads one row p[page] as a 1-D array and accumulates its entries; it only works if that row sums to 1.

## What it leads to (1)

These concepts need `random_move` first.

### `random_move` comes before `simulation_loop`

*take many random steps*

The simulation repeats the random move T times, each move starting from the page the previous move reached.

- **Grounding:** book passage
- **How `random_move` combines with `simulation_loop`:** Each move starts from the page the previous move produced, and the simulation repeats it T times; the next row used is p[new page].
- **How `simulation_loop` combines with `random_move`:** The loop body is one random move; page carries state from one pass to the next, so each move uses the row of the page reached last.

## Learned alongside (0)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

No parallel edge touches this concept.

## Misconceptions (1)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### CumulativeOffByOne

- **Wrong rule:** Whether the test is r &lt; s or r &lt;= s, or whether p[i][j] is added before or after the test, the same page is picked.
- **Right rule:** Add p[page][j] to sum and then test r &lt; sum: sum tracks the endpoints of the intervals defined by row p[page], so the loop finds the interval containing r, and r falls into each interval with probability precisely specified by its length.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: The cumulative-probability boundary test is inclusive/exclusive interchangeably. Right rule: Add p[page][j] to sum first and then test r &lt; sum; sum is the right endpoint of interval j, so r lands in interval j with probability equal to its length.
- **Shows at level L0 as:** inconsistent trace: Applies LT (r drawn once; for each j: add p[page][j] to sum, then test r &lt; sum) unevenly: e.g. testing before adding on some passes, or drawing a new r for each j. (here mixing in: "the cumulative-probability boundary test is inclusive/exclusive interchangeably")

## Errors (0)

An error edge states the rule that gets broken in a program, and the right rule.

The graph has no error edge from this concept.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for random move: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to random move agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

random move -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (3 ways).

- **everyday reading** (folk-meaning rule): Everyday "random" means every outcome equally likely, which is what Math.random() gives; the random move must instead pick page j with the unequal probability p[page][j].
- **misconception** (wrong rule / right rule; shows `CumulativeOffByOne`): wrong rule: The cumulative-probability boundary test is inclusive/exclusive interchangeably. Right rule: Add p[page][j] to sum first and then test r &lt; sum; sum is the right endpoint of interval j, so r lands in interval j with probability equal to its length.
- **inconsistent trace** (uneven-application rule; shows `CumulativeOffByOne`): Applies LT (r drawn once; for each j: add p[page][j] to sum, then test r &lt; sum) unevenly: e.g. testing before adding on some passes, or drawing a new r for each j. (here mixing in: "the cumulative-probability boundary test is inclusive/exclusive interchangeably")

### L1: Unistructural / atom x text surface

L1 for random move: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

random move -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

- **names the element** (identity rule): An algorithm: generating a random integer from a discrete distribution (row p[page]) by locating a uniform random number in cumulative intervals.
- **states the rule** (declarative rule): Think of row p[page] as N intervals of (0, 1) whose lengths are the probabilities; a uniform r from Math.random() falls into interval j with probability p[page][j], and the surfer moves to j.

### L2: Multistructural / block x execution / preoperational

L2 for random move: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

random move -&gt; L2 (Multistructural): the answer applies the rules of random move to every part of the code, in order (3 ways).

- **line by line trace** (operational sequencing rule): r = Math.random() is drawn once; sum = 0.0; j goes 0, 1, ...; on each pass sum += p[page][j] and then if (r &lt; sum) set page = j and break, so the first interval whose right end exceeds r wins.
- **output prediction** (evaluation / result rule): Returns (through page) one integer 0..N-1; at page 4 of tiny.txt sum takes 0.47, 0.49, 0.96, ... and r = .71 gives page 2.
- **one step execution** (state-transition rule): One move changes page from its current value to j (and leaves freq and p unchanged); the locals r, sum and j live only for that move.

### L3: Relational / relations x function (concrete operational begins)

L3 for random move: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

random move -&gt; L3 (Relational): the answer relates the parts (5 ways).

- **relation to neighbour** (composition rule (with a neighbour)): Reads exactly one row p[page]; the row must sum to 1, otherwise r can exceed the final sum and no j is chosen.
- **relation to neighbour** (composition rule (with a neighbour)): Each move starts from the page the previous move produced, and the simulation repeats it T times; the next row used is p[new page].
- **relation to neighbour** (composition rule (with a neighbour)): The relational test r &lt; sum decides both the chosen page and the early break; &lt; (not &lt;=) matches the half-open interval endpoint tracked by sum.
- **relation to neighbour** (composition rule (with a neighbour)): Math.random() supplies one uniform double in [0, 1) per move; it must be called once before the j loop, not inside it.
- **purpose of the whole** (plan / role rule): Sampling plan (search the cumulative sums): sum is a gatherer, j a stepper, and page a most-recent holder of the current location; break ends the search as soon as the interval is found.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for random move: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

random move -&gt; L4 (Extended abstract): the answer reasons beyond the given code (5 ways).

- **predict a change** (conservation rule; shows `CumulativeOffByOne`): Changing the search (linear to binary) or the order of pages keeps the distribution of outcomes; replacing r &lt; sum with r &lt;= sum changes it only on a zero-probability event; moving Math.random() into the loop breaks it.
- **transfer to a new program** (applicability rule): Use to draw from any non-uniform discrete distribution (one row of probabilities); for uniform choice Math.random() scaled is enough, and for large N a binary search over the cumulative sums is faster.
- **diagnose an error** (error rule): rule broken: Add the entry to sum before testing r &lt; sum. Kind: silent logic error. Trigger class: Test placed before sum += p[page][j]: the first test is r &lt; 0.0 (always false) and every page is chosen from the previous interval, shifting probabilities by one page.
- **diagnose an error** (error rule): rule broken: Row p[page] must sum to 1. Kind: silent logic error. Trigger class: Row sum &lt; 1 (e.g. dangling page, NaN): when r exceeds the final sum the loop ends with no break and page is unchanged.
- **diagnose an error** (error rule): rule broken: break must exit the search once the interval is found. Kind: silent logic error. Trigger class: break omitted: page is reassigned on every later j, so the surfer always moves to page N-1 (or the last j with r &lt; sum).

## Same topic

`random_move` belongs to the topic **Simulation (one random move, page ranks)** (`topic1.6.b`). The topic also contains: `frequency_counting`, `simulation_loop`.

## Rules of the concept (18)

- **folk-meaning rule:** Everyday "random" means every outcome equally likely, which is what Math.random() gives; the random move must instead pick page j with the unequal probability p[page][j].
- **wrong rule / right rule:** CumulativeOffByOne: wrong: The cumulative-probability boundary test is inclusive/exclusive interchangeably. \| right: Add p[page][j] to sum first and then test r &lt; sum; sum is the right endpoint of interval j, so r lands in interval j with probability equal to its length.
- **uneven-application rule:** Applies LT (r drawn once; for each j: add p[page][j] to sum, then test r &lt; sum) unevenly: e.g. testing before adding on some passes, or drawing a new r for each j.
- **identity rule:** An algorithm: generating a random integer from a discrete distribution (row p[page]) by locating a uniform random number in cumulative intervals.
- **declarative rule:** Think of row p[page] as N intervals of (0, 1) whose lengths are the probabilities; a uniform r from Math.random() falls into interval j with probability p[page][j], and the surfer moves to j.
- **operational sequencing rule:** r = Math.random() is drawn once; sum = 0.0; j goes 0, 1, ...; on each pass sum += p[page][j] and then if (r &lt; sum) set page = j and break, so the first interval whose right end exceeds r wins.
- **evaluation / result rule:** Returns (through page) one integer 0..N-1; at page 4 of tiny.txt sum takes 0.47, 0.49, 0.96, ... and r = .71 gives page 2.
- **state-transition rule:** One move changes page from its current value to j (and leaves freq and p unchanged); the locals r, sum and j live only for that move.
- **composition rule (with a neighbour):** with transition\_matrix: Reads exactly one row p[page]; the row must sum to 1, otherwise r can exceed the final sum and no j is chosen.
- **composition rule (with a neighbour):** with simulation\_loop: Each move starts from the page the previous move produced, and the simulation repeats it T times; the next row used is p[new page].
- **composition rule (with a neighbour):** with boolean\_expression: The relational test r &lt; sum decides both the chosen page and the early break; &lt; (not &lt;=) matches the half-open interval endpoint tracked by sum.
- **composition rule (with a neighbour):** with math\_library: Math.random() supplies one uniform double in [0, 1) per move; it must be called once before the j loop, not inside it.
- **plan / role rule:** Sampling plan (search the cumulative sums): sum is a gatherer, j a stepper, and page a most-recent holder of the current location; break ends the search as soon as the interval is found.
- **conservation rule:** Changing the search (linear to binary) or the order of pages keeps the distribution of outcomes; replacing r &lt; sum with r &lt;= sum changes it only on a zero-probability event; moving Math.random() into the loop breaks it.
- **error rule:** rule broken: Add the entry to sum before testing r &lt; sum. (silent logic error)
- **error rule:** rule broken: Row p[page] must sum to 1. (silent logic error)
- **error rule:** rule broken: break must exit the search once the interval is found. (silent logic error)
- **applicability rule:** Use to draw from any non-uniform discrete distribution (one row of probabilities); for uniform choice Math.random() scaled is enough, and for large N a binary search over the cumulative sums is faster.

## The whole prerequisite chain

- **Everything it builds on (24):** `arithmetic_operators`, `array_creation`, `array_declaration`, `array_initializer`, `boolean`, `boolean_expression`, `comparison_operators`, `data_structure`, `data_type`, `expression`, `identifier`, `indexing`, `input_graph`, `literal`, `logical_operators`, `math_library`, `method_call`, `primitive_type`, `standard_input`, `stream_model`, `teleportation`, `transition_matrix`, `two_dimensional_array`, `variable`
- **Everything that builds on it (3):** `frequency_counting`, `simulation_loop`, `two_models`
