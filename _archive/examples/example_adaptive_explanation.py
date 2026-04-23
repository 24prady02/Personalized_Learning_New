"""
Example: Adaptive Explanation Generator

Shows how explanations adapt to:
- Student's prior knowledge
- Prerequisites
- Learning style
- Cognitive state
"""

import yaml
from pathlib import Path
from src.knowledge_graph import AdaptiveExplanationGenerator

# Load configuration
config_path = Path("config.yaml")
if config_path.exists():
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
else:
    config = {
        'cse_kg': {
            'sparql_endpoint': 'http://w3id.org/cskg/sparql',
            'local_cache': True,
            'cache_dir': 'data/cse_kg_cache',
            'namespace': 'http://cse.ckcest.cn/cskg/',
            'entity_types': ['Method', 'Task', 'Material'],
            'relation_types': ['requiresKnowledge', 'relatedTo']
        },
        'pedagogical_kg': {
            'enabled': True,
            'data_dir': 'data/pedagogical_kg',
            'auto_save': True
        },
        'coke': {
            'enabled': True
        }
    }

def main():
    print("=" * 70)
    print("Adaptive Explanation Generator")
    print("=" * 70)
    
    # Initialize
    print("\n[1] Initializing...")
    try:
        generator = AdaptiveExplanationGenerator(config)
        print("[OK] Initialized!")
    except Exception as e:
        print(f"[ERROR] {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Example 1: Student with strong prerequisites
    print("\n[2] Example: Student with Strong Prerequisites...")
    student_data = {
        "student_id": "student_001",
        "code": "def factorial(n): return n * factorial(n-1)",
        "error_message": "RecursionError",
        "theory_of_mind": {"cognitive_state": "confused"}
    }
    
    try:
        explanation = generator.generate_adaptive_explanation(
            concept="recursion",
            student_id="student_001",
            student_data=student_data
        )
        
        print(f"\nStrategy: {explanation['strategy']}")
        print(f"Complexity: {explanation['complexity']}")
        print(f"\nPrior Knowledge:")
        print(f"  Strong areas: {explanation['prior_knowledge'].get('strong_areas', [])}")
        print(f"  Weak areas: {explanation['prior_knowledge'].get('weak_areas', [])}")
        print(f"\nKnowledge Gaps: {len(explanation['knowledge_gaps'])}")
        for gap in explanation['knowledge_gaps']:
            print(f"  - {gap['concept']}: {gap['mastery']:.0%} mastery ({gap['severity']})")
        print(f"\nLearning Style Adaptation:")
        print(f"  Visual/Verbal: {explanation['learning_style_adaptation'].get('visual_verbal')}")
        print(f"  Order: {explanation['learning_style_adaptation'].get('order', 'N/A')}")
        print(f"\nExplanation:")
        print(explanation['explanation'])
        
    except Exception as e:
        print(f"[ERROR] {e}")
        import traceback
        traceback.print_exc()
    
    # Example 2: Student with knowledge gaps
    print("\n" + "=" * 70)
    print("[3] Example: Student with Knowledge Gaps...")
    print("=" * 70)
    
    # Simulate student with low mastery
    # (In real system, would come from DINA)
    
    print("\n" + "=" * 70)
    print("The system adapts explanations based on:")
    print("  - What student already knows")
    print("  - Missing prerequisites")
    print("  - Learning style preferences")
    print("  - Cognitive state")
    print("  - Cognitive load management")
    print("=" * 70)

if __name__ == "__main__":
    main()












