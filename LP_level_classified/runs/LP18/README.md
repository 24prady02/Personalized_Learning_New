# LP18: how the overall level was calculated

This page shows only the overall level of this answer and how it was calculated. Every step of the run (what the graph offered, the model's replies, the labels, the figures) is in the notebook [`LP18.ipynb`](LP18.ipynb) and in `report.html`; the rule itself is explained in the [folder README](../../README.md).

## Input
Program:
```java
int i , n= 5
for(i=1;i<n;i++)
    i++;
    System.out.println(i)
system.out.println(i);
```
Question: Will this compile? What happens when you run it? Explain your reasoning.

Student's answer: Yes, it compiles and prints 5 twice. The missing ; do not matter because each statement is on its own line, and system.out is the same as System.out.

## Overall level

This scenario tests **L0: misconception**. How the overall level is decided is explained in the [folder README](../../README.md).

- **Overall level: L0** (decided by: held mistake)
- **Shares of the components:** L0 0.75, L2 0.25; LOW coherence
- **Mistake held (root cause):** statement / StatementNeedsNoTerminator
- **Expected by design:** overall L0; components `identifier` L0, `statement` L0; held IdentifierCaseInsensitive, StatementNeedsNoTerminator; root statement
- **Overall level matches the expected one:** yes

### How the overall level of this run was calculated

1. **Find the parts of the answer.** The answer touches 4 concepts (the components in the table below). Each one got its own level from what the student wrote about it.
2. **Is a real mistake held?** Yes. The student holds the wrong rule **StatementNeedsNoTerminator** at `statement`.
3. **Result.** An answer that is built on a wrong rule is **L0**, however well the other parts are done. So the overall level is **L0**.
4. **For information, the count of the parts:** 3 at L0, 1 at L2. The parts are far apart (LOW coherence): the student handles some parts well and holds a wrong rule on others.

| Component | Level | Decided by | Student's words |
|---|---|---|---|
| `compile_time_error` | L0 | way: inconsistent trace | Yes, it compiles and prints 5 twice; The missing; do not matter; because each statement is on its own line, and system.out is the same as System.out |
| `control_flow` | L2 | way: output prediction | Yes, it compiles and prints 5 twice |
| `println` | L0 | holds IdentifierCaseInsensitive | because each statement is on its own line, and system.out is the same as System.out |
| `statement` | L0 | error StatementNeedsNoTerminator | Yes, it compiles and prints 5 twice; The missing; do not matter |
