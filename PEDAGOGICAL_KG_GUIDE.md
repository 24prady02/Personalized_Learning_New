# Pedagogical Knowledge Graph Guide

## Overview

The **Pedagogical-CS Knowledge Graph** is a unified knowledge structure that combines:
1. **CS Domain Knowledge** (from CSE-KG 2.0) - Programming concepts, methods, tasks
2. **Cognitive/Learning Needs** - Misconceptions, learning progressions, cognitive load, interventions

This creates a comprehensive knowledge graph that understands both **what** students need to learn (domain knowledge) and **how** they learn it (pedagogical needs).

---

## Architecture

### Components

```
Pedagogical-CS Knowledge Graph
├── CSE-KG 2.0 (Domain Knowledge)
│   ├── Concepts (recursion, OOP, algorithms)
│   ├── Prerequisites (requiresKnowledge)
│   └── Relationships (relatedTo, usesMethod)
│
└── Pedagogical Extensions
    ├── Misconceptions Database
    ├── Learning Progressions
    ├── Cognitive Load Information
    └── Intervention Mappings
```

### Schema

The graph extends CSE-KG with new node types and relationships:

**Node Types:**
- `concept` - CS concepts (from CSE-KG + pedagogical metadata)
- `misconception` - Common student misconceptions
- `intervention` - Pedagogical interventions
- `progression` - Learning progression paths

**Relationships:**
- `hasMisconception` - Concept → Misconception
- `addressesMisconception` - Intervention → Misconception
- `recommendsIntervention` - Concept → Intervention
- `precedesInProgression` - Concept → Concept (in learning order)
- `hasCognitiveLoad` - Concept → Cognitive Load metadata

---

## Usage

### Basic Setup

```python
from src.knowledge_graph import PedagogicalKGIntegration
import yaml

# Load config
with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

# Initialize
pedagogical_kg = PedagogicalKGIntegration(config)
```

### Get Complete Concept Information

```python
# Get both domain knowledge AND pedagogical data
concept_info = pedagogical_kg.get_concept_full_info("recursion")

print(concept_info)
# {
#     "concept": "recursion",
#     "domain_knowledge": {
#         "label": "Recursion",
#         "description": "...",
#         "prerequisites": ["functions", "conditional_statements"],
#         "related_concepts": [...]
#     },
#     "pedagogical_data": {
#         "cognitive_load": {
#             "total": 5,
#             "intrinsic": 5,
#             "factors": ["abstract", "recursive_thinking"]
#         },
#         "common_misconceptions": [...],
#         "recommended_interventions": [...],
#         "typical_struggles": [...]
#     }
# }
```

### Detect Student Misconceptions

```python
# Student code with missing base case
student_code = """
def factorial(n):
    return n * factorial(n - 1)  # Missing base case!
"""

error_message = "RecursionError: maximum recursion depth exceeded"

# Detect misconception
misconception_info = pedagogical_kg.detect_student_misconception(
    concept="recursion",
    code=student_code,
    error_message=error_message
)

if misconception_info:
    print(f"Detected: {misconception_info['misconception']['description']}")
    print(f"Severity: {misconception_info['misconception']['severity']}")
    print(f"Recommended interventions: {len(misconception_info['recommended_interventions'])}")
```

### Get Learning Path

```python
# Student's current mastery
current_mastery = {
    "functions": 0.9,
    "conditional_statements": 0.85,
    "recursion_intro": 0.3,  # Struggling
    "base_case": 0.2,  # Not mastered
    "recursion": 0.1  # Goal
}

# Get learning path to recursion
path = pedagogical_kg.get_learning_path(
    target_concept="recursion",
    current_mastery=current_mastery
)

print(f"Next concept to learn: {path['next_concept']}")
for step in path['path']:
    print(f"  {step['concept']}: mastery={step['current_mastery']:.2f}, "
          f"ready={step['ready']}, time={step['estimated_time_hours']}h")
```

### Get Recommended Interventions

```python
# Student is struggling with recursion
interventions = pedagogical_kg.get_interventions_for_struggle(
    concept="recursion",
    struggle_type="missing_base_case"
)

# Sort by effectiveness
for intv in interventions:
    print(f"{intv['name']} ({intv['type']}): "
          f"effectiveness={intv['effectiveness']:.2f}")
```

### Get Cognitive Load Information

```python
# Check cognitive load before teaching a concept
load_info = pedagogical_kg.get_cognitive_load_info("recursion")

print(f"Total cognitive load: {load_info['total_load']}/5")
print(f"Factors: {load_info['factors']}")
print(f"Difficulty: {load_info['difficulty_level']}")

# High load? Consider breaking it down or using scaffolding
if load_info['total_load'] >= 4:
    print("⚠️ High cognitive load - use scaffolding!")
```

---

## Data Structure

### Misconceptions

Stored in `data/pedagogical_kg/misconceptions.json`:

```json
{
  "id": "mc_recursion_no_base_case",
  "concept": "recursion",
  "description": "Believes recursion doesn't need a base case",
  "common_indicators": [
    "infinite recursion",
    "RecursionError",
    "missing if statement before recursive call"
  ],
  "severity": "critical",
  "frequency": 0.7,
  "related_concepts": ["base_case", "conditional_statements"],
  "correction_strategy": "Explain base case necessity with examples"
}
```

### Learning Progressions

Stored in `data/pedagogical_kg/learning_progressions.json`:

```json
{
  "id": "prog_recursion_basics",
  "concept_sequence": [
    "functions",
    "conditional_statements",
    "recursion_intro",
    "base_case",
    "recursion"
  ],
  "difficulty_levels": [1, 1, 2, 2, 3],
  "prerequisites": {
    "recursion_intro": ["functions", "conditional_statements"],
    "base_case": ["recursion_intro"],
    "recursion": ["base_case", "recursion_intro"]
  },
  "estimated_time": {
    "functions": 2.0,
    "conditional_statements": 1.5,
    "recursion_intro": 3.0,
    "base_case": 2.0,
    "recursion": 4.0
  },
  "mastery_thresholds": {
    "functions": 0.8,
    "conditional_statements": 0.8,
    "recursion_intro": 0.7,
    "base_case": 0.85,
    "recursion": 0.8
  }
}
```

### Cognitive Loads

Stored in `data/pedagogical_kg/cognitive_loads.json`:

```json
{
  "concept": "recursion",
  "intrinsic_load": 5,
  "extraneous_load": 3,
  "germane_load": 4,
  "total_load": 5,
  "factors": ["abstract", "recursive_thinking", "call_stack"]
}
```

### Interventions

Stored in `data/pedagogical_kg/interventions.json`:

```json
{
  "id": "int_base_case_example",
  "name": "Base Case Example",
  "type": "example",
  "target_concept": "recursion",
  "target_misconception": "mc_recursion_no_base_case",
  "description": "Show concrete example of base case in recursion",
  "content_template": "Let's look at a recursive function with a base case: {example}",
  "prerequisites": ["functions"],
  "effectiveness_score": 0.8,
  "usage_count": 0
}
```

---

## Integration with Existing System

### With DINA Model

```python
# Get mastery from DINA
mastery = dina_model.get_student_mastery(student_id)

# Get learning path based on mastery
path = pedagogical_kg.get_learning_path("recursion", mastery)

# Identify knowledge gaps
for step in path['path']:
    if not step['ready']:
        print(f"Gap: {step['concept']} (mastery={step['current_mastery']:.2f})")
```

### With CodeBERT Analysis

```python
# Analyze code
code_analysis = codebert.analyze_code(student_code)

# Detect misconceptions from errors
if code_analysis['errors']:
    misconception = pedagogical_kg.detect_student_misconception(
        concept="recursion",
        code=student_code,
        error_message=code_analysis['error_message']
    )
```

### With Intervention Orchestrator

```python
# Get recommended interventions
interventions = pedagogical_kg.get_interventions_for_struggle(
    concept="recursion",
    misconception_id="mc_recursion_no_base_case"
)

# Select best intervention
best_intervention = max(interventions, key=lambda x: x['effectiveness'])

# Generate personalized content
content = generate_intervention_content(
    intervention=best_intervention,
    student_context=student_data
)
```

---

## Extending the Graph

### Adding New Misconceptions

```python
from src.knowledge_graph import PedagogicalKGBuilder

# Load builder
builder = PedagogicalKGBuilder(cse_kg_client, config)

# Add new misconception
new_mc = Misconception(
    id="mc_new_misconception",
    concept="loops",
    description="Believes loops always start at 0",
    common_indicators=["range(0, n)", "off-by-one errors"],
    severity=MisconceptionSeverity.MEDIUM,
    frequency=0.5
)

builder.misconceptions[new_mc.id] = new_mc
builder._save_misconceptions()
```

### Adding New Learning Progressions

```python
# Create new progression
new_prog = LearningProgression(
    id="prog_oop_basics",
    concept_sequence=["classes", "objects", "methods", "inheritance"],
    difficulty_levels=[DifficultyLevel.BEGINNER, DifficultyLevel.BEGINNER,
                      DifficultyLevel.INTERMEDIATE, DifficultyLevel.ADVANCED],
    prerequisites={
        "objects": ["classes"],
        "methods": ["objects"],
        "inheritance": ["methods"]
    },
    estimated_time={"classes": 3.0, "objects": 2.0, "methods": 4.0, "inheritance": 5.0},
    mastery_thresholds={"classes": 0.8, "objects": 0.8, "methods": 0.75, "inheritance": 0.8}
)

builder.learning_progressions[new_prog.id] = new_prog
builder._save_progressions()
```

---

## Benefits

1. **Unified Knowledge**: Single source of truth for both domain and pedagogical knowledge
2. **Misconception Detection**: Automatically detect common student errors
3. **Personalized Learning Paths**: Recommend optimal learning sequences
4. **Cognitive Load Awareness**: Adjust teaching based on concept difficulty
5. **Intervention Mapping**: Link struggles to effective interventions
6. **Extensible**: Easy to add new misconceptions, progressions, and interventions

---

## Next Steps

1. **Populate with More Data**: Add more misconceptions, progressions, and interventions
2. **Learn from Data**: Use student interaction data to refine misconceptions and interventions
3. **Integration**: Integrate with RL agent to learn optimal intervention selection
4. **Visualization**: Create visual representations of the knowledge graph












