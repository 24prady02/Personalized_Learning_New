# widening_conversion (`widening_conversion`)

automatic conversion to a type with a larger range

Section 1.2 Built-in Types of Data, topic 1.2.h Type conversion (automatic, cast, parsing).

![The knowledge graph around widening_conversion](widening_conversion.png)

## At a glance

- **Needs first:** `type_conversion`
- **Leads to:** nothing
- **Learned alongside:** `explicit_cast`
- **Misconceptions:** `NarrowingAssignmentAllowed`, `NoCastIfSameSize`
- **Errors:** none
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 16 edges around this concept. The edge logic, the wrong and right rules and the exact rules of the ways are copied word for word from the graph.

## To work on (0)

Nothing is missing for this concept.

## What it needs first (1)

A prerequisite edge means the other concept has to be understood before `widening_conversion`.

### `type_conversion` comes before `widening_conversion`

*implicit widening and explicit (cast)*

- **Edge:** `pre:type_conversion->widening_conversion`
- **Exact edge logic:** Widening is the automatic kind of type conversion.
- **Grounding:** book\_passage
- **Composition rule (R) of `widening_conversion` with `type_conversion`:** Widening is the automatic branch of type conversion; every other direction needs an explicit cast or method.
- **Composition rule (R) of `type_conversion` with `widening_conversion`:** Widening (promotion) is the automatic kind of conversion, applied at operators and assignments when the target type has a larger range.

## What it leads to (0)

These concepts need `widening_conversion` first.

No concept has this one as a prerequisite.

## Learned alongside (1)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

### `widening_conversion` alongside `explicit_cast`

*(int) x -- converts between numeric types, truncating toward zero*

- **Edge:** `par:widening_conversion~explicit_cast`
- **Exact edge logic:** Widening (promotion) happens automatically when a value goes to a type with a larger range (int to double) and loses nothing; a narrowing conversion (double to int) is never automatic and needs an explicit cast, which truncates toward zero.
- **Grounding:** book\_passage

## Misconceptions (2)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### NarrowingAssignmentAllowed

- **Edge:** `widening_conversion` &rarr; `NarrowingAssignmentAllowed` (misconception)
- **Exact edge logic (the wrong rule):** A double value can be stored in an int variable like an int in a double.
- **Twin logic (the right rule):** int to double is automatic; double to int needs a cast.
- **Wrong belief (on the node):** A double value can be stored in an int variable like an int in a double.
- **Correct rule (on the node):** int to double is automatic; double to int needs a cast.
- **Provenance:** textbook
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [2] misconception, exact rule:** wrong rule: A double value can be stored in an int variable like an int in a double. Right rule: int to double is automatic (widening); double to int needs a cast, otherwise the assignment is a compile-time error.
- **Edge `type_conversion` &rarr; `NarrowingAssignmentAllowed`, exact edge logic:** A double value can be stored in an int variable like an int in a double. **Twin logic:** int to double is automatic; double to int needs a cast. (role: context)

### NoCastIfSameSize

- **Edge:** `widening_conversion` &rarr; `NoCastIfSameSize` (misconception)
- **Exact edge logic (the wrong rule):** If a variable is at least as big as a value, no cast is needed to assign the value.
- **Twin logic (the right rule):** Assigning a double to an int needs a cast even when the value would fit, because a conversion that might involve loss of information leads to a compile-time error.
- **Wrong belief (on the node):** If a variable is at least as big as a value, no cast is needed to assign the value.
- **Correct rule (on the node):** Assigning a double to an int needs a cast even when the value would fit, because a conversion that might involve loss of information leads to a compile-time error.
- **Provenance:** published
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [1] misconception, exact rule:** wrong rule: If a variable is at least as big as a value, no cast is needed to assign the value. Right rule: The compiler decides by types, not values: assigning a double to an int needs a cast even when the value (e.g. 3.0) would fit, because a conversion that might involve loss of information leads to a compile-time error.
- **L0 way [3] inconsistent\_trace, exact rule:** Points to LT (promotion happens at each operator, at the moment an int operand meets a double). Applied unevenly: the student promotes the whole expression up front on one line (so b\*b - 4\*c is done in double) but per operator on another. (here mixing in: "If a variable is at least as big as a value, no cast is needed to assign the value")
- **Edge `type_conversion` &rarr; `NoCastIfSameSize`, exact edge logic:** If a variable is at least as big as a value, no cast is needed to assign the value. **Twin logic:** Assigning a double to an int needs a cast even when the value would fit, because a conversion that might involve loss of information leads to a compile-time error. (role: primary)

## Errors (0)

An error edge states the rule that gets broken in a program, and the right rule.

The graph has no error edge from this concept.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for widening conversion: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to widening conversion agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

- **Edge:** `widening_conversion` &rarr; `widening_conversion@L0` (has_level)
- **Exact edge logic:** widening conversion -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (4 ways).

Ways (4), each with its exact rule:

- **[0] everyday\_reading** (rule type E, folk-meaning rule): Folk meaning: like containers, a bigger box holds a smaller thing, and a smaller box holds a big thing if it happens to fit (3.0 fits in an int). Java rule: the compiler decides by types, not values: int to long or double is automatic, but double to int is never automatic, even for 3.0.
- **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `NoCastIfSameSize`: wrong rule: If a variable is at least as big as a value, no cast is needed to assign the value. Right rule: The compiler decides by types, not values: assigning a double to an int needs a cast even when the value (e.g. 3.0) would fit, because a conversion that might involve loss of information leads to a compile-time error.
- **[2] misconception** (rule type M, wrong rule / right rule) &rarr; `NarrowingAssignmentAllowed`: wrong rule: A double value can be stored in an int variable like an int in a double. Right rule: int to double is automatic (widening); double to int needs a cast, otherwise the assignment is a compile-time error.
- **[3] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `NoCastIfSameSize`: Points to LT (promotion happens at each operator, at the moment an int operand meets a double). Applied unevenly: the student promotes the whole expression up front on one line (so b\*b - 4\*c is done in double) but per operator on another. (here mixing in: "If a variable is at least as big as a value, no cast is needed to assign the value")

### L1: Unistructural / atom x text surface

L1 for widening conversion: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

- **Edge:** `widening_conversion` &rarr; `widening_conversion@L1` (has_level)
- **Exact edge logic:** widening conversion -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

Ways (2), each with its exact rule:

- **[0] names\_the\_element** (rule type N, identity rule): Widening conversion (promotion) is the automatic conversion of a value to a type with a larger range, e.g. int to long or double, char to int.
- **[1] states\_the\_rule** (rule type S, declarative rule): A value of a numeric type can be used wherever a type with a larger range is expected and is converted automatically; the magnitude is preserved (int to double is exact), though long to double may lose low-order precision.

### L2: Multistructural / block x execution / preoperational

L2 for widening conversion: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

- **Edge:** `widening_conversion` &rarr; `widening_conversion@L2` (has_level)
- **Exact edge logic:** widening conversion -&gt; L2 (Multistructural): the answer applies the rules of widening conversion to every part of the code, in order (3 ways).

Ways (3), each with its exact rule:

- **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): At a binary operator, if one operand is double the other is widened to double just before that operation; in an assignment or method argument, the value is widened to the target type after it has been computed.
- **[1] output\_prediction** (rule type OP, evaluation / result rule): The widened value has the larger type and the same magnitude: double d = 5; gives 5.0; 11 \* 0.3 is double 3.3; 'a' + 1 is int 98; (x &lt; 3.1) with int x = 3 is true.
- **[2] one\_step\_execution** (rule type OS, state-transition rule): Widening creates the converted value for the target; the source variable keeps its type and value (after double d = n; n is still an int).

### L3: Relational / relations x function (concrete operational begins)

L3 for widening conversion: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

- **Edge:** `widening_conversion` &rarr; `widening_conversion@L3` (has_level)
- **Exact edge logic:** widening conversion -&gt; L3 (Relational): the answer relates the parts (3 ways).

Ways (3), each with its exact rule:

- **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Widening is the automatic branch of type conversion; every other direction needs an explicit cast or method.
- **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Widening (promotion) happens automatically when a value goes to a type with a larger range (int to double) and loses nothing; a narrowing conversion (double to int) is never automatic and needs an explicit cast, which truncates toward zero.
- **[2] purpose\_of\_the\_whole** (rule type P, plan / role rule): Lets int data feed double formulas and library methods without explicit casts, e.g. Math.sqrt(25) or an int count in a double expression.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for widening conversion: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

- **Edge:** `widening_conversion` &rarr; `widening_conversion@L4` (has_level)
- **Exact edge logic:** widening conversion -&gt; L4 (Extended abstract): the answer reasons beyond the given code (4 ways).

Ways (4), each with its exact rule:

- **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `NoCastIfSameSize`: Widening an int to double and casting back restores the original int (reversible); widening a large long to double may not be reversible; widening an int quotient after the division cannot restore the lost fraction.
- **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Rely on widening when mixing int and double in formulas or passing ints to double methods; do not expect it to fix an int division already performed; when a narrowing is intended, write the cast explicitly.
- **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: Only widening is automatic; narrowing needs a cast. Kind: compile-time. Trigger class: A double (or long) value assigned or passed where an int is expected.
- **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: Widening applies to the value after the operation that produced it. Kind: silent logic error. Trigger class: Expecting double d = a / b; with int a, b to keep the fraction (gives the truncated quotient as a double).

## Same topic

`widening_conversion` belongs to the topic **Type conversion (automatic, cast, parsing)** (`topic1.2.h`). The topic also contains: `explicit_cast`, `parsing`, `string_conversion`, `type_conversion`.

## Rules of the concept (15)

- **Book** (SW-1e, p. 32 (pdf 42)): "You can use data of any primitive numeric type where a value whose type has a larger range of values is expected, because Java automatically converts to the type with the larger range."
- **Book** (SW-1.2, ): "For primitive numeric types, the system automatically performs type conversion when we use a value whose type has a larger range of values than expected."
- **E** (folk-meaning rule): Folk meaning: like containers, a bigger box holds a smaller thing, and a smaller box holds a big thing if it happens to fit (3.0 fits in an int). Java rule: the compiler decides by types, not values: int to long or double is automatic, but double to int is never automatic, even for 3.0.
- **M** (wrong rule / right rule): NarrowingAssignmentAllowed: wrong: A double value can be stored in an int variable like an int in a double. \| right: int to double is automatic (widening); double to int needs a cast, otherwise the assignment is a compile-time error.
- **M** (wrong rule / right rule): NoCastIfSameSize: wrong: If a variable is at least as big as a value, no cast is needed to assign the value. \| right: The compiler decides by types, not values: assigning a double to an int needs a cast even when the value (e.g. 3.0) would fit, because a conversion that might involve loss of information leads to a compile-time error.
- **T** (uneven-application rule): Points to LT (promotion happens at each operator, at the moment an int operand meets a double). Applied unevenly: the student promotes the whole expression up front on one line (so b\*b - 4\*c is done in double) but per operator on another.
- **N** (identity rule): Widening conversion (promotion) is the automatic conversion of a value to a type with a larger range, e.g. int to long or double, char to int.
- **S** (declarative rule): A value of a numeric type can be used wherever a type with a larger range is expected and is converted automatically; the magnitude is preserved (int to double is exact), though long to double may lose low-order precision.
- **LT** (operational sequencing rule): At a binary operator, if one operand is double the other is widened to double just before that operation; in an assignment or method argument, the value is widened to the target type after it has been computed.
- **OP** (evaluation / result rule): The widened value has the larger type and the same magnitude: double d = 5; gives 5.0; 11 \* 0.3 is double 3.3; 'a' + 1 is int 98; (x &lt; 3.1) with int x = 3 is true.
- **OS** (state-transition rule): Widening creates the converted value for the target; the source variable keeps its type and value (after double d = n; n is still an int).
- **R** (composition rule (with a neighbour)): with type\_conversion: Widening is the automatic branch of type conversion; every other direction needs an explicit cast or method.
- **P** (plan / role rule): Lets int data feed double formulas and library methods without explicit casts, e.g. Math.sqrt(25) or an int count in a double expression.
- **C** (conservation rule): Widening an int to double and casting back restores the original int (reversible); widening a large long to double may not be reversible; widening an int quotient after the division cannot restore the lost fraction.
- **D** (error rule): rule broken: Only widening is automatic; narrowing needs a cast. (compile-time)
- **D** (error rule): rule broken: Widening applies to the value after the operation that produced it. (silent logic error)
- **X** (applicability rule): Rely on widening when mixing int and double in formulas or passing ints to double methods; do not expect it to fix an int division already performed; when a narrowing is intended, write the cast explicitly.

## How it is found in code and answers (reader block)

- **Aliases:** widening, promotion, promoted
- **Code patterns:** `\b(?:double|float|long)\s+\w+\s*=\s*-?\d+\s*;`, `\bdouble\s+\w+\s*=\s*[^;.]*\b[a-z]\w*\s*[*/+\-]\s*\d+\.\d`, `(?<![\d.])\d+\s*[*/+\-]\s*\d+\.\d`
- **Operator symbols:** none
- **Java types:** none
- **Signal int\_into\_double** (scope program, decisive): `\b(?:int|long)\s+(?:[A-Za-z_]\w*\s*(?:=[^,;]*)?,\s*){0,8}(?P<a>[A-Za-z_]\w*)\s*(?:=[^,;]*)?[,;][\s\S]{0,4000}?\b(?:double|float|long)(?:\s*\[\s*\])?\s+(?P<d>[A-Za-z_]\w*)(?:[\s\S]{0,4000}?\b(?P=d))?(?:\s*\[[^\]]+\])?\s*=(?![ \t]*\(\s*(?:double|float)\s*\))[^;]*\b(?P=a)\b[^;]*;`

## The whole prerequisite chain

- **Everything it builds on (8):** `class_declaration`, `command_line_args`, `data_type`, `main_method`, `parsing`, `primitive_type`, `program_text`, `type_conversion`
- **Everything that builds on it (0):** nothing

## Every edge in this view and its exact edge logic (16)

All the edges drawn in the picture, in the order: prerequisite, parallel, misconception, error, has_level, contains.

**1. `type_conversion` &rarr; `widening_conversion`** (prerequisite)

- **Exact edge logic:** Widening is the automatic kind of type conversion.
- **Grounding:** book\_passage
- **Composition rule (R) of `type_conversion` with `widening_conversion`:** Widening (promotion) is the automatic kind of conversion, applied at operators and assignments when the target type has a larger range.
- **Composition rule (R) of `widening_conversion` with `type_conversion`:** Widening is the automatic branch of type conversion; every other direction needs an explicit cast or method.

**2. `widening_conversion` &harr; `explicit_cast`** (parallel)

- **Exact edge logic:** Widening (promotion) happens automatically when a value goes to a type with a larger range (int to double) and loses nothing; a narrowing conversion (double to int) is never automatic and needs an explicit cast, which truncates toward zero.
- **Grounding:** book\_passage

**3. `widening_conversion` &rarr; `NarrowingAssignmentAllowed`** (misconception)

- **Exact edge logic (the wrong rule):** A double value can be stored in an int variable like an int in a double.
- **Twin logic (the right rule):** int to double is automatic; double to int needs a cast.
- **Role:** primary

**4. `widening_conversion` &rarr; `NoCastIfSameSize`** (misconception)

- **Exact edge logic (the wrong rule):** If a variable is at least as big as a value, no cast is needed to assign the value.
- **Twin logic (the right rule):** Assigning a double to an int needs a cast even when the value would fit, because a conversion that might involve loss of information leads to a compile-time error.
- **Role:** context

**5. `type_conversion` &rarr; `NarrowingAssignmentAllowed`** (misconception)

- **Exact edge logic (the wrong rule):** A double value can be stored in an int variable like an int in a double.
- **Twin logic (the right rule):** int to double is automatic; double to int needs a cast.
- **Role:** context

**6. `type_conversion` &rarr; `NoCastIfSameSize`** (misconception)

- **Exact edge logic (the wrong rule):** If a variable is at least as big as a value, no cast is needed to assign the value.
- **Twin logic (the right rule):** Assigning a double to an int needs a cast even when the value would fit, because a conversion that might involve loss of information leads to a compile-time error.
- **Role:** primary

**7. `widening_conversion` &rarr; `widening_conversion@L0`** (has_level)

- **Exact edge logic:** widening conversion -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (4 ways).
  - **[0] everyday\_reading** (rule type E, folk-meaning rule): Folk meaning: like containers, a bigger box holds a smaller thing, and a smaller box holds a big thing if it happens to fit (3.0 fits in an int). Java rule: the compiler decides by types, not values: int to long or double is automatic, but double to int is never automatic, even for 3.0.
  - **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `NoCastIfSameSize`: wrong rule: If a variable is at least as big as a value, no cast is needed to assign the value. Right rule: The compiler decides by types, not values: assigning a double to an int needs a cast even when the value (e.g. 3.0) would fit, because a conversion that might involve loss of information leads to a compile-time error.
  - **[2] misconception** (rule type M, wrong rule / right rule) &rarr; `NarrowingAssignmentAllowed`: wrong rule: A double value can be stored in an int variable like an int in a double. Right rule: int to double is automatic (widening); double to int needs a cast, otherwise the assignment is a compile-time error.
  - **[3] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `NoCastIfSameSize`: Points to LT (promotion happens at each operator, at the moment an int operand meets a double). Applied unevenly: the student promotes the whole expression up front on one line (so b\*b - 4\*c is done in double) but per operator on another. (here mixing in: "If a variable is at least as big as a value, no cast is needed to assign the value")

**8. `widening_conversion` &rarr; `widening_conversion@L1`** (has_level)

- **Exact edge logic:** widening conversion -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).
  - **[0] names\_the\_element** (rule type N, identity rule): Widening conversion (promotion) is the automatic conversion of a value to a type with a larger range, e.g. int to long or double, char to int.
  - **[1] states\_the\_rule** (rule type S, declarative rule): A value of a numeric type can be used wherever a type with a larger range is expected and is converted automatically; the magnitude is preserved (int to double is exact), though long to double may lose low-order precision.

**9. `widening_conversion` &rarr; `widening_conversion@L2`** (has_level)

- **Exact edge logic:** widening conversion -&gt; L2 (Multistructural): the answer applies the rules of widening conversion to every part of the code, in order (3 ways).
  - **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): At a binary operator, if one operand is double the other is widened to double just before that operation; in an assignment or method argument, the value is widened to the target type after it has been computed.
  - **[1] output\_prediction** (rule type OP, evaluation / result rule): The widened value has the larger type and the same magnitude: double d = 5; gives 5.0; 11 \* 0.3 is double 3.3; 'a' + 1 is int 98; (x &lt; 3.1) with int x = 3 is true.
  - **[2] one\_step\_execution** (rule type OS, state-transition rule): Widening creates the converted value for the target; the source variable keeps its type and value (after double d = n; n is still an int).

**10. `widening_conversion` &rarr; `widening_conversion@L3`** (has_level)

- **Exact edge logic:** widening conversion -&gt; L3 (Relational): the answer relates the parts (3 ways).
  - **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Widening is the automatic branch of type conversion; every other direction needs an explicit cast or method.
  - **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Widening (promotion) happens automatically when a value goes to a type with a larger range (int to double) and loses nothing; a narrowing conversion (double to int) is never automatic and needs an explicit cast, which truncates toward zero.
  - **[2] purpose\_of\_the\_whole** (rule type P, plan / role rule): Lets int data feed double formulas and library methods without explicit casts, e.g. Math.sqrt(25) or an int count in a double expression.

**11. `widening_conversion` &rarr; `widening_conversion@L4`** (has_level)

- **Exact edge logic:** widening conversion -&gt; L4 (Extended abstract): the answer reasons beyond the given code (4 ways).
  - **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `NoCastIfSameSize`: Widening an int to double and casting back restores the original int (reversible); widening a large long to double may not be reversible; widening an int quotient after the division cannot restore the lost fraction.
  - **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Rely on widening when mixing int and double in formulas or passing ints to double methods; do not expect it to fix an int division already performed; when a narrowing is intended, write the cast explicitly.
  - **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: Only widening is automatic; narrowing needs a cast. Kind: compile-time. Trigger class: A double (or long) value assigned or passed where an int is expected.
  - **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: Widening applies to the value after the operation that produced it. Kind: silent logic error. Trigger class: Expecting double d = a / b; with int a, b to keep the fraction (gives the truncated quotient as a double).

**12. `topic1.2.h` &rarr; `widening_conversion`** (contains)

- topic `topic1.2.h` contains `widening_conversion`

**13. `topic1.2.h` &rarr; `explicit_cast`** (contains)

- topic `topic1.2.h` contains `explicit_cast`

**14. `topic1.2.h` &rarr; `parsing`** (contains)

- topic `topic1.2.h` contains `parsing`

**15. `topic1.2.h` &rarr; `string_conversion`** (contains)

- topic `topic1.2.h` contains `string_conversion`

**16. `topic1.2.h` &rarr; `type_conversion`** (contains)

- topic `topic1.2.h` contains `type_conversion`
