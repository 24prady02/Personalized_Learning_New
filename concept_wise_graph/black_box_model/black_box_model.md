# Program as a black box (`black_box_model`)

a program viewed as a black box that turns an input string (the command-line argument) into an output string

Section 1.1 1.1 Your First Program, topic 1.1.d Input and output (command-line arguments).

![The knowledge graph around black_box_model](black_box_model.png)

## At a glance

- **Needs first:** `command_line_args`
- **Leads to:** nothing
- **Learned alongside:** nothing
- **Misconceptions:** none
- **Errors:** none
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 8 edges around this concept, each explained in the graph's own words.

## What it needs first (1)

A prerequisite edge means the other concept has to be understood before `black_box_model`.

### `command_line_args` comes before `black_box_model`

*args[] -- strings passed at launch*

The black-box view treats the command-line argument as the input string and what the program prints as the output string.

- **Grounding:** book passage
- **How `black_box_model` combines with `command_line_args`:** The command-line argument is the box's input string, and what the program prints is its output string; parseInt lets the strings be read as numbers.
- **How `command_line_args` combines with `black_box_model`:** In the black-box view the command-line argument is the input string and what the program prints is the output string.

## What it leads to (0)

These concepts need `black_box_model` first.

No concept has this one as a prerequisite.

## Learned alongside (0)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

No parallel edge touches this concept.

## Misconceptions (0)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

The graph has no misconception edge from this concept.

## Errors (0)

An error edge states the rule that gets broken in a program, and the right rule.

The graph has no error edge from this concept.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for Program as a black box: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to Program as a black box agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

Program as a black box -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (1 way).

- **everyday reading** (folk-meaning rule): Everyday meaning: a 'black box' is something mysterious or a flight recorder. Here it means treating a program purely as a function from its input string (the command-line argument) to its output string, ignoring how it works inside.

### L1: Unistructural / atom x text surface

L1 for Program as a black box: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

Program as a black box -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

- **names the element** (identity rule): The black-box model is the view of a Java program as a box that converts an input string (the command-line argument) into an output string (what it prints).
- **states the rule** (declarative rule): A program like UseArgument implements a function that maps a string of characters (the argument) into another string of characters (the message printed); the model is general enough, in principle, for any computational task.

### L2: Multistructural / block x execution / preoperational

L2 for Program as a black box: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

Program as a black box -&gt; L2 (Multistructural): the answer applies the rules of Program as a black box to every part of the code, in order (3 ways).

- **line by line trace** (operational sequencing rule): Input is supplied at launch, the program computes, output is produced; the model hides the order of internal steps.
- **output prediction** (evaluation / result rule): Prediction at this level is input-output: for UseArgument, input Alice gives output Hi, Alice. How are you?
- **one step execution** (state-transition rule): One run maps one input string to one output string; nothing persists between runs.

### L3: Relational / relations x function (concrete operational begins)

L3 for Program as a black box: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

Program as a black box -&gt; L3 (Relational): the answer relates the parts (2 ways).

- **relation to neighbour** (composition rule (with a neighbour)): The command-line argument is the box's input string, and what the program prints is its output string; parseInt lets the strings be read as numbers.
- **purpose of the whole** (plan / role rule): Purpose: describe what a program does (its specification, input to output) separately from how it does it; the compiler itself fits the model (.java text in, .class out).

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for Program as a black box: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

Program as a black box -&gt; L4 (Extended abstract): the answer reasons beyond the given code (4 ways).

- **predict a change** (conservation rule): Any change inside the box that keeps every input-output pair the same keeps the program's behaviour; a change that alters any pair is a behaviour change.
- **transfer to a new program** (applicability rule): Use the black-box view to specify and test programs by input/output pairs; it extends in 1.5 to standard input, standard output, drawing and audio. It does not help to locate an error inside the box; for that, trace the code.
- **diagnose an error** (error rule): rule broken: The output depends only on the input given. Kind: run-time exception. Trigger class: running the box with missing input (no argument): the box fails with ArrayIndexOutOfBoundsException rather than mapping input to output
- **diagnose an error** (error rule): rule broken: Input and output in 1.1 are limited to strings of limited size. Kind: silent logic error. Trigger class: expecting numeric or long input to be used directly without parsing or standard input

## Same topic

`black_box_model` belongs to the topic **Input and output (command-line arguments)** (`topic1.1.d`). The topic also contains: `command_line_args`.

## Rules of the concept (13)

- **folk-meaning rule:** Everyday meaning: a 'black box' is something mysterious or a flight recorder. Here it means treating a program purely as a function from its input string (the command-line argument) to its output string, ignoring how it works inside.
- **uneven-application rule:** Applies the model unevenly: treats the program as input-to-output on one run but expects it to remember an earlier run's input, or counts the program text itself as input.
- **identity rule:** The black-box model is the view of a Java program as a box that converts an input string (the command-line argument) into an output string (what it prints).
- **declarative rule:** A program like UseArgument implements a function that maps a string of characters (the argument) into another string of characters (the message printed); the model is general enough, in principle, for any computational task.
- **operational sequencing rule:** Input is supplied at launch, the program computes, output is produced; the model hides the order of internal steps.
- **evaluation / result rule:** Prediction at this level is input-output: for UseArgument, input Alice gives output Hi, Alice. How are you?
- **state-transition rule:** One run maps one input string to one output string; nothing persists between runs.
- **composition rule (with a neighbour):** with command\_line\_args: The command-line argument is the box's input string, and what the program prints is its output string; parseInt lets the strings be read as numbers.
- **plan / role rule:** Purpose: describe what a program does (its specification, input to output) separately from how it does it; the compiler itself fits the model (.java text in, .class out).
- **conservation rule:** Any change inside the box that keeps every input-output pair the same keeps the program's behaviour; a change that alters any pair is a behaviour change.
- **error rule:** rule broken: The output depends only on the input given (run-time exception)
- **error rule:** rule broken: Input and output in 1.1 are limited to strings of limited size (silent logic error)
- **applicability rule:** Use the black-box view to specify and test programs by input/output pairs; it extends in 1.5 to standard input, standard output, drawing and audio. It does not help to locate an error inside the box; for that, trace the code.

## The whole prerequisite chain

- **Everything it builds on (4):** `class_declaration`, `command_line_args`, `main_method`, `program_text`
- **Everything that builds on it (0):** nothing
