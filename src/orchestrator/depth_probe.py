"""
Depth probe — the *conceptual depth* verification layer.

Purpose: when a student belief is being graded, this module asks a separate
question: "is the student's language actually backed by mechanism, or is
it hollow vocabulary?". It runs IN ADDITION to the LP-level grader (which
asks 'which level'), the multi-concept resolver (which asks 'which concepts'),
and the sub-criteria probe picker (which asks 'which facet next'). It does
NOT replace any of them — it sits as a higher-priority probe selector that
fires only when there is positive evidence of hollow jargon or surface
similarity to a wrong belief.

Composes with the multi-turn ladder:
  * the depth probe COUNTS toward probe_count (one ladder rung consumed)
  * the matched trap phrase / depth-check description is appended to
    probed_criteria so we never ask the same depth probe twice
  * the depth probe is scoped to ONE concept (the focus concept) at a time,
    so multi-concept turns route each concept through its own depth check

Two independent signals trigger a depth probe:

  1. JARGON TRAP — the student's text contains an authored hollow-jargon
     phrase from data/mental_models/jargon_traps.json. The trap carries
     its own `diagnostic_probe` question, which targets the specific
     misapplication. Highest priority: a matched trap is unambiguous.

  2. EMBEDDING-SIMILARITY GATE — the student's belief is HIGH cosine to
     BOTH the correct L3 rubric AND at least one wrong-model belief. That
     pattern indicates surface paraphrasing without commitment to either
     side. We ask the student to walk through the mechanism explicitly.

If neither signal fires, the caller falls back to the standard sub-criterion
probe picker (orchestrator._pick_unprobed_criterion / chat_app /
student_app equivalents).
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

# Default thresholds. Tuned conservatively — we'd rather miss a depth probe
# than fire spuriously on every student with technical vocabulary.
DEFAULT_SIM_TO_CORRECT_FLOOR = 0.50   # paraphrasing the right answer
DEFAULT_SIM_TO_WRONG_FLOOR   = 0.45   # ALSO resembling a wrong belief


@dataclass
class DepthProbe:
    """Result of a depth-probe selection — the question to ask + why."""
    question: str         # the diagnostic probe question to show the student
    reason: str           # "jargon_trap" | "high_sim_to_wrong" | None
    detail: str           # the trap phrase OR the wrong-belief that matched
    criterion_key: str    # used by the ladder for probed_criteria de-dup


def find_jargon_trap(student_text: str, catalogue, concept_id: str,
                     already_probed: Optional[List[str]] = None
                     ) -> Optional[DepthProbe]:
    """Return the first jargon trap whose phrase appears in student_text.
    Skips traps whose phrase has already been probed for this concept this
    session (de-dup via the ladder's probed_criteria list).
    """
    if not student_text:
        return None
    text = student_text.lower()
    traps = []
    try:
        traps = catalogue.get_jargon_traps(concept_id) or []
    except Exception:
        return None
    already = set(already_probed or [])
    for trap in traps:
        if not trap.phrase:
            continue
        if trap.phrase.lower() not in text:
            continue
        key = _trap_key(trap.phrase)
        if key in already:
            continue
        return DepthProbe(
            question=trap.diagnostic_probe,
            reason="jargon_trap",
            detail=trap.phrase,
            criterion_key=key,
        )
    return None


def embedding_depth_check(student_text: str, catalogue, concept_id: str,
                           rag=None,
                           sim_to_correct_floor: float = DEFAULT_SIM_TO_CORRECT_FLOOR,
                           sim_to_wrong_floor: float = DEFAULT_SIM_TO_WRONG_FLOOR,
                           already_probed: Optional[List[str]] = None
                           ) -> Optional[DepthProbe]:
    """Surface-paraphrase check. Returns a depth probe when the student text
    resembles BOTH the correct L3 rubric AND at least one wrong belief —
    classic "I've heard the phrasing on both sides" pattern.

    `rag` is an optional CatalogueRAG instance. When None we lazily try to
    build one; absence (no sentence-transformers) → return None silently.
    """
    if not student_text:
        return None
    if rag is None:
        try:
            from src.orchestrator.catalogue_rag import CatalogueRAG
            rag = CatalogueRAG()
        except Exception:
            return None

    entry = None
    try:
        entry = catalogue.get_concept(concept_id)
    except Exception:
        return None
    if not entry:
        return None
    rubric_l3 = (entry.lp_rubric.get("L3") or "").strip()
    if not rubric_l3:
        return None

    # Cosine via the RAG encoder. sim_to_correct = student vs L3 rubric;
    # sim_to_wrong = max over all wrong-belief texts for this concept.
    try:
        q_emb = rag._embed_query(student_text)
        rubric_emb = rag._embed_query(rubric_l3)
        import torch as _t
        sim_to_correct = float(_t.dot(q_emb, rubric_emb).item())
    except Exception:
        return None

    sim_to_wrong = 0.0
    matched_belief = ""
    for wm in entry.wrong_models:
        try:
            wm_emb = rag._embed_query(wm.wrong_belief)
            s = float(_t.dot(q_emb, wm_emb).item())
            if s > sim_to_wrong:
                sim_to_wrong = s
                matched_belief = wm.wrong_belief
        except Exception:
            continue

    # Both high → student text is in the overlap region.
    if (sim_to_correct >= sim_to_correct_floor and
            sim_to_wrong >= sim_to_wrong_floor):
        key = _depth_key("high_sim_to_wrong", matched_belief[:60])
        already = set(already_probed or [])
        if key in already:
            return None
        question = (
            f"Your wording sounds close to both the correct mechanism AND a "
            f"common misconception ({matched_belief[:120]}...). Walk me "
            f"through the operative step in detail — what does Java actually "
            f"DO at that point, not just what name we give it?"
        )
        return DepthProbe(
            question=question,
            reason="high_sim_to_wrong",
            detail=matched_belief,
            criterion_key=key,
        )
    return None


def select_depth_probe(student_text: str, catalogue, concept_id: str,
                        rag=None,
                        already_probed: Optional[List[str]] = None
                        ) -> Optional[DepthProbe]:
    """Pick a depth probe for this concept, if either signal fires.

    Priority:
      1. JARGON TRAP — exact-phrase match against authored traps. Highest
         priority because the misapplication is documented.
      2. EMBEDDING-SIMILARITY GATE — student text resembles both correct
         and wrong belief; ask them to commit.
    Returns None when neither fires — caller falls through to the standard
    sub-criterion probe picker.
    """
    trap_probe = find_jargon_trap(student_text, catalogue, concept_id,
                                  already_probed=already_probed)
    if trap_probe is not None:
        return trap_probe
    sim_probe = embedding_depth_check(student_text, catalogue, concept_id,
                                       rag=rag, already_probed=already_probed)
    return sim_probe


# -- internals ---------------------------------------------------------------

def _trap_key(phrase: str) -> str:
    """De-dup key for a jargon-trap probe in probed_criteria."""
    return f"depth:jargon:{phrase.strip().lower()[:60]}"


def _depth_key(reason: str, detail: str) -> str:
    """De-dup key for an embedding-similarity depth probe."""
    return f"depth:{reason}:{detail.strip().lower()[:60]}"
