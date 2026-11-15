# Think on the Graph

Diagnosing a student's answer about a short Java program by walking a knowledge graph. A subgraph is cut out of
the graph from the code alone; it is then walked against the student's answer, and the result is the wrong rules
held, the root cause and a level per concept.

The method has seven stages. This README and the README of every scenario use the same numbers and the same terms:

| Stage | What it does | Model | Code |
|---|---|---|---|
| 1 | from the code to a subgraph G: mask the code, tag concepts, handle generic concepts, cut out G | no | `src/preprocessing.py`, `src/model.py` |
| 2 | split the answer into clauses; choose the start concepts by BM25 | no | `src/traverse.py` |
| 3 | the traversal, a beam search over G: edge search, prune, label, score and keep, move, stop test | prune and label only | `src/traverse.py`, `src/prompts.py` |
| 4 | from labels to faults: error beside a misconception, one fault one place, shadows, broken edges | no | `src/traverse.py` |
| 5 | root cause | no | `src/traverse.py` |
| 6 | level of each concept (L0 to L4) | no | `src/traverse.py` |
| 7 | overall level | no | `src/traverse.py` |

The design of the knowledge graph is described under "How the knowledge graph was constructed" and "How a
learning-progression level attaches to a concept". Stage 1 is described under "Stage 1: what is being done", "How the matcher works" and "How the subgraph is taken
out"; Stages 2 to 7 under "Stages 2 to 7: the walk and the diagnosis".

## The 40 scenarios (MY01 to MY40)

The main scenario set is `data/raw/scenarios_40.json`: 40 short Java programs, each with a question and a student's
answer. They were entered and run one at a time in `scenario_explanations/think_on_the_graph.ipynb` (all seven
stages). They have no gold labels.

Every scenario has its own folder, `scenario_explanations/runs/MYnn/`:

| File | What it is |
|---|---|
| `README.md` | how the algorithm reached the result, stage by stage: each stage explained, with one output of that stage from the run |
| `MYnn.ipynb`, `report.html` | every output of every stage (all edges offered, every score and label, the figures) |
| `MYnn_G.html` | the interactive graph of the run |
| `input.json`, `subgraph.json`, `diagnosis.json`, `traverse_log.txt` | the input, the Stage 1 subgraph, the result of Stages 2 to 7 and the trace |
| `figureNN.png` | the pictures of the walk, depth by depth |

Results. In 29 of the 40 the walk holds at least one wrong rule; in 11 it holds none. The last
column is a reading of each stored result by hand against the student's answer (2026-11-13; the results that
changed in the re-runs of 2026-11-14 were read again), not a gold label:
35 correct, 3 partly right, 1 not right, 1 with a faulty input.

| Scenario | Wrong rules held | Root cause | Overall level | Check by hand |
|---|---|---|---|---|
| [MY01](scenario_explanations/runs/MY01/) | CastAfterIntDivision | `explicit_cast` | L0 | Correct |
| [MY02](scenario_explanations/runs/MY02/) | NegativeRemainderSign | `remainder_operator` | L0 | Correct |
| [MY03](scenario_explanations/runs/MY03/) | AssignmentCopiesObject | `array_aliasing` | L0 | Correct |
| [MY04](scenario_explanations/runs/MY04/) | SwitchNoFallThrough | `switch_statement` | L0 | Correct |
| [MY05](scenario_explanations/runs/MY05/) | CharNotNumeric | `char` | L0 | Correct |
| [MY06](scenario_explanations/runs/MY06/) | LoopBodyStatementOutsideLoop, LoopBodyScopeImpliesLoopLifetime | `loop_body` | L0 | Partly right |
| [MY07](scenario_explanations/runs/MY07/) | IntOverflowWidensAutomatically | `overflow` | L0 | Correct |
| [MY08](scenario_explanations/runs/MY08/) | none | none | L3 | Correct |
| [MY09](scenario_explanations/runs/MY09/) | TargetTyping | `integer_division` | L0 | Correct |
| [MY10](scenario_explanations/runs/MY10/) | ArrayIndexStartsAtOne, OutOfBoundsElementsAreNull | `indexing` | L0 | Correct |
| [MY11](scenario_explanations/runs/MY11/) | NestedLoopsSequential, LoopBodyStatementOutsideLoop, ForVariableScopeBeyondLoop | `nested_loops` | L0 | Correct |
| [MY12](scenario_explanations/runs/MY12/) | CharNotNumeric | `char` | L0 | Correct |
| [MY13](scenario_explanations/runs/MY13/) | CastAfterIntDivision | `explicit_cast` | L0 | Correct |
| [MY14](scenario_explanations/runs/MY14/) | LoopStepAlwaysOne | `for_loop` | L0 | Correct |
| [MY15](scenario_explanations/runs/MY15/) | IncrementByTwo, ForInitRepeats, ForUpdateBeforeBody, PreIncrementBeforeLoop | `for_loop` | L0 | Correct |
| [MY16](scenario_explanations/runs/MY16/) | CastAppliesToWholeExpression | `explicit_cast` | L0 | Correct |
| [MY17](scenario_explanations/runs/MY17/) | none | none | L4 | Correct |
| [MY18](scenario_explanations/runs/MY18/) | ArrayRangeInclusive, OffByOneBound, IdiomOverridesCode | `loop_control` | L0 | Correct |
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
| [MY40](scenario_explanations/runs/MY40/) | FewTrialsAreExact, ProbabilityIsPrediction | `frequency_counting` | L0 | Correct |

The five that are not simply correct:

| Scenario | What is wrong | Where it comes from |
|---|---|---|
| MY29 | the question and answer belong to the scenario before it, not to this program, so the result means nothing | the input |
| MY30 | the student takes `char + int` to be a letter; `CharNotNumeric` says something else | the graph has no misconception for it |
| MY19 | `TargetTyping` is right, but "7 % 2 is 0.5" is not picked up | the graph has no misconception for it |
| MY35 | the right error is found, but the overall level is empty | the graph has no misconception for "0 / 0 is 0", and the level rule sets L0 only for a misconception |
| MY06 | the fitting label, `LoopBodyScopeImpliesLoopLifetime`, is held but only second; the root went to a neighbour | how the root cause is chosen |

In MY26 and MY40 a line beginning "Actual:" had been pasted into the answer box, so it was read as part of the
student's answer. Both were run again on 2026-11-14 with only the student's own words. MY26 gives the same held rule
and root cause. MY40 now also holds FewTrialsAreExact at `frequency_counting`, which becomes the root cause;
ProbabilityIsPrediction is still held.

Notes on the set:

- **Numbering.** An exact repeat of MY18 was removed and the scenarios after it were renumbered, so MY26 to MY40 were
  MY27 to MY41 before. Commit messages before 2026-11-13 use the old numbers.
- **Code.** The notebook has no copy of the method. `think_on_the_graph.ipynb` imports `src/` and calls
  `model.subgraph_from_code` and `traverse.traverse` with the settings of `experiments/config.json`, as
  `src/demo.py` does; its own cells only draw and print. Running all 40 again from the cached model answers on the
  code and graph of this repository reproduces every stored result exactly (subgraph, held rules, root cause,
  levels).
- **Graph version.** All 40 stored runs are on graph 3.9.8, the graph in this repository. MY01 to MY25 were first run
  on 3.9.7, which differs for them only in the `primary` / `context` role of some misconception edges, and were run
  again on 2026-11-14 (MY26 and MY27 as well; they did not change). The re-run changed four results and left 23 as
  they were: MY05 and MY12 (CharNotNumeric is now filed at `char`, its primary concept, instead of
  `char_arithmetic`), MY18 (the root cause OffByOneBound is now at `loop_control` instead of `off_by_one_error`, and
  ArrayRangeInclusive and IdiomOverridesCode are held as well) and MY02 (`integer_division` is now L0).

## How the knowledge graph was constructed

The graph covers Chapter 1 of Sedgewick & Wayne, *Introduction to Programming in Java*, 1st ed. (sections 1.1 to 1.6), and was checked against the book and *Think Java*, 2nd ed. Every book quote in the graph is checked against these editions.

**What it holds** (`data/raw/chapter1_kg_updated.json`, v3.9.8):
- **Nodes:** 6 sections, 36 topics, 173 concepts, 255 misconceptions, 41 errors and 865 levels.
- **Edges:**
  - **contains** (209): section → topic → concept, where the book teaches it.
  - **prerequisite** (253): which concept must be learned before another, with the book passage.
  - **precedes** (5) and **section_prerequisite** (7): the order of the six sections, and which later section reuses an earlier one.
  - **parallel** (35): two concepts easily mixed up, and how they differ.
  - **misconception** (476) and **error** (93): the edge logic states the mistake, and the twin logic the correct rule.
  - **has_level** (865): concept → level L0 to L4. The edge logic lists the ways of reaching the level and the exact rule each way tests (3,079 ways).

### The rules of construction, and how the design satisfies them

Each rule starts from the exact words of a paper, turns them into a rule for the graph, and is applied to all the items it covers. The last column says which of four questions the rule helps answer, and how:

- **Q1.** "How do we validate ontologies."
- **Q2.** "To build java computer science concept inventories when it comes to learning progression analysis."
- **Q3.** "It is not traceable in the knowledge graph"
- **Q4.** "How do you handle ambiguity for that I have to look into the research."

| No. | Rule from the paper (exact words) | Rule for the graph | Applied to | Which question it answers, and how |
|---|---|---|---|---|
| 1 | “for target dimensions, accuracy, consistency, completeness, timeliness and redundancy are adopted for classfication” — Xue & Zou [89], p. 2 | Every concept has exactly one name. | 173 concepts | Q1: each book term maps to one named concept. Q4: one name, so two concepts are never confused. |
| 2 | “for target dimensions, accuracy, consistency, completeness, timeliness and redundancy are adopted for classfication” — Xue & Zou [89], p. 2 | Every concept has exactly one definition. | 173 concepts | Q2: the inventory states what each concept is. Q4: one definition, so its meaning is fixed. |
| 3 | “This is a response where the student manifests a correct grasp of some but not all aspects of the problem.” — Lister et al. [84], p. 2 | Every concept has exactly five levels (L0-L4). | 173 concepts | Q2: every concept has the full L0–L4 progression. |
| 4 | “(1) Establish topics. Determine the topics that are important to faculty members.” — Taylor et al. [90], p. 9 | Every concept is taught in exactly one topic. | 173 concepts | Q1: each concept sits where the book teaches it. Q2: the inventory follows the book’s topics. |
| 5 | “This is a response where the student manifests a correct grasp of some but not all aspects of the problem.” — Lister et al. [84], p. 2 | Every level code is one of L0, L1, L2, L3, L4. | 865 levels | Q2: all concepts use the same five levels. |
| 6 | “At the development stage, the researchers define the assessment construct” — Jin et al. [91], p. 6 | Every level has exactly one criterion. | 865 levels | Q2: each level is described before any student data. Q4: one criterion, so a level is read one way. |
| 7 | “At the development stage, the researchers define the assessment construct” — Jin et al. [91], p. 6 | Every level has one deciding question. | 865 levels | Q4: the deciding question settles an answer that sits between two levels. |
| 8 | “identity and unity are the most important philosophical notions we use in our methodology” — Guarino & Welty [92], p. 4 | Every level is attached to exactly one concept by a has_level edge. | 865 levels | Q2: each level belongs to one concept’s progression. Q3: every level traces to its concept through its has_level edge. |
| 9 | “At the development stage, the researchers define the assessment construct” — Jin et al. [91], p. 6 | Every way has one of the 13 rule categories. | 3,079 ways | Q2: every way is one of the 13 kinds of evidence for a level. |
| 10 | “At the development stage, the researchers define the assessment construct” — Jin et al. [91], p. 6 | Every way states one exact rule. | 3,079 ways | Q3: the way names the exact rule it tests. Q4: one rule, so the test has one reading. |
| 11 | “At the development stage, the researchers define the assessment construct” — Jin et al. [91], p. 6 | Every way states its edge logic, which is its exact rule. | 3,079 ways | Q2: says, by its exact rule, how an answer reaches the level. Q4: the evidence is stated, not guessed. |
| 12 | “This is a response where the student manifests a correct grasp of some but not all aspects of the problem.” — Lister et al. [84], p. 2 | The rule category of a way belongs to the level its edge points to (e.g. a tracing rule only at L2). | 3,079 ways | Q1: catches a way placed at the wrong level. Q2: keeps the order of the progression (tracing at L2, relating at L3). |
| 13 | “identity and unity are the most important philosophical notions we use in our methodology” — Guarino & Welty [92], p. 4 | Every way belongs to exactly one has_level edge. | 3,079 ways | Q3: each way traces to one concept and one level. Q4: a way cannot count for two levels. |
| 14 | “A programming language misconception is a statement that can be disproved by reasoning entirely based on the syntax and/or semantics of a programming language.” — Chiodini et al. [29], p. 2 | A misconception, inconsistent-trace or relation-to-neighbour way names the misconception or neighbouring concept it is about. | 1,070 ways of these three kinds | Q3: a way about a misconception or a neighbouring concept points to that node. |
| 15 | “A programming language misconception is a statement that can be disproved by reasoning entirely based on the syntax and/or semantics of a programming language.” — Chiodini et al. [29], p. 2 | Every misconception / error states one wrong belief. | 294 misconceptions and errors | Q2: each misconception in the inventory states its wrong belief. |
| 16 | “A programming language misconception is a statement that can be disproved by reasoning entirely based on the syntax and/or semantics of a programming language.” — Chiodini et al. [29], p. 2 | Every misconception / error states one correct rule. | 294 misconceptions and errors | Q2: each misconception states the correct rule. Q4: the right answer is fixed. |
| 17 | “A comprehensive list of validated misconceptions in some subject can be used to build formal evaluation methods like the Concept Inventory (CI)” — Caceffo et al. [28], p. 1 | Every misconception / error is linked to at least one concept. | 294 misconceptions and errors | Q2: misconceptions sit on the concepts they affect. Q3: each traces to a concept. |
| 18 | “A nanopublication is defined as a small data container consisting of three parts: an assertion part” — Kuhn et al. [93], p. 3 | Every meaningful edge carries edge logic. | 1,891 edges | Q3: every edge carries edge logic that says why it is there. |
| 19 | “A programming language misconception is a statement that can be disproved by reasoning entirely based on the syntax and/or semantics of a programming language.” — Chiodini et al. [29], p. 2 | Every misconception / error edge carries the correct rule (twin logic). | 564 misconception and error edges | Q2: each misconception edge states the correct rule (twin logic). Q3: the correction stays on the edge. |
| 20 | “For the evaluation of an ontology (however built) a major part of the evaluation should be to identify the 'fit' of the ontology with a domain specific corpus.” — Brewster et al. [94], p. 2 | Every prerequisite / parallel edge has a book quote or a stated grounding. | 241 prerequisite and parallel edges | Q2: prerequisite edges come with evidence. Q3: each prerequisite and parallel edge keeps its book quote or stated grounding. |
| 21 | “At the development stage, the researchers define the assessment construct” — Jin et al. [91], p. 6 | Every has_level edge states at least one way of reaching the level. | 865 has_level edges | Q2: every level has a has_level edge with at least one stated way. |
| 22 | “we attempted to articulate relationships and dependencies among the consensus goals that define potential pathways through the goals.” — Rich et al. [87], p. 4 | No prerequisite cycle. | 173 concepts | Q1: a cycle would make the prerequisite order impossible. Q2: the progression has a clear start. |
| 23 | “we attempted to articulate relationships and dependencies among the consensus goals that define potential pathways through the goals.” — Rich et al. [87], p. 4 | No parallel (contrast) edge on a prerequisite path. | 173 concepts | Q1: two concepts cannot be both parallel and on a prerequisite path. Q4: an edge has one meaning. |
| 24 | “we attempted to articulate relationships and dependencies among the consensus goals that define potential pathways through the goals.” — Rich et al. [87], p. 4 | No concept is its own prerequisite or contrast. | 173 concepts | Q1: no concept depends on itself. |
| 25 | “it pays too much attention to correctness and completeness and overlooks other issues such as timeliness and redundancy” — Xue & Zou [89], p. 2 | No redundant prerequisite (one already implied by a longer path). | 173 concepts | Q1: no redundant prerequisite edges, so the order stays minimal. |
| 26 | “unambiguity is based on whether an answer may have multiple interpretations” — Fowler et al. [88], p. 16 | Every way states its 'correct' check. | 3,079 ways | Q4: every way is checked to be correct. |
| 27 | “unambiguity is based on whether an answer may have multiple interpretations” — Fowler et al. [88], p. 16 | Every way states its 'unambiguous' check. | 3,079 ways | Q4: every way is checked to have only one reading. |
| 28 | “unambiguity is based on whether an answer may have multiple interpretations” — Fowler et al. [88], p. 16 | Every way states its 'high-level / scope' check. | 3,079 ways | Q4: every way is checked to be of the right scope for its level. |
| 29 | “for target dimensions, accuracy, consistency, completeness, timeliness and redundancy are adopted for classfication” — Xue & Zou [89], p. 2 | Every section has exactly one name. | 6 sections | Q1: each section matches a book section. Q4: one name each. |
| 30 | “(1) Establish topics. Determine the topics that are important to faculty members.” — Taylor et al. [90], p. 9 | Every section holds at least one topic. | 6 sections | Q1: no empty section, so every book section has content. |
| 31 | “for target dimensions, accuracy, consistency, completeness, timeliness and redundancy are adopted for classfication” — Xue & Zou [89], p. 2 | Every topic has exactly one name. | 36 topics | Q4: one name each, so topics are not confused. |
| 32 | “identity and unity are the most important philosophical notions we use in our methodology” — Guarino & Welty [92], p. 4 | Every topic sits in exactly one section. | 36 topics | Q1: matches the book’s structure. Q3: each topic traces to one section. |
| 33 | “(1) Establish topics. Determine the topics that are important to faculty members.” — Taylor et al. [90], p. 9 | Every topic holds at least one concept. | 36 topics | Q1: no empty topic. |

**How it is checked that the design satisfies every rule:**
- The graph is exported to RDF, and each rule runs as a SHACL shape over every item of its part (pyshacl).
- A negative test plants one break of each rule in a small graph and checks that SHACL reports it.
- All 33 rules hold (workbook sheet *Design rules*).

### How each concept is made

- It is named with the term the book uses where it teaches the construct, and given one definition quoted from the book with its page (rules 1–2).
- It is placed in the one topic where it is taught (rule 4).
- It gets its five levels L0–L4 (rule 3).
- Its prerequisite and parallel edges carry the book passage that states them (rule 20).
- Its misconceptions and errors carry the wrong rule and the correct rule (rules 15, 16, 19).
- It also holds regex patterns that recognise it in code, used by Stage 1 and tested on 372 snippets (`python src/train.py`).
- Each concept's view is drawn in `concept_wise_graph/<concept>/`. The chapter and section maps, with numbered edges and map keys, are in `Chapter1_KG_maps_and_keys.zip`.

**References for the construction** (numbers as in the notes):
- [14] Sedgewick & Wayne (2008), *Introduction to Programming in Java*, 1st ed.
- [81] Downey & Mayfield (2020), *Think Java*, 2nd ed.
- [84] Lister et al. (2006), ITiCSE '06.
- [88] Fowler et al. (2025), ACM TiiS 15(4).
- [89] Xue & Zou (2023), IEEE TKDE 35(5).
- [90] Taylor et al. (2014), *Computer Science Education* 24(4).
- [91] Jin et al. (2019), *IJSE* 41(10).
- [92] Guarino & Welty (2002), CACM 45(2).
- [93] Kuhn et al. (2016), PeerJ CS 2:e78.
- [94] Brewster et al. (2004), LREC.
- [28] Caceffo et al. (2019), ITiCSE '19.
- [29] Chiodini et al. (2021), ITiCSE '21.
- [87] Rich et al. (2017), ICER '17.

## How a learning-progression level attaches to a concept (from the workbook `Chapter1_KG_v3_9_7.xlsx`)

```
concept ──has_level──► concept@L0 … concept@L4      (5 level nodes per concept, 865 in all)
            └─ ways: each way = rule category + exact rule + boundary + source
                 L0 misconception way ──► misconception node it is about
                 L3 relation way      ──► neighbouring concept
```

### Many ways of reaching each level

A student can show the same level in different ways. One explains the rule, another traces the values, a third relates the construct to its neighbour. So a level is not one test but a set of **ways**, each a different kind of evidence. The workbook (sheets *Ways and rule categories*, *Rule category to level*) defines 13 ways, each tied to one rule category. Each concept has its own wording of every way that applies to it (sheet *Level edge Logic*, 3,079 rows).

| Level | Way | What the answer does | Boundary with the next level |
|---|---|---|---|
| **L0** | everyday reading (E) | reads the code with the everyday or maths meaning of its words | any correct, programming-specific statement makes it L1 or higher |
| | misconception (M) | applies a documented wrong rule that the language disproves | a single slip in an otherwise rule-correct trace is L2 with an error |
| | inconsistent trace (T) | applies the right rule at one place and a wrong rule at another in the same trace | a slip under one consistent, correct rule is L2 with an error |
| **L1** | names the element (N) | names or describes the construct correctly | covering every part of the code in order is L2 |
| | states the rule (S) | states the rule, without applying it to the values | applying it to this code's values is L2 |
| **L2** | line-by-line trace (LT) | executes each statement in order with its values | stating the purpose of the whole is L3 |
| | output prediction (OP) | gives the output and justifies it value by value | a bare correct output is not levelled |
| | one-step execution (OS) | gives the change one execution makes | one step of a longer fragment is L1 |
| **L3** | relation to a neighbour (R) | explains how the concept works with another construct in the same code | two separate correct rules are L1; running them in sequence is L2 |
| | purpose of the whole (P) | says what the code does for all inputs, deduced from the code | a purpose guessed from traced cases is L2 |
| **L4** | predict a change (C) | predicts what a change keeps or breaks, without re-tracing | re-tracing the changed code is L2 |
| | diagnose an error (D) | names the rule broken, the kind of error and the class of inputs that triggers it | fixing one given failing case is L3 |
| | transfer to a new program (X) | uses the construct in an unseen problem, knowing when it is the right tool | reproducing a familiar program is L1–L3 |

**How many ways each concept has:**
- **Once per concept:** everyday reading, names the element, states the rule, the three L2 ways, purpose of the whole, predict a change and transfer.
- **Once per related node:**
  - misconception: one per misconception attached to the concept;
  - relation to a neighbour: one per neighbouring concept;
  - diagnose an error: one per error or wrong rule it diagnoses.
- **Inconsistent trace:** at most one per concept (148 of the 173 have it).

So L1 always has 2 ways and L2 always 3, while L0 (1–20), L3 (2–11) and L4 (3–10) vary by concept.

**Example, `for_loop` (37 ways):**

| Level | Ways | One of them (exact rule) |
|---|---|---|
| L0 | 15: 1 everyday reading, 13 misconceptions, 1 inconsistent trace | misconception: "The initialization of a for loop runs again after a pass of the body." (right rule: it runs exactly once) |
| L1 | 2: names the element, states the rule | "for (<initialize>; <boolean expression>; <increment>) { <statements> }" |
| L2 | 3: trace, output prediction, one step | trace: "Run the initializer once; then repeatedly: test the condition (stop if false), execute the body, run the update." |
| L3 | 9: 8 relations, 1 purpose | relation to array indexing: "for (int i = 0; i < N; i++) gives i each valid index 0..N-1 exactly once" |
| L4 | 8: 1 predict a change, 6 diagnose an error, 1 transfer | diagnose: "A ; right after for (...) is an empty statement that is the whole loop body … silent logic error" |

**Reaching a level:**
- **One shown way is enough.** The student does not need every way of a level.
- **The answer's level is the highest level at which some way is shown,** because the levels are cumulative: an answer that relates the parts has also applied the rules.
- **L0 is the exception:** if a misconception way is shown (the wrong rule is held), the concept is L0 whatever else is shown.

### Source of every level, L0 to L4

The five levels are the SOLO levels for code (Lister et al., 2006) matched to the neo-Piagetian stages (Lister, 2011; Teague & Lister, 2014). Each level and each of its ways is mapped from the source below. The quotes are verbatim, with the PDF page.

**L0 Prestructural / sensorimotor.** No working model of the concept.
- Lister et al. 2006, p. 2: *"a student who gives a prestructural response is manifesting either a significant misconception of programming, or is using a preconception that is irrelevant to programming."*
- Teague & Lister 2014, p. 1: *"Novices who cannot trace code are working at the first stage, the sensorimotor stage."* and *"It is at this stage that misconceptions about basic programming concepts most influence the novice's behaviour"*

| Way | Source |
|---|---|
| everyday reading | Pea 1986, p. 2: *"programming is a formal system that interprets each part of a program … in terms of rules"*; Lister et al. 2006, p. 2 ("preconception that is irrelevant to programming") |
| misconception | ProgMiscon 2021, p. 2: *"A programming language misconception is a statement that can be disproved by reasoning entirely based on the syntax and/or semantics of a programming language."*; Teague & Lister 2014, p. 1 |
| inconsistent trace | Teague & Lister 2014, p. 1 (sensorimotor: "cannot trace code") |

**L1 Unistructural.** One correct aspect.
- Lister et al. 2006, p. 2: *"a response where the student manifests a correct grasp of some but not all aspects of the problem."*

| Way | Source |
|---|---|
| names the element | Lister et al. 2006, p. 2 |
| states the rule | Lister et al. 2006, p. 2 |

**L2 Multistructural / preoperational.** All parts, not related.
- Lister et al. 2006, p. 2: *"an understanding of all parts of the problem, but does not manifest an awareness of the relationships between these parts"*
- Teague & Lister 2014, p. 1: *"Novices who are working at the preoperational stage … can trace code but do not yet have a well-developed ability to reason about the code's purpose, other than by induction from input/output pairs."*
- Smith et al. 2025, p. 1: *"whether the student describes each line individually (many segments) or the code as a whole (fewer segments)."*

| Way | Source |
|---|---|
| line-by-line trace | Lister et al. 2006, p. 2; Teague & Lister 2014, p. 1; Sorva 2013, p. 2: *"the purpose of a notional machine is to explain program execution."* |
| output prediction | Lister et al. 2006, p. 2; Teague & Lister 2014, p. 1 |
| one-step execution | Sorva 2013, p. 2: *"A notional machine is a characterization of the computer in its role as executor of programs"*; Lister et al. 2006, p. 2 |

**L3 Relational / concrete operational begins.** The parts integrated.
- Lister et al. 2006, p. 2: *"the student integrates the parts of the problem into a coherent structure, and uses that structure to solve the task"*
- Smith et al. 2025, p. 1 (the code described as a whole, in fewer segments).

| Way | Source |
|---|---|
| relation to a neighbour | Lister et al. 2006, p. 2 |
| purpose of the whole | Lister et al. 2006, p. 2; Teague & Lister 2014, p. 1; Smith et al. 2025, p. 1 |

**L4 Extended abstract / concrete operational (conservation, reversibility).** Beyond the given code.
- Lister et al. 2006, p. 3: *"the student response goes beyond the immediate problem to be solved, and links the problem to a broader context."* For example, *"a comment that the code will only work for arrays that are sorted."*
- Lister 2011, p. 6: *"The archetypal manifestation of concrete thinking is the ability to reason about quantities that are conserved, and processes that are reversible."*

| Way | Source |
|---|---|
| predict a change | Lister 2011, p. 6; Lister et al. 2006, p. 3 |
| diagnose an error | Lister et al. 2006, p. 3 ("only work for arrays that are sorted"); Logic-errors survey (ASEE), p. 2: *"A logic error causes incorrect program execution, in contrast to a syntax error, which prevents execution."* |
| transfer to a new program | Lister et al. 2006, p. 3 |

**Where the sources disagree:**
- Jimoyiannis (2011) codes some misconception-driven answers at L1–L2, not L0.
- Jimoyiannis (2011) and Vrachnos & Jimoyiannis (2017) code modifying given code as L3, not L4.

**References**
- Lister, R., Simon, B., Thompson, E., Whalley, J., Prasad, C. (2006). Not seeing the forest for the trees: novice programmers and the SOLO taxonomy. *ITiCSE 2006*, 118–122.
- Lister, R. (2011). Concrete and other neo-Piagetian forms of reasoning in the novice programmer. *ACE 2011*, CRPIT 114, 9–18.
- Teague, D., Lister, R. (2014). Manifestations of preoperational reasoning on similar programming tasks. *ACE 2014*, CRPIT 148, 65–74.
- Pea, R. D. (1986). Language-independent conceptual "bugs" in novice programming. *J. Educational Computing Research* 2(1).
- Chiodini, L. et al. (2021). A curated inventory of programming language misconceptions (ProgMiscon). *ITiCSE 2021*. doi:10.1145/3430665.3456343
- Sorva, J. (2013). Notional machines and introductory programming education. *ACM TOCE* 13(2), Article 8.
- Smith, D. H. IV, Fowler, M., Denny, P., Zilles, C. (2025). LLM segmentation of Explain-in-Plain-English answers. *ITiCSE 2025*, arXiv:2503.12216.
- Common logic errors for programming learners: a three-decade literature survey. ASEE.
- Jimoyiannis, A. (2011). Using SOLO taxonomy to explore students' mental models of the programming variable and the assignment statement. *Themes in Science & Technology Education* 4(2), 53–74.
- Vrachnos, E., Jimoyiannis, A. (2017). *Themes in Science & Technology Education* 10(1).

### How the mapping works

**Stored in the graph, fixed before any answer is read:**
- Each level node has a criterion and a deciding question.
- Each `has_level` edge lists that level's ways, each with the concept's own exact rule (3,079 ways).
- An L0 misconception way names its misconception node, which joins a wrong belief to a level.

**Worked out from each answer, never stored in the graph:**
1. Each way is offered as an edge. The model says only whether the answer **shows** it, citing the student's clauses.
2. **L0** if a misconception is held on the concept, or only L0 ways are shown.
3. Otherwise the **highest level with a shown way**, since the levels are cumulative.
4. No evidence, no level.

A level always means one student, one concept, one answer.

**Example (MY01):** "The (double) cast turns the division into a decimal division" holds CastAfterIntDivision, so `explicit_cast` is at **L0**.

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
  processed/<sid>_diagnosis.json             output of Stages 2 to 7: held misconceptions, root cause, levels, paths, evidence, clause coverage, stop reason, prompts per step
src/
  preprocessing.py                           mask_java, split_statements, command_segments, Prepared
  model.py                                   tag_code (pattern channels of every concept) + extract_subgraph / subgraph_from_code
  train.py                                   builds and checks the pattern bank (no learned parameters; see below)
  evaluate.py                                runs the scenarios: processed JSON, coverage report, figures, summary.csv, results.md, metrics.json
  utils.py                                   paths, load_kg, load_scenarios, reader_blocks, gold_concepts (check only), regex cache
  traverse.py                                Stages 2 to 7: ToG traversal over a Stage 1 subgraph (reads question + answer), writes <sid>_diagnosis.json
  prompts.py                                 the Stage 3 prompts: one edge prune, three edge labels (misconception edge, concept edge, level way); the only places the model is asked
  compare.py                                 the diagnoses vs gold (checking only): results/tables/stage2_vs_gold.csv, results/stage2_results.md
  demo.py                                    all seven stages on one scenario, with the step report and the page of the run
  steps_report.py, viz.py                    the step report of a run (results/viewer/<sid>_steps.md) and its figures
  upload.py                                  builds scenario_explanations/runs/<sid>/ for a run and commits it
  concept_notebooks.py                       runs one notebook per concept and writes concept_wise_graph/<concept>/
scenario_explanations/
  think_on_the_graph.ipynb                   enter a program, a question and an answer; runs all seven stages and shows every step
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
  logs/subgraph_report.txt                   one line per scenario over tests/data/scenarios_gold.json, "fully covered: 30 / 30"
  logs/subgraph_report_not_from_code.txt     the same over scenarios_not_from_code.json (misses expected)
  logs/traverse_<sid>.txt                    trace of Stages 2 to 7: start ranking, candidates, kept edges, labels, clauses, clause coverage, levels
  llm_cache/<hash>.json                      every prompt sent in Stage 3 and the model's reply (re-runs are free and deterministic)
results/
  results.md                                 summary table, then per scenario: code, figure, concept nodes, edges with logic, misconception nodes, level counts
  figures/<sid>.png                          node visualization of each subgraph
  tables/summary.csv                         one row per scenario (counts, concept ids, edges traced, misconception node ids)
  metrics.json                               coverage and size metrics
  stage2_results.md, tables/stage2_vs_gold.csv   the diagnoses against the gold (checking only)
  viewer/<sid>_steps.md, _demo.html, _G.html, _figureNN.png   the step report, page, interactive graph and figures of each run
paper/
  main.tex, references.bib, main.pdf         mid-term progress report (ACM format)
  figures/                                   figures used by the paper
slides/
  Pradhyumn_Nair_midterm_slides.pptx         mid-term presentation
tests/
  test_subgraph.py                           Stage 1 (228 tests)
  test_traverse.py                           Stages 2 to 7 with a mocked model (19 tests, 1 skipped)
  data/scenarios_gold.json                   the earlier gold-labelled set, used by the tests and by compare.py
  data/concept_pattern_tests.json            must_tag / must_not_tag snippets for all 166 code-visible concepts
```

## Commands

```bash
pytest -q                      # 247 tests (the tests of Stages 2 to 7 use a mocked model, no real call)
python src/train.py            # compile every pattern, check the 372 labelled snippets, write experiments/pattern_bank.json
python src/evaluate.py --scenarios tests/data/scenarios_gold.json --log experiments/logs/subgraph_report.txt
                               # Stage 1 on the gold-labelled set: data/processed, the report, results/ (figures, summary.csv, results.md, metrics.json)
python src/evaluate.py --scenarios data/raw/scenarios_not_from_code.json --no-figures --no-json
jupyter notebook scenario_explanations/explore_subgraph.ipynb
python src/traverse.py MY07      # Stages 2 to 7 on one scenario (needs the claude CLI, or `--backend anthropic` with the SDK and a key)
python src/traverse.py --all     # every scenario of the scenario file (cached replies are reused; anything else is asked again)
python src/compare.py            # the diagnoses of tests/data/scenarios_gold.json against its gold (checking only)
python src/demo.py --scenario MY07   # all seven stages on one of the 40 scenarios, with its step report
python src/concept_notebooks.py      # one notebook per concept into concept_wise_graph/ (or name concepts to run only those)
scenario_explanations\start_notebook.bat   # open think_on_the_graph.ipynb to run a new scenario
```

Without `--scenarios`, `evaluate.py`, `traverse.py` and `demo.py` read the scenario file named in
`experiments/config.json`, which is the 40 scenarios. `evaluate.py` and `traverse.py` then write over the stored
`data/processed/MYnn_subgraph.json` and `MYnn_diagnosis.json` of those runs, so use them on the 40 only to re-run
them on purpose.

## Stages 2 to 7: the walk and the diagnosis (`traverse.py`, `prompts.py`)

These stages read the question and the student's answer and walk the Stage 1 subgraph G the way Think-on-Graph
walks a knowledge graph. The stage numbers and terms are those of the scenario READMEs
(`scenario_explanations/runs/MYnn/README.md`), which explain each stage in plain words with one output of the run;
this section adds the detail of the code. Settings are in the `traversal` block of `experiments/config.json`
(width N = 3, depth D = 3, model, prune tool llm / bm25 / sentencebert).

The model is asked in Stage 3 only, and there in two places: the edge prune (3.2, replaceable by BM25 /
sentence-BERT) and the edge label (3.3). The start concepts, the stop test, the faults, the root cause and the
levels are rules with no model call.

### Stage 2. Clauses and start concepts (no model)

- **2.1 Clauses.** Quote characters are removed, then the answer is split at sentence ends, at `;`, and before
  `because` / `so` (after a comma, a space or a closing quote); a parenthetical remark of two or more words becomes
  its own clause. `/` is kept: inside a written output it is a line break. The clauses are numbered c1, c2, …
- **2.2 Start concepts.** The candidates are every non-generic concept of G, that is, the concepts Stage 1 tagged
  in the code, plus a generic concept whose tagging text occurs verbatim in the answer (the student names it in
  code, e.g. `=` for assignment in "a = b"). When there are more than N, they are ranked by BM25 of the student's
  answer against each concept's text (its id with underscores as spaces plus the texts of its misconception and
  concept edges), ties broken by the number of Stage 1 code hits, then by id. The top N are the start concepts.

### Stage 3. The traversal: walking G (the model is asked here)

A beam search of width N over at most D depths plus one closing round. At each depth, for each current concept:

- **3.1 Edge search** (no model). A concept that has just been entered is read inwards, in two families: its
  misconception and error edges, and its **level ways**. Every way of a has_level edge in the graph is an edge of
  its own (`lvl:<concept>@<L>#i`, logic = the way's exact rule); ways of kind "misconception" are left out because
  the misconception edges already carry them. A concept already read inwards is read outwards: its prerequisite /
  parallel edges inside the same connected piece. An edge is offered once, not from each of its ends; primary role
  first. A level way leads nowhere: it describes the concept itself.
- **3.2 Prune** (model, first question). One call per concept and family picks up to N edges the answer engages
  with; the scores are rescaled to sum to 1 (the prune score), or BM25 / sentence-BERT similarity is used instead
  of the call. Pruning each family on its own means a level way never competes with a misconception edge for a
  place. Edge ids the model invents are ignored.
- **3.3 Label** (model, second question). The pruned misconception / error edges of a concept are judged together
  in one call, one reply line per edge: held / correct / not applied, each shown with its wrong rule and its right
  rule (the twin). Judging them side by side lets the model give held to the rule whose claim the student actually
  makes when several wrong rules would fit the same words, and still hold two when the student holds two (held
  means the answer follows the wrong rule in what sets it apart from the right rule: where the student gives a
  reason it must be this rule's own, a result the rule would also predict but reached by another reason does not
  hold it, and a rule about something neither the program nor the answer contains is not applied). The other edges
  get one call each: confirmed / broken / not applied for a concept edge shown with its logic; shown / not shown
  for a level way shown with the concept, the way's name and what an answer that shows the way does, and nothing
  else: no level name, no deciding question, no level in an id, so the way is judged against its own text like
  every other edge and its level comes only from where it sits in the graph. Every reply gives the clause numbers
  it rests on and a confidence from 0 to 1. The evidence is clause numbers, not a free quote, so the code knows
  exactly which words each label rests on, and two labels on the same clause are known to rest on the same words.
  A label with no clause behind it is not applied.
- **3.4 Score and keep.** Score = prune score × confidence. The best N are kept in tiers: tier 0, held
  misconceptions and broken edges, always kept; tier 1, held errors; tier 2, correct / confirmed / shown edges,
  which fill what is left of the N places, best score first (an edge reached from both ends in one round counts
  once). Confirmations therefore never crowd out a finding. Kept edges are added to the paths. Every labelled edge,
  kept or not, is recorded as **evidence**, so a dropped "correct" label still explains its clause and the levels
  of Stage 6 are read from all of it.
- **3.5 Move to the next concepts.** The far end of each kept concept edge is entered, so its own misconception
  edges and level ways are read at the next depth and it gets a level of its own; the concept of each held
  misconception stays current, so that its prerequisites are examined (to walk back); and every entered concept
  whose concept edges are unread stays current until they are read.
- **3.6 Stop test** (no model). (i) Graph check: every concept the walk has entered has had its concept edges, the
  prerequisite and parallel links to the other concepts of its piece, read. For a faulted concept that is where
  the root cause lies; for a concept the student got right it is the conceptual trace, the confirmed links between
  concepts, which is as much part of the diagnosis as the faults. (ii) Clause coverage: a clause is covered when a
  labelled rule edge names it (a misconception / error edge labelled held or correct, a concept edge labelled
  confirmed or broken). A shown level way does not count here: it says how the student reads the code, not which
  rule the clause applies. The walk stops with reason "sufficient" when both hold, and with "half_stop" when no
  concept is left to go to. When clauses remain uncovered (up to depth D), they bring in concepts the walk has not
  entered yet: BM25 of those clauses against the unvisited concepts of the start pool, the best N, no model call.
  This has its own cap of N, so it does not compete with the concepts already waiting to be read, and it is what
  lets a correct multi-concept answer, whose labels give no direction of their own, reach every concept the
  student wrote about. Otherwise the walk goes on to depth D, followed by one **closing round** in which the
  concepts entered last have their misconception edges and level ways read (reason "max depth"). The clauses no
  evidence covers are reported as unexplained.

Every prompt and reply is cached in `experiments/llm_cache/` by the exact text of the prompt, so a re-run asks only
the prompts that changed and gives the same result.

### Stage 4. From labels to faults (rules, no model)

Each kept edge labelled held is a candidate fault. Nothing is deleted from the record; the rules decide what counts.

- **Error beside a misconception.** A held error beside a held misconception on the same concept is evidence
  (`error_evidence`), not a second fault.
- **Several misconceptions.** Every held misconception stays: a student can hold several at once, and the judgement
  was made at the label step, edge by edge. A held misconception resting on the same clauses as a stronger one on
  the same concept is marked `shares_evidence_with` that edge (the graph words one wrong idea in several ways, e.g.
  IfConditionWatched / IfWaitsForCondition on if_statement; both come out held, and the comparison with the gold
  counts the pair as one).
- **One fault, one place.** The same misconception held at both ends of a prerequisite edge is filed once: at the
  concept the graph marks as `primary` for it when the roles decide, and otherwise at the dependent concept.
- **Shadows.** A held label on a prerequisite or on a generic concept that rests only on the clauses of a stronger,
  more specific label is a shadow of that label: it is listed under `shadowed`, is not a fault, cannot be the root
  cause and sets no level.
- **Broken edges.** A broken A → B says the student did not carry A into B, so the fault sits at B. A broken edge
  resting on the same clauses as a held misconception is that misconception's consequence (`consequence_of`), not
  a fault of its own.

### Stage 5. Root cause (rule, no model)

From each concept with a fault the prerequisite edges of G are walked backwards; whenever a concept reached that
way has a fault of its own (a held misconception, or it is the target of a broken prerequisite edge that is not a
consequence), the candidate moves back to it. Between the candidates the one with the fewest prerequisites of its
own in G is taken, and at a tie the one whose label has the higher confidence. Alphabetical order never decides.

### Stage 6. Level of each concept (rule, no model)

The model is never asked for a level; it only said in 3.3 whether a way was shown. A concept is L0 when a fault is
kept on it (the level then reads the edge of that misconception and carries the L0 way's own text from
`level_mis_links` as `rule`) or when the only ways shown on it are L0 ways (everyday reading, inconsistent trace).
Otherwise it gets the highest level with a shown way, because the levels are cumulative and an answer at L4 also
does L3. A concept with no fault and no shown way gets no level. A held error node sets no level.

### Stage 7. Overall level (rule, no model)

The root-cause concept's level. For an answer with no fault, the level reached on at least half of the concepts the
answer touched (the levels sorted from high to low, the middle one). Because a held error sets no level, the
overall level is empty when the root cause carries only an error (MY35).

The output (`<sid>_diagnosis.json`) also lists the evidence, which edge covers each clause, the uncovered clauses,
the stop reason (sufficient / half_stop / max depth) and the number of prompts per step (prune, label). The model
never answers from its own knowledge: every label is an edge of the graph plus the clauses of the answer it rests
on.

Results over the 27 gold-labelled scenarios that have a stored diagnosis (`python src/compare.py`, full table in
`results/stage2_results.md`; gold is used for checking only): held misconception set right in 27/27, every gold
"correct" misconception found in 24/27 (not in S026, S047, S057), root cause right in 26/27 (not in T017), overall
level right in 25/27 (not in S052, T019), 148 of 191 points (one point each for held set, correct set, root cause
and overall level, plus one per gold-scored concept level and per gold edge), 839 prompts in all, every one of
them a prune or a label. S134 is found through the generic-concept rule: its only tagged concept is
variable_swap, the gold misconception (VariablesHoldExpressions) sits on assignment, which Stage 1 marks generic,
and the answer repeats the `=` that tagged it. On S007 the held set is exact (OffByOneBound at loop_control, root
cause loop_control, L0). One of the two overall-level misses is S052, L3 where the gold says L2: the student's "an
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
   nodes over the concept edges. When there is more than one piece a warning names them. Six of the eleven S
   subgraphs (20 of all 31) fall into several pieces because the KG has no edge between concepts that occur together
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

Current run over the earlier gold-labelled set (`tests/data/scenarios_gold.json`). The eleven S scenarios are shown
here; all 31, with the twenty T scenarios, are in `results/tables/summary.csv`:

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
pieces, and the gold concepts not found) and ends with `fully covered: N / 30`; `results/metrics.json` holds
the same as numbers (mean gold-concept recall, share of gold among the nodes, mean sizes, subgraphs in one piece). On the earlier gold-labelled set (`tests/data/scenarios_gold.json`) every gold
concept of all thirty scenarios is found from the code: 30 / 30 (S000 is the reference case and is not counted). The extra nodes relative to gold are
non-generic constructs really present in the code (the loop around S057's division, for instance); only the
question and answer, read in a later stage, can say which of them a scenario is about.

The other ten scenarios are kept in `scenarios_not_from_code.json` because code alone cannot produce their
gold concepts: the "code" is prose or a bare declaration (S009, S010, S012, S015, S068), or a gold concept
comes only from the student's answer (the while loop compared with a do-while in S005, division in S016, the
missing `break` in S023 and S073, compiling in S080). Running the report on that file marks those misses
`xfail`.

## Tests (`pytest -q`, 247 passing: 228 for Stage 1, 19 for Stages 2 to 7)

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
