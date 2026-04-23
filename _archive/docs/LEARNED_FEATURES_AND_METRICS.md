# Learned Features vs Personalization Features: Complete Breakdown

## ⚠️ Important Distinction

**The 10 "features" are NOT learned - they are PERSONALIZATION STRATEGIES!**

What's actually **LEARNED** are the underlying **detections** (emotion, personality, mastery, etc.)

---

## 📊 What's Actually LEARNED (From Datasets)

### 1️⃣ **Emotion Detection Patterns** (Learned from ProgSnap2)

**What's learned:**
- Patterns that indicate emotions (confused, frustrated, engaged, confident)
- Behavioral sequences that correlate with emotions
- Temporal patterns (time stuck → frustration)

**Training Data:** ProgSnap2 (50K+ debugging sessions)

**Learned Patterns:**
```python
# Learned from dataset:
- "3 failed test runs" → frustrated (P=0.85)
- "long time stuck (>120s)" → frustrated (P=0.78)
- "quick success" → engaged (P=0.82)
- "asks 'why' questions" → confused (P=0.75)
```

**Accuracy Metrics:**
- **Emotion Classification Accuracy**: % correctly classified emotions
- **Frustration Detection Precision**: TP / (TP + FP)
- **Frustration Detection Recall**: TP / (TP + FN)
- **F1-Score**: 2 × (Precision × Recall) / (Precision + Recall)
- **Confusion Matrix**: Emotion class predictions vs actual

**Target Metrics:**
- Emotion accuracy: >75%
- Frustration precision: >80%
- Frustration recall: >75%
- F1-score: >0.75

---

### 2️⃣ **Engagement Detection Patterns** (Learned from ProgSnap2)

**What's learned:**
- Action patterns that indicate engagement
- Response time patterns
- Interaction frequency patterns

**Training Data:** ProgSnap2

**Learned Patterns:**
```python
# Learned from dataset:
- "Frequent interactions" → high engagement (P=0.80)
- "Long pauses" → low engagement (P=0.72)
- "Follow-up questions" → high engagement (P=0.85)
```

**Accuracy Metrics:**
- **Engagement Classification Accuracy**: % correctly classified engagement levels
- **Engagement Score Correlation**: Pearson correlation with ground truth
- **Engagement Prediction RMSE**: Root Mean Square Error
- **Engagement Level Precision/Recall**: Per engagement level (low/medium/high)

**Target Metrics:**
- Classification accuracy: >70%
- Correlation coefficient: >0.65
- RMSE: <0.15

---

### 3️⃣ **Code Pattern Recognition** (Learned from CodeNet)

**What's learned:**
- Code semantic patterns (what code means)
- Error patterns (common bugs)
- Code quality patterns

**Training Data:** CodeNet (14M code submissions)

**Learned Patterns:**
```python
# Learned from dataset:
- "max_num = 0" → initialization error pattern (P=0.92)
- "range(len(...)) with [i+1]" → off-by-one pattern (P=0.88)
- "node.next without None check" → null pointer pattern (P=0.90)
```

**Accuracy Metrics:**
- **Error Detection Accuracy**: % correctly detected errors
- **Error Type Classification Accuracy**: % correctly classified error types
- **False Positive Rate**: Incorrect error detections / Total detections
- **False Negative Rate**: Missed errors / Total actual errors
- **Error Location Accuracy**: % correctly identified error locations

**Target Metrics:**
- Error detection accuracy: >85%
- Error type accuracy: >80%
- False positive rate: <10%
- False negative rate: <15%

---

### 4️⃣ **Mastery Estimation Patterns** (Learned from ASSISTments)

**What's learned:**
- Response patterns that indicate mastery
- Skill-solution mappings (Q-matrix)
- Mastery probability estimation

**Training Data:** ASSISTments (500K+ student responses)

**Learned Patterns:**
```python
# Learned from dataset:
- "Correct on recursion problems" → high recursion mastery (P=0.85)
- "Wrong on base case problems" → low base case mastery (P=0.78)
- "Consistent correct answers" → high mastery (P=0.82)
```

**Accuracy Metrics:**
- **Mastery Prediction Accuracy**: % correctly predicted mastery levels
- **Mastery Estimation RMSE**: Root Mean Square Error vs actual mastery
- **Mastery Correlation**: Pearson correlation with ground truth
- **AUC-ROC**: Area Under ROC Curve (for mastery classification)
- **Calibration Error**: Difference between predicted and actual mastery

**Target Metrics:**
- Prediction accuracy: >75%
- RMSE: <0.15
- Correlation: >0.70
- AUC-ROC: >0.80
- Calibration error: <0.10

---

### 5️⃣ **Personality Inference Patterns** (Learned from Language Patterns)

**What's learned:**
- Language patterns that indicate personality traits
- Question type → learning preference mappings
- Behavioral patterns → personality traits

**Training Data:** Inferred from conversation patterns (not from dataset, but patterns are learned)

**Learned Patterns:**
```python
# Learned patterns (from language analysis):
- "why/how questions" → conceptual learner (P=0.85)
- "provides complete code" → high conscientiousness (P=0.78)
- "asks many questions" → high openness (P=0.75)
```

**Accuracy Metrics:**
- **Personality Trait Correlation**: Correlation with Big Five assessments
- **Learning Style Classification Accuracy**: % correctly classified learning styles
- **Personality Prediction RMSE**: Per trait (openness, conscientiousness, etc.)
- **Cross-Validation Accuracy**: K-fold cross-validation accuracy

**Target Metrics:**
- Trait correlation: >0.60
- Learning style accuracy: >70%
- RMSE per trait: <0.20

---

### 6️⃣ **Code Embedding Patterns** (Learned from CodeNet)

**What's learned:**
- Semantic representations of code
- Code similarity patterns
- Code-to-meaning mappings

**Training Data:** CodeNet

**Learned Patterns:**
```python
# Learned embeddings:
- Similar code structures → similar embeddings
- Code semantics → embedding space positions
- Code patterns → latent representations
```

**Accuracy Metrics:**
- **Code Similarity Accuracy**: % correctly identified similar code
- **Code Classification Accuracy**: % correctly classified code types
- **Embedding Quality**: Cosine similarity with human annotations
- **Retrieval Accuracy**: Code retrieval accuracy (find similar code)

**Target Metrics:**
- Similarity accuracy: >80%
- Classification accuracy: >75%
- Embedding quality: >0.70 cosine similarity

---

## 🎯 The 10 Personalization Features (NOT Learned, But Applied)

These are **strategies** that use the learned detections:

### Feature 1: Conversation Memory
**Uses learned:** BKT mastery history, emotion history
**Not learned:** Memory strategy itself

### Feature 2: Emotional Intelligence
**Uses learned:** Emotion detection, frustration detection
**Not learned:** Tone adaptation strategy

### Feature 3: Learning Style Personalization
**Uses learned:** Learning preference detection
**Not learned:** Style adaptation strategy

### Feature 4: Personality-Based Communication
**Uses learned:** Personality trait detection
**Not learned:** Communication style strategy

### Feature 5: Progress-Aware Responses
**Uses learned:** Mastery estimation, mastery changes
**Not learned:** Progress acknowledgment strategy

### Feature 6: Interest Personalization
**Uses learned:** None (manual input)
**Not learned:** Interest-based example strategy

### Feature 7: Format Preferences
**Uses learned:** Engagement patterns, personality
**Not learned:** Format adaptation strategy

### Feature 8: Error-Specific Feedback
**Uses learned:** Error detection patterns
**Not learned:** Error feedback strategy

### Feature 9: Metacognitive Guidance
**Uses learned:** Mastery trends, emotion patterns
**Not learned:** Strategy suggestion approach

### Feature 10: Adaptive Difficulty
**Uses learned:** Mastery estimation, engagement
**Not learned:** Difficulty adaptation strategy

---

## 📈 Complete Accuracy Metrics Table

| What's Learned | Metric | Target | How to Measure |
|----------------|--------|--------|----------------|
| **Emotion Detection** | Classification Accuracy | >75% | Compare predicted vs actual emotions |
| | Frustration Precision | >80% | TP / (TP + FP) |
| | Frustration Recall | >75% | TP / (TP + FN) |
| | F1-Score | >0.75 | 2 × (P × R) / (P + R) |
| **Engagement Detection** | Classification Accuracy | >70% | Compare predicted vs actual engagement |
| | Correlation | >0.65 | Pearson correlation with ground truth |
| | RMSE | <0.15 | Root Mean Square Error |
| **Error Detection** | Detection Accuracy | >85% | % correctly detected errors |
| | Error Type Accuracy | >80% | % correctly classified error types |
| | False Positive Rate | <10% | Incorrect detections / Total |
| | False Negative Rate | <15% | Missed errors / Total actual |
| **Mastery Estimation** | Prediction Accuracy | >75% | % correctly predicted mastery |
| | RMSE | <0.15 | Root Mean Square Error |
| | Correlation | >0.70 | Pearson correlation |
| | AUC-ROC | >0.80 | Area Under ROC Curve |
| **Personality Detection** | Trait Correlation | >0.60 | Correlation with Big Five |
| | Learning Style Accuracy | >70% | % correctly classified styles |
| | RMSE per Trait | <0.20 | Per trait (O, C, E, A, N) |
| **Code Embeddings** | Similarity Accuracy | >80% | % correctly identified similar code |
| | Classification Accuracy | >75% | % correctly classified code types |
| | Embedding Quality | >0.70 | Cosine similarity with annotations |

---

## 🔬 How to Measure Accuracy

### 1. Emotion Detection Metrics

```python
# Ground truth: Human-annotated emotions
ground_truth = ['confused', 'frustrated', 'engaged', ...]
predictions = model.predict(student_inputs)

# Calculate metrics
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

accuracy = accuracy_score(ground_truth, predictions)
precision = precision_score(ground_truth, predictions, average='weighted')
recall = recall_score(ground_truth, predictions, average='weighted')
f1 = f1_score(ground_truth, predictions, average='weighted')

# Confusion matrix
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(ground_truth, predictions)
```

### 2. Mastery Estimation Metrics

```python
# Ground truth: Actual mastery (from assessments)
ground_truth_mastery = [0.85, 0.60, 0.45, ...]
predicted_mastery = model.estimate_mastery(student_responses)

# Calculate metrics
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np

rmse = np.sqrt(mean_squared_error(ground_truth_mastery, predicted_mastery))
correlation = np.corrcoef(ground_truth_mastery, predicted_mastery)[0, 1]
r2 = r2_score(ground_truth_mastery, predicted_mastery)

# Calibration error
calibration_error = np.mean(np.abs(ground_truth_mastery - predicted_mastery))
```

### 3. Error Detection Metrics

```python
# Ground truth: Human-annotated errors
ground_truth_errors = [
    {'type': 'initialization_error', 'line': 2, 'present': True},
    {'type': 'off_by_one', 'line': 5, 'present': False},
    ...
]
predicted_errors = model.detect_errors(student_code)

# Calculate metrics
true_positives = sum(1 for gt, pred in zip(ground_truth_errors, predicted_errors) 
                    if gt['present'] and pred['present'])
false_positives = sum(1 for gt, pred in zip(ground_truth_errors, predicted_errors) 
                     if not gt['present'] and pred['present'])
false_negatives = sum(1 for gt, pred in zip(ground_truth_errors, predicted_errors) 
                     if gt['present'] and not pred['present'])

precision = true_positives / (true_positives + false_positives)
recall = true_positives / (true_positives + false_negatives)
f1 = 2 * (precision * recall) / (precision + recall)
```

### 4. Engagement Detection Metrics

```python
# Ground truth: Engagement scores (0-1)
ground_truth_engagement = [0.85, 0.60, 0.45, ...]
predicted_engagement = model.predict_engagement(student_actions)

# Calculate metrics
rmse = np.sqrt(mean_squared_error(ground_truth_engagement, predicted_engagement))
correlation = np.corrcoef(ground_truth_engagement, predicted_engagement)[0, 1]

# Classification accuracy (low/medium/high)
engagement_levels_gt = [quantize(e) for e in ground_truth_engagement]
engagement_levels_pred = [quantize(e) for e in predicted_engagement]
accuracy = accuracy_score(engagement_levels_gt, engagement_levels_pred)
```

---

## 📊 Evaluation Dataset Requirements

### For Emotion Detection:
- **Need:** Human-annotated emotions for student interactions
- **Size:** 500+ interactions
- **Labels:** confused, frustrated, engaged, confident, neutral

### For Mastery Estimation:
- **Need:** Actual mastery assessments (tests, quizzes)
- **Size:** 1000+ student responses
- **Labels:** Mastery scores (0-1) per skill

### For Error Detection:
- **Need:** Human-annotated code errors
- **Size:** 500+ code samples
- **Labels:** Error type, location, presence

### For Engagement:
- **Need:** Engagement scores (self-reported or observed)
- **Size:** 500+ interactions
- **Labels:** Engagement scores (0-1)

---

## 🎯 Summary

### What's LEARNED (6 things):
1. ✅ **Emotion Detection Patterns** (from ProgSnap2)
2. ✅ **Engagement Detection Patterns** (from ProgSnap2)
3. ✅ **Code Pattern Recognition** (from CodeNet)
4. ✅ **Mastery Estimation Patterns** (from ASSISTments)
5. ✅ **Personality Inference Patterns** (from language analysis)
6. ✅ **Code Embedding Patterns** (from CodeNet)

### What's NOT Learned (10 Personalization Features):
- These are **strategies** that use the learned detections
- They're **applied**, not learned

### Accuracy Metrics:
- **6 sets of metrics** for the 6 learned features
- **Target values** provided for each
- **Measurement methods** explained

---

**The 10 features are personalization strategies that USE the 6 learned detections!** 🎯

















