# LP16: how the overall level was calculated

This page shows only the overall level of this answer and how it was calculated. Every step of the run (what the graph offered, the model's replies, the labels, the figures) is in the notebook [`LP16.ipynb`](LP16.ipynb) and in `report.html`; the rule itself is explained in the [folder README](../../README.md).

## Input
Program:
```java
int i, n = 5;
for (i = 1; i < n; i++)
    i++;
    System.out.println(i);
System.out.println(i);
```
Question: What would be printed if braces { } were put around the two indented lines? Explain without tracing the new code line by line.

Student's answer: Then the println is in the body and runs on every pass, after the i++ and before the update. The passes do not change (the test still sees 1 and then 3), so it prints 2 and 4 inside the loop, and the last println still prints 5.

## Overall level

This scenario tests **L4: predict a change**. How the overall level is decided is explained in the [folder README](../../README.md).

- **Overall level: L4** (decided by: largest share)
- **Shares of the components:** L2 0.20, L3 0.20, L4 0.60; LOW coherence
- **Mistake held (root cause):** none
- **Expected by design:** overall L4; components `loop_body` L4; held none; root none
- **Overall level matches the expected one:** yes

### How the overall level of this run was calculated

1. **Find the parts of the answer.** The answer touches 5 concepts (the components in the table below). Each one got its own level from what the student wrote about it.
2. **Is a real mistake held?** No wrong rule is held.
3. **Count the parts at each level:** 1 at L2, 1 at L3, 3 at L4.
4. **Result.** Most parts (3 of 5) are at L4, so the overall level is **L4**.
5. **Check.** The levels of the parts are two or more apart (LOW coherence), so this one number hides real differences between the parts.

| Component | Level | Decided by | Student's words |
|---|---|---|---|
| `for_loop` | L3 | way: relation to neighbour | Then the println is in the body and runs on every pass, after the i++ and before the update; the test still sees 1 and then 3 |
| `increment_operators` | L2 | way: one step execution | the test still sees 1 and then 3; so it prints 2 and 4 inside the loop, and the last println still prints 5 |
| `loop_body` | L4 | way: predict a change | Then the println is in the body and runs on every pass, after the i++ and before the update; The passes do not change; so it prints 2 and 4 inside the loop, and the last println still prints 5 |
| `loop_control` | L4 | way: predict a change | Then the println is in the body and runs on every pass, after the i++ and before the update; The passes do not change; so it prints 2 and 4 inside the loop, and the last println still prints 5 |
| `loop_variable` | L4 | way: predict a change | Then the println is in the body and runs on every pass, after the i++ and before the update; The passes do not change; the test still sees 1 and then 3; so it prints 2 and 4 inside the loop, and the last println still prints 5 |
