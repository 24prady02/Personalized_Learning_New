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

PARTS_FORMAT = 2



def split_parts(text: str) -> list[str]:
    """Split edge logic into parts (the split word stays with the new part)."""
    parts = [p.strip(" .;") for p in lexicon.rx("edge_logic_split").split(text or "")]
    out = []
    for p in parts:
        p = lexicon.rx("edge_logic_split_word").sub("", p.strip())
        if p:
            out.append(p)
    return out


def tag_concept(mentions: list[Mention], endpoints: tuple[str, str], text: str = "",
                kg: "KG | None" = None) -> str | None:
    """The endpoint concept a part talks about (None for neither/both).

    By alias first; else by an endpoint's code cue in the raw part text
    (``println(``, ``%``, ``do {``); else by the first endpoint mentioned
    (the part's subject)."""
    hit = sorted({c for m in mentions for c in m.concepts if c in endpoints})
    if len(hit) == 1:
        return hit[0]
    if kg is not None and text and not hit:
        by_cue = sorted(c for c in endpoints
                        if any(re.search(rx, text) for rx in kg.cues.get(c, {}).get("code", [])))
        if len(by_cue) == 1:
            return by_cue[0]
    if len(hit) == 2:
        first = min((m for m in mentions if any(c in endpoints for c in m.concepts)),
                    key=lambda m: m.start)
        return next(c for c in first.concepts if c in endpoints)
    return None


def text_slots(kg: "KG", text: str, keep_examples: bool = False) -> tuple[list[Mention], list[list]]:
    """Mentions and slots (as lists) of one graph text.

    Concrete values in graph text belong to worked examples ("int x = 5;
    adds x holding 5"), not to the rule, so value / output / runs slots with
    a concrete value are dropped; none / default / garbage / endless stay.
    With ``keep_examples`` (misconception pairs) they stay, marked as
    examples by their slot name.
    """
    norm = normalize(text)
    mentions = find_mentions(norm, kg.alias_index_strict)
    keep = [s for s in extract_slots(norm, mentions, raw=text)
            if keep_examples or s.name not in lexicon.EXAMPLE_SLOTS or s.value in lexicon.RULE_VALUES]
    return mentions, [s.as_list() for s in keep]





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
                    "concept": tag_concept(mentions, (e.src, e.dst), p, kg),
                    "slots": slots,
                })
        # a two-sided contrast "A does X; B does Y": tag the untagged half by position
        logic_parts = [p for p in parts if p["from"] == "logic"]
        if len(logic_parts) == 2:
            a, b = logic_parts
            if a["concept"] and not b["concept"]:
                b["concept"] = e.dst if a["concept"] == e.src else e.src
            elif b["concept"] and not a["concept"]:
                a["concept"] = e.dst if b["concept"] == e.src else e.src
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
                    "evidence": lexicon.EVIDENCE_CLASS.get(w.rule_type, "statement"),
                    "slots": slots, "requires": sorted(w.requires),
                    "misconceptions": sorted(w.misconceptions),
                })
            out[cid][lv] = rows
    return out


def misconception_slot(wrong: list[list], right: list[list], concept: str | None = None) -> dict | None:
    """The slot whose value differs between wrong belief and correct rule.

    Rule families (``lexicon.RULE_SLOTS``) are tried first, then the other
    phrase slots, then worked-example slots (``expr`` / ``value`` /
    ``output`` with concrete values). A slot attached to another concept
    than this misconception's is dropped (it would fire on the wrong
    subject). ``slot_kind`` tells the reader how to use it."""
    def ok(s: list) -> bool:
        if s[0] not in lexicon.EXAMPLE_SLOTS or s[1] in lexicon.RULE_VALUES:
            return True
        subj = s[3]
        return not concept or subj is None or subj == concept or str(subj).startswith(("var:", "expr:"))

    wrong = [s for s in wrong if ok(s)]
    right = [s for s in right if ok(s)]
    for kind, pick in (("rule", lambda n: n in lexicon.RULE_SLOTS),
                       ("phrase", lambda n: n not in lexicon.RULE_SLOTS and n not in lexicon.EXAMPLE_SLOTS
                        and n not in lexicon.OUTCOME_SLOTS),
                       ("phrase", lambda n: n in ("value",)),
                       ("phrase", lambda n: n in lexicon.OUTCOME_SLOTS),
                       ("example", lambda n: n in lexicon.EXAMPLE_SLOTS)):
        spec = _differing([s for s in wrong if pick(s[0])], [s for s in right if pick(s[0])])
        if spec:
            spec["slot_kind"] = kind
            if kind == "example":
                subj = next((s[3] for s in wrong + right if s[0] == spec["slot"] and s[3]), None)
                if subj:
                    spec["subject"] = subj
            return spec
    return None


def _differing(wrong: list[list], right: list[list]) -> dict | None:
    w_vals: dict[str, list[str]] = {}
    r_vals: dict[str, list[str]] = {}
    for name, value, *rest in wrong:
        w_vals.setdefault(_slot_key(name, value, rest), []).append(value)
    for name, value, *rest in right:
        r_vals.setdefault(_slot_key(name, value, rest), []).append(value)
    names = sorted(set(w_vals) | set(r_vals))
    # first a slot stated on both sides with different values ...
    for name in names:
        ws, rs = sorted(set(w_vals.get(name, []))), sorted(set(r_vals.get(name, [])))
        w_only = [v for v in ws if v not in rs]
        r_only = [v for v in rs if v not in ws]
        if w_only and r_only:
            return {"slot": name.split("@")[0], "wrong_value": w_only[0], "right_value": r_only[0]}
    # ... else a slot stated on one side only, whose opposite is the other side
    for name in names:
        ws, rs = sorted(set(w_vals.get(name, []))), sorted(set(r_vals.get(name, [])))
        w_only = [v for v in ws if v not in rs]
        r_only = [v for v in rs if v not in ws]
        if w_only and not rs and w_only[0] in lexicon.OPPOSITE:
            return {"slot": name.split("@")[0], "wrong_value": w_only[0],
                    "right_value": lexicon.OPPOSITE[w_only[0]]}
        if r_only and not ws and r_only[0] in lexicon.OPPOSITE:
            return {"slot": name.split("@")[0], "wrong_value": lexicon.OPPOSITE[r_only[0]],
                    "right_value": r_only[0]}
    return None


def _slot_key(name: str, value: str, rest: list) -> str:
    """Example slots are compared per subject (17 % 5 with 17 % 5)."""
    subj = rest[1] if len(rest) > 1 else None
    if name in lexicon.EXAMPLE_SLOTS and subj and value not in lexicon.RULE_VALUES:
        return f"{name}@{subj}"
    return name


_STOP = frozenset("""a an the and or of to in on at by for with from as is are be been being it its
this that these those not no so than then when while which who what if into only also just same each
every any all one two can cannot will would does do did has have had there their them they you your
his her he she we our us i me my more most less like such through after before up down out over""".split())


def contrast_terms(wrong: str, right: str, aliases: list[str]) -> dict | None:
    """Content words of the wrong belief that the correct rule does not use
    (and the reverse), generated from the graph's own pair (§3.3). The reader
    accepts them only under strict conditions (several terms, concept named)."""
    def words(t: str) -> set[str]:
        out = set()
        for w in re.findall(r"[a-z][a-z]+", normalize(t)):
            w = re.sub(r"(?:ing|ed|es|s)$", "", w) if len(w) > 5 else w
            if w not in _STOP and len(w) >= 4:
                out.add(w)
        return out

    alias_words = {w for a in aliases for w in normalize(a).split()}
    w, r = words(wrong), words(right)
    w_only = sorted(w - r - alias_words)
    r_only = sorted(r - w - alias_words)
    if len(w_only) < 2:
        return None
    return {"wrong_terms": w_only, "right_terms": r_only}


def _misconceptions(kg: "KG") -> dict[str, dict]:
    out: dict[str, dict] = {}
    for cid in kg.concepts:
        for m in kg.mis_edges[cid]:
            _, w = text_slots(kg, m.wrong, keep_examples=True)
            _, r = text_slots(kg, m.right, keep_examples=True)
            slot = misconception_slot(w, r, cid)
            out[m.id] = {
                "concept": cid, "mis": m.mis, "kind": m.kind, "role": m.role,
                "wrong_slots": w, "right_slots": r,
                "slot": slot,
                "contrast": None if slot else contrast_terms(m.wrong, m.right, kg.aliases[cid]),
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
        "misconceptions_with_rule_slot": sum(1 for m in mis.values()
                                             if m["slot"] and m["slot"]["slot_kind"] != "example"),
        "misconceptions_with_contrast_only": sum(1 for m in mis.values()
                                                 if not m["slot"] and m["contrast"]),
        "edges_tagged_by_type": {k: sum(1 for e in edges.values() if e["kind"] == k
                                        and any(p["concept"] for p in e["parts"]))
                                 for k in ("prerequisite", "parallel")},
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
