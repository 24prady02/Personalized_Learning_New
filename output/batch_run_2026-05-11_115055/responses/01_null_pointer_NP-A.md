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
- Classifier WM: NP-B (score=0.7267476320266724)
- RAG hybrid WM: NP-B  (flipped=False)
- BKT mastery: 0.25 -> 0.23

## LLM response

**[ASCII Diagram]**

```plaintext
|---[Room Object]--------------------------------|
|  - describe() Method                           |
|                                                |
|---[Game Class]----------------------------------|
|  - currentRoom: Room                          | <--- null (no object)
|                                                |
|---[start() Method]------------------------------|
|  - currentRoom.describe();                      |
```

**Observation:** You're calling `describe()` on a field named `currentRoom` in your `Game` class, but it crashes with a `NullPointerException`. 

**Rule:** In Java, when you declare a reference variable like `currentRoom`, it initially holds the value `null`. Calling a method on `null` causes a `NullPointerException`.

**Example Code:**

```java
public class Game {
    Room currentRoom;

    public void start() { 
        // Step 1: currentRoom is declared but not initialized
        System.out.println("Starting game...");
        
        // Step 2: Trying to call describe() on null
        currentRoom.describe(); 
    }

    public static void main(String[] args) {
        Game game = new Game();
        game.start();
    }
}
```

**Explanation:**

1. **Step 1:** When you declare `Room currentRoom;`, it creates a reference to a Room object, but that reference is initially `null`.
2. **Step 2:** In the `start()` method, when you call `currentRoom.describe();`, Java tries to follow the reference to the actual Room object on the heap.
3. **Step 3:** Since `currentRoom` is `null`, there's no valid memory address to follow, so it throws a `NullPointerException`.

**Key Mechanism:** You must initialize `currentRoom` with an actual `Room` object before calling any methods on it.

**Check for Understanding:**
Can you explain why the code crashes and what needs to be fixed?