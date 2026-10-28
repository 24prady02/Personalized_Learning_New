"""Knowledge: the concepts, ways and misconceptions of the Chapter-1 graph.

Stand-in for ``lp_percpt.knowledge.PercptKnowledge`` with the same public
surface the classifier needs (``concepts``, ``ways``, ``prerequisites``,
``leads_to``, ``parallel``, ``misconceptions``). When merging into the repo
that has ``src/lp_percpt/``, point ``load_knowledge()`` at the real class (or
subclass it) instead of keeping two loaders.

Reads ``data/chapter1_kg.json`` (the source of truth) defensively so the
same code works on graph v3.9.x exports whose optional fields differ.
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from pathlib import Path

log = logging.getLogger(__name__)

LEVELS: tuple[str, ...] = ("L0", "L1", "L2", "L3", "L4")
DEFAULT_KG_PATH = Path(__file__).resolve().parents[2] / "data" / "chapter1_kg.json"


@dataclass(frozen=True)
class Concept:
    """One concept node."""

    id: str
    label: str
    description: str
    rules_by_type: dict = field(default_factory=dict, compare=False, hash=False)
    misconceptions: tuple[str, ...] = ()


@dataclass(frozen=True)
class Way:
    """One way of reaching a level (an entry of a has_level edge's ``ways``).

    ``rules`` holds the exact rule text the way tests. For L0 ways ``right``
    is the correct rule the answer contradicts and ``misconceptions`` the
    linked misconception ids.
    """

    concept: str
    level: str
    index: int
    way: str
    rule_type: str
    rules: tuple[str, ...]
    right: str = ""
    misconceptions: tuple[str, ...] = ()
    requires: tuple[str, ...] = ()
    edge: str = ""

    @property
    def text(self) -> str:
        return " ".join(self.rules)


@dataclass(frozen=True)
class Misconception:
    """A misconception or error node."""

    id: str
    kind: str
    wrong_belief: str
    correct_rule: str
    concepts: tuple[str, ...]


class PercptKnowledge:
    """Concepts, ways per level, relations and misconceptions from the JSON."""

    def __init__(self, path: str | Path = DEFAULT_KG_PATH) -> None:
        self.path = Path(path)
        with self.path.open(encoding="utf-8") as fh:
            self.raw: dict = json.load(fh)
        self.version: str = str(self.raw.get("version", "unknown"))
        log.info("knowledge graph %s, version %s", self.path.name, self.version)
        self.concepts: dict[str, Concept] = {}
        for c in self.raw.get("concepts", []):
            cid = c.get("id")
            if not cid:
                continue
            self.concepts[cid] = Concept(
                id=cid,
                label=str(c.get("label") or cid),
                description=str(c.get("description") or ""),
                rules_by_type=c.get("rules_by_type") or {},
                misconceptions=tuple(c.get("misconceptions") or ()),
            )
        self.misconceptions: dict[str, Misconception] = {}
        for m in self.raw.get("misconceptions_and_errors", []):
            mid = m.get("id")
            if not mid:
                continue
            self.misconceptions[mid] = Misconception(
                id=mid,
                kind=str(m.get("kind") or m.get("type") or "misconception"),
                wrong_belief=str(m.get("wrong_belief") or ""),
                correct_rule=str(m.get("correct_rule") or ""),
                concepts=tuple(m.get("concepts") or ()),
            )
        self.prerequisites: dict[str, list[str]] = {c: [] for c in self.concepts}
        self.leads_to: dict[str, list[str]] = {c: [] for c in self.concepts}
        self.parallel: dict[str, list[str]] = {c: [] for c in self.concepts}
        self.ways: dict[str, dict[str, list[Way]]] = {
            c: {lv: [] for lv in LEVELS} for c in self.concepts
        }
        for e in self.raw.get("edges", []):
            self._index_edge(e)
        for table in (self.prerequisites, self.leads_to, self.parallel):
            for k in table:
                table[k] = sorted(set(table[k]))

    def _index_edge(self, e: dict) -> None:
        kind, src, dst = e.get("type"), e.get("source"), e.get("target")
        if src not in self.concepts:
            return
        if kind == "prerequisite" and dst in self.concepts:
            self.prerequisites[dst].append(src)
            self.leads_to[src].append(dst)
        elif kind == "parallel" and dst in self.concepts:
            self.parallel[src].append(dst)
            self.parallel[dst].append(src)
        elif kind == "has_level":
            level = str(e.get("level") or "")
            if level not in LEVELS:
                return
            for i, w in enumerate(e.get("ways") or []):
                self.ways[src][level].append(_way(src, level, i, w))

    def ways_at(self, concept: str, level: str) -> list[Way]:
        return list(self.ways.get(concept, {}).get(level, []))


def _way(concept: str, level: str, index: int, w: dict) -> Way:
    rule = str(w.get("exact_rule") or w.get("edge_logic") or "")
    right = ""
    if level == "L0" and "Right rule:" in rule:
        right = rule.split("Right rule:", 1)[1].strip()
    return Way(
        concept=concept,
        level=level,
        index=index,
        way=str(w.get("way") or ""),
        rule_type=str(w.get("rule_type") or ""),
        rules=(rule,) if rule else (),
        right=right,
        misconceptions=tuple(w.get("linked_misconception") or ()),
        requires=tuple(w.get("requires_concept") or ()),
        edge=str(w.get("edge") or ""),
    )


def load_knowledge(path: str | Path = DEFAULT_KG_PATH) -> PercptKnowledge:
    """Load the knowledge object (this module's class; see module docstring)."""
    return PercptKnowledge(path)
