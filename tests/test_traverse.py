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
    return re.findall(r"^- ((?:mis|err|pre|par|lvl):\S+) \|", prompt, re.M)


def make_script(labels: dict[str, tuple[str, str]]):
    """labels: edge id -> (label, quote). The prune reply picks every candidate edge with equal scores. A level-way
    label prompt carries no edge id and no level (only the concept, the way and its text), so the way is found by its text."""
    way_by_text = {w["exact_rule"]: f"lvl:{le['target']}#{i}" for le in TINY["level_edges"] for i, w in enumerate(le["ways"])}

    def clause_no(prompt: str, quote: str) -> str:
        """The quote becomes the number of the clause that contains it: that is how the model now gives its evidence."""
        clauses = re.findall(r"^c(\d+): (.+)$", prompt, re.M)
        hits = [n for n, text in clauses if traverse._norm(quote) in traverse._norm(text)]
        return hits[0] if hits else "none"

    def script(prompt: str) -> str:
        if "Candidate edges of this concept" in prompt:
            ids = _edge_ids(prompt)
            return "\n".join(f"{{{e} (Score: {1 / len(ids):.3f})}}" for e in ids)
        if "Edges (each with its wrong rule and the right rule)" in prompt:      # the misconception set, judged together
            lines = []
            for eid in _edge_ids(prompt):
                label, quote = labels.get(eid, ("not applied", "none"))
                lines.append(f"{eid} | {label} | clauses: {clause_no(prompt, quote) if label != 'not applied' else 'none'} | confidence: 0.9")
            return "\n".join(lines)
        m = re.search(r"Edge: (\S+)", prompt)
        if m:
            eid = m.group(1)
        else:
            assert "Level" not in prompt and "deciding question" not in prompt and "lvl:" not in prompt
            eid = way_by_text[re.search(r"What an answer that shows this way does: (.+)", prompt).group(1).strip()]
        label, quote = labels.get(eid, ("not applied", "none"))
        return f"Label: {label}\nClauses: {clause_no(prompt, quote) if label != 'not applied' else 'none'}\nConfidence: 0.9"
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
    "levels": [{"id": "C@L0", "concept": "C", "level": "L0", "name": "Prestructural", "deciding_question": "q0"},
               {"id": "C@L2", "concept": "C", "level": "L2", "name": "Multistructural", "deciding_question": "q2"},
               {"id": "C@L3", "concept": "C", "level": "L3", "name": "Relational", "deciding_question": "q3"}],
    "level_edges": [
        {"id": "lvl:C->C@L0", "source": "C", "target": "C@L0", "level": "L0", "ways": [{"way": "misconception", "exact_rule": "wrong C"}, {"way": "everyday_reading", "exact_rule": "reads C as everyday"}]},
        {"id": "lvl:C->C@L2", "source": "C", "target": "C@L2", "level": "L2", "ways": [{"way": "output_prediction", "exact_rule": "predicts 0"}]},
        {"id": "lvl:C->C@L3", "source": "C", "target": "C@L3", "level": "L3", "ways": [{"way": "relation_to_neighbour", "exact_rule": "relates x to its declaration"}]},
    ],
    "level_mis_links": [{"level_node": "B@L0", "misconception": "MisB"}, {"level_node": "C@L0", "misconception": "MisC"}],
    "components": [["A", "B", "C", "G"]],
}
TINY_SC = {"id": "T001", "code": "int x;", "question": "What prints?", "answer": "It prints 0; because x is unset."}
CFG = {**DEFAULT_TRAVERSAL, "width": 3, "depth": 3}


def test_the_model_is_asked_in_two_places_only():
    assert STEPS == ("prune", "label")
    import prompts
    assert not hasattr(prompts, "START") and not hasattr(prompts, "SUFFICIENCY") and not hasattr(prompts, "LEVEL_LADDER")


def test_level_ways_are_edges_of_the_graph_without_misconception_ways():
    g = Graph(TINY)
    ids = [e["id"] for e in g.ways_by_concept["C"]]
    assert ids == ["lvl:C@L0#1", "lvl:C@L2#0", "lvl:C@L3#0"]      # the "misconception" way is left out
    assert g.edge_by_id["lvl:C@L3#0"]["logic"] == "relates x to its declaration"
    assert g.edge_text(g.edge_by_id["lvl:C@L2#0"]).startswith("lvl:C@L2#0 | level L2 way output_prediction: predicts 0")


def test_level_by_rule_highest_shown_way_and_l0_when_a_misconception_is_held():
    # correct answer: the L2 and L3 ways are shown -> L3 (the highest), no model call for the level itself
    labels = {"lvl:C@L2#0": ("shown", "It prints 0"), "lvl:C@L3#0": ("shown", "x is unset")}
    d = traverse.traverse(TINY, TINY_SC, {**CFG, "depth": 1}, ScriptedLLM(make_script(labels)), [])
    assert d["levels"]["C"]["level"] == "L3" and d["levels"]["C"]["way"] == "relation_to_neighbour"
    assert d["levels"]["C"]["also_shown"] == ["L2 output_prediction"] and d["overall_level"] == "L3"
    assert set(d["llm_calls_by_step"]) == {"prune", "label"}
    # the same ways shown, but MisC held as well -> L0
    labels["mis:C->MisC"] = ("held", "It prints 0")
    d = traverse.traverse(TINY, TINY_SC, {**CFG, "depth": 1}, ScriptedLLM(make_script(labels)), [])
    assert d["levels"]["C"]["level"] == "L0" and d["levels"]["C"]["misconception"] == "MisC" and d["overall_level"] == "L0"
    # an L0 way shown (everyday reading) beside an L3 way: the levels are cumulative, so the L3 way stands and the
    # L0 way is the weaker reading, listed under also_shown
    labels = {"lvl:C@L0#1": ("shown", "x is unset"), "lvl:C@L3#0": ("shown", "It prints 0")}
    d = traverse.traverse(TINY, TINY_SC, {**CFG, "depth": 1}, ScriptedLLM(make_script(labels)), [])
    assert d["levels"]["C"]["level"] == "L3" and d["levels"]["C"]["also_shown"] == ["L0 everyday_reading"]
    # an L0 way shown on its own, nothing above it -> L0
    labels = {"lvl:C@L0#1": ("shown", "x is unset")}
    d = traverse.traverse(TINY, TINY_SC, {**CFG, "depth": 1}, ScriptedLLM(make_script(labels)), [])
    assert d["levels"]["C"]["level"] == "L0" and d["levels"]["C"]["way"] == "everyday_reading"


def test_every_held_misconception_stays_and_shared_words_are_marked():
    # MisC and MisC2 both held on C from different words: two findings, the level reads the strongest edge and names the other
    labels = {"mis:C->MisC": ("held", "It prints 0"), "mis:C->MisC2": ("held", "x is unset")}
    d = traverse.traverse(TINY, TINY_SC, {**CFG, "depth": 1}, ScriptedLLM(make_script(labels)), [])
    assert sorted(h["misconception"] for h in d["held_misconceptions"]) == ["MisC", "MisC2"]
    assert not any("shares_evidence_with" in h for h in d["held_misconceptions"])
    assert d["levels"]["C"]["level"] == "L0" and d["levels"]["C"]["misconception"] == "MisC" and d["levels"]["C"]["rule"] == "wrong C"
    assert d["levels"]["C"]["also_held"] == ["MisC2"] and d["root_cause"] == {"concept": "C", "misconception": "MisC"}
    # both held from the same words: both stay, the weaker is marked as resting on the same words as the stronger
    labels = {"mis:C->MisC": ("held", "It prints 0"), "mis:C->MisC2": ("held", "It prints 0")}
    log: list[str] = []
    d = traverse.traverse(TINY, TINY_SC, {**CFG, "depth": 1}, ScriptedLLM(make_script(labels)), log)
    assert sorted(h["misconception"] for h in d["held_misconceptions"]) == ["MisC", "MisC2"]
    weaker = [h for h in d["held_misconceptions"] if h["misconception"] == "MisC2"][0]
    assert weaker["shares_evidence_with"] == "mis:C->MisC"
    assert any("same words as mis:C->MisC" in l for l in log)
    # a held misconception with no L0 way at its concept in the graph is reported as a graph gap
    labels = {"mis:C->MisC2": ("held", "It prints 0")}
    d = traverse.traverse(TINY, TINY_SC, {**CFG, "depth": 1}, ScriptedLLM(make_script(labels)), [])
    assert d["levels"]["C"]["source"] == "held_misconception" and "no L0 way" in d["levels"]["C"]["note"]
    # held misconceptions on two different concepts stay two findings
    labels = {"mis:B->MisB": ("held", "x is unset"), "mis:C->MisC": ("held", "It prints 0")}
    d = traverse.traverse(TINY, TINY_SC, {**CFG, "depth": 1}, ScriptedLLM(make_script(labels)), [])
    assert sorted(h["misconception"] for h in d["held_misconceptions"]) == ["MisB", "MisC"]


def test_same_misconception_at_both_ends_of_a_prerequisite_edge_is_filed_at_the_dependent_concept():
    import copy
    tiny = copy.deepcopy(TINY)
    tiny["mis_edges"].append({"id": "mis:B->MisC", "source": "B", "target": "MisC", "type": "misconception", "role": "primary",
                              "logic": "wrong C", "twin_logic": "right C"})
    labels = {"mis:B->MisC": ("held", "It prints 0"), "mis:C->MisC": ("held", "It prints 0")}
    d = traverse.traverse(tiny, TINY_SC, {**CFG, "depth": 1}, ScriptedLLM(make_script(labels)), [])
    assert [(h["concept"], h["misconception"]) for h in d["held_misconceptions"]] == [("C", "MisC")]
    assert d["root_cause"] == {"concept": "C", "misconception": "MisC"}      # not B, the prerequisite end
    assert "B" not in d["levels"] or d["levels"]["B"]["level"] == "L0"     # B's own evidence is untouched
    # without a prerequisite edge between the two concepts both findings stay
    two = [{"kind": "misconception", "source": "B", "target": "M", "score": 1}, {"kind": "misconception", "source": "C", "target": "M", "score": 1}]
    assert len(traverse.filed_at_dependent(two, {})) == 2 and len(traverse.filed_at_dependent(two, {"C": ["B"]})) == 1


def test_a_broken_edge_on_the_words_of_a_held_misconception_is_its_consequence_not_a_root():
    # MisC held at C from "It prints 0"; the second clause stays uncovered, so the walk goes back over pre:B->C
    # (confirmed) and finds pre:A->B broken from the same words as the misconception -> the fault stays at C
    labels = {"mis:C->MisC": ("held", "It prints 0"), "pre:B->C": ("confirmed", "It prints 0"), "pre:A->B": ("broken", "It prints 0")}
    d = traverse.traverse(TINY, TINY_SC, CFG, ScriptedLLM(make_script(labels)), [])
    assert d["root_cause"] == {"concept": "C", "misconception": "MisC"}
    assert [b for b in d["broken_edges"] if b["edge"] == "pre:A->B"][0]["consequence_of"] == "mis:C->MisC"
    # the same broken edge on other words is a fault of its own, further back, and becomes the root
    labels["pre:A->B"] = ("broken", "x is unset")
    d = traverse.traverse(TINY, TINY_SC, CFG, ScriptedLLM(make_script(labels)), [])
    assert d["root_cause"] == {"concept": "B", "misconception": None}
    assert "consequence_of" not in [b for b in d["broken_edges"] if b["edge"] == "pre:A->B"][0]


def test_uncovered_clauses_bring_in_a_concept_the_start_left_out():
    import copy
    tiny = copy.deepcopy(TINY)
    tiny["mis_edges"][0]["logic"] = "x is unset is the wrong B"    # B's text shares words with the second clause
    tiny["mis_edges"][2]["logic"] = "prints 0 is the wrong C"      # C's text shares words with the first clause
    labels = {"mis:B->MisB": ("held", "x is unset"), "mis:C->MisC": ("held", "It prints 0")}
    log: list[str] = []
    d = traverse.traverse(tiny, TINY_SC, {**CFG, "width": 1}, ScriptedLLM(make_script(labels)), log)
    assert len(d["start_concepts"]) == 1
    start, other = d["start_concepts"][0], ("C" if d["start_concepts"][0] == "B" else "B")
    # depth 1 explains one clause; the concept the start left out is brought in as a start concept, by the clause it
    # explains or because the answer names it (B is named by the "x" in the answer)
    assert any(l.startswith(f"  uncovered clauses bring in: {other}") or l.startswith(f"  named in the answer, entered next: {other}") for l in log)
    assert any(l.startswith(f"  {other} (misconceptions)") for l in log)
    assert sorted(h["misconception"] for h in d["held_misconceptions"]) == ["MisB", "MisC"]
    assert d["levels"]["B"]["level"] == "L0" and d["levels"]["C"]["level"] == "L0" and d["unexplained_clauses"] == []


def test_level_ways_never_become_next_hops():
    labels = {"lvl:C@L3#0": ("shown", "It prints 0")}
    log: list[str] = []
    d = traverse.traverse(TINY, TINY_SC, CFG, ScriptedLLM(make_script(labels)), log)
    # the shown way itself leads nowhere; what the walk reads next is the concept edges of the entered concepts
    assert not any("reached across lvl:" in l for l in log)
    assert any("not yet read: pre:A->B, pre:B->C" in l for l in log) and any("(concept edges)" in l for l in log)
    assert d["stop_reason"] == "half_stop" and d["depth_reached"] == 2 and any("no next nodes" in l for l in log)


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
    assert set(llm.asks_by_step) <= {"prune", "label"}
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
    assert any("not yet read:" in l and "pre:B->C" in l for l in log)
    assert d["depth_reached"] == 2 and d["stop_reason"] == "sufficient"
    assert [e["edge"] for e in d["evidence"] if e["label"] == "confirmed"] == ["pre:B->C"]    # the link is read and confirmed


def test_rule_stop_runs_to_max_depth_when_a_clause_is_uncovered():
    labels = {"mis:C->MisC": ("held", "It prints 0"), "pre:B->C": ("confirmed", "It prints 0"), "pre:A->B": ("confirmed", "prints 0")}
    llm = ScriptedLLM(make_script(labels))
    d = traverse.traverse(TINY, TINY_SC, CFG, llm, [])
    # every edge of the piece is read by depth 3 and the second clause is still unexplained: the walk runs out, it is never "sufficient"
    assert d["stop_reason"] in ("max depth", "half_stop") and d["depth_reached"] == 3
    assert d["unexplained_clauses"] == ["because x is unset"]
    assert sorted(e["edge"] for e in d["evidence"] if e["label"] == "confirmed") == ["pre:A->B", "pre:B->C"]


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
    assert set(d["llm_calls_by_step"]) == {"prune", "label"}
    assert {"concept": "loop_control", "misconception": "OffByOneBound"} in [
        {"concept": h["concept"], "misconception": h["misconception"]} for h in d["held_misconceptions"]]
    assert d["root_cause"] == {"concept": "loop_control", "misconception": "OffByOneBound"}
    assert d["overall_level"] == "L0" and d["levels"]["loop_control"]["level"] == "L0"
    assert d["stop_reason"] == "sufficient" and d["unexplained_clauses"] == []
