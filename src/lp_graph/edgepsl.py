"""Everything from edge reading: PSL decides which edges reason best, PCST keeps
the connected set.

Every edge out of a candidate concept node is a candidate, read through its own
edge logic:

* relation edges (prerequisite / parallel) to another candidate concept;
* misconception edges (the wrong belief);
* correct-rule edges (a misconception edge's twin logic);
* level edges, one per way of L1..L4 (its text, gated by the way's own
  ``requires`` neighbours and evidence kind; its slots count as exact evidence).

Each answer sentence gets a reading score for each edge of the concepts it
touches (TF-IDF retrieval + meaning, as a ratio to the graph-calibrated
threshold; an exact slot match counts 2), turned into a truth value
``p / (1 + p)``.

PSL (squared hinges, psl._LP) then reasons over all edges at once:

* score(s, e)                         -> X(s, e)          w 1
* X(s, wrong belief of m) + X(s, correct rule of m) <= 1     w 10
  (contradicting edges compete for a sentence: the stronger reading wins,
  equal readings cancel; level ways do not contradict each other)
* X(s, e)                             -> E(e)             w 10  (relation, level, correct rule)
* X(s, wrong of m) and not X(s, right of m) -> E(m)      w 10
* an L3/L4 way requiring nothing specific: X(s, way) + X(s, best lower way) <= 1
  and X(s, way) and not X(s, best lower way) -> E(way)    w 10
* E(level edge c, L)                  -> Lev(c, L)        w 10
* E(correct-rule edge of c)           -> Lev(c, L1)       w 1
* Lev(c, Lk)                          -> Lev(c, Lk-1)     w 10
* E(misconception edge of c)          -> not Lev(c, L)    w 10
* E(relation e to an L3 neighbour of c) and Lev(c, L2) -> Lev(c, L3)   w 1
* E(misconception edge of c) and E(relation e at c) -> Broken(e)      w 10
* priors: not X, not E, not Lev, not Broken (tiny linear pull)

Evidence the reader got from reading the code (readings) enters as evidence on
the edge itself. PCST (pcst._pcst) then keeps the connected set of edges from
the main concept and the concepts the answer names, with the PSL truth values
as prizes.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from . import lexicon
import os

from .endnode import _closeness, _distinct, _gate, _slot_match
from .pcst import LEVELS, STRONG, Node, Tree, _pcst, _ratio, _result
from .psl import W_EVIDENCE, W_GRAPH, W_PRIOR, _LP, _truth

if TYPE_CHECKING:  # pragma: no cover
    from .candidates import Candidates
    from .graph import KG
    from .reader import Reader
    from .statements import Statement


def _edges_of(kg: "KG", cands: "Candidates") -> dict[str, list[tuple[str, str, list[str], dict]]]:
    """Per concept: its candidate edges as (edge key, kind, texts, info)."""
    cset = set(cands.concepts)
    out: dict[str, list] = {c: [] for c in cset}
    for e in cands.relation_edges:
        if e.src in cset and e.dst in cset:
            texts = [p["text"] for p in kg.parts["edges"].get(e.id, {}).get("parts", []) if p["from"] == "logic"]
            texts += [e.logic] if e.logic else []
            info = {"edge": e, "slots": [s for p in kg.parts["edges"].get(e.id, {}).get("parts", [])
                                         for s in p.get("slots", [])]}
            out[e.src].append((f"E:{e.id}", "E", texts, info))
            out[e.dst].append((f"E:{e.id}", "E", texts, info))
    for m in cands.mis_edges:
        if m.concept in cset and m.wrong and m.right:
            out[m.concept].append((f"M:{m.concept}:{m.mis}", "M", [m.wrong], {"mis": m}))
            out[m.concept].append((f"R:{m.concept}:{m.mis}", "R", [m.right], {"mis": m}))
    for c in cset:
        for lv in LEVELS:
            rows = kg.parts["ways"].get(c, {}).get(lv, [])
            for i, w in enumerate(kg.ways(c, lv)):
                if w.text:
                    row = rows[i] if i < len(rows) else {}
                    out[c].append((f"W:{c}:{lv}:{i}", "W", [w.text], {"level": lv, "row": row}))
    return out


def _contradicts(wrong: str, logic: str) -> bool:
    """LP_GRAPH_CONTRA_BREAK=1: the reader finds the wrong belief contradicts
    the edge's logic (graph text against graph text, p >= 0.5). Off: any held
    misconception at an endpoint can break the edge (the earlier rule)."""
    if os.environ.get("LP_GRAPH_CONTRA_BREAK", "0") != "1":
        return True
    if not wrong or not logic:
        return False
    from . import conceptnli

    return conceptnli.test(wrong, [logic])[0][1] >= 0.5


def _contrasted(info: dict) -> bool:
    """An L3 / L4 way that requires nothing specific of the sentence: no
    neighbour, and evidence a plain statement could give."""
    row = info.get("row", {})
    return info["level"] in ("L3", "L4") and not row.get("requires") \
        and row.get("evidence", "statement") in ("statement", "relation", "run")


# --------------------------------------------------------------- best match
def _claim_slots(st: "Statement") -> set[tuple[str, str, bool]]:
    """What the claim says, as slots (expression values need the program and
    are left out)."""
    return {(x.name, x.value, bool(x.negated)) for x in st.slots if not x.implied and x.name != "expr"}


def _edge_slots(kg: "KG", kind: str, info: dict) -> list:
    if kind == "M":
        return kg.parts["misconceptions"].get(info["mis"].id, {}).get("wrong_slots") or []
    if kind == "R":
        return kg.parts["misconceptions"].get(info["mis"].id, {}).get("right_slots") or []
    if kind == "W":
        return info["row"].get("slots") or []
    return info.get("slots") or []


def _hits(claim: set, slots: list) -> int:
    return len({(x[0], x[1], bool(x[2])) for x in slots if x[0] != "expr"} & claim)


def best_match(kg: "KG", reader: "Reader", st: "Statement", cand: list) -> list[tuple]:
    """The edge logic a claim matches the most, among ``cand`` (concept, key,
    kind, texts, info): slots first (same slot and value), meaning of the
    distinguishing phrases to break ties or for claims without slots; the
    winner must lead by the calibrated margin. When only level ways of one
    concept stay tied, the claim shows at least the lowest of them. Otherwise
    the claim gives no evidence. Returns [(concept, key, kind, prize)]."""
    claim = _claim_slots(st)
    scored = []
    for c, key, kind, texts, info in cand:
        h = _hits(claim, _edge_slots(kg, kind, info))
        r = _ratio(reader, st.text, texts)
        if h or r >= 1:
            scored.append((c, key, kind, texts, info, h, r))
    if not scored:
        return []
    top_h = max(x[5] for x in scored)
    pool = [x for x in scored if x[5] == top_h]
    if len(pool) == 1:
        x = pool[0]
        return [(x[0], x[1], x[2], 2.0 if top_h else x[6])]
    pool = sorted(pool, key=lambda x: (-x[6], x[1]))[:6]
    meaning = reader.meaning()
    if meaning is not None:
        texts = [" ".join(x[3]) for x in pool]
        close = []
        for i, x in enumerate(pool):
            keys = _distinct(meaning, texts[i], [y for j, y in enumerate(texts) if j != i])
            close.append((_closeness(meaning, st.text, keys)[0], i))
        close.sort(key=lambda z: (-z[0], z[1]))
        if close[0][0] - close[1][0] >= meaning.margin:
            x = pool[close[0][1]]
            return [(x[0], x[1], x[2], 2.0 if top_h else max(x[6], 1.0))]
    if all(x[2] == "W" for x in pool) and len({x[0] for x in pool}) == 1:
        x = min(pool, key=lambda z: (z[4]["level"], -z[6]))
        return [(x[0], x[1], x[2], 2.0 if top_h else x[6])]
    return []


def solve_edges(kg: "KG", cands: "Candidates", reader: "Reader", a_st: list["Statement"],
                readings: list[dict]) -> Tree:
    answer = [s for s in a_st if s.source == "answer" and s.text.strip()]
    # the student's concept map: concepts a sentence names (alias, symbol,
    # own code) or points at (a variable, value or code it mentions: the
    # statement's context), plus the question's main concept when the answer
    # addresses it; graph neighbours the student never touches stay out. A
    # relation edge counts only where one sentence involves both ends.
    main = cands.main_concept
    middle = os.environ.get("LP_GRAPH_MAP", "all") == "middle"
    named = {s.id: set(s.concepts) | ({main} if main and main in s.concepts else set())
             for s in a_st if s.source in ("answer", "answer_code")}
    student = set().union(*named.values()) if named else set()
    if main:
        student.add(main)            # the answer answers the question about it
    if not middle:                   # every candidate concept (code concepts and their links)
        student = set(cands.concepts)
    edges = {c: es for c, es in _edges_of(kg, cands).items() if c in student}
    lp = _LP()
    best_sid: dict[str, tuple[float, str]] = {}
    # ---- hypothesis test: all of the student's logic about a concept is the
    # premise, each clause of the concept's edge logic a hypothesis (conceptnli)
    read_nli = os.environ.get("LP_GRAPH_READ", "") == "nli"
    evid: dict[str, float] = {}          # entailment per edge (for LP_GRAPH_PSL=0)
    if read_nli:
        from . import conceptnli

        for c in sorted(edges):
            mine = [s for s in answer if c in named.get(s.id, set())]
            if not mine:
                continue
            premise = " ".join(s.text.strip() for s in mine)
            sid = next((s.id for s in mine if c in s.direct), mine[0].id)
            cand = []
            for key, kind, texts, info in edges[c]:
                if kind == "W" and not any(_gate(s, info["row"]) for s in mine):
                    continue
                if kind == "E" and info["edge"].other(c) not in set().union(*(set(s.concepts) for s in mine)):
                    continue
                cand.append((key, kind, " ".join(texts)))
            if not cand:
                continue
            # a sentence that entails a wrong belief of c (and not its correct
            # rule) shows the misconception, not a level: it is left out of the
            # premise the level ways are tested against
            wrongs = [(" ".join(t2), " ".join(t3)) for k2, kind2, t2, _ in edges[c] if kind2 == "M"
                      for k3, kind3, t3, _ in edges[c] if kind3 == "R" and k3 == "R" + k2[1:]]
            sound = []
            for s in mine:
                if wrongs:
                    rs = conceptnli.test(s.text, [w for w, _ in wrongs] + [r for _, r in wrongs])
                    n = len(wrongs)
                    if any(rs[i][0] >= 0.5 and rs[i][0] > rs[n + i][0] for i in range(n)):
                        continue
                sound.append(s)
            level_premise = " ".join(s.text.strip() for s in sound)
            res = conceptnli.test(premise, [h for _, kind, h in cand if kind != "W"])
            res_w = conceptnli.test(level_premise, [h for _, kind, h in cand if kind == "W"]) if sound else \
                [(0.0, 0.0)] * sum(1 for _, kind, _ in cand if kind == "W")
            it, iw = iter(res), iter(res_w)
            res = [next(iw) if kind == "W" else next(it) for _, kind, _ in cand]
            xs = {}
            for (key, kind, _), (ent, _con) in zip(cand, res):
                if ent <= 0.0:
                    continue
                evid[key] = max(evid.get(key, 0.0), ent)
                x = lp.var(f"X:{c}:{key}")
                xs[key] = x
                lp.rule(W_EVIDENCE, {x: -1.0}, ent)                  # entailment -> X
                lp.rule(W_PRIOR, {x: 1.0}, 0.0)
                if kind != "M":
                    lp.rule(W_GRAPH, {x: 1.0, lp.var("e:" + key): -1.0}, 0.0)
                if ent > best_sid.get(key, (0.0, ""))[0]:
                    best_sid[key] = (ent, sid)
            for key, kind, _ in cand:
                if kind != "M" or key not in xs:
                    continue
                xr = xs.get("R" + key[1:])
                ev = lp.var("e:" + key)
                if xr is None:
                    lp.rule(W_GRAPH, {xs[key]: 1.0, ev: -1.0}, 0.0)
                else:
                    # the wrong belief and its correct rule compete; the
                    # misconception holds by how much its entailment wins
                    lp.rule(W_GRAPH, {xs[key]: 1.0, xr: 1.0}, -1.0)
                    lp.rule(W_GRAPH, {xs[key]: 1.0, xr: -1.0, ev: -1.0}, 0.0)
    # ---- best match: each claim feeds only the edge logic it matches the most
    best = os.environ.get("LP_GRAPH_BESTMATCH", "0") == "1" and not read_nli
    if best:
        for s in answer:
            cand, seen_keys = [], set()
            for c in sorted(named.get(s.id, set()) & set(edges)):
                for key, kind, texts, info in edges[c]:
                    if key in seen_keys or (kind in ("M", "R") and s.hypothetical):
                        continue
                    if kind == "W" and not _gate(s, info["row"]):
                        continue
                    seen_keys.add(key)
                    cand.append((c, key, kind, texts, info))
            for c, key, kind, p in best_match(kg, reader, s, cand):
                x = lp.var(f"X:{s.id}:{c}:{key}")
                lp.rule(W_EVIDENCE, {x: -1.0}, _truth(p))
                lp.rule(W_PRIOR, {x: 1.0}, 0.0)
                lp.rule(W_GRAPH, {x: 1.0, lp.var("e:" + key): -1.0}, 0.0)
                if p > best_sid.get(key, (0.0, ""))[0]:
                    best_sid[key] = (p, s.id)
    # ---- reading: score of each sentence for each edge of its concepts
    for s in (answer if not (best or read_nli) else []):
        mine = named.get(s.id, set())
        for c in sorted(mine & set(edges)):
            contrast: list[tuple[str, str, str, float]] = []
            lower: list[tuple[float, str]] = []
            for key, kind, texts, info in edges[c]:
                if kind in ("M", "R") and s.hypothetical:
                    continue
                if middle and kind == "E" and not ({info["edge"].src, info["edge"].dst} <= mine):
                    continue
                if kind == "W" and not _gate(s, info["row"]):
                    continue
                if middle and kind == "W" and not set(info["row"].get("requires", [])) <= set(s.direct):
                    continue                 # relating to a neighbour means talking about it
                p = 2.0 if _slot_match(s, info.get("row", {}).get("slots") or info.get("slots")) else 0.0
                p = max(p, _ratio(reader, s.text, texts))
                t = _truth(p)
                if t <= 0:
                    continue
                x = lp.var(f"X:{s.id}:{c}:{key}")
                lp.rule(W_EVIDENCE, {x: -1.0}, t)                        # score -> X
                lp.rule(W_PRIOR, {x: 1.0}, 0.0)
                if middle and kind == "W" and _contrasted(info):
                    contrast.append((key, info["level"], x, t))   # decided below
                elif kind != "M":
                    lp.rule(W_GRAPH, {x: 1.0, lp.var("e:" + key): -1.0}, 0.0)  # X -> E
                if kind == "W" and info["level"] in ("L1", "L2"):
                    lower.append((t, x))
                if p > best_sid.get(key, (0.0, ""))[0]:
                    best_sid[key] = (p, s.id)
            # a higher way that requires nothing specific (no neighbour, no
            # what-if, no correction) holds only by how much the sentence reads
            # it better than the concept's best lower way (L1/L2)
            best_low = max(lower)[1] if lower else None
            for key, lv, x, _ in contrast:
                ev = lp.var("e:" + key)
                if best_low is None:
                    lp.rule(W_GRAPH, {x: 1.0, ev: -1.0}, 0.0)
                else:
                    lp.rule(W_GRAPH, {x: 1.0, best_low: 1.0}, -1.0)
                    lp.rule(W_GRAPH, {x: 1.0, best_low: -1.0, ev: -1.0}, 0.0)
            # contradicting edges compete for the sentence: a wrong belief and
            # its correct rule (the stronger reading wins; equal ones cancel)
            for key, kind, _, _ in edges[c]:
                if kind != "M":
                    continue
                xm, xr = f"X:{s.id}:{c}:{key}", f"X:{s.id}:{c}:R" + key[1:]
                if xm in lp.index and xr in lp.index:
                    lp.rule(W_GRAPH, {xm: 1.0, xr: 1.0}, -1.0)
                    # X(wrong) and not X(right) -> Held: it holds by how much the
                    # wrong reading beats the correct one
                    lp.rule(W_GRAPH, {xm: 1.0, xr: -1.0, lp.var("e:" + key): -1.0}, 0.0)
                elif xm in lp.index:
                    lp.rule(W_GRAPH, {xm: 1.0, lp.var("e:" + key): -1.0}, 0.0)
    # ---- evidence from reading the code and the answer (reader readings);
    # with execution on these are grounded in the program's runs: a claim the
    # real run confirms is level evidence of its class (trace -> L2, what-if ->
    # L4, relation -> L3, rule -> L1), a claim a misread run confirms is a
    # misconception
    lev_sid: dict[tuple[str, str], tuple[float, str, str]] = {}
    for r in readings:
        if r["kind"] == "concept" and r["label"].startswith("MATCH") and r.get("concept") in edges:
            lv = lexicon.CLASS_LEVEL.get(r.get("class", "named"), "L1")
            name = f"L:{r['concept']}:{lv}"
            lp.rule(W_EVIDENCE, {lp.var(name): -1.0}, _truth(STRONG))
            evid[name] = max(evid.get(name, 0.0), _truth(STRONG))
            lev_sid.setdefault((r["concept"], lv), (STRONG, r["statement"], r.get("evidence", "")))
            continue
        if r["kind"] == "misconception" and r["label"] == "MATCH-WRONG":
            key = f"M:{r['concept']}:{r['element'].split(' ')[0]}"
        elif r["kind"] == "edge" and r["label"].startswith("MATCH"):
            key = f"E:{r['id']}"
        else:
            continue
        ends = [r.get("concept")] if r["kind"] == "misconception" else r.get("endpoints", [])
        if not ends or any(c not in student for c in ends):
            continue
        lp.rule(W_EVIDENCE, {lp.var("e:" + key): -1.0}, _truth(STRONG))
        evid[key] = max(evid.get(key, 0.0), _truth(STRONG))
        best_sid.setdefault(key, (STRONG, r["statement"]))
    # ---- graph rules over the concept nodes
    needs = {c: {x for row in kg.parts["ways"].get(c, {}).get("L3", []) for x in row["requires"]}
             for c in edges}
    for c in sorted(edges):
        lev = {lv: lp.var(f"L:{c}:{lv}") for lv in LEVELS}
        for i, lv in enumerate(LEVELS):
            lp.rule(W_PRIOR, {lev[lv]: 1.0}, 0.0)
            if i:
                lp.rule(W_GRAPH, {lev[lv]: 1.0, lev[LEVELS[i - 1]]: -1.0}, 0.0)
        for key, kind, _, info in edges[c]:
            ev = "e:" + key
            if ev not in lp.index:
                continue
            lp.rule(W_PRIOR, {ev: 1.0}, 0.0)
            if kind == "W":
                lp.rule(W_GRAPH, {ev: 1.0, lev[info["level"]]: -1.0}, 0.0)
            elif kind == "R":
                lp.rule(W_EVIDENCE, {ev: 1.0, lev["L1"]: -1.0}, 0.0)
            elif kind == "M":
                for lv in LEVELS:
                    lp.rule(W_GRAPH, {ev: 1.0, lev[lv]: 1.0}, -1.0)
            elif kind == "E":
                other = info["edge"].other(c)
                if other in needs.get(c, ()):
                    lp.rule(W_EVIDENCE, {ev: 1.0, lev["L2"]: 1.0, lev["L3"]: -1.0}, -1.0)
                for k2, kind2, _, info2 in edges[c]:
                    if kind2 == "M" and "e:" + k2 in lp.index and _contradicts(info2["mis"].wrong, info["edge"].logic):
                        b = lp.var("B:" + key)
                        lp.rule(W_PRIOR, {b: 1.0}, 0.0)
                        lp.rule(W_GRAPH, {"e:" + k2: 1.0, ev: 1.0, b: -1.0}, -1.0)
    if os.environ.get("LP_GRAPH_PSL", "1") == "0":
        # no reasoning: each edge's entailment is its value directly; a
        # misconception's is its wrong-belief entailment minus its correct
        # rule's; a level's is its best way's (run A of the comparison)
        val = {}
        for c in sorted(edges):
            for key, kind, _, info in edges[c]:
                if key not in evid:
                    continue
                v = evid[key]
                if kind == "M":
                    v = max(0.0, v - evid.get("R" + key[1:], 0.0))
                val["e:" + key] = v
                if kind == "W":
                    name = f"L:{c}:{info['level']}"
                    val[name] = max(val.get(name, 0.0), v)
        for name, v in evid.items():          # grounded level evidence
            if name.startswith("L:"):
                val[name] = max(val.get(name, 0.0), v)
    else:
        val = lp.solve()

    # ---- PCST over the PSL truth values (pcst.py nodes)
    def prize(v: float) -> float:
        v = min(v, 0.95)
        return v / (1.0 - v)

    nodes: dict[str, Node] = {}
    adj: dict[str, list[tuple[str, float]]] = {}

    def link(a: str, b: str, cost: float) -> None:
        adj.setdefault(a, []).append((b, cost))
        adj.setdefault(b, []).append((a, cost))

    for c in sorted(edges):
        nodes[f"C:{c}"] = Node(f"C:{c}", "C", c)
    seen = set()
    for c in sorted(edges):
        for key, kind, _, info in edges[c]:
            v = val.get("e:" + key, 0.0)
            if kind == "E" and key not in seen and {info["edge"].src, info["edge"].dst} <= student:
                seen.add(key)
                e = info["edge"]
                nodes[key] = Node(key, "E", None, prize(v), best_sid.get(key, (0, None))[1],
                                  f"states the edge logic (psl {v:.2f})", edge=e)
                link(f"C:{e.src}", key, 0.5)
                link(key, f"C:{e.dst}", 0.5)
            elif kind == "M":
                m = info["mis"]
                nodes[key] = Node(key, "M", c, prize(v), best_sid.get(key, (0, None))[1],
                                  f"explains the wrong belief best (psl {v:.2f}): {m.wrong}", mis=m)
                link(f"C:{c}", key, 1.0)
        for lv in LEVELS:
            v = val.get(f"L:{c}:{lv}", 0.0)
            if v <= 0.0:
                continue
            ways = [(best_sid.get(k, (0, None)), info.get("row", {}).get("way", ""))
                    for k, kind, _, info in edges[c] if kind == "W" and info["level"] == lv]
            sid = max((w for w in ways if w[0][1]), default=((0, None), ""), key=lambda w: w[0][0])
            if sid[0][1] is None and (c, lv) in lev_sid:
                # a level grounded in the run (or another reading of the code)
                sid = ((lev_sid[(c, lv)][0], lev_sid[(c, lv)][1]), lev_sid[(c, lv)][2][:40])
            if sid[0][1] is None and any(k[0] == c for k in lev_sid):
                # a level the order rule implies from a grounded higher level
                k = max((k for k in lev_sid if k[0] == c), key=lambda k: k[1])
                sid = ((lev_sid[k][0], lev_sid[k][1]), f"implied by {k[1]}")
            if sid[0][1] is None:
                # a level the order rule implies: shown by the concept's highest way read
                sid = max(((best_sid[k], info.get("row", {}).get("way", ""))
                           for k, kind, _, info in edges[c] if kind == "W" and k in best_sid),
                          default=((0, None), ""), key=lambda w: w[0][0])
            if sid[0][1] is None:
                continue
            nid = f"W:{c}:{lv}"
            nodes[nid] = Node(nid, "W", c, prize(v), sid[0][1],
                              f"states the {lv} way {sid[1]} (psl {v:.2f})", level=lv)
            link(f"C:{c}", nid, 1.0)
    roots = {f"C:{cands.main_concept}"} if cands.main_concept else set()
    roots |= {f"C:{c}" for s in a_st if s.source in ("answer", "answer_code") for c in s.direct}
    roots = {r for r in roots if r in nodes}
    tree = _pcst(nodes, adj, roots)
    out = _result(kg, nodes, tree, cands)
    out.broken = [{"edge": nodes[k[2:]].edge.id, "statement": nodes[k[2:]].statement or "",
                   "source": "psl", "reason": "a misconception held at an endpoint (psl)"}
                  for k, v in val.items() if k.startswith("B:") and v >= 0.5 and k[2:] in nodes]
    return out
