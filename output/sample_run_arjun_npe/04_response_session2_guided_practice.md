# Session 2 — Guided Practice Stage

**Student**: Arjun
**Concept**: `null_pointer` + `object_initialization`
**Stage**: 2 of 4 — GUIDED PRACTICE
**Scaffolding**: 3/5 (reduced from 5)
**Time**: 2026-05-07 10:15:42 (next day — spaced repetition)
**Mastery before this session**: `null_pointer`: 0.46, `object_initialization`: 0.52

---

## Arjun's Response from Session 1

> "I think (d) — a constructor for Game. Because if I put it in start(), I'd have to remember every time. And the field initializer (c) feels weird because what if Room needs arguments later? Constructor seems like the cleanest spot."

---

## Teaching Response

Excellent reasoning, Arjun. You picked (d) for the right reason — you thought about *future flexibility*, not just what makes the error go away. That's the difference between writing code and engineering it.

You're right that all four would technically work. Here's why (d) is what most Java programmers reach for:

| Choice | Works? | Tradeoff |
|---|---|---|
| (a) Inside `start()` | ✓ | Couples object creation to one method — can't reuse |
| (b) Inside `main` | ✓ | Game's *outsider* setting up Game's *internals* — leaks |
| (c) Field initializer | ✓ | Fine for simple cases; can't pass arguments easily |
| (d) Constructor | ✓ | Standard idiom; flexible; future-proof |

### Now you write the fix

I'll give you a starting point. **You** fill in the constructor:

```java
public class Game {
    Room currentRoom;

    public Game() {
        // ← your code here
        // (hint: you need to create a Room AND give it a name)
    }

    public void start() {
        currentRoom.describe();
    }

    public static void main(String[] args) {
        Game g = new Game();
        g.start();
    }
}
```

A few hints, in case you need them:

- The `Room` class has a `name` field but no constructor of its own — that means it gets a *default* constructor that takes no arguments
- After `new Room()`, the Room exists but its `name` is `null` (same problem one level deeper!)
- You'll need two lines inside the `Game` constructor

Try it. Run it. Tell me what happens — even if it works the first time, I want you to **explain why each line is there**.

---

## Predicted next-step gotchas (from KG)

The system anticipates Arjun will hit one of these in his answer:

1. He'll write `currentRoom = new Room();` and forget to set `name` → second NPE on `name` (same concept, deeper recursion of it)
2. He'll write `Room currentRoom = new Room();` shadowing the field with a local
3. He'll get it perfect — in which case Stage 3 starts immediately

If (1) happens, the system already has the follow-up ready: "*Same idea — but where?*" pointing him at line `name` instead of `currentRoom`.

---

## Provenance

- **Scaffolding reduced**: 5 → 3 (he answered correctly with reasoning, so we pull back support)
- **RL agent action**: `socratic_with_partial_template` (Q=5.12, up from 4.83 last session)
- **BKT update from Session 1**: `null_pointer` 0.14 → 0.46 after explained recognition
- **LP advancement**: L1_recognize ✓ → now at L2_apply_with_scaffolding
