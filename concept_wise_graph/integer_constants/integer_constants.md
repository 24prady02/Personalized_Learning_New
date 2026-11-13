# integer_constants (`integer_constants`)

Integer.MAX\_VALUE, Integer.MIN\_VALUE and their edge cases

Section 1.2 Built-in Types of Data, topic 1.2.c Integers.

![The knowledge graph around integer_constants](integer_constants.png)

## At a glance

- **Needs first:** `overflow`
- **Leads to:** nothing
- **Learned alongside:** nothing
- **Misconceptions:** `AbsAlwaysNonNegative`
- **Errors:** none
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 17 edges around this concept. The edge logic, the wrong and right rules and the exact rules of the ways are copied word for word from the graph.

## To work on (1)

- misconceptions with no L0 way linked to them: AbsAlwaysNonNegative

## What it needs first (1)

A prerequisite edge means the other concept has to be understood before `integer_constants`.

### `overflow` comes before `integer_constants`

*int arithmetic wraps around outside the 32-bit range*

- **Edge:** `pre:overflow->integer_constants`
- **Exact edge logic:** Integer.MAX\_VALUE is used to test for overflow: an int result that would go past it wraps around to a negative value.
- **Grounding:** book\_passage
- **Composition rule (R) of `integer_constants` with `overflow`:** Integer.MAX\_VALUE marks the overflow boundary: an int result past it wraps to a negative value, so a test such as sum &gt; Integer.MAX\_VALUE on an int is always false; an overflow guard must test before the operation (e.g. a &gt; Integer.MAX\_VALUE - b) or use long.
- **Composition rule (R) of `overflow` with `integer_constants`:** Integer.MAX\_VALUE and Integer.MIN\_VALUE mark the edges of the range. Testing a &gt; Integer.MAX\_VALUE - b before computing a + b avoids overflow.

## What it leads to (0)

These concepts need `integer_constants` first.

No concept has this one as a prerequisite.

## Learned alongside (0)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

No parallel edge touches this concept.

## Misconceptions (1)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### AbsAlwaysNonNegative

- **Edge:** `integer_constants` &rarr; `AbsAlwaysNonNegative` (misconception)
- **Exact edge logic (the wrong rule):** Math.abs always returns a non-negative number.
- **Twin logic (the right rule):** Math.abs(Integer.MIN\_VALUE) returns Integer.MIN\_VALUE, which is negative.
- **Wrong belief (on the node):** Math.abs always returns a non-negative number.
- **Correct rule (on the node):** Math.abs(Integer.MIN\_VALUE) returns Integer.MIN\_VALUE, which is negative.
- **Provenance:** rule\_dictionary
- **Role of this concept:** context
- **L0 way linked to it:** no
- **Edge `math_library` &rarr; `AbsAlwaysNonNegative`, exact edge logic:** Math.abs always returns a non-negative number. **Twin logic:** Math.abs(Integer.MIN\_VALUE) returns Integer.MIN\_VALUE, which is negative. (role: primary)
- **Edge `overflow` &rarr; `AbsAlwaysNonNegative`, exact edge logic:** Math.abs always returns a non-negative number. **Twin logic:** Math.abs(Integer.MIN\_VALUE) returns Integer.MIN\_VALUE, which is negative. (role: context)

## Errors (0)

An error edge states the rule that gets broken in a program, and the right rule.

The graph has no error edge from this concept.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for integer constants: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to integer constants agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

- **Edge:** `integer_constants` &rarr; `integer_constants@L0` (has_level)
- **Exact edge logic:** integer constants -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (1 way).

Ways (1), each with its exact rule:

- **[0] everyday\_reading** (rule type E, folk-meaning rule): Folk meaning: 'maximum' is a ceiling that nothing can pass (like a full tank, adding more leaves it full) and an absolute value is never negative. Java rule: int arithmetic wraps around silently, so Integer.MAX\_VALUE + 1 is Integer.MIN\_VALUE and Math.abs(Integer.MIN\_VALUE) is still -2147483648.

### L1: Unistructural / atom x text surface

L1 for integer constants: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

- **Edge:** `integer_constants` &rarr; `integer_constants@L1` (has_level)
- **Exact edge logic:** integer constants -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

Ways (2), each with its exact rule:

- **[0] names\_the\_element** (rule type N, identity rule): Integer.MAX\_VALUE and Integer.MIN\_VALUE are named constants of the wrapper class Integer: the largest int, 2147483647 (2^31 - 1), and the smallest int, -2147483648 (-2^31).
- **[1] states\_the\_rule** (rule type S, declarative rule): Each wrapper class defines MIN\_VALUE and MAX\_VALUE; for int the range is -2147483648 to 2147483647 inclusive, and results outside it are truncated (wrap) without any error signal.

### L2: Multistructural / block x execution / preoperational

L2 for integer constants: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

- **Edge:** `integer_constants` &rarr; `integer_constants@L2` (has_level)
- **Exact edge logic:** integer constants -&gt; L2 (Multistructural): the answer applies the rules of integer constants to every part of the code, in order (3 ways).

Ways (3), each with its exact rule:

- **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): The constant is read like a variable when its expression is evaluated; then operators are applied in precedence order, left operand first, each in 32-bit int arithmetic, wrapping at each step that leaves the range.
- **[1] output\_prediction** (rule type OP, evaluation / result rule): Type int, value wrapped modulo 2^32: Integer.MAX\_VALUE + 1 is -2147483648, Integer.MIN\_VALUE - 1 is 2147483647, 2 \* Integer.MAX\_VALUE is -2, and Math.abs(Integer.MIN\_VALUE) is -2147483648.
- **[2] one\_step\_execution** (rule type OS, state-transition rule): Reading the constant changes nothing (it is final); after int a = Integer.MAX\_VALUE; a = a + 1; the variable a holds Integer.MIN\_VALUE, and no exception is raised.

### L3: Relational / relations x function (concrete operational begins)

L3 for integer constants: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

- **Edge:** `integer_constants` &rarr; `integer_constants@L3` (has_level)
- **Exact edge logic:** integer constants -&gt; L3 (Relational): the answer relates the parts (2 ways).

Ways (2), each with its exact rule:

- **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Integer.MAX\_VALUE marks the overflow boundary: an int result past it wraps to a negative value, so a test such as sum &gt; Integer.MAX\_VALUE on an int is always false; an overflow guard must test before the operation (e.g. a &gt; Integer.MAX\_VALUE - b) or use long.
- **[1] purpose\_of\_the\_whole** (rule type P, plan / role rule): Used as the initial value of a most-wanted holder (Sajaniemi): max = Integer.MIN\_VALUE (or min = Integer.MAX\_VALUE) so the first real value always replaces it; also used as limits in overflow guards.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for integer constants: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

- **Edge:** `integer_constants` &rarr; `integer_constants@L4` (has_level)
- **Exact edge logic:** integer constants -&gt; L4 (Extended abstract): the answer reasons beyond the given code (3 ways).

Ways (3), each with its exact rule:

- **[0] predict\_a\_change** (rule type C, conservation rule): Changing the type from int to long moves the wrap point from 2^31 to 2^63 but does not remove it; replacing the initial max = Integer.MIN\_VALUE by max = 0 breaks the search for all-negative inputs. Invariant: the range is asymmetric, Integer.MIN\_VALUE == -Integer.MAX\_VALUE - 1, so negating MIN\_VALUE gives MIN\_VALUE back.
- **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Use Integer.MAX\_VALUE / MIN\_VALUE as sentinels for min/max searches and as bounds in overflow checks instead of typing digits; when values can approach the limits, switch to long rather than relying on the int constants.
- **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: int arithmetic stays within Integer.MIN\_VALUE..Integer.MAX\_VALUE by wrapping, without error. Kind: silent logic error. Trigger class: Any int computation whose true result exceeds Integer.MAX\_VALUE or is below Integer.MIN\_VALUE: sums/products of large values, MAX\_VALUE + 1, -Integer.MIN\_VALUE, Math.abs(Integer.MIN\_VALUE).

## Same topic

`integer_constants` belongs to the topic **Integers** (`topic1.2.c`). The topic also contains: `arithmetic_operators`, `int`, `int_literal_limit`, `integer_division`, `long_type`, `overflow`, `remainder_operator`.

## Rules of the concept (12)

- **Book** (SW-1e, p. 40 (pdf 50)): "int a = 2147483647 (or equivalently, Integer.MAX\_VALUE)"
- **Book** (CSA, ): "If you want to set a value to the smallest possible int values use Integer.MIN\_VALUE."
- **E** (folk-meaning rule): Folk meaning: 'maximum' is a ceiling that nothing can pass (like a full tank, adding more leaves it full) and an absolute value is never negative. Java rule: int arithmetic wraps around silently, so Integer.MAX\_VALUE + 1 is Integer.MIN\_VALUE and Math.abs(Integer.MIN\_VALUE) is still -2147483648.
- **T** (uneven-application rule): Points to LT (each operator on an int is carried out in 32-bit arithmetic and wraps). Applied unevenly: in a trace of 1.2.10 the student wraps a+1 to a negative value but then treats 2\*a or 4\*a as ordinary mathematical products (or vice versa).
- **N** (identity rule): Integer.MAX\_VALUE and Integer.MIN\_VALUE are named constants of the wrapper class Integer: the largest int, 2147483647 (2^31 - 1), and the smallest int, -2147483648 (-2^31).
- **S** (declarative rule): Each wrapper class defines MIN\_VALUE and MAX\_VALUE; for int the range is -2147483648 to 2147483647 inclusive, and results outside it are truncated (wrap) without any error signal.
- **LT** (operational sequencing rule): The constant is read like a variable when its expression is evaluated; then operators are applied in precedence order, left operand first, each in 32-bit int arithmetic, wrapping at each step that leaves the range.
- **OP** (evaluation / result rule): Type int, value wrapped modulo 2^32: Integer.MAX\_VALUE + 1 is -2147483648, Integer.MIN\_VALUE - 1 is 2147483647, 2 \* Integer.MAX\_VALUE is -2, and Math.abs(Integer.MIN\_VALUE) is -2147483648.
- **OS** (state-transition rule): Reading the constant changes nothing (it is final); after int a = Integer.MAX\_VALUE; a = a + 1; the variable a holds Integer.MIN\_VALUE, and no exception is raised.
- **R** (composition rule (with a neighbour)): with overflow: Integer.MAX\_VALUE marks the overflow boundary: an int result past it wraps to a negative value, so a test such as sum &gt; Integer.MAX\_VALUE on an int is always false; an overflow guard must test before the operation (e.g. a &gt; Integer.MAX\_VALUE - b) or use long.
- **P** (plan / role rule): Used as the initial value of a most-wanted holder (Sajaniemi): max = Integer.MIN\_VALUE (or min = Integer.MAX\_VALUE) so the first real value always replaces it; also used as limits in overflow guards.
- **C** (conservation rule): Changing the type from int to long moves the wrap point from 2^31 to 2^63 but does not remove it; replacing the initial max = Integer.MIN\_VALUE by max = 0 breaks the search for all-negative inputs. Invariant: the range is asymmetric, Integer.MIN\_VALUE == -Integer.MAX\_VALUE - 1, so negating MIN\_VALUE gives MIN\_VALUE back.
- **D** (error rule): rule broken: int arithmetic stays within Integer.MIN\_VALUE..Integer.MAX\_VALUE by wrapping, without error. (silent logic error)
- **X** (applicability rule): Use Integer.MAX\_VALUE / MIN\_VALUE as sentinels for min/max searches and as bounds in overflow checks instead of typing digits; when values can approach the limits, switch to long rather than relying on the int constants.

## How it is found in code and answers (reader block)

- **Aliases:** max\_value, min\_value
- **Code patterns:** `Integer\.(?:MAX|MIN)_VALUE`, `Long\.(?:MAX|MIN)_VALUE`
- **Operator symbols:** none
- **Java types:** none

## The whole prerequisite chain

- **Everything it builds on (4):** `data_type`, `int`, `overflow`, `primitive_type`
- **Everything that builds on it (0):** nothing

## Every edge in this view and its exact edge logic (17)

All the edges drawn in the picture, in the order: prerequisite, parallel, misconception, error, has_level, contains.

**1. `overflow` &rarr; `integer_constants`** (prerequisite)

- **Exact edge logic:** Integer.MAX\_VALUE is used to test for overflow: an int result that would go past it wraps around to a negative value.
- **Grounding:** book\_passage
- **Composition rule (R) of `overflow` with `integer_constants`:** Integer.MAX\_VALUE and Integer.MIN\_VALUE mark the edges of the range. Testing a &gt; Integer.MAX\_VALUE - b before computing a + b avoids overflow.
- **Composition rule (R) of `integer_constants` with `overflow`:** Integer.MAX\_VALUE marks the overflow boundary: an int result past it wraps to a negative value, so a test such as sum &gt; Integer.MAX\_VALUE on an int is always false; an overflow guard must test before the operation (e.g. a &gt; Integer.MAX\_VALUE - b) or use long.

**2. `integer_constants` &rarr; `AbsAlwaysNonNegative`** (misconception)

- **Exact edge logic (the wrong rule):** Math.abs always returns a non-negative number.
- **Twin logic (the right rule):** Math.abs(Integer.MIN\_VALUE) returns Integer.MIN\_VALUE, which is negative.
- **Role:** context

**3. `math_library` &rarr; `AbsAlwaysNonNegative`** (misconception)

- **Exact edge logic (the wrong rule):** Math.abs always returns a non-negative number.
- **Twin logic (the right rule):** Math.abs(Integer.MIN\_VALUE) returns Integer.MIN\_VALUE, which is negative.
- **Role:** primary

**4. `overflow` &rarr; `AbsAlwaysNonNegative`** (misconception)

- **Exact edge logic (the wrong rule):** Math.abs always returns a non-negative number.
- **Twin logic (the right rule):** Math.abs(Integer.MIN\_VALUE) returns Integer.MIN\_VALUE, which is negative.
- **Role:** context

**5. `integer_constants` &rarr; `integer_constants@L0`** (has_level)

- **Exact edge logic:** integer constants -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (1 way).
  - **[0] everyday\_reading** (rule type E, folk-meaning rule): Folk meaning: 'maximum' is a ceiling that nothing can pass (like a full tank, adding more leaves it full) and an absolute value is never negative. Java rule: int arithmetic wraps around silently, so Integer.MAX\_VALUE + 1 is Integer.MIN\_VALUE and Math.abs(Integer.MIN\_VALUE) is still -2147483648.

**6. `integer_constants` &rarr; `integer_constants@L1`** (has_level)

- **Exact edge logic:** integer constants -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).
  - **[0] names\_the\_element** (rule type N, identity rule): Integer.MAX\_VALUE and Integer.MIN\_VALUE are named constants of the wrapper class Integer: the largest int, 2147483647 (2^31 - 1), and the smallest int, -2147483648 (-2^31).
  - **[1] states\_the\_rule** (rule type S, declarative rule): Each wrapper class defines MIN\_VALUE and MAX\_VALUE; for int the range is -2147483648 to 2147483647 inclusive, and results outside it are truncated (wrap) without any error signal.

**7. `integer_constants` &rarr; `integer_constants@L2`** (has_level)

- **Exact edge logic:** integer constants -&gt; L2 (Multistructural): the answer applies the rules of integer constants to every part of the code, in order (3 ways).
  - **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): The constant is read like a variable when its expression is evaluated; then operators are applied in precedence order, left operand first, each in 32-bit int arithmetic, wrapping at each step that leaves the range.
  - **[1] output\_prediction** (rule type OP, evaluation / result rule): Type int, value wrapped modulo 2^32: Integer.MAX\_VALUE + 1 is -2147483648, Integer.MIN\_VALUE - 1 is 2147483647, 2 \* Integer.MAX\_VALUE is -2, and Math.abs(Integer.MIN\_VALUE) is -2147483648.
  - **[2] one\_step\_execution** (rule type OS, state-transition rule): Reading the constant changes nothing (it is final); after int a = Integer.MAX\_VALUE; a = a + 1; the variable a holds Integer.MIN\_VALUE, and no exception is raised.

**8. `integer_constants` &rarr; `integer_constants@L3`** (has_level)

- **Exact edge logic:** integer constants -&gt; L3 (Relational): the answer relates the parts (2 ways).
  - **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Integer.MAX\_VALUE marks the overflow boundary: an int result past it wraps to a negative value, so a test such as sum &gt; Integer.MAX\_VALUE on an int is always false; an overflow guard must test before the operation (e.g. a &gt; Integer.MAX\_VALUE - b) or use long.
  - **[1] purpose\_of\_the\_whole** (rule type P, plan / role rule): Used as the initial value of a most-wanted holder (Sajaniemi): max = Integer.MIN\_VALUE (or min = Integer.MAX\_VALUE) so the first real value always replaces it; also used as limits in overflow guards.

**9. `integer_constants` &rarr; `integer_constants@L4`** (has_level)

- **Exact edge logic:** integer constants -&gt; L4 (Extended abstract): the answer reasons beyond the given code (3 ways).
  - **[0] predict\_a\_change** (rule type C, conservation rule): Changing the type from int to long moves the wrap point from 2^31 to 2^63 but does not remove it; replacing the initial max = Integer.MIN\_VALUE by max = 0 breaks the search for all-negative inputs. Invariant: the range is asymmetric, Integer.MIN\_VALUE == -Integer.MAX\_VALUE - 1, so negating MIN\_VALUE gives MIN\_VALUE back.
  - **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Use Integer.MAX\_VALUE / MIN\_VALUE as sentinels for min/max searches and as bounds in overflow checks instead of typing digits; when values can approach the limits, switch to long rather than relying on the int constants.
  - **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: int arithmetic stays within Integer.MIN\_VALUE..Integer.MAX\_VALUE by wrapping, without error. Kind: silent logic error. Trigger class: Any int computation whose true result exceeds Integer.MAX\_VALUE or is below Integer.MIN\_VALUE: sums/products of large values, MAX\_VALUE + 1, -Integer.MIN\_VALUE, Math.abs(Integer.MIN\_VALUE).

**10. `topic1.2.c` &rarr; `integer_constants`** (contains)

- topic `topic1.2.c` contains `integer_constants`

**11. `topic1.2.c` &rarr; `arithmetic_operators`** (contains)

- topic `topic1.2.c` contains `arithmetic_operators`

**12. `topic1.2.c` &rarr; `int`** (contains)

- topic `topic1.2.c` contains `int`

**13. `topic1.2.c` &rarr; `int_literal_limit`** (contains)

- topic `topic1.2.c` contains `int_literal_limit`

**14. `topic1.2.c` &rarr; `integer_division`** (contains)

- topic `topic1.2.c` contains `integer_division`

**15. `topic1.2.c` &rarr; `long_type`** (contains)

- topic `topic1.2.c` contains `long_type`

**16. `topic1.2.c` &rarr; `overflow`** (contains)

- topic `topic1.2.c` contains `overflow`

**17. `topic1.2.c` &rarr; `remainder_operator`** (contains)

- topic `topic1.2.c` contains `remainder_operator`
