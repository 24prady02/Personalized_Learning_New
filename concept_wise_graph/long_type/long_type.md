# long_type (`long_type`)

64-bit integer type for values beyond the int range

Section 1.2 Built-in Types of Data, topic 1.2.c Integers.

![The knowledge graph around long_type](long_type.png)

## At a glance

- **Needs first:** `int`
- **Leads to:** nothing
- **Learned alongside:** nothing
- **Misconceptions:** `LargeIntegerLong`
- **Errors:** none
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 17 edges around this concept. The edge logic, the wrong and right rules and the exact rules of the ways are copied word for word from the graph.

## To work on (0)

Nothing is missing for this concept.

## What it needs first (1)

A prerequisite edge means the other concept has to be understood before `long_type`.

### `int` comes before `long_type`

*32-bit integer primitive*

- **Edge:** `pre:int->long_type`
- **Exact edge logic:** long is the wider integer type used when int's range is too small.
- **Grounding:** book\_passage
- **Composition rule (R) of `long_type` with `int`:** long is the wider integer type: an int widens to long automatically, and mixing an int with a long in an operation gives a long.
- **Composition rule (R) of `int` with `long_type`:** If either operand is long, the operation is 64-bit and the result is long. Storing a long into an int needs a cast.

## What it leads to (0)

These concepts need `long_type` first.

No concept has this one as a prerequisite.

## Learned alongside (0)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

No parallel edge touches this concept.

## Misconceptions (1)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### LargeIntegerLong

- **Edge:** `long_type` &rarr; `LargeIntegerLong` (misconception)
- **Exact edge logic (the wrong rule):** a large integer literal is automatically long
- **Twin logic (the right rule):** A sequence of digits is an int literal only if its value falls within the int range; for larger values the book advises the long type.
- **Wrong belief (on the node):** a large integer literal is automatically long
- **Correct rule (on the node):** A sequence of digits is an int literal only if its value falls within the int range; for larger values the book advises the long type.
- **Provenance:** published
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [1] misconception, exact rule:** wrong rule: a large integer literal is automatically long. Right rule: A sequence of digits is an int literal only if its value falls within the int range; for larger values the book advises the long type.
- **L0 way [2] inconsistent\_trace, exact rule:** Points to LT (only operations with a long operand run in 64 bits). Applied unevenly, a student treats long x = a \* b (int a, b) as 64-bit because the target is long. (here mixing in: "a large integer literal is automatically long")
- **Edge `int_literal_limit` &rarr; `LargeIntegerLong`, exact edge logic:** a large integer literal is automatically long **Twin logic:** A sequence of digits is an int literal only if its value falls within the int range; for larger values the book advises the long type. (role: context)
- **Edge `literal` &rarr; `LargeIntegerLong`, exact edge logic:** A whole-number literal that is too big for an int automatically becomes a long. **Twin logic:** A sequence of digits is an int literal only if its value falls within the int range; for larger values the book advises the long type. (role: primary)

## Errors (0)

An error edge states the rule that gets broken in a program, and the right rule.

The graph has no error edge from this concept.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for long type: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to long type agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

- **Edge:** `long_type` &rarr; `long_type@L0` (has_level)
- **Exact edge logic:** long type -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (3 ways).

Ways (3), each with its exact rule:

- **[0] everyday\_reading** (rule type E, folk-meaning rule): In English 'long' just means lengthy, so novices expect any big number to become a long automatically. In Java long is a separate 64-bit type that must be declared, and an integer literal outside the int range needs the L suffix.
- **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `LargeIntegerLong`: wrong rule: a large integer literal is automatically long. Right rule: A sequence of digits is an int literal only if its value falls within the int range; for larger values the book advises the long type.
- **[2] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `LargeIntegerLong`: Points to LT (only operations with a long operand run in 64 bits). Applied unevenly, a student treats long x = a \* b (int a, b) as 64-bit because the target is long. (here mixing in: "a large integer literal is automatically long")

### L1: Unistructural / atom x text surface

L1 for long type: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

- **Edge:** `long_type` &rarr; `long_type@L1` (has_level)
- **Exact edge logic:** long type -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

Ways (2), each with its exact rule:

- **[0] names\_the\_element** (rule type N, identity rule): long: Java's 64-bit signed integer primitive type.
- **[1] states\_the\_rule** (rule type S, declarative rule): long ranges from -9223372036854775808 to 9223372036854775807, and its literals end in L. An integer operation with at least one long operand is done in 64 bits and gives a long. int widens to long automatically, but long to int needs a cast.

### L2: Multistructural / block x execution / preoperational

L2 for long type: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

- **Edge:** `long_type` &rarr; `long_type@L2` (has_level)
- **Exact edge logic:** long type -&gt; L2 (Multistructural): the answer applies the rules of long type to every part of the code, in order (3 ways).

Ways (3), each with its exact rule:

- **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): In a mixed expression each operation checks its own operands. Only operations with a long operand run in 64 bits, so pure-int subexpressions that came earlier were already computed in 32 bits.
- **[1] output\_prediction** (rule type OP, evaluation / result rule): 2147483647L + 1 is the long 2147483648. Math.round(3.14159) has type long and value 3.
- **[2] one\_step\_execution** (rule type OS, state-transition rule): Assigning to a long variable stores a 64-bit value. Storing a long in an int requires an (int) cast, which keeps only the low 32 bits.

### L3: Relational / relations x function (concrete operational begins)

L3 for long type: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

- **Edge:** `long_type` &rarr; `long_type@L3` (has_level)
- **Exact edge logic:** long type -&gt; L3 (Relational): the answer relates the parts (2 ways).

Ways (2), each with its exact rule:

- **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): long is the wider integer type: an int widens to long automatically, and mixing an int with a long in an operation gives a long.
- **[1] purpose\_of\_the\_whole** (rule type P, plan / role rule): long holds huge integers: counts or sums beyond 2 billion, factorials up to 20!, products of large ints, and times in milliseconds.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for long type: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

- **Edge:** `long_type` &rarr; `long_type@L4` (has_level)
- **Exact edge logic:** long type -&gt; L4 (Extended abstract): the answer reasons beyond the given code (5 ways).

Ways (5), each with its exact rule:

- **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `LargeIntegerLong`: Changing int to long removes overflow below about 9.2e18, but a literal product is still computed in int unless one operand is long (1000000 \* 1000000 overflows, while 1000000L \* 1000000 does not).
- **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Use long when integer values may reach ten digits or more, and int otherwise. Use BigInteger beyond long's range, and double for non-integers.
- **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: A long value needs an explicit cast to be stored in an int. Kind: compile-time. Trigger class: int r = Math.round(x); or int n = someLong;: 'possible lossy conversion from long to int'.
- **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: An integer literal outside the int range needs an L suffix. Kind: compile-time. Trigger class: long big = 3000000000;: 'integer number too large'.
- **[4] diagnose\_an\_error** (rule type D, error rule): rule broken: A long target does not make int operands 64-bit. Kind: silent logic error. Trigger class: long x = a \* b; with int a and b whose product exceeds the int range.

## Same topic

`long_type` belongs to the topic **Integers** (`topic1.2.c`). The topic also contains: `arithmetic_operators`, `int`, `int_literal_limit`, `integer_constants`, `integer_division`, `overflow`, `remainder_operator`.

## Rules of the concept (15)

- **Book** (SW-1e, p. 23 (pdf 33)): "The long, short, and byte types are the same as int except that they use 64, 16, and 8 bits respectively, so the range of allowed values is accordingly different."
- **Book** (SW-1.3, p. 85 (pdf 95)): "Use the long data type."
- **E** (folk-meaning rule): In English 'long' just means lengthy, so novices expect any big number to become a long automatically. In Java long is a separate 64-bit type that must be declared, and an integer literal outside the int range needs the L suffix.
- **M** (wrong rule / right rule): LargeIntegerLong: wrong: a large integer literal is automatically long \| right: A sequence of digits is an int literal only if its value falls within the int range; for larger values the book advises the long type.
- **T** (uneven-application rule): Points to LT (only operations with a long operand run in 64 bits). Applied unevenly, a student treats long x = a \* b (int a, b) as 64-bit because the target is long.
- **N** (identity rule): long: Java's 64-bit signed integer primitive type.
- **S** (declarative rule): long ranges from -9223372036854775808 to 9223372036854775807, and its literals end in L. An integer operation with at least one long operand is done in 64 bits and gives a long. int widens to long automatically, but long to int needs a cast.
- **LT** (operational sequencing rule): In a mixed expression each operation checks its own operands. Only operations with a long operand run in 64 bits, so pure-int subexpressions that came earlier were already computed in 32 bits.
- **OP** (evaluation / result rule): 2147483647L + 1 is the long 2147483648. Math.round(3.14159) has type long and value 3.
- **OS** (state-transition rule): Assigning to a long variable stores a 64-bit value. Storing a long in an int requires an (int) cast, which keeps only the low 32 bits.
- **R** (composition rule (with a neighbour)): with int: long is the wider integer type: an int widens to long automatically, and mixing an int with a long in an operation gives a long.
- **P** (plan / role rule): long holds huge integers: counts or sums beyond 2 billion, factorials up to 20!, products of large ints, and times in milliseconds.
- **C** (conservation rule): Changing int to long removes overflow below about 9.2e18, but a literal product is still computed in int unless one operand is long (1000000 \* 1000000 overflows, while 1000000L \* 1000000 does not).
- **D** (error rule): rule broken: A long value needs an explicit cast to be stored in an int. (compile-time)
- **D** (error rule): rule broken: An integer literal outside the int range needs an L suffix. (compile-time)
- **D** (error rule): rule broken: A long target does not make int operands 64-bit. (silent logic error)
- **X** (applicability rule): Use long when integer values may reach ten digits or more, and int otherwise. Use BigInteger beyond long's range, and double for non-integers.

## How it is found in code and answers (reader block)

- **Aliases:** long
- **Code patterns:** `\blong\b`
- **Operator symbols:** none
- **Java types:** `long`

## The whole prerequisite chain

- **Everything it builds on (3):** `data_type`, `int`, `primitive_type`
- **Everything that builds on it (0):** nothing

## Every edge in this view and its exact edge logic (17)

All the edges drawn in the picture, in the order: prerequisite, parallel, misconception, error, has_level, contains.

**1. `int` &rarr; `long_type`** (prerequisite)

- **Exact edge logic:** long is the wider integer type used when int's range is too small.
- **Grounding:** book\_passage
- **Composition rule (R) of `int` with `long_type`:** If either operand is long, the operation is 64-bit and the result is long. Storing a long into an int needs a cast.
- **Composition rule (R) of `long_type` with `int`:** long is the wider integer type: an int widens to long automatically, and mixing an int with a long in an operation gives a long.

**2. `long_type` &rarr; `LargeIntegerLong`** (misconception)

- **Exact edge logic (the wrong rule):** a large integer literal is automatically long
- **Twin logic (the right rule):** A sequence of digits is an int literal only if its value falls within the int range; for larger values the book advises the long type.
- **Role:** context

**3. `int_literal_limit` &rarr; `LargeIntegerLong`** (misconception)

- **Exact edge logic (the wrong rule):** a large integer literal is automatically long
- **Twin logic (the right rule):** A sequence of digits is an int literal only if its value falls within the int range; for larger values the book advises the long type.
- **Role:** context

**4. `literal` &rarr; `LargeIntegerLong`** (misconception)

- **Exact edge logic (the wrong rule):** A whole-number literal that is too big for an int automatically becomes a long.
- **Twin logic (the right rule):** A sequence of digits is an int literal only if its value falls within the int range; for larger values the book advises the long type.
- **Role:** primary

**5. `long_type` &rarr; `long_type@L0`** (has_level)

- **Exact edge logic:** long type -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (3 ways).
  - **[0] everyday\_reading** (rule type E, folk-meaning rule): In English 'long' just means lengthy, so novices expect any big number to become a long automatically. In Java long is a separate 64-bit type that must be declared, and an integer literal outside the int range needs the L suffix.
  - **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `LargeIntegerLong`: wrong rule: a large integer literal is automatically long. Right rule: A sequence of digits is an int literal only if its value falls within the int range; for larger values the book advises the long type.
  - **[2] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `LargeIntegerLong`: Points to LT (only operations with a long operand run in 64 bits). Applied unevenly, a student treats long x = a \* b (int a, b) as 64-bit because the target is long. (here mixing in: "a large integer literal is automatically long")

**6. `long_type` &rarr; `long_type@L1`** (has_level)

- **Exact edge logic:** long type -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).
  - **[0] names\_the\_element** (rule type N, identity rule): long: Java's 64-bit signed integer primitive type.
  - **[1] states\_the\_rule** (rule type S, declarative rule): long ranges from -9223372036854775808 to 9223372036854775807, and its literals end in L. An integer operation with at least one long operand is done in 64 bits and gives a long. int widens to long automatically, but long to int needs a cast.

**7. `long_type` &rarr; `long_type@L2`** (has_level)

- **Exact edge logic:** long type -&gt; L2 (Multistructural): the answer applies the rules of long type to every part of the code, in order (3 ways).
  - **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): In a mixed expression each operation checks its own operands. Only operations with a long operand run in 64 bits, so pure-int subexpressions that came earlier were already computed in 32 bits.
  - **[1] output\_prediction** (rule type OP, evaluation / result rule): 2147483647L + 1 is the long 2147483648. Math.round(3.14159) has type long and value 3.
  - **[2] one\_step\_execution** (rule type OS, state-transition rule): Assigning to a long variable stores a 64-bit value. Storing a long in an int requires an (int) cast, which keeps only the low 32 bits.

**8. `long_type` &rarr; `long_type@L3`** (has_level)

- **Exact edge logic:** long type -&gt; L3 (Relational): the answer relates the parts (2 ways).
  - **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): long is the wider integer type: an int widens to long automatically, and mixing an int with a long in an operation gives a long.
  - **[1] purpose\_of\_the\_whole** (rule type P, plan / role rule): long holds huge integers: counts or sums beyond 2 billion, factorials up to 20!, products of large ints, and times in milliseconds.

**9. `long_type` &rarr; `long_type@L4`** (has_level)

- **Exact edge logic:** long type -&gt; L4 (Extended abstract): the answer reasons beyond the given code (5 ways).
  - **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `LargeIntegerLong`: Changing int to long removes overflow below about 9.2e18, but a literal product is still computed in int unless one operand is long (1000000 \* 1000000 overflows, while 1000000L \* 1000000 does not).
  - **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Use long when integer values may reach ten digits or more, and int otherwise. Use BigInteger beyond long's range, and double for non-integers.
  - **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: A long value needs an explicit cast to be stored in an int. Kind: compile-time. Trigger class: int r = Math.round(x); or int n = someLong;: 'possible lossy conversion from long to int'.
  - **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: An integer literal outside the int range needs an L suffix. Kind: compile-time. Trigger class: long big = 3000000000;: 'integer number too large'.
  - **[4] diagnose\_an\_error** (rule type D, error rule): rule broken: A long target does not make int operands 64-bit. Kind: silent logic error. Trigger class: long x = a \* b; with int a and b whose product exceeds the int range.

**10. `topic1.2.c` &rarr; `long_type`** (contains)

- topic `topic1.2.c` contains `long_type`

**11. `topic1.2.c` &rarr; `arithmetic_operators`** (contains)

- topic `topic1.2.c` contains `arithmetic_operators`

**12. `topic1.2.c` &rarr; `int`** (contains)

- topic `topic1.2.c` contains `int`

**13. `topic1.2.c` &rarr; `int_literal_limit`** (contains)

- topic `topic1.2.c` contains `int_literal_limit`

**14. `topic1.2.c` &rarr; `integer_constants`** (contains)

- topic `topic1.2.c` contains `integer_constants`

**15. `topic1.2.c` &rarr; `integer_division`** (contains)

- topic `topic1.2.c` contains `integer_division`

**16. `topic1.2.c` &rarr; `overflow`** (contains)

- topic `topic1.2.c` contains `overflow`

**17. `topic1.2.c` &rarr; `remainder_operator`** (contains)

- topic `topic1.2.c` contains `remainder_operator`
