# 04_integer_division_ID-A — integer_division (expected ID-A)

## Student message
I divided 5 by 2 in Java and got 2, not 2.5. That's not the right answer mathematically. Java rounded it down for no reason — five divided by two is two and a half!

## Student code
```java
double half = 5 / 2;
System.out.println(half);   // expected 2.5, got 2.0
```

## Diagnosis
- LP: L1 -> L2
- Classifier WM: ID-B (score=0.5396076440811157)
- RAG hybrid WM: ID-A  (flipped=True)
- BKT mastery: 0.20 -> 0.23

## LLM response

I see why you're stuck, and that's okay! It happens to almost everyone when they start learning programming. Let's talk about `null_pointer` first, as that's a prerequisite for understanding `integer_division`.

### What is `null_pointer`?

In Java, `null` means "no value" or "nothing." When you try to use an object reference but haven't initialized it yet, you get a `NullPointerException`. It’s like trying to touch air — nothing happens!

Here's an example:

```java
String name = null;
System.out.println(name.length());  // This will throw NullPointerException
```

### Why is `null_pointer` important?

When you learn about objects and references in Java, understanding what `null` means helps you avoid runtime errors. It’s like having a safety net to prevent your program from crashing when you try to do something with an object that doesn’t exist.

### How to fix it?

To use an object safely, always make sure it's not `null` before you use it. You can add checks:

```java
String name = null;
if (name != null) {
    System.out.println(name.length());
} else {
    System.out.println("Name is null!");
}
```

### Summary

- `null` means "no value" or "nothing."
- When you try to use a `null` reference, Java throws a `NullPointerException`.
- Always check if an object is not `null` before using it.

Now that you understand `null_pointer`, we’ll be ready to move on to `integer_division`. I'm excited to help you see how types work in Java!