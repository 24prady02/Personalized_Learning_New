# run (`run`)

java executes main in the JVM

Section 1.1 Your First Program, topic 1.1.a Programming in Java: create, compile, execute.

![The knowledge graph around run](run.png)

## At a glance

- **Needs first:** `compile`
- **Leads to:** `incremental_development`, `logical_error`, `piping`, `redirection`, `run_time_error`, `testing`
- **Learned alongside:** nothing
- **Misconceptions:** `CompileRunsProgram`
- **Errors:** `AudioProgramHangs`
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 20 edges around this concept, each explained in the graph's own words.

## What it needs first (1)

A prerequisite edge means the other concept has to be understood before `run`.

### `compile` comes before `run`

*javac turns source into bytecode*

java Name runs the Name.class file that javac produced, so compiling must succeed before the program can run.

- **Grounding:** book passage
- **How `run` combines with `compile`:** java Name runs the Name.class that javac produced, so compiling must succeed first; the run reflects the source as of the last successful compile.
- **How `compile` combines with `run`:** java Name loads the Name.class made by javac, so a successful compile must come before running, and edits take effect only after recompiling.

## What it leads to (6)

These concepts need `run` first.

### `run` comes before `incremental_development`

*building a program in small steps from a version that works, compiling and testing after each change*

Each small step is run and checked before the next one is added.

- **Grounding:** book passage
- **How `incremental_development` combines with `run`:** Running after each step shows at once whether the new lines do what was intended.

### `run` comes before `logical_error`

*the program runs but computes the wrong result*

A logical error is seen only by running the program and comparing its output with the intended output.

- **Grounding:** book passage
- **How `run` combines with `logical_error`:** A logic error is seen only by running the program and comparing its output with the intended output.
- **How `logical_error` combines with `run`:** A logic error is seen only by running the program and comparing its output with the intended output.

### `run` comes before `piping`

*\| connects one program's output to another's input*

Piping joins the commands that run two programs, so one program's output becomes the other's input.

- **Grounding:** book passage

### `run` comes before `redirection`

*&lt; / &gt; send a file in/out as standard input/output*

Redirection is written on the command that runs a program, with &lt; or &gt;.

- **Grounding:** book passage

### `run` comes before `run_time_error`

*an error raised while the program executes (e.g. ArrayIndexOutOfBounds, NumberFormatException)*

A run-time error appears only while java Name executes, after compiling has succeeded.

- **Grounding:** book passage
- **How `run` combines with `run_time_error`:** A run-time error appears only while java Name executes; the JVM stops the program and prints the exception.
- **How `run_time_error` combines with `run`:** A run-time error appears only while java Name executes, after compiling has succeeded.

### `run` comes before `testing`

*running a program on chosen inputs, including boundary and unusual ones, and comparing the output with what it should be*

A program is tested by running it on chosen inputs and comparing what it prints with what it should print.

- **Grounding:** book passage
- **How `testing` combines with `run`:** Each test is one run with one input: java Name followed by the test arguments (or with input redirected from a file).

## Learned alongside (0)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

No parallel edge touches this concept.

## Misconceptions (1)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### CompileRunsProgram

- **Wrong rule:** If javac Name.java finishes without errors, the program already works and has run.
- **Right rule:** javac only translates Name.java into Name.class; the program runs only with java Name, and run-time errors can still appear then.
- **Role of this concept:** context
- **Shows at level L0 as:** misconception: wrong rule: Compiling also executes the program. Right rule: The program runs only when java Name is typed; javac only translates it.
- **Shows at level L0 as:** inconsistent trace: Applies the run rule (LT: main's statements execute in order, one by one, each once) unevenly: e.g. executes the print statements in written order on one trace but skips one or reorders them on another. (here mixing in: "compiling also executes the program")
- **Also an edge from `compile`:** If javac Name.java finishes without errors, the program already works and has run.

## Errors (1)

An error edge states the rule that gets broken in a program, and the right rule.

### AudioProgramHangs

- **Wrong rule:** Ends a StdAudio program with no System.exit(0), so the terminal hangs and needs &lt;ctrl-c&gt;.
- **Right rule:** In the book's setup, a program that uses StdAudio should end main() with System.exit(0).
- **Role of this concept:** context
- **Also an edge from `standard_audio`:** Ends a StdAudio program with no System.exit(0), so the terminal hangs and needs &lt;ctrl-c&gt;.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for run: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to run agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

run -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (3 ways).

- **everyday reading** (folk-meaning rule): Everyday meaning: 'run the program' as if the file ran itself, or the program 'looks at all of itself at once'. Java rule: java Name starts the JVM, which calls Name's main() and executes its statements one at a time, in order.
- **misconception** (wrong rule / right rule; shows `CompileRunsProgram`): wrong rule: Compiling also executes the program. Right rule: The program runs only when java Name is typed; javac only translates it.
- **inconsistent trace** (uneven-application rule; shows `CompileRunsProgram`): Applies the run rule (LT: main's statements execute in order, one by one, each once) unevenly: e.g. executes the print statements in written order on one trace but skips one or reorders them on another. (here mixing in: "compiling also executes the program")

### L1: Unistructural / atom x text surface

L1 for run: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

run -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

- **names the element** (identity rule): Running (executing) a program is launching it with java Name so that the Java Virtual Machine follows its instructions.
- **states the rule** (declarative rule): Typing java followed by a class name makes the system call the main() method defined in that class and execute its statements; java Name args... also passes the command-line arguments to main. The development cycle is the same in any environment (terminal or IDE): edit the .java file, compile it with javac, run it with java.

### L2: Multistructural / block x execution / preoperational

L2 for run: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

run -&gt; L2 (Multistructural): the answer applies the rules of run to every part of the code, in order (3 ways).

- **line by line trace** (operational sequencing rule): The JVM starts at the first statement of main and ends when it finishes the last statement; statements run one by one, in order, and control returns to the system when main finishes.
- **output prediction** (evaluation / result rule): The result of a run is what the program prints to the terminal (for java HelloWorld: Hello, World), or an exception message if a run-time error occurs.
- **one step execution** (state-transition rule): One execution step runs one statement of main, which changes the program state (a variable or the output) and passes control to the next statement.

### L3: Relational / relations x function (concrete operational begins)

L3 for run: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

run -&gt; L3 (Relational): the answer relates the parts (6 ways).

- **relation to neighbour** (composition rule (with a neighbour)): java Name runs the Name.class that javac produced, so compiling must succeed first; the run reflects the source as of the last successful compile.
- **relation to neighbour** (composition rule (with a neighbour)): A run-time error appears only while java Name executes; the JVM stops the program and prints the exception.
- **relation to neighbour** (composition rule (with a neighbour)): A logic error is seen only by running the program and comparing its output with the intended output.
- **relation to neighbour** (composition rule (with a neighbour)): A program is tested by running it on chosen inputs and comparing what it prints with what it should print.
- **relation to neighbour** (composition rule (with a neighbour)): Each small step is run and checked before the next one is added.
- **purpose of the whole** (plan / role rule): Purpose: make the computer carry out the program on particular inputs; running the same compiled program with different command-line arguments gives different results.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for run: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

run -&gt; L4 (Extended abstract): the answer reasons beyond the given code (5 ways).

- **predict a change** (conservation rule; shows `CompileRunsProgram`): Running again with the same arguments reproduces the same output (for programs without randomness or input); changing the arguments changes the output without recompiling; editing the source changes nothing until recompiled.
- **transfer to a new program** (applicability rule): Run the program to test it on chosen inputs and to see run-time and logic errors that compiling cannot find; adding print statements and rerunning is a simple way to check what is actually executing.
- **diagnose an error** (error rule): rule broken: In the book's setup a StdAudio program should end main() with System.exit(0). Kind: silent logic error. Trigger class: a program that uses StdAudio and finishes main without System.exit(0): the terminal hangs and needs &lt;ctrl-c&gt;
- **diagnose an error** (error rule): rule broken: Run only after a successful compile; java takes a class name. Kind: launch error. Trigger class: running java Name when Name.class is missing or stale, or typing java Name.java
- **diagnose an error** (error rule): rule broken: A required command-line argument must be typed. Kind: run-time exception. Trigger class: running a program that reads args[0] with no argument

## Same topic

`run` belongs to the topic **Programming in Java: create, compile, execute** (`topic1.1.a`). The topic also contains: `compile`, `incremental_development`, `program_text`.

## Rules of the concept (17)

- **folk-meaning rule:** Everyday meaning: 'run the program' as if the file ran itself, or the program 'looks at all of itself at once'. Java rule: java Name starts the JVM, which calls Name's main() and executes its statements one at a time, in order.
- **wrong rule / right rule:** CompileRunsProgram: wrong: Compiling also executes the program. \| right: The program runs only when java Name is typed; javac only translates it.
- **uneven-application rule:** Applies the run rule (LT: main's statements execute in order, one by one, each once) unevenly: e.g. executes the print statements in written order on one trace but skips one or reorders them on another.
- **identity rule:** Running (executing) a program is launching it with java Name so that the Java Virtual Machine follows its instructions.
- **declarative rule:** Typing java followed by a class name makes the system call the main() method defined in that class and execute its statements; java Name args... also passes the command-line arguments to main. The development cycle is the same in any environment (terminal or IDE): edit the .java file, compile it with javac, run it with java.
- **operational sequencing rule:** The JVM starts at the first statement of main and ends when it finishes the last statement; statements run one by one, in order, and control returns to the system when main finishes.
- **evaluation / result rule:** The result of a run is what the program prints to the terminal (for java HelloWorld: Hello, World), or an exception message if a run-time error occurs.
- **state-transition rule:** One execution step runs one statement of main, which changes the program state (a variable or the output) and passes control to the next statement.
- **composition rule (with a neighbour):** with compile: java Name runs the Name.class that javac produced, so compiling must succeed first; the run reflects the source as of the last successful compile.
- **composition rule (with a neighbour):** with run\_time\_error: A run-time error appears only while java Name executes; the JVM stops the program and prints the exception.
- **composition rule (with a neighbour):** with logical\_error: A logic error is seen only by running the program and comparing its output with the intended output.
- **plan / role rule:** Purpose: make the computer carry out the program on particular inputs; running the same compiled program with different command-line arguments gives different results.
- **conservation rule:** Running again with the same arguments reproduces the same output (for programs without randomness or input); changing the arguments changes the output without recompiling; editing the source changes nothing until recompiled.
- **error rule:** rule broken: In the book's setup a StdAudio program should end main() with System.exit(0) (silent logic error)
- **error rule:** rule broken: Run only after a successful compile; java takes a class name (launch error)
- **error rule:** rule broken: A required command-line argument must be typed (run-time exception)
- **applicability rule:** Run the program to test it on chosen inputs and to see run-time and logic errors that compiling cannot find; adding print statements and rerunning is a simple way to check what is actually executing.

## The whole prerequisite chain

- **Everything it builds on (2):** `compile`, `program_text`
- **Everything that builds on it (9):** `data_driven_code`, `debugging`, `filter`, `incremental_development`, `logical_error`, `piping`, `redirection`, `run_time_error`, `testing`
