# LP19: how the overall level was calculated

This page shows only the overall level of this answer and how it was calculated. Every step of the run (what the graph offered, the model's replies, the labels, the figures) is in the notebook [`LP19.ipynb`](LP19.ipynb) and in `report.html`; the rule itself is explained in the [folder README](../../README.md).

## Input
Program:
```java
int i, n = 5;
for (i = 1; i < n; i++)
    i++;
    System.out.println(i);
System.out.println(i);
```
Question: Write a loop that prints every odd number smaller than n, and explain how it relates to this loop.

Student's answer: for (int i = 1; i < n; i += 2) System.out.println(i); This does on purpose what the given loop does by accident: the given loop also steps i by 2, because i++ is in both the body and the header. If I wanted more than one statement repeated I would add braces.

## Overall level

This scenario tests **L4: transfer to a new program**. How the overall level is decided is explained in the [folder README](../../README.md).

- **Overall level: L4** (decided by: largest share)
- **Shares of the components:** L2 0.25, L4 0.75; LOW coherence
- **Mistake held (root cause):** none
- **Expected by design:** overall L4; components `for_loop` L4; held none; root none
- **Overall level matches the expected one:** yes

### How the overall level of this run was calculated

1. **Find the parts of the answer.** The answer touches 4 concepts (the components in the table below). Each one got its own level from what the student wrote about it.
2. **Is a real mistake held?** No wrong rule is held.
3. **Count the parts at each level:** 1 at L2, 3 at L4.
4. **Result.** Most parts (3 of 4) are at L4, so the overall level is **L4**.
5. **Check.** The levels of the parts are two or more apart (LOW coherence), so this one number hides real differences between the parts.

| Component | Level | Decided by | Student's words |
|---|---|---|---|
| `increment_operators` | L4 | way: transfer to a new program | for (int i = 1; i < n; i += 2) System.out.println(i); This does on purpose what the given loop does by accident: the given loop also steps i by 2; because i++ is in both the body and the header |
| `loop_body` | L2 | way: one step execution | This does on purpose what the given loop does by accident: the given loop also steps i by 2; because i++ is in both the body and the header |
| `loop_control` | L4 | way: diagnose an error | This does on purpose what the given loop does by accident: the given loop also steps i by 2; because i++ is in both the body and the header |
| `loop_variable` | L4 | way: diagnose an error | This does on purpose what the given loop does by accident: the given loop also steps i by 2; because i++ is in both the body and the header |

Generic concepts with a level (not counted as components): `assignment` L3.
