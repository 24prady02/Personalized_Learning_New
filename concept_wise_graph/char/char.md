# char (`char`)

16-bit character primitive

Section 1.2 Built-in Types of Data, topic 1.2.b Characters and strings.

![The knowledge graph around char](char.png)

## At a glance

- **Needs first:** `primitive_type`
- **Leads to:** `char_arithmetic`
- **Learned alongside:** `boolean`, `double`, `int`, `string_type`
- **Misconceptions:** `CharNotNumeric`
- **Errors:** none
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 18 edges around this concept, each explained in the graph's own words.

## What it needs first (1)

A prerequisite edge means the other concept has to be understood before `char`.

### `primitive_type` comes before `char`

*int, double, boolean, char*

char is one of the eight primitive types, the one used for single characters.

- **Grounding:** book passage
- **How `char` combines with `primitive_type`:** char is one of the eight primitive types: the unsigned 16-bit integral one, used for single characters.
- **How `primitive_type` combines with `char`:** char is an integral primitive (16-bit unsigned UTF-16 code unit), so a char takes part in arithmetic as its numeric code.

## What it leads to (1)

These concepts need `char` first.

### `char` comes before `char_arithmetic`

*a char is a 16-bit number, so 'a' + 1 is an int*

Char arithmetic uses the numeric code stored for each char.

- **Grounding:** book passage
- **How `char` combines with `char_arithmetic`:** Char arithmetic works on each char's numeric code and yields an int. A cast turns the result back into a character.
- **How `char_arithmetic` combines with `char`:** Char arithmetic uses each char's numeric code, so the result is an int, not a char, unless it is cast back.

## Learned alongside (4)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

### `char` alongside `boolean`

*true/false primitive*

A boolean holds true or false; a char holds a single character such as 'c'.

- **Grounding:** book passage
- **How `char` combines with `boolean`:** char and boolean are unrelated: there is no conversion or cast between them, and 'c' is never true or false.
- **How `boolean` combines with `char`:** char is a numeric (integral) type whose values can be compared ('a' &lt; 'b' is a boolean), whereas boolean is not numeric; neither converts to the other.

### `char` alongside `double`

*64-bit floating-point primitive*

A double holds a number with a fractional part; a char holds one character code, which is a whole number.

- **Grounding:** book passage
- **How `char` combines with `double`:** A char widens automatically to double (its code), but a double needs a cast to become a char. A char never holds a fractional part.
- **How `double` combines with `char`:** char is an integral numeric type, so a char widens automatically to double in arithmetic ('a' + 0.5 is 97.5), but a double needs an explicit cast to become a char.

### `char` alongside `int`

*32-bit integer primitive*

An int holds a whole number; a char holds one character, which Java stores as its numeric code.

- **Grounding:** book passage
- **How `char` combines with `int`:** A char is stored as an unsigned 16-bit code, so in arithmetic it acts as an int ('a' + 1 is 98). Going from int to char needs a cast.
- **How `int` combines with `char`:** In arithmetic a char is promoted to its int code. An int becomes a char only through a cast.

### `char` alongside `string_type`

*String -- a reference type, not a primitive*

'a' is a char (one 16-bit character code, a primitive); "a" is a String (a sequence of characters, an object). 'a' + 'b' is the int 195, while "a" + "b" is "ab".

- **Grounding:** book passage

## Misconceptions (1)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### CharNotNumeric

- **Wrong rule:** A char is only a letter, so c + k is an error.
- **Right rule:** A char is encoded as a 16-bit integer, so arithmetic such as 'b' + 'c' or 'a' + 4 works on the character codes.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: char is not a numeric type. Right rule: A char is encoded as a 16-bit integer, so arithmetic such as 'b' + 'c' or 'a' + 4 works on the character codes.
- **Shows at level L0 as:** inconsistent trace: Points to LT (a char in arithmetic becomes its int code). Applied unevenly, a student treats 'b' + 'c' as 197 in one exercise but prints it as "bc" in another. (here mixing in: "char is not a numeric type")
- **Also an edge from `char_arithmetic`:** char is not a numeric type

## Errors (0)

An error edge states the rule that gets broken in a program, and the right rule.

The graph has no error edge from this concept.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for char: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to char agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

char -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (3 ways).

- **everyday reading** (folk-meaning rule): In everyday life '7' and 7 are the same thing, and a character is a letter, not a number. A Java char is a 16-bit numeric code: '7' has code 55, and 'a' + 1 is the int 98.
- **misconception** (wrong rule / right rule; shows `CharNotNumeric`): wrong rule: char is not a numeric type. Right rule: A char is encoded as a 16-bit integer, so arithmetic such as 'b' + 'c' or 'a' + 4 works on the character codes.
- **inconsistent trace** (uneven-application rule; shows `CharNotNumeric`): Points to LT (a char in arithmetic becomes its int code). Applied unevenly, a student treats 'b' + 'c' as 197 in one exercise but prints it as "bc" in another. (here mixing in: "char is not a numeric type")

### L1: Unistructural / atom x text surface

L1 for char: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

char -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

- **names the element** (identity rule): char: the primitive type for a single 16-bit Unicode character, such as 'a', '%' or '\n'.
- **states the rule** (declarative rule): A char literal is exactly one character (or one escape sequence) in single quotes. Values range from '\u0000' to '\uffff' (0 to 65535), and char is an integral type. A char literal is one character in single quotes ('a'); a String literal is any sequence in double quotes ("a"), so 'a' and "a" have different types and 'ab' does not compile.

### L2: Multistructural / block x execution / preoperational

L2 for char: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

char -&gt; L2 (Multistructural): the answer applies the rules of char to every part of the code, in order (3 ways).

- **line by line trace** (operational sequencing rule): When a char meets an arithmetic operator, it is first promoted to int (its code) and the operation runs in int. Storing the result back in a char needs an explicit cast.
- **output prediction** (evaluation / result rule): System.out.println('b') prints b. 'b' + 'c' is the int 197. (char) ('a' + 4) is 'e'.
- **one step execution** (state-transition rule): c++ on char c = 'A' makes c 'B', because increment works on chars directly. c = c + 1; does not compile, because the right side is an int.

### L3: Relational / relations x function (concrete operational begins)

L3 for char: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

char -&gt; L3 (Relational): the answer relates the parts (7 ways).

- **relation to neighbour** (composition rule (with a neighbour)): A char is stored as an unsigned 16-bit code, so in arithmetic it acts as an int ('a' + 1 is 98). Going from int to char needs a cast.
- **relation to neighbour** (composition rule (with a neighbour)): A char widens automatically to double (its code), but a double needs a cast to become a char. A char never holds a fractional part.
- **relation to neighbour** (composition rule (with a neighbour)): char and boolean are unrelated: there is no conversion or cast between them, and 'c' is never true or false.
- **relation to neighbour** (composition rule (with a neighbour)): Char arithmetic works on each char's numeric code and yields an int. A cast turns the result back into a character.
- **relation to neighbour** (composition rule (with a neighbour)): char is one of the eight primitive types: the unsigned 16-bit integral one, used for single characters.
- **relation to neighbour** (composition rule (with a neighbour)): 'a' is a char (one 16-bit character code, a primitive); "a" is a String (a sequence of characters, an object). 'a' + 'b' is the int 195, while "a" + "b" is "ab".
- **purpose of the whole** (plan / role rule): A char holds one character: processing text one character at a time (charAt), looping over 'A'..'Z', or shifting letters in a cipher.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for char: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

char -&gt; L4 (Extended abstract): the answer reasons beyond the given code (5 ways).

- **predict a change** (conservation rule; shows `CharNotNumeric`): Changing 'A' to "A" changes the type to String, so + concatenates instead of adding. Changing a char variable to int keeps the arithmetic, but println then prints numbers instead of letters.
- **transfer to a new program** (applicability rule): Use char for one character from a literal or from charAt, especially when the character's code matters (alphabet loops, ciphers). Use String for text of any length.
- **diagnose an error** (error rule): rule broken: A char literal holds exactly one character. Kind: compile-time. Trigger class: Several characters in single quotes ('ab') or a word in single quotes: 'unclosed character literal'.
- **diagnose an error** (error rule): rule broken: int arithmetic on chars yields an int, which cannot go into a char without a cast. Kind: compile-time. Trigger class: char c = 'a' + i; or c = c + 1; with variable i: 'possible lossy conversion from int to char'.
- **diagnose an error** (error rule): rule broken: A char compares by its code, not by the digit or letter it shows. Kind: silent logic error. Trigger class: Comparing a char with an int as if it were a digit (seat &lt;= 3 for seat = 'A'), or printing c + 1 expecting a letter.

## Same topic

`char` belongs to the topic **Characters and strings** (`topic1.2.b`). The topic also contains: `char_arithmetic`, `escape_sequences`, `string_concatenation`, `string_type`.

## Rules of the concept (19)

- **folk-meaning rule:** In everyday life '7' and 7 are the same thing, and a character is a letter, not a number. A Java char is a 16-bit numeric code: '7' has code 55, and 'a' + 1 is the int 98.
- **wrong rule / right rule:** CharNotNumeric: wrong: char is not a numeric type \| right: A char is encoded as a 16-bit integer, so arithmetic such as 'b' + 'c' or 'a' + 4 works on the character codes.
- **uneven-application rule:** Points to LT (a char in arithmetic becomes its int code). Applied unevenly, a student treats 'b' + 'c' as 197 in one exercise but prints it as "bc" in another.
- **identity rule:** char: the primitive type for a single 16-bit Unicode character, such as 'a', '%' or '\n'.
- **declarative rule:** A char literal is exactly one character (or one escape sequence) in single quotes. Values range from '\u0000' to '\uffff' (0 to 65535), and char is an integral type. A char literal is one character in single quotes ('a'); a String literal is any sequence in double quotes ("a"), so 'a' and "a" have different types and 'ab' does not compile.
- **operational sequencing rule:** When a char meets an arithmetic operator, it is first promoted to int (its code) and the operation runs in int. Storing the result back in a char needs an explicit cast.
- **evaluation / result rule:** System.out.println('b') prints b. 'b' + 'c' is the int 197. (char) ('a' + 4) is 'e'.
- **state-transition rule:** c++ on char c = 'A' makes c 'B', because increment works on chars directly. c = c + 1; does not compile, because the right side is an int.
- **composition rule (with a neighbour):** with int: A char is stored as an unsigned 16-bit code, so in arithmetic it acts as an int ('a' + 1 is 98). Going from int to char needs a cast.
- **composition rule (with a neighbour):** with double: A char widens automatically to double (its code), but a double needs a cast to become a char. A char never holds a fractional part.
- **composition rule (with a neighbour):** with boolean: char and boolean are unrelated: there is no conversion or cast between them, and 'c' is never true or false.
- **composition rule (with a neighbour):** with char\_arithmetic: Char arithmetic works on each char's numeric code and yields an int. A cast turns the result back into a character.
- **composition rule (with a neighbour):** with primitive\_type: char is one of the eight primitive types: the unsigned 16-bit integral one, used for single characters.
- **plan / role rule:** A char holds one character: processing text one character at a time (charAt), looping over 'A'..'Z', or shifting letters in a cipher.
- **conservation rule:** Changing 'A' to "A" changes the type to String, so + concatenates instead of adding. Changing a char variable to int keeps the arithmetic, but println then prints numbers instead of letters.
- **error rule:** rule broken: A char literal holds exactly one character. (compile-time)
- **error rule:** rule broken: int arithmetic on chars yields an int, which cannot go into a char without a cast. (compile-time)
- **error rule:** rule broken: A char compares by its code, not by the digit or letter it shows. (silent logic error)
- **applicability rule:** Use char for one character from a literal or from charAt, especially when the character's code matters (alphabet loops, ciphers). Use String for text of any length.

## The whole prerequisite chain

- **Everything it builds on (2):** `data_type`, `primitive_type`
- **Everything that builds on it (1):** `char_arithmetic`
