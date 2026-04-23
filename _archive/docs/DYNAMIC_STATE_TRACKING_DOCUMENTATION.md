# Dynamic State Tracking Documentation

## Overview

The system now **dynamically tracks and updates** student cognitive state and knowledge state from actual conversation and code interactions, rather than using static/default values.

## Key Changes

### 1. Student State Tracker

**File**: `src/orchestrator/student_state_tracker.py`

Tracks student state across sessions:
- **Cognitive State**: Inferred from conversation using COKE
- **Knowledge State**: Updated from code correctness and responses
- **Learning Progress**: Concept mastery over time
- **Conversation History**: Full interaction history

### 2. Dynamic Concept Extraction

**Location**: `src/orchestrator/orchestrator.py` and `src/knowledge_graph/adaptive_explanation_generator.py`

The system now:
- Extracts concepts **dynamically** from code, error messages, and conversation
- Uses CSE-KG to identify actual programming concepts
- Updates DINA mastery based on **actual performance**

### 3. Cognitive State Inference

**Location**: `src/orchestrator/orchestrator.py::_infer_cognitive_state_from_conversation()`

The system now:
- Uses COKE to infer cognitive state from conversation text
- Analyzes keywords and patterns in student messages
- Combines conversation analysis with behavioral data
- Updates state tracker with inferred cognitive state

### 4. Knowledge State Updates

**Location**: `src/orchestrator/orchestrator.py::process_session()`

After each session:
1. Extracts concepts from code/conversation
2. Infers cognitive state from conversation
3. Calculates code correctness
4. **Updates DINA mastery** based on actual performance
5. **Updates student state tracker** with new information

## How It Works

### Step 1: Session Processing

```python
session_data = {
    "student_id": "student_123",
    "code": "def factorial(n): return n * factorial(n-1)",
    "error_message": "RecursionError",
    "question": "Why isn't this working?",
    "conversation": ["I don't understand", "Help me"]
}
```

### Step 2: Dynamic Concept Extraction

```python
# System extracts concepts using CSE-KG
concepts = ["recursion", "base_case", "functions"]
```

### Step 3: Cognitive State Inference

```python
# COKE analyzes conversation
cognitive_state = "confused"  # From "I don't understand"
```

### Step 4: Code Correctness Analysis

```python
# CodeBERT analyzes code
code_correctness = 0.3  # Has error (missing base case)
```

### Step 5: State Update

```python
# Update student state
state_tracker.update_from_session(
    student_id="student_123",
    session_data=session_data,
    cognitive_state="confused",
    concepts_identified=["recursion", "base_case"],
    code_correctness=0.3,
    response_quality=0.8
)

# Update DINA mastery
dina_wrapper.update_mastery(
    student_id="student_123",
    concept="recursion",
    response_correct=False  # code_correctness < 0.7
)
```

### Step 6: Next Session

```python
# System retrieves updated state
state = state_tracker.get_student_state("student_123")

# Uses actual mastery scores
mastery = state['knowledge_state']['concept_mastery']
# {"recursion": 0.48, "base_case": 0.45, ...}

# Uses actual cognitive state
cognitive_state = state['cognitive_state']['current_state']
# "confused"
```

## State Persistence

Student states are saved to: `data/student_states.json`

Format:
```json
{
  "student_123": {
    "student_id": "student_123",
    "created_at": "2025-11-26T13:00:00",
    "last_updated": "2025-11-26T13:30:00",
    "cognitive_state": {
      "current_state": "confused",
      "confidence": 0.8,
      "state_history": [
        {
          "state": "confused",
          "timestamp": "2025-11-26T13:30:00",
          "context": {
            "has_error": true,
            "time_stuck": 65.0,
            "question": "Why isn't this working?"
          }
        }
      ]
    },
    "knowledge_state": {
      "concept_mastery": {
        "recursion": 0.48,
        "base_case": 0.45,
        "functions": 0.65
      },
      "mastery_history": [
        {
          "timestamp": "2025-11-26T13:30:00",
          "overall_mastery": 0.53,
          "concepts_tested": ["recursion", "base_case"]
        }
      ],
      "last_updated": "2025-11-26T13:30:00"
    },
    "conversation_history": [
      {
        "timestamp": "2025-11-26T13:30:00",
        "question": "Why isn't this working?",
        "code": "def factorial(n): return n * factorial(n-1)",
        "error": "RecursionError",
        "cognitive_state": "confused",
        "concepts": ["recursion", "base_case"],
        "correctness": 0.3
      }
    ],
    "session_count": 1,
    "total_interactions": 1
  }
}
```

## Benefits

1. **Accurate State Tracking**: System knows actual student state, not assumptions
2. **Learning Over Time**: Mastery scores update based on performance
3. **Cognitive Awareness**: System understands student's mental state from conversation
4. **Personalized Responses**: Responses adapt to actual knowledge gaps and cognitive state
5. **Progress Tracking**: Can see learning trajectory over time

## Integration Points

### Orchestrator

```python
# In process_session()
if self.state_tracker:
    self.state_tracker.update_from_session(...)
    
    # Update DINA
    if adaptive_explainer.dina_wrapper:
        for concept in concepts_identified:
            adaptive_explainer.dina_wrapper.update_mastery(...)
```

### Adaptive Explanation Generator

```python
# Extracts concepts dynamically
concepts_identified = self._extract_concepts_from_data(student_data)

# Returns in result
return {
    ...
    "concepts_identified": concepts_identified,
    "primary_concept": concept
}
```

### COKE Cognitive Graph

```python
# Infers cognitive state from conversation
cognitive_state = coke_graph.predict_cognitive_state(session_data)
```

## Testing

Run the complete response generation to see state tracking:

```bash
python generate_complete_response_with_metrics.py
```

Check state file:
```bash
cat data/student_states.json
```

## Future Enhancements

1. **Multi-session Learning**: Track progress across multiple sessions
2. **Predictive State**: Predict future cognitive states
3. **Intervention Effectiveness**: Track which interventions work best
4. **Collaborative Learning**: Track group interactions
5. **Long-term Memory**: Persistent state across sessions












