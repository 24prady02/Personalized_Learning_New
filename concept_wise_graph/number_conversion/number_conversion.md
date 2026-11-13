# Number conversion (binary) (`number_conversion`)

converting an integer to its binary representation by casting out powers of 2 in a loop

Section 1.3 1.3 Conditionals and Loops, topic 1.3.f Applications (finite sums, Newton, conversion, gambler's ruin, factoring).

![The knowledge graph around number_conversion](number_conversion.png)

## At a glance

- **Needs first:** `arithmetic_operators`, `while_loop`
- **Leads to:** nothing
- **Learned alongside:** nothing
- **Misconceptions:** none
- **Errors:** none
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 17 edges around this concept. The edge logic, the wrong and right rules and the exact rules of the ways are copied word for word from the graph.

## To work on (2)

- no misconception or error edge
- no aliases: a student's words cannot name this concept

## What it needs first (2)

A prerequisite edge means the other concept has to be understood before `number_conversion`.

### `arithmetic_operators` comes before `number_conversion`

*+ - \* / %*

- **Edge:** `pre:arithmetic_operators->number_conversion`
- **Exact edge logic:** Converting to binary works with powers of two, using / and % (or subtraction) on ints.
- **Grounding:** book\_passage

### `while_loop` comes before `number_conversion`

*repeat a block while a condition holds*

- **Edge:** `pre:while_loop->number_conversion`
- **Exact edge logic:** Binary conversion repeats one step in a while loop: find the largest power of 2 not above n, output a bit and subtract.
- **Grounding:** book\_passage
- **Composition rule (R) of `number_conversion` with `while_loop`:** Two while loops in sequence: the first's exit state (v = largest power of 2 ≤ N) is the second's starting state. The second runs once per bit and ends when integer halving takes v from 1 to 0.
- **Composition rule (R) of `while_loop` with `number_conversion`:** Binary conversion uses while loops: one to find the largest power of 2 &lt;= N, and one to cast out powers of 2 in decreasing order.

## What it leads to (0)

These concepts need `number_conversion` first.

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

L0 for Number conversion (binary): the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to Number conversion (binary) agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

- **Edge:** `number_conversion` &rarr; `number_conversion@L0` (has_level)
- **Exact edge logic:** Number conversion (binary) -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (1 way).

Ways (1), each with its exact rule:

- **[0] everyday\_reading** (rule type E, folk-meaning rule): Folk meaning: everyday digits are decimal, so '10011' reads as ten thousand and eleven, and 'converting' sounds like changing the number. Binary conversion changes only the representation: 19 and 10011 (base 2) are the same integer, printed as a sequence of bits by casting out powers of 2.

### L1: Unistructural / atom x text surface

L1 for Number conversion (binary): the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

- **Edge:** `number_conversion` &rarr; `number_conversion@L1` (has_level)
- **Exact edge logic:** Number conversion (binary) -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

Ways (2), each with its exact rule:

- **[0] names\_the\_element** (rule type N, identity rule): Algorithm: computing the base-2 (or base-k) representation of a positive integer by casting out powers of 2 in decreasing order, or by repeated division.
- **[1] states\_the\_rule** (rule type S, declarative rule): First find v, the largest power of 2 ≤ N (\`while (v &lt;= N/2) v = 2\*v;\`). Then, with n = N, for each v from there down to 1: if n &lt; v print 0, else print 1 and set n -= v; then v = v/2.

### L2: Multistructural / block x execution / preoperational

L2 for Number conversion (binary): the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

- **Edge:** `number_conversion` &rarr; `number_conversion@L2` (has_level)
- **Exact edge logic:** Number conversion (binary) -&gt; L2 (Multistructural): the answer applies the rules of Number conversion (binary) to every part of the code, in order (3 ways).

Ways (3), each with its exact rule:

- **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): Order inside each pass: test \`v &gt; 0\`; compare n &lt; v; print the bit; subtract v from n only when the bit is 1; then halve v. The first loop runs to completion before the second begins.
- **[1] output\_prediction** (rule type OP, evaluation / result rule): The output is the string of bits, most significant first. \`java Binary 19\` prints 10011, which is 16 + 2 + 1.
- **[2] one\_step\_execution** (rule type OS, state-transition rule): One pass prints one bit, possibly subtracts v from n (19 becomes 3 when v = 16), and halves v (16 becomes 8).

### L3: Relational / relations x function (concrete operational begins)

L3 for Number conversion (binary): the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

- **Edge:** `number_conversion` &rarr; `number_conversion@L3` (has_level)
- **Exact edge logic:** Number conversion (binary) -&gt; L3 (Relational): the answer relates the parts (2 ways).

Ways (2), each with its exact rule:

- **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Two while loops in sequence: the first's exit state (v = largest power of 2 ≤ N) is the second's starting state. The second runs once per bit and ends when integer halving takes v from 1 to 0.
- **[1] purpose\_of\_the\_whole** (rule type P, plan / role rule): Plan: representation conversion. v is a stepper (powers of 2 in decreasing order), and n is the remaining excess that shrinks to 0. The same plan gives base-k conversion, and the right-to-left variant builds the string with \`s = (n % 2) + s\`.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for Number conversion (binary): the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

- **Edge:** `number_conversion` &rarr; `number_conversion@L4` (has_level)
- **Exact edge logic:** Number conversion (binary) -&gt; L4 (Extended abstract): the answer reasons beyond the given code (6 ways).

Ways (6), each with its exact rule:

- **[0] predict\_a\_change** (rule type C, conservation rule): The right-to-left method \`for (n = N; n &gt; 0; n /= 2) s = (n % 2) + s;\` produces the same string. Appending instead (\`s = s + (n % 2)\`) reverses the bits. Invariant of the casting-out loop: the bits printed so far, times 2^(number of bits still to print), plus n, equals N.
- **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Use a hand-written conversion loop to learn or to support unusual bases. In practice use Integer.toBinaryString (or Integer.toString(n, k)). Conversion is needed only for display or I/O, because arithmetic works on the int itself.
- **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: When a 1 bit is printed, its power must be subtracted from n. Kind: silent logic error. Trigger class: Forgetting \`n -= v\`: every bit after the first prints 1 whenever n ≥ v (19 prints 11111).
- **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: The algorithm assumes a positive integer. Kind: silent logic error. Trigger class: N ≤ 0 (e.g. -5): the program prints 0, not a representation of N.
- **[4] diagnose\_an\_error** (rule type D, error rule): rule broken: The argument must parse as an int. Kind: run-time exception. Trigger class: A non-integer or too-large argument (\`java Binary 3.5\`): Integer.parseInt throws NumberFormatException.
- **[5] diagnose\_an\_error** (rule type D, error rule): rule broken: Digits above 9 need letters in bases above 10. Kind: silent logic error. Trigger class: Base-16 conversion printing remainders as numbers (\`1015\` instead of \`AF\`).

## Same topic

`number_conversion` belongs to the topic **Applications (finite sums, Newton, conversion, gambler's ruin, factoring)** (`topic1.3.f`). The topic also contains: `accumulator_pattern`, `convergence_test`, `counter_pattern`, `debugging`, `fencepost_loop`, `flag_search_loop`, `loop_performance`, `monte_carlo_simulation`, `testing`.

## Rules of the concept (15)

- **Book** (SW-1e, p. 65 (pdf 75)): "Converting data from one representation to another is a frequent theme in writing computer programs."
- **E** (folk-meaning rule): Folk meaning: everyday digits are decimal, so '10011' reads as ten thousand and eleven, and 'converting' sounds like changing the number. Binary conversion changes only the representation: 19 and 10011 (base 2) are the same integer, printed as a sequence of bits by casting out powers of 2.
- **T** (uneven-application rule): Applies the LT rule unevenly: on some passes v is halved before the comparison, or n -= v is applied when n &lt; v. The traced bits are then shifted or wrong (e.g. 1001 instead of 10011).
- **N** (identity rule): Algorithm: computing the base-2 (or base-k) representation of a positive integer by casting out powers of 2 in decreasing order, or by repeated division.
- **S** (declarative rule): First find v, the largest power of 2 ≤ N (\`while (v &lt;= N/2) v = 2\*v;\`). Then, with n = N, for each v from there down to 1: if n &lt; v print 0, else print 1 and set n -= v; then v = v/2.
- **LT** (operational sequencing rule): Order inside each pass: test \`v &gt; 0\`; compare n &lt; v; print the bit; subtract v from n only when the bit is 1; then halve v. The first loop runs to completion before the second begins.
- **OP** (evaluation / result rule): The output is the string of bits, most significant first. \`java Binary 19\` prints 10011, which is 16 + 2 + 1.
- **OS** (state-transition rule): One pass prints one bit, possibly subtracts v from n (19 becomes 3 when v = 16), and halves v (16 becomes 8).
- **R** (composition rule (with a neighbour)): with while\_loop: Two while loops in sequence: the first's exit state (v = largest power of 2 ≤ N) is the second's starting state. The second runs once per bit and ends when integer halving takes v from 1 to 0.
- **P** (plan / role rule): Plan: representation conversion. v is a stepper (powers of 2 in decreasing order), and n is the remaining excess that shrinks to 0. The same plan gives base-k conversion, and the right-to-left variant builds the string with \`s = (n % 2) + s\`.
- **C** (conservation rule): The right-to-left method \`for (n = N; n &gt; 0; n /= 2) s = (n % 2) + s;\` produces the same string. Appending instead (\`s = s + (n % 2)\`) reverses the bits. Invariant of the casting-out loop: the bits printed so far, times 2^(number of bits still to print), plus n, equals N.
- **D** (error rule): rule broken: When a 1 bit is printed, its power must be subtracted from n. (silent logic error)
- **D** (error rule): rule broken: The algorithm assumes a positive integer. (silent logic error)
- **D** (error rule): rule broken: The argument must parse as an int. (run-time exception)
- **D** (error rule): rule broken: Digits above 9 need letters in bases above 10. (silent logic error)
- **X** (applicability rule): Use a hand-written conversion loop to learn or to support unusual bases. In practice use Integer.toBinaryString (or Integer.toString(n, k)). Conversion is needed only for display or I/O, because arithmetic works on the int itself.

## How it is found in code and answers (reader block)

- **Aliases:** none
- **Code patterns:** `Integer\.toBinaryString\s*\(`, `\bpower\w*\s*(?:\*=|/=)\s*2\b`, `\b\w+\s*/=\s*2\s*;`, `\b(\w+)\s*=\s*\1\s*/\s*2\s*;`, `Integer\.to(?:Binary|Hex|Octal)String\s*\(`, `Integer\.parseInt\s*\([^,)]*,\s*\d+\s*\)`
- **Operator symbols:** none
- **Java types:** none

## The whole prerequisite chain

- **Everything it builds on (12):** `arithmetic_operators`, `boolean`, `boolean_expression`, `comparison_operators`, `data_type`, `expression`, `identifier`, `literal`, `logical_operators`, `primitive_type`, `variable`, `while_loop`
- **Everything that builds on it (0):** nothing

## Every edge in this view and its exact edge logic (17)

All the edges drawn in the picture, in the order: prerequisite, parallel, misconception, error, has_level, contains.

**1. `arithmetic_operators` &rarr; `number_conversion`** (prerequisite)

- **Exact edge logic:** Converting to binary works with powers of two, using / and % (or subtraction) on ints.
- **Grounding:** book\_passage

**2. `while_loop` &rarr; `number_conversion`** (prerequisite)

- **Exact edge logic:** Binary conversion repeats one step in a while loop: find the largest power of 2 not above n, output a bit and subtract.
- **Grounding:** book\_passage
- **Composition rule (R) of `while_loop` with `number_conversion`:** Binary conversion uses while loops: one to find the largest power of 2 &lt;= N, and one to cast out powers of 2 in decreasing order.
- **Composition rule (R) of `number_conversion` with `while_loop`:** Two while loops in sequence: the first's exit state (v = largest power of 2 ≤ N) is the second's starting state. The second runs once per bit and ends when integer halving takes v from 1 to 0.

**3. `number_conversion` &rarr; `number_conversion@L0`** (has_level)

- **Exact edge logic:** Number conversion (binary) -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (1 way).
  - **[0] everyday\_reading** (rule type E, folk-meaning rule): Folk meaning: everyday digits are decimal, so '10011' reads as ten thousand and eleven, and 'converting' sounds like changing the number. Binary conversion changes only the representation: 19 and 10011 (base 2) are the same integer, printed as a sequence of bits by casting out powers of 2.

**4. `number_conversion` &rarr; `number_conversion@L1`** (has_level)

- **Exact edge logic:** Number conversion (binary) -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).
  - **[0] names\_the\_element** (rule type N, identity rule): Algorithm: computing the base-2 (or base-k) representation of a positive integer by casting out powers of 2 in decreasing order, or by repeated division.
  - **[1] states\_the\_rule** (rule type S, declarative rule): First find v, the largest power of 2 ≤ N (\`while (v &lt;= N/2) v = 2\*v;\`). Then, with n = N, for each v from there down to 1: if n &lt; v print 0, else print 1 and set n -= v; then v = v/2.

**5. `number_conversion` &rarr; `number_conversion@L2`** (has_level)

- **Exact edge logic:** Number conversion (binary) -&gt; L2 (Multistructural): the answer applies the rules of Number conversion (binary) to every part of the code, in order (3 ways).
  - **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): Order inside each pass: test \`v &gt; 0\`; compare n &lt; v; print the bit; subtract v from n only when the bit is 1; then halve v. The first loop runs to completion before the second begins.
  - **[1] output\_prediction** (rule type OP, evaluation / result rule): The output is the string of bits, most significant first. \`java Binary 19\` prints 10011, which is 16 + 2 + 1.
  - **[2] one\_step\_execution** (rule type OS, state-transition rule): One pass prints one bit, possibly subtracts v from n (19 becomes 3 when v = 16), and halves v (16 becomes 8).

**6. `number_conversion` &rarr; `number_conversion@L3`** (has_level)

- **Exact edge logic:** Number conversion (binary) -&gt; L3 (Relational): the answer relates the parts (2 ways).
  - **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Two while loops in sequence: the first's exit state (v = largest power of 2 ≤ N) is the second's starting state. The second runs once per bit and ends when integer halving takes v from 1 to 0.
  - **[1] purpose\_of\_the\_whole** (rule type P, plan / role rule): Plan: representation conversion. v is a stepper (powers of 2 in decreasing order), and n is the remaining excess that shrinks to 0. The same plan gives base-k conversion, and the right-to-left variant builds the string with \`s = (n % 2) + s\`.

**7. `number_conversion` &rarr; `number_conversion@L4`** (has_level)

- **Exact edge logic:** Number conversion (binary) -&gt; L4 (Extended abstract): the answer reasons beyond the given code (6 ways).
  - **[0] predict\_a\_change** (rule type C, conservation rule): The right-to-left method \`for (n = N; n &gt; 0; n /= 2) s = (n % 2) + s;\` produces the same string. Appending instead (\`s = s + (n % 2)\`) reverses the bits. Invariant of the casting-out loop: the bits printed so far, times 2^(number of bits still to print), plus n, equals N.
  - **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Use a hand-written conversion loop to learn or to support unusual bases. In practice use Integer.toBinaryString (or Integer.toString(n, k)). Conversion is needed only for display or I/O, because arithmetic works on the int itself.
  - **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: When a 1 bit is printed, its power must be subtracted from n. Kind: silent logic error. Trigger class: Forgetting \`n -= v\`: every bit after the first prints 1 whenever n ≥ v (19 prints 11111).
  - **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: The algorithm assumes a positive integer. Kind: silent logic error. Trigger class: N ≤ 0 (e.g. -5): the program prints 0, not a representation of N.
  - **[4] diagnose\_an\_error** (rule type D, error rule): rule broken: The argument must parse as an int. Kind: run-time exception. Trigger class: A non-integer or too-large argument (\`java Binary 3.5\`): Integer.parseInt throws NumberFormatException.
  - **[5] diagnose\_an\_error** (rule type D, error rule): rule broken: Digits above 9 need letters in bases above 10. Kind: silent logic error. Trigger class: Base-16 conversion printing remainders as numbers (\`1015\` instead of \`AF\`).

**8. `topic1.3.f` &rarr; `number_conversion`** (contains)

- topic `topic1.3.f` contains `number_conversion`

**9. `topic1.3.f` &rarr; `accumulator_pattern`** (contains)

- topic `topic1.3.f` contains `accumulator_pattern`

**10. `topic1.3.f` &rarr; `convergence_test`** (contains)

- topic `topic1.3.f` contains `convergence_test`

**11. `topic1.3.f` &rarr; `counter_pattern`** (contains)

- topic `topic1.3.f` contains `counter_pattern`

**12. `topic1.3.f` &rarr; `debugging`** (contains)

- topic `topic1.3.f` contains `debugging`

**13. `topic1.3.f` &rarr; `fencepost_loop`** (contains)

- topic `topic1.3.f` contains `fencepost_loop`

**14. `topic1.3.f` &rarr; `flag_search_loop`** (contains)

- topic `topic1.3.f` contains `flag_search_loop`

**15. `topic1.3.f` &rarr; `loop_performance`** (contains)

- topic `topic1.3.f` contains `loop_performance`

**16. `topic1.3.f` &rarr; `monte_carlo_simulation`** (contains)

- topic `topic1.3.f` contains `monte_carlo_simulation`

**17. `topic1.3.f` &rarr; `testing`** (contains)

- topic `topic1.3.f` contains `testing`
