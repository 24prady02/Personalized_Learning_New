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

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 17 edges around this concept, each explained in the graph's own words.

## What it needs first (1)

A prerequisite edge means the other concept has to be understood before `integer_constants`.

### `overflow` comes before `integer_constants`

*int arithmetic wraps around outside the 32-bit range*

Integer.MAX\_VALUE is used to test for overflow: an int result that would go past it wraps around to a negative value.

- **Grounding:** book passage
- **How `integer_constants` combines with `overflow`:** Integer.MAX\_VALUE marks the overflow boundary: an int result past it wraps to a negative value, so a test such as sum &gt; Integer.MAX\_VALUE on an int is always false; an overflow guard must test before the operation (e.g. a &gt; Integer.MAX\_VALUE - b) or use long.
- **How `overflow` combines with `integer_constants`:** Integer.MAX\_VALUE and Integer.MIN\_VALUE mark the edges of the range. Testing a &gt; Integer.MAX\_VALUE - b before computing a + b avoids overflow.

## What it leads to (0)

These concepts need `integer_constants` first.

No concept has this one as a prerequisite.

## Learned alongside (0)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

No parallel edge touches this concept.

## Misconceptions (1)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### AbsAlwaysNonNegative

- **Wrong rule:** Math.abs always returns a non-negative number.
- **Right rule:** Math.abs(Integer.MIN\_VALUE) returns Integer.MIN\_VALUE, which is negative.
- **Role of this concept:** context
- **Also an edge from `math_library`:** Math.abs always returns a non-negative number.
- **Also an edge from `overflow`:** Math.abs always returns a non-negative number.

## Errors (0)

An error edge states the rule that gets broken in a program, and the right rule.

The graph has no error edge from this concept.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for integer constants: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to integer constants agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

integer constants -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (1 way).

- **everyday reading** (folk-meaning rule): Folk meaning: 'maximum' is a ceiling that nothing can pass (like a full tank, adding more leaves it full) and an absolute value is never negative. Java rule: int arithmetic wraps around silently, so Integer.MAX\_VALUE + 1 is Integer.MIN\_VALUE and Math.abs(Integer.MIN\_VALUE) is still -2147483648.

### L1: Unistructural / atom x text surface

L1 for integer constants: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

integer constants -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

- **names the element** (identity rule): Integer.MAX\_VALUE and Integer.MIN\_VALUE are named constants of the wrapper class Integer: the largest int, 2147483647 (2^31 - 1), and the smallest int, -2147483648 (-2^31).
- **states the rule** (declarative rule): Each wrapper class defines MIN\_VALUE and MAX\_VALUE; for int the range is -2147483648 to 2147483647 inclusive, and results outside it are truncated (wrap) without any error signal.

### L2: Multistructural / block x execution / preoperational

L2 for integer constants: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

integer constants -&gt; L2 (Multistructural): the answer applies the rules of integer constants to every part of the code, in order (3 ways).

- **line by line trace** (operational sequencing rule): The constant is read like a variable when its expression is evaluated; then operators are applied in precedence order, left operand first, each in 32-bit int arithmetic, wrapping at each step that leaves the range.
- **output prediction** (evaluation / result rule): Type int, value wrapped modulo 2^32: Integer.MAX\_VALUE + 1 is -2147483648, Integer.MIN\_VALUE - 1 is 2147483647, 2 \* Integer.MAX\_VALUE is -2, and Math.abs(Integer.MIN\_VALUE) is -2147483648.
- **one step execution** (state-transition rule): Reading the constant changes nothing (it is final); after int a = Integer.MAX\_VALUE; a = a + 1; the variable a holds Integer.MIN\_VALUE, and no exception is raised.

### L3: Relational / relations x function (concrete operational begins)

L3 for integer constants: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

integer constants -&gt; L3 (Relational): the answer relates the parts (2 ways).

- **relation to neighbour** (composition rule (with a neighbour)): Integer.MAX\_VALUE marks the overflow boundary: an int result past it wraps to a negative value, so a test such as sum &gt; Integer.MAX\_VALUE on an int is always false; an overflow guard must test before the operation (e.g. a &gt; Integer.MAX\_VALUE - b) or use long.
- **purpose of the whole** (plan / role rule): Used as the initial value of a most-wanted holder (Sajaniemi): max = Integer.MIN\_VALUE (or min = Integer.MAX\_VALUE) so the first real value always replaces it; also used as limits in overflow guards.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for integer constants: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

integer constants -&gt; L4 (Extended abstract): the answer reasons beyond the given code (3 ways).

- **predict a change** (conservation rule): Changing the type from int to long moves the wrap point from 2^31 to 2^63 but does not remove it; replacing the initial max = Integer.MIN\_VALUE by max = 0 breaks the search for all-negative inputs. Invariant: the range is asymmetric, Integer.MIN\_VALUE == -Integer.MAX\_VALUE - 1, so negating MIN\_VALUE gives MIN\_VALUE back.
- **transfer to a new program** (applicability rule): Use Integer.MAX\_VALUE / MIN\_VALUE as sentinels for min/max searches and as bounds in overflow checks instead of typing digits; when values can approach the limits, switch to long rather than relying on the int constants.
- **diagnose an error** (error rule): rule broken: int arithmetic stays within Integer.MIN\_VALUE..Integer.MAX\_VALUE by wrapping, without error. Kind: silent logic error. Trigger class: Any int computation whose true result exceeds Integer.MAX\_VALUE or is below Integer.MIN\_VALUE: sums/products of large values, MAX\_VALUE + 1, -Integer.MIN\_VALUE, Math.abs(Integer.MIN\_VALUE).

## Same topic

`integer_constants` belongs to the topic **Integers** (`topic1.2.c`). The topic also contains: `arithmetic_operators`, `int`, `int_literal_limit`, `integer_division`, `long_type`, `overflow`, `remainder_operator`.

## Rules of the concept (12)

- **folk-meaning rule:** Folk meaning: 'maximum' is a ceiling that nothing can pass (like a full tank, adding more leaves it full) and an absolute value is never negative. Java rule: int arithmetic wraps around silently, so Integer.MAX\_VALUE + 1 is Integer.MIN\_VALUE and Math.abs(Integer.MIN\_VALUE) is still -2147483648.
- **uneven-application rule:** Points to LT (each operator on an int is carried out in 32-bit arithmetic and wraps). Applied unevenly: in a trace of 1.2.10 the student wraps a+1 to a negative value but then treats 2\*a or 4\*a as ordinary mathematical products (or vice versa).
- **identity rule:** Integer.MAX\_VALUE and Integer.MIN\_VALUE are named constants of the wrapper class Integer: the largest int, 2147483647 (2^31 - 1), and the smallest int, -2147483648 (-2^31).
- **declarative rule:** Each wrapper class defines MIN\_VALUE and MAX\_VALUE; for int the range is -2147483648 to 2147483647 inclusive, and results outside it are truncated (wrap) without any error signal.
- **operational sequencing rule:** The constant is read like a variable when its expression is evaluated; then operators are applied in precedence order, left operand first, each in 32-bit int arithmetic, wrapping at each step that leaves the range.
- **evaluation / result rule:** Type int, value wrapped modulo 2^32: Integer.MAX\_VALUE + 1 is -2147483648, Integer.MIN\_VALUE - 1 is 2147483647, 2 \* Integer.MAX\_VALUE is -2, and Math.abs(Integer.MIN\_VALUE) is -2147483648.
- **state-transition rule:** Reading the constant changes nothing (it is final); after int a = Integer.MAX\_VALUE; a = a + 1; the variable a holds Integer.MIN\_VALUE, and no exception is raised.
- **composition rule (with a neighbour):** with overflow: Integer.MAX\_VALUE marks the overflow boundary: an int result past it wraps to a negative value, so a test such as sum &gt; Integer.MAX\_VALUE on an int is always false; an overflow guard must test before the operation (e.g. a &gt; Integer.MAX\_VALUE - b) or use long.
- **plan / role rule:** Used as the initial value of a most-wanted holder (Sajaniemi): max = Integer.MIN\_VALUE (or min = Integer.MAX\_VALUE) so the first real value always replaces it; also used as limits in overflow guards.
- **conservation rule:** Changing the type from int to long moves the wrap point from 2^31 to 2^63 but does not remove it; replacing the initial max = Integer.MIN\_VALUE by max = 0 breaks the search for all-negative inputs. Invariant: the range is asymmetric, Integer.MIN\_VALUE == -Integer.MAX\_VALUE - 1, so negating MIN\_VALUE gives MIN\_VALUE back.
- **error rule:** rule broken: int arithmetic stays within Integer.MIN\_VALUE..Integer.MAX\_VALUE by wrapping, without error. (silent logic error)
- **applicability rule:** Use Integer.MAX\_VALUE / MIN\_VALUE as sentinels for min/max searches and as bounds in overflow checks instead of typing digits; when values can approach the limits, switch to long rather than relying on the int constants.

## The whole prerequisite chain

- **Everything it builds on (4):** `data_type`, `int`, `overflow`, `primitive_type`
- **Everything that builds on it (0):** nothing
