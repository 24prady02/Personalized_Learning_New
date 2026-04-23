"""
Test that ALL knowledge graphs are being queried and integrated into responses
"""

import os
import yaml
from pathlib import Path
from src.orchestrator.orchestrator import InterventionOrchestrator
from src.models.hvsae.model import HVSAE
import torch

def main():
    print("=" * 80)
    print("TESTING ALL KNOWLEDGE GRAPHS INTEGRATION")
    print("=" * 80)
    
    # Get Groq API key from environment variable
    groq_api_key = os.getenv('GROQ_API_KEY', '')
    if not groq_api_key:
        print("[ERROR] GROQ_API_KEY environment variable not set!")
        print("[INFO] Please set it using: set GROQ_API_KEY=your_api_key")
        return
    
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
        models['hvsae'] = HVSAE(config)
        print("  [OK] HVSAE initialized")
    except Exception as e:
        print(f"  [WARN] HVSAE failed: {e}")
        models['hvsae'] = None
    
    # Initialize Orchestrator
    print("\n[2] Initializing Orchestrator...")
    orchestrator = InterventionOrchestrator(config, models, use_rl=True, use_hierarchical_rl=False)
    
    # Test session
    print("\n[3] Processing Test Session...")
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
    
    # Check knowledge graphs usage
    print("\n" + "=" * 80)
    print("KNOWLEDGE GRAPHS INTEGRATION CHECK")
    print("=" * 80)
    
    content = result.get('content', {})
    metrics = content.get('metrics', {})
    quantitative = metrics.get('quantitative', {})
    kgs_used = quantitative.get('knowledge_graphs_used', {})
    
    print("\nKnowledge Graphs Status:")
    print(f"  CSE-KG: {'[OK]' if kgs_used.get('cse_kg', False) else '[NOT USED]'}")
    print(f"  Pedagogical KG: {'[OK]' if kgs_used.get('pedagogical_kg', False) else '[NOT USED]'}")
    print(f"  COKE: {'[OK]' if kgs_used.get('coke', False) else '[NOT USED]'}")
    print(f"  DINA: {'[OK]' if kgs_used.get('dina', False) else '[NOT USED]'}")
    print(f"  Nestor: {'[OK]' if kgs_used.get('nestor', False) else '[NOT USED]'}")
    
    # Check if KG info is in analysis
    analysis = content.get('analysis', {})
    adaptive_analysis = content.get('adaptive_analysis', {})
    
    print("\nKnowledge Graph Data in Response:")
    
    # Check CSE-KG
    if adaptive_analysis.get('prerequisites'):
        print(f"  [OK] CSE-KG Prerequisites: {len(adaptive_analysis['prerequisites'])} found")
    else:
        print(f"  [WARN] CSE-KG Prerequisites: Not found")
    
    # Check Pedagogical KG
    if adaptive_analysis.get('knowledge_gaps'):
        print(f"  [OK] Pedagogical KG Knowledge Gaps: {len(adaptive_analysis['knowledge_gaps'])} found")
    else:
        print(f"  [WARN] Pedagogical KG Knowledge Gaps: Not found")
    
    # Check COKE
    cognitive_state = result.get('content', {}).get('cognitive_state_inferred')
    if cognitive_state:
        print(f"  [OK] COKE Cognitive State: {cognitive_state}")
    else:
        print(f"  [WARN] COKE Cognitive State: Not found")
    
    # Check response
    response_text = content.get('text', '')
    print(f"\nResponse Generated: {len(response_text)} characters")
    
    # Check if response mentions knowledge graph concepts
    response_lower = response_text.lower()
    kg_indicators = {
        'CSE-KG': ['prerequisite', 'concept', 'related', 'definition'],
        'Pedagogical KG': ['misconception', 'common mistake', 'learning progression', 'cognitive load'],
        'COKE': ['cognitive', 'mental state', 'understanding', 'confused', 'frustrated']
    }
    
    print("\nKnowledge Graph References in Response:")
    for kg_name, indicators in kg_indicators.items():
        found = sum(1 for ind in indicators if ind in response_lower)
        print(f"  {kg_name}: {found}/{len(indicators)} indicators found")
    
    print("\n" + "=" * 80)
    print("INTEGRATION TEST COMPLETE")
    print("=" * 80)
    
    return result

if __name__ == "__main__":
    result = main()









