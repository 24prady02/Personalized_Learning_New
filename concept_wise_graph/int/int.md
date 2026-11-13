# int (`int`)

32-bit integer primitive

Section 1.2 Built-in Types of Data, topic 1.2.c Integers.

![The knowledge graph around int](int.png)

## At a glance

- **Needs first:** `primitive_type`
- **Leads to:** `int_literal_limit`, `long_type`, `overflow`
- **Learned alongside:** `boolean`, `char`, `double`
- **Misconceptions:** `IntOverflowWidensAutomatically`, `IntegerDivisionGivesFraction`
- **Errors:** none
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 24 edges around this concept. The edge logic, the wrong and right rules and the exact rules of the ways are copied word for word from the graph.

## To work on (0)

Nothing is missing for this concept.

## What it needs first (1)

A prerequisite edge means the other concept has to be understood before `int`.

### `primitive_type` comes before `int`

*int, double, boolean, char*

- **Edge:** `pre:primitive_type->int`
- **Exact edge logic:** int is one of the eight primitive types, the one used for integers.
- **Grounding:** book\_passage
- **Composition rule (R) of `int` with `primitive_type`:** int is the 32-bit integral primitive type, and the default type for integer literals and arithmetic.
- **Composition rule (R) of `primitive_type` with `int`:** int is the 32-bit signed integral primitive. Arithmetic on byte, short and char is also carried out in int.

## What it leads to (3)

These concepts need `int` first.

### `int` comes before `int_literal_limit`

*2147483648 is legal only as -2147483648*

- **Edge:** `pre:int->int_literal_limit`
- **Exact edge logic:** The limit on int literals is int's 32-bit range, -2147483648 to 2147483647.
- **Grounding:** book\_passage
- **Composition rule (R) of `int` with `int_literal_limit`:** An int literal must lie in int's range, so larger digit strings need an L (long) literal.
- **Composition rule (R) of `int_literal_limit` with `int`:** The literal limit is exactly int's 32-bit range, but it is checked only for literals: the literal 2147483648 is a compile-time error, whereas the expression 2147483647 + 1 compiles and overflows at run time to -2147483648.

### `int` comes before `long_type`

*64-bit integer type for values beyond the int range*

- **Edge:** `pre:int->long_type`
- **Exact edge logic:** long is the wider integer type used when int's range is too small.
- **Grounding:** book\_passage
- **Composition rule (R) of `int` with `long_type`:** If either operand is long, the operation is 64-bit and the result is long. Storing a long into an int needs a cast.
- **Composition rule (R) of `long_type` with `int`:** long is the wider integer type: an int widens to long automatically, and mixing an int with a long in an operation gives a long.

### `int` comes before `overflow`

*int arithmetic wraps around outside the 32-bit range*

- **Edge:** `pre:int->overflow`
- **Exact edge logic:** Overflow happens because an int has a fixed 32-bit range.
- **Grounding:** book\_passage
- **Composition rule (R) of `int` with `overflow`:** Because int has a fixed 32-bit range, results outside it wrap around silently.
- **Composition rule (R) of `overflow` with `int`:** Overflow is possible because int has a fixed 32-bit range, -2^31 to 2^31 - 1.

## Learned alongside (3)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

### `int` alongside `boolean`

*true/false primitive*

- **Edge:** `par:int~boolean`
- **Exact edge logic:** An int holds an integer and is a numeric type for computing with numbers; a boolean holds only true or false and is used for computing with logical values.
- **Grounding:** book\_passage
- **Composition rule (R) of `int` with `boolean`:** int and boolean do not convert into each other. Comparing ints gives a boolean (x &gt; 0), and an int cannot itself be used as a condition.
- **Composition rule (R) of `boolean` with `int`:** int and boolean never convert into each other; an int becomes a boolean only through a comparison (year % 4 == 0), and an int condition such as if (n) does not compile.

### `int` alongside `char`

*16-bit character primitive*

- **Edge:** `par:int~char`
- **Exact edge logic:** An int holds a whole number; a char holds one character, which Java stores as its numeric code.
- **Grounding:** book\_passage
- **Composition rule (R) of `int` with `char`:** In arithmetic a char is promoted to its int code. An int becomes a char only through a cast.
- **Composition rule (R) of `char` with `int`:** A char is stored as an unsigned 16-bit code, so in arithmetic it acts as an int ('a' + 1 is 98). Going from int to char needs a cast.

### `int` alongside `double`

*64-bit floating-point primitive*

- **Edge:** `par:int~double`
- **Exact edge logic:** With two ints, a / b drops the fractional part; if either a or b is a double, a / b keeps the fractional part.
- **Grounding:** book\_passage
- **Composition rule (R) of `int` with `double`:** int op double promotes the int and gives a double. A double becomes an int only through a cast, which truncates toward zero.
- **Composition rule (R) of `double` with `int`:** Type flow decides the division: with two int operands a / b discards the fraction (10/3 is 3, and double d = 10/3; stores 3.0); if either operand is double the other is promoted and the fraction is kept (10/3.0 is 3.3333333333333335).

## Misconceptions (2)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### IntOverflowWidensAutomatically

- **Edge:** `int` &rarr; `IntOverflowWidensAutomatically` (misconception)
- **Exact edge logic (the wrong rule):** An int result that is too large is automatically stored as a bigger number.
- **Twin logic (the right rule):** int arithmetic is 32-bit; a result outside the range wraps around.
- **Wrong belief (on the node):** An int result that is too large is automatically stored as a bigger number.
- **Correct rule (on the node):** int arithmetic is 32-bit; a result outside the range wraps around.
- **Provenance:** textbook
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [2] misconception, exact rule:** wrong rule: An int result that is too large is automatically stored as a bigger number. Right rule: int arithmetic is 32-bit; a result outside the range wraps around.
- **Edge `overflow` &rarr; `IntOverflowWidensAutomatically`, exact edge logic:** An int result that is too large is automatically stored as a bigger number. **Twin logic:** int arithmetic is 32-bit; a result outside the range wraps around. (role: primary)

### IntegerDivisionGivesFraction

- **Edge:** `int` &rarr; `IntegerDivisionGivesFraction` (misconception)
- **Exact edge logic (the wrong rule):** 10 / 3 evaluates to 3.333....
- **Twin logic (the right rule):** Dividing two ints gives an int: the fractional part is discarded.
- **Wrong belief (on the node):** 10 / 3 evaluates to 3.333....
- **Correct rule (on the node):** Dividing two ints gives an int: the fractional part is discarded.
- **Provenance:** textbook
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [1] misconception, exact rule:** wrong rule: 10 / 3 evaluates to 3.333. Right rule: Dividing two ints gives an int: the fractional part is discarded.
- **L0 way [3] inconsistent\_trace, exact rule:** Points to LT (each int operation is done immediately in 32-bit integer arithmetic). Applied unevenly, a student truncates 10 / 3 to 3 in one step but computes 10 / 3 \* 3 as 10, or wraps on one overflow but not another. (here mixing in: "10 / 3 evaluates to 3.333")
- **Edge `integer_division` &rarr; `IntegerDivisionGivesFraction`, exact edge logic:** 10 / 3 evaluates to 3.333.... **Twin logic:** Dividing two ints gives an int: the fractional part is discarded. (role: primary)

## Errors (0)

An error edge states the rule that gets broken in a program, and the right rule.

The graph has no error edge from this concept.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for int: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to int agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

- **Edge:** `int` &rarr; `int@L0` (has_level)
- **Exact edge logic:** int -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (4 ways).

Ways (4), each with its exact rule:

- **[0] everyday\_reading** (rule type E, folk-meaning rule): In maths integers are unbounded, and dividing two integers can give a fraction (10 / 3 = 3.33...). A Java int has a fixed 32-bit range, its / discards the fraction, and results outside the range wrap around.
- **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `IntegerDivisionGivesFraction`: wrong rule: 10 / 3 evaluates to 3.333. Right rule: Dividing two ints gives an int: the fractional part is discarded.
- **[2] misconception** (rule type M, wrong rule / right rule) &rarr; `IntOverflowWidensAutomatically`: wrong rule: An int result that is too large is automatically stored as a bigger number. Right rule: int arithmetic is 32-bit; a result outside the range wraps around.
- **[3] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `IntegerDivisionGivesFraction`: Points to LT (each int operation is done immediately in 32-bit integer arithmetic). Applied unevenly, a student truncates 10 / 3 to 3 in one step but computes 10 / 3 \* 3 as 10, or wraps on one overflow but not another. (here mixing in: "10 / 3 evaluates to 3.333")

### L1: Unistructural / atom x text surface

L1 for int: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

- **Edge:** `int` &rarr; `int@L1` (has_level)
- **Exact edge logic:** int -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

Ways (2), each with its exact rule:

- **[0] names\_the\_element** (rule type N, identity rule): int: Java's 32-bit signed integer primitive type.
- **[1] states\_the\_rule** (rule type S, declarative rule): int values run from -2147483648 to 2147483647. + - \* / % take two ints and produce an int. / discards the fraction, and division or remainder by zero is not allowed.

### L2: Multistructural / block x execution / preoperational

L2 for int: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

- **Edge:** `int` &rarr; `int@L2` (has_level)
- **Exact edge logic:** int -&gt; L2 (Multistructural): the answer applies the rules of int to every part of the code, in order (3 ways).

Ways (3), each with its exact rule:

- **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): An int expression evaluates its operands left to right and applies \* / % before + -. Each operation is done at once in 32-bit precision, so every intermediate result is already truncated or wrapped.
- **[1] output\_prediction** (rule type OP, evaluation / result rule): The result is an int: 5 + 3 is 8, 5 / 3 is 1, 5 % 3 is 2, 3 \* 5 - 2 is 13, and 1 / 0 is a run-time error.
- **[2] one\_step\_execution** (rule type OS, state-transition rule): An assignment like n = n + 1 changes n by exactly 1, with no rounding. A result outside the range is stored wrapped around.

### L3: Relational / relations x function (concrete operational begins)

L3 for int: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

- **Edge:** `int` &rarr; `int@L3` (has_level)
- **Exact edge logic:** int -&gt; L3 (Relational): the answer relates the parts (8 ways).

Ways (8), each with its exact rule:

- **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): int op double promotes the int and gives a double. A double becomes an int only through a cast, which truncates toward zero.
- **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): int and boolean do not convert into each other. Comparing ints gives a boolean (x &gt; 0), and an int cannot itself be used as a condition.
- **[2] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): In arithmetic a char is promoted to its int code. An int becomes a char only through a cast.
- **[3] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Because int has a fixed 32-bit range, results outside it wrap around silently.
- **[4] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): If either operand is long, the operation is 64-bit and the result is long. Storing a long into an int needs a cast.
- **[5] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): An int literal must lie in int's range, so larger digit strings need an L (long) literal.
- **[6] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): int is the 32-bit integral primitive type, and the default type for integer literals and arithmetic.
- **[7] purpose\_of\_the\_whole** (rule type P, plan / role rule): int is used for counting and indexing: counters, loop steppers, array indices, sizes, and exact whole quantities (cents).

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for int: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

- **Edge:** `int` &rarr; `int@L4` (has_level)
- **Exact edge logic:** int -&gt; L4 (Extended abstract): the answer reasons beyond the given code (5 ways).

Ways (5), each with its exact rule:

- **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `IntegerDivisionGivesFraction`: Changing a variable from int to double changes / from truncating to fractional, and output from 3 to 3.0. Multiplying before dividing keeps precision (59 \* 100 / 60 is 98, but 59 / 60 \* 100 is 0).
- **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Use int for whole quantities that stay under about 2 billion (counts, indices, cents). Use long beyond that, BigInteger when values are unbounded, and double for measurements or fractions.
- **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: int division and remainder by zero are undefined. Kind: run-time exception. Trigger class: Any int / or % whose divisor evaluates to 0: ArithmeticException: / by zero.
- **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: int results are only 32 bits and overflow is not reported. Kind: silent logic error. Trigger class: Results beyond about plus or minus 2.1 billion (big products, factorials above 12!, sums of large values): a wrapped, often negative, value.
- **[4] diagnose\_an\_error** (rule type D, error rule): rule broken: A double cannot be stored in an int without a cast. Kind: compile-time. Trigger class: int x = 1.1; or int avg = sum / 2.0;: 'possible lossy conversion from double to int'.

## Same topic

`int` belongs to the topic **Integers** (`topic1.2.c`). The topic also contains: `arithmetic_operators`, `int_literal_limit`, `integer_constants`, `integer_division`, `long_type`, `overflow`, `remainder_operator`.

## Rules of the concept (22)

- **Book** (SW-1e, p. 21 (pdf 31)): "An int is an integer (natural number) between -2147483648"
- **Book** (OT-Datatypes, ): "By default, the int data type is a 32-bit signed two's complement integer"
- **Book** (SW-1.2, ): "An int is an integer (whole number) between -2^31 and 2^31 - 1."
- **E** (folk-meaning rule): In maths integers are unbounded, and dividing two integers can give a fraction (10 / 3 = 3.33...). A Java int has a fixed 32-bit range, its / discards the fraction, and results outside the range wrap around.
- **M** (wrong rule / right rule): IntOverflowWidensAutomatically: wrong: An int result that is too large is automatically stored as a bigger number. \| right: int arithmetic is 32-bit; a result outside the range wraps around.
- **M** (wrong rule / right rule): IntegerDivisionGivesFraction: wrong: 10 / 3 evaluates to 3.333.... \| right: Dividing two ints gives an int: the fractional part is discarded.
- **T** (uneven-application rule): Points to LT (each int operation is done immediately in 32-bit integer arithmetic). Applied unevenly, a student truncates 10 / 3 to 3 in one step but computes 10 / 3 \* 3 as 10, or wraps on one overflow but not another.
- **N** (identity rule): int: Java's 32-bit signed integer primitive type.
- **S** (declarative rule): int values run from -2147483648 to 2147483647. + - \* / % take two ints and produce an int. / discards the fraction, and division or remainder by zero is not allowed.
- **LT** (operational sequencing rule): An int expression evaluates its operands left to right and applies \* / % before + -. Each operation is done at once in 32-bit precision, so every intermediate result is already truncated or wrapped.
- **OP** (evaluation / result rule): The result is an int: 5 + 3 is 8, 5 / 3 is 1, 5 % 3 is 2, 3 \* 5 - 2 is 13, and 1 / 0 is a run-time error.
- **OS** (state-transition rule): An assignment like n = n + 1 changes n by exactly 1, with no rounding. A result outside the range is stored wrapped around.
- **R** (composition rule (with a neighbour)): with double: int op double promotes the int and gives a double. A double becomes an int only through a cast, which truncates toward zero.
- **R** (composition rule (with a neighbour)): with boolean: int and boolean do not convert into each other. Comparing ints gives a boolean (x &gt; 0), and an int cannot itself be used as a condition.
- **R** (composition rule (with a neighbour)): with char: In arithmetic a char is promoted to its int code. An int becomes a char only through a cast.
- **R** (composition rule (with a neighbour)): with overflow: Because int has a fixed 32-bit range, results outside it wrap around silently.
- **R** (composition rule (with a neighbour)): with long\_type: If either operand is long, the operation is 64-bit and the result is long. Storing a long into an int needs a cast.
- **R** (composition rule (with a neighbour)): with int\_literal\_limit: An int literal must lie in int's range, so larger digit strings need an L (long) literal.
- **R** (composition rule (with a neighbour)): with primitive\_type: int is the 32-bit integral primitive type, and the default type for integer literals and arithmetic.
- **P** (plan / role rule): int is used for counting and indexing: counters, loop steppers, array indices, sizes, and exact whole quantities (cents).
- **C** (conservation rule): Changing a variable from int to double changes / from truncating to fractional, and output from 3 to 3.0. Multiplying before dividing keeps precision (59 \* 100 / 60 is 98, but 59 / 60 \* 100 is 0).
- **D** (error rule): rule broken: int division and remainder by zero are undefined. (run-time exception)
- **D** (error rule): rule broken: int results are only 32 bits and overflow is not reported. (silent logic error)
- **D** (error rule): rule broken: A double cannot be stored in an int without a cast. (compile-time)
- **X** (applicability rule): Use int for whole quantities that stay under about 2 billion (counts, indices, cents). Use long beyond that, BigInteger when values are unbounded, and double for measurements or fractions.

## How it is found in code and answers (reader block)

- **Aliases:** int, integer, integers, ints
- **Code patterns:** `\bint\b`
- **Operator symbols:** none
- **Java types:** `int`

## The whole prerequisite chain

- **Everything it builds on (2):** `data_type`, `primitive_type`
- **Everything that builds on it (4):** `int_literal_limit`, `integer_constants`, `long_type`, `overflow`

## Every edge in this view and its exact edge logic (24)

All the edges drawn in the picture, in the order: prerequisite, parallel, misconception, error, has_level, contains.

**1. `int` &rarr; `int_literal_limit`** (prerequisite)

- **Exact edge logic:** The limit on int literals is int's 32-bit range, -2147483648 to 2147483647.
- **Grounding:** book\_passage
- **Composition rule (R) of `int` with `int_literal_limit`:** An int literal must lie in int's range, so larger digit strings need an L (long) literal.
- **Composition rule (R) of `int_literal_limit` with `int`:** The literal limit is exactly int's 32-bit range, but it is checked only for literals: the literal 2147483648 is a compile-time error, whereas the expression 2147483647 + 1 compiles and overflows at run time to -2147483648.

**2. `int` &rarr; `long_type`** (prerequisite)

- **Exact edge logic:** long is the wider integer type used when int's range is too small.
- **Grounding:** book\_passage
- **Composition rule (R) of `int` with `long_type`:** If either operand is long, the operation is 64-bit and the result is long. Storing a long into an int needs a cast.
- **Composition rule (R) of `long_type` with `int`:** long is the wider integer type: an int widens to long automatically, and mixing an int with a long in an operation gives a long.

**3. `int` &rarr; `overflow`** (prerequisite)

- **Exact edge logic:** Overflow happens because an int has a fixed 32-bit range.
- **Grounding:** book\_passage
- **Composition rule (R) of `int` with `overflow`:** Because int has a fixed 32-bit range, results outside it wrap around silently.
- **Composition rule (R) of `overflow` with `int`:** Overflow is possible because int has a fixed 32-bit range, -2^31 to 2^31 - 1.

**4. `primitive_type` &rarr; `int`** (prerequisite)

- **Exact edge logic:** int is one of the eight primitive types, the one used for integers.
- **Grounding:** book\_passage
- **Composition rule (R) of `primitive_type` with `int`:** int is the 32-bit signed integral primitive. Arithmetic on byte, short and char is also carried out in int.
- **Composition rule (R) of `int` with `primitive_type`:** int is the 32-bit integral primitive type, and the default type for integer literals and arithmetic.

**5. `int` &harr; `boolean`** (parallel)

- **Exact edge logic:** An int holds an integer and is a numeric type for computing with numbers; a boolean holds only true or false and is used for computing with logical values.
- **Grounding:** book\_passage
- **Composition rule (R) of `int` with `boolean`:** int and boolean do not convert into each other. Comparing ints gives a boolean (x &gt; 0), and an int cannot itself be used as a condition.
- **Composition rule (R) of `boolean` with `int`:** int and boolean never convert into each other; an int becomes a boolean only through a comparison (year % 4 == 0), and an int condition such as if (n) does not compile.

**6. `int` &harr; `char`** (parallel)

- **Exact edge logic:** An int holds a whole number; a char holds one character, which Java stores as its numeric code.
- **Grounding:** book\_passage
- **Composition rule (R) of `int` with `char`:** In arithmetic a char is promoted to its int code. An int becomes a char only through a cast.
- **Composition rule (R) of `char` with `int`:** A char is stored as an unsigned 16-bit code, so in arithmetic it acts as an int ('a' + 1 is 98). Going from int to char needs a cast.

**7. `int` &harr; `double`** (parallel)

- **Exact edge logic:** With two ints, a / b drops the fractional part; if either a or b is a double, a / b keeps the fractional part.
- **Grounding:** book\_passage
- **Composition rule (R) of `int` with `double`:** int op double promotes the int and gives a double. A double becomes an int only through a cast, which truncates toward zero.
- **Composition rule (R) of `double` with `int`:** Type flow decides the division: with two int operands a / b discards the fraction (10/3 is 3, and double d = 10/3; stores 3.0); if either operand is double the other is promoted and the fraction is kept (10/3.0 is 3.3333333333333335).

**8. `int` &rarr; `IntOverflowWidensAutomatically`** (misconception)

- **Exact edge logic (the wrong rule):** An int result that is too large is automatically stored as a bigger number.
- **Twin logic (the right rule):** int arithmetic is 32-bit; a result outside the range wraps around.
- **Role:** context

**9. `int` &rarr; `IntegerDivisionGivesFraction`** (misconception)

- **Exact edge logic (the wrong rule):** 10 / 3 evaluates to 3.333....
- **Twin logic (the right rule):** Dividing two ints gives an int: the fractional part is discarded.
- **Role:** context

**10. `integer_division` &rarr; `IntegerDivisionGivesFraction`** (misconception)

- **Exact edge logic (the wrong rule):** 10 / 3 evaluates to 3.333....
- **Twin logic (the right rule):** Dividing two ints gives an int: the fractional part is discarded.
- **Role:** primary

**11. `overflow` &rarr; `IntOverflowWidensAutomatically`** (misconception)

- **Exact edge logic (the wrong rule):** An int result that is too large is automatically stored as a bigger number.
- **Twin logic (the right rule):** int arithmetic is 32-bit; a result outside the range wraps around.
- **Role:** primary

**12. `int` &rarr; `int@L0`** (has_level)

- **Exact edge logic:** int -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (4 ways).
  - **[0] everyday\_reading** (rule type E, folk-meaning rule): In maths integers are unbounded, and dividing two integers can give a fraction (10 / 3 = 3.33...). A Java int has a fixed 32-bit range, its / discards the fraction, and results outside the range wrap around.
  - **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `IntegerDivisionGivesFraction`: wrong rule: 10 / 3 evaluates to 3.333. Right rule: Dividing two ints gives an int: the fractional part is discarded.
  - **[2] misconception** (rule type M, wrong rule / right rule) &rarr; `IntOverflowWidensAutomatically`: wrong rule: An int result that is too large is automatically stored as a bigger number. Right rule: int arithmetic is 32-bit; a result outside the range wraps around.
  - **[3] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `IntegerDivisionGivesFraction`: Points to LT (each int operation is done immediately in 32-bit integer arithmetic). Applied unevenly, a student truncates 10 / 3 to 3 in one step but computes 10 / 3 \* 3 as 10, or wraps on one overflow but not another. (here mixing in: "10 / 3 evaluates to 3.333")

**13. `int` &rarr; `int@L1`** (has_level)

- **Exact edge logic:** int -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).
  - **[0] names\_the\_element** (rule type N, identity rule): int: Java's 32-bit signed integer primitive type.
  - **[1] states\_the\_rule** (rule type S, declarative rule): int values run from -2147483648 to 2147483647. + - \* / % take two ints and produce an int. / discards the fraction, and division or remainder by zero is not allowed.

**14. `int` &rarr; `int@L2`** (has_level)

- **Exact edge logic:** int -&gt; L2 (Multistructural): the answer applies the rules of int to every part of the code, in order (3 ways).
  - **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): An int expression evaluates its operands left to right and applies \* / % before + -. Each operation is done at once in 32-bit precision, so every intermediate result is already truncated or wrapped.
  - **[1] output\_prediction** (rule type OP, evaluation / result rule): The result is an int: 5 + 3 is 8, 5 / 3 is 1, 5 % 3 is 2, 3 \* 5 - 2 is 13, and 1 / 0 is a run-time error.
  - **[2] one\_step\_execution** (rule type OS, state-transition rule): An assignment like n = n + 1 changes n by exactly 1, with no rounding. A result outside the range is stored wrapped around.

**15. `int` &rarr; `int@L3`** (has_level)

- **Exact edge logic:** int -&gt; L3 (Relational): the answer relates the parts (8 ways).
  - **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): int op double promotes the int and gives a double. A double becomes an int only through a cast, which truncates toward zero.
  - **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): int and boolean do not convert into each other. Comparing ints gives a boolean (x &gt; 0), and an int cannot itself be used as a condition.
  - **[2] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): In arithmetic a char is promoted to its int code. An int becomes a char only through a cast.
  - **[3] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Because int has a fixed 32-bit range, results outside it wrap around silently.
  - **[4] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): If either operand is long, the operation is 64-bit and the result is long. Storing a long into an int needs a cast.
  - **[5] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): An int literal must lie in int's range, so larger digit strings need an L (long) literal.
  - **[6] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): int is the 32-bit integral primitive type, and the default type for integer literals and arithmetic.
  - **[7] purpose\_of\_the\_whole** (rule type P, plan / role rule): int is used for counting and indexing: counters, loop steppers, array indices, sizes, and exact whole quantities (cents).

**16. `int` &rarr; `int@L4`** (has_level)

- **Exact edge logic:** int -&gt; L4 (Extended abstract): the answer reasons beyond the given code (5 ways).
  - **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `IntegerDivisionGivesFraction`: Changing a variable from int to double changes / from truncating to fractional, and output from 3 to 3.0. Multiplying before dividing keeps precision (59 \* 100 / 60 is 98, but 59 / 60 \* 100 is 0).
  - **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Use int for whole quantities that stay under about 2 billion (counts, indices, cents). Use long beyond that, BigInteger when values are unbounded, and double for measurements or fractions.
  - **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: int division and remainder by zero are undefined. Kind: run-time exception. Trigger class: Any int / or % whose divisor evaluates to 0: ArithmeticException: / by zero.
  - **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: int results are only 32 bits and overflow is not reported. Kind: silent logic error. Trigger class: Results beyond about plus or minus 2.1 billion (big products, factorials above 12!, sums of large values): a wrapped, often negative, value.
  - **[4] diagnose\_an\_error** (rule type D, error rule): rule broken: A double cannot be stored in an int without a cast. Kind: compile-time. Trigger class: int x = 1.1; or int avg = sum / 2.0;: 'possible lossy conversion from double to int'.

**17. `topic1.2.c` &rarr; `int`** (contains)

- topic `topic1.2.c` contains `int`

**18. `topic1.2.c` &rarr; `arithmetic_operators`** (contains)

- topic `topic1.2.c` contains `arithmetic_operators`

**19. `topic1.2.c` &rarr; `int_literal_limit`** (contains)

- topic `topic1.2.c` contains `int_literal_limit`

**20. `topic1.2.c` &rarr; `integer_constants`** (contains)

- topic `topic1.2.c` contains `integer_constants`

**21. `topic1.2.c` &rarr; `integer_division`** (contains)

- topic `topic1.2.c` contains `integer_division`

**22. `topic1.2.c` &rarr; `long_type`** (contains)

- topic `topic1.2.c` contains `long_type`

**23. `topic1.2.c` &rarr; `overflow`** (contains)

- topic `topic1.2.c` contains `overflow`

**24. `topic1.2.c` &rarr; `remainder_operator`** (contains)

- topic `topic1.2.c` contains `remainder_operator`
