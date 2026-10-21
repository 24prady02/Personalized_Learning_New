# CPAL — Project Report: Wiring Analysis Components into the Wireframe

_Project: LP-based personalized learning system for Java code comprehension
(CS1, Sedgewick & Wayne §1.1–1.6). This report covers the wiring of selected
analysis components from the codebase into the live wireframe._
_Maintained: rolling. Last update: 2026-06-08._

---

## 1. Abstract

CPAL (Code-comprehension Personalized Adaptive Learning) diagnoses **how deeply**
a CS1 student understands Java code — on a SOLO-for-code Learning Progression
(LP) — rather than only whether an answer is right. For each student turn the
system runs a pipeline of analyses (LP diagnosis, DINA mastery, wrong-model /
misconception matching, CSO-3.5 knowledge-graph tracing, and reinforcement-
learning intervention selection) and adapts its Socratic reply accordingly.

This phase of work **wires a chosen subset of those analysis components**
end-to-end into the running app and surfaces them in a **teacher-facing
wireframe** for Hello World (§1.1). The deliberate choice is to wire the
**diagnostic + graph-forming** analyses (LP, DINA, wrong-model, CSO tracing,
intervention selection) and to leave the heavier experimental signals
(3-channel psychological state, full RL reward shaping) out of the wireframe so
the teacher view stays legible. The wireframe is a high-fidelity **design
blueprint** of this workflow; one true backend hook now feeds the CSO student
graph from the live Gradio app.

---

## 2. Steps (what the wiring does, in order)

1. **Capture the student turn** in the Gradio app (`scripts/cpal_chat_app.py`).
2. **Diagnose LP level** with `LPDiagnostician.diagnose()` → current LP level,
   diagnostic confidence, matched wrong-model.
3. **Update mastery** with `DINAModel` (+ BKT) → scalar mastery per (student, concept).
4. **Match the wrong-model** via `MentalModelsCatalogue.match_wrong_model()`.
5. **Select the intervention**: `filter_interventions_by_lp()` (static LP gate)
   then refine with the trained `TeachingRLAgent.select_action()`.
6. **Couple onto the CSO graph**: `StudentGraphService.record_turn()` writes LP +
   DINA mastery + wrong-model + misconception + selected intervention onto the
   CSO-traced node and expands 1-hop neighbours (`CSOTraversal.get_neighbours()`).
7. **Serve the graph** at `GET /api/student/graph` (`StudentKnowledgeGraph.to_dict()`).
8. **Render in the wireframe** (`docs/wireframe/cpal_wireframe.html`) — Student
   conversation view + Teacher analysis view, both step-driven.

---

## 3. Architecture Diagram

```
                          ┌─────────────────────────────────────────┐
   Student answer  ─────► │  Gradio app · scripts/cpal_chat_app.py    │
   (HelloWorld.java)      │  _stream_teach() per turn                 │
                          └───────────────┬───────────────────────────┘
                                          │
        ┌─────────────────────────────────┼─────────────────────────────────┐
        ▼                 ▼                ▼                ▼                  ▼
 ┌────────────┐   ┌────────────┐   ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
 │ LP diagnose│   │ DINA mastery│  │ wrong-model   │  │ HVSAE latent │  │ RL teaching  │
 │ lp_        │   │ dina.py     │  │ mental_models │  │ hvsae.py     │  │ agent        │
 │ diagnostic │   │ get_mastery │  │ match_wrong_  │  │ encode reply │  │ select_action│
 │ classify_lp│   │             │  │ model()       │  │              │  │ + LP gate    │
 └─────┬──────┘   └─────┬───────┘  └──────┬────────┘  └──────┬───────┘  └──────┬───────┘
       └────────────────┴─────────────────┴──────────────────┴─────────────────┘
                                          │  (LP, mastery, WM, intervention)
                                          ▼
                       ┌──────────────────────────────────────────┐
                       │ StudentGraphService.record_turn()         │
                       │   update_from_diagnosis()  +              │
                       │   expand_neighbours()  (CSOTraversal)     │
                       │   → CSO-3.5 student knowledge graph        │
                       └───────────────────┬───────────────────────┘
                                           │ to_dict()
                                           ▼
                       ┌──────────────────────────────────────────┐
                       │ GET /api/student/graph  (api/student_app) │
                       └───────────────────┬───────────────────────┘
                                           │  (live feed; demo fallback)
                                           ▼
                       ┌──────────────────────────────────────────┐
                       │ Wireframe  docs/wireframe/*.html           │
                       │   Student view (chat) · Teacher view       │
                       │   ① LP ② mastery ③ misconception           │
                       │   ④ knowledge graph ⑤ policy ⑥ reply       │
                       └──────────────────────────────────────────┘
   Publishing: docs/ served on :8765 (start_docs.ps1, CpalDocsServer task)
               → cloudflared → tutor.cpaltutor.com/wireframe
```

---

## 4. Literature Review (brief)

- **SOLO taxonomy** (Biggs & Collis, 1982) — prestructural → unistructural →
  multistructural → relational → extended-abstract; the basis for the L0–L4
  reasoning scale ("SOLO-for-code").
- **Notional machine** (du Boulay, 1986) — the abstract model of program
  execution learners must build; grounds the L3 "mechanism" level (source →
  bytecode → JVM → output).
- **Learning Progressions & validity** (Jin et al.; Williamson, Xi & Breyer,
  2012) — the eight-assumption validity argument and ordinal-agreement metrics.
- **Cognitive diagnosis — DINA** (Junker & Sijtsma, 2001) — slip/guess latent
  skill model behind mastery estimation.
- **Knowledge tracing** — BKT (Corbett & Anderson, 1995), DKT (Piech et al.,
  2015), GIKT (graph-based, Yang et al., 2021) — mastery over response sequences.
- **CS knowledge graph** — CSO 3.5 (Salatino et al., 2020) — the external
  ontology the student graph is grounded in.
- **Programming misconceptions** — ProgMiscon and the wrong-models catalogue —
  concept-keyed beliefs (e.g. PS-A "compile = run").
- **RL for tutoring** — DQN-style policies selecting feedback/next-task from a
  diagnosed state.

---

## 5. Whiteboard (Kanban)

**Completed ✅**
- LP diagnosis (L1–L4) running in the app.
- DINA + BKT mastery update per turn.
- Wrong-model catalogue matching.
- CSO-3.5 student knowledge graph + 1-hop traversal.
- `record_turn()` wiring: live app now feeds the graph (LP + DINA + WM + misconception + intervention).
- Hello World teacher/student wireframe with the full workflow.
- Four student scenarios + per-answer explanations.
- Publishing: persistent docs server + permanent `/wireframe` link.
- Process documentation (`LP_LEARNING_PROGRESSION.md`).

**In progress 🟡**
- Keeping wireframe content aligned with the spec (L0 floor is in the wireframe but not yet in code).
- Per-concept mastery surfaced for teachers.

**To do / backlog ⬜**
- Decide direction: make wireframe honest to code (L1–L4) **or** implement spec (L0 floor, distribution mastery, scoring pipeline, four-action policy module).
- Wire the wireframe to the live `/api/student/graph` (currently static/demo).
- Two-confidence scoring + human-review routing in code.

---

## 6. JIRA (tickets)

| Key | Type | Summary | Status |
|---|---|---|---|
| CPAL-1 | Epic | Wire analysis components into the teacher wireframe | In Progress |
| CPAL-2 | Story | LP diagnosis feeds the graph node | Done |
| CPAL-3 | Story | DINA mastery coupled per turn | Done |
| CPAL-4 | Story | Wrong-model / misconception on the node | Done |
| CPAL-5 | Story | CSO-3.5 tracing (expand_neighbours) | Done |
| CPAL-6 | Story | Intervention selection coupled onto node | Done |
| CPAL-7 | Story | `record_turn()` called from live Gradio app | Done |
| CPAL-8 | Story | Hello World wireframe (Student + Teacher views) | Done |
| CPAL-9 | Story | Four student scenarios | Done |
| CPAL-10 | Story | Per-answer "Chat, explained" | Done |
| CPAL-11 | Task | Persistent docs server + permanent link | Done |
| CPAL-12 | Task | Process documentation | Done |
| CPAL-13 | Story | Connect wireframe to live `/api/student/graph` | To Do |
| CPAL-14 | Story | Implement L0 floor + distribution mastery in code | To Do |
| CPAL-15 | Story | Scoring pipeline + confidence routing in code | To Do |

---

## 7. Daily Updates

**2026-06-07**
- Audited the end-to-end CSO graph chain; found the live Gradio app did not feed the student graph and the intervention was not coupled.
- Added `StudentGraphService.record_turn(...)` to `_stream_teach` in `cpal_chat_app.py`; verified via smoke test that LP + DINA + WM + misconception + intervention couple onto the CSO node with neighbours traced.
- Built the Hello World wireframe; fixed the permanent `/wireframe` link (added `start_docs.ps1`, `index.html`, `CpalDocsServer` scheduled task).

**2026-06-08**
- Split the wireframe into Student (chat) and Teacher (analysis) views.
- Aligned wireframe to spec: L0–L4 scale, distribution mastery + reporting rule, multi-keyed misconception, four-action policy, ontology + prerequisite-DAG graph; removed QWK jargon.
- Added per-concept mastery, per-card blueprints (then paragraph form), on-graph LP/mastery/misconception, four student scenarios, "Chat, explained", and the "needed intervention — how to use it" closing.
- Removed the scoring/confidence card on request and renumbered panels.
- Wrote `LP_LEARNING_PROGRESSION.md` (full process) and this report.
- Committed and pushed to GitHub (`eb68239`).
- Verified the real response-generation path: confirmed `_build_enhanced_prompt()` reads all five components (LP, DINA, wrong-model, CSO/KG, intervention) and assembles them into one prompt (LP writes the wording). Surfaced this "how the reply was assembled" breakdown in the wireframe's ⑥ model-response card and documented it in §9.9.

---

## 8. GitHub Progress

Repo: `github.com/24prady02/Personalized_Learning_New` · branch `main`.

- `8139e3b` — CPAL tutor comparison study, boundary tests, 3-view wireframe
- `5f32345` — wireframe served at tutor.cpaltutor.com/wireframe → Chapter 1
- `e926142` — CSO v3.5-grounded student knowledge graph (central data structure)
- `eb68239` — **Add Hello World LP wireframe, docs server, and live CSO graph wiring** (this phase)

---

## 9. Components & Algorithmic Analysis

### 9.1 LP Diagnostician — `src/orchestrator/lp_diagnostic.py`
- **Role:** classify a student response onto the LP scale (L1–L4) with confidence.
- **Key fns:** `classify_lp_level()` (L298), `classify_post_reply()`, `LPDiagnostician.diagnose()` (L558), `filter_interventions_by_lp()` (L1714).
- **Algorithm:** rubric/feature signals + an HVSAE latent matcher (`HVSAEMatcher`,
  L433) score the text against per-level descriptors; a post-reply pass adjusts
  `delta_lp`. Heuristic post-corrections (substance penalty, mech-vocab bump,
  parroting downgrade, transfer upgrade) refine the level. Output: `current_lp_level`,
  `diagnostic_confidence`, `wrong_model_id`. **Cost:** one model encode per turn → O(L) over rubric levels.

### 9.2 DINA mastery — `src/models/dina.py`
- **Role:** estimate latent skill mastery per (student, concept).
- **Algorithm:** DINA (Deterministic Input, Noisy-And) with slip/guess parameters;
  conjunctive Q-matrix → P(correct | mastery). `get_mastery()` returns the
  posterior mastery probability, updated each turn from correctness. **Cost:** O(1) per skill per update.

### 9.3 Mental-models catalogue — `src/knowledge_graph/mental_models.py`
- **Role:** detect the specific wrong belief behind an answer.
- **Key fns:** `match_wrong_model()` (L218), `get_wrong_model()` (L209), `MentalModelsCatalogue` (L95).
- **Algorithm:** signal/keyword + confidence matching of the response against
  concept-keyed catalogue entries (`wrong_models_catalogue_v2.json`), each
  carrying belief, origin, signals, refutation. Returns the best `wrong_model_id`
  above a match threshold. **Cost:** O(entries for the concept).

### 9.4 CSO traversal — `src/knowledge_graph/cso_traversal.py`
- **Role:** ground concepts in the CSO 3.5 ontology and pull neighbours.
- **Key fns:** `CSOTraversal` (L63), `get_neighbours()` (L215), `canonical()`.
- **Algorithm:** in-memory index over `CSO.3.5.nt` exposing four relations
  (superTopicOf, relatedEquivalent, contributesTo, …); `get_neighbours()` returns
  parents/children/related/contributes-to; `canonical()` follows aliases.
  **Cost:** O(1) hash lookups after the one-time index build.

### 9.5 Student knowledge graph — `src/knowledge_graph/student_knowledge_graph.py` + `student_graph_service.py`
- **Role:** the central per-student structure that couples every analysis to CSO nodes.
- **Key fns:** `update_from_diagnosis()`, `expand_neighbours()`, `to_dict()`,
  `StudentGraphService.record_turn()`.
- **Algorithm:** resolve concept → CSO slug; create/update the node with LP,
  mastery (+delta), wrong-models (with L3+ refutation rule), misconception notes,
  and the optional per-turn analyses (intervention, etc.); add typed edges from
  1-hop CSO traversal; serialize for the API/UI. **Cost:** O(neighbours) per turn.

### 9.6 RL teaching agent — `src/reinforcement_learning/teaching_agent.py`
- **Role:** pick the intervention type from the diagnosed state.
- **Key fns:** `TeachingRLAgent` (L15), `select_action()` (L152), `get_state_representation()`.
- **Algorithm:** DQN over a state vector (HVSAE latent + mastery + emotion + LP);
  `select_action()` returns argmax-Q action (worked_example / socratic_prompt /
  trace_scaffold / transfer_task), then constrained by the LP-validity gate;
  in-chat learning closes the previous (s, a, r, s′) into the replay buffer.
  **Cost:** one forward pass per turn.

### 9.7 HVSAE encoder — `src/models/hvsae.py`
- **Role:** encode the student's reasoning into a latent used by the LP matcher and RL agent.
- **Algorithm:** hierarchical variational sparse auto-encoder (`HVSAE`, L177)
  producing a latent + misconception-probability head. **Cost:** one encode per turn.

### 9.8 Response generator — `enhanced_personalized_generator.py` (via app)
- **Role:** produce the LP-shaped Socratic tutor reply.
- **Key fn:** `_build_enhanced_prompt()` reads the analysis off `student_state` /
  `analysis` and assembles a structured prompt; `generate_personalized_response()`
  streams the LLM output.
- **Algorithm:** builds an LP-grounded prompt (level + rubric, wrong-model, KG
  context, mastery, chosen intervention) and streams a reply that never reveals
  the answer; a post-generation guardrail (`_sanitise_misconception_quote`)
  strips fabricated misconception quotes.

### 9.9 How the five components REACT to produce the response

The tutor reply is **not** generated from any single signal — it is a **joint
function of all five components**, combined at the prompt level by
`_build_enhanced_prompt()` and written by the LLM. Verified field-by-field:

| Component | What the generator reads (line) | How it shapes the reply |
|---|---|---|
| **LP level** | `current_lp_level`, `target_lp_level` (858–859, 943–944); `lp_rubric_current/target` (972–973) | Sets the target level and the **LP-3 "six-step" teaching structure** (1032) — *what* to teach toward and *how* to phrase it |
| **DINA mastery** | `student_state["dina_mastery"]` (889); mastery line in `tutor_input` | **Calibrates scaffolding** — low mastery → more support |
| **Wrong-model / misconception** | `wrong_model_id`, `_description`, `_origin`, `_refutation`, JLS/ProgMiscon refs (1042–1086); `rag_top_wrong_models` (1182–1212) | Reply **explicitly refutes** the belief using the catalogue refutation; guardrail blocks fabricated quotes |
| **CSO knowledge graph** | `analysis["cse_kg"]`, `pedagogical_kg`, `kg_context` block | **Grounds** the reply in real prerequisites/related concepts ("MUST REFERENCE") |
| **Intervention** | `student_state["recommended_intervention"]` (1133, 1232) | Sets the **move/format** (socratic / trace_scaffold / worked_example / transfer); in probe mode it *replaces* the six-step |

**Pipeline:** the five outputs are packed into `student_state` + `analysis` +
`tutor_input` in `_stream_teach()` → `_build_enhanced_prompt()` emits one prompt
with an LP-1 (diagnostic), LP-2 (wrong-model), LP-2b (RAG), LP-3 (six-step), KG,
mastery and intervention section → the LLM streams the reply → the guardrail
sanitizes it.

**Honest qualifier:** the five components **deterministically build the prompt
context**, but the **LLM writes the final wording**. So the reply reliably
*reflects* level + mastery + misconception + KG + intervention, but it is not a
fixed template — exact phrasing varies per generation, and the guardrail only
catches fabricated misconception quotes, not every possible drift.

---

## 10. Wiring logic — which components are surfaced, and why

**Wired into the wireframe / graph node (the diagnostic + graph-forming set):**
LP level · DINA mastery · wrong-model / misconception · CSO-3.5 tracing ·
selected intervention. These are the analyses a teacher needs to *act* on, and
together they form the student knowledge graph.

**Deliberately NOT surfaced in the wireframe:** the 3-channel psychological
state, the full RL reward breakdown, and the per-turn heuristic flags — they are
computed in the app but kept out of the teacher view to keep it legible. The
wireframe itself is static (a design blueprint); the only live hook is
`record_turn()` feeding the CSO graph from the running app.
