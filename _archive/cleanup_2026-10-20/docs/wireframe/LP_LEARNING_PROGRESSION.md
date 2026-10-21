# CPAL Wireframe — the full process (Learning Progression workflow)

_Scope: every step the wireframe (`cpal_wireframe.html`,
`tutor.cpaltutor.com/wireframe`) runs for each student message, on Hello World /
program structure (§1.1). The Learning Progression (LP) is the backbone the
whole process hangs off._

## The process in one line

> A student answers → the system reads **how deeply they understand** (LP) →
> tracks **mastery** → catches any **misconception** → places it all on the
> **knowledge graph** → chooses one **teaching action** → writes the **tutor
> reply** — and every step is explained.

The two views show two halves of this: the **Student** tab is just the
conversation; the **Teacher** tab is the live analysis, where all panels
recompute **simultaneously** on each message.

---

## Step 0 — The student answers (the input)

The student reads `HelloWorld.java` and types a response (a prediction, an
explanation, a trace, etc.). That single message is the input to everything
below. Each message is also an **assessment item** of a certain type
(syntax-identification → predict-output → explanation → trace-table →
debugging), which is what the level can climb through.

## Step 1 — Diagnose the LP level (panel ①)

The answer is placed on the five-level SOLO-for-code scale:

| Level | Name | Meaning | Hello World example |
|---|---|---|---|
| **L0** | Prestructural (floor) | no usable understanding | "I'm not sure what this does." |
| **L1** | Unistructural (symptom) | names one surface aspect | "It prints 'Hello, World'." |
| **L2** | Rule | states a correct rule | "javac compiles, then java runs — two steps." |
| **L3** | Mechanism | explains *why* | "javac makes bytecode; the JVM finds main and runs it." |
| **L4** | Transfer | applies it to new cases | "Rename the class → compile error; bad main signature → run-time error." |

**Mastery is stored as a probability distribution over L0–L4**, not one hard
level. A single **reported level** is derived only by a documented rule:

- report **Lk** when its mass > **0.55** and adjacent mass < **0.30**;
- otherwise report **"between Lk – Lk+1"** (the student is straddling).

## Step 2 — Track mastery over time (panel ②)

The per-turn distribution feeds a running **mastery estimate** for the concept
across the whole conversation (knowledge tracing), shown as a single trend %.
This is what tells the teacher whether mastery is *developing* or *strong* — and
a repeated later error can point back to an earlier prerequisite gap.

## Step 3 — Catch the misconception (panel ③)

The answer's reasoning pattern is matched against a misconception catalogue.
Each entry is **multi-keyed**: the concept(s) it belongs to, the LP level(s) it
shows at, the response pattern that gives it away, the **diagnostic trace step**
that exposes it, and the **remediation** resource. For Hello World the key one
is **PS-A — "compile and run are one step."** It is shown **matched**, then
**cleared** once the student reaches the mechanism.

## Step 4 — Place it on the knowledge graph (panel ④)

Everything couples onto one typed graph. `program_structure (§1.1)` is the
**root of the Chapter-1 prerequisite DAG**; around it attach typed nodes
(LPLevel, Misconception, AssessmentItem, Resource, Evidence) via typed edges
(`prerequisiteOf`, `alignedToLPLevel`, `indicatesMisconception`, `assessedBy`,
`remediatedBy`, `demonstrates`). The concept node shows its **LP level, mastery
and misconception right on it**, and the graph **grows turn by turn** — e.g. the
misconception node only appears for a student who actually holds it. The
`demonstrates` edge links *this answer* to how the node updates.

## Step 5 — Choose the teaching action (panel ⑤)

From the diagnosed evidence the policy selects **exactly one of four actions**:

1. **prerequisite remediation** — a prerequisite gap is detected;
2. **misconception repair** — a misconception is active;
3. **same-level practice** — mastery is still developing;
4. **transfer / debugging** — mastery is strong.

The card shows which action fired, the trigger, and the next task. (For Hello
World, prerequisite remediation rarely fires because the concept is the DAG
root — there is nothing earlier to send the student back to.)

## Step 6 — Write the tutor reply (panel ⑥)

The chosen action + the level + the item type shape the **model tutor
response** — Socratic, it asks the next good question and **never gives the
answer**. This reply goes to the Student tab and becomes context for the next
turn, closing the loop back to Step 0.

---

## Cross-cutting: explanation

Two panels make the process auditable rather than a black box:

- **Chat, explained** — every answer so far, each with the reasoning that
  produced its level and misconception flag.
- **The needed intervention — how to use it** — the chosen action restated in
  plain language for a teacher, with how to apply it.

## Cross-cutting: scenarios

The same process is demonstrated across different **student scenarios** — steady
learner, confident-but-wrong, struggling at Level 0, advanced/fast — so you can
see the workflow adapt: the advanced student skips straight to transfer; the
confident-but-wrong student plateaus and triggers human review; the struggling
student sits at the Level 0 floor with patient same-level practice.

## The loop

```
 student answer
      │
      ▼
 ① LP level (distribution over L0–L4, reported level)
      │
      ▼
 ② mastery (knowledge tracing)
      │
      ▼
 ③ misconception (multi-keyed catalogue)
      │
      ▼
 ④ knowledge graph (concept node + typed edges)
      │
      ▼
 ⑤ tutoring action (one of four)
      │
      ▼
 ⑥ model tutor reply  ──────────►  back to the student (next turn)
```

Every box recomputes on every message; the Teacher tab shows them all at once.
