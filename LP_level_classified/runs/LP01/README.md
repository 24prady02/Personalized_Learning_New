# LP01: how the overall level was calculated

This page shows only the overall level of this answer and how it was calculated. Every step of the run (what the graph offered, the model's replies, the labels, the figures) is in the notebook [`LP01.ipynb`](LP01.ipynb) and in `report.html`; the rule itself is explained in the [folder README](../../README.md).

## Input
Program:
```java
int i, n = 5;
for (i = 1; i < n; i++)
    i++;
    System.out.println(i);
System.out.println(i);
```
Question: What is printed? Explain, pass by pass, what happens to i.

Student's answer: It counts from 1 to 5, so it prints 1, 2, 3, 4, 5. 'For i from 1 to n' means do it for each number.

## Overall level

This scenario tests **L0: everyday reading**. How the overall level is decided is explained in the [folder README](../../README.md).

- **Overall level: L0** (decided by: held mistake)
- **Shares of the components:** L0 1.00; coherent
- **Mistake held (root cause):** loop_variable / BodyChangeIgnoredByCondition
- **Expected by design:** overall L0; components `for_loop` L0; held none; root none
- **Overall level matches the expected one:** yes

### How the overall level of this run was calculated

1. **Find the parts of the answer.** The answer touches 5 concepts (the components in the table below). Each one got its own level from what the student wrote about it.
2. **Is a real mistake held?** Yes. The student holds the wrong rule **BodyChangeIgnoredByCondition** at `loop_variable`.
3. **Result.** An answer that is built on a wrong rule is **L0**, however well the other parts are done. So the overall level is **L0**.
4. **For information, the count of the parts:** 5 at L0. The parts are close together.

| Component | Level | Decided by | Student's words |
|---|---|---|---|
| `for_loop` | L0 | way: everyday reading | It counts from 1 to 5; so it prints 1, 2, 3, 4, 5; For i from 1 to n means do it for each number |
| `increment_operators` | L0 | holds IdiomOverridesCode | It counts from 1 to 5; so it prints 1, 2, 3, 4, 5; For i from 1 to n means do it for each number |
| `loop_body` | L0 | holds ComputerFillsInIntent | It counts from 1 to 5; so it prints 1, 2, 3, 4, 5; For i from 1 to n means do it for each number |
| `loop_control` | L0 | way: everyday reading | It counts from 1 to 5; so it prints 1, 2, 3, 4, 5; For i from 1 to n means do it for each number |
| `loop_variable` | L0 | holds BodyChangeIgnoredByCondition | It counts from 1 to 5; For i from 1 to n means do it for each number |
