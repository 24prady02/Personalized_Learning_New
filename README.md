# CPAL — LP-grounded Java Tutor

CPAL is a Java tutor for Chapter 1 of *Introduction to Programming in Java*
(Sedgewick & Wayne §1.1–1.6). It doesn't just check whether a student's answer
is right. It reads **how deeply they understand the code**, places that on a
five-level **Learning Progression (LP)**, catches the **specific wrong belief**
behind a mistake, and picks a teaching move that fits that level.

Everything hangs off one graph: the **Chapter-1 concept + LP graph**
(`data/chapter1_concept_graph_percpt_lp.json`).

---

## Current status

| Part | Status |
|---|---|
| Chapter-1 concept + LP graph (loads, 70 concepts, 350 LP nodes, 0 broken edges) | ✅ works |
| Per-student knowledge graph (one node per Chapter-1 concept; LP level, mastery, misconceptions; saved to SQLite) | ✅ works (`scripts/smoke_test_student_graph.py`) |
| LP classifier, misconception matcher, LP-gated intervention filter | ✅ code works; best accuracy needs the trained heads in `checkpoints/` |
| Prompt builder (LP header + Chapter-1 context + intervention) | ✅ works |
| API concept endpoints (`/api/concept/{id}`, `/api/query/concepts`) | ✅ work |
| Gradio chat app (`scripts/cpal_chat_app.py`) | ❌ won't start: `configs/config.yaml` missing |
| API server full pipeline (`api/server.py`) | ❌ startup fails: `config.yaml` missing |
| Student quiz app (`api/student_app.py`) | ❌ `data/quiz_bank.json` missing |
| Trained models (`checkpoints/`), datasets (`data/…`) | ❌ not in this copy |
| LLM replies | ❌ need Ollama running locally (`ollama serve`) |
| `cpal_integration/tests/test_cpal_e2e.py` | ❌ fails (expects L4, gets L2) without the catalogue + trained heads |

To bring the full app up, restore `checkpoints/`, `configs/config.yaml`,
`data/mental_models/`, `data/dina/`, `data/quiz_bank.json` from the original
project, then run `python scripts/setup_java_knowledge.py` and start Ollama.

---

## The complete process — what happens on one student turn

The student sees a Java snippet with a multiple-choice question, picks an
answer, and writes **why**. That answer runs through these steps, in order:

```
 student answer + reasoning
        │
  ①  Diagnose LP level ............ how deep is the understanding?  (L0–L4)
  ②  Match misconception .......... which wrong belief, if any?
  ③  Update mastery ............... DINA / BKT probability of mastery
  ④  Probe or teach? .............. ask a sharper question, or teach now
  ⑤  Pick the teaching move ....... LP gate + RL agent
  ⑥  Build the prompt ............. LP + misconception + Chapter-1 context
  ⑦  Stream the tutor reply ....... Ollama LLM
  ⑧  Record the turn .............. student knowledge graph → SQLite
  ⑨  Learn from the turn .......... post-reply LP check, RL reward, state save
```

| Step | What it does | Where it happens |
|---|---|---|
| ① LP diagnosis | Classifies the reasoning into **L0 Prestructural → L1 Surface → L2 Rule/Tracing → L3 Mechanism → L4 Transfer**. Uses the trained LP head (sentence-transformer / HVSAE) when present, plus heuristic corrections (substance penalty, mechanism-vocab bump, parroting downgrade, transfer upgrade). Outputs a level, a distribution and a confidence. | `src/orchestrator/lp_diagnostic.py` → `LPDiagnostician.diagnose()` |
| ② Misconception | Matches the answer against the wrong-model catalogue for the concept; the best match above threshold becomes `wrong_model_id`. Reaching L3+ marks earlier wrong models as refuted. | `src/knowledge_graph/mental_models.py` → `match_wrong_model()`; `src/orchestrator/catalogue_rag.py` |
| ③ Mastery | DINA (slip/guess) and BKT update the probability the student has mastered the concept. | `src/models/dina.py`, `src/student_modeling/bayesian_knowledge_tracing.py`; chat app `_update_mastery()` |
| ④ Probe or teach | If confidence is low, asks a depth probe (jargon trap / sub-criterion) before teaching; handles several concepts in one answer. | `scripts/cpal_chat_app.py` → `_decide_probe_or_teach()`, `src/orchestrator/depth_probe.py`, `rubric_grader.py` |
| ⑤ Teaching move | Candidate interventions are filtered to the ones valid at the student's LP level (`filter_interventions_by_lp`); the trained RL agent (DQN) re-ranks them; a plateau at L2 forces a mechanism-building move. | `lp_diagnostic.py`, `src/reinforcement_learning/teaching_agent.py`, `src/orchestrator/orchestrator.py` → `_select_intervention()` |
| ⑥ Prompt | Assembles the LP header (current → target level), the wrong-model refutation, a level-specific teaching shape, and the **Chapter-1 graph block**: the concept's prerequisites, what it leads to, catalogued misconceptions, and what the current/target LP level looks like for this exact concept. | `src/orchestrator/enhanced_personalized_generator.py` → `_build_enhanced_prompt()`, `_chapter1_graph_block()` |
| ⑦ Reply | Streams the reply from a local Ollama model; a guardrail strips misquotes of the student. | `EnhancedPersonalizedGenerator.generate_personalized_response()` |
| ⑧ Record | Writes the turn onto the student's graph node (LP level, LP history, confidence, mastery + delta, wrong models, cognitive + progression state, intervention, reward) and adds the concept's Chapter-1 neighbours. Saved to `data/cpal.db`. | `src/knowledge_graph/student_graph_service.py` → `record_turn()`, `student_knowledge_graph.py` |
| ⑨ Learn | Re-classifies the next reply to get Δ-LP, computes the reward (learning gain .32, LP gain .32, engagement .18, ZPD fit .18), pushes an RL experience, and persists LP state. | `orchestrator.py` → `_cpal_stage4_5()`, `src/reinforcement_learning/reward_function.py`, `src/orchestrator/student_state_tracker.py` |

Alongside the LP, `student_state_tracker.py` keeps a **two-channel state** per
student: cognitive (encoding strength, dual coding, elaboration) and progression
(stage, ZPD, scaffold level).

**Inputs the system uses:** the student's answer and reasoning, the LP level,
the matched misconception, mastery (DINA), encoding strength, stage/ZPD,
debugging-action patterns (HMM/RNN strategy) and Nestor personality/learning
style. **Emotion and psychological state are not inputs** (see *Retired
components*).

---

## The Chapter-1 concept + LP graph

`data/chapter1_concept_graph_percpt_lp.json` (v1.1 + LP + ProgMiscon), loaded by
`src/knowledge_graph/chapter1_graph.py`.

| Layer | Contents | Count |
|---|---|---|
| 1 Chapter | Program structure, Types & expressions, Conditionals, Loops, Arrays, Input & output, Random web surfer | 7 |
| 2 Concept | e.g. `program_structure.println`, `arrays.array_bounds` | 70 |
| 3 Misconception | e.g. `PrintEqualsPrintln` — "println and print do the same thing" (ProgMiscon + CS1 additions) | 90 |
| 4 LP level | one L0–L4 ladder per concept, e.g. `program_structure.println@L2` | 350 |

Edges: `prerequisite` (A before B), `parallel` (sibling constructs),
`misconception` (concept → wrong belief), `chapter`, `lp_indicator` (concept →
its level, with a per-concept description of that level), `next_level`
(Lk → Lk+1).

The LP levels follow Jin et al.'s construct map; each per-concept level
description is derived with the Block Model (Izu et al.). The ordering is
marked *hypothesized until confirmed against student data*.

```python
from src.knowledge_graph.chapter1_graph import get_chapter1_graph
g = get_chapter1_graph()
g.canonical("println")                        # 'program_structure.println'
g.get_prerequisites("println")                # ['program_structure.statement', 'program_structure.string_literal']
g.misconceptions_for("println")               # [{'id': 'PrintEqualsPrintln', 'wrong_belief': ...}, ...]
g.lp_descriptor("println", "L2")              # what L2 looks like for println
```

Older CPAL concept ids (`string_equality`, `array_index`, …) are mapped to
Chapter-1 ids in `CPAL_TO_CHAPTER1`. Concepts outside Chapter 1
(`null_pointer`, `overloading`, …) stay as standalone nodes.

---

## Where things live

```
src/
  knowledge_graph/
    chapter1_graph.py            Chapter-1 concept + LP graph loader
    student_knowledge_graph.py   per-student graph (nodes = Chapter-1 concepts)
    student_graph_service.py     record_turn() + SQLite load/save
    mental_models.py             wrong-model (misconception) catalogue
    lp_index.py                  optional LP path lookup (data/java_curriculum/)
  orchestrator/
    lp_diagnostic.py             ① LP classifier, LP gate, post-reply check
    catalogue_rag.py             ② misconception retrieval
    depth_probe.py, rubric_grader.py, concept_resolver.py   ④ probing
    orchestrator.py              full pipeline (process_session)
    enhanced_personalized_generator.py   ⑥–⑦ prompt + Ollama reply
    student_state_tracker.py     cognitive + progression state, LP persistence
  models/                        HVSAE encoder, DINA, behavioral HMM/RNN, Nestor profiler
  reinforcement_learning/        DQN teaching agent, reward function, LP progression RNN
  student_modeling/              Bayesian knowledge tracing
  persistence/                   SQLite store (data/cpal.db), auth, A/B testing
  teaching/                      4-stage teaching engine
  system_registry.py             loads every component once for the apps
api/
  server.py                      FastAPI (port 8000): session, feedback, concept endpoints
  student_app.py                 FastAPI (port 8001): MCQ → belief → correction flow
scripts/
  cpal_chat_app.py               main Gradio chat app (port 7860)
  smoke_test_student_graph.py    student-graph smoke test
  setup_java_knowledge.py        writes data/java_curriculum/ (LP paths, rubric)
  cpal_train_*.py                train the LP / wrong-model heads
  run_*_scenarios*.py            scenario test suites
cpal_integration/                CPAL methodology integration notes, catalogues, tests
data/                            chapter1 graph, cpal.db, (restore: mental_models/, dina/, quiz_bank.json)
docs/                            reports, paper, wireframe + screenshots
_archive/knowledge_graph_models/ retired CSE-KG, Pedagogical KG and COKE code
```

---

## Running it

```bash
pip install -r requirements.txt
python scripts/setup_java_knowledge.py        # writes data/java_curriculum/
ollama serve                                  # local LLM; picks the best installed model,
                                              # override with CPAL_OLLAMA_MODEL=llama3.1:8b

python scripts/cpal_chat_app.py               # chat app  → http://localhost:7860
python api/server.py                          # API       → http://localhost:8000/docs
uvicorn api.student_app:app --port 8001       # quiz app  → http://localhost:8001
```

All three need the restored config/data/checkpoints listed under *Current status*.

Quick checks that run on this copy as-is:

```bash
python -m src.knowledge_graph.chapter1_graph       # graph loads + sample lookups
python scripts/smoke_test_student_graph.py         # builds a student graph → output/maya_student_graph.json
```

---

## Retired components

The **CSE-KG** (CSO / SPARQL computer-science graph), **Pedagogical KG** and
**COKE** cognitive graph — plus GIKT and the explanation generators built on
them — were removed from the live code on 2026-09-28. They needed training
data that isn't part of this project, and the Chapter-1 graph now covers
their role (concept prerequisites and misconceptions). The code is kept in
`_archive/knowledge_graph_models/` if it's ever needed again.

**Emotion and the psychological channel** were removed as inputs on
2026-09-28 because they can't be read reliably from what the system sees. This
covers the emotion classifier, frustrated/confused/engaged labels, and the
anxiety, flow, attribution, self-efficacy, imposter and SRL-phase signals.
Nothing detects or uses them:
- the teaching-move rules no longer have psychological gates, and the
  `attribution_reframe` / `mastery_surface` interventions no longer exist;
- the prompt no longer has emotional-tone or psychological-state sections;
- rewards no longer have emotion or attribution terms (chat app:
  `0.375·learning gain + 0.25·engagement + 0.375·LP gain`);
- the RL state and LP-ranker vectors keep their old size so trained
  checkpoints still load, but the former emotion slots are always zero, and
  the behavioural RNN's emotion layer is kept only for checkpoint shape.

The emotion-classifier training script is in `_archive/emotion_and_psych/`.

## License

MIT
