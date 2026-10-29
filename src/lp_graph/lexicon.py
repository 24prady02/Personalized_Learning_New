"""Lexicon: the reader's vocabulary, read from the knowledge graph.

The classifier holds no topic tables of its own. Everything it knows about
the chapter and about English comes from the graph file:

* the top-level ``reader`` section: slot families (values, opposites,
  phrases, kinds), English word lists and regex templates, the evidence class
  of each rule type, the level each evidence class supports, named roles;
* each concept's ``reader`` field: aliases, code / command patterns,
  operator symbols, Java types, generic / declaration flags, structural
  signals (decisive code patterns and the rule slot code acts out), the run
  outcome it stands for;
* each misconception's ``misread_as``: the code transform of its
  misinterpreter.

``load(raw)`` fills the module names below from a parsed graph (done for the
default graph at import, and again by ``graph.KG`` for any other file), then
calls the hooks other modules registered with ``on_load`` (to rebuild their
compiled patterns). ``rx(name)`` compiles one language pattern, with the
placeholders {VAL} {SEQ} {TOK} {END} {NUM} {OPS} {VALUE_VERBS}
{NUMBER_WORDS} filled in.

To grow the reader, edit the graph (scripts/prepare_kg_parts.py rebuilds the
derived data), never this file.
"""

from __future__ import annotations

import json
import re
from typing import Callable

from .knowledge import DEFAULT_KG_PATH

_HOOKS: list[Callable[[], None]] = []
_RX: dict[tuple[str, str], re.Pattern] = {}
_TEMPLATES: dict[str, str] = {}
_FLAGS: dict[str, str] = {}

# filled by load()
PHRASES: dict[str, dict[str, list[str]]] = {}
OPPOSITE: dict[str, str] = {}
SLOT_KIND: dict[str, str] = {}
RULE_SLOTS: frozenset[str] = frozenset()
OUTCOME_SLOTS: frozenset[str] = frozenset()
EXAMPLE_SLOTS: frozenset[str] = frozenset()
RULE_VALUES: frozenset[str] = frozenset()
NUMBER_WORDS: dict[str, str] = {}
NEGATION: tuple[str, ...] = ()
NEGATION_BREAKERS: tuple[str, ...] = ()
LINK_WORDS: tuple[str, ...] = ()
CLAUSE_SPLIT: tuple[str, ...] = ()
CONTRACTIONS: dict[str, str] = {}
VERB_RESOLVE: dict[str, list[str]] = {}
STOP_ALIASES: frozenset[str] = frozenset()
HYPOTHETICAL: tuple[str, ...] = ()
HYPOTHETICAL_CLAUSE: tuple[str, ...] = ()
CORRECTION: tuple[str, ...] = ()
QUESTION_TYPES: list[tuple[str, tuple[str, ...]]] = []
PRONOUNS: tuple[str, ...] = ()
VALUE_VERBS: tuple[str, ...] = ()
CHANGE_VERBS: frozenset[str] = frozenset()
OUTPUT_NOUNS: frozenset[str] = frozenset()
NOT_A_VARIABLE: frozenset[str] = frozenset()
STOPWORDS: frozenset[str] = frozenset()
SUFFIXES: tuple[str, ...] = ()
GENERIC: frozenset[str] = frozenset()
DECL_CONCEPTS: frozenset[str] = frozenset()
TYPE_CONCEPT: dict[str, str] = {}
OP_CONCEPT: dict[str, str] = {}
COMMAND_PATTERNS: list[tuple[str, str]] = []
CODE_PATTERNS: dict[str, list[str]] = {}
CODE_TEXT: dict[str, str] = {}
ALIASES: dict[str, list[str]] = {}
YIELDS: dict[str, str] = {}
OUTCOME: dict[str, str] = {}
SIGNALS: list[tuple[str, dict]] = []
DECISIVE: dict[str, str] = {}
FINDING_SLOTS: dict[str, tuple[str, str]] = {}
MISREAD: dict[str, list[dict]] = {}
EVIDENCE_CLASS: dict[str, str] = {}
CLASS_LEVEL: dict[str, str] = {}
ROLES: dict[str, str] = {}


def on_load(fn: Callable[[], None]) -> Callable[[], None]:
    """Register a function to rerun whenever a graph's vocabulary is loaded."""
    _HOOKS.append(fn)
    return fn


def load(raw: dict) -> None:
    """Fill the vocabulary from a parsed graph."""
    g = globals()
    reader = raw.get("reader") or {}
    lang = reader.get("language") or {}
    slots = reader.get("slots") or {}
    g["PHRASES"] = {s: {v: list(spec.get("phrases", [])) for v, spec in info.get("values", {}).items()}
                    for s, info in slots.items() if info.get("values")}
    g["OPPOSITE"] = {v: spec["opposite"] for info in slots.values()
                     for v, spec in info.get("values", {}).items() if "opposite" in spec}
    g["SLOT_KIND"] = {s: info.get("kind", "phrase") for s, info in slots.items()}
    g["RULE_SLOTS"] = frozenset(s for s, k in SLOT_KIND.items() if k == "rule")
    g["OUTCOME_SLOTS"] = frozenset(s for s, k in SLOT_KIND.items() if k == "outcome")
    g["EXAMPLE_SLOTS"] = frozenset(s for s, k in SLOT_KIND.items() if k == "example")
    g["RULE_VALUES"] = frozenset(reader.get("rule_values", []))
    g["NUMBER_WORDS"] = dict(lang.get("number_words", {}))
    for name, key in (("NEGATION", "negation"), ("NEGATION_BREAKERS", "negation_breakers"),
                      ("LINK_WORDS", "link_words"), ("CLAUSE_SPLIT", "clause_split"),
                      ("HYPOTHETICAL", "hypothetical_words"), ("HYPOTHETICAL_CLAUSE", "hypothetical_clause"),
                      ("CORRECTION", "correction"), ("PRONOUNS", "pronouns"), ("VALUE_VERBS", "value_verbs")):
        g[name] = tuple(lang.get(key, []))
    g["CONTRACTIONS"] = dict(lang.get("contractions", {}))
    g["VERB_RESOLVE"] = {k: list(v) for k, v in lang.get("ambiguous_aliases", {}).items()}
    g["STOP_ALIASES"] = frozenset(lang.get("stop_aliases", []))
    g["QUESTION_TYPES"] = [(k, tuple(v)) for k, v in lang.get("question_types", [])]
    g["CHANGE_VERBS"] = frozenset(lang.get("change_verbs", []))
    g["OUTPUT_NOUNS"] = frozenset(lang.get("output_nouns", []))
    g["NOT_A_VARIABLE"] = frozenset(lang.get("not_a_variable", []))
    g["STOPWORDS"] = frozenset(lang.get("stopwords", []))
    g["SUFFIXES"] = tuple(lang.get("suffixes", []))
    _TEMPLATES.clear()
    _TEMPLATES.update(lang.get("patterns", {}))
    _FLAGS.clear()
    _FLAGS.update(lang.get("flags", {}))
    _RX.clear()
    concepts = [c for c in raw.get("concepts", []) if c.get("id")]
    rd = {c["id"]: c.get("reader") or {} for c in concepts}
    g["GENERIC"] = frozenset(c for c, r in rd.items() if r.get("generic"))
    g["DECL_CONCEPTS"] = frozenset(c for c, r in rd.items() if r.get("shown_by_declaration"))
    g["TYPE_CONCEPT"] = {t: c for c, r in sorted(rd.items()) for t in r.get("java_types", [])}
    g["OP_CONCEPT"] = {op: c for c, r in sorted(rd.items()) for op in r.get("operator_symbols", [])}
    g["COMMAND_PATTERNS"] = [(p, c) for c, r in sorted(rd.items()) for p in r.get("command_patterns", [])]
    g["CODE_PATTERNS"] = {c: list(r.get("code_patterns", [])) for c, r in rd.items()}
    g["CODE_TEXT"] = {c: r.get("code_text", "masked") for c, r in rd.items()}
    g["ALIASES"] = {c: list(r.get("aliases", [])) for c, r in rd.items()}
    g["YIELDS"] = {c: r["yields_to"] for c, r in rd.items() if r.get("yields_to")}
    g["OUTCOME"] = {r["outcome"]: c for c, r in sorted(rd.items()) if r.get("outcome")}
    g["SIGNALS"] = [(c, dict(s)) for c, r in sorted(rd.items()) for s in r.get("signals", [])]
    g["DECISIVE"] = {s["name"]: c for c, s in SIGNALS if s.get("decisive")}
    g["FINDING_SLOTS"] = {s["name"]: tuple(s["states"]) for _, s in SIGNALS if s.get("states")}
    g["MISREAD"] = {m["id"]: list(m["misread_as"]) for m in raw.get("misconceptions_and_errors", [])
                    if m.get("id") and m.get("misread_as")}
    g["EVIDENCE_CLASS"] = dict(reader.get("evidence_classes", {}))
    g["CLASS_LEVEL"] = dict(reader.get("level_of_class", {}))
    g["ROLES"] = dict(reader.get("roles", {}))
    for fn in _HOOKS:
        fn()


def _fill(text: str) -> str:
    """Replace the known {NAME} placeholders (regex braces such as {1,12} stay)."""
    alts = {
        "NUMBER_WORDS": "|".join(re.escape(w) for w in sorted(NUMBER_WORDS, key=lambda s: (-len(s), s))),
        "VALUE_VERBS": "|".join(re.escape(v) for v in sorted(VALUE_VERBS, key=lambda s: (-len(s), s))),
    }
    out = text
    for n in ("VAL", "SEQ", "TOK", "END", "NUM", "OPS", "NUMBER_WORDS", "VALUE_VERBS"):
        token = "{" + n + "}"
        if token in out:
            out = out.replace(token, alts[n] if n in alts else _fill(_TEMPLATES.get(n.lower(), "")))
    return out


def template(name: str, **values: str) -> str:
    """A language pattern as text, with placeholders (and any given {VAR}) filled."""
    out = _fill(_TEMPLATES[name])
    for k, v in values.items():
        out = out.replace("{" + k + "}", v)
    return out


def rx(name: str, **values: str) -> re.Pattern:
    """A compiled language pattern from the graph (cached)."""
    key = (name, json.dumps(values, sort_keys=True))
    if key not in _RX:
        flags = 0
        for ch in _FLAGS.get(name, ""):
            flags |= {"i": re.I, "m": re.M, "s": re.S}[ch]
        _RX[key] = re.compile(template(name, **values), flags)
    return _RX[key]


def load_path(path) -> None:
    with open(path, encoding="utf-8") as fh:
        load(json.load(fh))


load_path(DEFAULT_KG_PATH)
