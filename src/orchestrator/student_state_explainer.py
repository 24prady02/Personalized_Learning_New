"""
Student-state explainer — turns the CPAL diagnostic dataclass into a
plain-English narrative a person can read.

Two audiences:

  audience="instructor"   — Frank, technical, intended for logs / debug
                            panel. Shows source attribution
                            (trained_wm_head / overlap / hvsae), exact
                            scores, and reasoning about WHY an
                            intervention was chosen. Read by you when
                            you're debugging the pipeline, or by an
                            instructor watching over a tutoring session.

  audience="llm"          — Concise prose summary. Becomes a context
                            block at the top of the tutor prompt
                            (LP-0 STUDENT STATE) so the LLM reads a
                            coherent narrative instead of a key-value
                            dump. The LLM's reply is generated FROM this
                            summary plus the structured LP-1/LP-2/LP-2.5
                            sections — the summary itself is NEVER shown
                            to the student.

Used by:
  - scripts/cpal_chat_app.py  (instructor narrative emitted after every
    diagnose() so logs show prose, not dicts)
  - src/orchestrator/enhanced_personalized_generator.py  (llm narrative
    injected at the top of every _build_enhanced_prompt call)

Design choices grounded in:
  - mental_models_cpal_methodology_revised.docx Part 3 (LP-level
    pedagogy — narrative framing of L1/L2/L3/L4)
  - Chiodini et al. ITiCSE 2021 (ProgMiscon refutation grounding)
"""
from __future__ import annotations

from types import SimpleNamespace
from typing import Optional, Union, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from src.orchestrator.lp_diagnostic import LPDiagnostic

DiagLike = Union["LPDiagnostic", dict]


def _coerce(diag: DiagLike) -> Any:
    """Accept either an LPDiagnostic dataclass OR its .to_dict() form
    (which is what the prompt builder hands us). Returns an object
    that supports attribute access either way."""
    if isinstance(diag, dict):
        # SimpleNamespace gives us .field access over the dict keys,
        # with safe default None for missing fields via __getattr__ fallback.
        return _DictView(diag)
    return diag


class _DictView:
    """Attribute-access view over a dict, returning None for missing keys
    instead of AttributeError. Keeps explain_state's call sites uniform
    between LPDiagnostic-instance and to_dict()-output inputs."""
    __slots__ = ("_d",)

    def __init__(self, d: dict): self._d = d
    def __getattr__(self, name: str):
        # __getattr__ only fires for missing attrs; _d is in __slots__.
        return self._d.get(name)


# Plain-English glosses for LP levels — used in both audiences.
_LP_PROSE = {
    "L1": ("L1 (surface)",
           "name the problem in everyday terms but can't articulate a "
           "rule or mechanism"),
    "L2": ("L2 (rule-level)",
           "can name the rule (e.g. 'use .equals') but haven't explained "
           "WHY the rule holds"),
    "L3": ("L3 (mechanism-level)",
           "explain the underlying mechanism (heap addresses, char-array "
           "comparison, etc.)"),
    "L4": ("L4 (transfer)",
           "generalise the mechanism to related contexts (e.g. Integer "
           "autoboxing, reference identity beyond strings)"),
}

# Glosses for the picker source — explains which subsystem made the
# wrong-model call. Useful in instructor mode for tracing surprising picks.
_SOURCE_GLOSS = {
    "trained_wm_head":  "the trained WM classifier",
    "hvsae":            "the HVSAE semantic matcher",
    "hvsae+overlap":    "the overlap matcher (HVSAE was loaded but didn't fire)",
    "overlap":          "the overlap matcher (signature-based, no embeddings)",
}


def _phrase_trajectory(prior_lp: Optional[str], current_lp: str,
                       streak: int) -> str:
    """One-line description of LP movement turn-over-turn."""
    if prior_lp is None:
        if streak == 0:
            return f"first turn at {current_lp}"
        return f"first observed at {current_lp} (streak {streak})"
    if prior_lp == current_lp:
        if streak >= 2:
            return (f"unchanged from last turn ({current_lp}, streak {streak} "
                    f"— plateau territory)")
        return f"unchanged from last turn ({current_lp})"
    # Compare positions
    order = ["L1", "L2", "L3", "L4"]
    try:
        delta = order.index(current_lp) - order.index(prior_lp)
    except ValueError:
        return f"moved from {prior_lp} to {current_lp}"
    if delta > 0:
        return f"advanced {prior_lp}→{current_lp} (+{delta} level)"
    if delta < 0:
        return f"regressed {prior_lp}→{current_lp} ({delta} level)"
    return f"unchanged ({current_lp})"


def _phrase_mastery_trend(mastery: Optional[float],
                          prior_mastery: Optional[float]) -> str:
    """Describe mastery in prose, with delta when prior is given."""
    if mastery is None:
        return "(no mastery reading)"
    pct = f"{mastery:.2f}"
    if prior_mastery is None:
        return f"mastery={pct}"
    delta = mastery - prior_mastery
    if abs(delta) < 0.01:
        return f"mastery={pct} (≈ unchanged)"
    if delta > 0:
        return f"mastery={pct} (up from {prior_mastery:.2f}, {delta:+.2f})"
    return f"mastery={pct} (down from {prior_mastery:.2f}, {delta:+.2f})"


def _phrase_misconception(diag, audience: str) -> Optional[str]:
    """Sentence(s) about the wrong-model identification, or None if none
    was matched."""
    if not diag.wrong_model_id:
        return None
    parts = []
    if audience == "instructor":
        parts.append(
            f"System identified the **{diag.wrong_model_id}** wrong model")
        if diag.wrong_model_description:
            parts.append(f"(\"{diag.wrong_model_description}\")")
        # Source attribution
        src = _SOURCE_GLOSS.get(diag.source, diag.source)
        parts.append(f"picked by {src}")
        if diag.match_score:
            parts.append(f"at confidence {diag.match_score:.2f}.")
        else:
            parts.append(".")
        # Triggering signal
        if diag.matched_signal:
            sig = diag.matched_signal
            if sig.startswith("[") and sig.endswith("]"):
                parts.append(f"Trigger: {sig}.")
            else:
                parts.append(f"Triggering signal: \"{sig}\".")
        # Origin of the belief (if we have one and it's instructive)
        if diag.wrong_model_origin:
            origin_short = diag.wrong_model_origin
            if len(origin_short) > 140:
                origin_short = origin_short[:137] + "..."
            parts.append(f"Origin of this belief: {origin_short}")
    else:  # llm
        # Concise prose for the LLM — assemble without dangling punctuation
        belief = (diag.wrong_model_description or "").strip().rstrip(".")
        origin = (diag.wrong_model_origin or "").strip().rstrip(".")
        sent = (f"The system suspects the student holds the "
                f"{diag.wrong_model_id} misconception")
        if belief:
            sent += f" — specifically: \"{belief}.\""
        else:
            sent += "."
        parts.append(sent)
        if origin:
            parts.append(f"This belief commonly comes from: {origin}.")
    return " ".join(parts)


def _phrase_grounding(diag) -> Optional[str]:
    """ProgMiscon / JLS grounding sentence, or None if absent."""
    if not diag.wrong_model_refutation:
        return None
    ref = diag.wrong_model_jls_ref or "JLS"
    pm  = diag.wrong_model_progmiscon_id
    s = f"Formal grounding available: {diag.wrong_model_refutation.strip()} ({ref})."
    if pm:
        s += f" ProgMiscon ID: {pm}."
    return s


def _phrase_plan(diag, audience: str) -> Optional[str]:
    """One sentence about plateau + intervention plan."""
    if not (diag.plateau_flag or diag.plateau_intervention):
        return None
    if audience == "instructor":
        if diag.plateau_flag:
            return (f"Plateau detected (streak {diag.lp_streak} at "
                    f"{diag.current_lp_level}). Planned intervention: "
                    f"`{diag.plateau_intervention or 'default'}`.")
        return (f"Planned plateau intervention even without flag: "
                f"`{diag.plateau_intervention}`.")
    # llm — no need to expose plateau jargon
    if diag.plateau_flag:
        return ("The student has been stuck at this level for multiple "
                "turns; the next intervention should break the plateau, "
                "not just re-explain.")
    return None


def explain_state(diag: DiagLike,
                  mastery: Optional[float] = None,
                  prior_lp_level: Optional[str] = None,
                  prior_mastery: Optional[float] = None,
                  audience: str = "instructor") -> str:
    """Build a natural-language narrative of the student's current state.

    audience: "instructor" or "llm".
      - "instructor" returns a multi-line markdown-ish block with
        explicit source attribution and scores. Designed for logs and
        debug panels.
      - "llm" returns a single short prose paragraph suitable for
        injection at the top of the tutor prompt. Never shown to the
        student.

    All inputs may be None — explain_state gracefully degrades to "we
    don't have a reading on X yet" rather than crashing.
    """
    if audience not in ("instructor", "llm"):
        raise ValueError(f"audience must be 'instructor' or 'llm', "
                         f"got {audience!r}")

    diag = _coerce(diag)
    concept   = diag.concept or "the current concept"
    cur_lp    = diag.current_lp_level or "L1"
    tgt_lp    = diag.target_lp_level or "L2"
    streak    = diag.lp_streak or 0
    lp_label, lp_desc = _LP_PROSE.get(cur_lp, (cur_lp, "(level glossary missing)"))
    trajectory = _phrase_trajectory(prior_lp_level, cur_lp, streak)
    mastery_phr = _phrase_mastery_trend(mastery, prior_mastery)
    misc_phr   = _phrase_misconception(diag, audience)
    ground_phr = _phrase_grounding(diag)
    plan_phr   = _phrase_plan(diag, audience)

    if audience == "instructor":
        lines = [
            f"=== STUDENT STATE — {diag.student_id} on `{concept}` ===",
            f"LP: {lp_label} — {lp_desc}",
            f"     ({trajectory}; target {tgt_lp}, logical_step={diag.logical_step}, "
            f"logical_step_detail={diag.logical_step_detail})",
            f"Mastery: {mastery_phr}",
        ]
        if misc_phr:
            lines.append(f"Misconception: {misc_phr}")
        else:
            lines.append("Misconception: none identified (no wrong-model signal fired).")
        if ground_phr:
            lines.append(f"Grounding: {ground_phr}")
        if plan_phr:
            lines.append(f"Plan: {plan_phr}")
        # Diagnostic confidence — useful for "should we probe more?" decisions
        if hasattr(diag, "diagnostic_confidence") and diag.diagnostic_confidence:
            lines.append(
                f"Diagnostic confidence: {diag.diagnostic_confidence:.2f} "
                f"(< 0.55 → probe; ≥ 0.55 → teach)"
            )
        return "\n".join(lines)

    # llm — single coherent paragraph
    parts = [
        f"Student is working on `{concept}` and currently reasons at "
        f"{lp_label} — they {lp_desc}. ({trajectory}.)"
    ]
    if mastery is not None:
        parts.append(f" Their {mastery_phr} on this concept.")
    for p in (misc_phr, ground_phr, plan_phr):
        if p:
            parts.append(" " + p.strip())
    parts.append(
        f" Your job is to teach them toward {tgt_lp} — produce a tutor "
        f"response that takes this state into account (do NOT reveal this "
        f"summary to the student)."
    )
    return "".join(parts)


if __name__ == "__main__":
    # Quick demo against synthetic LPDiagnostic shapes.
    from dataclasses import dataclass, field
    from typing import List, Dict

    @dataclass
    class _Stub:
        concept: str = "string_equality"
        student_id: str = "alice"
        wrong_model_id: str = "SE-A"
        wrong_model_description: str = (
            "== compares the content of strings. Two strings with the "
            "same characters are equal under ==.")
        wrong_model_origin: str = (
            "Python: == calls __eq__ which compares content.")
        matched_signal: str = "they're both hello so why is == false"
        match_score: float = 0.78
        wrong_model_refutation: str = (
            "o==p compares the references stored in the variables o and p")
        wrong_model_jls_ref: str = "JLS21 §15.21"
        wrong_model_progmiscon_id: str = "EqualityOperatorComparesObjectsValues"
        current_lp_level: str = "L2"
        target_lp_level: str = "L3"
        lp_streak: int = 2
        logical_step: bool = True
        logical_step_detail: bool = False
        plateau_flag: bool = True
        plateau_intervention: str = "trace_scaffold"
        source: str = "trained_wm_head"
        diagnostic_confidence: float = 0.42

    s = _Stub()
    print("\n--- instructor ---\n")
    print(explain_state(s, mastery=0.42, prior_lp_level="L2",
                        prior_mastery=0.38, audience="instructor"))
    print("\n--- llm ---\n")
    print(explain_state(s, mastery=0.42, prior_lp_level="L2",
                        prior_mastery=0.38, audience="llm"))
