# Session 3 — Independent Practice (Transfer Problem)

**Student**: Arjun
**Concept**: `null_pointer` + `object_initialization`
**Stage**: 3 of 4 — INDEPENDENT PRACTICE
**Scaffolding**: 1/5 (minimal — just framing)
**Time**: 2026-05-09 16:42:08 (3 days later — spaced)
**Mastery before this session**: `null_pointer`: 0.74, `object_initialization`: 0.81

---

## Why a transfer problem?

Sessions 1 and 2 used Arjun's *original* code (Game/Room). If we re-test on the same code, we measure memorization, not understanding. The system retrieves a *novel but isomorphic* problem from the KG so we can see whether the concept actually transferred.

**Selected problem** (from `data/codenet/java/buggy/`, lightly adapted):

```
KG retrieval query: same_concept_different_surface(null_pointer, difficulty=L3)
Match: BankAccount/Transaction problem (same shape: outer class holds ref to inner, ref never initialized)
```

---

## Teaching Response

Arjun — different problem, same family. No hints from me this time. Just the problem.

```java
public class Bank {
    Account customerAccount;
    String bankName = "First National";

    public void processDeposit(double amount) {
        customerAccount.deposit(amount);
        System.out.println("Deposited at " + bankName);
    }

    public static void main(String[] args) {
        Bank b = new Bank();
        b.processDeposit(100.0);
    }
}

class Account {
    double balance;
    String owner;

    public void deposit(double amount) {
        balance += amount;
        System.out.println(owner + " new balance: " + balance);
    }
}
```

**Three things to do**:

1. Predict the output — *before* you run it. Will it crash? If yes, where and why?
2. Fix it. Make it print a sensible deposit confirmation.
3. After your fix runs, look at the output. Is anything still wrong or weird? If so, what would you fix next?

Send me your prediction first, *then* your fix. I want to see whether you can spot it without running it — that's the real skill.

---

## What the system is measuring

| Sub-skill | How it's tested here |
|---|---|
| Recognize null reference pattern | Does Arjun spot it without running? |
| Apply two-step rule | Does his fix initialize `customerAccount`? |
| Recursive application | Does he also notice `owner` would be null? |
| Self-correction | Does step 3 catch the secondary issue? |

Hitting all four → mastery. Missing the recursive case (`owner`) → re-loop on Session 3 with a hint, not advance to Session 4.

---

## Predicted Arjun response (from RNN/HVSAE forecast)

The behavioral RNN, given Arjun's trajectory, predicts:

- **P(spots NPE without running)** = 0.78
- **P(initializes `customerAccount`)** = 0.91
- **P(also notices `owner` issue in step 3)** = 0.43 ← this is the discriminator

If he gets the third one, he's at mastery. If not, the system will route him into a targeted micro-lesson on "*where else could this same bug live in your code?*"

---

## Provenance

- **Scaffolding**: 1/5 — only problem framing, no hints
- **Transfer test**: KG-retrieved isomorphic problem, not original Game/Room
- **RL agent action**: `transfer_test_with_self_evaluation` (Q=5.41)
- **BKT predicted update on success**: `null_pointer` 0.74 → ~0.92
- **LP advancement on success**: L2_apply_with_scaffolding ✓ → L3_apply_independent
