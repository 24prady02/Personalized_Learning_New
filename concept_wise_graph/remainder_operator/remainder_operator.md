# remainder_operator (`remainder_operator`)

% gives the remainder of integer division

Section 1.2 Built-in Types of Data, topic 1.2.c Integers.

![The knowledge graph around remainder_operator](remainder_operator.png)

## At a glance

- **Needs first:** `arithmetic_operators`, `integer_division`
- **Leads to:** nothing
- **Learned alongside:** nothing
- **Misconceptions:** `NegativeRemainderSign`, `RemainderIsQuotient`, `RemainderIsSubtraction`
- **Errors:** none
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 20 edges around this concept, each explained in the graph's own words.

## What it needs first (2)

A prerequisite edge means the other concept has to be understood before `remainder_operator`.

### `arithmetic_operators` comes before `remainder_operator`

*+ - \* / %*

% is one of the int arithmetic operators; it gives the remainder of the division.

- **Grounding:** book passage

### `integer_division` comes before `remainder_operator`

*/ on two ints truncates; % is the remainder*

% is the companion of integer division: a = (a / b) \* b + a % b.

- **Grounding:** book passage
- **How `remainder_operator` combines with `integer_division`:** % is the companion of integer division, since a == (a / b) \* b + a % b. Both use the same quotient rounded toward 0.
- **How `integer_division` combines with `remainder_operator`:** % gives the remainder of the same truncating division: (a / b) \* b + a % b == a.

## What it leads to (0)

These concepts need `remainder_operator` first.

No concept has this one as a prerequisite.

## Learned alongside (0)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

No parallel edge touches this concept.

## Misconceptions (3)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### NegativeRemainderSign

- **Wrong rule:** a % b is never negative, and integer division of a negative number rounds down.
- **Right rule:** a / b rounds toward 0 and a % b takes the sign of a: -14 / 3 is -4 and -14 % 3 is -2.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: a % b is never negative, and integer division of a negative number rounds down. Right rule: a / b rounds toward 0 and a % b takes the sign of a: -14 / 3 is -4 and -14 % 3 is -2.
- **Also an edge from `integer_division`:** a % b is never negative, and integer division of a negative number rounds down.

### RemainderIsQuotient

- **Wrong rule:** 17 % 5 is 3 (the quotient).
- **Right rule:** % returns the remainder, so 17 % 5 is 2.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: 17 % 5 is 3 (the quotient). Right rule: % returns the remainder, so 17 % 5 is 2.
- **Shows at level L0 as:** inconsistent trace: Points to LT (compute the truncated quotient, then the remainder). Applied unevenly, a student gives the remainder for positive operands but the mathematical mod for negatives, or swaps quotient and remainder (17 % 5 as 3). (here mixing in: "17 % 5 is 3 (the quotient)")

### RemainderIsSubtraction

- **Wrong rule:** 9 % 5 means 9 minus 5 (a % b subtracts b from a).
- **Right rule:** % gives the remainder after integer division: 9 % 5 is 4 because 9 = 1 \* 5 + 4, and 17 % 5 is 2, not 12.
- **Role of this concept:** primary
- **Also an edge from `arithmetic_operators`:** 9 % 5 means 9 minus 5 (a % b subtracts b from a).

## Errors (0)

An error edge states the rule that gets broken in a program, and the right rule.

The graph has no error edge from this concept.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for remainder operator: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to remainder operator agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

remainder operator -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (4 ways).

- **everyday reading** (folk-meaning rule): In everyday use % means percent (50% of x), and in maths 'mod' always gives a non-negative result. In Java % is the remainder of truncating division, and its sign follows the left operand (-14 % 3 is -2).
- **misconception** (wrong rule / right rule; shows `RemainderIsQuotient`): wrong rule: 17 % 5 is 3 (the quotient). Right rule: % returns the remainder, so 17 % 5 is 2.
- **misconception** (wrong rule / right rule; shows `NegativeRemainderSign`): wrong rule: a % b is never negative, and integer division of a negative number rounds down. Right rule: a / b rounds toward 0 and a % b takes the sign of a: -14 / 3 is -4 and -14 % 3 is -2.
- **inconsistent trace** (uneven-application rule; shows `RemainderIsQuotient`): Points to LT (compute the truncated quotient, then the remainder). Applied unevenly, a student gives the remainder for positive operands but the mathematical mod for negatives, or swaps quotient and remainder (17 % 5 as 3). (here mixing in: "17 % 5 is 3 (the quotient)")

### L1: Unistructural / atom x text surface

L1 for remainder operator: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

remainder operator -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

- **names the element** (identity rule): Remainder operator %: the binary operator that gives the remainder after dividing a by b.
- **states the rule** (declarative rule): For ints, a % b is defined so that (a / b) \* b + a % b equals a. The result takes the sign of a, % by zero throws ArithmeticException, and % also works on doubles.

### L2: Multistructural / block x execution / preoperational

L2 for remainder operator: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

remainder operator -&gt; L2 (Multistructural): the answer applies the rules of remainder operator to every part of the code, in order (3 ways).

- **line by line trace** (operational sequencing rule): Evaluate a, then b, take the quotient rounded toward 0, and give what is left over. % has the same precedence as \* and /, and they group left to right.
- **output prediction** (evaluation / result rule): 17 % 3 is 2, 76 % 12 is 4, 1234 % 99 is 46, -14 % 3 is -2, and 14 % -3 is 2.
- **one step execution** (state-transition rule): r = a % b stores a remainder smaller in size than b and leaves a and b unchanged. If b is 0, ArithmeticException is thrown before anything is stored.

### L3: Relational / relations x function (concrete operational begins)

L3 for remainder operator: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

remainder operator -&gt; L3 (Relational): the answer relates the parts (2 ways).

- **relation to neighbour** (composition rule (with a neighbour)): % is the companion of integer division, since a == (a / b) \* b + a % b. Both use the same quotient rounded toward 0.
- **purpose of the whole** (plan / role rule): Plans: divisibility and parity tests (x % 2 == 0), digit extraction (x % 10), cyclic wrap-around ((i + 1) % n), leap-year rules, and splitting units (76 % 12 inches).

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for remainder operator: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

remainder operator -&gt; L4 (Extended abstract): the answer reasons beyond the given code (5 ways).

- **predict a change** (conservation rule; shows `RemainderIsQuotient`): Negating a flips the remainder's sign, so n % 2 == 1 fails for negative odd n while n % 2 != 0 still works. Changing the divisor changes the cycle length. Swapping % with / swaps the remainder for the quotient.
- **transfer to a new program** (applicability rule): Use % for divisibility, parity, digits, cyclic indices and unit splitting. Do not use it for percentages (use \* / 100.0), and do not use it where a non-negative mathematical mod is needed for negative values (adjust the result or use Math.floorMod).
- **diagnose an error** (error rule): rule broken: int remainder by zero is undefined. Kind: run-time exception. Trigger class: x % 0, or a divisor variable that is 0: ArithmeticException: / by zero.
- **diagnose an error** (error rule): rule broken: The remainder takes the sign of the dividend. Kind: silent logic error. Trigger class: Negative inputs in an odd test written as x % 2 == 1, or in a wrap-around index computed as (i - 1) % n.
- **diagnose an error** (error rule): rule broken: % is the remainder, not a percentage. Kind: silent logic error. Trigger class: Writing price % 15 for 15 percent of price.

## Same topic

`remainder_operator` belongs to the topic **Integers** (`topic1.2.c`). The topic also contains: `arithmetic_operators`, `int`, `int_literal_limit`, `integer_constants`, `integer_division`, `long_type`, `overflow`.

## Rules of the concept (16)

- **folk-meaning rule:** In everyday use % means percent (50% of x), and in maths 'mod' always gives a non-negative result. In Java % is the remainder of truncating division, and its sign follows the left operand (-14 % 3 is -2).
- **wrong rule / right rule:** RemainderIsQuotient: wrong: 17 % 5 is 3 (the quotient). \| right: % returns the remainder, so 17 % 5 is 2.
- **wrong rule / right rule:** NegativeRemainderSign: wrong: a % b is never negative, and integer division of a negative number rounds down. \| right: a / b rounds toward 0 and a % b takes the sign of a: -14 / 3 is -4 and -14 % 3 is -2.
- **uneven-application rule:** Points to LT (compute the truncated quotient, then the remainder). Applied unevenly, a student gives the remainder for positive operands but the mathematical mod for negatives, or swaps quotient and remainder (17 % 5 as 3).
- **identity rule:** Remainder operator %: the binary operator that gives the remainder after dividing a by b.
- **declarative rule:** For ints, a % b is defined so that (a / b) \* b + a % b equals a. The result takes the sign of a, % by zero throws ArithmeticException, and % also works on doubles.
- **operational sequencing rule:** Evaluate a, then b, take the quotient rounded toward 0, and give what is left over. % has the same precedence as \* and /, and they group left to right.
- **evaluation / result rule:** 17 % 3 is 2, 76 % 12 is 4, 1234 % 99 is 46, -14 % 3 is -2, and 14 % -3 is 2.
- **state-transition rule:** r = a % b stores a remainder smaller in size than b and leaves a and b unchanged. If b is 0, ArithmeticException is thrown before anything is stored.
- **composition rule (with a neighbour):** with integer\_division: % is the companion of integer division, since a == (a / b) \* b + a % b. Both use the same quotient rounded toward 0.
- **plan / role rule:** Plans: divisibility and parity tests (x % 2 == 0), digit extraction (x % 10), cyclic wrap-around ((i + 1) % n), leap-year rules, and splitting units (76 % 12 inches).
- **conservation rule:** Negating a flips the remainder's sign, so n % 2 == 1 fails for negative odd n while n % 2 != 0 still works. Changing the divisor changes the cycle length. Swapping % with / swaps the remainder for the quotient.
- **error rule:** rule broken: int remainder by zero is undefined. (run-time exception)
- **error rule:** rule broken: The remainder takes the sign of the dividend. (silent logic error)
- **error rule:** rule broken: % is the remainder, not a percentage. (silent logic error)
- **applicability rule:** Use % for divisibility, parity, digits, cyclic indices and unit splitting. Do not use it for percentages (use \* / 100.0), and do not use it where a non-negative mathematical mod is needed for negative values (adjust the result or use Math.floorMod).

## The whole prerequisite chain

- **Everything it builds on (2):** `arithmetic_operators`, `integer_division`
- **Everything that builds on it (0):** nothing
