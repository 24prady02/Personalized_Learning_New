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

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 15 edges around this concept. The edge logic, the wrong and right rules and the exact rules of the ways are copied word for word from the graph.

## To work on (1)

- no aliases: a student's words cannot name this concept

## What it needs first (1)

A prerequisite edge means the other concept has to be understood before `interactive_input`.

### `standard_input` comes before `interactive_input`

*StdIn -- reading a stream of values*

- **Edge:** `pre:standard_input->interactive_input`
- **Exact edge logic:** Standard input can be read at any time while the program runs, so the user can type values that change its control flow during execution.
- **Grounding:** book\_passage
- **Composition rule (R) of `interactive_input` with `standard_input`:** Because a StdIn read can run at any point, a read placed inside the game loop lets each reply choose the branch taken in that round.
- **Composition rule (R) of `standard_input` with `interactive_input`:** Because a read can run at any point in execution, a read inside a loop lets each typed value decide the next branch.

## What it leads to (0)

These concepts need `interactive_input` first.

No concept has this one as a prerequisite.

## Learned alongside (0)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

No parallel edge touches this concept.

## Misconceptions (1)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### InputFixedBeforeRun

- **Edge:** `interactive_input` &rarr; `InputFixedBeforeRun` (misconception)
- **Exact edge logic (the wrong rule):** All input to a program is fixed before it starts running.
- **Twin logic (the right rule):** With interactive input the user can change the control flow while the program is executing.
- **Wrong belief (on the node):** All input to a program is fixed before it starts running.
- **Correct rule (on the node):** With interactive input the user can change the control flow while the program is executing.
- **Provenance:** published
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [1] misconception, exact rule:** wrong rule: All input to a program is fixed before it starts running. Right rule: With StdIn, the user types values while the program runs, and each value can change the control flow. Only command-line arguments are fixed at launch.
- **L0 way [2] inconsistent\_trace, exact rule:** Points to LT (prompt, block for input, test, respond, loop). An uneven trace answers before the guess is read, or reads all the guesses at once. (here mixing in: "All input to a program is fixed before it starts running")

## Errors (0)

An error edge states the rule that gets broken in a program, and the right rule.

The graph has no error edge from this concept.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for interactive input: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to interactive input agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

- **Edge:** `interactive_input` &rarr; `interactive_input@L0` (has_level)
- **Exact edge logic:** interactive input -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (3 ways).

Ways (3), each with its exact rule:

- **[0] everyday\_reading** (rule type E, folk-meaning rule): Novices read a program as if it already knew all its inputs, e.g. treating AREA = HEIGHT\*WIDTH written before the input as using the typed values. In fact each read happens only when execution reaches it, and the typed value can change what runs next.
- **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `InputFixedBeforeRun`: wrong rule: All input to a program is fixed before it starts running. Right rule: With StdIn, the user types values while the program runs, and each value can change the control flow. Only command-line arguments are fixed at launch.
- **[2] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `InputFixedBeforeRun`: Points to LT (prompt, block for input, test, respond, loop). An uneven trace answers before the guess is read, or reads all the guesses at once. (here mixing in: "All input to a program is fixed before it starts running")

### L1: Unistructural / atom x text surface

L1 for interactive input: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

- **Edge:** `interactive_input` &rarr; `interactive_input@L1` (has_level)
- **Exact edge logic:** interactive input -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

Ways (2), each with its exact rule:

- **[0] names\_the\_element** (rule type N, identity rule): Interactive input is user dialogue through standard I/O: the program prints a prompt, reads the user's reply, and its control flow depends on that reply.
- **[1] states\_the\_rule** (rule type S, declarative rule): A value can be read from standard input at any time during execution, and each read blocks until the user enters input.

### L2: Multistructural / block x execution / preoperational

L2 for interactive input: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

- **Edge:** `interactive_input` &rarr; `interactive_input@L2` (has_level)
- **Exact edge logic:** interactive input -&gt; L2 (Multistructural): the answer applies the rules of interactive input to every part of the code, in order (3 ways).

Ways (3), each with its exact rule:

- **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): Each round prints the prompt, then readInt() blocks until the user types a number and &lt;return&gt;. The value is compared, a response is printed, and the loop test (m != N) runs again.
- **[1] output\_prediction** (rule type OP, evaluation / result rule): The terminal shows prompts, typed replies and responses interleaved: What's your guess? 500000 / Too high / What's your guess? 250000 / Too low ... and finally You win!.
- **[2] one\_step\_execution** (rule type OS, state-transition rule): One round sets m to the typed value and prints exactly one of You win!, Too low or Too high. N does not change.

### L3: Relational / relations x function (concrete operational begins)

L3 for interactive input: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

- **Edge:** `interactive_input` &rarr; `interactive_input@L3` (has_level)
- **Exact edge logic:** interactive input -&gt; L3 (Relational): the answer relates the parts (2 ways).

Ways (2), each with its exact rule:

- **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Because a StdIn read can run at any point, a read placed inside the game loop lets each reply choose the branch taken in that round.
- **[1] purpose\_of\_the\_whole** (rule type P, plan / role rule): Plan: the prompt-read-respond loop (a guessing game or menu). m is a most-recent holder and N a fixed value. The programmer must plan for every possible user reply.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for interactive input: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

- **Edge:** `interactive_input` &rarr; `interactive_input@L4` (has_level)
- **Exact edge logic:** interactive input -&gt; L4 (Extended abstract): the answer reasons beyond the given code (4 ways).

Ways (4), each with its exact rule:

- **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `InputFixedBeforeRun`: Redirecting a file of replies instead of typing keeps the same control flow, because the program cannot tell the difference. Only the echo of the typed input disappears from the screen.
- **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Use interactive input when later questions depend on earlier answers (games, menus, tutoring dialogues). For bulk data use files and redirection; modern applications take user input through a GUI.
- **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: Each reply must be a token of the expected type. Kind: run-time exception. Trigger class: The user types a non-integer (abc, 12.5) at a readInt() prompt: NumberFormatException.
- **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: No reads after the input ends. Kind: run-time exception. Trigger class: The user sends end-of-file (&lt;ctrl-d&gt;) before the loop ends, so the next readInt() fails.

## Same topic

`interactive_input` belongs to the topic **Standard input** (`topic1.5.c`). The topic also contains: `end_of_input`, `input_format`, `input_validation`, `read_loop_idiom`, `sentinel_loop`, `standard_input`, `token_vs_line_input`.

## Rules of the concept (14)

- **Book** (SW-1e, p. 128 (pdf 138)): "The fundamental difference between this program and others that we have written is that the user has the ability to change the control flow while the program is executing."
- **Book** (SW-1.5, p. 128 (pdf 138)): "the user has the ability to change the control flow while the program is executing."
- **E** (folk-meaning rule): Novices read a program as if it already knew all its inputs, e.g. treating AREA = HEIGHT\*WIDTH written before the input as using the typed values. In fact each read happens only when execution reaches it, and the typed value can change what runs next.
- **M** (wrong rule / right rule): InputFixedBeforeRun: wrong: All input to a program is fixed before it starts running. \| right: With StdIn, the user types values while the program runs, and each value can change the control flow. Only command-line arguments are fixed at launch.
- **T** (uneven-application rule): Points to LT (prompt, block for input, test, respond, loop). An uneven trace answers before the guess is read, or reads all the guesses at once.
- **N** (identity rule): Interactive input is user dialogue through standard I/O: the program prints a prompt, reads the user's reply, and its control flow depends on that reply.
- **S** (declarative rule): A value can be read from standard input at any time during execution, and each read blocks until the user enters input.
- **LT** (operational sequencing rule): Each round prints the prompt, then readInt() blocks until the user types a number and &lt;return&gt;. The value is compared, a response is printed, and the loop test (m != N) runs again.
- **OP** (evaluation / result rule): The terminal shows prompts, typed replies and responses interleaved: What's your guess? 500000 / Too high / What's your guess? 250000 / Too low ... and finally You win!.
- **OS** (state-transition rule): One round sets m to the typed value and prints exactly one of You win!, Too low or Too high. N does not change.
- **R** (composition rule (with a neighbour)): with standard\_input: Because a StdIn read can run at any point, a read placed inside the game loop lets each reply choose the branch taken in that round.
- **P** (plan / role rule): Plan: the prompt-read-respond loop (a guessing game or menu). m is a most-recent holder and N a fixed value. The programmer must plan for every possible user reply.
- **C** (conservation rule): Redirecting a file of replies instead of typing keeps the same control flow, because the program cannot tell the difference. Only the echo of the typed input disappears from the screen.
- **D** (error rule): rule broken: Each reply must be a token of the expected type. (run-time exception)
- **D** (error rule): rule broken: No reads after the input ends. (run-time exception)
- **X** (applicability rule): Use interactive input when later questions depend on earlier answers (games, menus, tutoring dialogues). For bulk data use files and redirection; modern applications take user input through a GUI.

## How it is found in code and answers (reader block)

- **Aliases:** none
- **Code patterns:** none
- **Operator symbols:** none
- **Java types:** none
- **Signal read\_then\_branch\_in\_loop** (scope program): `\b(?:while|for)\b[\s\S]{0,150}?(?:StdIn\.read\w*|\.next\w*)\s*\([\s\S]{0,150}?\bif\s*\(`

## The whole prerequisite chain

- **Everything it builds on (2):** `standard_input`, `stream_model`
- **Everything that builds on it (0):** nothing

## Every edge in this view and its exact edge logic (15)

All the edges drawn in the picture, in the order: prerequisite, parallel, misconception, error, has_level, contains.

**1. `standard_input` &rarr; `interactive_input`** (prerequisite)

- **Exact edge logic:** Standard input can be read at any time while the program runs, so the user can type values that change its control flow during execution.
- **Grounding:** book\_passage
- **Composition rule (R) of `standard_input` with `interactive_input`:** Because a read can run at any point in execution, a read inside a loop lets each typed value decide the next branch.
- **Composition rule (R) of `interactive_input` with `standard_input`:** Because a StdIn read can run at any point, a read placed inside the game loop lets each reply choose the branch taken in that round.

**2. `interactive_input` &rarr; `InputFixedBeforeRun`** (misconception)

- **Exact edge logic (the wrong rule):** All input to a program is fixed before it starts running.
- **Twin logic (the right rule):** With interactive input the user can change the control flow while the program is executing.
- **Role:** primary

**3. `interactive_input` &rarr; `interactive_input@L0`** (has_level)

- **Exact edge logic:** interactive input -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (3 ways).
  - **[0] everyday\_reading** (rule type E, folk-meaning rule): Novices read a program as if it already knew all its inputs, e.g. treating AREA = HEIGHT\*WIDTH written before the input as using the typed values. In fact each read happens only when execution reaches it, and the typed value can change what runs next.
  - **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `InputFixedBeforeRun`: wrong rule: All input to a program is fixed before it starts running. Right rule: With StdIn, the user types values while the program runs, and each value can change the control flow. Only command-line arguments are fixed at launch.
  - **[2] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `InputFixedBeforeRun`: Points to LT (prompt, block for input, test, respond, loop). An uneven trace answers before the guess is read, or reads all the guesses at once. (here mixing in: "All input to a program is fixed before it starts running")

**4. `interactive_input` &rarr; `interactive_input@L1`** (has_level)

- **Exact edge logic:** interactive input -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).
  - **[0] names\_the\_element** (rule type N, identity rule): Interactive input is user dialogue through standard I/O: the program prints a prompt, reads the user's reply, and its control flow depends on that reply.
  - **[1] states\_the\_rule** (rule type S, declarative rule): A value can be read from standard input at any time during execution, and each read blocks until the user enters input.

**5. `interactive_input` &rarr; `interactive_input@L2`** (has_level)

- **Exact edge logic:** interactive input -&gt; L2 (Multistructural): the answer applies the rules of interactive input to every part of the code, in order (3 ways).
  - **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): Each round prints the prompt, then readInt() blocks until the user types a number and &lt;return&gt;. The value is compared, a response is printed, and the loop test (m != N) runs again.
  - **[1] output\_prediction** (rule type OP, evaluation / result rule): The terminal shows prompts, typed replies and responses interleaved: What's your guess? 500000 / Too high / What's your guess? 250000 / Too low ... and finally You win!.
  - **[2] one\_step\_execution** (rule type OS, state-transition rule): One round sets m to the typed value and prints exactly one of You win!, Too low or Too high. N does not change.

**6. `interactive_input` &rarr; `interactive_input@L3`** (has_level)

- **Exact edge logic:** interactive input -&gt; L3 (Relational): the answer relates the parts (2 ways).
  - **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Because a StdIn read can run at any point, a read placed inside the game loop lets each reply choose the branch taken in that round.
  - **[1] purpose\_of\_the\_whole** (rule type P, plan / role rule): Plan: the prompt-read-respond loop (a guessing game or menu). m is a most-recent holder and N a fixed value. The programmer must plan for every possible user reply.

**7. `interactive_input` &rarr; `interactive_input@L4`** (has_level)

- **Exact edge logic:** interactive input -&gt; L4 (Extended abstract): the answer reasons beyond the given code (4 ways).
  - **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `InputFixedBeforeRun`: Redirecting a file of replies instead of typing keeps the same control flow, because the program cannot tell the difference. Only the echo of the typed input disappears from the screen.
  - **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Use interactive input when later questions depend on earlier answers (games, menus, tutoring dialogues). For bulk data use files and redirection; modern applications take user input through a GUI.
  - **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: Each reply must be a token of the expected type. Kind: run-time exception. Trigger class: The user types a non-integer (abc, 12.5) at a readInt() prompt: NumberFormatException.
  - **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: No reads after the input ends. Kind: run-time exception. Trigger class: The user sends end-of-file (&lt;ctrl-d&gt;) before the loop ends, so the next readInt() fails.

**8. `topic1.5.c` &rarr; `interactive_input`** (contains)

- topic `topic1.5.c` contains `interactive_input`

**9. `topic1.5.c` &rarr; `end_of_input`** (contains)

- topic `topic1.5.c` contains `end_of_input`

**10. `topic1.5.c` &rarr; `input_format`** (contains)

- topic `topic1.5.c` contains `input_format`

**11. `topic1.5.c` &rarr; `input_validation`** (contains)

- topic `topic1.5.c` contains `input_validation`

**12. `topic1.5.c` &rarr; `read_loop_idiom`** (contains)

- topic `topic1.5.c` contains `read_loop_idiom`

**13. `topic1.5.c` &rarr; `sentinel_loop`** (contains)

- topic `topic1.5.c` contains `sentinel_loop`

**14. `topic1.5.c` &rarr; `standard_input`** (contains)

- topic `topic1.5.c` contains `standard_input`

**15. `topic1.5.c` &rarr; `token_vs_line_input`** (contains)

- topic `topic1.5.c` contains `token_vs_line_input`
