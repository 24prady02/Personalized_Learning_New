"""Tests for Stage 2 (traverse.py) with a mocked LLM: no real model call is made here."""
from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

import pytest

import traverse
from traverse import DEFAULT_TRAVERSAL, STEPS, Graph, covered_clauses, select_start, split_clauses
from utils import load_scenarios

ROOT = Path(__file__).resolve().parents[1]
SCENARIOS = {s["id"]: s for s in load_scenarios(ROOT / "data/raw/scenarios_20.json")}
S007_ANSWER = SCENARIOS["S007"]["answer"]
S007_CLAUSES = ["3 2 1 / 2 1 / 1", "no empty line at the end", "because the loop stops at 1"]


# ---------------------------------------------------------------- mocks

class ScriptedLLM:
    """Answers every prompt from a script (prompt -> reply) and counts prompts per step."""

    model, backend = "mock", "mock"

    def __init__(self, script):
        self.script = script
        self.calls = 0
        self.cache_hits = 0
        self.asks_by_step: Counter = Counter()
        self.prompts: list[tuple[str, str]] = []

    def ask(self, prompt: str, step: str = "other") -> str:
        self.asks_by_step[step] += 1
        self.calls += 1
        self.prompts.append((step, prompt))
        return self.script(prompt)


class ReplayLLM(traverse.LLM):
    """The real client with the backend disabled: replies come from experiments/llm_cache only."""

    def _cli(self, prompt):
        raise pytest.skip.Exception("prompt not in experiments/llm_cache; run `python src/traverse.py S007` to record it")

    def _anthropic(self, prompt):
        return self._cli(prompt)


def _edge_ids(prompt: str) -> list[str]:
    return re.findall(r"^- ((?:mis|err|pre|par):\S+) \|", prompt, re.M)


def make_script(labels: dict[str, tuple[str, str]]):
    """labels: edge id -> (label, quote). The prune reply picks every candidate edge with equal scores."""
    def script(prompt: str) -> str:
        if "Candidate edges of this concept" in prompt:
            ids = _edge_ids(prompt)
            return "\n".join(f"{{{e} (Score: {1 / len(ids):.3f})}}" for e in ids)
        if "learning-progression ladder" in prompt:
            return "Level: L1\nWay: mock\nQuote: none"
        m = re.search(r"Edge: (\S+)", prompt)
        label, quote = labels.get(m.group(1), ("not applied", "none"))
        return f"Label: {label}\nQuote: {quote}\nConfidence: 0.9"
    return script


# A -pre-> B -pre-> C; misconceptions on B and C; G generic (its tagging text does not occur in the answer).
TINY = {
    "scenario": "T001",
    "concepts": [
        {"id": "A", "generic": False, "hits": [{"match": "int"}]}, {"id": "B", "generic": False, "hits": [{"match": "int"}, {"match": "x"}]},
        {"id": "C", "generic": False, "hits": [{"match": "int"}]}, {"id": "G", "generic": True, "hits": [{"match": "{"}, {"match": "int"}]},
    ],
    "concept_edges": [
        {"id": "pre:A->B", "source": "A", "target": "B", "type": "prerequisite", "logic": "A before B"},
        {"id": "pre:B->C", "source": "B", "target": "C", "type": "prerequisite", "logic": "B before C"},
    ],
    "misconceptions": [{"id": m, "type": "misconception"} for m in ("MisB", "MisB2", "MisC", "MisC2")],
    "mis_edges": [
        {"id": "mis:B->MisB", "source": "B", "target": "MisB", "type": "misconception", "role": "primary", "logic": "wrong B", "twin_logic": "right B"},
        {"id": "mis:B->MisB2", "source": "B", "target": "MisB2", "type": "misconception", "role": "secondary", "logic": "wrong B2", "twin_logic": "right B2"},
        {"id": "mis:C->MisC", "source": "C", "target": "MisC", "type": "misconception", "role": "primary", "logic": "wrong C", "twin_logic": "right C"},
        {"id": "mis:C->MisC2", "source": "C", "target": "MisC2", "type": "misconception", "role": "secondary", "logic": "wrong C2", "twin_logic": "right C2"},
    ],
    "levels": [], "level_edges": [],
    "level_mis_links": [{"level_node": "B@L0", "misconception": "MisB"}, {"level_node": "C@L0", "misconception": "MisC"}],
    "components": [["A", "B", "C", "G"]],
}
TINY_SC = {"id": "T001", "code": "int x;", "question": "What prints?", "answer": "It prints 0; because x is unset."}
CFG = {**DEFAULT_TRAVERSAL, "width": 3, "depth": 3}


def test_the_model_is_asked_in_three_places_only():
    assert STEPS == ("prune", "label", "level")
    import prompts
    assert not hasattr(prompts, "START") and not hasattr(prompts, "SUFFICIENCY")


# ---------------------------------------------------------------- 1. clause split

def test_split_clauses_s007():
    assert split_clauses(S007_ANSWER) == S007_CLAUSES


def test_split_clauses_rules():
    assert split_clauses('"Yes", because x is 1. So it stops; done') == ["Yes", "because x is 1", "So it stops", "done"]
    assert split_clauses("Cast (double) a / b gives 0.5") == ["Cast (double) a / b gives 0.5"]   # one-word parenthesis stays
    assert split_clauses("a / b (integer division) is 0") == ["a / b", "integer division", "is 0"]


# ---------------------------------------------------------------- 2. start concepts from Stage 1

def test_start_no_llm_no_generic_at_most_n_deterministic():
    g = Graph(TINY)
    runs = [select_start(g, TINY_SC["answer"], 2, []) for _ in range(3)]
    assert all(r == runs[0] for r in runs)
    assert len(runs[0]) == 2 and "G" not in runs[0]
    assert select_start(g, TINY_SC["answer"], 3, []) == ["A", "B", "C"]   # <= N: all tagged concepts


def test_start_on_s007_is_ranked_by_bm25_then_hits_then_id():
    sg = json.loads((ROOT / "data/processed/S007_subgraph.json").read_text(encoding="utf-8"))
    g = Graph(sg)
    log: list[str] = []
    chosen = select_start(g, S007_ANSWER, 3, log)
    assert len(chosen) == 3 and all(not g.concepts[c].get("generic") for c in chosen)
    assert "loop_control" in chosen
    assert any(l.startswith("start: BM25") for l in log)


def test_start_admits_a_generic_concept_the_answer_names_in_code():
    # S134: the only tagged concept is variable_swap; the answer repeats "=", the text that tagged the generic
    # concept assignment, so assignment joins the start concepts. S007's answer repeats none of its generic hits.
    for sid, expect_generic in (("S134", ["assignment"]), ("S007", [])):
        sg = json.loads((ROOT / f"data/processed/{sid}_subgraph.json").read_text(encoding="utf-8"))
        g = Graph(sg)
        chosen = select_start(g, SCENARIOS[sid]["answer"], 3, [])
        assert [c for c in chosen if g.concepts[c].get("generic")] == expect_generic


def test_names_in_code_whole_word_for_words_anywhere_for_symbols():
    assert traverse._names_in_code("=", "a = b")
    assert not traverse._names_in_code("int", "It prints 0")
    assert traverse._names_in_code("int", "an int is printed")
    assert not traverse._names_in_code("", "anything")


# ---------------------------------------------------------------- 3/4. evidence and the rule-based stop

def test_covered_clauses_uses_norm_matching():
    ev = [{"edge": "e1", "quote": "It prints 0."}, {"edge": "e2", "quote": "x is unset"}]
    assert covered_clauses(ev, ["It prints 0", "because x is unset", "other"]) == {0: "e1", 1: "e2"}


def test_rule_stop_waits_for_pending_prerequisites_and_full_coverage():
    # depth 1: MisC held covers clause 1; clause 2 is not covered and pre:B->C is unexamined -> deeper.
    # depth 2: pre:B->C broken covers clause 2; nothing pending any more -> stop: sufficient.
    labels = {"mis:C->MisC": ("held", "It prints 0"), "pre:B->C": ("broken", "because x is unset")}
    llm = ScriptedLLM(make_script(labels))
    log: list[str] = []
    d = traverse.traverse(TINY, TINY_SC, CFG, llm, log)
    assert set(llm.asks_by_step) <= {"prune", "label", "level"}
    assert d["stop_reason"] == "sufficient" and d["depth_reached"] == 2
    assert d["unexplained_clauses"] == [] and set(d["llm_calls_by_step"]) == set(STEPS)
    assert any("c1 <- mis:C->MisC" in l and "c2 <- pre:B->C" in l for l in log)
    assert d["root_cause"] == {"concept": "C", "misconception": "MisC"} and d["overall_level"] == "L0"


def test_rule_stop_does_not_stop_while_a_prerequisite_is_pending():
    # clause 2 is covered at depth 1 already, but MisC's concept C has the unexamined prerequisite edge pre:B->C.
    labels = {"mis:C->MisC": ("held", "It prints 0"), "mis:C->MisC2": ("correct", "because x is unset"), "pre:B->C": ("confirmed", "x is unset")}
    llm = ScriptedLLM(make_script(labels))
    log: list[str] = []
    d = traverse.traverse(TINY, TINY_SC, CFG, llm, log)
    assert any("unexamined prerequisites: pre:B->C" in l for l in log)
    assert d["depth_reached"] == 2 and d["stop_reason"] == "sufficient"


def test_rule_stop_runs_to_max_depth_when_a_clause_is_uncovered():
    labels = {"mis:C->MisC": ("held", "It prints 0"), "pre:B->C": ("confirmed", "It prints 0"), "pre:A->B": ("confirmed", "prints 0")}
    llm = ScriptedLLM(make_script(labels))
    d = traverse.traverse(TINY, TINY_SC, CFG, llm, [])
    assert d["stop_reason"] == "max depth" and d["depth_reached"] == 3
    assert d["unexplained_clauses"] == ["because x is unset"]


def test_evidence_keeps_dropped_correct_labels():
    # four labelled candidates, width 3: the correct one ranks last (tier 2) and is dropped from the paths ...
    labels = {"mis:B->MisB": ("held", "It prints 0"), "mis:B->MisB2": ("held", "prints 0"), "mis:C->MisC": ("held", "It prints 0"),
              "mis:C->MisC2": ("correct", "because x is unset")}
    llm = ScriptedLLM(make_script(labels))
    d = traverse.traverse(TINY, TINY_SC, {**CFG, "depth": 1}, llm, [])
    assert "mis:C->MisC2" not in {p["edge"] for p in d["paths"]}
    assert {e["edge"] for e in d["evidence"]} == set(labels)          # ... but it stays as evidence
    assert d["unexplained_clauses"] == []                            # and still covers its clause
    assert d["clause_coverage"]["because x is unset"] == "mis:C->MisC2"


# ---------------------------------------------------------------- S007 end to end, replayed from the cache

def test_s007_diagnosis_from_cached_replies():
    sg = json.loads((ROOT / "data/processed/S007_subgraph.json").read_text(encoding="utf-8"))
    cfg = {**DEFAULT_TRAVERSAL, "cache_dir": "experiments/llm_cache"}
    d = traverse.traverse(sg, SCENARIOS["S007"], cfg, ReplayLLM(cfg), [])
    assert d["clauses"] == S007_CLAUSES
    assert set(d["llm_calls_by_step"]) == {"prune", "label", "level"}
    assert {"concept": "loop_control", "misconception": "OffByOneBound"} in [
        {"concept": h["concept"], "misconception": h["misconception"]} for h in d["held_misconceptions"]]
    assert d["root_cause"] == {"concept": "loop_control", "misconception": "OffByOneBound"}
    assert d["overall_level"] == "L0" and d["levels"]["loop_control"]["level"] == "L0"
    assert d["stop_reason"] == "sufficient" and d["unexplained_clauses"] == []
