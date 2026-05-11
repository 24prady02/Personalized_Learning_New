# 02_type_mismatch_TM-B — type_mismatch (expected TM-B)

## Student message
I thought + would just combine an int and a string into one string the way Python does. Why won't Java do this automatically? It worked fine when I tested it in Python.

## Student code
```java
int score = 100;
String msg = "Score: " + score + 5;
// expected "Score: 105" but got "Score: 1005"
```

## Diagnosis
- LP: L2 -> L3
- Classifier WM: TM-B (score=0.5152639746665955)
- RAG hybrid WM: TM-B  (flipped=False)
- BKT mastery: 0.20 -> 0.23

## LLM response

### Student's Code Analysis

You've correctly identified that `int + String` results in an error because Java does not automatically convert types. This shows you have a good grasp of the rule, which is great! Let's dive deeper into why this happens and how to handle it.

### The Rule Underneath

Java treats type differences very seriously. It checks operand types at compile time, ensuring that operations are valid for their types. When you try to add an `int` and a `String`, Java sees two incompatible types, which leads to a type mismatch error.

### Example Walkthrough

Let's look at your code in detail:

```java
int score = 100;
String msg = "Score: " + score + 5;
// expected "Score: 105" but got "Score: 1005"
```

Here’s what happens during compilation:

1. **Compile-time Type Checking**:
   - Java compiles the code line by line, checking each expression.
   - The expression `score + 5` is valid because both operands are integers (compile time).
   - When it encounters `"Score: " + score`, it tries to concatenate a `String` and an `int`.

2. **Type Mismatch**:
   - Java does not implicitly convert the integer `score` to a string.
   - It expects the expression to be a valid concatenation of strings.

### Visual Representation

Here’s a simple visual representation of the problem:

```
// Before Compilation
String msg = "Score: " + score + 5;

// During Compilation (Error)
// Java sees: String + int + int
// Error: Cannot concatenate int with String directly
```

### Predicting the Outcome

Now, let's predict what would happen if we change one line of code:

```java
int score = 100;
String msg = "Score: " + (score + 5);
// expected "Score: 105"
```

What do you think will happen this time?

### Encouragement and Next Steps

Good job understanding the basic rule! The key takeaway is that Java enforces type safety at compile time. When faced with an operation involving different types, you need to explicitly convert them if necessary.

Next time, try explaining in your own words why Java doesn't automatically convert types. This will help solidify your understanding and move towards L3 proficiency.