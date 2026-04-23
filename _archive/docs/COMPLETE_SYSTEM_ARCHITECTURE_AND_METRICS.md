# Complete System Architecture: Datasets, CSE-KG 2.0, ML Models, and Accuracy Metrics

## 📊 **1. How Datasets Are Used**

### **1.1 ASSISTments Dataset (5.5M rows)**

**Purpose**: Training DINA model for mastery prediction

**Data Structure**:
```csv
user_id, problem_id, skill_name, correct, original, ms_first_response, hint_count, attempt_count, overlap_time
1, Problem_461, Skill_22, 0, 0, 28195, 3, 3, 32662
1, Problem_931, Skill_5, 0, 0, 29989, 0, 3, 34623
```

**How It's Used**:
1. **Q-Matrix Construction**: Maps problems → skills
   ```python
   Q_matrix = {
       "Problem_461": {"Skill_22": 1, "Skill_5": 0, ...},
       "Problem_931": {"Skill_22": 0, "Skill_5": 1, ...}
   }
   ```

2. **DINA Model Training**:
   - Input: Student responses (correct/incorrect) + Q-matrix
   - Output: Concept mastery probabilities
   - Training: Learns slip/guess parameters for each skill

3. **Evidence-Weighted BKT Validation**:
   - Uses `hint_count`, `attempt_count` to infer evidence strength
   - Validates mastery prediction accuracy

**Pipeline**:
```
ASSISTments CSV
    ↓
ASSISTmentsProcessor.process()
    ↓
Q-Matrix + Student Responses
    ↓
DINA Model Training
    ↓
Mastery Predictions (0.0 - 1.0 per skill)
```

---

### **1.2 ProgSnap2 Dataset (4.45M events)**

**Purpose**: Training Behavioral RNN/HMM for emotion/strategy detection

**Data Structure**:
```csv
EventID, SubjectID, ProblemID, EventType, ServerTimestamp, CodeStateSection
1, student_00001, p020, Run.Program, 1762271404, "def solution(): ..."
2, student_00001, p020, Run.Error, 1762271447, "def solution(): ..."
3, student_00001, p020, File.Edit, 1762271552, "def solution(): ..."
```

**How It's Used**:
1. **Action Sequence Extraction**:
   ```python
   Session = {
       "actions": ["Run.Program", "Run.Error", "File.Edit", "Run.Success"],
       "time_deltas": [0, 43, 105, 12],  # seconds
       "outcomes": [None, "error", None, "success"]
   }
   ```

2. **Behavioral RNN Training**:
   - Input: Action sequences + timestamps
   - Output: Emotion (frustrated, engaged, confused) + Strategy (systematic, exploratory)
   - Architecture: Bidirectional LSTM

3. **Behavioral HMM Training**:
   - Input: Action sequences
   - Output: Hidden states (stuck, progressing, debugging)
   - Architecture: Hidden Markov Model

**Pipeline**:
```
ProgSnap2 CSV
    ↓
ProgSnap2Processor.process()
    ↓
Action Sequences + Timestamps
    ↓
Behavioral RNN/HMM Training
    ↓
Emotion + Strategy Predictions
```

---

### **1.3 CodeNet Dataset (1,500 files)**

**Purpose**: Pre-training HVSAE code encoder

**Data Structure**:
```
data/codenet/
  ├── python/
  │   ├── correct_factorial.txt
  │   ├── buggy_factorial.txt
  │   └── ...
  ├── java/
  └── c++/
```

**How It's Used**:
1. **Code Understanding**:
   - Correct code → positive examples
   - Buggy code → negative examples
   - Trains CodeBERT encoder to understand code semantics

2. **HVSAE Pre-training**:
   - Input: Code snippets
   - Encoder: CodeBERT (microsoft/codebert-base)
   - Output: 768-dimensional code embeddings

**Pipeline**:
```
CodeNet Files
    ↓
CodeNetProcessor.process()
    ↓
Code Samples (correct/buggy)
    ↓
HVSAE Code Encoder (CodeBERT)
    ↓
Code Embeddings (768-dim)
```

---

### **1.4 MOOCCubeX Dataset (25.92 GB)**

**Purpose**: Knowledge graph enrichment + learning resource mapping

**Data Structure**:
```json
// entities.json
{
  "student": [{"id": "s_00001", "level": "beginner", ...}],
  "concept": [{"id": "K_001", "name": "recursion", ...}],
  "video": [{"id": "V_001", "title": "Introduction to Recursion", ...}],
  "problem": [{"id": "P_001", "difficulty": "medium", ...}]
}

// relations/concept-video.txt
K_001  V_001
K_001  V_002
```

**How It's Used**:
1. **Concept-Resource Mapping**:
   - Maps concepts → videos (624K relations)
   - Maps concepts → problems (33K relations)
   - Provides learning resources for each concept

2. **Learning Path Construction**:
   - Student progress tracking
   - Concept difficulty estimation
   - Personalized resource recommendations

**Pipeline**:
```
MOOCCubeX JSON/TSV
    ↓
MOOCCubeXProcessor.process()
    ↓
Concept-Resource Mappings
    ↓
Learning Resource Recommendations
```

---

## 🕸️ **2. CSE-KG 2.0 Structure**

### **2.1 Graph Structure**

**Type**: RDF/SPARQL Knowledge Graph

**Endpoint**: `http://cse.ckcest.cn/cskg/sparql`

**Namespace**: `http://cse.ckcest.cn/cskg/`

### **2.2 Entity Types**

```python
Entity Types:
├── Concept (cskg:Concept)
│   ├── Examples: recursion, object_oriented_programming, linked_list
│   └── Properties: label, description, broader, narrower
│
├── Method (cskg:Method)
│   ├── Examples: random_forest, deep_learning, quicksort
│   └── Properties: label, description, complexity
│
├── Task (cskg:Task)
│   ├── Examples: sentiment_analysis, tree_traversal, sorting
│   └── Properties: label, description, difficulty
│
└── Material (cskg:Material)
    ├── Examples: papers, datasets, tools
    └── Properties: title, type, url
```

### **2.3 Relationship Types**

```python
Relationships:
├── requiresKnowledge (Concept → Concept)
│   └── Example: recursion requiresKnowledge functions
│
├── isPrerequisiteOf (Concept → Concept)
│   └── Example: functions isPrerequisiteOf recursion
│
├── usesMethod (Concept → Method)
│   └── Example: tree_traversal usesMethod depth_first_search
│
├── solvesTask (Method → Task)
│   └── Example: quicksort solvesTask sorting
│
├── evaluatedBy (Concept → Metric)
│   └── Example: algorithm evaluatedBy time_complexity
│
└── relatedTo (Concept ↔ Concept)
    └── Example: recursion relatedTo iteration
```

### **2.4 SPARQL Query Structure**

**Example Query**:
```sparql
PREFIX cskg: <http://cse.ckcest.cn/cskg/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?concept ?label ?prereq WHERE {
    ?concept rdf:type cskg:Concept .
    ?concept rdfs:label ?label .
    ?concept cskg:requiresKnowledge ?prereq .
    FILTER(CONTAINS(LCASE(?label), "recursion"))
}
```

**Result**:
```json
{
  "concept": "cskg:recursion",
  "label": "Recursion",
  "prereq": "cskg:functions"
}
```

### **2.5 Caching Strategy**

**Local Cache**: `data/cse_kg_cache/*.pkl`

**Cache Key**: MD5 hash of SPARQL query

**Purpose**: Avoid repeated SPARQL queries for same concepts

---

## 🤖 **3. ML Architecture and Model Integration**

### **3.1 Complete Pipeline**

```
┌─────────────────────────────────────────────────────────────┐
│                    INPUT: Student Code/Question              │
└───────────────────────┬─────────────────────────────────────┘
                        │
        ┌───────────────┴───────────────┐
        │                               │
        ▼                               ▼
┌───────────────┐              ┌──────────────────┐
│   CodeBERT    │              │  CSE-KG 2.0      │
│   Encoder     │              │  Concept         │
│               │              │  Retrieval       │
└───────┬───────┘              └────────┬─────────┘
        │                               │
        │ Code Embeddings               │ Concepts
        │ (768-dim)                     │
        │                               │
        └───────────────┬───────────────┘
                        │
                        ▼
            ┌───────────────────────┐
            │      HVSAE Model      │
            │  (Multi-modal Fusion) │
            └───────────┬───────────┘
                        │
        ┌───────────────┼───────────────┐
        │               │               │
        ▼               ▼               ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│  DINA Model  │ │ Behavioral   │ │   Nestor     │
│  (Mastery)   │ │ RNN/HMM      │ │  (Personality│
│              │ │ (Emotion)    │ │   & Style)   │
└──────┬───────┘ └──────┬───────┘ └──────┬───────┘
       │                │                │
       │ Mastery        │ Emotion        │ Student Type
       │ Probabilities  │ + Strategy     │
       │                │                │
       └────────────────┼────────────────┘
                        │
                        ▼
            ┌───────────────────────┐
            │  Intervention         │
            │  Orchestrator         │
            │  (Personalized        │
            │   Response)           │
            └───────────────────────┘
```

### **3.2 HVSAE (Hyperspherical Variational Self-Attention Autoencoder)**

**Purpose**: Multi-modal encoding of student state

**Architecture**:
```python
Inputs:
├── Code: CodeBERT encoder → 768-dim embeddings
├── Text: BERT encoder → 768-dim embeddings
└── Behavior: LSTM encoder → 256-dim embeddings

Self-Attention:
├── 8 attention heads
├── 512-dimensional features
└── Multi-modal fusion

Latent Space:
├── 256-dimensional hypersphere
├── von Mises-Fisher distribution
└── kappa = 100 (concentration parameter)

Decoders:
├── GNN Decoder: Knowledge graph updates
├── Transformer Decoder: Explanation generation
└── MLP Classifier: Misconception detection
```

**Training**:
- **Loss Function**: Reconstruction + KL Divergence + Misconception Classification
- **Data**: CodeNet (code) + ASSISTments (text) + ProgSnap2 (behavior)
- **Optimizer**: AdamW (lr=0.0001)

---

### **3.3 DINA Model (Deterministic Input, Noisy And)**

**Purpose**: Cognitive diagnosis - estimate concept mastery

**Architecture**:
```python
Input:
├── Student responses (correct/incorrect)
├── Q-matrix (problem-skill mappings)
└── Slip/Guess parameters (learned)

Output:
└── Mastery probabilities per concept [0.0 - 1.0]

Parameters:
├── Slip (s): Probability of error when mastered
├── Guess (g): Probability of correct when not mastered
└── Mastery (α): Binary mastery state per concept
```

**Training**:
- **Data**: ASSISTments (5.5M responses)
- **Method**: Expectation-Maximization (EM) algorithm
- **Output**: Concept mastery probabilities

**Example**:
```python
Student responses:
  Problem_1 (requires: recursion, base_case) → Correct
  Problem_2 (requires: recursion) → Incorrect

DINA Output:
  recursion: 0.7 (70% mastery)
  base_case: 0.9 (90% mastery)
```

---

### **3.4 Behavioral RNN**

**Purpose**: Detect emotion and debugging strategy

**Architecture**:
```python
Input:
├── Action sequence: ["Run.Program", "Run.Error", "File.Edit", ...]
├── Time deltas: [0, 43, 105, 12]
└── Outcomes: [None, "error", None, "success"]

Architecture:
├── Bidirectional LSTM
├── 2 layers, 128 hidden dimensions
└── Dropout: 0.2

Output:
├── Emotion: [frustrated, engaged, confused, systematic, exploratory]
└── Strategy: [systematic, exploratory, help-seeking]
```

**Training**:
- **Data**: ProgSnap2 (4.45M events)
- **Loss**: Cross-entropy for emotion classification
- **Optimizer**: AdamW (lr=0.001)

---

### **3.5 Nestor Bayesian Network**

**Purpose**: Psychological profiling and learning style inference

**Architecture**:
```python
Input:
├── Behavioral patterns (from RNN)
├── Question analysis (depth, type)
└── Code patterns (complexity, errors)

Bayesian Network:
├── Personality Traits (Big Five)
│   ├── Openness
│   ├── Conscientiousness
│   ├── Extraversion
│   ├── Agreeableness
│   └── Neuroticism
│
├── Learning Styles (Felder-Silverman)
│   ├── Visual/Verbal
│   ├── Active/Reflective
│   ├── Sequential/Global
│   └── Sensing/Intuitive
│
└── Learning Strategies
    ├── Elaboration
    ├── Organization
    ├── Critical Thinking
    └── Metacognitive Self-Regulation

Output:
└── Student Type + Intervention Recommendations
```

---

## 📈 **4. Accuracy Metrics**

### **4.1 Misconception Detection Metrics**

**From**: `src/utils/metrics.py`

```python
Metrics:
├── Accuracy: (TP + TN) / (TP + TN + FP + FN)
├── Precision: TP / (TP + FP)  # Weighted average
├── Recall: TP / (TP + FN)     # Weighted average
├── F1-Score: 2 * (Precision * Recall) / (Precision + Recall)
└── AUC-ROC: Area under ROC curve (weighted)
```

**Usage**: Multi-label classification (student can have multiple misconceptions)

**Example**:
```python
Predictions: [0.8, 0.3, 0.9]  # Probabilities for 3 misconceptions
Targets:     [1, 0, 1]         # Actual misconceptions

Accuracy: 0.67 (2/3 correct)
Precision: 0.85
Recall: 0.90
F1: 0.87
```

---

### **4.2 Mastery Prediction Metrics**

**From**: `src/utils/metrics.py`

```python
Metrics:
├── MSE (Mean Squared Error): Mean((predicted - actual)²)
├── MAE (Mean Absolute Error): Mean(|predicted - actual|)
├── RMSE (Root Mean Squared Error): √MSE
└── Correlation: Pearson correlation coefficient
```

**Usage**: Regression task (mastery is continuous 0.0-1.0)

**Example**:
```python
Predicted Mastery: [0.7, 0.5, 0.9]
Actual Mastery:    [0.8, 0.4, 0.95]

MSE: 0.01
MAE: 0.05
RMSE: 0.10
Correlation: 0.98
```

---

### **4.3 Emotion Classification Metrics**

**From**: `src/utils/metrics.py`

```python
Metrics:
├── Accuracy: Correct predictions / Total
├── Precision: Macro-averaged (per emotion class)
├── Recall: Macro-averaged (per emotion class)
└── F1-Score: Macro-averaged (per emotion class)
```

**Usage**: Multi-class classification (5 emotions: frustrated, engaged, confused, systematic, exploratory)

**Example**:
```python
Predicted: ["frustrated", "engaged", "confused"]
Actual:    ["frustrated", "frustrated", "confused"]

Accuracy: 0.67 (2/3 correct)
Precision: 0.75 (macro-averaged)
Recall: 0.70 (macro-averaged)
F1: 0.72 (macro-averaged)
```

---

### **4.4 BKT Validation Metrics (ASSISTments)**

**From**: `validate_on_assistments.py`

```python
Metrics:
├── AUC-ROC: Area under ROC curve (mastery prediction)
├── Accuracy: Correct mastery predictions
├── RMSE: Root mean squared error (mastery probability)
└── Correlation: Pearson correlation (predicted vs actual)
```

**Evidence-Weighted BKT Innovation**:
```python
Standard BKT: Always uses evidence strength = 1.0
Your BKT: Adapts strength based on hints/attempts

Evidence Strength:
├── No hints, 1 attempt → 0.9 (strong evidence)
├── Some hints, 2 attempts → 0.7 (moderate evidence)
└── Many hints, 3+ attempts → 0.6 (weak evidence)
```

**Results** (from validation):
- **AUC-ROC**: ~0.75-0.85 (better than standard BKT)
- **Accuracy**: ~70-80%
- **RMSE**: ~0.15-0.25

---

### **4.5 Intervention Recommendation Metrics**

**From**: `src/utils/metrics.py`

```python
Metrics:
├── Success Rate: Successful interventions / Total recommended
└── Match Rate: Recommended interventions / Total successful
```

**Example**:
```python
Recommended: ["visual_explanation", "guided_practice", "motivational_support"]
Successful:  ["visual_explanation", "guided_practice"]

Success Rate: 0.67 (2/3 successful)
Match Rate: 1.0 (all successful were recommended)
```

---

## 🔄 **5. Complete Data Flow**

### **5.1 Training Pipeline**

```
1. Data Loading:
   ASSISTments → DINA training data
   ProgSnap2 → Behavioral RNN training data
   CodeNet → HVSAE pre-training data
   MOOCCubeX → Knowledge graph enrichment

2. Model Training:
   HVSAE: Multi-task learning (reconstruction + misconception)
   DINA: EM algorithm on ASSISTments
   Behavioral RNN: Sequence-to-sequence on ProgSnap2
   Nestor: Bayesian inference (no training needed)

3. Validation:
   ASSISTments → BKT validation (AUC-ROC, RMSE)
   ProgSnap2 → Emotion classification (Accuracy, F1)
   CodeNet → Code understanding (Embedding quality)
```

### **5.2 Inference Pipeline**

```
1. Student Input:
   Code + Question + Error Message

2. Concept Retrieval:
   CSE-KG 2.0 → Extract concepts from code/text
   MOOCCubeX → Find related resources

3. Multi-Modal Encoding:
   CodeBERT → Code embeddings
   BERT → Text embeddings
   LSTM → Behavior embeddings
   HVSAE → Fused representation

4. Model Predictions:
   DINA → Mastery probabilities
   Behavioral RNN → Emotion + Strategy
   Nestor → Student type + Learning style

5. Intervention Generation:
   Orchestrator → Personalized response
   Content Generator → Explanation + Examples
```

---

## 📊 **6. Summary Table**

| Component | Dataset | Model | Output | Metrics |
|-----------|---------|-------|--------|---------|
| **Code Understanding** | CodeNet | HVSAE (CodeBERT) | Code embeddings | Embedding quality |
| **Mastery Prediction** | ASSISTments | DINA | Mastery probabilities | AUC-ROC, RMSE, Correlation |
| **Emotion Detection** | ProgSnap2 | Behavioral RNN | Emotion + Strategy | Accuracy, F1, Precision |
| **Concept Retrieval** | CSE-KG 2.0 | ConceptRetriever | Concepts + Prerequisites | Retrieval accuracy |
| **Resource Mapping** | MOOCCubeX | Query Engine | Videos + Problems | Recommendation accuracy |
| **Personality Profiling** | All | Nestor | Student type | Classification accuracy |
| **Intervention** | All | Orchestrator | Personalized response | Success rate, Match rate |

---

## 🎯 **Key Insights**

1. **CSE-KG 2.0** is the backbone for concept retrieval and knowledge structure
2. **MOOCCubeX** enriches with learning resources and student interactions
3. **ASSISTments** trains mastery prediction (DINA)
4. **ProgSnap2** trains emotion/strategy detection (Behavioral RNN)
5. **CodeNet** pre-trains code understanding (HVSAE)
6. **All datasets** work together through HVSAE's multi-modal fusion
7. **Accuracy metrics** vary by task (classification vs regression vs retrieval)

The system is a **multi-modal, multi-task learning architecture** that combines:
- **Knowledge graphs** (CSE-KG 2.0, MOOCCubeX) for domain knowledge
- **Deep learning** (HVSAE, RNN) for pattern recognition
- **Cognitive models** (DINA, BKT) for mastery prediction
- **Psychological models** (Nestor) for personalization















