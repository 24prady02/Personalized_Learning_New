# LP17: how the overall level was calculated

This page shows only the overall level of this answer and how it was calculated. Every step of the run (what the graph offered, the model's replies, the labels, the figures) is in the notebook [`LP17.ipynb`](LP17.ipynb) and in `report.html`; the rule itself is explained in the [folder README](../../README.md).

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

Student's answer: It does not compile. Line 1 and line 4 are missing the ; at the end, so javac reports ';' expected. After those are fixed, system.out still fails because Java is case-sensitive: there is no package called system, it must be System. Even then the indentation is misleading: without braces only i++ is in the loop, a silent logic error whenever a braceless loop is followed by indented lines.

## Overall level

This scenario tests **L4: diagnose an error**. How the overall level is decided is explained in the [folder README](../../README.md).

- **Overall level: L4** (decided by: largest share)
- **Shares of the components:** L3 0.20, L4 0.80; coherent
- **Mistake held (root cause):** none
- **Expected by design:** overall L4; components `for_loop` L4, `statement` L4, `identifier` L4; held none; root none
- **Overall level matches the expected one:** yes

### How the overall level of this run was calculated

1. **Find the parts of the answer.** The answer touches 5 concepts (the components in the table below). Each one got its own level from what the student wrote about it.
2. **Is a real mistake held?** No wrong rule is held.
3. **Count the parts at each level:** 1 at L3, 4 at L4.
4. **Result.** Most parts (4 of 5) are at L4, so the overall level is **L4**.
5. **Check.** The levels of the parts are next to each other, so the answer is coherent.

| Component | Level | Decided by | Student's words |
|---|---|---|---|
| `compile_time_error` | L4 | way: diagnose an error | It does not compile; Line 1 and line 4 are missing the; at the end; so javac reports; expected |
| `control_flow` | L3 | way: relation to neighbour | Even then the indentation is misleading: without braces only i++ is in the loop, a silent logic error whenever a braceless loop is followed by indented lines |
| `for_loop` | L4 | way: diagnose an error | Even then the indentation is misleading: without braces only i++ is in the loop, a silent logic error whenever a braceless loop is followed by indented lines |
| `loop_body` | L4 | way: diagnose an error | Even then the indentation is misleading: without braces only i++ is in the loop, a silent logic error whenever a braceless loop is followed by indented lines |
| `println` | L4 | way: diagnose an error | After those are fixed, system.out still fails; because Java is case-sensitive: there is no package called system, it must be System |

Generic concepts with a level (not counted as components): `statement` L4.
