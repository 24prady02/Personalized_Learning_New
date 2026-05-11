# 08_assignment_vs_compare_AC-A — assignment_vs_compare (expected AC-A)

## Student message
My if-statement always enters the true branch even when x isn't 5. I wrote if (x = 5) and it seems to just set x to 5 and then the if is always true. Why does Java behave this way?

## Student code
```java
int x = 10;
if (x = 5) {
    System.out.println("x is 5");   // always prints
}
```

## Diagnosis
- LP: L3 -> L4
- Classifier WM: AC-A (score=0.47155532240867615)
- RAG hybrid WM: AC-C  (flipped=True)
- BKT mastery: 0.15 -> 0.22

## LLM response

It seems like you're stuck on why your if-statement is always entering the true branch even when `x` isn't 5. Let me help you understand what's happening with this piece of code:

```java
if (x = 5) {
    // This block will always execute
}
```

The issue here is that you used a single equals sign `=` instead of a double equals sign `==`. In Java, the single equals sign `=` is an assignment operator. It assigns the value on its right to the variable on its left and returns the assigned value.

So when you write `if (x = 5)`, it does the following:
1. Assigns the value `5` to `x`.
2. Returns the value `5`.

Since `5` is a non-zero integer, it's considered "truthy" in Java. Therefore, the condition `(x = 5)` evaluates to `true`, and the code inside the if-statement always executes.

To fix this, you should use the double equals sign `==` for comparison:

```java
if (x == 5) {
    // This block will only execute if x is actually equal to 5
}
```

With this change, your if-statement will correctly check whether `x` is equal to `5`.

Let's go through an example with ASCII diagrams to help visualize the difference:

1. **Assignment (`=`)**:
   ```
   x = 5;
   |       |
   |       v
   x -> 5 (non-zero integer, considered true)
   ```

2. **Comparison (`==`)**:
   ```
   if (x == 5) {
       // This block will only execute if x is actually equal to 5
   }
   |       |
   |       v
   x -> 5  ?
         |
         v
    true (because x is indeed equal to 5)
   ```

Now you know why your if-statement was always entering the true branch. By using `==` instead of `=`, you can correctly compare `x` with `5`.

I hope this explanation helps! If you have any more questions, feel free to ask.

Once you're comfortable with `null_pointer`, we'll come back to `assignment_vs_compare`.