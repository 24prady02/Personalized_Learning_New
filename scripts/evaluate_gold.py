"""Score the classifier against the gold answer key (data/gold_19.md).

Per scenario it checks:

* main concept (gold or an accepted alternative) and overall level;
* every gold concept's level (within its accepted levels);
* gold edges: ``confirmed`` must be read as stated by the student (an edge
  MATCH or an edge on the student route), ``broken`` must be reported as
  broken; ``context`` edges are listed but not scored;
* misconceptions held (by name) and the correct-side misconceptions that
  must NOT be flagged;
* the root cause concept.

    python scripts/evaluate_gold.py [--ids S016,S137]

Writes output/eval/gold/report.md and results.json.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from lp_graph.graph import KG  # noqa: E402
from lp_graph.pipeline import assess  # noqa: E402


def parse_gold(path: Path) -> dict[str, dict]:
    out = {}
    for block in path.read_text(encoding="utf-8").split("\n## ")[1:]:
        sid = block.split(" ", 1)[0].strip()
        g: dict = {"concepts": {}, "edges": {}, "held": [], "ok": [], "root": None}
        m = re.search(r"\*\*Main concept:\*\* `([^`]+)`(?: \(also accept: ([^)]*)\))?", block)
        g["main"] = [m.group(1)] + re.findall(r"`([^`]+)`", m.group(2) or "")
        m = re.search(r"\*\*Overall level:\*\* (L\d)(?: \(accept ([^)]*)\))?", block)
        g["level"] = sorted({m.group(1)} | set(re.findall(r"L\d", m.group(2) or "")))
        for row in re.finditer(r"^\| `([a-z_]+)` \| (L\d) \| ([^|]*) \|", block, re.M):
            g["concepts"][row.group(1)] = sorted({row.group(2)} | set(re.findall(r"L\d", row.group(3))))
        for row in re.finditer(r"^\| `((?:pre|par):[^`]+)` \| (\w+) \|", block, re.M):
            g["edges"][row.group(1)] = row.group(2)
        g["held"] = re.findall(r"\*\*Misconception held:\*\* `([^`]+)`", block)
        g["ok"] = re.findall(r"must NOT be flagged\):\*\* `([^`]+)`", block)
        m = re.search(r"\*\*Root cause:\*\* `([^`]+)`", block)
        g["root"] = m.group(1) if m else None
        out[sid] = g
    return out


def score(g: dict, a) -> dict:
    d = a.to_dict()
    levels = {c: r["level"] for c, r in d["levels"].items()}
    route_edges = set(d["route_student"]["edges"])
    match_edges = {r["id"] for r in d["readings"] if r["kind"] == "edge" and r["label"].startswith("MATCH")}
    confirmed = route_edges | match_edges | set(d.get("confirmed_edges", []))
    broken = {b["edge"] for b in d["comparison"]["broken"]}
    held = {m["id"] for m in d["misconceptions"] if m["status"] == "held"}
    rows = {"main": (d["main_concept"] in g["main"], d["main_concept"], g["main"]),
            "level": (d["headline_level"] in g["level"], d["headline_level"], g["level"])}
    rows["concepts"] = {c: (levels.get(c, "none") in acc, levels.get(c, "none"), acc)
                        for c, acc in g["concepts"].items()}
    rows["edges"] = {}
    for e, status in g["edges"].items():
        if status == "confirmed":
            rows["edges"][e] = (e in confirmed, "confirmed" if e in confirmed else
                                ("broken" if e in broken else "not read"), status)
        elif status == "broken":
            rows["edges"][e] = (e in broken, "broken" if e in broken else
                                ("confirmed" if e in confirmed else "not read"), status)
        else:
            rows["edges"][e] = (None, "broken" if e in broken else ("confirmed" if e in confirmed else "-"), status)
    rows["held"] = {m: (m.split("->")[1] in held, m.split("->")[1]) for m in g["held"]}
    rows["not_flagged"] = {m: (m.split("->")[1] not in held, m.split("->")[1]) for m in g["ok"]}
    extra = sorted(held - {m.split("->")[1] for m in g["held"]})
    rows["extra_held"] = extra
    rows["route_edges"] = {e: e in route_edges for e, st in g["edges"].items() if st == "confirmed"}
    roots = [rc["concept"] for rc in d["root_causes"]]
    rows["root"] = (None if not g["root"] else (g["root"].split(" / ")[0] in roots or
                    (bool(roots) and roots[0] == g["root"].split(" / ")[0])), roots[:2], g["root"])
    return rows


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ids")
    ap.add_argument("--tag", default="gold")
    args = ap.parse_args()
    gold = parse_gold(ROOT / "data" / "gold_19.md")
    held = {r["id"]: r for r in json.load(open(ROOT / "data" / "heldout_365.json", encoding="utf-8"))["rows"]}
    ids = args.ids.split(",") if args.ids else list(gold)
    kg = KG()
    tot = {"main": [0, 0], "level": [0, 0], "concepts": [0, 0], "edges_confirmed": [0, 0],
           "confirmed_on_viterbi_route": [0, 0],
           "edges_broken": [0, 0], "held": [0, 0], "not_flagged": [0, 0], "root": [0, 0]}
    lines, results = [], {}
    for sid in ids:
        g, r = gold[sid], held[sid]
        a = assess(r["code"], r["question"], r["answer"], kg)
        s = score(g, a)
        results[sid] = s
        mark = lambda ok: "ok " if ok else ("-  " if ok is None else "NO ")  # noqa: E731
        lines.append(f"## {sid}")
        lines.append(f"  {mark(s['main'][0])} main      got {s['main'][1]}  gold {'/'.join(s['main'][2])}")
        lines.append(f"  {mark(s['level'][0])} level     got {s['level'][1]}  gold {'/'.join(s['level'][2])}")
        tot["main"][0] += s["main"][0]; tot["main"][1] += 1
        tot["level"][0] += s["level"][0]; tot["level"][1] += 1
        for c, (ok, got, acc) in s["concepts"].items():
            lines.append(f"  {mark(ok)} concept   {c:22} got {got:5} gold {'/'.join(acc)}")
            tot["concepts"][0] += ok; tot["concepts"][1] += 1
        for e, (ok, got, status) in s["edges"].items():
            lines.append(f"  {mark(ok)} edge      {e:44} got {got:10} gold {status}")
            if status in ("confirmed", "broken"):
                tot[f"edges_{status}"][0] += ok; tot[f"edges_{status}"][1] += 1
        for e, on in s["route_edges"].items():
            tot["confirmed_on_viterbi_route"][0] += on
            tot["confirmed_on_viterbi_route"][1] += 1
        for m, (ok, name) in s["held"].items():
            lines.append(f"  {mark(ok)} held      {name}")
            tot["held"][0] += ok; tot["held"][1] += 1
        for m, (ok, name) in s["not_flagged"].items():
            lines.append(f"  {mark(ok)} not flag  {name}")
            tot["not_flagged"][0] += ok; tot["not_flagged"][1] += 1
        if s["extra_held"]:
            lines.append(f"  !! extra misconceptions reported: {', '.join(s['extra_held'])}")
        if s["root"][0] is not None:
            lines.append(f"  {mark(s['root'][0])} root      got {s['root'][1]}  gold {s['root'][2]}")
            tot["root"][0] += s["root"][0]; tot["root"][1] += 1
    summary = ["", "TOTALS"] + [f"  {k:16} {v[0]}/{v[1]}" for k, v in tot.items()]
    out = ROOT / "output" / "eval" / args.tag
    out.mkdir(parents=True, exist_ok=True)
    (out / "report.md").write_text("\n".join(lines + summary) + "\n", encoding="utf-8")
    json.dump(results, open(out / "results.json", "w", encoding="utf-8"), indent=1, default=str)
    print("\n".join(lines + summary))


if __name__ == "__main__":
    main()
