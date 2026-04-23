# Archive

Nothing in this folder is on the live pipeline's import path. All 204 files
here were moved from the repo root on 2026-04-22 to declutter. Moves only —
no deletions. Restore any file by moving it back to the original location
(see column 2 below).

## Contents

| Folder | Original location | Count | What it is |
|---|---|---|---|
| `docs/` | repo root | 103 | historical documentation (COMPLETE_*, FINAL_*, HONEST_*, OUTPUT_*, etc.) — superseded by README.md / QUICK_START.md / SETUP.md which stay at root |
| `examples/` | repo root | 10 | `example_*.py` — pre-integration demos; replaced by `scripts/demo_full_stack*.py` |
| `generate/` | repo root | 7 | `generate_*.py` — one-off dataset/sample generators |
| `chat/` | repo root | 5 | three overlapping chat UIs (`chat_interface.py`, `chat_interface_simple.py`, `chat_ui_local.py`) + their READMEs |
| `batch_scripts/` | repo root | 8 | `regenerate_*.py`, `run_*tests*.py` — one-off batch runners |
| `build_scripts/` | repo root | 14 | `build_*_kg.py`, `analyze_cse_kg_*.py`, `extract_cse_kg_*.py`, `show_graph_structure.py`, `visualize_cse_kg.py`, `check_dataset_sizes.py`, `expand_assistments.py`, `verify_large_datasets.py` |
| `download/` | repo root | 17 | `download_*.py`, `restore_original_datasets.py` — dataset fetchers |
| `tests/` | repo root | 13 | `test_all_*`, `test_cse_*`, `test_sparql_*`, `evaluate_responses.py`, `validate_*` — tests that predate our integration |
| `train_legacy/` | repo root | 2 | `train.py`, `train_and_use_real_data.py` — superseded by `scripts/train_*.py` |
| `misc/` | repo root | 13 | `COMPLETE_METRICS_IMPLEMENTATION.py`, `FINAL_INTEGRATED_SYSTEM.py`, `FINAL_SYSTEM_WITH_BKT.py`, `ENHANCED_SYSTEM_WITH_IMPROVEMENTS.py`, `complete_system_with_nestor.py`, `process_*.py`, etc. |
| `shell/` | repo root | 3 | `clean_secrets.sh`, `remove_secrets.sh`, `remove_all_secrets.sh` — three scripts for the same thing |
| `notebooks/` | repo root | 2 | `Hello_World.ipynb`, `Untitled213.ipynb` — empty/junk notebooks |
| `outputs/` | repo root | 6 | `complete_journey_20251109_*.md`, `followup_output_*.md`, `output_*.md`, `student_*.md` — generated artefacts, not code |
| `scripts_legacy/` | `scripts/legacy/` | 17+ | old dataset download attempts (`download_assistments_*`, ~12 `download_mooccubex_*` variants) |

## What stayed live at repo root

**Code & data actually driving the pipeline**:
- `src/` — all production modules (unchanged)
- `scripts/` — training + demo scripts we authored (`train_*.py`, `demo_full_stack*.py`, `run_end_to_end.py`, `test_streaming.py`, `smoke_test_trained.py`, `test_lp_across_mastery.py`, `test_prompt_to_personality.py`, `compare_models_end_to_end.py`)
- `checkpoints/` — trained model weights
- `data/` — training datasets + KG JSONs + student states
- `api/` — server entry point
- `config.yaml`, `config_smoke.yaml`, `requirements.txt`

**Top-level docs kept**:
- `README.md`, `QUICK_START.md`, `INSTALLATION.md`, `SETUP.md`, `DATASETS.md`

## Verification after moving

`scripts/smoke_test_trained.py` passed cleanly — all four trained components
(HMM, Nestor v2, Emotion MLP, RL) load and forward without referring to any
archived file.
