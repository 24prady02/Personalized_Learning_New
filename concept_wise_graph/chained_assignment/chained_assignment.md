# chained_assignment (`chained_assignment`)

a = b = 0 assigns right to left

Section 1.2 Built-in Types of Data, topic 1.2.a Data types and terminology (literals, identifiers, variables, declarations, assignment, expressions). From the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`).

![The knowledge graph around chained_assignment](chained_assignment.png)

## Concepts associated with chained\_assignment (15)

| Concept | Description | How it is associated |
| --- | --- | --- |
| **assignment** | = stores the computed value of the right side | prerequisite of it (it needs this)<br>composition rule (R) with it<br>shares misconception AssignmentNotExpression<br>same topic (topic1.2.a) |
| **data\_type** | a set of values and the operations defined on them | same topic (topic1.2.a) |
| **declaration** | int x; -- introduces a variable name and its type | same topic (topic1.2.a) |
| **definite\_assignment** | a local variable must be assigned before it is read | same topic (topic1.2.a) |
| **expression** | anything that evaluates to a value | shares misconception AssignmentNotExpression<br>same topic (topic1.2.a) |
| **identifier** | a name for a variable, method or class; case-sensitive, no spaces, not a keyword | same topic (topic1.2.a) |
| **literal** | a constant value written in code (42, 3.14, true, 'a', "hi") | same topic (topic1.2.a) |
| **named\_constants** | final constants in UPPER\_CASE instead of magic numbers | same topic (topic1.2.a) |
| **naming\_convention** | choosing meaningful names: full words, lowerCamelCase, single letters only for throwaway loop counters | same topic (topic1.2.a) |
| **operator\_precedence** | the order operators bind in an expression | same topic (topic1.2.a) |
| **primitive\_type** | int, double, boolean, char | same topic (topic1.2.a) |
| **program\_trace** | a table of the values of the variables after each statement, used to check what code does | same topic (topic1.2.a) |
| **read\_loop\_idiom** | reading until end-of-input | shares misconception AssignmentNotExpression |
| **variable** | a named, typed box that holds a value | same topic (topic1.2.a) |
| **variable\_swap** | exchanging two variables needs a temporary | same topic (topic1.2.a) |

## Every edge in this view and its full label (25)

| From | Edge | To | Full edge label |
| --- | --- | --- | --- |
| **assignment** | prerequisite | **chained\_assignment** | An assignment such as x = y is treated as an expression: it assigns the value of y to x and evaluates to that value.<br>grounding: questionable<br>composition rule (R) of assignment with chained\_assignment: Because an assignment is an expression whose value is the value stored, and = groups right to left, a = b = 0 first stores 0 in b and then stores that 0 in a.<br>composition rule (R) of chained\_assignment with assignment: A chain works only because an assignment is itself an expression whose value is the value stored, so it can be the right side of another =. |
| **assignment** | misconception | **AssignmentNotExpression** | **wrong rule:** An assignment cannot be used inside a larger expression, so a condition like (x = read()) != v is not allowed.<br>**right rule:** An assignment is an expression whose value is the value assigned, so (x = v) both stores v in x and gives v.<br>role: primary |
| **chained\_assignment** | misconception | **AssignmentNotExpression** | **wrong rule:** an assignment cannot be used inside a larger expression<br>**right rule:** An assignment is an expression whose value is the value assigned, so (x = v) both stores v in x and gives v.<br>role: context |
| **expression** | misconception | **AssignmentNotExpression** | **wrong rule:** An assignment cannot be used inside a larger expression, so a condition like (x = read()) != v is not allowed.<br>**right rule:** An assignment is an expression whose value is the value assigned, so (x = v) both stores v in x and gives v.<br>role: context |
| **read\_loop\_idiom** | misconception | **AssignmentNotExpression** | **wrong rule:** A read and a test cannot be combined, so while ((x = read()) != end) is not allowed.<br>**right rule:** while ((x = read()) != end) reads a value into x and tests that same value in one expression.<br>role: context |
| **chained\_assignment** | has\_level | **chained\_assignment@L0** | chained assignment -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (3 ways).<br>**[0] everyday\_reading** (E): In maths, a = b = 0 states that all three quantities are equal at once, in any reading order. In Java the = operators group right to left: b = 0 runs first, and its value 0 is then assigned to a.<br>**[1] misconception** (M) &rarr; AssignmentNotExpression: wrong rule: an assignment cannot be used inside a larger expression. Right rule: An assignment is an expression whose value is the value assigned, so (x = v) both stores v in x and gives v.<br>**[2] inconsistent\_trace** (T) &rarr; AssignmentNotExpression: Points to LT (the rightmost assignment runs first, and its value feeds the next one to its left). Applied unevenly, a student evaluates a = b first and gives a the old value of b. (here mixing in: "an assignment cannot be used inside a larger expression") |
| **chained\_assignment** | has\_level | **chained\_assignment@L1** | chained assignment -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).<br>**[0] names\_the\_element** (N): Chained assignment: several = in one expression (a = b = c = 0) that assigns one value to several variables.<br>**[1] states\_the\_rule** (S): = is right-associative, and an assignment expression has the value that was stored, so a = b = 0 means a = (b = 0). Every target must be a variable whose type accepts the value. |
| **chained\_assignment** | has\_level | **chained\_assignment@L2** | chained assignment -&gt; L2 (Multistructural): the answer applies the rules of chained assignment to every part of the code, in order (3 ways).<br>**[0] line\_by\_line\_trace** (LT): The innermost (rightmost) assignment runs first: evaluate 0, store it in b, and that assignment's value 0 is then stored in a.<br>**[1] output\_prediction** (OP): The whole expression's value is the value assigned. With int i and double d, d = i = 5 stores 5 in i and 5.0 in d.<br>**[2] one\_step\_execution** (OS): Every variable in the chain changes, right to left, to the same value (converted to its own type). |
| **chained\_assignment** | has\_level | **chained\_assignment@L3** | chained assignment -&gt; L3 (Relational): the answer relates the parts (2 ways).<br>**[0] relation\_to\_neighbour** (R): A chain works only because an assignment is itself an expression whose value is the value stored, so it can be the right side of another =.<br>**[1] purpose\_of\_the\_whole** (P): Initializing several counters or accumulators to the same starting value in one line (sum = count = 0). |
| **chained\_assignment** | has\_level | **chained\_assignment@L4** | chained assignment -&gt; L4 (Extended abstract): the answer reasons beyond the given code (4 ways).<br>**[0] predict\_a\_change** (C) &rarr; AssignmentNotExpression: Reordering targets with different types can break the chain: d = i = 5 compiles, but i = d = 5 does not, because the double value of d = 5 cannot go into int i.<br>**[1] transfer\_to\_a\_new\_program** (X): Use a chain only to give several variables of the same type one simple starting value. Avoid chains inside conditions or with expressions that have side effects.<br>**[2] diagnose\_an\_error** (D): rule broken: Every value in the chain must be assignable to the next target's type. Kind: compile-time. Trigger class: A chain passing through a wider type into a narrower one (int i; double d; i = d = 2.5;): 'possible lossy conversion'.<br>**[3] diagnose\_an\_error** (D): rule broken: int a = b = 0; declares only a; b must already exist. Kind: compile-time. Trigger class: Using the chain in a declaration with an undeclared inner variable: 'cannot find symbol b'. |
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
