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

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 19 edges around this concept. The edge logic, the wrong and right rules and the exact rules of the ways are copied word for word from the graph.

## To work on (1)

- no aliases: a student's words cannot name this concept

## What it needs first (1)

A prerequisite edge means the other concept has to be understood before `empty_statement`.

### `statement` comes before `empty_statement`

*one step, terminated by ;, executed in sequence*

- **Edge:** `pre:statement->empty_statement`
- **Exact edge logic:** Any part of a for loop, including its body, can be left empty (a null statement, a lone ;); the book prefers a while loop to null statements.
- **Grounding:** book\_passage
- **Composition rule (R) of `empty_statement` with `statement`:** The empty statement can stand wherever a statement is required (if body, loop body, for slots), and a block { } can stand alone; a ; after a header therefore silently becomes the body.
- **Composition rule (R) of `statement` with `empty_statement`:** A lone ; is the empty statement, which does nothing; it can fill a for-loop part or, by accident, end an if or loop header.

## What it leads to (1)

These concepts need `empty_statement` first.

### `empty_statement` comes before `logical_error`

*the program runs but computes the wrong result*

- **Edge:** `pre:empty_statement->logical_error`
- **Exact edge logic:** A ; right after an if or loop header is an empty statement, so the header controls nothing and the next line always runs: the program compiles but computes the wrong result.
- **Grounding:** spec\_passage

## Learned alongside (0)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

No parallel edge touches this concept.

## Misconceptions (0)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

The graph has no misconception edge from this concept.

## Errors (2)

An error edge states the rule that gets broken in a program, and the right rule.

### SemicolonAfterIfHeader

- **Edge:** `empty_statement` &rarr; `SemicolonAfterIfHeader` (error)
- **Exact edge logic (the wrong rule):** if (x &gt; 0); System.out.println("positive"); prints only for positive x.
- **Twin logic (the right rule):** The ; ends the if with an empty statement, so the next line always runs.
- **Wrong belief (on the node):** if (x &gt; 0); System.out.println("positive"); prints only for positive x.
- **Correct rule (on the node):** The ; ends the if with an empty statement, so the next line always runs.
- **Provenance:** published
- **Role of this concept:** context
- **Edge `for_loop` &rarr; `SemicolonAfterIfHeader`, exact edge logic:** if (x &gt; 0); System.out.println("positive"); prints only for positive x. **Twin logic:** The ; ends the if with an empty statement, so the next line always runs. (role: context)
- **Edge `if_statement` &rarr; `SemicolonAfterIfHeader`, exact edge logic:** if (x &gt; 0); System.out.println("positive"); prints only for positive x. **Twin logic:** The ; ends the if with an empty statement, so the next line always runs. (role: primary)
- **Edge `logical_error` &rarr; `SemicolonAfterIfHeader`, exact edge logic:** if (x &gt; 0); System.out.println("positive"); prints only for positive x. **Twin logic:** The ; ends the if with an empty statement, so the next line always runs. (role: context)
- **Edge `while_loop` &rarr; `SemicolonAfterIfHeader`, exact edge logic:** if (x &gt; 0); System.out.println("positive"); prints only for positive x. **Twin logic:** The ; ends the if with an empty statement, so the next line always runs. (role: context)

### SemicolonAfterLoopHeader

- **Edge:** `empty_statement` &rarr; `SemicolonAfterLoopHeader` (error)
- **Exact edge logic (the wrong rule):** Puts a ; right after for (...) or while (...).
- **Twin logic (the right rule):** A ; right after the loop header is a null (empty) loop body, so the statements written after it are not repeated by the loop.
- **Wrong belief (on the node):** Puts a ; right after for (...) or while (...).
- **Correct rule (on the node):** A ; right after the loop header is a null (empty) loop body, so the statements written after it are not repeated by the loop.
- **Provenance:** textbook
- **Role of this concept:** context
- **Edge `for_loop` &rarr; `SemicolonAfterLoopHeader`, exact edge logic:** Puts a ; right after for (...) or while (...). **Twin logic:** A ; right after the loop header is a null (empty) loop body, so the statements written after it are not repeated by the loop. (role: primary)
- **Edge `while_loop` &rarr; `SemicolonAfterLoopHeader`, exact edge logic:** Puts a ; right after for (...) or while (...). **Twin logic:** A ; right after the loop header is a null (empty) loop body, so the statements written after it are not repeated by the loop. (role: context)

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for empty statement: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to empty statement agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

- **Edge:** `empty_statement` &rarr; `empty_statement@L0` (has_level)
- **Exact edge logic:** empty statement -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (1 way).

Ways (1), each with its exact rule:

- **[0] everyday\_reading** (rule type E, folk-meaning rule): Folk meaning: in English a semicolon just separates or ends a clause, so 'if (x &gt; 0);' still reads as 'if x is positive, do the next thing'. In Java a lone ; is a complete statement that does nothing, and it becomes the whole body of the if or loop.

### L1: Unistructural / atom x text surface

L1 for empty statement: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

- **Edge:** `empty_statement` &rarr; `empty_statement@L1` (has_level)
- **Exact edge logic:** empty statement -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

Ways (2), each with its exact rule:

- **[0] names\_the\_element** (rule type N, identity rule): The empty (null) statement is a lone semicolon: a statement that does nothing.
- **[1] states\_the\_rule** (rule type S, declarative rule): An empty statement does nothing, and its execution always completes normally; any part of a for loop, including its body, may be left empty, but a while loop is better style than null statements.

### L2: Multistructural / block x execution / preoperational

L2 for empty statement: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

- **Edge:** `empty_statement` &rarr; `empty_statement@L2` (has_level)
- **Exact edge logic:** empty statement -&gt; L2 (Multistructural): the answer applies the rules of empty statement to every part of the code, in order (3 ways).

Ways (3), each with its exact rule:

- **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): Executing ; does nothing and passes control to the next statement; as a loop body it means each pass is just test (then update, for a for loop).
- **[1] output\_prediction** (rule type OP, evaluation / result rule): An empty statement produces no value and no output; e.g. for (int v = 1; v &lt;= N/2; v \*= 2) ; computes the same final v as the while version, but v is out of scope afterwards.
- **[2] one\_step\_execution** (rule type OS, state-transition rule): One execution changes no variable and returns nothing; only the header parts around it (test, update) change state.

### L3: Relational / relations x function (concrete operational begins)

L3 for empty statement: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

- **Edge:** `empty_statement` &rarr; `empty_statement@L3` (has_level)
- **Exact edge logic:** empty statement -&gt; L3 (Relational): the answer relates the parts (2 ways).

Ways (2), each with its exact rule:

- **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): The empty statement can stand wherever a statement is required (if body, loop body, for slots), and a block { } can stand alone; a ; after a header therefore silently becomes the body.
- **[1] purpose\_of\_the\_whole** (rule type P, plan / role rule): Plan: placeholder - an intentionally empty body when the loop header does all the work; the book avoids it and prefers a while loop.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for empty statement: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

- **Edge:** `empty_statement` &rarr; `empty_statement@L4` (has_level)
- **Exact edge logic:** empty statement -&gt; L4 (Extended abstract): the answer reasons beyond the given code (4 ways).

Ways (4), each with its exact rule:

- **[0] predict\_a\_change** (rule type C, conservation rule): Deleting a ; that stands right after an if or loop header changes the program: the next statement becomes the body. Adding or removing an extra ; between ordinary statements changes nothing.
- **[1] diagnose\_an\_error** (rule type D, error rule): rule broken: A ; right after if (...) is an empty statement that forms the whole then branch; the following statement or block is no longer part of the if. Kind: silent logic error. Trigger class: Any if (cond); followed by a statement or block: that statement runs for every input, whatever cond is (it compiles without error).
- **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: A ; right after while (...) or for (...) is an empty statement that is the whole loop body; the block written next is not repeated. Kind: silent logic error. Trigger class: for (...); { body } runs the body once after the loop ends; while (cond); with a cond that the empty body cannot change hangs forever (infinite loop) when cond starts true.
- **[3] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Use an empty statement only for a loop whose header does all the work, and comment it; otherwise write { } or restructure as a while loop. Never put ; directly after if (...), while (...) or for (...) by habit.

## Same topic

`empty_statement` belongs to the topic **If statements** (`topic1.3.b`). The topic also contains: `if_else_statement`, `if_statement`, `syntax_template`.

## Rules of the concept (13)

- **Book** (SW-1e, p. 76 (pdf 86)): "It is generally better style to use a while statement than null statements in a for loop."
- **Book** (SW-1.3, ): "It is legal (but uncommon) to have a block that does not belong to a conditional statement, loop, or method."
- **E** (folk-meaning rule): Folk meaning: in English a semicolon just separates or ends a clause, so 'if (x &gt; 0);' still reads as 'if x is positive, do the next thing'. In Java a lone ; is a complete statement that does nothing, and it becomes the whole body of the if or loop.
- **T** (uneven-application rule): Applies the empty-statement rule (LT) unevenly: treats a stray ; after an if or loop header as ending the body on one line but not on another, e.g. expects the following block to be controlled.
- **N** (identity rule): The empty (null) statement is a lone semicolon: a statement that does nothing.
- **S** (declarative rule): An empty statement does nothing, and its execution always completes normally; any part of a for loop, including its body, may be left empty, but a while loop is better style than null statements.
- **LT** (operational sequencing rule): Executing ; does nothing and passes control to the next statement; as a loop body it means each pass is just test (then update, for a for loop).
- **OP** (evaluation / result rule): An empty statement produces no value and no output; e.g. for (int v = 1; v &lt;= N/2; v \*= 2) ; computes the same final v as the while version, but v is out of scope afterwards.
- **OS** (state-transition rule): One execution changes no variable and returns nothing; only the header parts around it (test, update) change state.
- **R** (composition rule (with a neighbour)): with statement: The empty statement can stand wherever a statement is required (if body, loop body, for slots), and a block { } can stand alone; a ; after a header therefore silently becomes the body.
- **P** (plan / role rule): Plan: placeholder - an intentionally empty body when the loop header does all the work; the book avoids it and prefers a while loop.
- **C** (conservation rule): Deleting a ; that stands right after an if or loop header changes the program: the next statement becomes the body. Adding or removing an extra ; between ordinary statements changes nothing.
- **D** (error rule): rule broken: A ; right after if (...) is an empty statement that forms the whole then branch; the following statement or block is no longer part of the if. (silent logic error)
- **D** (error rule): rule broken: A ; right after while (...) or for (...) is an empty statement that is the whole loop body; the block written next is not repeated. (silent logic error)
- **X** (applicability rule): Use an empty statement only for a loop whose header does all the work, and comment it; otherwise write { } or restructure as a while loop. Never put ; directly after if (...), while (...) or for (...) by habit.

## How it is found in code and answers (reader block)

- **Aliases:** none
- **Code patterns:** none
- **Operator symbols:** none
- **Java types:** none
- **Signal empty\_body** (scope program, decisive): `(?:^|[;{])[ \t]*(?:if|while|for)\s*\((?:[^()]|\([^()]*\))*\)\s*;`
- **Signal lone\_semicolon** (scope program): `^\s*;\s*$`

## The whole prerequisite chain

- **Everything it builds on (4):** `class_declaration`, `main_method`, `program_text`, `statement`
- **Everything that builds on it (2):** `debugging`, `logical_error`

## Every edge in this view and its exact edge logic (19)

All the edges drawn in the picture, in the order: prerequisite, parallel, misconception, error, has_level, contains.

**1. `empty_statement` &rarr; `logical_error`** (prerequisite)

- **Exact edge logic:** A ; right after an if or loop header is an empty statement, so the header controls nothing and the next line always runs: the program compiles but computes the wrong result.
- **Grounding:** spec\_passage

**2. `statement` &rarr; `empty_statement`** (prerequisite)

- **Exact edge logic:** Any part of a for loop, including its body, can be left empty (a null statement, a lone ;); the book prefers a while loop to null statements.
- **Grounding:** book\_passage
- **Composition rule (R) of `statement` with `empty_statement`:** A lone ; is the empty statement, which does nothing; it can fill a for-loop part or, by accident, end an if or loop header.
- **Composition rule (R) of `empty_statement` with `statement`:** The empty statement can stand wherever a statement is required (if body, loop body, for slots), and a block { } can stand alone; a ; after a header therefore silently becomes the body.

**3. `empty_statement` &rarr; `SemicolonAfterIfHeader`** (error)

- **Exact edge logic (the wrong rule):** if (x &gt; 0); System.out.println("positive"); prints only for positive x.
- **Twin logic (the right rule):** The ; ends the if with an empty statement, so the next line always runs.
- **Role:** context

**4. `empty_statement` &rarr; `SemicolonAfterLoopHeader`** (error)

- **Exact edge logic (the wrong rule):** Puts a ; right after for (...) or while (...).
- **Twin logic (the right rule):** A ; right after the loop header is a null (empty) loop body, so the statements written after it are not repeated by the loop.
- **Role:** context

**5. `for_loop` &rarr; `SemicolonAfterIfHeader`** (error)

- **Exact edge logic (the wrong rule):** if (x &gt; 0); System.out.println("positive"); prints only for positive x.
- **Twin logic (the right rule):** The ; ends the if with an empty statement, so the next line always runs.
- **Role:** context

**6. `for_loop` &rarr; `SemicolonAfterLoopHeader`** (error)

- **Exact edge logic (the wrong rule):** Puts a ; right after for (...) or while (...).
- **Twin logic (the right rule):** A ; right after the loop header is a null (empty) loop body, so the statements written after it are not repeated by the loop.
- **Role:** primary

**7. `if_statement` &rarr; `SemicolonAfterIfHeader`** (error)

- **Exact edge logic (the wrong rule):** if (x &gt; 0); System.out.println("positive"); prints only for positive x.
- **Twin logic (the right rule):** The ; ends the if with an empty statement, so the next line always runs.
- **Role:** primary

**8. `logical_error` &rarr; `SemicolonAfterIfHeader`** (error)

- **Exact edge logic (the wrong rule):** if (x &gt; 0); System.out.println("positive"); prints only for positive x.
- **Twin logic (the right rule):** The ; ends the if with an empty statement, so the next line always runs.
- **Role:** context

**9. `while_loop` &rarr; `SemicolonAfterIfHeader`** (error)

- **Exact edge logic (the wrong rule):** if (x &gt; 0); System.out.println("positive"); prints only for positive x.
- **Twin logic (the right rule):** The ; ends the if with an empty statement, so the next line always runs.
- **Role:** context

**10. `while_loop` &rarr; `SemicolonAfterLoopHeader`** (error)

- **Exact edge logic (the wrong rule):** Puts a ; right after for (...) or while (...).
- **Twin logic (the right rule):** A ; right after the loop header is a null (empty) loop body, so the statements written after it are not repeated by the loop.
- **Role:** context

**11. `empty_statement` &rarr; `empty_statement@L0`** (has_level)

- **Exact edge logic:** empty statement -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (1 way).
  - **[0] everyday\_reading** (rule type E, folk-meaning rule): Folk meaning: in English a semicolon just separates or ends a clause, so 'if (x &gt; 0);' still reads as 'if x is positive, do the next thing'. In Java a lone ; is a complete statement that does nothing, and it becomes the whole body of the if or loop.

**12. `empty_statement` &rarr; `empty_statement@L1`** (has_level)

- **Exact edge logic:** empty statement -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).
  - **[0] names\_the\_element** (rule type N, identity rule): The empty (null) statement is a lone semicolon: a statement that does nothing.
  - **[1] states\_the\_rule** (rule type S, declarative rule): An empty statement does nothing, and its execution always completes normally; any part of a for loop, including its body, may be left empty, but a while loop is better style than null statements.

**13. `empty_statement` &rarr; `empty_statement@L2`** (has_level)

- **Exact edge logic:** empty statement -&gt; L2 (Multistructural): the answer applies the rules of empty statement to every part of the code, in order (3 ways).
  - **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): Executing ; does nothing and passes control to the next statement; as a loop body it means each pass is just test (then update, for a for loop).
  - **[1] output\_prediction** (rule type OP, evaluation / result rule): An empty statement produces no value and no output; e.g. for (int v = 1; v &lt;= N/2; v \*= 2) ; computes the same final v as the while version, but v is out of scope afterwards.
  - **[2] one\_step\_execution** (rule type OS, state-transition rule): One execution changes no variable and returns nothing; only the header parts around it (test, update) change state.

**14. `empty_statement` &rarr; `empty_statement@L3`** (has_level)

- **Exact edge logic:** empty statement -&gt; L3 (Relational): the answer relates the parts (2 ways).
  - **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): The empty statement can stand wherever a statement is required (if body, loop body, for slots), and a block { } can stand alone; a ; after a header therefore silently becomes the body.
  - **[1] purpose\_of\_the\_whole** (rule type P, plan / role rule): Plan: placeholder - an intentionally empty body when the loop header does all the work; the book avoids it and prefers a while loop.

**15. `empty_statement` &rarr; `empty_statement@L4`** (has_level)

- **Exact edge logic:** empty statement -&gt; L4 (Extended abstract): the answer reasons beyond the given code (4 ways).
  - **[0] predict\_a\_change** (rule type C, conservation rule): Deleting a ; that stands right after an if or loop header changes the program: the next statement becomes the body. Adding or removing an extra ; between ordinary statements changes nothing.
  - **[1] diagnose\_an\_error** (rule type D, error rule): rule broken: A ; right after if (...) is an empty statement that forms the whole then branch; the following statement or block is no longer part of the if. Kind: silent logic error. Trigger class: Any if (cond); followed by a statement or block: that statement runs for every input, whatever cond is (it compiles without error).
  - **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: A ; right after while (...) or for (...) is an empty statement that is the whole loop body; the block written next is not repeated. Kind: silent logic error. Trigger class: for (...); { body } runs the body once after the loop ends; while (cond); with a cond that the empty body cannot change hangs forever (infinite loop) when cond starts true.
  - **[3] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Use an empty statement only for a loop whose header does all the work, and comment it; otherwise write { } or restructure as a while loop. Never put ; directly after if (...), while (...) or for (...) by habit.

**16. `topic1.3.b` &rarr; `empty_statement`** (contains)

- topic `topic1.3.b` contains `empty_statement`

**17. `topic1.3.b` &rarr; `if_else_statement`** (contains)

- topic `topic1.3.b` contains `if_else_statement`

**18. `topic1.3.b` &rarr; `if_statement`** (contains)

- topic `topic1.3.b` contains `if_statement`

**19. `topic1.3.b` &rarr; `syntax_template`** (contains)

- topic `topic1.3.b` contains `syntax_template`
