# trig_functions (`trig_functions`)

Math.sin, Math.cos, Math.atan2 work in radians

Section 1.2 Built-in Types of Data, topic 1.2.g Library methods and APIs (Math). From the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`).

![The knowledge graph around trig_functions](trig_functions.png)

## Concepts associated with trig\_functions (5)

| Concept | Description | How it is associated |
| --- | --- | --- |
| **api** | a table of library methods giving each method's signature and a short description of what it computes | same topic (topic1.2.g) |
| **math\_library** | Math.abs, Math.sqrt, Math.max, Math.random, Math.round ... | prerequisite of it (it needs this)<br>composition rule (R) with it<br>same topic (topic1.2.g) |
| **math\_random** | Math.random() and scaling to an int range | same topic (topic1.2.g) |
| **math\_round** | Math.round rounds to the nearest integer and returns a long | same topic (topic1.2.g) |
| **method\_call** | name(arguments) -- invokes a library method and uses its return value | same topic (topic1.2.g) |

## Every edge in this view and its full label (13)

| From | Edge | To | Full edge label |
| --- | --- | --- | --- |
| **math\_library** | prerequisite | **trig\_functions** | The trig functions are Math library methods.<br>grounding: book\_passage<br>composition rule (R) of math\_library with trig\_functions: The trigonometric functions are Math methods whose angles are in radians; Math.toRadians and Math.toDegrees convert.<br>composition rule (R) of trig\_functions with math\_library: The trig functions belong to the Math API, whose note fixes the unit: angles are in radians, with toDegrees() and toRadians() for conversion. |
| **trig\_functions** | misconception | **TrigTakesDegrees** | **wrong rule:** Math.sin(30) is the sine of 30 degrees.<br>**right rule:** Math.sin takes radians; use Math.toRadians(30).<br>role: primary |
| **trig\_functions** | has\_level | **trig\_functions@L0** | trig functions -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (3 ways).<br>**[0] everyday\_reading** (E): Folk meaning: from school and calculators in degree mode, sin 30 means the sine of 30 degrees (0.5). Java rule: Math.sin, Math.cos and Math.tan take their argument in radians, so Math.sin(30) is about -0.988; use Math.sin(Math.toRadians(30)).<br>**[1] misconception** (M) &rarr; TrigTakesDegrees: wrong rule: Math.sin(30) is the sine of 30 degrees. Right rule: Math.sin takes radians; use Math.sin(Math.toRadians(30)).<br>**[2] inconsistent\_trace** (T) &rarr; TrigTakesDegrees: Points to LT (convert the angle to radians, then apply the function). Applied unevenly: in one program the student converts the angle before one call (Math.cos(Math.toRadians(x1))) but passes degrees directly to another (Math.sin(x2)). (here mixing in: "Math.sin(30) is the sine of 30 degrees") |
| **trig\_functions** | has\_level | **trig\_functions@L1** | trig functions -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).<br>**[0] names\_the\_element** (N): The trigonometric functions are Math library methods (sin, cos, tan, and inverses asin, acos, atan, atan2) whose angles are expressed in radians.<br>**[1] states\_the\_rule** (S): double sin(double theta), cos, tan take theta in radians; Math.toRadians and Math.toDegrees convert; the inverse functions return radians, and Math.atan2(y, x) returns the angle of (x, y) in the range from -pi to pi. |
| **trig\_functions** | has\_level | **trig\_functions@L2** | trig functions -&gt; L2 (Multistructural): the answer applies the rules of trig functions to every part of the code, in order (3 ways).<br>**[0] line\_by\_line\_trace** (LT): The argument expression is evaluated first (an inner Math.toRadians(deg) call runs before the outer Math.sin), then the function is computed on that double.<br>**[1] output\_prediction** (OP): A double: Math.sin(Math.PI/2) is 1.0; results are approximations, so Math.sin(Math.toRadians(30)) is 0.49999999999999994 and cos^2 + sin^2 is not always exactly 1.<br>**[2] one\_step\_execution** (OS): A trig call changes no variable; the result exists only if stored or used, e.g. double height = Math.sin(angle);. |
| **trig\_functions** | has\_level | **trig\_functions@L3** | trig functions -&gt; L3 (Relational): the answer relates the parts (2 ways).<br>**[0] relation\_to\_neighbour** (R): The trig functions belong to the Math API, whose note fixes the unit: angles are in radians, with toDegrees() and toRadians() for conversion.<br>**[1] purpose\_of\_the\_whole** (P): Used for geometry and periodic signals: polar coordinates (Math.atan2), great-circle distance, sampled sound waves (Math.sin(2\*Math.PI \* i \* hz / sps)), and points on a circle for drawing. |
| **trig\_functions** | has\_level | **trig\_functions@L4** | trig functions -&gt; L4 (Extended abstract): the answer reasons beyond the given code (3 ways).<br>**[0] predict\_a\_change** (C) &rarr; TrigTakesDegrees: Switching the input between degrees and radians changes the result completely (not just slightly); adding a full period 2\*Math.PI to the argument leaves the value unchanged up to rounding.<br>**[1] transfer\_to\_a\_new\_program** (X): Use the Math trig functions whenever angles or periodic behaviour are computed, converting degree inputs with Math.toRadians first; prefer Math.atan2(y, x) to Math.atan(y/x) when the full-circle angle is needed.<br>**[2] diagnose\_an\_error** (D): rule broken: Java's trigonometric functions take radians. Kind: silent logic error. Trigger class: An angle held in degrees (from user input, a formula given in degrees, or latitude/longitude) passed directly to Math.sin/cos/tan, or an inverse function's radian result printed as degrees. |
| **topic1.2.g** | contains | **api** | topic topic1.2.g contains api |
| **topic1.2.g** | contains | **math\_library** | topic topic1.2.g contains math\_library |
| **topic1.2.g** | contains | **math\_random** | topic topic1.2.g contains math\_random |
| **topic1.2.g** | contains | **math\_round** | topic topic1.2.g contains math\_round |
| **topic1.2.g** | contains | **method\_call** | topic topic1.2.g contains method\_call |
| **topic1.2.g** | contains | **trig\_functions** | topic topic1.2.g contains trig\_functions |
