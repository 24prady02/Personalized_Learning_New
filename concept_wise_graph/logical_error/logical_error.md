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

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 30 edges around this concept. The edge logic, the wrong and right rules and the exact rules of the ways are copied word for word from the graph.

## To work on (0)

Nothing is missing for this concept.

## What it needs first (2)

A prerequisite edge means the other concept has to be understood before `logical_error`.

### `empty_statement` comes before `logical_error`

*a lone ; is an empty statement; a block can stand alone*

- **Edge:** `pre:empty_statement->logical_error`
- **Exact edge logic:** A ; right after an if or loop header is an empty statement, so the header controls nothing and the next line always runs: the program compiles but computes the wrong result.
- **Grounding:** spec\_passage

### `run` comes before `logical_error`

*java executes main in the JVM*

- **Edge:** `pre:run->logical_error`
- **Exact edge logic:** A logical error is seen only by running the program and comparing its output with the intended output.
- **Grounding:** book\_passage
- **Composition rule (R) of `logical_error` with `run`:** A logic error is seen only by running the program and comparing its output with the intended output.
- **Composition rule (R) of `run` with `logical_error`:** A logic error is seen only by running the program and comparing its output with the intended output.

## What it leads to (1)

These concepts need `logical_error` first.

### `logical_error` comes before `debugging`

*finding and fixing the cause of a wrong result or error by forming a hypothesis, changing the program and checking the prediction*

- **Edge:** `pre:logical_error->debugging`
- **Exact edge logic:** Debugging is mostly the search for logic errors, which give wrong output without any message.
- **Grounding:** book\_passage
- **Composition rule (R) of `debugging` with `logical_error`:** A logic error gives no message, so it is found only by comparing actual values with expected ones.

## Learned alongside (1)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

### `logical_error` alongside `run_time_error`

*an error raised while the program executes (e.g. ArrayIndexOutOfBounds, NumberFormatException)*

- **Edge:** `par:run_time_error~logical_error`
- **Exact edge logic:** A run-time error stops the program with an exception; a logical error lets it finish with wrong output.
- **Grounding:** book\_passage
- **Composition rule (R) of `logical_error` with `run_time_error`:** A run-time error stops the program with an exception; a logic error lets it finish with wrong output.
- **Composition rule (R) of `run_time_error` with `logical_error`:** A run-time error stops the program with an exception message; a logic error lets it finish with wrong output and no message.

## Misconceptions (1)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### CompilesMeansWorks

- **Edge:** `logical_error` &rarr; `CompilesMeansWorks` (misconception)
- **Exact edge logic (the wrong rule):** Code that compiles is code that works.
- **Twin logic (the right rule):** Code that compiles can still have run-time and logical errors.
- **Wrong belief (on the node):** Code that compiles is code that works.
- **Correct rule (on the node):** Code that compiles can still have run-time and logical errors.
- **Provenance:** published
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [1] misconception, exact rule:** wrong rule: Code that compiles is code that works. Right rule: Code that compiles and runs can still compute the wrong result (a logic error).
- **L0 way [2] inconsistent\_trace, exact rule:** Applies the 'computer does exactly what is written' rule unevenly: traces some lines literally but reads the intended meaning into the faulty line, and so does not see the bug. (here mixing in: "Code that compiles is code that works")
- **Edge `compile` &rarr; `CompilesMeansWorks`, exact edge logic:** Code that compiles is code that works. **Twin logic:** Code that compiles can still have run-time and logical errors. (role: primary)
- **Edge `compile_time_error` &rarr; `CompilesMeansWorks`, exact edge logic:** Code that compiles is code that works. **Twin logic:** Code that compiles can still have run-time and logical errors. (role: context)
- **Edge `run_time_error` &rarr; `CompilesMeansWorks`, exact edge logic:** Code that compiles is code that works. **Twin logic:** Code that compiles can still have run-time and logical errors. (role: context)
- **Edge `testing` &rarr; `CompilesMeansWorks`, exact edge logic:** Code that compiles is code that works. **Twin logic:** Code that compiles can still have run-time and logical errors. (role: context)

## Errors (3)

An error edge states the rule that gets broken in a program, and the right rule.

### AccumulatorDeclaredInLoop

- **Edge:** `logical_error` &rarr; `AccumulatorDeclaredInLoop` (error)
- **Exact edge logic (the wrong rule):** Declaring sum inside the loop body keeps a running total across passes.
- **Twin logic (the right rule):** The accumulator must be declared and initialised before the loop.
- **Wrong belief (on the node):** Declaring sum inside the loop body keeps a running total across passes.
- **Correct rule (on the node):** The accumulator must be declared and initialised before the loop.
- **Provenance:** textbook
- **Role of this concept:** context
- **Edge `accumulator_pattern` &rarr; `AccumulatorDeclaredInLoop`, exact edge logic:** Declaring sum inside the loop body keeps a running total across passes. **Twin logic:** The accumulator must be declared and initialised before the loop. (role: context)
- **Edge `counter_pattern` &rarr; `AccumulatorDeclaredInLoop`, exact edge logic:** Declaring sum inside the loop body keeps a running total across passes. **Twin logic:** The accumulator must be declared and initialised before the loop. (role: context)
- **Edge `loop_scope` &rarr; `AccumulatorDeclaredInLoop`, exact edge logic:** Declaring sum inside the loop body keeps a running total across passes. **Twin logic:** The accumulator must be declared and initialised before the loop. (role: primary)

### LoopIgnoresCodeBefore

- **Edge:** `logical_error` &rarr; `LoopIgnoresCodeBefore` (error)
- **Exact edge logic (the wrong rule):** Initializes the flag before the loop so that the loop condition is already false, and the loop body never runs.
- **Twin logic (the right rule):** A while loop tests its condition before the first pass: if the values set before the loop make the condition false, the body never runs.
- **Wrong belief (on the node):** Initializes the flag before the loop so that the loop condition is already false, and the loop body never runs.
- **Correct rule (on the node):** A while loop tests its condition before the first pass: if the values set before the loop make the condition false, the body never runs.
- **Provenance:** published
- **Role of this concept:** context
- **Edge `flag_search_loop` &rarr; `LoopIgnoresCodeBefore`, exact edge logic:** Initializes the flag before the loop so that the loop condition is already false, and the loop body never runs. **Twin logic:** A while loop tests its condition before the first pass: if the values set before the loop make the condition false, the body never runs. (role: context)
- **Edge `while_loop` &rarr; `LoopIgnoresCodeBefore`, exact edge logic:** Initializes the flag before the loop so that the loop condition is already false, and the loop body never runs. **Twin logic:** A while loop tests its condition before the first pass: if the values set before the loop make the condition false, the body never runs. (role: primary)

### SemicolonAfterIfHeader

- **Edge:** `logical_error` &rarr; `SemicolonAfterIfHeader` (error)
- **Exact edge logic (the wrong rule):** if (x &gt; 0); System.out.println("positive"); prints only for positive x.
- **Twin logic (the right rule):** The ; ends the if with an empty statement, so the next line always runs.
- **Wrong belief (on the node):** if (x &gt; 0); System.out.println("positive"); prints only for positive x.
- **Correct rule (on the node):** The ; ends the if with an empty statement, so the next line always runs.
- **Provenance:** published
- **Role of this concept:** context
- **Edge `empty_statement` &rarr; `SemicolonAfterIfHeader`, exact edge logic:** if (x &gt; 0); System.out.println("positive"); prints only for positive x. **Twin logic:** The ; ends the if with an empty statement, so the next line always runs. (role: context)
- **Edge `for_loop` &rarr; `SemicolonAfterIfHeader`, exact edge logic:** if (x &gt; 0); System.out.println("positive"); prints only for positive x. **Twin logic:** The ; ends the if with an empty statement, so the next line always runs. (role: context)
- **Edge `if_statement` &rarr; `SemicolonAfterIfHeader`, exact edge logic:** if (x &gt; 0); System.out.println("positive"); prints only for positive x. **Twin logic:** The ; ends the if with an empty statement, so the next line always runs. (role: primary)
- **Edge `while_loop` &rarr; `SemicolonAfterIfHeader`, exact edge logic:** if (x &gt; 0); System.out.println("positive"); prints only for positive x. **Twin logic:** The ; ends the if with an empty statement, so the next line always runs. (role: context)

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for logical error: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to logical error agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

- **Edge:** `logical_error` &rarr; `logical_error@L0` (has_level)
- **Exact edge logic:** logical error -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (3 ways).

Ways (3), each with its exact rule:

- **[0] everyday\_reading** (rule type E, folk-meaning rule): Everyday reading: the computer understands what you meant and will complain if the program is wrong. Java rule: a program with a logic error compiles and runs without any message and does exactly what the code says, which differs from what was intended.
- **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `CompilesMeansWorks`: wrong rule: Code that compiles is code that works. Right rule: Code that compiles and runs can still compute the wrong result (a logic error).
- **[2] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `CompilesMeansWorks`: Applies the 'computer does exactly what is written' rule unevenly: traces some lines literally but reads the intended meaning into the faulty line, and so does not see the bug. (here mixing in: "Code that compiles is code that works")

### L1: Unistructural / atom x text surface

L1 for logical error: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

- **Edge:** `logical_error` &rarr; `logical_error@L1` (has_level)
- **Exact edge logic:** logical error -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

Ways (2), each with its exact rule:

- **[0] names\_the\_element** (rule type N, identity rule): A logic error is an error that makes a program do something other than what the programmer intended, without any compiler or run-time message.
- **[1] states\_the\_rule** (rule type S, declarative rule): If a program has a logic error, it will compile and run without generating error messages, but it will not do the right thing; the compiler and JVM cannot detect it since they don't know what the right thing is.

### L2: Multistructural / block x execution / preoperational

L2 for logical error: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

- **Edge:** `logical_error` &rarr; `logical_error@L2` (has_level)
- **Exact edge logic:** logical error -&gt; L2 (Multistructural): the answer applies the rules of logical error to every part of the code, in order (3 ways).

Ways (3), each with its exact rule:

- **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): Execution proceeds normally, statement by statement; the faulty statement executes without complaint and passes a wrong value or output onward.
- **[1] output\_prediction** (rule type OP, evaluation / result rule): Result is a normal-looking but wrong output, e.g. println("Hello, "); println("World!"); prints two lines where one was intended.
- **[2] one\_step\_execution** (rule type OS, state-transition rule): Each step makes a legal state change (e.g. an empty statement after if, or resetting sum each pass), but not the intended one.

### L3: Relational / relations x function (concrete operational begins)

L3 for logical error: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

- **Edge:** `logical_error` &rarr; `logical_error@L3` (has_level)
- **Exact edge logic:** logical error -&gt; L3 (Relational): the answer relates the parts (4 ways).

Ways (4), each with its exact rule:

- **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): A logic error is seen only by running the program and comparing its output with the intended output.
- **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): A run-time error stops the program with an exception; a logic error lets it finish with wrong output.
- **[2] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Debugging is mostly the search for logic errors, which give wrong output without any message.
- **[3] purpose\_of\_the\_whole** (rule type P, plan / role rule): Purpose (of the category): name the errors that only testing against the intended behaviour can find, so they are found by tracing, test cases and added print statements.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for logical error: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

- **Edge:** `logical_error` &rarr; `logical_error@L4` (has_level)
- **Exact edge logic:** logical error -&gt; L4 (Extended abstract): the answer reasons beyond the given code (6 ways).

Ways (6), each with its exact rule:

- **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `CompilesMeansWorks`: A logic error survives recompiling and rerunning unchanged; changing input may hide or reveal it; fixing it changes output only on the inputs it affected.
- **[1] diagnose\_an\_error** (rule type D, error rule): rule broken: A ; right after if (...) is an empty statement that forms the whole if body. Kind: silent logic error. Trigger class: if (x &gt; 0); System.out.println("positive"); prints for every x
- **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: The accumulator must be declared and initialized before the loop. Kind: silent logic error. Trigger class: int sum = 0; written inside the loop body: sum is reset each pass (and is out of scope after the loop)
- **[3] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Suspect a logic error when the program compiles and runs to the end but the output is wrong for some inputs; locate it by hand tracing, minimal test cases and print statements, since tools give no message.
- **[4] diagnose\_an\_error** (rule type D, error rule): rule broken: A while loop tests its condition before the first pass. Kind: silent logic error. Trigger class: values set before the loop already make the condition false, so the body never runs
- **[5] diagnose\_an\_error** (rule type D, error rule): rule broken: print vs println decides line breaks. Kind: silent logic error. Trigger class: println used where print was meant (or the reverse)

## Same topic

`logical_error` belongs to the topic **Errors** (`topic1.1.c`). The topic also contains: `compile_time_error`, `reading_error_messages`, `run_time_error`.

## Rules of the concept (17)

- **Book** (TJ-2e, p. 28 (pdf 50)): "If your program has a logic error, it will compile and run without generating error messages"
- **Book** (TJ-2e, p. 29 (pdf 51)): "Instead, it will do exactly what you told it to do."
- **Book** (SW-1.1, ): "These errors are (hopefully) caught by the programmer when we execute the program"
- **E** (folk-meaning rule): Everyday reading: the computer understands what you meant and will complain if the program is wrong. Java rule: a program with a logic error compiles and runs without any message and does exactly what the code says, which differs from what was intended.
- **M** (wrong rule / right rule): CompilesMeansWorks: wrong: Code that compiles is code that works. \| right: Code that compiles and runs can still compute the wrong result (a logic error).
- **T** (uneven-application rule): Applies the 'computer does exactly what is written' rule unevenly: traces some lines literally but reads the intended meaning into the faulty line, and so does not see the bug.
- **N** (identity rule): A logic error is an error that makes a program do something other than what the programmer intended, without any compiler or run-time message.
- **S** (declarative rule): If a program has a logic error, it will compile and run without generating error messages, but it will not do the right thing; the compiler and JVM cannot detect it since they don't know what the right thing is.
- **LT** (operational sequencing rule): Execution proceeds normally, statement by statement; the faulty statement executes without complaint and passes a wrong value or output onward.
- **OP** (evaluation / result rule): Result is a normal-looking but wrong output, e.g. println("Hello, "); println("World!"); prints two lines where one was intended.
- **OS** (state-transition rule): Each step makes a legal state change (e.g. an empty statement after if, or resetting sum each pass), but not the intended one.
- **R** (composition rule (with a neighbour)): with run: A logic error is seen only by running the program and comparing its output with the intended output.
- **R** (composition rule (with a neighbour)): with run\_time\_error: A run-time error stops the program with an exception; a logic error lets it finish with wrong output.
- **P** (plan / role rule): Purpose (of the category): name the errors that only testing against the intended behaviour can find, so they are found by tracing, test cases and added print statements.
- **C** (conservation rule): A logic error survives recompiling and rerunning unchanged; changing input may hide or reveal it; fixing it changes output only on the inputs it affected.
- **D** (error rule): rule broken: The accumulator must be declared and initialized before the loop (silent logic error)
- **D** (error rule): rule broken: A ; right after if (...) is an empty statement that forms the whole if body (silent logic error)
- **D** (error rule): rule broken: A while loop tests its condition before the first pass (silent logic error)
- **D** (error rule): rule broken: print vs println decides line breaks (silent logic error)
- **X** (applicability rule): Suspect a logic error when the program compiles and runs to the end but the output is wrong for some inputs; locate it by hand tracing, minimal test cases and print statements, since tools give no message.

## How it is found in code and answers (reader block)

- **Aliases:** logic error, logical error, wrong output, bug
- **Code patterns:** none
- **Operator symbols:** none
- **Java types:** none
- **Signal stray\_semicolon** (scope program, decisive): `(?:^|[;{])[ \t]*(?:if|while|for)\s*\((?:[^()]|\([^()]*\))*\)\s*;`

## The whole prerequisite chain

- **Everything it builds on (7):** `class_declaration`, `compile`, `empty_statement`, `main_method`, `program_text`, `run`, `statement`
- **Everything that builds on it (1):** `debugging`

## Every edge in this view and its exact edge logic (30)

All the edges drawn in the picture, in the order: prerequisite, parallel, misconception, error, has_level, contains.

**1. `empty_statement` &rarr; `logical_error`** (prerequisite)

- **Exact edge logic:** A ; right after an if or loop header is an empty statement, so the header controls nothing and the next line always runs: the program compiles but computes the wrong result.
- **Grounding:** spec\_passage

**2. `logical_error` &rarr; `debugging`** (prerequisite)

- **Exact edge logic:** Debugging is mostly the search for logic errors, which give wrong output without any message.
- **Grounding:** book\_passage
- **Composition rule (R) of `debugging` with `logical_error`:** A logic error gives no message, so it is found only by comparing actual values with expected ones.

**3. `run` &rarr; `logical_error`** (prerequisite)

- **Exact edge logic:** A logical error is seen only by running the program and comparing its output with the intended output.
- **Grounding:** book\_passage
- **Composition rule (R) of `run` with `logical_error`:** A logic error is seen only by running the program and comparing its output with the intended output.
- **Composition rule (R) of `logical_error` with `run`:** A logic error is seen only by running the program and comparing its output with the intended output.

**4. `run_time_error` &harr; `logical_error`** (parallel)

- **Exact edge logic:** A run-time error stops the program with an exception; a logical error lets it finish with wrong output.
- **Grounding:** book\_passage
- **Composition rule (R) of `run_time_error` with `logical_error`:** A run-time error stops the program with an exception message; a logic error lets it finish with wrong output and no message.
- **Composition rule (R) of `logical_error` with `run_time_error`:** A run-time error stops the program with an exception; a logic error lets it finish with wrong output.

**5. `logical_error` &rarr; `CompilesMeansWorks`** (misconception)

- **Exact edge logic (the wrong rule):** Code that compiles is code that works.
- **Twin logic (the right rule):** Code that compiles can still have run-time and logical errors.
- **Role:** context

**6. `compile` &rarr; `CompilesMeansWorks`** (misconception)

- **Exact edge logic (the wrong rule):** Code that compiles is code that works.
- **Twin logic (the right rule):** Code that compiles can still have run-time and logical errors.
- **Role:** primary

**7. `compile_time_error` &rarr; `CompilesMeansWorks`** (misconception)

- **Exact edge logic (the wrong rule):** Code that compiles is code that works.
- **Twin logic (the right rule):** Code that compiles can still have run-time and logical errors.
- **Role:** context

**8. `run_time_error` &rarr; `CompilesMeansWorks`** (misconception)

- **Exact edge logic (the wrong rule):** Code that compiles is code that works.
- **Twin logic (the right rule):** Code that compiles can still have run-time and logical errors.
- **Role:** context

**9. `testing` &rarr; `CompilesMeansWorks`** (misconception)

- **Exact edge logic (the wrong rule):** Code that compiles is code that works.
- **Twin logic (the right rule):** Code that compiles can still have run-time and logical errors.
- **Role:** context

**10. `logical_error` &rarr; `AccumulatorDeclaredInLoop`** (error)

- **Exact edge logic (the wrong rule):** Declaring sum inside the loop body keeps a running total across passes.
- **Twin logic (the right rule):** The accumulator must be declared and initialised before the loop.
- **Role:** context

**11. `logical_error` &rarr; `LoopIgnoresCodeBefore`** (error)

- **Exact edge logic (the wrong rule):** Initializes the flag before the loop so that the loop condition is already false, and the loop body never runs.
- **Twin logic (the right rule):** A while loop tests its condition before the first pass: if the values set before the loop make the condition false, the body never runs.
- **Role:** context

**12. `logical_error` &rarr; `SemicolonAfterIfHeader`** (error)

- **Exact edge logic (the wrong rule):** if (x &gt; 0); System.out.println("positive"); prints only for positive x.
- **Twin logic (the right rule):** The ; ends the if with an empty statement, so the next line always runs.
- **Role:** context

**13. `accumulator_pattern` &rarr; `AccumulatorDeclaredInLoop`** (error)

- **Exact edge logic (the wrong rule):** Declaring sum inside the loop body keeps a running total across passes.
- **Twin logic (the right rule):** The accumulator must be declared and initialised before the loop.
- **Role:** context

**14. `counter_pattern` &rarr; `AccumulatorDeclaredInLoop`** (error)

- **Exact edge logic (the wrong rule):** Declaring sum inside the loop body keeps a running total across passes.
- **Twin logic (the right rule):** The accumulator must be declared and initialised before the loop.
- **Role:** context

**15. `empty_statement` &rarr; `SemicolonAfterIfHeader`** (error)

- **Exact edge logic (the wrong rule):** if (x &gt; 0); System.out.println("positive"); prints only for positive x.
- **Twin logic (the right rule):** The ; ends the if with an empty statement, so the next line always runs.
- **Role:** context

**16. `flag_search_loop` &rarr; `LoopIgnoresCodeBefore`** (error)

- **Exact edge logic (the wrong rule):** Initializes the flag before the loop so that the loop condition is already false, and the loop body never runs.
- **Twin logic (the right rule):** A while loop tests its condition before the first pass: if the values set before the loop make the condition false, the body never runs.
- **Role:** context

**17. `for_loop` &rarr; `SemicolonAfterIfHeader`** (error)

- **Exact edge logic (the wrong rule):** if (x &gt; 0); System.out.println("positive"); prints only for positive x.
- **Twin logic (the right rule):** The ; ends the if with an empty statement, so the next line always runs.
- **Role:** context

**18. `if_statement` &rarr; `SemicolonAfterIfHeader`** (error)

- **Exact edge logic (the wrong rule):** if (x &gt; 0); System.out.println("positive"); prints only for positive x.
- **Twin logic (the right rule):** The ; ends the if with an empty statement, so the next line always runs.
- **Role:** primary

**19. `loop_scope` &rarr; `AccumulatorDeclaredInLoop`** (error)

- **Exact edge logic (the wrong rule):** Declaring sum inside the loop body keeps a running total across passes.
- **Twin logic (the right rule):** The accumulator must be declared and initialised before the loop.
- **Role:** primary

**20. `while_loop` &rarr; `LoopIgnoresCodeBefore`** (error)

- **Exact edge logic (the wrong rule):** Initializes the flag before the loop so that the loop condition is already false, and the loop body never runs.
- **Twin logic (the right rule):** A while loop tests its condition before the first pass: if the values set before the loop make the condition false, the body never runs.
- **Role:** primary

**21. `while_loop` &rarr; `SemicolonAfterIfHeader`** (error)

- **Exact edge logic (the wrong rule):** if (x &gt; 0); System.out.println("positive"); prints only for positive x.
- **Twin logic (the right rule):** The ; ends the if with an empty statement, so the next line always runs.
- **Role:** context

**22. `logical_error` &rarr; `logical_error@L0`** (has_level)

- **Exact edge logic:** logical error -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (3 ways).
  - **[0] everyday\_reading** (rule type E, folk-meaning rule): Everyday reading: the computer understands what you meant and will complain if the program is wrong. Java rule: a program with a logic error compiles and runs without any message and does exactly what the code says, which differs from what was intended.
  - **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `CompilesMeansWorks`: wrong rule: Code that compiles is code that works. Right rule: Code that compiles and runs can still compute the wrong result (a logic error).
  - **[2] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `CompilesMeansWorks`: Applies the 'computer does exactly what is written' rule unevenly: traces some lines literally but reads the intended meaning into the faulty line, and so does not see the bug. (here mixing in: "Code that compiles is code that works")

**23. `logical_error` &rarr; `logical_error@L1`** (has_level)

- **Exact edge logic:** logical error -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).
  - **[0] names\_the\_element** (rule type N, identity rule): A logic error is an error that makes a program do something other than what the programmer intended, without any compiler or run-time message.
  - **[1] states\_the\_rule** (rule type S, declarative rule): If a program has a logic error, it will compile and run without generating error messages, but it will not do the right thing; the compiler and JVM cannot detect it since they don't know what the right thing is.

**24. `logical_error` &rarr; `logical_error@L2`** (has_level)

- **Exact edge logic:** logical error -&gt; L2 (Multistructural): the answer applies the rules of logical error to every part of the code, in order (3 ways).
  - **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): Execution proceeds normally, statement by statement; the faulty statement executes without complaint and passes a wrong value or output onward.
  - **[1] output\_prediction** (rule type OP, evaluation / result rule): Result is a normal-looking but wrong output, e.g. println("Hello, "); println("World!"); prints two lines where one was intended.
  - **[2] one\_step\_execution** (rule type OS, state-transition rule): Each step makes a legal state change (e.g. an empty statement after if, or resetting sum each pass), but not the intended one.

**25. `logical_error` &rarr; `logical_error@L3`** (has_level)

- **Exact edge logic:** logical error -&gt; L3 (Relational): the answer relates the parts (4 ways).
  - **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): A logic error is seen only by running the program and comparing its output with the intended output.
  - **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): A run-time error stops the program with an exception; a logic error lets it finish with wrong output.
  - **[2] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Debugging is mostly the search for logic errors, which give wrong output without any message.
  - **[3] purpose\_of\_the\_whole** (rule type P, plan / role rule): Purpose (of the category): name the errors that only testing against the intended behaviour can find, so they are found by tracing, test cases and added print statements.

**26. `logical_error` &rarr; `logical_error@L4`** (has_level)

- **Exact edge logic:** logical error -&gt; L4 (Extended abstract): the answer reasons beyond the given code (6 ways).
  - **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `CompilesMeansWorks`: A logic error survives recompiling and rerunning unchanged; changing input may hide or reveal it; fixing it changes output only on the inputs it affected.
  - **[1] diagnose\_an\_error** (rule type D, error rule): rule broken: A ; right after if (...) is an empty statement that forms the whole if body. Kind: silent logic error. Trigger class: if (x &gt; 0); System.out.println("positive"); prints for every x
  - **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: The accumulator must be declared and initialized before the loop. Kind: silent logic error. Trigger class: int sum = 0; written inside the loop body: sum is reset each pass (and is out of scope after the loop)
  - **[3] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Suspect a logic error when the program compiles and runs to the end but the output is wrong for some inputs; locate it by hand tracing, minimal test cases and print statements, since tools give no message.
  - **[4] diagnose\_an\_error** (rule type D, error rule): rule broken: A while loop tests its condition before the first pass. Kind: silent logic error. Trigger class: values set before the loop already make the condition false, so the body never runs
  - **[5] diagnose\_an\_error** (rule type D, error rule): rule broken: print vs println decides line breaks. Kind: silent logic error. Trigger class: println used where print was meant (or the reverse)

**27. `topic1.1.c` &rarr; `logical_error`** (contains)

- topic `topic1.1.c` contains `logical_error`

**28. `topic1.1.c` &rarr; `compile_time_error`** (contains)

- topic `topic1.1.c` contains `compile_time_error`

**29. `topic1.1.c` &rarr; `reading_error_messages`** (contains)

- topic `topic1.1.c` contains `reading_error_messages`

**30. `topic1.1.c` &rarr; `run_time_error`** (contains)

- topic `topic1.1.c` contains `run_time_error`
