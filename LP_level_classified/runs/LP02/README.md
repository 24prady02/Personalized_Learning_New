# LP02: how the overall level was calculated

This page shows only the overall level of this answer and how it was calculated. Every step of the run (what the graph offered, the model's replies, the labels, the figures) is in the notebook [`LP02.ipynb`](LP02.ipynb) and in `report.html`; the rule itself is explained in the [folder README](../../README.md).

## Input
Program:
```java
int i, n = 5;
for (i = 1; i < n; i++)
    i++;
    System.out.println(i);
System.out.println(i);
```
Question: How many times is System.out.println executed? Explain your reasoning.

Student's answer: println runs 3 times. The indented println is inside the loop, so it runs on both passes and prints 2 and 4, and then the last println prints 5.

## Overall level

This scenario tests **L0: misconception**. How the overall level is decided is explained in the [folder README](../../README.md).

- **Overall level: L0** (decided by: held mistake)
- **Shares of the components:** L0 0.25, L2 0.75; LOW coherence
- **Mistake held (root cause):** statement / WhitespaceIsSignificant
- **Expected by design:** overall L0; components `loop_body` L0; held StatementAfterLoopInBody; root loop_body
- **Overall level matches the expected one:** yes

### How the overall level of this run was calculated

1. **Find the parts of the answer.** The answer touches 8 concepts (the components in the table below). Each one got its own level from what the student wrote about it.
2. **Is a real mistake held?** Yes. The student holds the wrong rule **WhitespaceIsSignificant** at `statement`.
3. **Result.** An answer that is built on a wrong rule is **L0**, however well the other parts are done. So the overall level is **L0**.
4. **For information, the count of the parts:** 2 at L0, 6 at L2. The parts are far apart (LOW coherence): the student handles some parts well and holds a wrong rule on others.

| Component | Level | Decided by | Student's words |
|---|---|---|---|
| `control_flow` | L2 | way: output prediction | println runs 3 times; so it runs on both passes and prints 2 and 4, and then the last println prints 5 |
| `for_loop` | L2 | way: line by line trace | so it runs on both passes and prints 2 and 4, and then the last println prints 5 |
| `increment_operators` | L2 | way: one step execution | so it runs on both passes and prints 2 and 4, and then the last println prints 5 |
| `loop_body` | L0 | a held mistake, no level of its own |  |
| `loop_control` | L2 | way: line by line trace | so it runs on both passes and prints 2 and 4, and then the last println prints 5 |
| `loop_variable` | L2 | way: one step execution | so it runs on both passes and prints 2 and 4, and then the last println prints 5 |
| `println` | L2 | way: output prediction | so it runs on both passes and prints 2 and 4, and then the last println prints 5 |
| `statement` | L0 | holds WhitespaceIsSignificant | println runs 3 times; The indented println is inside the loop; so it runs on both passes and prints 2 and 4, and then the last println prints 5 |
