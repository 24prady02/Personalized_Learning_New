"""Execution: split Java code into statements and run it for real.

Stand-in for ``lp_percpt.execution`` (``parse``, ``Tracer.trace``,
``MUTATIONS``):

* ``classify_code(code)`` tells Java from shell commands, prose that only
  describes a run, and writing tasks ("an int array data2 already exists");
  writing tasks give context declarations.
* ``parse(code)`` splits a snippet into simple statements, headers and
  comments, and records per statement what it declares, assigns and reads.
  Array initialisers ``{4, 7, 1}`` stay inside their statement; a line that
  lacks its ``;`` is split off and reported (``missing_semicolon``).
* ``static_checks(stmts)`` finds code patterns without running anything:
  definite assignment, integer division, and the structural patterns of
  ``lexicon.DECISIVE`` (swap, switch fall-through, do-while, nested loops
  and ifs, printf widths, ``%`` expressions, ``a[a.length - k]``, loops past
  the end, copy loops, naming).
* ``Tracer(code).trace()`` compiles the snippet wrapped in ``class Main``
  (a full class is compiled as written, under the file name its comment
  gives) with ``javac`` and runs it with ``java``. Variables the snippet uses
  without declaring get the values the question states, else fixed sample
  values. It records the output, every compile error, the run error and the
  value of each variable after each top-level statement. Without a JDK the
  run is ``available=False`` and only the static checks apply.
* Misinterpreters are generic rewrite operators (replace an operator, flip a
  loop bound, insert ``break``, auto-initialise, re-evaluate an assignment
  later, ...). ``operator_for(spec)`` maps a misconception's slot (from
  ``kg_parts.json``) to its operator, so a new misconception with a
  recognised slot gets a misinterpreter without new code.
* ``Tracer.trace_variant(change)`` runs the program with a stated change
  (start value, loop kind, format specifier, errors fixed);
  ``Tracer.trace_answer(code)`` runs code the student wrote.

All runs are cached per program text so repeated assessments are cheap and
identical.
"""

from __future__ import annotations

import re
import shutil
import subprocess
import tempfile
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path
from typing import Callable

from . import lexicon

_TYPES = ("int", "double", "boolean", "char", "long", "String", "float", "short", "byte")
_DEFAULTS = {"int": "0", "double": "0.0", "boolean": "false", "char": "'\\u0000'",
             "long": "0L", "String": "null", "float": "0.0f", "short": "0", "byte": "0"}
_KEYWORDS = frozenset({
    "int", "double", "boolean", "char", "long", "String", "float", "short", "byte",
    "if", "else", "for", "while", "do", "return", "new", "true", "false", "null",
    "System", "println", "print", "printf", "Math", "public", "static",
    "void", "class", "final", "break", "continue", "switch", "case", "default",
    "args", "main", "length", "StdOut", "StdIn", "StdDraw", "Integer", "Double",
})
_SAMPLE_INTS = ("3", "5", "7", "11", "13", "17")
_SAMPLE_ARRAYS = {"int": "{4, 7, 1}", "double": "{1.5, 2.5, 3.5, 4.5}", "char": "{'a', 'b', 'c'}",
                  "String": "{\"x\", \"y\", \"z\"}", "boolean": "{true, false, true}"}
_SAMPLE_SCALARS = {"int": "0", "double": "0.0", "char": "'a'", "String": "\"abc\"", "boolean": "false",
                   "long": "0L"}
RUN_TIMEOUT_S = 5
COMPILE_TIMEOUT_S = 60


@dataclass(frozen=True)
class CodeStmt:
    """One simple statement, header or comment of the snippet."""

    index: int
    text: str
    line: int
    depth: int
    kind: str  # decl | assign | print | header | close | comment | other
    declares: tuple[tuple[str, str, bool], ...] = ()  # (type, name, has_init)
    assigns: tuple[str, ...] = ()
    reads: tuple[str, ...] = ()
    printed: str | None = None  # argument text of print/println
    span: tuple[int, int] = field(default=(0, 0), compare=False)


@dataclass(frozen=True)
class Run:
    """Result of compiling and running one program text."""

    available: bool
    compiled: bool = False
    output: str = ""
    error: str = ""          # first compile or run error message
    error_kind: str = ""     # compile | run | timeout | ""
    values: tuple[tuple[str, str], ...] = ()  # final values of top-level variables
    timed_out: bool = False
    errors: tuple[str, ...] = ()               # every compile error
    snapshots: tuple[tuple[int, str, str], ...] = ()  # (statement index, name, value)

    def value_of(self, name: str) -> str | None:
        for k, v in self.values:
            if k == name:
                return v
        return None

    def value_after(self, name: str, index: int) -> str | None:
        """Value of ``name`` right after statement ``index`` (latest snapshot <= index)."""
        best = None
        for i, k, v in self.snapshots:
            if k == name and i <= index:
                best = v
        return best

    def initial(self, name: str) -> str | None:
        for _, k, v in self.snapshots:
            if k == name:
                return v
        return None


@dataclass(frozen=True)
class StaticFinding:
    """A code pattern found without running (see ``lexicon.DECISIVE``)."""

    pattern: str
    stmt_index: int
    variable: str
    message: str


@dataclass(frozen=True)
class CodeKind:
    """What the code field holds."""

    kind: str                         # java | commands | prose | writing | empty
    java: str = ""                    # Java text to parse and run
    context: tuple[str, ...] = ()     # context declarations (writing tasks)
    commands: tuple[str, ...] = ()    # shell command lines
    prose: str = ""                   # a description of a run


@dataclass
class Trace:
    """The real run plus the misinterpreter runs."""

    run: Run
    findings: tuple[StaticFinding, ...] = ()
    mutants: dict[str, Run] = field(default_factory=dict)
    program: str = ""
    assumed: dict[str, str] = field(default_factory=dict)      # free variable -> value used
    indistinguishable: frozenset[str] = frozenset()             # mutants giving the real result
    answer_run: Run | None = None
    answer_findings: tuple[StaticFinding, ...] = ()
    answer_mutants: dict[str, Run] = field(default_factory=dict)
    variants: dict[str, Run] = field(default_factory=dict)       # change key -> run
    stmts: tuple[CodeStmt, ...] = ()
    sampled: frozenset[str] = frozenset()    # free variables read with an invented value
    reads_input: bool = False                # the program reads standard input


# ------------------------------------------------------------------ the field



def classify_code(code: str) -> CodeKind:
    """Java, shell commands, a prose description, a writing task, or nothing."""
    text = (code or "").strip()
    if not text:
        return CodeKind("empty")
    if lexicon.rx("writing_task").search(text):
        ctx = []
        for m in lexicon.rx("already_exists").finditer(text):
            typ, what, name = m.group(1), (m.group(2) or "").lower(), m.group(3)
            typ = "String" if typ.lower() == "string" else typ.lower()
            if what == "array":
                ctx.append(f"{typ}[] {name} = {_SAMPLE_ARRAYS.get(typ, '{}')};")
            else:
                ctx.append(f"{typ} {name} = {_SAMPLE_SCALARS.get(typ, '0')};")
        return CodeKind("writing", context=tuple(ctx), prose=text)
    lines = [ln for ln in text.splitlines() if ln.strip()]
    cmd = [ln for ln in lines if re.match(r"\s*[%$]\s+\S", ln)]
    if cmd and len(cmd) * 2 >= len(lines):
        rest = " ".join(ln.strip() for ln in lines if ln not in cmd)
        return CodeKind("commands", commands=tuple(re.sub(r"^\s*[%$]\s*", "", c) for c in cmd), prose=rest)
    masked = mask_literals(text)
    if ";" not in masked and "{" not in masked:
        return CodeKind("prose", prose=text)
    return CodeKind("java", java=text)


# ------------------------------------------------------------------ parsing

def mask_literals(text: str) -> str:
    """Blank out string/char literal contents and comments (same length)."""
    out, i, n = [], 0, len(text)
    while i < n:
        ch = text[i]
        if text.startswith("//", i):
            j = text.find("\n", i)
            j = n if j < 0 else j
            out.append(" " * (j - i))
            i = j
        elif text.startswith("/*", i):
            j = text.find("*/", i + 2)
            j = n if j < 0 else j + 2
            out.append(re.sub(r"[^\n]", " ", text[i:j]))
            i = j
        elif ch in "\"'":
            j = i + 1
            while j < n and text[j] != ch and text[j] != "\n":
                j += 2 if text[j] == "\\" else 1
            j = min(j + 1, n)
            out.append(ch + " " * max(0, j - i - 2) + (ch if j - i >= 2 else ""))
            i = j
        else:
            out.append(ch)
            i += 1
    return "".join(out)


def program_text(code: str, prelude: tuple[str, ...] = ()) -> str:
    """The snippet as a compilable Main program (classes kept as written).
    ``prelude`` lines (context / free-variable declarations) go first in main."""
    if re.search(r"\bclass\s+\w+", mask_literals(code)):
        return code
    if re.search(r"static\s+void\s+main\s*\(", code):
        return "public class Main {\n" + code + "\n}\n"
    lines = list(prelude) + code.splitlines()
    body = "\n".join("        " + ln for ln in lines)
    return ("public class Main {\n    public static void main(String[] args) {\n"
            + body + "\n    }\n}\n")


def _body(code: str) -> str:
    """The statements inside main (or the snippet itself)."""
    m = re.search(r"static\s+void\s+main\s*\([^)]*\)\s*\{", code)
    if not m:
        return code
    depth, i = 1, m.end()
    masked = mask_literals(code)
    while i < len(code) and depth:
        depth += {"{": 1, "}": -1}.get(masked[i], 0)
        i += 1
    return code[m.end():i - 1]


_HEADER_START = re.compile(r"\s*(?:\}\s*)?(?:else\b|if\b|for\b|while\b|do\b|switch\b|case\b|default\b|try\b|"
                           r"catch\b|finally\b|public\b|private\b|static\b|class\b|\{|\})")


def _missing_semicolons(body: str, masked: str) -> list[int]:
    """Offsets (line ends) where a statement line lacks its ``;``."""
    out = []
    lines = masked.split("\n")
    pos = 0
    ends = []
    for ln in lines:
        ends.append((pos, pos + len(ln), ln))
        pos += len(ln) + 1
    for k, (s, e, ln) in enumerate(ends):
        t = ln.strip()
        if not t or _HEADER_START.match(ln) or t[-1] in ";{}(,+-*/=&|:?<>!":
            continue
        nxt = next((x for x in ends[k + 1:] if x[2].strip() or body[x[0]:x[1]].strip()), None)
        if nxt is None:
            continue
        raw_next = body[nxt[0]:nxt[1]].strip()
        if re.match(r"[A-Za-z_}/]", raw_next) and not re.match(r"[.+\-*/&|?:]", nxt[2].strip() or "x"):
            out.append(s + len(ln.rstrip()))
    return out


def parse(code: str) -> list[CodeStmt]:
    """Split a snippet (or the body of main) into statements, headers and
    comments.

    Spans are offsets into ``_body(code)`` so instrumentation can insert
    text without rebuilding the program.
    """
    body = _body(code)
    masked = mask_literals(body)
    stmts: list[CodeStmt] = []
    state = {"start": 0, "depth": 0}
    cuts = set(_missing_semicolons(body, masked))

    def flush(end: int, hint: str = "") -> None:
        s0 = state["start"]
        raw = body[s0:end]
        text = raw.strip()
        state["start"] = end
        if not text or not masked[s0:end].strip():
            return
        lead = s0 + (len(raw) - len(raw.lstrip()))
        m = re.match(r"else\b\s*(?!if\b)(?=\S)", text)
        if m and hint != "header":  # "else x = 1;" -> header "else" + statement
            _add(stmts, body, lead, lead + 4, state["depth"], "header")
            lead = lead + m.end()
            text = body[lead:end].strip()
        _add(stmts, body, lead, lead + len(text), state["depth"], hint)

    paren = 0
    i, n = 0, len(masked)
    while i < n:
        ch = masked[i]
        if i in cuts and paren == 0:
            flush(i, "")
        if ch == "(":
            paren += 1
        elif ch == ")":
            paren -= 1
            if paren == 0 and re.match(r"\s*(?:\}\s*)?(?:else\s+)?(?:if|for|while|switch)\b",
                                       masked[state["start"]:i]):
                nxt = re.match(r"\s*(\S)", masked[i + 1:])
                if nxt and nxt.group(1) not in "{;":
                    flush(i + 1, "header")  # header without braces
        elif ch == ";" and paren == 0:
            flush(i + 1)
        elif ch == "{" and paren == 0:
            before = masked[state["start"]:i]
            if re.search(r"(?:=|\bnew\s+\w+\s*(?:\[\s*\]\s*)+)\s*$", before):
                j, d = i, 0  # array initialiser: stays in the statement
                while j < n:
                    d += {"{": 1, "}": -1}.get(masked[j], 0)
                    if d == 0:
                        break
                    j += 1
                i = j + 1
                continue
            flush(i, "header")
            state["depth"] += 1
            state["start"] = i + 1
        elif ch == "}" and paren == 0:
            flush(i)
            state["depth"] = max(0, state["depth"] - 1)
            _add(stmts, body, i, i + 1, state["depth"], "close")
            state["start"] = i + 1
        elif ch == ":" and paren == 0 and re.match(r"\s*(?:case\b[^:]*|default\s*)$", masked[state["start"]:i]):
            flush(i + 1, "header")  # "case 1:" is a header of what follows
        i += 1
    flush(len(body))
    for m in re.finditer(r"//[^\n]*", body):
        if masked[m.start():m.start() + 2] == "  " and body[m.start():m.start() + 2] == "//":
            line = body.count("\n", 0, m.start()) + 1
            depth = next((s.depth for s in reversed(stmts) if s.span[0] <= m.start()), 0)
            stmts.append(CodeStmt(0, m.group(0).strip(), line, depth, "comment", span=(m.start(), m.end())))
    stmts.sort(key=lambda s: s.span[0])
    out = []
    for k, s in enumerate(stmts):
        out.append(CodeStmt(k, s.text, s.line, s.depth, s.kind, s.declares, s.assigns, s.reads,
                            s.printed, s.span))
    return out


def _add(stmts: list[CodeStmt], body: str, start: int, end: int, depth: int, hint: str) -> None:
    text = body[start:end].strip()
    line = body.count("\n", 0, start) + 1
    if hint == "close":
        stmts.append(CodeStmt(len(stmts), "}", line, depth, "close", span=(start, end)))
        return
    st = _make_stmt(len(stmts), text, line, depth, hint)
    stmts.append(CodeStmt(**{**st.__dict__, "span": (start, end)}))


_DECL_RE = re.compile(r"^(?:final\s+)?(" + "|".join(_TYPES) + r")(\s*\[\s*\])*\s+(.+)$", re.S)
_ID_RE = re.compile(r"\b([A-Za-z_]\w*)\b")


def _make_stmt(index: int, text: str, line: int, depth: int, hint: str) -> CodeStmt:
    masked = mask_literals(text).rstrip(";").strip()
    masked = re.sub(r"^(?:case\b[^:]*|default\s*):\s*", "", masked)  # a statement after a case label
    declares: list[tuple[str, str, bool]] = []
    assigns: list[str] = []
    reads: list[str] = []
    printed = None
    kind = hint or "other"
    rhs_parts: list[str] = []
    m = _DECL_RE.match(masked)
    if m and hint != "header":
        kind = "decl"
        typ = m.group(1) + ("[]" if m.group(2) else "")
        for part in _split_top(m.group(3), ","):
            name, _, init = part.partition("=")
            name = name.strip().split("[")[0].strip()
            if re.fullmatch(r"[A-Za-z_]\w*", name):
                declares.append((typ, name, bool(init.strip())))
                if init.strip():
                    assigns.append(name)
                    rhs_parts.append(init)
    else:
        am = re.match(r"^([A-Za-z_]\w*)\s*(\[[^\]]*\])?\s*([+\-*/%]?=)(?!=)(.*)$", masked, re.S)
        im = re.match(r"^(?:\+\+|--)?\s*([A-Za-z_]\w*)\s*(?:\+\+|--)?$", masked)
        if am and kind != "header":
            kind = "assign"
            assigns.append(am.group(1))
            rhs_parts.append(am.group(4) + (am.group(2) or ""))
            if am.group(3) != "=" or am.group(2):
                reads.append(am.group(1))
        elif im and ("++" in masked or "--" in masked):
            kind = "assign"
            assigns.append(im.group(1))
            reads.append(im.group(1))
        else:
            rhs_parts.append(masked)
    pm = re.search(r"(?:System\.out|StdOut)\.(println|print|printf)\s*\((.*)\)\s*$", text.rstrip(";").strip(), re.S)
    if pm and hint != "header":
        kind = "print"
        printed = pm.group(2).strip()
    for part in rhs_parts:
        for idm in _ID_RE.finditer(part):
            nm = idm.group(1)
            after = part[idm.end():idm.end() + 1]
            before = part[max(0, idm.start() - 1):idm.start()]
            if nm in _KEYWORDS or after == "(" or before == ".":
                continue
            if not nm[0].isdigit() and nm not in reads:
                reads.append(nm)
    return CodeStmt(index, text, line, depth, kind, tuple(declares),
                    tuple(dict.fromkeys(assigns)), tuple(dict.fromkeys(reads)), printed)


def _split_top(text: str, sep: str) -> list[str]:
    parts, depth, cur = [], 0, []
    for ch in text:
        if ch in "([{":
            depth += 1
        elif ch in ")]}":
            depth -= 1
        if ch == sep and depth == 0:
            parts.append("".join(cur))
            cur = []
        else:
            cur.append(ch)
    parts.append("".join(cur))
    return parts


def variables(stmts: list[CodeStmt]) -> dict[str, str]:
    """Declared variable name -> type, in declaration order."""
    out: dict[str, str] = {}
    for s in stmts:
        for typ, name, _ in s.declares:
            out.setdefault(name, typ)
    return out


_HEADER_DECL_RE = re.compile(r"\bfor\s*\(\s*(?:final\s+)?(?:" + "|".join(_TYPES) + r")(?:\s*\[\s*\])*\s+(\w+)")


def free_variables(stmts: list[CodeStmt]) -> list[tuple[str, bool]]:
    """Variables the snippet uses without declaring, in order of first use,
    with whether the first use assigns them (then they need no start value)."""
    declared = set(variables(stmts))
    for s in stmts:
        declared |= set(_HEADER_DECL_RE.findall(mask_literals(s.text)))
    out: dict[str, bool] = {}
    for s in stmts:
        if s.kind in ("comment", "close"):
            continue
        for nm in list(s.reads) + list(s.assigns):
            if nm in declared or nm in out or nm in _KEYWORDS or nm[0].isupper():
                continue
            out[nm] = nm in s.assigns and nm not in s.reads
    return list(out.items())


# ------------------------------------------------------------ static checks

def static_checks(stmts: list[CodeStmt], asked_name: str | None = None,
                  body: str = "") -> list[StaticFinding]:
    """Patterns found without running the code (sorted by statement).

    The patterns come from the graph (``lexicon.SIGNALS``): a regex over one
    statement (``scope: statement``, on the masked or raw text) or over the
    whole masked program (``scope: program``; the group ``at`` locates the
    statement), or a named Java analysis (``ANALYSES``). Compiler-message
    signals are matched after compiling (``Tracer.trace``). ``asked_name`` is
    a variable name the question asks the student to use; ``body`` is the
    program text the statements' spans point into."""
    live = [s for s in stmts if s.kind not in ("comment", "close")]
    found: list[StaticFinding] = []
    for concept, sig in lexicon.SIGNALS:
        name = sig["name"]
        if sig.get("analysis"):
            fn = ANALYSES.get(sig["analysis"])
            if fn:
                found += [StaticFinding(name, i, var, msg) for i, var, msg in fn(stmts, asked_name)]
        elif sig.get("regex") and sig.get("scope") == "program" and body:
            masked = mask_literals(body)
            for m in re.finditer(sig["regex"], masked):
                pos = m.start("at") if "at" in m.re.groupindex else m.start()
                owner = [s for s in live if s.span[0] <= pos]
                if owner:
                    found.append(StaticFinding(name, owner[-1].index, m.groupdict().get("var") or "",
                                               f"{name}: {m.group(0).strip()[:60]}"))
        elif sig.get("regex") and sig.get("scope", "statement") == "statement":
            for s in live:
                text = s.text if sig.get("text") == "raw" else mask_literals(s.text)
                m = re.search(sig["regex"], text)
                if m:
                    var = m.groupdict().get("var") or (s.assigns[0] if s.assigns else "")
                    found.append(StaticFinding(name, s.index, var, f"{name}: {m.group(0).strip()[:60]}"))
    return sorted(set(found), key=lambda f: (f.stmt_index, f.pattern, f.variable))


def _analysis_uninitialized(stmts: list[CodeStmt], asked: str | None) -> list[tuple[int, str, str]]:
    return [(f.stmt_index, f.variable, f.message) for f in _uninitialized_reads(stmts)]


def _analysis_int_division(stmts: list[CodeStmt], asked: str | None) -> list[tuple[int, str, str]]:
    types = variables(stmts)
    return [(s.index, "", "both operands of / are int") for s in stmts
            if s.kind not in ("comment", "close") and "/" in mask_literals(s.text) and _int_division(s, types)]


def _analysis_array_printed(stmts: list[CodeStmt], asked: str | None) -> list[tuple[int, str, str]]:
    types = variables(stmts)
    return [(s.index, s.printed.strip(), "printing an array variable prints its reference") for s in stmts
            if s.kind == "print" and s.printed and types.get(s.printed.strip(), "").endswith("[]")]


def _analysis_identifier_style(stmts: list[CodeStmt], asked: str | None) -> list[tuple[int, str, str]]:
    """Java's lowerCamelCase convention for locals, and the name the question asks for."""
    out = []
    for s in stmts:
        for _, name, _ in s.declares:
            if re.match(r"\s*final\b", s.text):
                continue
            if asked and name != asked and name.lower() == asked.lower():
                out.append((s.index, name, f"{name} differs only in case from the asked name {asked}"))
            elif name[0].isupper():
                out.append((s.index, name, f"{name} starts with a capital letter (lowerCamelCase expected)"))
            elif "_" in name.strip("_") or (name.isupper() and len(name) > 1):
                out.append((s.index, name, f"{name} is not lowerCamelCase"))
    return out


# named Java analyses a graph signal can ask for
ANALYSES: dict[str, Callable[[list[CodeStmt], str | None], list[tuple[int, str, str]]]] = {
    "uninitialized_read": _analysis_uninitialized,
    "int_division": _analysis_int_division,
    "array_printed": _analysis_array_printed,
    "identifier_style": _analysis_identifier_style,
}


def _uninitialized_reads(stmts: list[CodeStmt]) -> list[StaticFinding]:
    """Definite assignment, straight-line approximation.

    A variable declared without initializer is unassigned; an assignment at
    the same or a shallower depth assigns it; an assignment inside a deeper
    block (one branch of an if, a loop body) does not count once the block
    closes. A read while unassigned is a compile error.
    """
    unassigned: dict[str, int] = {}   # name -> depth of declaration
    inner: dict[str, int] = {}        # name -> depth where assigned inside a block
    found: list[StaticFinding] = []
    for s in stmts:
        if s.kind == "comment":
            continue
        if s.kind == "close":
            for nm, d in sorted(inner.items()):
                if d > s.depth:
                    unassigned[nm] = s.depth
                    del inner[nm]
            continue
        for nm in s.reads:
            if nm in unassigned and nm not in inner:
                found.append(StaticFinding(
                    "uninitialized_read", s.index, nm,
                    f"variable {nm} might not have been initialized"))
                del unassigned[nm]
        for typ, nm, has_init in s.declares:
            if not has_init:
                unassigned[nm] = s.depth
        for nm in s.assigns:
            if nm in unassigned:
                if s.depth > unassigned[nm]:
                    inner[nm] = s.depth
                else:
                    del unassigned[nm]
    return found


def _int_division(s: CodeStmt, types: dict[str, str]) -> bool:
    masked = mask_literals(s.text)
    for m in re.finditer(r"([A-Za-z_]\w*(?:\s*\[[^\]]*\])?|\d+(?:\.\d+)?)\s*/\s*([A-Za-z_]\w*|\d+(?:\.\d+)?)",
                         masked):
        a, b = m.group(1), m.group(2)
        a = re.sub(r"\s*\[.*$", "", a)
        if re.search(r"\(\s*(?:double|float)\s*\)\s*$", masked[:m.start()]):
            continue
        if all(_is_int(x, types, elem=True) for x in (a, b)):
            return True
    return False


def _is_int(tok: str, types: dict[str, str], elem: bool = False) -> bool:
    t = types.get(tok, "")
    if elem and t.endswith("[]"):
        t = t[:-2]
    return bool(re.fullmatch(r"\d+", tok)) or t in ("int", "long", "short", "byte")


# -------------------------------------------------------------------- runs

def jdk_available() -> bool:
    return bool(shutil.which("javac") and shutil.which("java"))


def _instrument(program: str) -> str:
    """Copy of ``program`` that prints variable values to stderr after each
    depth-0 statement (``@@<index>:<name>=``) and at the end of main.

    A print is not inserted after a statement that is the body of a header
    without braces (inserting there would change the control flow).
    """
    body = _body(program)
    if body == program:
        return program
    stmts = parse(program)
    types = variables(stmts)
    inserts: list[tuple[int, str]] = []
    assigned_any: set[str] = set()
    for k, s in enumerate(stmts):
        for nm in s.assigns:
            if types.get(nm, "") in _TYPES:
                assigned_any.add(nm)
        if s.depth != 0 or s.kind in ("header", "close", "comment"):
            continue
        prev = next((x for x in reversed(stmts[:k]) if x.kind != "comment"), None)
        if prev and prev.kind == "header" and not body[prev.span[1]:s.span[0]].strip().startswith("{"):
            continue
        names = [nm for nm in types if types[nm] in _TYPES and (nm in assigned_any or
                 any(nm == d[1] and d[2] for d in s.declares))]
        if s.kind == "close":
            continue
        text = "".join(f' System.err.println("@@{s.index}:{nm}=" + {nm});' for nm in names
                       if _declared_before(stmts, nm, k))
        if text and s.text.rstrip().endswith((";", "}")):
            inserts.append((s.span[1], text))
    top = [nm for nm in types if _declared_before(stmts, nm, len(stmts) - 1)]
    final = [f' System.err.println("@@end:{nm}=" + {nm});' for nm in sorted(top)
             if types[nm] in _TYPES and nm in assigned_any]
    final += [f' System.err.println("@@end:{nm}=" + java.util.Arrays.toString({nm}));' for nm in sorted(top)
              if types[nm].endswith("[]") and types[nm][:-2] in _TYPES]
    if final:
        inserts.append((len(body), "".join(final)))
    if not inserts:
        return program
    new_body = body
    for pos, text in sorted(inserts, reverse=True):
        new_body = new_body[:pos] + text + new_body[pos:]
    start = program.find(body)
    return program[:start] + new_body + program[start + len(body):]


def _declared_before(stmts: list[CodeStmt], name: str, k: int) -> bool:
    for s in stmts[:k + 1]:
        if any(d[1] == name and d[2] for d in s.declares) and s.depth == 0:
            return True
    return False


def _file_and_run(program: str) -> tuple[str, str, tuple[str, ...]]:
    """(source file name, class to run, args) from the program and its comments."""
    cls = re.search(r"public\s+class\s+(\w+)", program)
    name = cls.group(1) if cls else "Main"
    saved = lexicon.rx("saved_as").search(program)
    run_as = lexicon.rx("run_as").search(program)
    file_name = saved.group(1) if saved else name
    run_cls = run_as.group(1) if run_as else name
    args = tuple(run_as.group(2).split()) if run_as else ()
    return file_name, run_cls, args


@lru_cache(maxsize=512)
def run_program(program: str, instrument: bool = True) -> Run:
    """Compile and run one program text (cached)."""
    if not jdk_available():
        return Run(available=False)
    if instrument:
        inst = _instrument(program)
        if inst != program:
            r = _compile_and_run(inst)
            if r.compiled or r.error_kind != "compile":
                return r
    return _compile_and_run(program)


def _compile_and_run(program: str) -> Run:
    file_name, run_cls, args = _file_and_run(program)
    with tempfile.TemporaryDirectory(prefix="lp_graph_") as tmp:
        src = Path(tmp) / f"{file_name}.java"
        src.write_text(program, encoding="utf-8")
        try:
            comp = subprocess.run(["javac", "-encoding", "UTF-8", "-nowarn", src.name],
                                  cwd=tmp, capture_output=True, text=True,
                                  timeout=COMPILE_TIMEOUT_S)
        except (OSError, subprocess.TimeoutExpired):
            return Run(available=False)
        if comp.returncode != 0:
            msgs = tuple(m.strip() for m in re.findall(r"error: (.+)", comp.stderr))
            first = msgs[0] if msgs else comp.stderr.strip()[:200]
            return Run(True, False, "", first, "compile", errors=msgs or (first,))
        try:
            res = subprocess.run(["java", "-cp", tmp, run_cls, *args], cwd=tmp, capture_output=True,
                                 text=True, timeout=RUN_TIMEOUT_S, input="")
            out, err, timed_out = res.stdout, res.stderr, False
        except subprocess.TimeoutExpired as exc:
            out = exc.stdout.decode() if isinstance(exc.stdout, bytes) else (exc.stdout or "")
            err = exc.stderr.decode() if isinstance(exc.stderr, bytes) else (exc.stderr or "")
            timed_out = True
    values: dict[str, str] = {}
    snaps: list[tuple[int, str, str]] = []
    other_err: list[str] = []
    for ln in err.splitlines():
        m = re.match(r"@@(\d+|end):(\w+)=(.*)$", ln)
        if m:
            if m.group(1) == "end":
                values[m.group(2)] = m.group(3)
            else:
                snaps.append((int(m.group(1)), m.group(2), m.group(3)))
                values.setdefault(m.group(2), m.group(3))
        elif ln.strip():
            other_err.append(ln.strip())
    for i, k, v in snaps:  # without an end marker (a crash) the last snapshot is final
        if not any(x.startswith("@@end:") for x in err.splitlines()):
            values[k] = v
    exc_line = next((ln for ln in other_err if "Exception" in ln or "Error" in ln), "")
    kind = "timeout" if timed_out else ("run" if exc_line else "")
    return Run(True, True, out.replace("\r\n", "\n"), exc_line, kind,
               tuple(sorted(values.items())), timed_out, (), tuple(snaps))


# ------------------------------------------------- misinterpreter operators

def _auto_initialize(program: str) -> str | None:
    """An uninitialised local gets its default value."""
    changed = False

    def fix(m: re.Match) -> str:
        nonlocal changed
        typ, names = m.group(1), m.group(2)
        parts = []
        for p in _split_top(names, ","):
            if "=" not in p and re.fullmatch(r"\s*[A-Za-z_]\w*\s*", p):
                parts.append(f"{p.strip()} = {_DEFAULTS[typ]}")
                changed = True
            else:
                parts.append(p.strip())
        return f"{typ} {', '.join(parts)};"

    out = re.sub(r"\b(" + "|".join(_TYPES) + r")\s+([A-Za-z_][\w\s,=]*?);", fix, program)
    return out if changed else None


def _print_is_println(program: str) -> str | None:
    """print also ends the line."""
    out = re.sub(r"System\.out\.print\s*\(", "System.out.println(", program)
    return out if out != program else None


def _division_keeps_fraction(program: str) -> str | None:
    """int / int computed as real division (receivers become double)."""
    masked = mask_literals(program)
    out, last, changed = [], 0, False
    for m in re.finditer(r"(?<![\w.])([A-Za-z_]\w*(?:\[[^\]]*\])?|\d+)\s*/\s*([A-Za-z_]\w*|\d+)(?![\w.])", masked):
        out.append(program[last:m.start()])
        out.append(f"(double) {program[m.start(1):m.end(1)]} / {program[m.start(2):m.end(2)]}")
        last, changed = m.end(), True
    out.append(program[last:])
    if not changed:
        return None
    result = "".join(out)
    receivers = {s.assigns[0] for s in parse(program)
                 if s.assigns and "/" in mask_literals(s.text).split("=", 1)[-1]}
    for nm in sorted(receivers):
        result = re.sub(rf"\b(?:int|long)(\s+{re.escape(nm)}\b)", r"double\1", result)
    return result


def _replace_op(old: str, new: str) -> Callable[[str], str | None]:
    """Replace a binary operator between operands (outside strings)."""
    def op(program: str) -> str | None:
        masked = mask_literals(program)
        rx = re.compile(r"(?<=[\w)\]])(\s*)" + re.escape(old) + r"(?!=)(\s*)(?=[\w(])")
        spans = [m.span() for m in rx.finditer(masked)]
        if not spans:
            return None
        out, last = [], 0
        for a, b in spans:
            out.append(program[last:a])
            out.append(program[a:b].replace(old, new))
            last = b
        out.append(program[last:])
        return "".join(out)
    return op


def _flip_bound(program: str) -> str | None:
    """Read < and <= (and > and >=) as the same: flip them in loop conditions."""
    masked = mask_literals(program)
    out, last, changed = [], 0, False
    for m in re.finditer(r"\b(?:for\s*\([^;]*;([^;]*);|while\s*\(([^)]*)\))", masked):
        g = 1 if m.group(1) is not None else 2
        a, b = m.span(g)
        cond = program[a:b]
        new = re.sub(r"<=|>=|<(?!=)|>(?!=)", lambda x: {"<=": "<", ">=": ">", "<": "<=", ">": ">="}[x.group(0)], cond)
        if new != cond:
            out.append(program[last:a])
            out.append(new)
            last, changed = b, True
    out.append(program[last:])
    return "".join(out) if changed else None


def _no_fallthrough(program: str) -> str | None:
    """The switch ends after the matching case: insert break before each label
    that follows statements."""
    lines = program.split("\n")
    out, changed, in_case, has_stmt = [], False, False, False
    for ln in lines:
        t = mask_literals(ln).strip()
        if re.match(r"(?:case\b|default\b)", t):
            if has_stmt:
                out.append(re.match(r"\s*", ln).group(0) + "break;")
                changed = True
            in_case = True
            body = re.sub(r"^(?:case\b[^:]*|default\s*):\s*", "", t)
            has_stmt = bool(body) and not body.startswith("break")
        elif t.startswith("break"):
            has_stmt = False
        elif t.startswith("}"):
            in_case, has_stmt = False, False
        elif t and in_case:
            has_stmt = True
        out.append(ln)
    return "\n".join(out) if changed else None


def _empty_inner_skips_rest(program: str) -> str | None:
    """An inner loop that runs zero times also skips the rest of the outer body:
    guard the statements after the inner loop with its entry condition."""
    stmts = parse(program)
    body = _body(program)
    for k, s in enumerate(stmts):
        m = re.match(r"\s*for\s*\(\s*(?:int\s+)?(\w+)\s*=\s*([^;]+);([^;]+);", mask_literals(s.text))
        if not (s.kind == "header" and m and any(
                x.kind == "header" and re.match(r"\s*(?:for|while)\b", x.text) and x.depth < s.depth
                for x in stmts[:k])):
            continue
        var, init, cond = m.group(1), s.text[m.start(2):m.end(2)].strip(), s.text[m.start(3):m.end(3)].strip()
        entry = re.sub(rf"\b{re.escape(var)}\b", f"({init})", cond)
        close = next((x for x in stmts[k + 1:] if x.kind == "close" and x.depth == s.depth), None)
        outer_close = next((x for x in stmts[k + 1:] if x.kind == "close" and x.depth == s.depth - 1), None)
        if not close or not outer_close or outer_close.span[0] <= close.span[1]:
            continue
        a, b = close.span[1], outer_close.span[0]
        if not body[a:b].strip():
            continue
        new_body = body[:a] + f" if ({entry}) {{" + body[a:b] + "} " + body[b:]
        start = program.find(body)
        return program[:start] + new_body + program[start + len(body):]
    return None


def _hold_expressions(program: str) -> str | None:
    """A variable assigned from another variable keeps following it: a later
    read of t (after t = a; a = ...) reads a's current value."""
    body = _body(program)
    stmts = [s for s in parse(program) if s.kind in ("decl", "assign")]
    for k, s in enumerate(stmts):
        m = re.match(r"^(?:\w+\s+)?(\w+)\s*=\s*([A-Za-z_]\w*)\s*;?$", mask_literals(s.text).strip())
        if not m:
            continue
        t, src = m.group(1), m.group(2)
        later = [x for x in stmts[k + 1:] if src in x.assigns]
        if not later:
            continue
        for x in stmts[k + 1:]:
            if x.span[0] > later[0].span[0] and t in x.reads and t not in x.assigns:
                a, b = x.span
                new_text = re.sub(rf"(=\s*.*)\b{re.escape(t)}\b", lambda q: q.group(0)[:-len(t)] + src,
                                  body[a:b], count=1)
                if new_text == body[a:b]:
                    continue
                new_body = body[:a] + new_text + body[b:]
                start = program.find(body)
                return program[:start] + new_body + program[start + len(body):]
    return None


# (slot, wrong value) -> rewrite operator. A misconception whose kg_parts slot
# is listed here gets a misinterpreter automatically.
def _replace_text(find: str, replace: str) -> Callable[[str], str | None]:
    def op(program: str) -> str | None:
        out = re.sub(find, replace, program)
        return out if out != program else None
    return op


# generic Java transforms a misconception's ``misread_as`` can name (with args)
TRANSFORMS: dict[str, Callable[..., Callable[[str], str | None]]] = {
    "auto_initialize": lambda: _auto_initialize,
    "real_division": lambda: _division_keeps_fraction,
    "replace_operator": lambda old, new: _replace_op(old, new),
    "replace_text": lambda find, replace: _replace_text(find, replace),
    "remove_fallthrough": lambda: _no_fallthrough,
    "flip_loop_bounds": lambda: _flip_bound,
    "skip_after_empty_inner_loop": lambda: _empty_inner_skips_rest,
    "reads_follow_source": lambda: _hold_expressions,
}


def operator_for(mis: str, spec: dict | None = None) -> Callable[[str], str | None] | None:
    """The misinterpreter of a misconception, from its ``misread_as`` in the graph."""
    for m in lexicon.MISREAD.get(mis, []):
        make = TRANSFORMS.get(m.get("transform", ""))
        if make:
            return make(**m.get("args", {}))
    return None


# ---------------------------------------------------------------- variants

def apply_change(program: str, change: dict) -> str | None:
    """The program with one stated change (None when it does not apply)."""
    kind = change.get("kind")
    if kind == "start":
        var, val = change["var"], change["value"]
        new = re.sub(rf"(\b(?:int|long|double)\s+{re.escape(var)}\s*=\s*)[^;,]+", rf"\g<1>{val}", program, count=1)
        return new if new != program else None
    if kind == "loop_kind" and change.get("to") == "while":
        m = re.search(r"\bdo\s*\{", program)
        if not m:
            return None
        depth, i = 1, m.end()
        masked = mask_literals(program)
        while i < len(program) and depth:
            depth += {"{": 1, "}": -1}.get(masked[i], 0)
            i += 1
        w = re.match(r"\s*while\s*(\(.*?\))\s*;", program[i:], re.S)
        if not w:
            return None
        body = program[m.end():i - 1]
        return program[:m.start()] + f"while {w.group(1)} {{" + body + "}" + program[i + w.end():]
    if kind == "format":
        spec = change["spec"]
        new = re.sub(r"%-?\d*\.?\d*[fd]", spec, program, count=1)
        return new if new != program else None
    if kind == "repair":
        return repair(program)
    if kind == "cast":
        expr = re.sub(r"\s+", "", change["expr"])
        pat = r"\s*".join(re.escape(ch) for ch in expr)
        new = re.sub(rf"(?<![\w)])({pat})", lambda m: f"({change['cast']}) {m.group(1)}", program, count=1)
        return new if new != program else None
    return None


def repair(program: str, fix_name: bool = True) -> str | None:
    """The program with its compile errors fixed: missing semicolons added and
    the file named after its public class (the "after that" of a staged
    answer)."""
    body = _body(program)
    masked = mask_literals(body)
    cuts = _missing_semicolons(body, masked)
    new_body = body
    for pos in sorted(cuts, reverse=True):
        new_body = new_body[:pos] + ";" + new_body[pos:]
    new = program.replace(body, new_body) if cuts else program
    if fix_name:
        new = lexicon.rx("saved_as").sub("", new)
    return new if new != program else None


# ------------------------------------------------------------------- tracer



class Tracer:
    """Run a snippet for real, under misinterpretations and under changes."""

    def __init__(self, code: str, run_code: bool = True, question: str = "",
                 asked_name: str | None = None) -> None:
        self.code = code
        self.kind = classify_code(code)
        self.question = question
        self.asked_name = asked_name
        self.assumed: dict[str, str] = {}
        self.sampled: set[str] = set()   # free variables read with an invented value
        prelude = list(self.kind.context)
        java = self.kind.java
        if java:
            snippet_stmts = parse(program_text(java))
            for nm, assigned_first in free_variables(snippet_stmts):
                val = self._question_value(nm)
                if val is None:
                    val = "0" if assigned_first else _SAMPLE_INTS[len(self.assumed) % len(_SAMPLE_INTS)]
                    if not assigned_first:
                        self.sampled.add(nm)
                self.assumed[nm] = val
                typ = "double" if "." in val else "int"
                prelude.append(f"{typ} {nm} = {val};")
        self.prelude = tuple(prelude)
        self.program = program_text(java, self.prelude) if java else ""
        self.run_code = run_code and bool(self.program)

    def _question_value(self, name: str) -> str | None:
        for m in lexicon.rx("question_value").finditer(self.question or ""):
            if m.group(1) == name:
                return m.group(2)
        return None

    def trace(self, mis_specs: dict[str, dict | None] | None = None) -> Trace:
        stmts = parse(self.program) if self.program else []
        findings = tuple(static_checks(stmts, self.asked_name, _body(self.program) if self.program else ""))
        run = run_program(self.program) if self.run_code else Run(available=False)
        if not run.available and any(f.pattern == "uninitialized_read" for f in findings):
            f = next(f for f in findings if f.pattern == "uninitialized_read")
            run = Run(False, False, "", f.message, "compile")
        if self.run_code and run.error_kind == "compile":
            # javac reports errors in stages: syntax first, then the rest
            staged = list(run.errors)
            half = repair(self.program, fix_name=False)
            if half:
                staged += list(run_program(half).errors)
            run = Run(run.available, run.compiled, run.output, run.error, run.error_kind, run.values,
                      run.timed_out, tuple(dict.fromkeys(staged)), run.snapshots)
            idx = next((s.index for s in stmts if s.kind not in ("comment", "close", "header")
                        and not s.text.rstrip().endswith((";", "}", "{"))), 0)
            for _, sig in lexicon.SIGNALS:
                msg = next((e for e in run.errors if sig.get("compiler_message")
                            and re.search(sig["compiler_message"], e)), None)
                if msg:
                    findings += (StaticFinding(sig["name"], idx, "", msg),)
        mutants: dict[str, Run] = {}
        same: set[str] = set()
        for mid, spec in sorted((mis_specs or {}).items()):
            fn = operator_for(mid, spec)
            if not fn or not self.run_code:
                continue
            mutated = fn(self.program)
            if mutated and mutated != self.program:
                mutants[mid] = run_program(mutated)
                if _same_result(mutants[mid], run):
                    same.add(mid)
        return Trace(run, tuple(sorted(findings, key=lambda f: (f.stmt_index, f.pattern))), mutants,
                     self.program, dict(self.assumed), frozenset(same), stmts=tuple(stmts),
                     sampled=frozenset(self.sampled),
                     reads_input=bool(lexicon.rx("reads_input").search(self.program)))

    def trace_variant(self, change: dict) -> Run | None:
        return self.run_changes([change])

    def run_changes(self, changes: list[dict]) -> Run | None:
        """Run the program with several stated changes applied in order."""
        if not self.run_code or not changes:
            return None
        program = self.program
        for ch in changes:
            new = apply_change(program, ch)
            if new is None:
                return None
            program = new
        return run_program(program)

    def answer_program(self, answer_code: list[str]) -> tuple[str, list[StaticFinding]]:
        """The question's code (or context) followed by the student's code;
        variables the student uses without declaring are declared from use
        (and reported)."""
        base = list(self.prelude)
        if self.kind.java and not re.search(r"\bclass\s+\w+", self.kind.java):
            base += self.kind.java.splitlines()
        code = list(answer_code)
        probe = parse(program_text("\n".join(base + code)))
        types = variables(probe)
        extra, notes = [], []
        for nm, _ in free_variables(probe):
            elem = re.search(rf"\b{re.escape(nm)}\s*\[[^\]]+\]\s*=\s*(\w+)\s*\[", "\n".join(code))
            if elem and types.get(elem.group(1), "").endswith("[]"):
                src = elem.group(1)
                extra.append(f"{types[src]} {nm} = new {types[src][:-2]}[{src}.length];")
                notes.append(StaticFinding("missing_declaration", 0, nm,
                                           f"{nm} is used but never declared (assumed {types[src]} of {src}.length)"))
            else:
                extra.append(f"int {nm} = 0;")
                notes.append(StaticFinding("missing_declaration", 0, nm, f"{nm} is used but never declared"))
        return program_text("\n".join(base + extra + code)), notes

    def trace_answer(self, answer_code: list[str],
                     mis_specs: dict[str, dict | None] | None = None) -> tuple[Run, tuple[StaticFinding, ...], dict[str, Run]]:
        program, notes = self.answer_program(answer_code)
        stmts = parse(program)
        findings = tuple(notes) + tuple(static_checks(stmts, self.asked_name, _body(program)))
        run = run_program(program) if jdk_available() else Run(available=False)
        mutants = {}
        for mid, spec in sorted((mis_specs or {}).items()):
            fn = operator_for(mid, spec)
            if fn:
                mutated = fn(program)
                if mutated and mutated != program:
                    mutants[mid] = run_program(mutated)
        return run, findings, mutants


def _same_result(a: Run, b: Run) -> bool:
    return (a.output == b.output and a.error_kind == b.error_kind and a.values == b.values)
