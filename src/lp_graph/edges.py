"""Edge tracing: which relation edges does the student's reasoning state or break?

Run after the concept readings (the concepts are already found). For every
relation edge with an endpoint the answer engages (a concept read in the
answer, or one of its misconceptions) and the other endpoint among the
candidates, the edge's logic is compared with the answer by the NLI edge
reader (``nli.EdgeNLI``, fine-tuned on graph-built pairs only):

1. **Student statement vs edge logic.** The statements most similar to the
   edge (retrieval, no threshold) are compared with the whole logic and with
   the parts about a concept the statement itself is about (a statement about
   print is never compared with the part about println). A statement that
   agrees -> the edge is **confirmed**. A "contradicts" verdict here is not
   used: on student wording the model over-calls contradiction (it was
   trained on graph text only), so it cannot break an edge by itself.
2. **Held misconception vs edge logic.** For a misconception the student holds
   on concept c, every edge at c or at a neighbour of c whose logic the wrong
   belief contradicts is **broken** - the belief cannot be held together with
   that edge. This compares graph text with graph text, which is what the
   model was trained on. The other endpoint gets the misconception too when
   the graph attaches that misconception to it.

Returns reading rows (kind ``edge``, class ``relation``) that levels.py turns
into L3 / L1 evidence and broken-link entries for compare.py. Without the
fine-tuned model nothing is added.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from .nli import edge_nli

if TYPE_CHECKING:  # pragma: no cover
    from .candidates import Candidates
    from .graph import KG, RelEdge
    from .statements import Statement


def _parts(kg: "KG", e: "RelEdge", about: set[str] | None = None) -> list[str]:
    """The edge's whole logic and its parts; with ``about``, only the parts
    tagged with one of those concepts (or untagged)."""
    info = kg.parts["edges"].get(e.id, {})
    texts = [p["text"] for p in info.get("parts", []) if p["from"] == "logic" and len(p["text"]) >= 12
             and (about is None or p["concept"] is None or p["concept"] in about)]
    return list(dict.fromkeys(([e.logic] if e.logic else []) + texts))


def _edge_text(eid: str) -> str:
    body = eid.split(":", 1)[1]
    return "edge " + body.replace("->", " -> ").replace("~", " ~ ")


def trace_edges(kg: "KG", cands: "Candidates", a_st: list["Statement"], readings: list[dict],
                misconceptions: list[dict]) -> tuple[list[dict], list[dict], list[dict]]:
    """(edge reading rows, broken links, extra misconception rows).

    A. An edge between two concepts the same statement already shows (both
       read in it) is used by that reasoning: broken when the statement holds
       a misconception of an endpoint or a claim an endpoint produced is
       contradicted, confirmed when both endpoints read correctly.
    B. (reader.py) An edge whose logic a statement states is read there.
    C. With the fine-tuned NLI model: an edge whose logic a held
       misconception's wrong belief contradicts is broken (graph text against
       graph text, which the model was trained on)."""
    rows: list[dict] = []
    broken: list[dict] = []
    extra: list[dict] = []
    status: dict[str, str] = {r["id"]: ("broken" if r["label"] == "CONTRADICT" else "confirmed")
                              for r in readings if r["kind"] == "edge" and r["label"] != "NO"}
    by_stmt: dict[str, dict[str, set[str]]] = {}
    for r in readings:
        if r["kind"] in ("concept", "misconception") and r.get("concept"):
            lab = "wrong" if r["label"] in ("MATCH-WRONG", "CONTRADICT") else (
                "ok" if r["label"].startswith("MATCH") or r["label"] == "CONTRADICT-RIGHT" else "")
            if lab:
                by_stmt.setdefault(r["statement"], {}).setdefault(r["concept"], set()).add(lab)
    for e in cands.relation_edges:
        if e.id in status:
            continue
        both = [(sid, cs) for sid, cs in sorted(by_stmt.items()) if e.src in cs and e.dst in cs]
        # a statement that is wrong about an endpoint breaks the edge, whatever the others say
        both.sort(key=lambda x: (not ("wrong" in x[1][e.src] or "wrong" in x[1][e.dst]), x[0]))
        for sid, cs in both:
            if True:
                bad = "wrong" in cs[e.src] or "wrong" in cs[e.dst]
                st = "broken" if bad else "confirmed"
                status[e.id] = st
                rows.append({"statement": sid, "kind": "edge", "element": _edge_text(e.id), "id": e.id,
                             "label": "CONTRADICT" if bad else "MATCH", "class": "relation",
                             "endpoints": [e.src, e.dst], "source": "reasoning",
                             "evidence": "both ends read in the same statement" + (" (one wrong)" if bad else "")})
                if bad:
                    broken.append({"edge": e.id, "statement": sid, "parts": [], "stateable": e.stateable,
                                   "quote": next((s.text for s in a_st if s.id == sid), ""),
                                   "reason": "an endpoint is read wrong in this statement"})
                break

    model = edge_nli()
    if model is None:
        return rows, broken, extra
    held = [m for m in misconceptions if m["status"] == "held"]
    engaged = {r["concept"] for r in readings if r.get("concept") and r["label"] != "NO"}
    pool = engaged | set(cands.concepts) | {m["concept"] for m in held}
    statements = [s for s in a_st if s.source in ("answer", "answer_code")]
    for m in held:
        c = m["concept"]
        near_c = {c} | set(kg.adjacency.get(c, []))
        for e in sorted(kg.relation_edges.values(), key=lambda x: x.id):
            if status.get(e.id) == "broken" or not ({e.src, e.dst} & near_c) or not ({e.src, e.dst} <= pool):
                continue
            hit = None
            for part in _parts(kg, e):
                v, p = model.verdict(part, m["wrong"])
                if v == "contradicts" and (hit is None or p > hit[0]):
                    hit = (p, part)
            if hit is None:
                continue
            status[e.id] = "broken"
            sid = m["statements"][0] if m["statements"] else (statements[0].id if statements else "")
            broken.append({"edge": e.id, "statement": sid, "parts": [], "stateable": e.stateable,
                           "quote": m["wrong"], "reason": f"{m['id']} contradicts: {hit[1]}"})
            rows.append({"statement": sid, "kind": "edge", "element": _edge_text(e.id), "id": e.id,
                         "label": "CONTRADICT", "class": "relation", "endpoints": [e.src, e.dst], "source": "nli",
                         "evidence": f"the held misconception {m['id']} contradicts ({hit[0]:.2f}): {hit[1]}"})
            for end in (e.src, e.dst):
                mis_edge = next((x for x in kg.mis_edges.get(end, []) if x.mis == m["id"]), None)
                if mis_edge and end != c:
                    extra.append({"statement": sid, "kind": "misconception", "id": mis_edge.id,
                                  "element": f"{m['id']} (on {end}, {mis_edge.role})", "label": "MATCH-WRONG",
                                  "class": "wrong", "concept": end, "role": mis_edge.role, "source": "nli",
                                  "evidence": f"reached through broken {e.id}"})
    return rows, broken, extra
