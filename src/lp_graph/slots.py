"""Slots: the (slot, value, negated) facts a sentence states.

One extractor serves both sides of the comparison, so the reader compares
like with like:

* offline, ``scripts/prepare_kg_parts.py`` runs it on every edge-logic part,
  way rule and misconception pair of the graph;
* online, ``statements.py`` runs it on every answer clause.

A slot is a small fact such as ``cursor=next_line`` ("moves to the next
line"), ``compile=compile_error`` ("won't compile"), ``value=0`` for a
variable ("count is 0"), or ``output=0`` ("it prints 0"). Each slot is
attached to a *subject*: the concept or code variable named nearest to it,
so "println stays on the same line" gives ``cursor=same_line`` on
``println``, not on ``print``.

Phrase slots come from ``lexicon.PHRASES``; pattern slots (output, value,
runs N times) from the regexes below. All matching is on normalised text
(lower case, contractions expanded, '-' read as a space).
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from functools import lru_cache

from . import lexicon

_PUNCT_BREAK = re.compile(r"[.;:!?,]")


@dataclass(frozen=True)
class Mention:
    """A concept alias or code variable found in a text."""

    start: int
    end: int
    alias: str
    concepts: tuple[str, ...] = ()
    var: str | None = None

    @property
    def subject(self) -> str | None:
        if self.var:
            return f"var:{self.var}"
        return self.concepts[0] if len(self.concepts) == 1 else None


@dataclass(frozen=True)
class Slot:
    """One stated fact. ``subject`` is a concept id, ``var:<name>`` or None."""

    name: str
    value: str
    negated: bool = False
    subject: str | None = None
    implied: bool = False
    span: tuple[int, int] = field(default=(0, 0), compare=False)

    def key(self) -> tuple:
        return (self.name, self.value, self.negated, self.subject or "", self.implied)

    def as_list(self) -> list:
        return [self.name, self.value, self.negated, self.subject, self.implied]


# --------------------------------------------------------------- normalising

def normalize(text: str) -> str:
    """Lower-case, expand contractions, read '-' and '_' as spaces.

    Character positions are not preserved; all mentions and slots are found
    on the normalised string.
    """
    t = text.replace("’", "'").replace("‘", "'")
    t = t.replace("“", '"').replace("”", '"').lower()
    for k in sorted(lexicon.CONTRACTIONS, key=lambda s: (-len(s), s)):
        t = t.replace(k, lexicon.CONTRACTIONS[k])
    t = re.sub(r"(?<=\w)-(?=\w)", " ", t)
    t = t.replace("_", " ")
    return re.sub(r"\s+", " ", t).strip()


@lru_cache(maxsize=32)
def alternation(keys: tuple[str, ...]) -> re.Pattern:
    """One regex matching any key as a whole word; keys must be longest-first,
    so at each position the longest key wins."""
    return re.compile(r"(?<![\w])(?:" + "|".join(re.escape(k) for k in keys) + r")(?![\w])")


@lru_cache(maxsize=1)
def _phrase_table() -> tuple[re.Pattern, dict[str, tuple[tuple[str, str], ...]], frozenset[str]]:
    """All lexicon phrases: (regex, phrase -> [(slot, value)], absolute phrases).

    A phrase is *absolute* when it carries its own negation ("does not
    compile"), so a negation word before it does not flip it again.
    """
    emits: dict[str, list[tuple[str, str]]] = {}
    for slot in sorted(lexicon.PHRASES):
        for value in sorted(lexicon.PHRASES[slot]):
            for ph in lexicon.PHRASES[slot][value]:
                key = normalize(ph) if ph != "\\n" else "\\n"
                pair = (slot, value)
                if pair not in emits.setdefault(key, []):
                    emits[key].append(pair)
    keys = tuple(sorted(emits, key=lambda k: (-len(k), k)))
    absolute = frozenset(k for k in keys
                         if any(re.search(rf"(?<!\w){n}(?!\w)", k) for n in lexicon.NEGATION))
    return alternation(keys), {k: tuple(sorted(v)) for k, v in emits.items()}, absolute


def number(token: str) -> str:
    """Canonical value text: number words -> digits, quotes stripped."""
    t = token.strip().strip(".,").strip()
    if len(t) >= 2 and t[0] == t[-1] and t[0] in "\"'":
        return t[1:-1]
    t = lexicon.NUMBER_WORDS.get(t, t)
    if re.fullmatch(r"-?\d+\.0+", t):
        return t  # keep 0.0 distinct from 0 (double vs int output)
    return t


# ----------------------------------------------------------------- mentions

def find_mentions(
    text_norm: str,
    alias_index: list[tuple[str, tuple[str, ...]]],
    variables: tuple[str, ...] = (),
    fuzzy: bool = False,
) -> list[Mention]:
    """Concept aliases and code variable names in ``text_norm``.

    ``alias_index`` is ``[(alias, concepts)]`` sorted longest-first (see
    ``graph.KG.alias_index``). Code variable names win over aliases (a
    variable called ``count`` is the variable, not the counter pattern).
    Matches never overlap; with ``fuzzy`` a token of >=5 letters also matches
    a one-word alias of >=5 letters within one edit.
    """
    taken: list[tuple[int, int]] = []
    out: list[Mention] = []

    def free(s: int, e: int) -> bool:
        return all(e <= a or s >= b for a, b in taken)

    masked = text_norm
    var_keys = tuple(sorted({v.lower() for v in variables}, key=lambda k: (-len(k), k)))
    if var_keys:
        for m in alternation(var_keys).finditer(text_norm):
            if m.start() and text_norm[m.start() - 1] == ".":
                continue
            taken.append((m.start(), m.end()))
            out.append(Mention(m.start(), m.end(), m.group(0), (), m.group(0)))
            masked = masked[:m.start()] + " " * (m.end() - m.start()) + masked[m.end():]
    table = dict(alias_index)
    for m in alternation(tuple(a for a, _ in alias_index)).finditer(masked):
        taken.append((m.start(), m.end()))
        out.append(Mention(m.start(), m.end(), m.group(0), table[m.group(0)]))
    if fuzzy:
        singles = [(a, c) for a, c in alias_index if " " not in a and len(a) >= 5 and a.isalpha()]
        for m in re.finditer(r"[a-z]{5,}", text_norm):
            if not free(m.start(), m.end()):
                continue
            tok = m.group(0)
            for alias, concepts in singles:
                if abs(len(alias) - len(tok)) <= 1 and edit_distance(tok, alias) <= 1:
                    taken.append((m.start(), m.end()))
                    out.append(Mention(m.start(), m.end(), alias, concepts))
                    break
    return sorted(out, key=lambda x: (x.start, x.end, x.alias))


def edit_distance(a: str, b: str) -> int:
    """Levenshtein distance (small strings only)."""
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


def _subject(mentions: list[Mention], start: int, end: int) -> str | None:
    """Subject of a slot at [start, end): nearest mention before, else after."""
    before = [m for m in mentions if m.end <= start and m.subject]
    if before:
        return max(before, key=lambda m: (m.end, -m.start)).subject
    after = [m for m in mentions if m.start >= end and m.subject]
    if after:
        return min(after, key=lambda m: (m.start, m.end)).subject
    return None


def _negated_before(text: str, start: int) -> bool:
    """True if a negation word sits in the 4 words before ``start`` (same clause)."""
    window = text[max(0, start - 40):start]
    seg = _PUNCT_BREAK.split(window)[-1]
    words = seg.split()[-4:]
    for w in reversed(words):
        if w in lexicon.NEGATION_BREAKERS:
            return False
        if w in lexicon.NEGATION:
            return True
    return False


# -------------------------------------------------------------------- slots

_VAL = (r"(-?\d+(?:\.\d+)?|\"[^\"]*\"|'[^']*'|true|false|null|nothing|"
        + "|".join(sorted(lexicon.NUMBER_WORDS, key=lambda s: (-len(s), s))) + r")")
_END = r"(?!\w)(?!\.\d)"  # a value may end a sentence: "it prints 0."
_OUTPUT_RES = [
    re.compile(r"\b(?:prints?|printed|printing|outputs?|outputted|displays?|displayed|shows?)"
               r"(?: out)?(?: the)?(?: (?:value|number|text|string|word))?(?: of)?(?: is)? " + _VAL + _END),
    re.compile(r"\b(?:the )?(?:output|result|answer|printout)(?: of the program| of the code)?"
               r" (?:is|will be|would be|should be|=) " + _VAL + _END),
]
_VALUE_RE = re.compile(
    r"\b([a-z][a-z0-9]*|it)\s+(?:is|=|==|equals|becomes|will be|would be|holds|stores|contains|"
    r"has the value(?: of)?|has a value of|is equal to|is set to|gets|is now|starts at|starts as)"
    r"\s+(?:the value |a value of |equal to )?" + _VAL + _END)
_RUNS_RE = re.compile(r"\b(?:runs|loops|repeats|executes|iterates|goes)\s+(?:around\s+)?"
                      r"(\d+|" + "|".join(sorted(lexicon.NUMBER_WORDS, key=len, reverse=True)) + r")\s+times\b")
_NOT_A_VARIABLE = frozenset({
    "output", "result", "answer", "printout", "there", "this", "that", "what",
    "which", "who", "line", "value", "number", "program", "code", "loop",
})


def extract_slots(
    text_norm: str,
    mentions: list[Mention] | None = None,
    resolve_pronoun: str | None = None,
) -> list[Slot]:
    """All slots in one normalised text, sorted by position then key.

    ``mentions`` (from ``find_mentions``) give each slot its subject;
    ``resolve_pronoun`` is the variable "it" stands for (statements.py).
    """
    mentions = mentions or []
    found: list[Slot] = []
    rx, emits, absolute = _phrase_table()
    for m in rx.finditer(text_norm):
        s, e, ph = m.start(), m.end(), m.group(0)
        neg = ph not in absolute and _negated_before(text_norm, s)
        subj = _subject(mentions, s, e)
        for slot, value in emits[ph]:
            v = lexicon.OPPOSITE.get(value, value) if neg else value
            found.append(Slot(slot, v, neg and v == value, subj, False, (s, e)))
    for rx in _OUTPUT_RES:
        for m in rx.finditer(text_norm):
            neg = _negated_before(text_norm, m.start())
            val = number(m.group(1))
            if val == "nothing":
                val = ""
            found.append(Slot("output", val, neg, _subject(mentions, m.start(), m.start(1)),
                              False, (m.start(), m.end())))
    for m in _VALUE_RE.finditer(text_norm):
        who = m.group(1)
        if who in _NOT_A_VARIABLE:
            continue
        var = resolve_pronoun if who == "it" else who
        known = {x.var for x in mentions if x.var}
        if var is None or (known and var not in known and who != "it"):
            continue
        neg = _negated_before(text_norm, m.start(2)) or " not " in m.group(0)
        found.append(Slot("value", number(m.group(2)), neg, f"var:{var}", False, (m.start(), m.end())))
    for m in _RUNS_RE.finditer(text_norm):
        found.append(Slot("runs", number(m.group(1)), _negated_before(text_norm, m.start()),
                          _subject(mentions, m.start(), m.end()), False, (m.start(), m.end())))
    found = _dedupe(found)
    return sorted(found, key=lambda s: (s.span, s.key()))


def _dedupe(slots: list[Slot]) -> list[Slot]:
    seen: set[tuple] = set()
    out = []
    for s in sorted(slots, key=lambda x: (x.span, x.key())):
        if s.key() in seen:
            continue
        seen.add(s.key())
        out.append(s)
    return out


def implied_slots(slots: list[Slot]) -> list[Slot]:
    """Facts a slot implies: predicting an output implies the code compiles
    and runs without error (unless the statement says otherwise)."""
    names = {s.name for s in slots if not s.implied}
    out: list[Slot] = []
    for s in slots:
        if s.name == "output" and not s.negated and s.value != "":
            if "compile" not in names:
                out.append(Slot("compile", "compiles", False, s.subject, True, s.span))
            if "crash" not in names:
                out.append(Slot("crash", "no_error", False, s.subject, True, s.span))
    return _dedupe(out)


# --------------------------------------------------------------- comparing

def _is_number(v: str) -> bool:
    return bool(re.fullmatch(r"-?\d+(?:\.\d+)?", v))


def values_agree(name: str, a: str, b: str) -> bool:
    """Do two values of the same slot agree?

    For ``value``, a concrete number is consistent with ``default`` (some
    value exists) but not with ``none`` (no value at all).
    """
    if a == b:
        return True
    if name == "value":
        if _is_number(a) and _is_number(b):
            return float(a) == float(b)
        pair = {a, b}
        if "default" in pair and (pair - {"default"}).pop() not in ("none", "garbage"):
            return True
        return False
    if name == "output" and _is_number(a) and _is_number(b):
        return a == b
    return False


def slot_agrees(s: Slot, name: str, value: str) -> bool | None:
    """Agreement of a stated slot with a reference (name, value).

    None when the slot does not address that name. A negated slot that kept
    its value (no opposite exists) agrees only by differing.
    """
    if s.name != name:
        return None
    same = values_agree(name, s.value, value)
    return (not same) if s.negated else same
