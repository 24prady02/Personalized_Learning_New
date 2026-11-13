# formatted_output (`formatted_output`)

printf with a format string such as %d, %.2f, %s

Section 1.5 Input and Output, topic 1.5.b Standard output and formatted printing.

![The knowledge graph around formatted_output](formatted_output.png)

## At a glance

- **Needs first:** `standard_output`
- **Leads to:** nothing
- **Learned alongside:** `println`
- **Misconceptions:** `FieldWidthIsIntegerDigits`, `ManyDigitsMeanAccurate`, `PrintfAddsNewline`, `PrintfAnyConversion`
- **Errors:** none
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 16 edges around this concept. The edge logic, the wrong and right rules and the exact rules of the ways are copied word for word from the graph.

## To work on (0)

Nothing is missing for this concept.

## What it needs first (1)

A prerequisite edge means the other concept has to be understood before `formatted_output`.

### `standard_output` comes before `formatted_output`

*StdOut / System.out*

- **Edge:** `pre:standard_output->formatted_output`
- **Exact edge logic:** printf writes to standard output, like print, but formats each value first.
- **Grounding:** book\_passage
- **Composition rule (R) of `formatted_output` with `standard_output`:** printf output goes into the same stream as print/println and lands at the point in the stream where it was called. It does not end the line.
- **Composition rule (R) of `standard_output` with `formatted_output`:** printf writes to the same stream as print and println, so mixed calls appear in call order. Unlike println, printf ends a line only when the format contains \n.

## What it leads to (0)

These concepts need `formatted_output` first.

No concept has this one as a prerequisite.

## Learned alongside (1)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

### `formatted_output` alongside `println`

*System.out.println -- output with a trailing newline*

- **Edge:** `par:println~formatted_output`
- **Exact edge logic:** println prints each number with all its digits and ends the line; printf formats each value by its conversion code and starts a new line only when \n is in the format string.
- **Grounding:** book\_passage
- **Composition rule (R) of `formatted_output` with `println`:** println prints a double with all its digits (about 15 places) and always ends the line. printf("%.2f\n", x) controls the digits and ends the line only because of \n.
- **Composition rule (R) of `println` with `formatted_output`:** println prints numbers with all their digits and always ends the line; printf formats each value by its conversion code and ends the line only where the format has %n or \n.

## Misconceptions (4)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### FieldWidthIsIntegerDigits

- **Edge:** `formatted_output` &rarr; `FieldWidthIsIntegerDigits` (misconception)
- **Exact edge logic (the wrong rule):** %2.4f prints two digits before the decimal point and four after.
- **Twin logic (the right rule):** The number before the point is the width of the whole field; %7.2f means 7 characters in total with 2 digits after the decimal point.
- **Wrong belief (on the node):** %2.4f prints two digits before the decimal point and four after.
- **Correct rule (on the node):** The number before the point is the width of the whole field; %7.2f means 7 characters in total with 2 digits after the decimal point.
- **Provenance:** textbook
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [2] misconception, exact rule:** wrong rule: %2.4f prints two digits before the decimal point and four after. Right rule: The first number is the width of the whole field. %7.2f means 7 characters in total, with 2 digits after the decimal point.

### ManyDigitsMeanAccurate

- **Edge:** `formatted_output` &rarr; `ManyDigitsMeanAccurate` (misconception)
- **Exact edge logic (the wrong rule):** A result printed with many decimal places must be accurate to those places.
- **Twin logic (the right rule):** A program does not produce accurate answers simply because it can print numbers to many decimal places of precision; ensuring accuracy is often the most difficult challenge.
- **Wrong belief (on the node):** A result printed with many decimal places must be accurate to those places.
- **Correct rule (on the node):** A program does not produce accurate answers simply because it can print numbers to many decimal places of precision; ensuring accuracy is often the most difficult challenge.
- **Provenance:** textbook
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [5] misconception, exact rule:** wrong rule: A result printed with many decimal places must be accurate to those places. Right rule: Printing precision is only formatting. A value printed to many places can still be inaccurate, and ensuring accuracy is the hard part.
- **Edge `frequency_counting` &rarr; `ManyDigitsMeanAccurate`, exact edge logic:** A result printed with many decimal places must be accurate to those places. **Twin logic:** A program does not produce accurate answers simply because it can print numbers to many decimal places of precision; ensuring accuracy is often the most difficult challenge. (role: primary)
- **Edge `two_models` &rarr; `ManyDigitsMeanAccurate`, exact edge logic:** A result printed with many decimal places must be accurate to those places. **Twin logic:** A program does not produce accurate answers simply because it can print numbers to many decimal places of precision; ensuring accuracy is often the most difficult challenge. (role: context)

### PrintfAddsNewline

- **Edge:** `formatted_output` &rarr; `PrintfAddsNewline` (misconception)
- **Exact edge logic (the wrong rule):** printf() ends the line like println().
- **Twin logic (the right rule):** printf() does not add a newline; put \n in the format string to end the line.
- **Wrong belief (on the node):** printf() ends the line like println().
- **Correct rule (on the node):** printf() does not add a newline; put \n in the format string to end the line.
- **Provenance:** textbook
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [3] misconception, exact rule:** wrong rule: printf() ends the line like println(). Right rule: printf() adds no newline. Put \n (or %n) in the format string.
- **Edge `standard_output` &rarr; `PrintfAddsNewline`, exact edge logic:** printf() ends the line like println(). **Twin logic:** printf() does not add a newline; put \n in the format string to end the line. (role: context)

### PrintfAnyConversion

- **Edge:** `formatted_output` &rarr; `PrintfAnyConversion` (misconception)
- **Exact edge logic (the wrong rule):** Any conversion code (%d, %f, %s) works with any argument type.
- **Twin logic (the right rule):** Each conversion code must match its argument's type (any type works with %s); %d with a double or %f with an int throws an IllegalFormatConversionException at run time.
- **Wrong belief (on the node):** Any conversion code (%d, %f, %s) works with any argument type.
- **Correct rule (on the node):** Each conversion code must match its argument's type (any type works with %s); %d with a double or %f with an int throws an IllegalFormatConversionException at run time.
- **Provenance:** derived
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [1] misconception, exact rule:** wrong rule: Any conversion code (%d, %f, %s) works with any argument type. Right rule: The conversion must fit the argument's type (%s accepts any type). printf("%12d", Math.PI) or printf("%4.2f", 512) throws IllegalFormatConversionException at run time.
- **L0 way [4] inconsistent\_trace, exact rule:** Points to LT (specifiers are paired with arguments left to right, and the other characters pass through). An uneven trace pairs a specifier with the wrong argument, drops the literal text between specifiers, or pads on the wrong side on some fields. (here mixing in: "Any conversion code (%d, %f, %s) works with any argument type")

## Errors (0)

An error edge states the rule that gets broken in a program, and the right rule.

The graph has no error edge from this concept.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for formatted output: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to formatted output agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

- **Edge:** `formatted_output` &rarr; `formatted_output@L0` (has_level)
- **Exact edge logic:** formatted output -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (6 ways).

Ways (6), each with its exact rule:

- **[0] everyday\_reading** (rule type E, folk-meaning rule): In maths \`7.2\` (or %2.4f) reads as a decimal number, or as '7 digits before the point, 2 after'. In a format specifier the number before the point is the total field width and the number after it is the digits after the decimal point. Also \`%\` is not 'percent'.
- **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `PrintfAnyConversion`: wrong rule: Any conversion code (%d, %f, %s) works with any argument type. Right rule: The conversion must fit the argument's type (%s accepts any type). printf("%12d", Math.PI) or printf("%4.2f", 512) throws IllegalFormatConversionException at run time.
- **[2] misconception** (rule type M, wrong rule / right rule) &rarr; `FieldWidthIsIntegerDigits`: wrong rule: %2.4f prints two digits before the decimal point and four after. Right rule: The first number is the width of the whole field. %7.2f means 7 characters in total, with 2 digits after the decimal point.
- **[3] misconception** (rule type M, wrong rule / right rule) &rarr; `PrintfAddsNewline`: wrong rule: printf() ends the line like println(). Right rule: printf() adds no newline. Put \n (or %n) in the format string.
- **[4] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `PrintfAnyConversion`: Points to LT (specifiers are paired with arguments left to right, and the other characters pass through). An uneven trace pairs a specifier with the wrong argument, drops the literal text between specifiers, or pads on the wrong side on some fields. (here mixing in: "Any conversion code (%d, %f, %s) works with any argument type")
- **[5] misconception** (rule type M, wrong rule / right rule) &rarr; `ManyDigitsMeanAccurate`: wrong rule: A result printed with many decimal places must be accurate to those places. Right rule: Printing precision is only formatting. A value printed to many places can still be inaccurate, and ensuring accuracy is the hard part.

### L1: Unistructural / atom x text surface

L1 for formatted output: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

- **Edge:** `formatted_output` &rarr; `formatted_output@L1` (has_level)
- **Exact edge logic:** formatted output -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

Ways (2), each with its exact rule:

- **[0] names\_the\_element** (rule type N, identity rule): printf is the formatted-print method of standard output. It takes a format string and arguments and writes the formatted string.
- **[1] states\_the\_rule** (rule type S, declarative rule): A format specifier has the form %[argument\_index$][flags][width][.precision]conversion: d for integer types, f for floating-point values, s for String or any type. The width is a minimum character count, and for f the precision is the number of digits after the point.

### L2: Multistructural / block x execution / preoperational

L2 for formatted output: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

- **Edge:** `formatted_output` &rarr; `formatted_output@L2` (has_level)
- **Exact edge logic:** formatted output -&gt; L2 (Multistructural): the answer applies the rules of formatted output to every part of the code, in order (3 ways).

Ways (3), each with its exact rule:

- **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): The arguments are evaluated first. The format string is then scanned left to right: ordinary characters are copied, and each specifier takes the next argument, converts it, rounds it to the precision and pads it with blanks to the width (left side by default, right side with the \`-\` flag).
- **[1] output\_prediction** (rule type OP, evaluation / result rule): The output is the formatted text. printf("%7.5f", Math.PI) gives 3.14159, printf("PI is approximately %.2f\n", Math.PI) gives \`PI is approximately 3.14\` and a newline, and printf("%5d", 42) gives \`   42\`. Rounding is half-up.
- **[2] one\_step\_execution** (rule type OS, state-transition rule): One call appends one formatted string to standard output and adds no newline unless \n or %n is in the format. The stored values of the arguments do not change (only their printed form is rounded).

### L3: Relational / relations x function (concrete operational begins)

L3 for formatted output: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

- **Edge:** `formatted_output` &rarr; `formatted_output@L3` (has_level)
- **Exact edge logic:** formatted output -&gt; L3 (Relational): the answer relates the parts (3 ways).

Ways (3), each with its exact rule:

- **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): printf output goes into the same stream as print/println and lands at the point in the stream where it was called. It does not end the line.
- **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): println prints a double with all its digits (about 15 places) and always ends the line. printf("%.2f\n", x) controls the digits and ends the line only because of \n.
- **[2] purpose\_of\_the\_whole** (rule type P, plan / role rule): Plan: table printing. Inside a loop, one fixed format string with a specifier per column prints aligned rows (e.g. a loan table) at a chosen precision.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for formatted output: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

- **Edge:** `formatted_output` &rarr; `formatted_output@L4` (has_level)
- **Exact edge logic:** formatted output -&gt; L4 (Extended abstract): the answer reasons beyond the given code (5 ways).

Ways (5), each with its exact rule:

- **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `PrintfAnyConversion`: Changing the precision changes only the printed digits, not the stored value. Changing the width changes only the padding. A width smaller than the converted text is ignored, so nothing is truncated.
- **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Use printf when the number of digits, the field width or column alignment matters (tables, money, reports). For quick checks of a value, println is enough.
- **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: The conversion code must match the argument type. Kind: run-time exception. Trigger class: %d with a double, or %f with an int (e.g. printf("%4.2f", 512)): IllegalFormatConversionException.
- **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: There must be an argument for every specifier, and the format syntax must be legal. Kind: run-time exception. Trigger class: More specifiers than arguments (e.g. printf("%d %d", 3)), or a malformed specifier: an IllegalFormatException subclass such as MissingFormatArgumentException.
- **[4] diagnose\_an\_error** (rule type D, error rule): rule broken: printf adds no line separator. Kind: silent logic error. Trigger class: A printf in a loop without \n: all rows run together on one line.

## Same topic

`formatted_output` belongs to the topic **Standard output and formatted printing** (`topic1.5.b`). The topic also contains: `standard_output`.

## Rules of the concept (19)

- **Book** (SW-1e, p. 124 (pdf 134)): "The printf() method is more flexible: it allows us to specify the number of digits and the precision when converting data type values to strings for output."
- **Book** (SW-1e, p. 124 (pdf 134)): "The simplest type of format string begins with % and ends with a one-letter conversion code."
- **Book** (SW-1.5, ): "Format strings begin with % and end with a one-letter conversion code."
- **Book** (API-Format, ): "Unchecked exception thrown when the argument corresponding to the format specifier is of an incompatible type."
- **E** (folk-meaning rule): In maths \`7.2\` (or %2.4f) reads as a decimal number, or as '7 digits before the point, 2 after'. In a format specifier the number before the point is the total field width and the number after it is the digits after the decimal point. Also \`%\` is not 'percent'.
- **M** (wrong rule / right rule): PrintfAnyConversion: wrong: Any conversion code (%d, %f, %s) works with any argument type. \| right: The conversion must fit the argument's type (%s accepts any type). printf("%12d", Math.PI) or printf("%4.2f", 512) throws IllegalFormatConversionException at run time.
- **M** (wrong rule / right rule): FieldWidthIsIntegerDigits: wrong: %2.4f prints two digits before the decimal point and four after. \| right: The first number is the width of the whole field. %7.2f means 7 characters in total, with 2 digits after the decimal point.
- **M** (wrong rule / right rule): PrintfAddsNewline: wrong: printf() ends the line like println(). \| right: printf() adds no newline. Put \n (or %n) in the format string.
- **M** (wrong rule / right rule): ManyDigitsMeanAccurate: wrong: A result printed with many decimal places must be accurate to those places. \| right: Printing precision is only formatting. A value printed to many places can still be inaccurate, and ensuring accuracy is the hard part.
- **T** (uneven-application rule): Points to LT (specifiers are paired with arguments left to right, and the other characters pass through). An uneven trace pairs a specifier with the wrong argument, drops the literal text between specifiers, or pads on the wrong side on some fields.
- **N** (identity rule): printf is the formatted-print method of standard output. It takes a format string and arguments and writes the formatted string.
- **S** (declarative rule): A format specifier has the form %[argument\_index$][flags][width][.precision]conversion: d for integer types, f for floating-point values, s for String or any type. The width is a minimum character count, and for f the precision is the number of digits after the point.
- **LT** (operational sequencing rule): The arguments are evaluated first. The format string is then scanned left to right: ordinary characters are copied, and each specifier takes the next argument, converts it, rounds it to the precision and pads it with blanks to the width (left side by default, right side with the \`-\` flag).
- **OP** (evaluation / result rule): The output is the formatted text. printf("%7.5f", Math.PI) gives 3.14159, printf("PI is approximately %.2f\n", Math.PI) gives \`PI is approximately 3.14\` and a newline, and printf("%5d", 42) gives \`   42\`. Rounding is half-up.
- **OS** (state-transition rule): One call appends one formatted string to standard output and adds no newline unless \n or %n is in the format. The stored values of the arguments do not change (only their printed form is rounded).
- **R** (composition rule (with a neighbour)): with standard\_output: printf output goes into the same stream as print/println and lands at the point in the stream where it was called. It does not end the line.
- **R** (composition rule (with a neighbour)): with println: println prints a double with all its digits (about 15 places) and always ends the line. printf("%.2f\n", x) controls the digits and ends the line only because of \n.
- **P** (plan / role rule): Plan: table printing. Inside a loop, one fixed format string with a specifier per column prints aligned rows (e.g. a loan table) at a chosen precision.
- **C** (conservation rule): Changing the precision changes only the printed digits, not the stored value. Changing the width changes only the padding. A width smaller than the converted text is ignored, so nothing is truncated.
- **D** (error rule): rule broken: The conversion code must match the argument type. (run-time exception)
- **D** (error rule): rule broken: There must be an argument for every specifier, and the format syntax must be legal. (run-time exception)
- **D** (error rule): rule broken: printf adds no line separator. (silent logic error)
- **X** (applicability rule): Use printf when the number of digits, the field width or column alignment matters (tables, money, reports). For quick checks of a value, println is enough.

## How it is found in code and answers (reader block)

- **Aliases:** printf, format, formatted, format specifier
- **Code patterns:** `\.printf\s*\(`, `String\.format\s*\(`, `\.format\s*\(`
- **Operator symbols:** none
- **Java types:** none
- **Signal printf\_width** (scope statement, decisive): `printf\s*\(\s*\"[^\"]*(?:%-?\d+(?:\.\d+)?[dfse]|%\.\d+f)`

## The whole prerequisite chain

- **Everything it builds on (2):** `standard_output`, `stream_model`
- **Everything that builds on it (0):** nothing

## Every edge in this view and its exact edge logic (16)

All the edges drawn in the picture, in the order: prerequisite, parallel, misconception, error, has_level, contains.

**1. `standard_output` &rarr; `formatted_output`** (prerequisite)

- **Exact edge logic:** printf writes to standard output, like print, but formats each value first.
- **Grounding:** book\_passage
- **Composition rule (R) of `standard_output` with `formatted_output`:** printf writes to the same stream as print and println, so mixed calls appear in call order. Unlike println, printf ends a line only when the format contains \n.
- **Composition rule (R) of `formatted_output` with `standard_output`:** printf output goes into the same stream as print/println and lands at the point in the stream where it was called. It does not end the line.

**2. `println` &harr; `formatted_output`** (parallel)

- **Exact edge logic:** println prints each number with all its digits and ends the line; printf formats each value by its conversion code and starts a new line only when \n is in the format string.
- **Grounding:** book\_passage
- **Composition rule (R) of `println` with `formatted_output`:** println prints numbers with all their digits and always ends the line; printf formats each value by its conversion code and ends the line only where the format has %n or \n.
- **Composition rule (R) of `formatted_output` with `println`:** println prints a double with all its digits (about 15 places) and always ends the line. printf("%.2f\n", x) controls the digits and ends the line only because of \n.

**3. `formatted_output` &rarr; `FieldWidthIsIntegerDigits`** (misconception)

- **Exact edge logic (the wrong rule):** %2.4f prints two digits before the decimal point and four after.
- **Twin logic (the right rule):** The number before the point is the width of the whole field; %7.2f means 7 characters in total with 2 digits after the decimal point.
- **Role:** primary

**4. `formatted_output` &rarr; `ManyDigitsMeanAccurate`** (misconception)

- **Exact edge logic (the wrong rule):** A result printed with many decimal places must be accurate to those places.
- **Twin logic (the right rule):** A program does not produce accurate answers simply because it can print numbers to many decimal places of precision; ensuring accuracy is often the most difficult challenge.
- **Role:** context

**5. `formatted_output` &rarr; `PrintfAddsNewline`** (misconception)

- **Exact edge logic (the wrong rule):** printf() ends the line like println().
- **Twin logic (the right rule):** printf() does not add a newline; put \n in the format string to end the line.
- **Role:** primary

**6. `formatted_output` &rarr; `PrintfAnyConversion`** (misconception)

- **Exact edge logic (the wrong rule):** Any conversion code (%d, %f, %s) works with any argument type.
- **Twin logic (the right rule):** Each conversion code must match its argument's type (any type works with %s); %d with a double or %f with an int throws an IllegalFormatConversionException at run time.
- **Role:** primary

**7. `frequency_counting` &rarr; `ManyDigitsMeanAccurate`** (misconception)

- **Exact edge logic (the wrong rule):** A result printed with many decimal places must be accurate to those places.
- **Twin logic (the right rule):** A program does not produce accurate answers simply because it can print numbers to many decimal places of precision; ensuring accuracy is often the most difficult challenge.
- **Role:** primary

**8. `standard_output` &rarr; `PrintfAddsNewline`** (misconception)

- **Exact edge logic (the wrong rule):** printf() ends the line like println().
- **Twin logic (the right rule):** printf() does not add a newline; put \n in the format string to end the line.
- **Role:** context

**9. `two_models` &rarr; `ManyDigitsMeanAccurate`** (misconception)

- **Exact edge logic (the wrong rule):** A result printed with many decimal places must be accurate to those places.
- **Twin logic (the right rule):** A program does not produce accurate answers simply because it can print numbers to many decimal places of precision; ensuring accuracy is often the most difficult challenge.
- **Role:** context

**10. `formatted_output` &rarr; `formatted_output@L0`** (has_level)

- **Exact edge logic:** formatted output -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (6 ways).
  - **[0] everyday\_reading** (rule type E, folk-meaning rule): In maths \`7.2\` (or %2.4f) reads as a decimal number, or as '7 digits before the point, 2 after'. In a format specifier the number before the point is the total field width and the number after it is the digits after the decimal point. Also \`%\` is not 'percent'.
  - **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `PrintfAnyConversion`: wrong rule: Any conversion code (%d, %f, %s) works with any argument type. Right rule: The conversion must fit the argument's type (%s accepts any type). printf("%12d", Math.PI) or printf("%4.2f", 512) throws IllegalFormatConversionException at run time.
  - **[2] misconception** (rule type M, wrong rule / right rule) &rarr; `FieldWidthIsIntegerDigits`: wrong rule: %2.4f prints two digits before the decimal point and four after. Right rule: The first number is the width of the whole field. %7.2f means 7 characters in total, with 2 digits after the decimal point.
  - **[3] misconception** (rule type M, wrong rule / right rule) &rarr; `PrintfAddsNewline`: wrong rule: printf() ends the line like println(). Right rule: printf() adds no newline. Put \n (or %n) in the format string.
  - **[4] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `PrintfAnyConversion`: Points to LT (specifiers are paired with arguments left to right, and the other characters pass through). An uneven trace pairs a specifier with the wrong argument, drops the literal text between specifiers, or pads on the wrong side on some fields. (here mixing in: "Any conversion code (%d, %f, %s) works with any argument type")
  - **[5] misconception** (rule type M, wrong rule / right rule) &rarr; `ManyDigitsMeanAccurate`: wrong rule: A result printed with many decimal places must be accurate to those places. Right rule: Printing precision is only formatting. A value printed to many places can still be inaccurate, and ensuring accuracy is the hard part.

**11. `formatted_output` &rarr; `formatted_output@L1`** (has_level)

- **Exact edge logic:** formatted output -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).
  - **[0] names\_the\_element** (rule type N, identity rule): printf is the formatted-print method of standard output. It takes a format string and arguments and writes the formatted string.
  - **[1] states\_the\_rule** (rule type S, declarative rule): A format specifier has the form %[argument\_index$][flags][width][.precision]conversion: d for integer types, f for floating-point values, s for String or any type. The width is a minimum character count, and for f the precision is the number of digits after the point.

**12. `formatted_output` &rarr; `formatted_output@L2`** (has_level)

- **Exact edge logic:** formatted output -&gt; L2 (Multistructural): the answer applies the rules of formatted output to every part of the code, in order (3 ways).
  - **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): The arguments are evaluated first. The format string is then scanned left to right: ordinary characters are copied, and each specifier takes the next argument, converts it, rounds it to the precision and pads it with blanks to the width (left side by default, right side with the \`-\` flag).
  - **[1] output\_prediction** (rule type OP, evaluation / result rule): The output is the formatted text. printf("%7.5f", Math.PI) gives 3.14159, printf("PI is approximately %.2f\n", Math.PI) gives \`PI is approximately 3.14\` and a newline, and printf("%5d", 42) gives \`   42\`. Rounding is half-up.
  - **[2] one\_step\_execution** (rule type OS, state-transition rule): One call appends one formatted string to standard output and adds no newline unless \n or %n is in the format. The stored values of the arguments do not change (only their printed form is rounded).

**13. `formatted_output` &rarr; `formatted_output@L3`** (has_level)

- **Exact edge logic:** formatted output -&gt; L3 (Relational): the answer relates the parts (3 ways).
  - **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): printf output goes into the same stream as print/println and lands at the point in the stream where it was called. It does not end the line.
  - **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): println prints a double with all its digits (about 15 places) and always ends the line. printf("%.2f\n", x) controls the digits and ends the line only because of \n.
  - **[2] purpose\_of\_the\_whole** (rule type P, plan / role rule): Plan: table printing. Inside a loop, one fixed format string with a specifier per column prints aligned rows (e.g. a loan table) at a chosen precision.

**14. `formatted_output` &rarr; `formatted_output@L4`** (has_level)

- **Exact edge logic:** formatted output -&gt; L4 (Extended abstract): the answer reasons beyond the given code (5 ways).
  - **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `PrintfAnyConversion`: Changing the precision changes only the printed digits, not the stored value. Changing the width changes only the padding. A width smaller than the converted text is ignored, so nothing is truncated.
  - **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Use printf when the number of digits, the field width or column alignment matters (tables, money, reports). For quick checks of a value, println is enough.
  - **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: The conversion code must match the argument type. Kind: run-time exception. Trigger class: %d with a double, or %f with an int (e.g. printf("%4.2f", 512)): IllegalFormatConversionException.
  - **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: There must be an argument for every specifier, and the format syntax must be legal. Kind: run-time exception. Trigger class: More specifiers than arguments (e.g. printf("%d %d", 3)), or a malformed specifier: an IllegalFormatException subclass such as MissingFormatArgumentException.
  - **[4] diagnose\_an\_error** (rule type D, error rule): rule broken: printf adds no line separator. Kind: silent logic error. Trigger class: A printf in a loop without \n: all rows run together on one line.

**15. `topic1.5.b` &rarr; `formatted_output`** (contains)

- topic `topic1.5.b` contains `formatted_output`

**16. `topic1.5.b` &rarr; `standard_output`** (contains)

- topic `topic1.5.b` contains `standard_output`
