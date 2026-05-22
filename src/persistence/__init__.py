"""Persistence layer for CPAL student state.

Added 2026-05-21 as part of the production-hardening pass. Existing
JSON files (data/dina/*.json, data/student_states.json) are still
read at startup for backward compatibility, but every write goes
through SQLite via db_store.get_db().
"""
