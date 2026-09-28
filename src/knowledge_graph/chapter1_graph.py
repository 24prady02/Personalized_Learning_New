"""
chapter1_graph.py — loader for the Chapter-1 concept + LP graph.

Source: data/chapter1_concept_graph_percpt_lp.json
(Sedgewick & Wayne 1.1-1.6, misconceptions from ProgMiscon.)

Four layers:
    1  chapter        program_structure, types_expressions, ... (7)
    2  concept        e.g. program_structure.println (70)
    3  misconception  e.g. ParenthesesOnlyIfArgument
    4  lp_level       one L0-L4 ladder per concept, e.g. program_structure.println@L2

This replaces the CSO/CSE-KG lookup the student knowledge graph used to name
and connect its nodes. It exposes the same small API (exists / canonical /
get_neighbours / get_prerequisites) plus Chapter-1 extras (concept info,
misconceptions, LP-level descriptors).
"""
from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

DEFAULT_GRAPH_PATH = (Path(__file__).resolve().parents[2]
                      / "data" / "chapter1_concept_graph_percpt_lp.json")

# CPAL's older concept ids (used by the LP diagnostician, DINA and the chat
# app) -> Chapter-1 graph concept id. Concepts outside Chapter 1 map to None
# and keep their own id as a standalone node in the student graph.
CPAL_TO_CHAPTER1: Dict[str, Optional[str]] = {
    "hello_world":            "program_structure.program_text",
    "main_method":            "program_structure.main_method",
    "println":                "program_structure.println",
    "compile_vs_runtime":     "program_structure.compile",
    "syntax_errors":          "program_structure.statement",
    "type_mismatch":          "types_expressions.type_conversion",
    "integer_division":       "types_expressions.integer_division",
    "assignment_vs_compare":  "types_expressions.comparison_operators",
    "string_equality":        "types_expressions.string_type",
    "boolean_operators":      "conditionals.logical_operators",
    "infinite_loop":          "loops.loop_control",
    "variable_scope":         "loops.loop_scope",
    "array_index":            "arrays.array_bounds",
    "array_not_allocated":    "arrays.array_creation",
    "foreach_no_modify":      "arrays.enhanced_for",
    "command_line_args":      "input_output.command_line_args",
    "scanner_buffer":         "input_output.standard_input",
    "sentinel_loop":          "input_output.read_loop_idiom",
    # Not covered by Chapter 1 (classes/objects/methods come later)
    "null_pointer":           None,
    "missing_return":         None,
    "unreachable_code":       None,
    "string_immutability":    None,
    "no_default_constructor": None,
    "static_vs_instance":     None,
    "overloading":            None,
    "generics_primitives":    None,
}


class Chapter1Graph:
    """Read-only index over the Chapter-1 concept + LP graph."""

    def __init__(self, path: Path = DEFAULT_GRAPH_PATH):
        self.path = Path(path)
        self.loaded = False
        self.meta: Dict[str, Any] = {}
        self.chapters: Dict[str, Dict] = {}
        self.concepts: Dict[str, Dict] = {}
        self.misconceptions: Dict[str, Dict] = {}
        self.lp_scale: List[Dict] = []
        self._prereqs: Dict[str, Set[str]] = defaultdict(set)     # B -> {A} (A before B)
        self._leads_to: Dict[str, Set[str]] = defaultdict(set)    # A -> {B}
        self._parallel: Dict[str, Set[str]] = defaultdict(set)
        self._concept_miscs: Dict[str, Set[str]] = defaultdict(set)
        self._lp_desc: Dict[str, Dict[str, Dict]] = defaultdict(dict)  # concept -> level -> edge
        self._by_label: Dict[str, str] = {}
        if self.path.exists():
            self._load()
        else:
            print(f"[Chapter1Graph] no graph at {self.path}")

    def _load(self) -> None:
        with open(self.path, encoding="utf-8") as fh:
            d = json.load(fh)
        self.meta = {k: d.get(k) for k in ("version", "title", "source")}
        self.chapters = {c["id"]: c for c in d.get("chapters", [])}
        self.concepts = {c["id"]: c for c in d.get("concepts", [])}
        self.misconceptions = {m["id"]: m for m in d.get("misconceptions", [])}
        self.lp_scale = (d.get("scales") or {}).get("lp", {}).get("levels", [])
        for e in d.get("edges", []):
            s, t, kind = e["source"], e["target"], e["type"]
            if kind == "prerequisite":
                self._prereqs[t].add(s)
                self._leads_to[s].add(t)
            elif kind == "parallel":
                self._parallel[s].add(t)
                self._parallel[t].add(s)
            elif kind == "misconception":
                self._concept_miscs[s].add(t)
            elif kind == "lp_indicator":
                self._lp_desc[s][e.get("level")] = e
        # Short labels ("println") resolve when they are unique
        seen: Dict[str, List[str]] = defaultdict(list)
        for cid in self.concepts:
            seen[cid.split(".", 1)[-1]].append(cid)
        self._by_label = {k: v[0] for k, v in seen.items() if len(v) == 1}
        self.loaded = True

    # ── Lookup API (same shape the student graph used from CSO) ───────────

    def canonical(self, concept: str) -> str:
        """Map any concept id CPAL uses to its Chapter-1 id when one exists;
        otherwise return the id unchanged."""
        if concept in self.concepts:
            return concept
        mapped = CPAL_TO_CHAPTER1.get(concept)
        if mapped:
            return mapped
        return self._by_label.get(concept, concept)

    def exists(self, concept: str) -> bool:
        return self.canonical(concept) in self.concepts

    def get_prerequisites(self, concept: str) -> List[str]:
        return sorted(self._prereqs.get(self.canonical(concept), set()))

    def get_leads_to(self, concept: str) -> List[str]:
        return sorted(self._leads_to.get(self.canonical(concept), set()))

    def get_parallel(self, concept: str) -> List[str]:
        return sorted(self._parallel.get(self.canonical(concept), set()))

    def get_neighbours(self, concept: str) -> Dict[str, List[str]]:
        c = self.canonical(concept)
        return {
            "prerequisites": self.get_prerequisites(c),
            "leads_to":      self.get_leads_to(c),
            "parallel":      self.get_parallel(c),
        }

    # ── Chapter-1 extras ──────────────────────────────────────────────────

    def concept_info(self, concept: str) -> Optional[Dict]:
        return self.concepts.get(self.canonical(concept))

    def misconceptions_for(self, concept: str) -> List[Dict]:
        c = self.canonical(concept)
        return [self.misconceptions[m] for m in sorted(self._concept_miscs.get(c, set()))
                if m in self.misconceptions]

    def lp_descriptor(self, concept: str, level: str) -> Optional[str]:
        """The per-concept description of what an LP level looks like."""
        edge = self._lp_desc.get(self.canonical(concept), {}).get(level)
        return edge.get("logic") if edge else None


_INSTANCE: Optional[Chapter1Graph] = None


def get_chapter1_graph() -> Chapter1Graph:
    """Process-wide singleton (loaded on first call)."""
    global _INSTANCE
    if _INSTANCE is None:
        _INSTANCE = Chapter1Graph()
    return _INSTANCE


if __name__ == "__main__":
    g = get_chapter1_graph()
    print(g.meta)
    print(f"chapters={len(g.chapters)} concepts={len(g.concepts)} "
          f"misconceptions={len(g.misconceptions)}")
    for c in ["println", "string_equality", "arrays.array_bounds", "null_pointer"]:
        print(f"\n--- {c} -> {g.canonical(c)} (in Chapter 1: {g.exists(c)})")
        print(f"  neighbours    : {g.get_neighbours(c)}")
        print(f"  misconceptions: {[m['id'] for m in g.misconceptions_for(c)][:4]}")
        print(f"  L2 descriptor : {(g.lp_descriptor(c, 'L2') or '')[:100]}")
