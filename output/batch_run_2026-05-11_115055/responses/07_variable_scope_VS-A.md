# 07_variable_scope_VS-A — variable_scope (expected VS-A)

## Student message
I declared total inside the if block but now I can't use it outside. The compiler says "cannot find symbol". The braces are just for organisation, right? I already declared the variable, why does Java forget it?

## Student code
```java
if (x > 0) {
    int total = x * 2;
}
System.out.println(total);  // compile error
```

## Diagnosis
- LP: L2 -> L3
- Classifier WM: VS-A (score=1.0)
- RAG hybrid WM: VS-A  (flipped=False)
- BKT mastery: 0.20 -> 0.23

## LLM response

### Acknowledging and Reframing

Hello! It sounds like you're frustrated, but don't worry. This is totally normal for beginners! When you declare a variable inside an `if` block, it might seem like it exists throughout the method. But that's not quite right.

### Moving Beyond Braces

Imagine Java as a neat filing system. If you put a file (variable) in one drawer (`if` block), you can only access it if you know exactly which drawer to look in. Once you leave that drawer, you have to go back to the main folder (method) to find your file again.

### Why This Happens

When Java sees your `if` block, it's like opening a new folder. Inside this folder, any variables you declare are only accessible within that folder. Once you close the folder with the closing brace (`}`), all the variables inside go away until you reopen the same folder.

### Let’s See an Example

```java
public class ScopeExample {
    public static void main(String[] args) {
        int number = 10;

        if (number > 5) {
            int total = 20; // This is like opening a new drawer
        }

        System.out.println(total); // This will give an error because 'total' is outside its folder
    }
}
```

### Visualizing the Process

Imagine you have a big box (`main` method). Inside this box, there's another smaller box (`if` block) where you keep some special toys (variables). If you want to play with those toys, you need to open the smaller box first. Once you're done playing, close it again and go back to your main toybox.

### Predicting Behavior

Let’s change one small thing: remove the `int total` inside the `if` block and instead declare it outside.

```java
public class ScopeExample {
    public static void main(String[] args) {
        int number = 10;
        int total; // Declare here, but don't initialize yet

        if (number > 5) {
            total = 20; // Initialize inside the block
        }

        System.out.println(total); // This should work now!
    }
}
```

### Reflecting on Learning

Good job noticing why it didn’t work before! Now, try to explain the mechanism in your own words. What do you think happens when we declare `total` outside the `if` block? Why does this fix the error?

Feel free to take a break if you need it, and come back with fresh eyes once you're ready!