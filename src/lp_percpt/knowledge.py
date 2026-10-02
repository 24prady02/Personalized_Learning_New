"""
knowledge.py — the Chapter-1 percpt knowledge graph, as the classifier sees it.

Loads data/chapter1_concept_graph_percpt_lp.json (concepts, misconceptions,
prerequisite / parallel / misconception edges, the per-concept L0-L4 ladder
with its boundary misconceptions) and merges data/chapter1_execution_facts.json
(per-concept cues and execution facts). Everything the pipeline reasons over
comes from these two files.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path
from typing import Dict, List, Optional, Pattern, Set
import re

ROOT = Path(__file__).resolve().parents[2]
GRAPH_PATH = ROOT / "data" / "chapter1_concept_graph_percpt_lp.json"
FACTS_PATH = ROOT / "data" / "chapter1_execution_facts.json"

LEVELS = ("L0", "L1", "L2", "L3", "L4")


@dataclass
class Misconception:
    id: str
    wrong_belief: str
    concepts: Set[str]


@dataclass
class Concept:
    id: str
    label: str
    chapter: str
    description: str
    code_cues: List[Pattern]
    word_cues: List[str]
    facts: List[str]
    misconceptions: Set[str] = field(default_factory=set)        # every linked misconception
    boundary: Set[str] = field(default_factory=set)              # must be repaired to reach L3
    prerequisites: Set[str] = field(default_factory=set)
    leads_to: Set[str] = field(default_factory=set)
    parallel: Set[str] = field(default_factory=set)
    ladder: Dict[str, str] = field(default_factory=dict)         # level -> per-concept descriptor

    @property
    def neighbours(self) -> Set[str]:
        return self.prerequisites | self.leads_to | self.parallel


class PercptKnowledge:
    def __init__(self, graph_path: Path = GRAPH_PATH, facts_path: Path = FACTS_PATH):
        g = json.loads(Path(graph_path).read_text(encoding="utf-8"))
        overlay = json.loads(Path(facts_path).read_text(encoding="utf-8"))["concepts"]
        self.version = g.get("version")
        self.chapters: Dict[str, Dict] = {c["id"]: c for c in g["chapters"]}
        self.level_names: Dict[str, str] = {
            lv["id"]: lv["name"] for lv in g["scales"]["lp"]["levels"]}

        self.misconceptions: Dict[str, Misconception] = {
            m["id"]: Misconception(m["id"], m["wrong_belief"], set(m.get("concepts", [])))
            for m in g["misconceptions"]}

        self.concepts: Dict[str, Concept] = {}
        for c in g["concepts"]:
            ov = overlay.get(c["id"], {})
            cues = ov.get("cues", {})
            self.concepts[c["id"]] = Concept(
                id=c["id"], label=c["label"], chapter=c["chapter"],
                description=c.get("description", ""),
                code_cues=[re.compile(p, re.MULTILINE) for p in cues.get("code", [])],
                word_cues=[w.lower() for w in cues.get("words", [])],
                facts=list(ov.get("facts", [])),
                misconceptions=set(c.get("misconceptions", [])),
            )
        for m in self.misconceptions.values():
            for cid in m.concepts:
                if cid in self.concepts:
                    self.concepts[cid].misconceptions.add(m.id)

        for e in g["edges"]:
            s, t, kind = e["source"], e["target"], e["type"]
            if kind == "prerequisite" and s in self.concepts and t in self.concepts:
                self.concepts[t].prerequisites.add(s)
                self.concepts[s].leads_to.add(t)
            elif kind == "parallel" and s in self.concepts and t in self.concepts:
                self.concepts[s].parallel.add(t)
                self.concepts[t].parallel.add(s)
            elif kind == "lp_indicator" and s in self.concepts:
                c = self.concepts[s]
                c.ladder[e["level"]] = e.get("logic", "")
                c.boundary.update(e.get("boundary_misconceptions") or [])
            elif kind == "misconception" and s in self.concepts and t in self.misconceptions:
                self.concepts[s].misconceptions.add(t)

    def concept(self, cid: str) -> Optional[Concept]:
        return self.concepts.get(cid)

    def chapter_order(self) -> List[str]:
        return list(self.chapters)


@lru_cache(maxsize=1)
def get_knowledge() -> PercptKnowledge:
    return PercptKnowledge()
