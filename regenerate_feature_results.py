"""
Quick script to regenerate results for a specific feature with enhanced metrics
"""
import os
import sys
import json
from datetime import datetime

# Add current directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from chat_interface_simple import ChatInterface
from run_all_10_feature_tests import FEATURE_SCENARIOS, run_feature_scenario

# Get API key
groq_api_key = os.getenv('GROQ_API_KEY')
if not groq_api_key:
    print("[ERROR] GROQ_API_KEY environment variable not set!")
    print("[INFO] Please set it using: set GROQ_API_KEY=your_api_key")
    sys.exit(1)

def regenerate_feature(feature_id: str):
    """Regenerate results for a specific feature"""
    print(f"\n{'='*80}")
    print(f"🔄 Regenerating results for {feature_id}")
    print(f"{'='*80}\n")
    
    # Find the scenario
    scenario = None
    for s in FEATURE_SCENARIOS:
        if s["feature_id"] == feature_id:
            scenario = s
            break
    
    if not scenario:
        print(f"❌ Feature {feature_id} not found!")
        return
    
    # Initialize chat interface
    print("Initializing chat interface...")
    chat = ChatInterface(groq_api_key)
    print("✅ Chat interface ready\n")
    
    # Create feature folder
    feature_folder = os.path.join("feature_test_results", feature_id)
    os.makedirs(feature_folder, exist_ok=True)
    
    # Run scenario
    results = run_feature_scenario(chat, scenario)
    
    # Save JSON results
    json_file = os.path.join(feature_folder, "results.json")
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\n   💾 JSON saved: {json_file}")
    
    # Create comprehensive README.md documentation
    try:
        from run_all_10_feature_tests import create_feature_documentation
        create_feature_documentation(feature_folder, results)
        print(f"   📄 README.md generated: {os.path.join(feature_folder, 'README.md')}")
    except Exception as e:
        print(f"   ⚠️  Could not generate README.md: {e}")
        import traceback
        traceback.print_exc()
    
    # Generate RESULTS.md quantitative analysis
    try:
        from feature_test_results.generate_results_analysis import generate_results_md
        results_md = generate_results_md(feature_folder, results)
        results_md_file = os.path.join(feature_folder, "RESULTS.md")
        with open(results_md_file, 'w', encoding='utf-8') as f:
            f.write(results_md)
        print(f"   📊 RESULTS.md generated: {results_md_file}")
    except Exception as e:
        print(f"   ⚠️  Could not generate RESULTS.md: {e}")
        import traceback
        traceback.print_exc()
    
    print(f"\n✅ Successfully regenerated {feature_id} with enhanced metrics!")
    print(f"   Check: {feature_folder}/RESULTS.md")

if __name__ == "__main__":
    # Regenerate feature_001 first as a test
    if len(sys.argv) > 1:
        feature_id = sys.argv[1]
    else:
        feature_id = "feature_001"
    
    regenerate_feature(feature_id)

