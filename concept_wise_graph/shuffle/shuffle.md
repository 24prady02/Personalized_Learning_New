# shuffle (`shuffle`)

Knuth shuffle -- swap a[i] with a random a[r], r in i..n-1

Section 1.4 Arrays, topic 1.4.d Exchange, shuffling and sampling.

![The knowledge graph around shuffle](shuffle.png)

## At a glance

- **Needs first:** `array_exchange`, `math_library`
- **Leads to:** `sampling_without_replacement`
- **Learned alongside:** nothing
- **Misconceptions:** `BiasedShuffle`
- **Errors:** none
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 12 edges around this concept, each explained in the graph's own words.

## What it needs first (2)

A prerequisite edge means the other concept has to be understood before `shuffle`.

### `array_exchange` comes before `shuffle`

*swap a[i] and a[j] through a temporary variable*

Shuffling is a loop of exchanges with randomly chosen positions.

- **Grounding:** book passage
- **How `shuffle` combines with `array_exchange`:** Using the exchange idiom guarantees the deck holds the same cards after the shuffle.
- **How `array_exchange` combines with `shuffle`:** Shuffling is a loop of exchanges with random partner positions; using exchanges guarantees the same cards before and after.

### `math_library` comes before `shuffle`

*Math.abs, Math.sqrt, Math.max, Math.random, Math.round ...*

The random position r between i and N-1 is computed with Math.random(), so each remaining card is equally likely to be chosen.

- **Grounding:** book passage
- **How `shuffle` combines with `math_library`:** (int) (Math.random() \* (N-i)) is a uniform int in 0..N-i-1, so r = i + that value is uniform in i..N-1.
- **How `math_library` combines with `shuffle`:** In the shuffle, r = i + (int) (Math.random() \* (N-i)) scales Math.random() to a uniformly random position between i and N-1, so each remaining card is equally likely.

## What it leads to (1)

These concepts need `shuffle` first.

### `shuffle` comes before `sampling_without_replacement`

*choosing m distinct items at random*

Sample uses the basic operation underlying shuffling: for each of the first M positions it exchanges perm[i] with a random element to its right.

- **Grounding:** book passage
- **How `shuffle` combines with `sampling_without_replacement`:** Stopping the shuffle after the first M passes leaves a uniform random sample in positions 0..M-1.
- **How `sampling_without_replacement` combines with `shuffle`:** The sample is the first M passes of the shuffle applied to the identity permutation.

## Learned alongside (0)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

No parallel edge touches this concept.

## Misconceptions (1)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### BiasedShuffle

- **Wrong rule:** Swapping each a[i] with a random element from the whole array gives a uniformly random order.
- **Right rule:** r must be chosen between i and n - 1 for every ordering to be equally likely.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: Swapping each a[i] with a random element from the whole array gives a uniformly random order. Right rule: r must be chosen between i and n - 1 for every ordering to be equally likely.
- **Shows at level L0 as:** inconsistent trace: Points to LT: for each i from left to right, compute r in i..N-1 and then exchange deck[i] and deck[r]. Inconsistent application: r is drawn from the whole range on some passes, or the exchange is skipped when r == i. (here mixing in: "Swapping each a[i] with a random element from the whole array gives a uniformly random order")

## Errors (0)

An error edge states the rule that gets broken in a program, and the right rule.

The graph has no error edge from this concept.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for shuffle: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to shuffle agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

shuffle -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (3 ways).

- **everyday reading** (folk-meaning rule): Folk meaning: 'shuffle' means mix randomly, so any random swapping seems good enough. Java/algorithm rule: picking the partner r uniformly from i..N-1 makes all N! orders equally likely; picking from 0..N-1 does not.
- **misconception** (wrong rule / right rule; shows `BiasedShuffle`): wrong rule: Swapping each a[i] with a random element from the whole array gives a uniformly random order. Right rule: r must be chosen between i and n - 1 for every ordering to be equally likely.
- **inconsistent trace** (uneven-application rule; shows `BiasedShuffle`): Points to LT: for each i from left to right, compute r in i..N-1 and then exchange deck[i] and deck[r]. Inconsistent application: r is drawn from the whole range on some passes, or the exchange is skipped when r == i. (here mixing in: "Swapping each a[i] with a random element from the whole array gives a uniformly random order")

### L1: Unistructural / atom x text surface

L1 for shuffle: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

shuffle -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

- **names the element** (identity rule): Identity: the Knuth (Fisher-Yates) shuffle, which produces a random permutation by exchanging each position, left to right, with a uniformly chosen position at or to its right.
- **states the rule** (declarative rule): Declarative: for (int i = 0; i &lt; N; i++) { int r = i + (int) (Math.random() \* (N-i)); exchange deck[i] and deck[r]; }.

### L2: Multistructural / block x execution / preoperational

L2 for shuffle: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

shuffle -&gt; L2 (Multistructural): the answer applies the rules of shuffle to every part of the code, in order (3 ways).

- **line by line trace** (operational sequencing rule): Sequencing: N = deck.length is read once; on each pass r is computed first (Math.random(), times N-i, cast to int, plus i), then the three-step exchange runs, then i increases.
- **output prediction** (evaluation / result rule): Result: a permutation of the original elements with every one of the N! orders equally likely; the output differs from run to run.
- **one step execution** (state-transition rule): State transition: one pass picks r and exchanges deck[i] with deck[r]; afterwards deck[0..i] is fixed for the rest of the shuffle.

### L3: Relational / relations x function (concrete operational begins)

L3 for shuffle: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

shuffle -&gt; L3 (Relational): the answer relates the parts (4 ways).

- **relation to neighbour** (composition rule (with a neighbour)): Using the exchange idiom guarantees the deck holds the same cards after the shuffle.
- **relation to neighbour** (composition rule (with a neighbour)): (int) (Math.random() \* (N-i)) is a uniform int in 0..N-i-1, so r = i + that value is uniform in i..N-1.
- **relation to neighbour** (composition rule (with a neighbour)): Stopping the shuffle after the first M passes leaves a uniform random sample in positions 0..M-1.
- **purpose of the whole** (plan / role rule): Plan/role: randomize the order of an array in place in linear time (dealing cards, random permutations); the array is an organizer.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for shuffle: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

shuffle -&gt; L4 (Extended abstract): the answer reasons beyond the given code (5 ways).

- **predict a change** (conservation rule; shows `BiasedShuffle`): Conservation: the set of cards is invariant (exchanges only), and after pass i, deck[0..i] is a uniform random sample. Widening r's range to 0..N-1 keeps the set but breaks uniformity.
- **transfer to a new program** (applicability rule): Applicability: use it to randomize a whole array in place. For only M random items, run the first M passes. When the original order must be kept, shuffle an index permutation and use it to index the data.
- **diagnose an error** (error rule): rule broken: r must be uniform over i..N-1. Kind: silent logic error. Trigger class: r = (int) (Math.random() \* N): the shuffle runs and looks random, but some orders are more likely than others
- **diagnose an error** (error rule): rule broken: The cast applies to the scaled product. Kind: silent logic error. Trigger class: (int) Math.random() \* (N-i) casts first and is always 0, so r == i and nothing moves
- **diagnose an error** (error rule): rule broken: r must stay within 0..N-1. Kind: run-time exception. Trigger class: r = i + (int) (Math.random() \* N) can exceed N-1 (ArrayIndexOutOfBoundsException)

## Same topic

`shuffle` belongs to the topic **Exchange, shuffling and sampling** (`topic1.4.d`). The topic also contains: `array_exchange`, `sampling_without_replacement`.

## Rules of the concept (17)

- **folk-meaning rule:** Folk meaning: 'shuffle' means mix randomly, so any random swapping seems good enough. Java/algorithm rule: picking the partner r uniformly from i..N-1 makes all N! orders equally likely; picking from 0..N-1 does not.
- **wrong rule / right rule:** BiasedShuffle: wrong: Swapping each a[i] with a random element from the whole array gives a uniformly random order. \| right: r must be chosen between i and n - 1 for every ordering to be equally likely.
- **uneven-application rule:** Points to LT: for each i from left to right, compute r in i..N-1 and then exchange deck[i] and deck[r]. Inconsistent application: r is drawn from the whole range on some passes, or the exchange is skipped when r == i.
- **identity rule:** Identity: the Knuth (Fisher-Yates) shuffle, which produces a random permutation by exchanging each position, left to right, with a uniformly chosen position at or to its right.
- **declarative rule:** Declarative: for (int i = 0; i &lt; N; i++) { int r = i + (int) (Math.random() \* (N-i)); exchange deck[i] and deck[r]; }.
- **operational sequencing rule:** Sequencing: N = deck.length is read once; on each pass r is computed first (Math.random(), times N-i, cast to int, plus i), then the three-step exchange runs, then i increases.
- **evaluation / result rule:** Result: a permutation of the original elements with every one of the N! orders equally likely; the output differs from run to run.
- **state-transition rule:** State transition: one pass picks r and exchanges deck[i] with deck[r]; afterwards deck[0..i] is fixed for the rest of the shuffle.
- **composition rule (with a neighbour):** with array\_exchange: Using the exchange idiom guarantees the deck holds the same cards after the shuffle.
- **composition rule (with a neighbour):** with math\_library: (int) (Math.random() \* (N-i)) is a uniform int in 0..N-i-1, so r = i + that value is uniform in i..N-1.
- **composition rule (with a neighbour):** with sampling\_without\_replacement: Stopping the shuffle after the first M passes leaves a uniform random sample in positions 0..M-1.
- **plan / role rule:** Plan/role: randomize the order of an array in place in linear time (dealing cards, random permutations); the array is an organizer.
- **conservation rule:** Conservation: the set of cards is invariant (exchanges only), and after pass i, deck[0..i] is a uniform random sample. Widening r's range to 0..N-1 keeps the set but breaks uniformity.
- **error rule:** rule broken: r must be uniform over i..N-1. (silent logic error)
- **error rule:** rule broken: The cast applies to the scaled product. (silent logic error)
- **error rule:** rule broken: r must stay within 0..N-1. (run-time exception)
- **applicability rule:** Applicability: use it to randomize a whole array in place. For only M random items, run the first M passes. When the original order must be kept, shuffle an index permutation and use it to index the data.

## The whole prerequisite chain

- **Everything it builds on (17):** `arithmetic_operators`, `array_creation`, `array_declaration`, `array_exchange`, `array_initializer`, `assignment`, `data_structure`, `data_type`, `declaration`, `expression`, `identifier`, `indexing`, `literal`, `math_library`, `method_call`, `primitive_type`, `variable`
- **Everything that builds on it (1):** `sampling_without_replacement`
