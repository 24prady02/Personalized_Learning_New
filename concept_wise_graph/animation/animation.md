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

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 16 edges around this concept. The edge logic, the wrong and right rules and the exact rules of the ways are copied word for word from the graph.

## To work on (1)

- no aliases: a student's words cannot name this concept

## What it needs first (2)

A prerequisite edge means the other concept has to be understood before `animation`.

### `standard_drawing` comes before `animation`

*StdDraw -- graphical output (book-specific)*

- **Edge:** `pre:standard_drawing->animation`
- **Exact edge logic:** Animation uses StdDraw's clear() and show() methods to make dynamic changes to the image on the screen.
- **Grounding:** book\_passage
- **Composition rule (R) of `animation` with `standard_drawing`:** Animation uses StdDraw's drawing commands plus clear() and show(t). show(t) switches off the default show-after-every-command.
- **Composition rule (R) of `standard_drawing` with `animation`:** Animation reuses StdDraw's drawing commands but adds clear() and show(t), which control when the canvas is erased and displayed.

### `while_loop` comes before `animation`

*repeat a block while a condition holds*

- **Edge:** `pre:while_loop->animation`
- **Exact edge logic:** BouncingBall repeats erase, draw at the new position, and show with a pause inside a while (true) loop.
- **Grounding:** book\_passage
- **Composition rule (R) of `animation` with `while_loop`:** The frame loop is while (true): it never ends by its condition, so the animation runs until the window or program is closed.
- **Composition rule (R) of `while_loop` with `animation`:** An animation repeats clear/draw/show/pause steps inside a loop, typically one that runs indefinitely.

## What it leads to (1)

These concepts need `animation` first.

### `animation` comes before `mouse_interaction`

*reading mouse position and clicks from StdDraw*

- **Edge:** `pre:animation->mouse_interaction`
- **Exact edge logic:** Mouse checks run inside the animation loop.
- **Grounding:** questionable
- **Composition rule (R) of `animation` with `mouse_interaction`:** Mouse state is polled once per frame inside the animation loop, so it is checked about every dt milliseconds.
- **Composition rule (R) of `mouse_interaction` with `animation`:** Mouse checks run inside the frame loop. A click shorter than one frame (show(t) pause) can be missed.

## Learned alongside (0)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

No parallel edge touches this concept.

## Misconceptions (1)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### DrawWithoutShow

- **Edge:** `animation` &rarr; `DrawWithoutShow` (misconception)
- **Exact edge logic (the wrong rule):** With double buffering on, each drawing command appears on screen immediately.
- **Twin logic (the right rule):** By default each drawing command appears at once; after StdDraw.show(t) turns animation mode on, drawing is collected and appears only at the next show(t), which then pauses t milliseconds; show() with no argument turns per-command display back on.
- **Wrong belief (on the node):** With double buffering on, each drawing command appears on screen immediately.
- **Correct rule (on the node):** By default each drawing command appears at once; after StdDraw.show(t) turns animation mode on, drawing is collected and appears only at the next show(t), which then pauses t milliseconds; show() with no argument turns per-command display back on.
- **Provenance:** derived
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [1] misconception, exact rule:** wrong rule: With double buffering on, each drawing command appears on screen immediately. Right rule: Once show(t) has turned off per-command display, nothing new appears until the next show(t). Each frame must end with show(t).
- **L0 way [2] inconsistent\_trace, exact rule:** Points to LT (update the position, clear, draw, show and pause, in each frame). An uneven trace draws before updating on some frames, or checks the bounce after moving. (here mixing in: "With double buffering on, each drawing command appears on screen immediately")
- **Edge `standard_drawing` &rarr; `DrawWithoutShow`, exact edge logic:** With double buffering on, each drawing command appears on screen immediately. **Twin logic:** By default each drawing command appears at once; after StdDraw.show(t) turns animation mode on, drawing is collected and appears only at the next show(t), which then pauses t milliseconds; show() with no argument turns per-command display back on. (role: context)

## Errors (0)

An error edge states the rule that gets broken in a program, and the right rule.

The graph has no error edge from this concept.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for animation: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to animation agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

- **Edge:** `animation` &rarr; `animation@L0` (has_level)
- **Exact edge logic:** animation -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (3 ways).

Ways (3), each with its exact rule:

- **[0] everyday\_reading** (rule type E, folk-meaning rule): Everyday drawing (pen on paper) appears as you draw, and 'show' sounds like 'display what I drew'. In StdDraw animation mode, drawings are collected off-screen and appear all at once when show(t) is called, which then pauses t ms.
- **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `DrawWithoutShow`: wrong rule: With double buffering on, each drawing command appears on screen immediately. Right rule: Once show(t) has turned off per-command display, nothing new appears until the next show(t). Each frame must end with show(t).
- **[2] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `DrawWithoutShow`: Points to LT (update the position, clear, draw, show and pause, in each frame). An uneven trace draws before updating on some frames, or checks the bounce after moving. (here mixing in: "With double buffering on, each drawing command appears on screen immediately")

### L1: Unistructural / atom x text surface

L1 for animation: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

- **Edge:** `animation` &rarr; `animation@L1` (has_level)
- **Exact edge logic:** animation -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

Ways (2), each with its exact rule:

- **[0] names\_the\_element** (rule type N, identity rule): Animation is a StdDraw technique: a loop that repeatedly erases the canvas, draws the next frame and shows it with a pause, which creates the illusion of motion.
- **[1] states\_the\_rule** (rule type S, declarative rule): clear() and show() support dynamic images. Each frame: erase the drawing (without showing it), draw the new frame, then show the result and wait briefly.

### L2: Multistructural / block x execution / preoperational

L2 for animation: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

- **Edge:** `animation` &rarr; `animation@L2` (has_level)
- **Exact edge logic:** animation -&gt; L2 (Multistructural): the answer applies the rules of animation to every part of the code, in order (3 ways).

Ways (3), each with its exact rule:

- **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): In BouncingBall each pass of while (true) reverses vx or vy if the next position would cross a wall, then updates rx += vx and ry += vy, calls clear(), draws filledCircle(rx, ry, radius), and calls show(20), which displays the frame and pauses 20 ms.
- **[1] output\_prediction** (rule type OP, evaluation / result rule): The output is a sequence of frames: the ball appears to move in a straight line and bounce off the walls of the 2-by-2 box. Starting at rx = .480 with vx = .015, the x-positions are .495, .510, ... until a bounce.
- **[2] one\_step\_execution** (rule type OS, state-transition rule): One frame changes rx and ry by the velocity (flipping the sign of vx or vy at a wall) and replaces the displayed image with the ball at its new position.

### L3: Relational / relations x function (concrete operational begins)

L3 for animation: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

- **Edge:** `animation` &rarr; `animation@L3` (has_level)
- **Exact edge logic:** animation -&gt; L3 (Relational): the answer relates the parts (4 ways).

Ways (4), each with its exact rule:

- **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Animation uses StdDraw's drawing commands plus clear() and show(t). show(t) switches off the default show-after-every-command.
- **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): The frame loop is while (true): it never ends by its condition, so the animation runs until the window or program is closed.
- **[2] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Mouse state is polled once per frame inside the animation loop, so it is checked about every dt milliseconds.
- **[3] purpose\_of\_the\_whole** (rule type P, plan / role rule): Plan: the simulation (time-step) loop. rx and ry are steppers (they advance by a fixed velocity each frame), and vx and vy change only by sign at a bounce.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for animation: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

- **Edge:** `animation` &rarr; `animation@L4` (has_level)
- **Exact edge logic:** animation -&gt; L4 (Extended abstract): the answer reasons beyond the given code (5 ways).

Ways (5), each with its exact rule:

- **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `DrawWithoutShow`: Changing the pause dt changes the speed but not the path. Removing clear() leaves a track of the ball (Exercise 1.5.34). Dropping show(t) and its pause makes the image flicker.
- **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Use animation to show how something evolves over time (simulations, clocks, games). For a static plot, draw once without clear() or show(t).
- **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: In animation mode, each frame must end with show(t). Kind: silent logic error. Trigger class: show(t) is missing inside the loop after it has been called once, so the screen stops updating.
- **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: Without the show/pause control the frames flicker. Kind: silent logic error. Trigger class: clear() and drawing without show(t) (in default mode), so the ball flickers between black and white.
- **[4] diagnose\_an\_error** (rule type D, error rule): rule broken: Each frame must erase the previous one. Kind: silent logic error. Trigger class: clear() is missing, so a trail of balls builds up.

## Same topic

`animation` belongs to the topic **Standard drawing and animation** (`topic1.5.e`). The topic also contains: `coordinate_scaling`, `drawing_shapes`, `function_plotting`, `mouse_interaction`, `standard_drawing`.

## Rules of the concept (17)

- **Book** (SW-1e, p. 143 (pdf 153)): "The clear() and show() methods support dynamic changes in the images on the computer screen."
- **Book** (SW-1.5, ): "Only when you call show() does your drawing get copied from the offscreen canvas to the onscreen canvas."
- **E** (folk-meaning rule): Everyday drawing (pen on paper) appears as you draw, and 'show' sounds like 'display what I drew'. In StdDraw animation mode, drawings are collected off-screen and appear all at once when show(t) is called, which then pauses t ms.
- **M** (wrong rule / right rule): DrawWithoutShow: wrong: With double buffering on, each drawing command appears on screen immediately. \| right: Once show(t) has turned off per-command display, nothing new appears until the next show(t). Each frame must end with show(t).
- **T** (uneven-application rule): Points to LT (update the position, clear, draw, show and pause, in each frame). An uneven trace draws before updating on some frames, or checks the bounce after moving.
- **N** (identity rule): Animation is a StdDraw technique: a loop that repeatedly erases the canvas, draws the next frame and shows it with a pause, which creates the illusion of motion.
- **S** (declarative rule): clear() and show() support dynamic images. Each frame: erase the drawing (without showing it), draw the new frame, then show the result and wait briefly.
- **LT** (operational sequencing rule): In BouncingBall each pass of while (true) reverses vx or vy if the next position would cross a wall, then updates rx += vx and ry += vy, calls clear(), draws filledCircle(rx, ry, radius), and calls show(20), which displays the frame and pauses 20 ms.
- **OP** (evaluation / result rule): The output is a sequence of frames: the ball appears to move in a straight line and bounce off the walls of the 2-by-2 box. Starting at rx = .480 with vx = .015, the x-positions are .495, .510, ... until a bounce.
- **OS** (state-transition rule): One frame changes rx and ry by the velocity (flipping the sign of vx or vy at a wall) and replaces the displayed image with the ball at its new position.
- **R** (composition rule (with a neighbour)): with standard\_drawing: Animation uses StdDraw's drawing commands plus clear() and show(t). show(t) switches off the default show-after-every-command.
- **R** (composition rule (with a neighbour)): with while\_loop: The frame loop is while (true): it never ends by its condition, so the animation runs until the window or program is closed.
- **R** (composition rule (with a neighbour)): with mouse\_interaction: Mouse state is polled once per frame inside the animation loop, so it is checked about every dt milliseconds.
- **P** (plan / role rule): Plan: the simulation (time-step) loop. rx and ry are steppers (they advance by a fixed velocity each frame), and vx and vy change only by sign at a bounce.
- **C** (conservation rule): Changing the pause dt changes the speed but not the path. Removing clear() leaves a track of the ball (Exercise 1.5.34). Dropping show(t) and its pause makes the image flicker.
- **D** (error rule): rule broken: In animation mode, each frame must end with show(t). (silent logic error)
- **D** (error rule): rule broken: Without the show/pause control the frames flicker. (silent logic error)
- **D** (error rule): rule broken: Each frame must erase the previous one. (silent logic error)
- **X** (applicability rule): Use animation to show how something evolves over time (simulations, clocks, games). For a static plot, draw once without clear() or show(t).

## How it is found in code and answers (reader block)

- **Aliases:** none
- **Code patterns:** `StdDraw\.(?:clear|show|pause|enableDoubleBuffering)\s*\(`
- **Operator symbols:** none
- **Java types:** none

## The whole prerequisite chain

- **Everything it builds on (15):** `api`, `arithmetic_operators`, `boolean`, `boolean_expression`, `comparison_operators`, `data_type`, `expression`, `identifier`, `literal`, `logical_operators`, `method_call`, `primitive_type`, `standard_drawing`, `variable`, `while_loop`
- **Everything that builds on it (1):** `mouse_interaction`

## Every edge in this view and its exact edge logic (16)

All the edges drawn in the picture, in the order: prerequisite, parallel, misconception, error, has_level, contains.

**1. `animation` &rarr; `mouse_interaction`** (prerequisite)

- **Exact edge logic:** Mouse checks run inside the animation loop.
- **Grounding:** questionable
- **Composition rule (R) of `animation` with `mouse_interaction`:** Mouse state is polled once per frame inside the animation loop, so it is checked about every dt milliseconds.
- **Composition rule (R) of `mouse_interaction` with `animation`:** Mouse checks run inside the frame loop. A click shorter than one frame (show(t) pause) can be missed.

**2. `standard_drawing` &rarr; `animation`** (prerequisite)

- **Exact edge logic:** Animation uses StdDraw's clear() and show() methods to make dynamic changes to the image on the screen.
- **Grounding:** book\_passage
- **Composition rule (R) of `standard_drawing` with `animation`:** Animation reuses StdDraw's drawing commands but adds clear() and show(t), which control when the canvas is erased and displayed.
- **Composition rule (R) of `animation` with `standard_drawing`:** Animation uses StdDraw's drawing commands plus clear() and show(t). show(t) switches off the default show-after-every-command.

**3. `while_loop` &rarr; `animation`** (prerequisite)

- **Exact edge logic:** BouncingBall repeats erase, draw at the new position, and show with a pause inside a while (true) loop.
- **Grounding:** book\_passage
- **Composition rule (R) of `while_loop` with `animation`:** An animation repeats clear/draw/show/pause steps inside a loop, typically one that runs indefinitely.
- **Composition rule (R) of `animation` with `while_loop`:** The frame loop is while (true): it never ends by its condition, so the animation runs until the window or program is closed.

**4. `animation` &rarr; `DrawWithoutShow`** (misconception)

- **Exact edge logic (the wrong rule):** With double buffering on, each drawing command appears on screen immediately.
- **Twin logic (the right rule):** By default each drawing command appears at once; after StdDraw.show(t) turns animation mode on, drawing is collected and appears only at the next show(t), which then pauses t milliseconds; show() with no argument turns per-command display back on.
- **Role:** primary

**5. `standard_drawing` &rarr; `DrawWithoutShow`** (misconception)

- **Exact edge logic (the wrong rule):** With double buffering on, each drawing command appears on screen immediately.
- **Twin logic (the right rule):** By default each drawing command appears at once; after StdDraw.show(t) turns animation mode on, drawing is collected and appears only at the next show(t), which then pauses t milliseconds; show() with no argument turns per-command display back on.
- **Role:** context

**6. `animation` &rarr; `animation@L0`** (has_level)

- **Exact edge logic:** animation -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (3 ways).
  - **[0] everyday\_reading** (rule type E, folk-meaning rule): Everyday drawing (pen on paper) appears as you draw, and 'show' sounds like 'display what I drew'. In StdDraw animation mode, drawings are collected off-screen and appear all at once when show(t) is called, which then pauses t ms.
  - **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `DrawWithoutShow`: wrong rule: With double buffering on, each drawing command appears on screen immediately. Right rule: Once show(t) has turned off per-command display, nothing new appears until the next show(t). Each frame must end with show(t).
  - **[2] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `DrawWithoutShow`: Points to LT (update the position, clear, draw, show and pause, in each frame). An uneven trace draws before updating on some frames, or checks the bounce after moving. (here mixing in: "With double buffering on, each drawing command appears on screen immediately")

**7. `animation` &rarr; `animation@L1`** (has_level)

- **Exact edge logic:** animation -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).
  - **[0] names\_the\_element** (rule type N, identity rule): Animation is a StdDraw technique: a loop that repeatedly erases the canvas, draws the next frame and shows it with a pause, which creates the illusion of motion.
  - **[1] states\_the\_rule** (rule type S, declarative rule): clear() and show() support dynamic images. Each frame: erase the drawing (without showing it), draw the new frame, then show the result and wait briefly.

**8. `animation` &rarr; `animation@L2`** (has_level)

- **Exact edge logic:** animation -&gt; L2 (Multistructural): the answer applies the rules of animation to every part of the code, in order (3 ways).
  - **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): In BouncingBall each pass of while (true) reverses vx or vy if the next position would cross a wall, then updates rx += vx and ry += vy, calls clear(), draws filledCircle(rx, ry, radius), and calls show(20), which displays the frame and pauses 20 ms.
  - **[1] output\_prediction** (rule type OP, evaluation / result rule): The output is a sequence of frames: the ball appears to move in a straight line and bounce off the walls of the 2-by-2 box. Starting at rx = .480 with vx = .015, the x-positions are .495, .510, ... until a bounce.
  - **[2] one\_step\_execution** (rule type OS, state-transition rule): One frame changes rx and ry by the velocity (flipping the sign of vx or vy at a wall) and replaces the displayed image with the ball at its new position.

**9. `animation` &rarr; `animation@L3`** (has_level)

- **Exact edge logic:** animation -&gt; L3 (Relational): the answer relates the parts (4 ways).
  - **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Animation uses StdDraw's drawing commands plus clear() and show(t). show(t) switches off the default show-after-every-command.
  - **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): The frame loop is while (true): it never ends by its condition, so the animation runs until the window or program is closed.
  - **[2] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Mouse state is polled once per frame inside the animation loop, so it is checked about every dt milliseconds.
  - **[3] purpose\_of\_the\_whole** (rule type P, plan / role rule): Plan: the simulation (time-step) loop. rx and ry are steppers (they advance by a fixed velocity each frame), and vx and vy change only by sign at a bounce.

**10. `animation` &rarr; `animation@L4`** (has_level)

- **Exact edge logic:** animation -&gt; L4 (Extended abstract): the answer reasons beyond the given code (5 ways).
  - **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `DrawWithoutShow`: Changing the pause dt changes the speed but not the path. Removing clear() leaves a track of the ball (Exercise 1.5.34). Dropping show(t) and its pause makes the image flicker.
  - **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Use animation to show how something evolves over time (simulations, clocks, games). For a static plot, draw once without clear() or show(t).
  - **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: In animation mode, each frame must end with show(t). Kind: silent logic error. Trigger class: show(t) is missing inside the loop after it has been called once, so the screen stops updating.
  - **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: Without the show/pause control the frames flicker. Kind: silent logic error. Trigger class: clear() and drawing without show(t) (in default mode), so the ball flickers between black and white.
  - **[4] diagnose\_an\_error** (rule type D, error rule): rule broken: Each frame must erase the previous one. Kind: silent logic error. Trigger class: clear() is missing, so a trail of balls builds up.

**11. `topic1.5.e` &rarr; `animation`** (contains)

- topic `topic1.5.e` contains `animation`

**12. `topic1.5.e` &rarr; `coordinate_scaling`** (contains)

- topic `topic1.5.e` contains `coordinate_scaling`

**13. `topic1.5.e` &rarr; `drawing_shapes`** (contains)

- topic `topic1.5.e` contains `drawing_shapes`

**14. `topic1.5.e` &rarr; `function_plotting`** (contains)

- topic `topic1.5.e` contains `function_plotting`

**15. `topic1.5.e` &rarr; `mouse_interaction`** (contains)

- topic `topic1.5.e` contains `mouse_interaction`

**16. `topic1.5.e` &rarr; `standard_drawing`** (contains)

- topic `topic1.5.e` contains `standard_drawing`
