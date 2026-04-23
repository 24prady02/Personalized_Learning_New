# Complete 10 Personalization Feature Scenarios

This document contains 10 complete conversation scenarios, each testing one personalization feature with 4-5 question-response pairs and detailed metrics.

## How to Use

1. **Run the scenarios:**
   ```bash
   python run_personalization_tests.py
   ```

2. **View results:**
   - Individual results: `personalization_test_outputs/{scenario_id}_results.json`
   - Summary: `personalization_test_outputs/all_personalization_results.json`

3. **Analyze metrics:**
   - Each response has qualitative and quantitative metrics
   - Feature detection shows which of the 10 features were used
   - Scores show how well each feature was implemented

## Scenario Structure

Each scenario contains:
- **Student Profile**: Initial state (mastery, learning style, personality)
- **4-5 Conversation Turns**: Question → Response → Metrics
- **Feature Detection**: Which features were detected in each response
- **Qualitative Metrics**: What features are present (True/False)
- **Quantitative Metrics**: How well features are implemented (scores 0-1)
- **Summary Metrics**: Overall feature utilization score

## The 10 Features

1. **Conversation Memory & Context** - Remembers previous conversations
2. **Emotional Intelligence & Tone** - Adapts tone based on emotion
3. **Learning Style - Visual** - Provides visual explanations
4. **Learning Style - Conceptual** - Deep conceptual explanations
5. **Personality-Based Communication** - Adapts to personality traits
6. **Progress-Aware Responses** - Acknowledges student progress
7. **Interest & Context** - Incorporates student interests
8. **Response Format Preferences** - Adapts format (lists, code, etc.)
9. **Error-Specific & Diagnostic** - Provides targeted error feedback
10. **Metacognitive & Learning Strategy** - Teaches learning strategies

## Metrics Explained

### Qualitative Metrics
- **Boolean indicators**: Shows if a feature is present (True/False)
- **Feature detection**: Lists which of the 10 features were detected
- **Style indicators**: Shows adaptation type (visual, conceptual, etc.)

### Quantitative Metrics
- **Scores (0-1)**: How well a feature was implemented
- **Counts**: Number of relevant keywords/phrases found
- **Ratios**: Coverage percentages
- **Overall scores**: Weighted combination of all metrics

## Example Output

```json
{
  "turn": 2,
  "metrics": {
    "qualitative": {
      "references_previous": true,
      "maintains_metaphor": true,
      "builds_context": true
    },
    "quantitative": {
      "previous_references": 2,
      "metaphor_continuity": 1.0,
      "context_score": 0.9
    }
  },
  "feature_detection": {
    "conversation_memory": true,
    "learning_style_adaptation": true,
    "target_feature_detected": true
  }
}
```

See `personalization_conversation_scenarios.py` for complete scenario definitions.














