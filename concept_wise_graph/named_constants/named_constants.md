# named_constants (`named_constants`)

final constants in UPPER\_CASE instead of magic numbers

Section 1.2 Built-in Types of Data, topic 1.2.a Data types and terminology (literals, identifiers, variables, declarations, assignment, expressions).

![The knowledge graph around named_constants](named_constants.png)

## At a glance

- **Needs first:** `declaration`, `naming_convention`
- **Leads to:** nothing
- **Learned alongside:** nothing
- **Misconceptions:** `MagicNumbers`
- **Errors:** `AssignToFinal`
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 27 edges around this concept. The edge logic, the wrong and right rules and the exact rules of the ways are copied word for word from the graph.

## To work on (1)

- misconceptions with no L0 way linked to them: MagicNumbers

## What it needs first (2)

A prerequisite edge means the other concept has to be understood before `named_constants`.

### `declaration` comes before `named_constants`

*int x; -- introduces a variable name and its type*

- **Edge:** `pre:declaration->named_constants`
- **Exact edge logic:** A constant is a declaration marked final.
- **Grounding:** book\_passage
- **Composition rule (R) of `named_constants` with `declaration`:** A constant is an ordinary declaration with the final modifier, with the same type and scope rules.
- **Composition rule (R) of `declaration` with `named_constants`:** Adding final to a declaration makes the variable a constant that can be assigned only once.

### `naming_convention` comes before `named_constants`

*choosing meaningful names: full words, lowerCamelCase, single letters only for throwaway loop counters*

- **Edge:** `pre:naming_convention->named_constants`
- **Exact edge logic:** Constants have their own naming convention.
- **Grounding:** book\_passage
- **Composition rule (R) of `named_constants` with `naming_convention`:** Constants follow their own convention, ALL\_CAPS\_WITH\_UNDERSCORES, which sets them apart from lowerCamelCase variables.
- **Composition rule (R) of `naming_convention` with `named_constants`:** Constants are written in ALL\_CAPS with underscores, which sets them apart from lowerCamelCase variables and signals that they never change.

## What it leads to (0)

These concepts need `named_constants` first.

No concept has this one as a prerequisite.

## Learned alongside (0)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

No parallel edge touches this concept.

## Misconceptions (1)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### MagicNumbers

- **Edge:** `named_constants` &rarr; `MagicNumbers` (misconception)
- **Exact edge logic (the wrong rule):** Writing 7 or 0.0825 directly in formulas is as clear as using a named constant.
- **Twin logic (the right rule):** Give fixed values a final, UPPER\_CASE name and use the name.
- **Wrong belief (on the node):** Writing 7 or 0.0825 directly in formulas is as clear as using a named constant.
- **Correct rule (on the node):** Give fixed values a final, UPPER\_CASE name and use the name.
- **Provenance:** rule\_dictionary
- **Role of this concept:** primary
- **L0 way linked to it:** no
- **Edge `naming_convention` &rarr; `MagicNumbers`, exact edge logic:** Writing 7 or 0.0825 directly in formulas is as clear as using a named constant. **Twin logic:** Give fixed values a final, UPPER\_CASE name and use the name. (role: context)

## Errors (1)

An error edge states the rule that gets broken in a program, and the right rule.

### AssignToFinal

- **Edge:** `named_constants` &rarr; `AssignToFinal` (error)
- **Exact edge logic (the wrong rule):** Assigns a new value to a variable declared final.
- **Twin logic (the right rule):** A final variable cannot be reassigned after it is initialized; the compiler reports an error.
- **Wrong belief (on the node):** Assigns a new value to a variable declared final.
- **Correct rule (on the node):** A final variable cannot be reassigned after it is initialized; the compiler reports an error.
- **Provenance:** published
- **Role of this concept:** primary
- **Edge `assignment` &rarr; `AssignToFinal`, exact edge logic:** Assigns a new value to a variable declared final. **Twin logic:** A final variable cannot be reassigned after it is initialized; the compiler reports an error. (role: context)
- **Edge `compile_time_error` &rarr; `AssignToFinal`, exact edge logic:** Assigns a new value to a variable declared final. **Twin logic:** A final variable cannot be reassigned after it is initialized; the compiler reports an error. (role: context)

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for named constants: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to named constants agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

- **Edge:** `named_constants` &rarr; `named_constants@L0` (has_level)
- **Exact edge logic:** named constants -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (1 way).

Ways (1), each with its exact rule:

- **[0] everyday\_reading** (rule type E, folk-meaning rule): In everyday speech a 'constant' is just a number that stays the same in the problem, and a capitalized name looks official. In Java a value is constant only if its variable is declared final, which the compiler enforces; naming it in UPPER\_CASE alone protects nothing.

### L1: Unistructural / atom x text surface

L1 for named constants: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

- **Edge:** `named_constants` &rarr; `named_constants@L1` (has_level)
- **Exact edge logic:** named constants -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

Ways (2), each with its exact rule:

- **[0] names\_the\_element** (rule type N, identity rule): Named constant: a variable declared final (by convention named in UPPER\_CASE) that names a fixed value.
- **[1] states\_the\_rule** (rule type S, declarative rule): final type NAME = value; cannot be reassigned after initialization (the compiler reports an error). Constant names are all uppercase with \_ between words.

### L2: Multistructural / block x execution / preoperational

L2 for named constants: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

- **Edge:** `named_constants` &rarr; `named_constants@L2` (has_level)
- **Exact edge logic:** named constants -&gt; L2 (Multistructural): the answer applies the rules of named constants to every part of the code, in order (3 ways).

Ways (3), each with its exact rule:

- **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): A constant is initialized once, when its declaration executes. Every later use reads that same value.
- **[1] output\_prediction** (rule type OP, evaluation / result rule): A use of CM\_PER\_INCH evaluates to 2.54 with type double, exactly as the literal would.
- **[2] one\_step\_execution** (rule type OS, state-transition rule): Only the initialization changes state; no later statement can change the constant.

### L3: Relational / relations x function (concrete operational begins)

L3 for named constants: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

- **Edge:** `named_constants` &rarr; `named_constants@L3` (has_level)
- **Exact edge logic:** named constants -&gt; L3 (Relational): the answer relates the parts (3 ways).

Ways (3), each with its exact rule:

- **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): A constant is an ordinary declaration with the final modifier, with the same type and scope rules.
- **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Constants follow their own convention, ALL\_CAPS\_WITH\_UNDERSCORES, which sets them apart from lowerCamelCase variables.
- **[2] purpose\_of\_the\_whole** (rule type P, plan / role rule): Plan: replace magic numbers with a meaningful name (Sajaniemi role: fixed value), so the code is readable, the value is changed in one place, and accidental reassignment is prevented.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for named constants: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

- **Edge:** `named_constants` &rarr; `named_constants@L4` (has_level)
- **Exact edge logic:** named constants -&gt; L4 (Extended abstract): the answer reasons beyond the given code (4 ways).

Ways (4), each with its exact rule:

- **[0] predict\_a\_change** (rule type C, conservation rule): Changing the constant's value in its declaration changes every use consistently. Removing final keeps behavior but loses the protection. Adding any later assignment to it breaks compilation.
- **[1] diagnose\_an\_error** (rule type D, error rule): rule broken: A final variable is assigned exactly once; it cannot be reassigned after initialization. Kind: compile-time. Trigger class: Any assignment, ++ or op= to a final variable after its initialization: 'cannot assign a value to final variable'.
- **[2] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Use a named constant for a value fixed for the whole run that appears in formulas (conversion factors, physical constants, sizes, rates). Use a variable for values that are read or computed, and plain literals for self-evident values such as 0 or 1.
- **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: A final variable must be assigned before it is read. Kind: compile-time. Trigger class: Declaring final double RATE; and reading it on a path that never assigns it: 'variable RATE might not have been initialized'.

## Same topic

`named_constants` belongs to the topic **Data types and terminology (literals, identifiers, variables, declarations, assignment, expressions)** (`topic1.2.a`). The topic also contains: `assignment`, `chained_assignment`, `data_type`, `declaration`, `definite_assignment`, `expression`, `identifier`, `literal`, `naming_convention`, `operator_precedence`, `primitive_type`, `program_trace`, `variable`, `variable_swap`.

## Rules of the concept (14)

- **Book** (TJ-2e, p. 38 (pdf 60)): "Declaring that a variable is final means that it cannot be reassigned once it has been initialized."
- **Book** (TJ-2e, p. 38 (pdf 60)): "By convention, names for constants are all uppercase, with the underscore character (\_) between words."
- **Book** (RS, ): "constants, which have an even more distinct capitalization scheme, with all letters in uppercase and words separated by underscores"
- **E** (folk-meaning rule): In everyday speech a 'constant' is just a number that stays the same in the problem, and a capitalized name looks official. In Java a value is constant only if its variable is declared final, which the compiler enforces; naming it in UPPER\_CASE alone protects nothing.
- **T** (uneven-application rule): Points to LT (a final variable is assigned once and every read gives that value). Applied unevenly, a student treats a constant as updated later in the program on some reads.
- **N** (identity rule): Named constant: a variable declared final (by convention named in UPPER\_CASE) that names a fixed value.
- **S** (declarative rule): final type NAME = value; cannot be reassigned after initialization (the compiler reports an error). Constant names are all uppercase with \_ between words.
- **LT** (operational sequencing rule): A constant is initialized once, when its declaration executes. Every later use reads that same value.
- **OP** (evaluation / result rule): A use of CM\_PER\_INCH evaluates to 2.54 with type double, exactly as the literal would.
- **OS** (state-transition rule): Only the initialization changes state; no later statement can change the constant.
- **R** (composition rule (with a neighbour)): with declaration: A constant is an ordinary declaration with the final modifier, with the same type and scope rules.
- **R** (composition rule (with a neighbour)): with naming\_convention: Constants follow their own convention, ALL\_CAPS\_WITH\_UNDERSCORES, which sets them apart from lowerCamelCase variables.
- **P** (plan / role rule): Plan: replace magic numbers with a meaningful name (Sajaniemi role: fixed value), so the code is readable, the value is changed in one place, and accidental reassignment is prevented.
- **C** (conservation rule): Changing the constant's value in its declaration changes every use consistently. Removing final keeps behavior but loses the protection. Adding any later assignment to it breaks compilation.
- **D** (error rule): rule broken: A final variable is assigned exactly once; it cannot be reassigned after initialization. (compile-time)
- **D** (error rule): rule broken: A final variable must be assigned before it is read. (compile-time)
- **X** (applicability rule): Use a named constant for a value fixed for the whole run that appears in formulas (conversion factors, physical constants, sizes, rates). Use a variable for values that are read or computed, and plain literals for self-evident values such as 0 or 1.

## How it is found in code and answers (reader block)

- **Aliases:** constant, final
- **Code patterns:** `\bfinal\s+(?:int|double|boolean|char|long|String|float|short|byte)\s+[A-Z][A-Z0-9_]*\s*=`, `\bstatic\s+final\b`
- **Operator symbols:** none
- **Java types:** none

## The whole prerequisite chain

- **Everything it builds on (7):** `data_type`, `declaration`, `identifier`, `literal`, `naming_convention`, `primitive_type`, `variable`
- **Everything that builds on it (0):** nothing

## Every edge in this view and its exact edge logic (27)

All the edges drawn in the picture, in the order: prerequisite, parallel, misconception, error, has_level, contains.

**1. `declaration` &rarr; `named_constants`** (prerequisite)

- **Exact edge logic:** A constant is a declaration marked final.
- **Grounding:** book\_passage
- **Composition rule (R) of `declaration` with `named_constants`:** Adding final to a declaration makes the variable a constant that can be assigned only once.
- **Composition rule (R) of `named_constants` with `declaration`:** A constant is an ordinary declaration with the final modifier, with the same type and scope rules.

**2. `naming_convention` &rarr; `named_constants`** (prerequisite)

- **Exact edge logic:** Constants have their own naming convention.
- **Grounding:** book\_passage
- **Composition rule (R) of `naming_convention` with `named_constants`:** Constants are written in ALL\_CAPS with underscores, which sets them apart from lowerCamelCase variables and signals that they never change.
- **Composition rule (R) of `named_constants` with `naming_convention`:** Constants follow their own convention, ALL\_CAPS\_WITH\_UNDERSCORES, which sets them apart from lowerCamelCase variables.

**3. `named_constants` &rarr; `MagicNumbers`** (misconception)

- **Exact edge logic (the wrong rule):** Writing 7 or 0.0825 directly in formulas is as clear as using a named constant.
- **Twin logic (the right rule):** Give fixed values a final, UPPER\_CASE name and use the name.
- **Role:** primary

**4. `naming_convention` &rarr; `MagicNumbers`** (misconception)

- **Exact edge logic (the wrong rule):** Writing 7 or 0.0825 directly in formulas is as clear as using a named constant.
- **Twin logic (the right rule):** Give fixed values a final, UPPER\_CASE name and use the name.
- **Role:** context

**5. `named_constants` &rarr; `AssignToFinal`** (error)

- **Exact edge logic (the wrong rule):** Assigns a new value to a variable declared final.
- **Twin logic (the right rule):** A final variable cannot be reassigned after it is initialized; the compiler reports an error.
- **Role:** primary

**6. `assignment` &rarr; `AssignToFinal`** (error)

- **Exact edge logic (the wrong rule):** Assigns a new value to a variable declared final.
- **Twin logic (the right rule):** A final variable cannot be reassigned after it is initialized; the compiler reports an error.
- **Role:** context

**7. `compile_time_error` &rarr; `AssignToFinal`** (error)

- **Exact edge logic (the wrong rule):** Assigns a new value to a variable declared final.
- **Twin logic (the right rule):** A final variable cannot be reassigned after it is initialized; the compiler reports an error.
- **Role:** context

**8. `named_constants` &rarr; `named_constants@L0`** (has_level)

- **Exact edge logic:** named constants -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (1 way).
  - **[0] everyday\_reading** (rule type E, folk-meaning rule): In everyday speech a 'constant' is just a number that stays the same in the problem, and a capitalized name looks official. In Java a value is constant only if its variable is declared final, which the compiler enforces; naming it in UPPER\_CASE alone protects nothing.

**9. `named_constants` &rarr; `named_constants@L1`** (has_level)

- **Exact edge logic:** named constants -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).
  - **[0] names\_the\_element** (rule type N, identity rule): Named constant: a variable declared final (by convention named in UPPER\_CASE) that names a fixed value.
  - **[1] states\_the\_rule** (rule type S, declarative rule): final type NAME = value; cannot be reassigned after initialization (the compiler reports an error). Constant names are all uppercase with \_ between words.

**10. `named_constants` &rarr; `named_constants@L2`** (has_level)

- **Exact edge logic:** named constants -&gt; L2 (Multistructural): the answer applies the rules of named constants to every part of the code, in order (3 ways).
  - **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): A constant is initialized once, when its declaration executes. Every later use reads that same value.
  - **[1] output\_prediction** (rule type OP, evaluation / result rule): A use of CM\_PER\_INCH evaluates to 2.54 with type double, exactly as the literal would.
  - **[2] one\_step\_execution** (rule type OS, state-transition rule): Only the initialization changes state; no later statement can change the constant.

**11. `named_constants` &rarr; `named_constants@L3`** (has_level)

- **Exact edge logic:** named constants -&gt; L3 (Relational): the answer relates the parts (3 ways).
  - **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): A constant is an ordinary declaration with the final modifier, with the same type and scope rules.
  - **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Constants follow their own convention, ALL\_CAPS\_WITH\_UNDERSCORES, which sets them apart from lowerCamelCase variables.
  - **[2] purpose\_of\_the\_whole** (rule type P, plan / role rule): Plan: replace magic numbers with a meaningful name (Sajaniemi role: fixed value), so the code is readable, the value is changed in one place, and accidental reassignment is prevented.

**12. `named_constants` &rarr; `named_constants@L4`** (has_level)

- **Exact edge logic:** named constants -&gt; L4 (Extended abstract): the answer reasons beyond the given code (4 ways).
  - **[0] predict\_a\_change** (rule type C, conservation rule): Changing the constant's value in its declaration changes every use consistently. Removing final keeps behavior but loses the protection. Adding any later assignment to it breaks compilation.
  - **[1] diagnose\_an\_error** (rule type D, error rule): rule broken: A final variable is assigned exactly once; it cannot be reassigned after initialization. Kind: compile-time. Trigger class: Any assignment, ++ or op= to a final variable after its initialization: 'cannot assign a value to final variable'.
  - **[2] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Use a named constant for a value fixed for the whole run that appears in formulas (conversion factors, physical constants, sizes, rates). Use a variable for values that are read or computed, and plain literals for self-evident values such as 0 or 1.
  - **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: A final variable must be assigned before it is read. Kind: compile-time. Trigger class: Declaring final double RATE; and reading it on a path that never assigns it: 'variable RATE might not have been initialized'.

**13. `topic1.2.a` &rarr; `named_constants`** (contains)

- topic `topic1.2.a` contains `named_constants`

**14. `topic1.2.a` &rarr; `assignment`** (contains)

- topic `topic1.2.a` contains `assignment`

**15. `topic1.2.a` &rarr; `chained_assignment`** (contains)

- topic `topic1.2.a` contains `chained_assignment`

**16. `topic1.2.a` &rarr; `data_type`** (contains)

- topic `topic1.2.a` contains `data_type`

**17. `topic1.2.a` &rarr; `declaration`** (contains)

- topic `topic1.2.a` contains `declaration`

**18. `topic1.2.a` &rarr; `definite_assignment`** (contains)

- topic `topic1.2.a` contains `definite_assignment`

**19. `topic1.2.a` &rarr; `expression`** (contains)

- topic `topic1.2.a` contains `expression`

**20. `topic1.2.a` &rarr; `identifier`** (contains)

- topic `topic1.2.a` contains `identifier`

**21. `topic1.2.a` &rarr; `literal`** (contains)

- topic `topic1.2.a` contains `literal`

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

**27. `topic1.2.a` &rarr; `variable_swap`** (contains)

- topic `topic1.2.a` contains `variable_swap`
