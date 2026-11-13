# string_type (`string_type`)

String -- a reference type, not a primitive

Section 1.2 Built-in Types of Data, topic 1.2.b Characters and strings.

![The knowledge graph around string_type](string_type.png)

## At a glance

- **Needs first:** nothing
- **Leads to:** `string_concatenation`
- **Learned alongside:** `char`
- **Misconceptions:** `ArithmeticOnNumericStrings`, `EqualityOperatorComparesObjectsValues`, `EqualsComparesReferences`, `NullIsObject`, `ObjectsMustBeNamed`, `StringIsPrimitive`, `StringLiteralNoObject`, `StringMethodChangesString`, `StringRelationalComparison`
- **Errors:** none
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 30 edges around this concept, each explained in the graph's own words.

## What it needs first (0)

A prerequisite edge means the other concept has to be understood before `string_type`.

No prerequisite edge leads into this concept.

## What it leads to (1)

These concepts need `string_type` first.

### `string_type` comes before `string_concatenation`

*+ with a String builds a new string*

+ builds a new String whenever at least one of its operands is a String.

- **Grounding:** book passage
- **How `string_type` combines with `string_concatenation`:** + produces a new String whenever at least one operand is a String; the other operand is converted to text first.
- **How `string_concatenation` combines with `string_type`:** Concatenation always yields a String, even when one operand is a number, so its result cannot be used in arithmetic without parsing.

## Learned alongside (1)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

### `string_type` alongside `char`

*16-bit character primitive*

'a' is a char (one 16-bit character code, a primitive); "a" is a String (a sequence of characters, an object). 'a' + 'b' is the int 195, while "a" + "b" is "ab".

- **Grounding:** book passage

## Misconceptions (9)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### ArithmeticOnNumericStrings

- **Wrong rule:** "10" - 1 or "6" \* "2" works because the strings look like numbers.
- **Right rule:** Arithmetic operators other than + are not defined for Strings; a String of digits must first be converted to a number, e.g. with Integer.parseInt.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: "10" - 1 or "6" \* "2" works because the strings look like numbers. Right rule: Arithmetic operators other than + are not defined for Strings; a String of digits must first be converted to a number, e.g. with Integer.parseInt.
- **Also an edge from `arithmetic_operators`:** "10" - 1 or "6" \* "2" works because the strings look like numbers.

### EqualityOperatorComparesObjectsValues

- **Wrong rule:** s == t is true whenever the two Strings contain the same text.
- **Right rule:** s == t is true only when s and t refer to the same object; s.equals(t) compares the text.
- **Role of this concept:** context
- **Shows at level L0 as:** misconception: wrong rule: == compares contents (the String == bug). Right rule: s == t is true only when s and t refer to the same object; s.equals(t) compares the text.
- **Also an edge from `comparison_operators`:** s == t is true whenever the two Strings contain the same text.
- **Also an edge from `primitive_vs_reference`:** == compares contents (the String == bug)

### EqualsComparesReferences

- **Wrong rule:** s.equals(t) checks whether s and t are the same object.
- **Right rule:** s.equals(t) checks whether the two Strings contain the same characters.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: .equals() compares references, not contents. Right rule: s.equals(t) checks whether the two Strings contain the same characters.
- **Also an edge from `comparison_operators`:** .equals() compares references, not contents
- **Also an edge from `method_call`:** .equals() compares references, not contents

### NullIsObject

- **Wrong rule:** null is an object, so a method can be called on a variable that is null.
- **Right rule:** null means the variable refers to no object, so calling a method on it throws an exception.
- **Role of this concept:** primary

### ObjectsMustBeNamed

- **Wrong rule:** An object can only be created by first storing it in a variable.
- **Right rule:** An object can be created and used directly without a variable, as in "s".length() or passing new int[n] as an argument.
- **Role of this concept:** primary

### StringIsPrimitive

- **Wrong rule:** String is a primitive type like int.
- **Right rule:** String is not a primitive type; it is a class whose values are objects, although Java gives it some built-in support (literals, +).
- **Role of this concept:** context
- **Shows at level L0 as:** misconception: wrong rule: String is a primitive type like int. Right rule: String is not a primitive type; it is a class whose values are objects, although Java gives it some built-in support (literals, +).
- **Also an edge from `primitive_type`:** String is a primitive type like int.
- **Also an edge from `primitive_vs_reference`:** String is a primitive type like int.

### StringLiteralNoObject

- **Wrong rule:** "text" is not a String object until new String(...) is called.
- **Right rule:** A string literal is already a String object, so "text".length() works directly.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: a string literal isn't a String object until the constructor is called. Right rule: A string literal is already a String object, so "text".length() works directly.
- **Shows at level L0 as:** inconsistent trace: Points to LT (String expressions produce references to String objects, and operations build new strings). Applied unevenly, a student compares with equals in one test and == in another, or treats "12" as a number in one + and as text in the next. (here mixing in: "a string literal isn't a String object until the constructor is called")

### StringMethodChangesString

- **Wrong rule:** name.toUpperCase(); changes name.
- **Right rule:** Strings are immutable: String methods return a new String, which must be assigned, e.g. name = name.toUpperCase();
- **Role of this concept:** primary
- **Also an edge from `method_call`:** name.toUpperCase(); changes name.

### StringRelationalComparison

- **Wrong rule:** s &lt; t compares two Strings alphabetically.
- **Right rule:** &lt; and &gt; are defined only for primitive types; comparing Strings with them does not compile.
- **Role of this concept:** context
- **Shows at level L0 as:** misconception: wrong rule: s &lt; t compares two Strings alphabetically. Right rule: &lt; and &gt; are defined only for primitive types; comparing Strings with them does not compile.
- **Also an edge from `comparison_operators`:** s &lt; t compares two Strings alphabetically.

## Errors (0)

An error edge states the rule that gets broken in a program, and the right rule.

The graph has no error edge from this concept.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for string type: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to string type agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

string type -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (8 ways).

- **everyday reading** (folk-meaning rule): In everyday writing, quotes only mark words, "10" is the number ten, and two texts are 'equal' when they read the same. In Java a String is an object reached through a reference: "10" is text, + concatenates, and == compares references rather than contents.
- **misconception** (wrong rule / right rule; shows `StringLiteralNoObject`): wrong rule: a string literal isn't a String object until the constructor is called. Right rule: A string literal is already a String object, so "text".length() works directly.
- **misconception** (wrong rule / right rule; shows `EqualsComparesReferences`): wrong rule: .equals() compares references, not contents. Right rule: s.equals(t) checks whether the two Strings contain the same characters.
- **misconception** (wrong rule / right rule; shows `ArithmeticOnNumericStrings`): wrong rule: "10" - 1 or "6" \* "2" works because the strings look like numbers. Right rule: Arithmetic operators other than + are not defined for Strings; a String of digits must first be converted to a number, e.g. with Integer.parseInt.
- **inconsistent trace** (uneven-application rule; shows `StringLiteralNoObject`): Points to LT (String expressions produce references to String objects, and operations build new strings). Applied unevenly, a student compares with equals in one test and == in another, or treats "12" as a number in one + and as text in the next. (here mixing in: "a string literal isn't a String object until the constructor is called")
- **misconception** (wrong rule / right rule; shows `StringIsPrimitive`): wrong rule: String is a primitive type like int. Right rule: String is not a primitive type; it is a class whose values are objects, although Java gives it some built-in support (literals, +).
- **misconception** (wrong rule / right rule; shows `EqualityOperatorComparesObjectsValues`): wrong rule: == compares contents (the String == bug). Right rule: s == t is true only when s and t refer to the same object; s.equals(t) compares the text.
- **misconception** (wrong rule / right rule; shows `StringRelationalComparison`): wrong rule: s &lt; t compares two Strings alphabetically. Right rule: &lt; and &gt; are defined only for primitive types; comparing Strings with them does not compile.

### L1: Unistructural / atom x text surface

L1 for string type: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

string type -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

- **names the element** (identity rule): String: Java's built-in non-primitive (reference) type for a sequence of characters.
- **states the rule** (declarative rule): A String literal is characters in double quotes and denotes a String object. + concatenates. Contents are compared with equals, not ==. &lt; and &gt; are not defined for Strings, and Strings are immutable.

### L2: Multistructural / block x execution / preoperational

L2 for string type: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

string type -&gt; L2 (Multistructural): the answer applies the rules of string type to every part of the code, in order (3 ways).

- **line by line trace** (operational sequencing rule): A String expression is evaluated left to right. At each + with a String operand, the other operand is converted to a String and a new String object is made. Methods such as toUpperCase return a new String and leave the original unchanged.
- **output prediction** (evaluation / result rule): "Hi, " + "Bob" is "Hi, Bob" and "1234" + "99" is "123499". s.equals(t) is true exactly when the characters match, while "abc" == "ab" + x can be false for x = "c".
- **one step execution** (state-transition rule): No operation changes an existing String. s = s + "x" makes s refer to a new String, and other variables still referring to the old one are unaffected.

### L3: Relational / relations x function (concrete operational begins)

L3 for string type: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

string type -&gt; L3 (Relational): the answer relates the parts (3 ways).

- **relation to neighbour** (composition rule (with a neighbour)): + produces a new String whenever at least one operand is a String; the other operand is converted to text first.
- **relation to neighbour** (composition rule (with a neighbour)): 'a' is a char (one 16-bit character code, a primitive); "a" is a String (a sequence of characters, an object). 'a' + 'b' is the int 195, while "a" + "b" is "ab".
- **purpose of the whole** (plan / role rule): Strings handle all text: messages, labels, formatted output and command-line arguments (args[] are Strings and must be parsed before arithmetic).

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for string type: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

string type -&gt; L4 (Extended abstract): the answer reasons beyond the given code (6 ways).

- **predict a change** (conservation rule; shows `StringLiteralNoObject`): Replacing equals with == may still pass for two identical literals but fails for computed or input strings. Changing "5" to 5 turns concatenation into addition.
- **transfer to a new program** (applicability rule): Use String for any text: names, messages, tokens and output lines. Convert to int or double with Integer.parseInt or Double.parseDouble before arithmetic. Use char for a single character whose code matters.
- **diagnose an error** (error rule): rule broken: String contents are compared with equals; == compares references. Kind: silent logic error. Trigger class: Comparing a String read from input or built by + against a literal with == or !=: false even though the text matches.
- **diagnose an error** (error rule): rule broken: &lt; and &gt; (and - \* /) are defined only for primitive types, not for Strings. Kind: compile-time. Trigger class: s &lt; t, "10" - 1, "6" \* "2": 'bad operand types for binary operator'.
- **diagnose an error** (error rule): rule broken: A String variable can hold only a String (or null). Kind: compile-time. Trigger class: String message = 123;: 'incompatible types: int cannot be converted to String'.
- **diagnose an error** (error rule): rule broken: A method cannot be called through a null reference. Kind: run-time exception. Trigger class: Calling length(), equals() or charAt() on a String variable whose value is null: NullPointerException.

## Same topic

`string_type` belongs to the topic **Characters and strings** (`topic1.2.b`). The topic also contains: `char`, `char_arithmetic`, `escape_sequences`, `string_concatenation`.

## Rules of the concept (21)

- **folk-meaning rule:** In everyday writing, quotes only mark words, "10" is the number ten, and two texts are 'equal' when they read the same. In Java a String is an object reached through a reference: "10" is text, + concatenates, and == compares references rather than contents.
- **wrong rule / right rule:** EqualsComparesReferences: wrong: .equals() compares references, not contents \| right: s.equals(t) checks whether the two Strings contain the same characters.
- **wrong rule / right rule:** StringIsPrimitive: wrong: String is a primitive type like int. \| right: String is not a primitive type; it is a class whose values are objects, although Java gives it some built-in support (literals, +).
- **wrong rule / right rule:** StringLiteralNoObject: wrong: a string literal isn't a String object until the constructor is called \| right: A string literal is already a String object, so "text".length() works directly.
- **wrong rule / right rule:** EqualityOperatorComparesObjectsValues: wrong: == compares contents (the String == bug) \| right: s == t is true only when s and t refer to the same object; s.equals(t) compares the text.
- **wrong rule / right rule:** StringRelationalComparison: wrong: s &lt; t compares two Strings alphabetically. \| right: &lt; and &gt; are defined only for primitive types; comparing Strings with them does not compile.
- **wrong rule / right rule:** ArithmeticOnNumericStrings: wrong: "10" - 1 or "6" \* "2" works because the strings look like numbers. \| right: Arithmetic operators other than + are not defined for Strings; a String of digits must first be converted to a number, e.g. with Integer.parseInt.
- **uneven-application rule:** Points to LT (String expressions produce references to String objects, and operations build new strings). Applied unevenly, a student compares with equals in one test and == in another, or treats "12" as a number in one + and as text in the next.
- **identity rule:** String: Java's built-in non-primitive (reference) type for a sequence of characters.
- **declarative rule:** A String literal is characters in double quotes and denotes a String object. + concatenates. Contents are compared with equals, not ==. &lt; and &gt; are not defined for Strings, and Strings are immutable.
- **operational sequencing rule:** A String expression is evaluated left to right. At each + with a String operand, the other operand is converted to a String and a new String object is made. Methods such as toUpperCase return a new String and leave the original unchanged.
- **evaluation / result rule:** "Hi, " + "Bob" is "Hi, Bob" and "1234" + "99" is "123499". s.equals(t) is true exactly when the characters match, while "abc" == "ab" + x can be false for x = "c".
- **state-transition rule:** No operation changes an existing String. s = s + "x" makes s refer to a new String, and other variables still referring to the old one are unaffected.
- **composition rule (with a neighbour):** with string\_concatenation: + produces a new String whenever at least one operand is a String; the other operand is converted to text first.
- **plan / role rule:** Strings handle all text: messages, labels, formatted output and command-line arguments (args[] are Strings and must be parsed before arithmetic).
- **conservation rule:** Replacing equals with == may still pass for two identical literals but fails for computed or input strings. Changing "5" to 5 turns concatenation into addition.
- **error rule:** rule broken: String contents are compared with equals; == compares references. (silent logic error)
- **error rule:** rule broken: &lt; and &gt; (and - \* /) are defined only for primitive types, not for Strings. (compile-time)
- **error rule:** rule broken: A String variable can hold only a String (or null). (compile-time)
- **error rule:** rule broken: A method cannot be called through a null reference. (run-time exception)
- **applicability rule:** Use String for any text: names, messages, tokens and output lines. Convert to int or double with Integer.parseInt or Double.parseDouble before arithmetic. Use char for a single character whose code matters.

## The whole prerequisite chain

- **Everything it builds on (0):** nothing
- **Everything that builds on it (2):** `string_concatenation`, `string_conversion`
