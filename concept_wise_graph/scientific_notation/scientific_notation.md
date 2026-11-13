# scientific_notation (`scientific_notation`)

double literals like 6.022E23

Section 1.2 Built-in Types of Data, topic 1.2.d Floating-point numbers.

![The knowledge graph around scientific_notation](scientific_notation.png)

## At a glance

- **Needs first:** `literal`
- **Leads to:** nothing
- **Learned alongside:** nothing
- **Misconceptions:** `ExponentIsPower`
- **Errors:** none
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 11 edges around this concept, each explained in the graph's own words.

## What it needs first (1)

A prerequisite edge means the other concept has to be understood before `scientific_notation`.

### `literal` comes before `scientific_notation`

*a constant value written in code (42, 3.14, true, 'a', "hi")*

Scientific notation is a form of double literal.

- **Grounding:** book passage
- **How `scientific_notation` combines with `literal`:** Scientific notation is a double literal, so the literal rules for double apply: it cannot initialize an int without a cast (int n = 1e6; does not compile).
- **How `literal` combines with `scientific_notation`:** E-notation is a form of double literal. 6.022e23 and even 1e6 are doubles, so int n = 1e6; needs a cast.

## What it leads to (0)

These concepts need `scientific_notation` first.

No concept has this one as a prerequisite.

## Learned alongside (0)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

No parallel edge touches this concept.

## Misconceptions (1)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### ExponentIsPower

- **Wrong rule:** 6.022E23 means 6.022 times e to the power 23.
- **Right rule:** E23 means times 10 to the 23rd.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: 6.022E23 means 6.022 times e to the power 23. Right rule: E23 means times 10 to the 23rd; e to a power is computed with Math.exp(23), and the constant e is Math.E.
- **Shows at level L0 as:** inconsistent trace: Points to LT (the literal is converted once, at compile time, to the nearest double). Applied unevenly: the student shifts the decimal point the right way for 1e6 but the wrong way for a negative exponent such as 1e-15, or treats 1e6 as an int on some lines. (here mixing in: "6.022E23 means 6.022 times e to the power 23")

## Errors (0)

An error edge states the rule that gets broken in a program, and the right rule.

The graph has no error edge from this concept.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for scientific notation: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to scientific notation agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

scientific notation -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (3 ways).

- **everyday reading** (folk-meaning rule): Folk meaning: in maths e is Euler's number 2.718..., so 6.022E23 reads as 6.022 times e to the 23rd. Java rule: inside a numeric literal, e or E means 'times ten to the power', so 6.022e23 is 6.022 x 10^23; Euler's number is Math.E and e^x is Math.exp(x).
- **misconception** (wrong rule / right rule; shows `ExponentIsPower`): wrong rule: 6.022E23 means 6.022 times e to the power 23. Right rule: E23 means times 10 to the 23rd; e to a power is computed with Math.exp(23), and the constant e is Math.E.
- **inconsistent trace** (uneven-application rule; shows `ExponentIsPower`): Points to LT (the literal is converted once, at compile time, to the nearest double). Applied unevenly: the student shifts the decimal point the right way for 1e6 but the wrong way for a negative exponent such as 1e-15, or treats 1e6 as an int on some lines. (here mixing in: "6.022E23 means 6.022 times e to the power 23")

### L1: Unistructural / atom x text surface

L1 for scientific notation: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

scientific notation -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

- **names the element** (identity rule): Scientific notation is a form of floating-point (double) literal: a mantissa, then e or E, then a signed integer exponent of ten.
- **states the rule** (declarative rule): mEn denotes m x 10^n and is always of type double, even when the value is whole (1e6 is 1000000.0); the exponent may be negative (1e-15).

### L2: Multistructural / block x execution / preoperational

L2 for scientific notation: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

scientific notation -&gt; L2 (Multistructural): the answer applies the rules of scientific notation to every part of the code, in order (3 ways).

- **line by line trace** (operational sequencing rule): The value is fixed at compile time; at run time the literal is just a double operand, so the usual promotion applies to the other operand of each operator it meets.
- **output prediction** (evaluation / result rule): Type double: 6.02e23 / 2.0 is 3.01E23; 1e6 is 1000000.0; 1e-15 is 1.0E-15; println prints very large or very small doubles back in E notation.
- **one step execution** (state-transition rule): Evaluating the literal changes nothing; double big = 6.022e23; stores the nearest double to 6.022 x 10^23 in big.

### L3: Relational / relations x function (concrete operational begins)

L3 for scientific notation: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

scientific notation -&gt; L3 (Relational): the answer relates the parts (2 ways).

- **relation to neighbour** (composition rule (with a neighbour)): Scientific notation is a double literal, so the literal rules for double apply: it cannot initialize an int without a cast (int n = 1e6; does not compile).
- **purpose of the whole** (plan / role rule): Used to write very large or very small fixed constants readably, e.g. Avogadro's number or a tolerance epsilon = 1e-15 (Sajaniemi role: fixed value).

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for scientific notation: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

scientific notation -&gt; L4 (Extended abstract): the answer reasons beyond the given code (4 ways).

- **predict a change** (conservation rule; shows `ExponentIsPower`): Changing the sign of the exponent changes the magnitude by a factor 10^(2n); replacing 1e6 by 10^6 changes the value to 12 (^ is exclusive or); replacing it by Math.pow(10, 6) keeps the value but computes it at run time.
- **transfer to a new program** (applicability rule): Use e-notation for double constants spanning many orders of magnitude (physical constants, tolerances); for exact integers use int or long literals, and for computed powers use Math.pow.
- **diagnose an error** (error rule): rule broken: A power of ten is written with e-notation (or Math.pow), not with ^. Kind: silent logic error. Trigger class: Writing 10^6 (or 2^n) with int operands: it compiles and evaluates the exclusive or (10^6 is 12).
- **diagnose an error** (error rule): rule broken: An e-notation literal is a double and cannot be stored in an int without a cast. Kind: compile-time. Trigger class: int n = 1e6; or passing 1e3 to an int parameter.

## Same topic

`scientific_notation` belongs to the topic **Floating-point numbers** (`topic1.2.d`). The topic also contains: `division_by_zero`, `double`, `floating_point_precision`.

## Rules of the concept (14)

- **folk-meaning rule:** Folk meaning: in maths e is Euler's number 2.718..., so 6.022E23 reads as 6.022 times e to the 23rd. Java rule: inside a numeric literal, e or E means 'times ten to the power', so 6.022e23 is 6.022 x 10^23; Euler's number is Math.E and e^x is Math.exp(x).
- **wrong rule / right rule:** ExponentIsPower: wrong: 6.022E23 means 6.022 times e to the power 23. \| right: E23 means times 10 to the 23rd; e to a power is computed with Math.exp(23), and the constant e is Math.E.
- **uneven-application rule:** Points to LT (the literal is converted once, at compile time, to the nearest double). Applied unevenly: the student shifts the decimal point the right way for 1e6 but the wrong way for a negative exponent such as 1e-15, or treats 1e6 as an int on some lines.
- **identity rule:** Scientific notation is a form of floating-point (double) literal: a mantissa, then e or E, then a signed integer exponent of ten.
- **declarative rule:** mEn denotes m x 10^n and is always of type double, even when the value is whole (1e6 is 1000000.0); the exponent may be negative (1e-15).
- **operational sequencing rule:** The value is fixed at compile time; at run time the literal is just a double operand, so the usual promotion applies to the other operand of each operator it meets.
- **evaluation / result rule:** Type double: 6.02e23 / 2.0 is 3.01E23; 1e6 is 1000000.0; 1e-15 is 1.0E-15; println prints very large or very small doubles back in E notation.
- **state-transition rule:** Evaluating the literal changes nothing; double big = 6.022e23; stores the nearest double to 6.022 x 10^23 in big.
- **composition rule (with a neighbour):** with literal: Scientific notation is a double literal, so the literal rules for double apply: it cannot initialize an int without a cast (int n = 1e6; does not compile).
- **plan / role rule:** Used to write very large or very small fixed constants readably, e.g. Avogadro's number or a tolerance epsilon = 1e-15 (Sajaniemi role: fixed value).
- **conservation rule:** Changing the sign of the exponent changes the magnitude by a factor 10^(2n); replacing 1e6 by 10^6 changes the value to 12 (^ is exclusive or); replacing it by Math.pow(10, 6) keeps the value but computes it at run time.
- **error rule:** rule broken: A power of ten is written with e-notation (or Math.pow), not with ^. (silent logic error)
- **error rule:** rule broken: An e-notation literal is a double and cannot be stored in an int without a cast. (compile-time)
- **applicability rule:** Use e-notation for double constants spanning many orders of magnitude (physical constants, tolerances); for exact integers use int or long literals, and for computed powers use Math.pow.

## The whole prerequisite chain

- **Everything it builds on (3):** `data_type`, `literal`, `primitive_type`
- **Everything that builds on it (0):** nothing
