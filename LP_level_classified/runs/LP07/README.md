# LP07: how the overall level was calculated

This page shows only the overall level of this answer and how it was calculated. Every step of the run (what the graph offered, the model's replies, the labels, the figures) is in the notebook [`LP07.ipynb`](LP07.ipynb) and in `report.html`; the rule itself is explained in the [folder README](../../README.md).

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

Student's answer: Pass 1: i++ makes i 2 and println prints 2, then the update makes it 3. Pass 2: i++ makes it 4 and the update makes it 5. 5 < 5 is false, so the loop stops and the last line prints 5. Output: 2 and 5.

## Overall level

This scenario tests **L0: inconsistent trace**. How the overall level is decided is explained in the [folder README](../../README.md).

- **Overall level: L0** (decided by: held mistake)
- **Shares of the components:** L0 0.29, L2 0.71; LOW coherence
- **Mistake held (root cause):** statement / WhitespaceIsSignificant
- **Expected by design:** overall L0; components `loop_body` L0; held none; root none
- **Overall level matches the expected one:** yes

### How the overall level of this run was calculated

1. **Find the parts of the answer.** The answer touches 7 concepts (the components in the table below). Each one got its own level from what the student wrote about it.
2. **Is a real mistake held?** Yes. The student holds the wrong rule **WhitespaceIsSignificant** at `statement`.
3. **Result.** An answer that is built on a wrong rule is **L0**, however well the other parts are done. So the overall level is **L0**.
4. **For information, the count of the parts:** 2 at L0, 5 at L2. The parts are far apart (LOW coherence): the student handles some parts well and holds a wrong rule on others.

| Component | Level | Decided by | Student's words |
|---|---|---|---|
| `for_loop` | L2 | way: line by line trace | Pass 1: i++ makes i 2 and println prints 2, then the update makes it 3; Pass 2: i++ makes it 4 and the update makes it 5; 5 < 5 is false; so the loop stops and the last line prints 5 |
| `increment_operators` | L2 | way: one step execution | Pass 1: i++ makes i 2 and println prints 2, then the update makes it 3; Pass 2: i++ makes it 4 and the update makes it 5 |
| `loop_body` | L2 | way: line by line trace | Pass 1: i++ makes i 2 and println prints 2, then the update makes it 3; Pass 2: i++ makes it 4 and the update makes it 5 |
| `loop_control` | L0 | holds ForLoopPartSkipped | Pass 1: i++ makes i 2 and println prints 2, then the update makes it 3; Pass 2: i++ makes it 4 and the update makes it 5 |
| `loop_variable` | L2 | way: line by line trace | Pass 1: i++ makes i 2 and println prints 2, then the update makes it 3; Pass 2: i++ makes it 4 and the update makes it 5; 5 < 5 is false |
| `println` | L2 | way: output prediction | Pass 1: i++ makes i 2 and println prints 2, then the update makes it 3; so the loop stops and the last line prints 5; Output: 2 and 5 |
| `statement` | L0 | holds WhitespaceIsSignificant | Pass 1: i++ makes i 2 and println prints 2, then the update makes it 3; Output: 2 and 5 |
