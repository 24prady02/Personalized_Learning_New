"""
Extract Java-only buggy/fixed pairs from the already-downloaded
ManySStuBs4J instruction parquet.

The HF mirror zirui3/ManySStuBs4J-instructions-v0 stores rows as:
  instruction = "Find the bug in the following code:\n <buggy code>"
  answer      = "The fixed code is:\n``` <fixed code>```"
and mixes Python and Java. This script filters to Java, extracts the
code blocks, and writes .java files into
  data/codenet/java/{correct,buggy}/
then updates data/codenet/metadata.csv.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Optional, Tuple

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
CODENET_DIR = DATA / "codenet"
CORRECT_DIR = CODENET_DIR / "java" / "correct"
BUGGY_DIR = CODENET_DIR / "java" / "buggy"
PARQUET = DATA / "manysstubs_train_shard0.parquet"

MAX_JAVA_ROWS = 5000  # cap — more than this bloats the training set unnecessarily

JAVA_PATTERNS = [
    re.compile(r"\bpublic\s+(class|static)\b"),
    re.compile(r"\bprivate\s+(static|final|int|String|void)\b"),
    re.compile(r"\bimport\s+java\."),
    re.compile(r"\bSystem\.out\.print"),
    re.compile(r"\bimplements\s+\w+\s*\{"),
    re.compile(r"\bextends\s+\w+\s*\{"),
    re.compile(r"@Override\b"),
    re.compile(r"\bnew\s+\w+\s*\("),
]

PYTHON_HINTS = re.compile(r"^\s*(def |import |from |print\(|class .+:)", re.MULTILINE)


def _looks_like_java(code: str) -> bool:
    if not code or len(code) < 30:
        return False
    if PYTHON_HINTS.search(code):
        return False
    hits = sum(1 for p in JAVA_PATTERNS if p.search(code))
    return hits >= 2


_FENCE_RE = re.compile(r"```(?:java)?\s*(.*?)\s*```", re.DOTALL | re.IGNORECASE)
_INSTR_PREFIX = re.compile(
    r"^\s*Find the bug in the following code\s*:?\s*",
    re.IGNORECASE,
)
_ANSWER_PREFIX = re.compile(
    r"^\s*The fixed code is\s*:?\s*",
    re.IGNORECASE,
)


def _strip_instruction(text: str) -> str:
    text = _INSTR_PREFIX.sub("", text)
    m = _FENCE_RE.search(text)
    return (m.group(1) if m else text).strip()


def _strip_answer(text: str) -> str:
    text = _ANSWER_PREFIX.sub("", text)
    m = _FENCE_RE.search(text)
    return (m.group(1) if m else text).strip()


_CLASS_RE = re.compile(r"\bclass\s+([A-Za-z_][A-Za-z0-9_]*)")


def _wrap_as_java(code: str, sid: str) -> str:
    if _CLASS_RE.search(code):
        return code
    cls = f"MSS_{re.sub(r'[^A-Za-z0-9_]', '_', sid)[:40]}"
    return f"public class {cls} {{\n    {code.strip()}\n}}\n"


def _safe_name(s: str, n: int = 60) -> str:
    s = re.sub(r"[^A-Za-z0-9._-]", "_", s)
    return s[:n] or "m"


def main() -> int:
    if not PARQUET.exists():
        print(f"[fail] {PARQUET} missing — run download_real_data.py first")
        return 1

    CORRECT_DIR.mkdir(parents=True, exist_ok=True)
    BUGGY_DIR.mkdir(parents=True, exist_ok=True)

    print(f"Reading {PARQUET.name} ...")
    df = pd.read_parquet(PARQUET)
    print(f"  {len(df)} rows, columns: {list(df.columns)}")

    written_correct = written_buggy = 0
    scanned = 0
    stop_at = MAX_JAVA_ROWS

    for i, row in df.iterrows():
        if written_buggy >= stop_at:
            break
        scanned += 1
        if scanned % 50000 == 0:
            print(f"  scanned {scanned}, kept {written_buggy} buggy / {written_correct} correct")
        instr = str(row.get("instruction", ""))
        ans = str(row.get("answer", ""))
        bug = _strip_instruction(instr)
        fix = _strip_answer(ans)
        if not _looks_like_java(bug) or not _looks_like_java(fix):
            continue

        sid = f"mss_{i:07d}"
        bug_code = _wrap_as_java(bug, f"{sid}_bug")
        fix_code = _wrap_as_java(fix, f"{sid}_fix")

        bp = BUGGY_DIR / f"{_safe_name(sid)}_bug.java"
        fp = CORRECT_DIR / f"{_safe_name(sid)}_fix.java"

        if not bp.exists():
            bp.write_text(bug_code, encoding="utf-8")
            written_buggy += 1
        if not fp.exists():
            fp.write_text(fix_code, encoding="utf-8")
            written_correct += 1

    print(f"Scanned {scanned} rows; wrote {written_buggy} buggy + {written_correct} fixed.")

    # rebuild metadata.csv
    rows = []
    for p in sorted(CORRECT_DIR.glob("*.java")):
        rows.append((p.stem, p.stem, "accepted", "java",
                     str(p.relative_to(CODENET_DIR)).replace("\\", "/")))
    for p in sorted(BUGGY_DIR.glob("*.java")):
        rows.append((p.stem, p.stem, "wrong", "java",
                     str(p.relative_to(CODENET_DIR)).replace("\\", "/")))
    (CODENET_DIR / "metadata.csv").write_text(
        "submission_id,problem_id,status,language,file_path\n"
        + "\n".join(",".join(r) for r in rows),
        encoding="utf-8",
    )
    print(f"metadata.csv rewritten with {len(rows)} entries")
    return 0


if __name__ == "__main__":
    sys.exit(main())
