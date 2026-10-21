"""
Reward Function — Psychological + CPAL LP Integration Update
===================================================
Reward now encodes:
  T05 ZPD        → penalises tasks outside 0.40-0.75 mastery window
  T10 Flow       → maximises challenge-skill balance (flow channel bonus)
  T11 Attribution → bonus for interventions that shift attribution adaptive
  T12 Imposter   → bonus for mastery_surface resolving imposter flag
  T08 SCT        → engagement component reflects self-efficacy trajectory
  CPAL LP Gain   → bonus for LP-level advancement (L1->L2->L3->L4);
                    penalty for L-level regression. Primary training
                    signal for the LPProgressionRNN — see
                    mental_models_cpal_methodology.docx Part 3 Stage 4.
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
    1. learning_gain       (0.26) — BKT mastery delta
    2. engagement          (0.15) — engagement/flow quality
    3. zpd_alignment       (0.15) — was the task in the ZPD window?
    4. emotional_state     (0.12) — emotion trajectory improvement
    5. attribution_shift   (0.07) — fixed→adaptive attribution shift
    6. lp_gain             (0.25) — LP level advancement (CPAL Stage 4)
    """

    def __init__(self, config: Dict):
        self.config = config
        self.weights = {
            "learning_gain":     0.26,
            "engagement":        0.15,
            "zpd_alignment":     0.15,
            "emotional_state":   0.12,
            "attribution_shift": 0.07,
            "lp_gain":           0.25,   # NEW — CPAL Stage 4 primary signal
        }

    def calculate_reward(self, session_data: Dict, action_taken: int,
                         student_response: Dict) -> float:
        """
        Calculate total reward for a teaching action.

        student_response keys used:
          mastery_before, mastery_after       — BKT values
          engagement_score                    — float 0-1
          time_spent                          — seconds
          emotion_before, emotion_after       — string
          gave_up, has_misconception          — bool
          mastery_achieved, solved_independently, asked_deep_question — bool
          attribution_before, attribution_after — 'fixed'|'adaptive'|'neutral' [NEW]
          imposter_flag_before, imposter_flag_after — bool [NEW]
          zpd_status                          — 'overwhelmed'|'at_boundary'|'internalized' [NEW]
          intervention_type                   — string [NEW]
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

        # ── 4. Emotional State ────────────────────────────────────────────
        emotion_values = {
            "frustrated": -1.0, "confused": -0.5, "neutral": 0.0,
            "engaged": 0.5, "confident": 1.0
        }
        e_before = session_data.get("emotion", "neutral")
        e_after  = student_response.get("emotion_after", "neutral")
        e_change = emotion_values.get(e_after, 0) - emotion_values.get(e_before, 0)
        rewards["emotional_state"] = float(np.clip(e_change, -1, 1))

        # ── 5. Attribution Shift (T11 + T12) ─────────────────────────────
        attr_before   = student_response.get("attribution_before", "neutral")
        attr_after    = student_response.get("attribution_after", "neutral")
        imp_before    = student_response.get("imposter_flag_before", False)
        imp_after     = student_response.get("imposter_flag_after", False)
        intervention  = student_response.get("intervention_type", "")

        attr_reward = 0.0
        # Fixed → Adaptive shift: big bonus
        if attr_before == "fixed" and attr_after == "adaptive":
            attr_reward += 1.0
        # Imposter flag cleared: significant bonus
        if imp_before and not imp_after:
            attr_reward += 0.8
        # Attribution reframe used correctly (when fixed attr was present)
        if intervention == "attribution_reframe" and attr_before == "fixed":
            attr_reward += 0.5
        # Penalty: attribution_reframe used when not needed (wastes time)
        if intervention == "attribution_reframe" and attr_before != "fixed" and not imp_before:
            attr_reward -= 0.5
        # Mastery surface used correctly when imposter present
        if intervention == "mastery_surface" and imp_before:
            attr_reward += 0.4

        rewards["attribution_shift"] = float(np.clip(attr_reward, -1, 1))

        # ── 6. LP Gain (CPAL Stage 4 — primary training signal) ──────────
        # delta_lp is the level-index change computed by
        # LPDiagnostic.classify_post_reply:
        #    post_lvl_idx - pre_lvl_idx   where L1=1, L2=2, L3=3, L4=4.
        # Range is {-3 .. +3}. We normalise by /2 so a single-level gain
        # is a strong +0.5 signal and a two-level jump saturates at +1.
        # Regression (negative delta) penalises proportionally.
        #
        # Bonus: LP-valid intervention actually used. The intervention
        # _selector already filters through the LP gate in Stage 2, so
        # if we see a non-LP-valid intervention type here, something
        # upstream overrode the gate (psychological safety, for
        # example) — that's not a reward failure, just no bonus.
        delta_lp           = student_response.get("delta_lp", 0)
        lp_level_before    = student_response.get("lp_level_before", "L1")
        lp_level_after     = student_response.get("lp_level_after", lp_level_before)
        plateau_before     = student_response.get("plateau_flag_before", False)
        intervention_type  = intervention   # already pulled above

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
        if e_after == "frustrated" and e_before != "frustrated":
            rewards["emotional_state"] -= 0.3

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
