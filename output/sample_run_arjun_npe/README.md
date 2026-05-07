# Sample Run — Arjun's NullPointerException Journey

This folder contains a complete sample run of one student through the system, from raw input to final mastery. It demonstrates the type of output the system produces; these specific files were generated as faithful samples since `output/`, `test_output/`, and `feature_test_results_2/` (the historical generated outputs) were cleaned out during repository organization.

## What the system actually generates at runtime

The live pipeline (`scripts/demo_full_stack.py`, `scripts/cpal_demo_endtoend.py`, `api/server.py`) produces outputs of these same types when the trained checkpoints are loaded and the LLM (Ollama `qwen2.5-coder:7b`) is running.

## Files in this sample run

| # | File | What it shows |
|---|---|---|
| 01 | `01_raw_student_input.json` | The unprocessed student question, code, error, and behavioral signals — exactly what enters the system |
| 02 | `02_pipeline_diagnosis.json` | All 9 trained components firing on that input — personality inference, Nestor learning style, Behavioral HMM, emotion classifier, HVSAE+RNN, BKT mastery update, LP Index, RL teaching agent, and orchestrator decision |
| 02b | `02b_lp_diagnostic_wrong_model_and_lp_level.json` | **CPAL Stage 1 LPDiagnostic output** — matches Arjun's text against the `null_pointer` wrong-model catalogue (NP-A/NP-B/NP-C), classifies him at L1 on the L1–L4 progression rubric, and sets the L1→L2 transition target. Schema and matching logic grounded in `src/orchestrator/lp_diagnostic.py` and `data/mental_models/wrong_models_catalogue.json`. |
| 03 | `03_response_session1_introduction.md` | Session 1 — INTRODUCTION stage; max scaffolding (5/5); visual analogy + Socratic prediction question |
| 04 | `04_response_session2_guided_practice.md` | Session 2 — GUIDED PRACTICE; scaffolding 3/5; partial template + reasoning required |
| 05 | `05_response_session3_independent_practice.md` | Session 3 — INDEPENDENT PRACTICE; scaffolding 1/5; transfer problem from KG |
| 06 | `06_response_session4_mastery_and_final_state.md` | Session 4 — MASTERY CHECK; scaffolding 0/5; final mastery snapshot, mastery curve, RL feedback loop |

## The student's learning level over time

| Session | Date | Stage | Scaffolding | `null_pointer` mastery |
|---|---|---|---|---|
| 1 | Day 0 | Introduction | 5/5 | 0.14 → 0.46 |
| 2 | Day 1 | Guided Practice | 3/5 | 0.46 → 0.74 |
| 3 | Day 3 | Independent Practice | 1/5 | 0.74 → 0.91 |
| 4 | Day 7 | Mastery Check | 0/5 | 0.91 → **0.97 ✓ MASTERED** |

## To regenerate this with real LLM output

From the repo root, with checkpoints loaded and Ollama running:

```bash
python scripts/demo_full_stack.py     # full pipeline trace + LLM response
python scripts/cpal_demo_endtoend.py  # multi-session journey demo
python scripts/cpal_chat_app.py       # interactive chat
```

These will write similar JSON+MD artefacts. The schemas used in this sample folder match the formats those scripts produce (`student_states.json` structure, BKT update format, RL teaching agent state/action schema).
