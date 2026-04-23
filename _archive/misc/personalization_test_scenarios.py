"""
10 Personalization Feature Test Scenarios
Each scenario tests a specific personalization feature with psychological aspects
"""

PERSONALIZATION_SCENARIOS = [
    {
        "id": "personalization_001",
        "name": "Conversation Memory & Context",
        "feature": "conversation_memory",
        "description": "Tests if system remembers previous conversation context",
        "code": None,
        "conversation_history": [
            {"role": "student", "message": "I'm learning about recursion"},
            {"role": "bot", "message": "Great! Recursion is when a function calls itself..."},
            {"role": "student", "message": "Can you give me an example?"}
        ],
        "current_question": "How do I know when to stop it?",
        "expected_indicators": {
            "references_previous": ["recursion", "function", "calls itself"],
            "maintains_context": True,
            "builds_on_previous": True
        },
        "student_state": {
            "mastery": 0.3,
            "interaction_count": 3,
            "recent_topics": ["recursion"]
        },
        "quantitative_checks": {
            "previous_topic_mentions": 1,  # Should mention recursion
            "context_continuity": True
        }
    },
    {
        "id": "personalization_002",
        "name": "Emotional Intelligence & Tone Adaptation",
        "feature": "emotional_intelligence",
        "description": "Tests if system adapts tone based on student's frustration",
        "code": """def factorial(n):
    return n * factorial(n - 1)""",
        "question": "This keeps crashing! I've been trying for hours and nothing works!",
        "expected_indicators": {
            "tone": "gentle_supportive",
            "encouragement": ["don't worry", "common", "normal", "struggle"],
            "reassurance": True,
            "step_size": "small"
        },
        "student_state": {
            "mastery": 0.2,
            "emotion": "frustrated",
            "frustration_level": 0.8,
            "attempts": 5
        },
        "quantitative_checks": {
            "encouragement_words_count": 2,  # At least 2 encouraging phrases
            "tone_appropriateness": True
        }
    },
    {
        "id": "personalization_003",
        "name": "Learning Style Deep Personalization - Visual",
        "feature": "learning_style_visual",
        "description": "Tests if system provides visual explanations for visual learners",
        "code": """def traverse_list(head):
    current = head
    while current:
        print(current.data)
        current = current.next""",
        "question": "I don't understand how the nodes are connected. Can you show me?",
        "expected_indicators": {
            "visual_elements": ["diagram", "visual", "picture", "see", "imagine", "draw"],
            "spatial_descriptions": ["next to", "pointing to", "connected", "link"],
            "metaphors": ["chain", "train", "beads"]
        },
        "student_state": {
            "mastery": 0.4,
            "learning_style": "visual",
            "preferences": {"format": "diagrams", "examples": "visual"}
        },
        "quantitative_checks": {
            "visual_keywords_count": 3,  # At least 3 visual-related words
            "diagram_mentions": 1
        }
    },
    {
        "id": "personalization_004",
        "name": "Learning Style Deep Personalization - Conceptual",
        "feature": "learning_style_conceptual",
        "description": "Tests if system provides deep conceptual explanations",
        "code": None,
        "question": "Why does recursion work? What's the underlying principle?",
        "expected_indicators": {
            "conceptual_depth": ["principle", "fundamental", "underlying", "why", "how"],
            "theory_focus": True,
            "abstraction_level": "high"
        },
        "student_state": {
            "mastery": 0.6,
            "learning_style": "conceptual",
            "preferences": {"depth": "deep", "theory": True}
        },
        "quantitative_checks": {
            "conceptual_keywords_count": 3,
            "theory_mentions": 1
        }
    },
    {
        "id": "personalization_005",
        "name": "Personality-Based Communication - High Neuroticism",
        "feature": "personality_neuroticism",
        "description": "Tests if system provides extra reassurance for anxious students",
        "code": """def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1""",
        "question": "Is my code correct? I'm worried I might have made a mistake.",
        "expected_indicators": {
            "reassurance": ["correct", "good", "well done", "no worries"],
            "confidence_boosting": True,
            "anxiety_reduction": ["common", "normal", "everyone"]
        },
        "student_state": {
            "mastery": 0.5,
            "personality": {
                "neuroticism": 0.8,  # High anxiety
                "openness": 0.6,
                "conscientiousness": 0.7
            }
        },
        "quantitative_checks": {
            "reassurance_phrases_count": 2,
            "positive_feedback": True
        }
    },
    {
        "id": "personalization_006",
        "name": "Progress-Aware Responses",
        "feature": "progress_awareness",
        "description": "Tests if system acknowledges student's progress and mastery level",
        "code": """def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)""",
        "question": "I understand basic recursion now. Can you explain divide and conquer?",
        "expected_indicators": {
            "progress_acknowledgment": ["progress", "improved", "mastered", "understand"],
            "mastery_reference": True,
            "adaptive_complexity": "intermediate"  # Matches their progress
        },
        "student_state": {
            "mastery": 0.7,
            "interaction_count": 15,
            "recent_achievements": ["understood_recursion", "solved_3_problems"]
        },
        "quantitative_checks": {
            "progress_mentions": 1,
            "mastery_level_match": True
        }
    },
    {
        "id": "personalization_007",
        "name": "Interest & Context Personalization",
        "feature": "interest_context",
        "description": "Tests if system incorporates student's interests",
        "code": None,
        "question": "How can I use recursion in game development?",
        "expected_indicators": {
            "interest_connection": ["game", "gaming", "game development"],
            "contextual_examples": ["game", "player", "level", "character"],
            "relevance": True
        },
        "student_state": {
            "mastery": 0.5,
            "interests": ["gaming", "game development", "video games"],
            "context": "learning_for_game_project"
        },
        "quantitative_checks": {
            "interest_mentions": 2,
            "contextual_examples_count": 1
        }
    },
    {
        "id": "personalization_008",
        "name": "Response Format Preferences",
        "feature": "format_preferences",
        "description": "Tests if system adapts response format to student preferences",
        "code": """def find_max(numbers):
    max_num = 0
    for num in numbers:
        if num > max_num:
            max_num = num
    return max_num""",
        "question": "What's wrong with my code?",
        "expected_indicators": {
            "format_type": "structured",  # Student prefers lists/bullets
            "has_bullet_points": True,
            "has_numbered_steps": True,
            "clear_sections": True
        },
        "student_state": {
            "mastery": 0.4,
            "format_preference": "structured",
            "preferred_format": "bullet_points"
        },
        "quantitative_checks": {
            "bullet_points_count": 2,
            "structured_format": True
        }
    },
    {
        "id": "personalization_009",
        "name": "Error-Specific & Diagnostic Feedback",
        "feature": "error_diagnostic",
        "description": "Tests if system provides specific, diagnostic error feedback",
        "code": """def traverse_list(head):
    current = head
    while current:
        print(current.data)
        current = current.next
    return current.data  # Error: accessing after loop""",
        "question": "I'm getting a NoneType error. What's happening?",
        "expected_indicators": {
            "error_identification": ["NoneType", "null", "None", "after loop"],
            "specific_location": ["line", "after", "loop ends"],
            "diagnostic_explanation": ["why", "because", "reason"],
            "fix_suggestion": ["check", "if", "before", "access"]
        },
        "student_state": {
            "mastery": 0.5,
            "error_history": ["null_pointer", "index_error"]
        },
        "quantitative_checks": {
            "error_mentions": 2,
            "fix_suggestions_count": 1,
            "diagnostic_depth": "high"
        }
    },
    {
        "id": "personalization_010",
        "name": "Metacognitive & Learning Strategy Support",
        "feature": "metacognitive_guidance",
        "description": "Tests if system teaches learning strategies, not just answers",
        "code": None,
        "question": "I keep making the same mistakes. How can I learn better?",
        "expected_indicators": {
            "strategy_guidance": ["strategy", "approach", "method", "technique"],
            "metacognitive_prompts": ["think about", "reflect", "analyze", "why"],
            "learning_how_to_learn": True,
            "self_regulation": ["practice", "review", "identify patterns"]
        },
        "student_state": {
            "mastery": 0.4,
            "learning_strategies": ["needs_improvement"],
            "metacognitive_level": "developing"
        },
        "quantitative_checks": {
            "strategy_mentions": 2,
            "metacognitive_prompts_count": 1
        }
    },
    {
        "id": "personalization_011",
        "name": "Adaptive Difficulty & Pacing",
        "feature": "adaptive_difficulty",
        "description": "Tests if system adjusts difficulty based on student performance",
        "code": """def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)""",
        "question": "I understand this. What's next?",
        "expected_indicators": {
            "difficulty_progression": ["next level", "more advanced", "challenge"],
            "pacing_adaptation": "appropriate",
            "scaffolding_removal": True,  # Less hand-holding for advanced students
            "complexity_increase": True
        },
        "student_state": {
            "mastery": 0.8,
            "recent_success_rate": 0.9,
            "pacing_preference": "fast",
            "difficulty_level": "advanced"
        },
        "quantitative_checks": {
            "difficulty_mentions": 1,
            "pacing_appropriate": True
        }
    }
]

# Feature mapping for quick lookup
FEATURE_MAPPING = {
    "conversation_memory": "personalization_001",
    "emotional_intelligence": "personalization_002",
    "learning_style_visual": "personalization_003",
    "learning_style_conceptual": "personalization_004",
    "personality_neuroticism": "personalization_005",
    "progress_awareness": "personalization_006",
    "interest_context": "personalization_007",
    "format_preferences": "personalization_008",
    "error_diagnostic": "personalization_009",
    "metacognitive_guidance": "personalization_010",
    "adaptive_difficulty": "personalization_011"
}

def get_scenario_by_feature(feature_name):
    """Get scenario for a specific personalization feature"""
    scenario_id = FEATURE_MAPPING.get(feature_name)
    if scenario_id:
        return next((s for s in PERSONALIZATION_SCENARIOS if s["id"] == scenario_id), None)
    return None

def get_all_personalization_scenarios():
    """Get all personalization test scenarios"""
    return PERSONALIZATION_SCENARIOS

















