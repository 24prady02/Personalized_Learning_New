# drawing_shapes (`drawing_shapes`)

outline vs filled shapes, square half-length, colour and text

Section 1.5 Input and Output, topic 1.5.e Standard drawing and animation.

![The knowledge graph around drawing_shapes](drawing_shapes.png)

## At a glance

- **Needs first:** `standard_drawing`
- **Leads to:** nothing
- **Learned alongside:** nothing
- **Misconceptions:** `SquareArgIsSide`
- **Errors:** none
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 13 edges around this concept, each explained in the graph's own words.

## What it needs first (1)

A prerequisite edge means the other concept has to be understood before `drawing_shapes`.

### `standard_drawing` comes before `drawing_shapes`

*StdDraw -- graphical output (book-specific)*

Shape commands are StdDraw drawing commands.

- **Grounding:** book passage
- **How `drawing_shapes` combines with `standard_drawing`:** Shapes use StdDraw's current coordinate scale, pen radius and color, and paint over earlier marks.
- **How `standard_drawing` combines with `drawing_shapes`:** Shape commands are StdDraw drawing commands. They use the same coordinates, pen color and pen radius as line and point.

## What it leads to (0)

These concepts need `drawing_shapes` first.

No concept has this one as a prerequisite.

## Learned alongside (0)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

No parallel edge touches this concept.

## Misconceptions (1)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### SquareArgIsSide

- **Wrong rule:** StdDraw.square(x, y, r) draws a square with side length r.
- **Right rule:** The square has side length 2r, centred on (x, y).
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: StdDraw.square(x, y, r) draws a square with side length r. Right rule: The square has side length 2r, centred on (x, y).
- **Shows at level L0 as:** inconsistent trace: Points to LT (each shape is centred on (x, y); a polygon joins its points in order and closes back to the first). An uneven trace uses (x, y) as a corner for some shapes, or leaves a polygon open. (here mixing in: "StdDraw.square(x, y, r) draws a square with side length r")

## Errors (0)

An error edge states the rule that gets broken in a program, and the right rule.

The graph has no error edge from this concept.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for drawing shapes: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to drawing shapes agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

drawing shapes -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (3 ways).

- **everyday reading** (folk-meaning rule): In everyday geometry, square(x, y, r) reads as a square with side r, with (x, y) as a corner. In StdDraw, r is the half-side: the square has side 2r and is centred on (x, y). For circles, r is the radius.
- **misconception** (wrong rule / right rule; shows `SquareArgIsSide`): wrong rule: StdDraw.square(x, y, r) draws a square with side length r. Right rule: The square has side length 2r, centred on (x, y).
- **inconsistent trace** (uneven-application rule; shows `SquareArgIsSide`): Points to LT (each shape is centred on (x, y); a polygon joins its points in order and closes back to the first). An uneven trace uses (x, y) as a corner for some shapes, or leaves a polygon open. (here mixing in: "StdDraw.square(x, y, r) draws a square with side length r")

### L1: Unistructural / atom x text surface

L1 for drawing shapes: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

drawing shapes -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

- **names the element** (identity rule): Shape commands are StdDraw drawing methods: circle, square and polygon, each with a filled version, plus text and pen color.
- **states the rule** (declarative rule): A method named after the shape traces its outline, and one whose name begins with filled fills it solid. circle(x, y, r) has radius r and square(x, y, r) has side 2r, both centred on (x, y).

### L2: Multistructural / block x execution / preoperational

L2 for drawing shapes: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

drawing shapes -&gt; L2 (Multistructural): the answer applies the rules of drawing shapes to every part of the code, in order (3 ways).

- **line by line trace** (operational sequencing rule): polygon(x[], y[]) draws a line from point 0 to point 1, then 1 to 2, and so on, and finally from the last point back to point 0. Each shape is drawn in the pen color current at the call.
- **output prediction** (evaluation / result rule): square(.2, .8, .1) draws an outline square 0.2 wide with corners (.1, .7) and (.3, .9). filledSquare(.8, .8, .2) draws a solid 0.4-wide square. The methods return void.
- **one step execution** (state-transition rule): A shape call adds one outlined or filled shape in the current pen color. setPenColor only changes the ink used by later calls (the default is BLACK).

### L3: Relational / relations x function (concrete operational begins)

L3 for drawing shapes: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

drawing shapes -&gt; L3 (Relational): the answer relates the parts (2 ways).

- **relation to neighbour** (composition rule (with a neighbour)): Shapes use StdDraw's current coordinate scale, pen radius and color, and paint over earlier marks.
- **purpose of the whole** (plan / role rule): Shapes, color and text annotate and highlight drawings, and color can represent data values.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for drawing shapes: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

drawing shapes -&gt; L4 (Extended abstract): the answer reasons beyond the given code (4 ways).

- **predict a change** (conservation rule; shows `SquareArgIsSide`): Switching shape(...) to filledShape(...) keeps the geometry and only fills it. A diamond is the polygon of a 2r-by-2r square rotated 45 degrees about the same centre.
- **transfer to a new program** (applicability rule): Use circle and square (and their filled versions) for those shapes. For any other shape, use polygon or filledPolygon.
- **diagnose an error** (error rule): rule broken: square's r is the half-length. Kind: silent logic error. Trigger class: Passing the side length as r, so squares come out twice as large and overlap.
- **diagnose an error** (error rule): rule broken: setPenColor takes a Color constant, not a String. Kind: compile-time. Trigger class: StdDraw.setPenColor("red"): no method accepts a String (use StdDraw.RED).

## Same topic

`drawing_shapes` belongs to the topic **Standard drawing and animation** (`topic1.5.e`). The topic also contains: `animation`, `coordinate_scaling`, `function_plotting`, `mouse_interaction`, `standard_drawing`.

## Rules of the concept (14)

- **folk-meaning rule:** In everyday geometry, square(x, y, r) reads as a square with side r, with (x, y) as a corner. In StdDraw, r is the half-side: the square has side 2r and is centred on (x, y). For circles, r is the radius.
- **wrong rule / right rule:** SquareArgIsSide: wrong: StdDraw.square(x, y, r) draws a square with side length r. \| right: The square has side length 2r, centred on (x, y).
- **uneven-application rule:** Points to LT (each shape is centred on (x, y); a polygon joins its points in order and closes back to the first). An uneven trace uses (x, y) as a corner for some shapes, or leaves a polygon open.
- **identity rule:** Shape commands are StdDraw drawing methods: circle, square and polygon, each with a filled version, plus text and pen color.
- **declarative rule:** A method named after the shape traces its outline, and one whose name begins with filled fills it solid. circle(x, y, r) has radius r and square(x, y, r) has side 2r, both centred on (x, y).
- **operational sequencing rule:** polygon(x[], y[]) draws a line from point 0 to point 1, then 1 to 2, and so on, and finally from the last point back to point 0. Each shape is drawn in the pen color current at the call.
- **evaluation / result rule:** square(.2, .8, .1) draws an outline square 0.2 wide with corners (.1, .7) and (.3, .9). filledSquare(.8, .8, .2) draws a solid 0.4-wide square. The methods return void.
- **state-transition rule:** A shape call adds one outlined or filled shape in the current pen color. setPenColor only changes the ink used by later calls (the default is BLACK).
- **composition rule (with a neighbour):** with standard\_drawing: Shapes use StdDraw's current coordinate scale, pen radius and color, and paint over earlier marks.
- **plan / role rule:** Shapes, color and text annotate and highlight drawings, and color can represent data values.
- **conservation rule:** Switching shape(...) to filledShape(...) keeps the geometry and only fills it. A diamond is the polygon of a 2r-by-2r square rotated 45 degrees about the same centre.
- **error rule:** rule broken: square's r is the half-length. (silent logic error)
- **error rule:** rule broken: setPenColor takes a Color constant, not a String. (compile-time)
- **applicability rule:** Use circle and square (and their filled versions) for those shapes. For any other shape, use polygon or filledPolygon.

## The whole prerequisite chain

- **Everything it builds on (10):** `api`, `arithmetic_operators`, `data_type`, `expression`, `identifier`, `literal`, `method_call`, `primitive_type`, `standard_drawing`, `variable`
- **Everything that builds on it (0):** nothing
