# LP12: how the overall level was calculated

This page shows only the overall level of this answer and how it was calculated. Every step of the run (what the graph offered, the model's replies, the labels, the figures) is in the notebook [`LP12.ipynb`](LP12.ipynb) and in `report.html`; the rule itself is explained in the [folder README](../../README.md).

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

Student's answer: On one pass i goes up by 2: once by the i++ in the body and once by the i++ in the update. So after the first pass i is 3 instead of 2.

## Overall level

This scenario tests **L2: one step execution**. How the overall level is decided is explained in the [folder README](../../README.md).

- **Overall level: L2** (decided by: largest share)
- **Shares of the components:** L2 1.00; coherent
- **Mistake held (root cause):** none
- **Expected by design:** overall L2; components `for_loop` L2; held none; root none
- **Overall level matches the expected one:** yes

### How the overall level of this run was calculated

1. **Find the parts of the answer.** The answer touches 5 concepts (the components in the table below). Each one got its own level from what the student wrote about it.
2. **Is a real mistake held?** No wrong rule is held.
3. **Count the parts at each level:** 5 at L2.
4. **Result.** Most parts (5 of 5) are at L2, so the overall level is **L2**.
5. **Check.** The levels of the parts are next to each other, so the answer is coherent.

| Component | Level | Decided by | Student's words |
|---|---|---|---|
| `for_loop` | L2 | way: one step execution | On one pass i goes up by 2: once by the i++ in the body and once by the i++ in the update; So after the first pass i is 3 instead of 2 |
| `increment_operators` | L2 | way: one step execution | On one pass i goes up by 2: once by the i++ in the body and once by the i++ in the update; So after the first pass i is 3 instead of 2 |
| `loop_body` | L2 | way: one step execution | On one pass i goes up by 2: once by the i++ in the body and once by the i++ in the update; So after the first pass i is 3 instead of 2 |
| `loop_control` | L2 | way: one step execution | On one pass i goes up by 2: once by the i++ in the body and once by the i++ in the update; So after the first pass i is 3 instead of 2 |
| `loop_variable` | L2 | way: one step execution | On one pass i goes up by 2: once by the i++ in the body and once by the i++ in the update; So after the first pass i is 3 instead of 2 |

Generic concepts with a level (not counted as components): `assignment` L2.
