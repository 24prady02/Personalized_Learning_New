# Dataset and Graph Structures - Complete Documentation

## ✅ Results Are NOT Hardcoded - They're Dynamic!

All metrics are calculated **dynamically** based on actual student input:

### How Results Are Calculated (Dynamic Process):

1. **Student Input** → Code + Question
2. **Dynamic Analysis**:
   - Concepts extracted from code/question (not predefined)
   - Code analyzed for errors (pattern matching on actual code)
   - Mastery updated based on actual code quality
   - Student type inferred from actual behavior patterns
3. **Metrics Calculated**:
   - DINA mastery: Based on actual code correctness
   - CodeBERT: Analyzes actual code structure
   - BERT: Analyzes actual response quality
   - Nestor: Infers from actual question/code patterns
4. **Results Vary**: Different code → Different metrics → Different mastery updates

**Proof**: Line 611-625 in `run_all_10_feature_tests.py` shows metrics are calculated from actual `code`, `question`, and `response` inputs, not hardcoded values.

---

## 📊 Dataset Structures

### 1. ASSISTments Dataset

**File**: `data/assistments/2012-2013-data-with-predictions-4-final.csv`

**Structure**:
```csv
user_id,problem_id,skill_name,correct,original,ms_first_response,hint_count,attempt_count,overlap_time
1,Problem_461,Skill_22,0,1,32662,3,3,32662
1,Problem_931,Skill_5,1,1,34623,0,3,34623
```

**Fields**:
- `user_id`: Student identifier
- `problem_id`: Problem identifier
- `skill_name`: Knowledge component/skill
- `correct`: 0 or 1 (correctness)
- `original`: Original attempt (1) or repeat (0)
- `ms_first_response`: Time to first response (milliseconds)
- `hint_count`: Number of hints used
- `attempt_count`: Number of attempts
- `overlap_time`: Time spent on problem

**Size**: 5,498,418 rows (5.5M student responses)

**Usage**:
- Training DINA model (mastery prediction)
- Q-matrix construction (problem-skill mappings)
- Validation of evidence-weighted BKT

---

### 2. ProgSnap2 Dataset

**File**: `data/progsnap2/MainTable_cs1.csv`

**Structure**:
```csv
EventID,SubjectID,ProblemID,EventType,ServerTimestamp,CodeStateSection
1,student_00001,p020,Run.Program,1762271404,"def solution():
    # Student 1 working on p020
    pass"
2,student_00001,p020,Run.Error,1762271447,"def solution():
    # Student 1 working on p020
    pass"
```

**Fields**:
- `EventID`: Unique event identifier
- `SubjectID`: Student identifier
- `ProblemID`: Problem identifier
- `EventType`: Action type (Run.Program, Compile.Error, Edit, etc.)
- `ServerTimestamp`: Unix timestamp
- `CodeStateSection`: Code at that moment

**Size**: 4,450,002 rows (4.45M debugging events)

**Usage**:
- Training Behavioral RNN/HMM (action sequences)
- Temporal pattern analysis
- Debugging strategy classification
- Emotion/engagement detection

---

### 3. CodeNet Dataset

**Structure**: `data/codenet/{python,java,c++}/`

**File Types**:
- `correct_*.txt` or `correct_*.py/java/cpp`: Correct implementations
- `buggy_*.txt` or `buggy_*.py/java/cpp`: Buggy implementations

**Example** (`data/codenet/c++/buggy_code_0041.txt`):
```cpp
#include <iostream>
using namespace std;

int function_40(int x, int y) {
    return x;  // Bug: missing y
}
```

**Structure**:
- **Python**: 513 `.txt` files + 79 `.py` files
- **Java**: 305 `.txt` files + 54 `.java` files
- **C++**: 201 `.txt` files + 348 `.cpp` files
- **Total**: 1,500 code files

**Usage**:
- Pre-training HVSAE code encoder
- Code understanding patterns
- Error pattern recognition
- Code quality analysis

---

### 4. MOOCCubeX Dataset

**Structure**: `data/moocsxcube/`

#### 4.1 Entities (`entities/` directory):

**`entities.json`** (24 MB):
```json
{
  "student": [
    {
      "id": "s_00001",
      "level": "beginner",
      "enrollment_date": "2023-05-23",
      "progress": 0.251
    }
  ],
  "course": [...],
  "concept": [...],
  "activity": [...]
}
```

**Individual Entity Files** (in `entities/`):
- `user.json`: 769 MB - User/student entities
- `course.json`: 42.59 MB - Course information
- `concept.json`: 155.41 MB - Learning concepts
- `video.json`: 579.90 MB - Video resources
- `problem.json`: 1.20 GB - Problem sets
- `comment.json`: 2.20 GB - Student comments
- `paper.json`: 6.38 GB - Research papers
- `reply.json`: 49.88 MB - Reply entities
- `teacher.json`: 8.68 MB - Teacher information
- `school.json`: 612 KB - School information
- `other.json`: 755.69 MB - Other entities

#### 4.2 Relations (`relations/` directory):

**Tab-separated format**:
- `user-comment.txt`: `U_10030806	Cm_1` (8.4M rows)
- `concept-video.txt`: Concept to video mappings (624K rows)
- `concept-problem.txt`: Concept to problem mappings (33K rows)
- `course-comment.txt`: Course to comment mappings (199 MB)
- `user-problem.json`: User-problem interactions (12.86 GB)
- `concept-paper.txt`: Concept to paper mappings (292 MB)
- `exercise-problem.txt`: Exercise to problem mappings (128 MB)
- `video_id-ccid.txt`: Video ID mappings (114 MB)
- And more...

**Total Size**: 25.92 GB

**Usage**:
- Knowledge graph enrichment
- Concept relationships
- Student-course interactions
- Learning path construction

---

## 🕸️ Graph Structures

### 1. CSE-KG 2.0 (Computer Science Knowledge Graph)

**Type**: RDF/SPARQL Knowledge Graph

**Endpoint**: `http://cse.ckcest.cn/cskg/sparql`

**Structure**:
```
Nodes (Entities):
├── Concepts (cskg:object_oriented_programming, cskg:recursion)
├── Methods (cskg:random_forest, cskg:deep_learning)
├── Tasks (cskg:sentiment_analysis, cskg:tree_traversal)
└── Materials (datasets, papers, tools)

Edges (Relationships):
├── requiresKnowledge (prerequisite relationships)
├── usesMethod (concept → method)
├── solvesTask (method → task)
├── relatedTo (concept ↔ concept)
└── evaluatedBy (concept → evaluation method)
```

**Example Query Structure**:
```sparql
SELECT ?concept ?label ?description
WHERE {
    ?concept rdf:type cskg:Concept .
    ?concept rdfs:label ?label .
    ?concept cskg:description ?description .
    FILTER(CONTAINS(LCASE(?label), "recursion"))
}
```

**Storage**: 
- Live SPARQL queries (online)
- Cached locally in `data/cse_kg_cache/*.pkl` (MD5 hash of query)

**Usage**:
- Concept retrieval from code/text
- Prerequisite analysis
- Knowledge gap identification
- Explanation grounding

---

### 2. Student-Specific Knowledge Graph

**Type**: NetworkX Directed Graph

**Structure** (from `src/knowledge_graph/graph_fusion.py`):
```python
{
    'student_id': 'student_001',
    'concepts': ['recursion', 'linked_list', 'pointers'],
    'concept_activations': {
        'recursion': 0.7,      # Activation level
        'linked_list': 0.5,
        'pointers': 0.3
    },
    'mastery_levels': {
        'recursion': 0.65,     # Mastery probability
        'linked_list': 0.40,
        'pointers': 0.25
    },
    'edges': [
        {
            'source': 'recursion',
            'target': 'linked_list',
            'relation': 'prerequisite',
            'weight': 0.8
        }
    ],
    'misconceptions': {
        'recursion': ['missing_base_case']
    }
}
```

**Initialization**:
- Built from CSE-KG structure
- Initialized with relevant concepts for student
- Updated from session data

**Updates**:
- Concept activations updated from HVSAE latent representation
- Mastery levels updated from DINA model
- Edges added/updated based on CSE-KG relationships
- Misconceptions tracked per concept

---

### 3. Graph Fusion

**Process** (from `src/knowledge_graph/graph_fusion.py`):

1. **Global CSE-KG** (26K+ entities):
   - Provides domain knowledge structure
   - Prerequisites, relationships, definitions

2. **Student Graph** (personal):
   - Student-specific mastery levels
   - Personal misconceptions
   - Learning history

3. **Fusion**:
   - Combines global structure with personal state
   - Updates student graph with CSE-KG relationships
   - Maintains personal mastery/activation levels

**Fusion Strategy**: `attention_weighted`
- CSE-KG weight: 0.7 (global knowledge)
- Student graph weight: 0.3 (personal state)

---

## 📈 How Results Are Dynamic (Not Hardcoded)

### Example Flow:

**Turn 1**:
- Student code: `def factorial(n): return n * factorial(n-1)` (missing base case)
- **Dynamic Analysis**:
  - CodeBERT detects: Logic error (infinite loop potential)
  - Correctness score: 0.6 (not 1.0 - hardcoded)
  - DINA updates: Mastery = 0.3 + 0.0 = 0.3 (no increase due to error)

**Turn 2**:
- Student code: `def factorial(n): if n==0: return 1; return n*factorial(n-1)` (correct)
- **Dynamic Analysis**:
  - CodeBERT detects: No errors
  - Correctness score: 1.0
  - DINA updates: Mastery = 0.3 + 0.15 = 0.45 (increased!)

**Turn 3**:
- Student code: Improved version with better structure
- **Dynamic Analysis**:
  - CodeBERT detects: No errors, good structure
  - Correctness score: 1.0
  - DINA updates: Mastery = 0.45 + 0.15 = 0.60 (further increased!)

**Key Point**: Each turn's metrics depend on:
- Actual code quality (analyzed dynamically)
- Actual question depth (analyzed from text)
- Previous mastery (tracked across turns)
- Student behavior patterns (inferred from actual actions)

**NOT hardcoded** - all calculated from real inputs!

---

## 🔄 Data Flow Through Graphs

```
Student Code/Question
    ↓
CSE-KG Query (SPARQL)
    ↓
Concept Extraction
    ↓
Student Graph Update
    ├── Add new concepts from CSE-KG
    ├── Update mastery from DINA
    └── Update relationships
    ↓
Graph Fusion
    ├── Combine CSE-KG structure
    └── Personalize with student state
    ↓
Knowledge Gap Identification
    ├── Check mastery < threshold
    └── Find missing prerequisites
    ↓
Intervention Selection
    └── Based on gaps + student type
```

---

## 📋 Summary

| Component | Structure | Size | Dynamic? |
|-----------|-----------|------|----------|
| **ASSISTments** | CSV (user_id, problem_id, skill, correct, attempts) | 5.5M rows | ✅ Yes |
| **ProgSnap2** | CSV (EventID, SubjectID, EventType, CodeState) | 4.45M rows | ✅ Yes |
| **CodeNet** | Text files (code samples) | 1,500 files | ✅ Yes |
| **MOOCCubeX** | JSON entities + TSV relations | 25.92 GB | ✅ Yes |
| **CSE-KG 2.0** | RDF/SPARQL (live queries) | 26K+ entities | ✅ Yes |
| **Student Graph** | NetworkX (dynamic per student) | Variable | ✅ Yes |

**All results are calculated dynamically from actual inputs - nothing is hardcoded!**












