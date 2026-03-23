"""
Example: Extracting Theory of Mind from Conversation

Demonstrates how the system extracts cognitive states from conversation text
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
    print("Theory of Mind from Conversation Example")
    print("=" * 70)
    
    # Initialize
    print("\n[1] Initializing...")
    try:
        pedagogical_kg = PedagogicalKGIntegration(config)
        print("[OK] Initialized!")
    except Exception as e:
        print(f"[ERROR] {e}")
        return
    
    # Example 1: Confused student conversation
    print("\n[2] Example: Confused Student Conversation...")
    student_conversation = [
        {"role": "student", "content": "I don't understand why my recursion function isn't working"},
        {"role": "student", "content": "I keep getting RecursionError but I don't know what's wrong"},
        {"role": "student", "content": "Can you help me? I'm really confused about this"}
    ]
    
    student_data = {
        "conversation": student_conversation,
        "code": "def factorial(n): return n * factorial(n-1)",
        "error_message": "RecursionError: maximum recursion depth exceeded",
        "time_stuck": 45
    }
    
    try:
        explanation = pedagogical_kg.generate_unified_explanation(
            code=student_data["code"],
            error_message=student_data["error_message"],
            student_data=student_data
        )
        
        tom = explanation.get('theory_of_mind', {})
        print(f"\n  Cognitive State: {tom.get('cognitive_state', 'N/A')}")
        print(f"  WHY: {tom.get('why_student_went_wrong', 'N/A')}")
        print(f"  Extracted from conversation: {tom.get('conversation_analyzed', False)}")
        if tom.get('extracted_from_conversation'):
            print(f"  Conversation text: {tom['extracted_from_conversation']}")
    except Exception as e:
        print(f"  Error: {e}")
        import traceback
        traceback.print_exc()
    
    # Example 2: Frustrated student
    print("\n[3] Example: Frustrated Student Conversation...")
    student_question = "This is so frustrating! I've been trying for hours and nothing works. I hate recursion!"
    
    student_data = {
        "question": student_question,
        "code": "def factorial(n): return n * factorial(n-1)",
        "error_message": "RecursionError",
        "time_stuck": 120
    }
    
    try:
        explanation = pedagogical_kg.generate_unified_explanation(
            code=student_data["code"],
            error_message=student_data["error_message"],
            student_data=student_data
        )
        
        tom = explanation.get('theory_of_mind', {})
        print(f"\n  Cognitive State: {tom.get('cognitive_state', 'N/A')}")
        print(f"  WHY: {tom.get('why_student_went_wrong', 'N/A')}")
    except Exception as e:
        print(f"  Error: {e}")
    
    # Example 3: Understanding student
    print("\n[4] Example: Understanding Student Conversation...")
    student_message = "Oh I see! Now I understand how recursion works. Thanks for explaining!"
    
    student_data = {
        "message": student_message,
        "code": "def factorial(n):\n    if n <= 1: return 1\n    return n * factorial(n-1)",
        "error_message": None,
        "time_stuck": 0
    }
    
    try:
        explanation = pedagogical_kg.generate_unified_explanation(
            code=student_data["code"],
            error_message=student_data.get("error_message"),
            student_data=student_data
        )
        
        tom = explanation.get('theory_of_mind', {})
        print(f"\n  Cognitive State: {tom.get('cognitive_state', 'N/A')}")
        print(f"  WHY: {tom.get('why_student_went_wrong', 'N/A')}")
    except Exception as e:
        print(f"  Error: {e}")
    
    print("\n" + "=" * 70)
    print("The system now extracts Theory of Mind from conversation text!")
    print("=" * 70)

if __name__ == "__main__":
    main()












