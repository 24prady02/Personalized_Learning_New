# int_literal_limit (`int_literal_limit`)

2147483648 is legal only as -2147483648

Section 1.2 Built-in Types of Data, topic 1.2.c Integers.

![The knowledge graph around int_literal_limit](int_literal_limit.png)

## At a glance

- **Needs first:** `int`, `literal`
- **Leads to:** nothing
- **Learned alongside:** nothing
- **Misconceptions:** `LargeIntegerLong`
- **Errors:** none
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 18 edges around this concept. The edge logic, the wrong and right rules and the exact rules of the ways are copied word for word from the graph.

## To work on (1)

- no aliases: a student's words cannot name this concept

## What it needs first (2)

A prerequisite edge means the other concept has to be understood before `int_literal_limit`.

### `int` comes before `int_literal_limit`

*32-bit integer primitive*

- **Edge:** `pre:int->int_literal_limit`
- **Exact edge logic:** The limit on int literals is int's 32-bit range, -2147483648 to 2147483647.
- **Grounding:** book\_passage
- **Composition rule (R) of `int_literal_limit` with `int`:** The literal limit is exactly int's 32-bit range, but it is checked only for literals: the literal 2147483648 is a compile-time error, whereas the expression 2147483647 + 1 compiles and overflows at run time to -2147483648.
- **Composition rule (R) of `int` with `int_literal_limit`:** An int literal must lie in int's range, so larger digit strings need an L (long) literal.

### `literal` comes before `int_literal_limit`

*a constant value written in code (42, 3.14, true, 'a', "hi")*

- **Edge:** `pre:literal->int_literal_limit`
- **Exact edge logic:** An int literal is legal only if its value lies within the int range, so a digit sequence outside -2147483648..2147483647 is not a valid int literal.
- **Grounding:** book\_passage
- **Composition rule (R) of `int_literal_limit` with `literal`:** The general literal rule (a source-code representation of a value) is constrained here by int's range: a digit sequence outside -2147483648..2147483647 is not a valid int literal and must be written as a long literal with L.
- **Composition rule (R) of `literal` with `int_literal_limit`:** A literal without L must lie in -2147483648..2147483647, so 2147483648 alone is a compile error. Larger values need a long literal (2147483648L).

## What it leads to (0)

These concepts need `int_literal_limit` first.

No concept has this one as a prerequisite.

## Learned alongside (0)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

No parallel edge touches this concept.

## Misconceptions (1)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### LargeIntegerLong

- **Edge:** `int_literal_limit` &rarr; `LargeIntegerLong` (misconception)
- **Exact edge logic (the wrong rule):** a large integer literal is automatically long
- **Twin logic (the right rule):** A sequence of digits is an int literal only if its value falls within the int range; for larger values the book advises the long type.
- **Wrong belief (on the node):** a large integer literal is automatically long
- **Correct rule (on the node):** A sequence of digits is an int literal only if its value falls within the int range; for larger values the book advises the long type.
- **Provenance:** published
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [1] misconception, exact rule:** wrong rule: A large integer literal is automatically long. Right rule: A digit sequence is an int literal only if its value lies within the int range; a larger literal such as 3000000000 is a compile-time error unless written with the L suffix (3000000000L), and the book advises the long type for values of ten digits or more.
- **L0 way [2] inconsistent\_trace, exact rule:** Points to LT (the compiler checks each literal's value against the int range when it reads the token, before any code runs). Applied unevenly: the student accepts one out-of-range literal as 'automatically long' but rejects another, or treats -2147483648 as illegal because 2147483648 alone is illegal, or expects the range check to apply to computed values such as 2147483647 + 1 (which compiles and wraps). (here mixing in: "a large integer literal is automatically long")
- **Edge `literal` &rarr; `LargeIntegerLong`, exact edge logic:** A whole-number literal that is too big for an int automatically becomes a long. **Twin logic:** A sequence of digits is an int literal only if its value falls within the int range; for larger values the book advises the long type. (role: primary)
- **Edge `long_type` &rarr; `LargeIntegerLong`, exact edge logic:** a large integer literal is automatically long **Twin logic:** A sequence of digits is an int literal only if its value falls within the int range; for larger values the book advises the long type. (role: context)

## Errors (0)

An error edge states the rule that gets broken in a program, and the right rule.

The graph has no error edge from this concept.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for int literal limit: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to int literal limit agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

- **Edge:** `int_literal_limit` &rarr; `int_literal_limit@L0` (has_level)
- **Exact edge logic:** int literal limit -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (3 ways).

Ways (3), each with its exact rule:

- **[0] everyday\_reading** (rule type E, folk-meaning rule): Folk meaning: in maths any string of digits names a number, and a very large number simply 'becomes' a bigger kind of number. Java rule: a digit sequence without an L suffix is an int literal and must denote a value in -2147483648..2147483647; 2147483648 is legal only as the operand of unary minus (-2147483648), and 3000000000 does not compile (write 3000000000L).
- **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `LargeIntegerLong`: wrong rule: A large integer literal is automatically long. Right rule: A digit sequence is an int literal only if its value lies within the int range; a larger literal such as 3000000000 is a compile-time error unless written with the L suffix (3000000000L), and the book advises the long type for values of ten digits or more.
- **[2] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `LargeIntegerLong`: Points to LT (the compiler checks each literal's value against the int range when it reads the token, before any code runs). Applied unevenly: the student accepts one out-of-range literal as 'automatically long' but rejects another, or treats -2147483648 as illegal because 2147483648 alone is illegal, or expects the range check to apply to computed values such as 2147483647 + 1 (which compiles and wraps). (here mixing in: "a large integer literal is automatically long")

### L1: Unistructural / atom x text surface

L1 for int literal limit: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

- **Edge:** `int_literal_limit` &rarr; `int_literal_limit@L1` (has_level)
- **Exact edge logic:** int literal limit -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

Ways (2), each with its exact rule:

- **[0] names\_the\_element** (rule type N, identity rule): An int literal is a lexical constant: a source-code representation of an int value, written as decimal digits (optionally signed) whose value lies within the int range.
- **[1] states\_the\_rule** (rule type S, declarative rule): A digit sequence is an int literal only when its decimal value lies between -2147483648 and 2147483647 inclusive; the magnitude 2147483648 may appear only as -2147483648; larger literals need the long suffix L.

### L2: Multistructural / block x execution / preoperational

L2 for int literal limit: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

- **Edge:** `int_literal_limit` &rarr; `int_literal_limit@L2` (has_level)
- **Exact edge logic:** int literal limit -&gt; L2 (Multistructural): the answer applies the rules of int literal limit to every part of the code, in order (3 ways).

Ways (3), each with its exact rule:

- **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): At compile time the compiler reads the digit token, converts it to a value and checks the range; at run time the literal is simply evaluated to that fixed value, and a leading minus is applied as unary negation to the literal's value.
- **[1] output\_prediction** (rule type OP, evaluation / result rule): A legal int literal evaluates to the int value it denotes (2147483647 is int 2147483647; -2147483648 is int Integer.MIN\_VALUE); an out-of-range literal has no value because the program does not compile.
- **[2] one\_step\_execution** (rule type OS, state-transition rule): Evaluating a literal changes no variable and always yields the same int; in int x = 2147483647; the only state change is x receiving that value.

### L3: Relational / relations x function (concrete operational begins)

L3 for int literal limit: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

- **Edge:** `int_literal_limit` &rarr; `int_literal_limit@L3` (has_level)
- **Exact edge logic:** int literal limit -&gt; L3 (Relational): the answer relates the parts (3 ways).

Ways (3), each with its exact rule:

- **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): The general literal rule (a source-code representation of a value) is constrained here by int's range: a digit sequence outside -2147483648..2147483647 is not a valid int literal and must be written as a long literal with L.
- **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): The literal limit is exactly int's 32-bit range, but it is checked only for literals: the literal 2147483648 is a compile-time error, whereas the expression 2147483647 + 1 compiles and overflows at run time to -2147483648.
- **[2] purpose\_of\_the\_whole** (rule type P, plan / role rule): Used to write a fixed integer constant directly in code (Sajaniemi role: fixed value), including the extreme values; for the limits themselves the named constants Integer.MAX\_VALUE and Integer.MIN\_VALUE are clearer.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for int literal limit: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

- **Edge:** `int_literal_limit` &rarr; `int_literal_limit@L4` (has_level)
- **Exact edge logic:** int literal limit -&gt; L4 (Extended abstract): the answer reasons beyond the given code (3 ways).

Ways (3), each with its exact rule:

- **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `LargeIntegerLong`: Adding one digit or one unit can push a literal out of range (2147483647 compiles, 2147483648 does not), and adding a leading minus can bring it back (-2147483648 compiles); rewriting the literal as the expression 2147483647 + 1 compiles but silently wraps. Invariant: the range check is applied to literal tokens at compile time, never to computed values.
- **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Use a plain int literal for whole-number constants comfortably inside about plus or minus 2.1 billion; when values may reach ten digits use long with L-suffixed literals; for the extreme values use Integer.MAX\_VALUE and Integer.MIN\_VALUE rather than typing the digits.
- **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: An int literal must lie within the int range. Kind: compile-time. Trigger class: A digit sequence (without L) whose value exceeds 2147483647, or 2147483648 written without a leading minus, e.g. int big = 3000000000; (javac: integer number too large).

## Same topic

`int_literal_limit` belongs to the topic **Integers** (`topic1.2.c`). The topic also contains: `arithmetic_operators`, `int`, `integer_constants`, `integer_division`, `long_type`, `overflow`, `remainder_operator`.

## Rules of the concept (14)

- **Book** (SW-1e, p. 21 (pdf 31)): "(that, when interpreted as decimal numbers, fall within the defined range), are integer literal values."
- **Book** (SW-1.2, ): "The literal value 2147483648 (2^31) is permitted only as an operand of the unary minus operator, i.e., -2147483648."
- **E** (folk-meaning rule): Folk meaning: in maths any string of digits names a number, and a very large number simply 'becomes' a bigger kind of number. Java rule: a digit sequence without an L suffix is an int literal and must denote a value in -2147483648..2147483647; 2147483648 is legal only as the operand of unary minus (-2147483648), and 3000000000 does not compile (write 3000000000L).
- **M** (wrong rule / right rule): LargeIntegerLong: wrong: A large integer literal is automatically long. \| right: A digit sequence is an int literal only if its value lies within the int range; a larger literal such as 3000000000 is a compile-time error unless written with the L suffix (3000000000L), and the book advises the long type for values of ten digits or more.
- **T** (uneven-application rule): Points to LT (the compiler checks each literal's value against the int range when it reads the token, before any code runs). Applied unevenly: the student accepts one out-of-range literal as 'automatically long' but rejects another, or treats -2147483648 as illegal because 2147483648 alone is illegal, or expects the range check to apply to computed values such as 2147483647 + 1 (which compiles and wraps).
- **N** (identity rule): An int literal is a lexical constant: a source-code representation of an int value, written as decimal digits (optionally signed) whose value lies within the int range.
- **S** (declarative rule): A digit sequence is an int literal only when its decimal value lies between -2147483648 and 2147483647 inclusive; the magnitude 2147483648 may appear only as -2147483648; larger literals need the long suffix L.
- **LT** (operational sequencing rule): At compile time the compiler reads the digit token, converts it to a value and checks the range; at run time the literal is simply evaluated to that fixed value, and a leading minus is applied as unary negation to the literal's value.
- **OP** (evaluation / result rule): A legal int literal evaluates to the int value it denotes (2147483647 is int 2147483647; -2147483648 is int Integer.MIN\_VALUE); an out-of-range literal has no value because the program does not compile.
- **OS** (state-transition rule): Evaluating a literal changes no variable and always yields the same int; in int x = 2147483647; the only state change is x receiving that value.
- **R** (composition rule (with a neighbour)): with literal: The general literal rule (a source-code representation of a value) is constrained here by int's range: a digit sequence outside -2147483648..2147483647 is not a valid int literal and must be written as a long literal with L.
- **R** (composition rule (with a neighbour)): with int: The literal limit is exactly int's 32-bit range, but it is checked only for literals: the literal 2147483648 is a compile-time error, whereas the expression 2147483647 + 1 compiles and overflows at run time to -2147483648.
- **P** (plan / role rule): Used to write a fixed integer constant directly in code (Sajaniemi role: fixed value), including the extreme values; for the limits themselves the named constants Integer.MAX\_VALUE and Integer.MIN\_VALUE are clearer.
- **C** (conservation rule): Adding one digit or one unit can push a literal out of range (2147483647 compiles, 2147483648 does not), and adding a leading minus can bring it back (-2147483648 compiles); rewriting the literal as the expression 2147483647 + 1 compiles but silently wraps. Invariant: the range check is applied to literal tokens at compile time, never to computed values.
- **D** (error rule): rule broken: An int literal must lie within the int range. (compile-time)
- **X** (applicability rule): Use a plain int literal for whole-number constants comfortably inside about plus or minus 2.1 billion; when values may reach ten digits use long with L-suffixed literals; for the extreme values use Integer.MAX\_VALUE and Integer.MIN\_VALUE rather than typing the digits.

## How it is found in code and answers (reader block)

- **Aliases:** none
- **Code patterns:** `\b214748364[89]\b`, `\b9223372036854775808(?:L\b|\b)`
- **Operator symbols:** none
- **Java types:** none

## The whole prerequisite chain

- **Everything it builds on (4):** `data_type`, `int`, `literal`, `primitive_type`
- **Everything that builds on it (0):** nothing

## Every edge in this view and its exact edge logic (18)

All the edges drawn in the picture, in the order: prerequisite, parallel, misconception, error, has_level, contains.

**1. `int` &rarr; `int_literal_limit`** (prerequisite)

- **Exact edge logic:** The limit on int literals is int's 32-bit range, -2147483648 to 2147483647.
- **Grounding:** book\_passage
- **Composition rule (R) of `int` with `int_literal_limit`:** An int literal must lie in int's range, so larger digit strings need an L (long) literal.
- **Composition rule (R) of `int_literal_limit` with `int`:** The literal limit is exactly int's 32-bit range, but it is checked only for literals: the literal 2147483648 is a compile-time error, whereas the expression 2147483647 + 1 compiles and overflows at run time to -2147483648.

**2. `literal` &rarr; `int_literal_limit`** (prerequisite)

- **Exact edge logic:** An int literal is legal only if its value lies within the int range, so a digit sequence outside -2147483648..2147483647 is not a valid int literal.
- **Grounding:** book\_passage
- **Composition rule (R) of `literal` with `int_literal_limit`:** A literal without L must lie in -2147483648..2147483647, so 2147483648 alone is a compile error. Larger values need a long literal (2147483648L).
- **Composition rule (R) of `int_literal_limit` with `literal`:** The general literal rule (a source-code representation of a value) is constrained here by int's range: a digit sequence outside -2147483648..2147483647 is not a valid int literal and must be written as a long literal with L.

**3. `int_literal_limit` &rarr; `LargeIntegerLong`** (misconception)

- **Exact edge logic (the wrong rule):** a large integer literal is automatically long
- **Twin logic (the right rule):** A sequence of digits is an int literal only if its value falls within the int range; for larger values the book advises the long type.
- **Role:** context

**4. `literal` &rarr; `LargeIntegerLong`** (misconception)

- **Exact edge logic (the wrong rule):** A whole-number literal that is too big for an int automatically becomes a long.
- **Twin logic (the right rule):** A sequence of digits is an int literal only if its value falls within the int range; for larger values the book advises the long type.
- **Role:** primary

**5. `long_type` &rarr; `LargeIntegerLong`** (misconception)

- **Exact edge logic (the wrong rule):** a large integer literal is automatically long
- **Twin logic (the right rule):** A sequence of digits is an int literal only if its value falls within the int range; for larger values the book advises the long type.
- **Role:** context

**6. `int_literal_limit` &rarr; `int_literal_limit@L0`** (has_level)

- **Exact edge logic:** int literal limit -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (3 ways).
  - **[0] everyday\_reading** (rule type E, folk-meaning rule): Folk meaning: in maths any string of digits names a number, and a very large number simply 'becomes' a bigger kind of number. Java rule: a digit sequence without an L suffix is an int literal and must denote a value in -2147483648..2147483647; 2147483648 is legal only as the operand of unary minus (-2147483648), and 3000000000 does not compile (write 3000000000L).
  - **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `LargeIntegerLong`: wrong rule: A large integer literal is automatically long. Right rule: A digit sequence is an int literal only if its value lies within the int range; a larger literal such as 3000000000 is a compile-time error unless written with the L suffix (3000000000L), and the book advises the long type for values of ten digits or more.
  - **[2] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `LargeIntegerLong`: Points to LT (the compiler checks each literal's value against the int range when it reads the token, before any code runs). Applied unevenly: the student accepts one out-of-range literal as 'automatically long' but rejects another, or treats -2147483648 as illegal because 2147483648 alone is illegal, or expects the range check to apply to computed values such as 2147483647 + 1 (which compiles and wraps). (here mixing in: "a large integer literal is automatically long")

**7. `int_literal_limit` &rarr; `int_literal_limit@L1`** (has_level)

- **Exact edge logic:** int literal limit -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).
  - **[0] names\_the\_element** (rule type N, identity rule): An int literal is a lexical constant: a source-code representation of an int value, written as decimal digits (optionally signed) whose value lies within the int range.
  - **[1] states\_the\_rule** (rule type S, declarative rule): A digit sequence is an int literal only when its decimal value lies between -2147483648 and 2147483647 inclusive; the magnitude 2147483648 may appear only as -2147483648; larger literals need the long suffix L.

**8. `int_literal_limit` &rarr; `int_literal_limit@L2`** (has_level)

- **Exact edge logic:** int literal limit -&gt; L2 (Multistructural): the answer applies the rules of int literal limit to every part of the code, in order (3 ways).
  - **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): At compile time the compiler reads the digit token, converts it to a value and checks the range; at run time the literal is simply evaluated to that fixed value, and a leading minus is applied as unary negation to the literal's value.
  - **[1] output\_prediction** (rule type OP, evaluation / result rule): A legal int literal evaluates to the int value it denotes (2147483647 is int 2147483647; -2147483648 is int Integer.MIN\_VALUE); an out-of-range literal has no value because the program does not compile.
  - **[2] one\_step\_execution** (rule type OS, state-transition rule): Evaluating a literal changes no variable and always yields the same int; in int x = 2147483647; the only state change is x receiving that value.

**9. `int_literal_limit` &rarr; `int_literal_limit@L3`** (has_level)

- **Exact edge logic:** int literal limit -&gt; L3 (Relational): the answer relates the parts (3 ways).
  - **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): The general literal rule (a source-code representation of a value) is constrained here by int's range: a digit sequence outside -2147483648..2147483647 is not a valid int literal and must be written as a long literal with L.
  - **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): The literal limit is exactly int's 32-bit range, but it is checked only for literals: the literal 2147483648 is a compile-time error, whereas the expression 2147483647 + 1 compiles and overflows at run time to -2147483648.
  - **[2] purpose\_of\_the\_whole** (rule type P, plan / role rule): Used to write a fixed integer constant directly in code (Sajaniemi role: fixed value), including the extreme values; for the limits themselves the named constants Integer.MAX\_VALUE and Integer.MIN\_VALUE are clearer.

**10. `int_literal_limit` &rarr; `int_literal_limit@L4`** (has_level)

- **Exact edge logic:** int literal limit -&gt; L4 (Extended abstract): the answer reasons beyond the given code (3 ways).
  - **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `LargeIntegerLong`: Adding one digit or one unit can push a literal out of range (2147483647 compiles, 2147483648 does not), and adding a leading minus can bring it back (-2147483648 compiles); rewriting the literal as the expression 2147483647 + 1 compiles but silently wraps. Invariant: the range check is applied to literal tokens at compile time, never to computed values.
  - **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Use a plain int literal for whole-number constants comfortably inside about plus or minus 2.1 billion; when values may reach ten digits use long with L-suffixed literals; for the extreme values use Integer.MAX\_VALUE and Integer.MIN\_VALUE rather than typing the digits.
  - **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: An int literal must lie within the int range. Kind: compile-time. Trigger class: A digit sequence (without L) whose value exceeds 2147483647, or 2147483648 written without a leading minus, e.g. int big = 3000000000; (javac: integer number too large).

**11. `topic1.2.c` &rarr; `int_literal_limit`** (contains)

- topic `topic1.2.c` contains `int_literal_limit`

**12. `topic1.2.c` &rarr; `arithmetic_operators`** (contains)

- topic `topic1.2.c` contains `arithmetic_operators`

**13. `topic1.2.c` &rarr; `int`** (contains)

- topic `topic1.2.c` contains `int`

**14. `topic1.2.c` &rarr; `integer_constants`** (contains)

- topic `topic1.2.c` contains `integer_constants`

**15. `topic1.2.c` &rarr; `integer_division`** (contains)

- topic `topic1.2.c` contains `integer_division`

**16. `topic1.2.c` &rarr; `long_type`** (contains)

- topic `topic1.2.c` contains `long_type`

**17. `topic1.2.c` &rarr; `overflow`** (contains)

- topic `topic1.2.c` contains `overflow`

**18. `topic1.2.c` &rarr; `remainder_operator`** (contains)

- topic `topic1.2.c` contains `remainder_operator`
