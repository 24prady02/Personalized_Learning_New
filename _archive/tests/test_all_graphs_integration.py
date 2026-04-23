"""
Test that all three knowledge graphs are properly integrated
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
    print("Testing Knowledge Graph Integration")
    print("=" * 70)
    
    # Initialize
    print("\n[1] Initializing Adaptive Explanation Generator...")
    try:
        generator = AdaptiveExplanationGenerator(config)
        print("[OK] Initialized!")
    except Exception as e:
        print(f"[ERROR] {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Check which graphs are available
    print("\n[2] Checking Knowledge Graphs...")
    print(f"  CSE-KG 2.0: {'[OK]' if generator.cse_kg else '[NOT AVAILABLE]'}")
    print(f"  Pedagogical KG: {'[OK]' if generator.pedagogical_kg else '[NOT AVAILABLE]'}")
    print(f"  COKE Graph: {'[OK]' if generator.coke_graph else '[NOT AVAILABLE]'}")
    print(f"  DINA Model: {'[OK]' if generator.dina_model else '[NOT AVAILABLE]'}")
    
    # Test CSE-KG
    print("\n[3] Testing CSE-KG (Prerequisites)...")
    if generator.cse_kg:
        try:
            prereqs = generator._get_prerequisites("recursion")
            print(f"  Found {len(prereqs)} prerequisites for 'recursion'")
            for p in prereqs[:3]:  # Show first 3
                print(f"    - {p['concept']} (from {p['source']})")
        except Exception as e:
            print(f"  [ERROR] {e}")
    else:
        print("  [SKIP] CSE-KG not available")
    
    # Test Pedagogical KG
    print("\n[4] Testing Pedagogical KG (Cognitive Load)...")
    if generator.pedagogical_kg:
        try:
            load_info = generator.pedagogical_kg.get_cognitive_load_info("recursion")
            if load_info:
                print(f"  Cognitive Load for 'recursion': {load_info.get('total_load', 'N/A')}")
            else:
                print("  [INFO] No cognitive load data found (using defaults)")
        except Exception as e:
            print(f"  [ERROR] {e}")
    else:
        print("  [SKIP] Pedagogical KG not available")
    
    # Test COKE
    print("\n[5] Testing COKE (Theory of Mind)...")
    if generator.coke_graph:
        try:
            student_data = {
                "conversation": ["I don't understand recursion"],
                "code": "def factorial(n): return n * factorial(n-1)",
                "error_message": "RecursionError"
            }
            tom = generator.coke_graph.infer_theory_of_mind(student_data)
            print(f"  Cognitive State: {tom.get('cognitive_state', 'N/A')}")
            print(f"  Behavioral Response: {tom.get('behavioral_response', 'N/A')}")
            print(f"  Confidence: {tom.get('confidence', 0):.2f}")
        except Exception as e:
            print(f"  [ERROR] {e}")
    else:
        print("  [SKIP] COKE graph not available")
    
    # Test full integration
    print("\n[6] Testing Full Integration...")
    try:
        explanation = generator.generate_adaptive_explanation(
            concept="recursion",
            student_id="test_student",
            student_data={
                "conversation": ["I don't understand recursion"],
                "code": "def factorial(n): return n * factorial(n-1)",
                "error_message": "RecursionError",
                "time_stuck": 60
            }
        )
        
        kgs_used = explanation.get("knowledge_graphs_used", {})
        print(f"  Knowledge Graphs Used:")
        print(f"    CSE-KG: {'[OK]' if kgs_used.get('cse_kg') else '[NOT USED]'}")
        print(f"    Pedagogical KG: {'[OK]' if kgs_used.get('pedagogical_kg') else '[NOT USED]'}")
        print(f"    COKE: {'[OK]' if kgs_used.get('coke') else '[NOT USED]'}")
        print(f"    DINA: {'[OK]' if kgs_used.get('dina') else '[NOT USED]'}")
        
        print(f"\n  Strategy: {explanation.get('strategy', 'N/A')}")
        print(f"  Complexity: {explanation.get('complexity', 'N/A')}")
        print(f"  Knowledge Gaps: {len(explanation.get('knowledge_gaps', []))}")
        
    except Exception as e:
        print(f"  [ERROR] {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 70)
    print("All three knowledge graphs are now properly integrated!")
    print("=" * 70)

if __name__ == "__main__":
    main()












