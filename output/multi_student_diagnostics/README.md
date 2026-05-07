# Multi-Student LPDiagnostic Outputs

Five distinct student inputs run through CPAL Stage 1 (`src/orchestrator/lp_diagnostic.py`), each producing a faithful `LPDiagnostic` object grounded in `data/mental_models/wrong_models_catalogue.json`. The set was chosen to exercise different concepts, different wrong-model branches within those concepts, and different LP levels — including the plateau gate and a successful within-session L2→L3 progression.

## The five outputs

| # | Student | Concept | Wrong Model | LP Level | What it demonstrates |
|---|---|---|---|---|---|
| 01 | Priya | `type_mismatch` | TM-B (Python carry-over) | L1 | Most common CS1 wrong model — explicit Python reference in the message; near-verbatim catalogue signal match |
| 02 | Marcus | `string_equality` | SE-A (== compares content) | L2 | Knows the rule, can't explain mechanism; verbatim hedge ("something about how strings are stored?") matches the L2 rubric example exactly |
| 03 | Sneha | `static_vs_instance` | SVI-A (same-class-same-access) | L1 | All three documented SVI-A signals present; cleanest wrong-model match in the set |
| 04 | Daniel | `integer_division` | ID-C (cast-as-output) | L2 | **PLATEAU FLAG TRIGGERED** — second consecutive L2 session; methodology forces `trace_scaffold` over RL agent's preferred action |
| 05 | Aisha | `foreach_no_modify` | FNM-B (loop var as reference) | L2 → L3 | **Successful within-session progression** — round 1 at L2, round 2 reaches L3 with delta_lp=+1; both rounds documented |

## What "grounded in the codebase" means here

Every field in every output was derived by:

1. Reading the actual concept entry from `data/mental_models/wrong_models_catalogue.json`
2. Matching the student's message against that concept's `wrong_models[*].conversation_signals` array
3. Classifying LP level using the literal text of `lp_rubric.L1` through `lp_rubric.L4`
4. Following the schema of the `LPDiagnostic` dataclass (and the `WrongModelMatch` and field semantics) defined in `src/orchestrator/lp_diagnostic.py`
5. Applying the plateau rule (`L2_PLATEAU_THRESHOLD = 2`, `PLATEAU_INTERVENTION = "trace_scaffold"`) where applicable

Rubric texts inside each output are quoted verbatim from the catalogue so the documents stay in sync with the codebase.

## Coverage summary

- **Concepts**: 5 different (type_mismatch, string_equality, static_vs_instance, integer_division, foreach_no_modify) out of the catalogue's 20
- **LP levels**: L1 (×2), L2 (×2), L2→L3 progression (×1)
- **Plateau gate**: triggered (×1, in #04)
- **Source classifier paths**: trained_wm_head (all 5)
- **Pre-Python carry-over wrong models**: TM-B, SE-A (Python influence)
- **Pre-Python wrong models**: SVI-A (same-class-same-scope), ID-C (cast misplacement), FNM-B (reference-vs-value confusion)

## Codebase change accompanying these outputs

`src/models/nestor/nestor_bayesian_profiler.py` was modified to remove emotion-related inputs and logic:
- `emotional_variability` removed from `infer_personality()` and `infer_from_behavior()`
- `emotional_state` removed from `InterventionRecommender.recommend()` context
- Neuroticism formula re-derived from the remaining signals (persistence + organization)
- Emotion reading is now handled exclusively by the dedicated `emotion_classifier.pt` component (component #4 in `scripts/demo_full_stack.py`); Nestor focuses on BFI personality + Felder-Silverman learning styles + LISTK strategies only

See the explanatory notes embedded in `nestor_bayesian_profiler.py` (around lines 138, 495, 572) and the entry in `../CLEANUP_NOTES.md`.
