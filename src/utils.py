"""Shared helpers: paths, loading the knowledge graph and the scenarios, gold labels, regex cache.

Standard library only.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
KG_PATH = ROOT / "data/raw/chapter1_kg.json"
SCENARIOS_PATH = ROOT / "data/raw/scenarios_20.json"
SCENARIOS_NOT_FROM_CODE_PATH = ROOT / "data/raw/scenarios_not_from_code.json"
PROCESSED_DIR = ROOT / "data/processed"
RESULTS_DIR = ROOT / "results"
LOGS_DIR = ROOT / "experiments/logs"
CONFIG_PATH = ROOT / "experiments/config.json"

Hit = dict[str, Any]  # {channel, name, decisive, match, line}

# Concepts that the question or the student's answer brings in; they are not in the code. These scenarios live in
# data/raw/scenarios_not_from_code.json; the table is kept so that file can be run through the evaluation too.
NOT_IN_CODE: dict[str, set[str]] = {
    "S005": {"while_loop"},            # the code is a do-while; the student compares it with a while loop
    "S016": {"integer_division"},      # the code has % but no /; the student brings division in
    "S023": {"break_statement"},       # the switch has no break; the student explains the missing break
    "S073": {"break_statement"},
    "S080": {"compile"},               # no javac command in the code; the student describes compiling it
    "S009": {"array_bounds", "array_creation", "indexing", "length_field"},
    "S010": {"array_bounds", "array_copy", "array_traversal", "for_loop", "indexing", "off_by_one_error"},
    "S012": {"compound_assignment", "increment_operators"},
    "S015": {"char", "naming_convention", "variable"},
    "S057": {"explicit_cast"},
    "S068": {"power_method", "two_models"},
}


def load_config(path: Path = CONFIG_PATH) -> dict[str, Any]:
    """experiments/config.json: default paths and extractor settings."""
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {"kg": str(KG_PATH), "scenarios": str(SCENARIOS_PATH), "hops": 0, "keep_generic": False}


def load_kg(path: Path | str = KG_PATH) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def load_scenarios(path: Path | str = SCENARIOS_PATH) -> list[dict]:
    """The scenario list; the file is either a list or ``{"scenarios": [...]}``."""
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return data["scenarios"] if isinstance(data, dict) else data


def reader_blocks(kg: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """Concept id -> reader block (the code patterns live there)."""
    return {c["id"]: (c.get("reader") or {}) for c in kg["concepts"]}


def gold_concepts(sc: dict) -> set[str]:
    """Gold concepts of a scenario: the ``levels`` keys and both ends of each gold edge.

    Used only to check coverage (evaluate.py, tests); never by the extractor."""
    g = sc.get("gold", sc)
    need = set(g.get("levels", {}))
    for e in g.get("edges", []):
        eid = e["id"] if isinstance(e, dict) else e
        body = eid.split(":", 1)[1]
        a, b = (body.split("->") if "->" in body else body.split("~"))
        need.update([a, b])
    return need


_compiled: dict[tuple[str, int], re.Pattern[str]] = {}


def rx(pattern: str, flags: int = 0) -> re.Pattern[str]:
    """Compile once, reuse."""
    key = (pattern, flags)
    r = _compiled.get(key)
    if r is None:
        r = re.compile(pattern, flags)
        _compiled[key] = r
    return r


def line_of(code: str, pos: int) -> int:
    return code.count("\n", 0, pos) + 1
