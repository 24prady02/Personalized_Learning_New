# args_length (`args_length`)

args.length gives the number of command-line arguments

Section 1.4 Arrays, topic 1.4.a Arrays in Java (declare, create, initialize; indexing; length; default values).

![The knowledge graph around args_length](args_length.png)

## At a glance

- **Needs first:** `command_line_args`, `length_field`
- **Leads to:** nothing
- **Learned alongside:** nothing
- **Misconceptions:** none
- **Errors:** `ArgsAlwaysPresent`
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 18 edges around this concept. The edge logic, the wrong and right rules and the exact rules of the ways are copied word for word from the graph.

## To work on (0)

Nothing is missing for this concept.

## What it needs first (2)

A prerequisite edge means the other concept has to be understood before `args_length`.

### `command_line_args` comes before `args_length`

*args[] -- strings passed at launch*

- **Edge:** `pre:command_line_args->args_length`
- **Exact edge logic:** args is the array of command-line arguments.
- **Grounding:** book\_passage
- **Composition rule (R) of `args_length` with `command_line_args`:** args[i] may be read only for i &lt; args.length; with no arguments even args[0] is out of bounds.
- **Composition rule (R) of `command_line_args` with `args_length`:** args.length is the number of arguments typed (0 if none), so valid indices are 0 to args.length-1.

### `length_field` comes before `args_length`

*a.length is a field, not a method*

- **Edge:** `pre:length_field->args_length`
- **Exact edge logic:** args is an ordinary String array, so args.length is its length field and counts the command-line arguments.
- **Grounding:** order\_only
- **Composition rule (R) of `args_length` with `length_field`:** args.length is the ordinary array length field applied to the String[] args.
- **Composition rule (R) of `length_field` with `args_length`:** args is an ordinary String[], so args.length is its length field and counts the command-line arguments (0 when none are typed).

## What it leads to (0)

These concepts need `args_length` first.

No concept has this one as a prerequisite.

## Learned alongside (0)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

No parallel edge touches this concept.

## Misconceptions (0)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

The graph has no misconception edge from this concept.

## Errors (1)

An error edge states the rule that gets broken in a program, and the right rule.

### ArgsAlwaysPresent

- **Edge:** `args_length` &rarr; `ArgsAlwaysPresent` (error)
- **Exact edge logic (the wrong rule):** args[0] can always be read.
- **Twin logic (the right rule):** If you run the program without typing the command-line argument it expects, reading args[0] fails with java.lang.ArrayIndexOutOfBoundsException: 0.
- **Wrong belief (on the node):** args[0] can always be read.
- **Correct rule (on the node):** If you run the program without typing the command-line argument it expects, reading args[0] fails with java.lang.ArrayIndexOutOfBoundsException: 0.
- **Provenance:** textbook
- **Role of this concept:** primary
- **Edge `command_line_args` &rarr; `ArgsAlwaysPresent`, exact edge logic:** args[0] can always be read. **Twin logic:** If you run the program without typing the command-line argument it expects, reading args[0] fails with java.lang.ArrayIndexOutOfBoundsException: 0. (role: context)
- **Edge `run_time_error` &rarr; `ArgsAlwaysPresent`, exact edge logic:** args[0] can always be read. **Twin logic:** If you run the program without typing the command-line argument it expects, reading args[0] fails with java.lang.ArrayIndexOutOfBoundsException: 0. (role: context)

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for args length: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to args length agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

- **Edge:** `args_length` &rarr; `args_length@L0` (has_level)
- **Exact edge logic:** args length -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (1 way).

Ways (1), each with its exact rule:

- **[0] everyday\_reading** (rule type E, folk-meaning rule): Folk meaning: like a conversation partner, the program is thought to 'get' the input it expects; arguments are always there. Java rule: args holds exactly the strings typed after the class name, so args.length can be 0 and args[0] exists only when args.length &gt;= 1.

### L1: Unistructural / atom x text surface

L1 for args length: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

- **Edge:** `args_length` &rarr; `args_length@L1` (has_level)
- **Exact edge logic:** args length -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

Ways (2), each with its exact rule:

- **[0] names\_the\_element** (rule type N, identity rule): Identity: args.length is the length field of main's String[] parameter args; it counts the command-line arguments.
- **[1] states\_the\_rule** (rule type S, declarative rule): Declarative: args is a String[] whose elements args[0] .. args[args.length-1] are the typed arguments, as strings; numbers must be converted with Integer.parseInt or Double.parseDouble.

### L2: Multistructural / block x execution / preoperational

L2 for args length: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

- **Edge:** `args_length` &rarr; `args_length@L2` (has_level)
- **Exact edge logic:** args length -&gt; L2 (Multistructural): the answer applies the rules of args length to every part of the code, in order (3 ways).

Ways (3), each with its exact rule:

- **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): Sequencing: the command line is split at whitespace, and the pieces are stored in order in args before main's first statement runs. Reading args.length then behaves like any length field.
- **[1] output\_prediction** (rule type OP, evaluation / result rule): Result: an int equal to the number of typed arguments: 'java Max' gives 0, and 'java Max 10 -3 55 0 14' gives 5.
- **[2] one\_step\_execution** (rule type OS, state-transition rule): State transition: reading args.length changes nothing; args itself is fixed for the whole run.

### L3: Relational / relations x function (concrete operational begins)

L3 for args length: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

- **Edge:** `args_length` &rarr; `args_length@L3` (has_level)
- **Exact edge logic:** args length -&gt; L3 (Relational): the answer relates the parts (3 ways).

Ways (3), each with its exact rule:

- **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): args[i] may be read only for i &lt; args.length; with no arguments even args[0] is out of bounds.
- **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): args.length is the ordinary array length field applied to the String[] args.
- **[2] purpose\_of\_the\_whole** (rule type P, plan / role rule): Plan/role: validate input before use (print a usage message and return when args.length is too small), or loop over a variable number of arguments.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for args length: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

- **Edge:** `args_length` &rarr; `args_length@L4` (has_level)
- **Exact edge logic:** args length -&gt; L4 (Extended abstract): the answer reasons beyond the given code (4 ways).

Ways (4), each with its exact rule:

- **[0] predict\_a\_change** (rule type C, conservation rule): Conservation: extra arguments do not break code that reads args[0]; fewer arguments than the code reads break it at run time. Adding an args.length check keeps behaviour for correct input and only changes what happens for bad input.
- **[1] diagnose\_an\_error** (rule type D, error rule): rule broken: args[i] exists only if i &lt; args.length. Kind: run-time exception. Trigger class: the program is run with fewer command-line arguments than it reads, e.g. none at all (java.lang.ArrayIndexOutOfBoundsException: 0)
- **[2] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Applicability: use args.length to validate or iterate over a small, variable number of command-line values. For large or open-ended input, read standard input instead.
- **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: An argument is a String and must be a valid numeral to be parsed. Kind: run-time exception. Trigger class: a non-numeric argument is passed to Integer.parseInt, e.g. 'five' (NumberFormatException)

## Same topic

`args_length` belongs to the topic **Arrays in Java (declare, create, initialize; indexing; length; default values)** (`topic1.4.a`). The topic also contains: `array_creation`, `array_declaration`, `array_default_values`, `data_structure`, `indexing`, `length_field`, `off_by_one_error`.

## Rules of the concept (14)

- **Book** (TJ-2e, p. 152 (pdf 174)): "Now that you know about strings, arrays, and wrapper classes, we can finally explain the args"
- **Book** (SW-1.4, ): "takes a variable number of command-line arguments and prints how many there are."
- **E** (folk-meaning rule): Folk meaning: like a conversation partner, the program is thought to 'get' the input it expects; arguments are always there. Java rule: args holds exactly the strings typed after the class name, so args.length can be 0 and args[0] exists only when args.length &gt;= 1.
- **T** (uneven-application rule): Points to LT: args is built before main runs, and its length is fixed for the run. Inconsistent application: args[0] is read on one line, and args.length is checked only later (or never), as if checking were needed only sometimes.
- **N** (identity rule): Identity: args.length is the length field of main's String[] parameter args; it counts the command-line arguments.
- **S** (declarative rule): Declarative: args is a String[] whose elements args[0] .. args[args.length-1] are the typed arguments, as strings; numbers must be converted with Integer.parseInt or Double.parseDouble.
- **LT** (operational sequencing rule): Sequencing: the command line is split at whitespace, and the pieces are stored in order in args before main's first statement runs. Reading args.length then behaves like any length field.
- **OP** (evaluation / result rule): Result: an int equal to the number of typed arguments: 'java Max' gives 0, and 'java Max 10 -3 55 0 14' gives 5.
- **OS** (state-transition rule): State transition: reading args.length changes nothing; args itself is fixed for the whole run.
- **R** (composition rule (with a neighbour)): with command\_line\_args: args[i] may be read only for i &lt; args.length; with no arguments even args[0] is out of bounds.
- **R** (composition rule (with a neighbour)): with length\_field: args.length is the ordinary array length field applied to the String[] args.
- **P** (plan / role rule): Plan/role: validate input before use (print a usage message and return when args.length is too small), or loop over a variable number of arguments.
- **C** (conservation rule): Conservation: extra arguments do not break code that reads args[0]; fewer arguments than the code reads break it at run time. Adding an args.length check keeps behaviour for correct input and only changes what happens for bad input.
- **D** (error rule): rule broken: args[i] exists only if i &lt; args.length. (run-time exception)
- **D** (error rule): rule broken: An argument is a String and must be a valid numeral to be parsed. (run-time exception)
- **X** (applicability rule): Applicability: use args.length to validate or iterate over a small, variable number of command-line values. For large or open-ended input, read standard input instead.

## How it is found in code and answers (reader block)

- **Aliases:** args.length
- **Code patterns:** `\bargs\.length\b`
- **Operator symbols:** none
- **Java types:** none

## The whole prerequisite chain

- **Everything it builds on (10):** `array_creation`, `array_declaration`, `array_initializer`, `class_declaration`, `command_line_args`, `data_structure`, `data_type`, `length_field`, `main_method`, `program_text`
- **Everything that builds on it (0):** nothing

## Every edge in this view and its exact edge logic (18)

All the edges drawn in the picture, in the order: prerequisite, parallel, misconception, error, has_level, contains.

**1. `command_line_args` &rarr; `args_length`** (prerequisite)

- **Exact edge logic:** args is the array of command-line arguments.
- **Grounding:** book\_passage
- **Composition rule (R) of `command_line_args` with `args_length`:** args.length is the number of arguments typed (0 if none), so valid indices are 0 to args.length-1.
- **Composition rule (R) of `args_length` with `command_line_args`:** args[i] may be read only for i &lt; args.length; with no arguments even args[0] is out of bounds.

**2. `length_field` &rarr; `args_length`** (prerequisite)

- **Exact edge logic:** args is an ordinary String array, so args.length is its length field and counts the command-line arguments.
- **Grounding:** order\_only
- **Composition rule (R) of `length_field` with `args_length`:** args is an ordinary String[], so args.length is its length field and counts the command-line arguments (0 when none are typed).
- **Composition rule (R) of `args_length` with `length_field`:** args.length is the ordinary array length field applied to the String[] args.

**3. `args_length` &rarr; `ArgsAlwaysPresent`** (error)

- **Exact edge logic (the wrong rule):** args[0] can always be read.
- **Twin logic (the right rule):** If you run the program without typing the command-line argument it expects, reading args[0] fails with java.lang.ArrayIndexOutOfBoundsException: 0.
- **Role:** primary

**4. `command_line_args` &rarr; `ArgsAlwaysPresent`** (error)

- **Exact edge logic (the wrong rule):** args[0] can always be read.
- **Twin logic (the right rule):** If you run the program without typing the command-line argument it expects, reading args[0] fails with java.lang.ArrayIndexOutOfBoundsException: 0.
- **Role:** context

**5. `run_time_error` &rarr; `ArgsAlwaysPresent`** (error)

- **Exact edge logic (the wrong rule):** args[0] can always be read.
- **Twin logic (the right rule):** If you run the program without typing the command-line argument it expects, reading args[0] fails with java.lang.ArrayIndexOutOfBoundsException: 0.
- **Role:** context

**6. `args_length` &rarr; `args_length@L0`** (has_level)

- **Exact edge logic:** args length -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (1 way).
  - **[0] everyday\_reading** (rule type E, folk-meaning rule): Folk meaning: like a conversation partner, the program is thought to 'get' the input it expects; arguments are always there. Java rule: args holds exactly the strings typed after the class name, so args.length can be 0 and args[0] exists only when args.length &gt;= 1.

**7. `args_length` &rarr; `args_length@L1`** (has_level)

- **Exact edge logic:** args length -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).
  - **[0] names\_the\_element** (rule type N, identity rule): Identity: args.length is the length field of main's String[] parameter args; it counts the command-line arguments.
  - **[1] states\_the\_rule** (rule type S, declarative rule): Declarative: args is a String[] whose elements args[0] .. args[args.length-1] are the typed arguments, as strings; numbers must be converted with Integer.parseInt or Double.parseDouble.

**8. `args_length` &rarr; `args_length@L2`** (has_level)

- **Exact edge logic:** args length -&gt; L2 (Multistructural): the answer applies the rules of args length to every part of the code, in order (3 ways).
  - **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): Sequencing: the command line is split at whitespace, and the pieces are stored in order in args before main's first statement runs. Reading args.length then behaves like any length field.
  - **[1] output\_prediction** (rule type OP, evaluation / result rule): Result: an int equal to the number of typed arguments: 'java Max' gives 0, and 'java Max 10 -3 55 0 14' gives 5.
  - **[2] one\_step\_execution** (rule type OS, state-transition rule): State transition: reading args.length changes nothing; args itself is fixed for the whole run.

**9. `args_length` &rarr; `args_length@L3`** (has_level)

- **Exact edge logic:** args length -&gt; L3 (Relational): the answer relates the parts (3 ways).
  - **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): args[i] may be read only for i &lt; args.length; with no arguments even args[0] is out of bounds.
  - **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): args.length is the ordinary array length field applied to the String[] args.
  - **[2] purpose\_of\_the\_whole** (rule type P, plan / role rule): Plan/role: validate input before use (print a usage message and return when args.length is too small), or loop over a variable number of arguments.

**10. `args_length` &rarr; `args_length@L4`** (has_level)

- **Exact edge logic:** args length -&gt; L4 (Extended abstract): the answer reasons beyond the given code (4 ways).
  - **[0] predict\_a\_change** (rule type C, conservation rule): Conservation: extra arguments do not break code that reads args[0]; fewer arguments than the code reads break it at run time. Adding an args.length check keeps behaviour for correct input and only changes what happens for bad input.
  - **[1] diagnose\_an\_error** (rule type D, error rule): rule broken: args[i] exists only if i &lt; args.length. Kind: run-time exception. Trigger class: the program is run with fewer command-line arguments than it reads, e.g. none at all (java.lang.ArrayIndexOutOfBoundsException: 0)
  - **[2] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Applicability: use args.length to validate or iterate over a small, variable number of command-line values. For large or open-ended input, read standard input instead.
  - **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: An argument is a String and must be a valid numeral to be parsed. Kind: run-time exception. Trigger class: a non-numeric argument is passed to Integer.parseInt, e.g. 'five' (NumberFormatException)

**11. `topic1.4.a` &rarr; `args_length`** (contains)

- topic `topic1.4.a` contains `args_length`

**12. `topic1.4.a` &rarr; `array_creation`** (contains)

- topic `topic1.4.a` contains `array_creation`

**13. `topic1.4.a` &rarr; `array_declaration`** (contains)

- topic `topic1.4.a` contains `array_declaration`

**14. `topic1.4.a` &rarr; `array_default_values`** (contains)

- topic `topic1.4.a` contains `array_default_values`

**15. `topic1.4.a` &rarr; `data_structure`** (contains)

- topic `topic1.4.a` contains `data_structure`

**16. `topic1.4.a` &rarr; `indexing`** (contains)

- topic `topic1.4.a` contains `indexing`

**17. `topic1.4.a` &rarr; `length_field`** (contains)

- topic `topic1.4.a` contains `length_field`

**18. `topic1.4.a` &rarr; `off_by_one_error`** (contains)

- topic `topic1.4.a` contains `off_by_one_error`
