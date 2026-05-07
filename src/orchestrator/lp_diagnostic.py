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

    # HVSAE semantic-matcher audit trail (populated when HVSAE is available).
    # Lets downstream/debug code see WHY a wrong model or LP level was picked
    # when the decision came from the trained encoder rather than overlap.
    source: str = "overlap"                # "trained_wm_head" | "hvsae" | "overlap" | ...
    semantic_wm_top3: List[Dict] = field(default_factory=list)  # [{wm_id, score, signal}]
    semantic_lp_scores: Dict[str, float] = field(default_factory=dict)  # {"L1":0.12,...}
    hvsae_concept_top3: List[Dict] = field(default_factory=list)  # from misconception_probs
    # Trained-head outputs (probabilities), for auditability:
    trained_wm_probs: List[Dict] = field(default_factory=list)   # [{wm_id, prob}] within concept
    trained_lp_probs: Dict[str, float] = field(default_factory=dict)  # {"L1":.., "L2":..}

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
            "source": self.source,
            "semantic_wm_top3": list(self.semantic_wm_top3),
            "semantic_lp_scores": dict(self.semantic_lp_scores),
            "hvsae_concept_top3": list(self.hvsae_concept_top3),
            "trained_wm_probs": list(self.trained_wm_probs),
            "trained_lp_probs": dict(self.trained_lp_probs),
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

# -- HVSAE semantic matcher -----------------------------------------------
#
# Uses the pretrained HVSAE TextEncoder (128-d BiLSTM over a 6000-token
# vocab, trained on ProgSnap2 + CodeNet) to encode every catalogue signal
# and rubric line into a shared embedding space at init. At diagnose time
# the student's text is encoded the same way and cosine-matched against
# the bank.
#
# This is what lets the system handle diverse student vocabulary: a
# paraphrase like "duplicates should be identical" lands near SE-B's
# documented signal "a copy is the same thing" in HVSAE's latent space
# even though they share no content words. The overlap-ratio matcher
# (kept as fallback) would miss that; the semantic matcher won't.

class HVSAEMatcher:
    """HVSAE-powered semantic scorer for wrong-model id and LP-level."""

    # HVSAE was trained with bert-base-uncased tokenizer + modulo 6000 to
    # fit its embedding table. We replicate that pattern.
    TEXT_VOCAB = 6000
    MAX_TEXT_LEN = 64

    def __init__(self, hvsae_model, catalogue: MentalModelsCatalogue,
                 tokenizer=None, min_cosine_wm: float = 0.30,
                 min_cosine_lp: float = 0.20):
        self.hvsae = hvsae_model
        self.catalogue = catalogue
        self.tokenizer = tokenizer or self._try_load_bert()
        self.min_cosine_wm = min_cosine_wm
        self.min_cosine_lp = min_cosine_lp
        # Caches: concept_id -> list[{wm_id, belief, origin, signal, emb}]
        self.signal_bank: Dict[str, List[Dict]] = {}
        # concept_id -> {"L1": emb, ..., "L4": emb}
        self.rubric_bank: Dict[str, Dict[str, "torch.Tensor"]] = {}
        self._build_banks()

    @staticmethod
    def _try_load_bert():
        try:
            from transformers import AutoTokenizer
            return AutoTokenizer.from_pretrained("bert-base-uncased")
        except Exception:
            return None  # fall back to hash tokenizer

    def _tokenize(self, text: str):
        import torch
        text = (text or "").strip() or "empty"
        if self.tokenizer is not None:
            enc = self.tokenizer(
                text, return_tensors="pt", padding=True,
                truncation=True, max_length=self.MAX_TEXT_LEN,
            )
            ids = enc["input_ids"].long() % self.TEXT_VOCAB
        else:
            # Deterministic fallback: hash each word into vocab range.
            # Not HVSAE-optimal (random lookups into the embedding table)
            # but still consistent between student text and catalogue text,
            # so cosines are meaningful, just noisier.
            words = text.lower().split()[: self.MAX_TEXT_LEN]
            ids = torch.tensor(
                [[abs(hash(w)) % self.TEXT_VOCAB for w in words]],
                dtype=torch.long,
            )
        return ids

    def _encode(self, text: str):
        import torch
        ids = self._tokenize(text)
        with torch.no_grad():
            emb = self.hvsae.text_encoder(ids)  # (1, 128)
        return emb[0]

    def _build_banks(self) -> None:
        for concept_id in self.catalogue.all_concepts():
            entry = self.catalogue.get_concept(concept_id)
            if entry is None:
                continue
            per_concept: List[Dict] = []
            for wm in entry.wrong_models:
                for sig in wm.conversation_signals:
                    per_concept.append({
                        "wm_id": wm.id,
                        "belief": wm.wrong_belief,
                        "origin": wm.origin,
                        "signal": sig,
                        "emb": self._encode(sig),
                    })
            self.signal_bank[concept_id] = per_concept
            self.rubric_bank[concept_id] = {
                lvl: self._encode(entry.lp_rubric[lvl])
                for lvl in LP_ORDER if lvl in entry.lp_rubric
            }
        total_sigs = sum(len(v) for v in self.signal_bank.values())
        total_rubs = sum(len(v) for v in self.rubric_bank.values())
        print(f"[LP-Diag/HVSAE] embedding bank: "
              f"{total_sigs} signals + {total_rubs} rubric lines")

    @staticmethod
    def _cosine(a, b) -> float:
        import torch
        return float(torch.nn.functional.cosine_similarity(
            a.unsqueeze(0), b.unsqueeze(0)
        ).item())

    def rank_wrong_models(self, student_text: str,
                          concept_id: str) -> List[Dict]:
        if concept_id not in self.signal_bank:
            return []
        stud = self._encode(student_text)
        best_per_wm: Dict[str, Dict] = {}
        for item in self.signal_bank[concept_id]:
            score = self._cosine(stud, item["emb"])
            cur = best_per_wm.get(item["wm_id"])
            if (cur is None) or (score > cur["score"]):
                best_per_wm[item["wm_id"]] = {
                    "wm_id": item["wm_id"],
                    "score": score,
                    "signal": item["signal"],
                    "belief": item["belief"],
                    "origin": item["origin"],
                }
        ranked = sorted(best_per_wm.values(),
                        key=lambda d: d["score"], reverse=True)
        return ranked

    def rank_lp_levels(self, student_text: str,
                       concept_id: str) -> List[Dict]:
        if concept_id not in self.rubric_bank:
            return []
        stud = self._encode(student_text)
        return sorted(
            [{"level": lvl, "score": self._cosine(stud, emb)}
             for lvl, emb in self.rubric_bank[concept_id].items()],
            key=lambda d: d["score"], reverse=True,
        )


# -- LPDiagnostician ------------------------------------------------------

class LPDiagnostician:
    """
    CPAL Stage 1 orchestrator.

    With `hvsae_model` provided, uses the trained HVSAE TextEncoder for
    semantic wrong-model and LP-level matching; the overlap-ratio matcher
    becomes a fallback for low-confidence cases and an audit trail.

    Without `hvsae_model`, runs the original overlap-only path — every
    existing caller continues to work unchanged.
    """

    def __init__(self, catalogue: Optional[MentalModelsCatalogue] = None,
                 hvsae_model=None, tokenizer=None,
                 lp_head_path: Optional[str] = None,
                 wm_head_path: Optional[str] = None):
        self.catalogue = catalogue or get_catalogue()
        self.semantic: Optional[HVSAEMatcher] = None
        self.lp_head = None         # trained 4-class head on HVSAE latent
        self.wm_head = None         # trained (20*3)-class head on HVSAE latent
        self.wm_head_labels = None  # list of (concept, wm_id) for decoding
        self.lp_head_labels = None  # list of ["L1","L2","L3","L4"]
        if hvsae_model is not None:
            try:
                self.semantic = HVSAEMatcher(
                    hvsae_model=hvsae_model,
                    catalogue=self.catalogue,
                    tokenizer=tokenizer,
                )
            except Exception as e:
                print(f"[LP-Diag] HVSAE matcher init failed ({e}); "
                      f"falling back to overlap matcher.")
                self.semantic = None
        # Optional: load the trained LP + WM heads
        self._load_heads(lp_head_path, wm_head_path)

    def _load_heads(self, lp_head_path, wm_head_path):
        """Load the LP and WM heads.

        Prefers checkpoints/cpal_lp_head_st.pt (sentence-transformers
        based, val_acc ~0.74) over checkpoints/cpal_lp_head.pt (HVSAE
        latent based, val_acc ~0.33).

        WM head always uses HVSAE latent (val_acc ~0.04 — weak but
        better than overlap for paraphrases).
        """
        import os as _os
        default_lp_hvsae = "checkpoints/cpal_lp_head.pt"
        default_lp_st    = "checkpoints/cpal_lp_head_st.pt"
        lp_head_path = lp_head_path or default_lp_hvsae
        wm_head_path = wm_head_path or "checkpoints/cpal_wm_subhead.pt"
        import torch as _t
        import torch.nn as _nn

        def _build_mlp(in_dim, num_classes, hidden=128):
            return _nn.Sequential(
                _nn.Linear(in_dim, hidden), _nn.ReLU(), _nn.Dropout(0.3),
                _nn.Linear(hidden, hidden // 2), _nn.ReLU(), _nn.Dropout(0.3),
                _nn.Linear(hidden // 2, num_classes),
            )

        # --- Load sentence-transformers LP head if present (preferred) ---
        self.lp_st_encoder = None   # sentence_transformers model
        self.lp_st_head    = None
        if _os.path.exists(default_lp_st):
            try:
                ck = _t.load(default_lp_st, map_location="cpu",
                             weights_only=False)
                from sentence_transformers import SentenceTransformer
                self.lp_st_encoder = SentenceTransformer(
                    ck.get("encoder", "sentence-transformers/all-MiniLM-L6-v2")
                )
                h = _build_mlp(ck["in_dim"], ck["num_classes"])
                sd = {k.replace("net.", ""): v for k, v in ck["state_dict"].items()}
                h.load_state_dict(sd)
                h.eval()
                self.lp_st_head    = h
                self.lp_head_labels = ck["labels"]   # shared labels
                print(f"[LP-Diag] LP head (sentence-transformers) loaded: "
                      f"val_acc={ck.get('val_acc', '?'):.3f}  "
                      f"on {ck.get('num_examples', '?')} examples")
            except Exception as e:
                print(f"[LP-Diag] failed to load ST LP head: {e}")
                self.lp_st_encoder = None
                self.lp_st_head    = None

        for tag, p, attr_head, attr_lbl in [
            ("LP", lp_head_path, "lp_head", "lp_head_labels"),
            ("WM", wm_head_path, "wm_head", "wm_head_labels"),
        ]:
            if not _os.path.exists(p):
                continue
            try:
                ck = _t.load(p, map_location="cpu", weights_only=False)
                head = _build_mlp(ck["in_dim"], ck["num_classes"])
                # remap 'net.X.Y' -> 'X.Y'
                sd = {k.replace("net.", ""): v for k, v in ck["state_dict"].items()}
                head.load_state_dict(sd)
                head.eval()
                setattr(self, attr_head, head)
                setattr(self, attr_lbl, ck["labels"])
                print(f"[LP-Diag] trained {tag} head loaded: "
                      f"{ck['num_classes']} classes, "
                      f"trained on {ck.get('num_examples','?')} examples")
            except Exception as e:
                print(f"[LP-Diag] failed to load {tag} head from {p}: {e}")

    def diagnose(self,
                 student_id: str,
                 concept: str,
                 question_text: str,
                 stored_lp_level: Optional[str] = None,
                 stored_lp_streak: int = 0,
                 hvsae_latent=None,
                 hvsae_misconception_probs=None) -> LPDiagnostic:
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

        # -- Optional: read HVSAE's own concept prediction (20-class head) --
        # If misconception_probs is available we cache the top-3 for audit.
        if hvsae_misconception_probs is not None:
            try:
                import torch as _t
                probs = hvsae_misconception_probs.detach().view(-1)
                top = _t.topk(probs, k=min(3, probs.numel()))
                concept_ids = self.catalogue.all_concepts()
                diag.hvsae_concept_top3 = [
                    {"concept_id": concept_ids[i] if i < len(concept_ids) else f"idx_{i}",
                     "prob": float(probs[i].item())}
                    for i in top.indices.tolist()
                ]
            except Exception:
                pass  # audit-only; don't break diagnosis

        # -- Trained heads (primary path when available) ------------------
        # These heads sit on top of frozen HVSAE latent and are trained on
        # catalogue text + Ollama paraphrases. When confident, they take
        # precedence over cosine-matching and the overlap matcher.
        trained_wm_hit = None        # set by WM head
        trained_lp_level = None      # set by LP head

        # --- Sentence-transformers LP head (preferred if present) ---
        # Runs directly on question_text — doesn't need HVSAE latent.
        if self.lp_st_head is not None and self.lp_st_encoder is not None:
            try:
                import torch as _t
                emb = self.lp_st_encoder.encode(
                    [question_text], convert_to_tensor=True
                ).cpu().float()
                with _t.no_grad():
                    logits = self.lp_st_head(emb).squeeze(0)
                lp_probs = _t.softmax(logits, dim=-1)
                diag.trained_lp_probs = {
                    self.lp_head_labels[i]: float(lp_probs[i].item())
                    for i in range(len(self.lp_head_labels))
                }
                top_idx = int(lp_probs.argmax().item())
                # Accept ST LP head with a lower threshold — it's 3x chance
                if float(lp_probs[top_idx].item()) >= 0.40:
                    trained_lp_level = self.lp_head_labels[top_idx]
            except Exception as _e:
                print(f"[LP-Diag] ST LP head inference failed: {_e}")

        if hvsae_latent is not None:
            try:
                import torch as _t
                latent_flat = hvsae_latent.detach().view(1, -1).float()
                # --- Wrong-model sub-head (60-class over (concept, wm)) --
                if self.wm_head is not None and self.wm_head_labels is not None:
                    with _t.no_grad():
                        logits = self.wm_head(latent_flat).squeeze(0)
                    # Restrict to classes belonging to this concept
                    this_concept_idx = [
                        i for i, (c, _w) in enumerate(self.wm_head_labels)
                        if c == concept
                    ]
                    if this_concept_idx:
                        sub_logits = logits[this_concept_idx]
                        sub_probs = _t.softmax(sub_logits, dim=-1)
                        top = int(sub_probs.argmax().item())
                        chosen_label_idx = this_concept_idx[top]
                        chosen_concept, chosen_wm = self.wm_head_labels[chosen_label_idx]
                        confidence = float(sub_probs[top].item())
                        # Audit: all 3 sub-class probabilities for this concept
                        wm_top_for_concept = [
                            {"wm_id": self.wm_head_labels[this_concept_idx[i]][1],
                             "prob":  float(sub_probs[i].item())}
                            for i in range(len(this_concept_idx))
                        ]
                        wm_top_for_concept.sort(key=lambda d: d["prob"], reverse=True)
                        diag.trained_wm_probs = wm_top_for_concept
                        # Accept head's decision if reasonably confident
                        if confidence >= 0.45:
                            wm_obj = self.catalogue.get_wrong_model(
                                concept, chosen_wm)
                            if wm_obj is not None:
                                trained_wm_hit = {
                                    "wm_id":  chosen_wm,
                                    "belief": wm_obj.wrong_belief,
                                    "origin": wm_obj.origin,
                                    "signal": f"[trained-head match p={confidence:.2f}]",
                                    "score":  confidence,
                                }
                # --- LP-level head (HVSAE latent, fallback) -------------
                # Only fires when the better ST-based LP head didn't
                # already set a confident level (trained_lp_level None).
                if (trained_lp_level is None
                        and self.lp_head is not None
                        and self.lp_head_labels is not None
                        and not diag.trained_lp_probs):
                    with _t.no_grad():
                        lp_logits = self.lp_head(latent_flat).squeeze(0)
                    lp_probs = _t.softmax(lp_logits, dim=-1)
                    diag.trained_lp_probs = {
                        self.lp_head_labels[i]: float(lp_probs[i].item())
                        for i in range(len(self.lp_head_labels))
                    }
                    top_idx = int(lp_probs.argmax().item())
                    if float(lp_probs[top_idx].item()) >= 0.45:
                        trained_lp_level = self.lp_head_labels[top_idx]
            except Exception as _e:
                # heads available but failed — keep fallback path
                print(f"[LP-Diag] trained-head inference failed: {_e}")

        # -- Job 1: Wrong-model identification ----------------------------
        # Preferred: HVSAE semantic matcher (handles paraphrases).
        # Fallback: overlap-ratio matcher (handles exact-signal cases,
        # also runs when cosine confidence is low).
        semantic_hit = None
        if self.semantic is not None:
            ranked = self.semantic.rank_wrong_models(question_text, concept)
            diag.semantic_wm_top3 = [
                {"wm_id": r["wm_id"], "score": r["score"], "signal": r["signal"]}
                for r in ranked[:3]
            ]
            if ranked and ranked[0]["score"] >= self.semantic.min_cosine_wm:
                semantic_hit = ranked[0]

        # Preference order: trained WM head > HVSAE cosine > overlap
        if trained_wm_hit is not None:
            diag.wrong_model_id          = trained_wm_hit["wm_id"]
            diag.wrong_model_description = trained_wm_hit["belief"]
            diag.wrong_model_origin      = trained_wm_hit["origin"]
            diag.matched_signal          = trained_wm_hit["signal"]
            diag.match_score             = float(trained_wm_hit["score"])
            diag.source                  = "trained_wm_head"
        elif semantic_hit is not None:
            diag.wrong_model_id          = semantic_hit["wm_id"]
            diag.wrong_model_description = semantic_hit["belief"]
            diag.wrong_model_origin      = semantic_hit["origin"]
            diag.matched_signal          = semantic_hit["signal"]
            diag.match_score             = float(semantic_hit["score"])
            diag.source                  = "hvsae"
        else:
            # Fallback (or primary if HVSAE not loaded)
            match: WrongModelMatch = self.catalogue.match_wrong_model(
                question_text=question_text,
                concept_id=concept,
            )
            diag.wrong_model_id          = match.wrong_model_id
            diag.wrong_model_description = match.wrong_belief
            diag.wrong_model_origin      = match.origin
            diag.matched_signal          = match.matched_signal
            diag.match_score             = match.match_score
            diag.source = "overlap" if self.semantic is None else "hvsae+overlap"

        # -- Job 2: LP level classification -------------------------------
        # Preference order: trained LP head > (lexical + HVSAE cosine blend)
        clf = classify_lp_level(question_text)
        current_lp_level = clf["level"]
        diag.logical_step        = clf["logical_step"]
        diag.logical_step_detail = clf["logical_step_detail"]
        diag.lp_signals_detected = clf["signals_detected"]

        if trained_lp_level is not None:
            # Trained head wins when confident
            current_lp_level = trained_lp_level
        elif self.semantic is not None:
            lp_ranked = self.semantic.rank_lp_levels(question_text, concept)
            diag.semantic_lp_scores = {r["level"]: r["score"] for r in lp_ranked}
            if lp_ranked and lp_ranked[0]["score"] >= self.semantic.min_cosine_lp:
                sem_level = lp_ranked[0]["level"]
                sem_idx = LP_INDEX[sem_level]
                lex_idx = LP_INDEX[current_lp_level]
                # When they agree, no change. When they disagree by one
                # level, take the higher (evidence of more reasoning wins).
                # When they disagree by 2+, keep lexical — large gaps are
                # usually HVSAE noise, not genuine signal.
                if abs(sem_idx - lex_idx) == 1:
                    current_lp_level = LP_ORDER[max(sem_idx, lex_idx)]

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
