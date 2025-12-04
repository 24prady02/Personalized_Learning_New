"""
Integration of COKE and GIKT with existing system
Combines cognitive modeling (COKE) with knowledge tracing (GIKT)
"""

from typing import Dict, List, Optional
from .coke_cognitive_graph import COKECognitiveGraph, CognitiveState, BehavioralResponse
from .gikt_knowledge_tracing import GIKTKnowledgeTracer


class COKEGIKTIntegration:
    """
    Unified interface for COKE (cognitive modeling) and GIKT (knowledge tracing)
    
    Combines:
    - COKE: Theory of Mind, cognitive states, behavioral prediction
    - GIKT: Knowledge tracing, skill mastery, performance prediction
    """
    
    def __init__(self, config: Dict):
        """
        Args:
            config: Configuration dictionary
        """
        self.config = config
        
        # Initialize COKE
        if config.get('coke', {}).get('enabled', True):
            self.coke = COKECognitiveGraph(config.get('coke', {}))
        else:
            self.coke = None
        
        # Initialize GIKT
        if config.get('gikt', {}).get('enabled', True):
            self.gikt = GIKTKnowledgeTracer(config.get('gikt', {}))
        else:
            self.gikt = None
    
    def analyze_student_state(self, student_id: int, student_data: Dict) -> Dict:
        """
        Comprehensive student state analysis using COKE and GIKT
        
        Args:
            student_id: Student ID
            student_data: Dictionary with:
                - code: Student's code
                - error_message: Error if any
                - action_sequence: Recent actions
                - time_stuck: Time spent stuck
                - question_id: Current question (optional)
                - skill_ids: Skills involved (optional)
                
        Returns:
            Combined analysis from COKE and GIKT
        """
        result = {
            'student_id': student_id,
            'coke_analysis': {},
            'gikt_analysis': {}
        }
        
        # COKE: Cognitive state and behavioral prediction
        if self.coke:
            coke_result = self.coke.infer_theory_of_mind(student_data)
            result['coke_analysis'] = {
                'cognitive_state': coke_result['cognitive_state'],
                'predicted_behavior': coke_result['behavioral_response'],
                'confidence': coke_result['confidence'],
                'reasoning': coke_result['reasoning']
            }
        
        # GIKT: Knowledge state and performance prediction
        if self.gikt and 'question_id' in student_data:
            question_id = student_data['question_id']
            skill_ids = student_data.get('skill_ids', [])
            
            # Predict performance
            performance_prob = self.gikt.predict_performance(student_id, question_id)
            
            # Get knowledge state
            knowledge_state = self.gikt.get_student_knowledge_state(student_id)
            
            result['gikt_analysis'] = {
                'predicted_performance': performance_prob,
                'knowledge_state': knowledge_state,
                'skill_mastery': knowledge_state.get('skill_mastery', {}),
                'overall_mastery': knowledge_state.get('overall_mastery', 0.0)
            }
        
        return result
    
    def predict_next_action(self, student_id: int, student_data: Dict) -> Dict:
        """
        Predict student's next action using COKE behavioral prediction
        
        Args:
            student_id: Student ID
            student_data: Current student state
            
        Returns:
            Predicted next action and reasoning
        """
        if not self.coke:
            return {'predicted_action': 'unknown', 'confidence': 0.0}
        
        # Get cognitive state
        cognitive_state = self.coke.predict_cognitive_state(student_data)
        
        # Predict behavioral response
        context = student_data.get('context', 'general')
        behavioral_response = self.coke.predict_behavioral_response(cognitive_state, context)
        
        return {
            'predicted_action': behavioral_response.value,
            'cognitive_state': cognitive_state.value,
            'confidence': 0.7,  # Can be enhanced with actual chain confidence
            'reasoning': f"Student is {cognitive_state.value}, likely to {behavioral_response.value}"
        }
    
    def get_cognitive_trajectory(self, student_id: int, 
                                 session_history: List[Dict]) -> List[Dict]:
        """
        Get cognitive state trajectory over a session
        
        Args:
            student_id: Student ID
            session_history: List of student states over time
            
        Returns:
            List of cognitive states and transitions
        """
        if not self.coke:
            return []
        
        trajectory = []
        
        for i, state in enumerate(session_history):
            cognitive_state = self.coke.predict_cognitive_state(state)
            
            trajectory.append({
                'timestamp': i,
                'cognitive_state': cognitive_state.value,
                'context': state.get('context', 'general'),
                'has_error': bool(state.get('error_message')),
                'time_stuck': state.get('time_stuck', 0)
            })
            
            # Add transition if not first state
            if i > 0:
                prev_state = CognitiveState[trajectory[i-1]['cognitive_state'].upper()]
                transition_prob = self.coke.get_state_transition_probability(
                    prev_state, cognitive_state
                )
                trajectory[i]['transition_probability'] = transition_prob
        
        return trajectory
    
    def update_knowledge_tracing(self, student_id: int, question_id: int,
                                skill_ids: List[int], correct: bool):
        """
        Update GIKT knowledge tracing with new exercise result
        
        Args:
            student_id: Student ID
            question_id: Question ID
            skill_ids: List of skill IDs involved
            correct: Whether answer was correct
        """
        if self.gikt:
            # Add question-skill mapping if not exists
            for skill_id in skill_ids:
                if skill_id not in self.gikt.question_skill_map.get(question_id, []):
                    self.gikt.add_question_skill_mapping(question_id, skill_ids)
            
            # Record exercise
            self.gikt.record_exercise(student_id, question_id, skill_ids, correct)
    
    def get_unified_student_model(self, student_id: int, 
                                 current_state: Dict) -> Dict:
        """
        Get unified model combining COKE (cognitive) and GIKT (knowledge)
        
        Args:
            student_id: Student ID
            current_state: Current student state
            
        Returns:
            Unified student model
        """
        # Get COKE cognitive analysis
        coke_analysis = {}
        if self.coke:
            coke_result = self.coke.infer_theory_of_mind(current_state)
            coke_analysis = {
                'cognitive_state': coke_result['cognitive_state'],
                'mental_model': coke_result['reasoning'],
                'predicted_behavior': coke_result['behavioral_response']
            }
        
        # Get GIKT knowledge state
        gikt_analysis = {}
        if self.gikt:
            knowledge_state = self.gikt.get_student_knowledge_state(student_id)
            gikt_analysis = {
                'skill_mastery': knowledge_state.get('skill_mastery', {}),
                'overall_mastery': knowledge_state.get('overall_mastery', 0.0),
                'total_exercises': knowledge_state.get('total_exercises', 0)
            }
        
        return {
            'student_id': student_id,
            'cognitive_model': coke_analysis,
            'knowledge_model': gikt_analysis,
            'unified_insight': self._combine_insights(coke_analysis, gikt_analysis)
        }
    
    def _combine_insights(self, coke_analysis: Dict, gikt_analysis: Dict) -> str:
        """Combine COKE and GIKT insights into unified understanding"""
        insights = []
        
        if coke_analysis:
            cognitive_state = coke_analysis.get('cognitive_state', 'unknown')
            insights.append(f"Cognitive state: {cognitive_state}")
        
        if gikt_analysis:
            overall_mastery = gikt_analysis.get('overall_mastery', 0.0)
            insights.append(f"Knowledge mastery: {overall_mastery:.2%}")
        
        if coke_analysis and gikt_analysis:
            cognitive_state = coke_analysis.get('cognitive_state', '')
            mastery = gikt_analysis.get('overall_mastery', 0.0)
            
            if cognitive_state == 'confused' and mastery < 0.5:
                insights.append("Student is struggling - needs scaffolding")
            elif cognitive_state == 'understanding' and mastery > 0.7:
                insights.append("Student is progressing well")
        
        return "; ".join(insights) if insights else "No insights available"












