"""
Run Test Scenarios and Capture Outputs
Tests the system with different code scenarios and saves results
"""

import os
import json
from datetime import datetime
from typing import Dict, List
from chat_interface_simple import ChatInterface
from test_scenarios import TEST_SCENARIOS, get_all_scenarios

# Get API key
groq_api_key = os.getenv('GROQ_API_KEY')
if not groq_api_key:
    print("[ERROR] GROQ_API_KEY environment variable not set!")
    print("[INFO] Please set it using: set GROQ_API_KEY=your_api_key")
    sys.exit(1)


def run_scenario(chat: ChatInterface, scenario: Dict) -> Dict:
    """Run a single test scenario and capture the output"""
    
    print(f"\n{'='*80}")
    print(f"Running: {scenario['name']} ({scenario['id']})")
    print(f"{'='*80}")
    print(f"Category: {scenario['category']} | Difficulty: {scenario['difficulty']}")
    print(f"Question: {scenario['question']}")
    if scenario['code']:
        print(f"\nCode:\n{scenario['code']}")
    print(f"\nExpected Concepts: {', '.join(scenario['expected_concepts'])}")
    if scenario['expected_errors']:
        print(f"Expected Errors: {', '.join(scenario['expected_errors'])}")
    
    # Set student state if provided
    if 'student_state' in scenario:
        # Update student ID to match scenario
        chat.current_student_id = f"test_{scenario['id']}"
        chat.initialize_student(chat.current_student_id)
    
    # Process the scenario
    try:
        result = chat.process_message(
            scenario['question'],
            code=scenario.get('code')
        )
        
        response = result.get('response', '')
        analysis = result.get('analysis', {})
        state = result.get('state', {})
        
        # Capture output
        output = {
            'scenario_id': scenario['id'],
            'scenario_name': scenario['name'],
            'category': scenario['category'],
            'difficulty': scenario['difficulty'],
            'timestamp': datetime.now().isoformat(),
            'input': {
                'question': scenario['question'],
                'code': scenario.get('code'),
                'student_state': scenario.get('student_state', {})
            },
            'output': {
                'response': response,
                'response_length': len(response),
                'analysis': {
                    'focus': analysis.get('focus'),
                    'emotion': analysis.get('emotion'),
                    'frustration_level': analysis.get('frustration_level'),
                    'engagement_score': analysis.get('engagement_score'),
                    'mastery': analysis.get('mastery'),
                    'intervention': analysis.get('intervention')
                },
                'student_state_after': {
                    'interaction_count': state.get('interaction_count', 0),
                    'mastery': state.get('knowledge_state', {}).get('overall_mastery', 0)
                }
            },
            'expected': {
                'concepts': scenario['expected_concepts'],
                'errors': scenario.get('expected_errors', [])
            }
        }
        
        print(f"\n✅ Response generated ({len(response)} characters)")
        print(f"   Detected Focus: {analysis.get('focus', 'N/A')}")
        print(f"   Detected Emotion: {analysis.get('emotion', 'N/A')}")
        print(f"   Intervention: {analysis.get('intervention', 'N/A')}")
        
        return output
        
    except Exception as e:
        print(f"\n❌ Error processing scenario: {e}")
        import traceback
        traceback.print_exc()
        return {
            'scenario_id': scenario['id'],
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }


def run_all_scenarios(save_output=True, output_dir="test_outputs"):
    """Run all test scenarios and save results"""
    
    print("\n" + "="*80)
    print("🧪 Running All Test Scenarios")
    print("="*80)
    print(f"Total scenarios: {len(TEST_SCENARIOS)}")
    
    # Initialize chat interface
    print("\nInitializing chat interface...")
    chat = ChatInterface(groq_api_key)
    print("✅ Chat interface ready\n")
    
    # Create output directory
    if save_output:
        os.makedirs(output_dir, exist_ok=True)
    
    # Run all scenarios
    results = []
    for i, scenario in enumerate(TEST_SCENARIOS, 1):
        print(f"\n[{i}/{len(TEST_SCENARIOS)}] Processing scenario...")
        result = run_scenario(chat, scenario)
        results.append(result)
        
        # Save individual result
        if save_output:
            output_file = os.path.join(output_dir, f"{scenario['id']}_output.json")
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            print(f"   💾 Saved to: {output_file}")
    
    # Save summary
    if save_output:
        summary = {
            'timestamp': datetime.now().isoformat(),
            'total_scenarios': len(TEST_SCENARIOS),
            'results': results
        }
        summary_file = os.path.join(output_dir, 'all_results_summary.json')
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        print(f"\n💾 Summary saved to: {summary_file}")
    
    print("\n" + "="*80)
    print("✅ All scenarios completed!")
    print("="*80)
    
    return results


def run_specific_scenarios(scenario_ids: List[str], save_output=True, output_dir="test_outputs"):
    """Run specific scenarios by ID"""
    
    print(f"\nRunning {len(scenario_ids)} specific scenarios...")
    
    chat = ChatInterface(groq_api_key)
    
    if save_output:
        os.makedirs(output_dir, exist_ok=True)
    
    results = []
    for scenario_id in scenario_ids:
        scenario = next((s for s in TEST_SCENARIOS if s['id'] == scenario_id), None)
        if scenario:
            result = run_scenario(chat, scenario)
            results.append(result)
            
            if save_output:
                output_file = os.path.join(output_dir, f"{scenario_id}_output.json")
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(result, f, indent=2, ensure_ascii=False)
        else:
            print(f"⚠️ Scenario {scenario_id} not found")
    
    return results


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        # Run specific scenarios
        scenario_ids = sys.argv[1:]
        print(f"Running specific scenarios: {scenario_ids}")
        run_specific_scenarios(scenario_ids)
    else:
        # Run all scenarios
        run_all_scenarios()














