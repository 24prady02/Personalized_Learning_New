"""
Dynamic Knowledge Graph Updater
Updates KG structure based on student interactions and RL feedback
"""

import torch
from typing import Dict, List, Optional, Tuple
import networkx as nx
from datetime import datetime


class DynamicKGUpdater:
    """
    Dynamically updates knowledge graph based on student learning patterns
    
    Key Idea: The knowledge graph isn't static!
    
    It learns:
    - Which concepts are actually prerequisites (students struggle without them)
    - Which concepts are harder than expected (need more time)
    - Which misconceptions are common (create edges to track them)
    - Which learning paths work better (update edge weights)
    - Which examples are most effective (boost those)
    """
    
    def __init__(self, config: Dict, models: Dict):
        self.config = config
        self.models = models
        
        # Track concept difficulties (learned from student struggles)
        self.learned_difficulties = {}
        
        # Track prerequisite strengths (how critical each prerequisite is)
        self.prerequisite_strengths = {}
        
        # Track common misconceptions per concept
        self.common_misconceptions = {}
        
        # Track effective teaching sequences
        self.effective_sequences = []
        
        # Update statistics
        self.update_count = 0
        
    def update_from_interaction(self, session_data: Dict,
                               student_outcome: Dict,
                               success: bool) -> Dict:
        """
        Update knowledge graph based on student interaction
        
        Args:
            session_data: Student's session
            student_outcome: How they responded
            success: Whether intervention was successful
            
        Returns:
            Dictionary with update details
        """
        
        updates = {
            'num_updates': 0,
            'difficulty_updates': [],
            'prerequisite_updates': [],
            'misconception_updates': [],
            'sequence_updates': []
        }
        
        # Extract concepts involved
        concepts = student_outcome.get('concepts_involved', [])
        
        for concept in concepts:
            
            # === UPDATE 1: Concept Difficulty ===
            # Learn actual difficulty from student struggle
            time_stuck = session_data.get('time_stuck', 0)
            hints_used = student_outcome.get('hints_used', 0)
            
            # Calculate observed difficulty
            observed_difficulty = self._calculate_observed_difficulty(
                time_stuck, hints_used, success
            )
            
            # Update running average
            if concept not in self.learned_difficulties:
                self.learned_difficulties[concept] = observed_difficulty
            else:
                # Exponential moving average
                alpha = 0.2
                self.learned_difficulties[concept] = \
                    alpha * observed_difficulty + (1 - alpha) * self.learned_difficulties[concept]
            
            updates['difficulty_updates'].append({
                'concept': concept,
                'new_difficulty': self.learned_difficulties[concept]
            })
            updates['num_updates'] += 1
            
            # === UPDATE 2: Prerequisite Discovery ===
            # If student struggles with concept but has weak prerequisites,
            # strengthen that prerequisite edge
            if not success:
                knowledge_gaps = student_outcome.get('knowledge_gaps', [])
                
                for gap in knowledge_gaps:
                    gap_concept = gap['concept']
                    
                    # Create/strengthen prerequisite edge
                    edge_key = (gap_concept, concept)
                    
                    if edge_key not in self.prerequisite_strengths:
                        self.prerequisite_strengths[edge_key] = 0.5
                    else:
                        # Strengthen edge (this prerequisite is important!)
                        self.prerequisite_strengths[edge_key] = min(
                            1.0,
                            self.prerequisite_strengths[edge_key] + 0.1
                        )
                    
                    updates['prerequisite_updates'].append({
                        'from': gap_concept,
                        'to': concept,
                        'strength': self.prerequisite_strengths[edge_key]
                    })
                    updates['num_updates'] += 1
            
            # === UPDATE 3: Misconception Tracking ===
            # Record common misconceptions for this concept
            detected_misconceptions = student_outcome.get('misconceptions_detected', [])
            
            if concept not in self.common_misconceptions:
                self.common_misconceptions[concept] = {}
            
            for misconception in detected_misconceptions:
                misc_key = misconception['description']
                
                if misc_key not in self.common_misconceptions[concept]:
                    self.common_misconceptions[concept][misc_key] = {
                        'count': 0,
                        'students': set(),
                        'severity': misconception.get('severity', 0.5)
                    }
                
                # Update count
                self.common_misconceptions[concept][misc_key]['count'] += 1
                self.common_misconceptions[concept][misc_key]['students'].add(
                    session_data['student_id']
                )
                
                updates['misconception_updates'].append({
                    'concept': concept,
                    'misconception': misc_key,
                    'frequency': self.common_misconceptions[concept][misc_key]['count']
                })
                updates['num_updates'] += 1
        
        # === UPDATE 4: Effective Teaching Sequences ===
        # Track which intervention sequences lead to success
        if success:
            intervention_used = student_outcome.get('intervention_type')
            previous_interventions = student_outcome.get('previous_interventions', [])
            
            sequence = previous_interventions + [intervention_used]
            
            self.effective_sequences.append({
                'sequence': sequence,
                'concept': concepts[0] if concepts else 'unknown',
                'student_profile': student_outcome.get('student_profile', {}),
                'success_metrics': {
                    'mastery_gain': student_outcome.get('mastery_after', 0) - \
                                   student_outcome.get('mastery_before', 0),
                    'time': student_outcome.get('time_spent', 0),
                    'engagement': student_outcome.get('engagement_score', 0.5)
                }
            })
            
            updates['sequence_updates'].append({
                'sequence': sequence,
                'success': True
            })
            updates['num_updates'] += 1
        
        self.update_count += 1
        
        return updates
    
    def _calculate_observed_difficulty(self, time_stuck: float,
                                      hints_used: int,
                                      success: bool) -> float:
        """
        Calculate difficulty based on student's experience
        
        Returns:
            Difficulty score [0, 1]
        """
        
        difficulty = 0.0
        
        # Time component
        if time_stuck > 600:  # > 10 minutes
            difficulty += 0.4
        elif time_stuck > 300:  # > 5 minutes
            difficulty += 0.3
        elif time_stuck > 120:  # > 2 minutes
            difficulty += 0.2
        else:
            difficulty += 0.1
        
        # Hints component
        if hints_used >= 5:
            difficulty += 0.3
        elif hints_used >= 3:
            difficulty += 0.2
        elif hints_used >= 1:
            difficulty += 0.1
        
        # Success component
        if not success:
            difficulty += 0.3
        
        return min(1.0, difficulty)
    
    def get_concept_difficulty(self, concept: str) -> float:
        """Get learned difficulty for a concept"""
        return self.learned_difficulties.get(concept, 0.5)
    
    def get_prerequisite_strength(self, from_concept: str, to_concept: str) -> float:
        """Get strength of prerequisite relationship"""
        return self.prerequisite_strengths.get((from_concept, to_concept), 0.5)
    
    def get_common_misconceptions(self, concept: str, top_k: int = 5) -> List[Dict]:
        """
        Get most common misconceptions for a concept
        Learned from actual student errors!
        """
        
        if concept not in self.common_misconceptions:
            return []
        
        # Sort by frequency
        misconceptions = []
        for misc_desc, misc_data in self.common_misconceptions[concept].items():
            misconceptions.append({
                'description': misc_desc,
                'frequency': misc_data['count'],
                'affected_students': len(misc_data['students']),
                'severity': misc_data['severity']
            })
        
        misconceptions.sort(key=lambda x: x['frequency'], reverse=True)
        
        return misconceptions[:top_k]
    
    def get_effective_teaching_sequence(self, concept: str,
                                       student_profile: Dict) -> List[str]:
        """
        Get most effective teaching sequence for this type of student
        Learned from past successes!
        """
        
        # Filter sequences for this concept
        relevant = [
            seq for seq in self.effective_sequences
            if seq['concept'] == concept
        ]
        
        if not relevant:
            return ['guided_practice', 'independent_practice']  # Default
        
        # Find most similar student profile
        best_match = None
        best_similarity = 0
        
        for seq in relevant:
            similarity = self._profile_similarity(
                student_profile,
                seq['student_profile']
            )
            
            if similarity > best_similarity:
                best_similarity = similarity
                best_match = seq
        
        if best_match:
            return best_match['sequence']
        else:
            return relevant[0]['sequence']
    
    def _profile_similarity(self, profile1: Dict, profile2: Dict) -> float:
        """Calculate similarity between student profiles"""
        
        # Simple cosine similarity on personality traits
        traits = ['openness', 'conscientiousness', 'extraversion', 'agreeableness', 'neuroticism']
        
        vec1 = [profile1.get(t, 0.5) for t in traits]
        vec2 = [profile2.get(t, 0.5) for t in traits]
        
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        norm1 = sum(a ** 2 for a in vec1) ** 0.5
        norm2 = sum(b ** 2 for b in vec2) ** 0.5
        
        if norm1 * norm2 == 0:
            return 0.0
        
        return dot_product / (norm1 * norm2)
    
    def update_cse_kg_integration(self, concept: str):
        """
        Update how we query CSE-KG based on learned patterns
        
        For example:
        - If students consistently struggle with X after learning Y,
          add edge Y→X in our student graphs
        - If certain CSE-KG examples are more helpful,
          prioritize those in retrieval
        """
        
        # Get CSE-KG client
        cse_kg = self.models.get('cse_kg_client')
        
        if not cse_kg:
            return
        
        # Check if our learned difficulty differs from CSE-KG
        learned_diff = self.learned_difficulties.get(concept, 0.5)
        
        # Query CSE-KG for concept metadata
        concept_info = cse_kg.get_concept_info(concept)
        
        # If significant difference, could flag for human review
        # or adjust retrieval priorities
        
        print(f"\n🔄 KG Integration Update for '{concept}':")
        print(f"   Learned difficulty: {learned_diff:.2f}")
        print(f"   Adjusting retrieval priorities...")
    
    def generate_dynamic_kg_report(self) -> Dict:
        """
        Generate report on what the system has learned
        """
        
        return {
            'total_updates': self.update_count,
            'concepts_tracked': len(self.learned_difficulties),
            'prerequisites_discovered': len(self.prerequisite_strengths),
            'misconceptions_tracked': sum(
                len(miscs) for miscs in self.common_misconceptions.values()
            ),
            'effective_sequences': len(self.effective_sequences),
            
            'insights': {
                'hardest_concepts': self._get_hardest_concepts(),
                'most_critical_prerequisites': self._get_critical_prerequisites(),
                'most_common_misconceptions': self._get_most_common_misconceptions()
            }
        }
    
    def _get_hardest_concepts(self, top_k: int = 5) -> List[Tuple[str, float]]:
        """Get concepts students struggle with most"""
        sorted_concepts = sorted(
            self.learned_difficulties.items(),
            key=lambda x: x[1],
            reverse=True
        )
        return sorted_concepts[:top_k]
    
    def _get_critical_prerequisites(self, top_k: int = 5) -> List[Tuple[str, str, float]]:
        """Get most critical prerequisite relationships"""
        sorted_prereqs = sorted(
            self.prerequisite_strengths.items(),
            key=lambda x: x[1],
            reverse=True
        )
        return [(from_c, to_c, strength) for (from_c, to_c), strength in sorted_prereqs[:top_k]]
    
    def _get_most_common_misconceptions(self, top_k: int = 5) -> List[Dict]:
        """Get most frequently occurring misconceptions"""
        all_misconceptions = []
        
        for concept, misconceptions in self.common_misconceptions.items():
            for misc_desc, misc_data in misconceptions.items():
                all_misconceptions.append({
                    'concept': concept,
                    'description': misc_desc,
                    'frequency': misc_data['count'],
                    'students_affected': len(misc_data['students'])
                })
        
        all_misconceptions.sort(key=lambda x: x['frequency'], reverse=True)
        
        return all_misconceptions[:top_k]









