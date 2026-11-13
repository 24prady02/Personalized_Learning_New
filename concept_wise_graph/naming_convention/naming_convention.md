# naming_convention (`naming_convention`)

choosing meaningful names: full words, lowerCamelCase, single letters only for throwaway loop counters

Section 1.2 Built-in Types of Data, topic 1.2.a Data types and terminology (literals, identifiers, variables, declarations, assignment, expressions). From the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`).

![The knowledge graph around naming_convention](naming_convention.png)

## Concepts associated with naming\_convention (14)

| Concept | Description | How it is associated |
| --- | --- | --- |
| **assignment** | = stores the computed value of the right side | same topic (topic1.2.a) |
| **chained\_assignment** | a = b = 0 assigns right to left | same topic (topic1.2.a) |
| **data\_type** | a set of values and the operations defined on them | same topic (topic1.2.a) |
| **declaration** | int x; -- introduces a variable name and its type | same topic (topic1.2.a) |
| **definite\_assignment** | a local variable must be assigned before it is read | same topic (topic1.2.a) |
| **expression** | anything that evaluates to a value | same topic (topic1.2.a) |
| **identifier** | a name for a variable, method or class; case-sensitive, no spaces, not a keyword | same topic (topic1.2.a) |
| **literal** | a constant value written in code (42, 3.14, true, 'a', "hi") | same topic (topic1.2.a) |
| **named\_constants** | final constants in UPPER\_CASE instead of magic numbers | builds on it (needs it)<br>composition rule (R) with it<br>shares misconception MagicNumbers<br>same topic (topic1.2.a) |
| **operator\_precedence** | the order operators bind in an expression | same topic (topic1.2.a) |
| **primitive\_type** | int, double, boolean, char | same topic (topic1.2.a) |
| **program\_trace** | a table of the values of the variables after each statement, used to check what code does | same topic (topic1.2.a) |
| **variable** | a named, typed box that holds a value | prerequisite of it (it needs this)<br>composition rule (R) with it<br>shares misconception NameGivesMeaning<br>same topic (topic1.2.a) |
| **variable\_swap** | exchanging two variables needs a temporary | same topic (topic1.2.a) |

## Every edge in this view and its full label (28)

| From | Edge | To | Full edge label |
| --- | --- | --- | --- |
| **naming\_convention** | prerequisite | **named\_constants** | Constants have their own naming convention.<br>grounding: book\_passage<br>composition rule (R) of naming\_convention with named\_constants: Constants are written in ALL\_CAPS with underscores, which sets them apart from lowerCamelCase variables and signals that they never change.<br>composition rule (R) of named\_constants with naming\_convention: Constants follow their own convention, ALL\_CAPS\_WITH\_UNDERSCORES, which sets them apart from lowerCamelCase variables. |
| **variable** | prerequisite | **naming\_convention** | Each variable gets a name; the convention says the name should describe what the variable holds.<br>grounding: book\_passage<br>composition rule (R) of variable with naming\_convention: A variable's name should describe what it holds (lowerCamelCase), but the name has no effect on its value.<br>composition rule (R) of naming\_convention with variable: Each variable's name should describe what it holds (count, sum, maxSoFar). Single letters suit only short-lived loop indices. |
| **named\_constants** | misconception | **MagicNumbers** | **wrong rule:** Writing 7 or 0.0825 directly in formulas is as clear as using a named constant.<br>**right rule:** Give fixed values a final, UPPER\_CASE name and use the name.<br>role: primary |
| **naming\_convention** | misconception | **CrypticVariableName** | **wrong rule:** Uses abbreviated names such as c or s for a variable whose role is not a temporary loop counter (e.g. c for a count).<br>**right rule:** Use names that indicate what the variables mean.<br>role: primary |
| **naming\_convention** | misconception | **MagicNumbers** | **wrong rule:** Writing 7 or 0.0825 directly in formulas is as clear as using a named constant.<br>**right rule:** Give fixed values a final, UPPER\_CASE name and use the name.<br>role: context |
| **naming\_convention** | misconception | **NameGivesMeaning** | **wrong rule:** Naming a variable max (or average) makes it hold the largest value (or the average) without code that computes it.<br>**right rule:** A name only labels the variable for human readers; only the statements that assign to it decide its value.<br>role: primary |
| **naming\_convention** | misconception | **NameNotCamelCase** | **wrong rule:** Writes variable names as Total, total\_count or TOTALCOUNT.<br>**right rule:** Local variable names are written in lowerCamelCase.<br>role: primary |
| **variable** | misconception | **NameGivesMeaning** | **wrong rule:** Naming a variable max (or average) makes it hold the largest value (or the average) without code that computes it.<br>**right rule:** A name only labels the variable for human readers; only the statements that assign to it decide its value.<br>role: context |
| **naming\_convention** | has\_level | **naming\_convention@L0** | naming convention -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (3 ways).<br>**[0] everyday\_reading** (E): In everyday language a label tells you what a thing is (a jar labelled 'sugar' holds sugar), so novices expect a variable called max to hold the maximum. Java gives names no meaning: conventions exist only for human readers, and only assignments decide values.<br>**[1] misconception** (M) &rarr; NameGivesMeaning: wrong rule: Naming a variable max (or average) makes it hold the largest value (or the average) without code that computes it. Right rule: A name only labels the variable for human readers; only the statements that assign to it decide its value.<br>**[2] inconsistent\_trace** (T) &rarr; NameGivesMeaning: Points to LT (names carry no meaning at run time, so trace by values). Applied unevenly, a student traces values for most variables but assumes that largest is larger than smallest because of its name. (here mixing in: "Naming a variable max (or average) makes it hold the largest value (or the average) without code that computes it") |
| **naming\_convention** | has\_level | **naming\_convention@L1** | naming convention -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).<br>**[0] names\_the\_element** (N): Naming convention: a style rule (not a language rule) for choosing identifiers. Variables and methods use lowerCamelCase, classes UpperCamelCase, constants UPPER\_CASE\_WITH\_UNDERSCORES, and names describe meaning.<br>**[1] states\_the\_rule** (S): Variable names begin with a lowercase letter and capitalize each later word (firstName). Class names begin with a capital. Constants are all uppercase with \_ between words. Names should indicate what the variable means. |
| **naming\_convention** | has\_level | **naming\_convention@L2** | naming convention -&gt; L2 (Multistructural): the answer applies the rules of naming convention to every part of the code, in order (3 ways).<br>**[0] line\_by\_line\_trace** (LT): Conventions have no execution order: the compiler checks only that an identifier is legal and declared, never whether it follows convention.<br>**[1] output\_prediction** (OP): A program's output does not depend on its names: renaming total to t everywhere gives identical results.<br>**[2] one\_step\_execution** (OS): Following or breaking a convention changes no state; it only changes how readable the code is. |
| **naming\_convention** | has\_level | **naming\_convention@L3** | naming convention -&gt; L3 (Relational): the answer relates the parts (3 ways).<br>**[0] relation\_to\_neighbour** (R): Each variable's name should describe what it holds (count, sum, maxSoFar). Single letters suit only short-lived loop indices.<br>**[1] relation\_to\_neighbour** (R): Constants are written in ALL\_CAPS with underscores, which sets them apart from lowerCamelCase variables and signals that they never change.<br>**[2] purpose\_of\_the\_whole** (P): Good names make each variable's role visible (sum for a gatherer, count for a counter, max for a most-wanted holder, i for a stepper), so a reader can recognize the plan without tracing. |
| **naming\_convention** | has\_level | **naming\_convention@L4** | naming convention -&gt; L4 (Extended abstract): the answer reasons beyond the given code (4 ways).<br>**[0] predict\_a\_change** (C) &rarr; NameGivesMeaning: Renaming consistently keeps the program's meaning, because what it computes does not depend on names. A misleading name (max holding a minimum) still compiles and runs the same, but readers draw wrong conclusions.<br>**[1] transfer\_to\_a\_new\_program** (X): Apply the conventions to every name you write. Short names fit only tiny scopes (loop index i, coordinates x and y). No naming convention can replace the code that actually computes the value.<br>**[2] diagnose\_an\_error** (D): rule broken: A name does not compute or guarantee a value. Kind: silent logic error. Trigger class: Trusting a descriptive name instead of the code (e.g. assuming average holds the mean although it was never divided): wrong output that the name hides.<br>**[3] diagnose\_an\_error** (D): rule broken: Names that differ only in case are different identifiers. Kind: silent logic error. Trigger class: Declaring both count and Count (or total and Total) and updating one while printing the other. |
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
