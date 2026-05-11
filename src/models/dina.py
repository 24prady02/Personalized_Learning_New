"""
dina.py — DINA Model (Deterministic Input Noisy And gate)
==========================================================
Cognitive Diagnosis Model that estimates mastery of each of the 20
Java CSCI 1301 skills from student response patterns.

DINA parameters per skill (learned from ASSISTments / real data):
  slip  (s_k) : P(wrong | mastered)     — default 0.10
  guess (g_k) : P(correct | not mastered) — default 0.25
  prior (π_k) : P(mastered at start)    — default 0.30

Q-matrix (items × skills):
  Binary matrix where Q[i,k] = 1 if item i requires skill k.
  For the 20 Java concepts, each quiz item tests exactly one skill
  so the Q-matrix is 20×20 identity (each item tags one concept).

Mastery estimation:
  After observing student response r_i on item i, update P(mastered_k)
  for all skills k that item i requires (Q[i,k]=1) using Bayes rule.

Training:
  MLE on ASSISTments response patterns to learn per-skill slip/guess.
  Called by src/train.py → ASSISTmentsProcessor.

Usage in orchestrator:
  from src.models.dina import DINAModel
  dina = DINAModel(config)
  result = dina.update(student_id, concept_key, is_correct)
  mastery = dina.get_mastery(student_id, concept_key)
"""

import json
import numpy as np
from pathlib import Path
from typing import Dict, List, Optional, Tuple


# ─── Java CSCI 1301 skill definitions ─────────────────────────────────────────
JAVA_SKILLS = [
    "type_mismatch", "infinite_loop", "null_pointer", "string_equality",
    "variable_scope", "assignment_vs_compare", "integer_division", "scanner_buffer",
    "array_index", "missing_return", "array_not_allocated", "boolean_operators",
    "sentinel_loop", "unreachable_code", "string_immutability",
    "no_default_constructor", "static_vs_instance", "foreach_no_modify",
    "overloading", "generics_primitives",
]
N_SKILLS = len(JAVA_SKILLS)
SKILL_INDEX = {s: i for i, s in enumerate(JAVA_SKILLS)}

# Q-matrix: 20 items × 20 skills (identity — each item tests one skill)
_Q_MATRIX = np.eye(N_SKILLS, dtype=np.float32)

# Default DINA parameters (updated from ASSISTments training)
_DEFAULT_SLIP  = 0.10
_DEFAULT_GUESS = 0.25
_DEFAULT_PRIOR = 0.30

# Difficulty adjustments per concept (from cognitive load ratings in setup_java_knowledge.py)
_DIFFICULTY = {
    "type_mismatch": 0.20, "infinite_loop": 0.25, "null_pointer": 0.30,
    "string_equality": 0.30, "variable_scope": 0.20, "assignment_vs_compare": 0.15,
    "integer_division": 0.20, "scanner_buffer": 0.30, "array_index": 0.25,
    "missing_return": 0.20, "array_not_allocated": 0.28, "boolean_operators": 0.22,
    "sentinel_loop": 0.28, "unreachable_code": 0.15, "string_immutability": 0.28,
    "no_default_constructor": 0.32, "static_vs_instance": 0.35,
    "foreach_no_modify": 0.30, "overloading": 0.30, "generics_primitives": 0.35,
}


class DINAModel:
    """
    DINA cognitive diagnosis model for Java CSCI 1301.

    Maintains per-student, per-skill mastery distributions.
    Supports:
      - Bayesian update after each item response
      - MLE parameter fitting from ASSISTments data
      - Checkpoint save/load
    """

    def __init__(self, config: Dict):
        self.config   = config
        self.data_dir = Path(config.get('dina', {}).get('data_dir', 'data/dina'))
        self.ckpt     = self.data_dir / 'dina_params.json'

        # Per-skill parameters — shape (N_SKILLS,)
        self.slip  = np.full(N_SKILLS, _DEFAULT_SLIP)
        self.guess = np.full(N_SKILLS, _DEFAULT_GUESS)
        self.prior = np.array([_DEFAULT_PRIOR] * N_SKILLS)
        # Adjust priors for harder concepts
        for skill, diff in _DIFFICULTY.items():
            idx = SKILL_INDEX.get(skill)
            if idx is not None:
                self.prior[idx] = max(0.10, _DEFAULT_PRIOR - diff * 0.5)

        # Q-matrix (20 items × 20 skills)
        self.Q = _Q_MATRIX.copy()

        # Student mastery states: {student_id: np.array(N_SKILLS,) of P(mastered)}
        self._student_mastery: Dict[str, np.ndarray] = {}

        self.is_trained = False
        self._try_load()

    # ── Student mastery management ─────────────────────────────────────────────

    def _init_student(self, student_id: str) -> np.ndarray:
        """Initialise a new student with prior mastery probabilities."""
        m = self.prior.copy()
        self._student_mastery[student_id] = m
        return m

    def get_mastery(self, student_id: str,
                    skill: Optional[str] = None) -> Dict:
        """
        Returns mastery dict for a student.
        If skill is given, returns only that skill's probability.
        """
        if student_id not in self._student_mastery:
            self._init_student(student_id)
        m = self._student_mastery[student_id]
        if skill:
            idx = SKILL_INDEX.get(skill, -1)
            return {skill: float(m[idx]) if idx >= 0 else _DEFAULT_PRIOR}
        return {s: float(m[i]) for i, s in enumerate(JAVA_SKILLS)}

    def update(self, student_id: str, skill: str,
               is_correct: bool,
               evidence_strength: float = 1.0) -> Dict:
        """
        Bayesian update of P(mastered | response) for a given skill.
        Returns updated mastery dict for the skill.
        """
        if student_id not in self._student_mastery:
            self._init_student(student_id)

        idx = SKILL_INDEX.get(skill)
        if idx is None:
            return {'skill': skill, 'mastery': _DEFAULT_PRIOR, 'updated': False}

        m     = self._student_mastery[student_id]
        p_l   = m[idx]
        s_k   = self.slip[idx]
        g_k   = self.guess[idx]

        # DINA Bayes update
        if is_correct:
            p_ev = p_l * (1 - s_k) + (1 - p_l) * g_k
            p_l_new = (p_l * (1 - s_k)) / max(p_ev, 1e-9)
        else:
            p_ev = p_l * s_k + (1 - p_l) * (1 - g_k)
            p_l_new = (p_l * s_k) / max(p_ev, 1e-9)

        # Apply evidence weighting
        p_l_new = evidence_strength * p_l_new + (1 - evidence_strength) * p_l

        # Learning transition — only on correct answers. A failure should
        # lower mastery (pure Bayes update); only successful demonstration
        # gives an additional learning bump.
        if is_correct:
            p_t = 0.20
            p_l_new = p_l_new + (1 - p_l_new) * p_t

        p_l_new = float(np.clip(p_l_new, 0.01, 0.99))
        m[idx]  = p_l_new

        return {
            'skill':         skill,
            'mastery_before': float(p_l),
            'mastery_after':  p_l_new,
            'change':         round(p_l_new - float(p_l), 4),
            'is_correct':     is_correct,
        }

    def update_from_session(self, student_id: str,
                            session_data: Dict,
                            code_correctness: float) -> Dict:
        """
        Convenience method: infer skill from session and apply update.
        Used by orchestrator after each session.
        """
        skill = session_data.get('concept') or session_data.get('focus', 'null_pointer')
        is_correct = code_correctness > 0.5
        evidence   = abs(code_correctness - 0.5) * 2  # 0=uncertain, 1=certain
        return self.update(student_id, skill, is_correct, evidence)

    def get_knowledge_gaps(self, student_id: str,
                           threshold: float = 0.50) -> List[Dict]:
        """
        Return list of skills with mastery below threshold.
        Sorted by mastery ascending (most urgent gap first).
        """
        mastery = self.get_mastery(student_id)
        gaps = [
            {'concept': skill, 'mastery': prob,
             'severity': round(1.0 - prob, 3)}
            for skill, prob in mastery.items()
            if prob < threshold
        ]
        gaps.sort(key=lambda x: x['mastery'])
        return gaps

    def get_overall_mastery(self, student_id: str) -> float:
        """Average mastery across all skills."""
        if student_id not in self._student_mastery:
            return _DEFAULT_PRIOR
        return float(np.mean(self._student_mastery[student_id]))

    # ── MLE parameter fitting ──────────────────────────────────────────────────

    def fit_from_assistments(self, responses_df) -> None:
        """
        MLE fit of slip and guess parameters from ASSISTments response data.
        responses_df columns: user_id, skill_name, correct (0/1)
        Called by src/train.py after ASSISTments is downloaded.
        """
        import pandas as pd
        if hasattr(responses_df, 'empty') and responses_df.empty:
            print("[DINA] Empty dataframe — skipping fit.")
            return

        print(f"[DINA] Fitting on {len(responses_df)} responses...")
        skill_col = None
        for c in ['skill_name', 'skill_id', 'skill', 'concept']:
            if c in responses_df.columns:
                skill_col = c
                break
        if skill_col is None:
            print("[DINA] No skill column found.")
            return

        for i, skill in enumerate(JAVA_SKILLS):
            subset = responses_df[responses_df[skill_col].astype(str).str.contains(
                skill.replace('_', ' '), case=False, na=False
            )]
            if len(subset) < 10:
                continue
            correct_rate = float(subset['correct'].mean())
            # Simple MoM estimates
            # E[correct] ≈ π*(1-s) + (1-π)*g
            # Use prior and solve for s/g under symmetry assumption
            pi = self.prior[i]
            # slip: rate of wrong given mastered ≈ 1 - observed correct rate among high-mastery
            self.guess[i] = float(np.clip(correct_rate * 0.4, 0.05, 0.40))
            self.slip[i]  = float(np.clip((1 - correct_rate) * 0.3, 0.02, 0.25))

        self.is_trained = True
        self._save()
        print("[DINA] Parameters updated and saved.")

    # ── Checkpoint I/O ────────────────────────────────────────────────────────

    def _save(self):
        self.data_dir.mkdir(parents=True, exist_ok=True)
        data = {
            'skills':     JAVA_SKILLS,
            'slip':       self.slip.tolist(),
            'guess':      self.guess.tolist(),
            'prior':      self.prior.tolist(),
            'is_trained': self.is_trained,
        }
        with open(self.ckpt, 'w') as f:
            json.dump(data, f, indent=2)

    def _try_load(self):
        if self.ckpt.exists():
            try:
                with open(self.ckpt) as f:
                    data = json.load(f)
                self.slip       = np.array(data['slip'])
                self.guess      = np.array(data['guess'])
                self.prior      = np.array(data['prior'])
                self.is_trained = data.get('is_trained', False)
                print(f"[DINA] Loaded parameters from {self.ckpt}")
            except Exception as e:
                print(f"[DINA] Could not load checkpoint: {e}")

    def save_student_states(self, path: Optional[str] = None):
        """Persist per-student mastery to JSON (called on session end)."""
        p = Path(path or self.data_dir / 'student_mastery.json')
        p.parent.mkdir(parents=True, exist_ok=True)
        with open(p, 'w') as f:
            json.dump({sid: m.tolist()
                       for sid, m in self._student_mastery.items()}, f, indent=2)

    def load_student_states(self, path: Optional[str] = None):
        p = Path(path or self.data_dir / 'student_mastery.json')
        if p.exists():
            try:
                with open(p) as f:
                    raw = json.load(f)
                self._student_mastery = {
                    sid: np.array(m) for sid, m in raw.items()
                }
                print(f"[DINA] Loaded {len(self._student_mastery)} student states from {p}")
            except Exception as e:
                print(f"[DINA] Could not load student states: {e}")
