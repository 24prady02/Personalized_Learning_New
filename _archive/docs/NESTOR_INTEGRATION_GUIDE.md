# Nestor Bayesian Network Integration Guide

## 🎯 **Overview**

This guide explains how Nestor Bayesian Network is integrated into the system for improved personality-based inference.

**Based on**: ECSEE 2025 Paper - "Nestor: A Personalized Learning Path Recommendation Algorithm"

---

## 📊 **What is Nestor?**

Nestor is a **hybrid Bayesian Network** that models the relationships between:
- **Big Five Inventory (BFI) Personalities** (5 traits)
- **Felder-Silverman Learning Style Dimensions** (4 dimensions)
- **LISTK Learning Strategies** (4 strategies)
- **Learning Elements** (9 types)

**Structure**:
```
BFI Personalities (P1-P5)
    ↓
    ├─→ Learning Styles (D1-D4)
    ├─→ Learning Strategies (T1-T4)
    └─→ Learning Elements (L)
```

---

## 🔧 **Implementation**

### **1. Synthetic Data Generation**

**Script**: `scripts/generate_nestor_synthetic_personality_data.py`

**Purpose**: Generate synthetic personality data for training Nestor BN

**Usage**:
```bash
python scripts/generate_nestor_synthetic_personality_data.py
```

**Output**:
- `data/nestor/synthetic_{size}/nestor_synthetic_personality_data.csv`
- `data/nestor/synthetic_{size}/nestor_synthetic_personality_data.json`
- `data/nestor/synthetic_{size}/nestor_metadata.json`

**Sizes Generated**: 50, 100, 500, 1000, 5000, 10000 (as in the paper)

---

### **2. Nestor Bayesian Profiler**

**File**: `src/models/nestor/nestor_bayesian_profiler.py`

**Class**: `NestorBayesianProfiler`

**Features**:
- ✅ Personality inference from behavioral data
- ✅ Learning style inference from personality
- ✅ Learning strategy inference from personality
- ✅ Learning element preference prediction
- ✅ Complete inference pipeline

**Methods**:
```python
# Complete inference pipeline
result = profiler.complete_inference(behavioral_data)
# Returns:
# {
#   'personality': {...},
#   'learning_styles': {...},
#   'learning_strategies': {...},
#   'learning_element_preferences': {...},
#   'recommended_elements': [...]
# }
```

---

### **3. Integration with Orchestrator**

**File**: `src/orchestrator/orchestrator.py`

**Changes**:
1. **`_get_personality_profile()`**: Now uses Nestor profiler first
2. **`_assess_psychology()`**: Uses Nestor learning styles if available
3. **`_extract_behavioral_data_for_nestor()`**: Extracts behavioral indicators from session

**Behavioral Indicators Extracted**:
- `exploration_rate`: How many different actions tried
- `persistence`: Time spent before giving up
- `organization`: Code structure quality
- `social_interaction`: Frequency of help-seeking
- `emotional_variability`: Variance in time between actions

---

## 🚀 **Setup Instructions**

### **Step 1: Install Dependencies**

```bash
pip install -r requirements.txt
```

**New dependency**: `bayesnestor>=0.1.0`

### **Step 2: Generate Synthetic Data**

```bash
python scripts/generate_nestor_synthetic_personality_data.py
```

This generates synthetic datasets of various sizes (50, 100, 500, 1000, 5000, 10000).

### **Step 3: Initialize Nestor Profiler**

```bash
python scripts/initialize_nestor_profiler.py
```

This initializes the profiler and tests inference.

### **Step 4: Use in System**

```python
from src.models.nestor.nestor_bayesian_profiler import NestorBayesianProfiler

# Initialize
profiler = NestorBayesianProfiler(config)

# Add to models dictionary
models['nestor_profiler'] = profiler

# Orchestrator will automatically use it!
```

---

## 📈 **How It Works**

### **Inference Pipeline**:

1. **Behavioral Data Extraction**:
   ```python
   behavioral_data = {
       'exploration_rate': 0.7,      # From action diversity
       'persistence': 0.6,            # From time spent
       'organization': 0.8,           # From code structure
       'social_interaction': 0.5,      # From help-seeking
       'emotional_variability': 0.4    # From time variance
   }
   ```

2. **Personality Inference** (P1-P5):
   ```python
   personality = {
       'openness': 0.65,              # From exploration
       'conscientiousness': 0.75,     # From organization + persistence
       'extraversion': 0.50,          # From social interaction
       'agreeableness': 0.55,         # Default with variation
       'neuroticism': 0.40            # From emotional variability
   }
   ```

3. **Learning Style Inference** (D1-D4):
   ```python
   learning_styles = {
       'visual_verbal': 'visual',      # High openness → visual
       'sensing_intuitive': 'intuitive',  # High openness → intuitive
       'active_reflective': 'active',  # High extraversion → active
       'sequential_global': 'sequential'  # High conscientiousness → sequential
   }
   ```

4. **Learning Strategy Inference** (T1-T4):
   ```python
   learning_strategies = {
       'deep_processing': 0.70,       # Openness + Conscientiousness
       'elaboration': 0.65,           # Openness
       'organization': 0.75,          # Conscientiousness
       'metacognition': 0.68          # Conscientiousness + Openness
   }
   ```

5. **Learning Element Prediction** (L):
   ```python
   element_preferences = {
       'VAM': 0.25,  # Video Animation (high openness, visual)
       'MS': 0.20,    # Multimedia Simulation
       'EX': 0.18,    # Exercise (active)
       ...
   }
   ```

---

## ✅ **Benefits**

1. **Better Accuracy**: Bayesian Network captures probabilistic relationships
2. **Research-Based**: Based on validated psychological models
3. **Complete Pipeline**: Personality → Styles → Strategies → Elements
4. **Synthetic Data**: Can train on generated data when real data is scarce
5. **Fallback Support**: Works even if bayesnestor library is not available

---

## 🔄 **Fallback Behavior**

If `bayesnestor` library is not available:
- Uses probabilistic rules based on research correlations
- Still provides personality inference
- Still provides learning style inference
- Logs warning but continues operation

---

## 📊 **Example Output**

```json
{
  "personality": {
    "openness": 0.65,
    "conscientiousness": 0.75,
    "extraversion": 0.50,
    "agreeableness": 0.55,
    "neuroticism": 0.40
  },
  "learning_styles": {
    "visual_verbal": "visual",
    "sensing_intuitive": "intuitive",
    "active_reflective": "active",
    "sequential_global": "sequential"
  },
  "learning_strategies": {
    "deep_processing": 0.70,
    "elaboration": 0.65,
    "organization": 0.75,
    "metacognition": 0.68
  },
  "learning_element_preferences": {
    "VAM": 0.25,
    "MS": 0.20,
    "EX": 0.18,
    "QU": 0.15,
    "SU": 0.12,
    "LG": 0.10
  },
  "recommended_elements": [
    ["VAM", 0.25],
    ["MS", 0.20],
    ["EX", 0.18]
  ]
}
```

---

## 🎯 **Status**

✅ **Synthetic Data Generator**: Complete
✅ **Nestor Bayesian Profiler**: Complete
✅ **Orchestrator Integration**: Complete
✅ **Fallback Support**: Complete
✅ **Documentation**: Complete

**Ready to use!** 🚀








