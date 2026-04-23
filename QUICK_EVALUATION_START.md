# Quick Start: Evaluation and Validation

## 🚀 Getting Started (5 Steps)

### Step 1: Run Basic System Test

```bash
python scripts/start_evaluation.py
```

This will:
- Test if your system processes sessions correctly
- Check which components are working
- Measure processing time
- Identify any errors

**Expected Output**: Success rate, component usage, processing times

---

### Step 2: Create Test/Validation Splits

```python
# Create this script: scripts/prepare_evaluation_datasets.py
# (See EVALUATION_AND_VALIDATION_GUIDE.md for full code)

python scripts/prepare_evaluation_datasets.py
```

This creates:
- `data/evaluation/train.json` (70%)
- `data/evaluation/validation.json` (15%)
- `data/evaluation/test.json` (15%)

---

### Step 3: Create Ground Truth Annotations

**Option A: Use Existing Labels** (if available)
- Extract misconceptions from CodeNet buggy code
- Extract knowledge gaps from ASSISTments performance data
- Extract learning styles from ProgSnap2 behavioral patterns

**Option B: Manual Annotation** (for small sample)
- Annotate 50-100 sessions manually
- Focus on misconceptions and knowledge gaps
- Use 2-3 annotators for inter-rater agreement

**Option C: Semi-Automatic** (recommended)
- Use expert rules to create initial annotations
- Manually verify and correct
- Focus on high-confidence cases first

---

### Step 4: Implement First Evaluation Metric

Start with **Misconception Detection** (easiest to evaluate):

```python
# scripts/evaluate_misconception_detection.py
# (See EVALUATION_AND_VALIDATION_GUIDE.md for full code)

python scripts/evaluate_misconception_detection.py
```

**What you need**:
- Test data with student sessions
- Ground truth misconceptions (from Step 3)
- Your system's predictions

**Output**: Precision, Recall, F1-Score, AUC-ROC

---

### Step 5: Compare with Simple Baseline

Implement a simple baseline:

```python
# Baseline: Rule-based misconception detection
def baseline_detect_misconceptions(code, error):
    misconceptions = []
    if "RecursionError" in error:
        misconceptions.append("missing_base_case")
    if "IndexError" in error:
        misconceptions.append("array_bounds")
    if "KeyError" in error:
        misconceptions.append("dictionary_key")
    return misconceptions
```

Compare your system vs. baseline.

---

## 📊 Evaluation Checklist

- [ ] Basic system test passes (Step 1)
- [ ] Test/validation splits created (Step 2)
- [ ] Ground truth annotations created (Step 3)
- [ ] Misconception detection evaluated (Step 4)
- [ ] Baseline comparison done (Step 5)
- [ ] Knowledge gap identification evaluated
- [ ] Learning style inference evaluated
- [ ] Response quality evaluated
- [ ] Statistical significance tests run
- [ ] Human evaluation conducted (even 10-20 evaluators)

---

## 🎯 Minimum Viable Evaluation (For Paper)

To have a publishable paper, you need at least:

1. **One quantitative metric** (e.g., Misconception Detection F1 > 0.70)
2. **Baseline comparison** (your system vs. rule-based or random)
3. **Statistical significance** (p < 0.05)
4. **Small human evaluation** (10-20 responses rated by 2-3 evaluators)

---

## 📈 Expected Timeline

- **Week 1**: Steps 1-3 (setup and data preparation)
- **Week 2**: Step 4-5 (first evaluation metric + baseline)
- **Week 3**: Additional metrics (knowledge gaps, learning style)
- **Week 4**: Human evaluation and statistical analysis
- **Week 5**: Write results section

---

## 🔧 Troubleshooting

**Problem**: System crashes during evaluation
- **Solution**: Fix bugs first (see TypeError in terminal)
- Start with smaller test set (3-5 sessions)

**Problem**: No ground truth annotations
- **Solution**: Start with semi-automatic annotation
- Use existing dataset labels where possible
- Focus on high-confidence cases

**Problem**: Metrics are low
- **Solution**: This is normal! Document it honestly
- Compare with baselines to show relative improvement
- Analyze failure cases

---

## 📚 Full Guide

See `EVALUATION_AND_VALIDATION_GUIDE.md` for:
- Complete evaluation scripts
- All metric definitions
- Statistical analysis methods
- Human evaluation setup

---

## 💡 Tips

1. **Start small**: Evaluate 10-20 sessions first
2. **Focus on one metric**: Get misconception detection working first
3. **Document everything**: Save all results, even failures
4. **Be honest**: Low metrics are okay if you show improvement over baselines
5. **Iterate**: Fix issues, re-run, improve

---

## 🎓 For Research Paper

Your paper needs:
- **Introduction**: Why personalized learning matters
- **Related Work**: What others have done
- **Method**: Your architecture (you have this!)
- **Experiments**: Evaluation setup (follow this guide)
- **Results**: Quantitative metrics (from evaluation)
- **Discussion**: What works, what doesn't, why
- **Conclusion**: Contributions and future work

**You're 60% there!** Just need evaluation results.

