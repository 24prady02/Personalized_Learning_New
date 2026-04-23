"""
Example: Unified Explanation Generator
Combines Theory of Mind (COKE) + Misconceptions (Pedagogical KG)

Two Input Types:
1. Theory of Mind - WHY student went wrong cognitively
2. Misconceptions - WHAT wrong knowledge they have

Output: Best explanation combining both
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
        },
        'coke': {
            'enabled': True
        }
    }

def main():
    print("=" * 70)
    print("Unified Explanation Generator")
    print("Theory of Mind (COKE) + Misconceptions (Pedagogical KG)")
    print("=" * 70)
    
    # Initialize
    print("\n[1] Initializing...")
    try:
        pedagogical_kg = PedagogicalKGIntegration(config)
        print("[OK] Initialized successfully!")
    except Exception as e:
        print(f"[ERROR] {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Example: Recursion error
    print("\n[2] Example: Recursion Error...")
    student_code = """
def factorial(n):
    return n * factorial(n - 1)  # Missing base case!
"""
    error_message = "RecursionError: maximum recursion depth exceeded"
    student_data = {
        'code': student_code,
        'error_message': error_message,
        'time_stuck': 60,
        'action_sequence': ['code_edit', 'run_test', 'run_test', 'run_test'],
        'context': 'encountering_error'
    }
    
    try:
        explanation = pedagogical_kg.generate_unified_explanation(
            code=student_code,
            error_message=error_message,
            student_data=student_data
        )
        
        print("\n--- THEORY OF MIND (COKE) ---")
        tom = explanation.get('theory_of_mind', {})
        if tom:
            print(f"  Cognitive State: {tom.get('cognitive_state', 'unknown')}")
            print(f"  WHY Student Went Wrong: {tom.get('why_student_went_wrong', 'N/A')}")
            print(f"  Predicted Behavior: {tom.get('predicted_behavior', 'N/A')}")
        else:
            print("  [No Theory of Mind analysis available]")
        
        print("\n--- MISCONCEPTION (Pedagogical KG) ---")
        misconception = explanation.get('misconception', {})
        if misconception.get('detected'):
            print(f"  Detected: {misconception.get('description', 'N/A')}")
            print(f"  WHAT Student Believes Wrong: {misconception.get('what_student_believes_wrong', 'N/A')}")
            print(f"  Severity: {misconception.get('severity', 'N/A')}")
            if misconception.get('best_intervention'):
                print(f"  Best Intervention: {misconception['best_intervention'].get('name', 'N/A')}")
        else:
            print("  [No misconception detected]")
        
        print("\n--- UNIFIED EXPLANATION ---")
        unified = explanation.get('unified_explanation', {})
        if unified:
            print("\n  WHY Student Went Wrong:")
            for why in unified.get('why_student_went_wrong', []):
                print(f"    - {why}")
            
            print("\n  WHAT Student Believes Wrong:")
            for what in unified.get('what_student_believes_wrong', []):
                print(f"    - {what}")
            
            print("\n  BEST WAY TO HELP THEM UNDERSTAND:")
            best = unified.get('best_way_to_help_understand', '')
            if best:
                print(f"    {best}")
            else:
                print("    [No explanation generated]")
            
            print("\n  Summary:")
            print(f"    {unified.get('summary', 'N/A')}")
        
    except Exception as e:
        print(f"[ERROR] {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 70)
    print("Example completed!")
    print("=" * 70)

if __name__ == "__main__":
    main()












