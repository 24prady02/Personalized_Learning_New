"""
Generate Example Conversation with Nood
Demonstrates step-by-step explanations for a student missing prerequisites
"""

import yaml
import os
import json
from pathlib import Path
from datetime import datetime
from src.orchestrator.orchestrator import InterventionOrchestrator
from src.models.hvsae.model import HVSAE
import torch

def generate_conversation_turn(orchestrator, turn_number, student_id, question, code=None, error_message=None, conversation_history=None):
    """Generate a single conversation turn"""
    
    print(f"\n{'='*80}")
    print(f"TURN {turn_number}: {student_id}")
    print(f"{'='*80}")
    
    # Build session data
    session_data = {
        "student_id": student_id,
        "question": question,
        "conversation": conversation_history or [],
        "action_sequence": ["ask_question"],
        "time_deltas": [10.0],
        "time_stuck": 0.0
    }
    
    if code:
        session_data["code"] = code
    if error_message:
        session_data["error_message"] = error_message
    
    # Process session
    result = orchestrator.process_session(session_data)
    
    # Extract response
    response = result['content'].get('text', '')
    metrics = result['content'].get('metrics', {})
    adaptive_analysis = result['content'].get('adaptive_analysis', {})
    
    # Format output
    turn_output = {
        "turn_number": turn_number,
        "student_id": student_id,
        "timestamp": datetime.now().isoformat(),
        "student_input": {
            "question": question,
            "code": code,
            "error_message": error_message
        },
        "system_analysis": {
            "dina_mastery": metrics.get('quantitative', {}).get('dina_mastery', {}).get('overall_mastery', 0.0),
            "strategy": adaptive_analysis.get('strategy', 'unknown'),
            "complexity": adaptive_analysis.get('complexity', 0),
            "knowledge_gaps": adaptive_analysis.get('knowledge_gaps', []),
            "prerequisites": adaptive_analysis.get('prerequisites', []),
            "cognitive_state": metrics.get('qualitative', {}).get('cognitive_state', 'unknown'),
            "knowledge_graphs_used": metrics.get('quantitative', {}).get('knowledge_graphs_used', {})
        },
        "generated_response": response,
        "response_length": len(response),
        "metrics": metrics
    }
    
    # Display
    print(f"\n📝 STUDENT QUESTION:")
    print(f"{question}")
    if code:
        print(f"\n💻 CODE:")
        print(f"{code}")
    if error_message:
        print(f"\n❌ ERROR:")
        print(f"{error_message}")
    
    print(f"\n🤖 SYSTEM ANALYSIS:")
    print(f"  DINA Mastery: {turn_output['system_analysis']['dina_mastery']:.2%}")
    print(f"  Strategy: {turn_output['system_analysis']['strategy']}")
    print(f"  Complexity: {turn_output['system_analysis']['complexity']}")
    print(f"  Cognitive State: {turn_output['system_analysis']['cognitive_state']}")
    print(f"  Knowledge Gaps: {len(turn_output['system_analysis']['knowledge_gaps'])}")
    
    print(f"\n💬 GENERATED RESPONSE ({len(response)} chars):")
    print(f"{'-'*80}")
    print(response)
    print(f"{'-'*80}")
    
    return turn_output, result

def main():
    print("="*80)
    print("NOOD CONVERSATION GENERATOR")
    print("Demonstrating Step-by-Step Learning with Missing Prerequisites")
    print("="*80)
    
    # Set Groq API key
    groq_api_key = os.getenv('GROQ_API_KEY', '')
    if not groq_api_key:
        print("⚠️  WARNING: GROQ_API_KEY not set. Using placeholder.")
        groq_api_key = "your_key_here"
    os.environ['GROQ_API_KEY'] = groq_api_key
    
    # Load config
    config_path = Path("config.yaml")
    if config_path.exists():
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
    else:
        config = {
            'cse_kg': {
                'sparql_endpoint': 'http://w3id.org/cskg/sparql',
                'local_cache': True,
                'cache_dir': 'data/cse_kg_cache'
            },
            'pedagogical_kg': {'enabled': True},
            'coke': {'enabled': True},
            'hvsae': {},
            'groq': {'api_key': groq_api_key},
            'reinforcement_learning': {},
            'orchestrator': {
                'priority_factors': {
                    'knowledge_gap': 0.3,
                    'emotional_state': 0.2,
                    'time_stuck': 0.1
                },
                'intervention_threshold': 0.5
            }
        }
    
    # Initialize models
    print("\n[1] Initializing Models...")
    models = {}
    
    try:
        models['hvsae'] = HVSAE(config)
        print("  [OK] HVSAE initialized")
    except Exception as e:
        print(f"  [WARN] HVSAE failed: {e}")
        models['hvsae'] = None
    
    # Initialize Orchestrator
    print("\n[2] Initializing Orchestrator...")
    orchestrator = InterventionOrchestrator(config, models, use_rl=True, use_hierarchical_rl=False)
    
    # Student profile: Nood
    student_id = "nood_001"
    conversation_history = []
    all_turns = []
    
    # ===== TURN 1: Initial Question =====
    print("\n" + "="*80)
    print("STARTING CONVERSATION WITH NOOD")
    print("="*80)
    
    turn1, result1 = generate_conversation_turn(
        orchestrator=orchestrator,
        turn_number=1,
        student_id=student_id,
        question="I'm trying to write a function that calculates factorial, but I keep getting an error. Here's my code:\n\ndef factorial(n):\n    return n * factorial(n - 1)\n\nError: RecursionError: maximum recursion depth exceeded\n\nCan you help me understand what's wrong?",
        code="def factorial(n):\n    return n * factorial(n - 1)",
        error_message="RecursionError: maximum recursion depth exceeded",
        conversation_history=conversation_history
    )
    all_turns.append(turn1)
    conversation_history.append(turn1['student_input']['question'])
    conversation_history.append(turn1['generated_response'])
    
    # ===== TURN 2: About Base Cases =====
    turn2, result2 = generate_conversation_turn(
        orchestrator=orchestrator,
        turn_number=2,
        student_id=student_id,
        question="I think I understand the base case part, but I'm confused about how the function calls itself. When factorial(3) calls factorial(2), how does it 'remember' to multiply by 3 later? Does it just wait?",
        conversation_history=conversation_history
    )
    all_turns.append(turn2)
    conversation_history.append(turn2['student_input']['question'])
    conversation_history.append(turn2['generated_response'])
    
    # ===== TURN 3: About Return Statements =====
    turn3, result3 = generate_conversation_turn(
        orchestrator=orchestrator,
        turn_number=3,
        student_id=student_id,
        question="Okay, I think I get the stack part now. But I'm still confused about the return statement. In the code:\n\ndef factorial(n):\n    if n <= 1:\n        return 1\n    return n * factorial(n - 1)\n\nWhen we do `return n * factorial(n - 1)`, what exactly is being returned? Is it the number n, or the result of factorial(n - 1), or both multiplied together?",
        code="def factorial(n):\n    if n <= 1:\n        return 1\n    return n * factorial(n - 1)",
        conversation_history=conversation_history
    )
    all_turns.append(turn3)
    conversation_history.append(turn3['student_input']['question'])
    conversation_history.append(turn3['generated_response'])
    
    # ===== TURN 4: Student Tries It =====
    turn4, result4 = generate_conversation_turn(
        orchestrator=orchestrator,
        turn_number=4,
        student_id=student_id,
        question="I tried to write it myself! Does this work? I used `n == 0` instead of `n <= 1`. Is that okay?",
        code="def factorial(n):\n    if n == 0:\n        return 1\n    return n * factorial(n - 1)",
        conversation_history=conversation_history
    )
    all_turns.append(turn4)
    conversation_history.append(turn4['student_input']['question'])
    conversation_history.append(turn4['generated_response'])
    
    # ===== TURN 5: About Efficiency =====
    turn5, result5 = generate_conversation_turn(
        orchestrator=orchestrator,
        turn_number=5,
        student_id=student_id,
        question="Thanks! One more question - is recursion the best way to do factorial? I've seen people use loops. Which is better?",
        conversation_history=conversation_history
    )
    all_turns.append(turn5)
    conversation_history.append(turn5['student_input']['question'])
    conversation_history.append(turn5['generated_response'])
    
    # ===== SAVE COMPLETE CONVERSATION =====
    output_dir = Path("test_output")
    output_dir.mkdir(exist_ok=True)
    
    output_file = output_dir / f"nood_conversation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    conversation_output = {
        "student_id": student_id,
        "conversation_date": datetime.now().isoformat(),
        "total_turns": len(all_turns),
        "turns": all_turns,
        "summary": {
            "initial_mastery": all_turns[0]['system_analysis']['dina_mastery'],
            "final_mastery": all_turns[-1]['system_analysis']['dina_mastery'],
            "mastery_improvement": all_turns[-1]['system_analysis']['dina_mastery'] - all_turns[0]['system_analysis']['dina_mastery'],
            "total_responses": len(all_turns),
            "average_response_length": sum(t['response_length'] for t in all_turns) / len(all_turns)
        }
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(conversation_output, f, indent=2, default=str, ensure_ascii=False)
    
    # ===== DISPLAY SUMMARY =====
    print("\n" + "="*80)
    print("CONVERSATION SUMMARY")
    print("="*80)
    print(f"\nStudent: {student_id}")
    print(f"Total Turns: {len(all_turns)}")
    print(f"\nMastery Progression:")
    for i, turn in enumerate(all_turns, 1):
        print(f"  Turn {i}: {turn['system_analysis']['dina_mastery']:.2%} "
              f"(Strategy: {turn['system_analysis']['strategy']}, "
              f"Complexity: {turn['system_analysis']['complexity']})")
    
    print(f"\nInitial Mastery: {conversation_output['summary']['initial_mastery']:.2%}")
    print(f"Final Mastery: {conversation_output['summary']['final_mastery']:.2%}")
    print(f"Improvement: {conversation_output['summary']['mastery_improvement']:+.2%}")
    print(f"\nAverage Response Length: {conversation_output['summary']['average_response_length']:.0f} characters")
    
    print(f"\n✅ Complete conversation saved to: {output_file}")
    print("="*80)
    
    # ===== GENERATE MARKDOWN DOCUMENTATION =====
    md_file = output_dir / f"nood_conversation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    
    with open(md_file, 'w', encoding='utf-8') as f:
        f.write(f"# Conversation with {student_id}\n\n")
        f.write(f"**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"**Total Turns**: {len(all_turns)}\n\n")
        f.write("---\n\n")
        
        for turn in all_turns:
            f.write(f"## Turn {turn['turn_number']}\n\n")
            f.write(f"### Student Question\n\n")
            f.write(f"{turn['student_input']['question']}\n\n")
            
            if turn['student_input'].get('code'):
                f.write(f"### Code\n\n```python\n{turn['student_input']['code']}\n```\n\n")
            
            if turn['student_input'].get('error_message'):
                f.write(f"### Error\n\n```\n{turn['student_input']['error_message']}\n```\n\n")
            
            f.write(f"### System Analysis\n\n")
            f.write(f"- **DINA Mastery**: {turn['system_analysis']['dina_mastery']:.2%}\n")
            f.write(f"- **Strategy**: {turn['system_analysis']['strategy']}\n")
            f.write(f"- **Complexity**: {turn['system_analysis']['complexity']}\n")
            f.write(f"- **Cognitive State**: {turn['system_analysis']['cognitive_state']}\n")
            f.write(f"- **Knowledge Gaps**: {len(turn['system_analysis']['knowledge_gaps'])}\n")
            f.write(f"- **Prerequisites**: {len(turn['system_analysis']['prerequisites'])}\n")
            
            kgs = turn['system_analysis']['knowledge_graphs_used']
            f.write(f"\n**Knowledge Graphs Used**:\n")
            for kg, used in kgs.items():
                f.write(f"- {kg.upper()}: {'✓' if used else '✗'}\n")
            
            f.write(f"\n### Generated Response\n\n")
            f.write(f"{turn['generated_response']}\n\n")
            f.write("---\n\n")
        
        f.write(f"## Summary\n\n")
        f.write(f"- **Initial Mastery**: {conversation_output['summary']['initial_mastery']:.2%}\n")
        f.write(f"- **Final Mastery**: {conversation_output['summary']['final_mastery']:.2%}\n")
        f.write(f"- **Improvement**: {conversation_output['summary']['mastery_improvement']:+.2%}\n")
    
    print(f"✅ Markdown documentation saved to: {md_file}")
    
    return conversation_output

if __name__ == "__main__":
    result = main()











