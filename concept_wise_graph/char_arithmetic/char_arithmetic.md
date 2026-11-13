# char_arithmetic (`char_arithmetic`)

a char is a 16-bit number, so 'a' + 1 is an int

Section 1.2 Built-in Types of Data, topic 1.2.b Characters and strings.

![The knowledge graph around char_arithmetic](char_arithmetic.png)

## At a glance

- **Needs first:** `char`
- **Leads to:** nothing
- **Learned alongside:** nothing
- **Misconceptions:** `CharNotNumeric`
- **Errors:** none
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 13 edges around this concept, each explained in the graph's own words.

## What it needs first (1)

A prerequisite edge means the other concept has to be understood before `char_arithmetic`.

### `char` comes before `char_arithmetic`

*16-bit character primitive*

Char arithmetic uses the numeric code stored for each char.

- **Grounding:** book passage
- **How `char_arithmetic` combines with `char`:** Char arithmetic uses each char's numeric code, so the result is an int, not a char, unless it is cast back.
- **How `char` combines with `char_arithmetic`:** Char arithmetic works on each char's numeric code and yields an int. A cast turns the result back into a character.

## What it leads to (0)

These concepts need `char_arithmetic` first.

No concept has this one as a prerequisite.

## Learned alongside (0)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

No parallel edge touches this concept.

## Misconceptions (1)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### CharNotNumeric

- **Wrong rule:** char is not a numeric type
- **Right rule:** A char is encoded as a 16-bit integer, so arithmetic such as 'b' + 'c' or 'a' + 4 works on the character codes.
- **Role of this concept:** context
- **Shows at level L0 as:** misconception: wrong rule: char is not a numeric type. Right rule: A char is encoded as a 16-bit integer, so arithmetic such as 'b' + 'c' or 'a' + 4 works on the character codes.
- **Shows at level L0 as:** inconsistent trace: Points to LT (chars become int codes before the operator is applied). Applied unevenly, a student converts to codes in one step but keeps letters in another, e.g. printing 'b' + 'c' as "bc". (here mixing in: "char is not a numeric type")
- **Also an edge from `char`:** A char is only a letter, so c + k is an error.

## Errors (0)

An error edge states the rule that gets broken in a program, and the right rule.

The graph has no error edge from this concept.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for char arithmetic: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to char arithmetic agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

char arithmetic -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (3 ways).

- **everyday reading** (folk-meaning rule): In everyday use letters are not numbers, so 'a' + 1 seems meaningless or should give "a1". Java promotes each char to its int code, so 'a' + 1 is 98.
- **misconception** (wrong rule / right rule; shows `CharNotNumeric`): wrong rule: char is not a numeric type. Right rule: A char is encoded as a 16-bit integer, so arithmetic such as 'b' + 'c' or 'a' + 4 works on the character codes.
- **inconsistent trace** (uneven-application rule; shows `CharNotNumeric`): Points to LT (chars become int codes before the operator is applied). Applied unevenly, a student converts to codes in one step but keeps letters in another, e.g. printing 'b' + 'c' as "bc". (here mixing in: "char is not a numeric type")

### L1: Unistructural / atom x text surface

L1 for char arithmetic: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

char arithmetic -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

- **names the element** (identity rule): Char arithmetic: applying arithmetic or comparison operators to char values, which act on their Unicode codes.
- **states the rule** (declarative rule): char operands of arithmetic are promoted to int, so the result is an int. Casting an int to char gives the character with that code. ++, -- and comparisons work directly on chars.

### L2: Multistructural / block x execution / preoperational

L2 for char arithmetic: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

char arithmetic -&gt; L2 (Multistructural): the answer applies the rules of char arithmetic to every part of the code, in order (3 ways).

- **line by line trace** (operational sequencing rule): Each char operand is replaced by its code (promoted to int) and the operation runs in int. A cast written outside the parentheses, as in (char) ('a' + 4), is applied last.
- **output prediction** (evaluation / result rule): 'b' + 'c' is the int 197. 'a' + 4 is 101. (char) ('a' + 4) is 'e'. 'A' &lt; 'a' is true.
- **one step execution** (state-transition rule): For char c = 'A', c++ sets c to 'B'. c = c + 1; is rejected, because the right side is an int.

### L3: Relational / relations x function (concrete operational begins)

L3 for char arithmetic: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

char arithmetic -&gt; L3 (Relational): the answer relates the parts (2 ways).

- **relation to neighbour** (composition rule (with a neighbour)): Char arithmetic uses each char's numeric code, so the result is an int, not a char, unless it is cast back.
- **purpose of the whole** (plan / role rule): Plans: shifting letters (Caesar cipher), turning a digit char into its value (c - '0'), looping over 'A'..'Z', and testing whether a char is in a range.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for char arithmetic: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

char arithmetic -&gt; L4 (Extended abstract): the answer reasons beyond the given code (5 ways).

- **predict a change** (conservation rule; shows `CharNotNumeric`): Adding or removing the (char) cast changes the output from a number to a letter. Changing 'a' + 4 to "a" + 4 makes it concatenation ("a4").
- **transfer to a new program** (applicability rule): Use char arithmetic when the computation depends on character order or codes (alphabet loops, ciphers, digit values). To join characters into text, use String + or a String instead.
- **diagnose an error** (error rule): rule broken: Arithmetic on chars yields an int, which needs a cast to go back into a char. Kind: compile-time. Trigger class: char next = c + 1; or char d = 'a' + k;: 'possible lossy conversion from int to char'.
- **diagnose an error** (error rule): rule broken: Without a cast the int code is printed, not the letter. Kind: silent logic error. Trigger class: Printing c + 1 or 'a' + i when a letter was expected.
- **diagnose an error** (error rule): rule broken: A char compares by its code, not by the digit it shows. Kind: silent logic error. Trigger class: Comparing a char with an int as if it were a digit (seat &lt;= 3 for seat = 'A').

## Same topic

`char_arithmetic` belongs to the topic **Characters and strings** (`topic1.2.b`). The topic also contains: `char`, `escape_sequences`, `string_concatenation`, `string_type`.

## Rules of the concept (15)

- **folk-meaning rule:** In everyday use letters are not numbers, so 'a' + 1 seems meaningless or should give "a1". Java promotes each char to its int code, so 'a' + 1 is 98.
- **wrong rule / right rule:** CharNotNumeric: wrong: char is not a numeric type \| right: A char is encoded as a 16-bit integer, so arithmetic such as 'b' + 'c' or 'a' + 4 works on the character codes.
- **uneven-application rule:** Points to LT (chars become int codes before the operator is applied). Applied unevenly, a student converts to codes in one step but keeps letters in another, e.g. printing 'b' + 'c' as "bc".
- **identity rule:** Char arithmetic: applying arithmetic or comparison operators to char values, which act on their Unicode codes.
- **declarative rule:** char operands of arithmetic are promoted to int, so the result is an int. Casting an int to char gives the character with that code. ++, -- and comparisons work directly on chars.
- **operational sequencing rule:** Each char operand is replaced by its code (promoted to int) and the operation runs in int. A cast written outside the parentheses, as in (char) ('a' + 4), is applied last.
- **evaluation / result rule:** 'b' + 'c' is the int 197. 'a' + 4 is 101. (char) ('a' + 4) is 'e'. 'A' &lt; 'a' is true.
- **state-transition rule:** For char c = 'A', c++ sets c to 'B'. c = c + 1; is rejected, because the right side is an int.
- **composition rule (with a neighbour):** with char: Char arithmetic uses each char's numeric code, so the result is an int, not a char, unless it is cast back.
- **plan / role rule:** Plans: shifting letters (Caesar cipher), turning a digit char into its value (c - '0'), looping over 'A'..'Z', and testing whether a char is in a range.
- **conservation rule:** Adding or removing the (char) cast changes the output from a number to a letter. Changing 'a' + 4 to "a" + 4 makes it concatenation ("a4").
- **error rule:** rule broken: Arithmetic on chars yields an int, which needs a cast to go back into a char. (compile-time)
- **error rule:** rule broken: Without a cast the int code is printed, not the letter. (silent logic error)
- **error rule:** rule broken: A char compares by its code, not by the digit it shows. (silent logic error)
- **applicability rule:** Use char arithmetic when the computation depends on character order or codes (alphabet loops, ciphers, digit values). To join characters into text, use String + or a String instead.

## The whole prerequisite chain

- **Everything it builds on (3):** `char`, `data_type`, `primitive_type`
- **Everything that builds on it (0):** nothing
