"""
lp_concept_map.py — LP-level classification + student concept map, from the command line.

Runs the complete algorithm in src/lp_percpt (docs/CPAL_LP_Classification_Algorithm.xlsx)
on one or more student prompts and redraws the student's concept map.

Usage:
    python scripts/lp_concept_map.py --student maya --text "the loop never ends because i is never incremented"
    python scripts/lp_concept_map.py --student maya --turns turns.json
        # turns.json: ["msg", ...] or [{"text": "...", "shown": "...", "session": "..."}, ...]
    python scripts/lp_concept_map.py --student maya          # redraw the map only
    python scripts/lp_concept_map.py --student maya --override while_loop=L3

The student graph is kept in data/lp_percpt_students/<student>.json and the
map is written to output/concept_maps/<student>.html.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from src.lp_percpt.engine import get_engine  # noqa: E402


def _turns(args):
    out = []
    if args.turns:
        for t in json.loads(Path(args.turns).read_text(encoding="utf-8")):
            out.append(t if isinstance(t, dict) else {"text": str(t)})
    if args.text:
        out.append({"text": args.text, "shown": args.shown or "", "session": args.session})
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--student", required=True)
    ap.add_argument("--text", help="one student prompt")
    ap.add_argument("--shown", help="text the student was shown (for the parroting gate)")
    ap.add_argument("--session", help="session id (for the staleness gate)")
    ap.add_argument("--turns", help="JSON file with a list of prompts")
    ap.add_argument("--override", help="teacher override, e.g. while_loop=L3")
    args = ap.parse_args()

    eng = get_engine()
    if args.override:
        concept, level = args.override.split("=")
        eng.override(args.student, concept, level)
        print(f"pinned {concept} at {level}")
    for t in _turns(args):
        r = eng.process(args.student, t["text"], shown_text=t.get("shown", ""), session_id=t.get("session"))
        print(f"\n> {t['text']}")
        if r["prompt_gates"]:
            print(f"  prompt gates: {', '.join(r['prompt_gates'])}")
        for c in r["concepts"]:
            print(f"  {c['concept']:<38} prompt {c['prompt_level']}  ->  {c['level'] or '-'}"
                  f"{' (provisional)' if c['provisional'] else ''}  confidence {c['confidence']}")
            print(f"      {c['stop_reason']}")
            if c["held"]:
                print(f"      misconception held: {', '.join(c['held'])}")
            if c["gates"]:
                print(f"      gates: {', '.join(c['gates'])}")
    g = eng.graph(args.student)
    eng._save(g)
    print(f"\nconcept map: {eng.map_path(args.student)}")


if __name__ == "__main__":
    main()
