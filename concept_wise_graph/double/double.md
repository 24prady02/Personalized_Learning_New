# double (`double`)

64-bit floating-point primitive

Section 1.2 Built-in Types of Data, topic 1.2.d Floating-point numbers.

![The knowledge graph around double](double.png)

## At a glance

- **Needs first:** `primitive_type`
- **Leads to:** `division_by_zero`, `floating_point_precision`
- **Learned alongside:** `boolean`, `char`, `int`
- **Misconceptions:** `FloatingPointIsExact`, `WholeNumberLiteralIsInt`
- **Errors:** none
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 20 edges around this concept. The edge logic, the wrong and right rules and the exact rules of the ways are copied word for word from the graph.

## To work on (0)

Nothing is missing for this concept.

## What it needs first (1)

A prerequisite edge means the other concept has to be understood before `double`.

### `primitive_type` comes before `double`

*int, double, boolean, char*

- **Edge:** `pre:primitive_type->double`
- **Exact edge logic:** double is one of the eight primitive types, the one used for real (floating-point) numbers.
- **Grounding:** book\_passage
- **Composition rule (R) of `double` with `primitive_type`:** double is one of the eight primitive types and the default type of decimal literals (float would need an f suffix and is not used in the book).
- **Composition rule (R) of `primitive_type` with `double`:** double is the 64-bit IEEE 754 primitive. Once a double meets an integral operand in a binary operator, the whole operation becomes floating point.

## What it leads to (2)

These concepts need `double` first.

### `double` comes before `division_by_zero`

*int division by zero throws; double division gives Infinity or NaN*

- **Edge:** `pre:double->division_by_zero`
- **Exact edge logic:** For doubles, 1.0/0.0 is legal and has the value Infinity; a double result can also be the special value NaN when the calculation is undefined.
- **Grounding:** book\_passage
- **Composition rule (R) of `double` with `division_by_zero`:** For double operands a zero divisor is not an error: 1.0/0.0 is Infinity, -1.0/0.0 is -Infinity and 0.0/0.0 is NaN, whereas int division by zero throws an exception.
- **Composition rule (R) of `division_by_zero` with `double`:** Once either operand is a double the division follows IEEE 754 rules instead, so the same zero divisor gives Infinity or NaN rather than an exception.

### `double` comes before `floating_point_precision`

*double values are approximations; == on doubles is unreliable*

- **Edge:** `pre:double->floating_point_precision`
- **Exact edge logic:** A double approximates real numbers, so its arithmetic is not exact.
- **Grounding:** book\_passage
- **Composition rule (R) of `double` with `floating_point_precision`:** Every double operation rounds its result to the nearest representable value, so double results carry rounding error that can accumulate; this is why == on computed doubles is unreliable.
- **Composition rule (R) of `floating_point_precision` with `double`:** Imprecision is inherent in the double type, not in a particular program: any arithmetic on doubles may carry rounding error, so code that uses double must be written to tolerate it.

## Learned alongside (3)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

### `double` alongside `boolean`

*true/false primitive*

- **Edge:** `par:double~boolean`
- **Exact edge logic:** A double holds a number with a fractional part; a boolean holds only true or false.
- **Grounding:** book\_passage
- **Composition rule (R) of `double` with `boolean`:** double and boolean never convert into each other (no cast is allowed either way); they meet only through comparisons, which take doubles and produce a boolean, e.g. (x &lt; 3.1).
- **Composition rule (R) of `boolean` with `double`:** A double reaches the boolean world only through a comparison such as (x &lt; 3.1), which yields a boolean; there is no cast between double and boolean.

### `double` alongside `char`

*16-bit character primitive*

- **Edge:** `par:double~char`
- **Exact edge logic:** A double holds a number with a fractional part; a char holds one character code, which is a whole number.
- **Grounding:** book\_passage
- **Composition rule (R) of `double` with `char`:** char is an integral numeric type, so a char widens automatically to double in arithmetic ('a' + 0.5 is 97.5), but a double needs an explicit cast to become a char.
- **Composition rule (R) of `char` with `double`:** A char widens automatically to double (its code), but a double needs a cast to become a char. A char never holds a fractional part.

### `double` alongside `int`

*32-bit integer primitive*

- **Edge:** `par:int~double`
- **Exact edge logic:** With two ints, a / b drops the fractional part; if either a or b is a double, a / b keeps the fractional part.
- **Grounding:** book\_passage
- **Composition rule (R) of `double` with `int`:** Type flow decides the division: with two int operands a / b discards the fraction (10/3 is 3, and double d = 10/3; stores 3.0); if either operand is double the other is promoted and the fraction is kept (10/3.0 is 3.3333333333333335).
- **Composition rule (R) of `int` with `double`:** int op double promotes the int and gives a double. A double becomes an int only through a cast, which truncates toward zero.

## Misconceptions (2)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### FloatingPointIsExact

- **Edge:** `double` &rarr; `FloatingPointIsExact` (misconception)
- **Exact edge logic (the wrong rule):** Math.sqrt(2) \* Math.sqrt(2) == 2 is true.
- **Twin logic (the right rule):** A double is an approximation, so the product is close to 2 but not equal to 2.
- **Wrong belief (on the node):** Math.sqrt(2) \* Math.sqrt(2) == 2 is true.
- **Correct rule (on the node):** A double is an approximation, so the product is close to 2 but not equal to 2.
- **Provenance:** textbook
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [1] misconception, exact rule:** wrong rule: Math.sqrt(2) \* Math.sqrt(2) == 2 is true. Right rule: A double is an approximation: Math.sqrt(2) \* Math.sqrt(2) is 2.0000000000000004, so the == test is false; compare doubles with a tolerance.
- **L0 way [3] inconsistent\_trace, exact rule:** Points to LT (at each operator the narrower operand is promoted, then the operation is done in double and rounded). Applied unevenly: the student promotes to double on one line but keeps integer division on another, e.g. treats 1/2 \* x as 0.5 \* x on one pass and as 0 on the next. (here mixing in: "Math.sqrt(2) \* Math.sqrt(2) == 2 is true")
- **Edge `convergence_test` &rarr; `FloatingPointIsExact`, exact edge logic:** Math.sqrt(2) \* Math.sqrt(2) == 2 is true. **Twin logic:** A double is an approximation, so the product is close to 2 but not equal to 2. (role: context)
- **Edge `floating_point_precision` &rarr; `FloatingPointIsExact`, exact edge logic:** Math.sqrt(2) \* Math.sqrt(2) == 2 is true. **Twin logic:** A double is an approximation, so the product is close to 2 but not equal to 2. (role: primary)

### WholeNumberLiteralIsInt

- **Edge:** `double` &rarr; `WholeNumberLiteralIsInt` (misconception)
- **Exact edge logic (the wrong rule):** 207. and 2.3e4 are int values because they are whole numbers.
- **Twin logic (the right rule):** A decimal point or scientific notation makes the literal a double.
- **Wrong belief (on the node):** 207. and 2.3e4 are int values because they are whole numbers.
- **Correct rule (on the node):** A decimal point or scientific notation makes the literal a double.
- **Provenance:** textbook
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [2] misconception, exact rule:** wrong rule: 207. and 2.3e4 are int values because they are whole numbers. Right rule: A decimal point or scientific notation makes the literal a double, whatever its value: 207. is 207.0 and 2.3e4 is 23000.0, so int n = 2.3e4; does not compile.
- **Edge `literal` &rarr; `WholeNumberLiteralIsInt`, exact edge logic:** 207. and 2.3e4 are int values because they are whole numbers. **Twin logic:** A decimal point or scientific notation makes the literal a double. (role: primary)

## Errors (0)

An error edge states the rule that gets broken in a program, and the right rule.

The graph has no error edge from this concept.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for double: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to double agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

- **Edge:** `double` &rarr; `double@L0` (has_level)
- **Exact edge logic:** double -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (4 ways).

Ways (4), each with its exact rule:

- **[0] everyday\_reading** (rule type E, folk-meaning rule): Folk meaning: a number with a decimal point is the exact real number of school maths, and a whole-looking number such as 207. or 2.3e4 is an integer. Java rule: a double is a 64-bit binary approximation from a finite set of values, and any literal with a decimal point or exponent is a double (207. is 207.0, 2.3e4 is 23000.0).
- **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `FloatingPointIsExact`: wrong rule: Math.sqrt(2) \* Math.sqrt(2) == 2 is true. Right rule: A double is an approximation: Math.sqrt(2) \* Math.sqrt(2) is 2.0000000000000004, so the == test is false; compare doubles with a tolerance.
- **[2] misconception** (rule type M, wrong rule / right rule) &rarr; `WholeNumberLiteralIsInt`: wrong rule: 207. and 2.3e4 are int values because they are whole numbers. Right rule: A decimal point or scientific notation makes the literal a double, whatever its value: 207. is 207.0 and 2.3e4 is 23000.0, so int n = 2.3e4; does not compile.
- **[3] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `FloatingPointIsExact`: Points to LT (at each operator the narrower operand is promoted, then the operation is done in double and rounded). Applied unevenly: the student promotes to double on one line but keeps integer division on another, e.g. treats 1/2 \* x as 0.5 \* x on one pass and as 0 on the next. (here mixing in: "Math.sqrt(2) \* Math.sqrt(2) == 2 is true")

### L1: Unistructural / atom x text surface

L1 for double: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

- **Edge:** `double` &rarr; `double@L1` (has_level)
- **Exact edge logic:** double -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

Ways (2), each with its exact rule:

- **[0] names\_the\_element** (rule type N, identity rule): double is a primitive data type: Java's 64-bit IEEE 754 floating-point type for representing real numbers.
- **[1] states\_the\_rule** (rule type S, declarative rule): Values are 64-bit IEEE 754 numbers (about 15 significant digits) plus the special values Infinity and NaN; +, -, \*, / (and %) are defined; if at least one operand of a binary arithmetic operator is double, the operation is a floating-point operation.

### L2: Multistructural / block x execution / preoperational

L2 for double: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

- **Edge:** `double` &rarr; `double@L2` (has_level)
- **Exact edge logic:** double -&gt; L2 (Multistructural): the answer applies the rules of double to every part of the code, in order (3 ways).

Ways (3), each with its exact rule:

- **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): Operators are applied in precedence order, left operand first; at each operator, if one operand is double the other is widened to double before the operation, and the result is rounded to the nearest double before the next operator uses it.
- **[1] output\_prediction** (rule type OP, evaluation / result rule): The result has type double: 5.0/3.0 is 1.6666666666666667, 10/3.0 is 3.3333333333333335, 1.0/0.0 is Infinity, Math.sqrt(-1.0) is NaN; println always shows a decimal part (3.0, not 3).
- **[2] one\_step\_execution** (rule type OS, state-transition rule): An assignment to a double variable stores the nearest representable value (x = x + 0.1 replaces x with the rounded sum); no double operation throws an exception, so the variable may end up holding Infinity or NaN.

### L3: Relational / relations x function (concrete operational begins)

L3 for double: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

- **Edge:** `double` &rarr; `double@L3` (has_level)
- **Exact edge logic:** double -&gt; L3 (Relational): the answer relates the parts (7 ways).

Ways (7), each with its exact rule:

- **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Type flow decides the division: with two int operands a / b discards the fraction (10/3 is 3, and double d = 10/3; stores 3.0); if either operand is double the other is promoted and the fraction is kept (10/3.0 is 3.3333333333333335).
- **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): double and boolean never convert into each other (no cast is allowed either way); they meet only through comparisons, which take doubles and produce a boolean, e.g. (x &lt; 3.1).
- **[2] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): char is an integral numeric type, so a char widens automatically to double in arithmetic ('a' + 0.5 is 97.5), but a double needs an explicit cast to become a char.
- **[3] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Every double operation rounds its result to the nearest representable value, so double results carry rounding error that can accumulate; this is why == on computed doubles is unreliable.
- **[4] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): For double operands a zero divisor is not an error: 1.0/0.0 is Infinity, -1.0/0.0 is -Infinity and 0.0/0.0 is NaN, whereas int division by zero throws an exception.
- **[5] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): double is one of the eight primitive types and the default type of decimal literals (float would need an f suffix and is not used in the book).
- **[6] purpose\_of\_the\_whole** (rule type P, plan / role rule): Used for measured or computed real quantities (physics formulas, roots, averages, probabilities); a double variable often plays the gatherer role, as in Harmonic's sum += 1.0/i.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for double: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

- **Edge:** `double` &rarr; `double@L4` (has_level)
- **Exact edge logic:** double -&gt; L4 (Extended abstract): the answer reasons beyond the given code (5 ways).

Ways (5), each with its exact rule:

- **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `FloatingPointIsExact`: Changing a variable from int to double changes / from truncating to real division and changes the printed form (3 becomes 3.0); changing back needs a cast and loses the fraction. Invariant: values are approximations, so reordering a sum ((a+b)+c vs a+(b+c)) may change the last digits.
- **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Use double for real-valued quantities where approximate results are acceptable (science, geometry, probabilities, averages); do not use it for counts, array indices, loop counters or money that must be exact (use int or long, e.g. cents).
- **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: A double cannot be assigned to an int (narrowing) without a cast. Kind: compile-time. Trigger class: A double expression assigned or passed where an int is required, e.g. int n = Math.sqrt(x); or int n = 2.0 \* k; (possible lossy conversion).
- **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: Floating-point division needs at least one double operand. Kind: silent logic error. Trigger class: A formula assigned to a double whose division has only int operands, e.g. double y = 1 / 3; (gives 0.0) or (9/5)\*c + 32.
- **[4] diagnose\_an\_error** (rule type D, error rule): rule broken: Computed doubles are approximations and must not be compared with ==. Kind: silent logic error. Trigger class: == or != between doubles produced by arithmetic on non-dyadic fractions (0.1, 1/3, square roots).

## Same topic

`double` belongs to the topic **Floating-point numbers** (`topic1.2.d`). The topic also contains: `division_by_zero`, `floating_point_precision`, `scientific_notation`.

## Rules of the concept (21)

- **Book** (SW-1e, p. 23 (pdf 33)): "The double type is for representing floating-point numbers, for use in scientific and commercial applications."
- **Book** (OT-Datatypes, ): "For decimal values, this data type is generally the default choice."
- **Book** (SW-1.2, ): "The double type is for representing floating-point numbers, e.g., for use in scientific applications."
- **E** (folk-meaning rule): Folk meaning: a number with a decimal point is the exact real number of school maths, and a whole-looking number such as 207. or 2.3e4 is an integer. Java rule: a double is a 64-bit binary approximation from a finite set of values, and any literal with a decimal point or exponent is a double (207. is 207.0, 2.3e4 is 23000.0).
- **M** (wrong rule / right rule): FloatingPointIsExact: wrong: Math.sqrt(2) \* Math.sqrt(2) == 2 is true. \| right: A double is an approximation: Math.sqrt(2) \* Math.sqrt(2) is 2.0000000000000004, so the == test is false; compare doubles with a tolerance.
- **M** (wrong rule / right rule): WholeNumberLiteralIsInt: wrong: 207. and 2.3e4 are int values because they are whole numbers. \| right: A decimal point or scientific notation makes the literal a double, whatever its value: 207. is 207.0 and 2.3e4 is 23000.0, so int n = 2.3e4; does not compile.
- **T** (uneven-application rule): Points to LT (at each operator the narrower operand is promoted, then the operation is done in double and rounded). Applied unevenly: the student promotes to double on one line but keeps integer division on another, e.g. treats 1/2 \* x as 0.5 \* x on one pass and as 0 on the next.
- **N** (identity rule): double is a primitive data type: Java's 64-bit IEEE 754 floating-point type for representing real numbers.
- **S** (declarative rule): Values are 64-bit IEEE 754 numbers (about 15 significant digits) plus the special values Infinity and NaN; +, -, \*, / (and %) are defined; if at least one operand of a binary arithmetic operator is double, the operation is a floating-point operation.
- **LT** (operational sequencing rule): Operators are applied in precedence order, left operand first; at each operator, if one operand is double the other is widened to double before the operation, and the result is rounded to the nearest double before the next operator uses it.
- **OP** (evaluation / result rule): The result has type double: 5.0/3.0 is 1.6666666666666667, 10/3.0 is 3.3333333333333335, 1.0/0.0 is Infinity, Math.sqrt(-1.0) is NaN; println always shows a decimal part (3.0, not 3).
- **OS** (state-transition rule): An assignment to a double variable stores the nearest representable value (x = x + 0.1 replaces x with the rounded sum); no double operation throws an exception, so the variable may end up holding Infinity or NaN.
- **R** (composition rule (with a neighbour)): with int: Type flow decides the division: with two int operands a / b discards the fraction (10/3 is 3, and double d = 10/3; stores 3.0); if either operand is double the other is promoted and the fraction is kept (10/3.0 is 3.3333333333333335).
- **R** (composition rule (with a neighbour)): with boolean: double and boolean never convert into each other (no cast is allowed either way); they meet only through comparisons, which take doubles and produce a boolean, e.g. (x &lt; 3.1).
- **R** (composition rule (with a neighbour)): with char: char is an integral numeric type, so a char widens automatically to double in arithmetic ('a' + 0.5 is 97.5), but a double needs an explicit cast to become a char.
- **R** (composition rule (with a neighbour)): with floating\_point\_precision: Every double operation rounds its result to the nearest representable value, so double results carry rounding error that can accumulate; this is why == on computed doubles is unreliable.
- **R** (composition rule (with a neighbour)): with division\_by\_zero: For double operands a zero divisor is not an error: 1.0/0.0 is Infinity, -1.0/0.0 is -Infinity and 0.0/0.0 is NaN, whereas int division by zero throws an exception.
- **R** (composition rule (with a neighbour)): with primitive\_type: double is one of the eight primitive types and the default type of decimal literals (float would need an f suffix and is not used in the book).
- **P** (plan / role rule): Used for measured or computed real quantities (physics formulas, roots, averages, probabilities); a double variable often plays the gatherer role, as in Harmonic's sum += 1.0/i.
- **C** (conservation rule): Changing a variable from int to double changes / from truncating to real division and changes the printed form (3 becomes 3.0); changing back needs a cast and loses the fraction. Invariant: values are approximations, so reordering a sum ((a+b)+c vs a+(b+c)) may change the last digits.
- **D** (error rule): rule broken: A double cannot be assigned to an int (narrowing) without a cast. (compile-time)
- **D** (error rule): rule broken: Floating-point division needs at least one double operand. (silent logic error)
- **D** (error rule): rule broken: Computed doubles are approximations and must not be compared with ==. (silent logic error)
- **X** (applicability rule): Use double for real-valued quantities where approximate results are acceptable (science, geometry, probabilities, averages); do not use it for counts, array indices, loop counters or money that must be exact (use int or long, e.g. cents).

## How it is found in code and answers (reader block)

- **Aliases:** double, doubles, floating point, decimal
- **Code patterns:** `\bdouble\b`, `\b\d+\.\d*\b|\b\d*\.\d+\b`
- **Operator symbols:** none
- **Java types:** `double`, `float`

## The whole prerequisite chain

- **Everything it builds on (2):** `data_type`, `primitive_type`
- **Everything that builds on it (4):** `convergence_test`, `division_by_zero`, `floating_point_precision`, `run_time_error`

## Every edge in this view and its exact edge logic (20)

All the edges drawn in the picture, in the order: prerequisite, parallel, misconception, error, has_level, contains.

**1. `double` &rarr; `division_by_zero`** (prerequisite)

- **Exact edge logic:** For doubles, 1.0/0.0 is legal and has the value Infinity; a double result can also be the special value NaN when the calculation is undefined.
- **Grounding:** book\_passage
- **Composition rule (R) of `double` with `division_by_zero`:** For double operands a zero divisor is not an error: 1.0/0.0 is Infinity, -1.0/0.0 is -Infinity and 0.0/0.0 is NaN, whereas int division by zero throws an exception.
- **Composition rule (R) of `division_by_zero` with `double`:** Once either operand is a double the division follows IEEE 754 rules instead, so the same zero divisor gives Infinity or NaN rather than an exception.

**2. `double` &rarr; `floating_point_precision`** (prerequisite)

- **Exact edge logic:** A double approximates real numbers, so its arithmetic is not exact.
- **Grounding:** book\_passage
- **Composition rule (R) of `double` with `floating_point_precision`:** Every double operation rounds its result to the nearest representable value, so double results carry rounding error that can accumulate; this is why == on computed doubles is unreliable.
- **Composition rule (R) of `floating_point_precision` with `double`:** Imprecision is inherent in the double type, not in a particular program: any arithmetic on doubles may carry rounding error, so code that uses double must be written to tolerate it.

**3. `primitive_type` &rarr; `double`** (prerequisite)

- **Exact edge logic:** double is one of the eight primitive types, the one used for real (floating-point) numbers.
- **Grounding:** book\_passage
- **Composition rule (R) of `primitive_type` with `double`:** double is the 64-bit IEEE 754 primitive. Once a double meets an integral operand in a binary operator, the whole operation becomes floating point.
- **Composition rule (R) of `double` with `primitive_type`:** double is one of the eight primitive types and the default type of decimal literals (float would need an f suffix and is not used in the book).

**4. `double` &harr; `boolean`** (parallel)

- **Exact edge logic:** A double holds a number with a fractional part; a boolean holds only true or false.
- **Grounding:** book\_passage
- **Composition rule (R) of `double` with `boolean`:** double and boolean never convert into each other (no cast is allowed either way); they meet only through comparisons, which take doubles and produce a boolean, e.g. (x &lt; 3.1).
- **Composition rule (R) of `boolean` with `double`:** A double reaches the boolean world only through a comparison such as (x &lt; 3.1), which yields a boolean; there is no cast between double and boolean.

**5. `double` &harr; `char`** (parallel)

- **Exact edge logic:** A double holds a number with a fractional part; a char holds one character code, which is a whole number.
- **Grounding:** book\_passage
- **Composition rule (R) of `double` with `char`:** char is an integral numeric type, so a char widens automatically to double in arithmetic ('a' + 0.5 is 97.5), but a double needs an explicit cast to become a char.
- **Composition rule (R) of `char` with `double`:** A char widens automatically to double (its code), but a double needs a cast to become a char. A char never holds a fractional part.

**6. `int` &harr; `double`** (parallel)

- **Exact edge logic:** With two ints, a / b drops the fractional part; if either a or b is a double, a / b keeps the fractional part.
- **Grounding:** book\_passage
- **Composition rule (R) of `int` with `double`:** int op double promotes the int and gives a double. A double becomes an int only through a cast, which truncates toward zero.
- **Composition rule (R) of `double` with `int`:** Type flow decides the division: with two int operands a / b discards the fraction (10/3 is 3, and double d = 10/3; stores 3.0); if either operand is double the other is promoted and the fraction is kept (10/3.0 is 3.3333333333333335).

**7. `double` &rarr; `FloatingPointIsExact`** (misconception)

- **Exact edge logic (the wrong rule):** Math.sqrt(2) \* Math.sqrt(2) == 2 is true.
- **Twin logic (the right rule):** A double is an approximation, so the product is close to 2 but not equal to 2.
- **Role:** context

**8. `double` &rarr; `WholeNumberLiteralIsInt`** (misconception)

- **Exact edge logic (the wrong rule):** 207. and 2.3e4 are int values because they are whole numbers.
- **Twin logic (the right rule):** A decimal point or scientific notation makes the literal a double.
- **Role:** context

**9. `convergence_test` &rarr; `FloatingPointIsExact`** (misconception)

- **Exact edge logic (the wrong rule):** Math.sqrt(2) \* Math.sqrt(2) == 2 is true.
- **Twin logic (the right rule):** A double is an approximation, so the product is close to 2 but not equal to 2.
- **Role:** context

**10. `floating_point_precision` &rarr; `FloatingPointIsExact`** (misconception)

- **Exact edge logic (the wrong rule):** Math.sqrt(2) \* Math.sqrt(2) == 2 is true.
- **Twin logic (the right rule):** A double is an approximation, so the product is close to 2 but not equal to 2.
- **Role:** primary

**11. `literal` &rarr; `WholeNumberLiteralIsInt`** (misconception)

- **Exact edge logic (the wrong rule):** 207. and 2.3e4 are int values because they are whole numbers.
- **Twin logic (the right rule):** A decimal point or scientific notation makes the literal a double.
- **Role:** primary

**12. `double` &rarr; `double@L0`** (has_level)

- **Exact edge logic:** double -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (4 ways).
  - **[0] everyday\_reading** (rule type E, folk-meaning rule): Folk meaning: a number with a decimal point is the exact real number of school maths, and a whole-looking number such as 207. or 2.3e4 is an integer. Java rule: a double is a 64-bit binary approximation from a finite set of values, and any literal with a decimal point or exponent is a double (207. is 207.0, 2.3e4 is 23000.0).
  - **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `FloatingPointIsExact`: wrong rule: Math.sqrt(2) \* Math.sqrt(2) == 2 is true. Right rule: A double is an approximation: Math.sqrt(2) \* Math.sqrt(2) is 2.0000000000000004, so the == test is false; compare doubles with a tolerance.
  - **[2] misconception** (rule type M, wrong rule / right rule) &rarr; `WholeNumberLiteralIsInt`: wrong rule: 207. and 2.3e4 are int values because they are whole numbers. Right rule: A decimal point or scientific notation makes the literal a double, whatever its value: 207. is 207.0 and 2.3e4 is 23000.0, so int n = 2.3e4; does not compile.
  - **[3] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `FloatingPointIsExact`: Points to LT (at each operator the narrower operand is promoted, then the operation is done in double and rounded). Applied unevenly: the student promotes to double on one line but keeps integer division on another, e.g. treats 1/2 \* x as 0.5 \* x on one pass and as 0 on the next. (here mixing in: "Math.sqrt(2) \* Math.sqrt(2) == 2 is true")

**13. `double` &rarr; `double@L1`** (has_level)

- **Exact edge logic:** double -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).
  - **[0] names\_the\_element** (rule type N, identity rule): double is a primitive data type: Java's 64-bit IEEE 754 floating-point type for representing real numbers.
  - **[1] states\_the\_rule** (rule type S, declarative rule): Values are 64-bit IEEE 754 numbers (about 15 significant digits) plus the special values Infinity and NaN; +, -, \*, / (and %) are defined; if at least one operand of a binary arithmetic operator is double, the operation is a floating-point operation.

**14. `double` &rarr; `double@L2`** (has_level)

- **Exact edge logic:** double -&gt; L2 (Multistructural): the answer applies the rules of double to every part of the code, in order (3 ways).
  - **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): Operators are applied in precedence order, left operand first; at each operator, if one operand is double the other is widened to double before the operation, and the result is rounded to the nearest double before the next operator uses it.
  - **[1] output\_prediction** (rule type OP, evaluation / result rule): The result has type double: 5.0/3.0 is 1.6666666666666667, 10/3.0 is 3.3333333333333335, 1.0/0.0 is Infinity, Math.sqrt(-1.0) is NaN; println always shows a decimal part (3.0, not 3).
  - **[2] one\_step\_execution** (rule type OS, state-transition rule): An assignment to a double variable stores the nearest representable value (x = x + 0.1 replaces x with the rounded sum); no double operation throws an exception, so the variable may end up holding Infinity or NaN.

**15. `double` &rarr; `double@L3`** (has_level)

- **Exact edge logic:** double -&gt; L3 (Relational): the answer relates the parts (7 ways).
  - **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Type flow decides the division: with two int operands a / b discards the fraction (10/3 is 3, and double d = 10/3; stores 3.0); if either operand is double the other is promoted and the fraction is kept (10/3.0 is 3.3333333333333335).
  - **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): double and boolean never convert into each other (no cast is allowed either way); they meet only through comparisons, which take doubles and produce a boolean, e.g. (x &lt; 3.1).
  - **[2] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): char is an integral numeric type, so a char widens automatically to double in arithmetic ('a' + 0.5 is 97.5), but a double needs an explicit cast to become a char.
  - **[3] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Every double operation rounds its result to the nearest representable value, so double results carry rounding error that can accumulate; this is why == on computed doubles is unreliable.
  - **[4] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): For double operands a zero divisor is not an error: 1.0/0.0 is Infinity, -1.0/0.0 is -Infinity and 0.0/0.0 is NaN, whereas int division by zero throws an exception.
  - **[5] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): double is one of the eight primitive types and the default type of decimal literals (float would need an f suffix and is not used in the book).
  - **[6] purpose\_of\_the\_whole** (rule type P, plan / role rule): Used for measured or computed real quantities (physics formulas, roots, averages, probabilities); a double variable often plays the gatherer role, as in Harmonic's sum += 1.0/i.

**16. `double` &rarr; `double@L4`** (has_level)

- **Exact edge logic:** double -&gt; L4 (Extended abstract): the answer reasons beyond the given code (5 ways).
  - **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `FloatingPointIsExact`: Changing a variable from int to double changes / from truncating to real division and changes the printed form (3 becomes 3.0); changing back needs a cast and loses the fraction. Invariant: values are approximations, so reordering a sum ((a+b)+c vs a+(b+c)) may change the last digits.
  - **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Use double for real-valued quantities where approximate results are acceptable (science, geometry, probabilities, averages); do not use it for counts, array indices, loop counters or money that must be exact (use int or long, e.g. cents).
  - **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: A double cannot be assigned to an int (narrowing) without a cast. Kind: compile-time. Trigger class: A double expression assigned or passed where an int is required, e.g. int n = Math.sqrt(x); or int n = 2.0 \* k; (possible lossy conversion).
  - **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: Floating-point division needs at least one double operand. Kind: silent logic error. Trigger class: A formula assigned to a double whose division has only int operands, e.g. double y = 1 / 3; (gives 0.0) or (9/5)\*c + 32.
  - **[4] diagnose\_an\_error** (rule type D, error rule): rule broken: Computed doubles are approximations and must not be compared with ==. Kind: silent logic error. Trigger class: == or != between doubles produced by arithmetic on non-dyadic fractions (0.1, 1/3, square roots).

**17. `topic1.2.d` &rarr; `double`** (contains)

- topic `topic1.2.d` contains `double`

**18. `topic1.2.d` &rarr; `division_by_zero`** (contains)

- topic `topic1.2.d` contains `division_by_zero`

**19. `topic1.2.d` &rarr; `floating_point_precision`** (contains)

- topic `topic1.2.d` contains `floating_point_precision`

**20. `topic1.2.d` &rarr; `scientific_notation`** (contains)

- topic `topic1.2.d` contains `scientific_notation`
