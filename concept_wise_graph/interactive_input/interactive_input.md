# interactive_input (`interactive_input`)

the user's input can change the program's control flow while it runs

Section 1.5 Input and Output, topic 1.5.c Standard input.

![The knowledge graph around interactive_input](interactive_input.png)

## At a glance

- **Needs first:** `standard_input`
- **Leads to:** nothing
- **Learned alongside:** nothing
- **Misconceptions:** `InputFixedBeforeRun`
- **Errors:** none
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 15 edges around this concept, each explained in the graph's own words.

## What it needs first (1)

A prerequisite edge means the other concept has to be understood before `interactive_input`.

### `standard_input` comes before `interactive_input`

*StdIn -- reading a stream of values*

Standard input can be read at any time while the program runs, so the user can type values that change its control flow during execution.

- **Grounding:** book passage
- **How `interactive_input` combines with `standard_input`:** Because a StdIn read can run at any point, a read placed inside the game loop lets each reply choose the branch taken in that round.
- **How `standard_input` combines with `interactive_input`:** Because a read can run at any point in execution, a read inside a loop lets each typed value decide the next branch.

## What it leads to (0)

These concepts need `interactive_input` first.

No concept has this one as a prerequisite.

## Learned alongside (0)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

No parallel edge touches this concept.

## Misconceptions (1)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### InputFixedBeforeRun

- **Wrong rule:** All input to a program is fixed before it starts running.
- **Right rule:** With interactive input the user can change the control flow while the program is executing.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: All input to a program is fixed before it starts running. Right rule: With StdIn, the user types values while the program runs, and each value can change the control flow. Only command-line arguments are fixed at launch.
- **Shows at level L0 as:** inconsistent trace: Points to LT (prompt, block for input, test, respond, loop). An uneven trace answers before the guess is read, or reads all the guesses at once. (here mixing in: "All input to a program is fixed before it starts running")

## Errors (0)

An error edge states the rule that gets broken in a program, and the right rule.

The graph has no error edge from this concept.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for interactive input: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to interactive input agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

interactive input -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (3 ways).

- **everyday reading** (folk-meaning rule): Novices read a program as if it already knew all its inputs, e.g. treating AREA = HEIGHT\*WIDTH written before the input as using the typed values. In fact each read happens only when execution reaches it, and the typed value can change what runs next.
- **misconception** (wrong rule / right rule; shows `InputFixedBeforeRun`): wrong rule: All input to a program is fixed before it starts running. Right rule: With StdIn, the user types values while the program runs, and each value can change the control flow. Only command-line arguments are fixed at launch.
- **inconsistent trace** (uneven-application rule; shows `InputFixedBeforeRun`): Points to LT (prompt, block for input, test, respond, loop). An uneven trace answers before the guess is read, or reads all the guesses at once. (here mixing in: "All input to a program is fixed before it starts running")

### L1: Unistructural / atom x text surface

L1 for interactive input: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

interactive input -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

- **names the element** (identity rule): Interactive input is user dialogue through standard I/O: the program prints a prompt, reads the user's reply, and its control flow depends on that reply.
- **states the rule** (declarative rule): A value can be read from standard input at any time during execution, and each read blocks until the user enters input.

### L2: Multistructural / block x execution / preoperational

L2 for interactive input: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

interactive input -&gt; L2 (Multistructural): the answer applies the rules of interactive input to every part of the code, in order (3 ways).

- **line by line trace** (operational sequencing rule): Each round prints the prompt, then readInt() blocks until the user types a number and &lt;return&gt;. The value is compared, a response is printed, and the loop test (m != N) runs again.
- **output prediction** (evaluation / result rule): The terminal shows prompts, typed replies and responses interleaved: What's your guess? 500000 / Too high / What's your guess? 250000 / Too low ... and finally You win!.
- **one step execution** (state-transition rule): One round sets m to the typed value and prints exactly one of You win!, Too low or Too high. N does not change.

### L3: Relational / relations x function (concrete operational begins)

L3 for interactive input: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

interactive input -&gt; L3 (Relational): the answer relates the parts (2 ways).

- **relation to neighbour** (composition rule (with a neighbour)): Because a StdIn read can run at any point, a read placed inside the game loop lets each reply choose the branch taken in that round.
- **purpose of the whole** (plan / role rule): Plan: the prompt-read-respond loop (a guessing game or menu). m is a most-recent holder and N a fixed value. The programmer must plan for every possible user reply.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for interactive input: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

interactive input -&gt; L4 (Extended abstract): the answer reasons beyond the given code (4 ways).

- **predict a change** (conservation rule; shows `InputFixedBeforeRun`): Redirecting a file of replies instead of typing keeps the same control flow, because the program cannot tell the difference. Only the echo of the typed input disappears from the screen.
- **transfer to a new program** (applicability rule): Use interactive input when later questions depend on earlier answers (games, menus, tutoring dialogues). For bulk data use files and redirection; modern applications take user input through a GUI.
- **diagnose an error** (error rule): rule broken: Each reply must be a token of the expected type. Kind: run-time exception. Trigger class: The user types a non-integer (abc, 12.5) at a readInt() prompt: NumberFormatException.
- **diagnose an error** (error rule): rule broken: No reads after the input ends. Kind: run-time exception. Trigger class: The user sends end-of-file (&lt;ctrl-d&gt;) before the loop ends, so the next readInt() fails.

## Same topic

`interactive_input` belongs to the topic **Standard input** (`topic1.5.c`). The topic also contains: `end_of_input`, `input_format`, `input_validation`, `read_loop_idiom`, `sentinel_loop`, `standard_input`, `token_vs_line_input`.

## Rules of the concept (14)

- **folk-meaning rule:** Novices read a program as if it already knew all its inputs, e.g. treating AREA = HEIGHT\*WIDTH written before the input as using the typed values. In fact each read happens only when execution reaches it, and the typed value can change what runs next.
- **wrong rule / right rule:** InputFixedBeforeRun: wrong: All input to a program is fixed before it starts running. \| right: With StdIn, the user types values while the program runs, and each value can change the control flow. Only command-line arguments are fixed at launch.
- **uneven-application rule:** Points to LT (prompt, block for input, test, respond, loop). An uneven trace answers before the guess is read, or reads all the guesses at once.
- **identity rule:** Interactive input is user dialogue through standard I/O: the program prints a prompt, reads the user's reply, and its control flow depends on that reply.
- **declarative rule:** A value can be read from standard input at any time during execution, and each read blocks until the user enters input.
- **operational sequencing rule:** Each round prints the prompt, then readInt() blocks until the user types a number and &lt;return&gt;. The value is compared, a response is printed, and the loop test (m != N) runs again.
- **evaluation / result rule:** The terminal shows prompts, typed replies and responses interleaved: What's your guess? 500000 / Too high / What's your guess? 250000 / Too low ... and finally You win!.
- **state-transition rule:** One round sets m to the typed value and prints exactly one of You win!, Too low or Too high. N does not change.
- **composition rule (with a neighbour):** with standard\_input: Because a StdIn read can run at any point, a read placed inside the game loop lets each reply choose the branch taken in that round.
- **plan / role rule:** Plan: the prompt-read-respond loop (a guessing game or menu). m is a most-recent holder and N a fixed value. The programmer must plan for every possible user reply.
- **conservation rule:** Redirecting a file of replies instead of typing keeps the same control flow, because the program cannot tell the difference. Only the echo of the typed input disappears from the screen.
- **error rule:** rule broken: Each reply must be a token of the expected type. (run-time exception)
- **error rule:** rule broken: No reads after the input ends. (run-time exception)
- **applicability rule:** Use interactive input when later questions depend on earlier answers (games, menus, tutoring dialogues). For bulk data use files and redirection; modern applications take user input through a GUI.

## The whole prerequisite chain

- **Everything it builds on (2):** `standard_input`, `stream_model`
- **Everything that builds on it (0):** nothing
