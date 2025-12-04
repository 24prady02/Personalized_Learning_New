# Nestor Dataset Training Guide

## Overview

According to the Nestor research paper (ECSEE 2025), the Nestor Bayesian Network **must be trained on datasets** to learn Conditional Probability Tables (CPTs) for accurate inference. The current implementation has the capability but is not using it.

## Current Status

### ✅ What Exists
- `NestorBayesianNetwork.fit()` method in `src/models/nestor/model.py`
- Supports Maximum Likelihood Estimation (MLE) and Bayesian Estimation
- Can learn CPDs from pandas DataFrames

### ❌ What's Missing
- `NestorWrapper` does NOT call `fit()` during initialization
- No dataset preparation for Nestor training
- No integration with existing dataset processors
- Currently uses heuristic/rule-based inference instead of trained BN

## Required Dataset Format

Based on the Nestor paper, the training dataset should contain:

### Variables (Columns)
1. **Big Five Personality Traits** (P1-P5):
   - `personality_openness`: low/medium/high
   - `personality_conscientiousness`: low/medium/high
   - `personality_extraversion`: low/medium/high
   - `personality_agreeableness`: low/medium/high
   - `personality_neuroticism`: low/medium/high

2. **Felder-Silverman Learning Style Dimensions** (D1-D4):
   - `style_visual_verbal`: visual/verbal
   - `style_active_reflective`: active/reflective
   - `style_sequential_global`: sequential/global
   - `style_sensing_intuitive`: sensing/intuitive (if included)

3. **LISTK Learning Strategies** (T1-T4):
   - `strategy_elaboration`: low/medium/high
   - `strategy_organization`: low/medium/high
   - `strategy_critical_thinking`: low/medium/high
   - `strategy_metacognitive_self_regulation`: low/medium/high
   - `strategy_time_management`: low/medium/high

4. **Learning Elements** (L):
   - `learning_element`: BO/LG/MS/SU/EX/QU/VAM/TAM/AAM (9 distinct states)

5. **Emotional State**:
   - `emotional_state`: frustrated/engaged/confused/systematic/exploratory

### Example Dataset Structure

```csv
personality_openness,personality_conscientiousness,personality_extraversion,personality_agreeableness,personality_neuroticism,style_visual_verbal,style_active_reflective,style_sequential_global,strategy_elaboration,strategy_organization,strategy_critical_thinking,strategy_metacognitive_self_regulation,strategy_time_management,emotional_state,learning_element
high,high,medium,high,low,visual,active,sequential,high,high,medium,high,high,engaged,EX
medium,high,low,medium,medium,verbal,reflective,global,medium,high,high,medium,medium,engaged,LG
high,medium,high,high,low,visual,active,sequential,high,medium,high,high,medium,frustrated,MS
...
```

## Implementation Steps

### Step 1: Create Dataset Processor

Create `src/data/processors/nestor_processor.py`:

```python
"""
Processor for Nestor training dataset
Collects personality, learning style, strategy, and intervention preference data
"""

import pandas as pd
from pathlib import Path
from typing import Dict, Optional

class NestorProcessor:
    """Process datasets for Nestor Bayesian Network training"""
    
    def __init__(self, data_dir: str, config: Dict):
        self.data_dir = Path(data_dir)
        self.config = config
        
    def process(self) -> pd.DataFrame:
        """
        Process and combine data from multiple sources:
        - MOOCCubeX: Student-course interactions
        - ProgSnap2: Behavioral patterns
        - Custom questionnaires: Personality and learning style data
        """
        # Load and combine data sources
        # Map to Nestor variable format
        # Return DataFrame with all required columns
        pass
```

### Step 2: Update NestorWrapper

Modify `src/knowledge_graph/nestor_wrapper.py`:

```python
def _initialize_nestor(self):
    """Initialize Nestor components"""
    try:
        from src.models.nestor import NestorBayesianNetwork
        
        # Initialize BN
        nestor_config = self.config.get('nestor', {})
        self.nestor_model = NestorBayesianNetwork(nestor_config)
        
        # Load training dataset
        training_data_path = self.config.get('nestor', {}).get('training_data_path')
        if training_data_path and Path(training_data_path).exists():
            training_data = pd.read_csv(training_data_path)
            
            # Fit the Bayesian Network
            method = self.config.get('nestor', {}).get('training_method', 'bayes')
            self.nestor_model.fit(training_data, method=method)
            
            print(f"[OK] Nestor BN trained on {len(training_data)} samples")
        else:
            print("[WARN] No training data found for Nestor, using untrained model")
            # Could use synthetic data generation here (as per paper)
            
    except Exception as e:
        print(f"[WARN] Nestor initialization failed: {e}")
```

### Step 3: Add Synthetic Data Generation

As per the paper, synthetic data can be generated from empirical data using frameworks like Morpheus:

```python
def generate_synthetic_data(empirical_data: pd.DataFrame, size: int = 1000) -> pd.DataFrame:
    """
    Generate synthetic dataset from empirical data
    Uses Bayesian network structure to generate realistic samples
    """
    # Use pgmpy or Morpheus framework
    # Generate synthetic samples maintaining statistical properties
    pass
```

### Step 4: Update Configuration

Add to `config.yaml`:

```yaml
nestor:
  personality_traits: [...]
  learning_styles: [...]
  learning_strategies: [...]
  intervention_types: [...]
  # NEW: Training configuration
  training_data_path: data/processed/nestor_training_data.csv
  training_method: bayes  # 'mle' or 'bayes'
  use_synthetic_data: true
  synthetic_data_size: 1000
  model_save_path: models/nestor_bn.pkl
```

## Using the Official bayesnestor Package

The paper mentions an official Python package: **bayesnestor** (available on PyPI)

### Installation
```bash
pip install bayesNestor
```

### Usage
```python
from bayesnestor import Nestor

# Initialize with structure
nestor = Nestor()

# Load training data
data = pd.read_csv('nestor_training_data.csv')

# Train the network
nestor.fit(data, method='bayes')

# Perform inference
evidence = {
    'personality_openness': 'high',
    'style_visual_verbal': 'visual',
    'emotional_state': 'engaged'
}
recommendations = nestor.infer(evidence)
```

## Dataset Sources

### 1. Collect from Existing Data
- Extract personality/learning style from student questionnaires
- Infer from behavioral patterns (ProgSnap2)
- Map from course interactions (MOOCCubeX)

### 2. Use Paper's Dataset
- Contact authors for the empirical dataset (N=54 mentioned in paper)
- Use their synthetic data generation approach

### 3. Create Synthetic Dataset
- Use Morpheus framework (as mentioned in paper)
- Generate from empirical data using Bayesian network structure
- Validate with cross-validation

## Training Process

### 1. Data Preparation
```python
# Process and combine datasets
processor = NestorProcessor("data/", config)
training_data = processor.process()

# Save processed data
training_data.to_csv("data/processed/nestor_training_data.csv", index=False)
```

### 2. Train Model
```python
from src.models.nestor import NestorBayesianNetwork
import pandas as pd

# Load data
data = pd.read_csv("data/processed/nestor_training_data.csv")

# Initialize and train
nestor = NestorBayesianNetwork(config['nestor'])
nestor.fit(data, method='bayes')  # or 'mle'

# Save trained model
nestor.save("models/nestor_bn.pkl")
```

### 3. Evaluate Performance
As per paper, use:
- **Log-likelihood** for parameter evaluation
- **BIC** for structural evaluation  
- **Hamming Distance** for prediction evaluation
- **Cross-validation** (leave-one-out)

## Next Steps

1. ✅ Create `NestorProcessor` class
2. ✅ Update `NestorWrapper` to call `fit()`
3. ✅ Add dataset collection/preparation scripts
4. ✅ Integrate with existing dataset pipeline
5. ✅ Add synthetic data generation option
6. ✅ Update documentation
7. ✅ Add evaluation metrics

## References

- **Nestor Paper**: Nadimpalli et al. (2025). "Nestor: A Personalized Learning Path Recommendation Algorithm for Adaptive Learning Environments." ECSEE 2025.
- **bayesnestor Package**: https://pypi.org/project/bayesNestor/
- **Morpheus Framework**: For synthetic data generation








