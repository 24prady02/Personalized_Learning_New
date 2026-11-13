# logical_error (`logical_error`)

the program runs but computes the wrong result

Section 1.1 Your First Program, topic 1.1.c Errors.

![The knowledge graph around logical_error](logical_error.png)

## At a glance

- **Needs first:** `empty_statement`, `run`
- **Leads to:** `debugging`
- **Learned alongside:** `run_time_error`
- **Misconceptions:** `CompilesMeansWorks`
- **Errors:** `AccumulatorDeclaredInLoop`, `LoopIgnoresCodeBefore`, `SemicolonAfterIfHeader`
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 30 edges around this concept, each explained in the graph's own words.

## What it needs first (2)

A prerequisite edge means the other concept has to be understood before `logical_error`.

### `empty_statement` comes before `logical_error`

*a lone ; is an empty statement; a block can stand alone*

A ; right after an if or loop header is an empty statement, so the header controls nothing and the next line always runs: the program compiles but computes the wrong result.

- **Grounding:** spec passage

### `run` comes before `logical_error`

*java executes main in the JVM*

A logical error is seen only by running the program and comparing its output with the intended output.

- **Grounding:** book passage
- **How `logical_error` combines with `run`:** A logic error is seen only by running the program and comparing its output with the intended output.
- **How `run` combines with `logical_error`:** A logic error is seen only by running the program and comparing its output with the intended output.

## What it leads to (1)

These concepts need `logical_error` first.

### `logical_error` comes before `debugging`

*finding and fixing the cause of a wrong result or error by forming a hypothesis, changing the program and checking the prediction*

Debugging is mostly the search for logic errors, which give wrong output without any message.

- **Grounding:** book passage
- **How `debugging` combines with `logical_error`:** A logic error gives no message, so it is found only by comparing actual values with expected ones.

## Learned alongside (1)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

### `logical_error` alongside `run_time_error`

*an error raised while the program executes (e.g. ArrayIndexOutOfBounds, NumberFormatException)*

A run-time error stops the program with an exception; a logical error lets it finish with wrong output.

- **Grounding:** book passage
- **How `logical_error` combines with `run_time_error`:** A run-time error stops the program with an exception; a logic error lets it finish with wrong output.
- **How `run_time_error` combines with `logical_error`:** A run-time error stops the program with an exception message; a logic error lets it finish with wrong output and no message.

## Misconceptions (1)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### CompilesMeansWorks

- **Wrong rule:** Code that compiles is code that works.
- **Right rule:** Code that compiles can still have run-time and logical errors.
- **Role of this concept:** context
- **Shows at level L0 as:** misconception: wrong rule: Code that compiles is code that works. Right rule: Code that compiles and runs can still compute the wrong result (a logic error).
- **Shows at level L0 as:** inconsistent trace: Applies the 'computer does exactly what is written' rule unevenly: traces some lines literally but reads the intended meaning into the faulty line, and so does not see the bug. (here mixing in: "Code that compiles is code that works")
- **Also an edge from `compile`:** Code that compiles is code that works.
- **Also an edge from `compile_time_error`:** Code that compiles is code that works.
- **Also an edge from `run_time_error`:** Code that compiles is code that works.
- **Also an edge from `testing`:** Code that compiles is code that works.

## Errors (3)

An error edge states the rule that gets broken in a program, and the right rule.

### AccumulatorDeclaredInLoop

- **Wrong rule:** Declaring sum inside the loop body keeps a running total across passes.
- **Right rule:** The accumulator must be declared and initialised before the loop.
- **Role of this concept:** context
- **Also an edge from `accumulator_pattern`:** Declaring sum inside the loop body keeps a running total across passes.
- **Also an edge from `counter_pattern`:** Declaring sum inside the loop body keeps a running total across passes.
- **Also an edge from `loop_scope`:** Declaring sum inside the loop body keeps a running total across passes.

### LoopIgnoresCodeBefore

- **Wrong rule:** Initializes the flag before the loop so that the loop condition is already false, and the loop body never runs.
- **Right rule:** A while loop tests its condition before the first pass: if the values set before the loop make the condition false, the body never runs.
- **Role of this concept:** context
- **Also an edge from `flag_search_loop`:** Initializes the flag before the loop so that the loop condition is already false, and the loop body never runs.
- **Also an edge from `while_loop`:** Initializes the flag before the loop so that the loop condition is already false, and the loop body never runs.

### SemicolonAfterIfHeader

- **Wrong rule:** if (x &gt; 0); System.out.println("positive"); prints only for positive x.
- **Right rule:** The ; ends the if with an empty statement, so the next line always runs.
- **Role of this concept:** context
- **Also an edge from `empty_statement`:** if (x &gt; 0); System.out.println("positive"); prints only for positive x.
- **Also an edge from `for_loop`:** if (x &gt; 0); System.out.println("positive"); prints only for positive x.
- **Also an edge from `if_statement`:** if (x &gt; 0); System.out.println("positive"); prints only for positive x.
- **Also an edge from `while_loop`:** if (x &gt; 0); System.out.println("positive"); prints only for positive x.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for logical error: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to logical error agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

logical error -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (3 ways).

- **everyday reading** (folk-meaning rule): Everyday reading: the computer understands what you meant and will complain if the program is wrong. Java rule: a program with a logic error compiles and runs without any message and does exactly what the code says, which differs from what was intended.
- **misconception** (wrong rule / right rule; shows `CompilesMeansWorks`): wrong rule: Code that compiles is code that works. Right rule: Code that compiles and runs can still compute the wrong result (a logic error).
- **inconsistent trace** (uneven-application rule; shows `CompilesMeansWorks`): Applies the 'computer does exactly what is written' rule unevenly: traces some lines literally but reads the intended meaning into the faulty line, and so does not see the bug. (here mixing in: "Code that compiles is code that works")

### L1: Unistructural / atom x text surface

L1 for logical error: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

logical error -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

- **names the element** (identity rule): A logic error is an error that makes a program do something other than what the programmer intended, without any compiler or run-time message.
- **states the rule** (declarative rule): If a program has a logic error, it will compile and run without generating error messages, but it will not do the right thing; the compiler and JVM cannot detect it since they don't know what the right thing is.

### L2: Multistructural / block x execution / preoperational

L2 for logical error: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

logical error -&gt; L2 (Multistructural): the answer applies the rules of logical error to every part of the code, in order (3 ways).

- **line by line trace** (operational sequencing rule): Execution proceeds normally, statement by statement; the faulty statement executes without complaint and passes a wrong value or output onward.
- **output prediction** (evaluation / result rule): Result is a normal-looking but wrong output, e.g. println("Hello, "); println("World!"); prints two lines where one was intended.
- **one step execution** (state-transition rule): Each step makes a legal state change (e.g. an empty statement after if, or resetting sum each pass), but not the intended one.

### L3: Relational / relations x function (concrete operational begins)

L3 for logical error: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

logical error -&gt; L3 (Relational): the answer relates the parts (4 ways).

- **relation to neighbour** (composition rule (with a neighbour)): A logic error is seen only by running the program and comparing its output with the intended output.
- **relation to neighbour** (composition rule (with a neighbour)): A run-time error stops the program with an exception; a logic error lets it finish with wrong output.
- **relation to neighbour** (composition rule (with a neighbour)): Debugging is mostly the search for logic errors, which give wrong output without any message.
- **purpose of the whole** (plan / role rule): Purpose (of the category): name the errors that only testing against the intended behaviour can find, so they are found by tracing, test cases and added print statements.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for logical error: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

logical error -&gt; L4 (Extended abstract): the answer reasons beyond the given code (6 ways).

- **predict a change** (conservation rule; shows `CompilesMeansWorks`): A logic error survives recompiling and rerunning unchanged; changing input may hide or reveal it; fixing it changes output only on the inputs it affected.
- **diagnose an error** (error rule): rule broken: A ; right after if (...) is an empty statement that forms the whole if body. Kind: silent logic error. Trigger class: if (x &gt; 0); System.out.println("positive"); prints for every x
- **diagnose an error** (error rule): rule broken: The accumulator must be declared and initialized before the loop. Kind: silent logic error. Trigger class: int sum = 0; written inside the loop body: sum is reset each pass (and is out of scope after the loop)
- **transfer to a new program** (applicability rule): Suspect a logic error when the program compiles and runs to the end but the output is wrong for some inputs; locate it by hand tracing, minimal test cases and print statements, since tools give no message.
- **diagnose an error** (error rule): rule broken: A while loop tests its condition before the first pass. Kind: silent logic error. Trigger class: values set before the loop already make the condition false, so the body never runs
- **diagnose an error** (error rule): rule broken: print vs println decides line breaks. Kind: silent logic error. Trigger class: println used where print was meant (or the reverse)

## Same topic

`logical_error` belongs to the topic **Errors** (`topic1.1.c`). The topic also contains: `compile_time_error`, `reading_error_messages`, `run_time_error`.

## Rules of the concept (17)

- **folk-meaning rule:** Everyday reading: the computer understands what you meant and will complain if the program is wrong. Java rule: a program with a logic error compiles and runs without any message and does exactly what the code says, which differs from what was intended.
- **wrong rule / right rule:** CompilesMeansWorks: wrong: Code that compiles is code that works. \| right: Code that compiles and runs can still compute the wrong result (a logic error).
- **uneven-application rule:** Applies the 'computer does exactly what is written' rule unevenly: traces some lines literally but reads the intended meaning into the faulty line, and so does not see the bug.
- **identity rule:** A logic error is an error that makes a program do something other than what the programmer intended, without any compiler or run-time message.
- **declarative rule:** If a program has a logic error, it will compile and run without generating error messages, but it will not do the right thing; the compiler and JVM cannot detect it since they don't know what the right thing is.
- **operational sequencing rule:** Execution proceeds normally, statement by statement; the faulty statement executes without complaint and passes a wrong value or output onward.
- **evaluation / result rule:** Result is a normal-looking but wrong output, e.g. println("Hello, "); println("World!"); prints two lines where one was intended.
- **state-transition rule:** Each step makes a legal state change (e.g. an empty statement after if, or resetting sum each pass), but not the intended one.
- **composition rule (with a neighbour):** with run: A logic error is seen only by running the program and comparing its output with the intended output.
- **composition rule (with a neighbour):** with run\_time\_error: A run-time error stops the program with an exception; a logic error lets it finish with wrong output.
- **plan / role rule:** Purpose (of the category): name the errors that only testing against the intended behaviour can find, so they are found by tracing, test cases and added print statements.
- **conservation rule:** A logic error survives recompiling and rerunning unchanged; changing input may hide or reveal it; fixing it changes output only on the inputs it affected.
- **error rule:** rule broken: The accumulator must be declared and initialized before the loop (silent logic error)
- **error rule:** rule broken: A ; right after if (...) is an empty statement that forms the whole if body (silent logic error)
- **error rule:** rule broken: A while loop tests its condition before the first pass (silent logic error)
- **error rule:** rule broken: print vs println decides line breaks (silent logic error)
- **applicability rule:** Suspect a logic error when the program compiles and runs to the end but the output is wrong for some inputs; locate it by hand tracing, minimal test cases and print statements, since tools give no message.

## The whole prerequisite chain

- **Everything it builds on (7):** `class_declaration`, `compile`, `empty_statement`, `main_method`, `program_text`, `run`, `statement`
- **Everything that builds on it (1):** `debugging`
