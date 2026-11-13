# integer_division (`integer_division`)

/ on two ints truncates; % is the remainder

Section 1.2 Built-in Types of Data, topic 1.2.c Integers.

![The knowledge graph around integer_division](integer_division.png)

## At a glance

- **Needs first:** `arithmetic_operators`
- **Leads to:** `explicit_cast`, `normalization`, `remainder_operator`
- **Learned alongside:** nothing
- **Misconceptions:** `AllDoublesToAvoidDivision`, `CastAfterIntDivision`, `IntegerDivisionGivesFraction`, `LaterDoubleLiteralFixesDivision`, `NegativeRemainderSign`, `TargetTyping`
- **Errors:** none
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 30 edges around this concept, each explained in the graph's own words.

## What it needs first (1)

A prerequisite edge means the other concept has to be understood before `integer_division`.

### `arithmetic_operators` comes before `integer_division`

*+ - \* / %*

For ints a and b, / gives the whole quotient q and % gives the remainder r, so that a = b \* q + r.

- **Grounding:** book passage
- **How `integer_division` combines with `arithmetic_operators`:** / and % on ints are paired: q = a / b and r = a % b always satisfy a = b \* q + r.
- **How `arithmetic_operators` combines with `integer_division`:** For ints, / gives the truncated quotient and % the remainder, so (a / b) \* b + a % b == a.

## What it leads to (3)

These concepts need `integer_division` first.

### `integer_division` comes before `explicit_cast`

*(int) x -- converts between numeric types, truncating toward zero*

To divide two ints and keep the fraction, one operand is cast to double before the division, as in (double) freq[i] / T; casting the finished quotient comes too late.

- **Grounding:** book passage

### `integer_division` comes before `normalization`

*scaling a row so its probabilities sum to 1*

Normalising must divide as doubles, because with two ints counts / total truncates to 0 whenever counts &lt; total.

- **Grounding:** order only
- **How `integer_division` combines with `normalization`:** Normalizing counts must divide as doubles. With two ints, counts / total truncates to 0 whenever counts &lt; total.
- **How `normalization` combines with `integer_division`:** Type flow decides the result: with a double operand anywhere to the left (.90\*...) the division is floating-point; with two ints it truncates (2/5 == 0).

### `integer_division` comes before `remainder_operator`

*% gives the remainder of integer division*

% is the companion of integer division: a = (a / b) \* b + a % b.

- **Grounding:** book passage
- **How `integer_division` combines with `remainder_operator`:** % gives the remainder of the same truncating division: (a / b) \* b + a % b == a.
- **How `remainder_operator` combines with `integer_division`:** % is the companion of integer division, since a == (a / b) \* b + a % b. Both use the same quotient rounded toward 0.

## Learned alongside (0)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

No parallel edge touches this concept.

## Misconceptions (6)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### AllDoublesToAvoidDivision

- **Wrong rule:** Making every variable a double is the right fix for integer division.
- **Right rule:** Use int for countable things and double for measured ones; where a fraction is needed, make one operand of the division a double (or cast) instead of changing every type.
- **Role of this concept:** context
- **Shows at level L0 as:** misconception: wrong rule: Making every variable a double is the right fix for integer division. Right rule: Use int for countable things and double for measured ones; where a fraction is needed, make one operand of the division a double (or cast) instead of changing every type.
- **Also an edge from `data_type`:** Making every variable a double is the right fix for integer division.

### CastAfterIntDivision

- **Wrong rule:** (double) (3 / 5) is 0.6.
- **Right rule:** The integer division 3 / 5 = 0 happens before the cast, so the result is 0.0.
- **Role of this concept:** context
- **Shows at level L0 as:** misconception: wrong rule: (double) (3 / 5) is 0.6. Right rule: The integer division 3 / 5 = 0 happens before the cast, so the result is 0.0.
- **Also an edge from `explicit_cast`:** (double) (3 / 5) is 0.6.

### IntegerDivisionGivesFraction

- **Wrong rule:** 10 / 3 evaluates to 3.333....
- **Right rule:** Dividing two ints gives an int: the fractional part is discarded.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: 10 / 3 evaluates to 3.333. Right rule: Dividing two ints gives an int: the fractional part is discarded.
- **Also an edge from `int`:** 10 / 3 evaluates to 3.333....

### LaterDoubleLiteralFixesDivision

- **Wrong rule:** Changing a later literal to 100.0 fixes an earlier int division.
- **Right rule:** The int division happens first; the double must be in the division itself.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: Changing a later literal to 100.0 fixes an earlier int division. Right rule: The int division happens first; the double must be in the division itself.
- **Also an edge from `explicit_cast`:** Changing a later literal to 100.0 fixes an earlier int division.

### NegativeRemainderSign

- **Wrong rule:** a % b is never negative, and integer division of a negative number rounds down.
- **Right rule:** a / b rounds toward 0 and a % b takes the sign of a: -14 / 3 is -4 and -14 % 3 is -2.
- **Role of this concept:** context
- **Shows at level L0 as:** misconception: wrong rule: a % b is never negative, and integer division of a negative number rounds down. Right rule: a / b rounds toward 0 and a % b takes the sign of a: -14 / 3 is -4 and -14 % 3 is -2.
- **Also an edge from `remainder_operator`:** a % b is never negative, and integer division of a negative number rounds down.

### TargetTyping

- **Wrong rule:** The type of a numerical expression depends on the type expected by the surrounding context, so double d = a / b; keeps the fraction.
- **Right rule:** The type of a numerical expression is determined by the expression, so double d = a / b; with int a and b still divides as ints.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: The type of a numerical expression depends on the type expected by the surrounding context, so double d = a / b; keeps the fraction. Right rule: The type of a numerical expression is determined by the expression, so double d = a / b; with int a and b still divides as ints.
- **Shows at level L0 as:** inconsistent trace: Points to LT (each / looks at its own two operand types when it is evaluated). Applied unevenly, a student evaluates 9/5 as 1.8 in f = (9/5)\*c + 32 but as 1 elsewhere, or assumes a later double operand rescues an earlier int division. (here mixing in: "The type of a numerical expression depends on the type expected by the surrounding context, so double d = a / b; keeps the fraction")
- **Also an edge from `expression`:** The type of a numerical expression depends on the type expected by the surrounding context, so double d = a / b; keeps the fraction.
- **Also an edge from `type_conversion`:** The type of a numerical expression depends on the type expected by the surrounding context, so double d = a / b; keeps the fraction.

## Errors (0)

An error edge states the rule that gets broken in a program, and the right rule.

The graph has no error edge from this concept.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for integer division: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to integer division agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

integer division -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (8 ways).

- **everyday reading** (folk-meaning rule): In everyday and school arithmetic, 'divide' gives an exact answer or a fraction (10 ÷ 3 = 3 1/3), and rounding goes to the nearest whole number. In Java, / with two int operands discards the fraction, rounding toward zero (59 / 60 is 0).
- **misconception** (wrong rule / right rule; shows `TargetTyping`): wrong rule: The type of a numerical expression depends on the type expected by the surrounding context, so double d = a / b; keeps the fraction. Right rule: The type of a numerical expression is determined by the expression, so double d = a / b; with int a and b still divides as ints.
- **misconception** (wrong rule / right rule; shows `IntegerDivisionGivesFraction`): wrong rule: 10 / 3 evaluates to 3.333. Right rule: Dividing two ints gives an int: the fractional part is discarded.
- **misconception** (wrong rule / right rule; shows `LaterDoubleLiteralFixesDivision`): wrong rule: Changing a later literal to 100.0 fixes an earlier int division. Right rule: The int division happens first; the double must be in the division itself.
- **inconsistent trace** (uneven-application rule; shows `TargetTyping`): Points to LT (each / looks at its own two operand types when it is evaluated). Applied unevenly, a student evaluates 9/5 as 1.8 in f = (9/5)\*c + 32 but as 1 elsewhere, or assumes a later double operand rescues an earlier int division. (here mixing in: "The type of a numerical expression depends on the type expected by the surrounding context, so double d = a / b; keeps the fraction")
- **misconception** (wrong rule / right rule; shows `AllDoublesToAvoidDivision`): wrong rule: Making every variable a double is the right fix for integer division. Right rule: Use int for countable things and double for measured ones; where a fraction is needed, make one operand of the division a double (or cast) instead of changing every type.
- **misconception** (wrong rule / right rule; shows `CastAfterIntDivision`): wrong rule: (double) (3 / 5) is 0.6. Right rule: The integer division 3 / 5 = 0 happens before the cast, so the result is 0.0.
- **misconception** (wrong rule / right rule; shows `NegativeRemainderSign`): wrong rule: a % b is never negative, and integer division of a negative number rounds down. Right rule: a / b rounds toward 0 and a % b takes the sign of a: -14 / 3 is -4 and -14 % 3 is -2.

### L1: Unistructural / atom x text surface

L1 for integer division: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

integer division -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

- **names the element** (identity rule): Integer division: / applied to two integer operands, giving the whole-number quotient with the fractional part discarded.
- **states the rule** (declarative rule): If both operands of / are integral types, the result is an integer that rounds toward 0 (-14 / 3 is -4). If either operand is a double, the division is floating point.

### L2: Multistructural / block x execution / preoperational

L2 for integer division: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

integer division -&gt; L2 (Multistructural): the answer applies the rules of integer division to every part of the code, in order (3 ways).

- **line by line trace** (operational sequencing rule): Each / is evaluated when its turn comes (precedence, then left to right), using the types of its own two operands. Promoting the result to double, by a cast or by assignment, happens only afterwards and cannot restore the lost fraction.
- **output prediction** (evaluation / result rule): 10 / 3 is 3, 59 / 60 is 0, 1234 / 99 is 12, -14 / 3 is -4, and (double) (3 / 5) is 0.0.
- **one step execution** (state-transition rule): q = a / b stores the truncated quotient in q and leaves a and b unchanged. If b is 0, an ArithmeticException stops execution before anything is stored.

### L3: Relational / relations x function (concrete operational begins)

L3 for integer division: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

integer division -&gt; L3 (Relational): the answer relates the parts (4 ways).

- **relation to neighbour** (composition rule (with a neighbour)): / and % on ints are paired: q = a / b and r = a % b always satisfy a = b \* q + r.
- **relation to neighbour** (composition rule (with a neighbour)): Normalizing counts must divide as doubles. With two ints, counts / total truncates to 0 whenever counts &lt; total.
- **relation to neighbour** (composition rule (with a neighbour)): % gives the remainder of the same truncating division: (a / b) \* b + a % b == a.
- **purpose of the whole** (plan / role rule): Quotient plans: unit conversion (76 / 12 feet), dropping a digit (n / 10), finding a midpoint ((lo + hi) / 2), and computing a bucket or row index (i / cols).

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for integer division: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

integer division -&gt; L4 (Extended abstract): the answer reasons beyond the given code (5 ways).

- **predict a change** (conservation rule; shows `TargetTyping`): Making one operand a double (10.0 / 3) keeps the fraction (3.333...). Casting after the division does not. Multiplying before dividing preserves precision (59 \* 100 / 60 is 98). Changing an operand's sign changes only the quotient's sign, since rounding is toward zero.
- **transfer to a new program** (applicability rule): Use integer division when you want the whole quotient (units, digits, indices, half a size). When a fraction is needed, make one operand a double (10.0 / 3 or (double) a / b) rather than turning every variable into a double.
- **diagnose an error** (error rule): rule broken: With two int operands, / discards the fraction. Kind: silent logic error. Trigger class: Two int operands where a fraction is intended: 9/5 in a temperature formula, count / total, 1 / n, sum / n for an average.
- **diagnose an error** (error rule): rule broken: int division by zero is undefined. Kind: run-time exception. Trigger class: A divisor that evaluates to 0: ArithmeticException: / by zero.
- **diagnose an error** (error rule): rule broken: Integer division rounds toward zero, not down. Kind: silent logic error. Trigger class: Negative operands where floor was expected (-7 / 2 is -3, not -4).

## Same topic

`integer_division` belongs to the topic **Integers** (`topic1.2.c`). The topic also contains: `arithmetic_operators`, `int`, `int_literal_limit`, `integer_constants`, `long_type`, `overflow`, `remainder_operator`.

## Rules of the concept (22)

- **folk-meaning rule:** In everyday and school arithmetic, 'divide' gives an exact answer or a fraction (10 ÷ 3 = 3 1/3), and rounding goes to the nearest whole number. In Java, / with two int operands discards the fraction, rounding toward zero (59 / 60 is 0).
- **wrong rule / right rule:** AllDoublesToAvoidDivision: wrong: Making every variable a double is the right fix for integer division. \| right: Use int for countable things and double for measured ones; where a fraction is needed, make one operand of the division a double (or cast) instead of changing every type.
- **wrong rule / right rule:** CastAfterIntDivision: wrong: (double) (3 / 5) is 0.6. \| right: The integer division 3 / 5 = 0 happens before the cast, so the result is 0.0.
- **wrong rule / right rule:** IntegerDivisionGivesFraction: wrong: 10 / 3 evaluates to 3.333.... \| right: Dividing two ints gives an int: the fractional part is discarded.
- **wrong rule / right rule:** LaterDoubleLiteralFixesDivision: wrong: Changing a later literal to 100.0 fixes an earlier int division. \| right: The int division happens first; the double must be in the division itself.
- **wrong rule / right rule:** TargetTyping: wrong: The type of a numerical expression depends on the type expected by the surrounding context, so double d = a / b; keeps the fraction. \| right: The type of a numerical expression is determined by the expression, so double d = a / b; with int a and b still divides as ints.
- **wrong rule / right rule:** NegativeRemainderSign: wrong: a % b is never negative, and integer division of a negative number rounds down. \| right: a / b rounds toward 0 and a % b takes the sign of a: -14 / 3 is -4 and -14 % 3 is -2.
- **uneven-application rule:** Points to LT (each / looks at its own two operand types when it is evaluated). Applied unevenly, a student evaluates 9/5 as 1.8 in f = (9/5)\*c + 32 but as 1 elsewhere, or assumes a later double operand rescues an earlier int division.
- **identity rule:** Integer division: / applied to two integer operands, giving the whole-number quotient with the fractional part discarded.
- **declarative rule:** If both operands of / are integral types, the result is an integer that rounds toward 0 (-14 / 3 is -4). If either operand is a double, the division is floating point.
- **operational sequencing rule:** Each / is evaluated when its turn comes (precedence, then left to right), using the types of its own two operands. Promoting the result to double, by a cast or by assignment, happens only afterwards and cannot restore the lost fraction.
- **evaluation / result rule:** 10 / 3 is 3, 59 / 60 is 0, 1234 / 99 is 12, -14 / 3 is -4, and (double) (3 / 5) is 0.0.
- **state-transition rule:** q = a / b stores the truncated quotient in q and leaves a and b unchanged. If b is 0, an ArithmeticException stops execution before anything is stored.
- **composition rule (with a neighbour):** with arithmetic\_operators: / and % on ints are paired: q = a / b and r = a % b always satisfy a = b \* q + r.
- **composition rule (with a neighbour):** with normalization: Normalizing counts must divide as doubles. With two ints, counts / total truncates to 0 whenever counts &lt; total.
- **composition rule (with a neighbour):** with remainder\_operator: % gives the remainder of the same truncating division: (a / b) \* b + a % b == a.
- **plan / role rule:** Quotient plans: unit conversion (76 / 12 feet), dropping a digit (n / 10), finding a midpoint ((lo + hi) / 2), and computing a bucket or row index (i / cols).
- **conservation rule:** Making one operand a double (10.0 / 3) keeps the fraction (3.333...). Casting after the division does not. Multiplying before dividing preserves precision (59 \* 100 / 60 is 98). Changing an operand's sign changes only the quotient's sign, since rounding is toward zero.
- **error rule:** rule broken: With two int operands, / discards the fraction. (silent logic error)
- **error rule:** rule broken: int division by zero is undefined. (run-time exception)
- **error rule:** rule broken: Integer division rounds toward zero, not down. (silent logic error)
- **applicability rule:** Use integer division when you want the whole quotient (units, digits, indices, half a size). When a fraction is needed, make one operand a double (10.0 / 3 or (double) a / b) rather than turning every variable into a double.

## The whole prerequisite chain

- **Everything it builds on (1):** `arithmetic_operators`
- **Everything that builds on it (8):** `accumulator_pattern`, `compound_assignment`, `explicit_cast`, `math_random`, `monte_carlo_simulation`, `normalization`, `remainder_operator`, `sentinel_loop`
