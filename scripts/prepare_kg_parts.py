"""Generate ``data/kg_parts.json`` from ``data/chapter1_kg.json`` (offline).

Derived data the reader needs (edge-logic parts with slots, way slots,
misconception slots, aliases). ``chapter1_kg.json`` is never edited.
Deterministic: running it twice gives a byte-identical file.

    python scripts/prepare_kg_parts.py [--kg data/chapter1_kg.json] [--out data/kg_parts.json]
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from lp_graph.graph import DEFAULT_PARTS_PATH, KG  # noqa: E402
from lp_graph.knowledge import DEFAULT_KG_PATH  # noqa: E402
from lp_graph.parts import build_parts  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--kg", default=str(DEFAULT_KG_PATH))
    ap.add_argument("--out", default=str(DEFAULT_PARTS_PATH))
    args = ap.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")

    kg = KG(args.kg, parts_path=None)
    data = build_parts(kg)
    text = json.dumps(data, indent=1, sort_keys=True, ensure_ascii=False) + "\n"
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding="utf-8", newline="\n")

    cov = data["coverage"]
    print(f"graph {kg.path.name} version {kg.version}")
    print(f"wrote {out} ({len(text) // 1024} KiB)")
    print(f"relation edges with >=1 tagged part : {cov['edges_with_tagged_part']}/{cov['relation_edges']}")
    print(f"relation edges with >=1 slot        : {cov['edges_with_slot']}/{cov['relation_edges']}")
    print(f"relation edges tagged and slotted   : {cov['edges_tagged_and_slotted']}/{cov['relation_edges']}")
    print(f"parts tagged                        : {cov['parts_tagged']}/{cov['parts']}")
    print(f"misconception pairs with a slot     : {cov['misconceptions_with_slot']}/{cov['misconception_edges']}")
    print(f"way rules with >=1 slot             : {cov['ways_with_slot']}/{cov['ways']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
