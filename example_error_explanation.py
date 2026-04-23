"""
Example: Using Error-to-Explanation Knowledge Graph

Demonstrates how the system maps:
- Student Errors → Root Causes → Best Explanations
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
    print("Error-to-Explanation Knowledge Graph Example")
    print("=" * 70)
    
    # Initialize Pedagogical KG with Error Mapper
    print("\n[1] Initializing Pedagogical KG with Error-to-Explanation Mapper...")
    try:
        pedagogical_kg = PedagogicalKGIntegration(config)
        print("[OK] Pedagogical KG initialized successfully!")
    except Exception as e:
        print(f"[ERROR] Error initializing: {e}")
        return
    
    # Example 1: Recursion error without base case
    print("\n[2] Example: Recursion Error (Missing Base Case)...")
    student_code = """
def factorial(n):
    return n * factorial(n - 1)  # Missing base case!
"""
    error_message = "RecursionError: maximum recursion depth exceeded"
    
    try:
        explanation = pedagogical_kg.explain_student_error(
            code=student_code,
            error_message=error_message,
            student_data={
                'time_stuck': 60,
                'action_sequence': ['code_edit', 'run_test', 'run_test']
            }
        )
        
        if explanation.get('error_detected'):
            print(f"\n  Error Detected: {explanation['error']['description']}")
            print(f"  Concept: {explanation['error']['concept']}")
            
            print(f"\n  WHY STUDENT WENT WRONG:")
            print(f"    Root Cause: {explanation['root_cause']['type']}")
            print(f"    Description: {explanation['root_cause']['description']}")
            print(f"    Cognitive Reason: {explanation['root_cause']['cognitive_reason']}")
            
            if explanation.get('best_explanation'):
                exp = explanation['best_explanation']
                print(f"\n  BEST WAY TO HELP THEM UNDERSTAND:")
                print(f"    Strategy: {exp['strategy']}")
                print(f"    Approach: {exp['approach']}")
                print(f"    Explanation: {exp['explanation']}")
                print(f"    Why This Works: {exp['why_this_works']}")
                print(f"    Effectiveness: {exp['effectiveness']:.0%}")
        else:
            print("  No error pattern detected")
    except Exception as e:
        print(f"  Error: {e}")
    
    # Example 2: Variable scope error
    print("\n[3] Example: Variable Scope Error...")
    student_code = """
x = 10
def modify():
    x = x + 5  # Trying to modify global
    return x
"""
    error_message = "UnboundLocalError: local variable 'x' referenced before assignment"
    
    try:
        explanation = pedagogical_kg.explain_student_error(
            code=student_code,
            error_message=error_message
        )
        
        if explanation.get('error_detected'):
            print(f"\n  Error: {explanation['error']['description']}")
            print(f"\n  WHY: {explanation['root_cause']['cognitive_reason']}")
            
            if explanation.get('best_explanation'):
                exp = explanation['best_explanation']
                print(f"\n  BEST EXPLANATION:")
                print(f"    {exp['explanation']}")
    except Exception as e:
        print(f"  Error: {e}")
    
    # Example 3: Off-by-one error
    print("\n[4] Example: Off-by-One Error...")
    student_code = """
def print_list(items):
    for i in range(len(items) + 1):  # Off by one!
        print(items[i])
"""
    error_message = "IndexError: list index out of range"
    
    try:
        explanation = pedagogical_kg.explain_student_error(
            code=student_code,
            error_message=error_message
        )
        
        if explanation.get('error_detected'):
            print(f"\n  Error: {explanation['error']['description']}")
            print(f"\n  WHY: {explanation['root_cause']['cognitive_reason']}")
            
            if explanation.get('best_explanation'):
                exp = explanation['best_explanation']
                print(f"\n  BEST EXPLANATION:")
                print(f"    {exp['explanation']}")
    except Exception as e:
        print(f"  Error: {e}")
    
    print("\n" + "=" * 70)
    print("Example completed!")
    print("=" * 70)
    print("\nThe system now maps:")
    print("  Student Error → Root Cause (WHY) → Best Explanation (HOW TO HELP)")

if __name__ == "__main__":
    main()












