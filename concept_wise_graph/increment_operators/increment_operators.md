# increment_operators (`increment_operators`)

++ / -- (and +=)

Section 1.3 Conditionals and Loops, topic 1.3.d For loops (including i++ and scope).

![The knowledge graph around increment_operators](increment_operators.png)

## At a glance

- **Needs first:** `assignment`, `loop_control`
- **Leads to:** `counter_pattern`, `side_effect_order`
- **Learned alongside:** `compound_assignment`
- **Misconceptions:** `IdiomOverridesCode`, `IncrementByTwo`, `PostIncrementAssignsLater`, `PreIncrementBeforeLoop`, `PrePostIncrementSameValue`
- **Errors:** none
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 27 edges around this concept, each explained in the graph's own words.

## What it needs first (2)

A prerequisite edge means the other concept has to be understood before `increment_operators`.

### `assignment` comes before `increment_operators`

*= stores the computed value of the right side*

i++ is shorthand for the assignment i = i + 1.

- **Grounding:** book passage
- **How `increment_operators` combines with `assignment`:** i++ is shorthand for the assignment i = i + 1 (and i += k for i = i + k), so it changes the variable's stored value.
- **How `assignment` combines with `increment_operators`:** As a statement, i++ has the same effect as the assignment i = i + 1.

### `loop_control` comes before `increment_operators`

*the three slots: init ; condition ; update*

The loop update i = i + 1 comes first; ++ (and +=) are then introduced as shorthand for that update.

- **Grounding:** book passage
- **How `increment_operators` combines with `loop_control`:** The usual for-loop update is i++ (shorthand for i = i + 1); as a stand-alone update statement ++i and i++ give the same loop.
- **How `loop_control` combines with `increment_operators`:** The update i = i + 1 is usually written i++ (or i += k for other steps); as a whole update statement ++i and i++ are equivalent.

## What it leads to (2)

These concepts need `increment_operators` first.

### `increment_operators` comes before `counter_pattern`

*counting occurrences across passes*

A counter is updated with count++, adding one on each pass that matches.

- **Grounding:** book passage

### `increment_operators` comes before `side_effect_order`

*i = i++ and other expressions with side effects*

The result depends on the value an increment expression evaluates to.

- **Grounding:** book passage
- **How `increment_operators` combines with `side_effect_order`:** Inside a larger expression the result depends on which value (old or new) the increment yields and on left-to-right evaluation, e.g. j += j++ in Exercise 1.3.6.
- **How `side_effect_order` combines with `increment_operators`:** The result of an expression with a side effect depends on the value the increment expression evaluates to: old for i++, new for ++i.

## Learned alongside (1)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

### `increment_operators` alongside `compound_assignment`

*x += e, x -= e, ... include a hidden cast*

i++, ++i and i += 1 all add 1 to i; ++ and -- change a variable only by one and are normally used for integers, while i += k works for any amount and with any arithmetic operator (-=, \*=, /=, %=).

- **Grounding:** book passage

## Misconceptions (5)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### IdiomOverridesCode

- **Wrong rule:** An array loop processes the whole array from index 0 to length-1 and increments its index at the end of the body, whatever the code says.
- **Right rule:** The loop visits exactly the indices that its initialisation, guard and update produce, in the order in which its statements are written.
- **Role of this concept:** context
- **Shows at level L0 as:** misconception: wrong rule: An array loop processes the whole array from index 0 to length-1 and increments its index at the end of the body, whatever the code says. Right rule: The loop visits exactly the indices that its initialisation, guard and update produce, in the order in which its statements are written.
- **Also an edge from `array_traversal`:** An array loop processes the whole array from index 0 to length-1 and increments its index at the end of the body, whatever the code says.
- **Also an edge from `for_loop`:** An array loop processes the whole array from index 0 to length-1 and increments its index at the end of the body, whatever the code says.
- **Also an edge from `loop_control`:** An array loop processes the whole array from index 0 to length-1 and increments its index at the end of the body, whatever the code says.

### IncrementByTwo

- **Wrong rule:** i++ increases i by 2.
- **Right rule:** i++ (and ++i) increases i by exactly 1.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: i++ increases i by 2. Right rule: i++ (and ++i) increases i by exactly 1.

### PostIncrementAssignsLater

- **Wrong rule:** i = i++ increases i by 1.
- **Right rule:** i++ evaluates to the old value, so i = i++ stores the old value back.
- **Role of this concept:** context
- **Shows at level L0 as:** misconception: wrong rule: i = i++ increases i by 1. Right rule: i++ evaluates to the old value, so i = i++ stores the old value back.
- **Also an edge from `side_effect_order`:** i = i++ increases i by 1.

### PreIncrementBeforeLoop

- **Wrong rule:** ++i in the for-update runs before the body each pass
- **Right rule:** The update runs after each pass of the body, so with either ++i or i++ the first pass uses i = s.
- **Role of this concept:** context
- **Shows at level L0 as:** misconception: wrong rule: ++i in the for-update runs before the body each pass. Right rule: The update runs after each pass of the body, so with either ++i or i++ the first pass uses i = s.
- **Also an edge from `loop_control`:** With ++i in the update of for (int i = s; i &lt; n; ++i), i is increased before the body runs, so the first pass uses s + 1.

### PrePostIncrementSameValue

- **Wrong rule:** x = i++ and x = ++i store the same value in x.
- **Right rule:** Both increment i, but ++i has the value after the increment and i++ the value before.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: x = i++ and x = ++i store the same value in x. Right rule: Both increment i, but ++i has the value after the increment and i++ the value before.
- **Shows at level L0 as:** inconsistent trace: Applies the increment rule (LT) unevenly: uses the old value in one expression and the new value in another for the same i++, or performs the increment at the end of the loop body instead of where it is written. (here mixing in: "x = i++ and x = ++i store the same value in x")
- **Also an edge from `side_effect_order`:** x = i++ and x = ++i store the same value in x.

## Errors (0)

An error edge states the rule that gets broken in a program, and the right rule.

The graph has no error edge from this concept.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for increment operators: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to increment operators agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

increment operators -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (7 ways).

- **everyday reading** (folk-meaning rule): Folk meaning: '++' reads as 'plus plus' (add twice) or as a maths symbol with no effect, and i++ inside an expression is read as 'add 1 at some later time'. In Java i++ and ++i each add exactly 1 to i immediately when evaluated; they differ only in the value the expression yields.
- **misconception** (wrong rule / right rule; shows `PrePostIncrementSameValue`): wrong rule: x = i++ and x = ++i store the same value in x. Right rule: Both increment i, but ++i has the value after the increment and i++ the value before.
- **misconception** (wrong rule / right rule; shows `IncrementByTwo`): wrong rule: i++ increases i by 2. Right rule: i++ (and ++i) increases i by exactly 1.
- **inconsistent trace** (uneven-application rule; shows `PrePostIncrementSameValue`): Applies the increment rule (LT) unevenly: uses the old value in one expression and the new value in another for the same i++, or performs the increment at the end of the loop body instead of where it is written. (here mixing in: "x = i++ and x = ++i store the same value in x")
- **misconception** (wrong rule / right rule; shows `PostIncrementAssignsLater`): wrong rule: i = i++ increases i by 1. Right rule: i++ evaluates to the old value, so i = i++ stores the old value back.
- **misconception** (wrong rule / right rule; shows `PreIncrementBeforeLoop`): wrong rule: ++i in the for-update runs before the body each pass. Right rule: The update runs after each pass of the body, so with either ++i or i++ the first pass uses i = s.
- **misconception** (wrong rule / right rule; shows `IdiomOverridesCode`): wrong rule: An array loop processes the whole array from index 0 to length-1 and increments its index at the end of the body, whatever the code says. Right rule: The loop visits exactly the indices that its initialisation, guard and update produce, in the order in which its statements are written.

### L1: Unistructural / atom x text surface

L1 for increment operators: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

increment operators -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

- **names the element** (identity rule): ++ and -- are the increment and decrement operators: shorthand that adds 1 to (or subtracts 1 from) a numeric variable.
- **states the rule** (declarative rule): ++ has the same effect as i = i + 1 and -- the same as i = i - 1; as statements i++ and ++i are the same, but in expressions ++i has the value after the increment and i++ the value before.

### L2: Multistructural / block x execution / preoperational

L2 for increment operators: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

increment operators -&gt; L2 (Multistructural): the answer applies the rules of increment operators to every part of the code, in order (3 ways).

- **line by line trace** (operational sequencing rule): i++: fetch the value of i (that is the expression's value), then store i + 1 into i. ++i: store i + 1 into i, and the new value is the expression's value. Both happen before the rest of the enclosing expression continues.
- **output prediction** (evaluation / result rule): With i = 5: x = i++ gives x = 5, i = 6; x = ++i gives x = 6, i = 6; i = i++ leaves i = 5.
- **one step execution** (state-transition rule): One execution changes exactly one variable (i) by exactly 1 and returns its old (i++) or new (++i) value.

### L3: Relational / relations x function (concrete operational begins)

L3 for increment operators: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

increment operators -&gt; L3 (Relational): the answer relates the parts (5 ways).

- **relation to neighbour** (composition rule (with a neighbour)): The usual for-loop update is i++ (shorthand for i = i + 1); as a stand-alone update statement ++i and i++ give the same loop.
- **relation to neighbour** (composition rule (with a neighbour)): Inside a larger expression the result depends on which value (old or new) the increment yields and on left-to-right evaluation, e.g. j += j++ in Exercise 1.3.6.
- **relation to neighbour** (composition rule (with a neighbour)): i++ is shorthand for the assignment i = i + 1 (and i += k for i = i + k), so it changes the variable's stored value.
- **relation to neighbour** (composition rule (with a neighbour)): i++, ++i and i += 1 all add 1 to i; ++ and -- change a variable only by one and are normally used for integers, while i += k works for any amount and with any arithmetic operator (-=, \*=, /=, %=).
- **purpose of the whole** (plan / role rule): Plan/role: the update of a stepper or counter (count++ in a counter, i++ in a counted loop).

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for increment operators: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

increment operators -&gt; L4 (Extended abstract): the answer reasons beyond the given code (4 ways).

- **predict a change** (conservation rule; shows `PrePostIncrementSameValue`): As a stand-alone statement, replacing i++ by ++i, i += 1 or i = i + 1 preserves behaviour; inside an expression (x = i++ vs x = ++i) the swap changes the value used by 1.
- **transfer to a new program** (applicability rule): Use i++ / i-- as stand-alone statements and in for-loop updates; avoid them inside larger expressions (x = ++i), as the book does, and use += for steps other than 1.
- **diagnose an error** (error rule): rule broken: i = i++ stores the old value back. Kind: silent logic error. Trigger class: Writing i = i++ to increment: i never changes, so a loop driven by it is infinite.
- **diagnose an error** (error rule): rule broken: ++ and -- apply only to a variable. Kind: compile-time. Trigger class: Applying ++ to a value that is not a variable, e.g. 5++ or (i + 1)++: compile-time error.

## Same topic

`increment_operators` belongs to the topic **For loops (including i++ and scope)** (`topic1.3.d`). The topic also contains: `compound_assignment`, `for_loop`, `loop_scope`, `loop_variable`, `side_effect_order`.

## Rules of the concept (20)

- **folk-meaning rule:** Folk meaning: '++' reads as 'plus plus' (add twice) or as a maths symbol with no effect, and i++ inside an expression is read as 'add 1 at some later time'. In Java i++ and ++i each add exactly 1 to i immediately when evaluated; they differ only in the value the expression yields.
- **wrong rule / right rule:** PostIncrementAssignsLater: wrong: i = i++ increases i by 1. \| right: i++ evaluates to the old value, so i = i++ stores the old value back.
- **wrong rule / right rule:** PreIncrementBeforeLoop: wrong: ++i in the for-update runs before the body each pass \| right: The update runs after each pass of the body, so with either ++i or i++ the first pass uses i = s.
- **wrong rule / right rule:** PrePostIncrementSameValue: wrong: x = i++ and x = ++i store the same value in x. \| right: Both increment i, but ++i has the value after the increment and i++ the value before.
- **wrong rule / right rule:** IdiomOverridesCode: wrong: An array loop processes the whole array from index 0 to length-1 and increments its index at the end of the body, whatever the code says. \| right: The loop visits exactly the indices that its initialisation, guard and update produce, in the order in which its statements are written.
- **wrong rule / right rule:** IncrementByTwo: wrong: i++ increases i by 2. \| right: i++ (and ++i) increases i by exactly 1.
- **uneven-application rule:** Applies the increment rule (LT) unevenly: uses the old value in one expression and the new value in another for the same i++, or performs the increment at the end of the loop body instead of where it is written.
- **identity rule:** ++ and -- are the increment and decrement operators: shorthand that adds 1 to (or subtracts 1 from) a numeric variable.
- **declarative rule:** ++ has the same effect as i = i + 1 and -- the same as i = i - 1; as statements i++ and ++i are the same, but in expressions ++i has the value after the increment and i++ the value before.
- **operational sequencing rule:** i++: fetch the value of i (that is the expression's value), then store i + 1 into i. ++i: store i + 1 into i, and the new value is the expression's value. Both happen before the rest of the enclosing expression continues.
- **evaluation / result rule:** With i = 5: x = i++ gives x = 5, i = 6; x = ++i gives x = 6, i = 6; i = i++ leaves i = 5.
- **state-transition rule:** One execution changes exactly one variable (i) by exactly 1 and returns its old (i++) or new (++i) value.
- **composition rule (with a neighbour):** with loop\_control: The usual for-loop update is i++ (shorthand for i = i + 1); as a stand-alone update statement ++i and i++ give the same loop.
- **composition rule (with a neighbour):** with side\_effect\_order: Inside a larger expression the result depends on which value (old or new) the increment yields and on left-to-right evaluation, e.g. j += j++ in Exercise 1.3.6.
- **composition rule (with a neighbour):** with assignment: i++ is shorthand for the assignment i = i + 1 (and i += k for i = i + k), so it changes the variable's stored value.
- **plan / role rule:** Plan/role: the update of a stepper or counter (count++ in a counter, i++ in a counted loop).
- **conservation rule:** As a stand-alone statement, replacing i++ by ++i, i += 1 or i = i + 1 preserves behaviour; inside an expression (x = i++ vs x = ++i) the swap changes the value used by 1.
- **error rule:** rule broken: i = i++ stores the old value back. (silent logic error)
- **error rule:** rule broken: ++ and -- apply only to a variable. (compile-time)
- **applicability rule:** Use i++ / i-- as stand-alone statements and in for-loop updates; avoid them inside larger expressions (x = ++i), as the book does, and use += for steps other than 1.

## The whole prerequisite chain

- **Everything it builds on (17):** `arithmetic_operators`, `assignment`, `boolean`, `boolean_expression`, `comparison_operators`, `data_type`, `declaration`, `do_while_loop`, `expression`, `identifier`, `literal`, `logical_operators`, `loop_control`, `loop_variable`, `primitive_type`, `variable`, `while_loop`
- **Everything that builds on it (5):** `counter_pattern`, `frequency_counting`, `monte_carlo_simulation`, `side_effect_order`, `two_models`
