"""Hypothesis test of edge logic against the student's logic about a concept.

* **premise**: all of the student's logic about one concept - every answer
  sentence that names it or points at its code, in order, as one text;
* **hypothesis**: one piece of that concept's edge logic (a wrong belief, a
  correct rule, a relation edge's logic, a level way), one clause at a time.

An NLI cross-encoder (``cross-encoder/nli-deberta-v3-base``, off the shelf:
not fine-tuned on this project's data, not a generative model) gives
P(entailment), P(contradiction), P(neutral) for each pair. The edge logic is
stated by the student to the degree the premise entails its best-supported
sentence; it is denied to the degree the premise contradicts it.
"""

from __future__ import annotations

import re
from functools import lru_cache

import os

# LP_GRAPH_NLI_MODEL: a fine-tuned copy (scripts/train_answer_nli.py) instead of the base model
MODEL = os.environ.get("LP_GRAPH_NLI_MODEL", "cross-encoder/nli-deberta-v3-base")
# the hypotheses are the edge logic's clauses: split at sentence ends, colons,
# semicolons and parentheses (a general clause in parentheses, "a % b
# subtracts b from a", must not hide the concrete one, "9 % 5 means 9 minus 5")
_SENT = re.compile(r"(?<=[.;!?])\s+|\s*[():;]\s*")


@lru_cache(maxsize=1)
def _model():
    from sentence_transformers import CrossEncoder

    m = CrossEncoder(MODEL)
    labels = {v.lower(): int(k) for k, v in m.model.config.id2label.items()}
    if "entailment" not in labels:      # unnamed labels: the base model's order
        labels = {"contradiction": 0, "entailment": 1, "neutral": 2}
    return m, labels


@lru_cache(maxsize=1)
def _nlp():
    import spacy

    return spacy.load("en_core_web_sm", disable=["ner"])


@lru_cache(maxsize=50000)
def _is_claim(clause: str) -> bool:
    """A hypothesis must be a proposition: a clause with a verb (or "is"), not a
    noun-phrase fragment such as "Plans: divisibility and parity tests"."""
    return any(tok.pos_ in ("VERB", "AUX") for tok in _nlp()(clause))


def sentences(text: str) -> list[str]:
    # the edge logic's claims: clauses of at least three words that have a verb
    parts = [p.strip() for p in _SENT.split(text or "")
             if p and len(p.split()) >= 3 and _is_claim(p.strip())]
    # the whole edge-logic text is a hypothesis too (the trained reader learned it whole)
    whole = (text or "").strip()
    if whole and len(parts) > 1 and _is_claim(whole):
        parts.append(whole)
    return parts or ([text.strip()] if text and text.strip() and _is_claim(text.strip()) else [])


_cache: dict[tuple[str, str], tuple[float, float]] = {}


def test(premise: str, hypotheses: list[str]) -> list[tuple[float, float]]:
    """(P(entailment), P(contradiction)) of each hypothesis given the premise;
    a multi-sentence hypothesis takes its best-entailed sentence (and its most
    contradicted one)."""
    import numpy as np

    model, lab = _model()
    pairs = []
    for h in hypotheses:
        for s in sentences(h):
            if (premise, s) not in _cache:
                pairs.append((premise, s))
    pairs = list(dict.fromkeys(pairs))
    if pairs:
        logits = model.predict(pairs, batch_size=32, show_progress_bar=False)
        probs = np.exp(logits - logits.max(axis=1, keepdims=True))
        probs = probs / probs.sum(axis=1, keepdims=True)
        for (p, s), pr in zip(pairs, probs):
            _cache[(p, s)] = (float(pr[lab["entailment"]]), float(pr[lab["contradiction"]]))
    out = []
    for h in hypotheses:
        vals = [_cache[(premise, s)] for s in sentences(h) if (premise, s) in _cache]
        out.append((max(v[0] for v in vals), max(v[1] for v in vals)) if vals else (0.0, 0.0))
    return out
