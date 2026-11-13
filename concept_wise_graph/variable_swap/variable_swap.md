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

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 26 edges around this concept. The edge logic, the wrong and right rules and the exact rules of the ways are copied word for word from the graph.

## To work on (0)

Nothing is missing for this concept.

## What it needs first (1)

A prerequisite edge means the other concept has to be understood before `variable_swap`.

### `assignment` comes before `variable_swap`

*= stores the computed value of the right side*

- **Edge:** `pre:assignment->variable_swap`
- **Exact edge logic:** The three assignments int t = a; a = b; b = t; exchange the values of a and b, as a trace of the variable values after each statement shows.
- **Grounding:** book\_passage
- **Composition rule (R) of `variable_swap` with `assignment`:** A swap is three assignments whose order matters, because each one overwrites the old value of its left variable.
- **Composition rule (R) of `assignment` with `variable_swap`:** int t = a; a = b; b = t; works only in this order, because every assignment destroys its left variable's old value.

## What it leads to (0)

These concepts need `variable_swap` first.

No concept has this one as a prerequisite.

## Learned alongside (0)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

No parallel edge touches this concept.

## Misconceptions (2)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### AssignmentExchangesValues

- **Edge:** `variable_swap` &rarr; `AssignmentExchangesValues` (misconception)
- **Exact edge logic (the wrong rule):** b = a exchanges the values of a and b.
- **Twin logic (the right rule):** b = a copies a into b and leaves a unchanged; an exchange needs a temporary variable and three assignments.
- **Wrong belief (on the node):** b = a exchanges the values of a and b.
- **Correct rule (on the node):** b = a copies a into b and leaves a unchanged; an exchange needs a temporary variable and three assignments.
- **Provenance:** published
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [3] misconception, exact rule:** wrong rule: b = a exchanges the values of a and b. Right rule: b = a copies a into b and leaves a unchanged; an exchange needs a temporary variable and three assignments.
- **Edge `assignment` &rarr; `AssignmentExchangesValues`, exact edge logic:** b = a exchanges the values of a and b. **Twin logic:** b = a copies a into b and leaves a unchanged; an exchange needs a temporary variable and three assignments. (role: primary)

### SwapWithoutTemp

- **Edge:** `variable_swap` &rarr; `SwapWithoutTemp` (misconception)
- **Exact edge logic (the wrong rule):** a[i] = a[j]; a[j] = a[i]; exchanges the two values.
- **Twin logic (the right rule):** A temporary variable must save a[i] before it is overwritten.
- **Wrong belief (on the node):** a[i] = a[j]; a[j] = a[i]; exchanges the two values.
- **Correct rule (on the node):** A temporary variable must save a[i] before it is overwritten.
- **Provenance:** textbook
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [1] misconception, exact rule:** wrong rule: a[i] = a[j]; a[j] = a[i]; exchanges the two values. Right rule: A temporary variable must save a[i] before it is overwritten.
- **L0 way [2] inconsistent\_trace, exact rule:** Points to LT (three assignments in order, each using current values). Applied unevenly, a student traces the first two steps correctly but uses a's original value in the third, or calls one segment a swap and the other a copy without tracing either. (here mixing in: "a[i] = a[j]; a[j] = a[i]; exchanges the two values")
- **Edge `array_exchange` &rarr; `SwapWithoutTemp`, exact edge logic:** a[i] = a[j]; a[j] = a[i]; exchanges the two values. **Twin logic:** A temporary variable must save a[i] before it is overwritten. (role: primary)
- **Edge `assignment` &rarr; `SwapWithoutTemp`, exact edge logic:** a[i] = a[j]; a[j] = a[i]; exchanges the two values. **Twin logic:** A temporary variable must save a[i] before it is overwritten. (role: context)

## Errors (0)

An error edge states the rule that gets broken in a program, and the right rule.

The graph has no error edge from this concept.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for variable swap: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to variable swap agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

- **Edge:** `variable_swap` &rarr; `variable_swap@L0` (has_level)
- **Exact edge logic:** variable swap -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (4 ways).

Ways (4), each with its exact rule:

- **[0] everyday\_reading** (rule type E, folk-meaning rule): In everyday life two people swap objects at the same moment, hand to hand, and 'b = a' sounds like 'a and b are now the same thing'. Java statements run one at a time, so the first assignment destroys a value unless it was first saved in a temporary.
- **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `SwapWithoutTemp`: wrong rule: a[i] = a[j]; a[j] = a[i]; exchanges the two values. Right rule: A temporary variable must save a[i] before it is overwritten.
- **[2] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `SwapWithoutTemp`: Points to LT (three assignments in order, each using current values). Applied unevenly, a student traces the first two steps correctly but uses a's original value in the third, or calls one segment a swap and the other a copy without tracing either. (here mixing in: "a[i] = a[j]; a[j] = a[i]; exchanges the two values")
- **[3] misconception** (rule type M, wrong rule / right rule) &rarr; `AssignmentExchangesValues`: wrong rule: b = a exchanges the values of a and b. Right rule: b = a copies a into b and leaves a unchanged; an exchange needs a temporary variable and three assignments.

### L1: Unistructural / atom x text surface

L1 for variable swap: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

- **Edge:** `variable_swap` &rarr; `variable_swap@L1` (has_level)
- **Exact edge logic:** variable swap -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

Ways (2), each with its exact rule:

- **[0] names\_the\_element** (rule type N, identity rule): Variable swap: the three-assignment idiom that exchanges the values of two variables through a temporary variable.
- **[1] states\_the\_rule** (rule type S, declarative rule): int t = a; a = b; b = t; exchanges a and b. The temporary t must have their type, and the three statements must run in exactly this order.

### L2: Multistructural / block x execution / preoperational

L2 for variable swap: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

- **Edge:** `variable_swap` &rarr; `variable_swap@L2` (has_level)
- **Exact edge logic:** variable swap -&gt; L2 (Multistructural): the answer applies the rules of variable swap to every part of the code, in order (3 ways).

Ways (3), each with its exact rule:

- **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): Step 1 saves a in t. Step 2 overwrites a with b. Step 3 copies the saved value from t into b. Each step reads values left by the previous one.
- **[1] output\_prediction** (rule type OP, evaluation / result rule): Starting from a = 1234 and b = 99, the swap ends with a = 99, b = 1234 and t = 1234.
- **[2] one\_step\_execution** (rule type OS, state-transition rule): Each of the three statements changes exactly one variable: first t, then a, then b.

### L3: Relational / relations x function (concrete operational begins)

L3 for variable swap: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

- **Edge:** `variable_swap` &rarr; `variable_swap@L3` (has_level)
- **Exact edge logic:** variable swap -&gt; L3 (Relational): the answer relates the parts (2 ways).

Ways (2), each with its exact rule:

- **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): A swap is three assignments whose order matters, because each one overwrites the old value of its left variable.
- **[1] purpose\_of\_the\_whole** (rule type P, plan / role rule): Plan: exchange. It is used to reorder two values (make a &lt;= b), and inside sorting and shuffling of arrays. t plays Sajaniemi's temporary role.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for variable swap: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

- **Edge:** `variable_swap` &rarr; `variable_swap@L4` (has_level)
- **Exact edge logic:** variable swap -&gt; L4 (Extended abstract): the answer reasons beyond the given code (4 ways).

Ways (4), each with its exact rule:

- **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `SwapWithoutTemp`: Reordering the steps (int t = a; b = t; a = b;) breaks the swap: both variables end up holding a's value. Dropping the temporary breaks it the same way. Running the correct swap twice restores the originals, so a swap is its own inverse.
- **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Use the swap when two variables or array elements must exchange values (sorting, shuffling, ordering a pair). It is not needed when you only need a new variable holding the larger value, or when you can compute directly into new variables.
- **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: An assignment overwrites its target, so a value about to be overwritten must be saved first. Kind: silent logic error. Trigger class: Swapping without a temporary (a = b; b = a;) or in the wrong order: both variables end with the same value whenever a != b.
- **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: The temporary must have the type of the values being swapped. Kind: compile-time. Trigger class: Using int t to swap doubles: 'possible lossy conversion from double to int'.

## Same topic

`variable_swap` belongs to the topic **Data types and terminology (literals, identifiers, variables, declarations, assignment, expressions)** (`topic1.2.a`). The topic also contains: `assignment`, `chained_assignment`, `data_type`, `declaration`, `definite_assignment`, `expression`, `identifier`, `literal`, `named_constants`, `naming_convention`, `operator_precedence`, `primitive_type`, `program_trace`, `variable`.

## Rules of the concept (15)

- **Book** (SW-1e, p. 17 (pdf 27)): "convince yourself that the following code exchanges the values of a and b (assume that a and b are int variables)"
- **Book** (SW-1.2, ): "int t = a; b = t; a = b; … Solution: sets a, b, and t equal to the original value of a."
- **E** (folk-meaning rule): In everyday life two people swap objects at the same moment, hand to hand, and 'b = a' sounds like 'a and b are now the same thing'. Java statements run one at a time, so the first assignment destroys a value unless it was first saved in a temporary.
- **M** (wrong rule / right rule): SwapWithoutTemp: wrong: a[i] = a[j]; a[j] = a[i]; exchanges the two values. \| right: A temporary variable must save a[i] before it is overwritten.
- **M** (wrong rule / right rule): AssignmentExchangesValues: wrong: b = a exchanges the values of a and b. \| right: b = a copies a into b and leaves a unchanged; an exchange needs a temporary variable and three assignments.
- **T** (uneven-application rule): Points to LT (three assignments in order, each using current values). Applied unevenly, a student traces the first two steps correctly but uses a's original value in the third, or calls one segment a swap and the other a copy without tracing either.
- **N** (identity rule): Variable swap: the three-assignment idiom that exchanges the values of two variables through a temporary variable.
- **S** (declarative rule): int t = a; a = b; b = t; exchanges a and b. The temporary t must have their type, and the three statements must run in exactly this order.
- **LT** (operational sequencing rule): Step 1 saves a in t. Step 2 overwrites a with b. Step 3 copies the saved value from t into b. Each step reads values left by the previous one.
- **OP** (evaluation / result rule): Starting from a = 1234 and b = 99, the swap ends with a = 99, b = 1234 and t = 1234.
- **OS** (state-transition rule): Each of the three statements changes exactly one variable: first t, then a, then b.
- **R** (composition rule (with a neighbour)): with assignment: A swap is three assignments whose order matters, because each one overwrites the old value of its left variable.
- **P** (plan / role rule): Plan: exchange. It is used to reorder two values (make a &lt;= b), and inside sorting and shuffling of arrays. t plays Sajaniemi's temporary role.
- **C** (conservation rule): Reordering the steps (int t = a; b = t; a = b;) breaks the swap: both variables end up holding a's value. Dropping the temporary breaks it the same way. Running the correct swap twice restores the originals, so a swap is its own inverse.
- **D** (error rule): rule broken: An assignment overwrites its target, so a value about to be overwritten must be saved first. (silent logic error)
- **D** (error rule): rule broken: The temporary must have the type of the values being swapped. (compile-time)
- **X** (applicability rule): Use the swap when two variables or array elements must exchange values (sorting, shuffling, ordering a pair). It is not needed when you only need a new variable holding the larger value, or when you can compute directly into new variables.

## How it is found in code and answers (reader block)

- **Aliases:** swap, swaps, swapped, exchange, exchanges, swaps the values
- **Code patterns:** none
- **Operator symbols:** none
- **Java types:** none
- **Signal swap** (scope program, decisive): `(?:\b\w+\s+)?(?P<t>\b\w+)\s*=\s*(?P<var>\w+)\s*;\s*(?P=var)\s*=\s*(?P<b>\w+)\s*;\s*(?P=b)\s*=\s*(?P=t)\s*;`

## The whole prerequisite chain

- **Everything it builds on (7):** `assignment`, `data_type`, `declaration`, `identifier`, `literal`, `primitive_type`, `variable`
- **Everything that builds on it (0):** nothing

## Every edge in this view and its exact edge logic (26)

All the edges drawn in the picture, in the order: prerequisite, parallel, misconception, error, has_level, contains.

**1. `assignment` &rarr; `variable_swap`** (prerequisite)

- **Exact edge logic:** The three assignments int t = a; a = b; b = t; exchange the values of a and b, as a trace of the variable values after each statement shows.
- **Grounding:** book\_passage
- **Composition rule (R) of `assignment` with `variable_swap`:** int t = a; a = b; b = t; works only in this order, because every assignment destroys its left variable's old value.
- **Composition rule (R) of `variable_swap` with `assignment`:** A swap is three assignments whose order matters, because each one overwrites the old value of its left variable.

**2. `variable_swap` &rarr; `AssignmentExchangesValues`** (misconception)

- **Exact edge logic (the wrong rule):** b = a exchanges the values of a and b.
- **Twin logic (the right rule):** b = a copies a into b and leaves a unchanged; an exchange needs a temporary variable and three assignments.
- **Role:** context

**3. `variable_swap` &rarr; `SwapWithoutTemp`** (misconception)

- **Exact edge logic (the wrong rule):** a[i] = a[j]; a[j] = a[i]; exchanges the two values.
- **Twin logic (the right rule):** A temporary variable must save a[i] before it is overwritten.
- **Role:** context

**4. `array_exchange` &rarr; `SwapWithoutTemp`** (misconception)

- **Exact edge logic (the wrong rule):** a[i] = a[j]; a[j] = a[i]; exchanges the two values.
- **Twin logic (the right rule):** A temporary variable must save a[i] before it is overwritten.
- **Role:** primary

**5. `assignment` &rarr; `AssignmentExchangesValues`** (misconception)

- **Exact edge logic (the wrong rule):** b = a exchanges the values of a and b.
- **Twin logic (the right rule):** b = a copies a into b and leaves a unchanged; an exchange needs a temporary variable and three assignments.
- **Role:** primary

**6. `assignment` &rarr; `SwapWithoutTemp`** (misconception)

- **Exact edge logic (the wrong rule):** a[i] = a[j]; a[j] = a[i]; exchanges the two values.
- **Twin logic (the right rule):** A temporary variable must save a[i] before it is overwritten.
- **Role:** context

**7. `variable_swap` &rarr; `variable_swap@L0`** (has_level)

- **Exact edge logic:** variable swap -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (4 ways).
  - **[0] everyday\_reading** (rule type E, folk-meaning rule): In everyday life two people swap objects at the same moment, hand to hand, and 'b = a' sounds like 'a and b are now the same thing'. Java statements run one at a time, so the first assignment destroys a value unless it was first saved in a temporary.
  - **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `SwapWithoutTemp`: wrong rule: a[i] = a[j]; a[j] = a[i]; exchanges the two values. Right rule: A temporary variable must save a[i] before it is overwritten.
  - **[2] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `SwapWithoutTemp`: Points to LT (three assignments in order, each using current values). Applied unevenly, a student traces the first two steps correctly but uses a's original value in the third, or calls one segment a swap and the other a copy without tracing either. (here mixing in: "a[i] = a[j]; a[j] = a[i]; exchanges the two values")
  - **[3] misconception** (rule type M, wrong rule / right rule) &rarr; `AssignmentExchangesValues`: wrong rule: b = a exchanges the values of a and b. Right rule: b = a copies a into b and leaves a unchanged; an exchange needs a temporary variable and three assignments.

**8. `variable_swap` &rarr; `variable_swap@L1`** (has_level)

- **Exact edge logic:** variable swap -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).
  - **[0] names\_the\_element** (rule type N, identity rule): Variable swap: the three-assignment idiom that exchanges the values of two variables through a temporary variable.
  - **[1] states\_the\_rule** (rule type S, declarative rule): int t = a; a = b; b = t; exchanges a and b. The temporary t must have their type, and the three statements must run in exactly this order.

**9. `variable_swap` &rarr; `variable_swap@L2`** (has_level)

- **Exact edge logic:** variable swap -&gt; L2 (Multistructural): the answer applies the rules of variable swap to every part of the code, in order (3 ways).
  - **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): Step 1 saves a in t. Step 2 overwrites a with b. Step 3 copies the saved value from t into b. Each step reads values left by the previous one.
  - **[1] output\_prediction** (rule type OP, evaluation / result rule): Starting from a = 1234 and b = 99, the swap ends with a = 99, b = 1234 and t = 1234.
  - **[2] one\_step\_execution** (rule type OS, state-transition rule): Each of the three statements changes exactly one variable: first t, then a, then b.

**10. `variable_swap` &rarr; `variable_swap@L3`** (has_level)

- **Exact edge logic:** variable swap -&gt; L3 (Relational): the answer relates the parts (2 ways).
  - **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): A swap is three assignments whose order matters, because each one overwrites the old value of its left variable.
  - **[1] purpose\_of\_the\_whole** (rule type P, plan / role rule): Plan: exchange. It is used to reorder two values (make a &lt;= b), and inside sorting and shuffling of arrays. t plays Sajaniemi's temporary role.

**11. `variable_swap` &rarr; `variable_swap@L4`** (has_level)

- **Exact edge logic:** variable swap -&gt; L4 (Extended abstract): the answer reasons beyond the given code (4 ways).
  - **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `SwapWithoutTemp`: Reordering the steps (int t = a; b = t; a = b;) breaks the swap: both variables end up holding a's value. Dropping the temporary breaks it the same way. Running the correct swap twice restores the originals, so a swap is its own inverse.
  - **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Use the swap when two variables or array elements must exchange values (sorting, shuffling, ordering a pair). It is not needed when you only need a new variable holding the larger value, or when you can compute directly into new variables.
  - **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: An assignment overwrites its target, so a value about to be overwritten must be saved first. Kind: silent logic error. Trigger class: Swapping without a temporary (a = b; b = a;) or in the wrong order: both variables end with the same value whenever a != b.
  - **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: The temporary must have the type of the values being swapped. Kind: compile-time. Trigger class: Using int t to swap doubles: 'possible lossy conversion from double to int'.

**12. `topic1.2.a` &rarr; `variable_swap`** (contains)

- topic `topic1.2.a` contains `variable_swap`

**13. `topic1.2.a` &rarr; `assignment`** (contains)

- topic `topic1.2.a` contains `assignment`

**14. `topic1.2.a` &rarr; `chained_assignment`** (contains)

- topic `topic1.2.a` contains `chained_assignment`

**15. `topic1.2.a` &rarr; `data_type`** (contains)

- topic `topic1.2.a` contains `data_type`

**16. `topic1.2.a` &rarr; `declaration`** (contains)

- topic `topic1.2.a` contains `declaration`

**17. `topic1.2.a` &rarr; `definite_assignment`** (contains)

- topic `topic1.2.a` contains `definite_assignment`

**18. `topic1.2.a` &rarr; `expression`** (contains)

- topic `topic1.2.a` contains `expression`

**19. `topic1.2.a` &rarr; `identifier`** (contains)

- topic `topic1.2.a` contains `identifier`

**20. `topic1.2.a` &rarr; `literal`** (contains)

- topic `topic1.2.a` contains `literal`

**21. `topic1.2.a` &rarr; `named_constants`** (contains)

- topic `topic1.2.a` contains `named_constants`

**22. `topic1.2.a` &rarr; `naming_convention`** (contains)

- topic `topic1.2.a` contains `naming_convention`

**23. `topic1.2.a` &rarr; `operator_precedence`** (contains)

- topic `topic1.2.a` contains `operator_precedence`

**24. `topic1.2.a` &rarr; `primitive_type`** (contains)

- topic `topic1.2.a` contains `primitive_type`

**25. `topic1.2.a` &rarr; `program_trace`** (contains)

- topic `topic1.2.a` contains `program_trace`

**26. `topic1.2.a` &rarr; `variable`** (contains)

- topic `topic1.2.a` contains `variable`
