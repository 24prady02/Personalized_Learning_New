# 09_scanner_buffer_SB-A — scanner_buffer (expected SB-A)

## Student message
I called nextLine() right after nextInt() and now my string is empty. The Scanner is skipping my input completely. Each method should read its own line of input, right?

## Student code
```java
Scanner sc = new Scanner(System.in);
int age = sc.nextInt();
String name = sc.nextLine();    // always empty
System.out.println("Hello " + name);
```

## Diagnosis
- LP: L3 -> L4
- Classifier WM: SB-A (score=0.4625551998615265)
- RAG hybrid WM: SB-A  (flipped=False)
- BKT mastery: 0.20 -> 0.23

## LLM response

I see why you're stuck, but there's one more concept you need to master before we can move on to 'scanner_buffer'. The 'null_pointer' error is a prerequisite that will help us understand how memory and references work in Java. It’s like trying to build a tower with blocks when some of the blocks are missing!

Let me explain what a 'null_pointer' is:

In Java, when you try to use an object reference that hasn’t been properly initialized, it can point to `null`. This is similar to having a pointer in C++ that points to nothing. When you try to do something with a null reference, like calling a method on it or accessing its fields, Java throws a `NullPointerException`.

Here’s a simple example:

```java
String text = null;
System.out.println(text.length());  // This will throw a NullPointerException
```

In this example, `text` is initially set to `null`. When we try to call `length()` on it, Java gets confused because it doesn’t know what the length of nothing is. That’s why it throws an error.

Now, let's work through some exercises to practice identifying and handling `NullPointerExceptions`. Once you’re comfortable with that, we can come back to 'scanner_buffer' and see how these principles apply there.

Here’s a challenge for you:

1. Create a method that takes a string as input.
2. Inside the method, try to print the length of the string.
3. What should you do if the string is `null`?

Think about what might go wrong and how to handle it gracefully. Write some code and see what happens when you pass `null` to your method.

Once you’re ready, come back and let me know what you’ve done!