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

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 23 edges around this concept. The edge logic, the wrong and right rules and the exact rules of the ways are copied word for word from the graph.

## To work on (0)

Nothing is missing for this concept.

## What it needs first (1)

A prerequisite edge means the other concept has to be understood before `class_declaration`.

### `program_text` comes before `class_declaration`

*the source file; class name must match the filename*

- **Edge:** `pre:program_text->class_declaration`
- **Exact edge logic:** The source file Name.java holds the public class, and that class must be named Name.
- **Grounding:** book\_passage
- **Composition rule (R) of `class_declaration` with `program_text`:** The name after 'class' must equal the file name without .java.
- **Composition rule (R) of `program_text` with `class_declaration`:** The name after 'public class' constrains the file name: public class Name must be in Name.java, or javac rejects it.

## What it leads to (1)

These concepts need `class_declaration` first.

### `class_declaration` comes before `main_method`

*public static void main(String[] args) -- entry point*

- **Edge:** `pre:class_declaration->main_method`
- **Exact edge logic:** main is written inside the class's braces, so java Name looks inside the class Name to find main.
- **Grounding:** book\_passage
- **Composition rule (R) of `class_declaration` with `main_method`:** main must be declared inside the class's braces; java Name looks only inside class Name for main.
- **Composition rule (R) of `main_method` with `class_declaration`:** main is declared inside the class's braces; java Name looks in class Name for main.

## Learned alongside (0)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

No parallel edge touches this concept.

## Misconceptions (1)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### ClassNameMatchesFile

- **Edge:** `class_declaration` &rarr; `ClassNameMatchesFile` (misconception)
- **Exact edge logic (the wrong rule):** The class can have any name; the file name does not need to match it.
- **Twin logic (the right rule):** A public class Name must be saved in a file called Name.java.
- **Wrong belief (on the node):** class name and filename are independent
- **Correct rule (on the node):** A public class Name must be saved in a file called Name.java.
- **Provenance:** textbook
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [1] misconception, exact rule:** wrong rule: The class name and the file name are independent. Right rule: public class Name must be saved in a file named Name.java.
- **L0 way [2] inconsistent\_trace, exact rule:** Applies the containment rule unevenly: treats the class's closing brace as the end of main on one trace, or looks for main outside the class on another; the class body is everything between the outermost { and }. (here mixing in: "class name and filename are independent")
- **Edge `program_text` &rarr; `ClassNameMatchesFile`, exact edge logic:** class name and filename are independent **Twin logic:** A public class Name must be saved in a file called Name.java. (role: context)

## Errors (2)

An error edge states the rule that gets broken in a program, and the right rule.

### MissingKeyword

- **Edge:** `class_declaration` &rarr; `MissingKeyword` (error)
- **Exact edge logic (the wrong rule):** Leaves out a required keyword such as static or class.
- **Twin logic (the right rule):** public class Name and public static void main(String[] args) need their keywords, which are required; omitting or misspelling one is an error, usually caught by the compiler as a syntax error.
- **Wrong belief (on the node):** Leaves out a required keyword such as static or class.
- **Correct rule (on the node):** public class Name and public static void main(String[] args) need their keywords, which are required; omitting or misspelling one is an error, usually caught by the compiler as a syntax error.
- **Provenance:** textbook
- **Role of this concept:** context
- **Edge `main_method` &rarr; `MissingKeyword`, exact edge logic:** Leaves out a required keyword such as static or class. **Twin logic:** public class Name and public static void main(String[] args) need their keywords, which are required; omitting or misspelling one is an error, usually caught by the compiler as a syntax error. (role: primary)

### UnbalancedBraces

- **Edge:** `class_declaration` &rarr; `UnbalancedBraces` (error)
- **Exact edge logic (the wrong rule):** A missing { or } is harmless.
- **Twin logic (the right rule):** Every { must be matched by a } so the class body and the method body are well formed.
- **Wrong belief (on the node):** A missing { or } is harmless.
- **Correct rule (on the node):** Every { must be matched by a } so the class body and the method body are well formed.
- **Provenance:** published
- **Role of this concept:** context
- **Edge `block` &rarr; `UnbalancedBraces`, exact edge logic:** A missing { or } is harmless. **Twin logic:** Every { must be matched by a } so the class body and the method body are well formed. (role: primary)
- **Edge `compile_time_error` &rarr; `UnbalancedBraces`, exact edge logic:** A missing { or } is harmless. **Twin logic:** Every { must be matched by a } so the class body and the method body are well formed. (role: context)

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for class declaration: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to class declaration agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

- **Edge:** `class_declaration` &rarr; `class_declaration@L0` (has_level)
- **Exact edge logic:** class declaration -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (3 ways).

Ways (3), each with its exact rule:

- **[0] everyday\_reading** (rule type E, folk-meaning rule): Everyday meaning: a 'class' is a group of students or a category, and 'public' means open to everyone. Java rule: public class Name { ... } declares the named unit that holds the program's methods; for now S&amp;W say 'class' means 'program'.
- **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `ClassNameMatchesFile`: wrong rule: The class name and the file name are independent. Right rule: public class Name must be saved in a file named Name.java.
- **[2] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `ClassNameMatchesFile`: Applies the containment rule unevenly: treats the class's closing brace as the end of main on one trace, or looks for main outside the class on another; the class body is everything between the outermost { and }. (here mixing in: "class name and filename are independent")

### L1: Unistructural / atom x text surface

L1 for class declaration: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

- **Edge:** `class_declaration` &rarr; `class_declaration@L1` (has_level)
- **Exact edge logic:** class declaration -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

Ways (2), each with its exact rule:

- **[0] names\_the\_element** (rule type N, identity rule): A class declaration (public class Name { ... }) is the outer container of a Java program; in Chapter 1 each program is a single class with a single method main().
- **[1] states\_the\_rule** (rule type S, declarative rule): A program is written as public class Name { &lt;method declarations&gt; }; the outermost braces contain the class definition and the inner braces contain the method definitions, and the keywords public and class are required.

### L2: Multistructural / block x execution / preoperational

L2 for class declaration: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

- **Edge:** `class_declaration` &rarr; `class_declaration@L2` (has_level)
- **Exact edge logic:** class declaration -&gt; L2 (Multistructural): the answer applies the rules of class declaration to every part of the code, in order (3 ways).

Ways (3), each with its exact rule:

- **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): The class declaration itself does not execute: java Name looks up the class Name and calls its main(); the class is just the container that is searched.
- **[1] output\_prediction** (rule type OP, evaluation / result rule): A class declaration produces no output; compiling it produces the file Name.class.
- **[2] one\_step\_execution** (rule type OS, state-transition rule): Declaring the class changes no variable at run time; it only defines the name (Name) that javac uses for Name.class and that java Name uses to find main.

### L3: Relational / relations x function (concrete operational begins)

L3 for class declaration: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

- **Edge:** `class_declaration` &rarr; `class_declaration@L3` (has_level)
- **Exact edge logic:** class declaration -&gt; L3 (Relational): the answer relates the parts (3 ways).

Ways (3), each with its exact rule:

- **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): The name after 'class' must equal the file name without .java.
- **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): main must be declared inside the class's braces; java Name looks only inside class Name for main.
- **[2] purpose\_of\_the\_whole** (rule type P, plan / role rule): Purpose: package and name a program so it can be compiled and run by name; copying HelloWorld.java and replacing the name on the first line is how a new program is started.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for class declaration: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

- **Edge:** `class_declaration` &rarr; `class_declaration@L4` (has_level)
- **Exact edge logic:** class declaration -&gt; L4 (Extended abstract): the answer reasons beyond the given code (5 ways).

Ways (5), each with its exact rule:

- **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `ClassNameMatchesFile`: Renaming the class requires renaming the file (and the java command) to keep it compiling and runnable; moving main outside the class braces breaks compilation.
- **[1] diagnose\_an\_error** (rule type D, error rule): rule broken: public class Name needs the keyword class (and correct spelling). Kind: compile-time. Trigger class: omitting or misspelling class (or public) on the first line
- **[2] transfer\_to\_a\_new\_program** (rule type X, applicability rule): In Chapter 1 every program is exactly one public class containing main; a separate class (and file) is needed for each separate program. Multiple classes and methods come only in Section 2.1.
- **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: Every { must be matched by a }. Kind: compile-time. Trigger class: a missing or extra brace around the class or method body
- **[4] diagnose\_an\_error** (rule type D, error rule): rule broken: A public class must be in a file of the same name. Kind: compile-time. Trigger class: class name differs from file name

## Same topic

`class_declaration` belongs to the topic **Understanding a program (HelloWorld)** (`topic1.1.b`). The topic also contains: `block`, `comment`, `main_method`, `print`, `println`, `program_layout`, `statement`, `string_literal`.

## Rules of the concept (16)

- **Book** (SW-1e, p. 6 (pdf 16)): "For the time being, you can think of "class" as meaning "program.""
- **Book** (SW-1e, p. 6 (pdf 16)): "Its name is HelloWorld, which means that its code resides in a file named HelloWorld.java (by convention in Java)."
- **Book** (OT-Hello, ): "The keyword class begins the class definition for a class named name, and the code for each class appears between the opening and closing curly braces"
- **Book** (SW-1.1, p. 6 (pdf 16)): "public class HelloWorld {"
- **E** (folk-meaning rule): Everyday meaning: a 'class' is a group of students or a category, and 'public' means open to everyone. Java rule: public class Name { ... } declares the named unit that holds the program's methods; for now S&amp;W say 'class' means 'program'.
- **M** (wrong rule / right rule): ClassNameMatchesFile: wrong: The class name and the file name are independent. \| right: public class Name must be saved in a file named Name.java.
- **T** (uneven-application rule): Applies the containment rule unevenly: treats the class's closing brace as the end of main on one trace, or looks for main outside the class on another; the class body is everything between the outermost { and }.
- **N** (identity rule): A class declaration (public class Name { ... }) is the outer container of a Java program; in Chapter 1 each program is a single class with a single method main().
- **S** (declarative rule): A program is written as public class Name { &lt;method declarations&gt; }; the outermost braces contain the class definition and the inner braces contain the method definitions, and the keywords public and class are required.
- **LT** (operational sequencing rule): The class declaration itself does not execute: java Name looks up the class Name and calls its main(); the class is just the container that is searched.
- **OP** (evaluation / result rule): A class declaration produces no output; compiling it produces the file Name.class.
- **OS** (state-transition rule): Declaring the class changes no variable at run time; it only defines the name (Name) that javac uses for Name.class and that java Name uses to find main.
- **R** (composition rule (with a neighbour)): with program\_text: The name after 'class' must equal the file name without .java.
- **R** (composition rule (with a neighbour)): with main\_method: main must be declared inside the class's braces; java Name looks only inside class Name for main.
- **P** (plan / role rule): Purpose: package and name a program so it can be compiled and run by name; copying HelloWorld.java and replacing the name on the first line is how a new program is started.
- **C** (conservation rule): Renaming the class requires renaming the file (and the java command) to keep it compiling and runnable; moving main outside the class braces breaks compilation.
- **D** (error rule): rule broken: public class Name needs the keyword class (and correct spelling) (compile-time)
- **D** (error rule): rule broken: Every { must be matched by a } (compile-time)
- **D** (error rule): rule broken: A public class must be in a file of the same name (compile-time)
- **X** (applicability rule): In Chapter 1 every program is exactly one public class containing main; a separate class (and file) is needed for each separate program. Multiple classes and methods come only in Section 2.1.

## How it is found in code and answers (reader block)

- **Aliases:** class
- **Code patterns:** `\bclass\s+[A-Za-z_]\w*`
- **Operator symbols:** none
- **Java types:** none
- **Signal file\_name\_mismatch** (scope , decisive): `None`
- **Signal file\_name\_mismatch\_regex** (scope program, decisive): `\b(?P<f>[A-Z]\w*)\.java\b[\s\S]{0,400}?\bclass\s+(?!(?P=f)\b)[A-Z]\w*`

## The whole prerequisite chain

- **Everything it builds on (1):** `program_text`
- **Everything that builds on it (32):** `accumulator_pattern`, `algorithm_pseudocode`, `args_length`, `black_box_model`, `block`, `command_line_args`, `compound_assignment`, `conditional_operator`, `control_flow`, `dangling_else`, `debugging`, `else_if_chain`, `empty_statement`, `explicit_cast`, `flowchart`, `if_else_statement`, `if_statement`, `logical_error`, `main_method`, `math_random`, `monte_carlo_simulation`, `nested_conditionals`, `parsing`, `print`, `printing_array_reference`, `println`, `program_layout`, `sentinel_loop`, `statement`, `switch_statement`, `type_conversion`, `widening_conversion`

## Every edge in this view and its exact edge logic (23)

All the edges drawn in the picture, in the order: prerequisite, parallel, misconception, error, has_level, contains.

**1. `class_declaration` &rarr; `main_method`** (prerequisite)

- **Exact edge logic:** main is written inside the class's braces, so java Name looks inside the class Name to find main.
- **Grounding:** book\_passage
- **Composition rule (R) of `class_declaration` with `main_method`:** main must be declared inside the class's braces; java Name looks only inside class Name for main.
- **Composition rule (R) of `main_method` with `class_declaration`:** main is declared inside the class's braces; java Name looks in class Name for main.

**2. `program_text` &rarr; `class_declaration`** (prerequisite)

- **Exact edge logic:** The source file Name.java holds the public class, and that class must be named Name.
- **Grounding:** book\_passage
- **Composition rule (R) of `program_text` with `class_declaration`:** The name after 'public class' constrains the file name: public class Name must be in Name.java, or javac rejects it.
- **Composition rule (R) of `class_declaration` with `program_text`:** The name after 'class' must equal the file name without .java.

**3. `class_declaration` &rarr; `ClassNameMatchesFile`** (misconception)

- **Exact edge logic (the wrong rule):** The class can have any name; the file name does not need to match it.
- **Twin logic (the right rule):** A public class Name must be saved in a file called Name.java.
- **Role:** primary

**4. `program_text` &rarr; `ClassNameMatchesFile`** (misconception)

- **Exact edge logic (the wrong rule):** class name and filename are independent
- **Twin logic (the right rule):** A public class Name must be saved in a file called Name.java.
- **Role:** context

**5. `class_declaration` &rarr; `MissingKeyword`** (error)

- **Exact edge logic (the wrong rule):** Leaves out a required keyword such as static or class.
- **Twin logic (the right rule):** public class Name and public static void main(String[] args) need their keywords, which are required; omitting or misspelling one is an error, usually caught by the compiler as a syntax error.
- **Role:** context

**6. `class_declaration` &rarr; `UnbalancedBraces`** (error)

- **Exact edge logic (the wrong rule):** A missing { or } is harmless.
- **Twin logic (the right rule):** Every { must be matched by a } so the class body and the method body are well formed.
- **Role:** context

**7. `block` &rarr; `UnbalancedBraces`** (error)

- **Exact edge logic (the wrong rule):** A missing { or } is harmless.
- **Twin logic (the right rule):** Every { must be matched by a } so the class body and the method body are well formed.
- **Role:** primary

**8. `compile_time_error` &rarr; `UnbalancedBraces`** (error)

- **Exact edge logic (the wrong rule):** A missing { or } is harmless.
- **Twin logic (the right rule):** Every { must be matched by a } so the class body and the method body are well formed.
- **Role:** context

**9. `main_method` &rarr; `MissingKeyword`** (error)

- **Exact edge logic (the wrong rule):** Leaves out a required keyword such as static or class.
- **Twin logic (the right rule):** public class Name and public static void main(String[] args) need their keywords, which are required; omitting or misspelling one is an error, usually caught by the compiler as a syntax error.
- **Role:** primary

**10. `class_declaration` &rarr; `class_declaration@L0`** (has_level)

- **Exact edge logic:** class declaration -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (3 ways).
  - **[0] everyday\_reading** (rule type E, folk-meaning rule): Everyday meaning: a 'class' is a group of students or a category, and 'public' means open to everyone. Java rule: public class Name { ... } declares the named unit that holds the program's methods; for now S&amp;W say 'class' means 'program'.
  - **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `ClassNameMatchesFile`: wrong rule: The class name and the file name are independent. Right rule: public class Name must be saved in a file named Name.java.
  - **[2] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `ClassNameMatchesFile`: Applies the containment rule unevenly: treats the class's closing brace as the end of main on one trace, or looks for main outside the class on another; the class body is everything between the outermost { and }. (here mixing in: "class name and filename are independent")

**11. `class_declaration` &rarr; `class_declaration@L1`** (has_level)

- **Exact edge logic:** class declaration -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).
  - **[0] names\_the\_element** (rule type N, identity rule): A class declaration (public class Name { ... }) is the outer container of a Java program; in Chapter 1 each program is a single class with a single method main().
  - **[1] states\_the\_rule** (rule type S, declarative rule): A program is written as public class Name { &lt;method declarations&gt; }; the outermost braces contain the class definition and the inner braces contain the method definitions, and the keywords public and class are required.

**12. `class_declaration` &rarr; `class_declaration@L2`** (has_level)

- **Exact edge logic:** class declaration -&gt; L2 (Multistructural): the answer applies the rules of class declaration to every part of the code, in order (3 ways).
  - **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): The class declaration itself does not execute: java Name looks up the class Name and calls its main(); the class is just the container that is searched.
  - **[1] output\_prediction** (rule type OP, evaluation / result rule): A class declaration produces no output; compiling it produces the file Name.class.
  - **[2] one\_step\_execution** (rule type OS, state-transition rule): Declaring the class changes no variable at run time; it only defines the name (Name) that javac uses for Name.class and that java Name uses to find main.

**13. `class_declaration` &rarr; `class_declaration@L3`** (has_level)

- **Exact edge logic:** class declaration -&gt; L3 (Relational): the answer relates the parts (3 ways).
  - **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): The name after 'class' must equal the file name without .java.
  - **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): main must be declared inside the class's braces; java Name looks only inside class Name for main.
  - **[2] purpose\_of\_the\_whole** (rule type P, plan / role rule): Purpose: package and name a program so it can be compiled and run by name; copying HelloWorld.java and replacing the name on the first line is how a new program is started.

**14. `class_declaration` &rarr; `class_declaration@L4`** (has_level)

- **Exact edge logic:** class declaration -&gt; L4 (Extended abstract): the answer reasons beyond the given code (5 ways).
  - **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `ClassNameMatchesFile`: Renaming the class requires renaming the file (and the java command) to keep it compiling and runnable; moving main outside the class braces breaks compilation.
  - **[1] diagnose\_an\_error** (rule type D, error rule): rule broken: public class Name needs the keyword class (and correct spelling). Kind: compile-time. Trigger class: omitting or misspelling class (or public) on the first line
  - **[2] transfer\_to\_a\_new\_program** (rule type X, applicability rule): In Chapter 1 every program is exactly one public class containing main; a separate class (and file) is needed for each separate program. Multiple classes and methods come only in Section 2.1.
  - **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: Every { must be matched by a }. Kind: compile-time. Trigger class: a missing or extra brace around the class or method body
  - **[4] diagnose\_an\_error** (rule type D, error rule): rule broken: A public class must be in a file of the same name. Kind: compile-time. Trigger class: class name differs from file name

**15. `topic1.1.b` &rarr; `class_declaration`** (contains)

- topic `topic1.1.b` contains `class_declaration`

**16. `topic1.1.b` &rarr; `block`** (contains)

- topic `topic1.1.b` contains `block`

**17. `topic1.1.b` &rarr; `comment`** (contains)

- topic `topic1.1.b` contains `comment`

**18. `topic1.1.b` &rarr; `main_method`** (contains)

- topic `topic1.1.b` contains `main_method`

**19. `topic1.1.b` &rarr; `print`** (contains)

- topic `topic1.1.b` contains `print`

**20. `topic1.1.b` &rarr; `println`** (contains)

- topic `topic1.1.b` contains `println`

**21. `topic1.1.b` &rarr; `program_layout`** (contains)

- topic `topic1.1.b` contains `program_layout`

**22. `topic1.1.b` &rarr; `statement`** (contains)

- topic `topic1.1.b` contains `statement`

**23. `topic1.1.b` &rarr; `string_literal`** (contains)

- topic `topic1.1.b` contains `string_literal`
