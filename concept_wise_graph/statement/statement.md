# statement (`statement`)

one step, terminated by ;, executed in sequence

Section 1.1 Your First Program, topic 1.1.b Understanding a program (HelloWorld).

![The knowledge graph around statement](statement.png)

## At a glance

- **Needs first:** `main_method`
- **Leads to:** `algorithm_pseudocode`, `block`, `control_flow`, `empty_statement`, `print`, `println`
- **Learned alongside:** nothing
- **Misconceptions:** `ComputerFillsInIntent`, `ProgramLooksAhead`, `StatementsRunInAnyOrder`, `WhitespaceIsSignificant`
- **Errors:** `StatementNeedsNoTerminator`
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 34 edges around this concept. The edge logic, the wrong and right rules and the exact rules of the ways are copied word for word from the graph.

## To work on (0)

Nothing is missing for this concept.

## What it needs first (1)

A prerequisite edge means the other concept has to be understood before `statement`.

### `main_method` comes before `statement`

*public static void main(String[] args) -- entry point*

- **Edge:** `pre:main_method->statement`
- **Exact edge logic:** Statements are written in main's body, and running the program executes main's statements in order, one by one.
- **Grounding:** book\_passage
- **Composition rule (R) of `statement` with `main_method`:** Statements live in main's body; running the program executes main's statements in order.
- **Composition rule (R) of `main_method` with `statement`:** main's body holds the statements; running the program executes them in order, one by one.

## What it leads to (6)

These concepts need `statement` first.

### `statement` comes before `algorithm_pseudocode`

*an algorithm is a sequence of steps that solves a problem; pseudocode outlines it in English and Java before it is coded*

- **Edge:** `pre:statement->algorithm_pseudocode`
- **Exact edge logic:** An algorithm becomes a program as a sequence of statements, executed once each in the order given.
- **Grounding:** book\_passage
- **Composition rule (R) of `algorithm_pseudocode` with `statement`:** Each step of the algorithm becomes one or more statements, executed in the same order.

### `statement` comes before `block`

*{ ... } grouping statements*

- **Edge:** `pre:statement->block`
- **Exact edge logic:** A statement block is a sequence of statements, each terminated by a semicolon, enclosed in braces; the body of main() is such a sequence.
- **Grounding:** book\_passage
- **Composition rule (R) of `statement` with `block`:** A block groups a sequence of statements in braces; the body of main() is such a block.
- **Composition rule (R) of `block` with `statement`:** A block is built from statements, each ended by ;, and is itself usable as a single statement (e.g. a loop body).

### `statement` comes before `control_flow`

*the order in which statements are executed*

- **Edge:** `pre:statement->control_flow`
- **Exact edge logic:** Control flow is the order in which statements run.
- **Grounding:** book\_passage
- **Composition rule (R) of `statement` with `control_flow`:** Control flow is the order in which statements run; without control statements it is straight-line, each once in order.
- **Composition rule (R) of `control_flow` with `statement`:** Control flow is defined over statements: statements are executed for their effect, and if/while/for are themselves statements that may be used wherever a statement is allowed, so they can nest.

### `statement` comes before `empty_statement`

*a lone ; is an empty statement; a block can stand alone*

- **Edge:** `pre:statement->empty_statement`
- **Exact edge logic:** Any part of a for loop, including its body, can be left empty (a null statement, a lone ;); the book prefers a while loop to null statements.
- **Grounding:** book\_passage
- **Composition rule (R) of `statement` with `empty_statement`:** A lone ; is the empty statement, which does nothing; it can fill a for-loop part or, by accident, end an if or loop header.
- **Composition rule (R) of `empty_statement` with `statement`:** The empty statement can stand wherever a statement is required (if body, loop body, for slots), and a block { } can stand alone; a ; after a header therefore silently becomes the body.

### `statement` comes before `print`

*System.out.print -- output with no newline*

- **Edge:** `pre:statement->print`
- **Exact edge logic:** System.out.print(s); is itself a statement, so it runs at its own place in the sequence of statements.
- **Grounding:** book\_passage
- **Composition rule (R) of `statement` with `print`:** System.out.print(s); is a statement, so its output appears exactly at its place in the sequence, with no newline.
- **Composition rule (R) of `print` with `statement`:** System.out.print(s); is a statement, so its output appears at its place in the statement sequence.

### `statement` comes before `println`

*System.out.println -- output with a trailing newline*

- **Edge:** `pre:statement->println`
- **Exact edge logic:** System.out.println(s); is itself a statement, so its line of output appears at its own place in the sequence.
- **Grounding:** book\_passage
- **Composition rule (R) of `statement` with `println`:** System.out.println(s); is a statement, so its line of output appears at its place in the sequence; swapping two println statements swaps the output lines.
- **Composition rule (R) of `println` with `statement`:** System.out.println(s); is a statement, so its line of output appears at its own place in the sequence.

## Learned alongside (0)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

No parallel edge touches this concept.

## Misconceptions (4)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### ComputerFillsInIntent

- **Edge:** `statement` &rarr; `ComputerFillsInIntent` (misconception)
- **Exact edge logic (the wrong rule):** The computer fills in omitted steps or values that the programmer meant, e.g. REPEAT 4 [FORWARD 30] draws a square without a turn command.
- **Twin logic (the right rule):** The computer executes only what the code states; every needed step and value must be written.
- **Wrong belief (on the node):** The computer fills in omitted steps or values that the programmer meant, e.g. REPEAT 4 [FORWARD 30] draws a square without a turn command.
- **Correct rule (on the node):** The computer executes only what the code states; every needed step and value must be written.
- **Provenance:** published
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [1] misconception, exact rule:** wrong rule: The computer fills in omitted steps or values the programmer meant. Right rule: The computer executes only the statements written; every needed step and value must be written.
- **L0 way [2] inconsistent\_trace, exact rule:** Applies the sequencing rule (LT) unevenly: executes the statements in order on some lines but lets a later statement's effect leak into an earlier one, or skips or repeats a statement on one pass. (here mixing in: "The computer fills in omitted steps or values that the programmer meant, e.g. REPEAT 4 [FORWARD 30] draws a square without a turn command")
- **Edge `algorithm_pseudocode` &rarr; `ComputerFillsInIntent`, exact edge logic:** The computer fills in omitted steps or values that the programmer meant, e.g. REPEAT 4 [FORWARD 30] draws a square without a turn command. **Twin logic:** The computer executes only what the code states; every needed step and value must be written. (role: context)
- **Edge `loop_body` &rarr; `ComputerFillsInIntent`, exact edge logic:** The computer fills in omitted steps or values that the programmer meant, e.g. REPEAT 4 [FORWARD 30] draws a square without a turn command. **Twin logic:** The computer executes only what the code states; every needed step and value must be written. (role: context)
- **Edge `program_text` &rarr; `ComputerFillsInIntent`, exact edge logic:** The computer fills in omitted steps or values that the programmer meant, e.g. REPEAT 4 [FORWARD 30] draws a square without a turn command. **Twin logic:** The computer executes only what the code states; every needed step and value must be written. (role: context)

### ProgramLooksAhead

- **Edge:** `statement` &rarr; `ProgramLooksAhead` (misconception)
- **Exact edge logic (the wrong rule):** The program knows or sees what later lines will do and acts on those goals at the current line, e.g. it stops 'at ten' because it wants to draw a box.
- **Twin logic (the right rule):** Each statement executes using only the current state; later lines have no effect until control reaches them.
- **Wrong belief (on the node):** The program knows or sees what later lines will do and acts on those goals at the current line, e.g. it stops 'at ten' because it wants to draw a box.
- **Correct rule (on the node):** Each statement executes using only the current state; later lines have no effect until control reaches them.
- **Provenance:** published
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [5] misconception, exact rule:** wrong rule: The program knows what later lines will do and acts on that goal at the current line. Right rule: Each statement executes using only the current state; later lines have no effect until control reaches them.
- **Edge `control_flow` &rarr; `ProgramLooksAhead`, exact edge logic:** The program knows or sees what later lines will do and acts on those goals at the current line, e.g. it stops 'at ten' because it wants to draw a box. **Twin logic:** Each statement executes using only the current state; later lines have no effect until control reaches them. (role: primary)
- **Edge `if_statement` &rarr; `ProgramLooksAhead`, exact edge logic:** The program knows or sees what later lines will do and acts on those goals at the current line, e.g. it stops 'at ten' because it wants to draw a box. **Twin logic:** Each statement executes using only the current state; later lines have no effect until control reaches them. (role: context)

### StatementsRunInAnyOrder

- **Edge:** `statement` &rarr; `StatementsRunInAnyOrder` (misconception)
- **Exact edge logic (the wrong rule):** Statements in a program can run in any order.
- **Twin logic (the right rule):** Without control statements, statements run once each, top to bottom.
- **Wrong belief (on the node):** Statements in a program can run in any order.
- **Correct rule (on the node):** Without control statements, statements run once each, top to bottom.
- **Provenance:** published
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [3] misconception, exact rule:** wrong rule: Statements in a program can run in any order, so their order makes no difference. Right rule: Without control statements, statements run once each, top to bottom, in the order written.
- **Edge `control_flow` &rarr; `StatementsRunInAnyOrder`, exact edge logic:** Statements in a program can run in any order. **Twin logic:** Without control statements, statements run once each, top to bottom. (role: primary)

### WhitespaceIsSignificant

- **Edge:** `statement` &rarr; `WhitespaceIsSignificant` (misconception)
- **Exact edge logic (the wrong rule):** Line breaks and indentation change what the program does, so each statement must be on its own line.
- **Twin logic (the right rule):** Java compilers consider all whitespace in program text (outside quotation marks) to be equivalent; layout is for human readers.
- **Wrong belief (on the node):** Line breaks and indentation change what the program does, so each statement must be on its own line.
- **Correct rule (on the node):** Java compilers consider all whitespace in program text (outside quotation marks) to be equivalent; layout is for human readers.
- **Provenance:** textbook
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [4] misconception, exact rule:** wrong rule: Line breaks and indentation change what the program does, so each statement must be on its own line. Right rule: Java compilers treat all whitespace outside quotes as equivalent; statements are separated by ;, not by line breaks.
- **Edge `program_layout` &rarr; `WhitespaceIsSignificant`, exact edge logic:** Line breaks and indentation change what the program does, so each statement must be on its own line. **Twin logic:** Java compilers consider all whitespace in program text (outside quotation marks) to be equivalent; layout is for human readers. (role: primary)

## Errors (1)

An error edge states the rule that gets broken in a program, and the right rule.

### StatementNeedsNoTerminator

- **Edge:** `statement` &rarr; `StatementNeedsNoTerminator` (error)
- **Exact edge logic (the wrong rule):** A statement still compiles and runs if the semicolon at its end is left out, or if a stray ; is put right after if (c) or for (...).
- **Twin logic (the right rule):** Each statement must end with ;, otherwise javac reports ';' expected.
- **Wrong belief (on the node):** a statement runs without the ;
- **Correct rule (on the node):** Each statement must end with ;, otherwise javac reports ';' expected.
- **Provenance:** textbook
- **Role of this concept:** primary
- **Edge `compile_time_error` &rarr; `StatementNeedsNoTerminator`, exact edge logic:** a statement runs without the ; **Twin logic:** Each statement must end with ;, otherwise javac reports ';' expected. (role: context)

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for statement: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to statement agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

- **Edge:** `statement` &rarr; `statement@L0` (has_level)
- **Exact edge logic:** statement -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (6 ways).

Ways (6), each with its exact rule:

- **[0] everyday\_reading** (rule type E, folk-meaning rule): Everyday reading: a program is read like a text or a list of wishes that the computer takes in all at once, so line order, goals of later lines or what the writer meant can matter. Java rule: each statement is one step, ended by ;, executed once, in written order, using only the current state.
- **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `ComputerFillsInIntent`: wrong rule: The computer fills in omitted steps or values the programmer meant. Right rule: The computer executes only the statements written; every needed step and value must be written.
- **[2] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `ComputerFillsInIntent`: Applies the sequencing rule (LT) unevenly: executes the statements in order on some lines but lets a later statement's effect leak into an earlier one, or skips or repeats a statement on one pass. (here mixing in: "The computer fills in omitted steps or values that the programmer meant, e.g. REPEAT 4 [FORWARD 30] draws a square without a turn command")
- **[3] misconception** (rule type M, wrong rule / right rule) &rarr; `StatementsRunInAnyOrder`: wrong rule: Statements in a program can run in any order, so their order makes no difference. Right rule: Without control statements, statements run once each, top to bottom, in the order written.
- **[4] misconception** (rule type M, wrong rule / right rule) &rarr; `WhitespaceIsSignificant`: wrong rule: Line breaks and indentation change what the program does, so each statement must be on its own line. Right rule: Java compilers treat all whitespace outside quotes as equivalent; statements are separated by ;, not by line breaks.
- **[5] misconception** (rule type M, wrong rule / right rule) &rarr; `ProgramLooksAhead`: wrong rule: The program knows what later lines will do and acts on that goal at the current line. Right rule: Each statement executes using only the current state; later lines have no effect until control reaches them.

### L1: Unistructural / atom x text surface

L1 for statement: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

- **Edge:** `statement` &rarr; `statement@L1` (has_level)
- **Exact edge logic:** statement -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

Ways (2), each with its exact rule:

- **[0] names\_the\_element** (rule type N, identity rule): A statement is one step of a program (a declaration, assignment, method call such as System.out.println(...), or control statement), ended by a semicolon when it is a simple statement.
- **[1] states\_the\_rule** (rule type S, declarative rule): A method body is a sequence of statements enclosed in braces and each followed by a semicolon; statements are executed for their effect and have no value; an expression statement evaluates its expression and discards any value.

### L2: Multistructural / block x execution / preoperational

L2 for statement: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

- **Edge:** `statement` &rarr; `statement@L2` (has_level)
- **Exact edge logic:** statement -&gt; L2 (Multistructural): the answer applies the rules of statement to every part of the code, in order (3 ways).

Ways (3), each with its exact rule:

- **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): Statements run one at a time, from first to last; each completes (normally or abruptly) before the next starts.
- **[1] output\_prediction** (rule type OP, evaluation / result rule): A statement has no value; its result is its effect: a changed variable, printed output, or a change of control flow.
- **[2] one\_step\_execution** (rule type OS, state-transition rule): Executing one statement applies its single effect to the current state (e.g. prints one string, or stores one value) and then control moves to the next statement.

### L3: Relational / relations x function (concrete operational begins)

L3 for statement: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

- **Edge:** `statement` &rarr; `statement@L3` (has_level)
- **Exact edge logic:** statement -&gt; L3 (Relational): the answer relates the parts (8 ways).

Ways (8), each with its exact rule:

- **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Statements live in main's body; running the program executes main's statements in order.
- **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): A block groups a sequence of statements in braces; the body of main() is such a block.
- **[2] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): System.out.print(s); is a statement, so its output appears exactly at its place in the sequence, with no newline.
- **[3] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): System.out.println(s); is a statement, so its line of output appears at its place in the sequence; swapping two println statements swaps the output lines.
- **[4] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Control flow is the order in which statements run; without control statements it is straight-line, each once in order.
- **[5] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): A lone ; is the empty statement, which does nothing; it can fill a for-loop part or, by accident, end an if or loop header.
- **[6] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): An algorithm becomes a program as a sequence of statements, executed once each in the order given.
- **[7] purpose\_of\_the\_whole** (rule type P, plan / role rule): Purpose: a statement is the unit of action; a program is characterized by its sequence of statements, each doing one step of the algorithm.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for statement: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

- **Edge:** `statement` &rarr; `statement@L4` (has_level)
- **Exact edge logic:** statement -&gt; L4 (Extended abstract): the answer reasons beyond the given code (4 ways).

Ways (4), each with its exact rule:

- **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `ComputerFillsInIntent`: Swapping two statements that touch the same variable or the output generally changes the result; swapping independent statements, or changing only whitespace between them, keeps it.
- **[1] diagnose\_an\_error** (rule type D, error rule): rule broken: Each simple statement must end with ;. Kind: compile-time. Trigger class: omitting the ; at the end of a statement: javac reports ';' expected (often at the end of that line or the next)
- **[2] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Write one statement per step and order them as the algorithm requires; straight-line sequence suffices when every step runs once, otherwise use conditionals or loops.
- **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: A ; directly after an if/while/for header is an empty statement. Kind: silent logic error. Trigger class: if (x &gt; 0); or while (cond); followed by the intended body

## Same topic

`statement` belongs to the topic **Understanding a program (HelloWorld)** (`topic1.1.b`). The topic also contains: `block`, `class_declaration`, `comment`, `main_method`, `print`, `println`, `program_layout`, `string_literal`.

## Rules of the concept (22)

- **Book** (SW-1e, p. 6 (pdf 16)): "The first line of a method specifies its name and other information; the rest is a sequence of statements enclosed in braces and each followed by a semicolon."
- **Book** (OT-Expressions, ): "A statement forms a complete unit of execution. The following types of expressions can be made into a statement by terminating the expression with a semicolon (;)."
- **Book** (JLS-14, ): "Certain kinds of expressions may be used as statements by following them with semicolons."
- **E** (folk-meaning rule): Everyday reading: a program is read like a text or a list of wishes that the computer takes in all at once, so line order, goals of later lines or what the writer meant can matter. Java rule: each statement is one step, ended by ;, executed once, in written order, using only the current state.
- **M** (wrong rule / right rule): StatementsRunInAnyOrder: wrong: Statements in a program can run in any order, so their order makes no difference. \| right: Without control statements, statements run once each, top to bottom, in the order written.
- **M** (wrong rule / right rule): WhitespaceIsSignificant: wrong: Line breaks and indentation change what the program does, so each statement must be on its own line. \| right: Java compilers treat all whitespace outside quotes as equivalent; statements are separated by ;, not by line breaks.
- **M** (wrong rule / right rule): ProgramLooksAhead: wrong: The program knows what later lines will do and acts on that goal at the current line. \| right: Each statement executes using only the current state; later lines have no effect until control reaches them.
- **M** (wrong rule / right rule): ComputerFillsInIntent: wrong: The computer fills in omitted steps or values the programmer meant. \| right: The computer executes only the statements written; every needed step and value must be written.
- **T** (uneven-application rule): Applies the sequencing rule (LT) unevenly: executes the statements in order on some lines but lets a later statement's effect leak into an earlier one, or skips or repeats a statement on one pass.
- **N** (identity rule): A statement is one step of a program (a declaration, assignment, method call such as System.out.println(...), or control statement), ended by a semicolon when it is a simple statement.
- **S** (declarative rule): A method body is a sequence of statements enclosed in braces and each followed by a semicolon; statements are executed for their effect and have no value; an expression statement evaluates its expression and discards any value.
- **LT** (operational sequencing rule): Statements run one at a time, from first to last; each completes (normally or abruptly) before the next starts.
- **OP** (evaluation / result rule): A statement has no value; its result is its effect: a changed variable, printed output, or a change of control flow.
- **OS** (state-transition rule): Executing one statement applies its single effect to the current state (e.g. prints one string, or stores one value) and then control moves to the next statement.
- **R** (composition rule (with a neighbour)): with main\_method: Statements live in main's body; running the program executes main's statements in order.
- **R** (composition rule (with a neighbour)): with block: A block groups a sequence of statements in braces; the body of main() is such a block.
- **R** (composition rule (with a neighbour)): with print: System.out.print(s); is a statement, so its output appears exactly at its place in the sequence, with no newline.
- **R** (composition rule (with a neighbour)): with println: System.out.println(s); is a statement, so its line of output appears at its place in the sequence; swapping two println statements swaps the output lines.
- **R** (composition rule (with a neighbour)): with control\_flow: Control flow is the order in which statements run; without control statements it is straight-line, each once in order.
- **R** (composition rule (with a neighbour)): with empty\_statement: A lone ; is the empty statement, which does nothing; it can fill a for-loop part or, by accident, end an if or loop header.
- **P** (plan / role rule): Purpose: a statement is the unit of action; a program is characterized by its sequence of statements, each doing one step of the algorithm.
- **C** (conservation rule): Swapping two statements that touch the same variable or the output generally changes the result; swapping independent statements, or changing only whitespace between them, keeps it.
- **D** (error rule): rule broken: Each simple statement must end with ; (compile-time)
- **D** (error rule): rule broken: A ; directly after an if/while/for header is an empty statement (silent logic error)
- **X** (applicability rule): Write one statement per step and order them as the algorithm requires; straight-line sequence suffices when every step runs once, otherwise use conditionals or loops.

## How it is found in code and answers (reader block)

- **Aliases:** statement, statements, semicolon
- **Code patterns:** `;`
- **Operator symbols:** none
- **Java types:** none

## The whole prerequisite chain

- **Everything it builds on (3):** `class_declaration`, `main_method`, `program_text`
- **Everything that builds on it (18):** `algorithm_pseudocode`, `block`, `conditional_operator`, `control_flow`, `dangling_else`, `debugging`, `else_if_chain`, `empty_statement`, `flowchart`, `if_else_statement`, `if_statement`, `logical_error`, `nested_conditionals`, `print`, `printing_array_reference`, `println`, `program_layout`, `switch_statement`

## Every edge in this view and its exact edge logic (34)

All the edges drawn in the picture, in the order: prerequisite, parallel, misconception, error, has_level, contains.

**1. `main_method` &rarr; `statement`** (prerequisite)

- **Exact edge logic:** Statements are written in main's body, and running the program executes main's statements in order, one by one.
- **Grounding:** book\_passage
- **Composition rule (R) of `main_method` with `statement`:** main's body holds the statements; running the program executes them in order, one by one.
- **Composition rule (R) of `statement` with `main_method`:** Statements live in main's body; running the program executes main's statements in order.

**2. `statement` &rarr; `algorithm_pseudocode`** (prerequisite)

- **Exact edge logic:** An algorithm becomes a program as a sequence of statements, executed once each in the order given.
- **Grounding:** book\_passage
- **Composition rule (R) of `algorithm_pseudocode` with `statement`:** Each step of the algorithm becomes one or more statements, executed in the same order.

**3. `statement` &rarr; `block`** (prerequisite)

- **Exact edge logic:** A statement block is a sequence of statements, each terminated by a semicolon, enclosed in braces; the body of main() is such a sequence.
- **Grounding:** book\_passage
- **Composition rule (R) of `statement` with `block`:** A block groups a sequence of statements in braces; the body of main() is such a block.
- **Composition rule (R) of `block` with `statement`:** A block is built from statements, each ended by ;, and is itself usable as a single statement (e.g. a loop body).

**4. `statement` &rarr; `control_flow`** (prerequisite)

- **Exact edge logic:** Control flow is the order in which statements run.
- **Grounding:** book\_passage
- **Composition rule (R) of `statement` with `control_flow`:** Control flow is the order in which statements run; without control statements it is straight-line, each once in order.
- **Composition rule (R) of `control_flow` with `statement`:** Control flow is defined over statements: statements are executed for their effect, and if/while/for are themselves statements that may be used wherever a statement is allowed, so they can nest.

**5. `statement` &rarr; `empty_statement`** (prerequisite)

- **Exact edge logic:** Any part of a for loop, including its body, can be left empty (a null statement, a lone ;); the book prefers a while loop to null statements.
- **Grounding:** book\_passage
- **Composition rule (R) of `statement` with `empty_statement`:** A lone ; is the empty statement, which does nothing; it can fill a for-loop part or, by accident, end an if or loop header.
- **Composition rule (R) of `empty_statement` with `statement`:** The empty statement can stand wherever a statement is required (if body, loop body, for slots), and a block { } can stand alone; a ; after a header therefore silently becomes the body.

**6. `statement` &rarr; `print`** (prerequisite)

- **Exact edge logic:** System.out.print(s); is itself a statement, so it runs at its own place in the sequence of statements.
- **Grounding:** book\_passage
- **Composition rule (R) of `statement` with `print`:** System.out.print(s); is a statement, so its output appears exactly at its place in the sequence, with no newline.
- **Composition rule (R) of `print` with `statement`:** System.out.print(s); is a statement, so its output appears at its place in the statement sequence.

**7. `statement` &rarr; `println`** (prerequisite)

- **Exact edge logic:** System.out.println(s); is itself a statement, so its line of output appears at its own place in the sequence.
- **Grounding:** book\_passage
- **Composition rule (R) of `statement` with `println`:** System.out.println(s); is a statement, so its line of output appears at its place in the sequence; swapping two println statements swaps the output lines.
- **Composition rule (R) of `println` with `statement`:** System.out.println(s); is a statement, so its line of output appears at its own place in the sequence.

**8. `statement` &rarr; `ComputerFillsInIntent`** (misconception)

- **Exact edge logic (the wrong rule):** The computer fills in omitted steps or values that the programmer meant, e.g. REPEAT 4 [FORWARD 30] draws a square without a turn command.
- **Twin logic (the right rule):** The computer executes only what the code states; every needed step and value must be written.
- **Role:** primary

**9. `statement` &rarr; `ProgramLooksAhead`** (misconception)

- **Exact edge logic (the wrong rule):** The program knows or sees what later lines will do and acts on those goals at the current line, e.g. it stops 'at ten' because it wants to draw a box.
- **Twin logic (the right rule):** Each statement executes using only the current state; later lines have no effect until control reaches them.
- **Role:** context

**10. `statement` &rarr; `StatementsRunInAnyOrder`** (misconception)

- **Exact edge logic (the wrong rule):** Statements in a program can run in any order.
- **Twin logic (the right rule):** Without control statements, statements run once each, top to bottom.
- **Role:** context

**11. `statement` &rarr; `WhitespaceIsSignificant`** (misconception)

- **Exact edge logic (the wrong rule):** Line breaks and indentation change what the program does, so each statement must be on its own line.
- **Twin logic (the right rule):** Java compilers consider all whitespace in program text (outside quotation marks) to be equivalent; layout is for human readers.
- **Role:** context

**12. `algorithm_pseudocode` &rarr; `ComputerFillsInIntent`** (misconception)

- **Exact edge logic (the wrong rule):** The computer fills in omitted steps or values that the programmer meant, e.g. REPEAT 4 [FORWARD 30] draws a square without a turn command.
- **Twin logic (the right rule):** The computer executes only what the code states; every needed step and value must be written.
- **Role:** context

**13. `control_flow` &rarr; `ProgramLooksAhead`** (misconception)

- **Exact edge logic (the wrong rule):** The program knows or sees what later lines will do and acts on those goals at the current line, e.g. it stops 'at ten' because it wants to draw a box.
- **Twin logic (the right rule):** Each statement executes using only the current state; later lines have no effect until control reaches them.
- **Role:** primary

**14. `control_flow` &rarr; `StatementsRunInAnyOrder`** (misconception)

- **Exact edge logic (the wrong rule):** Statements in a program can run in any order.
- **Twin logic (the right rule):** Without control statements, statements run once each, top to bottom.
- **Role:** primary

**15. `if_statement` &rarr; `ProgramLooksAhead`** (misconception)

- **Exact edge logic (the wrong rule):** The program knows or sees what later lines will do and acts on those goals at the current line, e.g. it stops 'at ten' because it wants to draw a box.
- **Twin logic (the right rule):** Each statement executes using only the current state; later lines have no effect until control reaches them.
- **Role:** context

**16. `loop_body` &rarr; `ComputerFillsInIntent`** (misconception)

- **Exact edge logic (the wrong rule):** The computer fills in omitted steps or values that the programmer meant, e.g. REPEAT 4 [FORWARD 30] draws a square without a turn command.
- **Twin logic (the right rule):** The computer executes only what the code states; every needed step and value must be written.
- **Role:** context

**17. `program_layout` &rarr; `WhitespaceIsSignificant`** (misconception)

- **Exact edge logic (the wrong rule):** Line breaks and indentation change what the program does, so each statement must be on its own line.
- **Twin logic (the right rule):** Java compilers consider all whitespace in program text (outside quotation marks) to be equivalent; layout is for human readers.
- **Role:** primary

**18. `program_text` &rarr; `ComputerFillsInIntent`** (misconception)

- **Exact edge logic (the wrong rule):** The computer fills in omitted steps or values that the programmer meant, e.g. REPEAT 4 [FORWARD 30] draws a square without a turn command.
- **Twin logic (the right rule):** The computer executes only what the code states; every needed step and value must be written.
- **Role:** context

**19. `statement` &rarr; `StatementNeedsNoTerminator`** (error)

- **Exact edge logic (the wrong rule):** A statement still compiles and runs if the semicolon at its end is left out, or if a stray ; is put right after if (c) or for (...).
- **Twin logic (the right rule):** Each statement must end with ;, otherwise javac reports ';' expected.
- **Role:** primary

**20. `compile_time_error` &rarr; `StatementNeedsNoTerminator`** (error)

- **Exact edge logic (the wrong rule):** a statement runs without the ;
- **Twin logic (the right rule):** Each statement must end with ;, otherwise javac reports ';' expected.
- **Role:** context

**21. `statement` &rarr; `statement@L0`** (has_level)

- **Exact edge logic:** statement -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (6 ways).
  - **[0] everyday\_reading** (rule type E, folk-meaning rule): Everyday reading: a program is read like a text or a list of wishes that the computer takes in all at once, so line order, goals of later lines or what the writer meant can matter. Java rule: each statement is one step, ended by ;, executed once, in written order, using only the current state.
  - **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `ComputerFillsInIntent`: wrong rule: The computer fills in omitted steps or values the programmer meant. Right rule: The computer executes only the statements written; every needed step and value must be written.
  - **[2] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `ComputerFillsInIntent`: Applies the sequencing rule (LT) unevenly: executes the statements in order on some lines but lets a later statement's effect leak into an earlier one, or skips or repeats a statement on one pass. (here mixing in: "The computer fills in omitted steps or values that the programmer meant, e.g. REPEAT 4 [FORWARD 30] draws a square without a turn command")
  - **[3] misconception** (rule type M, wrong rule / right rule) &rarr; `StatementsRunInAnyOrder`: wrong rule: Statements in a program can run in any order, so their order makes no difference. Right rule: Without control statements, statements run once each, top to bottom, in the order written.
  - **[4] misconception** (rule type M, wrong rule / right rule) &rarr; `WhitespaceIsSignificant`: wrong rule: Line breaks and indentation change what the program does, so each statement must be on its own line. Right rule: Java compilers treat all whitespace outside quotes as equivalent; statements are separated by ;, not by line breaks.
  - **[5] misconception** (rule type M, wrong rule / right rule) &rarr; `ProgramLooksAhead`: wrong rule: The program knows what later lines will do and acts on that goal at the current line. Right rule: Each statement executes using only the current state; later lines have no effect until control reaches them.

**22. `statement` &rarr; `statement@L1`** (has_level)

- **Exact edge logic:** statement -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).
  - **[0] names\_the\_element** (rule type N, identity rule): A statement is one step of a program (a declaration, assignment, method call such as System.out.println(...), or control statement), ended by a semicolon when it is a simple statement.
  - **[1] states\_the\_rule** (rule type S, declarative rule): A method body is a sequence of statements enclosed in braces and each followed by a semicolon; statements are executed for their effect and have no value; an expression statement evaluates its expression and discards any value.

**23. `statement` &rarr; `statement@L2`** (has_level)

- **Exact edge logic:** statement -&gt; L2 (Multistructural): the answer applies the rules of statement to every part of the code, in order (3 ways).
  - **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): Statements run one at a time, from first to last; each completes (normally or abruptly) before the next starts.
  - **[1] output\_prediction** (rule type OP, evaluation / result rule): A statement has no value; its result is its effect: a changed variable, printed output, or a change of control flow.
  - **[2] one\_step\_execution** (rule type OS, state-transition rule): Executing one statement applies its single effect to the current state (e.g. prints one string, or stores one value) and then control moves to the next statement.

**24. `statement` &rarr; `statement@L3`** (has_level)

- **Exact edge logic:** statement -&gt; L3 (Relational): the answer relates the parts (8 ways).
  - **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Statements live in main's body; running the program executes main's statements in order.
  - **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): A block groups a sequence of statements in braces; the body of main() is such a block.
  - **[2] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): System.out.print(s); is a statement, so its output appears exactly at its place in the sequence, with no newline.
  - **[3] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): System.out.println(s); is a statement, so its line of output appears at its place in the sequence; swapping two println statements swaps the output lines.
  - **[4] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Control flow is the order in which statements run; without control statements it is straight-line, each once in order.
  - **[5] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): A lone ; is the empty statement, which does nothing; it can fill a for-loop part or, by accident, end an if or loop header.
  - **[6] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): An algorithm becomes a program as a sequence of statements, executed once each in the order given.
  - **[7] purpose\_of\_the\_whole** (rule type P, plan / role rule): Purpose: a statement is the unit of action; a program is characterized by its sequence of statements, each doing one step of the algorithm.

**25. `statement` &rarr; `statement@L4`** (has_level)

- **Exact edge logic:** statement -&gt; L4 (Extended abstract): the answer reasons beyond the given code (4 ways).
  - **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `ComputerFillsInIntent`: Swapping two statements that touch the same variable or the output generally changes the result; swapping independent statements, or changing only whitespace between them, keeps it.
  - **[1] diagnose\_an\_error** (rule type D, error rule): rule broken: Each simple statement must end with ;. Kind: compile-time. Trigger class: omitting the ; at the end of a statement: javac reports ';' expected (often at the end of that line or the next)
  - **[2] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Write one statement per step and order them as the algorithm requires; straight-line sequence suffices when every step runs once, otherwise use conditionals or loops.
  - **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: A ; directly after an if/while/for header is an empty statement. Kind: silent logic error. Trigger class: if (x &gt; 0); or while (cond); followed by the intended body

**26. `topic1.1.b` &rarr; `statement`** (contains)

- topic `topic1.1.b` contains `statement`

**27. `topic1.1.b` &rarr; `block`** (contains)

- topic `topic1.1.b` contains `block`

**28. `topic1.1.b` &rarr; `class_declaration`** (contains)

- topic `topic1.1.b` contains `class_declaration`

**29. `topic1.1.b` &rarr; `comment`** (contains)

- topic `topic1.1.b` contains `comment`

**30. `topic1.1.b` &rarr; `main_method`** (contains)

- topic `topic1.1.b` contains `main_method`

**31. `topic1.1.b` &rarr; `print`** (contains)

- topic `topic1.1.b` contains `print`

**32. `topic1.1.b` &rarr; `println`** (contains)

- topic `topic1.1.b` contains `println`

**33. `topic1.1.b` &rarr; `program_layout`** (contains)

- topic `topic1.1.b` contains `program_layout`

**34. `topic1.1.b` &rarr; `string_literal`** (contains)

- topic `topic1.1.b` contains `string_literal`
