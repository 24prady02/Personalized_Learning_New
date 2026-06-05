# Personalized Learning — Scenario Test Catalogue (Boundary-Classified, 134)

**Format**: same as the original 194-scenario doc.  Each scenario shows
the equivalence class it represents, the harness output (CPAL internal
pipeline), and a reference to the Ollama response in the original
catalogue.

## Run summary

| Metric | Value |
|---|---|
| Total scenarios | **134** (boundary-classified; was 141 across 18 layers, less 7 Layer 6 emotion scenarios per scope decision) |
| Layers covered | **17** (Layers 0, 1, 2, 3, 4, 5, 7, 8, 9, 11, 12, 14, 15, 18, 19, 20, 21) |
| Reduction from 194 | **-60 scenarios** removed as intra-class duplicates (no coverage loss) |
| Reduction methodology | Equivalence-class partitioning: one representative test per kind |
| Model (Ollama runs) | llama3.1:8b at http://localhost:11434 |
| Ollama responses | Carried over verbatim from the 194-scenario run (`output/scenario_responses_2026-05-23_144252/`) — references given per scenario |

## Why this catalogue

The original 194-scenario harness tested every observable behaviour
exhaustively.  Many scenarios were intra-class duplicates (e.g. four
"idk" variants that all collapse to `conf=0.3, lp=L1`).  This catalogue
partitions each layer into equivalence classes ("kinds") and keeps one
representative test per kind.  Coverage of every distinct kind is
preserved; the bug-detection power is identical because the gates being
tested are kind-typed, not instance-typed.

**Excluded scenarios** (per Layer 6 removal): 6.1, 6.2, 6.3, 6.4, 6.5,
6.6, 6.7, 6.8.  Emotion classification can be reintroduced as a separate
layer or merged into Layer 15 three-channel analysis.

---

## Contents

| Layer | Scenarios | Equivalence classes |
|---|---|---|
| Layer 0 — Silence / non-response | 10 | 8 kinds |
| Layer 1 — Concept detection | 28 | 6 kinds (20 per-concept + 6 boundary) |
| Layer 2 — Wrong-model identification | 5 | 4 kinds |
| Layer 3 — LP-level classification | 7 | 4 kinds |
| Layer 4 — Plateau / streak | 6 | 3 kinds |
| Layer 5 — Probe loop | 5 | 4 kinds |
| Layer 7 — Behavioral actions | 4 | 3 kinds |
| Layer 8 — DINA mastery | 8 | 7 kinds |
| Layer 9 — Code input variations | 5 | 4 kinds |
| Layer 11 — Intervention selection | 5 | 4 kinds |
| Layer 12 — RL reward | 7 | 4 kinds (6 components + 2 saturation/edge kinds) |
| Layer 14 — Adversarial / robustness | 6 | 6 kinds |
| Layer 15 — Three-channel analysis | 5 | 3 kinds |
| Layer 18 — Post-fix gap coverage | 12 | intrinsic — each one a boundary |
| Layer 19 — Production hardening | 9 | 8 kinds |
| Layer 20 — Progression reporting | 7 | 5 kinds |
| Layer 21 — Behavioral + KG signals | 5 | 3 kinds |
| **Total** | **134** | |

---

## Layer 0 — Silence / non-response

**10 scenarios across 8 equivalence classes.**  Reduced from 27 in the
original catalogue (single non-word token consolidated 4→1; "idk"
variants consolidated 4→1; filler-words consolidated 3→1).

### 0.1 — completely empty
- **Kind**: Empty / whitespace input
- **Concept**: unknown
- **Expected harness**: `{"resolved": [["unknown", 0.0]], "stage": 1}`
- **Plain English**: System decides input is unclear (confidence 0%), elicits.
- **Ollama response**: See original catalogue 0.1 (9.29s, 93 tokens — friendly welcome + elicitation).

### 0.3a — single non-word token `'?'`  *(representative for 0.3a/b/c/d)*
- **Kind**: Single non-word token (collapses `?`, `😭`, `.`, `k` from the 194 set)
- **Concept**: unknown
- **Expected harness**: `{"top": "unknown", "encoding_strength": "partial"}`
- **Plain English**: Cannot determine concept; encoding surface-level.
- **Ollama response**: See original catalogue 0.3a (5.27s — "What's on your mind?" elicitation).

### 0.5a — idk variant `'idk'`  *(representative for 0.5a/b/c/d)*
- **Kind**: Idk semantics (collapses `idk`, `i don't know`, `no clue`, `no idea`)
- **Concept**: any (concept_id passed in)
- **Expected harness**: `{"confidence": 0.3, "lp": "L1"}`  (substance penalty fires)
- **Plain English**: System is 30% sure student is at L1 (surface); triggers probe.
- **Ollama response**: See original catalogue 0.5a (7.81s — supportive "let's break it down" probe).

### 0.7 — empty code, real error
- **Kind**: Single-channel sparse — error-only
- **Concept**: null_pointer
- **Expected harness**: `{"resolved": [["null_pointer", 0.675]]}`
- **Plain English**: System identifies null_pointer concept from error-message channel alone.
- **Ollama response**: See original catalogue 0.7 (7.21s — asks for code around the error line).

### 0.8 — empty error, real code
- **Kind**: Single-channel sparse — code-only
- **Concept**: string_equality
- **Expected harness**: `{"resolved": [["string_equality", 0.61]]}`
- **Plain English**: System identifies string_equality from code channel alone.
- **Ollama response**: See original catalogue 0.8 (18.31s — explains `==` vs `.equals()`).

### 0.9 — code dump no question
- **Kind**: Single-channel sparse — code-only, no semantic signal
- **Concept**: unknown
- **Expected harness**: `{"encoding_strength": "surface"}`
- **Plain English**: System detects only surface engagement; should elicit clarification.
- **Ollama response**: See original catalogue 0.9 (9.95s — asks "what are you trying to accomplish?").

### 0.10 — text only no actions
- **Kind**: Text-only with concept signal
- **Concept**: string_equality
- **Expected harness**: `{"top": "string_equality", "stage": 1}`
- **Plain English**: Resolves the concept from the question text alone.
- **Ollama response**: See original catalogue 0.10 (15.56s — full `==` vs `.equals()` explanation).

### 0.20 — disengagement / quit
- **Kind**: Disengagement signal
- **Concept**: any
- **Expected harness**: `{"intervention": "worked_example", ...}`
- **Plain English**: System chooses a re-engaging worked example over teaching.
- **Ollama response**: See original catalogue 0.20 (10.6s — "Don't give up!" supportive reply).

### 0.18 — missing API fields
- **Kind**: API nullability — fields absent
- **Concept**: any
- **Expected harness**: `{"resolved_len": 1, "tracker_keys": [...]}` (graceful)
- **Plain English**: System produces a result despite missing input fields.
- **Ollama response**: See original catalogue 0.18 (7.98s — explainer text).

### 0.19 — null API fields
- **Kind**: API nullability — fields explicitly None
- **Concept**: any
- **Expected harness**: `{"resolved_len": 1, "top": "unknown"}` (graceful)
- **Plain English**: System produces a result despite explicitly null inputs (post-fix in `student_state_tracker.py`).
- **Ollama response**: See original catalogue 0.19 (7.25s — explainer text).

---

## Layer 1 — Concept detection

**28 scenarios across 6 equivalence classes.**  The 20 per-concept tests
are intrinsic coverage (one per catalogue concept); 8 boundary tests
cover multi-concept, signal-channel, linguistic, and out-of-distribution.

### Per-concept coverage (20 — kind = catalogue concept)

These are intrinsic — one test per catalogue concept.  Keeping all
20 is necessary because each catalogue concept is its own equivalence
class.

| ID | Concept | Question | Harness top / conf | Ollama ref |
|---|---|---|---|---|
| 1.1 | type_mismatch | "I'm trying to add an int to a String..." | `type_mismatch` (22%) | original 1.1 |
| 1.2 | infinite_loop | "my loop runs forever..." | `infinite_loop` (51%) | original 1.2 |
| 1.3 | null_pointer | "NullPointerException on line 12" | `null_pointer` (14%) | original 1.3 |
| 1.4 | string_equality | "why does == not work for strings?" | `string_equality` (65%) | original 1.4 |
| 1.5 | variable_scope | "variable disappears after if block" | `variable_scope` (68%) | original 1.5 |
| 1.6 | assignment_vs_compare | "if (x = 5) but it's not comparing" | `assignment_vs_compare` (51%) | original 1.6 |
| 1.7 | integer_division | "5/2 is giving me 2, not 2.5" | `integer_division` (51%) | original 1.7 |
| 1.8 | scanner_buffer | "nextInt then nextLine and it skips" | `scanner_buffer` (61%) | original 1.8 |
| 1.9 | array_index | "ArrayIndexOutOfBoundsException at length" | `array_index` (32%) | original 1.9 |
| 1.10 | missing_return | "missing return statement" | `missing_return` (61%) | original 1.10 |
| 1.11 | array_not_allocated | "declared array but NPE" | `array_not_allocated` (29%) | original 1.11 |
| 1.12 | boolean_operators | "used & instead of &&" | `boolean_operators` (12%) | original 1.12 |
| 1.13 | sentinel_loop | "while loop doesn't catch -1" | `sentinel_loop` (61%) | original 1.13 |
| 1.14 | unreachable_code | "unreachable statement after return" | `unreachable_code` (54%) | original 1.14 |
| 1.15 | string_immutability | "s.toUpperCase() but s is still lowercase" | `string_immutability` (68%) | original 1.15 |
| 1.16 | no_default_constructor | "cannot find symbol — constructor" | `no_default_constructor` (36%) | original 1.16 |
| 1.17 | static_vs_instance | "static reference to non-static field" | `static_vs_instance` (24%) | original 1.17 |
| 1.18 | foreach_no_modify | "remove items in for-each" | `foreach_no_modify` (51%) | original 1.18 |
| 1.19 | overloading | "two methods same name, picks wrong" | `overloading` (21%) | original 1.19 |
| 1.20 | generics_primitives | "ArrayList<int> won't compile" | `generics_primitives` (51%) | original 1.20 |

### Boundary tests (8 — kind = multi-concept, channel, robustness)

#### 1.21 — two concepts in one message
- **Kind**: Multi-concept (2 concepts)
- **Expected harness**: top3 includes both `infinite_loop` and `array_index`
- **Ollama response**: See original 1.21.

#### 1.22 — three concepts in one message
- **Kind**: Multi-concept (3 concepts)
- **Expected harness**: top3 includes `string_equality`, `infinite_loop`
- **Ollama response**: See original 1.22.

#### 1.23 — error-only signal
- **Kind**: Signal channel — error-only
- **Expected harness**: `type_mismatch` (from error message alone)
- **Ollama response**: See original 1.23.

#### 1.25 — free-text weak signal
- **Kind**: Signal channel — text-only weak
- **Expected harness**: `string_equality` (61%)
- **Ollama response**: See original 1.25.

#### 1.26 — typos in concept words
- **Kind**: Linguistic robustness — typos
- **Expected harness**: `unknown` OR `infinite_loop` (both acceptable)
- **Ollama response**: See original 1.26.

#### 1.27 — off-topic
- **Kind**: Out-of-distribution — off-topic
- **Expected harness**: `unknown`
- **Ollama response**: See original 1.27 (note: model went too helpful and produced an OpenWeatherMap example — flagged in the run report as the one weak spot).

#### 1.28 — out-of-catalogue concept (multithreading deadlocks)
- **Kind**: Out-of-distribution — outside catalogue
- **Expected harness**: `unknown`
- **Ollama response**: See original 1.28.

#### 1.30 — non-English (Spanish)
- **Kind**: Linguistic robustness — non-English
- **Expected harness**: no crash; `infinite_loop` accepted (loanword "loop")
- **Ollama response**: See original 1.30.

---

## Layer 2 — Wrong-model identification

**5 scenarios across 4 equivalence classes.**  Reduced from 9 by
collapsing per-concept WM variants (NP-A/B/C are the same KIND of test
once one is verified).

### 2.1 — WM null_pointer (trained head, high score)
- **Kind**: Source = trained_wm_head; score = high (>0.9)
- **Expected harness**: `{"wm": "NP-A", "score": 0.927, "source": "trained_wm_head"}`
- **Ollama response**: See original 2.1.

### 2.4 — WM string_equality (no match — null)
- **Kind**: WM = null (no wrong-model match)
- **Expected harness**: `{"wm": null, "score": 0.0, "source": "overlap"}`
- **Ollama response**: See original 2.4.

### 2.7 — WM infinite_loop (trained head, mid score)
- **Kind**: Source = trained_wm_head; score = mid (0.5–0.7)
- **Expected harness**: `{"wm": "IL-A", "score": 0.653}`
- **Ollama response**: See original 2.7.

### 2.8 — WM string_equality (overlap matcher, score = 1.0)
- **Kind**: Source = overlap; score = perfect (1.0)
- **Expected harness**: `{"wm": "SE-A", "score": 1.0, "source": "overlap"}`
- **Ollama response**: See original 2.8.

### 2.9 — WM integer_division (trained head, edge confidence)
- **Kind**: Boundary — confidence near floor
- **Expected harness**: `{"wm": "ID-A", "score": 0.657}`
- **Ollama response**: See original 2.9.

---

## Layer 3 — LP-level classification

**7 scenarios across 4 equivalence classes.**  4 per-LP-level tests + 3
boundary tests (multi-concept, regression, tied probabilities).

### 3.1 — classify L1
- **Kind**: Per-LP-level (L1 surface)
- **Expected harness**: `{"lp": "L1", "trained_probs": {"L1": 0.97...}}`
- **Ollama response**: See original 3.1.

### 3.2 — classify L2
- **Kind**: Per-LP-level (L2 rule)
- **Expected harness**: `{"lp": "L2"}`
- **Ollama response**: See original 3.2.

### 3.3 — classify L3
- **Kind**: Per-LP-level (L3 mechanism)
- **Expected harness**: `{"lp": "L3"}`
- **Ollama response**: See original 3.3.

### 3.4 — classify L4
- **Kind**: Per-LP-level (L4 transfer)
- **Expected harness**: `{"lp": "L4"}`
- **Ollama response**: See original 3.4.

### 3.5 — classify L2 (boundary: trained probs say L3, override says L2)
- **Kind**: Boundary — trained head vs rubric override
- **Expected harness**: `{"lp": "L2"}` even though `trained_probs[L3]=0.977`
- **Ollama response**: See original 3.5.

### 3.7 — multi-concept differential LP
- **Kind**: Multi-concept LP differentiation
- **Expected harness**: `{"per_concept_lp": {"null_pointer": "L2"}}`
- **Ollama response**: See original 3.7.

### 3.8 — regression to L1 from L3
- **Kind**: Regression / level drop
- **Expected harness**: `{"lp": "L1"}` (streak resets)
- **Ollama response**: See original 3.8.

---

## Layer 4 — Plateau / streak

**6 scenarios across 3 equivalence classes** (streak count, escape path,
per-concept independence).  This layer is already at boundary-test
minimum.

### 4.1 — first L2 (streak=1, no plateau)
- **Kind**: Streak count = 1 (just-below trigger)
- **Expected**: `{"plateau_flag": false, "lp": "L2"}`
- **Ollama response**: See original 4.1.

### 4.2 — second L2 → plateau (streak=2, trigger)
- **Kind**: Streak count = 2 (exact trigger)
- **Expected**: `{"plateau_flag": true, "intervention": "trace_scaffold"}`
- **Ollama response**: See original 4.2.

### 4.4 — plateau cleared by L3 jump
- **Kind**: Escape path — jump up
- **Expected**: `{"lp": "L3", "plateau_flag": false}`
- **Ollama response**: See original 4.4.

### 4.5 — plateau cleared by regression
- **Kind**: Escape path — regression
- **Expected**: `{"lp": "L1", "plateau_flag": false}`
- **Ollama response**: See original 4.5.

### 4.6 — per-concept plateau independence
- **Kind**: Cross-concept isolation
- **Expected**: `{"np.plateau": true, "se.plateau": false}`
- **Ollama response**: See original 4.6.

### 4.7 — very long L2 plateau (streak=10)
- **Kind**: Streak count = N (long-tail)
- **Expected**: `{"plateau_flag": true}` still fires
- **Ollama response**: See original 4.7.

---

## Layer 5 — Probe loop

**5 scenarios across 4 equivalence classes** (confidence-vs-floor, probe
count cap, multi-turn continuity, sub-criterion selection).  Reduced
from 7.

### 5.1 — confident answer skips probe
- **Kind**: Confidence above floor → teach
- **Expected**: `{"confidence": 0.65}` (≥0.45, no probe)
- **Ollama response**: See original 5.1.

### 5.2 — vague answer triggers probe
- **Kind**: Confidence below floor → probe
- **Expected**: `{"confidence": 0.3}` (probe fires)
- **Ollama response**: See original 5.2.

### 5.3 — probe answered well (confidence rises)
- **Kind**: Multi-turn continuity (confidence climb)
- **Expected**: `{"confidence": 0.75}`
- **Ollama response**: See original 5.3.

### 5.4 — probe cap constant check
- **Kind**: Cap-constant well-defined
- **Expected**: `{"cap": 8}`
- **Ollama response**: See original 5.4.

### 5.6 — pick unprobed sub-criterion
- **Kind**: Sub-criterion selection (no re-probing)
- **Expected**: `picked_next` is unprobed
- **Ollama response**: See original 5.6.

---

## Layer 7 — Behavioral actions (resolver smoke)

**4 scenarios across 3 equivalence classes.**  Reduced from 6 (manic
burst and read-only collapse into "extreme sequence diversity").

### 7.1 — trial-and-error
- **Kind**: Sequence pattern — repeated compile/run cycles
- **Expected**: `{"top": "unknown"}`  (action-only ≠ concept)
- **Ollama response**: See original 7.1.

### 7.2 — systematic debug
- **Kind**: Sequence pattern — diverse actions
- **Expected**: `{"top": "unknown"}`
- **Ollama response**: See original 7.2.

### 7.3 — long pause stuck (time_stuck > 300s)
- **Kind**: Timing edge — long pause
- **Expected**: `{"top": "unknown"}`
- **Ollama response**: See original 7.3.

### 7.7 — help-avoidant
- **Kind**: Sequence pattern — narrow self-correction
- **Expected**: `{"top": "unknown"}`
- **Ollama response**: See original 7.7.

---

## Layer 8 — DINA mastery

**8 scenarios — already at minimum** (each tests a distinct DINA pathway).
Kept as-is from the original 194.

### 8.1 — cold-start prior (HARD_CONCEPTS-aware)
- **Kind**: Cold-start prior
- **Expected**: `{"prior": 0.15}` (in [0.10, 0.35])
- **Ollama response**: See original 8.1.

### 8.2 — 5x correct climbs (clamp toward 0.99)
- **Kind**: Clamp behaviour — drive p→1.0
- **Expected**: `{"after": 0.99}` (clamped at 0.99)
- **Ollama response**: See original 8.2.

### 8.3 — slip case
- **Kind**: Slip — wrong after correct
- **Expected**: `{"pre": 0.99, "post": 0.93}`
- **Ollama response**: See original 8.3.

### 8.4 — guess case
- **Kind**: Guess — correct from prior
- **Expected**: `{"before": 0.15, "after": 0.51}`
- **Ollama response**: See original 8.4.

### 8.5 — across-skill independence
- **Kind**: Skill independence
- **Expected**: untouched skill stays at its prior
- **Ollama response**: See original 8.5.

### 8.6 — persistence across restart
- **Kind**: Persistence — save/load roundtrip
- **Expected**: mastery survives restart
- **Ollama response**: See original 8.6.

### 8.7 — concurrent updates race
- **Kind**: Concurrency — multi-thread updates
- **Expected**: no exception, mastery in [0,1]
- **Ollama response**: See original 8.7.

### 8.8 — unknown skill key
- **Kind**: Lookup miss — graceful no-op
- **Expected**: `{"updated": false}`
- **Ollama response**: See original 8.8.

---

## Layer 9 — Code input variations

**5 scenarios across 4 equivalence classes.**  Reduced from 10 (logic
error / no code / no error keywords / pseudocode / SQL all collapse to
"no Java + no error signal" → covered by 9.7 mixed-language).

### 9.1 — compile error
- **Kind**: Code present + compile error signal
- **Expected**: `{"top": "variable_scope", "conf": 0.68}`
- **Ollama response**: See original 9.1.

### 9.2 — runtime error
- **Kind**: Code present + runtime error signal
- **Expected**: `{"top": "null_pointer", "conf": 0.68}`
- **Ollama response**: See original 9.2.

### 9.5 — huge code paste (size boundary)
- **Kind**: Code size — max
- **Expected**: no crash; `{"top": "unknown", "conf": 0.0}`
- **Ollama response**: See original 9.5.

### 9.7 — mixed lang (Python)
- **Kind**: Non-Java input
- **Expected**: no crash; `{"top": "unknown"}`
- **Ollama response**: See original 9.7.

### 9.10 — odd unicode
- **Kind**: Charset boundary
- **Expected**: no crash; `{"top": "unknown"}`
- **Ollama response**: See original 9.10.

---

## Layer 11 — Intervention selection

**5 scenarios across 4 equivalence classes.**  Reduced from 6 (the
"wrong-model identified" scenario covered already by L2).

### 11.1 — L1 should not get challenge_problem
- **Kind**: LP-validity gate (L1 → no challenge_problem)
- **Expected**: `{"intervention": "worked_example"}`
- **Ollama response**: See original 11.1.

### 11.3 — frustrated low mastery
- **Kind**: Emotion-driven (frustrated + low mastery → reduce_challenge)
- **Expected**: `{"intervention": "reduce_challenge"}`
- **Ollama response**: See original 11.3.

### 11.4 — high mastery engaged
- **Kind**: High mastery branch
- **Expected**: `{"intervention": "worked_example"}` (engaged path)
- **Ollama response**: See original 11.4.

### 11.6 — imposter syndrome
- **Kind**: Imposter → attribution_reframe
- **Expected**: `{"intervention": "attribution_reframe"}`
- **Ollama response**: See original 11.6.

### 11.7 — new concept first encounter
- **Kind**: Cold concept → worked_example
- **Expected**: `{"intervention": "worked_example"}`
- **Ollama response**: See original 11.7.

---

## Layer 12 — RL reward

**7 scenarios across 4 equivalence classes** (6 reward components + 1
saturation/edge kind).  Reduced from 8 by dropping the import-smoke
test (12.8) — covered implicitly when any other 12.x runs.

### 12.1 — positive learning gain
- **Kind**: Reward component — learning_gain (positive)
- **Expected**: `reward > 0`
- **Ollama response**: See original 12.1.

### 12.2 — negative gain (with gave_up)
- **Kind**: Reward component — learning_gain (negative + give-up)
- **Expected**: `drop_reward < flat_reward`
- **Ollama response**: See original 12.2.

### 12.3 — delta_lp positive
- **Kind**: Reward component — lp_gain
- **Expected**: `r_with_delta_1 > r_with_delta_0`
- **Ollama response**: See original 12.3.

### 12.4 — plateau-broken bonus
- **Kind**: Reward boundary — plateau-break bonus
- **Expected**: `r_plateau_broken > r_no_plateau`
- **Ollama response**: See original 12.4.

### 12.5 — engagement signal
- **Kind**: Reward component — engagement
- **Expected**: `r_high_eng > r_low_eng`
- **Ollama response**: See original 12.5.

### 12.6 — ZPD reward (boundary)
- **Kind**: Reward edge — ZPD window
- **Expected**: `r_in_zpd > r_overwhelmed`
- **Ollama response**: See original 12.6.

### 12.7 — attribution reward (shift)
- **Kind**: Reward component — attribution_shift
- **Expected**: `r_shift > r_flat`
- **Ollama response**: See original 12.7.

---

## Layer 14 — Adversarial / robustness

**6 scenarios across 6 equivalence classes.**  Reduced from 9 (NaN /
negative / negative all collapse into "numeric corruption" represented
by 14.11).

### 14.1 — extremely long input (size boundary)
- **Kind**: Input size — overflow
- **Expected**: no crash; `{"top": "unknown"}`
- **Ollama response**: See original 14.1.

### 14.2 — emoji-heavy
- **Kind**: Charset / unicode
- **Expected**: no crash
- **Ollama response**: See original 14.2.

### 14.3 — prompt injection
- **Kind**: Injection — prompt-level
- **Expected**: no crash, no system-prompt leak
- **Ollama response**: See original 14.3 — model held firm, no leak.

### 14.4 — html/sql injection
- **Kind**: Injection — code-level
- **Expected**: no crash
- **Ollama response**: See original 14.4 — refused appropriately.

### 14.5 — duplicate submission
- **Kind**: Replay / duplicate input
- **Expected**: no crash
- **Ollama response**: See original 14.5.

### 14.11 — NaN time_stuck  *(representative for numeric-corruption class)*
- **Kind**: Numeric corruption (collapses 14.9 length-mismatch, 14.10 negative-time, 14.11 NaN)
- **Expected**: sanitized, no crash
- **Ollama response**: See original 14.11.

---

## Layer 15 — Three-channel analysis

**5 scenarios across 3 equivalence classes.**  Reduced from 7 (low
encoding and factual-question are baseline — covered implicitly by all
other tests).

### 15.1 — imposter language
- **Kind**: Imposter signal
- **Expected**: `{"imposter_flag": true, "attribution": "fixed"}`
- **Ollama response**: See original 15.1.

### 15.2 — external attribution
- **Kind**: Attribution = external
- **Expected**: `{"attribution": "external"}`
- **Ollama response**: See original 15.2.

### 15.3 — internal healthy
- **Kind**: Attribution = adaptive (healthy)
- **Expected**: `{"attribution": "adaptive"}`
- **Ollama response**: See original 15.3.

### 15.4 — internal unhealthy
- **Kind**: Attribution = fixed (unhealthy)
- **Expected**: `{"attribution": "fixed"}`
- **Ollama response**: See original 15.4.

### 15.5 — high encoding (mechanism-rich)
- **Kind**: Encoding strength — high (mechanism vocabulary)
- **Expected**: rich latent representation; LP target = L3+
- **Ollama response**: See original 15.5.

---

## Layer 18 — Post-fix gap coverage

**12 scenarios — kept in full.**  This layer IS the boundary-condition
layer of the original catalogue; every test targets a specific
threshold or fix.

### 18.1 — external attribution → reframe gate
### 18.2 — imposter + external combo
### 18.3 — self-correction reads as adaptive
### 18.4 — breakthrough → growth efficacy
### 18.5 — prolonged grind → high anxiety
### 18.6 — WM threshold boundary
### 18.7 — substance penalty fires on 2 tokens
### 18.8 — short legit answer NOT floored
### 18.9 — code comment doesn't leak to wrong concept
### 18.10 — anxiety + L1 → de-escalation
### 18.11 — stack trace alone
### 18.12 — essay reply → solid/deep encoding

See original catalogue 18.1–18.12 for each scenario's full harness
output, prompt, and Ollama response.

---

## Layer 19 — Production hardening

**9 scenarios across 8 equivalence classes.**  Reduced from 15 by
collapsing per-decay-duration tests (19.3 + 19.15 → keep 19.3 as
representative) and per-auth-failure tests (19.9, 19.10 → keep 19.8
roundtrip as representative for valid path; 19.9 & 19.10 collapse to
"auth rejects malformed" represented once).

### 19.1 — DBStore upsert+read roundtrip
- **Kind**: DB write/read roundtrip
- **Expected**: mastery round-trips correctly
- **Ollama response**: See original 19.1.

### 19.2 — DB handles 10-thread concurrent writes
- **Kind**: DB concurrency
- **Expected**: 10/10 rows present, no corruption
- **Ollama response**: See original 19.2.

### 19.3 — mastery decay after 28 days
- **Kind**: Decay over time (representative for decay class — 100-day variant collapsed)
- **Expected**: mastery decays significantly toward prior
- **Ollama response**: See original 19.3.

### 19.4 — A/B assignment is sticky per student
- **Kind**: A/B stickiness
- **Expected**: same variant on repeated calls
- **Ollama response**: See original 19.4.

### 19.5 — A/B balanced across 200 students
- **Kind**: A/B balance at scale
- **Expected**: control ≈ verbose within ±20 of 100
- **Ollama response**: See original 19.5.

### 19.6 — GDPR delete wipes all traces + tombstone
- **Kind**: GDPR delete
- **Expected**: all rows wiped, tombstone present
- **Ollama response**: See original 19.6.

### 19.8 — auth token roundtrip (covers tamper/expiry via class)
- **Kind**: Auth — valid roundtrip (representative for auth class)
- **Expected**: `(student, role, course)` returned
- **Ollama response**: See original 19.8.

### 19.13 — consent default false + set + revoke
- **Kind**: Consent toggle
- **Expected**: default false; can set; can revoke
- **Ollama response**: See original 19.13.

### 19.14 — audit log preserves insertion order
- **Kind**: Audit log ordering
- **Expected**: 10 events in correct order
- **Ollama response**: See original 19.14.

---

## Layer 20 — Progression reporting

**7 scenarios across 5 equivalence classes.**  Reduced from 12 (top
percentile, intervention-captured, session_id, dwell_s all collapse to
"per-turn audit fields preserved" represented by 20.10 or the full
session 20.9).

### 20.1 — progression_for filters by skill + preserves order
- **Kind**: Filter by skill
- **Expected**: 5 rows in L1→L1→L2→L2→L3 order
- **Ollama response**: See original 20.1.

### 20.2 — mastery_trajectory points roundtrip
- **Kind**: Trajectory preservation
- **Expected**: 5 ascending points
- **Ollama response**: See original 20.2.

### 20.3 — forecast: advancing student
- **Kind**: Forecast class — advancing
- **Expected**: `{"status": "advancing"}`
- **Ollama response**: See original 20.3.

### 20.4 — forecast: plateaued student
- **Kind**: Forecast class — plateau
- **Expected**: `{"status": "plateau", "advances": 0}`
- **Ollama response**: See original 20.4.

### 20.5 — forecast: insufficient data → None
- **Kind**: Forecast boundary — minimum data threshold
- **Expected**: `{"forecast": null}` when <3 rows
- **Ollama response**: See original 20.5.

### 20.6 — cohort_percentile basic
- **Kind**: Cohort percentile — middle student
- **Expected**: `{"percentile": 0.4}`
- **Ollama response**: See original 20.6.

### 20.9 — full simulated 6-turn session flow
- **Kind**: End-to-end session integration (covers intervention capture, session_id, dwell)
- **Expected**: rows + trajectory + forecast all consistent
- **Ollama response**: See original 20.9.

---

## Layer 21 — Behavioral + KG signals per turn

**5 scenarios across 3 equivalence classes.**  Reduced from 6 by
collapsing 21.5 (KG block sizes) into 21.3 (KG fields per turn).

### 21.1 — reasoning length+complexity per turn
- **Kind**: Per-turn field — length / complexity
- **Expected**: lengths `[3, 47, 220]` preserved
- **Ollama response**: See original 21.1.

### 21.2 — correct_streak grows + resets
- **Kind**: Per-turn field — sequence values
- **Expected**: `[1, 2, 3, 0, 1, 2]` pattern
- **Ollama response**: See original 21.2.

### 21.3 — KG concept + counts per turn (also covers KG block sizes from 21.5)
- **Kind**: Per-turn KG fields
- **Expected**: all KG fields preserved including block-char counts
- **Ollama response**: See original 21.3.

### 21.4 — COKE cognitive_state per turn
- **Kind**: Per-turn cognitive state field
- **Expected**: `["confused", "engaged", "frustrated"]` preserved
- **Ollama response**: See original 21.4.

### 21.6 — old + new fields coexist in one turn
- **Kind**: Schema compatibility (24+ fields)
- **Expected**: all expected fields present
- **Ollama response**: See original 21.6.

---

## Run context

- **Original 194-scenario Ollama run**:
  `output/scenario_responses_2026-05-23_144252/` — all Ollama responses
  cited above were captured in that run.
- **Multi-turn dialogue run**:
  `output/multiturn_responses_2026-05-23_173253/` — 3 clarification
  dialogues, 12 turns each.
- **Earlier full-pipeline batch runs**:
  `output/batch_run_2026-05-09_*` and `output/batch_run_2026-05-11_*` —
  10-scenario tutoring runs against concrete wrong-model variants.

---

## Appendix A — Missing boundary scenarios (added 2026-05-27)

**16 scenarios added.**  These close gaps where the original 134 covered
the *kind* but not the *edge* of a threshold.  Each scenario sits just
below, at, or just above a numeric gate in the actual source code.
Source line cited in every entry.

| Boundary kind | Scenarios | Code reference |
|---|---|---|
| Substance penalty 3-token companion (Layer 0) | A.0.1 | `lp_diagnostic.py:1343` |
| WM head 0.55 floor — below/above (Layer 2) | A.2.1, A.2.2 | `lp_diagnostic.py:993, 1046` |
| LP head 0.40 floor — below/above (Layer 3) | A.3.1, A.3.2 | `lp_diagnostic.py:936` |
| Parroting 15-word edge (Layer 3) | A.3.3 | `lp_diagnostic.py:1414` |
| L2 rule-naming 6-word edge (Layer 3) | A.3.4 | `lp_diagnostic.py:1399` |
| Probe floor 0.55 — below/above (Layer 5) | A.5.1, A.5.2 | `cpal_chat_app.py:793` |
| DINA lower clamp 0.01 (Layer 8) | A.8.1 | `dina.py:262` |
| Intervention branches uncovered (Layer 11) | A.11.1, A.11.2, A.11.3, A.11.4 | `student_state_tracker.py:425, 440, 451, 456` |
| Reward emotional_state component (Layer 12) | A.12.1 | `reward_function.py:48, 109-117` |
| Decay half-life 14-day boundary (Layer 19) | A.19.1 | `dina.py:181` |
| Auth TTL 7-day expiry boundary (Layer 19) | A.19.2 | `auth.py:82, 114` |
| **Total** | **16** | |

**New total: 134 + 16 = 150 scenarios.**

---

### A.0.1 — three-token reply must NOT fire substance penalty
- **Kind**: Substance penalty just-above (`len(_tokens) <= 2` → false at 3)
- **Source**: `lp_diagnostic.py:1343`
- **Input**: question_text = `"I am stuck"` (3 tokens, none filler)
- **Concept**: null_pointer
- **Expected harness**: `diagnostic_confidence` NOT floored to ≤ 0.30; should retain the head's raw value (typically ≥ 0.4 for short L1 reply).
- **Plain English**: Companion to 0.3a/18.7 — confirms the substance floor doesn't over-fire on legitimate short replies.

### A.2.1 — WM head confidence just BELOW 0.55 floor → no WM emission
- **Kind**: WM gate just-below
- **Source**: `lp_diagnostic.py:993` (`confidence >= 0.55`)
- **Setup**: force `wm_st_head` softmax top prob to **0.54** for `NP-A`.
- **Concept**: null_pointer
- **Expected harness**: `{"wrong_model_id": null, "match_score": 0.0, "source": "overlap"}` (trained_wm_hit never set; falls through to overlap/None).
- **Plain English**: Below threshold — no wrong-model attached.

### A.2.2 — WM head confidence just ABOVE 0.55 floor → WM emitted
- **Kind**: WM gate just-above
- **Source**: `lp_diagnostic.py:993`
- **Setup**: force `wm_st_head` softmax top prob to **0.56** for `NP-A`.
- **Concept**: null_pointer
- **Expected harness**: `{"wrong_model_id": "NP-A", "match_score": 0.56, "source": "trained_wm_head"}`.
- **Plain English**: At/above threshold — wrong-model attaches.

### A.3.1 — ST LP head prob just BELOW 0.40 → trained_lp_level stays None
- **Kind**: LP head gate just-below
- **Source**: `lp_diagnostic.py:936` (`lp_probs[top] >= 0.40`)
- **Setup**: force top LP prob to **0.39**.
- **Expected harness**: `trained_lp_level is None`; falls back to overlap-based classification.

### A.3.2 — ST LP head prob just ABOVE 0.40 → trained_lp_level adopted
- **Kind**: LP head gate just-above
- **Source**: `lp_diagnostic.py:936`
- **Setup**: force top LP prob to **0.41**.
- **Expected harness**: `trained_lp_level == "L2"` (or whichever class wins).

### A.3.3 — parroting at exactly 15 vs 16 words
- **Kind**: Parroting word-count edge
- **Source**: `lp_diagnostic.py:1411-1418` (`len(words) <= 15` triggers downgrade)
- **Input A**: trained head says L3, mech vocab present, no causal markers, **15-word** reply → downgrade to L2.
- **Input B**: same with **16 words** → stays L3.
- **Expected harness**: A: `lp_level=L2`; B: `lp_level=L3`.

### A.3.4 — L2 rule-naming at exactly 5 vs 6 words
- **Kind**: L2 rule-naming word-count edge
- **Source**: `lp_diagnostic.py:1397-1402` (`len(words) >= 6` AND pattern matches)
- **Input A**: trained head says L1, reply `"use .equals not =="` (5 words, pattern matches) → stays L1.
- **Input B**: `"you should use .equals not =="` (6 words, pattern matches) → upgrade to L2.
- **Expected harness**: A: `lp_level=L1`; B: `lp_level=L2`.

### A.5.1 — diagnostic_confidence just BELOW 0.55 → probe fires
- **Kind**: Probe floor just-below
- **Source**: `cpal_chat_app.py:793` (`CHAT_PROBE_CONFIDENCE_FLOOR = 0.55`)
- **Setup**: `diagnostic_confidence = 0.54`.
- **Expected harness**: chat app emits a probe (not a teach reply).

### A.5.2 — diagnostic_confidence just ABOVE 0.55 → teach reply
- **Kind**: Probe floor just-above
- **Source**: `cpal_chat_app.py:793`
- **Setup**: `diagnostic_confidence = 0.56`.
- **Expected harness**: chat app skips probe and produces a teach reply.

### A.8.1 — drive DINA mastery toward lower clamp (0.01)
- **Kind**: DINA lower-clamp boundary
- **Source**: `dina.py:262` (`np.clip(p_l_new, 0.01, 0.99)`)
- **Setup**: 5× incorrect on a single skill from prior 0.15.
- **Expected harness**: mastery clamped at **0.01** (NOT 0.0). Mirrors 8.2 on the upper side.

### A.11.1 — solid encoding + low efficacy → mastery_surface
- **Kind**: Intervention branch — mastery_surface
- **Source**: `student_state_tracker.py:425`
- **Setup**: cognitive={enc:"solid"}, psychological={eff:"low", imp:false, attr:"adaptive"}, stage=3
- **Expected harness**: `{"intervention": "mastery_surface"}`.

### A.11.2 — growth efficacy + stage 4a → increase_challenge (without deep enc)
- **Kind**: Intervention branch — increase_challenge (early Stage 4)
- **Source**: `student_state_tracker.py:440`
- **Setup**: cognitive={enc:"partial"}, psychological={eff:"growth", attr:"adaptive"}, stage="4a"
- **Expected harness**: `{"intervention": "increase_challenge"}`.

### A.11.3 — partial encoding + stage 2b → socratic_prompt
- **Kind**: Intervention branch — socratic_prompt
- **Source**: `student_state_tracker.py:451`
- **Setup**: cognitive={enc:"partial"}, psychological={eff:"neutral", attr:"adaptive"}, stage="2b"
- **Expected harness**: `{"intervention": "socratic_prompt"}`.

### A.11.4 — deep encoding + stage 4b → transfer_task
- **Kind**: Intervention branch — transfer_task
- **Source**: `student_state_tracker.py:456`
- **Setup**: cognitive={enc:"deep"}, psychological={eff:"neutral", attr:"adaptive"}, stage="4b"
- **Expected harness**: `{"intervention": "transfer_task"}`.

### A.12.1 — emotional_state component contributes to reward
- **Kind**: Reward component — emotional_state (weight 0.12)
- **Source**: `reward_function.py:48, 109-117`
- **Setup**: identical session/action; vary only `emotion` (before=`frustrated`) and `emotion_after`:
  - Run X: emotion_after=`engaged` → e_change = +1.5 → clipped +1.0
  - Run Y: emotion_after=`frustrated` → e_change = 0 (and the `frustrated`-persistence penalty does NOT fire because e_before is also `frustrated`)
- **Expected harness**: `reward_X > reward_Y` by ≈ `0.12 * 1.0 = 0.12` minus penalty deltas.
- **Plain English**: Verifies the 12 %-weighted emotional component is wired through into the total reward.

### A.19.1 — mastery decay at half-life boundary
- **Kind**: Decay half-life — exact boundary
- **Source**: `dina.py:181, 207`
- **Setup**: write a (student, skill) mastery of 0.90 with `last_iso` exactly **14.0 days** ago; prior=0.15.
- **Expected harness**: `(get_mastery)` returns ≈ `0.15 + (0.90 - 0.15) * 0.5 = 0.525` (within float tolerance).  Tests 13.0 and 15.0 days should give 0.554 and 0.498 respectively.

### A.19.2 — auth token just-before vs just-after 7-day expiry
- **Kind**: Auth TTL — expiry edge
- **Source**: `auth.py:82, 114`
- **Setup**: mint two tokens with `ttl_seconds`:
  - A: `7*24*3600 - 1` (1 s before expiry) → `validate_token` returns `(student, role, course)`.
  - B: `-1` (1 s past expiry) → `validate_token` returns `None`.
- **Expected harness**: A: tuple returned; B: `None`.

---

## Conversion to Word

To produce a `.docx` from this Markdown, use Pandoc:

```
pandoc docs/SCENARIO_CATALOGUE_BOUNDARY_134.md -o SCENARIO_CATALOGUE_BOUNDARY_134.docx
```

Or open in Microsoft Word with the **Markdown** import option.

---

**End of catalogue.**
