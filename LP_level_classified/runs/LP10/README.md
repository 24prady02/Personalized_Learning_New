# LP10: how the overall level was calculated

This page shows only the overall level of this answer and how it was calculated. Every step of the run (what the graph offered, the model's replies, the labels, the figures) is in the notebook [`LP10.ipynb`](LP10.ipynb) and in `report.html`; the rule itself is explained in the [folder README](../../README.md).

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

Student's answer: i starts at 1. 1 < 5 is true, the body i++ makes i 2, the update makes it 3. 3 < 5 is true, the body makes it 4, the update makes it 5. 5 < 5 is false, so the loop stops. Only i++ was in the loop. Then the two println lines print 5 and 5.

## Overall level

This scenario tests **L2: line by line trace**. How the overall level is decided is explained in the [folder README](../../README.md).

- **Overall level: L2** (decided by: largest share)
- **Shares of the components:** L2 0.67, L3 0.33; coherent
- **Mistake held (root cause):** none
- **Expected by design:** overall L2; components `for_loop` L2, `loop_body` L2; held none; root none
- **Overall level matches the expected one:** yes

### How the overall level of this run was calculated

1. **Find the parts of the answer.** The answer touches 6 concepts (the components in the table below). Each one got its own level from what the student wrote about it.
2. **Is a real mistake held?** No wrong rule is held.
3. **Count the parts at each level:** 4 at L2, 2 at L3.
4. **Result.** Most parts (4 of 6) are at L2, so the overall level is **L2**.
5. **Check.** The levels of the parts are next to each other, so the answer is coherent.

| Component | Level | Decided by | Student's words |
|---|---|---|---|
| `for_loop` | L3 | way: relation to neighbour | 1 < 5 is true, the body i++ makes i 2, the update makes it 3; 3 < 5 is true, the body makes it 4, the update makes it 5; Only i++ was in the loop |
| `increment_operators` | L2 | way: one step execution | 1 < 5 is true, the body i++ makes i 2, the update makes it 3; 3 < 5 is true, the body makes it 4, the update makes it 5 |
| `loop_body` | L2 | way: line by line trace | 1 < 5 is true, the body i++ makes i 2, the update makes it 3; 3 < 5 is true, the body makes it 4, the update makes it 5 |
| `loop_control` | L2 | way: line by line trace | i starts at 1; 1 < 5 is true, the body i++ makes i 2, the update makes it 3; 3 < 5 is true, the body makes it 4, the update makes it 5; 5 < 5 is false; so the loop stops |
| `loop_variable` | L2 | way: line by line trace | i starts at 1; 1 < 5 is true, the body i++ makes i 2, the update makes it 3; 3 < 5 is true, the body makes it 4, the update makes it 5; 5 < 5 is false |
| `println` | L3 | way: relation to neighbour | Only i++ was in the loop; Then the two println lines print 5 and 5 |

Generic concepts with a level (not counted as components): `statement` L3.
