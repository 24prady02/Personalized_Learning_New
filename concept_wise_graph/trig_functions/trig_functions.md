# trig_functions (`trig_functions`)

Math.sin, Math.cos, Math.atan2 work in radians

Section 1.2 Built-in Types of Data, topic 1.2.g Library methods and APIs (Math).

![The knowledge graph around trig_functions](trig_functions.png)

## At a glance

- **Needs first:** `math_library`
- **Leads to:** nothing
- **Learned alongside:** nothing
- **Misconceptions:** `TrigTakesDegrees`
- **Errors:** none
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 13 edges around this concept. The edge logic, the wrong and right rules and the exact rules of the ways are copied word for word from the graph.

## To work on (0)

Nothing is missing for this concept.

## What it needs first (1)

A prerequisite edge means the other concept has to be understood before `trig_functions`.

### `math_library` comes before `trig_functions`

*Math.abs, Math.sqrt, Math.max, Math.random, Math.round ...*

- **Edge:** `pre:math_library->trig_functions`
- **Exact edge logic:** The trig functions are Math library methods.
- **Grounding:** book\_passage
- **Composition rule (R) of `trig_functions` with `math_library`:** The trig functions belong to the Math API, whose note fixes the unit: angles are in radians, with toDegrees() and toRadians() for conversion.
- **Composition rule (R) of `math_library` with `trig_functions`:** The trigonometric functions are Math methods whose angles are in radians; Math.toRadians and Math.toDegrees convert.

## What it leads to (0)

These concepts need `trig_functions` first.

No concept has this one as a prerequisite.

## Learned alongside (0)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

No parallel edge touches this concept.

## Misconceptions (1)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### TrigTakesDegrees

- **Edge:** `trig_functions` &rarr; `TrigTakesDegrees` (misconception)
- **Exact edge logic (the wrong rule):** Math.sin(30) is the sine of 30 degrees.
- **Twin logic (the right rule):** Math.sin takes radians; use Math.toRadians(30).
- **Wrong belief (on the node):** Math.sin(30) is the sine of 30 degrees.
- **Correct rule (on the node):** Math.sin takes radians; use Math.toRadians(30).
- **Provenance:** derived
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [1] misconception, exact rule:** wrong rule: Math.sin(30) is the sine of 30 degrees. Right rule: Math.sin takes radians; use Math.sin(Math.toRadians(30)).
- **L0 way [2] inconsistent\_trace, exact rule:** Points to LT (convert the angle to radians, then apply the function). Applied unevenly: in one program the student converts the angle before one call (Math.cos(Math.toRadians(x1))) but passes degrees directly to another (Math.sin(x2)). (here mixing in: "Math.sin(30) is the sine of 30 degrees")

## Errors (0)

An error edge states the rule that gets broken in a program, and the right rule.

The graph has no error edge from this concept.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for trig functions: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to trig functions agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

- **Edge:** `trig_functions` &rarr; `trig_functions@L0` (has_level)
- **Exact edge logic:** trig functions -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (3 ways).

Ways (3), each with its exact rule:

- **[0] everyday\_reading** (rule type E, folk-meaning rule): Folk meaning: from school and calculators in degree mode, sin 30 means the sine of 30 degrees (0.5). Java rule: Math.sin, Math.cos and Math.tan take their argument in radians, so Math.sin(30) is about -0.988; use Math.sin(Math.toRadians(30)).
- **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `TrigTakesDegrees`: wrong rule: Math.sin(30) is the sine of 30 degrees. Right rule: Math.sin takes radians; use Math.sin(Math.toRadians(30)).
- **[2] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `TrigTakesDegrees`: Points to LT (convert the angle to radians, then apply the function). Applied unevenly: in one program the student converts the angle before one call (Math.cos(Math.toRadians(x1))) but passes degrees directly to another (Math.sin(x2)). (here mixing in: "Math.sin(30) is the sine of 30 degrees")

### L1: Unistructural / atom x text surface

L1 for trig functions: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

- **Edge:** `trig_functions` &rarr; `trig_functions@L1` (has_level)
- **Exact edge logic:** trig functions -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

Ways (2), each with its exact rule:

- **[0] names\_the\_element** (rule type N, identity rule): The trigonometric functions are Math library methods (sin, cos, tan, and inverses asin, acos, atan, atan2) whose angles are expressed in radians.
- **[1] states\_the\_rule** (rule type S, declarative rule): double sin(double theta), cos, tan take theta in radians; Math.toRadians and Math.toDegrees convert; the inverse functions return radians, and Math.atan2(y, x) returns the angle of (x, y) in the range from -pi to pi.

### L2: Multistructural / block x execution / preoperational

L2 for trig functions: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

- **Edge:** `trig_functions` &rarr; `trig_functions@L2` (has_level)
- **Exact edge logic:** trig functions -&gt; L2 (Multistructural): the answer applies the rules of trig functions to every part of the code, in order (3 ways).

Ways (3), each with its exact rule:

- **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): The argument expression is evaluated first (an inner Math.toRadians(deg) call runs before the outer Math.sin), then the function is computed on that double.
- **[1] output\_prediction** (rule type OP, evaluation / result rule): A double: Math.sin(Math.PI/2) is 1.0; results are approximations, so Math.sin(Math.toRadians(30)) is 0.49999999999999994 and cos^2 + sin^2 is not always exactly 1.
- **[2] one\_step\_execution** (rule type OS, state-transition rule): A trig call changes no variable; the result exists only if stored or used, e.g. double height = Math.sin(angle);.

### L3: Relational / relations x function (concrete operational begins)

L3 for trig functions: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

- **Edge:** `trig_functions` &rarr; `trig_functions@L3` (has_level)
- **Exact edge logic:** trig functions -&gt; L3 (Relational): the answer relates the parts (2 ways).

Ways (2), each with its exact rule:

- **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): The trig functions belong to the Math API, whose note fixes the unit: angles are in radians, with toDegrees() and toRadians() for conversion.
- **[1] purpose\_of\_the\_whole** (rule type P, plan / role rule): Used for geometry and periodic signals: polar coordinates (Math.atan2), great-circle distance, sampled sound waves (Math.sin(2\*Math.PI \* i \* hz / sps)), and points on a circle for drawing.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for trig functions: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

- **Edge:** `trig_functions` &rarr; `trig_functions@L4` (has_level)
- **Exact edge logic:** trig functions -&gt; L4 (Extended abstract): the answer reasons beyond the given code (3 ways).

Ways (3), each with its exact rule:

- **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `TrigTakesDegrees`: Switching the input between degrees and radians changes the result completely (not just slightly); adding a full period 2\*Math.PI to the argument leaves the value unchanged up to rounding.
- **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Use the Math trig functions whenever angles or periodic behaviour are computed, converting degree inputs with Math.toRadians first; prefer Math.atan2(y, x) to Math.atan(y/x) when the full-circle angle is needed.
- **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: Java's trigonometric functions take radians. Kind: silent logic error. Trigger class: An angle held in degrees (from user input, a formula given in degrees, or latitude/longitude) passed directly to Math.sin/cos/tan, or an inverse function's radian result printed as degrees.

## Same topic

`trig_functions` belongs to the topic **Library methods and APIs (Math)** (`topic1.2.g`). The topic also contains: `api`, `math_library`, `math_random`, `math_round`, `method_call`.

## Rules of the concept (13)

- **Book** (SW-1e, p. 44 (pdf 54)): "Note that this equation uses degrees, whereas Java's trigonometric functions use radians."
- **Book** (SW-1.2, ): "trigonometric functions in the Math library, such as Math.sin(), Math.cos(), and Math.toRadians()"
- **E** (folk-meaning rule): Folk meaning: from school and calculators in degree mode, sin 30 means the sine of 30 degrees (0.5). Java rule: Math.sin, Math.cos and Math.tan take their argument in radians, so Math.sin(30) is about -0.988; use Math.sin(Math.toRadians(30)).
- **M** (wrong rule / right rule): TrigTakesDegrees: wrong: Math.sin(30) is the sine of 30 degrees. \| right: Math.sin takes radians; use Math.sin(Math.toRadians(30)).
- **T** (uneven-application rule): Points to LT (convert the angle to radians, then apply the function). Applied unevenly: in one program the student converts the angle before one call (Math.cos(Math.toRadians(x1))) but passes degrees directly to another (Math.sin(x2)).
- **N** (identity rule): The trigonometric functions are Math library methods (sin, cos, tan, and inverses asin, acos, atan, atan2) whose angles are expressed in radians.
- **S** (declarative rule): double sin(double theta), cos, tan take theta in radians; Math.toRadians and Math.toDegrees convert; the inverse functions return radians, and Math.atan2(y, x) returns the angle of (x, y) in the range from -pi to pi.
- **LT** (operational sequencing rule): The argument expression is evaluated first (an inner Math.toRadians(deg) call runs before the outer Math.sin), then the function is computed on that double.
- **OP** (evaluation / result rule): A double: Math.sin(Math.PI/2) is 1.0; results are approximations, so Math.sin(Math.toRadians(30)) is 0.49999999999999994 and cos^2 + sin^2 is not always exactly 1.
- **OS** (state-transition rule): A trig call changes no variable; the result exists only if stored or used, e.g. double height = Math.sin(angle);.
- **R** (composition rule (with a neighbour)): with math\_library: The trig functions belong to the Math API, whose note fixes the unit: angles are in radians, with toDegrees() and toRadians() for conversion.
- **P** (plan / role rule): Used for geometry and periodic signals: polar coordinates (Math.atan2), great-circle distance, sampled sound waves (Math.sin(2\*Math.PI \* i \* hz / sps)), and points on a circle for drawing.
- **C** (conservation rule): Switching the input between degrees and radians changes the result completely (not just slightly); adding a full period 2\*Math.PI to the argument leaves the value unchanged up to rounding.
- **D** (error rule): rule broken: Java's trigonometric functions take radians. (silent logic error)
- **X** (applicability rule): Use the Math trig functions whenever angles or periodic behaviour are computed, converting degree inputs with Math.toRadians first; prefer Math.atan2(y, x) to Math.atan(y/x) when the full-circle angle is needed.

## How it is found in code and answers (reader block)

- **Aliases:** sine, cosine, math.sin, math.cos
- **Code patterns:** `Math\.(?:sin|cos|tan|atan2?|asin|acos|toRadians|toDegrees)\s*\(`
- **Operator symbols:** none
- **Java types:** none

## The whole prerequisite chain

- **Everything it builds on (9):** `arithmetic_operators`, `data_type`, `expression`, `identifier`, `literal`, `math_library`, `method_call`, `primitive_type`, `variable`
- **Everything that builds on it (0):** nothing

## Every edge in this view and its exact edge logic (13)

All the edges drawn in the picture, in the order: prerequisite, parallel, misconception, error, has_level, contains.

**1. `math_library` &rarr; `trig_functions`** (prerequisite)

- **Exact edge logic:** The trig functions are Math library methods.
- **Grounding:** book\_passage
- **Composition rule (R) of `math_library` with `trig_functions`:** The trigonometric functions are Math methods whose angles are in radians; Math.toRadians and Math.toDegrees convert.
- **Composition rule (R) of `trig_functions` with `math_library`:** The trig functions belong to the Math API, whose note fixes the unit: angles are in radians, with toDegrees() and toRadians() for conversion.

**2. `trig_functions` &rarr; `TrigTakesDegrees`** (misconception)

- **Exact edge logic (the wrong rule):** Math.sin(30) is the sine of 30 degrees.
- **Twin logic (the right rule):** Math.sin takes radians; use Math.toRadians(30).
- **Role:** primary

**3. `trig_functions` &rarr; `trig_functions@L0`** (has_level)

- **Exact edge logic:** trig functions -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (3 ways).
  - **[0] everyday\_reading** (rule type E, folk-meaning rule): Folk meaning: from school and calculators in degree mode, sin 30 means the sine of 30 degrees (0.5). Java rule: Math.sin, Math.cos and Math.tan take their argument in radians, so Math.sin(30) is about -0.988; use Math.sin(Math.toRadians(30)).
  - **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `TrigTakesDegrees`: wrong rule: Math.sin(30) is the sine of 30 degrees. Right rule: Math.sin takes radians; use Math.sin(Math.toRadians(30)).
  - **[2] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `TrigTakesDegrees`: Points to LT (convert the angle to radians, then apply the function). Applied unevenly: in one program the student converts the angle before one call (Math.cos(Math.toRadians(x1))) but passes degrees directly to another (Math.sin(x2)). (here mixing in: "Math.sin(30) is the sine of 30 degrees")

**4. `trig_functions` &rarr; `trig_functions@L1`** (has_level)

- **Exact edge logic:** trig functions -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).
  - **[0] names\_the\_element** (rule type N, identity rule): The trigonometric functions are Math library methods (sin, cos, tan, and inverses asin, acos, atan, atan2) whose angles are expressed in radians.
  - **[1] states\_the\_rule** (rule type S, declarative rule): double sin(double theta), cos, tan take theta in radians; Math.toRadians and Math.toDegrees convert; the inverse functions return radians, and Math.atan2(y, x) returns the angle of (x, y) in the range from -pi to pi.

**5. `trig_functions` &rarr; `trig_functions@L2`** (has_level)

- **Exact edge logic:** trig functions -&gt; L2 (Multistructural): the answer applies the rules of trig functions to every part of the code, in order (3 ways).
  - **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): The argument expression is evaluated first (an inner Math.toRadians(deg) call runs before the outer Math.sin), then the function is computed on that double.
  - **[1] output\_prediction** (rule type OP, evaluation / result rule): A double: Math.sin(Math.PI/2) is 1.0; results are approximations, so Math.sin(Math.toRadians(30)) is 0.49999999999999994 and cos^2 + sin^2 is not always exactly 1.
  - **[2] one\_step\_execution** (rule type OS, state-transition rule): A trig call changes no variable; the result exists only if stored or used, e.g. double height = Math.sin(angle);.

**6. `trig_functions` &rarr; `trig_functions@L3`** (has_level)

- **Exact edge logic:** trig functions -&gt; L3 (Relational): the answer relates the parts (2 ways).
  - **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): The trig functions belong to the Math API, whose note fixes the unit: angles are in radians, with toDegrees() and toRadians() for conversion.
  - **[1] purpose\_of\_the\_whole** (rule type P, plan / role rule): Used for geometry and periodic signals: polar coordinates (Math.atan2), great-circle distance, sampled sound waves (Math.sin(2\*Math.PI \* i \* hz / sps)), and points on a circle for drawing.

**7. `trig_functions` &rarr; `trig_functions@L4`** (has_level)

- **Exact edge logic:** trig functions -&gt; L4 (Extended abstract): the answer reasons beyond the given code (3 ways).
  - **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `TrigTakesDegrees`: Switching the input between degrees and radians changes the result completely (not just slightly); adding a full period 2\*Math.PI to the argument leaves the value unchanged up to rounding.
  - **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Use the Math trig functions whenever angles or periodic behaviour are computed, converting degree inputs with Math.toRadians first; prefer Math.atan2(y, x) to Math.atan(y/x) when the full-circle angle is needed.
  - **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: Java's trigonometric functions take radians. Kind: silent logic error. Trigger class: An angle held in degrees (from user input, a formula given in degrees, or latitude/longitude) passed directly to Math.sin/cos/tan, or an inverse function's radian result printed as degrees.

**8. `topic1.2.g` &rarr; `trig_functions`** (contains)

- topic `topic1.2.g` contains `trig_functions`

**9. `topic1.2.g` &rarr; `api`** (contains)

- topic `topic1.2.g` contains `api`

**10. `topic1.2.g` &rarr; `math_library`** (contains)

- topic `topic1.2.g` contains `math_library`

**11. `topic1.2.g` &rarr; `math_random`** (contains)

- topic `topic1.2.g` contains `math_random`

**12. `topic1.2.g` &rarr; `math_round`** (contains)

- topic `topic1.2.g` contains `math_round`

**13. `topic1.2.g` &rarr; `method_call`** (contains)

- topic `topic1.2.g` contains `method_call`
