# program_text (`program_text`)

the source file; class name must match the filename

Section 1.1 Your First Program, topic 1.1.a Programming in Java: create, compile, execute.

![The knowledge graph around program_text](program_text.png)

## At a glance

- **Needs first:** nothing
- **Leads to:** `class_declaration`, `comment`, `compile`
- **Learned alongside:** nothing
- **Misconceptions:** `ClassNameMatchesFile`, `ComputerFillsInIntent`
- **Errors:** none
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 18 edges around this concept, each explained in the graph's own words.

## What it needs first (0)

A prerequisite edge means the other concept has to be understood before `program_text`.

No prerequisite edge leads into this concept.

## What it leads to (3)

These concepts need `program_text` first.

### `program_text` comes before `class_declaration`

*public class Name { ... } -- the outer container*

The source file Name.java holds the public class, and that class must be named Name.

- **Grounding:** book passage
- **How `program_text` combines with `class_declaration`:** The name after 'public class' constrains the file name: public class Name must be in Name.java, or javac rejects it.
- **How `class_declaration` combines with `program_text`:** The name after 'class' must equal the file name without .java.

### `program_text` comes before `comment`

*// and /\* \*/ text that the compiler ignores*

Comments are part of the program text in Name.java but are ignored when it is compiled.

- **Grounding:** book passage
- **How `program_text` combines with `comment`:** Comments are part of the program text but are discarded when it is compiled: they may appear anywhere a whitespace may appear and never change Name.class's behaviour.
- **How `comment` combines with `program_text`:** Comments are part of the program text in Name.java but are dropped when it is compiled, so they cannot affect Name.class's behaviour.

### `program_text` comes before `compile`

*javac turns source into bytecode*

javac takes the program file Name.java as input and translates it into Name.class.

- **Grounding:** book passage
- **How `program_text` combines with `compile`:** javac takes the text file Name.java as input and produces Name.class; the text must be lexically and syntactically legal for any .class to be produced.
- **How `compile` combines with `program_text`:** javac takes the program text Name.java as input; its file name must match the public class name.

## Learned alongside (0)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

No parallel edge touches this concept.

## Misconceptions (2)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### ClassNameMatchesFile

- **Wrong rule:** class name and filename are independent
- **Right rule:** A public class Name must be saved in a file called Name.java.
- **Role of this concept:** context
- **Shows at level L0 as:** misconception: wrong rule: The class name and the file name are independent, so public class HelloWorld can be saved as hello.java or Program.java. Right rule: A public class Name must be saved in a file called exactly Name.java (same spelling and case).
- **Shows at level L0 as:** inconsistent trace: Applies the reading rule (LT for program\_text: the compiler reads the file Name.java character by character from top to bottom, ignoring comments and whitespace between tokens) unevenly: e.g. reads the code but also the comments as if they ran, or treats the file name as irrelevant on one pass and as the program name on another. (here mixing in: "class name and filename are independent")
- **Also an edge from `class_declaration`:** The class can have any name; the file name does not need to match it.

### ComputerFillsInIntent

- **Wrong rule:** The computer fills in omitted steps or values that the programmer meant, e.g. REPEAT 4 [FORWARD 30] draws a square without a turn command.
- **Right rule:** The computer executes only what the code states; every needed step and value must be written.
- **Role of this concept:** context
- **Shows at level L0 as:** misconception: wrong rule: The computer fills in steps or values the programmer meant but did not write. Right rule: The program text is all the computer has: it executes only what the code states, so every step and value must be written.
- **Also an edge from `algorithm_pseudocode`:** The computer fills in omitted steps or values that the programmer meant, e.g. REPEAT 4 [FORWARD 30] draws a square without a turn command.
- **Also an edge from `loop_body`:** The computer fills in omitted steps or values that the programmer meant, e.g. REPEAT 4 [FORWARD 30] draws a square without a turn command.
- **Also an edge from `statement`:** The computer fills in omitted steps or values that the programmer meant, e.g. REPEAT 4 [FORWARD 30] draws a square without a turn command.

## Errors (0)

An error edge states the rule that gets broken in a program, and the right rule.

The graph has no error edge from this concept.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for program text: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to program text agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

program text -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (4 ways).

- **everyday reading** (folk-meaning rule): Everyday reading: a 'program' is a document you can save under any name, like a letter or an essay, and a misspelt word does not stop a reader from understanding it. Java rule: the file must be named exactly after its public class plus .java (HelloWorld.java for public class HelloWorld), and every character, including case and punctuation, is significant to the compiler.
- **misconception** (wrong rule / right rule; shows `ClassNameMatchesFile`): wrong rule: The class name and the file name are independent, so public class HelloWorld can be saved as hello.java or Program.java. Right rule: A public class Name must be saved in a file called exactly Name.java (same spelling and case).
- **inconsistent trace** (uneven-application rule; shows `ClassNameMatchesFile`): Applies the reading rule (LT for program\_text: the compiler reads the file Name.java character by character from top to bottom, ignoring comments and whitespace between tokens) unevenly: e.g. reads the code but also the comments as if they ran, or treats the file name as irrelevant on one pass and as the program name on another. (here mixing in: "class name and filename are independent")
- **misconception** (wrong rule / right rule; shows `ComputerFillsInIntent`): wrong rule: The computer fills in steps or values the programmer meant but did not write. Right rule: The program text is all the computer has: it executes only what the code states, so every step and value must be written.

### L1: Unistructural / atom x text surface

L1 for program text: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

program text -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

- **names the element** (identity rule): Program text (source code) is the sequence of characters typed into a text file Name.java that holds one Java program; S&amp;W call it code.
- **states the rule** (declarative rule): A Java program is a sequence of characters stored in a file with a .java extension whose name matches the name after the word class on the first line (public class HelloWorld lives in HelloWorld.java).

### L2: Multistructural / block x execution / preoperational

L2 for program text: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

program text -&gt; L2 (Multistructural): the answer applies the rules of program text to every part of the code, in order (3 ways).

- **line by line trace** (operational sequencing rule): Development order: (1) edit Name.java, (2) javac Name.java translates the whole text, (3) java Name runs it. Within the text, the compiler reads tokens in order; at run time main's statements execute top to bottom.
- **output prediction** (evaluation / result rule): The program text itself produces no output; its result is the file Name.class produced by javac when the text is legal, and the program's output appears only when java Name runs it.
- **one step execution** (state-transition rule): One edit-save of the text changes only the file Name.java; the existing Name.class (and so the behaviour of java Name) does not change until javac is run again.

### L3: Relational / relations x function (concrete operational begins)

L3 for program text: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

program text -&gt; L3 (Relational): the answer relates the parts (4 ways).

- **relation to neighbour** (composition rule (with a neighbour)): The name after 'public class' constrains the file name: public class Name must be in Name.java, or javac rejects it.
- **relation to neighbour** (composition rule (with a neighbour)): Comments are part of the program text but are discarded when it is compiled: they may appear anywhere a whitespace may appear and never change Name.class's behaviour.
- **relation to neighbour** (composition rule (with a neighbour)): javac takes the text file Name.java as input and produces Name.class; the text must be lexically and syntactically legal for any .class to be produced.
- **purpose of the whole** (plan / role rule): The program text is the human-readable statement of a computation: it records exactly what the computer must do so that it can be compiled, run, read and modified (copy HelloWorld.java, rename the class, replace the statements).

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for program text: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

program text -&gt; L4 (Extended abstract): the answer reasons beyond the given code (4 ways).

- **predict a change** (conservation rule; shows `ClassNameMatchesFile`): Renaming the class without renaming the file (or vice versa) breaks compilation; changing whitespace between tokens or editing comments keeps the behaviour unchanged; changing any character inside quotes changes the output.
- **transfer to a new program** (applicability rule): Use one source file per program (one public class per Name.java) and edit the text rather than the .class file; do not expect the text to carry meaning that is not written in it.
- **diagnose an error** (error rule): rule broken: public class Name must be in Name.java. Kind: compile-time. Trigger class: file name and public class name differ in spelling or case (class HelloWorld saved as Hello.java or helloworld.java)
- **diagnose an error** (error rule): rule broken: java Name runs a class, not a file name. Kind: launch error. Trigger class: typing java UseArgument.java Bob or a class name whose .class does not exist

## Same topic

`program_text` belongs to the topic **Programming in Java: create, compile, execute** (`topic1.1.a`). The topic also contains: `compile`, `incremental_development`, `run`.

## Rules of the concept (17)

- **folk-meaning rule:** Everyday reading: a 'program' is a document you can save under any name, like a letter or an essay, and a misspelt word does not stop a reader from understanding it. Java rule: the file must be named exactly after its public class plus .java (HelloWorld.java for public class HelloWorld), and every character, including case and punctuation, is significant to the compiler.
- **wrong rule / right rule:** ClassNameMatchesFile: wrong: The class name and the file name are independent, so public class HelloWorld can be saved as hello.java or Program.java. \| right: A public class Name must be saved in a file called exactly Name.java (same spelling and case).
- **wrong rule / right rule:** ComputerFillsInIntent: wrong: The computer fills in steps or values the programmer meant but did not write. \| right: The program text is all the computer has: it executes only what the code states, so every step and value must be written.
- **uneven-application rule:** Applies the reading rule (LT for program\_text: the compiler reads the file Name.java character by character from top to bottom, ignoring comments and whitespace between tokens) unevenly: e.g. reads the code but also the comments as if they ran, or treats the file name as irrelevant on one pass and as the program name on another.
- **identity rule:** Program text (source code) is the sequence of characters typed into a text file Name.java that holds one Java program; S&amp;W call it code.
- **declarative rule:** A Java program is a sequence of characters stored in a file with a .java extension whose name matches the name after the word class on the first line (public class HelloWorld lives in HelloWorld.java).
- **operational sequencing rule:** Development order: (1) edit Name.java, (2) javac Name.java translates the whole text, (3) java Name runs it. Within the text, the compiler reads tokens in order; at run time main's statements execute top to bottom.
- **evaluation / result rule:** The program text itself produces no output; its result is the file Name.class produced by javac when the text is legal, and the program's output appears only when java Name runs it.
- **state-transition rule:** One edit-save of the text changes only the file Name.java; the existing Name.class (and so the behaviour of java Name) does not change until javac is run again.
- **composition rule (with a neighbour):** with class\_declaration: The name after 'public class' constrains the file name: public class Name must be in Name.java, or javac rejects it.
- **composition rule (with a neighbour):** with comment: Comments are part of the program text but are discarded when it is compiled: they may appear anywhere a whitespace may appear and never change Name.class's behaviour.
- **composition rule (with a neighbour):** with compile: javac takes the text file Name.java as input and produces Name.class; the text must be lexically and syntactically legal for any .class to be produced.
- **plan / role rule:** The program text is the human-readable statement of a computation: it records exactly what the computer must do so that it can be compiled, run, read and modified (copy HelloWorld.java, rename the class, replace the statements).
- **conservation rule:** Renaming the class without renaming the file (or vice versa) breaks compilation; changing whitespace between tokens or editing comments keeps the behaviour unchanged; changing any character inside quotes changes the output.
- **error rule:** rule broken: public class Name must be in Name.java (compile-time)
- **error rule:** rule broken: java Name runs a class, not a file name (launch error)
- **applicability rule:** Use one source file per program (one public class per Name.java) and edit the text rather than the .class file; do not expect the text to carry meaning that is not written in it.

## The whole prerequisite chain

- **Everything it builds on (0):** nothing
- **Everything that builds on it (45):** `accumulator_pattern`, `algorithm_pseudocode`, `args_length`, `black_box_model`, `block`, `class_declaration`, `command_line_args`, `comment`, `compile`, `compile_time_error`, `compound_assignment`, `conditional_operator`, `control_flow`, `dangling_else`, `data_driven_code`, `debugging`, `else_if_chain`, `empty_statement`, `explicit_cast`, `filter`, `flowchart`, `if_else_statement`, `if_statement`, `incremental_development`, `logical_error`, `main_method`, `math_random`, `monte_carlo_simulation`, `nested_conditionals`, `parsing`, `piping`, `print`, `printing_array_reference`, `println`, `program_layout`, `reading_error_messages`, `redirection`, `run`, `run_time_error`, `sentinel_loop`, `statement`, `switch_statement`, `testing`, `type_conversion`, `widening_conversion`
