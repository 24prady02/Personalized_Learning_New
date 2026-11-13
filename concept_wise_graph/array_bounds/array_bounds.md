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

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 24 edges around this concept, each explained in the graph's own words.

## What it needs first (1)

A prerequisite edge means the other concept has to be understood before `array_bounds`.

### `indexing` comes before `array_bounds`

*a[i] -- 0-based access*

Valid indexes run from 0 to a.length - 1; any other index throws an exception when it is used.

- **Grounding:** book passage
- **How `array_bounds` combines with `indexing`:** Every index value used in a[i] must satisfy 0 &lt;= i &lt;= a.length-1; the last element is a[a.length-1].
- **How `indexing` combines with `array_bounds`:** Every index value is checked against 0 and a.length at run time; any other value throws.

## What it leads to (2)

These concepts need `array_bounds` first.

### `array_bounds` comes before `loop_guard`

*Loop test as a guard: putting the bounds check in the loop condition so the body never makes an out-of-bounds array access*

Because an out-of-bounds index stops the program, the while test checks the bounds before the body uses the index.

- **Grounding:** book passage
- **How `array_bounds` combines with `loop_guard`:** Because an out-of-bounds index stops the program, the loop test checks the bounds before the body uses the index (e.g. x &gt; 0 &amp;&amp; x &lt; N-1 before a[x-1], a[x+1]).
- **How `loop_guard` combines with `array_bounds`:** Because an out-of-bounds index stops the program, the guard tests the bounds before the body uses the index, and it must cover every neighbour index (x-1, x+1) the body reads.

### `array_bounds` comes before `run_time_error`

*an error raised while the program executes (e.g. ArrayIndexOutOfBounds, NumberFormatException)*

An index outside 0 .. length-1 is not caught by the compiler; the access is checked when the program runs and stops it with ArrayIndexOutOfBoundsException.

- **Grounding:** book passage

## Learned alongside (0)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

No parallel edge touches this concept.

## Misconceptions (2)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### OffByOneBound

- **Wrong rule:** &lt; vs &lt;= and 0..n vs 0..n-1 are interchangeable
- **Right rule:** for (i = 0; i &lt; n; i++) runs n times with i going up to n - 1; with &lt;= it runs n + 1 times and reaches i = n.
- **Role of this concept:** context
- **Shows at level L0 as:** misconception: wrong rule: &lt; vs &lt;= and 0..n vs 0..n-1 are interchangeable. Right rule: for (i = 0; i &lt; n; i++) runs n times with i going up to n - 1; with &lt;= it runs n + 1 times and reaches i = n, which is out of bounds for an array of length n.
- **Also an edge from `array_reversal`:** &lt; vs &lt;= and 0..n vs 0..n-1 are interchangeable
- **Also an edge from `array_traversal`:** &lt; vs &lt;= and 0..n vs 0..n-1 are interchangeable
- **Also an edge from `boolean_flag_array`:** &lt; vs &lt;= and 0..n vs 0..n-1 are interchangeable
- **Also an edge from `loop_control`:** i &lt; n and i &lt;= n mean the same, so the loop runs until i equals n and the last pass can use a[n].
- **Also an edge from `off_by_one_error`:** &lt; vs &lt;= and 0..n vs 0..n-1 are interchangeable
- **Also an edge from `simulation_loop`:** t &lt; T and t &lt;= T give the same number of moves.

### OutOfBoundsElementsAreNull

- **Wrong rule:** Reading a[a.length] just gives null or 0.
- **Right rule:** Reading any index outside 0 to a.length - 1 throws ArrayIndexOutOfBoundsException.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: An out-of-bounds read returns null (or 0). Right rule: Reading or writing any index outside 0 to a.length - 1 throws ArrayIndexOutOfBoundsException and returns no value.
- **Shows at level L0 as:** inconsistent trace: Points to LT: the bounds check runs at every access, at run time. Inconsistent application: the trace accepts an index of a.length on the last pass (or -1 on the first) but rejects it elsewhere, or reads 'some value' there. (here mixing in: "an out-of-bounds read returns null (it throws)")

## Errors (0)

An error edge states the rule that gets broken in a program, and the right rule.

The graph has no error edge from this concept.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for array bounds: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to array bounds agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

array bounds -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (4 ways).

- **everyday reading** (folk-meaning rule): Folk meaning: in English, 'items 1 to 10' or 'up to n' includes the end point, and reading past the end of a list just gives 'nothing'. Java rule: the legal indices are 0..length-1, and any other index throws ArrayIndexOutOfBoundsException instead of returning a value.
- **misconception** (wrong rule / right rule; shows `OutOfBoundsElementsAreNull`): wrong rule: An out-of-bounds read returns null (or 0). Right rule: Reading or writing any index outside 0 to a.length - 1 throws ArrayIndexOutOfBoundsException and returns no value.
- **inconsistent trace** (uneven-application rule; shows `OutOfBoundsElementsAreNull`): Points to LT: the bounds check runs at every access, at run time. Inconsistent application: the trace accepts an index of a.length on the last pass (or -1 on the first) but rejects it elsewhere, or reads 'some value' there. (here mixing in: "an out-of-bounds read returns null (it throws)")
- **misconception** (wrong rule / right rule; shows `OffByOneBound`): wrong rule: &lt; vs &lt;= and 0..n vs 0..n-1 are interchangeable. Right rule: for (i = 0; i &lt; n; i++) runs n times with i going up to n - 1; with &lt;= it runs n + 1 times and reaches i = n, which is out of bounds for an array of length n.

### L1: Unistructural / atom x text surface

L1 for array bounds: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

array bounds -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

- **names the element** (identity rule): Identity: the bounds of an array are its legal index range, 0 to length-1.
- **states the rule** (declarative rule): Declarative: an index less than 0 or greater than length-1 makes the program terminate with an ArrayIndexOutOfBoundsException; it is the programmer's responsibility to use legal indices.

### L2: Multistructural / block x execution / preoperational

L2 for array bounds: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

array bounds -&gt; L2 (Multistructural): the answer applies the rules of array bounds to every part of the code, in order (3 ways).

- **line by line trace** (operational sequencing rule): Sequencing: at each access the index expression is evaluated first and then compared with 0 and a.length. Only if it is in range is the element read or written; otherwise the exception is thrown before any element changes.
- **output prediction** (evaluation / result rule): Result: a legal access yields the element. An illegal one yields no value; the program stops with ArrayIndexOutOfBoundsException naming the bad index (old JVMs print ': 10', current ones 'Index 10 out of bounds for length 10').
- **one step execution** (state-transition rule): State transition: an out-of-bounds write changes no element, because the exception is raised before the store. Control leaves the statement, and main terminates unless the exception is caught.

### L3: Relational / relations x function (concrete operational begins)

L3 for array bounds: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

array bounds -&gt; L3 (Relational): the answer relates the parts (3 ways).

- **relation to neighbour** (composition rule (with a neighbour)): Every index value used in a[i] must satisfy 0 &lt;= i &lt;= a.length-1; the last element is a[a.length-1].
- **relation to neighbour** (composition rule (with a neighbour)): Because an out-of-bounds index stops the program, the loop test checks the bounds before the body uses the index (e.g. x &gt; 0 &amp;&amp; x &lt; N-1 before a[x-1], a[x+1]).
- **purpose of the whole** (plan / role rule): Plan/role: run-time bounds checking makes an indexing mistake a visible error instead of silent memory corruption (buffer overflow).

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for array bounds: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

array bounds -&gt; L4 (Extended abstract): the answer reasons beyond the given code (4 ways).

- **predict a change** (conservation rule; shows `OutOfBoundsElementsAreNull`): Conservation: a loop bounded by i &lt; a.length stays within bounds when the array size changes. Changing &lt; to &lt;= adds one pass that throws, and starting at 1 or ending at a.length-1 silently skips an element.
- **transfer to a new program** (applicability rule): Applicability: check indices explicitly (or restrict the loop range) whenever an index is computed from data, a random number or a neighbour (i-1, i+1). A plain i &lt; a.length traversal or an enhanced for loop needs no extra check.
- **diagnose an error** (error rule): rule broken: Indices must be in 0..a.length-1. Kind: run-time exception. Trigger class: index &gt;= a.length or &lt; 0: i &lt;= a.length, a[i+1] on the last pass, a[i-1] at i = 0, a[0] on an empty array, or the Sample program run with M &gt; N (ArrayIndexOutOfBoundsException)
- **diagnose an error** (error rule): rule broken: A traversal must reach the last valid index a.length-1. Kind: silent logic error. Trigger class: the loop stops one short (i &lt; a.length-1) or starts at 1, so the last or first element is never processed

## Same topic

`array_bounds` belongs to the topic **Memory representation and bounds checking** (`topic1.4.b`). The topic also contains: `array_aliasing`, `array_copy`, `array_reference`, `loop_guard`, `primitive_vs_reference`, `printing_array_reference`, `program_state`.

## Rules of the concept (16)

- **folk-meaning rule:** Folk meaning: in English, 'items 1 to 10' or 'up to n' includes the end point, and reading past the end of a list just gives 'nothing'. Java rule: the legal indices are 0..length-1, and any other index throws ArrayIndexOutOfBoundsException instead of returning a value.
- **wrong rule / right rule:** OffByOneBound: wrong: &lt; vs &lt;= and 0..n vs 0..n-1 are interchangeable. \| right: for (i = 0; i &lt; n; i++) runs n times with i going up to n - 1; with &lt;= it runs n + 1 times and reaches i = n, which is out of bounds for an array of length n.
- **wrong rule / right rule:** OutOfBoundsElementsAreNull: wrong: An out-of-bounds read returns null (or 0). \| right: Reading or writing any index outside 0 to a.length - 1 throws ArrayIndexOutOfBoundsException and returns no value.
- **uneven-application rule:** Points to LT: the bounds check runs at every access, at run time. Inconsistent application: the trace accepts an index of a.length on the last pass (or -1 on the first) but rejects it elsewhere, or reads 'some value' there.
- **identity rule:** Identity: the bounds of an array are its legal index range, 0 to length-1.
- **declarative rule:** Declarative: an index less than 0 or greater than length-1 makes the program terminate with an ArrayIndexOutOfBoundsException; it is the programmer's responsibility to use legal indices.
- **operational sequencing rule:** Sequencing: at each access the index expression is evaluated first and then compared with 0 and a.length. Only if it is in range is the element read or written; otherwise the exception is thrown before any element changes.
- **evaluation / result rule:** Result: a legal access yields the element. An illegal one yields no value; the program stops with ArrayIndexOutOfBoundsException naming the bad index (old JVMs print ': 10', current ones 'Index 10 out of bounds for length 10').
- **state-transition rule:** State transition: an out-of-bounds write changes no element, because the exception is raised before the store. Control leaves the statement, and main terminates unless the exception is caught.
- **composition rule (with a neighbour):** with indexing: Every index value used in a[i] must satisfy 0 &lt;= i &lt;= a.length-1; the last element is a[a.length-1].
- **composition rule (with a neighbour):** with loop\_guard: Because an out-of-bounds index stops the program, the loop test checks the bounds before the body uses the index (e.g. x &gt; 0 &amp;&amp; x &lt; N-1 before a[x-1], a[x+1]).
- **plan / role rule:** Plan/role: run-time bounds checking makes an indexing mistake a visible error instead of silent memory corruption (buffer overflow).
- **conservation rule:** Conservation: a loop bounded by i &lt; a.length stays within bounds when the array size changes. Changing &lt; to &lt;= adds one pass that throws, and starting at 1 or ending at a.length-1 silently skips an element.
- **error rule:** rule broken: Indices must be in 0..a.length-1. (run-time exception)
- **error rule:** rule broken: A traversal must reach the last valid index a.length-1. (silent logic error)
- **applicability rule:** Applicability: check indices explicitly (or restrict the loop range) whenever an index is computed from data, a random number or a neighbour (i-1, i+1). A plain i &lt; a.length traversal or an enhanced for loop needs no extra check.

## The whole prerequisite chain

- **Everything it builds on (6):** `array_creation`, `array_declaration`, `array_initializer`, `data_structure`, `data_type`, `indexing`
- **Everything that builds on it (2):** `loop_guard`, `run_time_error`
