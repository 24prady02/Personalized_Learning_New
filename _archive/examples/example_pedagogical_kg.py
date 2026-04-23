"""
Example: Using the Pedagogical-CS Knowledge Graph

This demonstrates how to use the unified knowledge graph that combines:
- CS domain knowledge (from CSE-KG)
- Cognitive/learning needs (misconceptions, progressions, interventions)
"""

import yaml
from pathlib import Path
from src.knowledge_graph import PedagogicalKGIntegration

# Load configuration
config_path = Path("config.yaml")
if config_path.exists():
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
else:
    print("Warning: config.yaml not found. Using default config.")
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
        }
    }

def main():
    print("=" * 60)
    print("Pedagogical-CS Knowledge Graph Example")
    print("=" * 60)
    
    # Initialize Pedagogical KG
    print("\n[1] Initializing Pedagogical Knowledge Graph...")
    try:
        pedagogical_kg = PedagogicalKGIntegration(config)
        print("[OK] Pedagogical KG initialized successfully!")
    except Exception as e:
        print(f"[ERROR] Error initializing: {e}")
        return
    
    # Example 1: Get complete concept information
    print("\n[2] Getting complete information for 'recursion'...")
    try:
        concept_info = pedagogical_kg.get_concept_full_info("recursion")
        print(f"  Concept: {concept_info['concept']}")
        
        if concept_info.get('pedagogical_data'):
            ped_data = concept_info['pedagogical_data']
            print(f"  Cognitive Load: {ped_data['cognitive_load']['total']}/5")
            print(f"  Difficulty: {ped_data['difficulty_level']}")
            print(f"  Common Misconceptions: {len(ped_data['common_misconceptions'])}")
            print(f"  Recommended Interventions: {len(ped_data['recommended_interventions'])}")
    except Exception as e:
        print(f"  Error: {e}")
    
    # Example 2: Detect misconception from student code
    print("\n[3] Detecting misconception from student code...")
    student_code = """
def factorial(n):
    return n * factorial(n - 1)  # Missing base case!
"""
    error_message = "RecursionError: maximum recursion depth exceeded"
    
    try:
        misconception_info = pedagogical_kg.detect_student_misconception(
            concept="recursion",
            code=student_code,
            error_message=error_message
        )
        
        if misconception_info:
            mc = misconception_info['misconception']
            print(f"  [OK] Detected Misconception: {mc['description']}")
            print(f"    Severity: {mc['severity']}")
            print(f"    Frequency: {mc['frequency']:.1%}")
            print(f"    Recommended Interventions: {len(misconception_info['recommended_interventions'])}")
        else:
            print("  No misconception detected")
    except Exception as e:
        print(f"  Error: {e}")
    
    # Example 3: Get learning path
    print("\n[4] Getting learning path to 'recursion'...")
    current_mastery = {
        "functions": 0.9,
        "conditional_statements": 0.85,
        "recursion_intro": 0.3,
        "base_case": 0.2,
        "recursion": 0.1
    }
    
    try:
        path = pedagogical_kg.get_learning_path(
            target_concept="recursion",
            current_mastery=current_mastery
        )
        
        print(f"  Learning Path ({len(path['path'])} steps):")
        for i, step in enumerate(path['path'], 1):
            status = "[OK]" if step['ready'] else "[->]"
            print(f"    {i}. {status} {step['concept']}: "
                  f"mastery={step['current_mastery']:.2f} "
                  f"(need {step['required_mastery']:.2f}) "
                  f"[{step['estimated_time_hours']:.1f}h]")
        
        print(f"\n  Next concept to learn: {path['next_concept']}")
    except Exception as e:
        print(f"  Error: {e}")
    
    # Example 4: Get recommended interventions
    print("\n[5] Getting recommended interventions for 'recursion'...")
    try:
        interventions = pedagogical_kg.get_interventions_for_struggle(
            concept="recursion",
            struggle_type="missing_base_case"
        )
        
        print(f"  Found {len(interventions)} interventions:")
        for i, intv in enumerate(interventions[:3], 1):  # Show top 3
            print(f"    {i}. {intv['name']} ({intv['type']})")
            print(f"       Effectiveness: {intv['effectiveness']:.2f}")
            print(f"       Usage: {intv['usage_count']} times")
    except Exception as e:
        print(f"  Error: {e}")
    
    # Example 5: Get cognitive load information
    print("\n[6] Getting cognitive load information...")
    try:
        load_info = pedagogical_kg.get_cognitive_load_info("recursion")
        
        if load_info:
            print(f"  Concept: {load_info['concept']}")
            print(f"  Total Cognitive Load: {load_info['total_load']}/5")
            print(f"    - Intrinsic: {load_info['intrinsic_load']}/5")
            print(f"    - Extraneous: {load_info['extraneous_load']}/5")
            print(f"    - Germane: {load_info['germane_load']}/5")
            print(f"  Factors: {', '.join(load_info['factors'])}")
            print(f"  Difficulty: {load_info['difficulty_level']}")
            
            if load_info['total_load'] >= 4:
                print("  [WARN] High cognitive load - consider scaffolding!")
    except Exception as e:
        print(f"  Error: {e}")
    
    print("\n" + "=" * 60)
    print("Example completed!")
    print("=" * 60)

if __name__ == "__main__":
    main()

