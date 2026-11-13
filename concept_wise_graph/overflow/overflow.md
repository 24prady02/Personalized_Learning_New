# overflow (`overflow`)

int arithmetic wraps around outside the 32-bit range

Section 1.2 Built-in Types of Data, topic 1.2.c Integers. From the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`).

![The knowledge graph around overflow](overflow.png)

## Concepts associated with overflow (9)

| Concept | Description | How it is associated |
| --- | --- | --- |
| **arithmetic\_operators** | + - \* / % | same topic (topic1.2.c) |
| **floating\_point\_precision** | double values are approximations; == on doubles is unreliable | parallel concept |
| **int** | 32-bit integer primitive | prerequisite of it (it needs this)<br>composition rule (R) with it<br>shares misconception IntOverflowWidensAutomatically<br>same topic (topic1.2.c) |
| **int\_literal\_limit** | 2147483648 is legal only as -2147483648 | same topic (topic1.2.c) |
| **integer\_constants** | Integer.MAX\_VALUE, Integer.MIN\_VALUE and their edge cases | builds on it (needs it)<br>composition rule (R) with it<br>shares misconception AbsAlwaysNonNegative<br>same topic (topic1.2.c) |
| **integer\_division** | / on two ints truncates; % is the remainder | same topic (topic1.2.c) |
| **long\_type** | 64-bit integer type for values beyond the int range | same topic (topic1.2.c) |
| **math\_library** | Math.abs, Math.sqrt, Math.max, Math.random, Math.round ... | shares misconception AbsAlwaysNonNegative |
| **remainder\_operator** | % gives the remainder of integer division | same topic (topic1.2.c) |

## Every edge in this view and its full label (21)

| From | Edge | To | Full edge label |
| --- | --- | --- | --- |
| **int** | prerequisite | **overflow** | Overflow happens because an int has a fixed 32-bit range.<br>grounding: book\_passage<br>composition rule (R) of int with overflow: Because int has a fixed 32-bit range, results outside it wrap around silently.<br>composition rule (R) of overflow with int: Overflow is possible because int has a fixed 32-bit range, -2^31 to 2^31 - 1. |
| **overflow** | prerequisite | **integer\_constants** | Integer.MAX\_VALUE is used to test for overflow: an int result that would go past it wraps around to a negative value.<br>grounding: book\_passage<br>composition rule (R) of overflow with integer\_constants: Integer.MAX\_VALUE and Integer.MIN\_VALUE mark the edges of the range. Testing a &gt; Integer.MAX\_VALUE - b before computing a + b avoids overflow.<br>composition rule (R) of integer\_constants with overflow: Integer.MAX\_VALUE marks the overflow boundary: an int result past it wraps to a negative value, so a test such as sum &gt; Integer.MAX\_VALUE on an int is always false; an overflow guard must test before the operation (e.g. a &gt; Integer.MAX\_VALUE - b) or use long. |
| **overflow** | parallel | **floating\_point\_precision** | Both come from finite representations: an int result too large for 32 bits wraps around silently (overflow), while a double keeps about 15 significant digits so most results are approximations (5.0/3.0 is 1.6666666666666667). Neither raises an error.<br>grounding: book\_passage |
| **int** | misconception | **IntOverflowWidensAutomatically** | **wrong rule:** An int result that is too large is automatically stored as a bigger number.<br>**right rule:** int arithmetic is 32-bit; a result outside the range wraps around.<br>role: context |
| **integer\_constants** | misconception | **AbsAlwaysNonNegative** | **wrong rule:** Math.abs always returns a non-negative number.<br>**right rule:** Math.abs(Integer.MIN\_VALUE) returns Integer.MIN\_VALUE, which is negative.<br>role: context |
| **math\_library** | misconception | **AbsAlwaysNonNegative** | **wrong rule:** Math.abs always returns a non-negative number.<br>**right rule:** Math.abs(Integer.MIN\_VALUE) returns Integer.MIN\_VALUE, which is negative.<br>role: primary |
| **overflow** | misconception | **AbsAlwaysNonNegative** | **wrong rule:** Math.abs always returns a non-negative number.<br>**right rule:** Math.abs(Integer.MIN\_VALUE) returns Integer.MIN\_VALUE, which is negative.<br>role: context |
| **overflow** | misconception | **IntOverflowWidensAutomatically** | **wrong rule:** An int result that is too large is automatically stored as a bigger number.<br>**right rule:** int arithmetic is 32-bit; a result outside the range wraps around.<br>role: primary |
| **overflow** | has\_level | **overflow@L0** | overflow -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (3 ways).<br>**[0] everyday\_reading** (E): Everyday arithmetic assumes a bigger result just takes more digits. A Java int keeps only 32 bits, so a result that is too large wraps silently to a wrong (often negative) value.<br>**[1] misconception** (M) &rarr; IntOverflowWidensAutomatically: wrong rule: An int result that is too large is automatically stored as a bigger number. Right rule: int arithmetic is 32-bit; a result outside the range wraps around.<br>**[2] inconsistent\_trace** (T) &rarr; IntOverflowWidensAutomatically: Points to LT (each int operation wraps as soon as it leaves the range). Applied unevenly, a student wraps one step but writes a + 1 for a = Integer.MAX\_VALUE as 2147483648. (here mixing in: "An int result that is too large is automatically stored as a bigger number") |
| **overflow** | has\_level | **overflow@L1** | overflow -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).<br>**[0] names\_the\_element** (N): Overflow: the situation where an integer result is too large or too small for its type's fixed bits and is truncated, wrapping around.<br>**[1] states\_the\_rule** (S): int and long arithmetic is done in 32-bit and 64-bit two's complement. An out-of-range result keeps only its low-order bits, and no error or exception is raised. |
| **overflow** | has\_level | **overflow@L2** | overflow -&gt; L2 (Multistructural): the answer applies the rules of overflow to every part of the code, in order (3 ways).<br>**[0] line\_by\_line\_trace** (LT): Overflow happens in the single operation whose result leaves the range, before any later widening. With int a and b, long x = a \* b; overflows in 32-bit int arithmetic before the result is converted to long.<br>**[1] output\_prediction** (OP): Integer.MAX\_VALUE + 1 is -2147483648, 2 \* Integer.MAX\_VALUE is -2, and Math.abs(-2147483648) is -2147483648.<br>**[2] one\_step\_execution** (OS): The variable receives the wrapped value and nothing signals the error, so later statements carry on with it. |
| **overflow** | has\_level | **overflow@L3** | overflow -&gt; L3 (Relational): the answer relates the parts (4 ways).<br>**[0] relation\_to\_neighbour** (R): Overflow is possible because int has a fixed 32-bit range, -2^31 to 2^31 - 1.<br>**[1] relation\_to\_neighbour** (R): Integer.MAX\_VALUE and Integer.MIN\_VALUE mark the edges of the range. Testing a &gt; Integer.MAX\_VALUE - b before computing a + b avoids overflow.<br>**[2] relation\_to\_neighbour** (R): Both come from finite representations: an int result too large for 32 bits wraps around silently (overflow), while a double keeps about 15 significant digits so most results are approximations (5.0/3.0 is 1.6666666666666667). Neither raises an error.<br>**[3] purpose\_of\_the\_whole** (P): Knowing about overflow lets you guard against it: use long for products, factorials and large sums, or check against MAX\_VALUE before computing. |
| **overflow** | has\_level | **overflow@L4** | overflow -&gt; L4 (Extended abstract): the answer reasons beyond the given code (4 ways).<br>**[0] predict\_a\_change** (C) &rarr; IntOverflowWidensAutomatically: Changing int to long moves the overflow point (to about 9.2e18) but does not remove it. Dividing before multiplying can avoid overflow at the cost of truncation. Casting a result that has already overflowed does not repair it.<br>**[1] transfer\_to\_a\_new\_program** (X): Think about overflow whenever values can reach the billions. Use long (or a long operand, such as 1000L) for those, BigInteger for unbounded integers, and plain int for small counts and indices.<br>**[2] diagnose\_an\_error** (D): rule broken: int results are limited to 32 bits, and overflow is not reported. Kind: silent logic error. Trigger class: Values that reach into the billions: factorials above 12!, large products or powers, sums of many large values, Math.abs(Integer.MIN\_VALUE).<br>**[3] diagnose\_an\_error** (D): rule broken: An all-int expression is computed in int even when its result is stored in a long. Kind: silent logic error. Trigger class: long total = a \* b; or long ms = days \* 24 \* 60 \* 60 \* 1000; with int operands. |
| **topic1.2.c** | contains | **arithmetic\_operators** | topic topic1.2.c contains arithmetic\_operators |
| **topic1.2.c** | contains | **int** | topic topic1.2.c contains int |
| **topic1.2.c** | contains | **int\_literal\_limit** | topic topic1.2.c contains int\_literal\_limit |
| **topic1.2.c** | contains | **integer\_constants** | topic topic1.2.c contains integer\_constants |
| **topic1.2.c** | contains | **integer\_division** | topic topic1.2.c contains integer\_division |
| **topic1.2.c** | contains | **long\_type** | topic topic1.2.c contains long\_type |
| **topic1.2.c** | contains | **overflow** | topic topic1.2.c contains overflow |
| **topic1.2.c** | contains | **remainder\_operator** | topic topic1.2.c contains remainder\_operator |
