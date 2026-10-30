"""Tag concepts in Java code with the regex channels stored on each concept node.

Only the code is read. Aliases (for the student's words) are never used here.
"""
from __future__ import annotations

import re
from typing import Any

from .mask import mask_java, split_statements

Hit = dict[str, Any]  # {channel, name, decisive, match, line}

_COMMAND_RE = re.compile(r"(?:^|[%$:;]\s*|\s)((?:javac|java)\s+[^;%\n]*)")

_compiled: dict[tuple[str, int], re.Pattern[str]] = {}


def _rx(pattern: str, flags: int = 0) -> re.Pattern[str]:
    key = (pattern, flags)
    rx = _compiled.get(key)
    if rx is None:
        rx = re.compile(pattern, flags)
        _compiled[key] = rx
    return rx


def command_segments(text: str) -> list[str]:
    """Every shell command segment ``javac …`` / ``java …`` in the text."""
    return [m.group(1).strip() for m in _COMMAND_RE.finditer(text)]


def _line_of(code: str, pos: int) -> int:
    return code.count("\n", 0, pos) + 1


def _hit(channel: str, name: str, decisive: bool, m: re.Match[str], code: str, base: int = 0) -> Hit:
    return {
        "channel": channel,
        "name": name,
        "decisive": bool(decisive),
        "match": m.group(0),
        "line": _line_of(code, base + m.start()),
    }


class _Prepared:
    """The code, its masked form, the statement splits and the command segments, computed once."""

    def __init__(self, code: str):
        self.code = code
        self.masked = mask_java(code)
        self._splits: dict[bool, list[tuple[int, str]]] = {}
        self.commands: list[tuple[int, str]] = []
        base = 0
        for seg in command_segments(code):
            start = max(code.find(seg, base), 0)
            self.commands.append((start, seg))
            base = start + len(seg)

    def statements(self, raw: bool) -> list[tuple[int, str]]:
        """(offset, piece) pairs for the raw or masked text; offsets are identical in both."""
        if raw not in self._splits:
            text = self.code if raw else self.masked
            out, base = [], 0
            for piece in split_statements(text):
                start = text.find(piece, base)
                out.append((start, piece))
                base = start + len(piece)
            self._splits[raw] = out
        return self._splits[raw]


def tag_concept(code: str, rd: dict[str, Any], prepared: "_Prepared | None" = None) -> list[Hit]:
    """Run every regex channel of one reader block against the code."""
    if rd.get("code_visible") is False:
        return []
    prep = prepared or _Prepared(code)
    t = code if rd.get("code_text") == "raw" else prep.masked
    hits: list[Hit] = []

    for p in rd.get("code_patterns") or []:
        m = _rx(p, re.M).search(t)
        if m:
            hits.append(_hit("pattern", p, False, m, code))

    for s in rd.get("signals") or []:
        if "regex" not in s:
            continue
        sources = s.get("sources")
        if sources and "code" not in sources:
            continue
        raw = s.get("text") == "raw"
        tt = code if raw else t
        name = s.get("name", "")
        decisive = bool(s.get("decisive"))
        if s.get("scope") == "statement":
            rx = _rx(s["regex"], re.M)
            for start, piece in prep.statements(raw or rd.get("code_text") == "raw"):
                m = rx.search(piece)
                if m:
                    hits.append(_hit("signal", name, decisive, m, code, start))
                    break
        else:
            m = _rx(s["regex"], re.M | re.S).search(tt)
            if m:
                hits.append(_hit("signal", name, decisive, m, code))

    for o in rd.get("operator_symbols") or []:
        pos = t.find(o)
        if pos >= 0:
            hits.append({"channel": "operator", "name": o, "decisive": False, "match": o, "line": _line_of(code, pos)})

    for ty in rd.get("java_types") or []:
        m = _rx(r"\b" + re.escape(ty) + r"\b").search(t)
        if m:
            hits.append(_hit("type", ty, False, m, code))

    cmd_patterns = rd.get("command_patterns") or []
    if cmd_patterns:
        for start, seg in prep.commands:
            for p in cmd_patterns:
                m = _rx(p).search(seg)
                if m:
                    hits.append(_hit("command", p, False, m, code, start))

    return hits


def tag_code(code: str, reader: dict[str, dict[str, Any]]) -> dict[str, list[Hit]]:
    """``reader`` maps concept id -> reader block. Returns concept id -> hits
    for every concept with at least one hit."""
    tags: dict[str, list[Hit]] = {}
    prep = _Prepared(code)
    for cid, rd in reader.items():
        hits = tag_concept(code, rd, prep)
        if hits:
            tags[cid] = hits
    return tags


def reader_blocks(kg: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """Concept id -> reader block, from a loaded KG."""
    return {c["id"]: (c.get("reader") or {}) for c in kg["concepts"]}
