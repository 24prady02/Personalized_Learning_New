# boolean_flag_array (`boolean_flag_array`)

boolean[] used to mark which values are seen (coupon collector, sieve)

Section 1.4 Arrays, topic 1.4.f Applications (coupon collector, sieve of Eratosthenes).

![The knowledge graph around boolean_flag_array](boolean_flag_array.png)

## At a glance

- **Needs first:** `array_default_values`, `array_traversal`
- **Leads to:** nothing
- **Learned alongside:** nothing
- **Misconceptions:** `NewArrayHoldsGarbage`, `OffByOneBound`
- **Errors:** none
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 18 edges around this concept. The edge logic, the wrong and right rules and the exact rules of the ways are copied word for word from the graph.

## To work on (1)

- no aliases: a student's words cannot name this concept

## What it needs first (2)

A prerequisite edge means the other concept has to be understood before `boolean_flag_array`.

### `array_default_values` comes before `boolean_flag_array`

*new slots start at 0 / false / null*

- **Edge:** `pre:array_default_values->boolean_flag_array`
- **Exact edge logic:** new boolean[n] starts every flag at false.
- **Grounding:** order\_only
- **Composition rule (R) of `boolean_flag_array` with `array_default_values`:** new boolean[n] starts every flag at false, which CouponCollector relies on; PrimeSieve needs true and so sets it with a loop.
- **Composition rule (R) of `array_default_values` with `boolean_flag_array`:** new boolean[n] starts every flag at false ('not seen yet'), so CouponCollector needs no initialization loop. PrimeSieve needs true as its start value and so must loop to set it.

### `array_traversal` comes before `boolean_flag_array`

*walking the array with an index loop*

- **Edge:** `pre:array_traversal->boolean_flag_array`
- **Exact edge logic:** The sieve traverses isPrime[] to set every flag to true and later traverses it again to count the flags that are still true.
- **Grounding:** book\_passage
- **Composition rule (R) of `boolean_flag_array` with `array_traversal`:** The sieve traverses isPrime[] to set every flag to true and later traverses it again to count the flags still true.
- **Composition rule (R) of `array_traversal` with `boolean_flag_array`:** The sieve traverses isPrime[] once to set every flag to true and again at the end to count the flags still true.

## What it leads to (0)

These concepts need `boolean_flag_array` first.

No concept has this one as a prerequisite.

## Learned alongside (0)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

No parallel edge touches this concept.

## Misconceptions (2)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### NewArrayHoldsGarbage

- **Edge:** `boolean_flag_array` &rarr; `NewArrayHoldsGarbage` (misconception)
- **Exact edge logic (the wrong rule):** The slots of a new int[n] hold unpredictable values until assigned.
- **Twin logic (the right rule):** new fills every element with a default: 0 for numeric types, false for boolean, null for String and other non-primitive types.
- **Wrong belief (on the node):** The slots of a new int[n] hold unpredictable values until assigned.
- **Correct rule (on the node):** new fills every element with a default: 0 for numeric types, false for boolean, null for String and other non-primitive types.
- **Provenance:** published
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [2] misconception, exact rule:** wrong rule: The slots of a new boolean[n] hold unpredictable values until assigned. Right rule: new boolean[n] starts every flag at false.
- **Edge `array_default_values` &rarr; `NewArrayHoldsGarbage`, exact edge logic:** The slots of a new int[n] hold unpredictable values until assigned. **Twin logic:** new fills every element with a default: 0 for numeric types, false for boolean, null for String and other non-primitive types. (role: primary)
- **Edge `primitive_type` &rarr; `NewArrayHoldsGarbage`, exact edge logic:** The slots of a new int[n] hold unpredictable values until assigned. **Twin logic:** new fills every element with a default: 0 for numeric types, false for boolean, null for String and other non-primitive types. (role: context)

### OffByOneBound

- **Edge:** `boolean_flag_array` &rarr; `OffByOneBound` (misconception)
- **Exact edge logic (the wrong rule):** &lt; vs &lt;= and 0..n vs 0..n-1 are interchangeable
- **Twin logic (the right rule):** for (i = 0; i &lt; n; i++) runs n times with i going up to n - 1; with &lt;= it runs n + 1 times and reaches i = n.
- **Wrong belief (on the node):** &lt; vs &lt;= and 0..n vs 0..n-1 are interchangeable
- **Correct rule (on the node):** for (i = 0; i &lt; n; i++) runs n times with i going up to n - 1; with &lt;= it runs n + 1 times and reaches i = n.
- **Provenance:** published
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [1] misconception, exact rule:** wrong rule: &lt; vs &lt;= and 0..n vs 0..n-1 are interchangeable. Right rule: To use the value N itself as an index, the array must have length N+1 (new boolean[N+1]), and loops over values 2..N use i &lt;= N.
- **L0 way [3] inconsistent\_trace, exact rule:** Points to LT: for each new value, test found[val] and, only if it is false, count it and set the flag. Inconsistent application: the flag is set before the test on some passes, so a new value is counted as already seen. (here mixing in: "&lt; vs &lt;= and 0..n vs 0..n-1 are interchangeable")
- **Edge `array_bounds` &rarr; `OffByOneBound`, exact edge logic:** &lt; vs &lt;= and 0..n vs 0..n-1 are interchangeable **Twin logic:** for (i = 0; i &lt; n; i++) runs n times with i going up to n - 1; with &lt;= it runs n + 1 times and reaches i = n. (role: context)
- **Edge `array_reversal` &rarr; `OffByOneBound`, exact edge logic:** &lt; vs &lt;= and 0..n vs 0..n-1 are interchangeable **Twin logic:** for (i = 0; i &lt; n; i++) runs n times with i going up to n - 1; with &lt;= it runs n + 1 times and reaches i = n. (role: context)
- **Edge `array_traversal` &rarr; `OffByOneBound`, exact edge logic:** &lt; vs &lt;= and 0..n vs 0..n-1 are interchangeable **Twin logic:** for (i = 0; i &lt; n; i++) runs n times with i going up to n - 1; with &lt;= it runs n + 1 times and reaches i = n. (role: context)
- **Edge `loop_control` &rarr; `OffByOneBound`, exact edge logic:** i &lt; n and i &lt;= n mean the same, so the loop runs until i equals n and the last pass can use a[n]. **Twin logic:** for (i = 0; i &lt; n; i++) runs n times with i going up to n - 1; with &lt;= it runs n + 1 times and reaches i = n. (role: primary)
- **Edge `off_by_one_error` &rarr; `OffByOneBound`, exact edge logic:** &lt; vs &lt;= and 0..n vs 0..n-1 are interchangeable **Twin logic:** for (i = 0; i &lt; n; i++) runs n times with i going up to n - 1; with &lt;= it runs n + 1 times and reaches i = n. (role: context)
- **Edge `simulation_loop` &rarr; `OffByOneBound`, exact edge logic:** t &lt; T and t &lt;= T give the same number of moves. **Twin logic:** for (t = 0; t &lt; T; t++) makes exactly T moves; with &lt;= it makes T + 1. (role: context)

## Errors (0)

An error edge states the rule that gets broken in a program, and the right rule.

The graph has no error edge from this concept.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for boolean flag array: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to boolean flag array agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

- **Edge:** `boolean_flag_array` &rarr; `boolean_flag_array@L0` (has_level)
- **Exact edge logic:** boolean flag array -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (4 ways).

Ways (4), each with its exact rule:

- **[0] everyday\_reading** (rule type E, folk-meaning rule): Folk meaning: using a value (a card number) as a position is not how everyday checklists work; people search a list to see whether they have seen something. Java rule: found[val] is the flag stored at index val, so one indexed read answers 'seen val?'.
- **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `OffByOneBound`: wrong rule: &lt; vs &lt;= and 0..n vs 0..n-1 are interchangeable. Right rule: To use the value N itself as an index, the array must have length N+1 (new boolean[N+1]), and loops over values 2..N use i &lt;= N.
- **[2] misconception** (rule type M, wrong rule / right rule) &rarr; `NewArrayHoldsGarbage`: wrong rule: The slots of a new boolean[n] hold unpredictable values until assigned. Right rule: new boolean[n] starts every flag at false.
- **[3] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `OffByOneBound`: Points to LT: for each new value, test found[val] and, only if it is false, count it and set the flag. Inconsistent application: the flag is set before the test on some passes, so a new value is counted as already seen. (here mixing in: "&lt; vs &lt;= and 0..n vs 0..n-1 are interchangeable")

### L1: Unistructural / atom x text surface

L1 for boolean flag array: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

- **Edge:** `boolean_flag_array` &rarr; `boolean_flag_array@L1` (has_level)
- **Exact edge logic:** boolean flag array -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

Ways (2), each with its exact rule:

- **[0] names\_the\_element** (rule type N, identity rule): Identity: a boolean array indexed by value, in which flag[v] records whether v has been seen or has a property.
- **[1] states\_the\_rule** (rule type S, declarative rule): Declarative: create boolean[] flags = new boolean[N] (all false); mark v with flags[v] = true; test with if (!flags[v]). Values must lie in 0..N-1.

### L2: Multistructural / block x execution / preoperational

L2 for boolean flag array: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

- **Edge:** `boolean_flag_array` &rarr; `boolean_flag_array@L2` (has_level)
- **Exact edge logic:** boolean flag array -&gt; L2 (Multistructural): the answer applies the rules of boolean flag array to every part of the code, in order (3 ways).

Ways (3), each with its exact rule:

- **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): Sequencing (CouponCollector): generate val, increment cardcnt, test found[val], and if it is false increment valcnt and set found[val] = true; repeat while valcnt &lt; N.
- **[1] output\_prediction** (rule type OP, evaluation / result rule): Result: the count derived from the flags, e.g. CouponCollector prints the number of cards drawn, and PrimeSieve 25 prints 9; at the end of the collector found[] is all true.
- **[2] one\_step\_execution** (rule type OS, state-transition rule): State transition: one step sets at most one flag from false to true and never back, so each element is a one-way flag.

### L3: Relational / relations x function (concrete operational begins)

L3 for boolean flag array: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

- **Edge:** `boolean_flag_array` &rarr; `boolean_flag_array@L3` (has_level)
- **Exact edge logic:** boolean flag array -&gt; L3 (Relational): the answer relates the parts (3 ways).

Ways (3), each with its exact rule:

- **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): new boolean[n] starts every flag at false, which CouponCollector relies on; PrimeSieve needs true and so sets it with a loop.
- **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): The sieve traverses isPrime[] to set every flag to true and later traverses it again to count the flags still true.
- **[2] purpose\_of\_the\_whole** (rule type P, plan / role rule): Plan/role: set membership by direct indexing. Each element is a one-way flag (Sajaniemi), and the array lets data index into the array, turning 'have I seen v?' into one step.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for boolean flag array: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

- **Edge:** `boolean_flag_array` &rarr; `boolean_flag_array@L4` (has_level)
- **Exact edge logic:** boolean flag array -&gt; L4 (Extended abstract): the answer reasons beyond the given code (5 ways).

Ways (5), each with its exact rule:

- **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `OffByOneBound`: Conservation: in CouponCollector, valcnt always equals the number of true entries in found[]. Enlarging the value range requires enlarging the array (N+1 when N itself is an index).
- **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Applicability: use a flag array when the values are small non-negative integers (card values, numbers up to N) and memory for N flags is affordable. Do not use one for huge, negative or non-integer keys.
- **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: Values used as indices must lie in 0..length-1. Kind: run-time exception. Trigger class: new boolean[N] used with value N as an index (the sieve needs N+1), or a negative value (ArrayIndexOutOfBoundsException)
- **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: A start value other than false must be set explicitly. Kind: silent logic error. Trigger class: PrimeSieve without its initial isPrime[i] = true loop: no number is ever prime, so it prints 0
- **[4] diagnose\_an\_error** (rule type D, error rule): rule broken: Test the flag before setting it. Kind: silent logic error. Trigger class: found[val] = true written before if (!found[val]), so valcnt never increases and the loop never ends

## Same topic

`boolean_flag_array` belongs to the topic **Applications (coupon collector, sieve of Eratosthenes)** (`topic1.4.f`). It is the only concept of that topic.

## Rules of the concept (17)

- **Book** (SW-1e, p. 99 (pdf 109)): "To maintain that knowledge, we use an array found[], which uses the card value as an index"
- **Book** (SW-1.4, ): "The default initial value is 0 for all numeric primitive types and false for type boolean."
- **E** (folk-meaning rule): Folk meaning: using a value (a card number) as a position is not how everyday checklists work; people search a list to see whether they have seen something. Java rule: found[val] is the flag stored at index val, so one indexed read answers 'seen val?'.
- **M** (wrong rule / right rule): NewArrayHoldsGarbage: wrong: The slots of a new boolean[n] hold unpredictable values until assigned. \| right: new boolean[n] starts every flag at false.
- **M** (wrong rule / right rule): OffByOneBound: wrong: &lt; vs &lt;= and 0..n vs 0..n-1 are interchangeable. \| right: To use the value N itself as an index, the array must have length N+1 (new boolean[N+1]), and loops over values 2..N use i &lt;= N.
- **T** (uneven-application rule): Points to LT: for each new value, test found[val] and, only if it is false, count it and set the flag. Inconsistent application: the flag is set before the test on some passes, so a new value is counted as already seen.
- **N** (identity rule): Identity: a boolean array indexed by value, in which flag[v] records whether v has been seen or has a property.
- **S** (declarative rule): Declarative: create boolean[] flags = new boolean[N] (all false); mark v with flags[v] = true; test with if (!flags[v]). Values must lie in 0..N-1.
- **LT** (operational sequencing rule): Sequencing (CouponCollector): generate val, increment cardcnt, test found[val], and if it is false increment valcnt and set found[val] = true; repeat while valcnt &lt; N.
- **OP** (evaluation / result rule): Result: the count derived from the flags, e.g. CouponCollector prints the number of cards drawn, and PrimeSieve 25 prints 9; at the end of the collector found[] is all true.
- **OS** (state-transition rule): State transition: one step sets at most one flag from false to true and never back, so each element is a one-way flag.
- **R** (composition rule (with a neighbour)): with array\_default\_values: new boolean[n] starts every flag at false, which CouponCollector relies on; PrimeSieve needs true and so sets it with a loop.
- **R** (composition rule (with a neighbour)): with array\_traversal: The sieve traverses isPrime[] to set every flag to true and later traverses it again to count the flags still true.
- **P** (plan / role rule): Plan/role: set membership by direct indexing. Each element is a one-way flag (Sajaniemi), and the array lets data index into the array, turning 'have I seen v?' into one step.
- **C** (conservation rule): Conservation: in CouponCollector, valcnt always equals the number of true entries in found[]. Enlarging the value range requires enlarging the array (N+1 when N itself is an index).
- **D** (error rule): rule broken: Values used as indices must lie in 0..length-1. (run-time exception)
- **D** (error rule): rule broken: A start value other than false must be set explicitly. (silent logic error)
- **D** (error rule): rule broken: Test the flag before setting it. (silent logic error)
- **X** (applicability rule): Applicability: use a flag array when the values are small non-negative integers (card values, numbers up to N) and memory for N flags is affordable. Do not use one for huge, negative or non-integer keys.

## How it is found in code and answers (reader block)

- **Aliases:** none
- **Code patterns:** `\bboolean\s*\[\]\s*\w+`, `\bnew\s+boolean\s*\[`, `\b\w+\s*\[[^\]]+\]\s*=\s*(?:true|false)\s*;`
- **Operator symbols:** none
- **Java types:** none

## The whole prerequisite chain

- **Everything it builds on (24):** `arithmetic_operators`, `array_creation`, `array_declaration`, `array_default_values`, `array_initializer`, `array_traversal`, `boolean`, `boolean_expression`, `comparison_operators`, `data_structure`, `data_type`, `do_while_loop`, `expression`, `for_loop`, `identifier`, `indexing`, `length_field`, `literal`, `logical_operators`, `loop_control`, `loop_variable`, `primitive_type`, `variable`, `while_loop`
- **Everything that builds on it (0):** nothing

## Every edge in this view and its exact edge logic (18)

All the edges drawn in the picture, in the order: prerequisite, parallel, misconception, error, has_level, contains.

**1. `array_default_values` &rarr; `boolean_flag_array`** (prerequisite)

- **Exact edge logic:** new boolean[n] starts every flag at false.
- **Grounding:** order\_only
- **Composition rule (R) of `array_default_values` with `boolean_flag_array`:** new boolean[n] starts every flag at false ('not seen yet'), so CouponCollector needs no initialization loop. PrimeSieve needs true as its start value and so must loop to set it.
- **Composition rule (R) of `boolean_flag_array` with `array_default_values`:** new boolean[n] starts every flag at false, which CouponCollector relies on; PrimeSieve needs true and so sets it with a loop.

**2. `array_traversal` &rarr; `boolean_flag_array`** (prerequisite)

- **Exact edge logic:** The sieve traverses isPrime[] to set every flag to true and later traverses it again to count the flags that are still true.
- **Grounding:** book\_passage
- **Composition rule (R) of `array_traversal` with `boolean_flag_array`:** The sieve traverses isPrime[] once to set every flag to true and again at the end to count the flags still true.
- **Composition rule (R) of `boolean_flag_array` with `array_traversal`:** The sieve traverses isPrime[] to set every flag to true and later traverses it again to count the flags still true.

**3. `boolean_flag_array` &rarr; `NewArrayHoldsGarbage`** (misconception)

- **Exact edge logic (the wrong rule):** The slots of a new int[n] hold unpredictable values until assigned.
- **Twin logic (the right rule):** new fills every element with a default: 0 for numeric types, false for boolean, null for String and other non-primitive types.
- **Role:** context

**4. `boolean_flag_array` &rarr; `OffByOneBound`** (misconception)

- **Exact edge logic (the wrong rule):** &lt; vs &lt;= and 0..n vs 0..n-1 are interchangeable
- **Twin logic (the right rule):** for (i = 0; i &lt; n; i++) runs n times with i going up to n - 1; with &lt;= it runs n + 1 times and reaches i = n.
- **Role:** context

**5. `array_bounds` &rarr; `OffByOneBound`** (misconception)

- **Exact edge logic (the wrong rule):** &lt; vs &lt;= and 0..n vs 0..n-1 are interchangeable
- **Twin logic (the right rule):** for (i = 0; i &lt; n; i++) runs n times with i going up to n - 1; with &lt;= it runs n + 1 times and reaches i = n.
- **Role:** context

**6. `array_default_values` &rarr; `NewArrayHoldsGarbage`** (misconception)

- **Exact edge logic (the wrong rule):** The slots of a new int[n] hold unpredictable values until assigned.
- **Twin logic (the right rule):** new fills every element with a default: 0 for numeric types, false for boolean, null for String and other non-primitive types.
- **Role:** primary

**7. `array_reversal` &rarr; `OffByOneBound`** (misconception)

- **Exact edge logic (the wrong rule):** &lt; vs &lt;= and 0..n vs 0..n-1 are interchangeable
- **Twin logic (the right rule):** for (i = 0; i &lt; n; i++) runs n times with i going up to n - 1; with &lt;= it runs n + 1 times and reaches i = n.
- **Role:** context

**8. `array_traversal` &rarr; `OffByOneBound`** (misconception)

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

**11. `primitive_type` &rarr; `NewArrayHoldsGarbage`** (misconception)

- **Exact edge logic (the wrong rule):** The slots of a new int[n] hold unpredictable values until assigned.
- **Twin logic (the right rule):** new fills every element with a default: 0 for numeric types, false for boolean, null for String and other non-primitive types.
- **Role:** context

**12. `simulation_loop` &rarr; `OffByOneBound`** (misconception)

- **Exact edge logic (the wrong rule):** t &lt; T and t &lt;= T give the same number of moves.
- **Twin logic (the right rule):** for (t = 0; t &lt; T; t++) makes exactly T moves; with &lt;= it makes T + 1.
- **Role:** context

**13. `boolean_flag_array` &rarr; `boolean_flag_array@L0`** (has_level)

- **Exact edge logic:** boolean flag array -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (4 ways).
  - **[0] everyday\_reading** (rule type E, folk-meaning rule): Folk meaning: using a value (a card number) as a position is not how everyday checklists work; people search a list to see whether they have seen something. Java rule: found[val] is the flag stored at index val, so one indexed read answers 'seen val?'.
  - **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `OffByOneBound`: wrong rule: &lt; vs &lt;= and 0..n vs 0..n-1 are interchangeable. Right rule: To use the value N itself as an index, the array must have length N+1 (new boolean[N+1]), and loops over values 2..N use i &lt;= N.
  - **[2] misconception** (rule type M, wrong rule / right rule) &rarr; `NewArrayHoldsGarbage`: wrong rule: The slots of a new boolean[n] hold unpredictable values until assigned. Right rule: new boolean[n] starts every flag at false.
  - **[3] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `OffByOneBound`: Points to LT: for each new value, test found[val] and, only if it is false, count it and set the flag. Inconsistent application: the flag is set before the test on some passes, so a new value is counted as already seen. (here mixing in: "&lt; vs &lt;= and 0..n vs 0..n-1 are interchangeable")

**14. `boolean_flag_array` &rarr; `boolean_flag_array@L1`** (has_level)

- **Exact edge logic:** boolean flag array -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).
  - **[0] names\_the\_element** (rule type N, identity rule): Identity: a boolean array indexed by value, in which flag[v] records whether v has been seen or has a property.
  - **[1] states\_the\_rule** (rule type S, declarative rule): Declarative: create boolean[] flags = new boolean[N] (all false); mark v with flags[v] = true; test with if (!flags[v]). Values must lie in 0..N-1.

**15. `boolean_flag_array` &rarr; `boolean_flag_array@L2`** (has_level)

- **Exact edge logic:** boolean flag array -&gt; L2 (Multistructural): the answer applies the rules of boolean flag array to every part of the code, in order (3 ways).
  - **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): Sequencing (CouponCollector): generate val, increment cardcnt, test found[val], and if it is false increment valcnt and set found[val] = true; repeat while valcnt &lt; N.
  - **[1] output\_prediction** (rule type OP, evaluation / result rule): Result: the count derived from the flags, e.g. CouponCollector prints the number of cards drawn, and PrimeSieve 25 prints 9; at the end of the collector found[] is all true.
  - **[2] one\_step\_execution** (rule type OS, state-transition rule): State transition: one step sets at most one flag from false to true and never back, so each element is a one-way flag.

**16. `boolean_flag_array` &rarr; `boolean_flag_array@L3`** (has_level)

- **Exact edge logic:** boolean flag array -&gt; L3 (Relational): the answer relates the parts (3 ways).
  - **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): new boolean[n] starts every flag at false, which CouponCollector relies on; PrimeSieve needs true and so sets it with a loop.
  - **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): The sieve traverses isPrime[] to set every flag to true and later traverses it again to count the flags still true.
  - **[2] purpose\_of\_the\_whole** (rule type P, plan / role rule): Plan/role: set membership by direct indexing. Each element is a one-way flag (Sajaniemi), and the array lets data index into the array, turning 'have I seen v?' into one step.

**17. `boolean_flag_array` &rarr; `boolean_flag_array@L4`** (has_level)

- **Exact edge logic:** boolean flag array -&gt; L4 (Extended abstract): the answer reasons beyond the given code (5 ways).
  - **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `OffByOneBound`: Conservation: in CouponCollector, valcnt always equals the number of true entries in found[]. Enlarging the value range requires enlarging the array (N+1 when N itself is an index).
  - **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Applicability: use a flag array when the values are small non-negative integers (card values, numbers up to N) and memory for N flags is affordable. Do not use one for huge, negative or non-integer keys.
  - **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: Values used as indices must lie in 0..length-1. Kind: run-time exception. Trigger class: new boolean[N] used with value N as an index (the sieve needs N+1), or a negative value (ArrayIndexOutOfBoundsException)
  - **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: A start value other than false must be set explicitly. Kind: silent logic error. Trigger class: PrimeSieve without its initial isPrime[i] = true loop: no number is ever prime, so it prints 0
  - **[4] diagnose\_an\_error** (rule type D, error rule): rule broken: Test the flag before setting it. Kind: silent logic error. Trigger class: found[val] = true written before if (!found[val]), so valcnt never increases and the loop never ends

**18. `topic1.4.f` &rarr; `boolean_flag_array`** (contains)

- topic `topic1.4.f` contains `boolean_flag_array`
