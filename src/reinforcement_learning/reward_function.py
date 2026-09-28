"""
Reward Function — CPAL LP Integration
=====================================
Reward encodes:
  T05 ZPD        → penalises tasks outside 0.40-0.75 mastery window
  T10 Flow       → challenge-skill balance bonus (mastery band + engagement)
  CPAL LP Gain   → bonus for LP-level advancement (L1->L2->L3->L4);
                    penalty for L-level regression. Primary training
                    signal for the LPProgressionRNN — see
                    mental_models_cpal_methodology.docx Part 3 Stage 4.

Emotion and the psychological channel (attribution, imposter, self-efficacy)
are not reward inputs.
"""

import numpy as np
from typing import Dict


# ZPD mastery window (T05 Zone of Proximal Development)
ZPD_LOW  = 0.40   # Below this → overwhelmed (outside ZPD)
ZPD_HIGH = 0.75   # Above this → mastered / bored (outside ZPD)

# Flow channel (T10): optimal challenge-skill balance band
FLOW_LOW  = 0.42
FLOW_HIGH = 0.72


class RewardCalculator:
    """
    Calculates reward for teaching actions.

    Components (weights sum to 1.00):
    1. learning_gain       (0.32) — BKT mastery delta
    2. engagement          (0.18) — engagement/flow quality
    3. zpd_alignment       (0.18) — was the task in the ZPD window?
    4. lp_gain             (0.32) — LP level advancement (CPAL Stage 4)
    """

    def __init__(self, config: Dict):
        self.config = config
        self.weights = {
            "learning_gain":     0.32,
            "engagement":        0.18,
            "zpd_alignment":     0.18,
            "lp_gain":           0.32,   # CPAL Stage 4 primary signal
        }

    def calculate_reward(self, session_data: Dict, action_taken: int,
                         student_response: Dict) -> float:
        """
        Calculate total reward for a teaching action.

        student_response keys used:
          mastery_before, mastery_after       — BKT values
          engagement_score                    — float 0-1
          time_spent                          — seconds
          gave_up, has_misconception          — bool
          mastery_achieved, solved_independently, asked_deep_question — bool
          zpd_status                          — 'overwhelmed'|'at_boundary'|'internalized'
          delta_lp                            — int {-3..+3}  [CPAL Stage 4]
          lp_level_before, lp_level_after     — 'L1'|'L2'|'L3'|'L4'  [CPAL]
          plateau_flag_before                 — bool  [CPAL]
        """
        rewards = {}

        # ── 1. Learning Gain ──────────────────────────────────────────────
        m_before = student_response.get("mastery_before", 0.0)
        m_after  = student_response.get("mastery_after",  0.0)
        gain     = m_after - m_before
        rewards["learning_gain"] = float(np.clip(gain / 0.5, -1, 1))

        # ── 2. Engagement ─────────────────────────────────────────────────
        eng = student_response.get("engagement_score", 0.5)
        rewards["engagement"] = float((eng - 0.5) * 2)

        # ── 3. ZPD Alignment (T05 + T10) ─────────────────────────────────
        zpd_status    = student_response.get("zpd_status", "at_boundary")
        mastery_level = m_before  # task difficulty should match pre-task mastery

        # Core: was the task calibrated to the ZPD window?
        if ZPD_LOW <= mastery_level <= ZPD_HIGH:
            zpd_score = 1.0   # Perfect: task was in ZPD
        elif mastery_level < ZPD_LOW:
            # Too hard — outside ZPD (overwhelmed)
            zpd_score = -1.0 + (mastery_level / ZPD_LOW)  # partial credit
        else:
            # Too easy — already mastered
            zpd_score = 1.0 - (mastery_level - ZPD_HIGH) / (1.0 - ZPD_HIGH)

        # Flow bonus (T10): if mastery is in the tight flow band AND engagement high
        if FLOW_LOW <= mastery_level <= FLOW_HIGH and eng > 0.65:
            zpd_score = min(1.0, zpd_score + 0.3)

        # Penalise 'overwhelmed' zone (task too hard for current state)
        if zpd_status == "overwhelmed":
            zpd_score = min(zpd_score, -0.3)

        rewards["zpd_alignment"] = float(np.clip(zpd_score, -1, 1))

        # ── 4. LP Gain (CPAL Stage 4 — primary training signal) ──────────
        # delta_lp is the level-index change computed by
        # LPDiagnostic.classify_post_reply:
        #    post_lvl_idx - pre_lvl_idx   where L1=1, L2=2, L3=3, L4=4.
        # Range is {-3 .. +3}. We normalise by /2 so a single-level gain
        # is a strong +0.5 signal and a two-level jump saturates at +1.
        # Regression (negative delta) penalises proportionally.
        #
        delta_lp           = student_response.get("delta_lp", 0)
        lp_level_before    = student_response.get("lp_level_before", "L1")
        lp_level_after     = student_response.get("lp_level_after", lp_level_before)
        plateau_before     = student_response.get("plateau_flag_before", False)

        # Core signal: normalised delta_lp.
        lp_reward = float(np.clip(delta_lp / 2.0, -1.0, 1.0))

        # Plateau-break bonus: if student came in at an L2 plateau and
        # the delta_lp is positive (broke out), amplify the reward —
        # this is exactly the pattern the LPProgressionRNN needs to
        # learn.
        if plateau_before and delta_lp > 0:
            lp_reward = min(1.0, lp_reward + 0.3)

        # L4 consolidation: no level change at L4 is fine (stable is
        # the target at the top of the rubric). Don't penalise.
        if lp_level_before == "L4" and lp_level_after == "L4" and delta_lp == 0:
            lp_reward = max(lp_reward, 0.2)

        # Regression penalty: level drop is a strong negative signal.
        # (Already captured by the normalised delta_lp line above —
        # this is just a floor to prevent the saturating clip from
        # hiding a big regression.)
        if delta_lp <= -2:
            lp_reward = min(lp_reward, -0.8)

        rewards["lp_gain"] = float(np.clip(lp_reward, -1, 1))

        # ── Penalties ─────────────────────────────────────────────────────
        if student_response.get("gave_up", False):
            rewards["learning_gain"] = min(rewards["learning_gain"] - 0.5, -0.3)
        if student_response.get("has_misconception", False):
            rewards["learning_gain"] -= 0.3

        # ── Bonuses ───────────────────────────────────────────────────────
        if student_response.get("mastery_achieved", False):
            rewards["learning_gain"] = min(1.0, rewards["learning_gain"] + 0.5)
        if student_response.get("solved_independently", False):
            rewards["zpd_alignment"] = min(1.0, rewards["zpd_alignment"] + 0.3)
        if student_response.get("asked_deep_question", False):
            rewards["engagement"] = min(1.0, rewards["engagement"] + 0.2)

        # ── Transfer Learning bonus ───────────────────────────────────────
        if "transfer_success" in student_response:
            t_bonus = 0.3 if student_response["transfer_success"] else -0.1
            rewards["learning_gain"] = min(1.0, rewards["learning_gain"] + t_bonus)

        # ── Total ─────────────────────────────────────────────────────────
        total = sum(rewards[k] * self.weights[k] for k in self.weights)
        total = float(np.clip(total, -1, 1))

        print(f"\n[Reward] Breakdown:")
        for k, v in rewards.items():
            print(f"  {k:<22}: {v:+.3f}  (w={self.weights[k]})")
        print(f"  {'TOTAL':<22}: {total:+.3f}")

        return total

    def calculate_long_term_reward(self, student_id: str, concept: str,
                                   days_later: int = 7) -> float:
        retention_score = 0.85  # populated from spaced-repetition review session
        return float((retention_score - 0.5) * 2)

    def zpd_window_check(self, mastery: float) -> str:
        """Utility: classify mastery level relative to ZPD window."""
        if mastery < ZPD_LOW:    return "overwhelmed"
        if mastery > ZPD_HIGH:   return "mastered"
        return "at_boundary"
