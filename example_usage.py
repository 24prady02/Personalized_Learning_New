"""
Example usage of the Personalized Learning System
Enhanced with better output formatting, visualizations, and export capabilities
"""

import requests
import json
from typing import Dict, List, Optional
from datetime import datetime
import sys

# Try to import colorama for colored output (optional)
try:
    from colorama import init, Fore, Back, Style
    init(autoreset=True)
    HAS_COLORAMA = True
except ImportError:
    HAS_COLORAMA = False
    # Fallback colors (ANSI codes)
    class Fore:
        RED = '\033[91m'
        GREEN = '\033[92m'
        YELLOW = '\033[93m'
        BLUE = '\033[94m'
        MAGENTA = '\033[95m'
        CYAN = '\033[96m'
        WHITE = '\033[97m'
        RESET = '\033[0m'
    class Style:
        BRIGHT = '\033[1m'
        DIM = '\033[2m'
        RESET_ALL = '\033[0m'


def example_debugging_session():
    """
    Example: Send a debugging session to the API
    """
    
    # Student encounters a recursion bug
    session_data = {
        "student_id": "student_123",
        "code": """
def factorial(n):
    # Missing base case!
    return n * factorial(n - 1)

print(factorial(5))
        """,
        "error_message": "RecursionError: maximum recursion depth exceeded",
        "action_sequence": [
            "code_edit",
            "compile",
            "run_test",
            "search_documentation",
            "code_edit",
            "run_test"
        ],
        "time_deltas": [10.5, 2.1, 1.5, 45.2, 8.3, 1.8],
        "time_stuck": 69.4,
        "problem_id": "recursion_basics_1"
    }
    
    # Send to API
    response = requests.post(
        "http://localhost:8000/api/session",
        json=session_data
    )
    
    if response.status_code == 200:
        result = response.json()
        
        print("=== INTERVENTION RECOMMENDATION ===")
        print(f"Type: {result['intervention_type']}")
        print(f"Priority: {result['priority']:.2f}")
        print(f"Confidence: {result['confidence']:.2f}")
        print(f"\nRationale: {result['rationale']}")
        
        print(f"\n=== GENERATED CONTENT ===")
        print(result['content']['intro'])
        print(result['content']['explanation'])
        
        print(f"\n=== ANALYSIS ===")
        print(f"Emotional State: {result['analysis']['behavioral']['emotion']}")
        print(f"Knowledge Gaps: {len(result['analysis']['knowledge_gaps'])} identified")
        
        return result
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None


def example_student_profile():
    """
    Example: Update student profile with questionnaire data
    """
    
    profile_data = {
        "student_id": "student_123",
        "personality_responses": {
            "openness": [4, 5, 4, 5, 4],  # 1-5 scale responses
            "conscientiousness": [5, 5, 4, 5, 5],
            "extraversion": [3, 3, 2, 3, 3],
            "agreeableness": [4, 4, 5, 4, 4],
            "neuroticism": [2, 3, 2, 2, 3]
        },
        "learning_style_preferences": {
            "visual_verbal": "visual",
            "active_reflective": "active",
            "sequential_global": "sequential"
        }
    }
    
    response = requests.post(
        "http://localhost:8000/api/student/profile",
        json=profile_data
    )
    
    if response.status_code == 200:
        print("✓ Profile updated successfully")
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None


def example_concept_query():
    """
    Example: Query CSE-KG for concept information
    """
    
    concept = "recursion"
    
    response = requests.get(
        f"http://localhost:8000/api/concept/{concept}"
    )
    
    if response.status_code == 200:
        result = response.json()
        
        print(f"=== CONCEPT: {concept} ===")
        print(f"Labels: {result['info']['labels']}")
        print(f"Prerequisites: {len(result['prerequisites'])} concepts")
        print(f"Related: {len(result['related'])} concepts")
        
        return result
    else:
        print(f"Error: {response.status_code}")
        return None


def example_feedback():
    """
    Example: Provide feedback on intervention effectiveness
    """
    
    feedback_data = {
        "student_id": "student_123",
        "intervention_type": "visual_explanation",
        "effectiveness": 0.85,  # 0-1 scale
        "time_to_success": 120.5,  # seconds
        "engagement_score": 0.9
    }
    
    response = requests.post(
        "http://localhost:8000/api/feedback",
        json=feedback_data
    )
    
    if response.status_code == 200:
        print("✓ Feedback recorded")
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None


def main():
    """
    Run all examples
    """
    print("=" * 60)
    print("PERSONALIZED LEARNING SYSTEM - EXAMPLE USAGE")
    print("=" * 60)
    
    # Check if API is running
    try:
        response = requests.get("http://localhost:8000/")
        if response.status_code != 200:
            print("⚠ API is not running. Please start it with:")
            print("  python api/server.py")
            return
    except:
        print("⚠ Cannot connect to API. Please start it with:")
        print("  python api/server.py")
        return
    
    print("\n1. Updating Student Profile...")
    print("-" * 60)
    example_student_profile()
    
    print("\n2. Processing Debugging Session...")
    print("-" * 60)
    example_debugging_session()
    
    print("\n3. Querying Concept from CSE-KG...")
    print("-" * 60)
    example_concept_query()
    
    print("\n4. Providing Intervention Feedback...")
    print("-" * 60)
    example_feedback()
    
    print("\n" + "=" * 60)
    print("EXAMPLES COMPLETE")
    print("=" * 60)


# ===== ENHANCED OUTPUT FORMATTING FUNCTIONS =====

def print_header(text: str, char: str = "=", width: int = 80):
    """Print a formatted header with colors"""
    print(f"\n{Fore.CYAN}{Style.BRIGHT}{char * width}")
    print(f"{text.center(width)}")
    print(f"{char * width}{Style.RESET_ALL}\n")


def print_section(text: str, level: int = 1):
    """Print a section header with indentation"""
    if level == 1:
        print(f"\n{Fore.MAGENTA}{Style.BRIGHT}▶ {text}{Style.RESET_ALL}")
        print(f"{'─' * 78}")
    elif level == 2:
        print(f"\n{Fore.BLUE}  • {text}{Style.RESET_ALL}")
    else:
        print(f"{Fore.WHITE}    → {text}{Style.RESET_ALL}")


def print_success(text: str):
    """Print success message in green"""
    print(f"{Fore.GREEN}✓ {text}{Style.RESET_ALL}")


def print_warning(text: str):
    """Print warning message in yellow"""
    print(f"{Fore.YELLOW}⚠ {text}{Style.RESET_ALL}")


def print_error(text: str):
    """Print error message in red"""
    print(f"{Fore.RED}✗ {text}{Style.RESET_ALL}")


def print_info(text: str):
    """Print info message in cyan"""
    print(f"{Fore.CYAN}ℹ {text}{Style.RESET_ALL}")


def format_percentage(value: float, decimals: int = 1) -> str:
    """Format percentage with color coding based on value"""
    if value >= 0.8:
        color = Fore.GREEN
    elif value >= 0.5:
        color = Fore.YELLOW
    else:
        color = Fore.RED
    return f"{color}{value:.{decimals}%}{Style.RESET_ALL}"


def format_score(value: float, max_value: float = 1.0) -> str:
    """Format score with visual bar chart"""
    percentage = value / max_value
    bar_length = 40
    filled = int(percentage * bar_length)
    bar = "█" * filled + "░" * (bar_length - filled)
    
    if percentage >= 0.8:
        color = Fore.GREEN
    elif percentage >= 0.5:
        color = Fore.YELLOW
    else:
        color = Fore.RED
    
    return f"{color}{bar}{Style.RESET_ALL} {value:.3f}"


def print_table(data: List[Dict], headers: List[str], title: Optional[str] = None):
    """Print a formatted table with aligned columns"""
    if title:
        print_section(title, level=2)
    
    # Calculate column widths
    col_widths = [len(h) for h in headers]
    for row in data:
        for i, header in enumerate(headers):
            value = str(row.get(header, ""))
            col_widths[i] = max(col_widths[i], len(value))
    
    # Print header
    header_row = " | ".join(h.ljust(col_widths[i]) for i, h in enumerate(headers))
    print(f"{Fore.CYAN}{Style.BRIGHT}{header_row}{Style.RESET_ALL}")
    print(f"{'─' * len(header_row)}")
    
    # Print rows
    for row in data:
        row_str = " | ".join(str(row.get(h, "")).ljust(col_widths[i]) 
                            for i, h in enumerate(headers))
        print(row_str)


# ===== EXAMPLE FUNCTIONS =====

def example_hierarchical_multitask_rl():
    """
    Example: Multi-Level Multi-Task RL Teaching System
    Demonstrates all 4 levels of hierarchical RL with enhanced output
    """
    
    print_header("HIERARCHICAL MULTI-TASK RL: Complete Teaching Example", "═", 80)
    
    # Sarah's complete state
    sarah_state = {
        # Student identification
        "student_id": "sarah_2024",
        "student_type": "systematic_beginner",
        
        # Overall progress
        "overall_progress": 0.35,  # 35% through curriculum
        "completed_concepts": ["variables", "conditionals", "loops", "functions"],
        "learning_goals": ["master_recursion", "learn_data_structures", "algorithms"],
        
        # Current session state
        "current_concept": "recursion",
        "mastery": 0.18,  # 18% mastery of recursion
        "emotion": "confused",
        "frustration_level": 0.62,
        "engagement_score": 0.45,
        "time_stuck": 120,  # 2 minutes stuck
        
        # Knowledge gaps
        "knowledge_gaps": [
            {"concept": "base_case", "severity": 0.92, "blocks": "recursion"},
            {"concept": "recursive_call", "severity": 0.78, "blocks": "recursion"}
        ],
        
        # Personality traits
        "conscientiousness": 0.82,  # High
        "neuroticism": 0.45,  # Medium
        "openness": 0.55,  # Medium
        "learning_style": "visual_sequential",
        
        # Behavioral patterns
        "behavioral_pattern": "systematic_struggling",
        "dropout_risk": 0.35,
        
        # Session context
        "session_duration": 18,  # 18 minutes so far
        "previous_interventions": ["visual_explanation", "worked_example"],
        "time_of_day": "evening"
    }
    
    # Send to hierarchical multi-task RL API
    try:
        response = requests.post(
            "http://localhost:8000/api/hierarchical_rl/teach",
            json=sarah_state,
            timeout=30
        )
        
        if response.status_code != 200:
            print_error(f"API returned status {response.status_code}")
            print_error(response.text)
            return None
        
        result = response.json()
        print_success("Request processed successfully!")
        
    except requests.exceptions.ConnectionError:
        print_error("Cannot connect to API. Is the server running?")
        print_info("Start server with: python api/server.py")
        return None
    except Exception as e:
        print_error(f"Error: {e}")
        return None
    
    if result:
        print_header("LEVEL 1: META-LEVEL CONTROLLER", "─", 80)
        
        meta = result.get('meta_strategy', {})
        meta_table = [
            {"Property": "Student Type", "Value": meta.get('student_type', 'N/A')},
            {"Property": "Teaching Approach", "Value": meta.get('approach', 'N/A')},
            {"Property": "Pacing", "Value": meta.get('pacing', 'N/A')},
            {"Property": "Support Level", "Value": meta.get('support_level', 'N/A')},
            {"Property": "Expected Success", "Value": format_percentage(meta.get('expected_success', 0))},
        ]
        print_table(meta_table, ["Property", "Value"])
        
        print_info(f"System identified '{sarah_state['student_type']}' → "
                  f"Best strategy: {meta.get('approach', 'N/A')} "
                  f"({format_percentage(meta.get('expected_success', 0))} success rate)")
        
        
        print_header("LEVEL 2: CURRICULUM CONTROLLER", "─", 80)
        
        curr = result.get('curriculum_decision', {})
        curr_table = [
            {"Property": "Selected Concept", "Value": curr.get('concept', 'N/A')},
            {"Property": "Priority Score", "Value": f"{curr.get('score', 0):.3f}"},
            {"Property": "Prerequisites Met", "Value": "✓ Yes" if curr.get('prereqs_met', False) else "✗ No"},
            {"Property": "Estimated Sessions", "Value": str(curr.get('estimated_sessions', 'N/A'))},
        ]
        print_table(curr_table, ["Property", "Value"])
        
        print_info(f"Selected '{curr.get('concept', 'N/A')}' from 20+ possible concepts")
        print_info(f"Reasoning: {curr.get('reason', 'N/A')}")
        
        
        print_header("LEVEL 3: SESSION MULTI-TASK CONTROLLER", "─", 80)
        
        session = result.get('session_plan', {})
        print_section(f"Selected Intervention: {session.get('intervention', 'N/A')}", level=2)
        print_section(f"Primary Objective: {session.get('primary_objective', 'N/A')}", level=2)
        
        # Objective weights with visual bars
        weights = session.get('objective_weights', {})
        outcomes = session.get('expected_outcomes', {})
        
        print_section("Multi-Objective Weights (Adaptive)", level=2)
        for obj, weight in sorted(weights.items(), key=lambda x: x[1], reverse=True):
            bar = "█" * int(weight * 50)
            color = Fore.GREEN if weight > 0.3 else Fore.YELLOW if weight > 0.15 else Fore.WHITE
            line = f"  {obj:15s}: {color}{bar}{Style.RESET_ALL} {weight:.2f}"
            if obj in outcomes:
                q_val = outcomes[obj]
                q_color = Fore.GREEN if q_val > 0.7 else Fore.YELLOW if q_val > 0.4 else Fore.RED
                line += f"  {q_color}(Q={q_val:+.3f}){Style.RESET_ALL}"
            print(line)
        
        # Combined Q-value
        q_combined = session.get('q_combined', 0)
        print_section("Combined Q-Value (Expected Reward)", level=2)
        print(f"  {format_score(q_combined)}")
        
        print_info("System optimizes 5 objectives simultaneously based on student state")
        
        
        print_header("LEVEL 4: INTERVENTION EXECUTOR", "─", 80)
        
        interv = result.get('intervention', {})
        interv_table = [
            {"Property": "Content Type", "Value": interv.get('content_type', 'N/A')},
            {"Property": "Scaffolding Level", "Value": f"{interv.get('scaffolding', 0)}/5"},
            {"Property": "Estimated Duration", "Value": f"{interv.get('duration', 0)} minutes"},
        ]
        print_table(interv_table, ["Property", "Value"])
        
        # Content preview
        content = interv.get('content', '')
        if content:
            print_section("Content Preview", level=2)
            preview = content[:300] + "..." if len(content) > 300 else content
            print(f"  {preview}")
        
        # Insight
        scaffolding = interv.get('scaffolding', 0)
        print_info(f"High scaffolding ({scaffolding}/5) because:")
        print(f"  → Mastery is low ({format_percentage(sarah_state['mastery'])})")
        print(f"  → Student is {sarah_state['emotion']} and stuck")
        print(f"  → Systematic learner needs structured support")
        
        
        print_header("COMPLETE DECISION FLOW", "═", 80)
        
        # Decision tree visualization
        print_section("Decision Flow", level=1)
        meta = result.get('meta_strategy', {})
        curr = result.get('curriculum_decision', {})
        session = result.get('session_plan', {})
        interv = result.get('intervention', {})
        
        print(f"  {Fore.MAGENTA}↓ Meta-Level:{Style.RESET_ALL} {meta.get('approach', 'N/A')}")
        print(f"    {Fore.BLUE}↓ Curriculum:{Style.RESET_ALL} {curr.get('concept', 'N/A')}")
        print(f"      {Fore.YELLOW}↓ Session:{Style.RESET_ALL} {session.get('intervention', 'N/A')}")
        print(f"        {Fore.GREEN}✓ Intervention:{Style.RESET_ALL} {interv.get('content_type', 'N/A')}")
        
        # Summary table
        print_header("SUMMARY", "═", 80)
        summary_data = [
            {"Level": "Meta", "Decision": meta.get('approach', 'N/A'), 
             "Key Metric": format_percentage(meta.get('expected_success', 0))},
            {"Level": "Curriculum", "Decision": curr.get('concept', 'N/A'), 
             "Key Metric": f"Score: {curr.get('score', 0):.3f}"},
            {"Level": "Session", "Decision": session.get('intervention', 'N/A'), 
             "Key Metric": f"Q: {q_combined:.3f}"},
            {"Level": "Intervention", "Decision": interv.get('content_type', 'N/A'), 
             "Key Metric": f"Scaffolding: {scaffolding}/5"},
        ]
        print_table(summary_data, ["Level", "Decision", "Key Metric"])
        
        return result


def example_multitask_optimization():
    """
    Example: How Multi-Task RL Adapts to Different Student States
    Shows how objective weights change based on student condition
    """
    
    print("\n" + "="*80)
    print("MULTI-TASK RL: Adaptive Objective Weighting")
    print("="*80)
    
    # Test 3 different student states
    scenarios = [
        {
            "name": "Scenario 1: Confused Beginner (Sarah)",
            "state": {
                "student_id": "sarah",
                "mastery": 0.18,
                "emotion": "confused",
                "frustration_level": 0.62,
                "engagement_score": 0.45,
                "dropout_risk": 0.35
            }
        },
        {
            "name": "Scenario 2: Frustrated Struggling Student (Alex)",
            "state": {
                "student_id": "alex",
                "mastery": 0.35,
                "emotion": "frustrated",
                "frustration_level": 0.88,
                "engagement_score": 0.25,
                "dropout_risk": 0.75
            }
        },
        {
            "name": "Scenario 3: Engaged Advanced Student (Maya)",
            "state": {
                "student_id": "maya",
                "mastery": 0.82,
                "emotion": "engaged",
                "frustration_level": 0.15,
                "engagement_score": 0.92,
                "dropout_risk": 0.05
            }
        }
    ]
    
    for scenario in scenarios:
        print(f"\n{'='*80}")
        print(scenario['name'])
        print(f"{'='*80}")
        
        response = requests.post(
            "http://localhost:8000/api/multitask_rl/optimize",
            json=scenario['state']
        )
        
        if response.status_code == 200:
            result = response.json()
            
            print(f"\n📊 Student State:")
            print(f"  Mastery: {scenario['state']['mastery']:.0%}")
            print(f"  Emotion: {scenario['state']['emotion']}")
            print(f"  Frustration: {scenario['state']['frustration_level']:.0%}")
            print(f"  Engagement: {scenario['state']['engagement_score']:.0%}")
            print(f"  Dropout Risk: {scenario['state']['dropout_risk']:.0%}")
            
            print(f"\n🎯 Multi-Task Optimization Results:")
            print(f"  Selected Intervention: {result['intervention']}")
            print(f"  Primary Objective: {result['primary_objective']}")
            
            print(f"\n📈 Adaptive Weights:")
            for obj, weight in result['objective_weights'].items():
                bar = "█" * int(weight * 50)
                print(f"  {obj:12s}: {weight:.2f} {bar}")
            
            print(f"\n💡 Why these weights?")
            print(f"{result['weight_rationale']}")
        
        else:
            print(f"Error: {response.status_code}")
    
    print("\n" + "="*80)
    print("KEY INSIGHT: Multi-Task RL Adapts Objectives to Student State")
    print("="*80)
    print("""
    Confused Student  → Focus on LEARNING (guide them through)
    Frustrated Student → Focus on EMOTIONAL (reduce frustration first!)
    Engaged Student   → Focus on LEARNING + RETENTION (challenge them)
    
    The system automatically balances all 5 objectives based on student needs!
    """)


def example_rl_learning_progress():
    """
    Example: How RL Improves Over Time
    Shows Q-values before and after learning
    """
    
    print("\n" + "="*80)
    print("RL LEARNING PROGRESS: How System Improves")
    print("="*80)
    
    # Query RL learning statistics
    response = requests.get("http://localhost:8000/api/rl/learning_stats")
    
    if response.status_code == 200:
        stats = response.json()
        
        print(f"\n📊 Overall Learning Statistics:")
        print(f"  Total Students Trained: {stats['total_students']}")
        print(f"  Total Experiences: {stats['total_experiences']}")
        print(f"  Training Episodes: {stats['training_episodes']}")
        print(f"  Current Epsilon: {stats['epsilon']:.3f} (exploration rate)")
        
        print(f"\n📈 Performance Over Time:")
        print(f"  Initial Success Rate: {stats['initial_success_rate']:.0%}")
        print(f"  Current Success Rate: {stats['current_success_rate']:.0%}")
        print(f"  Improvement: +{(stats['current_success_rate'] - stats['initial_success_rate']) * 100:.0f}%")
        
        print(f"\n🎯 Learned Policies (What RL Discovered):")
        for policy in stats['learned_policies']:
            print(f"\n  Student Type: {policy['student_type']}")
            print(f"  Best Intervention: {policy['best_intervention']}")
            print(f"  Q-Value: {policy['q_value']:.3f}")
            print(f"  Success Rate: {policy['success_rate']:.0%}")
            print(f"  Evidence: {policy['num_trials']} students")
        
        print(f"\n💡 Key Learnings:")
        for insight in stats['key_insights']:
            print(f"  • {insight}")
        
        return stats
    else:
        print(f"Error: {response.status_code}")
        return None


def example_compare_interventions():
    """
    Example: Compare All Interventions for Sarah's Current State
    Shows Q-values for all 10 interventions
    """
    
    print("\n" + "="*80)
    print("INTERVENTION COMPARISON: Q-Values for Sarah")
    print("="*80)
    
    sarah_state = {
        "student_id": "sarah",
        "mastery": 0.18,
        "emotion": "confused",
        "current_concept": "recursion"
    }
    
    response = requests.post(
        "http://localhost:8000/api/rl/compare_interventions",
        json=sarah_state
    )
    
    if response.status_code == 200:
        result = response.json()
        
        print(f"\nStudent: Sarah (Mastery: 18%, Emotion: Confused)")
        print(f"Concept: Recursion\n")
        
        # Sort by Q-value
        interventions = sorted(
            result['interventions'].items(),
            key=lambda x: x[1]['q_value'],
            reverse=True
        )
        
        print("Q-Values (Expected Reward) for Each Intervention:\n")
        
        for rank, (intervention, data) in enumerate(interventions, 1):
            q_value = data['q_value']
            bar = "█" * int(q_value * 50) if q_value > 0 else ""
            star = "⭐" if rank == 1 else "  "
            
            print(f"{rank:2d}. {star} {intervention:25s} Q={q_value:+.3f} {bar}")
            print(f"       Best for: {data['best_for']}")
            print(f"       Success rate: {data['success_rate']:.0%}")
            print()
        
        print(f"\n✅ SELECTED: {result['selected_intervention']}")
        print(f"   Expected reward: {result['expected_reward']:.3f}")
        print(f"   Confidence: {result['confidence']:.0%}")
        
        return result
    else:
        print(f"Error: {response.status_code}")
        return None


def main():
    """
    Run all examples including hierarchical multi-task RL
    """
    print("=" * 80)
    print("PERSONALIZED LEARNING SYSTEM - COMPLETE EXAMPLE USAGE")
    print("=" * 80)
    
    # Check if API is running
    try:
        response = requests.get("http://localhost:8000/")
        if response.status_code != 200:
            print("⚠ API is not running. Please start it with:")
            print("  python api/server.py")
            return
    except:
        print("⚠ Cannot connect to API. Please start it with:")
        print("  python api/server.py")
        return
    
    # Original examples
    print("\n1. Updating Student Profile...")
    print("-" * 80)
    example_student_profile()
    
    print("\n2. Processing Debugging Session...")
    print("-" * 80)
    example_debugging_session()
    
    print("\n3. Querying Concept from CSE-KG...")
    print("-" * 80)
    example_concept_query()
    
    print("\n4. Providing Intervention Feedback...")
    print("-" * 80)
    example_feedback()
    
    # NEW: Multi-Task RL Examples
    print("\n" + "="*80)
    print("MULTI-TASK REINFORCEMENT LEARNING EXAMPLES")
    print("="*80)
    
    print("\n5. Hierarchical Multi-Task RL (4 Levels)...")
    print("-" * 80)
    example_hierarchical_multitask_rl()
    
    print("\n6. Multi-Task Optimization (Adaptive Weighting)...")
    print("-" * 80)
    example_multitask_optimization()
    
    print("\n7. RL Learning Progress...")
    print("-" * 80)
    example_rl_learning_progress()
    
    print("\n8. Compare All Interventions...")
    print("-" * 80)
    example_compare_interventions()
    
    print("\n" + "=" * 80)
    print("ALL EXAMPLES COMPLETE")
    print("=" * 80)
    print("""
    ✅ Basic API operations
    ✅ Hierarchical Multi-Task RL (4 levels)
    ✅ Multi-objective optimization (5 objectives)
    ✅ Adaptive weight adjustment
    ✅ RL learning progress tracking
    ✅ Intervention comparison
    
    The system now demonstrates the complete power of multi-level multi-task RL!
    """)


if __name__ == "__main__":
    main()

