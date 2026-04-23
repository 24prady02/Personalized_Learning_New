"""
Regenerate all 10 sample conversations with Groq API responses
Uses the new API key and ensures all conversations have proper Groq outputs
"""

import yaml
import os
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List
import torch

from generate_multi_turn_conversation import MultiTurnConversationGenerator
from generate_10_sample_conversations import STUDENT_SCENARIOS
import random


def regenerate_all_conversations():
    """Regenerate all 10 conversations with Groq API"""
    
    print("=" * 80)
    print("REGENERATING ALL 10 CONVERSATIONS WITH GROQ API")
    print("=" * 80)
    
    # Get API key from environment variable (user should set this)
    groq_api_key = os.getenv('GROQ_API_KEY', '')
    if not groq_api_key:
        print("[ERROR] GROQ_API_KEY environment variable not set!")
        print("[INFO] Please set it using: set GROQ_API_KEY=your_api_key")
        return
    
    # Also update config.yaml (but don't commit the key)
    config_path = "config.yaml"
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        if 'groq' not in config:
            config['groq'] = {}
        # Only update if not already set (to avoid overwriting)
        if not config['groq'].get('api_key'):
            config['groq']['api_key'] = groq_api_key
        
        with open(config_path, 'w') as f:
            yaml.dump(config, f, default_flow_style=False)
    
    print("[OK] Updated config.yaml with new Groq API key")
    
    # Initialize generator (will use new API key)
    print("\n[1] Initializing conversation generator...")
    generator = MultiTurnConversationGenerator()
    
    # Verify Groq client is initialized
    if generator.groq_client is None:
        print("[ERROR] Groq client not initialized! Check API key.")
        return
    
    print("[OK] Groq client initialized successfully")
    
    # Select 10 scenarios
    selected_scenarios = random.sample(STUDENT_SCENARIOS, min(10, len(STUDENT_SCENARIOS)))
    while len(selected_scenarios) < 10:
        selected_scenarios.append(random.choice(STUDENT_SCENARIOS))
    
    successful = 0
    failed = 0
    
    for i, scenario in enumerate(selected_scenarios[:10], 1):
        print(f"\n{'='*80}")
        print(f"REGENERATING CONVERSATION {i}/10: {scenario['problem_type']}")
        print(f"{'='*80}")
        
        # Prepare turns
        turns = []
        for j, turn_data in enumerate(scenario['turns'], 1):
            turns.append({
                "turn_number": j,
                **turn_data
            })
        
        # Generate conversation
        student_id = f"student_sample_{i:02d}"
        output_file = f"output/sample_conversation_{i:02d}"
        
        try:
            print(f"\n[2] Generating conversation for {student_id}...")
            conversation = generator.generate_conversation(
                student_id=student_id,
                conversation_turns=turns,
                output_file=output_file
            )
            
            # Verify Groq responses were generated
            all_have_responses = True
            for turn in conversation.get('turns', []):
                response = turn.get('system_response', {})
                response_text = response.get('response_text', '')
                if not response_text or response_text.startswith('[PLACEHOLDER]') or response_text.startswith('[Error'):
                    all_have_responses = False
                    print(f"[WARN] Turn {turn.get('turn_number')} missing Groq response")
            
            if all_have_responses:
                print(f"[OK] Conversation {i} generated successfully with Groq responses")
                successful += 1
            else:
                print(f"[WARN] Conversation {i} generated but some turns missing Groq responses")
                failed += 1
                
        except Exception as e:
            print(f"[ERROR] Failed to generate conversation {i}: {e}")
            import traceback
            traceback.print_exc()
            failed += 1
    
    print("\n" + "=" * 80)
    print("REGENERATION SUMMARY")
    print("=" * 80)
    print(f"Successful: {successful}/10")
    print(f"Failed: {failed}/10")
    print(f"\nAll conversations saved to: output/sample_conversation_*.md")
    print("=" * 80)


if __name__ == "__main__":
    regenerate_all_conversations()

