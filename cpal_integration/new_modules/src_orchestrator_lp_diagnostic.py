"""
LP Diagnostic - CPAL Stage 1.

Runs three jobs in sequence (from Part 3 of the methodology document):

  1. Wrong-model identification: match student question text against the
     documented conversation signals for the identified concept.
  2. LP level classification: classify the response on the two rubric
     dimensions - logical_step (can the student name the distinction/rule?)
     and logical_step_detail (can they articulate the execution mechanism?).
  3. Plateau check: if current_lp_level == L2 AND lp_streak >= 2 on this
     concept, the plateau_flag fires and plateau_intervention is set to
     trace_scaffold. This flag overrides all downstream intervention
     selection (Stage 2 respects it unconditionally).

The output is an lp_diagnostic object that threads through all five CPAL
stages - Stage 2 (intervention selection) uses it to filter the valid
intervention set by LP level, Stage 3 (prompt builder) uses it to fill the
LP-1/LP-2/LP-3 prompt sections, Stage 4 (post-reply) uses it as the baseline
for delta_lp computation, and Stage 5 (persistence) reads and writes its
fields in the Student Knowledge Graph.

Grounded in: mental_models_cpal_methodology_revised.docx, Part 3 Stage 1;
with the LP-rubric framing following the Jin et al. 2019 / 2025 tradition
of scoring responses on both rule-level and mechanism-level evidence, and
the plateau rule motivated by Chi et al. 1989, 1994 and Renkl 2002 (stalled
learners need mechanism-level scaffolding rather than more rule-level
exposition).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional
import re

from src.knowledge_graph.mental_models import (
    MentalModelsCatalogue,
    WrongModelMatch,
    get_catalogue,
)


# -- LP level constants ---------------------------------------------------

LP_L1 = "L1"   # heuristic - sees symptom, no rule, no mechanism
LP_L2 = "L2"   # qualitative - names the rule, cannot articulate the mechanism
LP_L3 = "L3"   # measurable - articulates the execution-level mechanism
LP_L4 = "L4"   # scientific - extends mechanism to novel/unseen cases

LP_ORDER = [LP_L1, LP_L2, LP_L3, LP_L4]
LP_INDEX = {lvl: i for i, lvl in enumerate(LP_ORDER)}


# -- Plateau rule ---------------------------------------------------------

#: Plateau triggers if the student has been at L2 for this many sessions on
#: the same concept without advancing. Motivated by Chi et al. (1989, 1994)
#: and Renkl (2002): stalled learners stop benefiting from more rule-level
#: exposition and need mechanism-level scaffolding (trace walkthrough).
L2_PLATEAU_THRESHOLD = 2

#: The intervention that the plateau flag forces. Methodology doc, Stage 2.
PLATEAU_INTERVENTION = "trace_scaffold"


# -- Diagnostic outputs ---------------------------------------------------

@dataclass
class LPDiagnostic:
    """
    The full Stage 1 diagnostic object that threads through the pipeline.

    Fields are grouped by which CPAL stage populates or consumes them:
      Stage 1 populates all of these.
      Stage 2 reads plateau_flag, plateau_intervention, current_lp_level.
      Stage 3 reads wrong_model_*, lp_rubric_*, current_lp_level, target_lp_level.
      Stage 4 reads current_lp_level as the pre-baseline for delta_lp.
      Stage 5 persists all of these to the Student Knowledge Graph.
    """
    # Identity
    concept: str
    student_id: str

    # Wrong-model identification
    wrong_model_id: Optional[str] = None
    wrong_model_description: Optional[str] = None
    wrong_model_origin: Optional[str] = None
    matched_signal: Optional[str] = None
    match_score: float = 0.0

    # LP-level classification
    current_lp_level: str = LP_L1
    logical_step: bool = False            # can name the distinction/rule
    logical_step_detail: bool = False     # can articulate the mechanism
    lp_signals_detected: List[str] = field(default_factory=list)
    lp_streak: int = 0                    # consecutive sessions at this level on this concept

    # Plateau gate
    plateau_flag: bool = False
    plateau_intervention: Optional[str] = None

    # Target (one level above current, capped at L4)
    target_lp_level: str = LP_L2
    transition: str = "L1->L2"

    # Rubric definitions (populated from catalogue for prompt context)
    lp_rubric_current: Optional[str] = None
    lp_rubric_target: Optional[str] = None
    expert_benchmark_key_ideas: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict:
        """Serialisation form for persistence and prompt-building."""
        return {
            "concept": self.concept,
            "student_id": self.student_id,
            "wrong_model_id": self.wrong_model_id,
            "wrong_model_description": self.wrong_model_description,
            "wrong_model_origin": self.wrong_model_origin,
            "matched_signal": self.matched_signal,
            "match_score": self.match_score,
            "current_lp_level": self.current_lp_level,
            "logical_step": self.logical_step,
            "logical_step_detail": self.logical_step_detail,
            "lp_signals_detected": list(self.lp_signals_detected),
            "lp_streak": self.lp_streak,
            "plateau_flag": self.plateau_flag,
            "plateau_intervention": self.plateau_intervention,
            "target_lp_level": self.target_lp_level,
            "transition": self.transition,
            "lp_rubric_current": self.lp_rubric_current,
            "lp_rubric_target": self.lp_rubric_target,
            "expert_benchmark_key_ideas": list(self.expert_benchmark_key_ideas),
        }


# -- LP classifier --------------------------------------------------------

#: Lexical cues for logical_step_detail - the mechanism-level vocabulary.
#: A reply containing any of these is treated as evidence the student can
#: trace the execution-level mechanism (L3 criterion).
#: Grounded in the L3 rubric rows across all 20 concepts in Part 2.
_MECHANISM_WORDS = frozenset({
    # execution verbs
    "trace", "traces", "tracing",
    "evaluate", "evaluates", "evaluated", "evaluation",
    "execute", "executes", "executed",
    "allocate", "allocates", "allocated", "allocation",
    "dereference", "dereferences", "dereferencing",
    # memory/heap language
    "heap", "stack", "address", "reference",
    "slot", "frame", "buffer",
    # mechanism connectives
    "because", "therefore",
    # causal/sequential chains
    "then", "step", "step-by-step",
    # compiler/runtime distinction
    "compile-time", "compile", "runtime",
    "static", "dynamic",
    # type-system mechanism
    "coerce", "coercion", "promote", "promotion",
    "cast", "casting",
    # loop mechanism
    "iteration", "iterations", "invariant",
    # control-flow mechanism
    "path", "paths", "branch", "branches",
    # object-system mechanism
    "instance", "class-level", "object-level",
})

#: Lexical cues for logical_step - the student at least names the distinction.
#: These are rule-level references, not mechanism descriptions.
_RULE_WORDS = frozenset({
    "use", "need", "should", "must",
    "equals", "cast", "null", "new",
    "length", "length-1",
    "priming", "sentinel",
    "wrapper", "integer",
    "declare", "initialise", "initialize",
    "static", "instance",
})

#: Hedging cues - presence downgrades confidence in logical_step_detail even
#: if mechanism words appear. "something about how" without concrete mechanism
#: is L2, not L3 (Jin et al. LP-scoring convention).
_HEDGE_PATTERNS = (
    re.compile(r"\bsomething about\b"),
    re.compile(r"\bsome\s?how\b"),
    re.compile(r"\bmaybe\b"),
    re.compile(r"\bi think\b"),
    re.compile(r"\bnot sure\b"),
    re.compile(r"\bi guess\b"),
    re.compile(r"\bkind of\b"),
    re.compile(r"\bsort of\b"),
)

#: Transfer/generalisation cues - evidence of L4 reasoning (spontaneous
#: generalisation to novel cases, connections to design rationale).
_TRANSFER_PATTERNS = (
    re.compile(r"\bthis applies to\b"),
    re.compile(r"\bsame principle\b"),
    re.compile(r"\bin general\b"),
    re.compile(r"\bwhy java chose\b"),
    re.compile(r"\bdesign choice\b"),
    re.compile(r"\bjust like\b"),
    re.compile(r"\balso works for\b"),
)


def classify_lp_level(text: str) -> Dict:
    """
    Classify a piece of student text on the L1-L4 rubric using two flags.

    Returns:
      {
        "level": "L1"|"L2"|"L3"|"L4",
        "logical_step": bool,
        "logical_step_detail": bool,
        "signals_detected": [str, ...],   # debug trail
      }

    Rules (from the methodology doc, Part 3 Stage 1):
      - No rule words, no mechanism words -> L1 (pure symptom description).
      - Rule words present, mechanism words absent or hedged -> L2.
      - Mechanism words present without hedging -> L3.
      - Mechanism + transfer/generalisation cues -> L4.
    """
    if not text:
        return {
            "level": LP_L1,
            "logical_step": False,
            "logical_step_detail": False,
            "signals_detected": [],
        }

    t = text.lower()
    t_words = set(re.findall(r"[a-z][a-z\-]*", t))

    mechanism_hits = sorted(w for w in _MECHANISM_WORDS if w in t_words)
    rule_hits      = sorted(w for w in _RULE_WORDS      if w in t_words)
    hedged         = any(p.search(t) for p in _HEDGE_PATTERNS)
    transfer       = any(p.search(t) for p in _TRANSFER_PATTERNS)

    signals: List[str] = []
    if rule_hits:      signals.append(f"rule_words={rule_hits}")
    if mechanism_hits: signals.append(f"mechanism_words={mechanism_hits}")
    if hedged:         signals.append("hedged=True")
    if transfer:       signals.append("transfer=True")

    logical_step = bool(rule_hits) or bool(mechanism_hits)

    # Mechanism-level detail requires real mechanism vocabulary that isn't
    # undercut by hedging. A single mechanism word with heavy hedging is L2.
    strong_mechanism = len(mechanism_hits) >= 2 or (
        len(mechanism_hits) >= 1 and not hedged
    )
    logical_step_detail = strong_mechanism

    # Level ladder
    if logical_step_detail and transfer:
        level = LP_L4
    elif logical_step_detail:
        level = LP_L3
    elif logical_step:
        level = LP_L2
    else:
        level = LP_L1

    return {
        "level": level,
        "logical_step": logical_step,
        "logical_step_detail": logical_step_detail,
        "signals_detected": signals,
    }


# -- Stage 1 orchestrator -------------------------------------------------

class LPDiagnostician:
    """
    CPAL Stage 1 orchestrator.

    Usage inside process_session:

        diag = lp_diagnostician.diagnose(
            student_id=student_id,
            concept=concept,
            question_text=session_data.get("question", ""),
            stored_lp_level=stored_lp_level,   # from Student KG, may be None on first session
            stored_lp_streak=stored_lp_streak, # from Student KG, 0 on first session
        )
        # diag is an LPDiagnostic, attach to the session context.
    """

    def __init__(self, catalogue: Optional[MentalModelsCatalogue] = None):
        self.catalogue = catalogue or get_catalogue()

    def diagnose(self,
                 student_id: str,
                 concept: str,
                 question_text: str,
                 stored_lp_level: Optional[str] = None,
                 stored_lp_streak: int = 0) -> LPDiagnostic:
        """
        Run the three Stage 1 jobs and produce an LPDiagnostic.

        Args:
          student_id:        the student's stable ID
          concept:           the concept being diagnosed (must be in catalogue)
          question_text:     the natural-language question the student just asked
          stored_lp_level:   the level this student was last assessed at on this
                             concept (from the Student KG). None means treat as L1.
          stored_lp_streak:  how many consecutive sessions the student has been
                             at stored_lp_level on this concept. 0 on first touch.
        """
        diag = LPDiagnostic(concept=concept, student_id=student_id)

        # -- Job 1: Wrong-model identification ----------------------------
        match: WrongModelMatch = self.catalogue.match_wrong_model(
            question_text=question_text,
            concept_id=concept,
        )
        diag.wrong_model_id          = match.wrong_model_id
        diag.wrong_model_description = match.wrong_belief
        diag.wrong_model_origin      = match.origin
        diag.matched_signal          = match.matched_signal
        diag.match_score             = match.match_score

        # -- Job 2: LP level classification -------------------------------
        clf = classify_lp_level(question_text)
        current_lp_level = clf["level"]
        diag.logical_step        = clf["logical_step"]
        diag.logical_step_detail = clf["logical_step_detail"]
        diag.lp_signals_detected = clf["signals_detected"]

        # Blend current-session classification with stored history. The
        # methodology doc treats both as inputs: current session is fresh
        # evidence, stored level is the prior. We take the MAX of current
        # and stored as the working level - this protects against a single
        # sloppy question wiping out established mastery, while still
        # letting the student advance on fresh L3 evidence.
        if stored_lp_level in LP_INDEX:
            stored_idx = LP_INDEX[stored_lp_level]
            current_idx = LP_INDEX[current_lp_level]
            if stored_idx > current_idx:
                current_lp_level = stored_lp_level
        diag.current_lp_level = current_lp_level

        # lp_streak: if the current-session level equals the stored level,
        # increment; otherwise reset to 0 (advancement/regression both
        # break the streak).
        if stored_lp_level == current_lp_level:
            diag.lp_streak = stored_lp_streak + 1
        else:
            diag.lp_streak = 0

        # -- Job 3: Plateau check -----------------------------------------
        # Methodology doc Stage 1: if L2 and streak >= 2, fire plateau_flag
        # and force trace_scaffold. The flag overrides all downstream
        # intervention selection (Stage 2).
        if diag.current_lp_level == LP_L2 and diag.lp_streak >= L2_PLATEAU_THRESHOLD:
            diag.plateau_flag = True
            diag.plateau_intervention = PLATEAU_INTERVENTION

        # -- Target level + rubric context --------------------------------
        cur_idx = LP_INDEX[diag.current_lp_level]
        target_idx = min(cur_idx + 1, len(LP_ORDER) - 1)
        diag.target_lp_level = LP_ORDER[target_idx]
        diag.transition = f"{diag.current_lp_level}->{diag.target_lp_level}"

        rubric = self.catalogue.get_lp_rubric(concept) or {}
        diag.lp_rubric_current = rubric.get(diag.current_lp_level)
        diag.lp_rubric_target  = rubric.get(diag.target_lp_level)

        # Expert benchmark key ideas: pull the L3 rubric row and split on
        # sentence boundaries. These are the "key ideas that must all be
        # present in a correct L3 explanation" the Stage 3 prompt needs.
        l3 = rubric.get(LP_L3, "") or ""
        diag.expert_benchmark_key_ideas = [
            s.strip() for s in re.split(r"(?<=[.!?])\s+", l3) if s.strip()
        ]

        return diag


# -- Stage 2 helper: LP-level validity gate -------------------------------
# Methodology doc, Part 3 Stage 2: at each LP level, only a subset of
# interventions is pedagogically appropriate. Stage 2 uses this table to
# filter the RNN/recommender output before picking the top intervention.
#
#   L1 students need structure: worked example, reduce challenge, model
#     explanation, Socratic prompt, misconception correction, attribution
#     reframe (psychological safety).
#   L2 students need the mechanism surfaced: trace scaffold (the
#     plateau-break default), Socratic prompt, misconception correction,
#     worked example, model explanation.
#   L3 students are ready for application: transfer prompt/task,
#     increase challenge, Socratic prompt.
#   L4 students are ready for extension: transfer task/prompt, increase
#     challenge.
LP_VALID_INTERVENTIONS: Dict[str, List[str]] = {
    LP_L1: [
        "worked_example", "reduce_challenge", "socratic_prompt",
        "misconception_correct", "model_explanation",
        "attribution_reframe",
    ],
    LP_L2: [
        "trace_scaffold", "socratic_prompt", "misconception_correct",
        "worked_example", "model_explanation",
    ],
    LP_L3: [
        "transfer_prompt", "transfer_task", "increase_challenge",
        "socratic_prompt",
    ],
    LP_L4: [
        "transfer_prompt", "transfer_task", "increase_challenge",
    ],
}


def filter_interventions_by_lp(ranked, lp_level: str):
    """Filter a ranked list of (intervention_type, score) pairs through
    the LP-level validity gate. Returns filtered list in the same order.
    If nothing survives (e.g. all candidates were outside the LP-valid
    set), returns the original list (fail-open — the caller decides).
    """
    allowed = set(LP_VALID_INTERVENTIONS.get(lp_level, []))
    if not allowed:
        return ranked
    filtered = [(t, s) for t, s in ranked if t in allowed]
    return filtered if filtered else ranked


# -- Stage 4 helper: post-reply classification ---------------------------

def classify_post_reply(reply_text: str):
    """Classify a student's reply AFTER the tutor's response.

    This is the Stage 4 post-reply scoring the methodology calls out —
    it produces (logical_step, logical_step_detail, post_lp_level) which
    the orchestrator uses to compute delta_lp = post - pre. Thin wrapper
    around classify_lp_level so Stage 4 doesn't need to know about the
    classifier's internal dict shape.
    """
    clf = classify_lp_level(reply_text or "")
    return bool(clf["logical_step"]), bool(clf["logical_step_detail"]), clf["level"]


# -- Module-level singleton -----------------------------------------------

_SINGLETON: Optional[LPDiagnostician] = None


def get_diagnostician() -> LPDiagnostician:
    """Lazy-construct the module-level diagnostician. Subsequent calls reuse it."""
    global _SINGLETON
    if _SINGLETON is None:
        _SINGLETON = LPDiagnostician()
    return _SINGLETON


if __name__ == "__main__":
    # Smoke test - exercise all four LP levels plus the plateau gate.
    d = get_diagnostician()

    print("\n=== L1 (pure symptom description) ===")
    r = d.diagnose(
        student_id="alice", concept="null_pointer",
        question_text="it's not working, I get an error",
    )
    print(f"  level={r.current_lp_level}  logical_step={r.logical_step}  "
          f"logical_step_detail={r.logical_step_detail}")
    print(f"  signals={r.lp_signals_detected}")
    print(f"  wrong_model={r.wrong_model_id}")

    print("\n=== L2 (names rule, no mechanism) ===")
    r = d.diagnose(
        student_id="alice", concept="string_equality",
        question_text="I need to use .equals() instead of == for strings",
    )
    print(f"  level={r.current_lp_level}  logical_step={r.logical_step}  "
          f"logical_step_detail={r.logical_step_detail}")
    print(f"  signals={r.lp_signals_detected}")

    print("\n=== L3 (mechanism-level trace) ===")
    r = d.diagnose(
        student_id="alice", concept="null_pointer",
        question_text=(
            "declaring String s creates a reference slot holding null. "
            "new allocates a heap object and returns its address. Method call "
            "dereferences the reference - if null, NPE."
        ),
    )
    print(f"  level={r.current_lp_level}  logical_step={r.logical_step}  "
          f"logical_step_detail={r.logical_step_detail}")
    print(f"  signals={r.lp_signals_detected}")

    print("\n=== L4 (transfer/generalisation) ===")
    r = d.diagnose(
        student_id="alice", concept="null_pointer",
        question_text=(
            "This applies to all reference types in Java. The same principle - "
            "dereferencing a null address - explains why Java chose to require "
            "explicit null checks on method calls."
        ),
    )
    print(f"  level={r.current_lp_level}  logical_step={r.logical_step}  "
          f"logical_step_detail={r.logical_step_detail}")
    print(f"  signals={r.lp_signals_detected}")

    print("\n=== Plateau gate: 2 consecutive L2 sessions on same concept ===")
    r = d.diagnose(
        student_id="alice", concept="string_equality",
        question_text="I use .equals() for strings",
        stored_lp_level="L2", stored_lp_streak=1,
    )
    print(f"  level={r.current_lp_level}  streak={r.lp_streak}  "
          f"plateau_flag={r.plateau_flag}  plateau_intervention={r.plateau_intervention}")

    print("\n=== Wrong-model signal match piped through diagnostic ===")
    r = d.diagnose(
        student_id="alice", concept="null_pointer",
        question_text="I declared it so why is it null, I created s right there at the top",
    )
    print(f"  level={r.current_lp_level}  wrong_model={r.wrong_model_id}  "
          f"score={r.match_score:.2f}")
    print(f"  signal='{r.matched_signal}'")
    print(f"  origin='{r.wrong_model_origin}'")
