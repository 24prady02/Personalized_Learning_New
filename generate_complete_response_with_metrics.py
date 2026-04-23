"""
Generate Complete Response with All Metrics
Uses integrated system: Knowledge Graphs + HVSAE + Groq + RL
"""

import yaml
import os
import json
from pathlib import Path
from datetime import datetime
from src.orchestrator.orchestrator import InterventionOrchestrator
from src.models.hvsae.model import HVSAE
import torch

def main():
    print("=" * 70)
    print("COMPLETE INTEGRATED SYSTEM - RESPONSE GENERATION")
    print("=" * 70)
    
    # Set Groq API key from environment or config
    groq_api_key = os.getenv('GROQ_API_KEY', '')
    if not groq_api_key:
        print("[WARN] GROQ_API_KEY not set. Set it as environment variable or in config.yaml")
    
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
    
    # Initialize Orchestrator (will initialize all knowledge graphs + Groq)
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
    
    # Save complete results
    output_dir = Path("test_output")
    output_dir.mkdir(exist_ok=True)
    
    output_file = output_dir / f"complete_response_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    # Format result for output
    output_result = {
        "session_id": f"test_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "student_id": session_data["student_id"],
        "timestamp": datetime.now().isoformat(),
        "input": {
            "question": session_data.get("question", ""),
            "code": session_data.get("code", ""),
            "error_message": session_data.get("error_message", ""),
            "conversation": session_data.get("conversation", [])
        },
        "output": {
            "response": result['content'].get('text', ''),
            "response_length": len(result['content'].get('text', '')),
            "analysis": {
                "focus": result['content'].get('strategy', 'general'),
                "emotion": result.get('analysis', {}).get('behavioral', {}).get('emotion', 'engaged'),
                "frustration_level": 0.3,
                "mastery": result['content'].get('metrics', {}).get('quantitative', {}).get('dina_mastery', {}).get('overall_mastery', 0.5) if result['content'].get('metrics') else 0.5
            }
        },
        "metrics": result['content'].get('metrics', {}),
        "intervention": result['intervention'],
        "knowledge_graphs_used": result['content'].get('knowledge_graphs_used', {}),
        "adaptive_analysis": result['content'].get('adaptive_analysis', {})
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_result, f, indent=2, default=str, ensure_ascii=False)
    
    # Display results
    print("\n" + "=" * 70)
    print("RESULTS")
    print("=" * 70)
    
    print(f"\nIntervention Type: {result['intervention'].get('type', 'N/A')}")
    print(f"Priority: {result['intervention'].get('priority', 0):.2f}")
    
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
    
    print(f"\nComplete Response:")
    print("-" * 70)
    print(response_text)
    print("-" * 70)
    
    print(f"\nFull results saved to: {output_file}")
    print("=" * 70)
    
    return output_result

if __name__ == "__main__":
    result = main()

