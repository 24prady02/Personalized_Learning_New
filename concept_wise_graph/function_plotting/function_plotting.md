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

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 16 edges around this concept. The edge logic, the wrong and right rules and the exact rules of the ways are copied word for word from the graph.

## To work on (1)

- no aliases: a student's words cannot name this concept

## What it needs first (3)

A prerequisite edge means the other concept has to be understood before `function_plotting`.

### `array_traversal` comes before `function_plotting`

*walking the array with an index loop*

- **Edge:** `pre:array_traversal->function_plotting`
- **Exact edge logic:** The sample points are kept in arrays and traversed.
- **Grounding:** book\_passage
- **Composition rule (R) of `function_plotting` with `array_traversal`:** The arrays have N+1 elements (indices 0..N). The drawing loop starts at i = 1 so that x[i-1] stays in bounds; starting at 0 would access x[-1].
- **Composition rule (R) of `array_traversal` with `function_plotting`:** Sample points are computed into x[] and y[] by one traversal and drawn by another.

### `coordinate_scaling` comes before `function_plotting`

*StdDraw's unit square and setXscale/setYscale*

- **Edge:** `pre:coordinate_scaling->function_plotting`
- **Exact edge logic:** Before plotting, the x-scale is set to the interval and the y-scale to the range of function values so the curve fits the canvas.
- **Grounding:** book\_passage
- **Composition rule (R) of `function_plotting` with `coordinate_scaling`:** The x-scale must match the sampled interval and the y-scale the function's range; otherwise the curve is clipped or squashed.
- **Composition rule (R) of `coordinate_scaling` with `function_plotting`:** Before plotting, set the x-scale to the sampled interval and the y-scale to the function's min and max, so the curve fits the canvas.

### `standard_drawing` comes before `function_plotting`

*StdDraw -- graphical output (book-specific)*

- **Edge:** `pre:standard_drawing->function_plotting`
- **Exact edge logic:** A function is plotted by drawing its sampled points and lines with StdDraw.
- **Grounding:** book\_passage

## What it leads to (1)

These concepts need `function_plotting` first.

### `function_plotting` comes before `standard_audio`

*StdAudio: sound as an array of samples*

- **Edge:** `pre:function_plotting->standard_audio`
- **Exact edge logic:** A sound wave is sampled at regular intervals exactly as a function is sampled for plotting, giving the array of samples that StdAudio plays.
- **Grounding:** book\_passage
- **Composition rule (R) of `function_plotting` with `standard_audio`:** A sound wave is sampled at regular intervals in exactly the way a function is sampled for plotting. The same array can be drawn or played.
- **Composition rule (R) of `standard_audio` with `function_plotting`:** Sampling for sound is the same as sampling for a plot. The same array can be sent to StdDraw and to StdAudio.

## Learned alongside (0)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

No parallel edge touches this concept.

## Misconceptions (1)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### PlotIsExactCurve

- **Edge:** `function_plotting` &rarr; `PlotIsExactCurve` (misconception)
- **Exact edge logic (the wrong rule):** The drawn plot is the exact curve.
- **Twin logic (the right rule):** It is a piecewise linear approximation through the sampled points.
- **Wrong belief (on the node):** The drawn plot is the exact curve.
- **Correct rule (on the node):** It is a piecewise linear approximation through the sampled points.
- **Provenance:** derived
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [1] misconception, exact rule:** wrong rule: The drawn plot is the exact curve. Right rule: The plot is a piecewise linear approximation through the sampled points. With too few samples it can miss major fluctuations.
- **L0 way [2] inconsistent\_trace, exact rule:** Points to LT (fill x[], fill y[], set the scales, then draw segment i from point i-1 to point i). An uneven trace pairs x[i] with y[i-1], or draws before setting the scale. (here mixing in: "The drawn plot is the exact curve")

## Errors (0)

An error edge states the rule that gets broken in a program, and the right rule.

The graph has no error edge from this concept.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for function plotting: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to function plotting agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

- **Edge:** `function_plotting` &rarr; `function_plotting@L0` (has_level)
- **Exact edge logic:** function plotting -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (3 ways).

Ways (3), each with its exact rule:

- **[0] everyday\_reading** (rule type E, folk-meaning rule): The everyday 'graph of a function' is an exact, smooth curve. A program can only evaluate the function at finitely many sampled points and join them with straight segments.
- **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `PlotIsExactCurve`: wrong rule: The drawn plot is the exact curve. Right rule: The plot is a piecewise linear approximation through the sampled points. With too few samples it can miss major fluctuations.
- **[2] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `PlotIsExactCurve`: Points to LT (fill x[], fill y[], set the scales, then draw segment i from point i-1 to point i). An uneven trace pairs x[i] with y[i-1], or draws before setting the scale. (here mixing in: "The drawn plot is the exact curve")

### L1: Unistructural / atom x text surface

L1 for function plotting: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

- **Edge:** `function_plotting` &rarr; `function_plotting@L1` (has_level)
- **Exact edge logic:** function plotting -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

Ways (2), each with its exact rule:

- **[0] names\_the\_element** (rule type N, identity rule): Function plotting is a sampling technique: evaluate f at evenly spaced x-values, store the values in arrays, set the scales, and connect consecutive points with lines.
- **[1] states\_the\_rule** (rule type S, declarative rule): Sample the function by choosing x-values and evaluating f at each one. Connecting successive points with lines gives a piecewise linear approximation.

### L2: Multistructural / block x execution / preoperational

L2 for function plotting: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

- **Edge:** `function_plotting` &rarr; `function_plotting@L2` (has_level)
- **Exact edge logic:** function plotting -&gt; L2 (Multistructural): the answer applies the rules of function plotting to every part of the code, in order (3 ways).

Ways (3), each with its exact rule:

- **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): 1) x[i] = Math.PI \* i / N for i = 0..N. 2) y[i] = f(x[i]). 3) setXscale and setYscale. 4) For i = 1..N, line(x[i-1], y[i-1], x[i], y[i]).
- **[1] output\_prediction** (rule type OP, evaluation / result rule): The plot is N line segments through N+1 sample points. With N = 20 the curve is jagged and misses wiggles; with N = 200 it looks smooth.
- **[2] one\_step\_execution** (rule type OS, state-transition rule): One drawing iteration draws one segment between consecutive samples i-1 and i. It changes no array values.

### L3: Relational / relations x function (concrete operational begins)

L3 for function plotting: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

- **Edge:** `function_plotting` &rarr; `function_plotting@L3` (has_level)
- **Exact edge logic:** function plotting -&gt; L3 (Relational): the answer relates the parts (4 ways).

Ways (4), each with its exact rule:

- **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): The arrays have N+1 elements (indices 0..N). The drawing loop starts at i = 1 so that x[i-1] stays in bounds; starting at 0 would access x[-1].
- **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): A sound wave is sampled at regular intervals in exactly the way a function is sampled for plotting. The same array can be drawn or played.
- **[2] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): The x-scale must match the sampled interval and the y-scale the function's range; otherwise the curve is clipped or squashed.
- **[3] purpose\_of\_the\_whole** (rule type P, plan / role rule): Plan: sample, then connect (a prototypical sampling computation). The arrays are containers of samples and i is a stepper.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for function plotting: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

- **Edge:** `function_plotting` &rarr; `function_plotting@L4` (has_level)
- **Exact edge logic:** function plotting -&gt; L4 (Extended abstract): the answer reasons beyond the given code (5 ways).

Ways (5), each with its exact rule:

- **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `PlotIsExactCurve`: Increasing N makes the curve smoother and keeps the end points, but costs time. Decreasing N keeps the sampled points but can lose features between them.
- **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Use sampled plotting to see the shape of a function or data series. For exact values, print them. For smooth curves with few points, the book later uses a different method (Section 2.4).
- **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: Array indices must stay in 0..N. Kind: run-time exception. Trigger class: The drawing loop starts at i = 0 (so x[i-1] is x[-1]) or runs to i &lt;= N+1: ArrayIndexOutOfBoundsException.
- **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: The sample must be dense enough for the function. Kind: silent logic error. Trigger class: N is too small for a rapidly oscillating f, so the plot misses major fluctuations.
- **[4] diagnose\_an\_error** (rule type D, error rule): rule broken: The y-scale must cover the function's range. Kind: silent logic error. Trigger class: The default unit square, or a wrong y-range, cuts off the negative part of sin(4x) + sin(20x).

## Same topic

`function_plotting` belongs to the topic **Standard drawing and animation** (`topic1.5.e`). The topic also contains: `animation`, `coordinate_scaling`, `drawing_shapes`, `mouse_interaction`, `standard_drawing`.

## Rules of the concept (17)

- **Book** (SW-1e, p. 140 (pdf 150)): "Plotting the function by connecting successive points with lines produces what is known as a piecewise linear approximation."
- **Book** (SW-1.5, p. 140 (pdf 150)): "Plotting the function by connecting successive points with lines produces what is known as a piecewise linear approximation."
- **E** (folk-meaning rule): The everyday 'graph of a function' is an exact, smooth curve. A program can only evaluate the function at finitely many sampled points and join them with straight segments.
- **M** (wrong rule / right rule): PlotIsExactCurve: wrong: The drawn plot is the exact curve. \| right: The plot is a piecewise linear approximation through the sampled points. With too few samples it can miss major fluctuations.
- **T** (uneven-application rule): Points to LT (fill x[], fill y[], set the scales, then draw segment i from point i-1 to point i). An uneven trace pairs x[i] with y[i-1], or draws before setting the scale.
- **N** (identity rule): Function plotting is a sampling technique: evaluate f at evenly spaced x-values, store the values in arrays, set the scales, and connect consecutive points with lines.
- **S** (declarative rule): Sample the function by choosing x-values and evaluating f at each one. Connecting successive points with lines gives a piecewise linear approximation.
- **LT** (operational sequencing rule): 1) x[i] = Math.PI \* i / N for i = 0..N. 2) y[i] = f(x[i]). 3) setXscale and setYscale. 4) For i = 1..N, line(x[i-1], y[i-1], x[i], y[i]).
- **OP** (evaluation / result rule): The plot is N line segments through N+1 sample points. With N = 20 the curve is jagged and misses wiggles; with N = 200 it looks smooth.
- **OS** (state-transition rule): One drawing iteration draws one segment between consecutive samples i-1 and i. It changes no array values.
- **R** (composition rule (with a neighbour)): with array\_traversal: The arrays have N+1 elements (indices 0..N). The drawing loop starts at i = 1 so that x[i-1] stays in bounds; starting at 0 would access x[-1].
- **R** (composition rule (with a neighbour)): with standard\_audio: A sound wave is sampled at regular intervals in exactly the way a function is sampled for plotting. The same array can be drawn or played.
- **R** (composition rule (with a neighbour)): with coordinate\_scaling: The x-scale must match the sampled interval and the y-scale the function's range; otherwise the curve is clipped or squashed.
- **P** (plan / role rule): Plan: sample, then connect (a prototypical sampling computation). The arrays are containers of samples and i is a stepper.
- **C** (conservation rule): Increasing N makes the curve smoother and keeps the end points, but costs time. Decreasing N keeps the sampled points but can lose features between them.
- **D** (error rule): rule broken: Array indices must stay in 0..N. (run-time exception)
- **D** (error rule): rule broken: The sample must be dense enough for the function. (silent logic error)
- **D** (error rule): rule broken: The y-scale must cover the function's range. (silent logic error)
- **X** (applicability rule): Use sampled plotting to see the shape of a function or data series. For exact values, print them. For smooth curves with few points, the book later uses a different method (Section 2.4).

## How it is found in code and answers (reader block)

- **Aliases:** none
- **Code patterns:** `StdDraw\.line\s*\([^;]*\[\s*\w+\s*-\s*1\s*\]`, `StdDraw\.(?:line|point)\s*\([^;]*Math\.(?:sin|cos)`, `\w\s*\[[^\]]+\]\s*=\s*[^;]*Math\.(?:sin|cos|exp|log|sqrt|pow)`
- **Operator symbols:** none
- **Java types:** none

## The whole prerequisite chain

- **Everything it builds on (27):** `api`, `arithmetic_operators`, `array_creation`, `array_declaration`, `array_initializer`, `array_traversal`, `boolean`, `boolean_expression`, `comparison_operators`, `coordinate_scaling`, `data_structure`, `data_type`, `do_while_loop`, `expression`, `for_loop`, `identifier`, `indexing`, `length_field`, `literal`, `logical_operators`, `loop_control`, `loop_variable`, `method_call`, `primitive_type`, `standard_drawing`, `variable`, `while_loop`
- **Everything that builds on it (1):** `standard_audio`

## Every edge in this view and its exact edge logic (16)

All the edges drawn in the picture, in the order: prerequisite, parallel, misconception, error, has_level, contains.

**1. `array_traversal` &rarr; `function_plotting`** (prerequisite)

- **Exact edge logic:** The sample points are kept in arrays and traversed.
- **Grounding:** book\_passage
- **Composition rule (R) of `array_traversal` with `function_plotting`:** Sample points are computed into x[] and y[] by one traversal and drawn by another.
- **Composition rule (R) of `function_plotting` with `array_traversal`:** The arrays have N+1 elements (indices 0..N). The drawing loop starts at i = 1 so that x[i-1] stays in bounds; starting at 0 would access x[-1].

**2. `coordinate_scaling` &rarr; `function_plotting`** (prerequisite)

- **Exact edge logic:** Before plotting, the x-scale is set to the interval and the y-scale to the range of function values so the curve fits the canvas.
- **Grounding:** book\_passage
- **Composition rule (R) of `coordinate_scaling` with `function_plotting`:** Before plotting, set the x-scale to the sampled interval and the y-scale to the function's min and max, so the curve fits the canvas.
- **Composition rule (R) of `function_plotting` with `coordinate_scaling`:** The x-scale must match the sampled interval and the y-scale the function's range; otherwise the curve is clipped or squashed.

**3. `function_plotting` &rarr; `standard_audio`** (prerequisite)

- **Exact edge logic:** A sound wave is sampled at regular intervals exactly as a function is sampled for plotting, giving the array of samples that StdAudio plays.
- **Grounding:** book\_passage
- **Composition rule (R) of `function_plotting` with `standard_audio`:** A sound wave is sampled at regular intervals in exactly the way a function is sampled for plotting. The same array can be drawn or played.
- **Composition rule (R) of `standard_audio` with `function_plotting`:** Sampling for sound is the same as sampling for a plot. The same array can be sent to StdDraw and to StdAudio.

**4. `standard_drawing` &rarr; `function_plotting`** (prerequisite)

- **Exact edge logic:** A function is plotted by drawing its sampled points and lines with StdDraw.
- **Grounding:** book\_passage

**5. `function_plotting` &rarr; `PlotIsExactCurve`** (misconception)

- **Exact edge logic (the wrong rule):** The drawn plot is the exact curve.
- **Twin logic (the right rule):** It is a piecewise linear approximation through the sampled points.
- **Role:** primary

**6. `function_plotting` &rarr; `function_plotting@L0`** (has_level)

- **Exact edge logic:** function plotting -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (3 ways).
  - **[0] everyday\_reading** (rule type E, folk-meaning rule): The everyday 'graph of a function' is an exact, smooth curve. A program can only evaluate the function at finitely many sampled points and join them with straight segments.
  - **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `PlotIsExactCurve`: wrong rule: The drawn plot is the exact curve. Right rule: The plot is a piecewise linear approximation through the sampled points. With too few samples it can miss major fluctuations.
  - **[2] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `PlotIsExactCurve`: Points to LT (fill x[], fill y[], set the scales, then draw segment i from point i-1 to point i). An uneven trace pairs x[i] with y[i-1], or draws before setting the scale. (here mixing in: "The drawn plot is the exact curve")

**7. `function_plotting` &rarr; `function_plotting@L1`** (has_level)

- **Exact edge logic:** function plotting -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).
  - **[0] names\_the\_element** (rule type N, identity rule): Function plotting is a sampling technique: evaluate f at evenly spaced x-values, store the values in arrays, set the scales, and connect consecutive points with lines.
  - **[1] states\_the\_rule** (rule type S, declarative rule): Sample the function by choosing x-values and evaluating f at each one. Connecting successive points with lines gives a piecewise linear approximation.

**8. `function_plotting` &rarr; `function_plotting@L2`** (has_level)

- **Exact edge logic:** function plotting -&gt; L2 (Multistructural): the answer applies the rules of function plotting to every part of the code, in order (3 ways).
  - **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): 1) x[i] = Math.PI \* i / N for i = 0..N. 2) y[i] = f(x[i]). 3) setXscale and setYscale. 4) For i = 1..N, line(x[i-1], y[i-1], x[i], y[i]).
  - **[1] output\_prediction** (rule type OP, evaluation / result rule): The plot is N line segments through N+1 sample points. With N = 20 the curve is jagged and misses wiggles; with N = 200 it looks smooth.
  - **[2] one\_step\_execution** (rule type OS, state-transition rule): One drawing iteration draws one segment between consecutive samples i-1 and i. It changes no array values.

**9. `function_plotting` &rarr; `function_plotting@L3`** (has_level)

- **Exact edge logic:** function plotting -&gt; L3 (Relational): the answer relates the parts (4 ways).
  - **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): The arrays have N+1 elements (indices 0..N). The drawing loop starts at i = 1 so that x[i-1] stays in bounds; starting at 0 would access x[-1].
  - **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): A sound wave is sampled at regular intervals in exactly the way a function is sampled for plotting. The same array can be drawn or played.
  - **[2] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): The x-scale must match the sampled interval and the y-scale the function's range; otherwise the curve is clipped or squashed.
  - **[3] purpose\_of\_the\_whole** (rule type P, plan / role rule): Plan: sample, then connect (a prototypical sampling computation). The arrays are containers of samples and i is a stepper.

**10. `function_plotting` &rarr; `function_plotting@L4`** (has_level)

- **Exact edge logic:** function plotting -&gt; L4 (Extended abstract): the answer reasons beyond the given code (5 ways).
  - **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `PlotIsExactCurve`: Increasing N makes the curve smoother and keeps the end points, but costs time. Decreasing N keeps the sampled points but can lose features between them.
  - **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Use sampled plotting to see the shape of a function or data series. For exact values, print them. For smooth curves with few points, the book later uses a different method (Section 2.4).
  - **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: Array indices must stay in 0..N. Kind: run-time exception. Trigger class: The drawing loop starts at i = 0 (so x[i-1] is x[-1]) or runs to i &lt;= N+1: ArrayIndexOutOfBoundsException.
  - **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: The sample must be dense enough for the function. Kind: silent logic error. Trigger class: N is too small for a rapidly oscillating f, so the plot misses major fluctuations.
  - **[4] diagnose\_an\_error** (rule type D, error rule): rule broken: The y-scale must cover the function's range. Kind: silent logic error. Trigger class: The default unit square, or a wrong y-range, cuts off the negative part of sin(4x) + sin(20x).

**11. `topic1.5.e` &rarr; `function_plotting`** (contains)

- topic `topic1.5.e` contains `function_plotting`

**12. `topic1.5.e` &rarr; `animation`** (contains)

- topic `topic1.5.e` contains `animation`

**13. `topic1.5.e` &rarr; `coordinate_scaling`** (contains)

- topic `topic1.5.e` contains `coordinate_scaling`

**14. `topic1.5.e` &rarr; `drawing_shapes`** (contains)

- topic `topic1.5.e` contains `drawing_shapes`

**15. `topic1.5.e` &rarr; `mouse_interaction`** (contains)

- topic `topic1.5.e` contains `mouse_interaction`

**16. `topic1.5.e` &rarr; `standard_drawing`** (contains)

- topic `topic1.5.e` contains `standard_drawing`
