"""Build and check the pattern bank: the "training" step of a model without learned parameters.

Stage 1 is rule based. Its parameters are the regular expressions stored on the 173 concept nodes of the
knowledge graph, written by hand and corrected in the KG itself (``kg["reader"]["pattern_fixes_reader4"]``).
This script does what a training script does for such a model:

1. compiles every pattern of every channel (code_patterns, signals, operator_symbols, java_types, command_patterns)
   and fails loudly on an invalid regex;
2. checks the pattern bank against the labelled snippets in tests/data/concept_pattern_tests.json
   (must_tag / must_not_tag for every code-visible concept);
3. saves the bank as experiments/pattern_bank.json (the model "checkpoint": one entry per concept with its
   channel counts, generic flag and visibility) and a log in experiments/logs/train_log.txt.

    python src/train.py [--kg data/raw/chapter1_kg_new.json] [--tests tests/data/concept_pattern_tests.json]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from model import tag_code
from utils import KG_PATH, LOGS_DIR, ROOT, load_kg, reader_blocks

CHANNELS = ("code_patterns", "signals", "operator_symbols", "java_types", "command_patterns")


def compile_bank(reader: dict[str, dict]) -> tuple[dict[str, dict], list[str]]:
    """Compile every regex; return the bank summary and a list of compile errors."""
    bank: dict[str, dict] = {}
    errors: list[str] = []
    for cid, rd in sorted(reader.items()):
        entry = {"code_visible": rd.get("code_visible") is not False, "generic": bool(rd.get("generic")),
                 "code_text": rd.get("code_text", "masked"), "channels": {}}
        for ch in CHANNELS:
            items = rd.get(ch) or []
            entry["channels"][ch] = len(items)
            regexes = [s["regex"] for s in items if isinstance(s, dict) and "regex" in s] if ch == "signals" else (
                items if ch in ("code_patterns", "command_patterns") else [])
            for p in regexes:
                try:
                    re.compile(p, re.M | re.S)
                except re.error as exc:
                    errors.append(f"{cid}.{ch}: {p!r}: {exc}")
        entry["skipped_signals"] = [s.get("name", "?") for s in rd.get("signals") or [] if "regex" not in s]
        bank[cid] = entry
    return bank, errors


def check_bank(reader: dict[str, dict], tests: dict[str, dict]) -> list[str]:
    """Run the must_tag / must_not_tag snippets; return the failures."""
    fails: list[str] = []
    for cid, spec in sorted(tests.items()):
        for snippet in spec.get("must_tag", []):
            if cid not in tag_code(snippet, reader):
                fails.append(f"{cid} should tag: {snippet!r}")
        for snippet in spec.get("must_not_tag", []):
            if cid in tag_code(snippet, reader):
                fails.append(f"{cid} should NOT tag: {snippet!r}")
    return fails


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--kg", default=str(KG_PATH))
    ap.add_argument("--tests", default=str(ROOT / "tests/data/concept_pattern_tests.json"))
    ap.add_argument("--out", default=str(ROOT / "experiments/pattern_bank.json"))
    a = ap.parse_args(argv)

    kg = load_kg(a.kg)
    reader = reader_blocks(kg)
    bank, errors = compile_bank(reader)
    tests = json.loads(Path(a.tests).read_text(encoding="utf-8"))
    fails = check_bank(reader, tests)

    visible = [c for c, e in bank.items() if e["code_visible"]]
    n_regex = sum(e["channels"]["code_patterns"] + e["channels"]["command_patterns"] for e in bank.values())
    n_sig = sum(e["channels"]["signals"] - len(e["skipped_signals"]) for e in bank.values())
    lines = [
        f"knowledge graph {kg.get('version')}",
        f"concepts {len(bank)}  code-visible {len(visible)}  generic {sum(e['generic'] for e in bank.values())}",
        f"regex patterns {n_regex}  regex signals {n_sig}  operator symbols {sum(e['channels']['operator_symbols'] for e in bank.values())}  "
        f"java types {sum(e['channels']['java_types'] for e in bank.values())}",
        f"compile errors {len(errors)}", *[f"  {e}" for e in errors],
        f"pattern tests: {sum(len(s.get('must_tag', [])) + len(s.get('must_not_tag', [])) for s in tests.values())} snippets over {len(tests)} concepts, "
        f"failures {len(fails)}", *[f"  {f}" for f in fails],
        f"missing tests for code-visible concepts: {sorted(set(visible) - set(tests)) or 'none'}",
    ]
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"kg_version": kg.get("version"), "concepts": bank}, indent=1), encoding="utf-8")
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    (LOGS_DIR / "train_log.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    print(f"wrote {out} and {LOGS_DIR / 'train_log.txt'}")
    return 1 if errors or fails else 0


if __name__ == "__main__":
    sys.exit(main())
