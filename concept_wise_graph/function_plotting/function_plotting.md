# function_plotting (`function_plotting`)

sampling a function and joining the points with lines

Section 1.5 Input and Output, topic 1.5.e Standard drawing and animation.

![The knowledge graph around function_plotting](function_plotting.png)

## At a glance

- **Needs first:** `array_traversal`, `coordinate_scaling`, `standard_drawing`
- **Leads to:** `standard_audio`
- **Learned alongside:** nothing
- **Misconceptions:** `PlotIsExactCurve`
- **Errors:** none
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 16 edges around this concept, each explained in the graph's own words.

## What it needs first (3)

A prerequisite edge means the other concept has to be understood before `function_plotting`.

### `array_traversal` comes before `function_plotting`

*walking the array with an index loop*

The sample points are kept in arrays and traversed.

- **Grounding:** book passage
- **How `function_plotting` combines with `array_traversal`:** The arrays have N+1 elements (indices 0..N). The drawing loop starts at i = 1 so that x[i-1] stays in bounds; starting at 0 would access x[-1].
- **How `array_traversal` combines with `function_plotting`:** Sample points are computed into x[] and y[] by one traversal and drawn by another.

### `coordinate_scaling` comes before `function_plotting`

*StdDraw's unit square and setXscale/setYscale*

Before plotting, the x-scale is set to the interval and the y-scale to the range of function values so the curve fits the canvas.

- **Grounding:** book passage
- **How `function_plotting` combines with `coordinate_scaling`:** The x-scale must match the sampled interval and the y-scale the function's range; otherwise the curve is clipped or squashed.
- **How `coordinate_scaling` combines with `function_plotting`:** Before plotting, set the x-scale to the sampled interval and the y-scale to the function's min and max, so the curve fits the canvas.

### `standard_drawing` comes before `function_plotting`

*StdDraw -- graphical output (book-specific)*

A function is plotted by drawing its sampled points and lines with StdDraw.

- **Grounding:** book passage

## What it leads to (1)

These concepts need `function_plotting` first.

### `function_plotting` comes before `standard_audio`

*StdAudio: sound as an array of samples*

A sound wave is sampled at regular intervals exactly as a function is sampled for plotting, giving the array of samples that StdAudio plays.

- **Grounding:** book passage
- **How `function_plotting` combines with `standard_audio`:** A sound wave is sampled at regular intervals in exactly the way a function is sampled for plotting. The same array can be drawn or played.
- **How `standard_audio` combines with `function_plotting`:** Sampling for sound is the same as sampling for a plot. The same array can be sent to StdDraw and to StdAudio.

## Learned alongside (0)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

No parallel edge touches this concept.

## Misconceptions (1)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### PlotIsExactCurve

- **Wrong rule:** The drawn plot is the exact curve.
- **Right rule:** It is a piecewise linear approximation through the sampled points.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: The drawn plot is the exact curve. Right rule: The plot is a piecewise linear approximation through the sampled points. With too few samples it can miss major fluctuations.
- **Shows at level L0 as:** inconsistent trace: Points to LT (fill x[], fill y[], set the scales, then draw segment i from point i-1 to point i). An uneven trace pairs x[i] with y[i-1], or draws before setting the scale. (here mixing in: "The drawn plot is the exact curve")

## Errors (0)

An error edge states the rule that gets broken in a program, and the right rule.

The graph has no error edge from this concept.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for function plotting: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to function plotting agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

function plotting -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (3 ways).

- **everyday reading** (folk-meaning rule): The everyday 'graph of a function' is an exact, smooth curve. A program can only evaluate the function at finitely many sampled points and join them with straight segments.
- **misconception** (wrong rule / right rule; shows `PlotIsExactCurve`): wrong rule: The drawn plot is the exact curve. Right rule: The plot is a piecewise linear approximation through the sampled points. With too few samples it can miss major fluctuations.
- **inconsistent trace** (uneven-application rule; shows `PlotIsExactCurve`): Points to LT (fill x[], fill y[], set the scales, then draw segment i from point i-1 to point i). An uneven trace pairs x[i] with y[i-1], or draws before setting the scale. (here mixing in: "The drawn plot is the exact curve")

### L1: Unistructural / atom x text surface

L1 for function plotting: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

function plotting -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

- **names the element** (identity rule): Function plotting is a sampling technique: evaluate f at evenly spaced x-values, store the values in arrays, set the scales, and connect consecutive points with lines.
- **states the rule** (declarative rule): Sample the function by choosing x-values and evaluating f at each one. Connecting successive points with lines gives a piecewise linear approximation.

### L2: Multistructural / block x execution / preoperational

L2 for function plotting: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

function plotting -&gt; L2 (Multistructural): the answer applies the rules of function plotting to every part of the code, in order (3 ways).

- **line by line trace** (operational sequencing rule): 1) x[i] = Math.PI \* i / N for i = 0..N. 2) y[i] = f(x[i]). 3) setXscale and setYscale. 4) For i = 1..N, line(x[i-1], y[i-1], x[i], y[i]).
- **output prediction** (evaluation / result rule): The plot is N line segments through N+1 sample points. With N = 20 the curve is jagged and misses wiggles; with N = 200 it looks smooth.
- **one step execution** (state-transition rule): One drawing iteration draws one segment between consecutive samples i-1 and i. It changes no array values.

### L3: Relational / relations x function (concrete operational begins)

L3 for function plotting: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

function plotting -&gt; L3 (Relational): the answer relates the parts (4 ways).

- **relation to neighbour** (composition rule (with a neighbour)): The arrays have N+1 elements (indices 0..N). The drawing loop starts at i = 1 so that x[i-1] stays in bounds; starting at 0 would access x[-1].
- **relation to neighbour** (composition rule (with a neighbour)): A sound wave is sampled at regular intervals in exactly the way a function is sampled for plotting. The same array can be drawn or played.
- **relation to neighbour** (composition rule (with a neighbour)): The x-scale must match the sampled interval and the y-scale the function's range; otherwise the curve is clipped or squashed.
- **purpose of the whole** (plan / role rule): Plan: sample, then connect (a prototypical sampling computation). The arrays are containers of samples and i is a stepper.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for function plotting: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

function plotting -&gt; L4 (Extended abstract): the answer reasons beyond the given code (5 ways).

- **predict a change** (conservation rule; shows `PlotIsExactCurve`): Increasing N makes the curve smoother and keeps the end points, but costs time. Decreasing N keeps the sampled points but can lose features between them.
- **transfer to a new program** (applicability rule): Use sampled plotting to see the shape of a function or data series. For exact values, print them. For smooth curves with few points, the book later uses a different method (Section 2.4).
- **diagnose an error** (error rule): rule broken: Array indices must stay in 0..N. Kind: run-time exception. Trigger class: The drawing loop starts at i = 0 (so x[i-1] is x[-1]) or runs to i &lt;= N+1: ArrayIndexOutOfBoundsException.
- **diagnose an error** (error rule): rule broken: The sample must be dense enough for the function. Kind: silent logic error. Trigger class: N is too small for a rapidly oscillating f, so the plot misses major fluctuations.
- **diagnose an error** (error rule): rule broken: The y-scale must cover the function's range. Kind: silent logic error. Trigger class: The default unit square, or a wrong y-range, cuts off the negative part of sin(4x) + sin(20x).

## Same topic

`function_plotting` belongs to the topic **Standard drawing and animation** (`topic1.5.e`). The topic also contains: `animation`, `coordinate_scaling`, `drawing_shapes`, `mouse_interaction`, `standard_drawing`.

## Rules of the concept (17)

- **folk-meaning rule:** The everyday 'graph of a function' is an exact, smooth curve. A program can only evaluate the function at finitely many sampled points and join them with straight segments.
- **wrong rule / right rule:** PlotIsExactCurve: wrong: The drawn plot is the exact curve. \| right: The plot is a piecewise linear approximation through the sampled points. With too few samples it can miss major fluctuations.
- **uneven-application rule:** Points to LT (fill x[], fill y[], set the scales, then draw segment i from point i-1 to point i). An uneven trace pairs x[i] with y[i-1], or draws before setting the scale.
- **identity rule:** Function plotting is a sampling technique: evaluate f at evenly spaced x-values, store the values in arrays, set the scales, and connect consecutive points with lines.
- **declarative rule:** Sample the function by choosing x-values and evaluating f at each one. Connecting successive points with lines gives a piecewise linear approximation.
- **operational sequencing rule:** 1) x[i] = Math.PI \* i / N for i = 0..N. 2) y[i] = f(x[i]). 3) setXscale and setYscale. 4) For i = 1..N, line(x[i-1], y[i-1], x[i], y[i]).
- **evaluation / result rule:** The plot is N line segments through N+1 sample points. With N = 20 the curve is jagged and misses wiggles; with N = 200 it looks smooth.
- **state-transition rule:** One drawing iteration draws one segment between consecutive samples i-1 and i. It changes no array values.
- **composition rule (with a neighbour):** with array\_traversal: The arrays have N+1 elements (indices 0..N). The drawing loop starts at i = 1 so that x[i-1] stays in bounds; starting at 0 would access x[-1].
- **composition rule (with a neighbour):** with standard\_audio: A sound wave is sampled at regular intervals in exactly the way a function is sampled for plotting. The same array can be drawn or played.
- **composition rule (with a neighbour):** with coordinate\_scaling: The x-scale must match the sampled interval and the y-scale the function's range; otherwise the curve is clipped or squashed.
- **plan / role rule:** Plan: sample, then connect (a prototypical sampling computation). The arrays are containers of samples and i is a stepper.
- **conservation rule:** Increasing N makes the curve smoother and keeps the end points, but costs time. Decreasing N keeps the sampled points but can lose features between them.
- **error rule:** rule broken: Array indices must stay in 0..N. (run-time exception)
- **error rule:** rule broken: The sample must be dense enough for the function. (silent logic error)
- **error rule:** rule broken: The y-scale must cover the function's range. (silent logic error)
- **applicability rule:** Use sampled plotting to see the shape of a function or data series. For exact values, print them. For smooth curves with few points, the book later uses a different method (Section 2.4).

## The whole prerequisite chain

- **Everything it builds on (27):** `api`, `arithmetic_operators`, `array_creation`, `array_declaration`, `array_initializer`, `array_traversal`, `boolean`, `boolean_expression`, `comparison_operators`, `coordinate_scaling`, `data_structure`, `data_type`, `do_while_loop`, `expression`, `for_loop`, `identifier`, `indexing`, `length_field`, `literal`, `logical_operators`, `loop_control`, `loop_variable`, `method_call`, `primitive_type`, `standard_drawing`, `variable`, `while_loop`
- **Everything that builds on it (1):** `standard_audio`
