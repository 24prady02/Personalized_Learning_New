# LP04: how the overall level was calculated

This page shows only the overall level of this answer and how it was calculated. Every step of the run (what the graph offered, the model's replies, the labels, the figures) is in the notebook [`LP04.ipynb`](LP04.ipynb) and in `report.html`; the rule itself is explained in the [folder README](../../README.md).

## Input
Program:
```java
int i, n = 5;
for (i = 1; i < n; i++)
    i++;
    System.out.println(i);
System.out.println(i);
```
Question: What is the value of i when the second println runs? Explain how i gets that value.

Student's answer: i is 5. The loop runs for i = 1, 2, 3, 4 and stops when i reaches 5; the i++ in the body does not affect the count.

## Overall level

This scenario tests **L0: misconception**. How the overall level is decided is explained in the [folder README](../../README.md).

- **Overall level: L0** (decided by: held mistake)
- **Shares of the components:** L0 0.43, L2 0.57; LOW coherence
- **Mistake held (root cause):** loop_variable / BodyChangeIgnoredByCondition
- **Expected by design:** overall L0; components `loop_variable` L0; held BodyChangeIgnoredByCondition; root loop_variable
- **Overall level matches the expected one:** yes

### How the overall level of this run was calculated

1. **Find the parts of the answer.** The answer touches 7 concepts (the components in the table below). Each one got its own level from what the student wrote about it.
2. **Is a real mistake held?** Yes. The student holds the wrong rule **BodyChangeIgnoredByCondition** at `loop_variable`.
3. **Result.** An answer that is built on a wrong rule is **L0**, however well the other parts are done. So the overall level is **L0**.
4. **For information, the count of the parts:** 3 at L0, 4 at L2. The parts are far apart (LOW coherence): the student handles some parts well and holds a wrong rule on others.

| Component | Level | Decided by | Student's words |
|---|---|---|---|
| `comparison_operators` | L2 | way: output prediction | The loop runs for i = 1, 2, 3, 4 and stops when i reaches 5 |
| `control_flow` | L2 | way: line by line trace | The loop runs for i = 1, 2, 3, 4 and stops when i reaches 5 |
| `for_loop` | L2 | way: output prediction | i is 5; The loop runs for i = 1, 2, 3, 4 and stops when i reaches 5; the i++ in the body does not affect the count |
| `increment_operators` | L0 | holds IdiomOverridesCode | The loop runs for i = 1, 2, 3, 4 and stops when i reaches 5; the i++ in the body does not affect the count |
| `loop_body` | L0 | holds ForLoopPartSkipped | The loop runs for i = 1, 2, 3, 4 and stops when i reaches 5; the i++ in the body does not affect the count |
| `loop_control` | L2 | way: output prediction | The loop runs for i = 1, 2, 3, 4 and stops when i reaches 5 |
| `loop_variable` | L0 | holds BodyChangeIgnoredByCondition | The loop runs for i = 1, 2, 3, 4 and stops when i reaches 5; the i++ in the body does not affect the count |
