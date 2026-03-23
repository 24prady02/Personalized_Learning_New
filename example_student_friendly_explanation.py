"""
Example: Student-Friendly Explanation Generator

Shows how complex analysis is converted into clear, understandable explanations
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
    print("Student-Friendly Explanation Generator")
    print("=" * 70)
    
    # Initialize
    print("\n[1] Initializing...")
    try:
        pedagogical_kg = PedagogicalKGIntegration(config)
        print("[OK] Initialized!")
    except Exception as e:
        print(f"[ERROR] {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Example: Confused student with recursion error
    print("\n[2] Generating Student-Friendly Explanation...")
    student_code = """
def factorial(n):
    return n * factorial(n - 1)  # Missing base case!
"""
    error_message = "RecursionError: maximum recursion depth exceeded"
    
    student_conversation = [
        "I don't understand why this isn't working",
        "I keep getting RecursionError",
        "Can you help me? I'm confused"
    ]
    
    student_data = {
        "conversation": student_conversation,
        "code": student_code,
        "error_message": error_message,
        "time_stuck": 60
    }
    
    try:
        explanation = pedagogical_kg.explain_to_student(
            code=student_code,
            error_message=error_message,
            student_data=student_data
        )
        
        print("\n" + "=" * 70)
        print("STUDENT-FRIENDLY EXPLANATION")
        print("=" * 70)
        
        student_exp = explanation.get("student_explanation", {})
        
        print(f"\n{student_exp.get('greeting', '')}")
        print(f"\n{student_exp.get('main_explanation', '')}")
        
        if student_exp.get('analogy'):
            print(f"\nThink of it like this: {student_exp['analogy']}")
        
        if student_exp.get('step_by_step'):
            print("\nHere's how to fix it:")
            for step in student_exp['step_by_step']:
                print(f"  {step}")
        
        if student_exp.get('example'):
            print(f"\nExample:\n{student_exp['example']}")
        
        if student_exp.get('encouragement'):
            print(f"\n{student_exp['encouragement']}")
        
        if student_exp.get('next_steps'):
            print("\nWhat to do next:")
            for step in student_exp['next_steps']:
                print(f"  • {step}")
        
        print("\n" + "=" * 70)
        print("FULL EXPLANATION (Ready to send to student):")
        print("=" * 70)
        print(explanation.get("full_response", ""))
        
    except Exception as e:
        print(f"[ERROR] {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 70)
    print("The system converts complex analysis into student-friendly explanations!")
    print("=" * 70)

if __name__ == "__main__":
    main()











