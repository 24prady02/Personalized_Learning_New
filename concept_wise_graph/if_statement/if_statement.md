# if_statement (`if_statement`)

run a block only when the condition holds

Section 1.3 Conditionals and Loops, topic 1.3.b If statements.

![The knowledge graph around if_statement](if_statement.png)

## At a glance

- **Needs first:** `boolean_expression`, `control_flow`
- **Leads to:** `if_else_statement`, `nested_conditionals`
- **Learned alongside:** `while_loop`
- **Misconceptions:** `AssignCompares`, `BranchChosenByIntent`, `CodeAfterIfSkipped`, `FalseConditionEndsProgram`, `FalseConditionRestartsProgram`, `IfConditionCheckedInHindsight`, `IfConditionWatched`, `IfInLoopUnchecked`, `IfIsLoop`, `IfRequiresElse`, `IfWaitsForCondition`, `LoopForOneTimeTest`, `MapToBooleanWithIf`, `MissingBraces`, `NextStatementIsElse`, `ProgramLooksAhead`, `SequentialIfsAreNested`, `StatementAfterIfInBranch`, `ThenAlwaysExecutes`
- **Errors:** `BracelessMultiStatementBody`, `CurlyIfCondition`, `SemicolonAfterIfHeader`
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 62 edges around this concept, each explained in the graph's own words.

## What it needs first (2)

A prerequisite edge means the other concept has to be understood before `if_statement`.

### `boolean_expression` comes before `if_statement`

*an expression that evaluates to true/false*

An if runs its block only when its boolean expression evaluates to true.

- **Grounding:** book passage
- **How `if_statement` combines with `boolean_expression`:** The condition must be a boolean expression; a non-boolean condition such as if (t = goal) with int t is a compile-time error, while if (b = false) with boolean b compiles and assigns.
- **How `boolean_expression` combines with `if_statement`:** The if statement evaluates its boolean expression once and runs its block only when the value is true; the expression must have type boolean, so if (x = 5) with int x does not compile.

### `control_flow` comes before `if_statement`

*the order in which statements are executed*

An if changes the default top-to-bottom flow by running a block only when its condition is true.

- **Grounding:** book passage
- **How `if_statement` combines with `control_flow`:** An if is a fork in the control flow: one path through the body, one around it, both rejoining at the next statement.
- **How `control_flow` combines with `if_statement`:** An if changes the default top-to-bottom flow: its condition is tested once when control reaches it, its block runs only if true, and in both cases control then continues with the next statement.

## What it leads to (2)

These concepts need `if_statement` first.

### `if_statement` comes before `if_else_statement`

*choose one of two blocks*

if-else extends if with a second block that runs exactly when the condition is false.

- **Grounding:** book passage
- **How `if_statement` combines with `if_else_statement`:** if-else extends if with a second branch that runs exactly when the condition is false; a lone if has an implicit empty else-case.
- **How `if_else_statement` combines with `if_statement`:** if-else is an if with a second branch for the false case; dropping the else gives a plain if in which the false case does nothing.

### `if_statement` comes before `nested_conditionals`

*else-if chains and conditionals inside conditionals*

An if statement can sit inside the body of another if; the inner one is tested only when the outer condition is true.

- **Grounding:** book passage

## Learned alongside (1)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

### `if_statement` alongside `while_loop`

*repeat a block while a condition holds*

if and while have the same form, but if tests its condition once and runs the block at most once, while while tests again after every pass and repeats the block as long as the condition is true.

- **Grounding:** book passage

## Misconceptions (19)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### AssignCompares

- **Wrong rule:** = compares two values instead of assigning
- **Right rule:** x = y copies the value of y into x; x == y is what compares them.
- **Role of this concept:** context
- **Shows at level L0 as:** misconception: wrong rule: = compares two values instead of assigning. Right rule: x = y copies the value of y into x; x == y is what compares them.
- **Also an edge from `assignment`:** x = y checks whether x and y are equal.
- **Also an edge from `comparison_operators`:** = compares two values instead of assigning

### BranchChosenByIntent

- **Wrong rule:** Which branch runs is decided by what the programmer meant or by code outside the if, not by whether the condition is true.
- **Right rule:** The then branch runs exactly when the condition evaluates to true at the moment it is tested; otherwise the else branch (if any) runs.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: Which branch runs is decided by what the programmer meant or by code outside the if, not by whether the condition is true. Right rule: The then branch runs exactly when the condition evaluates to true at the moment it is tested; otherwise the else branch (if any) runs.
- **Also an edge from `if_else_statement`:** Which branch runs is decided by what the programmer meant or by code outside the if, not by whether the condition is true.

### CodeAfterIfSkipped

- **Wrong rule:** When the then branch runs, the code after the if is skipped.
- **Right rule:** After the if finishes, execution continues with the next statement either way.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: When the then branch runs, the code after the if is skipped. Right rule: After the if finishes, execution continues with the next statement either way.
- **Also an edge from `control_flow`:** When the then branch runs, the code after the if is skipped.

### FalseConditionEndsProgram

- **Wrong rule:** A false condition with no else ends the program.
- **Right rule:** When an if condition is false and there is no else, execution continues with the statement after the if.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: A false condition with no else ends the program. Right rule: When an if condition is false and there is no else, execution continues with the statement after the if.

### FalseConditionRestartsProgram

- **Wrong rule:** When an if condition is false (and there is no else), control jumps back to the start of the program.
- **Right rule:** A false condition skips the then branch and execution continues with the statement after the if statement.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: When an if condition is false (and there is no else), control jumps back to the start of the program. Right rule: A false condition skips the then branch and execution continues with the statement after the if statement.
- **Also an edge from `control_flow`:** When an if condition is false (and there is no else), control jumps back to the start of the program.

### IfConditionCheckedInHindsight

- **Wrong rule:** Whether the branch runs is decided by the condition after the branch, or from the point inside the body where the condition becomes true.
- **Right rule:** The condition is tested once, before the branch; the whole branch runs if it was true at that moment and none of it runs otherwise.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: Whether the branch runs is decided by the condition after the branch, or from the point inside the body where the condition becomes true. Right rule: The condition is tested once, before the branch; the whole branch runs if it was true at that moment and none of it runs otherwise.

### IfConditionWatched

- **Wrong rule:** An if statement watches its condition while the program runs and fires as soon as the condition becomes true (if = whenever).
- **Right rule:** An if condition is tested once, when control reaches the if statement; later changes to the variables do not trigger the branch.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: An if statement watches its condition while the program runs and fires as soon as the condition becomes true (if = whenever). Right rule: An if condition is tested once, when control reaches the if statement; later changes to the variables do not trigger the branch.
- **Also an edge from `control_flow`:** An if statement watches its condition while the program runs and fires as soon as the condition becomes true (if = whenever).

### IfInLoopUnchecked

- **Wrong rule:** An if inside a loop body runs its branch on every pass without testing its condition.
- **Right rule:** The if condition is tested again on every pass, with the current values, so the branch runs only on passes where it is true.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: An if inside a loop body runs its branch on every pass without testing its condition. Right rule: The if condition is tested again on every pass, with the current values, so the branch runs only on passes where it is true.
- **Also an edge from `loop_body`:** An if inside a loop body runs its branch on every pass without testing its condition.

### IfIsLoop

- **Wrong rule:** The if body keeps repeating as long as its condition stays true.
- **Right rule:** An if body runs at most once; only a loop repeats its body.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: an if body repeats while its condition holds. Right rule: An if body runs at most once; only a loop repeats its body.
- **Shows at level L0 as:** inconsistent trace: Applies the if rule (LT) unevenly: tests the condition on some visits but not others (e.g. runs the branch on every loop pass without testing), runs the branch after a false test, or re-checks the condition after the branch has run. (here mixing in: "an if body repeats while its condition holds")
- **Also an edge from `while_loop`:** A while loop runs its body once when the condition is true, just like an if.

### IfRequiresElse

- **Wrong rule:** Every if statement requires an else.
- **Right rule:** An if statement may stand alone; the else part is optional.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: Every if statement requires an else. Right rule: An if statement may stand alone; the else part is optional.

### IfWaitsForCondition

- **Wrong rule:** An IF statement earlier in the program stays active and fires later, e.g. inside a later loop, when its condition becomes true.
- **Right rule:** An if is evaluated once when control reaches it; afterwards it is inactive unless control returns to it.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: An IF statement earlier in the program stays active and fires later, e.g. inside a later loop, when its condition becomes true. Right rule: An if is evaluated once when control reaches it; afterwards it is inactive unless control returns to it.
- **Also an edge from `control_flow`:** An IF statement earlier in the program stays active and fires later, e.g. inside a later loop, when its condition becomes true.

### LoopForOneTimeTest

- **Wrong rule:** Uses a loop where a condition needs to be tested only once.
- **Right rule:** A test made once is an if; a loop repeats.
- **Role of this concept:** context
- **Shows at level L0 as:** misconception: wrong rule: Uses a loop where a condition needs to be tested only once. Right rule: A test made once is an if; a loop repeats.
- **Also an edge from `boolean_expression`:** Uses a loop where a condition needs to be tested only once.
- **Also an edge from `while_loop`:** Uses a loop where a condition needs to be tested only once.

### MapToBooleanWithIf

- **Wrong rule:** you need an if to turn a boolean expression into a boolean
- **Right rule:** ok = (x &gt; y); stores the result of the comparison directly.
- **Role of this concept:** context
- **Shows at level L0 as:** misconception: wrong rule: you need an if to turn a boolean expression into a boolean. Right rule: ok = (x &gt; y); stores the result of the comparison directly.
- **Also an edge from `boolean_expression`:** To store whether x &gt; y in a boolean you need if (x &gt; y) ok = true; else ok = false;.

### MissingBraces

- **Wrong rule:** Omits braces around a single-statement body of if, for or while.
- **Right rule:** Braces are optional for a single-statement body, but using them anyway avoids bugs when statements are added later.
- **Role of this concept:** primary
- **Also an edge from `block`:** Omits braces around a single-statement body of if, for or while.
- **Also an edge from `for_loop`:** Omits braces around a single-statement body of if, for or while.
- **Also an edge from `while_loop`:** Omits braces around a single-statement body of if, for or while.

### NextStatementIsElse

- **Wrong rule:** In if (c) A; B; the statement B runs only when c is false.
- **Right rule:** B is not part of the if; it runs every time.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: In if (c) A; B; the statement B runs only when c is false. Right rule: B is not part of the if; it runs every time.

### ProgramLooksAhead

- **Wrong rule:** The program knows or sees what later lines will do and acts on those goals at the current line, e.g. it stops 'at ten' because it wants to draw a box.
- **Right rule:** Each statement executes using only the current state; later lines have no effect until control reaches them.
- **Role of this concept:** context
- **Shows at level L0 as:** misconception: wrong rule: The program knows or sees what later lines will do and acts on those goals at the current line, e.g. it stops 'at ten' because it wants to draw a box. Right rule: Each statement executes using only the current state; later lines have no effect until control reaches them.
- **Also an edge from `control_flow`:** The program knows or sees what later lines will do and acts on those goals at the current line, e.g. it stops 'at ten' because it wants to draw a box.
- **Also an edge from `statement`:** The program knows or sees what later lines will do and acts on those goals at the current line, e.g. it stops 'at ten' because it wants to draw a box.

### SequentialIfsAreNested

- **Wrong rule:** Of two if statements one after the other, the second runs its body only if both conditions are true.
- **Right rule:** Two ifs in sequence are independent: each tests only its own condition.
- **Role of this concept:** context
- **Shows at level L0 as:** misconception: wrong rule: Of two if statements one after the other, the second runs its body only if both conditions are true. Right rule: Two ifs in sequence are independent: each tests only its own condition.
- **Also an edge from `nested_conditionals`:** Of two if statements one after the other, the second runs its body only if both conditions are true.

### StatementAfterIfInBranch

- **Wrong rule:** A statement placed after the if statement belongs to its branch, so it runs only when the condition is true.
- **Right rule:** The branch ends at its closing brace (or after its single statement); the next statement runs whatever the condition was.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: A statement placed after the if statement belongs to its branch, so it runs only when the condition is true. Right rule: The branch ends at its closing brace (or after its single statement); the next statement runs whatever the condition was.
- **Also an edge from `block`:** A statement placed after the if statement belongs to its branch, so it runs only when the condition is true.

### ThenAlwaysExecutes

- **Wrong rule:** The then branch always runs.
- **Right rule:** The then branch runs only when the condition is true.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: The then branch always runs. Right rule: The then branch runs only when the condition is true.

## Errors (3)

An error edge states the rule that gets broken in a program, and the right rule.

### BracelessMultiStatementBody

- **Wrong rule:** Indenting several statements under an if or for makes them all part of its body, even without braces.
- **Right rule:** Without braces only the first statement belongs to the if/for; the rest run once, after it.
- **Role of this concept:** context
- **Also an edge from `for_loop`:** Indenting several statements under an if or for makes them all part of its body, even without braces.
- **Also an edge from `loop_body`:** Indenting several statements under an if or for makes them all part of its body, even without braces.
- **Also an edge from `nested_loops`:** Indenting several statements under an if or for makes them all part of its body, even without braces.

### CurlyIfCondition

- **Wrong rule:** Writes the if condition inside { } instead of ( ).
- **Right rule:** The condition of an if is written in parentheses.
- **Role of this concept:** primary

### SemicolonAfterIfHeader

- **Wrong rule:** if (x &gt; 0); System.out.println("positive"); prints only for positive x.
- **Right rule:** The ; ends the if with an empty statement, so the next line always runs.
- **Role of this concept:** primary
- **Also an edge from `empty_statement`:** if (x &gt; 0); System.out.println("positive"); prints only for positive x.
- **Also an edge from `for_loop`:** if (x &gt; 0); System.out.println("positive"); prints only for positive x.
- **Also an edge from `logical_error`:** if (x &gt; 0); System.out.println("positive"); prints only for positive x.
- **Also an edge from `while_loop`:** if (x &gt; 0); System.out.println("positive"); prints only for positive x.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for if statement: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to if statement agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

if statement -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (20 ways).

- **everyday reading** (folk-meaning rule): Folk meaning: English 'if' (and 'whenever') states a standing rule that stays in force and fires whenever its condition becomes true. A Java if is evaluated once, when control reaches it, and then is 'taken off the books'; changing the variables later does not re-trigger it.
- **misconception** (wrong rule / right rule; shows `IfIsLoop`): wrong rule: an if body repeats while its condition holds. Right rule: An if body runs at most once; only a loop repeats its body.
- **misconception** (wrong rule / right rule; shows `IfRequiresElse`): wrong rule: Every if statement requires an else. Right rule: An if statement may stand alone; the else part is optional.
- **misconception** (wrong rule / right rule; shows `FalseConditionEndsProgram`): wrong rule: A false condition with no else ends the program. Right rule: When an if condition is false and there is no else, execution continues with the statement after the if.
- **misconception** (wrong rule / right rule; shows `ThenAlwaysExecutes`): wrong rule: The then branch always runs. Right rule: The then branch runs only when the condition is true.
- **misconception** (wrong rule / right rule; shows `CodeAfterIfSkipped`): wrong rule: When the then branch runs, the code after the if is skipped. Right rule: After the if finishes, execution continues with the next statement either way.
- **misconception** (wrong rule / right rule; shows `NextStatementIsElse`): wrong rule: In if (c) A; B; the statement B runs only when c is false. Right rule: B is not part of the if; it runs every time.
- **misconception** (wrong rule / right rule; shows `IfWaitsForCondition`): wrong rule: An IF statement earlier in the program stays active and fires later, e.g. inside a later loop, when its condition becomes true. Right rule: An if is evaluated once when control reaches it; afterwards it is inactive unless control returns to it.
- **misconception** (wrong rule / right rule; shows `BranchChosenByIntent`): wrong rule: Which branch runs is decided by what the programmer meant or by code outside the if, not by whether the condition is true. Right rule: The then branch runs exactly when the condition evaluates to true at the moment it is tested; otherwise the else branch (if any) runs.
- **misconception** (wrong rule / right rule; shows `StatementAfterIfInBranch`): wrong rule: A statement placed after the if statement belongs to its branch, so it runs only when the condition is true. Right rule: The branch ends at its closing brace (or after its single statement); the next statement runs whatever the condition was.
- **misconception** (wrong rule / right rule; shows `FalseConditionRestartsProgram`): wrong rule: When an if condition is false (and there is no else), control jumps back to the start of the program. Right rule: A false condition skips the then branch and execution continues with the statement after the if statement.
- **misconception** (wrong rule / right rule; shows `IfConditionWatched`): wrong rule: An if statement watches its condition while the program runs and fires as soon as the condition becomes true (if = whenever). Right rule: An if condition is tested once, when control reaches the if statement; later changes to the variables do not trigger the branch.
- **misconception** (wrong rule / right rule; shows `IfConditionCheckedInHindsight`): wrong rule: Whether the branch runs is decided by the condition after the branch, or from the point inside the body where the condition becomes true. Right rule: The condition is tested once, before the branch; the whole branch runs if it was true at that moment and none of it runs otherwise.
- **misconception** (wrong rule / right rule; shows `IfInLoopUnchecked`): wrong rule: An if inside a loop body runs its branch on every pass without testing its condition. Right rule: The if condition is tested again on every pass, with the current values, so the branch runs only on passes where it is true.
- **inconsistent trace** (uneven-application rule; shows `IfIsLoop`): Applies the if rule (LT) unevenly: tests the condition on some visits but not others (e.g. runs the branch on every loop pass without testing), runs the branch after a false test, or re-checks the condition after the branch has run. (here mixing in: "an if body repeats while its condition holds")
- **misconception** (wrong rule / right rule; shows `AssignCompares`): wrong rule: = compares two values instead of assigning. Right rule: x = y copies the value of y into x; x == y is what compares them.
- **misconception** (wrong rule / right rule; shows `LoopForOneTimeTest`): wrong rule: Uses a loop where a condition needs to be tested only once. Right rule: A test made once is an if; a loop repeats.
- **misconception** (wrong rule / right rule; shows `MapToBooleanWithIf`): wrong rule: you need an if to turn a boolean expression into a boolean. Right rule: ok = (x &gt; y); stores the result of the comparison directly.
- **misconception** (wrong rule / right rule; shows `ProgramLooksAhead`): wrong rule: The program knows or sees what later lines will do and acts on those goals at the current line, e.g. it stops 'at ten' because it wants to draw a box. Right rule: Each statement executes using only the current state; later lines have no effect until control reaches them.
- **misconception** (wrong rule / right rule; shows `SequentialIfsAreNested`): wrong rule: Of two if statements one after the other, the second runs its body only if both conditions are true. Right rule: Two ifs in sequence are independent: each tests only its own condition.

### L1: Unistructural / atom x text surface

L1 for if statement: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

if statement -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

- **names the element** (identity rule): The if statement is a conditional (selection) statement: it runs a statement or block only when a boolean condition is true.
- **states the rule** (declarative rule): Syntax: if (&lt;boolean expression&gt;) &lt;statement or { block }&gt;; the braces are optional when the body is a single statement. The expression must have type boolean (or Boolean), and the body is executed if and only if the expression is true.

### L2: Multistructural / block x execution / preoperational

L2 for if statement: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

if statement -&gt; L2 (Multistructural): the answer applies the rules of if statement to every part of the code, in order (3 ways).

- **line by line trace** (operational sequencing rule): Evaluate the condition once; if true, execute the body; then, in either case, continue with the statement after the if.
- **output prediction** (evaluation / result rule): An if produces no value; its observable result is that the body's effects (assignments, output) happen exactly once when the condition is true and not at all when it is false; e.g. if (x &lt; 0) x = -x; leaves x = 5 for 5 and gives 5 for -5.
- **one step execution** (state-transition rule): One execution reads the variables in the condition, changes nothing by the test itself (unless the condition has a side effect), and, when true, applies the body's changes once; control then moves to the next statement.

### L3: Relational / relations x function (concrete operational begins)

L3 for if statement: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

if statement -&gt; L3 (Relational): the answer relates the parts (5 ways).

- **relation to neighbour** (composition rule (with a neighbour)): The condition must be a boolean expression; a non-boolean condition such as if (t = goal) with int t is a compile-time error, while if (b = false) with boolean b compiles and assigns.
- **relation to neighbour** (composition rule (with a neighbour)): if-else extends if with a second branch that runs exactly when the condition is false; a lone if has an implicit empty else-case.
- **relation to neighbour** (composition rule (with a neighbour)): An if is a fork in the control flow: one path through the body, one around it, both rejoining at the next statement.
- **relation to neighbour** (composition rule (with a neighbour)): if and while have the same form, but if tests its condition once and runs the block at most once, while while tests again after every pass and repeats the block as long as the condition is true.
- **purpose of the whole** (plan / role rule): Plan: guard / conditional action - do something only for the inputs that need it (absolute value, put two values in order, error check before dividing).

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for if statement: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

if statement -&gt; L4 (Extended abstract): the answer reasons beyond the given code (7 ways).

- **predict a change** (conservation rule; shows `IfIsLoop`): Negating the condition swaps which inputs run the body; changing &lt; to &lt;= changes only the boundary value. Adding a statement under a braceless if does not put it in the body. Whatever the condition, code after the if still runs exactly once.
- **diagnose an error** (error rule): rule broken: A ; right after if (...) is an empty statement that forms the whole then branch; the following statement or block is no longer part of the if. Kind: silent logic error. Trigger class: Any if (cond); followed by a statement or block: that statement runs for every input, whatever cond is (it compiles without error).
- **diagnose an error** (error rule): rule broken: The if template is if (&lt;boolean expression&gt;) &lt;statement&gt;: the condition must be enclosed in parentheses. Kind: compile-time. Trigger class: Any if whose condition is written in { } or without ( ), e.g. if {x &gt; 0} ... or if a &gt; b { c = 0; }.
- **transfer to a new program** (applicability rule): Use an if when an action is needed for some inputs only and the test happens once at that point; use a loop if the action must repeat while the condition holds, and assign a boolean directly (ok = x &gt; y;) when you only need the truth value.
- **diagnose an error** (error rule): rule broken: Without braces, the body of an if, while or for is exactly one statement; indentation does not add statements to it. Kind: silent logic error. Trigger class: A braceless header followed by two or more indented statements: only the first is controlled, the others run once, after the if/loop, on every input.
- **diagnose an error** (error rule): rule broken: The condition of an if must have type boolean. Kind: compile-time. Trigger class: Using = instead of == with int operands, e.g. if (t = goal): 'incompatible types: int cannot be converted to boolean'.
- **diagnose an error** (error rule): rule broken: With boolean operands, = is assignment, not comparison. Kind: silent logic error. Trigger class: if (isPrime = false) with boolean isPrime: compiles, sets isPrime to false and the branch never runs.

## Same topic

`if_statement` belongs to the topic **If statements** (`topic1.3.b`). The topic also contains: `empty_statement`, `if_else_statement`, `syntax_template`.

## Rules of the concept (36)

- **folk-meaning rule:** Folk meaning: English 'if' (and 'whenever') states a standing rule that stays in force and fires whenever its condition becomes true. A Java if is evaluated once, when control reaches it, and then is 'taken off the books'; changing the variables later does not re-trigger it.
- **wrong rule / right rule:** AssignCompares: wrong: = compares two values instead of assigning \| right: x = y copies the value of y into x; x == y is what compares them.
- **wrong rule / right rule:** CodeAfterIfSkipped: wrong: When the then branch runs, the code after the if is skipped. \| right: After the if finishes, execution continues with the next statement either way.
- **wrong rule / right rule:** FalseConditionEndsProgram: wrong: A false condition with no else ends the program. \| right: When an if condition is false and there is no else, execution continues with the statement after the if.
- **wrong rule / right rule:** IfIsLoop: wrong: an if body repeats while its condition holds \| right: An if body runs at most once; only a loop repeats its body.
- **wrong rule / right rule:** IfRequiresElse: wrong: Every if statement requires an else. \| right: An if statement may stand alone; the else part is optional.
- **wrong rule / right rule:** LoopForOneTimeTest: wrong: Uses a loop where a condition needs to be tested only once. \| right: A test made once is an if; a loop repeats.
- **wrong rule / right rule:** MapToBooleanWithIf: wrong: you need an if to turn a boolean expression into a boolean \| right: ok = (x &gt; y); stores the result of the comparison directly.
- **wrong rule / right rule:** NextStatementIsElse: wrong: In if (c) A; B; the statement B runs only when c is false. \| right: B is not part of the if; it runs every time.
- **wrong rule / right rule:** ThenAlwaysExecutes: wrong: The then branch always runs. \| right: The then branch runs only when the condition is true.
- **wrong rule / right rule:** IfWaitsForCondition: wrong: An IF statement earlier in the program stays active and fires later, e.g. inside a later loop, when its condition becomes true. \| right: An if is evaluated once when control reaches it; afterwards it is inactive unless control returns to it.
- **wrong rule / right rule:** ProgramLooksAhead: wrong: The program knows or sees what later lines will do and acts on those goals at the current line, e.g. it stops 'at ten' because it wants to draw a box. \| right: Each statement executes using only the current state; later lines have no effect until control reaches them.
- **wrong rule / right rule:** BranchChosenByIntent: wrong: Which branch runs is decided by what the programmer meant or by code outside the if, not by whether the condition is true. \| right: The then branch runs exactly when the condition evaluates to true at the moment it is tested; otherwise the else branch (if any) runs.
- **wrong rule / right rule:** StatementAfterIfInBranch: wrong: A statement placed after the if statement belongs to its branch, so it runs only when the condition is true. \| right: The branch ends at its closing brace (or after its single statement); the next statement runs whatever the condition was.
- **wrong rule / right rule:** FalseConditionRestartsProgram: wrong: When an if condition is false (and there is no else), control jumps back to the start of the program. \| right: A false condition skips the then branch and execution continues with the statement after the if statement.
- **wrong rule / right rule:** IfConditionWatched: wrong: An if statement watches its condition while the program runs and fires as soon as the condition becomes true (if = whenever). \| right: An if condition is tested once, when control reaches the if statement; later changes to the variables do not trigger the branch.
- **wrong rule / right rule:** IfConditionCheckedInHindsight: wrong: Whether the branch runs is decided by the condition after the branch, or from the point inside the body where the condition becomes true. \| right: The condition is tested once, before the branch; the whole branch runs if it was true at that moment and none of it runs otherwise.
- **wrong rule / right rule:** SequentialIfsAreNested: wrong: Of two if statements one after the other, the second runs its body only if both conditions are true. \| right: Two ifs in sequence are independent: each tests only its own condition.
- **wrong rule / right rule:** IfInLoopUnchecked: wrong: An if inside a loop body runs its branch on every pass without testing its condition. \| right: The if condition is tested again on every pass, with the current values, so the branch runs only on passes where it is true.
- **uneven-application rule:** Applies the if rule (LT) unevenly: tests the condition on some visits but not others (e.g. runs the branch on every loop pass without testing), runs the branch after a false test, or re-checks the condition after the branch has run.
- **identity rule:** The if statement is a conditional (selection) statement: it runs a statement or block only when a boolean condition is true.
- **declarative rule:** Syntax: if (&lt;boolean expression&gt;) &lt;statement or { block }&gt;; the braces are optional when the body is a single statement. The expression must have type boolean (or Boolean), and the body is executed if and only if the expression is true.
- **operational sequencing rule:** Evaluate the condition once; if true, execute the body; then, in either case, continue with the statement after the if.
- **evaluation / result rule:** An if produces no value; its observable result is that the body's effects (assignments, output) happen exactly once when the condition is true and not at all when it is false; e.g. if (x &lt; 0) x = -x; leaves x = 5 for 5 and gives 5 for -5.
- **state-transition rule:** One execution reads the variables in the condition, changes nothing by the test itself (unless the condition has a side effect), and, when true, applies the body's changes once; control then moves to the next statement.
- **composition rule (with a neighbour):** with boolean\_expression: The condition must be a boolean expression; a non-boolean condition such as if (t = goal) with int t is a compile-time error, while if (b = false) with boolean b compiles and assigns.
- **composition rule (with a neighbour):** with if\_else\_statement: if-else extends if with a second branch that runs exactly when the condition is false; a lone if has an implicit empty else-case.
- **composition rule (with a neighbour):** with control\_flow: An if is a fork in the control flow: one path through the body, one around it, both rejoining at the next statement.
- **plan / role rule:** Plan: guard / conditional action - do something only for the inputs that need it (absolute value, put two values in order, error check before dividing).
- **conservation rule:** Negating the condition swaps which inputs run the body; changing &lt; to &lt;= changes only the boundary value. Adding a statement under a braceless if does not put it in the body. Whatever the condition, code after the if still runs exactly once.
- **error rule:** rule broken: The if template is if (&lt;boolean expression&gt;) &lt;statement&gt;: the condition must be enclosed in parentheses. (compile-time)
- **error rule:** rule broken: A ; right after if (...) is an empty statement that forms the whole then branch; the following statement or block is no longer part of the if. (silent logic error)
- **error rule:** rule broken: Without braces, the body of an if, while or for is exactly one statement; indentation does not add statements to it. (silent logic error)
- **error rule:** rule broken: The condition of an if must have type boolean. (compile-time)
- **error rule:** rule broken: With boolean operands, = is assignment, not comparison. (silent logic error)
- **applicability rule:** Use an if when an action is needed for some inputs only and the test happens once at that point; use a loop if the action must repeat while the condition holds, and assign a boolean directly (ok = x &gt; y;) when you only need the truth value.

## The whole prerequisite chain

- **Everything it builds on (16):** `arithmetic_operators`, `boolean`, `boolean_expression`, `class_declaration`, `comparison_operators`, `control_flow`, `data_type`, `expression`, `identifier`, `literal`, `logical_operators`, `main_method`, `primitive_type`, `program_text`, `statement`, `variable`
- **Everything that builds on it (5):** `conditional_operator`, `dangling_else`, `else_if_chain`, `if_else_statement`, `nested_conditionals`
