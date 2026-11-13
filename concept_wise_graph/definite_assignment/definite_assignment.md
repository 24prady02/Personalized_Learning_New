# definite_assignment (`definite_assignment`)

a local variable must be assigned before it is read

Section 1.2 Built-in Types of Data, topic 1.2.a Data types and terminology (literals, identifiers, variables, declarations, assignment, expressions).

![The knowledge graph around definite_assignment](definite_assignment.png)

## At a glance

- **Needs first:** `declaration`
- **Leads to:** nothing
- **Learned alongside:** `array_default_values`
- **Misconceptions:** `LocalVariablesAutoInitialized`
- **Errors:** none
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 25 edges around this concept. The edge logic, the wrong and right rules and the exact rules of the ways are copied word for word from the graph.

## To work on (0)

Nothing is missing for this concept.

## What it needs first (1)

A prerequisite edge means the other concept has to be understood before `definite_assignment`.

### `declaration` comes before `definite_assignment`

*int x; -- introduces a variable name and its type*

- **Edge:** `pre:declaration->definite_assignment`
- **Exact edge logic:** A declared local variable has no defined value until it is assigned, and the compiler rejects any read before that assignment.
- **Grounding:** book\_passage
- **Composition rule (R) of `definite_assignment` with `declaration`:** A declaration without an initializer leaves the local unassigned. Writing = value in the declaration satisfies the rule at once.
- **Composition rule (R) of `declaration` with `definite_assignment`:** A declaration without an initializer leaves a local unassigned, and any read before an assignment on every path is a compile error.

## What it leads to (0)

These concepts need `definite_assignment` first.

No concept has this one as a prerequisite.

## Learned alongside (1)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

### `definite_assignment` alongside `array_default_values`

*new slots start at 0 / false / null*

- **Edge:** `par:definite_assignment~array_default_values`
- **Exact edge logic:** A local variable has no value until it is assigned: using it first is a compile-time error. An array element is given a default value (0, 0.0, false) when the array is created with new, so it can be read before any assignment.
- **Grounding:** book\_passage

## Misconceptions (1)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### LocalVariablesAutoInitialized

- **Edge:** `definite_assignment` &rarr; `LocalVariablesAutoInitialized` (misconception)
- **Exact edge logic (the wrong rule):** local variables get a default value on their own
- **Twin logic (the right rule):** A local variable has no value until it is assigned, and using it before then does not compile.
- **Wrong belief (on the node):** local variables get a default value on their own
- **Correct rule (on the node):** A local variable has no value until it is assigned, and using it before then does not compile.
- **Provenance:** published
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [1] misconception, exact rule:** wrong rule: local variables get a default value on their own. Right rule: A local variable has no value until it is assigned, and using it before then does not compile.
- **L0 way [2] inconsistent\_trace, exact rule:** Points to LT (along every control-flow path, an assignment must come before each read). Applied unevenly, a student checks straight-line code but assumes a variable assigned in only one branch of an if, or inside a loop, is assigned afterwards. (here mixing in: "local variables get a default value on their own")
- **Edge `declaration` &rarr; `LocalVariablesAutoInitialized`, exact edge logic:** local variables get a default value on their own **Twin logic:** A local variable has no value until it is assigned, and using it before then does not compile. (role: context)
- **Edge `variable` &rarr; `LocalVariablesAutoInitialized`, exact edge logic:** int x; inside main starts at 0, so x can be used before anything is assigned to it. **Twin logic:** A local variable has no value until it is assigned, and using it before then does not compile. (role: context)

## Errors (0)

An error edge states the rule that gets broken in a program, and the right rule.

The graph has no error edge from this concept.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for definite assignment: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to definite assignment agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

- **Edge:** `definite_assignment` &rarr; `definite_assignment@L0` (has_level)
- **Exact edge logic:** definite assignment -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (3 ways).

Ways (3), each with its exact rule:

- **[0] everyday\_reading** (rule type E, folk-meaning rule): Everyday intuition, and some older languages, treat a new or empty quantity as zero ("nothing yet means 0"). A Java local variable has no value at all until it is assigned, and the compiler rejects any read before that.
- **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `LocalVariablesAutoInitialized`: wrong rule: local variables get a default value on their own. Right rule: A local variable has no value until it is assigned, and using it before then does not compile.
- **[2] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `LocalVariablesAutoInitialized`: Points to LT (along every control-flow path, an assignment must come before each read). Applied unevenly, a student checks straight-line code but assumes a variable assigned in only one branch of an if, or inside a loop, is assigned afterwards. (here mixing in: "local variables get a default value on their own")

### L1: Unistructural / atom x text surface

L1 for definite assignment: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

- **Edge:** `definite_assignment` &rarr; `definite_assignment@L1` (has_level)
- **Exact edge logic:** definite assignment -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

Ways (2), each with its exact rule:

- **[0] names\_the\_element** (rule type N, identity rule): Definite assignment: the compile-time rule that a local variable must certainly have been assigned before any read of it.
- **[1] states\_the\_rule** (rule type S, declarative rule): Every access of a local variable must be preceded by an assignment on every possible path, or the program does not compile. The analysis ignores run-time values, except for constant booleans and the operators &amp;&amp; \|\| ?:.

### L2: Multistructural / block x execution / preoperational

L2 for definite assignment: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

- **Edge:** `definite_assignment` &rarr; `definite_assignment@L2` (has_level)
- **Exact edge logic:** definite assignment -&gt; L2 (Multistructural): the answer applies the rules of definite assignment to every part of the code, in order (3 ways).

Ways (3), each with its exact rule:

- **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): The compiler walks the control flow. After a declaration with no initializer the variable is unassigned, and an assignment makes it assigned on that path. Where paths merge (after if/else) it counts as assigned only if every incoming path assigned it, and an assignment inside a while body does not count after the loop.
- **[1] output\_prediction** (rule type OP, evaluation / result rule): The result appears at compile time: the code either compiles or reports 'variable x might not have been initialized'. No default value is ever produced for a local variable.
- **[2] one\_step\_execution** (rule type OS, state-transition rule): The first assignment (initialization) moves a variable from unassigned to holding a value, and only then may it be read.

### L3: Relational / relations x function (concrete operational begins)

L3 for definite assignment: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

- **Edge:** `definite_assignment` &rarr; `definite_assignment@L3` (has_level)
- **Exact edge logic:** definite assignment -&gt; L3 (Relational): the answer relates the parts (3 ways).

Ways (3), each with its exact rule:

- **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): A declaration without an initializer leaves the local unassigned. Writing = value in the declaration satisfies the rule at once.
- **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): A local variable has no value until it is assigned: using it first is a compile-time error. An array element is given a default value (0, 0.0, false) when the array is created with new, so it can be read before any assignment.
- **[2] purpose\_of\_the\_whole** (rule type P, plan / role rule): The rule guarantees that no program reads a meaningless value. The matching plan is to initialize counters and accumulators before the loop that updates them (int sum = 0; then sum += i inside the loop).

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for definite assignment: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

- **Edge:** `definite_assignment` &rarr; `definite_assignment@L4` (has_level)
- **Exact edge logic:** definite assignment -&gt; L4 (Extended abstract): the answer reasons beyond the given code (4 ways).

Ways (4), each with its exact rule:

- **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `LocalVariablesAutoInitialized`: Moving an initialization into one branch of an if, or into a loop body, breaks compilation of the reads that follow. Adding an else branch that also assigns, or initializing at the declaration, restores it.
- **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Initialize at the declaration whenever a sensible first value exists (0 for counters and sums). Leave the declaration bare only when every branch that follows assigns it. The rule covers local variables only: array elements and fields get default values.
- **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: A local variable must be definitely assigned before it is read. Kind: compile-time. Trigger class: A read reachable on a path with no assignment: declared without initializer, or assigned only inside an if without else, a loop body, or a switch case: 'variable might not have been initialized'.
- **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: A blank final variable must be assigned at most once. Kind: compile-time. Trigger class: Assigning a final local on two paths that can both run, or again inside a loop: 'variable might already have been assigned'.

## Same topic

`definite_assignment` belongs to the topic **Data types and terminology (literals, identifiers, variables, declarations, assignment, expressions)** (`topic1.2.a`). The topic also contains: `assignment`, `chained_assignment`, `data_type`, `declaration`, `expression`, `identifier`, `literal`, `named_constants`, `naming_convention`, `operator_precedence`, `primitive_type`, `program_trace`, `variable`, `variable_swap`.

## Rules of the concept (14)

- **Book** (SW-1e, p. 16 (pdf 26)): "In a simple declaration, the initial value of the variable is undefined."
- **Book** (SW-1e, p. 35 (pdf 45)): "The compiler checks for this condition and will give you a variable might not have been initialized error message if you try to use the variable in an expression."
- **Book** (SW-1.2, ): "The compiler complains that the variable x might not have been initialized. Variables within main are not automatically initialized."
- **Book** (RS, ): "Using this simple form of variable declaration, Java does not store an initial value in the memory location."
- **E** (folk-meaning rule): Everyday intuition, and some older languages, treat a new or empty quantity as zero ("nothing yet means 0"). A Java local variable has no value at all until it is assigned, and the compiler rejects any read before that.
- **M** (wrong rule / right rule): LocalVariablesAutoInitialized: wrong: local variables get a default value on their own \| right: A local variable has no value until it is assigned, and using it before then does not compile.
- **T** (uneven-application rule): Points to LT (along every control-flow path, an assignment must come before each read). Applied unevenly, a student checks straight-line code but assumes a variable assigned in only one branch of an if, or inside a loop, is assigned afterwards.
- **N** (identity rule): Definite assignment: the compile-time rule that a local variable must certainly have been assigned before any read of it.
- **S** (declarative rule): Every access of a local variable must be preceded by an assignment on every possible path, or the program does not compile. The analysis ignores run-time values, except for constant booleans and the operators &amp;&amp; \|\| ?:.
- **LT** (operational sequencing rule): The compiler walks the control flow. After a declaration with no initializer the variable is unassigned, and an assignment makes it assigned on that path. Where paths merge (after if/else) it counts as assigned only if every incoming path assigned it, and an assignment inside a while body does not count after the loop.
- **OP** (evaluation / result rule): The result appears at compile time: the code either compiles or reports 'variable x might not have been initialized'. No default value is ever produced for a local variable.
- **OS** (state-transition rule): The first assignment (initialization) moves a variable from unassigned to holding a value, and only then may it be read.
- **R** (composition rule (with a neighbour)): with declaration: A declaration without an initializer leaves the local unassigned. Writing = value in the declaration satisfies the rule at once.
- **P** (plan / role rule): The rule guarantees that no program reads a meaningless value. The matching plan is to initialize counters and accumulators before the loop that updates them (int sum = 0; then sum += i inside the loop).
- **C** (conservation rule): Moving an initialization into one branch of an if, or into a loop body, breaks compilation of the reads that follow. Adding an else branch that also assigns, or initializing at the declaration, restores it.
- **D** (error rule): rule broken: A local variable must be definitely assigned before it is read. (compile-time)
- **D** (error rule): rule broken: A blank final variable must be assigned at most once. (compile-time)
- **X** (applicability rule): Initialize at the declaration whenever a sensible first value exists (0 for counters and sums). Leave the declaration bare only when every branch that follows assigns it. The rule covers local variables only: array elements and fields get default values.

## How it is found in code and answers (reader block)

- **Aliases:** definite assignment, definitely assigned, initialized, initialised, initialize, initialise, initialization, uninitialized, uninitialised, not initialized, might not have been initialized, assigned before
- **Code patterns:** none
- **Operator symbols:** none
- **Java types:** none
- **Signal uninitialized\_read\_regex** (scope program, decisive): `\b(?:int|double|boolean|char|long|String)\s+(?P<v>\w+)\s*;(?:(?!\b(?P=v)\s*=(?!=))[\s\S]){0,2000}?\b(?P=v)\b(?!\s*=(?!=))`

## The whole prerequisite chain

- **Everything it builds on (2):** `declaration`, `identifier`
- **Everything that builds on it (0):** nothing

## Every edge in this view and its exact edge logic (25)

All the edges drawn in the picture, in the order: prerequisite, parallel, misconception, error, has_level, contains.

**1. `declaration` &rarr; `definite_assignment`** (prerequisite)

- **Exact edge logic:** A declared local variable has no defined value until it is assigned, and the compiler rejects any read before that assignment.
- **Grounding:** book\_passage
- **Composition rule (R) of `declaration` with `definite_assignment`:** A declaration without an initializer leaves a local unassigned, and any read before an assignment on every path is a compile error.
- **Composition rule (R) of `definite_assignment` with `declaration`:** A declaration without an initializer leaves the local unassigned. Writing = value in the declaration satisfies the rule at once.

**2. `definite_assignment` &harr; `array_default_values`** (parallel)

- **Exact edge logic:** A local variable has no value until it is assigned: using it first is a compile-time error. An array element is given a default value (0, 0.0, false) when the array is created with new, so it can be read before any assignment.
- **Grounding:** book\_passage

**3. `definite_assignment` &rarr; `LocalVariablesAutoInitialized`** (misconception)

- **Exact edge logic (the wrong rule):** local variables get a default value on their own
- **Twin logic (the right rule):** A local variable has no value until it is assigned, and using it before then does not compile.
- **Role:** primary

**4. `declaration` &rarr; `LocalVariablesAutoInitialized`** (misconception)

- **Exact edge logic (the wrong rule):** local variables get a default value on their own
- **Twin logic (the right rule):** A local variable has no value until it is assigned, and using it before then does not compile.
- **Role:** context

**5. `variable` &rarr; `LocalVariablesAutoInitialized`** (misconception)

- **Exact edge logic (the wrong rule):** int x; inside main starts at 0, so x can be used before anything is assigned to it.
- **Twin logic (the right rule):** A local variable has no value until it is assigned, and using it before then does not compile.
- **Role:** context

**6. `definite_assignment` &rarr; `definite_assignment@L0`** (has_level)

- **Exact edge logic:** definite assignment -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (3 ways).
  - **[0] everyday\_reading** (rule type E, folk-meaning rule): Everyday intuition, and some older languages, treat a new or empty quantity as zero ("nothing yet means 0"). A Java local variable has no value at all until it is assigned, and the compiler rejects any read before that.
  - **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `LocalVariablesAutoInitialized`: wrong rule: local variables get a default value on their own. Right rule: A local variable has no value until it is assigned, and using it before then does not compile.
  - **[2] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `LocalVariablesAutoInitialized`: Points to LT (along every control-flow path, an assignment must come before each read). Applied unevenly, a student checks straight-line code but assumes a variable assigned in only one branch of an if, or inside a loop, is assigned afterwards. (here mixing in: "local variables get a default value on their own")

**7. `definite_assignment` &rarr; `definite_assignment@L1`** (has_level)

- **Exact edge logic:** definite assignment -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).
  - **[0] names\_the\_element** (rule type N, identity rule): Definite assignment: the compile-time rule that a local variable must certainly have been assigned before any read of it.
  - **[1] states\_the\_rule** (rule type S, declarative rule): Every access of a local variable must be preceded by an assignment on every possible path, or the program does not compile. The analysis ignores run-time values, except for constant booleans and the operators &amp;&amp; \|\| ?:.

**8. `definite_assignment` &rarr; `definite_assignment@L2`** (has_level)

- **Exact edge logic:** definite assignment -&gt; L2 (Multistructural): the answer applies the rules of definite assignment to every part of the code, in order (3 ways).
  - **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): The compiler walks the control flow. After a declaration with no initializer the variable is unassigned, and an assignment makes it assigned on that path. Where paths merge (after if/else) it counts as assigned only if every incoming path assigned it, and an assignment inside a while body does not count after the loop.
  - **[1] output\_prediction** (rule type OP, evaluation / result rule): The result appears at compile time: the code either compiles or reports 'variable x might not have been initialized'. No default value is ever produced for a local variable.
  - **[2] one\_step\_execution** (rule type OS, state-transition rule): The first assignment (initialization) moves a variable from unassigned to holding a value, and only then may it be read.

**9. `definite_assignment` &rarr; `definite_assignment@L3`** (has_level)

- **Exact edge logic:** definite assignment -&gt; L3 (Relational): the answer relates the parts (3 ways).
  - **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): A declaration without an initializer leaves the local unassigned. Writing = value in the declaration satisfies the rule at once.
  - **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): A local variable has no value until it is assigned: using it first is a compile-time error. An array element is given a default value (0, 0.0, false) when the array is created with new, so it can be read before any assignment.
  - **[2] purpose\_of\_the\_whole** (rule type P, plan / role rule): The rule guarantees that no program reads a meaningless value. The matching plan is to initialize counters and accumulators before the loop that updates them (int sum = 0; then sum += i inside the loop).

**10. `definite_assignment` &rarr; `definite_assignment@L4`** (has_level)

- **Exact edge logic:** definite assignment -&gt; L4 (Extended abstract): the answer reasons beyond the given code (4 ways).
  - **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `LocalVariablesAutoInitialized`: Moving an initialization into one branch of an if, or into a loop body, breaks compilation of the reads that follow. Adding an else branch that also assigns, or initializing at the declaration, restores it.
  - **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Initialize at the declaration whenever a sensible first value exists (0 for counters and sums). Leave the declaration bare only when every branch that follows assigns it. The rule covers local variables only: array elements and fields get default values.
  - **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: A local variable must be definitely assigned before it is read. Kind: compile-time. Trigger class: A read reachable on a path with no assignment: declared without initializer, or assigned only inside an if without else, a loop body, or a switch case: 'variable might not have been initialized'.
  - **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: A blank final variable must be assigned at most once. Kind: compile-time. Trigger class: Assigning a final local on two paths that can both run, or again inside a loop: 'variable might already have been assigned'.

**11. `topic1.2.a` &rarr; `definite_assignment`** (contains)

- topic `topic1.2.a` contains `definite_assignment`

**12. `topic1.2.a` &rarr; `assignment`** (contains)

- topic `topic1.2.a` contains `assignment`

**13. `topic1.2.a` &rarr; `chained_assignment`** (contains)

- topic `topic1.2.a` contains `chained_assignment`

**14. `topic1.2.a` &rarr; `data_type`** (contains)

- topic `topic1.2.a` contains `data_type`

**15. `topic1.2.a` &rarr; `declaration`** (contains)

- topic `topic1.2.a` contains `declaration`

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
