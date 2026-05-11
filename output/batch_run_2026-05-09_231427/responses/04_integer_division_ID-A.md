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
- Classifier WM: ID-A (score=0.7906045317649841)
- RAG hybrid WM: ID-A  (flipped=False)
- BKT mastery: 0.20 -> 0.23

## LLM response

I understand you're frustrated, and I can see why you might feel stuck. But let's take a step back for a moment.

### Current Mastery: 55% / Required: 75%
The concept of 'null_pointer' is still on the path to understanding 'integer_division'. The next prerequisite to master is 'type_mismatch'.

**Why this was selected**: Your current mastery level on 'null_pointer' is at 55%, which is below the required threshold of 75%. The full progression is as follows:

1. **null_pointer** (diff=2, mastery=0.55/0.75 [NOT ready])
2. **string_equality** (diff=2, mastery=0.00/0.80 [NOT ready])
3. **variable_scope** (diff=2, mastery=0.00/0.70 [NOT ready])

### Mastering 'null_pointer'

When you declare a reference in Java, it doesn't automatically allocate memory for the object it's meant to point to. Instead, it is initialized to `null`, which means it currently doesn't point to any valid object.

#### Example Code:
```java
public class NullPointerExample {
    public static void main(String[] args) {
        String myString; // This is a reference variable.
        
        System.out.println(myString); // This will print 'null' because no memory was allocated yet.
        
        myString = new String("Hello"); // Now, memory is allocated for the string "Hello".
        System.out.println(myString); // This will print 'Hello'.
    }
}
```

### Key Points:
1. **Declaration vs. Initialization**: A reference variable is declared but not initialized (i.e., it's set to `null`).
2. **Memory Allocation**: Memory allocation happens when you use the `new` keyword to create an object.
3. **Avoiding RunTimeError**: Always initialize your references before using them.

### Steps for Improvement:
1. **Break Down the Problem**: Take a short break and try solving simpler versions of the problem.
2. **Explain Out Loud**: Explain the issue out loud or to someone (even yourself).
3. **Take Notes**: Write down any insights you have as you debug your code.

Once you feel more confident with 'null_pointer', we'll return to 'integer_division'. If you need help with that, I'm here to support you!