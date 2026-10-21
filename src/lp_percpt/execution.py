"""
execution.py — run the code a prompt is about, and run it again under each
misconception that can be written as a change to the code (evidence step).

    trace = get_tracer().trace(code, hint=question_text)

The code is parsed (the Chapter-1 Java subset: blocks, if / else, for, while,
do-while, switch, simple statements, class and method declarations), every
body is turned into a braced block, and the program is instrumented so that a
run records, besides what it prints:

    values   every value each variable takes, in order       @T name=value
    lines    the source lines executed, in order              @L n
    passes   how many times each loop body ran                @P id
    error    an exception, or "timeout" for a loop that does not end

Variables the snippet uses but does not declare are taken from the hint
("x = 17" in the question) or, failing that, declared as int 1, 2, 3, ... in turn.
StdIn / StdOut are stubbed; StdIn reads the input the question gives.

MUTATIONS maps misconception ids of the knowledge graph to a change of the
program that does what a student holding that misconception expects (e.g.
AssignmentOppositeDirection: `a = b;` runs as `b = a;`). Running each one gives
the values and output that misconception predicts. Only mutants that compile,
and whose result differs from the real run, are kept.

Needs a JDK (jshell on PATH); without one, trace() returns None and the
evidence step falls back to its text checks. Results are cached on disk.
"""
from __future__ import annotations

import hashlib
import os
import json
import re
import shutil
import subprocess
import tempfile
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path
from typing import Callable, Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parents[2]
CACHE_DIR = ROOT / "output" / "exec_cache"
MUTANT_WORKERS = 2      # jshell runs at once (each one starts two JVMs)
TIMEOUT = 15            # seconds per jshell run (a non-ending loop is cut off)
MAX_EVENTS = 4000       # trace lines kept per run
VERSION = "7"           # bump to invalidate the cache when instrumentation changes

# ── tokens ──────────────────────────────────────────────────────────────────
_TOKEN_RE = re.compile(r"""
    (?P<ws>\s+) | (?P<comment>//[^\n]*|/\*.*?\*/) |
    (?P<str>"(?:\\.|[^"\\])*") | (?P<chr>'(?:\\.|[^'\\])*') |
    (?P<num>\d+(?:\.\d+)?(?:[eE][+-]?\d+)?[LlDdFf]?) |
    (?P<id>[A-Za-z_$][\w$]*) |
    (?P<op>>>>=|<<=|>>=|>>>|\+\+|--|&&|\|\||[+\-*/%&|^!=<>]=|->|::|[{}()\[\];,.?:~+\-*/%&|^!=<>@])
""", re.S | re.X)

TYPES = {"int", "double", "boolean", "char", "long", "float", "short", "byte", "String", "var"}
MODIFIERS = {"public", "private", "protected", "static", "final", "abstract"}


@dataclass
class Tok:
    kind: str
    text: str
    line: int


def tokenize(code: str) -> List[Tok]:
    toks, line, pos = [], 1, 0
    while pos < len(code):
        m = _TOKEN_RE.match(code, pos)
        if not m:                                  # unknown character: keep it as an operator
            toks.append(Tok("op", code[pos], line))
            pos += 1
            continue
        kind, text = m.lastgroup, m.group()
        if kind not in ("ws", "comment"):
            toks.append(Tok(kind, text, line))
        line += text.count("\n")
        pos = m.end()
    return toks


def _join(toks: List[Tok]) -> str:
    out = ""
    for t in toks:
        if out and (t.kind in ("id", "num", "str", "chr") and (out[-1].isalnum() or out[-1] in "_$\"']")):
            out += " "
        elif out and t.text in ("=", "==", "!=", "<", ">", "<=", ">=", "&&", "||", "+", "-", "*", "/", "%",
                                "+=", "-=", "*=", "/=", "%=", "?", ":"):
            out += " "
        elif out and out[-1] in "=<>&|+-*/%?:," and not out.endswith(("++", "--")) and t.text not in (")", "]", ";", ",", "."):
            out += " "
        out += t.text
    return out


# ── statements ──────────────────────────────────────────────────────────────
@dataclass
class Stmt:
    kind: str                       # simple, block, if, for, while, do, switch, decl (class / method), label
    line: int
    text: str = ""                  # simple statement text without ';', or header text
    cond: str = ""
    body: Optional["Stmt"] = None
    other: Optional["Stmt"] = None  # else branch
    items: List["Stmt"] = field(default_factory=list)
    init: str = ""
    update: str = ""
    else_line: int = 0
    loop_id: int = 0


class _Parser:
    def __init__(self, toks: List[Tok]):
        self.t, self.i, self.loops = toks, 0, 0

    def peek(self, k: int = 0) -> Optional[Tok]:
        return self.t[self.i + k] if self.i + k < len(self.t) else None

    def take(self) -> Tok:
        tok = self.t[self.i]
        self.i += 1
        return tok

    def expect(self, text: str) -> Tok:
        tok = self.peek()
        if tok is None or tok.text != text:
            raise SyntaxError(f"expected {text!r} at {tok.text if tok else 'end'}")
        return self.take()

    def parens(self) -> List[Tok]:
        self.expect("(")
        depth, out = 1, []
        while True:
            tok = self.take()
            if tok.text == "(":
                depth += 1
            elif tok.text == ")":
                depth -= 1
                if depth == 0:
                    return out
            out.append(tok)

    def items(self, until: str = "") -> List[Stmt]:
        out = []
        while self.peek() is not None and self.peek().text != until:
            out.append(self.stmt())
        return out

    def stmt(self) -> Stmt:
        tok = self.peek()
        if tok.text == "{":
            self.take()
            body = self.items("}")
            self.expect("}")
            return Stmt("block", tok.line, items=body)
        if tok.text == ";":
            self.take()
            return Stmt("simple", tok.line, text="")
        if tok.text == "if":
            self.take()
            cond = _join(self.parens())
            body = self.stmt()
            other, else_line = None, 0
            if self.peek() is not None and self.peek().text == "else":
                else_line = self.take().line
                other = self.stmt()
            return Stmt("if", tok.line, cond=cond, body=body, other=other, else_line=else_line)
        if tok.text in ("for", "while"):
            self.take()
            head = self.parens()
            self.loops += 1
            lid = self.loops
            body = self.stmt()
            if tok.text == "while":
                return Stmt("while", tok.line, cond=_join(head), body=body, loop_id=lid)
            parts, cur, depth = [], [], 0
            for h in head:
                depth += h.text in "([{"
                depth -= h.text in ")]}"
                if h.text == ";" and depth == 0:
                    parts.append(cur)
                    cur = []
                else:
                    cur.append(h)
            parts.append(cur)
            if len(parts) == 3:
                return Stmt("for", tok.line, init=_join(parts[0]), cond=_join(parts[1]), update=_join(parts[2]),
                            body=body, loop_id=lid)
            return Stmt("foreach", tok.line, text=_join(head), body=body, loop_id=lid)
        if tok.text == "do":
            self.take()
            self.loops += 1
            lid = self.loops
            body = self.stmt()
            self.expect("while")
            cond = _join(self.parens())
            if self.peek() is not None and self.peek().text == ";":
                self.take()
            return Stmt("do", tok.line, cond=cond, body=body, loop_id=lid)
        if tok.text == "switch":
            self.take()
            head = _join(self.parens())
            self.expect("{")
            body: List[Stmt] = []
            while self.peek() is not None and self.peek().text != "}":
                if self.peek().text in ("case", "default"):
                    lab = []
                    while self.peek().text != ":":
                        lab.append(self.take())
                    self.take()
                    body.append(Stmt("label", lab[0].line, text=_join(lab) + ":"))
                else:
                    body.append(self.stmt())
            self.expect("}")
            return Stmt("switch", tok.line, cond=head, items=body)
        # class / method declaration: a header up to '{' that contains 'class' or a parameter list
        j, depth, head = self.i, 0, []
        while j < len(self.t):
            x = self.t[j]
            if x.text in (";",) and depth == 0:
                break
            if x.text == "{" and depth == 0:
                if any(h.text == "class" for h in head) or (head and head[-1].text == ")" and head[0].text in MODIFIERS | TYPES | {"void"}):
                    self.i = j + 1
                    members = self.items("}")
                    self.expect("}")
                    return Stmt("decl", tok.line, text=_join(head), items=members)
                break
            depth += x.text in "(["
            depth -= x.text in ")]"
            head.append(x)
            j += 1
        # simple statement up to ';' (braces inside are array initializers)
        out, depth = [], 0
        while self.peek() is not None:
            x = self.take()
            if x.text == ";" and depth == 0:
                break
            depth += x.text in "([{"
            depth -= x.text in ")]}"
            out.append(x)
        return Stmt("simple", tok.line, text=_join(out))


def parse(code: str) -> List[Stmt]:
    return _Parser(tokenize(code)).items()


# ── what a simple statement assigns ─────────────────────────────────────────
_DECL_RE = re.compile(r"^(?:final\s+)?(?:" + "|".join(sorted(TYPES)) + r"|[A-Z]\w*)(?:\s*\[\s*\])*\s+(.*)$")
_ASSIGN_RE = re.compile(r"^([A-Za-z_]\w*)\s*(?:\[[^\]]*\]\s*)*(?:=(?!=)|\+=|-=|\*=|/=|%=)")
_INC_RE = re.compile(r"^(?:(?:\+\+|--)\s*([A-Za-z_]\w*)|([A-Za-z_]\w*)\s*(?:\+\+|--))$")


def declared_names(text: str) -> List[str]:
    m = _DECL_RE.match(text)
    if not m or text.split()[0] in ("return", "new", "throw"):
        return []
    names, depth, cur = [], 0, ""
    for ch in m.group(1):
        depth += ch in "([{"
        depth -= ch in ")]}"
        if ch == "," and depth == 0:
            names.append(cur)
            cur = ""
        else:
            cur += ch
    names.append(cur)
    out = []
    for n in names:
        n = n.split("=")[0].strip()
        n = re.sub(r"\[\s*\]", "", n).strip()
        if re.fullmatch(r"[A-Za-z_]\w*", n):
            out.append(n)
    return out


def assigned_name(text: str) -> Optional[str]:
    m = _ASSIGN_RE.match(text) or _INC_RE.match(text)
    if not m:
        return None
    return next(g for g in m.groups() if g)


# ── emitting instrumented Java ──────────────────────────────────────────────
HELPERS = """
static String __s(Object v) {
  if (v instanceof int[] x) return java.util.Arrays.toString(x);
  if (v instanceof double[] x) return java.util.Arrays.toString(x);
  if (v instanceof boolean[] x) return java.util.Arrays.toString(x);
  if (v instanceof char[] x) return java.util.Arrays.toString(x);
  if (v instanceof long[] x) return java.util.Arrays.toString(x);
  if (v instanceof Object[] x) return java.util.Arrays.deepToString(x);
  return String.valueOf(v);
}
static int __n = 0;
static void __e(String s) { if (__n++ < %d) System.err.println(s); }
static void __t(String n, Object v) { __e("@T " + n + "=" + __s(v)); }
static void __l(int n) { __e("@L " + n); }
static void __p(int n) { __e("@P " + n); }
""" % MAX_EVENTS

# S&W's StdIn / StdOut, reading the input the question gives ("the user types: 42<Enter>")
LIBS = """
class StdIn {
  static java.util.Scanner sc = new java.util.Scanner(%s);
  static boolean isEmpty() { return !sc.hasNext(); }
  static boolean hasNextLine() { return sc.hasNextLine(); }
  static int readInt() { return sc.nextInt(); }
  static double readDouble() { return sc.nextDouble(); }
  static long readLong() { return sc.nextLong(); }
  static boolean readBoolean() { return sc.nextBoolean(); }
  static String readString() { return sc.next(); }
  static String readLine() { return sc.hasNextLine() ? sc.nextLine() : null; }
}
class StdOut {
  static void print(Object o) { System.out.print(o); }
  static void println(Object o) { System.out.println(o); }
  static void println() { System.out.println(); }
  static void printf(String f, Object... a) { System.out.printf(f, a); }
}
"""
_INPUT_TYPES_RE = re.compile(r"\btypes?:?\s+(.+?<Enter>.*?)(?:\n|$)", re.I)
_INPUT_FOR_RE = re.compile(r"\b(?:for|with) the input[ \t]+((?:-?[\w.]+[ \t]*)+?)[ \t]*(?:[?.;)\n]|$)", re.I)


def input_of(hint: str) -> str:
    """The standard input a question gives: 'the user types: 42<Enter> then Ann Lee<Enter>'
    or 'for the input 4 -2 6 99999 3'."""
    m = _INPUT_TYPES_RE.search(hint or "")
    if m:
        text = re.sub(r"\s*\bthen\b\s*", "", m.group(1)).replace("<Enter>", "\n")
        return "\n".join(line.strip() for line in text.split("\n"))
    m = _INPUT_FOR_RE.search(hint or "")
    return m.group(1).strip() + "\n" if m else ""


Rewrite = Callable[[Stmt], Optional[str]]      # a mutation: returns replacement Java for a statement, or None


class Emitter:
    def __init__(self, rewrite: Optional[Rewrite] = None, in_class: bool = False, in_method: bool = False):
        self.rewrite = rewrite
        self.in_class = in_class          # inside a class body
        self.in_method = in_method        # inside a method body (statements are instrumented)

    def block(self, s: Optional[Stmt], prefix: str = "", suffix: str = "") -> str:
        if s is None:
            return "{}"
        inner = "".join(self.stmt(x) for x in s.items) if s.kind == "block" else self.stmt(s)
        return "{" + prefix + inner + suffix + "}"

    def stmt(self, s: Stmt) -> str:
        if self.rewrite is not None:
            r = self.rewrite(s, self)
            if r is not None:
                return r
        return self.plain(s)

    def plain(self, s: Stmt) -> str:
        k = s.kind
        if k == "block":
            return self.block(s)
        if k == "label":
            return s.text + " "
        if k == "simple":
            return self.simple(s, s.text)
        if k == "if":
            out = f"__l({s.line}); if ({s.cond}) {self.block(s.body)}"
            if s.other is not None:
                out += f" else {self.block(s.other, prefix=f'__l({s.else_line});')}"
            return out + "\n"
        if k == "while":
            return f"__l({s.line}); while ({s.cond}) {self.block(s.body, prefix=f'__p({s.loop_id});')}\n"
        if k == "do":
            return f"__l({s.line}); do {self.block(s.body, prefix=f'__p({s.loop_id});')} while ({s.cond});\n"
        if k == "for":
            v = declared_names(s.init) or ([assigned_name(s.init)] if assigned_name(s.init) else [])
            trace = "".join(f'__t("{n}", {n});' for n in v)
            # the update also records the loop variable, so its value at the failing test is kept
            update = s.update + "".join(f', __t("{n}", {n})' for n in v) if s.update else s.update
            return f"__l({s.line}); for ({s.init}; {s.cond}; {update}) {self.block(s.body, prefix=f'__p({s.loop_id});' + trace)}\n"
        if k == "foreach":
            v = declared_names(s.text.split(":")[0].strip())
            trace = "".join(f'__t("{n}", {n});' for n in v)
            return f"__l({s.line}); for ({s.text}) {self.block(s.body, prefix=f'__p({s.loop_id});' + trace)}\n"
        if k == "switch":
            return f"__l({s.line}); switch ({s.cond}) {{" + "".join(self.stmt(x) for x in s.items) + "}\n"
        if k == "decl":
            is_class = "class " in s.text
            helpers = HELPERS if (is_class and not self.in_class) else ""
            inner = Emitter(self.rewrite, in_class=True, in_method=not is_class)
            return s.text + " {" + helpers + "".join(inner.stmt(x) for x in s.items) + "}\n"
        return ""

    def simple(self, s: Stmt, text: str) -> str:
        if not text:
            return ";"
        if text.split()[0] in ("break", "continue", "return", "throw"):
            return f"__l({s.line}); {text};\n"
        if self.in_class and not self.in_method:   # a field: not executable code
            return text + ";\n"
        # x++ / --x inside an expression (int w = ++x) changes x too
        bumped = []
        for a, b in re.findall(r"\b([A-Za-z_]\w*)\s*(?:\+\+|--)|(?:\+\+|--)\s*([A-Za-z_]\w*)", text):
            if (a or b) not in bumped and not (a or b).startswith("__"):
                bumped.append(a or b)
        names = declared_names(text)
        if names:                                  # declarations keep their scope: no braces
            return (f"__l({s.line}); {text}; "
                    + "".join(f'__t("{n}", {n});' for n in [b for b in bumped if b not in names] + names) + "\n")
        # a rewritten statement may hold several parts ("a = b; b = 0"): trace each assigned name
        assigned = []
        for part in text.split(";"):
            n = assigned_name(part.strip())
            if n and n not in assigned and not n.startswith("__"):
                assigned.append(n)
        assigned += [n for n in bumped if n not in assigned]
        return f"{{__l({s.line}); {text}; " + "".join(f'__t("{n}", {n});' for n in assigned) + "}\n"


# ── running ─────────────────────────────────────────────────────────────────
@dataclass
class Run:
    ok: bool                          # compiled and ran (a timeout or exception still counts as ran)
    output: str = ""
    values: Dict[str, List[str]] = field(default_factory=dict)
    lines: List[int] = field(default_factory=list)
    passes: Dict[int, int] = field(default_factory=dict)
    error: str = ""                   # exception class, "timeout", or a compile error

    @property
    def final(self) -> Dict[str, str]:
        return {k: v[-1] for k, v in self.values.items() if v}

    def observable(self) -> Tuple:
        return (self.output.strip(), tuple(sorted(self.final.items())), self.error.split(":")[0])

    def to_dict(self) -> Dict:
        return {"ok": self.ok, "output": self.output, "values": self.values, "lines": self.lines,
                "passes": {str(k): v for k, v in self.passes.items()}, "error": self.error}

    @classmethod
    def from_dict(cls, d: Dict) -> "Run":
        return cls(d["ok"], d["output"], d["values"], d["lines"], {int(k): v for k, v in d["passes"].items()}, d["error"])


@dataclass
class Trace:
    code: str
    run: Run
    mutants: Dict[str, Run]           # misconception id -> run of the mutated program
    loops: Dict[int, int]             # loop id -> source line


_LINE_NO_RE = re.compile(r"^\s*(\d+)\s{2,}", re.M)
_GIVEN_RE = re.compile(r"\b([a-z]\w*)\s*=\s*(-?\d+(?:\.\d+)?|true|false|\"[^\"]*\"|'.')")


def _strip_line_numbers(code: str) -> str:
    """'1  if (a > b) {' style listings: drop the numbers but keep them as the line numbers."""
    lines = code.split("\n")
    numbered = [l for l in lines if l.strip()]
    if numbered and all(_LINE_NO_RE.match(l) for l in numbered):
        out = [""] * (max(int(_LINE_NO_RE.match(l).group(1)) for l in numbered))
        for l in numbered:
            m = _LINE_NO_RE.match(l)
            out[int(m.group(1)) - 1] = l[m.end():]
        return "\n".join(out)
    return code


def program_text(code: str) -> str:
    """The code without prose: drops lines after a blank line that read as text."""
    code = _strip_line_numbers(code)
    keep = []
    for line in code.split("\n"):
        if re.match(r"^\s*(Trace line|Output|Answer|Note)\s*:", line):
            break
        keep.append(line)
    return "\n".join(keep)


def _type_of(value: str) -> str:
    if value in ("true", "false"):
        return "boolean"
    if value.startswith('"'):
        return "String"
    if value.startswith("'"):
        return "char"
    return "double" if "." in value else "int"


def _kill_tree(pid: int) -> None:
    """End a process and every process it started."""
    if os.name == "nt":
        subprocess.run(["taskkill", "/F", "/T", "/PID", str(pid)], capture_output=True)
        return
    try:
        children = subprocess.run(["pgrep", "-P", str(pid)], capture_output=True, text=True).stdout.split()
        for child in children:
            _kill_tree(int(child))
        os.kill(pid, 9)
    except (OSError, ValueError):
        pass


class Tracer:
    def __init__(self, jshell: Optional[str] = None, cache_dir: Path = CACHE_DIR):
        self.jshell = jshell or shutil.which("jshell")
        self.cache_dir = Path(cache_dir)

    @property
    def available(self) -> bool:
        return self.jshell is not None

    # one jshell run of an instrumented program
    def _jshell(self, src: str) -> Run:
        with tempfile.NamedTemporaryFile("w", suffix=".jsh", delete=False, encoding="utf-8") as fh:
            fh.write(src + "\n/exit\n")
            path = fh.name
        p = subprocess.Popen([self.jshell, "--feedback", "silent", "-J-Xmx96m", "-R-Xmx96m", "-R-Xss4m", path],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                             encoding="utf-8", errors="replace")
        try:
            out, err = p.communicate(timeout=TIMEOUT)
            timed_out = False
        except subprocess.TimeoutExpired:
            # jshell runs the code in a child JVM: end the whole tree, or a program
            # that does not stop keeps running after jshell is gone
            _kill_tree(p.pid)
            out, err = p.communicate()
            timed_out = True
        finally:
            Path(path).unlink(missing_ok=True)
        run = Run(True, out)
        problems = []
        for line in err.splitlines():
            if line.startswith("@T "):
                name, _, value = line[3:].partition("=")
                if not name.startswith("__"):
                    run.values.setdefault(name, []).append(value)
            elif line.startswith("@L "):
                run.lines.append(int(line[3:]))
            elif line.startswith("@P "):
                lid = int(line[3:])
                run.passes[lid] = run.passes.get(lid, 0) + 1
            elif line.strip():
                problems.append(line)
        text = "\n".join(problems)
        if timed_out or len(run.lines) >= MAX_EVENTS // 2:
            run.error = "timeout"
        elif "Error:" in text:
            run.ok, run.error = False, text[:400]
        else:
            m = re.search(r"Exception ([\w.]+)", text)
            if m:
                run.error = m.group(1).split(".")[-1]
        return run

    def _source(self, stmts: List[Stmt], given: str, rewrite: Optional[Rewrite]) -> str:
        body = "".join(Emitter(rewrite).stmt(s) for s in stmts)
        if any(s.kind == "decl" and "class " in s.text for s in stmts):
            cls = next(re.search(r"class\s+(\w+)", s.text).group(1) for s in stmts
                       if s.kind == "decl" and "class " in s.text)
            body = body.replace("public class", "class") + f"\n{cls}.main(new String[0]);"
            return given + body
        # at the end, record every top-level variable once more: an array changed through
        # another name (b[0] = 9 after b = a) then shows its final contents under each name
        names = [n for s in stmts if s.kind == "simple" for n in declared_names(s.text)]
        final = "".join(f'__t("{n}", {n});' for n in dict.fromkeys(names))
        return HELPERS + given + body + ("\n" + final if final else "")

    def _run_program(self, code: str, hint: str, rewrite: Optional[Rewrite] = None,
                     given: Optional[str] = None) -> Tuple[Run, str]:
        stmts = parse(program_text(code))
        if given is None:
            given = self._givens(code, hint, stmts)
        return self._jshell(self._source(stmts, given, rewrite)), given

    def _givens(self, code: str, hint: str, stmts: List[Stmt], allowed: Optional[set] = None) -> str:
        """Declarations for variables the snippet uses without declaring them.
        allowed: only these names are declared (for code a student wrote: the
        names the given code also uses), so a variable the student uses
        without declaring it does not compile, as in Java."""
        decls: Dict[str, str] = {}
        for name, value in _GIVEN_RE.findall(hint or ""):
            decls.setdefault(name, f"{_type_of(value)} {name} = {value};")
        given = ""
        if re.search(r"\bStd(In|Out)\.", code):
            given = LIBS % json.dumps(input_of(hint))
        start = 1
        for _ in range(6):                          # declare what jshell reports as missing
            run = self._jshell(self._source(stmts, given, None))
            missing = re.findall(r"symbol:\s+variable (\w+)", run.error)
            if allowed is not None:
                missing = [n for n in missing if n in allowed]
            if run.ok or not missing:
                break
            for name in missing:
                # distinct start values (1, 2, 3, ...), so a claim that mixes two
                # variables up ("a is b") is not confirmed by equal zeros
                given += decls.get(name, f"int {name} = {start};") + "\n"
                start += 1
        else:
            return given
        return given

    def trace(self, code: str, hint: str = "") -> Optional[Trace]:
        if not self.available or not code or not re.search(r"[;{}]", code):
            return None
        key = hashlib.sha1(f"{VERSION}\n{hint}\n{code}".encode("utf-8")).hexdigest()[:16]
        cached = self.cache_dir / f"{key}.json"
        if cached.exists():
            d = json.loads(cached.read_text(encoding="utf-8"))
            if d is None:
                return None
            return Trace(code, Run.from_dict(d["run"]), {k: Run.from_dict(v) for k, v in d["mutants"].items()},
                         {int(k): v for k, v in d["loops"].items()})
        result = self._trace(code, hint)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        cached.write_text(json.dumps(None if result is None else {
            "run": result.run.to_dict(), "mutants": {k: v.to_dict() for k, v in result.mutants.items()},
            "loops": result.loops}), encoding="utf-8")
        return result

    def _trace(self, code: str, hint: str) -> Optional[Trace]:
        try:
            stmts = parse(program_text(code))
        except (SyntaxError, IndexError, AttributeError):
            return None
        given = self._givens(code, hint, stmts)
        run = self._jshell(self._source(stmts, given, None))
        if not run.ok:
            return None
        loops = {}
        def walk(ss):
            for s in ss:
                if s.loop_id:
                    loops[s.loop_id] = s.line
                for c in (s.body, s.other):
                    if c is not None:
                        walk([c])
                walk(s.items)
        walk(stmts)
        applicable = []
        for mid, rewrite in MUTATIONS.items():
            src = self._source(stmts, given, rewrite)
            if src != self._source(stmts, given, None):
                applicable.append((mid, src))
        mutants: Dict[str, Run] = {}
        with ThreadPoolExecutor(max_workers=MUTANT_WORKERS) as pool:
            for (mid, _), r in zip(applicable, pool.map(lambda a: self._jshell(a[1]), applicable)):
                if r.ok and r.observable() != run.observable():
                    mutants[mid] = r
        return Trace(code, run, mutants, loops)

    def run_code(self, code: str, hint: str = "", allowed: Optional[set] = None) -> Optional[Run]:
        """One run of code the student wrote (no misconception runs). Unlike
        trace(), a run that does not compile is returned, with its error.
        allowed: the undeclared names that may be declared (see _givens)."""
        if not self.available or not code or not re.search(r"[;{}]", code):
            return None
        allowed = set(allowed or ())
        key = hashlib.sha1(f"{VERSION}\nstudent\n{sorted(allowed)}\n{input_of(hint)}\n{hint}\n{code}".encode("utf-8")).hexdigest()[:16]
        cached = self.cache_dir / f"{key}.json"
        if cached.exists():
            d = json.loads(cached.read_text(encoding="utf-8"))
            return None if d is None else Run.from_dict(d)
        try:
            stmts = parse(program_text(code))
            run = self._jshell(self._source(stmts, self._givens(code, hint, stmts, allowed=allowed), None))
        except (SyntaxError, IndexError, AttributeError):
            run = None
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        cached.write_text(json.dumps(None if run is None else run.to_dict()), encoding="utf-8")
        return run

    def compiles(self, code: str) -> Tuple[Optional[bool], str]:
        """Does the code compile as a block of Java statements? jshell's top level gives
        an unassigned int the value 0; a block applies Java's definite-assignment rules.
        It is compiled as a lambda body, which must compile in full (a jshell method may
        defer an unknown name). (None, "") when jshell is unavailable."""
        if not self.available or not code:
            return None, ""
        key = hashlib.sha1(f"{VERSION}\ncompiles-lambda\n{code}".encode("utf-8")).hexdigest()[:16]
        cached = self.cache_dir / f"{key}.json"
        if cached.exists():
            d = json.loads(cached.read_text(encoding="utf-8"))
            return d["ok"], d["error"]
        run = self._jshell("Runnable __check = () -> {\n" + code + "\n};")
        ok, err = bool(run and run.ok), (run.error if run else "")
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        cached.write_text(json.dumps({"ok": ok, "error": err}), encoding="utf-8")
        return ok, err

    def trace_many(self, items: List[Tuple[str, str]], workers: int = 3) -> None:
        """Warm the cache for many (code, hint) pairs."""
        with ThreadPoolExecutor(max_workers=workers) as pool:
            list(pool.map(lambda a: self.trace(*a), items))

    def evaluate(self, expressions: List[str]) -> Dict[str, str]:
        """Values of literal Java expressions ('7 / 2', '(int) 3.7'), as jshell prints them."""
        if not self.available or not expressions:
            return {}
        key = hashlib.sha1(("expr\n" + "\n".join(expressions)).encode("utf-8")).hexdigest()[:16]
        cached = self.cache_dir / f"{key}.json"
        if cached.exists():
            return json.loads(cached.read_text(encoding="utf-8"))
        src = "".join(f'try {{ System.out.println("@V{i} " + ({e})); }} catch (Throwable t) {{ System.out.println("@V{i} " + t.getClass().getSimpleName()); }}\n'
                      for i, e in enumerate(expressions))
        run = self._jshell(src)
        out = {}
        for line in run.output.splitlines():
            m = re.match(r"@V(\d+) (.*)$", line)
            if m:
                out[expressions[int(m.group(1))]] = m.group(2).strip()
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        cached.write_text(json.dumps(out), encoding="utf-8")
        return out


# ── misconceptions as program changes ───────────────────────────────────────
_VAR_COPY_RE = re.compile(r"^([A-Za-z_]\w*)\s*=\s*([A-Za-z_]\w*)$")
_SIMPLE_ASSIGN_RE = re.compile(r"^([A-Za-z_]\w*)\s*=(?!=)\s*(.+)$")


def _on_simple(fn: Callable[[str], Optional[str]]) -> Rewrite:
    def rewrite(s: Stmt, em: Emitter) -> Optional[str]:
        if s.kind != "simple" or not s.text or declared_names(s.text):
            return None
        new = fn(s.text)
        return None if new is None else em.simple(s, new)
    return rewrite


def _on_conditions(fn: Callable[[str], str], kinds=("if", "while", "for", "do")) -> Rewrite:
    def rewrite(s: Stmt, em: Emitter) -> Optional[str]:
        if s.kind not in kinds:
            return None
        changed = Stmt(**{**s.__dict__, "cond": fn(s.cond)})
        return em.plain(changed)
    return rewrite


def _swap_ops(text: str, pairs: Dict[str, str]) -> str:
    return re.sub("|".join(re.escape(k) for k in sorted(pairs, key=len, reverse=True)),
                  lambda m: pairs[m.group()], text)


def _if_rewrite(fn: Callable[[Stmt, Emitter], Optional[str]]) -> Rewrite:
    return lambda s, em: fn(s, em) if s.kind == "if" else None


def _else_always(s: Stmt, em: Emitter) -> Optional[str]:
    if s.other is None or s.other.kind == "if":
        return None
    return f"__l({s.line}); if ({s.cond}) {em.block(s.body)} {em.block(s.other, prefix=f'__l({s.else_line});')}\n"


def _both_branches(s: Stmt, em: Emitter) -> Optional[str]:
    if s.other is None:
        return None
    return f"__l({s.line}); {em.block(s.body)} {em.block(s.other, prefix=f'__l({s.else_line});')}\n"


def _else_if_separate(s: Stmt, em: Emitter) -> Optional[str]:
    if s.other is None or s.other.kind != "if":
        return None
    return f"__l({s.line}); if ({s.cond}) {em.block(s.body)}\n" + em.stmt(s.other)


def _if_is_loop(s: Stmt, em: Emitter) -> Optional[str]:
    if s.other is not None:
        return None
    return f"__l({s.line}); while ({s.cond}) {em.block(s.body)}\n"


def _loop_body_once(s: Stmt, em: Emitter) -> Optional[str]:
    if s.kind == "while":
        return f"__l({s.line}); do {em.block(s.body, prefix=f'__p({s.loop_id});')} while ({s.cond});\n"
    return None


def _do_tests_first(s: Stmt, em: Emitter) -> Optional[str]:
    if s.kind == "do":
        return f"__l({s.line}); while ({s.cond}) {em.block(s.body, prefix=f'__p({s.loop_id});')}\n"
    return None


def _for_is_conditional(s: Stmt, em: Emitter) -> Optional[str]:
    if s.kind != "for":
        return None
    return (f"__l({s.line}); for ({s.init}; {s.cond}; {s.update}) "
            + em.block(s.body, prefix=f"__p({s.loop_id});", suffix="break;") + "\n")


def _for_update_first(s: Stmt, em: Emitter) -> Optional[str]:
    if s.kind != "for" or not s.update:
        return None
    return (f"__l({s.line}); for ({s.init}; {s.cond}; ) "
            + em.block(s.body, prefix=f"__p({s.loop_id});{s.update};") + "\n")


def _outer_loop_once(s: Stmt, em: Emitter) -> Optional[str]:
    if s.kind not in ("for", "while") or s.body is None:
        return None
    body = s.body.items if s.body.kind == "block" else [s.body]
    if not any(x.kind in ("for", "while", "do") for x in body):
        return None
    head = f"for ({s.init}; {s.cond}; {s.update})" if s.kind == "for" else f"while ({s.cond})"
    return f"__l({s.line}); {head} " + em.block(s.body, prefix=f"__p({s.loop_id});", suffix="break;") + "\n"


MUTATIONS: Dict[str, Rewrite] = {
    # assignment models (Dehnadi & Bornat; Ma et al.)
    "AssignmentOppositeDirection": _on_simple(lambda t: (lambda m: f"{m.group(2)} = {m.group(1)}" if m else None)(_VAR_COPY_RE.match(t))),
    "AssignmentEmptiesSource": _on_simple(lambda t: (lambda m: f"{m.group(1)} = {m.group(2)}; {m.group(2)} = 0" if m else None)(_VAR_COPY_RE.match(t))),
    # numeric swap without a temporary, so the statement stays one assignment block
    "AssignmentExchangesValues": _on_simple(lambda t: (lambda m: f"{m.group(1)} = {m.group(1)} + {m.group(2)}; {m.group(2)} = {m.group(1)} - {m.group(2)}; {m.group(1)} = {m.group(1)} - {m.group(2)}" if m else None)(_VAR_COPY_RE.match(t))),
    "AssignmentAddsToTarget": _on_simple(lambda t: (lambda m: f"{m.group(1)} = {m.group(1)} + ({m.group(2)})" if m else None)(_SIMPLE_ASSIGN_RE.match(t))),
    # arithmetic and increments
    "IntegerDivisionGivesFraction": _on_simple(lambda t: t.replace(" / ", " * 1.0 / ") if " / " in t else None),
    "IncrementByTwo": _on_simple(lambda t: re.sub(r"\b(\w+)\s*\+\+|\+\+\s*(\w+)", lambda m: f"{m.group(1) or m.group(2)} += 2", t) if "++" in t else None),
    "PostIncrementAssignsLater": _on_simple(lambda t: (lambda m: f"{m.group(1)} = {m.group(1)} + 1" if m else None)(re.match(r"^(\w+)\s*=\s*\1\s*\+\+$", t))),
    "PrePostIncrementSameValue": _on_simple(lambda t: re.sub(r"=\s*(\w+)\s*\+\+", r"= ++\1", t) if re.search(r"=\s*\w+\s*\+\+", t) else None),
    # conditions
    "OffByOneBound": _on_conditions(lambda c: _swap_ops(c, {"<=": "<", "<": "<=", ">=": ">", ">": ">="}), kinds=("while", "for", "do")),
    "LessGreaterSwapped": _on_conditions(lambda c: _swap_ops(c, {"<=": ">=", ">=": "<=", "<": ">", ">": "<"})),
    "LoopTerminatingCondition": _on_conditions(lambda c: f"!({c})", kinds=("while", "for", "do")),
    # control flow
    "ElseAlwaysExecutes": _if_rewrite(_else_always),
    "BothBranchesExecute": _if_rewrite(_both_branches),
    "MultipleElseIfBranchesRun": _if_rewrite(_else_if_separate),
    "IfIsLoop": _if_rewrite(_if_is_loop),
    "LoopBodyAlwaysOnce": _loop_body_once,
    "DoWhileTestsFirst": _do_tests_first,
    "ForIsConditional": _for_is_conditional,
    "ForUpdateBeforeBody": _for_update_first,
    "OuterLoopIgnored": _outer_loop_once,
}


@lru_cache(maxsize=1)
def get_tracer() -> Tracer:
    return Tracer()
