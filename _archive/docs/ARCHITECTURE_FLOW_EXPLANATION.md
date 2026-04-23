# Architecture Flow: HVSAE, Feature Learning, and Knowledge Graph

## Your Understanding: ✅ Mostly Correct!

You're right about the general flow, but let me clarify the exact details:

---

## 🎯 The Complete Flow

```
┌─────────────────────────────────────────────────────────────┐
│              STUDENT INPUT (Current Interaction)            │
│  Message: "Why does my code fail?"                         │
│  Code: def find_max(numbers): max_num = 0 ...              │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│  STEP 1: HVSAE - Semantic Pattern Extraction               │
│  (Pre-trained on CodeNet, Applied to Current Input)        │
└───────────────────────┬─────────────────────────────────────┘
                        │
        ┌───────────────┼───────────────┐
        │               │               │
        ▼               ▼               ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│ Code Embedding│ │ Text Embedding│ │ Behavioral   │
│ (CodeBERT)   │ │ (BERT)       │ │ (LSTM)       │
│              │ │              │ │              │
│ Semantic     │ │ Semantic     │ │ Semantic     │
│ Patterns     │ │ Patterns     │ │ Patterns     │
└──────┬───────┘ └──────┬───────┘ └──────┬───────┘
       │                │                │
       └────────────────┼────────────────┘
                        │
                        ▼
        ┌───────────────────────────┐
        │ 8-Head Self-Attention     │
        │ (Fuses all modalities)    │
        └───────────┬───────────────┘
                    │
                    ▼
        ┌───────────────────────────┐
        │ 256-dim vMF Latent Space  │
        │ (Unified Semantic Rep)    │
        └───────────┬───────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────────┐
│  STEP 2: Feature Learning (Using Learned Patterns)         │
│  (Models Apply Learned Patterns to Current Input)          │
└───────────────────────┬─────────────────────────────────────┘
                        │
        ┌───────────────┼───────────────┐
        │               │               │
        ▼               ▼               ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│ Behavioral   │ │    Nestor    │ │     DINA     │
│    RNN       │ │  (Personality│ │  (Mastery)   │
│              │ │   Inference) │ │              │
│ Uses learned │ │ Real-time    │ │ Uses learned │
│ patterns from│ │ inference    │ │ patterns from│
│ ProgSnap2    │ │ from current │ │ ASSISTments  │
│              │ │ input        │ │              │
└──────┬───────┘ └──────┬───────┘ └──────┬───────┘
       │                │                │
       └────────────────┼────────────────┘
                        │
                        ▼
        ┌───────────────────────────┐
        │  Unified Student State    │
        │  (All Features Detected)  │
        └───────────┬───────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────────┐
│  STEP 3: Knowledge Graph - Specific Pattern Retrieval      │
│  (Retrieves Domain Knowledge for Detected Concepts)        │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
        ┌───────────────────────────┐
        │  CSE-KG Query             │
        │  Concept: "recursion"     │
        │  (Detected from input)    │
        └───────────┬───────────────┘
                    │
                    ▼
        ┌───────────────────────────┐
        │  Retrieved Knowledge:     │
        │  - Definition             │
        │  - Prerequisites          │
        │  - Misconceptions         │
        │  - Teaching approaches    │
        └───────────┬───────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────────┐
│  STEP 4: Personalization (10 Features)                     │
│  (Combines All: Patterns + Knowledge + State)              │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
            ┌───────────────────────┐
            │  Personalized Response│
            └───────────────────────┘
```

---

## 📊 Detailed Breakdown

### STEP 1: HVSAE - Semantic Pattern Extraction

**What HVSAE does:**
- **Learns semantic patterns** from CodeNet (offline training)
- **Extracts semantic patterns** from current student input (real-time)

**How it works:**

```python
# OFFLINE: Learn semantic patterns from CodeNet
hvsae.pretrain_on_codenet(CodeNet_dataset)
# Learns:
# - Code semantic patterns (what code means)
# - Text semantic patterns (what text means)
# - Behavioral semantic patterns (what actions mean)

# REAL-TIME: Extract semantic patterns from current input
current_input = {
    'code': "def find_max(numbers): max_num = 0 ...",
    'text': "Why does my code fail?",
    'actions': ['code_edit', 'run_test', 'error']
}

# HVSAE extracts semantic patterns
code_embedding = hvsae.code_encoder(current_input['code'])
# → Semantic pattern: "initialization error pattern"
# → Semantic pattern: "max function pattern"
# → Semantic pattern: "negative number handling pattern"

text_embedding = hvsae.text_encoder(current_input['text'])
# → Semantic pattern: "confusion pattern"
# → Semantic pattern: "why question pattern"
# → Semantic pattern: "error debugging pattern"

behavioral_embedding = hvsae.behavioral_encoder(current_input['actions'])
# → Semantic pattern: "stuck pattern"
# → Semantic pattern: "trial and error pattern"
```

**Output:**
```python
{
    'latent_representation': tensor([...]),  # 256-dim semantic representation
    'semantic_patterns': {
        'code': 'initialization_error',
        'text': 'confusion_question',
        'behavior': 'stuck_pattern'
    }
}
```

---

### STEP 2: Feature Learning (Using Learned Patterns)

**What happens:**
- Models use **learned patterns** (from datasets) + **semantic patterns** (from HVSAE)
- Apply to current student input to detect features

**How it works:**

#### A. Behavioral RNN (Uses Learned Patterns)

```python
# Learned patterns (from ProgSnap2 training):
# - "3 failed test runs" → frustrated emotion
# - "long time stuck" → high frustration
# - "quick success" → engaged emotion

# Apply to current input:
current_actions = ['code_edit', 'run_test', 'run_test', 'run_test']
# Matches learned pattern: "multiple test runs" → frustrated

emotion = behavioral_rnn.predict(current_actions)
# Uses learned semantic patterns to detect: emotion = 'frustrated'
```

#### B. Nestor (Real-Time Inference from Semantic Patterns)

```python
# Uses semantic patterns from HVSAE text embedding
text_semantic = hvsae.text_embedding  # "why question pattern"

# Infers personality from semantic patterns
if "why" in semantic_patterns:
    learning_preference = 'conceptual'  # Inferred from semantic pattern
```

#### C. DINA (Uses Learned Patterns)

```python
# Learned patterns (from ASSISTments training):
# - "Wrong on recursion problems" → low recursion mastery
# - "Correct on base case" → high base case mastery

# Apply to current input:
current_response = analyze_student_code()
# Matches learned pattern: "missing base case" → low mastery

mastery = dina.estimate(current_response)
# Uses learned patterns to estimate: mastery = 0.30
```

---

### STEP 3: Knowledge Graph - Specific Pattern Retrieval

**What happens:**
- **Detects concept** from semantic patterns (from HVSAE)
- **Retrieves specific knowledge** from CSE-KG for that concept

**How it works:**

```python
# Step 1: Detect concept from semantic patterns
semantic_patterns = hvsae.latent_representation
# Contains: "recursion pattern", "base case pattern", "error pattern"

# Step 2: Extract concept name
detected_concept = extract_concept(semantic_patterns)
# → "recursion"

# Step 3: Query Knowledge Graph for specific patterns
kg_knowledge = cse_kg_client.get_concept_info("recursion")
# Retrieves SPECIFIC patterns:
# - Pattern: "Recursion requires base case"
# - Pattern: "Common misconception: recursion = loops"
# - Pattern: "Teaching approach for visual learners: call stack diagrams"
# - Pattern: "Prerequisites: functions, conditionals"

# Step 4: Get teaching patterns for student's learning style
learning_style = nestor.learning_preference  # "visual"
teaching_pattern = kg_knowledge['teaching_approach'][learning_style]
# → "Use call stack diagrams" (specific pattern for visual learners)
```

**What Knowledge Graph provides:**
- **Specific teaching patterns** (for detected learning style)
- **Specific misconception patterns** (to address)
- **Specific prerequisite patterns** (to check)
- **Specific mental model patterns** (to use)

---

## 🔄 Complete Flow Example

```
Student Input:
  Code: "def factorial(n): return n * factorial(n-1)"
  Message: "Why does this fail?"

┌─────────────────────────────────────────────────────────────┐
│ STEP 1: HVSAE Extracts Semantic Patterns                   │
└─────────────────────────────────────────────────────────────┘
Code Semantic Patterns:
  - "recursion pattern" (detected)
  - "missing base case pattern" (detected)
  - "infinite recursion pattern" (detected)

Text Semantic Patterns:
  - "why question pattern" (detected)
  - "confusion pattern" (detected)
  - "error debugging pattern" (detected)

Latent Representation: [256-dim vector with all patterns]

┌─────────────────────────────────────────────────────────────┐
│ STEP 2: Feature Learning (Apply Learned Patterns)          │
└─────────────────────────────────────────────────────────────┘
Behavioral RNN:
  - Uses learned pattern: "why question" → confused emotion
  - Detects: emotion = 'confused'

Nestor:
  - Uses semantic pattern: "why question" → conceptual learner
  - Detects: learning_preference = 'conceptual'

DINA:
  - Uses learned pattern: "missing base case" → low mastery
  - Detects: mastery = 0.30

Code Analysis:
  - Uses semantic pattern: "missing base case pattern"
  - Detects: error = 'missing_base_case'

┌─────────────────────────────────────────────────────────────┐
│ STEP 3: Knowledge Graph Retrieves Specific Patterns        │
└─────────────────────────────────────────────────────────────┘
Concept Detected: "recursion" (from semantic patterns)

CSE-KG Retrieves:
  - Specific pattern: "Recursion requires base case"
  - Specific pattern: "Common misconception: recursion = loops"
  - Specific pattern: "Teaching approach for conceptual learners: 
    Explain mathematical induction and recursive thinking"
  - Specific pattern: "Prerequisites: functions, conditionals"

┌─────────────────────────────────────────────────────────────┐
│ STEP 4: Personalization (Combine All)                      │
└─────────────────────────────────────────────────────────────┘
All Information Combined:
  - Semantic patterns (from HVSAE)
  - Learned patterns (from models)
  - Specific knowledge patterns (from CSE-KG)
  - Student state (emotion, personality, mastery)

→ Generates personalized response using all patterns
```

---

## 🎯 Key Points

### ✅ **HVSAE:**
- **Learns semantic patterns** from CodeNet (offline)
- **Extracts semantic patterns** from current input (real-time)
- Provides **unified semantic representation**

### ✅ **Feature Learning:**
- **Uses learned patterns** (from datasets) to detect features
- **Applies to current input** using semantic patterns from HVSAE
- Detects: emotion, personality, mastery, errors

### ✅ **Knowledge Graph:**
- **Retrieves specific patterns** for detected concepts
- **Provides domain knowledge** (not inferred, retrieved)
- **Specific teaching patterns** for student's learning style

---

## 📊 Pattern Types

### 1. **Semantic Patterns** (HVSAE)
- What code/text/behavior **means**
- Learned from CodeNet
- Extracted from current input

### 2. **Learned Patterns** (Models)
- What patterns **indicate** (emotion, mastery, etc.)
- Learned from datasets (ProgSnap2, ASSISTments)
- Applied to current input

### 3. **Knowledge Patterns** (CSE-KG)
- What **domain knowledge** says
- Retrieved from knowledge graph
- Specific to detected concepts

---

## 🔍 Example: Pattern Flow

```
Input: "Why does my recursion code fail?"

1. HVSAE Semantic Patterns:
   - Code: "recursion pattern", "missing base case pattern"
   - Text: "why question pattern", "confusion pattern"

2. Feature Learning (Using Learned Patterns):
   - Behavioral RNN: "confusion pattern" → emotion = confused
   - Nestor: "why question pattern" → learning_preference = conceptual
   - Code Analysis: "missing base case pattern" → error detected

3. Knowledge Graph Retrieval (Specific Patterns):
   - Concept: "recursion" (from semantic patterns)
   - Retrieves: "Teaching pattern for conceptual learners: 
     Explain mathematical induction"
   - Retrieves: "Common misconception: recursion = loops"

4. Personalization:
   - Combines: Semantic + Learned + Knowledge patterns
   - Generates: Personalized response for conceptual learner
     explaining recursion with mathematical induction
```

---

## ✅ Your Understanding: Correct!

**You're right:**
1. ✅ **HVSAE gets semantic patterns** (learned from CodeNet, extracted from input)
2. ✅ **Features are learned** (using learned patterns from datasets)
3. ✅ **Knowledge graph retrieves specific patterns** (for detected concepts)

**The flow is:**
```
Semantic Patterns (HVSAE) 
    ↓
Feature Learning (Using Learned Patterns)
    ↓
Knowledge Graph Retrieval (Specific Patterns)
    ↓
Personalization (Combine All)
```

**Perfect understanding!** 🎯

















