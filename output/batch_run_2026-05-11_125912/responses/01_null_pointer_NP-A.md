# 01_null_pointer_NP-A — null_pointer (expected NP-A)

## Student message
I created a Room object but calling describe() on it crashes with NullPointerException. I declared the field right at the top of the class so it should exist already. What am I missing?

## Student code
```java
public class Game {
    Room currentRoom;
    public void start() { currentRoom.describe(); }
}
```

## Diagnosis
- LP: L1 -> L2
- Classifier WM: NP-B (score=0.6783530712127686)
- RAG hybrid WM: NP-B  (flipped=False)
- BKT mastery: 0.25 -> 0.23

## LLM response

### Tutoring Conversation #1: Moving from L1 to L2 on null_pointer

**Student:** I created a Room object but calling `describe()` on it crashes with `NullPointerException`. I declared the field right at the top of the class so it should exist already. What am I missing?

---

**[LP-3 Mastery Surface]**  
Let's start by looking at what you've done correctly in your code:

1. **Declaration:** You correctly declared a `Room` object called `currentRoom`.
   ```java
   Room currentRoom;
   ```
2. **Method Call:** You attempted to call the `describe()` method on this object.
   ```java
   public void start() { currentRoom.describe(); }
   ```

**[LP-2 Wrong Mental Model Correction]**  
The issue here is related to your mental model of what `null` means. According to the rule, `null` does not mean "no value" or "empty". Instead, it means that there is no object assigned to the reference.

Let's break down the problem using a visual metaphor:
Imagine you have a box labeled `currentRoom`. Initially, this box is empty (i.e., it contains `null`). When you try to open and read from this box (`describe()`), nothing happens because the box has nothing inside it. This results in a crash.

**[LP-3 Six-Step Instruction]**  
1. **Observation:** Your code declares a reference but does not initialize it with an actual object.
   ```java
   Room currentRoom;
   ```
2. **Rule:** A `null` reference means there is no object to call methods on.
   - The declaration creates a reference slot that holds `null`.
3. **Example:**
   ```java
   public class Game {
       Room currentRoom;

       // Method to start the game
       public void start() { 
           currentRoom.describe();  // This will throw NullPointerException
       }
   }
   ```
4. **Step-by-Step Explanation:**  
   - Line 1: `Room currentRoom;` — A reference named `currentRoom` is declared but not initialized.
   - Line 2-4: Inside the `start()` method, you call `describe()` on `currentRoom`.
   - Step-by-step: 
     a. The JVM tries to dereference `currentRoom` (go inside the box).
     b. It finds that the box (`currentRoom`) is empty (contains `null`).
     c. Since there's no object inside, calling `describe()` results in a `NullPointerException`.
5. **Key Mechanism:**  
   - A `null` reference leads to a `NullPointerException` when trying to call methods on it.
6. **Check-for-Understanding Question:**  
   - If I set `currentRoom = new Room();` inside the `start()` method, will it fix the issue? Why or why not?

**[Final Check]**  
Once you understand that a `null` reference leads to a `NullPointerException`, you can move on to initializing your object properly. This involves creating a new `Room` object and assigning it to the `currentRoom` reference.

### Suggested Code:
```java
public class Game {
    Room currentRoom;

    public void start() { 
        currentRoom = new Room();  // Initialize the object
        currentRoom.describe();       // Now this should work
    }
}
```

By initializing your `Room` object, you ensure that `currentRoom` is not `null`, and calling methods on it will no longer cause a crash.