"""
Tests for src/lp_percpt (LP-level classification on the percpt graph).

Unit tests need no models: they drive the ladder walk, the Layer-1 gates and
the student graph's stability gates and inference rules with hand-built
evidence. The integration test loads the embedder and NLI model and is
skipped when they are not available.

Run:  python -m pytest tests/test_lp_percpt.py -q
"""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.lp_percpt.evidence import (MET, NOT_MET, UNCERTAIN, ConceptEvidence, Item,  # noqa: E402
                                    content_gate, help_seeking, no_claim)
from src.lp_percpt.knowledge import get_knowledge  # noqa: E402
from src.lp_percpt.ladder import walk  # noqa: E402
from src.lp_percpt.student_graph import StudentGraph  # noqa: E402

KG = get_knowledge()
WHILE = "while_loop"
FOR = "for_loop"
LOOP_CONTROL = "loop_control"


def checks(e1=NOT_MET, e2=NOT_MET, e3=NOT_MET, e4=NOT_MET):
    return {"E1": e1, "E2": e2, "E3": e3, "E4": e4}


def evidence(cid, upto=0, text="clause", held=(), refuted=(), wrong_trace=False, uncertain=None):
    ev = ConceptEvidence(cid)
    for k in range(1, upto + 1):
        ev.set(f"E{k}", MET, Item(f"E{k}", f"{text} {k}", "stmt"))
    if uncertain:
        ev.set(uncertain, UNCERTAIN)
    ev.held, ev.refuted, ev.wrong_trace = set(held), set(refuted), wrong_trace
    ev.clause_keys = [text]
    return ev


# ── knowledge graph ─────────────────────────────────────────────────────────
def test_graph_loads():
    assert len(KG.concepts) == 173
    assert all(c.facts for c in KG.concepts.values())
    assert all(set(c.ladder) == {"L0", "L1", "L2", "L3", "L4"} for c in KG.concepts.values())
    assert "IfIsLoop" in KG.concepts[WHILE].boundary
    assert LOOP_CONTROL in KG.concepts[FOR].prerequisites


# ── Step 8 ladder walk ──────────────────────────────────────────────────────
def test_walk_climbs_while_requirements_met():
    assert walk(checks(), set()).level == 0
    assert walk(checks(MET), set()).level == 1
    assert walk(checks(MET, MET, MET), set()).level == 3
    assert walk(checks(MET, MET, MET, MET), set()).level == 4


def test_walk_reaches_highest_way_shown():
    # an L4 way (e.g. diagnose_an_error) counts without the code also being retraced
    r = walk(checks(MET, NOT_MET, MET, MET), set(), {4: "L4 diagnose_an_error"})
    assert r.level == 4 and "diagnose_an_error" in r.stop_reason


def test_walk_l0_way():
    # an L0 way puts the prompt at L0 unless a correct way above L1 is also shown
    assert walk(checks(MET), set(), l0_way="everyday_reading").level == 0
    assert walk(checks(MET, MET, MET), set(), l0_way="inconsistent_trace").level == 0
    assert walk(checks(MET, MET, MET), set(), l0_way="misconception (X)").level == 3


def test_walk_ambiguity_stays_lower():                       # G15
    r = walk(checks(MET, MET, UNCERTAIN), set())
    assert r.level == 2 and r.uncertain_toward == 3


def test_walk_boundary_misconception_blocks_l3():           # G13
    r = walk(checks(MET, MET, MET, MET), {"IfIsLoop"})
    assert r.level == 2 and r.blocked_by == {"IfIsLoop"}


# ── Layer 1 gates ───────────────────────────────────────────────────────────
def test_content_gate():                                     # G1
    assert content_gate("idk", 3)
    assert content_gate("loop?", 3)
    assert not content_gate("the loop condition never becomes false", 3)


def test_help_seeking_gate():                                # G2
    assert help_seeking("just tell me the answer")
    assert not help_seeking("the answer is 3 because both operands are int and the result is truncated")


@pytest.mark.parametrize("text", [
    "Why does my loop never end?", "Is count++ the same as count += 1?", "What does % do?",
    "How do I make my array bigger after I create it?", "I tried it and it crashed. Why?", "Is javac wrong?"])
def test_no_claim_gate_questions(text):                      # G2b
    assert no_claim(text)


@pytest.mark.parametrize("text", [
    "It prints 5, right?", "3 2 1?", "x becomes 6 and y stays 2, correct?", "idk, 10?", "Is it 7?",
    "Is the output 12?", "Does it print 'abc'?", "So it prints 3 then 4?", "i = 3 so it prints 3?",
    "The output is 12. Is that right?", "It prints 5 because i starts at 0. Is that right?"])
def test_no_claim_gate_tentative_answers_are_claims(text):    # G2b
    assert not no_claim(text)


# ── Step 10 stability gates and Step 12 rules ──────────────────────────────
def fresh():
    g = StudentGraph("t", KG)
    return g


def turn(g, ev, prompt_level=None, session="s1"):
    g.begin_turn(session)
    g.apply(ev, prompt_level if prompt_level is not None else walk(ev.checks, set()).level)
    g.infer()
    return g.nodes[ev.concept]


def test_accumulation_and_no_silent_drop():                  # R1, R2, G16
    g = fresh()
    turn(g, evidence(WHILE, 2, "a"))
    n = turn(g, evidence(WHILE, 1, "b"))
    assert n.level == 2                                       # a weaker prompt does not lower it


def test_jump_is_provisional_until_repeated():               # G17
    g = fresh()
    n = turn(g, evidence(WHILE, 3, "a"))
    assert n.level == 3 and n.provisional
    n = turn(g, evidence(WHILE, 3, "b"))
    assert not n.provisional


def test_repetition_adds_nothing():                          # G18
    g = fresh()
    turn(g, evidence(WHILE, 1, "same"))
    n = turn(g, evidence(WHILE, 2, "same"))
    assert n.level == 1 and "repetition" in n.last_gates


def test_boundary_cap_and_repair():                          # R3, R4
    g = fresh()
    turn(g, evidence(WHILE, 1, "a"))
    turn(g, evidence(WHILE, 2, "b"))
    n = turn(g, evidence(WHILE, 3, "c", held={"IfIsLoop"}))
    assert n.level == 2
    n = turn(g, evidence(WHILE, 2, "d", refuted={"IfIsLoop"}))
    assert n.level == 4 and "repair" in n.last_gates          # repair counts as E4


def test_wrong_trace_lowers_level():                         # G9
    g = fresh()
    turn(g, evidence(WHILE, 1, "a"))
    turn(g, evidence(WHILE, 2, "b"))
    n = turn(g, evidence(WHILE, 1, "c", wrong_trace=True))
    assert n.level == 1 and n.contested


def test_prerequisite_inference_and_gap():                   # R5, R6, G19
    g = fresh()
    turn(g, evidence(FOR, 1, "a"))
    turn(g, evidence(FOR, 2, "b"))
    pre = g.nodes[LOOP_CONTROL]
    assert not pre.observed and pre.inferred_level == 1
    assert [LOOP_CONTROL, FOR] not in g.gaps                  # inferred levels never make gaps
    turn(g, evidence(LOOP_CONTROL, 1, "c"))
    assert [LOOP_CONTROL, FOR] in g.gaps                      # observed L1 under an L2 concept


def test_at_risk_spreads_through_misconception_edges():      # R7
    g = fresh()
    turn(g, evidence(WHILE, 1, "a", held={"IfIsLoop"}))
    assert "IfIsLoop" in g.nodes["if_statement"].at_risk


def test_plateau_and_frontier():                             # R8, R9
    g = fresh()
    for t in ("a", "b", "c"):
        n = turn(g, evidence(WHILE, 1, t))
    assert n.plateau
    assert g.nodes["boolean_expression"].frontier


def test_staleness():                                        # G20
    g = fresh()
    turn(g, evidence(WHILE, 1, "a"), session="s1")
    for s in ("s2", "s3", "s4", "s5"):
        n = turn(g, evidence(WHILE, 0, f"x{s}"), session=s)
    assert n.stale


def test_teacher_override_is_not_lowered():                  # G21
    g = fresh()
    g.set_override(WHILE, 3)
    n = turn(g, evidence(WHILE, 1, "a"))
    assert n.level == 3


def test_graph_round_trip():
    g = fresh()
    turn(g, evidence(WHILE, 2, "a", held={"IfIsLoop"}))
    g2 = StudentGraph.from_dict(g.to_dict(), KG)
    assert g2.nodes[WHILE].level == 2 and g2.nodes[WHILE].held == {"IfIsLoop"}


# ── claims checked against a run (no Java needed: hand-made runs) ──────────
def test_claims_checked_against_run():
    from src.lp_percpt.claims import check, extract
    from src.lp_percpt.execution import Run
    run = Run(True, output="8, 10, 12, 13, ", values={"a": ["10", "20"], "b": ["20"]},
              lines=[1, 3, 4, 6], passes={1: 5})
    names = {"a", "b"}

    def verdicts(text, final=False):
        return [check(c, run) for c in extract(text, names, final_default=final)]
    assert verdicts("a = 20, b = 20.", final=True) == [True, True]
    assert verdicts("a = 10, b = 10.", final=True) == [False, False]   # first value, not the new one
    assert verdicts("it prints 8, 10, 12") == [True]
    assert verdicts("it prints 8, 9, 12") == [False]
    assert verdicts("the loop runs 5 times") == [True]
    assert verdicts("lines 1, 3, 4 and 6 run") == [True]
    assert verdicts("lines 1, 2 and 6 run") == [False]
    assert verdicts("the loop never ends") == [False]


def test_misconception_named_by_its_run():
    from src.lp_percpt.claims import check, extract
    from src.lp_percpt.execution import Run
    real = Run(True, values={"a": ["10", "20"], "b": ["20"]})
    mutants = {"AssignmentOppositeDirection": Run(True, values={"a": ["10"], "b": ["20", "10"]}),
               "AssignmentAddsToTarget": Run(True, values={"a": ["10", "30"], "b": ["20"]})}
    claims = extract("a = 10, b = 10.", {"a", "b"}, final_default=True)
    assert any(check(c, real) is False for c in claims)
    explained = [m for m, r in mutants.items() if all(check(c, r) for c in claims)]
    assert explained == ["AssignmentOppositeDirection"]


# ── integration: real models ────────────────────────────────────────────────
def _models_ok():
    try:
        from src.lp_percpt import models
        return all(models.available().values())
    except Exception:
        return False


@pytest.mark.skipif(not _models_ok(), reason="embedder / NLI model not available")
def test_engine_end_to_end(tmp_path):
    from src.lp_percpt.engine import LPPercptEngine
    eng = LPPercptEngine(store_dir=tmp_path / "st", map_dir=tmp_path / "maps", review_log=tmp_path / "rev.jsonl")

    def level(r, cid):
        return next(c for c in r["concepts"] if c["concept"] == cid)

    assert "help_seeking" in eng.process("s", "just tell me the answer")["prompt_gates"]
    assert "content" in eng.process("s", "idk")["prompt_gates"]

    r = eng.process("s", "my loop never stops")
    assert level(r, LOOP_CONTROL)["prompt_level"] == "L1"           # symptom report

    # the rule stated without applying it to any code is L1 (the graph's "states the rule" way)
    r = eng.process("s", "the while loop checks the condition before every pass and the body repeats while it is true")
    c = level(r, WHILE)
    assert c["prompt_level"] == "L1" and "IfIsLoop" not in c["held"]      # best-match principle

    r = eng.process("s", "i is never incremented so the condition i < 10 stays true and the loop "
                         "never ends because the loop variable does not change")
    assert level(r, LOOP_CONTROL)["prompt_level"] == "L3"

    r = eng.process("s", "I used == to compare two strings and it says false even though they are the same text")
    c = level(r, "comparison_operators")
    # a held misconception with nothing correct above L1 is the graph's L0 misconception way
    assert c["prompt_level"] == "L0" and "EqualityOperatorComparesObjectsValues" in c["held"]

    assert (tmp_path / "maps" / "s.html").exists()
