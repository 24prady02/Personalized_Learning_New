"""
Example: How Nestor Profiles Students from Conversation
Shows sample conversation prompts and how responses adapt based on personality/learning style
"""

import os
from src.knowledge_graph.nestor_wrapper import NestorWrapper
from src.orchestrator.enhanced_personalized_generator import EnhancedPersonalizedGenerator
from groq import Groq

# Sample conversation scenarios
CONVERSATION_SCENARIOS = {
    "high_openness_high_extraversion": {
        "question": "This is really interesting! Can you show me different ways to solve this? I want to explore all the possibilities!",
        "conversation": [
            "What if we tried a different approach?",
            "Maybe we could use recursion here?",
            "I'm curious about how this works with other data structures"
        ],
        "code": "def factorial(n):\n    return n * factorial(n-1)",
        "error_message": "RecursionError"
    },
    
    "high_neuroticism_low_extraversion": {
        "question": "I'm really stuck and worried I'll never understand this. I've been trying for hours and nothing works. Can you help?",
        "conversation": [
            "I don't understand why this isn't working",
            "I'm so frustrated",
            "This is too difficult for me",
            "I think I'm doing something wrong"
        ],
        "code": "def factorial(n):\n    return n * factorial(n-1)",
        "error_message": "RecursionError"
    },
    
    "high_conscientiousness_sequential": {
        "question": "I need to understand this step by step. First, can you explain what happens in the first step? Then the second? I want to make sure I follow the logic carefully.",
        "conversation": [
            "Let me check each step",
            "First, we need to...",
            "Then, after that...",
            "Finally, we should..."
        ],
        "code": "def factorial(n):\n    return n * factorial(n-1)",
        "error_message": "RecursionError"
    },
    
    "high_extraversion_visual": {
        "question": "Can you show me a diagram or visual example? I learn better when I can see things!",
        "conversation": [
            "Show me how this works",
            "I want to see an example",
            "Can you draw it out?",
            "Visual examples help me understand"
        ],
        "code": "def factorial(n):\n    return n * factorial(n-1)",
        "error_message": "RecursionError"
    },
    
    "low_openness_reflective": {
        "question": "I need to think about this carefully before trying anything. Can you explain the theory first?",
        "conversation": [
            "Let me understand the concept first",
            "I want to read about this",
            "Before I code, I need to understand",
            "Can you explain the theory?"
        ],
        "code": "def factorial(n):\n    return n * factorial(n-1)",
        "error_message": "RecursionError"
    }
}

def analyze_scenario(scenario_name: str, scenario_data: dict, nestor_wrapper: NestorWrapper, enhanced_generator: EnhancedPersonalizedGenerator):
    """Analyze a conversation scenario and show how Nestor profiles and adapts"""
    
    print("=" * 80)
    print(f"SCENARIO: {scenario_name.upper().replace('_', ' ')}")
    print("=" * 80)
    
    # Prepare student data
    student_data = {
        "question": scenario_data["question"],
        "conversation": scenario_data["conversation"],
        "code": scenario_data["code"],
        "error_message": scenario_data["error_message"],
        "action_sequence": ["code_edit", "run_test", "run_test", "search_documentation"],
        "time_deltas": [15.0, 2.0, 3.0, 45.0],
        "time_stuck": 65.0
    }
    
    print("\n[1] STUDENT'S CONVERSATION:")
    print(f"   Question: {scenario_data['question']}")
    print(f"   Conversation History:")
    for i, msg in enumerate(scenario_data['conversation'], 1):
        print(f"     {i}. {msg}")
    
    # Get Nestor profile
    print("\n[2] NESTOR ANALYSIS:")
    profile = nestor_wrapper.get_student_profile("test_student", student_data)
    
    print(f"   Personality (Big Five):")
    for trait, score in profile["personality"].items():
        level = "HIGH" if score > 0.6 else "LOW" if score < 0.4 else "MEDIUM"
        print(f"     - {trait.capitalize()}: {score:.2f} ({level})")
    
    print(f"\n   Learning Style (Felder-Silverman):")
    for dimension, style in profile["learning_style"].items():
        print(f"     - {dimension.replace('_', ' ').title()}: {style}")
    
    print(f"\n   Learning Strategy: {profile.get('learning_strategy', 'N/A')}")
    print(f"   Intervention Preferences: {profile.get('intervention_preferences', [])}")
    
    # Show how response adapts
    print("\n[3] RESPONSE ADAPTATION:")
    
    # Prepare student state for enhanced generator
    student_state = {
        'student_id': 'test_student',
        'interaction_count': 1,
        'personality': profile['personality'],
        'knowledge_state': {
            'overall_mastery': 0.5,
            'mastery_history': [0.5]
        }
    }
    
    analysis = {
        'emotion': 'confused',
        'frustration_level': profile['personality'].get('neuroticism', 0.5),
        'engagement_score': profile['personality'].get('extraversion', 0.5),
        'mastery_change': 0.0
    }
    
    # Get personality adaptation
    personality_adaptation = enhanced_generator._adapt_to_personality(student_state)
    
    print(f"   Communication Style: {personality_adaptation['communication_style']}")
    print(f"   Tone: {personality_adaptation['tone']}")
    print(f"   Reassurance Level: {personality_adaptation['reassurance_level']}")
    print(f"   Structure Level: {personality_adaptation['structure_level']}")
    print(f"   Engagement Style: {personality_adaptation['engagement_style']}")
    
    if 'instructions' in personality_adaptation:
        print(f"\n   Adaptation Instructions:")
        print(f"     {personality_adaptation['instructions']}")
    
    # Get learning style adaptation
    learning_style_adaptation = enhanced_generator._adapt_to_learning_style(student_state, analysis)
    
    print(f"\n   Learning Style Adaptation:")
    print(f"     Style: {learning_style_adaptation['style']}")
    if 'instructions' in learning_style_adaptation:
        print(f"     Instructions: {learning_style_adaptation['instructions']}")
    
    print("\n" + "-" * 80)
    print("HOW THE RESPONSE WILL BE DIFFERENT:")
    print("-" * 80)
    
    # Explain how response differs
    adaptations = []
    
    if profile['personality']['neuroticism'] > 0.6:
        adaptations.append("• Extra reassurance and gentle tone (high neuroticism)")
    if profile['personality']['openness'] > 0.7:
        adaptations.append("• Creative examples and exploration of alternatives (high openness)")
    if profile['personality']['conscientiousness'] > 0.7:
        adaptations.append("• Structured, step-by-step format with numbered sections (high conscientiousness)")
    if profile['personality']['extraversion'] > 0.6:
        adaptations.append("• Enthusiastic, conversational tone with engaging questions (high extraversion)")
    if profile['learning_style']['visual_verbal'] == 'visual':
        adaptations.append("• Visual diagrams, ASCII art, and visual metaphors (visual learner)")
    if profile['learning_style']['sequential_global'] == 'sequential':
        adaptations.append("• Linear, step-by-step progression (sequential learner)")
    if profile['learning_style']['active_reflective'] == 'reflective':
        adaptations.append("• Theory first, then examples (reflective learner)")
    
    for adaptation in adaptations:
        print(adaptation)
    
    print("\n")

def main():
    """Run all conversation scenarios"""
    
    # Initialize Nestor
    config = {
        'nestor': {
            'personality_traits': ['openness', 'conscientiousness', 'extraversion', 'agreeableness', 'neuroticism'],
            'learning_styles': ['visual_verbal', 'active_reflective', 'sequential_global'],
            'learning_strategies': ['systematic', 'exploratory', 'collaborative', 'independent'],
            'intervention_types': ['visual_explanation', 'interactive_exercise', 'guided_practice', 'conceptual_deepdive', 'motivational_support']
        }
    }
    
    nestor_wrapper = NestorWrapper(config)
    
    # Initialize Enhanced Generator (for adaptation examples)
    groq_api_key = os.getenv('GROQ_API_KEY', '')
    if groq_api_key:
        groq_client = Groq(api_key=groq_api_key)
        enhanced_generator = EnhancedPersonalizedGenerator(groq_client)
    else:
        print("[WARN] Groq API key not set - will show adaptation logic only")
        enhanced_generator = None
    
    print("\n" + "=" * 80)
    print("NESTOR CONVERSATION PROFILING EXAMPLES")
    print("=" * 80)
    print("\nThis demonstrates how Nestor analyzes conversation to understand")
    print("student personality and learning style, then adapts responses accordingly.\n")
    
    # Run each scenario
    for scenario_name, scenario_data in CONVERSATION_SCENARIOS.items():
        analyze_scenario(scenario_name, scenario_data, nestor_wrapper, enhanced_generator)
    
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print("""
Nestor analyzes conversation to infer:
1. Personality Traits (Big Five):
   - Openness: Creativity, curiosity (keywords: "what if", "explore", "interesting")
   - Conscientiousness: Organization, structure (keywords: "step by step", "first", "then")
   - Extraversion: Sociability, energy (keywords: "!", "excited", "let's", exclamation marks)
   - Agreeableness: Kindness, cooperation (keywords: "please", "thank you", "helpful")
   - Neuroticism: Emotional stability (keywords: "worried", "frustrated", "stuck")

2. Learning Style (Felder-Silverman):
   - Visual/Verbal: "show", "see", "diagram" vs "explain", "tell", "describe"
   - Active/Reflective: "try", "test", "run" vs "think", "analyze", "plan"
   - Sequential/Global: "step", "first", "then" vs "big picture", "overall", "whole"

3. Response Adaptation:
   - High Neuroticism -> Extra reassurance, gentle tone
   - High Openness -> Creative examples, exploration
   - High Conscientiousness -> Structured, detailed format
   - High Extraversion -> Enthusiastic, conversational
   - Visual Learner -> Diagrams, visual metaphors
   - Sequential Learner -> Step-by-step progression
""")

if __name__ == "__main__":
    main()

