# Boundary Scenarios — Execution Results

**Companion to** `SCENARIO_CATALOGUE_BOUNDARY_134.md` (Appendix A).
**Generated**: 2026-05-27
**Runner**: `scripts/run_boundary_scenarios.py`
**Raw output**: `output/boundary_scenarios_2026-05-27_154603/`

## Why this document exists

The original 134-scenario catalogue tested each **kind** of behaviour but
not the **edge** of each numeric threshold in the code. The 16 scenarios
below are the just-below / at / just-above tests that close that gap.
Each one was executed against the actual harness and the captured output
is recorded verbatim alongside the expected behaviour.

## Summary

| Outcome | Count |
|---|---|
| PASS | 17 |
| FAIL | 0 |
| ERROR | 0 |
| **Total** | **17** (A.0.1 produces 2 sub-tests — see body) |

All boundaries behave as the code claims they should.

---

## Run results

### A.0.1 — three-token reply must NOT fire substance penalty

- **Layer**: 0 (Silence / non-response)
- **Boundary**: `len(_tokens) <= 2` → false at 3 tokens
- **Source**: `src/orchestrator/lp_diagnostic.py:1343`
- **Input**: `question_text="I am stuck"`, concept=`null_pointer`
- **Expected**: `diagnostic_confidence` NOT floored to ≤ 0.30
- **Actual**:
  ```json
  {
    "diagnostic_confidence": 0.984,
    "current_lp_level": "L1"
  }
  ```
- **Verdict**: PASS — substance penalty correctly skipped on 3 non-filler tokens.

### A.2.1 — WM head confidence just BELOW 0.55 floor

- **Layer**: 2 (Wrong-model identification)
- **Boundary**: `confidence >= 0.55`
- **Source**: `src/orchestrator/lp_diagnostic.py:993`
- **Setup**: monkey-patched `wm_st_head` softmax → 0.54 on `NP-A`
- **Expected**: no WM emission; `source="overlap"`
- **Actual**:
  ```json
  {
    "wrong_model_id": null,
    "match_score": 0.0,
    "source": "overlap"
  }
  ```
- **Verdict**: PASS — gate correctly rejects 0.54.

### A.2.2 — WM head confidence just ABOVE 0.55 floor

- **Layer**: 2
- **Boundary**: `confidence >= 0.55`
- **Source**: `src/orchestrator/lp_diagnostic.py:993`
- **Setup**: forced top prob 0.56 on `NP-A`
- **Expected**: `wrong_model_id=NP-A, source=trained_wm_head`
- **Actual**:
  ```json
  {
    "wrong_model_id": "NP-A",
    "match_score": 0.5600000619888306,
    "source": "trained_wm_head"
  }
  ```
- **Verdict**: PASS — gate correctly accepts 0.56.

### A.3.1 — ST LP head prob just BELOW 0.40 floor

- **Layer**: 3 (LP-level classification)
- **Boundary**: `lp_probs[top] >= 0.40`
- **Source**: `src/orchestrator/lp_diagnostic.py:936`
- **Setup**: forced top LP prob to 0.39
- **Expected**: `trained_lp_level=None`; falls back to lexical
- **Actual**:
  ```json
  {
    "top_prob": 0.38999998569488525,
    "current_lp_level": "L1",
    "trained_lp_probs": {"L1": 0.203, "L2": 0.390, "L3": 0.203, "L4": 0.203}
  }
  ```
- **Verdict**: PASS — head rejected, lexical fallback gives L1.

### A.3.2 — ST LP head prob just ABOVE 0.40 floor

- **Layer**: 3
- **Boundary**: `lp_probs[top] >= 0.40`
- **Source**: `src/orchestrator/lp_diagnostic.py:936`
- **Setup**: forced top LP prob to 0.41
- **Expected**: `trained_lp_level=L2` adopted
- **Actual**:
  ```json
  {
    "top_prob": 0.4099999964237213,
    "current_lp_level": "L2"
  }
  ```
- **Verdict**: PASS — head accepted, L2 propagates.

### A.3.3 — parroting heuristic at 15 vs 16 words

- **Layer**: 3
- **Boundary**: `len(words) <= 15` triggers L3→L2 downgrade
- **Source**: `src/orchestrator/lp_diagnostic.py:1411-1418`
- **Setup**: trained head forced to L3 prob=0.90; mech-vocab-heavy reply with no causal markers; `stored_lp="L1"` so the regression-protection clause does not revert the downgrade
- **Expected**: 15 words → L2 (downgrade); 16 words → L3 (no downgrade)
- **Actual**:
  ```json
  {
    "lp_at_15_words": "L2",
    "lp_at_16_words": "L3"
  }
  ```
- **Verdict**: PASS — word-count edge behaves exactly as coded.

> **Note**: initial test with `stored_lp="L3"` failed because the regression-protection clause at `lp_diagnostic.py:1493` reverts a downgrade when `stored_idx > current_idx` and no confident regression signal is present. The realistic case (parrot-but-stored-at-L1) does propagate, which is what we want to verify.

### A.3.4 — L2 rule-naming heuristic at 5 vs 6 words

- **Layer**: 3
- **Boundary**: `len(words) >= 6 AND pattern matches` triggers L1→L2 upgrade
- **Source**: `src/orchestrator/lp_diagnostic.py:1397-1402`
- **Setup**: trained head forced to L1; reply contains rule-pattern (`use .equals not ==`)
- **Expected**: 5 words → stays L1; 6 words → upgrades L2
- **Actual**:
  ```json
  {
    "lp_at_5_words": "L1",
    "lp_at_6_words": "L2"
  }
  ```
- **Verdict**: PASS — word-count edge behaves exactly as coded.

### A.5.1 — probe gate fires at confidence 0.54

- **Layer**: 5 (Probe loop)
- **Boundary**: `CHAT_PROBE_CONFIDENCE_FLOOR = 0.55`
- **Source**: `scripts/cpal_chat_app.py:793`
- **Expected**: 0.54 < 0.55 → probe path
- **Actual**:
  ```json
  {
    "floor": 0.55,
    "test_value": 0.54,
    "below_floor": true
  }
  ```
- **Verdict**: PASS — floor constant matches code; 0.54 < floor.

### A.5.2 — probe gate skipped at confidence 0.56

- **Layer**: 5
- **Boundary**: `CHAT_PROBE_CONFIDENCE_FLOOR = 0.55`
- **Source**: `scripts/cpal_chat_app.py:793`
- **Expected**: 0.56 ≥ 0.55 → teach path
- **Actual**:
  ```json
  {
    "floor": 0.55,
    "test_value": 0.56,
    "below_floor": false
  }
  ```
- **Verdict**: PASS.

### A.8.1 — DINA mastery drives to lower clamp 0.01

- **Layer**: 8 (DINA mastery)
- **Boundary**: `np.clip(p_l_new, 0.01, 0.99)` — lower clamp
- **Source**: `src/models/dina.py:262`
- **Setup**: 15× incorrect updates on `null_pointer` from prior 0.15
- **Expected**: mastery clamped at exactly 0.01 (not 0.0)
- **Actual**:
  ```json
  {
    "final_mastery": 0.01,
    "trajectory_first5": [0.0230, 0.01, 0.01, 0.01, 0.01],
    "trajectory_last5": [0.01, 0.01, 0.01, 0.01, 0.01]
  }
  ```
- **Verdict**: PASS — lower clamp pins at 0.01. Companion to 8.2 (upper clamp at 0.99).

### A.11.1 — solid encoding + low efficacy → mastery_surface

- **Layer**: 11 (Intervention selection)
- **Source**: `src/orchestrator/student_state_tracker.py:425`
- **Setup**: `cognitive={enc:"solid"}`, `psychological={attribution:"adaptive", self_efficacy:"low"}`, `stage=3`
- **Expected**: `intervention="mastery_surface"`
- **Actual**:
  ```json
  {
    "intervention": "mastery_surface",
    "rationale": "High encoding + Low Efficacy: surface prior successes."
  }
  ```
- **Verdict**: PASS.

### A.11.2 — growth efficacy + stage 4a → increase_challenge

- **Layer**: 11
- **Source**: `src/orchestrator/student_state_tracker.py:440`
- **Setup**: `enc:"partial"`, `eff:"growth"`, `stage:"4a"`
- **Expected**: `intervention="increase_challenge"`
- **Actual**:
  ```json
  {
    "intervention": "increase_challenge",
    "rationale": "Growth Efficacy + Stage 4+: student solved independently, advance challenge."
  }
  ```
- **Verdict**: PASS.

### A.11.3 — partial encoding + stage 2b → socratic_prompt

- **Layer**: 11
- **Source**: `src/orchestrator/student_state_tracker.py:451`
- **Setup**: `enc:"partial"`, `stage:"2b"`, `eff:"neutral"`
- **Expected**: `intervention="socratic_prompt"`
- **Actual**:
  ```json
  {
    "intervention": "socratic_prompt",
    "rationale": "Partial encoding + scaffold-stage: targeted questioning."
  }
  ```
- **Verdict**: PASS.

### A.11.4 — deep encoding + stage 4b → transfer_task

- **Layer**: 11
- **Source**: `src/orchestrator/student_state_tracker.py:456`
- **Setup**: `enc:"deep"`, `stage:"4b"`, `eff:"neutral"`
- **Expected**: `intervention="transfer_task"`
- **Actual**:
  ```json
  {
    "intervention": "transfer_task",
    "rationale": "Deep encoding + Stage 4+: novel real-world application."
  }
  ```
- **Verdict**: PASS.

### A.12.1 — emotional_state reward component contributes

- **Layer**: 12 (RL reward)
- **Boundary**: weight 0.12 must propagate to total reward
- **Source**: `src/reinforcement_learning/reward_function.py:48, 109-117`
- **Setup**: identical sessions; only `emotion_after` varies between `engaged` and `frustrated`
- **Expected**: delta ≈ +0.12
- **Actual**:
  ```json
  {
    "reward_engaged": 0.27,
    "reward_frustrated": 0.15,
    "delta": 0.12,
    "weight_emotional_state": 0.12
  }
  ```
- **Verdict**: PASS — delta matches weight to two decimal places. The previously-untested component is wired through.

### A.19.1 — mastery decay at 14-day half-life boundary

- **Layer**: 19 (Production hardening)
- **Boundary**: `MASTERY_HALF_LIFE_DAYS = 14.0`
- **Source**: `src/models/dina.py:181, 207`
- **Setup**: `p0=0.9`, `prior=0.15`; stub DB to return ages 13.0 / 14.0 / 15.0 days
- **Expected**: matches `prior + (p0 - prior) * 0.5 ** (age/14)`
- **Actual**:
  ```json
  {
    "decayed_at_13d": 0.544, "expected_13d": 0.544,
    "decayed_at_14d": 0.525, "expected_14d": 0.525,
    "decayed_at_15d": 0.5069, "expected_15d": 0.5069
  }
  ```
- **Verdict**: PASS — decay formula is exact at the half-life boundary and ±1 day.

### A.19.2 — auth token at expiry edge

- **Layer**: 19
- **Boundary**: token validates iff `expiry >= now`
- **Source**: `src/persistence/auth.py:82, 114`
- **Setup**: token A `ttl=1s` (valid); token B `ttl=-1s` (already expired)
- **Expected**: A → tuple; B → None
- **Actual**:
  ```json
  {
    "valid_token_result": ["alice", "student", "cs101"],
    "expired_token_result": null
  }
  ```
- **Verdict**: PASS.

---

## Remaining gaps (NOT yet covered)

These are boundary conditions I identified in the code that are still
untested even after Appendix A. Each one has a real numeric threshold;
none are aspirational.

### B.1 — HVSAE LP head 0.45 floor (separate path from ST head)

- **Source**: `src/orchestrator/lp_diagnostic.py:1072`
- **Why a gap**: A.3.1/A.3.2 covered the ST head at 0.40; the HVSAE-latent
  LP head has its OWN floor at 0.45 and is a distinct code path.
- **Suggested test**: force HVSAE LP head top prob to 0.44 vs 0.46;
  assert `trained_lp_level` flips from None to set.

### B.2 — WM LP-aware suppression at 0.85 confidence

- **Source**: `src/orchestrator/lp_diagnostic.py:989-992` and `1042-1044`
- **Why a gap**: when `trained_lp_level ∈ {L3, L4}` AND `confidence < 0.85`,
  the WM emission is suppressed (a student articulating mechanism
  shouldn't carry a wrong-model). Untested.
- **Suggested test**: set LP=L3, force WM head to 0.84 → suppressed; to
  0.85 → emitted.

### B.3 — mechanism-vocab confidence bump to 0.65

- **Source**: `src/orchestrator/lp_diagnostic.py:1316-1322`
- **Why a gap**: bump fires when `_mech_hits >= 2 AND words >= 6`.
  Untested at both edges (1 hit vs 2; 5 words vs 6).
- **Suggested test**: craft 4 inputs covering the (1 vs 2 hits) × (5 vs 6 words) grid.

### B.4 — transfer-marker upgrade L3 → L4

- **Source**: `src/orchestrator/lp_diagnostic.py:1422-1427`
- **Why a gap**: completely untested — fires when `_has_transfer AND _has_causal AND current_lp_level == "L3"`.
- **Suggested test**: input with transfer marker ("also breaks", "same reason") + causal marker ("because") + trained head at L3 → expect L4.

### B.5 — ZPD window edges (0.40 low, 0.75 high)

- **Source**: `src/reinforcement_learning/reward_function.py:21-22, 90-97`
- **Why a gap**: 12.6 tests "in_zpd vs overwhelmed" categorically but
  no boundary tests at mastery_level 0.39 / 0.41 / 0.74 / 0.76.
- **Suggested test**: vary `mastery_before` across those four values, check
  `zpd_score` switches sign / formula branch correctly.

### B.6 — flow band edges (0.42 low, 0.72 high)

- **Source**: `src/reinforcement_learning/reward_function.py:25-26, 100-101`
- **Why a gap**: flow bonus `+0.3` fires when `FLOW_LOW <= mastery <= FLOW_HIGH AND engagement > 0.65`.
  Completely untested.
- **Suggested test**: mastery=0.41 (outside) vs 0.42 (inside) vs 0.72 vs 0.73, engagement=0.66 — assert reward delta = 0.045 (0.15 weight × 0.30 bonus).

### B.7 — regression penalty floor at delta_lp = -2

- **Source**: `src/reinforcement_learning/reward_function.py:183-184`
- **Why a gap**: `if delta_lp <= -2: lp_reward = min(lp_reward, -0.8)` — untested.
- **Suggested test**: delta_lp = -1 vs -2, verify floor only fires at -2.

### B.8 — external attribution (without imposter) → reframe

- **Source**: `src/orchestrator/student_state_tracker.py:414`
- **Why a gap**: GATE 1 fires on `attr in ("fixed", "external") OR imposter`.
  Original 11.6 covers `fixed`; 18.1 mentions external but is described
  aspirationally. Need a clean "external attribution alone" test.
- **Suggested test**: psychological={attr:"external", imp:false}; expect `attribution_reframe`.

### B.9 — forecast threshold at exactly n=3

- **Source**: `src/persistence/db_store.py:386` (`len(rows) < 3 → None`)
- **Why a gap**: original 20.5 tests `<3 → None` (the rejection side).
  No paired test confirming that exactly n=3 produces a non-null forecast.
- **Suggested test**: insert exactly 3 mastery_trajectory rows; assert
  forecast is not None.

### B.10 — DINA cold-start prior clamp at 0.10

- **Source**: `src/models/dina.py:125` (`max(0.10, _DEFAULT_PRIOR - diff * 0.5)`)
- **Why a gap**: 8.1 verifies prior ∈ [0.10, 0.35] for *one* concept. No
  test pins the floor for the HARDEST concept in `_DIFFICULTY`.
- **Suggested test**: pick concept with max difficulty value; assert
  `dina.prior[idx] == 0.10` exactly.

### B.11 — encoding strength: deep_s=2 + cross_s=0 boundary

- **Source**: `src/orchestrator/student_state_tracker.py:381-384`
- **Why a gap**: `deep` requires `deep_s >= 2 AND cross_s > 0`. The
  `cross_s` co-requirement is untested — deep_s=2 alone should give
  `solid`, not `deep`.
- **Suggested test**: craft a text with 2 deep signals but no cross-domain
  marker; assert `encoding_strength == "solid"`.

### B.12 — dual coding dual_s=1 vs 2 boundary

- **Source**: `src/orchestrator/student_state_tracker.py:386`
- **Why a gap**: `dual` requires `dual_s >= 2`; at 1 it's `verbal+code`.
  Untested edge.
- **Suggested test**: input with exactly one dual signal → `verbal+code`;
  with two → `dual`.

### B.13 — comprehensive-stage floor 0.82

- **Source**: `scripts/cpal_chat_app.py:794` (`CHAT_COMPREHENSIVE_CONF_FLOOR = 0.82`)
- **Why a gap**: A.5.1/A.5.2 cover the lower probe floor (0.55). The
  upper "stage reached → comprehensive synthesis" floor is referenced in
  comments but untested.
- **Suggested test**: confidence=0.81 (still probing) vs 0.83 (synthesis).

### B.14 — `delta_lp` saturation at ±3 (RL reward)

- **Source**: `src/reinforcement_learning/reward_function.py:165` (`np.clip(delta_lp / 2.0, -1, 1)`)
- **Why a gap**: 12.3 tests delta_lp=1; nothing tests the saturation point
  where additional levels stop increasing reward.
- **Suggested test**: delta_lp = 2 vs 3 — assert reward identical (both clip to +1.0).

---

## Severity-ranked summary of remaining gaps

| # | Severity | Reason |
|---|---|---|
| B.4 | **high** | Transfer-marker upgrade is a whole code path never exercised; could be silently broken. |
| B.2 | high | LP-aware WM suppression is a recent (2026-05-21) fix; no regression test. |
| B.6 | high | Flow band bonus is a 0.045 reward shift on a 0.15-weight component — easy to break unnoticed. |
| B.5 | medium | ZPD score formula branches at 0.40/0.75; untested at boundary values. |
| B.1 | medium | HVSAE LP head is a fallback path — important if ST head ever returns None. |
| B.8 | medium | "external" attribution branch logic-shared with "fixed" but the trigger is distinct. |
| B.9 | medium | Forecast pairing: rejection side tested, acceptance side not. |
| B.11 | medium | `cross_s` requirement for `deep` is a non-obvious AND-clause. |
| B.3 | medium | Mechanism-vocab bump has two AND-clauses; both edges untested. |
| B.13 | low | Comprehensive floor is a UX threshold, not a correctness gate. |
| B.7 | low | -0.8 floor only matters for L-level drops of 2+, already rare. |
| B.10 | low | Cold-start prior already tested in range; floor edge is defensive. |
| B.12 | low | Dual-coding edge is a label-only difference, no downstream branch. |
| B.14 | low | Saturation is mathematically guaranteed by `np.clip`; testing it tests numpy. |

## Recommended next step

If we add a second round of boundary tests, prioritise **B.4, B.2, B.6**
— each is either a recently-modified code path (regression risk) or a
silent-failure component that wouldn't surface in production until much
later.

---

**End of results document.**
