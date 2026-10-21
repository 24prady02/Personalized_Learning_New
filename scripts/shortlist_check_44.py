"""
shortlist_check_44.py — free check of the "send only the relevant edges" plan.

For each of the 44 labelled answers and each concept the judge graded, the
student's clauses (and the whole answer) are matched by similarity (MiniLM)
against every way of the concept's has_level edges, L0-L4, and the ways are
ranked per level. The shortlist keeps the top K ways per level (L0 always kept).

The check: does the shortlist still contain the way the Opus judge picked when it
saw the full ladder (its choices are saved in scenario_run_v10_all)? If it does,
the judge can be sent only the shortlist without changing its level, so 38/44 holds.
Also reports how much smaller the prompt becomes. No model calls besides MiniLM.

Usage: python scripts/shortlist_check_44.py
"""
from __future__ import annotations

import json
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from fuse_44 import GRAPH_KEY  # noqa: E402
from src.lp_percpt import judge as judgelib  # noqa: E402
from src.lp_percpt import models  # noqa: E402
from src.lp_percpt.identify import split_clauses  # noqa: E402

LEVELS = ("L0", "L1", "L2", "L3", "L4")


def entries(cid):
    """(level, way name, rule text) for every way of the concept's has_level edges."""
    out = []
    for lv in LEVELS:
        e = judgelib._edges().get((cid, lv))
        for w in (e or {}).get("ways", []):
            if w["way"] == "inconsistent_trace":
                continue
            rule = re.sub(r"\s+", " ", w.get("exact_rule", ""))
            if lv == "L0":
                rule = rule.split("Right rule:")[0].split("Java rule:")[0].split("In Java,")[0]
            out.append((lv, w["way"], rule[:230]))
    return out


def shortlist(text, cid, k):
    ents = entries(cid)
    if not ents:
        return [], ents
    units = split_clauses(text) + [text]
    sim = models.similarity(units, [r for _, _, r in ents]).max(axis=0)
    by_level = defaultdict(list)
    for (lv, w, r), s in zip(ents, sim):
        by_level[lv].append((float(s), lv, w, r))
    keep = []
    for lv in LEVELS:
        keep += sorted(by_level[lv], reverse=True)[:k]
    return keep, ents


def main() -> None:
    rows = [s for s in json.loads((ROOT / "output" / "scenario_run_v10_all" / "results.json").read_text(encoding="utf-8"))["scenarios"]
            if s.get("expected_level")]
    for k in (1, 2, 3):
        hit = tot = hit_set = tot_set = 0
        full_chars = short_chars = 0
        misses = []
        for s in rows:
            target = GRAPH_KEY.get(s["id"], (s["expected_level"],))[0]
            for c in s["concepts"]:
                item = c.get("judge") or {}
                lv, way = item.get("level"), (item.get("way") or "").strip()
                keep, ents = shortlist(s["text"], c["concept"], k)
                full_chars += sum(len(r) for _, _, r in ents)
                short_chars += sum(len(r) for _, _, _, r in keep)
                if lv not in LEVELS or not way:
                    continue
                inside = any(l == lv and w == way for _, l, w, _ in keep)
                tot += 1
                hit += inside
                # the judge item that set the answer's level
                if c.get("level_source") == "judge" and c["prompt_level"] == s["max_level"]:
                    tot_set += 1
                    hit_set += inside
                    if not inside:
                        misses.append(f"{s['id']} {c['concept']} {lv} {way} (answer {s['max_level']}, needed {target})")
        print(f"top {k} way(s) per level: judge's chosen way kept in {hit}/{tot} concept judgements; "
              f"in {hit_set}/{tot_set} that set the answer's level; prompt edge text {short_chars / max(1, full_chars):.0%} of the full ladder")
        for m in misses:
            print("    lost:", m)


if __name__ == "__main__":
    main()
