# Research-Based Quantitative Metrics for Learning Systems

## 📚 Standard Metrics from Research Papers

Based on educational data mining and adaptive tutoring system research, here are the **standard quantitative metrics** used to compare learning systems:

---

## 🎯 **1. Learning Outcome Metrics** (Most Important)

### **1.1 Normalized Learning Gain (NLG)**
**Source**: Hake (1998), widely used in physics education research

**Formula**:
```
NLG = (PostTest - PreTest) / (100 - PreTest)
```

**Interpretation**:
- **NLG > 0.7**: High learning gain (excellent)
- **NLG 0.3-0.7**: Medium learning gain (good)
- **NLG < 0.3**: Low learning gain (needs improvement)

**How to Calculate**:
```python
def normalized_learning_gain(pre_test_score, post_test_score):
    """
    Calculate normalized learning gain
    
    Args:
        pre_test_score: Score before learning (0-100)
        post_test_score: Score after learning (0-100)
    
    Returns:
        NLG value (0.0-1.0)
    """
    if pre_test_score >= 100:
        return 0.0  # Already mastered
    
    return (post_test_score - pre_test_score) / (100 - pre_test_score)
```

**Example**:
- Pre-test: 40%
- Post-test: 85%
- **NLG = (85-40)/(100-40) = 45/60 = 0.75** (High gain!)

---

### **1.2 Effect Size (Cohen's d)**
**Source**: Cohen (1988), standard in educational research

**Formula**:
```
Cohen's d = (Mean_Treatment - Mean_Control) / Pooled_StdDev
```

**Interpretation**:
- **d > 0.8**: Large effect (strong improvement)
- **d 0.5-0.8**: Medium effect (moderate improvement)
- **d 0.2-0.5**: Small effect (weak improvement)
- **d < 0.2**: Negligible effect

**How to Calculate**:
```python
import numpy as np
from scipy import stats

def cohens_d(treatment_scores, control_scores):
    """
    Calculate Cohen's d effect size
    
    Args:
        treatment_scores: Scores from personalized system
        control_scores: Scores from baseline system
    
    Returns:
        Cohen's d value
    """
    treatment_mean = np.mean(treatment_scores)
    control_mean = np.mean(control_scores)
    
    treatment_std = np.std(treatment_scores, ddof=1)
    control_std = np.std(control_scores, ddof=1)
    
    pooled_std = np.sqrt(
        ((len(treatment_scores) - 1) * treatment_std**2 + 
         (len(control_scores) - 1) * control_std**2) /
        (len(treatment_scores) + len(control_scores) - 2)
    )
    
    return (treatment_mean - control_mean) / pooled_std
```

---

### **1.3 Mastery Achievement Rate**
**Source**: Bloom (1984), mastery learning theory

**Formula**:
```
Mastery Rate = (Students who reached mastery) / (Total students)
```

**Mastery Threshold**: Typically 80-85% (your system uses 85%)

**Example**:
- Total students: 100
- Students reaching 85% mastery: 75
- **Mastery Rate = 75/100 = 0.75 = 75%**

---

## ⏱️ **2. Efficiency Metrics**

### **2.1 Time to Mastery**
**Source**: VanLehn (2006), intelligent tutoring systems

**Formula**:
```
Time to Mastery = Average time (in minutes/hours) for student to reach mastery threshold
```

**How to Calculate**:
```python
def time_to_mastery(student_sessions):
    """
    Calculate average time to mastery
    
    Args:
        student_sessions: List of sessions with timestamps and mastery levels
    
    Returns:
        Average time to mastery (in minutes)
    """
    times_to_mastery = []
    
    for student_id, sessions in student_sessions.items():
        mastery_threshold = 0.85
        start_time = sessions[0]['timestamp']
        
        for session in sessions:
            if session['mastery'] >= mastery_threshold:
                time_taken = (session['timestamp'] - start_time).total_seconds() / 60
                times_to_mastery.append(time_taken)
                break
    
    return np.mean(times_to_mastery) if times_to_mastery else None
```

**Comparison**:
- **Baseline system**: 120 minutes average
- **Your system**: 85 minutes average
- **Improvement**: 29% faster

---

### **2.2 Learning Efficiency**
**Source**: Koedinger et al. (2013), cognitive tutors

**Formula**:
```
Learning Efficiency = Learning Gain / Time Spent
```

**Units**: Points gained per minute

**Example**:
- Learning gain: 45 points
- Time spent: 90 minutes
- **Efficiency = 45/90 = 0.5 points/minute**

---

## 📈 **3. Engagement Metrics**

### **3.1 Engagement Score**
**Source**: Fredricks et al. (2004), engagement framework

**Components**:
- **Behavioral**: Time on task, number of interactions
- **Emotional**: Positive emotions, interest level
- **Cognitive**: Deep thinking, strategy use

**Formula**:
```
Engagement Score = (
    Behavioral_Engagement × 0.4 +
    Emotional_Engagement × 0.3 +
    Cognitive_Engagement × 0.3
)
```

**Your System Already Tracks**:
- Behavioral: `action_sequence` length, `time_stuck`
- Emotional: RNN emotion prediction
- Cognitive: COKE cognitive state

---

### **3.2 Intervention Acceptance Rate**
**Source**: Koedinger et al. (2013)

**Formula**:
```
Acceptance Rate = (Interventions Accepted) / (Total Interventions Offered)
```

**Interpretation**:
- **> 0.8**: High acceptance (students trust system)
- **0.5-0.8**: Medium acceptance
- **< 0.5**: Low acceptance (system not helpful)

---

## 🎓 **4. Retention Metrics**

### **4.1 Knowledge Retention Rate**
**Source**: Ebbinghaus (1885), forgetting curve

**Formula**:
```
Retention Rate = (Score_After_Delay - Score_Immediate) / Score_Immediate
```

**Typical Delays**:
- **1 day**: Short-term retention
- **1 week**: Medium-term retention
- **1 month**: Long-term retention

**Example**:
- Immediate post-test: 85%
- After 1 week: 78%
- **Retention = (78-85)/85 = -0.082 = -8.2%** (8.2% forgetting)

---

### **4.2 Transfer Learning Score**
**Source**: Singley & Anderson (1989), transfer of learning

**Formula**:
```
Transfer Score = Performance_On_New_Problem / Performance_On_Original_Problem
```

**Interpretation**:
- **> 0.8**: Excellent transfer (can apply knowledge)
- **0.5-0.8**: Good transfer
- **< 0.5**: Poor transfer (knowledge not generalizable)

---

## 🔍 **5. Diagnostic Accuracy Metrics**

### **5.1 Misconception Detection Accuracy**
**Source**: Educational data mining research

**Formula**:
```
Accuracy = (True_Positives + True_Negatives) / Total
Precision = True_Positives / (True_Positives + False_Positives)
Recall = True_Positives / (True_Positives + False_Negatives)
F1 = 2 × (Precision × Recall) / (Precision + Recall)
```

**Your System Already Has**: `misconception_probs` from HVSAE decoder

---

### **5.2 Mastery Prediction Accuracy**
**Source**: BKT (Bayesian Knowledge Tracing) research

**Metrics**:
- **RMSE**: Root Mean Squared Error (lower is better)
- **MAE**: Mean Absolute Error (lower is better)
- **Correlation**: Pearson correlation with true mastery (higher is better)

**Your System Already Has**: In `src/utils/metrics.py` - `mastery_metrics()`

---

## 📊 **6. Comparative Metrics (Your System vs Baseline)**

### **6.1 Improvement Percentage**
```
Improvement = ((Your_System_Metric - Baseline_Metric) / Baseline_Metric) × 100
```

**Example**:
- Baseline mastery rate: 40%
- Your system mastery rate: 98%
- **Improvement = ((98-40)/40) × 100 = 145% improvement**

---

### **6.2 Statistical Significance**
**Source**: Standard statistical testing

**Test**: t-test or Mann-Whitney U test

**Interpretation**:
- **p < 0.05**: Statistically significant improvement
- **p < 0.01**: Highly significant
- **p < 0.001**: Very highly significant

---

## 📋 **7. Complete Evaluation Framework**

### **Recommended Metrics for Your System**:

```python
EVALUATION_METRICS = {
    # Learning Outcomes (40% weight)
    "normalized_learning_gain": {
        "weight": 0.20,
        "target": "> 0.7",
        "source": "Hake (1998)"
    },
    "effect_size_cohens_d": {
        "weight": 0.15,
        "target": "> 0.8",
        "source": "Cohen (1988)"
    },
    "mastery_achievement_rate": {
        "weight": 0.05,
        "target": "> 0.85",
        "source": "Bloom (1984)"
    },
    
    # Efficiency (25% weight)
    "time_to_mastery": {
        "weight": 0.15,
        "target": "Minimize",
        "source": "VanLehn (2006)"
    },
    "learning_efficiency": {
        "weight": 0.10,
        "target": "Maximize",
        "source": "Koedinger (2013)"
    },
    
    # Engagement (20% weight)
    "engagement_score": {
        "weight": 0.10,
        "target": "> 0.7",
        "source": "Fredricks (2004)"
    },
    "intervention_acceptance_rate": {
        "weight": 0.10,
        "target": "> 0.8",
        "source": "Koedinger (2013)"
    },
    
    # Retention (10% weight)
    "knowledge_retention_rate": {
        "weight": 0.05,
        "target": "> 0.8",
        "source": "Ebbinghaus (1885)"
    },
    "transfer_learning_score": {
        "weight": 0.05,
        "target": "> 0.8",
        "source": "Singley & Anderson (1989)"
    },
    
    # Diagnostic Accuracy (5% weight)
    "misconception_detection_f1": {
        "weight": 0.03,
        "target": "> 0.8",
        "source": "EDM research"
    },
    "mastery_prediction_rmse": {
        "weight": 0.02,
        "target": "< 0.15",
        "source": "BKT research"
    }
}
```

---

## 📚 **Key Research Papers**

### **1. Learning Gain Metrics**:
- **Hake, R. R. (1998)**: "Interactive-engagement versus traditional methods: A six-thousand-student survey of mechanics test data for introductory physics courses"
- **Cohen, J. (1988)**: "Statistical Power Analysis for the Behavioral Sciences"

### **2. Intelligent Tutoring Systems**:
- **VanLehn, K. (2006)**: "The behavior of tutoring systems"
- **Koedinger, K. R., et al. (2013)**: "The Knowledge-Learning-Instruction framework: Bridging the science-practice chasm to enhance robust student learning"

### **3. Engagement**:
- **Fredricks, J. A., et al. (2004)**: "School engagement: Potential of the concept, state of the evidence"

### **4. Knowledge Tracing**:
- **Corbett, A. T., & Anderson, J. R. (1995)**: "Knowledge tracing: Modeling the acquisition of procedural knowledge"
- **Piech, C., et al. (2015)**: "Deep knowledge tracing"

### **5. Educational Data Mining**:
- **Romero, C., & Ventura, S. (2013)**: "Data mining in education"
- **Baker, R. S., & Inventado, P. S. (2014)**: "Educational data mining and learning analytics"

---

## 🔧 **Implementation in Your System**

### **What You Already Have**:
✅ Learning gain tracking (from mastery history)
✅ Engagement score (from behavioral analysis)
✅ Intervention acceptance (can track)
✅ Misconception detection (from HVSAE)
✅ Mastery prediction (from Student State Tracker)

### **What to Add**:
1. **Normalized Learning Gain**: Calculate from pre/post tests
2. **Effect Size**: Compare with baseline system
3. **Time to Mastery**: Track from session timestamps
4. **Retention Rate**: Test students after delay
5. **Transfer Learning**: Test on new problem types

---

## 📊 **Example Comparison Table**

| Metric | Baseline System | Your System | Improvement |
|--------|----------------|-------------|-------------|
| **Normalized Learning Gain** | 0.45 | 0.75 | +67% |
| **Effect Size (Cohen's d)** | 0.3 | 0.9 | +200% |
| **Mastery Achievement Rate** | 40% | 98% | +145% |
| **Time to Mastery** | 120 min | 85 min | -29% |
| **Engagement Score** | 0.5 | 0.85 | +70% |
| **Intervention Acceptance** | 0.6 | 0.87 | +45% |
| **Retention Rate (1 week)** | 0.65 | 0.82 | +26% |
| **Transfer Learning** | 0.55 | 0.88 | +60% |

---

## ✅ **Summary**

**Standard Quantitative Metrics from Research**:
1. ✅ **Normalized Learning Gain** (Hake, 1998) - Most important
2. ✅ **Effect Size** (Cohen's d) - For comparison
3. ✅ **Time to Mastery** - Efficiency metric
4. ✅ **Engagement Score** - Student motivation
5. ✅ **Retention Rate** - Long-term learning
6. ✅ **Transfer Learning** - Knowledge application

**Your System Can Track**:
- Most metrics already available
- Need to add: NLG calculation, effect size comparison, retention testing

**Next Steps**:
1. Implement NLG calculation
2. Set up baseline comparison
3. Add retention testing (delayed post-tests)
4. Calculate effect sizes for publication








