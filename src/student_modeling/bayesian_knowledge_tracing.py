"""
Bayesian Knowledge Tracing (BKT)
Tracks student knowledge state over time with probabilistic updates
"""

import numpy as np
from typing import Dict, List, Tuple
import json
from pathlib import Path


class BayesianKnowledgeTracer:
    """
    Bayesian Knowledge Tracing for maintaining student knowledge state
    
    BKT Parameters:
    - P(L0): Initial probability student knows the skill
    - P(T): Probability of learning (transition from not-learned to learned)
    - P(S): Probability of slip (knows but gets wrong)
    - P(G): Probability of guess (doesn't know but gets right)
    """
    
    def __init__(self):
        # Default BKT parameters (can be learned from data)
        self.default_params = {
            'p_l0': 0.3,   # Initial knowledge
            'p_t': 0.2,    # Learning rate
            'p_s': 0.1,    # Slip probability
            'p_g': 0.25    # Guess probability
        }
        
        # Student knowledge states: {student_id: {skill: p_learned}}
        self.student_states = {}
        
        # Skill-specific BKT parameters
        self.skill_params = {}
        
    def initialize_student(self, student_id: str, skills: List[str] = None):
        """Initialize a new student with default knowledge states"""
        
        if student_id not in self.student_states:
            self.student_states[student_id] = {}
        
        if skills:
            for skill in skills:
                if skill not in self.student_states[student_id]:
                    # Initialize with P(L0)
                    p_l0 = self.skill_params.get(skill, {}).get('p_l0', self.default_params['p_l0'])
                    self.student_states[student_id][skill] = {
                        'p_learned': p_l0,
                        'attempts': 0,
                        'correct': 0,
                        'history': []
                    }
    
    def update_knowledge(
        self,
        student_id: str,
        skill: str,
        is_correct: bool,
        evidence_strength: float = 1.0
    ) -> Dict:
        """
        Update student knowledge state based on performance
        
        Args:
            student_id: Student identifier
            skill: Skill being assessed
            is_correct: Whether student answered correctly
            evidence_strength: How much to weight this evidence (0-1)
        
        Returns:
            Updated knowledge state with metrics
        """
        
        # Initialize if needed
        self.initialize_student(student_id, [skill])
        
        # Get current probability of knowing the skill
        state = self.student_states[student_id][skill]
        p_l_prev = state['p_learned']
        
        # Get BKT parameters for this skill
        params = self.skill_params.get(skill, self.default_params)
        p_t = params.get('p_t', self.default_params['p_t'])
        p_s = params.get('p_s', self.default_params['p_s'])
        p_g = params.get('p_g', self.default_params['p_g'])
        
        # Calculate P(correct | learned) using BKT
        if is_correct:
            # P(L|correct) = P(correct|L) * P(L) / P(correct)
            p_correct_given_learned = 1 - p_s
            p_correct_given_not_learned = p_g
            
            p_correct = (p_correct_given_learned * p_l_prev + 
                        p_correct_given_not_learned * (1 - p_l_prev))
            
            p_l_given_correct = (p_correct_given_learned * p_l_prev) / p_correct
        else:
            # P(L|incorrect) = P(incorrect|L) * P(L) / P(incorrect)
            p_incorrect_given_learned = p_s
            p_incorrect_given_not_learned = 1 - p_g
            
            p_incorrect = (p_incorrect_given_learned * p_l_prev + 
                          p_incorrect_given_not_learned * (1 - p_l_prev))
            
            p_l_given_correct = (p_incorrect_given_learned * p_l_prev) / p_incorrect
        
        # Apply evidence strength weighting
        p_l_after_evidence = (evidence_strength * p_l_given_correct + 
                             (1 - evidence_strength) * p_l_prev)
        
        # Apply learning transition
        p_l_new = p_l_after_evidence + (1 - p_l_after_evidence) * p_t
        
        # Update state
        state['p_learned'] = p_l_new
        state['attempts'] += 1
        if is_correct:
            state['correct'] += 1
        
        state['history'].append({
            'is_correct': is_correct,
            'p_learned_before': p_l_prev,
            'p_learned_after': p_l_new,
            'evidence_strength': evidence_strength
        })
        
        return {
            'skill': skill,
            'p_learned_before': p_l_prev,
            'p_learned_after': p_l_new,
            'change': p_l_new - p_l_prev,
            'attempts': state['attempts'],
            'accuracy': state['correct'] / state['attempts']
        }
    
    def infer_performance(
        self,
        student_id: str,
        interaction_data: Dict
    ) -> Tuple[str, bool, float]:
        """
        Infer skill, performance, and evidence strength from student interaction
        
        Args:
            student_id: Student identifier
            interaction_data: Dict with question, response, analysis
        
        Returns:
            (skill, is_correct, evidence_strength)
        """
        
        # Extract skill from focus or concept
        skill = interaction_data.get('focus', 'general')
        
        # Infer correctness from emotion and mastery
        emotion = interaction_data.get('emotion', 'neutral')
        mastery = interaction_data.get('mastery', 0.5)
        
        # If confused + low mastery = incorrect understanding
        # If confident + high mastery = correct understanding
        
        if emotion in ['confused', 'frustrated']:
            is_correct = False
            evidence_strength = 0.7  # Strong evidence of not knowing
        elif emotion in ['confident', 'engaged']:
            is_correct = True
            evidence_strength = 0.7  # Strong evidence of knowing
        else:
            # Use mastery as proxy
            is_correct = mastery > 0.5
            evidence_strength = 0.5  # Moderate evidence
        
        # Check if question shows understanding progression
        message = interaction_data.get('message', '').lower()
        if 'i get that' in message or 'i understand' in message:
            # Partial understanding
            is_correct = True
            evidence_strength = 0.4  # Weaker evidence (partial)
        elif 'i don\'t understand' in message:
            is_correct = False
            evidence_strength = 0.8  # Strong evidence of confusion
        
        return skill, is_correct, evidence_strength
    
    def get_student_knowledge_state(self, student_id: str) -> Dict:
        """Get complete knowledge state for a student"""
        
        if student_id not in self.student_states:
            return {}
        
        state = self.student_states[student_id]
        
        # Calculate summary statistics
        summary = {
            'skills': {},
            'overall_mastery': 0.0,
            'total_attempts': 0,
            'skills_learned': 0,
            'skills_struggling': []
        }
        
        for skill, skill_state in state.items():
            p_learned = skill_state['p_learned']
            
            summary['skills'][skill] = {
                'mastery': p_learned,
                'attempts': skill_state['attempts'],
                'accuracy': skill_state['correct'] / max(skill_state['attempts'], 1),
                'status': self._get_skill_status(p_learned)
            }
            
            summary['overall_mastery'] += p_learned
            summary['total_attempts'] += skill_state['attempts']
            
            if p_learned >= 0.7:
                summary['skills_learned'] += 1
            elif p_learned < 0.4:
                summary['skills_struggling'].append(skill)
        
        if state:
            summary['overall_mastery'] /= len(state)
        
        return summary
    
    def _get_skill_status(self, p_learned: float) -> str:
        """Classify skill status based on probability"""
        if p_learned >= 0.7:
            return 'mastered'
        elif p_learned >= 0.5:
            return 'developing'
        elif p_learned >= 0.3:
            return 'emerging'
        else:
            return 'struggling'
    
    def get_recommended_skills(self, student_id: str, n: int = 3) -> List[str]:
        """Get recommended skills to practice based on zone of proximal development"""
        
        if student_id not in self.student_states:
            return []
        
        state = self.student_states[student_id]
        
        # Find skills in ZPD (0.3 - 0.7 range)
        zpd_skills = []
        for skill, skill_state in state.items():
            p_learned = skill_state['p_learned']
            if 0.3 <= p_learned <= 0.7:
                # In zone of proximal development
                zpd_skills.append((skill, p_learned))
        
        # Sort by closest to 0.5 (optimal challenge)
        zpd_skills.sort(key=lambda x: abs(x[1] - 0.5))
        
        return [skill for skill, _ in zpd_skills[:n]]
    
    def save_state(self, filepath: str):
        """Save student states to file"""
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, 'w') as f:
            json.dump({
                'student_states': self.student_states,
                'skill_params': self.skill_params
            }, f, indent=2)
    
    def load_state(self, filepath: str):
        """Load student states from file"""
        if Path(filepath).exists():
            with open(filepath, 'r') as f:
                data = json.load(f)
                self.student_states = data.get('student_states', {})
                self.skill_params = data.get('skill_params', {})


class StudentStateManager:
    """
    Manages complete student state including:
    - BKT knowledge tracking
    - Personality profile (Personality Profiler)
    - Learning history
    - Interaction patterns
    """
    
    def __init__(self, state_file: str = 'data/student_states.json'):
        self.state_file = state_file
        self.bkt = BayesianKnowledgeTracer()
        self.student_profiles = {}
        
        # Try to load existing state
        self.load_state()
    
    def update_from_interaction(
        self,
        student_id: str,
        interaction: Dict
    ) -> Dict:
        """
        Update student state from a complete interaction
        
        Args:
            student_id: Student identifier
            interaction: Dict with all interaction data
        
        Returns:
            Updated state summary
        """
        
        # Initialize profile if new student
        if student_id not in self.student_profiles:
            self.student_profiles[student_id] = {
                'personality': {},
                'interaction_count': 0,
                'session_history': []
            }
        
        profile = self.student_profiles[student_id]
        
        # Update personality (from Personality Profiler)
        if 'personality' in interaction:
            # Running average for personality traits (only numeric)
            for trait, value in interaction['personality'].items():
                if trait in profile['personality']:
                    # For numeric traits, use weighted average
                    # For categorical traits, keep most recent
                    if isinstance(value, (int, float)) and isinstance(profile['personality'][trait], (int, float)):
                        old_val = profile['personality'][trait]
                        profile['personality'][trait] = 0.7 * value + 0.3 * old_val
                    else:
                        # Categorical - keep most recent
                        profile['personality'][trait] = value
                else:
                    profile['personality'][trait] = value
        
        # Update BKT knowledge state
        skill, is_correct, evidence = self.bkt.infer_performance(student_id, interaction)
        bkt_update = self.bkt.update_knowledge(student_id, skill, is_correct, evidence)
        
        # Add to session history
        profile['interaction_count'] += 1
        profile['session_history'].append({
            'interaction': profile['interaction_count'],
            'skill': skill,
            'bkt_update': bkt_update,
            'emotion': interaction.get('emotion'),
            'intervention': interaction.get('intervention')
        })
        
        # Get complete knowledge state
        knowledge_state = self.bkt.get_student_knowledge_state(student_id)
        
        return {
            'student_id': student_id,
            'interaction_count': profile['interaction_count'],
            'personality': profile['personality'],
            'knowledge_state': knowledge_state,
            'bkt_update': bkt_update,
            'recommended_skills': self.bkt.get_recommended_skills(student_id)
        }
    
    def get_student_state(self, student_id: str) -> Dict:
        """Get complete current state for a student"""
        
        if student_id not in self.student_profiles:
            return {
                'student_id': student_id,
                'is_new': True,
                'knowledge_state': {},
                'personality': {}
            }
        
        profile = self.student_profiles[student_id]
        knowledge_state = self.bkt.get_student_knowledge_state(student_id)
        
        return {
            'student_id': student_id,
            'is_new': False,
            'interaction_count': profile['interaction_count'],
            'personality': profile['personality'],
            'knowledge_state': knowledge_state,
            'recommended_skills': self.bkt.get_recommended_skills(student_id),
            'recent_history': profile['session_history'][-5:]  # Last 5 interactions
        }
    
    def save_state(self):
        """Save all student states"""
        self.bkt.save_state(self.state_file)
        
        # Save profiles
        profile_file = self.state_file.replace('.json', '_profiles.json')
        Path(profile_file).parent.mkdir(parents=True, exist_ok=True)
        with open(profile_file, 'w') as f:
            json.dump(self.student_profiles, f, indent=2)
    
    def load_state(self):
        """Load all student states"""
        if Path(self.state_file).exists():
            self.bkt.load_state(self.state_file)
        
        profile_file = self.state_file.replace('.json', '_profiles.json')
        if Path(profile_file).exists():
            with open(profile_file, 'r') as f:
                self.student_profiles = json.load(f)

