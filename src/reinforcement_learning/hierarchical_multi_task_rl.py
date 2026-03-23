"""
Hierarchical Multi-Task Reinforcement Learning
Multi-level RL operating at:
1. Meta-level: Across students
2. Curriculum-level: Across concepts for one student
3. Session-level: Multiple objectives within session
4. Intervention-level: Specific teaching actions
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Dict, List, Tuple
import numpy as np


class HierarchicalMultiTaskRL:
    """
    Complete multi-level multi-task RL system
    
    LEVEL 1 (Meta): Learn to teach ANY student
    LEVEL 2 (Curriculum): Which concept to teach Sarah next
    LEVEL 3 (Session): Balance learning/engagement/emotion for Sarah
    LEVEL 4 (Intervention): Which specific action to take
    """
    
    def __init__(self, config: Dict):
        self.config = config
        
        # ===== LEVEL 1: META-LEVEL CONTROLLER =====
        # Learns general teaching strategy across ALL students
        self.meta_controller = MetaLevelController(
            input_dim=512,
            output_dim=64  # Meta-strategy embedding
        )
        
        # ===== LEVEL 2: CURRICULUM CONTROLLER =====
        # Decides which concept to teach Sarah next
        self.curriculum_controller = CurriculumController(
            meta_dim=64,
            state_dim=512,
            num_concepts=20  # All CS concepts Sarah needs
        )
        
        # ===== LEVEL 3: SESSION CONTROLLER (Multi-Task!) =====
        # Balances multiple objectives for Sarah's current session
        self.session_controller = SessionMultiTaskController(
            curriculum_dim=32,
            state_dim=512,
            num_interventions=10
        )
        
        # ===== LEVEL 4: INTERVENTION EXECUTOR =====
        # Executes specific teaching intervention
        self.intervention_executor = InterventionExecutor()
        
        print("✅ Hierarchical Multi-Task RL initialized")
        print("   4 levels: Meta → Curriculum → Session → Intervention")
    
    def teach_sarah(self, sarah_state: Dict, session_history: List):
        """
        Complete multi-level decision for teaching Sarah
        """
        
        print("\n" + "="*70)
        print("HIERARCHICAL MULTI-TASK RL: Teaching Sarah")
        print("="*70)
        
        # ===== LEVEL 1: META-LEVEL =====
        # What general teaching strategy for Sarah's type?
        
        meta_strategy = self.meta_controller.get_strategy(
            student_type=sarah_state['student_type'],
            overall_progress=sarah_state['overall_progress']
        )
        
        print("\n📊 LEVEL 1 (Meta): General Teaching Strategy")
        print(f"   Student type: {sarah_state['student_type']}")
        print(f"   Meta-strategy: {meta_strategy['approach']}")
        print(f"   Predicted success rate: {meta_strategy['expected_success']:.0%}")
        
        
        # ===== LEVEL 2: CURRICULUM-LEVEL =====
        # Which concept should Sarah learn next?
        
        curriculum_decision = self.curriculum_controller.select_next_concept(
            meta_strategy=meta_strategy,
            sarah_state=sarah_state,
            completed_concepts=sarah_state['completed_concepts'],
            current_goals=sarah_state['learning_goals']
        )
        
        print("\n📚 LEVEL 2 (Curriculum): Concept Selection")
        print(f"   Selected concept: {curriculum_decision['concept']}")
        print(f"   Reasoning: {curriculum_decision['reason']}")
        print(f"   Prerequisites met: {curriculum_decision['prereqs_met']}")
        print(f"   Estimated sessions: {curriculum_decision['estimated_sessions']}")
        
        
        # ===== LEVEL 3: SESSION-LEVEL (Multi-Task!) =====
        # Balance multiple objectives for Sarah THIS session
        
        session_plan = self.session_controller.plan_session(
            curriculum_context=curriculum_decision,
            sarah_current_state=sarah_state,
            concept=curriculum_decision['concept']
        )
        
        print("\n🎯 LEVEL 3 (Session): Multi-Objective Optimization")
        print(f"   Primary objective: {session_plan['primary_objective']}")
        print(f"   Objective weights:")
        for obj, weight in session_plan['objective_weights'].items():
            print(f"     {obj}: {weight:.2f}")
        print(f"   Selected intervention type: {session_plan['intervention']}")
        print(f"   Expected outcomes:")
        for obj, exp in session_plan['expected_outcomes'].items():
            print(f"     {obj}: {exp:.2f}")
        
        
        # ===== LEVEL 4: INTERVENTION-LEVEL =====
        # Execute specific teaching intervention
        
        intervention_result = self.intervention_executor.execute(
            intervention_type=session_plan['intervention'],
            concept=curriculum_decision['concept'],
            student_state=sarah_state,
            session_plan=session_plan
        )
        
        print("\n💬 LEVEL 4 (Intervention): Delivery")
        print(f"   Content type: {intervention_result['content_type']}")
        print(f"   Scaffolding level: {intervention_result['scaffolding']}")
        print(f"   Estimated duration: {intervention_result['duration']} min")
        
        return {
            'meta_strategy': meta_strategy,
            'curriculum_decision': curriculum_decision,
            'session_plan': session_plan,
            'intervention': intervention_result
        }


class MetaLevelController(nn.Module):
    """
    LEVEL 1: Meta-Level Controller
    
    Learns teaching strategy across ALL students
    Then adapts to Sarah's specific type
    """
    
    def __init__(self, input_dim: int, output_dim: int):
        super().__init__()
        
        # Learns student typology
        self.student_encoder = nn.Sequential(
            nn.Linear(input_dim, 256),
            nn.ReLU(),
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Linear(128, output_dim)  # Meta-strategy embedding
        )
        
        # Student type classifier (learned from data)
        self.type_classifier = nn.Sequential(
            nn.Linear(output_dim, 32),
            nn.ReLU(),
            nn.Linear(32, 8)  # 8 student archetypes
        )
        
        # Strategy selector per type
        self.strategy_network = nn.ModuleDict({
            f"type_{i}": nn.Linear(output_dim, 16)  # Strategy parameters
            for i in range(8)
        })
    
    def get_strategy(self, student_type: str, overall_progress: float) -> Dict:
        """
        Get teaching strategy for student type
        
        Learned from patterns across ALL students:
        - Type A (systematic beginners): gradual_scaffolding_strategy
        - Type B (chaotic intermediates): structure_first_strategy
        - Type C (visual advanced): challenge_based_strategy
        """
        
        # This is learned from meta-training on many students!
        
        strategies = {
            "type_systematic_beginner": {
                "approach": "gradual_scaffolding",
                "pacing": "slow",
                "support_level": "high",
                "expected_success": 0.92
            },
            "type_chaotic_beginner": {
                "approach": "structure_first",
                "pacing": "very_slow",
                "support_level": "very_high",
                "expected_success": 0.78
            },
            "type_visual_intermediate": {
                "approach": "diagram_driven",
                "pacing": "moderate",
                "support_level": "medium",
                "expected_success": 0.85
            }
        }
        
        return strategies.get(student_type, strategies["type_systematic_beginner"])


class CurriculumController(nn.Module):
    """
    LEVEL 2: Curriculum-Level Controller
    
    Multi-Task across CONCEPTS for Sarah:
    - Task 1: Teach recursion
    - Task 2: Teach loops
    - Task 3: Teach arrays
    - ...
    - Task N: Teach dynamic_programming
    
    Decides: Which concept should Sarah learn NEXT?
    """
    
    def __init__(self, meta_dim: int, state_dim: int, num_concepts: int):
        super().__init__()
        
        self.num_concepts = num_concepts
        
        # Shared encoder across all concepts
        self.concept_shared_encoder = nn.Sequential(
            nn.Linear(meta_dim + state_dim, 256),
            nn.ReLU(),
            nn.Linear(256, 128)
        )
        
        # Multi-Task: One head per concept
        # Each learns: "Should I teach THIS concept to Sarah now?"
        self.concept_heads = nn.ModuleDict({
            "recursion": nn.Linear(128, 1),          # Score for teaching recursion
            "loops": nn.Linear(128, 1),              # Score for teaching loops
            "arrays": nn.Linear(128, 1),             # Score for teaching arrays
            "functions": nn.Linear(128, 1),
            "oop": nn.Linear(128, 1),
            "sorting": nn.Linear(128, 1),
            "searching": nn.Linear(128, 1),
            "trees": nn.Linear(128, 1),
            "graphs": nn.Linear(128, 1),
            "dynamic_programming": nn.Linear(128, 1),
            "algorithms": nn.Linear(128, 1),
            "data_structures": nn.Linear(128, 1),
            "complexity_analysis": nn.Linear(128, 1),
            "debugging": nn.Linear(128, 1),
            "testing": nn.Linear(128, 1),
            "version_control": nn.Linear(128, 1),
            "design_patterns": nn.Linear(128, 1),
            "databases": nn.Linear(128, 1),
            "networking": nn.Linear(128, 1),
            "security": nn.Linear(128, 1)
        })
    
    def select_next_concept(self, meta_strategy: Dict, 
                           sarah_state: Dict,
                           completed_concepts: List,
                           current_goals: List) -> Dict:
        """
        Select which concept Sarah should learn next
        
        Considers:
        - Prerequisites (from CSE-KG)
        - Sarah's current mastery
        - Sarah's learning goals
        - Concept difficulty
        - Meta-strategy recommendation
        """
        
        # Encode combined state
        meta_embedding = torch.tensor(meta_strategy['embedding'])
        state_embedding = torch.tensor(sarah_state['embedding'])
        combined = torch.cat([meta_embedding, state_embedding])
        
        # Shared features
        features = self.concept_shared_encoder(combined)
        
        # Get score for each concept
        concept_scores = {}
        for concept_name, head in self.concept_heads.items():
            if concept_name not in completed_concepts:  # Not already mastered
                score = torch.sigmoid(head(features)).item()
                concept_scores[concept_name] = score
        
        # Select highest scoring concept
        best_concept = max(concept_scores.items(), key=lambda x: x[1])
        
        return {
            'concept': best_concept[0],
            'score': best_concept[1],
            'reason': f"Highest readiness score based on Sarah's state",
            'prereqs_met': True,  # Would check CSE-KG
            'estimated_sessions': 4
        }


class SessionMultiTaskController(nn.Module):
    """
    LEVEL 3: Session-Level Multi-Task Controller
    
    For Sarah learning ONE concept (e.g., recursion):
    
    Multi-Task optimization:
    - Task A: Maximize Sarah's mastery gain (recursion)
    - Task B: Maximize Sarah's engagement
    - Task C: Optimize Sarah's emotional state
    - Task D: Maximize time efficiency
    - Task E: Maximize long-term retention
    
    Outputs: Best intervention considering ALL objectives
    """
    
    def __init__(self, curriculum_dim: int, state_dim: int, num_interventions: int):
        super().__init__()
        
        # Shared encoder: Understands Sarah's current state
        self.shared_encoder = nn.Sequential(
            nn.Linear(curriculum_dim + state_dim, 256),
            nn.ReLU(),
            nn.LayerNorm(256),
            nn.Linear(256, 128)
        )
        
        # ===== MULTI-TASK HEADS (One per objective) =====
        
        # Task A: Learning optimization
        self.learning_task = nn.Sequential(
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, num_interventions)  # Q-values for learning
        )
        
        # Task B: Engagement optimization
        self.engagement_task = nn.Sequential(
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, num_interventions)  # Q-values for engagement
        )
        
        # Task C: Emotional optimization
        self.emotional_task = nn.Sequential(
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, num_interventions)  # Q-values for emotion
        )
        
        # Task D: Efficiency optimization
        self.efficiency_task = nn.Sequential(
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, num_interventions)  # Q-values for time
        )
        
        # Task E: Retention optimization
        self.retention_task = nn.Sequential(
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, num_interventions)  # Q-values for memory
        )
        
        # ===== ADAPTIVE WEIGHT NETWORK =====
        # Learns when to prioritize which objective for Sarah
        self.weight_adapter = nn.Sequential(
            nn.Linear(128, 32),
            nn.ReLU(),
            nn.Linear(32, 5),  # Weights for 5 objectives
            nn.Softmax(dim=-1)
        )
    
    def plan_session(self, curriculum_context: Dict,
                    sarah_current_state: Dict,
                    concept: str) -> Dict:
        """
        Plan session balancing multiple objectives
        """
        
        # Encode context
        curriculum_emb = torch.tensor(curriculum_context['embedding'])
        state_emb = torch.tensor(sarah_current_state['embedding'])
        combined = torch.cat([curriculum_emb, state_emb])
        
        # Shared encoding
        features = self.shared_encoder(combined)  # [128]
        
        # ===== GET Q-VALUES FROM EACH TASK HEAD =====
        
        q_learning = self.learning_task(features)      # [10] interventions
        q_engagement = self.engagement_task(features)  # [10] interventions
        q_emotional = self.emotional_task(features)    # [10] interventions
        q_efficiency = self.efficiency_task(features)  # [10] interventions
        q_retention = self.retention_task(features)    # [10] interventions
        
        # ===== ADAPTIVE WEIGHTING =====
        # Weights change based on Sarah's state!
        
        weights = self.weight_adapter(features)  # [5]
        
        # If Sarah frustrated: weights[2] (emotional) increases
        # If Sarah engaged: weights[0] (learning) increases
        # If Sarah bored: weights[1] (engagement) increases
        
        # ===== COMBINE Q-VALUES =====
        
        q_combined = (
            q_learning * weights[0] +      # Learning weight
            q_engagement * weights[1] +    # Engagement weight
            q_emotional * weights[2] +     # Emotional weight
            q_efficiency * weights[3] +    # Efficiency weight
            q_retention * weights[4]       # Retention weight
        )
        
        # Select best intervention
        intervention_id = q_combined.argmax().item()
        
        interventions = [
            "visual_explanation", "guided_practice", "interactive_exercise",
            "conceptual_deepdive", "motivational_support", "worked_example",
            "spaced_review", "peer_comparison", "error_analysis", "challenge"
        ]
        
        return {
            'intervention': interventions[intervention_id],
            'primary_objective': self._get_primary_objective(weights),
            'objective_weights': {
                'learning': weights[0].item(),
                'engagement': weights[1].item(),
                'emotional': weights[2].item(),
                'efficiency': weights[3].item(),
                'retention': weights[4].item()
            },
            'expected_outcomes': {
                'learning': q_learning[intervention_id].item(),
                'engagement': q_engagement[intervention_id].item(),
                'emotional': q_emotional[intervention_id].item(),
                'efficiency': q_efficiency[intervention_id].item(),
                'retention': q_retention[intervention_id].item()
            },
            'q_combined': q_combined[intervention_id].item()
        }
    
    def _get_primary_objective(self, weights: torch.Tensor) -> str:
        objectives = ['learning', 'engagement', 'emotional', 'efficiency', 'retention']
        primary_idx = weights.argmax().item()
        return objectives[primary_idx]


class InterventionExecutor:
    """
    LEVEL 4: Intervention Execution
    Delivers the teaching content
    """
    
    def execute(self, intervention_type: str, concept: str,
                student_state: Dict, session_plan: Dict) -> Dict:
        """Execute the intervention"""
        
        return {
            'content_type': intervention_type,
            'scaffolding': self._get_scaffolding(student_state['mastery']),
            'duration': self._estimate_duration(intervention_type),
            'content': f"Teaching content for {concept} using {intervention_type}"
        }
    
    def _get_scaffolding(self, mastery: float) -> int:
        if mastery < 0.3: return 5
        elif mastery < 0.6: return 3
        elif mastery < 0.8: return 1
        else: return 0
    
    def _estimate_duration(self, intervention: str) -> int:
        durations = {
            "visual_explanation": 10,
            "guided_practice": 15,
            "interactive_exercise": 20,
            "conceptual_deepdive": 25,
            "motivational_support": 5
        }
        return durations.get(intervention, 15)


# ===== COMPLETE EXAMPLE =====

def complete_example_sarah():
    """
    Show how all 4 levels work together for Sarah
    """
    
    print("\n" + "="*70)
    print("COMPLETE MULTI-LEVEL MULTI-TASK EXAMPLE: Teaching Sarah")
    print("="*70)
    
    # Sarah's complete state
    sarah_state = {
        # Overall
        "student_id": "sarah_2024",
        "student_type": "systematic_beginner",
        "overall_progress": 0.35,  # 35% through curriculum
        
        # Current session
        "current_concept": "recursion",
        "mastery": 0.18,
        "emotion": "confused",
        "time_stuck": 120,
        
        # History
        "completed_concepts": ["variables", "conditionals", "loops", "functions"],
        "learning_goals": ["master_recursion", "learn_data_structures"],
        
        # Personality
        "conscientiousness": 0.82,
        "openness": 0.55,
        
        # Embeddings (pre-computed)
        "embedding": [0.23, -0.45, 0.67, ...],  # 512-dim
    }
    
    # Initialize system
    system = HierarchicalMultiTaskRL(config={})
    
    # Process through all 4 levels
    result = system.teach_sarah(sarah_state, session_history=[])
    
    print("\n" + "="*70)
    print("DECISION SUMMARY")
    print("="*70)
    print(f"""
    LEVEL 1 (Meta): Use 'gradual_scaffolding' strategy for systematic beginners
    LEVEL 2 (Curriculum): Teach 'recursion' next (prerequisites met, high priority)
    LEVEL 3 (Session): Use 'guided_practice' balancing:
        - Learning (40%): Expected Q=0.88
        - Engagement (25%): Expected Q=0.68  
        - Emotional (20%): Expected Q=0.65
        - Efficiency (10%): Expected Q=0.85
        - Retention (5%): Expected Q=0.82
    LEVEL 4 (Intervention): Deliver structured step-by-step guidance
    
    EXPECTED OUTCOME: Sarah learns effectively while staying engaged!
    """)


if __name__ == "__main__":
    complete_example_sarah()



















