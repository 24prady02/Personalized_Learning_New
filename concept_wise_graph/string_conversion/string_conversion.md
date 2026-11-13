# string_conversion (`string_conversion`)

+ with a String converts the other operand to text

Section 1.2 Built-in Types of Data, topic 1.2.h Type conversion (automatic, cast, parsing).

![The knowledge graph around string_conversion](string_conversion.png)

## At a glance

- **Needs first:** `string_concatenation`
- **Leads to:** nothing
- **Learned alongside:** nothing
- **Misconceptions:** `StringPlusLeftToRight`
- **Errors:** none
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 14 edges around this concept. The edge logic, the wrong and right rules and the exact rules of the ways are copied word for word from the graph.

## To work on (1)

- no aliases: a student's words cannot name this concept

## What it needs first (1)

A prerequisite edge means the other concept has to be understood before `string_conversion`.

### `string_concatenation` comes before `string_conversion`

*+ with a String builds a new string*

- **Edge:** `pre:string_concatenation->string_conversion`
- **Exact edge logic:** When one operand of + is a String, Java converts the other operand to a String before concatenating.
- **Grounding:** book\_passage
- **Composition rule (R) of `string_conversion` with `string_concatenation`:** Conversion happens first, then concatenation: the non-String operand is turned into its characters before the two Strings are joined.
- **Composition rule (R) of `string_concatenation` with `string_conversion`:** The non-String operand is converted to its printed form (int 99 to "99", double 1.0 to "1.0", char 'a' to "a") before joining.

## What it leads to (0)

These concepts need `string_conversion` first.

No concept has this one as a prerequisite.

## Learned alongside (0)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

No parallel edge touches this concept.

## Misconceptions (1)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### StringPlusLeftToRight

- **Edge:** `string_conversion` &rarr; `StringPlusLeftToRight` (misconception)
- **Exact edge logic (the wrong rule):** 2 + 3 + "bc" and "bc" + 2 + 3 give the same text.
- **Twin logic (the right rule):** + is evaluated left to right: 2 + 3 + "bc" is "5bc" but "bc" + 2 + 3 is "bc23".
- **Wrong belief (on the node):** 2 + 3 + "bc" and "bc" + 2 + 3 give the same text.
- **Correct rule (on the node):** + is evaluated left to right: 2 + 3 + "bc" is "5bc" but "bc" + 2 + 3 is "bc23".
- **Provenance:** textbook
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [1] misconception, exact rule:** wrong rule: 2 + 3 + "bc" and "bc" + 2 + 3 give the same text. Right rule: + is evaluated left to right: 2 + 3 + "bc" is "5bc" but "bc" + 2 + 3 is "bc23".
- **L0 way [2] inconsistent\_trace, exact rule:** Points to LT (+ is applied left to right, each + deciding between addition and concatenation from its two operands at that moment). Applied unevenly: once a String has appeared the student goes back to numeric addition for later terms, or concatenates two numbers that come before any String. (here mixing in: "2 + 3 + "bc" and "bc" + 2 + 3 give the same text")
- **Edge `operator_precedence` &rarr; `StringPlusLeftToRight`, exact edge logic:** 2 + 3 + "bc" and "bc" + 2 + 3 give the same text. **Twin logic:** + is evaluated left to right: 2 + 3 + "bc" is "5bc" but "bc" + 2 + 3 is "bc23". (role: context)
- **Edge `string_concatenation` &rarr; `StringPlusLeftToRight`, exact edge logic:** 2 + 3 + "bc" and "bc" + 2 + 3 give the same text. **Twin logic:** + is evaluated left to right: 2 + 3 + "bc" is "5bc" but "bc" + 2 + 3 is "bc23". (role: context)

## Errors (0)

An error edge states the rule that gets broken in a program, and the right rule.

The graph has no error edge from this concept.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for string conversion: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to string conversion agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

- **Edge:** `string_conversion` &rarr; `string_conversion@L0` (has_level)
- **Exact edge logic:** string conversion -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (3 ways).

Ways (3), each with its exact rule:

- **[0] everyday\_reading** (rule type E, folk-meaning rule): Folk meaning: + is addition, which is commutative and associative, so 2 + 3 + "bc" and "bc" + 2 + 3 must give the same thing. Java rule: when one operand of + is a String the other is converted to a String and concatenated, and + is evaluated left to right, so 2 + 3 + "bc" is "5bc" but "bc" + 2 + 3 is "bc23".
- **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `StringPlusLeftToRight`: wrong rule: 2 + 3 + "bc" and "bc" + 2 + 3 give the same text. Right rule: + is evaluated left to right: 2 + 3 + "bc" is "5bc" but "bc" + 2 + 3 is "bc23".
- **[2] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `StringPlusLeftToRight`: Points to LT (+ is applied left to right, each + deciding between addition and concatenation from its two operands at that moment). Applied unevenly: once a String has appeared the student goes back to numeric addition for later terms, or concatenates two numbers that come before any String. (here mixing in: "2 + 3 + "bc" and "bc" + 2 + 3 give the same text")

### L1: Unistructural / atom x text surface

L1 for string conversion: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

- **Edge:** `string_conversion` &rarr; `string_conversion@L1` (has_level)
- **Exact edge logic:** string conversion -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

Ways (2), each with its exact rule:

- **[0] names\_the\_element** (rule type N, identity rule): String conversion is the automatic conversion of a non-String operand of + into its String form when the other operand is a String (also done for print/println arguments).
- **[1] states\_the\_rule** (rule type S, declarative rule): When either operand of + is a String, the other operand is converted to a String and the result is the characters of the first followed by those of the second; System.out.print and println also convert any argument to a String.

### L2: Multistructural / block x execution / preoperational

L2 for string conversion: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

- **Edge:** `string_conversion` &rarr; `string_conversion@L2` (has_level)
- **Exact edge logic:** string conversion -&gt; L2 (Multistructural): the answer applies the rules of string conversion to every part of the code, in order (3 ways).

Ways (3), each with its exact rule:

- **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): Evaluate + operators left to right (same precedence, left-associative): at each +, if either current operand is a String, convert the other and concatenate; otherwise add numerically. Parenthesized parts are evaluated first.
- **[1] output\_prediction** (rule type OP, evaluation / result rule): A String: 2 + "bc" is "2bc", 2 + 3 + "bc" is "5bc", "bc" + (2+3) is "bc5", "bc" + 2 + 3 is "bc23", "1234" + 99 is "123499".
- **[2] one\_step\_execution** (rule type OS, state-transition rule): Concatenation creates a new String and changes no variable; state changes only by assignment, e.g. String c = a + b; with a = "1234" and int b = 99 gives c the value "123499".

### L3: Relational / relations x function (concrete operational begins)

L3 for string conversion: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

- **Edge:** `string_conversion` &rarr; `string_conversion@L3` (has_level)
- **Exact edge logic:** string conversion -&gt; L3 (Relational): the answer relates the parts (2 ways).

Ways (2), each with its exact rule:

- **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Conversion happens first, then concatenation: the non-String operand is turned into its characters before the two Strings are joined.
- **[1] purpose\_of\_the\_whole** (rule type P, plan / role rule): Used to build output messages and labels from computed values, e.g. System.out.println(a + " + " + b + " = " + c);.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for string conversion: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

- **Edge:** `string_conversion` &rarr; `string_conversion@L4` (has_level)
- **Exact edge logic:** string conversion -&gt; L4 (Extended abstract): the answer reasons beyond the given code (4 ways).

Ways (4), each with its exact rule:

- **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `StringPlusLeftToRight`: Adding parentheses around the numeric part changes "bc23" into "bc5"; moving a String operand earlier turns every later + into concatenation; the order of operands matters, unlike numeric addition.
- **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Use string conversion with + to produce output and labels; do not use it to do arithmetic on numeric text (parse first), and parenthesize numeric parts that must be added before concatenation.
- **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: + is left-associative, so terms after a String are concatenated, not added. Kind: silent logic error. Trigger class: A numeric sum written after a String without parentheses, e.g. "Sum: " + a + b printing "Sum: 34" for a = 3, b = 4.
- **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: Only + converts to String; other arithmetic operators are not defined on Strings. Kind: compile-time. Trigger class: Using -, \*, / with a String operand, e.g. "Hello" - 1 or "12" \* 2.

## Same topic

`string_conversion` belongs to the topic **Type conversion (automatic, cast, parsing)** (`topic1.2.h`). The topic also contains: `explicit_cast`, `parsing`, `type_conversion`, `widening_conversion`.

## Rules of the concept (14)

- **Book** (SW-1e, p. 18 (pdf 28)): "whenever we use the + operator with a String as one of its operands, Java automatically converts the other to a String"
- **Book** (SW-1.2, ): "you can easily convert any type of data to a String by using the + operator."
- **E** (folk-meaning rule): Folk meaning: + is addition, which is commutative and associative, so 2 + 3 + "bc" and "bc" + 2 + 3 must give the same thing. Java rule: when one operand of + is a String the other is converted to a String and concatenated, and + is evaluated left to right, so 2 + 3 + "bc" is "5bc" but "bc" + 2 + 3 is "bc23".
- **M** (wrong rule / right rule): StringPlusLeftToRight: wrong: 2 + 3 + "bc" and "bc" + 2 + 3 give the same text. \| right: + is evaluated left to right: 2 + 3 + "bc" is "5bc" but "bc" + 2 + 3 is "bc23".
- **T** (uneven-application rule): Points to LT (+ is applied left to right, each + deciding between addition and concatenation from its two operands at that moment). Applied unevenly: once a String has appeared the student goes back to numeric addition for later terms, or concatenates two numbers that come before any String.
- **N** (identity rule): String conversion is the automatic conversion of a non-String operand of + into its String form when the other operand is a String (also done for print/println arguments).
- **S** (declarative rule): When either operand of + is a String, the other operand is converted to a String and the result is the characters of the first followed by those of the second; System.out.print and println also convert any argument to a String.
- **LT** (operational sequencing rule): Evaluate + operators left to right (same precedence, left-associative): at each +, if either current operand is a String, convert the other and concatenate; otherwise add numerically. Parenthesized parts are evaluated first.
- **OP** (evaluation / result rule): A String: 2 + "bc" is "2bc", 2 + 3 + "bc" is "5bc", "bc" + (2+3) is "bc5", "bc" + 2 + 3 is "bc23", "1234" + 99 is "123499".
- **OS** (state-transition rule): Concatenation creates a new String and changes no variable; state changes only by assignment, e.g. String c = a + b; with a = "1234" and int b = 99 gives c the value "123499".
- **R** (composition rule (with a neighbour)): with string\_concatenation: Conversion happens first, then concatenation: the non-String operand is turned into its characters before the two Strings are joined.
- **P** (plan / role rule): Used to build output messages and labels from computed values, e.g. System.out.println(a + " + " + b + " = " + c);.
- **C** (conservation rule): Adding parentheses around the numeric part changes "bc23" into "bc5"; moving a String operand earlier turns every later + into concatenation; the order of operands matters, unlike numeric addition.
- **D** (error rule): rule broken: + is left-associative, so terms after a String are concatenated, not added. (silent logic error)
- **D** (error rule): rule broken: Only + converts to String; other arithmetic operators are not defined on Strings. (compile-time)
- **X** (applicability rule): Use string conversion with + to produce output and labels; do not use it to do arithmetic on numeric text (parse first), and parenthesize numeric parts that must be added before concatenation.

## How it is found in code and answers (reader block)

- **Aliases:** none
- **Code patterns:** `\"\s*\+\s*(?:[a-z_]\w*|\d|\()`, `(?:[a-z_]\w*|\d|\))\s*\+\s*\"`, `String\.valueOf\s*\(`, `\b(?:Integer|Double|Long|Boolean|Character)\.toString\s*\(`
- **Operator symbols:** none
- **Java types:** none

## The whole prerequisite chain

- **Everything it builds on (2):** `string_concatenation`, `string_type`
- **Everything that builds on it (0):** nothing

## Every edge in this view and its exact edge logic (14)

All the edges drawn in the picture, in the order: prerequisite, parallel, misconception, error, has_level, contains.

**1. `string_concatenation` &rarr; `string_conversion`** (prerequisite)

- **Exact edge logic:** When one operand of + is a String, Java converts the other operand to a String before concatenating.
- **Grounding:** book\_passage
- **Composition rule (R) of `string_concatenation` with `string_conversion`:** The non-String operand is converted to its printed form (int 99 to "99", double 1.0 to "1.0", char 'a' to "a") before joining.
- **Composition rule (R) of `string_conversion` with `string_concatenation`:** Conversion happens first, then concatenation: the non-String operand is turned into its characters before the two Strings are joined.

**2. `string_conversion` &rarr; `StringPlusLeftToRight`** (misconception)

- **Exact edge logic (the wrong rule):** 2 + 3 + "bc" and "bc" + 2 + 3 give the same text.
- **Twin logic (the right rule):** + is evaluated left to right: 2 + 3 + "bc" is "5bc" but "bc" + 2 + 3 is "bc23".
- **Role:** primary

**3. `operator_precedence` &rarr; `StringPlusLeftToRight`** (misconception)

- **Exact edge logic (the wrong rule):** 2 + 3 + "bc" and "bc" + 2 + 3 give the same text.
- **Twin logic (the right rule):** + is evaluated left to right: 2 + 3 + "bc" is "5bc" but "bc" + 2 + 3 is "bc23".
- **Role:** context

**4. `string_concatenation` &rarr; `StringPlusLeftToRight`** (misconception)

- **Exact edge logic (the wrong rule):** 2 + 3 + "bc" and "bc" + 2 + 3 give the same text.
- **Twin logic (the right rule):** + is evaluated left to right: 2 + 3 + "bc" is "5bc" but "bc" + 2 + 3 is "bc23".
- **Role:** context

**5. `string_conversion` &rarr; `string_conversion@L0`** (has_level)

- **Exact edge logic:** string conversion -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (3 ways).
  - **[0] everyday\_reading** (rule type E, folk-meaning rule): Folk meaning: + is addition, which is commutative and associative, so 2 + 3 + "bc" and "bc" + 2 + 3 must give the same thing. Java rule: when one operand of + is a String the other is converted to a String and concatenated, and + is evaluated left to right, so 2 + 3 + "bc" is "5bc" but "bc" + 2 + 3 is "bc23".
  - **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `StringPlusLeftToRight`: wrong rule: 2 + 3 + "bc" and "bc" + 2 + 3 give the same text. Right rule: + is evaluated left to right: 2 + 3 + "bc" is "5bc" but "bc" + 2 + 3 is "bc23".
  - **[2] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `StringPlusLeftToRight`: Points to LT (+ is applied left to right, each + deciding between addition and concatenation from its two operands at that moment). Applied unevenly: once a String has appeared the student goes back to numeric addition for later terms, or concatenates two numbers that come before any String. (here mixing in: "2 + 3 + "bc" and "bc" + 2 + 3 give the same text")

**6. `string_conversion` &rarr; `string_conversion@L1`** (has_level)

- **Exact edge logic:** string conversion -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).
  - **[0] names\_the\_element** (rule type N, identity rule): String conversion is the automatic conversion of a non-String operand of + into its String form when the other operand is a String (also done for print/println arguments).
  - **[1] states\_the\_rule** (rule type S, declarative rule): When either operand of + is a String, the other operand is converted to a String and the result is the characters of the first followed by those of the second; System.out.print and println also convert any argument to a String.

**7. `string_conversion` &rarr; `string_conversion@L2`** (has_level)

- **Exact edge logic:** string conversion -&gt; L2 (Multistructural): the answer applies the rules of string conversion to every part of the code, in order (3 ways).
  - **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): Evaluate + operators left to right (same precedence, left-associative): at each +, if either current operand is a String, convert the other and concatenate; otherwise add numerically. Parenthesized parts are evaluated first.
  - **[1] output\_prediction** (rule type OP, evaluation / result rule): A String: 2 + "bc" is "2bc", 2 + 3 + "bc" is "5bc", "bc" + (2+3) is "bc5", "bc" + 2 + 3 is "bc23", "1234" + 99 is "123499".
  - **[2] one\_step\_execution** (rule type OS, state-transition rule): Concatenation creates a new String and changes no variable; state changes only by assignment, e.g. String c = a + b; with a = "1234" and int b = 99 gives c the value "123499".

**8. `string_conversion` &rarr; `string_conversion@L3`** (has_level)

- **Exact edge logic:** string conversion -&gt; L3 (Relational): the answer relates the parts (2 ways).
  - **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Conversion happens first, then concatenation: the non-String operand is turned into its characters before the two Strings are joined.
  - **[1] purpose\_of\_the\_whole** (rule type P, plan / role rule): Used to build output messages and labels from computed values, e.g. System.out.println(a + " + " + b + " = " + c);.

**9. `string_conversion` &rarr; `string_conversion@L4`** (has_level)

- **Exact edge logic:** string conversion -&gt; L4 (Extended abstract): the answer reasons beyond the given code (4 ways).
  - **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `StringPlusLeftToRight`: Adding parentheses around the numeric part changes "bc23" into "bc5"; moving a String operand earlier turns every later + into concatenation; the order of operands matters, unlike numeric addition.
  - **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Use string conversion with + to produce output and labels; do not use it to do arithmetic on numeric text (parse first), and parenthesize numeric parts that must be added before concatenation.
  - **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: + is left-associative, so terms after a String are concatenated, not added. Kind: silent logic error. Trigger class: A numeric sum written after a String without parentheses, e.g. "Sum: " + a + b printing "Sum: 34" for a = 3, b = 4.
  - **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: Only + converts to String; other arithmetic operators are not defined on Strings. Kind: compile-time. Trigger class: Using -, \*, / with a String operand, e.g. "Hello" - 1 or "12" \* 2.

**10. `topic1.2.h` &rarr; `string_conversion`** (contains)

- topic `topic1.2.h` contains `string_conversion`

**11. `topic1.2.h` &rarr; `explicit_cast`** (contains)

- topic `topic1.2.h` contains `explicit_cast`

**12. `topic1.2.h` &rarr; `parsing`** (contains)

- topic `topic1.2.h` contains `parsing`

**13. `topic1.2.h` &rarr; `type_conversion`** (contains)

- topic `topic1.2.h` contains `type_conversion`

**14. `topic1.2.h` &rarr; `widening_conversion`** (contains)

- topic `topic1.2.h` contains `widening_conversion`
