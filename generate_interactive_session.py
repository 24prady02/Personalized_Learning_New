"""
Generate an interactive session that shows student graph updates and metrics progression
"""

import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict

def generate_interactive_session(conversation_file: str):
    """Generate an interactive session view showing progression"""
    
    # Load conversation
    with open(conversation_file, 'r', encoding='utf-8') as f:
        conversation = json.load(f)
    
    student_id = conversation.get('student_id', 'unknown')
    turns = conversation.get('turns', [])
    
    output_lines = []
    output_lines.append("# Interactive Session: Student Graph Updates & Metrics Progression")
    output_lines.append("")
    output_lines.append(f"**Student ID**: `{student_id}`")
    output_lines.append(f"**Total Turns**: {len(turns)}")
    output_lines.append(f"**Generated**: {datetime.now().isoformat()}")
    output_lines.append("")
    output_lines.append("---")
    output_lines.append("")
    
    # Track progression
    concept_mastery_history = defaultdict(list)
    error_history = []
    misconception_history = []
    metrics_history = []
    
    for turn_num, turn in enumerate(turns, 1):
        output_lines.append(f"## 🔄 TURN {turn_num}")
        output_lines.append("")
        
        student_input = turn.get('student_input', {})
        question = student_input.get('question', '')
        error = student_input.get('error_message', '')
        code = student_input.get('code', '')
        
        system_analysis = turn.get('system_analysis', {})
        student_graph = system_analysis.get('student_graph', {})
        learned_misconceptions = system_analysis.get('learned_misconceptions', [])
        knowledge_gaps = system_analysis.get('knowledge_gaps', [])
        metrics = turn.get('metrics', {})
        
        # Student Input
        output_lines.append("### 📥 Student Input")
        output_lines.append("")
        if question:
            output_lines.append(f"**Question**: {question}")
            output_lines.append("")
        if error:
            output_lines.append(f"**Error**: `{error[:200]}`")
            error_history.append({
                'turn': turn_num,
                'error': error,
                'timestamp': turn.get('timestamp', '')
            })
            output_lines.append("")
        if code:
            output_lines.append("**Code**:")
            output_lines.append("```python")
            output_lines.append(code[:300])
            output_lines.append("```")
            output_lines.append("")
        
        output_lines.append("---")
        output_lines.append("")
        
        # Student Graph Updates
        output_lines.append("### 📊 Student Graph Updates")
        output_lines.append("")
        
        concept_mastery = student_graph.get('concept_mastery', {})
        previous_mastery = {}
        if turn_num > 1:
            # Get previous turn's mastery
            prev_turn = turns[turn_num - 2]
            prev_graph = prev_turn.get('system_analysis', {}).get('student_graph', {})
            previous_mastery = prev_graph.get('concept_mastery', {})
        
        # Show concept updates
        if concept_mastery:
            output_lines.append("**Concept Mastery Updates:**")
            output_lines.append("")
            
            for concept, mastery in concept_mastery.items():
                prev_mastery = previous_mastery.get(concept, 0.0)
                delta = mastery - prev_mastery
                
                if concept not in previous_mastery:
                    status = "🆕 NEW"
                elif delta > 0.1:
                    status = "📈 IMPROVED"
                elif delta < -0.1:
                    status = "📉 DECLINED"
                else:
                    status = "➡️ STABLE"
                
                mastery_bar = "█" * int(mastery * 20) + "░" * (20 - int(mastery * 20))
                
                output_lines.append(f"#### `{concept}`")
                output_lines.append(f"- **Current Mastery**: {mastery:.2f} {mastery_bar}")
                if concept in previous_mastery:
                    output_lines.append(f"- **Previous Mastery**: {prev_mastery:.2f}")
                    output_lines.append(f"- **Change**: {delta:+.2f} ({status})")
                else:
                    output_lines.append(f"- **Status**: {status}")
                output_lines.append("")
                
                # Track history
                concept_mastery_history[concept].append({
                    'turn': turn_num,
                    'mastery': mastery,
                    'delta': delta
                })
        
        # Show errors and their impact
        if error:
            output_lines.append("**Error Impact on Student Graph:**")
            output_lines.append("")
            output_lines.append(f"- **Error Type**: `{error.split(':')[0] if ':' in error else error[:50]}`")
            
            # Find related concepts
            related_concepts = []
            if "RecursionError" in error:
                related_concepts.append("recursion")
            elif "IndexError" in error:
                related_concepts.append("arrays")
            elif "KeyError" in error:
                related_concepts.append("dictionaries")
            elif "TypeError" in error:
                related_concepts.append("type_system")
            
            if related_concepts:
                output_lines.append(f"- **Affected Concepts**: {', '.join(related_concepts)}")
                for concept in related_concepts:
                    if concept in concept_mastery:
                        mastery = concept_mastery[concept]
                        output_lines.append(f"  - `{concept}`: Mastery = {mastery:.2f}")
            
            if learned_misconceptions:
                output_lines.append(f"- **Misconceptions Learned**: {len(learned_misconceptions)}")
                for mc in learned_misconceptions:
                    output_lines.append(f"  - `{mc.get('id', 'unknown')}` for concept `{mc.get('concept', 'unknown')}`")
            output_lines.append("")
        
        # Show misconceptions learned
        if learned_misconceptions:
            output_lines.append("**Misconceptions Learned This Turn:**")
            output_lines.append("")
            for mc in learned_misconceptions:
                output_lines.append(f"- **{mc.get('id', 'unknown')}**")
                output_lines.append(f"  - Concept: `{mc.get('concept', 'unknown')}`")
                output_lines.append(f"  - Error Type: `{mc.get('error_type', 'N/A')}`")
                output_lines.append(f"  - Severity: `{mc.get('severity', 'medium')}`")
                output_lines.append(f"  - Frequency: `{mc.get('frequency', 0):.2f}`")
                misconception_history.append({
                    'turn': turn_num,
                    'misconception': mc.get('id', 'unknown'),
                    'concept': mc.get('concept', 'unknown'),
                    'error_type': mc.get('error_type', 'N/A')
                })
            output_lines.append("")
        
        # Show knowledge gaps
        if knowledge_gaps:
            output_lines.append("**Knowledge Gaps Identified:**")
            output_lines.append("")
            for gap in knowledge_gaps[:5]:  # Show first 5
                concept = gap.get('concept', 'unknown')
                mastery = gap.get('mastery', 0.0)
                severity = gap.get('severity', 'medium')
                output_lines.append(f"- `{concept}`: Mastery = {mastery:.2f}, Severity = {severity}")
            if len(knowledge_gaps) > 5:
                output_lines.append(f"- ... and {len(knowledge_gaps) - 5} more gaps")
            output_lines.append("")
        
        # Show metrics
        if metrics:
            output_lines.append("### 📈 Metrics This Turn")
            output_lines.append("")
            
            quantitative = metrics.get('quantitative', {})
            if quantitative:
                # DINA Mastery
                dina = quantitative.get('dina_mastery', {})
                if dina:
                    overall = dina.get('overall_mastery', 0.0)
                    delta = dina.get('mastery_delta', 0.0)
                    output_lines.append("**DINA Mastery Model:**")
                    output_lines.append(f"- Overall Mastery: {overall:.2f}")
                    if delta != 0:
                        output_lines.append(f"- Mastery Delta: {delta:+.2f} ({'📈 Improved' if delta > 0 else '📉 Declined' if delta < 0 else '➡️ Stable'})")
                    output_lines.append("")
                
                # CodeBERT
                codebert = quantitative.get('codebert_analysis', {})
                if codebert:
                    correctness = codebert.get('correctness_score', 0.0)
                    syntax_errors = codebert.get('syntax_errors', 0.0)
                    logic_errors = codebert.get('logic_errors', 0.0)
                    quality = codebert.get('code_quality', 'unknown')
                    output_lines.append("**CodeBERT Analysis:**")
                    output_lines.append(f"- Correctness Score: {correctness:.2f}")
                    output_lines.append(f"- Syntax Errors: {syntax_errors:.2f}")
                    output_lines.append(f"- Logic Errors: {logic_errors:.2f}")
                    output_lines.append(f"- Code Quality: {quality}")
                    output_lines.append("")
                
                # Time Tracking
                time_tracking = quantitative.get('time_tracking', {})
                if time_tracking:
                    duration = time_tracking.get('turn_duration_seconds', 0.0)
                    stuck = time_tracking.get('time_stuck_seconds', 0.0)
                    output_lines.append("**Time Tracking:**")
                    output_lines.append(f"- Turn Duration: {duration:.1f} seconds")
                    output_lines.append(f"- Time Stuck: {stuck:.1f} seconds")
                    if duration > 0:
                        stuck_percentage = (stuck / duration) * 100
                        output_lines.append(f"- Stuck Percentage: {stuck_percentage:.1f}%")
                    output_lines.append("")
                
                # COKE Analysis
                coke = quantitative.get('coke_analysis', {})
                if coke:
                    cognitive_state = coke.get('cognitive_state', 'unknown')
                    confidence = coke.get('confidence', 0.0)
                    behavioral = coke.get('behavioral_response', 'unknown')
                    output_lines.append("**COKE Cognitive Analysis:**")
                    output_lines.append(f"- Cognitive State: `{cognitive_state}`")
                    output_lines.append(f"- Confidence: {confidence:.2f}")
                    output_lines.append(f"- Behavioral Response: `{behavioral}`")
                    output_lines.append("")
            
            # Track metrics
            metrics_history.append({
                'turn': turn_num,
                'overall_mastery': dina.get('overall_mastery', 0.0) if dina else 0.0,
                'correctness': codebert.get('correctness_score', 0.0) if codebert else 0.0,
                'duration': time_tracking.get('turn_duration_seconds', 0.0) if time_tracking else 0.0,
                'cognitive_state': coke.get('cognitive_state', 'unknown') if coke else 'unknown'
            })
        
        output_lines.append("---")
        output_lines.append("")
    
    # Summary Section
    output_lines.append("## 📊 Session Summary")
    output_lines.append("")
    
    # Concept Mastery Progression
    if concept_mastery_history:
        output_lines.append("### Concept Mastery Progression")
        output_lines.append("")
        for concept, history in concept_mastery_history.items():
            output_lines.append(f"#### `{concept}`")
            output_lines.append("")
            output_lines.append("| Turn | Mastery | Change |")
            output_lines.append("|------|---------|--------|")
            for entry in history:
                delta_str = f"{entry['delta']:+.2f}" if entry['delta'] != 0 else "0.00"
                output_lines.append(f"| {entry['turn']} | {entry['mastery']:.2f} | {delta_str} |")
            output_lines.append("")
    
    # Error Summary
    if error_history:
        output_lines.append("### Errors Encountered")
        output_lines.append("")
        output_lines.append("| Turn | Error Type |")
        output_lines.append("|------|------------|")
        for entry in error_history:
            error_type = entry['error'].split(':')[0] if ':' in entry['error'] else entry['error'][:30]
            output_lines.append(f"| {entry['turn']} | `{error_type}` |")
        output_lines.append("")
    
    # Misconception Summary
    if misconception_history:
        output_lines.append("### Misconceptions Learned")
        output_lines.append("")
        output_lines.append("| Turn | Misconception | Concept | Error Type |")
        output_lines.append("|------|---------------|---------|-----------|")
        for entry in misconception_history:
            output_lines.append(f"| {entry['turn']} | `{entry['misconception']}` | `{entry['concept']}` | `{entry['error_type']}` |")
        output_lines.append("")
    
    # Metrics Summary
    if metrics_history:
        output_lines.append("### Metrics Progression")
        output_lines.append("")
        output_lines.append("| Turn | Overall Mastery | Correctness | Duration (s) | Cognitive State |")
        output_lines.append("|------|-----------------|-------------|--------------|-----------------|")
        for entry in metrics_history:
            output_lines.append(f"| {entry['turn']} | {entry['overall_mastery']:.2f} | {entry['correctness']:.2f} | {entry['duration']:.1f} | `{entry['cognitive_state']}` |")
        output_lines.append("")
    
    # Save output
    output_file = Path(conversation_file).parent / f"interactive_session_{Path(conversation_file).stem}.md"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(output_lines))
    
    print(f"[OK] Interactive session saved to: {output_file}")
    return output_file

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        conversation_file = sys.argv[1]
    else:
        # Generate for all conversations
        output_dir = Path("output")
        for i in range(1, 11):
            json_file = output_dir / f"sample_conversation_{i:02d}.json"
            if json_file.exists():
                print(f"\nGenerating interactive session for conversation {i}...")
                generate_interactive_session(str(json_file))
        
        print("\n[OK] All interactive sessions generated!")

