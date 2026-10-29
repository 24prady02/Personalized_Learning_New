"""Claims: check a stated slot against a real (or misinterpreted) run.

Stand-in for ``lp_percpt.claims.check``. ``check(slot, run)`` answers
True (the run confirms the statement), False (the run contradicts it) or
None (the run says nothing about it, or no run is available).

Checkable slots:

* ``output`` - the whole output, compared line by line (empty lines kept,
  trailing spaces and commas ignored); ``printed`` - text that appears in
  the output ("it prints A");
* ``trailing_empty_line`` - whether the output ends with an empty line;
* ``value`` - a variable's value, at the code point the clause names
  ("after a = b, a is b") or at the end; the value may be another variable
  (``var:b``): with a change verb ("a becomes b") b's value before the code,
  else b's value at the same point;
* ``expr`` - an expression the student evaluated ("9 % 5 ... is 4"),
  evaluated with Java's integer rules;
* ``compile``, ``crash``, ``runs=endless``.

A hypothetical slot ("with %.3f it would print 3.142") is never checked
against the real run: ``check`` returns None unless the run passed is the
variant run of the stated change.
"""

from __future__ import annotations

import math
import re

from . import lexicon
from .execution import Run
from .slots import Slot, values_agree

CHECKABLE = frozenset({"output", "printed", "compile", "crash", "value", "runs", "expr",
                       "trailing_empty_line"})


def _norm_line(text: str) -> str:
    return re.sub(r"[\s,]+", " ", text.strip().strip('"').strip()).strip().lower()


def _lines(output: str) -> list[str]:
    out = output.replace("\r\n", "\n")
    if out.endswith("\n"):
        out = out[:-1]
    return [_norm_line(x) for x in out.split("\n")] if out else []


def _uninit_var(run: Run) -> str | None:
    m = re.search(r"variable (\w+) might not have been initialized", run.error)
    return m.group(1) if m else None


def check(slot: Slot, run: Run, variant: bool = False) -> bool | None:
    """Does ``run`` confirm (True), contradict (False) or ignore (None) ``slot``?"""
    if slot.hypothetical and not variant:
        return None
    verdict = _check(slot, run)
    if verdict is None:
        return None
    return (not verdict) if slot.negated else verdict


def _check(slot: Slot, run: Run) -> bool | None:
    if slot.name == "expr":
        return check_expr(slot)
    known = run.available or run.error_kind == "compile"
    if not known:
        return None
    name, value = slot.name, slot.value
    if name == "compile":
        if value == "compile_error":
            return run.error_kind == "compile"
        if value == "compiles":
            return run.error_kind != "compile"
        return None
    if name in ("output", "printed"):
        if run.error_kind == "compile":
            return value == ""
        if not run.available:
            return None
        got = _lines(run.output)
        want = [_norm_line(x) for x in value.split("\n")] if value else []
        if name == "output":
            if got == want:
                return True
            if len(want) == 1 and " ".join(x for x in got if x) == want[0]:
                return True  # one line written for a short multi-line output
            return False
        flat = " ".join(x for x in got if x)
        return bool(want) and all(re.search(rf"(?<![\w.]){re.escape(w)}(?![\w.])", flat) or w in flat
                                  for w in want if w)
    if name == "trailing_empty_line":
        if not run.available or run.error_kind:
            return None
        ends_empty = run.output.replace("\r\n", "\n").endswith("\n\n")
        return ends_empty == (value == "present")
    if name == "crash":
        if run.error_kind == "compile" or not run.available:
            return None
        return (run.error_kind == "run") == (value == "run_error")
    if name == "runs" and value == "endless":
        return run.timed_out if run.available else None
    if name == "value":
        return _check_value(slot, run)
    return None


def _check_value(slot: Slot, run: Run) -> bool | None:
    var = slot.subject[4:] if slot.subject and slot.subject.startswith("var:") else None
    uninit = _uninit_var(run)
    if slot.value in ("none", "default", "garbage"):
        if uninit is None or (var and var != uninit):
            return None
        return slot.value == "none"
    if var is None:
        return None
    if uninit == var:
        return False  # the variable has no value at all
    point = slot.get("point")
    if point == "mid":
        return None  # a value inside a loop pass: no snapshot to check it against
    if slot.get("verb") in ("starts at", "starts as"):
        actual = run.initial(var)
    else:
        actual = run.value_after(var, int(point)) if point else run.value_of(var)
    if actual is None:
        return None
    want = slot.value
    if want.startswith(("all:", "list:")):
        items = re.findall(r"-?\d+(?:\.\d+)?", actual)
        if not items or not actual.startswith("["):
            return None
        if want.startswith("all:"):
            return all(float(x) == float(want[4:]) for x in items)
        wanted = want[5:].split(",")
        return len(wanted) == len(items) and all(abs(float(a) - float(b)) < 1e-9 for a, b in zip(wanted, items))
    if want.startswith("var:"):
        other = want[4:]
        if slot.get("verb") in lexicon.CHANGE_VERBS:
            ref = run.initial(other)
        else:
            ref = run.value_after(other, int(point)) if point else run.value_of(other)
        if ref is None:
            return None
        return values_agree("value", actual, ref)
    return values_agree("value", want, actual)


def evaluate(expr: str) -> str | None:
    """Value of ``a op b`` with Java semantics (int division truncates, % keeps
    the dividend's sign)."""
    m = re.fullmatch(r"\s*(-?\d+(?:\.\d+)?)\s*(%|/|\*|\+|-|>=|<=|==|!=|>|<)\s*(-?\d+(?:\.\d+)?)\s*", expr)
    if not m:
        return None
    a_s, op, b_s = m.groups()
    is_int = "." not in a_s and "." not in b_s
    a, b = (int(a_s), int(b_s)) if is_int else (float(a_s), float(b_s))
    if op in (">=", "<=", "==", "!=", ">", "<"):
        res = {">=": a >= b, "<=": a <= b, "==": a == b, "!=": a != b, ">": a > b, "<": a < b}[op]
        return "true" if res else "false"
    if op in ("/", "%") and b == 0:
        return None
    if op == "/":
        v = math.trunc(a / b) if is_int else a / b
    elif op == "%":
        v = int(math.fmod(a, b)) if is_int else math.fmod(a, b)
    else:
        v = {"*": a * b, "+": a + b, "-": a - b}[op]
    return str(v)


def check_expr(slot: Slot) -> bool | None:
    v = evaluate(slot.get("expr") or (slot.subject or "")[5:])
    if v is None:
        return None
    return values_agree("value", slot.value, v) if v not in ("true", "false") else slot.value == v


def contradicted(slots: list[Slot] | tuple[Slot, ...], run: Run) -> list[Slot]:
    """The slots ``run`` contradicts (implied slots included, hypotheticals never)."""
    return [s for s in slots if s.name in CHECKABLE and check(s, run) is False]


def confirmed(slots: list[Slot] | tuple[Slot, ...], run: Run) -> list[Slot]:
    """The non-implied slots ``run`` confirms."""
    return [s for s in slots if s.name in CHECKABLE and not s.implied and check(s, run) is True]
