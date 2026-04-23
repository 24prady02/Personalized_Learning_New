# COKE Graph vs Pedagogical Graph - What They Represent

## 🧠 **COKE COGNITIVE GRAPH** - What It Represents

### **Purpose:**
COKE (Cognitive Knowledge Graph) represents **student mental states and behavioral patterns** - it's a **Theory of Mind** model that predicts how students think and act.

### **What It Models:**

1. **Cognitive States** (Mental Activities)
   - `confused` - Student doesn't understand
   - `frustrated` - Student is stuck/annoyed
   - `understanding` - Student is grasping the concept
   - `engaged` - Student is actively working
   - `insight` - Student has a breakthrough moment
   - `perceiving`, `believing`, `desiring`, `intending`, `knowing`

2. **Behavioral Responses** (What Students Do)
   - `ask_question` - Student asks for help
   - `search_info` - Student looks up documentation
   - `try_again` - Student attempts to fix code again
   - `continue` - Student keeps working
   - `give_up` - Student stops trying
   - `explain` - Student explains to others

3. **Cognitive Chains** (Mental State → Behavior)
   - **Pattern**: When student is in state X, they typically do action Y
   - **Example**: `confused` → `try_again` (32.6% probability, 32,599 evidence occurrences)
   - **Example**: `confused` → `continue` (63.9% probability, 63,941 evidence occurrences)

4. **Theory of Mind** (Why Students Act)
   - Predicts: "Why did the student go wrong?"
   - Infers: Student's reasoning and mental model
   - Explains: What the student believes vs. what's correct

### **What COKE Graph Represents:**
```
Student Mental State → Behavioral Response → Affective Response
     (confused)      →    (try_again)      →   (frustrated)
```

**COKE = "How students think and react"**

---

## 📚 **PEDAGOGICAL KNOWLEDGE GRAPH** - What It Represents

### **Purpose:**
Pedagogical KG represents **teaching knowledge and learning needs** - it's a **pedagogical model** that knows how to teach and what students struggle with.

### **What It Models:**

1. **Misconceptions** (What Students Get Wrong)
   - **198 misconceptions** learned from CodeNet + MOOCCubeX
   - **Types**:
     - Code errors (from CodeNet): Missing base case, IndexError, etc.
     - Prerequisite confusion (from MOOCCubeX): Wrong prerequisite beliefs
     - Concept confusion: Mixing up similar concepts
   - **Each includes**: Description, severity, frequency, correction strategy, evidence

2. **Learning Progressions** (How to Teach Concepts)
   - Optimal sequence: Basic → Intermediate → Advanced
   - **Example**: `variables` → `functions` → `recursion`
   - Includes difficulty levels and mastery checkpoints

3. **Cognitive Load** (How Hard Concepts Are)
   - **Intrinsic Load**: Complexity of concept itself
   - **Extraneous Load**: Unnecessary difficulty (errors, confusion)
   - **Germane Load**: Productive learning effort
   - Helps determine if content is too complex

4. **Interventions** (How to Help Students)
   - Teaching strategies for each misconception
   - Explanation approaches (visual, verbal, examples)
   - Scaffolding techniques
   - Remediation paths

5. **Error Patterns** (Common Mistakes)
   - Recognizes error types and maps to concepts
   - Provides quick diagnosis

6. **Root Causes** (Why Errors Happen)
   - Traces errors back to missing prerequisites
   - Identifies foundational gaps

### **What Pedagogical KG Represents:**
```
Concept → Misconceptions → Correction Strategy → Intervention
(recursion) → (no base case) → (show examples) → (guided practice)
```

**Pedagogical KG = "What students struggle with and how to teach them"**

---

## 🔄 **KEY DIFFERENCES**

| Aspect | COKE Graph | Pedagogical Graph |
|--------|------------|-------------------|
| **Focus** | Student mental state & behavior | Teaching knowledge & misconceptions |
| **Question** | "How is the student thinking?" | "What does the student not know?" |
| **Represents** | Cognitive processes | Pedagogical content |
| **Predicts** | Behavioral responses | Learning needs |
| **Learned From** | ProgSnap2 (behavioral patterns) | CodeNet + MOOCCubeX (errors & concepts) |
| **Output** | Cognitive state, Theory of Mind | Misconceptions, interventions, progressions |

---

## 🤝 **HOW THEY WORK TOGETHER**

### **Example: Student with Recursion Error**

**COKE Graph Analysis:**
```
Student is: confused
Will likely: try_again (32.6% probability)
Theory of Mind: "Student believes recursion doesn't need base case"
Why wrong: Missing understanding of base case necessity
```

**Pedagogical Graph Analysis:**
```
Detected: mc_recursion_no_base_case misconception
Severity: critical
Frequency: 0.75 (75% of students make this mistake)
Correction: "Explain base case necessity with examples"
Intervention: Show base case examples with visual diagrams
```

**Combined Response:**
- **COKE** tells us: Student is confused and will keep trying
- **Pedagogical** tells us: They have a misconception about base cases
- **Together**: System provides targeted intervention before student gets frustrated

---

## 📊 **DATA REPRESENTATION**

### **COKE Graph Structure:**
```python
CognitiveChain(
    mental_activity="confused",
    behavioral_response="try_again",
    context="encountering_error",
    frequency=0.326,  # 32.6% of confused students try again
    confidence=1.0,   # High confidence from 32,599 evidence occurrences
    source="progsnap2"
)
```

### **Pedagogical Graph Structure:**
```python
Misconception(
    id="mc_recursion_no_base_case",
    concept="recursion",
    description="Believes recursion doesn't need a base case",
    severity="critical",
    frequency=0.75,  # 75% of students make this mistake
    evidence_count=140,  # From 140 CodeNet buggy files
    correction_strategy="Explain base case necessity with examples",
    source="codenet"
)
```

---

## 🎯 **SUMMARY**

**COKE Graph = Psychology of Learning**
- Represents: How students think, feel, and behave
- Answers: "What's going on in the student's mind?"
- Used for: Predicting behavior, understanding motivation, Theory of Mind

**Pedagogical Graph = Content Knowledge**
- Represents: What students don't know and how to teach them
- Answers: "What does the student need to learn?"
- Used for: Detecting misconceptions, selecting interventions, planning lessons

**Together**: They provide complete understanding of both the **student's mental state** (COKE) and **what they need to learn** (Pedagogical), enabling truly personalized teaching! 🎓

