# string_concatenation (`string_concatenation`)

+ with a String builds a new string

Section 1.2 Built-in Types of Data, topic 1.2.b Characters and strings.

![The knowledge graph around string_concatenation](string_concatenation.png)

## At a glance

- **Needs first:** `string_type`
- **Leads to:** `string_conversion`
- **Learned alongside:** `arithmetic_operators`
- **Misconceptions:** `ArithmeticPlusPrecedes`, `StringPlusLeftToRight`, `StringPlusStringifiesExpression`
- **Errors:** none
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 19 edges around this concept, each explained in the graph's own words.

## What it needs first (1)

A prerequisite edge means the other concept has to be understood before `string_concatenation`.

### `string_type` comes before `string_concatenation`

*String -- a reference type, not a primitive*

+ builds a new String whenever at least one of its operands is a String.

- **Grounding:** book passage
- **How `string_concatenation` combines with `string_type`:** Concatenation always yields a String, even when one operand is a number, so its result cannot be used in arithmetic without parsing.
- **How `string_type` combines with `string_concatenation`:** + produces a new String whenever at least one operand is a String; the other operand is converted to text first.

## What it leads to (1)

These concepts need `string_concatenation` first.

### `string_concatenation` comes before `string_conversion`

*+ with a String converts the other operand to text*

When one operand of + is a String, Java converts the other operand to a String before concatenating.

- **Grounding:** book passage
- **How `string_concatenation` combines with `string_conversion`:** The non-String operand is converted to its printed form (int 99 to "99", double 1.0 to "1.0", char 'a' to "a") before joining.
- **How `string_conversion` combines with `string_concatenation`:** Conversion happens first, then concatenation: the non-String operand is turned into its characters before the two Strings are joined.

## Learned alongside (1)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

### `string_concatenation` alongside `arithmetic_operators`

*+ - \* / %*

+ adds when both operands are numbers and concatenates when either operand is a String, converting the other operand to a String. It is left-associative, so 1 + 2 + "3" is "33" but "1" + 2 + 3 is "123".

- **Grounding:** book passage

## Misconceptions (3)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### ArithmeticPlusPrecedes

- **Wrong rule:** In "s" + a + b, the numbers a and b are added first and their sum is joined to s.
- **Right rule:** Both uses of + have the same precedence and are evaluated left to right, so "s" + a + b joins a and then b as text; only "s" + (a + b) adds them first.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: arithmetic + binds tighter than string-concatenation +. Right rule: Both uses of + have the same precedence and are evaluated left to right, so "s" + a + b joins a and then b as text; only "s" + (a + b) adds them first.
- **Also an edge from `operator_precedence`:** In "s" + a + b, the numbers a and b are added first and their sum is joined to s.

### StringPlusLeftToRight

- **Wrong rule:** 2 + 3 + "bc" and "bc" + 2 + 3 give the same text.
- **Right rule:** + is evaluated left to right: 2 + 3 + "bc" is "5bc" but "bc" + 2 + 3 is "bc23".
- **Role of this concept:** context
- **Shows at level L0 as:** misconception: wrong rule: 2 + 3 + "bc" and "bc" + 2 + 3 give the same text. Right rule: + is evaluated left to right: 2 + 3 + "bc" is "5bc" but "bc" + 2 + 3 is "bc23".
- **Also an edge from `operator_precedence`:** 2 + 3 + "bc" and "bc" + 2 + 3 give the same text.
- **Also an edge from `string_conversion`:** 2 + 3 + "bc" and "bc" + 2 + 3 give the same text.

### StringPlusStringifiesExpression

- **Wrong rule:** In "s" + (a + b), the text a + b is joined to s instead of its value.
- **Right rule:** The expression (a + b) is evaluated first, and its value is then turned into text and joined to s.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: + with a String turns the whole other side into a string first. Right rule: The expression (a + b) is evaluated first, and its value is then turned into text and joined to s.
- **Shows at level L0 as:** inconsistent trace: Points to LT (left to right, and each + adds or concatenates according to its operands at that moment). Applied unevenly, a student keeps adding numbers after a String has appeared, or concatenates before any String appears (1 + 2 + "x" as "12x"). (here mixing in: "+ with a String turns the whole other side into a string first")

## Errors (0)

An error edge states the rule that gets broken in a program, and the right rule.

The graph has no error edge from this concept.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for string concatenation: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to string concatenation agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

string concatenation -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (5 ways).

- **everyday reading** (folk-meaning rule): In arithmetic, + always means 'add', and 'plus' combines quantities, so novices expect "1" + 2 to be 3. In Java, + with a String operand joins text end to end, and a chain of + is processed left to right, one operator at a time.
- **misconception** (wrong rule / right rule; shows `StringPlusStringifiesExpression`): wrong rule: + with a String turns the whole other side into a string first. Right rule: The expression (a + b) is evaluated first, and its value is then turned into text and joined to s.
- **misconception** (wrong rule / right rule; shows `StringPlusLeftToRight`): wrong rule: 2 + 3 + "bc" and "bc" + 2 + 3 give the same text. Right rule: + is evaluated left to right: 2 + 3 + "bc" is "5bc" but "bc" + 2 + 3 is "bc23".
- **inconsistent trace** (uneven-application rule; shows `StringPlusStringifiesExpression`): Points to LT (left to right, and each + adds or concatenates according to its operands at that moment). Applied unevenly, a student keeps adding numbers after a String has appeared, or concatenates before any String appears (1 + 2 + "x" as "12x"). (here mixing in: "+ with a String turns the whole other side into a string first")
- **misconception** (wrong rule / right rule; shows `ArithmeticPlusPrecedes`): wrong rule: arithmetic + binds tighter than string-concatenation +. Right rule: Both uses of + have the same precedence and are evaluated left to right, so "s" + a + b joins a and then b as text; only "s" + (a + b) adds them first.

### L1: Unistructural / atom x text surface

L1 for string concatenation: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

string concatenation -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

- **names the element** (identity rule): String concatenation: the + operator with a String operand, which joins two values end to end into a new String.
- **states the rule** (declarative rule): If either operand of + is a String, the other is converted to a String, and the result is a new String made of the first operand's characters followed by the second's.

### L2: Multistructural / block x execution / preoperational

L2 for string concatenation: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

string concatenation -&gt; L2 (Multistructural): the answer applies the rules of string concatenation to every part of the code, in order (3 ways).

- **line by line trace** (operational sequencing rule): A chain of + is evaluated left to right, after any parenthesized parts. At each + the current operand types decide: two numbers are added, otherwise the values are concatenated.
- **output prediction** (evaluation / result rule): The result is a String: 2 + "bc" is "2bc", 2 + 3 + "bc" is "5bc", "bc" + 2 + 3 is "bc23", and "bc" + (2+3) is "bc5".
- **one step execution** (state-transition rule): Concatenation creates a new String and changes no operand. A variable changes only if the result is assigned, as in ruler = ruler + i + ruler;.

### L3: Relational / relations x function (concrete operational begins)

L3 for string concatenation: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

string concatenation -&gt; L3 (Relational): the answer relates the parts (4 ways).

- **relation to neighbour** (composition rule (with a neighbour)): Concatenation always yields a String, even when one operand is a number, so its result cannot be used in arithmetic without parsing.
- **relation to neighbour** (composition rule (with a neighbour)): The non-String operand is converted to its printed form (int 99 to "99", double 1.0 to "1.0", char 'a' to "a") before joining.
- **relation to neighbour** (composition rule (with a neighbour)): + adds when both operands are numbers and concatenates when either operand is a String, converting the other operand to a String. It is left-associative, so 1 + 2 + "3" is "33" but "1" + 2 + 3 is "123".
- **purpose of the whole** (plan / role rule): Concatenation builds output lines and labels from computed values (a + " + " + b + " = " + c). Repeated s = s + piece makes s a gatherer of text.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for string concatenation: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

string concatenation -&gt; L4 (Extended abstract): the answer reasons beyond the given code (5 ways).

- **predict a change** (conservation rule; shows `StringPlusStringifiesExpression`): Parenthesizing numeric parts changes the result ("sum " + (a + b) adds before joining). Moving numbers before or after the first String changes whether they are added. Concatenating into a printf format string removes the separate argument printf needs.
- **transfer to a new program** (applicability rule): Use + concatenation for simple output and labels, putting parentheses around any arithmetic inside. Use printf when numbers need formatting, and parse Strings before using them as numbers.
- **diagnose an error** (error rule): rule broken: Once a String appears in a + chain, every later + concatenates. Kind: silent logic error. Trigger class: "Sum: " + a + b with numbers a and b prints both digit strings side by side (e.g. Sum: 23).
- **diagnose an error** (error rule): rule broken: char + char is numeric addition, not concatenation. Kind: silent logic error. Trigger class: Joining two chars with + when no String is involved ('b' + 'c' prints 197).
- **diagnose an error** (error rule): rule broken: printf needs its values as separate arguments matching the format specifiers. Kind: run-time exception. Trigger class: Concatenating the value into the format (printf("inches = %d" + inch)): MissingFormatArgumentException.

## Same topic

`string_concatenation` belongs to the topic **Characters and strings** (`topic1.2.b`). The topic also contains: `char`, `char_arithmetic`, `escape_sequences`, `string_type`.

## Rules of the concept (18)

- **folk-meaning rule:** In arithmetic, + always means 'add', and 'plus' combines quantities, so novices expect "1" + 2 to be 3. In Java, + with a String operand joins text end to end, and a chain of + is processed left to right, one operator at a time.
- **wrong rule / right rule:** ArithmeticPlusPrecedes: wrong: arithmetic + binds tighter than string-concatenation + \| right: Both uses of + have the same precedence and are evaluated left to right, so "s" + a + b joins a and then b as text; only "s" + (a + b) adds them first.
- **wrong rule / right rule:** StringPlusLeftToRight: wrong: 2 + 3 + "bc" and "bc" + 2 + 3 give the same text. \| right: + is evaluated left to right: 2 + 3 + "bc" is "5bc" but "bc" + 2 + 3 is "bc23".
- **wrong rule / right rule:** StringPlusStringifiesExpression: wrong: + with a String turns the whole other side into a string first \| right: The expression (a + b) is evaluated first, and its value is then turned into text and joined to s.
- **uneven-application rule:** Points to LT (left to right, and each + adds or concatenates according to its operands at that moment). Applied unevenly, a student keeps adding numbers after a String has appeared, or concatenates before any String appears (1 + 2 + "x" as "12x").
- **identity rule:** String concatenation: the + operator with a String operand, which joins two values end to end into a new String.
- **declarative rule:** If either operand of + is a String, the other is converted to a String, and the result is a new String made of the first operand's characters followed by the second's.
- **operational sequencing rule:** A chain of + is evaluated left to right, after any parenthesized parts. At each + the current operand types decide: two numbers are added, otherwise the values are concatenated.
- **evaluation / result rule:** The result is a String: 2 + "bc" is "2bc", 2 + 3 + "bc" is "5bc", "bc" + 2 + 3 is "bc23", and "bc" + (2+3) is "bc5".
- **state-transition rule:** Concatenation creates a new String and changes no operand. A variable changes only if the result is assigned, as in ruler = ruler + i + ruler;.
- **composition rule (with a neighbour):** with string\_type: Concatenation always yields a String, even when one operand is a number, so its result cannot be used in arithmetic without parsing.
- **composition rule (with a neighbour):** with string\_conversion: The non-String operand is converted to its printed form (int 99 to "99", double 1.0 to "1.0", char 'a' to "a") before joining.
- **plan / role rule:** Concatenation builds output lines and labels from computed values (a + " + " + b + " = " + c). Repeated s = s + piece makes s a gatherer of text.
- **conservation rule:** Parenthesizing numeric parts changes the result ("sum " + (a + b) adds before joining). Moving numbers before or after the first String changes whether they are added. Concatenating into a printf format string removes the separate argument printf needs.
- **error rule:** rule broken: Once a String appears in a + chain, every later + concatenates. (silent logic error)
- **error rule:** rule broken: char + char is numeric addition, not concatenation. (silent logic error)
- **error rule:** rule broken: printf needs its values as separate arguments matching the format specifiers. (run-time exception)
- **applicability rule:** Use + concatenation for simple output and labels, putting parentheses around any arithmetic inside. Use printf when numbers need formatting, and parse Strings before using them as numbers.

## The whole prerequisite chain

- **Everything it builds on (1):** `string_type`
- **Everything that builds on it (1):** `string_conversion`
