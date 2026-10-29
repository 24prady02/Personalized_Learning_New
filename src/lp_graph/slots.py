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
    hypothetical: bool = False
    extra: tuple[tuple[str, str], ...] = field(default=(), compare=False)

    def key(self) -> tuple:
        return (self.name, self.value, self.negated, self.subject or "", self.implied,
                self.hypothetical)

    def get(self, k: str, default: str = "") -> str:
        return dict(self.extra).get(k, default)

    @property
    def kind(self) -> str:
        """rule | output | value | expr | other (see lexicon.RULE_SLOTS)."""
        if self.name in lexicon.RULE_SLOTS:
            return "rule"
        if self.name in ("output", "printed"):
            return "output"
        if self.name in ("value", "expr"):
            return self.name
        return "other"

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




def _subject(mentions: list[Mention], start: int, end: int, text: str = "") -> str | None:
    """Subject of a slot at [start, end): the first mention of its sub-clause
    (approximately the grammatical subject), else the nearest mention before,
    else the nearest after."""
    if text:
        cuts = [m.end() for m in lexicon.rx("subclause").finditer(text, 0, start)]
        lo = cuts[-1] if cuts else 0
        first = [m for m in mentions if lo <= m.start and m.end <= start and m.subject]
        if first:
            return min(first, key=lambda m: (m.start, m.end)).subject
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
    seg = lexicon.rx("punct_break").split(window)[-1]
    words = seg.split()[-4:]
    for w in reversed(words):
        if w in lexicon.NEGATION_BREAKERS:
            return False
        if w in lexicon.NEGATION:
            return True
    return False


# -------------------------------------------------------------------- slots

def _seq_value(raw: str) -> str:
    """Canonical printed sequence: '/' and '|' separate lines, quotes removed."""
    out = []
    for ln in re.split(r"\s*[/|]\s*", raw.strip()):
        toks = [number(x) for x in re.findall(r"\"[^\"]*\"|'[^']*'|[^\s,]+", ln.strip(" ,"))]
        out.append(" ".join(toks))
    return "\n".join(out)


def extract_slots(
    text_norm: str,
    mentions: list[Mention] | None = None,
    resolve_pronoun: str | None = None,
    raw: str | None = None,
    prev_vars: tuple[str, ...] = (),
) -> list[Slot]:
    """All slots in one normalised text, sorted by position then key.

    ``mentions`` (from ``find_mentions``) give each slot its subject;
    ``resolve_pronoun`` is the variable "it" stands for (statements.py);
    ``raw`` is the original text (printed words in capitals are read from it);
    ``prev_vars`` are the variables of the previous clause ("both are b").
    """
    mentions = mentions or []
    found: list[Slot] = []
    rx, emits, absolute = _phrase_table()
    for m in rx.finditer(text_norm):
        s, e, ph = m.start(), m.end(), m.group(0)
        neg = ph not in absolute and _negated_before(text_norm, s)
        subj = _subject(mentions, s, e, text_norm)
        for slot, value in emits[ph]:
            v = lexicon.OPPOSITE.get(value, value) if neg else value
            found.append(Slot(slot, v, neg and v == value, subj, False, (s, e)))
    found += _elliptic_negation(text_norm, mentions, found)
    src = re.sub(r"\s+", " ", (raw if raw is not None else text_norm)
                 .replace("“", '"').replace("”", '"')).strip()
    taken: list[tuple[int, int]] = []
    for name, rgx in (("output", lexicon.rx("whole")), ("printed", lexicon.rx("prints"))):
        for m in rgx.finditer(src):
            if any(a <= m.start(1) < b for a, b in taken):
                continue
            body = m.group(1)
            if re.fullmatch(r"[A-Za-z]+", body) and (raw is None or not body.isupper()):
                continue  # a plain word, not printed text
            taken.append((m.start(1), m.end(1)))
            neg = _negated_before(src.lower(), m.start())
            found.append(Slot(name, _seq_value(body), neg, None, False, (m.start(), m.end())))
    for m in lexicon.rx("prints_nothing").finditer(text_norm):
        found.append(Slot("output", "", _negated_before(text_norm, m.start()), None, False,
                          (m.start(), m.end())))
    known = {x.var for x in mentions if x.var}
    # text inside quotes is printed text, never a claim about a variable
    unquoted = re.sub(r"\"[^\"]*\"", lambda q: " " * len(q.group(0)), text_norm)
    for m in lexicon.rx("value").finditer(unquoted):
        who = m.group(1)
        if who in lexicon.NOT_A_VARIABLE and who not in known:
            continue
        var = resolve_pronoun if who == "it" else who
        if var is None or (known and var not in known and who != "it"):
            continue
        # without known variables (graph text) only code-like names count: x, n1
        if not known and who != "it" and not re.fullmatch(r"[a-z]\d*", who):
            continue
        neg = _negated_before(text_norm, m.start(3)) or " not " in m.group(0)
        found.append(Slot("value", number(m.group(3)), neg, f"var:{var}", False,
                          (m.start(), m.end()), extra=(("verb", m.group(2)),)))
    for m in lexicon.rx("var_value").finditer(unquoted):
        who, verb, other = m.group(1), m.group(2), m.group(3)
        var = resolve_pronoun if who == "it" else who
        if not var or var not in known | {resolve_pronoun} or other not in known or other == var:
            continue
        found.append(Slot("value", f"var:{other}", " not " in m.group(0), f"var:{var}", False,
                          (m.start(), m.end()), extra=(("verb", verb),)))
    for m in lexicon.rx("both").finditer(text_norm):
        val = m.group(1)
        for v in sorted(set(prev_vars)):
            value = f"var:{val}" if val in known or val in prev_vars else number(val)
            if value != f"var:{v}":
                found.append(Slot("value", value, False, f"var:{v}", False, (m.start(), m.end()),
                                  extra=(("verb", "are"),)))
    for m in lexicon.rx("first_index").finditer(src.lower()):
        idx = m.group(1) or m.group(2)
        found.append(Slot("first_index", idx, _negated_before(src.lower(), m.start()), None, False,
                          (m.start(), m.end())))
    for m in lexicon.rx("expr").finditer(src.lower()):
        a, op, b, v = m.group(1), m.group(2), m.group(3), m.group(4)
        found.append(Slot("expr", v, False, f"expr:{a} {op} {b}", False, (m.start(), m.end()),
                          extra=(("expr", f"{a} {op} {b}"),)))
    for m in lexicon.rx("runs").finditer(text_norm):
        found.append(Slot("runs", number(m.group(1)), _negated_before(text_norm, m.start()),
                          _subject(mentions, m.start(), m.end(), text_norm), False, (m.start(), m.end())))
    found = _dedupe(found)
    return sorted(found, key=lambda s: (s.span, s.key()))


def _elliptic_negation(text: str, mentions: list[Mention], found: list[Slot]) -> list[Slot]:
    """"X does V and Y does not": Y gets X's binary slots, flipped."""
    out: list[Slot] = []
    for m in lexicon.rx("ellipsis").finditer(text):
        who = [x for x in mentions if x.start >= m.start(1) and x.end <= m.end(1) and x.subject]
        if not who:
            continue
        subj = who[0].subject
        for s in found:
            if s.span[1] <= m.start() and s.subject != subj and s.value in lexicon.OPPOSITE:
                out.append(Slot(s.name, lexicon.OPPOSITE[s.value], False, subj, False,
                                (m.start(), m.end())))
    return out


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
        if s.name in ("output", "printed") and not s.negated and s.value != "" and not s.hypothetical:
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


@lexicon.on_load
def _reset() -> None:
    """A new vocabulary invalidates the compiled phrase table."""
    _phrase_table.cache_clear()
    alternation.cache_clear()
