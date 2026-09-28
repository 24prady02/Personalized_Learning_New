"""
Unified Explanation Generator
Combines Theory of Mind (COKE) + Misconceptions (Pedagogical KG) to create explanations

Two Input Types:
1. Theory of Mind (COKE) - WHY student went wrong cognitively
2. Misconceptions (Pedagogical KG) - WHAT misconception they have

Output: Best explanation combining both cognitive understanding and misconception correction
"""

from typing import Dict, List, Optional
from .coke_cognitive_graph import COKECognitiveGraph, CognitiveState, BehavioralResponse
from .pedagogical_kg_builder import PedagogicalKGBuilder
from .error_explanation_mapper import ErrorExplanationMapper, ErrorPattern, RootCause


class UnifiedExplanationGenerator:
    """
    Generates explanations by combining:
    1. Theory of Mind (COKE) - Cognitive reasons why student went wrong
    2. Misconceptions (Pedagogical KG) - What wrong knowledge they have
    
    Creates unified output explaining both WHY and HOW TO FIX
    """
    
    def __init__(self, config: Dict, pedagogical_builder: PedagogicalKGBuilder,
                 coke_graph: Optional[COKECognitiveGraph] = None):
        """
        Args:
            config: Configuration dictionary
            pedagogical_builder: Pedagogical KG builder (for misconceptions)
            coke_graph: COKE graph (for Theory of Mind)
        """
        self.config = config
        self.pedagogical_builder = pedagogical_builder
        self.coke_graph = coke_graph
        
        # Initialize error mapper
        self.error_mapper = ErrorExplanationMapper(
            config,
            pedagogical_builder=pedagogical_builder,
            coke_graph=coke_graph
        )
    
    def generate_unified_explanation(self, code: Optional[str] = None,
                                    error_message: Optional[str] = None,
                                    student_data: Optional[Dict] = None) -> Dict:
        """
        Generate unified explanation combining Theory of Mind + Misconceptions
        
        Args:
            code: Student's code
            error_message: Error message
            student_data: Student context
            
        Returns:
            Unified explanation with:
            - Theory of Mind analysis (WHY cognitively)
            - Misconception detection (WHAT wrong knowledge)
            - Combined best explanation
        """
        result = {
            "theory_of_mind": {},
            "misconception": {},
            "unified_explanation": {}
        }
        
        # ===== PART 1: THEORY OF MIND (COKE) =====
        if self.coke_graph and student_data:
            tom_analysis = self.coke_graph.infer_theory_of_mind(student_data)
            result["theory_of_mind"] = {
                "cognitive_state": tom_analysis.get("cognitive_state"),
                "why_student_went_wrong": tom_analysis.get("reasoning"),
                "predicted_behavior": tom_analysis.get("behavioral_response"),
                "confidence": tom_analysis.get("confidence")
            }
        else:
            # Fallback: infer from error
            if error_message:
                if "RecursionError" in error_message:
                    result["theory_of_mind"] = {
                        "cognitive_state": "confused",
                        "why_student_went_wrong": "Student doesn't understand recursion needs a stopping condition",
                        "predicted_behavior": "ask_question"
                    }
                elif "UnboundLocalError" in error_message:
                    result["theory_of_mind"] = {
                        "cognitive_state": "confused",
                        "why_student_went_wrong": "Student has incorrect mental model of variable scope",
                        "predicted_behavior": "search_info"
                    }
        
        # ===== PART 2: MISCONCEPTION DETECTION (Pedagogical KG) =====
        # Detect misconception from code/error
        concept = None
        if code or error_message:
            # Try to extract concept from error
            if "recursion" in str(error_message).lower() or "recursive" in str(code).lower():
                concept = "recursion"
            elif "scope" in str(error_message).lower() or "UnboundLocalError" in str(error_message):
                concept = "variable_scope"
            elif "IndexError" in str(error_message) or "index" in str(error_message).lower():
                concept = "loops"
        
        if concept:
            misconception = self.pedagogical_builder.detect_misconception(
                concept=concept,
                code=code,
                error_message=error_message
            )
            
            if misconception:
                result["misconception"] = {
                    "detected": True,
                    "misconception_id": misconception.id,
                    "description": misconception.description,
                    "what_student_believes_wrong": misconception.description,
                    "severity": misconception.severity.value,
                    "correction_strategy": misconception.correction_strategy
                }
                
                # Get recommended interventions for this misconception
                interventions = self.pedagogical_builder.get_recommended_interventions(
                    concept=concept,
                    misconception_id=misconception.id
                )
                
                if interventions:
                    best_intervention = max(interventions, key=lambda x: x.effectiveness_score)
                    result["misconception"]["best_intervention"] = {
                        "name": best_intervention.name,
                        "type": best_intervention.type.value,
                        "description": best_intervention.description,
                        "content_template": best_intervention.content_template,
                        "effectiveness": best_intervention.effectiveness_score
                    }
            else:
                result["misconception"] = {
                    "detected": False,
                    "message": "No specific misconception detected"
                }
        
        # ===== PART 3: ERROR-TO-EXPLANATION MAPPING =====
        error_explanation = self.error_mapper.generate_explanation(
            code=code,
            error_message=error_message,
            student_data=student_data
        )
        
        if error_explanation.get("error_detected"):
            result["error_analysis"] = {
                "error_type": error_explanation["error"]["type"],
                "error_description": error_explanation["error"]["description"],
                "root_cause": error_explanation.get("root_cause", {}),
                "best_explanation_strategy": error_explanation.get("best_explanation", {})
            }
        
        # ===== PART 4: UNIFIED EXPLANATION (COMBINING BOTH) =====
        result["unified_explanation"] = self._combine_explanations(
            theory_of_mind=result.get("theory_of_mind", {}),
            misconception=result.get("misconception", {}),
            error_analysis=result.get("error_analysis", {})
        )
        
        return result
    
    def _combine_explanations(self, theory_of_mind: Dict, misconception: Dict,
                             error_analysis: Dict) -> Dict:
        """
        Combine Theory of Mind + Misconception into unified explanation
        
        Args:
            theory_of_mind: COKE analysis
            misconception: Pedagogical KG misconception
            error_analysis: Error-to-explanation mapping
            
        Returns:
            Unified explanation combining all three
        """
        unified = {
            "why_student_went_wrong": [],
            "what_student_believes_wrong": [],
            "best_way_to_help_understand": "",
            "explanation_components": []
        }
        
        # Combine WHY (Theory of Mind)
        if theory_of_mind.get("why_student_went_wrong"):
            unified["why_student_went_wrong"].append(
                theory_of_mind["why_student_went_wrong"]
            )
        
        if error_analysis.get("root_cause", {}).get("cognitive_reason"):
            unified["why_student_went_wrong"].append(
                error_analysis["root_cause"]["cognitive_reason"]
            )
        
        # Combine WHAT (Misconception)
        if misconception.get("what_student_believes_wrong"):
            unified["what_student_believes_wrong"].append(
                misconception["what_student_believes_wrong"]
            )
        
        # Combine BEST EXPLANATION
        explanations = []
        
        # From misconception intervention
        if misconception.get("best_intervention"):
            exp = misconception["best_intervention"]
            explanations.append({
                "source": "misconception_correction",
                "strategy": exp.get("name"),
                "explanation": exp.get("content_template"),
                "effectiveness": exp.get("effectiveness", 0.5)
            })
        
        # From error explanation strategy
        if error_analysis.get("best_explanation_strategy"):
            exp = error_analysis["best_explanation_strategy"]
            explanations.append({
                "source": "error_root_cause",
                "strategy": exp.get("strategy"),
                "explanation": exp.get("explanation"),
                "effectiveness": exp.get("effectiveness", 0.5)
            })
        
        # Select best explanation (highest effectiveness)
        if explanations:
            best = max(explanations, key=lambda x: x["effectiveness"])
            unified["best_way_to_help_understand"] = best["explanation"]
            unified["explanation_components"] = explanations
        
        # Create summary
        unified["summary"] = self._create_summary(
            theory_of_mind, misconception, error_analysis
        )
        
        return unified
    
    def generate_student_friendly_output(self, code: Optional[str] = None,
                                       error_message: Optional[str] = None,
                                       student_data: Optional[Dict] = None) -> Dict:
        """
        Generate complete student-friendly explanation
        
        Combines all analysis and converts to understandable format
        
        Args:
            code: Student's code
            error_message: Error message
            student_data: Student context
            
        Returns:
            Complete student-friendly explanation
        """
        from .student_friendly_explainer import StudentFriendlyExplainer
        
        # Get unified analysis
        analysis = self.generate_unified_explanation(
            code=code,
            error_message=error_message,
            student_data=student_data
        )
        
        # Convert to student-friendly format
        explainer = StudentFriendlyExplainer(self.config)
        
        # Add code to analysis for better examples
        analysis_with_code = analysis.copy()
        if code:
            analysis_with_code["code"] = code
        
        friendly_explanation = explainer.generate_student_friendly_explanation(analysis_with_code)
        
        return {
            "analysis": analysis,  # Keep technical analysis
            "student_explanation": friendly_explanation,  # Student-friendly version
            "full_response": friendly_explanation.get("full_explanation", "")
        }
    
    def _create_summary(self, theory_of_mind: Dict, misconception: Dict,
                       error_analysis: Dict) -> str:
        """Create human-readable summary"""
        parts = []
        
        # Why they went wrong
        if theory_of_mind.get("why_student_went_wrong"):
            parts.append(f"WHY: {theory_of_mind['why_student_went_wrong']}")
        
        # What they believe wrong
        if misconception.get("what_student_believes_wrong"):
            parts.append(f"WHAT: Student believes: {misconception['what_student_believes_wrong']}")
        
        # Best explanation
        if error_analysis.get("best_explanation_strategy", {}).get("explanation"):
            parts.append(f"HOW TO HELP: {error_analysis['best_explanation_strategy']['explanation']}")
        
        return " | ".join(parts) if parts else "Analysis complete"

