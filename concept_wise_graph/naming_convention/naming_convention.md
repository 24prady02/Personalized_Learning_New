# naming_convention (`naming_convention`)

choosing meaningful names: full words, lowerCamelCase, single letters only for throwaway loop counters

Section 1.2 Built-in Types of Data, topic 1.2.a Data types and terminology (literals, identifiers, variables, declarations, assignment, expressions).

![The knowledge graph around naming_convention](naming_convention.png)

## At a glance

- **Needs first:** `variable`
- **Leads to:** `named_constants`
- **Learned alongside:** nothing
- **Misconceptions:** `CrypticVariableName`, `MagicNumbers`, `NameGivesMeaning`, `NameNotCamelCase`
- **Errors:** none
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 28 edges around this concept. The edge logic, the wrong and right rules and the exact rules of the ways are copied word for word from the graph.

## To work on (1)

- misconceptions with no L0 way linked to them: CrypticVariableName, NameNotCamelCase, MagicNumbers

## What it needs first (1)

A prerequisite edge means the other concept has to be understood before `naming_convention`.

### `variable` comes before `naming_convention`

*a named, typed box that holds a value*

- **Edge:** `pre:variable->naming_convention`
- **Exact edge logic:** Each variable gets a name; the convention says the name should describe what the variable holds.
- **Grounding:** book\_passage
- **Composition rule (R) of `naming_convention` with `variable`:** Each variable's name should describe what it holds (count, sum, maxSoFar). Single letters suit only short-lived loop indices.
- **Composition rule (R) of `variable` with `naming_convention`:** A variable's name should describe what it holds (lowerCamelCase), but the name has no effect on its value.

## What it leads to (1)

These concepts need `naming_convention` first.

### `naming_convention` comes before `named_constants`

*final constants in UPPER\_CASE instead of magic numbers*

- **Edge:** `pre:naming_convention->named_constants`
- **Exact edge logic:** Constants have their own naming convention.
- **Grounding:** book\_passage
- **Composition rule (R) of `naming_convention` with `named_constants`:** Constants are written in ALL\_CAPS with underscores, which sets them apart from lowerCamelCase variables and signals that they never change.
- **Composition rule (R) of `named_constants` with `naming_convention`:** Constants follow their own convention, ALL\_CAPS\_WITH\_UNDERSCORES, which sets them apart from lowerCamelCase variables.

## Learned alongside (0)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

No parallel edge touches this concept.

## Misconceptions (4)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### CrypticVariableName

- **Edge:** `naming_convention` &rarr; `CrypticVariableName` (misconception)
- **Exact edge logic (the wrong rule):** Uses abbreviated names such as c or s for a variable whose role is not a temporary loop counter (e.g. c for a count).
- **Twin logic (the right rule):** Use names that indicate what the variables mean.
- **Wrong belief (on the node):** Uses abbreviated names such as c or s for a variable whose role is not a temporary loop counter (e.g. c for a count).
- **Correct rule (on the node):** Use names that indicate what the variables mean.
- **Provenance:** rule\_dictionary
- **Role of this concept:** primary
- **L0 way linked to it:** no

### MagicNumbers

- **Edge:** `naming_convention` &rarr; `MagicNumbers` (misconception)
- **Exact edge logic (the wrong rule):** Writing 7 or 0.0825 directly in formulas is as clear as using a named constant.
- **Twin logic (the right rule):** Give fixed values a final, UPPER\_CASE name and use the name.
- **Wrong belief (on the node):** Writing 7 or 0.0825 directly in formulas is as clear as using a named constant.
- **Correct rule (on the node):** Give fixed values a final, UPPER\_CASE name and use the name.
- **Provenance:** rule\_dictionary
- **Role of this concept:** context
- **L0 way linked to it:** no
- **Edge `named_constants` &rarr; `MagicNumbers`, exact edge logic:** Writing 7 or 0.0825 directly in formulas is as clear as using a named constant. **Twin logic:** Give fixed values a final, UPPER\_CASE name and use the name. (role: primary)

### NameGivesMeaning

- **Edge:** `naming_convention` &rarr; `NameGivesMeaning` (misconception)
- **Exact edge logic (the wrong rule):** Naming a variable max (or average) makes it hold the largest value (or the average) without code that computes it.
- **Twin logic (the right rule):** A name only labels the variable for human readers; only the statements that assign to it decide its value.
- **Wrong belief (on the node):** Naming a variable max (or average) makes it hold the largest value (or the average) without code that computes it.
- **Correct rule (on the node):** A name only labels the variable for human readers; only the statements that assign to it decide its value.
- **Provenance:** published
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [1] misconception, exact rule:** wrong rule: Naming a variable max (or average) makes it hold the largest value (or the average) without code that computes it. Right rule: A name only labels the variable for human readers; only the statements that assign to it decide its value.
- **L0 way [2] inconsistent\_trace, exact rule:** Points to LT (names carry no meaning at run time, so trace by values). Applied unevenly, a student traces values for most variables but assumes that largest is larger than smallest because of its name. (here mixing in: "Naming a variable max (or average) makes it hold the largest value (or the average) without code that computes it")
- **Edge `variable` &rarr; `NameGivesMeaning`, exact edge logic:** Naming a variable max (or average) makes it hold the largest value (or the average) without code that computes it. **Twin logic:** A name only labels the variable for human readers; only the statements that assign to it decide its value. (role: context)

### NameNotCamelCase

- **Edge:** `naming_convention` &rarr; `NameNotCamelCase` (misconception)
- **Exact edge logic (the wrong rule):** Writes variable names as Total, total\_count or TOTALCOUNT.
- **Twin logic (the right rule):** Local variable names are written in lowerCamelCase.
- **Wrong belief (on the node):** Writes variable names as Total, total\_count or TOTALCOUNT.
- **Correct rule (on the node):** Local variable names are written in lowerCamelCase.
- **Provenance:** rule\_dictionary
- **Role of this concept:** primary
- **L0 way linked to it:** no

## Errors (0)

An error edge states the rule that gets broken in a program, and the right rule.

The graph has no error edge from this concept.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for naming convention: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to naming convention agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

- **Edge:** `naming_convention` &rarr; `naming_convention@L0` (has_level)
- **Exact edge logic:** naming convention -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (3 ways).

Ways (3), each with its exact rule:

- **[0] everyday\_reading** (rule type E, folk-meaning rule): In everyday language a label tells you what a thing is (a jar labelled 'sugar' holds sugar), so novices expect a variable called max to hold the maximum. Java gives names no meaning: conventions exist only for human readers, and only assignments decide values.
- **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `NameGivesMeaning`: wrong rule: Naming a variable max (or average) makes it hold the largest value (or the average) without code that computes it. Right rule: A name only labels the variable for human readers; only the statements that assign to it decide its value.
- **[2] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `NameGivesMeaning`: Points to LT (names carry no meaning at run time, so trace by values). Applied unevenly, a student traces values for most variables but assumes that largest is larger than smallest because of its name. (here mixing in: "Naming a variable max (or average) makes it hold the largest value (or the average) without code that computes it")

### L1: Unistructural / atom x text surface

L1 for naming convention: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

- **Edge:** `naming_convention` &rarr; `naming_convention@L1` (has_level)
- **Exact edge logic:** naming convention -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

Ways (2), each with its exact rule:

- **[0] names\_the\_element** (rule type N, identity rule): Naming convention: a style rule (not a language rule) for choosing identifiers. Variables and methods use lowerCamelCase, classes UpperCamelCase, constants UPPER\_CASE\_WITH\_UNDERSCORES, and names describe meaning.
- **[1] states\_the\_rule** (rule type S, declarative rule): Variable names begin with a lowercase letter and capitalize each later word (firstName). Class names begin with a capital. Constants are all uppercase with \_ between words. Names should indicate what the variable means.

### L2: Multistructural / block x execution / preoperational

L2 for naming convention: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

- **Edge:** `naming_convention` &rarr; `naming_convention@L2` (has_level)
- **Exact edge logic:** naming convention -&gt; L2 (Multistructural): the answer applies the rules of naming convention to every part of the code, in order (3 ways).

Ways (3), each with its exact rule:

- **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): Conventions have no execution order: the compiler checks only that an identifier is legal and declared, never whether it follows convention.
- **[1] output\_prediction** (rule type OP, evaluation / result rule): A program's output does not depend on its names: renaming total to t everywhere gives identical results.
- **[2] one\_step\_execution** (rule type OS, state-transition rule): Following or breaking a convention changes no state; it only changes how readable the code is.

### L3: Relational / relations x function (concrete operational begins)

L3 for naming convention: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

- **Edge:** `naming_convention` &rarr; `naming_convention@L3` (has_level)
- **Exact edge logic:** naming convention -&gt; L3 (Relational): the answer relates the parts (3 ways).

Ways (3), each with its exact rule:

- **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Each variable's name should describe what it holds (count, sum, maxSoFar). Single letters suit only short-lived loop indices.
- **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Constants are written in ALL\_CAPS with underscores, which sets them apart from lowerCamelCase variables and signals that they never change.
- **[2] purpose\_of\_the\_whole** (rule type P, plan / role rule): Good names make each variable's role visible (sum for a gatherer, count for a counter, max for a most-wanted holder, i for a stepper), so a reader can recognize the plan without tracing.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for naming convention: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

- **Edge:** `naming_convention` &rarr; `naming_convention@L4` (has_level)
- **Exact edge logic:** naming convention -&gt; L4 (Extended abstract): the answer reasons beyond the given code (4 ways).

Ways (4), each with its exact rule:

- **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `NameGivesMeaning`: Renaming consistently keeps the program's meaning, because what it computes does not depend on names. A misleading name (max holding a minimum) still compiles and runs the same, but readers draw wrong conclusions.
- **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Apply the conventions to every name you write. Short names fit only tiny scopes (loop index i, coordinates x and y). No naming convention can replace the code that actually computes the value.
- **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: A name does not compute or guarantee a value. Kind: silent logic error. Trigger class: Trusting a descriptive name instead of the code (e.g. assuming average holds the mean although it was never divided): wrong output that the name hides.
- **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: Names that differ only in case are different identifiers. Kind: silent logic error. Trigger class: Declaring both count and Count (or total and Total) and updating one while printing the other.

## Same topic

`naming_convention` belongs to the topic **Data types and terminology (literals, identifiers, variables, declarations, assignment, expressions)** (`topic1.2.a`). The topic also contains: `assignment`, `chained_assignment`, `data_type`, `declaration`, `definite_assignment`, `expression`, `identifier`, `literal`, `named_constants`, `operator_precedence`, `primitive_type`, `program_trace`, `variable`, `variable_swap`.

## Rules of the concept (15)

- **Book** (TJ-2e, p. 18 (pdf 40)): "Variable names usually begin with a lowercase letter, in contrast to class names (like Hello) that start with a capital letter."
- **Book** (TJ-2e, p. 18 (pdf 40)): "When a variable name contains more than one word (like firstName), it is conventional to capitalize the first letter of each subsequent word."
- **Book** (OT-Variables, ): "When choosing a name for your variables, use full words instead of cryptic abbreviations."
- **Book** (OT-Variables, ): "If the name you choose consists of only one word, spell that word in all lowercase letters. If it consists of more than one word, capitalize the first letter of each subsequent word."
- **Book** (OCC-Naming, ): "Variable names should be short yet meaningful."
- **Book** (OCC-Naming, ): "One-character variable names should be avoided except for temporary "throwaway" variables."
- **Book** (OCC-Naming, ): "Common names for temporary variables are i, j, k, m, and n for integers; c, d, and e for characters."
- **Book** (GJS, ): "Local variable names are written in lowerCamelCase."
- **E** (folk-meaning rule): In everyday language a label tells you what a thing is (a jar labelled 'sugar' holds sugar), so novices expect a variable called max to hold the maximum. Java gives names no meaning: conventions exist only for human readers, and only assignments decide values.
- **M** (wrong rule / right rule): NameGivesMeaning: wrong: Naming a variable max (or average) makes it hold the largest value (or the average) without code that computes it. \| right: A name only labels the variable for human readers; only the statements that assign to it decide its value.
- **T** (uneven-application rule): Points to LT (names carry no meaning at run time, so trace by values). Applied unevenly, a student traces values for most variables but assumes that largest is larger than smallest because of its name.
- **N** (identity rule): Naming convention: a style rule (not a language rule) for choosing identifiers. Variables and methods use lowerCamelCase, classes UpperCamelCase, constants UPPER\_CASE\_WITH\_UNDERSCORES, and names describe meaning.
- **S** (declarative rule): Variable names begin with a lowercase letter and capitalize each later word (firstName). Class names begin with a capital. Constants are all uppercase with \_ between words. Names should indicate what the variable means.
- **LT** (operational sequencing rule): Conventions have no execution order: the compiler checks only that an identifier is legal and declared, never whether it follows convention.
- **OP** (evaluation / result rule): A program's output does not depend on its names: renaming total to t everywhere gives identical results.
- **OS** (state-transition rule): Following or breaking a convention changes no state; it only changes how readable the code is.
- **R** (composition rule (with a neighbour)): with variable: Each variable's name should describe what it holds (count, sum, maxSoFar). Single letters suit only short-lived loop indices.
- **R** (composition rule (with a neighbour)): with named\_constants: Constants are written in ALL\_CAPS with underscores, which sets them apart from lowerCamelCase variables and signals that they never change.
- **P** (plan / role rule): Good names make each variable's role visible (sum for a gatherer, count for a counter, max for a most-wanted holder, i for a stepper), so a reader can recognize the plan without tracing.
- **C** (conservation rule): Renaming consistently keeps the program's meaning, because what it computes does not depend on names. A misleading name (max holding a minimum) still compiles and runs the same, but readers draw wrong conclusions.
- **D** (error rule): rule broken: A name does not compute or guarantee a value. (silent logic error)
- **D** (error rule): rule broken: Names that differ only in case are different identifiers. (silent logic error)
- **X** (applicability rule): Apply the conventions to every name you write. Short names fit only tiny scopes (loop index i, coordinates x and y). No naming convention can replace the code that actually computes the value.

## How it is found in code and answers (reader block)

- **Aliases:** naming convention, java convention, camel case, camelcase, lowercamelcase
- **Code patterns:** none
- **Operator symbols:** none
- **Java types:** none
- **Signal bad\_name\_regex** (scope program, decisive): `(?<!final )\b(?:int|double|char|boolean|long|String|float|short|byte)(?:\[\])*\s+(?:[A-Z]\w*|[a-z][a-z0-9]*_\w+)(?=\s*[=;,])`
- **Signal bad\_class\_name** (scope program, decisive): `\bclass\s+[a-z]\w*`

## The whole prerequisite chain

- **Everything it builds on (5):** `data_type`, `identifier`, `literal`, `primitive_type`, `variable`
- **Everything that builds on it (1):** `named_constants`

## Every edge in this view and its exact edge logic (28)

All the edges drawn in the picture, in the order: prerequisite, parallel, misconception, error, has_level, contains.

**1. `naming_convention` &rarr; `named_constants`** (prerequisite)

- **Exact edge logic:** Constants have their own naming convention.
- **Grounding:** book\_passage
- **Composition rule (R) of `naming_convention` with `named_constants`:** Constants are written in ALL\_CAPS with underscores, which sets them apart from lowerCamelCase variables and signals that they never change.
- **Composition rule (R) of `named_constants` with `naming_convention`:** Constants follow their own convention, ALL\_CAPS\_WITH\_UNDERSCORES, which sets them apart from lowerCamelCase variables.

**2. `variable` &rarr; `naming_convention`** (prerequisite)

- **Exact edge logic:** Each variable gets a name; the convention says the name should describe what the variable holds.
- **Grounding:** book\_passage
- **Composition rule (R) of `variable` with `naming_convention`:** A variable's name should describe what it holds (lowerCamelCase), but the name has no effect on its value.
- **Composition rule (R) of `naming_convention` with `variable`:** Each variable's name should describe what it holds (count, sum, maxSoFar). Single letters suit only short-lived loop indices.

**3. `naming_convention` &rarr; `CrypticVariableName`** (misconception)

- **Exact edge logic (the wrong rule):** Uses abbreviated names such as c or s for a variable whose role is not a temporary loop counter (e.g. c for a count).
- **Twin logic (the right rule):** Use names that indicate what the variables mean.
- **Role:** primary

**4. `naming_convention` &rarr; `MagicNumbers`** (misconception)

- **Exact edge logic (the wrong rule):** Writing 7 or 0.0825 directly in formulas is as clear as using a named constant.
- **Twin logic (the right rule):** Give fixed values a final, UPPER\_CASE name and use the name.
- **Role:** context

**5. `naming_convention` &rarr; `NameGivesMeaning`** (misconception)

- **Exact edge logic (the wrong rule):** Naming a variable max (or average) makes it hold the largest value (or the average) without code that computes it.
- **Twin logic (the right rule):** A name only labels the variable for human readers; only the statements that assign to it decide its value.
- **Role:** primary

**6. `naming_convention` &rarr; `NameNotCamelCase`** (misconception)

- **Exact edge logic (the wrong rule):** Writes variable names as Total, total\_count or TOTALCOUNT.
- **Twin logic (the right rule):** Local variable names are written in lowerCamelCase.
- **Role:** primary

**7. `named_constants` &rarr; `MagicNumbers`** (misconception)

- **Exact edge logic (the wrong rule):** Writing 7 or 0.0825 directly in formulas is as clear as using a named constant.
- **Twin logic (the right rule):** Give fixed values a final, UPPER\_CASE name and use the name.
- **Role:** primary

**8. `variable` &rarr; `NameGivesMeaning`** (misconception)

- **Exact edge logic (the wrong rule):** Naming a variable max (or average) makes it hold the largest value (or the average) without code that computes it.
- **Twin logic (the right rule):** A name only labels the variable for human readers; only the statements that assign to it decide its value.
- **Role:** context

**9. `naming_convention` &rarr; `naming_convention@L0`** (has_level)

- **Exact edge logic:** naming convention -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (3 ways).
  - **[0] everyday\_reading** (rule type E, folk-meaning rule): In everyday language a label tells you what a thing is (a jar labelled 'sugar' holds sugar), so novices expect a variable called max to hold the maximum. Java gives names no meaning: conventions exist only for human readers, and only assignments decide values.
  - **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `NameGivesMeaning`: wrong rule: Naming a variable max (or average) makes it hold the largest value (or the average) without code that computes it. Right rule: A name only labels the variable for human readers; only the statements that assign to it decide its value.
  - **[2] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `NameGivesMeaning`: Points to LT (names carry no meaning at run time, so trace by values). Applied unevenly, a student traces values for most variables but assumes that largest is larger than smallest because of its name. (here mixing in: "Naming a variable max (or average) makes it hold the largest value (or the average) without code that computes it")

**10. `naming_convention` &rarr; `naming_convention@L1`** (has_level)

- **Exact edge logic:** naming convention -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).
  - **[0] names\_the\_element** (rule type N, identity rule): Naming convention: a style rule (not a language rule) for choosing identifiers. Variables and methods use lowerCamelCase, classes UpperCamelCase, constants UPPER\_CASE\_WITH\_UNDERSCORES, and names describe meaning.
  - **[1] states\_the\_rule** (rule type S, declarative rule): Variable names begin with a lowercase letter and capitalize each later word (firstName). Class names begin with a capital. Constants are all uppercase with \_ between words. Names should indicate what the variable means.

**11. `naming_convention` &rarr; `naming_convention@L2`** (has_level)

- **Exact edge logic:** naming convention -&gt; L2 (Multistructural): the answer applies the rules of naming convention to every part of the code, in order (3 ways).
  - **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): Conventions have no execution order: the compiler checks only that an identifier is legal and declared, never whether it follows convention.
  - **[1] output\_prediction** (rule type OP, evaluation / result rule): A program's output does not depend on its names: renaming total to t everywhere gives identical results.
  - **[2] one\_step\_execution** (rule type OS, state-transition rule): Following or breaking a convention changes no state; it only changes how readable the code is.

**12. `naming_convention` &rarr; `naming_convention@L3`** (has_level)

- **Exact edge logic:** naming convention -&gt; L3 (Relational): the answer relates the parts (3 ways).
  - **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Each variable's name should describe what it holds (count, sum, maxSoFar). Single letters suit only short-lived loop indices.
  - **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Constants are written in ALL\_CAPS with underscores, which sets them apart from lowerCamelCase variables and signals that they never change.
  - **[2] purpose\_of\_the\_whole** (rule type P, plan / role rule): Good names make each variable's role visible (sum for a gatherer, count for a counter, max for a most-wanted holder, i for a stepper), so a reader can recognize the plan without tracing.

**13. `naming_convention` &rarr; `naming_convention@L4`** (has_level)

- **Exact edge logic:** naming convention -&gt; L4 (Extended abstract): the answer reasons beyond the given code (4 ways).
  - **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `NameGivesMeaning`: Renaming consistently keeps the program's meaning, because what it computes does not depend on names. A misleading name (max holding a minimum) still compiles and runs the same, but readers draw wrong conclusions.
  - **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Apply the conventions to every name you write. Short names fit only tiny scopes (loop index i, coordinates x and y). No naming convention can replace the code that actually computes the value.
  - **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: A name does not compute or guarantee a value. Kind: silent logic error. Trigger class: Trusting a descriptive name instead of the code (e.g. assuming average holds the mean although it was never divided): wrong output that the name hides.
  - **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: Names that differ only in case are different identifiers. Kind: silent logic error. Trigger class: Declaring both count and Count (or total and Total) and updating one while printing the other.

**14. `topic1.2.a` &rarr; `naming_convention`** (contains)

- topic `topic1.2.a` contains `naming_convention`

**15. `topic1.2.a` &rarr; `assignment`** (contains)

- topic `topic1.2.a` contains `assignment`

**16. `topic1.2.a` &rarr; `chained_assignment`** (contains)

- topic `topic1.2.a` contains `chained_assignment`

**17. `topic1.2.a` &rarr; `data_type`** (contains)

- topic `topic1.2.a` contains `data_type`

**18. `topic1.2.a` &rarr; `declaration`** (contains)

- topic `topic1.2.a` contains `declaration`

**19. `topic1.2.a` &rarr; `definite_assignment`** (contains)

- topic `topic1.2.a` contains `definite_assignment`

**20. `topic1.2.a` &rarr; `expression`** (contains)

- topic `topic1.2.a` contains `expression`

**21. `topic1.2.a` &rarr; `identifier`** (contains)

- topic `topic1.2.a` contains `identifier`

**22. `topic1.2.a` &rarr; `literal`** (contains)

- topic `topic1.2.a` contains `literal`

**23. `topic1.2.a` &rarr; `named_constants`** (contains)

- topic `topic1.2.a` contains `named_constants`

**24. `topic1.2.a` &rarr; `operator_precedence`** (contains)

- topic `topic1.2.a` contains `operator_precedence`

**25. `topic1.2.a` &rarr; `primitive_type`** (contains)

- topic `topic1.2.a` contains `primitive_type`

**26. `topic1.2.a` &rarr; `program_trace`** (contains)

- topic `topic1.2.a` contains `program_trace`

**27. `topic1.2.a` &rarr; `variable`** (contains)

- topic `topic1.2.a` contains `variable`

**28. `topic1.2.a` &rarr; `variable_swap`** (contains)

- topic `topic1.2.a` contains `variable_swap`
