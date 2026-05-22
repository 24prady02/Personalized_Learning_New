"""SQLite persistence for the CPAL chat app.

Why this exists
---------------
The original system stored per-student state in JSON files:
  data/dina/dina_params.json         - the model params (slip/guess/prior)
  data/dina/student_mastery.json     - {student_id: [20 mastery floats]}
  data/student_states.json           - {student_id: {3-graph state ...}}

That worked fine for a single user in dev. In production with multiple
concurrent students, JSON has two killer problems:
  1. Whole-file rewrites: any update rewrites the entire file, so
     concurrent writes corrupt it.
  2. Whole-file reads: every read pulls every student's data into RAM.

This module is a thin, dependency-free SQLite layer that fixes both.
WAL mode for concurrent readers + serialised writers. One DB file
(default data/cpal.db) so backup is one cp.

Backward compatibility
----------------------
The existing JSON files are still loaded at startup if present (so
prior sessions don't lose data). Every write goes to SQLite only.
After one full restart cycle on the new DB, the JSON files can be
deleted.

Tables
------
  mastery (student_id, skill, p_mastered, last_seen_iso)
      PRIMARY KEY (student_id, skill)
      Per-skill mastery probability, with last-seen timestamp so the
      decay rule has something to decay against.

  student_state (student_id, json_payload, updated_iso)
      PRIMARY KEY (student_id)
      The 3-graph state blob (cognitive/progression/psychological)
      stored as JSON for now — the schema is too fluid to normalise.

  variant_assignment (student_id, experiment, variant, assigned_iso)
      PRIMARY KEY (student_id, experiment)
      Sticky A/B variant per (student, experiment).

  audit_log (id, ts_iso, student_id, event, payload_json)
      Append-only audit trail for GDPR + debug.

  consent (student_id, consent_given, consent_iso)
      GDPR consent tracking. Default not-given.

Concurrency note
----------------
SQLite WAL handles concurrent readers + a single writer well. For
hundreds of concurrent students you'd want Postgres; for tens-to-low-
hundreds, this is fine. Each write is in its own short transaction.
"""
from __future__ import annotations
import json
import sqlite3
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple


_DEFAULT_DB_PATH = Path(__file__).resolve().parents[2] / "data" / "cpal.db"

_DB_INSTANCE: Optional["DBStore"] = None
_DB_LOCK = threading.Lock()


def _utcnow_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


class DBStore:
    """Thin SQLite wrapper. All methods are thread-safe."""

    def __init__(self, db_path: Optional[Path] = None):
        self.path = Path(db_path) if db_path else _DEFAULT_DB_PATH
        self.path.parent.mkdir(parents=True, exist_ok=True)
        # check_same_thread=False + an explicit lock so we can share
        # one connection across the Gradio request threads. SQLite's
        # default thread mode would otherwise reject this.
        self._conn = sqlite3.connect(
            str(self.path), check_same_thread=False, timeout=20.0,
        )
        self._lock = threading.RLock()
        self._init_schema()

    def _init_schema(self) -> None:
        with self._lock, self._conn:
            self._conn.executescript("""
                PRAGMA journal_mode=WAL;
                PRAGMA synchronous=NORMAL;
                PRAGMA foreign_keys=ON;

                CREATE TABLE IF NOT EXISTS mastery (
                    student_id    TEXT NOT NULL,
                    skill         TEXT NOT NULL,
                    p_mastered    REAL NOT NULL,
                    last_seen_iso TEXT NOT NULL,
                    PRIMARY KEY (student_id, skill)
                );
                CREATE INDEX IF NOT EXISTS mastery_student_idx
                    ON mastery (student_id);

                CREATE TABLE IF NOT EXISTS student_state (
                    student_id   TEXT PRIMARY KEY,
                    json_payload TEXT NOT NULL,
                    updated_iso  TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS variant_assignment (
                    student_id   TEXT NOT NULL,
                    experiment   TEXT NOT NULL,
                    variant      TEXT NOT NULL,
                    assigned_iso TEXT NOT NULL,
                    PRIMARY KEY (student_id, experiment)
                );

                CREATE TABLE IF NOT EXISTS audit_log (
                    id           INTEGER PRIMARY KEY AUTOINCREMENT,
                    ts_iso       TEXT NOT NULL,
                    student_id   TEXT,
                    event        TEXT NOT NULL,
                    payload_json TEXT
                );
                CREATE INDEX IF NOT EXISTS audit_student_idx
                    ON audit_log (student_id);
                CREATE INDEX IF NOT EXISTS audit_event_idx
                    ON audit_log (event);

                CREATE TABLE IF NOT EXISTS consent (
                    student_id     TEXT PRIMARY KEY,
                    consent_given  INTEGER NOT NULL,
                    consent_iso    TEXT NOT NULL
                );
            """)

    # ── Mastery ────────────────────────────────────────────────────────
    def get_mastery(self, student_id: str, skill: str
                    ) -> Optional[Tuple[float, str]]:
        """Returns (p_mastered, last_seen_iso) or None if no row."""
        with self._lock:
            row = self._conn.execute(
                "SELECT p_mastered, last_seen_iso FROM mastery "
                "WHERE student_id=? AND skill=?",
                (student_id, skill),
            ).fetchone()
        return (float(row[0]), row[1]) if row else None

    def get_all_mastery(self, student_id: str) -> Dict[str, Tuple[float, str]]:
        with self._lock:
            rows = self._conn.execute(
                "SELECT skill, p_mastered, last_seen_iso FROM mastery "
                "WHERE student_id=?", (student_id,),
            ).fetchall()
        return {r[0]: (float(r[1]), r[2]) for r in rows}

    def upsert_mastery(self, student_id: str, skill: str,
                       p_mastered: float, last_seen_iso: Optional[str] = None
                       ) -> None:
        ts = last_seen_iso or _utcnow_iso()
        with self._lock, self._conn:
            self._conn.execute(
                "INSERT INTO mastery (student_id, skill, p_mastered, last_seen_iso) "
                "VALUES (?, ?, ?, ?) "
                "ON CONFLICT(student_id, skill) DO UPDATE SET "
                "p_mastered=excluded.p_mastered, "
                "last_seen_iso=excluded.last_seen_iso",
                (student_id, skill, float(p_mastered), ts),
            )

    # ── Student state ──────────────────────────────────────────────────
    def get_student_state(self, student_id: str) -> Optional[Dict[str, Any]]:
        with self._lock:
            row = self._conn.execute(
                "SELECT json_payload FROM student_state WHERE student_id=?",
                (student_id,),
            ).fetchone()
        if not row:
            return None
        try:
            return json.loads(row[0])
        except Exception:
            return None

    def upsert_student_state(self, student_id: str, state: Dict[str, Any]
                              ) -> None:
        payload = json.dumps(state, default=str)
        with self._lock, self._conn:
            self._conn.execute(
                "INSERT INTO student_state (student_id, json_payload, updated_iso) "
                "VALUES (?, ?, ?) "
                "ON CONFLICT(student_id) DO UPDATE SET "
                "json_payload=excluded.json_payload, "
                "updated_iso=excluded.updated_iso",
                (student_id, payload, _utcnow_iso()),
            )

    def list_students(self) -> List[str]:
        """Every student_id we've seen (from mastery OR state OR audit)."""
        with self._lock:
            rows = self._conn.execute("""
                SELECT DISTINCT student_id FROM (
                    SELECT student_id FROM mastery
                    UNION
                    SELECT student_id FROM student_state
                    UNION
                    SELECT student_id FROM audit_log WHERE student_id IS NOT NULL
                )
            """).fetchall()
        return sorted(r[0] for r in rows if r[0])

    # ── A/B variant assignment ─────────────────────────────────────────
    def get_variant(self, student_id: str, experiment: str) -> Optional[str]:
        with self._lock:
            row = self._conn.execute(
                "SELECT variant FROM variant_assignment "
                "WHERE student_id=? AND experiment=?",
                (student_id, experiment),
            ).fetchone()
        return row[0] if row else None

    def set_variant(self, student_id: str, experiment: str, variant: str
                    ) -> None:
        with self._lock, self._conn:
            self._conn.execute(
                "INSERT OR IGNORE INTO variant_assignment "
                "(student_id, experiment, variant, assigned_iso) "
                "VALUES (?, ?, ?, ?)",
                (student_id, experiment, variant, _utcnow_iso()),
            )

    # ── Audit log ──────────────────────────────────────────────────────
    def audit(self, event: str, student_id: Optional[str] = None,
              payload: Optional[Dict[str, Any]] = None) -> None:
        with self._lock, self._conn:
            self._conn.execute(
                "INSERT INTO audit_log (ts_iso, student_id, event, payload_json) "
                "VALUES (?, ?, ?, ?)",
                (_utcnow_iso(), student_id, event,
                 json.dumps(payload, default=str) if payload else None),
            )

    def audit_for_student(self, student_id: str) -> List[Dict[str, Any]]:
        with self._lock:
            rows = self._conn.execute(
                "SELECT ts_iso, event, payload_json FROM audit_log "
                "WHERE student_id=? ORDER BY id",
                (student_id,),
            ).fetchall()
        out = []
        for ts, ev, pl in rows:
            try:
                p = json.loads(pl) if pl else None
            except Exception:
                p = None
            out.append({"ts": ts, "event": ev, "payload": p})
        return out

    # ── Consent ────────────────────────────────────────────────────────
    def has_consent(self, student_id: str) -> bool:
        with self._lock:
            row = self._conn.execute(
                "SELECT consent_given FROM consent WHERE student_id=?",
                (student_id,),
            ).fetchone()
        return bool(row and row[0])

    def set_consent(self, student_id: str, given: bool) -> None:
        with self._lock, self._conn:
            self._conn.execute(
                "INSERT INTO consent (student_id, consent_given, consent_iso) "
                "VALUES (?, ?, ?) "
                "ON CONFLICT(student_id) DO UPDATE SET "
                "consent_given=excluded.consent_given, "
                "consent_iso=excluded.consent_iso",
                (student_id, 1 if given else 0, _utcnow_iso()),
            )

    # ── GDPR ───────────────────────────────────────────────────────────
    def export_student(self, student_id: str) -> Dict[str, Any]:
        """All data we have for this student — for GDPR /export."""
        return {
            "student_id":    student_id,
            "mastery":       self.get_all_mastery(student_id),
            "state":         self.get_student_state(student_id),
            "consent":       self.has_consent(student_id),
            "variants": {
                row[0]: row[1] for row in self._conn.execute(
                    "SELECT experiment, variant FROM variant_assignment "
                    "WHERE student_id=?", (student_id,)
                ).fetchall()
            },
            "audit":         self.audit_for_student(student_id),
            "exported_at":   _utcnow_iso(),
        }

    def delete_student(self, student_id: str) -> Dict[str, int]:
        """Wipe every row referencing this student. Returns row counts.

        Audit_log is preserved (the deletion itself is logged), but
        existing audit rows are dropped — except for one tombstone
        recording the deletion timestamp.
        """
        counts: Dict[str, int] = {}
        with self._lock, self._conn:
            for tbl in ("mastery", "student_state", "variant_assignment",
                         "consent", "audit_log"):
                cur = self._conn.execute(
                    f"DELETE FROM {tbl} WHERE student_id=?", (student_id,))
                counts[tbl] = cur.rowcount
            # Tombstone — keeps a record that the deletion happened,
            # without the deleted PII.
            self._conn.execute(
                "INSERT INTO audit_log (ts_iso, student_id, event, payload_json) "
                "VALUES (?, ?, ?, ?)",
                (_utcnow_iso(), None, "gdpr_delete",
                 json.dumps({"deleted_id_hash":
                              str(abs(hash(student_id)) % 10**10),
                              "row_counts": counts})),
            )
        return counts

    # ── Aggregations (for teacher dashboard) ───────────────────────────
    def mastery_heatmap(self) -> Dict[str, Dict[str, float]]:
        """Returns {student_id: {skill: p_mastered}} for ALL students."""
        with self._lock:
            rows = self._conn.execute(
                "SELECT student_id, skill, p_mastered FROM mastery"
            ).fetchall()
        out: Dict[str, Dict[str, float]] = {}
        for sid, sk, p in rows:
            out.setdefault(sid, {})[sk] = float(p)
        return out

    def struggling_concepts(self, threshold: float = 0.40,
                            limit: int = 10) -> List[Tuple[str, int, float]]:
        """[(skill, n_students_below_threshold, mean_mastery), ...]
        Sorted by n_students_below_threshold descending."""
        with self._lock:
            rows = self._conn.execute(
                "SELECT skill, COUNT(*) AS n_low, AVG(p_mastered) AS mean_p "
                "FROM mastery WHERE p_mastered < ? "
                "GROUP BY skill ORDER BY n_low DESC LIMIT ?",
                (float(threshold), int(limit)),
            ).fetchall()
        return [(r[0], int(r[1]), float(r[2])) for r in rows]

    # ── Progression queries (added 2026-05-22) ─────────────────────────
    def progression_for(self, student_id: str, skill: str
                        ) -> List[Dict[str, Any]]:
        """All turn_completed audit rows for this (student, skill),
        oldest → newest. Each row is `{ts, lp_before, lp_after,
        mastery_before, mastery_after, intervention, conf, ...}`."""
        with self._lock:
            rows = self._conn.execute(
                "SELECT ts_iso, payload_json FROM audit_log "
                "WHERE student_id=? AND event='turn_completed' "
                "ORDER BY id",
                (student_id,),
            ).fetchall()
        out = []
        for ts, pl in rows:
            try:
                p = json.loads(pl) if pl else {}
            except Exception:
                p = {}
            if p.get("skill") != skill:
                continue
            p["_ts"] = ts
            out.append(p)
        return out

    def forecast_lp_advance(self, student_id: str, skill: str
                            ) -> Optional[Dict[str, Any]]:
        """Estimate turns until the next LP level, based on the recent
        rate of LP advance. Returns None when there isn't enough data
        (< 3 turns recorded for this skill).

        Algorithm: count LP level advances (deltas > 0) in the most
        recent N turns; if rate is >0, project at that rate to next
        level. If rate is 0, return "plateau — unknown ETA".
        """
        rows = self.progression_for(student_id, skill)
        if len(rows) < 3:
            return None
        recent = rows[-10:]
        # LP_INDEX ordering
        lp_order = ["L1", "L2", "L3", "L4"]
        advances = 0
        for r in recent:
            try:
                if (lp_order.index(r.get("lp_after", "L1"))
                        > lp_order.index(r.get("lp_before", "L1"))):
                    advances += 1
            except ValueError:
                continue
        n = len(recent)
        if advances == 0:
            return {"status": "plateau", "turns_recent": n, "advances": 0,
                    "current_lp": recent[-1].get("lp_after", "?"),
                    "eta_turns_to_next": None}
        rate = advances / n   # advances per turn
        current = recent[-1].get("lp_after", "L1")
        try:
            steps_remaining = 3 - lp_order.index(current)
        except ValueError:
            steps_remaining = 1
        eta = int(round(steps_remaining / rate)) if rate > 0 else None
        return {"status": "advancing", "turns_recent": n,
                "advances": advances, "rate_per_turn": round(rate, 3),
                "current_lp": current, "eta_turns_to_next": eta}

    def cohort_percentile(self, student_id: str, skill: str
                          ) -> Optional[float]:
        """Percentile of this student's CURRENT mastery in the cohort
        for `skill`. 0.0 = worst, 1.0 = best. None if no mastery row."""
        own = self.get_mastery(student_id, skill)
        if not own:
            return None
        own_p = own[0]
        with self._lock:
            rows = self._conn.execute(
                "SELECT p_mastered FROM mastery WHERE skill=?", (skill,),
            ).fetchall()
        ps = [float(r[0]) for r in rows]
        if not ps:
            return None
        below = sum(1 for p in ps if p < own_p)
        return round(below / len(ps), 3)

    def mastery_trajectory(self, student_id: str, skill: str
                           ) -> List[Tuple[str, float]]:
        """List of (ts_iso, mastery_after) points for sparkline rendering."""
        rows = self.progression_for(student_id, skill)
        return [(r["_ts"], float(r.get("mastery_after", 0.0)))
                for r in rows if "mastery_after" in r]

    def lp_trajectory(self, student_id: str, skill: str
                      ) -> List[Tuple[str, str]]:
        rows = self.progression_for(student_id, skill)
        return [(r["_ts"], r.get("lp_after", "?")) for r in rows
                if "lp_after" in r]

    def intervention_counts(self) -> Dict[str, int]:
        """{intervention_type: count} from audit events with event='intervention_picked'."""
        with self._lock:
            rows = self._conn.execute(
                "SELECT payload_json FROM audit_log WHERE event=?",
                ("intervention_picked",),
            ).fetchall()
        counts: Dict[str, int] = {}
        for (pl,) in rows:
            try:
                p = json.loads(pl) if pl else {}
                k = p.get("type") or "unknown"
                counts[k] = counts.get(k, 0) + 1
            except Exception:
                pass
        return counts


def get_db(path: Optional[Path] = None) -> DBStore:
    """Process-wide singleton."""
    global _DB_INSTANCE
    if _DB_INSTANCE is not None:
        return _DB_INSTANCE
    with _DB_LOCK:
        if _DB_INSTANCE is None:
            _DB_INSTANCE = DBStore(path)
    return _DB_INSTANCE
