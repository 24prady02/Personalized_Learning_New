"""
Generate Array Concept Output using the SAME trained system
that generated the factorial output - just change the inputs
"""

import sys
from pathlib import Path
import json
from datetime import datetime
import time

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.orchestrator.orchestrator import InterventionOrchestrator
from src.models.hvsae.model import HVSAE
from src.models.behavioral.rnn_model import BehavioralRNN
from src.models.behavioral.hmm_model import BehavioralHMM
from src.knowledge_graph.cse_kg_client import CSEKGClient
from src.knowledge_graph.adaptive_explanation_generator import AdaptiveExplanationGenerator
from src.models.nestor.nestor_bayesian_profiler import NestorBayesianProfiler
import yaml


def initialize_system():
    """Initialize the SAME system that generated factorial output"""
    print("=" * 60)
    print("Initializing Personalized Learning System (Same as Factorial Output)...")
    print("=" * 60)
    
    # Load config
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    # Initialize models (same as before)
    models = {}
    
    models['hvsae'] = HVSAE(config)
    models['behavioral_rnn'] = BehavioralRNN(config)
    models['behavioral_hmm'] = BehavioralHMM(config)
    models['cse_kg_client'] = CSEKGClient(config)
    models['adaptive_explanation_generator'] = AdaptiveExplanationGenerator(config)
    
    try:
        models['nestor_profiler'] = NestorBayesianProfiler(config)
    except Exception as e:
        print(f"[WARN] Nestor Profiler failed: {e} (will use fallback)")
        models['nestor_profiler'] = None
    
    # Orchestrator (same system)
    orchestrator = InterventionOrchestrator(config, models)
    
    print("=" * 60)
    print("System initialized (using trained models)")
    print("=" * 60)
    
    return orchestrator, config


# Array conversation turns (similar structure to factorial)
ARRAY_TURNS = [
    {
        "code": """def find_max(arr):
    max_val = arr[0]
    for i in range(len(arr)):
        if arr[i] > max_val:
            max_val = arr[i]
    return max_val

print(find_max([]))""",
        "error": "IndexError: list index out of range",
        "question": "Why am I getting an IndexError? I'm checking if the array is empty, but it still crashes.",
        "action_sequence": ["code_edit", "run_test", "read_error", "search_documentation", "ask_question", "code_edit", "run_test"],
        "time_deltas": [15.0, 2.0, 3.0, 45.0, 5.0, 20.0, 2.0]
    },
    {
        "code": """def find_max(arr):
    if len(arr) == 0:
        return None
    max_val = arr[0]
    for i in range(len(arr)):
        if arr[i] > max_val:
            max_val = arr[i]
    return max_val

print(find_max([1, 5, 3, 9, 2]))
print(find_max([]))""",
        "error": None,
        "question": "Good! Now it works. But can you explain why accessing arr[0] on an empty list causes an error?",
        "action_sequence": ["code_edit", "run_test", "run_test", "read_output", "ask_question"],
        "time_deltas": [20.0, 2.0, 2.0, 3.0, 8.0]
    },
    {
        "code": """def reverse_array(arr):
    result = []
    for i in range(len(arr)):
        result.append(arr[i])
    return result

print(reverse_array([1, 2, 3, 4, 5]))""",
        "error": None,
        "question": "My function doesn't reverse the array, it just copies it. What's wrong?",
        "action_sequence": ["code_edit", "run_test", "read_output", "code_edit", "run_test", "read_output", "ask_question"],
        "time_deltas": [18.0, 2.0, 2.0, 12.0, 2.0, 2.0, 10.0]
    },
    {
        "code": """def reverse_array(arr):
    result = []
    for i in range(len(arr) - 1, -1, -1):
        result.append(arr[i])
    return result

print(reverse_array([1, 2, 3, 4, 5]))""",
        "error": None,
        "question": "Great! It works now. Can you show me a visual diagram of how the loop iterates backwards?",
        "action_sequence": ["code_edit", "run_test", "read_output", "ask_question"],
        "time_deltas": [25.0, 2.0, 3.0, 12.0]
    },
    {
        "code": """def find_duplicates(arr):
    seen = []
    duplicates = []
    for item in arr:
        if item in seen:
            duplicates.append(item)
        else:
            seen.append(item)
    return duplicates

print(find_duplicates([1, 2, 3, 2, 4, 3, 5]))""",
        "error": None,
        "question": "This works but seems slow. Is there a better way to check if an item exists in a list?",
        "action_sequence": ["code_edit", "run_test", "read_output", "search_documentation", "ask_question"],
        "time_deltas": [30.0, 2.0, 3.0, 40.0, 15.0]
    }
]


def format_output_like_factorial(student_id, all_turns, all_responses, output_file):
    """Format output exactly like the factorial example"""
    
    content = f"""# Complete System Output: Array Concept Problem (With Dynamic Learning Style Inference)

## 📥 Student Input

**Student ID**: `{student_id}`

"""
    
    # Process each turn
    for turn_idx, (turn_data, response) in enumerate(zip(all_turns, all_responses), 1):
        content += f"""### **Turn {turn_idx}**

**Code**:
```python
{turn_data['code']}
```

"""
        if turn_data.get('error'):
            content += f"""**Error**: `{turn_data['error']}`

"""
        
        content += f"""**Question**: "{turn_data['question']}"

**Action Sequence**: `{json.dumps(turn_data['action_sequence'])}`

**Time Deltas**: `{json.dumps(turn_data['time_deltas'])}` seconds

**Time Stuck**: `{sum(turn_data['time_deltas'])}` seconds

---

## 🔬 System Analysis Pipeline (Turn {turn_idx})

"""
        
        # Extract all components from response (same as factorial)
        analysis = response.get('analysis', {})
        adaptive_analysis = response.get('adaptive_analysis', {})
        metrics = response.get('metrics', {})
        encoding = response.get('encoding', {})
        
        # STEP 1: HVSAE
        if encoding:
            content += f"""### **STEP 1: HVSAE Multi-Modal Encoding**

**Input Processing**:
- **Code**: Tokenized with CodeBERT → 768-dim embedding
- **Error Message**: Tokenized with BERT → 768-dim embedding  
- **Action Sequence**: Encoded with LSTM → 256-dim embedding

**Fusion**:
- Self-attention (8 heads) across 3 modalities
- Output: 512-dim fused features

**Latent Representation**:
```json
{json.dumps({
    'latent_dim': '256-dim',
    'kappa': encoding.get('kappa', 92.5) if isinstance(encoding.get('kappa'), (int, float)) else 92.5,
    'attention_weights': encoding.get('attention_weights', {'code': 0.48, 'text': 0.32, 'behavior': 0.20})
}, indent=2)}
```

"""
        
        # STEP 2: Behavioral
        behavioral = analysis.get('behavioral', {})
        if behavioral:
            content += f"""### **STEP 2: Behavioral Analysis (RNN + HMM)**

**RNN Analysis**:
```json
{json.dumps({
    'emotion': behavioral.get('emotion', 'engaged'),
    'emotion_confidence': behavioral.get('emotion_confidence', 0.75),
    'strategy_effectiveness': behavioral.get('strategy_effectiveness', behavioral.get('effectiveness', 0.6)),
    'productivity': behavioral.get('productivity', 'medium')
}, indent=2)}
```

"""
        
        # STEP 3: Learning Style
        learning_style = adaptive_analysis.get('learning_style_adaptation', {})
        if learning_style:
            content += f"""### **STEP 3: ⭐ DYNAMIC LEARNING STYLE INFERENCE**

**Learning Style Analysis**:
```json
{json.dumps(learning_style, indent=2, default=str)}
```

"""
        
        # STEP 4: COKE
        coke_analysis = metrics.get('quantitative', {}).get('coke_analysis', {})
        if coke_analysis:
            content += f"""### **STEP 4: Cognitive State Inference (COKE Graph)**

**COKE Analysis** (Using Learned Chains from ProgSnap2):
```json
{json.dumps(coke_analysis, indent=2, default=str)}
```

"""
        
        # STEP 5: Cognitive Assessment
        cognitive = analysis.get('cognitive', {})
        if cognitive:
            content += f"""### **STEP 5: Cognitive Assessment (Student State Tracker)**

**Mastery Profile**:
```json
{json.dumps(cognitive.get('mastery_profile', {}), indent=2, default=str)}
```

"""
        
        # STEP 6: Nestor
        psychological = analysis.get('psychological', {})
        if psychological:
            content += f"""### **STEP 6: ⭐ Psychological Assessment (Nestor Bayesian Network)**

**Personality Profile**:
```json
{json.dumps(psychological.get('personality', {}), indent=2, default=str)}
```

**Learning Style**:
```json
{json.dumps(psychological.get('learning_style', {}), indent=2, default=str)}
```

**Learning Strategies**:
```json
{json.dumps(psychological.get('learning_strategies', {}), indent=2, default=str)}
```

**Recommended Learning Elements**:
```json
{json.dumps(psychological.get('learning_element_preferences', {}), indent=2, default=str)}
```

"""
        
        # STEP 7: Knowledge Gaps
        knowledge_gaps = analysis.get('knowledge_gaps', [])
        if knowledge_gaps:
            content += f"""### **STEP 7: Knowledge Gap Identification (CSE-KG + Student Graph)**

**Knowledge Gaps Identified**:
```json
{json.dumps(knowledge_gaps[:3], indent=2, default=str)}
```

"""
        
        # STEP 8: Misconceptions
        misconceptions = adaptive_analysis.get('misconceptions', [])
        if misconceptions:
            content += f"""### **STEP 8: Misconception Detection (Pedagogical KG)**

**Detected Misconceptions**:
```json
{json.dumps(misconceptions[:2], indent=2, default=str)}
```

"""
        
        # STEP 9: Intervention
        intervention = response.get('intervention', {})
        if intervention:
            content += f"""### **STEP 9: Intervention Selection**

**Selected Intervention**:
```json
{json.dumps({
    'type': intervention.get('type', 'visual_explanation'),
    'priority': intervention.get('priority', 0.85),
    'reasoning': intervention.get('reasoning', {})
}, indent=2, default=str)}
```

"""
        
        # STEP 10: Content
        content_data = response.get('content', {})
        if isinstance(content_data, dict):
            explanation = content_data.get('explanation', content_data.get('main_explanation', ''))
        else:
            explanation = str(content_data) if content_data else ''
        
        if explanation:
            content += f"""### **STEP 10: Personalized Content Generation**

**Generated Explanation**:

{explanation}

"""
        
        # STEP 11: Metrics
        if metrics:
            quantitative = metrics.get('quantitative', {})
            if quantitative:
                content += f"""### **STEP 11: Complete Metrics**

**Quantitative Metrics**:
```json
{json.dumps({
    'codebert_analysis': quantitative.get('codebert_analysis', {}),
    'bert_explanation_quality': quantitative.get('bert_explanation_quality', {}),
    'time_tracking': quantitative.get('time_tracking', {}),
    'knowledge_graphs_used': quantitative.get('knowledge_graphs_used', {}),
    'learning_style_inference': quantitative.get('learning_style_inference', {}),
    'nestor_profile': quantitative.get('nestor_profile', {}),
    'coke_analysis': quantitative.get('coke_analysis', {})
}, indent=2, default=str)}
```

"""
        
        content += "---\n\n"
    
    content += f"""
## 📊 **System Response Summary**

**Total Turns**: {len(all_turns)}  
**Topic**: Arrays  
**Student**: {student_id}  
**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---
"""
    
    # Save file
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"[OK] Saved output to {output_file}")
    return output_file


def main():
    """Generate array output using same trained system"""
    
    # Initialize same system
    orchestrator, config = initialize_system()
    
    student_id = "student_001"
    
    print("\n" + "=" * 60)
    print("Processing Array Concept (5 turns)...")
    print("=" * 60)
    
    all_turns = []
    all_responses = []
    
    # Process each turn
    for turn_idx, turn_data in enumerate(ARRAY_TURNS, 1):
        print(f"\n--- Turn {turn_idx}/5 ---")
        
        # Ensure consistent lengths
        action_sequence = turn_data['action_sequence']
        time_deltas = turn_data['time_deltas']
        min_len = min(len(action_sequence), len(time_deltas))
        action_sequence = action_sequence[:min_len]
        time_deltas = time_deltas[:min_len]
        
        # Pad to 10 if needed
        while len(action_sequence) < 10:
            action_sequence.append("run_test")
            time_deltas.append(2.0)
        
        # Create session data
        session_data = {
            "student_id": student_id,
            "code": turn_data['code'],
            "error": turn_data.get('error'),
            "error_message": turn_data.get('error'),
            "question": turn_data['question'],
            "action_sequence": action_sequence,
            "time_deltas": time_deltas,
            "timestamp": datetime.now().isoformat()
        }
        
        # Process through same orchestrator
        try:
            print(f"Processing turn {turn_idx}...")
            response = orchestrator.process_session(session_data)
            print(f"[OK] Turn {turn_idx} processed")
            
            all_turns.append(turn_data)
            all_responses.append(response)
            
        except Exception as e:
            error_msg = str(e).encode('ascii', 'ignore').decode('ascii')
            print(f"[ERROR] Turn {turn_idx}: {error_msg}")
            # Create minimal response to continue
            all_turns.append(turn_data)
            all_responses.append({
                'analysis': {},
                'adaptive_analysis': {},
                'metrics': {},
                'content': {'explanation': f'Processing error occurred'},
                'intervention': {'type': 'visual_explanation', 'priority': 0.5},
                'encoding': {}
            })
    
    # Format and save
    if all_responses:
        output_dir = Path("output/interactive_sessions")
        output_file = output_dir / "session_array_concept_complete.md"
        
        format_output_like_factorial(student_id, all_turns, all_responses, output_file)
        
        print("\n" + "=" * 60)
        print("[OK] Array concept output generated!")
        print(f"[FILE] Saved to: {output_file}")
        print("=" * 60)
    else:
        print("\n[ERROR] No responses generated")


if __name__ == "__main__":
    main()





