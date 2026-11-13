# main_method (`main_method`)

public static void main(String[] args) -- entry point

Section 1.1 Your First Program, topic 1.1.b Understanding a program (HelloWorld).

![The knowledge graph around main_method](main_method.png)

## At a glance

- **Needs first:** `class_declaration`
- **Leads to:** `command_line_args`, `statement`
- **Learned alongside:** nothing
- **Misconceptions:** none
- **Errors:** `MainWithoutStringArgs`, `MissingKeyword`
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 21 edges around this concept, each explained in the graph's own words.

## What it needs first (1)

A prerequisite edge means the other concept has to be understood before `main_method`.

### `class_declaration` comes before `main_method`

*public class Name { ... } -- the outer container*

main is written inside the class's braces, so java Name looks inside the class Name to find main.

- **Grounding:** book passage
- **How `main_method` combines with `class_declaration`:** main is declared inside the class's braces; java Name looks in class Name for main.
- **How `class_declaration` combines with `main_method`:** main must be declared inside the class's braces; java Name looks only inside class Name for main.

## What it leads to (2)

These concepts need `main_method` first.

### `main_method` comes before `command_line_args`

*args[] -- strings passed at launch*

The command-line arguments arrive in main's parameter args, an array of Strings.

- **Grounding:** book passage
- **How `main_method` combines with `command_line_args`:** The command-line arguments arrive in main's parameter args, an array of Strings (args[0], args[1], ...).
- **How `command_line_args` combines with `main_method`:** The arguments arrive in main's parameter args (String[] args).

### `main_method` comes before `statement`

*one step, terminated by ;, executed in sequence*

Statements are written in main's body, and running the program executes main's statements in order, one by one.

- **Grounding:** book passage
- **How `main_method` combines with `statement`:** main's body holds the statements; running the program executes them in order, one by one.
- **How `statement` combines with `main_method`:** Statements live in main's body; running the program executes main's statements in order.

## Learned alongside (0)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

No parallel edge touches this concept.

## Misconceptions (0)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

The graph has no misconception edge from this concept.

## Errors (2)

An error edge states the rule that gets broken in a program, and the right rule.

### MainWithoutStringArgs

- **Wrong rule:** public static void main() is an acceptable entry point.
- **Right rule:** main is written public static void main(String[] args); these keywords and the args parameter are required.
- **Role of this concept:** primary
- **Also an edge from `run_time_error`:** public static void main() is an acceptable entry point.

### MissingKeyword

- **Wrong rule:** Leaves out a required keyword such as static or class.
- **Right rule:** public class Name and public static void main(String[] args) need their keywords, which are required; omitting or misspelling one is an error, usually caught by the compiler as a syntax error.
- **Role of this concept:** primary
- **Also an edge from `class_declaration`:** Leaves out a required keyword such as static or class.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for main method: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to main method agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

main method -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (1 way).

- **everyday reading** (folk-meaning rule): Everyday reading: 'main' sounds like the most important part, and 'void' like empty or invalid. Java rule: main is the entry point that java Name calls; public static void main(String[] args) must be written exactly, and void only means main returns no value.

### L1: Unistructural / atom x text surface

L1 for main method: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

main method -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

- **names the element** (identity rule): main is the method that is the entry point of a Java program: public static void main(String[] args) { statements }.
- **states the rule** (declarative rule): The header must be public static void main(String[] args); the keywords are required; its body is a sequence of statements in braces, each followed by a semicolon.

### L2: Multistructural / block x execution / preoperational

L2 for main method: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

main method -&gt; L2 (Multistructural): the answer applies the rules of main method to every part of the code, in order (3 ways).

- **line by line trace** (operational sequencing rule): When the program runs, it starts at the first statement in main and ends when it finishes the last statement, executing the statements in order, one by one.
- **output prediction** (evaluation / result rule): main returns no value (void); the program's observable result is whatever main's statements print.
- **one step execution** (state-transition rule): Calling main binds args to the array of command-line strings and then runs its body; when its last statement finishes, control goes back to the system.

### L3: Relational / relations x function (concrete operational begins)

L3 for main method: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

main method -&gt; L3 (Relational): the answer relates the parts (4 ways).

- **relation to neighbour** (composition rule (with a neighbour)): main is declared inside the class's braces; java Name looks in class Name for main.
- **relation to neighbour** (composition rule (with a neighbour)): main's body holds the statements; running the program executes them in order, one by one.
- **relation to neighbour** (composition rule (with a neighbour)): The command-line arguments arrive in main's parameter args, an array of Strings (args[0], args[1], ...).
- **purpose of the whole** (plan / role rule): Purpose: the single place where a Chapter 1 program's work is written; programming at this stage means specifying a class name and the sequence of statements in its main().

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for main method: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

main method -&gt; L4 (Extended abstract): the answer reasons beyond the given code (4 ways).

- **predict a change** (conservation rule): Changing the order of main's statements changes the order of output; changing public static void main(String[] args) (e.g. dropping static or args) keeps it compiling but leaves the class without a launchable entry point, or breaks compilation if misspelt.
- **diagnose an error** (error rule): rule broken: main is written public static void main(String[] args). Kind: launch error. Trigger class: header written as public static void main() (or without static): it compiles, but java Name reports that no main method is found
- **transfer to a new program** (applicability rule): Every runnable program needs exactly this main; put Chapter 1 code in it. It is not the place for code that should be reused or tested separately (that needs other methods, Section 2.1).
- **diagnose an error** (error rule): rule broken: public, static, void and main must be present and correctly spelled. Kind: compile-time. Trigger class: misspelling a keyword (e.g. stati, viod) so the header cannot be parsed

## Same topic

`main_method` belongs to the topic **Understanding a program (HelloWorld)** (`topic1.1.b`). The topic also contains: `block`, `class_declaration`, `comment`, `print`, `println`, `program_layout`, `statement`, `string_literal`.

## Rules of the concept (15)

- **folk-meaning rule:** Everyday reading: 'main' sounds like the most important part, and 'void' like empty or invalid. Java rule: main is the entry point that java Name calls; public static void main(String[] args) must be written exactly, and void only means main returns no value.
- **uneven-application rule:** Applies the entry-point rule (LT) unevenly: starts tracing at the top of the file on one trace and at main on another, or stops before main's last statement.
- **identity rule:** main is the method that is the entry point of a Java program: public static void main(String[] args) { statements }.
- **declarative rule:** The header must be public static void main(String[] args); the keywords are required; its body is a sequence of statements in braces, each followed by a semicolon.
- **operational sequencing rule:** When the program runs, it starts at the first statement in main and ends when it finishes the last statement, executing the statements in order, one by one.
- **evaluation / result rule:** main returns no value (void); the program's observable result is whatever main's statements print.
- **state-transition rule:** Calling main binds args to the array of command-line strings and then runs its body; when its last statement finishes, control goes back to the system.
- **composition rule (with a neighbour):** with class\_declaration: main is declared inside the class's braces; java Name looks in class Name for main.
- **composition rule (with a neighbour):** with statement: main's body holds the statements; running the program executes them in order, one by one.
- **composition rule (with a neighbour):** with command\_line\_args: The command-line arguments arrive in main's parameter args, an array of Strings (args[0], args[1], ...).
- **plan / role rule:** Purpose: the single place where a Chapter 1 program's work is written; programming at this stage means specifying a class name and the sequence of statements in its main().
- **conservation rule:** Changing the order of main's statements changes the order of output; changing public static void main(String[] args) (e.g. dropping static or args) keeps it compiling but leaves the class without a launchable entry point, or breaks compilation if misspelt.
- **error rule:** rule broken: main is written public static void main(String[] args) (launch error)
- **error rule:** rule broken: public, static, void and main must be present and correctly spelled (compile-time)
- **applicability rule:** Every runnable program needs exactly this main; put Chapter 1 code in it. It is not the place for code that should be reused or tested separately (that needs other methods, Section 2.1).

## The whole prerequisite chain

- **Everything it builds on (2):** `class_declaration`, `program_text`
- **Everything that builds on it (31):** `accumulator_pattern`, `algorithm_pseudocode`, `args_length`, `black_box_model`, `block`, `command_line_args`, `compound_assignment`, `conditional_operator`, `control_flow`, `dangling_else`, `debugging`, `else_if_chain`, `empty_statement`, `explicit_cast`, `flowchart`, `if_else_statement`, `if_statement`, `logical_error`, `math_random`, `monte_carlo_simulation`, `nested_conditionals`, `parsing`, `print`, `printing_array_reference`, `println`, `program_layout`, `sentinel_loop`, `statement`, `switch_statement`, `type_conversion`, `widening_conversion`
