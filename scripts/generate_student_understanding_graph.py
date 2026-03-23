"""
Generate visual student understanding graph showing code correctness and cognitive state progression
"""

import json
from pathlib import Path
from collections import defaultdict
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import numpy as np

def generate_understanding_graph(conversation_file: str, output_dir: str = "output"):
    """Generate visual graph of student understanding progression"""
    
    # Load conversation
    with open(conversation_file, 'r', encoding='utf-8') as f:
        conversation = json.load(f)
    
    student_id = conversation.get('student_id', 'unknown')
    turns = conversation.get('turns', [])
    
    # Extract data (without DINA mastery)
    turn_numbers = []
    correctness_scores = []
    cognitive_states = []
    errors_encountered = []
    time_durations = []
    time_stuck = []
    
    for turn in turns:
        turn_num = turn.get('turn_number', 0)
        turn_numbers.append(turn_num)
        
        metrics = turn.get('metrics', {})
        quantitative = metrics.get('quantitative', {})
        
        # Code correctness
        codebert = quantitative.get('codebert_analysis', {})
        correctness = codebert.get('correctness_score', 0.5) if codebert else 0.5
        correctness_scores.append(correctness)
        
        # Cognitive state
        coke = quantitative.get('coke_analysis', {})
        cognitive_state = coke.get('cognitive_state', 'unknown') if coke else 'unknown'
        cognitive_states.append(cognitive_state)
        
        # Errors
        student_input = turn.get('student_input', {})
        error = student_input.get('error_message', '')
        errors_encountered.append(1 if error else 0)
        
        # Time tracking
        time_tracking = quantitative.get('time_tracking', {})
        if time_tracking:
            time_durations.append(time_tracking.get('turn_duration_seconds', 0.0))
            time_stuck.append(time_tracking.get('time_stuck_seconds', 0.0))
        else:
            time_durations.append(0.0)
            time_stuck.append(0.0)
    
    # Create figure with subplots
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle(f'Student Understanding Graph: {student_id}', fontsize=16, fontweight='bold')
    
    # Plot 1: Code Correctness Progression
    ax1 = axes[0, 0]
    ax1.plot(turn_numbers, correctness_scores, marker='o', linewidth=2, markersize=8, color='#27AE60', label='Code Correctness')
    ax1.fill_between(turn_numbers, correctness_scores, alpha=0.3, color='#27AE60')
    ax1.axhline(y=0.8, color='green', linestyle='--', alpha=0.5, label='Good (0.8)')
    ax1.axhline(y=0.5, color='orange', linestyle='--', alpha=0.5, label='Fair (0.5)')
    ax1.set_xlabel('Turn Number', fontsize=12)
    ax1.set_ylabel('Correctness Score', fontsize=12)
    ax1.set_title('Code Correctness Progression', fontsize=14, fontweight='bold')
    ax1.set_ylim(0, 1)
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    
    # Plot 2: Errors Encountered
    ax2 = axes[0, 1]
    colors = ['red' if e else 'green' for e in errors_encountered]
    ax2.bar(turn_numbers, errors_encountered, color=colors, alpha=0.7, edgecolor='black', linewidth=1)
    ax2.set_xlabel('Turn Number', fontsize=12)
    ax2.set_ylabel('Error Occurred', fontsize=12)
    ax2.set_title('Errors Encountered per Turn', fontsize=14, fontweight='bold')
    ax2.set_ylim(-0.1, 1.1)
    ax2.set_yticks([0, 1])
    ax2.set_yticklabels(['No Error', 'Error'], fontsize=10)
    ax2.grid(True, alpha=0.3, axis='y')
    
    # Plot 3: Time Analysis
    ax3 = axes[1, 0]
    ax3.plot(turn_numbers, time_durations, marker='o', linewidth=2, markersize=8, color='#3498DB', label='Turn Duration', zorder=2)
    ax3.plot(turn_numbers, time_stuck, marker='s', linewidth=2, markersize=8, color='#E74C3C', label='Time Stuck', zorder=2)
    ax3.fill_between(turn_numbers, time_durations, alpha=0.2, color='#3498DB')
    ax3.fill_between(turn_numbers, time_stuck, alpha=0.2, color='#E74C3C')
    ax3.set_xlabel('Turn Number', fontsize=12)
    ax3.set_ylabel('Time (seconds)', fontsize=12)
    ax3.set_title('Time Analysis per Turn', fontsize=14, fontweight='bold')
    ax3.grid(True, alpha=0.3, zorder=0)
    ax3.legend()
    
    # Plot 4: Cognitive State Transitions
    ax4 = axes[1, 1]
    # Map cognitive states to numbers for plotting
    state_map = {'perceiving': 1, 'understanding': 2, 'engaged': 3, 'confused': 4, 'frustrated': 5, 'unknown': 0}
    state_numbers = [state_map.get(s, 0) for s in cognitive_states]
    ax4.plot(turn_numbers, state_numbers, marker='o', linewidth=2, markersize=10, color='#9B59B6', zorder=2)
    ax4.set_xlabel('Turn Number', fontsize=12)
    ax4.set_ylabel('Cognitive State', fontsize=12)
    ax4.set_title('Cognitive State Transitions', fontsize=14, fontweight='bold')
    ax4.set_yticks([0, 1, 2, 3, 4, 5])
    ax4.set_yticklabels(['Unknown', 'Perceiving', 'Understanding', 'Engaged', 'Confused', 'Frustrated'], fontsize=9)
    ax4.set_ylim(-0.5, 5.5)
    ax4.grid(True, alpha=0.3, zorder=0)
    
    plt.tight_layout()
    
    # Save figure
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    graph_file = output_path / f"understanding_graph_{Path(conversation_file).stem}.png"
    plt.savefig(graph_file, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"[OK] Understanding graph saved to: {graph_file}")
    return graph_file

if __name__ == "__main__":
    import sys
    
    output_dir = "output"
    
    if len(sys.argv) > 1:
        conversation_file = sys.argv[1]
        generate_understanding_graph(conversation_file, output_dir)
    else:
        # Generate for all conversations
        for i in range(1, 11):
            json_file = Path(output_dir) / f"sample_conversation_{i:02d}.json"
            if json_file.exists():
                print(f"\nGenerating understanding graph for conversation {i}...")
                generate_understanding_graph(str(json_file), output_dir)
        
        print("\n[OK] All understanding graphs generated!")

