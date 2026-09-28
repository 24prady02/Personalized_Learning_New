"""
Pedagogical Knowledge Graph Schema
Combines CS domain knowledge (from CSE-KG) with cognitive/learning needs
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum


class CognitiveLoadLevel(Enum):
    """Cognitive load levels for concepts"""
    VERY_LOW = 1
    LOW = 2
    MODERATE = 3
    HIGH = 4
    VERY_HIGH = 5


class DifficultyLevel(Enum):
    """Difficulty levels for learning progressions"""
    BEGINNER = 1
    INTERMEDIATE = 2
    ADVANCED = 3
    EXPERT = 4


class MisconceptionSeverity(Enum):
    """Severity levels for misconceptions"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class InterventionType(Enum):
    """Types of pedagogical interventions"""
    EXPLANATION = "explanation"
    EXAMPLE = "example"
    ANALOGY = "analogy"
    VISUALIZATION = "visualization"
    PRACTICE = "practice"
    HINT = "hint"
    SCAFFOLDING = "scaffolding"
    CORRECTIVE_FEEDBACK = "corrective_feedback"


@dataclass
class Misconception:
    """Represents a common misconception about a concept"""
    id: str
    concept: str  # Concept this misconception relates to
    description: str  # Description of the misconception
    common_indicators: List[str]  # Code/behavior patterns that indicate this misconception
    severity: MisconceptionSeverity
    frequency: float  # How common (0.0 to 1.0)
    related_concepts: List[str] = field(default_factory=list)
    correction_strategy: str = ""  # How to address this misconception


@dataclass
class LearningProgression:
    """Represents a learning path through concepts"""
    id: str
    concept_sequence: List[str]  # Ordered list of concepts
    difficulty_levels: List[DifficultyLevel]  # Difficulty for each step
    prerequisites: Dict[str, List[str]]  # Prerequisites for each concept in sequence
    estimated_time: Dict[str, float]  # Estimated time to master each step (hours)
    mastery_thresholds: Dict[str, float]  # Mastery level needed to proceed (0.0 to 1.0)


@dataclass
class CognitiveLoad:
    """Cognitive load information for a concept"""
    concept: str
    intrinsic_load: int  # Inherent complexity (1-5)
    extraneous_load: int  # Load from presentation (1-5)
    germane_load: int  # Load from schema construction (1-5)
    total_load: int  # Combined load (1-5)
    factors: List[str]  # Factors contributing to load (e.g., "abstract", "recursive")


@dataclass
class Intervention:
    """Pedagogical intervention for addressing learning needs"""
    id: str
    name: str
    type: InterventionType
    target_concept: str
    target_misconception: Optional[str] = None  # If addressing a specific misconception
    description: str = ""
    content_template: str = ""  # Template for generating intervention content
    prerequisites: List[str] = field(default_factory=list)
    effectiveness_score: float = 0.5  # Historical effectiveness (0.0 to 1.0)
    usage_count: int = 0


@dataclass
class ConceptPedagogicalData:
    """Pedagogical metadata for a CS concept"""
    concept: str
    cognitive_load: CognitiveLoad
    common_misconceptions: List[Misconception]
    learning_progressions: List[LearningProgression]  # Progressions that include this concept
    recommended_interventions: List[Intervention]
    difficulty_level: DifficultyLevel
    typical_struggles: List[str]  # Common struggles students face
    success_indicators: List[str]  # Signs that student understands


class PedagogicalKGSchema:
    """
    Schema definition for Pedagogical-CS Knowledge Graph
    
    Extends CSE-KG with:
    - Misconceptions database
    - Learning progressions
    - Cognitive load information
    - Intervention mappings
    """
    
    # Namespace for pedagogical extensions
    PEDAGOGICAL_NS = "http://pedagogical.kg/cskg/"
    
    # Relation types (extending CSE-KG)
    RELATION_TYPES = {
        # From CSE-KG
        "requiresKnowledge": "Prerequisite relationship",
        "isPrerequisiteOf": "Reverse prerequisite",
        "usesMethod": "Concept uses method",
        "solvesTask": "Method solves task",
        "relatedTo": "Related concepts",
        
        # Pedagogical extensions
        "hasMisconception": "Concept has common misconception",
        "addressesMisconception": "Intervention addresses misconception",
        "hasCognitiveLoad": "Concept has cognitive load",
        "precedesInProgression": "Concept precedes another in learning progression",
        "requiresIntervention": "Concept/struggle requires intervention",
        "recommendsIntervention": "Concept recommends intervention",
        "hasDifficulty": "Concept has difficulty level",
        "typicalStruggle": "Concept has typical student struggle",
    }
    
    @staticmethod
    def get_concept_pedagogical_uri(concept: str) -> str:
        """Get URI for concept in pedagogical KG"""
        return f"{PedagogicalKGSchema.PEDAGOGICAL_NS}concept/{concept}"
    
    @staticmethod
    def get_misconception_uri(misconception_id: str) -> str:
        """Get URI for misconception"""
        return f"{PedagogicalKGSchema.PEDAGOGICAL_NS}misconception/{misconception_id}"
    
    @staticmethod
    def get_intervention_uri(intervention_id: str) -> str:
        """Get URI for intervention"""
        return f"{PedagogicalKGSchema.PEDAGOGICAL_NS}intervention/{intervention_id}"
    
    @staticmethod
    def get_progression_uri(progression_id: str) -> str:
        """Get URI for learning progression"""
        return f"{PedagogicalKGSchema.PEDAGOGICAL_NS}progression/{progression_id}"












