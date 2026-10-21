"""
ladder.py — Step 8: the level of a prompt on a concept's L0-L4 ladder.

Each concept -> level has_level edge of the graph lists the ways an answer
shows that level, and each check stands for the ways of one level:
    E1 -> L1 ways (names_the_element, states_the_rule)
    E2 -> L2 ways (line_by_line_trace, output_prediction, one_step_execution)
    E3 -> L3 ways (relation_to_neighbour, purpose_of_the_whole)
    E4 -> L4 ways (predict_a_change, diagnose_an_error, transfer_to_a_new_program)
The prompt is at the highest level whose way it shows: an answer that predicts
a change or diagnoses an error is L4 without also retracing the code. An L0 way
(a held misconception, an everyday reading, an uneven trace) puts the prompt at
L0 unless it also shows a correct way above L1 (G12 then applies). A level
whose check scores in the ambiguity band above the reached level marks the
result "uncertain toward" it (G15). A held boundary misconception caps the
prompt below L3 (G13).
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


def walk(checks: Dict[str, str], held_boundary: Set[str], ways: Optional[Dict[int, str]] = None,
         l0_way: Optional[str] = None) -> WalkResult:
    """ways: level -> the way shown for it (for the reason text); l0_way: the
    L0 way the prompt shows, if any."""
    ways = ways or {}
    met = [k for k in (1, 2, 3, 4) if checks.get(REQUIRES[k]) == MET]
    level = max(met, default=0)
    if l0_way and (l0_way == "inconsistent_trace" or level <= 1):
        return WalkResult(0, None, f"L0 way shown: {l0_way}", set())
    if level >= 3 and held_boundary:
        return WalkResult(max((k for k in met if k < 3), default=0), None,
                          f"L3 blocked: boundary misconception held ({', '.join(sorted(held_boundary))})",
                          set(held_boundary))
    shown = (f"L{level} way shown: {ways[level]}" if level in ways
             else f"L{level}: {CHECK_NAMES[REQUIRES[level]]} met" if level else "no way shown")
    unsure = [k for k in (1, 2, 3, 4) if k > level and checks.get(REQUIRES[k]) == UNCERTAIN]
    if unsure:
        k = unsure[0]
        return WalkResult(level, k, f"{shown}; uncertain toward L{k}: {CHECK_NAMES[REQUIRES[k]]} in the ambiguity band",
                          set())
    if level == 4:
        return WalkResult(4, None, f"{shown} (top of the ladder)", set())
    return WalkResult(level, None, f"{shown}; no L{level + 1} way shown", set())
