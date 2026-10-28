"""Cues: word aliases and code regexes per concept.

Stand-in for ``lp_percpt.cues.CUES`` (same shape: ``CUES[cid] = {"words":
[...], "code": [...]}``). When this package is merged into the repo that has
``src/lp_percpt/``, ``load_cues()`` prefers the real table and only fills
gaps from the one below.

* ``words`` are English aliases a student may use for the concept.
* ``code`` are regexes run on one Java statement (strings and comments are
  blanked first, see ``execution.mask_literals``).

Every concept also gets its id/label as an alias automatically (see
``graph.KG.aliases``) unless the label is in ``lexicon.STOP_ALIASES``.
"""

from __future__ import annotations

_TYPES = r"(?:int|double|boolean|char|long|String|float|short|byte)"

CUES: dict[str, dict[str, list[str]]] = {
    "declaration": {
        "words": ["declared", "declare", "declares", "declaring", "declaration",
                  "declarations", "declared as", "creates a variable", "creates the variable"],
        "code": [rf"^\s*(?:final\s+)?{_TYPES}(?:\[\])*\s+[A-Za-z_]\w*\s*(?:[=;,\[])"],
    },
    "variable": {
        "words": ["variable", "variables", "local variable", "local variables"],
        "code": [rf"^\s*(?:final\s+)?{_TYPES}(?:\[\])*\s+[A-Za-z_]\w*"],
    },
    "assignment": {
        "words": ["assigned", "assign", "assigns", "assignment", "set to",
                  "is set", "stored in", "store", "stores"],
        "code": [r"(?<![=!<>+\-*/%&|^])=(?!=)"],
    },
    "definite_assignment": {
        "words": ["definite assignment", "definitely assigned", "initialized",
                  "initialised", "initialize", "initialise", "initialization",
                  "uninitialized", "uninitialised", "not initialized",
                  "might not have been initialized", "assigned before"],
        "code": [],
    },
    "int": {
        "words": ["int", "integer", "integers", "ints"],
        "code": [r"\bint\b"],
    },
    "double": {
        "words": ["double", "doubles", "floating point", "decimal"],
        "code": [r"\bdouble\b", r"\b\d+\.\d*\b|\b\d*\.\d+\b"],
    },
    "boolean": {
        "words": ["boolean", "booleans", "true or false"],
        "code": [r"\bboolean\b", r"\btrue\b|\bfalse\b"],
    },
    "char": {
        "words": ["char", "character", "chars"],
        "code": [r"\bchar\b", r"'(?:\\.|[^'\\])'"],
    },
    "long_type": {"words": ["long"], "code": [r"\blong\b"]},
    "string_type": {
        "words": ["string", "strings"],
        "code": [r"\bString\b"],
    },
    "string_literal": {
        "words": ["string literal", "quotes", "quotation marks", "in quotes"],
        "code": [r"\"(?:\\.|[^\"\\])*\""],
    },
    "string_concatenation": {
        "words": ["concatenation", "concatenate", "concatenates", "joins", "glue"],
        "code": [r"\"(?:\\.|[^\"\\])*\"\s*\+|\+\s*\"(?:\\.|[^\"\\])*\""],
    },
    "println": {
        "words": ["println", "print line", "system.out.println", "printline"],
        "code": [r"System\.out\.println\s*\(", r"StdOut\.println\s*\("],
    },
    "print": {
        "words": ["print", "system.out.print"],
        "code": [r"System\.out\.print\s*\(", r"StdOut\.print\s*\("],
    },
    "formatted_output": {
        "words": ["printf", "format", "formatted", "format specifier"],
        "code": [r"\.printf\s*\(", r"String\.format\s*\("],
    },
    "standard_output": {
        "words": ["standard output", "stdout", "console", "the screen", "terminal"],
        "code": [r"System\.out\.", r"StdOut\."],
    },
    "standard_input": {
        "words": ["standard input", "stdin", "input stream", "reads input"],
        "code": [r"StdIn\.", r"new\s+Scanner\s*\(", r"System\.in"],
    },
    "standard_drawing": {"words": ["stddraw", "standard drawing", "draws"], "code": [r"StdDraw\."]},
    "standard_audio": {"words": ["stdaudio", "standard audio"], "code": [r"StdAudio\."]},
    "command_line_args": {
        "words": ["command line argument", "command line arguments", "args"],
        "code": [r"\bargs\s*\["],
    },
    "args_length": {"words": ["args.length"], "code": [r"\bargs\.length\b"]},
    "parsing": {
        "words": ["parseint", "parsedouble", "parse", "parses"],
        "code": [r"Integer\.parseInt\s*\(", r"Double\.parseDouble\s*\(", r"Boolean\.parseBoolean\s*\("],
    },
    "arithmetic_operators": {
        "words": ["arithmetic", "plus", "minus", "multiplied", "multiply", "subtracts"],
        "code": [r"[A-Za-z_0-9)\]]\s*[+\-*/%]\s*[A-Za-z_0-9(]"],
    },
    "integer_division": {
        "words": ["integer division", "int division", "divided", "division", "divide", "divides"],
        "code": [],
    },
    "remainder_operator": {
        "words": ["remainder", "modulo", "mod", "modulus"],
        "code": [r"[A-Za-z_0-9)\]]\s*%\s*[A-Za-z_0-9(]"],
    },
    "division_by_zero": {
        "words": ["division by zero", "divide by zero", "divided by zero", "by zero"],
        "code": [r"/\s*0(?![.\d])", r"%\s*0(?![.\d])"],
    },
    "increment_operators": {
        "words": ["increment", "increments", "decrement", "plus plus", "++"],
        "code": [r"\+\+|--"],
    },
    "compound_assignment": {
        "words": ["compound assignment", "+=", "plus equals"],
        "code": [r"[+\-*/%]="],
    },
    "explicit_cast": {
        "words": ["cast", "casting", "casts", "type cast"],
        "code": [rf"\(\s*{_TYPES}\s*\)\s*[A-Za-z_0-9(]"],
    },
    "widening_conversion": {"words": ["widening", "promotion", "promoted"], "code": []},
    "type_conversion": {"words": ["type conversion", "converted", "converts", "conversion"], "code": []},
    "math_library": {"words": ["math library", "math."], "code": [r"\bMath\.\w+"]},
    "math_random": {"words": ["math.random", "random number", "random"], "code": [r"Math\.random\s*\("]},
    "math_round": {"words": ["math.round", "round", "rounds", "rounding"], "code": [r"Math\.round\s*\("]},
    "trig_functions": {"words": ["sine", "cosine", "math.sin", "math.cos"], "code": [r"Math\.(?:sin|cos|tan|atan2?|asin|acos)\s*\("]},
    "comparison_operators": {
        "words": ["comparison", "compares", "less than", "greater than", "equal to", "=="],
        "code": [r"[<>]=?|==|!="],
    },
    "logical_operators": {
        "words": ["and operator", "or operator", "logical", "&&", "||"],
        "code": [r"&&|\|\||!(?!=)"],
    },
    "boolean_expression": {"words": ["boolean expression", "condition", "conditions"], "code": []},
    "short_circuit": {"words": ["short circuit", "short-circuit"], "code": [r"&&|\|\|"]},
    "conditional_operator": {"words": ["ternary", "conditional operator"], "code": [r"\?[^:]*:"]},
    "if_statement": {
        "words": ["if statement", "if condition"],
        "code": [r"^\s*if\s*\("],
    },
    "if_else_statement": {"words": ["else", "if else", "else branch"], "code": [r"^\s*}?\s*else\b"]},
    "else_if_chain": {"words": ["else if"], "code": [r"\belse\s+if\b"]},
    "nested_conditionals": {"words": ["nested if"], "code": []},
    "switch_statement": {"words": ["switch", "switch statement"], "code": [r"^\s*switch\s*\(", r"^\s*case\b"]},
    "while_loop": {
        "words": ["while loop", "while condition"],
        "code": [r"^\s*while\s*\("],
    },
    "do_while_loop": {"words": ["do while", "do-while"], "code": [r"^\s*do\b"]},
    "for_loop": {
        "words": ["for loop", "for loops"],
        "code": [r"^\s*for\s*\("],
    },
    "enhanced_for": {"words": ["for each", "enhanced for"], "code": [r"^\s*for\s*\([^;]*:[^;]*\)"]},
    "loop_body": {"words": ["loop body", "body of the loop", "inside the loop"], "code": []},
    "loop_variable": {"words": ["loop variable", "index variable"], "code": []},
    "loop_guard": {"words": ["loop condition", "guard", "loop test"], "code": []},
    "infinite_loop": {"words": ["infinite loop", "forever", "never stops", "never ends", "endless"], "code": [r"while\s*\(\s*true\s*\)", r"for\s*\(\s*;\s*;\s*\)"]},
    "break_statement": {"words": ["break"], "code": [r"^\s*break\s*;"]},
    "continue_statement": {"words": ["continue"], "code": [r"^\s*continue\s*;"]},
    "labeled_break": {"words": ["labeled break", "labelled break"], "code": [r"^\s*break\s+\w+\s*;"]},
    "nested_loops": {"words": ["nested loop", "nested loops", "inner loop", "outer loop"], "code": []},
    "off_by_one_error": {"words": ["off by one", "one too many", "one too few"], "code": []},
    "counter_pattern": {"words": ["counter", "counter variable"], "code": []},
    "accumulator_pattern": {"words": ["accumulator", "running sum", "running total"], "code": []},
    "array_declaration": {"words": ["array declaration"], "code": [rf"{_TYPES}\s*\[\]\s*\w+"]},
    "array_creation": {"words": ["new array", "creates an array", "array creation"], "code": [rf"\bnew\s+{_TYPES}\s*\["]},
    "array_initializer": {"words": ["array initializer", "curly braces"], "code": [r"=\s*\{"]},
    "array_default_values": {
        "words": ["array default", "array defaults", "array element", "array elements",
                  "default value", "default values", "defaults to zero"],
        "code": [],
    },
    "indexing": {"words": ["index", "indices", "indexing"], "code": [r"\w\s*\[[^\]]+\]"]},
    "length_field": {"words": ["length", ".length"], "code": [r"\.length\b(?!\s*\()"]},
    "array_bounds": {"words": ["out of bounds", "bounds", "arrayindexoutofboundsexception"], "code": []},
    "array_reference": {"words": ["reference", "references", "array variable"], "code": []},
    "array_aliasing": {"words": ["alias", "aliasing", "same array"], "code": []},
    "printing_array_reference": {"words": ["memory address", "hash code", "address"], "code": []},
    "two_dimensional_array": {"words": ["2d array", "two dimensional", "matrix", "row", "column"], "code": [r"\[\s*\]\s*\[\s*\]", r"\w\s*\[[^\]]+\]\s*\[[^\]]+\]"]},
    "main_method": {"words": ["main method", "main function"], "code": [r"static\s+void\s+main\s*\("]},
    "class_declaration": {"words": ["class"], "code": [r"^\s*(?:public\s+)?class\s+\w+"]},
    "compile_time_error": {"words": ["compile error", "compile time error", "compile-time error", "compiler error", "syntax error"], "code": []},
    "run_time_error": {"words": ["runtime error", "run time error", "run-time error", "exception", "crash", "crashes"], "code": []},
    "logical_error": {"words": ["logic error", "logical error", "wrong output", "bug"], "code": []},
    "escape_sequences": {"words": ["escape sequence", "backslash", "\\n", "\\t"], "code": [r"\\[ntb\"'\\]"]},
    "operator_precedence": {"words": ["precedence", "order of operations"], "code": []},
    "overflow": {"words": ["overflow", "overflows", "wraps around"], "code": [r"Integer\.MAX_VALUE|Integer\.MIN_VALUE"]},
    "floating_point_precision": {"words": ["precision", "rounding error", "0.30000000000000004"], "code": []},
    "named_constants": {"words": ["constant", "final"], "code": [r"\bfinal\b"]},
    "method_call": {"words": ["method call", "calls a method"], "code": [r"\b(?!out\b)[a-z]\w*\.[a-z]\w*\s*\("]},
    "side_effect_order": {"words": ["side effect"], "code": []},
    "chained_assignment": {"words": ["chained assignment"], "code": [r"\w+\s*=\s*\w+\s*=(?!=)"]},
    "variable_swap": {"words": ["swap", "swaps", "exchange"], "code": []},
    "program_trace": {"words": ["trace", "tracing", "step by step"], "code": []},
    "scientific_notation": {"words": ["scientific notation", "e notation"], "code": [r"\d[eE][+\-]?\d"]},
    "integer_constants": {"words": ["max_value", "min_value"], "code": [r"Integer\.(?:MAX|MIN)_VALUE"]},
    "char_arithmetic": {"words": ["char arithmetic", "unicode", "ascii"], "code": []},
    "block": {"words": ["block", "curly braces", "braces"], "code": [r"\{"]},
    "statement": {"words": ["statement", "statements", "semicolon"], "code": []},
    "expression": {"words": ["expression", "expressions"], "code": []},
    "literal": {"words": ["literal", "literals"], "code": []},
    "identifier": {"words": ["identifier", "name of the variable", "variable name"], "code": []},
    "data_type": {"words": ["data type", "data types"], "code": []},
    "primitive_type": {"words": ["primitive", "primitive type", "primitives"], "code": []},
    "compile": {"words": ["compile", "compiles", "compiler", "compiling", "javac"], "code": []},
    "run": {"words": ["execute", "executes", "execution", "java command"], "code": []},
    "comment": {"words": ["comment", "comments"], "code": []},
}


def load_cues() -> dict[str, dict[str, list[str]]]:
    """Return the cue table, preferring ``lp_percpt.cues.CUES`` when present.

    Concepts missing from the real table (or the whole table when
    ``lp_percpt`` is absent) come from ``CUES`` above. Lists are copied so
    callers cannot mutate the module tables.
    """
    merged = {cid: {"words": list(v["words"]), "code": list(v["code"])}
              for cid, v in CUES.items()}
    try:  # pragma: no cover - only in the full repo
        from lp_percpt.cues import CUES as REAL  # type: ignore
    except Exception:
        return merged
    for cid, v in REAL.items():
        entry = merged.setdefault(cid, {"words": [], "code": []})
        for key in ("words", "code"):
            for item in v.get(key, []):
                if item not in entry[key]:
                    entry[key].append(item)
    return merged
