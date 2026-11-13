# standard_audio (`standard_audio`)

StdAudio: sound as an array of samples

Section 1.5 Input and Output, topic 1.5.f Standard audio.

![The knowledge graph around standard_audio](standard_audio.png)

## At a glance

- **Needs first:** `api`, `function_plotting`, `math_library`
- **Leads to:** nothing
- **Learned alongside:** nothing
- **Misconceptions:** `AmplitudeIsPitch`, `AnyFrequencyPlayable`
- **Errors:** `AudioProgramHangs`, `StdLibraryNotInDirectory`
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 16 edges around this concept. The edge logic, the wrong and right rules and the exact rules of the ways are copied word for word from the graph.

## To work on (0)

Nothing is missing for this concept.

## What it needs first (3)

A prerequisite edge means the other concept has to be understood before `standard_audio`.

### `api` comes before `standard_audio`

*Application programming interface (API): a table of library methods giving each method's signature and a short description of what it computes*

- **Edge:** `pre:api->standard_audio`
- **Exact edge logic:** StdAudio is a library used through its API of static methods.
- **Grounding:** book\_passage

### `function_plotting` comes before `standard_audio`

*sampling a function and joining the points with lines*

- **Edge:** `pre:function_plotting->standard_audio`
- **Exact edge logic:** A sound wave is sampled at regular intervals exactly as a function is sampled for plotting, giving the array of samples that StdAudio plays.
- **Grounding:** book\_passage
- **Composition rule (R) of `standard_audio` with `function_plotting`:** Sampling for sound is the same as sampling for a plot. The same array can be sent to StdDraw and to StdAudio.
- **Composition rule (R) of `function_plotting` with `standard_audio`:** A sound wave is sampled at regular intervals in exactly the way a function is sampled for plotting. The same array can be drawn or played.

### `math_library` comes before `standard_audio`

*Math.abs, Math.sqrt, Math.max, Math.random, Math.round ...*

- **Edge:** `pre:math_library->standard_audio`
- **Exact edge logic:** To play a tone, each sample a[i] of the sound array is computed with Math.sin at evenly spaced times.
- **Grounding:** book\_passage
- **Composition rule (R) of `standard_audio` with `math_library`:** Each sample is computed with Math.sin at evenly spaced times t = i/sps. The note's frequency comes from Math.pow(2, pitch/12.0).
- **Composition rule (R) of `math_library` with `standard_audio`:** Each sample a[i] = Math.sin(2\*Math.PI \* i \* hz / sps) is taken at evenly spaced times; the 2\*Math.PI factor is needed because Math.sin works in radians, one cycle being 2 pi.

## What it leads to (0)

These concepts need `standard_audio` first.

No concept has this one as a prerequisite.

## Learned alongside (0)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

No parallel edge touches this concept.

## Misconceptions (2)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### AmplitudeIsPitch

- **Edge:** `standard_audio` &rarr; `AmplitudeIsPitch` (misconception)
- **Exact edge logic (the wrong rule):** Making the sample values larger raises the pitch of the note.
- **Twin logic (the right rule):** The amplitude (y-value) corresponds to the volume; the frequency sets the pitch.
- **Wrong belief (on the node):** Making the sample values larger raises the pitch of the note.
- **Correct rule (on the node):** The amplitude (y-value) corresponds to the volume; the frequency sets the pitch.
- **Provenance:** derived
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [1] misconception, exact rule:** wrong rule: Making the sample values larger raises the pitch of the note. Right rule: The amplitude (y-value) corresponds to the volume, and the frequency sets the pitch.
- **L0 way [3] inconsistent\_trace, exact rule:** Points to LT (compute N, allocate N+1 samples, fill a[i] = sin(2\*pi\*i\*hz/sps), then play). An uneven trace uses i/sps on some samples and i\*hz/sps on others, or plays before filling. (here mixing in: "Making the sample values larger raises the pitch of the note")

### AnyFrequencyPlayable

- **Edge:** `standard_audio` &rarr; `AnyFrequencyPlayable` (misconception)
- **Exact edge logic (the wrong rule):** A sine wave of any frequency, e.g. 30,000 Hz, plays correctly with StdAudio.
- **Twin logic (the right rule):** With 44,100 samples per second the highest frequency that can be reproduced is the Nyquist frequency, 22,050 Hz.
- **Wrong belief (on the node):** A sine wave of any frequency, e.g. 30,000 Hz, plays correctly with StdAudio.
- **Correct rule (on the node):** With 44,100 samples per second the highest frequency that can be reproduced is the Nyquist frequency, 22,050 Hz.
- **Provenance:** textbook
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [2] misconception, exact rule:** wrong rule: A sine wave of any frequency, e.g. 30,000 Hz, plays correctly with StdAudio. Right rule: At 44,100 samples per second the highest reproducible frequency is the Nyquist frequency, 22,050 Hz.

## Errors (2)

An error edge states the rule that gets broken in a program, and the right rule.

### AudioProgramHangs

- **Edge:** `standard_audio` &rarr; `AudioProgramHangs` (error)
- **Exact edge logic (the wrong rule):** Ends a StdAudio program with no System.exit(0), so the terminal hangs and needs &lt;ctrl-c&gt;.
- **Twin logic (the right rule):** In the book's setup, a program that uses StdAudio should end main() with System.exit(0).
- **Wrong belief (on the node):** Ends a StdAudio program with no System.exit(0), so the terminal hangs and needs &lt;ctrl-c&gt;.
- **Correct rule (on the node):** In the book's setup, a program that uses StdAudio should end main() with System.exit(0).
- **Provenance:** textbook
- **Role of this concept:** primary
- **Edge `run` &rarr; `AudioProgramHangs`, exact edge logic:** Ends a StdAudio program with no System.exit(0), so the terminal hangs and needs &lt;ctrl-c&gt;. **Twin logic:** In the book's setup, a program that uses StdAudio should end main() with System.exit(0). (role: context)

### StdLibraryNotInDirectory

- **Edge:** `standard_audio` &rarr; `StdLibraryNotInDirectory` (error)
- **Exact edge logic (the wrong rule):** Uses StdIn (or StdDraw/StdAudio) without StdIn.java in the working directory.
- **Twin logic (the right rule):** The Std\* libraries are not built into Java; StdIn.java etc. must be in the same directory (or on the classpath), otherwise Java reports NoClassDefFoundError.
- **Wrong belief (on the node):** Uses StdIn (or StdDraw/StdAudio) without StdIn.java in the working directory.
- **Correct rule (on the node):** The Std\* libraries are not built into Java; StdIn.java etc. must be in the same directory (or on the classpath), otherwise Java reports NoClassDefFoundError.
- **Provenance:** textbook
- **Role of this concept:** context
- **Edge `standard_drawing` &rarr; `StdLibraryNotInDirectory`, exact edge logic:** Uses StdIn (or StdDraw/StdAudio) without StdIn.java in the working directory. **Twin logic:** The Std\* libraries are not built into Java; StdIn.java etc. must be in the same directory (or on the classpath), otherwise Java reports NoClassDefFoundError. (role: context)
- **Edge `standard_input` &rarr; `StdLibraryNotInDirectory`, exact edge logic:** Uses StdIn (or StdDraw/StdAudio) without StdIn.java in the working directory. **Twin logic:** The Std\* libraries are not built into Java; StdIn.java etc. must be in the same directory (or on the classpath), otherwise Java reports NoClassDefFoundError. (role: primary)

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for standard audio: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to standard audio agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

- **Edge:** `standard_audio` &rarr; `standard_audio@L0` (has_level)
- **Exact edge logic:** standard audio -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (4 ways).

Ways (4), each with its exact rule:

- **[0] everyday\_reading** (rule type E, folk-meaning rule): Everyday intuition links 'bigger numbers' with a 'higher note'. In digital sound the sample amplitude (y-value) sets the volume, and the frequency of oscillation sets the pitch (doubling it raises the note an octave).
- **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `AmplitudeIsPitch`: wrong rule: Making the sample values larger raises the pitch of the note. Right rule: The amplitude (y-value) corresponds to the volume, and the frequency sets the pitch.
- **[2] misconception** (rule type M, wrong rule / right rule) &rarr; `AnyFrequencyPlayable`: wrong rule: A sine wave of any frequency, e.g. 30,000 Hz, plays correctly with StdAudio. Right rule: At 44,100 samples per second the highest reproducible frequency is the Nyquist frequency, 22,050 Hz.
- **[3] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `AmplitudeIsPitch`: Points to LT (compute N, allocate N+1 samples, fill a[i] = sin(2\*pi\*i\*hz/sps), then play). An uneven trace uses i/sps on some samples and i\*hz/sps on others, or plays before filling. (here mixing in: "Making the sample values larger raises the pitch of the note")

### L1: Unistructural / atom x text surface

L1 for standard audio: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

- **Edge:** `standard_audio` &rarr; `standard_audio@L1` (has_level)
- **Exact edge logic:** standard audio -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

Ways (2), each with its exact rule:

- **[0] names\_the\_element** (rule type N, identity rule): StdAudio is a booksite library for playing, saving and reading sound, which it represents as an array of samples.
- **[1] states\_the\_rule** (rule type S, declarative rule): Sound is an array of doubles between -1 and +1, sampled 44,100 times per second. StdAudio.play(double[] a) plays the sound that the array represents.

### L2: Multistructural / block x execution / preoperational

L2 for standard audio: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

- **Edge:** `standard_audio` &rarr; `standard_audio@L2` (has_level)
- **Exact edge logic:** standard audio -&gt; L2 (Multistructural): the answer applies the rules of standard audio to every part of the code, in order (3 ways).

Ways (3), each with its exact rule:

- **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): N = (int) (sps \* duration), a = new double[N+1], then for i = 0..N a[i] = Math.sin(2\*Math.PI\*i\*hz/sps), then StdAudio.play(a). The samples sound in index order, 44,100 per second.
- **[1] output\_prediction** (rule type OP, evaluation / result rule): Ten seconds of concert A (440 Hz) needs 441,001 sample values, and each one is in [-1, 1]. play is void: its result is sound.
- **[2] one\_step\_execution** (rule type OS, state-transition rule): play(a) plays a.length/44,100 seconds of sound and leaves a unchanged. play(double x) plays one sample for 1/44,100 second. save writes a .wav file and read returns an array.

### L3: Relational / relations x function (concrete operational begins)

L3 for standard audio: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

- **Edge:** `standard_audio` &rarr; `standard_audio@L3` (has_level)
- **Exact edge logic:** standard audio -&gt; L3 (Relational): the answer relates the parts (3 ways).

Ways (3), each with its exact rule:

- **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Each sample is computed with Math.sin at evenly spaced times t = i/sps. The note's frequency comes from Math.pow(2, pitch/12.0).
- **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Sampling for sound is the same as sampling for a plot. The same array can be sent to StdDraw and to StdAudio.
- **[2] purpose\_of\_the\_whole** (rule type P, plan / role rule): Plan: sample-and-play synthesis. In PlayThatTune it is driven by data: a loop reads (pitch, duration) pairs and plays each note.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for standard audio: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

- **Edge:** `standard_audio` &rarr; `standard_audio@L4` (has_level)
- **Exact edge logic:** standard audio -&gt; L4 (Extended abstract): the answer reasons beyond the given code (5 ways).

Ways (5), each with its exact rule:

- **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `AmplitudeIsPitch`: Doubling hz moves the note up an octave and keeps the duration. Multiplying all samples by a factor below 1 changes only the volume. Writing pitch / 12 (integer division) instead of pitch / 12.0 breaks the pitch.
- **[1] diagnose\_an\_error** (rule type D, error rule): rule broken: In the book's setup a StdAudio program should end main() with System.exit(0). Kind: silent logic error. Trigger class: A StdAudio program without System.exit(0): after the sound ends, the terminal does not return to a prompt and needs &lt;ctrl-c&gt;.
- **[2] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Use StdAudio to synthesize or sonify sampled data (tones, tunes, signal processing). Long recordings are stored in binary .wav files, not as text streams.
- **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: StdAudio.java must be in the working directory or on the classpath. Kind: run-time exception. Trigger class: StdAudio.class is absent at run time: NoClassDefFoundError (javac reports 'cannot find symbol' at compile time).
- **[4] diagnose\_an\_error** (rule type D, error rule): rule broken: Frequencies must stay below the Nyquist frequency, 22,050 Hz. Kind: silent logic error. Trigger class: Sonifying a 30,000 Hz sine wave gives weird (aliased) sound.

## Same topic

`standard_audio` belongs to the topic **Standard audio** (`topic1.5.f`). It is the only concept of that topic.

## Rules of the concept (17)

- **Book** (SW-1e, p. 148 (pdf 158)): "we represent sound as an array of numbers"
- **Book** (SW-1e, p. 148 (pdf 158)): "Our standard sound library method StdAudio.play() takes an array as its argument and plays the sound represented by that array on your computer."
- **Book** (SW-1.5, p. 148 (pdf 158)): "It is that simple: we represent sound as an array of numbers"
- **E** (folk-meaning rule): Everyday intuition links 'bigger numbers' with a 'higher note'. In digital sound the sample amplitude (y-value) sets the volume, and the frequency of oscillation sets the pitch (doubling it raises the note an octave).
- **M** (wrong rule / right rule): AmplitudeIsPitch: wrong: Making the sample values larger raises the pitch of the note. \| right: The amplitude (y-value) corresponds to the volume, and the frequency sets the pitch.
- **M** (wrong rule / right rule): AnyFrequencyPlayable: wrong: A sine wave of any frequency, e.g. 30,000 Hz, plays correctly with StdAudio. \| right: At 44,100 samples per second the highest reproducible frequency is the Nyquist frequency, 22,050 Hz.
- **T** (uneven-application rule): Points to LT (compute N, allocate N+1 samples, fill a[i] = sin(2\*pi\*i\*hz/sps), then play). An uneven trace uses i/sps on some samples and i\*hz/sps on others, or plays before filling.
- **N** (identity rule): StdAudio is a booksite library for playing, saving and reading sound, which it represents as an array of samples.
- **S** (declarative rule): Sound is an array of doubles between -1 and +1, sampled 44,100 times per second. StdAudio.play(double[] a) plays the sound that the array represents.
- **LT** (operational sequencing rule): N = (int) (sps \* duration), a = new double[N+1], then for i = 0..N a[i] = Math.sin(2\*Math.PI\*i\*hz/sps), then StdAudio.play(a). The samples sound in index order, 44,100 per second.
- **OP** (evaluation / result rule): Ten seconds of concert A (440 Hz) needs 441,001 sample values, and each one is in [-1, 1]. play is void: its result is sound.
- **OS** (state-transition rule): play(a) plays a.length/44,100 seconds of sound and leaves a unchanged. play(double x) plays one sample for 1/44,100 second. save writes a .wav file and read returns an array.
- **R** (composition rule (with a neighbour)): with math\_library: Each sample is computed with Math.sin at evenly spaced times t = i/sps. The note's frequency comes from Math.pow(2, pitch/12.0).
- **R** (composition rule (with a neighbour)): with function\_plotting: Sampling for sound is the same as sampling for a plot. The same array can be sent to StdDraw and to StdAudio.
- **P** (plan / role rule): Plan: sample-and-play synthesis. In PlayThatTune it is driven by data: a loop reads (pitch, duration) pairs and plays each note.
- **C** (conservation rule): Doubling hz moves the note up an octave and keeps the duration. Multiplying all samples by a factor below 1 changes only the volume. Writing pitch / 12 (integer division) instead of pitch / 12.0 breaks the pitch.
- **D** (error rule): rule broken: StdAudio.java must be in the working directory or on the classpath. (run-time exception)
- **D** (error rule): rule broken: In the book's setup a StdAudio program should end main() with System.exit(0). (silent logic error)
- **D** (error rule): rule broken: Frequencies must stay below the Nyquist frequency, 22,050 Hz. (silent logic error)
- **X** (applicability rule): Use StdAudio to synthesize or sonify sampled data (tones, tunes, signal processing). Long recordings are stored in binary .wav files, not as text streams.

## How it is found in code and answers (reader block)

- **Aliases:** stdaudio, standard audio
- **Code patterns:** `StdAudio\.`
- **Operator symbols:** none
- **Java types:** none

## The whole prerequisite chain

- **Everything it builds on (29):** `api`, `arithmetic_operators`, `array_creation`, `array_declaration`, `array_initializer`, `array_traversal`, `boolean`, `boolean_expression`, `comparison_operators`, `coordinate_scaling`, `data_structure`, `data_type`, `do_while_loop`, `expression`, `for_loop`, `function_plotting`, `identifier`, `indexing`, `length_field`, `literal`, `logical_operators`, `loop_control`, `loop_variable`, `math_library`, `method_call`, `primitive_type`, `standard_drawing`, `variable`, `while_loop`
- **Everything that builds on it (0):** nothing

## Every edge in this view and its exact edge logic (16)

All the edges drawn in the picture, in the order: prerequisite, parallel, misconception, error, has_level, contains.

**1. `api` &rarr; `standard_audio`** (prerequisite)

- **Exact edge logic:** StdAudio is a library used through its API of static methods.
- **Grounding:** book\_passage

**2. `function_plotting` &rarr; `standard_audio`** (prerequisite)

- **Exact edge logic:** A sound wave is sampled at regular intervals exactly as a function is sampled for plotting, giving the array of samples that StdAudio plays.
- **Grounding:** book\_passage
- **Composition rule (R) of `function_plotting` with `standard_audio`:** A sound wave is sampled at regular intervals in exactly the way a function is sampled for plotting. The same array can be drawn or played.
- **Composition rule (R) of `standard_audio` with `function_plotting`:** Sampling for sound is the same as sampling for a plot. The same array can be sent to StdDraw and to StdAudio.

**3. `math_library` &rarr; `standard_audio`** (prerequisite)

- **Exact edge logic:** To play a tone, each sample a[i] of the sound array is computed with Math.sin at evenly spaced times.
- **Grounding:** book\_passage
- **Composition rule (R) of `math_library` with `standard_audio`:** Each sample a[i] = Math.sin(2\*Math.PI \* i \* hz / sps) is taken at evenly spaced times; the 2\*Math.PI factor is needed because Math.sin works in radians, one cycle being 2 pi.
- **Composition rule (R) of `standard_audio` with `math_library`:** Each sample is computed with Math.sin at evenly spaced times t = i/sps. The note's frequency comes from Math.pow(2, pitch/12.0).

**4. `standard_audio` &rarr; `AmplitudeIsPitch`** (misconception)

- **Exact edge logic (the wrong rule):** Making the sample values larger raises the pitch of the note.
- **Twin logic (the right rule):** The amplitude (y-value) corresponds to the volume; the frequency sets the pitch.
- **Role:** primary

**5. `standard_audio` &rarr; `AnyFrequencyPlayable`** (misconception)

- **Exact edge logic (the wrong rule):** A sine wave of any frequency, e.g. 30,000 Hz, plays correctly with StdAudio.
- **Twin logic (the right rule):** With 44,100 samples per second the highest frequency that can be reproduced is the Nyquist frequency, 22,050 Hz.
- **Role:** primary

**6. `standard_audio` &rarr; `AudioProgramHangs`** (error)

- **Exact edge logic (the wrong rule):** Ends a StdAudio program with no System.exit(0), so the terminal hangs and needs &lt;ctrl-c&gt;.
- **Twin logic (the right rule):** In the book's setup, a program that uses StdAudio should end main() with System.exit(0).
- **Role:** primary

**7. `standard_audio` &rarr; `StdLibraryNotInDirectory`** (error)

- **Exact edge logic (the wrong rule):** Uses StdIn (or StdDraw/StdAudio) without StdIn.java in the working directory.
- **Twin logic (the right rule):** The Std\* libraries are not built into Java; StdIn.java etc. must be in the same directory (or on the classpath), otherwise Java reports NoClassDefFoundError.
- **Role:** context

**8. `run` &rarr; `AudioProgramHangs`** (error)

- **Exact edge logic (the wrong rule):** Ends a StdAudio program with no System.exit(0), so the terminal hangs and needs &lt;ctrl-c&gt;.
- **Twin logic (the right rule):** In the book's setup, a program that uses StdAudio should end main() with System.exit(0).
- **Role:** context

**9. `standard_drawing` &rarr; `StdLibraryNotInDirectory`** (error)

- **Exact edge logic (the wrong rule):** Uses StdIn (or StdDraw/StdAudio) without StdIn.java in the working directory.
- **Twin logic (the right rule):** The Std\* libraries are not built into Java; StdIn.java etc. must be in the same directory (or on the classpath), otherwise Java reports NoClassDefFoundError.
- **Role:** context

**10. `standard_input` &rarr; `StdLibraryNotInDirectory`** (error)

- **Exact edge logic (the wrong rule):** Uses StdIn (or StdDraw/StdAudio) without StdIn.java in the working directory.
- **Twin logic (the right rule):** The Std\* libraries are not built into Java; StdIn.java etc. must be in the same directory (or on the classpath), otherwise Java reports NoClassDefFoundError.
- **Role:** primary

**11. `standard_audio` &rarr; `standard_audio@L0`** (has_level)

- **Exact edge logic:** standard audio -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (4 ways).
  - **[0] everyday\_reading** (rule type E, folk-meaning rule): Everyday intuition links 'bigger numbers' with a 'higher note'. In digital sound the sample amplitude (y-value) sets the volume, and the frequency of oscillation sets the pitch (doubling it raises the note an octave).
  - **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `AmplitudeIsPitch`: wrong rule: Making the sample values larger raises the pitch of the note. Right rule: The amplitude (y-value) corresponds to the volume, and the frequency sets the pitch.
  - **[2] misconception** (rule type M, wrong rule / right rule) &rarr; `AnyFrequencyPlayable`: wrong rule: A sine wave of any frequency, e.g. 30,000 Hz, plays correctly with StdAudio. Right rule: At 44,100 samples per second the highest reproducible frequency is the Nyquist frequency, 22,050 Hz.
  - **[3] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `AmplitudeIsPitch`: Points to LT (compute N, allocate N+1 samples, fill a[i] = sin(2\*pi\*i\*hz/sps), then play). An uneven trace uses i/sps on some samples and i\*hz/sps on others, or plays before filling. (here mixing in: "Making the sample values larger raises the pitch of the note")

**12. `standard_audio` &rarr; `standard_audio@L1`** (has_level)

- **Exact edge logic:** standard audio -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).
  - **[0] names\_the\_element** (rule type N, identity rule): StdAudio is a booksite library for playing, saving and reading sound, which it represents as an array of samples.
  - **[1] states\_the\_rule** (rule type S, declarative rule): Sound is an array of doubles between -1 and +1, sampled 44,100 times per second. StdAudio.play(double[] a) plays the sound that the array represents.

**13. `standard_audio` &rarr; `standard_audio@L2`** (has_level)

- **Exact edge logic:** standard audio -&gt; L2 (Multistructural): the answer applies the rules of standard audio to every part of the code, in order (3 ways).
  - **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): N = (int) (sps \* duration), a = new double[N+1], then for i = 0..N a[i] = Math.sin(2\*Math.PI\*i\*hz/sps), then StdAudio.play(a). The samples sound in index order, 44,100 per second.
  - **[1] output\_prediction** (rule type OP, evaluation / result rule): Ten seconds of concert A (440 Hz) needs 441,001 sample values, and each one is in [-1, 1]. play is void: its result is sound.
  - **[2] one\_step\_execution** (rule type OS, state-transition rule): play(a) plays a.length/44,100 seconds of sound and leaves a unchanged. play(double x) plays one sample for 1/44,100 second. save writes a .wav file and read returns an array.

**14. `standard_audio` &rarr; `standard_audio@L3`** (has_level)

- **Exact edge logic:** standard audio -&gt; L3 (Relational): the answer relates the parts (3 ways).
  - **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Each sample is computed with Math.sin at evenly spaced times t = i/sps. The note's frequency comes from Math.pow(2, pitch/12.0).
  - **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Sampling for sound is the same as sampling for a plot. The same array can be sent to StdDraw and to StdAudio.
  - **[2] purpose\_of\_the\_whole** (rule type P, plan / role rule): Plan: sample-and-play synthesis. In PlayThatTune it is driven by data: a loop reads (pitch, duration) pairs and plays each note.

**15. `standard_audio` &rarr; `standard_audio@L4`** (has_level)

- **Exact edge logic:** standard audio -&gt; L4 (Extended abstract): the answer reasons beyond the given code (5 ways).
  - **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `AmplitudeIsPitch`: Doubling hz moves the note up an octave and keeps the duration. Multiplying all samples by a factor below 1 changes only the volume. Writing pitch / 12 (integer division) instead of pitch / 12.0 breaks the pitch.
  - **[1] diagnose\_an\_error** (rule type D, error rule): rule broken: In the book's setup a StdAudio program should end main() with System.exit(0). Kind: silent logic error. Trigger class: A StdAudio program without System.exit(0): after the sound ends, the terminal does not return to a prompt and needs &lt;ctrl-c&gt;.
  - **[2] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Use StdAudio to synthesize or sonify sampled data (tones, tunes, signal processing). Long recordings are stored in binary .wav files, not as text streams.
  - **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: StdAudio.java must be in the working directory or on the classpath. Kind: run-time exception. Trigger class: StdAudio.class is absent at run time: NoClassDefFoundError (javac reports 'cannot find symbol' at compile time).
  - **[4] diagnose\_an\_error** (rule type D, error rule): rule broken: Frequencies must stay below the Nyquist frequency, 22,050 Hz. Kind: silent logic error. Trigger class: Sonifying a 30,000 Hz sine wave gives weird (aliased) sound.

**16. `topic1.5.f` &rarr; `standard_audio`** (contains)

- topic `topic1.5.f` contains `standard_audio`
