# Getting Started with Personalized Learning System

This notebook guides you through using the system.

## Installation

```bash
pip install -r requirements.txt
python scripts/quick_start.py
```

## Starting the System

```bash
python api/server.py
```

## Basic Usage

### 1. Send a Debugging Session

```python
import requests

session = {
    "student_id": "student_001",
    "code": """
def factorial(n):
    return n * factorial(n - 1)  # Missing base case!
    """,
    "error_message": "RecursionError",
    "action_sequence": ["code_edit", "run_test", "search_documentation"],
    "time_deltas": [10.0, 2.0, 30.0],
    "time_stuck": 42.0
}

response = requests.post("http://localhost:8000/api/session", json=session)
result = response.json()

print(f"Intervention Type: {result['intervention_type']}")
print(f"Explanation: {result['content']['explanation']}")
```

### 2. Query CSE-KG for Concepts

```python
# Get concept information
concept = requests.get("http://localhost:8000/api/concept/recursion")
print(concept.json())

# Search for concepts
query = {"text": "recursion and base cases"}
results = requests.post("http://localhost:8000/api/query/concepts", json=query)
print(results.json())
```

### 3. Update Student Profile

```python
profile = {
    "student_id": "student_001",
    "personality_responses": {
        "openness": [4, 5, 4, 5, 4],
        "conscientiousness": [5, 5, 4, 5, 5],
        "extraversion": [3, 3, 2, 3, 3],
        "agreeableness": [4, 4, 5, 4, 4],
        "neuroticism": [2, 3, 2, 2, 3]
    }
}

response = requests.post("http://localhost:8000/api/student/profile", json=profile)
```

### 4. Provide Feedback

```python
feedback = {
    "student_id": "student_001",
    "intervention_type": "visual_explanation",
    "effectiveness": 0.85,
    "time_to_success": 120.0
}

response = requests.post("http://localhost:8000/api/feedback", json=feedback)
```

## Training Models

```python
# Load configuration
import yaml
with open('config.yaml') as f:
    config = yaml.safe_load(f)

# Create model
from src.models.hvsae import HVSAE
model = HVSAE(config)

# Load data
from src.data.dataloader import create_dataloaders
import pandas as pd

train_data = pd.read_csv('data/processed/progsnap2_processed.csv')
val_data = train_data.sample(frac=0.2)

loaders = create_dataloaders(config, train_data, val_data)

# Train
# See train.py for full training pipeline
```

## Exploring CSE-KG

```python
from src.knowledge_graph import CSEKGClient

client = CSEKGClient(config)

# Get prerequisites
prereqs = client.get_prerequisites("binary_tree")
print(f"Prerequisites: {prereqs}")

# Find related concepts
related = client.get_related_concepts("sorting", max_distance=1)
for concept, relation, dist in related:
    print(f"{concept} ({relation})")

# Get methods for a task
methods = client.get_methods_for_task("sentiment_analysis")
for method in methods:
    print(method['label'])
```

## Next Steps

- Explore the full API at http://localhost:8000/docs
- Check SYSTEM_OVERVIEW.md for architecture details
- Read DATASETS.md to understand the data
- Customize config.yaml for your needs




















