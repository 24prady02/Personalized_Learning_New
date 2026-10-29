"""Tests for the graph-traversal classifier (src/lp_graph)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from lp_graph import execution  # noqa: E402
from lp_graph.candidates import select  # noqa: E402
from lp_graph.compare import compare_routes  # noqa: E402
from lp_graph.graph import KG  # noqa: E402
from lp_graph.levels import LevelResult, _consistency  # noqa: E402
from lp_graph.pipeline import assess  # noqa: E402
from lp_graph.reader import CONTRADICT, MATCH, Reader, Reading, Segment  # noqa: E402
from lp_graph.statements import answer_statements, code_context  # noqa: E402
from lp_graph.viterbi import Route, State, Step  # noqa: E402

REF_CODE = "int count;\nSystem.out.println(count);"
REF_Q = "What does the system print?"
TWIN = "A local variable has no value until it is assigned, and using it before then does not compile."
PRINT_Q = "What is the difference between print and println?"


@pytest.fixture(scope="module")
def kg() -> KG:
    return KG()


@pytest.fixture(scope="module")
def ref(kg):
    return assess(REF_CODE, REF_Q, "It will print 0.", kg)


# ------------------------------------------------- definite assignment check

def test_static_definite_assignment():
    stmts = execution.parse(execution.program_text(REF_CODE))
    found = execution.static_checks(stmts)
    assert [f.pattern for f in found] == ["uninitialized_read"]
    assert found[0].variable == "count"
    assert "might not have been initialized" in found[0].message


def test_static_check_allows_assigned_variable():
    code = "int count;\ncount = 3;\nSystem.out.println(count);"
    found = execution.static_checks(execution.parse(execution.program_text(code)))
    assert not [f for f in found if f.pattern == "uninitialized_read"]


def test_branch_assignment_is_not_definite():
    code = "int x;\nif (true) { x = 1; }\nSystem.out.println(x);"
    found = execution.static_checks(execution.parse(execution.program_text(code)))
    assert [f.variable for f in found if f.pattern == "uninitialized_read"] == ["x"]


def test_code_result_is_compile_error(ref):
    run = ref.trace.run
    assert run.error_kind == "compile"
    assert "might not have been initialized" in run.error


# ------------------------------------------------------- reference case

def test_reference_case(ref):
    assert ref.main_concept == "definite_assignment"
    for c in ("declaration", "variable", "int", "println", "definite_assignment"):
        assert c in ref.candidates.concepts
    assert "array_default_values" in ref.candidates.bridges
    assert [m["id"] for m in ref.misconceptions] == ["LocalVariablesAutoInitialized"]
    assert ref.levels["definite_assignment"].level == "L0"
    assert ref.headline_level == "L0"
    assert ref.feedback == [TWIN]
    # the correct route is built from the graph around the expected concepts
    assert "definite_assignment" in ref.route_correct.concepts()
    steps = ref.route_student.steps
    assert len(steps) == 1 and steps[0].state.kind == "M"
    assert steps[0].state.c_in == "definite_assignment"
    contrast = [ct["neighbour"] for rc in ref.root_causes for ct in rc.contrast]
    assert "array_default_values" in contrast


def test_reference_markdown(ref):
    md = ref.to_markdown()
    assert "definite_assignment L0 (misconception LocalVariablesAutoInitialized)" in md
    assert "likely source: contrast with array_default_values" in md
    assert f"feedback: {TWIN}" in md


# ---------------------------------------------------- three statements

def test_three_statement_version(kg):
    a = assess(REF_CODE, REF_Q,
               "count is declared as an int. It has no value yet so it is 0. So it prints 0.", kg)
    assert a.levels["declaration"].level == "L1"
    assert a.levels["definite_assignment"].level == "L0"
    by_id = {s.id: s for s in a.statements}
    mis_sentences = {by_id[sid].sentence for m in a.misconceptions for sid in m["statements"]}
    assert mis_sentences == {1, 2}  # sentences 2 and 3 (0-based 1, 2)
    assert [m["id"] for m in a.misconceptions] == ["LocalVariablesAutoInitialized"]
    # "declared" names declaration directly; "count" alone would not
    assert "declaration" in by_id["c1"].direct


# ------------------------------------------------------ print / println

def _reader_for(kg, answer):
    ctx = code_context(kg, "", None)
    sts = answer_statements(kg, answer, ctx)
    return Reader(kg, None), sts


def test_print_println_contrast_matches(kg):
    reader, sts = _reader_for(kg, "print stays on the same line but println moves to the next line")
    assert len(sts) == 2
    edge = kg.relation_edges["par:print~println"]
    assert reader.read_edge(Segment(tuple(sts)), edge).label == MATCH
    a = assess("", PRINT_Q, "print stays on the same line but println moves to the next line", kg)
    assert "par:print~println" in a.route_student.edges()
    assert not a.misconceptions


def test_println_same_line_contradicts(kg):
    reader, sts = _reader_for(kg, "println stays on the same line")
    edge = kg.relation_edges["par:print~println"]
    r = reader.read_edge(Segment(tuple(sts)), edge)
    assert r.label == CONTRADICT
    assert r.part_ids == ("par:print~println#1",)
    a = assess("", PRINT_Q, "println stays on the same line", kg)
    assert "par:print~println" in [b["edge"] for b in a.comparison.broken]
    assert "par:print~println" not in a.route_student.edges()


# ------------------------------------------------------------ determinism

def test_determinism(kg):
    ans = "count is declared as an int. It has no value yet so it is 0. So it prints 0."
    d1 = assess(REF_CODE, REF_Q, ans, kg).to_dict()
    d2 = assess(REF_CODE, REF_Q, ans, kg).to_dict()
    assert json.dumps(d1, sort_keys=True) == json.dumps(d2, sort_keys=True)


def test_ppr_stable_and_main_by_rule(kg, ref):
    stmts = ref.statements
    c1 = select(kg, stmts, ref.trace)
    c2 = select(kg, stmts, ref.trace)
    assert c1.to_dict() == c2.to_dict()
    assert set(c1.seeds) <= set(c1.concepts)
    # generic concepts are never the main concept when another one fits
    assert c1.main_concept not in ("declaration", "variable", "int")


# ------------------------------------------------------------ consistency

def test_consistency_caps_broken_prerequisite(kg):
    eid = "pre:declaration->definite_assignment"
    results = {"definite_assignment": LevelResult(
        "definite_assignment", "L2", ["c1"],
        [{"level": "L1", "index": 0, "way": "names_the_element"},
         {"level": "L2", "index": 1, "way": "output_prediction"}])}
    _consistency(kg, results, {eid})
    r = results["definite_assignment"]
    assert r.level == "L1" and r.capped
    assert eid in r.note
    assert all(w["level"] == "L1" for w in r.ways)


# ------------------------------------------------------ non-stateable edges

def test_non_stateable_edges_never_lacking(kg):
    non_stateable = sorted(e for e, x in kg.relation_edges.items() if not x.stateable)
    assert non_stateable, "graph should contain questionable / order_only edges"
    groundings = {kg.relation_edges[e].grounding for e in non_stateable}
    assert groundings <= {"questionable", "order_only"}
    steps = []
    for eid in non_stateable + ["pre:declaration->definite_assignment"]:
        e = kg.relation_edges[eid]
        steps.append(Step(State(f"E:{eid}:fwd", "E", e.src, e.dst, eid), ("k1",), "edge", 0,
                          Reading(MATCH)))
    correct = Route(steps, 0, 0, len(steps))
    cmp_ = compare_routes(kg, correct, Route(), [])
    assert not set(non_stateable) & set(cmp_.lacking_edges)
    assert "pre:declaration->definite_assignment" in cmp_.lacking_edges


# ------------------------------------------------------------- kg parts

def test_parts_cover_reference_elements(kg):
    parts = kg.parts
    assert parts["source_hash"] == kg.source_hash
    spec = parts["misconceptions"]["mis:definite_assignment->LocalVariablesAutoInitialized"]["slot"]
    assert spec == {"slot": "value", "wrong_value": "default", "right_value": "none", "slot_kind": "phrase"}
    pp = {p["concept"]: p["slots"] for p in parts["edges"]["par:print~println"]["parts"]}
    assert pp["print"][0][:2] == ["cursor", "same_line"]
    assert pp["println"][0][:2] == ["cursor", "next_line"]


# ------------------------------------------------- mechanisms of the fixes

def test_stated_rule_matches_misconception_without_the_run(kg):
    # the wrong meaning of % gives the right number here, so only the wording can decide
    a = assess("int a = 9, b = 5;\nint r = a % b;", "Explain how r is computed.",
               "r is 4 because 9 % 5 means 9 minus 5.", kg)
    assert a.main_concept == "remainder_operator"
    assert "RemainderIsSubtraction" in [m["id"] for m in a.misconceptions]
    assert a.headline_level == "L0"


def test_variable_mention_is_not_declaration(kg):
    a = assess("int a = 3;\nint b = a + 2;", "What is b?", "b is 5.", kg)
    c = [s for s in a.statements if s.source == "answer"][0]
    assert "declaration" not in c.direct and "declaration" not in c.context
    assert a.headline_level == "L2"


def test_turns_and_self_correction(kg):
    code = "int v = 2, r = 0;\nswitch (v) {\ncase 1: r = 10;\ncase 2: r = 20;\ndefault: r = 30;\n}"
    a = assess(code, "What is r after the switch?", 'Turn 1: "r is 20."\nTurn 2: "Oh wait, it is 30."', kg)
    assert a.headline_level == "L2"
    assert [(m["id"], m["status"]) for m in a.misconceptions] == [("SwitchNoFallThrough", "corrected")]


def test_student_code_is_run(kg):
    a = assess("(writing task) int array nums already exists", "Copy nums into a new array.",
               "for (int i = 0; i <= nums.length; i++) out[i] = nums[i];", kg)
    assert a.trace.answer_run.error_kind == "run"
    assert "OffByOneBound" in [m["id"] for m in a.misconceptions]


def test_what_if_is_checked_against_the_changed_program(kg):
    a = assess('double x = 2.71828;\nSystem.out.printf("%5.1f", x);', "What is printed?",
               "With %.2f it would print 2.72.", kg)
    assert a.headline_level == "L4"


# ------------------------------------------------ no topic knowledge in code

ENGINE_WORDS = frozenset({
    # Java types and statement kinds the parser knows
    "int", "double", "char", "boolean", "print", "println", "comment", "statement", "variable",
    # kinds of run outcome and slot names of the engine's claim checks
    "compile", "run",
})


def test_no_topic_tables_in_code():
    """Every concept and misconception the classifier reads comes from the
    graph: no concept or misconception id appears as a string in src/lp_graph
    except the Java / engine words above (which only coincide with ids)."""
    import io
    import re
    import tokenize

    raw = json.load(open(ROOT / "data" / "chapter1_kg.json", encoding="utf-8"))
    ids = {c["id"] for c in raw["concepts"]} | {m["id"] for m in raw["misconceptions_and_errors"]}
    bad = []
    for f in sorted((ROOT / "src" / "lp_graph").glob("*.py")):
        src = f.read_text(encoding="utf-8")
        for tok in tokenize.generate_tokens(io.StringIO(src).readline):
            if tok.type != tokenize.STRING or tok.string.startswith(('"""', "'''", 'r"""')):
                continue
            for w in re.findall(r"[A-Za-z_]+", tok.string):
                if w in ids and w not in ENGINE_WORDS:
                    bad.append(f"{f.name}:{tok.start[0]} {w}")
    assert not bad, bad


def test_vocabulary_comes_from_the_graph(kg):
    from lp_graph import lexicon

    assert lexicon.PHRASES and lexicon.SIGNALS and lexicon.MISREAD and lexicon.OP_CONCEPT
    assert raw_reader_section_present()


def raw_reader_section_present() -> bool:
    raw = json.load(open(ROOT / "data" / "chapter1_kg.json", encoding="utf-8"))
    return "reader" in raw and all("reader" in c for c in raw["concepts"])


def test_engine_follows_the_graph(tmp_path):
    """Remove one piece of knowledge from a copy of the graph (the wording and
    the misinterpreter of RemainderIsSubtraction): with no code change the
    engine stops detecting it, and detects it again with the original graph."""
    code, q, ans = "int a = 9, b = 5;\nint r = a % b;", "Explain how r is computed.", "r is 4 because 9 % 5 means 9 minus 5."
    raw = json.load(open(ROOT / "data" / "chapter1_kg.json", encoding="utf-8"))
    sub = raw["reader"]["slots"]["op_meaning"]["values"]["subtraction"]
    sub["phrases"] = []
    for m in raw["misconceptions_and_errors"]:
        if m["id"] == "RemainderIsSubtraction":
            m.pop("misread_as", None)
    edited = tmp_path / "graph.json"
    edited.write_text(json.dumps(raw), encoding="utf-8")
    try:
        a = assess(code, q, ans, KG(edited, parts_path=None))
        assert "RemainderIsSubtraction" not in [m["id"] for m in a.misconceptions]
    finally:
        original = KG()  # reloads the original vocabulary
    a = assess(code, q, ans, original)
    assert "RemainderIsSubtraction" in [m["id"] for m in a.misconceptions]
