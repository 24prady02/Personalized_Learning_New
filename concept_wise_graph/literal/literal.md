# literal (`literal`)

a constant value written in code (42, 3.14, true, 'a', "hi")

Section 1.2 Built-in Types of Data, topic 1.2.a Data types and terminology (literals, identifiers, variables, declarations, assignment, expressions).

![The knowledge graph around literal](literal.png)

## At a glance

- **Needs first:** `primitive_type`
- **Leads to:** `int_literal_limit`, `scientific_notation`, `variable`
- **Learned alongside:** nothing
- **Misconceptions:** `LargeIntegerLong`, `NoFloatLiterals`, `NoLongLiterals`, `WholeNumberLiteralIsInt`
- **Errors:** none
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 31 edges around this concept. The edge logic, the wrong and right rules and the exact rules of the ways are copied word for word from the graph.

## To work on (0)

Nothing is missing for this concept.

## What it needs first (1)

A prerequisite edge means the other concept has to be understood before `literal`.

### `primitive_type` comes before `literal`

*int, double, boolean, char*

- **Edge:** `pre:primitive_type->literal`
- **Exact edge logic:** A literal is the source-code form of a value of some type, and the way it is written fixes that type: 1234 is an int, 3.14 a double, true a boolean, 'c' a char.
- **Grounding:** book\_passage
- **Composition rule (R) of `literal` with `primitive_type`:** The form of a literal selects its primitive type, and that type must be assignable to the target: int x = 3.0; does not compile even though 3.0 is a whole number.
- **Composition rule (R) of `primitive_type` with `literal`:** How a literal is written fixes its primitive type (1234 int, 3.14 double, true boolean, 'c' char), and it must fit the primitive type of the variable it initializes.

## What it leads to (3)

These concepts need `literal` first.

### `literal` comes before `int_literal_limit`

*2147483648 is legal only as -2147483648*

- **Edge:** `pre:literal->int_literal_limit`
- **Exact edge logic:** An int literal is legal only if its value lies within the int range, so a digit sequence outside -2147483648..2147483647 is not a valid int literal.
- **Grounding:** book\_passage
- **Composition rule (R) of `literal` with `int_literal_limit`:** A literal without L must lie in -2147483648..2147483647, so 2147483648 alone is a compile error. Larger values need a long literal (2147483648L).
- **Composition rule (R) of `int_literal_limit` with `literal`:** The general literal rule (a source-code representation of a value) is constrained here by int's range: a digit sequence outside -2147483648..2147483647 is not a valid int literal and must be written as a long literal with L.

### `literal` comes before `scientific_notation`

*double literals like 6.022E23*

- **Edge:** `pre:literal->scientific_notation`
- **Exact edge logic:** Scientific notation is a form of double literal.
- **Grounding:** book\_passage
- **Composition rule (R) of `literal` with `scientific_notation`:** E-notation is a form of double literal. 6.022e23 and even 1e6 are doubles, so int n = 1e6; needs a cast.
- **Composition rule (R) of `scientific_notation` with `literal`:** Scientific notation is a double literal, so the literal rules for double apply: it cannot initialize an int without a cast (int n = 1e6; does not compile).

### `literal` comes before `variable`

*a named, typed box that holds a value*

- **Edge:** `pre:literal->variable`
- **Exact edge logic:** A variable of type t is given a value of type t, often written as a literal.
- **Grounding:** order\_only
- **Composition rule (R) of `literal` with `variable`:** Literals commonly initialize variables. The literal's type must equal or widen to the variable's type: double y = 1; widens, but int x = 1.1; is an error.
- **Composition rule (R) of `variable` with `literal`:** Literals commonly give variables their values, and the literal's type must fit the variable's type (int x = 1.1; is rejected).

## Learned alongside (0)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

No parallel edge touches this concept.

## Misconceptions (4)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### LargeIntegerLong

- **Edge:** `literal` &rarr; `LargeIntegerLong` (misconception)
- **Exact edge logic (the wrong rule):** A whole-number literal that is too big for an int automatically becomes a long.
- **Twin logic (the right rule):** A sequence of digits is an int literal only if its value falls within the int range; for larger values the book advises the long type.
- **Wrong belief (on the node):** a large integer literal is automatically long
- **Correct rule (on the node):** A sequence of digits is an int literal only if its value falls within the int range; for larger values the book advises the long type.
- **Provenance:** published
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [1] misconception, exact rule:** wrong rule: a large integer literal is automatically long. Right rule: A sequence of digits is an int literal only if its value falls within the int range; for larger values the book advises the long type.
- **L0 way [5] inconsistent\_trace, exact rule:** Points to LT (each literal denotes one fixed value whose type is read from how it is written). Applied unevenly, a student reads 2.0 as an int in one place, or '7' as the number 7 in one expression and as a character in the next. (here mixing in: "a large integer literal is automatically long")
- **Edge `int_literal_limit` &rarr; `LargeIntegerLong`, exact edge logic:** a large integer literal is automatically long **Twin logic:** A sequence of digits is an int literal only if its value falls within the int range; for larger values the book advises the long type. (role: context)
- **Edge `long_type` &rarr; `LargeIntegerLong`, exact edge logic:** a large integer literal is automatically long **Twin logic:** A sequence of digits is an int literal only if its value falls within the int range; for larger values the book advises the long type. (role: context)

### NoFloatLiterals

- **Edge:** `literal` &rarr; `NoFloatLiterals` (misconception)
- **Exact edge logic (the wrong rule):** Java has no way to write a float literal.
- **Twin logic (the right rule):** A decimal literal ending in f is a float; without the f it is a double.
- **Wrong belief (on the node):** Java has no float literals
- **Correct rule (on the node):** A decimal literal ending in f is a float; without the f it is a double.
- **Provenance:** published
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [2] misconception, exact rule:** wrong rule: Java has no float literals. Right rule: A decimal literal ending in f is a float; without the f it is a double.

### NoLongLiterals

- **Edge:** `literal` &rarr; `NoLongLiterals` (misconception)
- **Exact edge logic (the wrong rule):** Java has no way to write a long literal.
- **Twin logic (the right rule):** An integer literal ending in L is a long.
- **Wrong belief (on the node):** Java has no long literals
- **Correct rule (on the node):** An integer literal ending in L is a long.
- **Provenance:** published
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [3] misconception, exact rule:** wrong rule: Java has no long literals. Right rule: An integer literal ending in L is a long.

### WholeNumberLiteralIsInt

- **Edge:** `literal` &rarr; `WholeNumberLiteralIsInt` (misconception)
- **Exact edge logic (the wrong rule):** 207. and 2.3e4 are int values because they are whole numbers.
- **Twin logic (the right rule):** A decimal point or scientific notation makes the literal a double.
- **Wrong belief (on the node):** 207. and 2.3e4 are int values because they are whole numbers.
- **Correct rule (on the node):** A decimal point or scientific notation makes the literal a double.
- **Provenance:** textbook
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [4] misconception, exact rule:** wrong rule: 207. and 2.3e4 are int values because they are whole numbers. Right rule: A decimal point or scientific notation makes the literal a double.
- **Edge `double` &rarr; `WholeNumberLiteralIsInt`, exact edge logic:** 207. and 2.3e4 are int values because they are whole numbers. **Twin logic:** A decimal point or scientific notation makes the literal a double. (role: context)

## Errors (0)

An error edge states the rule that gets broken in a program, and the right rule.

The graph has no error edge from this concept.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for literal: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to literal agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

- **Edge:** `literal` &rarr; `literal@L0` (has_level)
- **Exact edge logic:** literal -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (6 ways).

Ways (6), each with its exact rule:

- **[0] everyday\_reading** (rule type E, folk-meaning rule): In everyday writing, 1,000,000, 007, 1/2 and $5 all stand for numbers. Java literals have strict forms: commas are not allowed, 1/2 is an int division expression worth 0, and a leading 0 makes the number octal (013 is 11).
- **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `LargeIntegerLong`: wrong rule: a large integer literal is automatically long. Right rule: A sequence of digits is an int literal only if its value falls within the int range; for larger values the book advises the long type.
- **[2] misconception** (rule type M, wrong rule / right rule) &rarr; `NoFloatLiterals`: wrong rule: Java has no float literals. Right rule: A decimal literal ending in f is a float; without the f it is a double.
- **[3] misconception** (rule type M, wrong rule / right rule) &rarr; `NoLongLiterals`: wrong rule: Java has no long literals. Right rule: An integer literal ending in L is a long.
- **[4] misconception** (rule type M, wrong rule / right rule) &rarr; `WholeNumberLiteralIsInt`: wrong rule: 207. and 2.3e4 are int values because they are whole numbers. Right rule: A decimal point or scientific notation makes the literal a double.
- **[5] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `LargeIntegerLong`: Points to LT (each literal denotes one fixed value whose type is read from how it is written). Applied unevenly, a student reads 2.0 as an int in one place, or '7' as the number 7 in one expression and as a character in the next. (here mixing in: "a large integer literal is automatically long")

### L1: Unistructural / atom x text surface

L1 for literal: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

- **Edge:** `literal` &rarr; `literal@L1` (has_level)
- **Exact edge logic:** literal -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

Ways (2), each with its exact rule:

- **[0] names\_the\_element** (rule type N, identity rule): Literal: a source-code representation of one fixed data-type value, such as 42, 3.14, true, 'a' or "hi".
- **[1] states\_the\_rule** (rule type S, declarative rule): A digit sequence within the int range is an int literal. A decimal point or e-notation makes a double (3.14, 6.022e23). Suffix L gives a long and f a float. true and false are boolean, one character in single quotes is a char, and characters in double quotes are a String. Integer literals can also be written in hexadecimal (0x1F), octal (a leading 0: 013 is 11) or binary (0b101) and may contain underscores (1\_000\_000); a trailing L makes a long literal (2147483648L) and a trailing F a float literal (2.5F).

### L2: Multistructural / block x execution / preoperational

L2 for literal: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

- **Edge:** `literal` &rarr; `literal@L2` (has_level)
- **Exact edge logic:** literal -&gt; L2 (Multistructural): the answer applies the rules of literal to every part of the code, in order (3 ways).

Ways (3), each with its exact rule:

- **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): A literal is evaluated at once, with no computation, and its evaluation always completes normally. An expression built from literals, such as 1/2, is still computed by its operators when it is reached.
- **[1] output\_prediction** (rule type OP, evaluation / result rule): A literal's value is itself, with a type fixed by its form: 1234 is int 1234, 3.0 is double, '1' is char (code 49), and "2.5" is a String, not a number.
- **[2] one\_step\_execution** (rule type OS, state-transition rule): A literal changes no state by itself. On the right of an assignment it supplies the value stored, e.g. a = 1234; sets a to 1234.

### L3: Relational / relations x function (concrete operational begins)

L3 for literal: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

- **Edge:** `literal` &rarr; `literal@L3` (has_level)
- **Exact edge logic:** literal -&gt; L3 (Relational): the answer relates the parts (5 ways).

Ways (5), each with its exact rule:

- **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): The form of a literal selects its primitive type, and that type must be assignable to the target: int x = 3.0; does not compile even though 3.0 is a whole number.
- **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Literals commonly initialize variables. The literal's type must equal or widen to the variable's type: double y = 1; widens, but int x = 1.1; is an error.
- **[2] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): E-notation is a form of double literal. 6.022e23 and even 1e6 are doubles, so int n = 1e6; needs a cast.
- **[3] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): A literal without L must lie in -2147483648..2147483647, so 2147483648 alone is a compile error. Larger values need a long literal (2147483648L).
- **[4] purpose\_of\_the\_whole** (rule type P, plan / role rule): Literals supply the fixed values a computation starts from: initial values of counters and totals (0), messages and labels, and known constants. A meaningful number that is repeated (a 'magic number') should become a named constant.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for literal: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

- **Edge:** `literal` &rarr; `literal@L4` (has_level)
- **Exact edge logic:** literal -&gt; L4 (Extended abstract): the answer reasons beyond the given code (5 ways).

Ways (5), each with its exact rule:

- **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `LargeIntegerLong`: Rewriting a literal in another form keeps the value but changes the type, and so the operation: 10 / 3 is 3 but 10.0 / 3 is 3.333..., and "5" + 1 is "51" but 5 + 1 is 6.
- **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Use a literal for a self-explanatory value fixed when the program is written (0, 1, "Hello"). Use a final named constant for a meaningful or repeated value, and command-line or standard input for values that change between runs.
- **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: An int literal must lie within the int range. Kind: compile-time. Trigger class: A digit sequence greater than 2147483647 without an L suffix (e.g. long big = 3000000000;): 'integer number too large'.
- **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: A char literal holds exactly one character in single quotes, and a String literal must be closed on the same line. Kind: compile-time. Trigger class: Writing 'ab', using single quotes for a word, or leaving out a closing quote: 'unclosed character literal' or 'unclosed string literal'.
- **[4] diagnose\_an\_error** (rule type D, error rule): rule broken: A leading 0 makes an integer literal octal. Kind: silent logic error. Trigger class: Zero-padded numbers such as 010 or 013 (evaluate to 8 and 11).

## Same topic

`literal` belongs to the topic **Data types and terminology (literals, identifiers, variables, declarations, assignment, expressions)** (`topic1.2.a`). The topic also contains: `assignment`, `chained_assignment`, `data_type`, `declaration`, `definite_assignment`, `expression`, `identifier`, `named_constants`, `naming_convention`, `operator_precedence`, `primitive_type`, `program_trace`, `variable`, `variable_swap`.

## Rules of the concept (21)

- **Book** (SW-1e, p. 15 (pdf 25)): "A literal is a source-code representation of a data-type value."
- **Book** (OT-Datatypes, ): "An integer literal is of type long if it ends with the letter L or l; otherwise it is of type int."
- **Book** (OT-Datatypes, ): "A floating-point literal is of type float if it ends with the letter F or f; otherwise its type is double and it can optionally end with the letter D or d."
- **Book** (OT-Datatypes, ): "Always use 'single quotes' for char literals and "double quotes" for String literals."
- **Book** (RS, ): "Character literals (of type char) are enclosed in single quotation marks and can include just one character"
- **Book** (RS, ): "Notice that 207. is considered a double even though it coincides with an integer because of the decimal point."
- **E** (folk-meaning rule): In everyday writing, 1,000,000, 007, 1/2 and $5 all stand for numbers. Java literals have strict forms: commas are not allowed, 1/2 is an int division expression worth 0, and a leading 0 makes the number octal (013 is 11).
- **M** (wrong rule / right rule): LargeIntegerLong: wrong: a large integer literal is automatically long \| right: A sequence of digits is an int literal only if its value falls within the int range; for larger values the book advises the long type.
- **M** (wrong rule / right rule): NoFloatLiterals: wrong: Java has no float literals \| right: A decimal literal ending in f is a float; without the f it is a double.
- **M** (wrong rule / right rule): NoLongLiterals: wrong: Java has no long literals \| right: An integer literal ending in L is a long.
- **M** (wrong rule / right rule): WholeNumberLiteralIsInt: wrong: 207. and 2.3e4 are int values because they are whole numbers. \| right: A decimal point or scientific notation makes the literal a double.
- **T** (uneven-application rule): Points to LT (each literal denotes one fixed value whose type is read from how it is written). Applied unevenly, a student reads 2.0 as an int in one place, or '7' as the number 7 in one expression and as a character in the next.
- **N** (identity rule): Literal: a source-code representation of one fixed data-type value, such as 42, 3.14, true, 'a' or "hi".
- **S** (declarative rule): A digit sequence within the int range is an int literal. A decimal point or e-notation makes a double (3.14, 6.022e23). Suffix L gives a long and f a float. true and false are boolean, one character in single quotes is a char, and characters in double quotes are a String. Integer literals can also be written in hexadecimal (0x1F), octal (a leading 0: 013 is 11) or binary (0b101) and may contain underscores (1\_000\_000); a trailing L makes a long literal (2147483648L) and a trailing F a float literal (2.5F).
- **LT** (operational sequencing rule): A literal is evaluated at once, with no computation, and its evaluation always completes normally. An expression built from literals, such as 1/2, is still computed by its operators when it is reached.
- **OP** (evaluation / result rule): A literal's value is itself, with a type fixed by its form: 1234 is int 1234, 3.0 is double, '1' is char (code 49), and "2.5" is a String, not a number.
- **OS** (state-transition rule): A literal changes no state by itself. On the right of an assignment it supplies the value stored, e.g. a = 1234; sets a to 1234.
- **R** (composition rule (with a neighbour)): with primitive\_type: The form of a literal selects its primitive type, and that type must be assignable to the target: int x = 3.0; does not compile even though 3.0 is a whole number.
- **R** (composition rule (with a neighbour)): with variable: Literals commonly initialize variables. The literal's type must equal or widen to the variable's type: double y = 1; widens, but int x = 1.1; is an error.
- **R** (composition rule (with a neighbour)): with scientific\_notation: E-notation is a form of double literal. 6.022e23 and even 1e6 are doubles, so int n = 1e6; needs a cast.
- **R** (composition rule (with a neighbour)): with int\_literal\_limit: A literal without L must lie in -2147483648..2147483647, so 2147483648 alone is a compile error. Larger values need a long literal (2147483648L).
- **P** (plan / role rule): Literals supply the fixed values a computation starts from: initial values of counters and totals (0), messages and labels, and known constants. A meaningful number that is repeated (a 'magic number') should become a named constant.
- **C** (conservation rule): Rewriting a literal in another form keeps the value but changes the type, and so the operation: 10 / 3 is 3 but 10.0 / 3 is 3.333..., and "5" + 1 is "51" but 5 + 1 is 6.
- **D** (error rule): rule broken: An int literal must lie within the int range. (compile-time)
- **D** (error rule): rule broken: A char literal holds exactly one character in single quotes, and a String literal must be closed on the same line. (compile-time)
- **D** (error rule): rule broken: A leading 0 makes an integer literal octal. (silent logic error)
- **X** (applicability rule): Use a literal for a self-explanatory value fixed when the program is written (0, 1, "Hello"). Use a final named constant for a meaningful or repeated value, and command-line or standard input for values that change between runs.

## How it is found in code and answers (reader block)

- **Aliases:** literal, literals
- **Code patterns:** `\b\d+(?:\.\d+)?\b`, `\btrue\b|\bfalse\b`, `\"`, `'`
- **Operator symbols:** none
- **Java types:** none

## The whole prerequisite chain

- **Everything it builds on (2):** `data_type`, `primitive_type`
- **Everything that builds on it (80):** `accumulator_pattern`, `animation`, `api`, `array_copy`, `array_exchange`, `array_reversal`, `array_traversal`, `assignment`, `boolean_expression`, `boolean_flag_array`, `break_statement`, `chained_assignment`, `comparison_operators`, `compound_assignment`, `conditional_operator`, `continue_statement`, `convergence_rate`, `convergence_test`, `coordinate_scaling`, `counter_pattern`, `dangling_else`, `debugging`, `do_while_loop`, `drawing_shapes`, `else_if_chain`, `enhanced_for`, `expression`, `fencepost_loop`, `flag_search_loop`, `for_loop`, `frequency_counting`, `function_plotting`, `if_else_statement`, `if_statement`, `increment_operators`, `infinite_loop`, `int_literal_limit`, `labeled_break`, `loop_body`, `loop_control`, `loop_invariant_reasoning`, `loop_performance`, `loop_scope`, `loop_variable`, `math_library`, `math_random`, `math_round`, `matrix_operations`, `method_call`, `monte_carlo_simulation`, `mouse_interaction`, `named_constants`, `naming_convention`, `nested_conditionals`, `nested_loops`, `number_conversion`, `off_by_one_error`, `operator_precedence`, `power_method`, `program_state`, `program_trace`, `random_move`, `row_major_order`, `running_extreme`, `sampling_without_replacement`, `scientific_notation`, `sentinel_loop`, `shuffle`, `side_effect_order`, `simulation_loop`, `standard_audio`, `standard_drawing`, `switch_statement`, `syntax_template`, `testing`, `trig_functions`, `two_models`, `variable`, `variable_swap`, `while_loop`

## Every edge in this view and its exact edge logic (31)

All the edges drawn in the picture, in the order: prerequisite, parallel, misconception, error, has_level, contains.

**1. `literal` &rarr; `int_literal_limit`** (prerequisite)

- **Exact edge logic:** An int literal is legal only if its value lies within the int range, so a digit sequence outside -2147483648..2147483647 is not a valid int literal.
- **Grounding:** book\_passage
- **Composition rule (R) of `literal` with `int_literal_limit`:** A literal without L must lie in -2147483648..2147483647, so 2147483648 alone is a compile error. Larger values need a long literal (2147483648L).
- **Composition rule (R) of `int_literal_limit` with `literal`:** The general literal rule (a source-code representation of a value) is constrained here by int's range: a digit sequence outside -2147483648..2147483647 is not a valid int literal and must be written as a long literal with L.

**2. `literal` &rarr; `scientific_notation`** (prerequisite)

- **Exact edge logic:** Scientific notation is a form of double literal.
- **Grounding:** book\_passage
- **Composition rule (R) of `literal` with `scientific_notation`:** E-notation is a form of double literal. 6.022e23 and even 1e6 are doubles, so int n = 1e6; needs a cast.
- **Composition rule (R) of `scientific_notation` with `literal`:** Scientific notation is a double literal, so the literal rules for double apply: it cannot initialize an int without a cast (int n = 1e6; does not compile).

**3. `literal` &rarr; `variable`** (prerequisite)

- **Exact edge logic:** A variable of type t is given a value of type t, often written as a literal.
- **Grounding:** order\_only
- **Composition rule (R) of `literal` with `variable`:** Literals commonly initialize variables. The literal's type must equal or widen to the variable's type: double y = 1; widens, but int x = 1.1; is an error.
- **Composition rule (R) of `variable` with `literal`:** Literals commonly give variables their values, and the literal's type must fit the variable's type (int x = 1.1; is rejected).

**4. `primitive_type` &rarr; `literal`** (prerequisite)

- **Exact edge logic:** A literal is the source-code form of a value of some type, and the way it is written fixes that type: 1234 is an int, 3.14 a double, true a boolean, 'c' a char.
- **Grounding:** book\_passage
- **Composition rule (R) of `primitive_type` with `literal`:** How a literal is written fixes its primitive type (1234 int, 3.14 double, true boolean, 'c' char), and it must fit the primitive type of the variable it initializes.
- **Composition rule (R) of `literal` with `primitive_type`:** The form of a literal selects its primitive type, and that type must be assignable to the target: int x = 3.0; does not compile even though 3.0 is a whole number.

**5. `literal` &rarr; `LargeIntegerLong`** (misconception)

- **Exact edge logic (the wrong rule):** A whole-number literal that is too big for an int automatically becomes a long.
- **Twin logic (the right rule):** A sequence of digits is an int literal only if its value falls within the int range; for larger values the book advises the long type.
- **Role:** primary

**6. `literal` &rarr; `NoFloatLiterals`** (misconception)

- **Exact edge logic (the wrong rule):** Java has no way to write a float literal.
- **Twin logic (the right rule):** A decimal literal ending in f is a float; without the f it is a double.
- **Role:** primary

**7. `literal` &rarr; `NoLongLiterals`** (misconception)

- **Exact edge logic (the wrong rule):** Java has no way to write a long literal.
- **Twin logic (the right rule):** An integer literal ending in L is a long.
- **Role:** primary

**8. `literal` &rarr; `WholeNumberLiteralIsInt`** (misconception)

- **Exact edge logic (the wrong rule):** 207. and 2.3e4 are int values because they are whole numbers.
- **Twin logic (the right rule):** A decimal point or scientific notation makes the literal a double.
- **Role:** primary

**9. `double` &rarr; `WholeNumberLiteralIsInt`** (misconception)

- **Exact edge logic (the wrong rule):** 207. and 2.3e4 are int values because they are whole numbers.
- **Twin logic (the right rule):** A decimal point or scientific notation makes the literal a double.
- **Role:** context

**10. `int_literal_limit` &rarr; `LargeIntegerLong`** (misconception)

- **Exact edge logic (the wrong rule):** a large integer literal is automatically long
- **Twin logic (the right rule):** A sequence of digits is an int literal only if its value falls within the int range; for larger values the book advises the long type.
- **Role:** context

**11. `long_type` &rarr; `LargeIntegerLong`** (misconception)

- **Exact edge logic (the wrong rule):** a large integer literal is automatically long
- **Twin logic (the right rule):** A sequence of digits is an int literal only if its value falls within the int range; for larger values the book advises the long type.
- **Role:** context

**12. `literal` &rarr; `literal@L0`** (has_level)

- **Exact edge logic:** literal -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (6 ways).
  - **[0] everyday\_reading** (rule type E, folk-meaning rule): In everyday writing, 1,000,000, 007, 1/2 and $5 all stand for numbers. Java literals have strict forms: commas are not allowed, 1/2 is an int division expression worth 0, and a leading 0 makes the number octal (013 is 11).
  - **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `LargeIntegerLong`: wrong rule: a large integer literal is automatically long. Right rule: A sequence of digits is an int literal only if its value falls within the int range; for larger values the book advises the long type.
  - **[2] misconception** (rule type M, wrong rule / right rule) &rarr; `NoFloatLiterals`: wrong rule: Java has no float literals. Right rule: A decimal literal ending in f is a float; without the f it is a double.
  - **[3] misconception** (rule type M, wrong rule / right rule) &rarr; `NoLongLiterals`: wrong rule: Java has no long literals. Right rule: An integer literal ending in L is a long.
  - **[4] misconception** (rule type M, wrong rule / right rule) &rarr; `WholeNumberLiteralIsInt`: wrong rule: 207. and 2.3e4 are int values because they are whole numbers. Right rule: A decimal point or scientific notation makes the literal a double.
  - **[5] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `LargeIntegerLong`: Points to LT (each literal denotes one fixed value whose type is read from how it is written). Applied unevenly, a student reads 2.0 as an int in one place, or '7' as the number 7 in one expression and as a character in the next. (here mixing in: "a large integer literal is automatically long")

**13. `literal` &rarr; `literal@L1`** (has_level)

- **Exact edge logic:** literal -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).
  - **[0] names\_the\_element** (rule type N, identity rule): Literal: a source-code representation of one fixed data-type value, such as 42, 3.14, true, 'a' or "hi".
  - **[1] states\_the\_rule** (rule type S, declarative rule): A digit sequence within the int range is an int literal. A decimal point or e-notation makes a double (3.14, 6.022e23). Suffix L gives a long and f a float. true and false are boolean, one character in single quotes is a char, and characters in double quotes are a String. Integer literals can also be written in hexadecimal (0x1F), octal (a leading 0: 013 is 11) or binary (0b101) and may contain underscores (1\_000\_000); a trailing L makes a long literal (2147483648L) and a trailing F a float literal (2.5F).

**14. `literal` &rarr; `literal@L2`** (has_level)

- **Exact edge logic:** literal -&gt; L2 (Multistructural): the answer applies the rules of literal to every part of the code, in order (3 ways).
  - **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): A literal is evaluated at once, with no computation, and its evaluation always completes normally. An expression built from literals, such as 1/2, is still computed by its operators when it is reached.
  - **[1] output\_prediction** (rule type OP, evaluation / result rule): A literal's value is itself, with a type fixed by its form: 1234 is int 1234, 3.0 is double, '1' is char (code 49), and "2.5" is a String, not a number.
  - **[2] one\_step\_execution** (rule type OS, state-transition rule): A literal changes no state by itself. On the right of an assignment it supplies the value stored, e.g. a = 1234; sets a to 1234.

**15. `literal` &rarr; `literal@L3`** (has_level)

- **Exact edge logic:** literal -&gt; L3 (Relational): the answer relates the parts (5 ways).
  - **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): The form of a literal selects its primitive type, and that type must be assignable to the target: int x = 3.0; does not compile even though 3.0 is a whole number.
  - **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Literals commonly initialize variables. The literal's type must equal or widen to the variable's type: double y = 1; widens, but int x = 1.1; is an error.
  - **[2] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): E-notation is a form of double literal. 6.022e23 and even 1e6 are doubles, so int n = 1e6; needs a cast.
  - **[3] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): A literal without L must lie in -2147483648..2147483647, so 2147483648 alone is a compile error. Larger values need a long literal (2147483648L).
  - **[4] purpose\_of\_the\_whole** (rule type P, plan / role rule): Literals supply the fixed values a computation starts from: initial values of counters and totals (0), messages and labels, and known constants. A meaningful number that is repeated (a 'magic number') should become a named constant.

**16. `literal` &rarr; `literal@L4`** (has_level)

- **Exact edge logic:** literal -&gt; L4 (Extended abstract): the answer reasons beyond the given code (5 ways).
  - **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `LargeIntegerLong`: Rewriting a literal in another form keeps the value but changes the type, and so the operation: 10 / 3 is 3 but 10.0 / 3 is 3.333..., and "5" + 1 is "51" but 5 + 1 is 6.
  - **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Use a literal for a self-explanatory value fixed when the program is written (0, 1, "Hello"). Use a final named constant for a meaningful or repeated value, and command-line or standard input for values that change between runs.
  - **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: An int literal must lie within the int range. Kind: compile-time. Trigger class: A digit sequence greater than 2147483647 without an L suffix (e.g. long big = 3000000000;): 'integer number too large'.
  - **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: A char literal holds exactly one character in single quotes, and a String literal must be closed on the same line. Kind: compile-time. Trigger class: Writing 'ab', using single quotes for a word, or leaving out a closing quote: 'unclosed character literal' or 'unclosed string literal'.
  - **[4] diagnose\_an\_error** (rule type D, error rule): rule broken: A leading 0 makes an integer literal octal. Kind: silent logic error. Trigger class: Zero-padded numbers such as 010 or 013 (evaluate to 8 and 11).

**17. `topic1.2.a` &rarr; `literal`** (contains)

- topic `topic1.2.a` contains `literal`

**18. `topic1.2.a` &rarr; `assignment`** (contains)

- topic `topic1.2.a` contains `assignment`

**19. `topic1.2.a` &rarr; `chained_assignment`** (contains)

- topic `topic1.2.a` contains `chained_assignment`

**20. `topic1.2.a` &rarr; `data_type`** (contains)

- topic `topic1.2.a` contains `data_type`

**21. `topic1.2.a` &rarr; `declaration`** (contains)

- topic `topic1.2.a` contains `declaration`

**22. `topic1.2.a` &rarr; `definite_assignment`** (contains)

- topic `topic1.2.a` contains `definite_assignment`

**23. `topic1.2.a` &rarr; `expression`** (contains)

- topic `topic1.2.a` contains `expression`

**24. `topic1.2.a` &rarr; `identifier`** (contains)

- topic `topic1.2.a` contains `identifier`

**25. `topic1.2.a` &rarr; `named_constants`** (contains)

- topic `topic1.2.a` contains `named_constants`

**26. `topic1.2.a` &rarr; `naming_convention`** (contains)

- topic `topic1.2.a` contains `naming_convention`

**27. `topic1.2.a` &rarr; `operator_precedence`** (contains)

- topic `topic1.2.a` contains `operator_precedence`

**28. `topic1.2.a` &rarr; `primitive_type`** (contains)

- topic `topic1.2.a` contains `primitive_type`

**29. `topic1.2.a` &rarr; `program_trace`** (contains)

- topic `topic1.2.a` contains `program_trace`

**30. `topic1.2.a` &rarr; `variable`** (contains)

- topic `topic1.2.a` contains `variable`

**31. `topic1.2.a` &rarr; `variable_swap`** (contains)

- topic `topic1.2.a` contains `variable_swap`
