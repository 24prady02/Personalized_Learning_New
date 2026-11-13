# math_library (`math_library`)

Math.abs, Math.sqrt, Math.max, Math.random, Math.round ...

Section 1.2 Built-in Types of Data, topic 1.2.g Library methods and APIs (Math).

![The knowledge graph around math_library](math_library.png)

## At a glance

- **Needs first:** `method_call`
- **Leads to:** `math_random`, `math_round`, `random_move`, `shuffle`, `standard_audio`, `trig_functions`
- **Learned alongside:** nothing
- **Misconceptions:** `AbsAlwaysNonNegative`, `CastRounds`
- **Errors:** `MathMethodWithoutClassName`, `WrongArgumentType`
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 29 edges around this concept, each explained in the graph's own words.

## What it needs first (1)

A prerequisite edge means the other concept has to be understood before `math_library`.

### `method_call` comes before `math_library`

*name(arguments) -- invokes a library method and uses its return value*

Math.sqrt(x) and other Math methods are used through method calls.

- **Grounding:** book passage
- **How `math_library` combines with `method_call`:** Every Math facility is used through a method call with the Math. prefix and parentheses (the constants Math.PI and Math.E are written without parentheses).
- **How `method_call` combines with `math_library`:** Math methods are called through the class name, Math.sqrt(x); without the prefix the compiler looks for the method in the current class and reports cannot find symbol.

## What it leads to (6)

These concepts need `math_library` first.

### `math_library` comes before `math_random`

*Math.random() and scaling to an int range*

Math.random() is a Math library method; unlike the others it takes no argument and returns a random double in [0, 1).

- **Grounding:** book passage
- **How `math_library` combines with `math_random`:** Math.random() is the one Math method that takes no argument and is not a mathematical function: it returns a random double in [0, 1).
- **How `math_random` combines with `math_library`:** Math.random() is the Math method that takes no argument and, unlike the others, is not a function of its input: it returns a random double in [0, 1).

### `math_library` comes before `math_round`

*Math.round rounds to the nearest integer and returns a long*

Math.round is a Math library method.

- **Grounding:** book passage
- **How `math_library` combines with `math_round`:** Math.round is the Math method that rounds to the nearest integer, but it returns a long, so storing it in an int needs a cast.
- **How `math_round` combines with `math_library`:** Math.round is listed in the Math API with return type long, which is what forces the cast when the result goes to an int (unlike the other Math methods, which return double).

### `math_library` comes before `random_move`

*pick the next page from a cumulative-probability test*

The random move draws r with Math.random() and then finds the interval of row p[page] that contains r.

- **Grounding:** book passage
- **How `math_library` combines with `random_move`:** The random move draws r = Math.random() once per move and compares it with growing cumulative sums of row p[page] to find which interval contains it.
- **How `random_move` combines with `math_library`:** Math.random() supplies one uniform double in [0, 1) per move; it must be called once before the j loop, not inside it.

### `math_library` comes before `shuffle`

*Knuth shuffle -- swap a[i] with a random a[r], r in i..n-1*

The random position r between i and N-1 is computed with Math.random(), so each remaining card is equally likely to be chosen.

- **Grounding:** book passage
- **How `math_library` combines with `shuffle`:** In the shuffle, r = i + (int) (Math.random() \* (N-i)) scales Math.random() to a uniformly random position between i and N-1, so each remaining card is equally likely.
- **How `shuffle` combines with `math_library`:** (int) (Math.random() \* (N-i)) is a uniform int in 0..N-i-1, so r = i + that value is uniform in i..N-1.

### `math_library` comes before `standard_audio`

*StdAudio: sound as an array of samples*

To play a tone, each sample a[i] of the sound array is computed with Math.sin at evenly spaced times.

- **Grounding:** book passage
- **How `math_library` combines with `standard_audio`:** Each sample a[i] = Math.sin(2\*Math.PI \* i \* hz / sps) is taken at evenly spaced times; the 2\*Math.PI factor is needed because Math.sin works in radians, one cycle being 2 pi.
- **How `standard_audio` combines with `math_library`:** Each sample is computed with Math.sin at evenly spaced times t = i/sps. The note's frequency comes from Math.pow(2, pitch/12.0).

### `math_library` comes before `trig_functions`

*Math.sin, Math.cos, Math.atan2 work in radians*

The trig functions are Math library methods.

- **Grounding:** book passage
- **How `math_library` combines with `trig_functions`:** The trigonometric functions are Math methods whose angles are in radians; Math.toRadians and Math.toDegrees convert.
- **How `trig_functions` combines with `math_library`:** The trig functions belong to the Math API, whose note fixes the unit: angles are in radians, with toDegrees() and toRadians() for conversion.

## Learned alongside (0)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

No parallel edge touches this concept.

## Misconceptions (2)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### AbsAlwaysNonNegative

- **Wrong rule:** Math.abs always returns a non-negative number.
- **Right rule:** Math.abs(Integer.MIN\_VALUE) returns Integer.MIN\_VALUE, which is negative.
- **Role of this concept:** primary
- **Also an edge from `integer_constants`:** Math.abs always returns a non-negative number.
- **Also an edge from `overflow`:** Math.abs always returns a non-negative number.

### CastRounds

- **Wrong rule:** (int) 2.7 evaluates to 3.
- **Right rule:** A cast to int discards the fractional part (rounds toward zero, so (int) -2.7 is -2); Math.round rounds to the nearest integer.
- **Role of this concept:** context
- **Shows at level L0 as:** misconception: wrong rule: (int) 2.7 evaluates to 3. Right rule: A cast to int discards the fractional part (rounds toward zero, so (int) -2.7 is -2); Math.round rounds to the nearest integer.
- **Shows at level L0 as:** inconsistent trace: Points to LT (the argument is evaluated, then the method computes from it). Applied unevenly: within one trace the student feeds degrees to Math.sin on one call and radians on another, or rounds the result of one call and truncates another. (here mixing in: "(int) 2.7 evaluates to 3")
- **Also an edge from `explicit_cast`:** (int) 2.7 evaluates to 3.
- **Also an edge from `math_round`:** (int) 2.7 evaluates to 3.

## Errors (2)

An error edge states the rule that gets broken in a program, and the right rule.

### MathMethodWithoutClassName

- **Wrong rule:** sqrt(x) calls the square-root method.
- **Right rule:** Library methods are called with the class name, e.g. Math.sqrt(x).
- **Role of this concept:** context
- **Also an edge from `compile_time_error`:** sqrt(x) calls the square-root method.
- **Also an edge from `method_call`:** sqrt(x) calls the square-root method.

### WrongArgumentType

- **Wrong rule:** Calls a method with arguments of the wrong type, e.g. Math.sqrt("2").
- **Right rule:** Each argument must have the type the method's API lists.
- **Role of this concept:** context
- **Also an edge from `method_call`:** Calls a method with arguments of the wrong type, e.g. Math.sqrt("2").

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for math library: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to math library agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

math library -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (3 ways).

- **everyday reading** (folk-meaning rule): Folk meaning: the calculator's function buttons, which work in degrees, round 2.7 to 3 when 'converting to a whole number', and always give a non-negative absolute value. Java rule: Math's trigonometric methods take radians, a cast to int truncates (only Math.round rounds, returning a long), and integer overflow makes Math.abs(-2147483648) negative.
- **misconception** (wrong rule / right rule; shows `CastRounds`): wrong rule: (int) 2.7 evaluates to 3. Right rule: A cast to int discards the fractional part (rounds toward zero, so (int) -2.7 is -2); Math.round rounds to the nearest integer.
- **inconsistent trace** (uneven-application rule; shows `CastRounds`): Points to LT (the argument is evaluated, then the method computes from it). Applied unevenly: within one trace the student feeds degrees to Math.sin on one call and radians on another, or rounds the result of one call and truncates another. (here mixing in: "(int) 2.7 evaluates to 3")

### L1: Unistructural / atom x text surface

L1 for math library: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

math library -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

- **names the element** (identity rule): The Math library is Java's class Math (in java.lang, no import needed) of static methods for mathematical functions (abs, max, min, sin, cos, tan, exp, log, pow, sqrt, round, random) and the constants PI and E.
- **states the rule** (declarative rule): Per the API: double abs/max/min (also for int, long, float), double sin/cos/tan(double theta) with theta in radians, double exp, log (natural), pow(a, b), sqrt; long round(double); double random() in [0, 1); constants Math.PI and Math.E.

### L2: Multistructural / block x execution / preoperational

L2 for math library: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

math library -&gt; L2 (Multistructural): the answer applies the rules of math library to every part of the code, in order (3 ways).

- **line by line trace** (operational sequencing rule): For Math.f(arg): evaluate arg (an int argument is widened to double), call the method, use the returned double in the enclosing expression; in nested calls the innermost runs first.
- **output prediction** (evaluation / result rule): Math.sqrt(2.0) is 1.4142135623730951, Math.sqrt(-1.0) is NaN, Math.sin(Math.PI/2) is 1.0, Math.log(Math.E) is 1.0, Math.pow(2.0, 10.0) is 1024.0, and Math.abs(-2147483648) is -2147483648.
- **one step execution** (state-transition rule): All the listed Math methods except random() are mathematical functions: they change no variable and return the same result for the same argument; random() takes no argument and returns a different value on each call.

### L3: Relational / relations x function (concrete operational begins)

L3 for math library: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

math library -&gt; L3 (Relational): the answer relates the parts (8 ways).

- **relation to neighbour** (composition rule (with a neighbour)): Every Math facility is used through a method call with the Math. prefix and parentheses (the constants Math.PI and Math.E are written without parentheses).
- **relation to neighbour** (composition rule (with a neighbour)): In the shuffle, r = i + (int) (Math.random() \* (N-i)) scales Math.random() to a uniformly random position between i and N-1, so each remaining card is equally likely.
- **relation to neighbour** (composition rule (with a neighbour)): Each sample a[i] = Math.sin(2\*Math.PI \* i \* hz / sps) is taken at evenly spaced times; the 2\*Math.PI factor is needed because Math.sin works in radians, one cycle being 2 pi.
- **relation to neighbour** (composition rule (with a neighbour)): Math.random() is the one Math method that takes no argument and is not a mathematical function: it returns a random double in [0, 1).
- **relation to neighbour** (composition rule (with a neighbour)): Math.round is the Math method that rounds to the nearest integer, but it returns a long, so storing it in an int needs a cast.
- **relation to neighbour** (composition rule (with a neighbour)): The trigonometric functions are Math methods whose angles are in radians; Math.toRadians and Math.toDegrees convert.
- **relation to neighbour** (composition rule (with a neighbour)): The random move draws r = Math.random() once per move and compares it with growing cumulative sums of row p[page] to find which interval contains it.
- **purpose of the whole** (plan / role rule): Used as a black box for standard numeric computations so that a program reads like the formula, e.g. Quadratic computes double d = Math.sqrt(discriminant);.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for math library: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

math library -&gt; L4 (Extended abstract): the answer reasons beyond the given code (5 ways).

- **predict a change** (conservation rule; shows `CastRounds`): Replacing Math.pow(x, 2) by x \* x keeps the value (up to rounding) and is cheaper; replacing Math.round(x) by (int) x changes results whenever the fractional part is at least .5 (and for negatives); replacing Math.sin(x)/Math.cos(x) by Math.tan(x) keeps the value.
- **diagnose an error** (error rule): rule broken: Library methods are called with the class name, e.g. Math.sqrt(x). Kind: compile-time. Trigger class: Calling sqrt(x) or pow(a, b) without Math. (cannot find symbol).
- **transfer to a new program** (applicability rule): Use Math for standard functions (roots, logs, trig, extremes, rounding, randomness); for squaring or small known integer powers multiply instead of calling Math.pow, and write known powers of ten as literals such as 1e6.
- **diagnose an error** (error rule): rule broken: Each argument must have the type the method's API lists. Kind: compile-time. Trigger class: Passing a String (Math.sqrt("2")) or a boolean to a Math method; numeric arguments are widened automatically.
- **diagnose an error** (error rule): rule broken: Math.sqrt and Math.log are undefined for negative arguments and return NaN. Kind: silent logic error. Trigger class: A negative argument (e.g. a negative discriminant in Quadratic, Math.log(-1)); NaN then propagates to the output.

## Same topic

`math_library` belongs to the topic **Library methods and APIs (Math)** (`topic1.2.g`). The topic also contains: `api`, `math_random`, `math_round`, `method_call`, `trig_functions`.

## Rules of the concept (21)

- **folk-meaning rule:** Folk meaning: the calculator's function buttons, which work in degrees, round 2.7 to 3 when 'converting to a whole number', and always give a non-negative absolute value. Java rule: Math's trigonometric methods take radians, a cast to int truncates (only Math.round rounds, returning a long), and integer overflow makes Math.abs(-2147483648) negative.
- **wrong rule / right rule:** CastRounds: wrong: (int) 2.7 evaluates to 3. \| right: A cast to int discards the fractional part (rounds toward zero, so (int) -2.7 is -2); Math.round rounds to the nearest integer.
- **uneven-application rule:** Points to LT (the argument is evaluated, then the method computes from it). Applied unevenly: within one trace the student feeds degrees to Math.sin on one call and radians on another, or rounds the result of one call and truncates another.
- **identity rule:** The Math library is Java's class Math (in java.lang, no import needed) of static methods for mathematical functions (abs, max, min, sin, cos, tan, exp, log, pow, sqrt, round, random) and the constants PI and E.
- **declarative rule:** Per the API: double abs/max/min (also for int, long, float), double sin/cos/tan(double theta) with theta in radians, double exp, log (natural), pow(a, b), sqrt; long round(double); double random() in [0, 1); constants Math.PI and Math.E.
- **operational sequencing rule:** For Math.f(arg): evaluate arg (an int argument is widened to double), call the method, use the returned double in the enclosing expression; in nested calls the innermost runs first.
- **evaluation / result rule:** Math.sqrt(2.0) is 1.4142135623730951, Math.sqrt(-1.0) is NaN, Math.sin(Math.PI/2) is 1.0, Math.log(Math.E) is 1.0, Math.pow(2.0, 10.0) is 1024.0, and Math.abs(-2147483648) is -2147483648.
- **state-transition rule:** All the listed Math methods except random() are mathematical functions: they change no variable and return the same result for the same argument; random() takes no argument and returns a different value on each call.
- **composition rule (with a neighbour):** with method\_call: Every Math facility is used through a method call with the Math. prefix and parentheses (the constants Math.PI and Math.E are written without parentheses).
- **composition rule (with a neighbour):** with shuffle: In the shuffle, r = i + (int) (Math.random() \* (N-i)) scales Math.random() to a uniformly random position between i and N-1, so each remaining card is equally likely.
- **composition rule (with a neighbour):** with standard\_audio: Each sample a[i] = Math.sin(2\*Math.PI \* i \* hz / sps) is taken at evenly spaced times; the 2\*Math.PI factor is needed because Math.sin works in radians, one cycle being 2 pi.
- **composition rule (with a neighbour):** with math\_random: Math.random() is the one Math method that takes no argument and is not a mathematical function: it returns a random double in [0, 1).
- **composition rule (with a neighbour):** with math\_round: Math.round is the Math method that rounds to the nearest integer, but it returns a long, so storing it in an int needs a cast.
- **composition rule (with a neighbour):** with trig\_functions: The trigonometric functions are Math methods whose angles are in radians; Math.toRadians and Math.toDegrees convert.
- **composition rule (with a neighbour):** with random\_move: The random move draws r = Math.random() once per move and compares it with growing cumulative sums of row p[page] to find which interval contains it.
- **plan / role rule:** Used as a black box for standard numeric computations so that a program reads like the formula, e.g. Quadratic computes double d = Math.sqrt(discriminant);.
- **conservation rule:** Replacing Math.pow(x, 2) by x \* x keeps the value (up to rounding) and is cheaper; replacing Math.round(x) by (int) x changes results whenever the fractional part is at least .5 (and for negatives); replacing Math.sin(x)/Math.cos(x) by Math.tan(x) keeps the value.
- **error rule:** rule broken: Library methods are called with the class name, e.g. Math.sqrt(x). (compile-time)
- **error rule:** rule broken: Each argument must have the type the method's API lists. (compile-time)
- **error rule:** rule broken: Math.sqrt and Math.log are undefined for negative arguments and return NaN. (silent logic error)
- **applicability rule:** Use Math for standard functions (roots, logs, trig, extremes, rounding, randomness); for squaring or small known integer powers multiply instead of calling Math.pow, and write known powers of ten as literals such as 1e6.

## The whole prerequisite chain

- **Everything it builds on (8):** `arithmetic_operators`, `data_type`, `expression`, `identifier`, `literal`, `method_call`, `primitive_type`, `variable`
- **Everything that builds on it (11):** `frequency_counting`, `math_random`, `math_round`, `monte_carlo_simulation`, `random_move`, `sampling_without_replacement`, `shuffle`, `simulation_loop`, `standard_audio`, `trig_functions`, `two_models`
