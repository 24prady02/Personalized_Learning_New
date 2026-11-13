# explicit_cast (`explicit_cast`)

(int) x -- converts between numeric types, truncating toward zero

Section 1.2 Built-in Types of Data, topic 1.2.h Type conversion (automatic, cast, parsing).

![The knowledge graph around explicit_cast](explicit_cast.png)

## At a glance

- **Needs first:** `integer_division`, `type_conversion`
- **Leads to:** `compound_assignment`, `math_random`
- **Learned alongside:** `math_round`, `widening_conversion`
- **Misconceptions:** `CastAfterIntDivision`, `CastAppliesToWholeExpression`, `CastParsesString`, `CastRounds`, `LaterDoubleLiteralFixesDivision`
- **Errors:** `RoundReturnsInt`
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 29 edges around this concept. The edge logic, the wrong and right rules and the exact rules of the ways are copied word for word from the graph.

## To work on (0)

Nothing is missing for this concept.

## What it needs first (2)

A prerequisite edge means the other concept has to be understood before `explicit_cast`.

### `integer_division` comes before `explicit_cast`

*/ on two ints truncates; % is the remainder*

- **Edge:** `pre:integer_division->explicit_cast`
- **Exact edge logic:** To divide two ints and keep the fraction, one operand is cast to double before the division, as in (double) freq[i] / T; casting the finished quotient comes too late.
- **Grounding:** book\_passage

### `type_conversion` comes before `explicit_cast`

*implicit widening and explicit (cast)*

- **Edge:** `pre:type_conversion->explicit_cast`
- **Exact edge logic:** A cast is the explicit form of type conversion between primitive types, required when the conversion may lose information (e.g. (int) 2.71828 is 2).
- **Grounding:** book\_passage
- **Composition rule (R) of `explicit_cast` with `type_conversion`:** A cast is the explicit conversion between primitive types, needed exactly where automatic conversion is refused because information may be lost.
- **Composition rule (R) of `type_conversion` with `explicit_cast`:** A cast is the explicit conversion between primitive types, required when information may be lost: (int) 2.71828 is 2.

## What it leads to (2)

These concepts need `explicit_cast` first.

### `explicit_cast` comes before `compound_assignment`

*x += e, x -= e, ... include a hidden cast*

- **Edge:** `pre:explicit_cast->compound_assignment`
- **Exact edge logic:** x op= e means x = (T)(x op e), where T is the type of x, so the result is cast back to the type of x.
- **Grounding:** questionable
- **Composition rule (R) of `explicit_cast` with `compound_assignment`:** x op= e contains an implicit cast back to the type of x, so with int x, x += 0.5 compiles (x = (int) (x + 0.5)) while x = x + 0.5 is a compile-time error.
- **Composition rule (R) of `compound_assignment` with `explicit_cast`:** x op= e includes a hidden narrowing cast to the type of x: with int x = 1, x += 1.7 compiles (as x = (int)(x + 1.7), giving 2) while x = x + 1.7 does not.

### `explicit_cast` comes before `math_random`

*Math.random() and scaling to an int range*

- **Edge:** `pre:explicit_cast->math_random`
- **Exact edge logic:** To turn Math.random()'s double in [0, 1) into a random int from 0 to N-1, multiply it by N and cast the result to int.
- **Grounding:** book\_passage
- **Composition rule (R) of `explicit_cast` with `math_random`:** To turn Math.random()'s double into a random int from 0 to N-1, the cast must enclose the product: (int) (Math.random() \* N); casting first gives 0.
- **Composition rule (R) of `math_random` with `explicit_cast`:** Converting to a random int requires the cast to apply to the whole product: (int) (Math.random() \* N); (int) Math.random() \* N casts first and is always 0.

## Learned alongside (2)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

### `explicit_cast` alongside `math_round`

*Math.round rounds to the nearest integer and returns a long*

- **Edge:** `par:math_round~explicit_cast`
- **Exact edge logic:** (int) 2.71828 truncates toward zero and gives 2; Math.round(2.71828) rounds to the nearest integer and gives 3, as a long that needs (int) to become an int.
- **Grounding:** book\_passage

### `explicit_cast` alongside `widening_conversion`

*automatic conversion to a type with a larger range*

- **Edge:** `par:widening_conversion~explicit_cast`
- **Exact edge logic:** Widening (promotion) happens automatically when a value goes to a type with a larger range (int to double) and loses nothing; a narrowing conversion (double to int) is never automatic and needs an explicit cast, which truncates toward zero.
- **Grounding:** book\_passage

## Misconceptions (5)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### CastAfterIntDivision

- **Edge:** `explicit_cast` &rarr; `CastAfterIntDivision` (misconception)
- **Exact edge logic (the wrong rule):** (double) (3 / 5) is 0.6.
- **Twin logic (the right rule):** The integer division 3 / 5 = 0 happens before the cast, so the result is 0.0.
- **Wrong belief (on the node):** (double) (3 / 5) is 0.6.
- **Correct rule (on the node):** The integer division 3 / 5 = 0 happens before the cast, so the result is 0.0.
- **Provenance:** textbook
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [2] misconception, exact rule:** wrong rule: (double) (3 / 5) is 0.6. Right rule: The integer division 3 / 5 = 0 happens inside the parentheses before the cast, so the result is 0.0; write (double) 3 / 5 to get 0.6.
- **Edge `integer_division` &rarr; `CastAfterIntDivision`, exact edge logic:** (double) (3 / 5) is 0.6. **Twin logic:** The integer division 3 / 5 = 0 happens before the cast, so the result is 0.0. (role: context)

### CastAppliesToWholeExpression

- **Edge:** `explicit_cast` &rarr; `CastAppliesToWholeExpression` (misconception)
- **Exact edge logic (the wrong rule):** (int) 2.5 / 0.15 casts the whole quotient to int.
- **Twin logic (the right rule):** The cast applies only to what comes right after it, here 2.5.
- **Wrong belief (on the node):** (int) 2.5 / 0.15 casts the whole quotient to int.
- **Correct rule (on the node):** The cast applies only to what comes right after it, here 2.5.
- **Provenance:** textbook
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [3] misconception, exact rule:** wrong rule: (int) 2.5 / 0.15 casts the whole quotient to int. Right rule: The cast applies only to what comes right after it, here 2.5, so the expression is 2 / 0.15 (a double); write (int) (2.5 / 0.15) to cast the quotient.
- **Edge `operator_precedence` &rarr; `CastAppliesToWholeExpression`, exact edge logic:** (int) 2.5 / 0.15 casts the whole quotient to int. **Twin logic:** The cast applies only to what comes right after it, here 2.5. (role: context)

### CastParsesString

- **Edge:** `explicit_cast` &rarr; `CastParsesString` (misconception)
- **Exact edge logic (the wrong rule):** (int) args[0] converts the text "34" into the number 34.
- **Twin logic (the right rule):** A String argument that represents a number must be converted with a method such as Integer.parseInt.
- **Wrong belief (on the node):** (int) args[0] converts the text "34" into the number 34.
- **Correct rule (on the node):** A String argument that represents a number must be converted with a method such as Integer.parseInt.
- **Provenance:** derived
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [5] misconception, exact rule:** wrong rule: (int) args[0] converts the text "34" into the number 34. Right rule: A cast cannot convert a String; a String argument that represents a number must be converted with a method such as Integer.parseInt.
- **Edge `parsing` &rarr; `CastParsesString`, exact edge logic:** (int) args[0] converts the text "34" into the number 34. **Twin logic:** A String argument that represents a number must be converted with a method such as Integer.parseInt. (role: primary)

### CastRounds

- **Edge:** `explicit_cast` &rarr; `CastRounds` (misconception)
- **Exact edge logic (the wrong rule):** (int) 2.7 evaluates to 3.
- **Twin logic (the right rule):** A cast to int discards the fractional part (rounds toward zero, so (int) -2.7 is -2); Math.round rounds to the nearest integer.
- **Wrong belief (on the node):** (int) 2.7 evaluates to 3.
- **Correct rule (on the node):** A cast to int discards the fractional part (rounds toward zero, so (int) -2.7 is -2); Math.round rounds to the nearest integer.
- **Provenance:** textbook
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [1] misconception, exact rule:** wrong rule: (int) 2.7 evaluates to 3. Right rule: A cast to int discards the fractional part (rounds toward zero, so (int) -2.7 is -2); Math.round rounds to the nearest integer.
- **L0 way [4] inconsistent\_trace, exact rule:** Points to LT (the cast is a unary operator applied to the operand right after it, before \* and /). Applied unevenly: in one line the student casts only the first operand, and in another applies the same cast to the whole expression. (here mixing in: "(int) 2.7 evaluates to 3")
- **Edge `math_library` &rarr; `CastRounds`, exact edge logic:** (int) 2.7 evaluates to 3. **Twin logic:** A cast to int discards the fractional part (rounds toward zero, so (int) -2.7 is -2); Math.round rounds to the nearest integer. (role: context)
- **Edge `math_round` &rarr; `CastRounds`, exact edge logic:** (int) 2.7 evaluates to 3. **Twin logic:** A cast to int discards the fractional part (rounds toward zero, so (int) -2.7 is -2); Math.round rounds to the nearest integer. (role: context)

### LaterDoubleLiteralFixesDivision

- **Edge:** `explicit_cast` &rarr; `LaterDoubleLiteralFixesDivision` (misconception)
- **Exact edge logic (the wrong rule):** Changing a later literal to 100.0 fixes an earlier int division.
- **Twin logic (the right rule):** The int division happens first; the double must be in the division itself.
- **Wrong belief (on the node):** Changing a later literal to 100.0 fixes an earlier int division.
- **Correct rule (on the node):** The int division happens first; the double must be in the division itself.
- **Provenance:** textbook
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [6] misconception, exact rule:** wrong rule: Changing a later literal to 100.0 fixes an earlier int division. Right rule: The int division happens first, when its own operands are both ints; a double must appear in that division itself (or one operand must be cast before it).
- **Edge `integer_division` &rarr; `LaterDoubleLiteralFixesDivision`, exact edge logic:** Changing a later literal to 100.0 fixes an earlier int division. **Twin logic:** The int division happens first; the double must be in the division itself. (role: primary)

## Errors (1)

An error edge states the rule that gets broken in a program, and the right rule.

### RoundReturnsInt

- **Edge:** `explicit_cast` &rarr; `RoundReturnsInt` (error)
- **Exact edge logic (the wrong rule):** Writes int n = Math.round(x); because Math.round gives an int.
- **Twin logic (the right rule):** Math.round(double) returns a long, so storing it in an int needs a cast: int n = (int) Math.round(x);
- **Wrong belief (on the node):** Writes int n = Math.round(x); because Math.round gives an int.
- **Correct rule (on the node):** Math.round(double) returns a long, so storing it in an int needs a cast: int n = (int) Math.round(x);
- **Provenance:** textbook
- **Role of this concept:** context
- **Edge `math_round` &rarr; `RoundReturnsInt`, exact edge logic:** Writes int n = Math.round(x); because Math.round gives an int. **Twin logic:** Math.round(double) returns a long, so storing it in an int needs a cast: int n = (int) Math.round(x); (role: primary)

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for explicit cast: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to explicit cast agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

- **Edge:** `explicit_cast` &rarr; `explicit_cast@L0` (has_level)
- **Exact edge logic:** explicit cast -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (7 ways).

Ways (7), each with its exact rule:

- **[0] everyday\_reading** (rule type E, folk-meaning rule): Folk meaning: 'convert 2.7 to a whole number' means round it to 3, and (int) looks like a function label that applies to everything written after it. Java rule: a cast to int truncates toward zero ((int) 2.7 is 2) and, having higher precedence than arithmetic, applies only to the value immediately following it.
- **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `CastRounds`: wrong rule: (int) 2.7 evaluates to 3. Right rule: A cast to int discards the fractional part (rounds toward zero, so (int) -2.7 is -2); Math.round rounds to the nearest integer.
- **[2] misconception** (rule type M, wrong rule / right rule) &rarr; `CastAfterIntDivision`: wrong rule: (double) (3 / 5) is 0.6. Right rule: The integer division 3 / 5 = 0 happens inside the parentheses before the cast, so the result is 0.0; write (double) 3 / 5 to get 0.6.
- **[3] misconception** (rule type M, wrong rule / right rule) &rarr; `CastAppliesToWholeExpression`: wrong rule: (int) 2.5 / 0.15 casts the whole quotient to int. Right rule: The cast applies only to what comes right after it, here 2.5, so the expression is 2 / 0.15 (a double); write (int) (2.5 / 0.15) to cast the quotient.
- **[4] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `CastRounds`: Points to LT (the cast is a unary operator applied to the operand right after it, before \* and /). Applied unevenly: in one line the student casts only the first operand, and in another applies the same cast to the whole expression. (here mixing in: "(int) 2.7 evaluates to 3")
- **[5] misconception** (rule type M, wrong rule / right rule) &rarr; `CastParsesString`: wrong rule: (int) args[0] converts the text "34" into the number 34. Right rule: A cast cannot convert a String; a String argument that represents a number must be converted with a method such as Integer.parseInt.
- **[6] misconception** (rule type M, wrong rule / right rule) &rarr; `LaterDoubleLiteralFixesDivision`: wrong rule: Changing a later literal to 100.0 fixes an earlier int division. Right rule: The int division happens first, when its own operands are both ints; a double must appear in that division itself (or one operand must be cast before it).

### L1: Unistructural / atom x text surface

L1 for explicit cast: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

- **Edge:** `explicit_cast` &rarr; `explicit_cast@L1` (has_level)
- **Exact edge logic:** explicit cast -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

Ways (2), each with its exact rule:

- **[0] names\_the\_element** (rule type N, identity rule): A cast is a unary operator, written (type) expression, that converts a value of one primitive type to another, used when the conversion may lose information.
- **[1] states\_the\_rule** (rule type S, declarative rule): (T) e converts the value of e to type T; a double-to-int cast discards the fraction by rounding toward zero; a cast is required for narrowing conversions; it has higher precedence than arithmetic; casts between boolean and numbers, or from String to int, are not allowed.

### L2: Multistructural / block x execution / preoperational

L2 for explicit cast: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

- **Edge:** `explicit_cast` &rarr; `explicit_cast@L2` (has_level)
- **Exact edge logic:** explicit cast -&gt; L2 (Multistructural): the answer applies the rules of explicit cast to every part of the code, in order (3 ways).

Ways (3), each with its exact rule:

- **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): Evaluate the operand immediately to the right of the cast (a parenthesized expression is evaluated completely first), convert that value, then continue with the remaining operators of the expression.
- **[1] output\_prediction** (rule type OP, evaluation / result rule): (int) 2.71828 is int 2; (int) -2.7 is -2; (int) 11 \* 0.3 is double 3.3; (int) (11 \* 0.3) is int 3; (double) 3 / 5 is 0.6 but (double) (3 / 5) is 0.0; (char) ('a' + 4) is 'e'.
- **[2] one\_step\_execution** (rule type OS, state-transition rule): A cast yields a new value and changes nothing else: neither the type nor the value of the variable being cast changes (after int x = (int) pi; pi is still 3.14159).

### L3: Relational / relations x function (concrete operational begins)

L3 for explicit cast: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

- **Edge:** `explicit_cast` &rarr; `explicit_cast@L3` (has_level)
- **Exact edge logic:** explicit cast -&gt; L3 (Relational): the answer relates the parts (6 ways).

Ways (6), each with its exact rule:

- **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): A cast is the explicit conversion between primitive types, needed exactly where automatic conversion is refused because information may be lost.
- **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): To turn Math.random()'s double into a random int from 0 to N-1, the cast must enclose the product: (int) (Math.random() \* N); casting first gives 0.
- **[2] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): x op= e contains an implicit cast back to the type of x, so with int x, x += 0.5 compiles (x = (int) (x + 0.5)) while x = x + 0.5 is a compile-time error.
- **[3] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Widening (promotion) happens automatically when a value goes to a type with a larger range (int to double) and loses nothing; a narrowing conversion (double to int) is never automatic and needs an explicit cast, which truncates toward zero.
- **[4] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): (int) 2.71828 truncates toward zero and gives 2; Math.round(2.71828) rounds to the nearest integer and gives 3, as a long that needs (int) to become an int.
- **[5] purpose\_of\_the\_whole** (rule type P, plan / role rule): Used to discard information on purpose: truncating a scaled random number to an index, taking the integer part, converting between char and int codes ((char) ('a' + k)), or forcing real division with (double) sum / n.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for explicit cast: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

- **Edge:** `explicit_cast` &rarr; `explicit_cast@L4` (has_level)
- **Exact edge logic:** explicit cast -&gt; L4 (Extended abstract): the answer reasons beyond the given code (6 ways).

Ways (6), each with its exact rule:

- **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `CastRounds`: Moving the parentheses changes when truncation happens ((int) (a \* b) vs (int) a \* b); removing a cast from a narrowing assignment turns it into a compile-time error; int to double to int restores the value, but double to int to double loses the fraction.
- **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Use a cast when you intend to truncate or narrow (random indices, integer parts, char codes); use Math.round to round, Integer.parseInt for Strings, and put a double into the division itself rather than casting its int result.
- **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: Math.round(double) returns a long, so storing it in an int needs a cast: int n = (int) Math.round(x);. Kind: compile-time. Trigger class: int n = Math.round(x); with double x.
- **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: A cast applies only to the value right after it. Kind: compile-time. Trigger class: int n = (int) 11 \* 0.3; the product is still a double (possible loss of precision); in a double context the same mistake is a silent logic error ((int) pi \* 20.0 gives 60.0).
- **[4] diagnose\_an\_error** (rule type D, error rule): rule broken: Casts require compatible types. Kind: compile-time. Trigger class: (int) "3" or (int) args[0] on a String, or a cast between boolean and a number.
- **[5] diagnose\_an\_error** (rule type D, error rule): rule broken: A narrowing cast may lose magnitude, not just the fraction. Kind: silent logic error. Trigger class: Casting a value outside the target range, e.g. (int) of a long above 2147483647 or of a huge double.

## Same topic

`explicit_cast` belongs to the topic **Type conversion (automatic, cast, parsing)** (`topic1.2.h`). The topic also contains: `parsing`, `string_conversion`, `type_conversion`, `widening_conversion`.

## Rules of the concept (22)

- **Book** (SW-1e, p. 32 (pdf 42)): "You have to make your intention to do so explicit by using a device called a cast."
- **Book** (SW-1.2, ): "you have to make your intention using something called a cast"
- **Book** (RS, ): "the cast is applied to whatever comes right after it"
- **E** (folk-meaning rule): Folk meaning: 'convert 2.7 to a whole number' means round it to 3, and (int) looks like a function label that applies to everything written after it. Java rule: a cast to int truncates toward zero ((int) 2.7 is 2) and, having higher precedence than arithmetic, applies only to the value immediately following it.
- **M** (wrong rule / right rule): CastAfterIntDivision: wrong: (double) (3 / 5) is 0.6. \| right: The integer division 3 / 5 = 0 happens inside the parentheses before the cast, so the result is 0.0; write (double) 3 / 5 to get 0.6.
- **M** (wrong rule / right rule): CastAppliesToWholeExpression: wrong: (int) 2.5 / 0.15 casts the whole quotient to int. \| right: The cast applies only to what comes right after it, here 2.5, so the expression is 2 / 0.15 (a double); write (int) (2.5 / 0.15) to cast the quotient.
- **M** (wrong rule / right rule): CastParsesString: wrong: (int) args[0] converts the text "34" into the number 34. \| right: A cast cannot convert a String; a String argument that represents a number must be converted with a method such as Integer.parseInt.
- **M** (wrong rule / right rule): CastRounds: wrong: (int) 2.7 evaluates to 3. \| right: A cast to int discards the fractional part (rounds toward zero, so (int) -2.7 is -2); Math.round rounds to the nearest integer.
- **M** (wrong rule / right rule): LaterDoubleLiteralFixesDivision: wrong: Changing a later literal to 100.0 fixes an earlier int division. \| right: The int division happens first, when its own operands are both ints; a double must appear in that division itself (or one operand must be cast before it).
- **T** (uneven-application rule): Points to LT (the cast is a unary operator applied to the operand right after it, before \* and /). Applied unevenly: in one line the student casts only the first operand, and in another applies the same cast to the whole expression.
- **N** (identity rule): A cast is a unary operator, written (type) expression, that converts a value of one primitive type to another, used when the conversion may lose information.
- **S** (declarative rule): (T) e converts the value of e to type T; a double-to-int cast discards the fraction by rounding toward zero; a cast is required for narrowing conversions; it has higher precedence than arithmetic; casts between boolean and numbers, or from String to int, are not allowed.
- **LT** (operational sequencing rule): Evaluate the operand immediately to the right of the cast (a parenthesized expression is evaluated completely first), convert that value, then continue with the remaining operators of the expression.
- **OP** (evaluation / result rule): (int) 2.71828 is int 2; (int) -2.7 is -2; (int) 11 \* 0.3 is double 3.3; (int) (11 \* 0.3) is int 3; (double) 3 / 5 is 0.6 but (double) (3 / 5) is 0.0; (char) ('a' + 4) is 'e'.
- **OS** (state-transition rule): A cast yields a new value and changes nothing else: neither the type nor the value of the variable being cast changes (after int x = (int) pi; pi is still 3.14159).
- **R** (composition rule (with a neighbour)): with type\_conversion: A cast is the explicit conversion between primitive types, needed exactly where automatic conversion is refused because information may be lost.
- **R** (composition rule (with a neighbour)): with math\_random: To turn Math.random()'s double into a random int from 0 to N-1, the cast must enclose the product: (int) (Math.random() \* N); casting first gives 0.
- **R** (composition rule (with a neighbour)): with compound\_assignment: x op= e contains an implicit cast back to the type of x, so with int x, x += 0.5 compiles (x = (int) (x + 0.5)) while x = x + 0.5 is a compile-time error.
- **P** (plan / role rule): Used to discard information on purpose: truncating a scaled random number to an index, taking the integer part, converting between char and int codes ((char) ('a' + k)), or forcing real division with (double) sum / n.
- **C** (conservation rule): Moving the parentheses changes when truncation happens ((int) (a \* b) vs (int) a \* b); removing a cast from a narrowing assignment turns it into a compile-time error; int to double to int restores the value, but double to int to double loses the fraction.
- **D** (error rule): rule broken: Math.round(double) returns a long, so storing it in an int needs a cast: int n = (int) Math.round(x); (compile-time)
- **D** (error rule): rule broken: A cast applies only to the value right after it. (compile-time)
- **D** (error rule): rule broken: Casts require compatible types. (compile-time)
- **D** (error rule): rule broken: A narrowing cast may lose magnitude, not just the fraction. (silent logic error)
- **X** (applicability rule): Use a cast when you intend to truncate or narrow (random indices, integer parts, char codes); use Math.round to round, Integer.parseInt for Strings, and put a double into the division itself rather than casting its int result.

## How it is found in code and answers (reader block)

- **Aliases:** cast, casting, casts, type cast
- **Code patterns:** `\(\s*(?:int|double|boolean|char|long|String|float|short|byte)\s*\)(?=\s*[A-Za-z_0-9(])`
- **Operator symbols:** none
- **Java types:** none

## The whole prerequisite chain

- **Everything it builds on (10):** `arithmetic_operators`, `class_declaration`, `command_line_args`, `data_type`, `integer_division`, `main_method`, `parsing`, `primitive_type`, `program_text`, `type_conversion`
- **Everything that builds on it (5):** `accumulator_pattern`, `compound_assignment`, `math_random`, `monte_carlo_simulation`, `sentinel_loop`

## Every edge in this view and its exact edge logic (29)

All the edges drawn in the picture, in the order: prerequisite, parallel, misconception, error, has_level, contains.

**1. `explicit_cast` &rarr; `compound_assignment`** (prerequisite)

- **Exact edge logic:** x op= e means x = (T)(x op e), where T is the type of x, so the result is cast back to the type of x.
- **Grounding:** questionable
- **Composition rule (R) of `explicit_cast` with `compound_assignment`:** x op= e contains an implicit cast back to the type of x, so with int x, x += 0.5 compiles (x = (int) (x + 0.5)) while x = x + 0.5 is a compile-time error.
- **Composition rule (R) of `compound_assignment` with `explicit_cast`:** x op= e includes a hidden narrowing cast to the type of x: with int x = 1, x += 1.7 compiles (as x = (int)(x + 1.7), giving 2) while x = x + 1.7 does not.

**2. `explicit_cast` &rarr; `math_random`** (prerequisite)

- **Exact edge logic:** To turn Math.random()'s double in [0, 1) into a random int from 0 to N-1, multiply it by N and cast the result to int.
- **Grounding:** book\_passage
- **Composition rule (R) of `explicit_cast` with `math_random`:** To turn Math.random()'s double into a random int from 0 to N-1, the cast must enclose the product: (int) (Math.random() \* N); casting first gives 0.
- **Composition rule (R) of `math_random` with `explicit_cast`:** Converting to a random int requires the cast to apply to the whole product: (int) (Math.random() \* N); (int) Math.random() \* N casts first and is always 0.

**3. `integer_division` &rarr; `explicit_cast`** (prerequisite)

- **Exact edge logic:** To divide two ints and keep the fraction, one operand is cast to double before the division, as in (double) freq[i] / T; casting the finished quotient comes too late.
- **Grounding:** book\_passage

**4. `type_conversion` &rarr; `explicit_cast`** (prerequisite)

- **Exact edge logic:** A cast is the explicit form of type conversion between primitive types, required when the conversion may lose information (e.g. (int) 2.71828 is 2).
- **Grounding:** book\_passage
- **Composition rule (R) of `type_conversion` with `explicit_cast`:** A cast is the explicit conversion between primitive types, required when information may be lost: (int) 2.71828 is 2.
- **Composition rule (R) of `explicit_cast` with `type_conversion`:** A cast is the explicit conversion between primitive types, needed exactly where automatic conversion is refused because information may be lost.

**5. `math_round` &harr; `explicit_cast`** (parallel)

- **Exact edge logic:** (int) 2.71828 truncates toward zero and gives 2; Math.round(2.71828) rounds to the nearest integer and gives 3, as a long that needs (int) to become an int.
- **Grounding:** book\_passage

**6. `widening_conversion` &harr; `explicit_cast`** (parallel)

- **Exact edge logic:** Widening (promotion) happens automatically when a value goes to a type with a larger range (int to double) and loses nothing; a narrowing conversion (double to int) is never automatic and needs an explicit cast, which truncates toward zero.
- **Grounding:** book\_passage

**7. `explicit_cast` &rarr; `CastAfterIntDivision`** (misconception)

- **Exact edge logic (the wrong rule):** (double) (3 / 5) is 0.6.
- **Twin logic (the right rule):** The integer division 3 / 5 = 0 happens before the cast, so the result is 0.0.
- **Role:** primary

**8. `explicit_cast` &rarr; `CastAppliesToWholeExpression`** (misconception)

- **Exact edge logic (the wrong rule):** (int) 2.5 / 0.15 casts the whole quotient to int.
- **Twin logic (the right rule):** The cast applies only to what comes right after it, here 2.5.
- **Role:** primary

**9. `explicit_cast` &rarr; `CastParsesString`** (misconception)

- **Exact edge logic (the wrong rule):** (int) args[0] converts the text "34" into the number 34.
- **Twin logic (the right rule):** A String argument that represents a number must be converted with a method such as Integer.parseInt.
- **Role:** context

**10. `explicit_cast` &rarr; `CastRounds`** (misconception)

- **Exact edge logic (the wrong rule):** (int) 2.7 evaluates to 3.
- **Twin logic (the right rule):** A cast to int discards the fractional part (rounds toward zero, so (int) -2.7 is -2); Math.round rounds to the nearest integer.
- **Role:** primary

**11. `explicit_cast` &rarr; `LaterDoubleLiteralFixesDivision`** (misconception)

- **Exact edge logic (the wrong rule):** Changing a later literal to 100.0 fixes an earlier int division.
- **Twin logic (the right rule):** The int division happens first; the double must be in the division itself.
- **Role:** context

**12. `integer_division` &rarr; `CastAfterIntDivision`** (misconception)

- **Exact edge logic (the wrong rule):** (double) (3 / 5) is 0.6.
- **Twin logic (the right rule):** The integer division 3 / 5 = 0 happens before the cast, so the result is 0.0.
- **Role:** context

**13. `integer_division` &rarr; `LaterDoubleLiteralFixesDivision`** (misconception)

- **Exact edge logic (the wrong rule):** Changing a later literal to 100.0 fixes an earlier int division.
- **Twin logic (the right rule):** The int division happens first; the double must be in the division itself.
- **Role:** primary

**14. `math_library` &rarr; `CastRounds`** (misconception)

- **Exact edge logic (the wrong rule):** (int) 2.7 evaluates to 3.
- **Twin logic (the right rule):** A cast to int discards the fractional part (rounds toward zero, so (int) -2.7 is -2); Math.round rounds to the nearest integer.
- **Role:** context

**15. `math_round` &rarr; `CastRounds`** (misconception)

- **Exact edge logic (the wrong rule):** (int) 2.7 evaluates to 3.
- **Twin logic (the right rule):** A cast to int discards the fractional part (rounds toward zero, so (int) -2.7 is -2); Math.round rounds to the nearest integer.
- **Role:** context

**16. `operator_precedence` &rarr; `CastAppliesToWholeExpression`** (misconception)

- **Exact edge logic (the wrong rule):** (int) 2.5 / 0.15 casts the whole quotient to int.
- **Twin logic (the right rule):** The cast applies only to what comes right after it, here 2.5.
- **Role:** context

**17. `parsing` &rarr; `CastParsesString`** (misconception)

- **Exact edge logic (the wrong rule):** (int) args[0] converts the text "34" into the number 34.
- **Twin logic (the right rule):** A String argument that represents a number must be converted with a method such as Integer.parseInt.
- **Role:** primary

**18. `explicit_cast` &rarr; `RoundReturnsInt`** (error)

- **Exact edge logic (the wrong rule):** Writes int n = Math.round(x); because Math.round gives an int.
- **Twin logic (the right rule):** Math.round(double) returns a long, so storing it in an int needs a cast: int n = (int) Math.round(x);
- **Role:** context

**19. `math_round` &rarr; `RoundReturnsInt`** (error)

- **Exact edge logic (the wrong rule):** Writes int n = Math.round(x); because Math.round gives an int.
- **Twin logic (the right rule):** Math.round(double) returns a long, so storing it in an int needs a cast: int n = (int) Math.round(x);
- **Role:** primary

**20. `explicit_cast` &rarr; `explicit_cast@L0`** (has_level)

- **Exact edge logic:** explicit cast -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (7 ways).
  - **[0] everyday\_reading** (rule type E, folk-meaning rule): Folk meaning: 'convert 2.7 to a whole number' means round it to 3, and (int) looks like a function label that applies to everything written after it. Java rule: a cast to int truncates toward zero ((int) 2.7 is 2) and, having higher precedence than arithmetic, applies only to the value immediately following it.
  - **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `CastRounds`: wrong rule: (int) 2.7 evaluates to 3. Right rule: A cast to int discards the fractional part (rounds toward zero, so (int) -2.7 is -2); Math.round rounds to the nearest integer.
  - **[2] misconception** (rule type M, wrong rule / right rule) &rarr; `CastAfterIntDivision`: wrong rule: (double) (3 / 5) is 0.6. Right rule: The integer division 3 / 5 = 0 happens inside the parentheses before the cast, so the result is 0.0; write (double) 3 / 5 to get 0.6.
  - **[3] misconception** (rule type M, wrong rule / right rule) &rarr; `CastAppliesToWholeExpression`: wrong rule: (int) 2.5 / 0.15 casts the whole quotient to int. Right rule: The cast applies only to what comes right after it, here 2.5, so the expression is 2 / 0.15 (a double); write (int) (2.5 / 0.15) to cast the quotient.
  - **[4] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `CastRounds`: Points to LT (the cast is a unary operator applied to the operand right after it, before \* and /). Applied unevenly: in one line the student casts only the first operand, and in another applies the same cast to the whole expression. (here mixing in: "(int) 2.7 evaluates to 3")
  - **[5] misconception** (rule type M, wrong rule / right rule) &rarr; `CastParsesString`: wrong rule: (int) args[0] converts the text "34" into the number 34. Right rule: A cast cannot convert a String; a String argument that represents a number must be converted with a method such as Integer.parseInt.
  - **[6] misconception** (rule type M, wrong rule / right rule) &rarr; `LaterDoubleLiteralFixesDivision`: wrong rule: Changing a later literal to 100.0 fixes an earlier int division. Right rule: The int division happens first, when its own operands are both ints; a double must appear in that division itself (or one operand must be cast before it).

**21. `explicit_cast` &rarr; `explicit_cast@L1`** (has_level)

- **Exact edge logic:** explicit cast -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).
  - **[0] names\_the\_element** (rule type N, identity rule): A cast is a unary operator, written (type) expression, that converts a value of one primitive type to another, used when the conversion may lose information.
  - **[1] states\_the\_rule** (rule type S, declarative rule): (T) e converts the value of e to type T; a double-to-int cast discards the fraction by rounding toward zero; a cast is required for narrowing conversions; it has higher precedence than arithmetic; casts between boolean and numbers, or from String to int, are not allowed.

**22. `explicit_cast` &rarr; `explicit_cast@L2`** (has_level)

- **Exact edge logic:** explicit cast -&gt; L2 (Multistructural): the answer applies the rules of explicit cast to every part of the code, in order (3 ways).
  - **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): Evaluate the operand immediately to the right of the cast (a parenthesized expression is evaluated completely first), convert that value, then continue with the remaining operators of the expression.
  - **[1] output\_prediction** (rule type OP, evaluation / result rule): (int) 2.71828 is int 2; (int) -2.7 is -2; (int) 11 \* 0.3 is double 3.3; (int) (11 \* 0.3) is int 3; (double) 3 / 5 is 0.6 but (double) (3 / 5) is 0.0; (char) ('a' + 4) is 'e'.
  - **[2] one\_step\_execution** (rule type OS, state-transition rule): A cast yields a new value and changes nothing else: neither the type nor the value of the variable being cast changes (after int x = (int) pi; pi is still 3.14159).

**23. `explicit_cast` &rarr; `explicit_cast@L3`** (has_level)

- **Exact edge logic:** explicit cast -&gt; L3 (Relational): the answer relates the parts (6 ways).
  - **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): A cast is the explicit conversion between primitive types, needed exactly where automatic conversion is refused because information may be lost.
  - **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): To turn Math.random()'s double into a random int from 0 to N-1, the cast must enclose the product: (int) (Math.random() \* N); casting first gives 0.
  - **[2] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): x op= e contains an implicit cast back to the type of x, so with int x, x += 0.5 compiles (x = (int) (x + 0.5)) while x = x + 0.5 is a compile-time error.
  - **[3] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Widening (promotion) happens automatically when a value goes to a type with a larger range (int to double) and loses nothing; a narrowing conversion (double to int) is never automatic and needs an explicit cast, which truncates toward zero.
  - **[4] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): (int) 2.71828 truncates toward zero and gives 2; Math.round(2.71828) rounds to the nearest integer and gives 3, as a long that needs (int) to become an int.
  - **[5] purpose\_of\_the\_whole** (rule type P, plan / role rule): Used to discard information on purpose: truncating a scaled random number to an index, taking the integer part, converting between char and int codes ((char) ('a' + k)), or forcing real division with (double) sum / n.

**24. `explicit_cast` &rarr; `explicit_cast@L4`** (has_level)

- **Exact edge logic:** explicit cast -&gt; L4 (Extended abstract): the answer reasons beyond the given code (6 ways).
  - **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `CastRounds`: Moving the parentheses changes when truncation happens ((int) (a \* b) vs (int) a \* b); removing a cast from a narrowing assignment turns it into a compile-time error; int to double to int restores the value, but double to int to double loses the fraction.
  - **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Use a cast when you intend to truncate or narrow (random indices, integer parts, char codes); use Math.round to round, Integer.parseInt for Strings, and put a double into the division itself rather than casting its int result.
  - **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: Math.round(double) returns a long, so storing it in an int needs a cast: int n = (int) Math.round(x);. Kind: compile-time. Trigger class: int n = Math.round(x); with double x.
  - **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: A cast applies only to the value right after it. Kind: compile-time. Trigger class: int n = (int) 11 \* 0.3; the product is still a double (possible loss of precision); in a double context the same mistake is a silent logic error ((int) pi \* 20.0 gives 60.0).
  - **[4] diagnose\_an\_error** (rule type D, error rule): rule broken: Casts require compatible types. Kind: compile-time. Trigger class: (int) "3" or (int) args[0] on a String, or a cast between boolean and a number.
  - **[5] diagnose\_an\_error** (rule type D, error rule): rule broken: A narrowing cast may lose magnitude, not just the fraction. Kind: silent logic error. Trigger class: Casting a value outside the target range, e.g. (int) of a long above 2147483647 or of a huge double.

**25. `topic1.2.h` &rarr; `explicit_cast`** (contains)

- topic `topic1.2.h` contains `explicit_cast`

**26. `topic1.2.h` &rarr; `parsing`** (contains)

- topic `topic1.2.h` contains `parsing`

**27. `topic1.2.h` &rarr; `string_conversion`** (contains)

- topic `topic1.2.h` contains `string_conversion`

**28. `topic1.2.h` &rarr; `type_conversion`** (contains)

- topic `topic1.2.h` contains `type_conversion`

**29. `topic1.2.h` &rarr; `widening_conversion`** (contains)

- topic `topic1.2.h` contains `widening_conversion`
