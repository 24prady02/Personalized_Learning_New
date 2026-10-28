"""Optional NLI fallback (off by default: ``assess(..., use_nli=False)``).

A cross-encoder may label relation-edge parts and has_level ways that have
no slots. It never decides a misconception on its own. The model is loaded
offline only (``HF_HUB_OFFLINE=1``): it must already be in the local cache,
so the classifier still makes no network call at run time.
"""

from __future__ import annotations

import os

DEFAULT_MODEL = "cross-encoder/nli-deberta-v3-small"
ENTAIL_THRESHOLD = 0.5


class NLI:
    """Entailment check with a locally cached sentence-transformers cross-encoder."""

    def __init__(self, model: str = DEFAULT_MODEL) -> None:
        os.environ.setdefault("HF_HUB_OFFLINE", "1")
        os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")
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
