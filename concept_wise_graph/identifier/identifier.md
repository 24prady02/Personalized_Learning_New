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

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 31 edges around this concept, each explained in the graph's own words.

## What it needs first (0)

A prerequisite edge means the other concept has to be understood before `identifier`.

No prerequisite edge leads into this concept.

## What it leads to (2)

These concepts need `identifier` first.

### `identifier` comes before `declaration`

*int x; -- introduces a variable name and its type*

A declaration pairs a type with an identifier, e.g. int count;.

- **Grounding:** book passage
- **How `identifier` combines with `declaration`:** A declaration binds the identifier to a type. Every later use must repeat exactly that spelling, or the compiler cannot resolve it.
- **How `declaration` combines with `identifier`:** A declaration binds a legal identifier to a type, and that identifier must not already be declared in the same scope.

### `identifier` comes before `variable`

*a named, typed box that holds a value*

Every variable is named by an identifier that follows the naming rules.

- **Grounding:** book passage
- **How `identifier` combines with `variable`:** Each variable is named by one identifier, which must be unique within its scope: declaring a second local with the same name in that scope is a compile error.
- **How `variable` combines with `identifier`:** Each variable is named by an identifier, which must be legal and unique within the variable's scope.

## Learned alongside (0)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

No parallel edge touches this concept.

## Misconceptions (2)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### IdentifierCaseInsensitive

- **Wrong rule:** System.out.Println and System.out.println name the same method.
- **Right rule:** Java is case-sensitive: names of variables, methods and classes that differ only in capitalization are different names.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: System.out.Println and System.out.println name the same method. Right rule: Java is case-sensitive: names of variables, methods and classes that differ only in capitalization are different names.
- **Shows at level L0 as:** inconsistent trace: Points to LT (a name refers to the declaration with exactly that spelling in scope). Applied unevenly, a student treats Count and count as one variable in one statement but as two in another. (here mixing in: "System.out.Println and System.out.println name the same method")
- **Also an edge from `println`:** System.out.Println and System.out.println name the same method.

### NoReservedWords

- **Wrong rule:** A keyword such as int or class can be used as a variable name.
- **Right rule:** Keywords are reserved by Java and cannot be used as variable names.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: keywords may be reused as identifiers. Right rule: Keywords are reserved by Java and cannot be used as variable names.
- **Also an edge from `variable`:** A keyword such as int or class can be used as a variable name.

## Errors (2)

An error edge states the rule that gets broken in a program, and the right rule.

### MisspelledIdentifier

- **Wrong rule:** Writes Sytem.out.prinln or a misspelled variable name.
- **Right rule:** Every name must be spelled exactly, including capitalization.
- **Role of this concept:** primary
- **Also an edge from `compile_time_error`:** Writes Sytem.out.prinln or a misspelled variable name.

### UndeclaredOrRenamedVariable

- **Wrong rule:** Uses a variable that was never declared, or under a different name (studentTotal vs total).
- **Right rule:** Every variable must be declared, and used with exactly the declared name.
- **Role of this concept:** context
- **Also an edge from `declaration`:** Uses a variable that was never declared, or under a different name (studentTotal vs total).
- **Also an edge from `variable`:** Uses a variable that was never declared, or under a different name (studentTotal vs total).

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for identifier: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to identifier agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

identifier -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (4 ways).

- **everyday reading** (folk-meaning rule): In English, Total, total and TOTAL are the same word, and names may contain spaces or hyphens (max-value). Java identifiers are case-sensitive and may use only letters, digits, \_ and $, so total and Total are different names and max-value is a subtraction.
- **misconception** (wrong rule / right rule; shows `IdentifierCaseInsensitive`): wrong rule: System.out.Println and System.out.println name the same method. Right rule: Java is case-sensitive: names of variables, methods and classes that differ only in capitalization are different names.
- **misconception** (wrong rule / right rule; shows `NoReservedWords`): wrong rule: keywords may be reused as identifiers. Right rule: Keywords are reserved by Java and cannot be used as variable names.
- **inconsistent trace** (uneven-application rule; shows `IdentifierCaseInsensitive`): Points to LT (a name refers to the declaration with exactly that spelling in scope). Applied unevenly, a student treats Count and count as one variable in one statement but as two in another. (here mixing in: "System.out.Println and System.out.println name the same method")

### L1: Unistructural / atom x text surface

L1 for identifier: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

identifier -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

- **names the element** (identity rule): Identifier: a name for a variable, method or class, made of letters, digits, \_ and $ and not starting with a digit.
- **states the rule** (declarative rule): An identifier is a sequence of letters, digits, \_ and $ whose first character is not a digit. Identifiers are case-sensitive, and reserved words such as int, public or class cannot be used.

### L2: Multistructural / block x execution / preoperational

L2 for identifier: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

identifier -&gt; L2 (Multistructural): the answer applies the rules of identifier to every part of the code, in order (3 ways).

- **line by line trace** (operational sequencing rule): When an identifier appears, the compiler looks it up by exact spelling among the declarations in scope (an error if none matches). At run time a variable's name is replaced by that variable's current value.
- **output prediction** (evaluation / result rule): An identifier used as an expression yields the current value of the variable it names, with that variable's declared type. abc, Ab$, abc123 and a\_b are legal names; Ab\*, 1abc and a+b are not.
- **one step execution** (state-transition rule): A name does nothing at run time. Only an assignment (or ++ or op=) with the name on its left changes the variable it names.

### L3: Relational / relations x function (concrete operational begins)

L3 for identifier: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

identifier -&gt; L3 (Relational): the answer relates the parts (3 ways).

- **relation to neighbour** (composition rule (with a neighbour)): Each variable is named by one identifier, which must be unique within its scope: declaring a second local with the same name in that scope is a compile error.
- **relation to neighbour** (composition rule (with a neighbour)): A declaration binds the identifier to a type. Every later use must repeat exactly that spelling, or the compiler cannot resolve it.
- **purpose of the whole** (plan / role rule): Identifiers let code refer to values and code by name. Descriptive names make each variable's role readable to people, though names have no effect on what the program computes.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for identifier: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

identifier -&gt; L4 (Extended abstract): the answer reasons beyond the given code (6 ways).

- **predict a change** (conservation rule; shows `IdentifierCaseInsensitive`): Renaming an identifier consistently at its declaration and every use leaves behavior unchanged. Renaming only some occurrences, or changing only the capitalization, breaks compilation with 'cannot find symbol'.
- **diagnose an error** (error rule): rule broken: Identifiers are case-sensitive and must match a declaration exactly; a name that matches nothing in scope cannot be resolved. Kind: compile-time. Trigger class: Any use whose spelling or capitalization differs from the declaration or library name (Sytem, prinln, Println, studentTotl): compiler reports 'cannot find symbol'.
- **transfer to a new program** (applicability rule): Every variable, method and class needs an identifier. Pick descriptive lowerCamelCase names, and use single letters only for short-lived loop indices or standard maths symbols. A name never stands in for a value; only literals and expressions do that.
- **diagnose an error** (error rule): rule broken: Every variable must be declared (with a type) before use and referred to by exactly the declared name, inside its scope. Kind: compile-time. Trigger class: Use of a name that was never declared, was declared under another name, or is used outside the block where it was declared: 'cannot find symbol' (one missing declaration can produce several errors).
- **diagnose an error** (error rule): rule broken: Reserved words cannot be used as identifiers. Kind: compile-time. Trigger class: Naming a variable new, class, int, public and so on: '&lt;identifier&gt; expected' or 'not a statement'.
- **diagnose an error** (error rule): rule broken: An identifier may not start with a digit or contain spaces or operator symbols. Kind: compile-time. Trigger class: Names like 2ndValue, max value or max-value: syntax errors, or max - value parsed as a subtraction.

## Same topic

`identifier` belongs to the topic **Data types and terminology (literals, identifiers, variables, declarations, assignment, expressions)** (`topic1.2.a`). The topic also contains: `assignment`, `chained_assignment`, `data_type`, `declaration`, `definite_assignment`, `expression`, `literal`, `named_constants`, `naming_convention`, `operator_precedence`, `primitive_type`, `program_trace`, `variable`, `variable_swap`.

## Rules of the concept (18)

- **folk-meaning rule:** In English, Total, total and TOTAL are the same word, and names may contain spaces or hyphens (max-value). Java identifiers are case-sensitive and may use only letters, digits, \_ and $, so total and Total are different names and max-value is a subtraction.
- **wrong rule / right rule:** IdentifierCaseInsensitive: wrong: System.out.Println and System.out.println name the same method. \| right: Java is case-sensitive: names of variables, methods and classes that differ only in capitalization are different names.
- **wrong rule / right rule:** NoReservedWords: wrong: keywords may be reused as identifiers \| right: Keywords are reserved by Java and cannot be used as variable names.
- **uneven-application rule:** Points to LT (a name refers to the declaration with exactly that spelling in scope). Applied unevenly, a student treats Count and count as one variable in one statement but as two in another.
- **identity rule:** Identifier: a name for a variable, method or class, made of letters, digits, \_ and $ and not starting with a digit.
- **declarative rule:** An identifier is a sequence of letters, digits, \_ and $ whose first character is not a digit. Identifiers are case-sensitive, and reserved words such as int, public or class cannot be used.
- **operational sequencing rule:** When an identifier appears, the compiler looks it up by exact spelling among the declarations in scope (an error if none matches). At run time a variable's name is replaced by that variable's current value.
- **evaluation / result rule:** An identifier used as an expression yields the current value of the variable it names, with that variable's declared type. abc, Ab$, abc123 and a\_b are legal names; Ab\*, 1abc and a+b are not.
- **state-transition rule:** A name does nothing at run time. Only an assignment (or ++ or op=) with the name on its left changes the variable it names.
- **composition rule (with a neighbour):** with variable: Each variable is named by one identifier, which must be unique within its scope: declaring a second local with the same name in that scope is a compile error.
- **composition rule (with a neighbour):** with declaration: A declaration binds the identifier to a type. Every later use must repeat exactly that spelling, or the compiler cannot resolve it.
- **plan / role rule:** Identifiers let code refer to values and code by name. Descriptive names make each variable's role readable to people, though names have no effect on what the program computes.
- **conservation rule:** Renaming an identifier consistently at its declaration and every use leaves behavior unchanged. Renaming only some occurrences, or changing only the capitalization, breaks compilation with 'cannot find symbol'.
- **error rule:** rule broken: Identifiers are case-sensitive and must match a declaration exactly; a name that matches nothing in scope cannot be resolved. (compile-time)
- **error rule:** rule broken: Every variable must be declared (with a type) before use and referred to by exactly the declared name, inside its scope. (compile-time)
- **error rule:** rule broken: Reserved words cannot be used as identifiers. (compile-time)
- **error rule:** rule broken: An identifier may not start with a digit or contain spaces or operator symbols. (compile-time)
- **applicability rule:** Every variable, method and class needs an identifier. Pick descriptive lowerCamelCase names, and use single letters only for short-lived loop indices or standard maths symbols. A name never stands in for a value; only literals and expressions do that.

## The whole prerequisite chain

- **Everything it builds on (0):** nothing
- **Everything that builds on it (80):** `accumulator_pattern`, `animation`, `api`, `array_copy`, `array_exchange`, `array_reversal`, `array_traversal`, `assignment`, `boolean_expression`, `boolean_flag_array`, `break_statement`, `chained_assignment`, `comparison_operators`, `compound_assignment`, `conditional_operator`, `continue_statement`, `convergence_rate`, `convergence_test`, `coordinate_scaling`, `counter_pattern`, `dangling_else`, `debugging`, `declaration`, `definite_assignment`, `do_while_loop`, `drawing_shapes`, `else_if_chain`, `enhanced_for`, `expression`, `fencepost_loop`, `flag_search_loop`, `for_loop`, `frequency_counting`, `function_plotting`, `if_else_statement`, `if_statement`, `increment_operators`, `infinite_loop`, `labeled_break`, `loop_body`, `loop_control`, `loop_invariant_reasoning`, `loop_performance`, `loop_scope`, `loop_variable`, `math_library`, `math_random`, `math_round`, `matrix_operations`, `method_call`, `monte_carlo_simulation`, `mouse_interaction`, `named_constants`, `naming_convention`, `nested_conditionals`, `nested_loops`, `number_conversion`, `off_by_one_error`, `operator_precedence`, `power_method`, `program_state`, `program_trace`, `random_move`, `row_major_order`, `running_extreme`, `sampling_without_replacement`, `sentinel_loop`, `shuffle`, `side_effect_order`, `simulation_loop`, `standard_audio`, `standard_drawing`, `switch_statement`, `syntax_template`, `testing`, `trig_functions`, `two_models`, `variable`, `variable_swap`, `while_loop`
