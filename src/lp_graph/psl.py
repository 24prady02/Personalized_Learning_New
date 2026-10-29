"""Probabilistic Soft Logic over the edge logic of the concepts found.

Every unknown is a soft truth value in [0, 1]:

* ``Held(m)``      - the answer holds misconception edge m;
* ``Lev(c, L)``    - concept c is reached at level L (L1..L4);
* ``Stated(e)``    - the answer states relation edge e;
* ``Broken(e)``    - relation edge e is broken.

Evidence comes from the same prizes as pcst.py (TF-IDF retrieval, meaning
reader, readings of the code and answer), turned into truth values
``p / (1 + p)``: a prize at the graph-calibrated threshold (1) is 0.5.

Rules (Lukasiewicz logic; a rule's distance to satisfaction is a hinge):

=====================================================  ======
rule                                                   weight
=====================================================  ======
wrong-side evidence(m)          -> Held(m)             1
correct-side evidence(m)        -> not Held(m)         1
Held(m on c)                    -> not Lev(c, L)       10
Lev(c, Lk)                      -> Lev(c, Lk-1)        10
Held(m on c) and Stated(e at c) -> Broken(e)           10
level evidence(c, L)            -> Lev(c, L)           1
edge evidence(e)                -> Stated(e)           1
Stated(e to an L3 neighbour of c) and Lev(c, L2) -> Lev(c, L3)   1
not Held, not Lev, not Stated, not Broken (priors)     0.01
=====================================================  ======

The weights only rank the kinds of rule (graph rules over evidence; the
priors are a tiny linear pull that only settles otherwise free values);
nothing is fitted to answers or gold. MAP inference minimises the weighted sum
of **squared** hinges (as in PSL), so conflicting evidence is traded in
proportion to its strength (the stronger side wins). The problem is convex;
it is solved with L-BFGS-B from all-zero values, so the result is exact and
deterministic. A value of at least 0.5 is true.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

from .pcst import LEVELS, Node

if TYPE_CHECKING:  # pragma: no cover
    from .graph import KG

W_EVIDENCE, W_GRAPH, W_PRIOR = 1.0, 10.0, 0.01


def _truth(p: float) -> float:
    return p / (1.0 + p) if p > 0 else 0.0


class _LP:
    """Variables in [0, 1] plus one slack per rule; minimise sum w * slack."""

    def __init__(self) -> None:
        self.names: list[str] = []
        self.index: dict[str, int] = {}
        self.rules: list[tuple[float, dict[str, float], float]] = []  # w, coef, const: slack >= coef.x + const

    def var(self, name: str) -> str:
        if name not in self.index:
            self.index[name] = len(self.names)
            self.names.append(name)
        return name

    def rule(self, w: float, coef: dict[str, float], const: float) -> None:
        self.rules.append((w, coef, const))

    def solve(self) -> dict[str, float]:
        """Minimise sum w * max(0, a.x + c)^2 for hinge rules and w * x for the
        prior rules (one variable, coefficient 1, constant 0, weight W_PRIOR)."""
        from scipy.optimize import minimize

        n = len(self.names)
        if n == 0:
            return {}
        hinge = [(w, coef, const) for w, coef, const in self.rules if w != W_PRIOR]
        prior = np.zeros(n)
        for w, coef, _ in self.rules:
            if w == W_PRIOR:
                for name in coef:
                    prior[self.index[name]] += w
        A = np.zeros((len(hinge), n))
        c = np.zeros(len(hinge))
        wv = np.zeros(len(hinge))
        for i, (w, coef, const) in enumerate(hinge):
            for name, v in coef.items():
                A[i, self.index[name]] += v
            c[i], wv[i] = const, w

        def f(x: np.ndarray) -> tuple[float, np.ndarray]:
            r = np.maximum(0.0, A @ x + c)
            return float(wv @ (r * r) + prior @ x), 2 * A.T @ (wv * r) + prior

        res = minimize(f, np.zeros(n), jac=True, method="L-BFGS-B", bounds=[(0.0, 1.0)] * n,
                       options={"maxiter": 2000, "ftol": 1e-12, "gtol": 1e-9})
        return {name: float(res.x[self.index[name]]) for name in self.names}


def infer(kg: "KG", nodes: dict[str, Node]) -> tuple[set[str], list[dict], dict[str, float]]:
    """(kept node ids, broken edges, truth values) by PSL MAP inference."""
    lp = _LP()
    concepts = sorted({n.concept for n in nodes.values() if n.kind == "C"})
    # misconceptions
    for nid, n in nodes.items():
        if n.kind != "M":
            continue
        h = lp.var("H:" + nid)
        t = _truth(getattr(n, "lead", n.prize))
        r = _truth(getattr(n, "against", 0.0))
        lp.rule(W_EVIDENCE, {h: -1.0}, t)                 # t -> H
        if r > 0:
            lp.rule(W_EVIDENCE, {h: 1.0}, r - 1.0)        # r -> not H
        lp.rule(W_PRIOR, {h: 1.0}, 0.0)
    # levels
    for c in concepts:
        for i, lv in enumerate(LEVELS):
            v = lp.var(f"L:{c}:{lv}")
            n = nodes.get(f"W:{c}:{lv}")
            if n is not None and n.prize > 0:
                lp.rule(W_EVIDENCE, {v: -1.0}, _truth(n.prize))
            lp.rule(W_PRIOR, {v: 1.0}, 0.0)
            if i > 0:
                lp.rule(W_GRAPH, {v: 1.0, f"L:{c}:{LEVELS[i - 1]}": -1.0}, 0.0)   # Lk -> Lk-1
        for nid, n in nodes.items():
            if n.kind == "M" and n.concept == c:
                for lv in LEVELS:
                    lp.rule(W_GRAPH, {"H:" + nid: 1.0, f"L:{c}:{lv}": 1.0}, -1.0)  # H -> not Lev
    # relation edges
    needs = {c: {x for row in kg.parts["ways"].get(c, {}).get("L3", []) for x in row["requires"]}
             for c in concepts}
    for nid, n in nodes.items():
        if n.kind != "E":
            continue
        e = n.edge
        s = lp.var("S:" + nid)
        b = lp.var("B:" + nid)
        if n.prize > 0:
            lp.rule(W_EVIDENCE, {s: -1.0}, _truth(n.prize))
        lp.rule(W_PRIOR, {s: 1.0}, 0.0)
        lp.rule(W_PRIOR, {b: 1.0}, 0.0)
        for c in (e.src, e.dst):
            for mid, m in nodes.items():
                if m.kind == "M" and m.concept == c:
                    # H and S -> B
                    lp.rule(W_GRAPH, {"H:" + mid: 1.0, s: 1.0, b: -1.0}, -1.0)
            other = e.other(c)
            if other in needs.get(c, ()) and f"L:{c}:L2" in lp.index:
                # S and L2 -> L3
                lp.rule(W_EVIDENCE, {s: 1.0, f"L:{c}:L2": 1.0, f"L:{c}:L3": -1.0}, -1.0)
    val = lp.solve()

    keep: set[str] = set()
    for name, v in val.items():
        if v < 0.5:
            continue
        kind, _, rest = name.partition(":")
        if kind in ("H", "S"):
            keep.add(rest)
        elif kind == "L":
            c, lv = rest.rsplit(":", 1)
            nid = f"W:{c}:{lv}"
            if nid not in nodes:
                # a level the order rule implies: shown by the concept's highest level evidence
                src = next((nodes[f"W:{c}:{x}"] for x in reversed(LEVELS)
                            if f"W:{c}:{x}" in nodes and nodes[f"W:{c}:{x}"].statement), None)
                if src is None:
                    continue
                nodes[nid] = Node(nid, "W", c, 0.0, src.statement, f"implied by {src.level} (psl)", level=lv)
            keep.add(nid)
    for nid in list(keep):
        if nid in nodes and nodes[nid].concept:
            keep.add(f"C:{nodes[nid].concept}")
        if nid in nodes and nodes[nid].kind == "E":
            keep |= {f"C:{nodes[nid].edge.src}", f"C:{nodes[nid].edge.dst}"}
    broken = []
    for name, v in val.items():
        if name.startswith("B:") and v >= 0.5:
            n = nodes[name[2:]]
            broken.append({"edge": n.edge.id, "statement": n.statement or "", "source": "psl",
                           "reason": "a misconception held at an endpoint (psl)"})
    keep = {k for k in keep if k in nodes}
    return keep, broken, val
