# Session 4 — Mastery Check & Final Learning Level

**Student**: Arjun
**Concept**: `null_pointer` + `object_initialization`
**Stage**: 4 of 4 — MASTERY CHECK
**Scaffolding**: 0/5 (none)
**Time**: 2026-05-13 09:08:31 (1 week after first session)
**Mastery before**: `null_pointer`: 0.91, `object_initialization`: 0.94

---

## What happened in Sessions 1–3 (recap)

| Session | Stage | Days from start | Mastery (null_pointer) | Outcome |
|---|---|---|---|---|
| 1 | Introduction | Day 0 | 0.14 → 0.46 | Recognized the concept; chose constructor for the right reason |
| 2 | Guided Practice | Day 1 | 0.46 → 0.74 | Wrote the fix; explained each line; caught the "name field also null" gotcha unprompted |
| 3 | Independent Practice (transfer) | Day 3 | 0.74 → 0.91 | Spotted NPE in BankAccount problem without running; got `owner` issue on step 3 |

---

## Mastery Check Problem

```java
// Class hierarchy with multiple uninitialized references.
// Find every place this code can throw NullPointerException
// and rewrite it correctly.

public class Library {
    Catalog catalog;
    Librarian onDuty;

    public void openForDay() {
        catalog.refreshIndex();
        onDuty.greet();
    }
}

class Catalog {
    Book[] books;
    public void refreshIndex() {
        for (Book b : books) b.touch();
    }
}

class Book {
    String title;
    public void touch() { System.out.println("touched: " + title); }
}

class Librarian {
    String name;
    public void greet() { System.out.println("Hi, I'm " + name); }
}
```

Arjun was given **15 minutes**, **no hints**, and asked to:
1. List every potential NPE
2. Rewrite the code correctly
3. Explain his strategy in 2–3 sentences

---

## Arjun's Submission (verbatim)

> "There are **four** places this can throw NPE:
> 1. `catalog` is never initialized → `openForDay` crashes line 1
> 2. `onDuty` is never initialized → would crash line 2 if we got past line 1
> 3. Inside Catalog, `books` is never initialized → enhanced-for-loop crashes
> 4. Even after `books = new Book[3]`, the *array slots* are all null by default → `b.touch()` crashes
>
> The fix is to give every class a constructor that initializes its own references. Library shouldn't be responsible for initializing Catalog's books — that's encapsulation. So Catalog's constructor creates and fills its own array, Library's constructor creates Catalog and Librarian.
>
> ```java
> public class Library {
>     Catalog catalog;
>     Librarian onDuty;
>     public Library() {
>         catalog = new Catalog();
>         onDuty = new Librarian();
>     }
>     // ... openForDay unchanged
> }
>
> class Catalog {
>     Book[] books;
>     public Catalog() {
>         books = new Book[]{ new Book("Dune"), new Book("1984") };
>     }
>     // ...
> }
>
> class Book {
>     String title;
>     public Book(String title) { this.title = title; }
>     // ...
> }
>
> class Librarian {
>     String name;
>     public Librarian() { this.name = "Sam"; }
>     // ...
> }
> ```
>
> **Strategy**: each class fixes its own internal nulls. The compiler error always tells you the *what*; what it can't tell you is *whose responsibility* the fix is."

---

## System Evaluation

| Criterion | Result |
|---|---|
| Identified all 4 NPE sites | ✓ |
| Code compiles and runs | ✓ |
| Used constructor pattern (not field initializers or method-local) | ✓ |
| Encapsulation reasoning ("Library shouldn't initialize Catalog's books") | ✓ — *unprompted, beyond rubric* |
| Recognized array-of-references vs array-itself distinction | ✓ — this was the deepest test |
| Explained strategy generally, not just this problem | ✓ |

**Verdict**: **MASTERED** ✓

---

## Final Learning Level Snapshot

Stored to `data/student_states.json` under `arjun`:

```json
{
  "student_id": "arjun",
  "last_updated": "2026-05-13T09:23:54.118402",
  "cognitive_graph": {
    "concept_nodes": {
      "null_pointer": {
        "mastery": 0.97,
        "encoding": "deep",
        "dual_coding": "verbal_and_visual",
        "elaboration": true,
        "transfer_demonstrated": true,
        "encoding_history": [
          {"timestamp": "2026-05-06T14:30:14", "encoding": "surface", "mastery": 0.14},
          {"timestamp": "2026-05-06T14:42:08", "encoding": "partial", "mastery": 0.46},
          {"timestamp": "2026-05-07T10:31:55", "encoding": "partial", "mastery": 0.74},
          {"timestamp": "2026-05-09T16:58:22", "encoding": "deep",    "mastery": 0.91},
          {"timestamp": "2026-05-13T09:23:54", "encoding": "deep",    "mastery": 0.97}
        ]
      },
      "object_initialization": {
        "mastery": 0.96,
        "encoding": "deep",
        "dual_coding": "verbal_and_visual",
        "elaboration": true
      },
      "constructors": {
        "mastery": 0.84,
        "encoding": "deep",
        "elaboration": true,
        "note": "Strengthened indirectly through this journey"
      },
      "encapsulation": {
        "mastery": 0.61,
        "encoding": "partial",
        "note": "Emerged as Arjun's own insight in mastery check; flagged as next teaching target"
      },
      "array_of_references": {
        "mastery": 0.72,
        "encoding": "partial",
        "note": "New concept introduced in mastery check; needs reinforcement"
      }
    }
  },
  "lp_index": {
    "OOP_References_Track": "L4_explain_and_transfer (mastered)"
  },
  "rl_signal": {
    "session_count": 4,
    "successful_strategies": [
      "introduce_with_visual_analogy",
      "socratic_with_partial_template",
      "transfer_test_with_self_evaluation"
    ],
    "reward_total": 18.4,
    "reward_breakdown": {
      "learning_gain": 12.1,
      "engagement": 4.8,
      "transfer_bonus": 1.5
    }
  },
  "next_recommended_concepts": [
    "encapsulation",
    "array_of_references",
    "polymorphism_basics"
  ]
}
```

---

## Mastery Progression Chart

```
null_pointer mastery over 4 sessions:

1.0 ┤                                    ╭───── ✓ MASTERED
0.9 ┤                              ╭─────╯ 0.97
0.8 ┤                              │  0.91
0.7 ┤                       ╭──────╯
0.6 ┤                       │  0.74
0.5 ┤                ╭──────╯
0.4 ┤                │  0.46
0.3 ┤                │
0.2 ┤  ●─────────────╯
0.1 ┤  0.14
0.0 ┴────┬────────┬─────────┬──────────┬────
       Day 0    Day 1     Day 3      Day 7
       S1: Intro  S2: Guided  S3: Transfer  S4: Mastery
```

---

## What the system learned from this student (RL feedback loop)

The `rl_teaching_agent.pt` weights are updated based on the reward signal:

- Sequence `[visual_analogy → socratic_template → transfer → mastery_check]` produced reward **+18.4** for student profile `(high_conscientiousness, active_visual_learner, moderate_neuroticism)`
- This reinforces the policy for the *next* student matching that profile cluster
- Per the README's claim of "69% better over 100 students", this is exactly the mechanism — accumulated rewards across diverse profiles update the DQN's value estimates

---

*This is what one full successful learning journey looks like through the system, end to end.*
