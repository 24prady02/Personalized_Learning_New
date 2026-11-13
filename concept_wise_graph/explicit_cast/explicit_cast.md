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

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 29 edges around this concept, each explained in the graph's own words.

## What it needs first (2)

A prerequisite edge means the other concept has to be understood before `explicit_cast`.

### `integer_division` comes before `explicit_cast`

*/ on two ints truncates; % is the remainder*

To divide two ints and keep the fraction, one operand is cast to double before the division, as in (double) freq[i] / T; casting the finished quotient comes too late.

- **Grounding:** book passage

### `type_conversion` comes before `explicit_cast`

*implicit widening and explicit (cast)*

A cast is the explicit form of type conversion between primitive types, required when the conversion may lose information (e.g. (int) 2.71828 is 2).

- **Grounding:** book passage
- **How `explicit_cast` combines with `type_conversion`:** A cast is the explicit conversion between primitive types, needed exactly where automatic conversion is refused because information may be lost.
- **How `type_conversion` combines with `explicit_cast`:** A cast is the explicit conversion between primitive types, required when information may be lost: (int) 2.71828 is 2.

## What it leads to (2)

These concepts need `explicit_cast` first.

### `explicit_cast` comes before `compound_assignment`

*x += e, x -= e, ... include a hidden cast*

x op= e means x = (T)(x op e), where T is the type of x, so the result is cast back to the type of x.

- **Grounding:** questionable
- **How `explicit_cast` combines with `compound_assignment`:** x op= e contains an implicit cast back to the type of x, so with int x, x += 0.5 compiles (x = (int) (x + 0.5)) while x = x + 0.5 is a compile-time error.
- **How `compound_assignment` combines with `explicit_cast`:** x op= e includes a hidden narrowing cast to the type of x: with int x = 1, x += 1.7 compiles (as x = (int)(x + 1.7), giving 2) while x = x + 1.7 does not.

### `explicit_cast` comes before `math_random`

*Math.random() and scaling to an int range*

To turn Math.random()'s double in [0, 1) into a random int from 0 to N-1, multiply it by N and cast the result to int.

- **Grounding:** book passage
- **How `explicit_cast` combines with `math_random`:** To turn Math.random()'s double into a random int from 0 to N-1, the cast must enclose the product: (int) (Math.random() \* N); casting first gives 0.
- **How `math_random` combines with `explicit_cast`:** Converting to a random int requires the cast to apply to the whole product: (int) (Math.random() \* N); (int) Math.random() \* N casts first and is always 0.

## Learned alongside (2)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

### `explicit_cast` alongside `math_round`

*Math.round rounds to the nearest integer and returns a long*

(int) 2.71828 truncates toward zero and gives 2; Math.round(2.71828) rounds to the nearest integer and gives 3, as a long that needs (int) to become an int.

- **Grounding:** book passage

### `explicit_cast` alongside `widening_conversion`

*automatic conversion to a type with a larger range*

Widening (promotion) happens automatically when a value goes to a type with a larger range (int to double) and loses nothing; a narrowing conversion (double to int) is never automatic and needs an explicit cast, which truncates toward zero.

- **Grounding:** book passage

## Misconceptions (5)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### CastAfterIntDivision

- **Wrong rule:** (double) (3 / 5) is 0.6.
- **Right rule:** The integer division 3 / 5 = 0 happens before the cast, so the result is 0.0.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: (double) (3 / 5) is 0.6. Right rule: The integer division 3 / 5 = 0 happens inside the parentheses before the cast, so the result is 0.0; write (double) 3 / 5 to get 0.6.
- **Also an edge from `integer_division`:** (double) (3 / 5) is 0.6.

### CastAppliesToWholeExpression

- **Wrong rule:** (int) 2.5 / 0.15 casts the whole quotient to int.
- **Right rule:** The cast applies only to what comes right after it, here 2.5.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: (int) 2.5 / 0.15 casts the whole quotient to int. Right rule: The cast applies only to what comes right after it, here 2.5, so the expression is 2 / 0.15 (a double); write (int) (2.5 / 0.15) to cast the quotient.
- **Also an edge from `operator_precedence`:** (int) 2.5 / 0.15 casts the whole quotient to int.

### CastParsesString

- **Wrong rule:** (int) args[0] converts the text "34" into the number 34.
- **Right rule:** A String argument that represents a number must be converted with a method such as Integer.parseInt.
- **Role of this concept:** context
- **Shows at level L0 as:** misconception: wrong rule: (int) args[0] converts the text "34" into the number 34. Right rule: A cast cannot convert a String; a String argument that represents a number must be converted with a method such as Integer.parseInt.
- **Also an edge from `parsing`:** (int) args[0] converts the text "34" into the number 34.

### CastRounds

- **Wrong rule:** (int) 2.7 evaluates to 3.
- **Right rule:** A cast to int discards the fractional part (rounds toward zero, so (int) -2.7 is -2); Math.round rounds to the nearest integer.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: (int) 2.7 evaluates to 3. Right rule: A cast to int discards the fractional part (rounds toward zero, so (int) -2.7 is -2); Math.round rounds to the nearest integer.
- **Shows at level L0 as:** inconsistent trace: Points to LT (the cast is a unary operator applied to the operand right after it, before \* and /). Applied unevenly: in one line the student casts only the first operand, and in another applies the same cast to the whole expression. (here mixing in: "(int) 2.7 evaluates to 3")
- **Also an edge from `math_library`:** (int) 2.7 evaluates to 3.
- **Also an edge from `math_round`:** (int) 2.7 evaluates to 3.

### LaterDoubleLiteralFixesDivision

- **Wrong rule:** Changing a later literal to 100.0 fixes an earlier int division.
- **Right rule:** The int division happens first; the double must be in the division itself.
- **Role of this concept:** context
- **Shows at level L0 as:** misconception: wrong rule: Changing a later literal to 100.0 fixes an earlier int division. Right rule: The int division happens first, when its own operands are both ints; a double must appear in that division itself (or one operand must be cast before it).
- **Also an edge from `integer_division`:** Changing a later literal to 100.0 fixes an earlier int division.

## Errors (1)

An error edge states the rule that gets broken in a program, and the right rule.

### RoundReturnsInt

- **Wrong rule:** Writes int n = Math.round(x); because Math.round gives an int.
- **Right rule:** Math.round(double) returns a long, so storing it in an int needs a cast: int n = (int) Math.round(x);
- **Role of this concept:** context
- **Also an edge from `math_round`:** Writes int n = Math.round(x); because Math.round gives an int.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for explicit cast: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to explicit cast agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

explicit cast -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (7 ways).

- **everyday reading** (folk-meaning rule): Folk meaning: 'convert 2.7 to a whole number' means round it to 3, and (int) looks like a function label that applies to everything written after it. Java rule: a cast to int truncates toward zero ((int) 2.7 is 2) and, having higher precedence than arithmetic, applies only to the value immediately following it.
- **misconception** (wrong rule / right rule; shows `CastRounds`): wrong rule: (int) 2.7 evaluates to 3. Right rule: A cast to int discards the fractional part (rounds toward zero, so (int) -2.7 is -2); Math.round rounds to the nearest integer.
- **misconception** (wrong rule / right rule; shows `CastAfterIntDivision`): wrong rule: (double) (3 / 5) is 0.6. Right rule: The integer division 3 / 5 = 0 happens inside the parentheses before the cast, so the result is 0.0; write (double) 3 / 5 to get 0.6.
- **misconception** (wrong rule / right rule; shows `CastAppliesToWholeExpression`): wrong rule: (int) 2.5 / 0.15 casts the whole quotient to int. Right rule: The cast applies only to what comes right after it, here 2.5, so the expression is 2 / 0.15 (a double); write (int) (2.5 / 0.15) to cast the quotient.
- **inconsistent trace** (uneven-application rule; shows `CastRounds`): Points to LT (the cast is a unary operator applied to the operand right after it, before \* and /). Applied unevenly: in one line the student casts only the first operand, and in another applies the same cast to the whole expression. (here mixing in: "(int) 2.7 evaluates to 3")
- **misconception** (wrong rule / right rule; shows `CastParsesString`): wrong rule: (int) args[0] converts the text "34" into the number 34. Right rule: A cast cannot convert a String; a String argument that represents a number must be converted with a method such as Integer.parseInt.
- **misconception** (wrong rule / right rule; shows `LaterDoubleLiteralFixesDivision`): wrong rule: Changing a later literal to 100.0 fixes an earlier int division. Right rule: The int division happens first, when its own operands are both ints; a double must appear in that division itself (or one operand must be cast before it).

### L1: Unistructural / atom x text surface

L1 for explicit cast: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

explicit cast -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

- **names the element** (identity rule): A cast is a unary operator, written (type) expression, that converts a value of one primitive type to another, used when the conversion may lose information.
- **states the rule** (declarative rule): (T) e converts the value of e to type T; a double-to-int cast discards the fraction by rounding toward zero; a cast is required for narrowing conversions; it has higher precedence than arithmetic; casts between boolean and numbers, or from String to int, are not allowed.

### L2: Multistructural / block x execution / preoperational

L2 for explicit cast: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

explicit cast -&gt; L2 (Multistructural): the answer applies the rules of explicit cast to every part of the code, in order (3 ways).

- **line by line trace** (operational sequencing rule): Evaluate the operand immediately to the right of the cast (a parenthesized expression is evaluated completely first), convert that value, then continue with the remaining operators of the expression.
- **output prediction** (evaluation / result rule): (int) 2.71828 is int 2; (int) -2.7 is -2; (int) 11 \* 0.3 is double 3.3; (int) (11 \* 0.3) is int 3; (double) 3 / 5 is 0.6 but (double) (3 / 5) is 0.0; (char) ('a' + 4) is 'e'.
- **one step execution** (state-transition rule): A cast yields a new value and changes nothing else: neither the type nor the value of the variable being cast changes (after int x = (int) pi; pi is still 3.14159).

### L3: Relational / relations x function (concrete operational begins)

L3 for explicit cast: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

explicit cast -&gt; L3 (Relational): the answer relates the parts (6 ways).

- **relation to neighbour** (composition rule (with a neighbour)): A cast is the explicit conversion between primitive types, needed exactly where automatic conversion is refused because information may be lost.
- **relation to neighbour** (composition rule (with a neighbour)): To turn Math.random()'s double into a random int from 0 to N-1, the cast must enclose the product: (int) (Math.random() \* N); casting first gives 0.
- **relation to neighbour** (composition rule (with a neighbour)): x op= e contains an implicit cast back to the type of x, so with int x, x += 0.5 compiles (x = (int) (x + 0.5)) while x = x + 0.5 is a compile-time error.
- **relation to neighbour** (composition rule (with a neighbour)): Widening (promotion) happens automatically when a value goes to a type with a larger range (int to double) and loses nothing; a narrowing conversion (double to int) is never automatic and needs an explicit cast, which truncates toward zero.
- **relation to neighbour** (composition rule (with a neighbour)): (int) 2.71828 truncates toward zero and gives 2; Math.round(2.71828) rounds to the nearest integer and gives 3, as a long that needs (int) to become an int.
- **purpose of the whole** (plan / role rule): Used to discard information on purpose: truncating a scaled random number to an index, taking the integer part, converting between char and int codes ((char) ('a' + k)), or forcing real division with (double) sum / n.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for explicit cast: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

explicit cast -&gt; L4 (Extended abstract): the answer reasons beyond the given code (6 ways).

- **predict a change** (conservation rule; shows `CastRounds`): Moving the parentheses changes when truncation happens ((int) (a \* b) vs (int) a \* b); removing a cast from a narrowing assignment turns it into a compile-time error; int to double to int restores the value, but double to int to double loses the fraction.
- **transfer to a new program** (applicability rule): Use a cast when you intend to truncate or narrow (random indices, integer parts, char codes); use Math.round to round, Integer.parseInt for Strings, and put a double into the division itself rather than casting its int result.
- **diagnose an error** (error rule): rule broken: Math.round(double) returns a long, so storing it in an int needs a cast: int n = (int) Math.round(x);. Kind: compile-time. Trigger class: int n = Math.round(x); with double x.
- **diagnose an error** (error rule): rule broken: A cast applies only to the value right after it. Kind: compile-time. Trigger class: int n = (int) 11 \* 0.3; the product is still a double (possible loss of precision); in a double context the same mistake is a silent logic error ((int) pi \* 20.0 gives 60.0).
- **diagnose an error** (error rule): rule broken: Casts require compatible types. Kind: compile-time. Trigger class: (int) "3" or (int) args[0] on a String, or a cast between boolean and a number.
- **diagnose an error** (error rule): rule broken: A narrowing cast may lose magnitude, not just the fraction. Kind: silent logic error. Trigger class: Casting a value outside the target range, e.g. (int) of a long above 2147483647 or of a huge double.

## Same topic

`explicit_cast` belongs to the topic **Type conversion (automatic, cast, parsing)** (`topic1.2.h`). The topic also contains: `parsing`, `string_conversion`, `type_conversion`, `widening_conversion`.

## Rules of the concept (22)

- **folk-meaning rule:** Folk meaning: 'convert 2.7 to a whole number' means round it to 3, and (int) looks like a function label that applies to everything written after it. Java rule: a cast to int truncates toward zero ((int) 2.7 is 2) and, having higher precedence than arithmetic, applies only to the value immediately following it.
- **wrong rule / right rule:** CastAfterIntDivision: wrong: (double) (3 / 5) is 0.6. \| right: The integer division 3 / 5 = 0 happens inside the parentheses before the cast, so the result is 0.0; write (double) 3 / 5 to get 0.6.
- **wrong rule / right rule:** CastAppliesToWholeExpression: wrong: (int) 2.5 / 0.15 casts the whole quotient to int. \| right: The cast applies only to what comes right after it, here 2.5, so the expression is 2 / 0.15 (a double); write (int) (2.5 / 0.15) to cast the quotient.
- **wrong rule / right rule:** CastParsesString: wrong: (int) args[0] converts the text "34" into the number 34. \| right: A cast cannot convert a String; a String argument that represents a number must be converted with a method such as Integer.parseInt.
- **wrong rule / right rule:** CastRounds: wrong: (int) 2.7 evaluates to 3. \| right: A cast to int discards the fractional part (rounds toward zero, so (int) -2.7 is -2); Math.round rounds to the nearest integer.
- **wrong rule / right rule:** LaterDoubleLiteralFixesDivision: wrong: Changing a later literal to 100.0 fixes an earlier int division. \| right: The int division happens first, when its own operands are both ints; a double must appear in that division itself (or one operand must be cast before it).
- **uneven-application rule:** Points to LT (the cast is a unary operator applied to the operand right after it, before \* and /). Applied unevenly: in one line the student casts only the first operand, and in another applies the same cast to the whole expression.
- **identity rule:** A cast is a unary operator, written (type) expression, that converts a value of one primitive type to another, used when the conversion may lose information.
- **declarative rule:** (T) e converts the value of e to type T; a double-to-int cast discards the fraction by rounding toward zero; a cast is required for narrowing conversions; it has higher precedence than arithmetic; casts between boolean and numbers, or from String to int, are not allowed.
- **operational sequencing rule:** Evaluate the operand immediately to the right of the cast (a parenthesized expression is evaluated completely first), convert that value, then continue with the remaining operators of the expression.
- **evaluation / result rule:** (int) 2.71828 is int 2; (int) -2.7 is -2; (int) 11 \* 0.3 is double 3.3; (int) (11 \* 0.3) is int 3; (double) 3 / 5 is 0.6 but (double) (3 / 5) is 0.0; (char) ('a' + 4) is 'e'.
- **state-transition rule:** A cast yields a new value and changes nothing else: neither the type nor the value of the variable being cast changes (after int x = (int) pi; pi is still 3.14159).
- **composition rule (with a neighbour):** with type\_conversion: A cast is the explicit conversion between primitive types, needed exactly where automatic conversion is refused because information may be lost.
- **composition rule (with a neighbour):** with math\_random: To turn Math.random()'s double into a random int from 0 to N-1, the cast must enclose the product: (int) (Math.random() \* N); casting first gives 0.
- **composition rule (with a neighbour):** with compound\_assignment: x op= e contains an implicit cast back to the type of x, so with int x, x += 0.5 compiles (x = (int) (x + 0.5)) while x = x + 0.5 is a compile-time error.
- **plan / role rule:** Used to discard information on purpose: truncating a scaled random number to an index, taking the integer part, converting between char and int codes ((char) ('a' + k)), or forcing real division with (double) sum / n.
- **conservation rule:** Moving the parentheses changes when truncation happens ((int) (a \* b) vs (int) a \* b); removing a cast from a narrowing assignment turns it into a compile-time error; int to double to int restores the value, but double to int to double loses the fraction.
- **error rule:** rule broken: Math.round(double) returns a long, so storing it in an int needs a cast: int n = (int) Math.round(x); (compile-time)
- **error rule:** rule broken: A cast applies only to the value right after it. (compile-time)
- **error rule:** rule broken: Casts require compatible types. (compile-time)
- **error rule:** rule broken: A narrowing cast may lose magnitude, not just the fraction. (silent logic error)
- **applicability rule:** Use a cast when you intend to truncate or narrow (random indices, integer parts, char codes); use Math.round to round, Integer.parseInt for Strings, and put a double into the division itself rather than casting its int result.

## The whole prerequisite chain

- **Everything it builds on (10):** `arithmetic_operators`, `class_declaration`, `command_line_args`, `data_type`, `integer_division`, `main_method`, `parsing`, `primitive_type`, `program_text`, `type_conversion`
- **Everything that builds on it (5):** `accumulator_pattern`, `compound_assignment`, `math_random`, `monte_carlo_simulation`, `sentinel_loop`
