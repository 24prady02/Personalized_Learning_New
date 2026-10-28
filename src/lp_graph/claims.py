"""Claims: check a stated slot against a real (or misinterpreted) run.

Stand-in for ``lp_percpt.claims.check``. ``check(slot, run)`` answers
True (the run confirms the statement), False (the run contradicts it) or
None (the run says nothing about it, or no run is available).

Checkable slots: ``output``, ``compile``, ``crash``, ``value`` (of a code
variable, or none/default for an uninitialised read) and ``runs=endless``.
"""

from __future__ import annotations

import re

from .execution import Run
from .slots import Slot, values_agree

CHECKABLE = frozenset({"output", "compile", "crash", "value", "runs"})


def _norm_out(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().strip('"').strip()).lower()


def _uninit_var(run: Run) -> str | None:
    m = re.search(r"variable (\w+) might not have been initialized", run.error)
    return m.group(1) if m else None


def check(slot: Slot, run: Run) -> bool | None:
    """Does ``run`` confirm (True), contradict (False) or ignore (None) ``slot``?"""
    verdict = _check(slot, run)
    if verdict is None:
        return None
    return (not verdict) if slot.negated else verdict


def _check(slot: Slot, run: Run) -> bool | None:
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
    if name == "output":
        if run.error_kind == "compile":
            return value == ""
        if not run.available:
            return None
        printed = _norm_out(run.output)
        want = _norm_out(value)
        if printed == want:
            return True
        lines = [_norm_out(x) for x in run.output.splitlines() if x.strip()]
        if want and want in lines and len(lines) == 1:
            return True
        return values_agree("output", printed, want)
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
    actual = run.value_of(var)
    if actual is None:
        return None
    return values_agree("value", slot.value, actual)


def contradicted(slots: list[Slot] | tuple[Slot, ...], run: Run) -> list[Slot]:
    """The slots ``run`` contradicts (implied slots included)."""
    return [s for s in slots if s.name in CHECKABLE and check(s, run) is False]


def confirmed(slots: list[Slot] | tuple[Slot, ...], run: Run) -> list[Slot]:
    """The non-implied slots ``run`` confirms."""
    return [s for s in slots if s.name in CHECKABLE and not s.implied and check(s, run) is True]
