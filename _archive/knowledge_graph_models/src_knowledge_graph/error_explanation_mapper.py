"""
Error-to-Explanation Knowledge Graph Mapper
Maps: Student Errors → Root Causes → Best Explanations

Enhances Pedagogical KG with:
- Error patterns and their root causes
- Optimal explanation strategies for each error
- Cognitive reasons why students make mistakes
- Best teaching approaches to help them understand
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import json
from pathlib import Path

from .pedagogical_kg_schema import (
    Misconception,
    Intervention,
    MisconceptionSeverity,
    InterventionType
)
from .coke_cognitive_graph import COKECognitiveGraph, CognitiveState


class ErrorType(Enum):
    """Types of programming errors"""
    SYNTAX_ERROR = "syntax_error"
    LOGIC_ERROR = "logic_error"
    RUNTIME_ERROR = "runtime_error"
    CONCEPTUAL_ERROR = "conceptual_error"
    MISCONCEPTION = "misconception"
    MISSING_KNOWLEDGE = "missing_knowledge"


class RootCauseType(Enum):
    """Root causes of student errors"""
    COGNITIVE_LOAD = "cognitive_load"  # Concept too complex
    MISSING_PREREQUISITE = "missing_prerequisite"  # Don't know basics
    MISCONCEPTION = "misconception"  # Wrong understanding
    ATTENTION_LAPSE = "attention_lapse"  # Careless mistake
    TRANSFER_FAILURE = "transfer_failure"  # Can't apply to new context
    OVERGENERALIZATION = "overgeneralization"  # Applied rule too broadly
    UNDERSPECIFICATION = "underspecification"  # Rule not specific enough


@dataclass
class ErrorPattern:
    """Represents a common student error pattern"""
    id: str
    error_type: ErrorType
    description: str
    code_patterns: List[str]  # Code patterns that indicate this error
    error_messages: List[str]  # Error messages that indicate this error
    concept: str  # Concept this error relates to
    root_cause_ids: List[str]  # IDs of root causes (not types)
    frequency: float  # How common (0.0 to 1.0)


@dataclass
class RootCause:
    """Root cause of an error"""
    id: str
    type: RootCauseType
    description: str
    cognitive_reason: str  # Why this happens cognitively
    indicators: List[str]  # Signs that this is the root cause
    related_misconception: Optional[str] = None  # Linked misconception if any


@dataclass
class ExplanationStrategy:
    """Best explanation strategy for addressing an error/root cause"""
    id: str
    name: str
    target_error: str  # Error pattern this addresses
    target_root_cause: RootCauseType
    explanation_approach: str  # How to explain
    content_template: str  # Template for explanation
    examples: List[str]  # Example explanations
    effectiveness_score: float  # How effective (0.0 to 1.0)
    cognitive_state: Optional[CognitiveState] = None  # Best for this cognitive state
    prerequisites: List[str] = field(default_factory=list)


class ErrorExplanationMapper:
    """
    Maps student errors to root causes and best explanations
    
    Structure:
    Error → Root Causes → Explanation Strategies
    """
    
    def __init__(self, config: Dict, pedagogical_builder=None, coke_graph=None):
        """
        Args:
            config: Configuration dictionary
            pedagogical_builder: PedagogicalKGBuilder instance
            coke_graph: COKECognitiveGraph instance
        """
        self.config = config
        self.pedagogical_builder = pedagogical_builder
        self.coke_graph = coke_graph
        
        # Data directories
        self.data_dir = Path(config.get('pedagogical_kg', {}).get('data_dir', 'data/pedagogical_kg'))
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # Error patterns database
        self.error_patterns: Dict[str, ErrorPattern] = {}
        
        # Root causes database
        self.root_causes: Dict[str, RootCause] = {}
        
        # Explanation strategies database
        self.explanation_strategies: Dict[str, ExplanationStrategy] = {}
        
        # Error → Root Cause → Strategy mappings
        self.error_to_root_cause: Dict[str, List[str]] = {}
        self.root_cause_to_strategy: Dict[str, List[str]] = {}
        
        # Load or initialize
        self._load_or_initialize()
    
    def _load_or_initialize(self):
        """Load existing data or initialize with defaults"""
        errors_file = self.data_dir / "error_patterns.json"
        root_causes_file = self.data_dir / "root_causes.json"
        strategies_file = self.data_dir / "explanation_strategies.json"
        
        if errors_file.exists() and root_causes_file.exists() and strategies_file.exists():
            self._load_from_files()
        else:
            self._initialize_default_mappings()
            self._save_to_files()
    
    def _initialize_default_mappings(self):
        """Initialize with default error-to-explanation mappings"""
        
        # ===== ROOT CAUSES =====
        root_causes_data = [
            {
                "id": "rc_missing_base_case",
                "type": "missing_prerequisite",
                "description": "Student doesn't understand that recursion needs a base case",
                "cognitive_reason": "Student hasn't learned the fundamental rule that recursive functions must have a stopping condition",
                "indicators": ["infinite recursion", "RecursionError", "no if statement before recursive call"],
                "related_misconception": "mc_recursion_no_base_case"
            },
            {
                "id": "rc_cognitive_overload",
                "type": "cognitive_load",
                "description": "Concept is too complex for student's current level",
                "cognitive_reason": "Student's working memory is overloaded - too many concepts at once",
                "indicators": ["multiple errors", "confused code structure", "trying to use advanced concepts"],
                "related_misconception": None
            },
            {
                "id": "rc_scope_confusion",
                "type": "misconception",
                "description": "Student confuses local vs global variable scope",
                "cognitive_reason": "Student has incorrect mental model of how variable scope works",
                "indicators": ["UnboundLocalError", "variable used before assignment", "expecting global modification"],
                "related_misconception": "mc_variable_scope"
            },
            {
                "id": "rc_off_by_one_thinking",
                "type": "misconception",
                "description": "Student has off-by-one errors in loop bounds",
                "cognitive_reason": "Student doesn't understand boundary conditions - edge cases",
                "indicators": ["IndexError", "loop runs one too many/few times", "range(len(list)) issues"],
                "related_misconception": "mc_off_by_one"
            },
            {
                "id": "rc_transfer_failure",
                "type": "transfer_failure",
                "description": "Student can't apply concept to new context",
                "cognitive_reason": "Student learned concept in one context but can't generalize",
                "indicators": ["works in example but not in problem", "can't adapt solution"],
                "related_misconception": None
            }
        ]
        
        for rc_data in root_causes_data:
            rc = RootCause(
                id=rc_data["id"],
                type=RootCauseType(rc_data["type"]),
                description=rc_data["description"],
                cognitive_reason=rc_data["cognitive_reason"],
                indicators=rc_data["indicators"],
                related_misconception=rc_data.get("related_misconception")
            )
            self.root_causes[rc.id] = rc
        
        # ===== ERROR PATTERNS =====
        error_patterns_data = [
            {
                "id": "err_recursion_no_base_case",
                "error_type": "runtime_error",
                "description": "Recursion without base case causing infinite loop",
                "code_patterns": [
                    "def.*recursive.*:\s*return.*recursive",
                    "def.*\(.*\):\s*return.*\(.*-.*1\)",  # Missing if before recursive call
                ],
                "error_messages": [
                    "RecursionError",
                    "maximum recursion depth exceeded",
                    "stack overflow"
                ],
                "concept": "recursion",
                "root_cause_ids": ["rc_missing_base_case"],
                "frequency": 0.7
            },
            {
                "id": "err_variable_scope",
                "error_type": "runtime_error",
                "description": "Variable scope confusion",
                "code_patterns": [
                    "global.*=.*\n.*=.*global",  # Trying to modify global
                    "def.*:\s*.*=.*\n\s*.*=.*",  # Using before assignment
                ],
                "error_messages": [
                    "UnboundLocalError",
                    "variable.*before assignment",
                    "name.*not defined"
                ],
                "concept": "variable_scope",
                "root_cause_ids": ["rc_scope_confusion"],
                "frequency": 0.6
            },
            {
                "id": "err_off_by_one",
                "error_type": "logic_error",
                "description": "Off-by-one errors in loops",
                "code_patterns": [
                    "range\(len\(.*\)\)",  # Should be len-1 sometimes
                    "for.*in range\(.*\):\s*.*\[.*\+.*1\]",  # Index out of bounds
                ],
                "error_messages": [
                    "IndexError",
                    "list index out of range",
                    "string index out of range"
                ],
                "concept": "loops",
                "root_cause_ids": ["rc_off_by_one_thinking"],
                "frequency": 0.8
            },
            {
                "id": "err_too_complex",
                "error_type": "conceptual_error",
                "description": "Code is too complex for student's level",
                "code_patterns": [
                    ".*\n.*\n.*\n.*\n.*\n.*\n.*",  # Too many lines
                    "def.*def.*def.*def",  # Too many nested functions
                ],
                "error_messages": [
                    "multiple errors",
                    "too complex"
                ],
                "concept": "general_programming",
                "root_cause_ids": ["rc_cognitive_overload"],
                "frequency": 0.5
            }
        ]
        
        for err_data in error_patterns_data:
            err = ErrorPattern(
                id=err_data["id"],
                error_type=ErrorType(err_data["error_type"]),
                description=err_data["description"],
                code_patterns=err_data["code_patterns"],
                error_messages=err_data["error_messages"],
                concept=err_data["concept"],
                root_cause_ids=err_data["root_cause_ids"],
                frequency=err_data["frequency"]
            )
            self.error_patterns[err.id] = err
            self.error_to_root_cause[err.id] = err_data["root_cause_ids"]
        
        # ===== EXPLANATION STRATEGIES =====
        strategies_data = [
            {
                "id": "exp_base_case_analogy",
                "name": "Base Case Analogy",
                "target_error": "err_recursion_no_base_case",
                "target_root_cause": "missing_prerequisite",
                "explanation_approach": "Use analogy to explain base case necessity",
                "content_template": "Think of recursion like climbing stairs. The base case is like reaching the ground floor - you stop there! Without it, you'd fall forever. Your function needs a 'stop condition' - when n reaches 0 or 1, return 1. That's your ground floor!",
                "examples": [
                    "Like a light switch - base case turns recursion OFF",
                    "Like a countdown - base case is when you reach 0"
                ],
                "effectiveness_score": 0.85,
                "cognitive_state": "confused",
                "prerequisites": ["functions", "conditional_statements"]
            },
            {
                "id": "exp_base_case_visual",
                "name": "Base Case Visualization",
                "target_error": "err_recursion_no_base_case",
                "target_root_cause": "missing_prerequisite",
                "explanation_approach": "Show call stack visualization",
                "content_template": "Let's trace what happens: factorial(3) calls factorial(2) calls factorial(1) calls factorial(0) calls factorial(-1)... forever! The base case stops this chain. Add: if n <= 1: return 1",
                "examples": [
                    "Call stack diagram showing infinite calls",
                    "Step-by-step execution trace"
                ],
                "effectiveness_score": 0.80,
                "cognitive_state": "understanding",
                "prerequisites": ["functions"]
            },
            {
                "id": "exp_scope_visualization",
                "name": "Scope Visualization",
                "target_error": "err_variable_scope",
                "target_root_cause": "misconception",
                "explanation_approach": "Visual diagram showing scope boundaries",
                "content_template": "Variables have 'scopes' - like rooms in a house. Local variables live in the function room. Global variables live in the house. You can't change a global from inside a function room without saying 'global variable_name' first!",
                "examples": [
                    "Scope diagram with boxes",
                    "Memory visualization showing local vs global"
                ],
                "effectiveness_score": 0.75,
                "cognitive_state": "confused",
                "prerequisites": ["functions"]
            },
            {
                "id": "exp_boundary_practice",
                "name": "Boundary Case Practice",
                "target_error": "err_off_by_one",
                "target_root_cause": "misconception",
                "explanation_approach": "Practice with boundary cases",
                "content_template": "Off-by-one errors happen at boundaries. Let's practice: For a list of 5 items (indices 0-4), range(5) gives 0,1,2,3,4. That's correct! But if you do range(len(list)+1), you get 0,1,2,3,4,5 - that's one too many! Always check: 'What's the last valid index?'",
                "examples": [
                    "Practice with lists of different sizes",
                    "Trace through boundary cases step-by-step"
                ],
                "effectiveness_score": 0.70,
                "cognitive_state": "understanding",
                "prerequisites": ["loops", "lists"]
            },
            {
                "id": "exp_break_down_complex",
                "name": "Break Down Complexity",
                "target_error": "err_too_complex",
                "target_root_cause": "cognitive_load",
                "explanation_approach": "Simplify and break into smaller parts",
                "content_template": "This is too complex! Let's break it down. First, let's just make it work with one simple case. Once that works, we'll add the next part. Don't try to solve everything at once - one step at a time!",
                "examples": [
                    "Start with simplest version",
                    "Add features incrementally"
                ],
                "effectiveness_score": 0.80,
                "cognitive_state": "frustrated",
                "prerequisites": []
            }
        ]
        
        for strat_data in strategies_data:
            strat = ExplanationStrategy(
                id=strat_data["id"],
                name=strat_data["name"],
                target_error=strat_data["target_error"],
                target_root_cause=RootCauseType(strat_data["target_root_cause"]),
                explanation_approach=strat_data["explanation_approach"],
                content_template=strat_data["content_template"],
                examples=strat_data["examples"],
                effectiveness_score=strat_data["effectiveness_score"],
                cognitive_state=CognitiveState[strat_data.get("cognitive_state", "confused").upper()] if strat_data.get("cognitive_state") else None,
                prerequisites=strat_data.get("prerequisites", [])
            )
            self.explanation_strategies[strat.id] = strat
            
            # Map root cause to strategy
            root_cause_id = None
            for rc_id, rc in self.root_causes.items():
                if rc.type == strat.target_root_cause:
                    root_cause_id = rc_id
                    break
            
            if root_cause_id:
                if root_cause_id not in self.root_cause_to_strategy:
                    self.root_cause_to_strategy[root_cause_id] = []
                self.root_cause_to_strategy[root_cause_id].append(strat.id)
    
    def detect_error(self, code: Optional[str] = None,
                    error_message: Optional[str] = None) -> Optional[ErrorPattern]:
        """
        Detect error pattern from code and error message
        
        Args:
            code: Student's code
            error_message: Error message if any
            
        Returns:
            Detected error pattern or None
        """
        import re
        
        # Check error messages first (more reliable)
        if error_message:
            error_lower = error_message.lower()
            for err in self.error_patterns.values():
                for pattern in err.error_messages:
                    if pattern.lower() in error_lower:
                        return err
        
        # Check code patterns
        if code:
            code_lower = code.lower()
            for err in self.error_patterns.values():
                for pattern in err.code_patterns:
                    try:
                        if re.search(pattern, code_lower, re.IGNORECASE):
                            return err
                    except:
                        continue
        
        return None
    
    def identify_root_causes(self, error_pattern: ErrorPattern,
                            student_data: Optional[Dict] = None) -> List[RootCause]:
        """
        Identify root causes for an error
        
        Args:
            error_pattern: Detected error pattern
            student_data: Additional student context
            
        Returns:
            List of root causes (ordered by likelihood)
        """
        root_cause_ids = self.error_to_root_cause.get(error_pattern.id, [])
        if not root_cause_ids:
            # Use root_cause_ids from error pattern
            root_cause_ids = error_pattern.root_cause_ids
        root_causes = [self.root_causes[rc_id] for rc_id in root_cause_ids if rc_id in self.root_causes]
        
        # If COKE available, use cognitive state to refine
        if self.coke_graph and student_data:
            cognitive_state = self.coke_graph.predict_cognitive_state(student_data)
            
            # Prioritize root causes based on cognitive state
            if cognitive_state == CognitiveState.CONFUSED:
                # More likely to be missing prerequisite or misconception
                root_causes.sort(key=lambda rc: rc.type in [
                    RootCauseType.MISSING_PREREQUISITE,
                    RootCauseType.MISCONCEPTION
                ], reverse=True)
            elif cognitive_state == CognitiveState.FRUSTRATED:
                # More likely to be cognitive overload
                root_causes.sort(key=lambda rc: rc.type == RootCauseType.COGNITIVE_LOAD, reverse=True)
        
        return root_causes
    
    def get_best_explanation(self, error_pattern: ErrorPattern,
                            root_cause: RootCause,
                            student_data: Optional[Dict] = None) -> Optional[ExplanationStrategy]:
        """
        Get best explanation strategy for error and root cause
        
        Args:
            error_pattern: Detected error
            root_cause: Identified root cause
            student_data: Student context (for cognitive state)
            
        Returns:
            Best explanation strategy
        """
        # Get strategies for this root cause
        strategy_ids = self.root_cause_to_strategy.get(root_cause.id, [])
        strategies = [
            self.explanation_strategies[sid]
            for sid in strategy_ids
            if sid in self.explanation_strategies
        ]
        
        if not strategies:
            return None
        
        # Filter by error pattern
        strategies = [s for s in strategies if s.target_error == error_pattern.id]
        
        if not strategies:
            return None
        
        # If COKE available, prioritize by cognitive state
        if self.coke_graph and student_data:
            cognitive_state = self.coke_graph.predict_cognitive_state(student_data)
            
            # Find strategy matching cognitive state
            matching_strategy = next(
                (s for s in strategies if s.cognitive_state == cognitive_state),
                None
            )
            if matching_strategy:
                return matching_strategy
        
        # Otherwise, return most effective
        return max(strategies, key=lambda s: s.effectiveness_score)
    
    def generate_explanation(self, code: Optional[str] = None,
                            error_message: Optional[str] = None,
                            student_data: Optional[Dict] = None) -> Dict:
        """
        Complete pipeline: Error → Root Cause → Best Explanation
        
        Args:
            code: Student's code
            error_message: Error message
            student_data: Student context
            
        Returns:
            Complete explanation with root cause and strategy
        """
        # Step 1: Detect error
        error_pattern = self.detect_error(code, error_message)
        
        if not error_pattern:
            return {
                "error_detected": False,
                "message": "No known error pattern detected"
            }
        
        # Step 2: Identify root causes
        root_causes = self.identify_root_causes(error_pattern, student_data)
        
        if not root_causes:
            return {
                "error_detected": True,
                "error": error_pattern.description,
                "root_causes": [],
                "message": "Error detected but root causes unknown"
            }
        
        # Step 3: Get best explanation for primary root cause
        primary_root_cause = root_causes[0]
        best_strategy = self.get_best_explanation(error_pattern, primary_root_cause, student_data)
        
        # Step 4: Generate explanation
        explanation = {
            "error_detected": True,
            "error": {
                "id": error_pattern.id,
                "type": error_pattern.error_type.value,
                "description": error_pattern.description,
                "concept": error_pattern.concept
            },
            "root_cause": {
                "id": primary_root_cause.id,
                "type": primary_root_cause.type.value,
                "description": primary_root_cause.description,
                "cognitive_reason": primary_root_cause.cognitive_reason,
                "why_student_went_wrong": primary_root_cause.cognitive_reason
            },
            "best_explanation": None,
            "all_root_causes": [
                {
                    "id": rc.id,
                    "type": rc.type.value,
                    "description": rc.description
                }
                for rc in root_causes
            ]
        }
        
        if best_strategy:
            explanation["best_explanation"] = {
                "strategy": best_strategy.name,
                "approach": best_strategy.explanation_approach,
                "explanation": best_strategy.content_template,
                "examples": best_strategy.examples,
                "effectiveness": best_strategy.effectiveness_score,
                "why_this_works": f"This approach addresses the {primary_root_cause.type.value} root cause by {best_strategy.explanation_approach.lower()}"
            }
        
        return explanation
    
    def _load_from_files(self):
        """Load data from JSON files"""
        # Implementation for loading from files
        pass
    
    def _save_to_files(self):
        """Save data to JSON files"""
        # Save error patterns
        errors_data = [
            {
                "id": err.id,
                "error_type": err.error_type.value,
                "description": err.description,
                "code_patterns": err.code_patterns,
                "error_messages": err.error_messages,
                "concept": err.concept,
                "root_cause_ids": err.root_cause_ids,
                "frequency": err.frequency
            }
            for err in self.error_patterns.values()
        ]
        
        with open(self.data_dir / "error_patterns.json", 'w', encoding='utf-8') as f:
            json.dump(errors_data, f, indent=2, ensure_ascii=False)
        
        # Save root causes
        root_causes_data = [
            {
                "id": rc.id,
                "type": rc.type.value,
                "description": rc.description,
                "cognitive_reason": rc.cognitive_reason,
                "indicators": rc.indicators,
                "related_misconception": rc.related_misconception
            }
            for rc in self.root_causes.values()
        ]
        
        with open(self.data_dir / "root_causes.json", 'w', encoding='utf-8') as f:
            json.dump(root_causes_data, f, indent=2, ensure_ascii=False)
        
        # Save explanation strategies
        strategies_data = [
            {
                "id": strat.id,
                "name": strat.name,
                "target_error": strat.target_error,
                "target_root_cause": strat.target_root_cause.value,
                "explanation_approach": strat.explanation_approach,
                "content_template": strat.content_template,
                "examples": strat.examples,
                "effectiveness_score": strat.effectiveness_score,
                "cognitive_state": strat.cognitive_state.value if strat.cognitive_state else None,
                "prerequisites": strat.prerequisites
            }
            for strat in self.explanation_strategies.values()
        ]
        
        with open(self.data_dir / "explanation_strategies.json", 'w', encoding='utf-8') as f:
            json.dump(strategies_data, f, indent=2, ensure_ascii=False)

