"""
Catalogue RAG — embedding-based retrieval over the wrong-models catalogue
and LP rubric, plus hybrid scoring with the trained WM head.

Why this exists:
  The trained WM sub-head (cpal_wm_subhead.pt) has val_acc ~0.04 on 60
  classes. Above random (1/60 ~ 0.017) but wrong most of the time. When
  it picks the wrong wrong-model, the LP-2 prompt section feeds the LLM
  a misconception the student isn't actually exhibiting.

What this fixes:
  At inference, embed the student's text and compute cosine similarity
  against pre-embedded catalogue entries. Combine with classifier probs
  via hybrid scoring so we get the classifier's signal when confident
  and lean on retrieval when it hedges.

Encoder: sentence-transformers/all-MiniLM-L6-v2 (already loaded for the
sentence-transformers LP head; ~22 MB, 384-dim).

Catalogue:  data/mental_models/wrong_models_catalogue.json
            20 concepts -> 60 wrong models, each with wrong_belief, origin,
            and conversation_signals
LP rubric:  data/mental_models/wrong_models_catalogue.json -> per-concept
            lp_rubric: {L1, L2, L3, L4 -> rubric text}
            => 80 rubric entries (20 concepts * 4 levels)
"""
from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Optional, Tuple
import json

ROOT = Path(__file__).parent.parent.parent
CATALOGUE_PATH = ROOT / "data" / "mental_models" / "wrong_models_catalogue.json"
ENCODER_NAME   = "sentence-transformers/all-MiniLM-L6-v2"


class CatalogueRAG:
    """Embedding-based retrieval + hybrid scoring over the wrong-models
    catalogue and LP rubric. Encodes 60 + 80 = 140 entries once at init."""

    def __init__(self, catalogue_path: Optional[Path] = None,
                 encoder_name: str = ENCODER_NAME):
        self.catalogue_path = Path(catalogue_path or CATALOGUE_PATH)
        self.encoder_name   = encoder_name
        self._encoder       = None
        # Wrong-model index
        self.wm_ids:    List[str]   = []     # parallel to wm_emb rows
        self.wm_concept: List[str]  = []     # which concept this WM belongs to
        self.wm_text:   List[str]   = []     # the text that was embedded
        self.wm_meta:   List[Dict]  = []     # full entry (belief, origin, ...)
        self.wm_emb                  = None  # (60, 384) torch.FloatTensor
        # LP rubric index
        self.lp_keys:   List[str]   = []     # "{concept}:{level}"
        self.lp_concept: List[str]  = []
        self.lp_level:  List[str]   = []     # "L1".."L4"
        self.lp_text:   List[str]   = []
        self.lp_emb                  = None  # (80, 384) torch.FloatTensor
        self._load_and_embed()

    # ------------------------------------------------------------------ #
    # Setup                                                              #
    # ------------------------------------------------------------------ #

    def _ensure_encoder(self):
        if self._encoder is not None:
            return self._encoder
        from sentence_transformers import SentenceTransformer
        self._encoder = SentenceTransformer(self.encoder_name)
        return self._encoder

    def _load_and_embed(self):
        import torch
        cat = json.loads(self.catalogue_path.read_text(encoding="utf-8"))

        # Build wrong-model text (belief + origin + signals concatenated)
        for concept_id, entry in cat.get("concepts", {}).items():
            for wm in entry.get("wrong_models", []):
                self.wm_ids.append(wm["id"])
                self.wm_concept.append(concept_id)
                belief = wm.get("wrong_belief", "")
                origin = wm.get("origin", "")
                signals = " | ".join(wm.get("conversation_signals", []) or [])
                # Concatenate. Belief carries the strongest signal so we
                # repeat it once to up-weight without changing similarity
                # math.
                text = (f"{belief} {belief} | origin: {origin} | "
                        f"signals: {signals}").strip()
                self.wm_text.append(text)
                self.wm_meta.append({
                    "id":            wm["id"],
                    "concept":       concept_id,
                    "wrong_belief":  belief,
                    "origin":        origin,
                    "signals":       wm.get("conversation_signals", []) or [],
                })
            # LP rubric (4 levels per concept)
            rubric = entry.get("lp_rubric", {}) or {}
            for level in ("L1", "L2", "L3", "L4"):
                txt = rubric.get(level, "")
                if not txt: continue
                self.lp_keys.append(f"{concept_id}:{level}")
                self.lp_concept.append(concept_id)
                self.lp_level.append(level)
                self.lp_text.append(txt)

        encoder = self._ensure_encoder()
        if self.wm_text:
            self.wm_emb = encoder.encode(
                self.wm_text, convert_to_tensor=True,
                normalize_embeddings=True, show_progress_bar=False,
            ).cpu()
        if self.lp_text:
            self.lp_emb = encoder.encode(
                self.lp_text, convert_to_tensor=True,
                normalize_embeddings=True, show_progress_bar=False,
            ).cpu()
        print(f"[CatalogueRAG] indexed {len(self.wm_ids)} wrong-models, "
              f"{len(self.lp_keys)} LP rubric entries "
              f"(encoder={self.encoder_name})")

    # ------------------------------------------------------------------ #
    # Retrieval                                                          #
    # ------------------------------------------------------------------ #

    def _embed_query(self, text: str):
        import torch
        encoder = self._ensure_encoder()
        v = encoder.encode([text], convert_to_tensor=True,
                           normalize_embeddings=True,
                           show_progress_bar=False).cpu()
        return v[0]  # (384,)

    def retrieve_wrong_models(self, text: str, top_k: int = 3,
                              concept_filter: Optional[str] = None
                              ) -> List[Dict]:
        """Return top-k wrong-models by cosine similarity to `text`.

        Args:
          concept_filter: if given, restrict to wrong-models for that
                          concept (e.g. only NP-A/B/C when concept='null_pointer').
        """
        if self.wm_emb is None or not self.wm_ids:
            return []
        import torch
        q = self._embed_query(text)
        sims = (self.wm_emb @ q).tolist()  # (60,) cosine since normalised

        rows = list(range(len(self.wm_ids)))
        if concept_filter is not None:
            rows = [i for i in rows if self.wm_concept[i] == concept_filter]

        rows.sort(key=lambda i: sims[i], reverse=True)
        out = []
        for i in rows[:top_k]:
            m = dict(self.wm_meta[i])
            m["similarity"] = float(sims[i])
            out.append(m)
        return out

    def retrieve_lp_rubric(self, text: str, top_k: int = 3,
                           concept_filter: Optional[str] = None
                           ) -> List[Dict]:
        """Return top-k LP rubric entries by cosine similarity."""
        if self.lp_emb is None or not self.lp_keys:
            return []
        import torch
        q = self._embed_query(text)
        sims = (self.lp_emb @ q).tolist()

        rows = list(range(len(self.lp_keys)))
        if concept_filter is not None:
            rows = [i for i in rows if self.lp_concept[i] == concept_filter]

        rows.sort(key=lambda i: sims[i], reverse=True)
        out = []
        for i in rows[:top_k]:
            out.append({
                "concept":     self.lp_concept[i],
                "level":       self.lp_level[i],
                "text":        self.lp_text[i],
                "similarity":  float(sims[i]),
            })
        return out

    # ------------------------------------------------------------------ #
    # Hybrid scoring (classifier prob + retrieval similarity)            #
    # ------------------------------------------------------------------ #

    def hybrid_rank_wrong_models(self, text: str,
                                 classifier_probs: Dict[str, float],
                                 alpha: float = 0.4,
                                 top_k: int = 3,
                                 concept_filter: Optional[str] = None
                                 ) -> List[Dict]:
        """
        Combine classifier output (per-id probabilities) with cosine
        similarity. Both are squashed to [0,1] then linearly blended:
            hybrid = alpha * P(classifier) + (1 - alpha) * cosine

        Default alpha=0.4 leans on retrieval slightly more, since the
        WM head's val_acc is ~0.04 — retrieval is a stronger signal in
        practice.
        """
        if self.wm_emb is None or not self.wm_ids:
            return []
        import torch
        q = self._embed_query(text)
        sims = (self.wm_emb @ q).tolist()

        # Min-max normalise cosine to [0,1] over the candidate set
        rows = list(range(len(self.wm_ids)))
        if concept_filter is not None:
            rows = [i for i in rows if self.wm_concept[i] == concept_filter]
        if not rows:
            return []
        cand_sims = [sims[i] for i in rows]
        s_lo, s_hi = min(cand_sims), max(cand_sims)
        s_rng = max(s_hi - s_lo, 1e-6)
        sim_norm = {i: (sims[i] - s_lo) / s_rng for i in rows}

        # Classifier probs already sum to 1 across 60 classes. Re-normalise
        # over the candidate set so prob and sim are on the same scale.
        cls_in_set = [classifier_probs.get(self.wm_ids[i], 0.0) for i in rows]
        cls_sum = sum(cls_in_set) or 1e-6
        cls_norm = {i: classifier_probs.get(self.wm_ids[i], 0.0) / cls_sum
                    for i in rows}

        scored = []
        for i in rows:
            score = alpha * cls_norm[i] + (1 - alpha) * sim_norm[i]
            row = dict(self.wm_meta[i])
            row.update({
                "similarity":      float(sims[i]),
                "classifier_prob": float(classifier_probs.get(self.wm_ids[i], 0.0)),
                "hybrid_score":    float(score),
                "alpha":           alpha,
            })
            scored.append(row)

        scored.sort(key=lambda r: r["hybrid_score"], reverse=True)
        return scored[:top_k]
