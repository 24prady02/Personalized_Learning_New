# standard_drawing (`standard_drawing`)

StdDraw -- graphical output (book-specific)

Section 1.5 Input and Output, topic 1.5.e Standard drawing and animation.

![The knowledge graph around standard_drawing](standard_drawing.png)

## At a glance

- **Needs first:** `api`
- **Leads to:** `animation`, `coordinate_scaling`, `drawing_shapes`, `function_plotting`, `mouse_interaction`
- **Learned alongside:** `standard_input`, `standard_output`
- **Misconceptions:** `DrawWithoutShow`, `PixelCoordinates`
- **Errors:** `StdLibraryNotInDirectory`
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 26 edges around this concept. The edge logic, the wrong and right rules and the exact rules of the ways are copied word for word from the graph.

## To work on (0)

Nothing is missing for this concept.

## What it needs first (1)

A prerequisite edge means the other concept has to be understood before `standard_drawing`.

### `api` comes before `standard_drawing`

*Application programming interface (API): a table of library methods giving each method's signature and a short description of what it computes*

- **Edge:** `pre:api->standard_drawing`
- **Exact edge logic:** StdDraw is a library used through its API of static methods.
- **Grounding:** book\_passage

## What it leads to (5)

These concepts need `standard_drawing` first.

### `standard_drawing` comes before `animation`

*StdDraw animation: clear, draw, show, pause in a loop*

- **Edge:** `pre:standard_drawing->animation`
- **Exact edge logic:** Animation uses StdDraw's clear() and show() methods to make dynamic changes to the image on the screen.
- **Grounding:** book\_passage
- **Composition rule (R) of `standard_drawing` with `animation`:** Animation reuses StdDraw's drawing commands but adds clear() and show(t), which control when the canvas is erased and displayed.
- **Composition rule (R) of `animation` with `standard_drawing`:** Animation uses StdDraw's drawing commands plus clear() and show(t). show(t) switches off the default show-after-every-command.

### `standard_drawing` comes before `coordinate_scaling`

*StdDraw's unit square and setXscale/setYscale*

- **Edge:** `pre:standard_drawing->coordinate_scaling`
- **Exact edge logic:** Scaling sets the coordinate system StdDraw uses.
- **Grounding:** book\_passage
- **Composition rule (R) of `standard_drawing` with `coordinate_scaling`:** setXscale and setYscale set the coordinate system that every later StdDraw command uses.
- **Composition rule (R) of `coordinate_scaling` with `standard_drawing`:** The scale fixes how every later StdDraw coordinate is interpreted. The pen radius is unaffected by it.

### `standard_drawing` comes before `drawing_shapes`

*outline vs filled shapes, square half-length, colour and text*

- **Edge:** `pre:standard_drawing->drawing_shapes`
- **Exact edge logic:** Shape commands are StdDraw drawing commands.
- **Grounding:** book\_passage
- **Composition rule (R) of `standard_drawing` with `drawing_shapes`:** Shape commands are StdDraw drawing commands. They use the same coordinates, pen color and pen radius as line and point.
- **Composition rule (R) of `drawing_shapes` with `standard_drawing`:** Shapes use StdDraw's current coordinate scale, pen radius and color, and paint over earlier marks.

### `standard_drawing` comes before `function_plotting`

*sampling a function and joining the points with lines*

- **Edge:** `pre:standard_drawing->function_plotting`
- **Exact edge logic:** A function is plotted by drawing its sampled points and lines with StdDraw.
- **Grounding:** book\_passage

### `standard_drawing` comes before `mouse_interaction`

*reading mouse position and clicks from StdDraw*

- **Edge:** `pre:standard_drawing->mouse_interaction`
- **Exact edge logic:** Mouse position and clicks are read through StdDraw methods such as StdDraw.mousePressed().
- **Grounding:** order\_only

## Learned alongside (2)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

### `standard_drawing` alongside `standard_input`

*StdIn -- reading a stream of values*

- **Edge:** `par:standard_input~standard_drawing`
- **Exact edge logic:** Like StdIn, StdDraw is a library downloaded from the booksite; StdIn brings values into the program, while StdDraw produces drawings as output.
- **Grounding:** book\_passage
- **Composition rule (R) of `standard_drawing` with `standard_input`:** StdIn values can be drawn directly: PlotFilter reads the bounding box, then point coordinates, and calls StdDraw.point for each pair. Both libraries must be downloaded into the program's directory.
- **Composition rule (R) of `standard_input` with `standard_drawing`:** StdIn values can drive StdDraw output. PlotFilter reads x, y pairs and draws a point for each, after scaling from the first four numbers.

### `standard_drawing` alongside `standard_output`

*StdOut / System.out*

- **Edge:** `par:standard_output~standard_drawing`
- **Exact edge logic:** StdOut writes text to the output stream; StdDraw draws shapes at (x, y) coordinates in a window.
- **Grounding:** book\_passage
- **Composition rule (R) of `standard_drawing` with `standard_output`:** StdOut writes text to a stream, while StdDraw draws in a separate window at (x, y) coordinates. Neither affects the other.
- **Composition rule (R) of `standard_output` with `standard_drawing`:** StdOut text and StdDraw pictures are independent outputs: printing does not draw, and drawing does not print.

## Misconceptions (2)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### DrawWithoutShow

- **Edge:** `standard_drawing` &rarr; `DrawWithoutShow` (misconception)
- **Exact edge logic (the wrong rule):** With double buffering on, each drawing command appears on screen immediately.
- **Twin logic (the right rule):** By default each drawing command appears at once; after StdDraw.show(t) turns animation mode on, drawing is collected and appears only at the next show(t), which then pauses t milliseconds; show() with no argument turns per-command display back on.
- **Wrong belief (on the node):** With double buffering on, each drawing command appears on screen immediately.
- **Correct rule (on the node):** By default each drawing command appears at once; after StdDraw.show(t) turns animation mode on, drawing is collected and appears only at the next show(t), which then pauses t milliseconds; show() with no argument turns per-command display back on.
- **Provenance:** derived
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [3] misconception, exact rule:** wrong rule: With double buffering on, each drawing command appears on screen immediately. Right rule: By default each command is shown at once. After StdDraw.show(t) turns animation mode on, drawing is collected off-screen and appears only at the next show(t). show() with no argument turns per-command display back on. (Newer StdDraw versions use enableDoubleBuffering().)
- **Edge `animation` &rarr; `DrawWithoutShow`, exact edge logic:** With double buffering on, each drawing command appears on screen immediately. **Twin logic:** By default each drawing command appears at once; after StdDraw.show(t) turns animation mode on, drawing is collected and appears only at the next show(t), which then pauses t milliseconds; show() with no argument turns per-command display back on. (role: primary)

### PixelCoordinates

- **Edge:** `standard_drawing` &rarr; `PixelCoordinates` (misconception)
- **Exact edge logic (the wrong rule):** StdDraw.point(256, 256) draws in the middle of the default window.
- **Twin logic (the right rule):** The default coordinate scale is the unit square, so the middle is (0.5, 0.5).
- **Wrong belief (on the node):** StdDraw.point(256, 256) draws in the middle of the default window.
- **Correct rule (on the node):** The default coordinate scale is the unit square, so the middle is (0.5, 0.5).
- **Provenance:** derived
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [1] misconception, exact rule:** wrong rule: StdDraw.point(256, 256) draws in the middle of the default window. Right rule: The default window is 512-by-512 pixels, but coordinates are in the unit square, so the middle is (0.5, 0.5). (256, 256) is far off the canvas.
- **L0 way [2] inconsistent\_trace, exact rule:** Points to LT (commands run in program order; each uses the current scale, color and pen radius; later marks cover earlier ones). An uneven trace uses pixel units for some points, puts y downwards, or applies a setting to commands issued before it. (here mixing in: "StdDraw.point(256, 256) draws in the middle of the default window")
- **Edge `coordinate_scaling` &rarr; `PixelCoordinates`, exact edge logic:** StdDraw.point(256, 256) draws in the middle of the default window. **Twin logic:** The default coordinate scale is the unit square, so the middle is (0.5, 0.5). (role: context)

## Errors (1)

An error edge states the rule that gets broken in a program, and the right rule.

### StdLibraryNotInDirectory

- **Edge:** `standard_drawing` &rarr; `StdLibraryNotInDirectory` (error)
- **Exact edge logic (the wrong rule):** Uses StdIn (or StdDraw/StdAudio) without StdIn.java in the working directory.
- **Twin logic (the right rule):** The Std\* libraries are not built into Java; StdIn.java etc. must be in the same directory (or on the classpath), otherwise Java reports NoClassDefFoundError.
- **Wrong belief (on the node):** Uses StdIn (or StdDraw/StdAudio) without StdIn.java in the working directory.
- **Correct rule (on the node):** The Std\* libraries are not built into Java; StdIn.java etc. must be in the same directory (or on the classpath), otherwise Java reports NoClassDefFoundError.
- **Provenance:** textbook
- **Role of this concept:** context
- **Edge `standard_audio` &rarr; `StdLibraryNotInDirectory`, exact edge logic:** Uses StdIn (or StdDraw/StdAudio) without StdIn.java in the working directory. **Twin logic:** The Std\* libraries are not built into Java; StdIn.java etc. must be in the same directory (or on the classpath), otherwise Java reports NoClassDefFoundError. (role: context)
- **Edge `standard_input` &rarr; `StdLibraryNotInDirectory`, exact edge logic:** Uses StdIn (or StdDraw/StdAudio) without StdIn.java in the working directory. **Twin logic:** The Std\* libraries are not built into Java; StdIn.java etc. must be in the same directory (or on the classpath), otherwise Java reports NoClassDefFoundError. (role: primary)

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for standard drawing: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to standard drawing agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

- **Edge:** `standard_drawing` &rarr; `standard_drawing@L0` (has_level)
- **Exact edge logic:** standard drawing -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (4 ways).

Ways (4), each with its exact rule:

- **[0] everyday\_reading** (rule type E, folk-meaning rule): In geometry a point has no size, and on screens positions are pixels with y pointing down. StdDraw.point(x, y) draws a visible spot (a circle of the pen radius) in user coordinates: the default is the unit square, with (0, 0) at the lower-left corner.
- **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `PixelCoordinates`: wrong rule: StdDraw.point(256, 256) draws in the middle of the default window. Right rule: The default window is 512-by-512 pixels, but coordinates are in the unit square, so the middle is (0.5, 0.5). (256, 256) is far off the canvas.
- **[2] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `PixelCoordinates`: Points to LT (commands run in program order; each uses the current scale, color and pen radius; later marks cover earlier ones). An uneven trace uses pixel units for some points, puts y downwards, or applies a setting to commands issued before it. (here mixing in: "StdDraw.point(256, 256) draws in the middle of the default window")
- **[3] misconception** (rule type M, wrong rule / right rule) &rarr; `DrawWithoutShow`: wrong rule: With double buffering on, each drawing command appears on screen immediately. Right rule: By default each command is shown at once. After StdDraw.show(t) turns animation mode on, drawing is collected off-screen and appears only at the next show(t). show() with no argument turns per-command display back on. (Newer StdDraw versions use enableDoubleBuffering().)

### L1: Unistructural / atom x text surface

L1 for standard drawing: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

- **Edge:** `standard_drawing` &rarr; `standard_drawing@L1` (has_level)
- **Exact edge logic:** standard drawing -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

Ways (2), each with its exact rule:

- **[0] names\_the\_element** (rule type N, identity rule): StdDraw is a booksite library of static methods for graphical output: lines, points, shapes and text drawn on a 2-D canvas in a window.
- **[1] states\_the\_rule** (rule type S, declarative rule): StdDraw models an abstract device that draws lines and points on a two-dimensional canvas. The default scale is the unit square, and methods with no arguments reset to the defaults.

### L2: Multistructural / block x execution / preoperational

L2 for standard drawing: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

- **Edge:** `standard_drawing` &rarr; `standard_drawing@L2` (has_level)
- **Exact edge logic:** standard drawing -&gt; L2 (Multistructural): the answer applies the rules of standard drawing to every part of the code, in order (3 ways).

Ways (3), each with its exact rule:

- **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): Calls run in program order. Each control command (setXscale, setPenRadius, setPenColor) affects only the drawing commands after it, and each drawing command paints over what is already on the canvas.
- **[1] output\_prediction** (rule type OP, evaluation / result rule): The result is a picture in a window, not a value: the methods are void. Triangle's three line() calls and one point() call produce an equilateral triangle with a dot inside.
- **[2] one\_step\_execution** (rule type OS, state-transition rule): One drawing command adds marks to the canvas (shown at once by default). One control command changes the drawing state (scale, pen radius or color) without drawing anything.

### L3: Relational / relations x function (concrete operational begins)

L3 for standard drawing: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

- **Edge:** `standard_drawing` &rarr; `standard_drawing@L3` (has_level)
- **Exact edge logic:** standard drawing -&gt; L3 (Relational): the answer relates the parts (6 ways).

Ways (6), each with its exact rule:

- **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): StdIn values can be drawn directly: PlotFilter reads the bounding box, then point coordinates, and calls StdDraw.point for each pair. Both libraries must be downloaded into the program's directory.
- **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): StdOut writes text to a stream, while StdDraw draws in a separate window at (x, y) coordinates. Neither affects the other.
- **[2] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Animation reuses StdDraw's drawing commands but adds clear() and show(t), which control when the canvas is erased and displayed.
- **[3] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): setXscale and setYscale set the coordinate system that every later StdDraw command uses.
- **[4] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Shape commands are StdDraw drawing commands. They use the same coordinates, pen color and pen radius as line and point.
- **[5] purpose\_of\_the\_whole** (rule type P, plan / role rule): StdDraw is used to visualize data and functions, which is often more meaningful than lists of numbers.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for standard drawing: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

- **Edge:** `standard_drawing` &rarr; `standard_drawing@L4` (has_level)
- **Exact edge logic:** standard drawing -&gt; L4 (Extended abstract): the answer reasons beyond the given code (5 ways).

Ways (5), each with its exact rule:

- **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `PixelCoordinates`: Rescaling the coordinates together with the data keeps the picture. The pen radius is not affected by scaling. Reordering drawing commands changes which mark covers which.
- **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Use StdDraw for simple plots, data visualizations and teaching animations. It is crude compared with production graphics libraries, and exact numeric results belong on standard output.
- **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: StdDraw.java must be in the working directory or on the classpath. Kind: run-time exception. Trigger class: Running without StdDraw.class available: NoClassDefFoundError: StdDraw (javac reports 'cannot find symbol' if it is missing at compile time).
- **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: Coordinates must lie inside the current scale to be visible. Kind: silent logic error. Trigger class: Pixel-style coordinates such as (256, 256) with the default unit square: nothing visible is drawn.
- **[4] diagnose\_an\_error** (rule type D, error rule): rule broken: setCanvasSize must be called before any drawing. Kind: silent logic error. Trigger class: Calling setCanvasSize() after drawing commands, so the earlier drawing is lost.

## Same topic

`standard_drawing` belongs to the topic **Standard drawing and animation** (`topic1.5.e`). The topic also contains: `animation`, `coordinate_scaling`, `drawing_shapes`, `function_plotting`, `mouse_interaction`.

## Rules of the concept (20)

- **Book** (SW-1e, p. 137 (pdf 147)): "The default scale is the unit square (all coordinates between 0 and 1)."
- **Book** (SW-1.5, ): "The default coordinate scale is the unit square (all x- and y-coordinates between 0 and 1)."
- **Book** (StdDraw-API, ): "All subsequent calls to drawing methods such as line(), circle(), and square() will be deffered until the next call to show()."
- **E** (folk-meaning rule): In geometry a point has no size, and on screens positions are pixels with y pointing down. StdDraw.point(x, y) draws a visible spot (a circle of the pen radius) in user coordinates: the default is the unit square, with (0, 0) at the lower-left corner.
- **M** (wrong rule / right rule): DrawWithoutShow: wrong: With double buffering on, each drawing command appears on screen immediately. \| right: By default each command is shown at once. After StdDraw.show(t) turns animation mode on, drawing is collected off-screen and appears only at the next show(t). show() with no argument turns per-command display back on. (Newer StdDraw versions use enableDoubleBuffering().)
- **M** (wrong rule / right rule): PixelCoordinates: wrong: StdDraw.point(256, 256) draws in the middle of the default window. \| right: The default window is 512-by-512 pixels, but coordinates are in the unit square, so the middle is (0.5, 0.5). (256, 256) is far off the canvas.
- **T** (uneven-application rule): Points to LT (commands run in program order; each uses the current scale, color and pen radius; later marks cover earlier ones). An uneven trace uses pixel units for some points, puts y downwards, or applies a setting to commands issued before it.
- **N** (identity rule): StdDraw is a booksite library of static methods for graphical output: lines, points, shapes and text drawn on a 2-D canvas in a window.
- **S** (declarative rule): StdDraw models an abstract device that draws lines and points on a two-dimensional canvas. The default scale is the unit square, and methods with no arguments reset to the defaults.
- **LT** (operational sequencing rule): Calls run in program order. Each control command (setXscale, setPenRadius, setPenColor) affects only the drawing commands after it, and each drawing command paints over what is already on the canvas.
- **OP** (evaluation / result rule): The result is a picture in a window, not a value: the methods are void. Triangle's three line() calls and one point() call produce an equilateral triangle with a dot inside.
- **OS** (state-transition rule): One drawing command adds marks to the canvas (shown at once by default). One control command changes the drawing state (scale, pen radius or color) without drawing anything.
- **R** (composition rule (with a neighbour)): with standard\_input: StdIn values can be drawn directly: PlotFilter reads the bounding box, then point coordinates, and calls StdDraw.point for each pair. Both libraries must be downloaded into the program's directory.
- **R** (composition rule (with a neighbour)): with standard\_output: StdOut writes text to a stream, while StdDraw draws in a separate window at (x, y) coordinates. Neither affects the other.
- **R** (composition rule (with a neighbour)): with animation: Animation reuses StdDraw's drawing commands but adds clear() and show(t), which control when the canvas is erased and displayed.
- **R** (composition rule (with a neighbour)): with coordinate\_scaling: setXscale and setYscale set the coordinate system that every later StdDraw command uses.
- **R** (composition rule (with a neighbour)): with drawing\_shapes: Shape commands are StdDraw drawing commands. They use the same coordinates, pen color and pen radius as line and point.
- **P** (plan / role rule): StdDraw is used to visualize data and functions, which is often more meaningful than lists of numbers.
- **C** (conservation rule): Rescaling the coordinates together with the data keeps the picture. The pen radius is not affected by scaling. Reordering drawing commands changes which mark covers which.
- **D** (error rule): rule broken: StdDraw.java must be in the working directory or on the classpath. (run-time exception)
- **D** (error rule): rule broken: Coordinates must lie inside the current scale to be visible. (silent logic error)
- **D** (error rule): rule broken: setCanvasSize must be called before any drawing. (silent logic error)
- **X** (applicability rule): Use StdDraw for simple plots, data visualizations and teaching animations. It is crude compared with production graphics libraries, and exact numeric results belong on standard output.

## How it is found in code and answers (reader block)

- **Aliases:** stddraw, standard drawing, draws
- **Code patterns:** `StdDraw\.`
- **Operator symbols:** none
- **Java types:** none

## The whole prerequisite chain

- **Everything it builds on (9):** `api`, `arithmetic_operators`, `data_type`, `expression`, `identifier`, `literal`, `method_call`, `primitive_type`, `variable`
- **Everything that builds on it (6):** `animation`, `coordinate_scaling`, `drawing_shapes`, `function_plotting`, `mouse_interaction`, `standard_audio`

## Every edge in this view and its exact edge logic (26)

All the edges drawn in the picture, in the order: prerequisite, parallel, misconception, error, has_level, contains.

**1. `api` &rarr; `standard_drawing`** (prerequisite)

- **Exact edge logic:** StdDraw is a library used through its API of static methods.
- **Grounding:** book\_passage

**2. `standard_drawing` &rarr; `animation`** (prerequisite)

- **Exact edge logic:** Animation uses StdDraw's clear() and show() methods to make dynamic changes to the image on the screen.
- **Grounding:** book\_passage
- **Composition rule (R) of `standard_drawing` with `animation`:** Animation reuses StdDraw's drawing commands but adds clear() and show(t), which control when the canvas is erased and displayed.
- **Composition rule (R) of `animation` with `standard_drawing`:** Animation uses StdDraw's drawing commands plus clear() and show(t). show(t) switches off the default show-after-every-command.

**3. `standard_drawing` &rarr; `coordinate_scaling`** (prerequisite)

- **Exact edge logic:** Scaling sets the coordinate system StdDraw uses.
- **Grounding:** book\_passage
- **Composition rule (R) of `standard_drawing` with `coordinate_scaling`:** setXscale and setYscale set the coordinate system that every later StdDraw command uses.
- **Composition rule (R) of `coordinate_scaling` with `standard_drawing`:** The scale fixes how every later StdDraw coordinate is interpreted. The pen radius is unaffected by it.

**4. `standard_drawing` &rarr; `drawing_shapes`** (prerequisite)

- **Exact edge logic:** Shape commands are StdDraw drawing commands.
- **Grounding:** book\_passage
- **Composition rule (R) of `standard_drawing` with `drawing_shapes`:** Shape commands are StdDraw drawing commands. They use the same coordinates, pen color and pen radius as line and point.
- **Composition rule (R) of `drawing_shapes` with `standard_drawing`:** Shapes use StdDraw's current coordinate scale, pen radius and color, and paint over earlier marks.

**5. `standard_drawing` &rarr; `function_plotting`** (prerequisite)

- **Exact edge logic:** A function is plotted by drawing its sampled points and lines with StdDraw.
- **Grounding:** book\_passage

**6. `standard_drawing` &rarr; `mouse_interaction`** (prerequisite)

- **Exact edge logic:** Mouse position and clicks are read through StdDraw methods such as StdDraw.mousePressed().
- **Grounding:** order\_only

**7. `standard_input` &harr; `standard_drawing`** (parallel)

- **Exact edge logic:** Like StdIn, StdDraw is a library downloaded from the booksite; StdIn brings values into the program, while StdDraw produces drawings as output.
- **Grounding:** book\_passage
- **Composition rule (R) of `standard_input` with `standard_drawing`:** StdIn values can drive StdDraw output. PlotFilter reads x, y pairs and draws a point for each, after scaling from the first four numbers.
- **Composition rule (R) of `standard_drawing` with `standard_input`:** StdIn values can be drawn directly: PlotFilter reads the bounding box, then point coordinates, and calls StdDraw.point for each pair. Both libraries must be downloaded into the program's directory.

**8. `standard_output` &harr; `standard_drawing`** (parallel)

- **Exact edge logic:** StdOut writes text to the output stream; StdDraw draws shapes at (x, y) coordinates in a window.
- **Grounding:** book\_passage
- **Composition rule (R) of `standard_output` with `standard_drawing`:** StdOut text and StdDraw pictures are independent outputs: printing does not draw, and drawing does not print.
- **Composition rule (R) of `standard_drawing` with `standard_output`:** StdOut writes text to a stream, while StdDraw draws in a separate window at (x, y) coordinates. Neither affects the other.

**9. `standard_drawing` &rarr; `DrawWithoutShow`** (misconception)

- **Exact edge logic (the wrong rule):** With double buffering on, each drawing command appears on screen immediately.
- **Twin logic (the right rule):** By default each drawing command appears at once; after StdDraw.show(t) turns animation mode on, drawing is collected and appears only at the next show(t), which then pauses t milliseconds; show() with no argument turns per-command display back on.
- **Role:** context

**10. `standard_drawing` &rarr; `PixelCoordinates`** (misconception)

- **Exact edge logic (the wrong rule):** StdDraw.point(256, 256) draws in the middle of the default window.
- **Twin logic (the right rule):** The default coordinate scale is the unit square, so the middle is (0.5, 0.5).
- **Role:** primary

**11. `animation` &rarr; `DrawWithoutShow`** (misconception)

- **Exact edge logic (the wrong rule):** With double buffering on, each drawing command appears on screen immediately.
- **Twin logic (the right rule):** By default each drawing command appears at once; after StdDraw.show(t) turns animation mode on, drawing is collected and appears only at the next show(t), which then pauses t milliseconds; show() with no argument turns per-command display back on.
- **Role:** primary

**12. `coordinate_scaling` &rarr; `PixelCoordinates`** (misconception)

- **Exact edge logic (the wrong rule):** StdDraw.point(256, 256) draws in the middle of the default window.
- **Twin logic (the right rule):** The default coordinate scale is the unit square, so the middle is (0.5, 0.5).
- **Role:** context

**13. `standard_drawing` &rarr; `StdLibraryNotInDirectory`** (error)

- **Exact edge logic (the wrong rule):** Uses StdIn (or StdDraw/StdAudio) without StdIn.java in the working directory.
- **Twin logic (the right rule):** The Std\* libraries are not built into Java; StdIn.java etc. must be in the same directory (or on the classpath), otherwise Java reports NoClassDefFoundError.
- **Role:** context

**14. `standard_audio` &rarr; `StdLibraryNotInDirectory`** (error)

- **Exact edge logic (the wrong rule):** Uses StdIn (or StdDraw/StdAudio) without StdIn.java in the working directory.
- **Twin logic (the right rule):** The Std\* libraries are not built into Java; StdIn.java etc. must be in the same directory (or on the classpath), otherwise Java reports NoClassDefFoundError.
- **Role:** context

**15. `standard_input` &rarr; `StdLibraryNotInDirectory`** (error)

- **Exact edge logic (the wrong rule):** Uses StdIn (or StdDraw/StdAudio) without StdIn.java in the working directory.
- **Twin logic (the right rule):** The Std\* libraries are not built into Java; StdIn.java etc. must be in the same directory (or on the classpath), otherwise Java reports NoClassDefFoundError.
- **Role:** primary

**16. `standard_drawing` &rarr; `standard_drawing@L0`** (has_level)

- **Exact edge logic:** standard drawing -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (4 ways).
  - **[0] everyday\_reading** (rule type E, folk-meaning rule): In geometry a point has no size, and on screens positions are pixels with y pointing down. StdDraw.point(x, y) draws a visible spot (a circle of the pen radius) in user coordinates: the default is the unit square, with (0, 0) at the lower-left corner.
  - **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `PixelCoordinates`: wrong rule: StdDraw.point(256, 256) draws in the middle of the default window. Right rule: The default window is 512-by-512 pixels, but coordinates are in the unit square, so the middle is (0.5, 0.5). (256, 256) is far off the canvas.
  - **[2] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `PixelCoordinates`: Points to LT (commands run in program order; each uses the current scale, color and pen radius; later marks cover earlier ones). An uneven trace uses pixel units for some points, puts y downwards, or applies a setting to commands issued before it. (here mixing in: "StdDraw.point(256, 256) draws in the middle of the default window")
  - **[3] misconception** (rule type M, wrong rule / right rule) &rarr; `DrawWithoutShow`: wrong rule: With double buffering on, each drawing command appears on screen immediately. Right rule: By default each command is shown at once. After StdDraw.show(t) turns animation mode on, drawing is collected off-screen and appears only at the next show(t). show() with no argument turns per-command display back on. (Newer StdDraw versions use enableDoubleBuffering().)

**17. `standard_drawing` &rarr; `standard_drawing@L1`** (has_level)

- **Exact edge logic:** standard drawing -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).
  - **[0] names\_the\_element** (rule type N, identity rule): StdDraw is a booksite library of static methods for graphical output: lines, points, shapes and text drawn on a 2-D canvas in a window.
  - **[1] states\_the\_rule** (rule type S, declarative rule): StdDraw models an abstract device that draws lines and points on a two-dimensional canvas. The default scale is the unit square, and methods with no arguments reset to the defaults.

**18. `standard_drawing` &rarr; `standard_drawing@L2`** (has_level)

- **Exact edge logic:** standard drawing -&gt; L2 (Multistructural): the answer applies the rules of standard drawing to every part of the code, in order (3 ways).
  - **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): Calls run in program order. Each control command (setXscale, setPenRadius, setPenColor) affects only the drawing commands after it, and each drawing command paints over what is already on the canvas.
  - **[1] output\_prediction** (rule type OP, evaluation / result rule): The result is a picture in a window, not a value: the methods are void. Triangle's three line() calls and one point() call produce an equilateral triangle with a dot inside.
  - **[2] one\_step\_execution** (rule type OS, state-transition rule): One drawing command adds marks to the canvas (shown at once by default). One control command changes the drawing state (scale, pen radius or color) without drawing anything.

**19. `standard_drawing` &rarr; `standard_drawing@L3`** (has_level)

- **Exact edge logic:** standard drawing -&gt; L3 (Relational): the answer relates the parts (6 ways).
  - **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): StdIn values can be drawn directly: PlotFilter reads the bounding box, then point coordinates, and calls StdDraw.point for each pair. Both libraries must be downloaded into the program's directory.
  - **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): StdOut writes text to a stream, while StdDraw draws in a separate window at (x, y) coordinates. Neither affects the other.
  - **[2] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Animation reuses StdDraw's drawing commands but adds clear() and show(t), which control when the canvas is erased and displayed.
  - **[3] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): setXscale and setYscale set the coordinate system that every later StdDraw command uses.
  - **[4] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Shape commands are StdDraw drawing commands. They use the same coordinates, pen color and pen radius as line and point.
  - **[5] purpose\_of\_the\_whole** (rule type P, plan / role rule): StdDraw is used to visualize data and functions, which is often more meaningful than lists of numbers.

**20. `standard_drawing` &rarr; `standard_drawing@L4`** (has_level)

- **Exact edge logic:** standard drawing -&gt; L4 (Extended abstract): the answer reasons beyond the given code (5 ways).
  - **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `PixelCoordinates`: Rescaling the coordinates together with the data keeps the picture. The pen radius is not affected by scaling. Reordering drawing commands changes which mark covers which.
  - **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Use StdDraw for simple plots, data visualizations and teaching animations. It is crude compared with production graphics libraries, and exact numeric results belong on standard output.
  - **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: StdDraw.java must be in the working directory or on the classpath. Kind: run-time exception. Trigger class: Running without StdDraw.class available: NoClassDefFoundError: StdDraw (javac reports 'cannot find symbol' if it is missing at compile time).
  - **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: Coordinates must lie inside the current scale to be visible. Kind: silent logic error. Trigger class: Pixel-style coordinates such as (256, 256) with the default unit square: nothing visible is drawn.
  - **[4] diagnose\_an\_error** (rule type D, error rule): rule broken: setCanvasSize must be called before any drawing. Kind: silent logic error. Trigger class: Calling setCanvasSize() after drawing commands, so the earlier drawing is lost.

**21. `topic1.5.e` &rarr; `standard_drawing`** (contains)

- topic `topic1.5.e` contains `standard_drawing`

**22. `topic1.5.e` &rarr; `animation`** (contains)

- topic `topic1.5.e` contains `animation`

**23. `topic1.5.e` &rarr; `coordinate_scaling`** (contains)

- topic `topic1.5.e` contains `coordinate_scaling`

**24. `topic1.5.e` &rarr; `drawing_shapes`** (contains)

- topic `topic1.5.e` contains `drawing_shapes`

**25. `topic1.5.e` &rarr; `function_plotting`** (contains)

- topic `topic1.5.e` contains `function_plotting`

**26. `topic1.5.e` &rarr; `mouse_interaction`** (contains)

- topic `topic1.5.e` contains `mouse_interaction`
