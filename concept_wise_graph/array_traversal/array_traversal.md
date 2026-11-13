# array_traversal (`array_traversal`)

walking the array with an index loop

Section 1.4 Arrays, topic 1.4.c Setting array values at compile time and at run time.

![The knowledge graph around array_traversal](array_traversal.png)

## At a glance

- **Needs first:** `for_loop`, `indexing`, `length_field`
- **Leads to:** `array_copy`, `array_reversal`, `boolean_flag_array`, `enhanced_for`, `function_plotting`, `running_extreme`
- **Learned alongside:** nothing
- **Misconceptions:** `ArrayUseScansAllCells`, `ElementBoundToOldIndex`, `IdiomOverridesCode`, `OffByOneBound`, `WholeArrayArithmetic`
- **Errors:** `EarlyReturnInLoop`
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 37 edges around this concept. The edge logic, the wrong and right rules and the exact rules of the ways are copied word for word from the graph.

## To work on (1)

- no aliases: a student's words cannot name this concept

## What it needs first (3)

A prerequisite edge means the other concept has to be understood before `array_traversal`.

### `for_loop` comes before `array_traversal`

*a while with init/condition/update packaged together*

- **Edge:** `pre:for_loop->array_traversal`
- **Exact edge logic:** for (int i = 0; i &lt; a.length; i++) gives i every valid index exactly once, in increasing order.
- **Grounding:** book\_passage
- **Composition rule (R) of `array_traversal` with `for_loop`:** for (int i = 0; i &lt; a.length; i++) gives i every valid index exactly once, in increasing order; the bound must be &lt; a.length, not &lt;=.
- **Composition rule (R) of `for_loop` with `array_traversal`:** for (int i = 0; i &lt; N; i++) gives i each valid index 0..N-1 exactly once in increasing order, the standard way to process every array element.

### `indexing` comes before `array_traversal`

*a[i] -- 0-based access*

- **Edge:** `pre:indexing->array_traversal`
- **Exact edge logic:** A traversal uses the loop variable i as the index, so a[i] reaches a different element on each pass.
- **Grounding:** book\_passage
- **Composition rule (R) of `array_traversal` with `indexing`:** The loop variable is used as the index, so a[i] reaches a different element on each pass.
- **Composition rule (R) of `indexing` with `array_traversal`:** A traversal uses the loop variable as the index, so the same expression a[i] reaches a different element on each pass.

### `length_field` comes before `array_traversal`

*a.length is a field, not a method*

- **Edge:** `pre:length_field->array_traversal`
- **Exact edge logic:** A traversal loop runs its index from 0 while it is below a.length, so it visits every element once.
- **Grounding:** book\_passage

## What it leads to (6)

These concepts need `array_traversal` first.

### `array_traversal` comes before `array_copy`

*making a second, independent array with the same elements: create a new array and copy element by element (or Arrays.copyOf)*

- **Edge:** `pre:array_traversal->array_copy`
- **Exact edge logic:** The elements are copied one at a time by a loop over every index.
- **Grounding:** book\_passage
- **Composition rule (R) of `array_copy` with `array_traversal`:** The copy is a traversal of every index of the original.

### `array_traversal` comes before `array_reversal`

*reversing an array in place*

- **Edge:** `pre:array_traversal->array_reversal`
- **Exact edge logic:** Reversal traverses only the first half of the array (i &lt; N/2), exchanging each a[i] with its mirror a[N-1-i].
- **Grounding:** book\_passage
- **Composition rule (R) of `array_traversal` with `array_reversal`:** Reversal traverses only the first half (i &lt; N/2), exchanging each a[i] with its mirror a[N-1-i].
- **Composition rule (R) of `array_reversal` with `array_traversal`:** Reversal traverses only the first half (i &lt; N/2) while indexing the second half through the mirror index.

### `array_traversal` comes before `boolean_flag_array`

*boolean[] used to mark which values are seen (coupon collector, sieve)*

- **Edge:** `pre:array_traversal->boolean_flag_array`
- **Exact edge logic:** The sieve traverses isPrime[] to set every flag to true and later traverses it again to count the flags that are still true.
- **Grounding:** book\_passage
- **Composition rule (R) of `array_traversal` with `boolean_flag_array`:** The sieve traverses isPrime[] once to set every flag to true and again at the end to count the flags still true.
- **Composition rule (R) of `boolean_flag_array` with `array_traversal`:** The sieve traverses isPrime[] to set every flag to true and later traverses it again to count the flags still true.

### `array_traversal` comes before `enhanced_for`

*for (int x : a) -- the for-each form*

- **Edge:** `pre:array_traversal->enhanced_for`
- **Exact edge logic:** for (int x : a) is a traversal that hands the body each value a[i] instead of the index i.
- **Grounding:** book\_passage
- **Composition rule (R) of `array_traversal` with `enhanced_for`:** for (int x : a) is a traversal that hands the body each value a[i] and hides the index i.
- **Composition rule (R) of `enhanced_for` with `array_traversal`:** It is a full forward traversal with the index hidden, so it cannot skip, go backward, stop at a computed index or write a[i].

### `array_traversal` comes before `function_plotting`

*sampling a function and joining the points with lines*

- **Edge:** `pre:array_traversal->function_plotting`
- **Exact edge logic:** The sample points are kept in arrays and traversed.
- **Grounding:** book\_passage
- **Composition rule (R) of `array_traversal` with `function_plotting`:** Sample points are computed into x[] and y[] by one traversal and drawn by another.
- **Composition rule (R) of `function_plotting` with `array_traversal`:** The arrays have N+1 elements (indices 0..N). The drawing loop starts at i = 1 so that x[i-1] stays in bounds; starting at 0 would access x[-1].

### `array_traversal` comes before `running_extreme`

*tracking the max or min of a stream*

- **Edge:** `pre:array_traversal->running_extreme`
- **Exact edge logic:** The running maximum is found by traversing the array once, keeping the largest value seen so far (starting from Double.NEGATIVE\_INFINITY).
- **Grounding:** book\_passage
- **Composition rule (R) of `array_traversal` with `running_extreme`:** The running maximum is found in one traversal that keeps the largest value seen so far, starting from Double.NEGATIVE\_INFINITY.
- **Composition rule (R) of `running_extreme` with `array_traversal`:** The maximum is found in one traversal, keeping the largest value seen so far, starting from Double.NEGATIVE\_INFINITY.

## Learned alongside (0)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

No parallel edge touches this concept.

## Misconceptions (5)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### ArrayUseScansAllCells

- **Edge:** `array_traversal` &rarr; `ArrayUseScansAllCells` (misconception)
- **Exact edge logic (the wrong rule):** Using an array means every cell must be scanned.
- **Twin logic (the right rule):** Arrays allow random access: a[i] reaches one element directly, and a loop visits only the elements the task needs.
- **Wrong belief (on the node):** Using an array means every cell must be scanned.
- **Correct rule (on the node):** Arrays allow random access: a[i] reaches one element directly, and a loop visits only the elements the task needs.
- **Provenance:** published
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [3] misconception, exact rule:** wrong rule: Using an array means every cell must be scanned. Right rule: A traversal may cover only part of the array or stop early (as in a search); indexing reaches single elements directly.
- **Edge `indexing` &rarr; `ArrayUseScansAllCells`, exact edge logic:** Using an array means every cell must be scanned. **Twin logic:** Arrays allow random access: a[i] reaches one element directly, and a loop visits only the elements the task needs. (role: context)

### ElementBoundToOldIndex

- **Edge:** `array_traversal` &rarr; `ElementBoundToOldIndex` (misconception)
- **Exact edge logic (the wrong rule):** After i changes, X[i] still refers to the element at the old value of i.
- **Twin logic (the right rule):** a[i] is evaluated with the current value of i each time it is used.
- **Wrong belief (on the node):** After i changes, X[i] still refers to the element at the old value of i.
- **Correct rule (on the node):** a[i] is evaluated with the current value of i each time it is used.
- **Provenance:** published
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [6] misconception, exact rule:** wrong rule: After i changes, X[i] still refers to the element at the old value of i. Right rule: a[i] is evaluated with the current value of i each time it is used.
- **Edge `indexing` &rarr; `ElementBoundToOldIndex`, exact edge logic:** After i changes, X[i] still refers to the element at the old value of i. **Twin logic:** a[i] is evaluated with the current value of i each time it is used. (role: primary)

### IdiomOverridesCode

- **Edge:** `array_traversal` &rarr; `IdiomOverridesCode` (misconception)
- **Exact edge logic (the wrong rule):** An array loop processes the whole array from index 0 to length-1 and increments its index at the end of the body, whatever the code says.
- **Twin logic (the right rule):** The loop visits exactly the indices that its initialisation, guard and update produce, in the order in which its statements are written.
- **Wrong belief (on the node):** An array loop processes the whole array from index 0 to length-1 and increments its index at the end of the body, whatever the code says.
- **Correct rule (on the node):** The loop visits exactly the indices that its initialisation, guard and update produce, in the order in which its statements are written.
- **Provenance:** published
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [2] misconception, exact rule:** wrong rule: An array loop processes the whole array from index 0 to length-1 and increments its index at the end of the body, whatever the code says. Right rule: The loop visits exactly the indices that its initialisation, guard and update produce, in the order in which its statements are written.
- **Edge `for_loop` &rarr; `IdiomOverridesCode`, exact edge logic:** An array loop processes the whole array from index 0 to length-1 and increments its index at the end of the body, whatever the code says. **Twin logic:** The loop visits exactly the indices that its initialisation, guard and update produce, in the order in which its statements are written. (role: context)
- **Edge `increment_operators` &rarr; `IdiomOverridesCode`, exact edge logic:** An array loop processes the whole array from index 0 to length-1 and increments its index at the end of the body, whatever the code says. **Twin logic:** The loop visits exactly the indices that its initialisation, guard and update produce, in the order in which its statements are written. (role: context)
- **Edge `loop_control` &rarr; `IdiomOverridesCode`, exact edge logic:** An array loop processes the whole array from index 0 to length-1 and increments its index at the end of the body, whatever the code says. **Twin logic:** The loop visits exactly the indices that its initialisation, guard and update produce, in the order in which its statements are written. (role: context)

### OffByOneBound

- **Edge:** `array_traversal` &rarr; `OffByOneBound` (misconception)
- **Exact edge logic (the wrong rule):** &lt; vs &lt;= and 0..n vs 0..n-1 are interchangeable
- **Twin logic (the right rule):** for (i = 0; i &lt; n; i++) runs n times with i going up to n - 1; with &lt;= it runs n + 1 times and reaches i = n.
- **Wrong belief (on the node):** &lt; vs &lt;= and 0..n vs 0..n-1 are interchangeable
- **Correct rule (on the node):** for (i = 0; i &lt; n; i++) runs n times with i going up to n - 1; with &lt;= it runs n + 1 times and reaches i = n.
- **Provenance:** published
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [5] misconception, exact rule:** wrong rule: &lt; vs &lt;= and 0..n vs 0..n-1 are interchangeable. Right rule: for (i = 0; i &lt; n; i++) runs n times with i going up to n - 1; with &lt;= it runs n + 1 times and reaches i = n.
- **Edge `array_bounds` &rarr; `OffByOneBound`, exact edge logic:** &lt; vs &lt;= and 0..n vs 0..n-1 are interchangeable **Twin logic:** for (i = 0; i &lt; n; i++) runs n times with i going up to n - 1; with &lt;= it runs n + 1 times and reaches i = n. (role: context)
- **Edge `array_reversal` &rarr; `OffByOneBound`, exact edge logic:** &lt; vs &lt;= and 0..n vs 0..n-1 are interchangeable **Twin logic:** for (i = 0; i &lt; n; i++) runs n times with i going up to n - 1; with &lt;= it runs n + 1 times and reaches i = n. (role: context)
- **Edge `boolean_flag_array` &rarr; `OffByOneBound`, exact edge logic:** &lt; vs &lt;= and 0..n vs 0..n-1 are interchangeable **Twin logic:** for (i = 0; i &lt; n; i++) runs n times with i going up to n - 1; with &lt;= it runs n + 1 times and reaches i = n. (role: context)
- **Edge `loop_control` &rarr; `OffByOneBound`, exact edge logic:** i &lt; n and i &lt;= n mean the same, so the loop runs until i equals n and the last pass can use a[n]. **Twin logic:** for (i = 0; i &lt; n; i++) runs n times with i going up to n - 1; with &lt;= it runs n + 1 times and reaches i = n. (role: primary)
- **Edge `off_by_one_error` &rarr; `OffByOneBound`, exact edge logic:** &lt; vs &lt;= and 0..n vs 0..n-1 are interchangeable **Twin logic:** for (i = 0; i &lt; n; i++) runs n times with i going up to n - 1; with &lt;= it runs n + 1 times and reaches i = n. (role: context)
- **Edge `simulation_loop` &rarr; `OffByOneBound`, exact edge logic:** t &lt; T and t &lt;= T give the same number of moves. **Twin logic:** for (t = 0; t &lt; T; t++) makes exactly T moves; with &lt;= it makes T + 1. (role: context)

### WholeArrayArithmetic

- **Edge:** `array_traversal` &rarr; `WholeArrayArithmetic` (misconception)
- **Exact edge logic (the wrong rule):** a = a + b adds the arrays element by element.
- **Twin logic (the right rule):** Java has no arithmetic on whole arrays; write a loop that adds a[i] + b[i] for each i.
- **Wrong belief (on the node):** a = a + b adds the arrays element by element.
- **Correct rule (on the node):** Java has no arithmetic on whole arrays; write a loop that adds a[i] + b[i] for each i.
- **Provenance:** textbook
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [1] misconception, exact rule:** wrong rule: a = a + b adds the arrays element by element. Right rule: Java has no arithmetic on whole arrays; write a loop that adds a[i] + b[i] for each i.
- **L0 way [4] inconsistent\_trace, exact rule:** Points to LT: initialize i, test, run the body with the current i, update, test again. Inconsistent application: on some passes the update is applied before the body, or a[i] is traced with the previous i. (here mixing in: "a = a + b adds the arrays element by element")
- **Edge `matrix_operations` &rarr; `WholeArrayArithmetic`, exact edge logic:** a = a + b adds the arrays element by element. **Twin logic:** Java has no arithmetic on whole arrays; write a loop that adds a[i] + b[i] for each i. (role: context)

## Errors (1)

An error edge states the rule that gets broken in a program, and the right rule.

### EarlyReturnInLoop

- **Edge:** `array_traversal` &rarr; `EarlyReturnInLoop` (error)
- **Exact edge logic (the wrong rule):** Leaves a traversal loop with return before every element has been processed.
- **Twin logic (the right rule):** A result that depends on all elements is known only after the loop ends.
- **Wrong belief (on the node):** Leaves a traversal loop with return before every element has been processed.
- **Correct rule (on the node):** A result that depends on all elements is known only after the loop ends.
- **Provenance:** textbook
- **Role of this concept:** primary

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for array traversal: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to array traversal agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

- **Edge:** `array_traversal` &rarr; `array_traversal@L0` (has_level)
- **Exact edge logic:** array traversal -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (7 ways).

Ways (7), each with its exact rule:

- **[0] everyday\_reading** (rule type E, folk-meaning rule): Folk meaning: 'go through the list' in English means look at every item once, first to last, so an array loop is assumed to process the whole array whatever its code says. Java rule: the loop visits exactly the indices its initialization, guard and update generate, in that order.
- **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `WholeArrayArithmetic`: wrong rule: a = a + b adds the arrays element by element. Right rule: Java has no arithmetic on whole arrays; write a loop that adds a[i] + b[i] for each i.
- **[2] misconception** (rule type M, wrong rule / right rule) &rarr; `IdiomOverridesCode`: wrong rule: An array loop processes the whole array from index 0 to length-1 and increments its index at the end of the body, whatever the code says. Right rule: The loop visits exactly the indices that its initialisation, guard and update produce, in the order in which its statements are written.
- **[3] misconception** (rule type M, wrong rule / right rule) &rarr; `ArrayUseScansAllCells`: wrong rule: Using an array means every cell must be scanned. Right rule: A traversal may cover only part of the array or stop early (as in a search); indexing reaches single elements directly.
- **[4] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `WholeArrayArithmetic`: Points to LT: initialize i, test, run the body with the current i, update, test again. Inconsistent application: on some passes the update is applied before the body, or a[i] is traced with the previous i. (here mixing in: "a = a + b adds the arrays element by element")
- **[5] misconception** (rule type M, wrong rule / right rule) &rarr; `OffByOneBound`: wrong rule: &lt; vs &lt;= and 0..n vs 0..n-1 are interchangeable. Right rule: for (i = 0; i &lt; n; i++) runs n times with i going up to n - 1; with &lt;= it runs n + 1 times and reaches i = n.
- **[6] misconception** (rule type M, wrong rule / right rule) &rarr; `ElementBoundToOldIndex`: wrong rule: After i changes, X[i] still refers to the element at the old value of i. Right rule: a[i] is evaluated with the current value of i each time it is used.

### L1: Unistructural / atom x text surface

L1 for array traversal: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

- **Edge:** `array_traversal` &rarr; `array_traversal@L1` (has_level)
- **Exact edge logic:** array traversal -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

Ways (2), each with its exact rule:

- **[0] names\_the\_element** (rule type N, identity rule): Identity: a traversal is a loop that steps an index through the array and performs the same operation on each element it visits.
- **[1] states\_the\_rule** (rule type S, declarative rule): Declarative: the canonical traversal is 'for (int i = 0; i &lt; a.length; i++) { ... a[i] ... }', which gives i every valid index exactly once, in increasing order; the for loop is equivalent to initialize; while (test) { body; increment; }.

### L2: Multistructural / block x execution / preoperational

L2 for array traversal: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

- **Edge:** `array_traversal` &rarr; `array_traversal@L2` (has_level)
- **Exact edge logic:** array traversal -&gt; L2 (Multistructural): the answer applies the rules of array traversal to every part of the code, in order (3 ways).

Ways (3), each with its exact rule:

- **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): Sequencing: i = 0; test i &lt; a.length; body using a[i]; i++; test; ... When i == a.length the test fails and the body is not executed, so a[a.length] is never touched.
- **[1] output\_prediction** (rule type OP, evaluation / result rule): Result: the body runs a.length times, and the result depends on the body. Squaring each element of {1, 2, 3, 4, 5} leaves {1, 4, 9, 16, 25}; summing leaves the total in the accumulator.
- **[2] one\_step\_execution** (rule type OS, state-transition rule): State transition: one pass applies the body to element i (reading or writing a[i] and possibly updating an accumulator), then i increases by 1; no other element is touched unless the body indexes it.

### L3: Relational / relations x function (concrete operational begins)

L3 for array traversal: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

- **Edge:** `array_traversal` &rarr; `array_traversal@L3` (has_level)
- **Exact edge logic:** array traversal -&gt; L3 (Relational): the answer relates the parts (9 ways).

Ways (9), each with its exact rule:

- **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): The loop variable is used as the index, so a[i] reaches a different element on each pass.
- **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): for (int x : a) is a traversal that hands the body each value a[i] and hides the index i.
- **[2] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): for (int i = 0; i &lt; a.length; i++) gives i every valid index exactly once, in increasing order; the bound must be &lt; a.length, not &lt;=.
- **[3] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): The sieve traverses isPrime[] once to set every flag to true and again at the end to count the flags still true.
- **[4] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Reversal traverses only the first half (i &lt; N/2), exchanging each a[i] with its mirror a[N-1-i].
- **[5] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Sample points are computed into x[] and y[] by one traversal and drawn by another.
- **[6] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): The running maximum is found in one traversal that keeps the largest value seen so far, starting from Double.NEGATIVE\_INFINITY.
- **[7] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): The elements are copied one at a time by a loop over every index.
- **[8] purpose\_of\_the\_whole** (rule type P, plan / role rule): Plan/role: the index is a stepper, and the loop carries out a Soloway-style plan (accumulate/sum with a gatherer, count, search, find the extreme, copy) once for each element.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for array traversal: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

- **Edge:** `array_traversal` &rarr; `array_traversal@L4` (has_level)
- **Exact edge logic:** array traversal -&gt; L4 (Extended abstract): the answer reasons beyond the given code (6 ways).

Ways (6), each with its exact rule:

- **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `WholeArrayArithmetic`: Conservation: running the index downward (a.length-1 to 0) visits the same set of elements in reverse order, harmless for a sum but not for a shift. Starting at 1 or stopping at a.length-1 drops an element. Invariant: before pass i, elements 0..i-1 have been processed.
- **[1] diagnose\_an\_error** (rule type D, error rule): rule broken: A result that depends on all elements is known only after the loop ends. Kind: silent logic error. Trigger class: a return (or break) placed inside the loop body fires on the first element, e.g. returning false/-1 in the else branch of a search, or returning the sum inside the loop
- **[2] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Applicability: use an index traversal when every element (or a contiguous range) must be processed and the index matters (writing a[i], comparing neighbours, reporting positions). Use enhanced for when only the values matter, and stop early when one element settles the answer (search).
- **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: The guard must be i &lt; a.length. Kind: run-time exception. Trigger class: i &lt;= a.length (or a body that reads a[i+1]) makes the last pass index a.length (ArrayIndexOutOfBoundsException)
- **[4] diagnose\_an\_error** (rule type D, error rule): rule broken: The traversal must cover every element it is meant to process. Kind: silent logic error. Trigger class: the loop starts at 1 or stops at a.length-1, so an end element is skipped
- **[5] diagnose\_an\_error** (rule type D, error rule): rule broken: Arithmetic operators do not apply to whole arrays. Kind: compile-time. Trigger class: a + b or a \* 2 written for arrays (bad operand types for binary operator)

## Same topic

`array_traversal` belongs to the topic **Setting array values at compile time and at run time** (`topic1.4.c`). The topic also contains: `array_initializer`, `array_reversal`, `enhanced_for`, `running_extreme`.

## Rules of the concept (26)

- **Book** (TJ-2e, p. 113 (pdf 135)): "Looping through the elements of an array is called a traversal"
- **Book** (OT-Arrays, ): "for (int i = 0; i &lt; a.length; i++) visits every valid index once: numbering begins with 0 and the built-in length property gives the size."
- **E** (folk-meaning rule): Folk meaning: 'go through the list' in English means look at every item once, first to last, so an array loop is assumed to process the whole array whatever its code says. Java rule: the loop visits exactly the indices its initialization, guard and update generate, in that order.
- **M** (wrong rule / right rule): OffByOneBound: wrong: &lt; vs &lt;= and 0..n vs 0..n-1 are interchangeable. \| right: for (i = 0; i &lt; n; i++) runs n times with i going up to n - 1; with &lt;= it runs n + 1 times and reaches i = n.
- **M** (wrong rule / right rule): WholeArrayArithmetic: wrong: a = a + b adds the arrays element by element. \| right: Java has no arithmetic on whole arrays; write a loop that adds a[i] + b[i] for each i.
- **M** (wrong rule / right rule): IdiomOverridesCode: wrong: An array loop processes the whole array from index 0 to length-1 and increments its index at the end of the body, whatever the code says. \| right: The loop visits exactly the indices that its initialisation, guard and update produce, in the order in which its statements are written.
- **M** (wrong rule / right rule): ElementBoundToOldIndex: wrong: After i changes, X[i] still refers to the element at the old value of i. \| right: a[i] is evaluated with the current value of i each time it is used.
- **M** (wrong rule / right rule): ArrayUseScansAllCells: wrong: Using an array means every cell must be scanned. \| right: A traversal may cover only part of the array or stop early (as in a search); indexing reaches single elements directly.
- **T** (uneven-application rule): Points to LT: initialize i, test, run the body with the current i, update, test again. Inconsistent application: on some passes the update is applied before the body, or a[i] is traced with the previous i.
- **N** (identity rule): Identity: a traversal is a loop that steps an index through the array and performs the same operation on each element it visits.
- **S** (declarative rule): Declarative: the canonical traversal is 'for (int i = 0; i &lt; a.length; i++) { ... a[i] ... }', which gives i every valid index exactly once, in increasing order; the for loop is equivalent to initialize; while (test) { body; increment; }.
- **LT** (operational sequencing rule): Sequencing: i = 0; test i &lt; a.length; body using a[i]; i++; test; ... When i == a.length the test fails and the body is not executed, so a[a.length] is never touched.
- **OP** (evaluation / result rule): Result: the body runs a.length times, and the result depends on the body. Squaring each element of {1, 2, 3, 4, 5} leaves {1, 4, 9, 16, 25}; summing leaves the total in the accumulator.
- **OS** (state-transition rule): State transition: one pass applies the body to element i (reading or writing a[i] and possibly updating an accumulator), then i increases by 1; no other element is touched unless the body indexes it.
- **R** (composition rule (with a neighbour)): with indexing: The loop variable is used as the index, so a[i] reaches a different element on each pass.
- **R** (composition rule (with a neighbour)): with enhanced\_for: for (int x : a) is a traversal that hands the body each value a[i] and hides the index i.
- **R** (composition rule (with a neighbour)): with for\_loop: for (int i = 0; i &lt; a.length; i++) gives i every valid index exactly once, in increasing order; the bound must be &lt; a.length, not &lt;=.
- **R** (composition rule (with a neighbour)): with boolean\_flag\_array: The sieve traverses isPrime[] once to set every flag to true and again at the end to count the flags still true.
- **R** (composition rule (with a neighbour)): with array\_reversal: Reversal traverses only the first half (i &lt; N/2), exchanging each a[i] with its mirror a[N-1-i].
- **R** (composition rule (with a neighbour)): with function\_plotting: Sample points are computed into x[] and y[] by one traversal and drawn by another.
- **R** (composition rule (with a neighbour)): with running\_extreme: The running maximum is found in one traversal that keeps the largest value seen so far, starting from Double.NEGATIVE\_INFINITY.
- **P** (plan / role rule): Plan/role: the index is a stepper, and the loop carries out a Soloway-style plan (accumulate/sum with a gatherer, count, search, find the extreme, copy) once for each element.
- **C** (conservation rule): Conservation: running the index downward (a.length-1 to 0) visits the same set of elements in reverse order, harmless for a sum but not for a shift. Starting at 1 or stopping at a.length-1 drops an element. Invariant: before pass i, elements 0..i-1 have been processed.
- **D** (error rule): rule broken: A result that depends on all elements is known only after the loop ends. (silent logic error)
- **D** (error rule): rule broken: The guard must be i &lt; a.length. (run-time exception)
- **D** (error rule): rule broken: The traversal must cover every element it is meant to process. (silent logic error)
- **D** (error rule): rule broken: Arithmetic operators do not apply to whole arrays. (compile-time)
- **X** (applicability rule): Applicability: use an index traversal when every element (or a contiguous range) must be processed and the index matters (writing a[i], comparing neighbours, reporting positions). Use enhanced for when only the values matter, and stop early when one element settles the answer (search).

## How it is found in code and answers (reader block)

- **Aliases:** none
- **Code patterns:** `\bfor\s*\([^;]*;[^;]*\.length\b`, `\bfor\s*\(\s*(?:int\s+)?(\w+)\s*=[^;]*;[^;]*;[^)]*\)\s*\{?[^{}]*?\w\s*\[\s*\1\s*\]`, `^\s*for\s*\([^;]*:[^;]*\)`, `\bwhile\s*\([^)]*\.length\b`, `\bwhile\s*\(\s*(\w+)\s*[<>]=?[^)]*\)\s*\{?[^{}]*?\w\s*\[\s*\1\s*\]`
- **Operator symbols:** none
- **Java types:** none

## The whole prerequisite chain

- **Everything it builds on (22):** `arithmetic_operators`, `array_creation`, `array_declaration`, `array_initializer`, `boolean`, `boolean_expression`, `comparison_operators`, `data_structure`, `data_type`, `do_while_loop`, `expression`, `for_loop`, `identifier`, `indexing`, `length_field`, `literal`, `logical_operators`, `loop_control`, `loop_variable`, `primitive_type`, `variable`, `while_loop`
- **Everything that builds on it (7):** `array_copy`, `array_reversal`, `boolean_flag_array`, `enhanced_for`, `function_plotting`, `running_extreme`, `standard_audio`

## Every edge in this view and its exact edge logic (37)

All the edges drawn in the picture, in the order: prerequisite, parallel, misconception, error, has_level, contains.

**1. `array_traversal` &rarr; `array_copy`** (prerequisite)

- **Exact edge logic:** The elements are copied one at a time by a loop over every index.
- **Grounding:** book\_passage
- **Composition rule (R) of `array_copy` with `array_traversal`:** The copy is a traversal of every index of the original.

**2. `array_traversal` &rarr; `array_reversal`** (prerequisite)

- **Exact edge logic:** Reversal traverses only the first half of the array (i &lt; N/2), exchanging each a[i] with its mirror a[N-1-i].
- **Grounding:** book\_passage
- **Composition rule (R) of `array_traversal` with `array_reversal`:** Reversal traverses only the first half (i &lt; N/2), exchanging each a[i] with its mirror a[N-1-i].
- **Composition rule (R) of `array_reversal` with `array_traversal`:** Reversal traverses only the first half (i &lt; N/2) while indexing the second half through the mirror index.

**3. `array_traversal` &rarr; `boolean_flag_array`** (prerequisite)

- **Exact edge logic:** The sieve traverses isPrime[] to set every flag to true and later traverses it again to count the flags that are still true.
- **Grounding:** book\_passage
- **Composition rule (R) of `array_traversal` with `boolean_flag_array`:** The sieve traverses isPrime[] once to set every flag to true and again at the end to count the flags still true.
- **Composition rule (R) of `boolean_flag_array` with `array_traversal`:** The sieve traverses isPrime[] to set every flag to true and later traverses it again to count the flags still true.

**4. `array_traversal` &rarr; `enhanced_for`** (prerequisite)

- **Exact edge logic:** for (int x : a) is a traversal that hands the body each value a[i] instead of the index i.
- **Grounding:** book\_passage
- **Composition rule (R) of `array_traversal` with `enhanced_for`:** for (int x : a) is a traversal that hands the body each value a[i] and hides the index i.
- **Composition rule (R) of `enhanced_for` with `array_traversal`:** It is a full forward traversal with the index hidden, so it cannot skip, go backward, stop at a computed index or write a[i].

**5. `array_traversal` &rarr; `function_plotting`** (prerequisite)

- **Exact edge logic:** The sample points are kept in arrays and traversed.
- **Grounding:** book\_passage
- **Composition rule (R) of `array_traversal` with `function_plotting`:** Sample points are computed into x[] and y[] by one traversal and drawn by another.
- **Composition rule (R) of `function_plotting` with `array_traversal`:** The arrays have N+1 elements (indices 0..N). The drawing loop starts at i = 1 so that x[i-1] stays in bounds; starting at 0 would access x[-1].

**6. `array_traversal` &rarr; `running_extreme`** (prerequisite)

- **Exact edge logic:** The running maximum is found by traversing the array once, keeping the largest value seen so far (starting from Double.NEGATIVE\_INFINITY).
- **Grounding:** book\_passage
- **Composition rule (R) of `array_traversal` with `running_extreme`:** The running maximum is found in one traversal that keeps the largest value seen so far, starting from Double.NEGATIVE\_INFINITY.
- **Composition rule (R) of `running_extreme` with `array_traversal`:** The maximum is found in one traversal, keeping the largest value seen so far, starting from Double.NEGATIVE\_INFINITY.

**7. `for_loop` &rarr; `array_traversal`** (prerequisite)

- **Exact edge logic:** for (int i = 0; i &lt; a.length; i++) gives i every valid index exactly once, in increasing order.
- **Grounding:** book\_passage
- **Composition rule (R) of `for_loop` with `array_traversal`:** for (int i = 0; i &lt; N; i++) gives i each valid index 0..N-1 exactly once in increasing order, the standard way to process every array element.
- **Composition rule (R) of `array_traversal` with `for_loop`:** for (int i = 0; i &lt; a.length; i++) gives i every valid index exactly once, in increasing order; the bound must be &lt; a.length, not &lt;=.

**8. `indexing` &rarr; `array_traversal`** (prerequisite)

- **Exact edge logic:** A traversal uses the loop variable i as the index, so a[i] reaches a different element on each pass.
- **Grounding:** book\_passage
- **Composition rule (R) of `indexing` with `array_traversal`:** A traversal uses the loop variable as the index, so the same expression a[i] reaches a different element on each pass.
- **Composition rule (R) of `array_traversal` with `indexing`:** The loop variable is used as the index, so a[i] reaches a different element on each pass.

**9. `length_field` &rarr; `array_traversal`** (prerequisite)

- **Exact edge logic:** A traversal loop runs its index from 0 while it is below a.length, so it visits every element once.
- **Grounding:** book\_passage

**10. `array_traversal` &rarr; `ArrayUseScansAllCells`** (misconception)

- **Exact edge logic (the wrong rule):** Using an array means every cell must be scanned.
- **Twin logic (the right rule):** Arrays allow random access: a[i] reaches one element directly, and a loop visits only the elements the task needs.
- **Role:** primary

**11. `array_traversal` &rarr; `ElementBoundToOldIndex`** (misconception)

- **Exact edge logic (the wrong rule):** After i changes, X[i] still refers to the element at the old value of i.
- **Twin logic (the right rule):** a[i] is evaluated with the current value of i each time it is used.
- **Role:** context

**12. `array_traversal` &rarr; `IdiomOverridesCode`** (misconception)

- **Exact edge logic (the wrong rule):** An array loop processes the whole array from index 0 to length-1 and increments its index at the end of the body, whatever the code says.
- **Twin logic (the right rule):** The loop visits exactly the indices that its initialisation, guard and update produce, in the order in which its statements are written.
- **Role:** primary

**13. `array_traversal` &rarr; `OffByOneBound`** (misconception)

- **Exact edge logic (the wrong rule):** &lt; vs &lt;= and 0..n vs 0..n-1 are interchangeable
- **Twin logic (the right rule):** for (i = 0; i &lt; n; i++) runs n times with i going up to n - 1; with &lt;= it runs n + 1 times and reaches i = n.
- **Role:** context

**14. `array_traversal` &rarr; `WholeArrayArithmetic`** (misconception)

- **Exact edge logic (the wrong rule):** a = a + b adds the arrays element by element.
- **Twin logic (the right rule):** Java has no arithmetic on whole arrays; write a loop that adds a[i] + b[i] for each i.
- **Role:** primary

**15. `array_bounds` &rarr; `OffByOneBound`** (misconception)

- **Exact edge logic (the wrong rule):** &lt; vs &lt;= and 0..n vs 0..n-1 are interchangeable
- **Twin logic (the right rule):** for (i = 0; i &lt; n; i++) runs n times with i going up to n - 1; with &lt;= it runs n + 1 times and reaches i = n.
- **Role:** context

**16. `array_reversal` &rarr; `OffByOneBound`** (misconception)

- **Exact edge logic (the wrong rule):** &lt; vs &lt;= and 0..n vs 0..n-1 are interchangeable
- **Twin logic (the right rule):** for (i = 0; i &lt; n; i++) runs n times with i going up to n - 1; with &lt;= it runs n + 1 times and reaches i = n.
- **Role:** context

**17. `boolean_flag_array` &rarr; `OffByOneBound`** (misconception)

- **Exact edge logic (the wrong rule):** &lt; vs &lt;= and 0..n vs 0..n-1 are interchangeable
- **Twin logic (the right rule):** for (i = 0; i &lt; n; i++) runs n times with i going up to n - 1; with &lt;= it runs n + 1 times and reaches i = n.
- **Role:** context

**18. `for_loop` &rarr; `IdiomOverridesCode`** (misconception)

- **Exact edge logic (the wrong rule):** An array loop processes the whole array from index 0 to length-1 and increments its index at the end of the body, whatever the code says.
- **Twin logic (the right rule):** The loop visits exactly the indices that its initialisation, guard and update produce, in the order in which its statements are written.
- **Role:** context

**19. `increment_operators` &rarr; `IdiomOverridesCode`** (misconception)

- **Exact edge logic (the wrong rule):** An array loop processes the whole array from index 0 to length-1 and increments its index at the end of the body, whatever the code says.
- **Twin logic (the right rule):** The loop visits exactly the indices that its initialisation, guard and update produce, in the order in which its statements are written.
- **Role:** context

**20. `indexing` &rarr; `ArrayUseScansAllCells`** (misconception)

- **Exact edge logic (the wrong rule):** Using an array means every cell must be scanned.
- **Twin logic (the right rule):** Arrays allow random access: a[i] reaches one element directly, and a loop visits only the elements the task needs.
- **Role:** context

**21. `indexing` &rarr; `ElementBoundToOldIndex`** (misconception)

- **Exact edge logic (the wrong rule):** After i changes, X[i] still refers to the element at the old value of i.
- **Twin logic (the right rule):** a[i] is evaluated with the current value of i each time it is used.
- **Role:** primary

**22. `loop_control` &rarr; `IdiomOverridesCode`** (misconception)

- **Exact edge logic (the wrong rule):** An array loop processes the whole array from index 0 to length-1 and increments its index at the end of the body, whatever the code says.
- **Twin logic (the right rule):** The loop visits exactly the indices that its initialisation, guard and update produce, in the order in which its statements are written.
- **Role:** context

**23. `loop_control` &rarr; `OffByOneBound`** (misconception)

- **Exact edge logic (the wrong rule):** i &lt; n and i &lt;= n mean the same, so the loop runs until i equals n and the last pass can use a[n].
- **Twin logic (the right rule):** for (i = 0; i &lt; n; i++) runs n times with i going up to n - 1; with &lt;= it runs n + 1 times and reaches i = n.
- **Role:** primary

**24. `matrix_operations` &rarr; `WholeArrayArithmetic`** (misconception)

- **Exact edge logic (the wrong rule):** a = a + b adds the arrays element by element.
- **Twin logic (the right rule):** Java has no arithmetic on whole arrays; write a loop that adds a[i] + b[i] for each i.
- **Role:** context

**25. `off_by_one_error` &rarr; `OffByOneBound`** (misconception)

- **Exact edge logic (the wrong rule):** &lt; vs &lt;= and 0..n vs 0..n-1 are interchangeable
- **Twin logic (the right rule):** for (i = 0; i &lt; n; i++) runs n times with i going up to n - 1; with &lt;= it runs n + 1 times and reaches i = n.
- **Role:** context

**26. `simulation_loop` &rarr; `OffByOneBound`** (misconception)

- **Exact edge logic (the wrong rule):** t &lt; T and t &lt;= T give the same number of moves.
- **Twin logic (the right rule):** for (t = 0; t &lt; T; t++) makes exactly T moves; with &lt;= it makes T + 1.
- **Role:** context

**27. `array_traversal` &rarr; `EarlyReturnInLoop`** (error)

- **Exact edge logic (the wrong rule):** Leaves a traversal loop with return before every element has been processed.
- **Twin logic (the right rule):** A result that depends on all elements is known only after the loop ends.
- **Role:** primary

**28. `array_traversal` &rarr; `array_traversal@L0`** (has_level)

- **Exact edge logic:** array traversal -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (7 ways).
  - **[0] everyday\_reading** (rule type E, folk-meaning rule): Folk meaning: 'go through the list' in English means look at every item once, first to last, so an array loop is assumed to process the whole array whatever its code says. Java rule: the loop visits exactly the indices its initialization, guard and update generate, in that order.
  - **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `WholeArrayArithmetic`: wrong rule: a = a + b adds the arrays element by element. Right rule: Java has no arithmetic on whole arrays; write a loop that adds a[i] + b[i] for each i.
  - **[2] misconception** (rule type M, wrong rule / right rule) &rarr; `IdiomOverridesCode`: wrong rule: An array loop processes the whole array from index 0 to length-1 and increments its index at the end of the body, whatever the code says. Right rule: The loop visits exactly the indices that its initialisation, guard and update produce, in the order in which its statements are written.
  - **[3] misconception** (rule type M, wrong rule / right rule) &rarr; `ArrayUseScansAllCells`: wrong rule: Using an array means every cell must be scanned. Right rule: A traversal may cover only part of the array or stop early (as in a search); indexing reaches single elements directly.
  - **[4] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `WholeArrayArithmetic`: Points to LT: initialize i, test, run the body with the current i, update, test again. Inconsistent application: on some passes the update is applied before the body, or a[i] is traced with the previous i. (here mixing in: "a = a + b adds the arrays element by element")
  - **[5] misconception** (rule type M, wrong rule / right rule) &rarr; `OffByOneBound`: wrong rule: &lt; vs &lt;= and 0..n vs 0..n-1 are interchangeable. Right rule: for (i = 0; i &lt; n; i++) runs n times with i going up to n - 1; with &lt;= it runs n + 1 times and reaches i = n.
  - **[6] misconception** (rule type M, wrong rule / right rule) &rarr; `ElementBoundToOldIndex`: wrong rule: After i changes, X[i] still refers to the element at the old value of i. Right rule: a[i] is evaluated with the current value of i each time it is used.

**29. `array_traversal` &rarr; `array_traversal@L1`** (has_level)

- **Exact edge logic:** array traversal -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).
  - **[0] names\_the\_element** (rule type N, identity rule): Identity: a traversal is a loop that steps an index through the array and performs the same operation on each element it visits.
  - **[1] states\_the\_rule** (rule type S, declarative rule): Declarative: the canonical traversal is 'for (int i = 0; i &lt; a.length; i++) { ... a[i] ... }', which gives i every valid index exactly once, in increasing order; the for loop is equivalent to initialize; while (test) { body; increment; }.

**30. `array_traversal` &rarr; `array_traversal@L2`** (has_level)

- **Exact edge logic:** array traversal -&gt; L2 (Multistructural): the answer applies the rules of array traversal to every part of the code, in order (3 ways).
  - **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): Sequencing: i = 0; test i &lt; a.length; body using a[i]; i++; test; ... When i == a.length the test fails and the body is not executed, so a[a.length] is never touched.
  - **[1] output\_prediction** (rule type OP, evaluation / result rule): Result: the body runs a.length times, and the result depends on the body. Squaring each element of {1, 2, 3, 4, 5} leaves {1, 4, 9, 16, 25}; summing leaves the total in the accumulator.
  - **[2] one\_step\_execution** (rule type OS, state-transition rule): State transition: one pass applies the body to element i (reading or writing a[i] and possibly updating an accumulator), then i increases by 1; no other element is touched unless the body indexes it.

**31. `array_traversal` &rarr; `array_traversal@L3`** (has_level)

- **Exact edge logic:** array traversal -&gt; L3 (Relational): the answer relates the parts (9 ways).
  - **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): The loop variable is used as the index, so a[i] reaches a different element on each pass.
  - **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): for (int x : a) is a traversal that hands the body each value a[i] and hides the index i.
  - **[2] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): for (int i = 0; i &lt; a.length; i++) gives i every valid index exactly once, in increasing order; the bound must be &lt; a.length, not &lt;=.
  - **[3] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): The sieve traverses isPrime[] once to set every flag to true and again at the end to count the flags still true.
  - **[4] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Reversal traverses only the first half (i &lt; N/2), exchanging each a[i] with its mirror a[N-1-i].
  - **[5] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Sample points are computed into x[] and y[] by one traversal and drawn by another.
  - **[6] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): The running maximum is found in one traversal that keeps the largest value seen so far, starting from Double.NEGATIVE\_INFINITY.
  - **[7] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): The elements are copied one at a time by a loop over every index.
  - **[8] purpose\_of\_the\_whole** (rule type P, plan / role rule): Plan/role: the index is a stepper, and the loop carries out a Soloway-style plan (accumulate/sum with a gatherer, count, search, find the extreme, copy) once for each element.

**32. `array_traversal` &rarr; `array_traversal@L4`** (has_level)

- **Exact edge logic:** array traversal -&gt; L4 (Extended abstract): the answer reasons beyond the given code (6 ways).
  - **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `WholeArrayArithmetic`: Conservation: running the index downward (a.length-1 to 0) visits the same set of elements in reverse order, harmless for a sum but not for a shift. Starting at 1 or stopping at a.length-1 drops an element. Invariant: before pass i, elements 0..i-1 have been processed.
  - **[1] diagnose\_an\_error** (rule type D, error rule): rule broken: A result that depends on all elements is known only after the loop ends. Kind: silent logic error. Trigger class: a return (or break) placed inside the loop body fires on the first element, e.g. returning false/-1 in the else branch of a search, or returning the sum inside the loop
  - **[2] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Applicability: use an index traversal when every element (or a contiguous range) must be processed and the index matters (writing a[i], comparing neighbours, reporting positions). Use enhanced for when only the values matter, and stop early when one element settles the answer (search).
  - **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: The guard must be i &lt; a.length. Kind: run-time exception. Trigger class: i &lt;= a.length (or a body that reads a[i+1]) makes the last pass index a.length (ArrayIndexOutOfBoundsException)
  - **[4] diagnose\_an\_error** (rule type D, error rule): rule broken: The traversal must cover every element it is meant to process. Kind: silent logic error. Trigger class: the loop starts at 1 or stops at a.length-1, so an end element is skipped
  - **[5] diagnose\_an\_error** (rule type D, error rule): rule broken: Arithmetic operators do not apply to whole arrays. Kind: compile-time. Trigger class: a + b or a \* 2 written for arrays (bad operand types for binary operator)

**33. `topic1.4.c` &rarr; `array_traversal`** (contains)

- topic `topic1.4.c` contains `array_traversal`

**34. `topic1.4.c` &rarr; `array_initializer`** (contains)

- topic `topic1.4.c` contains `array_initializer`

**35. `topic1.4.c` &rarr; `array_reversal`** (contains)

- topic `topic1.4.c` contains `array_reversal`

**36. `topic1.4.c` &rarr; `enhanced_for`** (contains)

- topic `topic1.4.c` contains `enhanced_for`

**37. `topic1.4.c` &rarr; `running_extreme`** (contains)

- topic `topic1.4.c` contains `running_extreme`
