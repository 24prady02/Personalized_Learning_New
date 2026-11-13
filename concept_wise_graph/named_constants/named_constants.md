# named_constants (`named_constants`)

final constants in UPPER\_CASE instead of magic numbers

Section 1.2 Built-in Types of Data, topic 1.2.a Data types and terminology (literals, identifiers, variables, declarations, assignment, expressions). From the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`).

![The knowledge graph around named_constants](named_constants.png)

## Concepts associated with named\_constants (15)

| Concept | Description | How it is associated |
| --- | --- | --- |
| **assignment** | = stores the computed value of the right side | shares error AssignToFinal<br>same topic (topic1.2.a) |
| **chained\_assignment** | a = b = 0 assigns right to left | same topic (topic1.2.a) |
| **compile\_time\_error** | an error javac reports before the program can run (syntax, types) | shares error AssignToFinal |
| **data\_type** | a set of values and the operations defined on them | same topic (topic1.2.a) |
| **declaration** | int x; -- introduces a variable name and its type | prerequisite of it (it needs this)<br>composition rule (R) with it<br>same topic (topic1.2.a) |
| **definite\_assignment** | a local variable must be assigned before it is read | same topic (topic1.2.a) |
| **expression** | anything that evaluates to a value | same topic (topic1.2.a) |
| **identifier** | a name for a variable, method or class; case-sensitive, no spaces, not a keyword | same topic (topic1.2.a) |
| **literal** | a constant value written in code (42, 3.14, true, 'a', "hi") | same topic (topic1.2.a) |
| **naming\_convention** | choosing meaningful names: full words, lowerCamelCase, single letters only for throwaway loop counters | prerequisite of it (it needs this)<br>composition rule (R) with it<br>shares misconception MagicNumbers<br>same topic (topic1.2.a) |
| **operator\_precedence** | the order operators bind in an expression | same topic (topic1.2.a) |
| **primitive\_type** | int, double, boolean, char | same topic (topic1.2.a) |
| **program\_trace** | a table of the values of the variables after each statement, used to check what code does | same topic (topic1.2.a) |
| **variable** | a named, typed box that holds a value | same topic (topic1.2.a) |
| **variable\_swap** | exchanging two variables needs a temporary | same topic (topic1.2.a) |

## Every edge in this view and its full label (27)

| From | Edge | To | Full edge label |
| --- | --- | --- | --- |
| **declaration** | prerequisite | **named\_constants** | A constant is a declaration marked final.<br>grounding: book\_passage<br>composition rule (R) of declaration with named\_constants: Adding final to a declaration makes the variable a constant that can be assigned only once.<br>composition rule (R) of named\_constants with declaration: A constant is an ordinary declaration with the final modifier, with the same type and scope rules. |
| **naming\_convention** | prerequisite | **named\_constants** | Constants have their own naming convention.<br>grounding: book\_passage<br>composition rule (R) of naming\_convention with named\_constants: Constants are written in ALL\_CAPS with underscores, which sets them apart from lowerCamelCase variables and signals that they never change.<br>composition rule (R) of named\_constants with naming\_convention: Constants follow their own convention, ALL\_CAPS\_WITH\_UNDERSCORES, which sets them apart from lowerCamelCase variables. |
| **named\_constants** | misconception | **MagicNumbers** | **wrong rule:** Writing 7 or 0.0825 directly in formulas is as clear as using a named constant.<br>**right rule:** Give fixed values a final, UPPER\_CASE name and use the name.<br>role: primary |
| **naming\_convention** | misconception | **MagicNumbers** | **wrong rule:** Writing 7 or 0.0825 directly in formulas is as clear as using a named constant.<br>**right rule:** Give fixed values a final, UPPER\_CASE name and use the name.<br>role: context |
| **assignment** | error | **AssignToFinal** | **wrong rule:** Assigns a new value to a variable declared final.<br>**right rule:** A final variable cannot be reassigned after it is initialized; the compiler reports an error.<br>role: context |
| **compile\_time\_error** | error | **AssignToFinal** | **wrong rule:** Assigns a new value to a variable declared final.<br>**right rule:** A final variable cannot be reassigned after it is initialized; the compiler reports an error.<br>role: context |
| **named\_constants** | error | **AssignToFinal** | **wrong rule:** Assigns a new value to a variable declared final.<br>**right rule:** A final variable cannot be reassigned after it is initialized; the compiler reports an error.<br>role: primary |
| **named\_constants** | has\_level | **named\_constants@L0** | named constants -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (1 way).<br>**[0] everyday\_reading** (E): In everyday speech a 'constant' is just a number that stays the same in the problem, and a capitalized name looks official. In Java a value is constant only if its variable is declared final, which the compiler enforces; naming it in UPPER\_CASE alone protects nothing. |
| **named\_constants** | has\_level | **named\_constants@L1** | named constants -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).<br>**[0] names\_the\_element** (N): Named constant: a variable declared final (by convention named in UPPER\_CASE) that names a fixed value.<br>**[1] states\_the\_rule** (S): final type NAME = value; cannot be reassigned after initialization (the compiler reports an error). Constant names are all uppercase with \_ between words. |
| **named\_constants** | has\_level | **named\_constants@L2** | named constants -&gt; L2 (Multistructural): the answer applies the rules of named constants to every part of the code, in order (3 ways).<br>**[0] line\_by\_line\_trace** (LT): A constant is initialized once, when its declaration executes. Every later use reads that same value.<br>**[1] output\_prediction** (OP): A use of CM\_PER\_INCH evaluates to 2.54 with type double, exactly as the literal would.<br>**[2] one\_step\_execution** (OS): Only the initialization changes state; no later statement can change the constant. |
| **named\_constants** | has\_level | **named\_constants@L3** | named constants -&gt; L3 (Relational): the answer relates the parts (3 ways).<br>**[0] relation\_to\_neighbour** (R): A constant is an ordinary declaration with the final modifier, with the same type and scope rules.<br>**[1] relation\_to\_neighbour** (R): Constants follow their own convention, ALL\_CAPS\_WITH\_UNDERSCORES, which sets them apart from lowerCamelCase variables.<br>**[2] purpose\_of\_the\_whole** (P): Plan: replace magic numbers with a meaningful name (Sajaniemi role: fixed value), so the code is readable, the value is changed in one place, and accidental reassignment is prevented. |
| **named\_constants** | has\_level | **named\_constants@L4** | named constants -&gt; L4 (Extended abstract): the answer reasons beyond the given code (4 ways).<br>**[0] predict\_a\_change** (C): Changing the constant's value in its declaration changes every use consistently. Removing final keeps behavior but loses the protection. Adding any later assignment to it breaks compilation.<br>**[1] diagnose\_an\_error** (D): rule broken: A final variable is assigned exactly once; it cannot be reassigned after initialization. Kind: compile-time. Trigger class: Any assignment, ++ or op= to a final variable after its initialization: 'cannot assign a value to final variable'.<br>**[2] transfer\_to\_a\_new\_program** (X): Use a named constant for a value fixed for the whole run that appears in formulas (conversion factors, physical constants, sizes, rates). Use a variable for values that are read or computed, and plain literals for self-evident values such as 0 or 1.<br>**[3] diagnose\_an\_error** (D): rule broken: A final variable must be assigned before it is read. Kind: compile-time. Trigger class: Declaring final double RATE; and reading it on a path that never assigns it: 'variable RATE might not have been initialized'. |
| **topic1.2.a** | contains | **assignment** | topic topic1.2.a contains assignment |
| **topic1.2.a** | contains | **chained\_assignment** | topic topic1.2.a contains chained\_assignment |
| **topic1.2.a** | contains | **data\_type** | topic topic1.2.a contains data\_type |
| **topic1.2.a** | contains | **declaration** | topic topic1.2.a contains declaration |
| **topic1.2.a** | contains | **definite\_assignment** | topic topic1.2.a contains definite\_assignment |
| **topic1.2.a** | contains | **expression** | topic topic1.2.a contains expression |
| **topic1.2.a** | contains | **identifier** | topic topic1.2.a contains identifier |
| **topic1.2.a** | contains | **literal** | topic topic1.2.a contains literal |
| **topic1.2.a** | contains | **named\_constants** | topic topic1.2.a contains named\_constants |
| **topic1.2.a** | contains | **naming\_convention** | topic topic1.2.a contains naming\_convention |
| **topic1.2.a** | contains | **operator\_precedence** | topic topic1.2.a contains operator\_precedence |
| **topic1.2.a** | contains | **primitive\_type** | topic topic1.2.a contains primitive\_type |
| **topic1.2.a** | contains | **program\_trace** | topic topic1.2.a contains program\_trace |
| **topic1.2.a** | contains | **variable** | topic topic1.2.a contains variable |
| **topic1.2.a** | contains | **variable\_swap** | topic topic1.2.a contains variable\_swap |
