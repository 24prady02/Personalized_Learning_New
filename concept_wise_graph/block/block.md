# block (`block`)

{ ... } grouping statements

Section 1.1 Your First Program, topic 1.1.b Understanding a program (HelloWorld).

![The knowledge graph around block](block.png)

## At a glance

- **Needs first:** `statement`
- **Leads to:** `program_layout`
- **Learned alongside:** nothing
- **Misconceptions:** `InconsistentIndentation`, `LocalVarOutsideScope`, `LoopBodyStatementOutsideLoop`, `MissingBraces`, `StatementAfterIfInBranch`, `StatementAfterLoopInBody`
- **Errors:** `UnbalancedBraces`
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 36 edges around this concept. The edge logic, the wrong and right rules and the exact rules of the ways are copied word for word from the graph.

## To work on (1)

- misconceptions with no L0 way linked to them: MissingBraces, InconsistentIndentation

## What it needs first (1)

A prerequisite edge means the other concept has to be understood before `block`.

### `statement` comes before `block`

*one step, terminated by ;, executed in sequence*

- **Edge:** `pre:statement->block`
- **Exact edge logic:** A statement block is a sequence of statements, each terminated by a semicolon, enclosed in braces; the body of main() is such a sequence.
- **Grounding:** book\_passage
- **Composition rule (R) of `block` with `statement`:** A block is built from statements, each ended by ;, and is itself usable as a single statement (e.g. a loop body).
- **Composition rule (R) of `statement` with `block`:** A block groups a sequence of statements in braces; the body of main() is such a block.

## What it leads to (1)

These concepts need `block` first.

### `block` comes before `program_layout`

*one statement per line and indentation that shows nesting*

- **Edge:** `pre:block->program_layout`
- **Exact edge logic:** Indentation makes the nesting of blocks visible, so the reader can see which statements belong to which block.
- **Grounding:** book\_passage
- **Composition rule (R) of `block` with `program_layout`:** Indentation should show block nesting, but only braces define it; layout that disagrees with the braces misleads the reader, not the compiler.
- **Composition rule (R) of `program_layout` with `block`:** Indentation should show which statements belong to which block; braces, not indentation, decide it, so wrong indentation misleads.

## Learned alongside (0)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

No parallel edge touches this concept.

## Misconceptions (6)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### InconsistentIndentation

- **Edge:** `block` &rarr; `InconsistentIndentation` (misconception)
- **Exact edge logic (the wrong rule):** Indents nested blocks inconsistently, so the visual nesting differs from the real nesting.
- **Twin logic (the right rule):** Indent consistently, one level deeper for each nested block, so the layout shows the real nesting; the compiler ignores indentation.
- **Wrong belief (on the node):** Indents nested blocks inconsistently, so the visual nesting differs from the real nesting.
- **Correct rule (on the node):** Indent consistently, one level deeper for each nested block, so the layout shows the real nesting; the compiler ignores indentation.
- **Provenance:** rule\_dictionary
- **Role of this concept:** context
- **L0 way linked to it:** no
- **Edge `nested_conditionals` &rarr; `InconsistentIndentation`, exact edge logic:** Indents nested blocks inconsistently, so the visual nesting differs from the real nesting. **Twin logic:** Indent consistently, one level deeper for each nested block, so the layout shows the real nesting; the compiler ignores indentation. (role: context)
- **Edge `nested_loops` &rarr; `InconsistentIndentation`, exact edge logic:** Indents nested blocks inconsistently, so the visual nesting differs from the real nesting. **Twin logic:** Indent consistently, one level deeper for each nested block, so the layout shows the real nesting; the compiler ignores indentation. (role: context)
- **Edge `program_layout` &rarr; `InconsistentIndentation`, exact edge logic:** Indents nested blocks inconsistently, so the visual nesting differs from the real nesting. **Twin logic:** Indent consistently, one level deeper for each nested block, so the layout shows the real nesting; the compiler ignores indentation. (role: primary)

### LocalVarOutsideScope

- **Edge:** `block` &rarr; `LocalVarOutsideScope` (misconception)
- **Exact edge logic (the wrong rule):** A variable declared inside a block can be used anywhere in the program, like a global.
- **Twin logic (the right rule):** A local variable exists only from its declaration to the end of its block.
- **Wrong belief (on the node):** A variable declared inside a block can be used anywhere in the program, like a global.
- **Correct rule (on the node):** A local variable exists only from its declaration to the end of its block.
- **Provenance:** published
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [1] misconception, exact rule:** wrong rule: A variable declared inside a block can be used anywhere in the program, like a global. Right rule: A local variable's scope runs from its declaration to the end of the enclosing block.
- **L0 way [2] inconsistent\_trace, exact rule:** Applies the block rule (LT: all statements of the block in order, the whole block as one unit) unevenly: includes the statement after the closing brace in the body on one pass but not another, or runs only part of the body. (here mixing in: "A variable declared inside a block can be used anywhere in the program, like a global")
- **Edge `loop_scope` &rarr; `LocalVarOutsideScope`, exact edge logic:** A variable declared inside a block can be used anywhere in the program, like a global. **Twin logic:** A local variable exists only from its declaration to the end of its block. (role: primary)
- **Edge `variable` &rarr; `LocalVarOutsideScope`, exact edge logic:** A variable declared inside a block can be used anywhere in the program, like a global. **Twin logic:** A local variable exists only from its declaration to the end of its block. (role: context)

### LoopBodyStatementOutsideLoop

- **Edge:** `block` &rarr; `LoopBodyStatementOutsideLoop` (misconception)
- **Exact edge logic (the wrong rule):** Some statements inside the braces of a loop body are not repeated; they run once, before or after the loop.
- **Twin logic (the right rule):** Every statement inside the loop braces is part of the body and runs on every pass.
- **Wrong belief (on the node):** Some statements inside the braces of a loop body are not repeated; they run once, before or after the loop.
- **Correct rule (on the node):** Every statement inside the loop braces is part of the body and runs on every pass.
- **Provenance:** published
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [4] misconception, exact rule:** wrong rule: Some statements inside the loop braces are not repeated; they run once, before or after the loop. Right rule: Every statement inside the loop braces is part of the body and runs on every pass.
- **Edge `loop_body` &rarr; `LoopBodyStatementOutsideLoop`, exact edge logic:** Some statements inside the braces of a loop body are not repeated; they run once, before or after the loop. **Twin logic:** Every statement inside the loop braces is part of the body and runs on every pass. (role: primary)

### MissingBraces

- **Edge:** `block` &rarr; `MissingBraces` (misconception)
- **Exact edge logic (the wrong rule):** Omits braces around a single-statement body of if, for or while.
- **Twin logic (the right rule):** Braces are optional for a single-statement body, but using them anyway avoids bugs when statements are added later.
- **Wrong belief (on the node):** Omits braces around a single-statement body of if, for or while.
- **Correct rule (on the node):** Braces are optional for a single-statement body, but using them anyway avoids bugs when statements are added later.
- **Provenance:** rule\_dictionary
- **Role of this concept:** context
- **L0 way linked to it:** no
- **Edge `for_loop` &rarr; `MissingBraces`, exact edge logic:** Omits braces around a single-statement body of if, for or while. **Twin logic:** Braces are optional for a single-statement body, but using them anyway avoids bugs when statements are added later. (role: context)
- **Edge `if_statement` &rarr; `MissingBraces`, exact edge logic:** Omits braces around a single-statement body of if, for or while. **Twin logic:** Braces are optional for a single-statement body, but using them anyway avoids bugs when statements are added later. (role: primary)
- **Edge `while_loop` &rarr; `MissingBraces`, exact edge logic:** Omits braces around a single-statement body of if, for or while. **Twin logic:** Braces are optional for a single-statement body, but using them anyway avoids bugs when statements are added later. (role: context)

### StatementAfterIfInBranch

- **Edge:** `block` &rarr; `StatementAfterIfInBranch` (misconception)
- **Exact edge logic (the wrong rule):** A statement placed after the if statement belongs to its branch, so it runs only when the condition is true.
- **Twin logic (the right rule):** The branch ends at its closing brace (or after its single statement); the next statement runs whatever the condition was.
- **Wrong belief (on the node):** A statement placed after the if statement belongs to its branch, so it runs only when the condition is true.
- **Correct rule (on the node):** The branch ends at its closing brace (or after its single statement); the next statement runs whatever the condition was.
- **Provenance:** published
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [3] misconception, exact rule:** wrong rule: A statement placed after the if statement belongs to its branch, so it runs only when the condition is true. Right rule: The branch ends at its closing brace (or after its single statement); the next statement runs whatever the condition was.
- **Edge `if_statement` &rarr; `StatementAfterIfInBranch`, exact edge logic:** A statement placed after the if statement belongs to its branch, so it runs only when the condition is true. **Twin logic:** The branch ends at its closing brace (or after its single statement); the next statement runs whatever the condition was. (role: primary)

### StatementAfterLoopInBody

- **Edge:** `block` &rarr; `StatementAfterLoopInBody` (misconception)
- **Exact edge logic (the wrong rule):** A statement written after the loop is repeated with the loop body.
- **Twin logic (the right rule):** The body ends at the closing brace (or after its single statement); code after it runs once, after the loop ends.
- **Wrong belief (on the node):** A statement written after the loop is repeated with the loop body.
- **Correct rule (on the node):** The body ends at the closing brace (or after its single statement); code after it runs once, after the loop ends.
- **Provenance:** published
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [5] misconception, exact rule:** wrong rule: A statement written after the loop is repeated with the loop body. Right rule: The body ends at the closing brace (or after its single statement); code after it runs once, after the loop ends.
- **Edge `loop_body` &rarr; `StatementAfterLoopInBody`, exact edge logic:** A statement written after the loop is repeated with the loop body. **Twin logic:** The body ends at the closing brace (or after its single statement); code after it runs once, after the loop ends. (role: primary)

## Errors (1)

An error edge states the rule that gets broken in a program, and the right rule.

### UnbalancedBraces

- **Edge:** `block` &rarr; `UnbalancedBraces` (error)
- **Exact edge logic (the wrong rule):** A missing { or } is harmless.
- **Twin logic (the right rule):** Every { must be matched by a } so the class body and the method body are well formed.
- **Wrong belief (on the node):** A missing { or } is harmless.
- **Correct rule (on the node):** Every { must be matched by a } so the class body and the method body are well formed.
- **Provenance:** published
- **Role of this concept:** primary
- **Edge `class_declaration` &rarr; `UnbalancedBraces`, exact edge logic:** A missing { or } is harmless. **Twin logic:** Every { must be matched by a } so the class body and the method body are well formed. (role: context)
- **Edge `compile_time_error` &rarr; `UnbalancedBraces`, exact edge logic:** A missing { or } is harmless. **Twin logic:** Every { must be matched by a } so the class body and the method body are well formed. (role: context)

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for block: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to block agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

- **Edge:** `block` &rarr; `block@L0` (has_level)
- **Exact edge logic:** block -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (6 ways).

Ways (6), each with its exact rule:

- **[0] everyday\_reading** (rule type E, folk-meaning rule): Everyday/visual reading: indentation or line position tells you what belongs together, as in an outline. Java rule: only braces delimit a block; indentation is ignored, and without braces an if or loop body is just the next single statement.
- **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `LocalVarOutsideScope`: wrong rule: A variable declared inside a block can be used anywhere in the program, like a global. Right rule: A local variable's scope runs from its declaration to the end of the enclosing block.
- **[2] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `LocalVarOutsideScope`: Applies the block rule (LT: all statements of the block in order, the whole block as one unit) unevenly: includes the statement after the closing brace in the body on one pass but not another, or runs only part of the body. (here mixing in: "A variable declared inside a block can be used anywhere in the program, like a global")
- **[3] misconception** (rule type M, wrong rule / right rule) &rarr; `StatementAfterIfInBranch`: wrong rule: A statement placed after the if statement belongs to its branch, so it runs only when the condition is true. Right rule: The branch ends at its closing brace (or after its single statement); the next statement runs whatever the condition was.
- **[4] misconception** (rule type M, wrong rule / right rule) &rarr; `LoopBodyStatementOutsideLoop`: wrong rule: Some statements inside the loop braces are not repeated; they run once, before or after the loop. Right rule: Every statement inside the loop braces is part of the body and runs on every pass.
- **[5] misconception** (rule type M, wrong rule / right rule) &rarr; `StatementAfterLoopInBody`: wrong rule: A statement written after the loop is repeated with the loop body. Right rule: The body ends at the closing brace (or after its single statement); code after it runs once, after the loop ends.

### L1: Unistructural / atom x text surface

L1 for block: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

- **Edge:** `block` &rarr; `block@L1` (has_level)
- **Exact edge logic:** block -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

Ways (2), each with its exact rule:

- **[0] names\_the\_element** (rule type N, identity rule): A block (statement block) is a sequence of statements enclosed in braces { }; it counts as one statement where a single statement is expected.
- **[1] states\_the\_rule** (rule type S, declarative rule): A block is a sequence of statements and local variable declarations within braces; a variable declared in a block is in scope only from its declaration to the end of that block.

### L2: Multistructural / block x execution / preoperational

L2 for block: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

- **Edge:** `block` &rarr; `block@L2` (has_level)
- **Exact edge logic:** block -&gt; L2 (Multistructural): the answer applies the rules of block to every part of the code, in order (3 ways).

Ways (3), each with its exact rule:

- **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): A block executes each of its statements in order from first to last; if a statement completes abruptly, the rest of the block is skipped.
- **[1] output\_prediction** (rule type OP, evaluation / result rule): A block has no value; its result is the combined effect of its statements, in order.
- **[2] one\_step\_execution** (rule type OS, state-transition rule): Entering a block makes room for its local variables; leaving it (at the closing brace) ends their scope, so they can no longer be used.

### L3: Relational / relations x function (concrete operational begins)

L3 for block: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

- **Edge:** `block` &rarr; `block@L3` (has_level)
- **Exact edge logic:** block -&gt; L3 (Relational): the answer relates the parts (3 ways).

Ways (3), each with its exact rule:

- **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): A block is built from statements, each ended by ;, and is itself usable as a single statement (e.g. a loop body).
- **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Indentation should show block nesting, but only braces define it; layout that disagrees with the braces misleads the reader, not the compiler.
- **[2] purpose\_of\_the\_whole** (rule type P, plan / role rule): Purpose: group several statements so they act as one body (of main, an if branch or a loop) and limit the scope of variables to where they are needed.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for block: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

- **Edge:** `block` &rarr; `block@L4` (has_level)
- **Exact edge logic:** block -&gt; L4 (Extended abstract): the answer reasons beyond the given code (5 ways).

Ways (5), each with its exact rule:

- **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `LocalVarOutsideScope`: Adding braces around a single-statement body keeps behaviour; adding a second statement to a braceless body changes it (the new statement runs outside); moving a declaration into a block makes later uses outside the block fail to compile.
- **[1] diagnose\_an\_error** (rule type D, error rule): rule broken: Every { must be matched by a }. Kind: compile-time. Trigger class: a missing or extra brace: javac reports '{' expected, 'class' or 'interface' expected, or reached end of file while parsing, often on a later line
- **[2] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Use a block whenever a body has more than one statement (S&amp;W and TJ advise braces even for one), and declare variables in the innermost block that needs them.
- **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: Without braces only one statement is the body. Kind: silent logic error. Trigger class: a multi-statement body written without braces, indented as if all were inside
- **[4] diagnose\_an\_error** (rule type D, error rule): rule broken: A local variable is visible only inside its block. Kind: compile-time. Trigger class: using a variable after the block that declared it has closed (cannot find symbol)

## Same topic

`block` belongs to the topic **Understanding a program (HelloWorld)** (`topic1.1.b`). The topic also contains: `class_declaration`, `comment`, `main_method`, `print`, `println`, `program_layout`, `statement`, `string_literal`.

## Rules of the concept (19)

- **Book** (SW-1e, p. 6 (pdf 16)): "The first line of a method specifies its name and other information; the rest is a sequence of statements enclosed in braces and each followed by a semicolon."
- **Book** (OT-Expressions, ): "A block is a group of zero or more statements between balanced braces and can be used anywhere a single statement is allowed."
- **Book** (GJS, ): "Each time a new block or block-like construct is opened, the indent increases by two spaces."
- **Book** (JLS-14, ): "A block is a sequence of statements, local class declarations, and local variable declaration statements within braces."
- **E** (folk-meaning rule): Everyday/visual reading: indentation or line position tells you what belongs together, as in an outline. Java rule: only braces delimit a block; indentation is ignored, and without braces an if or loop body is just the next single statement.
- **M** (wrong rule / right rule): LocalVarOutsideScope: wrong: A variable declared inside a block can be used anywhere in the program, like a global. \| right: A local variable's scope runs from its declaration to the end of the enclosing block.
- **M** (wrong rule / right rule): StatementAfterIfInBranch: wrong: A statement placed after the if statement belongs to its branch, so it runs only when the condition is true. \| right: The branch ends at its closing brace (or after its single statement); the next statement runs whatever the condition was.
- **M** (wrong rule / right rule): LoopBodyStatementOutsideLoop: wrong: Some statements inside the loop braces are not repeated; they run once, before or after the loop. \| right: Every statement inside the loop braces is part of the body and runs on every pass.
- **M** (wrong rule / right rule): StatementAfterLoopInBody: wrong: A statement written after the loop is repeated with the loop body. \| right: The body ends at the closing brace (or after its single statement); code after it runs once, after the loop ends.
- **T** (uneven-application rule): Applies the block rule (LT: all statements of the block in order, the whole block as one unit) unevenly: includes the statement after the closing brace in the body on one pass but not another, or runs only part of the body.
- **N** (identity rule): A block (statement block) is a sequence of statements enclosed in braces { }; it counts as one statement where a single statement is expected.
- **S** (declarative rule): A block is a sequence of statements and local variable declarations within braces; a variable declared in a block is in scope only from its declaration to the end of that block.
- **LT** (operational sequencing rule): A block executes each of its statements in order from first to last; if a statement completes abruptly, the rest of the block is skipped.
- **OP** (evaluation / result rule): A block has no value; its result is the combined effect of its statements, in order.
- **OS** (state-transition rule): Entering a block makes room for its local variables; leaving it (at the closing brace) ends their scope, so they can no longer be used.
- **R** (composition rule (with a neighbour)): with statement: A block is built from statements, each ended by ;, and is itself usable as a single statement (e.g. a loop body).
- **R** (composition rule (with a neighbour)): with program\_layout: Indentation should show block nesting, but only braces define it; layout that disagrees with the braces misleads the reader, not the compiler.
- **P** (plan / role rule): Purpose: group several statements so they act as one body (of main, an if branch or a loop) and limit the scope of variables to where they are needed.
- **C** (conservation rule): Adding braces around a single-statement body keeps behaviour; adding a second statement to a braceless body changes it (the new statement runs outside); moving a declaration into a block makes later uses outside the block fail to compile.
- **D** (error rule): rule broken: Every { must be matched by a } (compile-time)
- **D** (error rule): rule broken: Without braces only one statement is the body (silent logic error)
- **D** (error rule): rule broken: A local variable is visible only inside its block (compile-time)
- **X** (applicability rule): Use a block whenever a body has more than one statement (S&amp;W and TJ advise braces even for one), and declare variables in the innermost block that needs them.

## How it is found in code and answers (reader block)

- **Aliases:** block, curly braces, braces
- **Code patterns:** `\{`
- **Operator symbols:** none
- **Java types:** none

## The whole prerequisite chain

- **Everything it builds on (4):** `class_declaration`, `main_method`, `program_text`, `statement`
- **Everything that builds on it (1):** `program_layout`

## Every edge in this view and its exact edge logic (36)

All the edges drawn in the picture, in the order: prerequisite, parallel, misconception, error, has_level, contains.

**1. `block` &rarr; `program_layout`** (prerequisite)

- **Exact edge logic:** Indentation makes the nesting of blocks visible, so the reader can see which statements belong to which block.
- **Grounding:** book\_passage
- **Composition rule (R) of `block` with `program_layout`:** Indentation should show block nesting, but only braces define it; layout that disagrees with the braces misleads the reader, not the compiler.
- **Composition rule (R) of `program_layout` with `block`:** Indentation should show which statements belong to which block; braces, not indentation, decide it, so wrong indentation misleads.

**2. `statement` &rarr; `block`** (prerequisite)

- **Exact edge logic:** A statement block is a sequence of statements, each terminated by a semicolon, enclosed in braces; the body of main() is such a sequence.
- **Grounding:** book\_passage
- **Composition rule (R) of `statement` with `block`:** A block groups a sequence of statements in braces; the body of main() is such a block.
- **Composition rule (R) of `block` with `statement`:** A block is built from statements, each ended by ;, and is itself usable as a single statement (e.g. a loop body).

**3. `block` &rarr; `InconsistentIndentation`** (misconception)

- **Exact edge logic (the wrong rule):** Indents nested blocks inconsistently, so the visual nesting differs from the real nesting.
- **Twin logic (the right rule):** Indent consistently, one level deeper for each nested block, so the layout shows the real nesting; the compiler ignores indentation.
- **Role:** context

**4. `block` &rarr; `LocalVarOutsideScope`** (misconception)

- **Exact edge logic (the wrong rule):** A variable declared inside a block can be used anywhere in the program, like a global.
- **Twin logic (the right rule):** A local variable exists only from its declaration to the end of its block.
- **Role:** context

**5. `block` &rarr; `LoopBodyStatementOutsideLoop`** (misconception)

- **Exact edge logic (the wrong rule):** Some statements inside the braces of a loop body are not repeated; they run once, before or after the loop.
- **Twin logic (the right rule):** Every statement inside the loop braces is part of the body and runs on every pass.
- **Role:** context

**6. `block` &rarr; `MissingBraces`** (misconception)

- **Exact edge logic (the wrong rule):** Omits braces around a single-statement body of if, for or while.
- **Twin logic (the right rule):** Braces are optional for a single-statement body, but using them anyway avoids bugs when statements are added later.
- **Role:** context

**7. `block` &rarr; `StatementAfterIfInBranch`** (misconception)

- **Exact edge logic (the wrong rule):** A statement placed after the if statement belongs to its branch, so it runs only when the condition is true.
- **Twin logic (the right rule):** The branch ends at its closing brace (or after its single statement); the next statement runs whatever the condition was.
- **Role:** context

**8. `block` &rarr; `StatementAfterLoopInBody`** (misconception)

- **Exact edge logic (the wrong rule):** A statement written after the loop is repeated with the loop body.
- **Twin logic (the right rule):** The body ends at the closing brace (or after its single statement); code after it runs once, after the loop ends.
- **Role:** context

**9. `for_loop` &rarr; `MissingBraces`** (misconception)

- **Exact edge logic (the wrong rule):** Omits braces around a single-statement body of if, for or while.
- **Twin logic (the right rule):** Braces are optional for a single-statement body, but using them anyway avoids bugs when statements are added later.
- **Role:** context

**10. `if_statement` &rarr; `MissingBraces`** (misconception)

- **Exact edge logic (the wrong rule):** Omits braces around a single-statement body of if, for or while.
- **Twin logic (the right rule):** Braces are optional for a single-statement body, but using them anyway avoids bugs when statements are added later.
- **Role:** primary

**11. `if_statement` &rarr; `StatementAfterIfInBranch`** (misconception)

- **Exact edge logic (the wrong rule):** A statement placed after the if statement belongs to its branch, so it runs only when the condition is true.
- **Twin logic (the right rule):** The branch ends at its closing brace (or after its single statement); the next statement runs whatever the condition was.
- **Role:** primary

**12. `loop_body` &rarr; `LoopBodyStatementOutsideLoop`** (misconception)

- **Exact edge logic (the wrong rule):** Some statements inside the braces of a loop body are not repeated; they run once, before or after the loop.
- **Twin logic (the right rule):** Every statement inside the loop braces is part of the body and runs on every pass.
- **Role:** primary

**13. `loop_body` &rarr; `StatementAfterLoopInBody`** (misconception)

- **Exact edge logic (the wrong rule):** A statement written after the loop is repeated with the loop body.
- **Twin logic (the right rule):** The body ends at the closing brace (or after its single statement); code after it runs once, after the loop ends.
- **Role:** primary

**14. `loop_scope` &rarr; `LocalVarOutsideScope`** (misconception)

- **Exact edge logic (the wrong rule):** A variable declared inside a block can be used anywhere in the program, like a global.
- **Twin logic (the right rule):** A local variable exists only from its declaration to the end of its block.
- **Role:** primary

**15. `nested_conditionals` &rarr; `InconsistentIndentation`** (misconception)

- **Exact edge logic (the wrong rule):** Indents nested blocks inconsistently, so the visual nesting differs from the real nesting.
- **Twin logic (the right rule):** Indent consistently, one level deeper for each nested block, so the layout shows the real nesting; the compiler ignores indentation.
- **Role:** context

**16. `nested_loops` &rarr; `InconsistentIndentation`** (misconception)

- **Exact edge logic (the wrong rule):** Indents nested blocks inconsistently, so the visual nesting differs from the real nesting.
- **Twin logic (the right rule):** Indent consistently, one level deeper for each nested block, so the layout shows the real nesting; the compiler ignores indentation.
- **Role:** context

**17. `program_layout` &rarr; `InconsistentIndentation`** (misconception)

- **Exact edge logic (the wrong rule):** Indents nested blocks inconsistently, so the visual nesting differs from the real nesting.
- **Twin logic (the right rule):** Indent consistently, one level deeper for each nested block, so the layout shows the real nesting; the compiler ignores indentation.
- **Role:** primary

**18. `variable` &rarr; `LocalVarOutsideScope`** (misconception)

- **Exact edge logic (the wrong rule):** A variable declared inside a block can be used anywhere in the program, like a global.
- **Twin logic (the right rule):** A local variable exists only from its declaration to the end of its block.
- **Role:** context

**19. `while_loop` &rarr; `MissingBraces`** (misconception)

- **Exact edge logic (the wrong rule):** Omits braces around a single-statement body of if, for or while.
- **Twin logic (the right rule):** Braces are optional for a single-statement body, but using them anyway avoids bugs when statements are added later.
- **Role:** context

**20. `block` &rarr; `UnbalancedBraces`** (error)

- **Exact edge logic (the wrong rule):** A missing { or } is harmless.
- **Twin logic (the right rule):** Every { must be matched by a } so the class body and the method body are well formed.
- **Role:** primary

**21. `class_declaration` &rarr; `UnbalancedBraces`** (error)

- **Exact edge logic (the wrong rule):** A missing { or } is harmless.
- **Twin logic (the right rule):** Every { must be matched by a } so the class body and the method body are well formed.
- **Role:** context

**22. `compile_time_error` &rarr; `UnbalancedBraces`** (error)

- **Exact edge logic (the wrong rule):** A missing { or } is harmless.
- **Twin logic (the right rule):** Every { must be matched by a } so the class body and the method body are well formed.
- **Role:** context

**23. `block` &rarr; `block@L0`** (has_level)

- **Exact edge logic:** block -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (6 ways).
  - **[0] everyday\_reading** (rule type E, folk-meaning rule): Everyday/visual reading: indentation or line position tells you what belongs together, as in an outline. Java rule: only braces delimit a block; indentation is ignored, and without braces an if or loop body is just the next single statement.
  - **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `LocalVarOutsideScope`: wrong rule: A variable declared inside a block can be used anywhere in the program, like a global. Right rule: A local variable's scope runs from its declaration to the end of the enclosing block.
  - **[2] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `LocalVarOutsideScope`: Applies the block rule (LT: all statements of the block in order, the whole block as one unit) unevenly: includes the statement after the closing brace in the body on one pass but not another, or runs only part of the body. (here mixing in: "A variable declared inside a block can be used anywhere in the program, like a global")
  - **[3] misconception** (rule type M, wrong rule / right rule) &rarr; `StatementAfterIfInBranch`: wrong rule: A statement placed after the if statement belongs to its branch, so it runs only when the condition is true. Right rule: The branch ends at its closing brace (or after its single statement); the next statement runs whatever the condition was.
  - **[4] misconception** (rule type M, wrong rule / right rule) &rarr; `LoopBodyStatementOutsideLoop`: wrong rule: Some statements inside the loop braces are not repeated; they run once, before or after the loop. Right rule: Every statement inside the loop braces is part of the body and runs on every pass.
  - **[5] misconception** (rule type M, wrong rule / right rule) &rarr; `StatementAfterLoopInBody`: wrong rule: A statement written after the loop is repeated with the loop body. Right rule: The body ends at the closing brace (or after its single statement); code after it runs once, after the loop ends.

**24. `block` &rarr; `block@L1`** (has_level)

- **Exact edge logic:** block -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).
  - **[0] names\_the\_element** (rule type N, identity rule): A block (statement block) is a sequence of statements enclosed in braces { }; it counts as one statement where a single statement is expected.
  - **[1] states\_the\_rule** (rule type S, declarative rule): A block is a sequence of statements and local variable declarations within braces; a variable declared in a block is in scope only from its declaration to the end of that block.

**25. `block` &rarr; `block@L2`** (has_level)

- **Exact edge logic:** block -&gt; L2 (Multistructural): the answer applies the rules of block to every part of the code, in order (3 ways).
  - **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): A block executes each of its statements in order from first to last; if a statement completes abruptly, the rest of the block is skipped.
  - **[1] output\_prediction** (rule type OP, evaluation / result rule): A block has no value; its result is the combined effect of its statements, in order.
  - **[2] one\_step\_execution** (rule type OS, state-transition rule): Entering a block makes room for its local variables; leaving it (at the closing brace) ends their scope, so they can no longer be used.

**26. `block` &rarr; `block@L3`** (has_level)

- **Exact edge logic:** block -&gt; L3 (Relational): the answer relates the parts (3 ways).
  - **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): A block is built from statements, each ended by ;, and is itself usable as a single statement (e.g. a loop body).
  - **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Indentation should show block nesting, but only braces define it; layout that disagrees with the braces misleads the reader, not the compiler.
  - **[2] purpose\_of\_the\_whole** (rule type P, plan / role rule): Purpose: group several statements so they act as one body (of main, an if branch or a loop) and limit the scope of variables to where they are needed.

**27. `block` &rarr; `block@L4`** (has_level)

- **Exact edge logic:** block -&gt; L4 (Extended abstract): the answer reasons beyond the given code (5 ways).
  - **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `LocalVarOutsideScope`: Adding braces around a single-statement body keeps behaviour; adding a second statement to a braceless body changes it (the new statement runs outside); moving a declaration into a block makes later uses outside the block fail to compile.
  - **[1] diagnose\_an\_error** (rule type D, error rule): rule broken: Every { must be matched by a }. Kind: compile-time. Trigger class: a missing or extra brace: javac reports '{' expected, 'class' or 'interface' expected, or reached end of file while parsing, often on a later line
  - **[2] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Use a block whenever a body has more than one statement (S&amp;W and TJ advise braces even for one), and declare variables in the innermost block that needs them.
  - **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: Without braces only one statement is the body. Kind: silent logic error. Trigger class: a multi-statement body written without braces, indented as if all were inside
  - **[4] diagnose\_an\_error** (rule type D, error rule): rule broken: A local variable is visible only inside its block. Kind: compile-time. Trigger class: using a variable after the block that declared it has closed (cannot find symbol)

**28. `topic1.1.b` &rarr; `block`** (contains)

- topic `topic1.1.b` contains `block`

**29. `topic1.1.b` &rarr; `class_declaration`** (contains)

- topic `topic1.1.b` contains `class_declaration`

**30. `topic1.1.b` &rarr; `comment`** (contains)

- topic `topic1.1.b` contains `comment`

**31. `topic1.1.b` &rarr; `main_method`** (contains)

- topic `topic1.1.b` contains `main_method`

**32. `topic1.1.b` &rarr; `print`** (contains)

- topic `topic1.1.b` contains `print`

**33. `topic1.1.b` &rarr; `println`** (contains)

- topic `topic1.1.b` contains `println`

**34. `topic1.1.b` &rarr; `program_layout`** (contains)

- topic `topic1.1.b` contains `program_layout`

**35. `topic1.1.b` &rarr; `statement`** (contains)

- topic `topic1.1.b` contains `statement`

**36. `topic1.1.b` &rarr; `string_literal`** (contains)

- topic `topic1.1.b` contains `string_literal`
