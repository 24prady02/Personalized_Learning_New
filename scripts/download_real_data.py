"""
Unified Java-focused real-data download + preparation script.

Replaces the scattered / broken download_*.py scripts at the repo root.

Goal: assemble a Java-focused training corpus for "student code comprehension
tied to a Java ontology", using only public, no-registration sources.

What this does:
  1. CodeNet Java accepted submissions
       HF: yangccccc/codenet_after_java (~300 real IBM CodeNet Java)
       -> data/codenet/java/correct/*.java
  2. Defects4J Java bug/fix pairs
       HF: rufimelo/defects4j (1.4 MB, real open-source bugs)
       -> data/codenet/java/buggy/*.java (func_before)  and matching correct
  3. ManySStuBs4J single-statement Java bugs
       HF: zirui3/ManySStuBs4J-instructions-v0 (1 shard, ~200 MB)
       -> mined for (before, after) pairs, sampled into correct/buggy folders
  4. CodeSearchNet Java functions
       HF: Nan-Do/code-search-net-java (1 shard, ~100 MB)
       -> sampled Java functions into correct/
  5. Synthesized ProgSnap2 MainTable.csv (schema-accurate)
       -> data/progsnap2/MainTable.csv (BehavioralRNN training)
  6. Writes data/codenet/metadata.csv so CodeNetProcessor gets the fast path.

Not handled (require registration):
  - PSLCDataShop CodeWorkout (real CS1 Java student traces)
  - BlueJ / Blackbox (real novice Java sessions)
  - Full IBM CodeNet (100 GB)
  - Full MOOCCubeX
See REGISTRATION_REQUIRED.md for how to acquire them.
"""

from __future__ import annotations

import json
import random
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import pandas as pd
import requests
from tqdm import tqdm

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
CODENET_DIR = DATA / "codenet"
JAVA_DIR = CODENET_DIR / "java"
CORRECT_DIR = JAVA_DIR / "correct"
BUGGY_DIR = JAVA_DIR / "buggy"
PROGSNAP_DIR = DATA / "progsnap2"

HF_CODENET_JAVA_URL = (
    "https://huggingface.co/datasets/yangccccc/codenet_after_java/"
    "resolve/main/after_codenet_java.json"
)
HF_DEFECTS4J_URL = (
    "https://huggingface.co/datasets/rufimelo/defects4j/resolve/main/train.csv"
)
HF_MANYSSTUBS_URL = (
    "https://huggingface.co/datasets/zirui3/ManySStuBs4J-instructions-v0/"
    "resolve/main/data/train-00000-of-00004-205b9db0d7bde2c9.parquet"
)
HF_CODESEARCHNET_URL = (
    "https://huggingface.co/datasets/Nan-Do/code-search-net-java/"
    "resolve/main/data/train-00000-of-00004-63114f67d19982c3.parquet"
)

CODESEARCHNET_SAMPLE_N = 8000  # sampled from ~124K real Java functions in shard 0


# ── download helper ──────────────────────────────────────────────────────────

def _download(url: str, dest: Path, desc: str, min_bytes: int = 1024) -> bool:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists() and dest.stat().st_size >= min_bytes:
        print(f"  [skip] {dest.relative_to(ROOT)} "
              f"({dest.stat().st_size / 1024 / 1024:.1f} MB already present)")
        return True

    try:
        r = requests.get(url, stream=True, timeout=120, allow_redirects=True)
        r.raise_for_status()
    except Exception as e:
        print(f"  [fail] {url}: {e}")
        return False

    total = int(r.headers.get("content-length", 0))
    with open(dest, "wb") as f, tqdm(
        total=total, unit="B", unit_scale=True, unit_divisor=1024, desc=desc
    ) as bar:
        for chunk in r.iter_content(chunk_size=256 * 1024):
            if chunk:
                f.write(chunk)
                bar.update(len(chunk))

    if dest.stat().st_size < min_bytes:
        print(f"  [fail] {dest.name} too small — removing")
        dest.unlink(missing_ok=True)
        return False

    print(f"  [ok] {dest.relative_to(ROOT)} "
          f"({dest.stat().st_size / 1024 / 1024:.1f} MB)")
    return True


# ── helpers for writing java samples ─────────────────────────────────────────

_CLASS_RE = re.compile(r"\bclass\s+([A-Za-z_][A-Za-z0-9_]*)")


def _sanitize_filename(s: str, max_len: int = 60) -> str:
    s = re.sub(r"[^A-Za-z0-9._-]", "_", s)
    return s[:max_len] or "sample"


def _wrap_as_java(code: str, sid: str) -> str:
    """
    If `code` is a method/snippet (not a top-level class), wrap it in a
    minimal class so the file is parseable Java (CodeNetProcessor only reads
    up to max_code_len characters, so this never blows up).
    """
    if _CLASS_RE.search(code):
        return code
    cls = f"Sample_{_sanitize_filename(sid)}"
    return (
        f"public class {cls} {{\n"
        f"    // auto-wrapped snippet\n"
        f"    {code.strip()}\n"
        f"}}\n"
    )


def _write_java(target_dir: Path, stem: str, code: str) -> bool:
    if not code or len(code) < 30:
        return False
    target_dir.mkdir(parents=True, exist_ok=True)
    path = target_dir / f"{_sanitize_filename(stem)}.java"
    if path.exists():
        return False
    try:
        path.write_text(code, encoding="utf-8")
        return True
    except Exception:
        return False


# ── (1) CodeNet Java accepted submissions ───────────────────────────────────

def fetch_codenet_java() -> int:
    print("\n[1] CodeNet Java (IBM Project CodeNet mirror)")
    raw = CODENET_DIR / "after_codenet_java.json"
    if not _download(HF_CODENET_JAVA_URL, raw, "codenet", 100_000):
        return 0

    with open(raw, "r", encoding="utf-8") as f:
        samples = json.load(f)

    written = 0
    for s in samples:
        code = s.get("code", "")
        sid = s.get("id", f"cn_{written:06d}")
        if _write_java(CORRECT_DIR, f"cn_{sid}", code):
            written += 1
    print(f"  -> wrote {written} CodeNet accepted Java files to {CORRECT_DIR.name}/")
    return written


# ── (2) Defects4J bug/fix pairs ──────────────────────────────────────────────

def fetch_defects4j() -> Tuple[int, int]:
    print("\n[2] Defects4J Java bug/fix pairs")
    raw = DATA / "defects4j_train.csv"
    if not _download(HF_DEFECTS4J_URL, raw, "defects4j", 500_000):
        return 0, 0

    df = pd.read_csv(raw)
    print(f"  parsed {len(df)} bug/fix rows; columns: {list(df.columns)}")

    cols = {c.lower(): c for c in df.columns}
    id_col = cols.get("bug_id") or cols.get("id")
    before_col = cols.get("func_before") or cols.get("before") or cols.get("buggy")
    after_col = cols.get("func_after") or cols.get("after") or cols.get("fixed")
    if not before_col or not after_col:
        print(f"  [warn] could not identify before/after columns; skipping")
        return 0, 0

    buggy_n = correct_n = 0
    for _, row in df.iterrows():
        bid = str(row[id_col]) if id_col else f"d4j_{buggy_n}"
        b_code = _wrap_as_java(str(row[before_col]), f"d4j_{bid}_bug")
        a_code = _wrap_as_java(str(row[after_col]), f"d4j_{bid}_fix")
        if _write_java(BUGGY_DIR, f"d4j_{bid}_bug", b_code):
            buggy_n += 1
        if _write_java(CORRECT_DIR, f"d4j_{bid}_fix", a_code):
            correct_n += 1
    print(f"  -> wrote {buggy_n} buggy + {correct_n} fixed Java files")
    return correct_n, buggy_n


# ── (3) ManySStuBs4J ─────────────────────────────────────────────────────────

def _detect_cols(df: pd.DataFrame, *candidates: str) -> Optional[str]:
    for c in candidates:
        for col in df.columns:
            if c.lower() == col.lower():
                return col
    for c in candidates:
        for col in df.columns:
            if c.lower() in col.lower():
                return col
    return None


def fetch_manysstubs() -> Tuple[int, int]:
    print("\n[3] ManySStuBs4J (real GitHub Java single-statement bugs)")
    raw = DATA / "manysstubs_train_shard0.parquet"
    if not _download(HF_MANYSSTUBS_URL, raw, "manysstubs", 50_000_000):
        return 0, 0

    try:
        df = pd.read_parquet(raw, columns=None)
    except Exception as e:
        print(f"  [fail] read_parquet: {e}")
        return 0, 0
    print(f"  parsed {len(df)} rows; columns: {list(df.columns)[:12]}")

    before_col = _detect_cols(df, "bugSource", "sourceBeforeFix", "before_code", "buggy", "input")
    after_col = _detect_cols(df, "fixSource", "sourceAfterFix", "after_code", "fixed", "output")
    type_col = _detect_cols(df, "bugType", "bug_type", "type", "category", "label")

    if before_col is None or after_col is None:
        print(f"  [warn] could not find before/after columns — trying 'instruction'/'output'")
        before_col = _detect_cols(df, "instruction", "prompt")
        after_col = _detect_cols(df, "output", "response", "completion")

    if before_col is None or after_col is None:
        print("  [skip] ManySStuBs4J schema not recognized")
        return 0, 0

    df = df.sample(min(MANYSSTUBS_SAMPLE_N, len(df)), random_state=42)
    print(f"  sampling {len(df)} rows; before='{before_col}', after='{after_col}', type='{type_col}'")

    buggy_n = correct_n = 0
    bug_types: Dict[str, int] = {}
    for i, row in df.iterrows():
        bt = str(row[type_col]) if type_col else "unknown"
        bug_types[bt] = bug_types.get(bt, 0) + 1
        b_raw = str(row[before_col])
        a_raw = str(row[after_col])
        sid = f"mss_{i:07d}_{_sanitize_filename(bt, 20)}"
        if _write_java(BUGGY_DIR, f"{sid}_bug", _wrap_as_java(b_raw, sid)):
            buggy_n += 1
        if _write_java(CORRECT_DIR, f"{sid}_fix", _wrap_as_java(a_raw, sid)):
            correct_n += 1

    # Save bug category distribution for later mapping to misconceptions
    out = DATA / "manysstubs_bug_category_distribution.json"
    out.write_text(json.dumps(bug_types, indent=2, sort_keys=True), encoding="utf-8")
    print(f"  -> wrote {buggy_n} buggy + {correct_n} fixed Java files")
    print(f"  -> saved bug category histogram to {out.relative_to(ROOT)}")
    return correct_n, buggy_n


# ── (4) CodeSearchNet Java ───────────────────────────────────────────────────

def fetch_codesearchnet() -> int:
    print("\n[4] CodeSearchNet-Java (real GitHub Java functions)")
    raw = DATA / "codesearchnet_java_shard0.parquet"
    if not _download(HF_CODESEARCHNET_URL, raw, "codesearchnet", 50_000_000):
        return 0

    try:
        df = pd.read_parquet(raw, columns=None)
    except Exception as e:
        print(f"  [fail] read_parquet: {e}")
        return 0
    print(f"  parsed {len(df)} rows; columns: {list(df.columns)[:12]}")

    code_col = _detect_cols(df, "func_code_string", "code", "whole_func_string", "function")
    if code_col is None:
        print("  [skip] couldn't find a code column")
        return 0

    df = df.sample(min(CODESEARCHNET_SAMPLE_N, len(df)), random_state=42)
    print(f"  sampling {len(df)} rows from '{code_col}'")

    written = 0
    for i, row in df.iterrows():
        code = str(row[code_col])
        if _write_java(CORRECT_DIR, f"csn_{i:07d}", _wrap_as_java(code, f"csn_{i}")):
            written += 1
    print(f"  -> wrote {written} CodeSearchNet Java functions to {CORRECT_DIR.name}/")
    return written


# ── (5) Synthesized ProgSnap2 ────────────────────────────────────────────────

EVENT_TYPES = [
    ("File.Edit", 0.40), ("Run.Program", 0.20), ("Compile.Error", 0.12),
    ("Run.Error", 0.08), ("File.Open", 0.06), ("Submit", 0.05),
    ("HelpRequest", 0.04), ("Resource.View", 0.03), ("Webpage.Open", 0.02),
]
CS1_PROBLEMS = [
    ("P01_HelloWorld", "print_statement"), ("P02_Variables", "variables"),
    ("P03_Addition", "arithmetic"), ("P04_IfElse", "conditionals"),
    ("P05_ForLoop", "loops"), ("P06_WhileLoop", "loops"),
    ("P07_Methods", "methods"), ("P08_Array", "arrays"),
    ("P09_StringOps", "strings"), ("P10_Recursion", "recursion"),
    ("P11_SortArray", "sorting"), ("P12_FileIO", "io"),
    ("P13_Classes", "oop"), ("P14_Inheritance", "oop"),
    ("P15_Exceptions", "exceptions"),
]


def _sample_event(rng: random.Random) -> str:
    r = rng.random()
    c = 0.0
    for name, p in EVENT_TYPES:
        c += p
        if r <= c:
            return name
    return "File.Edit"


def synth_progsnap2(n_subjects: int = 400) -> bool:
    print(f"\n[5] Synthesized ProgSnap2 (real not publicly available)")
    PROGSNAP_DIR.mkdir(parents=True, exist_ok=True)
    dest = PROGSNAP_DIR / "MainTable.csv"
    if dest.exists() and dest.stat().st_size > 500_000:
        print(f"  [skip] {dest.relative_to(ROOT)} already exists "
              f"({dest.stat().st_size / 1024 / 1024:.1f} MB)")
        return True

    rng = random.Random(2024)
    rows: List[Dict[str, Any]] = []
    base_ts = datetime(2024, 1, 15, 9, 0, 0).timestamp()

    for s in tqdm(range(n_subjects), desc="subjects"):
        subj = f"S{s:04d}"
        problems = rng.sample(CS1_PROBLEMS, k=rng.randint(3, 8))
        for pid, concept in problems:
            t = base_ts + s * 3600 + rng.randint(0, 86400 * 7)
            n_events = rng.randint(10, 40)
            for _ in range(n_events):
                t += max(1.0, rng.expovariate(1 / 25.0))
                ev = _sample_event(rng)
                code_state = (
                    f"public class P {{ /* {concept} */ "
                    f"public static void main(String[] a) {{}} }}"
                )
                rows.append({
                    "SubjectID": subj,
                    "ProblemID": pid,
                    "EventType": ev,
                    "ServerTimestamp": round(t, 3),
                    "CodeStateSection": code_state,
                    "Score": 1 if ev == "Submit" and rng.random() < 0.7 else 0,
                })

    df = pd.DataFrame(rows)
    df.to_csv(dest, index=False)
    (PROGSNAP_DIR / "DatasetMetadata.json").write_text(json.dumps({
        "ProgSnap2 Version": "6",
        "IsEventOrderingConsistent": True,
        "EventOrderField": "ServerTimestamp",
        "AnalysisFocus": "CS1 Java debugging (synthesized)",
        "SubjectCount": n_subjects,
        "EventCount": len(rows),
    }, indent=2), encoding="utf-8")
    print(f"  -> {dest.relative_to(ROOT)} "
          f"({dest.stat().st_size / 1024 / 1024:.1f} MB, {len(rows)} events)")
    return True


# ── (6) metadata.csv for CodeNetProcessor fast path ──────────────────────────

def write_codenet_metadata() -> int:
    rows = []
    for p in sorted(CORRECT_DIR.glob("*.java")):
        rows.append((p.stem, p.stem, "accepted", "java",
                     str(p.relative_to(CODENET_DIR)).replace("\\", "/")))
    for p in sorted(BUGGY_DIR.glob("*.java")):
        rows.append((p.stem, p.stem, "wrong", "java",
                     str(p.relative_to(CODENET_DIR)).replace("\\", "/")))
    if not rows:
        return 0
    meta = CODENET_DIR / "metadata.csv"
    meta.write_text(
        "submission_id,problem_id,status,language,file_path\n" +
        "\n".join(",".join(r) for r in rows),
        encoding="utf-8",
    )
    print(f"\n[6] metadata.csv -> {len(rows)} entries at {meta.relative_to(ROOT)}")
    return len(rows)


# ── main ─────────────────────────────────────────────────────────────────────

def main() -> int:
    print(f"Repo root: {ROOT}")
    print(f"Data dir:  {DATA}")
    DATA.mkdir(parents=True, exist_ok=True)
    CORRECT_DIR.mkdir(parents=True, exist_ok=True)
    BUGGY_DIR.mkdir(parents=True, exist_ok=True)

    # Remove any stale template-generated files from old download scripts
    removed = 0
    for p in list(CORRECT_DIR.glob("code_*.java")) + list(CORRECT_DIR.glob("code_*.txt")):
        p.unlink(); removed += 1
    for p in list(BUGGY_DIR.glob("code_*.java")) + list(BUGGY_DIR.glob("code_*.txt")):
        p.unlink(); removed += 1
    if removed:
        print(f"(cleared {removed} stale template files)")

    totals = {"correct": 0, "buggy": 0}
    totals["correct"] += fetch_codenet_java()
    c, b = fetch_defects4j(); totals["correct"] += c; totals["buggy"] += b
    c, b = fetch_manysstubs(); totals["correct"] += c; totals["buggy"] += b
    totals["correct"] += fetch_codesearchnet()
    synth_progsnap2()
    meta_rows = write_codenet_metadata()

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"  Java correct files: {totals['correct']}")
    print(f"  Java buggy files:   {totals['buggy']}")
    print(f"  metadata.csv rows:  {meta_rows}")
    print(f"  ProgSnap2 MainTable.csv: {'OK' if (PROGSNAP_DIR / 'MainTable.csv').exists() else 'MISSING'}")

    print("\nNext:")
    print("  python train.py --config config.yaml")

    return 0


if __name__ == "__main__":
    sys.exit(main())
