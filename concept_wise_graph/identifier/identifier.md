# identifier (`identifier`)

a name for a variable, method or class; case-sensitive, no spaces, not a keyword

Section 1.2 Built-in Types of Data, topic 1.2.a Data types and terminology (literals, identifiers, variables, declarations, assignment, expressions).

![The knowledge graph around identifier](identifier.png)

## At a glance

- **Needs first:** nothing
- **Leads to:** `declaration`, `variable`
- **Learned alongside:** nothing
- **Misconceptions:** `IdentifierCaseInsensitive`, `NoReservedWords`
- **Errors:** `MisspelledIdentifier`, `UndeclaredOrRenamedVariable`
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 31 edges around this concept. The edge logic, the wrong and right rules and the exact rules of the ways are copied word for word from the graph.

## To work on (0)

Nothing is missing for this concept.

## What it needs first (0)

A prerequisite edge means the other concept has to be understood before `identifier`.

No prerequisite edge leads into this concept.

## What it leads to (2)

These concepts need `identifier` first.

### `identifier` comes before `declaration`

*int x; -- introduces a variable name and its type*

- **Edge:** `pre:identifier->declaration`
- **Exact edge logic:** A declaration pairs a type with an identifier, e.g. int count;.
- **Grounding:** book\_passage
- **Composition rule (R) of `identifier` with `declaration`:** A declaration binds the identifier to a type. Every later use must repeat exactly that spelling, or the compiler cannot resolve it.
- **Composition rule (R) of `declaration` with `identifier`:** A declaration binds a legal identifier to a type, and that identifier must not already be declared in the same scope.

### `identifier` comes before `variable`

*a named, typed box that holds a value*

- **Edge:** `pre:identifier->variable`
- **Exact edge logic:** Every variable is named by an identifier that follows the naming rules.
- **Grounding:** book\_passage
- **Composition rule (R) of `identifier` with `variable`:** Each variable is named by one identifier, which must be unique within its scope: declaring a second local with the same name in that scope is a compile error.
- **Composition rule (R) of `variable` with `identifier`:** Each variable is named by an identifier, which must be legal and unique within the variable's scope.

## Learned alongside (0)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

No parallel edge touches this concept.

## Misconceptions (2)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### IdentifierCaseInsensitive

- **Edge:** `identifier` &rarr; `IdentifierCaseInsensitive` (misconception)
- **Exact edge logic (the wrong rule):** System.out.Println and System.out.println name the same method.
- **Twin logic (the right rule):** Java is case-sensitive: names of variables, methods and classes that differ only in capitalization are different names.
- **Wrong belief (on the node):** System.out.Println and System.out.println name the same method.
- **Correct rule (on the node):** Java is case-sensitive: names of variables, methods and classes that differ only in capitalization are different names.
- **Provenance:** textbook
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [1] misconception, exact rule:** wrong rule: System.out.Println and System.out.println name the same method. Right rule: Java is case-sensitive: names of variables, methods and classes that differ only in capitalization are different names.
- **L0 way [3] inconsistent\_trace, exact rule:** Points to LT (a name refers to the declaration with exactly that spelling in scope). Applied unevenly, a student treats Count and count as one variable in one statement but as two in another. (here mixing in: "System.out.Println and System.out.println name the same method")
- **Edge `println` &rarr; `IdentifierCaseInsensitive`, exact edge logic:** System.out.Println and System.out.println name the same method. **Twin logic:** Java is case-sensitive: names of variables, methods and classes that differ only in capitalization are different names. (role: context)

### NoReservedWords

- **Edge:** `identifier` &rarr; `NoReservedWords` (misconception)
- **Exact edge logic (the wrong rule):** A keyword such as int or class can be used as a variable name.
- **Twin logic (the right rule):** Keywords are reserved by Java and cannot be used as variable names.
- **Wrong belief (on the node):** keywords may be reused as identifiers
- **Correct rule (on the node):** Keywords are reserved by Java and cannot be used as variable names.
- **Provenance:** published
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [2] misconception, exact rule:** wrong rule: keywords may be reused as identifiers. Right rule: Keywords are reserved by Java and cannot be used as variable names.
- **Edge `variable` &rarr; `NoReservedWords`, exact edge logic:** A keyword such as int or class can be used as a variable name. **Twin logic:** Keywords are reserved by Java and cannot be used as variable names. (role: context)

## Errors (2)

An error edge states the rule that gets broken in a program, and the right rule.

### MisspelledIdentifier

- **Edge:** `identifier` &rarr; `MisspelledIdentifier` (error)
- **Exact edge logic (the wrong rule):** Writes Sytem.out.prinln or a misspelled variable name.
- **Twin logic (the right rule):** Every name must be spelled exactly, including capitalization.
- **Wrong belief (on the node):** Writes Sytem.out.prinln or a misspelled variable name.
- **Correct rule (on the node):** Every name must be spelled exactly, including capitalization.
- **Provenance:** textbook
- **Role of this concept:** primary
- **Edge `compile_time_error` &rarr; `MisspelledIdentifier`, exact edge logic:** Writes Sytem.out.prinln or a misspelled variable name. **Twin logic:** Every name must be spelled exactly, including capitalization. (role: context)

### UndeclaredOrRenamedVariable

- **Edge:** `identifier` &rarr; `UndeclaredOrRenamedVariable` (error)
- **Exact edge logic (the wrong rule):** Uses a variable that was never declared, or under a different name (studentTotal vs total).
- **Twin logic (the right rule):** Every variable must be declared, and used with exactly the declared name.
- **Wrong belief (on the node):** Uses a variable that was never declared, or under a different name (studentTotal vs total).
- **Correct rule (on the node):** Every variable must be declared, and used with exactly the declared name.
- **Provenance:** textbook
- **Role of this concept:** context
- **Edge `declaration` &rarr; `UndeclaredOrRenamedVariable`, exact edge logic:** Uses a variable that was never declared, or under a different name (studentTotal vs total). **Twin logic:** Every variable must be declared, and used with exactly the declared name. (role: context)
- **Edge `variable` &rarr; `UndeclaredOrRenamedVariable`, exact edge logic:** Uses a variable that was never declared, or under a different name (studentTotal vs total). **Twin logic:** Every variable must be declared, and used with exactly the declared name. (role: primary)

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for identifier: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to identifier agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

- **Edge:** `identifier` &rarr; `identifier@L0` (has_level)
- **Exact edge logic:** identifier -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (4 ways).

Ways (4), each with its exact rule:

- **[0] everyday\_reading** (rule type E, folk-meaning rule): In English, Total, total and TOTAL are the same word, and names may contain spaces or hyphens (max-value). Java identifiers are case-sensitive and may use only letters, digits, \_ and $, so total and Total are different names and max-value is a subtraction.
- **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `IdentifierCaseInsensitive`: wrong rule: System.out.Println and System.out.println name the same method. Right rule: Java is case-sensitive: names of variables, methods and classes that differ only in capitalization are different names.
- **[2] misconception** (rule type M, wrong rule / right rule) &rarr; `NoReservedWords`: wrong rule: keywords may be reused as identifiers. Right rule: Keywords are reserved by Java and cannot be used as variable names.
- **[3] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `IdentifierCaseInsensitive`: Points to LT (a name refers to the declaration with exactly that spelling in scope). Applied unevenly, a student treats Count and count as one variable in one statement but as two in another. (here mixing in: "System.out.Println and System.out.println name the same method")

### L1: Unistructural / atom x text surface

L1 for identifier: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

- **Edge:** `identifier` &rarr; `identifier@L1` (has_level)
- **Exact edge logic:** identifier -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

Ways (2), each with its exact rule:

- **[0] names\_the\_element** (rule type N, identity rule): Identifier: a name for a variable, method or class, made of letters, digits, \_ and $ and not starting with a digit.
- **[1] states\_the\_rule** (rule type S, declarative rule): An identifier is a sequence of letters, digits, \_ and $ whose first character is not a digit. Identifiers are case-sensitive, and reserved words such as int, public or class cannot be used.

### L2: Multistructural / block x execution / preoperational

L2 for identifier: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

- **Edge:** `identifier` &rarr; `identifier@L2` (has_level)
- **Exact edge logic:** identifier -&gt; L2 (Multistructural): the answer applies the rules of identifier to every part of the code, in order (3 ways).

Ways (3), each with its exact rule:

- **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): When an identifier appears, the compiler looks it up by exact spelling among the declarations in scope (an error if none matches). At run time a variable's name is replaced by that variable's current value.
- **[1] output\_prediction** (rule type OP, evaluation / result rule): An identifier used as an expression yields the current value of the variable it names, with that variable's declared type. abc, Ab$, abc123 and a\_b are legal names; Ab\*, 1abc and a+b are not.
- **[2] one\_step\_execution** (rule type OS, state-transition rule): A name does nothing at run time. Only an assignment (or ++ or op=) with the name on its left changes the variable it names.

### L3: Relational / relations x function (concrete operational begins)

L3 for identifier: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

- **Edge:** `identifier` &rarr; `identifier@L3` (has_level)
- **Exact edge logic:** identifier -&gt; L3 (Relational): the answer relates the parts (3 ways).

Ways (3), each with its exact rule:

- **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Each variable is named by one identifier, which must be unique within its scope: declaring a second local with the same name in that scope is a compile error.
- **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): A declaration binds the identifier to a type. Every later use must repeat exactly that spelling, or the compiler cannot resolve it.
- **[2] purpose\_of\_the\_whole** (rule type P, plan / role rule): Identifiers let code refer to values and code by name. Descriptive names make each variable's role readable to people, though names have no effect on what the program computes.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for identifier: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

- **Edge:** `identifier` &rarr; `identifier@L4` (has_level)
- **Exact edge logic:** identifier -&gt; L4 (Extended abstract): the answer reasons beyond the given code (6 ways).

Ways (6), each with its exact rule:

- **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `IdentifierCaseInsensitive`: Renaming an identifier consistently at its declaration and every use leaves behavior unchanged. Renaming only some occurrences, or changing only the capitalization, breaks compilation with 'cannot find symbol'.
- **[1] diagnose\_an\_error** (rule type D, error rule): rule broken: Identifiers are case-sensitive and must match a declaration exactly; a name that matches nothing in scope cannot be resolved. Kind: compile-time. Trigger class: Any use whose spelling or capitalization differs from the declaration or library name (Sytem, prinln, Println, studentTotl): compiler reports 'cannot find symbol'.
- **[2] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Every variable, method and class needs an identifier. Pick descriptive lowerCamelCase names, and use single letters only for short-lived loop indices or standard maths symbols. A name never stands in for a value; only literals and expressions do that.
- **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: Every variable must be declared (with a type) before use and referred to by exactly the declared name, inside its scope. Kind: compile-time. Trigger class: Use of a name that was never declared, was declared under another name, or is used outside the block where it was declared: 'cannot find symbol' (one missing declaration can produce several errors).
- **[4] diagnose\_an\_error** (rule type D, error rule): rule broken: Reserved words cannot be used as identifiers. Kind: compile-time. Trigger class: Naming a variable new, class, int, public and so on: '&lt;identifier&gt; expected' or 'not a statement'.
- **[5] diagnose\_an\_error** (rule type D, error rule): rule broken: An identifier may not start with a digit or contain spaces or operator symbols. Kind: compile-time. Trigger class: Names like 2ndValue, max value or max-value: syntax errors, or max - value parsed as a subtraction.

## Same topic

`identifier` belongs to the topic **Data types and terminology (literals, identifiers, variables, declarations, assignment, expressions)** (`topic1.2.a`). The topic also contains: `assignment`, `chained_assignment`, `data_type`, `declaration`, `definite_assignment`, `expression`, `literal`, `named_constants`, `naming_convention`, `operator_precedence`, `primitive_type`, `program_trace`, `variable`, `variable_swap`.

## Rules of the concept (18)

- **Book** (SW-1e, p. 15 (pdf 25)): "An identifier is a sequence of letters, digits, \_, and $, the first of which is not a digit."
- **Book** (SW-1e, p. 15 (pdf 25)): "Identifiers are case-sensitive, so Ab, ab, and AB are all different names."
- **Book** (OT-Variables, ): "Variable names are case-sensitive."
- **Book** (OT-Variables, ): "White space is not permitted."
- **Book** (OT-Variables, ): "Also keep in mind that the name you choose must not be a keyword or reserved word."
- **E** (folk-meaning rule): In English, Total, total and TOTAL are the same word, and names may contain spaces or hyphens (max-value). Java identifiers are case-sensitive and may use only letters, digits, \_ and $, so total and Total are different names and max-value is a subtraction.
- **M** (wrong rule / right rule): IdentifierCaseInsensitive: wrong: System.out.Println and System.out.println name the same method. \| right: Java is case-sensitive: names of variables, methods and classes that differ only in capitalization are different names.
- **M** (wrong rule / right rule): NoReservedWords: wrong: keywords may be reused as identifiers \| right: Keywords are reserved by Java and cannot be used as variable names.
- **T** (uneven-application rule): Points to LT (a name refers to the declaration with exactly that spelling in scope). Applied unevenly, a student treats Count and count as one variable in one statement but as two in another.
- **N** (identity rule): Identifier: a name for a variable, method or class, made of letters, digits, \_ and $ and not starting with a digit.
- **S** (declarative rule): An identifier is a sequence of letters, digits, \_ and $ whose first character is not a digit. Identifiers are case-sensitive, and reserved words such as int, public or class cannot be used.
- **LT** (operational sequencing rule): When an identifier appears, the compiler looks it up by exact spelling among the declarations in scope (an error if none matches). At run time a variable's name is replaced by that variable's current value.
- **OP** (evaluation / result rule): An identifier used as an expression yields the current value of the variable it names, with that variable's declared type. abc, Ab$, abc123 and a\_b are legal names; Ab\*, 1abc and a+b are not.
- **OS** (state-transition rule): A name does nothing at run time. Only an assignment (or ++ or op=) with the name on its left changes the variable it names.
- **R** (composition rule (with a neighbour)): with variable: Each variable is named by one identifier, which must be unique within its scope: declaring a second local with the same name in that scope is a compile error.
- **R** (composition rule (with a neighbour)): with declaration: A declaration binds the identifier to a type. Every later use must repeat exactly that spelling, or the compiler cannot resolve it.
- **P** (plan / role rule): Identifiers let code refer to values and code by name. Descriptive names make each variable's role readable to people, though names have no effect on what the program computes.
- **C** (conservation rule): Renaming an identifier consistently at its declaration and every use leaves behavior unchanged. Renaming only some occurrences, or changing only the capitalization, breaks compilation with 'cannot find symbol'.
- **D** (error rule): rule broken: Identifiers are case-sensitive and must match a declaration exactly; a name that matches nothing in scope cannot be resolved. (compile-time)
- **D** (error rule): rule broken: Every variable must be declared (with a type) before use and referred to by exactly the declared name, inside its scope. (compile-time)
- **D** (error rule): rule broken: Reserved words cannot be used as identifiers. (compile-time)
- **D** (error rule): rule broken: An identifier may not start with a digit or contain spaces or operator symbols. (compile-time)
- **X** (applicability rule): Every variable, method and class needs an identifier. Pick descriptive lowerCamelCase names, and use single letters only for short-lived loop indices or standard maths symbols. A name never stands in for a value; only literals and expressions do that.

## How it is found in code and answers (reader block)

- **Aliases:** identifier, name of the variable, variable name
- **Code patterns:** `\b[A-Za-z_]\w*\b`
- **Operator symbols:** none
- **Java types:** none

## The whole prerequisite chain

- **Everything it builds on (0):** nothing
- **Everything that builds on it (80):** `accumulator_pattern`, `animation`, `api`, `array_copy`, `array_exchange`, `array_reversal`, `array_traversal`, `assignment`, `boolean_expression`, `boolean_flag_array`, `break_statement`, `chained_assignment`, `comparison_operators`, `compound_assignment`, `conditional_operator`, `continue_statement`, `convergence_rate`, `convergence_test`, `coordinate_scaling`, `counter_pattern`, `dangling_else`, `debugging`, `declaration`, `definite_assignment`, `do_while_loop`, `drawing_shapes`, `else_if_chain`, `enhanced_for`, `expression`, `fencepost_loop`, `flag_search_loop`, `for_loop`, `frequency_counting`, `function_plotting`, `if_else_statement`, `if_statement`, `increment_operators`, `infinite_loop`, `labeled_break`, `loop_body`, `loop_control`, `loop_invariant_reasoning`, `loop_performance`, `loop_scope`, `loop_variable`, `math_library`, `math_random`, `math_round`, `matrix_operations`, `method_call`, `monte_carlo_simulation`, `mouse_interaction`, `named_constants`, `naming_convention`, `nested_conditionals`, `nested_loops`, `number_conversion`, `off_by_one_error`, `operator_precedence`, `power_method`, `program_state`, `program_trace`, `random_move`, `row_major_order`, `running_extreme`, `sampling_without_replacement`, `sentinel_loop`, `shuffle`, `side_effect_order`, `simulation_loop`, `standard_audio`, `standard_drawing`, `switch_statement`, `syntax_template`, `testing`, `trig_functions`, `two_models`, `variable`, `variable_swap`, `while_loop`

## Every edge in this view and its exact edge logic (31)

All the edges drawn in the picture, in the order: prerequisite, parallel, misconception, error, has_level, contains.

**1. `identifier` &rarr; `declaration`** (prerequisite)

- **Exact edge logic:** A declaration pairs a type with an identifier, e.g. int count;.
- **Grounding:** book\_passage
- **Composition rule (R) of `identifier` with `declaration`:** A declaration binds the identifier to a type. Every later use must repeat exactly that spelling, or the compiler cannot resolve it.
- **Composition rule (R) of `declaration` with `identifier`:** A declaration binds a legal identifier to a type, and that identifier must not already be declared in the same scope.

**2. `identifier` &rarr; `variable`** (prerequisite)

- **Exact edge logic:** Every variable is named by an identifier that follows the naming rules.
- **Grounding:** book\_passage
- **Composition rule (R) of `identifier` with `variable`:** Each variable is named by one identifier, which must be unique within its scope: declaring a second local with the same name in that scope is a compile error.
- **Composition rule (R) of `variable` with `identifier`:** Each variable is named by an identifier, which must be legal and unique within the variable's scope.

**3. `identifier` &rarr; `IdentifierCaseInsensitive`** (misconception)

- **Exact edge logic (the wrong rule):** System.out.Println and System.out.println name the same method.
- **Twin logic (the right rule):** Java is case-sensitive: names of variables, methods and classes that differ only in capitalization are different names.
- **Role:** primary

**4. `identifier` &rarr; `NoReservedWords`** (misconception)

- **Exact edge logic (the wrong rule):** A keyword such as int or class can be used as a variable name.
- **Twin logic (the right rule):** Keywords are reserved by Java and cannot be used as variable names.
- **Role:** primary

**5. `println` &rarr; `IdentifierCaseInsensitive`** (misconception)

- **Exact edge logic (the wrong rule):** System.out.Println and System.out.println name the same method.
- **Twin logic (the right rule):** Java is case-sensitive: names of variables, methods and classes that differ only in capitalization are different names.
- **Role:** context

**6. `variable` &rarr; `NoReservedWords`** (misconception)

- **Exact edge logic (the wrong rule):** A keyword such as int or class can be used as a variable name.
- **Twin logic (the right rule):** Keywords are reserved by Java and cannot be used as variable names.
- **Role:** context

**7. `identifier` &rarr; `MisspelledIdentifier`** (error)

- **Exact edge logic (the wrong rule):** Writes Sytem.out.prinln or a misspelled variable name.
- **Twin logic (the right rule):** Every name must be spelled exactly, including capitalization.
- **Role:** primary

**8. `identifier` &rarr; `UndeclaredOrRenamedVariable`** (error)

- **Exact edge logic (the wrong rule):** Uses a variable that was never declared, or under a different name (studentTotal vs total).
- **Twin logic (the right rule):** Every variable must be declared, and used with exactly the declared name.
- **Role:** context

**9. `compile_time_error` &rarr; `MisspelledIdentifier`** (error)

- **Exact edge logic (the wrong rule):** Writes Sytem.out.prinln or a misspelled variable name.
- **Twin logic (the right rule):** Every name must be spelled exactly, including capitalization.
- **Role:** context

**10. `declaration` &rarr; `UndeclaredOrRenamedVariable`** (error)

- **Exact edge logic (the wrong rule):** Uses a variable that was never declared, or under a different name (studentTotal vs total).
- **Twin logic (the right rule):** Every variable must be declared, and used with exactly the declared name.
- **Role:** context

**11. `variable` &rarr; `UndeclaredOrRenamedVariable`** (error)

- **Exact edge logic (the wrong rule):** Uses a variable that was never declared, or under a different name (studentTotal vs total).
- **Twin logic (the right rule):** Every variable must be declared, and used with exactly the declared name.
- **Role:** primary

**12. `identifier` &rarr; `identifier@L0`** (has_level)

- **Exact edge logic:** identifier -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (4 ways).
  - **[0] everyday\_reading** (rule type E, folk-meaning rule): In English, Total, total and TOTAL are the same word, and names may contain spaces or hyphens (max-value). Java identifiers are case-sensitive and may use only letters, digits, \_ and $, so total and Total are different names and max-value is a subtraction.
  - **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `IdentifierCaseInsensitive`: wrong rule: System.out.Println and System.out.println name the same method. Right rule: Java is case-sensitive: names of variables, methods and classes that differ only in capitalization are different names.
  - **[2] misconception** (rule type M, wrong rule / right rule) &rarr; `NoReservedWords`: wrong rule: keywords may be reused as identifiers. Right rule: Keywords are reserved by Java and cannot be used as variable names.
  - **[3] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `IdentifierCaseInsensitive`: Points to LT (a name refers to the declaration with exactly that spelling in scope). Applied unevenly, a student treats Count and count as one variable in one statement but as two in another. (here mixing in: "System.out.Println and System.out.println name the same method")

**13. `identifier` &rarr; `identifier@L1`** (has_level)

- **Exact edge logic:** identifier -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).
  - **[0] names\_the\_element** (rule type N, identity rule): Identifier: a name for a variable, method or class, made of letters, digits, \_ and $ and not starting with a digit.
  - **[1] states\_the\_rule** (rule type S, declarative rule): An identifier is a sequence of letters, digits, \_ and $ whose first character is not a digit. Identifiers are case-sensitive, and reserved words such as int, public or class cannot be used.

**14. `identifier` &rarr; `identifier@L2`** (has_level)

- **Exact edge logic:** identifier -&gt; L2 (Multistructural): the answer applies the rules of identifier to every part of the code, in order (3 ways).
  - **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): When an identifier appears, the compiler looks it up by exact spelling among the declarations in scope (an error if none matches). At run time a variable's name is replaced by that variable's current value.
  - **[1] output\_prediction** (rule type OP, evaluation / result rule): An identifier used as an expression yields the current value of the variable it names, with that variable's declared type. abc, Ab$, abc123 and a\_b are legal names; Ab\*, 1abc and a+b are not.
  - **[2] one\_step\_execution** (rule type OS, state-transition rule): A name does nothing at run time. Only an assignment (or ++ or op=) with the name on its left changes the variable it names.

**15. `identifier` &rarr; `identifier@L3`** (has_level)

- **Exact edge logic:** identifier -&gt; L3 (Relational): the answer relates the parts (3 ways).
  - **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Each variable is named by one identifier, which must be unique within its scope: declaring a second local with the same name in that scope is a compile error.
  - **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): A declaration binds the identifier to a type. Every later use must repeat exactly that spelling, or the compiler cannot resolve it.
  - **[2] purpose\_of\_the\_whole** (rule type P, plan / role rule): Identifiers let code refer to values and code by name. Descriptive names make each variable's role readable to people, though names have no effect on what the program computes.

**16. `identifier` &rarr; `identifier@L4`** (has_level)

- **Exact edge logic:** identifier -&gt; L4 (Extended abstract): the answer reasons beyond the given code (6 ways).
  - **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `IdentifierCaseInsensitive`: Renaming an identifier consistently at its declaration and every use leaves behavior unchanged. Renaming only some occurrences, or changing only the capitalization, breaks compilation with 'cannot find symbol'.
  - **[1] diagnose\_an\_error** (rule type D, error rule): rule broken: Identifiers are case-sensitive and must match a declaration exactly; a name that matches nothing in scope cannot be resolved. Kind: compile-time. Trigger class: Any use whose spelling or capitalization differs from the declaration or library name (Sytem, prinln, Println, studentTotl): compiler reports 'cannot find symbol'.
  - **[2] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Every variable, method and class needs an identifier. Pick descriptive lowerCamelCase names, and use single letters only for short-lived loop indices or standard maths symbols. A name never stands in for a value; only literals and expressions do that.
  - **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: Every variable must be declared (with a type) before use and referred to by exactly the declared name, inside its scope. Kind: compile-time. Trigger class: Use of a name that was never declared, was declared under another name, or is used outside the block where it was declared: 'cannot find symbol' (one missing declaration can produce several errors).
  - **[4] diagnose\_an\_error** (rule type D, error rule): rule broken: Reserved words cannot be used as identifiers. Kind: compile-time. Trigger class: Naming a variable new, class, int, public and so on: '&lt;identifier&gt; expected' or 'not a statement'.
  - **[5] diagnose\_an\_error** (rule type D, error rule): rule broken: An identifier may not start with a digit or contain spaces or operator symbols. Kind: compile-time. Trigger class: Names like 2ndValue, max value or max-value: syntax errors, or max - value parsed as a subtraction.

**17. `topic1.2.a` &rarr; `identifier`** (contains)

- topic `topic1.2.a` contains `identifier`

**18. `topic1.2.a` &rarr; `assignment`** (contains)

- topic `topic1.2.a` contains `assignment`

**19. `topic1.2.a` &rarr; `chained_assignment`** (contains)

- topic `topic1.2.a` contains `chained_assignment`

**20. `topic1.2.a` &rarr; `data_type`** (contains)

- topic `topic1.2.a` contains `data_type`

**21. `topic1.2.a` &rarr; `declaration`** (contains)

- topic `topic1.2.a` contains `declaration`

**22. `topic1.2.a` &rarr; `definite_assignment`** (contains)

- topic `topic1.2.a` contains `definite_assignment`

**23. `topic1.2.a` &rarr; `expression`** (contains)

- topic `topic1.2.a` contains `expression`

**24. `topic1.2.a` &rarr; `literal`** (contains)

- topic `topic1.2.a` contains `literal`

**25. `topic1.2.a` &rarr; `named_constants`** (contains)

- topic `topic1.2.a` contains `named_constants`

**26. `topic1.2.a` &rarr; `naming_convention`** (contains)

- topic `topic1.2.a` contains `naming_convention`

**27. `topic1.2.a` &rarr; `operator_precedence`** (contains)

- topic `topic1.2.a` contains `operator_precedence`

**28. `topic1.2.a` &rarr; `primitive_type`** (contains)

- topic `topic1.2.a` contains `primitive_type`

**29. `topic1.2.a` &rarr; `program_trace`** (contains)

- topic `topic1.2.a` contains `program_trace`

**30. `topic1.2.a` &rarr; `variable`** (contains)

- topic `topic1.2.a` contains `variable`

**31. `topic1.2.a` &rarr; `variable_swap`** (contains)

- topic `topic1.2.a` contains `variable_swap`
