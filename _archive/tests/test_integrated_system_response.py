"""
Test Complete Integrated System Response Generation
Uses existing orchestrator with all knowledge graphs integrated
"""

import yaml
import os
from pathlib import Path
from src.orchestrator.orchestrator import InterventionOrchestrator
from src.models.hvsae.model import HVSAE
import torch

def main():
    print("=" * 70)
    print("INTEGRATED SYSTEM RESPONSE GENERATION TEST")
    print("=" * 70)
    
    # Load config
    config_path = Path("config.yaml")
    if config_path.exists():
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
    else:
        config = {
            'cse_kg': {
                'sparql_endpoint': 'http://w3id.org/cskg/sparql',
                'local_cache': True,
                'cache_dir': 'data/cse_kg_cache'
            },
            'pedagogical_kg': {'enabled': True},
            'coke': {'enabled': True},
            'hvsae': {},
            'groq': {'api_key': os.getenv('GROQ_API_KEY', '')},
            'reinforcement_learning': {},
            'orchestrator': {
                'priority_factors': {
                    'knowledge_gap': 0.3,
                    'emotional_state': 0.2,
                    'time_stuck': 0.1
                },
                'intervention_threshold': 0.5
            }
        }
    
    # Initialize models
    print("\n[1] Initializing Models...")
    models = {}
    
    # HVSAE
    try:
        if 'hvsae' in config and config['hvsae']:
            models['hvsae'] = HVSAE(config)
            print("  [OK] HVSAE initialized")
        else:
            print("  [WARN] HVSAE config not found")
            models['hvsae'] = None
    except Exception as e:
        print(f"  [WARN] HVSAE failed: {e}")
        import traceback
        traceback.print_exc()
        models['hvsae'] = None
    
    # Initialize Orchestrator (will initialize Adaptive Explainer, Groq, etc.)
    print("\n[2] Initializing Orchestrator...")
    orchestrator = InterventionOrchestrator(config, models, use_rl=True, use_hierarchical_rl=False)
    
    # Test student session
    print("\n[3] Processing Student Session...")
    session_data = {
        "student_id": "test_student_001",
        "code": """def factorial(n):
    return n * factorial(n - 1)  # Missing base case!""",
        "error_message": "RecursionError: maximum recursion depth exceeded",
        "question": "I wrote this recursive function but it's not working. Can you help me?",
        "conversation": [
            "I don't understand why this isn't working",
            "I keep getting RecursionError"
        ],
        "action_sequence": ["code_edit", "run_test", "run_test", "search_documentation"],
        "time_deltas": [15.0, 2.0, 3.0, 45.0],
        "time_stuck": 65.0
    }
    
    # Process session
    result = orchestrator.process_session(session_data)
    
    # Display results
    print("\n" + "=" * 70)
    print("RESULTS")
    print("=" * 70)
    
    print(f"\nIntervention Type: {result['intervention'].get('type', 'N/A')}")
    print(f"Priority: {result['intervention'].get('priority', 0):.2f}")
    print(f"Confidence: {result['intervention'].get('confidence', 0):.2f}")
    
    response_text = result['content'].get('text', '')
    print(f"\nResponse Length: {len(response_text)} characters")
    
    if 'metrics' in result['content']:
        metrics = result['content']['metrics']
        print(f"\nQuantitative Metrics:")
        print(f"  DINA Mastery: {metrics['quantitative']['dina_mastery']['overall_mastery']:.2%}")
        print(f"  CodeBERT Correctness: {metrics['quantitative']['codebert_analysis']['correctness_score']:.2%}")
        print(f"  BERT Quality: {metrics['quantitative']['bert_explanation_quality']['quality_score']:.2f}")
        
        print(f"\nKnowledge Graphs Used:")
        kgs = metrics['quantitative']['knowledge_graphs_used']
        for kg, used in kgs.items():
            print(f"  {kg.upper()}: {'[OK]' if used else '[NOT USED]'}")
    
    print(f"\nResponse Preview:")
    print("-" * 70)
    if response_text:
        print(response_text[:500] + "..." if len(response_text) > 500 else response_text)
    else:
        print("No response generated")
    print("-" * 70)
    
    # Show adaptive analysis if available
    if 'adaptive_analysis' in result['content']:
        adaptive = result['content']['adaptive_analysis']
        print(f"\nAdaptive Analysis:")
        print(f"  Strategy: {adaptive.get('strategy', 'N/A')}")
        print(f"  Complexity: {adaptive.get('complexity', 'N/A')}")
        print(f"  Knowledge Gaps: {len(adaptive.get('knowledge_gaps', []))}")
    
    print("\n" + "=" * 70)
    print("Complete response generated with all metrics!")
    print("=" * 70)
    
    return result

if __name__ == "__main__":
    result = main()

