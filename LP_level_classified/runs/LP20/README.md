# LP20: how the overall level was calculated

This page shows only the overall level of this answer and how it was calculated. Every step of the run (what the graph offered, the model's replies, the labels, the figures) is in the notebook [`LP20.ipynb`](LP20.ipynb) and in `report.html`; the rule itself is explained in the [folder README](../../README.md).

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

Student's answer: 5 5

## Overall level

This scenario tests **no level: none (bare correct output)**. How the overall level is decided is explained in the [folder README](../../README.md).

- **Overall level: no level** (decided by: no component)
- **Shares of the components:** no component
- **Mistake held (root cause):** none
- **Expected by design:** overall no level; components none; held none; root none
- **Overall level matches the expected one:** yes

### How the overall level of this run was calculated

1. **Find the parts of the answer.** The answer gives no reason, only an output, so no component got a level (very general concepts such as statement are not counted).
2. **Result.** With nothing to count, the answer gets **no level**.

No component has a level.

Generic concepts with a level (not counted as components): `statement` L2.
