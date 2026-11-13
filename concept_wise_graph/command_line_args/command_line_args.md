# command_line_args (`command_line_args`)

args[] -- strings passed at launch

Section 1.1 Your First Program, topic 1.1.d Input and output (command-line arguments).

![The knowledge graph around command_line_args](command_line_args.png)

## At a glance

- **Needs first:** `main_method`
- **Leads to:** `args_length`, `black_box_model`, `parsing`
- **Learned alongside:** `standard_input`
- **Misconceptions:** `ArgsAreNumbers`
- **Errors:** `ArgsAlwaysPresent`, `FirstArgIsArgsOne`
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 18 edges around this concept, each explained in the graph's own words.

## What it needs first (1)

A prerequisite edge means the other concept has to be understood before `command_line_args`.

### `main_method` comes before `command_line_args`

*public static void main(String[] args) -- entry point*

The command-line arguments arrive in main's parameter args, an array of Strings.

- **Grounding:** book passage
- **How `command_line_args` combines with `main_method`:** The arguments arrive in main's parameter args (String[] args).
- **How `main_method` combines with `command_line_args`:** The command-line arguments arrive in main's parameter args, an array of Strings (args[0], args[1], ...).

## What it leads to (3)

These concepts need `command_line_args` first.

### `command_line_args` comes before `args_length`

*args.length gives the number of command-line arguments*

args is the array of command-line arguments.

- **Grounding:** book passage
- **How `command_line_args` combines with `args_length`:** args.length is the number of arguments typed (0 if none), so valid indices are 0 to args.length-1.
- **How `args_length` combines with `command_line_args`:** args[i] may be read only for i &lt; args.length; with no arguments even args[0] is out of bounds.

### `command_line_args` comes before `black_box_model`

*Program as a black box: a program viewed as a black box that turns an input string (the command-line argument) into an output string*

The black-box view treats the command-line argument as the input string and what the program prints as the output string.

- **Grounding:** book passage
- **How `command_line_args` combines with `black_box_model`:** In the black-box view the command-line argument is the input string and what the program prints is the output string.
- **How `black_box_model` combines with `command_line_args`:** The command-line argument is the box's input string, and what the program prints is its output string; parseInt lets the strings be read as numbers.

### `command_line_args` comes before `parsing`

*Integer.parseInt / Double.parseDouble turn text into numbers*

args[k] is always a String, so Integer.parseInt(args[k]) is needed before it can be used as a number.

- **Grounding:** book passage
- **How `command_line_args` combines with `parsing`:** args[k] is always a String, so Integer.parseInt(args[k]) or Double.parseDouble(args[k]) must convert it before arithmetic.
- **How `parsing` combines with `command_line_args`:** Because args[k] is always a String, a numeric argument must be passed through a parse method before it can be used in arithmetic or comparisons.

## Learned alongside (1)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

### `command_line_args` alongside `standard_input`

*StdIn -- reading a stream of values*

Command-line arguments are a fixed number of strings given once when the program starts (args[]); standard input is a stream of any length read while the program runs (StdIn.readInt()). Both arrive as text and must be parsed into numbers.

- **Grounding:** book passage

## Misconceptions (1)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### ArgsAreNumbers

- **Wrong rule:** If a number is typed when the program is launched, args[0] is already an int and can be used in arithmetic.
- **Right rule:** args[0] is always a String, so Integer.parseInt(args[0]) is needed to get its number.
- **Role of this concept:** context
- **Shows at level L0 as:** misconception: wrong rule: Command-line arguments arrive already typed as numbers, so no parsing is needed. Right rule: args[0] is always a String, so Integer.parseInt(args[0]) is needed to get its number.
- **Shows at level L0 as:** inconsistent trace: Applies the args rule unevenly: maps the first typed word to args[0] on one run but to args[1] on another, or treats a numeric argument as a String in one place and as an int in another. (here mixing in: "command-line args arrive already typed, no parsing needed")
- **Also an edge from `parsing`:** If a number is typed when the program is launched, args[0] is already an int and can be used in arithmetic.

## Errors (2)

An error edge states the rule that gets broken in a program, and the right rule.

### ArgsAlwaysPresent

- **Wrong rule:** args[0] can always be read.
- **Right rule:** If you run the program without typing the command-line argument it expects, reading args[0] fails with java.lang.ArrayIndexOutOfBoundsException: 0.
- **Role of this concept:** context
- **Also an edge from `args_length`:** args[0] can always be read.
- **Also an edge from `run_time_error`:** args[0] can always be read.

### FirstArgIsArgsOne

- **Wrong rule:** The first command-line argument is args[1].
- **Right rule:** Counting starts at 0: the first argument is args[0], the second args[1].
- **Role of this concept:** primary

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for command line args: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to command line args agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

command line args -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (3 ways).

- **everyday reading** (folk-meaning rule): Everyday/maths reading: '1234' typed on the command line is a number, and the first item in a list is item 1. Java rule: every command-line argument arrives as a String in args, and the first is args[0].
- **misconception** (wrong rule / right rule; shows `ArgsAreNumbers`): wrong rule: Command-line arguments arrive already typed as numbers, so no parsing is needed. Right rule: args[0] is always a String, so Integer.parseInt(args[0]) is needed to get its number.
- **inconsistent trace** (uneven-application rule; shows `ArgsAreNumbers`): Applies the args rule unevenly: maps the first typed word to args[0] on one run but to args[1] on another, or treats a numeric argument as a String in one place and as an int in another. (here mixing in: "command-line args arrive already typed, no parsing needed")

### L1: Unistructural / atom x text surface

L1 for command line args: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

command line args -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

- **names the element** (identity rule): Command-line arguments are the strings typed after the class name in java Name a b c; they reach main as the String array args.
- **states the rule** (declarative rule): args[0] represents the first string typed on the command line, args[1] the second, and so on (counting starts at 0); every element is a String.

### L2: Multistructural / block x execution / preoperational

L2 for command line args: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

command line args -&gt; L2 (Multistructural): the answer applies the rules of command line args to every part of the code, in order (3 ways).

- **line by line trace** (operational sequencing rule): At launch the JVM splits the words after java Name at spaces, stores them in order in args, then calls main(args); the program reads args[k] whenever that expression is evaluated.
- **output prediction** (evaluation / result rule): args[k] evaluates to the k-th typed string, e.g. java UseArgument Alice gives args[0] = "Alice" and prints Hi, Alice. How are you?
- **one step execution** (state-transition rule): Reading args[k] changes nothing; args is set once at launch and the same program gives different outputs only because different arguments were typed.

### L3: Relational / relations x function (concrete operational begins)

L3 for command line args: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

command line args -&gt; L3 (Relational): the answer relates the parts (6 ways).

- **relation to neighbour** (composition rule (with a neighbour)): args[k] is always a String, so Integer.parseInt(args[k]) or Double.parseDouble(args[k]) must convert it before arithmetic.
- **relation to neighbour** (composition rule (with a neighbour)): The arguments arrive in main's parameter args (String[] args).
- **relation to neighbour** (composition rule (with a neighbour)): args.length is the number of arguments typed (0 if none), so valid indices are 0 to args.length-1.
- **relation to neighbour** (composition rule (with a neighbour)): In the black-box view the command-line argument is the input string and what the program prints is the output string.
- **relation to neighbour** (composition rule (with a neighbour)): Command-line arguments are a fixed number of strings given once when the program starts (args[]); standard input is a stream of any length read while the program runs (StdIn.readInt()). Both arrive as text and must be parsed into numbers.
- **purpose of the whole** (plan / role rule): Purpose: give the program its input at launch so the same compiled program can be tailored to different data without editing or recompiling.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for command line args: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

command line args -&gt; L4 (Extended abstract): the answer reasons beyond the given code (6 ways).

- **predict a change** (conservation rule; shows `ArgsAreNumbers`): Changing the typed arguments changes the output but not the program; typing fewer arguments than the program reads causes ArrayIndexOutOfBoundsException; extra arguments are ignored unless read.
- **diagnose an error** (error rule): rule broken: Counting starts at 0: the first argument is args[0]. Kind: silent logic error. Trigger class: using args[1] for the first argument: wrong argument used, or ArrayIndexOutOfBoundsException: 1 if only one was typed
- **transfer to a new program** (applicability rule): Use command-line arguments for a few small inputs known at launch (sizes, names, seeds); use standard input for long or interactive input.
- **diagnose an error** (error rule): rule broken: args[k] exists only if at least k+1 arguments were typed. Kind: run-time exception. Trigger class: running without the expected argument: java.lang.ArrayIndexOutOfBoundsException: 0
- **diagnose an error** (error rule): rule broken: Arguments are Strings; numbers must be parsed. Kind: compile-time. Trigger class: int n = args[0]; incompatible types: String cannot be converted to int
- **diagnose an error** (error rule): rule broken: Integer.parseInt needs digits. Kind: run-time exception. Trigger class: java Prog five or 12.2 where an int is parsed: NumberFormatException

## Same topic

`command_line_args` belongs to the topic **Input and output (command-line arguments)** (`topic1.1.d`). The topic also contains: `black_box_model`.

## Rules of the concept (19)

- **folk-meaning rule:** Everyday/maths reading: '1234' typed on the command line is a number, and the first item in a list is item 1. Java rule: every command-line argument arrives as a String in args, and the first is args[0].
- **wrong rule / right rule:** ArgsAreNumbers: wrong: Command-line arguments arrive already typed as numbers, so no parsing is needed. \| right: args[0] is always a String, so Integer.parseInt(args[0]) is needed to get its number.
- **uneven-application rule:** Applies the args rule unevenly: maps the first typed word to args[0] on one run but to args[1] on another, or treats a numeric argument as a String in one place and as an int in another.
- **identity rule:** Command-line arguments are the strings typed after the class name in java Name a b c; they reach main as the String array args.
- **declarative rule:** args[0] represents the first string typed on the command line, args[1] the second, and so on (counting starts at 0); every element is a String.
- **operational sequencing rule:** At launch the JVM splits the words after java Name at spaces, stores them in order in args, then calls main(args); the program reads args[k] whenever that expression is evaluated.
- **evaluation / result rule:** args[k] evaluates to the k-th typed string, e.g. java UseArgument Alice gives args[0] = "Alice" and prints Hi, Alice. How are you?
- **state-transition rule:** Reading args[k] changes nothing; args is set once at launch and the same program gives different outputs only because different arguments were typed.
- **composition rule (with a neighbour):** with parsing: args[k] is always a String, so Integer.parseInt(args[k]) or Double.parseDouble(args[k]) must convert it before arithmetic.
- **composition rule (with a neighbour):** with main\_method: The arguments arrive in main's parameter args (String[] args).
- **composition rule (with a neighbour):** with args\_length: args.length is the number of arguments typed (0 if none), so valid indices are 0 to args.length-1.
- **composition rule (with a neighbour):** with black\_box\_model: In the black-box view the command-line argument is the input string and what the program prints is the output string.
- **plan / role rule:** Purpose: give the program its input at launch so the same compiled program can be tailored to different data without editing or recompiling.
- **conservation rule:** Changing the typed arguments changes the output but not the program; typing fewer arguments than the program reads causes ArrayIndexOutOfBoundsException; extra arguments are ignored unless read.
- **error rule:** rule broken: args[k] exists only if at least k+1 arguments were typed (run-time exception)
- **error rule:** rule broken: Counting starts at 0: the first argument is args[0] (silent logic error)
- **error rule:** rule broken: Arguments are Strings; numbers must be parsed (compile-time)
- **error rule:** rule broken: Integer.parseInt needs digits (run-time exception)
- **applicability rule:** Use command-line arguments for a few small inputs known at launch (sizes, names, seeds); use standard input for long or interactive input.

## The whole prerequisite chain

- **Everything it builds on (3):** `class_declaration`, `main_method`, `program_text`
- **Everything that builds on it (11):** `accumulator_pattern`, `args_length`, `black_box_model`, `compound_assignment`, `explicit_cast`, `math_random`, `monte_carlo_simulation`, `parsing`, `sentinel_loop`, `type_conversion`, `widening_conversion`
