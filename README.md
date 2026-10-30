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
  raw/scenarios_20.json         S000 reference case + the 10 gold scenarios whose gold concepts the code alone shows
  raw/scenarios_not_from_code.json  the other 10 gold scenarios (prose code, or a gold concept only the answer brings in)
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
with `fully covered: N / 10`. The dataset keeps the scenarios whose gold concepts the code alone shows
(S001, S007, S008, S021, S026, S047, S052, S057, S134, S137, plus the reference case S000): 10 / 10.
The other ten gold scenarios are kept in `data/raw/scenarios_not_from_code.json`: their "code" is prose or a
bare declaration (S009, S010, S012, S015, S068), or a gold concept comes only from the student's answer (the
while loop compared with a do-while in S005, division in S016, the missing `break` in S023 and S073, compiling
in S080). Run them with `--gold data/raw/scenarios_not_from_code.json`; misses there are expected (`xfail`).

## How the matcher works

1. `mask_java` blanks string / char literal contents and comments (same length, newlines kept).
2. `split_statements` splits on `;` `{` `}` at parenthesis depth 0, so a `for (…; …; …)` header stays whole.
3. For each concept's `reader` block: `code_patterns` (regex on the whole program), `signals` (regex, program or
   statement scope, masked or raw text; compiler-message signals without a regex are skipped), `operator_symbols`
   (substrings), `java_types` (whole words), `command_patterns` (regex on `java …` / `javac …` shell segments).
   Concepts with `code_visible: false` never tag. `aliases` are never used here.
4. `extract_subgraph`: the concept nodes are the concepts whose code patterns fired, **minus bare generic
   ones**. The KG marks 21 concepts `generic` (statement, identifier, literal, int, assignment, ...); they fire on
   almost any Java line. A generic concept is kept only when the code ties it to something specific: the KG
   has a prerequisite or parallel edge between it and a non-generic tagged concept (assignment stays next to
   variable_swap, string_literal next to println), or one of its own decisive signals fired (class_declaration
   with a file-name mismatch). This rule reads nothing but the KG, so it is the same for every snippet.
   `--keep-generic` keeps every tagged concept. Then `prerequisite` / `parallel` edges with both ends inside;
   `misconception` / `error` edges from the concepts; `has_level` edges with their ways; links from each way's
   `linked_misconception`. `--hops 1` optionally adds one prerequisite hop (off by default).
   The remaining extras relative to a scenario's gold are non-generic constructs really present in the code
   (the loop around S057's division, for instance); only the question and answer, read in a later stage, can
   say which of them the scenario is about.

## Recall audit: alternative spellings

`tests/data/recall_variants.json` holds 581 alternative Java spellings across the 166 code-visible concepts
(StdOut vs System.out, braces or none, one-line forms, other primitive types, Scanner vs StdIn, shell lines).
557 are asserted by `test_recall_variants`; the other 24 (`not_decidable`) cannot be decided from a snippet by
any regex: a type declared outside the snippet (`sum / n`, `long n = i`, `b = a`, `a == b`), operands of unknown
type (`String s = a + b`), an index of unknown value (`a[n]`), or unbalanced parentheses.
The audit added 77 general patterns and signals to the KG (see the next section); none changed the 20 scenarios'
node sets.

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
