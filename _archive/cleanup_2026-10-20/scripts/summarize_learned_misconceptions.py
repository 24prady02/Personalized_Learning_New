"""
Summarize all misconceptions learned at each turn across all conversations
"""

import json
from pathlib import Path
from collections import defaultdict

def summarize_misconceptions():
    """Extract and summarize all misconceptions learned from conversations"""
    
    output_dir = Path("output")
    conversations = []
    
    # Load all conversation JSON files
    for i in range(1, 11):
        json_file = output_dir / f"sample_conversation_{i:02d}.json"
        if json_file.exists():
            with open(json_file, 'r', encoding='utf-8') as f:
                conversations.append(json.load(f))
    
    print("=" * 80)
    print("MISCONCEPTIONS LEARNED FROM STUDENT CONVERSATIONS")
    print("=" * 80)
    print()
    
    all_misconceptions = defaultdict(list)  # misconception_id -> list of (conversation, turn, details)
    
    for conv_idx, conversation in enumerate(conversations, 1):
        student_id = conversation.get('student_id', f'student_sample_{conv_idx:02d}')
        turns = conversation.get('turns', [])
        
        print(f"CONVERSATION {conv_idx}: {student_id}")
        print("-" * 80)
        
        for turn in turns:
            turn_num = turn.get('turn_number', 0)
            student_input = turn.get('student_input', {})
            question = student_input.get('question', '')
            error = student_input.get('error_message', '')
            code = student_input.get('code', '')
            
            system_analysis = turn.get('system_analysis', {})
            learned_misconceptions = system_analysis.get('learned_misconceptions', [])
            
            if learned_misconceptions:
                print(f"\n  TURN {turn_num}:")
                print(f"    Student Question: {question[:80]}...")
                if error:
                    print(f"    Error: {error}")
                
                for mc_idx, mc in enumerate(learned_misconceptions, 1):
                    mc_id = mc.get('id', 'unknown')
                    concept = mc.get('concept', 'unknown')
                    error_type = mc.get('error_type', 'N/A')
                    description = mc.get('description', 'N/A')
                    severity = mc.get('severity', 'medium')
                    frequency = mc.get('frequency', 0.0)
                    
                    print(f"\n    [MISCONCEPTION {mc_idx}]: {mc_id}")
                    print(f"       Concept: {concept}")
                    print(f"       Error Type: {error_type}")
                    print(f"       Description: {description}")
                    print(f"       Severity: {severity}")
                    print(f"       Frequency: {frequency:.2f}")
                    
                    # Store for summary
                    all_misconceptions[mc_id].append({
                        'conversation': conv_idx,
                        'turn': turn_num,
                        'student_id': student_id,
                        'concept': concept,
                        'error_type': error_type,
                        'question': question,
                        'error': error,
                        'severity': severity,
                        'frequency': frequency
                    })
            else:
                # Check if there's an error but no misconception extracted
                if error:
                    print(f"\n  TURN {turn_num}:")
                    print(f"    Student Question: {question[:80]}...")
                    print(f"    Error: {error}")
                    print(f"    [WARN] No misconception extracted (should infer from error)")
        
        print()
        print("=" * 80)
        print()
    
    # Summary statistics
    print("\n" + "=" * 80)
    print("SUMMARY STATISTICS")
    print("=" * 80)
    print(f"\nTotal Unique Misconceptions Learned: {len(all_misconceptions)}")
    print(f"Total Misconception Occurrences: {sum(len(v) for v in all_misconceptions.values())}")
    
    print("\nMost Frequently Learned Misconceptions:")
    sorted_mcs = sorted(all_misconceptions.items(), key=lambda x: len(x[1]), reverse=True)
    for mc_id, occurrences in sorted_mcs[:10]:
        print(f"  {mc_id}: {len(occurrences)} occurrence(s)")
        for occ in occurrences[:3]:  # Show first 3 occurrences
            print(f"    - Conversation {occ['conversation']}, Turn {occ['turn']}: {occ['error_type']} in {occ['concept']}")
    
    print("\nMisconceptions by Concept:")
    concept_counts = defaultdict(int)
    for mc_id, occurrences in all_misconceptions.items():
        if occurrences:
            concept = occurrences[0]['concept']
            concept_counts[concept] += len(occurrences)
    
    for concept, count in sorted(concept_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  {concept}: {count} misconception(s)")
    
    print("\nMisconceptions by Error Type:")
    error_counts = defaultdict(int)
    for mc_id, occurrences in all_misconceptions.items():
        for occ in occurrences:
            error_type = occ['error_type']
            if error_type != 'N/A':
                error_counts[error_type] += 1
    
    for error_type, count in sorted(error_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  {error_type}: {count} occurrence(s)")
    
    # Save detailed summary
    summary_file = output_dir / "misconceptions_summary.json"
    summary_data = {
        'total_unique_misconceptions': len(all_misconceptions),
        'total_occurrences': sum(len(v) for v in all_misconceptions.values()),
        'misconceptions': {
            mc_id: {
                'id': mc_id,
                'concept': occurrences[0]['concept'] if occurrences else 'unknown',
                'error_type': occurrences[0]['error_type'] if occurrences else 'N/A',
                'total_occurrences': len(occurrences),
                'occurrences': occurrences
            }
            for mc_id, occurrences in all_misconceptions.items()
        }
    }
    
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(summary_data, f, indent=2, default=str)
    
    print(f"\n[OK] Detailed summary saved to: {summary_file}")

if __name__ == "__main__":
    summarize_misconceptions()

