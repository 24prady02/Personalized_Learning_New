"""
Mental-model catalogue for Java CS1 wrong models.

Loads data/mental_models/wrong_models_catalogue.json and exposes:

  catalogue.get_concept(concept_id) -> ConceptEntry
  catalogue.match_wrong_model(question_text, concept_id) -> WrongModelMatch
  catalogue.get_lp_rubric(concept_id) -> Dict[str, str]  # {L1, L2, L3, L4}
  catalogue.all_concepts() -> List[str]

Grounded in mental_models_cpal_methodology_revised.docx Part 2 - the 20-concept
catalogue of documented wrong beliefs, origins, and conversation signals
(Kaczmarczyk et al. 2010, Sorva 2013, Kennedy & Kraemer 2018).

Used by:
  - LPDiagnostic (orchestrator, Stage 1) to identify wrong_model_id from the
    student's question text before any intervention selection.
  - _build_enhanced_prompt (Stage 3, Section LP-2) to feed wrong-model
    context into the LLM prompt.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import json
import re


@dataclass
class WrongModel:
    """One wrong mental model for a concept."""
    id: str
    wrong_belief: str
    origin: str
    conversation_signals: List[str]


@dataclass
class ConceptEntry:
    """Full catalogue entry for one Java CS1 concept."""
    concept_id: str
    week: int
    error_class: str                 # compile_error, runtime_error, logic_error, ...
    java_concept: str                # short prose description
    wrong_models: List[WrongModel]
    lp_rubric: Dict[str, str]        # {"L1": ..., "L2": ..., "L3": ..., "L4": ...}


@dataclass
class WrongModelMatch:
    """Result of matching a student question against the catalogue."""
    concept_id: str
    wrong_model_id: Optional[str]    # e.g. "NP-A" - None if no signal matched
    wrong_belief: Optional[str]
    origin: Optional[str]
    matched_signal: Optional[str]    # the literal phrase that triggered the match
    match_score: float               # 0.0 (no match) .. 1.0 (perfect)
    all_candidates: List[Tuple[str, float]]  # [(wrong_model_id, score), ...] sorted desc


class MentalModelsCatalogue:
    """Catalogue of wrong mental models, loaded once at init."""

    DEFAULT_PATH = "data/mental_models/wrong_models_catalogue.json"

    def __init__(self, json_path: Optional[str] = None):
        self.json_path = Path(json_path or self.DEFAULT_PATH)
        self._concepts: Dict[str, ConceptEntry] = {}
        self._load()

    def _load(self) -> None:
        if not self.json_path.exists():
            print(f"[MentalModels] WARN: no catalogue at {self.json_path}")
            return
        with open(self.json_path) as f:
            raw = json.load(f)
        for cid, entry in raw.get("concepts", {}).items():
            wrong_models = [
                WrongModel(
                    id=wm["id"],
                    wrong_belief=wm["wrong_belief"],
                    origin=wm["origin"],
                    conversation_signals=wm["conversation_signals"],
                )
                for wm in entry.get("wrong_models", [])
            ]
            self._concepts[cid] = ConceptEntry(
                concept_id=cid,
                week=int(entry.get("week", 0)),
                error_class=entry.get("error_class", ""),
                java_concept=entry.get("java_concept", ""),
                wrong_models=wrong_models,
                lp_rubric=dict(entry.get("lp_rubric", {})),
            )
        print(f"[MentalModels] loaded {len(self._concepts)} concepts, "
              f"{sum(len(c.wrong_models) for c in self._concepts.values())} wrong models")

    # -- Public API --------------------------------------------------------

    def all_concepts(self) -> List[str]:
        return sorted(self._concepts.keys())

    def get_concept(self, concept_id: str) -> Optional[ConceptEntry]:
        return self._concepts.get(concept_id)

    def get_lp_rubric(self, concept_id: str) -> Optional[Dict[str, str]]:
        entry = self._concepts.get(concept_id)
        return dict(entry.lp_rubric) if entry else None

    def get_wrong_model(self, concept_id: str, wrong_model_id: str) -> Optional[WrongModel]:
        entry = self._concepts.get(concept_id)
        if not entry:
            return None
        for wm in entry.wrong_models:
            if wm.id == wrong_model_id:
                return wm
        return None

    def match_wrong_model(self,
                          question_text: str,
                          concept_id: str) -> WrongModelMatch:
        """
        Match a student's natural-language question against the catalogue for a
        given concept.

        Returns a WrongModelMatch with the best-scoring wrong model and its
        matched signal, or a match with wrong_model_id=None and score=0.0 if
        nothing in the catalogue fires.

        Matching strategy (deliberately simple, deterministic, and debuggable):

          1. Normalise the question (lowercase, strip punctuation).
          2. For each wrong model, score each of its conversation_signals by
             computing how many of the signal's content words appear in the
             question, divided by the total number of content words in the
             signal (overlap ratio, 0.0..1.0).
          3. A signal counts as a "hit" if its overlap ratio is >= 0.6 AND at
             least 2 content words overlap. Short signals (1-2 words) require
             a full match.
          4. The wrong model's score is the max signal hit across its signals.
          5. Return the highest-scoring wrong model.

        Why not fuzzy/embedding matching? Because the methodology doc says
        conversation signals are "specific phrases and patterns" - we want
        exact, interpretable matches we can debug, not opaque similarity.
        Embedding-based matching would be an upgrade path; for now keep it
        explicit so misdiagnoses are traceable to specific signals.
        """
        entry = self._concepts.get(concept_id)
        if not entry:
            return WrongModelMatch(
                concept_id=concept_id, wrong_model_id=None,
                wrong_belief=None, origin=None, matched_signal=None,
                match_score=0.0, all_candidates=[],
            )

        q_norm = self._normalise(question_text)
        q_words = set(self._content_words(q_norm))

        best_score = 0.0
        best_wm: Optional[WrongModel] = None
        best_signal: Optional[str] = None
        per_wm_scores: List[Tuple[str, float]] = []

        for wm in entry.wrong_models:
            wm_best_score = 0.0
            wm_best_signal: Optional[str] = None
            for signal in wm.conversation_signals:
                score, _ = self._score_signal(signal, q_words, q_norm)
                if score > wm_best_score:
                    wm_best_score = score
                    wm_best_signal = signal
            per_wm_scores.append((wm.id, wm_best_score))
            if wm_best_score > best_score:
                best_score = wm_best_score
                best_wm = wm
                best_signal = wm_best_signal

        per_wm_scores.sort(key=lambda t: t[1], reverse=True)

        if best_wm is None or best_score == 0.0:
            return WrongModelMatch(
                concept_id=concept_id, wrong_model_id=None,
                wrong_belief=None, origin=None, matched_signal=None,
                match_score=0.0, all_candidates=per_wm_scores,
            )

        return WrongModelMatch(
            concept_id=concept_id,
            wrong_model_id=best_wm.id,
            wrong_belief=best_wm.wrong_belief,
            origin=best_wm.origin,
            matched_signal=best_signal,
            match_score=best_score,
            all_candidates=per_wm_scores,
        )

    # -- Scoring helpers ---------------------------------------------------

    # Stopwords - content-free tokens that shouldn't count toward overlap.
    # Intentionally small: we keep "it", "is", "the" etc out so the overlap
    # ratio reflects meaningful word match, but we keep programming nouns
    # ("string", "int", "null") since those are signal-defining.
    _STOPWORDS = frozenset({
        "a", "an", "the", "is", "are", "was", "were", "be", "been",
        "i", "my", "me", "you", "your", "we", "they",
        "to", "of", "in", "on", "at", "for", "with", "by",
        "and", "or", "but", "so", "if", "then", "because",
        "this", "that", "these", "those",
        "do", "does", "did", "doing", "done",
        "have", "has", "had", "having",
        "will", "would", "could", "should", "can",
        "what", "why", "how", "when", "where", "which",
        "not", "no",  # kept out - most signals don't hinge on these
    })

    @staticmethod
    def _normalise(text: str) -> str:
        """Lowercase, collapse whitespace, keep apostrophes and operator glyphs."""
        text = text.lower()
        # keep word chars, apostrophe, and common operator glyphs the signals reference
        text = re.sub(r"[^a-z0-9'+\-=<>!&|*/\[\]().]", " ", text)
        text = re.sub(r"\s+", " ", text).strip()
        return text

    @classmethod
    def _content_words(cls, normalised_text: str) -> List[str]:
        """Split to tokens, drop stopwords, drop single-char tokens."""
        toks = normalised_text.split()
        return [t for t in toks if t not in cls._STOPWORDS and len(t) > 1]

    @classmethod
    def _score_signal(cls,
                      signal: str,
                      q_words: set,
                      q_norm: str) -> Tuple[float, int]:
        """
        Score one signal phrase against the question.
        Returns (score, overlap_count).

        - Full substring match of the signal in the question -> 1.0 (the
          strongest possible signal).
        - Otherwise overlap ratio: |signal_content_words INT q_words| /
          |signal_content_words|, gated by min-overlap rules.
        """
        sig_norm = cls._normalise(signal)
        # Fast path: literal substring hit.
        if sig_norm and sig_norm in q_norm:
            return 1.0, len(sig_norm.split())

        sig_words = [w for w in sig_norm.split()
                     if w not in cls._STOPWORDS and len(w) > 1]
        if not sig_words:
            return 0.0, 0

        overlap = sum(1 for w in sig_words if w in q_words)
        if overlap == 0:
            return 0.0, 0

        ratio = overlap / len(sig_words)
        # Gating rules to prevent spurious matches on very short signals.
        if len(sig_words) <= 2:
            # Short signal: need ALL content words to hit.
            if overlap < len(sig_words):
                return 0.0, overlap
            return ratio, overlap
        # Longer signal: need >=60% overlap AND at least 2 matching words.
        if ratio < 0.60 or overlap < 2:
            return 0.0, overlap
        return ratio, overlap


# Module-level singleton so callers can just import the catalogue once.
# Importing this module does NOT trigger the load - call get_catalogue() to
# construct on first use (lazy init keeps import cheap and test-friendly).
_SINGLETON: Optional[MentalModelsCatalogue] = None


def get_catalogue(json_path: Optional[str] = None) -> MentalModelsCatalogue:
    """Lazy-construct the module-level catalogue. Subsequent calls reuse it."""
    global _SINGLETON
    if _SINGLETON is None:
        _SINGLETON = MentalModelsCatalogue(json_path=json_path)
    return _SINGLETON


if __name__ == "__main__":
    # Smoke tests against signals from the catalogue.
    cat = get_catalogue()
    print(f"\nLoaded {len(cat.all_concepts())} concepts.")
    print(f"Concepts: {cat.all_concepts()}\n")

    cases = [
        ("null_pointer",
         "I declared it so why is it null though, String s; I thought that made the string"),
        ("string_equality",
         "they're both 'hello' so why is == false? I printed them both"),
        ("array_index",
         "I have 5 elements so I used arr[5] for the last one but it crashed"),
        ("integer_division",
         "5 divided by 2 is 2.5 so why does Java say 2? it rounded"),
        ("type_mismatch",
         "in Python this just works, why won't + just combine the int and the string"),
        ("null_pointer",
         "what is cache consistency in distributed systems"),  # unrelated, expect no match
    ]
    for concept, q in cases:
        m = cat.match_wrong_model(q, concept)
        print(f"[{concept}] q='{q[:60]}...'")
        print(f"  -> wrong_model={m.wrong_model_id}  score={m.match_score:.2f}")
        print(f"     signal='{m.matched_signal}'")
        print(f"     candidates={m.all_candidates}")
        print()
