# LP14: how the overall level was calculated

This page shows only the overall level of this answer and how it was calculated. Every step of the run (what the graph offered, the model's replies, the labels, the figures) is in the notebook [`LP14.ipynb`](LP14.ipynb) and in `report.html`; the rule itself is explained in the [folder README](../../README.md).

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

Student's answer: Twice. The body's i++ and the header's i++ change the same variable, so the condition sees i as 1, then 3, then 5 and fails on the third test. Because there are no braces the body is only i++; the indented println is after the loop.

## Overall level

This scenario tests **L3: relation to neighbour**. How the overall level is decided is explained in the [folder README](../../README.md).

- **Overall level: L3** (decided by: largest share)
- **Shares of the components:** L2 0.20, L3 0.40, L4 0.40; LOW coherence
- **Mistake held (root cause):** none
- **Expected by design:** overall L3; components `for_loop` L3, `increment_operators` L3; held none; root none
- **Overall level matches the expected one:** yes

### How the overall level of this run was calculated

1. **Find the parts of the answer.** The answer touches 5 concepts (the components in the table below). Each one got its own level from what the student wrote about it.
2. **Is a real mistake held?** No wrong rule is held.
3. **Count the parts at each level:** 1 at L2, 2 at L3, 2 at L4.
4. **Result.** L3 and L4 have the same number of parts (2 each). On a tie the lower level is taken, the one the answer reliably reaches, so the overall level is **L3**.
5. **Check.** The levels of the parts are two or more apart (LOW coherence), so this one number hides real differences between the parts.

| Component | Level | Decided by | Student's words |
|---|---|---|---|
| `for_loop` | L4 | way: diagnose an error | Because there are no braces the body is only i++; the indented println is after the loop |
| `increment_operators` | L3 | way: relation to neighbour | The bodys i++ and the headers i++ change the same variable; so the condition sees i as 1, then 3, then 5 and fails on the third test |
| `loop_body` | L4 | way: diagnose an error | Because there are no braces the body is only i++; the indented println is after the loop |
| `loop_control` | L3 | way: relation to neighbour | The bodys i++ and the headers i++ change the same variable; so the condition sees i as 1, then 3, then 5 and fails on the third test |
| `loop_variable` | L2 | way: one step execution | The bodys i++ and the headers i++ change the same variable; so the condition sees i as 1, then 3, then 5 and fails on the third test |

Generic concepts with a level (not counted as components): `assignment` L3.
