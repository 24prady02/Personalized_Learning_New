# LP08: the overall level and how it was arrived at

This page explains, with the numbers of this run, how one overall level was worked out for this answer. Every step of the run itself (what the graph offered, the model's replies, all labels, all figures) is in the notebook [`LP08.ipynb`](LP08.ipynb) and in `report.html`.

## The answer that was read

```java
int i, n = 5;
for (i = 1; i < n; i++)
    i++;
    System.out.println(i);
System.out.println(i);
```

**Question.** How many times is System.out.println executed? Explain your reasoning.

**Student's answer.** The program has two System.out.println statements and one for loop. The for loop has a header with a start, a condition and an update, and a body.

**What this scenario was written to test.** L1: names the element.

## Result

- **Overall level: L1** (unistructural)
- **Decided by:** no mistake is held, so the level that most components have (step 4 below)
- **Expected by design:** L1. **Match: yes**

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
| `control_flow` |  | L1 | **yes** |
| `expression` | yes | none | no: generic, and the answer shows nothing about it |
| `for_loop` |  | L1 | **yes** |
| `increment_operators` |  | none | no: the answer shows nothing about it, so it has no level |
| `loop_body` |  | L1 | **yes** |
| `loop_control` |  | L1 | **yes** |
| `loop_variable` |  | none | no: the answer shows nothing about it, so it has no level |
| `println` |  | L1 | **yes** |
| `statement` | yes | none | no: generic, and the answer shows nothing about it |

**Components of this answer: 5.** `control_flow`, `for_loop`, `loop_body`, `loop_control`, `println`.

![The concepts of this run, coloured by level](figure07.png)

*The concepts of this program and the links between them, after the run. A coloured concept has a level (red L0, orange L1, yellow L2, light green L3, green L4); a grey concept was found in the code but the answer shows nothing about it. A thick black outline marks the root cause, and a diamond is a wrong rule the student holds. The picture also colours generic concepts that have a level; the table above says which of them are counted.*

## Step 2. The level of each component

Each component gets its level by the first of these rules that fits:

- **(a)** a wrong rule (misconception) is held on the concept: **L0**, whatever else is shown;
- **(b)** only L0 ways are shown (everyday reading, inconsistent trace): **L0**;
- **(c)** otherwise the **highest** level at which a way is shown. One shown way is enough, because the levels build on each other.

A way above L2 is counted only when the model's confidence is above 0.60 and it does not rest only on the words of a held mistake.

### `control_flow`: L1

- **Rule (c).** The highest way shown is **L1 "names the element"**.
- Student's words: "The program has two System.out.println statements and one for loop; The for loop has a header with a start, a condition and an update, and a body"
- All ways shown on this concept: L1 "names the element" (confidence 0.60).

### `for_loop`: L1

- **Rule (c).** The highest way shown is **L1 "names the element"**.
- Student's words: "The for loop has a header with a start, a condition and an update, and a body"
- All ways shown on this concept: L1 "names the element" (confidence 0.85); L1 "states the rule" (confidence 0.65).

### `loop_body`: L1

- **Rule (c).** The highest way shown is **L1 "names the element"**.
- Student's words: "The for loop has a header with a start, a condition and an update, and a body"
- All ways shown on this concept: L1 "names the element" (confidence 0.60).

### `loop_control`: L1

- **Rule (c).** The highest way shown is **L1 "names the element"**.
- Student's words: "The for loop has a header with a start, a condition and an update, and a body"
- All ways shown on this concept: L1 "names the element" (confidence 0.70).

### `println`: L1

- **Rule (c).** The highest way shown is **L1 "names the element"**.
- Student's words: "The program has two System.out.println statements and one for loop"
- All ways shown on this concept: L1 "names the element" (confidence 0.60).

## Step 3. Is a real mistake held?

A real mistake is a wrong rule (misconception) or a broken rule (error) that the student's own words show, after the same mistake found at two concepts has been counted once. If there is one, the walk also names the concept where the mistake starts, the **root cause**: among the concepts with a mistake, the one furthest back along the prerequisite links.

**No.** No wrong rule or broken rule is held in this answer, so the overall level is decided by the count in step 4.

## Step 4. Count the components at each level

| Level | Components at this level | Number | Share |
|---|---|---|---|
| L1 | `control_flow`, `for_loop`, `loop_body`, `loop_control`, `println` | 5 | 5 ÷ 5 = 1.00 |

The largest share is at **L1** (5 of 5 components).

No mistake is held, so this decides: the overall level is **L1**.

## Step 5. How far apart are the components?

The lowest component level is L1 and the highest is L1: 1 − 1 = 0.

The components are at most one level apart, so the answer is **coherent**: the one overall level describes it well.

## Conclusion

5 components; no mistake is held; the largest share is at L1; so the overall level is **L1**. Shares: L1 1.00; coherent.

| | Overall level | Components | Held mistake | Root cause |
|---|---|---|---|---|
| This run | L1 | `control_flow` L1, `for_loop` L1, `loop_body` L1, `loop_control` L1, `println` L1 | none | none |
| Expected by design | L1 | `for_loop` L1 | none | none |

The expected result lists only the main concept the scenario was written for; the run levels every concept the answer touches, so it usually has more components.

The rule and how it was made are in the [folder README](../../README.md).
