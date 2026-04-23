"""
Enhanced Example Usage with Improved Output Formatting
Features:
- Color-coded output
- Better table formatting
- Progress visualizations
- Export capabilities
- Interactive comparisons
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


def print_header(text: str, char: str = "=", width: int = 80):
    """Print a formatted header"""
    print(f"\n{Fore.CYAN}{Style.BRIGHT}{char * width}")
    print(f"{text.center(width)}")
    print(f"{char * width}{Style.RESET_ALL}\n")


def print_section(text: str, level: int = 1):
    """Print a section header"""
    if level == 1:
        print(f"\n{Fore.MAGENTA}{Style.BRIGHT}▶ {text}{Style.RESET_ALL}")
        print(f"{'─' * 78}")
    elif level == 2:
        print(f"\n{Fore.BLUE}  • {text}{Style.RESET_ALL}")
    else:
        print(f"{Fore.WHITE}    → {text}{Style.RESET_ALL}")


def print_success(text: str):
    """Print success message"""
    print(f"{Fore.GREEN}✓ {text}{Style.RESET_ALL}")


def print_warning(text: str):
    """Print warning message"""
    print(f"{Fore.YELLOW}⚠ {text}{Style.RESET_ALL}")


def print_error(text: str):
    """Print error message"""
    print(f"{Fore.RED}✗ {text}{Style.RESET_ALL}")


def print_info(text: str):
    """Print info message"""
    print(f"{Fore.CYAN}ℹ {text}{Style.RESET_ALL}")


def format_percentage(value: float, decimals: int = 1) -> str:
    """Format percentage with color coding"""
    if value >= 0.8:
        color = Fore.GREEN
    elif value >= 0.5:
        color = Fore.YELLOW
    else:
        color = Fore.RED
    return f"{color}{value:.{decimals}%}{Style.RESET_ALL}"


def format_score(value: float, max_value: float = 1.0) -> str:
    """Format score with visual bar"""
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
    """Print a formatted table"""
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


def print_decision_tree(decisions: Dict):
    """Print hierarchical decision tree"""
    print_section("Decision Flow", level=1)
    
    levels = [
        ("Meta-Level", decisions.get('meta_strategy', {})),
        ("Curriculum", decisions.get('curriculum_decision', {})),
        ("Session", decisions.get('session_plan', {})),
        ("Intervention", decisions.get('intervention', {}))
    ]
    
    for i, (level_name, level_data) in enumerate(levels):
        indent = "  " * i
        arrow = "↓" if i < len(levels) - 1 else "✓"
        
        if level_name == "Meta-Level":
            approach = level_data.get('approach', 'N/A')
            print(f"{indent}{Fore.MAGENTA}{arrow} {level_name}:{Style.RESET_ALL} {approach}")
        elif level_name == "Curriculum":
            concept = level_data.get('concept', 'N/A')
            print(f"{indent}{Fore.BLUE}{arrow} {level_name}:{Style.RESET_ALL} {concept}")
        elif level_name == "Session":
            intervention = level_data.get('intervention', 'N/A')
            print(f"{indent}{Fore.YELLOW}{arrow} {level_name}:{Style.RESET_ALL} {intervention}")
        else:
            content_type = level_data.get('content_type', 'N/A')
            print(f"{indent}{Fore.GREEN}{arrow} {level_name}:{Style.RESET_ALL} {content_type}")


def print_objective_weights(weights: Dict, outcomes: Optional[Dict] = None):
    """Print objective weights with visual bars"""
    print_section("Multi-Objective Optimization", level=2)
    
    for obj, weight in sorted(weights.items(), key=lambda x: x[1], reverse=True):
        bar = "█" * int(weight * 50)
        color = Fore.GREEN if weight > 0.3 else Fore.YELLOW if weight > 0.15 else Fore.WHITE
        
        line = f"  {obj:15s}: {color}{bar}{Style.RESET_ALL} {weight:.2f}"
        
        if outcomes and obj in outcomes:
            q_val = outcomes[obj]
            q_color = Fore.GREEN if q_val > 0.7 else Fore.YELLOW if q_val > 0.4 else Fore.RED
            line += f"  {q_color}(Q={q_val:+.3f}){Style.RESET_ALL}"
        
        print(line)


def print_knowledge_gaps(gaps: List[Dict]):
    """Print knowledge gaps with severity indicators"""
    if not gaps:
        print_success("No critical knowledge gaps detected!")
        return
    
    print_section("Knowledge Gaps", level=2)
    
    for gap in gaps:
        concept = gap.get('concept', 'Unknown')
        severity = gap.get('severity', 0.0)
        blocks = gap.get('blocks', 'Unknown')
        
        if severity >= 0.8:
            severity_color = Fore.RED
            severity_icon = "🔴"
        elif severity >= 0.5:
            severity_color = Fore.YELLOW
            severity_icon = "🟡"
        else:
            severity_color = Fore.GREEN
            severity_icon = "🟢"
        
        print(f"  {severity_icon} {concept:20s} "
              f"{severity_color}Severity: {severity:.0%}{Style.RESET_ALL} "
              f"→ Blocks: {blocks}")


def export_to_json(data: Dict, filename: str):
    """Export results to JSON file"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print_success(f"Results exported to {filename}")
    except Exception as e:
        print_error(f"Failed to export: {e}")


def export_to_markdown(data: Dict, filename: str):
    """Export results to Markdown file"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"# Hierarchical RL Teaching Results\n\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # Meta Strategy
            if 'meta_strategy' in data:
                f.write("## Meta-Level Strategy\n\n")
                meta = data['meta_strategy']
                f.write(f"- **Student Type**: {meta.get('student_type', 'N/A')}\n")
                f.write(f"- **Approach**: {meta.get('approach', 'N/A')}\n")
                f.write(f"- **Expected Success**: {meta.get('expected_success', 0):.0%}\n\n")
            
            # Curriculum Decision
            if 'curriculum_decision' in data:
                f.write("## Curriculum Decision\n\n")
                curr = data['curriculum_decision']
                f.write(f"- **Concept**: {curr.get('concept', 'N/A')}\n")
                f.write(f"- **Priority Score**: {curr.get('score', 0):.3f}\n\n")
            
            # Session Plan
            if 'session_plan' in data:
                f.write("## Session Plan\n\n")
                session = data['session_plan']
                f.write(f"- **Intervention**: {session.get('intervention', 'N/A')}\n")
                f.write(f"- **Primary Objective**: {session.get('primary_objective', 'N/A')}\n\n")
                
                f.write("### Objective Weights\n\n")
                for obj, weight in session.get('objective_weights', {}).items():
                    f.write(f"- {obj}: {weight:.2f}\n")
                f.write("\n")
            
            # Intervention
            if 'intervention' in data:
                f.write("## Intervention Details\n\n")
                interv = data['intervention']
                f.write(f"- **Content Type**: {interv.get('content_type', 'N/A')}\n")
                f.write(f"- **Scaffolding Level**: {interv.get('scaffolding', 0)}/5\n")
                f.write(f"- **Duration**: {interv.get('duration', 0)} minutes\n\n")
        
        print_success(f"Results exported to {filename}")
    except Exception as e:
        print_error(f"Failed to export: {e}")


def example_hierarchical_multitask_rl_enhanced(export: bool = False):
    """
    Enhanced version with better output formatting
    """
    
    print_header("HIERARCHICAL MULTI-TASK RL: Complete Teaching Example", "═", 80)
    
    # Sarah's complete state
    sarah_state = {
        "student_id": "sarah_2024",
        "student_type": "systematic_beginner",
        "overall_progress": 0.35,
        "completed_concepts": ["variables", "conditionals", "loops", "functions"],
        "learning_goals": ["master_recursion", "learn_data_structures", "algorithms"],
        "current_concept": "recursion",
        "mastery": 0.18,
        "emotion": "confused",
        "frustration_level": 0.62,
        "engagement_score": 0.45,
        "time_stuck": 120,
        "knowledge_gaps": [
            {"concept": "base_case", "severity": 0.92, "blocks": "recursion"},
            {"concept": "recursive_call", "severity": 0.78, "blocks": "recursion"}
        ],
        "conscientiousness": 0.82,
        "neuroticism": 0.45,
        "openness": 0.55,
        "learning_style": "visual_sequential",
        "behavioral_pattern": "systematic_struggling",
        "dropout_risk": 0.35,
        "session_duration": 18,
        "previous_interventions": ["visual_explanation", "worked_example"],
        "time_of_day": "evening"
    }
    
    # Display input state
    print_section("Student State Analysis", level=1)
    
    state_table = [
        {"Metric": "Student ID", "Value": sarah_state['student_id']},
        {"Metric": "Type", "Value": sarah_state['student_type']},
        {"Metric": "Current Concept", "Value": sarah_state['current_concept']},
        {"Metric": "Mastery", "Value": format_percentage(sarah_state['mastery'])},
        {"Metric": "Emotion", "Value": sarah_state['emotion']},
        {"Metric": "Frustration", "Value": format_percentage(sarah_state['frustration_level'])},
        {"Metric": "Engagement", "Value": format_percentage(sarah_state['engagement_score'])},
        {"Metric": "Dropout Risk", "Value": format_percentage(sarah_state['dropout_risk'])},
    ]
    print_table(state_table, ["Metric", "Value"], "Current State")
    
    # Display knowledge gaps
    print_knowledge_gaps(sarah_state['knowledge_gaps'])
    
    # Send to API
    print_section("Processing Request", level=1)
    print_info("Sending request to hierarchical RL API...")
    
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
    
    # LEVEL 1: Meta-Level Controller
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
    
    print_info(f"System identified '{meta.get('student_type', 'N/A')}' → "
              f"Best strategy: {meta.get('approach', 'N/A')} "
              f"({format_percentage(meta.get('expected_success', 0))} success rate)")
    
    # LEVEL 2: Curriculum Controller
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
    
    # LEVEL 3: Session Multi-Task Controller
    print_header("LEVEL 3: SESSION MULTI-TASK CONTROLLER", "─", 80)
    
    session = result.get('session_plan', {})
    print_section(f"Selected Intervention: {session.get('intervention', 'N/A')}", level=2)
    print_section(f"Primary Objective: {session.get('primary_objective', 'N/A')}", level=2)
    
    # Objective weights with visual bars
    weights = session.get('objective_weights', {})
    outcomes = session.get('expected_outcomes', {})
    print_objective_weights(weights, outcomes)
    
    # Combined Q-value
    q_combined = session.get('q_combined', 0)
    print_section("Combined Q-Value (Expected Reward)", level=2)
    print(f"  {format_score(q_combined)}")
    
    # Insight
    print_info("System optimizes 5 objectives simultaneously based on student state")
    
    # LEVEL 4: Intervention Executor
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
    
    # Complete Decision Flow
    print_header("COMPLETE DECISION FLOW", "═", 80)
    print_decision_tree(result)
    
    # Summary
    print_header("SUMMARY", "═", 80)
    summary_table = [
        {"Level", "Decision", "Key Metric"},
        {"Meta", meta.get('approach', 'N/A'), format_percentage(meta.get('expected_success', 0))},
        {"Curriculum", curr.get('concept', 'N/A'), f"Score: {curr.get('score', 0):.3f}"},
        {"Session", session.get('intervention', 'N/A'), f"Q: {q_combined:.3f}"},
        {"Intervention", interv.get('content_type', 'N/A'), f"Scaffolding: {scaffolding}/5"},
    ]
    print_table(summary_table, ["Level", "Decision", "Key Metric"])
    
    # Export if requested
    if export:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        export_to_json(result, f"rl_results_{timestamp}.json")
        export_to_markdown(result, f"rl_results_{timestamp}.md")
    
    return result


def example_compare_interventions_enhanced():
    """Enhanced intervention comparison with better visualization"""
    
    print_header("INTERVENTION COMPARISON: Q-Values Analysis", "═", 80)
    
    sarah_state = {
        "student_id": "sarah",
        "mastery": 0.18,
        "emotion": "confused",
        "current_concept": "recursion"
    }
    
    print_section("Student State", level=1)
    print(f"  Mastery: {format_percentage(sarah_state['mastery'])}")
    print(f"  Emotion: {sarah_state['emotion']}")
    print(f"  Concept: {sarah_state['current_concept']}")
    
    try:
        response = requests.post(
            "http://localhost:8000/api/rl/compare_interventions",
            json=sarah_state,
            timeout=30
        )
        
        if response.status_code != 200:
            print_error(f"API returned status {response.status_code}")
            return None
        
        result = response.json()
        
    except requests.exceptions.ConnectionError:
        print_error("Cannot connect to API. Is the server running?")
        return None
    except Exception as e:
        print_error(f"Error: {e}")
        return None
    
    # Sort interventions by Q-value
    interventions = sorted(
        result['interventions'].items(),
        key=lambda x: x[1]['q_value'],
        reverse=True
    )
    
    print_header("Intervention Rankings", "─", 80)
    
    # Create comparison table
    comparison_data = []
    for rank, (intervention, data) in enumerate(interventions, 1):
        q_value = data['q_value']
        success_rate = data.get('success_rate', 0)
        
        comparison_data.append({
            "Rank": f"#{rank}",
            "Intervention": intervention.replace('_', ' ').title(),
            "Q-Value": f"{q_value:.3f}",
            "Success Rate": format_percentage(success_rate),
            "Best For": data.get('best_for', 'N/A')[:40]
        })
    
    print_table(comparison_data, ["Rank", "Intervention", "Q-Value", "Success Rate", "Best For"])
    
    # Highlight top 3
    print_section("Top 3 Recommendations", level=1)
    for rank, (intervention, data) in enumerate(interventions[:3], 1):
        medal = "🥇" if rank == 1 else "🥈" if rank == 2 else "🥉"
        print(f"  {medal} {rank}. {intervention.replace('_', ' ').title()}")
        print(f"     Q-Value: {format_score(data['q_value'])}")
        print(f"     Success Rate: {format_percentage(data.get('success_rate', 0))}")
        print(f"     Best for: {data.get('best_for', 'N/A')}\n")
    
    # Selected intervention
    selected = result.get('selected_intervention', 'N/A')
    print_section("Selected Intervention", level=1)
    print_success(f"{selected.replace('_', ' ').title()}")
    print(f"  Expected Reward: {format_score(result.get('expected_reward', 0))}")
    print(f"  Confidence: {format_percentage(result.get('confidence', 0))}")
    
    return result


if __name__ == "__main__":
    print_header("ENHANCED PERSONALIZED LEARNING SYSTEM", "═", 80)
    print_info("Improved output formatting with colors, tables, and visualizations\n")
    
    # Check API connection
    try:
        response = requests.get("http://localhost:8000/", timeout=5)
        if response.status_code == 200:
            print_success("API server is running")
        else:
            print_warning("API server returned unexpected status")
    except:
        print_error("Cannot connect to API server")
        print_info("Please start the server with: python api/server.py")
        sys.exit(1)
    
    # Run enhanced examples
    print("\n" + "="*80)
    print("Running Enhanced Hierarchical RL Example")
    print("="*80)
    
    result = example_hierarchical_multitask_rl_enhanced(export=True)
    
    if result:
        print("\n" + "="*80)
        print("Running Enhanced Intervention Comparison")
        print("="*80)
        example_compare_interventions_enhanced()
    
    print_header("Examples Complete!", "═", 80)

















