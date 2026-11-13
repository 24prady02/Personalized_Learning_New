# string_literal (`string_literal`)

"Hello, World" -- the text being printed

Section 1.1 Your First Program, topic 1.1.b Understanding a program (HelloWorld).

![The knowledge graph around string_literal](string_literal.png)

## At a glance

- **Needs first:** nothing
- **Leads to:** `escape_sequences`, `print`, `println`
- **Learned alongside:** nothing
- **Misconceptions:** `PrintedTextIsExecuted`
- **Errors:** `SingleQuotedString`, `StringLiteralSpansLines`, `UnclosedStringLiteral`
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 24 edges around this concept. The edge logic, the wrong and right rules and the exact rules of the ways are copied word for word from the graph.

## To work on (1)

- misconceptions with no L0 way linked to them: PrintedTextIsExecuted

## What it needs first (0)

A prerequisite edge means the other concept has to be understood before `string_literal`.

No prerequisite edge leads into this concept.

## What it leads to (3)

These concepts need `string_literal` first.

### `string_literal` comes before `escape_sequences`

*backslash codes inside literals: '\t' tab, '\n' newline*

- **Edge:** `pre:string_literal->escape_sequences`
- **Exact edge logic:** Escape sequences are written inside string or char literals.
- **Grounding:** book\_passage
- **Composition rule (R) of `string_literal` with `escape_sequences`:** Escape sequences (\n, \t, \", \\) are written inside string or char literals to stand for one character that cannot be typed directly.
- **Composition rule (R) of `escape_sequences` with `string_literal`:** Escapes are written inside "..." or '...'. \" puts a double quote inside a String literal without ending it.

### `string_literal` comes before `print`

*System.out.print -- output with no newline*

- **Edge:** `pre:string_literal->print`
- **Exact edge logic:** print("s") outputs exactly the characters between the quotes, without the quotes.
- **Grounding:** book\_passage
- **Composition rule (R) of `string_literal` with `print`:** print("s") outputs exactly the characters between the quotes, without the quotes.
- **Composition rule (R) of `print` with `string_literal`:** print("s") outputs exactly the characters between the quotes, without the quotes; spaces inside the quotes are printed.

### `string_literal` comes before `println`

*System.out.println -- output with a trailing newline*

- **Edge:** `pre:string_literal->println`
- **Exact edge logic:** println("s") outputs exactly the characters between the quotes and then ends the line.
- **Grounding:** book\_passage
- **Composition rule (R) of `string_literal` with `println`:** println("s") outputs exactly the characters between the quotes and then ends the line.
- **Composition rule (R) of `println` with `string_literal`:** println("s") outputs exactly the characters between the quotes and then ends the line.

## Learned alongside (0)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

No parallel edge touches this concept.

## Misconceptions (1)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### PrintedTextIsExecuted

- **Edge:** `string_literal` &rarr; `PrintedTextIsExecuted` (misconception)
- **Exact edge logic (the wrong rule):** System.out.println("x is 5"); sets x to 5 (text inside the quotes is run as code).
- **Twin logic (the right rule):** Characters inside double quotes are printed literally; println only displays them and changes no variable. Only an assignment such as x = 5; sets x.
- **Wrong belief (on the node):** System.out.println("x is 5"); sets x to 5 (text inside the quotes is run as code).
- **Correct rule (on the node):** Characters inside double quotes are printed literally; println only displays them and changes no variable. Only an assignment such as x = 5; sets x.
- **Provenance:** scenario
- **Role of this concept:** context
- **L0 way linked to it:** no
- **Edge `assignment` &rarr; `PrintedTextIsExecuted`, exact edge logic:** System.out.println("x is 5"); sets x to 5 (text inside the quotes is run as code). **Twin logic:** Characters inside double quotes are printed literally; println only displays them and changes no variable. Only an assignment such as x = 5; sets x. (role: context)
- **Edge `println` &rarr; `PrintedTextIsExecuted`, exact edge logic:** System.out.println("x is 5"); sets x to 5 (text inside the quotes is run as code). **Twin logic:** Characters inside double quotes are printed literally; println only displays them and changes no variable. Only an assignment such as x = 5; sets x. (role: primary)

## Errors (3)

An error edge states the rule that gets broken in a program, and the right rule.

### SingleQuotedString

- **Edge:** `string_literal` &rarr; `SingleQuotedString` (error)
- **Exact edge logic (the wrong rule):** Writes a string literal in single quotes: 'Hello'.
- **Twin logic (the right rule):** String literals use double quotes; single quotes are for one char.
- **Wrong belief (on the node):** Writes a string literal in single quotes: 'Hello'.
- **Correct rule (on the node):** String literals use double quotes; single quotes are for one char.
- **Provenance:** textbook
- **Role of this concept:** primary

### StringLiteralSpansLines

- **Edge:** `string_literal` &rarr; `StringLiteralSpansLines` (error)
- **Exact edge logic (the wrong rule):** Breaks a string literal across two lines of code.
- **Twin logic (the right rule):** String literals must not span more than one line of a program.
- **Wrong belief (on the node):** Breaks a string literal across two lines of code.
- **Correct rule (on the node):** String literals must not span more than one line of a program.
- **Provenance:** textbook
- **Role of this concept:** primary

### UnclosedStringLiteral

- **Edge:** `string_literal` &rarr; `UnclosedStringLiteral` (error)
- **Exact edge logic (the wrong rule):** A string literal can be left without its closing quote.
- **Twin logic (the right rule):** A String literal is enclosed in a pair of double quotes.
- **Wrong belief (on the node):** A string literal can be left without its closing quote.
- **Correct rule (on the node):** A String literal is enclosed in a pair of double quotes.
- **Provenance:** published
- **Role of this concept:** primary
- **Edge `compile_time_error` &rarr; `UnclosedStringLiteral`, exact edge logic:** A string literal can be left without its closing quote. **Twin logic:** A String literal is enclosed in a pair of double quotes. (role: context)

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for string literal: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to string literal agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

- **Edge:** `string_literal` &rarr; `string_literal@L0` (has_level)
- **Exact edge logic:** string literal -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (1 way).

Ways (1), each with its exact rule:

- **[0] everyday\_reading** (rule type E, folk-meaning rule): Everyday reading: quotation marks are just decoration, and spacing inside them is tidied up like ordinary text; single and double quotes mean the same thing. Java rule: characters within double quotes are taken literally (every space counts), the quotes are not part of the value, and single quotes are for one char.

### L1: Unistructural / atom x text surface

L1 for string literal: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

- **Edge:** `string_literal` &rarr; `string_literal@L1` (has_level)
- **Exact edge logic:** string literal -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

Ways (2), each with its exact rule:

- **[0] names\_the\_element** (rule type N, identity rule): A string literal is a sequence of characters written in double quotes in the source code, e.g. "Hello, World"; it is a value of type String.
- **[1] states\_the\_rule** (rule type S, declarative rule): A String literal is enclosed in a pair of double quotes; everything inside is taken literally, special characters such as " and newline are written with escape sequences, and the literal must close on the same source line.

### L2: Multistructural / block x execution / preoperational

L2 for string literal: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

- **Edge:** `string_literal` &rarr; `string_literal@L2` (has_level)
- **Exact edge logic:** string literal -&gt; L2 (Multistructural): the answer applies the rules of string literal to every part of the code, in order (3 ways).

Ways (3), each with its exact rule:

- **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): The literal is a constant: it is fixed at compile time and simply supplies its value when the expression containing it is evaluated.
- **[1] output\_prediction** (rule type OP, evaluation / result rule): Value is the String of the characters between the quotes (escape sequences replaced by the characters they stand for), without the quotes: "Hi, " has 4 characters, and printing it shows Hi, followed by a space.
- **[2] one\_step\_execution** (rule type OS, state-transition rule): Evaluating a literal changes no state; it just yields the same String value every time.

### L3: Relational / relations x function (concrete operational begins)

L3 for string literal: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

- **Edge:** `string_literal` &rarr; `string_literal@L3` (has_level)
- **Exact edge logic:** string literal -&gt; L3 (Relational): the answer relates the parts (4 ways).

Ways (4), each with its exact rule:

- **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): print("s") outputs exactly the characters between the quotes, without the quotes.
- **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): println("s") outputs exactly the characters between the quotes and then ends the line.
- **[2] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Escape sequences (\n, \t, \", \\) are written inside string or char literals to stand for one character that cannot be typed directly.
- **[3] purpose\_of\_the\_whole** (rule type P, plan / role rule): Purpose: state fixed text exactly, such as messages, labels and prompts, so you can precisely specify what gets printed.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for string literal: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

- **Edge:** `string_literal` &rarr; `string_literal@L4` (has_level)
- **Exact edge logic:** string literal -&gt; L4 (Extended abstract): the answer reasons beyond the given code (6 ways).

Ways (6), each with its exact rule:

- **[0] predict\_a\_change** (rule type C, conservation rule): Changing any character inside the quotes (including adding a space) changes the output by exactly that character; changing spaces outside the quotes changes nothing.
- **[1] diagnose\_an\_error** (rule type D, error rule): rule broken: A String literal is enclosed in a pair of double quotes. Kind: compile-time. Trigger class: a missing closing (or opening) quote; the compiler may get very confused and report errors elsewhere
- **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: String literals use double quotes; single quotes are for one char. Kind: compile-time. Trigger class: 'Hello' (more than one character in single quotes): unclosed character literal
- **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: A string literal must not span source lines. Kind: compile-time. Trigger class: a line break inside "...": unclosed string literal
- **[4] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Use a string literal for fixed text known when the program is written; use args, input or variables for text that varies between runs, and char literals for a single character.
- **[5] diagnose\_an\_error** (rule type D, error rule): rule broken: A double quote inside a string must be escaped. Kind: compile-time. Trigger class: "She said "Hi"" without \"

## Same topic

`string_literal` belongs to the topic **Understanding a program (HelloWorld)** (`topic1.1.b`). The topic also contains: `block`, `class_declaration`, `comment`, `main_method`, `print`, `println`, `program_layout`, `statement`.

## Rules of the concept (17)

- **Book** (SW-1e, p. 11 (pdf 21)): "things within quotes are taken literally so that you can precisely specify what gets printed."
- **Book** (RS, ): "String literals must not span more than one line of a program."
- **Book** (SW-1.1, ): "The key line with System.out.println() prints the text "Hello, World" in the terminal window."
- **E** (folk-meaning rule): Everyday reading: quotation marks are just decoration, and spacing inside them is tidied up like ordinary text; single and double quotes mean the same thing. Java rule: characters within double quotes are taken literally (every space counts), the quotes are not part of the value, and single quotes are for one char.
- **T** (uneven-application rule): Applies the literal rule unevenly: prints the quotes on one line but not another, or collapses spaces inside one string but keeps them in another.
- **N** (identity rule): A string literal is a sequence of characters written in double quotes in the source code, e.g. "Hello, World"; it is a value of type String.
- **S** (declarative rule): A String literal is enclosed in a pair of double quotes; everything inside is taken literally, special characters such as " and newline are written with escape sequences, and the literal must close on the same source line.
- **LT** (operational sequencing rule): The literal is a constant: it is fixed at compile time and simply supplies its value when the expression containing it is evaluated.
- **OP** (evaluation / result rule): Value is the String of the characters between the quotes (escape sequences replaced by the characters they stand for), without the quotes: "Hi, " has 4 characters, and printing it shows Hi, followed by a space.
- **OS** (state-transition rule): Evaluating a literal changes no state; it just yields the same String value every time.
- **R** (composition rule (with a neighbour)): with print: print("s") outputs exactly the characters between the quotes, without the quotes.
- **R** (composition rule (with a neighbour)): with println: println("s") outputs exactly the characters between the quotes and then ends the line.
- **R** (composition rule (with a neighbour)): with escape\_sequences: Escape sequences (\n, \t, \", \\) are written inside string or char literals to stand for one character that cannot be typed directly.
- **P** (plan / role rule): Purpose: state fixed text exactly, such as messages, labels and prompts, so you can precisely specify what gets printed.
- **C** (conservation rule): Changing any character inside the quotes (including adding a space) changes the output by exactly that character; changing spaces outside the quotes changes nothing.
- **D** (error rule): rule broken: String literals use double quotes; single quotes are for one char (compile-time)
- **D** (error rule): rule broken: A string literal must not span source lines (compile-time)
- **D** (error rule): rule broken: A String literal is enclosed in a pair of double quotes (compile-time)
- **D** (error rule): rule broken: A double quote inside a string must be escaped (compile-time)
- **X** (applicability rule): Use a string literal for fixed text known when the program is written; use args, input or variables for text that varies between runs, and char literals for a single character.

## How it is found in code and answers (reader block)

- **Aliases:** string literal, quotes, quotation marks, in quotes
- **Code patterns:** `\"(?:\\.|[^\"\\])*\"`
- **Operator symbols:** none
- **Java types:** none

## The whole prerequisite chain

- **Everything it builds on (0):** nothing
- **Everything that builds on it (4):** `escape_sequences`, `print`, `printing_array_reference`, `println`

## Every edge in this view and its exact edge logic (24)

All the edges drawn in the picture, in the order: prerequisite, parallel, misconception, error, has_level, contains.

**1. `string_literal` &rarr; `escape_sequences`** (prerequisite)

- **Exact edge logic:** Escape sequences are written inside string or char literals.
- **Grounding:** book\_passage
- **Composition rule (R) of `string_literal` with `escape_sequences`:** Escape sequences (\n, \t, \", \\) are written inside string or char literals to stand for one character that cannot be typed directly.
- **Composition rule (R) of `escape_sequences` with `string_literal`:** Escapes are written inside "..." or '...'. \" puts a double quote inside a String literal without ending it.

**2. `string_literal` &rarr; `print`** (prerequisite)

- **Exact edge logic:** print("s") outputs exactly the characters between the quotes, without the quotes.
- **Grounding:** book\_passage
- **Composition rule (R) of `string_literal` with `print`:** print("s") outputs exactly the characters between the quotes, without the quotes.
- **Composition rule (R) of `print` with `string_literal`:** print("s") outputs exactly the characters between the quotes, without the quotes; spaces inside the quotes are printed.

**3. `string_literal` &rarr; `println`** (prerequisite)

- **Exact edge logic:** println("s") outputs exactly the characters between the quotes and then ends the line.
- **Grounding:** book\_passage
- **Composition rule (R) of `string_literal` with `println`:** println("s") outputs exactly the characters between the quotes and then ends the line.
- **Composition rule (R) of `println` with `string_literal`:** println("s") outputs exactly the characters between the quotes and then ends the line.

**4. `string_literal` &rarr; `PrintedTextIsExecuted`** (misconception)

- **Exact edge logic (the wrong rule):** System.out.println("x is 5"); sets x to 5 (text inside the quotes is run as code).
- **Twin logic (the right rule):** Characters inside double quotes are printed literally; println only displays them and changes no variable. Only an assignment such as x = 5; sets x.
- **Role:** context

**5. `assignment` &rarr; `PrintedTextIsExecuted`** (misconception)

- **Exact edge logic (the wrong rule):** System.out.println("x is 5"); sets x to 5 (text inside the quotes is run as code).
- **Twin logic (the right rule):** Characters inside double quotes are printed literally; println only displays them and changes no variable. Only an assignment such as x = 5; sets x.
- **Role:** context

**6. `println` &rarr; `PrintedTextIsExecuted`** (misconception)

- **Exact edge logic (the wrong rule):** System.out.println("x is 5"); sets x to 5 (text inside the quotes is run as code).
- **Twin logic (the right rule):** Characters inside double quotes are printed literally; println only displays them and changes no variable. Only an assignment such as x = 5; sets x.
- **Role:** primary

**7. `string_literal` &rarr; `SingleQuotedString`** (error)

- **Exact edge logic (the wrong rule):** Writes a string literal in single quotes: 'Hello'.
- **Twin logic (the right rule):** String literals use double quotes; single quotes are for one char.
- **Role:** primary

**8. `string_literal` &rarr; `StringLiteralSpansLines`** (error)

- **Exact edge logic (the wrong rule):** Breaks a string literal across two lines of code.
- **Twin logic (the right rule):** String literals must not span more than one line of a program.
- **Role:** primary

**9. `string_literal` &rarr; `UnclosedStringLiteral`** (error)

- **Exact edge logic (the wrong rule):** A string literal can be left without its closing quote.
- **Twin logic (the right rule):** A String literal is enclosed in a pair of double quotes.
- **Role:** primary

**10. `compile_time_error` &rarr; `UnclosedStringLiteral`** (error)

- **Exact edge logic (the wrong rule):** A string literal can be left without its closing quote.
- **Twin logic (the right rule):** A String literal is enclosed in a pair of double quotes.
- **Role:** context

**11. `string_literal` &rarr; `string_literal@L0`** (has_level)

- **Exact edge logic:** string literal -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (1 way).
  - **[0] everyday\_reading** (rule type E, folk-meaning rule): Everyday reading: quotation marks are just decoration, and spacing inside them is tidied up like ordinary text; single and double quotes mean the same thing. Java rule: characters within double quotes are taken literally (every space counts), the quotes are not part of the value, and single quotes are for one char.

**12. `string_literal` &rarr; `string_literal@L1`** (has_level)

- **Exact edge logic:** string literal -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).
  - **[0] names\_the\_element** (rule type N, identity rule): A string literal is a sequence of characters written in double quotes in the source code, e.g. "Hello, World"; it is a value of type String.
  - **[1] states\_the\_rule** (rule type S, declarative rule): A String literal is enclosed in a pair of double quotes; everything inside is taken literally, special characters such as " and newline are written with escape sequences, and the literal must close on the same source line.

**13. `string_literal` &rarr; `string_literal@L2`** (has_level)

- **Exact edge logic:** string literal -&gt; L2 (Multistructural): the answer applies the rules of string literal to every part of the code, in order (3 ways).
  - **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): The literal is a constant: it is fixed at compile time and simply supplies its value when the expression containing it is evaluated.
  - **[1] output\_prediction** (rule type OP, evaluation / result rule): Value is the String of the characters between the quotes (escape sequences replaced by the characters they stand for), without the quotes: "Hi, " has 4 characters, and printing it shows Hi, followed by a space.
  - **[2] one\_step\_execution** (rule type OS, state-transition rule): Evaluating a literal changes no state; it just yields the same String value every time.

**14. `string_literal` &rarr; `string_literal@L3`** (has_level)

- **Exact edge logic:** string literal -&gt; L3 (Relational): the answer relates the parts (4 ways).
  - **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): print("s") outputs exactly the characters between the quotes, without the quotes.
  - **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): println("s") outputs exactly the characters between the quotes and then ends the line.
  - **[2] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Escape sequences (\n, \t, \", \\) are written inside string or char literals to stand for one character that cannot be typed directly.
  - **[3] purpose\_of\_the\_whole** (rule type P, plan / role rule): Purpose: state fixed text exactly, such as messages, labels and prompts, so you can precisely specify what gets printed.

**15. `string_literal` &rarr; `string_literal@L4`** (has_level)

- **Exact edge logic:** string literal -&gt; L4 (Extended abstract): the answer reasons beyond the given code (6 ways).
  - **[0] predict\_a\_change** (rule type C, conservation rule): Changing any character inside the quotes (including adding a space) changes the output by exactly that character; changing spaces outside the quotes changes nothing.
  - **[1] diagnose\_an\_error** (rule type D, error rule): rule broken: A String literal is enclosed in a pair of double quotes. Kind: compile-time. Trigger class: a missing closing (or opening) quote; the compiler may get very confused and report errors elsewhere
  - **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: String literals use double quotes; single quotes are for one char. Kind: compile-time. Trigger class: 'Hello' (more than one character in single quotes): unclosed character literal
  - **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: A string literal must not span source lines. Kind: compile-time. Trigger class: a line break inside "...": unclosed string literal
  - **[4] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Use a string literal for fixed text known when the program is written; use args, input or variables for text that varies between runs, and char literals for a single character.
  - **[5] diagnose\_an\_error** (rule type D, error rule): rule broken: A double quote inside a string must be escaped. Kind: compile-time. Trigger class: "She said "Hi"" without \"

**16. `topic1.1.b` &rarr; `string_literal`** (contains)

- topic `topic1.1.b` contains `string_literal`

**17. `topic1.1.b` &rarr; `block`** (contains)

- topic `topic1.1.b` contains `block`

**18. `topic1.1.b` &rarr; `class_declaration`** (contains)

- topic `topic1.1.b` contains `class_declaration`

**19. `topic1.1.b` &rarr; `comment`** (contains)

- topic `topic1.1.b` contains `comment`

**20. `topic1.1.b` &rarr; `main_method`** (contains)

- topic `topic1.1.b` contains `main_method`

**21. `topic1.1.b` &rarr; `print`** (contains)

- topic `topic1.1.b` contains `print`

**22. `topic1.1.b` &rarr; `println`** (contains)

- topic `topic1.1.b` contains `println`

**23. `topic1.1.b` &rarr; `program_layout`** (contains)

- topic `topic1.1.b` contains `program_layout`

**24. `topic1.1.b` &rarr; `statement`** (contains)

- topic `topic1.1.b` contains `statement`
