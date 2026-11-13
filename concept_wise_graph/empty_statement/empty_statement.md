# empty_statement (`empty_statement`)

a lone ; is an empty statement; a block can stand alone

Section 1.3 Conditionals and Loops, topic 1.3.b If statements.

![The knowledge graph around empty_statement](empty_statement.png)

## At a glance

- **Needs first:** `statement`
- **Leads to:** `logical_error`
- **Learned alongside:** nothing
- **Misconceptions:** none
- **Errors:** `SemicolonAfterIfHeader`, `SemicolonAfterLoopHeader`
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 19 edges around this concept, each explained in the graph's own words.

## What it needs first (1)

A prerequisite edge means the other concept has to be understood before `empty_statement`.

### `statement` comes before `empty_statement`

*one step, terminated by ;, executed in sequence*

Any part of a for loop, including its body, can be left empty (a null statement, a lone ;); the book prefers a while loop to null statements.

- **Grounding:** book passage
- **How `empty_statement` combines with `statement`:** The empty statement can stand wherever a statement is required (if body, loop body, for slots), and a block { } can stand alone; a ; after a header therefore silently becomes the body.
- **How `statement` combines with `empty_statement`:** A lone ; is the empty statement, which does nothing; it can fill a for-loop part or, by accident, end an if or loop header.

## What it leads to (1)

These concepts need `empty_statement` first.

### `empty_statement` comes before `logical_error`

*the program runs but computes the wrong result*

A ; right after an if or loop header is an empty statement, so the header controls nothing and the next line always runs: the program compiles but computes the wrong result.

- **Grounding:** spec passage

## Learned alongside (0)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

No parallel edge touches this concept.

## Misconceptions (0)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

The graph has no misconception edge from this concept.

## Errors (2)

An error edge states the rule that gets broken in a program, and the right rule.

### SemicolonAfterIfHeader

- **Wrong rule:** if (x &gt; 0); System.out.println("positive"); prints only for positive x.
- **Right rule:** The ; ends the if with an empty statement, so the next line always runs.
- **Role of this concept:** context
- **Also an edge from `for_loop`:** if (x &gt; 0); System.out.println("positive"); prints only for positive x.
- **Also an edge from `if_statement`:** if (x &gt; 0); System.out.println("positive"); prints only for positive x.
- **Also an edge from `logical_error`:** if (x &gt; 0); System.out.println("positive"); prints only for positive x.
- **Also an edge from `while_loop`:** if (x &gt; 0); System.out.println("positive"); prints only for positive x.

### SemicolonAfterLoopHeader

- **Wrong rule:** Puts a ; right after for (...) or while (...).
- **Right rule:** A ; right after the loop header is a null (empty) loop body, so the statements written after it are not repeated by the loop.
- **Role of this concept:** context
- **Also an edge from `for_loop`:** Puts a ; right after for (...) or while (...).
- **Also an edge from `while_loop`:** Puts a ; right after for (...) or while (...).

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for empty statement: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to empty statement agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

empty statement -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (1 way).

- **everyday reading** (folk-meaning rule): Folk meaning: in English a semicolon just separates or ends a clause, so 'if (x &gt; 0);' still reads as 'if x is positive, do the next thing'. In Java a lone ; is a complete statement that does nothing, and it becomes the whole body of the if or loop.

### L1: Unistructural / atom x text surface

L1 for empty statement: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

empty statement -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

- **names the element** (identity rule): The empty (null) statement is a lone semicolon: a statement that does nothing.
- **states the rule** (declarative rule): An empty statement does nothing, and its execution always completes normally; any part of a for loop, including its body, may be left empty, but a while loop is better style than null statements.

### L2: Multistructural / block x execution / preoperational

L2 for empty statement: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

empty statement -&gt; L2 (Multistructural): the answer applies the rules of empty statement to every part of the code, in order (3 ways).

- **line by line trace** (operational sequencing rule): Executing ; does nothing and passes control to the next statement; as a loop body it means each pass is just test (then update, for a for loop).
- **output prediction** (evaluation / result rule): An empty statement produces no value and no output; e.g. for (int v = 1; v &lt;= N/2; v \*= 2) ; computes the same final v as the while version, but v is out of scope afterwards.
- **one step execution** (state-transition rule): One execution changes no variable and returns nothing; only the header parts around it (test, update) change state.

### L3: Relational / relations x function (concrete operational begins)

L3 for empty statement: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

empty statement -&gt; L3 (Relational): the answer relates the parts (2 ways).

- **relation to neighbour** (composition rule (with a neighbour)): The empty statement can stand wherever a statement is required (if body, loop body, for slots), and a block { } can stand alone; a ; after a header therefore silently becomes the body.
- **purpose of the whole** (plan / role rule): Plan: placeholder - an intentionally empty body when the loop header does all the work; the book avoids it and prefers a while loop.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for empty statement: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

empty statement -&gt; L4 (Extended abstract): the answer reasons beyond the given code (4 ways).

- **predict a change** (conservation rule): Deleting a ; that stands right after an if or loop header changes the program: the next statement becomes the body. Adding or removing an extra ; between ordinary statements changes nothing.
- **diagnose an error** (error rule): rule broken: A ; right after if (...) is an empty statement that forms the whole then branch; the following statement or block is no longer part of the if. Kind: silent logic error. Trigger class: Any if (cond); followed by a statement or block: that statement runs for every input, whatever cond is (it compiles without error).
- **diagnose an error** (error rule): rule broken: A ; right after while (...) or for (...) is an empty statement that is the whole loop body; the block written next is not repeated. Kind: silent logic error. Trigger class: for (...); { body } runs the body once after the loop ends; while (cond); with a cond that the empty body cannot change hangs forever (infinite loop) when cond starts true.
- **transfer to a new program** (applicability rule): Use an empty statement only for a loop whose header does all the work, and comment it; otherwise write { } or restructure as a while loop. Never put ; directly after if (...), while (...) or for (...) by habit.

## Same topic

`empty_statement` belongs to the topic **If statements** (`topic1.3.b`). The topic also contains: `if_else_statement`, `if_statement`, `syntax_template`.

## Rules of the concept (13)

- **folk-meaning rule:** Folk meaning: in English a semicolon just separates or ends a clause, so 'if (x &gt; 0);' still reads as 'if x is positive, do the next thing'. In Java a lone ; is a complete statement that does nothing, and it becomes the whole body of the if or loop.
- **uneven-application rule:** Applies the empty-statement rule (LT) unevenly: treats a stray ; after an if or loop header as ending the body on one line but not on another, e.g. expects the following block to be controlled.
- **identity rule:** The empty (null) statement is a lone semicolon: a statement that does nothing.
- **declarative rule:** An empty statement does nothing, and its execution always completes normally; any part of a for loop, including its body, may be left empty, but a while loop is better style than null statements.
- **operational sequencing rule:** Executing ; does nothing and passes control to the next statement; as a loop body it means each pass is just test (then update, for a for loop).
- **evaluation / result rule:** An empty statement produces no value and no output; e.g. for (int v = 1; v &lt;= N/2; v \*= 2) ; computes the same final v as the while version, but v is out of scope afterwards.
- **state-transition rule:** One execution changes no variable and returns nothing; only the header parts around it (test, update) change state.
- **composition rule (with a neighbour):** with statement: The empty statement can stand wherever a statement is required (if body, loop body, for slots), and a block { } can stand alone; a ; after a header therefore silently becomes the body.
- **plan / role rule:** Plan: placeholder - an intentionally empty body when the loop header does all the work; the book avoids it and prefers a while loop.
- **conservation rule:** Deleting a ; that stands right after an if or loop header changes the program: the next statement becomes the body. Adding or removing an extra ; between ordinary statements changes nothing.
- **error rule:** rule broken: A ; right after if (...) is an empty statement that forms the whole then branch; the following statement or block is no longer part of the if. (silent logic error)
- **error rule:** rule broken: A ; right after while (...) or for (...) is an empty statement that is the whole loop body; the block written next is not repeated. (silent logic error)
- **applicability rule:** Use an empty statement only for a loop whose header does all the work, and comment it; otherwise write { } or restructure as a while loop. Never put ; directly after if (...), while (...) or for (...) by habit.

## The whole prerequisite chain

- **Everything it builds on (4):** `class_declaration`, `main_method`, `program_text`, `statement`
- **Everything that builds on it (2):** `debugging`, `logical_error`
