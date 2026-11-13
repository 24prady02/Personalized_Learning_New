# animation (`animation`)

StdDraw animation: clear, draw, show, pause in a loop

Section 1.5 Input and Output, topic 1.5.e Standard drawing and animation.

![The knowledge graph around animation](animation.png)

## At a glance

- **Needs first:** `standard_drawing`, `while_loop`
- **Leads to:** `mouse_interaction`
- **Learned alongside:** nothing
- **Misconceptions:** `DrawWithoutShow`
- **Errors:** none
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 16 edges around this concept, each explained in the graph's own words.

## What it needs first (2)

A prerequisite edge means the other concept has to be understood before `animation`.

### `standard_drawing` comes before `animation`

*StdDraw -- graphical output (book-specific)*

Animation uses StdDraw's clear() and show() methods to make dynamic changes to the image on the screen.

- **Grounding:** book passage
- **How `animation` combines with `standard_drawing`:** Animation uses StdDraw's drawing commands plus clear() and show(t). show(t) switches off the default show-after-every-command.
- **How `standard_drawing` combines with `animation`:** Animation reuses StdDraw's drawing commands but adds clear() and show(t), which control when the canvas is erased and displayed.

### `while_loop` comes before `animation`

*repeat a block while a condition holds*

BouncingBall repeats erase, draw at the new position, and show with a pause inside a while (true) loop.

- **Grounding:** book passage
- **How `animation` combines with `while_loop`:** The frame loop is while (true): it never ends by its condition, so the animation runs until the window or program is closed.
- **How `while_loop` combines with `animation`:** An animation repeats clear/draw/show/pause steps inside a loop, typically one that runs indefinitely.

## What it leads to (1)

These concepts need `animation` first.

### `animation` comes before `mouse_interaction`

*reading mouse position and clicks from StdDraw*

Mouse checks run inside the animation loop.

- **Grounding:** questionable
- **How `animation` combines with `mouse_interaction`:** Mouse state is polled once per frame inside the animation loop, so it is checked about every dt milliseconds.
- **How `mouse_interaction` combines with `animation`:** Mouse checks run inside the frame loop. A click shorter than one frame (show(t) pause) can be missed.

## Learned alongside (0)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

No parallel edge touches this concept.

## Misconceptions (1)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### DrawWithoutShow

- **Wrong rule:** With double buffering on, each drawing command appears on screen immediately.
- **Right rule:** By default each drawing command appears at once; after StdDraw.show(t) turns animation mode on, drawing is collected and appears only at the next show(t), which then pauses t milliseconds; show() with no argument turns per-command display back on.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: With double buffering on, each drawing command appears on screen immediately. Right rule: Once show(t) has turned off per-command display, nothing new appears until the next show(t). Each frame must end with show(t).
- **Shows at level L0 as:** inconsistent trace: Points to LT (update the position, clear, draw, show and pause, in each frame). An uneven trace draws before updating on some frames, or checks the bounce after moving. (here mixing in: "With double buffering on, each drawing command appears on screen immediately")
- **Also an edge from `standard_drawing`:** With double buffering on, each drawing command appears on screen immediately.

## Errors (0)

An error edge states the rule that gets broken in a program, and the right rule.

The graph has no error edge from this concept.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for animation: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to animation agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

animation -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (3 ways).

- **everyday reading** (folk-meaning rule): Everyday drawing (pen on paper) appears as you draw, and 'show' sounds like 'display what I drew'. In StdDraw animation mode, drawings are collected off-screen and appear all at once when show(t) is called, which then pauses t ms.
- **misconception** (wrong rule / right rule; shows `DrawWithoutShow`): wrong rule: With double buffering on, each drawing command appears on screen immediately. Right rule: Once show(t) has turned off per-command display, nothing new appears until the next show(t). Each frame must end with show(t).
- **inconsistent trace** (uneven-application rule; shows `DrawWithoutShow`): Points to LT (update the position, clear, draw, show and pause, in each frame). An uneven trace draws before updating on some frames, or checks the bounce after moving. (here mixing in: "With double buffering on, each drawing command appears on screen immediately")

### L1: Unistructural / atom x text surface

L1 for animation: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

animation -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

- **names the element** (identity rule): Animation is a StdDraw technique: a loop that repeatedly erases the canvas, draws the next frame and shows it with a pause, which creates the illusion of motion.
- **states the rule** (declarative rule): clear() and show() support dynamic images. Each frame: erase the drawing (without showing it), draw the new frame, then show the result and wait briefly.

### L2: Multistructural / block x execution / preoperational

L2 for animation: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

animation -&gt; L2 (Multistructural): the answer applies the rules of animation to every part of the code, in order (3 ways).

- **line by line trace** (operational sequencing rule): In BouncingBall each pass of while (true) reverses vx or vy if the next position would cross a wall, then updates rx += vx and ry += vy, calls clear(), draws filledCircle(rx, ry, radius), and calls show(20), which displays the frame and pauses 20 ms.
- **output prediction** (evaluation / result rule): The output is a sequence of frames: the ball appears to move in a straight line and bounce off the walls of the 2-by-2 box. Starting at rx = .480 with vx = .015, the x-positions are .495, .510, ... until a bounce.
- **one step execution** (state-transition rule): One frame changes rx and ry by the velocity (flipping the sign of vx or vy at a wall) and replaces the displayed image with the ball at its new position.

### L3: Relational / relations x function (concrete operational begins)

L3 for animation: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

animation -&gt; L3 (Relational): the answer relates the parts (4 ways).

- **relation to neighbour** (composition rule (with a neighbour)): Animation uses StdDraw's drawing commands plus clear() and show(t). show(t) switches off the default show-after-every-command.
- **relation to neighbour** (composition rule (with a neighbour)): The frame loop is while (true): it never ends by its condition, so the animation runs until the window or program is closed.
- **relation to neighbour** (composition rule (with a neighbour)): Mouse state is polled once per frame inside the animation loop, so it is checked about every dt milliseconds.
- **purpose of the whole** (plan / role rule): Plan: the simulation (time-step) loop. rx and ry are steppers (they advance by a fixed velocity each frame), and vx and vy change only by sign at a bounce.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for animation: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

animation -&gt; L4 (Extended abstract): the answer reasons beyond the given code (5 ways).

- **predict a change** (conservation rule; shows `DrawWithoutShow`): Changing the pause dt changes the speed but not the path. Removing clear() leaves a track of the ball (Exercise 1.5.34). Dropping show(t) and its pause makes the image flicker.
- **transfer to a new program** (applicability rule): Use animation to show how something evolves over time (simulations, clocks, games). For a static plot, draw once without clear() or show(t).
- **diagnose an error** (error rule): rule broken: In animation mode, each frame must end with show(t). Kind: silent logic error. Trigger class: show(t) is missing inside the loop after it has been called once, so the screen stops updating.
- **diagnose an error** (error rule): rule broken: Without the show/pause control the frames flicker. Kind: silent logic error. Trigger class: clear() and drawing without show(t) (in default mode), so the ball flickers between black and white.
- **diagnose an error** (error rule): rule broken: Each frame must erase the previous one. Kind: silent logic error. Trigger class: clear() is missing, so a trail of balls builds up.

## Same topic

`animation` belongs to the topic **Standard drawing and animation** (`topic1.5.e`). The topic also contains: `coordinate_scaling`, `drawing_shapes`, `function_plotting`, `mouse_interaction`, `standard_drawing`.

## Rules of the concept (17)

- **folk-meaning rule:** Everyday drawing (pen on paper) appears as you draw, and 'show' sounds like 'display what I drew'. In StdDraw animation mode, drawings are collected off-screen and appear all at once when show(t) is called, which then pauses t ms.
- **wrong rule / right rule:** DrawWithoutShow: wrong: With double buffering on, each drawing command appears on screen immediately. \| right: Once show(t) has turned off per-command display, nothing new appears until the next show(t). Each frame must end with show(t).
- **uneven-application rule:** Points to LT (update the position, clear, draw, show and pause, in each frame). An uneven trace draws before updating on some frames, or checks the bounce after moving.
- **identity rule:** Animation is a StdDraw technique: a loop that repeatedly erases the canvas, draws the next frame and shows it with a pause, which creates the illusion of motion.
- **declarative rule:** clear() and show() support dynamic images. Each frame: erase the drawing (without showing it), draw the new frame, then show the result and wait briefly.
- **operational sequencing rule:** In BouncingBall each pass of while (true) reverses vx or vy if the next position would cross a wall, then updates rx += vx and ry += vy, calls clear(), draws filledCircle(rx, ry, radius), and calls show(20), which displays the frame and pauses 20 ms.
- **evaluation / result rule:** The output is a sequence of frames: the ball appears to move in a straight line and bounce off the walls of the 2-by-2 box. Starting at rx = .480 with vx = .015, the x-positions are .495, .510, ... until a bounce.
- **state-transition rule:** One frame changes rx and ry by the velocity (flipping the sign of vx or vy at a wall) and replaces the displayed image with the ball at its new position.
- **composition rule (with a neighbour):** with standard\_drawing: Animation uses StdDraw's drawing commands plus clear() and show(t). show(t) switches off the default show-after-every-command.
- **composition rule (with a neighbour):** with while\_loop: The frame loop is while (true): it never ends by its condition, so the animation runs until the window or program is closed.
- **composition rule (with a neighbour):** with mouse\_interaction: Mouse state is polled once per frame inside the animation loop, so it is checked about every dt milliseconds.
- **plan / role rule:** Plan: the simulation (time-step) loop. rx and ry are steppers (they advance by a fixed velocity each frame), and vx and vy change only by sign at a bounce.
- **conservation rule:** Changing the pause dt changes the speed but not the path. Removing clear() leaves a track of the ball (Exercise 1.5.34). Dropping show(t) and its pause makes the image flicker.
- **error rule:** rule broken: In animation mode, each frame must end with show(t). (silent logic error)
- **error rule:** rule broken: Without the show/pause control the frames flicker. (silent logic error)
- **error rule:** rule broken: Each frame must erase the previous one. (silent logic error)
- **applicability rule:** Use animation to show how something evolves over time (simulations, clocks, games). For a static plot, draw once without clear() or show(t).

## The whole prerequisite chain

- **Everything it builds on (15):** `api`, `arithmetic_operators`, `boolean`, `boolean_expression`, `comparison_operators`, `data_type`, `expression`, `identifier`, `literal`, `logical_operators`, `method_call`, `primitive_type`, `standard_drawing`, `variable`, `while_loop`
- **Everything that builds on it (1):** `mouse_interaction`
