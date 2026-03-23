"""
Quick-start evaluation script
Run this to begin evaluating your system
"""

import json
import numpy as np
from pathlib import Path
import sys
import yaml

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.orchestrator.orchestrator import InterventionOrchestrator
from src.utils.metrics import MetricsCalculator

def load_config():
    """Load system configuration"""
    config_path = Path("config.yaml")
    if config_path.exists():
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    return {}

def create_sample_test_data():
    """Create sample test data for evaluation"""
    
    test_data = [
        {
            "student_id": "test_student_01",
            "code": "def factorial(n):\n    return n * factorial(n-1)",
            "error_message": "RecursionError: maximum recursion depth exceeded",
            "question": "Why am I getting a recursion error?",
            "action_sequence": ["code_edit", "run_test", "run_test"],
            "time_deltas": [10.0, 2.0, 3.0],
            "time_stuck": 15.0
        },
        {
            "student_id": "test_student_02",
            "code": "arr = [1, 2, 3]\nprint(arr[5])",
            "error_message": "IndexError: list index out of range",
            "question": "Why is my index out of range?",
            "action_sequence": ["code_edit", "compile", "run_test"],
            "time_deltas": [5.0, 1.0, 2.0],
            "time_stuck": 8.0
        },
        {
            "student_id": "test_student_03",
            "code": "student = {\"name\": \"Alice\"}\nprint(student[\"age\"])",
            "error_message": "KeyError: 'age'",
            "question": "Why am I getting a KeyError?",
            "action_sequence": ["code_edit", "run_test", "search_documentation"],
            "time_deltas": [8.0, 2.0, 30.0],
            "time_stuck": 40.0
        }
    ]
    
    return test_data

def evaluate_system_basic(orchestrator, test_data):
    """Basic evaluation of system functionality"""
    
    print("=" * 60)
    print("BASIC SYSTEM EVALUATION")
    print("=" * 60)
    
    results = {
        "total_sessions": len(test_data),
        "successful_processing": 0,
        "failed_processing": 0,
        "average_processing_time": [],
        "components_used": {
            "hvsae": 0,
            "behavioral": 0,
            "coke": 0,
            "nestor": 0,
            "cse_kg": 0,
            "pedagogical_kg": 0
        }
    }
    
    import time
    
    for i, session_data in enumerate(test_data):
        print(f"\nProcessing session {i+1}/{len(test_data)}: {session_data['student_id']}")
        
        try:
            start_time = time.time()
            result = orchestrator.process_session(session_data)
            processing_time = time.time() - start_time
            
            results["successful_processing"] += 1
            results["average_processing_time"].append(processing_time)
            
            # Check which components were used
            system_analysis = result.get('system_analysis', {})
            if system_analysis.get('hvsae_encoding'):
                results["components_used"]["hvsae"] += 1
            if system_analysis.get('behavioral_analysis'):
                results["components_used"]["behavioral"] += 1
            if system_analysis.get('coke_analysis'):
                results["components_used"]["coke"] += 1
            if system_analysis.get('nestor_inference'):
                results["components_used"]["nestor"] += 1
            if system_analysis.get('cse_kg_queries'):
                results["components_used"]["cse_kg"] += 1
            if system_analysis.get('pedagogical_kg'):
                results["components_used"]["pedagogical_kg"] += 1
            
            print(f"  [OK] Processed in {processing_time:.2f}s")
            print(f"  Intervention: {result.get('intervention_type', 'N/A')}")
            
        except Exception as e:
            results["failed_processing"] += 1
            print(f"  [FAIL] Error: {e}")
    
    # Calculate averages
    if results["average_processing_time"]:
        results["average_processing_time"] = np.mean(results["average_processing_time"])
    else:
        results["average_processing_time"] = 0.0
    
    # Print summary
    print("\n" + "=" * 60)
    print("EVALUATION SUMMARY")
    print("=" * 60)
    print(f"Total Sessions: {results['total_sessions']}")
    print(f"Successful: {results['successful_processing']}")
    print(f"Failed: {results['failed_processing']}")
    print(f"Success Rate: {results['successful_processing']/results['total_sessions']*100:.1f}%")
    print(f"Average Processing Time: {results['average_processing_time']:.2f}s")
    print("\nComponents Used:")
    for component, count in results["components_used"].items():
        print(f"  {component}: {count}/{results['total_sessions']}")
    
    return results

def save_results(results, output_path="results/basic_evaluation.json"):
    """Save evaluation results"""
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nResults saved to: {output_file}")

def main():
    """Main evaluation function"""
    
    print("Starting Basic System Evaluation...")
    print("This will test if your system processes sessions correctly.\n")
    
    # Load configuration
    config = load_config()
    
    # Initialize orchestrator (you may need to adjust this based on your setup)
    try:
        # This is a simplified initialization - adjust based on your actual setup
        models = {}  # You'll need to initialize your models here
        orchestrator = InterventionOrchestrator(config, models, use_rl=False)
        print("[OK] Orchestrator initialized")
    except Exception as e:
        print(f"[ERROR] Failed to initialize orchestrator: {e}")
        print("\nNote: You may need to adjust the initialization code based on your setup.")
        return
    
    # Create test data
    test_data = create_sample_test_data()
    print(f"[OK] Created {len(test_data)} test sessions\n")
    
    # Run evaluation
    results = evaluate_system_basic(orchestrator, test_data)
    
    # Save results
    save_results(results)
    
    print("\n" + "=" * 60)
    print("NEXT STEPS:")
    print("=" * 60)
    print("1. Review the results above")
    print("2. Fix any errors that occurred")
    print("3. Implement ground truth annotations (see EVALUATION_AND_VALIDATION_GUIDE.md)")
    print("4. Run full evaluation scripts (misconception detection, knowledge gaps, etc.)")
    print("=" * 60)

if __name__ == "__main__":
    main()

