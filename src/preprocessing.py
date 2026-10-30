"""Preprocessing of a scenario's Java code before any pattern is matched.

1. ``mask_java``: blank the inside of string / char literals and the text of comments (same length, newlines kept).
2. ``split_statements``: cut the text at ``;`` ``{`` ``}`` at parenthesis depth 0 (a ``for (…; …; …)`` header stays whole).
3. ``command_segments``: the ``javac …`` / ``java …`` shell segments in the text.
4. ``Prepared``: all of the above computed once per program and shared by every concept's patterns.

Standard library only.
"""
from __future__ import annotations

import re

_COMMAND_RE = re.compile(r"(?:^|[%$:;]\s*|\s)((?:javac|java)\s+[^;%\n]*)")


def mask_java(code: str) -> str:
    """Return a string of the same length as ``code`` with the inside of string
    and char literals and the text of comments replaced by spaces.

    Quotes are kept. ``\\"``, ``\\'`` and ``\\\\`` inside literals are handled.
    Newlines are kept so line numbers stay valid.
    """
    out = list(code)
    n = len(code)
    i = 0
    while i < n:
        ch = code[i]
        if ch == '"' or ch == "'":
            quote = ch
            i += 1
            while i < n and code[i] != quote:
                if code[i] == "\\" and i + 1 < n:
                    out[i] = " "
                    if code[i + 1] != "\n":
                        out[i + 1] = " "
                    i += 2
                    continue
                if code[i] == "\n":  # unterminated literal: stop at end of line
                    break
                out[i] = " "
                i += 1
            i += 1  # closing quote (or past the newline)
            continue
        if ch == "/" and i + 1 < n and code[i + 1] == "/":
            while i < n and code[i] != "\n":
                out[i] = " "
                i += 1
            continue
        if ch == "/" and i + 1 < n and code[i + 1] == "*":
            out[i] = " "
            out[i + 1] = " "
            i += 2
            while i < n and not (code[i] == "*" and i + 1 < n and code[i + 1] == "/"):
                if code[i] != "\n":
                    out[i] = " "
                i += 1
            if i < n:
                out[i] = " "
                out[i + 1] = " "
                i += 2
            continue
        i += 1
    return "".join(out)


def split_statements(text: str) -> list[str]:
    """Split on ``;``, ``{`` and ``}`` at parenthesis depth 0 only, so a
    ``for (init; test; update)`` header stays in one piece.

    Each piece keeps its terminating character so statement-scoped regexes
    that look for ``;`` still work. Empty pieces are dropped.
    """
    pieces: list[str] = []
    depth = 0
    start = 0
    for i, ch in enumerate(text):
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth = max(0, depth - 1)
        elif ch in ";{}" and depth == 0:
            piece = text[start : i + 1]
            if piece.strip():
                pieces.append(piece)
            start = i + 1
    tail = text[start:]
    if tail.strip():
        pieces.append(tail)
    return pieces


def command_segments(text: str) -> list[str]:
    """Every shell command segment ``javac …`` / ``java …`` in the text."""
    return [m.group(1).strip() for m in _COMMAND_RE.finditer(text)]


class Prepared:
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
