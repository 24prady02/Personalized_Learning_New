# sampling_without_replacement (`sampling_without_replacement`)

choosing m distinct items at random

Section 1.4 Arrays, topic 1.4.d Exchange, shuffling and sampling.

![The knowledge graph around sampling_without_replacement](sampling_without_replacement.png)

## At a glance

- **Needs first:** `array_creation`, `shuffle`
- **Leads to:** nothing
- **Learned alongside:** nothing
- **Misconceptions:** `SampleMayRepeat`
- **Errors:** none
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 11 edges around this concept, each explained in the graph's own words.

## What it needs first (2)

A prerequisite edge means the other concept has to be understood before `sampling_without_replacement`.

### `array_creation` comes before `sampling_without_replacement`

*new int[n] -- allocates n slots*

Sampling without replacement first creates an array of all candidates (perm), then picks from the part not yet chosen.

- **Grounding:** book passage

### `shuffle` comes before `sampling_without_replacement`

*Knuth shuffle -- swap a[i] with a random a[r], r in i..n-1*

Sample uses the basic operation underlying shuffling: for each of the first M positions it exchanges perm[i] with a random element to its right.

- **Grounding:** book passage
- **How `sampling_without_replacement` combines with `shuffle`:** The sample is the first M passes of the shuffle applied to the identity permutation.
- **How `shuffle` combines with `sampling_without_replacement`:** Stopping the shuffle after the first M passes leaves a uniform random sample in positions 0..M-1.

## What it leads to (0)

These concepts need `sampling_without_replacement` first.

No concept has this one as a prerequisite.

## Learned alongside (0)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

No parallel edge touches this concept.

## Misconceptions (1)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### SampleMayRepeat

- **Wrong rule:** A sample drawn without replacement may contain the same item twice.
- **Right rule:** Each member of the set appears at most once in the sample.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: A sample drawn without replacement may contain the same item twice. Right rule: Each member of the set appears at most once in the sample.
- **Shows at level L0 as:** inconsistent trace: Points to LT: perm[] is first filled with 0..N-1, then the first M shuffle passes run, then perm[0..M-1] is printed. Inconsistent application: the sample is read before all M exchanges are done, or the identity fill is skipped on a trace. (here mixing in: "A sample drawn without replacement may contain the same item twice")

## Errors (0)

An error edge states the rule that gets broken in a program, and the right rule.

The graph has no error edge from this concept.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for sampling without replacement: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to sampling without replacement agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

sampling without replacement -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (3 ways).

- **everyday reading** (folk-meaning rule): Folk meaning: 'pick M random items' is read as M independent random picks, so repeats seem acceptable. Rule: in sampling without replacement each member of the set appears at most once, like lottery balls not put back.
- **misconception** (wrong rule / right rule; shows `SampleMayRepeat`): wrong rule: A sample drawn without replacement may contain the same item twice. Right rule: Each member of the set appears at most once in the sample.
- **inconsistent trace** (uneven-application rule; shows `SampleMayRepeat`): Points to LT: perm[] is first filled with 0..N-1, then the first M shuffle passes run, then perm[0..M-1] is printed. Inconsistent application: the sample is read before all M exchanges are done, or the identity fill is skipped on a trace. (here mixing in: "A sample drawn without replacement may contain the same item twice")

### L1: Unistructural / atom x text surface

L1 for sampling without replacement: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

sampling without replacement -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

- **names the element** (identity rule): Identity: sampling without replacement draws a random sample of M items from N in which no item can be chosen twice.
- **states the rule** (declarative rule): Declarative (Program 1.4.1): perm[j] = j for all j; for i &lt; M, r = i + (int) (Math.random() \* (N-i)) and exchange perm[i] with perm[r]; perm[0..M-1] is the sample.

### L2: Multistructural / block x execution / preoperational

L2 for sampling without replacement: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

sampling without replacement -&gt; L2 (Multistructural): the answer applies the rules of sampling without replacement to every part of the code, in order (3 ways).

- **line by line trace** (operational sequencing rule): Sequencing: read M and N, create perm, fill it with the identity, run M exchange passes left to right, then print perm[0] .. perm[M-1].
- **output prediction** (evaluation / result rule): Result: M distinct integers from 0..N-1 (e.g. java Sample 6 16 prints 9 5 13 1 11 8). If M == N the result is a random permutation; if M &gt; N the program throws ArrayIndexOutOfBoundsException.
- **one step execution** (state-transition rule): State transition: each pass exchanges perm[i] with one element to its right, fixing perm[i] as the next sampled item; perm stays a permutation of 0..N-1.

### L3: Relational / relations x function (concrete operational begins)

L3 for sampling without replacement: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

sampling without replacement -&gt; L3 (Relational): the answer relates the parts (2 ways).

- **relation to neighbour** (composition rule (with a neighbour)): The sample is the first M passes of the shuffle applied to the identity permutation.
- **purpose of the whole** (plan / role rule): Plan/role: draw lottery numbers or deal a hand. The permutation can also serve as indices into another array (deck[perm[i]]) to sample it without rearranging it.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for sampling without replacement: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

sampling without replacement -&gt; L4 (Extended abstract): the answer reasons beyond the given code (4 ways).

- **predict a change** (conservation rule; shows `SampleMayRepeat`): Conservation: perm remains a permutation of 0..N-1 after every exchange, so no value can appear twice for any M &lt;= N; changing M changes only how many passes run.
- **transfer to a new program** (applicability rule): Applicability: use it when the sample must contain distinct items (lotteries, card hands, survey samples). When repeats are allowed (sampling with replacement), independent random indices are simpler.
- **diagnose an error** (error rule): rule broken: The sample size cannot exceed the population size. Kind: run-time exception. Trigger class: M &gt; N on the command line, so perm[i] is indexed at i = N (ArrayIndexOutOfBoundsException)
- **diagnose an error** (error rule): rule broken: Each pick must come from the items not yet sampled. Kind: silent logic error. Trigger class: independent picks (int) (Math.random() \* N) without exchanging, which can repeat an item

## Same topic

`sampling_without_replacement` belongs to the topic **Exchange, shuffling and sampling** (`topic1.4.d`). The topic also contains: `array_exchange`, `shuffle`.

## Rules of the concept (14)

- **folk-meaning rule:** Folk meaning: 'pick M random items' is read as M independent random picks, so repeats seem acceptable. Rule: in sampling without replacement each member of the set appears at most once, like lottery balls not put back.
- **wrong rule / right rule:** SampleMayRepeat: wrong: A sample drawn without replacement may contain the same item twice. \| right: Each member of the set appears at most once in the sample.
- **uneven-application rule:** Points to LT: perm[] is first filled with 0..N-1, then the first M shuffle passes run, then perm[0..M-1] is printed. Inconsistent application: the sample is read before all M exchanges are done, or the identity fill is skipped on a trace.
- **identity rule:** Identity: sampling without replacement draws a random sample of M items from N in which no item can be chosen twice.
- **declarative rule:** Declarative (Program 1.4.1): perm[j] = j for all j; for i &lt; M, r = i + (int) (Math.random() \* (N-i)) and exchange perm[i] with perm[r]; perm[0..M-1] is the sample.
- **operational sequencing rule:** Sequencing: read M and N, create perm, fill it with the identity, run M exchange passes left to right, then print perm[0] .. perm[M-1].
- **evaluation / result rule:** Result: M distinct integers from 0..N-1 (e.g. java Sample 6 16 prints 9 5 13 1 11 8). If M == N the result is a random permutation; if M &gt; N the program throws ArrayIndexOutOfBoundsException.
- **state-transition rule:** State transition: each pass exchanges perm[i] with one element to its right, fixing perm[i] as the next sampled item; perm stays a permutation of 0..N-1.
- **composition rule (with a neighbour):** with shuffle: The sample is the first M passes of the shuffle applied to the identity permutation.
- **plan / role rule:** Plan/role: draw lottery numbers or deal a hand. The permutation can also serve as indices into another array (deck[perm[i]]) to sample it without rearranging it.
- **conservation rule:** Conservation: perm remains a permutation of 0..N-1 after every exchange, so no value can appear twice for any M &lt;= N; changing M changes only how many passes run.
- **error rule:** rule broken: The sample size cannot exceed the population size. (run-time exception)
- **error rule:** rule broken: Each pick must come from the items not yet sampled. (silent logic error)
- **applicability rule:** Applicability: use it when the sample must contain distinct items (lotteries, card hands, survey samples). When repeats are allowed (sampling with replacement), independent random indices are simpler.

## The whole prerequisite chain

- **Everything it builds on (18):** `arithmetic_operators`, `array_creation`, `array_declaration`, `array_exchange`, `array_initializer`, `assignment`, `data_structure`, `data_type`, `declaration`, `expression`, `identifier`, `indexing`, `literal`, `math_library`, `method_call`, `primitive_type`, `shuffle`, `variable`
- **Everything that builds on it (0):** nothing
