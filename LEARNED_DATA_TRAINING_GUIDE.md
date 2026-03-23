# Learned Data Training Guide

## 🎯 Overview

The system now **learns from real datasets** instead of using hardcoded logic! This makes the system:
- **Data-driven**: Learns from actual student behavior and code patterns
- **Scalable**: Can learn new misconceptions and cognitive patterns automatically
- **Accurate**: Based on real evidence from thousands of examples

---

## 📊 What Gets Learned

### 1. **Misconceptions from CodeNet**
- Extracts common error patterns from buggy code
- Learns frequency and severity from data
- Identifies correction strategies from correct code examples

### 2. **COKE Chains from ProgSnap2**
- Learns cognitive state → behavioral response patterns
- Extracts from real debugging session action sequences
- Calculates confidence and frequency from evidence

### 3. **Misconceptions from ASSISTments**
- Learns from wrong answer patterns
- Identifies which concepts cause most confusion
- Tracks how many students are affected

---

## 🚀 Quick Start

### Run All Training (Recommended)

```bash
python scripts/train_all_learned_data.py
```

This runs all learning scripts in sequence:
1. Extract misconceptions from CodeNet
2. Learn COKE chains from ProgSnap2
3. Learn misconceptions from ASSISTments
4. Merge all learned data

### Run Individual Scripts

```bash
# Extract misconceptions from CodeNet
python scripts/learn_misconceptions_from_codenet.py

# Learn COKE chains from ProgSnap2
python scripts/learn_coke_chains_from_progsnap2.py

# Learn misconceptions from ASSISTments
python scripts/learn_misconceptions_from_assistments.py

# Merge all learned data
python scripts/merge_learned_data.py
```

---

## 📁 Output Files

After training, learned data is saved to:

```
data/pedagogical_kg/
├── misconceptions.json          # Merged misconceptions (used by system)
├── misconceptions_learned.json  # From CodeNet
├── misconceptions_assistments_learned.json  # From ASSISTments
├── coke_chains.json             # Merged COKE chains (used by system)
└── coke_chains_learned.json     # From ProgSnap2
```

---

## 🔄 How System Uses Learned Data

### Priority Order:

1. **Learned Data** (if available)
   - Loads from `data/pedagogical_kg/misconceptions.json`
   - Loads from `data/pedagogical_kg/coke_chains.json`

2. **Hardcoded Defaults** (fallback)
   - Only used if learned data doesn't exist
   - Provides basic functionality until training completes

### Automatic Detection:

The system automatically detects and uses learned data:
- **PedagogicalKGBuilder**: Checks for `misconceptions.json` on startup
- **COKECognitiveGraph**: Checks for `coke_chains.json` on startup
- Prints status messages indicating which source is used

---

## 📈 What Gets Learned

### From CodeNet:

```python
{
  "id": "mc_recursion_RecursionError",
  "concept": "recursion",
  "description": "Common recursion misconception - missing base case",
  "common_indicators": ["RecursionError", "infinite recursion"],
  "severity": "high",
  "frequency": 0.15,  # Learned from data!
  "evidence_count": 45,  # 45 buggy files showed this pattern
  "source": "codenet"
}
```

### From ProgSnap2:

```python
{
  "id": "chain_confused_to_search_info",
  "mental_activity": "confused",
  "behavioral_response": "search_info",
  "context": "encountering_error",
  "frequency": 0.23,  # Learned from data!
  "confidence": 0.85,  # Based on evidence
  "evidence_count": 234,  # 234 sessions showed this pattern
  "source": "progsnap2"
}
```

### From ASSISTments:

```python
{
  "id": "mc_assistments_addition",
  "concept": "Addition",
  "description": "Common misconception in Addition",
  "frequency": 0.12,  # Learned from wrong answers
  "affected_students": 156,  # 156 students struggled
  "avg_attempts": 2.3,  # Students tried 2.3 times on average
  "source": "assistments"
}
```

---

## 🔧 Configuration

### Data Directories:

Update `config.yaml` if needed:

```yaml
pedagogical_kg:
  data_dir: "data/pedagogical_kg"  # Where learned data is saved
```

### Dataset Paths:

Make sure datasets are in correct locations:
- `data/codenet/` - CodeNet buggy/correct code
- `data/progsnap2/` - ProgSnap2 debugging sessions
- `data/assistments/` - ASSISTments student responses

---

## 📊 Training Statistics

After training, you'll see:

```
SUMMARY
============================================================
Total buggy files analyzed: 500+
Misconceptions extracted: 25
Total sessions analyzed: 10,000+
Cognitive chains extracted: 15
Total skills analyzed: 50
```

---

## 🔄 Re-training

To update learned data:

1. **Add new datasets**: Place new data in dataset directories
2. **Re-run training**: `python scripts/train_all_learned_data.py`
3. **Restart system**: System will automatically load new learned data

---

## ⚠️ Troubleshooting

### No Learned Data Found

**Problem**: System uses hardcoded defaults

**Solution**: 
1. Check datasets exist: `ls data/codenet/`, `ls data/progsnap2/`
2. Run training: `python scripts/train_all_learned_data.py`
3. Check output files exist: `ls data/pedagogical_kg/`

### Training Fails

**Problem**: Scripts error out

**Solution**:
1. Check dataset format matches expected structure
2. Verify file permissions
3. Check Python dependencies installed
4. Run individual scripts to isolate issue

### Low Quality Learned Data

**Problem**: Learned data has low evidence counts

**Solution**:
1. Use larger datasets (full CodeNet, full ProgSnap2)
2. Adjust thresholds in learning scripts (min evidence counts)
3. Combine multiple data sources (already done by merge script)

---

## 🎓 Benefits

### Before (Hardcoded):
- ❌ Limited to 4 misconceptions
- ❌ Limited to 5 COKE chains
- ❌ Static, doesn't improve
- ❌ May not match real student behavior

### After (Learned):
- ✅ Learns from 500+ buggy code files
- ✅ Learns from 10,000+ debugging sessions
- ✅ Learns from 50+ skills/concepts
- ✅ Automatically updates with new data
- ✅ Based on real student evidence
- ✅ Scales to new concepts automatically

---

## 📚 Next Steps

1. **Run Training**: `python scripts/train_all_learned_data.py`
2. **Verify Output**: Check `data/pedagogical_kg/` for learned files
3. **Restart System**: System will automatically use learned data
4. **Monitor**: Check console for "[PedagogicalKG] Loaded X misconceptions from learned data"

---

## 🔗 Related Files

- `scripts/learn_misconceptions_from_codenet.py` - CodeNet learner
- `scripts/learn_coke_chains_from_progsnap2.py` - ProgSnap2 learner
- `scripts/learn_misconceptions_from_assistments.py` - ASSISTments learner
- `scripts/merge_learned_data.py` - Data merger
- `scripts/train_all_learned_data.py` - Main training script
- `src/knowledge_graph/pedagogical_kg_builder.py` - Uses learned misconceptions
- `src/knowledge_graph/coke_cognitive_graph.py` - Uses learned COKE chains

---

## ✅ Success Indicators

You'll know it's working when you see:

```
[PedagogicalKG] Loaded 25 misconceptions from learned data
[COKE] Loaded 15 cognitive chains from learned data
```

Instead of:

```
[PedagogicalKG] No learned misconceptions found, using hardcoded defaults
[COKE] No learned cognitive chains found, using hardcoded defaults
```

---

**🎉 Your system is now data-driven and continuously learning!**








