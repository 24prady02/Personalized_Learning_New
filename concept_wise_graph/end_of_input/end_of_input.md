# end_of_input (`end_of_input`)

StdIn.isEmpty() and the end-of-file keystroke

Section 1.5 Input and Output, topic 1.5.c Standard input.

![The knowledge graph around end_of_input](end_of_input.png)

## At a glance

- **Needs first:** `read_loop_idiom`
- **Leads to:** nothing
- **Learned alongside:** nothing
- **Misconceptions:** `IsEmptyMeansBlankLine`
- **Errors:** `ReadPastEndOfInput`
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 18 edges around this concept. The edge logic, the wrong and right rules and the exact rules of the ways are copied word for word from the graph.

## To work on (1)

- no aliases: a student's words cannot name this concept

## What it needs first (1)

A prerequisite edge means the other concept has to be understood before `end_of_input`.

### `read_loop_idiom` comes before `end_of_input`

*reading until end-of-input*

- **Edge:** `pre:read_loop_idiom->end_of_input`
- **Exact edge logic:** The read loop runs until StdIn.isEmpty() returns true, which happens when the user types the end-of-file sequence (&lt;ctrl-d&gt;).
- **Grounding:** book\_passage
- **Composition rule (R) of `end_of_input` with `read_loop_idiom`:** isEmpty() is the condition of the read loop, so the loop ends exactly when end-of-file is reached (&lt;ctrl-d&gt; at the keyboard, end of file with &lt;).
- **Composition rule (R) of `read_loop_idiom` with `end_of_input`:** The loop ends only when isEmpty() becomes true: at the end of a redirected file, or after the end-of-file keystroke (&lt;ctrl-d&gt;, or &lt;ctrl-z&gt; on some systems).

## What it leads to (0)

These concepts need `end_of_input` first.

No concept has this one as a prerequisite.

## Learned alongside (0)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

No parallel edge touches this concept.

## Misconceptions (1)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### IsEmptyMeansBlankLine

- **Edge:** `end_of_input` &rarr; `IsEmptyMeansBlankLine` (misconception)
- **Exact edge logic (the wrong rule):** StdIn.isEmpty() becomes true when the user presses Enter on an empty line.
- **Twin logic (the right rule):** isEmpty() is true only when no more values remain: at the end of a redirected file, or after the end-of-file sequence (&lt;ctrl-d&gt;, or &lt;ctrl-z&gt; on some systems, on a line by itself) is typed; an empty line is just whitespace.
- **Wrong belief (on the node):** StdIn.isEmpty() becomes true when the user presses Enter on an empty line.
- **Correct rule (on the node):** isEmpty() is true only when no more values remain: at the end of a redirected file, or after the end-of-file sequence (&lt;ctrl-d&gt;, or &lt;ctrl-z&gt; on some systems, on a line by itself) is typed; an empty line is just whitespace.
- **Provenance:** derived
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [1] misconception, exact rule:** wrong rule: StdIn.isEmpty() becomes true when the user presses Enter on an empty line. Right rule: isEmpty() is true only when no tokens remain: at the end of a redirected file, or after the end-of-file sequence (&lt;ctrl-d&gt;, or &lt;ctrl-z&gt; on some systems, on a line by itself). An empty line is just whitespace.
- **L0 way [2] inconsistent\_trace, exact rule:** Points to LT (isEmpty() waits until it can decide; it returns true only after end-of-file). An uneven trace ends the loop at a blank line on some passes, or counts the end-of-file keystroke as a value. (here mixing in: "StdIn.isEmpty() becomes true when the user presses Enter on an empty line")

## Errors (1)

An error edge states the rule that gets broken in a program, and the right rule.

### ReadPastEndOfInput

- **Edge:** `end_of_input` &rarr; `ReadPastEndOfInput` (error)
- **Exact edge logic (the wrong rule):** Calls StdIn.readInt() again after the input has run out.
- **Twin logic (the right rule):** Reading after standard input is exhausted is a run-time error; test StdIn.isEmpty() before each read.
- **Wrong belief (on the node):** Calls StdIn.readInt() again after the input has run out.
- **Correct rule (on the node):** Reading after standard input is exhausted is a run-time error; test StdIn.isEmpty() before each read.
- **Provenance:** textbook
- **Role of this concept:** primary
- **Edge `read_loop_idiom` &rarr; `ReadPastEndOfInput`, exact edge logic:** Calls StdIn.readInt() again after the input has run out. **Twin logic:** Reading after standard input is exhausted is a run-time error; test StdIn.isEmpty() before each read. (role: context)
- **Edge `standard_input` &rarr; `ReadPastEndOfInput`, exact edge logic:** Calls StdIn.readInt() again after the input has run out. **Twin logic:** Reading after standard input is exhausted is a run-time error; test StdIn.isEmpty() before each read. (role: context)

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for end of input: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to end of input agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

- **Edge:** `end_of_input` &rarr; `end_of_input@L0` (has_level)
- **Exact edge logic:** end of input -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (3 ways).

Ways (3), each with its exact rule:

- **[0] everyday\_reading** (rule type E, folk-meaning rule): Everyday 'empty' and 'done' suggest that a blank line, or pressing Enter, ends the input. For StdIn, a blank line is only whitespace: input ends only when the end-of-file signal arrives.
- **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `IsEmptyMeansBlankLine`: wrong rule: StdIn.isEmpty() becomes true when the user presses Enter on an empty line. Right rule: isEmpty() is true only when no tokens remain: at the end of a redirected file, or after the end-of-file sequence (&lt;ctrl-d&gt;, or &lt;ctrl-z&gt; on some systems, on a line by itself). An empty line is just whitespace.
- **[2] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `IsEmptyMeansBlankLine`: Points to LT (isEmpty() waits until it can decide; it returns true only after end-of-file). An uneven trace ends the loop at a blank line on some passes, or counts the end-of-file keystroke as a value. (here mixing in: "StdIn.isEmpty() becomes true when the user presses Enter on an empty line")

### L1: Unistructural / atom x text surface

L1 for end of input: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

- **Edge:** `end_of_input` &rarr; `end_of_input@L1` (has_level)
- **Exact edge logic:** end of input -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

Ways (2), each with its exact rule:

- **[0] names\_the\_element** (rule type N, identity rule): End of input is the end-of-file condition of the input stream. Typing the end-of-file sequence or reaching the end of a redirected file signals it, and StdIn.isEmpty() tests it.
- **[1] states\_the\_rule** (rule type S, declarative rule): isEmpty() returns true if standard input has no more values (only whitespace may be left). At a terminal the book signals the end with &lt;ctrl-d&gt;; the other widely used convention is &lt;ctrl-z&gt;.

### L2: Multistructural / block x execution / preoperational

L2 for end of input: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

- **Edge:** `end_of_input` &rarr; `end_of_input@L2` (has_level)
- **Exact edge logic:** end of input -&gt; L2 (Multistructural): the answer applies the rules of end of input to every part of the code, in order (3 ways).

Ways (3), each with its exact rule:

- **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): When isEmpty() is called at a terminal, it blocks until a token arrives (it returns false) or the end-of-file sequence is typed (it returns true). With a redirected file, it returns true right after the last token.
- **[1] output\_prediction** (rule type OP, evaluation / result rule): isEmpty() returns a boolean: true if there are no more values, false otherwise.
- **[2] one\_step\_execution** (rule type OS, state-transition rule): isEmpty() consumes no value (at most it skips whitespace) and returns a boolean. Only the read that follows advances past a token.

### L3: Relational / relations x function (concrete operational begins)

L3 for end of input: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

- **Edge:** `end_of_input` &rarr; `end_of_input@L3` (has_level)
- **Exact edge logic:** end of input -&gt; L3 (Relational): the answer relates the parts (2 ways).

Ways (2), each with its exact rule:

- **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): isEmpty() is the condition of the read loop, so the loop ends exactly when end-of-file is reached (&lt;ctrl-d&gt; at the keyboard, end of file with &lt;).
- **[1] purpose\_of\_the\_whole** (rule type P, plan / role rule): Role: the termination signal of a process-until-done loop, used when the amount of data is unknown.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for end of input: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

- **Edge:** `end_of_input` &rarr; `end_of_input@L4` (has_level)
- **Exact edge logic:** end of input -&gt; L4 (Extended abstract): the answer reasons beyond the given code (4 ways).

Ways (4), each with its exact rule:

- **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `IsEmptyMeansBlankLine`: Adding blank lines or trailing spaces at the end of the input keeps isEmpty()'s answer (still true at the end). Adding any token changes it.
- **[1] diagnose\_an\_error** (rule type D, error rule): rule broken: Reading after the stream is exhausted is an error. Test isEmpty() first. Kind: run-time exception. Trigger class: Any read after the end-of-file signal or after the last token of the file.
- **[2] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Ending on end-of-file is right when data come from a file or a pipe, or the count is unknown. For human typists a count or a sentinel can be clearer, because the end-of-file key differs between systems.
- **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: The end must be signalled with the system's end-of-file key. Kind: silent logic error. Trigger class: At a terminal the user presses Enter, or uses the other system's key, so isEmpty() keeps waiting and the program seems to hang.

## Same topic

`end_of_input` belongs to the topic **Standard input** (`topic1.5.c`). The topic also contains: `input_format`, `input_validation`, `interactive_input`, `read_loop_idiom`, `sentinel_loop`, `standard_input`, `token_vs_line_input`.

## Rules of the concept (14)

- **Book** (SW-1e, p. 131 (pdf 141)): "How do we signal that we have no more data to type?"
- **Book** (SW-1.5, ): "[ use Ctrl-d (OS X or Dr. Java) or Ctrl-z (Windows) for EOF ]"
- **E** (folk-meaning rule): Everyday 'empty' and 'done' suggest that a blank line, or pressing Enter, ends the input. For StdIn, a blank line is only whitespace: input ends only when the end-of-file signal arrives.
- **M** (wrong rule / right rule): IsEmptyMeansBlankLine: wrong: StdIn.isEmpty() becomes true when the user presses Enter on an empty line. \| right: isEmpty() is true only when no tokens remain: at the end of a redirected file, or after the end-of-file sequence (&lt;ctrl-d&gt;, or &lt;ctrl-z&gt; on some systems, on a line by itself). An empty line is just whitespace.
- **T** (uneven-application rule): Points to LT (isEmpty() waits until it can decide; it returns true only after end-of-file). An uneven trace ends the loop at a blank line on some passes, or counts the end-of-file keystroke as a value.
- **N** (identity rule): End of input is the end-of-file condition of the input stream. Typing the end-of-file sequence or reaching the end of a redirected file signals it, and StdIn.isEmpty() tests it.
- **S** (declarative rule): isEmpty() returns true if standard input has no more values (only whitespace may be left). At a terminal the book signals the end with &lt;ctrl-d&gt;; the other widely used convention is &lt;ctrl-z&gt;.
- **LT** (operational sequencing rule): When isEmpty() is called at a terminal, it blocks until a token arrives (it returns false) or the end-of-file sequence is typed (it returns true). With a redirected file, it returns true right after the last token.
- **OP** (evaluation / result rule): isEmpty() returns a boolean: true if there are no more values, false otherwise.
- **OS** (state-transition rule): isEmpty() consumes no value (at most it skips whitespace) and returns a boolean. Only the read that follows advances past a token.
- **R** (composition rule (with a neighbour)): with read\_loop\_idiom: isEmpty() is the condition of the read loop, so the loop ends exactly when end-of-file is reached (&lt;ctrl-d&gt; at the keyboard, end of file with &lt;).
- **P** (plan / role rule): Role: the termination signal of a process-until-done loop, used when the amount of data is unknown.
- **C** (conservation rule): Adding blank lines or trailing spaces at the end of the input keeps isEmpty()'s answer (still true at the end). Adding any token changes it.
- **D** (error rule): rule broken: Reading after the stream is exhausted is an error. Test isEmpty() first. (run-time exception)
- **D** (error rule): rule broken: The end must be signalled with the system's end-of-file key. (silent logic error)
- **X** (applicability rule): Ending on end-of-file is right when data come from a file or a pipe, or the count is unknown. For human typists a count or a sentinel can be clearer, because the end-of-file key differs between systems.

## How it is found in code and answers (reader block)

- **Aliases:** none
- **Code patterns:** `StdIn\.isEmpty\s*\(`, `\.hasNext\w*\s*\(`
- **Operator symbols:** none
- **Java types:** none

## The whole prerequisite chain

- **Everything it builds on (3):** `read_loop_idiom`, `standard_input`, `stream_model`
- **Everything that builds on it (0):** nothing

## Every edge in this view and its exact edge logic (18)

All the edges drawn in the picture, in the order: prerequisite, parallel, misconception, error, has_level, contains.

**1. `read_loop_idiom` &rarr; `end_of_input`** (prerequisite)

- **Exact edge logic:** The read loop runs until StdIn.isEmpty() returns true, which happens when the user types the end-of-file sequence (&lt;ctrl-d&gt;).
- **Grounding:** book\_passage
- **Composition rule (R) of `read_loop_idiom` with `end_of_input`:** The loop ends only when isEmpty() becomes true: at the end of a redirected file, or after the end-of-file keystroke (&lt;ctrl-d&gt;, or &lt;ctrl-z&gt; on some systems).
- **Composition rule (R) of `end_of_input` with `read_loop_idiom`:** isEmpty() is the condition of the read loop, so the loop ends exactly when end-of-file is reached (&lt;ctrl-d&gt; at the keyboard, end of file with &lt;).

**2. `end_of_input` &rarr; `IsEmptyMeansBlankLine`** (misconception)

- **Exact edge logic (the wrong rule):** StdIn.isEmpty() becomes true when the user presses Enter on an empty line.
- **Twin logic (the right rule):** isEmpty() is true only when no more values remain: at the end of a redirected file, or after the end-of-file sequence (&lt;ctrl-d&gt;, or &lt;ctrl-z&gt; on some systems, on a line by itself) is typed; an empty line is just whitespace.
- **Role:** primary

**3. `end_of_input` &rarr; `ReadPastEndOfInput`** (error)

- **Exact edge logic (the wrong rule):** Calls StdIn.readInt() again after the input has run out.
- **Twin logic (the right rule):** Reading after standard input is exhausted is a run-time error; test StdIn.isEmpty() before each read.
- **Role:** primary

**4. `read_loop_idiom` &rarr; `ReadPastEndOfInput`** (error)

- **Exact edge logic (the wrong rule):** Calls StdIn.readInt() again after the input has run out.
- **Twin logic (the right rule):** Reading after standard input is exhausted is a run-time error; test StdIn.isEmpty() before each read.
- **Role:** context

**5. `standard_input` &rarr; `ReadPastEndOfInput`** (error)

- **Exact edge logic (the wrong rule):** Calls StdIn.readInt() again after the input has run out.
- **Twin logic (the right rule):** Reading after standard input is exhausted is a run-time error; test StdIn.isEmpty() before each read.
- **Role:** context

**6. `end_of_input` &rarr; `end_of_input@L0`** (has_level)

- **Exact edge logic:** end of input -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (3 ways).
  - **[0] everyday\_reading** (rule type E, folk-meaning rule): Everyday 'empty' and 'done' suggest that a blank line, or pressing Enter, ends the input. For StdIn, a blank line is only whitespace: input ends only when the end-of-file signal arrives.
  - **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `IsEmptyMeansBlankLine`: wrong rule: StdIn.isEmpty() becomes true when the user presses Enter on an empty line. Right rule: isEmpty() is true only when no tokens remain: at the end of a redirected file, or after the end-of-file sequence (&lt;ctrl-d&gt;, or &lt;ctrl-z&gt; on some systems, on a line by itself). An empty line is just whitespace.
  - **[2] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `IsEmptyMeansBlankLine`: Points to LT (isEmpty() waits until it can decide; it returns true only after end-of-file). An uneven trace ends the loop at a blank line on some passes, or counts the end-of-file keystroke as a value. (here mixing in: "StdIn.isEmpty() becomes true when the user presses Enter on an empty line")

**7. `end_of_input` &rarr; `end_of_input@L1`** (has_level)

- **Exact edge logic:** end of input -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).
  - **[0] names\_the\_element** (rule type N, identity rule): End of input is the end-of-file condition of the input stream. Typing the end-of-file sequence or reaching the end of a redirected file signals it, and StdIn.isEmpty() tests it.
  - **[1] states\_the\_rule** (rule type S, declarative rule): isEmpty() returns true if standard input has no more values (only whitespace may be left). At a terminal the book signals the end with &lt;ctrl-d&gt;; the other widely used convention is &lt;ctrl-z&gt;.

**8. `end_of_input` &rarr; `end_of_input@L2`** (has_level)

- **Exact edge logic:** end of input -&gt; L2 (Multistructural): the answer applies the rules of end of input to every part of the code, in order (3 ways).
  - **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): When isEmpty() is called at a terminal, it blocks until a token arrives (it returns false) or the end-of-file sequence is typed (it returns true). With a redirected file, it returns true right after the last token.
  - **[1] output\_prediction** (rule type OP, evaluation / result rule): isEmpty() returns a boolean: true if there are no more values, false otherwise.
  - **[2] one\_step\_execution** (rule type OS, state-transition rule): isEmpty() consumes no value (at most it skips whitespace) and returns a boolean. Only the read that follows advances past a token.

**9. `end_of_input` &rarr; `end_of_input@L3`** (has_level)

- **Exact edge logic:** end of input -&gt; L3 (Relational): the answer relates the parts (2 ways).
  - **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): isEmpty() is the condition of the read loop, so the loop ends exactly when end-of-file is reached (&lt;ctrl-d&gt; at the keyboard, end of file with &lt;).
  - **[1] purpose\_of\_the\_whole** (rule type P, plan / role rule): Role: the termination signal of a process-until-done loop, used when the amount of data is unknown.

**10. `end_of_input` &rarr; `end_of_input@L4`** (has_level)

- **Exact edge logic:** end of input -&gt; L4 (Extended abstract): the answer reasons beyond the given code (4 ways).
  - **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `IsEmptyMeansBlankLine`: Adding blank lines or trailing spaces at the end of the input keeps isEmpty()'s answer (still true at the end). Adding any token changes it.
  - **[1] diagnose\_an\_error** (rule type D, error rule): rule broken: Reading after the stream is exhausted is an error. Test isEmpty() first. Kind: run-time exception. Trigger class: Any read after the end-of-file signal or after the last token of the file.
  - **[2] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Ending on end-of-file is right when data come from a file or a pipe, or the count is unknown. For human typists a count or a sentinel can be clearer, because the end-of-file key differs between systems.
  - **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: The end must be signalled with the system's end-of-file key. Kind: silent logic error. Trigger class: At a terminal the user presses Enter, or uses the other system's key, so isEmpty() keeps waiting and the program seems to hang.

**11. `topic1.5.c` &rarr; `end_of_input`** (contains)

- topic `topic1.5.c` contains `end_of_input`

**12. `topic1.5.c` &rarr; `input_format`** (contains)

- topic `topic1.5.c` contains `input_format`

**13. `topic1.5.c` &rarr; `input_validation`** (contains)

- topic `topic1.5.c` contains `input_validation`

**14. `topic1.5.c` &rarr; `interactive_input`** (contains)

- topic `topic1.5.c` contains `interactive_input`

**15. `topic1.5.c` &rarr; `read_loop_idiom`** (contains)

- topic `topic1.5.c` contains `read_loop_idiom`

**16. `topic1.5.c` &rarr; `sentinel_loop`** (contains)

- topic `topic1.5.c` contains `sentinel_loop`

**17. `topic1.5.c` &rarr; `standard_input`** (contains)

- topic `topic1.5.c` contains `standard_input`

**18. `topic1.5.c` &rarr; `token_vs_line_input`** (contains)

- topic `topic1.5.c` contains `token_vs_line_input`
