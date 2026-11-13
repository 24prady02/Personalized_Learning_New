# drawing_shapes (`drawing_shapes`)

outline vs filled shapes, square half-length, colour and text

Section 1.5 Input and Output, topic 1.5.e Standard drawing and animation. From the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`).

![The knowledge graph around drawing_shapes](drawing_shapes.png)

## Concepts associated with drawing\_shapes (5)

| Concept | Description | How it is associated |
| --- | --- | --- |
| **animation** | StdDraw animation: clear, draw, show, pause in a loop | same topic (topic1.5.e) |
| **coordinate\_scaling** | StdDraw's unit square and setXscale/setYscale | same topic (topic1.5.e) |
| **function\_plotting** | sampling a function and joining the points with lines | same topic (topic1.5.e) |
| **mouse\_interaction** | reading mouse position and clicks from StdDraw | same topic (topic1.5.e) |
| **standard\_drawing** | StdDraw -- graphical output (book-specific) | prerequisite of it (it needs this)<br>composition rule (R) with it<br>same topic (topic1.5.e) |

## Every edge in this view and its full label (13)

| From | Edge | To | Full edge label |
| --- | --- | --- | --- |
| **standard\_drawing** | prerequisite | **drawing\_shapes** | Shape commands are StdDraw drawing commands.<br>grounding: book\_passage<br>composition rule (R) of standard\_drawing with drawing\_shapes: Shape commands are StdDraw drawing commands. They use the same coordinates, pen color and pen radius as line and point.<br>composition rule (R) of drawing\_shapes with standard\_drawing: Shapes use StdDraw's current coordinate scale, pen radius and color, and paint over earlier marks. |
| **drawing\_shapes** | misconception | **SquareArgIsSide** | **wrong rule:** StdDraw.square(x, y, r) draws a square with side length r.<br>**right rule:** The square has side length 2r, centred on (x, y).<br>role: primary |
| **drawing\_shapes** | has\_level | **drawing\_shapes@L0** | drawing shapes -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (3 ways).<br>**[0] everyday\_reading** (E): In everyday geometry, square(x, y, r) reads as a square with side r, with (x, y) as a corner. In StdDraw, r is the half-side: the square has side 2r and is centred on (x, y). For circles, r is the radius.<br>**[1] misconception** (M) &rarr; SquareArgIsSide: wrong rule: StdDraw.square(x, y, r) draws a square with side length r. Right rule: The square has side length 2r, centred on (x, y).<br>**[2] inconsistent\_trace** (T) &rarr; SquareArgIsSide: Points to LT (each shape is centred on (x, y); a polygon joins its points in order and closes back to the first). An uneven trace uses (x, y) as a corner for some shapes, or leaves a polygon open. (here mixing in: "StdDraw.square(x, y, r) draws a square with side length r") |
| **drawing\_shapes** | has\_level | **drawing\_shapes@L1** | drawing shapes -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).<br>**[0] names\_the\_element** (N): Shape commands are StdDraw drawing methods: circle, square and polygon, each with a filled version, plus text and pen color.<br>**[1] states\_the\_rule** (S): A method named after the shape traces its outline, and one whose name begins with filled fills it solid. circle(x, y, r) has radius r and square(x, y, r) has side 2r, both centred on (x, y). |
| **drawing\_shapes** | has\_level | **drawing\_shapes@L2** | drawing shapes -&gt; L2 (Multistructural): the answer applies the rules of drawing shapes to every part of the code, in order (3 ways).<br>**[0] line\_by\_line\_trace** (LT): polygon(x[], y[]) draws a line from point 0 to point 1, then 1 to 2, and so on, and finally from the last point back to point 0. Each shape is drawn in the pen color current at the call.<br>**[1] output\_prediction** (OP): square(.2, .8, .1) draws an outline square 0.2 wide with corners (.1, .7) and (.3, .9). filledSquare(.8, .8, .2) draws a solid 0.4-wide square. The methods return void.<br>**[2] one\_step\_execution** (OS): A shape call adds one outlined or filled shape in the current pen color. setPenColor only changes the ink used by later calls (the default is BLACK). |
| **drawing\_shapes** | has\_level | **drawing\_shapes@L3** | drawing shapes -&gt; L3 (Relational): the answer relates the parts (2 ways).<br>**[0] relation\_to\_neighbour** (R): Shapes use StdDraw's current coordinate scale, pen radius and color, and paint over earlier marks.<br>**[1] purpose\_of\_the\_whole** (P): Shapes, color and text annotate and highlight drawings, and color can represent data values. |
| **drawing\_shapes** | has\_level | **drawing\_shapes@L4** | drawing shapes -&gt; L4 (Extended abstract): the answer reasons beyond the given code (4 ways).<br>**[0] predict\_a\_change** (C) &rarr; SquareArgIsSide: Switching shape(...) to filledShape(...) keeps the geometry and only fills it. A diamond is the polygon of a 2r-by-2r square rotated 45 degrees about the same centre.<br>**[1] transfer\_to\_a\_new\_program** (X): Use circle and square (and their filled versions) for those shapes. For any other shape, use polygon or filledPolygon.<br>**[2] diagnose\_an\_error** (D): rule broken: square's r is the half-length. Kind: silent logic error. Trigger class: Passing the side length as r, so squares come out twice as large and overlap.<br>**[3] diagnose\_an\_error** (D): rule broken: setPenColor takes a Color constant, not a String. Kind: compile-time. Trigger class: StdDraw.setPenColor("red"): no method accepts a String (use StdDraw.RED). |
| **topic1.5.e** | contains | **animation** | topic topic1.5.e contains animation |
| **topic1.5.e** | contains | **coordinate\_scaling** | topic topic1.5.e contains coordinate\_scaling |
| **topic1.5.e** | contains | **drawing\_shapes** | topic topic1.5.e contains drawing\_shapes |
| **topic1.5.e** | contains | **function\_plotting** | topic topic1.5.e contains function\_plotting |
| **topic1.5.e** | contains | **mouse\_interaction** | topic topic1.5.e contains mouse\_interaction |
| **topic1.5.e** | contains | **standard\_drawing** | topic topic1.5.e contains standard\_drawing |
