"""Prize-Collecting Steiner Tree over the edge logic of the concepts found.

The answer is read onto the graph as the connected piece of edge logic it
best expresses. The PCST graph has

* a node per candidate concept;
* a node per relation edge between two candidates (linked to both ends);
* a node per misconception edge of a candidate (linked to its concept);
* a node per level L1..L4 of a candidate (linked to its concept): the level's
  ways are that level's edge logic.

**Prizes** say how well the answer's statements express the node's edge logic,
as a ratio to the graph-calibrated threshold (1 = just stated):

* relation edge: TF-IDF anchors (score / match) or meaning (meaning.py,
  similarity / sent_min) of the edge logic;
* misconception: the statement means the wrong side (meaning lead / margin, or
  TF-IDF distinguishing anchors); evidence the reader got from reading the
  code or the answer (MATCH-WRONG) counts 2;
* level: each statement votes for the level whose ways it is closest to; a
  reading of the concept with an evidence class (named / rule ...) counts 2 for
  that class's level.

**Costs**: 1 per node joined (0.5 per side of a relation-edge node). The roots
are the main concept and the concepts the answer names. The tree grows
greedily (Goemans-Williamson style growth simplified): repeatedly join the
node whose cheapest path from the tree gains the most prize minus cost, while
the gain is positive. Deterministic; no model is trained, no gold is used.

The tree's nodes become reading rows (``source: "pcst"``): misconceptions held,
concept levels, edges stated, and a ``Route`` of its edges for the report.
"""

from __future__ import annotations

import heapq
import os
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from .reader import Reading
from .viterbi import Route, State, Step

if TYPE_CHECKING:  # pragma: no cover
    from .candidates import Candidates
    from .graph import KG
    from .reader import Reader
    from .statements import Statement

LEVELS = ("L1", "L2", "L3", "L4")
CLASS_OF = {"L1": "rule", "L2": "run", "L3": "relation", "L4": "hypothetical"}
STRONG = 2.0   # prize of evidence the reader already decided


@dataclass
class Node:
    id: str
    kind: str                 # C | E | M | W
    concept: str | None = None
    prize: float = 0.0
    statement: str | None = None
    evidence: str = ""
    edge: object = None
    mis: object = None
    level: str | None = None
    lead: float = 0.0        # misconception: wrong-side evidence before the correct side counts against
    against: float = 0.0     # misconception: correct-side evidence


@dataclass
class Tree:
    nodes: list[Node] = field(default_factory=list)
    rows: list[dict] = field(default_factory=list)
    route: Route = field(default_factory=Route)
    broken: list[dict] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {"nodes": [{"id": n.id, "prize": round(n.prize, 3), "statement": n.statement,
                           "evidence": n.evidence} for n in self.nodes]}


def _ratio(reader: "Reader", text: str, targets: list[str]) -> float:
    """How well a statement states any of the texts, 1 = at the threshold."""
    targets = [t for t in targets if t]
    if not targets:
        return 0.0
    vs = reader.variables()
    logic = reader.logic
    best = max(logic.score(text, t, vs) for t in targets) / logic.match
    meaning = reader.meaning()
    if meaning is not None:
        best = max(best, meaning.states(text, targets, vs) / meaning.sent_min)
    return best


def _side_lead(reader: "Reader", text: str, m) -> float:
    """Signed lead of the wrong side over the correct side, as a ratio to the
    graph-calibrated margin: > 0 means the wrong belief, < 0 the correct rule.
    Retrieved only when the statement shares an anchor with the edge."""
    vs = reader.variables()
    if reader.logic.score(text, m.wrong, vs) + reader.logic.score(text, m.right, vs) <= 0:
        return 0.0
    meaning = reader.meaning()
    if meaning is None:
        side, score = reader.logic.side(text, m.wrong, m.right, vs)
        return 0.0 if side is None else (1 if side == "a" else -1) * score / reader.logic.match
    sa, sb = meaning.side_scores(text, m.wrong, m.right)
    return (sa - sb) / meaning.margin


def _wrong_side(reader: "Reader", text: str, m) -> float:
    """How clearly a statement means the wrong side of a misconception edge."""
    vs = reader.variables()
    best = 0.0
    side, score = reader.logic.side(text, m.wrong, m.right, vs)
    if side == "a":
        best = score / reader.logic.match
    meaning = reader.meaning()
    if meaning is not None and reader.logic.score(text, m.wrong, vs) + reader.logic.score(text, m.right, vs) > 0:
        sa, sb = meaning.side_scores(text, m.wrong, m.right)
        if sa > sb:
            best = max(best, (sa - sb) / meaning.margin)
    return best


def build(kg: "KG", cands: "Candidates", reader: "Reader", a_st: list["Statement"],
          readings: list[dict], exclusive: bool = False) -> tuple[dict[str, Node], dict[str, list[tuple[str, float]]]]:
    """``exclusive``: a statement that means a misconception's wrong side is
    not also level evidence for that misconception's concept."""
    answer = [s for s in a_st if s.source == "answer" and s.text.strip()]
    plain = [s for s in answer if not s.hypothetical]
    cset = set(cands.concepts)
    nodes: dict[str, Node] = {}
    adj: dict[str, list[tuple[str, float]]] = {}

    def link(a: str, b: str, cost: float) -> None:
        adj.setdefault(a, []).append((b, cost))
        adj.setdefault(b, []).append((a, cost))

    for c in sorted(cset):
        nodes[f"C:{c}"] = Node(f"C:{c}", "C", c)
    # relation edges
    stated = {r["id"]: r for r in readings if r["kind"] == "edge" and r["label"].startswith("MATCH")}
    for e in cands.relation_edges:
        if e.src not in cset or e.dst not in cset:
            continue
        texts = [p["text"] for p in kg.parts["edges"].get(e.id, {}).get("parts", []) if p["from"] == "logic"]
        texts += [e.logic] if e.logic else []
        best, sid = 0.0, None
        for s in plain:
            if not ({e.src, e.dst} & (set(s.concepts) | set(getattr(s, "context", ())))):
                continue
            v = _ratio(reader, s.text, texts)
            if v > best:
                best, sid = v, s.id
        if os.environ.get("LP_GRAPH_ENDNODE", "0") == "1":
            # a slot of an edge-logic part stated with both ends present
            from .endnode import _slot_match

            parts = kg.parts["edges"].get(e.id, {}).get("parts", [])
            for s in plain:
                if {e.src, e.dst} <= set(s.concepts) and any(_slot_match(s, pt.get("slots")) for pt in parts):
                    best, sid = max(best, STRONG), sid or s.id
        if e.id in stated:
            best, sid = max(best, STRONG), sid or stated[e.id]["statement"]
        n = Node(f"E:{e.id}", "E", None, best, sid, f"states the edge logic (pcst {best:.2f})", edge=e)
        nodes[n.id] = n
        link(f"C:{e.src}", n.id, 0.5)
        link(n.id, f"C:{e.dst}", 0.5)
    # misconception edges
    decided = {(r["concept"], r["element"].split(" ")[0]): r for r in readings
               if r["kind"] == "misconception" and r["label"] == "MATCH-WRONG"}
    # each statement votes for the one misconception edge whose wrong side it
    # means most clearly; a statement meaning the correct side counts against
    from . import endnode

    end_nodes = os.environ.get("LP_GRAPH_ENDNODE", "0") == "1"
    lead: dict[str, list[tuple[float, str]]] = {}
    for s in plain:
        best_s = None
        # end-node reading: PageRank candidates, read against all siblings (endnode.py)
        signed = endnode.read_mis(kg, reader, cands, s) if end_nodes else None
        for m in cands.mis_edges:
            if m.concept not in cset or m.concept not in s.concepts or not (m.wrong and m.right):
                continue
            v = signed.get(m.id, 0.0) if signed is not None else _side_lead(reader, s.text, m)
            lead.setdefault(m.id, []).append((v, s.id))
            if v > 0 and (best_s is None or v > best_s[0]):
                best_s = (v, m.id)
        if best_s is not None:
            lead.setdefault("vote:" + best_s[1], []).append((best_s[0], s.id))
    for m in cands.mis_edges:
        if m.concept not in cset:
            continue
        best, sid, ev = 0.0, None, ""
        votes_m = lead.get("vote:" + m.id, [])
        against = max((-v for v, _ in lead.get(m.id, []) if v < 0), default=0.0)
        if votes_m:
            v, sid = max(votes_m)
            best = max(0.0, v - against)
            ev = f"means the wrong belief (lead {v:.2f}, against {against:.2f}): {m.wrong}"
        r = decided.get((m.concept, m.mis))
        if r is not None and STRONG >= best:
            best, sid, ev = STRONG, r["statement"], r.get("evidence", "")
        nid = f"M:{m.concept}:{m.mis}"
        if nid in nodes and nodes[nid].prize >= best:
            continue
        nodes[nid] = Node(nid, "M", m.concept, best, sid, ev, mis=m,
                          lead=STRONG if (r is not None and best == STRONG) else (max(votes_m)[0] if votes_m else 0.0),
                          against=0.0 if (r is not None and best == STRONG) else against)
        link(f"C:{m.concept}", nid, 1.0)
    wrong_sid = {(n.concept, n.statement) for n in nodes.values() if n.kind == "M" and n.prize > 0 and n.statement}
    # levels: each statement votes for its closest level's ways
    votes: dict[tuple[str, str], tuple[float, str, str]] = {}
    for c in sorted(cset):
        ways = {lv: [w.text for w in kg.ways(c, lv) if w.text] for lv in LEVELS}
        for s in answer:
            if c not in s.concepts or (exclusive and (c, s.id) in wrong_sid):
                continue
            if end_nodes:
                # the level end node, read against all of the concept's ways
                # with each way's own requirements (endnode.read_level)
                got = endnode.read_level(kg, reader, c, s)
                if got is None:
                    continue
                lv, v, way = got
                old = votes.get((c, lv), (0.0, "", ""))
                votes[(c, lv)] = (old[0] + v, old[1] or s.id, f"states the {lv} way {way} (pcst)")
                continue
            scored = [(_ratio(reader, s.text, ways[lv]), lv) for lv in LEVELS if ways[lv]]
            if not scored:
                continue
            v, lv = max(scored)
            if v <= 0:
                continue
            old = votes.get((c, lv), (0.0, "", ""))
            votes[(c, lv)] = (old[0] + v, old[1] or s.id, f"states an {lv} way (pcst)")
    from . import lexicon

    for r in readings:
        if r["kind"] == "concept" and r["label"].startswith("MATCH") and r.get("concept") in cset:
            lv = lexicon.CLASS_LEVEL.get(r.get("class", "named"), "L1")
            old = votes.get((r["concept"], lv), (0.0, "", ""))
            if old[0] < STRONG:
                votes[(r["concept"], lv)] = (STRONG, r["statement"], r.get("evidence", ""))
    for (c, lv), (p, sid, ev) in sorted(votes.items()):
        nid = f"W:{c}:{lv}"
        nodes[nid] = Node(nid, "W", c, p, sid, ev, level=lv)
        link(f"C:{c}", nid, 1.0)
    return nodes, adj


def solve(kg: "KG", cands: "Candidates", reader: "Reader", a_st: list["Statement"],
          readings: list[dict], method: str = "pcst") -> Tree:
    """method: pcst | threshold | kshortest | pathrag (same prizes, different
    selection of the edge logic kept)."""
    if method == "edgepsl":
        # everything from edge reading: PSL over all edges, then PCST (edgepsl.py)
        from .edgepsl import solve_edges

        return solve_edges(kg, cands, reader, a_st, readings)
    nodes, adj = build(kg, cands, reader, a_st, readings, exclusive=method.startswith("psl"))
    roots = {f"C:{cands.main_concept}"} if cands.main_concept else set()
    roots |= {f"C:{c}" for s in a_st if s.source in ("answer", "answer_code") for c in s.direct}
    roots = {r for r in roots if r in nodes}
    n_answer = len([s for s in a_st if s.source == "answer"])
    broken: list[dict] = []
    if method.startswith("psl"):
        # PSL reasons over the edge logic first (psl.py); with "psl+<selector>"
        # its truth values become the prizes the path selector works on
        from .psl import infer

        psl_keep, broken, val = infer(kg, nodes)
        if method == "psl":
            out = _result(kg, nodes, psl_keep, cands)
            out.broken = broken
            return out
        for nid, n in nodes.items():
            key = {"M": "H:", "W": "L:", "E": "S:"}.get(n.kind)
            if key is None:
                continue
            name = key + (f"{n.concept}:{n.level}" if n.kind == "W" else nid)
            v = min(val.get(name, 0.0), 0.95)
            n.prize = v / (1.0 - v)          # back to the prize scale (0.5 -> 1)
        method = method[4:]
    if method == "threshold":
        tree = _threshold(nodes, adj)
    elif method == "kshortest":
        tree = _kshortest(nodes, adj, roots)
    elif method == "pathrag":
        tree = _pathrag(nodes, adj, roots, max(1, n_answer))
    else:
        tree = _pcst(nodes, adj, roots)
    out = _result(kg, nodes, tree, cands)
    out.broken = broken
    return out


def _attach_cost(nid: str, adj) -> float:
    ws = [w for _, w in adj.get(nid, [])]
    if not ws:
        return 1.0
    return sum(ws) if nid.startswith("E:") else min(ws)


def _threshold(nodes: dict[str, Node], adj) -> set[str]:
    """TF-IDF / meaning alone: every element whose prize beats its own cost,
    no graph structure."""
    keep = set()
    for nid, n in nodes.items():
        if n.kind != "C" and n.prize > _attach_cost(nid, adj):
            keep.add(nid)
            keep |= {v for v, _ in adj.get(nid, []) if v.startswith("C:")}
    return keep


def _simple_paths(adj, roots: set[str], max_len: int = 7):
    """All simple paths from a root (up to max_len nodes: three concept hops
    and an end node), as (end, path, cost). Only concept and relation-edge
    nodes are passed through."""
    out = []
    stack = [(r, (r,), 0.0) for r in sorted(roots)]
    while stack:
        u, path, cost = stack.pop()
        out.append((u, path, cost))
        if len(path) >= max_len or not (u.startswith("C:") or u.startswith("E:")):
            continue
        for v, w in adj.get(u, []):
            if v not in path:
                stack.append((v, path + (v,), cost + w))
    return out


def _kshortest(nodes: dict[str, Node], adj, roots: set[str]) -> set[str]:
    """k shortest paths: each element is decided on the best of its short
    paths from the roots (prize collected on the path minus its cost); costs
    are not shared between elements."""
    best: dict[str, tuple[float, tuple]] = {}
    for end, path, cost in _simple_paths(adj, roots):
        gain = sum(nodes[x].prize for x in path) - cost
        if end not in best or gain > best[end][0]:
            best[end] = (gain, path)
    keep = set(roots)
    for end, (gain, path) in best.items():
        if nodes[end].kind != "C" and nodes[end].prize > 0 and gain > 0:
            keep |= set(path)
    return keep


def _pathrag(nodes: dict[str, Node], adj, roots: set[str], k: int,
             alpha: float = 0.8, theta: float = 0.05) -> set[str]:
    """PathRAG-style flow pruning: resource 1 at each root flows to the
    neighbours (shared equally, decayed by alpha) and stops below theta; a
    path's reliability is the mean resource of its nodes times its end's
    prize. The k most reliable paths (k = answer statements) are kept."""
    flow: dict[str, float] = {}
    for r in sorted(roots):
        layer, seen = {r: 1.0}, {r}
        while layer:
            nxt: dict[str, float] = {}
            for u, f in layer.items():
                flow[u] = flow.get(u, 0.0) + f
                share = alpha * f / max(1, len(adj.get(u, [])))
                if share < theta:
                    continue
                for v, _ in adj.get(u, []):
                    if v not in seen:
                        nxt[v] = nxt.get(v, 0.0) + share
            seen |= set(nxt)
            layer = nxt
    scored = []
    for end, path, cost in _simple_paths(adj, roots):
        n = nodes[end]
        if n.kind == "C" or n.prize < _attach_cost(end, adj) or any(x not in flow for x in path):
            continue
        scored.append((sum(flow[x] for x in path) / len(path) * n.prize, path))
    scored.sort(key=lambda x: (-x[0], x[1]))
    keep, taken = set(roots), set()
    for rel, path in scored:
        if path[-1] in taken:
            continue
        keep |= set(path)
        taken.add(path[-1])
        if len(taken) >= k:
            break
    return keep


def _pcst(nodes: dict[str, Node], adj, roots: set[str]) -> set[str]:
    """Greedy PCST growth from the roots."""
    tree = set(roots)
    while True:
        # cheapest path from the tree to every node (multi-source Dijkstra)
        dist = {t: 0.0 for t in tree}
        prev: dict[str, str | None] = {t: None for t in tree}
        heap = [(0.0, t) for t in sorted(tree)]
        while heap:
            d, u = heapq.heappop(heap)
            if d > dist.get(u, 1e9):
                continue
            for v, w in adj.get(u, []):
                nd = d + w
                if nd < dist.get(v, 1e9) - 1e-12:
                    dist[v], prev[v] = nd, u
                    heapq.heappush(heap, (nd, v))
        best, best_path = 0.0, None
        for v in sorted(dist):
            if v in tree:
                continue
            path, u = [], v
            while u is not None and u not in tree:
                path.append(u)
                u = prev[u]
            gain = sum(nodes[x].prize for x in path) - dist[v]
            if gain > best + 1e-9:
                best, best_path = gain, path
        if best_path is None:
            break
        tree |= set(best_path)
    return tree


def _result(kg: "KG", nodes: dict[str, Node], tree: set[str], cands: "Candidates") -> Tree:
    out = Tree()
    steps: list[Step] = []
    for nid in sorted(tree):
        n = nodes[nid]
        out.nodes.append(n)
        sid = n.statement
        if n.kind == "E" and sid:
            e = n.edge
            out.rows.append({"statement": sid, "kind": "edge", "id": e.id, "element": e.id,
                             "label": "MATCH", "class": "relation", "endpoints": [e.src, e.dst],
                             "source": "pcst", "evidence": n.evidence, "confidence": round(n.prize, 3)})
            steps.append(Step(State(f"E:{e.id}:fwd", "E", e.src, e.dst, e.id), (sid,), "edge", 0,
                              Reading("MATCH", evidence=n.evidence, cls="relation")))
        elif n.kind == "M" and sid:
            m = n.mis
            out.rows.append({"statement": sid, "kind": "misconception", "id": f"pcst:{nid}",
                             "element": f"{m.mis} (on {m.concept}, pcst)", "label": "MATCH-WRONG",
                             "class": "wrong", "concept": m.concept, "role": m.role or "primary",
                             "source": "pcst", "evidence": n.evidence, "confidence": round(n.prize, 3)})
            steps.append(Step(State(nid, "M", m.concept, m.concept, mis=m.mis), (sid,), "stay", 0,
                              Reading("MATCH-WRONG", evidence=n.evidence)))
        elif n.kind == "W" and sid:
            out.rows.append({"statement": sid, "kind": "concept", "id": nid, "element": f"{n.level} {n.concept}",
                             "label": "MATCH", "class": CLASS_OF[n.level], "concept": n.concept,
                             "source": "pcst", "evidence": n.evidence, "confidence": round(n.prize, 3)})
            steps.append(Step(State(f"N:{n.concept}", "N", n.concept, n.concept), (sid,), "stay", 0,
                              Reading("MATCH", evidence=n.evidence, cls=CLASS_OF[n.level])))
    out.route = Route(steps=steps, cost=0, jumps=0, n_statements=len({s.statements[0] for s in steps}))
    return out
