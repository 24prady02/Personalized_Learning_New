"""Operator tool — mint a signed login URL for a student.

Usage:
    python scripts/issue_token.py alice student CSCI1301
    python scripts/issue_token.py prof_smith teacher CSCI1301 --ttl-days 30

Outputs a URL the operator can paste into email / LMS. Without the
signed token, anyone visiting the public URL is anonymous.

See src/persistence/auth.py for the scope caveats — this is NOT
real OAuth.

Added 2026-05-21.
"""
from __future__ import annotations
import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def main() -> int:
    p = argparse.ArgumentParser(description="Mint a CPAL login token.")
    p.add_argument("student_id")
    p.add_argument("role", choices=["student", "teacher", "admin"],
                   default="student", nargs="?")
    p.add_argument("course", default="default", nargs="?")
    p.add_argument("--ttl-days", type=int, default=7)
    p.add_argument("--base-url", default="https://tutor.cpaltutor.com")
    args = p.parse_args()
    from src.persistence.auth import issue_token
    tok = issue_token(args.student_id, args.role, args.course,
                       ttl_seconds=args.ttl_days * 24 * 3600)
    print(f"Login URL (valid {args.ttl_days} days):")
    print(f"  {args.base_url}/?token={tok}")
    print()
    print("Bare token (use this in API headers if you build a REST client):")
    print(f"  {tok}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
