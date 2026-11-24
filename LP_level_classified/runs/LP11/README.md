# LP11: how the overall level was calculated

This page shows only the overall level of this answer and how it was calculated. Every step of the run (what the graph offered, the model's replies, the labels, the figures) is in the notebook [`LP11.ipynb`](LP11.ipynb) and in `report.html`; the rule itself is explained in the [folder README](../../README.md).

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

Student's answer: i is 5. The loop leaves when the test 5 < 5 fails, so i is 5 at that point, and nothing after the loop changes i. Both println lines print 5.

## Overall level

This scenario tests **L2: output prediction**. How the overall level is decided is explained in the [folder README](../../README.md).

- **Overall level: L2** (decided by: largest share)
- **Shares of the components:** L1 0.25, L2 0.50, L3 0.25; LOW coherence
- **Mistake held (root cause):** none
- **Expected by design:** overall L2; components `for_loop` L2; held none; root none
- **Overall level matches the expected one:** yes

### How the overall level of this run was calculated

1. **Find the parts of the answer.** The answer touches 4 concepts (the components in the table below). Each one got its own level from what the student wrote about it.
2. **Is a real mistake held?** No wrong rule is held.
3. **Count the parts at each level:** 1 at L1, 2 at L2, 1 at L3.
4. **Result.** Most parts (2 of 4) are at L2, so the overall level is **L2**.
5. **Check.** The levels of the parts are two or more apart (LOW coherence), so this one number hides real differences between the parts.

| Component | Level | Decided by | Student's words |
|---|---|---|---|
| `loop_body` | L1 | way: states the rule | Both println lines print 5 |
| `loop_control` | L2 | way: one step execution | The loop leaves when the test 5 < 5 fails |
| `loop_variable` | L3 | way: relation to neighbour | The loop leaves when the test 5 < 5 fails; so i is 5 at that point, and nothing after the loop changes i; Both println lines print 5 |
| `println` | L2 | way: one step execution | so i is 5 at that point, and nothing after the loop changes i; Both println lines print 5 |

Generic concepts with a level (not counted as components): `statement` L3.
