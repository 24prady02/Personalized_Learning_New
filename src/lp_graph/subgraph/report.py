"""Report CLI: one line per scenario, then ``fully covered: N / 20``.

    python -m lp_graph.subgraph.report --kg data/raw/chapter1_kg.json --gold data/raw/scenarios_20.json [--json OUT_DIR]
"""
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

from .extract import subgraph_from_code

# Concepts that the question or the student's answer brings in; they are not in the code.
NOT_IN_CODE = {
    "S005": {"while_loop"},            # the code is a do-while; the student compares it with a while loop
    "S016": {"integer_division"},      # the code has % but no /; the student brings division in
    "S023": {"break_statement"},       # the switch has no break; the student explains the missing break
    "S073": {"break_statement"},
    "S009": {"array_bounds", "array_creation", "indexing", "length_field"},  # array_creation: endpoint of the gold context edge, also not in the code
    "S010": {"array_bounds", "array_copy", "array_traversal", "for_loop", "indexing", "off_by_one_error"},
    "S012": {"compound_assignment", "increment_operators"},
    "S015": {"char", "naming_convention", "variable"},
    "S057": {"explicit_cast"},
    "S068": {"power_method", "two_models"},
}


def load_gold(path: Path) -> list[dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    return data["scenarios"] if isinstance(data, dict) else data


def gold_concepts(sc: dict) -> set[str]:
    """Concepts in ``levels``, both ends of each edge, and the concepts whose
    misconceptions are in ``held`` / ``correct`` (resolved through the edge id
    when present, else the level concepts)."""
    g = sc.get("gold", sc)
    need = set(g.get("levels", {}))
    for e in g.get("edges", []):
        eid = e["id"] if isinstance(e, dict) else e
        body = eid.split(":", 1)[1]
        a, b = (body.split("->") if "->" in body else body.split("~"))
        need.update([a, b])
    return need


def run(kg_path: Path, gold_path: Path, out_dir: Path | None = None, kg=None, hops: int = 0) -> dict:
    kg = kg or json.loads(kg_path.read_text(encoding="utf-8"))
    generic = {c["id"] for c in kg["concepts"] if (c.get("reader") or {}).get("generic")}
    scenarios = load_gold(gold_path)
    lines = []
    covered = 0
    fire = Counter()
    sizes = []
    results = {}
    for sc in scenarios:
        sid = sc["id"]
        is_ref = bool(sc.get("reference_case"))
        sg = subgraph_from_code(sc["code"], kg, sid, hops)
        got = {c["id"] for c in sg["concepts"]}
        tagged = {c["id"] for c in sg["concepts"] if c["why"] == "code"}
        if not is_ref:
            fire.update(t for t in tagged if t not in generic)
            sizes.append(len(got))
        need = gold_concepts(sc)
        missed = sorted(need - got)
        expected_miss = NOT_IN_CODE.get(sid, set())
        unexpected = sorted(set(missed) - expected_miss)
        if not missed and not is_ref:
            covered += 1
        c = sg["counts"]
        tag = "ref" if is_ref else ("ok" if not missed else ("xfail" if not unexpected else "MISS"))
        lines.append(f"{sid:5} tagged {c['tagged']:3}  nodes {c['concepts']:3} ({c['generic']} generic)  edges {c['concept_edges']:3}  mis {c['mis_edges']:3}  "
                     f"levels {c['levels']:3}  links {c['level_mis_links']:3}  {tag:5} missed: {', '.join(missed) or '-'}")
        results[sid] = {"subgraph": sg, "missed": missed, "unexpected_miss": unexpected}
        if out_dir:
            out_dir.mkdir(parents=True, exist_ok=True)
            (out_dir / f"{sid}_subgraph.json").write_text(json.dumps(sg, indent=1, ensure_ascii=False), encoding="utf-8")
    n = len(sizes)
    lines.append(f"fully covered: {covered} / {n}   (mean concepts per subgraph: {sum(sizes) / max(1, n):.1f}; S000 is the reference case, not counted)")
    broad = [(cid, k) for cid, k in fire.most_common() if k >= 12]
    lines.append("non-generic concepts firing in >= 12 scenarios: " + (", ".join(f"{c} ({k})" for c, k in broad) or "none"))
    return {"lines": lines, "covered": covered, "n": n, "results": results, "fire": fire}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--kg", default="data/raw/chapter1_kg.json")
    ap.add_argument("--gold", default="data/raw/scenarios_20.json")
    ap.add_argument("--json", dest="out_dir", default=None)
    ap.add_argument("--hops", type=int, default=0, help="0 (default): nodes are exactly the tagged concepts; 1: add one prerequisite hop")
    a = ap.parse_args(argv)
    r = run(Path(a.kg), Path(a.gold), Path(a.out_dir) if a.out_dir else None, hops=a.hops)
    print("\n".join(r["lines"]))


if __name__ == "__main__":
    main()
