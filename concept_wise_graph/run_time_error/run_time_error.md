# run_time_error (`run_time_error`)

an error raised while the program executes (e.g. ArrayIndexOutOfBounds, NumberFormatException)

Section 1.1 Your First Program, topic 1.1.c Errors.

![The knowledge graph around run_time_error](run_time_error.png)

## At a glance

- **Needs first:** `array_bounds`, `division_by_zero`, `run`
- **Leads to:** nothing
- **Learned alongside:** `compile_time_error`, `logical_error`
- **Misconceptions:** `CompilesMeansWorks`, `DivisionByZeroIsCompileError`, `ParseAnyString`
- **Errors:** `ArgsAlwaysPresent`, `InputTypeMismatch`, `MainWithoutStringArgs`, `NegativeArraySize`
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 34 edges around this concept, each explained in the graph's own words.

## What it needs first (3)

A prerequisite edge means the other concept has to be understood before `run_time_error`.

### `array_bounds` comes before `run_time_error`

*valid indices are 0 .. length-1; otherwise throws*

An index outside 0 .. length-1 is not caught by the compiler; the access is checked when the program runs and stops it with ArrayIndexOutOfBoundsException.

- **Grounding:** book passage

### `division_by_zero` comes before `run_time_error`

*int division by zero throws; double division gives Infinity or NaN*

Dividing an int by zero compiles but throws ArithmeticException when the program runs: a run-time error.

- **Grounding:** spec passage

### `run` comes before `run_time_error`

*java executes main in the JVM*

A run-time error appears only while java Name executes, after compiling has succeeded.

- **Grounding:** book passage
- **How `run_time_error` combines with `run`:** A run-time error appears only while java Name executes, after compiling has succeeded.
- **How `run` combines with `run_time_error`:** A run-time error appears only while java Name executes; the JVM stops the program and prints the exception.

## What it leads to (0)

These concepts need `run_time_error` first.

No concept has this one as a prerequisite.

## Learned alongside (2)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

### `run_time_error` alongside `compile_time_error`

*an error javac reports before the program can run (syntax, types)*

A compile-time error is found by javac before the program runs; a run-time error is found while it runs.

- **Grounding:** book passage
- **How `run_time_error` combines with `compile_time_error`:** javac cannot detect it because it depends on run-time values (the argument typed, the divisor's value).
- **How `compile_time_error` combines with `run_time_error`:** A compile-time error is found by javac before the program runs; a run-time error only while it runs, so code that compiles can still crash.

### `run_time_error` alongside `logical_error`

*the program runs but computes the wrong result*

A run-time error stops the program with an exception; a logical error lets it finish with wrong output.

- **Grounding:** book passage
- **How `run_time_error` combines with `logical_error`:** A run-time error stops the program with an exception message; a logic error lets it finish with wrong output and no message.
- **How `logical_error` combines with `run_time_error`:** A run-time error stops the program with an exception; a logic error lets it finish with wrong output.

## Misconceptions (3)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### CompilesMeansWorks

- **Wrong rule:** Code that compiles is code that works.
- **Right rule:** Code that compiles can still have run-time and logical errors.
- **Role of this concept:** context
- **Shows at level L0 as:** misconception: wrong rule: Code that compiles is code that works. Right rule: Code that compiles can still fail at run time (an exception) or give wrong output.
- **Shows at level L0 as:** inconsistent trace: Applies the exception rule (LT: execution stops at the faulty statement) unevenly: lets the program keep printing after the failing statement on one trace, or reports the error before any earlier output on another. (here mixing in: "Code that compiles is code that works")
- **Also an edge from `compile`:** Code that compiles is code that works.
- **Also an edge from `compile_time_error`:** Code that compiles is code that works.
- **Also an edge from `logical_error`:** Code that compiles is code that works.
- **Also an edge from `testing`:** Code that compiles is code that works.

### DivisionByZeroIsCompileError

- **Wrong rule:** System.out.println(5 / 0); is rejected by the compiler.
- **Right rule:** It compiles; the ArithmeticException happens when the program runs.
- **Role of this concept:** context
- **Shows at level L0 as:** misconception: wrong rule: System.out.println(5 / 0); is rejected by the compiler. Right rule: It compiles; integer division by zero throws ArithmeticException when the statement runs.
- **Also an edge from `division_by_zero`:** System.out.println(5 / 0); is rejected by the compiler.

### ParseAnyString

- **Wrong rule:** Integer.parseInt works on any text, e.g. "five" or "12.2".
- **Right rule:** Integer.parseInt throws a NumberFormatException at run time when the string is not an integer written in digits.
- **Role of this concept:** context
- **Shows at level L0 as:** misconception: wrong rule: Integer.parseInt works on any text, e.g. "five" or "12.2". Right rule: Integer.parseInt throws a NumberFormatException at run time when the string is not an integer written in digits.
- **Also an edge from `parsing`:** Integer.parseInt works on any text, e.g. "five" or "12.2".

## Errors (4)

An error edge states the rule that gets broken in a program, and the right rule.

### ArgsAlwaysPresent

- **Wrong rule:** args[0] can always be read.
- **Right rule:** If you run the program without typing the command-line argument it expects, reading args[0] fails with java.lang.ArrayIndexOutOfBoundsException: 0.
- **Role of this concept:** context
- **Also an edge from `args_length`:** args[0] can always be read.
- **Also an edge from `command_line_args`:** args[0] can always be read.

### InputTypeMismatch

- **Wrong rule:** StdIn.readInt() accepts any typed text such as abc or 12.2.
- **Right rule:** If the next token is not an int (e.g. abc, 12.2, true), StdIn.readInt() throws a NumberFormatException at run time (Scanner.nextInt throws InputMismatchException).
- **Role of this concept:** context
- **Also an edge from `input_format`:** StdIn.readInt() accepts any typed text such as abc or 12.2.
- **Also an edge from `input_validation`:** StdIn.readInt() accepts any typed text such as abc or 12.2.
- **Also an edge from `standard_input`:** StdIn.readInt() accepts any typed text such as abc or 12.2.

### MainWithoutStringArgs

- **Wrong rule:** public static void main() is an acceptable entry point.
- **Right rule:** main is written public static void main(String[] args); these keywords and the args parameter are required.
- **Role of this concept:** context
- **Also an edge from `main_method`:** public static void main() is an acceptable entry point.

### NegativeArraySize

- **Wrong rule:** new int[n] with a negative n creates an empty array.
- **Right rule:** Creating an array with a negative length throws NegativeArraySizeException at run time.
- **Role of this concept:** context
- **Also an edge from `array_creation`:** new int[n] with a negative n creates an empty array.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for run time error: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to run time error agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

run time error -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (5 ways).

- **everyday reading** (folk-meaning rule): Everyday reading: if the program compiled, the computer has accepted it, so any problem would have been reported then. Java rule: run-time errors are detected only while the program executes, on particular data (e.g. no argument, a divisor of 0), and stop it with an exception.
- **misconception** (wrong rule / right rule; shows `CompilesMeansWorks`): wrong rule: Code that compiles is code that works. Right rule: Code that compiles can still fail at run time (an exception) or give wrong output.
- **misconception** (wrong rule / right rule; shows `DivisionByZeroIsCompileError`): wrong rule: System.out.println(5 / 0); is rejected by the compiler. Right rule: It compiles; integer division by zero throws ArithmeticException when the statement runs.
- **inconsistent trace** (uneven-application rule; shows `CompilesMeansWorks`): Applies the exception rule (LT: execution stops at the faulty statement) unevenly: lets the program keep printing after the failing statement on one trace, or reports the error before any earlier output on another. (here mixing in: "Code that compiles is code that works")
- **misconception** (wrong rule / right rule; shows `ParseAnyString`): wrong rule: Integer.parseInt works on any text, e.g. "five" or "12.2". Right rule: Integer.parseInt throws a NumberFormatException at run time when the string is not an integer written in digits.

### L1: Unistructural / atom x text surface

L1 for run time error: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

run time error -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

- **names the element** (identity rule): A run-time error (exception) is an error that does not show up until the program is executed and makes it impossible to run to completion.
- **states the rule** (declarative rule): When a run-time error occurs, the program 'crashes' (terminates) and the JVM prints the exception name, a message, and the method, file and line where it happened.

### L2: Multistructural / block x execution / preoperational

L2 for run time error: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

run time error -&gt; L2 (Multistructural): the answer applies the rules of run time error to every part of the code, in order (3 ways).

- **line by line trace** (operational sequencing rule): Statements before the faulty one run normally (their output appears); the faulty statement throws; no later statement runs.
- **output prediction** (evaluation / result rule): Output: any earlier output, then Exception in thread "main" java.lang.&lt;Name&gt;: &lt;detail&gt; at Class.main(Class.java:&lt;line&gt;).
- **one step execution** (state-transition rule): The throwing step changes no variable it was meant to set (the operation does not complete) and transfers control out of main, ending the program.

### L3: Relational / relations x function (concrete operational begins)

L3 for run time error: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

run time error -&gt; L3 (Relational): the answer relates the parts (4 ways).

- **relation to neighbour** (composition rule (with a neighbour)): A run-time error appears only while java Name executes, after compiling has succeeded.
- **relation to neighbour** (composition rule (with a neighbour)): javac cannot detect it because it depends on run-time values (the argument typed, the divisor's value).
- **relation to neighbour** (composition rule (with a neighbour)): A run-time error stops the program with an exception message; a logic error lets it finish with wrong output and no message.
- **purpose of the whole** (plan / role rule): Purpose (of exceptions): stop the program at the point where something impossible was asked, instead of continuing with an undefined value, and report what and where.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for run time error: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

run time error -&gt; L4 (Extended abstract): the answer reasons beyond the given code (8 ways).

- **predict a change** (conservation rule; shows `CompilesMeansWorks`): The same compiled program may run fine on one input and throw on another (UseArgument with and without an argument); adding a guard such as checking args.length removes the trigger without changing correct runs.
- **diagnose an error** (error rule): rule broken: main is written public static void main(String[] args). Kind: launch error. Trigger class: header public static void main(): compiles, but java Name cannot find the main method
- **diagnose an error** (error rule): rule broken: Array length must be &gt;= 0. Kind: run-time exception. Trigger class: new int[n] with n &lt; 0: NegativeArraySizeException
- **diagnose an error** (error rule): rule broken: args[k] exists only if at least k+1 arguments were typed. Kind: run-time exception. Trigger class: running without the expected argument: java.lang.ArrayIndexOutOfBoundsException: 0
- **transfer to a new program** (applicability rule): Expect a run-time error when correctness depends on data (array indices, divisors, parsed input, presence of arguments); validate such data before use. Errors that depend only on the text are compile-time; wrong-but-legal results are logic errors.
- **diagnose an error** (error rule): rule broken: StdIn.readInt() needs the next token to be an int. Kind: run-time exception. Trigger class: next token abc, 12.2 or true (StdIn: InputMismatchException/NumberFormatException depending on version; Scanner.nextInt: InputMismatchException)
- **diagnose an error** (error rule): rule broken: Integer division and remainder by zero are undefined. Kind: run-time exception. Trigger class: a / b or a % b with int b == 0: ArithmeticException: / by zero
- **diagnose an error** (error rule): rule broken: Integer.parseInt needs an integer written in digits. Kind: run-time exception. Trigger class: parsing "five" or "12.2": NumberFormatException

## Same topic

`run_time_error` belongs to the topic **Errors** (`topic1.1.c`). The topic also contains: `compile_time_error`, `logical_error`, `reading_error_messages`.

## Rules of the concept (22)

- **folk-meaning rule:** Everyday reading: if the program compiled, the computer has accepted it, so any problem would have been reported then. Java rule: run-time errors are detected only while the program executes, on particular data (e.g. no argument, a divisor of 0), and stop it with an exception.
- **wrong rule / right rule:** CompilesMeansWorks: wrong: Code that compiles is code that works. \| right: Code that compiles can still fail at run time (an exception) or give wrong output.
- **wrong rule / right rule:** DivisionByZeroIsCompileError: wrong: System.out.println(5 / 0); is rejected by the compiler. \| right: It compiles; integer division by zero throws ArithmeticException when the statement runs.
- **wrong rule / right rule:** ParseAnyString: wrong: Integer.parseInt works on any text, e.g. "five" or "12.2". \| right: Integer.parseInt throws a NumberFormatException at run time when the string is not an integer written in digits.
- **uneven-application rule:** Applies the exception rule (LT: execution stops at the faulty statement) unevenly: lets the program keep printing after the failing statement on one trace, or reports the error before any earlier output on another.
- **identity rule:** A run-time error (exception) is an error that does not show up until the program is executed and makes it impossible to run to completion.
- **declarative rule:** When a run-time error occurs, the program 'crashes' (terminates) and the JVM prints the exception name, a message, and the method, file and line where it happened.
- **operational sequencing rule:** Statements before the faulty one run normally (their output appears); the faulty statement throws; no later statement runs.
- **evaluation / result rule:** Output: any earlier output, then Exception in thread "main" java.lang.&lt;Name&gt;: &lt;detail&gt; at Class.main(Class.java:&lt;line&gt;).
- **state-transition rule:** The throwing step changes no variable it was meant to set (the operation does not complete) and transfers control out of main, ending the program.
- **composition rule (with a neighbour):** with run: A run-time error appears only while java Name executes, after compiling has succeeded.
- **composition rule (with a neighbour):** with compile\_time\_error: javac cannot detect it because it depends on run-time values (the argument typed, the divisor's value).
- **composition rule (with a neighbour):** with logical\_error: A run-time error stops the program with an exception message; a logic error lets it finish with wrong output and no message.
- **plan / role rule:** Purpose (of exceptions): stop the program at the point where something impossible was asked, instead of continuing with an undefined value, and report what and where.
- **conservation rule:** The same compiled program may run fine on one input and throw on another (UseArgument with and without an argument); adding a guard such as checking args.length removes the trigger without changing correct runs.
- **error rule:** rule broken: args[k] exists only if at least k+1 arguments were typed (run-time exception)
- **error rule:** rule broken: main is written public static void main(String[] args) (launch error)
- **error rule:** rule broken: Array length must be &gt;= 0 (run-time exception)
- **error rule:** rule broken: StdIn.readInt() needs the next token to be an int (run-time exception)
- **error rule:** rule broken: Integer division and remainder by zero are undefined (run-time exception)
- **error rule:** rule broken: Integer.parseInt needs an integer written in digits (run-time exception)
- **applicability rule:** Expect a run-time error when correctness depends on data (array indices, divisors, parsed input, presence of arguments); validate such data before use. Errors that depend only on the text are compile-time; wrong-but-legal results are logic errors.

## The whole prerequisite chain

- **Everything it builds on (14):** `arithmetic_operators`, `array_bounds`, `array_creation`, `array_declaration`, `array_initializer`, `compile`, `data_structure`, `data_type`, `division_by_zero`, `double`, `indexing`, `primitive_type`, `program_text`, `run`
- **Everything that builds on it (0):** nothing
