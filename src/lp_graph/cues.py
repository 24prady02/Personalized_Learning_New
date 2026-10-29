"""Cues: word aliases and code regexes per concept, read from the graph.

Each concept's ``reader`` field in the graph holds ``aliases`` (English words
a student may use for it) and ``code_patterns`` (regexes run on one Java
statement; strings and comments are blanked first unless its ``code_text``
is ``raw``). ``load_cues()`` returns them in the shape the rest of the
package uses: ``{concept: {"words": [...], "code": [...]}}``.

Every concept also gets its id / label as an alias automatically (see
``graph.KG.aliases``) unless the label is a stop alias of the graph's
language section.
"""

from __future__ import annotations

from . import lexicon


def load_cues() -> dict[str, dict[str, list[str]]]:
    """Aliases and code patterns of every concept (copies, so callers cannot
    change the loaded vocabulary)."""
    return {cid: {"words": list(lexicon.ALIASES.get(cid, [])), "code": list(lexicon.CODE_PATTERNS.get(cid, []))}
            for cid in sorted(set(lexicon.ALIASES) | set(lexicon.CODE_PATTERNS))}
