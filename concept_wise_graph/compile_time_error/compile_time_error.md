# compile_time_error (`compile_time_error`)

an error javac reports before the program can run (syntax, types)

Section 1.1 Your First Program, topic 1.1.c Errors.

![The knowledge graph around compile_time_error](compile_time_error.png)

## At a glance

- **Needs first:** `compile`
- **Leads to:** `reading_error_messages`
- **Learned alongside:** `run_time_error`
- **Misconceptions:** `CompilerSuggestionIsFix`, `CompilesMeansWorks`, `ErrorLineIsFaultLine`
- **Errors:** `AssignToFinal`, `MathMethodWithoutClassName`, `MisspelledIdentifier`, `StatementNeedsNoTerminator`, `UnbalancedBraces`, `UnclosedComment`, `UnclosedStringLiteral`
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 40 edges around this concept, each explained in the graph's own words.

## What it needs first (1)

A prerequisite edge means the other concept has to be understood before `compile_time_error`.

### `compile` comes before `compile_time_error`

*javac turns source into bytecode*

A compile-time error is reported while javac compiles Name.java, so no Name.class is produced.

- **Grounding:** book passage
- **How `compile_time_error` combines with `compile`:** A compile-time error is reported while javac compiles Name.java, so no new Name.class is produced.
- **How `compile` combines with `compile_time_error`:** A compile-time error stops the translation, so no Name.class is produced and there is nothing new to run.

## What it leads to (1)

These concepts need `compile_time_error` first.

### `compile_time_error` comes before `reading_error_messages`

*how to read compiler error messages: first error first; reported line may follow the real fault*

Reading error messages is how compile-time errors are found and fixed.

- **Grounding:** book passage
- **How `compile_time_error` combines with `reading_error_messages`:** Each compile-time error comes with a message; reading it (first error first, line may be late) is how it is found and fixed.
- **How `reading_error_messages` combines with `compile_time_error`:** Compile-time errors are found and fixed by reading their messages; the message maps imperfectly to the fault.

## Learned alongside (1)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

### `compile_time_error` alongside `run_time_error`

*an error raised while the program executes (e.g. ArrayIndexOutOfBounds, NumberFormatException)*

A compile-time error is found by javac before the program runs; a run-time error is found while it runs.

- **Grounding:** book passage
- **How `compile_time_error` combines with `run_time_error`:** A compile-time error is found by javac before the program runs; a run-time error only while it runs, so code that compiles can still crash.
- **How `run_time_error` combines with `compile_time_error`:** javac cannot detect it because it depends on run-time values (the argument typed, the divisor's value).

## Misconceptions (3)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### CompilerSuggestionIsFix

- **Wrong rule:** Doing exactly what the compiler message suggests will fix the error.
- **Right rule:** An error message is evidence that something is wrong, but its suggested remedy may be wrong; find the actual cause.
- **Role of this concept:** context
- **Shows at level L0 as:** misconception: wrong rule: Doing exactly what the compiler message suggests will fix the error. Right rule: An error message is evidence that something is wrong, but its suggested remedy may be wrong; find the actual cause.
- **Also an edge from `debugging`:** Doing exactly what the compiler message suggests will fix the error.
- **Also an edge from `reading_error_messages`:** Doing exactly what the compiler message suggests will fix the error.

### CompilesMeansWorks

- **Wrong rule:** Code that compiles is code that works.
- **Right rule:** Code that compiles can still have run-time and logical errors.
- **Role of this concept:** context
- **Shows at level L0 as:** misconception: wrong rule: Code that compiles is code that works. Right rule: Compiling only checks the language rules; code that compiles can still have run-time and logic errors.
- **Shows at level L0 as:** inconsistent trace: Applies the 'javac checks before running' rule unevenly: predicts output for a program that would not compile, or expects a compile error from a fault (such as division by zero) that only shows at run time. (here mixing in: "Code that compiles is code that works")
- **Also an edge from `compile`:** Code that compiles is code that works.
- **Also an edge from `logical_error`:** Code that compiles is code that works.
- **Also an edge from `run_time_error`:** Code that compiles is code that works.
- **Also an edge from `testing`:** Code that compiles is code that works.

### ErrorLineIsFaultLine

- **Wrong rule:** The line number in a javac error is always the line that has the mistake.
- **Right rule:** The compiler reports where it noticed the problem, which can be after the real fault; for example, omitting the second left brace of HelloWorld produces errors reported on later lines.
- **Role of this concept:** context
- **Shows at level L0 as:** misconception: wrong rule: The line number in a javac error is always the line that has the mistake. Right rule: The compiler reports where it noticed the problem, which can be after the real fault (omitting HelloWorld's second left brace gives errors on later lines).
- **Also an edge from `debugging`:** The line number in a javac error is always the line that has the mistake.
- **Also an edge from `reading_error_messages`:** The line number in a javac error is always the line that has the mistake.

## Errors (7)

An error edge states the rule that gets broken in a program, and the right rule.

### AssignToFinal

- **Wrong rule:** Assigns a new value to a variable declared final.
- **Right rule:** A final variable cannot be reassigned after it is initialized; the compiler reports an error.
- **Role of this concept:** context
- **Also an edge from `assignment`:** Assigns a new value to a variable declared final.
- **Also an edge from `named_constants`:** Assigns a new value to a variable declared final.

### MathMethodWithoutClassName

- **Wrong rule:** sqrt(x) calls the square-root method.
- **Right rule:** Library methods are called with the class name, e.g. Math.sqrt(x).
- **Role of this concept:** context
- **Also an edge from `math_library`:** sqrt(x) calls the square-root method.
- **Also an edge from `method_call`:** sqrt(x) calls the square-root method.

### MisspelledIdentifier

- **Wrong rule:** Writes Sytem.out.prinln or a misspelled variable name.
- **Right rule:** Every name must be spelled exactly, including capitalization.
- **Role of this concept:** context
- **Also an edge from `identifier`:** Writes Sytem.out.prinln or a misspelled variable name.

### StatementNeedsNoTerminator

- **Wrong rule:** a statement runs without the ;
- **Right rule:** Each statement must end with ;, otherwise javac reports ';' expected.
- **Role of this concept:** context
- **Also an edge from `statement`:** A statement still compiles and runs if the semicolon at its end is left out, or if a stray ; is put right after if (c) or for (...).

### UnbalancedBraces

- **Wrong rule:** A missing { or } is harmless.
- **Right rule:** Every { must be matched by a } so the class body and the method body are well formed.
- **Role of this concept:** context
- **Also an edge from `block`:** A missing { or } is harmless.
- **Also an edge from `class_declaration`:** A missing { or } is harmless.

### UnclosedComment

- **Wrong rule:** Opens a comment with /\* and never closes it.
- **Right rule:** A /\* comment is the text between /\* and \*/, so the closing \*/ is required.
- **Role of this concept:** context
- **Also an edge from `comment`:** Opens a comment with /\* and never closes it.

### UnclosedStringLiteral

- **Wrong rule:** A string literal can be left without its closing quote.
- **Right rule:** A String literal is enclosed in a pair of double quotes.
- **Role of this concept:** context
- **Also an edge from `string_literal`:** A string literal can be left without its closing quote.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for compile time error: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to compile time error agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

compile time error -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (5 ways).

- **everyday reading** (folk-meaning rule): Everyday reading: 'error' means the program will do something wrong when used, and a message points exactly at the mistake. Java rule: a compile-time error is a breach of the language rules found by javac before any execution; no .class is produced, and the reported line is where javac noticed it.
- **misconception** (wrong rule / right rule; shows `CompilesMeansWorks`): wrong rule: Code that compiles is code that works. Right rule: Compiling only checks the language rules; code that compiles can still have run-time and logic errors.
- **misconception** (wrong rule / right rule; shows `ErrorLineIsFaultLine`): wrong rule: The line number in a javac error is always the line that has the mistake. Right rule: The compiler reports where it noticed the problem, which can be after the real fault (omitting HelloWorld's second left brace gives errors on later lines).
- **inconsistent trace** (uneven-application rule; shows `CompilesMeansWorks`): Applies the 'javac checks before running' rule unevenly: predicts output for a program that would not compile, or expects a compile error from a fault (such as division by zero) that only shows at run time. (here mixing in: "Code that compiles is code that works")
- **misconception** (wrong rule / right rule; shows `CompilerSuggestionIsFix`): wrong rule: Doing exactly what the compiler message suggests will fix the error. Right rule: An error message is evidence that something is wrong, but its suggested remedy may be wrong; find the actual cause.

### L1: Unistructural / atom x text surface

L1 for compile time error: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

compile time error -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

- **names the element** (identity rule): A compile-time error (syntax error) is an error in the source code, caught by javac, that prevents the program from being translated.
- **states the rule** (declarative rule): Compile-time errors occur when the code violates the rules of the Java language (syntax, names, types); they are caught when you compile and prevent the translation.

### L2: Multistructural / block x execution / preoperational

L2 for compile time error: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

compile time error -&gt; L2 (Multistructural): the answer applies the rules of compile time error to every part of the code, in order (3 ways).

- **line by line trace** (operational sequencing rule): javac reads the whole file, reports each error with file name, line number and message, tries to recover and continue, and prints a count; the first message is the most reliable.
- **output prediction** (evaluation / result rule): Result: messages such as Bad.java:4: ';' expected ... 3 errors, and no Name.class; nothing of the program runs.
- **one step execution** (state-transition rule): A failed compile leaves the file system without a new Name.class (an older one, if any, is not updated) and changes no program state.

### L3: Relational / relations x function (concrete operational begins)

L3 for compile time error: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

compile time error -&gt; L3 (Relational): the answer relates the parts (4 ways).

- **relation to neighbour** (composition rule (with a neighbour)): A compile-time error is reported while javac compiles Name.java, so no new Name.class is produced.
- **relation to neighbour** (composition rule (with a neighbour)): Each compile-time error comes with a message; reading it (first error first, line may be late) is how it is found and fixed.
- **relation to neighbour** (composition rule (with a neighbour)): A compile-time error is found by javac before the program runs; a run-time error only while it runs, so code that compiles can still crash.
- **purpose of the whole** (plan / role rule): Purpose (of the check): catch rule violations automatically before running, so they cannot cause wrong behaviour; S&amp;W say treat the compiler as a friend.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for compile time error: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

compile time error -&gt; L4 (Extended abstract): the answer reasons beyond the given code (10 ways).

- **predict a change** (conservation rule; shows `CompilesMeansWorks`): Fixing the first error and recompiling can remove many messages at once; a single missing brace or semicolon can cause several messages.
- **diagnose an error** (error rule): rule broken: Each statement must end with ;. Kind: compile-time. Trigger class: missing ; at the end of a statement: ';' expected
- **diagnose an error** (error rule): rule broken: Every { must be matched by a }. Kind: compile-time. Trigger class: missing or extra brace: '{' expected, 'class' or 'interface' expected, reached end of file while parsing
- **diagnose an error** (error rule): rule broken: A String literal is enclosed in a pair of double quotes. Kind: compile-time. Trigger class: missing closing quote: unclosed string literal, often with confusing follow-on errors
- **diagnose an error** (error rule): rule broken: Library static methods are called with the class name, e.g. Math.sqrt(x). Kind: compile-time. Trigger class: calling sqrt(x) without Math.: cannot find symbol
- **diagnose an error** (error rule): rule broken: Every name must be spelled exactly, including capitalization. Kind: compile-time. Trigger class: Sytem.out.prinln, Println, or a misspelled variable: cannot find symbol
- **diagnose an error** (error rule): rule broken: A /\* comment needs its closing \*/. Kind: compile-time. Trigger class: /\* with no \*/ swallows the rest of the file
- **transfer to a new program** (applicability rule): Expect compile-time errors for anything the compiler can check from the text alone (syntax, names, types, final); expect run-time or logic errors for faults that depend on input values or on what the program was meant to do.
- **diagnose an error** (error rule): rule broken: A final variable cannot be reassigned after it is initialized. Kind: compile-time. Trigger class: assigning a second value to a final variable
- **diagnose an error** (error rule): rule broken: Required keywords (class, static, void...) must be present and spelled right. Kind: compile-time. Trigger class: omitting or misspelling a keyword in public class Name or the main header

## Same topic

`compile_time_error` belongs to the topic **Errors** (`topic1.1.c`). The topic also contains: `logical_error`, `reading_error_messages`, `run_time_error`.

## Rules of the concept (24)

- **folk-meaning rule:** Everyday reading: 'error' means the program will do something wrong when used, and a message points exactly at the mistake. Java rule: a compile-time error is a breach of the language rules found by javac before any execution; no .class is produced, and the reported line is where javac noticed it.
- **wrong rule / right rule:** CompilesMeansWorks: wrong: Code that compiles is code that works. \| right: Compiling only checks the language rules; code that compiles can still have run-time and logic errors.
- **wrong rule / right rule:** ErrorLineIsFaultLine: wrong: The line number in a javac error is always the line that has the mistake. \| right: The compiler reports where it noticed the problem, which can be after the real fault (omitting HelloWorld's second left brace gives errors on later lines).
- **wrong rule / right rule:** CompilerSuggestionIsFix: wrong: Doing exactly what the compiler message suggests will fix the error. \| right: An error message is evidence that something is wrong, but its suggested remedy may be wrong; find the actual cause.
- **uneven-application rule:** Applies the 'javac checks before running' rule unevenly: predicts output for a program that would not compile, or expects a compile error from a fault (such as division by zero) that only shows at run time.
- **identity rule:** A compile-time error (syntax error) is an error in the source code, caught by javac, that prevents the program from being translated.
- **declarative rule:** Compile-time errors occur when the code violates the rules of the Java language (syntax, names, types); they are caught when you compile and prevent the translation.
- **operational sequencing rule:** javac reads the whole file, reports each error with file name, line number and message, tries to recover and continue, and prints a count; the first message is the most reliable.
- **evaluation / result rule:** Result: messages such as Bad.java:4: ';' expected ... 3 errors, and no Name.class; nothing of the program runs.
- **state-transition rule:** A failed compile leaves the file system without a new Name.class (an older one, if any, is not updated) and changes no program state.
- **composition rule (with a neighbour):** with compile: A compile-time error is reported while javac compiles Name.java, so no new Name.class is produced.
- **composition rule (with a neighbour):** with reading\_error\_messages: Each compile-time error comes with a message; reading it (first error first, line may be late) is how it is found and fixed.
- **composition rule (with a neighbour):** with run\_time\_error: A compile-time error is found by javac before the program runs; a run-time error only while it runs, so code that compiles can still crash.
- **plan / role rule:** Purpose (of the check): catch rule violations automatically before running, so they cannot cause wrong behaviour; S&amp;W say treat the compiler as a friend.
- **conservation rule:** Fixing the first error and recompiling can remove many messages at once; a single missing brace or semicolon can cause several messages.
- **error rule:** rule broken: Library static methods are called with the class name, e.g. Math.sqrt(x) (compile-time)
- **error rule:** rule broken: Every name must be spelled exactly, including capitalization (compile-time)
- **error rule:** rule broken: Each statement must end with ; (compile-time)
- **error rule:** rule broken: Every { must be matched by a } (compile-time)
- **error rule:** rule broken: A /\* comment needs its closing \*/ (compile-time)
- **error rule:** rule broken: A String literal is enclosed in a pair of double quotes (compile-time)
- **error rule:** rule broken: A final variable cannot be reassigned after it is initialized (compile-time)
- **error rule:** rule broken: Required keywords (class, static, void...) must be present and spelled right (compile-time)
- **applicability rule:** Expect compile-time errors for anything the compiler can check from the text alone (syntax, names, types, final); expect run-time or logic errors for faults that depend on input values or on what the program was meant to do.

## The whole prerequisite chain

- **Everything it builds on (2):** `compile`, `program_text`
- **Everything that builds on it (2):** `debugging`, `reading_error_messages`
