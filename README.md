# Subgraph extraction from code only

First stage of the Chapter-1 Java pipeline: read a scenario's **Java code** (nothing else),
match the regex patterns stored on each concept node of the knowledge graph, and take out the
subgraph: concept nodes, the edges between them, their misconception / error nodes and edges,
their level nodes L0–L4 with the `has_level` edges, and the level ↔ misconception links.

Not in this stage: the question, the student's answer, PageRank, NLI, Viterbi, embeddings, LLMs,
edge selection, level decisions.

## Setup

```bash
pip install -r requirements.txt     # pytest only; the code uses the standard library
```

## Layout

```
README.md
requirements.txt
data/
  raw/chapter1_kg.json          knowledge graph v3.9.5-reader4 (173 concepts, reader layer with code patterns)
  raw/scenarios_20.json         S000 reference case + the 20 student scenarios (code, question, answer, gold labels)
  processed/<sid>_subgraph.json one extracted subgraph per scenario (output of the report CLI)
src/lp_graph/subgraph/
  mask.py                       mask_java, split_statements
  tagger.py                     tag_code, command_segments
  extract.py                    extract_subgraph, subgraph_from_code
  report.py                     python -m lp_graph.subgraph.report
notebooks/                      exploration (empty)
experiments/logs/               subgraph_report.txt
slides/                         (empty)
tests/
  test_subgraph.py              pytest -q
  data/concept_pattern_tests.json  must_tag / must_not_tag snippets for all 166 code-visible concepts
```

## Commands

```bash
pytest -q
PYTHONPATH=src python -m lp_graph.subgraph.report --kg data/raw/chapter1_kg.json --gold data/raw/scenarios_20.json --json data/processed
```

The report prints one line per scenario (concepts tagged, subgraph counts, gold concepts missed) and ends
with `fully covered: N / 20`. Misses marked `xfail` are gold concepts that the code does not show and only the
question or the student's answer brings in: prose or one-line "code" (S009, S010, S012, S015, S068), the while
loop a student compares a do-while with (S005), division in a program that only uses `%` (S016), the missing
`break` in a fall-through switch (S023, S073), and compiling a program whose code only says how to run it (S080).
Current result: 10 / 20 fully covered from code alone, 20 / 20 with no unexpected miss.

## How the matcher works

1. `mask_java` blanks string / char literal contents and comments (same length, newlines kept).
2. `split_statements` splits on `;` `{` `}` at parenthesis depth 0, so a `for (…; …; …)` header stays whole.
3. For each concept's `reader` block: `code_patterns` (regex on the whole program), `signals` (regex, program or
   statement scope, masked or raw text; compiler-message signals without a regex are skipped), `operator_symbols`
   (substrings), `java_types` (whole words), `command_patterns` (regex on `java …` / `javac …` shell segments).
   Concepts with `code_visible: false` never tag. `aliases` are never used here.
4. `extract_subgraph`: the concept nodes are **exactly the concepts whose code patterns fired**, nothing else.
   Then `prerequisite` / `parallel` edges with both ends inside; `misconception` / `error` edges from the
   concepts; `has_level` edges with their ways; links from each way's `linked_misconception`.
   `--hops 1` optionally adds the source of each incoming prerequisite edge of a non-generic tagged concept
   (one hop, never from generic concepts); it is off by default because it adds nodes the code did not show.
   Concepts the KG marks `generic` (statement, variable, int, assignment, ...) are kept but flagged, and the
   report shows their count per scenario.

## Pattern fixes made in the KG (v3.9.5-reader4)

Every fix is listed in `kg["reader"]["pattern_fixes_reader4"]` with the old and new regex, and each touched
reader block carries `patterns_fixed_in`. Found by running all 166 concepts over the 361 test snippets and the
20 scenarios and reading every cross-fire.

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
