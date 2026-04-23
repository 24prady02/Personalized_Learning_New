# How Pedagogical KG and COKE Are Currently Used

## 🎯 Overview

Both **Pedagogical Knowledge Graph** and **COKE (Cognitive Knowledge Graph)** are integrated into the system's content generation pipeline to provide personalized, adaptive explanations.

---

## 📊 PEDAGOGICAL KNOWLEDGE GRAPH - How It's Used

### **1. Initialization** (`src/knowledge_graph/adaptive_explanation_generator.py`)

```python
# Line 64-65
from .pedagogical_kg_integration import PedagogicalKGIntegration
self.pedagogical_kg = PedagogicalKGIntegration(self.config)
```

**What it loads:**
- ✅ Misconceptions (from `misconceptions.json` - learned from CodeNet + ASSISTments)
- ✅ Learning Progressions (from `learning_progressions.json` - learned from MOOCCubeX)
- ✅ Cognitive Loads (from `cognitive_loads.json` - learned from ASSISTments + ProgSnap2)
- ✅ Interventions (from `interventions.json` - learned from ASSISTments + ProgSnap2)

---

### **2. During Content Generation** (`src/orchestrator/orchestrator.py`)

#### **Step 1: Query Pedagogical KG** (Lines 757-814)

```python
# Get Pedagogical KG information
pedagogical_kg_info = {}
if adaptive_explainer and adaptive_explainer.pedagogical_kg:
    # Query for full concept info
    concept_full_info = adaptive_explainer.pedagogical_kg.get_concept_full_info(concept)
    
    # Get misconceptions
    misconceptions = adaptive_explainer.pedagogical_kg.get_misconceptions_for_concept(concept)
    
    # Get cognitive load
    cognitive_load = adaptive_explainer.pedagogical_kg.get_cognitive_load_info(concept)
    
    # Get learning progression
    progression = concept_full_info.get('learning_progression', {})
    
    # Get recommended interventions
    interventions = concept_full_info.get('interventions', [])
```

**What it retrieves:**
- ✅ **Misconceptions**: Common errors students make with this concept
- ✅ **Cognitive Load**: How difficult this concept is (intrinsic/extraneous/germane)
- ✅ **Learning Progression**: What concepts should be learned before this
- ✅ **Interventions**: What teaching strategies work best for this concept

#### **Step 2: Pass to Enhanced Generator** (Lines 816-832)

```python
analysis = {
    'pedagogical_kg': pedagogical_kg_info,  # ← Passed here
    'cse_kg': cse_kg_info,
    'coke': coke_info,
    # ...
}

# Generate response with Pedagogical KG info
enhanced_response = self.models['enhanced_generator'].generate_personalized_response(
    analysis=analysis,  # ← Contains pedagogical_kg_info
    # ...
)
```

#### **Step 3: Used in Prompt Engineering** (`src/orchestrator/enhanced_personalized_generator.py`)

```python
# Lines 837-845
pedagogical_kg_info = analysis.get('pedagogical_kg', {})
if pedagogical_kg_info:
    prompt_parts.append(f"  - Learning Progression: {pedagogical_kg_info.get('progression', 'N/A')}")
    
    misconceptions = pedagogical_kg_info.get('misconceptions', [])
    if misconceptions:
        prompt_parts.append(f"  - Common Misconceptions: {', '.join(misconceptions)}")
    
    prompt_parts.append(f"  - Cognitive Load Level: {pedagogical_kg_info.get('cognitive_load', 'N/A')}")
    prompt_parts.append(f"  - Recommended Interventions: {', '.join(pedagogical_kg_info.get('interventions', []))}")
```

**Result:** The LLM (Groq) receives:
- ✅ What misconceptions to address
- ✅ How to manage cognitive load
- ✅ What learning path to follow
- ✅ Which interventions to use

---

### **3. Dynamic Learning** (`src/orchestrator/orchestrator.py` - Lines 222-279)

After each session, the system **learns** from student behavior:

```python
# 1. Learn misconceptions
learned_mc = pedagogical_builder.learn_from_session(
    code=code,
    error_message=error_message,
    concept=concept
)

# 2. Learn cognitive load
learned_load = pedagogical_builder.learn_cognitive_load_from_session(
    concept=concept,
    session_data=session_data
)

# 3. Learn learning progression
pedagogical_builder.learn_progression_from_session(
    concept_sequence=concepts_learned,
    student_mastery=mastery_profile
)
```

**Result:** Graphs update automatically from every session!

---

## 🧠 COKE (Cognitive Knowledge Graph) - How It's Used

### **1. Initialization** (`src/knowledge_graph/adaptive_explanation_generator.py`)

```python
# Lines 70-78
self.coke_graph = None
if self.config.get('coke', {}).get('enabled', False):
    try:
        from .coke_cognitive_graph import COKECognitiveGraph
        self.coke_graph = COKECognitiveGraph(self.config.get('coke', {}))
    except Exception as e:
        print(f"[WARN] COKE graph not available: {e}")
```

**What it loads:**
- ✅ Cognitive Chains (from `coke_chains.json` - learned from ProgSnap2)
- ✅ State transitions (mental activity → behavioral response)
- ✅ Theory of Mind patterns

---

### **2. During Content Generation** (`src/orchestrator/orchestrator.py`)

#### **Step 1: Predict Cognitive State** (Lines 659-715)

```python
# Get COKE cognitive state
coke_cognitive_state = None
coke_info = {}
if adaptive_explainer and adaptive_explainer.coke_graph:
    # Predict cognitive state from conversation
    coke_cognitive_state = adaptive_explainer.coke_graph.predict_cognitive_state(student_data)
    
    # Get behavioral response prediction
    behavioral_response = adaptive_explainer.coke_graph.predict_behavioral_response(
        coke_cognitive_state, 
        student_data
    )
    
    # Get cognitive chain
    chains = adaptive_explainer.coke_graph.get_cognitive_chains_for_state(coke_cognitive_state)
```

**What it predicts:**
- ✅ **Cognitive State**: `confused`, `frustrated`, `engaged`, `understanding`, `insight`
- ✅ **Behavioral Response**: `ask_question`, `continue`, `search_info`, `explain`
- ✅ **Cognitive Chain**: Mental activity → Behavioral response pattern

#### **Step 2: Pass to Enhanced Generator** (Lines 816-832)

```python
analysis = {
    'coke': coke_info,  # ← Contains cognitive state, behavioral response
    'pedagogical_kg': pedagogical_kg_info,
    'cse_kg': cse_kg_info,
    # ...
}
```

#### **Step 3: Used in Prompt Engineering** (`src/orchestrator/enhanced_personalized_generator.py`)

```python
# Lines 848-859
coke_info = analysis.get('coke', {})
if coke_info:
    prompt_parts.append("\n[COKE - Cognitive Knowledge Graph for Theory of Mind]")
    prompt_parts.append(f"  - Cognitive State: {coke_info.get('cognitive_state', 'N/A')}")
    prompt_parts.append(f"  - Mental Activity: {coke_info.get('mental_activity', 'N/A')}")
    prompt_parts.append(f"  - Behavioral Response: {coke_info.get('behavioral_response', 'N/A')}")
    prompt_parts.append(f"  - Confidence: {coke_info.get('confidence', 0.5):.2f}")
    prompt_parts.append("  - MUST: Use COKE cognitive state to understand student's mental state and adapt explanation accordingly")
```

**Result:** The LLM adapts its explanation based on:
- ✅ Student's **mental state** (confused → simpler language)
- ✅ **Predicted behavior** (will ask question → prepare answer)
- ✅ **Theory of Mind** (why student went wrong cognitively)

---

### **3. Cognitive State Inference** (`src/orchestrator/orchestrator.py` - Lines 998-1033)

```python
def _infer_cognitive_state_from_conversation(self, session_data: Dict, behavioral_analysis: Dict) -> str:
    # Try COKE graph if available
    adaptive_explainer = self.models.get('adaptive_explainer')
    if adaptive_explainer and adaptive_explainer.coke_graph:
        cognitive_state = adaptive_explainer.coke_graph.predict_cognitive_state(session_data)
        return cognitive_state.value
```

**Used for:**
- ✅ Selecting intervention type
- ✅ Adjusting explanation complexity
- ✅ Determining urgency

---

### **4. Dynamic Learning** (`src/knowledge_graph/coke_cognitive_graph.py`)

COKE learns automatically when `infer_theory_of_mind()` is called:

```python
def infer_theory_of_mind(self, student_data: Dict) -> Dict:
    # Predict cognitive state
    cognitive_state = self.predict_cognitive_state(student_data)
    
    # Predict behavioral response
    behavioral_response = self.predict_behavioral_response(cognitive_state, student_data)
    
    # Learn from this interaction (called by orchestrator)
    self.learn_from_session(student_data, cognitive_state, behavioral_response)
```

**Result:** Cognitive chains update from every student interaction!

---

## 🔄 Complete Flow: How They Work Together

### **Session Processing Pipeline:**

```
1. Student submits code with error
   ↓
2. Orchestrator calls AdaptiveExplanationGenerator
   ↓
3. COKE predicts cognitive state (confused/frustrated/engaged)
   ↓
4. Pedagogical KG retrieves:
   - Misconceptions for this concept
   - Cognitive load level
   - Learning progression
   - Recommended interventions
   ↓
5. All info passed to Enhanced Generator (Groq LLM)
   ↓
6. LLM generates personalized explanation using:
   - COKE cognitive state (adapt language)
   - Pedagogical KG misconceptions (address errors)
   - Pedagogical KG cognitive load (manage difficulty)
   - Pedagogical KG interventions (use best strategy)
   ↓
7. Response delivered to student
   ↓
8. System learns from session:
   - COKE: Updates cognitive chains
   - Pedagogical KG: Updates misconceptions, cognitive load, progressions
```

---

## 📈 What Gets Learned Dynamically

### **Pedagogical KG Learns:**
1. ✅ **Misconceptions**: New error patterns from student code
2. ✅ **Cognitive Load**: Actual struggle time → load levels
3. ✅ **Learning Progressions**: Real mastery sequences
4. ✅ **Intervention Effectiveness**: Which strategies work

### **COKE Learns:**
1. ✅ **Cognitive Chains**: Mental state → behavior patterns
2. ✅ **State Transitions**: How students move between cognitive states
3. ✅ **Theory of Mind**: Better prediction of student mental models

---

## 🎯 Key Methods Called

### **Pedagogical KG:**
- `get_concept_full_info(concept)` - Get all info for a concept
- `get_misconceptions_for_concept(concept)` - Get misconceptions
- `get_cognitive_load_info(concept)` - Get cognitive load
- `learn_from_session()` - Learn misconceptions
- `learn_cognitive_load_from_session()` - Learn cognitive load
- `learn_progression_from_session()` - Learn progressions

### **COKE:**
- `predict_cognitive_state(student_data)` - Predict mental state
- `predict_behavioral_response(state, data)` - Predict behavior
- `infer_theory_of_mind(student_data)` - Full Theory of Mind analysis
- `get_cognitive_chains_for_state(state)` - Get chains for state
- `learn_from_session()` - Learn cognitive chains

---

## ✅ Summary

**Pedagogical KG** = **WHAT** to teach (misconceptions, progressions, interventions)
**COKE** = **HOW** to teach (cognitive state, mental model, behavioral prediction)

**Together:** They enable the system to:
- ✅ Understand student's mental state (COKE)
- ✅ Know what errors to address (Pedagogical KG)
- ✅ Adapt explanation complexity (COKE + Pedagogical KG)
- ✅ Use best teaching strategies (Pedagogical KG)
- ✅ Continuously improve from every session (Both)

**Result:** Truly personalized, adaptive, continuously learning teaching system! 🎓








