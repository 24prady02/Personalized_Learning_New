# Deferred work — catalogue expansion (Priority 4)

**Status:** Not implemented in the 2026-05-23 scenario-coverage pass.
**Reason:** Heavy multi-day model-retraining effort; out of scope for a
same-session change.

## What it would entail

Expanding the catalogue from 20 to ~30 concepts (the recommended
additions were OOP basics, exception handling, recursion, common
collections, basic algorithms, file I/O). Every concept addition
requires:

1. **Catalogue definition** — add wrong-model variants (A, B, C) per
   concept to `src/knowledge_graph/mental_models.py` (or wherever the
   catalogue lives), each with `conversation_signals`, jargon traps,
   LP-level rubrics, and intervention preferences.

2. **`CONCEPT_SIGNATURES` table** — extend
   `src/orchestrator/concept_resolver.py` with substring + regex
   patterns per concept for error/code/text channels. Existing
   table has ~60 entries per concept; adding 10 concepts ≈ 600 new
   patterns. Each needs validation against false positives.

3. **`SKILL_INDEX` + DINA Q-matrix** — extend
   `src/models/dina.py` to add 10 new skills. Update `_DIFFICULTY`
   bumps for any new HARD_CONCEPTS. Q-matrix may need to expand
   (items × skills).

4. **LP head retraining** — the trained sentence-transformer LP
   head currently uses 4 classes (L1-L4) trained on 1349 examples
   (val_acc 0.764). Adding concepts doesn't change the LP head
   schema but DOES change the data distribution if new concepts
   have different LP-level prose. Re-curate training data, re-run
   `scripts/cpal_train_lp_st_v2.py` (multi-hour on GPU).

5. **WM head retraining** — the trained WM head has 60 classes
   (3 wrong-models × 20 concepts) trained on 784 examples
   (val_acc 0.549). Adding 10 concepts = 30 new wrong-model
   variants = re-curate ~390 labeled examples, retrain via
   `scripts/cpal_train_wm_st.py`.

6. **RAG corpus update** — the catalogue RAG store needs the
   new concepts indexed. Run `scripts/cpal_train_heads.py` (or
   the relevant index builder).

7. **Scenario coverage** — add ~50 new scenarios across the
   10 new concepts (3-5 per concept) to both `run_all_scenarios.py`
   and `run_all_scenarios_ollama.py`.

8. **Re-run everything** — internal harness, Ollama runner,
   multi-turn runner. Diff against current baseline.

## Estimated effort

| Phase | Time |
|---|---|
| Catalogue + signatures + DINA expansion | 1 day |
| LP head data curation + retraining | 1-2 days (data quality is the bottleneck) |
| WM head data curation + retraining | 2-3 days (60 → 90 classes, low val_acc already a concern) |
| RAG corpus rebuild + validation | 0.5 day |
| New scenarios + harness re-run | 0.5 day |
| **Total** | **5-7 days of focused work** |

## When to do it

Doesn't make sense until:
- (a) Real student data confirms the current 20-concept catalogue is
  the actual coverage gap (vs. e.g. response quality or multi-turn
  state being the real issue), OR
- (b) There's a labeled dataset of student inputs across the 10 new
  concepts that can be used for retraining without manual annotation.

## Alternative — concept-extension WITHOUT retraining the heads

A lighter intermediate step: add new concepts to the resolver
signatures + catalogue ONLY, accept that LP and WM classification
will degrade for those concepts (LP head returns one of L1-L4 based
on prose features regardless; WM head can't return labels it wasn't
trained on). This gives ~80% of the value at ~10% of the cost but
the WM head will systematically miss the new concepts.

If you want this intermediate step, that's a ~1-day change instead
of 5-7. Say the word.
