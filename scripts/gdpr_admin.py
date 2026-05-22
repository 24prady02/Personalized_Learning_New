"""GDPR admin tool — export / delete a student's data.

Usage:
    python scripts/gdpr_admin.py export <student_id> [--out file.json]
    python scripts/gdpr_admin.py delete <student_id> [--yes]

What gets purged on `delete`:
  * Every SQLite row keyed on student_id (mastery, student_state,
    variant_assignment, consent, audit_log) — see DBStore.delete_student.
  * Per-student entries in data/dina/student_mastery.json
    (the legacy JSON cache still loaded at startup).
  * Per-student entries in data/student_states.json.
  * Log lines in cpal_chat_app.log* containing the student_id (best-
    effort grep + rewrite).

What's preserved:
  * A tombstone audit_log row recording the deletion time + a hash
    of the deleted id, so we have proof a deletion happened without
    keeping the PII.

This is meant to be run by an operator (you), NOT exposed on the
public Gradio interface. Future work: surface a "delete my data"
button to authenticated students.

Added 2026-05-21 as part of the production-hardening pass.
"""
from __future__ import annotations
import argparse
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def _scrub_json_file(path: Path, student_id: str) -> int:
    """Remove any top-level dict entry keyed on student_id from a JSON
    file. Returns number of entries removed (0 if file missing / wrong
    shape / nothing to remove)."""
    if not path.exists():
        return 0
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        return 0
    if not isinstance(data, dict) or student_id not in data:
        return 0
    data.pop(student_id, None)
    # Atomic rewrite
    import tempfile
    with tempfile.NamedTemporaryFile(
        "w", encoding="utf-8", delete=False,
        dir=str(path.parent), prefix=path.name + ".", suffix=".tmp",
    ) as tf:
        json.dump(data, tf, indent=2)
        tf.flush()
        os.fsync(tf.fileno())
        tmp = tf.name
    os.replace(tmp, str(path))
    return 1


def _scrub_log_file(path: Path, student_id: str) -> int:
    """Drop any line in `path` containing student_id (case-sensitive).
    Returns line count dropped. Best-effort — log lines can split a
    student_id across two writes; we'd need a proper logging library
    for stronger guarantees."""
    if not path.exists():
        return 0
    try:
        kept = []
        dropped = 0
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            for line in f:
                if student_id in line:
                    dropped += 1
                else:
                    kept.append(line)
        if dropped == 0:
            return 0
        import tempfile
        with tempfile.NamedTemporaryFile(
            "w", encoding="utf-8", delete=False,
            dir=str(path.parent), prefix=path.name + ".", suffix=".tmp",
        ) as tf:
            tf.writelines(kept)
            tf.flush()
            os.fsync(tf.fileno())
            tmp = tf.name
        os.replace(tmp, str(path))
        return dropped
    except Exception as e:
        print(f"[gdpr_admin] log scrub failed for {path}: {e}")
        return 0


def cmd_export(student_id: str, out_path: str = None) -> None:
    from src.persistence.db_store import get_db
    payload = get_db().export_student(student_id)
    txt = json.dumps(payload, indent=2, default=str)
    if out_path:
        Path(out_path).write_text(txt, encoding="utf-8")
        print(f"Wrote {len(txt):,} bytes to {out_path}")
    else:
        print(txt)


def cmd_delete(student_id: str, yes: bool = False) -> None:
    if not yes:
        ans = input(
            f"You are about to permanently delete every trace of "
            f"student '{student_id}'. Type the student_id again to "
            f"confirm: ").strip()
        if ans != student_id:
            print("Aborted (confirmation did not match).")
            return
    from src.persistence.db_store import get_db
    db_counts = get_db().delete_student(student_id)
    print(f"SQLite rows deleted: {db_counts}")

    # JSON file purge
    json_counts = {}
    for p in [
        ROOT / "data" / "dina" / "student_mastery.json",
        ROOT / "data" / "student_states.json",
    ]:
        json_counts[str(p.relative_to(ROOT))] = _scrub_json_file(p, student_id)
    print(f"JSON file entries removed: {json_counts}")

    # Log scrub (best-effort)
    log_counts = {}
    for p in [
        ROOT / "cpal_chat_app.log",
        ROOT / "cpal_chat_app.log.err",
    ]:
        log_counts[str(p.relative_to(ROOT))] = _scrub_log_file(p, student_id)
    print(f"Log lines dropped: {log_counts}")
    print(f"\nTombstone audit row written. Deletion complete.")


def main() -> int:
    p = argparse.ArgumentParser(
        description="GDPR /export and /delete for CPAL student data.")
    sub = p.add_subparsers(dest="cmd", required=True)
    pe = sub.add_parser("export")
    pe.add_argument("student_id")
    pe.add_argument("--out", help="write to file instead of stdout")
    pd = sub.add_parser("delete")
    pd.add_argument("student_id")
    pd.add_argument("--yes", action="store_true",
                    help="skip the typed confirmation")
    args = p.parse_args()
    if args.cmd == "export":
        cmd_export(args.student_id, args.out)
    else:
        cmd_delete(args.student_id, args.yes)
    return 0


if __name__ == "__main__":
    sys.exit(main())
