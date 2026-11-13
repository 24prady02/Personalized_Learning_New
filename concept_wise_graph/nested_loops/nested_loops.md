# nested_loops (`nested_loops`)

a loop inside a loop

Section 1.3 Conditionals and Loops, topic 1.3.e Nesting.

![The knowledge graph around nested_loops](nested_loops.png)

## At a glance

- **Needs first:** `for_loop`
- **Leads to:** `labeled_break`, `matrix_operations`, `row_major_order`
- **Learned alongside:** nothing
- **Misconceptions:** `EmptyInnerLoopSkipsRest`, `InconsistentIndentation`, `InnerCounterOverwritesOuter`, `InnerOuterSwapped`, `NestedLoopsLockstep`, `NestedLoopsSequential`, `OuterLoopIgnored`
- **Errors:** `BracelessMultiStatementBody`
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 27 edges around this concept, each explained in the graph's own words.

## What it needs first (1)

A prerequisite edge means the other concept has to be understood before `nested_loops`.

### `for_loop` comes before `nested_loops`

*a while with init/condition/update packaged together*

In nested loops the inner for runs its complete set of passes for every single pass of the outer for.

- **Grounding:** book passage
- **How `nested_loops` combines with `for_loop`:** Usually both loops are for loops: the inner for runs its complete set of passes for every single pass of the outer for.
- **How `for_loop` combines with `nested_loops`:** A for may be the body of another for: the inner for runs its complete set of passes for every single pass of the outer one.

## What it leads to (3)

These concepts need `nested_loops` first.

### `nested_loops` comes before `labeled_break`

*labeled break/continue exit or continue an outer loop*

A labeled break is needed only when a loop is nested inside another and the inner loop must end the outer one.

- **Grounding:** questionable
- **How `nested_loops` combines with `labeled_break`:** A plain break ends only the innermost loop; a labeled break is needed when the inner loop must end the outer one too.
- **How `labeled_break` combines with `nested_loops`:** A label is needed only when an inner loop must end or advance an outer loop. The label goes on the outer loop header, and both loops share the outer variables, which keep the values they had at the exit.

### `nested_loops` comes before `matrix_operations`

*matrix addition and multiplication with nested loops*

Matrix addition uses two nested loops over i and j, and matrix multiplication adds a third inner loop over k to compute each dot product c[i][j].

- **Grounding:** book passage
- **How `nested_loops` combines with `matrix_operations`:** Matrix addition uses two nested loops over i and j; matrix multiplication adds a third, innermost loop over k for each dot product.
- **How `matrix_operations` combines with `nested_loops`:** Addition uses two nested loops (i, j); multiplication adds a third inner loop over k for each dot product.

### `nested_loops` comes before `row_major_order`

*Row-major and column-major order: processing a 2-D array row by row (row-major) or column by column (column-major)*

Which loop is outside decides whether the entries are processed row by row or column by column.

- **Grounding:** book passage
- **How `nested_loops` combines with `row_major_order`:** Which loop is outside decides the visiting order: row index outside gives row-major order, column index outside gives column-major order.
- **How `row_major_order` combines with `nested_loops`:** Which loop is outside decides whether entries are processed row by row or column by column; the inner loop finishes for each outer value.

## Learned alongside (0)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

No parallel edge touches this concept.

## Misconceptions (7)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### EmptyInnerLoopSkipsRest

- **Wrong rule:** If the inner loop runs zero times, the rest of that outer pass is skipped too.
- **Right rule:** An inner loop that runs zero times just ends; the statements after it in the outer body still run.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: If the inner loop runs zero times, the rest of that outer pass is skipped too. Right rule: An inner loop that runs zero times just ends; the statements after it in the outer body still run.

### InconsistentIndentation

- **Wrong rule:** Indents nested blocks inconsistently, so the visual nesting differs from the real nesting.
- **Right rule:** Indent consistently, one level deeper for each nested block, so the layout shows the real nesting; the compiler ignores indentation.
- **Role of this concept:** context
- **Also an edge from `block`:** Indents nested blocks inconsistently, so the visual nesting differs from the real nesting.
- **Also an edge from `nested_conditionals`:** Indents nested blocks inconsistently, so the visual nesting differs from the real nesting.
- **Also an edge from `program_layout`:** Indents nested blocks inconsistently, so the visual nesting differs from the real nesting.

### InnerCounterOverwritesOuter

- **Wrong rule:** The inner loop count replaces the outer loop count, so the nested loops run as one loop.
- **Right rule:** The two counts multiply: the inner body runs (outer passes) x (inner passes) times.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: The inner loop count replaces the outer loop count, so the nested loops run as one loop. Right rule: The two counts multiply: the inner body runs (outer passes) x (inner passes) times.

### InnerOuterSwapped

- **Wrong rule:** The inner loop's variable changes more slowly than the outer loop's.
- **Right rule:** The inner loop runs all its passes for each single pass of the outer loop.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: The inner loop's variable changes more slowly than the outer loop's. Right rule: The inner loop runs all its passes for each single pass of the outer loop.

### NestedLoopsLockstep

- **Wrong rule:** Nested loops run in step as one loop: both variables change together and both conditions are tested together.
- **Right rule:** For each pass of the outer loop the inner loop runs all its passes; the inner variable changes fastest.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: Nested loops run in step as one loop: both variables change together and both conditions are tested together. Right rule: For each pass of the outer loop the inner loop runs all its passes; the inner variable changes fastest.

### NestedLoopsSequential

- **Wrong rule:** The outer loop runs completely, then the inner loop runs completely.
- **Right rule:** The inner loop runs all its passes during each single pass of the outer loop.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: The outer loop runs completely, then the inner loop runs completely. Right rule: The inner loop runs all its passes during each single pass of the outer loop.
- **Shows at level L0 as:** inconsistent trace: Applies the nested-loop rule (LT) unevenly: resets the inner variable on some outer passes but not others, or advances the outer variable in the middle of the inner loop. (here mixing in: "The outer loop runs completely, then the inner loop runs completely")

### OuterLoopIgnored

- **Wrong rule:** In nested loops only the inner loop repeats; the outer loop runs once.
- **Right rule:** The outer loop repeats as its own condition says, and the inner loop runs fully on each outer pass.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: In nested loops only the inner loop repeats; the outer loop runs once. Right rule: The outer loop repeats as its own condition says, and the inner loop runs fully on each outer pass.

## Errors (1)

An error edge states the rule that gets broken in a program, and the right rule.

### BracelessMultiStatementBody

- **Wrong rule:** Indenting several statements under an if or for makes them all part of its body, even without braces.
- **Right rule:** Without braces only the first statement belongs to the if/for; the rest run once, after it.
- **Role of this concept:** context
- **Also an edge from `for_loop`:** Indenting several statements under an if or for makes them all part of its body, even without braces.
- **Also an edge from `if_statement`:** Indenting several statements under an if or for makes them all part of its body, even without braces.
- **Also an edge from `loop_body`:** Indenting several statements under an if or for makes them all part of its body, even without braces.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for nested loops: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to nested loops agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

nested loops -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (8 ways).

- **everyday reading** (folk-meaning rule): Folk meaning: 'for each row and each column' sounds like doing two things side by side or one after the other. In Java the inner loop is a statement in the outer body, so it runs all its passes during each single outer pass (like the hands of a clock).
- **misconception** (wrong rule / right rule; shows `NestedLoopsSequential`): wrong rule: The outer loop runs completely, then the inner loop runs completely. Right rule: The inner loop runs all its passes during each single pass of the outer loop.
- **misconception** (wrong rule / right rule; shows `InnerOuterSwapped`): wrong rule: The inner loop's variable changes more slowly than the outer loop's. Right rule: The inner loop runs all its passes for each single pass of the outer loop.
- **misconception** (wrong rule / right rule; shows `NestedLoopsLockstep`): wrong rule: Nested loops run in step as one loop: both variables change together and both conditions are tested together. Right rule: For each pass of the outer loop the inner loop runs all its passes; the inner variable changes fastest.
- **misconception** (wrong rule / right rule; shows `OuterLoopIgnored`): wrong rule: In nested loops only the inner loop repeats; the outer loop runs once. Right rule: The outer loop repeats as its own condition says, and the inner loop runs fully on each outer pass.
- **misconception** (wrong rule / right rule; shows `InnerCounterOverwritesOuter`): wrong rule: The inner loop count replaces the outer loop count, so the nested loops run as one loop. Right rule: The two counts multiply: the inner body runs (outer passes) x (inner passes) times.
- **misconception** (wrong rule / right rule; shows `EmptyInnerLoopSkipsRest`): wrong rule: If the inner loop runs zero times, the rest of that outer pass is skipped too. Right rule: An inner loop that runs zero times just ends; the statements after it in the outer body still run.
- **inconsistent trace** (uneven-application rule; shows `NestedLoopsSequential`): Applies the nested-loop rule (LT) unevenly: resets the inner variable on some outer passes but not others, or advances the outer variable in the middle of the inner loop. (here mixing in: "The outer loop runs completely, then the inner loop runs completely")

### L1: Unistructural / atom x text surface

L1 for nested loops: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

nested loops -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

- **names the element** (identity rule): Nested loops are a loop inside the body of another loop: the outer loop and the inner loop.
- **states the rule** (declarative rule): Because loops are statements, one can be the body of another; the inner loop iterates all the way through for each iteration of the outer loop.

### L2: Multistructural / block x execution / preoperational

L2 for nested loops: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

nested loops -&gt; L2 (Multistructural): the answer applies the rules of nested loops to every part of the code, in order (3 ways).

- **line by line trace** (operational sequencing rule): Outer init; outer test; [inner init; inner test; inner body; inner update; ... until the inner test fails]; rest of the outer body; outer update; outer test; ... The inner init runs again on every outer pass.
- **output prediction** (evaluation / result rule): The inner body runs (outer passes) x (inner passes) times: two loops of 1..10 call printf 100 times; DivisorPattern 3 prints 3 rows of 3 entries, each row ending with its row number.
- **one step execution** (state-transition rule): One outer pass resets the inner variable, runs the complete inner loop, executes the rest of the outer body once, and then updates the outer variable once.

### L3: Relational / relations x function (concrete operational begins)

L3 for nested loops: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

nested loops -&gt; L3 (Relational): the answer relates the parts (5 ways).

- **relation to neighbour** (composition rule (with a neighbour)): Usually both loops are for loops: the inner for runs its complete set of passes for every single pass of the outer for.
- **relation to neighbour** (composition rule (with a neighbour)): Matrix addition uses two nested loops over i and j; matrix multiplication adds a third, innermost loop over k for each dot product.
- **relation to neighbour** (composition rule (with a neighbour)): A plain break ends only the innermost loop; a labeled break is needed when the inner loop must end the outer one too.
- **relation to neighbour** (composition rule (with a neighbour)): Which loop is outside decides the visiting order: row index outside gives row-major order, column index outside gives column-major order.
- **purpose of the whole** (plan / role rule): Plan: process every pair (i, j) - two-dimensional tables, every row x column of a matrix, every pair of elements; the outer variable is a slow stepper, the inner a fast stepper.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for nested loops: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

nested loops -&gt; L4 (Extended abstract): the answer reasons beyond the given code (5 ways).

- **predict a change** (conservation rule; shows `NestedLoopsSequential`): Swapping the outer and inner loops visits the same pairs in a different order (rows vs columns), which preserves a sum but changes printed layout; moving a statement between the inner body and the outer body changes its count from (outer x inner) to outer.
- **transfer to a new program** (applicability rule): Use nested loops when the work ranges over all combinations of two indices (tables, matrices, pairs); expect running time proportional to the product of the pass counts, and prefer a single loop when the second index is a function of the first.
- **diagnose an error** (error rule): rule broken: Without braces, the body of an if, while or for is exactly one statement; indentation does not add statements to it. Kind: silent logic error. Trigger class: A braceless header followed by two or more indented statements: only the first is controlled, the others run once, after the if/loop, on every input.
- **diagnose an error** (error rule): rule broken: The inner loop needs its own loop variable. Kind: compile-time. Trigger class: Redeclaring the outer variable in the inner header (for (int i ...) { for (int i ...) }): 'variable i is already defined'.
- **diagnose an error** (error rule): rule broken: The inner loop must update its own variable. Kind: silent logic error. Trigger class: Writing for (int j = 0; j &lt; N; i++) in the inner loop: j never changes, so the inner loop is infinite (or i runs out of range).

## Same topic

`nested_loops` belongs to the topic **Nesting** (`topic1.3.e`). The topic also contains: `dangling_else`, `else_if_chain`, `nested_conditionals`.

## Rules of the concept (23)

- **folk-meaning rule:** Folk meaning: 'for each row and each column' sounds like doing two things side by side or one after the other. In Java the inner loop is a statement in the outer body, so it runs all its passes during each single outer pass (like the hands of a clock).
- **wrong rule / right rule:** InnerOuterSwapped: wrong: The inner loop's variable changes more slowly than the outer loop's. \| right: The inner loop runs all its passes for each single pass of the outer loop.
- **wrong rule / right rule:** NestedLoopsSequential: wrong: The outer loop runs completely, then the inner loop runs completely. \| right: The inner loop runs all its passes during each single pass of the outer loop.
- **wrong rule / right rule:** NestedLoopsLockstep: wrong: Nested loops run in step as one loop: both variables change together and both conditions are tested together. \| right: For each pass of the outer loop the inner loop runs all its passes; the inner variable changes fastest.
- **wrong rule / right rule:** OuterLoopIgnored: wrong: In nested loops only the inner loop repeats; the outer loop runs once. \| right: The outer loop repeats as its own condition says, and the inner loop runs fully on each outer pass.
- **wrong rule / right rule:** InnerCounterOverwritesOuter: wrong: The inner loop count replaces the outer loop count, so the nested loops run as one loop. \| right: The two counts multiply: the inner body runs (outer passes) x (inner passes) times.
- **wrong rule / right rule:** EmptyInnerLoopSkipsRest: wrong: If the inner loop runs zero times, the rest of that outer pass is skipped too. \| right: An inner loop that runs zero times just ends; the statements after it in the outer body still run.
- **uneven-application rule:** Applies the nested-loop rule (LT) unevenly: resets the inner variable on some outer passes but not others, or advances the outer variable in the middle of the inner loop.
- **identity rule:** Nested loops are a loop inside the body of another loop: the outer loop and the inner loop.
- **declarative rule:** Because loops are statements, one can be the body of another; the inner loop iterates all the way through for each iteration of the outer loop.
- **operational sequencing rule:** Outer init; outer test; [inner init; inner test; inner body; inner update; ... until the inner test fails]; rest of the outer body; outer update; outer test; ... The inner init runs again on every outer pass.
- **evaluation / result rule:** The inner body runs (outer passes) x (inner passes) times: two loops of 1..10 call printf 100 times; DivisorPattern 3 prints 3 rows of 3 entries, each row ending with its row number.
- **state-transition rule:** One outer pass resets the inner variable, runs the complete inner loop, executes the rest of the outer body once, and then updates the outer variable once.
- **composition rule (with a neighbour):** with for\_loop: Usually both loops are for loops: the inner for runs its complete set of passes for every single pass of the outer for.
- **composition rule (with a neighbour):** with matrix\_operations: Matrix addition uses two nested loops over i and j; matrix multiplication adds a third, innermost loop over k for each dot product.
- **composition rule (with a neighbour):** with labeled\_break: A plain break ends only the innermost loop; a labeled break is needed when the inner loop must end the outer one too.
- **composition rule (with a neighbour):** with row\_major\_order: Which loop is outside decides the visiting order: row index outside gives row-major order, column index outside gives column-major order.
- **plan / role rule:** Plan: process every pair (i, j) - two-dimensional tables, every row x column of a matrix, every pair of elements; the outer variable is a slow stepper, the inner a fast stepper.
- **conservation rule:** Swapping the outer and inner loops visits the same pairs in a different order (rows vs columns), which preserves a sum but changes printed layout; moving a statement between the inner body and the outer body changes its count from (outer x inner) to outer.
- **error rule:** rule broken: Without braces, the body of an if, while or for is exactly one statement; indentation does not add statements to it. (silent logic error)
- **error rule:** rule broken: The inner loop needs its own loop variable. (compile-time)
- **error rule:** rule broken: The inner loop must update its own variable. (silent logic error)
- **applicability rule:** Use nested loops when the work ranges over all combinations of two indices (tables, matrices, pairs); expect running time proportional to the product of the pass counts, and prefer a single loop when the second index is a function of the first.

## The whole prerequisite chain

- **Everything it builds on (16):** `arithmetic_operators`, `boolean`, `boolean_expression`, `comparison_operators`, `data_type`, `do_while_loop`, `expression`, `for_loop`, `identifier`, `literal`, `logical_operators`, `loop_control`, `loop_variable`, `primitive_type`, `variable`, `while_loop`
- **Everything that builds on it (6):** `convergence_rate`, `labeled_break`, `matrix_operations`, `power_method`, `row_major_order`, `two_models`
