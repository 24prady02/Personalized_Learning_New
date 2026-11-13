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

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 11 edges around this concept. The edge logic, the wrong and right rules and the exact rules of the ways are copied word for word from the graph.

## To work on (0)

Nothing is missing for this concept.

## What it needs first (1)

A prerequisite edge means the other concept has to be understood before `scientific_notation`.

### `literal` comes before `scientific_notation`

*a constant value written in code (42, 3.14, true, 'a', "hi")*

- **Edge:** `pre:literal->scientific_notation`
- **Exact edge logic:** Scientific notation is a form of double literal.
- **Grounding:** book\_passage
- **Composition rule (R) of `scientific_notation` with `literal`:** Scientific notation is a double literal, so the literal rules for double apply: it cannot initialize an int without a cast (int n = 1e6; does not compile).
- **Composition rule (R) of `literal` with `scientific_notation`:** E-notation is a form of double literal. 6.022e23 and even 1e6 are doubles, so int n = 1e6; needs a cast.

## What it leads to (0)

These concepts need `scientific_notation` first.

No concept has this one as a prerequisite.

## Learned alongside (0)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

No parallel edge touches this concept.

## Misconceptions (1)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### ExponentIsPower

- **Edge:** `scientific_notation` &rarr; `ExponentIsPower` (misconception)
- **Exact edge logic (the wrong rule):** 6.022E23 means 6.022 times e to the power 23.
- **Twin logic (the right rule):** E23 means times 10 to the 23rd.
- **Wrong belief (on the node):** 6.022E23 means 6.022 times e to the power 23.
- **Correct rule (on the node):** E23 means times 10 to the 23rd.
- **Provenance:** derived
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [1] misconception, exact rule:** wrong rule: 6.022E23 means 6.022 times e to the power 23. Right rule: E23 means times 10 to the 23rd; e to a power is computed with Math.exp(23), and the constant e is Math.E.
- **L0 way [2] inconsistent\_trace, exact rule:** Points to LT (the literal is converted once, at compile time, to the nearest double). Applied unevenly: the student shifts the decimal point the right way for 1e6 but the wrong way for a negative exponent such as 1e-15, or treats 1e6 as an int on some lines. (here mixing in: "6.022E23 means 6.022 times e to the power 23")

## Errors (0)

An error edge states the rule that gets broken in a program, and the right rule.

The graph has no error edge from this concept.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for scientific notation: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to scientific notation agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

- **Edge:** `scientific_notation` &rarr; `scientific_notation@L0` (has_level)
- **Exact edge logic:** scientific notation -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (3 ways).

Ways (3), each with its exact rule:

- **[0] everyday\_reading** (rule type E, folk-meaning rule): Folk meaning: in maths e is Euler's number 2.718..., so 6.022E23 reads as 6.022 times e to the 23rd. Java rule: inside a numeric literal, e or E means 'times ten to the power', so 6.022e23 is 6.022 x 10^23; Euler's number is Math.E and e^x is Math.exp(x).
- **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `ExponentIsPower`: wrong rule: 6.022E23 means 6.022 times e to the power 23. Right rule: E23 means times 10 to the 23rd; e to a power is computed with Math.exp(23), and the constant e is Math.E.
- **[2] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `ExponentIsPower`: Points to LT (the literal is converted once, at compile time, to the nearest double). Applied unevenly: the student shifts the decimal point the right way for 1e6 but the wrong way for a negative exponent such as 1e-15, or treats 1e6 as an int on some lines. (here mixing in: "6.022E23 means 6.022 times e to the power 23")

### L1: Unistructural / atom x text surface

L1 for scientific notation: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

- **Edge:** `scientific_notation` &rarr; `scientific_notation@L1` (has_level)
- **Exact edge logic:** scientific notation -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

Ways (2), each with its exact rule:

- **[0] names\_the\_element** (rule type N, identity rule): Scientific notation is a form of floating-point (double) literal: a mantissa, then e or E, then a signed integer exponent of ten.
- **[1] states\_the\_rule** (rule type S, declarative rule): mEn denotes m x 10^n and is always of type double, even when the value is whole (1e6 is 1000000.0); the exponent may be negative (1e-15).

### L2: Multistructural / block x execution / preoperational

L2 for scientific notation: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

- **Edge:** `scientific_notation` &rarr; `scientific_notation@L2` (has_level)
- **Exact edge logic:** scientific notation -&gt; L2 (Multistructural): the answer applies the rules of scientific notation to every part of the code, in order (3 ways).

Ways (3), each with its exact rule:

- **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): The value is fixed at compile time; at run time the literal is just a double operand, so the usual promotion applies to the other operand of each operator it meets.
- **[1] output\_prediction** (rule type OP, evaluation / result rule): Type double: 6.02e23 / 2.0 is 3.01E23; 1e6 is 1000000.0; 1e-15 is 1.0E-15; println prints very large or very small doubles back in E notation.
- **[2] one\_step\_execution** (rule type OS, state-transition rule): Evaluating the literal changes nothing; double big = 6.022e23; stores the nearest double to 6.022 x 10^23 in big.

### L3: Relational / relations x function (concrete operational begins)

L3 for scientific notation: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

- **Edge:** `scientific_notation` &rarr; `scientific_notation@L3` (has_level)
- **Exact edge logic:** scientific notation -&gt; L3 (Relational): the answer relates the parts (2 ways).

Ways (2), each with its exact rule:

- **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Scientific notation is a double literal, so the literal rules for double apply: it cannot initialize an int without a cast (int n = 1e6; does not compile).
- **[1] purpose\_of\_the\_whole** (rule type P, plan / role rule): Used to write very large or very small fixed constants readably, e.g. Avogadro's number or a tolerance epsilon = 1e-15 (Sajaniemi role: fixed value).

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for scientific notation: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

- **Edge:** `scientific_notation` &rarr; `scientific_notation@L4` (has_level)
- **Exact edge logic:** scientific notation -&gt; L4 (Extended abstract): the answer reasons beyond the given code (4 ways).

Ways (4), each with its exact rule:

- **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `ExponentIsPower`: Changing the sign of the exponent changes the magnitude by a factor 10^(2n); replacing 1e6 by 10^6 changes the value to 12 (^ is exclusive or); replacing it by Math.pow(10, 6) keeps the value but computes it at run time.
- **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Use e-notation for double constants spanning many orders of magnitude (physical constants, tolerances); for exact integers use int or long literals, and for computed powers use Math.pow.
- **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: A power of ten is written with e-notation (or Math.pow), not with ^. Kind: silent logic error. Trigger class: Writing 10^6 (or 2^n) with int operands: it compiles and evaluates the exclusive or (10^6 is 12).
- **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: An e-notation literal is a double and cannot be stored in an int without a cast. Kind: compile-time. Trigger class: int n = 1e6; or passing 1e3 to an int parameter.

## Same topic

`scientific_notation` belongs to the topic **Floating-point numbers** (`topic1.2.d`). The topic also contains: `division_by_zero`, `double`, `floating_point_precision`.

## Rules of the concept (14)

- **Book** (SW-1e, p. 23 (pdf 33)): "the literal 6.022e23 represents the number 6.022"
- **Book** (SW-1.2, ): "with a notation like scientific notation, e.g., 6.022E23 for Avogadro's constant"
- **E** (folk-meaning rule): Folk meaning: in maths e is Euler's number 2.718..., so 6.022E23 reads as 6.022 times e to the 23rd. Java rule: inside a numeric literal, e or E means 'times ten to the power', so 6.022e23 is 6.022 x 10^23; Euler's number is Math.E and e^x is Math.exp(x).
- **M** (wrong rule / right rule): ExponentIsPower: wrong: 6.022E23 means 6.022 times e to the power 23. \| right: E23 means times 10 to the 23rd; e to a power is computed with Math.exp(23), and the constant e is Math.E.
- **T** (uneven-application rule): Points to LT (the literal is converted once, at compile time, to the nearest double). Applied unevenly: the student shifts the decimal point the right way for 1e6 but the wrong way for a negative exponent such as 1e-15, or treats 1e6 as an int on some lines.
- **N** (identity rule): Scientific notation is a form of floating-point (double) literal: a mantissa, then e or E, then a signed integer exponent of ten.
- **S** (declarative rule): mEn denotes m x 10^n and is always of type double, even when the value is whole (1e6 is 1000000.0); the exponent may be negative (1e-15).
- **LT** (operational sequencing rule): The value is fixed at compile time; at run time the literal is just a double operand, so the usual promotion applies to the other operand of each operator it meets.
- **OP** (evaluation / result rule): Type double: 6.02e23 / 2.0 is 3.01E23; 1e6 is 1000000.0; 1e-15 is 1.0E-15; println prints very large or very small doubles back in E notation.
- **OS** (state-transition rule): Evaluating the literal changes nothing; double big = 6.022e23; stores the nearest double to 6.022 x 10^23 in big.
- **R** (composition rule (with a neighbour)): with literal: Scientific notation is a double literal, so the literal rules for double apply: it cannot initialize an int without a cast (int n = 1e6; does not compile).
- **P** (plan / role rule): Used to write very large or very small fixed constants readably, e.g. Avogadro's number or a tolerance epsilon = 1e-15 (Sajaniemi role: fixed value).
- **C** (conservation rule): Changing the sign of the exponent changes the magnitude by a factor 10^(2n); replacing 1e6 by 10^6 changes the value to 12 (^ is exclusive or); replacing it by Math.pow(10, 6) keeps the value but computes it at run time.
- **D** (error rule): rule broken: A power of ten is written with e-notation (or Math.pow), not with ^. (silent logic error)
- **D** (error rule): rule broken: An e-notation literal is a double and cannot be stored in an int without a cast. (compile-time)
- **X** (applicability rule): Use e-notation for double constants spanning many orders of magnitude (physical constants, tolerances); for exact integers use int or long literals, and for computed powers use Math.pow.

## How it is found in code and answers (reader block)

- **Aliases:** scientific notation, e notation
- **Code patterns:** `\d[eE][+\-]?\d`
- **Operator symbols:** none
- **Java types:** none

## The whole prerequisite chain

- **Everything it builds on (3):** `data_type`, `literal`, `primitive_type`
- **Everything that builds on it (0):** nothing

## Every edge in this view and its exact edge logic (11)

All the edges drawn in the picture, in the order: prerequisite, parallel, misconception, error, has_level, contains.

**1. `literal` &rarr; `scientific_notation`** (prerequisite)

- **Exact edge logic:** Scientific notation is a form of double literal.
- **Grounding:** book\_passage
- **Composition rule (R) of `literal` with `scientific_notation`:** E-notation is a form of double literal. 6.022e23 and even 1e6 are doubles, so int n = 1e6; needs a cast.
- **Composition rule (R) of `scientific_notation` with `literal`:** Scientific notation is a double literal, so the literal rules for double apply: it cannot initialize an int without a cast (int n = 1e6; does not compile).

**2. `scientific_notation` &rarr; `ExponentIsPower`** (misconception)

- **Exact edge logic (the wrong rule):** 6.022E23 means 6.022 times e to the power 23.
- **Twin logic (the right rule):** E23 means times 10 to the 23rd.
- **Role:** primary

**3. `scientific_notation` &rarr; `scientific_notation@L0`** (has_level)

- **Exact edge logic:** scientific notation -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (3 ways).
  - **[0] everyday\_reading** (rule type E, folk-meaning rule): Folk meaning: in maths e is Euler's number 2.718..., so 6.022E23 reads as 6.022 times e to the 23rd. Java rule: inside a numeric literal, e or E means 'times ten to the power', so 6.022e23 is 6.022 x 10^23; Euler's number is Math.E and e^x is Math.exp(x).
  - **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `ExponentIsPower`: wrong rule: 6.022E23 means 6.022 times e to the power 23. Right rule: E23 means times 10 to the 23rd; e to a power is computed with Math.exp(23), and the constant e is Math.E.
  - **[2] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `ExponentIsPower`: Points to LT (the literal is converted once, at compile time, to the nearest double). Applied unevenly: the student shifts the decimal point the right way for 1e6 but the wrong way for a negative exponent such as 1e-15, or treats 1e6 as an int on some lines. (here mixing in: "6.022E23 means 6.022 times e to the power 23")

**4. `scientific_notation` &rarr; `scientific_notation@L1`** (has_level)

- **Exact edge logic:** scientific notation -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).
  - **[0] names\_the\_element** (rule type N, identity rule): Scientific notation is a form of floating-point (double) literal: a mantissa, then e or E, then a signed integer exponent of ten.
  - **[1] states\_the\_rule** (rule type S, declarative rule): mEn denotes m x 10^n and is always of type double, even when the value is whole (1e6 is 1000000.0); the exponent may be negative (1e-15).

**5. `scientific_notation` &rarr; `scientific_notation@L2`** (has_level)

- **Exact edge logic:** scientific notation -&gt; L2 (Multistructural): the answer applies the rules of scientific notation to every part of the code, in order (3 ways).
  - **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): The value is fixed at compile time; at run time the literal is just a double operand, so the usual promotion applies to the other operand of each operator it meets.
  - **[1] output\_prediction** (rule type OP, evaluation / result rule): Type double: 6.02e23 / 2.0 is 3.01E23; 1e6 is 1000000.0; 1e-15 is 1.0E-15; println prints very large or very small doubles back in E notation.
  - **[2] one\_step\_execution** (rule type OS, state-transition rule): Evaluating the literal changes nothing; double big = 6.022e23; stores the nearest double to 6.022 x 10^23 in big.

**6. `scientific_notation` &rarr; `scientific_notation@L3`** (has_level)

- **Exact edge logic:** scientific notation -&gt; L3 (Relational): the answer relates the parts (2 ways).
  - **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Scientific notation is a double literal, so the literal rules for double apply: it cannot initialize an int without a cast (int n = 1e6; does not compile).
  - **[1] purpose\_of\_the\_whole** (rule type P, plan / role rule): Used to write very large or very small fixed constants readably, e.g. Avogadro's number or a tolerance epsilon = 1e-15 (Sajaniemi role: fixed value).

**7. `scientific_notation` &rarr; `scientific_notation@L4`** (has_level)

- **Exact edge logic:** scientific notation -&gt; L4 (Extended abstract): the answer reasons beyond the given code (4 ways).
  - **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `ExponentIsPower`: Changing the sign of the exponent changes the magnitude by a factor 10^(2n); replacing 1e6 by 10^6 changes the value to 12 (^ is exclusive or); replacing it by Math.pow(10, 6) keeps the value but computes it at run time.
  - **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Use e-notation for double constants spanning many orders of magnitude (physical constants, tolerances); for exact integers use int or long literals, and for computed powers use Math.pow.
  - **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: A power of ten is written with e-notation (or Math.pow), not with ^. Kind: silent logic error. Trigger class: Writing 10^6 (or 2^n) with int operands: it compiles and evaluates the exclusive or (10^6 is 12).
  - **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: An e-notation literal is a double and cannot be stored in an int without a cast. Kind: compile-time. Trigger class: int n = 1e6; or passing 1e3 to an int parameter.

**8. `topic1.2.d` &rarr; `scientific_notation`** (contains)

- topic `topic1.2.d` contains `scientific_notation`

**9. `topic1.2.d` &rarr; `division_by_zero`** (contains)

- topic `topic1.2.d` contains `division_by_zero`

**10. `topic1.2.d` &rarr; `double`** (contains)

- topic `topic1.2.d` contains `double`

**11. `topic1.2.d` &rarr; `floating_point_precision`** (contains)

- topic `topic1.2.d` contains `floating_point_precision`
