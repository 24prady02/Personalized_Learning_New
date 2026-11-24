# LP12: the overall level and how it was arrived at

This page explains, with the numbers of this run, how one overall level was worked out for this answer. Every step of the run itself (what the graph offered, the model's replies, all labels, all figures) is in the notebook [`LP12.ipynb`](LP12.ipynb) and in `report.html`.

## The answer that was read

```java
int i, n = 5;
for (i = 1; i < n; i++)
    i++;
    System.out.println(i);
System.out.println(i);
```

**Question.** How many times does the body of the for loop run? Explain your reasoning.

**Student's answer.** On one pass i goes up by 2: once by the i++ in the body and once by the i++ in the update. So after the first pass i is 3 instead of 2.

**What this scenario was written to test.** L2: one step execution.

## Result

- **Overall level: L2** (multistructural)
- **Decided by:** no mistake is held, so the level that most components have (step 4 below)
- **Expected by design:** L2. **Match: yes**

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
| `assignment` | yes | L2 | no: generic |
| `boolean_expression` |  | none | no: the answer shows nothing about it, so it has no level |
| `comparison_operators` |  | none | no: the answer shows nothing about it, so it has no level |
| `control_flow` |  | none | no: the answer shows nothing about it, so it has no level |
| `expression` | yes | none | no: generic, and the answer shows nothing about it |
| `for_loop` |  | L2 | **yes** |
| `increment_operators` |  | L2 | **yes** |
| `loop_body` |  | L2 | **yes** |
| `loop_control` |  | L2 | **yes** |
| `loop_variable` |  | L2 | **yes** |
| `println` |  | none | no: the answer shows nothing about it, so it has no level |
| `statement` | yes | none | no: generic, and the answer shows nothing about it |

**Components of this answer: 5.** `for_loop`, `increment_operators`, `loop_body`, `loop_control`, `loop_variable`.

![The concepts of this run, coloured by level](figure08.png)

*The concepts of this program and the links between them, after the run. A coloured concept has a level (red L0, orange L1, yellow L2, light green L3, green L4); a grey concept was found in the code but the answer shows nothing about it. A thick black outline marks the root cause, and a diamond is a wrong rule the student holds. The picture also colours generic concepts that have a level; the table above says which of them are counted.*

**Where this step comes from**

- Each concept is levelled on its own. Jin et al. 2019, IJSE, p. 1325: “some researchers identify multiple progress variables of an LP, with each progress variable elaborating the development in one dimension of the LP”. Here each component is one progress variable.
- The whole answer is one unit of evidence. Jin, Lima & Wang 2025, EM:IP, p. 5: multi-part answers “were combined into a single response to allow for a comprehensive analysis of student reasoning”.
- Which concepts count (non-generic concepts with a level, plus any concept where a real mistake is held) is the rule of the LP test instructions.

## Step 2. The level of each component

Each component gets its level by the first of these rules that fits:

- **(a)** a wrong rule (misconception) is held on the concept: **L0**, whatever else is shown;
- **(b)** only L0 ways are shown (everyday reading, inconsistent trace): **L0**;
- **(c)** otherwise the **highest** level at which a way is shown. One shown way is enough, because the levels build on each other.

A way above L2 is counted only when the model's confidence is above 0.60 and it does not rest only on the words of a held mistake.

### `for_loop`: L2

- **Rule (c).** The highest way shown is **L2 "one step execution"**.
- Student's words: "On one pass i goes up by 2: once by the i++ in the body and once by the i++ in the update; So after the first pass i is 3 instead of 2"
- All ways shown on this concept: L2 "one step execution" (confidence 0.85); L2 "line by line trace" (confidence 0.75).

### `increment_operators`: L2

- **Rule (c).** The highest way shown is **L2 "one step execution"**.
- Student's words: "On one pass i goes up by 2: once by the i++ in the body and once by the i++ in the update; So after the first pass i is 3 instead of 2"
- All ways shown on this concept: L2 "one step execution" (confidence 0.80); L2 "line by line trace" (confidence 0.70).
- Shown but not counted: L3 "relation to neighbour" (confidence 0.60 is not above 0.60).

### `loop_body`: L2

- **Rule (c).** The highest way shown is **L2 "one step execution"**.
- Student's words: "On one pass i goes up by 2: once by the i++ in the body and once by the i++ in the update; So after the first pass i is 3 instead of 2"
- All ways shown on this concept: L1 "names the element" (confidence 0.70); L2 "one step execution" (confidence 0.80); L2 "line by line trace" (confidence 0.75).

### `loop_control`: L2

- **Rule (c).** The highest way shown is **L2 "one step execution"**.
- Student's words: "On one pass i goes up by 2: once by the i++ in the body and once by the i++ in the update; So after the first pass i is 3 instead of 2"
- All ways shown on this concept: L2 "one step execution" (confidence 0.85); L2 "line by line trace" (confidence 0.75).
- Shown but not counted: L4 "diagnose an error" (confidence 0.60 is not above 0.60).

### `loop_variable`: L2

- **Rule (c).** The highest way shown is **L2 "one step execution"**.
- Student's words: "On one pass i goes up by 2: once by the i++ in the body and once by the i++ in the update; So after the first pass i is 3 instead of 2"
- All ways shown on this concept: L2 "one step execution" (confidence 0.78); L2 "line by line trace" (confidence 0.70).

**Where this step comes from**

- Levels are read from indicators (the ways), not from one overall impression. Jin, Lima & Wang 2025, EM:IP, p. 2: “Analytic rubrics specify indicators to be detected from students’ responses”; analytic scoring “often results in greater details and precision”. P. 5: “analytical rubrics that contain item-specific indicators for each LP level”.
- Rule (a). Lister et al. 2006, p. 2: a prestructural response manifests “a significant misconception of programming”. Also Teague & Lister 2014, p. 1, and ProgMiscon (Chiodini et al. 2021), p. 2.
- Rule (b). Pea 1986, p. 2; Teague & Lister 2014, p. 1 (“cannot trace code”).
- Rule (c). Lister et al. 2006, p. 2 (the SOLO levels build on each other); Jin, Lima & Wang 2025, p. 6 (an answer is scored at the level whose indicator it shows).
- No way shown, no level. Workbook boundary: “a bare correct output is not levelled”.
- The levels, their ways and their indicators are fixed before any student answer is read (Jin et al. 2019, p. 6). They are the SOLO levels for code (Lister et al. 2006) matched to the neo-Piagetian stages (Lister 2011; Teague & Lister 2014).
- The confidence limit of 0.60 for ways above L2 is this project's own rule; it has no source in the literature.

## Step 3. Is a real mistake held?

A real mistake is a wrong rule (misconception) or a broken rule (error) that the student's own words show, after the same mistake found at two concepts has been counted once. If there is one, the walk also names the concept where the mistake starts, the **root cause**: among the concepts with a mistake, the one furthest back along the prerequisite links.

**No.** No wrong rule or broken rule is held in this answer, so the overall level is decided by the count in step 4.

**Where this step comes from**

- **This step is this project's own; none of the papers states it.** It takes rule (a) of step 2, which the sources give for one concept (Lister et al. 2006, p. 2: “a significant misconception of programming”), and applies it to the whole answer.
- The papers by Jin et al. would go a different way here: when the parts of an answer sit at levels far apart, Jin et al. 2019, p. 1337, say “we cannot make any inferences about the students’ levels”. That is why the count of step 4 and the coherence check of step 5 are always shown beside the L0.

## Step 4. Count the components at each level

| Level | Components at this level | Number | Share |
|---|---|---|---|
| L2 | `for_loop`, `increment_operators`, `loop_body`, `loop_control`, `loop_variable` | 5 | 5 ÷ 5 = 1.00 |

The largest share is at **L2** (5 of 5 components).

No mistake is held, so this decides: the overall level is **L2**.

**Where this step comes from**

- Shares and the largest share. Jin et al. 2019, IJSE, pp. 1338–1339, Table 4, reports level classification probabilities per student, for example Student 210: L2 .68, L3 .32 (the level with the largest share is the student's level), and Student 220: L1 .50, L2 .50, described as “rely on Level 1 and Level 2 reasoning”.
- The tie rule (the lower level) is an adaptation of the LP test instructions: Jin et al. report Student 220 at both levels; one number is needed here, so the lower is taken.
- Adapted from Jin et al.: they apply this across many items and students with a partial credit model (Jin et al. 2017, JRST, pp. 862–863: “we used the resulting person proficiencies from the item response model analysis”); here it is applied across the components of one answer with simple shares.

## Step 5. How far apart are the components?

The lowest component level is L2 and the highest is L2: 2 − 2 = 0.

The components are at most one level apart, so the answer is **coherent**: the one overall level describes it well.

**Where this step comes from**

- Why the check is made. Jin et al. 2019, p. 1337: “Most students in our study provided responses at different levels for different assessment items”, so one level can hide real differences.
- Adjacent levels are coherent. Jin et al. 2019, p. 1338: “each student produced responses at adjacent levels, suggesting that those students’ ideas are coherent to a certain degree”.
- Far apart, no inference. Jin et al. 2019, p. 1337: “If the result shows evidence of ‘knowledge-in-pieces’ (e.g. probabilities of responses at different levels are about the same) … we cannot make any inferences about the students’ levels”.

## Conclusion

5 components; no mistake is held; the largest share is at L2; so the overall level is **L2**. Shares: L2 1.00; coherent.

| | Overall level | Components | Held mistake | Root cause |
|---|---|---|---|---|
| This run | L2 | `for_loop` L2, `increment_operators` L2, `loop_body` L2, `loop_control` L2, `loop_variable` L2 | none | none |
| Expected by design | L2 | `for_loop` L2 | none | none |

The expected result lists only the main concept the scenario was written for; the run levels every concept the answer touches, so it usually has more components.

## Sources

The quotations and page numbers on this page are those given in the LP test instructions for these scenarios; they were not checked again against the papers here.

- Jin et al. 2019, *IJSE* (pp. 1325, 1337 to 1339, Table 4): progress variables, levels differing across items, coherence, level shares.
- Jin, Lima & Wang 2025, *EM:IP* (pp. 2, 5, 6): analytic rubrics, indicators for each level, one response as the unit.
- Jin et al. 2017, *JRST* (pp. 862 to 863): the partial credit model, the full method for many students and items.
- Lister et al. 2006 (p. 2): the SOLO levels for code; Lister 2011 and Teague & Lister 2014 (p. 1): the neo-Piagetian stages.
- Pea 1986 (p. 2); ProgMiscon, Chiodini et al. 2021 (p. 2): misconceptions.
- Where the sources disagree: Jimoyiannis (2011) codes some misconception-driven answers at L1 to L2, not L0, and modifying given code as L3, not L4 (also Vrachnos & Jimoyiannis 2017).

The rule and how it was made are in the [folder README](../../README.md).
