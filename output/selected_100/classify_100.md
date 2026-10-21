# Classifying 100 student answers on the Chapter-1 learning ladder (L0-L4)

You are an experienced Java teacher. For each of the 100 student answers below, give the level the answer
shows on a 5-level learning ladder (L0-L4), or "none" if the answer makes no claim.

How to decide:
- Use only the level definitions and boundary rules below.
- Work out what the code really does (its run output is given where it could be run) and whether the
  student's reasoning is correct before you decide.
- Mark the answer as a whole, for the main thing the question part asks.
- Judge each answer on its own.

Reply with one table and nothing else, one row per answer, in the order given:

| ID | Level | Why (one sentence) |
|----|-------|--------------------|
| S088 | L2 | ... |


## Level definitions

L0 (Prestructural): An answer is at L0 for the concept when it shows no working model of the concept: it reads the code with everyday or maths meanings, applies a documented wrong rule, or traces it accurately only now and then.
   Deciding question: Does every rule the answer applies to the concept agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.
L1 (Unistructural): An answer is at L1 for the concept when it grasps one correct aspect of the concept: it names or describes one part of the given code, or states the rule of the concept, without covering all parts or applying the rule to the values.
   Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.
L2 (Multistructural): An answer is at L2 for the concept when it covers all parts of the code that use the concept, line by line or value by value, without relating them to what the code is for. It may be correct, or a multistructural error.
   Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.
L3 (Relational): An answer is at L3 for the concept when it integrates the parts into one structure: it relates the concept to another construct in the same code, or states in one sentence what the code does, deduced from the code. It may be correct, or a relational error.
   Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?
L4 (Extended abstract (concrete-operational reversibility and conservation)): An answer is at L4 for the concept when it goes beyond the given code with the rule of the concept: it predicts a change by reasoning about what is conserved, states the class of inputs under which an error shows, or solves an unseen problem.
   Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.

## Boundary rules from the knowledge graph (apply them):
- Reading the code with everyday meanings, or using a rule that contradicts Java, is L0, even with Java words.
- Copying the code back word for word with no interpretation is L0.
- A single slip in an otherwise rule-correct trace is L2 with an error, not L0.
- Naming the element, or stating one correct rule or definition without applying it to this code, is L1.
- A bare correct result or output with no justification is L1 (a correct output is not levelled above L1 on its own).
- Applying the rules to this code's values or lines, in order, with justification, is L2.
- Relating the concept to another construct, or stating the purpose of the code, with a reason, is L3.
  A relational answer may be correct or a relational error.
- Locating and fixing the mistake for one given failing case is L3.
- Correct reasoning about code, an input or a change that is NOT in the given code (predicting the effect of a
  change, diagnosing a class of error, writing correct new code) is L4. New code must be correct to be L4.
- A student's question that makes no claim is not levelled: "none".

## The 100 answers

### 1. S001

**Question (the part the student answers):**

What is the exact output, including line breaks? Explain how you got it.

**Code:**

```java
System.out.print("Welcome to Java. This is ");
System.out.println("A nice programming language ");
System.out.print("that I have to learn.");
```

**Output of running the code:**

```
Welcome to Java. This is A nice programming language 
that I have to learn.
```

**Student answer:**

> println adds a newline after the text and print does not.

### 2. S002

**Question (the part the student answers):**

What is the exact output, including line breaks? Explain how you got it.

**Code:**

```java
System.out.print("Welcome to Java. This is ");
System.out.println("A nice programming language ");
System.out.print("that I have to learn.");
```

**Output of running the code:**

```
Welcome to Java. This is A nice programming language 
that I have to learn.
```

**Student answer:**

> Welcome to Java. This is A nice programming language
> that I have to learn.

### 3. S004

**Question (the part the student answers):**

What is printed when x = 17? Explain.

**Code:**

```java
System.out.print("A");
if (x % 2 == 0) {
  System.out.print("B");
  if (x % 5 == 2) { System.out.print("C"); } else { System.out.print("D"); }
} else {
  if (x % 5 == 2) { System.out.print("E"); } else { System.out.print("F"); }
  System.out.print("G");
}
```

**Output of running the code:**

```
AEG
```

**Student answer:**

> It prints A, goes to the odd part and prints the letters there.

### 4. S005

**Question (the part the student answers):**

What is the output? Explain. (b) What if i started at 61?

**Code:**

```java
int i = 81;
do {
  if (i % 2 == 1 && i != 73) {
    System.out.printf("%d ", i);
  }
  i--;
} while (i >= 70);
```

**Output of running the code:**

```
81 79 77 75 71
```

**Student answer:**

> With a while loop the output is the same here, because 81 >= 70 is true at the start; it would only differ if i started below 70.

### 5. S007

**Question (the part the student answers):**

Give the exact output, including spacing and empty lines. Explain.

**Code:**

```java
for (int i = 3; i >= 0; i--) {
  for (int j = i; j > 0; j--) {
    System.out.printf("%d ", j);
  }
  System.out.println();
}
```

**Output of running the code:**

```
3 2 1 
2 1 
1
```

**Student answer:**

> 3 2 1 / 2 1 / 1" (no empty line at the end), "because the loop stops at 1.

### 6. S008

**Question (the part the student answers):**

What is the output? Trace i, num1 and num2. (b) Rewrite it with a for loop.

**Code:**

```java
int num = 8, num1 = num + 1, num2 = num1 + 3;
int i = num;
do {
  if (i != num1 && i != num2) {
    System.out.printf("%d, ", i);
  } else {
    num2--;
  }
  i++;
} while (i < 14);
```

**Output of running the code:**

```
8, 10, 12, 13,
```

**Student answer:**

> num1 is 9 and num2 starts at 12. At i = 9 num2 drops to 11; at i = 11 it drops to 10. So it prints 8, 10, 12, 13,

### 7. S009

**Question (the part the student answers):**

Assign 7.9 to the next-to-last position without hard-coding the index.

**Code:**

```java
(writing task) double array sensorReadings already exists
```

**Output of running the code:**

```
(not run: no runnable code, or it needs input)
```

**Student answer:**

> sensorReadings[sensorReadings.length - 2] = 7.9; — the last index is length - 1, so next-to-last is length - 2.

### 8. S010

**Question (the part the student answers):**

Make an exact copy of data2 (no System.arraycopy).

**Code:**

```java
(writing task) int array data2 already exists
```

**Output of running the code:**

```
(not run: no runnable code, or it needs input)
```

**Student answer:**

> for (int i = 0; i <= data2.length; i++) copy[i] = data2[i];

### 9. S012

**Question (the part the student answers):**

Show three different statements that add 1 to count and store the result in count.

**Code:**

```java
(writing task) int variable count already exists
```

**Output of running the code:**

```
(not run: no runnable code, or it needs input)
```

**Student answer:**

> Is count++ the same as count += 1?

### 10. S013

**Question (the part the student answers):**

Rewrite this if-else as one line using the conditional operator.

**Code:**

```java
if (inValue >= 0) {
  outputValue = 100;
} else {
  outputValue = -50;
}
```

**Output of running the code:**

```
(not run: no runnable code, or it needs input)
```

**Student answer:**

> outputValue = (inValue >= 0) ? 100 : -50;

### 11. S014

**Question (the part the student answers):**

Which values of p and q make p && q true? Which make p || q false? Explain.

**Code:**

```java
(boolean variables p and q exist)
```

**Output of running the code:**

```
(not run: no runnable code, or it needs input)
```

**Student answer:**

> p && q is true only when both are true; p || q is false only when both are false.

### 12. S015

**Question (the part the student answers):**

Declare a variable named singleLetter that holds one letter, with initial value Q, following Java convention.

**Code:**

```java
(writing task)
```

**Output of running the code:**

```
(not run: no runnable code, or it needs input)
```

**Student answer:**

> char SingleLetter = 'Q';

### 13. S016

**Question (the part the student answers):**

What is the exact output? Explain how num4 is computed.

**Code:**

```java
int num1 = 9, num2 = 5;
double num3 = 26.3;
double num4 = (num1 % num2) + num3;
System.out.println("Result is ");
System.out.println("num4 = " + num4);
```

**Output of running the code:**

```
Result is 
num4 = 30.3
```

**Student answer:**

> num4 = 30.3, because 9 % 5 means 9 minus 5, which is 4.

### 14. S017

**Question (the part the student answers):**

Give the exact output, including spacing and empty lines. Explain.

**Code:**

```java
for (int i = 3; i >= 0; i--) {
  for (int j = i; j > 0; j--) {
    System.out.printf("%d ", j);
  }
  System.out.println();
}
```

**Output of running the code:**

```
3 2 1 
2 1 
1
```

**Student answer:**

> i = 3 prints 3 2 1, i = 2 prints 2 1, and so on.

### 15. S020

**Question (the part the student answers):**

Find and print the smallest value in data.

**Code:**

```java
(writing task) double array data already exists
```

**Output of running the code:**

```
(not run: no runnable code, or it needs input)
```

**Student answer:**

> best = first; for each element: if smaller than best → best = element; print best

### 16. S021

**Question (the part the student answers):**

What is printed when x = 17? Explain.

**Code:**

```java
System.out.print("A");
if (x % 2 == 0) {
  System.out.print("B");
  if (x % 5 == 2) { System.out.print("C"); } else { System.out.print("D"); }
} else {
  if (x % 5 == 2) { System.out.print("E"); } else { System.out.print("F"); }
  System.out.print("G");
}
```

**Output of running the code:**

```
AEG
```

**Student answer:**

> So first Java looks at the code and the first thing it does is print A, which always happens no matter what x is, and then it checks whether x is even, and 17 is not even because 17 divided by 2 leaves 1, so it skips the whole first part with B, C and D, and goes to the else part, where it checks 17 % 5, which is 2, so it prints E, and then after that inner if-else it prints G, so overall I think the answer would be AEG, which makes sense because…

### 17. S022

**Question (the part the student answers):**

What is the output? Explain when the loop stops.

**Code:**

```java
int i = 1;
boolean isDone = false;
while (i < 100 && !isDone) {
  System.out.print(i + " ");
  if (i % 5 == 0) { isDone = true; }
  i = i + 3;
}
```

**Output of running the code:**

```
1 4 7 10
```

**Student answer:**

> It keeps jumping up by 3 and quits after the pass where it hits a multiple of 5.

### 18. S023

**Question (the part the student answers):**

If value is 2, what is result after the switch? Explain.

**Code:**

```java
switch (value) {
case 1: result = 10;
case 2:
case 3: result = 20;
case 4: result = 40;
default: result = 50;
}
```

**Output of running the code:**

```
(not run: no runnable code, or it needs input)
```

**Student answer:**

> the swich no have break so it go down all the case and result become 50

### 19. S026

**Question (the part the student answers):**

Explain in plain English what these three lines do.

**Code:**

```java
int t = a;
a = b;
b = t;
```

**Output of running the code:**

```
(not run: no runnable code, or it needs input)
```

**Student answer:**

> a becomes b and b becomes a.

### 20. S028

**Question (the part the student answers):**

What is the exact output? Explain how num4 is computed.

**Code:**

```java
int num1 = 9, num2 = 5;
double num3 = 26.3;
double num4 = (num1 % num2) + num3;
System.out.println("Result is ");
System.out.println("num4 = " + num4);
```

**Output of running the code:**

```
Result is 
num4 = 30.3
```

**Student answer:**

> remainder modulus widening double concatenation println newline

### 21. S034

**Question (the part the student answers):**

Declare a variable named singleLetter that holds one letter, with initial value Q, following Java convention.

**Code:**

```java
(writing task)
```

**Output of running the code:**

```
(not run: no runnable code, or it needs input)
```

**Student answer:**

> Why does Java have both char and String?

### 22. S036

**Question (the part the student answers):**

Find and print the smallest value in data.

**Code:**

```java
(writing task) double array data already exists
```

**Output of running the code:**

```
(not run: no runnable code, or it needs input)
```

**Student answer:**

> double min = data[0]; for (double v : data) min = Math.min(min, v); System.out.println(min);

### 23. S037

**Question (the part the student answers):**

Give the output and explain it, addressing parameter passing.

**Code:**

```java
public static void swap(int num1, int num2) {
  int temp = num1; num1 = num2; num2 = temp;
  System.out.printf("in swap: num1 = %d num2 = %d%n", num1, num2);
}
// main: int num1 = 7; int num2 = 42; swap(num1, num2);
// System.out.printf("in main: num1 = %d num2 = %d", num1, num2);
```

**Output of running the code:**

```
(not run: no runnable code, or it needs input)
```

**Student answer:**

> in swap: num1 = 42 num2 = 7, then in main: num1 = 7 num2 = 42. Java passes copies of the values, so main's variables do not change.

### 24. S038

**Question (the part the student answers):**

Give the output. In what order are the methods called?

**Code:**

```java
int scaleValue = -11, total = 0;
total = update(scaleValue);
println("num1 = " + scaleValue); println("num2 = " + total);
// update(s): s = 25 + reCalculate(s); return s;
// reCalculate(v): v += 10; v = finalAdjust(v) / 2; return v;
// finalAdjust(v): v = (v >= 0) ? v + 6 : v - 9; return v;
```

**Output of running the code:**

```
(not run: no runnable code, or it needs input)
```

**Student answer:**

> finalAdjust(-1) gives 5, so reCalculate returns 2 and num2 = 27.

### 25. S039

**Question (the part the student answers):**

Return the index of the LAST occurrence of key, or -1 if it is not found.

**Code:**

```java
public static int linearSearch(int[] arr, double key) { ... }
```

**Output of running the code:**

```
(not run: no runnable code, or it needs input)
```

**Student answer:**

> for (...) { if (arr[i] == key) return i; else return -1; }

### 26. S041

**Question (the part the student answers):**

What is printed? Explain.

**Code:**

```java
String name = "java";
name.toUpperCase();
System.out.println(name);
```

**Output of running the code:**

```
java
```

**Student answer:**

> JAVA, because toUpperCase changes name.

### 27. S042

**Question (the part the student answers):**

Write calculateMPG that returns miles per gallon.

**Code:**

```java
(writing task) calculateMPG(double miles, double gallons)
```

**Output of running the code:**

```
(not run: no runnable code, or it needs input)
```

**Student answer:**

> public static double calculateMPG(double miles, double gallons) { double mpg = miles / gallons; }

### 28. S043

**Question (the part the student answers):**

A classmate says both i and c break the naming convention. Is that right? Rename only what needs renaming, and say whether the output changes.

**Code:**

```java
int[] scores = {72, 45, 90, 60};
int c = 0;
for (int i = 0; i < scores.length; i++) {
  if (scores[i] >= 60) { c++; }
}
System.out.println(c);
```

**Output of running the code:**

```
3
```

**Student answer:**

> i is fine because it is only the loop index. c should be passCount, since it counts the passing scores. It still prints 3.

### 29. S047

**Question (the part the student answers):**

What is printed, exactly (count the spaces)? Explain each format specifier.

**Code:**

```java
double price = 3.14159;
System.out.printf("%6.2f", price);
System.out.printf("|%d items%n", 4);
```

**Output of running the code:**

```
3.14|4 items
```

**Student answer:**

> With %.3f it would print 3.142 and no spaces. price itself is still 3.14159; only the printed digits change.

### 30. S048

**Question (the part the student answers):**

(a) What is printed for the input 5 3 8? (b) For empty input? (c) For the input 5 3 abc?

**Code:**

```java
int sum = 0, count = 0;
while (!StdIn.isEmpty()) {
  int x = StdIn.readInt();
  sum += x;
  count++;
}
StdOut.println(sum + " " + count);
```

**Output of running the code:**

```
16 3
```

**Student answer:**

> (c) It prints 8 2 and skips abc.

### 31. S049

**Question (the part the student answers):**

(a) What is printed for the input 5 3 8? (b) For empty input? (c) For the input 5 3 abc?

**Code:**

```java
int sum = 0, count = 0;
while (!StdIn.isEmpty()) {
  int x = StdIn.readInt();
  sum += x;
  count++;
}
StdOut.println(sum + " " + count);
```

**Output of running the code:**

```
16 3
```

**Student answer:**

> I read two numbers in each pass and with 5 3 8 it crashes at the end. Why?

### 32. S050

**Question (the part the student answers):**

(a) What is printed for the input 5 3 8? (b) For empty input? (c) For the input 5 3 abc?

**Code:**

```java
int sum = 0, count = 0;
while (!StdIn.isEmpty()) {
  int x = StdIn.readInt();
  sum += x;
  count++;
}
StdOut.println(sum + " " + count);
```

**Output of running the code:**

```
16 3
```

**Student answer:**

> StdIn is a variable that holds all the numbers, like an array.

### 33. S051

**Question (the part the student answers):**

What is printed for the input 4 -2 6 99999 3? (b) What if the first value is 99999?

**Code:**

```java
int sum = 0, count = 0;
int v = StdIn.readInt();
while (v != 99999) {
  if (v >= 0) { sum += v; count++; }
  v = StdIn.readInt();
}
if (count > 0) { StdOut.println((double) sum / count); }
```

**Output of running the code:**

```
5.0
```

**Student answer:**

> I removed if (v >= 0) because rain values are always fine.

### 34. S052

**Question (the part the student answers):**

What appears in the terminal after each command? What does args[] contain when Average runs?

**Code:**

```java
% java RandomSeq 5 > data.txt
% java Average < data.txt
% java RandomSeq 5 | java Average
(RandomSeq N prints N random numbers; Average reads numbers from standard input and prints their average)
```

**Output of running the code:**

```
(not run: no runnable code, or it needs input)
```

**Student answer:**

> 1: nothing, the numbers go into data.txt. 2: the average. 3: an average of 5 new numbers, no file. args is empty.

### 35. S054

**Question (the part the student answers):**

What appears in the terminal after each command? What does args[] contain when Average runs?

**Code:**

```java
% java RandomSeq 5 > data.txt
% java Average < data.txt
% java RandomSeq 5 | java Average
(RandomSeq N prints N random numbers; Average reads numbers from standard input and prints their average)
```

**Output of running the code:**

```
(not run: no runnable code, or it needs input)
```

**Student answer:**

> Do I need to change my program to read from a file?

### 36. S057

**Question (the part the student answers):**

What does p hold after the loop? Is it a probability row? Fix it if needed.

**Code:**

```java
int[] counts = {0, 0, 2, 2, 1};
int outDegree = 5;
double[] p = new double[5];
for (int j = 0; j < 5; j++) {
  p[j] = counts[j] / outDegree;
}
```

**Output of running the code:**

```
(not run: no runnable code, or it needs input)
```

**Student answer:**

> All zeros, because int / int is integer division. Cast: (double) counts[j] / outDegree gives 0, 0, 0.4, 0.4, 0.2, which sums to 1.

### 37. S060

**Question (the part the student answers):**

What does p hold after the loop? Is it a probability row? Fix it if needed.

**Code:**

```java
int[] counts = {0, 0, 2, 2, 1};
int outDegree = 5;
double[] p = new double[5];
for (int j = 0; j < 5; j++) {
  p[j] = counts[j] / outDegree;
}
```

**Output of running the code:**

```
(not run: no runnable code, or it needs input)
```

**Student answer:**

> An all-zero row is fine; it just means the page has no links.

### 38. S061

**Question (the part the student answers):**

What is next? (b) What if row were {0.1, 0.3, 0.5} and r = 0.95?

**Code:**

```java
double[] row = {0.1, 0.3, 0.6};
double r = 0.35;
double sum = 0.0;
int next = -1;
for (int j = 0; j < row.length; j++) {
  sum += row[j];
  if (r < sum) { next = j; break; }
}
```

**Output of running the code:**

```
(not run: no runnable code, or it needs input)
```

**Student answer:**

> sum is 0.1 then 0.4; 0.35 < 0.4 so next = 1. (b) the sums only reach 0.9, so next stays -1 because the row does not add to 1.

### 39. S065

**Question (the part the student answers):**

Are these the page ranks? Would starting at page 3 change them?

**Code:**

```java
RandomSurfer was run for 100 moves starting at page 0 and printed:
0.31000 0.25000 0.14000 0.24000 0.06000
```

**Output of running the code:**

```
(not run: no runnable code, or it needs input)
```

**Student answer:**

> Only estimates; 100 moves is far too few and the zeros mean nothing. In the long run the start page does not matter.

### 40. S068

**Question (the part the student answers):**

Are these the page ranks? Would starting at page 3 change them?

**Code:**

```java
RandomSurfer was run for 100 moves starting at page 0 and printed:
0.31000 0.25000 0.14000 0.24000 0.06000
```

**Output of running the code:**

```
(not run: no runnable code, or it needs input)
```

**Student answer:**

> They are estimates. But starting at page 3 would change the ranks.

### 41. S069

**Question (the part the student answers):**

(a) Does page 1 link to page 0? (b) Is newRank the page rank?

**Code:**

```java
tiny.txt contains the line  0 1
rank = {1, 0, 0, 0, 0};  after one vector-matrix multiplication, newRank equals row 0 of p
```

**Output of running the code:**

```
(not run: no runnable code, or it needs input)
```

**Student answer:**

> (a) No, 0 1 is only a link from 0 to 1. (b) No, it is where you are after one move; you keep multiplying until it stops changing.

### 42. S073

**Question (the part the student answers):**

If value is 2, what is result after the switch? Explain.

**Code:**

```java
switch (value) {
case 1: result = 10;
case 2:
case 3: result = 20;
case 4: result = 40;
default: result = 50;
}
```

**Output of running the code:**

```
(not run: no runnable code, or it needs input)
```

**Student answer:**

> Turn 1: "result is 20."
> Probe: "If value is 1, what is result?"
> Turn 2: "10. Oh wait, then 20, 40, 50… so for 2 it is 50 too."

### 43. S076

**Question (the part the student answers):**

Make an exact copy of data2 (no System.arraycopy).

**Code:**

```java
(writing task) int array data2 already exists
```

**Output of running the code:**

```
(not run: no runnable code, or it needs input)
```

**Student answer:**

> int[] copy = new int[data2.length()]; for (int i = 0; i < data2.length(); i++) copy[i] = data2[i];

### 44. S080

**Question (the part the student answers):**

What goes wrong, and in what order will the student meet each problem? Which line(s) never run?

**Code:**

```java
// saved as Hello.java, run as:  java Greeting Ann
public class Greeting {
  public static void main(String[] args) {
    System.out.println("Hi, " + args[1])
    // System.out.println("Bye");
  }
}
```

**Output of running the code:**

```
(not run: no runnable code, or it needs input)
```

**Student answer:**

> Two compile errors first: the class must be in Greeting.java and the ; is missing. After that it compiles, but args[1] crashes at run time because Ann is args[0]. The comment never runs.

### 45. S084

**Question (the part the student answers):**

What is printed by  java Order 3 ? By  java Order five ?

**Code:**

```java
public class Order {
  public static void main(String[] args) {
    int n = Integer.parseInt(args[0]);
    System.out.println("start");
    if (n > 5)
      System.out.println("big");
      System.out.println("done");
  }
}
```

**Output of running the code:**

```
(not run: no runnable code, or it needs input)
```

**Student answer:**

> Only start, because done is inside the if and 3 is not > 5.

### 46. S088

**Question (the part the student answers):**

After javac Big.java succeeds, what has happened and what has not?

**Code:**

```java
A student writes all 200 lines of Big.java, then runs  javac Big.java  for the first time and gets 37 error messages.
```

**Output of running the code:**

```
(not run: no runnable code, or it needs input)
```

**Student answer:**

> There is a Big.class file now, but nothing is printed because the program has not run yet.

### 47. S089

**Question (the part the student answers):**

Why would compiling and testing in small steps have helped?

**Code:**

```java
A student writes all 200 lines of Big.java, then runs  javac Big.java  for the first time and gets 37 error messages.
```

**Output of running the code:**

```
(not run: no runnable code, or it needs input)
```

**Student answer:**

> If you compile after every few lines, each error is next to the code you just wrote, so it is easy to find.

### 48. S091

**Question (the part the student answers):**

A classmate wrote  System.out.println("Hi there);  What happens and why?

**Code:**

```java
public class Hello {
  public static void main(String[] args) {
    // greet
    System.out.print("Hi");
    System.out.println(" there");
  }
}
```

**Output of running the code:**

```
Hi there
```

**Student answer:**

> It will not compile: the string has no closing quote, so Java says unclosed string literal.

### 49. S092

**Question (the part the student answers):**

(a) Name the part  public class Hello { ... }  and say which file it must be in.
(b) What is printed?
(c) Why does  java Hello  start at main, and what happens if main is written as  public static void main() ?
(d) A classmate wrote  System.out.println("Hi there);  What happens and why?

**Code:**

```java
public class Hello {
  public static void main(String[] args) {
    // greet
    System.out.print("Hi");
    System.out.println(" there");
  }
}
```

**Output of running the code:**

```
Hi there
```

**Student answer:**

> main() without String[] args is fine because the program uses no arguments.

### 50. S093

**Question (the part the student answers):**

Fix it so it prints 5.5.

**Code:**

```java
// goal: print the average of 4 and 7
int a = 4, b = 7;
double avg = a + b / 2;
System.out.println(avg);
```

**Output of running the code:**

```
7.0
```

**Student answer:**

> Use (a + b) / 2.0: parentheses for the order and 2.0 so the division is not integer division.

### 51. S094

**Question (the part the student answers):**

What happens with  java Twice  (no argument)?

**Code:**

```java
public class Twice {
  public static void main(String[] args) {
    int n = Integer.parseInt(args[0]);
    System.out.println(args[0] + args[0] + " " + 2 * n);
  }
}
% java Twice 21
```

**Output of running the code:**

```
(not run: no runnable code, or it needs input)
```

**Student answer:**

> It crashes when it runs, because args is empty and args[0] is out of bounds.

### 52. S095

**Question (the part the student answers):**

Which of int, double, boolean, char, String is not a primitive type?

**Code:**

```java
final double TAX = 0.08;
int a, b;
a = b = 5;
double total = a * 2 + 1.5;
total = total + total * TAX;
```

**Output of running the code:**

```
(not run: no runnable code, or it needs input)
```

**Student answer:**

> String; it is a class. The other four are primitive.

### 53. S097

**Question (the part the student answers):**

Give the three lines printed.

**Code:**

```java
char c = 'A';
int n = c + 2;
char d = (char) (c + 2);
System.out.println(n + "\t" + d);
System.out.println("A" + 1 + 2);
System.out.println('A' + 1 + "2");
```

**Output of running the code:**

```
67	C
A12
662
```

**Student answer:**

> 67, a tab, C; then A12; then 662.

### 54. S098

**Question (the part the student answers):**

What is  Math.abs(Integer.MIN_VALUE) ?

**Code:**

```java
int max = Integer.MAX_VALUE;   // 2147483647
int over = max + 1;
long big = max + 1L;
int neg = -7 / 2;
int rem = -7 % 2;
int sq = 3 ^ 2;
```

**Output of running the code:**

```
(not run: no runnable code, or it needs input)
```

**Student answer:**

> Still -2147483648, because +2147483648 does not fit in an int.

### 55. S099

**Question (the part the student answers):**

(a) What number is 6.02e23?
(b) Give the first three lines printed.
(c) Why is x == 0.3 false, and how should two doubles be compared?
(d) What happens at the last line, and how is it different from 1.0 / 0?
(e) How do int and double differ for 7 / 2 and 7.0 / 2?

**Code:**

```java
double x = 0.1 + 0.2;
System.out.println(x == 0.3);
System.out.println(1.0 / 0);
System.out.println(6.02e23 > 1e23);
int z = 0;
System.out.println(5 / z);
```

**Output of running the code:**

```
false
Infinity
true
```

**Student answer:**

> 6.02e23 is 6.02 times e to the power 23.

### 56. S100

**Question (the part the student answers):**

(a) What number is 6.02e23?
(b) Give the first three lines printed.
(c) Why is x == 0.3 false, and how should two doubles be compared?
(d) What happens at the last line, and how is it different from 1.0 / 0?
(e) How do int and double differ for 7 / 2 and 7.0 / 2?

**Code:**

```java
double x = 0.1 + 0.2;
System.out.println(x == 0.3);
System.out.println(1.0 / 0);
System.out.println(6.02e23 > 1e23);
int z = 0;
System.out.println(5 / z);
```

**Output of running the code:**

```
false
Infinity
true
```

**Student answer:**

> Dividing by zero gives an error.

### 57. S101

**Question (the part the student answers):**

What does ^ do on two booleans?

**Code:**

```java
int n = 0;
boolean a = (n != 0) && (10 / n > 1);
boolean b = !(n > 5 && n < 10);
boolean c = (n > 5) ^ (n < 10);
System.out.println(a + " " + b + " " + c);
```

**Output of running the code:**

```
false true true
```

**Student answer:**

> It gives true when the two sides are different.

### 58. S103

**Question (the part the student answers):**

What does  int k2 = Math.round(2.5);  do?

**Code:**

```java
double r = Math.random();
int die = (int) (r * 6) + 1;
long k = Math.round(2.5);
double s = Math.sin(Math.PI / 6);
double h = Math.sqrt(16);
int m = Math.max(3, 7);
```

**Output of running the code:**

```
(not run: no runnable code, or it needs input)
```

**Student answer:**

> It does not compile, since round gives a long.

### 59. S104

**Question (the part the student answers):**

Which line converts automatically, and which needs a cast?

**Code:**

```java
int i = 7;
double d = i;
int j = (int) 9.99;
double q = (double) (i / 2);
double r = (double) i / 2;
int p = Integer.parseInt("42") + 1;
String t = "" + i + 1;
```

**Output of running the code:**

```
(not run: no runnable code, or it needs input)
```

**Student answer:**

> d = i happens by itself because double is bigger; going from 9.99 to int needs (int).

### 60. S106

**Question (the part the student answers):**

List what runs, in order, and what is printed.

**Code:**

```java
// pseudocode: if the score is at least 50 say "pass", otherwise say "fail"; always say "done"
int score = 42;
if (score >= 50) {
  System.out.println("pass");
}
System.out.println("done");
```

**Output of running the code:**

```
done
```

**Student answer:**

> score gets 42, the if test is false so pass is skipped, then done is printed.

### 61. S107

**Question (the part the student answers):**

(a) In the template  if (<boolean expression>) <statement>,  what may replace <boolean expression>?
(b) What is printed?
(c) Why is positive printed although x is negative?
(d) What is printed if x = 5?
(e) Fix the code so positive is printed only for positive x.
(f) What would happen if the second if were a while?

**Code:**

```java
int x = -3;
if (x > 0);
  System.out.println("positive");
if (x < 0)
  System.out.println("negative");
  System.out.println("checked");
```

**Output of running the code:**

```
positive
negative
checked
```

**Student answer:**

> positive is not printed, because x > 0 is false.

### 62. S108

**Question (the part the student answers):**

Give y, w and x at the end.

**Code:**

```java
int total = 0;
for (int i = 10; i > 0; i -= 4) {
  total += i;
}
int x = 5;
int y = x++;
int w = ++x;
int z = 7;
z += 0.5;
```

**Output of running the code:**

```
(not run: no runnable code, or it needs input)
```

**Student answer:**

> y is 5, then x is 6, then ++x makes it 7, so w is 7 and x is 7.

### 63. S109

**Question (the part the student answers):**

What is printed for t = 5?

**Code:**

```java
int t = 25;
if (t > 10)
  if (t > 30)
    System.out.println("hot");
else
  System.out.println("cold");
if (t > 30) System.out.println("A");
else if (t > 20) System.out.println("B");
else if (t > 10) System.out.println("C");
```

**Output of running the code:**

```
cold
B
```

**Student answer:**

> Nothing at all, because the outer if fails and the else is part of the inner if.

### 64. S110

**Question (the part the student answers):**

Which variable is an accumulator and which is a counter?

**Code:**

```java
int[] v = {3, 8, 5, 8};
int sum = 0, count = 0;
for (int i = 0; i < v.length; i++) {
  sum += v[i];
  if (v[i] == 8) count++;
}
System.out.print(v[0]);
for (int i = 1; i < v.length; i++) System.out.print(", " + v[i]);
System.out.println();
```

**Output of running the code:**

```
3, 8, 5, 8
```

**Student answer:**

> sum builds a total, count counts.

### 65. S111

**Question (the part the student answers):**

A classmate always gets 0.0. Their test is  (int) Math.random() * 6 + 1 == 6.  Find the cause by reasoning.

**Code:**

```java
// estimate the chance that a die shows 6
int trials = 1000, sixes = 0;
for (int t = 0; t < trials; t++) {
  if ((int) (Math.random() * 6) + 1 == 6) sixes++;
}
System.out.println((double) sixes / trials);
```

**Output of running the code:**

```
0.172
```

**Student answer:**

> The cast happens first, so (int) Math.random() is 0 and the die is always 1. Cast after multiplying.

### 66. S112

**Question (the part the student answers):**

How do break and continue differ in the first loop?

**Code:**

```java
int sum = 0;
for (int i = 1; i <= 6; i++) {
  if (i % 2 == 0) continue;
  if (i == 5) break;
  sum += i;
  System.out.print(i + ",");
}
System.out.println(" sum=" + sum);
outer:
for (int r = 0; r < 3; r++)
  for (int c = 0; c < 3; c++) {
    if (c == r) continue outer;
    if (r == 2) break outer;
    System.out.print(r + "" + c + " ");
  }
```

**Output of running the code:**

```
1,3, sum=4
10
```

**Student answer:**

> continue jumps to the next i for the even numbers, break stops the loop completely at 5.

### 67. S113

**Question (the part the student answers):**

What is an infinite loop?

**Code:**

```java
int i = 0;
while (i < 10) {
  System.out.print(i);
  i += 0.5;
}
```

**Output of running the code:**

```
000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
... (output cut: 886315 characters in all)
```

**Student answer:**

> A loop that never stops because its condition stays true.

### 68. S114

**Question (the part the student answers):**

Why can a[0] be printed when a local  int x;  without a value cannot?

**Code:**

```java
int[] a;
a = new int[4];
a[1] = 7;
boolean[] seen = new boolean[3];
int[] empty = new int[0];
System.out.println(a[0] + " " + a[1] + " " + a.length + " " + seen[2] + " " + empty.length);
```

**Output of running the code:**

```
0 7 4 false 0
```

**Student answer:**

> new fills the array with 0s, but a local variable has no value until you give it one.

### 69. S115

**Question (the part the student answers):**

What does  System.out.println(a);  show?

**Code:**

```java
int[] a = {4, 8, 15};
int[] b = a;
int[] c = {4, 8, 15};
b[0] = 99;
System.out.println(a[0] + " " + (a == b) + " " + (a == c));
System.out.println(a);
int i = 0;
while (i < a.length && a[i] != 15) i++;
System.out.println(i);
```

**Output of running the code:**

```
99 true false
[I@61f8bee4
2
```

**Student answer:**

> Something like [I@ and a hex code, not the numbers.

### 70. S116

**Question (the part the student answers):**

Write a loop that multiplies every element by 10.

**Code:**

```java
int[] a = {1, 2, 3, 4, 5};
int n = a.length;
for (int i = 0; i < n / 2; i++) {
  int t = a[i]; a[i] = a[n - 1 - i]; a[n - 1 - i] = t;
}
for (int x : a) { x = x * 10; }
for (int x : a) System.out.print(x + " ");
```

**Output of running the code:**

```
5 4 3 2 1
```

**Student answer:**

> for (int i = 0; i < a.length; i++) a[i] = a[i] * 10;

### 71. S117

**Question (the part the student answers):**

Why is t needed in the swap?

**Code:**

```java
// Knuth shuffle of String[] a of length n
for (int i = 0; i < n; i++) {
  int r = i + (int) (Math.random() * (n - i));
  String t = a[i]; a[i] = a[r]; a[r] = t;
}
// a sample of m items: a[0] .. a[m - 1] after the shuffle
```

**Output of running the code:**

```
(not run: no runnable code, or it needs input)
```

**Student answer:**

> Otherwise a[i] is overwritten before it is saved.

### 72. S118

**Question (the part the student answers):**

What is months used for?

**Code:**

```java
String[] months = {"Jan", "Feb", "Mar", "Apr"};
int m = 3;
System.out.println(months[m - 1]);
long[] fact = new long[21];
fact[0] = 1;
for (int i = 1; i <= 20; i++) fact[i] = fact[i - 1] * i;
```

**Output of running the code:**

```
Mar
```

**Student answer:**

> It is a table to look up a month name from its number.

### 73. S119

**Question (the part the student answers):**

What does composite[k] mean, and what is it at the start?

**Code:**

```java
int n = 20;
boolean[] composite = new boolean[n + 1];
for (int i = 2; i * i <= n; i++)
  if (!composite[i])
    for (int j = i * i; j <= n; j += i) composite[j] = true;
for (int i = 2; i <= n; i++) if (!composite[i]) System.out.print(i + " ");
```

**Output of running the code:**

```
2 3 5 7 11 13 17 19
```

**Student answer:**

> It marks whether k is not prime; everything starts as false.

### 74. S120

**Question (the part the student answers):**

Would b × a give the same c?

**Code:**

```java
int[][] a = {{1, 2}, {3, 4}};
int[][] b = {{0, 1}, {1, 0}};
int[][] c = new int[2][2];
for (int i = 0; i < 2; i++)
  for (int j = 0; j < 2; j++)
    for (int k = 0; k < 2; k++)
      c[i][j] += a[i][k] * b[k][j];
int[][][] cube = new int[2][3][4];
```

**Output of running the code:**

```
(not run: no runnable code, or it needs input)
```

**Student answer:**

> No, b times a is 3 4 / 1 2, so the order matters.

### 75. S121

**Question (the part the student answers):**

What are age, rest and name?

**Code:**

```java
// the user types:  42<Enter>  then  Ann Lee<Enter>
int age = StdIn.readInt();
String rest = StdIn.readLine();
String name = StdIn.readLine();
```

**Output of running the code:**

```
(not run: no runnable code, or it needs input)
```

**Student answer:**

> 42, an empty string, and "Ann Lee".

### 76. S122

**Question (the part the student answers):**

Why is rest empty?

**Code:**

```java
// the user types:  42<Enter>  then  Ann Lee<Enter>
int age = StdIn.readInt();
String rest = StdIn.readLine();
String name = StdIn.readLine();
```

**Output of running the code:**

```
(not run: no runnable code, or it needs input)
```

**Student answer:**

> readInt takes 42 but not the Enter, so readLine just finishes that line.

### 77. S123

**Question (the part the student answers):**

A program asks "Again? (y/n)" in a loop. Can it know how many rounds it will run before it starts?

**Code:**

```java
// the user types:  42<Enter>  then  Ann Lee<Enter>
int age = StdIn.readInt();
String rest = StdIn.readLine();
String name = StdIn.readLine();
```

**Output of running the code:**

```
(not run: no runnable code, or it needs input)
```

**Student answer:**

> No, the user decides each time, while it is running.

### 78. S124

**Question (the part the student answers):**

What makes this program a filter?

**Code:**

```java
// Filter: copy only the non-negative numbers from standard input to standard output
while (!StdIn.isEmpty()) {
  int v = StdIn.readInt();
  if (v >= 0) StdOut.print(v + " ");
}
% java RandomInts 6 | java Filter > clean.txt     (RandomInts printed: 4 -1 7 -3 0 2)
```

**Output of running the code:**

```
(not run: no runnable code, or it needs input)
```

**Student answer:**

> It reads from standard input and writes to standard output.

### 79. S125

**Question (the part the student answers):**

What happens without StdDraw.clear()?

**Code:**

```java
StdDraw.setXscale(0, Math.PI);
int N = 4;
double[] x = new double[N + 1], y = new double[N + 1];
for (int i = 0; i <= N; i++) { x[i] = Math.PI * i / N; y[i] = Math.sin(x[i]); }
for (int i = 0; i < N; i++) StdDraw.line(x[i], y[i], x[i + 1], y[i + 1]);
// animation
while (true) {
  StdDraw.clear();
  if (StdDraw.mousePressed()) StdDraw.filledCircle(StdDraw.mouseX(), StdDraw.mouseY(), 0.05);
  StdDraw.show(20);
}
```

**Output of running the code:**

```
(not run: no runnable code, or it needs input)
```

**Student answer:**

> The circles are never erased, so you get a trail.

### 80. S126

**Question (the part the student answers):**

It plays, but the terminal does not come back. Why?

**Code:**

```java
int SR = 44100;
double hz = 440.0, duration = 1.0;
int n = (int) (SR * duration);
double[] a = new double[n + 1];
for (int i = 0; i <= n; i++) a[i] = 0.5 * Math.sin(2 * Math.PI * i * hz / SR);
StdAudio.play(a);
```

**Output of running the code:**

```
(not run: no runnable code, or it needs input)
```

**Student answer:**

> You need System.exit(0) at the end of main.

### 81. S127

**Question (the part the student answers):**

Which page is dangling?

**Code:**

```java
// 3 pages; links 0→1, 1→0, 1→2; page 2 has no outgoing links
// 90-10 rule:  p[i][j] = .90 * counts[i][j] / outDegree[i] + .10 / N
```

**Output of running the code:**

```
(not run: no runnable code, or it needs input)
```

**Student answer:**

> Page 2, it links nowhere.

### 82. S129

**Question (the part the student answers):**

Without the 10% jump, what can happen with a group of pages that only link to each other?

**Code:**

```java
// 3 pages; links 0→1, 1→0, 1→2; page 2 has no outgoing links
// 90-10 rule:  p[i][j] = .90 * counts[i][j] / outDegree[i] + .10 / N
```

**Output of running the code:**

```
(not run: no runnable code, or it needs input)
```

**Student answer:**

> The surfer gets trapped in that group and the other pages get rank 0.

### 83. S132

**Question (the part the student answers):**

(a) List the literals and give the type of each.
(b) Which of int, double, boolean, char, String is not a primitive type?
(c) What is a data type?
(d) Make a trace table of a, b and total after each line.
(e) In  a = b = 5,  which assignment happens first, and why can it be one line?
(f) What happens if you add  int c;  System.out.println(c + 1); ?
(g) Why use TAX instead of 0.08, and what does  TAX = 0.1;  later do?

**Code:**

```java
final double TAX = 0.08;
int a, b;
a = b = 5;
double total = a * 2 + 1.5;
total = total + total * TAX;
```

**Output of running the code:**

```
(not run: no runnable code, or it needs input)
```

**Student answer:**

> a and b are 5 and total is 11.5; after the last line total is still 11.5, because it already has a value.

### 84. S133

**Question (the part the student answers):**

(a) List the literals and give the type of each.
(b) Which of int, double, boolean, char, String is not a primitive type?
(c) What is a data type?
(d) Make a trace table of a, b and total after each line.
(e) In  a = b = 5,  which assignment happens first, and why can it be one line?
(f) What happens if you add  int c;  System.out.println(c + 1); ?
(g) Why use TAX instead of 0.08, and what does  TAX = 0.1;  later do?

**Code:**

```java
final double TAX = 0.08;
int a, b;
a = b = 5;
double total = a * 2 + 1.5;
total = total + total * TAX;
```

**Output of running the code:**

```
(not run: no runnable code, or it needs input)
```

**Student answer:**

> int c; declares c, so c is 0.

### 85. S134

**Question (the part the student answers):**

Explain in plain English what these three lines do.

**Code:**

```java
int t = a;
a = b;
b = t;
```

**Output of running the code:**

```
(not run: no runnable code, or it needs input)
```

**Student answer:**

> After t = a and a = b, a is b. Then b = t means b equals a, so both are b.

### 86. S135

**Question (the part the student answers):**

(a) What values can a boolean hold?
(b) What does ^ do on two booleans?
(c) What is printed?
(d) Why does 10 / n not crash?
(e) Rewrite b without !( ) using De Morgan.
(f) What if && in line 2 were & ?

**Code:**

```java
int n = 0;
boolean a = (n != 0) && (10 / n > 1);
boolean b = !(n > 5 && n < 10);
boolean c = (n > 5) ^ (n < 10);
System.out.println(a + " " + b + " " + c);
```

**Output of running the code:**

```
false true true
```

**Student answer:**

> You could write b as !(5 < n < 10).

### 87. S136

**Question (the part the student answers):**

What is the output? Explain when the loop stops.

**Code:**

```java
int i = 1;
boolean isDone = false;
while (i < 100 && !isDone) {
  System.out.print(i + " ");
  if (i % 5 == 0) { isDone = true; }
  i = i + 3;
}
```

**Output of running the code:**

```
1 4 7 10
```

**Student answer:**

> isDone = (i % 5 == 0); would do the same as the if.

### 88. S137

**Question (the part the student answers):**

What is the exact output, including line breaks? Explain how you got it.

**Code:**

```java
System.out.print("Welcome to Java. This is ");
System.out.println("A nice programming language ");
System.out.print("that I have to learn.");
```

**Output of running the code:**

```
Welcome to Java. This is A nice programming language 
that I have to learn.
```

**Student answer:**

> System.out.println("x is 5"); sets x to 5.

### 89. S138

**Question (the part the student answers):**

What is printed for the input 4 -2 6 99999 3? (b) What if the first value is 99999?

**Code:**

```java
int sum = 0, count = 0;
int v = StdIn.readInt();
while (v != 99999) {
  if (v >= 0) { sum += v; count++; }
  v = StdIn.readInt();
}
if (count > 0) { StdOut.println((double) sum / count); }
```

**Output of running the code:**

```
5.0
```

**Student answer:**

> Add v to sum first, then check if it was negative and subtract it again.

### 90. S139

**Question (the part the student answers):**

Describe what appears in the default window.

**Code:**

```java
StdDraw.square(0.5, 0.5, 0.25);
StdDraw.point(256, 256);
```

**Output of running the code:**

```
(not run: no runnable code, or it needs input)
```

**Student answer:**

> The square uses 0.5 as the centre, but the point uses pixels, so both are in the middle.

### 91. S140

**Question (the part the student answers):**

A classmate says every number here is a magic number and must become a named constant. Is that right?

**Code:**

```java
double area = 3.14159 * r * r;
for (int i = 0; i < n; i++) {
  total = total + 1;
}
```

**Output of running the code:**

```
(not run: no runnable code, or it needs input)
```

**Student answer:**

> Writing 3.14159 in the formula is just as clear as a name.

### 92. S141

**Question (the part the student answers):**

Is this legal Java? Is it good style?

**Code:**

```java
if (x > 0) count++;
```

**Output of running the code:**

```
(not run: no runnable code, or it needs input)
```

**Student answer:**

> Braces are pointless, I never write them.

### 93. S142

**Question (the part the student answers):**

A student says this is wrong because it has no parentheses. Is it? What is r?

**Code:**

```java
int a = 1, b = 2, c = 3;
int r = a + b * c;
```

**Output of running the code:**

```
(not run: no runnable code, or it needs input)
```

**Student answer:**

> Every expression must be fully in parentheses, otherwise Java guesses the order.

### 94. S143

**Question (the part the student answers):**

Is the indentation a problem? What is printed for score = 50?

**Code:**

```java
if (score > 90)
    System.out.println("A");
        System.out.println("great");
```

**Output of running the code:**

```
great
```

**Student answer:**

> Indentation does not matter, I indent however I like.

### 95. S145

**Question (the part the student answers):**

Does it compile and run? Is anything wrong?

**Code:**

```java
// saved as hello.java
public class hello {
  public static void main(String[] args) { System.out.println("hi"); }
}
```

**Output of running the code:**

```
hi
```

**Student answer:**

> I can rename the file to Greeting.java and keep public class hello.

### 96. S149

**Question (the part the student answers):**

Print all elements row by row, separated by spaces, one row per line; it must work for any 2-D array.

**Code:**

```java
(writing task) void print2DArray(double[][] a)
```

**Output of running the code:**

```
(not run: no runnable code, or it needs input)
```

**Student answer:**

> For a 3 × 3 board I would use a[0].length, but for any 2-D array I need a[i].length.

### 97. S150

**Question (the part the student answers):**

Show three different statements that add 1 to count and store the result in count.

**Code:**

```java
(writing task) int variable count already exists
```

**Output of running the code:**

```
(not run: no runnable code, or it needs input)
```

**Student answer:**

> System.out.println(count + 1) shows one more, but count + 1 on its own line does not change count.

### 98. S156

**Question (the part the student answers):**

Give the exact output. Explain.

**Code:**

```java
for (int i = 1; i < 4; i++) {
  for (int j = 1; j <= i; j++) {
    System.out.printf("%d ", j);
  }
  System.out.println();
}
```

**Output of running the code:**

```
1 
1 2 
1 2 3
```

**Student answer:**

> When i is 3 it prints 1 2 3.

### 99. S164

**Question (the part the student answers):**

Convert the switch into an if-else-if statement.

**Code:**

```java
switch (value) {
case 1: result = 30; break;
case 2:
case 3: result = -10; break;
default: result = 5; break;
}
```

**Output of running the code:**

```
(not run: no runnable code, or it needs input)
```

**Student answer:**

> if (value == 1) result = 30; elif (value == 2 || value == 3) result = -10; else result = 5;

### 100. S169

**Question (the part the student answers):**

Put the lines in order so the program prints 1 + 2 + … + n once. Explain your order.

**Code:**

```java
Lines (shuffled):
A  sum += i;
B  int sum = 0;
C  for (int i = 1; i <= n; i++) {
D  }
E  System.out.println(sum);
```

**Output of running the code:**

```
(not run: no runnable code, or it needs input)
```

**Student answer:**

> B C A D E: sum has to start at 0 before the loop, be added to in every pass, and be printed once after the loop.
