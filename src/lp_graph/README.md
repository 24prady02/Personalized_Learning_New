# lp_graph — graph-traversal classifier (no LLM)

Reads a student's answer onto the Chapter-1 knowledge graph
(`data/chapter1_kg.json`) with two graph algorithms — **Personalized PageRank**
for candidate concepts and **ES-Viterbi** (Element-State Semi-Markov Viterbi)
for the route — and returns concept nodes, the student route (concept map),
the correct route, their comparison, misconceptions, a level per concept
(L0–L4), the root cause and feedback.

No generative model is called and nothing touches the network at run time.
spaCy (`en_core_web_sm`) only splits sentences; `javac`/`java` (if installed)
compile and run the code. The same input always gives the same output.

```python
from lp_graph.graph import KG
from lp_graph.pipeline import assess

kg = KG()                                     # loads data/chapter1_kg.json (+ kg_parts.json)
a = assess("int count;\nSystem.out.println(count);",
           "What does the system print?", "It will print 0.", kg)
print(a.to_markdown())                        # readable trace; a.to_dict() for JSON
```

## Pipeline (one module per step)

| # | Step | Module |
|---|------|--------|
| 1 | Split into statements. **Code**: one per statement/header (`execution.parse`) + a result statement from the real run (output or compile/run error). A local declared without initializer and then read is a compile error, found statically and by `javac` (never jshell, which would default it to 0). **Question**: sentences + type (`output / explain / why / fix`). **Answer**: sentences → clauses (so / because / but / then / whereas), each with concepts, slots, negation, link words. | `statements.py`, `execution.py`, `slots.py` |
| 2 | Personalized PageRank seeded code ×1.0, question ×0.6, answer ×0.4; restart 0.5; ranked by `pi/deg`. Candidates = seeds + top-6 bridges within 2 hops + the main concept's contrast (parallel) neighbours; main concept = top code/question seed unless a decisive code pattern forces it. | `candidates.py` |
| 3 | Reader: each 1–3 statement segment vs each candidate element → `MATCH / CONTRADICT / NO` (concept ways, relation edges by edge-logic parts), `MATCH-WRONG / CONTRADICT-RIGHT` (misconceptions, confirmed by the real run and the misinterpreter run), `WRONG_UNLISTED`. | `reader.py`, `claims.py` |
| 4 | ES-Viterbi twice: code + question → correct route; answer → student route (2-best, plus a connected subgraph for list-like answers). | `viterbi.py` |
| 5 | Compare routes → covered / lacking / excessive / broken / skipped. Non-stateable edges (`questionable`, `order_only`) are never lacking. | `compare.py` |
| 6 | Level per concept (L0 gate, then L1→L4), root cause (reverse BFS up prerequisites + contrast neighbour), consistency caps. | `levels.py` |
| 7 | `Assessment.to_dict()` / `to_markdown()`. | `pipeline.py` |

Supporting modules: `graph.py` (KG wrapper: adjacency, `RelEdge`/`MisEdge`,
topological order, hop distances, aliases), `knowledge.py` / `cues.py`
(stand-ins for `lp_percpt.knowledge` / `lp_percpt.cues`), `parts.py` (derived
data), `lexicon.py` (all word lists), `nli.py` (optional, off by default).

## Derived data

`python scripts/prepare_kg_parts.py` writes `data/kg_parts.json`: edge-logic
parts tagged with their endpoint concept and slots, way-rule slots,
misconception wrong/right slots, aliases and a coverage report. It is
byte-identical across runs and records the hash of the graph file; if the
graph changes, `KG` rebuilds the parts in memory and logs a warning until you
regenerate. `chapter1_kg.json` itself is never edited.

## Where the knowledge lives

The code holds no topic tables. Everything the reader knows about the chapter
and about English is in the graph file (`data/chapter1_kg.json`):

* each concept's `reader` field: aliases, code / command patterns, operator
  symbols, Java types, generic / declaration flags, structural `signals`
  (regexes or named Java analyses; decisive or not; the rule slot code with
  that signal acts out) and the run outcome it stands for;
* each misconception's `misread_as`: the generic code transform of its
  misinterpreter (`replace_operator`, `flip_loop_bounds`, `remove_fallthrough`, ...);
* the top-level `reader` section: slot families (values, opposites, phrases,
  kinds), the English word lists and regex templates, the evidence class per
  rule type, the level per evidence class, and named roles.

`lexicon.py` loads this at import (and `KG(path)` reloads it for another graph
file). The engine keeps only Java mechanics: parsing, compiling and running,
the named analyses and transforms a graph can refer to. A new chapter is a new
graph file, not new code; `test_no_topic_tables_in_code` and
`test_engine_follows_the_graph` check this.

To grow the reader:

1. Run `python scripts/evaluate_lp_graph.py`; unmatched answer statements are
   in `output/eval/<tag>/`.
2. Add the wording to the graph: a phrase to `reader.slots.<slot>.values.<value>.phrases`,
   a word to a concept's `reader.aliases`, a code pattern to its
   `reader.code_patterns`, a misinterpreter to a misconception's `misread_as`.
3. Rerun `python scripts/prepare_kg_parts.py`, then `pytest -q`, then the evaluation.

`scripts/migrate_reader_layer.py` is the one-time migration that moved the
former code tables into the graph.

## Tests

`pytest -q` — reference case, three-statement case, print/println contrast,
determinism, PPR stability, consistency cap, non-stateable edges, static
definite-assignment check.
