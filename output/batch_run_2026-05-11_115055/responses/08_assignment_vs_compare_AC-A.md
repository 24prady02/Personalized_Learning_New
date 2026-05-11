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
- Classifier WM: AC-C (score=0.75)
- RAG hybrid WM: AC-C  (flipped=False)
- BKT mastery: 0.15 -> 0.22

## LLM response

I can see why you're stuck, but let me explain something important first before we go any further.

When you write `if (x = 5)`, you might think that it’s checking if `x` is equal to 5. However, what actually happens is that `=` is an assignment operator, not a comparison operator. This means that Java will try to assign the value `5` to `x`. If this succeeds, the entire expression `x = 5` evaluates to `5`, which is considered truthy in Java because it's non-zero.

That’s why your if-statement always seems to enter the true branch even when `x` isn’t 5. You’re basically saying "If I assign the value 5 to x, then this condition is true."

This confuses nearly everyone at first, but that’s okay! The fact that you spotted it means you are making progress.

To help illustrate this, let's look at a simple example:

```java
int x = 3;
if (x = 5) {
    System.out.println("This will print because the condition is true");
} else {
    System.out.println("This won't print");
}
```

In this code:
- `x` is initially assigned the value `3`.
- The condition `(x = 5)` assigns `5` to `x`, and since assignment returns the assigned value, it evaluates to `5`.
- Because `5` is truthy, the if-statement executes the true branch, printing "This will print because the condition is true".

Now, let's move on to a different topic. I need you to understand something called 'null_pointer' before we can go back to `assignment_vs_compare`.

The `null_pointer` error happens when you try to use an object reference that hasn’t been initialized. This is a common mistake for beginners like yourself.

Here’s a simple example:

```java
String myString = null;
System.out.println(myString.length());  // This will throw a NullPointerException
```

In this code:
- `myString` is declared but not assigned any value, so it remains `null`.
- When you try to call `length()` on `myString`, Java throws a `NullPointerException` because you can't perform operations on `null`.

To avoid this error, always make sure your object references are properly initialized before you use them.

I’ll explain more about `null_pointer` later, but for now, focus on understanding why it’s important to initialize variables correctly. Once you get comfortable with that, we can come back and tackle `assignment_vs_compare` again.

Do you have any questions about `null_pointer`?