"""Pseudo-SSO via HMAC-signed tokens.

⚠️ Important scope note ⚠️
This is NOT real OAuth/SSO. Real SSO needs an external identity
provider (Google / Microsoft / Okta) and either an OAuth app
registration or SAML config — none of which I can set up from
within the running app. What this gives you:

  * A way to issue a token from an admin script that binds a
    student_id to a course/role.
  * Server-side validation of that token on every request, so a
    student can't just type "?student=alice" to impersonate
    someone else.

When you're ready for real SSO, replace `validate_token` with an
OAuth-callback handler that issues these same tokens after the
IdP says yes.

How it works
------------
A token is `<student_id>.<role>.<course>.<expiry_unix>.<hmac>`
where the hmac is HMAC-SHA256(secret, "<student_id>|<role>|...|<expiry>").

Usage from the chat app
-----------------------
1. Operator runs:
     python scripts/issue_token.py alice student CSCI1301
   → prints a URL like https://tutor.cpaltutor.com/?token=eyJ...
2. Student opens that URL.
3. cpal_chat_app's _resolve_student_id reads ?token=, calls
   validate_token, and uses the embedded student_id.
4. If invalid/expired, the request is treated as anonymous
   (student_id="chat_user").

Configuration
-------------
The secret is read from env var CPAL_AUTH_SECRET. If unset, falls
back to a dev secret stored in `.auth_secret_dev` next to this
module — created on first import. **Rotate the dev secret before
deploying** by setting CPAL_AUTH_SECRET to a real random value.

Added 2026-05-21.
"""
from __future__ import annotations
import base64
import hashlib
import hmac
import os
import secrets
import time
from pathlib import Path
from typing import Optional, Tuple


_DEV_SECRET_PATH = Path(__file__).resolve().parent / ".auth_secret_dev"


def _load_secret() -> bytes:
    env = os.environ.get("CPAL_AUTH_SECRET")
    if env:
        return env.encode("utf-8")
    # Dev fallback — write a random secret on first run so dev sessions
    # are stable. NEVER use this in production: anyone with code-read
    # access can read it.
    if _DEV_SECRET_PATH.exists():
        return _DEV_SECRET_PATH.read_bytes()
    new = secrets.token_bytes(32)
    _DEV_SECRET_PATH.write_bytes(new)
    return new


_SECRET = _load_secret()


def _sign(payload: str) -> str:
    sig = hmac.new(_SECRET, payload.encode("utf-8"), hashlib.sha256).digest()
    return base64.urlsafe_b64encode(sig).decode("ascii").rstrip("=")


def issue_token(student_id: str, role: str = "student",
                course: str = "default",
                ttl_seconds: int = 7 * 24 * 3600) -> str:
    """Mint a signed token for this (student_id, role, course)."""
    expiry = int(time.time()) + int(ttl_seconds)
    payload = f"{student_id}|{role}|{course}|{expiry}"
    sig = _sign(payload)
    return base64.urlsafe_b64encode(
        f"{payload}|{sig}".encode("utf-8")
    ).decode("ascii").rstrip("=")


def validate_token(token: str) -> Optional[Tuple[str, str, str]]:
    """Returns (student_id, role, course) if valid, else None.

    Treats any of these as invalid:
      - malformed encoding
      - HMAC mismatch (tampering)
      - expired
    """
    if not token:
        return None
    try:
        pad = "=" * (-len(token) % 4)
        raw = base64.urlsafe_b64decode(token + pad).decode("utf-8")
        student_id, role, course, expiry, sig = raw.rsplit("|", 4)
    except Exception:
        return None
    payload = f"{student_id}|{role}|{course}|{expiry}"
    expected = _sign(payload)
    # constant-time compare
    if not hmac.compare_digest(sig, expected):
        return None
    try:
        if int(expiry) < int(time.time()):
            return None
    except Exception:
        return None
    return (student_id, role, course)
