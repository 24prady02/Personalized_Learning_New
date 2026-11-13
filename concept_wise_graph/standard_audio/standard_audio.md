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

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 16 edges around this concept, each explained in the graph's own words.

## What it needs first (3)

A prerequisite edge means the other concept has to be understood before `standard_audio`.

### `api` comes before `standard_audio`

*Application programming interface (API): a table of library methods giving each method's signature and a short description of what it computes*

StdAudio is a library used through its API of static methods.

- **Grounding:** book passage

### `function_plotting` comes before `standard_audio`

*sampling a function and joining the points with lines*

A sound wave is sampled at regular intervals exactly as a function is sampled for plotting, giving the array of samples that StdAudio plays.

- **Grounding:** book passage
- **How `standard_audio` combines with `function_plotting`:** Sampling for sound is the same as sampling for a plot. The same array can be sent to StdDraw and to StdAudio.
- **How `function_plotting` combines with `standard_audio`:** A sound wave is sampled at regular intervals in exactly the way a function is sampled for plotting. The same array can be drawn or played.

### `math_library` comes before `standard_audio`

*Math.abs, Math.sqrt, Math.max, Math.random, Math.round ...*

To play a tone, each sample a[i] of the sound array is computed with Math.sin at evenly spaced times.

- **Grounding:** book passage
- **How `standard_audio` combines with `math_library`:** Each sample is computed with Math.sin at evenly spaced times t = i/sps. The note's frequency comes from Math.pow(2, pitch/12.0).
- **How `math_library` combines with `standard_audio`:** Each sample a[i] = Math.sin(2\*Math.PI \* i \* hz / sps) is taken at evenly spaced times; the 2\*Math.PI factor is needed because Math.sin works in radians, one cycle being 2 pi.

## What it leads to (0)

These concepts need `standard_audio` first.

No concept has this one as a prerequisite.

## Learned alongside (0)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

No parallel edge touches this concept.

## Misconceptions (2)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### AmplitudeIsPitch

- **Wrong rule:** Making the sample values larger raises the pitch of the note.
- **Right rule:** The amplitude (y-value) corresponds to the volume; the frequency sets the pitch.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: Making the sample values larger raises the pitch of the note. Right rule: The amplitude (y-value) corresponds to the volume, and the frequency sets the pitch.
- **Shows at level L0 as:** inconsistent trace: Points to LT (compute N, allocate N+1 samples, fill a[i] = sin(2\*pi\*i\*hz/sps), then play). An uneven trace uses i/sps on some samples and i\*hz/sps on others, or plays before filling. (here mixing in: "Making the sample values larger raises the pitch of the note")

### AnyFrequencyPlayable

- **Wrong rule:** A sine wave of any frequency, e.g. 30,000 Hz, plays correctly with StdAudio.
- **Right rule:** With 44,100 samples per second the highest frequency that can be reproduced is the Nyquist frequency, 22,050 Hz.
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: A sine wave of any frequency, e.g. 30,000 Hz, plays correctly with StdAudio. Right rule: At 44,100 samples per second the highest reproducible frequency is the Nyquist frequency, 22,050 Hz.

## Errors (2)

An error edge states the rule that gets broken in a program, and the right rule.

### AudioProgramHangs

- **Wrong rule:** Ends a StdAudio program with no System.exit(0), so the terminal hangs and needs &lt;ctrl-c&gt;.
- **Right rule:** In the book's setup, a program that uses StdAudio should end main() with System.exit(0).
- **Role of this concept:** primary
- **Also an edge from `run`:** Ends a StdAudio program with no System.exit(0), so the terminal hangs and needs &lt;ctrl-c&gt;.

### StdLibraryNotInDirectory

- **Wrong rule:** Uses StdIn (or StdDraw/StdAudio) without StdIn.java in the working directory.
- **Right rule:** The Std\* libraries are not built into Java; StdIn.java etc. must be in the same directory (or on the classpath), otherwise Java reports NoClassDefFoundError.
- **Role of this concept:** context
- **Also an edge from `standard_drawing`:** Uses StdIn (or StdDraw/StdAudio) without StdIn.java in the working directory.
- **Also an edge from `standard_input`:** Uses StdIn (or StdDraw/StdAudio) without StdIn.java in the working directory.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for standard audio: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to standard audio agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

standard audio -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (4 ways).

- **everyday reading** (folk-meaning rule): Everyday intuition links 'bigger numbers' with a 'higher note'. In digital sound the sample amplitude (y-value) sets the volume, and the frequency of oscillation sets the pitch (doubling it raises the note an octave).
- **misconception** (wrong rule / right rule; shows `AmplitudeIsPitch`): wrong rule: Making the sample values larger raises the pitch of the note. Right rule: The amplitude (y-value) corresponds to the volume, and the frequency sets the pitch.
- **misconception** (wrong rule / right rule; shows `AnyFrequencyPlayable`): wrong rule: A sine wave of any frequency, e.g. 30,000 Hz, plays correctly with StdAudio. Right rule: At 44,100 samples per second the highest reproducible frequency is the Nyquist frequency, 22,050 Hz.
- **inconsistent trace** (uneven-application rule; shows `AmplitudeIsPitch`): Points to LT (compute N, allocate N+1 samples, fill a[i] = sin(2\*pi\*i\*hz/sps), then play). An uneven trace uses i/sps on some samples and i\*hz/sps on others, or plays before filling. (here mixing in: "Making the sample values larger raises the pitch of the note")

### L1: Unistructural / atom x text surface

L1 for standard audio: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

standard audio -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

- **names the element** (identity rule): StdAudio is a booksite library for playing, saving and reading sound, which it represents as an array of samples.
- **states the rule** (declarative rule): Sound is an array of doubles between -1 and +1, sampled 44,100 times per second. StdAudio.play(double[] a) plays the sound that the array represents.

### L2: Multistructural / block x execution / preoperational

L2 for standard audio: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

standard audio -&gt; L2 (Multistructural): the answer applies the rules of standard audio to every part of the code, in order (3 ways).

- **line by line trace** (operational sequencing rule): N = (int) (sps \* duration), a = new double[N+1], then for i = 0..N a[i] = Math.sin(2\*Math.PI\*i\*hz/sps), then StdAudio.play(a). The samples sound in index order, 44,100 per second.
- **output prediction** (evaluation / result rule): Ten seconds of concert A (440 Hz) needs 441,001 sample values, and each one is in [-1, 1]. play is void: its result is sound.
- **one step execution** (state-transition rule): play(a) plays a.length/44,100 seconds of sound and leaves a unchanged. play(double x) plays one sample for 1/44,100 second. save writes a .wav file and read returns an array.

### L3: Relational / relations x function (concrete operational begins)

L3 for standard audio: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

standard audio -&gt; L3 (Relational): the answer relates the parts (3 ways).

- **relation to neighbour** (composition rule (with a neighbour)): Each sample is computed with Math.sin at evenly spaced times t = i/sps. The note's frequency comes from Math.pow(2, pitch/12.0).
- **relation to neighbour** (composition rule (with a neighbour)): Sampling for sound is the same as sampling for a plot. The same array can be sent to StdDraw and to StdAudio.
- **purpose of the whole** (plan / role rule): Plan: sample-and-play synthesis. In PlayThatTune it is driven by data: a loop reads (pitch, duration) pairs and plays each note.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for standard audio: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

standard audio -&gt; L4 (Extended abstract): the answer reasons beyond the given code (5 ways).

- **predict a change** (conservation rule; shows `AmplitudeIsPitch`): Doubling hz moves the note up an octave and keeps the duration. Multiplying all samples by a factor below 1 changes only the volume. Writing pitch / 12 (integer division) instead of pitch / 12.0 breaks the pitch.
- **diagnose an error** (error rule): rule broken: In the book's setup a StdAudio program should end main() with System.exit(0). Kind: silent logic error. Trigger class: A StdAudio program without System.exit(0): after the sound ends, the terminal does not return to a prompt and needs &lt;ctrl-c&gt;.
- **transfer to a new program** (applicability rule): Use StdAudio to synthesize or sonify sampled data (tones, tunes, signal processing). Long recordings are stored in binary .wav files, not as text streams.
- **diagnose an error** (error rule): rule broken: StdAudio.java must be in the working directory or on the classpath. Kind: run-time exception. Trigger class: StdAudio.class is absent at run time: NoClassDefFoundError (javac reports 'cannot find symbol' at compile time).
- **diagnose an error** (error rule): rule broken: Frequencies must stay below the Nyquist frequency, 22,050 Hz. Kind: silent logic error. Trigger class: Sonifying a 30,000 Hz sine wave gives weird (aliased) sound.

## Same topic

`standard_audio` belongs to the topic **Standard audio** (`topic1.5.f`). It is the only concept of that topic.

## Rules of the concept (17)

- **folk-meaning rule:** Everyday intuition links 'bigger numbers' with a 'higher note'. In digital sound the sample amplitude (y-value) sets the volume, and the frequency of oscillation sets the pitch (doubling it raises the note an octave).
- **wrong rule / right rule:** AmplitudeIsPitch: wrong: Making the sample values larger raises the pitch of the note. \| right: The amplitude (y-value) corresponds to the volume, and the frequency sets the pitch.
- **wrong rule / right rule:** AnyFrequencyPlayable: wrong: A sine wave of any frequency, e.g. 30,000 Hz, plays correctly with StdAudio. \| right: At 44,100 samples per second the highest reproducible frequency is the Nyquist frequency, 22,050 Hz.
- **uneven-application rule:** Points to LT (compute N, allocate N+1 samples, fill a[i] = sin(2\*pi\*i\*hz/sps), then play). An uneven trace uses i/sps on some samples and i\*hz/sps on others, or plays before filling.
- **identity rule:** StdAudio is a booksite library for playing, saving and reading sound, which it represents as an array of samples.
- **declarative rule:** Sound is an array of doubles between -1 and +1, sampled 44,100 times per second. StdAudio.play(double[] a) plays the sound that the array represents.
- **operational sequencing rule:** N = (int) (sps \* duration), a = new double[N+1], then for i = 0..N a[i] = Math.sin(2\*Math.PI\*i\*hz/sps), then StdAudio.play(a). The samples sound in index order, 44,100 per second.
- **evaluation / result rule:** Ten seconds of concert A (440 Hz) needs 441,001 sample values, and each one is in [-1, 1]. play is void: its result is sound.
- **state-transition rule:** play(a) plays a.length/44,100 seconds of sound and leaves a unchanged. play(double x) plays one sample for 1/44,100 second. save writes a .wav file and read returns an array.
- **composition rule (with a neighbour):** with math\_library: Each sample is computed with Math.sin at evenly spaced times t = i/sps. The note's frequency comes from Math.pow(2, pitch/12.0).
- **composition rule (with a neighbour):** with function\_plotting: Sampling for sound is the same as sampling for a plot. The same array can be sent to StdDraw and to StdAudio.
- **plan / role rule:** Plan: sample-and-play synthesis. In PlayThatTune it is driven by data: a loop reads (pitch, duration) pairs and plays each note.
- **conservation rule:** Doubling hz moves the note up an octave and keeps the duration. Multiplying all samples by a factor below 1 changes only the volume. Writing pitch / 12 (integer division) instead of pitch / 12.0 breaks the pitch.
- **error rule:** rule broken: StdAudio.java must be in the working directory or on the classpath. (run-time exception)
- **error rule:** rule broken: In the book's setup a StdAudio program should end main() with System.exit(0). (silent logic error)
- **error rule:** rule broken: Frequencies must stay below the Nyquist frequency, 22,050 Hz. (silent logic error)
- **applicability rule:** Use StdAudio to synthesize or sonify sampled data (tones, tunes, signal processing). Long recordings are stored in binary .wav files, not as text streams.

## The whole prerequisite chain

- **Everything it builds on (29):** `api`, `arithmetic_operators`, `array_creation`, `array_declaration`, `array_initializer`, `array_traversal`, `boolean`, `boolean_expression`, `comparison_operators`, `coordinate_scaling`, `data_structure`, `data_type`, `do_while_loop`, `expression`, `for_loop`, `function_plotting`, `identifier`, `indexing`, `length_field`, `literal`, `logical_operators`, `loop_control`, `loop_variable`, `math_library`, `method_call`, `primitive_type`, `standard_drawing`, `variable`, `while_loop`
- **Everything that builds on it (0):** nothing
