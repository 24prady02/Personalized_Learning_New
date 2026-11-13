# exclusive_or (`exclusive_or`)

^ on booleans is true when the operands differ

Section 1.2 Built-in Types of Data, topic 1.2.e Booleans. From the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`).

![The knowledge graph around exclusive_or](exclusive_or.png)

## Concepts associated with exclusive\_or (6)

| Concept | Description | How it is associated |
| --- | --- | --- |
| **arithmetic\_operators** | + - \* / % | shares misconception CaretIsPower |
| **boolean** | true/false primitive | same topic (topic1.2.e) |
| **boolean\_expression** | an expression that evaluates to true/false | same topic (topic1.2.e) |
| **de\_morgan** | !(a &amp;&amp; b) == !a \|\| !b and !(a \|\| b) == !a &amp;&amp; !b | same topic (topic1.2.e) |
| **logical\_operators** | &amp;&amp; \|\| ! | prerequisite of it (it needs this)<br>composition rule (R) with it<br>same topic (topic1.2.e) |
| **short\_circuit** | &amp;&amp;/\|\| stop evaluating once the result is known | same topic (topic1.2.e) |

## Every edge in this view and its full label (14)

| From | Edge | To | Full edge label |
| --- | --- | --- | --- |
| **logical\_operators** | prerequisite | **exclusive\_or** | ^ on booleans is another logical operator, defined by a truth table like &amp;&amp;, \|\| and !: true exactly when its operands differ.<br>grounding: order\_only<br>composition rule (R) of logical\_operators with exclusive\_or: ^ on booleans is a further logical operator, true exactly when the operands differ (it equals (a \|\| b) &amp;&amp; !(a &amp;&amp; b)), but unlike &amp;&amp; and \|\| it always evaluates both operands.<br>composition rule (R) of exclusive\_or with logical\_operators: ^ belongs with &amp;&amp;, \|\| and ! as a boolean operator defined by a truth table, but it is not short-circuit and it binds tighter than &amp;&amp; and \|\|; a ^ b equals (a \|\| b) &amp;&amp; !(a &amp;&amp; b). |
| **arithmetic\_operators** | misconception | **CaretIsPower** | **wrong rule:** a^2 computes a squared.<br>**right rule:** Java has no exponent operator; ^ is exclusive or, and a \* a or Math.pow(a, 2) computes a squared.<br>role: primary |
| **exclusive\_or** | misconception | **CaretIsPower** | **wrong rule:** a^2 computes a squared.<br>**right rule:** Java has no exponent operator; ^ is exclusive or, and a \* a or Math.pow(a, 2) computes a squared.<br>role: context |
| **exclusive\_or** | has\_level | **exclusive\_or@L0** | exclusive or -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (3 ways).<br>**[0] everyday\_reading** (E): Folk meaning: on calculators, in spreadsheets and in typed maths ^ means 'to the power of', so a^2 is a squared. Java rule: ^ is exclusive or (bitwise on ints), there is no exponent operator, and 10^6 is 12.<br>**[1] misconception** (M) &rarr; CaretIsPower: wrong rule: a^2 computes a squared. Right rule: Java has no exponent operator; ^ is exclusive or, and a \* a or Math.pow(a, 2) computes a squared.<br>**[2] inconsistent\_trace** (T) &rarr; CaretIsPower: Points to LT (both operands are evaluated, then compared: true if they differ). Applied unevenly: in the true/true row of a truth table the student gives true (treating ^ like \|\|) while the other rows are right. (here mixing in: "a^2 computes a squared") |
| **exclusive\_or** | has\_level | **exclusive\_or@L1** | exclusive or -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).<br>**[0] names\_the\_element** (N): ^ applied to boolean operands is the exclusive-or logical operator.<br>**[1] states\_the\_rule** (S): For booleans, a ^ b is true if a and b are different and false if they are the same (equivalent to a != b); both operands are always evaluated. |
| **exclusive\_or** | has\_level | **exclusive\_or@L2** | exclusive or -&gt; L2 (Multistructural): the answer applies the rules of exclusive or to every part of the code, in order (3 ways).<br>**[0] line\_by\_line\_trace** (LT): Evaluate the left operand, then the right operand (always, no short-circuit), then compare them.<br>**[1] output\_prediction** (OP): Boolean result: true ^ true is false, true ^ false is true, false ^ false is false; with int operands ^ gives an int bitwise result, so 10 ^ 6 is 12.<br>**[2] one\_step\_execution** (OS): ^ changes no variable; flag = flag ^ true stores the opposite value, toggling the flag. |
| **exclusive\_or** | has\_level | **exclusive\_or@L3** | exclusive or -&gt; L3 (Relational): the answer relates the parts (2 ways).<br>**[0] relation\_to\_neighbour** (R): ^ belongs with &amp;&amp;, \|\| and ! as a boolean operator defined by a truth table, but it is not short-circuit and it binds tighter than &amp;&amp; and \|\|; a ^ b equals (a \|\| b) &amp;&amp; !(a &amp;&amp; b).<br>**[1] purpose\_of\_the\_whole** (P): Expresses 'exactly one of two conditions' (e.g. exactly one of two coordinates is negative) or toggles a parity flag. |
| **exclusive\_or** | has\_level | **exclusive\_or@L4** | exclusive or -&gt; L4 (Extended abstract): the answer reasons beyond the given code (3 ways).<br>**[0] predict\_a\_change** (C) &rarr; CaretIsPower: Swapping the operands keeps the value (^ is commutative), and applying ^ b twice restores the original value ((a ^ b) ^ b == a), so xor with a fixed operand is reversible.<br>**[1] transfer\_to\_a\_new\_program** (X): Use ^ (or the clearer a != b) when the test is 'the two conditions differ'; never use ^ for powers (use multiplication, Math.pow, or e-notation literals such as 1e6).<br>**[2] diagnose\_an\_error** (D): rule broken: ^ is exclusive or, not exponentiation. Kind: silent logic error. Trigger class: Writing x^2 or 10^n with int operands: it compiles and computes a bitwise xor (10^6 is 12); with double operands such as 2.0^2 it is a compile-time error instead. |
| **topic1.2.e** | contains | **boolean** | topic topic1.2.e contains boolean |
| **topic1.2.e** | contains | **boolean\_expression** | topic topic1.2.e contains boolean\_expression |
| **topic1.2.e** | contains | **de\_morgan** | topic topic1.2.e contains de\_morgan |
| **topic1.2.e** | contains | **exclusive\_or** | topic topic1.2.e contains exclusive\_or |
| **topic1.2.e** | contains | **logical\_operators** | topic topic1.2.e contains logical\_operators |
| **topic1.2.e** | contains | **short\_circuit** | topic topic1.2.e contains short\_circuit |
