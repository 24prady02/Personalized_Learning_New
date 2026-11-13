# class_declaration (`class_declaration`)

public class Name { ... } -- the outer container

Section 1.1 Your First Program, topic 1.1.b Understanding a program (HelloWorld).

![The knowledge graph around class_declaration](class_declaration.png)

## At a glance

- **Needs first:** `program_text`
- **Leads to:** `main_method`
- **Learned alongside:** nothing
- **Misconceptions:** `ClassNameMatchesFile`
- **Errors:** `MissingKeyword`, `UnbalancedBraces`
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 23 edges around this concept, each explained in the graph's own words.

## What it needs first (1)

A prerequisite edge means the other concept has to be understood before `class_declaration`.

### `program_text` comes before `class_declaration`

*the source file; class name must match the filename*

The source file Name.java holds the public class, and that class must be named Name.

- **Grounding:** book passage
- **How `class_declaration` combines with `program_text`:** The name after 'class' must equal the file name without .java.
- **How `program_text` combines with `class_declaration`:** The name after 'public class' constrains the file name: public class Name must be in Name.java, or javac rejects it.

## What it leads to (1)

These concepts need `class_declaration` first.

### `class_declaration` comes before `main_method`

*public static void main(String[] args) -- entry point*

main is written inside the class's braces, so java Name looks inside the class Name to find main.

- **Grounding:** book passage
- **How `class_declaration` combines with `main_method`:** main must be declared inside the class's braces; java Name looks only inside class Name for main.
- **How `main_method` combines with `class_declaration`:** main is declared inside the class's braces; java Name looks in class Name for main.

## Learned alongside (0)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

No parallel edge touches this concept.

## Misconceptions (1)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### ClassNameMatchesFile

- **Wrong rule:** The class can have any name; the file name does not need to match it.
- **Right rule:** A public class Name must be saved in a file called Name.java.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: The class name and the file name are independent. Right rule: public class Name must be saved in a file named Name.java.
- **Shows at level L0 as:** inconsistent trace: Applies the containment rule unevenly: treats the class's closing brace as the end of main on one trace, or looks for main outside the class on another; the class body is everything between the outermost { and }. (here mixing in: "class name and filename are independent")
- **Also an edge from `program_text`:** class name and filename are independent

## Errors (2)

An error edge states the rule that gets broken in a program, and the right rule.

### MissingKeyword

- **Wrong rule:** Leaves out a required keyword such as static or class.
- **Right rule:** public class Name and public static void main(String[] args) need their keywords, which are required; omitting or misspelling one is an error, usually caught by the compiler as a syntax error.
- **Role of this concept:** context
- **Also an edge from `main_method`:** Leaves out a required keyword such as static or class.

### UnbalancedBraces

- **Wrong rule:** A missing { or } is harmless.
- **Right rule:** Every { must be matched by a } so the class body and the method body are well formed.
- **Role of this concept:** context
- **Also an edge from `block`:** A missing { or } is harmless.
- **Also an edge from `compile_time_error`:** A missing { or } is harmless.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for class declaration: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to class declaration agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

class declaration -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (3 ways).

- **everyday reading** (folk-meaning rule): Everyday meaning: a 'class' is a group of students or a category, and 'public' means open to everyone. Java rule: public class Name { ... } declares the named unit that holds the program's methods; for now S&amp;W say 'class' means 'program'.
- **misconception** (wrong rule / right rule; shows `ClassNameMatchesFile`): wrong rule: The class name and the file name are independent. Right rule: public class Name must be saved in a file named Name.java.
- **inconsistent trace** (uneven-application rule; shows `ClassNameMatchesFile`): Applies the containment rule unevenly: treats the class's closing brace as the end of main on one trace, or looks for main outside the class on another; the class body is everything between the outermost { and }. (here mixing in: "class name and filename are independent")

### L1: Unistructural / atom x text surface

L1 for class declaration: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

class declaration -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

- **names the element** (identity rule): A class declaration (public class Name { ... }) is the outer container of a Java program; in Chapter 1 each program is a single class with a single method main().
- **states the rule** (declarative rule): A program is written as public class Name { &lt;method declarations&gt; }; the outermost braces contain the class definition and the inner braces contain the method definitions, and the keywords public and class are required.

### L2: Multistructural / block x execution / preoperational

L2 for class declaration: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

class declaration -&gt; L2 (Multistructural): the answer applies the rules of class declaration to every part of the code, in order (3 ways).

- **line by line trace** (operational sequencing rule): The class declaration itself does not execute: java Name looks up the class Name and calls its main(); the class is just the container that is searched.
- **output prediction** (evaluation / result rule): A class declaration produces no output; compiling it produces the file Name.class.
- **one step execution** (state-transition rule): Declaring the class changes no variable at run time; it only defines the name (Name) that javac uses for Name.class and that java Name uses to find main.

### L3: Relational / relations x function (concrete operational begins)

L3 for class declaration: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

class declaration -&gt; L3 (Relational): the answer relates the parts (3 ways).

- **relation to neighbour** (composition rule (with a neighbour)): The name after 'class' must equal the file name without .java.
- **relation to neighbour** (composition rule (with a neighbour)): main must be declared inside the class's braces; java Name looks only inside class Name for main.
- **purpose of the whole** (plan / role rule): Purpose: package and name a program so it can be compiled and run by name; copying HelloWorld.java and replacing the name on the first line is how a new program is started.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for class declaration: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

class declaration -&gt; L4 (Extended abstract): the answer reasons beyond the given code (5 ways).

- **predict a change** (conservation rule; shows `ClassNameMatchesFile`): Renaming the class requires renaming the file (and the java command) to keep it compiling and runnable; moving main outside the class braces breaks compilation.
- **diagnose an error** (error rule): rule broken: public class Name needs the keyword class (and correct spelling). Kind: compile-time. Trigger class: omitting or misspelling class (or public) on the first line
- **transfer to a new program** (applicability rule): In Chapter 1 every program is exactly one public class containing main; a separate class (and file) is needed for each separate program. Multiple classes and methods come only in Section 2.1.
- **diagnose an error** (error rule): rule broken: Every { must be matched by a }. Kind: compile-time. Trigger class: a missing or extra brace around the class or method body
- **diagnose an error** (error rule): rule broken: A public class must be in a file of the same name. Kind: compile-time. Trigger class: class name differs from file name

## Same topic

`class_declaration` belongs to the topic **Understanding a program (HelloWorld)** (`topic1.1.b`). The topic also contains: `block`, `comment`, `main_method`, `print`, `println`, `program_layout`, `statement`, `string_literal`.

## Rules of the concept (16)

- **folk-meaning rule:** Everyday meaning: a 'class' is a group of students or a category, and 'public' means open to everyone. Java rule: public class Name { ... } declares the named unit that holds the program's methods; for now S&amp;W say 'class' means 'program'.
- **wrong rule / right rule:** ClassNameMatchesFile: wrong: The class name and the file name are independent. \| right: public class Name must be saved in a file named Name.java.
- **uneven-application rule:** Applies the containment rule unevenly: treats the class's closing brace as the end of main on one trace, or looks for main outside the class on another; the class body is everything between the outermost { and }.
- **identity rule:** A class declaration (public class Name { ... }) is the outer container of a Java program; in Chapter 1 each program is a single class with a single method main().
- **declarative rule:** A program is written as public class Name { &lt;method declarations&gt; }; the outermost braces contain the class definition and the inner braces contain the method definitions, and the keywords public and class are required.
- **operational sequencing rule:** The class declaration itself does not execute: java Name looks up the class Name and calls its main(); the class is just the container that is searched.
- **evaluation / result rule:** A class declaration produces no output; compiling it produces the file Name.class.
- **state-transition rule:** Declaring the class changes no variable at run time; it only defines the name (Name) that javac uses for Name.class and that java Name uses to find main.
- **composition rule (with a neighbour):** with program\_text: The name after 'class' must equal the file name without .java.
- **composition rule (with a neighbour):** with main\_method: main must be declared inside the class's braces; java Name looks only inside class Name for main.
- **plan / role rule:** Purpose: package and name a program so it can be compiled and run by name; copying HelloWorld.java and replacing the name on the first line is how a new program is started.
- **conservation rule:** Renaming the class requires renaming the file (and the java command) to keep it compiling and runnable; moving main outside the class braces breaks compilation.
- **error rule:** rule broken: public class Name needs the keyword class (and correct spelling) (compile-time)
- **error rule:** rule broken: Every { must be matched by a } (compile-time)
- **error rule:** rule broken: A public class must be in a file of the same name (compile-time)
- **applicability rule:** In Chapter 1 every program is exactly one public class containing main; a separate class (and file) is needed for each separate program. Multiple classes and methods come only in Section 2.1.

## The whole prerequisite chain

- **Everything it builds on (1):** `program_text`
- **Everything that builds on it (32):** `accumulator_pattern`, `algorithm_pseudocode`, `args_length`, `black_box_model`, `block`, `command_line_args`, `compound_assignment`, `conditional_operator`, `control_flow`, `dangling_else`, `debugging`, `else_if_chain`, `empty_statement`, `explicit_cast`, `flowchart`, `if_else_statement`, `if_statement`, `logical_error`, `main_method`, `math_random`, `monte_carlo_simulation`, `nested_conditionals`, `parsing`, `print`, `printing_array_reference`, `println`, `program_layout`, `sentinel_loop`, `statement`, `switch_statement`, `type_conversion`, `widening_conversion`
