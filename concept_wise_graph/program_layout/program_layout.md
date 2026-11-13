# program_layout (`program_layout`)

one statement per line and indentation that shows nesting

Section 1.1 Your First Program, topic 1.1.b Understanding a program (HelloWorld).

![The knowledge graph around program_layout](program_layout.png)

## At a glance

- **Needs first:** `block`
- **Leads to:** nothing
- **Learned alongside:** nothing
- **Misconceptions:** `InconsistentIndentation`, `WhitespaceIsSignificant`
- **Errors:** none
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 21 edges around this concept. The edge logic, the wrong and right rules and the exact rules of the ways are copied word for word from the graph.

## To work on (2)

- misconceptions with no L0 way linked to them: InconsistentIndentation
- no aliases: a student's words cannot name this concept

## What it needs first (1)

A prerequisite edge means the other concept has to be understood before `program_layout`.

### `block` comes before `program_layout`

*{ ... } grouping statements*

- **Edge:** `pre:block->program_layout`
- **Exact edge logic:** Indentation makes the nesting of blocks visible, so the reader can see which statements belong to which block.
- **Grounding:** book\_passage
- **Composition rule (R) of `program_layout` with `block`:** Indentation should show which statements belong to which block; braces, not indentation, decide it, so wrong indentation misleads.
- **Composition rule (R) of `block` with `program_layout`:** Indentation should show block nesting, but only braces define it; layout that disagrees with the braces misleads the reader, not the compiler.

## What it leads to (0)

These concepts need `program_layout` first.

No concept has this one as a prerequisite.

## Learned alongside (0)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

No parallel edge touches this concept.

## Misconceptions (2)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### InconsistentIndentation

- **Edge:** `program_layout` &rarr; `InconsistentIndentation` (misconception)
- **Exact edge logic (the wrong rule):** Indents nested blocks inconsistently, so the visual nesting differs from the real nesting.
- **Twin logic (the right rule):** Indent consistently, one level deeper for each nested block, so the layout shows the real nesting; the compiler ignores indentation.
- **Wrong belief (on the node):** Indents nested blocks inconsistently, so the visual nesting differs from the real nesting.
- **Correct rule (on the node):** Indent consistently, one level deeper for each nested block, so the layout shows the real nesting; the compiler ignores indentation.
- **Provenance:** rule\_dictionary
- **Role of this concept:** primary
- **L0 way linked to it:** no
- **Edge `block` &rarr; `InconsistentIndentation`, exact edge logic:** Indents nested blocks inconsistently, so the visual nesting differs from the real nesting. **Twin logic:** Indent consistently, one level deeper for each nested block, so the layout shows the real nesting; the compiler ignores indentation. (role: context)
- **Edge `nested_conditionals` &rarr; `InconsistentIndentation`, exact edge logic:** Indents nested blocks inconsistently, so the visual nesting differs from the real nesting. **Twin logic:** Indent consistently, one level deeper for each nested block, so the layout shows the real nesting; the compiler ignores indentation. (role: context)
- **Edge `nested_loops` &rarr; `InconsistentIndentation`, exact edge logic:** Indents nested blocks inconsistently, so the visual nesting differs from the real nesting. **Twin logic:** Indent consistently, one level deeper for each nested block, so the layout shows the real nesting; the compiler ignores indentation. (role: context)

### WhitespaceIsSignificant

- **Edge:** `program_layout` &rarr; `WhitespaceIsSignificant` (misconception)
- **Exact edge logic (the wrong rule):** Line breaks and indentation change what the program does, so each statement must be on its own line.
- **Twin logic (the right rule):** Java compilers consider all whitespace in program text (outside quotation marks) to be equivalent; layout is for human readers.
- **Wrong belief (on the node):** Line breaks and indentation change what the program does, so each statement must be on its own line.
- **Correct rule (on the node):** Java compilers consider all whitespace in program text (outside quotation marks) to be equivalent; layout is for human readers.
- **Provenance:** textbook
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [1] misconception, exact rule:** wrong rule: Line breaks and indentation change what the program does, so each statement must be on its own line. Right rule: Java compilers consider all whitespace in program text (outside quotation marks) to be equivalent; layout is for human readers.
- **L0 way [2] inconsistent\_trace, exact rule:** Applies the 'layout is ignored' rule unevenly: follows the braces on one trace but the indentation on another, e.g. treats a mis-indented line after a braceless if as part of the branch. (here mixing in: "Line breaks and indentation change what the program does, so each statement must be on its own line")
- **Edge `statement` &rarr; `WhitespaceIsSignificant`, exact edge logic:** Line breaks and indentation change what the program does, so each statement must be on its own line. **Twin logic:** Java compilers consider all whitespace in program text (outside quotation marks) to be equivalent; layout is for human readers. (role: context)

## Errors (0)

An error edge states the rule that gets broken in a program, and the right rule.

The graph has no error edge from this concept.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for program layout: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to program layout agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

- **Edge:** `program_layout` &rarr; `program_layout@L0` (has_level)
- **Exact edge logic:** program layout -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (3 ways).

Ways (3), each with its exact rule:

- **[0] everyday\_reading** (rule type E, folk-meaning rule): Everyday reading: as in poetry or Python, line breaks and indentation carry meaning. Java rule: the compiler treats all whitespace between tokens as equivalent; layout is for human readers only (some spaces separate words, e.g. public class).
- **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `WhitespaceIsSignificant`: wrong rule: Line breaks and indentation change what the program does, so each statement must be on its own line. Right rule: Java compilers consider all whitespace in program text (outside quotation marks) to be equivalent; layout is for human readers.
- **[2] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `WhitespaceIsSignificant`: Applies the 'layout is ignored' rule unevenly: follows the braces on one trace but the indentation on another, e.g. treats a mis-indented line after a braceless if as part of the branch. (here mixing in: "Line breaks and indentation change what the program does, so each statement must be on its own line")

### L1: Unistructural / atom x text surface

L1 for program layout: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

- **Edge:** `program_layout` &rarr; `program_layout@L1` (has_level)
- **Exact edge logic:** program layout -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

Ways (2), each with its exact rule:

- **[0] names\_the\_element** (rule type N, identity rule): Program layout is the use of whitespace (one statement per line, indentation one level per nested block) to make program structure visible; it is a style convention, not syntax.
- **[1] states\_the\_rule** (rule type S, declarative rule): Whitespace is needed only to separate adjacent words; otherwise all whitespace is equivalent, so the whole HelloWorld program can be written on one line; by convention, indent consistently to show nesting.

### L2: Multistructural / block x execution / preoperational

L2 for program layout: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

- **Edge:** `program_layout` &rarr; `program_layout@L2` (has_level)
- **Exact edge logic:** program layout -&gt; L2 (Multistructural): the answer applies the rules of program layout to every part of the code, in order (3 ways).

Ways (3), each with its exact rule:

- **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): Layout has no execution order of its own: execution follows statements and braces, regardless of lines and indentation.
- **[1] output\_prediction** (rule type OP, evaluation / result rule): Changing layout produces the same program output; only whitespace inside string literals appears in the output.
- **[2] one\_step\_execution** (rule type OS, state-transition rule): Re-formatting changes no state and no behaviour; it only changes how readable the text is.

### L3: Relational / relations x function (concrete operational begins)

L3 for program layout: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

- **Edge:** `program_layout` &rarr; `program_layout@L3` (has_level)
- **Exact edge logic:** program layout -&gt; L3 (Relational): the answer relates the parts (2 ways).

Ways (2), each with its exact rule:

- **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Indentation should show which statements belong to which block; braces, not indentation, decide it, so wrong indentation misleads.
- **[1] purpose\_of\_the\_whole** (rule type P, plan / role rule): Purpose: make the program's structure (or intended structure) apparent so it is easier to read and to find errors.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for program layout: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

- **Edge:** `program_layout` &rarr; `program_layout@L4` (has_level)
- **Exact edge logic:** program layout -&gt; L4 (Extended abstract): the answer reasons beyond the given code (4 ways).

Ways (4), each with its exact rule:

- **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `WhitespaceIsSignificant`: Re-indenting or re-wrapping lines (outside string literals) keeps behaviour; removing a needed space between words (publicclass) breaks compilation.
- **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Always use consistent indentation and one statement per line (an editor can auto-format); it matters most in nested code, and checking indentation helps spot syntax errors.
- **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: Indentation does not create a block. Kind: silent logic error. Trigger class: a second statement indented under a braceless if or while, expected to be conditional or repeated
- **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: Some spaces are required between words. Kind: compile-time. Trigger class: keywords run together, e.g. publicclassGoodbye

## Same topic

`program_layout` belongs to the topic **Understanding a program (HelloWorld)** (`topic1.1.b`). The topic also contains: `block`, `class_declaration`, `comment`, `main_method`, `print`, `println`, `statement`, `string_literal`.

## Rules of the concept (14)

- **Book** (TJ-2e, p. 8 (pdf 30)): "Many editors will automatically format source code with consistent indenting and line breaks."
- **Book** (TJ-2e, p. 75 (pdf 97)): "Good indentation is essential to make the structure (or intended structure) apparent to the reader."
- **Book** (RS, ): "Put no more than one statement on each line. Indent your program properly. When a { brace appears, increase the indentation of following lines."
- **E** (folk-meaning rule): Everyday reading: as in poetry or Python, line breaks and indentation carry meaning. Java rule: the compiler treats all whitespace between tokens as equivalent; layout is for human readers only (some spaces separate words, e.g. public class).
- **M** (wrong rule / right rule): WhitespaceIsSignificant: wrong: Line breaks and indentation change what the program does, so each statement must be on its own line. \| right: Java compilers consider all whitespace in program text (outside quotation marks) to be equivalent; layout is for human readers.
- **T** (uneven-application rule): Applies the 'layout is ignored' rule unevenly: follows the braces on one trace but the indentation on another, e.g. treats a mis-indented line after a braceless if as part of the branch.
- **N** (identity rule): Program layout is the use of whitespace (one statement per line, indentation one level per nested block) to make program structure visible; it is a style convention, not syntax.
- **S** (declarative rule): Whitespace is needed only to separate adjacent words; otherwise all whitespace is equivalent, so the whole HelloWorld program can be written on one line; by convention, indent consistently to show nesting.
- **LT** (operational sequencing rule): Layout has no execution order of its own: execution follows statements and braces, regardless of lines and indentation.
- **OP** (evaluation / result rule): Changing layout produces the same program output; only whitespace inside string literals appears in the output.
- **OS** (state-transition rule): Re-formatting changes no state and no behaviour; it only changes how readable the text is.
- **R** (composition rule (with a neighbour)): with block: Indentation should show which statements belong to which block; braces, not indentation, decide it, so wrong indentation misleads.
- **P** (plan / role rule): Purpose: make the program's structure (or intended structure) apparent so it is easier to read and to find errors.
- **C** (conservation rule): Re-indenting or re-wrapping lines (outside string literals) keeps behaviour; removing a needed space between words (publicclass) breaks compilation.
- **D** (error rule): rule broken: Indentation does not create a block (silent logic error)
- **D** (error rule): rule broken: Some spaces are required between words (compile-time)
- **X** (applicability rule): Always use consistent indentation and one statement per line (an editor can auto-format); it matters most in nested code, and checking indentation helps spot syntax errors.

## How it is found in code and answers (reader block)

- **Aliases:** none
- **Code patterns:** none
- **Operator symbols:** none
- **Java types:** none
- **Signal two\_statements\_one\_line** (scope program): `^(?![^\n]*\b(?:for\s*\(|case\b|default\s*:))[^\n]*;[ \t]*(?!//|else\b)[A-Za-z_][^\n;]*;`

## The whole prerequisite chain

- **Everything it builds on (5):** `block`, `class_declaration`, `main_method`, `program_text`, `statement`
- **Everything that builds on it (0):** nothing

## Every edge in this view and its exact edge logic (21)

All the edges drawn in the picture, in the order: prerequisite, parallel, misconception, error, has_level, contains.

**1. `block` &rarr; `program_layout`** (prerequisite)

- **Exact edge logic:** Indentation makes the nesting of blocks visible, so the reader can see which statements belong to which block.
- **Grounding:** book\_passage
- **Composition rule (R) of `block` with `program_layout`:** Indentation should show block nesting, but only braces define it; layout that disagrees with the braces misleads the reader, not the compiler.
- **Composition rule (R) of `program_layout` with `block`:** Indentation should show which statements belong to which block; braces, not indentation, decide it, so wrong indentation misleads.

**2. `program_layout` &rarr; `InconsistentIndentation`** (misconception)

- **Exact edge logic (the wrong rule):** Indents nested blocks inconsistently, so the visual nesting differs from the real nesting.
- **Twin logic (the right rule):** Indent consistently, one level deeper for each nested block, so the layout shows the real nesting; the compiler ignores indentation.
- **Role:** primary

**3. `program_layout` &rarr; `WhitespaceIsSignificant`** (misconception)

- **Exact edge logic (the wrong rule):** Line breaks and indentation change what the program does, so each statement must be on its own line.
- **Twin logic (the right rule):** Java compilers consider all whitespace in program text (outside quotation marks) to be equivalent; layout is for human readers.
- **Role:** primary

**4. `block` &rarr; `InconsistentIndentation`** (misconception)

- **Exact edge logic (the wrong rule):** Indents nested blocks inconsistently, so the visual nesting differs from the real nesting.
- **Twin logic (the right rule):** Indent consistently, one level deeper for each nested block, so the layout shows the real nesting; the compiler ignores indentation.
- **Role:** context

**5. `nested_conditionals` &rarr; `InconsistentIndentation`** (misconception)

- **Exact edge logic (the wrong rule):** Indents nested blocks inconsistently, so the visual nesting differs from the real nesting.
- **Twin logic (the right rule):** Indent consistently, one level deeper for each nested block, so the layout shows the real nesting; the compiler ignores indentation.
- **Role:** context

**6. `nested_loops` &rarr; `InconsistentIndentation`** (misconception)

- **Exact edge logic (the wrong rule):** Indents nested blocks inconsistently, so the visual nesting differs from the real nesting.
- **Twin logic (the right rule):** Indent consistently, one level deeper for each nested block, so the layout shows the real nesting; the compiler ignores indentation.
- **Role:** context

**7. `statement` &rarr; `WhitespaceIsSignificant`** (misconception)

- **Exact edge logic (the wrong rule):** Line breaks and indentation change what the program does, so each statement must be on its own line.
- **Twin logic (the right rule):** Java compilers consider all whitespace in program text (outside quotation marks) to be equivalent; layout is for human readers.
- **Role:** context

**8. `program_layout` &rarr; `program_layout@L0`** (has_level)

- **Exact edge logic:** program layout -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (3 ways).
  - **[0] everyday\_reading** (rule type E, folk-meaning rule): Everyday reading: as in poetry or Python, line breaks and indentation carry meaning. Java rule: the compiler treats all whitespace between tokens as equivalent; layout is for human readers only (some spaces separate words, e.g. public class).
  - **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `WhitespaceIsSignificant`: wrong rule: Line breaks and indentation change what the program does, so each statement must be on its own line. Right rule: Java compilers consider all whitespace in program text (outside quotation marks) to be equivalent; layout is for human readers.
  - **[2] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `WhitespaceIsSignificant`: Applies the 'layout is ignored' rule unevenly: follows the braces on one trace but the indentation on another, e.g. treats a mis-indented line after a braceless if as part of the branch. (here mixing in: "Line breaks and indentation change what the program does, so each statement must be on its own line")

**9. `program_layout` &rarr; `program_layout@L1`** (has_level)

- **Exact edge logic:** program layout -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).
  - **[0] names\_the\_element** (rule type N, identity rule): Program layout is the use of whitespace (one statement per line, indentation one level per nested block) to make program structure visible; it is a style convention, not syntax.
  - **[1] states\_the\_rule** (rule type S, declarative rule): Whitespace is needed only to separate adjacent words; otherwise all whitespace is equivalent, so the whole HelloWorld program can be written on one line; by convention, indent consistently to show nesting.

**10. `program_layout` &rarr; `program_layout@L2`** (has_level)

- **Exact edge logic:** program layout -&gt; L2 (Multistructural): the answer applies the rules of program layout to every part of the code, in order (3 ways).
  - **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): Layout has no execution order of its own: execution follows statements and braces, regardless of lines and indentation.
  - **[1] output\_prediction** (rule type OP, evaluation / result rule): Changing layout produces the same program output; only whitespace inside string literals appears in the output.
  - **[2] one\_step\_execution** (rule type OS, state-transition rule): Re-formatting changes no state and no behaviour; it only changes how readable the text is.

**11. `program_layout` &rarr; `program_layout@L3`** (has_level)

- **Exact edge logic:** program layout -&gt; L3 (Relational): the answer relates the parts (2 ways).
  - **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Indentation should show which statements belong to which block; braces, not indentation, decide it, so wrong indentation misleads.
  - **[1] purpose\_of\_the\_whole** (rule type P, plan / role rule): Purpose: make the program's structure (or intended structure) apparent so it is easier to read and to find errors.

**12. `program_layout` &rarr; `program_layout@L4`** (has_level)

- **Exact edge logic:** program layout -&gt; L4 (Extended abstract): the answer reasons beyond the given code (4 ways).
  - **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `WhitespaceIsSignificant`: Re-indenting or re-wrapping lines (outside string literals) keeps behaviour; removing a needed space between words (publicclass) breaks compilation.
  - **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Always use consistent indentation and one statement per line (an editor can auto-format); it matters most in nested code, and checking indentation helps spot syntax errors.
  - **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: Indentation does not create a block. Kind: silent logic error. Trigger class: a second statement indented under a braceless if or while, expected to be conditional or repeated
  - **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: Some spaces are required between words. Kind: compile-time. Trigger class: keywords run together, e.g. publicclassGoodbye

**13. `topic1.1.b` &rarr; `program_layout`** (contains)

- topic `topic1.1.b` contains `program_layout`

**14. `topic1.1.b` &rarr; `block`** (contains)

- topic `topic1.1.b` contains `block`

**15. `topic1.1.b` &rarr; `class_declaration`** (contains)

- topic `topic1.1.b` contains `class_declaration`

**16. `topic1.1.b` &rarr; `comment`** (contains)

- topic `topic1.1.b` contains `comment`

**17. `topic1.1.b` &rarr; `main_method`** (contains)

- topic `topic1.1.b` contains `main_method`

**18. `topic1.1.b` &rarr; `print`** (contains)

- topic `topic1.1.b` contains `print`

**19. `topic1.1.b` &rarr; `println`** (contains)

- topic `topic1.1.b` contains `println`

**20. `topic1.1.b` &rarr; `statement`** (contains)

- topic `topic1.1.b` contains `statement`

**21. `topic1.1.b` &rarr; `string_literal`** (contains)

- topic `topic1.1.b` contains `string_literal`
