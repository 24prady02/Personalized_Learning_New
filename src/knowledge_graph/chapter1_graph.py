"""
chapter1_graph.py — loader for the Chapter-1 knowledge graph.

Source: data/chapter1_kg.json (v3.9; Sedgewick & Wayne 1.1-1.6, misconceptions
and errors from the literature, checked against the book).

Node types:
    section         sec1.1 ... sec1.6 (6)
    topic           topic1.1.a ... (36)
    concept         e.g. println (173)
    misconception   e.g. ParenthesesOnlyIfArgument
    error           e.g. StatementNeedsNoTerminator
    learning_level  one L0-L4 ladder per concept, e.g. println@L2

It exposes a small API (exists / canonical / get_neighbours /
get_prerequisites) plus Chapter-1 extras (concept info, misconceptions,
LP-level descriptors). Older ids ("program_structure.println") resolve through
each concept's previous_id.
"""
from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

DEFAULT_GRAPH_PATH = (Path(__file__).resolve().parents[2]
                      / "data" / "chapter1_kg.json")

# CPAL's older concept ids (used by the quiz and chat apps) -> Chapter-1
# graph concept id. Concepts outside Chapter 1 map to None and keep their own
# id as a standalone node in the student graph.
CPAL_TO_CHAPTER1: Dict[str, Optional[str]] = {
    "hello_world":            "program_text",
    "main_method":            "main_method",
    "println":                "println",
    "compile_vs_runtime":     "compile",
    "syntax_errors":          "statement",
    "type_mismatch":          "type_conversion",
    "integer_division":       "integer_division",
    "assignment_vs_compare":  "comparison_operators",
    "string_equality":        "string_type",
    "boolean_operators":      "logical_operators",
    "infinite_loop":          "infinite_loop",
    "variable_scope":         "loop_scope",
    "array_index":            "array_bounds",
    "array_not_allocated":    "array_creation",
    "foreach_no_modify":      "enhanced_for",
    "command_line_args":      "command_line_args",
    "scanner_buffer":         "standard_input",
    "sentinel_loop":          "sentinel_loop",
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
    """Read-only index over the Chapter-1 knowledge graph."""

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
        self._lp_desc: Dict[str, Dict[str, Dict]] = defaultdict(dict)  # concept -> level -> learning_level node
        self._by_label: Dict[str, str] = {}
        if self.path.exists():
            self._load()
        else:
            print(f"[Chapter1Graph] no graph at {self.path}")

    def _load(self) -> None:
        with open(self.path, encoding="utf-8") as fh:
            d = json.load(fh)
        self.meta = {k: d.get(k) for k in ("version", "title", "source")}
        self.chapters = {s["id"]: s for s in d.get("sections", [])}
        section_id = {s["section"]: s["id"] for s in d.get("sections", [])}
        self.concepts = {c["id"]: {**c, "chapter": section_id.get(c.get("section"), "")}
                         for c in d.get("concepts", [])}
        self.misconceptions = {m["id"]: m for m in d.get("misconceptions_and_errors", [])}
        names = (d.get("schema") or {}).get("learning_levels", {}).get("level_names", {})
        self.lp_scale = [{"id": k, "name": v} for k, v in names.items()]
        for lv in d.get("learning_levels", []):
            self._lp_desc[lv["concept"]][lv["level"]] = lv
        for e in d.get("edges", []):
            s, t, kind = e["source"], e["target"], e["type"]
            if kind == "prerequisite":
                self._prereqs[t].add(s)
                self._leads_to[s].add(t)
            elif kind == "parallel":
                self._parallel[s].add(t)
                self._parallel[t].add(s)
            elif kind in ("misconception", "error"):
                self._concept_miscs[s].add(t)
        # Older ids (previous_id) and labels resolve to the current id
        for cid, c in self.concepts.items():
            prev = c.get("previous_id")
            for p in (prev if isinstance(prev, list) else [prev] if prev else []):
                self._by_label[p] = cid
            self._by_label.setdefault(c.get("label", cid), cid)
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
        node = self._lp_desc.get(self.canonical(concept), {}).get(level)
        return node.get("criterion") if node else None


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
    print(f"sections={len(g.chapters)} concepts={len(g.concepts)} "
          f"misconceptions={len(g.misconceptions)}")
    for c in ["println", "string_equality", "arrays.array_bounds", "null_pointer"]:
        print(f"\n--- {c} -> {g.canonical(c)} (in Chapter 1: {g.exists(c)})")
        print(f"  neighbours    : {g.get_neighbours(c)}")
        print(f"  misconceptions: {[m['id'] for m in g.misconceptions_for(c)][:4]}")
        print(f"  L2 descriptor : {(g.lp_descriptor(c, 'L2') or '')[:100]}")
