# LP08: how the overall level was calculated

This page shows only the overall level of this answer and how it was calculated. Every step of the run (what the graph offered, the model's replies, the labels, the figures) is in the notebook [`LP08.ipynb`](LP08.ipynb) and in `report.html`; the rule itself is explained in the [folder README](../../README.md).

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

Student's answer: The program has two System.out.println statements and one for loop. The for loop has a header with a start, a condition and an update, and a body.

## Overall level

This scenario tests **L1: names the element**. How the overall level is decided is explained in the [folder README](../../README.md).

- **Overall level: L1** (decided by: largest share)
- **Shares of the components:** L1 1.00; coherent
- **Mistake held (root cause):** none
- **Expected by design:** overall L1; components `for_loop` L1; held none; root none
- **Overall level matches the expected one:** yes

### How the overall level of this run was calculated

1. **Find the parts of the answer.** The answer touches 5 concepts (the components in the table below). Each one got its own level from what the student wrote about it.
2. **Is a real mistake held?** No wrong rule is held.
3. **Count the parts at each level:** 5 at L1.
4. **Result.** Most parts (5 of 5) are at L1, so the overall level is **L1**.
5. **Check.** The levels of the parts are next to each other, so the answer is coherent.

| Component | Level | Decided by | Student's words |
|---|---|---|---|
| `control_flow` | L1 | way: names the element | The program has two System.out.println statements and one for loop; The for loop has a header with a start, a condition and an update, and a body |
| `for_loop` | L1 | way: names the element | The for loop has a header with a start, a condition and an update, and a body |
| `loop_body` | L1 | way: names the element | The for loop has a header with a start, a condition and an update, and a body |
| `loop_control` | L1 | way: names the element | The for loop has a header with a start, a condition and an update, and a body |
| `println` | L1 | way: names the element | The program has two System.out.println statements and one for loop |
