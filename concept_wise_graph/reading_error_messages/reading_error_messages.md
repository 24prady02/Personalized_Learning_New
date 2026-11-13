# reading_error_messages (`reading_error_messages`)

how to read compiler error messages: first error first; reported line may follow the real fault

Section 1.1 Your First Program, topic 1.1.c Errors.

![The knowledge graph around reading_error_messages](reading_error_messages.png)

## At a glance

- **Needs first:** `compile_time_error`
- **Leads to:** `debugging`
- **Learned alongside:** nothing
- **Misconceptions:** `CompilerSuggestionIsFix`, `ErrorLineIsFaultLine`, `FixEveryErrorMessage`
- **Errors:** none
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 19 edges around this concept, each explained in the graph's own words.

## What it needs first (1)

A prerequisite edge means the other concept has to be understood before `reading_error_messages`.

### `compile_time_error` comes before `reading_error_messages`

*an error javac reports before the program can run (syntax, types)*

Reading error messages is how compile-time errors are found and fixed.

- **Grounding:** book passage
- **How `reading_error_messages` combines with `compile_time_error`:** Compile-time errors are found and fixed by reading their messages; the message maps imperfectly to the fault.
- **How `compile_time_error` combines with `reading_error_messages`:** Each compile-time error comes with a message; reading it (first error first, line may be late) is how it is found and fixed.

## What it leads to (1)

These concepts need `reading_error_messages` first.

### `reading_error_messages` comes before `debugging`

*finding and fixing the cause of a wrong result or error by forming a hypothesis, changing the program and checking the prediction*

Reading an error message tells you where to start looking; debugging goes on from there to the cause.

- **Grounding:** book passage
- **How `debugging` combines with `reading_error_messages`:** An error message gives the place where Java noticed the problem; the cause may be earlier, so it is the start of the search, not the answer.

## Learned alongside (0)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

No parallel edge touches this concept.

## Misconceptions (3)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### CompilerSuggestionIsFix

- **Wrong rule:** Doing exactly what the compiler message suggests will fix the error.
- **Right rule:** An error message is evidence that something is wrong, but its suggested remedy may be wrong; find the actual cause.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: Doing exactly what the compiler message suggests will fix the error. Right rule: An error message is evidence that something is wrong, but its suggested remedy may be wrong; find the actual cause.
- **Also an edge from `compile_time_error`:** Doing exactly what the compiler message suggests will fix the error.
- **Also an edge from `debugging`:** Doing exactly what the compiler message suggests will fix the error.

### ErrorLineIsFaultLine

- **Wrong rule:** The line number in a javac error is always the line that has the mistake.
- **Right rule:** The compiler reports where it noticed the problem, which can be after the real fault; for example, omitting the second left brace of HelloWorld produces errors reported on later lines.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: The line number in a javac error is always the line that has the mistake. Right rule: The compiler reports where it noticed the problem, which can be after the real fault.
- **Shows at level L0 as:** inconsistent trace: Applies the read-first-error rule unevenly: starts from the first message on one compile but from the last on another, or looks only at the reported line without checking the lines before it. (here mixing in: "The line number in a javac error is always the line that has the mistake")
- **Also an edge from `compile_time_error`:** The line number in a javac error is always the line that has the mistake.
- **Also an edge from `debugging`:** The line number in a javac error is always the line that has the mistake.

### FixEveryErrorMessage

- **Wrong rule:** Each error message is a separate mistake that needs its own fix.
- **Right rule:** One fault can produce several messages; fix the first and recompile.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: Each error message is a separate mistake that needs its own fix. Right rule: One fault can produce several messages; fix the first and recompile.
- **Also an edge from `debugging`:** Each error message is a separate mistake that needs its own fix.

## Errors (0)

An error edge states the rule that gets broken in a program, and the right rule.

The graph has no error edge from this concept.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for reading error messages: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to reading error messages agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

reading error messages -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (5 ways).

- **everyday reading** (folk-meaning rule): Everyday reading: an error message is like a teacher's correction, naming the exact mistake, its line and its fix, one message per mistake. Java rule: the message reports what javac detected and where it noticed it; one fault can cause several messages and the suggested remedy may be wrong.
- **misconception** (wrong rule / right rule; shows `ErrorLineIsFaultLine`): wrong rule: The line number in a javac error is always the line that has the mistake. Right rule: The compiler reports where it noticed the problem, which can be after the real fault.
- **misconception** (wrong rule / right rule; shows `FixEveryErrorMessage`): wrong rule: Each error message is a separate mistake that needs its own fix. Right rule: One fault can produce several messages; fix the first and recompile.
- **misconception** (wrong rule / right rule; shows `CompilerSuggestionIsFix`): wrong rule: Doing exactly what the compiler message suggests will fix the error. Right rule: An error message is evidence that something is wrong, but its suggested remedy may be wrong; find the actual cause.
- **inconsistent trace** (uneven-application rule; shows `ErrorLineIsFaultLine`): Applies the read-first-error rule unevenly: starts from the first message on one compile but from the last on another, or looks only at the reported line without checking the lines before it. (here mixing in: "The line number in a javac error is always the line that has the mistake")

### L1: Unistructural / atom x text surface

L1 for reading error messages: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

reading error messages -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

- **names the element** (identity rule): Reading error messages is the debugging skill of interpreting a compiler (or JVM) message, File.java:line: description, to locate and fix the fault.
- **states the rule** (declarative rule): Each javac message gives the file, the line where the error was detected and a description; only the first message is truly reliable, and the real error is generally at or before the reported line.

### L2: Multistructural / block x execution / preoperational

L2 for reading error messages: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

reading error messages -&gt; L2 (Multistructural): the answer applies the rules of reading error messages to every part of the code, in order (3 ways).

- **line by line trace** (operational sequencing rule): Read the first message, go to its line, look there and then backwards for the cause, fix that one error, recompile, and repeat.
- **output prediction** (evaluation / result rule): Reading 'Bad.java:2: '{' expected' yields the location (file Bad.java, line 2) and the kind of problem (a missing left brace); with a later or vaguer message, it yields only where to start looking.
- **one step execution** (state-transition rule): One read-fix-recompile cycle removes one fault and often several messages; the message count after recompiling can drop sharply.

### L3: Relational / relations x function (concrete operational begins)

L3 for reading error messages: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

reading error messages -&gt; L3 (Relational): the answer relates the parts (3 ways).

- **relation to neighbour** (composition rule (with a neighbour)): Compile-time errors are found and fixed by reading their messages; the message maps imperfectly to the fault.
- **relation to neighbour** (composition rule (with a neighbour)): Reading an error message tells you where to start looking; debugging goes on from there to the cause.
- **purpose of the whole** (plan / role rule): Purpose: use the compiler as a friend that says something is wrong, turning its message into a hypothesis about the fault.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for reading error messages: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

reading error messages -&gt; L4 (Extended abstract): the answer reasons beyond the given code (5 ways).

- **predict a change** (conservation rule; shows `ErrorLineIsFaultLine`): Introducing a known mistake into a working program and reading the resulting message shows which messages a fault produces; adding a fault earlier in the file can change messages reported later.
- **transfer to a new program** (applicability rule): Read messages first-error-first whenever javac or the JVM reports an error; for logic errors there is no message, so use tracing and print statements instead.
- **diagnose an error** (error rule): rule broken: Reported line = where javac noticed the problem. Kind: compile-time. Trigger class: a missing brace or quote, reported lines later (e.g. reached end of file while parsing)
- **diagnose an error** (error rule): rule broken: Suggested remedies are unreliable. Kind: compile-time. Trigger class: a message whose literal advice (e.g. declare a class abstract) is wrong
- **diagnose an error** (error rule): rule broken: Run-time messages name the exception and the line. Kind: run-time exception. Trigger class: reading Exception in thread "main" java.lang.ArrayIndexOutOfBoundsException: 0 at UseArgument.main(UseArgument.java:6)

## Same topic

`reading_error_messages` belongs to the topic **Errors** (`topic1.1.c`). The topic also contains: `compile_time_error`, `logical_error`, `run_time_error`.

## Rules of the concept (17)

- **folk-meaning rule:** Everyday reading: an error message is like a teacher's correction, naming the exact mistake, its line and its fix, one message per mistake. Java rule: the message reports what javac detected and where it noticed it; one fault can cause several messages and the suggested remedy may be wrong.
- **wrong rule / right rule:** ErrorLineIsFaultLine: wrong: The line number in a javac error is always the line that has the mistake. \| right: The compiler reports where it noticed the problem, which can be after the real fault.
- **wrong rule / right rule:** FixEveryErrorMessage: wrong: Each error message is a separate mistake that needs its own fix. \| right: One fault can produce several messages; fix the first and recompile.
- **wrong rule / right rule:** CompilerSuggestionIsFix: wrong: Doing exactly what the compiler message suggests will fix the error. \| right: An error message is evidence that something is wrong, but its suggested remedy may be wrong; find the actual cause.
- **uneven-application rule:** Applies the read-first-error rule unevenly: starts from the first message on one compile but from the last on another, or looks only at the reported line without checking the lines before it.
- **identity rule:** Reading error messages is the debugging skill of interpreting a compiler (or JVM) message, File.java:line: description, to locate and fix the fault.
- **declarative rule:** Each javac message gives the file, the line where the error was detected and a description; only the first message is truly reliable, and the real error is generally at or before the reported line.
- **operational sequencing rule:** Read the first message, go to its line, look there and then backwards for the cause, fix that one error, recompile, and repeat.
- **evaluation / result rule:** Reading 'Bad.java:2: '{' expected' yields the location (file Bad.java, line 2) and the kind of problem (a missing left brace); with a later or vaguer message, it yields only where to start looking.
- **state-transition rule:** One read-fix-recompile cycle removes one fault and often several messages; the message count after recompiling can drop sharply.
- **composition rule (with a neighbour):** with compile\_time\_error: Compile-time errors are found and fixed by reading their messages; the message maps imperfectly to the fault.
- **plan / role rule:** Purpose: use the compiler as a friend that says something is wrong, turning its message into a hypothesis about the fault.
- **conservation rule:** Introducing a known mistake into a working program and reading the resulting message shows which messages a fault produces; adding a fault earlier in the file can change messages reported later.
- **error rule:** rule broken: Reported line = where javac noticed the problem (compile-time)
- **error rule:** rule broken: Suggested remedies are unreliable (compile-time)
- **error rule:** rule broken: Run-time messages name the exception and the line (run-time exception)
- **applicability rule:** Read messages first-error-first whenever javac or the JVM reports an error; for logic errors there is no message, so use tracing and print statements instead.

## The whole prerequisite chain

- **Everything it builds on (3):** `compile`, `compile_time_error`, `program_text`
- **Everything that builds on it (1):** `debugging`
