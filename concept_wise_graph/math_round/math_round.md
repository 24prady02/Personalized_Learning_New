# math_round (`math_round`)

Math.round rounds to the nearest integer and returns a long

Section 1.2 Built-in Types of Data, topic 1.2.g Library methods and APIs (Math).

![The knowledge graph around math_round](math_round.png)

## At a glance

- **Needs first:** `math_library`
- **Leads to:** nothing
- **Learned alongside:** `explicit_cast`
- **Misconceptions:** `CastRounds`
- **Errors:** `DiscardedReturnValue`, `RoundReturnsInt`
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 20 edges around this concept. The edge logic, the wrong and right rules and the exact rules of the ways are copied word for word from the graph.

## To work on (0)

Nothing is missing for this concept.

## What it needs first (1)

A prerequisite edge means the other concept has to be understood before `math_round`.

### `math_library` comes before `math_round`

*Math.abs, Math.sqrt, Math.max, Math.random, Math.round ...*

- **Edge:** `pre:math_library->math_round`
- **Exact edge logic:** Math.round is a Math library method.
- **Grounding:** book\_passage
- **Composition rule (R) of `math_round` with `math_library`:** Math.round is listed in the Math API with return type long, which is what forces the cast when the result goes to an int (unlike the other Math methods, which return double).
- **Composition rule (R) of `math_library` with `math_round`:** Math.round is the Math method that rounds to the nearest integer, but it returns a long, so storing it in an int needs a cast.

## What it leads to (0)

These concepts need `math_round` first.

No concept has this one as a prerequisite.

## Learned alongside (1)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

### `math_round` alongside `explicit_cast`

*(int) x -- converts between numeric types, truncating toward zero*

- **Edge:** `par:math_round~explicit_cast`
- **Exact edge logic:** (int) 2.71828 truncates toward zero and gives 2; Math.round(2.71828) rounds to the nearest integer and gives 3, as a long that needs (int) to become an int.
- **Grounding:** book\_passage

## Misconceptions (1)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### CastRounds

- **Edge:** `math_round` &rarr; `CastRounds` (misconception)
- **Exact edge logic (the wrong rule):** (int) 2.7 evaluates to 3.
- **Twin logic (the right rule):** A cast to int discards the fractional part (rounds toward zero, so (int) -2.7 is -2); Math.round rounds to the nearest integer.
- **Wrong belief (on the node):** (int) 2.7 evaluates to 3.
- **Correct rule (on the node):** A cast to int discards the fractional part (rounds toward zero, so (int) -2.7 is -2); Math.round rounds to the nearest integer.
- **Provenance:** textbook
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [1] misconception, exact rule:** wrong rule: (int) 2.7 evaluates to 3. Right rule: A cast to int discards the fractional part (rounds toward zero, so (int) -2.7 is -2); Math.round rounds to the nearest integer.
- **L0 way [2] inconsistent\_trace, exact rule:** Points to LT (evaluate the argument, round it, return a long that must be stored or used). Applied unevenly: the student stores the rounded value in one step but on another line assumes the call itself changed x, or treats the result as an int in one place and as a long elsewhere. (here mixing in: "(int) 2.7 evaluates to 3")
- **Edge `explicit_cast` &rarr; `CastRounds`, exact edge logic:** (int) 2.7 evaluates to 3. **Twin logic:** A cast to int discards the fractional part (rounds toward zero, so (int) -2.7 is -2); Math.round rounds to the nearest integer. (role: primary)
- **Edge `math_library` &rarr; `CastRounds`, exact edge logic:** (int) 2.7 evaluates to 3. **Twin logic:** A cast to int discards the fractional part (rounds toward zero, so (int) -2.7 is -2); Math.round rounds to the nearest integer. (role: context)

## Errors (2)

An error edge states the rule that gets broken in a program, and the right rule.

### DiscardedReturnValue

- **Edge:** `math_round` &rarr; `DiscardedReturnValue` (error)
- **Exact edge logic (the wrong rule):** Writes Math.round(x); on its own line expecting x to be rounded.
- **Twin logic (the right rule):** Math.round(x) returns a value; that value has to be stored or used (e.g. long r = Math.round(x);), because the call on its own line does nothing with it.
- **Wrong belief (on the node):** Writes Math.round(x); on its own line expecting x to be rounded.
- **Correct rule (on the node):** Math.round(x) returns a value; that value has to be stored or used (e.g. long r = Math.round(x);), because the call on its own line does nothing with it.
- **Provenance:** published
- **Role of this concept:** context
- **Edge `method_call` &rarr; `DiscardedReturnValue`, exact edge logic:** Writes Math.round(x); on its own line expecting x to be rounded. **Twin logic:** Math.round(x) returns a value; that value has to be stored or used (e.g. long r = Math.round(x);), because the call on its own line does nothing with it. (role: primary)

### RoundReturnsInt

- **Edge:** `math_round` &rarr; `RoundReturnsInt` (error)
- **Exact edge logic (the wrong rule):** Writes int n = Math.round(x); because Math.round gives an int.
- **Twin logic (the right rule):** Math.round(double) returns a long, so storing it in an int needs a cast: int n = (int) Math.round(x);
- **Wrong belief (on the node):** Writes int n = Math.round(x); because Math.round gives an int.
- **Correct rule (on the node):** Math.round(double) returns a long, so storing it in an int needs a cast: int n = (int) Math.round(x);
- **Provenance:** textbook
- **Role of this concept:** primary
- **Edge `explicit_cast` &rarr; `RoundReturnsInt`, exact edge logic:** Writes int n = Math.round(x); because Math.round gives an int. **Twin logic:** Math.round(double) returns a long, so storing it in an int needs a cast: int n = (int) Math.round(x); (role: context)

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for math round: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to math round agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

- **Edge:** `math_round` &rarr; `math_round@L0` (has_level)
- **Exact edge logic:** math round -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (3 ways).

Ways (3), each with its exact rule:

- **[0] everyday\_reading** (rule type E, folk-meaning rule): Folk meaning: 'round x' (as in school or on a calculator) changes x itself into a whole number, of the ordinary integer kind. Java rule: Math.round(x) leaves x unchanged and returns a new value, the nearest integer, of type long (ties go up, so Math.round(2.5) is 3 and Math.round(-2.5) is -2).
- **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `CastRounds`: wrong rule: (int) 2.7 evaluates to 3. Right rule: A cast to int discards the fractional part (rounds toward zero, so (int) -2.7 is -2); Math.round rounds to the nearest integer.
- **[2] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `CastRounds`: Points to LT (evaluate the argument, round it, return a long that must be stored or used). Applied unevenly: the student stores the rounded value in one step but on another line assumes the call itself changed x, or treats the result as an int in one place and as a long elsewhere. (here mixing in: "(int) 2.7 evaluates to 3")

### L1: Unistructural / atom x text surface

L1 for math round: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

- **Edge:** `math_round` &rarr; `math_round@L1` (has_level)
- **Exact edge logic:** math round -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

Ways (2), each with its exact rule:

- **[0] names\_the\_element** (rule type N, identity rule): Math.round is a Math library (explicit conversion) method that takes a double and returns the nearest integer as a long.
- **[1] states\_the\_rule** (rule type S, declarative rule): Signature long round(double a): round to the nearest integer; the result is long, so storing it in an int requires an explicit cast, as in (int) Math.round(x).

### L2: Multistructural / block x execution / preoperational

L2 for math round: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

- **Edge:** `math_round` &rarr; `math_round@L2` (has_level)
- **Exact edge logic:** math round -&gt; L2 (Multistructural): the answer applies the rules of math round to every part of the code, in order (3 ways).

Ways (3), each with its exact rule:

- **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): In int n = (int) Math.round(x \* 10): evaluate x \* 10, call Math.round on that double, which returns a long, apply the (int) cast, then assign to n.
- **[1] output\_prediction** (rule type OP, evaluation / result rule): Type long: Math.round(3.14159) and Math.round(2.71828) are both 3; Math.round(Math.PI \* 20.0) is 63; (int) Math.round(2.71828) is int 3.
- **[2] one\_step\_execution** (rule type OS, state-transition rule): The call changes no variable: x keeps its value; the only state change is the assignment of the returned long, e.g. long r = Math.round(x);.

### L3: Relational / relations x function (concrete operational begins)

L3 for math round: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

- **Edge:** `math_round` &rarr; `math_round@L3` (has_level)
- **Exact edge logic:** math round -&gt; L3 (Relational): the answer relates the parts (3 ways).

Ways (3), each with its exact rule:

- **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Math.round is listed in the Math API with return type long, which is what forces the cast when the result goes to an int (unlike the other Math methods, which return double).
- **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): (int) 2.71828 truncates toward zero and gives 2; Math.round(2.71828) rounds to the nearest integer and gives 3, as a long that needs (int) to become an int.
- **[2] purpose\_of\_the\_whole** (rule type P, plan / role rule): Converts a computed real value to the nearest whole number for counting, display or pixel coordinates, typically as (int) Math.round(x).

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for math round: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

- **Edge:** `math_round` &rarr; `math_round@L4` (has_level)
- **Exact edge logic:** math round -&gt; L4 (Extended abstract): the answer reasons beyond the given code (4 ways).

Ways (4), each with its exact rule:

- **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `CastRounds`: Replacing Math.round(x) with (int) x changes the result whenever the fractional part is .5 or more (and for negative values), because the cast truncates toward zero; adding the (int) cast keeps the value as long as it fits in the int range.
- **[1] diagnose\_an\_error** (rule type D, error rule): rule broken: Math.round(double) returns a long, so storing it in an int needs a cast: int n = (int) Math.round(x);. Kind: compile-time. Trigger class: int n = Math.round(x); with a double x (possible lossy conversion from long to int).
- **[2] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Use Math.round when the nearest integer is wanted; use a cast when truncation toward zero is wanted; to round only what is printed (e.g. two decimals), use printf instead of changing the value.
- **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: Math.round(x) returns a value and does not change x; the value must be stored or used. Kind: silent logic error. Trigger class: Math.round(x); written as a statement on its own, then x used as if rounded.

## Same topic

`math_round` belongs to the topic **Library methods and APIs (Math)** (`topic1.2.g`). The topic also contains: `api`, `math_library`, `math_random`, `method_call`, `trig_functions`.

## Rules of the concept (14)

- **Book** (SW-1e, p. 31 (pdf 41)): "the library method Math.round() takes a double argument and returns a long result: the nearest integer to the argument."
- **Book** (SW-1.2, ): "Call methods such as Math.round(), Integer.parseInt(), and Double.parseDouble()."
- **E** (folk-meaning rule): Folk meaning: 'round x' (as in school or on a calculator) changes x itself into a whole number, of the ordinary integer kind. Java rule: Math.round(x) leaves x unchanged and returns a new value, the nearest integer, of type long (ties go up, so Math.round(2.5) is 3 and Math.round(-2.5) is -2).
- **M** (wrong rule / right rule): CastRounds: wrong: (int) 2.7 evaluates to 3. \| right: A cast to int discards the fractional part (rounds toward zero, so (int) -2.7 is -2); Math.round rounds to the nearest integer.
- **T** (uneven-application rule): Points to LT (evaluate the argument, round it, return a long that must be stored or used). Applied unevenly: the student stores the rounded value in one step but on another line assumes the call itself changed x, or treats the result as an int in one place and as a long elsewhere.
- **N** (identity rule): Math.round is a Math library (explicit conversion) method that takes a double and returns the nearest integer as a long.
- **S** (declarative rule): Signature long round(double a): round to the nearest integer; the result is long, so storing it in an int requires an explicit cast, as in (int) Math.round(x).
- **LT** (operational sequencing rule): In int n = (int) Math.round(x \* 10): evaluate x \* 10, call Math.round on that double, which returns a long, apply the (int) cast, then assign to n.
- **OP** (evaluation / result rule): Type long: Math.round(3.14159) and Math.round(2.71828) are both 3; Math.round(Math.PI \* 20.0) is 63; (int) Math.round(2.71828) is int 3.
- **OS** (state-transition rule): The call changes no variable: x keeps its value; the only state change is the assignment of the returned long, e.g. long r = Math.round(x);.
- **R** (composition rule (with a neighbour)): with math\_library: Math.round is listed in the Math API with return type long, which is what forces the cast when the result goes to an int (unlike the other Math methods, which return double).
- **P** (plan / role rule): Converts a computed real value to the nearest whole number for counting, display or pixel coordinates, typically as (int) Math.round(x).
- **C** (conservation rule): Replacing Math.round(x) with (int) x changes the result whenever the fractional part is .5 or more (and for negative values), because the cast truncates toward zero; adding the (int) cast keeps the value as long as it fits in the int range.
- **D** (error rule): rule broken: Math.round(x) returns a value and does not change x; the value must be stored or used. (silent logic error)
- **D** (error rule): rule broken: Math.round(double) returns a long, so storing it in an int needs a cast: int n = (int) Math.round(x); (compile-time)
- **X** (applicability rule): Use Math.round when the nearest integer is wanted; use a cast when truncation toward zero is wanted; to round only what is printed (e.g. two decimals), use printf instead of changing the value.

## How it is found in code and answers (reader block)

- **Aliases:** math.round, round, rounds, rounding
- **Code patterns:** `Math\.round\s*\(`
- **Operator symbols:** none
- **Java types:** none

## The whole prerequisite chain

- **Everything it builds on (9):** `arithmetic_operators`, `data_type`, `expression`, `identifier`, `literal`, `math_library`, `method_call`, `primitive_type`, `variable`
- **Everything that builds on it (0):** nothing

## Every edge in this view and its exact edge logic (20)

All the edges drawn in the picture, in the order: prerequisite, parallel, misconception, error, has_level, contains.

**1. `math_library` &rarr; `math_round`** (prerequisite)

- **Exact edge logic:** Math.round is a Math library method.
- **Grounding:** book\_passage
- **Composition rule (R) of `math_library` with `math_round`:** Math.round is the Math method that rounds to the nearest integer, but it returns a long, so storing it in an int needs a cast.
- **Composition rule (R) of `math_round` with `math_library`:** Math.round is listed in the Math API with return type long, which is what forces the cast when the result goes to an int (unlike the other Math methods, which return double).

**2. `math_round` &harr; `explicit_cast`** (parallel)

- **Exact edge logic:** (int) 2.71828 truncates toward zero and gives 2; Math.round(2.71828) rounds to the nearest integer and gives 3, as a long that needs (int) to become an int.
- **Grounding:** book\_passage

**3. `math_round` &rarr; `CastRounds`** (misconception)

- **Exact edge logic (the wrong rule):** (int) 2.7 evaluates to 3.
- **Twin logic (the right rule):** A cast to int discards the fractional part (rounds toward zero, so (int) -2.7 is -2); Math.round rounds to the nearest integer.
- **Role:** context

**4. `explicit_cast` &rarr; `CastRounds`** (misconception)

- **Exact edge logic (the wrong rule):** (int) 2.7 evaluates to 3.
- **Twin logic (the right rule):** A cast to int discards the fractional part (rounds toward zero, so (int) -2.7 is -2); Math.round rounds to the nearest integer.
- **Role:** primary

**5. `math_library` &rarr; `CastRounds`** (misconception)

- **Exact edge logic (the wrong rule):** (int) 2.7 evaluates to 3.
- **Twin logic (the right rule):** A cast to int discards the fractional part (rounds toward zero, so (int) -2.7 is -2); Math.round rounds to the nearest integer.
- **Role:** context

**6. `math_round` &rarr; `DiscardedReturnValue`** (error)

- **Exact edge logic (the wrong rule):** Writes Math.round(x); on its own line expecting x to be rounded.
- **Twin logic (the right rule):** Math.round(x) returns a value; that value has to be stored or used (e.g. long r = Math.round(x);), because the call on its own line does nothing with it.
- **Role:** context

**7. `math_round` &rarr; `RoundReturnsInt`** (error)

- **Exact edge logic (the wrong rule):** Writes int n = Math.round(x); because Math.round gives an int.
- **Twin logic (the right rule):** Math.round(double) returns a long, so storing it in an int needs a cast: int n = (int) Math.round(x);
- **Role:** primary

**8. `explicit_cast` &rarr; `RoundReturnsInt`** (error)

- **Exact edge logic (the wrong rule):** Writes int n = Math.round(x); because Math.round gives an int.
- **Twin logic (the right rule):** Math.round(double) returns a long, so storing it in an int needs a cast: int n = (int) Math.round(x);
- **Role:** context

**9. `method_call` &rarr; `DiscardedReturnValue`** (error)

- **Exact edge logic (the wrong rule):** Writes Math.round(x); on its own line expecting x to be rounded.
- **Twin logic (the right rule):** Math.round(x) returns a value; that value has to be stored or used (e.g. long r = Math.round(x);), because the call on its own line does nothing with it.
- **Role:** primary

**10. `math_round` &rarr; `math_round@L0`** (has_level)

- **Exact edge logic:** math round -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (3 ways).
  - **[0] everyday\_reading** (rule type E, folk-meaning rule): Folk meaning: 'round x' (as in school or on a calculator) changes x itself into a whole number, of the ordinary integer kind. Java rule: Math.round(x) leaves x unchanged and returns a new value, the nearest integer, of type long (ties go up, so Math.round(2.5) is 3 and Math.round(-2.5) is -2).
  - **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `CastRounds`: wrong rule: (int) 2.7 evaluates to 3. Right rule: A cast to int discards the fractional part (rounds toward zero, so (int) -2.7 is -2); Math.round rounds to the nearest integer.
  - **[2] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `CastRounds`: Points to LT (evaluate the argument, round it, return a long that must be stored or used). Applied unevenly: the student stores the rounded value in one step but on another line assumes the call itself changed x, or treats the result as an int in one place and as a long elsewhere. (here mixing in: "(int) 2.7 evaluates to 3")

**11. `math_round` &rarr; `math_round@L1`** (has_level)

- **Exact edge logic:** math round -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).
  - **[0] names\_the\_element** (rule type N, identity rule): Math.round is a Math library (explicit conversion) method that takes a double and returns the nearest integer as a long.
  - **[1] states\_the\_rule** (rule type S, declarative rule): Signature long round(double a): round to the nearest integer; the result is long, so storing it in an int requires an explicit cast, as in (int) Math.round(x).

**12. `math_round` &rarr; `math_round@L2`** (has_level)

- **Exact edge logic:** math round -&gt; L2 (Multistructural): the answer applies the rules of math round to every part of the code, in order (3 ways).
  - **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): In int n = (int) Math.round(x \* 10): evaluate x \* 10, call Math.round on that double, which returns a long, apply the (int) cast, then assign to n.
  - **[1] output\_prediction** (rule type OP, evaluation / result rule): Type long: Math.round(3.14159) and Math.round(2.71828) are both 3; Math.round(Math.PI \* 20.0) is 63; (int) Math.round(2.71828) is int 3.
  - **[2] one\_step\_execution** (rule type OS, state-transition rule): The call changes no variable: x keeps its value; the only state change is the assignment of the returned long, e.g. long r = Math.round(x);.

**13. `math_round` &rarr; `math_round@L3`** (has_level)

- **Exact edge logic:** math round -&gt; L3 (Relational): the answer relates the parts (3 ways).
  - **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Math.round is listed in the Math API with return type long, which is what forces the cast when the result goes to an int (unlike the other Math methods, which return double).
  - **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): (int) 2.71828 truncates toward zero and gives 2; Math.round(2.71828) rounds to the nearest integer and gives 3, as a long that needs (int) to become an int.
  - **[2] purpose\_of\_the\_whole** (rule type P, plan / role rule): Converts a computed real value to the nearest whole number for counting, display or pixel coordinates, typically as (int) Math.round(x).

**14. `math_round` &rarr; `math_round@L4`** (has_level)

- **Exact edge logic:** math round -&gt; L4 (Extended abstract): the answer reasons beyond the given code (4 ways).
  - **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `CastRounds`: Replacing Math.round(x) with (int) x changes the result whenever the fractional part is .5 or more (and for negative values), because the cast truncates toward zero; adding the (int) cast keeps the value as long as it fits in the int range.
  - **[1] diagnose\_an\_error** (rule type D, error rule): rule broken: Math.round(double) returns a long, so storing it in an int needs a cast: int n = (int) Math.round(x);. Kind: compile-time. Trigger class: int n = Math.round(x); with a double x (possible lossy conversion from long to int).
  - **[2] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Use Math.round when the nearest integer is wanted; use a cast when truncation toward zero is wanted; to round only what is printed (e.g. two decimals), use printf instead of changing the value.
  - **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: Math.round(x) returns a value and does not change x; the value must be stored or used. Kind: silent logic error. Trigger class: Math.round(x); written as a statement on its own, then x used as if rounded.

**15. `topic1.2.g` &rarr; `math_round`** (contains)

- topic `topic1.2.g` contains `math_round`

**16. `topic1.2.g` &rarr; `api`** (contains)

- topic `topic1.2.g` contains `api`

**17. `topic1.2.g` &rarr; `math_library`** (contains)

- topic `topic1.2.g` contains `math_library`

**18. `topic1.2.g` &rarr; `math_random`** (contains)

- topic `topic1.2.g` contains `math_random`

**19. `topic1.2.g` &rarr; `method_call`** (contains)

- topic `topic1.2.g` contains `method_call`

**20. `topic1.2.g` &rarr; `trig_functions`** (contains)

- topic `topic1.2.g` contains `trig_functions`
