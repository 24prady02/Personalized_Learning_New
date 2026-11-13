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

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 18 edges around this concept, each explained in the graph's own words.

## What it needs first (2)

A prerequisite edge means the other concept has to be understood before `int_literal_limit`.

### `int` comes before `int_literal_limit`

*32-bit integer primitive*

The limit on int literals is int's 32-bit range, -2147483648 to 2147483647.

- **Grounding:** book passage
- **How `int_literal_limit` combines with `int`:** The literal limit is exactly int's 32-bit range, but it is checked only for literals: the literal 2147483648 is a compile-time error, whereas the expression 2147483647 + 1 compiles and overflows at run time to -2147483648.
- **How `int` combines with `int_literal_limit`:** An int literal must lie in int's range, so larger digit strings need an L (long) literal.

### `literal` comes before `int_literal_limit`

*a constant value written in code (42, 3.14, true, 'a', "hi")*

An int literal is legal only if its value lies within the int range, so a digit sequence outside -2147483648..2147483647 is not a valid int literal.

- **Grounding:** book passage
- **How `int_literal_limit` combines with `literal`:** The general literal rule (a source-code representation of a value) is constrained here by int's range: a digit sequence outside -2147483648..2147483647 is not a valid int literal and must be written as a long literal with L.
- **How `literal` combines with `int_literal_limit`:** A literal without L must lie in -2147483648..2147483647, so 2147483648 alone is a compile error. Larger values need a long literal (2147483648L).

## What it leads to (0)

These concepts need `int_literal_limit` first.

No concept has this one as a prerequisite.

## Learned alongside (0)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

No parallel edge touches this concept.

## Misconceptions (1)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### LargeIntegerLong

- **Wrong rule:** a large integer literal is automatically long
- **Right rule:** A sequence of digits is an int literal only if its value falls within the int range; for larger values the book advises the long type.
- **Role of this concept:** context
- **Shows at level L0 as:** misconception: wrong rule: A large integer literal is automatically long. Right rule: A digit sequence is an int literal only if its value lies within the int range; a larger literal such as 3000000000 is a compile-time error unless written with the L suffix (3000000000L), and the book advises the long type for values of ten digits or more.
- **Shows at level L0 as:** inconsistent trace: Points to LT (the compiler checks each literal's value against the int range when it reads the token, before any code runs). Applied unevenly: the student accepts one out-of-range literal as 'automatically long' but rejects another, or treats -2147483648 as illegal because 2147483648 alone is illegal, or expects the range check to apply to computed values such as 2147483647 + 1 (which compiles and wraps). (here mixing in: "a large integer literal is automatically long")
- **Also an edge from `literal`:** A whole-number literal that is too big for an int automatically becomes a long.
- **Also an edge from `long_type`:** a large integer literal is automatically long

## Errors (0)

An error edge states the rule that gets broken in a program, and the right rule.

The graph has no error edge from this concept.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for int literal limit: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to int literal limit agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

int literal limit -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (3 ways).

- **everyday reading** (folk-meaning rule): Folk meaning: in maths any string of digits names a number, and a very large number simply 'becomes' a bigger kind of number. Java rule: a digit sequence without an L suffix is an int literal and must denote a value in -2147483648..2147483647; 2147483648 is legal only as the operand of unary minus (-2147483648), and 3000000000 does not compile (write 3000000000L).
- **misconception** (wrong rule / right rule; shows `LargeIntegerLong`): wrong rule: A large integer literal is automatically long. Right rule: A digit sequence is an int literal only if its value lies within the int range; a larger literal such as 3000000000 is a compile-time error unless written with the L suffix (3000000000L), and the book advises the long type for values of ten digits or more.
- **inconsistent trace** (uneven-application rule; shows `LargeIntegerLong`): Points to LT (the compiler checks each literal's value against the int range when it reads the token, before any code runs). Applied unevenly: the student accepts one out-of-range literal as 'automatically long' but rejects another, or treats -2147483648 as illegal because 2147483648 alone is illegal, or expects the range check to apply to computed values such as 2147483647 + 1 (which compiles and wraps). (here mixing in: "a large integer literal is automatically long")

### L1: Unistructural / atom x text surface

L1 for int literal limit: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

int literal limit -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

- **names the element** (identity rule): An int literal is a lexical constant: a source-code representation of an int value, written as decimal digits (optionally signed) whose value lies within the int range.
- **states the rule** (declarative rule): A digit sequence is an int literal only when its decimal value lies between -2147483648 and 2147483647 inclusive; the magnitude 2147483648 may appear only as -2147483648; larger literals need the long suffix L.

### L2: Multistructural / block x execution / preoperational

L2 for int literal limit: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

int literal limit -&gt; L2 (Multistructural): the answer applies the rules of int literal limit to every part of the code, in order (3 ways).

- **line by line trace** (operational sequencing rule): At compile time the compiler reads the digit token, converts it to a value and checks the range; at run time the literal is simply evaluated to that fixed value, and a leading minus is applied as unary negation to the literal's value.
- **output prediction** (evaluation / result rule): A legal int literal evaluates to the int value it denotes (2147483647 is int 2147483647; -2147483648 is int Integer.MIN\_VALUE); an out-of-range literal has no value because the program does not compile.
- **one step execution** (state-transition rule): Evaluating a literal changes no variable and always yields the same int; in int x = 2147483647; the only state change is x receiving that value.

### L3: Relational / relations x function (concrete operational begins)

L3 for int literal limit: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

int literal limit -&gt; L3 (Relational): the answer relates the parts (3 ways).

- **relation to neighbour** (composition rule (with a neighbour)): The general literal rule (a source-code representation of a value) is constrained here by int's range: a digit sequence outside -2147483648..2147483647 is not a valid int literal and must be written as a long literal with L.
- **relation to neighbour** (composition rule (with a neighbour)): The literal limit is exactly int's 32-bit range, but it is checked only for literals: the literal 2147483648 is a compile-time error, whereas the expression 2147483647 + 1 compiles and overflows at run time to -2147483648.
- **purpose of the whole** (plan / role rule): Used to write a fixed integer constant directly in code (Sajaniemi role: fixed value), including the extreme values; for the limits themselves the named constants Integer.MAX\_VALUE and Integer.MIN\_VALUE are clearer.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for int literal limit: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

int literal limit -&gt; L4 (Extended abstract): the answer reasons beyond the given code (3 ways).

- **predict a change** (conservation rule; shows `LargeIntegerLong`): Adding one digit or one unit can push a literal out of range (2147483647 compiles, 2147483648 does not), and adding a leading minus can bring it back (-2147483648 compiles); rewriting the literal as the expression 2147483647 + 1 compiles but silently wraps. Invariant: the range check is applied to literal tokens at compile time, never to computed values.
- **transfer to a new program** (applicability rule): Use a plain int literal for whole-number constants comfortably inside about plus or minus 2.1 billion; when values may reach ten digits use long with L-suffixed literals; for the extreme values use Integer.MAX\_VALUE and Integer.MIN\_VALUE rather than typing the digits.
- **diagnose an error** (error rule): rule broken: An int literal must lie within the int range. Kind: compile-time. Trigger class: A digit sequence (without L) whose value exceeds 2147483647, or 2147483648 written without a leading minus, e.g. int big = 3000000000; (javac: integer number too large).

## Same topic

`int_literal_limit` belongs to the topic **Integers** (`topic1.2.c`). The topic also contains: `arithmetic_operators`, `int`, `integer_constants`, `integer_division`, `long_type`, `overflow`, `remainder_operator`.

## Rules of the concept (14)

- **folk-meaning rule:** Folk meaning: in maths any string of digits names a number, and a very large number simply 'becomes' a bigger kind of number. Java rule: a digit sequence without an L suffix is an int literal and must denote a value in -2147483648..2147483647; 2147483648 is legal only as the operand of unary minus (-2147483648), and 3000000000 does not compile (write 3000000000L).
- **wrong rule / right rule:** LargeIntegerLong: wrong: A large integer literal is automatically long. \| right: A digit sequence is an int literal only if its value lies within the int range; a larger literal such as 3000000000 is a compile-time error unless written with the L suffix (3000000000L), and the book advises the long type for values of ten digits or more.
- **uneven-application rule:** Points to LT (the compiler checks each literal's value against the int range when it reads the token, before any code runs). Applied unevenly: the student accepts one out-of-range literal as 'automatically long' but rejects another, or treats -2147483648 as illegal because 2147483648 alone is illegal, or expects the range check to apply to computed values such as 2147483647 + 1 (which compiles and wraps).
- **identity rule:** An int literal is a lexical constant: a source-code representation of an int value, written as decimal digits (optionally signed) whose value lies within the int range.
- **declarative rule:** A digit sequence is an int literal only when its decimal value lies between -2147483648 and 2147483647 inclusive; the magnitude 2147483648 may appear only as -2147483648; larger literals need the long suffix L.
- **operational sequencing rule:** At compile time the compiler reads the digit token, converts it to a value and checks the range; at run time the literal is simply evaluated to that fixed value, and a leading minus is applied as unary negation to the literal's value.
- **evaluation / result rule:** A legal int literal evaluates to the int value it denotes (2147483647 is int 2147483647; -2147483648 is int Integer.MIN\_VALUE); an out-of-range literal has no value because the program does not compile.
- **state-transition rule:** Evaluating a literal changes no variable and always yields the same int; in int x = 2147483647; the only state change is x receiving that value.
- **composition rule (with a neighbour):** with literal: The general literal rule (a source-code representation of a value) is constrained here by int's range: a digit sequence outside -2147483648..2147483647 is not a valid int literal and must be written as a long literal with L.
- **composition rule (with a neighbour):** with int: The literal limit is exactly int's 32-bit range, but it is checked only for literals: the literal 2147483648 is a compile-time error, whereas the expression 2147483647 + 1 compiles and overflows at run time to -2147483648.
- **plan / role rule:** Used to write a fixed integer constant directly in code (Sajaniemi role: fixed value), including the extreme values; for the limits themselves the named constants Integer.MAX\_VALUE and Integer.MIN\_VALUE are clearer.
- **conservation rule:** Adding one digit or one unit can push a literal out of range (2147483647 compiles, 2147483648 does not), and adding a leading minus can bring it back (-2147483648 compiles); rewriting the literal as the expression 2147483647 + 1 compiles but silently wraps. Invariant: the range check is applied to literal tokens at compile time, never to computed values.
- **error rule:** rule broken: An int literal must lie within the int range. (compile-time)
- **applicability rule:** Use a plain int literal for whole-number constants comfortably inside about plus or minus 2.1 billion; when values may reach ten digits use long with L-suffixed literals; for the extreme values use Integer.MAX\_VALUE and Integer.MIN\_VALUE rather than typing the digits.

## The whole prerequisite chain

- **Everything it builds on (4):** `data_type`, `int`, `literal`, `primitive_type`
- **Everything that builds on it (0):** nothing
