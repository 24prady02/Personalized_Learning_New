# definite_assignment (`definite_assignment`)

a local variable must be assigned before it is read

Section 1.2 Built-in Types of Data, topic 1.2.a Data types and terminology (literals, identifiers, variables, declarations, assignment, expressions). From the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`).

![The knowledge graph around definite_assignment](definite_assignment.png)

## Concepts associated with definite\_assignment (15)

| Concept | Description | How it is associated |
| --- | --- | --- |
| **array\_default\_values** | new slots start at 0 / false / null | parallel concept |
| **assignment** | = stores the computed value of the right side | same topic (topic1.2.a) |
| **chained\_assignment** | a = b = 0 assigns right to left | same topic (topic1.2.a) |
| **data\_type** | a set of values and the operations defined on them | same topic (topic1.2.a) |
| **declaration** | int x; -- introduces a variable name and its type | prerequisite of it (it needs this)<br>composition rule (R) with it<br>shares misconception LocalVariablesAutoInitialized<br>same topic (topic1.2.a) |
| **expression** | anything that evaluates to a value | same topic (topic1.2.a) |
| **identifier** | a name for a variable, method or class; case-sensitive, no spaces, not a keyword | same topic (topic1.2.a) |
| **literal** | a constant value written in code (42, 3.14, true, 'a', "hi") | same topic (topic1.2.a) |
| **named\_constants** | final constants in UPPER\_CASE instead of magic numbers | same topic (topic1.2.a) |
| **naming\_convention** | choosing meaningful names: full words, lowerCamelCase, single letters only for throwaway loop counters | same topic (topic1.2.a) |
| **operator\_precedence** | the order operators bind in an expression | same topic (topic1.2.a) |
| **primitive\_type** | int, double, boolean, char | same topic (topic1.2.a) |
| **program\_trace** | a table of the values of the variables after each statement, used to check what code does | same topic (topic1.2.a) |
| **variable** | a named, typed box that holds a value | shares misconception LocalVariablesAutoInitialized<br>same topic (topic1.2.a) |
| **variable\_swap** | exchanging two variables needs a temporary | same topic (topic1.2.a) |

## Every edge in this view and its full label (25)

| From | Edge | To | Full edge label |
| --- | --- | --- | --- |
| **declaration** | prerequisite | **definite\_assignment** | A declared local variable has no defined value until it is assigned, and the compiler rejects any read before that assignment.<br>grounding: book\_passage<br>composition rule (R) of declaration with definite\_assignment: A declaration without an initializer leaves a local unassigned, and any read before an assignment on every path is a compile error.<br>composition rule (R) of definite\_assignment with declaration: A declaration without an initializer leaves the local unassigned. Writing = value in the declaration satisfies the rule at once. |
| **definite\_assignment** | parallel | **array\_default\_values** | A local variable has no value until it is assigned: using it first is a compile-time error. An array element is given a default value (0, 0.0, false) when the array is created with new, so it can be read before any assignment.<br>grounding: book\_passage |
| **declaration** | misconception | **LocalVariablesAutoInitialized** | **wrong rule:** local variables get a default value on their own<br>**right rule:** A local variable has no value until it is assigned, and using it before then does not compile.<br>role: context |
| **definite\_assignment** | misconception | **LocalVariablesAutoInitialized** | **wrong rule:** local variables get a default value on their own<br>**right rule:** A local variable has no value until it is assigned, and using it before then does not compile.<br>role: primary |
| **variable** | misconception | **LocalVariablesAutoInitialized** | **wrong rule:** int x; inside main starts at 0, so x can be used before anything is assigned to it.<br>**right rule:** A local variable has no value until it is assigned, and using it before then does not compile.<br>role: context |
| **definite\_assignment** | has\_level | **definite\_assignment@L0** | definite assignment -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (3 ways).<br>**[0] everyday\_reading** (E): Everyday intuition, and some older languages, treat a new or empty quantity as zero ("nothing yet means 0"). A Java local variable has no value at all until it is assigned, and the compiler rejects any read before that.<br>**[1] misconception** (M) &rarr; LocalVariablesAutoInitialized: wrong rule: local variables get a default value on their own. Right rule: A local variable has no value until it is assigned, and using it before then does not compile.<br>**[2] inconsistent\_trace** (T) &rarr; LocalVariablesAutoInitialized: Points to LT (along every control-flow path, an assignment must come before each read). Applied unevenly, a student checks straight-line code but assumes a variable assigned in only one branch of an if, or inside a loop, is assigned afterwards. (here mixing in: "local variables get a default value on their own") |
| **definite\_assignment** | has\_level | **definite\_assignment@L1** | definite assignment -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).<br>**[0] names\_the\_element** (N): Definite assignment: the compile-time rule that a local variable must certainly have been assigned before any read of it.<br>**[1] states\_the\_rule** (S): Every access of a local variable must be preceded by an assignment on every possible path, or the program does not compile. The analysis ignores run-time values, except for constant booleans and the operators &amp;&amp; \|\| ?:. |
| **definite\_assignment** | has\_level | **definite\_assignment@L2** | definite assignment -&gt; L2 (Multistructural): the answer applies the rules of definite assignment to every part of the code, in order (3 ways).<br>**[0] line\_by\_line\_trace** (LT): The compiler walks the control flow. After a declaration with no initializer the variable is unassigned, and an assignment makes it assigned on that path. Where paths merge (after if/else) it counts as assigned only if every incoming path assigned it, and an assignment inside a while body does not count after the loop.<br>**[1] output\_prediction** (OP): The result appears at compile time: the code either compiles or reports 'variable x might not have been initialized'. No default value is ever produced for a local variable.<br>**[2] one\_step\_execution** (OS): The first assignment (initialization) moves a variable from unassigned to holding a value, and only then may it be read. |
| **definite\_assignment** | has\_level | **definite\_assignment@L3** | definite assignment -&gt; L3 (Relational): the answer relates the parts (3 ways).<br>**[0] relation\_to\_neighbour** (R): A declaration without an initializer leaves the local unassigned. Writing = value in the declaration satisfies the rule at once.<br>**[1] relation\_to\_neighbour** (R): A local variable has no value until it is assigned: using it first is a compile-time error. An array element is given a default value (0, 0.0, false) when the array is created with new, so it can be read before any assignment.<br>**[2] purpose\_of\_the\_whole** (P): The rule guarantees that no program reads a meaningless value. The matching plan is to initialize counters and accumulators before the loop that updates them (int sum = 0; then sum += i inside the loop). |
| **definite\_assignment** | has\_level | **definite\_assignment@L4** | definite assignment -&gt; L4 (Extended abstract): the answer reasons beyond the given code (4 ways).<br>**[0] predict\_a\_change** (C) &rarr; LocalVariablesAutoInitialized: Moving an initialization into one branch of an if, or into a loop body, breaks compilation of the reads that follow. Adding an else branch that also assigns, or initializing at the declaration, restores it.<br>**[1] transfer\_to\_a\_new\_program** (X): Initialize at the declaration whenever a sensible first value exists (0 for counters and sums). Leave the declaration bare only when every branch that follows assigns it. The rule covers local variables only: array elements and fields get default values.<br>**[2] diagnose\_an\_error** (D): rule broken: A local variable must be definitely assigned before it is read. Kind: compile-time. Trigger class: A read reachable on a path with no assignment: declared without initializer, or assigned only inside an if without else, a loop body, or a switch case: 'variable might not have been initialized'.<br>**[3] diagnose\_an\_error** (D): rule broken: A blank final variable must be assigned at most once. Kind: compile-time. Trigger class: Assigning a final local on two paths that can both run, or again inside a loop: 'variable might already have been assigned'. |
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
