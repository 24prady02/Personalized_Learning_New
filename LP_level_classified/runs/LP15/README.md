# LP15: how the overall level was calculated

This page shows only the overall level of this answer and how it was calculated. Every step of the run (what the graph offered, the model's replies, the labels, the figures) is in the notebook [`LP15.ipynb`](LP15.ipynb) and in `report.html`; the rule itself is explained in the [folder README](../../README.md).

## Input
Program:
```java
int i, n = 5;
for (i = 1; i < n; i++)
    i++;
    System.out.println(i);
System.out.println(i);
```
Question: Without tracing line by line, explain what this code does for any value of n.

Student's answer: Whatever n is, i starts at 1 and goes up by 2 on every pass, so the loop stops at the first odd number that is n or more. The program prints that number twice. For n = 5 that is 5; for n = 6 it would be 7.

## Overall level

This scenario tests **L3: purpose of the whole**. How the overall level is decided is explained in the [folder README](../../README.md).

- **Overall level: L3** (decided by: largest share)
- **Shares of the components:** L2 0.20, L3 0.80; coherent
- **Mistake held (root cause):** none
- **Expected by design:** overall L3; components `for_loop` L3; held none; root none
- **Overall level matches the expected one:** yes

### How the overall level of this run was calculated

1. **Find the parts of the answer.** The answer touches 5 concepts (the components in the table below). Each one got its own level from what the student wrote about it.
2. **Is a real mistake held?** No wrong rule is held.
3. **Count the parts at each level:** 1 at L2, 4 at L3.
4. **Result.** Most parts (4 of 5) are at L3, so the overall level is **L3**.
5. **Check.** The levels of the parts are next to each other, so the answer is coherent.

| Component | Level | Decided by | Student's words |
|---|---|---|---|
| `for_loop` | L3 | way: purpose of the whole | Whatever n is, i starts at 1 and goes up by 2 on every pass; so the loop stops at the first odd number that is n or more; The program prints that number twice |
| `increment_operators` | L3 | way: purpose of the whole | Whatever n is, i starts at 1 and goes up by 2 on every pass; so the loop stops at the first odd number that is n or more; The program prints that number twice |
| `loop_body` | L2 | way: one step execution | Whatever n is, i starts at 1 and goes up by 2 on every pass; so the loop stops at the first odd number that is n or more |
| `loop_control` | L3 | way: purpose of the whole | Whatever n is, i starts at 1 and goes up by 2 on every pass; so the loop stops at the first odd number that is n or more; The program prints that number twice |
| `loop_variable` | L3 | way: purpose of the whole | Whatever n is, i starts at 1 and goes up by 2 on every pass; so the loop stops at the first odd number that is n or more; The program prints that number twice |
