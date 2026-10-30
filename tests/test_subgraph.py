"""Tests for the code-only subgraph stage."""
from __future__ import annotations

import json
import re
import time
from collections import Counter
from pathlib import Path

import pytest

from lp_graph.subgraph import command_segments, extract_subgraph, mask_java, reader_blocks, split_statements, subgraph_from_code, tag_code
from lp_graph.subgraph.report import NOT_IN_CODE, gold_concepts, load_gold

ROOT = Path(__file__).resolve().parents[1]
KG = json.loads((ROOT / "data/raw/chapter1_kg.json").read_text(encoding="utf-8"))
READER = reader_blocks(KG)
PATTERN_TESTS = json.loads((ROOT / "tests/data/concept_pattern_tests.json").read_text(encoding="utf-8"))
SCENARIOS = load_gold(ROOT / "data/raw/scenarios_20.json")
GOLD = [s for s in SCENARIOS if not s.get("reference_case")]


# ---------------------------------------------------------------- mask / split

def test_mask_keeps_length_and_blanks_literals_and_comments():
    code = 'String s = "a;b"; // c;\nchar q = \'\\\'\'; /* x\ny */ int z;'
    m = mask_java(code)
    assert len(m) == len(code)
    assert m.count("\n") == code.count("\n")
    assert '"a;b"' not in m and '"   "' in m
    assert "c;" not in m.split("\n")[0]
    assert "x" not in m.split("\n")[1] or m.split("\n")[1].strip().startswith("y") is False
    assert "int z;" in m


def test_split_keeps_for_header_in_one_piece():
    parts = split_statements("for (int i = 0; i <= a.length; i++) b[i] = a[i];")
    assert len(parts) == 1
    parts = split_statements("int a = 1; { b = 2; }")
    assert [p.strip() for p in parts] == ["int a = 1;", "{", "b = 2;", "}"]


def test_command_segments():
    segs = command_segments("% java RandomSeq 5 > data.txt\n% java Average < data.txt\n% java RandomSeq 5 | java Average")
    assert segs == ["java RandomSeq 5 > data.txt", "java Average < data.txt", "java RandomSeq 5 | java Average"]


# ---------------------------------------------------------------- per-concept patterns

def test_every_code_visible_concept_has_pattern_tests():
    visible = {c["id"] for c in KG["concepts"] if (c.get("reader") or {}).get("code_visible") is not False}
    assert visible == set(PATTERN_TESTS)
    assert len(visible) == 182


@pytest.mark.parametrize("cid", sorted(PATTERN_TESTS))
def test_concept_patterns(cid):
    spec = PATTERN_TESTS[cid]
    for snippet in spec["must_tag"]:
        assert cid in tag_code(snippet, READER), f"{cid} should tag: {snippet!r}"
    for snippet in spec["must_not_tag"]:
        assert cid not in tag_code(snippet, READER), f"{cid} should NOT tag: {snippet!r}"


def test_code_invisible_concepts_never_tag():
    code = "\n".join(s for spec in PATTERN_TESTS.values() for s in spec["must_tag"])
    tags = tag_code(code, READER)
    for c in KG["concepts"]:
        if (c.get("reader") or {}).get("code_visible") is False:
            assert c["id"] not in tags


# ---------------------------------------------------------------- speed

def _timed(rx: str, text: str) -> float:
    t0 = time.perf_counter()
    re.search(rx, text, re.M | re.S)
    return time.perf_counter() - t0


def test_speed():
    big = "\n".join(s for spec in PATTERN_TESTS.values() for s in spec["must_tag"]) * 20
    assert len(big) > 90_000
    t0 = time.perf_counter()
    tag_code(big, READER)
    assert time.perf_counter() - t0 < 5.0
    masked = mask_java(big)
    slow = []
    for cid, rd in READER.items():
        regexes = list(rd.get("code_patterns") or []) + [s["regex"] for s in rd.get("signals") or [] if "regex" in s]
        for rx in regexes:
            dt = min(_timed(rx, masked) for _ in range(3))  # best of three: the limit is about the regex, not CPU jitter
            # the limit scales with the corpus (0.25 s per 100k characters): a linear pattern such as
            # integer_division.int_var_div_literal (one 800-char scan per int declaration) stays under it on any
            # corpus size, while a quadratic pattern blows past it
            if dt > 0.25 * max(1.0, len(masked) / 100_000):
                slow.append((cid, rx[:60], round(dt, 3)))
    assert not slow, slow


# ---------------------------------------------------------------- S007 end to end

S007 = """for (int i = 3; i >= 0; i--) {
  for (int j = i; j > 0; j--) {
    System.out.printf("%d ", j);
  }
  System.out.println();
}"""


def test_s007_subgraph():
    tags = tag_code(S007, READER)
    assert {"for_loop", "loop_control", "nested_loops", "formatted_output", "println"} <= set(tags)
    assert any(h["channel"] == "signal" and h["name"] == "for_header" and h["decisive"] for h in tags["loop_control"])
    assert any(h["channel"] == "signal" and h["name"] == "nested_for" and h["decisive"] for h in tags["nested_loops"])
    assert not any(h["name"] == "printf_width" for h in tags["formatted_output"])
    sg = extract_subgraph(KG, tags, "S007")
    edge_ids = {e["id"] for e in sg["concept_edges"]}
    assert {"pre:loop_control->for_loop", "pre:for_loop->nested_loops", "par:println~formatted_output"} <= edge_ids
    mis = {e["id"]: e for e in sg["mis_edges"]}
    assert "mis:loop_control->OffByOneBound" in mis
    assert mis["mis:loop_control->OffByOneBound"]["logic"] and mis["mis:loop_control->OffByOneBound"]["twin_logic"]
    level_ids = {l["id"] for l in sg["levels"]}
    for c in ("loop_control", "nested_loops"):
        assert {f"{c}@L{i}" for i in range(5)} <= level_ids
    links = {(l["level_node"], l["misconception"]) for l in sg["level_mis_links"]}
    assert ("loop_control@L0", "OffByOneBound") in links
    assert ("nested_loops@L0", "EmptyInnerLoopSkipsRest") in links


# ---------------------------------------------------------------- snippets from the task

SNIPPETS = [
    ('System.out.println("for (int i = 0; i < 3; i++)");', [], ["for_loop", "loop_control"]),
    ("do { i++; } while (i < 5);", ["do_while_loop"], ["empty_statement", "logical_error"]),
    ("if (x > 0);\ny = 1;", ["empty_statement", "logical_error"], []),
    ("for (int i = 0; i <= a.length; i++) b[i] = a[i];", ["off_by_one_error", "array_bounds", "array_copy", "array_traversal"], []),
    ("int a = 7, b = 2; int c = a / b;", ["integer_division"], []),
    ("int a = 7; int b = 2; double c = a / b;", ["integer_division"], []),
    ("int x = 9 / 2;", ["integer_division"], []),
    ("double c = 7.0 / 2;", [], ["integer_division"]),
    ("int a = 7; double c = (double) a / 2;", [], ["integer_division"]),
    ("int[] counts = {0,2}; int d = 5; double[] p = new double[2]; p[0] = counts[0] / d;", ["integer_division", "normalization"], []),
    ("int x; System.out.println(x);", ["definite_assignment"], []),
    ("int x; x = 3; System.out.println(x);", [], ["definite_assignment"]),
    ("int[] a = new int[3]; System.out.println(a);", ["printing_array_reference"], []),
    ("int[] a = new int[3]; System.out.println(a[0]);", [], ["printing_array_reference"]),
    ("char SingleLetter = 'Q';", ["naming_convention"], []),
    ("char singleLetter = 'Q';", [], ["naming_convention"]),
    ("final int MAX_SIZE = 10;", [], ["naming_convention"]),
    ("int[] b = a;", ["array_aliasing", "array_reference"], []),
    ("if (a[i] > max) max = a[i];", ["running_extreme"], []),
    ("i = i++;", ["side_effect_order"], []),
    ("if (a) if (b) x = 1; else x = 2;", ["dangling_else"], []),
    ("boolean found = false;\nfor (int i = 0; i < n; i++) if (a[i] == k) found = true;", ["flag_search_loop"], []),
    ("while (!StdIn.isEmpty()) { int x = StdIn.readInt(); }", ["read_loop_idiom", "end_of_input", "input_format", "stream_model"], []),
]


@pytest.mark.parametrize("code,must,must_not", SNIPPETS)
def test_snippets(code, must, must_not):
    tags = set(tag_code(code, READER))
    assert set(must) <= tags, f"missing {set(must) - tags}"
    assert not (set(must_not) & tags), f"should not tag {set(must_not) & tags}"


# ---------------------------------------------------------------- the 20 gold scenarios, code only

@pytest.mark.parametrize("sc", GOLD, ids=[s["id"] for s in GOLD])
def test_gold_scenario_coverage(sc):
    sg = subgraph_from_code(sc["code"], KG, sc["id"])
    got = {c["id"] for c in sg["concepts"]}
    missed = gold_concepts(sc) - got
    expected = NOT_IN_CODE.get(sc["id"], set())
    unexpected = missed - expected
    assert not unexpected, f"{sc['id']} missed {sorted(unexpected)}"
    if missed:
        pytest.xfail(f"{sc['id']}: {sorted(missed)} not present in the code; the question or the student's answer brings it in")


def test_gold_summary_and_breadth():
    generic = {c["id"] for c in KG["concepts"] if (c.get("reader") or {}).get("generic")}
    covered = 0
    fire: Counter[str] = Counter()
    sizes = []
    for sc in GOLD:
        sg = subgraph_from_code(sc["code"], KG, sc["id"])
        got = {c["id"] for c in sg["concepts"]}
        sizes.append(len(got))
        fire.update(c["id"] for c in sg["concepts"] if c["why"] == "code" and c["id"] not in generic)
        if not (gold_concepts(sc) - got):
            covered += 1
    expected_partial = {sc["id"] for sc in GOLD if gold_concepts(sc) & NOT_IN_CODE.get(sc["id"], set())}
    assert covered == len(GOLD) - len(expected_partial), f"fully covered from code alone: {covered} / {len(GOLD)}"
    broad = [(c, k) for c, k in fire.items() if k >= 12]
    assert not broad, f"pattern too broad: {broad}"
    assert 10 <= sum(sizes) / len(sizes) <= 25


def test_nodes_are_exactly_the_tagged_concepts():
    for sc in SCENARIOS:
        tags = set(tag_code(sc["code"], READER))
        sg = subgraph_from_code(sc["code"], KG, sc["id"])
        assert {c["id"] for c in sg["concepts"]} == tags
        assert all(c["why"] == "code" for c in sg["concepts"])
        assert sg["counts"]["from_hop"] == 0


def test_extract_rules():
    """Optional prerequisite hop: one hop, never from generic concepts; edges need both ends; ids well formed."""
    sg = subgraph_from_code("int[] b = a;", KG, hops=1)
    ids = {c["id"] for c in sg["concepts"]}
    assert any(c["why"].startswith("prerequisite_of:") for c in sg["concepts"])
    for c in sg["concepts"]:
        if c["why"].startswith("prerequisite_of:"):
            parent = c["why"].split(":", 1)[1]
            assert parent in ids
            assert not READER[parent].get("generic")
    for e in sg["concept_edges"]:
        assert e["source"] in ids and e["target"] in ids
        assert e["id"].startswith(("pre:", "par:"))
    for e in sg["mis_edges"]:
        assert e["source"] in ids and e["id"].startswith(("mis:", "err:"))
    for l in sg["level_edges"]:
        assert l["source"] in ids
    assert sg["counts"]["concepts"] == len(sg["concepts"])


# ---------------------------------------------------------------- recall: alternative spellings per concept

RECALL = json.loads((ROOT / "tests/data/recall_variants.json").read_text(encoding="utf-8"))["must_tag"]


@pytest.mark.parametrize("cid", sorted(RECALL))
def test_recall_variants(cid):
    missed = [s for s in RECALL[cid] if cid not in tag_code(s, READER)]
    assert not missed, f"{cid} misses {missed}"
