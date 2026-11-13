# exclusive_or (`exclusive_or`)

^ on booleans is true when the operands differ

Section 1.2 Built-in Types of Data, topic 1.2.e Booleans.

![The knowledge graph around exclusive_or](exclusive_or.png)

## At a glance

- **Needs first:** `logical_operators`
- **Leads to:** nothing
- **Learned alongside:** nothing
- **Misconceptions:** `CaretIsPower`
- **Errors:** none
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 14 edges around this concept. The edge logic, the wrong and right rules and the exact rules of the ways are copied word for word from the graph.

## To work on (1)

- no aliases: a student's words cannot name this concept

## What it needs first (1)

A prerequisite edge means the other concept has to be understood before `exclusive_or`.

### `logical_operators` comes before `exclusive_or`

*&amp;&amp; \|\| !*

- **Edge:** `pre:logical_operators->exclusive_or`
- **Exact edge logic:** ^ on booleans is another logical operator, defined by a truth table like &amp;&amp;, \|\| and !: true exactly when its operands differ.
- **Grounding:** order\_only
- **Composition rule (R) of `exclusive_or` with `logical_operators`:** ^ belongs with &amp;&amp;, \|\| and ! as a boolean operator defined by a truth table, but it is not short-circuit and it binds tighter than &amp;&amp; and \|\|; a ^ b equals (a \|\| b) &amp;&amp; !(a &amp;&amp; b).
- **Composition rule (R) of `logical_operators` with `exclusive_or`:** ^ on booleans is a further logical operator, true exactly when the operands differ (it equals (a \|\| b) &amp;&amp; !(a &amp;&amp; b)), but unlike &amp;&amp; and \|\| it always evaluates both operands.

## What it leads to (0)

These concepts need `exclusive_or` first.

No concept has this one as a prerequisite.

## Learned alongside (0)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

No parallel edge touches this concept.

## Misconceptions (1)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### CaretIsPower

- **Edge:** `exclusive_or` &rarr; `CaretIsPower` (misconception)
- **Exact edge logic (the wrong rule):** a^2 computes a squared.
- **Twin logic (the right rule):** Java has no exponent operator; ^ is exclusive or, and a \* a or Math.pow(a, 2) computes a squared.
- **Wrong belief (on the node):** a^2 computes a squared.
- **Correct rule (on the node):** Java has no exponent operator; ^ is exclusive or, and a \* a or Math.pow(a, 2) computes a squared.
- **Provenance:** textbook
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [1] misconception, exact rule:** wrong rule: a^2 computes a squared. Right rule: Java has no exponent operator; ^ is exclusive or, and a \* a or Math.pow(a, 2) computes a squared.
- **L0 way [2] inconsistent\_trace, exact rule:** Points to LT (both operands are evaluated, then compared: true if they differ). Applied unevenly: in the true/true row of a truth table the student gives true (treating ^ like \|\|) while the other rows are right. (here mixing in: "a^2 computes a squared")
- **Edge `arithmetic_operators` &rarr; `CaretIsPower`, exact edge logic:** a^2 computes a squared. **Twin logic:** Java has no exponent operator; ^ is exclusive or, and a \* a or Math.pow(a, 2) computes a squared. (role: primary)

## Errors (0)

An error edge states the rule that gets broken in a program, and the right rule.

The graph has no error edge from this concept.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for exclusive or: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to exclusive or agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

- **Edge:** `exclusive_or` &rarr; `exclusive_or@L0` (has_level)
- **Exact edge logic:** exclusive or -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (3 ways).

Ways (3), each with its exact rule:

- **[0] everyday\_reading** (rule type E, folk-meaning rule): Folk meaning: on calculators, in spreadsheets and in typed maths ^ means 'to the power of', so a^2 is a squared. Java rule: ^ is exclusive or (bitwise on ints), there is no exponent operator, and 10^6 is 12.
- **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `CaretIsPower`: wrong rule: a^2 computes a squared. Right rule: Java has no exponent operator; ^ is exclusive or, and a \* a or Math.pow(a, 2) computes a squared.
- **[2] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `CaretIsPower`: Points to LT (both operands are evaluated, then compared: true if they differ). Applied unevenly: in the true/true row of a truth table the student gives true (treating ^ like \|\|) while the other rows are right. (here mixing in: "a^2 computes a squared")

### L1: Unistructural / atom x text surface

L1 for exclusive or: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

- **Edge:** `exclusive_or` &rarr; `exclusive_or@L1` (has_level)
- **Exact edge logic:** exclusive or -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

Ways (2), each with its exact rule:

- **[0] names\_the\_element** (rule type N, identity rule): ^ applied to boolean operands is the exclusive-or logical operator.
- **[1] states\_the\_rule** (rule type S, declarative rule): For booleans, a ^ b is true if a and b are different and false if they are the same (equivalent to a != b); both operands are always evaluated.

### L2: Multistructural / block x execution / preoperational

L2 for exclusive or: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

- **Edge:** `exclusive_or` &rarr; `exclusive_or@L2` (has_level)
- **Exact edge logic:** exclusive or -&gt; L2 (Multistructural): the answer applies the rules of exclusive or to every part of the code, in order (3 ways).

Ways (3), each with its exact rule:

- **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): Evaluate the left operand, then the right operand (always, no short-circuit), then compare them.
- **[1] output\_prediction** (rule type OP, evaluation / result rule): Boolean result: true ^ true is false, true ^ false is true, false ^ false is false; with int operands ^ gives an int bitwise result, so 10 ^ 6 is 12.
- **[2] one\_step\_execution** (rule type OS, state-transition rule): ^ changes no variable; flag = flag ^ true stores the opposite value, toggling the flag.

### L3: Relational / relations x function (concrete operational begins)

L3 for exclusive or: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

- **Edge:** `exclusive_or` &rarr; `exclusive_or@L3` (has_level)
- **Exact edge logic:** exclusive or -&gt; L3 (Relational): the answer relates the parts (2 ways).

Ways (2), each with its exact rule:

- **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): ^ belongs with &amp;&amp;, \|\| and ! as a boolean operator defined by a truth table, but it is not short-circuit and it binds tighter than &amp;&amp; and \|\|; a ^ b equals (a \|\| b) &amp;&amp; !(a &amp;&amp; b).
- **[1] purpose\_of\_the\_whole** (rule type P, plan / role rule): Expresses 'exactly one of two conditions' (e.g. exactly one of two coordinates is negative) or toggles a parity flag.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for exclusive or: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

- **Edge:** `exclusive_or` &rarr; `exclusive_or@L4` (has_level)
- **Exact edge logic:** exclusive or -&gt; L4 (Extended abstract): the answer reasons beyond the given code (3 ways).

Ways (3), each with its exact rule:

- **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `CaretIsPower`: Swapping the operands keeps the value (^ is commutative), and applying ^ b twice restores the original value ((a ^ b) ^ b == a), so xor with a fixed operand is reversible.
- **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Use ^ (or the clearer a != b) when the test is 'the two conditions differ'; never use ^ for powers (use multiplication, Math.pow, or e-notation literals such as 1e6).
- **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: ^ is exclusive or, not exponentiation. Kind: silent logic error. Trigger class: Writing x^2 or 10^n with int operands: it compiles and computes a bitwise xor (10^6 is 12); with double operands such as 2.0^2 it is a compile-time error instead.

## Same topic

`exclusive_or` belongs to the topic **Booleans** (`topic1.2.e`). The topic also contains: `boolean`, `boolean_expression`, `de_morgan`, `logical_operators`, `short_circuit`.

## Rules of the concept (13)

- **Book** (SW-1e, p. 39 (pdf 49)): "The exclusive or operator ^ for boolean operands is defined to be true if they are different, false if they are the same."
- **Book** (SW-1.2, p. 39 (pdf 49)): "The exclusive or operator ^ for boolean operands is defined to be true if they are different, false if they are the same."
- **E** (folk-meaning rule): Folk meaning: on calculators, in spreadsheets and in typed maths ^ means 'to the power of', so a^2 is a squared. Java rule: ^ is exclusive or (bitwise on ints), there is no exponent operator, and 10^6 is 12.
- **M** (wrong rule / right rule): CaretIsPower: wrong: a^2 computes a squared. \| right: Java has no exponent operator; ^ is exclusive or, and a \* a or Math.pow(a, 2) computes a squared.
- **T** (uneven-application rule): Points to LT (both operands are evaluated, then compared: true if they differ). Applied unevenly: in the true/true row of a truth table the student gives true (treating ^ like \|\|) while the other rows are right.
- **N** (identity rule): ^ applied to boolean operands is the exclusive-or logical operator.
- **S** (declarative rule): For booleans, a ^ b is true if a and b are different and false if they are the same (equivalent to a != b); both operands are always evaluated.
- **LT** (operational sequencing rule): Evaluate the left operand, then the right operand (always, no short-circuit), then compare them.
- **OP** (evaluation / result rule): Boolean result: true ^ true is false, true ^ false is true, false ^ false is false; with int operands ^ gives an int bitwise result, so 10 ^ 6 is 12.
- **OS** (state-transition rule): ^ changes no variable; flag = flag ^ true stores the opposite value, toggling the flag.
- **R** (composition rule (with a neighbour)): with logical\_operators: ^ belongs with &amp;&amp;, \|\| and ! as a boolean operator defined by a truth table, but it is not short-circuit and it binds tighter than &amp;&amp; and \|\|; a ^ b equals (a \|\| b) &amp;&amp; !(a &amp;&amp; b).
- **P** (plan / role rule): Expresses 'exactly one of two conditions' (e.g. exactly one of two coordinates is negative) or toggles a parity flag.
- **C** (conservation rule): Swapping the operands keeps the value (^ is commutative), and applying ^ b twice restores the original value ((a ^ b) ^ b == a), so xor with a fixed operand is reversible.
- **D** (error rule): rule broken: ^ is exclusive or, not exponentiation. (silent logic error)
- **X** (applicability rule): Use ^ (or the clearer a != b) when the test is 'the two conditions differ'; never use ^ for powers (use multiplication, Math.pow, or e-notation literals such as 1e6).

## How it is found in code and answers (reader block)

- **Aliases:** none
- **Code patterns:** `\w\s*\^\s*\w`
- **Operator symbols:** none
- **Java types:** none

## The whole prerequisite chain

- **Everything it builds on (4):** `boolean`, `data_type`, `logical_operators`, `primitive_type`
- **Everything that builds on it (0):** nothing

## Every edge in this view and its exact edge logic (14)

All the edges drawn in the picture, in the order: prerequisite, parallel, misconception, error, has_level, contains.

**1. `logical_operators` &rarr; `exclusive_or`** (prerequisite)

- **Exact edge logic:** ^ on booleans is another logical operator, defined by a truth table like &amp;&amp;, \|\| and !: true exactly when its operands differ.
- **Grounding:** order\_only
- **Composition rule (R) of `logical_operators` with `exclusive_or`:** ^ on booleans is a further logical operator, true exactly when the operands differ (it equals (a \|\| b) &amp;&amp; !(a &amp;&amp; b)), but unlike &amp;&amp; and \|\| it always evaluates both operands.
- **Composition rule (R) of `exclusive_or` with `logical_operators`:** ^ belongs with &amp;&amp;, \|\| and ! as a boolean operator defined by a truth table, but it is not short-circuit and it binds tighter than &amp;&amp; and \|\|; a ^ b equals (a \|\| b) &amp;&amp; !(a &amp;&amp; b).

**2. `exclusive_or` &rarr; `CaretIsPower`** (misconception)

- **Exact edge logic (the wrong rule):** a^2 computes a squared.
- **Twin logic (the right rule):** Java has no exponent operator; ^ is exclusive or, and a \* a or Math.pow(a, 2) computes a squared.
- **Role:** context

**3. `arithmetic_operators` &rarr; `CaretIsPower`** (misconception)

- **Exact edge logic (the wrong rule):** a^2 computes a squared.
- **Twin logic (the right rule):** Java has no exponent operator; ^ is exclusive or, and a \* a or Math.pow(a, 2) computes a squared.
- **Role:** primary

**4. `exclusive_or` &rarr; `exclusive_or@L0`** (has_level)

- **Exact edge logic:** exclusive or -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (3 ways).
  - **[0] everyday\_reading** (rule type E, folk-meaning rule): Folk meaning: on calculators, in spreadsheets and in typed maths ^ means 'to the power of', so a^2 is a squared. Java rule: ^ is exclusive or (bitwise on ints), there is no exponent operator, and 10^6 is 12.
  - **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `CaretIsPower`: wrong rule: a^2 computes a squared. Right rule: Java has no exponent operator; ^ is exclusive or, and a \* a or Math.pow(a, 2) computes a squared.
  - **[2] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `CaretIsPower`: Points to LT (both operands are evaluated, then compared: true if they differ). Applied unevenly: in the true/true row of a truth table the student gives true (treating ^ like \|\|) while the other rows are right. (here mixing in: "a^2 computes a squared")

**5. `exclusive_or` &rarr; `exclusive_or@L1`** (has_level)

- **Exact edge logic:** exclusive or -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).
  - **[0] names\_the\_element** (rule type N, identity rule): ^ applied to boolean operands is the exclusive-or logical operator.
  - **[1] states\_the\_rule** (rule type S, declarative rule): For booleans, a ^ b is true if a and b are different and false if they are the same (equivalent to a != b); both operands are always evaluated.

**6. `exclusive_or` &rarr; `exclusive_or@L2`** (has_level)

- **Exact edge logic:** exclusive or -&gt; L2 (Multistructural): the answer applies the rules of exclusive or to every part of the code, in order (3 ways).
  - **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): Evaluate the left operand, then the right operand (always, no short-circuit), then compare them.
  - **[1] output\_prediction** (rule type OP, evaluation / result rule): Boolean result: true ^ true is false, true ^ false is true, false ^ false is false; with int operands ^ gives an int bitwise result, so 10 ^ 6 is 12.
  - **[2] one\_step\_execution** (rule type OS, state-transition rule): ^ changes no variable; flag = flag ^ true stores the opposite value, toggling the flag.

**7. `exclusive_or` &rarr; `exclusive_or@L3`** (has_level)

- **Exact edge logic:** exclusive or -&gt; L3 (Relational): the answer relates the parts (2 ways).
  - **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): ^ belongs with &amp;&amp;, \|\| and ! as a boolean operator defined by a truth table, but it is not short-circuit and it binds tighter than &amp;&amp; and \|\|; a ^ b equals (a \|\| b) &amp;&amp; !(a &amp;&amp; b).
  - **[1] purpose\_of\_the\_whole** (rule type P, plan / role rule): Expresses 'exactly one of two conditions' (e.g. exactly one of two coordinates is negative) or toggles a parity flag.

**8. `exclusive_or` &rarr; `exclusive_or@L4`** (has_level)

- **Exact edge logic:** exclusive or -&gt; L4 (Extended abstract): the answer reasons beyond the given code (3 ways).
  - **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `CaretIsPower`: Swapping the operands keeps the value (^ is commutative), and applying ^ b twice restores the original value ((a ^ b) ^ b == a), so xor with a fixed operand is reversible.
  - **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Use ^ (or the clearer a != b) when the test is 'the two conditions differ'; never use ^ for powers (use multiplication, Math.pow, or e-notation literals such as 1e6).
  - **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: ^ is exclusive or, not exponentiation. Kind: silent logic error. Trigger class: Writing x^2 or 10^n with int operands: it compiles and computes a bitwise xor (10^6 is 12); with double operands such as 2.0^2 it is a compile-time error instead.

**9. `topic1.2.e` &rarr; `exclusive_or`** (contains)

- topic `topic1.2.e` contains `exclusive_or`

**10. `topic1.2.e` &rarr; `boolean`** (contains)

- topic `topic1.2.e` contains `boolean`

**11. `topic1.2.e` &rarr; `boolean_expression`** (contains)

- topic `topic1.2.e` contains `boolean_expression`

**12. `topic1.2.e` &rarr; `de_morgan`** (contains)

- topic `topic1.2.e` contains `de_morgan`

**13. `topic1.2.e` &rarr; `logical_operators`** (contains)

- topic `topic1.2.e` contains `logical_operators`

**14. `topic1.2.e` &rarr; `short_circuit`** (contains)

- topic `topic1.2.e` contains `short_circuit`
