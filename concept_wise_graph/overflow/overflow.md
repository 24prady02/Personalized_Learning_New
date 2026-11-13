# overflow (`overflow`)

int arithmetic wraps around outside the 32-bit range

Section 1.2 Built-in Types of Data, topic 1.2.c Integers.

![The knowledge graph around overflow](overflow.png)

## At a glance

- **Needs first:** `int`
- **Leads to:** `integer_constants`
- **Learned alongside:** `floating_point_precision`
- **Misconceptions:** `AbsAlwaysNonNegative`, `IntOverflowWidensAutomatically`
- **Errors:** none
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 21 edges around this concept. The edge logic, the wrong and right rules and the exact rules of the ways are copied word for word from the graph.

## To work on (1)

- misconceptions with no L0 way linked to them: AbsAlwaysNonNegative

## What it needs first (1)

A prerequisite edge means the other concept has to be understood before `overflow`.

### `int` comes before `overflow`

*32-bit integer primitive*

- **Edge:** `pre:int->overflow`
- **Exact edge logic:** Overflow happens because an int has a fixed 32-bit range.
- **Grounding:** book\_passage
- **Composition rule (R) of `overflow` with `int`:** Overflow is possible because int has a fixed 32-bit range, -2^31 to 2^31 - 1.
- **Composition rule (R) of `int` with `overflow`:** Because int has a fixed 32-bit range, results outside it wrap around silently.

## What it leads to (1)

These concepts need `overflow` first.

### `overflow` comes before `integer_constants`

*Integer.MAX\_VALUE, Integer.MIN\_VALUE and their edge cases*

- **Edge:** `pre:overflow->integer_constants`
- **Exact edge logic:** Integer.MAX\_VALUE is used to test for overflow: an int result that would go past it wraps around to a negative value.
- **Grounding:** book\_passage
- **Composition rule (R) of `overflow` with `integer_constants`:** Integer.MAX\_VALUE and Integer.MIN\_VALUE mark the edges of the range. Testing a &gt; Integer.MAX\_VALUE - b before computing a + b avoids overflow.
- **Composition rule (R) of `integer_constants` with `overflow`:** Integer.MAX\_VALUE marks the overflow boundary: an int result past it wraps to a negative value, so a test such as sum &gt; Integer.MAX\_VALUE on an int is always false; an overflow guard must test before the operation (e.g. a &gt; Integer.MAX\_VALUE - b) or use long.

## Learned alongside (1)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

### `overflow` alongside `floating_point_precision`

*double values are approximations; == on doubles is unreliable*

- **Edge:** `par:overflow~floating_point_precision`
- **Exact edge logic:** Both come from finite representations: an int result too large for 32 bits wraps around silently (overflow), while a double keeps about 15 significant digits so most results are approximations (5.0/3.0 is 1.6666666666666667). Neither raises an error.
- **Grounding:** book\_passage

## Misconceptions (2)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### AbsAlwaysNonNegative

- **Edge:** `overflow` &rarr; `AbsAlwaysNonNegative` (misconception)
- **Exact edge logic (the wrong rule):** Math.abs always returns a non-negative number.
- **Twin logic (the right rule):** Math.abs(Integer.MIN\_VALUE) returns Integer.MIN\_VALUE, which is negative.
- **Wrong belief (on the node):** Math.abs always returns a non-negative number.
- **Correct rule (on the node):** Math.abs(Integer.MIN\_VALUE) returns Integer.MIN\_VALUE, which is negative.
- **Provenance:** rule\_dictionary
- **Role of this concept:** context
- **L0 way linked to it:** no
- **Edge `integer_constants` &rarr; `AbsAlwaysNonNegative`, exact edge logic:** Math.abs always returns a non-negative number. **Twin logic:** Math.abs(Integer.MIN\_VALUE) returns Integer.MIN\_VALUE, which is negative. (role: context)
- **Edge `math_library` &rarr; `AbsAlwaysNonNegative`, exact edge logic:** Math.abs always returns a non-negative number. **Twin logic:** Math.abs(Integer.MIN\_VALUE) returns Integer.MIN\_VALUE, which is negative. (role: primary)

### IntOverflowWidensAutomatically

- **Edge:** `overflow` &rarr; `IntOverflowWidensAutomatically` (misconception)
- **Exact edge logic (the wrong rule):** An int result that is too large is automatically stored as a bigger number.
- **Twin logic (the right rule):** int arithmetic is 32-bit; a result outside the range wraps around.
- **Wrong belief (on the node):** An int result that is too large is automatically stored as a bigger number.
- **Correct rule (on the node):** int arithmetic is 32-bit; a result outside the range wraps around.
- **Provenance:** textbook
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [1] misconception, exact rule:** wrong rule: An int result that is too large is automatically stored as a bigger number. Right rule: int arithmetic is 32-bit; a result outside the range wraps around.
- **L0 way [2] inconsistent\_trace, exact rule:** Points to LT (each int operation wraps as soon as it leaves the range). Applied unevenly, a student wraps one step but writes a + 1 for a = Integer.MAX\_VALUE as 2147483648. (here mixing in: "An int result that is too large is automatically stored as a bigger number")
- **Edge `int` &rarr; `IntOverflowWidensAutomatically`, exact edge logic:** An int result that is too large is automatically stored as a bigger number. **Twin logic:** int arithmetic is 32-bit; a result outside the range wraps around. (role: context)

## Errors (0)

An error edge states the rule that gets broken in a program, and the right rule.

The graph has no error edge from this concept.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for overflow: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to overflow agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

- **Edge:** `overflow` &rarr; `overflow@L0` (has_level)
- **Exact edge logic:** overflow -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (3 ways).

Ways (3), each with its exact rule:

- **[0] everyday\_reading** (rule type E, folk-meaning rule): Everyday arithmetic assumes a bigger result just takes more digits. A Java int keeps only 32 bits, so a result that is too large wraps silently to a wrong (often negative) value.
- **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `IntOverflowWidensAutomatically`: wrong rule: An int result that is too large is automatically stored as a bigger number. Right rule: int arithmetic is 32-bit; a result outside the range wraps around.
- **[2] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `IntOverflowWidensAutomatically`: Points to LT (each int operation wraps as soon as it leaves the range). Applied unevenly, a student wraps one step but writes a + 1 for a = Integer.MAX\_VALUE as 2147483648. (here mixing in: "An int result that is too large is automatically stored as a bigger number")

### L1: Unistructural / atom x text surface

L1 for overflow: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

- **Edge:** `overflow` &rarr; `overflow@L1` (has_level)
- **Exact edge logic:** overflow -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

Ways (2), each with its exact rule:

- **[0] names\_the\_element** (rule type N, identity rule): Overflow: the situation where an integer result is too large or too small for its type's fixed bits and is truncated, wrapping around.
- **[1] states\_the\_rule** (rule type S, declarative rule): int and long arithmetic is done in 32-bit and 64-bit two's complement. An out-of-range result keeps only its low-order bits, and no error or exception is raised.

### L2: Multistructural / block x execution / preoperational

L2 for overflow: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

- **Edge:** `overflow` &rarr; `overflow@L2` (has_level)
- **Exact edge logic:** overflow -&gt; L2 (Multistructural): the answer applies the rules of overflow to every part of the code, in order (3 ways).

Ways (3), each with its exact rule:

- **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): Overflow happens in the single operation whose result leaves the range, before any later widening. With int a and b, long x = a \* b; overflows in 32-bit int arithmetic before the result is converted to long.
- **[1] output\_prediction** (rule type OP, evaluation / result rule): Integer.MAX\_VALUE + 1 is -2147483648, 2 \* Integer.MAX\_VALUE is -2, and Math.abs(-2147483648) is -2147483648.
- **[2] one\_step\_execution** (rule type OS, state-transition rule): The variable receives the wrapped value and nothing signals the error, so later statements carry on with it.

### L3: Relational / relations x function (concrete operational begins)

L3 for overflow: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

- **Edge:** `overflow` &rarr; `overflow@L3` (has_level)
- **Exact edge logic:** overflow -&gt; L3 (Relational): the answer relates the parts (4 ways).

Ways (4), each with its exact rule:

- **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Overflow is possible because int has a fixed 32-bit range, -2^31 to 2^31 - 1.
- **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Integer.MAX\_VALUE and Integer.MIN\_VALUE mark the edges of the range. Testing a &gt; Integer.MAX\_VALUE - b before computing a + b avoids overflow.
- **[2] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Both come from finite representations: an int result too large for 32 bits wraps around silently (overflow), while a double keeps about 15 significant digits so most results are approximations (5.0/3.0 is 1.6666666666666667). Neither raises an error.
- **[3] purpose\_of\_the\_whole** (rule type P, plan / role rule): Knowing about overflow lets you guard against it: use long for products, factorials and large sums, or check against MAX\_VALUE before computing.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for overflow: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

- **Edge:** `overflow` &rarr; `overflow@L4` (has_level)
- **Exact edge logic:** overflow -&gt; L4 (Extended abstract): the answer reasons beyond the given code (4 ways).

Ways (4), each with its exact rule:

- **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `IntOverflowWidensAutomatically`: Changing int to long moves the overflow point (to about 9.2e18) but does not remove it. Dividing before multiplying can avoid overflow at the cost of truncation. Casting a result that has already overflowed does not repair it.
- **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Think about overflow whenever values can reach the billions. Use long (or a long operand, such as 1000L) for those, BigInteger for unbounded integers, and plain int for small counts and indices.
- **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: int results are limited to 32 bits, and overflow is not reported. Kind: silent logic error. Trigger class: Values that reach into the billions: factorials above 12!, large products or powers, sums of many large values, Math.abs(Integer.MIN\_VALUE).
- **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: An all-int expression is computed in int even when its result is stored in a long. Kind: silent logic error. Trigger class: long total = a \* b; or long ms = days \* 24 \* 60 \* 60 \* 1000; with int operands.

## Same topic

`overflow` belongs to the topic **Integers** (`topic1.2.c`). The topic also contains: `arithmetic_operators`, `int`, `int_literal_limit`, `integer_constants`, `integer_division`, `long_type`, `remainder_operator`.

## Rules of the concept (15)

- **Book** (SW-1e, p. 21 (pdf 31)): "if the result is too large to fit into int's 32-bit representation, then it will be truncated in a well-defined manner."
- **Book** (SW-1e, p. 21 (pdf 31)): "This situation is known as overflow."
- **Book** (OT-Datatypes, ): "By default, the int data type is a 32-bit signed two's complement integer"
- **E** (folk-meaning rule): Everyday arithmetic assumes a bigger result just takes more digits. A Java int keeps only 32 bits, so a result that is too large wraps silently to a wrong (often negative) value.
- **M** (wrong rule / right rule): IntOverflowWidensAutomatically: wrong: An int result that is too large is automatically stored as a bigger number. \| right: int arithmetic is 32-bit; a result outside the range wraps around.
- **T** (uneven-application rule): Points to LT (each int operation wraps as soon as it leaves the range). Applied unevenly, a student wraps one step but writes a + 1 for a = Integer.MAX\_VALUE as 2147483648.
- **N** (identity rule): Overflow: the situation where an integer result is too large or too small for its type's fixed bits and is truncated, wrapping around.
- **S** (declarative rule): int and long arithmetic is done in 32-bit and 64-bit two's complement. An out-of-range result keeps only its low-order bits, and no error or exception is raised.
- **LT** (operational sequencing rule): Overflow happens in the single operation whose result leaves the range, before any later widening. With int a and b, long x = a \* b; overflows in 32-bit int arithmetic before the result is converted to long.
- **OP** (evaluation / result rule): Integer.MAX\_VALUE + 1 is -2147483648, 2 \* Integer.MAX\_VALUE is -2, and Math.abs(-2147483648) is -2147483648.
- **OS** (state-transition rule): The variable receives the wrapped value and nothing signals the error, so later statements carry on with it.
- **R** (composition rule (with a neighbour)): with int: Overflow is possible because int has a fixed 32-bit range, -2^31 to 2^31 - 1.
- **R** (composition rule (with a neighbour)): with integer\_constants: Integer.MAX\_VALUE and Integer.MIN\_VALUE mark the edges of the range. Testing a &gt; Integer.MAX\_VALUE - b before computing a + b avoids overflow.
- **P** (plan / role rule): Knowing about overflow lets you guard against it: use long for products, factorials and large sums, or check against MAX\_VALUE before computing.
- **C** (conservation rule): Changing int to long moves the overflow point (to about 9.2e18) but does not remove it. Dividing before multiplying can avoid overflow at the cost of truncation. Casting a result that has already overflowed does not repair it.
- **D** (error rule): rule broken: int results are limited to 32 bits, and overflow is not reported. (silent logic error)
- **D** (error rule): rule broken: An all-int expression is computed in int even when its result is stored in a long. (silent logic error)
- **X** (applicability rule): Think about overflow whenever values can reach the billions. Use long (or a long operand, such as 1000L) for those, BigInteger for unbounded integers, and plain int for small counts and indices.

## How it is found in code and answers (reader block)

- **Aliases:** overflow, overflows, wraps around
- **Code patterns:** `Integer\.(?:MAX|MIN)_VALUE\s*[+\-*]|[+\-*]\s*Integer\.(?:MAX|MIN)_VALUE|Math\.abs\s*\(\s*Integer\.MIN_VALUE|-\s*Integer\.MIN_VALUE`, `\b2147483647\s*\+|\+\s*2147483647\b|\b2147483647\s*\*|\*\s*2147483647\b`, `\b\d{7,}\s*\*\s*\d{5,}\b|\b\d{5,}\s*\*\s*\d{7,}\b`
- **Operator symbols:** none
- **Java types:** none
- **Signal int\_limit\_held\_in\_variable** (scope program, decisive): `\b(\w+)\s*=\s*(?:2147483647|-\s*2147483648|Integer\.(?:MAX|MIN)_VALUE)\s*;(?:(?!\b\1\s*=(?!=)(?![^;]*\b\1\b))[\s\S]){0,4000}?(?:\b\1\s*(?:[+\-*]|\+=|-=|\*=)|[+\-*]\s*\b\1\b)`

## The whole prerequisite chain

- **Everything it builds on (3):** `data_type`, `int`, `primitive_type`
- **Everything that builds on it (1):** `integer_constants`

## Every edge in this view and its exact edge logic (21)

All the edges drawn in the picture, in the order: prerequisite, parallel, misconception, error, has_level, contains.

**1. `int` &rarr; `overflow`** (prerequisite)

- **Exact edge logic:** Overflow happens because an int has a fixed 32-bit range.
- **Grounding:** book\_passage
- **Composition rule (R) of `int` with `overflow`:** Because int has a fixed 32-bit range, results outside it wrap around silently.
- **Composition rule (R) of `overflow` with `int`:** Overflow is possible because int has a fixed 32-bit range, -2^31 to 2^31 - 1.

**2. `overflow` &rarr; `integer_constants`** (prerequisite)

- **Exact edge logic:** Integer.MAX\_VALUE is used to test for overflow: an int result that would go past it wraps around to a negative value.
- **Grounding:** book\_passage
- **Composition rule (R) of `overflow` with `integer_constants`:** Integer.MAX\_VALUE and Integer.MIN\_VALUE mark the edges of the range. Testing a &gt; Integer.MAX\_VALUE - b before computing a + b avoids overflow.
- **Composition rule (R) of `integer_constants` with `overflow`:** Integer.MAX\_VALUE marks the overflow boundary: an int result past it wraps to a negative value, so a test such as sum &gt; Integer.MAX\_VALUE on an int is always false; an overflow guard must test before the operation (e.g. a &gt; Integer.MAX\_VALUE - b) or use long.

**3. `overflow` &harr; `floating_point_precision`** (parallel)

- **Exact edge logic:** Both come from finite representations: an int result too large for 32 bits wraps around silently (overflow), while a double keeps about 15 significant digits so most results are approximations (5.0/3.0 is 1.6666666666666667). Neither raises an error.
- **Grounding:** book\_passage

**4. `overflow` &rarr; `AbsAlwaysNonNegative`** (misconception)

- **Exact edge logic (the wrong rule):** Math.abs always returns a non-negative number.
- **Twin logic (the right rule):** Math.abs(Integer.MIN\_VALUE) returns Integer.MIN\_VALUE, which is negative.
- **Role:** context

**5. `overflow` &rarr; `IntOverflowWidensAutomatically`** (misconception)

- **Exact edge logic (the wrong rule):** An int result that is too large is automatically stored as a bigger number.
- **Twin logic (the right rule):** int arithmetic is 32-bit; a result outside the range wraps around.
- **Role:** primary

**6. `int` &rarr; `IntOverflowWidensAutomatically`** (misconception)

- **Exact edge logic (the wrong rule):** An int result that is too large is automatically stored as a bigger number.
- **Twin logic (the right rule):** int arithmetic is 32-bit; a result outside the range wraps around.
- **Role:** context

**7. `integer_constants` &rarr; `AbsAlwaysNonNegative`** (misconception)

- **Exact edge logic (the wrong rule):** Math.abs always returns a non-negative number.
- **Twin logic (the right rule):** Math.abs(Integer.MIN\_VALUE) returns Integer.MIN\_VALUE, which is negative.
- **Role:** context

**8. `math_library` &rarr; `AbsAlwaysNonNegative`** (misconception)

- **Exact edge logic (the wrong rule):** Math.abs always returns a non-negative number.
- **Twin logic (the right rule):** Math.abs(Integer.MIN\_VALUE) returns Integer.MIN\_VALUE, which is negative.
- **Role:** primary

**9. `overflow` &rarr; `overflow@L0`** (has_level)

- **Exact edge logic:** overflow -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (3 ways).
  - **[0] everyday\_reading** (rule type E, folk-meaning rule): Everyday arithmetic assumes a bigger result just takes more digits. A Java int keeps only 32 bits, so a result that is too large wraps silently to a wrong (often negative) value.
  - **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `IntOverflowWidensAutomatically`: wrong rule: An int result that is too large is automatically stored as a bigger number. Right rule: int arithmetic is 32-bit; a result outside the range wraps around.
  - **[2] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `IntOverflowWidensAutomatically`: Points to LT (each int operation wraps as soon as it leaves the range). Applied unevenly, a student wraps one step but writes a + 1 for a = Integer.MAX\_VALUE as 2147483648. (here mixing in: "An int result that is too large is automatically stored as a bigger number")

**10. `overflow` &rarr; `overflow@L1`** (has_level)

- **Exact edge logic:** overflow -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).
  - **[0] names\_the\_element** (rule type N, identity rule): Overflow: the situation where an integer result is too large or too small for its type's fixed bits and is truncated, wrapping around.
  - **[1] states\_the\_rule** (rule type S, declarative rule): int and long arithmetic is done in 32-bit and 64-bit two's complement. An out-of-range result keeps only its low-order bits, and no error or exception is raised.

**11. `overflow` &rarr; `overflow@L2`** (has_level)

- **Exact edge logic:** overflow -&gt; L2 (Multistructural): the answer applies the rules of overflow to every part of the code, in order (3 ways).
  - **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): Overflow happens in the single operation whose result leaves the range, before any later widening. With int a and b, long x = a \* b; overflows in 32-bit int arithmetic before the result is converted to long.
  - **[1] output\_prediction** (rule type OP, evaluation / result rule): Integer.MAX\_VALUE + 1 is -2147483648, 2 \* Integer.MAX\_VALUE is -2, and Math.abs(-2147483648) is -2147483648.
  - **[2] one\_step\_execution** (rule type OS, state-transition rule): The variable receives the wrapped value and nothing signals the error, so later statements carry on with it.

**12. `overflow` &rarr; `overflow@L3`** (has_level)

- **Exact edge logic:** overflow -&gt; L3 (Relational): the answer relates the parts (4 ways).
  - **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Overflow is possible because int has a fixed 32-bit range, -2^31 to 2^31 - 1.
  - **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Integer.MAX\_VALUE and Integer.MIN\_VALUE mark the edges of the range. Testing a &gt; Integer.MAX\_VALUE - b before computing a + b avoids overflow.
  - **[2] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Both come from finite representations: an int result too large for 32 bits wraps around silently (overflow), while a double keeps about 15 significant digits so most results are approximations (5.0/3.0 is 1.6666666666666667). Neither raises an error.
  - **[3] purpose\_of\_the\_whole** (rule type P, plan / role rule): Knowing about overflow lets you guard against it: use long for products, factorials and large sums, or check against MAX\_VALUE before computing.

**13. `overflow` &rarr; `overflow@L4`** (has_level)

- **Exact edge logic:** overflow -&gt; L4 (Extended abstract): the answer reasons beyond the given code (4 ways).
  - **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `IntOverflowWidensAutomatically`: Changing int to long moves the overflow point (to about 9.2e18) but does not remove it. Dividing before multiplying can avoid overflow at the cost of truncation. Casting a result that has already overflowed does not repair it.
  - **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Think about overflow whenever values can reach the billions. Use long (or a long operand, such as 1000L) for those, BigInteger for unbounded integers, and plain int for small counts and indices.
  - **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: int results are limited to 32 bits, and overflow is not reported. Kind: silent logic error. Trigger class: Values that reach into the billions: factorials above 12!, large products or powers, sums of many large values, Math.abs(Integer.MIN\_VALUE).
  - **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: An all-int expression is computed in int even when its result is stored in a long. Kind: silent logic error. Trigger class: long total = a \* b; or long ms = days \* 24 \* 60 \* 60 \* 1000; with int operands.

**14. `topic1.2.c` &rarr; `overflow`** (contains)

- topic `topic1.2.c` contains `overflow`

**15. `topic1.2.c` &rarr; `arithmetic_operators`** (contains)

- topic `topic1.2.c` contains `arithmetic_operators`

**16. `topic1.2.c` &rarr; `int`** (contains)

- topic `topic1.2.c` contains `int`

**17. `topic1.2.c` &rarr; `int_literal_limit`** (contains)

- topic `topic1.2.c` contains `int_literal_limit`

**18. `topic1.2.c` &rarr; `integer_constants`** (contains)

- topic `topic1.2.c` contains `integer_constants`

**19. `topic1.2.c` &rarr; `integer_division`** (contains)

- topic `topic1.2.c` contains `integer_division`

**20. `topic1.2.c` &rarr; `long_type`** (contains)

- topic `topic1.2.c` contains `long_type`

**21. `topic1.2.c` &rarr; `remainder_operator`** (contains)

- topic `topic1.2.c` contains `remainder_operator`
