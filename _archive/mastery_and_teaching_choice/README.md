# Mastery tracking, teaching-action choice and hierarchical RL (archived 2026-10-01)

The live system now does two things only: LP-level classification
(`src/orchestrator/lp_diagnostic.py`) and the student concept map on the
Chapter-1 graph (`src/knowledge_graph/student_knowledge_graph.py`,
`src/knowledge_graph/concept_map.py`). No tutor reply is generated.

Moved here, paths mirror their old location:

| What | Files |
|---|---|
| Mastery tracking | `src/models/dina.py` (DINA), `src/student_modeling/` (BKT) |
| Teaching-action choice | `src/reinforcement_learning/teaching_agent.py`, `lp_progression_rnn.py` (intervention ranker), `policy_network.py`, `reward_function.py`, `src/orchestrator/orchestrator.py` (InterventionOrchestrator), `src/teaching/` |
| Hierarchical RL | `src/reinforcement_learning/hierarchical_multi_task_rl.py` |
| Dynamic KG updater | `src/reinforcement_learning/knowledge_graph_updater.py` |
| Orchestrator API | `api/server.py` |
| RL training | `scripts/train_rl_teaching_agent.py` |

Snapshots of the files that were cut down rather than moved, as they were
before the change: `scripts/cpal_chat_app_with_tutor.py`,
`api/student_app_with_mastery.py`, `src/system_registry_full.py`.

To restore, move the files back and replace the cut-down files with the
snapshots.
