"""
Pedagogical Knowledge Graph Builder
Extends CSE-KG 2.0 with cognitive/learning needs data
"""

import json
import pickle
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple
import networkx as nx

from .cse_kg_client import CSEKGClient
from .pedagogical_kg_schema import (
    PedagogicalKGSchema,
    Misconception,
    LearningProgression,
    CognitiveLoad,
    Intervention,
    ConceptPedagogicalData,
    CognitiveLoadLevel,
    DifficultyLevel,
    MisconceptionSeverity,
    InterventionType
)


class PedagogicalKGBuilder:
    """
    Builds a unified Pedagogical-CS Knowledge Graph by extending CSE-KG
    
    Combines:
    1. CS domain knowledge (from CSE-KG)
    2. Cognitive/learning needs (misconceptions, progressions, cognitive load, interventions)
    """
    
    def __init__(self, cse_kg_client: CSEKGClient, config: Dict):
        """
        Args:
            cse_kg_client: CSE-KG client for domain knowledge
            config: Configuration dictionary
        """
        self.cse_kg_client = cse_kg_client
        self.config = config
        
        # Data directories
        self.data_dir = Path(config.get('pedagogical_kg', {}).get('data_dir', 'data/pedagogical_kg'))
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # Load pedagogical data
        self.misconceptions: Dict[str, Misconception] = {}
        self.learning_progressions: Dict[str, LearningProgression] = {}
        self.cognitive_loads: Dict[str, CognitiveLoad] = {}
        self.interventions: Dict[str, Intervention] = {}
        self.concept_pedagogical_data: Dict[str, ConceptPedagogicalData] = {}
        
        # Unified graph (NetworkX)
        self.unified_graph = nx.MultiDiGraph()
        
        # Load existing data
        self._load_pedagogical_data()
        
        # Build unified graph
        self._build_unified_graph()
    
    def _load_pedagogical_data(self):
        """Load pedagogical data from files (learned data takes priority)"""
        # Load misconceptions (learned data takes priority)
        misconceptions_file = self.data_dir / "misconceptions.json"
        if misconceptions_file.exists():
            with open(misconceptions_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, dict):
                    data = list(data.values())
                learned_count = 0
                for item in data:
                    mc = Misconception(
                        id=item['id'],
                        concept=item['concept'],
                        description=item['description'],
                        common_indicators=item.get('common_indicators', []),
                        severity=MisconceptionSeverity(item['severity']),
                        frequency=item.get('frequency', 0.5),
                        related_concepts=item.get('related_concepts', []),
                        correction_strategy=item.get('correction_strategy', '')
                    )
                    self.misconceptions[mc.id] = mc
                    learned_count += 1
                print(f"[PedagogicalKG] Loaded {learned_count} misconceptions from learned data")
        else:
            # Initialize with default misconceptions (fallback)
            print("[PedagogicalKG] No learned misconceptions found, using hardcoded defaults")
            self._initialize_default_misconceptions()
        
        # Load learning progressions
        progressions_file = self.data_dir / "learning_progressions.json"
        if progressions_file.exists():
            with open(progressions_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, dict):
                    data = list(data.values())
                for item in data:
                    prog = LearningProgression(
                        id=item['id'],
                        concept_sequence=item['concept_sequence'],
                        difficulty_levels=[DifficultyLevel(d) for d in item['difficulty_levels']],
                        prerequisites=item.get('prerequisites', {}),
                        estimated_time=item.get('estimated_time', {}),
                        mastery_thresholds=item.get('mastery_thresholds', {})
                    )
                    self.learning_progressions[prog.id] = prog
        else:
            self._initialize_default_progressions()
        
        # Load cognitive loads
        cognitive_loads_file = self.data_dir / "cognitive_loads.json"
        if cognitive_loads_file.exists():
            with open(cognitive_loads_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, dict):
                    data = list(data.values())
                for item in data:
                    cl = CognitiveLoad(
                        concept=item['concept'],
                        intrinsic_load=item.get('intrinsic_load', item.get('intrinsic', 0.5)),
                        extraneous_load=item.get('extraneous_load', item.get('extraneous', 0.3)),
                        germane_load=item.get('germane_load', item.get('germane', 0.4)),
                        total_load=item.get('total_load', item.get('total', 0.0)),
                        factors=item.get('factors', [])
                    )
                    self.cognitive_loads[cl.concept] = cl
        else:
            self._initialize_default_cognitive_loads()
        
        # Load interventions
        interventions_file = self.data_dir / "interventions.json"
        if interventions_file.exists():
            with open(interventions_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, dict):
                    data = list(data.values())
                # Map values in the data file that don't directly match the enum
                _type_alias = {
                    'worked_example': 'example',
                    'socratic':       'scaffolding',
                }
                for item in data:
                    # target_concept(s) may be a single string or a list
                    tc = item.get('target_concept')
                    if tc is None:
                        tc_list = item.get('target_concepts', [])
                        tc = tc_list[0] if tc_list else ''
                    raw_type = item.get('type', 'explanation')
                    try:
                        it_type = InterventionType(raw_type)
                    except ValueError:
                        it_type = InterventionType(_type_alias.get(raw_type, 'explanation'))
                    intervention = Intervention(
                        id=item['id'],
                        name=item['name'],
                        type=it_type,
                        target_concept=tc,
                        target_misconception=item.get('target_misconception'),
                        description=item.get('description', ''),
                        content_template=item.get('content_template', ''),
                        prerequisites=item.get('prerequisites', []),
                        effectiveness_score=item.get('effectiveness_score', 0.5),
                        usage_count=item.get('usage_count', 0)
                    )
                    self.interventions[intervention.id] = intervention
        else:
            self._initialize_default_interventions()
        
        # Build concept pedagogical data
        self._build_concept_pedagogical_data()
    
    def _initialize_default_misconceptions(self):
        """Initialize with common programming misconceptions"""
        default_misconceptions = [
            {
                "id": "mc_recursion_no_base_case",
                "concept": "recursion",
                "description": "Believes recursion doesn't need a base case",
                "common_indicators": [
                    "infinite recursion",
                    "RecursionError",
                    "missing if statement before recursive call"
                ],
                "severity": "critical",
                "frequency": 0.7,
                "related_concepts": ["base_case", "conditional_statements"],
                "correction_strategy": "Explain base case necessity with examples"
            },
            {
                "id": "mc_variable_scope",
                "concept": "variable_scope",
                "description": "Confuses local vs global variable scope",
                "common_indicators": [
                    "UnboundLocalError",
                    "variable used before assignment",
                    "expecting global variable to be modified locally"
                ],
                "severity": "high",
                "frequency": 0.6,
                "related_concepts": ["functions", "namespaces"],
                "correction_strategy": "Show scope visualization and examples"
            },
            {
                "id": "mc_off_by_one",
                "concept": "loops",
                "description": "Off-by-one errors in loop bounds",
                "common_indicators": [
                    "IndexError",
                    "loop runs one too many/few times",
                    "range(len(list)) vs range(len(list)-1)"
                ],
                "severity": "medium",
                "frequency": 0.8,
                "related_concepts": ["arrays", "indexing"],
                "correction_strategy": "Practice with boundary cases"
            },
            {
                "id": "mc_mutation_vs_assignment",
                "concept": "mutability",
                "description": "Confuses mutation with assignment",
                "common_indicators": [
                    "unexpected list modification",
                    "expecting immutable behavior",
                    "reference vs value confusion"
                ],
                "severity": "high",
                "frequency": 0.5,
                "related_concepts": ["lists", "dictionaries", "references"],
                "correction_strategy": "Demonstrate with id() and memory visualization"
            }
        ]
        
        for item in default_misconceptions:
            mc = Misconception(
                id=item['id'],
                concept=item['concept'],
                description=item['description'],
                common_indicators=item['common_indicators'],
                severity=MisconceptionSeverity(item['severity']),
                frequency=item['frequency'],
                related_concepts=item['related_concepts'],
                correction_strategy=item['correction_strategy']
            )
            self.misconceptions[mc.id] = mc
        
        # Save to file
        self._save_misconceptions()
    
    def _initialize_default_progressions(self):
        """Initialize with default learning progressions"""
        default_progressions = [
            {
                "id": "prog_recursion_basics",
                "concept_sequence": [
                    "functions",
                    "conditional_statements",
                    "recursion_intro",
                    "base_case",
                    "recursion"
                ],
                "difficulty_levels": [1, 1, 2, 2, 3],
                "prerequisites": {
                    "recursion_intro": ["functions", "conditional_statements"],
                    "base_case": ["recursion_intro"],
                    "recursion": ["base_case", "recursion_intro"]
                },
                "estimated_time": {
                    "functions": 2.0,
                    "conditional_statements": 1.5,
                    "recursion_intro": 3.0,
                    "base_case": 2.0,
                    "recursion": 4.0
                },
                "mastery_thresholds": {
                    "functions": 0.8,
                    "conditional_statements": 0.8,
                    "recursion_intro": 0.7,
                    "base_case": 0.85,
                    "recursion": 0.8
                }
            }
        ]
        
        for item in default_progressions:
            prog = LearningProgression(
                id=item['id'],
                concept_sequence=item['concept_sequence'],
                difficulty_levels=[DifficultyLevel(d) for d in item['difficulty_levels']],
                prerequisites=item['prerequisites'],
                estimated_time=item['estimated_time'],
                mastery_thresholds=item['mastery_thresholds']
            )
            self.learning_progressions[prog.id] = prog
        
        # Save to file
        self._save_progressions()
    
    def _initialize_default_cognitive_loads(self):
        """Initialize with default cognitive load data"""
        default_loads = [
            {
                "concept": "recursion",
                "intrinsic_load": 5,
                "extraneous_load": 3,
                "germane_load": 4,
                "total_load": 5,
                "factors": ["abstract", "recursive_thinking", "call_stack"]
            },
            {
                "concept": "variables",
                "intrinsic_load": 1,
                "extraneous_load": 1,
                "germane_load": 2,
                "total_load": 1,
                "factors": ["concrete", "direct_assignment"]
            },
            {
                "concept": "loops",
                "intrinsic_load": 3,
                "extraneous_load": 2,
                "germane_load": 3,
                "total_load": 3,
                "factors": ["iteration", "control_flow"]
            },
            {
                "concept": "object_oriented_programming",
                "intrinsic_load": 5,
                "extraneous_load": 4,
                "germane_load": 5,
                "total_load": 5,
                "factors": ["abstraction", "encapsulation", "inheritance", "polymorphism"]
            }
        ]
        
        for item in default_loads:
            cl = CognitiveLoad(
                concept=item['concept'],
                intrinsic_load=item['intrinsic_load'],
                extraneous_load=item['extraneous_load'],
                germane_load=item['germane_load'],
                total_load=item['total_load'],
                factors=item['factors']
            )
            self.cognitive_loads[cl.concept] = cl
        
        # Save to file
        self._save_cognitive_loads()
    
    def _initialize_default_interventions(self):
        """Initialize with default interventions"""
        default_interventions = [
            {
                "id": "int_base_case_example",
                "name": "Base Case Example",
                "type": "example",
                "target_concept": "recursion",
                "target_misconception": "mc_recursion_no_base_case",
                "description": "Show concrete example of base case in recursion",
                "content_template": "Let's look at a recursive function with a base case: {example}",
                "prerequisites": ["functions"],
                "effectiveness_score": 0.8,
                "usage_count": 0
            },
            {
                "id": "int_scope_visualization",
                "name": "Variable Scope Visualization",
                "type": "visualization",
                "target_concept": "variable_scope",
                "target_misconception": "mc_variable_scope",
                "description": "Visual diagram showing local vs global scope",
                "content_template": "Here's how variable scope works: {visualization}",
                "prerequisites": ["functions"],
                "effectiveness_score": 0.75,
                "usage_count": 0
            },
            {
                "id": "int_loop_boundary_practice",
                "name": "Loop Boundary Practice",
                "type": "practice",
                "target_concept": "loops",
                "target_misconception": "mc_off_by_one",
                "description": "Practice problems focusing on loop boundaries",
                "content_template": "Let's practice with boundary cases: {practice_problems}",
                "prerequisites": ["loops"],
                "effectiveness_score": 0.7,
                "usage_count": 0
            }
        ]
        
        for item in default_interventions:
            intervention = Intervention(
                id=item['id'],
                name=item['name'],
                type=InterventionType(item['type']),
                target_concept=item['target_concept'],
                target_misconception=item.get('target_misconception'),
                description=item.get('description', ''),
                content_template=item.get('content_template', ''),
                prerequisites=item.get('prerequisites', []),
                effectiveness_score=item.get('effectiveness_score', 0.5),
                usage_count=item.get('usage_count', 0)
            )
            self.interventions[intervention.id] = intervention
        
        # Save to file
        self._save_interventions()
    
    def _build_concept_pedagogical_data(self):
        """Build ConceptPedagogicalData for each concept"""
        # Get all unique concepts from misconceptions, progressions, and cognitive loads
        all_concepts = set()
        for mc in self.misconceptions.values():
            all_concepts.add(mc.concept)
            all_concepts.update(mc.related_concepts)
        
        for prog in self.learning_progressions.values():
            all_concepts.update(prog.concept_sequence)
        
        all_concepts.update(self.cognitive_loads.keys())
        
        for concept in all_concepts:
            # Get misconceptions for this concept
            concept_misconceptions = [
                mc for mc in self.misconceptions.values()
                if mc.concept == concept
            ]
            
            # Get progressions that include this concept
            concept_progressions = [
                prog for prog in self.learning_progressions.values()
                if concept in prog.concept_sequence
            ]
            
            # Get cognitive load
            cognitive_load = self.cognitive_loads.get(
                concept,
                CognitiveLoad(
                    concept=concept,
                    intrinsic_load=3,
                    extraneous_load=2,
                    germane_load=3,
                    total_load=3,
                    factors=[]
                )
            )
            
            # Get recommended interventions
            recommended_interventions = [
                intv for intv in self.interventions.values()
                if intv.target_concept == concept
            ]
            
            # Determine difficulty level from cognitive load
            if cognitive_load.total_load <= 2:
                difficulty = DifficultyLevel.BEGINNER
            elif cognitive_load.total_load <= 3:
                difficulty = DifficultyLevel.INTERMEDIATE
            elif cognitive_load.total_load <= 4:
                difficulty = DifficultyLevel.ADVANCED
            else:
                difficulty = DifficultyLevel.EXPERT
            
            # Build typical struggles from misconceptions
            typical_struggles = [mc.description for mc in concept_misconceptions]
            
            # Success indicators (placeholder - can be enhanced)
            success_indicators = [
                f"Can explain {concept}",
                f"Can implement {concept} correctly",
                f"Can debug {concept} issues"
            ]
            
            self.concept_pedagogical_data[concept] = ConceptPedagogicalData(
                concept=concept,
                cognitive_load=cognitive_load,
                common_misconceptions=concept_misconceptions,
                learning_progressions=concept_progressions,
                recommended_interventions=recommended_interventions,
                difficulty_level=difficulty,
                typical_struggles=typical_struggles,
                success_indicators=success_indicators
            )
    
    def _build_unified_graph(self):
        """Build unified graph combining CSE-KG and pedagogical data"""
        # Add nodes from CSE-KG concepts
        # (We'll query CSE-KG for concepts as needed)
        
        # Add pedagogical nodes
        for concept, data in self.concept_pedagogical_data.items():
            self.unified_graph.add_node(
                concept,
                type="concept",
                cognitive_load=data.cognitive_load.total_load,
                difficulty=data.difficulty_level.value,
                num_misconceptions=len(data.common_misconceptions),
                num_interventions=len(data.recommended_interventions)
            )
        
        # Add misconception nodes
        for mc_id, mc in self.misconceptions.items():
            self.unified_graph.add_node(
                mc_id,
                type="misconception",
                concept=mc.concept,
                severity=mc.severity.value,
                frequency=mc.frequency
            )
            # Link misconception to concept
            self.unified_graph.add_edge(
                mc.concept,
                mc_id,
                relation="hasMisconception"
            )
        
        # Add intervention nodes
        for intv_id, intv in self.interventions.items():
            self.unified_graph.add_node(
                intv_id,
                type="intervention",
                name=intv.name,
                intervention_type=intv.type.value,
                target_concept=intv.target_concept,
                effectiveness=intv.effectiveness_score
            )
            # Link intervention to concept
            self.unified_graph.add_edge(
                intv.target_concept,
                intv_id,
                relation="recommendsIntervention"
            )
            # Link intervention to misconception if applicable
            if intv.target_misconception:
                self.unified_graph.add_edge(
                    intv_id,
                    intv.target_misconception,
                    relation="addressesMisconception"
                )
        
        # Add progression nodes and edges
        for prog_id, prog in self.learning_progressions.items():
            self.unified_graph.add_node(
                prog_id,
                type="progression",
                num_steps=len(prog.concept_sequence)
            )
            # Add progression edges
            for i in range(len(prog.concept_sequence) - 1):
                current = prog.concept_sequence[i]
                next_concept = prog.concept_sequence[i + 1]
                self.unified_graph.add_edge(
                    current,
                    next_concept,
                    relation="precedesInProgression",
                    progression=prog_id
                )
    
    def get_concept_pedagogical_info(self, concept: str) -> Optional[ConceptPedagogicalData]:
        """Get pedagogical information for a concept"""
        return self.concept_pedagogical_data.get(concept)
    
    def get_misconceptions_for_concept(self, concept: str) -> List[Misconception]:
        """Get all misconceptions for a concept"""
        return [
            mc for mc in self.misconceptions.values()
            if mc.concept == concept
        ]
    
    def get_recommended_interventions(self, concept: str, 
                                     misconception_id: Optional[str] = None) -> List[Intervention]:
        """Get recommended interventions for a concept or misconception"""
        if misconception_id:
            return [
                intv for intv in self.interventions.values()
                if intv.target_misconception == misconception_id
            ]
        else:
            return [
                intv for intv in self.interventions.values()
                if intv.target_concept == concept
            ]
    
    def get_learning_progression(self, target_concept: str) -> Optional[LearningProgression]:
        """Get learning progression that leads to target concept"""
        for prog in self.learning_progressions.values():
            if target_concept in prog.concept_sequence:
                return prog
        return None
    
    def detect_misconception(self, concept: str, code: Optional[str] = None,
                           error_message: Optional[str] = None) -> Optional[Misconception]:
        """Detect if student code/error indicates a misconception"""
        misconceptions = self.get_misconceptions_for_concept(concept)
        
        for mc in misconceptions:
            # Check common indicators
            if code:
                for indicator in mc.common_indicators:
                    if indicator.lower() in code.lower():
                        return mc
            
            if error_message:
                for indicator in mc.common_indicators:
                    if indicator.lower() in error_message.lower():
                        return mc
        
        return None
    
    def learn_cognitive_load_from_session(self, concept: str, session_data: Dict) -> Optional[CognitiveLoad]:
        """
        DYNAMIC LEARNING: Learn cognitive load from student session
        
        Infers cognitive load from:
        - Time stuck (longer = higher load)
        - Attempt count (more attempts = higher load)
        - Error frequency (more errors = higher load)
        
        Args:
            concept: Concept being learned
            session_data: Session data with time_stuck, attempts, errors
            
        Returns:
            Updated or new CognitiveLoad
        """
        if not concept:
            return None
        
        time_stuck = session_data.get('time_stuck', 0)
        attempt_count = len(session_data.get('action_sequence', []))
        has_error = bool(session_data.get('error_message'))
        
        # Infer cognitive load components
        # Intrinsic load: Based on concept complexity (from existing or default)
        existing_load = self.cognitive_loads.get(concept)
        if existing_load:
            intrinsic_load = existing_load.intrinsic_load
        else:
            # Estimate from concept name
            if "recursion" in concept.lower() or "object" in concept.lower():
                intrinsic_load = 5
            elif "loop" in concept.lower() or "array" in concept.lower():
                intrinsic_load = 3
            else:
                intrinsic_load = 2
        
        # Extraneous load: Based on time stuck and errors
        if time_stuck > 300:  # 5 minutes
            extraneous_load = min(5, intrinsic_load + 2)
        elif time_stuck > 120:  # 2 minutes
            extraneous_load = min(5, intrinsic_load + 1)
        elif has_error:
            extraneous_load = min(5, intrinsic_load + 1)
        else:
            extraneous_load = intrinsic_load
        
        # Germane load: Based on engagement (inverse of extraneous)
        germane_load = max(1, 5 - extraneous_load)
        
        # Total load
        total_load = max(intrinsic_load, extraneous_load)
        
        # Update or create cognitive load
        if existing_load:
            # Update with exponential moving average
            alpha = 0.1  # Learning rate
            existing_load.intrinsic_load = int(alpha * intrinsic_load + (1 - alpha) * existing_load.intrinsic_load)
            existing_load.extraneous_load = int(alpha * extraneous_load + (1 - alpha) * existing_load.extraneous_load)
            existing_load.germane_load = int(alpha * germane_load + (1 - alpha) * existing_load.germane_load)
            existing_load.total_load = max(existing_load.intrinsic_load, existing_load.extraneous_load)
            self._save_cognitive_loads()
            return existing_load
        else:
            # Create new cognitive load
            new_load = CognitiveLoad(
                concept=concept,
                intrinsic_load=intrinsic_load,
                extraneous_load=extraneous_load,
                germane_load=germane_load,
                total_load=total_load,
                factors=["learned_from_session"]
            )
            self.cognitive_loads[concept] = new_load
            self._save_cognitive_loads()
            print(f"[PedagogicalKG] Learned cognitive load for: {concept}")
            return new_load
    
    def learn_intervention_effectiveness(self, intervention_id: str, 
                                       success: bool, 
                                       learning_gain: float = 0.0):
        """
        DYNAMIC LEARNING: Update intervention effectiveness from outcomes
        
        Args:
            intervention_id: ID of intervention used
            success: Whether intervention was successful
            learning_gain: Learning gain score (0.0-1.0)
        """
        intervention = self.interventions.get(intervention_id)
        if not intervention:
            # Create new intervention if not found
            intervention = Intervention(
                id=intervention_id,
                name=intervention_id.replace('_', ' ').title(),
                type=InterventionType.EXPLANATION,
                target_concept="general",
                description="Learned from session",
                effectiveness_score=0.5,
                usage_count=0
            )
            self.interventions[intervention_id] = intervention
        
        # Update effectiveness score
        alpha = 0.1  # Learning rate
        if success:
            # Increase effectiveness
            new_score = min(1.0, intervention.effectiveness_score + alpha * (1.0 - intervention.effectiveness_score))
            if learning_gain > 0:
                # Weight by learning gain
                new_score = min(1.0, intervention.effectiveness_score + alpha * learning_gain)
        else:
            # Decrease effectiveness
            new_score = max(0.0, intervention.effectiveness_score - alpha * 0.2)
        
        intervention.effectiveness_score = new_score
        intervention.usage_count = intervention.usage_count + 1
        
        # Save
        self._save_interventions()
        print(f"[PedagogicalKG] Updated intervention {intervention_id}: effectiveness={new_score:.2f}, usage={intervention.usage_count}")
    
    def learn_progression_from_session(self, concept_sequence: List[str], 
                                      student_mastery: Dict[str, float]):
        """
        DYNAMIC LEARNING: Learn learning progression from student mastery sequence
        
        Args:
            concept_sequence: Sequence of concepts student learned
            student_mastery: Mastery levels for each concept
        """
        if len(concept_sequence) < 2:
            return
        
        # Create progression ID
        progression_id = f"prog_{concept_sequence[0]}_to_{concept_sequence[-1]}"
        
        # Check if progression exists
        existing_prog = self.learning_progressions.get(progression_id)
        
        # Extract prerequisites from sequence
        prerequisites = {}
        for i, concept in enumerate(concept_sequence):
            if i > 0:
                prerequisites[concept] = concept_sequence[:i]  # All previous concepts
        
        # Determine difficulty levels from mastery
        difficulty_levels = []
        for concept in concept_sequence:
            mastery_raw = student_mastery.get(concept, 0.5)
            # Ensure mastery is a float
            if isinstance(mastery_raw, dict):
                mastery = float(mastery_raw.get('mastery', mastery_raw.get('value', 0.5)))
            elif isinstance(mastery_raw, list):
                mastery = float(mastery_raw[0]) if len(mastery_raw) > 0 else 0.5
            else:
                mastery = float(mastery_raw) if mastery_raw is not None else 0.5
            # Lower mastery = higher difficulty
            if mastery < 0.3:
                difficulty = 5
            elif mastery < 0.5:
                difficulty = 4
            elif mastery < 0.7:
                difficulty = 3
            elif mastery < 0.85:
                difficulty = 2
            else:
                difficulty = 1
            difficulty_levels.append(difficulty)
        
        # Estimate time from mastery (lower mastery = more time needed)
        estimated_time = {}
        for concept in concept_sequence:
            mastery = student_mastery.get(concept, 0.5)
            # Inverse relationship: lower mastery = more time
            time_hours = 1.0 + (1.0 - mastery) * 4.0
            estimated_time[concept] = time_hours
        
        # Mastery thresholds (from actual mastery achieved)
        mastery_thresholds = {}
        for concept in concept_sequence:
            mastery = student_mastery.get(concept, 0.7)
            # Use actual mastery as threshold
            mastery_thresholds[concept] = max(0.7, mastery)
        
        if existing_prog:
            # Update existing progression
            # Merge sequences (keep longer one)
            if len(concept_sequence) > len(existing_prog.concept_sequence):
                existing_prog.concept_sequence = concept_sequence
                existing_prog.difficulty_levels = difficulty_levels
                existing_prog.prerequisites = prerequisites
                existing_prog.estimated_time = estimated_time
                existing_prog.mastery_thresholds = mastery_thresholds
                self._save_progressions()
                print(f"[PedagogicalKG] Updated progression: {progression_id}")
        else:
            # Create new progression
            new_prog = LearningProgression(
                id=progression_id,
                concept_sequence=concept_sequence,
                difficulty_levels=[DifficultyLevel(d) for d in difficulty_levels],
                prerequisites=prerequisites,
                estimated_time=estimated_time,
                mastery_thresholds=mastery_thresholds
            )
            self.learning_progressions[progression_id] = new_prog
            self._save_progressions()
            print(f"[PedagogicalKG] Learned new progression: {progression_id}")
    
    def learn_from_session(self, code: Optional[str] = None, 
                          error_message: Optional[str] = None,
                          concept: Optional[str] = None) -> Optional[Misconception]:
        """
        DYNAMIC LEARNING: Learn new misconception from student session
        
        Args:
            code: Student's buggy code
            error_message: Error message
            concept: Detected concept (if known)
            
        Returns:
            Newly learned or updated misconception
        """
        if not error_message and not code:
            return None
        
        # Extract concept from error if not provided
        if not concept:
            if error_message:
                if "RecursionError" in error_message:
                    concept = "recursion"
                elif "IndexError" in error_message:
                    concept = "arrays"
                elif "UnboundLocalError" in error_message:
                    concept = "variable_scope"
                elif "TypeError" in error_message:
                    concept = "type_system"
                elif "AttributeError" in error_message:
                    concept = "object_oriented"
                elif "KeyError" in error_message:
                    concept = "dictionaries"
                else:
                    concept = "general"
            else:
                concept = "general"
        
        # Extract error type
        error_type = None
        if error_message:
            for err in ["RecursionError", "IndexError", "UnboundLocalError", 
                       "TypeError", "AttributeError", "KeyError", "ValueError"]:
                if err in error_message:
                    error_type = err
                    break
        
        # Check if misconception already exists
        existing_mc = None
        for mc in self.misconceptions.values():
            if mc.concept == concept and error_type:
                # Check if error type matches
                if error_type in str(mc.common_indicators):
                    existing_mc = mc
                    break
        
        if existing_mc:
            # Update existing misconception (increment evidence)
            existing_mc.frequency = min(1.0, existing_mc.frequency + 0.01)  # Small increment
            # Add new indicator if found
            if error_type and error_type not in existing_mc.common_indicators:
                existing_mc.common_indicators.append(error_type)
            self._save_misconceptions()
            return existing_mc
        else:
            # Learn new misconception
            mc_id = f"mc_{concept}_{error_type.lower() if error_type else 'general'}"
            
            # Extract indicators from code/error
            indicators = []
            if error_type:
                indicators.append(error_type)
            if code:
                if "def" in code and "return" not in code:
                    indicators.append("missing return")
                if "recursive" in code.lower() and "if" not in code:
                    indicators.append("missing base case")
            
            # Determine severity
            if error_type in ["RecursionError", "IndexError"]:
                severity = MisconceptionSeverity.HIGH
            else:
                severity = MisconceptionSeverity.MEDIUM
            
            new_mc = Misconception(
                id=mc_id,
                concept=concept,
                description=f"Common {concept} misconception - {error_type or 'code error'}",
                common_indicators=indicators,
                severity=severity,
                frequency=0.1,  # Start with low frequency, will increase with more evidence
                related_concepts=self._get_related_concepts(concept),
                correction_strategy=self._generate_correction_strategy(concept, error_type)
            )
            
            self.misconceptions[mc_id] = new_mc
            self._save_misconceptions()
            
            print(f"[PedagogicalKG] Learned new misconception: {mc_id} from session")
            return new_mc
    
    def _get_related_concepts(self, concept: str) -> List[str]:
        """Get related concepts"""
        concept_map = {
            "recursion": ["base_case", "conditional_statements", "functions"],
            "arrays": ["loops", "indexing", "lists"],
            "variable_scope": ["functions", "namespaces", "global"],
            "loops": ["arrays", "conditionals", "iteration"],
            "type_system": ["variables", "functions", "classes"],
            "object_oriented": ["classes", "inheritance", "methods"],
            "dictionaries": ["data_structures", "key_value_pairs"]
        }
        return concept_map.get(concept, [])
    
    def _generate_correction_strategy(self, concept: str, error_type: Optional[str]) -> str:
        """Generate correction strategy"""
        strategies = {
            "recursion": "Explain base case necessity with examples. Show how recursion needs a stopping condition.",
            "arrays": "Practice with boundary cases. Show how to check array bounds before accessing.",
            "variable_scope": "Show scope visualization and examples. Explain local vs global variables.",
            "loops": "Practice with boundary cases. Show how to correctly set loop bounds.",
            "type_system": "Explain type checking and type conversion. Show examples of type errors.",
            "object_oriented": "Explain object instantiation and method calls. Show attribute access patterns.",
            "dictionaries": "Explain key existence checking. Show how to safely access dictionary values."
        }
        return strategies.get(concept, f"Review {concept} fundamentals and common pitfalls.")
    
    def suggest_learning_path(self, target_concept: str,
                            current_mastery: Dict[str, float]) -> List[str]:
        """Suggest learning path to target concept based on current mastery"""
        progression = self.get_learning_progression(target_concept)
        
        if not progression:
            # Fallback: use CSE-KG prerequisites
            try:
                prereqs = self.cse_kg_client.get_prerequisites(target_concept)
                return list(prereqs) if prereqs else [target_concept]
            except:
                return [target_concept]
        
        # Find where student is in progression
        path = []
        for concept in progression.concept_sequence:
            mastery = current_mastery.get(concept, 0.0)
            threshold = progression.mastery_thresholds.get(concept, 0.7)
            
            if mastery < threshold:
                path.append(concept)
            
            if concept == target_concept:
                break
        
        return path if path else [target_concept]
    
    # Save methods
    def _save_misconceptions(self):
        """Save misconceptions to file"""
        data = [
            {
                "id": mc.id,
                "concept": mc.concept,
                "description": mc.description,
                "common_indicators": mc.common_indicators,
                "severity": mc.severity.value,
                "frequency": mc.frequency,
                "related_concepts": mc.related_concepts,
                "correction_strategy": mc.correction_strategy
            }
            for mc in self.misconceptions.values()
        ]
        with open(self.data_dir / "misconceptions.json", 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def _save_progressions(self):
        """Save learning progressions to file"""
        data = [
            {
                "id": prog.id,
                "concept_sequence": prog.concept_sequence,
                "difficulty_levels": [d.value if hasattr(d, 'value') else d for d in prog.difficulty_levels],
                "prerequisites": prog.prerequisites,
                "estimated_time": prog.estimated_time,
                "mastery_thresholds": prog.mastery_thresholds
            }
            for prog in self.learning_progressions.values()
        ]
        with open(self.data_dir / "learning_progressions.json", 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def _save_cognitive_loads(self):
        """Save cognitive loads to file"""
        data = [
            {
                "concept": cl.concept,
                "intrinsic_load": cl.intrinsic_load,
                "extraneous_load": cl.extraneous_load,
                "germane_load": cl.germane_load,
                "total_load": cl.total_load,
                "factors": cl.factors
            }
            for cl in self.cognitive_loads.values()
        ]
        with open(self.data_dir / "cognitive_loads.json", 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def _save_interventions(self):
        """Save interventions to file"""
        data = [
            {
                "id": intv.id,
                "name": intv.name,
                "type": intv.type.value,
                "target_concept": intv.target_concept,
                "target_misconception": intv.target_misconception,
                "description": intv.description,
                "content_template": intv.content_template,
                "prerequisites": intv.prerequisites,
                "effectiveness_score": intv.effectiveness_score,
                "usage_count": intv.usage_count
            }
            for intv in self.interventions.values()
        ]
        with open(self.data_dir / "interventions.json", 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def save_unified_graph(self, filepath: Optional[Path] = None):
        """Save unified graph to file"""
        if filepath is None:
            filepath = self.data_dir / "unified_graph.pkl"
        
        with open(filepath, 'wb') as f:
            pickle.dump(self.unified_graph, f)
    
    def load_unified_graph(self, filepath: Optional[Path] = None):
        """Load unified graph from file"""
        if filepath is None:
            filepath = self.data_dir / "unified_graph.pkl"
        
        if filepath.exists():
            with open(filepath, 'rb') as f:
                self.unified_graph = pickle.load(f)





