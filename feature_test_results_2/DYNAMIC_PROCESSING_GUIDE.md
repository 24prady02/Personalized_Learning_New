# Dynamic Processing Guide - Real Dataset Tests

## Overview

The `run_real_dataset_tests.py` script processes **real student data** from actual datasets. **NO VALUES ARE HARDCODED** - everything is extracted dynamically.

## How It Works

### 1. Dataset Loading

The script loads real datasets:

```python
loader = RealDatasetLoader()
loader.load_progsnap2()      # Real debugging sessions
loader.load_assistments()    # Real student responses
loader.load_codenet()        # Real code submissions
```

### 2. Dynamic Session Extraction

Sessions are extracted from real data:

- **ProgSnap2**: Groups by SubjectID and ProblemID to get full debugging sessions
- **CodeNet**: Extracts code samples with actual bugs and correct implementations
- **ASSISTments**: Uses real student response patterns

### 3. Question Generation

Questions are generated dynamically based on:
- Event types (Compile.Error, Run.Program, etc.)
- Error messages (RecursionError, SyntaxError, etc.)
- Code content (factorial, recursion, etc.)

**Example**:
```python
# If error contains "RecursionError":
question = "I'm getting a recursion error. Can you help me understand what's wrong with my code?"

# If event is "Run.Program" with code:
question = "I wrote this code but I'm not sure if it's correct. Can you review it?"
```

### 4. Real Model Processing

Each turn is processed through:
- **DINA Model**: Real cognitive diagnosis (not simulated)
- **CodeBERT**: Real code analysis (not pattern matching)
- **BERT**: Real text understanding (not keyword matching)
- **Nestor**: Real personality profiling (NO FALLBACK)
- **CSE-KG**: Real knowledge graph queries

### 5. Dynamic Metrics Calculation

Metrics are calculated in real-time:
- Mastery progression based on actual code quality
- Code quality from CodeBERT embeddings
- Explanation quality from BERT analysis
- Engagement from behavioral patterns
- Student type from Nestor personality profiling

## Output Format

Each session generates:

```
feature_test_results_2/
├── progsnap2_student_001_problem_001/
│   ├── results.json          # Detailed metrics per turn
│   └── README.md            # Human-readable summary
├── codenet_buggy_factorial.txt/
│   ├── results.json
│   └── README.md
└── REAL_DATASET_SUMMARY.md  # Overall summary
```

## Example Output Structure

### results.json
```json
{
  "session_id": "progsnap2_student_001_problem_001",
  "source": "ProgSnap2",
  "student_id": "student_001",
  "conversation_results": [
    {
      "turn": 1,
      "input": {
        "question": "I'm getting a recursion error...",
        "code": "def factorial(n):\n    return n * factorial(n-1)",
        "error_message": "RecursionError: maximum recursion depth exceeded",
        "concepts_detected": ["recursion", "base_case", "functions"]
      },
      "output": {
        "response": "...",
        "analysis": {
          "mastery": 0.35
        }
      },
      "metrics": {
        "mastery": {"overall": 0.35, "recursion": 0.25},
        "code_quality": {"overall": 0.6, "syntax": 1.0, "logic": 0.2},
        "explanation_quality": {"overall": 0.85},
        "engagement": {"overall": 0.7},
        "student_type": {"type": "curious_learner"}
      }
    }
  ]
}
```

### README.md
Similar format to `feature_test_results/feature_001/README.md`:
- Student progression overview
- Mastery progression table
- Detailed turn-by-turn analysis
- All metrics displayed

## Key Differences from Hardcoded Tests

| Aspect | Hardcoded Tests | Real Dataset Tests |
|--------|----------------|-------------------|
| **Questions** | Predefined | Generated from events/errors |
| **Code** | Fixed examples | Extracted from datasets |
| **Errors** | Simulated | Real error messages |
| **Sessions** | Scripted | Actual student sessions |
| **Metrics** | May use simulated models | Always uses real models |
| **Output** | Predictable | Varies with real data |

## Benefits

1. **Realistic**: Uses actual student behavior patterns
2. **Dynamic**: Adapts to different datasets
3. **Scalable**: Can process any number of sessions
4. **Accurate**: Real models provide accurate metrics
5. **Reproducible**: Same dataset = same results

## Requirements

1. Datasets must be downloaded:
   ```bash
   python scripts/download_datasets.py
   ```

2. Real models must be available:
   - DINA model in `src/models/dina/`
   - CodeBERT/BERT models (auto-downloaded)
   - Nestor model in `src/models/nestor/`
   - CSE-KG client configured

3. API key for chat interface:
   ```bash
   export GROQ_API_KEY=your_key
   ```

## Troubleshooting

### "No sessions extracted"
- Run `python scripts/download_datasets.py` first
- Check that `data/progsnap2/` or `data/codenet/` exists

### "Error importing real models"
- Ensure all model dependencies are installed
- Check that `src/models/` directory structure is correct

### "CSE-KG extractor not available"
- This is a warning, not an error
- System will continue without CSE-KG concept extraction
- Metrics will still be calculated using other models

## Next Steps

1. Run the script: `python run_real_dataset_tests.py`
2. Review generated summaries in each session folder
3. Compare metrics across different sessions
4. Use results to evaluate system effectiveness with real data












