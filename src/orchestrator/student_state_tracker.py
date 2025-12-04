"""
Student State Tracker
Tracks and updates student cognitive state, knowledge state, and learning progress
from actual conversation and code interactions
"""

from typing import Dict, List, Optional
from datetime import datetime
import json
from pathlib import Path


class StudentStateTracker:
    """
    Tracks student state across sessions:
    - Cognitive state (from COKE analysis of conversation)
    - Knowledge state (from code correctness and performance)
    - Learning progress (concept mastery over time)
    - Conversation history
    """
    
    def __init__(self, config: Dict):
        """
        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.student_states = {}  # student_id -> state dict
        self.state_file = Path(config.get('student_state', {}).get('state_file', 'data/student_states.json'))
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Load existing states
        self._load_states()
    
    def _load_states(self):
        """Load student states from file"""
        if self.state_file.exists():
            try:
                with open(self.state_file, 'r') as f:
                    self.student_states = json.load(f)
            except Exception as e:
                print(f"[WARN] Failed to load student states: {e}")
                self.student_states = {}
    
    def _save_states(self):
        """Save student states to file"""
        try:
            with open(self.state_file, 'w') as f:
                json.dump(self.student_states, f, indent=2, default=str)
        except Exception as e:
            print(f"[WARN] Failed to save student states: {e}")
    
    def get_student_state(self, student_id: str) -> Dict:
        """
        Get current student state
        
        Args:
            student_id: Student identifier
            
        Returns:
            Dictionary with student state
        """
        if student_id not in self.student_states:
            self.student_states[student_id] = self._initialize_student_state(student_id)
        
        return self.student_states[student_id]
    
    def _initialize_student_state(self, student_id: str) -> Dict:
        """Initialize new student state"""
        return {
            'student_id': student_id,
            'created_at': datetime.now().isoformat(),
            'last_updated': datetime.now().isoformat(),
            'cognitive_state': {
                'current_state': 'engaged',
                'confidence': 0.5,
                'state_history': []
            },
            'knowledge_state': {
                'concept_mastery': {},
                'mastery_history': [],
                'last_updated': None
            },
            'conversation_history': [],
            'session_count': 0,
            'total_interactions': 0
        }
    
    def update_from_session(
        self,
        student_id: str,
        session_data: Dict,
        cognitive_state: str,
        concepts_identified: List[str],
        code_correctness: float,
        response_quality: float
    ):
        """
        Update student state from a session
        
        Args:
            student_id: Student identifier
            session_data: Session data (code, question, conversation, etc.)
            cognitive_state: Inferred cognitive state (from COKE)
            concepts_identified: Concepts extracted from code/conversation
            code_correctness: Code correctness score (0.0-1.0)
            response_quality: Response quality score (0.0-1.0)
        """
        state = self.get_student_state(student_id)
        
        # Update cognitive state
        state['cognitive_state']['current_state'] = cognitive_state
        state['cognitive_state']['state_history'].append({
            'state': cognitive_state,
            'timestamp': datetime.now().isoformat(),
            'context': {
                'has_error': bool(session_data.get('error_message')),
                'time_stuck': session_data.get('time_stuck', 0),
                'question': session_data.get('question', '')[:100]
            }
        })
        # Keep only last 50 states
        if len(state['cognitive_state']['state_history']) > 50:
            state['cognitive_state']['state_history'] = state['cognitive_state']['state_history'][-50:]
        
        # Update knowledge state based on code correctness
        for concept in concepts_identified:
            if concept not in state['knowledge_state']['concept_mastery']:
                state['knowledge_state']['concept_mastery'][concept] = 0.5  # Start with moderate
        
            # Update mastery: if code is correct, increase; if incorrect, decrease slightly
            current_mastery = state['knowledge_state']['concept_mastery'][concept]
            if code_correctness > 0.8:
                # Strong positive signal
                new_mastery = min(1.0, current_mastery + 0.1)
            elif code_correctness > 0.5:
                # Moderate positive signal
                new_mastery = min(1.0, current_mastery + 0.05)
            elif code_correctness < 0.3:
                # Strong negative signal (but don't penalize too much)
                new_mastery = max(0.0, current_mastery - 0.02)
            else:
                # Neutral - slight increase from practice
                new_mastery = min(1.0, current_mastery + 0.01)
            
            state['knowledge_state']['concept_mastery'][concept] = new_mastery
        
        # Record mastery history
        overall_mastery = sum(state['knowledge_state']['concept_mastery'].values()) / max(len(state['knowledge_state']['concept_mastery']), 1)
        state['knowledge_state']['mastery_history'].append({
            'timestamp': datetime.now().isoformat(),
            'overall_mastery': overall_mastery,
            'concepts_tested': concepts_identified
        })
        # Keep only last 100 history entries
        if len(state['knowledge_state']['mastery_history']) > 100:
            state['knowledge_state']['mastery_history'] = state['knowledge_state']['mastery_history'][-100:]
        
        state['knowledge_state']['last_updated'] = datetime.now().isoformat()
        
        # Update conversation history
        conversation_entry = {
            'timestamp': datetime.now().isoformat(),
            'question': session_data.get('question', ''),
            'code': session_data.get('code', '')[:200],  # Truncate
            'error': session_data.get('error_message', ''),
            'cognitive_state': cognitive_state,
            'concepts': concepts_identified,
            'correctness': code_correctness
        }
        state['conversation_history'].append(conversation_entry)
        # Keep only last 100 conversations
        if len(state['conversation_history']) > 100:
            state['conversation_history'] = state['conversation_history'][-100:]
        
        # Update session stats
        state['session_count'] += 1
        state['total_interactions'] += 1
        state['last_updated'] = datetime.now().isoformat()
        
        # Save to file
        self._save_states()
    
    def get_cognitive_state(self, student_id: str) -> Dict:
        """Get current cognitive state"""
        state = self.get_student_state(student_id)
        return state['cognitive_state']
    
    def get_knowledge_state(self, student_id: str) -> Dict:
        """Get current knowledge state"""
        state = self.get_student_state(student_id)
        return state['knowledge_state']
    
    def get_conversation_history(self, student_id: str, limit: int = 10) -> List[Dict]:
        """Get recent conversation history"""
        state = self.get_student_state(student_id)
        return state['conversation_history'][-limit:]
    
    def get_learning_trajectory(self, student_id: str) -> Dict:
        """Get learning trajectory over time"""
        state = self.get_student_state(student_id)
        mastery_history = state['knowledge_state']['mastery_history']
        
        if len(mastery_history) < 2:
            return {'trend': 'insufficient_data', 'slope': 0.0}
        
        # Calculate trend
        recent = mastery_history[-5:] if len(mastery_history) >= 5 else mastery_history
        older = mastery_history[:5] if len(mastery_history) >= 10 else mastery_history[:len(mastery_history)//2]
        
        recent_avg = sum(h['overall_mastery'] for h in recent) / len(recent)
        older_avg = sum(h['overall_mastery'] for h in older) / len(older) if older else recent_avg
        
        slope = recent_avg - older_avg
        
        if slope > 0.1:
            trend = 'improving'
        elif slope < -0.1:
            trend = 'declining'
        else:
            trend = 'stable'
        
        return {
            'trend': trend,
            'slope': slope,
            'current_mastery': recent_avg,
            'previous_mastery': older_avg,
            'data_points': len(mastery_history)
        }





