"""
Regenerate all 10 features with enhanced metrics
"""
import os
import sys
import json
from datetime import datetime

# Add current directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from chat_interface_simple import ChatInterface
from run_all_10_feature_tests import FEATURE_SCENARIOS, run_feature_scenario, create_feature_documentation

# Get API key
groq_api_key = os.getenv('GROQ_API_KEY')
if not groq_api_key:
    print("[ERROR] GROQ_API_KEY environment variable not set!")
    print("[INFO] Please set it using: set GROQ_API_KEY=your_api_key")
    sys.exit(1)

def regenerate_all_features():
    """Regenerate results for all features"""
    print("\n" + "="*80)
    print("🔄 Regenerating ALL 10 Features with Enhanced Metrics")
    print("="*80 + "\n")
    
    # Initialize chat interface
    print("Initializing chat interface...")
    chat = ChatInterface(groq_api_key)
    print("✅ Chat interface ready\n")
    
    # Create main output directory
    main_output_dir = "feature_test_results"
    os.makedirs(main_output_dir, exist_ok=True)
    
    all_results = []
    
    # Process each feature
    for i, scenario in enumerate(FEATURE_SCENARIOS, 1):
        feature_id = scenario["feature_id"]
        feature_name = scenario["feature_name"]
        
        print(f"\n{'='*80}")
        print(f"[{i}/10] Processing: {feature_name} ({feature_id})")
        print(f"{'='*80}")
        
        # Create feature folder
        feature_folder = os.path.join(main_output_dir, feature_id)
        os.makedirs(feature_folder, exist_ok=True)
        
        try:
            # Run scenario
            results = run_feature_scenario(chat, scenario)
            all_results.append(results)
            
            # Save JSON results
            json_file = os.path.join(feature_folder, "results.json")
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            print(f"\n   💾 JSON saved: {json_file}")
            
            # Create documentation
            create_feature_documentation(feature_folder, results)
            
            # Generate RESULTS.md
            try:
                from feature_test_results.generate_results_analysis import generate_results_md
                results_md = generate_results_md(feature_folder, results)
                results_md_file = os.path.join(feature_folder, "RESULTS.md")
                with open(results_md_file, 'w', encoding='utf-8') as f:
                    f.write(results_md)
                print(f"   📊 RESULTS.md generated: {results_md_file}")
            except Exception as e:
                print(f"   ⚠️  Could not generate RESULTS.md: {e}")
            
            print(f"   ✅ Completed {feature_id}")
            
        except Exception as e:
            print(f"   ❌ Error processing {feature_id}: {e}")
            import traceback
            traceback.print_exc()
            continue
    
    # Save overall summary
    summary = {
        "timestamp": datetime.now().isoformat(),
        "total_features_tested": len(FEATURE_SCENARIOS),
        "successful_features": len(all_results),
        "features": [r["feature_id"] for r in all_results]
    }
    
    summary_file = os.path.join(main_output_dir, "regeneration_summary.json")
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    print(f"\n{'='*80}")
    print("✅ Regeneration Complete!")
    print(f"{'='*80}")
    print(f"Successfully regenerated {len(all_results)}/{len(FEATURE_SCENARIOS)} features")
    print(f"Summary saved to: {summary_file}")
    print(f"\nAll features now include:")
    print("  ✅ DINA Mastery Metrics")
    print("  ✅ CodeBERT Analysis")
    print("  ✅ BERT Explanation Quality")
    print("  ✅ Nestor Student Type Detection")
    print("  ✅ Complete RESULTS.md files")

if __name__ == "__main__":
    regenerate_all_features()












