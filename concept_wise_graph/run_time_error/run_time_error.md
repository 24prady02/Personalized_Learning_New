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

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 34 edges around this concept. The edge logic, the wrong and right rules and the exact rules of the ways are copied word for word from the graph.

## To work on (0)

Nothing is missing for this concept.

## What it needs first (3)

A prerequisite edge means the other concept has to be understood before `run_time_error`.

### `array_bounds` comes before `run_time_error`

*valid indices are 0 .. length-1; otherwise throws*

- **Edge:** `pre:array_bounds->run_time_error`
- **Exact edge logic:** An index outside 0 .. length-1 is not caught by the compiler; the access is checked when the program runs and stops it with ArrayIndexOutOfBoundsException.
- **Grounding:** book\_passage

### `division_by_zero` comes before `run_time_error`

*int division by zero throws; double division gives Infinity or NaN*

- **Edge:** `pre:division_by_zero->run_time_error`
- **Exact edge logic:** Dividing an int by zero compiles but throws ArithmeticException when the program runs: a run-time error.
- **Grounding:** spec\_passage

### `run` comes before `run_time_error`

*java executes main in the JVM*

- **Edge:** `pre:run->run_time_error`
- **Exact edge logic:** A run-time error appears only while java Name executes, after compiling has succeeded.
- **Grounding:** book\_passage
- **Composition rule (R) of `run_time_error` with `run`:** A run-time error appears only while java Name executes, after compiling has succeeded.
- **Composition rule (R) of `run` with `run_time_error`:** A run-time error appears only while java Name executes; the JVM stops the program and prints the exception.

## What it leads to (0)

These concepts need `run_time_error` first.

No concept has this one as a prerequisite.

## Learned alongside (2)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

### `run_time_error` alongside `compile_time_error`

*an error javac reports before the program can run (syntax, types)*

- **Edge:** `par:compile_time_error~run_time_error`
- **Exact edge logic:** A compile-time error is found by javac before the program runs; a run-time error is found while it runs.
- **Grounding:** book\_passage
- **Composition rule (R) of `run_time_error` with `compile_time_error`:** javac cannot detect it because it depends on run-time values (the argument typed, the divisor's value).
- **Composition rule (R) of `compile_time_error` with `run_time_error`:** A compile-time error is found by javac before the program runs; a run-time error only while it runs, so code that compiles can still crash.

### `run_time_error` alongside `logical_error`

*the program runs but computes the wrong result*

- **Edge:** `par:run_time_error~logical_error`
- **Exact edge logic:** A run-time error stops the program with an exception; a logical error lets it finish with wrong output.
- **Grounding:** book\_passage
- **Composition rule (R) of `run_time_error` with `logical_error`:** A run-time error stops the program with an exception message; a logic error lets it finish with wrong output and no message.
- **Composition rule (R) of `logical_error` with `run_time_error`:** A run-time error stops the program with an exception; a logic error lets it finish with wrong output.

## Misconceptions (3)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### CompilesMeansWorks

- **Edge:** `run_time_error` &rarr; `CompilesMeansWorks` (misconception)
- **Exact edge logic (the wrong rule):** Code that compiles is code that works.
- **Twin logic (the right rule):** Code that compiles can still have run-time and logical errors.
- **Wrong belief (on the node):** Code that compiles is code that works.
- **Correct rule (on the node):** Code that compiles can still have run-time and logical errors.
- **Provenance:** published
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [1] misconception, exact rule:** wrong rule: Code that compiles is code that works. Right rule: Code that compiles can still fail at run time (an exception) or give wrong output.
- **L0 way [3] inconsistent\_trace, exact rule:** Applies the exception rule (LT: execution stops at the faulty statement) unevenly: lets the program keep printing after the failing statement on one trace, or reports the error before any earlier output on another. (here mixing in: "Code that compiles is code that works")
- **Edge `compile` &rarr; `CompilesMeansWorks`, exact edge logic:** Code that compiles is code that works. **Twin logic:** Code that compiles can still have run-time and logical errors. (role: primary)
- **Edge `compile_time_error` &rarr; `CompilesMeansWorks`, exact edge logic:** Code that compiles is code that works. **Twin logic:** Code that compiles can still have run-time and logical errors. (role: context)
- **Edge `logical_error` &rarr; `CompilesMeansWorks`, exact edge logic:** Code that compiles is code that works. **Twin logic:** Code that compiles can still have run-time and logical errors. (role: context)
- **Edge `testing` &rarr; `CompilesMeansWorks`, exact edge logic:** Code that compiles is code that works. **Twin logic:** Code that compiles can still have run-time and logical errors. (role: context)

### DivisionByZeroIsCompileError

- **Edge:** `run_time_error` &rarr; `DivisionByZeroIsCompileError` (misconception)
- **Exact edge logic (the wrong rule):** System.out.println(5 / 0); is rejected by the compiler.
- **Twin logic (the right rule):** It compiles; the ArithmeticException happens when the program runs.
- **Wrong belief (on the node):** System.out.println(5 / 0); is rejected by the compiler.
- **Correct rule (on the node):** It compiles; the ArithmeticException happens when the program runs.
- **Provenance:** textbook
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [2] misconception, exact rule:** wrong rule: System.out.println(5 / 0); is rejected by the compiler. Right rule: It compiles; integer division by zero throws ArithmeticException when the statement runs.
- **Edge `division_by_zero` &rarr; `DivisionByZeroIsCompileError`, exact edge logic:** System.out.println(5 / 0); is rejected by the compiler. **Twin logic:** It compiles; the ArithmeticException happens when the program runs. (role: primary)

### ParseAnyString

- **Edge:** `run_time_error` &rarr; `ParseAnyString` (misconception)
- **Exact edge logic (the wrong rule):** Integer.parseInt works on any text, e.g. "five" or "12.2".
- **Twin logic (the right rule):** Integer.parseInt throws a NumberFormatException at run time when the string is not an integer written in digits.
- **Wrong belief (on the node):** Integer.parseInt works on any text, e.g. "five" or "12.2".
- **Correct rule (on the node):** Integer.parseInt throws a NumberFormatException at run time when the string is not an integer written in digits.
- **Provenance:** textbook
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [4] misconception, exact rule:** wrong rule: Integer.parseInt works on any text, e.g. "five" or "12.2". Right rule: Integer.parseInt throws a NumberFormatException at run time when the string is not an integer written in digits.
- **Edge `parsing` &rarr; `ParseAnyString`, exact edge logic:** Integer.parseInt works on any text, e.g. "five" or "12.2". **Twin logic:** Integer.parseInt throws a NumberFormatException at run time when the string is not an integer written in digits. (role: primary)

## Errors (4)

An error edge states the rule that gets broken in a program, and the right rule.

### ArgsAlwaysPresent

- **Edge:** `run_time_error` &rarr; `ArgsAlwaysPresent` (error)
- **Exact edge logic (the wrong rule):** args[0] can always be read.
- **Twin logic (the right rule):** If you run the program without typing the command-line argument it expects, reading args[0] fails with java.lang.ArrayIndexOutOfBoundsException: 0.
- **Wrong belief (on the node):** args[0] can always be read.
- **Correct rule (on the node):** If you run the program without typing the command-line argument it expects, reading args[0] fails with java.lang.ArrayIndexOutOfBoundsException: 0.
- **Provenance:** textbook
- **Role of this concept:** context
- **Edge `args_length` &rarr; `ArgsAlwaysPresent`, exact edge logic:** args[0] can always be read. **Twin logic:** If you run the program without typing the command-line argument it expects, reading args[0] fails with java.lang.ArrayIndexOutOfBoundsException: 0. (role: primary)
- **Edge `command_line_args` &rarr; `ArgsAlwaysPresent`, exact edge logic:** args[0] can always be read. **Twin logic:** If you run the program without typing the command-line argument it expects, reading args[0] fails with java.lang.ArrayIndexOutOfBoundsException: 0. (role: context)

### InputTypeMismatch

- **Edge:** `run_time_error` &rarr; `InputTypeMismatch` (error)
- **Exact edge logic (the wrong rule):** StdIn.readInt() accepts any typed text such as abc or 12.2.
- **Twin logic (the right rule):** If the next token is not an int (e.g. abc, 12.2, true), StdIn.readInt() throws a NumberFormatException at run time (Scanner.nextInt throws InputMismatchException).
- **Wrong belief (on the node):** StdIn.readInt() accepts any typed text such as abc or 12.2.
- **Correct rule (on the node):** If the next token is not an int (e.g. abc, 12.2, true), StdIn.readInt() throws a NumberFormatException at run time (Scanner.nextInt throws InputMismatchException).
- **Provenance:** textbook
- **Role of this concept:** context
- **Edge `input_format` &rarr; `InputTypeMismatch`, exact edge logic:** StdIn.readInt() accepts any typed text such as abc or 12.2. **Twin logic:** If the next token is not an int (e.g. abc, 12.2, true), StdIn.readInt() throws a NumberFormatException at run time (Scanner.nextInt throws InputMismatchException). (role: primary)
- **Edge `input_validation` &rarr; `InputTypeMismatch`, exact edge logic:** StdIn.readInt() accepts any typed text such as abc or 12.2. **Twin logic:** If the next token is not an int (e.g. abc, 12.2, true), StdIn.readInt() throws a NumberFormatException at run time (Scanner.nextInt throws InputMismatchException). (role: context)
- **Edge `standard_input` &rarr; `InputTypeMismatch`, exact edge logic:** StdIn.readInt() accepts any typed text such as abc or 12.2. **Twin logic:** If the next token is not an int (e.g. abc, 12.2, true), StdIn.readInt() throws a NumberFormatException at run time (Scanner.nextInt throws InputMismatchException). (role: context)

### MainWithoutStringArgs

- **Edge:** `run_time_error` &rarr; `MainWithoutStringArgs` (error)
- **Exact edge logic (the wrong rule):** public static void main() is an acceptable entry point.
- **Twin logic (the right rule):** main is written public static void main(String[] args); these keywords and the args parameter are required.
- **Wrong belief (on the node):** public static void main() is an acceptable entry point.
- **Correct rule (on the node):** main is written public static void main(String[] args); these keywords and the args parameter are required.
- **Provenance:** textbook
- **Role of this concept:** context
- **Edge `main_method` &rarr; `MainWithoutStringArgs`, exact edge logic:** public static void main() is an acceptable entry point. **Twin logic:** main is written public static void main(String[] args); these keywords and the args parameter are required. (role: primary)

### NegativeArraySize

- **Edge:** `run_time_error` &rarr; `NegativeArraySize` (error)
- **Exact edge logic (the wrong rule):** new int[n] with a negative n creates an empty array.
- **Twin logic (the right rule):** Creating an array with a negative length throws NegativeArraySizeException at run time.
- **Wrong belief (on the node):** new int[n] with a negative n creates an empty array.
- **Correct rule (on the node):** Creating an array with a negative length throws NegativeArraySizeException at run time.
- **Provenance:** textbook
- **Role of this concept:** context
- **Edge `array_creation` &rarr; `NegativeArraySize`, exact edge logic:** new int[n] with a negative n creates an empty array. **Twin logic:** Creating an array with a negative length throws NegativeArraySizeException at run time. (role: primary)

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for run time error: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to run time error agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

- **Edge:** `run_time_error` &rarr; `run_time_error@L0` (has_level)
- **Exact edge logic:** run time error -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (5 ways).

Ways (5), each with its exact rule:

- **[0] everyday\_reading** (rule type E, folk-meaning rule): Everyday reading: if the program compiled, the computer has accepted it, so any problem would have been reported then. Java rule: run-time errors are detected only while the program executes, on particular data (e.g. no argument, a divisor of 0), and stop it with an exception.
- **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `CompilesMeansWorks`: wrong rule: Code that compiles is code that works. Right rule: Code that compiles can still fail at run time (an exception) or give wrong output.
- **[2] misconception** (rule type M, wrong rule / right rule) &rarr; `DivisionByZeroIsCompileError`: wrong rule: System.out.println(5 / 0); is rejected by the compiler. Right rule: It compiles; integer division by zero throws ArithmeticException when the statement runs.
- **[3] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `CompilesMeansWorks`: Applies the exception rule (LT: execution stops at the faulty statement) unevenly: lets the program keep printing after the failing statement on one trace, or reports the error before any earlier output on another. (here mixing in: "Code that compiles is code that works")
- **[4] misconception** (rule type M, wrong rule / right rule) &rarr; `ParseAnyString`: wrong rule: Integer.parseInt works on any text, e.g. "five" or "12.2". Right rule: Integer.parseInt throws a NumberFormatException at run time when the string is not an integer written in digits.

### L1: Unistructural / atom x text surface

L1 for run time error: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

- **Edge:** `run_time_error` &rarr; `run_time_error@L1` (has_level)
- **Exact edge logic:** run time error -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

Ways (2), each with its exact rule:

- **[0] names\_the\_element** (rule type N, identity rule): A run-time error (exception) is an error that does not show up until the program is executed and makes it impossible to run to completion.
- **[1] states\_the\_rule** (rule type S, declarative rule): When a run-time error occurs, the program 'crashes' (terminates) and the JVM prints the exception name, a message, and the method, file and line where it happened.

### L2: Multistructural / block x execution / preoperational

L2 for run time error: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

- **Edge:** `run_time_error` &rarr; `run_time_error@L2` (has_level)
- **Exact edge logic:** run time error -&gt; L2 (Multistructural): the answer applies the rules of run time error to every part of the code, in order (3 ways).

Ways (3), each with its exact rule:

- **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): Statements before the faulty one run normally (their output appears); the faulty statement throws; no later statement runs.
- **[1] output\_prediction** (rule type OP, evaluation / result rule): Output: any earlier output, then Exception in thread "main" java.lang.&lt;Name&gt;: &lt;detail&gt; at Class.main(Class.java:&lt;line&gt;).
- **[2] one\_step\_execution** (rule type OS, state-transition rule): The throwing step changes no variable it was meant to set (the operation does not complete) and transfers control out of main, ending the program.

### L3: Relational / relations x function (concrete operational begins)

L3 for run time error: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

- **Edge:** `run_time_error` &rarr; `run_time_error@L3` (has_level)
- **Exact edge logic:** run time error -&gt; L3 (Relational): the answer relates the parts (4 ways).

Ways (4), each with its exact rule:

- **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): A run-time error appears only while java Name executes, after compiling has succeeded.
- **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): javac cannot detect it because it depends on run-time values (the argument typed, the divisor's value).
- **[2] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): A run-time error stops the program with an exception message; a logic error lets it finish with wrong output and no message.
- **[3] purpose\_of\_the\_whole** (rule type P, plan / role rule): Purpose (of exceptions): stop the program at the point where something impossible was asked, instead of continuing with an undefined value, and report what and where.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for run time error: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

- **Edge:** `run_time_error` &rarr; `run_time_error@L4` (has_level)
- **Exact edge logic:** run time error -&gt; L4 (Extended abstract): the answer reasons beyond the given code (8 ways).

Ways (8), each with its exact rule:

- **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `CompilesMeansWorks`: The same compiled program may run fine on one input and throw on another (UseArgument with and without an argument); adding a guard such as checking args.length removes the trigger without changing correct runs.
- **[1] diagnose\_an\_error** (rule type D, error rule): rule broken: main is written public static void main(String[] args). Kind: launch error. Trigger class: header public static void main(): compiles, but java Name cannot find the main method
- **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: Array length must be &gt;= 0. Kind: run-time exception. Trigger class: new int[n] with n &lt; 0: NegativeArraySizeException
- **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: args[k] exists only if at least k+1 arguments were typed. Kind: run-time exception. Trigger class: running without the expected argument: java.lang.ArrayIndexOutOfBoundsException: 0
- **[4] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Expect a run-time error when correctness depends on data (array indices, divisors, parsed input, presence of arguments); validate such data before use. Errors that depend only on the text are compile-time; wrong-but-legal results are logic errors.
- **[5] diagnose\_an\_error** (rule type D, error rule): rule broken: StdIn.readInt() needs the next token to be an int. Kind: run-time exception. Trigger class: next token abc, 12.2 or true (StdIn: InputMismatchException/NumberFormatException depending on version; Scanner.nextInt: InputMismatchException)
- **[6] diagnose\_an\_error** (rule type D, error rule): rule broken: Integer division and remainder by zero are undefined. Kind: run-time exception. Trigger class: a / b or a % b with int b == 0: ArithmeticException: / by zero
- **[7] diagnose\_an\_error** (rule type D, error rule): rule broken: Integer.parseInt needs an integer written in digits. Kind: run-time exception. Trigger class: parsing "five" or "12.2": NumberFormatException

## Same topic

`run_time_error` belongs to the topic **Errors** (`topic1.1.c`). The topic also contains: `compile_time_error`, `logical_error`, `reading_error_messages`.

## Rules of the concept (22)

- **Book** (SW-1e, p. 8 (pdf 18)): "Other errors, known as run-time errors, do not show up until you execute the program."
- **Book** (SW-1.1, ): "These errors are caught by the system when we execute the program, because the program tries"
- **E** (folk-meaning rule): Everyday reading: if the program compiled, the computer has accepted it, so any problem would have been reported then. Java rule: run-time errors are detected only while the program executes, on particular data (e.g. no argument, a divisor of 0), and stop it with an exception.
- **M** (wrong rule / right rule): CompilesMeansWorks: wrong: Code that compiles is code that works. \| right: Code that compiles can still fail at run time (an exception) or give wrong output.
- **M** (wrong rule / right rule): DivisionByZeroIsCompileError: wrong: System.out.println(5 / 0); is rejected by the compiler. \| right: It compiles; integer division by zero throws ArithmeticException when the statement runs.
- **M** (wrong rule / right rule): ParseAnyString: wrong: Integer.parseInt works on any text, e.g. "five" or "12.2". \| right: Integer.parseInt throws a NumberFormatException at run time when the string is not an integer written in digits.
- **T** (uneven-application rule): Applies the exception rule (LT: execution stops at the faulty statement) unevenly: lets the program keep printing after the failing statement on one trace, or reports the error before any earlier output on another.
- **N** (identity rule): A run-time error (exception) is an error that does not show up until the program is executed and makes it impossible to run to completion.
- **S** (declarative rule): When a run-time error occurs, the program 'crashes' (terminates) and the JVM prints the exception name, a message, and the method, file and line where it happened.
- **LT** (operational sequencing rule): Statements before the faulty one run normally (their output appears); the faulty statement throws; no later statement runs.
- **OP** (evaluation / result rule): Output: any earlier output, then Exception in thread "main" java.lang.&lt;Name&gt;: &lt;detail&gt; at Class.main(Class.java:&lt;line&gt;).
- **OS** (state-transition rule): The throwing step changes no variable it was meant to set (the operation does not complete) and transfers control out of main, ending the program.
- **R** (composition rule (with a neighbour)): with run: A run-time error appears only while java Name executes, after compiling has succeeded.
- **R** (composition rule (with a neighbour)): with compile\_time\_error: javac cannot detect it because it depends on run-time values (the argument typed, the divisor's value).
- **R** (composition rule (with a neighbour)): with logical\_error: A run-time error stops the program with an exception message; a logic error lets it finish with wrong output and no message.
- **P** (plan / role rule): Purpose (of exceptions): stop the program at the point where something impossible was asked, instead of continuing with an undefined value, and report what and where.
- **C** (conservation rule): The same compiled program may run fine on one input and throw on another (UseArgument with and without an argument); adding a guard such as checking args.length removes the trigger without changing correct runs.
- **D** (error rule): rule broken: args[k] exists only if at least k+1 arguments were typed (run-time exception)
- **D** (error rule): rule broken: main is written public static void main(String[] args) (launch error)
- **D** (error rule): rule broken: Array length must be &gt;= 0 (run-time exception)
- **D** (error rule): rule broken: StdIn.readInt() needs the next token to be an int (run-time exception)
- **D** (error rule): rule broken: Integer division and remainder by zero are undefined (run-time exception)
- **D** (error rule): rule broken: Integer.parseInt needs an integer written in digits (run-time exception)
- **X** (applicability rule): Expect a run-time error when correctness depends on data (array indices, divisors, parsed input, presence of arguments); validate such data before use. Errors that depend only on the text are compile-time; wrong-but-legal results are logic errors.

## How it is found in code and answers (reader block)

- **Aliases:** runtime error, run time error, run-time error, exception, crash, crashes
- **Code patterns:** `\bargs\s*\[\s*[1-9]\d*\s*\]`, `Integer\.parseInt\s*\(`, `Double\.parseDouble\s*\(`, `/\s*0(?![.\d])`, `%\s*0(?![.\d])`, `\[\s*\w+\.length\s*\]`, `<=\s*\w+\.length\b`, `\[\s*-\s*\d+\s*\]`, `\bnew\s+\w+\s*\[\s*-\s*\d+\s*\]`
- **Operator symbols:** none
- **Java types:** none
- **Signal zero\_divisor\_in\_variable** (scope program): `\b(?:int|long)\s+(?:\w+\s*=[^,;]*,\s*)*(\w+)\s*=\s*0\s*[,;](?:(?!\b\1\s*(?:!=\s*0|=(?!=)))[\s\S]){0,4000}?[/%]\s*\b\1\b(?!\s*[.\[(])`

## The whole prerequisite chain

- **Everything it builds on (14):** `arithmetic_operators`, `array_bounds`, `array_creation`, `array_declaration`, `array_initializer`, `compile`, `data_structure`, `data_type`, `division_by_zero`, `double`, `indexing`, `primitive_type`, `program_text`, `run`
- **Everything that builds on it (0):** nothing

## Every edge in this view and its exact edge logic (34)

All the edges drawn in the picture, in the order: prerequisite, parallel, misconception, error, has_level, contains.

**1. `array_bounds` &rarr; `run_time_error`** (prerequisite)

- **Exact edge logic:** An index outside 0 .. length-1 is not caught by the compiler; the access is checked when the program runs and stops it with ArrayIndexOutOfBoundsException.
- **Grounding:** book\_passage

**2. `division_by_zero` &rarr; `run_time_error`** (prerequisite)

- **Exact edge logic:** Dividing an int by zero compiles but throws ArithmeticException when the program runs: a run-time error.
- **Grounding:** spec\_passage

**3. `run` &rarr; `run_time_error`** (prerequisite)

- **Exact edge logic:** A run-time error appears only while java Name executes, after compiling has succeeded.
- **Grounding:** book\_passage
- **Composition rule (R) of `run` with `run_time_error`:** A run-time error appears only while java Name executes; the JVM stops the program and prints the exception.
- **Composition rule (R) of `run_time_error` with `run`:** A run-time error appears only while java Name executes, after compiling has succeeded.

**4. `compile_time_error` &harr; `run_time_error`** (parallel)

- **Exact edge logic:** A compile-time error is found by javac before the program runs; a run-time error is found while it runs.
- **Grounding:** book\_passage
- **Composition rule (R) of `compile_time_error` with `run_time_error`:** A compile-time error is found by javac before the program runs; a run-time error only while it runs, so code that compiles can still crash.
- **Composition rule (R) of `run_time_error` with `compile_time_error`:** javac cannot detect it because it depends on run-time values (the argument typed, the divisor's value).

**5. `run_time_error` &harr; `logical_error`** (parallel)

- **Exact edge logic:** A run-time error stops the program with an exception; a logical error lets it finish with wrong output.
- **Grounding:** book\_passage
- **Composition rule (R) of `run_time_error` with `logical_error`:** A run-time error stops the program with an exception message; a logic error lets it finish with wrong output and no message.
- **Composition rule (R) of `logical_error` with `run_time_error`:** A run-time error stops the program with an exception; a logic error lets it finish with wrong output.

**6. `run_time_error` &rarr; `CompilesMeansWorks`** (misconception)

- **Exact edge logic (the wrong rule):** Code that compiles is code that works.
- **Twin logic (the right rule):** Code that compiles can still have run-time and logical errors.
- **Role:** context

**7. `run_time_error` &rarr; `DivisionByZeroIsCompileError`** (misconception)

- **Exact edge logic (the wrong rule):** System.out.println(5 / 0); is rejected by the compiler.
- **Twin logic (the right rule):** It compiles; the ArithmeticException happens when the program runs.
- **Role:** context

**8. `run_time_error` &rarr; `ParseAnyString`** (misconception)

- **Exact edge logic (the wrong rule):** Integer.parseInt works on any text, e.g. "five" or "12.2".
- **Twin logic (the right rule):** Integer.parseInt throws a NumberFormatException at run time when the string is not an integer written in digits.
- **Role:** context

**9. `compile` &rarr; `CompilesMeansWorks`** (misconception)

- **Exact edge logic (the wrong rule):** Code that compiles is code that works.
- **Twin logic (the right rule):** Code that compiles can still have run-time and logical errors.
- **Role:** primary

**10. `compile_time_error` &rarr; `CompilesMeansWorks`** (misconception)

- **Exact edge logic (the wrong rule):** Code that compiles is code that works.
- **Twin logic (the right rule):** Code that compiles can still have run-time and logical errors.
- **Role:** context

**11. `division_by_zero` &rarr; `DivisionByZeroIsCompileError`** (misconception)

- **Exact edge logic (the wrong rule):** System.out.println(5 / 0); is rejected by the compiler.
- **Twin logic (the right rule):** It compiles; the ArithmeticException happens when the program runs.
- **Role:** primary

**12. `logical_error` &rarr; `CompilesMeansWorks`** (misconception)

- **Exact edge logic (the wrong rule):** Code that compiles is code that works.
- **Twin logic (the right rule):** Code that compiles can still have run-time and logical errors.
- **Role:** context

**13. `parsing` &rarr; `ParseAnyString`** (misconception)

- **Exact edge logic (the wrong rule):** Integer.parseInt works on any text, e.g. "five" or "12.2".
- **Twin logic (the right rule):** Integer.parseInt throws a NumberFormatException at run time when the string is not an integer written in digits.
- **Role:** primary

**14. `testing` &rarr; `CompilesMeansWorks`** (misconception)

- **Exact edge logic (the wrong rule):** Code that compiles is code that works.
- **Twin logic (the right rule):** Code that compiles can still have run-time and logical errors.
- **Role:** context

**15. `run_time_error` &rarr; `ArgsAlwaysPresent`** (error)

- **Exact edge logic (the wrong rule):** args[0] can always be read.
- **Twin logic (the right rule):** If you run the program without typing the command-line argument it expects, reading args[0] fails with java.lang.ArrayIndexOutOfBoundsException: 0.
- **Role:** context

**16. `run_time_error` &rarr; `InputTypeMismatch`** (error)

- **Exact edge logic (the wrong rule):** StdIn.readInt() accepts any typed text such as abc or 12.2.
- **Twin logic (the right rule):** If the next token is not an int (e.g. abc, 12.2, true), StdIn.readInt() throws a NumberFormatException at run time (Scanner.nextInt throws InputMismatchException).
- **Role:** context

**17. `run_time_error` &rarr; `MainWithoutStringArgs`** (error)

- **Exact edge logic (the wrong rule):** public static void main() is an acceptable entry point.
- **Twin logic (the right rule):** main is written public static void main(String[] args); these keywords and the args parameter are required.
- **Role:** context

**18. `run_time_error` &rarr; `NegativeArraySize`** (error)

- **Exact edge logic (the wrong rule):** new int[n] with a negative n creates an empty array.
- **Twin logic (the right rule):** Creating an array with a negative length throws NegativeArraySizeException at run time.
- **Role:** context

**19. `args_length` &rarr; `ArgsAlwaysPresent`** (error)

- **Exact edge logic (the wrong rule):** args[0] can always be read.
- **Twin logic (the right rule):** If you run the program without typing the command-line argument it expects, reading args[0] fails with java.lang.ArrayIndexOutOfBoundsException: 0.
- **Role:** primary

**20. `array_creation` &rarr; `NegativeArraySize`** (error)

- **Exact edge logic (the wrong rule):** new int[n] with a negative n creates an empty array.
- **Twin logic (the right rule):** Creating an array with a negative length throws NegativeArraySizeException at run time.
- **Role:** primary

**21. `command_line_args` &rarr; `ArgsAlwaysPresent`** (error)

- **Exact edge logic (the wrong rule):** args[0] can always be read.
- **Twin logic (the right rule):** If you run the program without typing the command-line argument it expects, reading args[0] fails with java.lang.ArrayIndexOutOfBoundsException: 0.
- **Role:** context

**22. `input_format` &rarr; `InputTypeMismatch`** (error)

- **Exact edge logic (the wrong rule):** StdIn.readInt() accepts any typed text such as abc or 12.2.
- **Twin logic (the right rule):** If the next token is not an int (e.g. abc, 12.2, true), StdIn.readInt() throws a NumberFormatException at run time (Scanner.nextInt throws InputMismatchException).
- **Role:** primary

**23. `input_validation` &rarr; `InputTypeMismatch`** (error)

- **Exact edge logic (the wrong rule):** StdIn.readInt() accepts any typed text such as abc or 12.2.
- **Twin logic (the right rule):** If the next token is not an int (e.g. abc, 12.2, true), StdIn.readInt() throws a NumberFormatException at run time (Scanner.nextInt throws InputMismatchException).
- **Role:** context

**24. `main_method` &rarr; `MainWithoutStringArgs`** (error)

- **Exact edge logic (the wrong rule):** public static void main() is an acceptable entry point.
- **Twin logic (the right rule):** main is written public static void main(String[] args); these keywords and the args parameter are required.
- **Role:** primary

**25. `standard_input` &rarr; `InputTypeMismatch`** (error)

- **Exact edge logic (the wrong rule):** StdIn.readInt() accepts any typed text such as abc or 12.2.
- **Twin logic (the right rule):** If the next token is not an int (e.g. abc, 12.2, true), StdIn.readInt() throws a NumberFormatException at run time (Scanner.nextInt throws InputMismatchException).
- **Role:** context

**26. `run_time_error` &rarr; `run_time_error@L0`** (has_level)

- **Exact edge logic:** run time error -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (5 ways).
  - **[0] everyday\_reading** (rule type E, folk-meaning rule): Everyday reading: if the program compiled, the computer has accepted it, so any problem would have been reported then. Java rule: run-time errors are detected only while the program executes, on particular data (e.g. no argument, a divisor of 0), and stop it with an exception.
  - **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `CompilesMeansWorks`: wrong rule: Code that compiles is code that works. Right rule: Code that compiles can still fail at run time (an exception) or give wrong output.
  - **[2] misconception** (rule type M, wrong rule / right rule) &rarr; `DivisionByZeroIsCompileError`: wrong rule: System.out.println(5 / 0); is rejected by the compiler. Right rule: It compiles; integer division by zero throws ArithmeticException when the statement runs.
  - **[3] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `CompilesMeansWorks`: Applies the exception rule (LT: execution stops at the faulty statement) unevenly: lets the program keep printing after the failing statement on one trace, or reports the error before any earlier output on another. (here mixing in: "Code that compiles is code that works")
  - **[4] misconception** (rule type M, wrong rule / right rule) &rarr; `ParseAnyString`: wrong rule: Integer.parseInt works on any text, e.g. "five" or "12.2". Right rule: Integer.parseInt throws a NumberFormatException at run time when the string is not an integer written in digits.

**27. `run_time_error` &rarr; `run_time_error@L1`** (has_level)

- **Exact edge logic:** run time error -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).
  - **[0] names\_the\_element** (rule type N, identity rule): A run-time error (exception) is an error that does not show up until the program is executed and makes it impossible to run to completion.
  - **[1] states\_the\_rule** (rule type S, declarative rule): When a run-time error occurs, the program 'crashes' (terminates) and the JVM prints the exception name, a message, and the method, file and line where it happened.

**28. `run_time_error` &rarr; `run_time_error@L2`** (has_level)

- **Exact edge logic:** run time error -&gt; L2 (Multistructural): the answer applies the rules of run time error to every part of the code, in order (3 ways).
  - **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): Statements before the faulty one run normally (their output appears); the faulty statement throws; no later statement runs.
  - **[1] output\_prediction** (rule type OP, evaluation / result rule): Output: any earlier output, then Exception in thread "main" java.lang.&lt;Name&gt;: &lt;detail&gt; at Class.main(Class.java:&lt;line&gt;).
  - **[2] one\_step\_execution** (rule type OS, state-transition rule): The throwing step changes no variable it was meant to set (the operation does not complete) and transfers control out of main, ending the program.

**29. `run_time_error` &rarr; `run_time_error@L3`** (has_level)

- **Exact edge logic:** run time error -&gt; L3 (Relational): the answer relates the parts (4 ways).
  - **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): A run-time error appears only while java Name executes, after compiling has succeeded.
  - **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): javac cannot detect it because it depends on run-time values (the argument typed, the divisor's value).
  - **[2] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): A run-time error stops the program with an exception message; a logic error lets it finish with wrong output and no message.
  - **[3] purpose\_of\_the\_whole** (rule type P, plan / role rule): Purpose (of exceptions): stop the program at the point where something impossible was asked, instead of continuing with an undefined value, and report what and where.

**30. `run_time_error` &rarr; `run_time_error@L4`** (has_level)

- **Exact edge logic:** run time error -&gt; L4 (Extended abstract): the answer reasons beyond the given code (8 ways).
  - **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `CompilesMeansWorks`: The same compiled program may run fine on one input and throw on another (UseArgument with and without an argument); adding a guard such as checking args.length removes the trigger without changing correct runs.
  - **[1] diagnose\_an\_error** (rule type D, error rule): rule broken: main is written public static void main(String[] args). Kind: launch error. Trigger class: header public static void main(): compiles, but java Name cannot find the main method
  - **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: Array length must be &gt;= 0. Kind: run-time exception. Trigger class: new int[n] with n &lt; 0: NegativeArraySizeException
  - **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: args[k] exists only if at least k+1 arguments were typed. Kind: run-time exception. Trigger class: running without the expected argument: java.lang.ArrayIndexOutOfBoundsException: 0
  - **[4] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Expect a run-time error when correctness depends on data (array indices, divisors, parsed input, presence of arguments); validate such data before use. Errors that depend only on the text are compile-time; wrong-but-legal results are logic errors.
  - **[5] diagnose\_an\_error** (rule type D, error rule): rule broken: StdIn.readInt() needs the next token to be an int. Kind: run-time exception. Trigger class: next token abc, 12.2 or true (StdIn: InputMismatchException/NumberFormatException depending on version; Scanner.nextInt: InputMismatchException)
  - **[6] diagnose\_an\_error** (rule type D, error rule): rule broken: Integer division and remainder by zero are undefined. Kind: run-time exception. Trigger class: a / b or a % b with int b == 0: ArithmeticException: / by zero
  - **[7] diagnose\_an\_error** (rule type D, error rule): rule broken: Integer.parseInt needs an integer written in digits. Kind: run-time exception. Trigger class: parsing "five" or "12.2": NumberFormatException

**31. `topic1.1.c` &rarr; `run_time_error`** (contains)

- topic `topic1.1.c` contains `run_time_error`

**32. `topic1.1.c` &rarr; `compile_time_error`** (contains)

- topic `topic1.1.c` contains `compile_time_error`

**33. `topic1.1.c` &rarr; `logical_error`** (contains)

- topic `topic1.1.c` contains `logical_error`

**34. `topic1.1.c` &rarr; `reading_error_messages`** (contains)

- topic `topic1.1.c` contains `reading_error_messages`
