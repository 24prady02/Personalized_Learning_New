"""Lexicon: every word list the reader uses, kept in one file so it can grow.

The graph-traversal classifier never calls a language model. Everything it
"understands" about English comes from the tables below:

* ``PHRASES``      value phrases per slot (e.g. ``cursor -> next_line``).
* ``OPPOSITE``     the value a negated binary slot flips to.
* ``NUMBER_WORDS`` number words -> digits.
* ``NEGATION``     negation tokens (in addition to spaCy's ``neg`` dependency).
* ``LINK_WORDS``   linking words recorded on each answer clause.
* ``CLAUSE_SPLIT`` words an answer sentence is split on.
* ``VERB_RESOLVE`` ambiguous verbs resolved by what the code uses
  ("print" means ``println`` when the code only calls println).
* ``STOP_ALIASES`` concept labels too common in English to use as aliases.
* ``DECISIVE``     code patterns that force the main concept.
* ``HYPOTHETICAL`` markers of predict-a-change / transfer answers (L4).

How to grow it: run ``scripts/run_lp_graph_44.py``, open
``output/lp_graph/unmatched.json`` and add the phrases students actually used
to the right list here, then rerun ``scripts/prepare_kg_parts.py``.
"""

from __future__ import annotations

# slot -> value -> phrases (lower case; '-' is read as a space, contractions
# are expanded before matching, so write "does not compile", not "doesn't").
PHRASES: dict[str, dict[str, list[str]]] = {
    "cursor": {
        "next_line": [
            "new line", "next line", "line break", "moves down", "goes down",
            "enter", "fresh line", "\\n", "newline", "ends the line",
            "terminates the line", "own line", "separate line",
            "separate lines", "different line", "different lines",
            "beginning of the next line", "start of the next line",
            "two lines", "line separator",
        ],
        "same_line": [
            "same line", "stays on the line", "stays on the same line",
            "on the line", "one line", "single line", "next to each other",
            "side by side", "no newline", "without a newline",
            "no new line", "does not end the line", "leaves the cursor",
            "right after", "continues the line",
        ],
    },
    "compile": {
        "compile_error": [
            "will not compile", "does not compile", "would not compile",
            "cannot compile", "can not compile", "not compile",
            "compile error", "compiler error", "compile time error",
            "compilation error", "error", "compiler complains",
            "not initialized", "not been initialized", "uninitialized",
            "not initialised", "uninitialised", "might not have been initialized",
            "compiler rejects", "rejects", "fails to compile", "syntax error",
            "will not run", "does not run", "can not run", "cannot run",
        ],
        "compiles": [
            "compiles", "compiles fine", "compiles correctly",
            "compiles successfully", "no error", "no errors", "is valid",
            "is legal", "runs fine", "works fine",
        ],
    },
    "crash": {
        "run_error": [
            "run time error", "runtime error", "exception", "crashes",
            "crash", "throws", "stops the program", "terminates with",
            "arithmeticexception", "arrayindexoutofboundsexception",
            "out of bounds", "divide by zero error",
        ],
        "no_error": ["does not crash", "no exception", "will not crash"],
    },
    "error_time": {
        "compile": [
            "compile error", "compile time error", "compile time",
            "found by javac", "before the program runs", "compiler error",
            "at compile time", "compilation error",
        ],
        "run": [
            "run time error", "runtime error", "while it runs",
            "at run time", "at runtime", "while the program runs",
            "during execution",
        ],
    },
    "value": {
        "none": [
            "no value", "has no value", "no defined value", "undefined",
            "not assigned", "unassigned", "has nothing", "no initial value",
            "empty", "not defined", "nothing stored", "is not set",
        ],
        "default": [
            "default value", "default values", "by default", "automatically",
            "on their own", "on its own", "auto initialized",
            "auto initialised", "initialized automatically",
            "set automatically", "starts at zero", "starts at 0",
            "starts as 0", "starts as zero", "default of 0", "defaults to",
        ],
        "garbage": ["garbage", "random value", "junk value", "leftover value"],
    },
    "division": {
        "drops_fraction": [
            "drops the fractional part", "drops the fraction",
            "discards the fractional part", "fractional part is discarded",
            "drops the decimal", "throws away the decimal",
            "cuts off the decimal", "integer division", "whole number result",
            "rounds down", "truncates the decimal", "chops off the decimal",
            "drops the remainder",
        ],
        "keeps_fraction": [
            "keeps the fractional part", "keeps the fraction",
            "keeps the decimal", "decimal result", "gives a decimal",
            "floating point division", "exact division",
        ],
    },
    "holds": {
        "integer": [
            "holds an integer", "holds a whole number", "whole number",
            "whole numbers", "an integer",
        ],
        "fraction": [
            "number with a fractional part", "decimal number", "real number",
            "decimal numbers", "real numbers", "floating point number",
        ],
        "boolean": ["true or false", "true and false", "only true or false"],
        "character": [
            "one character", "a single character", "single character",
            "character code",
        ],
        "text": ["sequence of characters", "a string of characters"],
    },
    "loop_exit": {
        "whole_loop": [
            "ends the whole loop", "exits the loop", "leaves the loop",
            "stops the loop", "ends the loop", "breaks out", "jumps out",
            "out of the loop",
        ],
        "current_pass": [
            "ends only the current pass", "skips to the next iteration",
            "next iteration", "skips the rest", "current pass",
            "current iteration", "goes back to the top",
        ],
    },
    "repeats": {
        "once": ["at most once", "tests its condition once", "only once", "runs once"],
        "repeatedly": [
            "again after every pass", "repeats", "repeatedly", "keeps going",
            "over and over", "each pass", "every pass",
        ],
    },
    "runs": {
        "endless": [
            "forever", "infinite loop", "never stops", "never ends",
            "endless", "infinitely", "does not stop", "does not end",
            "goes on forever", "runs forever",
        ],
    },
    "op": {
        "stores": ["stores the value", "stores", "puts the value", "assigns"],
        "compares": [
            "tests whether", "compares", "checks if", "checks whether",
            "tests if", "test for equality", "are equal",
        ],
    },
    "rounding": {
        "truncate": ["truncates toward zero", "truncates", "chops off", "cuts off"],
        "nearest": ["rounds to the nearest", "nearest integer", "rounds"],
    },
    "plus": {
        "concat": [
            "concatenates", "concatenation", "joins", "sticks together",
            "glues", "appends the text", "joined together",
        ],
        "add": ["adds them as numbers", "numeric addition", "arithmetic addition"],
    },
    "array_ref": {
        "same_array": [
            "same array", "second name", "alias", "aliases",
            "points to the same", "refer to the same", "refers to the same",
            "same reference",
        ],
        "copy": [
            "new array", "separate array", "independent copy",
            "second array", "copy of the array", "copies the elements",
        ],
    },
    "printed": {
        "reference": [
            "memory address", "hash code", "hashcode", "address of the array",
            "weird string", "reference value",
        ],
        "contents": [
            "prints the contents", "prints the elements", "prints the values",
            "prints each element", "prints all the elements",
        ],
    },
}

# Value a negated binary slot flips to ("does not move to the next line"
# -> same_line). Values not listed keep their value and carry negated=True.
OPPOSITE: dict[str, str] = {
    "next_line": "same_line", "same_line": "next_line",
    "compile_error": "compiles", "compiles": "compile_error",
    "run_error": "no_error", "no_error": "run_error",
    "default": "none",
    "drops_fraction": "keeps_fraction", "keeps_fraction": "drops_fraction",
    "whole_loop": "current_pass", "current_pass": "whole_loop",
    "once": "repeatedly", "repeatedly": "once",
    "same_array": "copy", "copy": "same_array",
    "reference": "contents", "contents": "reference",
    "concat": "add", "add": "concat",
    "compile": "run", "run": "compile",
}

NUMBER_WORDS: dict[str, str] = {
    "zero": "0", "one": "1", "two": "2", "three": "3", "four": "4",
    "five": "5", "six": "6", "seven": "7", "eight": "8", "nine": "9",
    "ten": "10", "eleven": "11", "twelve": "12", "thirteen": "13",
    "fourteen": "14", "fifteen": "15", "sixteen": "16", "seventeen": "17",
    "eighteen": "18", "nineteen": "19", "twenty": "20", "thirty": "30",
    "forty": "40", "fifty": "50", "hundred": "100",
}

NEGATION: tuple[str, ...] = (
    "not", "no", "never", "cannot", "nothing", "without", "neither", "nor",
)

# Words after which a slot phrase is not negated even if a negation word
# precedes them in the window (e.g. "not only ... but").
NEGATION_BREAKERS: tuple[str, ...] = ("but", "only", "so", "because", "and", "then")

LINK_WORDS: tuple[str, ...] = (
    "because", "so", "therefore", "thus", "since", "but", "whereas",
    "while", "then", "if", "when", "unless", "although", "however",
    "instead", "hence",
)

# Clause boundaries inside a sentence (the word itself starts the new clause).
CLAUSE_SPLIT: tuple[str, ...] = ("so", "because", "but", "then", "whereas")

# Contractions expanded before any matching.
CONTRACTIONS: dict[str, str] = {
    "won't": "will not", "can't": "cannot", "n't": " not",
    "it's": "it is", "that's": "that is", "there's": "there is",
    "'s": " is", "'ll": " will", "'d": " would", "'re": " are",
}

# An alias that names several concepts; the code decides which one is meant.
# alias -> candidate concepts in preference order (first one used when the
# code shows none of them).
VERB_RESOLVE: dict[str, list[str]] = {
    "print": ["print", "println", "formatted_output"],
    "prints": ["print", "println", "formatted_output"],
    "printed": ["print", "println", "formatted_output"],
    "printing": ["print", "println", "formatted_output"],
    "output": ["println", "print", "formatted_output"],
    "outputs": ["println", "print", "formatted_output"],
    "display": ["println", "print", "formatted_output"],
    "displays": ["println", "print", "formatted_output"],
    "shows": ["println", "print", "formatted_output"],
}

# Concept labels that are ordinary English words: not used as automatic
# aliases (their hand-written cue words in cues.py still apply).
STOP_ALIASES: frozenset[str] = frozenset({
    "run", "filter", "block", "statement", "expression", "api", "testing",
    "animation", "shuffle", "parsing", "debugging", "literal", "comment",
    "identifier", "variable", "program state", "flowchart", "indexing",
    "teleportation", "normalization", "piping", "redirection",
    "data structure", "compile", "assignment", "declaration",
})

# Code patterns (found by execution.static_checks) that decide the main
# concept on their own. pattern name -> concept id.
DECISIVE: dict[str, str] = {
    "uninitialized_read": "definite_assignment",
    "array_printed": "printing_array_reference",
    "int_division": "integer_division",
}

HYPOTHETICAL: tuple[str, ...] = (
    "if", "would", "instead", "change", "changed", "replace", "replaced",
    "fix", "fixed", "otherwise", "could", "were",
)

# Question type rules: first rule whose words appear wins (order matters).
QUESTION_TYPES: list[tuple[str, tuple[str, ...]]] = [
    ("fix", ("fix", "wrong", "error", "bug", "correct the", "mistake")),
    ("why", ("why",)),
    ("explain", ("explain", "describe", "difference", "what happens", "how does")),
    ("output", ("print", "output", "value", "display", "result", "show")),
]

PRONOUNS: tuple[str, ...] = ("it", "its", "this", "that", "the variable", "this variable")
