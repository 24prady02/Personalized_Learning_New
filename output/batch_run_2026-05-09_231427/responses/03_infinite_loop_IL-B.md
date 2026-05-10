# 03_infinite_loop_IL-B — infinite_loop (expected IL-B)

## Student message
My while loop keeps running forever. I use i in the condition so I thought i would automatically increase each iteration. Doesn't i update on its own when it's used in the loop?

## Student code
```java
int i = 0;
while (i < 10) {
    System.out.println(i);
    // I thought i would increase here automatically
}
```

## Diagnosis
- LP: L3 -> L4
- Classifier WM: IL-B (score=0.8760698437690735)
- RAG hybrid WM: IL-B  (flipped=False)
- BKT mastery: 0.15 -> 0.22
- DINA mastery: 0.17 -> 0.00

## LLM response

It looks like your while loop might be running forever because you're using `i` in the condition without updating it. Let's take a step back and talk about something simpler first.

When you declare a variable in Java, you need to make sure it has a proper value. This is called initialization. If you don't initialize a variable before you use it, it might end up with an unexpected value. For example:

```java
int i; // Declare a variable but don't give it a value yet

if (i == 5) { // Trying to use the uninitialized 'i' here could cause problems
    System.out.println("This will never be printed");
}
```

In this case, `i` has an "unknown" value because it wasn't initialized. This is why we always want to initialize our variables when we declare them.

So, let's practice initializing variables:

1. Declare a variable.
2. Give it a proper initial value.
3. Use it safely in your code.

Here’s an example that should work correctly:

```java
int i = 0; // Initialize 'i' with a value of 0

while (i < 5) { // The condition checks if 'i' is less than 5
    System.out.println("Current value of i: " + i);
    i++; // Increment 'i' by 1 each time the loop runs
}
```

In this example, `i` starts at 0 and increases by 1 in each iteration. The loop will stop when `i` reaches 5.

Now, if you ever find yourself stuck with a similar issue, take a break and try to understand what you've initialized and how it's being used. Remember, initialization is key!

Once you feel more comfortable with initializing variables, we can come back and tackle those tricky infinite loops. Does that sound good?