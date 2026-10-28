"""Execution: split Java code into statements and run it for real.

Stand-in for ``lp_percpt.execution`` (``parse``, ``Tracer.trace``,
``MUTATIONS``):

* ``parse(code)`` splits a snippet into simple statements and headers, and
  records per statement what it declares, assigns and reads.
* ``static_checks(stmts)`` finds code patterns without running anything,
  most importantly "declared without initializer, then read" (definite
  assignment). jshell would give such a top-level variable a default value,
  so the snippet is never run in jshell.
* ``Tracer(code).trace()`` compiles the snippet wrapped in
  ``class Main { public static void main(String[] args) { ... } }`` with
  ``javac`` and runs it with ``java``. It records the output, the compile or
  run error, and the values of top-level variables (by instrumenting the
  copy with ``System.err`` prints). Without a JDK the run is
  ``available=False`` and only the static checks apply.
* ``MUTATIONS[mis_id]`` rewrites the code the way a student holding that
  misconception reads it (the misinterpreter); ``Trace.mutants[mis_id]`` is
  the run of the rewritten code.

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

_TYPES = ("int", "double", "boolean", "char", "long", "String", "float", "short", "byte")
_DEFAULTS = {"int": "0", "double": "0.0", "boolean": "false", "char": "'\\u0000'",
             "long": "0L", "String": "null", "float": "0.0f", "short": "0", "byte": "0"}
_KEYWORDS = frozenset({
    "int", "double", "boolean", "char", "long", "String", "float", "short", "byte",
    "if", "else", "for", "while", "do", "return", "new", "true", "false", "null",
    "System", "out", "println", "print", "printf", "Math", "public", "static",
    "void", "class", "final", "break", "continue", "switch", "case", "default",
    "args", "main", "length", "StdOut", "StdIn", "StdDraw", "Integer", "Double",
})
RUN_TIMEOUT_S = 5
COMPILE_TIMEOUT_S = 60


@dataclass(frozen=True)
class CodeStmt:
    """One simple statement or header of the snippet."""

    index: int
    text: str
    line: int
    depth: int
    kind: str  # decl | assign | print | header | close | other
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

    def value_of(self, name: str) -> str | None:
        for k, v in self.values:
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


@dataclass
class Trace:
    """The real run plus the misinterpreter runs."""

    run: Run
    findings: tuple[StaticFinding, ...] = ()
    mutants: dict[str, Run] = field(default_factory=dict)
    program: str = ""


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


def program_text(code: str) -> str:
    """The snippet as a compilable Main program (classes kept as written)."""
    if re.search(r"\bclass\s+\w+", code):
        return code
    if re.search(r"static\s+void\s+main\s*\(", code):
        return "public class Main {\n" + code + "\n}\n"
    body = "\n".join("        " + ln for ln in code.splitlines())
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


def parse(code: str) -> list[CodeStmt]:
    """Split a snippet (or the body of main) into statements and headers.

    Spans are offsets into ``_body(code)`` so instrumentation can insert
    text without rebuilding the program.
    """
    body = _body(code)
    masked = mask_literals(body)
    stmts: list[CodeStmt] = []
    state = {"start": 0, "depth": 0}

    def flush(end: int, hint: str = "") -> None:
        s0 = state["start"]
        raw = body[s0:end]
        text = raw.strip()
        state["start"] = end
        if not text:
            return
        lead = s0 + (len(raw) - len(raw.lstrip()))
        m = re.match(r"else\b\s*(?!if\b)(?=\S)", text)
        if m and hint != "header":  # "else x = 1;" -> header "else" + statement
            _add(stmts, body, lead, lead + 4, state["depth"], "header")
            lead = lead + m.end()
            text = body[lead:end].strip()
        _add(stmts, body, lead, lead + len(text), state["depth"], hint)

    paren = 0
    for i, ch in enumerate(masked):
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
            flush(i, "header")
            state["depth"] += 1
            state["start"] = i + 1
        elif ch == "}" and paren == 0:
            flush(i)
            state["depth"] = max(0, state["depth"] - 1)
            _add(stmts, body, i, i + 1, state["depth"], "close")
            state["start"] = i + 1
    flush(len(body))
    return stmts


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


# ------------------------------------------------------------ static checks

def static_checks(stmts: list[CodeStmt]) -> list[StaticFinding]:
    """Patterns found without running the code (sorted by statement)."""
    found: list[StaticFinding] = []
    found += _uninitialized_reads(stmts)
    types = variables(stmts)
    for s in stmts:
        if s.kind == "print" and s.printed and types.get(s.printed.strip(), "").endswith("[]"):
            found.append(StaticFinding("array_printed", s.index, s.printed.strip(),
                                       "printing an array variable prints its reference"))
        if "/" in mask_literals(s.text) and _int_division(s, types):
            found.append(StaticFinding("int_division", s.index, "", "both operands of / are int"))
    return sorted(found, key=lambda f: (f.stmt_index, f.pattern, f.variable))


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
    for m in re.finditer(r"([A-Za-z_]\w*|\d+(?:\.\d+)?)\s*/\s*([A-Za-z_]\w*|\d+(?:\.\d+)?)", masked):
        a, b = m.group(1), m.group(2)
        if all(_is_int(x, types) for x in (a, b)):
            return True
    return False


def _is_int(tok: str, types: dict[str, str]) -> bool:
    return bool(re.fullmatch(r"\d+", tok)) or types.get(tok) in ("int", "long", "short", "byte")


# -------------------------------------------------------------------- runs

def jdk_available() -> bool:
    return bool(shutil.which("javac") and shutil.which("java"))


def _instrument(program: str) -> str:
    """Copy of ``program`` that prints top-level variable values to stderr.

    A print is inserted after each depth-0 statement that assigns a
    primitive or String variable, unless that statement is the body of a
    header without braces (inserting there would change the control flow).
    """
    body = _body(program)
    if body == program:
        return program
    stmts = parse(program)
    types = variables(stmts)
    inserts: list[tuple[int, str]] = []
    for k, s in enumerate(stmts):
        if s.depth != 0 or s.kind in ("header", "close"):
            continue
        prev = stmts[k - 1] if k else None
        if prev and prev.kind == "header" and not body[prev.span[1]:s.span[0]].strip().startswith("{"):
            continue
        for nm in s.assigns:
            if types.get(nm, "") in _TYPES:
                inserts.append((s.span[1], f' System.err.println("@@{nm}=" + {nm});'))
    # final values at the end of main override the per-statement snapshots
    final = sorted({nm for _, txt in inserts for nm in re.findall(r"@@(\w+)=", txt)})
    if final:
        inserts.append((len(body), "".join(f' System.err.println("@@{nm}=" + {nm});' for nm in final)))
    if not inserts:
        return program
    new_body = body
    for pos, text in sorted(inserts, reverse=True):
        new_body = new_body[:pos] + text + new_body[pos:]
    start = program.find(body)
    return program[:start] + new_body + program[start + len(body):]


@lru_cache(maxsize=256)
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
    cls = re.search(r"public\s+class\s+(\w+)", program)
    name = cls.group(1) if cls else "Main"
    with tempfile.TemporaryDirectory(prefix="lp_graph_") as tmp:
        src = Path(tmp) / f"{name}.java"
        src.write_text(program, encoding="utf-8")
        try:
            comp = subprocess.run(["javac", "-encoding", "UTF-8", "-nowarn", src.name],
                                  cwd=tmp, capture_output=True, text=True,
                                  timeout=COMPILE_TIMEOUT_S)
        except (OSError, subprocess.TimeoutExpired):
            return Run(available=False)
        if comp.returncode != 0:
            msgs = re.findall(r"error: (.+)", comp.stderr)
            return Run(True, False, "", msgs[0].strip() if msgs else comp.stderr.strip()[:200], "compile")
        try:
            res = subprocess.run(["java", "-cp", tmp, name], cwd=tmp, capture_output=True,
                                 text=True, timeout=RUN_TIMEOUT_S, input="")
            out, err, timed_out = res.stdout, res.stderr, False
        except subprocess.TimeoutExpired as exc:
            out = exc.stdout.decode() if isinstance(exc.stdout, bytes) else (exc.stdout or "")
            err = exc.stderr.decode() if isinstance(exc.stderr, bytes) else (exc.stderr or "")
            timed_out = True
    values: dict[str, str] = {}
    other_err: list[str] = []
    for ln in err.splitlines():
        m = re.match(r"@@(\w+)=(.*)$", ln)
        if m:
            values[m.group(1)] = m.group(2)
        elif ln.strip():
            other_err.append(ln.strip())
    exc_line = next((ln for ln in other_err if "Exception" in ln or "Error" in ln), "")
    kind = "timeout" if timed_out else ("run" if exc_line else "")
    return Run(True, True, out.replace("\r\n", "\n"), exc_line, kind,
               tuple(sorted(values.items())), timed_out)


# --------------------------------------------------------------- mutations

def _auto_initialize(program: str) -> str | None:
    """LocalVariablesAutoInitialized: every local gets its default value."""
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
    """PrintEqualsPrintln (read as: print also ends the line)."""
    out = re.sub(r"System\.out\.print\s*\(", "System.out.println(", program)
    return out if out != program else None


def _division_keeps_fraction(program: str) -> str | None:
    """IntegerDivisionGivesFraction: int / int computed as real division.

    Variables that receive a division become double so the misread program
    still compiles (the student expects them to hold the fraction).
    """
    masked = mask_literals(program)
    out, last, changed = [], 0, False
    for m in re.finditer(r"(?<![\w.])([A-Za-z_]\w*|\d+)\s*/\s*([A-Za-z_]\w*|\d+)(?![\w.])", masked):
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


MUTATIONS: dict[str, Callable[[str], str | None]] = {
    "LocalVariablesAutoInitialized": _auto_initialize,
    "PrintEqualsPrintln": _print_is_println,
    "IntegerDivisionGivesFraction": _division_keeps_fraction,
}


class Tracer:
    """Run a snippet for real and under misinterpretations."""

    def __init__(self, code: str, run_code: bool = True) -> None:
        self.code = code
        self.program = program_text(code) if code.strip() else ""
        self.run_code = run_code and bool(self.program)

    def trace(self, mis_ids: list[str] | tuple[str, ...] = ()) -> Trace:
        stmts = parse(self.program) if self.program else []
        findings = tuple(static_checks(stmts))
        run = run_program(self.program) if self.run_code else Run(available=False)
        if not run.available and any(f.pattern == "uninitialized_read" for f in findings):
            f = next(f for f in findings if f.pattern == "uninitialized_read")
            run = Run(False, False, "", f.message, "compile")
        mutants: dict[str, Run] = {}
        for mid in sorted(set(mis_ids)):
            fn = MUTATIONS.get(mid)
            if not fn or not self.run_code:
                continue
            mutated = fn(self.program)
            if mutated:
                mutants[mid] = run_program(mutated)
        return Trace(run, findings, mutants, self.program)
