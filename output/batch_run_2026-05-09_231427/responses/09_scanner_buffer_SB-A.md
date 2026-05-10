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
- Classifier WM: SB-B (score=0.6486724019050598)
- RAG hybrid WM: SB-A  (flipped=True)
- BKT mastery: 0.20 -> 0.23
- DINA mastery: 0.15 -> 0.00

## LLM response

It looks like you're stuck on why your string input is being skipped after using `nextInt()` in Java. This issue is quite common for beginners, but don't worry—many other learners have run into it too! Let's focus on understanding what happens when you use different methods with the `Scanner` class.

### Understanding the Scanner Buffer

When you read an integer using `nextInt()`, it reads digits up to but not including the newline character. This means that if you immediately call `nextLine()` after `nextInt()`, the leftover newline character is still in the buffer. As a result, `nextLine()` reads this empty line instead of waiting for new input.

Here’s an example to illustrate:

```java
Scanner scanner = new Scanner(System.in);
System.out.println("Enter an integer:");
int number = scanner.nextInt();
scanner.nextLine(); // This consumes the leftover newline character
System.out.println("Enter a string:");
String text = scanner.nextLine();
System.out.println("You entered: " + number + ", " + text);
```

In this code, after `nextInt()`, there's a newline character left in the buffer. When you call `nextLine()` immediately afterward, it reads this newline and moves on to the next line of input.

### Fixing the Issue

To fix this, you need an extra `nextLine()` call right after `nextInt()` to consume the leftover newline:

```java
Scanner scanner = new Scanner(System.in);
System.out.println("Enter an integer:");
int number = scanner.nextInt();
scanner.nextLine(); // Consumes the leftover newline character
System.out.println("Enter a string:");
String text = scanner.nextLine();
System.out.println("You entered: " + number + ", " + text);
```

Now, `nextLine()` will wait for new input as expected.

### Visual Explanation

Imagine the buffer as a stream of water. When you use `nextInt()`, it reads up to the last digit and stops before hitting the newline character (which is like a drop in the stream). This leaves a small puddle of newline at the end. 

If you call `nextLine()` right away, it's like trying to drink from that puddle instead of waiting for new water to come down the stream. To fix this, you need to make sure all the leftover water (newline characters) is consumed before calling `nextLine()` again.

### Connecting the Concepts

Do you see how the mechanism where `nextInt()` leaves a newline in the buffer and `nextLine()` reads it next time works? It's like leaving a little bit of coffee on your spoon after pouring, and then expecting to eat directly from it. You need to clean up (in this case, use an extra `nextLine()`) before you can use it again.

### Transfer Challenge

Now, try to apply what you learned in a new scenario:

1. Write a program that reads two strings: one after an integer.
2. Use the `Scanner` class to handle user input.
3. Make sure both strings are correctly read without skipping any.

This should help solidify your understanding of how the scanner buffer works and why you need the extra `nextLine()` call. Keep practicing, and soon you’ll be reading user inputs like a pro!