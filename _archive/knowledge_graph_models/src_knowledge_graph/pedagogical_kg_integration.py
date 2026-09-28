"""
Integration module for Pedagogical Knowledge Graph
Provides easy access to unified pedagogical-CS knowledge graph
"""

from typing import Dict, List, Optional
from .cse_kg_client import CSEKGClient
from .pedagogical_kg_builder import PedagogicalKGBuilder
from .pedagogical_kg_schema import (
    ConceptPedagogicalData,
    Misconception,
    Intervention,
    LearningProgression
)
from .error_explanation_mapper import ErrorExplanationMapper


class PedagogicalKGIntegration:
    """
    High-level interface for accessing unified Pedagogical-CS Knowledge Graph
    
    Combines:
    - CSE-KG (domain knowledge)
    - Pedagogical data (misconceptions, progressions, cognitive load, interventions)
    """
    
    def __init__(self, config: Dict):
        """
        Args:
            config: Configuration dictionary
        """
        self.config = config
        
        # Initialize CSE-KG client
        self.cse_kg_client = CSEKGClient(config)
        
        # Initialize Pedagogical KG Builder
        self.pedagogical_builder = PedagogicalKGBuilder(self.cse_kg_client, config)
        
        # Initialize Error-to-Explanation Mapper
        # Try to get COKE if available
        coke_graph = None
        if config.get('coke', {}).get('enabled', False):
            try:
                from .coke_cognitive_graph import COKECognitiveGraph
                coke_graph = COKECognitiveGraph(config.get('coke', {}))
            except:
                pass
        
        self.error_mapper = ErrorExplanationMapper(
            config,
            pedagogical_builder=self.pedagogical_builder,
            coke_graph=coke_graph
        )
    
    def get_concept_full_info(self, concept: str) -> Dict:
        """
        Get complete information about a concept:
        - Domain knowledge (from CSE-KG)
        - Pedagogical data (misconceptions, cognitive load, interventions)
        
        Args:
            concept: Concept name
            
        Returns:
            Dictionary with complete concept information
        """
        result = {
            "concept": concept,
            "domain_knowledge": {},
            "pedagogical_data": {}
        }
        
        # Get domain knowledge from CSE-KG
        try:
            concept_info = self.cse_kg_client.get_concept_info(concept)
            if concept_info:
                result["domain_knowledge"] = {
                    "label": concept_info.get("label", ""),
                    "description": concept_info.get("description", ""),
                    "uri": concept_info.get("uri", "")
                }
            
            # Get prerequisites
            prereqs = self.cse_kg_client.get_prerequisites(concept)
            if prereqs:
                result["domain_knowledge"]["prerequisites"] = list(prereqs)
            
            # Get related concepts
            related = self.cse_kg_client.get_related_concepts(concept, max_distance=1)
            if related:
                result["domain_knowledge"]["related_concepts"] = [
                    {"concept": r[0], "relation": r[1]} for r in related
                ]
        except Exception as e:
            result["domain_knowledge"]["error"] = str(e)
        
        # Get pedagogical data
        pedagogical_data = self.pedagogical_builder.get_concept_pedagogical_info(concept)
        if pedagogical_data:
            result["pedagogical_data"] = {
                "cognitive_load": {
                    "intrinsic": pedagogical_data.cognitive_load.intrinsic_load,
                    "extraneous": pedagogical_data.cognitive_load.extraneous_load,
                    "germane": pedagogical_data.cognitive_load.germane_load,
                    "total": pedagogical_data.cognitive_load.total_load,
                    "factors": pedagogical_data.cognitive_load.factors
                },
                "difficulty_level": pedagogical_data.difficulty_level.value,
                "common_misconceptions": [
                    {
                        "id": mc.id,
                        "description": mc.description,
                        "severity": mc.severity.value,
                        "frequency": mc.frequency,
                        "common_indicators": mc.common_indicators
                    }
                    for mc in pedagogical_data.common_misconceptions
                ],
                "recommended_interventions": [
                    {
                        "id": intv.id,
                        "name": intv.name,
                        "type": intv.type.value,
                        "description": intv.description,
                        "effectiveness": intv.effectiveness_score
                    }
                    for intv in pedagogical_data.recommended_interventions
                ],
                "typical_struggles": pedagogical_data.typical_struggles,
                "success_indicators": pedagogical_data.success_indicators
            }
        
        return result
    
    def detect_student_misconception(self, concept: str, code: Optional[str] = None,
                                   error_message: Optional[str] = None) -> Optional[Dict]:
        """
        Detect if student code/error indicates a misconception
        
        Args:
            concept: Concept being worked on
            code: Student's code
            error_message: Error message if any
            
        Returns:
            Misconception information if detected, None otherwise
        """
        misconception = self.pedagogical_builder.detect_misconception(
            concept, code, error_message
        )
        
        if misconception:
            # Get recommended interventions for this misconception
            interventions = self.pedagogical_builder.get_recommended_interventions(
                concept, misconception.id
            )
            
            return {
                "misconception": {
                    "id": misconception.id,
                    "description": misconception.description,
                    "severity": misconception.severity.value,
                    "frequency": misconception.frequency,
                    "correction_strategy": misconception.correction_strategy
                },
                "recommended_interventions": [
                    {
                        "id": intv.id,
                        "name": intv.name,
                        "type": intv.type.value,
                        "description": intv.description,
                        "content_template": intv.content_template
                    }
                    for intv in interventions
                ]
            }
        
        return None
    
    def get_learning_path(self, target_concept: str,
                         current_mastery: Dict[str, float]) -> Dict:
        """
        Get recommended learning path to target concept
        
        Args:
            target_concept: Goal concept
            current_mastery: Dictionary of concept -> mastery level (0.0 to 1.0)
            
        Returns:
            Learning path information
        """
        # Get progression from pedagogical KG
        progression = self.pedagogical_builder.get_learning_progression(target_concept)
        
        if progression:
            # Find where student is in progression
            path = []
            for concept in progression.concept_sequence:
                mastery = current_mastery.get(concept, 0.0)
                threshold = progression.mastery_thresholds.get(concept, 0.7)
                
                path.append({
                    "concept": concept,
                    "current_mastery": mastery,
                    "required_mastery": threshold,
                    "ready": mastery >= threshold,
                    "estimated_time_hours": progression.estimated_time.get(concept, 2.0)
                })
                
                if concept == target_concept:
                    break
            
            return {
                "progression_id": progression.id,
                "path": path,
                "next_concept": next(
                    (p["concept"] for p in path if not p["ready"]),
                    target_concept
                )
            }
        else:
            # Fallback: use CSE-KG prerequisites
            try:
                prereqs = self.cse_kg_client.get_prerequisites(target_concept)
                path = [
                    {
                        "concept": p,
                        "current_mastery": current_mastery.get(p, 0.0),
                        "required_mastery": 0.7,
                        "ready": current_mastery.get(p, 0.0) >= 0.7,
                        "estimated_time_hours": 2.0
                    }
                    for p in prereqs
                ]
                path.append({
                    "concept": target_concept,
                    "current_mastery": current_mastery.get(target_concept, 0.0),
                    "required_mastery": 0.8,
                    "ready": current_mastery.get(target_concept, 0.0) >= 0.8,
                    "estimated_time_hours": 3.0
                })
                
                return {
                    "progression_id": None,
                    "path": path,
                    "next_concept": next(
                        (p["concept"] for p in path if not p["ready"]),
                        target_concept
                    )
                }
            except:
                return {
                    "progression_id": None,
                    "path": [{
                        "concept": target_concept,
                        "current_mastery": current_mastery.get(target_concept, 0.0),
                        "required_mastery": 0.8,
                        "ready": False,
                        "estimated_time_hours": 3.0
                    }],
                    "next_concept": target_concept
                }
    
    def get_interventions_for_struggle(self, concept: str,
                                      struggle_type: Optional[str] = None,
                                      misconception_id: Optional[str] = None) -> List[Dict]:
        """
        Get recommended interventions for a student struggle
        
        Args:
            concept: Concept student is struggling with
            struggle_type: Type of struggle (optional)
            misconception_id: Specific misconception ID (optional)
            
        Returns:
            List of recommended interventions
        """
        interventions = self.pedagogical_builder.get_recommended_interventions(
            concept, misconception_id
        )
        
        # Sort by effectiveness
        interventions.sort(key=lambda x: x.effectiveness_score, reverse=True)
        
        return [
            {
                "id": intv.id,
                "name": intv.name,
                "type": intv.type.value,
                "description": intv.description,
                "content_template": intv.content_template,
                "effectiveness": intv.effectiveness_score,
                "usage_count": intv.usage_count
            }
            for intv in interventions
        ]
    
    def generate_unified_explanation(self, code: Optional[str] = None,
                                    error_message: Optional[str] = None,
                                    student_data: Optional[Dict] = None) -> Dict:
        """
        Generate unified explanation combining:
        1. Theory of Mind (COKE) - WHY student went wrong cognitively
        2. Misconceptions (Pedagogical KG) - WHAT wrong knowledge they have
        
        Args:
            code: Student's code
            error_message: Error message
            student_data: Student context
            
        Returns:
            Unified explanation combining both Theory of Mind and Misconceptions
        """
        from .unified_explanation_generator import UnifiedExplanationGenerator
        
        # Get COKE if available
        coke_graph = None
        if self.config.get('coke', {}).get('enabled', False):
            try:
                from .coke_cognitive_graph import COKECognitiveGraph
                coke_graph = COKECognitiveGraph(self.config.get('coke', {}))
            except:
                pass
        
        # Create unified generator
        generator = UnifiedExplanationGenerator(
            self.config,
            pedagogical_builder=self.pedagogical_builder,
            coke_graph=coke_graph
        )
        
        return generator.generate_unified_explanation(
            code=code,
            error_message=error_message,
            student_data=student_data
        )
    
    def explain_to_student(self, code: Optional[str] = None,
                          error_message: Optional[str] = None,
                          student_data: Optional[Dict] = None) -> Dict:
        """
        Generate student-friendly explanation
        
        Converts complex analysis into clear, understandable explanation
        
        Args:
            code: Student's code
            error_message: Error message
            student_data: Student context (including conversation)
            
        Returns:
            Student-friendly explanation with:
            - Clear main explanation
            - Simple analogies
            - Step-by-step guidance
            - Encouraging tone
        """
        from .unified_explanation_generator import UnifiedExplanationGenerator
        
        # Get COKE if available
        coke_graph = None
        if self.config.get('coke', {}).get('enabled', False):
            try:
                from .coke_cognitive_graph import COKECognitiveGraph
                coke_graph = COKECognitiveGraph(self.config.get('coke', {}))
            except:
                pass
        
        # Create unified generator
        generator = UnifiedExplanationGenerator(
            self.config,
            pedagogical_builder=self.pedagogical_builder,
            coke_graph=coke_graph
        )
        
        return generator.generate_student_friendly_output(
            code=code,
            error_message=error_message,
            student_data=student_data
        )
    
    def get_cognitive_load_info(self, concept: str) -> Optional[Dict]:
        """
        Get cognitive load information for a concept
        
        Args:
            concept: Concept name
            
        Returns:
            Cognitive load information
        """
        pedagogical_data = self.pedagogical_builder.get_concept_pedagogical_info(concept)
        
        if pedagogical_data:
            return {
                "concept": concept,
                "intrinsic_load": pedagogical_data.cognitive_load.intrinsic_load,
                "extraneous_load": pedagogical_data.cognitive_load.extraneous_load,
                "germane_load": pedagogical_data.cognitive_load.germane_load,
                "total_load": pedagogical_data.cognitive_load.total_load,
                "factors": pedagogical_data.cognitive_load.factors,
                "difficulty_level": pedagogical_data.difficulty_level.value
            }
        
        return None

