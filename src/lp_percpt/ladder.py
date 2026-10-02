"""
ladder.py — Step 8: walk a concept's L0-L4 ladder along its next_level edges.

Each level node requires one evidence check (Ladder sheet):
    concept@L1 -> E1   concept@L2 -> E2   concept@L3 -> E3 (+ no boundary misconception held)
    concept@L4 -> E4
The walk starts at concept@L0 and steps up while the next node's requirement
is met. It stops at the first unmet requirement, or one level lower with an
"uncertain" mark when that requirement scores inside the ambiguity band (G15).
A held boundary misconception blocks the step into concept@L3 (G13).
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional, Set

from .evidence import MET, UNCERTAIN

LEVELS = ("L0", "L1", "L2", "L3", "L4")
REQUIRES = {1: "E1", 2: "E2", 3: "E3", 4: "E4"}
CHECK_NAMES = {"E1": "E1 Reference", "E2": "E2 Execution", "E3": "E3 Integration", "E4": "E4 Transfer / debug"}


@dataclass
class WalkResult:
    level: int
    uncertain_toward: Optional[int]
    stop_reason: str
    blocked_by: Set[str]

    @property
    def label(self) -> str:
        return LEVELS[self.level]


def walk(checks: Dict[str, str], held_boundary: Set[str]) -> WalkResult:
    level = 0
    for k in (1, 2, 3, 4):
        check = REQUIRES[k]
        status = checks.get(check)
        if k == 3 and held_boundary and status in (MET, UNCERTAIN):
            return WalkResult(level, None,
                              f"L3 blocked: boundary misconception held ({', '.join(sorted(held_boundary))})",
                              set(held_boundary))
        if status == MET:
            level = k
            continue
        if status == UNCERTAIN:
            return WalkResult(level, k, f"uncertain toward L{k}: {CHECK_NAMES[check]} in the ambiguity band", set())
        return WalkResult(level, None, f"stopped at L{level}: {CHECK_NAMES[check]} not shown", set())
    return WalkResult(4, None, "top of the ladder", set())
