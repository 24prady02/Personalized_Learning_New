# comment (`comment`)

// and /\* \*/ text that the compiler ignores

Section 1.1 Your First Program, topic 1.1.b Understanding a program (HelloWorld).

![The knowledge graph around comment](comment.png)

## At a glance

- **Needs first:** `program_text`
- **Leads to:** nothing
- **Learned alongside:** nothing
- **Misconceptions:** `CommentIsExecuted`
- **Errors:** `SpacedCommentDelimiter`, `UnclosedComment`
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 19 edges around this concept. The edge logic, the wrong and right rules and the exact rules of the ways are copied word for word from the graph.

## To work on (0)

Nothing is missing for this concept.

## What it needs first (1)

A prerequisite edge means the other concept has to be understood before `comment`.

### `program_text` comes before `comment`

*the source file; class name must match the filename*

- **Edge:** `pre:program_text->comment`
- **Exact edge logic:** Comments are part of the program text in Name.java but are ignored when it is compiled.
- **Grounding:** book\_passage
- **Composition rule (R) of `comment` with `program_text`:** Comments are part of the program text in Name.java but are dropped when it is compiled, so they cannot affect Name.class's behaviour.
- **Composition rule (R) of `program_text` with `comment`:** Comments are part of the program text but are discarded when it is compiled: they may appear anywhere a whitespace may appear and never change Name.class's behaviour.

## What it leads to (0)

These concepts need `comment` first.

No concept has this one as a prerequisite.

## Learned alongside (0)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

No parallel edge touches this concept.

## Misconceptions (1)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### CommentIsExecuted

- **Edge:** `comment` &rarr; `CommentIsExecuted` (misconception)
- **Exact edge logic (the wrong rule):** A comment line is run like a statement.
- **Twin logic (the right rule):** The compiler ignores comments: everything from // to the end of the line and everything between /\* and \*/.
- **Wrong belief (on the node):** A comment line is run like a statement.
- **Correct rule (on the node):** The compiler ignores comments: everything from // to the end of the line and everything between /\* and \*/.
- **Provenance:** textbook
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [1] misconception, exact rule:** wrong rule: A comment line is run like a statement. Right rule: The compiler ignores comments: everything from // to the end of the line and everything between /\* and \*/.
- **L0 way [2] inconsistent\_trace, exact rule:** Applies the skip rule unevenly: skips one comment while tracing but 'executes' another (e.g. a commented-out println), or forgets that // ends at the line break. (here mixing in: "A comment line is run like a statement")

## Errors (2)

An error edge states the rule that gets broken in a program, and the right rule.

### SpacedCommentDelimiter

- **Edge:** `comment` &rarr; `SpacedCommentDelimiter` (error)
- **Exact edge logic (the wrong rule):** Writes / \* comment \* / with spaces inside the delimiters.
- **Twin logic (the right rule):** The delimiters /\* and \*/ must be written without spaces.
- **Wrong belief (on the node):** Writes / \* comment \* / with spaces inside the delimiters.
- **Correct rule (on the node):** The delimiters /\* and \*/ must be written without spaces.
- **Provenance:** textbook
- **Role of this concept:** primary

### UnclosedComment

- **Edge:** `comment` &rarr; `UnclosedComment` (error)
- **Exact edge logic (the wrong rule):** Opens a comment with /\* and never closes it.
- **Twin logic (the right rule):** A /\* comment is the text between /\* and \*/, so the closing \*/ is required.
- **Wrong belief (on the node):** Opens a comment with /\* and never closes it.
- **Correct rule (on the node):** A /\* comment is the text between /\* and \*/, so the closing \*/ is required.
- **Provenance:** textbook
- **Role of this concept:** primary
- **Edge `compile_time_error` &rarr; `UnclosedComment`, exact edge logic:** Opens a comment with /\* and never closes it. **Twin logic:** A /\* comment is the text between /\* and \*/, so the closing \*/ is required. (role: context)

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for comment: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to comment agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

- **Edge:** `comment` &rarr; `comment@L0` (has_level)
- **Exact edge logic:** comment -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (3 ways).

Ways (3), each with its exact rule:

- **[0] everyday\_reading** (rule type E, folk-meaning rule): Everyday reading: text written in a program is an instruction the computer reads and obeys. Java rule: comments (// to end of line, /\* ... \*/) are ignored by the compiler and have no effect on execution; they are for human readers.
- **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `CommentIsExecuted`: wrong rule: A comment line is run like a statement. Right rule: The compiler ignores comments: everything from // to the end of the line and everything between /\* and \*/.
- **[2] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `CommentIsExecuted`: Applies the skip rule unevenly: skips one comment while tracing but 'executes' another (e.g. a commented-out println), or forgets that // ends at the line break. (here mixing in: "A comment line is run like a statement")

### L1: Unistructural / atom x text surface

L1 for comment: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

- **Edge:** `comment` &rarr; `comment@L1` (has_level)
- **Exact edge logic:** comment -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

Ways (2), each with its exact rule:

- **[0] names\_the\_element** (rule type N, identity rule): A comment is explanatory text in the program that the compiler ignores.
- **[1] states\_the\_rule** (rule type S, declarative rule): A comment is either text between /\* and \*/ or text from // to the end of the line; the compiler ignores it. A comment that starts with /\*\* is a documentation (Javadoc) comment, written before a class or method; tools turn it into API documentation.

### L2: Multistructural / block x execution / preoperational

L2 for comment: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

- **Edge:** `comment` &rarr; `comment@L2` (has_level)
- **Exact edge logic:** comment -&gt; L2 (Multistructural): the answer applies the rules of comment to every part of the code, in order (3 ways).

Ways (3), each with its exact rule:

- **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): Comments are removed when the source is read by the compiler, so they never take part in execution order; tracing skips them.
- **[1] output\_prediction** (rule type OP, evaluation / result rule): A comment produces no value and no output.
- **[2] one\_step\_execution** (rule type OS, state-transition rule): A comment changes no state; adding one and recompiling leaves the program's behaviour identical.

### L3: Relational / relations x function (concrete operational begins)

L3 for comment: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

- **Edge:** `comment` &rarr; `comment@L3` (has_level)
- **Exact edge logic:** comment -&gt; L3 (Relational): the answer relates the parts (2 ways).

Ways (2), each with its exact rule:

- **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Comments are part of the program text in Name.java but are dropped when it is compiled, so they cannot affect Name.class's behaviour.
- **[1] purpose\_of\_the\_whole** (rule type P, plan / role rule): Purpose: explain what the code does and why, for other programmers and your future self; also used to disable code temporarily.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for comment: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

- **Edge:** `comment` &rarr; `comment@L4` (has_level)
- **Exact edge logic:** comment -&gt; L4 (Extended abstract): the answer reasons beyond the given code (4 ways).

Ways (4), each with its exact rule:

- **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `CommentIsExecuted`: Adding, removing or editing a comment keeps behaviour unchanged, as long as the delimiters stay intact; deleting a closing \*/ or turning a statement into a comment changes the program.
- **[1] diagnose\_an\_error** (rule type D, error rule): rule broken: A /\* comment needs its closing \*/. Kind: compile-time. Trigger class: a /\* with no matching \*/: the rest of the file becomes comment, so javac reports an unclosed comment or reached end of file
- **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: /\* and \*/ are two-character tokens with no space inside. Kind: compile-time. Trigger class: writing / \* ... \* /: the slashes and stars are read as operators, producing syntax errors
- **[3] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Use comments to document intent where the code alone is unclear; do not rely on them to change what the program does, and keep them in step with the code.

## Same topic

`comment` belongs to the topic **Understanding a program (HelloWorld)** (`topic1.1.b`). The topic also contains: `block`, `class_declaration`, `main_method`, `print`, `println`, `program_layout`, `statement`, `string_literal`.

## Rules of the concept (14)

- **Book** (SW-1e, p. 10 (pdf 20)): "A comment is either text in between /\* and \*/ or at the end of a line after //."
- **Book** (SW-1e, p. 10 (pdf 20)): "They denote comments, which are ignored by the compiler."
- **Book** (OT-Hello, ): "Comments are ignored by the compiler but are useful to other programmers."
- **Book** (OT-Hello, ): "// text The compiler ignores everything from // to the end of the line."
- **Book** (RS, ): "The only thing you aren't allowed to put inside a comment is the comment end character(s)."
- **E** (folk-meaning rule): Everyday reading: text written in a program is an instruction the computer reads and obeys. Java rule: comments (// to end of line, /\* ... \*/) are ignored by the compiler and have no effect on execution; they are for human readers.
- **M** (wrong rule / right rule): CommentIsExecuted: wrong: A comment line is run like a statement. \| right: The compiler ignores comments: everything from // to the end of the line and everything between /\* and \*/.
- **T** (uneven-application rule): Applies the skip rule unevenly: skips one comment while tracing but 'executes' another (e.g. a commented-out println), or forgets that // ends at the line break.
- **N** (identity rule): A comment is explanatory text in the program that the compiler ignores.
- **S** (declarative rule): A comment is either text between /\* and \*/ or text from // to the end of the line; the compiler ignores it. A comment that starts with /\*\* is a documentation (Javadoc) comment, written before a class or method; tools turn it into API documentation.
- **LT** (operational sequencing rule): Comments are removed when the source is read by the compiler, so they never take part in execution order; tracing skips them.
- **OP** (evaluation / result rule): A comment produces no value and no output.
- **OS** (state-transition rule): A comment changes no state; adding one and recompiling leaves the program's behaviour identical.
- **R** (composition rule (with a neighbour)): with program\_text: Comments are part of the program text in Name.java but are dropped when it is compiled, so they cannot affect Name.class's behaviour.
- **P** (plan / role rule): Purpose: explain what the code does and why, for other programmers and your future self; also used to disable code temporarily.
- **C** (conservation rule): Adding, removing or editing a comment keeps behaviour unchanged, as long as the delimiters stay intact; deleting a closing \*/ or turning a statement into a comment changes the program.
- **D** (error rule): rule broken: /\* and \*/ are two-character tokens with no space inside (compile-time)
- **D** (error rule): rule broken: A /\* comment needs its closing \*/ (compile-time)
- **X** (applicability rule): Use comments to document intent where the code alone is unclear; do not rely on them to change what the program does, and keep them in step with the code.

## How it is found in code and answers (reader block)

- **Aliases:** comment, comments
- **Code patterns:** `//`, `/\*`
- **Operator symbols:** none
- **Java types:** none

## The whole prerequisite chain

- **Everything it builds on (1):** `program_text`
- **Everything that builds on it (0):** nothing

## Every edge in this view and its exact edge logic (19)

All the edges drawn in the picture, in the order: prerequisite, parallel, misconception, error, has_level, contains.

**1. `program_text` &rarr; `comment`** (prerequisite)

- **Exact edge logic:** Comments are part of the program text in Name.java but are ignored when it is compiled.
- **Grounding:** book\_passage
- **Composition rule (R) of `program_text` with `comment`:** Comments are part of the program text but are discarded when it is compiled: they may appear anywhere a whitespace may appear and never change Name.class's behaviour.
- **Composition rule (R) of `comment` with `program_text`:** Comments are part of the program text in Name.java but are dropped when it is compiled, so they cannot affect Name.class's behaviour.

**2. `comment` &rarr; `CommentIsExecuted`** (misconception)

- **Exact edge logic (the wrong rule):** A comment line is run like a statement.
- **Twin logic (the right rule):** The compiler ignores comments: everything from // to the end of the line and everything between /\* and \*/.
- **Role:** primary

**3. `comment` &rarr; `SpacedCommentDelimiter`** (error)

- **Exact edge logic (the wrong rule):** Writes / \* comment \* / with spaces inside the delimiters.
- **Twin logic (the right rule):** The delimiters /\* and \*/ must be written without spaces.
- **Role:** primary

**4. `comment` &rarr; `UnclosedComment`** (error)

- **Exact edge logic (the wrong rule):** Opens a comment with /\* and never closes it.
- **Twin logic (the right rule):** A /\* comment is the text between /\* and \*/, so the closing \*/ is required.
- **Role:** primary

**5. `compile_time_error` &rarr; `UnclosedComment`** (error)

- **Exact edge logic (the wrong rule):** Opens a comment with /\* and never closes it.
- **Twin logic (the right rule):** A /\* comment is the text between /\* and \*/, so the closing \*/ is required.
- **Role:** context

**6. `comment` &rarr; `comment@L0`** (has_level)

- **Exact edge logic:** comment -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (3 ways).
  - **[0] everyday\_reading** (rule type E, folk-meaning rule): Everyday reading: text written in a program is an instruction the computer reads and obeys. Java rule: comments (// to end of line, /\* ... \*/) are ignored by the compiler and have no effect on execution; they are for human readers.
  - **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `CommentIsExecuted`: wrong rule: A comment line is run like a statement. Right rule: The compiler ignores comments: everything from // to the end of the line and everything between /\* and \*/.
  - **[2] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `CommentIsExecuted`: Applies the skip rule unevenly: skips one comment while tracing but 'executes' another (e.g. a commented-out println), or forgets that // ends at the line break. (here mixing in: "A comment line is run like a statement")

**7. `comment` &rarr; `comment@L1`** (has_level)

- **Exact edge logic:** comment -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).
  - **[0] names\_the\_element** (rule type N, identity rule): A comment is explanatory text in the program that the compiler ignores.
  - **[1] states\_the\_rule** (rule type S, declarative rule): A comment is either text between /\* and \*/ or text from // to the end of the line; the compiler ignores it. A comment that starts with /\*\* is a documentation (Javadoc) comment, written before a class or method; tools turn it into API documentation.

**8. `comment` &rarr; `comment@L2`** (has_level)

- **Exact edge logic:** comment -&gt; L2 (Multistructural): the answer applies the rules of comment to every part of the code, in order (3 ways).
  - **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): Comments are removed when the source is read by the compiler, so they never take part in execution order; tracing skips them.
  - **[1] output\_prediction** (rule type OP, evaluation / result rule): A comment produces no value and no output.
  - **[2] one\_step\_execution** (rule type OS, state-transition rule): A comment changes no state; adding one and recompiling leaves the program's behaviour identical.

**9. `comment` &rarr; `comment@L3`** (has_level)

- **Exact edge logic:** comment -&gt; L3 (Relational): the answer relates the parts (2 ways).
  - **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Comments are part of the program text in Name.java but are dropped when it is compiled, so they cannot affect Name.class's behaviour.
  - **[1] purpose\_of\_the\_whole** (rule type P, plan / role rule): Purpose: explain what the code does and why, for other programmers and your future self; also used to disable code temporarily.

**10. `comment` &rarr; `comment@L4`** (has_level)

- **Exact edge logic:** comment -&gt; L4 (Extended abstract): the answer reasons beyond the given code (4 ways).
  - **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `CommentIsExecuted`: Adding, removing or editing a comment keeps behaviour unchanged, as long as the delimiters stay intact; deleting a closing \*/ or turning a statement into a comment changes the program.
  - **[1] diagnose\_an\_error** (rule type D, error rule): rule broken: A /\* comment needs its closing \*/. Kind: compile-time. Trigger class: a /\* with no matching \*/: the rest of the file becomes comment, so javac reports an unclosed comment or reached end of file
  - **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: /\* and \*/ are two-character tokens with no space inside. Kind: compile-time. Trigger class: writing / \* ... \* /: the slashes and stars are read as operators, producing syntax errors
  - **[3] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Use comments to document intent where the code alone is unclear; do not rely on them to change what the program does, and keep them in step with the code.

**11. `topic1.1.b` &rarr; `comment`** (contains)

- topic `topic1.1.b` contains `comment`

**12. `topic1.1.b` &rarr; `block`** (contains)

- topic `topic1.1.b` contains `block`

**13. `topic1.1.b` &rarr; `class_declaration`** (contains)

- topic `topic1.1.b` contains `class_declaration`

**14. `topic1.1.b` &rarr; `main_method`** (contains)

- topic `topic1.1.b` contains `main_method`

**15. `topic1.1.b` &rarr; `print`** (contains)

- topic `topic1.1.b` contains `print`

**16. `topic1.1.b` &rarr; `println`** (contains)

- topic `topic1.1.b` contains `println`

**17. `topic1.1.b` &rarr; `program_layout`** (contains)

- topic `topic1.1.b` contains `program_layout`

**18. `topic1.1.b` &rarr; `statement`** (contains)

- topic `topic1.1.b` contains `statement`

**19. `topic1.1.b` &rarr; `string_literal`** (contains)

- topic `topic1.1.b` contains `string_literal`
