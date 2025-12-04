"""
Test Scenarios for Personalized Learning System
Different code types and scenarios to test system responses
"""

# Test Scenarios - Different code types and student situations
TEST_SCENARIOS = [
    {
        "id": "scenario_001",
        "name": "Recursion Missing Base Case",
        "category": "recursion",
        "difficulty": "beginner",
        "code": """def factorial(n):
    return n * factorial(n - 1)""",
        "question": "Why does my code fail?",
        "expected_concepts": ["recursion", "base_case", "infinite_recursion"],
        "expected_errors": ["missing_base_case", "recursion_error"],
        "student_state": {
            "mastery": 0.3,
            "emotion": "confused",
            "learning_style": "visual"
        }
    },
    {
        "id": "scenario_002",
        "name": "Null Pointer Exception",
        "category": "linked_list",
        "difficulty": "intermediate",
        "code": """def traverse_list(head):
    current = head
    while current:
        print(current.data)
        current = current.next
    return current.data  # Error: accessing after loop""",
        "question": "I'm getting an error when the list is empty. What's wrong?",
        "expected_concepts": ["null_pointer", "linked_list", "edge_cases"],
        "expected_errors": ["null_pointer_exception", "empty_list_handling"],
        "student_state": {
            "mastery": 0.5,
            "emotion": "frustrated",
            "learning_style": "practical"
        }
    },
    {
        "id": "scenario_003",
        "name": "Off-by-One Error",
        "category": "arrays",
        "difficulty": "beginner",
        "code": """def find_max(numbers):
    max_num = 0
    for i in range(len(numbers)):
        if numbers[i] > max_num:
            max_num = numbers[i]
    return max_num""",
        "question": "My function returns 0 for negative numbers. Why?",
        "expected_concepts": ["initialization", "edge_cases", "negative_numbers"],
        "expected_errors": ["initialization_error", "off_by_one"],
        "student_state": {
            "mastery": 0.4,
            "emotion": "confused",
            "learning_style": "conceptual"
        }
    },
    {
        "id": "scenario_004",
        "name": "Variable Scope Issue",
        "category": "scope",
        "difficulty": "intermediate",
        "code": """def process_data():
    result = []
    for item in data:
        processed = item * 2
        result.append(processed)
    return result

data = [1, 2, 3]
print(process_data())""",
        "question": "Why is 'data' not defined error happening?",
        "expected_concepts": ["variable_scope", "function_parameters", "global_variables"],
        "expected_errors": ["name_error", "scope_issue"],
        "student_state": {
            "mastery": 0.6,
            "emotion": "neutral",
            "learning_style": "practical"
        }
    },
    {
        "id": "scenario_005",
        "name": "Infinite Loop",
        "category": "loops",
        "difficulty": "beginner",
        "code": """def countdown(n):
    while n > 0:
        print(n)
    print("Blast off!")""",
        "question": "My program never stops. What's wrong?",
        "expected_concepts": ["infinite_loop", "loop_condition", "variable_modification"],
        "expected_errors": ["infinite_loop", "missing_increment"],
        "student_state": {
            "mastery": 0.3,
            "emotion": "frustrated",
            "learning_style": "visual"
        }
    },
    {
        "id": "scenario_006",
        "name": "Type Error - String vs Int",
        "category": "types",
        "difficulty": "beginner",
        "code": """def add_numbers(a, b):
    return a + b

result = add_numbers("5", 3)
print(result)""",
        "question": "Why am I getting '53' instead of 8?",
        "expected_concepts": ["type_conversion", "string_concatenation", "type_errors"],
        "expected_errors": ["type_error", "implicit_conversion"],
        "student_state": {
            "mastery": 0.35,
            "emotion": "confused",
            "learning_style": "conceptual"
        }
    },
    {
        "id": "scenario_007",
        "name": "Index Out of Bounds",
        "category": "arrays",
        "difficulty": "intermediate",
        "code": """def get_middle_element(arr):
    mid = len(arr) // 2
    return arr[mid]

print(get_middle_element([]))""",
        "question": "I get an error with empty arrays. How do I fix this?",
        "expected_concepts": ["index_error", "edge_cases", "array_bounds"],
        "expected_errors": ["index_out_of_bounds", "empty_array"],
        "student_state": {
            "mastery": 0.5,
            "emotion": "neutral",
            "learning_style": "practical"
        }
    },
    {
        "id": "scenario_008",
        "name": "Logic Error - Comparison",
        "category": "logic",
        "difficulty": "intermediate",
        "code": """def is_even(n):
    if n % 2 = 0:  # Error: assignment instead of comparison
        return True
    return False""",
        "question": "Why is there a syntax error?",
        "expected_concepts": ["assignment_vs_comparison", "syntax_error", "operators"],
        "expected_errors": ["syntax_error", "assignment_in_condition"],
        "student_state": {
            "mastery": 0.45,
            "emotion": "confused",
            "learning_style": "visual"
        }
    },
    {
        "id": "scenario_009",
        "name": "Memory Issue - List Mutation",
        "category": "data_structures",
        "difficulty": "advanced",
        "code": """def remove_duplicates(lst):
    for item in lst:
        if lst.count(item) > 1:
            lst.remove(item)
    return lst

numbers = [1, 2, 2, 3, 3, 3]
print(remove_duplicates(numbers))""",
        "question": "Why doesn't this remove all duplicates?",
        "expected_concepts": ["list_mutation", "iteration_while_modifying", "algorithm_complexity"],
        "expected_errors": ["logical_error", "mutation_during_iteration"],
        "student_state": {
            "mastery": 0.7,
            "emotion": "frustrated",
            "learning_style": "conceptual"
        }
    },
    {
        "id": "scenario_010",
        "name": "Conceptual Question - No Code",
        "category": "conceptual",
        "difficulty": "beginner",
        "code": None,
        "question": "I don't understand how pointers work in linked lists. Can you explain?",
        "expected_concepts": ["pointers", "linked_list", "memory_references"],
        "expected_errors": [],
        "student_state": {
            "mastery": 0.2,
            "emotion": "confused",
            "learning_style": "visual"
        }
    }
]

# Scenario categories for analysis
SCENARIO_CATEGORIES = {
    "recursion": ["scenario_001"],
    "linked_list": ["scenario_002"],
    "arrays": ["scenario_003", "scenario_007"],
    "scope": ["scenario_004"],
    "loops": ["scenario_005"],
    "types": ["scenario_006"],
    "logic": ["scenario_008"],
    "data_structures": ["scenario_009"],
    "conceptual": ["scenario_010"]
}

# Difficulty levels
DIFFICULTY_LEVELS = {
    "beginner": ["scenario_001", "scenario_003", "scenario_005", "scenario_006", "scenario_010"],
    "intermediate": ["scenario_002", "scenario_004", "scenario_007", "scenario_008"],
    "advanced": ["scenario_009"]
}


def get_scenario_by_id(scenario_id):
    """Get a specific scenario by ID"""
    for scenario in TEST_SCENARIOS:
        if scenario["id"] == scenario_id:
            return scenario
    return None


def get_scenarios_by_category(category):
    """Get all scenarios in a category"""
    return [s for s in TEST_SCENARIOS if s["category"] == category]


def get_scenarios_by_difficulty(difficulty):
    """Get all scenarios of a specific difficulty"""
    return [s for s in TEST_SCENARIOS if s["difficulty"] == difficulty]


def get_all_scenarios():
    """Get all test scenarios"""
    return TEST_SCENARIOS

















