# chained_assignment (`chained_assignment`)

a = b = 0 assigns right to left

Section 1.2 Built-in Types of Data, topic 1.2.a Data types and terminology (literals, identifiers, variables, declarations, assignment, expressions).

![The knowledge graph around chained_assignment](chained_assignment.png)

## At a glance

- **Needs first:** `assignment`
- **Leads to:** nothing
- **Learned alongside:** nothing
- **Misconceptions:** `AssignmentNotExpression`
- **Errors:** none
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 25 edges around this concept. The edge logic, the wrong and right rules and the exact rules of the ways are copied word for word from the graph.

## To work on (0)

Nothing is missing for this concept.

## What it needs first (1)

A prerequisite edge means the other concept has to be understood before `chained_assignment`.

### `assignment` comes before `chained_assignment`

*= stores the computed value of the right side*

- **Edge:** `pre:assignment->chained_assignment`
- **Exact edge logic:** An assignment such as x = y is treated as an expression: it assigns the value of y to x and evaluates to that value.
- **Grounding:** questionable
- **Composition rule (R) of `chained_assignment` with `assignment`:** A chain works only because an assignment is itself an expression whose value is the value stored, so it can be the right side of another =.
- **Composition rule (R) of `assignment` with `chained_assignment`:** Because an assignment is an expression whose value is the value stored, and = groups right to left, a = b = 0 first stores 0 in b and then stores that 0 in a.

## What it leads to (0)

These concepts need `chained_assignment` first.

No concept has this one as a prerequisite.

## Learned alongside (0)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

No parallel edge touches this concept.

## Misconceptions (1)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### AssignmentNotExpression

- **Edge:** `chained_assignment` &rarr; `AssignmentNotExpression` (misconception)
- **Exact edge logic (the wrong rule):** an assignment cannot be used inside a larger expression
- **Twin logic (the right rule):** An assignment is an expression whose value is the value assigned, so (x = v) both stores v in x and gives v.
- **Wrong belief (on the node):** an assignment cannot be used inside a larger expression
- **Correct rule (on the node):** An assignment is an expression whose value is the value assigned, so (x = v) both stores v in x and gives v.
- **Provenance:** published
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [1] misconception, exact rule:** wrong rule: an assignment cannot be used inside a larger expression. Right rule: An assignment is an expression whose value is the value assigned, so (x = v) both stores v in x and gives v.
- **L0 way [2] inconsistent\_trace, exact rule:** Points to LT (the rightmost assignment runs first, and its value feeds the next one to its left). Applied unevenly, a student evaluates a = b first and gives a the old value of b. (here mixing in: "an assignment cannot be used inside a larger expression")
- **Edge `assignment` &rarr; `AssignmentNotExpression`, exact edge logic:** An assignment cannot be used inside a larger expression, so a condition like (x = read()) != v is not allowed. **Twin logic:** An assignment is an expression whose value is the value assigned, so (x = v) both stores v in x and gives v. (role: primary)
- **Edge `expression` &rarr; `AssignmentNotExpression`, exact edge logic:** An assignment cannot be used inside a larger expression, so a condition like (x = read()) != v is not allowed. **Twin logic:** An assignment is an expression whose value is the value assigned, so (x = v) both stores v in x and gives v. (role: context)
- **Edge `read_loop_idiom` &rarr; `AssignmentNotExpression`, exact edge logic:** A read and a test cannot be combined, so while ((x = read()) != end) is not allowed. **Twin logic:** while ((x = read()) != end) reads a value into x and tests that same value in one expression. (role: context)

## Errors (0)

An error edge states the rule that gets broken in a program, and the right rule.

The graph has no error edge from this concept.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for chained assignment: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to chained assignment agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

- **Edge:** `chained_assignment` &rarr; `chained_assignment@L0` (has_level)
- **Exact edge logic:** chained assignment -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (3 ways).

Ways (3), each with its exact rule:

- **[0] everyday\_reading** (rule type E, folk-meaning rule): In maths, a = b = 0 states that all three quantities are equal at once, in any reading order. In Java the = operators group right to left: b = 0 runs first, and its value 0 is then assigned to a.
- **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `AssignmentNotExpression`: wrong rule: an assignment cannot be used inside a larger expression. Right rule: An assignment is an expression whose value is the value assigned, so (x = v) both stores v in x and gives v.
- **[2] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `AssignmentNotExpression`: Points to LT (the rightmost assignment runs first, and its value feeds the next one to its left). Applied unevenly, a student evaluates a = b first and gives a the old value of b. (here mixing in: "an assignment cannot be used inside a larger expression")

### L1: Unistructural / atom x text surface

L1 for chained assignment: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

- **Edge:** `chained_assignment` &rarr; `chained_assignment@L1` (has_level)
- **Exact edge logic:** chained assignment -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

Ways (2), each with its exact rule:

- **[0] names\_the\_element** (rule type N, identity rule): Chained assignment: several = in one expression (a = b = c = 0) that assigns one value to several variables.
- **[1] states\_the\_rule** (rule type S, declarative rule): = is right-associative, and an assignment expression has the value that was stored, so a = b = 0 means a = (b = 0). Every target must be a variable whose type accepts the value.

### L2: Multistructural / block x execution / preoperational

L2 for chained assignment: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

- **Edge:** `chained_assignment` &rarr; `chained_assignment@L2` (has_level)
- **Exact edge logic:** chained assignment -&gt; L2 (Multistructural): the answer applies the rules of chained assignment to every part of the code, in order (3 ways).

Ways (3), each with its exact rule:

- **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): The innermost (rightmost) assignment runs first: evaluate 0, store it in b, and that assignment's value 0 is then stored in a.
- **[1] output\_prediction** (rule type OP, evaluation / result rule): The whole expression's value is the value assigned. With int i and double d, d = i = 5 stores 5 in i and 5.0 in d.
- **[2] one\_step\_execution** (rule type OS, state-transition rule): Every variable in the chain changes, right to left, to the same value (converted to its own type).

### L3: Relational / relations x function (concrete operational begins)

L3 for chained assignment: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

- **Edge:** `chained_assignment` &rarr; `chained_assignment@L3` (has_level)
- **Exact edge logic:** chained assignment -&gt; L3 (Relational): the answer relates the parts (2 ways).

Ways (2), each with its exact rule:

- **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): A chain works only because an assignment is itself an expression whose value is the value stored, so it can be the right side of another =.
- **[1] purpose\_of\_the\_whole** (rule type P, plan / role rule): Initializing several counters or accumulators to the same starting value in one line (sum = count = 0).

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for chained assignment: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

- **Edge:** `chained_assignment` &rarr; `chained_assignment@L4` (has_level)
- **Exact edge logic:** chained assignment -&gt; L4 (Extended abstract): the answer reasons beyond the given code (4 ways).

Ways (4), each with its exact rule:

- **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `AssignmentNotExpression`: Reordering targets with different types can break the chain: d = i = 5 compiles, but i = d = 5 does not, because the double value of d = 5 cannot go into int i.
- **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Use a chain only to give several variables of the same type one simple starting value. Avoid chains inside conditions or with expressions that have side effects.
- **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: Every value in the chain must be assignable to the next target's type. Kind: compile-time. Trigger class: A chain passing through a wider type into a narrower one (int i; double d; i = d = 2.5;): 'possible lossy conversion'.
- **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: int a = b = 0; declares only a; b must already exist. Kind: compile-time. Trigger class: Using the chain in a declaration with an undeclared inner variable: 'cannot find symbol b'.

## Same topic

`chained_assignment` belongs to the topic **Data types and terminology (literals, identifiers, variables, declarations, assignment, expressions)** (`topic1.2.a`). The topic also contains: `assignment`, `data_type`, `declaration`, `definite_assignment`, `expression`, `identifier`, `literal`, `named_constants`, `naming_convention`, `operator_precedence`, `primitive_type`, `program_trace`, `variable`, `variable_swap`.

## Rules of the concept (14)

- **Book** (RS, ): "Unlike most other operators, the assignment operator evaluates from right to left"
- **E** (folk-meaning rule): In maths, a = b = 0 states that all three quantities are equal at once, in any reading order. In Java the = operators group right to left: b = 0 runs first, and its value 0 is then assigned to a.
- **M** (wrong rule / right rule): AssignmentNotExpression: wrong: an assignment cannot be used inside a larger expression \| right: An assignment is an expression whose value is the value assigned, so (x = v) both stores v in x and gives v.
- **T** (uneven-application rule): Points to LT (the rightmost assignment runs first, and its value feeds the next one to its left). Applied unevenly, a student evaluates a = b first and gives a the old value of b.
- **N** (identity rule): Chained assignment: several = in one expression (a = b = c = 0) that assigns one value to several variables.
- **S** (declarative rule): = is right-associative, and an assignment expression has the value that was stored, so a = b = 0 means a = (b = 0). Every target must be a variable whose type accepts the value.
- **LT** (operational sequencing rule): The innermost (rightmost) assignment runs first: evaluate 0, store it in b, and that assignment's value 0 is then stored in a.
- **OP** (evaluation / result rule): The whole expression's value is the value assigned. With int i and double d, d = i = 5 stores 5 in i and 5.0 in d.
- **OS** (state-transition rule): Every variable in the chain changes, right to left, to the same value (converted to its own type).
- **R** (composition rule (with a neighbour)): with assignment: A chain works only because an assignment is itself an expression whose value is the value stored, so it can be the right side of another =.
- **P** (plan / role rule): Initializing several counters or accumulators to the same starting value in one line (sum = count = 0).
- **C** (conservation rule): Reordering targets with different types can break the chain: d = i = 5 compiles, but i = d = 5 does not, because the double value of d = 5 cannot go into int i.
- **D** (error rule): rule broken: Every value in the chain must be assignable to the next target's type. (compile-time)
- **D** (error rule): rule broken: int a = b = 0; declares only a; b must already exist. (compile-time)
- **X** (applicability rule): Use a chain only to give several variables of the same type one simple starting value. Avoid chains inside conditions or with expressions that have side effects.

## How it is found in code and answers (reader block)

- **Aliases:** chained assignment
- **Code patterns:** `\b\w+\s*=(?!=)\s*\w+\s*=(?!=)`
- **Operator symbols:** none
- **Java types:** none

## The whole prerequisite chain

- **Everything it builds on (7):** `assignment`, `data_type`, `declaration`, `identifier`, `literal`, `primitive_type`, `variable`
- **Everything that builds on it (0):** nothing

## Every edge in this view and its exact edge logic (25)

All the edges drawn in the picture, in the order: prerequisite, parallel, misconception, error, has_level, contains.

**1. `assignment` &rarr; `chained_assignment`** (prerequisite)

- **Exact edge logic:** An assignment such as x = y is treated as an expression: it assigns the value of y to x and evaluates to that value.
- **Grounding:** questionable
- **Composition rule (R) of `assignment` with `chained_assignment`:** Because an assignment is an expression whose value is the value stored, and = groups right to left, a = b = 0 first stores 0 in b and then stores that 0 in a.
- **Composition rule (R) of `chained_assignment` with `assignment`:** A chain works only because an assignment is itself an expression whose value is the value stored, so it can be the right side of another =.

**2. `chained_assignment` &rarr; `AssignmentNotExpression`** (misconception)

- **Exact edge logic (the wrong rule):** an assignment cannot be used inside a larger expression
- **Twin logic (the right rule):** An assignment is an expression whose value is the value assigned, so (x = v) both stores v in x and gives v.
- **Role:** context

**3. `assignment` &rarr; `AssignmentNotExpression`** (misconception)

- **Exact edge logic (the wrong rule):** An assignment cannot be used inside a larger expression, so a condition like (x = read()) != v is not allowed.
- **Twin logic (the right rule):** An assignment is an expression whose value is the value assigned, so (x = v) both stores v in x and gives v.
- **Role:** primary

**4. `expression` &rarr; `AssignmentNotExpression`** (misconception)

- **Exact edge logic (the wrong rule):** An assignment cannot be used inside a larger expression, so a condition like (x = read()) != v is not allowed.
- **Twin logic (the right rule):** An assignment is an expression whose value is the value assigned, so (x = v) both stores v in x and gives v.
- **Role:** context

**5. `read_loop_idiom` &rarr; `AssignmentNotExpression`** (misconception)

- **Exact edge logic (the wrong rule):** A read and a test cannot be combined, so while ((x = read()) != end) is not allowed.
- **Twin logic (the right rule):** while ((x = read()) != end) reads a value into x and tests that same value in one expression.
- **Role:** context

**6. `chained_assignment` &rarr; `chained_assignment@L0`** (has_level)

- **Exact edge logic:** chained assignment -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (3 ways).
  - **[0] everyday\_reading** (rule type E, folk-meaning rule): In maths, a = b = 0 states that all three quantities are equal at once, in any reading order. In Java the = operators group right to left: b = 0 runs first, and its value 0 is then assigned to a.
  - **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `AssignmentNotExpression`: wrong rule: an assignment cannot be used inside a larger expression. Right rule: An assignment is an expression whose value is the value assigned, so (x = v) both stores v in x and gives v.
  - **[2] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `AssignmentNotExpression`: Points to LT (the rightmost assignment runs first, and its value feeds the next one to its left). Applied unevenly, a student evaluates a = b first and gives a the old value of b. (here mixing in: "an assignment cannot be used inside a larger expression")

**7. `chained_assignment` &rarr; `chained_assignment@L1`** (has_level)

- **Exact edge logic:** chained assignment -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).
  - **[0] names\_the\_element** (rule type N, identity rule): Chained assignment: several = in one expression (a = b = c = 0) that assigns one value to several variables.
  - **[1] states\_the\_rule** (rule type S, declarative rule): = is right-associative, and an assignment expression has the value that was stored, so a = b = 0 means a = (b = 0). Every target must be a variable whose type accepts the value.

**8. `chained_assignment` &rarr; `chained_assignment@L2`** (has_level)

- **Exact edge logic:** chained assignment -&gt; L2 (Multistructural): the answer applies the rules of chained assignment to every part of the code, in order (3 ways).
  - **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): The innermost (rightmost) assignment runs first: evaluate 0, store it in b, and that assignment's value 0 is then stored in a.
  - **[1] output\_prediction** (rule type OP, evaluation / result rule): The whole expression's value is the value assigned. With int i and double d, d = i = 5 stores 5 in i and 5.0 in d.
  - **[2] one\_step\_execution** (rule type OS, state-transition rule): Every variable in the chain changes, right to left, to the same value (converted to its own type).

**9. `chained_assignment` &rarr; `chained_assignment@L3`** (has_level)

- **Exact edge logic:** chained assignment -&gt; L3 (Relational): the answer relates the parts (2 ways).
  - **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): A chain works only because an assignment is itself an expression whose value is the value stored, so it can be the right side of another =.
  - **[1] purpose\_of\_the\_whole** (rule type P, plan / role rule): Initializing several counters or accumulators to the same starting value in one line (sum = count = 0).

**10. `chained_assignment` &rarr; `chained_assignment@L4`** (has_level)

- **Exact edge logic:** chained assignment -&gt; L4 (Extended abstract): the answer reasons beyond the given code (4 ways).
  - **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `AssignmentNotExpression`: Reordering targets with different types can break the chain: d = i = 5 compiles, but i = d = 5 does not, because the double value of d = 5 cannot go into int i.
  - **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Use a chain only to give several variables of the same type one simple starting value. Avoid chains inside conditions or with expressions that have side effects.
  - **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: Every value in the chain must be assignable to the next target's type. Kind: compile-time. Trigger class: A chain passing through a wider type into a narrower one (int i; double d; i = d = 2.5;): 'possible lossy conversion'.
  - **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: int a = b = 0; declares only a; b must already exist. Kind: compile-time. Trigger class: Using the chain in a declaration with an undeclared inner variable: 'cannot find symbol b'.

**11. `topic1.2.a` &rarr; `chained_assignment`** (contains)

- topic `topic1.2.a` contains `chained_assignment`

**12. `topic1.2.a` &rarr; `assignment`** (contains)

- topic `topic1.2.a` contains `assignment`

**13. `topic1.2.a` &rarr; `data_type`** (contains)

- topic `topic1.2.a` contains `data_type`

**14. `topic1.2.a` &rarr; `declaration`** (contains)

- topic `topic1.2.a` contains `declaration`

**15. `topic1.2.a` &rarr; `definite_assignment`** (contains)

- topic `topic1.2.a` contains `definite_assignment`

**16. `topic1.2.a` &rarr; `expression`** (contains)

- topic `topic1.2.a` contains `expression`

**17. `topic1.2.a` &rarr; `identifier`** (contains)

- topic `topic1.2.a` contains `identifier`

**18. `topic1.2.a` &rarr; `literal`** (contains)

- topic `topic1.2.a` contains `literal`

**19. `topic1.2.a` &rarr; `named_constants`** (contains)

- topic `topic1.2.a` contains `named_constants`

**20. `topic1.2.a` &rarr; `naming_convention`** (contains)

- topic `topic1.2.a` contains `naming_convention`

**21. `topic1.2.a` &rarr; `operator_precedence`** (contains)

- topic `topic1.2.a` contains `operator_precedence`

**22. `topic1.2.a` &rarr; `primitive_type`** (contains)

- topic `topic1.2.a` contains `primitive_type`

**23. `topic1.2.a` &rarr; `program_trace`** (contains)

- topic `topic1.2.a` contains `program_trace`

**24. `topic1.2.a` &rarr; `variable`** (contains)

- topic `topic1.2.a` contains `variable`

**25. `topic1.2.a` &rarr; `variable_swap`** (contains)

- topic `topic1.2.a` contains `variable_swap`
