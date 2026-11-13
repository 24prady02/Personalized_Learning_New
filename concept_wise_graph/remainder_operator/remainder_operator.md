# remainder_operator (`remainder_operator`)

% gives the remainder of integer division

Section 1.2 Built-in Types of Data, topic 1.2.c Integers. From the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`).

![The knowledge graph around remainder_operator](remainder_operator.png)

## Concepts associated with remainder\_operator (7)

| Concept | Description | How it is associated |
| --- | --- | --- |
| **arithmetic\_operators** | + - \* / % | prerequisite of it (it needs this)<br>shares misconception RemainderIsSubtraction<br>same topic (topic1.2.c) |
| **int** | 32-bit integer primitive | same topic (topic1.2.c) |
| **int\_literal\_limit** | 2147483648 is legal only as -2147483648 | same topic (topic1.2.c) |
| **integer\_constants** | Integer.MAX\_VALUE, Integer.MIN\_VALUE and their edge cases | same topic (topic1.2.c) |
| **integer\_division** | / on two ints truncates; % is the remainder | prerequisite of it (it needs this)<br>composition rule (R) with it<br>shares misconception NegativeRemainderSign<br>same topic (topic1.2.c) |
| **long\_type** | 64-bit integer type for values beyond the int range | same topic (topic1.2.c) |
| **overflow** | int arithmetic wraps around outside the 32-bit range | same topic (topic1.2.c) |

## Every edge in this view and its full label (20)

| From | Edge | To | Full edge label |
| --- | --- | --- | --- |
| **arithmetic\_operators** | prerequisite | **remainder\_operator** | % is one of the int arithmetic operators; it gives the remainder of the division.<br>grounding: book\_passage |
| **integer\_division** | prerequisite | **remainder\_operator** | % is the companion of integer division: a = (a / b) \* b + a % b.<br>grounding: book\_passage<br>composition rule (R) of integer\_division with remainder\_operator: % gives the remainder of the same truncating division: (a / b) \* b + a % b == a.<br>composition rule (R) of remainder\_operator with integer\_division: % is the companion of integer division, since a == (a / b) \* b + a % b. Both use the same quotient rounded toward 0. |
| **arithmetic\_operators** | misconception | **RemainderIsSubtraction** | **wrong rule:** 9 % 5 means 9 minus 5 (a % b subtracts b from a).<br>**right rule:** % gives the remainder after integer division: 9 % 5 is 4 because 9 = 1 \* 5 + 4, and 17 % 5 is 2, not 12.<br>role: context |
| **integer\_division** | misconception | **NegativeRemainderSign** | **wrong rule:** a % b is never negative, and integer division of a negative number rounds down.<br>**right rule:** a / b rounds toward 0 and a % b takes the sign of a: -14 / 3 is -4 and -14 % 3 is -2.<br>role: context |
| **remainder\_operator** | misconception | **NegativeRemainderSign** | **wrong rule:** a % b is never negative, and integer division of a negative number rounds down.<br>**right rule:** a / b rounds toward 0 and a % b takes the sign of a: -14 / 3 is -4 and -14 % 3 is -2.<br>role: primary |
| **remainder\_operator** | misconception | **RemainderIsQuotient** | **wrong rule:** 17 % 5 is 3 (the quotient).<br>**right rule:** % returns the remainder, so 17 % 5 is 2.<br>role: primary |
| **remainder\_operator** | misconception | **RemainderIsSubtraction** | **wrong rule:** 9 % 5 means 9 minus 5 (a % b subtracts b from a).<br>**right rule:** % gives the remainder after integer division: 9 % 5 is 4 because 9 = 1 \* 5 + 4, and 17 % 5 is 2, not 12.<br>role: primary |
| **remainder\_operator** | has\_level | **remainder\_operator@L0** | remainder operator -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (4 ways).<br>**[0] everyday\_reading** (E): In everyday use % means percent (50% of x), and in maths 'mod' always gives a non-negative result. In Java % is the remainder of truncating division, and its sign follows the left operand (-14 % 3 is -2).<br>**[1] misconception** (M) &rarr; RemainderIsQuotient: wrong rule: 17 % 5 is 3 (the quotient). Right rule: % returns the remainder, so 17 % 5 is 2.<br>**[2] misconception** (M) &rarr; NegativeRemainderSign: wrong rule: a % b is never negative, and integer division of a negative number rounds down. Right rule: a / b rounds toward 0 and a % b takes the sign of a: -14 / 3 is -4 and -14 % 3 is -2.<br>**[3] inconsistent\_trace** (T) &rarr; RemainderIsQuotient: Points to LT (compute the truncated quotient, then the remainder). Applied unevenly, a student gives the remainder for positive operands but the mathematical mod for negatives, or swaps quotient and remainder (17 % 5 as 3). (here mixing in: "17 % 5 is 3 (the quotient)") |
| **remainder\_operator** | has\_level | **remainder\_operator@L1** | remainder operator -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).<br>**[0] names\_the\_element** (N): Remainder operator %: the binary operator that gives the remainder after dividing a by b.<br>**[1] states\_the\_rule** (S): For ints, a % b is defined so that (a / b) \* b + a % b equals a. The result takes the sign of a, % by zero throws ArithmeticException, and % also works on doubles. |
| **remainder\_operator** | has\_level | **remainder\_operator@L2** | remainder operator -&gt; L2 (Multistructural): the answer applies the rules of remainder operator to every part of the code, in order (3 ways).<br>**[0] line\_by\_line\_trace** (LT): Evaluate a, then b, take the quotient rounded toward 0, and give what is left over. % has the same precedence as \* and /, and they group left to right.<br>**[1] output\_prediction** (OP): 17 % 3 is 2, 76 % 12 is 4, 1234 % 99 is 46, -14 % 3 is -2, and 14 % -3 is 2.<br>**[2] one\_step\_execution** (OS): r = a % b stores a remainder smaller in size than b and leaves a and b unchanged. If b is 0, ArithmeticException is thrown before anything is stored. |
| **remainder\_operator** | has\_level | **remainder\_operator@L3** | remainder operator -&gt; L3 (Relational): the answer relates the parts (2 ways).<br>**[0] relation\_to\_neighbour** (R): % is the companion of integer division, since a == (a / b) \* b + a % b. Both use the same quotient rounded toward 0.<br>**[1] purpose\_of\_the\_whole** (P): Plans: divisibility and parity tests (x % 2 == 0), digit extraction (x % 10), cyclic wrap-around ((i + 1) % n), leap-year rules, and splitting units (76 % 12 inches). |
| **remainder\_operator** | has\_level | **remainder\_operator@L4** | remainder operator -&gt; L4 (Extended abstract): the answer reasons beyond the given code (5 ways).<br>**[0] predict\_a\_change** (C) &rarr; RemainderIsQuotient: Negating a flips the remainder's sign, so n % 2 == 1 fails for negative odd n while n % 2 != 0 still works. Changing the divisor changes the cycle length. Swapping % with / swaps the remainder for the quotient.<br>**[1] transfer\_to\_a\_new\_program** (X): Use % for divisibility, parity, digits, cyclic indices and unit splitting. Do not use it for percentages (use \* / 100.0), and do not use it where a non-negative mathematical mod is needed for negative values (adjust the result or use Math.floorMod).<br>**[2] diagnose\_an\_error** (D): rule broken: int remainder by zero is undefined. Kind: run-time exception. Trigger class: x % 0, or a divisor variable that is 0: ArithmeticException: / by zero.<br>**[3] diagnose\_an\_error** (D): rule broken: The remainder takes the sign of the dividend. Kind: silent logic error. Trigger class: Negative inputs in an odd test written as x % 2 == 1, or in a wrap-around index computed as (i - 1) % n.<br>**[4] diagnose\_an\_error** (D): rule broken: % is the remainder, not a percentage. Kind: silent logic error. Trigger class: Writing price % 15 for 15 percent of price. |
| **topic1.2.c** | contains | **arithmetic\_operators** | topic topic1.2.c contains arithmetic\_operators |
| **topic1.2.c** | contains | **int** | topic topic1.2.c contains int |
| **topic1.2.c** | contains | **int\_literal\_limit** | topic topic1.2.c contains int\_literal\_limit |
| **topic1.2.c** | contains | **integer\_constants** | topic topic1.2.c contains integer\_constants |
| **topic1.2.c** | contains | **integer\_division** | topic topic1.2.c contains integer\_division |
| **topic1.2.c** | contains | **long\_type** | topic topic1.2.c contains long\_type |
| **topic1.2.c** | contains | **overflow** | topic topic1.2.c contains overflow |
| **topic1.2.c** | contains | **remainder\_operator** | topic topic1.2.c contains remainder\_operator |
