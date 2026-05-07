# Cleanup & Reorganization Notes

This repository was cleaned up and restructured on 2026-05-06. This file documents what changed so the history is auditable.

## Codebase changes

### 2026-05-06: Removed emotion reading from Nestor

`src/models/nestor/nestor_bayesian_profiler.py` was modified to detach emotion reading from the personality/learning-style profiler:

| Method | Change |
|---|---|
| `NestorBayesianProfiler.infer_personality()` | Removed `emotional_variability` parameter from `behavioral_data`. Re-derived neuroticism from `(1 - persistence)` and `(1 - organization)` instead of `emotional_variability * 0.8`. Re-derived agreeableness from `social_interaction` + `organization` instead of using `(1 - emotional_variability)`. |
| `NestorBayesianProfiler.infer_from_behavior()` | Same parameter removal and same neuroticism/agreeableness re-derivation. |
| `InterventionRecommender.recommend()` | Removed the `emotional_state` context key and the `emotion in ('frustrated', 'anxious')` boost block (formerly +0.20 to `reduce_challenge`/`attribution_reframe`, –0.25 to `transfer_task`/`increase_challenge`). |

**Rationale**: Emotion reading is handled by the dedicated `emotion_classifier.pt` (component #4 in `scripts/demo_full_stack.py`). Nestor's job is BFI personality + Felder-Silverman learning styles + LISTK strategies. The orchestrator (`src/orchestrator/orchestrator.py`) is the right place to combine emotion signals with Nestor's personality output, not Nestor itself.

**Verification**: file parses cleanly via `python3 -c "import ast; ast.parse(open(...).read())"`. All remaining mentions of "emotion" in the file are explanatory comments only — no live code paths.

## What was removed

| Removed | Size | Reason |
|---|---|---|
| `pls_fixed/_archive/` | 3.3 MB, 204 files | Already-archived superseded code (see its old README — old demos, legacy `train.py`, dead chat UIs, one-off generators, junk notebooks, duplicate shell scripts). Confirmed off the live import path; smoke test had passed without it. |
| `pls_fixed/_pre_cpal_backup/` | 228 KB | Pre-CPAL backups of `orchestrator.py`, `student_state_tracker.py`, `reward_function.py`, `enhanced_personalized_generator.py`. Current versions live in `src/orchestrator/` and `src/reinforcement_learning/`. |
| `pls_fixed/output/` | 15 MB | Generated artefacts (sample conversation PNGs/JSON/MD). Re-creatable from `scripts/`. |
| `pls_fixed/test_output/` | 48 KB | Test run outputs. |
| `pls_fixed/feature_test_results_2/` | 56 KB | Feature test outputs. |
| `pls_fixed/results/` | (empty) | Empty placeholder. |
| `pls_fixed/cse_kg_*.png` (3 files at root) | 2.7 MB | KG visualizations, regeneratable from `scripts/visualize_*` (archived). |
| All `__pycache__/` and `*.pyc` | — | Python bytecode cache, always regenerated. |
| `.claude/` directories | — | Editor/tooling cache. |

Total reclaimed: ~22 MB. Repo went from 416 MB to 395 MB. The remaining bulk is `checkpoints/` (214 MB of trained weights) and `data/` (164 MB of training datasets) — both required for the system to function.

## What was reorganized

The old layout was double-nested (`pls_complete_final_v2/pls_fixed/...` and `cpal_integration/cpal_integration/...`). The new layout is a single clean root.

| Old path | New path |
|---|---|
| `pls_complete_final_v2/pls_fixed/*` | `./*` (flattened to repo root) |
| `pls_complete_final_v2/cpal_integration/cpal_integration/` | `./cpal_integration/` |
| `pls_fixed/config.yaml`, `config_smoke.yaml`, `cse_kg_graph_structure_example.json` | `./configs/` |
| `pls_fixed/paper/` | `./docs/paper/` |
| `pls_fixed/slides/` | `./docs/slides/` |
| `pls_fixed/DATASETS.md`, `Final_Project_Report.docx` | `./docs/` |

Top-level docs (`README.md`, `QUICK_START.md`, `INSTALLATION.md`, `SETUP.md`) and `requirements.txt` stayed at the root. `.git/`, `.gitignore`, and `.env.example` were preserved.

## What was kept (live pipeline)

- `src/` — all production source
- `api/` — FastAPI server
- `scripts/` — training, demos, dataset prep
- `cpal_integration/` — CPAL integration module
- `configs/` — config files
- `checkpoints/` — trained model weights (do not delete; expensive to retrain)
- `data/` — training datasets (CodeNet Java/Python/C++ samples, ProgSnap2, Nestor, etc.)
- `docs/`, `examples/`, `notebooks/` — documentation and reference materials

## If you need to recover something

The deletions above are gone from this working tree, but the original zip (`Personalized_Learning.zip`) was the source — restore from that if anything turns out to have been needed.
