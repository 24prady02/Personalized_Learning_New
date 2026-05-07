"""
LPProgressionRNN — Stage 2 intervention-ranking model.

This is the sequence model called out in the methodology document
(mental_models_cpal_methodology.docx, Part 3 Stage 2 and Stage 5). It
consumes the student's historical session_state_vectors for a given
concept and outputs a ranked list of intervention types.

The critical design point is that the ranking is *historical*, not
per-session. From Part 3 Stage 5:

    "The LPProgressionRNN processes only the current session's state
     vector instead of the full historical sequence. The temporal
     learning pattern that is the architecture's core strength —
     learning that trace_scaffold after two worked_example failures
     produces L2→L3 gain — cannot be learned from a single-session
     vector."

So the RNN takes a variable-length sequence of state vectors, runs a
GRU over them, and produces logits over the intervention vocabulary.
The caller (Stage 2) then filters those logits through the LP-level
validity gate (LPDiagnostic.filter_interventions_by_lp) before picking
the top intervention.

State vector layout (dimension = 12):
    0  mastery                (0-1)
    1  lp_level_idx           (0=L1, 1=L2, 2=L3, 3=L4; normalised to 0-1)
    2  logical_step           (0/1)
    3  logical_step_detail    (0/1)
    4  lp_streak              (normalised / 5)
    5  plateau_flag           (0/1)
    6  delta_lp_last          (-3..+3 / 3)
    7  last_intervention_idx  (/ num_interventions)
    8  emotion_valence        (-1..+1)
    9  encoding_strength      (0=surface, 0.5=partial, 1=solid/deep)
    10 stage                  (1..5 / 5)
    11 scaffold_level         (1..5 / 5)

The model is trained by Stage 4's post-reply LP assessment loop:
delta_lp from one session becomes the reward signal for the (state,
intervention) pair that produced it. See _learn_from_session wiring in
orchestrator.py (Turn 2).

The intervention vocabulary is drawn from the methodology's LP-
validity table (LP_VALID_INTERVENTIONS in lp_diagnostic.py) merged
with the interventions already used by InterventionSelector.
"""
from __future__ import annotations

from typing import Dict, List, Optional, Tuple

try:
    import torch
    import torch.nn as nn
    _TORCH_OK = True
except ImportError:     # torch may be absent in light installs
    torch = None        # type: ignore
    nn = None           # type: ignore
    _TORCH_OK = False


# ──────────────────────────────────────────────────────────────────────
# Intervention vocabulary — UNION of Stage 2 selector types and the
# LP-validity table in lp_diagnostic.py. Order is fixed and used for
# both the RNN output layer and the heuristic ranker.
# ──────────────────────────────────────────────────────────────────────
INTERVENTION_VOCAB: List[str] = [
    "worked_example",
    "reduce_challenge",
    "socratic_prompt",
    "misconception_correct",
    "model_explanation",
    "attribution_reframe",
    "mastery_surface",
    "trace_scaffold",
    "transfer_prompt",
    "transfer_task",
    "increase_challenge",
    "validate_and_advance",
]
INTERVENTION_TO_IDX: Dict[str, int] = {t: i for i, t in enumerate(INTERVENTION_VOCAB)}
NUM_INTERVENTIONS = len(INTERVENTION_VOCAB)

STATE_DIM = 12


# ──────────────────────────────────────────────────────────────────────
# State-vector builder
# ──────────────────────────────────────────────────────────────────────
_LP_IDX = {"L1": 0, "L2": 1, "L3": 2, "L4": 3}
_ENC_SCORE = {"surface": 0.0, "partial": 0.5, "solid": 0.85, "deep": 1.0}
_EMOTION_VALENCE = {
    "frustrated": -0.8, "anxious": -0.7, "confused": -0.3,
    "neutral": 0.0, "engaged": 0.5, "confident": 0.9,
}


def build_state_vector(lp_state: Optional[Dict],
                       intervention_type: Optional[str] = None,
                       delta_lp_last: int = 0,
                       emotion: str = "neutral",
                       encoding_strength: str = "surface",
                       stage: int = 1,
                       scaffold_level: int = 3,
                       mastery: float = 0.30) -> List[float]:
    """Build a single 12-d state vector from the current LP + channel state."""
    lp_state = lp_state or {}
    lp_level    = lp_state.get("lp_level", "L1")
    lp_streak   = int(lp_state.get("lp_streak", 0))
    step_flag   = 1.0 if lp_state.get("logical_step", False) else 0.0
    detail_flag = 1.0 if lp_state.get("logical_step_detail", False) else 0.0
    plateau     = 1.0 if lp_state.get("plateau_flag", False) else 0.0
    int_idx     = INTERVENTION_TO_IDX.get(intervention_type or "", -1)

    return [
        float(max(0.0, min(1.0, mastery))),
        _LP_IDX.get(lp_level, 0) / 3.0,
        step_flag,
        detail_flag,
        max(0.0, min(1.0, lp_streak / 5.0)),
        plateau,
        max(-1.0, min(1.0, delta_lp_last / 3.0)),
        (int_idx + 1) / NUM_INTERVENTIONS if int_idx >= 0 else 0.0,
        _EMOTION_VALENCE.get(emotion, 0.0),
        _ENC_SCORE.get(encoding_strength, 0.0),
        max(0.0, min(1.0, float(_stage_as_int(stage)) / 5.0)),
        max(0.0, min(1.0, float(scaffold_level) / 5.0)),
    ]


def _stage_as_int(stage) -> int:
    """Handle stage values like '4a', '4b', 5, etc."""
    if isinstance(stage, int):
        return stage
    if isinstance(stage, str):
        # strip trailing letters ('4a' -> 4)
        digits = ''.join(c for c in stage if c.isdigit())
        if digits:
            return int(digits)
    return 1


# ──────────────────────────────────────────────────────────────────────
# LPProgressionRNN (torch)
# ──────────────────────────────────────────────────────────────────────
if _TORCH_OK:

    class LPProgressionRNN(nn.Module):
        """GRU over historical session-state vectors.

        Input shape:  (batch, seq_len, STATE_DIM)
        Output shape: (batch, NUM_INTERVENTIONS)  — intervention logits

        For single-student inference, wrap a list of vectors as
        tensor([vectors]).unsqueeze(0) and take the returned logits[0].
        """

        def __init__(self, state_dim: int = STATE_DIM,
                     num_interventions: int = NUM_INTERVENTIONS,
                     hidden_dim: int = 64,
                     num_layers: int = 1,
                     dropout: float = 0.1):
            super().__init__()
            self.state_dim = state_dim
            self.num_interventions = num_interventions

            self.gru = nn.GRU(
                input_size  = state_dim,
                hidden_size = hidden_dim,
                num_layers  = num_layers,
                batch_first = True,
                dropout     = dropout if num_layers > 1 else 0.0,
            )
            self.head = nn.Sequential(
                nn.LayerNorm(hidden_dim),
                nn.Dropout(dropout),
                nn.Linear(hidden_dim, num_interventions),
            )

        def forward(self, seq: "torch.Tensor") -> "torch.Tensor":
            # seq: (B, T, STATE_DIM). Use final hidden state.
            _, h = self.gru(seq)
            last = h[-1]  # (B, hidden_dim)
            return self.head(last)

        def rank(self, session_state_vectors: List[List[float]]
                 ) -> List[Tuple[str, float]]:
            """Single-student inference convenience.

            Returns a list of (intervention_type, score) in descending
            score order. Scores are the raw logits — the caller may
            softmax them if a probability is needed.
            """
            if not session_state_vectors:
                return []
            self.eval()
            with torch.no_grad():
                x = torch.tensor([session_state_vectors],
                                 dtype=torch.float32)
                logits = self(x)[0]  # (NUM_INTERVENTIONS,)
                scores = logits.cpu().tolist()
            ranked = sorted(
                zip(INTERVENTION_VOCAB, scores),
                key=lambda p: p[1],
                reverse=True,
            )
            return ranked

else:

    LPProgressionRNN = None  # type: ignore


# ──────────────────────────────────────────────────────────────────────
# Heuristic fallback — used when torch is unavailable OR no training
# has occurred yet (cold-start). This ranker honours the LP-level
# bias encoded in LP_VALID_INTERVENTIONS so Stage 2 still does
# something sensible on day 1.
# ──────────────────────────────────────────────────────────────────────
_LP_LEVEL_PREFERENCES: Dict[str, List[Tuple[str, float]]] = {
    # Orderings chosen to match the methodology's L1-L4 rubric rationale:
    # L1 students get structure, L2 students get mechanism scaffolding,
    # L3 students get transfer, L4 students get challenge.
    "L1": [
        ("worked_example",          0.85),
        ("model_explanation",       0.78),
        ("reduce_challenge",        0.72),
        ("socratic_prompt",         0.60),
        ("misconception_correct",   0.55),
        ("attribution_reframe",     0.40),
    ],
    "L2": [
        ("trace_scaffold",          0.90),   # plateau-break default
        ("socratic_prompt",         0.80),
        ("misconception_correct",   0.75),
        ("worked_example",          0.68),
        ("model_explanation",       0.55),
    ],
    "L3": [
        ("transfer_prompt",         0.88),
        ("transfer_task",           0.82),
        ("socratic_prompt",         0.72),
        ("increase_challenge",      0.68),
    ],
    "L4": [
        ("transfer_task",           0.90),
        ("transfer_prompt",         0.85),
        ("increase_challenge",      0.78),
    ],
}


def heuristic_rank(lp_level: str,
                    plateau_flag: bool = False) -> List[Tuple[str, float]]:
    """Heuristic intervention ranking for cold-start Stage 2.

    Called when LPProgressionRNN is unavailable (torch missing, or
    policy not yet trained). Returns (intervention_type, score) pairs
    sorted by descending score. Plateau flag pins trace_scaffold to
    the top.
    """
    base = list(_LP_LEVEL_PREFERENCES.get(lp_level, _LP_LEVEL_PREFERENCES["L1"]))
    if plateau_flag:
        # Remove any existing trace_scaffold entry, then prepend.
        base = [(t, s) for t, s in base if t != "trace_scaffold"]
        base.insert(0, ("trace_scaffold", 1.0))
    return base


# ──────────────────────────────────────────────────────────────────────
# Public facade — one entry point Stage 2 calls regardless of whether
# torch is installed and a trained policy exists.
# ──────────────────────────────────────────────────────────────────────
class LPProgressionRanker:
    """Facade: Stage 2 calls rank() and gets a ranked intervention list.

    The ranker tries the trained RNN first; if the RNN is unavailable
    or returns nothing useful (empty history, etc.), it falls back to
    the heuristic ranker. This keeps the system functional on day 1
    and lets the trained model take over once it has data.
    """

    def __init__(self, rnn_model: Optional["LPProgressionRNN"] = None):
        self.rnn = rnn_model

    def rank(self, session_state_vectors: List[List[float]],
             lp_level: str,
             plateau_flag: bool = False) -> List[Tuple[str, float]]:
        # 1. Try the trained RNN if we have one AND enough history.
        # A single vector is useless to a recurrent model — the whole
        # point is temporal pattern. Require at least 2 historical
        # sessions before trusting the RNN output.
        if (self.rnn is not None
                and _TORCH_OK
                and len(session_state_vectors) >= 2):
            try:
                ranked = self.rnn.rank(session_state_vectors)
                if ranked:
                    # If plateau is set, force trace_scaffold to the top.
                    if plateau_flag:
                        ranked = [(t, s) for t, s in ranked
                                  if t != "trace_scaffold"]
                        ranked.insert(0, ("trace_scaffold", 1.0))
                    return ranked
            except Exception as e:
                print(f"[LPRNN] rank failed, falling back: {e}")

        # 2. Heuristic fallback.
        return heuristic_rank(lp_level, plateau_flag=plateau_flag)


# ──────────────────────────────────────────────────────────────────────
# Smoke test
# ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print(f"torch available: {_TORCH_OK}")
    print(f"STATE_DIM: {STATE_DIM}  NUM_INTERVENTIONS: {NUM_INTERVENTIONS}")

    # Build a few state vectors
    v1 = build_state_vector(
        lp_state={"lp_level": "L1", "lp_streak": 0,
                  "logical_step": False, "logical_step_detail": False},
        intervention_type=None, delta_lp_last=0, emotion="confused",
        encoding_strength="surface", stage=1, scaffold_level=4,
        mastery=0.25,
    )
    v2 = build_state_vector(
        lp_state={"lp_level": "L2", "lp_streak": 1,
                  "logical_step": True, "logical_step_detail": False},
        intervention_type="worked_example", delta_lp_last=1,
        emotion="neutral", encoding_strength="partial",
        stage=2, scaffold_level=3, mastery=0.48,
    )
    v3 = build_state_vector(
        lp_state={"lp_level": "L2", "lp_streak": 2,
                  "logical_step": True, "logical_step_detail": False,
                  "plateau_flag": True},
        intervention_type="worked_example", delta_lp_last=0,
        emotion="confused", encoding_strength="partial",
        stage=2, scaffold_level=3, mastery=0.52,
    )
    print(f"v1 (L1): {[f'{x:.2f}' for x in v1]}")
    print(f"v2 (L2): {[f'{x:.2f}' for x in v2]}")
    print(f"v3 (L2-plateau): {[f'{x:.2f}' for x in v3]}")

    # Heuristic rank at each level
    for lvl in ("L1", "L2", "L3", "L4"):
        print(f"\nheuristic L={lvl}")
        for t, s in heuristic_rank(lvl)[:3]:
            print(f"  {t:<22} {s:.2f}")

    print("\nheuristic L2 + plateau:")
    for t, s in heuristic_rank("L2", plateau_flag=True)[:3]:
        print(f"  {t:<22} {s:.2f}")

    if _TORCH_OK:
        # Build an untrained RNN, confirm rank() doesn't crash
        model = LPProgressionRNN()
        ranker = LPProgressionRanker(model)
        print("\nLPProgressionRanker (untrained RNN, 3-session history, L2 plateau):")
        ranked = ranker.rank([v1, v2, v3], "L2", plateau_flag=True)
        for t, s in ranked[:5]:
            print(f"  {t:<22} {s:.3f}")

        print("\nLPProgressionRanker (untrained RNN, only 1-session history, L1):")
        # With <2 sessions, facade should fall back to heuristic
        ranked_hs = ranker.rank([v1], "L1", plateau_flag=False)
        for t, s in ranked_hs[:3]:
            print(f"  {t:<22} {s:.3f}")
    else:
        print("\n(torch not installed — heuristic-only mode)")
        ranker = LPProgressionRanker(None)
        print("\nLPProgressionRanker fallback (no torch), L2 plateau:")
        for t, s in ranker.rank([v1, v2, v3], "L2", plateau_flag=True)[:3]:
            print(f"  {t:<22} {s:.2f}")
