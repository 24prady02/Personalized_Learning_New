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

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 21 edges around this concept. The edge logic, the wrong and right rules and the exact rules of the ways are copied word for word from the graph.

## To work on (0)

Nothing is missing for this concept.

## What it needs first (1)

A prerequisite edge means the other concept has to be understood before `main_method`.

### `class_declaration` comes before `main_method`

*public class Name { ... } -- the outer container*

- **Edge:** `pre:class_declaration->main_method`
- **Exact edge logic:** main is written inside the class's braces, so java Name looks inside the class Name to find main.
- **Grounding:** book\_passage
- **Composition rule (R) of `main_method` with `class_declaration`:** main is declared inside the class's braces; java Name looks in class Name for main.
- **Composition rule (R) of `class_declaration` with `main_method`:** main must be declared inside the class's braces; java Name looks only inside class Name for main.

## What it leads to (2)

These concepts need `main_method` first.

### `main_method` comes before `command_line_args`

*args[] -- strings passed at launch*

- **Edge:** `pre:main_method->command_line_args`
- **Exact edge logic:** The command-line arguments arrive in main's parameter args, an array of Strings.
- **Grounding:** book\_passage
- **Composition rule (R) of `main_method` with `command_line_args`:** The command-line arguments arrive in main's parameter args, an array of Strings (args[0], args[1], ...).
- **Composition rule (R) of `command_line_args` with `main_method`:** The arguments arrive in main's parameter args (String[] args).

### `main_method` comes before `statement`

*one step, terminated by ;, executed in sequence*

- **Edge:** `pre:main_method->statement`
- **Exact edge logic:** Statements are written in main's body, and running the program executes main's statements in order, one by one.
- **Grounding:** book\_passage
- **Composition rule (R) of `main_method` with `statement`:** main's body holds the statements; running the program executes them in order, one by one.
- **Composition rule (R) of `statement` with `main_method`:** Statements live in main's body; running the program executes main's statements in order.

## Learned alongside (0)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

No parallel edge touches this concept.

## Misconceptions (0)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

The graph has no misconception edge from this concept.

## Errors (2)

An error edge states the rule that gets broken in a program, and the right rule.

### MainWithoutStringArgs

- **Edge:** `main_method` &rarr; `MainWithoutStringArgs` (error)
- **Exact edge logic (the wrong rule):** public static void main() is an acceptable entry point.
- **Twin logic (the right rule):** main is written public static void main(String[] args); these keywords and the args parameter are required.
- **Wrong belief (on the node):** public static void main() is an acceptable entry point.
- **Correct rule (on the node):** main is written public static void main(String[] args); these keywords and the args parameter are required.
- **Provenance:** textbook
- **Role of this concept:** primary
- **Edge `run_time_error` &rarr; `MainWithoutStringArgs`, exact edge logic:** public static void main() is an acceptable entry point. **Twin logic:** main is written public static void main(String[] args); these keywords and the args parameter are required. (role: context)

### MissingKeyword

- **Edge:** `main_method` &rarr; `MissingKeyword` (error)
- **Exact edge logic (the wrong rule):** Leaves out a required keyword such as static or class.
- **Twin logic (the right rule):** public class Name and public static void main(String[] args) need their keywords, which are required; omitting or misspelling one is an error, usually caught by the compiler as a syntax error.
- **Wrong belief (on the node):** Leaves out a required keyword such as static or class.
- **Correct rule (on the node):** public class Name and public static void main(String[] args) need their keywords, which are required; omitting or misspelling one is an error, usually caught by the compiler as a syntax error.
- **Provenance:** textbook
- **Role of this concept:** primary
- **Edge `class_declaration` &rarr; `MissingKeyword`, exact edge logic:** Leaves out a required keyword such as static or class. **Twin logic:** public class Name and public static void main(String[] args) need their keywords, which are required; omitting or misspelling one is an error, usually caught by the compiler as a syntax error. (role: context)

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for main method: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to main method agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

- **Edge:** `main_method` &rarr; `main_method@L0` (has_level)
- **Exact edge logic:** main method -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (1 way).

Ways (1), each with its exact rule:

- **[0] everyday\_reading** (rule type E, folk-meaning rule): Everyday reading: 'main' sounds like the most important part, and 'void' like empty or invalid. Java rule: main is the entry point that java Name calls; public static void main(String[] args) must be written exactly, and void only means main returns no value.

### L1: Unistructural / atom x text surface

L1 for main method: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

- **Edge:** `main_method` &rarr; `main_method@L1` (has_level)
- **Exact edge logic:** main method -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

Ways (2), each with its exact rule:

- **[0] names\_the\_element** (rule type N, identity rule): main is the method that is the entry point of a Java program: public static void main(String[] args) { statements }.
- **[1] states\_the\_rule** (rule type S, declarative rule): The header must be public static void main(String[] args); the keywords are required; its body is a sequence of statements in braces, each followed by a semicolon.

### L2: Multistructural / block x execution / preoperational

L2 for main method: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

- **Edge:** `main_method` &rarr; `main_method@L2` (has_level)
- **Exact edge logic:** main method -&gt; L2 (Multistructural): the answer applies the rules of main method to every part of the code, in order (3 ways).

Ways (3), each with its exact rule:

- **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): When the program runs, it starts at the first statement in main and ends when it finishes the last statement, executing the statements in order, one by one.
- **[1] output\_prediction** (rule type OP, evaluation / result rule): main returns no value (void); the program's observable result is whatever main's statements print.
- **[2] one\_step\_execution** (rule type OS, state-transition rule): Calling main binds args to the array of command-line strings and then runs its body; when its last statement finishes, control goes back to the system.

### L3: Relational / relations x function (concrete operational begins)

L3 for main method: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

- **Edge:** `main_method` &rarr; `main_method@L3` (has_level)
- **Exact edge logic:** main method -&gt; L3 (Relational): the answer relates the parts (4 ways).

Ways (4), each with its exact rule:

- **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): main is declared inside the class's braces; java Name looks in class Name for main.
- **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): main's body holds the statements; running the program executes them in order, one by one.
- **[2] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): The command-line arguments arrive in main's parameter args, an array of Strings (args[0], args[1], ...).
- **[3] purpose\_of\_the\_whole** (rule type P, plan / role rule): Purpose: the single place where a Chapter 1 program's work is written; programming at this stage means specifying a class name and the sequence of statements in its main().

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for main method: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

- **Edge:** `main_method` &rarr; `main_method@L4` (has_level)
- **Exact edge logic:** main method -&gt; L4 (Extended abstract): the answer reasons beyond the given code (4 ways).

Ways (4), each with its exact rule:

- **[0] predict\_a\_change** (rule type C, conservation rule): Changing the order of main's statements changes the order of output; changing public static void main(String[] args) (e.g. dropping static or args) keeps it compiling but leaves the class without a launchable entry point, or breaks compilation if misspelt.
- **[1] diagnose\_an\_error** (rule type D, error rule): rule broken: main is written public static void main(String[] args). Kind: launch error. Trigger class: header written as public static void main() (or without static): it compiles, but java Name reports that no main method is found
- **[2] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Every runnable program needs exactly this main; put Chapter 1 code in it. It is not the place for code that should be reused or tested separately (that needs other methods, Section 2.1).
- **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: public, static, void and main must be present and correctly spelled. Kind: compile-time. Trigger class: misspelling a keyword (e.g. stati, viod) so the header cannot be parsed

## Same topic

`main_method` belongs to the topic **Understanding a program (HelloWorld)** (`topic1.1.b`). The topic also contains: `block`, `class_declaration`, `comment`, `print`, `println`, `program_layout`, `statement`, `string_literal`.

## Rules of the concept (15)

- **Book** (SW-1e, p. 7 (pdf 17)): "When you type java followed by a class name in your terminal application, the system calls the main() method that you defined in that class"
- **Book** (OT-Hello, ): "In the Java programming language, every application must contain a main method whose signature is: public static void main(String[] args)"
- **Book** (OT-Hello, ): "The main method accepts a single argument: an array of elements of type String."
- **Book** (JLS-12.1, ): "The Java Virtual Machine starts execution by invoking the method main of some specified class, passing it a single argument, which is an array of strings."
- **E** (folk-meaning rule): Everyday reading: 'main' sounds like the most important part, and 'void' like empty or invalid. Java rule: main is the entry point that java Name calls; public static void main(String[] args) must be written exactly, and void only means main returns no value.
- **T** (uneven-application rule): Applies the entry-point rule (LT) unevenly: starts tracing at the top of the file on one trace and at main on another, or stops before main's last statement.
- **N** (identity rule): main is the method that is the entry point of a Java program: public static void main(String[] args) { statements }.
- **S** (declarative rule): The header must be public static void main(String[] args); the keywords are required; its body is a sequence of statements in braces, each followed by a semicolon.
- **LT** (operational sequencing rule): When the program runs, it starts at the first statement in main and ends when it finishes the last statement, executing the statements in order, one by one.
- **OP** (evaluation / result rule): main returns no value (void); the program's observable result is whatever main's statements print.
- **OS** (state-transition rule): Calling main binds args to the array of command-line strings and then runs its body; when its last statement finishes, control goes back to the system.
- **R** (composition rule (with a neighbour)): with class\_declaration: main is declared inside the class's braces; java Name looks in class Name for main.
- **R** (composition rule (with a neighbour)): with statement: main's body holds the statements; running the program executes them in order, one by one.
- **R** (composition rule (with a neighbour)): with command\_line\_args: The command-line arguments arrive in main's parameter args, an array of Strings (args[0], args[1], ...).
- **P** (plan / role rule): Purpose: the single place where a Chapter 1 program's work is written; programming at this stage means specifying a class name and the sequence of statements in its main().
- **C** (conservation rule): Changing the order of main's statements changes the order of output; changing public static void main(String[] args) (e.g. dropping static or args) keeps it compiling but leaves the class without a launchable entry point, or breaks compilation if misspelt.
- **D** (error rule): rule broken: main is written public static void main(String[] args) (launch error)
- **D** (error rule): rule broken: public, static, void and main must be present and correctly spelled (compile-time)
- **X** (applicability rule): Every runnable program needs exactly this main; put Chapter 1 code in it. It is not the place for code that should be reused or tested separately (that needs other methods, Section 2.1).

## How it is found in code and answers (reader block)

- **Aliases:** main method, main function
- **Code patterns:** `\bstatic\s+void\s+main\s*\(`, `\bvoid\s+main\s*\(\s*String`
- **Operator symbols:** none
- **Java types:** none

## The whole prerequisite chain

- **Everything it builds on (2):** `class_declaration`, `program_text`
- **Everything that builds on it (31):** `accumulator_pattern`, `algorithm_pseudocode`, `args_length`, `black_box_model`, `block`, `command_line_args`, `compound_assignment`, `conditional_operator`, `control_flow`, `dangling_else`, `debugging`, `else_if_chain`, `empty_statement`, `explicit_cast`, `flowchart`, `if_else_statement`, `if_statement`, `logical_error`, `math_random`, `monte_carlo_simulation`, `nested_conditionals`, `parsing`, `print`, `printing_array_reference`, `println`, `program_layout`, `sentinel_loop`, `statement`, `switch_statement`, `type_conversion`, `widening_conversion`

## Every edge in this view and its exact edge logic (21)

All the edges drawn in the picture, in the order: prerequisite, parallel, misconception, error, has_level, contains.

**1. `class_declaration` &rarr; `main_method`** (prerequisite)

- **Exact edge logic:** main is written inside the class's braces, so java Name looks inside the class Name to find main.
- **Grounding:** book\_passage
- **Composition rule (R) of `class_declaration` with `main_method`:** main must be declared inside the class's braces; java Name looks only inside class Name for main.
- **Composition rule (R) of `main_method` with `class_declaration`:** main is declared inside the class's braces; java Name looks in class Name for main.

**2. `main_method` &rarr; `command_line_args`** (prerequisite)

- **Exact edge logic:** The command-line arguments arrive in main's parameter args, an array of Strings.
- **Grounding:** book\_passage
- **Composition rule (R) of `main_method` with `command_line_args`:** The command-line arguments arrive in main's parameter args, an array of Strings (args[0], args[1], ...).
- **Composition rule (R) of `command_line_args` with `main_method`:** The arguments arrive in main's parameter args (String[] args).

**3. `main_method` &rarr; `statement`** (prerequisite)

- **Exact edge logic:** Statements are written in main's body, and running the program executes main's statements in order, one by one.
- **Grounding:** book\_passage
- **Composition rule (R) of `main_method` with `statement`:** main's body holds the statements; running the program executes them in order, one by one.
- **Composition rule (R) of `statement` with `main_method`:** Statements live in main's body; running the program executes main's statements in order.

**4. `main_method` &rarr; `MainWithoutStringArgs`** (error)

- **Exact edge logic (the wrong rule):** public static void main() is an acceptable entry point.
- **Twin logic (the right rule):** main is written public static void main(String[] args); these keywords and the args parameter are required.
- **Role:** primary

**5. `main_method` &rarr; `MissingKeyword`** (error)

- **Exact edge logic (the wrong rule):** Leaves out a required keyword such as static or class.
- **Twin logic (the right rule):** public class Name and public static void main(String[] args) need their keywords, which are required; omitting or misspelling one is an error, usually caught by the compiler as a syntax error.
- **Role:** primary

**6. `class_declaration` &rarr; `MissingKeyword`** (error)

- **Exact edge logic (the wrong rule):** Leaves out a required keyword such as static or class.
- **Twin logic (the right rule):** public class Name and public static void main(String[] args) need their keywords, which are required; omitting or misspelling one is an error, usually caught by the compiler as a syntax error.
- **Role:** context

**7. `run_time_error` &rarr; `MainWithoutStringArgs`** (error)

- **Exact edge logic (the wrong rule):** public static void main() is an acceptable entry point.
- **Twin logic (the right rule):** main is written public static void main(String[] args); these keywords and the args parameter are required.
- **Role:** context

**8. `main_method` &rarr; `main_method@L0`** (has_level)

- **Exact edge logic:** main method -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (1 way).
  - **[0] everyday\_reading** (rule type E, folk-meaning rule): Everyday reading: 'main' sounds like the most important part, and 'void' like empty or invalid. Java rule: main is the entry point that java Name calls; public static void main(String[] args) must be written exactly, and void only means main returns no value.

**9. `main_method` &rarr; `main_method@L1`** (has_level)

- **Exact edge logic:** main method -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).
  - **[0] names\_the\_element** (rule type N, identity rule): main is the method that is the entry point of a Java program: public static void main(String[] args) { statements }.
  - **[1] states\_the\_rule** (rule type S, declarative rule): The header must be public static void main(String[] args); the keywords are required; its body is a sequence of statements in braces, each followed by a semicolon.

**10. `main_method` &rarr; `main_method@L2`** (has_level)

- **Exact edge logic:** main method -&gt; L2 (Multistructural): the answer applies the rules of main method to every part of the code, in order (3 ways).
  - **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): When the program runs, it starts at the first statement in main and ends when it finishes the last statement, executing the statements in order, one by one.
  - **[1] output\_prediction** (rule type OP, evaluation / result rule): main returns no value (void); the program's observable result is whatever main's statements print.
  - **[2] one\_step\_execution** (rule type OS, state-transition rule): Calling main binds args to the array of command-line strings and then runs its body; when its last statement finishes, control goes back to the system.

**11. `main_method` &rarr; `main_method@L3`** (has_level)

- **Exact edge logic:** main method -&gt; L3 (Relational): the answer relates the parts (4 ways).
  - **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): main is declared inside the class's braces; java Name looks in class Name for main.
  - **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): main's body holds the statements; running the program executes them in order, one by one.
  - **[2] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): The command-line arguments arrive in main's parameter args, an array of Strings (args[0], args[1], ...).
  - **[3] purpose\_of\_the\_whole** (rule type P, plan / role rule): Purpose: the single place where a Chapter 1 program's work is written; programming at this stage means specifying a class name and the sequence of statements in its main().

**12. `main_method` &rarr; `main_method@L4`** (has_level)

- **Exact edge logic:** main method -&gt; L4 (Extended abstract): the answer reasons beyond the given code (4 ways).
  - **[0] predict\_a\_change** (rule type C, conservation rule): Changing the order of main's statements changes the order of output; changing public static void main(String[] args) (e.g. dropping static or args) keeps it compiling but leaves the class without a launchable entry point, or breaks compilation if misspelt.
  - **[1] diagnose\_an\_error** (rule type D, error rule): rule broken: main is written public static void main(String[] args). Kind: launch error. Trigger class: header written as public static void main() (or without static): it compiles, but java Name reports that no main method is found
  - **[2] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Every runnable program needs exactly this main; put Chapter 1 code in it. It is not the place for code that should be reused or tested separately (that needs other methods, Section 2.1).
  - **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: public, static, void and main must be present and correctly spelled. Kind: compile-time. Trigger class: misspelling a keyword (e.g. stati, viod) so the header cannot be parsed

**13. `topic1.1.b` &rarr; `main_method`** (contains)

- topic `topic1.1.b` contains `main_method`

**14. `topic1.1.b` &rarr; `block`** (contains)

- topic `topic1.1.b` contains `block`

**15. `topic1.1.b` &rarr; `class_declaration`** (contains)

- topic `topic1.1.b` contains `class_declaration`

**16. `topic1.1.b` &rarr; `comment`** (contains)

- topic `topic1.1.b` contains `comment`

**17. `topic1.1.b` &rarr; `print`** (contains)

- topic `topic1.1.b` contains `print`

**18. `topic1.1.b` &rarr; `println`** (contains)

- topic `topic1.1.b` contains `println`

**19. `topic1.1.b` &rarr; `program_layout`** (contains)

- topic `topic1.1.b` contains `program_layout`

**20. `topic1.1.b` &rarr; `statement`** (contains)

- topic `topic1.1.b` contains `statement`

**21. `topic1.1.b` &rarr; `string_literal`** (contains)

- topic `topic1.1.b` contains `string_literal`
