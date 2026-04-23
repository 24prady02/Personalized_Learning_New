# Real Models + CSE-KG 2.0 Integration Guide

## Overview

The `run_real_dataset_tests.py` script processes **real student data** using:
- ✅ **Groq API** for generating responses (with dataset context)
- ✅ **CSE-KG 2.0** for dynamic concept extraction (not keyword matching)
- ✅ **Real AI Models** (DINA, CodeBERT, BERT, Nestor - NO FALLBACK)
- ✅ **Real Datasets** (ProgSnap2, ASSISTments, CodeNet)
- ✅ **Output Format** exactly like `feature_001`

## How It Works

### 1. Groq API Integration

**Input Flow:**
```
Student Question + Code + Error
        ↓
ChatInterface.process_message()
        ↓
Groq API (llama-3.1-8b-instant)
        ↓
Personalized Response
```

**Key Features:**
- Uses Groq API for all responses
- Has access to datasets through system context
- Generates personalized responses based on student state
- No hardcoded responses - all generated dynamically

### 2. CSE-KG 2.0 Concept Extraction

**Dynamic Extraction Process:**
```
Student Question + Code
        ↓
CSEKGConceptExtractor.extract_concepts()
        ↓
CSE-KG 2.0 SPARQL Query
        ↓
Real Concepts from Knowledge Graph
```

**NOT Keyword Matching:**
- ❌ Does NOT use simple keyword matching
- ✅ Queries actual CSE-KG 2.0 SPARQL endpoint
- ✅ Uses graph relationships (requiresKnowledge, usesMethod, etc.)
- ✅ Returns real concepts from knowledge graph

**Fallback Chain:**
1. **Primary**: `CSEKGConceptExtractor` (uses CSE-KG client)
2. **Secondary**: Direct `CSEKGClient.search_concepts()` (SPARQL query)
3. **Last Resort**: Keyword extraction (only if CSE-KG unavailable)

### 3. Real AI Models

All models are **REAL** (not simulated):

| Model | Purpose | Real Implementation |
|-------|---------|-------------------|
| **DINA** | Cognitive diagnosis | `RealDINAModel` - PyTorch DINA model |
| **CodeBERT** | Code analysis | `RealCodeBERT` - HuggingFace CodeBERT |
| **BERT** | Text understanding | `RealBERT` - HuggingFace BERT |
| **Nestor** | Personality profiling | `RealNestor` - NO FALLBACK, uses real PersonalityProfiler |
| **CSE-KG** | Concept extraction | `CSEKGClient` - SPARQL queries to CSE-KG 2.0 |

### 4. Dataset Integration

**Real Data Sources:**
- **ProgSnap2**: Actual debugging sessions with code evolution
- **ASSISTments**: Real student responses and problem-solving attempts
- **CodeNet**: Real code submissions (correct and buggy)

**Dynamic Extraction:**
- Questions generated from event types and errors
- Code extracted from actual student sessions
- Errors from real error messages
- No hardcoded examples

### 5. Output Format

Matches `feature_001/README.md` exactly:

```
# Real Dataset Test - {session_id}

## Feature Information
## Student Profile
## Student Progression Overview
### Progression Summary
## Conversation Results
### Turn 1 - Mastery: X% (+Y%)
**Student Question/Doubt:**
**Concepts Detected:** (from CSE-KG 2.0)
**Student Code:**
**System Response:**
**Learning Outcome Metrics (Enhanced):**
  **Quantitative:**
    - DINA Mastery
    - CodeBERT Analysis
    - BERT Explanation Quality
    - Time Tracking
  **Qualitative:**
    - Question Analysis
    - Behavior Tracking
    - Nestor Student Type Detection
```

## Key Differences from Hardcoded Tests

| Aspect | Hardcoded Tests | Real Dataset Tests |
|--------|----------------|-------------------|
| **Questions** | Predefined | Generated from datasets |
| **Code** | Fixed examples | Extracted from real sessions |
| **Concepts** | Keyword matching | CSE-KG 2.0 graph queries |
| **Responses** | Template-based | Groq API generated |
| **Models** | May be simulated | Always real models |
| **Output** | Predictable | Varies with real data |

## Verification Checklist

✅ **Groq API**: Used for all responses (check `chat.process_message()`)  
✅ **CSE-KG 2.0**: Used for concept extraction (check `cse_kg_extractor.extract_concepts()`)  
✅ **Real Models**: DINA, CodeBERT, BERT, Nestor all real (check imports)  
✅ **No Hardcoding**: All values from datasets (check `RealDatasetLoader`)  
✅ **Output Format**: Matches feature_001 exactly (check `generate_summary_markdown()`)  

## Running the Tests

```bash
# 1. Ensure datasets are downloaded
python scripts/download_datasets.py

# 2. Run real dataset tests
python run_real_dataset_tests.py
```

This will:
1. Load real datasets
2. Extract student sessions dynamically
3. Process through Groq API
4. Extract concepts using CSE-KG 2.0
5. Calculate metrics using real models
6. Generate output in feature_001 format

## Expected Output

Each session generates:
- `results.json`: Detailed metrics (same structure as feature_001)
- `README.md`: Human-readable summary (same format as feature_001)

All metrics are calculated using **real models** and **real data** - no hardcoded values!












