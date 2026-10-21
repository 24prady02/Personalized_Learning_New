"""
claims.py — the checkable claims in a student's reasoning (evidence step).

A clause is read for claims that a run of the code can decide:

    value    "x is 6", "a = 20", "a[0] = 9", "total ends as 15"
    output   "it prints 8, 10, 12", a bare list "81 79 77"
    count    "the loop runs 5 times", "the body never runs"
    endless  "the loop never ends"
    crash    "it crashes", "throws an exception"
    lines    "lines 1, 3, 4 and 6 run", "line 2 is skipped"
    expr     "7 / 2 gives 3.5", "(int) 3.7 is 3"  (literal expressions, evaluated in Java)

check() decides a claim against one run (the real one, or a misconception's
mutant): True, False, or None when the run cannot decide it.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set

from .execution import Run

_WORDNUM = {"zero": 0, "never": 0, "once": 1, "one": 1, "twice": 2, "two": 2, "three": 3, "four": 4, "five": 5,
            "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10}
_NUMTOK = r"(?:-?\d+(?:\.\d+)?)"
_VALUE = rf"({_NUMTOK}|true|false|\[[^\]]*\]|\"[^\"]*\"|'.')"
_BIND_RE = re.compile(rf"\b([A-Za-z_]\w*(?:\[\d+\])?)\s*(?:=|==|is|becomes|equals|ends as|ends at|ends up as|is still|stays|holds|gets|will be|is now|turns into|goes to|changes to)\s*{_VALUE}",
                      re.I)
_FINAL_RE = re.compile(r"\b(final|finally|in the end|at the end|after the (loop|last line|switch|code)|ends|new values?|afterwards)\b", re.I)
_SAYS_OUTPUT_RE = re.compile(r"\b(prints?|printed|outputs?|displays?|shows?)\b", re.I)
_LOOP_WORD_RE = re.compile(r"\b(loop|body|for|while|repeats?|iterations?|pass(es)?|times round|inner|outer)\b", re.I)
_COUNT_RE = re.compile(r"\b(?:runs|repeats|loops|iterates|executes|goes round|goes around|is executed|is repeated)\s+"
                       r"(\d+|zero|once|twice|one|two|three|four|five|six|seven|eight|nine|ten)\b(?:\s*times)?"
                       r"|\b(\d+|one|two|three|four|five|six|seven|eight|nine|ten)\s+(?:times|passes|iterations)\b"
                       r"|\b(never runs|does not run at all|doesn't run at all|runs zero times|is skipped entirely)\b", re.I)
_ENDLESS_RE = re.compile(r"\b(never (ends|stops|terminates|finishes)|runs forever|loops forever|goes on forever|infinite loop|keeps (going|running) forever)\b", re.I)
_NOT_ENDLESS_RE = re.compile(r"\b(not (an )?infinite|does(n't| not) (run|loop) forever|(will|does) (end|stop|terminate))\b", re.I)
_CRASH_RE = re.compile(r"\b(crash(es|ed)?|throws?|exception|out of bounds|run-?time error)\b", re.I)
_HYPOTHETICAL_RE = re.compile(r"\b(if|would|could|might|unless|otherwise|without)\b", re.I)
_LINES_RE = re.compile(r"\blines?\s+((?:\d+\s*(?:,|and|then|->|→|to)?\s*)+)", re.I)
_SKIPPED_RE = re.compile(r"\b(skipped|never runs|does(n't| not) run|not run|is not executed)\b", re.I)
_EXPR_RE = re.compile(r"((?:\(\s*(?:int|double|long|char)\s*\)\s*)?\(?\s*-?\d+(?:\.\d+)?(?:\s*[-+*/%]\s*\(?\s*-?\d+(?:\.\d+)?\s*\)?)+\s*\)?"
                      r"|\(\s*(?:int|double|long|char)\s*\)\s*-?\d+(?:\.\d+)?)"
                      rf"\s*(?:is|=|==|gives|equals|evaluates to|returns|makes|comes out as|becomes)\s*{_VALUE}", re.I)
_NUM_RE = re.compile(r"(?<![\w.])-?\d+(?:\.\d+)?(?![\w.]*\w)")


@dataclass
class Claim:
    kind: str
    text: str
    var: str = ""
    value: str = ""
    final: bool = False
    values: List[str] = field(default_factory=list)
    n: int = 0
    lines: List[int] = field(default_factory=list)
    negated: bool = False
    expr: str = ""
    note: str = ""              # set when a compile probe decided the claim (evidence._probe_claims)

    def describe(self) -> str:
        return {"value": f"{self.var} = {self.value}" + (" (final)" if self.final else ""),
                "output": "prints " + " ".join(self.values),
                "count": f"runs {self.n} times", "endless": "never ends",
                "crash": "crashes", "lines": ("line(s) " + ", ".join(map(str, self.lines))
                                              + (" do not run" if self.negated else " run")),
                "expr": f"{self.expr} = {self.value}"}.get(self.kind, self.kind)


def _num(v: str) -> str:
    v = v.strip().strip('"').strip("'")
    try:
        f = float(v)
        return str(int(f)) if f == int(f) and "e" not in v.lower() else str(f)
    except ValueError:
        return v


def asks_final(question: str) -> bool:
    """The question asks for values after the code ran ('the new values of a and b')."""
    return bool(_FINAL_RE.search(question or ""))


def extract(text: str, code_vars: Set[str], letters_in_output: bool = False,
            final_default: bool = False) -> List[Claim]:
    """Claims a single clause makes. code_vars: names the code uses (value claims
    are only taken for these, so 'it is 3 times' is not read as a variable).
    final_default: the question asks for final values, so a bare 'a = 20' is one."""
    out: List[Claim] = []
    final = final_default or bool(_FINAL_RE.search(text))
    binds = [m for m in _BIND_RE.finditer(text) if m.group(1).split("[")[0] in code_vars]
    last = {m.group(1): m for m in binds}                  # the last value stated for each variable
    for m in binds:
        name, value = m.group(1), m.group(2)
        # "at i = 9 ..." / "when x is 3": a moment of the run, not a result
        moment = bool(re.search(r"\b(at|when|while|whenever|once|until)\s+$", text[max(0, m.start() - 9):m.start()], re.I))
        # in a sequence ("x is 6, then ... x is 7") only the last value is the final one
        out.append(Claim("value", text, var=name, value=value,
                         final=final and not moment and last[name] is m))
    for expr, value in _EXPR_RE.findall(text):
        out.append(Claim("expr", text, expr=expr.strip(), value=value))
    nums = _NUM_RE.findall(text)
    stripped = re.sub(r"\b(and|then|so|it|the|output|is)\b", "", text, flags=re.I)
    bare_list = len(nums) >= 2 and not re.search(r"[A-Za-z]{2,}", re.sub(r"\b(and|then)\b", "", stripped))
    code_like = bool(re.search(r"[;{}?]|==|\b(int|double|String|boolean|for|while|if)\b\s*[\w(]", text))
    if (_SAYS_OUTPUT_RE.search(text) or bare_list) and not code_like and not any(c.kind == "value" for c in out):
        vals = [n for n in nums if not re.search(rf"\blines?\s+{re.escape(n)}\b", text)]
        vals += re.findall(r'"([^"]+)"', text)
        if letters_in_output:
            vals += re.findall(r"\b([A-Z])\b", text)
        if vals and not _HYPOTHETICAL_RE.search(text):
            out.append(Claim("output", text, values=vals))
    if _LOOP_WORD_RE.search(text) and not re.search(r"\bif\b", text, re.I):
        for m in _COUNT_RE.finditer(text):
            word = (m.group(1) or m.group(2) or "never").lower()
            n = int(word) if word.isdigit() else _WORDNUM.get(word.split()[0], 0)
            if not _HYPOTHETICAL_RE.search(text):
                out.append(Claim("count", text, n=n))
            break
    if _ENDLESS_RE.search(text) and not _NOT_ENDLESS_RE.search(text) and not _HYPOTHETICAL_RE.search(text):
        out.append(Claim("endless", text))
    if _CRASH_RE.search(text) and not _HYPOTHETICAL_RE.search(text) and not re.search(r"\b(no|not|never|doesn't|won't)\b", text, re.I):
        out.append(Claim("crash", text))
    m = _LINES_RE.search(text)
    if m:
        lines = [int(x) for x in re.findall(r"\d+", m.group(1))]
        if lines:
            out.append(Claim("lines", text, lines=lines, negated=bool(_SKIPPED_RE.search(text))))
    return out


_ASKS_OUTPUT_RE = re.compile(r"\b(what is printed|what does .{0,60}\b(print|show|output)|give the .{0,30}\b(lines?|output) printed|what is the (exact )?output)\b", re.I)
_EMPTY_RE = re.compile(r"^(an? )?(empty( string)?|nothing|blank|\"\")$", re.I)
_OUT_TOKEN_RE = re.compile(r'"[^"]+"|\[[A-Z]@|(?<![\w.])-?\d+(?:\.\d+)?(?![\w.]*\w)|\b[A-Z]\d*\b|\b[A-Za-z]+\d+\b')


def extract_answer(text: str, asked: str, code_vars: Set[str]) -> List[Claim]:
    """Claims a clause makes only as an answer to the part asked:
    "What are age, rest and name?" -> "42, an empty string, and "Ann Lee"" states
    age = 42, rest = "" and name = "Ann Lee" (final values, in the order asked);
    "What is printed?" -> "67, a tab, C" states that 67 and C are printed."""
    if not asked or _HYPOTHETICAL_RE.search(text):
        return []
    asked_vars = [w for w in dict.fromkeys(re.findall(r"\b[A-Za-z_]\w*\b", asked)) if w in code_vars]
    items = [p.strip(" .") for p in re.split(r",\s*(?:and\s+)?|\s+and\s+|;\s*", text) if p.strip(" .")]
    if len(asked_vars) >= 2 and len(items) == len(asked_vars) and not any(
            re.search(rf"\b{re.escape(v)}\b", text) for v in asked_vars):
        out = []
        for var, item in zip(asked_vars, items):
            if _EMPTY_RE.match(item):
                value = '""'
            elif re.fullmatch(_VALUE, item, re.I):
                value = item
            else:
                return []
            out.append(Claim("value", text, var=var, value=value, final=True))
        return out
    # an output answer is a list ("67, a tab, C"), not prose that happens to hold numbers
    prose = [w for w in re.findall(r"\b[a-z]{2,}\b", re.sub(r'"[^"]*"', "", text))
             if w not in ("an", "and", "then", "tab", "space", "newline", "line", "lines", "the", "it", "prints",
                          "about", "empty", "string", "nothing")]
    if _ASKS_OUTPUT_RE.search(asked) and len(prose) <= 1:
        vals = [t.strip('"') for t in _OUT_TOKEN_RE.findall(text)]
        # "A" / "I" followed by a word are an article / a pronoun, not output
        vals = [v for v in vals if v not in ("I", "A") or not re.search(rf"\b{v}\s+[a-z]", text)]
        if vals:
            return [Claim("output", text, values=vals)]
    return []


def check(c: Claim, run: Run, evaluated: Optional[Dict[str, str]] = None) -> Optional[bool]:
    if c.kind == "expr":
        got = (evaluated or {}).get(c.expr)
        return None if got is None else _num(got) == _num(c.value)
    if c.kind == "value":
        base, _, idx = c.var.partition("[")
        seq = run.values.get(base)
        if not seq:
            return None
        if idx:                                         # a[0]: element of the array's last value
            i = int(idx.rstrip("]"))
            last = [x.strip() for x in seq[-1].strip("[]").split(",")]
            return None if i >= len(last) else _num(last[i]) == _num(c.value)
        if c.final:
            return _num(seq[-1]) == _num(c.value)
        return _num(c.value) in {_num(v) for v in seq}
    if c.kind == "output":
        out = run.output
        printed = {_num(n) for n in _NUM_RE.findall(out)}
        for v in c.values:
            if re.fullmatch(r"-?\d+(?:\.\d+)?", v):
                if _num(v) not in printed:
                    return False
            elif v not in out:
                return False
        return True
    if c.kind == "count":
        if not run.passes and run.error != "timeout":
            return c.n == 0 if run.lines else None
        return c.n in run.passes.values() or (c.n == 0 and len(run.passes) == 0)
    if c.kind == "endless":
        return run.error == "timeout"
    if c.kind == "crash":
        return bool(run.error) and run.error != "timeout"
    if c.kind == "lines":
        ran = set(run.lines)
        if c.negated:
            return not any(n in ran for n in c.lines)
        if len(c.lines) >= 2:                          # a list of the lines that run: must be all of them
            return set(c.lines) == ran
        return all(n in ran for n in c.lines)
    return None
