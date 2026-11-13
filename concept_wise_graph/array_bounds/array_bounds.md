# array_bounds (`array_bounds`)

valid indices are 0 .. length-1; otherwise throws

Section 1.4 Arrays, topic 1.4.b Memory representation and bounds checking.

![The knowledge graph around array_bounds](array_bounds.png)

## At a glance

- **Needs first:** `indexing`
- **Leads to:** `loop_guard`, `run_time_error`
- **Learned alongside:** nothing
- **Misconceptions:** `OffByOneBound`, `OutOfBoundsElementsAreNull`
- **Errors:** none
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 24 edges around this concept. The edge logic, the wrong and right rules and the exact rules of the ways are copied word for word from the graph.

## To work on (0)

Nothing is missing for this concept.

## What it needs first (1)

A prerequisite edge means the other concept has to be understood before `array_bounds`.

### `indexing` comes before `array_bounds`

*a[i] -- 0-based access*

- **Edge:** `pre:indexing->array_bounds`
- **Exact edge logic:** Valid indexes run from 0 to a.length - 1; any other index throws an exception when it is used.
- **Grounding:** book\_passage
- **Composition rule (R) of `array_bounds` with `indexing`:** Every index value used in a[i] must satisfy 0 &lt;= i &lt;= a.length-1; the last element is a[a.length-1].
- **Composition rule (R) of `indexing` with `array_bounds`:** Every index value is checked against 0 and a.length at run time; any other value throws.

## What it leads to (2)

These concepts need `array_bounds` first.

### `array_bounds` comes before `loop_guard`

*Loop test as a guard: putting the bounds check in the loop condition so the body never makes an out-of-bounds array access*

- **Edge:** `pre:array_bounds->loop_guard`
- **Exact edge logic:** Because an out-of-bounds index stops the program, the while test checks the bounds before the body uses the index.
- **Grounding:** book\_passage
- **Composition rule (R) of `array_bounds` with `loop_guard`:** Because an out-of-bounds index stops the program, the loop test checks the bounds before the body uses the index (e.g. x &gt; 0 &amp;&amp; x &lt; N-1 before a[x-1], a[x+1]).
- **Composition rule (R) of `loop_guard` with `array_bounds`:** Because an out-of-bounds index stops the program, the guard tests the bounds before the body uses the index, and it must cover every neighbour index (x-1, x+1) the body reads.

### `array_bounds` comes before `run_time_error`

*an error raised while the program executes (e.g. ArrayIndexOutOfBounds, NumberFormatException)*

- **Edge:** `pre:array_bounds->run_time_error`
- **Exact edge logic:** An index outside 0 .. length-1 is not caught by the compiler; the access is checked when the program runs and stops it with ArrayIndexOutOfBoundsException.
- **Grounding:** book\_passage

## Learned alongside (0)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

No parallel edge touches this concept.

## Misconceptions (2)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### OffByOneBound

- **Edge:** `array_bounds` &rarr; `OffByOneBound` (misconception)
- **Exact edge logic (the wrong rule):** &lt; vs &lt;= and 0..n vs 0..n-1 are interchangeable
- **Twin logic (the right rule):** for (i = 0; i &lt; n; i++) runs n times with i going up to n - 1; with &lt;= it runs n + 1 times and reaches i = n.
- **Wrong belief (on the node):** &lt; vs &lt;= and 0..n vs 0..n-1 are interchangeable
- **Correct rule (on the node):** for (i = 0; i &lt; n; i++) runs n times with i going up to n - 1; with &lt;= it runs n + 1 times and reaches i = n.
- **Provenance:** published
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [3] misconception, exact rule:** wrong rule: &lt; vs &lt;= and 0..n vs 0..n-1 are interchangeable. Right rule: for (i = 0; i &lt; n; i++) runs n times with i going up to n - 1; with &lt;= it runs n + 1 times and reaches i = n, which is out of bounds for an array of length n.
- **Edge `array_reversal` &rarr; `OffByOneBound`, exact edge logic:** &lt; vs &lt;= and 0..n vs 0..n-1 are interchangeable **Twin logic:** for (i = 0; i &lt; n; i++) runs n times with i going up to n - 1; with &lt;= it runs n + 1 times and reaches i = n. (role: context)
- **Edge `array_traversal` &rarr; `OffByOneBound`, exact edge logic:** &lt; vs &lt;= and 0..n vs 0..n-1 are interchangeable **Twin logic:** for (i = 0; i &lt; n; i++) runs n times with i going up to n - 1; with &lt;= it runs n + 1 times and reaches i = n. (role: context)
- **Edge `boolean_flag_array` &rarr; `OffByOneBound`, exact edge logic:** &lt; vs &lt;= and 0..n vs 0..n-1 are interchangeable **Twin logic:** for (i = 0; i &lt; n; i++) runs n times with i going up to n - 1; with &lt;= it runs n + 1 times and reaches i = n. (role: context)
- **Edge `loop_control` &rarr; `OffByOneBound`, exact edge logic:** i &lt; n and i &lt;= n mean the same, so the loop runs until i equals n and the last pass can use a[n]. **Twin logic:** for (i = 0; i &lt; n; i++) runs n times with i going up to n - 1; with &lt;= it runs n + 1 times and reaches i = n. (role: primary)
- **Edge `off_by_one_error` &rarr; `OffByOneBound`, exact edge logic:** &lt; vs &lt;= and 0..n vs 0..n-1 are interchangeable **Twin logic:** for (i = 0; i &lt; n; i++) runs n times with i going up to n - 1; with &lt;= it runs n + 1 times and reaches i = n. (role: context)
- **Edge `simulation_loop` &rarr; `OffByOneBound`, exact edge logic:** t &lt; T and t &lt;= T give the same number of moves. **Twin logic:** for (t = 0; t &lt; T; t++) makes exactly T moves; with &lt;= it makes T + 1. (role: context)

### OutOfBoundsElementsAreNull

- **Edge:** `array_bounds` &rarr; `OutOfBoundsElementsAreNull` (misconception)
- **Exact edge logic (the wrong rule):** Reading a[a.length] just gives null or 0.
- **Twin logic (the right rule):** Reading any index outside 0 to a.length - 1 throws ArrayIndexOutOfBoundsException.
- **Wrong belief (on the node):** an out-of-bounds read returns null (it throws)
- **Correct rule (on the node):** Reading any index outside 0 to a.length - 1 throws ArrayIndexOutOfBoundsException.
- **Provenance:** published
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [1] misconception, exact rule:** wrong rule: An out-of-bounds read returns null (or 0). Right rule: Reading or writing any index outside 0 to a.length - 1 throws ArrayIndexOutOfBoundsException and returns no value.
- **L0 way [2] inconsistent\_trace, exact rule:** Points to LT: the bounds check runs at every access, at run time. Inconsistent application: the trace accepts an index of a.length on the last pass (or -1 on the first) but rejects it elsewhere, or reads 'some value' there. (here mixing in: "an out-of-bounds read returns null (it throws)")

## Errors (0)

An error edge states the rule that gets broken in a program, and the right rule.

The graph has no error edge from this concept.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for array bounds: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to array bounds agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

- **Edge:** `array_bounds` &rarr; `array_bounds@L0` (has_level)
- **Exact edge logic:** array bounds -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (4 ways).

Ways (4), each with its exact rule:

- **[0] everyday\_reading** (rule type E, folk-meaning rule): Folk meaning: in English, 'items 1 to 10' or 'up to n' includes the end point, and reading past the end of a list just gives 'nothing'. Java rule: the legal indices are 0..length-1, and any other index throws ArrayIndexOutOfBoundsException instead of returning a value.
- **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `OutOfBoundsElementsAreNull`: wrong rule: An out-of-bounds read returns null (or 0). Right rule: Reading or writing any index outside 0 to a.length - 1 throws ArrayIndexOutOfBoundsException and returns no value.
- **[2] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `OutOfBoundsElementsAreNull`: Points to LT: the bounds check runs at every access, at run time. Inconsistent application: the trace accepts an index of a.length on the last pass (or -1 on the first) but rejects it elsewhere, or reads 'some value' there. (here mixing in: "an out-of-bounds read returns null (it throws)")
- **[3] misconception** (rule type M, wrong rule / right rule) &rarr; `OffByOneBound`: wrong rule: &lt; vs &lt;= and 0..n vs 0..n-1 are interchangeable. Right rule: for (i = 0; i &lt; n; i++) runs n times with i going up to n - 1; with &lt;= it runs n + 1 times and reaches i = n, which is out of bounds for an array of length n.

### L1: Unistructural / atom x text surface

L1 for array bounds: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

- **Edge:** `array_bounds` &rarr; `array_bounds@L1` (has_level)
- **Exact edge logic:** array bounds -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

Ways (2), each with its exact rule:

- **[0] names\_the\_element** (rule type N, identity rule): Identity: the bounds of an array are its legal index range, 0 to length-1.
- **[1] states\_the\_rule** (rule type S, declarative rule): Declarative: an index less than 0 or greater than length-1 makes the program terminate with an ArrayIndexOutOfBoundsException; it is the programmer's responsibility to use legal indices.

### L2: Multistructural / block x execution / preoperational

L2 for array bounds: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

- **Edge:** `array_bounds` &rarr; `array_bounds@L2` (has_level)
- **Exact edge logic:** array bounds -&gt; L2 (Multistructural): the answer applies the rules of array bounds to every part of the code, in order (3 ways).

Ways (3), each with its exact rule:

- **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): Sequencing: at each access the index expression is evaluated first and then compared with 0 and a.length. Only if it is in range is the element read or written; otherwise the exception is thrown before any element changes.
- **[1] output\_prediction** (rule type OP, evaluation / result rule): Result: a legal access yields the element. An illegal one yields no value; the program stops with ArrayIndexOutOfBoundsException naming the bad index (old JVMs print ': 10', current ones 'Index 10 out of bounds for length 10').
- **[2] one\_step\_execution** (rule type OS, state-transition rule): State transition: an out-of-bounds write changes no element, because the exception is raised before the store. Control leaves the statement, and main terminates unless the exception is caught.

### L3: Relational / relations x function (concrete operational begins)

L3 for array bounds: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

- **Edge:** `array_bounds` &rarr; `array_bounds@L3` (has_level)
- **Exact edge logic:** array bounds -&gt; L3 (Relational): the answer relates the parts (3 ways).

Ways (3), each with its exact rule:

- **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Every index value used in a[i] must satisfy 0 &lt;= i &lt;= a.length-1; the last element is a[a.length-1].
- **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Because an out-of-bounds index stops the program, the loop test checks the bounds before the body uses the index (e.g. x &gt; 0 &amp;&amp; x &lt; N-1 before a[x-1], a[x+1]).
- **[2] purpose\_of\_the\_whole** (rule type P, plan / role rule): Plan/role: run-time bounds checking makes an indexing mistake a visible error instead of silent memory corruption (buffer overflow).

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for array bounds: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

- **Edge:** `array_bounds` &rarr; `array_bounds@L4` (has_level)
- **Exact edge logic:** array bounds -&gt; L4 (Extended abstract): the answer reasons beyond the given code (4 ways).

Ways (4), each with its exact rule:

- **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `OutOfBoundsElementsAreNull`: Conservation: a loop bounded by i &lt; a.length stays within bounds when the array size changes. Changing &lt; to &lt;= adds one pass that throws, and starting at 1 or ending at a.length-1 silently skips an element.
- **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Applicability: check indices explicitly (or restrict the loop range) whenever an index is computed from data, a random number or a neighbour (i-1, i+1). A plain i &lt; a.length traversal or an enhanced for loop needs no extra check.
- **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: Indices must be in 0..a.length-1. Kind: run-time exception. Trigger class: index &gt;= a.length or &lt; 0: i &lt;= a.length, a[i+1] on the last pass, a[i-1] at i = 0, a[0] on an empty array, or the Sample program run with M &gt; N (ArrayIndexOutOfBoundsException)
- **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: A traversal must reach the last valid index a.length-1. Kind: silent logic error. Trigger class: the loop stops one short (i &lt; a.length-1) or starts at 1, so the last or first element is never processed

## Same topic

`array_bounds` belongs to the topic **Memory representation and bounds checking** (`topic1.4.b`). The topic also contains: `array_aliasing`, `array_copy`, `array_reference`, `loop_guard`, `primitive_vs_reference`, `printing_array_reference`, `program_state`.

## Rules of the concept (16)

- **Book** (SW-1e, p. 91 (pdf 101)): "It is your responsibility to use legal indices when accessing an array element."
- **Book** (SW-1e, p. 89 (pdf 99)): "Note that the last element of an array is always a[a.length-1]."
- **Book** (SW-1.4, p. 91 (pdf 101)): "It is your responsibility to use legal indices when accessing an array element."
- **E** (folk-meaning rule): Folk meaning: in English, 'items 1 to 10' or 'up to n' includes the end point, and reading past the end of a list just gives 'nothing'. Java rule: the legal indices are 0..length-1, and any other index throws ArrayIndexOutOfBoundsException instead of returning a value.
- **M** (wrong rule / right rule): OffByOneBound: wrong: &lt; vs &lt;= and 0..n vs 0..n-1 are interchangeable. \| right: for (i = 0; i &lt; n; i++) runs n times with i going up to n - 1; with &lt;= it runs n + 1 times and reaches i = n, which is out of bounds for an array of length n.
- **M** (wrong rule / right rule): OutOfBoundsElementsAreNull: wrong: An out-of-bounds read returns null (or 0). \| right: Reading or writing any index outside 0 to a.length - 1 throws ArrayIndexOutOfBoundsException and returns no value.
- **T** (uneven-application rule): Points to LT: the bounds check runs at every access, at run time. Inconsistent application: the trace accepts an index of a.length on the last pass (or -1 on the first) but rejects it elsewhere, or reads 'some value' there.
- **N** (identity rule): Identity: the bounds of an array are its legal index range, 0 to length-1.
- **S** (declarative rule): Declarative: an index less than 0 or greater than length-1 makes the program terminate with an ArrayIndexOutOfBoundsException; it is the programmer's responsibility to use legal indices.
- **LT** (operational sequencing rule): Sequencing: at each access the index expression is evaluated first and then compared with 0 and a.length. Only if it is in range is the element read or written; otherwise the exception is thrown before any element changes.
- **OP** (evaluation / result rule): Result: a legal access yields the element. An illegal one yields no value; the program stops with ArrayIndexOutOfBoundsException naming the bad index (old JVMs print ': 10', current ones 'Index 10 out of bounds for length 10').
- **OS** (state-transition rule): State transition: an out-of-bounds write changes no element, because the exception is raised before the store. Control leaves the statement, and main terminates unless the exception is caught.
- **R** (composition rule (with a neighbour)): with indexing: Every index value used in a[i] must satisfy 0 &lt;= i &lt;= a.length-1; the last element is a[a.length-1].
- **R** (composition rule (with a neighbour)): with loop\_guard: Because an out-of-bounds index stops the program, the loop test checks the bounds before the body uses the index (e.g. x &gt; 0 &amp;&amp; x &lt; N-1 before a[x-1], a[x+1]).
- **P** (plan / role rule): Plan/role: run-time bounds checking makes an indexing mistake a visible error instead of silent memory corruption (buffer overflow).
- **C** (conservation rule): Conservation: a loop bounded by i &lt; a.length stays within bounds when the array size changes. Changing &lt; to &lt;= adds one pass that throws, and starting at 1 or ending at a.length-1 silently skips an element.
- **D** (error rule): rule broken: Indices must be in 0..a.length-1. (run-time exception)
- **D** (error rule): rule broken: A traversal must reach the last valid index a.length-1. (silent logic error)
- **X** (applicability rule): Applicability: check indices explicitly (or restrict the loop range) whenever an index is computed from data, a random number or a neighbour (i-1, i+1). A plain i &lt; a.length traversal or an enhanced for loop needs no extra check.

## How it is found in code and answers (reader block)

- **Aliases:** out of bounds, bounds, arrayindexoutofboundsexception
- **Code patterns:** `\[\s*\w+\.length\s*(?:-\s*\d+\s*)?\]`, `<=\s*\w+\.length\b`, `\bargs\s*\[\s*\d+\s*\]`, `\w+\s*<\s*\w+\.length\b`, `<\s*\w+\s*\.\s*length\s*\+\s*1\b`
- **Operator symbols:** none
- **Java types:** none

## The whole prerequisite chain

- **Everything it builds on (6):** `array_creation`, `array_declaration`, `array_initializer`, `data_structure`, `data_type`, `indexing`
- **Everything that builds on it (2):** `loop_guard`, `run_time_error`

## Every edge in this view and its exact edge logic (24)

All the edges drawn in the picture, in the order: prerequisite, parallel, misconception, error, has_level, contains.

**1. `array_bounds` &rarr; `loop_guard`** (prerequisite)

- **Exact edge logic:** Because an out-of-bounds index stops the program, the while test checks the bounds before the body uses the index.
- **Grounding:** book\_passage
- **Composition rule (R) of `array_bounds` with `loop_guard`:** Because an out-of-bounds index stops the program, the loop test checks the bounds before the body uses the index (e.g. x &gt; 0 &amp;&amp; x &lt; N-1 before a[x-1], a[x+1]).
- **Composition rule (R) of `loop_guard` with `array_bounds`:** Because an out-of-bounds index stops the program, the guard tests the bounds before the body uses the index, and it must cover every neighbour index (x-1, x+1) the body reads.

**2. `array_bounds` &rarr; `run_time_error`** (prerequisite)

- **Exact edge logic:** An index outside 0 .. length-1 is not caught by the compiler; the access is checked when the program runs and stops it with ArrayIndexOutOfBoundsException.
- **Grounding:** book\_passage

**3. `indexing` &rarr; `array_bounds`** (prerequisite)

- **Exact edge logic:** Valid indexes run from 0 to a.length - 1; any other index throws an exception when it is used.
- **Grounding:** book\_passage
- **Composition rule (R) of `indexing` with `array_bounds`:** Every index value is checked against 0 and a.length at run time; any other value throws.
- **Composition rule (R) of `array_bounds` with `indexing`:** Every index value used in a[i] must satisfy 0 &lt;= i &lt;= a.length-1; the last element is a[a.length-1].

**4. `array_bounds` &rarr; `OffByOneBound`** (misconception)

- **Exact edge logic (the wrong rule):** &lt; vs &lt;= and 0..n vs 0..n-1 are interchangeable
- **Twin logic (the right rule):** for (i = 0; i &lt; n; i++) runs n times with i going up to n - 1; with &lt;= it runs n + 1 times and reaches i = n.
- **Role:** context

**5. `array_bounds` &rarr; `OutOfBoundsElementsAreNull`** (misconception)

- **Exact edge logic (the wrong rule):** Reading a[a.length] just gives null or 0.
- **Twin logic (the right rule):** Reading any index outside 0 to a.length - 1 throws ArrayIndexOutOfBoundsException.
- **Role:** primary

**6. `array_reversal` &rarr; `OffByOneBound`** (misconception)

- **Exact edge logic (the wrong rule):** &lt; vs &lt;= and 0..n vs 0..n-1 are interchangeable
- **Twin logic (the right rule):** for (i = 0; i &lt; n; i++) runs n times with i going up to n - 1; with &lt;= it runs n + 1 times and reaches i = n.
- **Role:** context

**7. `array_traversal` &rarr; `OffByOneBound`** (misconception)

- **Exact edge logic (the wrong rule):** &lt; vs &lt;= and 0..n vs 0..n-1 are interchangeable
- **Twin logic (the right rule):** for (i = 0; i &lt; n; i++) runs n times with i going up to n - 1; with &lt;= it runs n + 1 times and reaches i = n.
- **Role:** context

**8. `boolean_flag_array` &rarr; `OffByOneBound`** (misconception)

- **Exact edge logic (the wrong rule):** &lt; vs &lt;= and 0..n vs 0..n-1 are interchangeable
- **Twin logic (the right rule):** for (i = 0; i &lt; n; i++) runs n times with i going up to n - 1; with &lt;= it runs n + 1 times and reaches i = n.
- **Role:** context

**9. `loop_control` &rarr; `OffByOneBound`** (misconception)

- **Exact edge logic (the wrong rule):** i &lt; n and i &lt;= n mean the same, so the loop runs until i equals n and the last pass can use a[n].
- **Twin logic (the right rule):** for (i = 0; i &lt; n; i++) runs n times with i going up to n - 1; with &lt;= it runs n + 1 times and reaches i = n.
- **Role:** primary

**10. `off_by_one_error` &rarr; `OffByOneBound`** (misconception)

- **Exact edge logic (the wrong rule):** &lt; vs &lt;= and 0..n vs 0..n-1 are interchangeable
- **Twin logic (the right rule):** for (i = 0; i &lt; n; i++) runs n times with i going up to n - 1; with &lt;= it runs n + 1 times and reaches i = n.
- **Role:** context

**11. `simulation_loop` &rarr; `OffByOneBound`** (misconception)

- **Exact edge logic (the wrong rule):** t &lt; T and t &lt;= T give the same number of moves.
- **Twin logic (the right rule):** for (t = 0; t &lt; T; t++) makes exactly T moves; with &lt;= it makes T + 1.
- **Role:** context

**12. `array_bounds` &rarr; `array_bounds@L0`** (has_level)

- **Exact edge logic:** array bounds -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (4 ways).
  - **[0] everyday\_reading** (rule type E, folk-meaning rule): Folk meaning: in English, 'items 1 to 10' or 'up to n' includes the end point, and reading past the end of a list just gives 'nothing'. Java rule: the legal indices are 0..length-1, and any other index throws ArrayIndexOutOfBoundsException instead of returning a value.
  - **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `OutOfBoundsElementsAreNull`: wrong rule: An out-of-bounds read returns null (or 0). Right rule: Reading or writing any index outside 0 to a.length - 1 throws ArrayIndexOutOfBoundsException and returns no value.
  - **[2] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `OutOfBoundsElementsAreNull`: Points to LT: the bounds check runs at every access, at run time. Inconsistent application: the trace accepts an index of a.length on the last pass (or -1 on the first) but rejects it elsewhere, or reads 'some value' there. (here mixing in: "an out-of-bounds read returns null (it throws)")
  - **[3] misconception** (rule type M, wrong rule / right rule) &rarr; `OffByOneBound`: wrong rule: &lt; vs &lt;= and 0..n vs 0..n-1 are interchangeable. Right rule: for (i = 0; i &lt; n; i++) runs n times with i going up to n - 1; with &lt;= it runs n + 1 times and reaches i = n, which is out of bounds for an array of length n.

**13. `array_bounds` &rarr; `array_bounds@L1`** (has_level)

- **Exact edge logic:** array bounds -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).
  - **[0] names\_the\_element** (rule type N, identity rule): Identity: the bounds of an array are its legal index range, 0 to length-1.
  - **[1] states\_the\_rule** (rule type S, declarative rule): Declarative: an index less than 0 or greater than length-1 makes the program terminate with an ArrayIndexOutOfBoundsException; it is the programmer's responsibility to use legal indices.

**14. `array_bounds` &rarr; `array_bounds@L2`** (has_level)

- **Exact edge logic:** array bounds -&gt; L2 (Multistructural): the answer applies the rules of array bounds to every part of the code, in order (3 ways).
  - **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): Sequencing: at each access the index expression is evaluated first and then compared with 0 and a.length. Only if it is in range is the element read or written; otherwise the exception is thrown before any element changes.
  - **[1] output\_prediction** (rule type OP, evaluation / result rule): Result: a legal access yields the element. An illegal one yields no value; the program stops with ArrayIndexOutOfBoundsException naming the bad index (old JVMs print ': 10', current ones 'Index 10 out of bounds for length 10').
  - **[2] one\_step\_execution** (rule type OS, state-transition rule): State transition: an out-of-bounds write changes no element, because the exception is raised before the store. Control leaves the statement, and main terminates unless the exception is caught.

**15. `array_bounds` &rarr; `array_bounds@L3`** (has_level)

- **Exact edge logic:** array bounds -&gt; L3 (Relational): the answer relates the parts (3 ways).
  - **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Every index value used in a[i] must satisfy 0 &lt;= i &lt;= a.length-1; the last element is a[a.length-1].
  - **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Because an out-of-bounds index stops the program, the loop test checks the bounds before the body uses the index (e.g. x &gt; 0 &amp;&amp; x &lt; N-1 before a[x-1], a[x+1]).
  - **[2] purpose\_of\_the\_whole** (rule type P, plan / role rule): Plan/role: run-time bounds checking makes an indexing mistake a visible error instead of silent memory corruption (buffer overflow).

**16. `array_bounds` &rarr; `array_bounds@L4`** (has_level)

- **Exact edge logic:** array bounds -&gt; L4 (Extended abstract): the answer reasons beyond the given code (4 ways).
  - **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `OutOfBoundsElementsAreNull`: Conservation: a loop bounded by i &lt; a.length stays within bounds when the array size changes. Changing &lt; to &lt;= adds one pass that throws, and starting at 1 or ending at a.length-1 silently skips an element.
  - **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Applicability: check indices explicitly (or restrict the loop range) whenever an index is computed from data, a random number or a neighbour (i-1, i+1). A plain i &lt; a.length traversal or an enhanced for loop needs no extra check.
  - **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: Indices must be in 0..a.length-1. Kind: run-time exception. Trigger class: index &gt;= a.length or &lt; 0: i &lt;= a.length, a[i+1] on the last pass, a[i-1] at i = 0, a[0] on an empty array, or the Sample program run with M &gt; N (ArrayIndexOutOfBoundsException)
  - **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: A traversal must reach the last valid index a.length-1. Kind: silent logic error. Trigger class: the loop stops one short (i &lt; a.length-1) or starts at 1, so the last or first element is never processed

**17. `topic1.4.b` &rarr; `array_bounds`** (contains)

- topic `topic1.4.b` contains `array_bounds`

**18. `topic1.4.b` &rarr; `array_aliasing`** (contains)

- topic `topic1.4.b` contains `array_aliasing`

**19. `topic1.4.b` &rarr; `array_copy`** (contains)

- topic `topic1.4.b` contains `array_copy`

**20. `topic1.4.b` &rarr; `array_reference`** (contains)

- topic `topic1.4.b` contains `array_reference`

**21. `topic1.4.b` &rarr; `loop_guard`** (contains)

- topic `topic1.4.b` contains `loop_guard`

**22. `topic1.4.b` &rarr; `primitive_vs_reference`** (contains)

- topic `topic1.4.b` contains `primitive_vs_reference`

**23. `topic1.4.b` &rarr; `printing_array_reference`** (contains)

- topic `topic1.4.b` contains `printing_array_reference`

**24. `topic1.4.b` &rarr; `program_state`** (contains)

- topic `topic1.4.b` contains `program_state`
