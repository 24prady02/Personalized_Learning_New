# compound_assignment (`compound_assignment`)

x += e, x -= e, ... include a hidden cast

Section 1.3 Conditionals and Loops, topic 1.3.d For loops (including i++ and scope).

![The knowledge graph around compound_assignment](compound_assignment.png)

## At a glance

- **Needs first:** `assignment`, `explicit_cast`
- **Leads to:** `accumulator_pattern`
- **Learned alongside:** `increment_operators`
- **Misconceptions:** `CompoundAssignmentNoCast`, `CompoundSubtractIsAssignNegative`
- **Errors:** none
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 18 edges around this concept, each explained in the graph's own words.

## What it needs first (2)

A prerequisite edge means the other concept has to be understood before `compound_assignment`.

### `assignment` comes before `compound_assignment`

*= stores the computed value of the right side*

x op= e is shorthand for the assignment x = x op e.

- **Grounding:** book passage
- **How `compound_assignment` combines with `assignment`:** x op= e is shorthand for the assignment x = x op e, so the new value depends on the old one (x is read, then written).
- **How `assignment` combines with `compound_assignment`:** x op= e is shorthand for x = x op e. The left variable's current value is fetched first and then combined with e.

### `explicit_cast` comes before `compound_assignment`

*(int) x -- converts between numeric types, truncating toward zero*

x op= e means x = (T)(x op e), where T is the type of x, so the result is cast back to the type of x.

- **Grounding:** questionable
- **How `compound_assignment` combines with `explicit_cast`:** x op= e includes a hidden narrowing cast to the type of x: with int x = 1, x += 1.7 compiles (as x = (int)(x + 1.7), giving 2) while x = x + 1.7 does not.
- **How `explicit_cast` combines with `compound_assignment`:** x op= e contains an implicit cast back to the type of x, so with int x, x += 0.5 compiles (x = (int) (x + 0.5)) while x = x + 0.5 is a compile-time error.

## What it leads to (1)

These concepts need `compound_assignment` first.

### `compound_assignment` comes before `accumulator_pattern`

*building up a running total/result*

sum += x is the usual way a running total is updated on each pass.

- **Grounding:** book passage

## Learned alongside (1)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

### `compound_assignment` alongside `increment_operators`

*++ / -- (and +=)*

i++, ++i and i += 1 all add 1 to i; ++ and -- change a variable only by one and are normally used for integers, while i += k works for any amount and with any arithmetic operator (-=, \*=, /=, %=).

- **Grounding:** book passage

## Misconceptions (2)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### CompoundAssignmentNoCast

- **Wrong rule:** x += 0.5 adds one half to an int x.
- **Right rule:** x += 0.5 is x = (int) (x + 0.5), so an int x does not change.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: x += 0.5 adds one half to an int x. Right rule: x += 0.5 means x = (int) (x + 0.5) for an int x, so the sum is cast back to int and truncated: x stays the same (x = 3 gives 3.5, cast to 3).
- **Shows at level L0 as:** inconsistent trace: Applies the compound-assignment rule (LT) unevenly: uses the current value of x on some passes but treats x -= y as x = -y on others, or forgets the implicit cast on some lines. (here mixing in: "x += 0.5 adds one half to an int x")
- **Also an edge from `infinite_loop`:** x += 0.5 adds one half to an int x.

### CompoundSubtractIsAssignNegative

- **Wrong rule:** x[i] -= y sets x[i] to -y (reads -= as assignment of a negated value).
- **Right rule:** x[i] -= y means x[i] = x[i] - y: it subtracts y from the current value.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: x[i] -= y sets x[i] to -y (reads -= as assignment of a negated value). Right rule: x[i] -= y means x[i] = x[i] - y: it subtracts y from the current value.

## Errors (0)

An error edge states the rule that gets broken in a program, and the right rule.

The graph has no error edge from this concept.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for compound assignment: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to compound assignment agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

compound assignment -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (4 ways).

- **everyday reading** (folk-meaning rule): Folk meaning: x -= y reads as 'x equals minus y' and x += 0.5 as 'add a half' in arithmetic. In Java x op= e means x = (T) (x op e): it updates x from its current value and casts the result back to x's type.
- **misconception** (wrong rule / right rule; shows `CompoundAssignmentNoCast`): wrong rule: x += 0.5 adds one half to an int x. Right rule: x += 0.5 means x = (int) (x + 0.5) for an int x, so the sum is cast back to int and truncated: x stays the same (x = 3 gives 3.5, cast to 3).
- **misconception** (wrong rule / right rule; shows `CompoundSubtractIsAssignNegative`): wrong rule: x[i] -= y sets x[i] to -y (reads -= as assignment of a negated value). Right rule: x[i] -= y means x[i] = x[i] - y: it subtracts y from the current value.
- **inconsistent trace** (uneven-application rule; shows `CompoundAssignmentNoCast`): Applies the compound-assignment rule (LT) unevenly: uses the current value of x on some passes but treats x -= y as x = -y on others, or forgets the implicit cast on some lines. (here mixing in: "x += 0.5 adds one half to an int x")

### L1: Unistructural / atom x text surface

L1 for compound assignment: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

compound assignment -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

- **names the element** (identity rule): A compound assignment operator (+=, -=, \*=, /=, %=) is an assignment shorthand that combines a binary operation with storing the result back in the left-hand variable.
- **states the rule** (declarative rule): x op= e is equivalent to x = (T) ((x) op (e)) where T is the type of x, with x evaluated only once; it works for any arithmetic operator in any primitive numeric type. x op= e means x = (T)(x op e), with a hidden cast to the type T of x: with int x = 3, x += 0.5 compiles and leaves 3, while x = x + 0.5 does not compile.

### L2: Multistructural / block x execution / preoperational

L2 for compound assignment: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

compound assignment -&gt; L2 (Multistructural): the answer applies the rules of compound assignment to every part of the code, in order (3 ways).

- **line by line trace** (operational sequencing rule): Evaluate x and save its value, then evaluate e, then compute x op e, cast to x's type, and store into x.
- **output prediction** (evaluation / result rule): The new value of x is (T)(old x op e) and is also the expression's value: each starting from int x = 7: x += 3 gives 10, x /= 2 gives 3, and x += 0.5 gives 7 (7.5 truncated) instead of a compile error.
- **one step execution** (state-transition rule): One execution changes exactly one variable, x, from its old value (sum += x[i] turns sum = 1 into 1 + 4 = 5).

### L3: Relational / relations x function (concrete operational begins)

L3 for compound assignment: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

compound assignment -&gt; L3 (Relational): the answer relates the parts (4 ways).

- **relation to neighbour** (composition rule (with a neighbour)): x op= e is shorthand for the assignment x = x op e, so the new value depends on the old one (x is read, then written).
- **relation to neighbour** (composition rule (with a neighbour)): x op= e includes a hidden narrowing cast to the type of x: with int x = 1, x += 1.7 compiles (as x = (int)(x + 1.7), giving 2) while x = x + 1.7 does not.
- **relation to neighbour** (composition rule (with a neighbour)): i++, ++i and i += 1 all add 1 to i; ++ and -- change a variable only by one and are normally used for integers, while i += k works for any amount and with any arithmetic operator (-=, \*=, /=, %=).
- **purpose of the whole** (plan / role rule): Plan/role: the update step of a gatherer (sum += a[i], product \*= i) or of a stepper with a step other than 1 (i += 2).

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for compound assignment: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

compound assignment -&gt; L4 (Extended abstract): the answer reasons beyond the given code (4 ways).

- **predict a change** (conservation rule; shows `CompoundAssignmentNoCast`): For a variable of the same type as the result, replacing x op= e by x = x op e preserves behaviour; when x is narrower (int x, double e), x = x op e no longer compiles, so the two are not always interchangeable. Swapping += and -= reverses the effect of each pass.
- **transfer to a new program** (applicability rule): Use op= for in-place updates of accumulators, products and counters with steps other than 1; avoid it when x is int and e is fractional (silent truncation), and use explicit x = x op e when the cast should be visible.
- **diagnose an error** (error rule): rule broken: x op= e silently casts the result to the type of x. Kind: silent logic error. Trigger class: int total = 0; total += 0.5 \* k; or int avg = 7; avg /= 2.0;: fractional parts are discarded (avg becomes 3) without a compiler error.
- **diagnose an error** (error rule): rule broken: =- is assignment of a negated value, not -=. Kind: silent logic error. Trigger class: Typing x =- y for x -= y: compiles as x = -y.

## Same topic

`compound_assignment` belongs to the topic **For loops (including i++ and scope)** (`topic1.3.d`). The topic also contains: `for_loop`, `increment_operators`, `loop_scope`, `loop_variable`, `side_effect_order`.

## Rules of the concept (16)

- **folk-meaning rule:** Folk meaning: x -= y reads as 'x equals minus y' and x += 0.5 as 'add a half' in arithmetic. In Java x op= e means x = (T) (x op e): it updates x from its current value and casts the result back to x's type.
- **wrong rule / right rule:** CompoundAssignmentNoCast: wrong: x += 0.5 adds one half to an int x. \| right: x += 0.5 means x = (int) (x + 0.5) for an int x, so the sum is cast back to int and truncated: x stays the same (x = 3 gives 3.5, cast to 3).
- **wrong rule / right rule:** CompoundSubtractIsAssignNegative: wrong: x[i] -= y sets x[i] to -y (reads -= as assignment of a negated value). \| right: x[i] -= y means x[i] = x[i] - y: it subtracts y from the current value.
- **uneven-application rule:** Applies the compound-assignment rule (LT) unevenly: uses the current value of x on some passes but treats x -= y as x = -y on others, or forgets the implicit cast on some lines.
- **identity rule:** A compound assignment operator (+=, -=, \*=, /=, %=) is an assignment shorthand that combines a binary operation with storing the result back in the left-hand variable.
- **declarative rule:** x op= e is equivalent to x = (T) ((x) op (e)) where T is the type of x, with x evaluated only once; it works for any arithmetic operator in any primitive numeric type. x op= e means x = (T)(x op e), with a hidden cast to the type T of x: with int x = 3, x += 0.5 compiles and leaves 3, while x = x + 0.5 does not compile.
- **operational sequencing rule:** Evaluate x and save its value, then evaluate e, then compute x op e, cast to x's type, and store into x.
- **evaluation / result rule:** The new value of x is (T)(old x op e) and is also the expression's value: each starting from int x = 7: x += 3 gives 10, x /= 2 gives 3, and x += 0.5 gives 7 (7.5 truncated) instead of a compile error.
- **state-transition rule:** One execution changes exactly one variable, x, from its old value (sum += x[i] turns sum = 1 into 1 + 4 = 5).
- **composition rule (with a neighbour):** with assignment: x op= e is shorthand for the assignment x = x op e, so the new value depends on the old one (x is read, then written).
- **composition rule (with a neighbour):** with explicit\_cast: x op= e includes a hidden narrowing cast to the type of x: with int x = 1, x += 1.7 compiles (as x = (int)(x + 1.7), giving 2) while x = x + 1.7 does not.
- **plan / role rule:** Plan/role: the update step of a gatherer (sum += a[i], product \*= i) or of a stepper with a step other than 1 (i += 2).
- **conservation rule:** For a variable of the same type as the result, replacing x op= e by x = x op e preserves behaviour; when x is narrower (int x, double e), x = x op e no longer compiles, so the two are not always interchangeable. Swapping += and -= reverses the effect of each pass.
- **error rule:** rule broken: x op= e silently casts the result to the type of x. (silent logic error)
- **error rule:** rule broken: =- is assignment of a negated value, not -=. (silent logic error)
- **applicability rule:** Use op= for in-place updates of accumulators, products and counters with steps other than 1; avoid it when x is int and e is fractional (silent truncation), and use explicit x = x op e when the cast should be visible.

## The whole prerequisite chain

- **Everything it builds on (16):** `arithmetic_operators`, `assignment`, `class_declaration`, `command_line_args`, `data_type`, `declaration`, `explicit_cast`, `identifier`, `integer_division`, `literal`, `main_method`, `parsing`, `primitive_type`, `program_text`, `type_conversion`, `variable`
- **Everything that builds on it (2):** `accumulator_pattern`, `sentinel_loop`
