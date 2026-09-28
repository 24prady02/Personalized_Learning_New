"""
Adaptive Explanation Generator
Considers student's prior knowledge, prerequisites, learning style, and cognitive state
to generate the best possible explanation for each individual student

Based on:
- FOKE (Foundation models, Knowledge graphs, Prompt engineering)
- SkillTree (Knowledge graphs + LLMs for personalized learning)
- Causal inference for learning path optimization
"""

from typing import Dict, List, Optional, Tuple
from enum import Enum
import yaml
from pathlib import Path


class ExplanationComplexity(Enum):
    """Explanation complexity levels"""
    VERY_SIMPLE = 1  # No prerequisites assumed
    SIMPLE = 2  # Basic prerequisites
    MODERATE = 3  # Some prerequisites
    DETAILED = 4  # Most prerequisites
    ADVANCED = 5  # All prerequisites assumed


class ExplanationStyle(Enum):
    """Explanation styles based on learning preferences"""
    VISUAL = "visual"  # Diagrams, examples
    VERBAL = "verbal"  # Text-heavy, detailed
    ACTIVE = "active"  # Hands-on, interactive
    REFLECTIVE = "reflective"  # Step-by-step, analytical
    SEQUENTIAL = "sequential"  # Linear, step-by-step
    GLOBAL = "global"  # Big picture first, then details


class AdaptiveExplanationGenerator:
    """
    Generates adaptive explanations considering:
    1. Student's prior knowledge (from Student State Tracker)
    2. Prerequisites (from CSE-KG)
    3. Learning style (from Personality Profiler)
    4. Cognitive state (from COKE)
    5. Cognitive load management
    6. Learning progression (from Pedagogical KG)
    """
    
    def __init__(self, config: Dict):
        """
        Args:
            config: Configuration dictionary
        """
        self.config = config
        
        # Initialize components
        self._init_components()
        
        # Explanation strategies
        self.explanation_strategies = self._initialize_strategies()
    
    def _init_components(self):
        """Initialize required components"""
        # Pedagogical KG
        from .pedagogical_kg_integration import PedagogicalKGIntegration
        self.pedagogical_kg = PedagogicalKGIntegration(self.config)
        
        # CSE-KG client (for prerequisites) - Get from Pedagogical KG
        self.cse_kg = self.pedagogical_kg.cse_kg_client
        
        # COKE Cognitive Graph (for Theory of Mind)
        self.coke_graph = None
        if self.config.get('coke', {}).get('enabled', False):
            try:
                from .coke_cognitive_graph import COKECognitiveGraph
                self.coke_graph = COKECognitiveGraph(self.config.get('coke', {}))
            except Exception as e:
                print(f"[WARN] COKE graph not available: {e}")
                self.coke_graph = None
        
        # Student State Tracker (for mastery) - will be passed from orchestrator
        self.state_tracker = None
        
        # Personality Profiler (for learning style) - will be passed from orchestrator
        self.personality_profiler = None
    
    def _initialize_strategies(self) -> Dict:
        """Initialize explanation strategies"""
        return {
            "build_on_known": {
                "description": "Build explanation on concepts student already knows",
                "complexity": ExplanationComplexity.SIMPLE,
                "use_when": "Student has strong prerequisites"
            },
            "fill_gaps_first": {
                "description": "Fill knowledge gaps before explaining target concept",
                "complexity": ExplanationComplexity.VERY_SIMPLE,
                "use_when": "Student missing critical prerequisites"
            },
            "scaffold_gradually": {
                "description": "Gradually increase complexity",
                "complexity": ExplanationComplexity.MODERATE,
                "use_when": "Student has partial prerequisites"
            },
            "analogy_based": {
                "description": "Use analogies to relate to known concepts",
                "complexity": ExplanationComplexity.SIMPLE,
                "use_when": "Student learns by comparison"
            },
            "example_driven": {
                "description": "Start with examples, then explain theory",
                "complexity": ExplanationComplexity.MODERATE,
                "use_when": "Student prefers active learning"
            }
        }
    
    def generate_adaptive_explanation(self,
                                     concept: str,
                                     student_id: str,
                                     student_data: Dict) -> Dict:
        """
        Generate adaptive explanation for a concept
        
        Args:
            concept: Concept to explain
            student_id: Student identifier
            student_data: Student context (code, error, conversation, etc.)
            
        Returns:
            Adaptive explanation with:
            - Explanation text (adapted to student)
            - Prerequisites checked
            - Knowledge gaps addressed
            - Learning style adaptation
            - Cognitive load management
        """
        # ===== STEP 1: ASSESS STUDENT'S PRIOR KNOWLEDGE =====
        prior_knowledge = self._assess_prior_knowledge(student_id, concept)
        
        # ===== STEP 2: IDENTIFY PREREQUISITES =====
        prerequisites = self._get_prerequisites(concept)
        
        # ===== STEP 3: CHECK KNOWLEDGE GAPS =====
        knowledge_gaps = self._identify_knowledge_gaps(
            prior_knowledge, prerequisites
        )
        
        # ===== STEP 4: GET STUDENT PROFILE =====
        student_profile = self._get_student_profile(student_id, student_data)
        
        # ===== STEP 5: SELECT EXPLANATION STRATEGY =====
        strategy = self._select_strategy(
            prior_knowledge, knowledge_gaps, student_profile
        )
        
        # ===== STEP 6: DETERMINE COMPLEXITY =====
        complexity = self._determine_complexity(
            prior_knowledge, knowledge_gaps, student_profile
        )
        
        # ===== STEP 7: ADAPT TO LEARNING STYLE =====
        style_adaptation = self._adapt_to_learning_style(
            student_profile, concept
        )
        
        # ===== STEP 8: MANAGE COGNITIVE LOAD =====
        cognitive_load_info = self._manage_cognitive_load(
            concept, complexity, student_profile
        )
        
        # ===== STEP 9: GENERATE EXPLANATION =====
        explanation = self._generate_explanation_text(
            concept=concept,
            prior_knowledge=prior_knowledge,
            knowledge_gaps=knowledge_gaps,
            strategy=strategy,
            complexity=complexity,
            style=style_adaptation,
            cognitive_load=cognitive_load_info,
            student_data=student_data
        )
        
        # Extract concepts dynamically
        concepts_identified = self._extract_concepts_from_data(student_data)
        
        return {
            "explanation": explanation,
            "prior_knowledge": prior_knowledge,
            "prerequisites": prerequisites,
            "knowledge_gaps": knowledge_gaps,
            "strategy": strategy,
            "complexity": complexity.value,
            "learning_style_adaptation": style_adaptation,
            "cognitive_load": cognitive_load_info,
            "personalization_factors": {
                "based_on_prior_knowledge": True,
                "gaps_addressed": len(knowledge_gaps) > 0,
                "style_adapted": True,
                "load_managed": True
            },
            "knowledge_graphs_used": {
                "cse_kg": self.cse_kg is not None,
                "pedagogical_kg": self.pedagogical_kg is not None,
                "coke": self.coke_graph is not None,
                "state_tracker": self.state_tracker is not None,
                "personality_profiler": self.personality_profiler is not None
            },
            "concepts_identified": concepts_identified,
            "primary_concept": concept
        }
    
    def _assess_prior_knowledge(self, student_id: str, concept: str) -> Dict:
        """
        Assess what student already knows using Student State Tracker
        
        Returns:
            Dictionary with:
            - mastery_scores: Dict[concept -> mastery (0.0-1.0)]
            - strong_areas: List of concepts student knows well
            - weak_areas: List of concepts student struggles with
        """
        mastery_scores = {}
        strong_areas = []
        weak_areas = []
        
        # Use Student State Tracker to get mastery
        if self.state_tracker:
            try:
                knowledge_state = self.state_tracker.get_knowledge_state(student_id)
                mastery_scores = knowledge_state.get('concept_mastery', {})
                
                # Get related concepts
                related_concepts = [concept, "functions", "variables", "conditional_statements", "loops"]
                for related_concept in related_concepts:
                    if related_concept not in mastery_scores:
                        mastery_scores[related_concept] = 0.5  # Default moderate
                
                # Classify areas
                for concept_name, score in mastery_scores.items():
                    if score >= 0.7:
                        strong_areas.append(concept_name)
                    elif score < 0.5:
                        weak_areas.append(concept_name)
            except Exception as e:
                print(f"[WARN] Student State Tracker mastery assessment failed: {e}")
        
        # If no tracker data, use heuristics
        if not mastery_scores:
            # Default: assume basic knowledge
            mastery_scores = {
                "functions": 0.6,
                "variables": 0.6,
                "conditional_statements": 0.5,
                concept: 0.3  # Target concept assumed weak
            }
        
        return {
            "mastery_scores": mastery_scores,
            "strong_areas": strong_areas,
            "weak_areas": weak_areas,
            "average_mastery": sum(mastery_scores.values()) / len(mastery_scores) if mastery_scores else 0.5
        }
    
    def _get_prerequisites(self, concept: str) -> List[Dict]:
        """
        Get prerequisites for concept from CSE-KG
        
        Returns:
            List of prerequisite concepts with their importance
        """
        prerequisites = []
        
        # Try CSE-KG first (primary source)
        if self.cse_kg:
            try:
                # Get prerequisites from CSE-KG
                prereqs = self.cse_kg.get_prerequisites(concept)
                if prereqs:
                    for prereq in prereqs:
                        prerequisites.append({
                            "concept": prereq,
                            "importance": "high",
                            "source": "cse_kg"
                        })
            except Exception as e:
                print(f"[WARN] CSE-KG prerequisite query failed: {e}")
        
        # Fallback/Supplement: Use Pedagogical KG
        if not prerequisites:
            try:
                concept_info = self.pedagogical_kg.get_concept_full_info(concept)
                if concept_info:
                    # Get from domain_knowledge
                    domain_knowledge = concept_info.get("domain_knowledge", {})
                    prereqs = domain_knowledge.get("prerequisites", [])
                    if prereqs:
                        for prereq in prereqs:
                            # Avoid duplicates
                            if not any(p["concept"] == prereq for p in prerequisites):
                                prerequisites.append({
                                    "concept": prereq,
                                    "importance": "medium",
                                    "source": "pedagogical_kg"
                                })
            except Exception as e:
                print(f"[WARN] Pedagogical KG prerequisite query failed: {e}")
        
        return prerequisites
    
    def _identify_knowledge_gaps(self, prior_knowledge: Dict,
                                 prerequisites: List[Dict]) -> List[Dict]:
        """
        Identify knowledge gaps (missing prerequisites)
        
        Returns:
            List of knowledge gaps with severity
        """
        gaps = []
        mastery_scores = prior_knowledge.get("mastery_scores", {})
        
        for prereq in prerequisites:
            prereq_concept = prereq["concept"]
            mastery = mastery_scores.get(prereq_concept, 0.0)
            
            if mastery < 0.5:  # Below threshold
                severity = "critical" if mastery < 0.3 else "high"
                gaps.append({
                    "concept": prereq_concept,
                    "mastery": mastery,
                    "severity": severity,
                    "importance": prereq.get("importance", "medium"),
                    "blocks": True  # Blocks understanding of target concept
                })
        
        return gaps
    
    def _get_student_profile(self, student_id: str, student_data: Dict) -> Dict:
        """
        Get student's learning profile
        
        Returns:
            Dictionary with:
            - learning_style: Visual/Verbal, Active/Reflective, Sequential/Global
            - personality: Big Five traits
            - cognitive_state: Current cognitive state
        """
        profile = {
            "learning_style": {
                "visual_verbal": "visual",  # Default
                "active_reflective": "active",
                "sequential_global": "sequential"
            },
            "personality": {
                "openness": 0.5,
                "conscientiousness": 0.5,
                "extraversion": 0.5,
                "agreeableness": 0.5,
                "neuroticism": 0.5
            },
            "cognitive_state": "engaged"
        }
        
        # Get personality and learning style from Personality Profiler (if available)
        # Note: Personality profiler should be passed from orchestrator
        # For now, use simple heuristics based on conversation
        try:
            conversation_text = ""
            if "conversation" in student_data:
                conv = student_data["conversation"]
                if isinstance(conv, list):
                    conversation_text = " ".join([str(m) for m in conv])
                else:
                    conversation_text = str(conv)
            if "question" in student_data:
                conversation_text += " " + str(student_data["question"])
            
            # Simple personality inference (can be enhanced with Personality Profiler)
            if conversation_text:
                text_lower = conversation_text.lower()
                # Simple heuristics
                if "step by step" in text_lower or "organized" in text_lower:
                    profile["personality"] = profile.get("personality", {})
                    profile["personality"]["conscientiousness"] = 0.7
                if "what if" in text_lower or "maybe" in text_lower:
                    profile["personality"] = profile.get("personality", {})
                    profile["personality"]["openness"] = 0.7
                    
                # Simple learning style inference
                if "visual" in text_lower or "see" in text_lower or "show" in text_lower:
                    profile["learning_style"] = {"visual_verbal": "visual"}
                elif "read" in text_lower or "explain" in text_lower:
                    profile["learning_style"] = {"visual_verbal": "verbal"}
        except Exception as e:
            print(f"[WARN] Personality profiling failed: {e}")
        
        # Get cognitive state from COKE graph (if available)
        if self.coke_graph:
            try:
                # Use COKE to infer Theory of Mind from student data
                tom_result = self.coke_graph.infer_theory_of_mind(student_data)
                profile["cognitive_state"] = tom_result.get("cognitive_state", "engaged")
                profile["behavioral_response"] = tom_result.get("behavioral_response", "continue")
                profile["tom_confidence"] = tom_result.get("confidence", 0.5)
                profile["tom_reasoning"] = tom_result.get("reasoning", "")
            except Exception as e:
                print(f"[WARN] COKE inference failed: {e}")
                # Fallback to student_data
                if "theory_of_mind" in student_data:
                    tom = student_data["theory_of_mind"]
                    profile["cognitive_state"] = tom.get("cognitive_state", "engaged")
        else:
            # Fallback: Get cognitive state from student_data
            if "theory_of_mind" in student_data:
                tom = student_data["theory_of_mind"]
                profile["cognitive_state"] = tom.get("cognitive_state", "engaged")
        
        return profile
    
    def _select_strategy(self, prior_knowledge: Dict,
                        knowledge_gaps: List[Dict],
                        student_profile: Dict) -> str:
        """
        Select best explanation strategy
        
        Returns:
            Strategy name
        """
        # If critical gaps, fill gaps first
        critical_gaps = [g for g in knowledge_gaps if g["severity"] == "critical"]
        if critical_gaps:
            return "fill_gaps_first"
        
        # If strong prerequisites, build on known
        avg_mastery = prior_knowledge.get("average_mastery", 0.5)
        if avg_mastery >= 0.7 and len(knowledge_gaps) == 0:
            return "build_on_known"
        
        # If partial prerequisites, scaffold
        if 0.3 <= avg_mastery < 0.7:
            return "scaffold_gradually"
        
        # If visual learner, use analogies
        learning_style = student_profile.get("learning_style", {})
        if learning_style.get("visual_verbal") == "visual":
            return "analogy_based"
        
        # If active learner, use examples
        if learning_style.get("active_reflective") == "active":
            return "example_driven"
        
        # Default
        return "scaffold_gradually"
    
    def _determine_complexity(self, prior_knowledge: Dict,
                             knowledge_gaps: List[Dict],
                             student_profile: Dict) -> ExplanationComplexity:
        """
        Determine appropriate explanation complexity
        """
        avg_mastery = prior_knowledge.get("average_mastery", 0.5)
        num_gaps = len(knowledge_gaps)
        
        # More gaps = simpler explanation
        if num_gaps > 2 or avg_mastery < 0.3:
            return ExplanationComplexity.VERY_SIMPLE
        elif num_gaps > 0 or avg_mastery < 0.5:
            return ExplanationComplexity.SIMPLE
        elif avg_mastery < 0.7:
            return ExplanationComplexity.MODERATE
        elif avg_mastery < 0.9:
            return ExplanationComplexity.DETAILED
        else:
            return ExplanationComplexity.ADVANCED
    
    def _adapt_to_learning_style(self, student_profile: Dict,
                                 concept: str) -> Dict:
        """
        Adapt explanation to learning style
        
        Returns:
            Style adaptation instructions
        """
        learning_style = student_profile.get("learning_style", {})
        
        adaptations = {
            "visual_verbal": learning_style.get("visual_verbal", "visual"),
            "active_reflective": learning_style.get("active_reflective", "active"),
            "sequential_global": learning_style.get("sequential_global", "sequential"),
            "preferred_format": [],
            "avoid_format": []
        }
        
        # Visual learners: diagrams, examples, visualizations
        if adaptations["visual_verbal"] == "visual":
            adaptations["preferred_format"].extend([
                "diagrams", "examples", "visualizations", "code_samples"
            ])
            adaptations["avoid_format"].append("long_text")
        
        # Verbal learners: detailed text, explanations
        else:
            adaptations["preferred_format"].extend([
                "detailed_text", "explanations", "definitions"
            ])
        
        # Active learners: hands-on, examples first
        if adaptations["active_reflective"] == "active":
            adaptations["preferred_format"].extend([
                "examples_first", "hands_on", "interactive"
            ])
            adaptations["order"] = "example_then_theory"
        else:
            adaptations["order"] = "theory_then_example"
        
        # Sequential learners: step-by-step
        if adaptations["sequential_global"] == "sequential":
            adaptations["preferred_format"].extend([
                "step_by_step", "linear", "progressive"
            ])
        else:
            adaptations["preferred_format"].extend([
                "big_picture_first", "overview", "connections"
            ])
        
        return adaptations
    
    def _manage_cognitive_load(self, concept: str,
                              complexity: ExplanationComplexity,
                              student_profile: Dict) -> Dict:
        """
        Manage cognitive load for explanation
        
        Returns:
            Cognitive load management instructions
        """
        # Get cognitive load info from Pedagogical KG
        load_info = self.pedagogical_kg.get_cognitive_load_info(concept)
        
        if not load_info:
            load_info = {
                "intrinsic_load": 3,  # Default moderate
                "extraneous_load": 2,
                "germane_load": 3,
                "total_load": 3
            }
        
        # Adjust based on complexity
        if complexity == ExplanationComplexity.VERY_SIMPLE:
            load_info["target_load"] = 2  # Keep it low
        elif complexity == ExplanationComplexity.SIMPLE:
            load_info["target_load"] = 2.5
        elif complexity == ExplanationComplexity.MODERATE:
            load_info["target_load"] = 3
        elif complexity == ExplanationComplexity.DETAILED:
            load_info["target_load"] = 3.5
        else:
            load_info["target_load"] = 4
        
        # Strategies to reduce load
        load_info["strategies"] = []
        if load_info["total_load"] > load_info["target_load"]:
            load_info["strategies"].extend([
                "break_into_smaller_parts",
                "use_analogies",
                "provide_examples",
                "avoid_jargon",
                "use_visuals"
            ])
        
        return load_info
    
    def _generate_explanation_text(self, concept: str,
                                   prior_knowledge: Dict,
                                   knowledge_gaps: List[Dict],
                                   strategy: str,
                                   complexity: ExplanationComplexity,
                                   style: Dict,
                                   cognitive_load: Dict,
                                   student_data: Dict) -> str:
        """
        Generate actual explanation text
        
        This is a template - in production, would use LLM with prompts
        """
        explanation_parts = []
        
        # ===== 1. ADDRESS KNOWLEDGE GAPS FIRST =====
        if knowledge_gaps and strategy == "fill_gaps_first":
            explanation_parts.append("Before we dive into this, let's make sure you have the basics:")
            for gap in knowledge_gaps[:2]:  # Top 2 gaps
                explanation_parts.append(
                    f"- {gap['concept']} (you're at {gap['mastery']:.0%} mastery - let's review this first)"
                )
            explanation_parts.append("")
        
        # ===== 2. BUILD ON PRIOR KNOWLEDGE =====
        if strategy == "build_on_known" and prior_knowledge.get("strong_areas"):
            strong = prior_knowledge["strong_areas"][:2]
            explanation_parts.append(
                f"Great! I see you already understand {', '.join(strong)}. "
                f"Let's build on that to understand {concept}."
            )
            explanation_parts.append("")
        
        # ===== 3. MAIN EXPLANATION =====
        if style.get("order") == "example_then_theory":
            # Example first
            explanation_parts.append("Let's start with an example:")
            explanation_parts.append(self._get_example(concept))
            explanation_parts.append("")
            explanation_parts.append("Now let's understand why this works:")
            explanation_parts.append(self._get_theory(concept, complexity))
        else:
            # Theory first
            explanation_parts.append(self._get_theory(concept, complexity))
            explanation_parts.append("")
            explanation_parts.append("Here's an example:")
            explanation_parts.append(self._get_example(concept))
        
        # ===== 4. ANALOGY (if visual learner) =====
        if style.get("visual_verbal") == "visual" and strategy == "analogy_based":
            analogy = self._get_analogy(concept)
            if analogy:
                explanation_parts.append("")
                explanation_parts.append(f"Think of it like this: {analogy}")
        
        # ===== 5. STEP-BY-STEP (if sequential learner) =====
        if style.get("sequential_global") == "sequential":
            steps = self._get_steps(concept)
            if steps:
                explanation_parts.append("")
                explanation_parts.append("Here's how to do it step by step:")
                for i, step in enumerate(steps, 1):
                    explanation_parts.append(f"{i}. {step}")
        
        return "\n".join(explanation_parts)
    
    def _get_theory(self, concept: str, complexity: ExplanationComplexity) -> str:
        """Get theoretical explanation (simplified)"""
        # In production, would query Pedagogical KG or use LLM
        if "recursion" in concept.lower():
            if complexity in [ExplanationComplexity.VERY_SIMPLE, ExplanationComplexity.SIMPLE]:
                return "Recursion is when a function calls itself. It needs a stopping point (base case) to avoid going forever."
            else:
                return "Recursion is a programming technique where a function calls itself to solve a problem. It requires a base case (stopping condition) and a recursive case (calling itself with simpler input)."
        return f"Here's how {concept} works..."
    
    def _get_example(self, concept: str) -> str:
        """Get example (simplified)"""
        if "recursion" in concept.lower():
            return """
def factorial(n):
    if n <= 1:        # Base case - stop here!
        return 1
    return n * factorial(n - 1)  # Recursive case - call itself
"""
        return "Example code here..."
    
    def _get_analogy(self, concept: str) -> str:
        """Get analogy (simplified)"""
        if "recursion" in concept.lower():
            return "Like climbing stairs - you need to know when to stop (base case) or you'll fall forever."
        return None
    
    def _get_steps(self, concept: str) -> List[str]:
        """Get step-by-step instructions"""
        if "recursion" in concept.lower():
            return [
                "Every recursive function needs a base case (stopping point)",
                "Without it, the function calls itself forever",
                "Add an 'if' statement that checks when to stop",
                "For factorial, stop when n is 0 or 1"
            ]
        return []
    
    def _extract_concepts_from_data(self, student_data: Dict) -> List[str]:
        """
        Dynamically extract concepts from student data using CSE-KG
        """
        concepts = []
        
        # Extract from code and error using CSE-KG
        code = student_data.get("code", "")
        error = student_data.get("error_message", "")
        question = student_data.get("question", "")
        
        if self.cse_kg:
            try:
                # Use concept retriever if available
                from src.knowledge_graph.query_engine import ConceptRetriever
                retriever = ConceptRetriever(self.cse_kg)
                extracted = retriever.retrieve_from_code(code, error)
                concepts.extend(extracted)
            except Exception as e:
                print(f"[WARN] CSE-KG concept extraction failed: {e}")
        
        # Fallback: keyword-based extraction
        if not concepts:
            text = f"{code} {error} {question}".lower()
            concept_keywords = {
                'recursion': ['recursion', 'recursive', 'base case', 'factorial'],
                'loops': ['loop', 'for', 'while', 'iterate', 'iteration'],
                'functions': ['function', 'def', 'call', 'return'],
                'variables': ['variable', 'assign', '=', 'var'],
                'conditional_statements': ['if', 'else', 'elif', 'conditional', 'condition'],
                'data_structures': ['list', 'dict', 'array', 'tuple', 'set'],
                'algorithms': ['algorithm', 'sort', 'search', 'binary'],
                'object_oriented': ['class', 'object', 'method', 'attribute', 'instance'],
                'error_handling': ['try', 'except', 'error', 'exception', 'raise']
            }
            
            for concept, keywords in concept_keywords.items():
                if any(kw in text for kw in keywords):
                    concepts.append(concept)
        
        return list(set(concepts)) if concepts else ['programming']

