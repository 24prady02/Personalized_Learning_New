# compile (`compile`)

javac turns source into bytecode

Section 1.1 Your First Program, topic 1.1.a Programming in Java: create, compile, execute.

![The knowledge graph around compile](compile.png)

## At a glance

- **Needs first:** `program_text`
- **Leads to:** `compile_time_error`, `run`
- **Learned alongside:** nothing
- **Misconceptions:** `CompileRunsProgram`, `CompilesMeansWorks`
- **Errors:** none
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 19 edges around this concept, each explained in the graph's own words.

## What it needs first (1)

A prerequisite edge means the other concept has to be understood before `compile`.

### `program_text` comes before `compile`

*the source file; class name must match the filename*

javac takes the program file Name.java as input and translates it into Name.class.

- **Grounding:** book passage
- **How `compile` combines with `program_text`:** javac takes the program text Name.java as input; its file name must match the public class name.
- **How `program_text` combines with `compile`:** javac takes the text file Name.java as input and produces Name.class; the text must be lexically and syntactically legal for any .class to be produced.

## What it leads to (2)

These concepts need `compile` first.

### `compile` comes before `compile_time_error`

*an error javac reports before the program can run (syntax, types)*

A compile-time error is reported while javac compiles Name.java, so no Name.class is produced.

- **Grounding:** book passage
- **How `compile` combines with `compile_time_error`:** A compile-time error stops the translation, so no Name.class is produced and there is nothing new to run.
- **How `compile_time_error` combines with `compile`:** A compile-time error is reported while javac compiles Name.java, so no new Name.class is produced.

### `compile` comes before `run`

*java executes main in the JVM*

java Name runs the Name.class file that javac produced, so compiling must succeed before the program can run.

- **Grounding:** book passage
- **How `compile` combines with `run`:** java Name loads the Name.class made by javac, so a successful compile must come before running, and edits take effect only after recompiling.
- **How `run` combines with `compile`:** java Name runs the Name.class that javac produced, so compiling must succeed first; the run reflects the source as of the last successful compile.

## Learned alongside (0)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

No parallel edge touches this concept.

## Misconceptions (2)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### CompileRunsProgram

- **Wrong rule:** If javac Name.java finishes without errors, the program already works and has run.
- **Right rule:** javac only translates Name.java into Name.class; the program runs only with java Name, and run-time errors can still appear then.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: Compiling also executes the program. Right rule: javac only translates Name.java into Name.class; the program runs only with java Name, and run-time errors can appear then.
- **Shows at level L0 as:** inconsistent trace: Applies the compile rule (LT) unevenly: expects output after javac on one try but not another, or runs java Name after a failed compile as if the old Name.class reflected the new edits. (here mixing in: "compiling also executes the program")
- **Also an edge from `run`:** If javac Name.java finishes without errors, the program already works and has run.

### CompilesMeansWorks

- **Wrong rule:** Code that compiles is code that works.
- **Right rule:** Code that compiles can still have run-time and logical errors.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: Code that compiles is code that works. Right rule: Code that compiles can still have run-time errors and logic errors.
- **Also an edge from `compile_time_error`:** Code that compiles is code that works.
- **Also an edge from `logical_error`:** Code that compiles is code that works.
- **Also an edge from `run_time_error`:** Code that compiles is code that works.
- **Also an edge from `testing`:** Code that compiles is code that works.

## Errors (0)

An error edge states the rule that gets broken in a program, and the right rule.

The graph has no error edge from this concept.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for compile: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to compile agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

compile -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (4 ways).

- **everyday reading** (folk-meaning rule): Everyday meaning: to 'compile' is to gather or put together (compile a list), and 'running' a program sounds like it starts on its own. Java rule: compiling with javac only translates Name.java into bytecode in Name.class; nothing executes until java Name is typed.
- **misconception** (wrong rule / right rule; shows `CompileRunsProgram`): wrong rule: Compiling also executes the program. Right rule: javac only translates Name.java into Name.class; the program runs only with java Name, and run-time errors can appear then.
- **misconception** (wrong rule / right rule; shows `CompilesMeansWorks`): wrong rule: Code that compiles is code that works. Right rule: Code that compiles can still have run-time errors and logic errors.
- **inconsistent trace** (uneven-application rule; shows `CompileRunsProgram`): Applies the compile rule (LT) unevenly: expects output after javac on one try but not another, or runs java Name after a failed compile as if the old Name.class reflected the new edits. (here mixing in: "compiling also executes the program")

### L1: Unistructural / atom x text surface

L1 for compile: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

compile -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

- **names the element** (identity rule): Compiling is translating the whole Java source file into a lower-level form (Java bytecode) before execution; javac is the Java compiler.
- **states the rule** (declarative rule): javac Name.java takes the file Name.java as input and, if there are no compile-time errors, produces Name.class (the bytecode version) with the same name.

### L2: Multistructural / block x execution / preoperational

L2 for compile: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

compile -&gt; L2 (Multistructural): the answer applies the rules of compile to every part of the code, in order (3 ways).

- **line by line trace** (operational sequencing rule): The compiler first reads (parses) the entire file, then translates it; it does all this before the program starts running, and only if no errors were found does it write Name.class.
- **output prediction** (evaluation / result rule): Result of javac Name.java: either a new file Name.class and no terminal output, or a list of error messages (file:line: message, then 'N errors') and no Name.class.
- **one step execution** (state-transition rule): One compile changes only the file system: it creates or overwrites Name.class; it changes no program variable and prints no program output.

### L3: Relational / relations x function (concrete operational begins)

L3 for compile: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

compile -&gt; L3 (Relational): the answer relates the parts (4 ways).

- **relation to neighbour** (composition rule (with a neighbour)): java Name loads the Name.class made by javac, so a successful compile must come before running, and edits take effect only after recompiling.
- **relation to neighbour** (composition rule (with a neighbour)): A compile-time error stops the translation, so no Name.class is produced and there is nothing new to run.
- **relation to neighbour** (composition rule (with a neighbour)): javac takes the program text Name.java as input; its file name must match the public class name.
- **purpose of the whole** (plan / role rule): Purpose: check the program against the language rules and turn it into a form the JVM can execute, once, so it can then be run repeatedly with different inputs.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for compile: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

compile -&gt; L4 (Extended abstract): the answer reasons beyond the given code (4 ways).

- **predict a change** (conservation rule; shows `CompileRunsProgram`): Recompiling the same unchanged source gives the same Name.class; any edit to the source is invisible to java Name until recompiled; adding or deleting comments or whitespace changes nothing the program does.
- **transfer to a new program** (applicability rule): Compile after every change before running, and compile often while making small changes, so each error is found close to its cause; compiling cannot find run-time or logic errors.
- **diagnose an error** (error rule): rule broken: Source must obey Java's syntax and type rules. Kind: compile-time. Trigger class: any syntax error (missing ; or brace, misspelled keyword) or type error in Name.java
- **diagnose an error** (error rule): rule broken: javac needs the .java file name. Kind: launch error. Trigger class: typing javac Name (no .java) or the wrong file name / directory

## Same topic

`compile` belongs to the topic **Programming in Java: create, compile, execute** (`topic1.1.a`). The topic also contains: `incremental_development`, `program_text`, `run`.

## Rules of the concept (17)

- **folk-meaning rule:** Everyday meaning: to 'compile' is to gather or put together (compile a list), and 'running' a program sounds like it starts on its own. Java rule: compiling with javac only translates Name.java into bytecode in Name.class; nothing executes until java Name is typed.
- **wrong rule / right rule:** CompileRunsProgram: wrong: Compiling also executes the program. \| right: javac only translates Name.java into Name.class; the program runs only with java Name, and run-time errors can appear then.
- **wrong rule / right rule:** CompilesMeansWorks: wrong: Code that compiles is code that works. \| right: Code that compiles can still have run-time errors and logic errors.
- **uneven-application rule:** Applies the compile rule (LT) unevenly: expects output after javac on one try but not another, or runs java Name after a failed compile as if the old Name.class reflected the new edits.
- **identity rule:** Compiling is translating the whole Java source file into a lower-level form (Java bytecode) before execution; javac is the Java compiler.
- **declarative rule:** javac Name.java takes the file Name.java as input and, if there are no compile-time errors, produces Name.class (the bytecode version) with the same name.
- **operational sequencing rule:** The compiler first reads (parses) the entire file, then translates it; it does all this before the program starts running, and only if no errors were found does it write Name.class.
- **evaluation / result rule:** Result of javac Name.java: either a new file Name.class and no terminal output, or a list of error messages (file:line: message, then 'N errors') and no Name.class.
- **state-transition rule:** One compile changes only the file system: it creates or overwrites Name.class; it changes no program variable and prints no program output.
- **composition rule (with a neighbour):** with run: java Name loads the Name.class made by javac, so a successful compile must come before running, and edits take effect only after recompiling.
- **composition rule (with a neighbour):** with compile\_time\_error: A compile-time error stops the translation, so no Name.class is produced and there is nothing new to run.
- **composition rule (with a neighbour):** with program\_text: javac takes the program text Name.java as input; its file name must match the public class name.
- **plan / role rule:** Purpose: check the program against the language rules and turn it into a form the JVM can execute, once, so it can then be run repeatedly with different inputs.
- **conservation rule:** Recompiling the same unchanged source gives the same Name.class; any edit to the source is invisible to java Name until recompiled; adding or deleting comments or whitespace changes nothing the program does.
- **error rule:** rule broken: Source must obey Java's syntax and type rules (compile-time)
- **error rule:** rule broken: javac needs the .java file name (launch error)
- **applicability rule:** Compile after every change before running, and compile often while making small changes, so each error is found close to its cause; compiling cannot find run-time or logic errors.

## The whole prerequisite chain

- **Everything it builds on (1):** `program_text`
- **Everything that builds on it (12):** `compile_time_error`, `data_driven_code`, `debugging`, `filter`, `incremental_development`, `logical_error`, `piping`, `reading_error_messages`, `redirection`, `run`, `run_time_error`, `testing`
