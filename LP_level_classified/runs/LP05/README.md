# LP05: how the overall level was calculated

This page shows only the overall level of this answer and how it was calculated. Every step of the run (what the graph offered, the model's replies, the labels, the figures) is in the notebook [`LP05.ipynb`](LP05.ipynb) and in `report.html`; the rule itself is explained in the [folder README](../../README.md).

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

Student's answer: The body runs once. i++ adds 2, so after the body i is 3, and the update makes it 5. Then 5 < 5 is false, so the loop stops.

## Overall level

This scenario tests **L0: misconception**. How the overall level is decided is explained in the [folder README](../../README.md).

- **Overall level: L0** (decided by: held mistake)
- **Shares of the components:** L0 0.50, L2 0.50; LOW coherence
- **Mistake held (root cause):** loop_control / WrongIterationCount
- **Expected by design:** overall L0; components `increment_operators` L0; held IncrementByTwo; root increment_operators
- **Overall level matches the expected one:** yes

### How the overall level of this run was calculated

1. **Find the parts of the answer.** The answer touches 4 concepts (the components in the table below). Each one got its own level from what the student wrote about it.
2. **Is a real mistake held?** Yes. The student holds the wrong rule **WrongIterationCount** at `loop_control`.
3. **Result.** An answer that is built on a wrong rule is **L0**, however well the other parts are done. So the overall level is **L0**.
4. **For information, the count of the parts:** 2 at L0, 2 at L2. The parts are far apart (LOW coherence): the student handles some parts well and holds a wrong rule on others.

| Component | Level | Decided by | Student's words |
|---|---|---|---|
| `for_loop` | L2 | way: line by line trace | so after the body i is 3, and the update makes it 5; Then 5 < 5 is false; so the loop stops |
| `increment_operators` | L0 | holds IncrementByTwo | i++ adds 2; so after the body i is 3, and the update makes it 5 |
| `loop_control` | L0 | error WrongIterationCount | The body runs once; i++ adds 2; so after the body i is 3, and the update makes it 5; Then 5 < 5 is false; so the loop stops |
| `loop_variable` | L2 | way: line by line trace | so after the body i is 3, and the update makes it 5; Then 5 < 5 is false; so the loop stops |
