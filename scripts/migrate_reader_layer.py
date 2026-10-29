"""One-time migration: move every topic table out of src/lp_graph into the graph.

Reads the tables that were written in code (cues.py, lexicon.py and the
concept / pattern constants of statements.py, reader.py, execution.py,
parts.py, levels.py) and writes them into data/chapter1_kg.json:

* ``concepts[i].reader``: aliases, code patterns (and whether they read the
  raw text), command patterns, operator symbols, Java types, generic /
  declaration flags, the concept a print-like pattern yields to, structural
  signals (regexes or named program analyses, decisive or not, and the rule
  slot code with that signal acts out), and the run outcome it stands for;
* ``misconceptions_and_errors[i].misread_as``: the generic transform its
  misinterpreter applies to code, with parameters;
* top-level ``reader``: the slot vocabulary (values, opposites, phrases,
  kinds), the English language patterns, evidence classes per rule type,
  the level each evidence class supports, and named roles.

After this runs, the engine (src/lp_graph) reads all of it from the graph and
the code tables are deleted. Run once; rerunning on a migrated graph is a
no-op (it refuses).

    python scripts/migrate_reader_layer.py
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
KG_PATH = ROOT / "data" / "chapter1_kg.json"

# Structural signals: what a single code-cue regex cannot see. Written here
# once as graph data (regexes over the masked program, or named analyses the
# engine implements for Java). ``at`` names the group whose position gives the
# statement; ``states`` is the rule slot the code acts out.
SIGNALS = {
    "definite_assignment": [{"name": "uninitialized_read", "analysis": "uninitialized_read", "decisive": True}],
    "printing_array_reference": [{"name": "array_printed", "analysis": "array_printed", "decisive": True}],
    "integer_division": [{"name": "int_division", "analysis": "int_division", "decisive": True}],
    "variable_swap": [{"name": "swap", "scope": "program", "decisive": True,
                       "regex": r"(?:\b\w+\s+)?(?P<t>\b\w+)\s*=\s*(?P<a>\w+)\s*;\s*(?P=a)\s*=\s*(?P<b>\w+)\s*;\s*(?P=b)\s*=\s*(?P=t)\s*;"}],
    "switch_statement": [{"name": "switch_fallthrough", "scope": "program", "decisive": True,
                          "regex": r"\bcase\b[^:]*:\s*(?:(?!\bbreak\b)[^;{}:])+;\s*(?P<at>case\b|default\b)"}],
    "do_while_loop": [{"name": "do_while", "scope": "program", "decisive": True, "regex": r"(?P<at>\bdo)\s*\{"}],
    "nested_loops": [{"name": "nested_for", "scope": "program", "decisive": True,
                      "regex": r"\b(?:for|while)\s*\([^)]*\)\s*\{(?:[^{}]|\{[^{}]*\})*?(?P<at>\bfor\s*\()"}],
    "nested_conditionals": [{"name": "nested_if", "scope": "program", "decisive": True,
                             "regex": r"(?:\bif\s*\([^)]*\)|\belse)\s*\{(?:[^{}]|\{[^{}]*\})*?(?P<at>\bif\s*\()"}],
    "formatted_output": [{"name": "printf_width", "scope": "statement", "text": "raw", "decisive": True,
                          "regex": r"printf\s*\(\s*\"[^\"]*(?:%-?\d+(?:\.\d+)?[dfse]|%\.\d+f)"}],
    "remainder_operator": [{"name": "remainder_expr", "scope": "statement", "decisive": True,
                            "regex": r"(?<![=!<>+\-*/%])=(?!=)[^;]*[\w)\]]\s*%\s*[\w(]"}],
    "indexing": [{"name": "index_from_length", "scope": "statement", "decisive": True,
                  "regex": r"(\w+)\s*\[\s*\1\s*\.\s*length\s*-\s*\d+\s*\]"}],
    "off_by_one_error": [{"name": "loop_past_end", "scope": "statement", "decisive": True,
                          "regex": r"\bfor\s*\([^;]*;\s*\w+\s*<=\s*\w+\s*\.\s*length\b",
                          "states": ["loop_bound", "same_bound"]}],
    "array_copy": [{"name": "copy_loop", "scope": "statement", "decisive": True,
                    "regex": r"\b(\w+)\s*\[\s*(\w+)\s*\]\s*=\s*(?!\1\b)(\w+)\s*\[\s*\2\s*\]\s*;?\s*$"}],
    "naming_convention": [{"name": "bad_name", "analysis": "identifier_style", "decisive": True,
                           "states": ["name_style", "upper_first"]}],
    "compile_time_error": [{"name": "missing_semicolon", "compiler_message": r"';' expected", "decisive": True}],
    "class_declaration": [{"name": "file_name_mismatch", "compiler_message": r"should be declared in a file named",
                           "decisive": True}],
}
# misinterpreter transforms the engine provides for Java, chosen per misconception
TRANSFORMS_BY_SLOT = {
    ("value", "default"): {"transform": "auto_initialize"},
    ("division", "keeps_fraction"): {"transform": "real_division"},
    ("op_meaning", "subtraction"): {"transform": "replace_operator", "args": {"old": "%", "new": "-"}},
    ("op_meaning", "quotient"): {"transform": "replace_operator", "args": {"old": "%", "new": "/"}},
    ("case_end", "stops"): {"transform": "remove_fallthrough"},
    ("loop_bound", "same_bound"): {"transform": "flip_loop_bounds"},
    ("loop_bound", "includes_end"): {"transform": "flip_loop_bounds"},
    ("inner_loop", "skips_rest"): {"transform": "skip_after_empty_inner_loop"},
    ("var_holds", "expression"): {"transform": "reads_follow_source"},
    ("cursor", "next_line"): {"transform": "replace_text", "args": {"find": r"System\.out\.print\s*\(",
                                                                     "replace": "System.out.println("}},
}
TRANSFORMS_BY_NAME = {
    "LocalVariablesAutoInitialized": {"transform": "auto_initialize"},
    "PrintEqualsPrintln": TRANSFORMS_BY_SLOT[("cursor", "next_line")],
    "IntegerDivisionGivesFraction": {"transform": "real_division"},
}
# what a run outcome or a code element stands for
OUTCOMES = {"compile_time_error": "compile_error", "run_time_error": "run_error", "infinite_loop": "timeout",
            "comment": "comment", "compile": "compiling", "run": "running"}
ROLES = {"command_arguments": "command_line_args"}
RAW_TEXT = ("string_literal", "string_concatenation", "char", "escape_sequences")
YIELDS = {"print": "println"}   # print's pattern also matches println( : yield to it on the same statement
COMMANDS = [(r"\s>\s*\S+", "redirection"), (r"\s<\s*\S+", "redirection"), (r"\s<\s*\S+", "standard_input"),
            (r"\|\s*java\b", "piping"), (r"^java\s+\w+\s+\S", "command_line_args"), (r"^java\b", "run"),
            (r"^javac\b", "compile")]
OPERATORS = {"%": "remainder_operator", "/": "integer_division", "*": "arithmetic_operators",
             "+": "arithmetic_operators", "-": "arithmetic_operators", ">=": "comparison_operators",
             "<=": "comparison_operators", ">": "comparison_operators", "<": "comparison_operators",
             "==": "comparison_operators", "!=": "comparison_operators"}
TYPES = {"int": "int", "double": "double", "boolean": "boolean", "char": "char", "long": "long_type",
         "String": "string_type", "float": "double"}
DECLARATION = ("declaration", "variable", "int", "double", "boolean", "char", "long_type", "string_type",
               "array_declaration")


def language(lexicon, slots, statements, reader, execution) -> dict:
    nw = "|".join(sorted(lexicon.NUMBER_WORDS, key=lambda s: (-len(s), s)))
    return {
        "number_words": lexicon.NUMBER_WORDS, "negation": list(lexicon.NEGATION),
        "negation_breakers": list(lexicon.NEGATION_BREAKERS), "link_words": list(lexicon.LINK_WORDS),
        "clause_split": list(lexicon.CLAUSE_SPLIT), "contractions": lexicon.CONTRACTIONS,
        "ambiguous_aliases": lexicon.VERB_RESOLVE, "stop_aliases": sorted(lexicon.STOP_ALIASES),
        "hypothetical_words": list(lexicon.HYPOTHETICAL), "hypothetical_clause": list(lexicon.HYPOTHETICAL_CLAUSE),
        "correction": list(lexicon.CORRECTION), "question_types": [[k, list(v)] for k, v in lexicon.QUESTION_TYPES],
        "pronouns": list(lexicon.PRONOUNS), "value_verbs": list(lexicon.VALUE_VERBS),
        "change_verbs": sorted(lexicon.CHANGE_VERBS), "output_nouns": sorted(statements._OUTPUT_NOUNS),
        "not_a_variable": sorted(slots._NOT_A_VARIABLE),
        # regex templates: {VAL} {SEQ} {TOK} {END} {NUM} {OPS} {VALUE_VERBS} {NUMBER_WORDS} {VAR}
        "patterns": {
            "punct_break": slots._PUNCT_BREAK.pattern,
            "subclause": slots._SUBCLAUSE.pattern,
            "val": r"(-?\d+(?:\.\d+)?|\"[^\"]*\"|'[^']*'|true|false|null|nothing|{NUMBER_WORDS})",
            "end": slots._END,
            "tok": slots._TOK,
            "seq": "{TOK}" + r"(?:(?:\s*[,/|]\s*|\s+)" + "{TOK}" + r")*,?",
            "num": slots._NUM,
            "ops": slots._OPS,
            "prints": slots._PRINTS_RE.pattern.replace(slots._SEQ, "{SEQ}").replace(slots._END, "{END}"),
            "whole": slots._WHOLE_RE.pattern.replace(slots._SEQ, "{SEQ}").replace(slots._END, "{END}"),
            "prints_nothing": r"\b(?:prints?|printed|outputs?|displays?) nothing\b",
            "expr": slots._EXPR_RE.pattern.replace(slots._NUM, "{NUM}").replace(slots._OPS, "{OPS}").replace(slots._END, "{END}"),
            "value": r"\b([a-z][a-z0-9]*|it)\s+({VALUE_VERBS})\s+(?:the value |a value of |equal to |still )?{VAL}{END}",
            "var_value": slots._VAR_VALUE_RE.pattern.replace(slots._VALUE_VERB, "{VALUE_VERBS}"),
            "first_index": slots._FIRST_INDEX_RE.pattern,
            "both": slots._BOTH_RE.pattern,
            "runs": r"\b(?:runs|loops|repeats|executes|iterates|goes)\s+(?:around\s+)?(\d+|{NUMBER_WORDS})\s+times\b",
            "ellipsis": slots._ELLIPSIS_RE.pattern,
            "turn": statements._TURN_RE.pattern,
            "answer_parts": statements._PARTS_RE.pattern,
            "change_loop_kind": statements._CHANGE_RES[0][0].pattern,
            "change_start": statements._CHANGE_RES[1][0].pattern,
            "change_start_bound": statements._CHANGE_RES[2][0].pattern,
            "change_for_value": statements._CHANGE_RES[3][0].pattern,
            "change_format": statements._CHANGE_RES[4][0].pattern,
            "change_repair": statements._CHANGE_RES[5][0].pattern,
            "change_cast": statements._CHANGE_RES[6][0].pattern,
            "after_fix": r"\bafter that\b",
            "all_same": statements._ALL_SAME.pattern,
            "list_values": statements._LIST.pattern,
            "mid_trace": statements._MID_TRACE.pattern,
            "bare_sequence": statements._BARE_SEQ.pattern,
            "asked_name": r"\bnamed\s+([A-Za-z_]\w*)",
            "given_value": r"\b{VAR}\s*(?:=|is|equals)\s*-?\d",
            "same_result": reader._SAME_RE.pattern,
            "differ": reader._DIFFER_RE.pattern,
            "writing_task": execution._WRITING_RE.pattern,
            "already_exists": execution._EXISTS_RE.pattern,
            "question_value": execution._Q_VALUE_RE.pattern,
            "saved_as": r"saved as\s+(\w+)\.java",
            "run_as": r"run as:?\s+java\s+(\w+)((?:[ \t]+[^\s,;]+)*)",
            "reads_input": r"StdIn\.|System\.in|new\s+Scanner",
            "multiple_choice_or_multipart": statements._PARTS_RE.pattern,
            "edge_logic_split": r";|\s+(?=(?:while|whereas|but)\s)|(?<=[.!?])\s+(?=[A-Z0-9(\"'])",
            "edge_logic_split_word": r"^(?:while|whereas|but)\s+",
        },
        "flags": {"turn": "im", "change_loop_kind": "i", "change_start": "i", "change_start_bound": "i",
                  "change_for_value": "i", "change_format": "i", "change_repair": "i", "writing_task": "i",
                  "already_exists": "i", "saved_as": "i", "run_as": "i"},
    }


def main() -> int:
    import lp_graph.cues as cues
    import lp_graph.execution as execution
    import lp_graph.lexicon as lexicon
    import lp_graph.levels as levels
    import lp_graph.parts as parts
    import lp_graph.reader as reader
    import lp_graph.slots as slots
    import lp_graph.statements as statements

    kg = json.load(open(KG_PATH, encoding="utf-8"))
    if "reader" in kg:
        print("graph already holds the reader layer; nothing to do")
        return 1
    ids = {c["id"] for c in kg["concepts"]}
    for c in kg["concepts"]:
        cid = c["id"]
        cue = cues.CUES.get(cid, {})
        r = {"aliases": list(cue.get("words", [])),
             "code_patterns": list(cue.get("code", [])),
             "code_text": "raw" if cid in RAW_TEXT else "masked",
             "command_patterns": [rx for rx, cc in COMMANDS if cc == cid],
             "operator_symbols": sorted(op for op, cc in OPERATORS.items() if cc == cid),
             "java_types": sorted(t for t, cc in TYPES.items() if cc == cid),
             "generic": cid in lexicon.GENERIC,
             "shown_by_declaration": cid in DECLARATION,
             "signals": SIGNALS.get(cid, [])}
        if cid in YIELDS:
            r["yields_to"] = YIELDS[cid]
        if cid in OUTCOMES:
            r["outcome"] = OUTCOMES[cid]
        c["reader"] = r
    assert set(SIGNALS) <= ids and set(OUTCOMES) <= ids, "a signal or outcome names an unknown concept"
    # misinterpreters: per misconception node, from its derived slot or its name
    part_slots = json.load(open(ROOT / "data" / "kg_parts.json", encoding="utf-8"))["misconceptions"]
    by_mis: dict[str, dict] = {}
    for info in part_slots.values():
        spec = info.get("slot")
        if spec and (spec["slot"], spec["wrong_value"]) in TRANSFORMS_BY_SLOT:
            by_mis.setdefault(info["mis"], TRANSFORMS_BY_SLOT[(spec["slot"], spec["wrong_value"])])
    by_mis.update(TRANSFORMS_BY_NAME)
    n_mis = 0
    for m in kg["misconceptions_and_errors"]:
        if m["id"] in by_mis:
            m["misread_as"] = [by_mis[m["id"]]]
            n_mis += 1
    slot_kind = {}
    for s in lexicon.PHRASES:
        slot_kind[s] = ("rule" if s in lexicon.RULE_SLOTS else
                        "outcome" if s in parts.OUTCOME_SLOTS else "phrase")
    for s in parts.EXAMPLE_SLOTS:
        slot_kind.setdefault(s, "example")
    kg["reader"] = {
        "about": "Everything the reader knows about this chapter and about English. The engine "
                 "(src/lp_graph) has no topic tables; it reads this section and the reader fields "
                 "of concepts and misconceptions.",
        "slots": {s: {"kind": slot_kind[s],
                      "values": {v: {"phrases": list(ph), **({"opposite": lexicon.OPPOSITE[v]}
                                                            if v in lexicon.OPPOSITE else {})}
                                 for v, ph in lexicon.PHRASES.get(s, {}).items()}}
                  for s in sorted(slot_kind)},
        "rule_values": sorted(parts.RULE_VALUES),
        "language": language(lexicon, slots, statements, reader, execution),
        "evidence_classes": parts.EVIDENCE_CLASS,
        "level_of_class": levels._CLASS_LEVEL,
        "roles": ROLES,
    }
    kg["version"] = kg["version"].split(" ")[0] + "-reader1 (v3.9.5 + reader layer: every topic table of the "\
        "classifier moved from code into the graph)"
    tmp = KG_PATH.with_suffix(".tmp")
    tmp.write_text(json.dumps(kg, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")
    tmp.replace(KG_PATH)
    n_sig = sum(len(v) for v in SIGNALS.values())
    print(f"concepts with a reader field: {len(kg['concepts'])}; signals: {n_sig}; "
          f"misconceptions with a misinterpreter: {n_mis}; slots: {len(slot_kind)}; "
          f"language patterns: {len(kg['reader']['language']['patterns'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
