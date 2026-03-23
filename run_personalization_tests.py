"""
Run Personalization Feature Tests
Tests all 10 features with conversation scenarios and generates metrics
"""

import os
import json
from datetime import datetime
from chat_interface_simple import ChatInterface
from personalization_conversation_scenarios import CONVERSATION_SCENARIOS

# Get API key
groq_api_key = os.getenv('GROQ_API_KEY')
if not groq_api_key:
    print("[ERROR] GROQ_API_KEY environment variable not set!")
    print("[INFO] Please set it using: set GROQ_API_KEY=your_api_key")
    sys.exit(1)


def run_conversation_scenario(chat: ChatInterface, scenario: dict) -> dict:
    """Run a complete conversation scenario and capture all responses"""
    
    print(f"\n{'='*80}")
    print(f"Testing: {scenario['feature_name']}")
    print(f"{'='*80}")
    
    # Initialize student
    student_id = scenario['student_profile']['student_id']
    chat.current_student_id = student_id
    chat.initialize_student(student_id)
    
    results = {
        "scenario_id": scenario["scenario_id"],
        "feature_name": scenario["feature_name"],
        "timestamp": datetime.now().isoformat(),
        "conversation_results": []
    }
    
    # Run each turn in the conversation
    for turn_data in scenario["conversation"]:
        turn = turn_data["turn"]
        question = turn_data["question"]
        expected_response = turn_data.get("response", "")
        expected_metrics = turn_data.get("metrics", {})
        
        print(f"\n[Turn {turn}] Question: {question[:60]}...")
        
        # Get code if present
        code = turn_data.get("code")
        
        # Process message
        try:
            result = chat.process_message(question, code=code)
            actual_response = result.get('response', '')
            analysis = result.get('analysis', {})
            
            # Calculate actual metrics
            actual_metrics = calculate_feature_metrics(
                actual_response,
                analysis,
                scenario['feature_name'],
                expected_metrics
            )
            
            turn_result = {
                "turn": turn,
                "input": {
                    "question": question,
                    "code": code
                },
                "output": {
                    "response": actual_response,
                    "response_length": len(actual_response),
                    "analysis": analysis
                },
                "expected_metrics": expected_metrics,
                "actual_metrics": actual_metrics,
                "feature_detection": detect_features_in_response(
                    actual_response,
                    analysis,
                    scenario['feature_name']
                )
            }
            
            results["conversation_results"].append(turn_result)
            
            print(f"   ✅ Response generated ({len(actual_response)} chars)")
            print(f"   📊 Feature score: {actual_metrics.get('feature_score', 0):.2%}")
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
            results["conversation_results"].append({
                "turn": turn,
                "error": str(e)
            })
    
    return results


def detect_features_in_response(response: str, analysis: dict, target_feature: str) -> dict:
    """Detect which personalization features are present in the response"""
    
    response_lower = response.lower()
    features_detected = {}
    
    # Feature 1: Conversation Memory
    memory_indicators = ["remember", "previous", "earlier", "before", "last time", "we discussed"]
    features_detected["conversation_memory"] = any(ind in response_lower for ind in memory_indicators)
    
    # Feature 2: Emotional Intelligence
    emotion_indicators = ["don't worry", "great", "excellent", "frustrated", "understand", "challenging"]
    features_detected["emotional_intelligence"] = any(ind in response_lower for ind in emotion_indicators)
    
    # Feature 3: Visual Learning
    visual_indicators = ["imagine", "visualize", "see", "picture", "diagram", "draw"]
    features_detected["visual_learning"] = any(ind in response_lower for ind in visual_indicators)
    
    # Feature 4: Conceptual Learning
    conceptual_indicators = ["principle", "fundamental", "underlying", "why", "concept", "theory"]
    features_detected["conceptual_learning"] = any(ind in response_lower for ind in conceptual_indicators)
    
    # Feature 5: Personality Adaptation
    personality_indicators = ["normal", "common", "everyone", "many students"]
    features_detected["personality_adaptation"] = any(ind in response_lower for ind in personality_indicators)
    
    # Feature 6: Progress Awareness
    progress_indicators = ["progress", "improved", "mastered", "understand", "learned"]
    features_detected["progress_awareness"] = any(ind in response_lower for ind in progress_indicators)
    
    # Feature 7: Interest Context
    # (Would need student interests from state)
    features_detected["interest_context"] = False  # Placeholder
    
    # Feature 8: Format Preferences
    format_indicators = ["\n-", "\n1.", "\n*", "```"]
    features_detected["format_preferences"] = any(ind in response for ind in format_indicators)
    
    # Feature 9: Error Diagnostic
    error_indicators = ["error", "issue", "problem", "wrong", "fix", "solution"]
    features_detected["error_diagnostic"] = any(ind in response_lower for ind in error_indicators)
    
    # Feature 10: Metacognitive
    metacognitive_indicators = ["think about", "reflect", "strategy", "approach", "method"]
    features_detected["metacognitive_guidance"] = any(ind in response_lower for ind in metacognitive_indicators)
    
    # Check if target feature was detected
    feature_key = target_feature.lower().replace(" ", "_").replace("-", "_")
    target_detected = features_detected.get(feature_key, False)
    
    return {
        "target_feature_detected": target_detected,
        "all_features_detected": features_detected,
        "feature_count": sum(features_detected.values())
    }


def calculate_feature_metrics(response: str, analysis: dict, feature_name: str, expected_metrics: dict) -> dict:
    """Calculate quantitative metrics for the response"""
    
    response_lower = response.lower()
    
    metrics = {
        "response_length": len(response),
        "word_count": len(response.split()),
        "has_code_example": "```" in response or "def " in response,
        "has_explanation": any(word in response_lower for word in ["because", "why", "reason", "explain"]),
        "has_solution": any(word in response_lower for word in ["fix", "solution", "correct", "should"]),
        "has_structure": "\n\n" in response or "\n-" in response or "\n1." in response
    }
    
    # Feature-specific metrics
    if "visual" in feature_name.lower():
        visual_keywords = ["imagine", "visualize", "see", "picture", "diagram", "draw", "visual"]
        metrics["visual_keywords_count"] = sum(1 for kw in visual_keywords if kw in response_lower)
        metrics["visual_score"] = min(metrics["visual_keywords_count"] / 3.0, 1.0)
    
    if "emotional" in feature_name.lower() or "tone" in feature_name.lower():
        encouragement_words = ["great", "excellent", "wonderful", "good", "perfect", "fantastic"]
        metrics["encouragement_count"] = sum(1 for word in encouragement_words if word in response_lower)
        metrics["tone_score"] = min(metrics["encouragement_count"] / 2.0, 1.0)
    
    if "conversation" in feature_name.lower() or "memory" in feature_name.lower():
        memory_words = ["remember", "previous", "earlier", "before", "we discussed", "last time"]
        metrics["memory_references"] = sum(1 for word in memory_words if word in response_lower)
        metrics["memory_score"] = min(metrics["memory_references"] / 2.0, 1.0)
    
    # Overall feature score (simplified)
    feature_scores = [v for k, v in metrics.items() if k.endswith("_score")]
    metrics["feature_score"] = sum(feature_scores) / len(feature_scores) if feature_scores else 0.5
    
    return metrics


def run_all_personalization_tests():
    """Run all personalization feature tests"""
    
    print("\n" + "="*80)
    print("🧪 Running 10 Personalization Feature Tests")
    print("="*80)
    
    # Initialize chat interface
    chat = ChatInterface(groq_api_key)
    
    # Create output directory
    output_dir = "personalization_test_outputs"
    os.makedirs(output_dir, exist_ok=True)
    
    all_results = []
    
    # Run each scenario
    for scenario in CONVERSATION_SCENARIOS:
        result = run_conversation_scenario(chat, scenario)
        all_results.append(result)
        
        # Save individual result
        output_file = os.path.join(output_dir, f"{scenario['scenario_id']}_results.json")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(f"💾 Saved: {output_file}")
    
    # Save summary
    summary = {
        "timestamp": datetime.now().isoformat(),
        "total_scenarios": len(CONVERSATION_SCENARIOS),
        "results": all_results
    }
    
    summary_file = os.path.join(output_dir, "all_personalization_results.json")
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Summary saved: {summary_file}")
    print("\n✅ All personalization tests completed!")
    
    return all_results


if __name__ == "__main__":
    run_all_personalization_tests()














