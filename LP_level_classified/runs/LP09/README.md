# LP09: how the overall level was calculated

This page shows only the overall level of this answer and how it was calculated. Every step of the run (what the graph offered, the model's replies, the labels, the figures) is in the notebook [`LP09.ipynb`](LP09.ipynb) and in `report.html`; the rule itself is explained in the [folder README](../../README.md).

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

Student's answer: Without braces a for loop repeats only the one statement right after its header. The indentation does not matter, so the println lines are not part of the loop.

## Overall level

This scenario tests **L1: states the rule**. How the overall level is decided is explained in the [folder README](../../README.md).

- **Overall level: L4** (decided by: largest share)
- **Shares of the components:** L3 0.33, L4 0.67; coherent
- **Mistake held (root cause):** none
- **Expected by design:** overall L1; components `loop_body` L1; held none; root none
- **Overall level matches the expected one:** no

### How the overall level of this run was calculated

1. **Find the parts of the answer.** The answer touches 3 concepts (the components in the table below). Each one got its own level from what the student wrote about it.
2. **Is a real mistake held?** No wrong rule is held.
3. **Count the parts at each level:** 1 at L3, 2 at L4.
4. **Result.** Most parts (2 of 3) are at L4, so the overall level is **L4**.
5. **Check.** The levels of the parts are next to each other, so the answer is coherent.

| Component | Level | Decided by | Student's words |
|---|---|---|---|
| `control_flow` | L3 | way: relation to neighbour | Without braces a for loop repeats only the one statement right after its header; The indentation does not matter; so the println lines are not part of the loop |
| `for_loop` | L4 | way: diagnose an error | Without braces a for loop repeats only the one statement right after its header; The indentation does not matter; so the println lines are not part of the loop |
| `loop_body` | L4 | way: diagnose an error | Without braces a for loop repeats only the one statement right after its header; The indentation does not matter; so the println lines are not part of the loop |

Generic concepts with a level (not counted as components): `statement` L3.
