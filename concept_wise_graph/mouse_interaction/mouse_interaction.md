# mouse_interaction (`mouse_interaction`)

reading mouse position and clicks from StdDraw

Section 1.5 Input and Output, topic 1.5.e Standard drawing and animation.

![The knowledge graph around mouse_interaction](mouse_interaction.png)

## At a glance

- **Needs first:** `animation`, `standard_drawing`
- **Leads to:** nothing
- **Learned alongside:** nothing
- **Misconceptions:** `MouseIsEvent`
- **Errors:** none
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 14 edges around this concept. The edge logic, the wrong and right rules and the exact rules of the ways are copied word for word from the graph.

## To work on (1)

- no aliases: a student's words cannot name this concept

## What it needs first (2)

A prerequisite edge means the other concept has to be understood before `mouse_interaction`.

### `animation` comes before `mouse_interaction`

*StdDraw animation: clear, draw, show, pause in a loop*

- **Edge:** `pre:animation->mouse_interaction`
- **Exact edge logic:** Mouse checks run inside the animation loop.
- **Grounding:** questionable
- **Composition rule (R) of `mouse_interaction` with `animation`:** Mouse checks run inside the frame loop. A click shorter than one frame (show(t) pause) can be missed.
- **Composition rule (R) of `animation` with `mouse_interaction`:** Mouse state is polled once per frame inside the animation loop, so it is checked about every dt milliseconds.

### `standard_drawing` comes before `mouse_interaction`

*StdDraw -- graphical output (book-specific)*

- **Edge:** `pre:standard_drawing->mouse_interaction`
- **Exact edge logic:** Mouse position and clicks are read through StdDraw methods such as StdDraw.mousePressed().
- **Grounding:** order\_only

## What it leads to (0)

These concepts need `mouse_interaction` first.

No concept has this one as a prerequisite.

## Learned alongside (0)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

No parallel edge touches this concept.

## Misconceptions (1)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### MouseIsEvent

- **Edge:** `mouse_interaction` &rarr; `MouseIsEvent` (misconception)
- **Exact edge logic (the wrong rule):** StdDraw.mousePressed() waits until the user clicks.
- **Twin logic (the right rule):** mousePressed() only reports whether the button is down at that moment, so it is checked repeatedly in a loop.
- **Wrong belief (on the node):** StdDraw.mousePressed() waits until the user clicks.
- **Correct rule (on the node):** mousePressed() only reports whether the button is down at that moment, so it is checked repeatedly in a loop.
- **Provenance:** derived
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [1] misconception, exact rule:** wrong rule: StdDraw.mousePressed() waits until the user clicks. Right rule: mousePressed() returns immediately with true or false for that moment. To catch clicks, poll it on every frame of a loop.
- **L0 way [2] inconsistent\_trace, exact rule:** Points to LT (each frame polls mousePressed, mouseX and mouseY once). An uneven trace treats one poll as blocking, or reuses an old position on some frames. (here mixing in: "StdDraw.mousePressed() waits until the user clicks")

## Errors (0)

An error edge states the rule that gets broken in a program, and the right rule.

The graph has no error edge from this concept.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for mouse interaction: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to mouse interaction agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

- **Edge:** `mouse_interaction` &rarr; `mouse_interaction@L0` (has_level)
- **Exact edge logic:** mouse interaction -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (3 ways).

Ways (3), each with its exact rule:

- **[0] everyday\_reading** (rule type E, folk-meaning rule): In the everyday sense, 'mouse pressed' is an event the program waits for. StdDraw.mousePressed() only reports whether the button is down at the moment of the call.
- **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `MouseIsEvent`: wrong rule: StdDraw.mousePressed() waits until the user clicks. Right rule: mousePressed() returns immediately with true or false for that moment. To catch clicks, poll it on every frame of a loop.
- **[2] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `MouseIsEvent`: Points to LT (each frame polls mousePressed, mouseX and mouseY once). An uneven trace treats one poll as blocking, or reuses an old position on some frames. (here mixing in: "StdDraw.mousePressed() waits until the user clicks")

### L1: Unistructural / atom x text surface

L1 for mouse interaction: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

- **Edge:** `mouse_interaction` &rarr; `mouse_interaction@L1` (has_level)
- **Exact edge logic:** mouse interaction -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

Ways (2), each with its exact rule:

- **[0] names\_the\_element** (rule type N, identity rule): Mouse interaction is the StdDraw input methods mousePressed(), mouseX() and mouseY(), which report the mouse state in user coordinates.
- **[1] states\_the\_rule** (rule type S, declarative rule): mousePressed() returns whether the button is currently pressed. mouseX() and mouseY() return the latest pointer position in the current x/y scale.

### L2: Multistructural / block x execution / preoperational

L2 for mouse interaction: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

- **Edge:** `mouse_interaction` &rarr; `mouse_interaction@L2` (has_level)
- **Exact edge logic:** mouse interaction -&gt; L2 (Multistructural): the answer applies the rules of mouse interaction to every part of the code, in order (3 ways).

Ways (3), each with its exact rule:

- **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): Inside the animation loop: poll the mouse, update state from it, clear, draw, show(t). The mouse is sampled once per frame.
- **[1] output\_prediction** (rule type OP, evaluation / result rule): mousePressed() returns a boolean, and mouseX()/mouseY() return doubles in drawing coordinates (e.g. 0.5, 0.5 at the centre of the default canvas).
- **[2] one\_step\_execution** (rule type OS, state-transition rule): A poll changes no state and does not wait. It returns the current mouse state.

### L3: Relational / relations x function (concrete operational begins)

L3 for mouse interaction: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

- **Edge:** `mouse_interaction` &rarr; `mouse_interaction@L3` (has_level)
- **Exact edge logic:** mouse interaction -&gt; L3 (Relational): the answer relates the parts (2 ways).

Ways (2), each with its exact rule:

- **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Mouse checks run inside the frame loop. A click shorter than one frame (show(t) pause) can be missed.
- **[1] purpose\_of\_the\_whole** (rule type P, plan / role rule): Plan: polling loop. The mouse coordinates are most-recent holders updated every frame.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for mouse interaction: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

- **Edge:** `mouse_interaction` &rarr; `mouse_interaction@L4` (has_level)
- **Exact edge logic:** mouse interaction -&gt; L4 (Extended abstract): the answer reasons beyond the given code (3 ways).

Ways (3), each with its exact rule:

- **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `MouseIsEvent`: Changing the frame pause changes how responsive the program is to clicks, but not what a click does.
- **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Use mouse polling for interactive drawings and games built on StdDraw. For text dialogue, use StdIn.
- **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: mousePressed() does not block. Kind: silent logic error. Trigger class: Calling mousePressed() once outside a loop: it returns false before the user can click, and the click is ignored.

## Same topic

`mouse_interaction` belongs to the topic **Standard drawing and animation** (`topic1.5.e`). The topic also contains: `animation`, `coordinate_scaling`, `drawing_shapes`, `function_plotting`, `standard_drawing`.

## Rules of the concept (13)

- **Book** (SW-1.5, ): "Our standard draw library also includes methods so that the user can interact with the window using the mouse."
- **E** (folk-meaning rule): In the everyday sense, 'mouse pressed' is an event the program waits for. StdDraw.mousePressed() only reports whether the button is down at the moment of the call.
- **M** (wrong rule / right rule): MouseIsEvent: wrong: StdDraw.mousePressed() waits until the user clicks. \| right: mousePressed() returns immediately with true or false for that moment. To catch clicks, poll it on every frame of a loop.
- **T** (uneven-application rule): Points to LT (each frame polls mousePressed, mouseX and mouseY once). An uneven trace treats one poll as blocking, or reuses an old position on some frames.
- **N** (identity rule): Mouse interaction is the StdDraw input methods mousePressed(), mouseX() and mouseY(), which report the mouse state in user coordinates.
- **S** (declarative rule): mousePressed() returns whether the button is currently pressed. mouseX() and mouseY() return the latest pointer position in the current x/y scale.
- **LT** (operational sequencing rule): Inside the animation loop: poll the mouse, update state from it, clear, draw, show(t). The mouse is sampled once per frame.
- **OP** (evaluation / result rule): mousePressed() returns a boolean, and mouseX()/mouseY() return doubles in drawing coordinates (e.g. 0.5, 0.5 at the centre of the default canvas).
- **OS** (state-transition rule): A poll changes no state and does not wait. It returns the current mouse state.
- **R** (composition rule (with a neighbour)): with animation: Mouse checks run inside the frame loop. A click shorter than one frame (show(t) pause) can be missed.
- **P** (plan / role rule): Plan: polling loop. The mouse coordinates are most-recent holders updated every frame.
- **C** (conservation rule): Changing the frame pause changes how responsive the program is to clicks, but not what a click does.
- **D** (error rule): rule broken: mousePressed() does not block. (silent logic error)
- **X** (applicability rule): Use mouse polling for interactive drawings and games built on StdDraw. For text dialogue, use StdIn.

## How it is found in code and answers (reader block)

- **Aliases:** none
- **Code patterns:** `StdDraw\.(?:mousePressed|isMousePressed|mouseX|mouseY)\s*\(`
- **Operator symbols:** none
- **Java types:** none

## The whole prerequisite chain

- **Everything it builds on (16):** `animation`, `api`, `arithmetic_operators`, `boolean`, `boolean_expression`, `comparison_operators`, `data_type`, `expression`, `identifier`, `literal`, `logical_operators`, `method_call`, `primitive_type`, `standard_drawing`, `variable`, `while_loop`
- **Everything that builds on it (0):** nothing

## Every edge in this view and its exact edge logic (14)

All the edges drawn in the picture, in the order: prerequisite, parallel, misconception, error, has_level, contains.

**1. `animation` &rarr; `mouse_interaction`** (prerequisite)

- **Exact edge logic:** Mouse checks run inside the animation loop.
- **Grounding:** questionable
- **Composition rule (R) of `animation` with `mouse_interaction`:** Mouse state is polled once per frame inside the animation loop, so it is checked about every dt milliseconds.
- **Composition rule (R) of `mouse_interaction` with `animation`:** Mouse checks run inside the frame loop. A click shorter than one frame (show(t) pause) can be missed.

**2. `standard_drawing` &rarr; `mouse_interaction`** (prerequisite)

- **Exact edge logic:** Mouse position and clicks are read through StdDraw methods such as StdDraw.mousePressed().
- **Grounding:** order\_only

**3. `mouse_interaction` &rarr; `MouseIsEvent`** (misconception)

- **Exact edge logic (the wrong rule):** StdDraw.mousePressed() waits until the user clicks.
- **Twin logic (the right rule):** mousePressed() only reports whether the button is down at that moment, so it is checked repeatedly in a loop.
- **Role:** primary

**4. `mouse_interaction` &rarr; `mouse_interaction@L0`** (has_level)

- **Exact edge logic:** mouse interaction -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (3 ways).
  - **[0] everyday\_reading** (rule type E, folk-meaning rule): In the everyday sense, 'mouse pressed' is an event the program waits for. StdDraw.mousePressed() only reports whether the button is down at the moment of the call.
  - **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `MouseIsEvent`: wrong rule: StdDraw.mousePressed() waits until the user clicks. Right rule: mousePressed() returns immediately with true or false for that moment. To catch clicks, poll it on every frame of a loop.
  - **[2] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `MouseIsEvent`: Points to LT (each frame polls mousePressed, mouseX and mouseY once). An uneven trace treats one poll as blocking, or reuses an old position on some frames. (here mixing in: "StdDraw.mousePressed() waits until the user clicks")

**5. `mouse_interaction` &rarr; `mouse_interaction@L1`** (has_level)

- **Exact edge logic:** mouse interaction -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).
  - **[0] names\_the\_element** (rule type N, identity rule): Mouse interaction is the StdDraw input methods mousePressed(), mouseX() and mouseY(), which report the mouse state in user coordinates.
  - **[1] states\_the\_rule** (rule type S, declarative rule): mousePressed() returns whether the button is currently pressed. mouseX() and mouseY() return the latest pointer position in the current x/y scale.

**6. `mouse_interaction` &rarr; `mouse_interaction@L2`** (has_level)

- **Exact edge logic:** mouse interaction -&gt; L2 (Multistructural): the answer applies the rules of mouse interaction to every part of the code, in order (3 ways).
  - **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): Inside the animation loop: poll the mouse, update state from it, clear, draw, show(t). The mouse is sampled once per frame.
  - **[1] output\_prediction** (rule type OP, evaluation / result rule): mousePressed() returns a boolean, and mouseX()/mouseY() return doubles in drawing coordinates (e.g. 0.5, 0.5 at the centre of the default canvas).
  - **[2] one\_step\_execution** (rule type OS, state-transition rule): A poll changes no state and does not wait. It returns the current mouse state.

**7. `mouse_interaction` &rarr; `mouse_interaction@L3`** (has_level)

- **Exact edge logic:** mouse interaction -&gt; L3 (Relational): the answer relates the parts (2 ways).
  - **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Mouse checks run inside the frame loop. A click shorter than one frame (show(t) pause) can be missed.
  - **[1] purpose\_of\_the\_whole** (rule type P, plan / role rule): Plan: polling loop. The mouse coordinates are most-recent holders updated every frame.

**8. `mouse_interaction` &rarr; `mouse_interaction@L4`** (has_level)

- **Exact edge logic:** mouse interaction -&gt; L4 (Extended abstract): the answer reasons beyond the given code (3 ways).
  - **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `MouseIsEvent`: Changing the frame pause changes how responsive the program is to clicks, but not what a click does.
  - **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Use mouse polling for interactive drawings and games built on StdDraw. For text dialogue, use StdIn.
  - **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: mousePressed() does not block. Kind: silent logic error. Trigger class: Calling mousePressed() once outside a loop: it returns false before the user can click, and the click is ignored.

**9. `topic1.5.e` &rarr; `mouse_interaction`** (contains)

- topic `topic1.5.e` contains `mouse_interaction`

**10. `topic1.5.e` &rarr; `animation`** (contains)

- topic `topic1.5.e` contains `animation`

**11. `topic1.5.e` &rarr; `coordinate_scaling`** (contains)

- topic `topic1.5.e` contains `coordinate_scaling`

**12. `topic1.5.e` &rarr; `drawing_shapes`** (contains)

- topic `topic1.5.e` contains `drawing_shapes`

**13. `topic1.5.e` &rarr; `function_plotting`** (contains)

- topic `topic1.5.e` contains `function_plotting`

**14. `topic1.5.e` &rarr; `standard_drawing`** (contains)

- topic `topic1.5.e` contains `standard_drawing`
