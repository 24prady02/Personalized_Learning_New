"""
models.py — the two pretrained models the pipeline uses, loaded once.

  * Embedder  (sentence-transformers/all-MiniLM-L6-v2): semantic similarity
    between a student clause and graph statements.
  * NLI       (cross-encoder/nli-deberta-v3-small): does a clause entail or
    contradict a graph statement.

Neither is trained or fine-tuned here. If one fails to load, the pipeline
runs without it and says so in each result's `degraded` list.
"""
from __future__ import annotations

import os
from functools import lru_cache
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np

EMBEDDER_NAME = "sentence-transformers/all-MiniLM-L6-v2"
NLI_NAME = "cross-encoder/nli-deberta-v3-small"


@lru_cache(maxsize=1)
def _embedder():
    try:
        from sentence_transformers import SentenceTransformer
        return SentenceTransformer(EMBEDDER_NAME)
    except Exception as e:                     # pragma: no cover - environment
        print(f"[lp_percpt] embedder unavailable: {e}")
        return None


@lru_cache(maxsize=1)
def _nli():
    try:
        from sentence_transformers import CrossEncoder
        model = CrossEncoder(NLI_NAME)
        labels = {v.lower(): int(k) for k, v in model.model.config.id2label.items()}
        return model, labels
    except Exception as e:                     # pragma: no cover - environment
        print(f"[lp_percpt] NLI model unavailable: {e}")
        return None


def available() -> Dict[str, bool]:
    return {"embedder": _embedder() is not None, "nli": _nli() is not None}


_EMB_CACHE: Dict[str, np.ndarray] = {}


def embed(texts: Sequence[str]) -> Optional[np.ndarray]:
    """Unit-normalised embeddings; graph statements are cached."""
    model = _embedder()
    if model is None:
        return None
    missing = [t for t in texts if t not in _EMB_CACHE]
    if missing:
        vecs = model.encode(list(missing), normalize_embeddings=True,
                            show_progress_bar=False)
        for t, v in zip(missing, vecs):
            _EMB_CACHE[t] = v
    return np.stack([_EMB_CACHE[t] for t in texts])


def similarity(a: Sequence[str], b: Sequence[str]) -> Optional[np.ndarray]:
    """Cosine similarity matrix, shape (len(a), len(b))."""
    if not a or not b:
        return np.zeros((len(a), len(b)))
    ea, eb = embed(a), embed(b)
    if ea is None or eb is None:
        return None
    return ea @ eb.T


def nli(pairs: List[Tuple[str, str]]) -> Optional[List[Dict[str, float]]]:
    """For each (premise, hypothesis): {'entailment', 'contradiction', 'neutral'}.
    LP_NO_NLI=1 switches NLI off (the pipeline runs as if the model were unavailable)."""
    if os.environ.get("LP_NO_NLI") == "1":
        return None
    loaded = _nli()
    if loaded is None:
        return None
    if not pairs:
        return []
    model, labels = loaded
    probs = model.predict(pairs, apply_softmax=True, show_progress_bar=False)
    return [{name: float(p[idx]) for name, idx in labels.items()} for p in probs]
