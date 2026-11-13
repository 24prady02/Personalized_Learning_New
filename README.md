# Think on the Graph

Diagnosing a student's answer about a short Java program by walking a knowledge graph. Stage 1 cuts a subgraph out
of the graph from the code alone; Stage 2 walks that subgraph against the student's answer and reports the wrong
rules held, the root cause and a level per concept.

## The 40 scenarios (MY01 to MY40)

The main scenario set is `data/raw/scenarios_40.json`: 40 short Java programs, each with a question and a student's
answer. They were entered and run one at a time in `scenario_explanations/think_on_the_graph.ipynb` (Stage 1, then
Stage 2). They have no gold labels.

Every scenario has its own folder, `scenario_explanations/runs/MYnn/`:

| File | What it is |
|---|---|
| `README.md` | how the algorithm reached the result, stage by stage: each stage explained, with one output of that stage from the run |
| `MYnn.ipynb`, `report.html` | every output of every stage (all edges offered, every score and label, the figures) |
| `MYnn_G.html` | the interactive graph of the run |
| `input.json`, `subgraph.json`, `diagnosis.json`, `traverse_log.txt` | the input, the Stage 1 subgraph, the Stage 2 result and the trace |
| `figureNN.png` | the pictures of the walk, depth by depth |

Results. In 29 of the 40 the walk holds at least one wrong rule; in 11 it holds none. The last
column is a reading of each stored result by hand against the student's answer (2026-11-13), not a gold label:
35 correct, 3 partly right, 1 not right, 1 with a faulty input.

| Scenario | Wrong rules held | Root cause | Overall level | Check by hand |
|---|---|---|---|---|
| [MY01](scenario_explanations/runs/MY01/) | CastAfterIntDivision | `explicit_cast` | L0 | Correct |
| [MY02](scenario_explanations/runs/MY02/) | NegativeRemainderSign | `remainder_operator` | L0 | Correct |
| [MY03](scenario_explanations/runs/MY03/) | AssignmentCopiesObject | `array_aliasing` | L0 | Correct |
| [MY04](scenario_explanations/runs/MY04/) | SwitchNoFallThrough | `switch_statement` | L0 | Correct |
| [MY05](scenario_explanations/runs/MY05/) | CharNotNumeric | `char_arithmetic` | L0 | Correct |
| [MY06](scenario_explanations/runs/MY06/) | LoopBodyStatementOutsideLoop, LoopBodyScopeImpliesLoopLifetime | `loop_body` | L0 | Partly right |
| [MY07](scenario_explanations/runs/MY07/) | IntOverflowWidensAutomatically | `overflow` | L0 | Correct |
| [MY08](scenario_explanations/runs/MY08/) | none | none | L3 | Correct |
| [MY09](scenario_explanations/runs/MY09/) | TargetTyping | `integer_division` | L0 | Correct |
| [MY10](scenario_explanations/runs/MY10/) | ArrayIndexStartsAtOne, OutOfBoundsElementsAreNull | `indexing` | L0 | Correct |
| [MY11](scenario_explanations/runs/MY11/) | NestedLoopsSequential, LoopBodyStatementOutsideLoop, ForVariableScopeBeyondLoop | `nested_loops` | L0 | Correct |
| [MY12](scenario_explanations/runs/MY12/) | CharNotNumeric | `char_arithmetic` | L0 | Correct |
| [MY13](scenario_explanations/runs/MY13/) | CastAfterIntDivision | `explicit_cast` | L0 | Correct |
| [MY14](scenario_explanations/runs/MY14/) | LoopStepAlwaysOne | `for_loop` | L0 | Correct |
| [MY15](scenario_explanations/runs/MY15/) | IncrementByTwo, ForInitRepeats, ForUpdateBeforeBody, PreIncrementBeforeLoop | `for_loop` | L0 | Correct |
| [MY16](scenario_explanations/runs/MY16/) | CastAppliesToWholeExpression | `explicit_cast` | L0 | Correct |
| [MY17](scenario_explanations/runs/MY17/) | none | none | L4 | Correct |
| [MY18](scenario_explanations/runs/MY18/) | OffByOneBound | `off_by_one_error` | L0 | Correct |
| [MY19](scenario_explanations/runs/MY19/) | TargetTyping | `integer_division` | L0 | Partly right |
| [MY20](scenario_explanations/runs/MY20/) | none | none | L2 | Correct |
| [MY21](scenario_explanations/runs/MY21/) | none | none | L3 | Correct |
| [MY22](scenario_explanations/runs/MY22/) | none | none | L2 | Correct |
| [MY23](scenario_explanations/runs/MY23/) | CastAfterIntDivision | `explicit_cast` | L0 | Correct |
| [MY24](scenario_explanations/runs/MY24/) | none | none | L3 | Correct |
| [MY25](scenario_explanations/runs/MY25/) | ThenAlwaysExecutes | `if_statement` | L0 | Correct |
| [MY26](scenario_explanations/runs/MY26/) | DivisionByZeroIsCompileError | `division_by_zero` | L0 | Correct |
| [MY27](scenario_explanations/runs/MY27/) | StringPlusLeftToRight, ArithmeticPlusPrecedes | `string_concatenation` | L0 | Correct |
| [MY28](scenario_explanations/runs/MY28/) | CastAfterIntDivision | `explicit_cast` | L0 | Correct |
| [MY29](scenario_explanations/runs/MY29/) | none | none | L4 | Faulty input |
| [MY30](scenario_explanations/runs/MY30/) | CharNotNumeric | `char_arithmetic` | L0 | Not right |
| [MY31](scenario_explanations/runs/MY31/) | none | none | L3 | Correct |
| [MY32](scenario_explanations/runs/MY32/) | DoWhileTestsFirst | `do_while_loop` | L0 | Correct |
| [MY33](scenario_explanations/runs/MY33/) | none | none | L1 | Correct |
| [MY34](scenario_explanations/runs/MY34/) | ElseMatchesIndentation | `dangling_else` | L0 | Correct |
| [MY35](scenario_explanations/runs/MY35/) | AverageWithoutZeroGuard | `division_by_zero` | None | Partly right |
| [MY36](scenario_explanations/runs/MY36/) | AssignmentCopiesObject | `array_aliasing` | L0 | Correct |
| [MY37](scenario_explanations/runs/MY37/) | none | none | L4 | Correct |
| [MY38](scenario_explanations/runs/MY38/) | none | none | L4 | Correct |
| [MY39](scenario_explanations/runs/MY39/) | RaggedRowsSameLength, NoJaggedArrays | `ragged_array` | L0 | Correct |
| [MY40](scenario_explanations/runs/MY40/) | ProbabilityIsPrediction | `math_random` | L0 | Correct |

The five that are not simply correct:

| Scenario | What is wrong | Where it comes from |
|---|---|---|
| MY29 | the question and answer belong to the scenario before it, not to this program, so the result means nothing | the input |
| MY30 | the student takes `char + int` to be a letter; `CharNotNumeric` says something else | the graph has no misconception for it |
| MY19 | `TargetTyping` is right, but "7 % 2 is 0.5" is not picked up | the graph has no misconception for it |
| MY35 | the right error is found, but the overall level is empty | the graph has no misconception for "0 / 0 is 0", and the level rule sets L0 only for a misconception |
| MY06 | the fitting label, `LoopBodyScopeImpliesLoopLifetime`, is held but only second; the root went to a neighbour | how the root cause is chosen |

Two more inputs carry a slip that does not change the diagnosis: in MY26 and MY40 a line beginning "Actual:" was
pasted into the answer box.

Notes on the set:

- **Numbering.** An exact repeat of MY18 was removed and the scenarios after it were renumbered, so MY26 to MY40 were
  MY27 to MY41 before. Commit messages before 2026-11-13 use the old numbers.
- **Graph version.** MY01 to MY25 were run on graph 3.9.7 and MY26 to MY40 on 3.9.8, the graph in this repository.
  For these scenarios the two differ only in the `primary` / `context` role of some misconception edges; no text,
  concept or edge differs. Replaying the recorded model answers on the current graph gives the same held rules, root
  cause and levels in 37 of the 40. The three that change are MY05 and MY12 (the same misconception, filed at `char`
  instead of `char_arithmetic`) and MY18 (root cause `loop_control` instead of `off_by_one_error`). The stored
  results were not re-run.

## The knowledge graph, concept by concept

`concept_wise_graph/<concept>/` has one folder for each of the 173 concepts of the graph, named by the concept id,
with three files: `<concept>.ipynb` (the short notebook that was run for it), `<concept>.png` (the picture of the
graph around the concept) and `<concept>.md` (the concepts associated with it, and every edge in the view with its
full label: the exact edge logic, the wrong and right rules, every way of each level with its exact rule). They are
written by `python src/concept_notebooks.py`. `scenario_explanations/kg_visualizer.ipynb` draws the same view
interactively for any concept; every edge it draws is an edge of the graph.

## Stage 1: what is being done

A scenario is a short Java program (plus a question and a student's answer, which this stage never opens).
The knowledge graph (KG) stores, on every concept node, the regular expressions that recognise that concept in
Java code. Stage 1 runs those patterns over the scenario's code and takes the matching part of the KG out:

1. **Concept nodes** – the concepts whose own code patterns matched the code. Nothing is added from the
   question, the answer, or from neighbouring KG nodes.
2. **Concept edges** – every `prerequisite` and `parallel` edge of the KG whose two ends are both concept nodes.
3. **Misconception and error nodes and edges** – every `misconception` / `error` edge that leaves a concept
   node, together with the record it points to (wrong belief, correct rule).
4. **Level nodes and edges** – the five `has_level` edges L0–L4 of each concept node, with their level nodes
   and the `ways` stored on each edge.
5. **Level ↔ misconception links** – the `linked_misconception` entries inside those ways.

The result is written as one JSON file per scenario, one figure per scenario, a summary table and a listing.

Not in this stage: the question, the student's answer, concept `aliases`, PageRank, NLI, Viterbi, embeddings,
LLMs, edge selection, level decisions. The gold concept labels in the scenario file are used only by the report
and the tests to check coverage; they never enter the subgraphs, the figures, the summary or the listing.

## Setup

```bash
pip install -r requirements.txt     # pytest; matplotlib and networkx only for the figures
```

## Layout

```
README.md                                    this file
requirements.txt                             pytest; matplotlib, networkx (figures); jupyter only for the notebook
pytest.ini                                   testpaths = tests, pythonpath = src
data/
  raw/chapter1_kg_updated.json                   knowledge graph v3.9.8 (173 concepts, 1943 edges, 296 misconception/error records, 865 level nodes)
  raw/scenarios_40.json                      the main set: the 40 scenarios MY01-MY40 (code, question, answer; no gold labels yet)
  raw/scenarios_not_from_code.json           the other 10 scenarios (prose code, or a gold concept only the answer brings in)
  processed/<sid>_subgraph.json              one extracted subgraph per scenario (output of src/evaluate.py)
  processed/<sid>_diagnosis.json             Stage 2 output: held misconceptions, root cause, levels, paths, evidence, clause coverage, stop reason, prompts per step
src/
  preprocessing.py                           mask_java, split_statements, command_segments, Prepared
  model.py                                   tag_code (pattern channels of every concept) + extract_subgraph / subgraph_from_code
  train.py                                   builds and checks the pattern bank (no learned parameters; see below)
  evaluate.py                                runs the scenarios: processed JSON, coverage report, figures, summary.csv, results.md, metrics.json
  utils.py                                   paths, load_kg, load_scenarios, reader_blocks, gold_concepts (check only), regex cache
  traverse.py                                Stage 2: ToG traversal over a Stage 1 subgraph (reads question + answer), writes <sid>_diagnosis.json
  prompts.py                                 the Stage 2 prompts: one edge prune, three edge labels (misconception edge, concept edge, level way); the only places the model is asked
  compare.py                                 Stage 2 vs gold (checking only): results/tables/stage2_vs_gold.csv, results/stage2_results.md
  demo.py                                    Stage 1 and Stage 2 on one scenario, with the step report and the page of the run
  steps_report.py, viz.py                    the step report of a run (results/viewer/<sid>_steps.md) and its figures
  upload.py                                  builds scenario_explanations/runs/<sid>/ for a run and commits it
  concept_notebooks.py                       runs one notebook per concept and writes concept_wise_graph/<concept>/
scenario_explanations/
  think_on_the_graph.ipynb                   enter a program, a question and an answer; runs Stage 1 and Stage 2 and shows every step
  start_notebook.bat                         starts the notebook server and opens think_on_the_graph.ipynb
  runs/MYnn/                                 one folder per scenario (see "The 40 scenarios" above)
  kg_visualizer.ipynb                        the graph around any concept, interactive; lists the concept folders
  explore_subgraph.ipynb                     step through one scenario: code, masked code, hits, subgraph, figure
concept_wise_graph/
  <concept>/<concept>.ipynb, .png, .md       one folder per concept of the graph: notebook, picture, every edge with its full label
experiments/
  config.json                                default paths and extractor settings (hops 0, keep_generic false)
  pattern_bank.json                          the compiled pattern bank summary written by train.py (the model "checkpoint")
  logs/train_log.txt                         pattern compile + pattern-test check
  logs/subgraph_report.txt                   one line per scenario over tests/data/scenarios_gold.json, "fully covered: 10 / 10"
  logs/subgraph_report_not_from_code.txt     the same over scenarios_not_from_code.json (misses expected)
  logs/traverse_<sid>.txt                    Stage 2 trace: start ranking, candidates, kept edges, labels, quotes, clause coverage, levels
  llm_cache/<hash>.json                      every prompt sent in Stage 2 and the model's reply (re-runs are free and deterministic)
results/
  results.md                                 summary table, then per scenario: code, figure, concept nodes, edges with logic, misconception nodes, level counts
  figures/<sid>.png                          node visualization of each subgraph
  tables/summary.csv                         one row per scenario (counts, concept ids, edges traced, misconception node ids)
  metrics.json                               coverage and size metrics
  stage2_results.md, tables/stage2_vs_gold.csv   Stage 2 diagnoses against the gold (checking only)
  viewer/<sid>_steps.md, _demo.html, _G.html, _figureNN.png   the step report, page, interactive graph and figures of each run
paper/
  main.tex, references.bib, main.pdf         mid-term progress report (ACM format)
  figures/                                   figures used by the paper
slides/
  Pradhyumn_Nair_midterm_slides.pptx         mid-term presentation
tests/
  test_subgraph.py                           Stage 1 (228 tests)
  test_traverse.py                           Stage 2 with a mocked model (19 tests, 1 skipped)
  data/scenarios_gold.json                   the earlier gold-labelled set, used by the tests and by compare.py
  data/concept_pattern_tests.json            must_tag / must_not_tag snippets for all 166 code-visible concepts
```

## Commands

```bash
pytest -q                      # 247 tests (Stage 2 tests use a mocked model, no real call)
python src/train.py            # compile every pattern, check the 372 labelled snippets, write experiments/pattern_bank.json
python src/evaluate.py         # data/processed, experiments/logs/subgraph_report.txt, results/ (figures, summary.csv, results.md, metrics.json)
python src/evaluate.py --scenarios data/raw/scenarios_not_from_code.json --no-figures --no-json
jupyter notebook scenario_explanations/explore_subgraph.ipynb
python src/traverse.py MY07      # Stage 2 on one scenario (needs the claude CLI, or `--backend anthropic` with the SDK and a key)
python src/traverse.py --all     # every scenario
python src/compare.py            # Stage 2 diagnoses against the gold (gold is used for checking only)
python src/demo.py --scenario MY07   # Stage 1 and Stage 2 on one of the 40 scenarios, with its step report
python src/concept_notebooks.py      # one notebook per concept into concept_wise_graph/ (or name concepts to run only those)
scenario_explanations\start_notebook.bat   # open think_on_the_graph.ipynb to run a new scenario
```

## Stage 2: ToG traversal (`traverse.py`, `prompts.py`)

Stage 2 reads the question and the student's answer and walks the Stage 1 subgraph the way Think-on-Graph walks
a knowledge graph. Settings are in the `traversal` block of `experiments/config.json` (width N = 3, depth D = 3,
model, prune tool llm / bm25 / sentencebert).

The model is used in two places only: edge pruning (replaceable by BM25 / sentence-BERT) and edge labelling.
Start concepts are Stage 1's tagged concepts, as ToG's released code uses the given topic entities; the stop
decision is a rule (graph check plus clause coverage); and levels are read from the graph by rule, because the
level ways are edges of the search like everything else.

1. **Clauses and start concepts.** Quote characters are removed, then the answer is split at sentence ends, `;`,
   before `because` / `so` (after a comma, a space or a closing quote), and a parenthetical remark of two or more
   words becomes its own clause. `/` is kept: inside a written output it is a line break. Start concepts (no
   model call): every non-generic concept of the subgraph, that is, the concepts Stage 1 tagged in the code, plus
   a generic concept whose tagging text occurs verbatim in the answer (the student names it in code, e.g. `=` for
   assignment in "a = b"). When there are more than N, they are ranked by BM25 of the student's answer against each concept's text (its id
   with underscores as spaces plus the texts of its misconception and concept edges), ties broken by the number
   of Stage 1 code hits, then by id.
2. **Edge search** (no model). Depth 1: two families, the concept's misconception and error edges, and its
   **level ways**. Every way of a has_level edge in the graph is an edge of its own (`lvl:<concept>@<L>#i`, logic =
   the way's exact rule); ways of kind "misconception" are left out because the misconception edges already carry
   them. Deeper: the concept's prerequisite / parallel edges inside the same connected piece. Edges already on a
   path are skipped; primary role first.
3. **Edge prune.** One call per concept and family picks up to N edges the answer engages with, scores summing
   to 1 (or BM25 / sentence-BERT similarity instead of the call). Pruning each family on its own means a level way
   never competes with a misconception edge for a slot.
4. **Edge label.** The kept misconception / error edges of a concept are judged together in one call, one reply
   line per edge: held / correct / not applied, each shown with its wrong rule and right rule. Judging them side
   by side lets the model give held to the rule whose claim the student actually makes when several wrong rules
   would fit the same words, and still hold two when the student holds two (held means the answer follows the
   wrong rule in what sets it apart from the right rule: where the student gives a reason it must be this rule's
   own, a result the rule would also predict but reached by another reason does not hold it, and a rule about
   something neither the program nor the answer contains is not applied). Evidence is given as clause numbers,
   not a free quote, so the code knows exactly which words each label rests on and two labels on the same clause
   are known to rest on the same words. One call per edge, with the same clause-number evidence: confirmed /
   broken / not applied for a concept edge shown with its logic; shown /
   not shown for a level way shown with the concept, the way's name and what an answer that shows the way does,
   and nothing else: no level name, no deciding question, no level in an id, so the way is judged against its own
   text like every other edge and its level comes only from where it sits in the graph. Every reply names the
   clauses and gives a confidence; a label with no clause behind it is not applied.
   Score = prune score × confidence.
5. **Keep the best N in tiers**: held misconceptions and broken edges first, then held errors, then correct /
   confirmed / shown edges; by score within a tier (an edge reached from both ends in one round counts once).
   Confirmations therefore never crowd out a diagnosis. Every labelled edge whose quote is in the answer is
   recorded as **evidence**, kept or not, so a dropped "correct" label still explains its clause.
6. **Stop test** (no model). (i) Graph check: every concept the walk has entered has its concept edges, the
   prerequisite and parallel links to the other concepts of its piece, read before the walk may stop. For a
   faulted concept that is where the root cause lies; for a concept the student got right it is the conceptual
   trace, the confirmed links between concepts, which is as much part of the diagnosis as the faults. (ii) Clause
   coverage: a clause is covered when some labelled edge names it. The walk stops with reason "sufficient" when
   no concept edge is pending and every clause is covered; at max depth the uncovered clauses are reported as
   unexplained.
7. **Next concepts**: every entered concept whose concept edges are unread (it reads them next); the far end of
   each kept concept edge, entered as a start concept so its own misconception edges and level ways are read and
   it gets a level of its own; the source of each held misconception (to walk back). An edge is offered once per
   depth, not from each of its ends. A level way leads nowhere: it describes the concept itself. When clauses
   remain uncovered and the width is
   not full, the uncovered clauses bring in concepts the walk has not entered yet: BM25 of those clauses against
   the unvisited concepts of the start pool, best first, no model call. Such a concept enters as a start concept,
   so its own misconception edges and level ways are read at the next depth. This is what lets a correct
   multi-concept answer, whose labels give no direction of their own, reach every concept the student wrote about.
8. **Diagnose.** A held error beside a held misconception on the same concept is evidence, not a second diagnosis.
   Every held misconception stays: a student can hold several at once, and the judgement is made at the label
   step, edge by edge. A held misconception resting on the same words as a stronger one on the same concept is
   marked `shares_evidence_with` that edge (the graph words one wrong idea in several ways, e.g.
   IfConditionWatched / IfWaitsForCondition on if_statement; both come out held, and the comparison counts the
   pair as one). One fault, one location: the same misconception held at both ends of a prerequisite edge is
   filed at the dependent concept, and a broken edge shown by the same words as a held misconception is that
   misconception's consequence (`consequence_of`), so neither marks a root cause of its own.
   Root cause: walk prerequisite edges back from the concepts with a held misconception and take the furthest-back
   concept that itself holds a misconception or is the target of a broken prerequisite edge (a broken A → B says
   the student did not carry A into B, so the fault sits at B). Level per concept, by rule from the evidence and
   with no model call: L0 when the concept holds a misconception (the level then reads the edge of that one
   misconception, the kept finding, and carries the L0 way's own text from `level_mis_links` as `rule`) or an L0
   way (everyday reading, inconsistent trace) is shown, since the L0 deciding question asks whether every rule the
   answer applies agrees with the language rule; otherwise the highest level with a shown way, because the levels are cumulative and an answer
   at L4 also does L3. A concept with no held misconception and no shown way gets no level. Overall level: the
   root-cause concept's level (for an answer with no error, the lowest level reached). Output also lists the
   evidence, which edge covers each clause, the uncovered clauses, the stop reason (sufficient / half_stop / max
   depth) and the number of prompts per step (prune, label).

The model never answers from its own knowledge: every label is an edge of the graph plus a quote. Replies are
cached in `experiments/llm_cache/`, so a re-run costs only the prompts that changed.

Results over the 10 gold scenarios (`python src/compare.py`, full table in `results/stage2_results.md`; gold is
used for checking only): held misconception set right in 9/10, every gold "correct" misconception found in 8/10,
root cause right in 10/10, overall level right in 9/10, 47 of 72 points (one point each for held set, correct set,
root cause and overall level, plus one per gold-scored concept level and per gold edge), 195 prompts in all, every
one of them a prune or a label. S134 is found through the generic-concept rule: its only tagged concept is
variable_swap, the gold misconception (VariablesHoldExpressions) sits on assignment, which Stage 1 marks generic,
and the answer repeats the `=` that tagged it. On S007 the held set is exact (OffByOneBound at loop_control, root
cause loop_control, L0). The one remaining level miss is S052, L3 where the gold says L2: the student's "an
average of 5 new numbers, no file" matches the redirection way "`A > f` followed by `B < f` has the same effect as
`A | B`, except that the pipe creates no file", and "args is empty" matches "args.length is the number of arguments
typed (0 if none)"; the graph files both ways at L3, the gold levels the answer L2. The walk read the edges as the
graph states them; the disagreement is between the graph's placement of those ways and the gold.

The way-label prompt shows the model the concept, the way's name and the way's text, and nothing else. An earlier
form also showed the level's name and deciding question; on S057 the model then followed the deciding question's
boundary ("fixing one given failing case is L3") and rejected two L4 ways whose own text the student matched, which
put the answer at L2 overall instead of the gold's L4. Judging the way against its own text, like every other edge,
gives L4.

Two earlier versions were run over the same 10 scenarios and removed. One asked the model for the start concepts
(a START prompt) and the stop decision (a SUFFICIENCY prompt): same 42/72 points as the rule-based start and stop
of the time, 126 prompts against 114; neither prompt changed a diagnosis. The other levelled a concept with one
level-ladder prompt over all its ways after the walk, and only for concepts on a kept path: 42/72 points, overall
level right in 6/10, with correct answers (S026, S047) getting no level at all because no misconception edge was
labelled and the level ways were never searched. Making the ways edges of the search raised that to 46/72 and 8/10.

`evaluate.py` flags: `--hops 1` adds one prerequisite hop (off by default, so nodes are exactly the tagged
concepts); `--keep-generic` switches the generic-node rule below off; `--no-figures` skips matplotlib /
networkx. Defaults come from `experiments/config.json`.

`train.py` is the training step of a model that has no learned parameters: the parameters are the regexes
stored in the KG. It compiles every pattern of every channel, runs the must_tag / must_not_tag snippets of
all 166 code-visible concepts, and saves the pattern-bank summary and a log. It exits non-zero on any compile
error or failed snippet.

## How the matcher works (`model.py`, part 1)

1. `mask_java` blanks the contents of string and char literals and of comments, keeping every length and
   newline, so a `%` or `;` inside `"..."` cannot match a pattern. Line numbers of hits stay correct.
2. `split_statements` cuts the masked text at `;` `{` `}` when the parenthesis depth is 0, so a
   `for (…; …; …)` header stays one statement. Statement-scoped signals run on these pieces.
3. Shell lines (`% java Prog 3 < in.txt`) are cut into `java …` / `javac …` segments for the command patterns.
4. For each concept's `reader` block the channels are run, each hit recorded as
   `{channel, name, decisive, match, line}`:

   | channel | KG field | runs on |
   |---|---|---|
   | pattern | `code_patterns` | whole masked program (raw text if the block says `code_text: raw`) |
   | signal | `signals[].regex` | program or each statement, per `scope`; signals without a regex (compiler messages) are skipped and reported in `warnings` |
   | operator | `operator_symbols` | substring search in the masked program |
   | type | `java_types` | whole-word search |
   | command | `command_patterns` | the `java` / `javac` shell segments |

   Concepts with `code_visible: false` (7 of the 173) never tag. `aliases` are never used.
   The program is masked and split once and shared by all 166 pattern sets.

## How the subgraph is taken out (`model.py`, part 2)

1. **Tagged concepts, minus bare generic ones.** The KG marks 21 concepts `generic` (statement, identifier,
   literal, int, assignment, variable, …); they fire on almost any Java line. A generic concept stays a node
   only when the code ties it to something specific: the KG has a prerequisite or parallel edge between it and
   a non-generic tagged concept (assignment next to variable_swap, string_literal next to println), or one of
   its own decisive signals fired (class_declaration with a file-name mismatch). This rule reads nothing but
   the KG, so it is the same for every snippet; nothing scenario-specific is applied anywhere.
2. `prerequisite` / `parallel` edges with both ends inside, ids `pre:a->b`, `par:a~b`, with the KG `logic` text.
3. `misconception` / `error` edges from each node, ids `mis:a->M`, `err:a->E`, with role, logic, twin logic,
   and the target record's wrong belief and correct rule.
4. `has_level` edges from each node (ids `lvl:a->a@Lk`) with their ways, and the level node records
   (name, criterion, deciding question).
5. `linked_misconception` entries of every way, as `{level_node, misconception, way, rule_type, exact_rule}`.
6. **Connectivity is reported, never repaired.** `components` lists the connected pieces of the concept
   nodes over the concept edges. When there is more than one piece a warning names them. Six of the eleven
   subgraphs fall into several pieces because the KG has no edge between concepts that occur together
   (for example loop_body and for_loop, arithmetic_operators and remainder_operator, run and
   command_line_args, do_while_loop and loop_control). Those are gaps in the KG; the extractor does not invent
   edges to close them.

Output JSON per scenario:

```
scenario, concepts[{id, why, hits, generic}], concept_edges, misconceptions, mis_edges,
levels, level_edges (with ways), level_mis_links, components,
counts{tagged, concepts, generic, from_hop, concept_edges, misconceptions, mis_edges, levels, level_edges, level_mis_links, components},
warnings
```

## Results

`evaluate.py` draws each subgraph: concept nodes (dark blue, generic ones light blue) laid out per connected
piece, prerequisite arrows and dashed parallel edges, the five level squares under each concept, misconception
(red) and error (orange) nodes around each concept, and a side panel listing the misconception and error nodes
per concept. `results/results.md` opens with the summary table (counts, the edges traced, the misconception
node ids) and then lists each scenario with its code, figure, concept nodes, edges with logic, misconception
nodes and level counts. `results/tables/summary.csv` holds the same per-scenario data. The order of every list in the outputs is
fixed (sorted ids), so two runs produce identical files.

Current run over the earlier gold-labelled set (`tests/data/scenarios_gold.json`):

| scenario | concept nodes | concept edges | misconception/error edges | misconception nodes | level nodes | pieces |
|---|---|---|---|---|---|---|
| S000 (reference) | 4 | 2 | 18 | 17 | 20 | 2 |
| S001 | 4 | 5 | 18 | 15 | 20 | 1 |
| S007 | 17 | 14 | 141 | 104 | 85 | 3 |
| S008 | 19 | 16 | 141 | 108 | 95 | 4 |
| S021 | 12 | 10 | 87 | 69 | 60 | 2 |
| S026 | 2 | 1 | 17 | 15 | 10 | 1 |
| S047 | 2 | 1 | 7 | 6 | 10 | 1 |
| S052 | 8 | 7 | 17 | 16 | 40 | 2 |
| S057 | 26 | 22 | 167 | 120 | 130 | 4 |
| S134 | 2 | 1 | 17 | 15 | 10 | 1 |
| S137 | 4 | 5 | 18 | 15 | 20 | 1 |

## Coverage report and dataset split

`evaluate.py` also prints one line per scenario (tagged concepts, node / edge / misconception / level counts,
pieces, and the gold concepts not found) and ends with `fully covered: N / 10`; `results/metrics.json` holds
the same as numbers (mean gold-concept recall, share of gold among the nodes, mean sizes, subgraphs in one piece). On the earlier gold-labelled set (`tests/data/scenarios_gold.json`) every gold
concept of all ten scenarios is found from the code: 10 / 10. The extra nodes relative to gold are
non-generic constructs really present in the code (the loop around S057's division, for instance); only the
question and answer, read in a later stage, can say which of them a scenario is about.

The other ten scenarios are kept in `scenarios_not_from_code.json` because code alone cannot produce their
gold concepts: the "code" is prose or a bare declaration (S009, S010, S012, S015, S068), or a gold concept
comes only from the student's answer (the while loop compared with a do-while in S005, division in S016, the
missing `break` in S023 and S073, compiling in S080). Running the report on that file marks those misses
`xfail`.

## Tests (`pytest -q`, 247 passing: 228 for Stage 1, 19 for Stage 2)

- masking keeps length and blanks literals and comments; statement splitting keeps a `for` header whole;
  shell segments are cut correctly;
- every one of the 166 code-visible concepts has must_tag / must_not_tag snippets and passes them; the 7
  code-invisible concepts never tag;
- the matcher stays fast on long inputs (per-regex time limit, best of three runs);
- the S007 subgraph has the expected nodes, edges, misconception edges and levels; 23 small task snippets tag
  the right concepts;
- every gold concept of every scenario in the earlier gold-labelled set (`tests/data/scenarios_gold.json`) is found, and the concept nodes are exactly
  the tagged concepts (no hop, no node the code did not show).

## Concepts the knowledge graph does not have

Constructs that chapter-1 student code can contain and that no concept node covers, so no regex can produce a
node for them. The graph is kept at its 173 concepts on purpose; an extension with sixteen concepts for these
constructs was built and then withdrawn (git history, commit 898436e) and can be restored if wanted.

| Construct | Example | Nearest existing concept |
|---|---|---|
| String methods and string comparison | `s.length()`, `s.charAt(0)`, `s.equals(t)`, `s == t` | api (lists the calls), string_type |
| Method definition, return, parameters, recursion | `static int sq(int x) { return x * x; }` | main_method, method_call (calls only) |
| import / package | `import java.util.Scanner;` | none |
| null and object references | `String s = null;` | primitive_vs_reference, array_reference (arrays only) |
| Unary operators | `-x`, `+x` | arithmetic_operators (binary only), logical_operators (`!`) |
| Bitwise and shift operators | `a & b`, `x << 1` | exclusive_or (`^` only) |
| Hex, octal, binary and underscore literals | `0x1F`, `0b101`, `1_000_000` | number_conversion (toBinaryString only) |
| Character methods | `Character.isDigit(c)`, `Character.toUpperCase(c)` | char, api |
| StringBuilder | `new StringBuilder()` | none |
| Exceptions | `try { } catch (Exception e) { }`, `throw` | run_time_error (effects only) |
| Wrapper types and autoboxing | `Integer n = 5;` | integer_constants, parsing |
| Collections | `ArrayList<Integer>` | none (later chapter) |

## Pattern changes made in the KG (v3.9.5-reader4)

The KG file is the only place patterns live, so pattern errors were fixed in the KG itself. All 77 changes
(35 corrections of existing patterns, 42 additions) are listed in `kg["reader"]["pattern_fixes_reader4"]` with
the old and new regex, and each touched reader block carries `patterns_fixed_in`. They were found by running all 166 concepts over the test snippets and the 20
scenarios and reading every cross-fire (precision), and by running 581 variant snippets of chapter-1 constructs
and reading every miss (recall). None of them is tied to a scenario.

Precision fixes (a pattern fired where the concept was not present):

| Concept(s) | Error | Fix |
|---|---|---|
| remainder_operator, arithmetic_operators | the shell prompt `%` and prose across a line break tagged the operators | operands must sit on one line; bare `%` operator symbol dropped |
| comparison_operators | redirection `<` `>` on shell lines tagged it | pattern skips lines starting with `%`, `$`, `java`, `javac`; bare symbols dropped |
| command_line_args, black_box_model | `java Average < data.txt` counted `<` as an argument | argument may not start with `<`, `>`, `\|` |
| overflow | identical to integer_constants, so naming `Integer.MAX_VALUE` was "overflow" | needs arithmetic on the constant (`MAX_VALUE + 1`, `-MIN_VALUE`, `Math.abs(MIN_VALUE)`) |
| widening_conversion, type_conversion | `0.1 + 0.2` matched as int `1 + 0.2` | int literal may not be the fraction digits of a double |
| program_layout | one `if … ; else …;` or one `case …: …; break;` counted as two statements on a line | else / case / default lines skipped |
| compile_time_error | a continuation line ending in `+` or `,` was a "missing semicolon" | lines ending in an operator or comma not flagged |
| while_loop | the `while (c);` tail of a do-while tagged a while loop | that tail excluded |
| array_compared (x2), array_printed_regex, flag_set_in_loop, loop_variable, uninitialized_read_regex | unbounded `[\s\S]*?` gaps, quadratic on long inputs | bounded to 800 (2000) characters, same convention as integer_division |

Recall additions (the concept was present and no pattern fired), 42 new patterns or signals, for example:
`System.err.print` / `println` for print and println, `.format(` for formatted_output, brace-less `do`, `if`
inside `if` and loop inside loop without braces, while-loop array traversal, `s += "text"` for
string_concatenation, `String.valueOf` / `Integer.toString` for string_conversion, `\r` `\f` and unicode
escapes, `(int)` on a char and `++` on a char for char_arithmetic, a lower-case class name for
naming_convention, arithmetic on the literal `2147483647` for overflow, `Long.MAX_VALUE`, tolerance
comparisons for floating_point_precision, an `int_into_double` signal for widening_conversion and
type_conversion, `Integer.parseInt(` and `* 1.0` for type_conversion, `StdRandom` calls, library calls such as
`Math.max(` for method_call, the String API for api, Scanner reads for standard_input, output redirection
`> file` for standard_output, `args.length` for command_line_args, a type-mismatch literal and `=` in a
condition for compile_time_error, negative indices for run_time_error, parenthesised sums before `*` for
operator_precedence, array transpose for matrix_operations, `a[i]++` for frequency_counting, `!a && !b` for
de_morgan, and a `file_name_mismatch_regex` signal on class_declaration.
