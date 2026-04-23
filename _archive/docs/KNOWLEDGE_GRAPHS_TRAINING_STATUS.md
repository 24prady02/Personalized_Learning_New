# Knowledge Graphs Training Status

## Summary

**Not all knowledge graphs are trained on datasets.** Here's the breakdown:

---

## ✅ **TRAINED Knowledge Graphs** (From Datasets)

### **1. COKE Cognitive Graph** ✅ TRAINED

**Status**: ✅ Trained from ProgSnap2 dataset

**Training Script**: `scripts/learn_coke_chains_from_progsnap2.py`

**Dataset Used**: ProgSnap2 (50K+ debugging sessions)

**What It Learns**:
- Cognitive state → Behavioral response chains
- Theory of Mind patterns
- Mental activity patterns (confused → ask_question, frustrated → try_again, etc.)

**Output File**: `data/pedagogical_kg/coke_chains.json`

**Example Learned Chain**:
```json
{
  "id": "chain_confused_to_ask",
  "mental_activity": "confused",
  "behavioral_response": "ask_question",
  "frequency": 0.72,  // Learned from ProgSnap2
  "confidence": 0.85
}
```

**Usage**: 
- Loaded in `src/knowledge_graph/coke_cognitive_graph.py`
- Used for cognitive state inference and behavioral prediction

---

### **2. Pedagogical KG (Misconceptions)** ✅ TRAINED

**Status**: ✅ Trained from CodeNet and ASSISTments datasets

**Training Scripts**:
- `scripts/learn_misconceptions_from_codenet.py` - Learns from buggy code patterns
- `scripts/learn_misconceptions_from_assistments.py` - Learns from student responses

**Datasets Used**:
- **CodeNet**: 14M code submissions (buggy code patterns)
- **ASSISTments**: 500K+ student responses (common errors)

**What It Learns**:
- Common misconception patterns
- Error type → Concept mappings
- Misconception frequency and severity
- Correction strategies

**Output Files**:
- `data/pedagogical_kg/misconceptions_codenet.json`
- `data/pedagogical_kg/misconceptions_assistments.json`

**Example Learned Misconception**:
```json
{
  "id": "mc_recursion_no_base_case",
  "concept": "recursion",
  "description": "Believes recursion doesn't need a base case",
  "frequency": 0.78,  // Learned from CodeNet
  "evidence_count": 1247,  // Updated from dataset training
  "severity": "critical"
}
```

**Usage**:
- Loaded in `src/knowledge_graph/pedagogical_kg.py`
- Used for misconception detection and correction strategy selection

---

### **3. Learning Progressions** ✅ TRAINED

**Status**: ✅ Trained from MOOCCubeX dataset

**Training Script**: `scripts/learn_progressions_from_mooccubex.py`

**Dataset Used**: MOOCCubeX (2.1M student activities)

**What It Learns**:
- Concept prerequisite sequences
- Optimal learning paths
- Concept relationships and dependencies

**Output File**: `data/pedagogical_kg/learning_progressions.json`

**Usage**:
- Used for learning path recommendations
- Prerequisite analysis

---

## ❌ **NOT TRAINED Knowledge Graphs** (External or Dynamic)

### **1. CSE-KG (Computer Science Knowledge Graph)** ❌ EXTERNAL

**Status**: ❌ **NOT trained by us** - It's an external pre-existing knowledge graph

**Source**: CSE-KG 2.0 (http://cse.ckcest.cn/cskg/sparql)

**What It Is**:
- Pre-existing Computer Science Knowledge Graph
- 26,000+ CS entities (Concepts, Methods, Tasks, Materials)
- Relationships: requiresKnowledge, usesMethod, solvesTask
- Accessed via SPARQL endpoint

**How We Use It**:
- Query via SPARQL endpoint (`src/knowledge_graph/cse_kg_client.py`)
- Cache queries locally for performance
- Use for domain knowledge, prerequisites, concept definitions

**Why Not Trained**:
- It's a **pre-existing external resource**
- We query it, not train it
- It's maintained by the CSE-KG 2.0 project

**Files**:
- `src/knowledge_graph/cse_kg_client.py` - SPARQL client
- Cache: `data/cse_kg_cache/*.pkl`

---

### **2. Student Graph** ❌ DYNAMIC (Not Trained)

**Status**: ❌ **NOT trained from datasets** - Built dynamically per-student

**What It Is**:
- Individual student mastery tracking graph
- Built and updated in real-time during sessions
- Tracks concept-specific mastery, knowledge gaps, learning history

**How It's Built**:
- Created per-student by `src/orchestrator/student_state_tracker.py`
- Updated dynamically from student interactions
- Uses DINA model for mastery estimation

**Why Not Trained**:
- It's **student-specific** and built dynamically
- Each student has their own graph
- Updated in real-time, not pre-trained

**Files**:
- `src/orchestrator/student_state_tracker.py` - Student graph builder

---

## 📊 **Training Summary**

| Knowledge Graph | Trained? | Dataset | Training Script |
|----------------|----------|---------|-----------------|
| **COKE Cognitive Graph** | ✅ YES | ProgSnap2 | `learn_coke_chains_from_progsnap2.py` |
| **Pedagogical KG (Misconceptions)** | ✅ YES | CodeNet + ASSISTments | `learn_misconceptions_from_codenet.py`<br>`learn_misconceptions_from_assistments.py` |
| **Learning Progressions** | ✅ YES | MOOCCubeX | `learn_progressions_from_mooccubex.py` |
| **CSE-KG** | ❌ NO | N/A (External) | N/A (External resource) |
| **Student Graph** | ❌ NO | N/A (Dynamic) | N/A (Built per-student) |

---

## 🔄 **Orchestrating All Training**

**Main Training Script**: `scripts/learn_all_metrics_from_datasets.py`

This script runs all training scripts in sequence:
1. Misconceptions from CodeNet
2. COKE chains from ProgSnap2
3. Misconceptions from ASSISTments
4. Learning Progressions from MOOCCubeX
5. Cognitive Load (dynamic)
6. Intervention Effectiveness (dynamic)
7. Merge all learned data

**To Train All Graphs**:
```bash
python scripts/learn_all_metrics_from_datasets.py
```

---

## ✅ **Answer to Your Question**

**"All knowledge graphs have been trained upon datasets, right?"**

**Answer**: **Not all of them!**

- ✅ **COKE Graph**: YES - Trained from ProgSnap2
- ✅ **Pedagogical KG (Misconceptions)**: YES - Trained from CodeNet + ASSISTments
- ✅ **Learning Progressions**: YES - Trained from MOOCCubeX
- ❌ **CSE-KG**: NO - External pre-existing knowledge graph (we query it, not train it)
- ❌ **Student Graph**: NO - Built dynamically per-student (not trained from datasets)

**3 out of 5 knowledge graphs are trained from datasets.**

---

## 📝 **Notes**

1. **CSE-KG is external**: It's a pre-existing knowledge graph maintained by the CSE-KG 2.0 project. We use it as a domain knowledge backbone, but we don't train it.

2. **Student Graph is dynamic**: Each student gets their own graph built in real-time. It's not pre-trained because it's student-specific.

3. **Training scripts exist**: All training scripts are in `scripts/` directory and can be run to update the learned knowledge graphs.

4. **Learned data takes priority**: When learned data exists (e.g., `coke_chains.json`), the system uses it. Otherwise, it falls back to default/hardcoded values.

---

**Last Updated**: November 2024






