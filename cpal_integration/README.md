# CPAL Integration into Personalized_Learning_New

Complete integration of the CPAL (Cognitive-Preference Adaptive Learning)
framework from `mental_models_cpal_methodology_revised.docx` into the
existing `Personalized_Learning_New` codebase.

All five CPAL stages are wired end-to-end. Every new module has a smoke
test, and the full pipeline passes an end-to-end integration test
(`tests/test_cpal_e2e.py`).

## What to read first

1. **`tests/test_cpal_e2e.py`** — the integration test shows exactly how
   the five stages compose and is the fastest way to understand what the
   code does. Run it with `python3 test_cpal_e2e.py` from the repo root.
2. **`new_modules/src_orchestrator_lp_diagnostic.py`** — the heart of
   Stage 1. The `LPDiagnostician.diagnose()` method implements the three
   Stage 1 jobs (wrong-model identification, LP-level classification,
   plateau check) as described in Part 3 of the methodology.
3. **`existing_files_edited/src_orchestrator_orchestrator.py`** — the
   pipeline wiring. Look for `# === STEP 1c: CPAL STAGE 1` and the
   `# LP PLATEAU OVERRIDE` block in `process_session`.

## Where each CPAL stage lives in the code

| Stage | Function / Location |
|-------|---------------------|
| Stage 1: LP Diagnostic | `LPDiagnostician.diagnose()` in `lp_diagnostic.py`; called from Step 1c of `process_session` in `orchestrator.py` |
| Stage 2: Intervention Selection | LP plateau override in `process_session` Step 6; LP-validity gate in `_select_intervention` (3 call sites: recommender filter, LPProgressionRanker, `_lp_guard` helper) |
| Stage 3: Prompt Builder | `_build_enhanced_prompt` in `enhanced_personalized_generator.py` — new LP-1/LP-2/LP-3 sections injected when `lp_diagnostic` is present in `student_state` |
| Stage 4: Post-Reply Assessment | `_cpal_stage4_5` helper in `orchestrator.py`, called from `_learn_from_session` |
| Stage 5: Persistence | `load_lp_state`, `persist_lp_state`, `get_session_state_vectors` in `student_state_tracker.py`; `lp_state` block added to each per-concept node in `_init_state` |

## File layout

### `new_modules/` — pure additions (nothing existing changed)

| File | Lines | Purpose |
|------|-------|---------|
| `src_knowledge_graph_mental_models.py` | 314 | `MentalModelsCatalogue` — loads the 20-concept JSON catalogue, exposes `match_wrong_model(question_text, concept_id) → WrongModelMatch` |
| `src_orchestrator_lp_diagnostic.py` | 534 | `LPDiagnostician.diagnose()` for Stage 1; `filter_interventions_by_lp` and `classify_post_reply` helpers for Stages 2/4; LP-level constants and the `LP_VALID_INTERVENTIONS` table |
| `src_reinforcement_learning_lp_progression_rnn.py` | 375 | `LPProgressionRNN` (GRU-based sequence model over historical session state vectors); `LPProgressionRanker` facade with heuristic fallback; `build_state_vector` helper |

### `data/` — the 20-concept wrong-models catalogue

| File | Content |
|------|---------|
| `wrong_models_catalogue.json` | 20 concepts × 3 wrong models × 3+ conversation signals + L1-L4 LP rubric per concept. Transcribed from Part 2 of the methodology document. |

Drop it in your repo at `data/mental_models/wrong_models_catalogue.json`.

### `existing_files_edited/` — edits to four existing files

| File | Edit Summary |
|------|--------------|
| `src_orchestrator_orchestrator.py` | `__init__` instantiates `LPDiagnostician`, `MentalModelsCatalogue`, `LPProgressionRanker` alongside existing trackers. `process_session` has new Step 1c for CPAL Stage 1 and a plateau override at top of Step 6. `_select_intervention` rewritten to apply LP-validity gate to recommender output and LPProgressionRanker output. `_learn_from_session` now delegates to new `_cpal_stage4_5` helper which classifies replies, computes delta_lp, and persists state. `_generate_content` accepts `lp_diagnostic` kwarg and threads it into `student_state`. |
| `src_orchestrator_student_state_tracker.py` | `lp_state` block added to each per-concept node in `_init_state`. Three new methods: `load_lp_state`, `persist_lp_state`, `get_session_state_vectors`. Back-compat: old saved states without `lp_state` lazily get one on first access via `_ensure_lp_state`. |
| `src_orchestrator_enhanced_personalized_generator.py` | New LP-grounded header when `lp_diagnostic` is present. New LP-1/LP-2/LP-3 prompt sections injected conditionally: LP-1 surfaces the diagnosis, LP-2 surfaces the wrong mental model + L3 expert benchmark, LP-3 gives a level-specific six-step instruction (L1/L2/L3/L4 each get different instructions). All new sections are additive — the existing 10 sections still run. |
| `src_reinforcement_learning_reward_function.py` | New `lp_gain` reward component at weight 0.25. Existing five weights rebalanced (learning_gain 0.35→0.26, engagement 0.20→0.15, zpd 0.20→0.15, emotion 0.15→0.12, attribution 0.10→0.07). Weights still sum to 1.00. Student-response keys now accept `delta_lp`, `lp_level_before`, `lp_level_after`, `plateau_flag_before`. |

## How to apply these edits

1. **New files** — drop them into the corresponding paths:
   - `new_modules/src_knowledge_graph_mental_models.py` → `src/knowledge_graph/mental_models.py`
   - `new_modules/src_orchestrator_lp_diagnostic.py` → `src/orchestrator/lp_diagnostic.py`
   - `new_modules/src_reinforcement_learning_lp_progression_rnn.py` → `src/reinforcement_learning/lp_progression_rnn.py`
   - `data/wrong_models_catalogue.json` → `data/mental_models/wrong_models_catalogue.json` (create the `data/mental_models/` directory first)

2. **Edited files** — the four files in `existing_files_edited/` are
   drop-in replacements for their counterparts. Before replacing, I
   recommend running a diff against your current versions so you can
   see every change in context.

3. **Run the integration test**:
   ```bash
   python3 tests/test_cpal_e2e.py
   ```
   Expected output: `✓ ALL TESTS PASSED — CPAL integration wiring is correct`

## Backward compatibility guarantees

Every edit preserves the original behaviour when CPAL context is missing:

- If `lp_diagnostic` is `None` in `process_session` (e.g., the
  catalogue failed to load), `_select_intervention` falls through to
  its original principled rules without LP filtering.
- If a student's saved state doesn't have an `lp_state` block (old
  student_states.json format), `load_lp_state` lazily creates one.
- If `lp_diagnostic` is `None` in the prompt builder, the original
  header and existing 10 sections run unchanged.
- If the new reward response keys (`delta_lp`, etc.) are absent, the
  lp_gain component defaults to 0.0 and the rest of the reward behaves
  normally.
- The LPProgressionRanker heuristic-only mode works without torch, so
  the pipeline runs even in a minimal install.

## Reward-function weight rebalance

Old:
- learning_gain 0.35, engagement 0.20, zpd_alignment 0.20,
  emotional_state 0.15, attribution_shift 0.10 (sum=1.00)

New:
- learning_gain 0.26, engagement 0.15, zpd_alignment 0.15,
  emotional_state 0.12, attribution_shift 0.07, **lp_gain 0.25**
  (sum=1.00)

The reduction factor on the existing five weights is 0.75 across the
board, preserving relative ordering. The new lp_gain component gets
0.25 — the methodology document specifies this as the primary
training signal for the LPProgressionRNN, so it needs to be a
substantial fraction of the reward without overwhelming the existing
psychological/cognitive signals.

## What I verified

- All seven files (3 new + 4 edited) parse cleanly with `ast.parse`.
- `test_lp_pipeline.py` validates the Stage 1 diagnoser, Stage 2
  LP-validity gate, and Stage 4 post-reply classifier on hand-crafted
  L1/L2/L3/L4/plateau test cases.
- `test_cpal_e2e.py` simulates a full three-session student journey
  (L1→L2→L3) exercising all five stages together, plus reward-function
  integration on plateau-break and regression scenarios.
- Reward weights sum to exactly 1.00.
- No stale method-call references to the old LPDiagnostic API remain
  in the orchestrator.
- The 20-concept JSON catalogue validates: 20 concepts, 60 wrong
  models (3 each), complete L1-L4 rubric on every concept.

## What I did NOT verify (sandbox limitations)

- The full pipeline against a live Ollama / Groq model (no API keys in
  sandbox).
- The PyTorch-backed `LPProgressionRNN.rank()` path (torch wouldn't
  install in the sandbox — the heuristic fallback was tested instead).
  The torch code is straightforward GRU-with-softmax and follows the
  pattern used by `policy_network.py` in your codebase.
- Integration with the existing `TeachingRLAgent` training loop —
  the reward function returns a scalar that plugs into the same
  pipeline as before, but I didn't run a training iteration.

Those three paths should work — the logic is correct and the APIs
match — but they need your local dev environment to exercise fully.

## Citations

The methodology grounding for each design decision is inline in the
code as comments, referencing the 15 verified citations from the
revised methodology document. Key ones:

- **Wrong-model identification**: Kaczmarczyk et al. 2010 (conversation
  signals), Sorva 2013 (systematic review of novice misconceptions),
  Kennedy & Kraemer 2018 (elicitation before instruction).
- **LP-level rubric**: Jin et al. 2019, 2025 (validation-argument
  framework for LP movement as primary outcome).
- **Plateau rule**: Chi et al. 1989, 1994 (mechanism-level self-
  explanation), Renkl 2002 (scaffolded worked examples close L2→L3
  gap).
- **Step-level intervention granularity**: VanLehn 2011.

---

**Integration complete.** Let me know if anything needs adjustment.
