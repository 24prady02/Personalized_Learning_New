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
- Classifier WM: TM-A (score=0.75)
- RAG hybrid WM: TM-B  (flipped=True)
- BKT mastery: 0.20 -> 0.23

## LLM response

**Qwen:**

Hi there! I see you've been working on some code involving integers and strings, and you noticed something different from what you're used to in languages like Python. Let's talk about this a bit.

You know that when you add an `int` and a `String`, Java doesn't just combine them into one string. Instead, it gives you an error. Can you tell me why?

---

### Introducing the Mechanism

The reason behind this is that in Java, types are very important. When you declare a variable, you're telling the compiler exactly what kind of data it will hold. An `int` holds numbers, and a `String` holds text.

Java doesn't automatically change one type to fit another because it can lead to bugs if not done carefully. For example, imagine if Java could just turn an integer into a string without you knowing. What if someone used that code and didn't realize they were mixing types?

Instead, Java requires you to be explicit about how you want to combine these different types.

### Example Walkthrough

Let's look at your Python code and then we'll translate it to Java:

**Python Code:**
```python
int score = 100;
String msg = "Score: " + score + 5;
// expected "Score: 105" but got "Score: 1005"
```

In this Python code, the `+` operator is used to concatenate strings. It's smart enough to convert an integer (like `score`) to a string before combining them.

Now, let's see how Java handles it:

```java
int score = 100;
String msg = "Score: " + score + 5;
```

**What Java Does Line by Line:**

1. **Line 1:** You declare an `int` variable named `score` and initialize it with the value `100`.
   ```java
   int score = 100; // This is a compile-time operation. The compiler knows exactly what type 'score' is.
   ```

2. **Line 2:** You're trying to create a new `String`. But there's a problem!
   ```java
   String msg = "Score: " + score + 5;
   ```
   At compile time, Java sees that the `+` operator is being used with both a `String` and an `int`. It doesn't know if you want to concatenate or do some arithmetic.

   This is where the type mismatch happens. The compiler can't decide how to combine these two types because they're not compatible.

### Predicting Behavior

Now, let's imagine we change just one line of this code:

```java
int score = 100;
String msg = "Score: " + (score + 5);
```

What do you think will happen? What should the output be?

---

**Qwen:** 

Try explaining why `msg` would be different in this case. Think about what Java does at compile time when it encounters the parentheses.

Once you're ready, let's go over your explanation!