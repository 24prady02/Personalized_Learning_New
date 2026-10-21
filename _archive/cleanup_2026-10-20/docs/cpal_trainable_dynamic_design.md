# CPAL — Trainable & Dynamic Architecture (Design)

Status: **proposal** · Author: design pass · Scope: Stage 1 (LP diagnostic),
the wrong-models catalogue, and concept detection.

## TL;DR

Today the three diagnostic "parts" — **concept detection**, **LP level
(L1–L4)**, and **wrong mental model** — are each a *static, one-shot, single-
label* guess. This document turns each into a **two-tier component**:

- a **dynamic** (non-parametric) tier — retrieval + LLM-grading — that
  improves the instant you add a catalogue entry or a labelled example, with
  **no retraining**;
- a **trainable** (parametric) tier — the existing heads — that improves when
  retrained, fed by a **data flywheel** that turns every real session into a
  labelled example.

It also makes diagnosis **multi-concept**: one student message can mention
several concepts, and each is probed and levelled independently.

---

## 1. Where we are today (honest assessment)

| Part | How it's decided now | Why it's neither trainable nor dynamic |
|------|----------------------|----------------------------------------|
| Concept | keyword signature table (`_CONCEPT_SIGNATURES`) | hand-written; one concept per message; never learns |
| LP level | keyword classifier + heads (`classify_lp_level`, `cpal_lp_head*.pt`) | heads trained once on synthetic data; val_acc capped ~0.74 |
| Wrong model | overlap matcher / HVSAE cosine / WM head | WM head val_acc **0.04**; catalogue frozen at 20×3 |

**The training pipeline is self-referential.** `cpal_gen_corpus.py` asks
llama3.2 to paraphrase the catalogue's own rubric/belief text; the heads then
learn to classify those paraphrases. The model can never exceed the catalogue
it was generated from.

**The loop is open.** `_cpal_stage4_5` computes `delta_lp` (did the student
move up a level after the tutor's reply?) and persists it to the student
state — but nothing reads it back. The single most valuable signal in the
system is being discarded.

**Diagnosis is single-label.** `_extract_concept` returns one concept;
`diagnose()` produces one LP level and one wrong model. A message like *"my
loop never stops and I think the array index is off"* touches two concepts and
gets collapsed to one.

---

## 2. Design principle — two tiers per part

Every diagnostic part is split into two cooperating tiers:

```
            ┌─────────────────────────────────────────────┐
student ───▶│  DYNAMIC tier  (non-parametric)              │
text        │   retrieval over catalogue + labelled bank   │──┐
            │   + LLM grader against the rubric            │  │
            └─────────────────────────────────────────────┘  │
            ┌─────────────────────────────────────────────┐  ├─▶ arbiter ─▶ result
            │  TRAINABLE tier  (parametric)                │  │   (confidence-
            │   cpal_lp_head_st.pt / wm head / concept head│──┘    weighted)
            └─────────────────────────────────────────────┘
                          ▲
                          │ retrained nightly from …
            ┌─────────────────────────────────────────────┐
            │  DATA FLYWHEEL — interaction_log.jsonl       │
            │  every real session → a labelled example     │
            └─────────────────────────────────────────────┘
```

- **Dynamic tier** = "gets better when you add knowledge." Add a wrong-model
  entry, add a graded example to the bank → retrieval picks it up next call.
  No training, no checkpoint, no downtime.
- **Trainable tier** = "gets better when you add data." The heads stay, but
  they're retrained from real interactions instead of synthetic paraphrases.
- **Arbiter** = a single confidence-weighted fusion step replacing the
  current hand-tuned `if trained… elif semantic… else overlap` chains.

This is the answer to *"trainable AND dynamic"*: the dynamic tier gives
instant adaptivity; the trainable tier gives long-horizon learning; the
flywheel feeds the trainable tier so it actually compounds.

---

## 3. The data flywheel (keystone — build this first)

Nothing else compounds without this. Every session already produces, for
free, everything a labelled example needs:

```jsonc
// data/mental_models/interaction_log.jsonl  — one line per session
{
  "ts": "2026-05-14T14:59:12Z",
  "student_id": "…",
  "text": "my nextLine() after nextInt() reads nothing",
  "code": "…", "error": "…",
  "pred": {                       // what Stage 1 guessed
    "concept": "scanner_buffer", "concept_conf": 0.81,
    "lp_level": "L2",             "lp_conf": 0.55,
    "wrong_model": "SB-A",        "wm_conf": 0.40,
    "source": "arbiter"
  },
  "outcome": {                    // what Stage 4 observed afterwards
    "post_lp_level": "L3", "delta_lp": +1,
    "intervention": "trace_scaffold",
    "student_confirmed": true     // optional: "yes that helped" signal
  }
}
```

**Why this is gold:** `delta_lp > 0` is a *weak label* that the pre-session
diagnosis + chosen intervention were appropriate. `delta_lp <= 0` says they
weren't. After N sessions you have N real, in-distribution `(text → concept,
level, wrong_model)` examples — exactly what the synthetic corpus is a poor
proxy for.

Implementation: a `DiagnosticLogger` appended to in `_cpal_stage4_5`. Cheap,
append-only, no schema migration. **~1 day of work, unblocks everything.**

---

## 4. Part-by-part redesign

### 4a. Concept detection → trainable + multi-label

- **Dynamic now:** keep `_CONCEPT_SIGNATURES` as the cold-start floor; add a
  retrieval step over `java_concept` + signal text (CatalogueRAG already
  embeds these). Returns a *ranked list with scores*, not one string.
- **Multi-label:** `ConceptResolver.resolve(session) → [(concept, conf), …]`.
  Any concept above a threshold is diagnosed independently (see §5).
- **Trainable:** once the flywheel has data, train a small multi-label concept
  head on SBERT embeddings of `text+error`. Labels come from the log (with
  `delta_lp`-confirmed sessions weighted higher). Replaces the hand table as
  it earns its accuracy; the table stays as fallback.
- **Dynamic catalogue hook:** when *every* concept scores below threshold, log
  the text to an `unmatched/` bucket (see §4c).

### 4b. LP level → trainable grader + calibrated confidence

- **Dynamic now:** an **LLM-as-rubric-grader** — send `(student_text, concept
  L1–L4 rubric)` to the model, get back `{level, criteria_met[], confidence}`.
  This is non-parametric: edit the rubric in the catalogue JSON and grading
  changes immediately. It also fixes the core "doesn't feel like a tutor"
  problem — level is judged on *understanding shown*, not vocabulary spotted.
- **Trainable:** the ST head (`cpal_lp_head_st.pt`, the 0.74 one) stays as the
  fast path. Retrain it from the flywheel log instead of `gen_cache.json` —
  real student text, labels = the LLM grader's verdict on the *next* turn
  cross-checked against observed `delta_lp`. This is semi-supervised
  self-training and it *will* push past 0.74 because the data is real.
- **Arbiter:** LLM grader and head agree → high confidence, use it. Disagree →
  lower confidence, and (if it's a concept the student is actively working)
  trigger a probe (§5). The keyword `classify_lp_level` becomes the offline /
  no-API floor only.

### 4c. Wrong models → living, growable catalogue

This is where "dynamic" matters most — the catalogue is currently frozen.

- **Retrieval over a growable bank:** `CatalogueRAG` already embeds the 60
  wrong models. Add a second index: **confirmed examples from the flywheel**
  (`text → wm_id` pairs where the correction worked). Retrieval searches
  both. New examples = better matching, instantly, no retrain.
- **Catalogue grows from real misconceptions:** texts that match *no* wrong
  model well land in `unmatched/`. A periodic job clusters them (embedding
  k-means), LLM-summarises each cluster into a candidate `{wrong_belief,
  origin, conversation_signals}` block, and writes it to
  `catalogue_candidates.json` for **human review**. Approved entries merge
  into the catalogue. The 20×3 catalogue becomes a living store.
- **Trainable:** retire the 0.04 WM *sub-head* — 60-way classification from
  synthetic data is the wrong tool. Replace with retrieval + a binary
  "does this text actually exhibit wm_X" verifier (LLM or a tiny trained
  cross-encoder), which is a far easier learning problem and improves with
  the flywheel.

---

## 5. Multi-concept probing loop

The user's explicit ask: *probe the concept level of each part the student
mentions.* Architecturally:

1. `ConceptResolver` returns **all** concepts above threshold for the message.
2. `diagnose()` runs **per concept** → a list of `LPDiagnostic` objects, each
   with its own level, wrong model, and **confidence**.
3. The orchestrator picks the *focus* concept for this turn (lowest level /
   highest stuck-ness / explicit student focus) but **persists all of them**
   to the student KG — so the others aren't lost.
4. **Active probing:** when the focus part's confidence is low, the selected
   intervention *is* an elicitation turn — a targeted question whose answer
   maps to a specific rubric criterion. The reply is graded against *that
   criterion* next turn, not re-keyword-scanned. Diagnosis becomes a
   diagnose → probe → re-diagnose loop instead of a one-shot guess.

`diagnostic_confidence` per `(student, concept)` is the new state field that
drives whether to teach or to probe.

---

## 6. Feasibility & honest constraints

- **It is feasible** — the encoders (SBERT, HVSAE), the train scripts, the RAG
  index, and the Stage 4 hook all already exist. This is mostly *rewiring*,
  not greenfield.
- **The data ceiling is real.** Until the flywheel has run for a while, the
  trainable tier still leans on synthetic data. That's fine — the **dynamic
  tier carries quality from day one** while the flywheel fills up. Don't
  expect the heads to jump immediately; expect them to *start compounding*.
- **LLM-grader cost:** +1 local model call per session (~1–2 s). Mitigated by
  caching on `(concept, text_hash)` and keeping the keyword classifier as the
  offline fallback. Acceptable for a tutor; measure it.
- **Cold start:** every dynamic component degrades to today's behaviour when
  the API/encoder is unavailable — no regressions, just no upside.
- **Human-in-the-loop is required** for catalogue growth. Auto-generated
  catalogue entries are *candidates*, never auto-merged.

---

## 7. Phased rollout

| Phase | Deliverable | Risk | Unblocks |
|-------|-------------|------|----------|
| **0** | Eval harness — golden set of ~50 labelled turns, run on every change | none | safe iteration on all below |
| **1** | Data flywheel — `DiagnosticLogger` + `interaction_log.jsonl` | low | all training |
| **2** | LLM-rubric-grader (dynamic LP tier) + confidence arbiter | med | "tutor-like" levels |
| **3** | `ConceptResolver` multi-label + retrieval; retire keyword-only path | med | multi-concept probing |
| **4** | Multi-concept `diagnose()` + active probing loop | med | the user's core ask |
| **5** | Retrain heads from flywheel data (semi-supervised) | low | trainable tier compounds |
| **6** | Living catalogue — `unmatched/` clustering → `catalogue_candidates.json` | low | catalogue grows |

Phases 0–1 are prerequisites and cheap. Phase 2 delivers the most visible
quality jump. Phases 3–4 deliver the multi-concept probing. Phases 5–6 are
the long-horizon "it learns from itself" payoff.

---

## 8. New / changed components

| Component | New? | Role |
|-----------|------|------|
| `eval/cpal_golden_set.jsonl` + runner | new | regression measurement (Phase 0) |
| `DiagnosticLogger` (in `lp_diagnostic.py` or new module) | new | append `interaction_log.jsonl` (Phase 1) |
| `RubricGrader` | new | LLM grades text vs L1–L4 rubric (Phase 2) |
| `DiagnosisArbiter` | new | confidence-weighted fusion of tiers (Phase 2) |
| `ConceptResolver` | new | multi-label concept ranking (Phase 3) |
| `LPDiagnostician.diagnose()` | changed | per-concept list; consumes arbiter; probe-aware (Phase 4) |
| `_cpal_stage4_5` | changed | writes flywheel log; grades probe replies (Phase 1, 4) |
| `cpal_train_*` scripts | changed | read `interaction_log.jsonl`, not `gen_cache.json` (Phase 5) |
| `catalogue_growth.py` | new | cluster `unmatched/` → candidate entries (Phase 6) |
| `student_state_tracker.py` | changed | `diagnostic_confidence` per concept (Phase 4) |

---

## Open questions for review

1. LLM-grader: same local Ollama model as the tutor, or a separate smaller
   one for speed?
2. Catalogue growth cadence — manual trigger, or nightly job?
3. Do we keep the HVSAE WM sub-head at all, or fully retire it in Phase 5?
4. Is there any real student-interaction data to seed the flywheel, or does
   Phase 1 start from zero?
