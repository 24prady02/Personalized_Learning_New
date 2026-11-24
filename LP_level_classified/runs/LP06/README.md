# LP06: the overall level and how it was arrived at

This page explains, with the numbers of this run, how one overall level was worked out for this answer. Every step of the run itself (what the graph offered, the model's replies, all labels, all figures) is in the notebook [`LP06.ipynb`](LP06.ipynb) and in `report.html`.

## The answer that was read

```java
int i, n = 5;
for (i = 1; i < n; i++)
    i++;
    System.out.println(i);
System.out.println(i);
```

**Question.** What is printed? Explain, pass by pass, what happens to i.

**Student's answer.** It never stops. Each pass starts again with i = 1, so i goes 1, 2, 3 and back to 1, and the println lines are never reached.

**What this scenario was written to test.** L0: misconception.

## Result

- **Overall level: L0** (prestructural)
- **Decided by:** a real mistake is held, so the answer is L0 (step 3 below)
- **Expected by design:** L0. **Match: yes**

## The five levels

| Level | Name | What an answer at this level does |
|---|---|---|
| L0 | prestructural | holds a rule that contradicts Java, or reads the code in an everyday sense |
| L1 | unistructural | names a part or states one rule without applying it |
| L2 | multistructural | applies the rules to the code step by step (a trace, a predicted output, one step) |
| L3 | relational | relates the parts to each other or gives the purpose of the whole |
| L4 | extended abstract | reasons beyond the given code (a change, an error, a new program) |

A level is never asked from the model directly. For each concept the model only says which *ways* of showing a level the student's words show (for example "output prediction", which sits at L2) and which wrong rules the student holds. The level is then read off by fixed rules.

## Step 1. Which concepts were taken

Stage 1 read the program and found 12 concepts in it. Not all of them count for the overall level. A concept is taken as a **component** when two things hold:

- it is not a *generic* concept (one that almost every Java program has, such as `statement`), unless a real mistake is held on it;
- the student's answer shows something about it, so that it has a level.

| Concept | Generic | Level | Taken as a component? |
|---|---|---|---|
| `assignment` | yes | none | no: generic, and the answer shows nothing about it |
| `boolean_expression` |  | none | no: the answer shows nothing about it, so it has no level |
| `comparison_operators` |  | none | no: the answer shows nothing about it, so it has no level |
| `control_flow` |  | none | no: the answer shows nothing about it, so it has no level |
| `expression` | yes | none | no: generic, and the answer shows nothing about it |
| `for_loop` |  | L0 | **yes** |
| `increment_operators` |  | L2 | **yes** |
| `loop_body` |  | L0 | **yes** |
| `loop_control` |  | L0 | **yes** |
| `loop_variable` |  | L0 | **yes** |
| `println` |  | none | no: the answer shows nothing about it, so it has no level |
| `statement` | yes | none | no: generic, and the answer shows nothing about it |

**Components of this answer: 5.** `for_loop`, `increment_operators`, `loop_body`, `loop_control`, `loop_variable`.

![The concepts of this run, coloured by level](figure08.png)

*The concepts of this program and the links between them, after the run. A coloured concept has a level (red L0, orange L1, yellow L2, light green L3, green L4); a grey concept was found in the code but the answer shows nothing about it. A thick black outline marks the root cause, and a diamond is a wrong rule the student holds. The picture also colours generic concepts that have a level; the table above says which of them are counted.*

## Step 2. The level of each component

Each component gets its level by the first of these rules that fits:

- **(a)** a wrong rule (misconception) is held on the concept: **L0**, whatever else is shown;
- **(b)** only L0 ways are shown (everyday reading, inconsistent trace): **L0**;
- **(c)** otherwise the **highest** level at which a way is shown. One shown way is enough, because the levels build on each other.

A way above L2 is counted only when the model's confidence is above 0.60 and it does not rest only on the words of a held mistake.

### `for_loop`: L0

- **Rule (a).** The student holds the wrong rule **ForInitRepeats** on this concept.
- Wrong rule: "The initialization of a for loop runs again after a pass of the body."
- Right rule: "The initialization runs exactly once, before the first condition test."
- Student's words: "Each pass starts again with i = 1; so i goes 1, 2, 3 and back to 1, and the println lines are never reached"
- Ways also shown on this concept (they do not change the L0): L0 "inconsistent trace" (confidence 0.85).

### `increment_operators`: L2

- **Rule (c).** The highest way shown is **L2 "one step execution"**.
- Student's words: "so i goes 1, 2, 3 and back to 1, and the println lines are never reached"
- All ways shown on this concept: L2 "one step execution" (confidence 0.55).

### `loop_body`: L0

- **Rule (a).** The student holds the wrong rule **StateChangeIgnoredAcrossPasses** on this concept.
- Wrong rule: "Values changed by one pass of a loop (other than the loop variable) do not affect later passes."
- Right rule: "Each pass starts from the state left by the previous pass, so a change in one pass carries into the next ones."
- Student's words: "Each pass starts again with i = 1; so i goes 1, 2, 3 and back to 1, and the println lines are never reached"

### `loop_control`: L0

- **Rule (b).** Only L0 ways are shown: inconsistent trace.
- Student's words: "Each pass starts again with i = 1; so i goes 1, 2, 3 and back to 1, and the println lines are never reached"
- All ways shown on this concept: L0 "inconsistent trace" (confidence 0.85).
- The student does this kind of thing, but what is said is wrong in Java, so it is not counted: L3 "relation to neighbour".

### `loop_variable`: L0

- **Rule (b).** Only L0 ways are shown: inconsistent trace.
- Student's words: "Each pass starts again with i = 1; so i goes 1, 2, 3 and back to 1, and the println lines are never reached"
- All ways shown on this concept: L0 "inconsistent trace" (confidence 0.90).

## Step 3. Is a real mistake held?

A real mistake is a wrong rule (misconception) or a broken rule (error) that the student's own words show, after the same mistake found at two concepts has been counted once. If there is one, the walk also names the concept where the mistake starts, the **root cause**: among the concepts with a mistake, the one furthest back along the prerequisite links.

| Mistake | Kind | At concept | Student's words |
|---|---|---|---|
| ForInitRepeats | misconception | `for_loop` | Each pass starts again with i = 1; so i goes 1, 2, 3 and back to 1, and the println lines are never reached |
| StateChangeIgnoredAcrossPasses | misconception | `loop_body` | Each pass starts again with i = 1; so i goes 1, 2, 3 and back to 1, and the println lines are never reached |

- **ForInitRepeats.** Wrong rule: "The initialization of a for loop runs again after a pass of the body." Right rule: "The initialization runs exactly once, before the first condition test."
- **StateChangeIgnoredAcrossPasses.** Wrong rule: "Values changed by one pass of a loop (other than the loop variable) do not affect later passes." Right rule: "Each pass starts from the state left by the previous pass, so a change in one pass carries into the next ones."

Read a second time at another concept and therefore not counted again: LoopHeaderIsEquations at `loop_control`; ForInitRepeats at `loop_variable`.

**Yes.** Root cause: `for_loop`, with ForInitRepeats.

**Rule: an answer that is built on a wrong rule is L0, however well its other parts are done.** So the overall level is **L0**, and the count in step 4 is given for information only.

## Step 4. Count the components at each level

| Level | Components at this level | Number | Share |
|---|---|---|---|
| L0 | `for_loop`, `loop_body`, `loop_control`, `loop_variable` | 4 | 4 ÷ 5 = 0.80 |
| L2 | `increment_operators` | 1 | 1 ÷ 5 = 0.20 |

The largest share is at **L0** (4 of 5 components).

Because a real mistake is held (step 3), this count does not decide: the overall level stays **L0**.

## Step 5. How far apart are the components?

The lowest component level is L0 and the highest is L2: 2 − 0 = 2.

The components are two or more levels apart, so the answer is marked **LOW coherence**: the one overall level hides real differences between the parts, and the table of step 2 should be read with it.

## Conclusion

5 components; a real mistake is held (ForInitRepeats at `for_loop`); so the overall level is **L0**. Shares: L0 0.80, L2 0.20; LOW coherence.

| | Overall level | Components | Held mistake | Root cause |
|---|---|---|---|---|
| This run | L0 | `for_loop` L0, `increment_operators` L2, `loop_body` L0, `loop_control` L0, `loop_variable` L0 | ForInitRepeats, StateChangeIgnoredAcrossPasses | `for_loop` |
| Expected by design | L0 | `for_loop` L0 | ForInitRepeats | `for_loop` |

The expected result lists only the main concept the scenario was written for; the run levels every concept the answer touches, so it usually has more components.

The rule and how it was made are in the [folder README](../../README.md).
