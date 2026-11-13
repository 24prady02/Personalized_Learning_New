# indexing (`indexing`)

a[i] -- 0-based access

Section 1.4 Arrays, topic 1.4.a Arrays in Java (declare, create, initialize; indexing; length; default values).

![The knowledge graph around indexing](indexing.png)

## At a glance

- **Needs first:** `array_creation`, `array_initializer`
- **Leads to:** `array_bounds`, `array_exchange`, `array_traversal`, `lookup_table`, `off_by_one_error`, `space_time_tradeoff`, `two_dimensional_array`
- **Learned alongside:** nothing
- **Misconceptions:** `ArrayAccessWithParentheses`, `ArrayElementNotVariable`, `ArrayIndexStartsAtOne`, `ArrayRangeInclusive`, `ArrayUseScansAllCells`, `ElementBoundToOldIndex`, `ElementNameIsWholeArray`, `IndexIsValue`
- **Errors:** none
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 36 edges around this concept. The edge logic, the wrong and right rules and the exact rules of the ways are copied word for word from the graph.

## To work on (0)

Nothing is missing for this concept.

## What it needs first (2)

A prerequisite edge means the other concept has to be understood before `indexing`.

### `array_creation` comes before `indexing`

*new int[n] -- allocates n slots*

- **Edge:** `pre:array_creation->indexing`
- **Exact edge logic:** An array must be created with new before any of its elements a[i] can be accessed.
- **Grounding:** book\_passage
- **Composition rule (R) of `indexing` with `array_creation`:** An element can be indexed only after the array is created, and the n given to new sets the valid indices 0..n-1.
- **Composition rule (R) of `array_creation` with `indexing`:** Elements can be indexed only after creation, and the n given to new fixes the valid index range 0..n-1.

### `array_initializer` comes before `indexing`

*{1, 2, 3} literal initialization*

- **Edge:** `pre:array_initializer->indexing`
- **Exact edge logic:** The values listed in braces are stored at indices 0, 1, 2, ... in order, and a[i] reads the value at index i.
- **Grounding:** spec\_passage

## What it leads to (7)

These concepts need `indexing` first.

### `indexing` comes before `array_bounds`

*valid indices are 0 .. length-1; otherwise throws*

- **Edge:** `pre:indexing->array_bounds`
- **Exact edge logic:** Valid indexes run from 0 to a.length - 1; any other index throws an exception when it is used.
- **Grounding:** book\_passage
- **Composition rule (R) of `indexing` with `array_bounds`:** Every index value is checked against 0 and a.length at run time; any other value throws.
- **Composition rule (R) of `array_bounds` with `indexing`:** Every index value used in a[i] must satisfy 0 &lt;= i &lt;= a.length-1; the last element is a[a.length-1].

### `indexing` comes before `array_exchange`

*swap a[i] and a[j] through a temporary variable*

- **Edge:** `pre:indexing->array_exchange`
- **Exact edge logic:** An exchange reads and writes a[i] and a[j] by index.
- **Grounding:** book\_passage
- **Composition rule (R) of `indexing` with `array_exchange`:** The exchange reads and writes elements only through their indices: t = a[i]; a[i] = a[j]; a[j] = t.
- **Composition rule (R) of `array_exchange` with `indexing`:** The exchange reads and writes elements only through their indices a[i] and a[j], which must both be in bounds.

### `indexing` comes before `array_traversal`

*walking the array with an index loop*

- **Edge:** `pre:indexing->array_traversal`
- **Exact edge logic:** A traversal uses the loop variable i as the index, so a[i] reaches a different element on each pass.
- **Grounding:** book\_passage
- **Composition rule (R) of `indexing` with `array_traversal`:** A traversal uses the loop variable as the index, so the same expression a[i] reaches a different element on each pass.
- **Composition rule (R) of `array_traversal` with `indexing`:** The loop variable is used as the index, so a[i] reaches a different element on each pass.

### `indexing` comes before `lookup_table`

*an array of precomputed values or names indexed by position*

- **Edge:** `pre:indexing->lookup_table`
- **Exact edge logic:** A lookup table is read by index, a[i].
- **Grounding:** book\_passage
- **Composition rule (R) of `indexing` with `lookup_table`:** A lookup table uses a data value as the index (months[m]), so the data must lie in 0..length-1.
- **Composition rule (R) of `lookup_table` with `indexing`:** The key itself is the index (months[m], rank[i]), so keys must fall in 0..length-1.

### `indexing` comes before `off_by_one_error`

*a loop or index that runs one time too many or too few (&lt; vs &lt;=, 0..n vs 1..n, length vs length-1)*

- **Edge:** `pre:indexing->off_by_one_error`
- **Exact edge logic:** Indices start at 0, so the last element is a[N-1]; misreading this convention is the usual source of off-by-one errors.
- **Grounding:** book\_passage
- **Composition rule (R) of `off_by_one_error` with `indexing`:** Because indexing starts at 0, the last valid index is length-1, and that is the bound most often missed by one.

### `indexing` comes before `space_time_tradeoff`

*Space-time tradeoff: investing memory (an array of saved values) to save computation time*

- **Edge:** `pre:indexing->space_time_tradeoff`
- **Exact edge logic:** Saved values are read back by index, H[i], instead of being recomputed.
- **Grounding:** book\_passage

### `indexing` comes before `two_dimensional_array`

*an array of arrays (a[i][j])*

- **Edge:** `pre:indexing->two_dimensional_array`
- **Exact edge logic:** A 1-D array uses one index a[i]; a 2-D array uses two, a[i][j], where the first index chooses the row array.
- **Grounding:** book\_passage
- **Composition rule (R) of `indexing` with `two_dimensional_array`:** a[i] on a 2-D array yields row i (itself a 1-D array), and a[i][j] then indexes into that row.
- **Composition rule (R) of `two_dimensional_array` with `indexing`:** A 2-D array uses two indices, and the first chooses the row array: a[i][j] is (a[i])[j].

## Learned alongside (0)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

No parallel edge touches this concept.

## Misconceptions (8)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### ArrayAccessWithParentheses

- **Edge:** `indexing` &rarr; `ArrayAccessWithParentheses` (misconception)
- **Exact edge logic (the wrong rule):** a(i) accesses element i of an array.
- **Twin logic (the right rule):** Array elements are accessed with square brackets, a[i].
- **Wrong belief (on the node):** a(i) accesses element i of an array.
- **Correct rule (on the node):** Array elements are accessed with square brackets, a[i].
- **Provenance:** published
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [4] misconception, exact rule:** wrong rule: a(i) accesses element i of an array. Right rule: Array elements are selected with square brackets, a[i]; a(i) would be a call of a method named a.

### ArrayElementNotVariable

- **Edge:** `indexing` &rarr; `ArrayElementNotVariable` (misconception)
- **Exact edge logic (the wrong rule):** An array element a[i] is not a variable, so it cannot be read into directly or used inside another index, as in a[a[i]].
- **Twin logic (the right rule):** Each element a[i] is a variable of the element type and can be used anywhere a variable of that type can, including as an index.
- **Wrong belief (on the node):** An array element a[i] is not a variable, so it cannot be read into directly or used inside another index, as in a[a[i]].
- **Correct rule (on the node):** Each element a[i] is a variable of the element type and can be used anywhere a variable of that type can, including as an index.
- **Provenance:** published
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [5] misconception, exact rule:** wrong rule: An array element a[i] is not a variable, so it cannot be read into directly or used inside another index, as in a[a[i]]. Right rule: Each element a[i] is a variable of the element type and can be used anywhere a variable of that type can, including as an index.
- **Edge `variable` &rarr; `ArrayElementNotVariable`, exact edge logic:** An array element a[i] is not a variable, so it cannot be read into directly or used inside another index, as in a[a[i]]. **Twin logic:** Each element a[i] is a variable of the element type and can be used anywhere a variable of that type can, including as an index. (role: context)

### ArrayIndexStartsAtOne

- **Edge:** `indexing` &rarr; `ArrayIndexStartsAtOne` (misconception)
- **Exact edge logic (the wrong rule):** The first element of a is a[1].
- **Twin logic (the right rule):** Numbering begins with 0; the first element is a[0].
- **Wrong belief (on the node):** The first element of a is a[1].
- **Correct rule (on the node):** Numbering begins with 0; the first element is a[0].
- **Provenance:** published
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [2] misconception, exact rule:** wrong rule: The first element of a is a[1]. Right rule: Numbering begins with 0; the first element is a[0].
- **Edge `lookup_table` &rarr; `ArrayIndexStartsAtOne`, exact edge logic:** The first element of a is a[1]. **Twin logic:** Numbering begins with 0; the first element is a[0]. (role: context)

### ArrayRangeInclusive

- **Edge:** `indexing` &rarr; `ArrayRangeInclusive` (misconception)
- **Exact edge logic (the wrong rule):** new int[n] has slots 0 to n, inclusive.
- **Twin logic (the right rule):** The slots are 0 to n - 1.
- **Wrong belief (on the node):** new int[n] has slots 0 to n, inclusive.
- **Correct rule (on the node):** The slots are 0 to n - 1.
- **Provenance:** published
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [3] misconception, exact rule:** wrong rule: new int[n] has slots 0 to n, inclusive. Right rule: The slots are 0 to n - 1.
- **Edge `array_creation` &rarr; `ArrayRangeInclusive`, exact edge logic:** new int[n] has slots 0 to n, inclusive. **Twin logic:** The slots are 0 to n - 1. (role: context)

### ArrayUseScansAllCells

- **Edge:** `indexing` &rarr; `ArrayUseScansAllCells` (misconception)
- **Exact edge logic (the wrong rule):** Using an array means every cell must be scanned.
- **Twin logic (the right rule):** Arrays allow random access: a[i] reaches one element directly, and a loop visits only the elements the task needs.
- **Wrong belief (on the node):** Using an array means every cell must be scanned.
- **Correct rule (on the node):** Arrays allow random access: a[i] reaches one element directly, and a loop visits only the elements the task needs.
- **Provenance:** published
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [9] misconception, exact rule:** wrong rule: Using an array means every cell must be scanned. Right rule: Arrays allow random access: a[i] reaches one element directly, and a loop visits only the elements the task needs.
- **Edge `array_traversal` &rarr; `ArrayUseScansAllCells`, exact edge logic:** Using an array means every cell must be scanned. **Twin logic:** Arrays allow random access: a[i] reaches one element directly, and a loop visits only the elements the task needs. (role: primary)

### ElementBoundToOldIndex

- **Edge:** `indexing` &rarr; `ElementBoundToOldIndex` (misconception)
- **Exact edge logic (the wrong rule):** After i changes, X[i] still refers to the element at the old value of i.
- **Twin logic (the right rule):** a[i] is evaluated with the current value of i each time it is used.
- **Wrong belief (on the node):** After i changes, X[i] still refers to the element at the old value of i.
- **Correct rule (on the node):** a[i] is evaluated with the current value of i each time it is used.
- **Provenance:** published
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [7] misconception, exact rule:** wrong rule: After i changes, X[i] still refers to the element at the old value of i. Right rule: a[i] is evaluated with the current value of i each time it is executed.
- **Edge `array_traversal` &rarr; `ElementBoundToOldIndex`, exact edge logic:** After i changes, X[i] still refers to the element at the old value of i. **Twin logic:** a[i] is evaluated with the current value of i each time it is used. (role: context)

### ElementNameIsWholeArray

- **Edge:** `indexing` &rarr; `ElementNameIsWholeArray` (misconception)
- **Exact edge logic (the wrong rule):** X[i] names the whole array, not one element.
- **Twin logic (the right rule):** The array is a; a[i] is the single element at index i.
- **Wrong belief (on the node):** X[i] names the whole array, not one element.
- **Correct rule (on the node):** The array is a; a[i] is the single element at index i.
- **Provenance:** published
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [6] misconception, exact rule:** wrong rule: X[i] names the whole array, not one element. Right rule: The array is a (a[] in the book); a[i] is the single element at index i.
- **Edge `array_declaration` &rarr; `ElementNameIsWholeArray`, exact edge logic:** X[i] names the whole array, not one element. **Twin logic:** The array is a; a[i] is the single element at index i. (role: context)

### IndexIsValue

- **Edge:** `indexing` &rarr; `IndexIsValue` (misconception)
- **Exact edge logic (the wrong rule):** i and a[i] are the same thing, so the position is the stored value.
- **Twin logic (the right rule):** i is a position; a[i] is the value stored at that position.
- **Wrong belief (on the node):** i and a[i] are the same thing, so the position is the stored value.
- **Correct rule (on the node):** i is a position; a[i] is the value stored at that position.
- **Provenance:** published
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [1] misconception, exact rule:** wrong rule: i and a[i] are the same thing, so the position is the stored value. Right rule: i is a position; a[i] is the value stored at that position.
- **L0 way [8] inconsistent\_trace, exact rule:** Points to LT: in a[i], a is evaluated, then i with its current value, then the bounds check, then the element is read or written. Inconsistent application: i is updated on one line, but a later a[i] is traced with the old i. (here mixing in: "i and a[i] are the same thing, so the position is the stored value")

## Errors (0)

An error edge states the rule that gets broken in a program, and the right rule.

The graph has no error edge from this concept.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for indexing: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to indexing agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

- **Edge:** `indexing` &rarr; `indexing@L0` (has_level)
- **Exact edge logic:** indexing -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (10 ways).

Ways (10), each with its exact rule:

- **[0] everyday\_reading** (rule type E, folk-meaning rule): Folk meaning: everyday counting starts at 1 (first = number 1), maths subscripts a\_1..a\_n run from 1, and f(i) with parentheses means 'apply to i'. Java rule: a[i] uses square brackets and is 0-origin, so the first element is a[0] and the last is a[a.length-1].
- **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `IndexIsValue`: wrong rule: i and a[i] are the same thing, so the position is the stored value. Right rule: i is a position; a[i] is the value stored at that position.
- **[2] misconception** (rule type M, wrong rule / right rule) &rarr; `ArrayIndexStartsAtOne`: wrong rule: The first element of a is a[1]. Right rule: Numbering begins with 0; the first element is a[0].
- **[3] misconception** (rule type M, wrong rule / right rule) &rarr; `ArrayRangeInclusive`: wrong rule: new int[n] has slots 0 to n, inclusive. Right rule: The slots are 0 to n - 1.
- **[4] misconception** (rule type M, wrong rule / right rule) &rarr; `ArrayAccessWithParentheses`: wrong rule: a(i) accesses element i of an array. Right rule: Array elements are selected with square brackets, a[i]; a(i) would be a call of a method named a.
- **[5] misconception** (rule type M, wrong rule / right rule) &rarr; `ArrayElementNotVariable`: wrong rule: An array element a[i] is not a variable, so it cannot be read into directly or used inside another index, as in a[a[i]]. Right rule: Each element a[i] is a variable of the element type and can be used anywhere a variable of that type can, including as an index.
- **[6] misconception** (rule type M, wrong rule / right rule) &rarr; `ElementNameIsWholeArray`: wrong rule: X[i] names the whole array, not one element. Right rule: The array is a (a[] in the book); a[i] is the single element at index i.
- **[7] misconception** (rule type M, wrong rule / right rule) &rarr; `ElementBoundToOldIndex`: wrong rule: After i changes, X[i] still refers to the element at the old value of i. Right rule: a[i] is evaluated with the current value of i each time it is executed.
- **[8] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `IndexIsValue`: Points to LT: in a[i], a is evaluated, then i with its current value, then the bounds check, then the element is read or written. Inconsistent application: i is updated on one line, but a later a[i] is traced with the old i. (here mixing in: "i and a[i] are the same thing, so the position is the stored value")
- **[9] misconception** (rule type M, wrong rule / right rule) &rarr; `ArrayUseScansAllCells`: wrong rule: Using an array means every cell must be scanned. Right rule: Arrays allow random access: a[i] reaches one element directly, and a loop visits only the elements the task needs.

### L1: Unistructural / atom x text surface

L1 for indexing: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

- **Edge:** `indexing` &rarr; `indexing@L1` (has_level)
- **Exact edge logic:** indexing -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

Ways (2), each with its exact rule:

- **[0] names\_the\_element** (rule type N, identity rule): Identity: an array access expression; a[i] names the single element variable at position i of the array a refers to.
- **[1] states\_the\_rule** (rule type S, declarative rule): Declarative: the index is any int-valued expression in square brackets; the valid indices of an array of length n are 0 to n-1, and an access outside that range throws ArrayIndexOutOfBoundsException.

### L2: Multistructural / block x execution / preoperational

L2 for indexing: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

- **Edge:** `indexing` &rarr; `indexing@L2` (has_level)
- **Exact edge logic:** indexing -&gt; L2 (Multistructural): the answer applies the rules of indexing to every part of the code, in order (3 ways).

Ways (3), each with its exact rule:

- **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): Sequencing: the array reference is evaluated before the index; the index expression is fully evaluated with current variable values; the bounds are checked; then the element is fetched or, on the left of =, becomes the target. In a[i] = a[j], the target a[i] is located before a[j] is read.
- **[1] output\_prediction** (rule type OP, evaluation / result rule): Result: a[i] has the element type and the value currently stored at position i. For int[] a = {5, 7, 9}, a[1] is 7 and a[0] + a[2] is 14.
- **[2] one\_step\_execution** (rule type OS, state-transition rule): State transition: reading a[i] changes nothing. a[i] = v changes only element i (i, a and all other elements are unchanged), and a[i]++ adds 1 to that one element.

### L3: Relational / relations x function (concrete operational begins)

L3 for indexing: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

- **Edge:** `indexing` &rarr; `indexing@L3` (has_level)
- **Exact edge logic:** indexing -&gt; L3 (Relational): the answer relates the parts (8 ways).

Ways (8), each with its exact rule:

- **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): An element can be indexed only after the array is created, and the n given to new sets the valid indices 0..n-1.
- **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): A traversal uses the loop variable as the index, so the same expression a[i] reaches a different element on each pass.
- **[2] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Every index value is checked against 0 and a.length at run time; any other value throws.
- **[3] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): a[i] on a 2-D array yields row i (itself a 1-D array), and a[i][j] then indexes into that row.
- **[4] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): The exchange reads and writes elements only through their indices: t = a[i]; a[i] = a[j]; a[j] = t.
- **[5] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): A lookup table uses a data value as the index (months[m]), so the data must lie in 0..length-1.
- **[6] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Indices start at 0, so the last element is a[N-1]; misreading this convention is the usual source of off-by-one errors.
- **[7] purpose\_of\_the\_whole** (rule type P, plan / role rule): Plan/role: random access, reaching any element directly by its position in constant time (address plus index), so code touches only the elements it needs.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for indexing: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

- **Edge:** `indexing` &rarr; `indexing@L4` (has_level)
- **Exact edge logic:** indexing -&gt; L4 (Extended abstract): the answer reasons beyond the given code (6 ways).

Ways (6), each with its exact rule:

- **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `IndexIsValue`: Conservation: changing the index expression (i to i+1 or i-1) shifts which element is touched and can leave the bounds at the ends. Writing a[a[i]] instead of a[i] uses an element value as the index, a different access entirely. Changing what is stored never changes the positions.
- **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Applicability: index when you need a particular element by position, or when the position is computed from data (counts[score]++, months[m]). When every value is processed in order and the position is never needed, an enhanced for loop is simpler.
- **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: The index must be in 0..a.length-1. Kind: run-time exception. Trigger class: index &lt; 0 or &gt;= a.length, e.g. a[a.length], a[i+1] on the last pass, a[i-1] at i = 0, a[0] of an empty array (ArrayIndexOutOfBoundsException)
- **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: The index must have type int (after promotion); long or double indices are rejected. Kind: compile-time. Trigger class: a[1.5], a[x] with double x, or a[n] with long n (incompatible types: possible lossy conversion)
- **[4] diagnose\_an\_error** (rule type D, error rule): rule broken: Elements are selected with brackets, not parentheses. Kind: compile-time. Trigger class: a(i) is written for a[i] (cannot find symbol: method a)
- **[5] diagnose\_an\_error** (rule type D, error rule): rule broken: An index is a position, not the stored value. Kind: silent logic error. Trigger class: code uses i where a[i] is meant (or a[i] where i is meant), e.g. returning i as the maximum value or comparing positions instead of contents

## Same topic

`indexing` belongs to the topic **Arrays in Java (declare, create, initialize; indexing; length; default values)** (`topic1.4.a`). The topic also contains: `args_length`, `array_creation`, `array_declaration`, `array_default_values`, `data_structure`, `length_field`, `off_by_one_error`.

## Rules of the concept (28)

- **Book** (SW-1e, p. 87 (pdf 97)): "We refer to each value by putting its index in brackets after the array name."
- **Book** (SW-1e, p. 86 (pdf 96)): "If we have N values, we think of them as being numbered from 0 to N"
- **Book** (OT-Arrays, ): "As shown in the preceding illustration, numbering begins with 0."
- **E** (folk-meaning rule): Folk meaning: everyday counting starts at 1 (first = number 1), maths subscripts a\_1..a\_n run from 1, and f(i) with parentheses means 'apply to i'. Java rule: a[i] uses square brackets and is 0-origin, so the first element is a[0] and the last is a[a.length-1].
- **M** (wrong rule / right rule): ArrayAccessWithParentheses: wrong: a(i) accesses element i of an array. \| right: Array elements are selected with square brackets, a[i]; a(i) would be a call of a method named a.
- **M** (wrong rule / right rule): ArrayIndexStartsAtOne: wrong: The first element of a is a[1]. \| right: Numbering begins with 0; the first element is a[0].
- **M** (wrong rule / right rule): ArrayRangeInclusive: wrong: new int[n] has slots 0 to n, inclusive. \| right: The slots are 0 to n - 1.
- **M** (wrong rule / right rule): IndexIsValue: wrong: i and a[i] are the same thing, so the position is the stored value. \| right: i is a position; a[i] is the value stored at that position.
- **M** (wrong rule / right rule): ArrayElementNotVariable: wrong: An array element a[i] is not a variable, so it cannot be read into directly or used inside another index, as in a[a[i]]. \| right: Each element a[i] is a variable of the element type and can be used anywhere a variable of that type can, including as an index.
- **M** (wrong rule / right rule): ElementNameIsWholeArray: wrong: X[i] names the whole array, not one element. \| right: The array is a (a[] in the book); a[i] is the single element at index i.
- **M** (wrong rule / right rule): ElementBoundToOldIndex: wrong: After i changes, X[i] still refers to the element at the old value of i. \| right: a[i] is evaluated with the current value of i each time it is executed.
- **M** (wrong rule / right rule): ArrayUseScansAllCells: wrong: Using an array means every cell must be scanned. \| right: Arrays allow random access: a[i] reaches one element directly, and a loop visits only the elements the task needs.
- **T** (uneven-application rule): Points to LT: in a[i], a is evaluated, then i with its current value, then the bounds check, then the element is read or written. Inconsistent application: i is updated on one line, but a later a[i] is traced with the old i.
- **N** (identity rule): Identity: an array access expression; a[i] names the single element variable at position i of the array a refers to.
- **S** (declarative rule): Declarative: the index is any int-valued expression in square brackets; the valid indices of an array of length n are 0 to n-1, and an access outside that range throws ArrayIndexOutOfBoundsException.
- **LT** (operational sequencing rule): Sequencing: the array reference is evaluated before the index; the index expression is fully evaluated with current variable values; the bounds are checked; then the element is fetched or, on the left of =, becomes the target. In a[i] = a[j], the target a[i] is located before a[j] is read.
- **OP** (evaluation / result rule): Result: a[i] has the element type and the value currently stored at position i. For int[] a = {5, 7, 9}, a[1] is 7 and a[0] + a[2] is 14.
- **OS** (state-transition rule): State transition: reading a[i] changes nothing. a[i] = v changes only element i (i, a and all other elements are unchanged), and a[i]++ adds 1 to that one element.
- **R** (composition rule (with a neighbour)): with array\_creation: An element can be indexed only after the array is created, and the n given to new sets the valid indices 0..n-1.
- **R** (composition rule (with a neighbour)): with array\_traversal: A traversal uses the loop variable as the index, so the same expression a[i] reaches a different element on each pass.
- **R** (composition rule (with a neighbour)): with array\_bounds: Every index value is checked against 0 and a.length at run time; any other value throws.
- **R** (composition rule (with a neighbour)): with two\_dimensional\_array: a[i] on a 2-D array yields row i (itself a 1-D array), and a[i][j] then indexes into that row.
- **R** (composition rule (with a neighbour)): with array\_exchange: The exchange reads and writes elements only through their indices: t = a[i]; a[i] = a[j]; a[j] = t.
- **R** (composition rule (with a neighbour)): with lookup\_table: A lookup table uses a data value as the index (months[m]), so the data must lie in 0..length-1.
- **P** (plan / role rule): Plan/role: random access, reaching any element directly by its position in constant time (address plus index), so code touches only the elements it needs.
- **C** (conservation rule): Conservation: changing the index expression (i to i+1 or i-1) shifts which element is touched and can leave the bounds at the ends. Writing a[a[i]] instead of a[i] uses an element value as the index, a different access entirely. Changing what is stored never changes the positions.
- **D** (error rule): rule broken: The index must be in 0..a.length-1. (run-time exception)
- **D** (error rule): rule broken: The index must have type int (after promotion); long or double indices are rejected. (compile-time)
- **D** (error rule): rule broken: Elements are selected with brackets, not parentheses. (compile-time)
- **D** (error rule): rule broken: An index is a position, not the stored value. (silent logic error)
- **X** (applicability rule): Applicability: index when you need a particular element by position, or when the position is computed from data (counts[score]++, months[m]). When every value is processed in order and the position is never needed, an enhanced for loop is simpler.

## How it is found in code and answers (reader block)

- **Aliases:** index, indices, indexing
- **Code patterns:** `\w\s*\[[^\]]+\]`
- **Operator symbols:** none
- **Java types:** none
- **Signal index\_from\_length** (scope statement, decisive): `(\w+)\s*\[\s*\1\s*\.\s*length\s*-\s*\d+\s*\]`

## The whole prerequisite chain

- **Everything it builds on (5):** `array_creation`, `array_declaration`, `array_initializer`, `data_structure`, `data_type`
- **Everything that builds on it (33):** `array_bounds`, `array_copy`, `array_exchange`, `array_reversal`, `array_traversal`, `boolean_flag_array`, `convergence_rate`, `dangling_pages`, `enhanced_for`, `frequency_counting`, `function_plotting`, `input_graph`, `lookup_table`, `loop_guard`, `markov_chain`, `matrix_operations`, `multidimensional_array`, `normalization`, `off_by_one_error`, `power_method`, `ragged_array`, `random_move`, `row_major_order`, `run_time_error`, `running_extreme`, `sampling_without_replacement`, `shuffle`, `simulation_loop`, `space_time_tradeoff`, `standard_audio`, `transition_matrix`, `two_dimensional_array`, `two_models`

## Every edge in this view and its exact edge logic (36)

All the edges drawn in the picture, in the order: prerequisite, parallel, misconception, error, has_level, contains.

**1. `array_creation` &rarr; `indexing`** (prerequisite)

- **Exact edge logic:** An array must be created with new before any of its elements a[i] can be accessed.
- **Grounding:** book\_passage
- **Composition rule (R) of `array_creation` with `indexing`:** Elements can be indexed only after creation, and the n given to new fixes the valid index range 0..n-1.
- **Composition rule (R) of `indexing` with `array_creation`:** An element can be indexed only after the array is created, and the n given to new sets the valid indices 0..n-1.

**2. `array_initializer` &rarr; `indexing`** (prerequisite)

- **Exact edge logic:** The values listed in braces are stored at indices 0, 1, 2, ... in order, and a[i] reads the value at index i.
- **Grounding:** spec\_passage

**3. `indexing` &rarr; `array_bounds`** (prerequisite)

- **Exact edge logic:** Valid indexes run from 0 to a.length - 1; any other index throws an exception when it is used.
- **Grounding:** book\_passage
- **Composition rule (R) of `indexing` with `array_bounds`:** Every index value is checked against 0 and a.length at run time; any other value throws.
- **Composition rule (R) of `array_bounds` with `indexing`:** Every index value used in a[i] must satisfy 0 &lt;= i &lt;= a.length-1; the last element is a[a.length-1].

**4. `indexing` &rarr; `array_exchange`** (prerequisite)

- **Exact edge logic:** An exchange reads and writes a[i] and a[j] by index.
- **Grounding:** book\_passage
- **Composition rule (R) of `indexing` with `array_exchange`:** The exchange reads and writes elements only through their indices: t = a[i]; a[i] = a[j]; a[j] = t.
- **Composition rule (R) of `array_exchange` with `indexing`:** The exchange reads and writes elements only through their indices a[i] and a[j], which must both be in bounds.

**5. `indexing` &rarr; `array_traversal`** (prerequisite)

- **Exact edge logic:** A traversal uses the loop variable i as the index, so a[i] reaches a different element on each pass.
- **Grounding:** book\_passage
- **Composition rule (R) of `indexing` with `array_traversal`:** A traversal uses the loop variable as the index, so the same expression a[i] reaches a different element on each pass.
- **Composition rule (R) of `array_traversal` with `indexing`:** The loop variable is used as the index, so a[i] reaches a different element on each pass.

**6. `indexing` &rarr; `lookup_table`** (prerequisite)

- **Exact edge logic:** A lookup table is read by index, a[i].
- **Grounding:** book\_passage
- **Composition rule (R) of `indexing` with `lookup_table`:** A lookup table uses a data value as the index (months[m]), so the data must lie in 0..length-1.
- **Composition rule (R) of `lookup_table` with `indexing`:** The key itself is the index (months[m], rank[i]), so keys must fall in 0..length-1.

**7. `indexing` &rarr; `off_by_one_error`** (prerequisite)

- **Exact edge logic:** Indices start at 0, so the last element is a[N-1]; misreading this convention is the usual source of off-by-one errors.
- **Grounding:** book\_passage
- **Composition rule (R) of `off_by_one_error` with `indexing`:** Because indexing starts at 0, the last valid index is length-1, and that is the bound most often missed by one.

**8. `indexing` &rarr; `space_time_tradeoff`** (prerequisite)

- **Exact edge logic:** Saved values are read back by index, H[i], instead of being recomputed.
- **Grounding:** book\_passage

**9. `indexing` &rarr; `two_dimensional_array`** (prerequisite)

- **Exact edge logic:** A 1-D array uses one index a[i]; a 2-D array uses two, a[i][j], where the first index chooses the row array.
- **Grounding:** book\_passage
- **Composition rule (R) of `indexing` with `two_dimensional_array`:** a[i] on a 2-D array yields row i (itself a 1-D array), and a[i][j] then indexes into that row.
- **Composition rule (R) of `two_dimensional_array` with `indexing`:** A 2-D array uses two indices, and the first chooses the row array: a[i][j] is (a[i])[j].

**10. `indexing` &rarr; `ArrayAccessWithParentheses`** (misconception)

- **Exact edge logic (the wrong rule):** a(i) accesses element i of an array.
- **Twin logic (the right rule):** Array elements are accessed with square brackets, a[i].
- **Role:** primary

**11. `indexing` &rarr; `ArrayElementNotVariable`** (misconception)

- **Exact edge logic (the wrong rule):** An array element a[i] is not a variable, so it cannot be read into directly or used inside another index, as in a[a[i]].
- **Twin logic (the right rule):** Each element a[i] is a variable of the element type and can be used anywhere a variable of that type can, including as an index.
- **Role:** primary

**12. `indexing` &rarr; `ArrayIndexStartsAtOne`** (misconception)

- **Exact edge logic (the wrong rule):** The first element of a is a[1].
- **Twin logic (the right rule):** Numbering begins with 0; the first element is a[0].
- **Role:** primary

**13. `indexing` &rarr; `ArrayRangeInclusive`** (misconception)

- **Exact edge logic (the wrong rule):** new int[n] has slots 0 to n, inclusive.
- **Twin logic (the right rule):** The slots are 0 to n - 1.
- **Role:** primary

**14. `indexing` &rarr; `ArrayUseScansAllCells`** (misconception)

- **Exact edge logic (the wrong rule):** Using an array means every cell must be scanned.
- **Twin logic (the right rule):** Arrays allow random access: a[i] reaches one element directly, and a loop visits only the elements the task needs.
- **Role:** context

**15. `indexing` &rarr; `ElementBoundToOldIndex`** (misconception)

- **Exact edge logic (the wrong rule):** After i changes, X[i] still refers to the element at the old value of i.
- **Twin logic (the right rule):** a[i] is evaluated with the current value of i each time it is used.
- **Role:** primary

**16. `indexing` &rarr; `ElementNameIsWholeArray`** (misconception)

- **Exact edge logic (the wrong rule):** X[i] names the whole array, not one element.
- **Twin logic (the right rule):** The array is a; a[i] is the single element at index i.
- **Role:** primary

**17. `indexing` &rarr; `IndexIsValue`** (misconception)

- **Exact edge logic (the wrong rule):** i and a[i] are the same thing, so the position is the stored value.
- **Twin logic (the right rule):** i is a position; a[i] is the value stored at that position.
- **Role:** primary

**18. `array_creation` &rarr; `ArrayRangeInclusive`** (misconception)

- **Exact edge logic (the wrong rule):** new int[n] has slots 0 to n, inclusive.
- **Twin logic (the right rule):** The slots are 0 to n - 1.
- **Role:** context

**19. `array_declaration` &rarr; `ElementNameIsWholeArray`** (misconception)

- **Exact edge logic (the wrong rule):** X[i] names the whole array, not one element.
- **Twin logic (the right rule):** The array is a; a[i] is the single element at index i.
- **Role:** context

**20. `array_traversal` &rarr; `ArrayUseScansAllCells`** (misconception)

- **Exact edge logic (the wrong rule):** Using an array means every cell must be scanned.
- **Twin logic (the right rule):** Arrays allow random access: a[i] reaches one element directly, and a loop visits only the elements the task needs.
- **Role:** primary

**21. `array_traversal` &rarr; `ElementBoundToOldIndex`** (misconception)

- **Exact edge logic (the wrong rule):** After i changes, X[i] still refers to the element at the old value of i.
- **Twin logic (the right rule):** a[i] is evaluated with the current value of i each time it is used.
- **Role:** context

**22. `lookup_table` &rarr; `ArrayIndexStartsAtOne`** (misconception)

- **Exact edge logic (the wrong rule):** The first element of a is a[1].
- **Twin logic (the right rule):** Numbering begins with 0; the first element is a[0].
- **Role:** context

**23. `variable` &rarr; `ArrayElementNotVariable`** (misconception)

- **Exact edge logic (the wrong rule):** An array element a[i] is not a variable, so it cannot be read into directly or used inside another index, as in a[a[i]].
- **Twin logic (the right rule):** Each element a[i] is a variable of the element type and can be used anywhere a variable of that type can, including as an index.
- **Role:** context

**24. `indexing` &rarr; `indexing@L0`** (has_level)

- **Exact edge logic:** indexing -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (10 ways).
  - **[0] everyday\_reading** (rule type E, folk-meaning rule): Folk meaning: everyday counting starts at 1 (first = number 1), maths subscripts a\_1..a\_n run from 1, and f(i) with parentheses means 'apply to i'. Java rule: a[i] uses square brackets and is 0-origin, so the first element is a[0] and the last is a[a.length-1].
  - **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `IndexIsValue`: wrong rule: i and a[i] are the same thing, so the position is the stored value. Right rule: i is a position; a[i] is the value stored at that position.
  - **[2] misconception** (rule type M, wrong rule / right rule) &rarr; `ArrayIndexStartsAtOne`: wrong rule: The first element of a is a[1]. Right rule: Numbering begins with 0; the first element is a[0].
  - **[3] misconception** (rule type M, wrong rule / right rule) &rarr; `ArrayRangeInclusive`: wrong rule: new int[n] has slots 0 to n, inclusive. Right rule: The slots are 0 to n - 1.
  - **[4] misconception** (rule type M, wrong rule / right rule) &rarr; `ArrayAccessWithParentheses`: wrong rule: a(i) accesses element i of an array. Right rule: Array elements are selected with square brackets, a[i]; a(i) would be a call of a method named a.
  - **[5] misconception** (rule type M, wrong rule / right rule) &rarr; `ArrayElementNotVariable`: wrong rule: An array element a[i] is not a variable, so it cannot be read into directly or used inside another index, as in a[a[i]]. Right rule: Each element a[i] is a variable of the element type and can be used anywhere a variable of that type can, including as an index.
  - **[6] misconception** (rule type M, wrong rule / right rule) &rarr; `ElementNameIsWholeArray`: wrong rule: X[i] names the whole array, not one element. Right rule: The array is a (a[] in the book); a[i] is the single element at index i.
  - **[7] misconception** (rule type M, wrong rule / right rule) &rarr; `ElementBoundToOldIndex`: wrong rule: After i changes, X[i] still refers to the element at the old value of i. Right rule: a[i] is evaluated with the current value of i each time it is executed.
  - **[8] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `IndexIsValue`: Points to LT: in a[i], a is evaluated, then i with its current value, then the bounds check, then the element is read or written. Inconsistent application: i is updated on one line, but a later a[i] is traced with the old i. (here mixing in: "i and a[i] are the same thing, so the position is the stored value")
  - **[9] misconception** (rule type M, wrong rule / right rule) &rarr; `ArrayUseScansAllCells`: wrong rule: Using an array means every cell must be scanned. Right rule: Arrays allow random access: a[i] reaches one element directly, and a loop visits only the elements the task needs.

**25. `indexing` &rarr; `indexing@L1`** (has_level)

- **Exact edge logic:** indexing -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).
  - **[0] names\_the\_element** (rule type N, identity rule): Identity: an array access expression; a[i] names the single element variable at position i of the array a refers to.
  - **[1] states\_the\_rule** (rule type S, declarative rule): Declarative: the index is any int-valued expression in square brackets; the valid indices of an array of length n are 0 to n-1, and an access outside that range throws ArrayIndexOutOfBoundsException.

**26. `indexing` &rarr; `indexing@L2`** (has_level)

- **Exact edge logic:** indexing -&gt; L2 (Multistructural): the answer applies the rules of indexing to every part of the code, in order (3 ways).
  - **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): Sequencing: the array reference is evaluated before the index; the index expression is fully evaluated with current variable values; the bounds are checked; then the element is fetched or, on the left of =, becomes the target. In a[i] = a[j], the target a[i] is located before a[j] is read.
  - **[1] output\_prediction** (rule type OP, evaluation / result rule): Result: a[i] has the element type and the value currently stored at position i. For int[] a = {5, 7, 9}, a[1] is 7 and a[0] + a[2] is 14.
  - **[2] one\_step\_execution** (rule type OS, state-transition rule): State transition: reading a[i] changes nothing. a[i] = v changes only element i (i, a and all other elements are unchanged), and a[i]++ adds 1 to that one element.

**27. `indexing` &rarr; `indexing@L3`** (has_level)

- **Exact edge logic:** indexing -&gt; L3 (Relational): the answer relates the parts (8 ways).
  - **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): An element can be indexed only after the array is created, and the n given to new sets the valid indices 0..n-1.
  - **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): A traversal uses the loop variable as the index, so the same expression a[i] reaches a different element on each pass.
  - **[2] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Every index value is checked against 0 and a.length at run time; any other value throws.
  - **[3] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): a[i] on a 2-D array yields row i (itself a 1-D array), and a[i][j] then indexes into that row.
  - **[4] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): The exchange reads and writes elements only through their indices: t = a[i]; a[i] = a[j]; a[j] = t.
  - **[5] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): A lookup table uses a data value as the index (months[m]), so the data must lie in 0..length-1.
  - **[6] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Indices start at 0, so the last element is a[N-1]; misreading this convention is the usual source of off-by-one errors.
  - **[7] purpose\_of\_the\_whole** (rule type P, plan / role rule): Plan/role: random access, reaching any element directly by its position in constant time (address plus index), so code touches only the elements it needs.

**28. `indexing` &rarr; `indexing@L4`** (has_level)

- **Exact edge logic:** indexing -&gt; L4 (Extended abstract): the answer reasons beyond the given code (6 ways).
  - **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `IndexIsValue`: Conservation: changing the index expression (i to i+1 or i-1) shifts which element is touched and can leave the bounds at the ends. Writing a[a[i]] instead of a[i] uses an element value as the index, a different access entirely. Changing what is stored never changes the positions.
  - **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Applicability: index when you need a particular element by position, or when the position is computed from data (counts[score]++, months[m]). When every value is processed in order and the position is never needed, an enhanced for loop is simpler.
  - **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: The index must be in 0..a.length-1. Kind: run-time exception. Trigger class: index &lt; 0 or &gt;= a.length, e.g. a[a.length], a[i+1] on the last pass, a[i-1] at i = 0, a[0] of an empty array (ArrayIndexOutOfBoundsException)
  - **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: The index must have type int (after promotion); long or double indices are rejected. Kind: compile-time. Trigger class: a[1.5], a[x] with double x, or a[n] with long n (incompatible types: possible lossy conversion)
  - **[4] diagnose\_an\_error** (rule type D, error rule): rule broken: Elements are selected with brackets, not parentheses. Kind: compile-time. Trigger class: a(i) is written for a[i] (cannot find symbol: method a)
  - **[5] diagnose\_an\_error** (rule type D, error rule): rule broken: An index is a position, not the stored value. Kind: silent logic error. Trigger class: code uses i where a[i] is meant (or a[i] where i is meant), e.g. returning i as the maximum value or comparing positions instead of contents

**29. `topic1.4.a` &rarr; `indexing`** (contains)

- topic `topic1.4.a` contains `indexing`

**30. `topic1.4.a` &rarr; `args_length`** (contains)

- topic `topic1.4.a` contains `args_length`

**31. `topic1.4.a` &rarr; `array_creation`** (contains)

- topic `topic1.4.a` contains `array_creation`

**32. `topic1.4.a` &rarr; `array_declaration`** (contains)

- topic `topic1.4.a` contains `array_declaration`

**33. `topic1.4.a` &rarr; `array_default_values`** (contains)

- topic `topic1.4.a` contains `array_default_values`

**34. `topic1.4.a` &rarr; `data_structure`** (contains)

- topic `topic1.4.a` contains `data_structure`

**35. `topic1.4.a` &rarr; `length_field`** (contains)

- topic `topic1.4.a` contains `length_field`

**36. `topic1.4.a` &rarr; `off_by_one_error`** (contains)

- topic `topic1.4.a` contains `off_by_one_error`
