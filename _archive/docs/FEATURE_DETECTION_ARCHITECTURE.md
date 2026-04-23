# Feature Detection Architecture: What Detects What

## Overview

This document explains:
1. **Which architectures/models detect each feature**
2. **How detected information feeds into the 10 personalization features**
3. **The complete data flow from detection → personalization**

---

## Detection Architecture Map

```
┌─────────────────────────────────────────────────────────────────┐
│                    INPUT: Student Message + Code                │
└───────────────────────┬─────────────────────────────────────────┘
                        │
        ┌───────────────┼───────────────┐
        │               │               │
        ▼               ▼               ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│   HVSAE      │ │   Nestor     │ │ Behavioral   │
│  (Encoding)  │ │  (Personality│ │    RNN       │
│              │ │   Profiling) │ │  (Emotion)   │
└──────┬───────┘ └──────┬───────┘ └──────┬───────┘
       │                │                │
       ▼                ▼                ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│   DINA       │ │     BKT      │ │   CSE-KG     │
│ (Cognitive   │ │ (Knowledge   │ │  (Domain     │
│  Diagnosis)  │ │  Tracking)   │ │  Knowledge)  │
└──────┬───────┘ └──────┬───────┘ └──────┬───────┘
       │                │                │
       └────────────────┼────────────────┘
                        │
                        ▼
            ┌───────────────────────┐
            │  Unified Student State│
            │  (All Detections)     │
            └───────────┬───────────┘
                        │
                        ▼
        ┌───────────────────────────────┐
        │  10 Personalization Features  │
        │  (Use Detected Information)   │
        └───────────────────────────────┘
```

---

## Detection → Feature Mapping

### 1️⃣ **HVSAE (Hyperspherical Variational Autoencoder)**

**What it detects:**
- Multi-modal encoding of student input
- Latent representation of student state
- Code understanding (via CodeBERT encoder)
- Text understanding (via BERT encoder)
- Behavioral patterns (via LSTM encoder)

**Architecture:**
```
Input (Code + Text + Actions)
    ↓
[CodeBERT Encoder] → Code embeddings
[BERT Encoder] → Text embeddings  
[LSTM Encoder] → Behavioral sequences
    ↓
[8-head Self-Attention] → Fusion
    ↓
[256-dim vMF Latent Space] → Unified representation
```

**Feeds into which features:**
- **Feature 3 (Learning Style)**: Latent representation helps identify learning patterns
- **Feature 7 (Format Preferences)**: Code understanding helps determine code style preferences
- **Feature 8 (Error Detection)**: Code analysis detects errors

**Detection Output:**
```python
{
    'latent_representation': tensor([...]),  # 256-dim vector
    'code_embedding': tensor([...]),
    'text_embedding': tensor([...]),
    'behavioral_embedding': tensor([...])
}
```

---

### 2️⃣ **Nestor Bayesian Network**

**What it detects:**
- **Big Five Personality Traits** (Openness, Conscientiousness, Extraversion, Agreeableness, Neuroticism)
- **Learning Style Preferences** (Visual, Conceptual, Practical, Sequential)
- **Cognitive Style** (Systematic, Exploratory)
- **Intervention Preferences**

**Architecture:**
```
Student Language Patterns
    ↓
[Bayesian Network Inference]
    ↓
Question_Pattern → Learning_Preference
    ↓
Learning_Preference → Cognitive_Style
    ↓
Cognitive_Style → Conscientiousness
    ↓
All Traits → Intervention_Selection
```

**Detection Logic:**
```python
# Example: Detects personality from language
if "why" in message or "how" in message:
    learning_preference = 'conceptual'  # P=0.85
if provides_complete_code:
    conscientiousness = 0.70  # High
if asks_many_questions:
    openness = 0.75  # High
```

**Feeds into which features:**
- ✅ **Feature 3 (Learning Style)**: Uses `learning_preference` directly
- ✅ **Feature 4 (Personality)**: Uses all Big Five traits
- ✅ **Feature 7 (Format Preferences)**: Uses conscientiousness for structure preference

**Detection Output:**
```python
{
    'personality': {
        'openness': 0.75,
        'conscientiousness': 0.70,
        'extraversion': 0.60,
        'agreeableness': 0.65,
        'neuroticism': 0.45
    },
    'learning_preference': 'conceptual',
    'cognitive_style': 'systematic',
    'learning_style': 'visual_sequential'
}
```

---

### 3️⃣ **Behavioral RNN (Recurrent Neural Network)**

**What it detects:**
- **Emotional State** (Confused, Frustrated, Neutral, Engaged, Confident)
- **Frustration Level** (0.0 - 1.0)
- **Engagement Score** (0.0 - 1.0)
- **Behavioral Patterns** (Systematic, Exploratory, Stuck, Productive)
- **Dropout Risk** (0.0 - 1.0)

**Architecture:**
```
Action Sequence + Timing Data
    ↓
[Bidirectional LSTM]
    ↓
[Emotion Classifier] → 5 emotion classes
[Engagement Predictor] → Engagement score
[Frustration Detector] → Frustration level
    ↓
[HMM State Inference] → Behavioral pattern
```

**Detection Logic:**
```python
# Example: Detects emotion from patterns
if "don't understand" in message:
    emotion = 'confused'
    frustration_level = 0.65
if time_stuck > 120:  # 2 minutes
    frustration_level += 0.2
if action_sequence.count('run_test') > 3:
    emotion = 'frustrated'
    engagement_score = 0.40  # Low
```

**Feeds into which features:**
- ✅ **Feature 2 (Emotional Intelligence)**: Uses emotion, frustration, engagement
- ✅ **Feature 8 (Error Feedback)**: Uses frustration to adjust hint level
- ✅ **Feature 10 (Difficulty & Pacing)**: Uses emotion/engagement for pacing

**Detection Output:**
```python
{
    'emotion': 'confused',
    'frustration_level': 0.65,
    'engagement_score': 0.55,
    'behavioral_pattern': 'systematic_struggling',
    'dropout_risk': 0.35
}
```

---

### 4️⃣ **DINA (Diagnostic Item Nonparametric Analysis)**

**What it detects:**
- **Concept Mastery Estimates** (per skill/concept)
- **Knowledge Component Mapping** (Q-matrix)
- **Slip and Guess Parameters**
- **Skill Proficiency Levels**

**Architecture:**
```
Student Response History
    ↓
[Q-Matrix Mapping] → Skills required for each problem
    ↓
[DINA Model] → P(Y_ij = 1) = (1-s_j)^(η_ij) × g_j^(1-η_ij)
    ↓
[Bayesian Estimation] → Mastery probabilities
```

**Detection Logic:**
```python
# DINA formula
P(correct) = (1 - slip)^(has_skills) × guess^(1 - has_skills)

# Example
if student_has_skills(['base_case', 'recursion']):
    mastery['recursion'] = 0.65
else:
    mastery['recursion'] = 0.30
```

**Feeds into which features:**
- ✅ **Feature 5 (Progress)**: Provides baseline mastery estimates
- ✅ **Feature 10 (Difficulty)**: Uses mastery to determine difficulty level

**Detection Output:**
```python
{
    'skill_mastery': {
        'recursion': 0.45,
        'base_case': 0.30,
        'functions': 0.85
    },
    'overall_mastery': 0.53
}
```

---

### 5️⃣ **BKT (Bayesian Knowledge Tracing)**

**What it detects:**
- **Knowledge Probability P(L)** for each skill (0.0 - 1.0)
- **Learning Rate P(T)**
- **Evidence-Weighted Updates** (from NLP analysis)
- **Knowledge State Transitions** (struggling → emerging → developing → mastered)
- **Mastery Changes** (before/after each interaction)

**Architecture:**
```
Previous P(L) + Current Evidence
    ↓
[NLP Evidence Extraction] → Evidence strength (0.0-1.0)
    ↓
[Bayesian Update] → P(L|evidence) = P(evidence|L) × P(L) / P(evidence)
    ↓
[Evidence Weighting] → P(L_weighted) = evidence × P(L|evidence) + (1-evidence) × P(L_old)
    ↓
[Learning Application] → P(L_new) = P(L_weighted) + (1-P(L_weighted)) × P(T)
```

**Detection Logic:**
```python
# Evidence extraction from language
if "I don't understand" in message:
    evidence_strength = 0.8  # Strong confusion
    correctness = False
elif "Oh I see!" in message:
    evidence_strength = 0.7  # Strong understanding
    correctness = True

# Bayesian update
P(L_new) = bayesian_update(P(L_old), evidence_strength, correctness)
```

**Feeds into which features:**
- ✅ **Feature 1 (Conversation Memory)**: Tracks mastery history for trajectory
- ✅ **Feature 5 (Progress)**: Provides mastery change calculations
- ✅ **Feature 9 (Metacognitive)**: Uses mastery trends for strategy suggestions
- ✅ **Feature 10 (Difficulty)**: Uses current P(L) to determine difficulty

**Detection Output:**
```python
{
    'bkt_update': {
        'p_learned_before': 0.30,
        'p_learned_after': 0.45,
        'change': 0.15,
        'attempts': 3,
        'status': 'developing'  # struggling/emerging/developing/mastered
    },
    'knowledge_state': {
        'overall_mastery': 0.45,
        'mastery_history': [0.30, 0.35, 0.40, 0.45]
    }
}
```

---

### 6️⃣ **CSE-KG (Computer Science Knowledge Graph)**

**What it detects:**
- **Concept Definitions** and relationships
- **Prerequisites** for concepts
- **Common Misconceptions**
- **Better Mental Models**
- **Teaching Approaches** (per learning style)
- **Concept Progression** (emerging → developing → mastered)

**Architecture:**
```
Concept Name (e.g., "recursion")
    ↓
[SPARQL Query] → CSE-KG 2.0 Endpoint
    ↓
[Knowledge Retrieval] → Concept info, prerequisites, misconceptions
    ↓
[Teaching Approach Selection] → Based on learning style + BKT status
```

**Detection Logic:**
```python
# SPARQL query example
query = """
SELECT ?prerequisite WHERE {
    cskg:recursion cskg:requiresKnowledge ?prerequisite
}
"""

# Retrieves:
knowledge = {
    'name': 'Recursion',
    'prerequisites': ['functions', 'base_case', 'conditional_statements'],
    'common_misconceptions': ['Recursion is just loops', 'Base case is optional'],
    'better_mental_model': 'Recursion is like Russian dolls',
    'teaching_approach': {
        'visual_learners': 'Use call stack diagrams',
        'conceptual_learners': 'Explain mathematical induction'
    }
}
```

**Feeds into which features:**
- ✅ **Feature 3 (Learning Style)**: Provides teaching approaches per style
- ✅ **Feature 5 (Progress)**: Provides progression content for mastery level
- ✅ **Feature 8 (Error Feedback)**: Provides misconceptions to address

**Detection Output:**
```python
{
    'kg_knowledge': {
        'name': 'Recursion',
        'definition': '...',
        'prerequisites': ['functions', 'base_case'],
        'common_misconceptions': ['Recursion is just loops'],
        'better_mental_model': 'Like Russian dolls',
        'teaching_approach': {
            'visual_learners': 'Use call stack diagrams',
            'conceptual_learners': 'Explain mathematical induction'
        },
        'progression': {
            'emerging': 'Basic recursion concept',
            'developing': 'Recursive thinking patterns',
            'mastered': 'Advanced recursion techniques'
        }
    }
}
```

---

### 7️⃣ **Code Analysis (AST Parser + Pattern Matching)**

**What it detects:**
- **Syntax Errors**
- **Logic Errors** (initialization, off-by-one, null checks)
- **Code Quality** (complexity, comments, structure)
- **Understanding Indicators** (shows understanding vs confusion)
- **Error Locations** (exact line numbers)

**Architecture:**
```
Student Code
    ↓
[AST Parser] → Parse tree
    ↓
[Pattern Matching] → Error detection
    ↓
[Complexity Analysis] → Code quality
    ↓
[Understanding Analysis] → Shows understanding?
```

**Detection Logic:**
```python
# AST parsing
tree = ast.parse(code)

# Error detection
if 'max_num = 0' in code:
    errors.append({
        'type': 'initialization_error',
        'line': 2,
        'issue': 'Fails for negative numbers',
        'fix': 'Use numbers[0] or float("-inf")'
    })

# Understanding indicators
if node_count > 15 and '#' in code:
    shows_understanding = True
```

**Feeds into which features:**
- ✅ **Feature 8 (Error Feedback)**: Provides exact error details
- ✅ **Feature 5 (Progress)**: Code quality affects BKT evidence strength

**Detection Output:**
```python
{
    'code_analysis': {
        'has_code': True,
        'errors': [{
            'type': 'initialization_error',
            'line': 2,
            'severity': 'high',
            'issue': 'Fails for negative numbers',
            'fix': 'Use numbers[0] or float("-inf")'
        }],
        'quality_indicators': {
            'complexity': 25,
            'has_comments': True,
            'shows_understanding': False
        }
    }
}
```

---

## Complete Feature → Detection Mapping

### Feature 1: Conversation Memory & Context
**Uses:**
- BKT (mastery history for trajectory)
- Conversation history (stored interactions)
- Behavioral RNN (emotion history)

**Detected by:**
- BKT: Mastery trends
- System: Conversation storage
- Behavioral RNN: Emotion patterns

---

### Feature 2: Emotional Intelligence & Tone Adaptation
**Uses:**
- Behavioral RNN: emotion, frustration_level, engagement_score
- BKT: mastery (for celebration detection)

**Detected by:**
- Behavioral RNN: Primary detector
- BKT: Secondary (for progress celebration)

---

### Feature 3: Learning Style Deep Personalization
**Uses:**
- Nestor: learning_preference, learning_style
- CSE-KG: teaching_approach per learning style
- HVSAE: latent representation (for style inference)

**Detected by:**
- Nestor: Primary detector
- CSE-KG: Provides teaching approaches
- HVSAE: Supports style inference

---

### Feature 4: Personality-Based Communication
**Uses:**
- Nestor: All Big Five traits (openness, conscientiousness, extraversion, agreeableness, neuroticism)

**Detected by:**
- Nestor: Only detector

---

### Feature 5: Progress-Aware Responses
**Uses:**
- BKT: p_learned_before, p_learned_after, change, mastery_history
- DINA: Baseline mastery estimates
- CSE-KG: Progression content for mastery level

**Detected by:**
- BKT: Primary detector (mastery changes)
- DINA: Baseline estimates
- CSE-KG: Progression content

---

### Feature 6: Interest & Context Personalization
**Uses:**
- Student Profile: interests, hobbies, career_goals (manually provided or inferred)

**Detected by:**
- Manual input or inference from conversation topics
- Not directly detected by models (requires student input)

---

### Feature 7: Response Format Preferences
**Uses:**
- Conversation History: response_length, has_diagrams, engagement
- Nestor: conscientiousness (for structure preference)
- HVSAE: Code style analysis

**Detected by:**
- Conversation History: Primary (what worked before)
- Nestor: Personality-based preferences
- HVSAE: Code style analysis

---

### Feature 8: Error-Specific & Diagnostic Feedback
**Uses:**
- Code Analysis: errors, error_type, error_location, error_issue, error_fix
- Behavioral RNN: frustration_level (for hint level)
- CSE-KG: common_misconceptions

**Detected by:**
- Code Analysis: Primary detector
- Behavioral RNN: Adjusts hint level
- CSE-KG: Provides misconceptions

---

### Feature 9: Metacognitive & Learning Strategy Support
**Uses:**
- BKT: mastery_history, mastery trends
- Behavioral RNN: emotion (for self-regulation)
- Conversation History: interaction patterns

**Detected by:**
- BKT: Mastery trends
- Behavioral RNN: Emotion patterns
- Conversation History: Learning patterns

---

### Feature 10: Adaptive Difficulty & Pacing
**Uses:**
- BKT: current mastery (P(L))
- Behavioral RNN: emotion, engagement (for pacing)
- DINA: Baseline mastery

**Detected by:**
- BKT: Primary (current mastery)
- Behavioral RNN: Emotion/engagement for pacing
- DINA: Baseline estimates

---

## Complete Data Flow

```
┌─────────────────────────────────────────────────────────────┐
│                    STUDENT INPUT                            │
│  Message: "Why does my code fail?"                         │
│  Code: def find_max(numbers): max_num = 0 ...              │
└───────────────────────┬─────────────────────────────────────┘
                        │
        ┌───────────────┼───────────────┐
        │               │               │
        ▼               ▼               ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│   HVSAE      │ │   Nestor     │ │ Behavioral   │
│              │ │              │ │    RNN       │
│ Detects:     │ │ Detects:     │ │ Detects:     │
│ - Code emb   │ │ - Learning   │ │ - Emotion:   │
│ - Text emb   │ │   style:     │ │   confused   │
│ - Latent rep │ │   visual     │ │ - Frust: 0.65│
│              │ │ - Personality│ │ - Engage:0.55│
└──────┬───────┘ └──────┬───────┘ └──────┬───────┘
       │                │                │
       ▼                ▼                ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│   DINA       │ │     BKT      │ │   CSE-KG     │
│              │ │              │ │              │
│ Detects:     │ │ Detects:     │ │ Detects:     │
│ - Mastery:   │ │ - P(L): 0.30 │ │ - Concept:   │
│   0.45       │ │ - Change:    │ │   recursion  │
│              │ │   +0.15      │ │ - Misconcept │
└──────┬───────┘ └──────┬───────┘ └──────┬───────┘
       │                │                │
       └────────────────┼────────────────┘
                        │
                        ▼
            ┌───────────────────────┐
            │  Unified Analysis     │
            │  {                    │
            │    emotion: confused  │
            │    frustration: 0.65  │
            │    learning_style:    │
            │      visual           │
            │    mastery: 0.45      │
            │    ...                │
            │  }                    │
            └───────────┬───────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│           10 PERSONALIZATION FEATURES                       │
│                                                             │
│ Feature 2: Emotional → Uses emotion, frustration           │
│ Feature 3: Learning Style → Uses learning_style            │
│ Feature 4: Personality → Uses personality traits           │
│ Feature 5: Progress → Uses mastery, change                 │
│ Feature 8: Error → Uses code_analysis                      │
│ Feature 10: Difficulty → Uses mastery, emotion             │
│ ...                                                         │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
            ┌───────────────────────┐
            │  Personalized Prompt  │
            │  (All 10 contexts)    │
            └───────────┬───────────┘
                        │
                        ▼
            ┌───────────────────────┐
            │   LLM Generation      │
            │   (Groq Llama-3.1)    │
            └───────────┬───────────┘
                        │
                        ▼
            ┌───────────────────────┐
            │  Personalized Response│
            └───────────────────────┘
```

---

## Summary Table

| Feature | Primary Detector | Secondary Detector | What It Uses |
|---------|-----------------|-------------------|--------------|
| **1. Conversation Memory** | BKT, History | Behavioral RNN | Mastery history, emotion patterns |
| **2. Emotional Intelligence** | Behavioral RNN | BKT | Emotion, frustration, engagement |
| **3. Learning Style** | Nestor | CSE-KG, HVSAE | Learning preference, teaching approaches |
| **4. Personality** | Nestor | - | Big Five traits |
| **5. Progress** | BKT | DINA, CSE-KG | Mastery changes, progression content |
| **6. Interests** | Manual/Inference | - | Student profile |
| **7. Format Preferences** | History | Nestor, HVSAE | What worked, personality, code style |
| **8. Error Feedback** | Code Analysis | Behavioral RNN, CSE-KG | Errors, frustration, misconceptions |
| **9. Metacognitive** | BKT | Behavioral RNN, History | Mastery trends, emotion patterns |
| **10. Difficulty & Pacing** | BKT | Behavioral RNN, DINA | Mastery, emotion, engagement |

---

**This shows exactly which architectures detect what, and how that information flows into the 10 personalization features!** 🎯

















