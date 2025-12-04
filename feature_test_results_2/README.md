# Feature Test Results 2 - Real Dataset Tests

This directory contains **real dataset-based tests** that use **actual student questions, code, and errors** from real-life datasets. **NO HARDCODED VALUES** - everything is extracted dynamically from datasets.

## 🎯 Key Features

- ✅ **Real Data**: Uses actual student sessions from ProgSnap2, ASSISTments, CodeNet
- ✅ **Dynamic Processing**: All questions, code, and errors extracted from datasets
- ✅ **Real AI Models**: DINA, CodeBERT, BERT, Nestor (NO FALLBACK)
- ✅ **Comprehensive Metrics**: Mastery, code quality, explanation quality, engagement
- ✅ **No Hardcoding**: Everything generated dynamically from real data

## Purpose

These conversations simulate authentic student-teacher interactions where:
- Students ask questions about code
- Students struggle with debugging
- Students learn new concepts progressively
- The system provides personalized responses based on student state

## Conversation Scenarios

### 1. `conv_001` - Recursion Debugging - Missing Base Case
**Focus**: Recursion fundamentals, base cases, optimization

**Student Profile**:
- Initial Mastery: 25%
- Learning Style: Verbal
- Personality: Moderate openness, high neuroticism

**Conversation Flow**:
1. Student encounters RecursionError (missing base case)
2. Learns about base cases
3. Understands why factorial(0) = 1
4. Applies recursion to Fibonacci
5. Learns about memoization for optimization

**Key Concepts Tested**:
- Recursion fundamentals
- Base case identification
- Recursive thinking
- Algorithm optimization

---

### 2. `conv_002` - Tree Traversal Learning - Understanding DFS vs BFS
**Focus**: Data structures, tree algorithms, traversal methods

**Student Profile**:
- Initial Mastery: 40%
- Learning Style: Visual
- Personality: High openness, low neuroticism, high conscientiousness

**Conversation Flow**:
1. Student creates tree structure, needs traversal help
2. Implements in-order traversal
3. Learns about pre-order and post-order
4. Implements BFS (breadth-first search)
5. Understands when to use DFS vs BFS

**Key Concepts Tested**:
- Binary tree structure
- Tree traversal algorithms
- DFS (Depth-First Search)
- BFS (Breadth-First Search)
- Algorithm selection

---

### 3. `conv_003` - Algorithm Optimization - From O(n²) to O(n log n)
**Focus**: Time complexity, algorithm optimization, hash maps, sorting

**Student Profile**:
- Initial Mastery: 55%
- Learning Style: Active
- Personality: High openness, moderate neuroticism, high conscientiousness

**Conversation Flow**:
1. Student has slow O(n²) two-sum solution
2. Learns hash map optimization to O(n)
3. Learns about better sorting algorithms
4. Implements merge sort
5. Understands trade-offs between algorithms

**Key Concepts Tested**:
- Time complexity analysis
- Hash map optimization
- Sorting algorithms
- Algorithm trade-offs
- Performance optimization

---

## Running the Tests

### Option 1: Real Dataset Tests (Recommended - NO HARDCODING)

Uses actual student data from real datasets:

```bash
# First, download datasets (if not already done)
python scripts/download_datasets.py

# Then run real dataset tests
python run_real_dataset_tests.py
```

This will:
1. Load real datasets (ProgSnap2, ASSISTments, CodeNet)
2. Extract actual student questions, code, and errors
3. Process them dynamically through the system
4. Generate metrics using real AI models
5. Create output similar to feature_001 format

### Option 2: Predefined Conversation Tests

Uses predefined conversation scenarios:

```bash
python run_feature_test_results_2.py
```

This will:
1. Process each conversation turn-by-turn
2. Calculate metrics using real AI models (DINA, CodeBERT, BERT, Nestor)
3. Generate detailed results in JSON format
4. Create summary markdown files
5. Track learning progression

## Output Structure

Each conversation generates:

```
feature_test_results_2/
├── conv_001/
│   ├── results.json          # Detailed turn-by-turn metrics
│   └── SUMMARY.md            # Human-readable summary
├── conv_002/
│   ├── results.json
│   └── SUMMARY.md
├── conv_003/
│   ├── results.json
│   └── SUMMARY.md
└── OVERALL_SUMMARY.md        # Summary of all conversations
```

## Metrics Tracked

For each conversation turn, the system tracks:

1. **Mastery Progression** (DINA Model)
   - Concept mastery scores
   - Overall mastery percentage
   - Mastery changes per turn

2. **Code Quality** (CodeBERT)
   - Syntax correctness
   - Logic errors
   - Code structure quality
   - Best practices adherence

3. **Explanation Quality** (BERT)
   - Completeness
   - Clarity
   - Relevance
   - Educational value

4. **Engagement** (Behavioral Analysis)
   - Proactive behavior
   - Help-seeking patterns
   - Frustration indicators
   - Learning momentum

5. **Student Type** (Nestor)
   - Personality traits (Big Five)
   - Learning styles (Felder-Silverman)
   - Student classification
   - Personalized recommendations

6. **Response Time**
   - Time to generate response
   - System efficiency

## Using Real AI Models

These tests use **real AI models** (not simulated):
- ✅ **DINA Model**: Real cognitive diagnosis
- ✅ **CodeBERT**: Real code analysis
- ✅ **BERT**: Real text understanding
- ✅ **Nestor**: Real personality profiling (NO FALLBACK)
- ✅ **CSE-KG**: Real knowledge graph integration

## Expected Outcomes

After running these tests, you should see:

1. **Learning Progression**: Mastery scores increasing over turns
2. **Code Improvement**: Code quality metrics improving
3. **Personalization**: Responses adapted to student type
4. **Engagement**: Student engagement patterns
5. **Concept Mastery**: Specific concept mastery tracking

## Notes

- These conversations are designed to be realistic and progressive
- Each conversation builds on previous turns
- Metrics are calculated using real AI models
- Results can be used to evaluate system effectiveness
- Can be compared with `feature_test_results/` for consistency

