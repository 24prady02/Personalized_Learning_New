# LP03: how the overall level was calculated

This page shows only the overall level of this answer and how it was calculated. Every step of the run (what the graph offered, the model's replies, the labels, the figures) is in the notebook [`LP03.ipynb`](LP03.ipynb) and in `report.html`; the rule itself is explained in the [folder README](../../README.md).

## Input
Program:
```java
int i, n = 5;
for (i = 1; i < n; i++)
    i++;
    System.out.println(i);
System.out.println(i);
```
Question: How many times does the body of the for loop run? Explain your reasoning.

Student's answer: The body runs 4 times, for i = 1, 2, 3 and 4. The header says i < 5 and i++, so it runs 4 times; the i++ inside the body does not change how many times the loop runs.

## Overall level

This scenario tests **L0: misconception**. How the overall level is decided is explained in the [folder README](../../README.md).

- **Overall level: L0** (decided by: held mistake)
- **Shares of the components:** L0 0.80, L2 0.20; LOW coherence
- **Mistake held (root cause):** loop_variable / BodyChangeIgnoredByCondition
- **Expected by design:** overall L0; components `loop_variable` L0; held BodyChangeIgnoredByCondition; root loop_variable
- **Overall level matches the expected one:** yes

### How the overall level of this run was calculated

1. **Find the parts of the answer.** The answer touches 5 concepts (the components in the table below). Each one got its own level from what the student wrote about it.
2. **Is a real mistake held?** Yes. The student holds the wrong rule **BodyChangeIgnoredByCondition** at `loop_variable`.
3. **Result.** An answer that is built on a wrong rule is **L0**, however well the other parts are done. So the overall level is **L0**.
4. **For information, the count of the parts:** 4 at L0, 1 at L2. The parts are far apart (LOW coherence): the student handles some parts well and holds a wrong rule on others.

| Component | Level | Decided by | Student's words |
|---|---|---|---|
| `for_loop` | L2 | way: output prediction | The body runs 4 times, for i = 1, 2, 3 and 4; The header says i < 5 and i++; so it runs 4 times; the i++ inside the body does not change how many times the loop runs |
| `increment_operators` | L0 | holds IdiomOverridesCode | The body runs 4 times, for i = 1, 2, 3 and 4; so it runs 4 times; the i++ inside the body does not change how many times the loop runs |
| `loop_body` | L0 | holds StateChangeIgnoredAcrossPasses | The body runs 4 times, for i = 1, 2, 3 and 4; so it runs 4 times; the i++ inside the body does not change how many times the loop runs |
| `loop_control` | L0 | holds IdiomOverridesCode | The body runs 4 times, for i = 1, 2, 3 and 4; The header says i < 5 and i++; so it runs 4 times; the i++ inside the body does not change how many times the loop runs |
| `loop_variable` | L0 | holds BodyChangeIgnoredByCondition | The body runs 4 times, for i = 1, 2, 3 and 4; so it runs 4 times; the i++ inside the body does not change how many times the loop runs |
