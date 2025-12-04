# Per-Session Quantitative Metrics (Single Student)

## 🎯 **Metrics That DON'T Require Multiple Students**

These metrics can be calculated from **individual student sessions** and don't need aggregation across multiple students.

---

## 📊 **1. Code Quality Metrics** (Per Session)

### **1.1 Code Correctness Score**
**Formula**:
```
Correctness = 1.0 - (Syntax_Errors × 0.3 + Logic_Errors × 0.7)
```

**From Your System**:
- Syntax errors: Count from code analysis
- Logic errors: Detected from error messages
- **Source**: `orchestrator.py` line 1105-1111

**Example**:
```python
syntax_errors = 0  # No syntax errors
logic_errors = 1   # Missing base case
correctness = 1.0 - (0 × 0.3 + 1 × 0.7) = 0.3
```

**✅ You Have This**: Already calculated in `_calculate_complete_metrics()`

---

### **1.2 Error Reduction Rate**
**Formula**:
```
Error Reduction = (Errors_Before - Errors_After) / Errors_Before
```

**From Your System**:
- Errors before: From first session
- Errors after: From current session
- **Source**: Compare sessions in conversation history

**Example**:
```python
# First session
errors_before = 3  # syntax + logic errors

# Current session (after intervention)
errors_after = 1

error_reduction = (3 - 1) / 3 = 0.67 = 67% reduction
```

**✅ You Can Calculate**: From session history

---

### **1.3 Code Complexity Score**
**Formula**:
```
Complexity = (Cyclomatic_Complexity + Nesting_Depth + Lines_of_Code) / 3
```

**From Your System**:
- Analyze code structure
- Count branches, loops, nesting

**Example**:
```python
# Student's code
code = """
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)
"""

cyclomatic = 2  # if statement + function
nesting = 1     # one level
loc = 5         # lines of code

complexity = (2 + 1 + 5) / 3 = 2.67
```

---

## 📝 **2. Explanation Quality Metrics** (Per Response)

### **2.1 Explanation Completeness**
**Formula**:
```
Completeness = (Key_Points_Covered / Total_Key_Points) × 100
```

**Key Points to Check**:
- Error explanation
- Root cause identification
- Solution provided
- Examples given
- Prerequisites mentioned

**From Your System**:
- Explanation text from `adaptive_result`
- **Source**: `orchestrator.py` line 1116-1126

**Example**:
```python
explanation = "Your code is missing a base case..."
key_points = [
    "error_explained",      # ✅ Found
    "root_cause",           # ✅ Found
    "solution_provided",    # ✅ Found
    "example_given",        # ❌ Missing
    "prerequisites"         # ❌ Missing
]

completeness = 3 / 5 = 0.6 = 60%
```

**✅ You Have This**: Already calculated in `bert_quality['completeness']`

---

### **2.2 Explanation Clarity Score**
**Formula**:
```
Clarity = (Clarity_Indicators / Total_Words) × Weight
```

**Clarity Indicators**:
- "because", "reason", "why", "how"
- "step", "example", "simple", "clear"
- Code examples
- Visual aids mentioned

**From Your System**:
- **Source**: `orchestrator.py` line 1118-1119

**Example**:
```python
explanation = "The reason is because recursion needs a base case..."
words = 10
clarity_indicators = 2  # "reason", "because"
clarity = (2 / 10) × 10 = 2.0 (normalized to 0.0-1.0)
```

**✅ You Have This**: Already calculated in `bert_quality['clarity']`

---

### **2.3 Response Relevance Score**
**Formula**:
```
Relevance = (Relevant_Concepts_Mentioned / Total_Concepts_Needed) × 100
```

**From Your System**:
- Concepts needed: From knowledge gaps
- Concepts mentioned: Extract from explanation text

**Example**:
```python
concepts_needed = ["recursion", "base_case", "conditional_statements"]
concepts_mentioned = ["recursion", "base_case"]  # From explanation

relevance = 2 / 3 = 0.67 = 67%
```

---

## ⚡ **3. Learning Velocity Metrics** (Per Session)

### **3.1 Mastery Change Per Session**
**Formula**:
```
Mastery_Velocity = (Mastery_After - Mastery_Before) / Session_Duration
```

**From Your System**:
- Mastery before: From previous session
- Mastery after: From current session
- Session duration: `time_stuck` or timestamp difference

**Example**:
```python
mastery_before = 0.25
mastery_after = 0.35
session_duration = 10  # minutes

velocity = (0.35 - 0.25) / 10 = 0.01 mastery points per minute
```

**✅ You Can Calculate**: From mastery history + session timestamps

---

### **3.2 Concept Acquisition Rate**
**Formula**:
```
Acquisition_Rate = New_Concepts_Learned / Sessions_Count
```

**From Your System**:
- New concepts: Concepts that went from mastery < 0.5 to > 0.7
- Sessions: `session_count` from Student State Tracker

**Example**:
```python
# Session 1: recursion mastery = 0.2
# Session 5: recursion mastery = 0.75 (learned!)

new_concepts = 1  # recursion
sessions = 5

acquisition_rate = 1 / 5 = 0.2 concepts per session
```

**✅ You Can Calculate**: From mastery history

---

### **3.3 Error Recovery Speed**
**Formula**:
```
Recovery_Speed = 1 / Sessions_To_Fix_Error
```

**From Your System**:
- Sessions to fix: Number of sessions until error no longer occurs

**Example**:
```python
# Session 1: RecursionError occurs
# Session 2: RecursionError occurs
# Session 3: No error! (fixed)

sessions_to_fix = 3
recovery_speed = 1 / 3 = 0.33
```

**✅ You Can Calculate**: From error tracking in sessions

---

## 🎯 **4. Diagnostic Accuracy Metrics** (Per Session)

### **4.1 Misconception Detection Precision**
**Formula**:
```
Precision = True_Positive_Misconceptions / Total_Detected_Misconceptions
```

**From Your System**:
- Detected misconceptions: From Pedagogical KG
- True positives: Misconceptions that match actual errors

**Example**:
```python
detected_misconceptions = ["missing_base_case", "wrong_recursion"]
actual_error = "RecursionError: maximum recursion depth exceeded"

# Check if detected matches actual
true_positives = 1  # "missing_base_case" matches
precision = 1 / 2 = 0.5
```

**✅ You Have This**: From HVSAE misconception detection

---

### **4.2 Knowledge Gap Identification Accuracy**
**Formula**:
```
Accuracy = Correctly_Identified_Gaps / Total_Gaps
```

**From Your System**:
- Identified gaps: From `_identify_gaps()`
- Correct gaps: Gaps that actually block learning

**Example**:
```python
identified_gaps = ["base_case", "functions", "loops"]
actual_blocking_gaps = ["base_case", "functions"]  # These actually block

accuracy = 2 / 3 = 0.67
```

**✅ You Can Calculate**: Compare identified vs actual performance

---

## 🔄 **5. Intervention Effectiveness Metrics** (Per Session)

### **5.1 Intervention Impact Score**
**Formula**:
```
Impact = (Mastery_After_Intervention - Mastery_Before_Intervention) / Intervention_Type_Weight
```

**From Your System**:
- Mastery before/after: From session data
- Intervention type: From orchestrator

**Example**:
```python
mastery_before = 0.25
mastery_after = 0.35
intervention_type = "visual_explanation"  # weight = 1.0

impact = (0.35 - 0.25) / 1.0 = 0.10
```

**✅ You Can Calculate**: From intervention + mastery changes

---

### **5.2 Intervention Efficiency**
**Formula**:
```
Efficiency = Mastery_Improvement / Time_Spent_On_Intervention
```

**From Your System**:
- Mastery improvement: Delta from intervention
- Time spent: Time between intervention and next session

**Example**:
```python
mastery_improvement = 0.10
time_spent = 5  # minutes

efficiency = 0.10 / 5 = 0.02 mastery points per minute
```

---

## 📈 **6. Cognitive Load Metrics** (Per Session)

### **6.1 Cognitive Load Reduction**
**Formula**:
```
Load_Reduction = (Initial_Load - Final_Load) / Initial_Load
```

**From Your System**:
- Initial load: From Pedagogical KG (before session)
- Final load: Updated after session (from struggle time)

**Example**:
```python
initial_load = 5  # High load
final_load = 3    # Reduced after explanation

reduction = (5 - 3) / 5 = 0.4 = 40% reduction
```

**✅ You Can Calculate**: From cognitive load updates

---

### **6.2 Struggle Time Ratio**
**Formula**:
```
Struggle_Ratio = Time_Stuck / Total_Session_Time
```

**From Your System**:
- `time_stuck`: From session data
- Total time: Sum of `time_deltas`

**Example**:
```python
time_stuck = 89.5  # seconds
total_time = sum(time_deltas) = 89.5  # seconds

struggle_ratio = 89.5 / 89.5 = 1.0  # 100% struggle (bad!)
```

**✅ You Have This**: `time_stuck` from session data

---

## 🧠 **7. Cognitive State Metrics** (Per Session)

### **7.1 Cognitive State Transition Rate**
**Formula**:
```
Transition_Rate = State_Changes / Total_Sessions
```

**From Your System**:
- State changes: Count transitions in cognitive state history
- **Source**: `cognitive_state['state_history']`

**Example**:
```python
state_history = ["confused", "confused", "understanding", "engaged"]
transitions = 2  # confused→understanding, understanding→engaged
sessions = 4

transition_rate = 2 / 4 = 0.5 transitions per session
```

**✅ You Have This**: Cognitive state history

---

### **7.2 Cognitive State Stability**
**Formula**:
```
Stability = 1.0 - (State_Changes / Total_Sessions)
```

**From Your System**:
- Lower changes = more stable (better)

**Example**:
```python
state_changes = 2
total_sessions = 10

stability = 1.0 - (2 / 10) = 0.8 = 80% stable
```

---

## 🎓 **8. Prerequisite Mastery Progression** (Per Session)

### **8.1 Prerequisite Completion Rate**
**Formula**:
```
Completion = Prerequisites_Mastered / Total_Prerequisites
```

**From Your System**:
- Prerequisites: From CSE-KG
- Mastered: Mastery > 0.7

**Example**:
```python
prerequisites = ["functions", "conditional_statements", "base_case"]
mastery = {
    "functions": 0.85,              # ✅ Mastered
    "conditional_statements": 0.90, # ✅ Mastered
    "base_case": 0.20               # ❌ Not mastered
}

completion = 2 / 3 = 0.67 = 67%
```

**✅ You Can Calculate**: From CSE-KG prerequisites + mastery levels

---

### **8.2 Learning Path Adherence**
**Formula**:
```
Adherence = Concepts_Learned_In_Order / Total_Concepts_In_Path
```

**From Your System**:
- Learning path: From Pedagogical KG progression
- Concepts learned: In order from mastery history

**Example**:
```python
expected_path = ["functions", "conditionals", "base_case", "recursion"]
actual_path = ["functions", "base_case", "recursion"]  # Skipped conditionals!

adherence = 2 / 4 = 0.5  # Only 50% followed path
```

---

## 🔍 **9. Error Pattern Metrics** (Per Session)

### **9.1 Error Type Distribution**
**Formula**:
```
Distribution = Count_Of_Error_Type / Total_Errors
```

**From Your System**:
- Error types: RecursionError, IndexError, TypeError, etc.
- Count: From error messages

**Example**:
```python
errors = ["RecursionError", "RecursionError", "IndexError"]
total = 3

recursion_error_rate = 2 / 3 = 0.67 = 67%
index_error_rate = 1 / 3 = 0.33 = 33%
```

**✅ You Can Calculate**: From error messages in sessions

---

### **9.2 Error Persistence Rate**
**Formula**:
```
Persistence = Sessions_With_Same_Error / Total_Sessions
```

**From Your System**:
- Same error: Same error type across sessions

**Example**:
```python
sessions = [
    {"error": "RecursionError"},
    {"error": "RecursionError"},
    {"error": "RecursionError"},
    {"error": None}  # Fixed!
]

persistence = 3 / 4 = 0.75 = 75% (high persistence = bad)
```

---

## ⏱️ **10. Response Time Metrics** (Per Session)

### **10.1 System Response Time**
**Formula**:
```
Response_Time = Time_To_Generate_Response (seconds)
```

**From Your System**:
- Measure: Time from session input to response output
- **Source**: Can add timing in orchestrator

**Example**:
```python
start_time = time.time()
response = orchestrator.process_session(session_data)
end_time = time.time()

response_time = end_time - start_time  # e.g., 2.3 seconds
```

---

### **10.2 Time to First Correct Code**
**Formula**:
```
Time_To_Correct = Timestamp_First_Correct - Timestamp_First_Session
```

**From Your System**:
- First correct: Session where `code_correctness > 0.8`
- **Source**: Conversation history timestamps

**Example**:
```python
first_session = "2025-01-01 10:00:00"
first_correct = "2025-01-01 10:15:00"  # 15 minutes later

time_to_correct = 15  # minutes
```

---

## 📊 **11. Knowledge Graph Utilization Metrics** (Per Session)

### **11.1 Graph Query Efficiency**
**Formula**:
```
Efficiency = Concepts_Retrieved / Queries_Made
```

**From Your System**:
- Queries: CSE-KG, Pedagogical KG, COKE queries
- Concepts: Unique concepts retrieved

**Example**:
```python
queries_made = 5  # CSE-KG, Pedagogical KG, COKE, etc.
concepts_retrieved = 12  # Unique concepts

efficiency = 12 / 5 = 2.4 concepts per query
```

---

### **11.2 Graph Coverage Score**
**Formula**:
```
Coverage = Concepts_From_Graphs / Total_Concepts_Needed
```

**From Your System**:
- Concepts from graphs: Retrieved from CSE-KG, Pedagogical KG
- Total needed: All concepts in student's learning path

**Example**:
```python
concepts_from_graphs = 8  # Retrieved from KGs
total_needed = 10

coverage = 8 / 10 = 0.8 = 80%
```

---

## 🎯 **12. Personalization Metrics** (Per Session)

### **12.1 Personalization Score**
**Formula**:
```
Personalization = (
    Learning_Style_Matched × 0.3 +
    Cognitive_State_Adapted × 0.3 +
    Knowledge_Gaps_Addressed × 0.2 +
    Misconceptions_Targeted × 0.2
)
```

**From Your System**:
- Learning style matched: Explanation matches student's style
- Cognitive state adapted: Tone matches cognitive state
- Knowledge gaps addressed: Gaps mentioned in explanation
- Misconceptions targeted: Detected misconceptions addressed

**Example**:
```python
learning_style_matched = 1.0  # ✅ Matched
cognitive_state_adapted = 0.8  # ✅ Mostly adapted
gaps_addressed = 1.0          # ✅ All addressed
misconceptions_targeted = 0.9  # ✅ Mostly targeted

personalization = (1.0×0.3 + 0.8×0.3 + 1.0×0.2 + 0.9×0.2) = 0.92
```

**✅ You Can Calculate**: From adaptive explanation analysis

---

### **12.2 Adaptation Accuracy**
**Formula**:
```
Accuracy = Correct_Adaptations / Total_Adaptations
```

**From Your System**:
- Correct adaptations: Adaptations that led to improvement

**Example**:
```python
adaptations = [
    {"type": "simpler_language", "result": "improved"},  # ✅
    {"type": "more_examples", "result": "improved"},     # ✅
    {"type": "visual_aid", "result": "no_change"}        # ❌
]

accuracy = 2 / 3 = 0.67
```

---

## 📋 **Complete List: Per-Session Metrics**

### **✅ Code Quality** (3 metrics):
1. Code Correctness Score ✅
2. Error Reduction Rate ✅
3. Code Complexity Score ✅

### **✅ Explanation Quality** (3 metrics):
4. Explanation Completeness ✅
5. Explanation Clarity Score ✅
6. Response Relevance Score ✅

### **✅ Learning Velocity** (3 metrics):
7. Mastery Change Per Session ✅
8. Concept Acquisition Rate ✅
9. Error Recovery Speed ✅

### **✅ Diagnostic Accuracy** (2 metrics):
10. Misconception Detection Precision ✅
11. Knowledge Gap Identification Accuracy ✅

### **✅ Intervention Effectiveness** (2 metrics):
12. Intervention Impact Score ✅
13. Intervention Efficiency ✅

### **✅ Cognitive Load** (2 metrics):
14. Cognitive Load Reduction ✅
15. Struggle Time Ratio ✅

### **✅ Cognitive State** (2 metrics):
16. Cognitive State Transition Rate ✅
17. Cognitive State Stability ✅

### **✅ Prerequisites** (2 metrics):
18. Prerequisite Completion Rate ✅
19. Learning Path Adherence ✅

### **✅ Error Patterns** (2 metrics):
20. Error Type Distribution ✅
21. Error Persistence Rate ✅

### **✅ Response Time** (2 metrics):
22. System Response Time ✅
23. Time to First Correct Code ✅

### **✅ Knowledge Graph** (2 metrics):
24. Graph Query Efficiency ✅
25. Graph Coverage Score ✅

### **✅ Personalization** (2 metrics):
26. Personalization Score ✅
27. Adaptation Accuracy ✅

---

## 🎯 **Top 10 Most Important Per-Session Metrics**

1. **Code Correctness Score** - Direct performance measure
2. **Mastery Change Per Session** - Learning progress
3. **Error Reduction Rate** - Problem-solving improvement
4. **Explanation Completeness** - Teaching quality
5. **Intervention Impact Score** - Teaching effectiveness
6. **Misconception Detection Precision** - Diagnostic accuracy
7. **Cognitive Load Reduction** - Learning efficiency
8. **Personalization Score** - Adaptation quality
9. **Error Recovery Speed** - Problem resolution
10. **Concept Acquisition Rate** - Learning velocity

---

## ✅ **Summary**

**27 Per-Session Metrics** that don't require multiple students:

- ✅ **Code Quality**: Correctness, error reduction, complexity
- ✅ **Explanation Quality**: Completeness, clarity, relevance
- ✅ **Learning Velocity**: Mastery change, acquisition rate, recovery speed
- ✅ **Diagnostic**: Misconception precision, gap accuracy
- ✅ **Intervention**: Impact, efficiency
- ✅ **Cognitive**: Load reduction, struggle ratio, state transitions
- ✅ **Prerequisites**: Completion rate, path adherence
- ✅ **Errors**: Type distribution, persistence
- ✅ **Time**: Response time, time to correct
- ✅ **Graphs**: Query efficiency, coverage
- ✅ **Personalization**: Score, adaptation accuracy

**All can be calculated from single student sessions!** 🎯








