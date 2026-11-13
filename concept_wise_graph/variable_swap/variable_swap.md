# variable_swap (`variable_swap`)

exchanging two variables needs a temporary

Section 1.2 Built-in Types of Data, topic 1.2.a Data types and terminology (literals, identifiers, variables, declarations, assignment, expressions).

![The knowledge graph around variable_swap](variable_swap.png)

## At a glance

- **Needs first:** `assignment`
- **Leads to:** nothing
- **Learned alongside:** nothing
- **Misconceptions:** `AssignmentExchangesValues`, `SwapWithoutTemp`
- **Errors:** none
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 26 edges around this concept, each explained in the graph's own words.

## What it needs first (1)

A prerequisite edge means the other concept has to be understood before `variable_swap`.

### `assignment` comes before `variable_swap`

*= stores the computed value of the right side*

The three assignments int t = a; a = b; b = t; exchange the values of a and b, as a trace of the variable values after each statement shows.

- **Grounding:** book passage
- **How `variable_swap` combines with `assignment`:** A swap is three assignments whose order matters, because each one overwrites the old value of its left variable.
- **How `assignment` combines with `variable_swap`:** int t = a; a = b; b = t; works only in this order, because every assignment destroys its left variable's old value.

## What it leads to (0)

These concepts need `variable_swap` first.

No concept has this one as a prerequisite.

## Learned alongside (0)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

No parallel edge touches this concept.

## Misconceptions (2)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### AssignmentExchangesValues

- **Wrong rule:** b = a exchanges the values of a and b.
- **Right rule:** b = a copies a into b and leaves a unchanged; an exchange needs a temporary variable and three assignments.
- **Role of this concept:** context
- **Shows at level L0 as:** misconception: wrong rule: b = a exchanges the values of a and b. Right rule: b = a copies a into b and leaves a unchanged; an exchange needs a temporary variable and three assignments.
- **Also an edge from `assignment`:** b = a exchanges the values of a and b.

### SwapWithoutTemp

- **Wrong rule:** a[i] = a[j]; a[j] = a[i]; exchanges the two values.
- **Right rule:** A temporary variable must save a[i] before it is overwritten.
- **Role of this concept:** context
- **Shows at level L0 as:** misconception: wrong rule: a[i] = a[j]; a[j] = a[i]; exchanges the two values. Right rule: A temporary variable must save a[i] before it is overwritten.
- **Shows at level L0 as:** inconsistent trace: Points to LT (three assignments in order, each using current values). Applied unevenly, a student traces the first two steps correctly but uses a's original value in the third, or calls one segment a swap and the other a copy without tracing either. (here mixing in: "a[i] = a[j]; a[j] = a[i]; exchanges the two values")
- **Also an edge from `array_exchange`:** a[i] = a[j]; a[j] = a[i]; exchanges the two values.
- **Also an edge from `assignment`:** a[i] = a[j]; a[j] = a[i]; exchanges the two values.

## Errors (0)

An error edge states the rule that gets broken in a program, and the right rule.

The graph has no error edge from this concept.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for variable swap: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to variable swap agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

variable swap -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (4 ways).

- **everyday reading** (folk-meaning rule): In everyday life two people swap objects at the same moment, hand to hand, and 'b = a' sounds like 'a and b are now the same thing'. Java statements run one at a time, so the first assignment destroys a value unless it was first saved in a temporary.
- **misconception** (wrong rule / right rule; shows `SwapWithoutTemp`): wrong rule: a[i] = a[j]; a[j] = a[i]; exchanges the two values. Right rule: A temporary variable must save a[i] before it is overwritten.
- **inconsistent trace** (uneven-application rule; shows `SwapWithoutTemp`): Points to LT (three assignments in order, each using current values). Applied unevenly, a student traces the first two steps correctly but uses a's original value in the third, or calls one segment a swap and the other a copy without tracing either. (here mixing in: "a[i] = a[j]; a[j] = a[i]; exchanges the two values")
- **misconception** (wrong rule / right rule; shows `AssignmentExchangesValues`): wrong rule: b = a exchanges the values of a and b. Right rule: b = a copies a into b and leaves a unchanged; an exchange needs a temporary variable and three assignments.

### L1: Unistructural / atom x text surface

L1 for variable swap: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

variable swap -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

- **names the element** (identity rule): Variable swap: the three-assignment idiom that exchanges the values of two variables through a temporary variable.
- **states the rule** (declarative rule): int t = a; a = b; b = t; exchanges a and b. The temporary t must have their type, and the three statements must run in exactly this order.

### L2: Multistructural / block x execution / preoperational

L2 for variable swap: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

variable swap -&gt; L2 (Multistructural): the answer applies the rules of variable swap to every part of the code, in order (3 ways).

- **line by line trace** (operational sequencing rule): Step 1 saves a in t. Step 2 overwrites a with b. Step 3 copies the saved value from t into b. Each step reads values left by the previous one.
- **output prediction** (evaluation / result rule): Starting from a = 1234 and b = 99, the swap ends with a = 99, b = 1234 and t = 1234.
- **one step execution** (state-transition rule): Each of the three statements changes exactly one variable: first t, then a, then b.

### L3: Relational / relations x function (concrete operational begins)

L3 for variable swap: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

variable swap -&gt; L3 (Relational): the answer relates the parts (2 ways).

- **relation to neighbour** (composition rule (with a neighbour)): A swap is three assignments whose order matters, because each one overwrites the old value of its left variable.
- **purpose of the whole** (plan / role rule): Plan: exchange. It is used to reorder two values (make a &lt;= b), and inside sorting and shuffling of arrays. t plays Sajaniemi's temporary role.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for variable swap: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

variable swap -&gt; L4 (Extended abstract): the answer reasons beyond the given code (4 ways).

- **predict a change** (conservation rule; shows `SwapWithoutTemp`): Reordering the steps (int t = a; b = t; a = b;) breaks the swap: both variables end up holding a's value. Dropping the temporary breaks it the same way. Running the correct swap twice restores the originals, so a swap is its own inverse.
- **transfer to a new program** (applicability rule): Use the swap when two variables or array elements must exchange values (sorting, shuffling, ordering a pair). It is not needed when you only need a new variable holding the larger value, or when you can compute directly into new variables.
- **diagnose an error** (error rule): rule broken: An assignment overwrites its target, so a value about to be overwritten must be saved first. Kind: silent logic error. Trigger class: Swapping without a temporary (a = b; b = a;) or in the wrong order: both variables end with the same value whenever a != b.
- **diagnose an error** (error rule): rule broken: The temporary must have the type of the values being swapped. Kind: compile-time. Trigger class: Using int t to swap doubles: 'possible lossy conversion from double to int'.

## Same topic

`variable_swap` belongs to the topic **Data types and terminology (literals, identifiers, variables, declarations, assignment, expressions)** (`topic1.2.a`). The topic also contains: `assignment`, `chained_assignment`, `data_type`, `declaration`, `definite_assignment`, `expression`, `identifier`, `literal`, `named_constants`, `naming_convention`, `operator_precedence`, `primitive_type`, `program_trace`, `variable`.

## Rules of the concept (15)

- **folk-meaning rule:** In everyday life two people swap objects at the same moment, hand to hand, and 'b = a' sounds like 'a and b are now the same thing'. Java statements run one at a time, so the first assignment destroys a value unless it was first saved in a temporary.
- **wrong rule / right rule:** SwapWithoutTemp: wrong: a[i] = a[j]; a[j] = a[i]; exchanges the two values. \| right: A temporary variable must save a[i] before it is overwritten.
- **wrong rule / right rule:** AssignmentExchangesValues: wrong: b = a exchanges the values of a and b. \| right: b = a copies a into b and leaves a unchanged; an exchange needs a temporary variable and three assignments.
- **uneven-application rule:** Points to LT (three assignments in order, each using current values). Applied unevenly, a student traces the first two steps correctly but uses a's original value in the third, or calls one segment a swap and the other a copy without tracing either.
- **identity rule:** Variable swap: the three-assignment idiom that exchanges the values of two variables through a temporary variable.
- **declarative rule:** int t = a; a = b; b = t; exchanges a and b. The temporary t must have their type, and the three statements must run in exactly this order.
- **operational sequencing rule:** Step 1 saves a in t. Step 2 overwrites a with b. Step 3 copies the saved value from t into b. Each step reads values left by the previous one.
- **evaluation / result rule:** Starting from a = 1234 and b = 99, the swap ends with a = 99, b = 1234 and t = 1234.
- **state-transition rule:** Each of the three statements changes exactly one variable: first t, then a, then b.
- **composition rule (with a neighbour):** with assignment: A swap is three assignments whose order matters, because each one overwrites the old value of its left variable.
- **plan / role rule:** Plan: exchange. It is used to reorder two values (make a &lt;= b), and inside sorting and shuffling of arrays. t plays Sajaniemi's temporary role.
- **conservation rule:** Reordering the steps (int t = a; b = t; a = b;) breaks the swap: both variables end up holding a's value. Dropping the temporary breaks it the same way. Running the correct swap twice restores the originals, so a swap is its own inverse.
- **error rule:** rule broken: An assignment overwrites its target, so a value about to be overwritten must be saved first. (silent logic error)
- **error rule:** rule broken: The temporary must have the type of the values being swapped. (compile-time)
- **applicability rule:** Use the swap when two variables or array elements must exchange values (sorting, shuffling, ordering a pair). It is not needed when you only need a new variable holding the larger value, or when you can compute directly into new variables.

## The whole prerequisite chain

- **Everything it builds on (7):** `assignment`, `data_type`, `declaration`, `identifier`, `literal`, `primitive_type`, `variable`
- **Everything that builds on it (0):** nothing
