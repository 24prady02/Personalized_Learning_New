# Think on the Graph

Stage 1: subgraph extraction from code only.

## What is being done

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
  raw/chapter1_kg.json                       knowledge graph v3.9.5-reader4 (173 concepts, 1896 edges, 296 misconception/error records, 865 level nodes)
  raw/scenarios_20.json                      S000 reference case + the 10 scenarios whose gold concepts the code alone shows
  raw/scenarios_not_from_code.json           the other 10 scenarios (prose code, or a gold concept only the answer brings in)
  processed/<sid>_subgraph.json              one extracted subgraph per scenario (output of src/evaluate.py)
  processed/<sid>_diagnosis.json             Stage 2 output: held misconceptions, root cause, levels, paths, stop reason (src/traverse.py)
src/
  preprocessing.py                           mask_java, split_statements, command_segments, Prepared
  model.py                                   tag_code (pattern channels of every concept) + extract_subgraph / subgraph_from_code
  train.py                                   builds and checks the pattern bank (no learned parameters; see below)
  evaluate.py                                runs the scenarios: processed JSON, coverage report, figures, summary.csv, results.md, metrics.json
  utils.py                                   paths, load_kg, load_scenarios, reader_blocks, gold_concepts (check only), regex cache
  traverse.py                                Stage 2: ToG traversal over a Stage 1 subgraph (reads question + answer), writes <sid>_diagnosis.json
  prompts.py                                 the four Stage 2 prompts: edge prune, edge label, sufficiency check, level ladder
notebooks/
  explore_subgraph.ipynb                     step through one scenario: code, masked code, hits, subgraph, figure
experiments/
  config.json                                default paths and extractor settings (hops 0, keep_generic false)
  pattern_bank.json                          the compiled pattern bank summary written by train.py (the model "checkpoint")
  logs/train_log.txt                         pattern compile + pattern-test check
  logs/subgraph_report.txt                   one line per scenario over scenarios_20.json, "fully covered: 10 / 10"
  logs/subgraph_report_not_from_code.txt     the same over scenarios_not_from_code.json (misses expected)
  logs/traverse_<sid>.txt                    Stage 2 trace: candidates, kept edges, labels, quotes, sufficiency, levels
  llm_cache/<hash>.json                      every prompt sent in Stage 2 and the model's reply (re-runs are free and deterministic)
results/
  results.md                                 summary table, then per scenario: code, figure, concept nodes, edges with logic, misconception nodes, level counts
  figures/<sid>.png                          node visualization of each subgraph
  tables/summary.csv                         one row per scenario (counts, concept ids, edges traced, misconception node ids)
  metrics.json                               coverage and size metrics
paper/
  main.tex, references.bib, main.pdf         mid-term progress report (ACM format)
  figures/                                   figures used by the paper
slides/
  Pradhyumn_Nair_midterm_slides.pptx         mid-term presentation
tests/
  test_subgraph.py                           pytest -q  (208 tests)
  data/concept_pattern_tests.json            must_tag / must_not_tag snippets for all 166 code-visible concepts
```

## Commands

```bash
pytest -q                      # 208 tests
python src/train.py            # compile every pattern, check the 372 labelled snippets, write experiments/pattern_bank.json
python src/evaluate.py         # data/processed, experiments/logs/subgraph_report.txt, results/ (figures, summary.csv, results.md, metrics.json)
python src/evaluate.py --scenarios data/raw/scenarios_not_from_code.json --no-figures --no-json
jupyter notebook notebooks/explore_subgraph.ipynb
python src/traverse.py S007      # Stage 2 on one scenario (needs the claude CLI, or `--backend anthropic` with the SDK and a key)
```

## Stage 2: ToG traversal (`traverse.py`, `prompts.py`)

Stage 2 reads the question and the student's answer and walks the Stage 1 subgraph the way Think-on-Graph walks
a knowledge graph. Settings are in the `traversal` block of `experiments/config.json` (width N = 3, depth D = 3,
model, prune tool llm / bm25 / sentencebert). Start concepts are all non-generic concept nodes; the answer is
split into clauses. At each depth, for each current concept: list its edges (depth 1 misconception / error
edges, deeper the prerequisite / parallel edges inside the same piece), prune to N with one model call (or by
similarity), label each kept edge with one call (held / correct / not applied for a misconception edge,
confirmed / broken / not applied for a concept edge, with a verbatim quote and a confidence; a quote not found in
the answer makes the label not applied), keep the best N by prune score × confidence, ask once whether the paths
explain every clause and the root cause, and continue from the source of held misconceptions and the far end of
concept edges. The diagnosis lists the held misconceptions, broken edges, the root cause (furthest back along
prerequisite edges), a level per concept on a path (from level_mis_links when a held misconception is linked,
otherwise one level-ladder call), the overall level, unexplained clauses, the stop reason and the call count.
The model never answers from its own knowledge: every label is an edge of the graph plus a quote.

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

Current run over `scenarios_20.json`:

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
the same as numbers (mean gold-concept recall, share of gold among the nodes, mean sizes, subgraphs in one piece). On `scenarios_20.json` every gold
concept of all ten scenarios is found from the code: 10 / 10. The extra nodes relative to gold are
non-generic constructs really present in the code (the loop around S057's division, for instance); only the
question and answer, read in a later stage, can say which of them a scenario is about.

The other ten scenarios are kept in `scenarios_not_from_code.json` because code alone cannot produce their
gold concepts: the "code" is prose or a bare declaration (S009, S010, S012, S015, S068), or a gold concept
comes only from the student's answer (the while loop compared with a do-while in S005, division in S016, the
missing `break` in S023 and S073, compiling in S080). Running the report on that file marks those misses
`xfail`.

## Tests (`pytest -q`, 208 passing)

- masking keeps length and blanks literals and comments; statement splitting keeps a `for` header whole;
  shell segments are cut correctly;
- every one of the 166 code-visible concepts has must_tag / must_not_tag snippets and passes them; the 7
  code-invisible concepts never tag;
- the matcher stays fast on long inputs (per-regex time limit, best of three runs);
- the S007 subgraph has the expected nodes, edges, misconception edges and levels; 23 small task snippets tag
  the right concepts;
- every gold concept of every scenario in `scenarios_20.json` is found, and the concept nodes are exactly
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
