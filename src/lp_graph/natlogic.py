"""Natural-logic comparison of a statement with edge logic (no model, no code run).

A light version of natural logic (MacCartney & Manning): the two texts are
compared word by word, with each word's polarity (inside the scope of
"no / not" or not) and the lexical relation between words from WordNet:

* the same word or a WordNet synonym, same polarity -> agreement;
* the same word, opposite polarity ("depend" / "do not depend") -> conflict;
* a WordNet antonym ("same" / "different"), same polarity -> conflict;
* a WordNet antonym under opposite polarity ("not the same" / "different")
  -> agreement.

Each match is weighted by the word's rarity in the graph (edgelogic IDF).

``side(statement, wrong, right)`` decides which side of a misconception edge
the statement expresses: the statement must be about the edge (TF-IDF score
at least the reader's threshold); then the side with the larger net
agreement wins if it leads by at least ``LEAD`` (one rare word) or the other
side is in conflict with the statement. Otherwise None (undecided).
"""

from __future__ import annotations

import re
from functools import lru_cache
from typing import TYPE_CHECKING, Iterable

from . import lexicon

if TYPE_CHECKING:  # pragma: no cover
    from .edgelogic import EdgeLogicReader

LEAD = 2.0     # net agreement lead needed without any conflict (about one rare word)
_WORD = re.compile(r"[A-Za-z_][A-Za-z_0-9]*|\d+(?:\.\d+)?|<=|>=|==|!=|[%<>/*+\-=]")


@lru_cache(maxsize=20000)
def _relations(word: str) -> tuple[frozenset[str], frozenset[str]]:
    """(synonyms, antonyms) of a word from WordNet (lower case lemma names)."""
    try:
        from nltk.corpus import wordnet as wn
    except Exception:  # pragma: no cover - optional dependency
        return frozenset(), frozenset()
    syn, ant = set(), set()
    for s in wn.synsets(word):
        for lem in s.lemmas():
            syn.add(lem.name().lower().replace("_", " "))
            for a in lem.antonyms():
                ant.add(a.name().lower().replace("_", " "))
        for sim in s.similar_tos():
            for lem in sim.lemmas():
                for a in lem.antonyms():
                    ant.add(a.name().lower())
    return frozenset(syn), frozenset(ant)


def _words(text: str, variables: Iterable[str]) -> list[tuple[str, str, bool]]:
    """(surface word, stem, negated) for the content words of a text."""
    vars_ = {v.lower() for v in variables}
    out, negated = [], 0
    for raw in _WORD.findall(text or ""):
        w = raw.lower()
        if w in lexicon.NEGATION:
            negated = 3
            continue
        if w in lexicon.STOPWORDS:
            continue
        stem = "VAR" if (w in vars_ or (len(w) == 1 and w.isalpha() and raw.islower())) else w
        if stem != "VAR" and stem.isalpha():
            for suf in lexicon.SUFFIXES:
                if len(stem) > len(suf) + 3 and stem.endswith(suf):
                    stem = stem[: -len(suf)]
                    break
            if len(stem) > 4 and stem.endswith("e"):
                stem = stem[:-1]
        out.append((w, stem, negated > 0))
        if negated and w.isalpha():
            negated -= 1
    return out


def compare(r: "EdgeLogicReader", statement: str, text: str,
            variables: Iterable[str] = ()) -> tuple[float, float]:
    """(agreement, conflict) between a statement and a graph text."""
    a, b = _words(statement, variables), _words(text, ())
    agree = conflict = 0.0
    used: set[int] = set()
    for w, stem, neg in a:
        syn, ant = _relations(w) if w.isalpha() and len(w) > 2 else (frozenset(), frozenset())
        for k, (w2, stem2, neg2) in enumerate(b):
            if k in used:
                continue
            same = stem == stem2 or (w2 in syn and len(w2) > 2)
            opposite = w2 in ant
            if not (same or opposite):
                continue
            used.add(k)
            weight = r.weight(stem2 if stem2 != "VAR" else "VAR")
            if (same and neg == neg2) or (opposite and neg != neg2):
                agree += weight
            else:
                conflict += weight
            break
    return agree, conflict


def side(r: "EdgeLogicReader", statement: str, wrong: str, right: str,
         variables: Iterable[str] = ()) -> str | None:
    """"wrong" | "right" | None: which side of a misconception edge the
    statement expresses, by natural-logic agreement and conflict."""
    if max(r.score(statement, wrong, variables), r.score(statement, right, variables)) < r.match:
        return None
    aw, cw = compare(r, statement, wrong, variables)
    ar, cr = compare(r, statement, right, variables)
    nw, nr = aw - cw, ar - cr
    if nw > nr and (nw - nr >= LEAD or (cr > 0 and cw == 0)) and nw > 0:
        return "wrong"
    if nr > nw and (nr - nw >= LEAD or (cw > 0 and cr == 0)) and nr > 0:
        return "right"
    return None
