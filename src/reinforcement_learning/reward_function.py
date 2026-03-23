"""
Reward Function for Teaching RL Agent
Calculates rewards based on student learning outcomes
"""

import numpy as np
from typing import Dict


class RewardCalculator:
    """
    Calculates reward for teaching actions
    
    Good reward = Student learns effectively
    Bad reward = Student doesn't learn or gets frustrated
    
    Reward Components:
    1. Learning gain (did mastery improve?)
    2. Engagement (was student engaged?)
    3. Efficiency (time to success)
    4. Retention (remembered later?)
    5. Transfer (applied to new problems?)
    """
    
    def __init__(self, config: Dict):
        self.config = config
        
        # Reward component weights
        self.weights = {
            'learning_gain': 0.40,      # Most important!
            'engagement': 0.20,
            'efficiency': 0.15,
            'emotional_state': 0.15,
            'transfer_learning': 0.10
        }
    
    def calculate_reward(self, session_data: Dict,
                        action_taken: int,
                        student_response: Dict) -> float:
        """
        Calculate total reward for a teaching action
        
        Args:
            session_data: Original session info
            action_taken: Which intervention was used
            student_response: How student responded
            
        Returns:
            Reward value [-1, 1]
        """
        
        rewards = {}
        
        # === REWARD 1: Learning Gain ===
        # Did student's mastery improve?
        mastery_before = student_response.get('mastery_before', 0.0)
        mastery_after = student_response.get('mastery_after', 0.0)
        learning_gain = mastery_after - mastery_before
        
        # Normalize to [-1, 1]
        rewards['learning_gain'] = np.clip(learning_gain / 0.5, -1, 1)
        
        # === REWARD 2: Engagement ===
        # Was student engaged or frustrated/bored?
        engagement_score = student_response.get('engagement_score', 0.5)
        rewards['engagement'] = (engagement_score - 0.5) * 2  # Map [0,1] to [-1,1]
        
        # === REWARD 3: Efficiency ===
        # Did they learn quickly or take very long?
        time_spent = student_response.get('time_spent', 300)
        expected_time = 300  # 5 minutes
        
        if time_spent < expected_time * 0.5:
            # Too fast - might not have learned deeply
            rewards['efficiency'] = 0.5
        elif time_spent < expected_time * 1.5:
            # Good time
            rewards['efficiency'] = 1.0
        else:
            # Took too long - intervention might not have been effective
            rewards['efficiency'] = max(-1, 1 - (time_spent / expected_time - 1))
        
        # === REWARD 4: Emotional State ===
        # Did intervention improve emotional state?
        emotion_before = session_data.get('emotion', 'neutral')
        emotion_after = student_response.get('emotion_after', 'neutral')
        
        emotion_values = {
            'frustrated': -1.0,
            'confused': -0.5,
            'neutral': 0.0,
            'engaged': 0.5,
            'confident': 1.0
        }
        
        emotion_change = emotion_values.get(emotion_after, 0) - \
                        emotion_values.get(emotion_before, 0)
        rewards['emotional_state'] = np.clip(emotion_change, -1, 1)
        
        # === REWARD 5: Transfer Learning ===
        # Can student apply to new problems?
        if 'transfer_success' in student_response:
            rewards['transfer_learning'] = 1.0 if student_response['transfer_success'] else -0.5
        else:
            rewards['transfer_learning'] = 0.0  # Not tested yet
        
        # === PENALTIES ===
        
        # Penalty if student gave up
        if student_response.get('gave_up', False):
            rewards['learning_gain'] -= 0.5
        
        # Penalty if student became more frustrated
        if emotion_after == 'frustrated' and emotion_before != 'frustrated':
            rewards['emotional_state'] -= 0.3
        
        # Penalty if incorrect understanding
        if student_response.get('has_misconception', False):
            rewards['learning_gain'] -= 0.3
        
        # === BONUSES ===
        
        # Bonus for mastery achievement
        if student_response.get('mastery_achieved', False):
            rewards['learning_gain'] += 0.5
        
        # Bonus for independent problem solving
        if student_response.get('solved_independently', False):
            rewards['transfer_learning'] += 0.3
        
        # Bonus for asking good questions (shows deep thinking)
        if student_response.get('asked_deep_question', False):
            rewards['engagement'] += 0.2
        
        # === CALCULATE TOTAL REWARD ===
        total_reward = sum(
            rewards[component] * self.weights[component]
            for component in self.weights.keys()
        )
        
        # Clip to valid range
        total_reward = np.clip(total_reward, -1, 1)
        
        print(f"\n💰 REWARD BREAKDOWN:")
        print(f"   Learning gain: {rewards['learning_gain']:.3f} (weight: {self.weights['learning_gain']})")
        print(f"   Engagement: {rewards['engagement']:.3f} (weight: {self.weights['engagement']})")
        print(f"   Efficiency: {rewards['efficiency']:.3f} (weight: {self.weights['efficiency']})")
        print(f"   Emotional: {rewards['emotional_state']:.3f} (weight: {self.weights['emotional_state']})")
        print(f"   Transfer: {rewards['transfer_learning']:.3f} (weight: {self.weights['transfer_learning']})")
        print(f"   ──────────────────────────")
        print(f"   TOTAL REWARD: {total_reward:.3f}")
        
        return total_reward
    
    def calculate_long_term_reward(self, student_id: str,
                                   concept: str,
                                   days_later: int = 7) -> float:
        """
        Calculate long-term reward based on retention
        
        Called after spaced repetition review
        Checks if student still remembers after days
        """
        
        # This would query student's performance on review session
        retention_score = 0.85  # Placeholder
        
        # High retention = good teaching!
        reward = (retention_score - 0.5) * 2
        
        return reward




















