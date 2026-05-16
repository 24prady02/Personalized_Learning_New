"""
Depth probe — the *conceptual depth* verification layer (DYNAMIC).

Purpose: when a student belief is being graded, this module asks a separate
question: "is the student's language actually backed by mechanism, or is
it hollow vocabulary?". It runs IN ADDITION to the LP-level grader (which
asks 'which level'), the multi-concept resolver (which asks 'which concepts'),
and the sub-criteria probe picker (which asks 'which facet next').

DYNAMIC by design — the probe is GENERATED per-turn by the LLM from the
specific student text + the catalogue's wrong-belief + the target rubric.
There are NO hardcoded probe questions on the hot path. The
data/mental_models/jargon_traps.json file is kept only as a fast-path
fallback for offline use; the primary path queries the LLM so any concept
in any catalogue gets depth probes "for free" — no manual authoring per
concept required.

Detection signals (run in this order):

  1. EMBEDDING-SIMILARITY GATE — the student's belief is HIGH cosine to
     BOTH the correct L3 rubric AND at least one wrong-model belief. This
     pattern indicates surface paraphrasing without commitment. The matched
     wrong-belief becomes the LLM's anchor for generating a probe targeting
     the SPECIFIC misapplication the student is at risk of.

  2. MECHANISM-VOCABULARY DENSITY GATE — the student uses several mechanism
     terms (heap, address, reference, dereference, runtime, ...) but the
     surrounding text doesn't form a causal chain (no because/so/therefore,
     short, no verbs of execution). LLM generates a probe asking the
     student to trace the mechanism the vocabulary references.

  3. AUTHORED JARGON TRAP (fallback only) — exact-phrase match against the
     legacy traps file. Used only when the LLM is unreachable.

Composes with the multi-turn ladder:
  * the depth probe COUNTS toward probe_count (one ladder rung consumed)
  * the criterion_key is appended to probed_criteria so the same depth
    probe never fires twice within a session
  * the depth probe is scoped to ONE concept (the focus concept) at a time;
    multi-concept turns route each concept through its own depth check
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional
import os
import re

# Default thresholds. Tuned conservatively — we'd rather miss a depth probe
# than fire spuriously on every student with technical vocabulary.
DEFAULT_SIM_TO_CORRECT_FLOOR = 0.50   # paraphrasing the right answer
DEFAULT_SIM_TO_WRONG_FLOOR   = 0.45   # ALSO resembling a wrong belief

# Mechanism-vocabulary density gate. Counts how many of these words appear in
# the student text; if >= MIN_MECHANISM_WORDS but the text shows no causal
# chain (no `because`, `so`, `therefore`, no execution verbs), the vocab is
# probably hollow and we generate a "trace this please" probe.
_MECHANISM_VOCAB = frozenset({
    "heap", "stack", "address", "addresses", "reference", "references",
    "pointer", "pointers", "allocate", "allocates", "allocation",
    "dereference", "dereferences", "compile-time", "runtime",
    "instance", "static", "object", "objects", "memory", "slot", "frame",
    "buffer", "interning", "intern", "constant pool",
    "garbage collector", "garbage collection", "gc",
})
_CAUSAL_CHAIN_MARKERS = frozenset({
    "because", "so", "therefore", "since", "then", "thus", "hence",
    "as a result", "which means", "that's why",
})
_EXECUTION_VERBS = frozenset({
    "evaluates", "evaluated", "computes", "computed", "executes",
    "executed", "checks", "checked", "compares", "compared", "walks",
    "walked", "follows", "followed", "reads", "writes", "wrote",
    "creates", "created", "produces", "produced", "stores", "stored",
})
MIN_MECHANISM_WORDS = 2


def _has_causal_chain(text: str) -> bool:
    low = (text or "").lower()
    return any(m in low for m in _CAUSAL_CHAIN_MARKERS)


def _has_execution_verb(text: str) -> bool:
    low = (text or "").lower()
    return any(v in low for v in _EXECUTION_VERBS)


def _mechanism_word_count(text: str) -> int:
    low = (text or "").lower()
    # Match whole words; phrases like "garbage collector" use literal substring.
    word_set = set(re.findall(r"[a-z][a-z\-]*", low))
    phrase_hits = sum(1 for p in _MECHANISM_VOCAB if " " in p and p in low)
    word_hits   = sum(1 for w in _MECHANISM_VOCAB if " " not in w
                       and w in word_set)
    return phrase_hits + word_hits


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


def _llm_generate_probe(student_text: str, target_belief: str,
                         target_rubric: str, signal: str) -> Optional[str]:
    """Ask the LLM to compose ONE probe question targeting the specific gap
    detected. Returns the question text, or None when the LLM is unavailable.

    `signal` is "embedding_sim_to_wrong" or "vocab_density" — it shapes the
    framing so the probe doesn't sound generic.
    """
    try:
        import requests
        model = (
            os.environ.get("CPAL_OLLAMA_MODEL")
            or "llama3.1:8b"
        )
        framing = {
            "embedding_sim_to_wrong":
                ("The student's wording is uncomfortably close to a "
                 "documented MISCONCEPTION. Ask ONE focused question that "
                 "would force them to commit either to the misconception OR "
                 "to the correct mechanism — they cannot answer both."),
            "vocab_density":
                ("The student used MECHANISM VOCABULARY but did not trace "
                 "any causal chain. Ask ONE focused question that requires "
                 "them to EXPLAIN what one of those terms actually does at "
                 "runtime/compile-time in THIS case — not just name it."),
        }.get(signal, "Ask ONE focused depth-check question.")

        prompt = (
            "You are diagnosing a Java student's CONCEPTUAL DEPTH.\n\n"
            f"STUDENT WROTE: \"{student_text}\"\n\n"
            f"DOCUMENTED MISCONCEPTION to use as your anchor: "
            f"\"{target_belief}\"\n\n"
            f"CORRECT MECHANISM (target understanding): "
            f"\"{target_rubric}\"\n\n"
            f"{framing}\n\n"
            "RULES:\n"
            " - ONE question only, 1-2 sentences.\n"
            " - Reference the SPECIFIC term or phrase the student used.\n"
            " - Do NOT teach. Do NOT use phrases like \"great question\", "
            "\"let's dive\", \"good question\".\n"
            " - The answer to your question must distinguish UNDERSTANDING "
            "from VOCABULARY-PARROTING.\n"
            " - Plain text only. No markdown, no JSON.\n\n"
            "Probe question:"
        )
        r = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": model, "prompt": prompt, "stream": False,
                  "options": {"temperature": 0.3, "num_predict": 140}},
            timeout=30,
        )
        r.raise_for_status()
        out = (r.json().get("response") or "").strip()
        # Strip any leading "Probe question:" the model might echo back.
        out = re.sub(r"^\s*probe\s*question\s*:\s*", "", out, flags=re.I).strip()
        # Take only the first 1-2 sentences, never let it wander.
        sents = re.split(r"(?<=[.?!])\s+", out, maxsplit=2)
        out = " ".join(sents[:2]).strip()
        return out or None
    except Exception as e:
        print(f"[Depth] LLM probe-gen failed: {e}")
        return None


def select_depth_probe(student_text: str, catalogue, concept_id: str,
                        rag=None,
                        already_probed: Optional[List[str]] = None
                        ) -> Optional[DepthProbe]:
    """Pick a depth probe for this concept (DYNAMIC primary path).

    Priority — every tier generates the question via the LLM when reachable,
    using the catalogue's own rubric + wrong-beliefs as anchors. Authored
    jargon_traps are only consulted as a fast-path fallback when both LLM
    and embedding tier are unavailable.

      1. EMBEDDING-SIMILARITY GATE → LLM-generated probe targeting the
         matched wrong-belief.
      2. MECHANISM-VOCAB DENSITY GATE → LLM-generated probe asking the
         student to trace one of the terms they used.
      3. AUTHORED JARGON TRAP → fallback (offline-safe).
    Returns None when no signal fires; caller falls through to the standard
    sub-criterion probe picker.
    """
    if not student_text or not catalogue or not concept_id:
        return None

    # --- Tier 1: embedding-similarity gate -----------------------------
    sim_probe = embedding_depth_check(student_text, catalogue, concept_id,
                                       rag=rag, already_probed=already_probed)
    if sim_probe is not None:
        # Upgrade the templated question to an LLM-generated one targeting
        # the SPECIFIC matched wrong-belief.
        entry = None
        try:
            entry = catalogue.get_concept(concept_id)
        except Exception:
            pass
        target_rubric = (entry.lp_rubric.get("L3") if entry else "") or ""
        gen_q = _llm_generate_probe(
            student_text=student_text,
            target_belief=sim_probe.detail,
            target_rubric=target_rubric,
            signal="embedding_sim_to_wrong",
        )
        if gen_q:
            sim_probe.question = gen_q
            sim_probe.reason = "dynamic_sim_to_wrong"
        return sim_probe

    # --- Tier 2: mechanism-vocab density gate --------------------------
    if (_mechanism_word_count(student_text) >= MIN_MECHANISM_WORDS
            and not _has_causal_chain(student_text)
            and not _has_execution_verb(student_text)):
        entry = None
        try:
            entry = catalogue.get_concept(concept_id)
        except Exception:
            pass
        target_rubric = (entry.lp_rubric.get("L3") if entry else "") or ""
        # Use the highest-density wrong-belief as the anchor for the LLM.
        anchor_belief = (entry.wrong_models[0].wrong_belief
                          if entry and entry.wrong_models else "")
        gen_q = _llm_generate_probe(
            student_text=student_text,
            target_belief=anchor_belief,
            target_rubric=target_rubric,
            signal="vocab_density",
        )
        if gen_q:
            key = _depth_key("vocab_density",
                              student_text.lower()[:40])
            already = set(already_probed or [])
            if key not in already:
                return DepthProbe(
                    question=gen_q,
                    reason="dynamic_vocab_density",
                    detail="mechanism vocab without causal chain",
                    criterion_key=key,
                )

    # --- Tier 3: authored jargon trap (offline-safe fallback) ----------
    trap_probe = find_jargon_trap(student_text, catalogue, concept_id,
                                  already_probed=already_probed)
    return trap_probe


# -- internals ---------------------------------------------------------------

def _trap_key(phrase: str) -> str:
    """De-dup key for a jargon-trap probe in probed_criteria."""
    return f"depth:jargon:{phrase.strip().lower()[:60]}"


def _depth_key(reason: str, detail: str) -> str:
    """De-dup key for an embedding-similarity depth probe."""
    return f"depth:{reason}:{detail.strip().lower()[:60]}"
