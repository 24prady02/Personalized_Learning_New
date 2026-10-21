"""
knowledge.py — the Chapter-1 knowledge graph, as the classifier sees it.

Loads data/chapter1_kg.json (v3.9: sections, 173 concepts, misconception and
error nodes, prerequisite / parallel / misconception / error edges, and the
per-concept L0-L4 learning-level nodes). Everything the pipeline reasons over
comes from this one file:

    execution facts  the concept's rules_by_type N, S, LT, OS and OP rules,
                     split into sentences, plus the correct rule ("right") of
                     each misconception listed under M
    misconceptions   misconception and error nodes linked to the concept
    boundary         misconceptions on a `primary` misconception / error edge
                     (must be repaired to reach L3)
    neighbours       prerequisite, parallel and R (relation) neighbours
    ladder           the criterion of each concept@L0..L4 learning-level node
    ways             every way on the concept -> L0..L4 has_level edges: the
                     way's name, its exact rule (for an L0 way, the wrong
                     reading it describes), the concepts it requires and the
                     misconceptions it stands for. The level a prompt reaches
                     is the highest level whose way the prompt shows (ladder.py).

The only thing not in the graph is the cue lexicon (cues.py), which says how a
concept shows up in a student's text.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path
from typing import Dict, List, Optional, Pattern, Set
import re

from .cues import CUES

ROOT = Path(__file__).resolve().parents[2]
GRAPH_PATH = ROOT / "data" / "chapter1_kg.json"

LEVELS = ("L0", "L1", "L2", "L3", "L4")
FACT_RULES = ("N", "S", "LT", "OS", "OP")      # rules_by_type keys that state what the construct does

_SENTENCE_RE = re.compile(r"(?<=[.;])(?<!e\.g\.)(?<!i\.e\.)\s+(?=[A-Z0-9(])")
_STEP_RE = re.compile(r"^\s*\d+\.\s*")
_RULE_PREFIX_RE = re.compile(r"\b(rule broken|Kind|Trigger class|Plan):\s*", re.I)
# an L0 way states the wrong reading, then the Java rule it breaks
_WRONG_PART_RE = re.compile(r"^\s*(?:everyday (?:reading|meaning)|folk meaning|wrong rule)\s*:\s*", re.I)
_RIGHT_PART_RE = re.compile(r"\b(?:Java rule|Right rule|In Java)\b\s*:?\s*")


def _sentences(text: str) -> List[str]:
    out = []
    for s in _SENTENCE_RE.split(text or ""):
        s = _STEP_RE.sub("", s).strip()
        if len(s.split()) >= 4:
            out.append(s)
    return out


@dataclass
class Misconception:
    id: str
    wrong_belief: str
    concepts: Set[str]
    kind: str = "misconception"                 # misconception | error


@dataclass
class Way:
    """One way on a concept -> level has_level edge."""
    name: str                                   # e.g. output_prediction, relation_to_neighbour
    level: str                                  # L0..L4
    rules: List[str]                            # sentences of its exact rule (L0: the wrong reading)
    right: List[str] = field(default_factory=list)          # L0: the Java rule the reading breaks
    requires: List[str] = field(default_factory=list)       # requires_concept (relation ways)
    misconceptions: List[str] = field(default_factory=list)


def _way(level: str, w: Dict) -> Way:
    text = _RULE_PREFIX_RE.sub("", w.get("exact_rule", ""))
    right: List[str] = []
    if level == "L0":
        text = text.split("(here mixing in", 1)[0]
        parts = _RIGHT_PART_RE.split(_WRONG_PART_RE.sub("", text), maxsplit=1)
        text, right = parts[0], _sentences(parts[1]) if len(parts) > 1 else []
    rules = _sentences(text) or ([text.strip()] if text.strip() else [])
    return Way(w.get("way", ""), level, rules, right, list(w.get("requires_concept") or []),
               list(w.get("linked_misconception") or []))


@dataclass
class Concept:
    id: str
    label: str
    chapter: str                                # section node id, e.g. sec1.3
    description: str
    code_cues: List[Pattern]
    word_cues: List[str]
    facts: List[str]
    misconceptions: Set[str] = field(default_factory=set)        # every linked misconception / error
    boundary: Set[str] = field(default_factory=set)              # must be repaired to reach L3
    prerequisites: Set[str] = field(default_factory=set)
    leads_to: Set[str] = field(default_factory=set)
    parallel: Set[str] = field(default_factory=set)
    related: Set[str] = field(default_factory=set)               # R-rule neighbours
    ladder: Dict[str, str] = field(default_factory=dict)         # level -> per-concept criterion
    ways: Dict[str, List[Way]] = field(default_factory=dict)       # L0..L4 -> the ways of that has_level edge
    deciding: Dict[str, str] = field(default_factory=dict)       # level -> the level node's deciding question

    @property
    def neighbours(self) -> Set[str]:
        return self.prerequisites | self.leads_to | self.parallel | self.related

    def way_rules(self, level: str) -> List[str]:
        return list(dict.fromkeys(r for w in self.ways.get(level, []) for r in w.rules))

    def relation_targets(self) -> Set[str]:
        """The concepts the L3 relation ways relate this concept to."""
        return {t for w in self.ways.get("L3", []) for t in w.requires}


def _word_cues(c: Dict, extra: List[str]) -> List[str]:
    words = [w.lower() for w in extra]
    for name in (c["id"].replace("_", " "), c["label"].replace("_", " ")):
        name = name.lower().strip()
        if re.fullmatch(r"[\w .'-]+", name) and name not in words:
            words.append(name)
    return words


class PercptKnowledge:
    def __init__(self, graph_path: Path = GRAPH_PATH):
        g = json.loads(Path(graph_path).read_text(encoding="utf-8"))
        self.version = g.get("version")
        self.chapters: Dict[str, Dict] = {
            s["id"]: {"id": s["id"], "section": s["section"],
                      "label": re.sub(r"^\d+(\.\d+)*\s+", "", s["label"])}
            for s in g["sections"]}
        section_id = {s["section"]: s["id"] for s in g["sections"]}
        self.level_names: Dict[str, str] = dict(g["schema"]["learning_levels"]["level_names"])

        self.misconceptions: Dict[str, Misconception] = {
            m["id"]: Misconception(m["id"], m["wrong_belief"], set(m.get("concepts", [])), m.get("kind", "misconception"))
            for m in g["misconceptions_and_errors"]}

        self.concepts: Dict[str, Concept] = {}
        for c in g["concepts"]:
            rb = c.get("rules_by_type") or {}
            facts: List[str] = []
            for key in FACT_RULES:
                facts += _sentences((rb.get(key) or {}).get("rule", ""))
            for m in rb.get("M") or []:
                facts += _sentences(m.get("right", ""))
            cues = CUES.get(c["id"], {})
            self.concepts[c["id"]] = Concept(
                id=c["id"], label=c["label"], chapter=section_id[c["section"]],
                description=c.get("description", ""),
                code_cues=[re.compile(p, re.MULTILINE) for p in cues.get("code", [])],
                word_cues=_word_cues(c, cues.get("words", [])),
                facts=list(dict.fromkeys(facts)),
                misconceptions={m for m in c.get("misconceptions", []) + c.get("errors", [])
                                if m in self.misconceptions},
                related={r["neighbour"] for r in rb.get("R") or [] if r.get("neighbour")},
            )
        for c in self.concepts.values():
            c.related = {n for n in c.related if n in self.concepts and n != c.id}
        for m in self.misconceptions.values():
            for cid in m.concepts:
                if cid in self.concepts:
                    self.concepts[cid].misconceptions.add(m.id)

        for lv in g["learning_levels"]:
            if lv["concept"] in self.concepts:
                self.concepts[lv["concept"]].ladder[lv["level"]] = lv.get("criterion", "")
                self.concepts[lv["concept"]].deciding[lv["level"]] = lv.get("deciding_question", "")

        for e in g["edges"]:
            s, t, kind = e["source"], e["target"], e["type"]
            if kind == "prerequisite" and s in self.concepts and t in self.concepts:
                self.concepts[t].prerequisites.add(s)
                self.concepts[s].leads_to.add(t)
            elif kind == "parallel" and s in self.concepts and t in self.concepts:
                self.concepts[s].parallel.add(t)
                self.concepts[t].parallel.add(s)
            elif kind == "has_level" and s in self.concepts and e.get("level") in LEVELS:
                self.concepts[s].ways[e["level"]] = [_way(e["level"], w) for w in e.get("ways") or []]
            elif kind in ("misconception", "error") and s in self.concepts and t in self.misconceptions:
                self.concepts[s].misconceptions.add(t)
                self.misconceptions[t].concepts.add(s)
                if e.get("role") == "primary":
                    self.concepts[s].boundary.add(t)

    def concept(self, cid: str) -> Optional[Concept]:
        return self.concepts.get(cid)

    def chapter_order(self) -> List[str]:
        return list(self.chapters)


@lru_cache(maxsize=1)
def get_knowledge() -> PercptKnowledge:
    return PercptKnowledge()
