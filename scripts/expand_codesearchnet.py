"""Expand CodeSearchNet-Java sampling to 8000 functions and rebuild metadata.csv."""
import re
import sys
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
CODENET_DIR = ROOT / "data" / "codenet"
CORRECT_DIR = CODENET_DIR / "java" / "correct"
BUGGY_DIR = CODENET_DIR / "java" / "buggy"
PARQUET = ROOT / "data" / "codesearchnet_java_shard0.parquet"

_CLASS_RE = re.compile(r"\bclass\s+([A-Za-z_][A-Za-z0-9_]*)")


def _safe(s: str, n: int = 60) -> str:
    s = re.sub(r"[^A-Za-z0-9._-]", "_", s)
    return s[:n] or "x"


def _wrap(code: str, sid: str) -> str:
    if _CLASS_RE.search(code):
        return code
    cls = "Sample_" + _safe(sid, 40)
    return f"public class {cls} {{\n    {code.strip()}\n}}\n"


def main() -> int:
    if not PARQUET.exists():
        print(f"[fail] {PARQUET.name} missing")
        return 1

    df = pd.read_parquet(PARQUET, columns=["code"])
    df = df.sample(8000, random_state=42)
    print(f"Sampled {len(df)} rows")

    written = 0
    for i, row in df.iterrows():
        code = str(row["code"])
        if len(code) < 30:
            continue
        p = CORRECT_DIR / f"csn_{i:07d}.java"
        if p.exists():
            continue
        p.write_text(_wrap(code, f"csn_{i}"), encoding="utf-8")
        written += 1
    print(f"Wrote {written} new CodeSearchNet files")

    # Rebuild metadata.csv
    rows = []
    for p in sorted(CORRECT_DIR.glob("*.java")):
        rel = str(p.relative_to(CODENET_DIR)).replace("\\", "/")
        rows.append((p.stem, p.stem, "accepted", "java", rel))
    for p in sorted(BUGGY_DIR.glob("*.java")):
        rel = str(p.relative_to(CODENET_DIR)).replace("\\", "/")
        rows.append((p.stem, p.stem, "wrong", "java", rel))
    (CODENET_DIR / "metadata.csv").write_text(
        "submission_id,problem_id,status,language,file_path\n"
        + "\n".join(",".join(r) for r in rows),
        encoding="utf-8",
    )
    print(f"metadata.csv -> {len(rows)} entries")
    return 0


if __name__ == "__main__":
    sys.exit(main())
