"""NLI edge reader: does a statement agree with, contradict, or ignore an edge's logic?

``EdgeNLI`` uses the cross-encoder fine-tuned on pairs built from the graph
alone (``scripts/build_nli_pairs.py`` -> ``scripts/finetune_nli.py`` ->
``models/nli-chapter1``) and a small sentence-embedding model to pick which
statements to compare with which edge (retrieval only: the most similar
statements, no similarity threshold).

A verdict counts only when it is the model's top label with a probability at
or above the threshold fixed on the dev split of the graph-built pairs
(``models/nli-chapter1/thresholds.json``, at least ``MIN_PROB``); otherwise
the pair is "unrelated". Nothing is tuned on student answers. Both models are loaded offline (``HF_HUB_OFFLINE=1``)
from the local cache, so assessing an answer makes no network call. If the
fine-tuned model is missing the edge reader is simply off.

The older ``NLI`` class (``use_nli``) is kept for the optional way / edge
fallback of reader.py.
"""

from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path

DEFAULT_MODEL = "cross-encoder/nli-deberta-v3-small"
ENTAIL_THRESHOLD = 0.5
EDGE_MODEL = Path(__file__).resolve().parents[2] / "models" / "nli-chapter1"
EMBEDDER = "sentence-transformers/all-MiniLM-L6-v2"
MIN_PROB = 0.5
TOP_CLAUSES = 2       # statements compared with each edge (the most similar ones)
CONTRADICTION, ENTAILMENT, NEUTRAL = 0, 1, 2


def _offline() -> None:
    os.environ.setdefault("HF_HUB_OFFLINE", "1")
    os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")


class NLI:
    """Entailment check with a locally cached sentence-transformers cross-encoder."""

    def __init__(self, model: str = DEFAULT_MODEL) -> None:
        _offline()
        try:
            from sentence_transformers import CrossEncoder
        except ImportError as exc:  # pragma: no cover - optional dependency
            raise RuntimeError("use_nli=True needs sentence-transformers and a cached "
                               f"{model} model") from exc
        self.model = CrossEncoder(model)
        labels = getattr(self.model.config, "id2label", {}) or {}
        self.entail_index = next((i for i, l in labels.items() if "entail" in str(l).lower()), 1)

    def entails(self, premise: str, hypothesis: str) -> bool:
        import numpy as np

        logits = np.asarray(self.model.predict([(premise, hypothesis)]))[0]
        probs = np.exp(logits - logits.max())
        probs = probs / probs.sum()
        return bool(probs[int(self.entail_index)] >= ENTAIL_THRESHOLD)


class EdgeNLI:
    """Agree / contradict / unrelated between graph text and statements."""

    def __init__(self, path: Path = EDGE_MODEL) -> None:
        _offline()
        from sentence_transformers import CrossEncoder, SentenceTransformer

        try:
            import torch

            device = "cuda" if torch.cuda.is_available() else "cpu"
        except ImportError:  # pragma: no cover
            device = "cpu"
        self.model = CrossEncoder(str(path), max_length=256, device=device)
        self.embedder = SentenceTransformer(EMBEDDER, device=device)
        self._cache: dict[tuple[str, str], tuple[float, float, float]] = {}
        # thresholds fixed on the dev split of the graph-built pairs (finetune_nli.py)
        import json

        th = json.load(open(path / "thresholds.json", encoding="utf-8")) if (path / "thresholds.json").exists() else {}
        self.min_entail = max(MIN_PROB, float(th.get("entailment", MIN_PROB)))
        self.min_contra = max(MIN_PROB, float(th.get("contradiction", MIN_PROB)))

    def probs(self, pairs: list[tuple[str, str]]) -> list[tuple[float, float, float]]:
        todo = [p for p in dict.fromkeys(pairs) if p not in self._cache]
        if todo:
            out = self.model.predict(todo, apply_softmax=True, batch_size=32, show_progress_bar=False)
            for p, pr in zip(todo, out):
                self._cache[p] = tuple(float(x) for x in pr)
        return [self._cache[p] for p in pairs]

    def verdict(self, premise: str, hypothesis: str) -> tuple[str, float]:
        """("agrees" | "contradicts" | "unrelated", probability)."""
        pr = self.probs([(premise, hypothesis)])[0]
        k = max(range(3), key=lambda i: pr[i])
        if k == ENTAILMENT and pr[k] >= self.min_entail:
            return "agrees", pr[k]
        if k == CONTRADICTION and pr[k] >= self.min_contra:
            return "contradicts", pr[k]
        return "unrelated", pr[k]

    def closest(self, texts: list[str], queries: list[str], k: int = TOP_CLAUSES) -> list[list[int]]:
        """For each query, the indices of the k most similar texts."""
        if not texts or not queries:
            return [[] for _ in queries]
        import numpy as np

        a = self.embedder.encode(texts, normalize_embeddings=True, show_progress_bar=False)
        b = self.embedder.encode(queries, normalize_embeddings=True, show_progress_bar=False)
        sims = b @ a.T
        return [list(np.argsort(-row)[:k]) for row in sims]


@lru_cache(maxsize=1)
def edge_nli() -> EdgeNLI | None:
    """The fine-tuned edge reader, or None when it has not been trained (or
    LP_GRAPH_EDGE_NLI=0 switches it off)."""
    if os.environ.get("LP_GRAPH_EDGE_NLI", "1") == "0" or not (EDGE_MODEL / "config.json").exists():
        return None
    try:
        return EdgeNLI()
    except Exception:  # pragma: no cover - missing optional dependency
        return None
