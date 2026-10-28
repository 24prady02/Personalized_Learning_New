# ES-Viterbi Personalized Learning

Graph-traversal classifier for student answers on the Chapter-1 Java knowledge
graph: Personalized PageRank + ES-Viterbi, no LLM. See
[`src/lp_graph/README.md`](src/lp_graph/README.md) for the pipeline.

## Setup

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

A JDK (`javac`, `java`) is used when present to compile and run the code
snippet; without it the static checks still run and the result says
`code_check: unavailable` (or `static` when a static check decided).

## Layout

```
data/chapter1_kg.json        knowledge graph (source of truth, never edited)
data/kg_parts.json           derived reader data (scripts/prepare_kg_parts.py)
src/lp_graph/                the classifier
scripts/prepare_kg_parts.py  regenerate data/kg_parts.json
scripts/run_lp_graph_44.py   evaluate on the labelled scenarios -> output/lp_graph/
tests/test_lp_graph.py       pytest -q
```

## Commands

```bash
python scripts/prepare_kg_parts.py       # deterministic; prints coverage
pytest -q
python scripts/run_lp_graph_44.py        # needs the labelled scenarios (see the script docstring)
```
