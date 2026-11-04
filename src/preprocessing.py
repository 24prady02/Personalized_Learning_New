"""Preprocessing of a scenario's Java code before any pattern is matched.

1. ``normalize_text``: pasted look-alike characters (curly quotes, non-breaking spaces, Unicode minus) to ASCII (same length).
   ``mask_java``: blank the inside of string literals and the text of comments (same length, newlines kept); char literals stay.
2. ``split_statements``: cut the text at ``;`` ``{`` ``}`` at parenthesis depth 0 (a ``for (…; …; …)`` header stays whole).
3. ``command_segments``: the ``javac …`` / ``java …`` shell segments in the text.
4. ``Prepared``: all of the above computed once per program and shared by every concept's patterns.

Standard library only.
"""
from __future__ import annotations

import re

_COMMAND_RE = re.compile(r"(?:^|[%$:;]\s*|\s)((?:javac|java)\s+[^;%\n]*)")

# Characters a word processor or a web page puts into pasted code, each mapped to the ASCII character the
# student meant. Every mapping is one character to one character, so offsets and line numbers do not move.
_PASTE_CHARS = str.maketrans({
    "“": '"', "”": '"', "„": '"', "‟": '"', "″": '"',   # curly / low / prime double quotes
    "‘": "'", "’": "'", "‚": "'", "‛": "'", "′": "'",   # curly / low / prime single quotes
    " ": " ", " ": " ", " ": " ", "　": " ",                  # non-breaking and wide spaces
    "−": "-", "–": "-", "—": "-",                                  # minus sign, en dash, em dash
    "×": "*", "∕": "/", "⁄": "/",                                  # multiplication sign, division slashes
})


def normalize_text(code: str) -> str:
    """Return ``code`` with pasted look-alike characters (curly quotes, non-breaking spaces, Unicode minus and
    dashes, multiplication and division signs) replaced by the ASCII character the student meant. Same length."""
    return code.translate(_PASTE_CHARS)


def mask_java(code: str) -> str:
    """Return a string of the same length as ``code`` with the inside of string
    literals and the text of comments replaced by spaces. Char literals (``'A'``,
    ``'\\n'``) are kept as they are: they are code, not text.

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
            blank = quote == '"'
            i += 1
            while i < n and code[i] != quote:
                if code[i] == "\\" and i + 1 < n:
                    if blank:
                        out[i] = " "
                        if code[i + 1] != "\n":
                            out[i + 1] = " "
                    i += 2
                    continue
                if code[i] == "\n":  # unterminated literal: stop at end of line
                    break
                if blank:
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
        self.code = code = normalize_text(code)
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
