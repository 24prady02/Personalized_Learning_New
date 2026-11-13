# parsing (`parsing`)

Integer.parseInt / Double.parseDouble turn text into numbers

Section 1.2 Built-in Types of Data, topic 1.2.h Type conversion (automatic, cast, parsing).

![The knowledge graph around parsing](parsing.png)

## At a glance

- **Needs first:** `command_line_args`
- **Leads to:** `type_conversion`
- **Learned alongside:** nothing
- **Misconceptions:** `ArgsAreNumbers`, `CastParsesString`, `ParseAnyString`
- **Errors:** none
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 18 edges around this concept, each explained in the graph's own words.

## What it needs first (1)

A prerequisite edge means the other concept has to be understood before `parsing`.

### `command_line_args` comes before `parsing`

*args[] -- strings passed at launch*

args[k] is always a String, so Integer.parseInt(args[k]) is needed before it can be used as a number.

- **Grounding:** book passage
- **How `parsing` combines with `command_line_args`:** Because args[k] is always a String, a numeric argument must be passed through a parse method before it can be used in arithmetic or comparisons.
- **How `command_line_args` combines with `parsing`:** args[k] is always a String, so Integer.parseInt(args[k]) or Double.parseDouble(args[k]) must convert it before arithmetic.

## What it leads to (1)

These concepts need `parsing` first.

### `parsing` comes before `type_conversion`

*implicit widening and explicit (cast)*

Integer.parseInt(s) converts the String s into an int; SW later classifies such methods as explicit type conversion.

- **Grounding:** questionable
- **How `parsing` combines with `type_conversion`:** SW classifies parse methods as explicit type conversion: a method takes an argument of one type and produces a result of another.
- **How `type_conversion` combines with `parsing`:** Parsing methods are explicit type conversion from String to a number: a method takes an argument of one type and produces a result of another.

## Learned alongside (0)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

No parallel edge touches this concept.

## Misconceptions (3)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### ArgsAreNumbers

- **Wrong rule:** If a number is typed when the program is launched, args[0] is already an int and can be used in arithmetic.
- **Right rule:** args[0] is always a String, so Integer.parseInt(args[0]) is needed to get its number.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: Command-line args arrive already typed, so no parsing is needed. Right rule: args[0] is always a String, so Integer.parseInt(args[0]) is needed to get its number.
- **Also an edge from `command_line_args`:** If a number is typed when the program is launched, args[0] is already an int and can be used in arithmetic.

### CastParsesString

- **Wrong rule:** (int) args[0] converts the text "34" into the number 34.
- **Right rule:** A String argument that represents a number must be converted with a method such as Integer.parseInt.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: (int) args[0] converts the text "34" into the number 34. Right rule: A String argument that represents a number must be converted with a method such as Integer.parseInt; a cast from String to int does not compile.
- **Shows at level L0 as:** inconsistent trace: Points to LT (the method reads the whole string; it returns a number only if every character fits the format, otherwise it throws). Applied unevenly: the student parses "12" correctly but expects "12.2" to give 12 or "five" to give 5 on another call. (here mixing in: "(int) args[0] converts the text "34" into the number 34")
- **Also an edge from `explicit_cast`:** (int) args[0] converts the text "34" into the number 34.

### ParseAnyString

- **Wrong rule:** Integer.parseInt works on any text, e.g. "five" or "12.2".
- **Right rule:** Integer.parseInt throws a NumberFormatException at run time when the string is not an integer written in digits.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: Integer.parseInt works on any text, e.g. "five" or "12.2". Right rule: Integer.parseInt throws a NumberFormatException at run time when the string is not an integer written in digits.
- **Also an edge from `run_time_error`:** Integer.parseInt works on any text, e.g. "five" or "12.2".

## Errors (0)

An error edge states the rule that gets broken in a program, and the right rule.

The graph has no error edge from this concept.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for parsing: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to parsing agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

parsing -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (5 ways).

- **everyday reading** (folk-meaning rule): Folk meaning: what the user typed, such as 34, already is a number, so a command-line argument can be used in arithmetic or simply cast. Java rule: command-line arguments are Strings; a String is converted to a number only by a parse method such as Integer.parseInt(args[0]) (parse = read and translate).
- **misconception** (wrong rule / right rule; shows `CastParsesString`): wrong rule: (int) args[0] converts the text "34" into the number 34. Right rule: A String argument that represents a number must be converted with a method such as Integer.parseInt; a cast from String to int does not compile.
- **misconception** (wrong rule / right rule; shows `ParseAnyString`): wrong rule: Integer.parseInt works on any text, e.g. "five" or "12.2". Right rule: Integer.parseInt throws a NumberFormatException at run time when the string is not an integer written in digits.
- **inconsistent trace** (uneven-application rule; shows `CastParsesString`): Points to LT (the method reads the whole string; it returns a number only if every character fits the format, otherwise it throws). Applied unevenly: the student parses "12" correctly but expects "12.2" to give 12 or "five" to give 5 on another call. (here mixing in: "(int) args[0] converts the text "34" into the number 34")
- **misconception** (wrong rule / right rule; shows `ArgsAreNumbers`): wrong rule: Command-line args arrive already typed, so no parsing is needed. Right rule: args[0] is always a String, so Integer.parseInt(args[0]) is needed to get its number.

### L1: Unistructural / atom x text surface

L1 for parsing: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

parsing -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

- **names the element** (identity rule): Parsing is explicit type conversion from text: a library method such as Integer.parseInt or Double.parseDouble reads a String and translates it into a value of a primitive type.
- **states the rule** (declarative rule): int Integer.parseInt(String s), double Double.parseDouble(String s) and long Long.parseLong(String s) convert s to an int, double or long; if s is not a valid representation they throw NumberFormatException.

### L2: Multistructural / block x execution / preoperational

L2 for parsing: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

parsing -&gt; L2 (Multistructural): the answer applies the rules of parsing to every part of the code, in order (3 ways).

- **line by line trace** (operational sequencing rule): The argument expression (e.g. args[0]) is evaluated to a String, the method scans its characters and either returns the number or throws; then the value is used, typically assigned to a typed variable.
- **output prediction** (evaluation / result rule): Integer.parseInt("123") is the int 123 (same as typing the literal 123); Double.parseDouble("-3.0") is the double -3.0; Integer.parseInt("12.2") or ("five") produces no value but a NumberFormatException.
- **one step execution** (state-transition rule): The String is left unchanged; the only state change is the assignment of the result, e.g. int N = Integer.parseInt(args[0]); sets N.

### L3: Relational / relations x function (concrete operational begins)

L3 for parsing: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

parsing -&gt; L3 (Relational): the answer relates the parts (3 ways).

- **relation to neighbour** (composition rule (with a neighbour)): Because args[k] is always a String, a numeric argument must be passed through a parse method before it can be used in arithmetic or comparisons.
- **relation to neighbour** (composition rule (with a neighbour)): SW classifies parse methods as explicit type conversion: a method takes an argument of one type and produces a result of another.
- **purpose of the whole** (plan / role rule): Input-conversion plan: at the top of main, parse each command-line argument once into a typed variable (Sajaniemi role: fixed value) and use that variable afterwards.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for parsing: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

parsing -&gt; L4 (Extended abstract): the answer reasons beyond the given code (5 ways).

- **predict a change** (conservation rule; shows `CastParsesString`): Changing Integer.parseInt to Double.parseDouble widens the accepted inputs ("2.5") and changes the variable's type to double; changing the input text from "34" to "34.0" or "thirty" turns a working run into a NumberFormatException; converting a number back to a String always succeeds.
- **transfer to a new program** (applicability rule): Use parse methods whenever numbers arrive as text (command-line arguments, tokens of a line); StdIn.readInt() already parses its token; use casts, not parse methods, between numeric types.
- **diagnose an error** (error rule): rule broken: The string passed to a parse method must be a valid number of that type. Kind: run-time exception. Trigger class: Input that is not an integer in digits for parseInt: words ("five"), decimals ("12.2"), empty strings or embedded spaces (NumberFormatException).
- **diagnose an error** (error rule): rule broken: args[k] exists only if at least k+1 arguments were typed. Kind: run-time exception. Trigger class: Running the program with too few command-line arguments, so Integer.parseInt(args[0]) fails with ArrayIndexOutOfBoundsException before parsing.
- **diagnose an error** (error rule): rule broken: A String cannot be cast to a number. Kind: compile-time. Trigger class: (int) args[0].

## Same topic

`parsing` belongs to the topic **Type conversion (automatic, cast, parsing)** (`topic1.2.h`). The topic also contains: `explicit_cast`, `string_conversion`, `type_conversion`, `widening_conversion`.

## Rules of the concept (18)

- **folk-meaning rule:** Folk meaning: what the user typed, such as 34, already is a number, so a command-line argument can be used in arithmetic or simply cast. Java rule: command-line arguments are Strings; a String is converted to a number only by a parse method such as Integer.parseInt(args[0]) (parse = read and translate).
- **wrong rule / right rule:** ArgsAreNumbers: wrong: Command-line args arrive already typed, so no parsing is needed. \| right: args[0] is always a String, so Integer.parseInt(args[0]) is needed to get its number.
- **wrong rule / right rule:** CastParsesString: wrong: (int) args[0] converts the text "34" into the number 34. \| right: A String argument that represents a number must be converted with a method such as Integer.parseInt; a cast from String to int does not compile.
- **wrong rule / right rule:** ParseAnyString: wrong: Integer.parseInt works on any text, e.g. "five" or "12.2". \| right: Integer.parseInt throws a NumberFormatException at run time when the string is not an integer written in digits.
- **uneven-application rule:** Points to LT (the method reads the whole string; it returns a number only if every character fits the format, otherwise it throws). Applied unevenly: the student parses "12" correctly but expects "12.2" to give 12 or "five" to give 5 on another call.
- **identity rule:** Parsing is explicit type conversion from text: a library method such as Integer.parseInt or Double.parseDouble reads a String and translates it into a value of a primitive type.
- **declarative rule:** int Integer.parseInt(String s), double Double.parseDouble(String s) and long Long.parseLong(String s) convert s to an int, double or long; if s is not a valid representation they throw NumberFormatException.
- **operational sequencing rule:** The argument expression (e.g. args[0]) is evaluated to a String, the method scans its characters and either returns the number or throws; then the value is used, typically assigned to a typed variable.
- **evaluation / result rule:** Integer.parseInt("123") is the int 123 (same as typing the literal 123); Double.parseDouble("-3.0") is the double -3.0; Integer.parseInt("12.2") or ("five") produces no value but a NumberFormatException.
- **state-transition rule:** The String is left unchanged; the only state change is the assignment of the result, e.g. int N = Integer.parseInt(args[0]); sets N.
- **composition rule (with a neighbour):** with command\_line\_args: Because args[k] is always a String, a numeric argument must be passed through a parse method before it can be used in arithmetic or comparisons.
- **composition rule (with a neighbour):** with type\_conversion: SW classifies parse methods as explicit type conversion: a method takes an argument of one type and produces a result of another.
- **plan / role rule:** Input-conversion plan: at the top of main, parse each command-line argument once into a typed variable (Sajaniemi role: fixed value) and use that variable afterwards.
- **conservation rule:** Changing Integer.parseInt to Double.parseDouble widens the accepted inputs ("2.5") and changes the variable's type to double; changing the input text from "34" to "34.0" or "thirty" turns a working run into a NumberFormatException; converting a number back to a String always succeeds.
- **error rule:** rule broken: The string passed to a parse method must be a valid number of that type. (run-time exception)
- **error rule:** rule broken: args[k] exists only if at least k+1 arguments were typed. (run-time exception)
- **error rule:** rule broken: A String cannot be cast to a number. (compile-time)
- **applicability rule:** Use parse methods whenever numbers arrive as text (command-line arguments, tokens of a line); StdIn.readInt() already parses its token; use casts, not parse methods, between numeric types.

## The whole prerequisite chain

- **Everything it builds on (4):** `class_declaration`, `command_line_args`, `main_method`, `program_text`
- **Everything that builds on it (8):** `accumulator_pattern`, `compound_assignment`, `explicit_cast`, `math_random`, `monte_carlo_simulation`, `sentinel_loop`, `type_conversion`, `widening_conversion`
