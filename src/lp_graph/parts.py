"""Step 2 - derived reader data (``data/kg_parts.json``).

The reader compares a student statement with the *parts* of an edge's
logic, not with the whole sentence. ``build_parts(kg)`` derives, without
touching ``chapter1_kg.json``:

1. **Edge parts**: each relation edge's ``logic`` (and ``contrast``) split
   at ``;``, `` while ``, `` whereas ``, `` but `` and sentence ends. Each
   part is tagged with the endpoint concept it talks about (``concept``;
   None if it names neither or both endpoints).
2. **Slots per part**: ``slots.extract_slots`` on each part, the same
   extractor the reader runs on student text.
3. **Misconception slots**: for each misconception edge, the slot whose
   value differs between the wrong belief and the correct rule
   (``{slot, wrong_value, right_value}``; None if no slot was found).
4. **Way slots**: slots of every has_level way rule (for "stay on concept"
   matching and the level ladder).
5. **Aliases** and a coverage report.

Output is fully sorted so regenerating gives an identical file.
"""

from __future__ import annotations

import re
from typing import TYPE_CHECKING

from . import lexicon
from .knowledge import LEVELS
from .slots import Mention, extract_slots, find_mentions, normalize

if TYPE_CHECKING:  # pragma: no cover
    from .graph import KG

PARTS_FORMAT = 1
_SPLIT_RE = re.compile(r";|\s+(?=(?:while|whereas|but)\s)|(?<=[.!?])\s+(?=[A-Z0-9(\"'])")


def split_parts(text: str) -> list[str]:
    """Split edge logic into parts (the split word stays with the new part)."""
    parts = [p.strip(" .;") for p in _SPLIT_RE.split(text or "")]
    out = []
    for p in parts:
        p = re.sub(r"^(?:while|whereas|but)\s+", "", p.strip())
        if p:
            out.append(p)
    return out


def tag_concept(mentions: list[Mention], endpoints: tuple[str, str]) -> str | None:
    """The single endpoint concept a part names (None for neither/both)."""
    hit = sorted({c for m in mentions for c in m.concepts if c in endpoints})
    return hit[0] if len(hit) == 1 else None


def text_slots(kg: "KG", text: str) -> tuple[list[Mention], list[list]]:
    """Mentions and slots (as lists) of one graph text.

    Concrete values in graph text belong to worked examples ("int x = 5;
    adds x holding 5"), not to the rule, so value / output / runs slots with
    a concrete value are dropped; none / default / garbage / endless stay.
    """
    norm = normalize(text)
    mentions = find_mentions(norm, kg.alias_index_strict)
    keep = [s for s in extract_slots(norm, mentions)
            if s.name not in EXAMPLE_SLOTS or s.value in RULE_VALUES]
    return mentions, [s.as_list() for s in keep]


EXAMPLE_SLOTS = frozenset({"value", "output", "runs"})
RULE_VALUES = frozenset({"none", "default", "garbage", "endless"})


def _edge_parts(kg: "KG") -> dict[str, dict]:
    out: dict[str, dict] = {}
    for eid in sorted(kg.relation_edges):
        e = kg.relation_edges[eid]
        parts = []
        for origin, text in (("logic", e.logic), ("contrast", e.contrast)):
            for p in split_parts(text):
                mentions, slots = text_slots(kg, p)
                parts.append({
                    "id": f"{eid}#{len(parts)}",
                    "from": origin,
                    "text": p,
                    "concept": tag_concept(mentions, (e.src, e.dst)),
                    "slots": slots,
                })
        out[eid] = {
            "src": e.src, "dst": e.dst, "kind": e.kind,
            "stateable": e.stateable, "grounding": e.grounding, "parts": parts,
        }
    return out


def _ways(kg: "KG") -> dict[str, dict[str, list[dict]]]:
    out: dict[str, dict[str, list[dict]]] = {}
    for cid in kg.concepts:
        out[cid] = {}
        for lv in LEVELS:
            rows = []
            for w in kg.ways(cid, lv):
                _, slots = text_slots(kg, w.text)
                rows.append({
                    "index": w.index, "way": w.way, "rule_type": w.rule_type,
                    "slots": slots, "requires": sorted(w.requires),
                    "misconceptions": sorted(w.misconceptions),
                })
            out[cid][lv] = rows
    return out


def misconception_slot(wrong: list[list], right: list[list]) -> dict | None:
    """The slot whose value differs between wrong belief and correct rule."""
    w_vals: dict[str, list[str]] = {}
    r_vals: dict[str, list[str]] = {}
    for name, value, *_ in wrong:
        w_vals.setdefault(name, []).append(value)
    for name, value, *_ in right:
        r_vals.setdefault(name, []).append(value)
    names = sorted(set(w_vals) | set(r_vals))
    # first a slot stated on both sides with different values ...
    for name in names:
        ws, rs = sorted(set(w_vals.get(name, []))), sorted(set(r_vals.get(name, [])))
        w_only = [v for v in ws if v not in rs]
        r_only = [v for v in rs if v not in ws]
        if w_only and r_only:
            return {"slot": name, "wrong_value": w_only[0], "right_value": r_only[0]}
    # ... else a slot stated on one side only, whose opposite is the other side
    for name in names:
        ws, rs = sorted(set(w_vals.get(name, []))), sorted(set(r_vals.get(name, [])))
        w_only = [v for v in ws if v not in rs]
        r_only = [v for v in rs if v not in ws]
        if w_only and not rs and w_only[0] in lexicon.OPPOSITE:
            return {"slot": name, "wrong_value": w_only[0], "right_value": lexicon.OPPOSITE[w_only[0]]}
        if r_only and not ws and r_only[0] in lexicon.OPPOSITE:
            return {"slot": name, "wrong_value": lexicon.OPPOSITE[r_only[0]], "right_value": r_only[0]}
    return None


def _misconceptions(kg: "KG") -> dict[str, dict]:
    out: dict[str, dict] = {}
    for cid in kg.concepts:
        for m in kg.mis_edges[cid]:
            _, w = text_slots(kg, m.wrong)
            _, r = text_slots(kg, m.right)
            out[m.id] = {
                "concept": cid, "mis": m.mis, "kind": m.kind, "role": m.role,
                "wrong_slots": w, "right_slots": r,
                "slot": misconception_slot(w, r),
            }
    return out


def build_parts(kg: "KG") -> dict:
    """All derived data, deterministic and JSON-serialisable."""
    edges = _edge_parts(kg)
    mis = _misconceptions(kg)
    ways = _ways(kg)
    n_ways = sum(len(r) for c in ways.values() for r in c.values())
    coverage = {
        "relation_edges": len(edges),
        "edges_with_tagged_part": sum(any(p["concept"] for p in e["parts"]) for e in edges.values()),
        "edges_with_slot": sum(any(p["slots"] for p in e["parts"]) for e in edges.values()),
        "edges_tagged_and_slotted": sum(any(p["concept"] and p["slots"] for p in e["parts"])
                                        for e in edges.values()),
        "parts": sum(len(e["parts"]) for e in edges.values()),
        "parts_tagged": sum(1 for e in edges.values() for p in e["parts"] if p["concept"]),
        "misconception_edges": len(mis),
        "misconceptions_with_slot": sum(1 for m in mis.values() if m["slot"]),
        "ways": n_ways,
        "ways_with_slot": sum(1 for c in ways.values() for r in c.values() for w in r if w["slots"]),
    }
    return {
        "format": PARTS_FORMAT,
        "graph_version": kg.version,
        "source_file": kg.path.name,
        "source_hash": kg.source_hash,
        "aliases": {c: kg.aliases[c] for c in kg.concepts},
        "edges": edges,
        "ways": ways,
        "misconceptions": mis,
        "coverage": coverage,
    }
