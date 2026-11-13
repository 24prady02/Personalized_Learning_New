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

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 18 edges around this concept. The edge logic, the wrong and right rules and the exact rules of the ways are copied word for word from the graph.

## To work on (0)

Nothing is missing for this concept.

## What it needs first (1)

A prerequisite edge means the other concept has to be understood before `char`.

### `primitive_type` comes before `char`

*int, double, boolean, char*

- **Edge:** `pre:primitive_type->char`
- **Exact edge logic:** char is one of the eight primitive types, the one used for single characters.
- **Grounding:** book\_passage
- **Composition rule (R) of `char` with `primitive_type`:** char is one of the eight primitive types: the unsigned 16-bit integral one, used for single characters.
- **Composition rule (R) of `primitive_type` with `char`:** char is an integral primitive (16-bit unsigned UTF-16 code unit), so a char takes part in arithmetic as its numeric code.

## What it leads to (1)

These concepts need `char` first.

### `char` comes before `char_arithmetic`

*a char is a 16-bit number, so 'a' + 1 is an int*

- **Edge:** `pre:char->char_arithmetic`
- **Exact edge logic:** Char arithmetic uses the numeric code stored for each char.
- **Grounding:** book\_passage
- **Composition rule (R) of `char` with `char_arithmetic`:** Char arithmetic works on each char's numeric code and yields an int. A cast turns the result back into a character.
- **Composition rule (R) of `char_arithmetic` with `char`:** Char arithmetic uses each char's numeric code, so the result is an int, not a char, unless it is cast back.

## Learned alongside (4)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

### `char` alongside `boolean`

*true/false primitive*

- **Edge:** `par:boolean~char`
- **Exact edge logic:** A boolean holds true or false; a char holds a single character such as 'c'.
- **Grounding:** book\_passage
- **Composition rule (R) of `char` with `boolean`:** char and boolean are unrelated: there is no conversion or cast between them, and 'c' is never true or false.
- **Composition rule (R) of `boolean` with `char`:** char is a numeric (integral) type whose values can be compared ('a' &lt; 'b' is a boolean), whereas boolean is not numeric; neither converts to the other.

### `char` alongside `double`

*64-bit floating-point primitive*

- **Edge:** `par:double~char`
- **Exact edge logic:** A double holds a number with a fractional part; a char holds one character code, which is a whole number.
- **Grounding:** book\_passage
- **Composition rule (R) of `char` with `double`:** A char widens automatically to double (its code), but a double needs a cast to become a char. A char never holds a fractional part.
- **Composition rule (R) of `double` with `char`:** char is an integral numeric type, so a char widens automatically to double in arithmetic ('a' + 0.5 is 97.5), but a double needs an explicit cast to become a char.

### `char` alongside `int`

*32-bit integer primitive*

- **Edge:** `par:int~char`
- **Exact edge logic:** An int holds a whole number; a char holds one character, which Java stores as its numeric code.
- **Grounding:** book\_passage
- **Composition rule (R) of `char` with `int`:** A char is stored as an unsigned 16-bit code, so in arithmetic it acts as an int ('a' + 1 is 98). Going from int to char needs a cast.
- **Composition rule (R) of `int` with `char`:** In arithmetic a char is promoted to its int code. An int becomes a char only through a cast.

### `char` alongside `string_type`

*String -- a reference type, not a primitive*

- **Edge:** `par:char~string_type`
- **Exact edge logic:** 'a' is a char (one 16-bit character code, a primitive); "a" is a String (a sequence of characters, an object). 'a' + 'b' is the int 195, while "a" + "b" is "ab".
- **Grounding:** book\_passage

## Misconceptions (1)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### CharNotNumeric

- **Edge:** `char` &rarr; `CharNotNumeric` (misconception)
- **Exact edge logic (the wrong rule):** A char is only a letter, so c + k is an error.
- **Twin logic (the right rule):** A char is encoded as a 16-bit integer, so arithmetic such as 'b' + 'c' or 'a' + 4 works on the character codes.
- **Wrong belief (on the node):** char is not a numeric type
- **Correct rule (on the node):** A char is encoded as a 16-bit integer, so arithmetic such as 'b' + 'c' or 'a' + 4 works on the character codes.
- **Provenance:** published
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [1] misconception, exact rule:** wrong rule: char is not a numeric type. Right rule: A char is encoded as a 16-bit integer, so arithmetic such as 'b' + 'c' or 'a' + 4 works on the character codes.
- **L0 way [2] inconsistent\_trace, exact rule:** Points to LT (a char in arithmetic becomes its int code). Applied unevenly, a student treats 'b' + 'c' as 197 in one exercise but prints it as "bc" in another. (here mixing in: "char is not a numeric type")
- **Edge `char_arithmetic` &rarr; `CharNotNumeric`, exact edge logic:** char is not a numeric type **Twin logic:** A char is encoded as a 16-bit integer, so arithmetic such as 'b' + 'c' or 'a' + 4 works on the character codes. (role: context)

## Errors (0)

An error edge states the rule that gets broken in a program, and the right rule.

The graph has no error edge from this concept.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for char: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to char agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

- **Edge:** `char` &rarr; `char@L0` (has_level)
- **Exact edge logic:** char -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (3 ways).

Ways (3), each with its exact rule:

- **[0] everyday\_reading** (rule type E, folk-meaning rule): In everyday life '7' and 7 are the same thing, and a character is a letter, not a number. A Java char is a 16-bit numeric code: '7' has code 55, and 'a' + 1 is the int 98.
- **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `CharNotNumeric`: wrong rule: char is not a numeric type. Right rule: A char is encoded as a 16-bit integer, so arithmetic such as 'b' + 'c' or 'a' + 4 works on the character codes.
- **[2] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `CharNotNumeric`: Points to LT (a char in arithmetic becomes its int code). Applied unevenly, a student treats 'b' + 'c' as 197 in one exercise but prints it as "bc" in another. (here mixing in: "char is not a numeric type")

### L1: Unistructural / atom x text surface

L1 for char: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

- **Edge:** `char` &rarr; `char@L1` (has_level)
- **Exact edge logic:** char -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

Ways (2), each with its exact rule:

- **[0] names\_the\_element** (rule type N, identity rule): char: the primitive type for a single 16-bit Unicode character, such as 'a', '%' or '\n'.
- **[1] states\_the\_rule** (rule type S, declarative rule): A char literal is exactly one character (or one escape sequence) in single quotes. Values range from '\u0000' to '\uffff' (0 to 65535), and char is an integral type. A char literal is one character in single quotes ('a'); a String literal is any sequence in double quotes ("a"), so 'a' and "a" have different types and 'ab' does not compile.

### L2: Multistructural / block x execution / preoperational

L2 for char: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

- **Edge:** `char` &rarr; `char@L2` (has_level)
- **Exact edge logic:** char -&gt; L2 (Multistructural): the answer applies the rules of char to every part of the code, in order (3 ways).

Ways (3), each with its exact rule:

- **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): When a char meets an arithmetic operator, it is first promoted to int (its code) and the operation runs in int. Storing the result back in a char needs an explicit cast.
- **[1] output\_prediction** (rule type OP, evaluation / result rule): System.out.println('b') prints b. 'b' + 'c' is the int 197. (char) ('a' + 4) is 'e'.
- **[2] one\_step\_execution** (rule type OS, state-transition rule): c++ on char c = 'A' makes c 'B', because increment works on chars directly. c = c + 1; does not compile, because the right side is an int.

### L3: Relational / relations x function (concrete operational begins)

L3 for char: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

- **Edge:** `char` &rarr; `char@L3` (has_level)
- **Exact edge logic:** char -&gt; L3 (Relational): the answer relates the parts (7 ways).

Ways (7), each with its exact rule:

- **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): A char is stored as an unsigned 16-bit code, so in arithmetic it acts as an int ('a' + 1 is 98). Going from int to char needs a cast.
- **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): A char widens automatically to double (its code), but a double needs a cast to become a char. A char never holds a fractional part.
- **[2] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): char and boolean are unrelated: there is no conversion or cast between them, and 'c' is never true or false.
- **[3] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Char arithmetic works on each char's numeric code and yields an int. A cast turns the result back into a character.
- **[4] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): char is one of the eight primitive types: the unsigned 16-bit integral one, used for single characters.
- **[5] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): 'a' is a char (one 16-bit character code, a primitive); "a" is a String (a sequence of characters, an object). 'a' + 'b' is the int 195, while "a" + "b" is "ab".
- **[6] purpose\_of\_the\_whole** (rule type P, plan / role rule): A char holds one character: processing text one character at a time (charAt), looping over 'A'..'Z', or shifting letters in a cipher.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for char: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

- **Edge:** `char` &rarr; `char@L4` (has_level)
- **Exact edge logic:** char -&gt; L4 (Extended abstract): the answer reasons beyond the given code (5 ways).

Ways (5), each with its exact rule:

- **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `CharNotNumeric`: Changing 'A' to "A" changes the type to String, so + concatenates instead of adding. Changing a char variable to int keeps the arithmetic, but println then prints numbers instead of letters.
- **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Use char for one character from a literal or from charAt, especially when the character's code matters (alphabet loops, ciphers). Use String for text of any length.
- **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: A char literal holds exactly one character. Kind: compile-time. Trigger class: Several characters in single quotes ('ab') or a word in single quotes: 'unclosed character literal'.
- **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: int arithmetic on chars yields an int, which cannot go into a char without a cast. Kind: compile-time. Trigger class: char c = 'a' + i; or c = c + 1; with variable i: 'possible lossy conversion from int to char'.
- **[4] diagnose\_an\_error** (rule type D, error rule): rule broken: A char compares by its code, not by the digit or letter it shows. Kind: silent logic error. Trigger class: Comparing a char with an int as if it were a digit (seat &lt;= 3 for seat = 'A'), or printing c + 1 expecting a letter.

## Same topic

`char` belongs to the topic **Characters and strings** (`topic1.2.b`). The topic also contains: `char_arithmetic`, `escape_sequences`, `string_concatenation`, `string_type`.

## Rules of the concept (19)

- **Book** (SW-1e, p. 19 (pdf 29)): "A char is an alphanumeric character or symbol, like the ones that you type."
- **Book** (OT-Datatypes, ): "The char data type is a single 16-bit Unicode character."
- **E** (folk-meaning rule): In everyday life '7' and 7 are the same thing, and a character is a letter, not a number. A Java char is a 16-bit numeric code: '7' has code 55, and 'a' + 1 is the int 98.
- **M** (wrong rule / right rule): CharNotNumeric: wrong: char is not a numeric type \| right: A char is encoded as a 16-bit integer, so arithmetic such as 'b' + 'c' or 'a' + 4 works on the character codes.
- **T** (uneven-application rule): Points to LT (a char in arithmetic becomes its int code). Applied unevenly, a student treats 'b' + 'c' as 197 in one exercise but prints it as "bc" in another.
- **N** (identity rule): char: the primitive type for a single 16-bit Unicode character, such as 'a', '%' or '\n'.
- **S** (declarative rule): A char literal is exactly one character (or one escape sequence) in single quotes. Values range from '\u0000' to '\uffff' (0 to 65535), and char is an integral type. A char literal is one character in single quotes ('a'); a String literal is any sequence in double quotes ("a"), so 'a' and "a" have different types and 'ab' does not compile.
- **LT** (operational sequencing rule): When a char meets an arithmetic operator, it is first promoted to int (its code) and the operation runs in int. Storing the result back in a char needs an explicit cast.
- **OP** (evaluation / result rule): System.out.println('b') prints b. 'b' + 'c' is the int 197. (char) ('a' + 4) is 'e'.
- **OS** (state-transition rule): c++ on char c = 'A' makes c 'B', because increment works on chars directly. c = c + 1; does not compile, because the right side is an int.
- **R** (composition rule (with a neighbour)): with int: A char is stored as an unsigned 16-bit code, so in arithmetic it acts as an int ('a' + 1 is 98). Going from int to char needs a cast.
- **R** (composition rule (with a neighbour)): with double: A char widens automatically to double (its code), but a double needs a cast to become a char. A char never holds a fractional part.
- **R** (composition rule (with a neighbour)): with boolean: char and boolean are unrelated: there is no conversion or cast between them, and 'c' is never true or false.
- **R** (composition rule (with a neighbour)): with char\_arithmetic: Char arithmetic works on each char's numeric code and yields an int. A cast turns the result back into a character.
- **R** (composition rule (with a neighbour)): with primitive\_type: char is one of the eight primitive types: the unsigned 16-bit integral one, used for single characters.
- **P** (plan / role rule): A char holds one character: processing text one character at a time (charAt), looping over 'A'..'Z', or shifting letters in a cipher.
- **C** (conservation rule): Changing 'A' to "A" changes the type to String, so + concatenates instead of adding. Changing a char variable to int keeps the arithmetic, but println then prints numbers instead of letters.
- **D** (error rule): rule broken: A char literal holds exactly one character. (compile-time)
- **D** (error rule): rule broken: int arithmetic on chars yields an int, which cannot go into a char without a cast. (compile-time)
- **D** (error rule): rule broken: A char compares by its code, not by the digit or letter it shows. (silent logic error)
- **X** (applicability rule): Use char for one character from a literal or from charAt, especially when the character's code matters (alphabet loops, ciphers). Use String for text of any length.

## How it is found in code and answers (reader block)

- **Aliases:** char, character, chars
- **Code patterns:** `\bchar\b`, `'(?:\\.|[^'\\])'`
- **Operator symbols:** none
- **Java types:** `char`

## The whole prerequisite chain

- **Everything it builds on (2):** `data_type`, `primitive_type`
- **Everything that builds on it (1):** `char_arithmetic`

## Every edge in this view and its exact edge logic (18)

All the edges drawn in the picture, in the order: prerequisite, parallel, misconception, error, has_level, contains.

**1. `char` &rarr; `char_arithmetic`** (prerequisite)

- **Exact edge logic:** Char arithmetic uses the numeric code stored for each char.
- **Grounding:** book\_passage
- **Composition rule (R) of `char` with `char_arithmetic`:** Char arithmetic works on each char's numeric code and yields an int. A cast turns the result back into a character.
- **Composition rule (R) of `char_arithmetic` with `char`:** Char arithmetic uses each char's numeric code, so the result is an int, not a char, unless it is cast back.

**2. `primitive_type` &rarr; `char`** (prerequisite)

- **Exact edge logic:** char is one of the eight primitive types, the one used for single characters.
- **Grounding:** book\_passage
- **Composition rule (R) of `primitive_type` with `char`:** char is an integral primitive (16-bit unsigned UTF-16 code unit), so a char takes part in arithmetic as its numeric code.
- **Composition rule (R) of `char` with `primitive_type`:** char is one of the eight primitive types: the unsigned 16-bit integral one, used for single characters.

**3. `boolean` &harr; `char`** (parallel)

- **Exact edge logic:** A boolean holds true or false; a char holds a single character such as 'c'.
- **Grounding:** book\_passage
- **Composition rule (R) of `boolean` with `char`:** char is a numeric (integral) type whose values can be compared ('a' &lt; 'b' is a boolean), whereas boolean is not numeric; neither converts to the other.
- **Composition rule (R) of `char` with `boolean`:** char and boolean are unrelated: there is no conversion or cast between them, and 'c' is never true or false.

**4. `char` &harr; `string_type`** (parallel)

- **Exact edge logic:** 'a' is a char (one 16-bit character code, a primitive); "a" is a String (a sequence of characters, an object). 'a' + 'b' is the int 195, while "a" + "b" is "ab".
- **Grounding:** book\_passage

**5. `double` &harr; `char`** (parallel)

- **Exact edge logic:** A double holds a number with a fractional part; a char holds one character code, which is a whole number.
- **Grounding:** book\_passage
- **Composition rule (R) of `double` with `char`:** char is an integral numeric type, so a char widens automatically to double in arithmetic ('a' + 0.5 is 97.5), but a double needs an explicit cast to become a char.
- **Composition rule (R) of `char` with `double`:** A char widens automatically to double (its code), but a double needs a cast to become a char. A char never holds a fractional part.

**6. `int` &harr; `char`** (parallel)

- **Exact edge logic:** An int holds a whole number; a char holds one character, which Java stores as its numeric code.
- **Grounding:** book\_passage
- **Composition rule (R) of `int` with `char`:** In arithmetic a char is promoted to its int code. An int becomes a char only through a cast.
- **Composition rule (R) of `char` with `int`:** A char is stored as an unsigned 16-bit code, so in arithmetic it acts as an int ('a' + 1 is 98). Going from int to char needs a cast.

**7. `char` &rarr; `CharNotNumeric`** (misconception)

- **Exact edge logic (the wrong rule):** A char is only a letter, so c + k is an error.
- **Twin logic (the right rule):** A char is encoded as a 16-bit integer, so arithmetic such as 'b' + 'c' or 'a' + 4 works on the character codes.
- **Role:** primary

**8. `char_arithmetic` &rarr; `CharNotNumeric`** (misconception)

- **Exact edge logic (the wrong rule):** char is not a numeric type
- **Twin logic (the right rule):** A char is encoded as a 16-bit integer, so arithmetic such as 'b' + 'c' or 'a' + 4 works on the character codes.
- **Role:** context

**9. `char` &rarr; `char@L0`** (has_level)

- **Exact edge logic:** char -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (3 ways).
  - **[0] everyday\_reading** (rule type E, folk-meaning rule): In everyday life '7' and 7 are the same thing, and a character is a letter, not a number. A Java char is a 16-bit numeric code: '7' has code 55, and 'a' + 1 is the int 98.
  - **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `CharNotNumeric`: wrong rule: char is not a numeric type. Right rule: A char is encoded as a 16-bit integer, so arithmetic such as 'b' + 'c' or 'a' + 4 works on the character codes.
  - **[2] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `CharNotNumeric`: Points to LT (a char in arithmetic becomes its int code). Applied unevenly, a student treats 'b' + 'c' as 197 in one exercise but prints it as "bc" in another. (here mixing in: "char is not a numeric type")

**10. `char` &rarr; `char@L1`** (has_level)

- **Exact edge logic:** char -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).
  - **[0] names\_the\_element** (rule type N, identity rule): char: the primitive type for a single 16-bit Unicode character, such as 'a', '%' or '\n'.
  - **[1] states\_the\_rule** (rule type S, declarative rule): A char literal is exactly one character (or one escape sequence) in single quotes. Values range from '\u0000' to '\uffff' (0 to 65535), and char is an integral type. A char literal is one character in single quotes ('a'); a String literal is any sequence in double quotes ("a"), so 'a' and "a" have different types and 'ab' does not compile.

**11. `char` &rarr; `char@L2`** (has_level)

- **Exact edge logic:** char -&gt; L2 (Multistructural): the answer applies the rules of char to every part of the code, in order (3 ways).
  - **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): When a char meets an arithmetic operator, it is first promoted to int (its code) and the operation runs in int. Storing the result back in a char needs an explicit cast.
  - **[1] output\_prediction** (rule type OP, evaluation / result rule): System.out.println('b') prints b. 'b' + 'c' is the int 197. (char) ('a' + 4) is 'e'.
  - **[2] one\_step\_execution** (rule type OS, state-transition rule): c++ on char c = 'A' makes c 'B', because increment works on chars directly. c = c + 1; does not compile, because the right side is an int.

**12. `char` &rarr; `char@L3`** (has_level)

- **Exact edge logic:** char -&gt; L3 (Relational): the answer relates the parts (7 ways).
  - **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): A char is stored as an unsigned 16-bit code, so in arithmetic it acts as an int ('a' + 1 is 98). Going from int to char needs a cast.
  - **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): A char widens automatically to double (its code), but a double needs a cast to become a char. A char never holds a fractional part.
  - **[2] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): char and boolean are unrelated: there is no conversion or cast between them, and 'c' is never true or false.
  - **[3] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Char arithmetic works on each char's numeric code and yields an int. A cast turns the result back into a character.
  - **[4] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): char is one of the eight primitive types: the unsigned 16-bit integral one, used for single characters.
  - **[5] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): 'a' is a char (one 16-bit character code, a primitive); "a" is a String (a sequence of characters, an object). 'a' + 'b' is the int 195, while "a" + "b" is "ab".
  - **[6] purpose\_of\_the\_whole** (rule type P, plan / role rule): A char holds one character: processing text one character at a time (charAt), looping over 'A'..'Z', or shifting letters in a cipher.

**13. `char` &rarr; `char@L4`** (has_level)

- **Exact edge logic:** char -&gt; L4 (Extended abstract): the answer reasons beyond the given code (5 ways).
  - **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `CharNotNumeric`: Changing 'A' to "A" changes the type to String, so + concatenates instead of adding. Changing a char variable to int keeps the arithmetic, but println then prints numbers instead of letters.
  - **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Use char for one character from a literal or from charAt, especially when the character's code matters (alphabet loops, ciphers). Use String for text of any length.
  - **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: A char literal holds exactly one character. Kind: compile-time. Trigger class: Several characters in single quotes ('ab') or a word in single quotes: 'unclosed character literal'.
  - **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: int arithmetic on chars yields an int, which cannot go into a char without a cast. Kind: compile-time. Trigger class: char c = 'a' + i; or c = c + 1; with variable i: 'possible lossy conversion from int to char'.
  - **[4] diagnose\_an\_error** (rule type D, error rule): rule broken: A char compares by its code, not by the digit or letter it shows. Kind: silent logic error. Trigger class: Comparing a char with an int as if it were a digit (seat &lt;= 3 for seat = 'A'), or printing c + 1 expecting a letter.

**14. `topic1.2.b` &rarr; `char`** (contains)

- topic `topic1.2.b` contains `char`

**15. `topic1.2.b` &rarr; `char_arithmetic`** (contains)

- topic `topic1.2.b` contains `char_arithmetic`

**16. `topic1.2.b` &rarr; `escape_sequences`** (contains)

- topic `topic1.2.b` contains `escape_sequences`

**17. `topic1.2.b` &rarr; `string_concatenation`** (contains)

- topic `topic1.2.b` contains `string_concatenation`

**18. `topic1.2.b` &rarr; `string_type`** (contains)

- topic `topic1.2.b` contains `string_type`
