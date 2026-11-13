# Data-driven code (`data_driven_code`)

keeping data in files and writing programs that read it from standard input, so the data can change without changing the program

Section 1.5 1.5 Input and Output, topic 1.5.d Redirection and piping (filters).

![The knowledge graph around data_driven_code](data_driven_code.png)

## At a glance

- **Needs first:** `redirection`
- **Leads to:** nothing
- **Learned alongside:** nothing
- **Misconceptions:** none
- **Errors:** none
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 10 edges around this concept. The edge logic, the wrong and right rules and the exact rules of the ways are copied word for word from the graph.

## To work on (3)

- no misconception or error edge
- no code pattern or signal: the code cannot tag this concept
- no aliases: a student's words cannot name this concept

## What it needs first (1)

A prerequisite edge means the other concept has to be understood before `data_driven_code`.

### `redirection` comes before `data_driven_code`

*&lt; / &gt; send a file in/out as standard input/output*

- **Edge:** `pre:redirection->data_driven_code`
- **Exact edge logic:** Redirecting a file to standard input lets the same program process different data files without being changed.
- **Grounding:** book\_passage
- **Composition rule (R) of `data_driven_code` with `redirection`:** Redirecting a different data file to standard input changes what the unchanged program processes.
- **Composition rule (R) of `redirection` with `data_driven_code`:** Redirecting different files into the same program changes the data it processes without changing the program.

## What it leads to (0)

These concepts need `data_driven_code` first.

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

L0 for Data-driven code: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to Data-driven code agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

- **Edge:** `data_driven_code` &rarr; `data_driven_code@L0` (has_level)
- **Exact edge logic:** Data-driven code -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (1 way).

Ways (1), each with its exact rule:

- **[0] everyday\_reading** (rule type E, folk-meaning rule): In the everyday sense, a 'program' includes its data, so changing the results means editing the code. In data-driven code the data live in files read from standard input, so they change while the program stays the same.

### L1: Unistructural / atom x text surface

L1 for Data-driven code: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

- **Edge:** `data_driven_code` &rarr; `data_driven_code@L1` (has_level)
- **Exact edge logic:** Data-driven code -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

Ways (2), each with its exact rule:

- **[0] names\_the\_element** (rule type N, identity rule): Data-driven code is a design style: data are kept in files and the program reads them from standard input, so the data can change without changing the program.
- **[1] states\_the\_rule** (rule type S, declarative rule): Keep the data in files and write programs that read from standard input. Then change the data, not the program.

### L2: Multistructural / block x execution / preoperational

L2 for Data-driven code: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

- **Edge:** `data_driven_code` &rarr; `data_driven_code@L2` (has_level)
- **Exact edge logic:** Data-driven code -&gt; L2 (Multistructural): the answer applies the rules of Data-driven code to every part of the code, in order (3 ways).

Ways (3), each with its exact rule:

- **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): The program is launched with \`&lt; file\`. It reads values in file order and interprets them by a format convention (e.g. a header first, then records) until isEmpty().
- **[1] output\_prediction** (rule type OP, evaluation / result rule): The same program with different files gives different outputs. \`java PlayThatTune &lt; elise.txt\` plays Für Elise, and another file plays another tune.
- **[2] one\_step\_execution** (rule type OS, state-transition rule): Each read takes the next value from the data file, where a literal written in the code would otherwise be.

### L3: Relational / relations x function (concrete operational begins)

L3 for Data-driven code: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

- **Edge:** `data_driven_code` &rarr; `data_driven_code@L3` (has_level)
- **Exact edge logic:** Data-driven code -&gt; L3 (Relational): the answer relates the parts (2 ways).

Ways (2), each with its exact rule:

- **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Redirecting a different data file to standard input changes what the unchanged program processes.
- **[1] purpose\_of\_the\_whole** (rule type P, plan / role rule): Data-driven code lets one program serve many data sets (experiments, transactions, web models). It is the norm in data processing.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for Data-driven code: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

- **Edge:** `data_driven_code` &rarr; `data_driven_code@L4` (has_level)
- **Exact edge logic:** Data-driven code -&gt; L4 (Extended abstract): the answer reasons beyond the given code (4 ways).

Ways (4), each with its exact rule:

- **[0] predict\_a\_change** (rule type C, conservation rule): Changing the data file keeps the program and its correctness. Changing the file's format (field order, header) breaks the program's reads.
- **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Use data-driven code when the same computation must run on many or changing data sets. Values that are intrinsic to the algorithm belong in the code, and a few launch parameters go on the command line.
- **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: The data file must follow the program's input format. Kind: run-time exception. Trigger class: A file with a non-numeric token, or fields in the wrong order: NumberFormatException at the read.
- **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: The data file must contain all the values the program reads. Kind: run-time exception. Trigger class: A truncated file (fewer values than a header promises): the read after the end fails.

## Same topic

`data_driven_code` belongs to the topic **Redirection and piping (filters)** (`topic1.5.d`). The topic also contains: `filter`, `piping`, `redirection`.

## Rules of the concept (13)

- **Book** (SW-1e, p. 133 (pdf 143)): "enables us to create data-driven code"
- **Book** (SW-1e, p. 177 (pdf 187)): "Data-driven code is prevalent"
- **E** (folk-meaning rule): In the everyday sense, a 'program' includes its data, so changing the results means editing the code. In data-driven code the data live in files read from standard input, so they change while the program stays the same.
- **T** (uneven-application rule): Points to LT (the program reads the file's values, in the file's order, at run time). An uneven trace uses values from a different file, or hard-coded values, for some reads.
- **N** (identity rule): Data-driven code is a design style: data are kept in files and the program reads them from standard input, so the data can change without changing the program.
- **S** (declarative rule): Keep the data in files and write programs that read from standard input. Then change the data, not the program.
- **LT** (operational sequencing rule): The program is launched with \`&lt; file\`. It reads values in file order and interprets them by a format convention (e.g. a header first, then records) until isEmpty().
- **OP** (evaluation / result rule): The same program with different files gives different outputs. \`java PlayThatTune &lt; elise.txt\` plays Für Elise, and another file plays another tune.
- **OS** (state-transition rule): Each read takes the next value from the data file, where a literal written in the code would otherwise be.
- **R** (composition rule (with a neighbour)): with redirection: Redirecting a different data file to standard input changes what the unchanged program processes.
- **P** (plan / role rule): Data-driven code lets one program serve many data sets (experiments, transactions, web models). It is the norm in data processing.
- **C** (conservation rule): Changing the data file keeps the program and its correctness. Changing the file's format (field order, header) breaks the program's reads.
- **D** (error rule): rule broken: The data file must follow the program's input format. (run-time exception)
- **D** (error rule): rule broken: The data file must contain all the values the program reads. (run-time exception)
- **X** (applicability rule): Use data-driven code when the same computation must run on many or changing data sets. Values that are intrinsic to the algorithm belong in the code, and a few launch parameters go on the command line.

## How it is found in code and answers (reader block)

- **Aliases:** none
- **Code patterns:** none
- **Operator symbols:** none
- **Java types:** none

## The whole prerequisite chain

- **Everything it builds on (7):** `compile`, `program_text`, `redirection`, `run`, `standard_input`, `standard_output`, `stream_model`
- **Everything that builds on it (0):** nothing

## Every edge in this view and its exact edge logic (10)

All the edges drawn in the picture, in the order: prerequisite, parallel, misconception, error, has_level, contains.

**1. `redirection` &rarr; `data_driven_code`** (prerequisite)

- **Exact edge logic:** Redirecting a file to standard input lets the same program process different data files without being changed.
- **Grounding:** book\_passage
- **Composition rule (R) of `redirection` with `data_driven_code`:** Redirecting different files into the same program changes the data it processes without changing the program.
- **Composition rule (R) of `data_driven_code` with `redirection`:** Redirecting a different data file to standard input changes what the unchanged program processes.

**2. `data_driven_code` &rarr; `data_driven_code@L0`** (has_level)

- **Exact edge logic:** Data-driven code -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (1 way).
  - **[0] everyday\_reading** (rule type E, folk-meaning rule): In the everyday sense, a 'program' includes its data, so changing the results means editing the code. In data-driven code the data live in files read from standard input, so they change while the program stays the same.

**3. `data_driven_code` &rarr; `data_driven_code@L1`** (has_level)

- **Exact edge logic:** Data-driven code -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).
  - **[0] names\_the\_element** (rule type N, identity rule): Data-driven code is a design style: data are kept in files and the program reads them from standard input, so the data can change without changing the program.
  - **[1] states\_the\_rule** (rule type S, declarative rule): Keep the data in files and write programs that read from standard input. Then change the data, not the program.

**4. `data_driven_code` &rarr; `data_driven_code@L2`** (has_level)

- **Exact edge logic:** Data-driven code -&gt; L2 (Multistructural): the answer applies the rules of Data-driven code to every part of the code, in order (3 ways).
  - **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): The program is launched with \`&lt; file\`. It reads values in file order and interprets them by a format convention (e.g. a header first, then records) until isEmpty().
  - **[1] output\_prediction** (rule type OP, evaluation / result rule): The same program with different files gives different outputs. \`java PlayThatTune &lt; elise.txt\` plays Für Elise, and another file plays another tune.
  - **[2] one\_step\_execution** (rule type OS, state-transition rule): Each read takes the next value from the data file, where a literal written in the code would otherwise be.

**5. `data_driven_code` &rarr; `data_driven_code@L3`** (has_level)

- **Exact edge logic:** Data-driven code -&gt; L3 (Relational): the answer relates the parts (2 ways).
  - **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Redirecting a different data file to standard input changes what the unchanged program processes.
  - **[1] purpose\_of\_the\_whole** (rule type P, plan / role rule): Data-driven code lets one program serve many data sets (experiments, transactions, web models). It is the norm in data processing.

**6. `data_driven_code` &rarr; `data_driven_code@L4`** (has_level)

- **Exact edge logic:** Data-driven code -&gt; L4 (Extended abstract): the answer reasons beyond the given code (4 ways).
  - **[0] predict\_a\_change** (rule type C, conservation rule): Changing the data file keeps the program and its correctness. Changing the file's format (field order, header) breaks the program's reads.
  - **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Use data-driven code when the same computation must run on many or changing data sets. Values that are intrinsic to the algorithm belong in the code, and a few launch parameters go on the command line.
  - **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: The data file must follow the program's input format. Kind: run-time exception. Trigger class: A file with a non-numeric token, or fields in the wrong order: NumberFormatException at the read.
  - **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: The data file must contain all the values the program reads. Kind: run-time exception. Trigger class: A truncated file (fewer values than a header promises): the read after the end fails.

**7. `topic1.5.d` &rarr; `data_driven_code`** (contains)

- topic `topic1.5.d` contains `data_driven_code`

**8. `topic1.5.d` &rarr; `filter`** (contains)

- topic `topic1.5.d` contains `filter`

**9. `topic1.5.d` &rarr; `piping`** (contains)

- topic `topic1.5.d` contains `piping`

**10. `topic1.5.d` &rarr; `redirection`** (contains)

- topic `topic1.5.d` contains `redirection`
