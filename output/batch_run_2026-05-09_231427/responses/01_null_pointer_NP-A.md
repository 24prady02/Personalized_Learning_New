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
- Classifier WM: NP-C (score=0.688133180141449)
- RAG hybrid WM: NP-B  (flipped=True)
- BKT mastery: 0.25 -> 0.23

## LLM response

### Question:
I created a Room object but calling describe() on it crashes with NullPointerException. I declared the field right at the top of the class so it should exist already. What am I missing?

### Response:

#### Surface Observation:
The program crashed with `NullPointerException` when you tried to call the `describe()` method on the `currentRoom` variable.

#### Rule/Concept:
When you declare a reference but don't initialize it with an object, it points to `null`. Calling methods on `null` results in a `NullPointerException`.

#### Example and Explanation:

```java
public class Game {
    Room currentRoom;  // Declaration creates a reference slot holding null

    public void start() {
        System.out.println("Starting the game...");
        currentRoom.describe();  // Dereferences the reference - follows the address to the heap object
    }
}
```

1. **Line 3**: `Room currentRoom;` — This declares a reference named `currentRoom`. The declaration creates a slot in memory for the reference, but it currently holds `null`.
   
2. **Line 6-7**: 
   - `System.out.println("Starting the game...");` — This line executes successfully.
   - `currentRoom.describe();` — Here, Java tries to dereference the `currentRoom` reference. Since it points to `null`, Java cannot follow this address to a valid object and throws a `NullPointerException`.

#### Key Mechanism:
The key mechanism you need to remember is that when you declare a reference but don't initialize it with an object, it starts as `null`. Calling methods on `null` leads to a `NullPointerException`.

#### Check-for-Understanding Question:
Before calling methods on a reference, what should you always check to avoid a `NullPointerException`?

---

### Explanation for Visual Learners:

Imagine you have a box (that's the reference) and inside this box, there might be nothing or something. If it's empty, trying to open it will give you an error because there's no content.

In Java:
- The box is declared (`Room currentRoom;`).
- But initially, it has nothing in it (`null`).
- Trying to open the box (call `currentRoom.describe()`) without anything inside leads to a crash.