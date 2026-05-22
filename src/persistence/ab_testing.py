"""A/B testing framework for CPAL prompt + intervention variants.

Why
---
We want to measure whether prompt phrasing X teaches better than Y,
or whether intervention policy A produces better mastery deltas than
B. Without sticky assignment, the same student bouncing between
variants makes the signal unreadable.

How
---
ASSIGN_EXPERIMENTS describes each live experiment. For a given
(student_id, experiment), assign_variant() returns the variant name —
deterministically per student (hash-based fallback) and sticky
(persisted in the variant_assignment table once assigned).

Then in the chat app, you read the variant via
get_variant(student_id, experiment_name) and branch on it.

Adding a new experiment
-----------------------
1. Add a new entry to ASSIGN_EXPERIMENTS below.
2. In cpal_chat_app.py, somewhere before the LLM call, do:

       variant = get_variant(student_id, "teach_prompt_v2")
       if variant == "verbose":
           prompt = VERBOSE_TEACH_PROMPT
       else:
           prompt = TERSE_TEACH_PROMPT

3. The variant_assignment row + audit_log entry mean you can later
   join mastery deltas to variant to compute lift.

Added 2026-05-21 as part of the production-hardening pass.
"""
from __future__ import annotations
import hashlib
from typing import Dict, List, Optional


# ── Live experiments ──────────────────────────────────────────────────────
# Each entry: experiment_name -> {weight: float per variant}.
# Weights are relative; they don't need to sum to 1.
#
# An empty dict disables the experiment (every student gets None and
# the chat app's "if variant ==" branches fall through to the default).
ASSIGN_EXPERIMENTS: Dict[str, Dict[str, float]] = {
    # Example: 50/50 split on the comprehensive teach prompt's
    # phrasing. "control" = current production prompt. "verbose" =
    # add a "but first restate the question in your own words" line
    # to encourage encoding.
    "teach_prompt_v2": {"control": 0.5, "verbose": 0.5},

    # Example: should the probe ladder show 4 probes max or 6 max
    # before forcing comprehensive synthesis? Control is the current
    # CHAT_MAX_PROBES=8 (treated as 'short' here).
    "probe_cap_v1":    {"short": 0.5, "long": 0.5},
}


def _stable_hash(s: str) -> int:
    """Deterministic per-student hash (sha1, top 64 bits)."""
    return int(hashlib.sha1(s.encode("utf-8")).hexdigest()[:16], 16)


def _bucket(student_id: str, experiment: str, variants: Dict[str, float]
            ) -> str:
    """Hash-based deterministic bucketing — same student gets the same
    variant even if the variant_assignment table is wiped. Lets us
    keep experiments reproducible after a GDPR delete + recreation."""
    if not variants:
        return "control"
    total = sum(variants.values())
    h = _stable_hash(f"{experiment}::{student_id}")
    bucket = (h % 10**6) / 10**6 * total
    cum = 0.0
    for name, w in variants.items():
        cum += w
        if bucket < cum:
            return name
    # numerical safety: fall through to last variant
    return list(variants.keys())[-1]


def assign_variant(student_id: str, experiment: str) -> Optional[str]:
    """Return the sticky variant for this (student, experiment). Looks
    up the DB first; if not assigned, picks via hash bucket and
    persists.

    Soft-fails to None if DB is unreachable (chat app falls through
    to control behavior)."""
    if experiment not in ASSIGN_EXPERIMENTS:
        return None
    try:
        from src.persistence.db_store import get_db
        db = get_db()
        existing = db.get_variant(student_id, experiment)
        if existing:
            return existing
        variant = _bucket(student_id, experiment,
                           ASSIGN_EXPERIMENTS[experiment])
        db.set_variant(student_id, experiment, variant)
        db.audit("ab_assign", student_id=student_id,
                 payload={"experiment": experiment, "variant": variant})
        return variant
    except Exception as e:
        print(f"[AB] assign_variant fell through: {e}")
        return None


def get_variant(student_id: str, experiment: str) -> Optional[str]:
    """Read-only variant lookup. If not assigned yet, returns None
    (caller should use default behavior)."""
    if experiment not in ASSIGN_EXPERIMENTS:
        return None
    try:
        from src.persistence.db_store import get_db
        return get_db().get_variant(student_id, experiment)
    except Exception:
        return None


def list_experiments() -> List[str]:
    return list(ASSIGN_EXPERIMENTS.keys())
