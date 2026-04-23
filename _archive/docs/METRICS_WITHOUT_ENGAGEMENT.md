# Quantitative Metrics WITHOUT Engagement Data

## ✅ **Metrics You CAN Calculate (No Engagement Needed)**

---

## 🎯 **1. Learning Outcome Metrics** (Most Important)

### **1.1 Normalized Learning Gain (NLG)**
**What You Need**: Pre-test and post-test scores (or mastery levels)

**Formula**:
```
NLG = (Post_Mastery - Pre_Mastery) / (1.0 - Pre_Mastery)
```

**From Your System**:
- **Pre-mastery**: Initial mastery level (from first session)
- **Post-mastery**: Final mastery level (from last session)
- **Source**: `student_state_tracker.py` - `mastery_history`

**Example**:
```python
# From Student State Tracker
pre_mastery = 0.25  # Initial mastery
post_mastery = 0.85  # Final mastery

nlg = (0.85 - 0.25) / (1.0 - 0.25)
    = 0.60 / 0.75
    = 0.80  # High learning gain!
```

**✅ You Have This**: Mastery history in Student State Tracker

---

### **1.2 Mastery Achievement Rate**
**What You Need**: Number of students reaching mastery threshold

**Formula**:
```
Mastery Rate = Students_Reaching_85% / Total_Students
```

**From Your System**:
- Count students with mastery > 0.85
- **Source**: `student_state_tracker.py` - `concept_mastery`

**Example**:
```python
# Count students with mastery >= 0.85
students_mastered = sum(
    1 for student_id, state in student_states.items()
    if max(state['knowledge_state']['concept_mastery'].values()) >= 0.85
)
total_students = len(student_states)
mastery_rate = students_mastered / total_students
```

**✅ You Have This**: Mastery levels per student

---

### **1.3 Average Mastery Improvement**
**What You Need**: Mastery levels over time

**Formula**:
```
Average Improvement = Mean(Post_Mastery - Pre_Mastery)
```

**From Your System**:
- Calculate from `mastery_history` in Student State Tracker

**Example**:
```python
# For each student
improvements = []
for student_id, state in student_states.items():
    mastery_history = state['knowledge_state']['mastery_history']
    if len(mastery_history) >= 2:
        pre = mastery_history[0]['overall_mastery']
        post = mastery_history[-1]['overall_mastery']
        improvements.append(post - pre)

avg_improvement = np.mean(improvements)
```

**✅ You Have This**: Mastery history tracks this

---

## ⏱️ **2. Efficiency Metrics**

### **2.1 Time to Mastery**
**What You Need**: Session timestamps and mastery levels

**Formula**:
```
Time to Mastery = Timestamp_When_Mastery_Reached - Timestamp_First_Session
```

**From Your System**:
- Session timestamps from `conversation_history`
- Mastery levels from `mastery_history`

**Example**:
```python
def time_to_mastery(student_id, student_state):
    mastery_history = student_state['knowledge_state']['mastery_history']
    conversation_history = student_state['conversation_history']
    
    # Find when mastery >= 0.85
    for i, mastery_entry in enumerate(mastery_history):
        if mastery_entry['overall_mastery'] >= 0.85:
            # Get corresponding session timestamp
            session_timestamp = conversation_history[i]['timestamp']
            first_timestamp = conversation_history[0]['timestamp']
            
            time_diff = (session_timestamp - first_timestamp).total_seconds() / 60
            return time_diff
    
    return None  # Never reached mastery
```

**✅ You Have This**: Timestamps in conversation history

---

### **2.2 Learning Efficiency**
**What You Need**: Learning gain and time spent

**Formula**:
```
Efficiency = Learning_Gain / Time_Spent
```

**From Your System**:
- Learning gain: `post_mastery - pre_mastery`
- Time spent: Sum of `time_stuck` from sessions

**Example**:
```python
learning_gain = post_mastery - pre_mastery
total_time = sum(session['time_stuck'] for session in sessions) / 60  # minutes
efficiency = learning_gain / total_time  # mastery points per minute
```

**✅ You Have This**: Mastery levels + time_stuck from sessions

---

### **2.3 Sessions to Mastery**
**What You Need**: Number of sessions until mastery reached

**Formula**:
```
Sessions to Mastery = Session_Number_When_Mastery_Reached
```

**From Your System**:
- `session_count` in Student State Tracker
- Mastery threshold: 0.85

**Example**:
```python
# Find session number when mastery reached
for i, mastery_entry in enumerate(mastery_history):
    if mastery_entry['overall_mastery'] >= 0.85:
        sessions_to_mastery = i + 1  # 1-indexed
        break
```

**✅ You Have This**: Session count + mastery history

---

## 🎓 **3. Knowledge Gap Metrics**

### **3.1 Knowledge Gap Resolution Rate**
**What You Need**: Concepts with low mastery → high mastery

**Formula**:
```
Gap Resolution = Concepts_Filled / Total_Gaps
```

**From Your System**:
- Initial gaps: Concepts with mastery < 0.5
- Final gaps: Concepts still with mastery < 0.5

**Example**:
```python
# Initial gaps
initial_gaps = [
    concept for concept, mastery in initial_mastery.items()
    if mastery < 0.5
]

# Final gaps
final_gaps = [
    concept for concept, mastery in final_mastery.items()
    if mastery < 0.5
]

gaps_resolved = len(initial_gaps) - len(final_gaps)
resolution_rate = gaps_resolved / len(initial_gaps) if initial_gaps else 0.0
```

**✅ You Have This**: Mastery levels per concept

---

### **3.2 Concept Coverage**
**What You Need**: Number of concepts learned

**Formula**:
```
Coverage = Concepts_Learned / Total_Concepts
```

**From Your System**:
- Concepts with mastery > 0.7
- Total concepts from CSE-KG or session data

**Example**:
```python
concepts_learned = sum(
    1 for mastery in concept_mastery.values()
    if mastery > 0.7
)
total_concepts = len(concept_mastery)
coverage = concepts_learned / total_concepts
```

**✅ You Have This**: Concept mastery dictionary

---

## 🔍 **4. Diagnostic Accuracy Metrics**

### **4.1 Misconception Detection Accuracy**
**What You Need**: Detected misconceptions vs actual errors

**Formula**:
```
Accuracy = (True_Positives + True_Negatives) / Total
Precision = True_Positives / (True_Positives + False_Positives)
Recall = True_Positives / (True_Positives + False_Negatives)
F1 = 2 × (Precision × Recall) / (Precision + Recall)
```

**From Your System**:
- Detected misconceptions from Pedagogical KG
- Actual errors from code/error_message

**Example**:
```python
# Compare detected vs actual
detected_misconceptions = pedagogical_kg.get_misconceptions_for_concept(concept)
actual_error = error_message  # RecursionError

# Check if detected matches actual
true_positive = any(
    "recursion" in mc.description.lower() 
    for mc in detected_misconceptions
) and "RecursionError" in actual_error
```

**✅ You Have This**: Misconception detection from HVSAE + Pedagogical KG

---

### **4.2 Mastery Prediction Accuracy**
**What You Need**: Predicted mastery vs actual performance

**Formula**:
```
RMSE = sqrt(mean((Predicted_Mastery - Actual_Performance)^2))
MAE = mean(abs(Predicted_Mastery - Actual_Performance))
Correlation = corr(Predicted_Mastery, Actual_Performance)
```

**From Your System**:
- Predicted mastery: From Student State Tracker
- Actual performance: Code correctness (0.0-1.0)

**Example**:
```python
predicted_masteries = [state['knowledge_state']['concept_mastery'][concept] 
                       for state in student_states.values()]
actual_performances = [session['code_correctness'] 
                      for session in sessions]

rmse = np.sqrt(np.mean((predicted_masteries - actual_performances)**2))
mae = np.mean(np.abs(predicted_masteries - actual_performances))
correlation = np.corrcoef(predicted_masteries, actual_performances)[0, 1]
```

**✅ You Have This**: Mastery predictions + code correctness scores

---

## 📊 **5. Intervention Effectiveness Metrics**

### **5.1 Intervention Success Rate**
**What You Need**: Interventions used and whether student improved

**Formula**:
```
Success Rate = Successful_Interventions / Total_Interventions
```

**From Your System**:
- Intervention used: From orchestrator
- Success: Mastery increased after intervention

**Example**:
```python
successful = 0
total = 0

for session in sessions:
    if 'intervention' in session:
        mastery_before = session['mastery_before']
        mastery_after = session['mastery_after']
        
        if mastery_after > mastery_before:
            successful += 1
        total += 1

success_rate = successful / total if total > 0 else 0.0
```

**✅ You Have This**: Intervention tracking + mastery changes

---

### **5.2 Misconception Resolution Rate**
**What You Need**: Misconceptions detected and resolved

**Formula**:
```
Resolution Rate = Misconceptions_Resolved / Total_Misconceptions
```

**From Your System**:
- Misconceptions detected: From Pedagogical KG
- Resolved: Student no longer makes same error

**Example**:
```python
# Track misconceptions per student
misconceptions_detected = {}  # student_id -> [misconception_ids]
misconceptions_resolved = {}  # student_id -> [misconception_ids]

# After intervention, check if error no longer occurs
for student_id, misconceptions in misconceptions_detected.items():
    recent_errors = get_recent_errors(student_id)
    for mc_id in misconceptions:
        if mc_id not in recent_errors:
            misconceptions_resolved[student_id].append(mc_id)

resolution_rate = sum(len(resolved) for resolved in misconceptions_resolved.values()) / \
                  sum(len(detected) for detected in misconceptions_detected.values())
```

**✅ You Have This**: Misconception detection + error tracking

---

## 📈 **6. Comparative Metrics (vs Baseline)**

### **6.1 Improvement Percentage**
**What You Need**: Your system metric vs baseline metric

**Formula**:
```
Improvement = ((Your_Metric - Baseline_Metric) / Baseline_Metric) × 100
```

**Example**:
- Baseline mastery rate: 40%
- Your system: 75%
- **Improvement = ((75-40)/40) × 100 = 87.5%**

**✅ You Can Calculate**: If you have baseline data

---

### **6.2 Effect Size (Cohen's d)**
**What You Need**: Your system scores vs baseline scores

**Formula**:
```
Cohen's d = (Mean_Your_System - Mean_Baseline) / Pooled_StdDev
```

**From Your System**:
- Your system: Mastery levels from Student State Tracker
- Baseline: Need comparison data

**Example**:
```python
your_system_scores = [state['knowledge_state']['overall_mastery'] 
                      for state in student_states.values()]
baseline_scores = [0.4, 0.35, 0.45, ...]  # From baseline system

cohens_d = calculate_cohens_d(your_system_scores, baseline_scores)
```

**✅ You Can Calculate**: If you have baseline comparison data

---

## 📋 **Complete List: Metrics WITHOUT Engagement**

### **✅ Metrics You CAN Calculate**:

1. **Normalized Learning Gain (NLG)** ✅
   - From: Pre/post mastery levels
   - Formula: `(Post - Pre) / (1.0 - Pre)`

2. **Mastery Achievement Rate** ✅
   - From: Students reaching 85% mastery
   - Formula: `Students_Mastered / Total_Students`

3. **Average Mastery Improvement** ✅
   - From: Mastery history
   - Formula: `Mean(Post_Mastery - Pre_Mastery)`

4. **Time to Mastery** ✅
   - From: Session timestamps + mastery levels
   - Formula: `Time_When_Mastery_Reached - Time_First_Session`

5. **Learning Efficiency** ✅
   - From: Learning gain + time spent
   - Formula: `Learning_Gain / Time_Spent`

6. **Sessions to Mastery** ✅
   - From: Session count + mastery history
   - Formula: `Session_Number_When_Mastery_Reached`

7. **Knowledge Gap Resolution Rate** ✅
   - From: Initial vs final gaps
   - Formula: `Gaps_Resolved / Total_Gaps`

8. **Concept Coverage** ✅
   - From: Concepts learned
   - Formula: `Concepts_Learned / Total_Concepts`

9. **Misconception Detection Accuracy** ✅
   - From: Detected vs actual misconceptions
   - Formula: `(TP + TN) / Total`

10. **Mastery Prediction Accuracy** ✅
    - From: Predicted vs actual mastery
    - Formula: `RMSE, MAE, Correlation`

11. **Intervention Success Rate** ✅
    - From: Interventions + mastery changes
    - Formula: `Successful / Total`

12. **Misconception Resolution Rate** ✅
    - From: Misconceptions resolved
    - Formula: `Resolved / Total`

13. **Improvement Percentage** ✅
    - From: Your system vs baseline
    - Formula: `((Your - Baseline) / Baseline) × 100`

14. **Effect Size (Cohen's d)** ✅
    - From: Your system vs baseline scores
    - Formula: `(Mean_Your - Mean_Baseline) / Pooled_StdDev`

---

## ❌ **Metrics You CANNOT Calculate (Need Engagement)**:

1. **Engagement Score** ❌
   - Needs: Behavioral, emotional, cognitive engagement data

2. **Intervention Acceptance Rate** ❌
   - Needs: Whether student accepted/rejected intervention

3. **Time on Task** ❌
   - Needs: Active engagement time (not just time_stuck)

4. **Interaction Frequency** ❌
   - Needs: Number of student interactions (clicks, edits, etc.)

---

## 🎯 **Recommended Core Metrics (No Engagement Needed)**

### **Top 5 Most Important**:

1. **Normalized Learning Gain (NLG)** - Primary learning outcome
2. **Mastery Achievement Rate** - How many students succeed
3. **Time to Mastery** - Efficiency metric
4. **Knowledge Gap Resolution Rate** - Problem-solving effectiveness
5. **Misconception Detection Accuracy** - System diagnostic quality

### **Secondary Metrics**:

6. **Learning Efficiency** - Gain per time unit
7. **Sessions to Mastery** - Efficiency alternative
8. **Concept Coverage** - Breadth of learning
9. **Intervention Success Rate** - Teaching effectiveness
10. **Effect Size** - Statistical comparison (if baseline available)

---

## 📊 **Example Evaluation Report (No Engagement)**

```json
{
  "learning_outcomes": {
    "normalized_learning_gain": 0.75,
    "mastery_achievement_rate": 0.85,
    "average_mastery_improvement": 0.45
  },
  "efficiency": {
    "time_to_mastery_minutes": 85.3,
    "sessions_to_mastery": 12.5,
    "learning_efficiency": 0.0053
  },
  "knowledge_gaps": {
    "gap_resolution_rate": 0.78,
    "concept_coverage": 0.65
  },
  "diagnostic_accuracy": {
    "misconception_detection_f1": 0.82,
    "mastery_prediction_rmse": 0.12,
    "mastery_prediction_correlation": 0.87
  },
  "interventions": {
    "intervention_success_rate": 0.73,
    "misconception_resolution_rate": 0.68
  },
  "comparison": {
    "improvement_vs_baseline": 0.875,
    "effect_size_cohens_d": 0.92
  }
}
```

---

## ✅ **Summary**

**You Can Calculate 14 Metrics WITHOUT Engagement Data**:

✅ **Learning Outcomes**: NLG, Mastery Rate, Improvement
✅ **Efficiency**: Time to Mastery, Sessions to Mastery, Learning Efficiency
✅ **Knowledge Gaps**: Gap Resolution, Concept Coverage
✅ **Diagnostic**: Misconception Accuracy, Mastery Prediction Accuracy
✅ **Interventions**: Success Rate, Resolution Rate
✅ **Comparison**: Improvement %, Effect Size

**You Need Engagement Data For**:
❌ Engagement Score
❌ Intervention Acceptance Rate
❌ Time on Task
❌ Interaction Frequency

**Bottom Line**: You can still do a comprehensive evaluation with 14 metrics without engagement data! The most important ones (NLG, Mastery Rate, Time to Mastery) don't need engagement.








