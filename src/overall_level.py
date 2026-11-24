"""One overall level per scenario from its component levels. The rule and how it was arrived at: LP_level_classified/README.md.

    python src/overall_level.py --scenarios data/raw/scenarios_loop_LP.json [--tag lp] [--out LP_level_classified/results_LP]

The rule:
1. Components: the non-generic concepts that have a level, plus any concept where a real mistake is held (a held
   misconception or error that is not a shadow). A held mistake on a concept without a level counts as L0.
2. A real mistake is held (the walk names a root cause) -> the overall level is L0.
3. Otherwise -> the level with the largest share of components; on a tie, the lower level. No component -> no level.
4. Beside the level: the share of components at each level and the coherence flag (coherent when the component
   levels are at most one level apart, otherwise "LOW coherence").

Step 2 is this project's own step; steps 1, 3 and 4 follow the LP test instructions (after Jin et al.). The share rule
alone (step 3 for every answer) is also reported, for comparison.

The same rule is applied to the expected result of the scenario file ("expected": {"levels": {...}, "held": [...]}),
so the system and the expected result are compared in the same way. Writes <out>.csv and <out>.md.
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from utils import PROCESSED_DIR, RESULTS_DIR, load_scenarios  # noqa: E402

NL = chr(10)


def share_rule(levels: dict[str, str]) -> dict:
    """Component levels -> shares, coherence and the level with the largest share (tie: the lower level)."""
    if not levels:
        return {"shares": {}, "coherent": None, "overall": None}
    count = Counter(levels.values())
    shares = {lv: round(n / len(levels), 2) for lv, n in sorted(count.items())}
    nums = [int(lv[1]) for lv in levels.values()]
    best = max(count.values())
    return {"shares": shares, "coherent": max(nums) - min(nums) <= 1, "overall": min(lv for lv, n in count.items() if n == best)}


overall = share_rule      # earlier name


def overall_level(levels: dict[str, str], mistake_held: bool) -> dict:
    """The rule: a held mistake -> L0; otherwise the share rule. Shares and coherence are reported in both cases."""
    r = dict(share_rule(levels))
    r["share_overall"] = r["overall"]
    if mistake_held:
        r["overall"] = "L0"
    r["by"] = "held mistake" if mistake_held else ("largest share" if levels else "no component")
    return r


def components(diag: dict, sg: dict) -> dict[str, str]:
    generic = {c["id"] for c in sg["concepts"] if c.get("generic")}
    comp = {c: v["level"] for c, v in diag.get("levels", {}).items() if v.get("level") and c not in generic}
    for h in diag.get("held_misconceptions", []):            # a real mistake: the concept is a component, generic or not
        comp[h["concept"]] = (diag.get("levels", {}).get(h["concept"]) or {}).get("level") or "L0"
    return dict(sorted(comp.items()))


def shares_text(r: dict) -> str:
    if not r["shares"]:
        return "no component"
    return ", ".join(f"{lv} {s:.2f}" for lv, s in r["shares"].items()) + ("; coherent" if r["coherent"] else "; LOW coherence")


def main(argv=None) -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--scenarios", required=True)
    ap.add_argument("--tag", default="")
    ap.add_argument("--processed", default=str(PROCESSED_DIR))
    ap.add_argument("--out", default=None, help="output path without extension (default results/overall_level[_<tag>])")
    a = ap.parse_args(argv)
    tag = f".{a.tag}" if a.tag else ""
    rows, n_overall, n_share, n_held, n_root, flagged = [], 0, 0, 0, 0, 0
    for sc in load_scenarios(a.scenarios):
        sid = sc["id"]
        f = Path(a.processed) / f"{sid}_diagnosis{tag}.json"
        if not f.exists():
            print(f"{sid}: no diagnosis ({f.name})")
            continue
        diag = json.loads(f.read_text(encoding="utf-8"))
        sg = json.loads((Path(a.processed) / f"{sid}_subgraph.json").read_text(encoding="utf-8"))
        exp = sc.get("expected") or {}
        comp = components(diag, sg)
        root = diag.get("root_cause") or {}
        got = overall_level(comp, bool(root.get("concept")))
        want = overall_level(exp.get("levels", {}), bool(exp.get("held")))
        held = sorted({h["misconception"] for h in diag.get("held_misconceptions", [])})
        ok = got["overall"] == want["overall"]
        ok_share = got["share_overall"] == want["share_overall"]
        ok_held = set(exp.get("held", [])) <= set(held) and bool(exp.get("held")) == bool(held)
        ok_root = (root.get("concept") or None) == exp.get("root")
        n_overall += ok
        n_share += ok_share
        n_held += ok_held
        n_root += ok_root
        flagged += got["coherent"] is False
        rows.append({
            "scenario": sid, "way tested": exp.get("way", ""),
            "components": ", ".join(f"{c} {lv}" for c, lv in comp.items()) or "none",
            "held": ", ".join(f"{h['misconception']} at {h['concept']}" for h in diag.get("held_misconceptions", [])) or "none",
            "root cause": (root.get("concept") or "none") + (f" / {root['misconception']}" if root.get("misconception") else ""),
            "overall": got["overall"] or "no level", "decided by": got["by"], "shares": shares_text(got),
            "expected overall": want["overall"] or "no level", "match": "yes" if ok else "NO",
            "expected held": ", ".join(exp.get("held", [])) or "none", "held match": "yes" if ok_held else "NO",
            "expected root": exp.get("root") or "none", "root match": "yes" if ok_root else "NO",
            "share rule alone": got["share_overall"] or "no level"})
        print(f"{sid}: {rows[-1]['components']} -> {rows[-1]['overall']} ({got['by']}; {rows[-1]['shares']}) | expected {rows[-1]['expected overall']} "
              f"| {'match' if ok else 'NO MATCH'} | held {'ok' if ok_held else 'X'} | root {'ok' if ok_root else 'X'}")
    cols = ["scenario", "way tested", "components", "held", "root cause", "overall", "decided by", "shares", "expected overall", "match",
            "expected held", "held match", "expected root", "root match", "share rule alone"]
    out = Path(a.out) if a.out else RESULTS_DIR / (f"overall_level_{a.tag}" if a.tag else "overall_level")
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out.with_suffix(".csv"), "w", newline="", encoding="utf-8") as fh:
        wr = csv.DictWriter(fh, fieldnames=cols)
        wr.writeheader()
        wr.writerows(rows)
    n = len(rows)
    tail = [f"Overall level matches the expected one: {n_overall} / {n}",
            f"Held misconceptions match: {n_held} / {n}",
            f"Root cause matches: {n_root} / {n}",
            f"Flagged for LOW coherence: {flagged} / {n}",
            f"For comparison, the share rule alone matches: {n_share} / {n}"]
    md = ["| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)] + ["| " + " | ".join(r[c] for c in cols) + " |" for r in rows] + [""] + [t + "  " for t in tail]
    out.with_suffix(".md").write_text(NL.join(md) + NL, encoding="utf-8")
    print(NL.join(tail))


if __name__ == "__main__":
    main()
