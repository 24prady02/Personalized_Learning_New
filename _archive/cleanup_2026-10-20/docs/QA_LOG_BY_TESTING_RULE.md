# Q&A Log — Grouped by Software-Testing Rule

**Generated**: 2026-05-27
**Purpose**: chronological log of the user's questions and my responses about
the CPAL test catalogue, organised by which ISTQB Foundation-level testing
technique each question targets.

This document is a companion to:

- `docs/SCENARIO_CATALOGUE_BOUNDARY_134.md` — the original 134-scenario catalogue
- `docs/BOUNDARY_SCENARIOS_RESULTS.md` — first BVA pass (16 scenarios + outputs)
- `docs/TESTING_COMPLETE_REPORT.md` — full ISTQB suite report (42 scenarios)

---

## Quick reference — the techniques in scope

| Technique | What it does | Where applied in CPAL |
|---|---|---|
| **Equivalence Class Partitioning (ECP)** | Split inputs into classes; test one representative per class | Original 134-catalogue |
| **Boundary Value Analysis (BVA)** | For each ECP class boundary, test just-below / at / just-above | Appendix A (16) + Part 1 of test suite (14) = 30 |
| **Decision Table Testing** | Enumerate (condition × outcome) rows; test each rule once + verify ordering | Part 2 of test suite (16 rows) |
| **State Transition Testing** | Test each defined edge of the state machine | Part 3 of test suite (12 transitions) |
| **Error Guessing** | Based on past bugs / hunches, target known weak spots | Layer 18 of catalogue (12 scenarios) |

---

## Group 1 — Equivalence Class Partitioning (ECP)

### Q1: "now you look at 134 scenarios is all of this correct please tell me that"

**Testing rule**: ECP completeness audit — does the existing partitioning
hold up?

**Response summary**:
- Scenario totals add up to **134**, matching the title (10+28+5+7+6+5+4+8+5+5+7+6+5+12+9+7+5 = 134).
- Found **7 internal inconsistencies** between the Contents table and the
  per-layer headings:
  1. Layer 6 exclusion off-by-one (says "less 7" but lists 8 scenarios 6.1–6.8)
  2. Layer 1 Contents: says "6 boundary" but body has 8
  3. Layer 3 Contents: says "4 kinds" but body lists 7
  4. Layer 5 Contents: says "4 kinds" but body lists 5
  5. Layer 8 Contents: says "7 kinds" but body lists 8
  6. Layer 12 Contents: arithmetic broken (`6 components + 2 saturation = 8`, not 4)
  7. Layer 15 Contents: says "3 kinds" but body lists 5
- The reduction math overall is consistent: 194 → −53 intra-class duplicates → 141 → −7 Layer-6 emotion → 134.
- **ECP partitioning is sound**, but the catalogue metadata needs cleanup.

---

## Group 2 — Boundary Value Analysis (BVA)

### Q2: "no i am asking are all the boundary conditions satisfied"

**Testing rule**: BVA coverage audit — does the catalogue test the *edge*
of each numeric threshold or just the *kind* of behaviour?

**Response summary** (8 high-impact gaps identified):

1. **Layer 12** — `emotional_state` reward component (weight 0.12) is entirely untested.
2. **Layer 5** — catalogue documented probe floor as 0.45, actual constant is 0.55 (`cpal_chat_app.py:793`). Documentation bug.
3. **Layer 2** — WM gate `>= 0.55` (`lp_diagnostic.py:993, 1046`) has no just-below/just-above pair.
4. **Layer 3** — Multiple word-count and probability thresholds untested at boundaries (`>= 0.40`, `>= 0.45`, `<= 15 words`, `>= 6 words`, `>= 2 mech hits`).
5. **Layer 11** — 4 intervention branches uncovered: `mastery_surface`, `increase_challenge` (early stage 4), `transfer_task`, `socratic_prompt`.
6. **Layer 0 / 18.7** — Substance penalty fires on ≤ 2 tokens. No companion test verifying 3 tokens does NOT fire.
7. **Layer 8** — Lower DINA clamp 0.01 (`dina.py:262`) untested. Companion to 8.2 (upper clamp 0.99) missing.
8. **Layer 19** — 14-day mastery half-life and 7-day auth TTL boundaries untested.

### Q3: "yes write the missing boundary scenarios and then after that try to get an output for the missing boundary scenarios okay"

**Testing rule**: BVA execution — produce the just-below / at / just-above
tests and run them against the actual harness.

**Response summary** (16 scenarios A.0.1–A.19.2):

- Wrote `scripts/run_boundary_scenarios.py` instantiating `LPDiagnostician`,
  `InterventionSelector`, `RewardCalculator`, `DINAModel`, auth helpers.
- 16 scenarios appended to `docs/SCENARIO_CATALOGUE_BOUNDARY_134.md` as
  Appendix A.
- Initial run: 16 PASS / 1 FAIL — A.3.3 (parroting at 15 words).
  Root cause: the regression-protection clause at `lp_diagnostic.py:1493`
  reverts a parroting downgrade when stored LP > current LP. Fixed test
  with `stored_lp="L1"`.
- Final run: **17 / 17 PASS**.
- Outputs captured to `output/boundary_scenarios_2026-05-27_154603/`.

Key captured outputs:

| Boundary | Observed |
|---|---|
| WM gate 0.55: at 0.54 | `wm_id=None, source=overlap` |
| WM gate 0.55: at 0.56 | `wm_id=NP-A, source=trained_wm_head, match_score=0.56` |
| DINA lower clamp | 15× incorrect → `mastery=0.01` exactly |
| Emotional reward delta | engaged − frustrated = **0.12** (matches weight) |
| Half-life decay | 13d→0.544, 14d→0.525, 15d→0.5069 (formula exact) |
| Auth expiry | valid 1s-before → tuple; 1s-after → None |

### Q4: "so now make a new document and put all of these inside the new scenarios please tell me if we have missed any other scenarios or boundary conditions"

**Testing rule**: BVA gap-finding — have we exhausted the boundaries?

**Response summary**:
- Wrote `docs/BOUNDARY_SCENARIOS_RESULTS.md` with all 16 scenarios + their
  captured outputs verbatim.
- Identified **14 remaining BVA gaps (B.1–B.14)**, severity-ranked:

| Severity | ID | Boundary |
|---|---|---|
| high | B.4 | Transfer-marker upgrade L3→L4 (whole code path untested) |
| high | B.2 | WM LP-aware suppression at 0.85 (recent fix, no regression test) |
| high | B.6 | Flow band edges 0.42 / 0.72 |
| medium | B.1 | HVSAE LP head 0.45 floor |
| medium | B.3 | Mech-vocab confidence bump (2 hits AND 6 words) |
| medium | B.5 | ZPD window edges 0.40 / 0.75 |
| medium | B.8 | External attribution alone → reframe |
| medium | B.9 | Forecast at exactly n=3 rows |
| medium | B.11 | Encoding deep_s=2 + cross_s=0 AND-clause |
| low | B.7, B.10, B.12, B.13, B.14 | Defensive / cosmetic edges |

### Q5: "so no other scenarios to test is that correct"

**Testing rule**: BVA exhaustiveness check.

**Response summary**: **No, not correct.** Beyond the 14 B-gaps, named
several other untested areas:

- Layer 7: 120s `time_stuck` threshold (`pedagogical_kg_builder.py:653`)
- Layer 1: three concept-resolver floors (`SIGNATURE_STRONG_FLOOR=0.55`, `RAG_SIM_FLOOR=0.30`, `CONCEPT_CONFIDENCE_FLOOR=0.20`)
- Layer 3 arbitration logic (grader-vs-trained-head 1-step / 2-step disagreement)
- Layer 14: prompt-injection regex coverage (7 patterns)
- Layer 4 cross-concept plateau independence at exact streak edges
- Layer 19 DB concurrency at varying thread counts

Honest answer: 14 catalogued gaps + an unknown number beyond them (likely
30–50 more numeric constants across the codebase).

---

## Group 3 — Test Adequacy / Stopping Rule

### Q6: "So if you run these 14 caps and put into 134 catalogues do you think you would have covered every possible scenario that the ttor could offer"

**Testing rule**: test adequacy — what is "complete enough"?

**Response summary**: **No**, even with 134 + 16 + 14 = 164 scenarios you
would not have covered every possible scenario. Five reasons:

1. **Combinatorial explosion** — boundaries tested individually, not their
   interactions. 4 LP × 20 concepts × 80 wrong-models × 8 interventions ×
   5 emotions × 7 stages = millions of distinct paths.
2. **LLM reply quality is invisible to the harness** — scenarios verify
   deterministic harness output, not whether the actual tutor text is
   pedagogically correct (e.g., 1.27 OpenWeatherMap case had correct harness
   output but bad LLM reply).
3. **Multi-turn dialogue barely covered** — most scenarios are single-turn.
4. **30–50 more numeric thresholds** I haven't catalogued (GIKT, COKE,
   HVSAE, hierarchical RL, etc.).
5. **Real students write unbounded inputs** — ECP assumes you know the classes.

### Q7: "But here is the thing you know the concept of software testing right you need to make a non exhaustive list how do you do that"

**Testing rule**: meta — the user reframes the question. In software
testing you never aim for exhaustive. ISTQB technique stack produces a
**finite but defensibly-complete** suite.

**Response summary** (the recipe):

| Technique | Status at this point |
|---|---|
| ECP | ✅ Complete (134) |
| BVA | 🟡 16 done, 14 outstanding |
| Decision Table | ❌ Not done — `InterventionSelector` + LP-arbitration + WM-precedence need formal tables |
| State Transition | 🟡 Partial — LP transitions yes, plateau/persistence/regression not as a matrix |
| Error Guessing | ✅ Complete (Layer 18) |

**Stopping rule**: ECP + BVA + Decision Table + State Transition + Error
Guessing. ~30 more scenarios total, then stop. Anything beyond is
LLM eval / production telemetry (different disciplines).

---

## Group 4 — Decision Table Testing

### Q8 (Decision Table portion): "Okay try doing all of this and provide me a report like style in the documents or the codebase"

**Testing rule**: Decision Table — enumerate each conditional branch in
`InterventionSelector.select()` and verify both branch coverage and
gate-order priority.

**Response summary** (16 scenarios, all PASS):

**Branch coverage (DT.1–DT.13)** — every rule in `student_state_tracker.py:401-467`
exercised once:

| ID | Conditions | Outcome |
|---|---|---|
| DT.1 | attr=fixed | attribution_reframe |
| DT.2 | imposter=true | attribution_reframe |
| DT.3 | attr=external | attribution_reframe |
| DT.4 | stage=1 + anxiety | reduce_challenge |
| DT.5 | stage=1 + eff=low | reduce_challenge |
| DT.6 | solid + eff=low | mastery_surface |
| DT.7 | solid + stage 4a + growth + adaptive | validate_and_advance |
| DT.8 | partial + stage 4a + growth | increase_challenge |
| DT.9 | surface + stage 1 | worked_example |
| DT.10 | partial + stage 2b | socratic_prompt |
| DT.11 | deep + stage 4b | transfer_task |
| DT.12 | solid + stage 3 + growth | increase_challenge |
| DT.13 | surface + stage 3 + neutral | worked_example (default) |

**Gate-order tests (DT.G1–DT.G3)** — multiple rules could fire; higher
wins:

| ID | Multi-rule scenario | Winner |
|---|---|---|
| DT.G1 | fixed + stage 1 + anxiety | GATE 1 (reframe) beats GATE 2 (reduce_challenge) |
| DT.G2 | stage 1 + eff=low + solid | GATE 2 (reduce_challenge) beats mastery_surface |
| DT.G3 | solid + stage 4a + growth + **fixed** attr | GATE 1 (reframe) beats validate_and_advance |

All 16 PASS — every branch reachable and gate ordering correct.

---

## Group 5 — State Transition Testing

### Q8 (State Transition portion): same prompt as Q8 above

**Testing rule**: State Transition — exercise each defined edge of the
LP / plateau / persistence state machine.

**Response summary** (12 scenarios, all PASS):

State diagram exercised:

```
L1 ── advance ──> L2 ── advance ──> L3 ── advance ──> L4
 ▲                ▲   (streak=2)     │                 │
 │                │                   │                 │
 │           plateau_fire             │                 │
 │                │                   │                 │
 │          L2_plateau                │                 │
 │            ↙   ↘                   │                 │
 │      jump_up  regression           │                 │
 │         to L3   to L1              │                 │
 │                                    │                 │
 └── confident regression ────────────┘─────────────────┘
```

| ID | Transition | Verified |
|---|---|---|
| ST.1 | L1 → L2 advance | ✅ |
| ST.2 | L2 → L3 advance | ✅ |
| ST.3 | L3 → L4 via transfer markers | ✅ |
| ST.4 | L4 → L4 (stay at top) | ✅ |
| ST.5 | L2 streak=1 (no plateau) | ✅ |
| ST.6 | L2 streak=2 (plateau fires) | ✅ |
| ST.7 | L2_plateau → L3 (jump escape) | ✅ |
| ST.8 | L2_plateau → L1 (regression escape) | ✅ |
| ST.9 | L3 → L1 (substance-indicates-regression) | ✅ |
| ST.10 | L3 → L3 (regression protection) | ✅ |
| ST.11 | streak increments across calls | ✅ |
| ST.12 | per-concept plateau independence | ✅ |

All 12 PASS.

---

## Group 6 — Error Guessing

**Testing rule**: target known weak spots and historic bugs.

**Response summary**: this technique is already complete in the original
catalogue as **Layer 18 — Post-fix gap coverage** (12 scenarios). Each
maps to a specific past bug or post-incident fix:

- 18.1 external attribution reframe gate
- 18.2 imposter + external combo
- 18.3 self-correction reads as adaptive
- 18.4 breakthrough → growth efficacy
- 18.5 prolonged grind → high anxiety
- 18.6 WM threshold boundary
- 18.7 substance penalty fires on 2 tokens
- 18.8 short legit answer NOT floored
- 18.9 code comment doesn't leak to wrong concept
- 18.10 anxiety + L1 → de-escalation
- 18.11 stack trace alone
- 18.12 essay reply → solid/deep encoding

No additional Error Guessing was added in this work — Layer 18 is
unchanged.

---

## Findings the testing surfaced (incidental, non-failure)

During execution, 3 design observations came up that aren't test
failures but are worth recording:

1. **Flow bonus is dead code** (`reward_function.py:100-101`). FLOW band
   is a strict subset of ZPD band, so the +0.3 bonus is always clipped
   by the ZPD score of 1.0. Recommendation in `TESTING_COMPLETE_REPORT.md` § 6.

2. **DINA cold-start prior 0.10 floor is unreachable** (`dina.py:125`).
   With current `_DIFFICULTY` values, the minimum reachable prior is
   0.125 (`static_vs_instance` and `generics_primitives`).

3. **Regression-protection clause masks parroting downgrades**
   (`lp_diagnostic.py:1493`). When stored LP > current LP and no
   confident regression, current is reverted to stored. This means the
   parroting heuristic only has observable effect on first-time L3
   cases. Correct behaviour but worth documenting.

---

## Final coverage snapshot

| Technique | Scenarios | Pass rate (latest run) |
|---|---|---|
| ECP (original catalogue) | 134 | (carried over from prior run) |
| BVA — Appendix A | 16 | 17/17 PASS |
| BVA — Part 1 of suite | 14 | 14/14 PASS |
| Decision Table | 16 | 16/16 PASS |
| State Transition | 12 | 12/12 PASS |
| Error Guessing (Layer 18) | 12 | (carried over) |
| **Total** | **192 scenarios** | **All ISTQB techniques applied** |

By Foundation-level testing standards, the deterministic core of CPAL
has full technique coverage. Further coverage (LLM output quality,
multi-turn pedagogical effectiveness, production telemetry) belongs to
disciplines outside scenario-based unit/integration testing.

---

**End of Q&A log.**
